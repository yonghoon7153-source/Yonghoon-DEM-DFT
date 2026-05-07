#!/usr/bin/env python
"""KISTI Watch — ENUM (GPU0) + PHASE 2a v10 (GPU1, Sandwich Wad)

Mirror of /tmp/watch_kisti.py (v10 update).
Master copy: /home01/x3430a02/watch_kisti.py
Repo mirror: 필독/adhesion/watch_kisti.py

v10 changes from v9 watch:
- PHASE_RES: phase2a_v9_results -> phase2a_v10_results
- PHASE_WD_LOG: watchdog_phase2a_v9.log -> watchdog_phase2a_v10.log
- procs grep: phase2a_v9 -> phase2a_v10
- title: "Cleavage Wad" -> "Sandwich Wad (Camacho-Forero 2020)"
- iso parsing: fire_steps -> lbfgs_steps
- progress regex: steps=N E_int=X.XXX Wad=Y (Li_mig top=A pbc=B)
- per-comp: li_mig top + pbc separately
- cross-family verdict: + Camacho-Forero 1.44 J/m^2 LPSCl/Li2S(001) anchor
"""
import os, re, time, subprocess, json, datetime
from pathlib import Path

ENUM_DIR = Path("/scratch/x3430a02/kgy/nd_doped_modelc/1_enumerate")
ENUM_WORK = ENUM_DIR / "enum_run"
ENUM_LOG = ENUM_DIR / "enum.log"
ENUM_WD_LOG = ENUM_DIR / "watchdog.log"

PHASE_DIR = Path("/scratch/x3430a02/kgy/manuscript_support/adhesion_v5_v2")
PHASE_WD_LOG = PHASE_DIR / "watchdog_phase2a_v10.log"
PHASE_RES = PHASE_DIR / "phase2a_v10_results"
PHASE_PROG = PHASE_RES / "progress.log"
PHASE_WAD = PHASE_RES / "wad_results.json"
PHASE_ISO = PHASE_RES / "E_iso.json"

TOTAL_SCF = 13244
N_PAIRS = 26
PAPER_REF = {'comp1': 1.28, 'comp2': 1.18, 'comp3': 2.10, 'comp4': 1.97, 'comp5': 1.65}
CAMACHO_FORERO_ANCHOR = 1.44   # LPSCl/Li2S(001) Wadh, J/m^2 (Chem. Mater. 2020 Table 4)


def sh(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5).stdout.strip()
    except Exception:
        return ""


def head():
    print("═" * 88)
    print(f"  KISTI Watch — ENUM (GPU0) + PHASE 2a v10 (GPU1, Sandwich Wad)  ({time.strftime('%H:%M:%S')})")
    print("═" * 88)


def procs_section():
    out = sh("ps -eo pid,etime,pcpu,rss,stat,cmd | grep -E 'enumerate_unified|phase2a_v10|watchdog_(phase2a|enum)' | grep -v grep")
    enum_p = phase_p = None
    for l in out.splitlines():
        parts = l.split(None, 5)
        if len(parts) < 6:
            continue
        if 'enumerate_unified' in parts[5]:
            enum_p = parts
        elif 'phase2a_v10' in parts[5]:
            phase_p = parts
    print("Processes:")
    if enum_p:
        rss_mb = int(enum_p[3]) // 1024
        print(f"  ● ENUM    (GPU0)  PID={enum_p[0]:>7s}  etime={enum_p[1]:>9s}  cpu={float(enum_p[2]):>5.1f}%  rss={rss_mb:>5d}MB  stat={enum_p[4]}")
    else:
        print("  ○ ENUM    (GPU0)  not running")
    if phase_p:
        rss_mb = int(phase_p[3]) // 1024
        print(f"  ● PHASE2a (GPU1)  PID={phase_p[0]:>7s}  etime={phase_p[1]:>9s}  cpu={float(phase_p[2]):>5.1f}%  rss={rss_mb:>5d}MB  stat={phase_p[4]}")
    else:
        print("  ○ PHASE2a (GPU1)  not running")
    if ENUM_WD_LOG.exists():
        lines = ENUM_WD_LOG.read_text().splitlines()
        n = sum(1 for l in lines if 'retry' in l.lower() or 'start' in l.lower())
        last = next((l for l in reversed(lines) if l.strip()), "")
        print(f"  Watchdog ENUM : {n} events, last: {last[:80]}")
    if PHASE_WD_LOG.exists():
        lines = PHASE_WD_LOG.read_text().splitlines()
        n = sum(1 for l in lines if 'retry' in l.lower() or 'start' in l.lower())
        last = next((l for l in reversed(lines) if l.strip() and ('retry' in l.lower() or 'start' in l.lower())), "")
        if not last:
            last = next((l for l in reversed(lines) if l.strip()), "")
        print(f"  Watchdog PHASE: {n} events, last: {last[:80]}")


