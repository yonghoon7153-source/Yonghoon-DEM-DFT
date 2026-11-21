"""Read six existing arms from the fixed first-author archive without extracting."""
import hashlib
import json
from pathlib import Path
import sys
import tarfile


def check(path, expected):
    with path.open("rb") as stream:
        if hashlib.file_digest(stream, "sha256").hexdigest() != expected:
            raise ValueError("prior archive SHA256 differs")
        stream.seek(0)
        with tarfile.open(fileobj=stream, mode="r:gz") as archive:
            members = archive.getmembers()
            if len({m.name for m in members}) != len(members):
                raise ValueError("duplicate prior member")

            def raw(name):
                member = archive.getmember(name)
                if not member.isfile():
                    raise ValueError("unexpected prior member type")
                return archive.extractfile(member).read()

            origin = raw("run/origin.txt").decode("ascii").splitlines()
            if "release=6bdfac91520c868b5036071e6d60464972727f49" not in origin:
                raise ValueError("prior source pin differs")
            inputs = json.loads(raw("run/summary.json"))["inputs"]
            for model in ("S", "F"):
                for cells in (12, 16, 24):
                    name = model + str(cells)
                    folder = "run/arms/" + name + "/"
                    receipt = json.loads(raw(folder + "result.json"))
                    digest = hashlib.sha256(raw(folder + "trace.csv")).hexdigest()
                    if (receipt["arm"] != model or receipt["cells"] != cells or
                            receipt["status"] not in ("TARGET_BRACKETED", "GEOMETRY_LIMIT") or
                            receipt["trace_sha256"] != digest or inputs[name]["trace_sha256"] != digest):
                        raise ValueError("prior receipt or trace differs: " + name)
    print("PRIOR_TRACES_OK=6")


if __name__ == "__main__":
    try:
        check(Path(sys.argv[1]), sys.argv[2])
    except (KeyError, OSError, ValueError, tarfile.TarError) as exc:
        print("Prior input check failed:", exc, file=sys.stderr)
        raise SystemExit(2)
