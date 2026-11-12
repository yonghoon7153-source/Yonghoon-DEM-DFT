#!/usr/bin/env python3
"""restore.py — 컨테이너가 새로 떴을 때 대피 세션의 자리를 다시 만든다 (정본 가지의 evac/ 사본에서).

쓰는 법 (정본 가지를 받은 뒤 · 리포 본 트리의 파일은 건드리지 않는다 — worktree 등록만 한다):

  git -C /home/user/Yonghoon-DEM-DFT fetch origin claude/friendly-meitner-lldvar
  git -C /home/user/Yonghoon-DEM-DFT show origin/claude/friendly-meitner-lldvar:litdb/_curation/evac/tools/restore.py > /tmp/restore.py
  python3 -I /tmp/restore.py --scratch <이 세션의 scratchpad 경로> --uploads <업로드 폴더>

  python3 -I tools/restore.py --write-manifest     # 지금 inbox → tools/received_files.tsv (평소에 · 파일을 새로 받은 뒤)
  python3 -I tools/restore.py --verify             # inbox 를 목록과 견준다 (이름 · 크기 · sha256)

하는 일 (있는 것은 건너뛴다)
  1. 패키지: pymupdf 1.28.2 · pillow · numpy · openpyxl
  2. 작업 트리 셋: litdb-canon · litdb-canon2 · litdb-ctl (sparse — litdb/_curation 만)
  3. scratchpad tools/ · STATE.md 를 정본 evac/ 에서 복사
  4. 업로드 폴더가 남아 있으면 intake.py 로 stage · inbox 를 다시 채움 → 받은 파일 목록과 대조
  5. 참고 저장소 셋 (읽기 전용) 을 다시 받음
  6. 그림 도구 selftest
끝에 "다음에 할 일" 을 찍는다.  커밋 끝 두 줄 (tools/trailer.txt) 은 세션이 손으로 적는다 — 정본에 없다.
"""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

MAIN = Path("/home/user/Yonghoon-DEM-DFT")
BR = "claude/friendly-meitner-lldvar"
REF = f"origin/{BR}"
TREES = [(Path("/home/user/litdb-canon"), "tmp-litdb-evac"), (Path("/home/user/litdb-canon2"), "tmp-litdb-evac2")]
CTL = (Path("/home/user/litdb-ctl"), "tmp-litdb-evac-ctl")
REPOS = [("lescopenaccess/codes-and-data", ""), ("adama-wzr/effectivediffusivityfvm", ""), ("damask-multiphysics/damask", "v2.0.2")]
NAME_RE = re.compile(r"^[0-9a-f]{8}-(\d+(?:-\d+)?)\._{0,2}")


def sh(*cmd, check=False, env=None):
    r = subprocess.run(list(cmd), capture_output=True, text=True, env=env)
    if check and r.returncode:
        sys.exit(f"⛔ {' '.join(cmd)}\n{r.stdout}{r.stderr}")
    return r


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def manifest_rows(inbox):
    rows = []
    for f in sorted(inbox.iterdir()):
        if not f.is_file():
            continue
        m = NAME_RE.match(f.name)
        key = f"N-{m.group(1)}" if m else "?"
        rows.append((key, f.name, str(f.stat().st_size), sha(f), "zip 에서 품" if "_SupZ_" in f.name else "올린 파일"))
    return rows


def write_manifest(scr):
    rows = manifest_rows(TREES[0][0] / "litdb" / "inbox")
    out = scr / "tools" / "received_files.tsv"
    out.write_text("키\t파일 이름\t바이트\tsha256\t어디서\n" + "\n".join("\t".join(r) for r in rows) + "\n", encoding="utf-8")
    print(f"{out} — {len(rows)} 파일 · {sum(int(r[2]) for r in rows) / 1e6:.0f} MB")


def verify(scr, quiet=False):
    mf = scr / "tools" / "received_files.tsv"
    if not mf.is_file():
        print("⚠ 받은 파일 목록 (tools/received_files.tsv) 이 없다")
        return None
    want = [l.split("\t") for l in mf.read_text(encoding="utf-8").split("\n")[1:] if l.strip()]
    res = {}
    for wt, _ in TREES:
        ib = wt / "litdb" / "inbox"
        miss, bad = [], []
        for key, name, size, digest, _src in want:
            p = ib / name
            if not p.is_file():
                miss.append((key, name))
            elif str(p.stat().st_size) != size or sha(p) != digest:
                bad.append((key, name))
        res[str(wt)] = (miss, bad)
        print(f"{ib}: 목록 {len(want)} · 없음 {len(miss)} · 다름 {len(bad)}")
        if not quiet:
            keys = sorted({k for k, _ in miss + bad}, key=lambda s: [int(x) for x in re.findall(r"\d+", s)] or [0])
            if keys:
                print("  없는 / 다른 파일이 있는 키:", " ".join(keys))
    return res


