#!/usr/bin/env python3
"""watch_phaseA_rescan.py — 최상단 층 자유(freeze_frac 0.85) Phase-A 재스캔 전용 화면.

    watch -n 120 python3 tools/sdcp/watch_phaseA_rescan.py

왜 따로 만드나
  이 재스캔은 "표면 Li 가 술폰산 쪽으로 올라오나"를 보려고 도는 것이다. 그러니 진행률보다
  **표면이 실제로 움직였나**가 먼저 나와야 한다. 그게 안 움직이면 재스캔을 돌릴 이유가 없다.

⚠ conda run 은 출력을 **프로세스가 끝날 때까지 버퍼링**한다. 그래서 로그가 비어 있어도
  죽은 게 아니다 — 이 watch 는 로그가 아니라 **산출 파일 개수**로 진행을 잰다
  (스캔이 자세마다 complex_<label>.xyz 를 바로 쓴다).

  0) 살아 있나 + 로그 버퍼링 진단
  1) 진행률 — complex_*.xyz / 예상 총수, 속도, ETA
  2) ★ **표면이 움직였나** — 이 재스캔의 존재 이유
  3) ★ 술폰산 O ↔ 표면 Li 거리 — 1.90–2.20 Å 로 들어와야 성공
  4) 지금까지의 E_bind (로그가 풀렸을 때만)
"""
import glob
import os
import re
import subprocess
import sys
from datetime import datetime

import numpy as np
from ase.io import read

OUT = os.environ.get("OUT", "/data/work/runs/sdcp_v2/phaseA_top1free")
LOG = os.path.expanduser(os.environ.get("LOG", "~/logs/phaseA_top1free.log"))
SLAB = os.environ.get("SLAB", os.path.expanduser(
    "~/Yonghoon-DEM-DFT/db/structures/linio2_104_sym_1x4L4_relaxed.vasp"))
NSLAB = int(os.environ.get("NSLAB", "192"))
NTOT = int(os.environ.get("NTOT", "216"))      # 2 종 × 3 배향 × 4 회전 × 9 격자
SAMPLE = int(os.environ.get("SAMPLE", "8"))    # 최근 몇 개만 기하 분석 (전수는 느리다)
LI_LO, LI_HI = 1.90, 2.20                      # Li⁺–O 배위 기준
BAR = "─" * 74


def sh(c):
    try:
        return subprocess.run(c, shell=True, capture_output=True, text=True,
                              timeout=10).stdout
    except Exception:
        return ""


def alive(pat):
    out = subprocess.run(["pgrep", "-f", pat], capture_output=True, text=True).stdout.split()
    anc, pid = set(), os.getpid()
    for _ in range(8):
        if pid <= 1:
            break
        anc.add(pid)
        try:
            with open(f"/proc/{pid}/status") as f:
                pid = next(int(l.split()[1]) for l in f if l.startswith("PPid:"))
        except Exception:
            break
    return [q for q in out if int(q) not in anc]


print("=" * 74)
gpu = sh("nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader,nounits").strip()
tmux = [t.split(":")[0] for t in sh("tmux ls").splitlines() if t.strip()]
proc = alive("phaseA_v7c_orient_scan")
print(f"Phase-A 재스캔 (freeze_frac 0.85, 최상단 층 자유) · {datetime.now():%m-%d %H:%M} · "
      f"GPU {gpu or '?'} · scan {'ALIVE' if proc else '-'} · tmux {' '.join(tmux) or '없음'}")
print(f"경로 {OUT}")
print(BAR)

xyz = sorted(glob.glob(os.path.join(OUT, "complex_*.xyz")), key=os.path.getmtime)
n = len(xyz)

# ── 0) 착수/생존 진단 ────────────────────────────────────────────────────────
if not n:
    print("· 아직 산출물 없음.")
    if proc:
        print("  ▶ 프로세스는 살아 있다 — 첫 자세(슬랩 참조 이완 포함)를 도는 중이다.")
        print("    ⚠ freeze_frac<1.0 이면 **슬랩 참조 이완이 먼저** 돌아간다. 그게 끝나야")
        print("      첫 complex_*.xyz 가 나온다 — 조금 기다릴 것.")
    else:
        print("  ⛔ 프로세스도 없다 — 시작을 못 했거나 죽었다.")
        print(f"     로그 꼬리 ({LOG}):")
        if os.path.isfile(LOG) and os.path.getsize(LOG):
            for ln in sh(f"tail -25 {LOG}").splitlines():
                print("       " + ln)
        else:
            print("       (비어 있다) ⚠ conda run 은 출력을 끝까지 버퍼링한다 —")
            print("       로그가 비었다고 죽은 게 아니다. 하지만 프로세스도 없으면 죽은 것이다.")
            print("       → 다음부터는 conda run 대신 env 파이썬을 직접 쓸 것:")
            print("         /data/apps/miniforge3/envs/uma/bin/python3 tools/sdcp/...")
    print(BAR)
    sys.exit(0)

# ── 1) 진행률 ────────────────────────────────────────────────────────────────
t0, t1 = os.path.getmtime(xyz[0]), os.path.getmtime(xyz[-1])
now = datetime.now().timestamp()
age = (now - t1) / 60.0
rate = (n - 1) / ((t1 - t0) / 60.0) if n > 1 and t1 > t0 else 0.0
eta = (NTOT - n) / rate if rate > 0 else 0.0
bar = "█" * int(28 * n / NTOT) + "·" * (28 - int(28 * n / NTOT))
print(f"① 진행 {n}/{NTOT}  [{bar}] {100*n/NTOT:.0f}%   "
      f"{rate:.2f} 자세/분 · 마지막 {age:.0f}분 전" + (f" · ETA {eta/60:.1f}h" if rate else ""))