def gpus_section():
    out = sh("nvidia-smi --query-gpu=index,memory.used,memory.total,utilization.gpu,temperature.gpu,power.draw --format=csv,noheader,nounits")
    print("\nGPUs:")
    labels = ['ENUM', 'PHASE2a']
    for i, line in enumerate(out.splitlines()[:2]):
        try:
            idx, mu, mt, ut, temp, pwr = [x.strip() for x in line.split(",")]
            lab = labels[i] if i < len(labels) else f"GPU{i}"
            print(f"  GPU{idx} ({lab}): {ut:>3}% util  mem {mu}/{mt} MiB  T={temp}°C  P={pwr}W")
        except Exception:
            pass


def enum_section():
    print("\n━━━ [1] ENUM Nd₂O₃ + O ━━━")
    if not ENUM_WORK.exists():
        print("  (enum_run/ not found)")
        return
    pair_dirs = sorted(ENUM_WORK.glob("pair_*"))
    if not pair_dirs:
        print("  (no pair_* dirs yet)")
        return
    pairs_data = []
    current_pair = None
    for d in pair_dirs:
        sf = d / "state.json"
        if not sf.exists():
            continue
        try:
            s = json.loads(sf.read_text())
        except Exception:
            continue
        ns = len(s.get('scf', {}))
        nl = len(s.get('lbfgs', {}))
        na = len(s.get('annealed', {}))
        done = (na >= 5)
        if not done and current_pair is None:
            current_pair = (d, s)
        pairs_data.append((d, s, ns, nl, na, done))
    n_done = 0
    for d, s, ns, nl, na, done in pairs_data:
        pct = ns / TOTAL_SCF
        bar = '█' * int(15 * pct) + '░' * (15 - int(15 * pct))
        mark = "✓" if done else ("▶" if current_pair and d == current_pair[0] else " ")
        print(f"  {mark} {d.name:<32} [{bar}] SCF{ns:<5d} L{nl:<2d} A{na}")
        if done:
            n_done += 1
    eta = max(N_PAIRS - n_done, 0) * 2.5
    print(f"  Done: {n_done}/{N_PAIRS}  ETA: {eta:.0f}h")
    if current_pair:
        d, s = current_pair
        mtime = datetime.datetime.fromtimestamp((d / 'state.json').stat().st_mtime)
        age_min = (datetime.datetime.now() - mtime).total_seconds() / 60
        print(f"\n  ▶ {d.name} (state mtime {age_min:.0f}min ago)")
        lbfgs = s.get('lbfgs', {})
        annealed = s.get('annealed', {})
        if lbfgs:
            ranked = sorted(lbfgs.items(), key=lambda kv: kv[1].get('E_lbfgs', 1e9))
            for i, (key, info) in enumerate(ranked[:5], 1):
                E = info.get('E_lbfgs', float('nan'))
                cat = info.get('cat', '?')
                if key in annealed:
                    E_a = annealed[key].get('E_anneal', float('nan'))
                    a_ranked = sorted(annealed.items(), key=lambda kv: kv[1].get('E_anneal', 1e9))
                    a_rank = next((j + 1 for j, (k, _) in enumerate(a_ranked) if k == key), 0)
                    trophy = "🏆" if a_rank == 1 else f"#{a_rank}"
                    print(f"  ★{i} {key:<12} {cat:<2} E={E:>9.3f}  ✓ E_a={E_a:>8.3f} {trophy}")
                else:
                    if i <= len(annealed) + 1:
                        print(f"  ★{i} {key:<12} {cat:<2} E={E:>9.3f}  ⏳ in progress (~{age_min:.0f}min)")
                    else:
                        print(f"  ★{i} {key:<12} {cat:<2} E={E:>9.3f}  (pending)")
    champs = [(d, s) for d, s, ns, nl, na, done in pairs_data if done]
    if champs:
        print("\n  Champions:")
        cat_dist = {}
        for d, s in champs:
            ann = s.get('annealed', {})
            best = min(ann.items(), key=lambda kv: kv[1].get('E_anneal', 1e9), default=(None, None))
            if best[0]:
                cat = best[1].get('cat', '?')
                E_a = best[1].get('E_anneal', 0)
                print(f"    {d.name:<32} cat={cat} E_a={E_a:>8.3f}")
                cat_dist[cat] = cat_dist.get(cat, 0) + 1
        print(f"    Cat dist: {cat_dist}")


