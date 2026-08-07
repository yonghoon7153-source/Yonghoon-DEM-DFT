#!/usr/bin/env python3
"""watch_gabia.py — gabia 전체 상황판 (SEI DFT + SDCP + 재부팅 복구).

    watch -n 120 python3 tools/sei/watch_gabia.py

왜 이 화면인가
  2026-08-06 서버가 재부팅되면서 tmux 세션과 돌던 계산이 전부 죽었다. 그럴 때 제일
  먼저 알아야 할 건 "무엇이 살아남았고 무엇을 다시 걸어야 하나" 다. 그래서 진행률보다
  **단계별 완료 매트릭스**를 먼저 띄운다 — 러너가 resume-safe 라 끝난 단계는 안 다시 돈다.

  ⚠ 갭은 03 단계(fixed-occ nscf)의 고유값이 정본이다. DOS 문턱 판독 금지.
"""
import glob
import json
import os
import subprocess
import sys
from datetime import datetime

SEI = os.environ.get("SEI", "/data/work/runs/sei_dft")
SDCP_VASP = "/data/work/runs/sdcp_v2/phaseB_vasp"
STAGES = [("01_vcrelax", "vc-rlx"), ("02_scf", "scf"), ("03_nscf_gap", "gap"),
          ("04_nscf_dos", "dos-k"), ("05_dos", "dos"), ("06_projwfc", "pdos")]
BAR = "─" * 76


def sh(c):
    try:
        return subprocess.run(c, shell=True, capture_output=True, text=True,
                              timeout=10).stdout
    except Exception:
        return ""


def done(d, stem):
    """단계 완료 판정. pw.x/dos.x/projwfc.x 다 'JOB DONE' 을 찍는다."""
    o = os.path.join(d, stem + ".out")
    if not os.path.isfile(o):
        return " "
    try:
        tx = open(o, errors="ignore").read()
    except OSError:
        return "?"
    if "JOB DONE" in tx:
        return "✓"
    if "Error in routine" in tx or "%%%%" in tx or "MPI_ABORT" in tx:
        return "✗"
    return "▸"          # 시작은 했는데 안 끝났다 (재부팅으로 끊긴 것)


print("=" * 76)
gpu = sh("nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total "
         "--format=csv,noheader,nounits").strip()
tmux = [t.split(":")[0] for t in sh("tmux ls").splitlines() if t.strip()]
pw = len([x for x in sh("pgrep -f 'pw.x|dos.x|projwfc.x'").split() if x])
up = sh("uptime -p").strip() or sh("uptime").strip()
print(f"gabia · {datetime.now():%m-%d %H:%M} · GPU {gpu or '?'} · "
      f"QE 프로세스 {pw} · tmux {' '.join(tmux) or '없음'}")
print(f"가동 {up}")
print(BAR)

# ── 1) SEI DFT 단계 매트릭스 ────────────────────────────────────────────────
tags = sorted(os.path.basename(x) for x in glob.glob(os.path.join(SEI, "*"))
              if os.path.isdir(x))
if not tags:
    print(f"⛔ {SEI} 에 작업 폴더가 없다 — build_dft_inputs.py 부터.")
else:
    print(f"① SEI DFT — {len(tags)}종 × 6단계   (✓ 완료 · ▸ 중단 · ✗ 오류 · 공백 미착수)")
    print("   " + " " * 26 + "  ".join(f"{s:>6s}" for _, s in STAGES))
    ndone = 0
    for t in tags:
        d = os.path.join(SEI, t)
        marks = [done(d, stem) for stem, _ in STAGES]
        gj = os.path.join(d, "gap.json")
        g = ""
        if os.path.isfile(gj):
            try:
                j = json.load(open(gj))
                g = f"  gap {j['gap']:6.3f} eV  {j['verdict']}"
            except Exception:
                g = "  (gap.json 손상)"
        if all(m == "✓" for m in marks) and os.path.isfile(gj):
            ndone += 1
        print(f"   {t:26s}" + "  ".join(f"{m:>6s}" for m in marks) + g)
    print(f"\n   완주 {ndone}/{len(tags)}")

    # 끊긴 것 = 재부팅 피해. 러너가 resume-safe 라 그냥 다시 걸면 된다.
    broken = [t for t in tags
              if any(done(os.path.join(SEI, t), s) == "▸" for s, _ in STAGES)]
    if broken and pw == 0:
        print(f"\n   ⚠ 중단된 조성 {len(broken)}개: {', '.join(broken)}")
        print("     러너는 resume-safe 다 — 끝난 단계는 건너뛰므로 그냥 다시 걸면 된다:")
        print("       tmux new -s seidft -d \"bash tools/sei/run_sei_dft.sh 2>&1 "
              "| tee -a ~/logs/sei_dft.log\"")

print(BAR)

# ── 2) 갭 결산 ─────────────────────────────────────────────────────────────
gaps = []
for j in sorted(glob.glob(os.path.join(SEI, "*", "gap.json"))):
    try:
        gaps.append(json.load(open(j)))
    except Exception:
        pass
if gaps:
    print(f"② 갭 (fixed-occ nscf 고유값 — DOS 문턱 아님)")
    print(f"   {'상':26s} {'VBM':>8s} {'CBM':>8s} {'gap(eV)':>9s}  판정")
    for d in sorted(gaps, key=lambda x: -x["gap"]):
        nd = "Nd" in d["tag"] or "nd2" in d["tag"]
        flag = "  ⚠ 4f valence — 진단용" if nd else ""
        print(f"   {d['tag']:26s} {d['vbm']:8.3f} {d['cbm']:8.3f} "
              f"{d['gap']:9.3f}  {d['verdict']}{flag}")
    print("   ⚠ PBE 갭은 넓은 갭 절연체에서 30–50% 과소 — 실험값과 나란히 놓지 말 것")
else:
    print("② 갭 — 아직 gap.json 이 없다")

print(BAR)

# ── 3) SDCP 외주 패키지 ────────────────────────────────────────────────────
z = SDCP_VASP + ".zip"
if os.path.isfile(z):
    n = len([x for x in glob.glob(os.path.join(SDCP_VASP, "*", "POSCAR"))])
    print(f"③ SDCP VASP 외주 패키지 — ✅ 준비됨 ({n} job · "
          f"{os.path.getsize(z)//1024} KB)")
    print(f"   {z}")
    print("   로컬로:  scp root@121.78.116.27:" + z + " ~/Downloads/")
else:
    print("③ SDCP VASP 외주 패키지 — 없음 (qe_to_vasp.py --zip 으로 생성)")

# ── 4) 디스크 ──────────────────────────────────────────────────────────────
df = sh("df -h /data | tail -1").split()
if len(df) >= 5:
    print(f"\n디스크 /data  {df[2]} 사용 / {df[1]}  (여유 {df[3]}, {df[4]})")
print(BAR)
