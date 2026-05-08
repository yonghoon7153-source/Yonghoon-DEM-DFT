#!/usr/bin/env python3
"""ENUM Detailed Watch v2 — fixed done-detection.

Replaces /tmp/watch_enum_detailed.py.

Bug in v1: used `nl >= 32` (LBFGS count) as done criterion, but enum process
advances after fewer LBFGS iterations if convergence reached. Result: pairs
06, 07, 09, 10, 11 had L=29-31 + anneal 5/5 done, enum moved on, but watch
showed them as not-done and pair_06 as Active — confusing.

v2 fix: use `na >= 5` (Stage 3 anneal count) as primary done criterion.
This matches enum's own logic ("done pair N" written to enum.log when na hits 5).
Active pair = first pair where na < 5.

Usage:
  python /tmp/watch_enum_detailed_v2.py
  while true; do clear; python /tmp/watch_enum_detailed_v2.py; sleep 30; done

Auto-detects PID via pgrep -f enumerate_unified_fin.
"""
import json, os, sys, datetime, subprocess
from pathlib import Path

WORK = Path("enum_run")
LOG = "enum.log"
TOTAL_SCF = 13244
N_PAIRS_PLANNED = 26  # planned total (enum may create dirs lazily)
ANNEAL_TARGET = 5

G='\033[92m'; Y='\033[93m'; R='\033[91m'; B='\033[94m'; C='\033[96m'
W='\033[0m'; BD='\033[1m'; D='\033[90m'

# Auto-detect PID if not given
PID = sys.argv[1] if len(sys.argv) > 1 else None
if PID is None:
    try:
        out = subprocess.check_output(['pgrep', '-f', 'enumerate_unified_fin'],
                                       stderr=subprocess.DEVNULL).decode().strip()
        PID = out.split('\n')[0] if out else None
    except subprocess.CalledProcessError:
        PID = None

# ── Header ──
print(f"{BD}{'═'*70}{W}")
print(f"{BD}═══ ENUM Detailed Watch v2 ({datetime.datetime.now():%H:%M:%S}) ═══{W}")
print(f"{BD}{'═'*70}{W}")

# ── Process ──
if PID:
    try:
        out = subprocess.check_output(
            ['ps', '-p', str(PID), '-o', 'pid,etime,pcpu,pmem,rss,stat'],
            stderr=subprocess.DEVNULL).decode()
        print(f"{C}Process:{W}")
        for line in out.strip().split('\n'):
            print(f"  {line}")
    except subprocess.CalledProcessError:
        print(f"  {R}PID {PID} NOT RUNNING{W}")
else:
    print(f"  {Y}No enum process detected (pgrep -f enumerate_unified_fin){W}")

# ── GPU ──
try:
    gpu = subprocess.check_output(
        ['nvidia-smi', '--query-gpu=index,memory.used,memory.total,utilization.gpu,temperature.gpu,power.draw',
         '--format=csv,noheader,nounits'], stderr=subprocess.DEVNULL, timeout=3).decode()
    print(f"{C}GPU:{W}")
    for line in gpu.strip().split('\n'):
        parts = [x.strip() for x in line.split(',')]
        idx, mu, mt, ut, temp, pw = parts[:6]
        col = G if int(ut) > 30 else (Y if int(ut) > 0 else D)
        print(f"  GPU{idx}: {col}{ut:>3}% util{W}  mem {mu}/{mt} MiB  T={temp}°C  P={float(pw):.2f}W")
except Exception:
    pass


# ── Read pair states ──
def read_pair_state(d):
    sf = d / "state.json"
    if not sf.exists():
        return None
    try:
        s = json.loads(sf.read_text())
    except Exception:
        return None
    return {
        'ns': len(s.get('scf', {})),
        'nl': len(s.get('lbfgs', {})),
        'na': len(s.get('annealed', {})),
        'lbfgs': s.get('lbfgs', {}),
        'annealed': s.get('annealed', {}),
        'name': d.name,
    }


def get_E_anneal(v):
    """Try multiple field names for post-anneal energy."""
    for k in ('E_anneal', 'E_post', 'e_anneal', 'e_after', 'e_post'):
        if k in v and v[k] is not None:
            return v[k]
    return None


def get_E_pre(v, lbfgs_dict, name_key):
    """Try multiple field names for pre-anneal energy.
    Falls back to lbfgs[idx]['E'] using parsed index from name like '01141_E'."""
    for k in ('E_pre', 'E_lbfgs', 'e_pre', 'e_before'):
        if k in v and v[k] is not None:
            return v[k]
    # Parse name key like "01141_E" -> lookup lbfgs['01141'] or lbfgs[1141]
    idx_str = name_key.split('_')[0] if '_' in name_key else name_key
    for key in (idx_str, idx_str.lstrip('0') or '0', int(idx_str.lstrip('0') or '0')):
        if key in lbfgs_dict:
            for ek in ('E', 'e', 'energy', 'E_lbfgs'):
                if ek in lbfgs_dict[key] and lbfgs_dict[key][ek] is not None:
                    return lbfgs_dict[key][ek]
    return None


