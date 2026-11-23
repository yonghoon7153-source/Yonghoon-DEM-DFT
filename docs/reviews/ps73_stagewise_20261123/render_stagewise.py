"""Build one WSL operator TXT from the stagewise source in a fixed Git commit."""
import argparse
import base64
import hashlib
from pathlib import Path
import re
import subprocess


REL = "docs/reviews/ps73_stagewise_20261123/ps73_stagewise.py"
TEMPLATE = r'''#!/usr/bin/env bash
set -euo pipefail
umask 077
if (( $# != 1 )); then echo 'Usage: bash THIS.txt CHECK_ONLY|STATUS|GO_TAKEOVER_BEFORE_UT|GO_TAKEOVER_BEFORE_UC|GO_TAKEOVER_BEFORE_UV|GO_TAKEOVER_BEFORE_UTc|RECORD_ONLY|GO_UT_ONCE|GO_UC_ONCE|GO_UVa_ONCE|GO_UVb_ONCE|GO_UTc_ONCE' >&2; exit 2; fi
mode=$1
case "$mode" in CHECK_ONLY|STATUS|GO_TAKEOVER_BEFORE_UT|GO_TAKEOVER_BEFORE_UC|GO_TAKEOVER_BEFORE_UV|GO_TAKEOVER_BEFORE_UTc|RECORD_ONLY|GO_UT_ONCE|GO_UC_ONCE|GO_UVa_ONCE|GO_UVb_ONCE|GO_UTc_ONCE) ;; *) echo 'Unknown action.' >&2; exit 2;; esac
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
fixed=${PS73_FIXED_BLOCK:-"$here/../ps73_unloading_20261121/PASTE_PS73_UNLOADING_2f4c42a3b205.txt"}
if [[ ! -f "$fixed" || -L "$fixed" ]]; then echo 'Set PS73_FIXED_BLOCK to the original 2f4c42a3b205 author TXT.' >&2; exit 2; fi
orig=e0d546d995bb5850a79eb9256de5cee5fb73ec4ced0e6e7033b1418b96c8048c
printf '%s  %s\n' "$orig" "$fixed" | sha256sum --check --status -
out=$(mktemp -d "$HOME/ps73_stagewise_XXXXXXXX")
echo "LOCAL_DIR=$out"
echo 'RELEASE=@PIN@'
sha=@SHA@
base64 -d > "$out/ps73_stagewise.py" <<'SOURCE'
@PAYLOAD@
SOURCE
printf '%s  %s\n' "$sha" "$out/ps73_stagewise.py" | sha256sum --check --status -
if [[ "$mode" == CHECK_ONLY ]]; then echo CHECK_OK; exit 0; fi
# Copy only the connection fields from the verified field block; do not execute it.
host=$(sed -n "s/^IBB='\([^']*\)'$/\1/p" "$fixed")
port=$(sed -n 's/^IBBP=\([0-9]*\)$/\1/p' "$fixed")
if [[ ! "$host" =~ ^[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+$ || ! "$port" =~ ^[0-9]+$ ]]; then echo 'Fixed connection fields missing.' >&2; exit 2; fi
cmd=$(python3 -I -B - "$mode" "$sha" <<'BUILD'
import shlex,sys
loader = ("import hashlib,sys;raw=sys.stdin.buffer.read();"
          "match=hashlib.sha256(raw).hexdigest()==sys.argv[2];"
          "sys.exit(2) if not match else exec(compile(raw,'<ps73_stagewise>','exec'))")
print('exec env -u BASH_ENV -u ENV -u CDPATH -u PYTHONPATH -u PYTHONHOME '
      '"$HOME/.conda/envs/myenv/bin/python3" -I -B -c '+shlex.quote(loader)
      +' '+shlex.quote(sys.argv[1])+' '+shlex.quote(sys.argv[2]))
BUILD
)
rc=0
ssh -T -o ConnectionAttempts=1 -o ConnectTimeout=25 -o ServerAliveInterval=30 -o ServerAliveCountMax=3 -p "$port" "$host" "$cmd" < "$out/ps73_stagewise.py" | tee "$out/response.txt" || rc=$?
printf 'SSH_OR_OPERATION_RC=%s\n' "$rc"
if (( rc != 0 )); then echo 'Use STATUS after a disconnect or unclear acknowledgement; preserve the current job.'; fi
exit "$rc"
'''


def build(repo, pin):
    if not re.fullmatch("[0-9a-f]{40}",pin):
        raise ValueError("pass a full 40-digit commit hash")
    command = ["git","-c","safe.directory="+str(repo.resolve().as_posix()),"-C",str(repo),"show",pin+":"+REL]
    raw = subprocess.run(command,check=True,stdout=subprocess.PIPE).stdout
    return TEMPLATE.replace("@PIN@",pin).replace("@SHA@",hashlib.sha256(raw).hexdigest()).replace(
        "@PAYLOAD@",base64.encodebytes(raw).decode("ascii").strip()).encode("ascii")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo",type=Path)
    parser.add_argument("pin")
    parser.add_argument("out",type=Path)
    opts = parser.parse_args()
    with opts.out.open("xb") as fp:
        fp.write(build(opts.repo,opts.pin))