def restore(scr, uploads):
    print("== 1. 패키지")
    r = sh(sys.executable, "-m", "pip", "install", "-q", "pymupdf==1.28.2", "numpy", "openpyxl")
    r2 = sh(sys.executable, "-m", "pip", "install", "-q", "--upgrade", "pillow")
    print("   pip:", "ok" if not (r.returncode or r2.returncode) else (r.stderr + r2.stderr)[-300:])

    print("== 2. 작업 트리")
    sh("git", "-C", str(MAIN), "fetch", "-q", "origin", BR, check=True)
    sh("git", "-C", str(MAIN), "worktree", "prune")
    for wt, br in TREES:
        if (wt / ".git").exists():
            print(f"   있음: {wt}")
            continue
        sh("git", "-C", str(MAIN), "worktree", "add", "-q", "-B", br, str(wt), REF, check=True)
        print(f"   만듦: {wt} ({br})")
    wt, br = CTL
    if (wt / ".git").exists():
        print(f"   있음: {wt}")
    else:
        sh("git", "-C", str(MAIN), "worktree", "add", "-q", "--no-checkout", "-B", br, str(wt), REF, check=True)
        sh("git", "-C", str(wt), "sparse-checkout", "set", "--no-cone", "/litdb/_curation/", check=True)
        sh("git", "-C", str(wt), "checkout", "-q", br, check=True)
        print(f"   만듦: {wt} ({br} · sparse litdb/_curation)")

    print("== 3. scratchpad 도구")
    ev = CTL[0] / "litdb" / "_curation" / "evac"
    (scr / "tools").mkdir(parents=True, exist_ok=True)
    for d in ("briefs", "litcards", "intake"):
        (scr / d).mkdir(exist_ok=True)
    n = 0
    for f in (ev / "tools").iterdir():
        t = scr / "tools" / f.name
        if not t.exists():
            shutil.copy2(f, t)
            n += 1
    if not (scr / "STATE.md").exists():
        shutil.copy2(ev / "STATE.md", scr / "STATE.md")
    print(f"   도구 {n} 개 복사 → {scr / 'tools'}")
    if not (scr / "tools" / "trailer.txt").is_file():
        print("   ⚠ tools/trailer.txt 가 없다 — 이 세션의 커밋 끝 두 줄 (공동 저자 줄 · 세션 줄) 을 적는다")

    print("== 4. 받은 파일")
    if uploads and Path(uploads).is_dir() and any(Path(uploads).iterdir()):
        ip = scr / "tools" / "intake.py"
        t = ip.read_text(encoding="utf-8")
        t2 = re.sub(r'^UP = Path\(".*?"\)', f'UP = Path("{uploads}")', t, count=1, flags=re.M)
        if t2 != t:
            ip.write_text(t2, encoding="utf-8")
        seen = scr / "tools" / "seen.json"
        if seen.exists():
            seen.unlink()
        r = sh(sys.executable, "-I", str(ip))
        (scr / "intake" / "_restore_intake.log").write_text(r.stdout + r.stderr, encoding="utf-8")
        print(f"   intake 다시 돌림 (rc {r.returncode} · 기록 = intake/_restore_intake.log)")
    else:
        print(f"   ⛔ 업로드 폴더가 없거나 비었다: {uploads} — 1저자가 PDF 를 다시 올려야 한다 (어느 것이 필요한지는 아래 대조 + status.tsv 의 '차례 기다림')")
    res = verify(scr)

    print("== 5. 참고 저장소 (읽기 전용)")
    for repo, tag in REPOS:
        d = Path("/home/user") / repo
        if (d / ".git").exists():
            print(f"   있음: {d}")
            continue
        d.parent.mkdir(parents=True, exist_ok=True)
        cmd = ["git", "clone", "-q", "--depth", "1"] + (["--branch", tag] if tag else []) + [f"https://github.com/{repo}", str(d)]
        import os
        r = sh(*cmd, env={**os.environ, "GIT_LFS_SKIP_SMUDGE": "1"})
        print(f"   {'받음' if not r.returncode else '⚠ 실패'}: {d} {r.stderr.strip()[-120:] if r.returncode else ''}")

    print("== 6. 그림 도구 selftest")
    r = subprocess.run([sys.executable, "tools/litdb/extract_figures.py", "--selftest"],
                       capture_output=True, text=True, cwd=str(TREES[0][0]))
    print("   " + (r.stdout.strip().split("\n")[-1][:160] if r.stdout.strip() else r.stderr.strip()[-160:]))

    print("\n== 다음에 할 일")
    print("  - status.tsv 에서 세션 칸이 '대피' 이고 '도는 중' 인 줄 = 재시작으로 끊긴 편 → 원격에 그 카드 커밋이 없으면 처음부터 다시 띄운다 (launch.py)")
    print("  - '차례 기다림' 을 번호순으로 · 한 번에 둘 · 보강 넷은 맨 끝 (STATE.md)")
    if res and any(m or b for m, b in res.values()):
        print("  - ⛔ 없는 파일이 있는 키는 띄우지 못한다 — 1저자에게 그 번호의 파일을 다시 올려 달라고 한다")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--uploads", default="")
    ap.add_argument("--write-manifest", action="store_true")
    ap.add_argument("--verify", action="store_true")
    a = ap.parse_args()
    scr = Path(a.scratch)
    if a.write_manifest:
        write_manifest(scr)
    elif a.verify:
        verify(scr)
    else:
        restore(scr, a.uploads)


if __name__ == "__main__":
    main()