def get_cat(v, name_key):
    """Try cat field, else parse from name like '01141_E'."""
    if 'cat' in v:
        return v['cat']
    if 'category' in v:
        return v['category']
    if '_' in name_key:
        return name_key.rsplit('_', 1)[1]
    return '?'


def progress_bar(done, total, width=15):
    if total == 0:
        return '[' + '·' * width + ']'
    n = int(round(width * done / total))
    return '[' + '█' * n + '·' * (width - n) + ']'


pair_dirs = sorted(WORK.glob("pair_*")) if WORK.exists() else []
pair_states = []
for d in pair_dirs:
    s = read_pair_state(d)
    pair_states.append((d, s))

# Done = na >= ANNEAL_TARGET (matches enum's 'done pair N' criterion)
done_indices = [i for i, (_, s) in enumerate(pair_states)
                if s and s['na'] >= ANNEAL_TARGET]
n_done = len(done_indices)

# Active = first pair where na < ANNEAL_TARGET
active_idx = None
for i, (_, s) in enumerate(pair_states):
    if s is None:
        continue
    if s['na'] < ANNEAL_TARGET:
        active_idx = i
        break

# ── Pair Overview ──
n_existing = len(pair_dirs)
n_total = max(N_PAIRS_PLANNED, n_existing)
print(f"\n{C}Pairs ({n_existing}/{n_total} created, target SCF={TOTAL_SCF}, anneal={ANNEAL_TARGET}):{W}")
for i, (d, s) in enumerate(pair_states):
    name = d.name
    if s is None:
        print(f"  {D}· {name:<30s} no state.json{W}")
        continue
    bar = progress_bar(s['ns'], TOTAL_SCF)
    info = f"SCF{s['ns']:>5d} L{s['nl']:>2d} A{s['na']}"
    if i in done_indices:
        mark = f"{G}✓{W}"
    elif i == active_idx:
        mark = f"{Y}▶{W}"
    else:
        mark = ' '
    print(f"  {mark} {name:<30s} {bar} {info}")
# Placeholder for not-yet-created pairs
for i in range(n_existing, N_PAIRS_PLANNED):
    print(f"  {D}· (pair_{i:02d} not yet created){W}")
print(f"  {BD}Done: {n_done}/{N_PAIRS_PLANNED} pairs ({100*n_done//max(N_PAIRS_PLANNED,1)}%){W}")

# ── Active pair detail ──
if active_idx is not None:
    d, s = pair_states[active_idx]
    print(f"\n{Y}▶ Active: {d.name}{W}")
    print(f"  Stage 1 SCF: {s['ns']}/{TOTAL_SCF}, "
          f"Stage 2 LBFGS: {s['nl']}, "
          f"Stage 3 Anneal: {s['na']}/{ANNEAL_TARGET}")
    if s['annealed']:
        print(f"\n  Anneal status:")
        # rank by E_anneal ascending (lowest = champion)
        items = []
        for k, v in s['annealed'].items():
            E_a = get_E_anneal(v)
            E_p = get_E_pre(v, s.get('lbfgs', {}), k)
            cat = get_cat(v, k)
            items.append((k, v, cat, E_p, E_a))
        items.sort(key=lambda x: (x[4] if x[4] is not None else float('inf')))
        for rank, (k, v, cat, E_pre, E_post) in enumerate(items[:ANNEAL_TARGET], 1):
            tag = "🏆" if rank == 1 else f"#{rank}"
            E_pre_s = f"{E_pre:+.3f}" if E_pre is not None else "  ?  "
            if E_post is not None:
                rest = f"✓ E_a={E_post:+.3f} {tag}"
            else:
                rest = "⏳ in progress"
            print(f"  ★{rank} {k:<14s}  {cat}  E={E_pre_s}  {rest}")

# ── Champions per done pair ──
if done_indices:
    print(f"\n{C}Champions per done pair:{W}")
    cats = {}
    for i in done_indices:
        d, s = pair_states[i]
        if not s['annealed']:
            continue
        # champion = lowest E_anneal among all annealed entries
        scored = []
        for k, v in s['annealed'].items():
            E_a = get_E_anneal(v)
            if E_a is not None:
                scored.append((k, v, E_a))
        if not scored:
            continue
        scored.sort(key=lambda x: x[2])
        kc, vc, E_a_best = scored[0]
        cat = get_cat(vc, kc)
        cats[cat] = cats.get(cat, 0) + 1
        print(f"  {d.name:<30s} cat={cat} E_a={E_a_best:+.3f}")
    if cats:
        print(f"\n  Category distribution: {cats}")

# ── enum.log tail ──
if Path(LOG).exists():
    print(f"\n{D}── enum.log (last 8 lines) ──{W}")
    try:
        tail = subprocess.check_output(['tail', '-8', LOG], stderr=subprocess.DEVNULL).decode()
        for line in tail.rstrip().split('\n'):
            print(f"  {line}")
    except Exception:
        pass

# ── ETA ──
remaining = len(pair_dirs) - n_done
if remaining > 0:
    eta_h = remaining * 3
    eta_d = eta_h / 24
    print(f"\n{C}Total ETA: {remaining} pairs × ~3h = ~{eta_h}h ({eta_d:.1f}일){W}")

print(f"{BD}{'═'*70}{W}")
