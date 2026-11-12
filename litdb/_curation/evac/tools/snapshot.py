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


SKIP_PARTS = {".git", "__pycache__", "node_modules"}
TOTAL_LIMIT = 30_000_000      # 묶음 하나의 압축 전 합 — 넘는 파일은 뺀다 (11-12 사고: 조수의 리포 사본 1.6 GB 를 묶어 136 MB → 가지 push 막힘)
PACK_LIMIT = 45_000_000       # 압축 뒤 이보다 크면 쓰지 않는다 (옛 판 그대로 · GitHub 한 파일 100 MB 막힘 · 50 MB 경고)


def _git_tree_entries(d, rel):
    """조수가 scratchpad 안에 만든 git 작업 사본 — 파일 전체 대신 바탕 커밋 뒤 바뀐 것만 (커밋 패치 · 커밋 안 된 차이 · 새 파일).
    읽기만 (GIT_OPTIONAL_LOCKS=0 · 색인을 쓰지 않는다 — 조수가 같은 사본에서 git 을 돌려도 잠금이 겹치지 않게)."""
    import os
    env = dict(os.environ, GIT_OPTIONAL_LOCKS="0")

    def run(*a):
        r = subprocess.run(["git", "-C", str(d), *a], capture_output=True, env=env, timeout=300)
        return r.stdout if r.returncode == 0 else b""

    out = []
    root = run("rev-list", "--max-parents=0", "HEAD").split()
    parts = [b"# git work copy " + rel.encode() + b" HEAD " + run("rev-parse", "HEAD").strip()]
    if root:
        parts.append(b"# commits after base " + root[-1] + b"\n" + run("format-patch", "--stdout", "--binary", root[-1].decode() + "..HEAD"))
    parts.append(b"# uncommitted diff vs HEAD\n" + run("diff", "--binary", "HEAD"))
    out.append((f"{rel}.gitstate.patch", b"\n".join(parts) + b"\n"))
    for name in run("ls-files", "--others", "--exclude-standard", "-z").split(b"\0"):
        if name:
            nm = name.decode("utf-8", "replace")
            f = d / nm
            if f.is_file() and not f.is_symlink():
                out.append((f"{rel}.untracked/{nm}", f))
    return out


def folder_tgz(rels, limit=8_000_000, total_limit=TOTAL_LIMIT):
    """scratchpad 의 폴더 · 파일 몇 개를 한 tgz 로 (이름순 · 시각 0 → 내용이 같으면 바이트가 같다). 주소 · 포트 꼴이 보이는 파일과 큰 파일은 뺀다.
    .git · __pycache__ 는 건너뛰고, 안에 .git 이 있는 폴더 (조수의 리포 사본) 는 바뀐 것만 담는다 · 합이 total_limit 를 넘는 파일은 뺀다."""
    import gzip, io, os, tarfile
    entries, skipped = [], []
    for rel in rels:
        p = SCR / rel
        if p.is_file() and not p.is_symlink():
            entries.append((str(p.relative_to(SCR)), p))
        elif p.is_dir():
            for dirpath, dirnames, filenames in os.walk(p):
                dp = Path(dirpath)
                if (dp / ".git").exists():
                    r = str(dp.relative_to(SCR))
                    try:
                        entries += _git_tree_entries(dp, r)
                    except Exception as e:  # noqa: BLE001 — 사본 하나가 깨져도 나머지는 묶는다
                        skipped.append(f"{r} (git 사본 · {type(e).__name__})")
                    dirnames[:] = []
                    continue
                dirnames[:] = sorted(x for x in dirnames if x not in SKIP_PARTS)
                for fn in filenames:
                    f = dp / fn
                    if f.is_file() and not f.is_symlink():
                        entries.append((str(f.relative_to(SCR)), f))
    buf = io.BytesIO()
    n = 0
    total = 0
    with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode="w", format=tarfile.PAX_FORMAT) as tf:
            for arc, src in sorted(entries, key=lambda x: x[0]):
                try:
                    b = src if isinstance(src, bytes) else src.read_bytes()
                except OSError:
                    skipped.append(arc + " (읽는 중 사라짐)")
                    continue
                if len(b) > limit or BAD.search(b) or total + len(b) > total_limit:
                    skipped.append(arc)
                    continue
                total += len(b)
                ti = tarfile.TarInfo(arc)
                ti.size = len(b); ti.mtime = 0; ti.mode = 0o644; ti.uid = ti.gid = 0; ti.uname = ti.gname = ""
                tf.addfile(ti, io.BytesIO(b))
                n += 1
    return buf.getvalue(), n, skipped


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
    # scratchpad 에만 있는 조수 산출 (정독 종합 묶음 · 메모 3.2 초안) — 내용이 같으면 바이트도 같게 묶는다 (가지에 새 덩어리가 안 쌓이게)
    for name, rels in (("synthfix_work.tgz", ["synthfix/package", "synthfix/APPLIED.md", "synthfix/applied_log.jsonl",
                                               "synthfix/post_build_notes.md", "synthfix/tools", "synthfix/out_before"]),
                       ("dem_redesign_work.tgz", ["dem_redesign"]),
                       ("mixer_e0_work.tgz", ["mixer_e0_v2"]),
                       ("p1g2c_work.tgz", ["p1g2c", "g2c_dry/compare_run40000.log", "g2c_dry/compare_dry200.log"]),
                       ("litdb_wish_work.tgz", ["litdb_wish", "tools/wishlist_table.py", "wishlist_table.tsv"])):
        data, n, skipped = folder_tgz(rels)
        if n and len(data) > PACK_LIMIT:
            info.append(f"⛔ {name}: 압축 {len(data)} B > {PACK_LIMIT} B — 쓰지 않음 (옛 판 그대로 · 무엇이 큰지 볼 것)")
            continue
        if n:
            (dest / name).write_bytes(data)
            info.append(f"{name}: 파일 {n} · {len(data)} B" + (f" · 뺀 파일 {len(skipped)} (주소 꼴 · 큰 파일): {skipped[:5]}" if skipped else ""))
    (dest / "SNAP_INFO.txt").write_text("\n".join(info) + "\n", encoding="utf-8")
    return info


if __name__ == "__main__":
    import sys
    print("\n".join(snap(sys.argv[1])))
