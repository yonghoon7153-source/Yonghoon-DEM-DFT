"""Build the stand-alone author block from the fixed Git metadata and the adjacent reader."""
import base64
import hashlib
import json
from pathlib import Path
import runpy
import subprocess
import sys
import textwrap
import zlib


def main(repo, destination):
    reader_path = Path(__file__).with_name("read_inventory_receipts.py")
    reader = runpy.run_path(str(reader_path))
    raw = {}
    root = Path(repo).resolve().as_posix()
    for name in reader["BLOBS"]:
        raw[name] = subprocess.check_output(
            ["git", "-c", "safe.directory=" + root, "-C", root,
             "show", reader["BASE"] + ":" + name])
    reader["readback"](raw)
    data = {name: base64.b64encode(content).decode("ascii") for name, content in raw.items()}
    encoded = base64.b64encode(zlib.compress(json.dumps(data).encode("ascii"), 9)).decode("ascii")
    payload = "\n".join('    "' + piece + '"' for piece in textwrap.wrap(encoded, 96))
    source = reader_path.read_text(encoding="utf-8")
    start = """#!/usr/bin/env bash
# Operator-only replay of archived WSL30 metadata. CPU 1; expected seconds.
# Prints the report to stdout. Opens no live study files. No transfer or retry.
set -eu
if [ "$#" -ne 1 ] || [ "$1" != GO_LHS_WSL30_INVENTORY_READBACK_ONCE ]; then
    printf '%s\\n' 'HOLD: expected GO_LHS_WSL30_INVENTORY_READBACK_ONCE' >&2
    exit 2
fi
export LC_ALL=C
exec python3 -I -B - <<'LHS_FIXED_RECEIPTS'
"""
    end = """
import sys
try:
    result = readback(unpack_metadata(ENCODED))
except (KeyError, TypeError, ValueError, zlib.error):
    print("HOLD: invalid receipt bytes or metadata", file=sys.stderr)
    raise SystemExit(2)
print(json.dumps(result, ensure_ascii=True, separators=(",", ":")))
LHS_FIXED_RECEIPTS
"""
    block = (start + source + "\nENCODED = (\n" + payload + "\n)\n" + end).encode("ascii")
    with Path(destination).open("xb") as stream:
        stream.write(block)
    print(hashlib.sha256(block).hexdigest(), Path(destination).name)


if __name__ == "__main__":
    main(*sys.argv[1:])