def parse_progress_log():
    """Parse v10 progress.log: [N/216] comp/reg steps=N E_int=X Wad=Y [Li_mig top=A pbc=B] (Xmin) ETA=Yh"""
    if not PHASE_PROG.exists():
        return {}, []
    text = PHASE_PROG.read_text()
    pat = re.compile(
        r"\[(\d+)/216\]\s+(\w+)/(\w+)\s+steps=(\d+)\s+E_int=([\-\d.]+)\s+Wad=([\+\-\d.]+)"
        r"(?:\s+Li_mig\s+top=(\d+)\s+pbc=(\d+))?\s+\(([\d.]+)min\)\s+ETA=([\d.]+)h"
    )
    by_comp = {}
    rows = []
    for m in pat.finditer(text):
        n, comp, reg, steps, E, W, lim_top, lim_pbc, wall, eta = m.groups()
        lt = int(lim_top) if lim_top else 0
        lp = int(lim_pbc) if lim_pbc else 0
        info = {
            'idx': int(n), 'steps': int(steps),
            'E': float(E), 'Wad': float(W),
            'li_mig_top': lt, 'li_mig_pbc': lp, 'li_mig': lt + lp,
            'wall_min': float(wall), 'eta_h': float(eta),
        }
        by_comp.setdefault(comp, {})[reg] = info
        rows.append((comp, reg, info))
    return by_comp, rows


