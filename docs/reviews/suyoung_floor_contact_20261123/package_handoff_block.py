"""Wrap a release-pinned author block together with the three items needed for final handoff."""
import argparse
import base64
import hashlib
import io
import json
from pathlib import Path
import subprocess
import textwrap
import zipfile


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def stage(repo, out, inner):
    root = "docs/reviews/suyoung_floor_contact_20261123/"
    def git(*args,data=None):
        return subprocess.check_output(["git","-c","safe.directory="+repo.as_posix(),"-C",str(repo),*args],input=data)
    def rev(name):
        return git("rev-parse","--verify",name+"^{commit}").decode().strip()
    pin, base = rev("HEAD"),rev("bd8620d10e18")
    parent = base
    files, chain = {}, []
    for n,commit in enumerate(git("rev-list","--reverse",base+".."+pin).decode().splitlines(), 1):
        if git("show","-s","--format=%P",commit).decode().strip() != parent:
            raise ValueError("nonlinear handoff")
        patch = git("format-patch","--stdout","--binary","--full-index","--no-renames","--no-signature","-1",commit)
        name = "patches/%02d_%s.patch" % (n,commit[:12])
        pid = git("patch-id","--stable",data=patch).split()[0].decode()
        other = git("patch-id","--stable",data=git("diff","--binary","--full-index","--no-renames",parent,commit)).split()[0].decode()
        if other != pid or not patch.startswith(b"From "+commit.encode()+b" "):
            raise ValueError("patch identity")
        files[name] = patch
        chain.append(dict(commit=commit,patch_id=pid,patch=name))
        parent = commit
    if not chain or parent != pin:
        raise ValueError("missing release")
    paths = git("diff","-z","--no-renames","--name-only",base,pin).decode().strip("\0").split("\0")
    for path in paths:
        if not path.startswith("docs/") or ".." in Path(path).parts:
            raise ValueError("unexpected delivery path: "+path)
        files["snapshot/"+path] = git("show",pin+":"+path)
    files["CHAIN.json"] = (json.dumps(dict(base=base,release=pin,items=chain),indent=2)+"\n").encode()
    files["HANDOFF.md"] = ("# 반입 순서\n\n바탕 "+base+" · 실행 핀 "+pin+"\n\n"
        +"\n".join(f"- {x['commit']} · patch-id {x['patch_id']}" for x in chain)
        +"\n\n1저자 반입 승인 뒤 이 순서로 cherry-pick -x 한다. 원 생성물은 weekly/에 담는다.\n").encode()
    files["README_CLAUDE.md"] = ("# 수영 아래판 후보와 주간보고\n\n"
        "HANDOFF.md 순서 및 CHAIN.json으로 패치를 대조한다. SHA256SUMS는 자기 자신을 제외한 전체 목록이다. "
        "weekly/weekly_pressure_displacement.png와 weekly/pressure_displacement.csv는 1저자 실행이 실제로 끝난 뒤 묶이는 8칸 270걸음·16칸 540걸음까지의 그림과 네 곡선 원표본이다. "
        "weekly/summary.json에 실행 핀과 새 곡선 해시가 있다. U6(c)·단계 3·3D는 계속 보류한다.\n").encode()
    files["SHA256SUMS"] = "".join(sha(raw)+"  "+name+"\n" for name,raw in sorted(files.items())).encode()
    memory = io.BytesIO()
    with zipfile.ZipFile(memory,"w") as z:
        for name, raw in sorted(files.items()):
            z.writestr(zipfile.ZipInfo(name),raw,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    source_zip = memory.getvalue()
    with zipfile.ZipFile(io.BytesIO(source_zip)) as z:
        if z.testzip() or any(z.read(name) != raw for name,raw in files.items()):
            raise ValueError("incoming code handoff")
    shell = """#!/usr/bin/env bash
set -euo pipefail
umask 077
case "${1:-}" in
  CHECK_ONLY|GO_SUYOUNG_FLOOR_PREFIX_ONCE) ;;
  PACK_ONLY) [[ $# -eq 2 && -d "$2" ]] || { echo 'PACK_ONLY <completed return directory>' >&2; exit 2; } ;;
  *) echo 'Use CHECK_ONLY or GO_SUYOUNG_FLOOR_PREFIX_ONCE with the prior cross return. PACK_ONLY accepts a completed result folder.' >&2; exit 2 ;;
esac
bundle=$(mktemp -d)
"""
    def cat_payload(name, raw):
        return ("base64 -d > \"$bundle/"+name+"\" <<'PAYLOAD'\n"+"\n".join(textwrap.wrap(base64.b64encode(raw).decode(),100))+
                "\nPAYLOAD\nprintf '%s  %s\\n' '"+sha(raw)+"' \"$bundle/"+name+"\" | sha256sum --strict --check --status\n")
    if pin[:12] not in inner.name:
        raise ValueError("inner author script must be release-pinned")
    shell += cat_payload("run.txt",inner.read_bytes())
    shell += cat_payload("code.zip",source_zip)
    shell += cat_payload("finish.py",files["snapshot/"+root+"finish_handoff.py"])
    shell += """if [[ $1 == CHECK_ONLY ]]; then exec bash "$bundle/run.txt" "$@"; fi
if [[ $1 == PACK_ONLY ]]; then
  returned=$(realpath -e -- "$2")
else
  bash "$bundle/run.txt" "$@" | tee "$bundle/field_screen.txt"
  returned=$(sed -n 's/^RETURN_DIRECTORY=//p' "$bundle/field_screen.txt" | tail -n 1)
  [[ -d "$returned" ]] || { echo 'No completed return directory' >&2; exit 3; }
fi
"$HOME/Yonghoon-DEM-DFT/venv/bin/python" -I -B "$bundle/finish.py" "$bundle/code.zip" 'SOURCE_DIGEST' "$returned" 'PIN_VALUE'
""".replace("SOURCE_DIGEST",sha(source_zip)).replace("PIN_VALUE",pin)
    raw = shell.encode("ascii")
    name = out/("PASTE_SUYOUNG_FLOOR_PREFIX_"+pin[:12]+"_1123.txt")
    for f,content in ((name,raw),(Path(str(name)+".sha256"),(sha(raw)+"  "+name.name+"\n").encode())):
        if f.exists() and f.read_bytes()!=content:
            raise ValueError("conflicting author block")
        if not f.exists():
            f.write_bytes(content)
    print(name,sha(raw),"code-set members",len(files)-1)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--repo",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--inner",type=Path,required=True)
    a=p.parse_args()
    a.out.mkdir(parents=True,exist_ok=True)
    stage(a.repo.resolve(),a.out.resolve(),a.inner)
