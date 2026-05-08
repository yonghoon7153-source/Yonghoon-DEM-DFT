#!/usr/bin/env python3
"""Watch UMA (v29 AIMD) and MACE (v30 Z-scan) progress side by side.

Auto-detects PIDs via pgrep -f. Tails respective logs to extract:
  - v29 AIMD: current comp, current step, RMS, ETA
  - v30 MACE Z-scan: current comp, current gap, partial W_max

Run on KISTI in any conda env (no calc imports needed):
  cd /scratch/x3430a02/kgy/manuscript_support/adhesion_v5_v2
  python /tmp/watch_uma_mace.py

Continuous refresh:
  while true; do clear; python /tmp/watch_uma_mace.py; sleep 30; done
"""
import os, sys, re, subprocess, datetime, time
from pathlib import Path

G='\033[92m'; Y='\033[93m'; R='\033[91m'; B='\033[94m'; C='\033[96m'
W='\033[0m'; BD='\033[1m'; D='\033[90m'

ALL_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5', 'modelC']
N_COMPS = len(ALL_COMPS)
N_STEPS_AIMD = 500    # v29 Langevin
N_GAPS = 23           # v30 Z-scan

LOG_V29 = Path("phase2a_v29_results/run.log")
LOG_V30 = Path("phase2a_v30_results/run.log")


def find_pid(pattern):
    try:
        out = subprocess.check_output(['pgrep', '-f', pattern],
                                       stderr=subprocess.DEVNULL).decode().strip()
        return out.split('\n')[0] if out else None
    except subprocess.CalledProcessError:
        return None


def proc_info(pid):
    if not pid:
        return None
    try:
        out = subprocess.check_output(
            ['ps', '-p', str(pid), '-o', 'pid,etime,pcpu,pmem,rss,stat'],
            stderr=subprocess.DEVNULL).decode().strip().split('\n')
        if len(out) < 2:
            return None
        return out[1]  # data line
    except subprocess.CalledProcessError:
        return None


def gpu_info():
    try:
        out = subprocess.check_output(
            ['nvidia-smi',
             '--query-gpu=index,memory.used,memory.total,utilization.gpu,temperature.gpu,power.draw',
             '--format=csv,noheader,nounits'],
            stderr=subprocess.DEVNULL, timeout=3).decode()
        return out.strip().split('\n')
    except Exception:
        return []


def progress_bar(done, total, width=12):
    if total == 0:
        return '[' + '·' * width + ']'
    n = int(round(width * done / total))
    return '[' + '█' * n + '·' * (width - n) + ']'


def parse_v29(log):
    """Returns dict per comp + current state."""
    if not log.exists():
        return None
    text = log.read_text()
    state = {
        'comps_seen': [],
        'current_comp': None,
        'current_phase': None,  # 'pre-relax' or 'langevin' or None
        'final_rms': {},        # comp -> rms (after pre-relax)
        'final_max': {},
        'verdicts': {},
        'aimd_running_steps': 0,
        'aimd_total_steps': 0,
    }
    # comp markers
    comp_re = re.compile(r'========= (comp\d|modelC) \(')
    pre_done_re = re.compile(r'M2 pre-relax done')
    langevin_start_re = re.compile(r'Running Langevin: (\d+) steps')
    rms_re = re.compile(r'Final t=[\d.]+ fs: RMS=([\d.]+) A, max=([\d.]+) A')
    verdict_re = re.compile(r'VERDICT: (.+)')

    last_comp = None
    for line in text.split('\n'):
        m = comp_re.search(line)
        if m:
            last_comp = m.group(1)
            if last_comp not in state['comps_seen']:
                state['comps_seen'].append(last_comp)
            state['current_comp'] = last_comp
            state['current_phase'] = 'starting'
        elif pre_done_re.search(line):
            state['current_phase'] = 'pre-relaxed'
        elif langevin_start_re.search(line):
            state['current_phase'] = 'langevin'
            n_total = int(langevin_start_re.search(line).group(1))
            state['aimd_total_steps'] = n_total
        elif rms_re.search(line):
            m = rms_re.search(line)
            state['final_rms'][last_comp] = float(m.group(1))
            state['final_max'][last_comp] = float(m.group(2))
            state['current_phase'] = 'done'
        elif verdict_re.search(line):
            state['verdicts'][last_comp] = verdict_re.search(line).group(1)

    # If currently in langevin, we don't know exact step from log (no per-step output)
    return state


def parse_v30(log):
    """Returns dict per comp + current state."""
    if not log.exists():
        return None
    text = log.read_text()
    state = {
        'comps_seen': [],
        'current_comp': None,
        'gaps_done': {},      # comp -> count of gap points logged
        'partial_curve': {},  # comp -> list of (gap, Wad)
        'W_max': {},
        'd_min': {},
        'comps_done': set(),
    }
    comp_re = re.compile(r'========= (comp\d|modelC) =========')
    iso_re = re.compile(r'E_se_iso = ([\d.+-]+) eV, E_ncm_iso = ([\d.+-]+) eV')
    gap_re = re.compile(r'gap=([\d.]+)\s+E_int=([\d.+-]+)\s+Wad=([\d.+-]+)')
    summary_re = re.compile(r'W_max = ([\d.+-]+) J/m\S+ at d_min = ([\d.]+)')
    last_comp = None
    for line in text.split('\n'):
        m = comp_re.search(line)
        if m:
            last_comp = m.group(1)
            if last_comp not in state['comps_seen']:
                state['comps_seen'].append(last_comp)
            state['current_comp'] = last_comp
        elif gap_re.search(line) and last_comp:
            mg = gap_re.search(line)
            gap, e, w = float(mg.group(1)), float(mg.group(2)), float(mg.group(3))
            state['partial_curve'].setdefault(last_comp, []).append((gap, w))
            state['gaps_done'][last_comp] = state['gaps_done'].get(last_comp, 0) + 1
        elif summary_re.search(line) and last_comp:
            ms = summary_re.search(line)
            state['W_max'][last_comp] = float(ms.group(1))
            state['d_min'][last_comp] = float(ms.group(2))
            state['comps_done'].add(last_comp)
    return state


