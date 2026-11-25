#!/usr/bin/env python3
"""watch_lpsocl_elf.py — LPSOCl ELF(+CDD) 단독 watch.

관례:  watch -n 30 python3 tools/electronic/watch_lpsocl_elf.py

대상: tools/electronic/run_lpsocl_elf_gabia.sh (CPU pw.x/pp.x — GPU 작업과 동시 실행 안전)
단계: pseudo 수집 → scf(prefix=lpsocl) → scf_atomic(lpsocl_at) → pp.x ELF(plot_num=8)
      → pp.x rho_scf/rho_atomic(plot_num=0)
"""
import glob
import os
import re
import subprocess
from datetime import datetime

E = os.environ.get("ELF_DIR", "/data/work/runs/lpsocl_elf")
LOG = os.path.join(E, "run.log")
BAR = "-" * 68


def sh(c):
    try:
        return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=10).stdout
    except Exception:
        return ""


def alive(p):
    return "ALIVE" if sh(f"pgrep -x {p}").strip() else "-"


print("=" * 68)
print(f"LPSOCl ELF (+CDD)   {datetime.now():%m-%d %H:%M:%S}")
print("=" * 68)
cpu = sh("nproc").strip()
la = open("/proc/loadavg").read().split()[:3] if os.path.exists("/proc/loadavg") else []
print(f"CPU {cpu} cores · load {' '.join(la)}   (CPU 빌드 — GPU 작업과 무관)")
print(f"  pw.x {alive('pw.x')} · pp.x {alive('pp.x')}")
# ⚠ 재부팅하면 tmux 가 통째로 날아가고 pgrep 도 전부 '-' 가 된다. 그 상태를 "진행 중"과
#   구분하려면 **로그 마지막 기록이 부팅보다 이른가**를 봐야 한다 — 그거면 확실히 죽음이다.
BOOT = sh("uptime -s").strip()
try:
    BOOTDT = datetime.strptime(BOOT, "%Y-%m-%d %H:%M:%S")
except ValueError:
    BOOTDT = None
print(f"  부팅 {BOOT or '?'} ({sh('uptime -p').strip()})")
if BOOTDT and os.path.isfile(LOG):
    lm = datetime.fromtimestamp(os.path.getmtime(LOG))
    if lm < BOOTDT:
        print(f"  ⛔ **재부팅으로 죽음** — run.log 마지막 기록 {lm:%m-%d %H:%M} < 부팅")
        print("     재기동: tmux new -s lpsoclelf -d 'bash tools/electronic/run_lpsocl_elf_gabia.sh \\")
        print(f"       > {LOG} 2>&1'")
print(BAR)

if not os.path.isfile(LOG):
    print(f"로그 없음: {LOG}")
    print("  tmux new -s lpsoclelf -d 'bash tools/electronic/run_lpsocl_elf_gabia.sh \\")
    print(f"    > {LOG} 2>&1'")
    raise SystemExit

t = open(LOG, errors="ignore").read()

# ── 단계 진행 ──────────────────────────────────────────────────────────
STAGES = [("[pseudo] OK", "① pseudo 수집"),
          ("pw.x scf.in", "② scf (lpsocl)"),
          ("scf_atomic", "③ scf_atomic (lpsocl_at)"),
          ("pp.x elf", "④ pp.x ELF (plot_num=8)"),
          ("pp_rho.in", "⑤ pp.x rho_scf (plot_num=0)"),
          ("pp_rho_at.in", "⑥ pp.x rho_atomic")]
print("단계")
for k, name in STAGES:
    print(f"  {'✓' if k.lower() in t.lower() else '·'} {name}")
print(BAR)

# ── SCF 수렴 ───────────────────────────────────────────────────────────
# ⚠ scf_must_converge=.false. + electron_maxstep 도달 = **가짜 수렴**.
#    실제로 SDCP 에서 'convergence has been achieved in 150 iterations' 가
#    maxstep 150 이라 가짜였던 사례가 있다. 반복수를 반드시 본다.
mx = re.search(r"electron_maxstep\s*=\s*(\d+)", t)
maxstep = int(mx.group(1)) if mx else None
conv = re.findall(r"convergence has been achieved in\s+(\d+)\s+iterations", t)
print("SCF")
if maxstep:
    print(f"  electron_maxstep = {maxstep}")
if conv:
    for n in conv[-3:]:
        flag = "  ⛔ **가짜 수렴 의심 (maxstep 과 동일)**" if maxstep and int(n) >= maxstep else "  ✓"
        print(f"  수렴: {n} iterations{flag}")
else:
    print("  (아직 수렴 없음)")
it = re.findall(r"iteration #\s*(\d+).*?ecut", t)
acc = re.findall(r"estimated scf accuracy\s+<\s+([\d.E+-]+)\s+Ry", t)
if it or acc:
    print(f"  현재: iteration #{it[-1] if it else '?'} · accuracy {acc[-1] if acc else '?'} Ry")
etot = re.findall(r"!\s+total energy\s+=\s+([-\d.]+)\s+Ry", t)
if etot:
    print(f"  total energy = {etot[-1]} Ry")
print(BAR)

# ── 산출물 ─────────────────────────────────────────────────────────────
print("산출물")
want = [("lpsocl_elf.cube", "ELF (VESTA 등가면)"),
        ("lpsocl_rho_scf.cube", "SCF 전하밀도 — **Bader 재사용 가능(단 가전자)**"),
        ("lpsocl_rho_atomic.cube", "원자 중첩 밀도 (CDD 차분용)")]
for fn, desc in want:
    p = os.path.join(E, fn)
    if os.path.exists(p):
        print(f"  ✓ {fn:26s} {os.path.getsize(p)/1e6:6.1f} MB  {desc}")
    else:
        print(f"  · {fn:26s} {'':>9s}  {desc}")
print(BAR)

# ── 에러 ───────────────────────────────────────────────────────────────
err = [l.strip() for l in t.splitlines()
       if re.search(r"Error|%%%%|ERROR|forrtl|Fatal", l)]
if err:
    print("⛔ 에러")
    for l in err[-3:]:
        print("  " + l[:100])
    print(BAR)

# ── 다음 단계 안내 ─────────────────────────────────────────────────────
print("다음")
if os.path.exists(os.path.join(E, "lpsocl_elf.cube")):
    print("  ELF 완료 → repo 로 회수 + VESTA 세션 생성")
    print("  ⚠ Bader 는 이 rho_scf(NC ONCV, plot_num=0 **가전자**)로는")
    print("     기존 bader_b2o3_vs_lpscl16.csv(**AE, plot_num=17, PAW kjpaw**)와 **비교 불가**.")
    print("     비교하려면 kjpaw pseudo 로 SCF 를 한 번 더 돌려야 한다.")
else:
    print("  진행 중 — pw.x/pp.x 생존과 accuracy 하강만 보면 된다")
print(f"  로그: tail -f {LOG}")
