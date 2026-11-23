"""Make the WSL30-only operator TXT with the previously reviewed shell source as exact bytes."""
import base64
import hashlib
from pathlib import Path
import runpy
import subprocess
import sys
import textwrap
import zlib


def main(repo, out):
    root = Path(repo).resolve().as_posix()
    commit = "9352c4ece10a64a04ffd620062894bd616589582"
    name = "docs/reviews/lhs_pressure_inventory_20261104/pressure_inventory.sh"
    source = subprocess.check_output(["git", "-c", "safe.directory=" + root, "-C", root,
                                      "show", commit + ":" + name])
    checkfile = Path(__file__).with_name("check_live_metadata.py")
    if hashlib.sha256(source).hexdigest() != runpy.run_path(str(checkfile))["SCANNER_SHA"]:
        raise ValueError("sealed source does not match")
    payload = base64.b64encode(zlib.compress(source, 9)).decode("ascii")
    lines = "\n".join('    "' + s + '"' for s in textwrap.wrap(payload, 96))
    start = """#!/usr/bin/env bash
# WSL30 structural inventory only. Local WSL, one CPU, no wall-clock timeout or retry.
# Only the operator return is written, in a new directory under the user's home.
set -eu
if [ "$#" -ne 1 ] || [ "$1" != GO_LHS_WSL30_PRESSURE_INVENTORY_ONCE ]; then
    printf '%s\\n' 'HOLD: expected GO_LHS_WSL30_PRESSURE_INVENTORY_ONCE' >&2
    exit 2
fi
export LC_ALL=C
umask 077
exec /usr/bin/python3 -I -B - <<'LHS_LIVE'
"""
    end = """
import base64
import datetime
import hashlib
import os
from pathlib import Path
import platform
import pwd
import subprocess
import sys
import tempfile
import zipfile
import zlib


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


source = zlib.decompress(base64.b64decode(SOURCE, validate=True))
if sha(source) != SCANNER_SHA or "microsoft" not in platform.release().lower():
    raise SystemExit("HOLD: source or WSL runtime mismatch")
home = Path(pwd.getpwuid(os.geteuid()).pw_dir)
folder = Path(tempfile.mkdtemp(prefix="lhs_wsl30_pressure_return_", dir=str(home)))
print("WSL30_ONLY COUNTS_AND_BYTES_ONLY", flush=True)
print("RETURN_DIRECTORY=" + str(folder), flush=True)
started = utc()
proc = subprocess.run(["/bin/sh", "-s", "--", "wsl"], input=source,
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                      env={"PATH": "/usr/bin:/bin", "LC_ALL": "C"}, check=False)
files = {}
receipt = {"scope": "WSL30", "sealed_scanner_sha256": sha(source),
           "begin_utc": started, "end_utc": utc(), "scanner_process_rc": proc.returncode,
           "execution_identity": "NOT_ESTABLISHED", "canonical_run_segment": "UNSELECTED",
           "section5": "UNRESOLVED", "tau": "NOT_EVALUATED", "value_access": "NOT_GRANTED",
           "v13_release": "NOT_AUTHORIZED", "source_lead_last_reported": "NONE_KNOWN"}
rc = 2
try:
    check(not proc.stderr)
    meta = validate(proc.stdout, proc.returncode)
    receipt.update(status="INVENTORY_COMPLETE", observation=observation(meta),
                   inventory_sha256=sha(proc.stdout))
    files["inventory.json"] = proc.stdout
    rc = 0
except (ValueError, TypeError, KeyError):
    receipt["status"] = "INCOMPLETE"
    receipt["reason"] = "SCANNER_OR_OUTPUT_CONTRACT"
receipt["command_rc"] = rc
files["receipt.json"] = (json.dumps(receipt, sort_keys=True, indent=2) + "\\n").encode("ascii")
files["SHA256SUMS"] = "".join(sha(buf) + "  " + n + "\\n" for n, buf in files.items()).encode("ascii")
archive = folder / "lhs_wsl30_pressure_return.zip"
with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED) as packed:
    for n, buf in files.items():
        packed.writestr(n, buf)
with zipfile.ZipFile(archive) as packed:
    check(packed.testzip() is None and all(packed.read(n) == buf for n, buf in files.items()))
print("SCANNER_RC=" + str(proc.returncode))
print("INVENTORY_STATUS=" + receipt["status"])
print("COMMAND_RC=" + str(rc))
print("RETURN_ZIP=" + str(archive))
print("SHA256=" + sha(archive.read_bytes()))
raise SystemExit(rc)
LHS_LIVE
"""
    text = start + checkfile.read_text(encoding="utf-8") + "\nSOURCE = (\n" + lines + "\n)\n" + end
    data = text.encode("ascii")
    with Path(out).open("xb") as stream:
        stream.write(data)
    print(hashlib.sha256(data).hexdigest(), Path(out).name)


if __name__ == "__main__":
    main(*sys.argv[1:])
