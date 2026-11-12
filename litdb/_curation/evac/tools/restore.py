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
        if f.is_file() and not t.exists():
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


def restore_code(scr):
    """코드 가지 (pqwtv8) 쪽 일을 이어가기 위한 복구 — 11-12 인계 뒤에 더함.  본 트리 파일은 고치지 않는다 (안내만 찍는다)."""
    import os
    ev = CTL[0] / "litdb" / "_curation" / "evac"
    print("== 7. 리포 전체 이력 · 관련 가지 (문서 검사 · 게이트가 요구)")
    if sh("git", "-C", str(MAIN), "rev-parse", "--is-shallow-repository").stdout.strip() == "true":
        r = sh("git", "-C", str(MAIN), "fetch", "-q", "--unshallow", "origin", "claude/sdcp-dem-manuscript-si-pqwtv8")
        print("   unshallow rc", r.returncode)
    specs = ["+refs/heads/claude/stoic-knuth-NObVQ:refs/remotes/origin/claude/stoic-knuth-NObVQ",
             "+refs/heads/codex/*:refs/remotes/origin/codex/*", "+refs/heads/Codex/*:refs/remotes/origin/Codex/*",
             "+refs/heads/claude/evac-*:refs/remotes/origin/claude/evac-*", "+refs/heads/claude/wip-*:refs/remotes/origin/claude/wip-*",
             "+refs/heads/main:refs/remotes/origin/main", "+refs/heads/manuscript-track:refs/remotes/origin/manuscript-track",
             "+refs/heads/lit-reader:refs/remotes/origin/lit-reader", "+refs/heads/rescue/*:refs/remotes/origin/rescue/*"] + [
        f"+refs/heads/claude/{b}:refs/remotes/origin/claude/{b}" for b in (
            "rint-pf2-handoff-20261022", "phase-a-96arm-kgy", "resistor-network-solver-LDjW6", "review-ml-migration-1BN1c",
            "windows-reinstall-backup-oducnh", "zip-git-gpu-setup-vdqdtd", "14-gate-code-review-9qkx05", "gate80-standby-9a26dd5f",
            "dashboard-standby-e2f56971", "solid-state-cathode-improvement-hevry0")]
    r = sh("git", "-C", str(MAIN), "fetch", "-q", "origin", *specs, env={**os.environ, "GIT_LFS_SKIP_SMUDGE": "1"})
    print("   가지 받기 rc", r.returncode, "· 원격 추적 ref", len(sh("git", "-C", str(MAIN), "for-each-ref", "refs/remotes").stdout.split("\n")) - 1,
          "→ `python3 scripts/check_doc_refs.py` 가 '깨진 참조 없음' 이어야 한다 (없는 커밋이 남으면 그 가지를 더 받는다)")
    print("== 8. 게이트용 패키지 (본 트리 webapp/requirements.txt)")
    sh(sys.executable, "-m", "pip", "install", "-q", "--ignore-installed", "blinker")      # debian blinker 1.7 을 pip 이 못 지움 → 이것만
    r = sh(sys.executable, "-m", "pip", "install", "-q", "-r", str(MAIN / "webapp" / "requirements.txt"), "pandas==2.3.3", "pytz")
    r2 = subprocess.run(["bash", "scripts/setup_kgy_py38.sh"], capture_output=True, text=True, cwd=str(MAIN))
    print("   pip rc", r.returncode, "· kgy 판 (3.8) rc", r2.returncode, (r2.stdout.strip().split("\n") or [""])[-1][:120])
    print("== 9. 인계 묶음 (본 세션 → 대피 세션 · 11-12)")
    for name, dest in (("handoff_evac_20261112_redacted.tgz", "handoff_20261112"), ("handoff_evac_litread_20261112.tgz", "handoff_litread_20261112")):
        src, out = ev / "handoff_20261112" / name, scr / dest
        if src.is_file() and not (out.exists() and any(out.iterdir())):
            r = sh(sys.executable, "-I", str(scr / "tools" / "safe_untar.py"), str(src), str(out))
            print("  ", (r.stdout.strip().split("\n") or [""])[-1][:150])
    print("   ⚠ 사본의 g2c/ibb_try4_cmds_template.txt 는 접속 계정 · 주소 · 포트를 가렸다 — 값은 1저자가 채팅으로 준다")
    print("== 10. Rint 코드 묶음 작업 트리 (스냅샷에서)")
    snap, rint = ev / "snap", Path("/home/user/rint-codepkg")
    if (rint / ".git").exists():
        print("   있음:", rint)
    else:
        sh("git", "-C", str(MAIN), "worktree", "add", "-q", "--detach", str(rint), "origin/claude/stoic-knuth-NObVQ", check=True)
        b = snap / "rint_codepkg_unpushed.bundle"
        if b.is_file():
            sh("git", "-C", str(rint), "fetch", "-q", str(b), "+HEAD:refs/tmp/rint_snap")
            r = sh("git", "-C", str(rint), "checkout", "-q", "--detach", "refs/tmp/rint_snap")
            print("   커밋 되살림 rc", r.returncode, sh("git", "-C", str(rint), "log", "--oneline", "-3").stdout.replace("\n", " | ")[:200])
        d = snap / "rint_codepkg_wip.diff"
        if d.is_file():
            print("   커밋 전 수정 얹기 rc", sh("git", "-C", str(rint), "apply", str(d)).returncode)
        u = snap / "rint_codepkg_untracked.tgz"
        if u.is_file():
            tmp = scr / "rint" / "_untracked_restore"
            if not tmp.exists():
                sh(sys.executable, "-I", str(scr / "tools" / "safe_untar.py"), str(u), str(tmp))
                for f in tmp.rglob("*"):
                    if f.is_file():
                        tgt = rint / f.relative_to(tmp)
                        tgt.parent.mkdir(parents=True, exist_ok=True)
                        if not tgt.exists():
                            shutil.copy2(f, tgt)
        nd = snap / "rint_codepkg_notes"
        if nd.is_dir():
            (scr / "rint" / "codepkg").mkdir(parents=True, exist_ok=True)
            for f in nd.iterdir():
                if not (scr / "rint" / "codepkg" / f.name).exists():
                    shutil.copy2(f, scr / "rint" / "codepkg" / f.name)
    print("== 11. 본 트리 (pqwtv8) — 손으로 볼 것")
    print("   `git -C", MAIN, "status` · `git fetch origin claude/sdcp-dem-manuscript-si-pqwtv8` 뒤 원격 끝과 견준다.")
    for f in ("main_unpushed.bundle", "main_wip.diff", "main_untracked.tgz"):
        if (snap / f).is_file():
            print(f"   스냅샷에 {f} 있음 ({(snap / f).stat().st_size} B) — push 안 된 커밋 · 커밋 전 수정이 있었다 → STATE.md '인계 받은 일' 절의 순서대로 되살린다")
    print("   SNAP_INFO:", (snap / "SNAP_INFO.txt").read_text(encoding="utf-8")[:500] if (snap / "SNAP_INFO.txt").is_file() else "없음")


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
        restore_code(scr)


if __name__ == "__main__":
    main()