# ── Header ──
print(f"{BD}{'═'*70}{W}")
print(f"{BD}═══ UMA (v29 AIMD) + MACE (v30 Z-scan) Watch  "
      f"({datetime.datetime.now():%H:%M:%S}){W}")
print(f"{BD}{'═'*70}{W}")

# ── GPU ──
for line in gpu_info():
    parts = [x.strip() for x in line.split(',')]
    if len(parts) < 6:
        continue
    idx, mu, mt, ut, temp, pw = parts[:6]
    col = G if int(ut) > 30 else (Y if int(ut) > 0 else D)
    print(f"  GPU{idx}: {col}{ut:>3}% util{W}  mem {mu}/{mt} MiB  T={temp}°C  P={float(pw):.1f}W")

# ─────────────────────── v29 (UMA AIMD) ───────────────────────
print(f"\n{BD}{C}── v29 UMA AIMD (M2 stability check) ──{W}")
pid_v29 = find_pid("phase2a_v29_aimd_stability")
if pid_v29:
    info = proc_info(pid_v29)
    print(f"  PID {pid_v29}: {G}RUNNING{W}  {info or ''}")
else:
    print(f"  {Y}no v29 process detected{W}")

s29 = parse_v29(LOG_V29)
if s29:
    n_done = len(s29['final_rms'])
    cur = s29['current_comp']
    phase = s29['current_phase']
    print(f"  Done {n_done}/{N_COMPS} comps  "
          f"{progress_bar(n_done, N_COMPS, 14)}")
    print(f"  Current: {cur or '?'} ({phase or 'unknown'})")
    if cur and phase == 'langevin':
        print(f"    {Y}Running 1 ps Langevin (no per-step output, ~10-15 min/comp){W}")

    if s29['final_rms']:
        print(f"\n  {C}Per-comp RMS displacement after AIMD:{W}")
        print(f"    {'comp':<8} {'RMS (Å)':>9} {'Max (Å)':>9}  verdict")
        for c in ALL_COMPS:
            if c in s29['final_rms']:
                rms = s29['final_rms'][c]
                mx = s29['final_max'][c]
                v = s29['verdicts'].get(c, '?')
                col = G if 'PASS' in v else (R if 'FAIL' in v else Y)
                print(f"    {c:<8} {rms:>9.3f} {mx:>9.3f}  {col}{v[:40]}{W}")
else:
    print(f"  {Y}no log yet ({LOG_V29}){W}")

# ─────────────────────── v30 (MACE Z-scan) ───────────────────────
print(f"\n{BD}{C}── v30 MACE Z-scan binding curve ──{W}")
pid_v30 = find_pid("phase2a_v30_mace_zscan")
if pid_v30:
    info = proc_info(pid_v30)
    print(f"  PID {pid_v30}: {G}RUNNING{W}  {info or ''}")
else:
    print(f"  {Y}no v30 process detected{W}")

s30 = parse_v30(LOG_V30)
if s30:
    n_done = len(s30['comps_done'])
    cur = s30['current_comp']
    print(f"  Done {n_done}/{N_COMPS} comps  "
          f"{progress_bar(n_done, N_COMPS, 14)}")
    print(f"  Current: {cur or '?'}")
    if cur and cur not in s30['comps_done']:
        gaps_done = s30['gaps_done'].get(cur, 0)
        print(f"    {cur} gap progress: {gaps_done}/{N_GAPS}  "
              f"{progress_bar(gaps_done, N_GAPS, 14)}")
        if cur in s30['partial_curve']:
            recent = s30['partial_curve'][cur][-3:]
            print(f"    Recent (gap, Wad J/m²):")
            for g, w in recent:
                print(f"      gap={g:.2f}  Wad={w:+.4f}")

    if s30['W_max']:
        print(f"\n  {C}Completed comps:{W}")
        print(f"    {'comp':<8} {'W_max(J/m²)':>12} {'d_min(Å)':>10}")
        for c in ALL_COMPS:
            if c in s30['W_max']:
                print(f"    {c:<8} {s30['W_max'][c]:>+12.4f} {s30['d_min'][c]:>10.2f}")
else:
    print(f"  {Y}no log yet ({LOG_V30}){W}")

# ─────────────────────── tails (last 5 lines) ───────────────────────
def tail_n(path, n=5):
    if not path.exists():
        return ['(no log)']
    try:
        out = subprocess.check_output(['tail', f'-{n}', str(path)],
                                       stderr=subprocess.DEVNULL).decode()
        return out.rstrip().split('\n')
    except Exception:
        return ['(read error)']

print(f"\n{D}── v29 log (last 5 lines) ──{W}")
for line in tail_n(LOG_V29, 5):
    print(f"  {line}")

print(f"\n{D}── v30 log (last 5 lines) ──{W}")
for line in tail_n(LOG_V30, 5):
    print(f"  {line}")

print(f"{BD}{'═'*70}{W}")