if age > 25 and proc:
    print("   ⚠ 25분 넘게 새 자세가 안 나온다 — 한 자세가 --steps 300 을 다 태우는 중일 수 있다")
elif age > 25 and not proc:
    print("   ⛔ 프로세스가 없고 산출도 멈췄다 — 중단된 것이다")
print(f"   최근: {os.path.basename(xyz[-1])[len('complex_'):-4]}")

# ── 2) ★ 표면이 움직였나 — 이 재스캔의 존재 이유 ─────────────────────────────
ref = read(SLAB)
rpos, rsym = ref.positions, ref.get_chemical_symbols()
rz = rpos[:, 2]
ztop = rz[:NSLAB].max()
top_i = [i for i in range(NSLAB) if rz[i] > ztop - 1.0]      # 최상단 층
print(BAR)
print(f"② ★ 표면이 움직였나  (최상단 층 {len(top_i)}원자 · 최근 {min(SAMPLE, n)}개 자세)")
rows = []
for fp in xyz[-SAMPLE:]:
    try:
        at = read(fp)
    except Exception:
        continue
    if len(at) <= NSLAB:
        continue
    d = np.linalg.norm(at.positions[:NSLAB] - rpos[:NSLAB], axis=1)
    dz_li = max((at.positions[i, 2] - rpos[i, 2] for i in top_i if rsym[i] == "Li"),
                default=0.0)
    dz_ni = max((at.positions[i, 2] - rpos[i, 2] for i in top_i if rsym[i] == "Ni"),
                default=0.0)
    rows.append((os.path.basename(fp)[len("complex_"):-4], float(d.max()),
                 float(dz_li), float(dz_ni), at))
if not rows:
    print("   (읽을 자세가 없다)")
else:
    print(f"   {'자세':38s} {'max|Δr|':>8s} {'Li Δz↑':>8s} {'Ni Δz↑':>8s}")
    for lab, dmax, dli, dni, _ in rows:
        print(f"   {lab:38s} {dmax:7.3f} Å {dli:+7.3f} Å {dni:+7.3f} Å")
    mx = max(r[1] for r in rows)
    if mx < 0.02:
        print("   ⛔ **표면이 사실상 안 움직였다** — constraint 가 의도대로 안 걸렸을 수 있다")
        print("      (freeze_frac 인자가 먹었는지, 로그의 '⚠ freeze_frac ... < 1.0' 줄 확인)")
    else:
        print(f"   ✓ 표면이 움직인다 (최대 {mx:.3f} Å). Li Δz 가 양수면 술폰산 쪽으로 올라온 것이다.")
        if max(r[2] for r in rows) > 0.5:
            print("   ⚠ Li 가 0.5 Å 넘게 올라왔다 — **추출로 번질 수 있다.**")
            print("      전하분리는 UMA 가 판정 못 한다 → 그렇게 나오면 DFT 로만 결론 낼 것.")

# ── 3) ★ 술폰산 O ↔ 표면 Li — 성공 판정선 ────────────────────────────────────
print(BAR)
print(f"③ ★ 분자 O ↔ 표면 Li 최단  (성공선 {LI_LO:.2f}–{LI_HI:.2f} Å · 이전 스캔은 2.5–2.9)")
best = None
for lab, _, _, _, at in rows:
    at.set_cell(ref.cell); at.set_pbc(True)
    sym = at.get_chemical_symbols()
    mo = [i for i in range(NSLAB, len(at)) if sym[i] == "O"]
    li = [i for i in range(NSLAB) if sym[i] == "Li"]
    if not mo or not li:
        continue
    dmin = min(float(at.get_distances(m, li, mic=True).min()) for m in mo)
    mark = "★ 배위" if dmin <= LI_HI else ("· 접근" if dmin < 2.5 else "  멀다")
    print(f"   {lab:38s} {dmin:5.2f} Å  {mark}")
    best = dmin if best is None else min(best, dmin)
if best is not None:
    print(f"   → 표본 최단 {best:.2f} Å  "
          + ("**성공선 안이다 — Phase-B 가 값을 한다**" if best <= LI_HI else
             "아직 물리흡착 영역. 전수 끝나고 site_preference 로 최종 판정." ))

# ── 4) E_bind (conda run 이 버퍼를 풀어 줬을 때만) ───────────────────────────
if os.path.isfile(LOG) and os.path.getsize(LOG):
    txt = open(LOG, errors="ignore").read()
    hits = re.findall(r"^\s*(\S+)\s+E_bind = ([+-][\d.]+) eV", txt, re.M)
    if hits:
        print(BAR)
        print("④ 지금까지 최저 E_bind (UMA — 순위용, 절대값 인용 금지)")
        for lab, e in sorted(hits, key=lambda h: float(h[1]))[:5]:
            print(f"   {float(e):+.3f} eV  {lab}")
        nc = txt.count("NOT CONVERGED")
        if nc:
            print(f"   ⚠ 미수렴 {nc}개 — 순위에서 제외된다")
    elif "freeze_frac" in txt:
        print(BAR)
        print("④ 로그에 E_bind 줄이 아직 없다 (버퍼링 중이거나 슬랩 참조 이완 단계)")
print(BAR)
print("끝나면:  python3 tools/sdcp/site_preference.py --scan " + OUT + " \\")
print("           --slab " + SLAB)
