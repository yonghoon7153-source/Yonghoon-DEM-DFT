#!/usr/bin/env python3
"""Watch BOTH mlip_elastic_snapshot_v2 (comp2B/comp5) AND
phase2a_v31_mlip_elastic_v2_3comp (comp1_v2/comp2_v2/modelC_v2) side by side.

Run on KISTI from /scratch/x3430a02/kgy/manuscript_support/:
  python /tmp/watch_elastic_dual.py

Continuous:
  while true; do clear; python /tmp/watch_elastic_dual.py; sleep 30; done
"""
import os, re, sys, subprocess, datetime
from pathlib import Path

G='\033[92m'; Y='\033[93m'; R='\033[91m'; B='\033[94m'; C='\033[96m'
W='\033[0m'; BD='\033[1m'; D='\033[90m'

# Both scripts use 5 snapshots × 6 strain pairs. Equilib 3000 steps + 5×1000.
N_SNAPSHOTS = 5


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
        return out[1] if len(out) > 1 else None
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


def parse_snapshot_elastic_log(text):
    """Parse log from snapshot_elastic style runs.

    Returns list of (comp_name, status_str)
    where status_str is one of:
      - 'equilibrating'
      - 'snap N/5 done, ...'
      - 'AVG done'
    """
    if not text:
        return []
    comps = {}
    cur_comp = None
    comp_re = re.compile(r'^---\s*(\S+)\s+\((\d+)\s+atoms\)\s*---', re.M)
    snap_re = re.compile(r'snap\s+(\d+):\s+C11=([\d.]+),\s+C12=([\d.]+),\s+C44=([\d.]+),\s+E=([\d.]+)')
    avg_re = re.compile(r'AVG:\s+C11=([\d.]+).*?E=([\d.]+)', re.S)
    equil_re = re.compile(r'Equilibrating at \d+K')

    for line in text.split('\n'):
        m = comp_re.match(line)
        if m:
            cur_comp = m.group(1)
            comps[cur_comp] = {'atoms': int(m.group(2)), 'snaps': [], 'avg': None}
            continue
        if cur_comp is None:
            continue
        m = snap_re.search(line)
        if m:
            comps[cur_comp]['snaps'].append({
                'i': int(m.group(1)),
                'C11': float(m.group(2)), 'C12': float(m.group(3)),
                'C44': float(m.group(4)), 'E': float(m.group(5)),
            })
            continue
        m = avg_re.search(line)
        if m:
            comps[cur_comp]['avg'] = {
                'C11': float(m.group(1)), 'E': float(m.group(2)),
            }
    return comps


def show_section(title, pid_pattern, log_paths, color=C):
    print(f"\n{BD}{color}── {title} ──{W}")
    pid = find_pid(pid_pattern)
    if pid:
        info = proc_info(pid)
        print(f"  PID {pid}: {G}RUNNING{W}  {info or ''}")
    else:
        print(f"  {Y}no process detected ({pid_pattern}){W}")

    # find which log path exists
    log = None
    for p in log_paths:
        if Path(p).exists():
            log = p
            break
    if not log:
        print(f"  {D}no log found{W}")
        return

    # parse
    text = Path(log).read_text()
    comps = parse_snapshot_elastic_log(text)
    if not comps:
        print(f"  {D}log parsing yielded no comps yet{W}")
        # show last 5 lines
        last = text.rstrip().split('\n')[-5:]
        for line in last:
            print(f"  {D}{line}{W}")
        return

    print(f"  Log: {log}")
    print(f"  {'comp':<14} {'atoms':>6} {'snaps':>10} {'C11 avg':>10} {'E avg':>10}")
    for name, d in comps.items():
        n_snap = len(d['snaps'])
        progress = f"{n_snap}/{N_SNAPSHOTS}"
        if d['avg']:
            mark = f"{G}✓{W}"
            c11_avg = f"{d['avg']['C11']:.1f}"
            e_avg = f"{d['avg']['E']:.1f}"
        elif n_snap > 0:
            mark = f"{Y}▶{W}"
            c11_avg = f"({d['snaps'][-1]['C11']:.1f})"
            e_avg = f"({d['snaps'][-1]['E']:.1f})"
        else:
            mark = f"{D}·{W}"
            c11_avg = "—"
            e_avg = "—"
        print(f"  {mark} {name:<12} {d['atoms']:>6} {progress:>10} {c11_avg:>10} {e_avg:>10}")


# ── Header ──
print(f"{BD}{'═'*70}{W}")
print(f"{BD}═══ Elastic Dual Watch (mlip_elastic_snapshot_v2 + v31)  "
      f"({datetime.datetime.now():%H:%M:%S}){W}")
print(f"{BD}{'═'*70}{W}")

# GPU
for line in gpu_info():
    parts = [x.strip() for x in line.split(',')]
    if len(parts) < 6:
        continue
    idx, mu, mt, ut, temp, pw = parts[:6]
    col = G if int(ut) > 30 else (Y if int(ut) > 0 else D)
    print(f"  GPU{idx}: {col}{ut:>3}% util{W}  mem {mu}/{mt} MiB  T={temp}°C  P={float(pw):.1f}W")

# (a) original mlip_elastic_snapshot_v2 (comp2B, comp5)
show_section(
    "mlip_elastic_snapshot_v2 (comp2B, comp5 — original v2 hardcoded loop)",
    "mlip_elastic_snapshot_v2",
    ["mlip_elastic_snapshot_v2.log",
     "mlip_snapshot_v2_log.txt",
     "phase2a_v31_results/run.log"],  # fallback if user named it differently
    color=C
)

# (b) v31 wrapper (comp1_v2, comp2_v2, modelC_v2)
show_section(
    "phase2a_v31 (comp1_v2, comp2_v2, modelC_v2 — v2 anneal champions)",
    "phase2a_v31",
    ["phase2a_v31_results/run.log"],
    color=B
)

print(f"\n{BD}{'═'*70}{W}")
