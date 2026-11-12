#!/usr/bin/env python3
"""snapshot.py — 코드 가지 쪽 진행 중 작업을 정본 가지 대피 자리 (litdb/_curation/evac/snap/) 에 묶어 둔다 (컨테이너 재시작 대비).

finish.py 의 sync_evac() 가 부른다 (논문 한 편이 끝날 때 · --sync-only 때마다).  하는 일:
  · Rint 작업 트리 (/home/user/rint-codepkg): stoic 끝 뒤의 커밋 → rint_codepkg.bundle · 커밋 전 수정 → rint_codepkg_wip.diff ·
    추적 안 된 파일 → rint_codepkg_untracked.tgz · scratchpad rint/codepkg 의 메모 · 초안
  · 본 트리 (/home/user/Yonghoon-DEM-DFT): push 안 된 커밋 → main_unpushed.bundle · 커밋 전 수정 → main_wip.diff · 추적 안 된 파일 → main_untracked.tgz
  · SNAP_INFO.txt (시각 · HEAD)
주소 · 포트 · 계정 꼴이 보이면 그 파일은 올리지 않는다 (공개 가지).
"""
import io
import re
import subprocess
import tarfile
import time
from pathlib import Path

SCR = Path(__file__).resolve().parents[1]
MAIN = Path("/home/user/Yonghoon-DEM-DFT")
RINT = Path("/home/user/rint-codepkg")
STOIC = "origin/claude/stoic-knuth-NObVQ"
PQ = "origin/claude/sdcp-dem-manuscript-si-pqwtv8"
BAD = re.compile(rb"[A-Za-z0-9._-]+@(?!anthropic\.com)[A-Za-z0-9-]+\.[A-Za-z0-9.-]+|(?:-P|-p) ?[0-9]{4,5}\b|([0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]+")


def g(cwd, *a, binary=False):
    r = subprocess.run(["git", "-C", str(cwd), *a], capture_output=True)
    return r.stdout if binary else r.stdout.decode("utf-8", "replace")


def put(dest, name, data, info):
    if not data:
        (dest / name).unlink(missing_ok=True)
        return
    if BAD.search(data if len(data) < 5_000_000 else data[:5_000_000]) and not name.endswith((".bundle", ".tgz")):
        info.append(f"⚠ {name}: 주소 · 포트 꼴이 보여 올리지 않음")
        (dest / name).unlink(missing_ok=True)
        return
    (dest / name).write_bytes(data)
    info.append(f"{name}: {len(data)} B")


def untracked_tgz(tree):
    names = [n for n in g(tree, "ls-files", "-o", "--exclude-standard").split("\n") if n.strip()]
    names = [n for n in names if (tree / n).is_file() and (tree / n).stat().st_size < 20_000_000]
    if not names:
        return b"", 0
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as t:
        for n in names:
            t.add(str(tree / n), arcname=n, recursive=False)
    return buf.getvalue(), len(names)


def tree_snap(tree, base, prefix, dest, info):
    if not (tree / ".git").exists():
        info.append(f"{prefix}: 트리 없음")
        return
    head = g(tree, "rev-parse", "HEAD").strip()
    n = g(tree, "rev-list", "--count", f"{base}..HEAD").strip()
    info.append(f"{prefix}: HEAD {head[:9]} · {base} 뒤 커밋 {n}")
    b = dest / f"{prefix}_unpushed.bundle"
    b.unlink(missing_ok=True)
    if n not in ("", "0"):
        subprocess.run(["git", "-C", str(tree), "bundle", "create", "-q", str(b), f"{base}..HEAD"], capture_output=True)
        info.append(f"{b.name}: {b.stat().st_size if b.exists() else 0} B")
    put(dest, f"{prefix}_wip.diff", g(tree, "diff", "HEAD", "--binary", binary=True), info)
    data, k = untracked_tgz(tree)
    put(dest, f"{prefix}_untracked.tgz", data, info)
    if k:
        info.append(f"{prefix}: 추적 안 된 파일 {k}")


def snap(evac_dir):
    dest = Path(evac_dir) / "snap"
    dest.mkdir(parents=True, exist_ok=True)
    info = [time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())]
    tree_snap(RINT, STOIC, "rint_codepkg", dest, info)
    tree_snap(MAIN, PQ, "main", dest, info)
    nd = dest / "rint_codepkg_notes"
    src = SCR / "rint" / "codepkg"
    if src.is_dir():
        nd.mkdir(exist_ok=True)
        for f in src.iterdir():
            if f.is_file() and f.suffix in (".md", ".txt") and f.stat().st_size < 2_000_000:
                put(nd, f.name, f.read_bytes(), info)
    for extra in ("formation_20261112.md",):
        if (SCR / extra).is_file():
            put(dest, extra, (SCR / extra).read_bytes(), info)
    (dest / "SNAP_INFO.txt").write_text("\n".join(info) + "\n", encoding="utf-8")
    return info


if __name__ == "__main__":
    import sys
    print("\n".join(snap(sys.argv[1])))
