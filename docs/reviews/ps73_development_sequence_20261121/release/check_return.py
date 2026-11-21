"""Verify author-private ZIP without extracting it or printing research data."""
import hashlib
import json
from pathlib import PurePosixPath
import re
import sys
import zipfile


def verify(path):
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        if len(set(names)) != len(names) or any(
            PurePosixPath(n).is_absolute() or ".." in PurePosixPath(n).parts or "\\" in n for n in names
        ):
            raise ValueError("unsafe or duplicate archive member")
        sums = {}
        for line in z.read("SHA256SUMS").decode("ascii").splitlines():
            digest, name = line.split("  ", 1)
            if not re.fullmatch("[0-9a-f]{64}", digest) or name in sums:
                raise ValueError("invalid checksum row")
            sums[name] = digest
        if set(sums) != set(names) - {"SHA256SUMS"}:
            raise ValueError("archive membership mismatch")
        for name, expected in sums.items():
            h = hashlib.sha256()
            with z.open(name) as member:
                for block in iter(lambda: member.read(1024*1024), b""):
                    h.update(block)
            if h.hexdigest() != expected:
                raise ValueError("member hash mismatch")
        receipt = json.loads(z.read("collection.json"))
        if receipt.get("submitted_by_collection") is not False:
            raise ValueError("unexpected collection scope")
        return {"checked": len(sums), "terminal_reports": receipt["terminal_reports"],
                "captured_utc": receipt["captured_utc"]}


if __name__ == "__main__":
    try:
        print(json.dumps(verify(sys.argv[1]), sort_keys=True))
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as err:
        print("INCOMPLETE_RETURN", err, file=sys.stderr)
        sys.exit(2)