def phase_section():
    print("\n━━━ [2] PHASE 2a v10 — Sandwich Wad (Round-robin) ━━━")
    print(f"  Method: Camacho-Forero 2020 (sandwich, no vacuum, /(2A))")
    print(f"  Anchors: paper #1 v5 (per-comp PAPER_REF) + Camacho-Forero LPSCl/Li2S(001)={CAMACHO_FORERO_ANCHOR} J/m²")
    if not PHASE_PROG.exists():
        print("\n  (waiting — phase2a_v10_results/progress.log not yet created)")
        if PHASE_WD_LOG.exists():
            print("\n  Watchdog log (last 5):")
            for l in PHASE_WD_LOG.read_text().splitlines()[-5:]:
                print(f"    {l}")
        return
    iso = json.loads(PHASE_ISO.read_text()) if PHASE_ISO.exists() else {}
    print(f"\n  Stage A — Iso ({len(iso)}/8):")
    for k, v in iso.items():
        n = v.get('n', 0)
        E = v.get('E', 0)
        E_per = E / n if n else 0
        nf = v.get('n_fixed', '-')
        steps = v.get('lbfgs_steps', '?')
        typ = v.get('type', '')
        wall = v.get('wall_min', 0)
        print(f"    {k:<36} {E_per:>8.4f} eV/atom ({n:>4d} at) fix={nf} steps={steps} {wall:>4.1f}min {typ}")
    by_comp, rows = parse_progress_log()
    comps = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5', 'modelC']
    cycle = max((len(by_comp.get(c, {})) for c in comps), default=0)
    n_reg = 36
    print(f"\n  Stage B — Round-robin (Current Cycle: {cycle}/{n_reg}):")
    li6_w, li54_w = [], []
    for c in comps:
        regs = by_comp.get(c, {})
        wads = [r['Wad'] for r in regs.values()]
        n = len(wads)
        if n:
            avg = sum(wads) / n
            std = (sum((w - avg)**2 for w in wads) / n)**0.5 if n > 1 else 0
            ref = PAPER_REF.get(c)
            ref_s = f"vs paper {ref}: {avg/ref:.2f}×" if ref else "no ref"
            li_top_avg = sum(r['li_mig_top'] for r in regs.values()) / n
            li_pbc_avg = sum(r['li_mig_pbc'] for r in regs.values()) / n
            li_max = max(r['li_mig'] for r in regs.values())
            wall = sum(r['wall_min'] for r in regs.values()) / n
            wstr = f"{wall:.1f}min/iface"
        else:
            avg = std = 0
            ref = PAPER_REF.get(c)
            ref_s = f"vs paper {ref}: -" if ref else "no ref"
            li_top_avg = li_pbc_avg = 0
            li_max = 0
            wstr = ""
        bar_n = int(20 * n / n_reg)
        bar = "█" * bar_n + "░" * (20 - bar_n)
        wstr2 = f"W={avg:+.3f}±{std:.2f}" if n else "W=-"
        print(f"    {c:<8} [{bar}] {n:>3d}/{n_reg}  {wstr2}  {ref_s}  "
              f"Li_mig top={li_top_avg:>3.1f} pbc={li_pbc_avg:>3.1f} max={li_max}  {wstr}")
        if c in ('comp1', 'comp2'):
            li6_w.extend(wads)
        else:
            li54_w.extend(wads)
    total_done = sum(len(by_comp.get(c, {})) for c in comps)
    total = len(comps) * n_reg
    pct = 100 * total_done / total if total else 0
    print(f"  Total: {total_done}/{total} = {pct:.1f}%")
    if li6_w and li54_w:
        l6 = sum(li6_w) / len(li6_w)
        l54 = sum(li54_w) / len(li54_w)
        verdict = "✓ PAPER MATCH (Li5.4 > Li6, vacancy chemical anchor)" if l54 > l6 else "✗ INVERTED (Li6 > Li5.4, sandwich method bug?)"
        print(f"\n  Cross-family: Li6={l6:.3f}  Li5.4+modelC={l54:.3f}  {verdict}")
        print(f"  Anchor (Camacho-Forero 2020): LPSCl/Li2S(001) Wadh = {CAMACHO_FORERO_ANCHOR} J/m² "
              f"(comp1 LPSCl/NCM scale check: {l6:.3f} J/m² vs {CAMACHO_FORERO_ANCHOR})")
    if rows:
        print("\n  Latest results (last 5):")
        for c, r, info in rows[-5:]:
            tag = "Li6" if c in ('comp1', 'comp2') else ("modelC" if c == 'modelC' else "Li5.4")
            li_mig_str = ""
            if info['li_mig'] > 0:
                li_mig_str = f" Li_mig top={info['li_mig_top']} pbc={info['li_mig_pbc']}"
            print(f"    [{info['idx']:>3}/216] {c:<7}/{r:<10} {tag:<6} steps={info['steps']:>3} "
                  f"W={info['Wad']:+.3f}{li_mig_str} ({info['wall_min']:.1f}min)")


def log_tails():
    if ENUM_LOG.exists():
        out = sh(f"tail -4 {ENUM_LOG}")
        if out:
            print("\n── ENUM log (last 4) ──")
            for l in out.splitlines():
                print(f"  {l[:110]}")
    if PHASE_PROG.exists():
        out = sh(f"tail -4 {PHASE_PROG}")
        if out:
            print("\n── PHASE2a v10 log (last 4) ──")
            for l in out.splitlines():
                print(f"  {l[:110]}")


def main():
    head()
    procs_section()
    gpus_section()
    enum_section()
    phase_section()
    log_tails()
    print("═" * 88)


if __name__ == "__main__":
    main()
