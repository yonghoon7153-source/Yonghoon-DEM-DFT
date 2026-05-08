#!/usr/bin/env python3
"""Watch v31c MLIP 600K snapshot elastic (comp1_v2/comp2_v2/modelC_v2).

(Earlier mlip_elastic_snapshot_v2 section removed — that script had bugs and
was superseded by v31c.)

Run on KISTI from /scratch/x3430a02/kgy/manuscript_support/:
  python /tmp/watch_elastic_dual.py

Continuous:
  while true; do clear; python /tmp/watch_elastic_dual.py; sleep 30; done
"""
import os, re, sys, subprocess, datetime
from pathlib import Path

G='\033[92m'; Y='\033[93m'; R='\033[91m'; B='\033[94m'; C='\033[96m'
W='\033[0m'; BD='\033[1m'; D='\033[90m'

N_SNAPSHOTS = 5
EXPECTED_COMPS = ['comp1_v2', 'comp2_v2', 'modelC_v2']


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


def parse_log(text):
    """Parse v31c md_then_snapshot_elastic output.

    Banner: '<spaces><comp_name> - MD(600K) -> 5 snapshots -> 0K elastic'
    Atoms: 'loaded: NN atoms, ...'
    Snap:  'snap N: C11=..., C12=..., C44=..., E=...'
    Avg:   '=== compname Average ==='
    """
    if not text:
        return {}
    comps = {}
    cur_comp = None
    comp_re_old = re.compile(r'^---\s*(\S+)\s+\((\d+)\s+atoms\)\s*---', re.M)
    comp_re_new = re.compile(r'^\s+(\S+)\s+-\s+MD\(\d+K\)\s+->\s+\d+\s+snapshots', re.M)
    atoms_re = re.compile(r'========= (\S+) =========')
    loaded_re = re.compile(r'loaded:\s+(\d+)\s+atoms')
    snap_re = re.compile(r'snap\s+(\d+):\s+C11=([\d.]+),\s+C12=([\d.]+),\s+C44=([\d.]+),\s+E=([\d.]+)')
    avg_old_re = re.compile(r'AVG:\s+C11=([\d.]+).*?E=([\d.]+)')
    avg_new_re = re.compile(r'===\s+(\S+)\s+Average\s+===')

    pending_atoms = None
    last_section_comp = None  # from "========= compname ====="
    for line in text.split('\n'):
        m = atoms_re.search(line)
        if m:
            last_section_comp = m.group(1)
            if last_section_comp not in comps:
                comps[last_section_comp] = {'atoms': 0, 'snaps': [], 'avg': None}
            cur_comp = last_section_comp
            continue
        m = loaded_re.search(line)
        if m and last_section_comp:
            comps[last_section_comp]['atoms'] = int(m.group(1))
            continue
        m = comp_re_old.match(line)
        if m:
            cur_comp = m.group(1)
            if cur_comp not in comps:
                comps[cur_comp] = {'atoms': int(m.group(2)), 'snaps': [], 'avg': None}
            else:
                comps[cur_comp]['atoms'] = int(m.group(2))
            continue
        m = comp_re_new.match(line)
        if m:
            cur_comp = m.group(1)
            if cur_comp not in comps:
                comps[cur_comp] = {'atoms': 0, 'snaps': [], 'avg': None}
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
        m = avg_old_re.search(line)
        if m:
            comps[cur_comp]['avg'] = {
                'C11': float(m.group(1)), 'E': float(m.group(2)),
            }
            continue
        m = avg_new_re.search(line)
        if m:
            avg_name = m.group(1)
            # 'Average' summary just marks where to look — actual values are in
            # multiple lines after. Use last snap's mean as proxy if not parsed.
            pass
    return comps


def progress_bar(done, total, width=12):
    if total == 0:
        return '[' + '·' * width + ']'
    n = int(round(width * done / total))
    return '[' + '█' * n + '·' * (width - n) + ']'


# ── Header ──
print(f"{BD}{'═'*70}{W}")
print(f"{BD}═══ v31c MLIP Elastic Watch ({datetime.datetime.now():%H:%M:%S}){W}")
print(f"{BD}{'═'*70}{W}")

# GPU
for line in gpu_info():
    parts = [x.strip() for x in line.split(',')]
    if len(parts) < 6:
        continue
    idx, mu, mt, ut, temp, pw = parts[:6]
    col = G if int(ut) > 30 else (Y if int(ut) > 0 else D)
    print(f"  GPU{idx}: {col}{ut:>3}% util{W}  mem {mu}/{mt} MiB  T={temp}°C  P={float(pw):.1f}W")

# v31c section
print(f"\n{BD}{C}── v31c (comp1_v2, comp2_v2, modelC_v2 v2 anneal champions) ──{W}")
pid = find_pid("phase2a_v31")
if pid:
    info = proc_info(pid)
    print(f"  PID {pid}: {G}RUNNING{W}  {info or ''}")
else:
    print(f"  {Y}no process detected{W}")

LOG = Path("phase2a_v31_results/run.log")
if not LOG.exists():
    print(f"  {D}no log yet ({LOG}){W}")
else:
    text = LOG.read_text()
    comps = parse_log(text)
    if not comps:
        # show last 10 lines
        last = text.rstrip().split('\n')[-10:]
        print(f"  {D}log parsing pending. Last lines:{W}")
        for line in last:
            print(f"    {D}{line}{W}")
    else:
        n_done = sum(1 for d in comps.values() if d['avg'])
        n_total_expected = len(EXPECTED_COMPS)
        print(f"  Done {n_done}/{n_total_expected} comps  "
              f"{progress_bar(n_done, n_total_expected, 14)}")
        print(f"  {'comp':<14} {'atoms':>6} {'snaps':>10} {'C11 avg':>10} {'E avg':>10}")
        for name in EXPECTED_COMPS:
            if name not in comps:
                print(f"  {D}· {name:<12} {'—':>6} {'pending':>10} {'—':>10} {'—':>10}{W}")
                continue
            d = comps[name]
            n_snap = len(d['snaps'])
            progress = f"{n_snap}/{N_SNAPSHOTS}"
            atoms_s = str(d['atoms']) if d['atoms'] else '?'
            if d['avg']:
                mark = f"{G}✓{W}"
                c11_s = f"{d['avg']['C11']:.1f}"
                e_s = f"{d['avg']['E']:.1f}"
            elif n_snap > 0:
                mark = f"{Y}▶{W}"
                # running mean across snaps so far
                c11_s = f"({sum(s['C11'] for s in d['snaps'])/n_snap:.1f})"
                e_s = f"({sum(s['E'] for s in d['snaps'])/n_snap:.1f})"
            else:
                mark = f"{Y}▶{W}" if name == EXPECTED_COMPS[0] and pid else f"{D}·{W}"
                c11_s = "—"
                e_s = "—"
            print(f"  {mark} {name:<12} {atoms_s:>6} {progress:>10} {c11_s:>10} {e_s:>10}")

        # Show last 3 lines from log for context
        print(f"\n  {D}─── Last 3 log lines ───{W}")
        for line in text.rstrip().split('\n')[-3:]:
            print(f"    {D}{line}{W}")

print(f"{BD}{'═'*70}{W}")
