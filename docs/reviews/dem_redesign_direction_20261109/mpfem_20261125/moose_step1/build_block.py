#!/usr/bin/env python3
"""Build moose_step1_block.txt: the WSL paste block for MPFEM step 1 (MOOSE).

Same format as ../moose_wsl/moose_wsl_block.txt: each file goes into ~/moose_step1 through a
quoted heredoc, then one gate line compares the md5 of the written files (fixed order) with
the md5 of the sources; only on a match does it run run_step1.sh.  One changed character
anywhere in the files closes the gate.  Standard library only.
"""
import argparse
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = [("step1_disk.i", "MS1_INPUT_EOF"), ("make_disk_msh.py", "MS1_MESH_EOF"),
         ("check_step1.py", "MS1_CHECK_EOF"), ("run_step1.sh", "MS1_RUN_EOF")]
TARGET = "~/moose_step1"
HEADER = ("# MPFEM 1 단계 MOOSE 블록 (WSL) - 개발 자료 - 파일 넷을 ~/moose_step1 에 쓰고, "
          "md5 가 맞을 때만 돌린다 (스모크 m13 12 걸음 -> m13 -> m26 -> 검사 C P1 P2 P4)")
REFUSE = "⛔ 붙여넣기가 깨짐 (md5 다름) — 아무것도 안 함"


def build():
    parts, md5 = [HEADER, "mkdir -p " + TARGET], hashlib.md5()
    for name, eof in FILES:
        with open(os.path.join(HERE, name), "rb") as f:
            data = f.read()
        text = data.decode("ascii")                 # files are ASCII by design
        if not text.endswith("\n"):
            raise SystemExit("%s must end with a newline" % name)
        if eof in text.splitlines() or "\r" in text:
            raise SystemExit("%s contains its heredoc delimiter or a carriage return" % name)
        if "\t" in text:
            raise SystemExit("%s contains a TAB (a paste can trigger completion)" % name)
        bang = [ln for ln in text.splitlines() if re.search(r"!(?![ =(]|$)", ln)]
        if bang:
            raise SystemExit("%s: '!' could start bash history expansion in a paste: %r"
                             % (name, bang[0]))
        md5.update(data)
        parts.append("cat > %s/%s <<'%s'" % (TARGET, name, eof))
        parts.append(text + eof)
    digest = md5.hexdigest()
    names = " ".join(n for n, _ in FILES)
    parts.append('cd %s && if [ "$(cat %s | md5sum | cut -c1-32)" = %s ]; then '
                 'echo "== gate OK (md5 %s)"; bash run_step1.sh; else echo "%s"; fi'
                 % (TARGET, names, digest, digest, REFUSE))
    return "\n".join(parts) + "\n", digest


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=os.path.join(HERE, "moose_step1_block.txt"))
    args = ap.parse_args(argv)
    text, digest = build()
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("block %s  md5 of files %s  bytes %d" % (args.out, digest, len(text.encode("utf-8"))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
