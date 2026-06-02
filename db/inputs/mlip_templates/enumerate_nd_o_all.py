"""Comprehensive Nd₂O₃ + O placement enumeration for Model C (Paper #2).

Coverage guarantee — ALL corner variations of PS3O / PS2O2 / PSO3 are enumerated
because we iterate every C(24, 3) combination of the 24 oxygen-eligible sites
(20 PS4 corner S + 4 free anion 4a/4d).

Categorization (auto by # of O at each PS4):
  A: 3 PS3O distributed     C(5,3)·4³  = 640
  B: 2 PS3O + 1 free        C(5,2)·4²·4 = 640
  C: 1 PS3O + 2 free        5·4·C(4,2)  = 120
  D: 3 free                 C(4,3)      = 4
  E: 1 PS2O2 + 1 PS3O       5·C(4,2)·4·4 = 480
  F: 1 PS2O2 + 1 free       5·C(4,2)·4   = 120
  G: 1 PSO3                 5·C(4,3)    = 20
  Total                                  = 2024 = C(24,3)  ✅

Per Nd pair: 3-stage hierarchical screening.
  Stage 1: SCF single-point on all 2024     (~1 s/cfg → ~30 min/pair)
  Stage 2: LBFGS relax on top 20            (~5 min/cfg → ~100 min/pair)
  Stage 3: 500 K MD anneal on top 5         (~30 min/cfg → ~150 min/pair)
Total ~5 h/pair × 26 pairs ≈ 5 days.

Pipeline (PIPELINE.md Step 1-3):
  Step 1: O placement enumerate (this script)
  Step 2: MLIP screen (SCF → LBFGS)
  Step 3: Top-5 → 500 K MD anneal → champion

Translation symmetry dedup: in 1×1×2 supercell, skip Nd pairs where
both indices ≥ n_primitive (those are translations of pairs in lower half).

Reference Nd pair (1, 82) force-included ahead of bins.
"""
from __future__ import annotations
import os, sys, json, itertools, time, gc
from pathlib import Path
import numpy as np
from ase.io import read, write
from ase.optimize import LBFGS
from ase.md.langevin import Langevin
from ase import units

# ---------------------- CONFIG ----------------------
BASE_CIF        = "modelC_112_supercell.cif"     # 1×1×2 supercell, 124 atoms
N_PRIMITIVE     = 62                              # Model C primitive
N_PER_BIN       = 5                               # Nd pairs per distance bin (close/mid/far/very_far/cross-cell)
FORCE_PAIR      = (1, 82)                         # Reference pair (always included)
TOP_K_LBFGS     = 20                              # # of top SCF configs → LBFGS relax per Nd pair
TOP_K_ANNEAL    = 5                               # # of top LBFGS configs → MD anneal per Nd pair
ANNEAL_T        = 500                             # K
ANNEAL_PS       = 50                              # ps
DT_FS           = 2.0                             # MD timestep
LBFGS_FMAX      = 0.05                            # eV/Å for relax
ANNEAL_FMAX     = 0.02                            # eV/Å for post-anneal relax
WORK_DIR        = Path("./enum_run")
DRY_RUN         = "--dry-run" in sys.argv          # only enumerate + count, no MLIP

# UMA fairchem calculator
def make_calc():
    from fairchem.core import OCPCalculator
    return OCPCalculator(
        model_name="uma-s-1p1",
        local_cache="./uma_cache",
        cpu=False,
    )

# ---------------------- ATOM INDEX HELPERS ----------------------
def find_p_and_corners(atoms, p_cutoff=2.4):
    """Return (p_indices, ps4_groups[p_idx]→[s1..s4], all_16e_S, all_free_S)."""
    syms = atoms.get_chemical_symbols()
    p_idx = [i for i, s in enumerate(syms) if s == "P"]
    s_idx = [i for i, s in enumerate(syms) if s == "S"]
    ps4 = {}
    for p in p_idx:
        d = atoms.get_distances(p, s_idx, mic=True)
        nbr = sorted(zip(d, s_idx))[:4]
        ps4[p] = [i for _, i in nbr]
    all_16e = sorted({s for grp in ps4.values() for s in grp})
    all_free = sorted(set(s_idx) - set(all_16e))
    return p_idx, ps4, all_16e, all_free

def find_li_and_halogens(atoms):
    syms = atoms.get_chemical_symbols()
    li = [i for i, s in enumerate(syms) if s == "Li"]
    cl = [i for i, s in enumerate(syms) if s == "Cl"]
    return li, cl

# ---------------------- Nd PAIR GENERATION ----------------------
def generate_nd_pairs(atoms, li_idx, n_per_bin=N_PER_BIN, force_pair=FORCE_PAIR):
    """Generate Nd substitution pairs across distance bins.

    Returns list of dicts: {'pair': (i,j), 'd': float, 'bin': str}.
    Skips translation duplicates (both indices ≥ N_PRIMITIVE).
    """
    pairs = []
    for i, j in itertools.combinations(li_idx, 2):
        if i >= N_PRIMITIVE and j >= N_PRIMITIVE:
            continue   # translation duplicate
        d = atoms.get_distance(i, j, mic=True)
        pairs.append({'pair': (i, j), 'd': d})

    # Distance bins (Å)
    bins = {
        'close':     (0.0,  6.0),
        'mid':       (6.0,  10.0),
        'far':       (10.0, 14.0),
        'very_far':  (14.0, 22.0),
        'cross':     (22.0, 100.0),
    }
    selected = []
    if force_pair is not None:
        # always first
        i, j = force_pair
        d_ref = atoms.get_distance(i, j, mic=True)
        selected.append({'pair': force_pair, 'd': d_ref, 'bin': 'reference'})

    for bname, (lo, hi) in bins.items():
        cands = [p for p in pairs if lo <= p['d'] < hi and p['pair'] != force_pair]
        cands.sort(key=lambda p: p['d'])
        for p in cands[:n_per_bin]:
            p['bin'] = bname
            selected.append(p)
    return selected

# ---------------------- O PLACEMENT GENERATION ----------------------
def categorize(o_combo, all_16e, all_free, s_to_p):
    """Return one of A/B/C/D/E/F/G + per-PS4 corner count dict."""
    free_O = [s for s in o_combo if s in all_free]
    pscorner_O = [s for s in o_combo if s in all_16e]
    n_free = len(free_O)

    # Count O per P
    p_counts = {}
    for s in pscorner_O:
        p = s_to_p[s]
        p_counts[p] = p_counts.get(p, 0) + 1

    if n_free == 3:
        return 'D'
    if n_free == 2:
        return 'C'   # 1 PS3O + 2 free
    if n_free == 1:
        # 2 corner O distributed: PS3O+PS3O or PS2O2
        if len(p_counts) == 2:
            return 'B'         # 2 PS3O + 1 free
        else:
            return 'F'         # 1 PS2O2 + 1 free
    # n_free == 0 → 3 corner O
    if len(p_counts) == 3:
        return 'A'             # 3 PS3O
    if len(p_counts) == 2:
        return 'E'             # PS2O2 + PS3O
    return 'G'                  # PSO3 (single PS4 takes all 3)

def enumerate_o_configs(all_16e, all_free, s_to_p):
    """Enumerate all C(24,3) O placements with category labels."""
    o_pool = list(all_16e) + list(all_free)
    configs = []
    cat_count = {c: 0 for c in 'ABCDEFG'}
    for combo in itertools.combinations(o_pool, 3):
        cat = categorize(combo, all_16e, all_free, s_to_p)
        configs.append({'o_sites': combo, 'category': cat})
        cat_count[cat] += 1
    return configs, cat_count

# ---------------------- STRUCTURE BUILD ----------------------
def build_doped_structure(base, nd_pair, vac_li, o_sites):
    """Apply Nd substitution + Li vacancies + O substitution to base atoms."""
    a = base.copy()
    # Substitute Li → Nd (preserve coordinates)
    syms = list(a.get_chemical_symbols())
    for idx in nd_pair:
        syms[idx] = 'Nd'
    # Remove vacancy Li (charge balance: 4 V_Li per 2 Nd)
    keep = [i for i in range(len(a)) if i not in vac_li]
    # Substitute S → O
    for s in o_sites:
        syms[s] = 'O'
    a = a[keep]
    a.set_chemical_symbols([syms[i] for i in keep])
    return a

def select_vacancy_li(atoms, nd_pair, n_vac=4):
    """Pick 4 Li sites farthest from Nd pair (charge balance)."""
    syms = atoms.get_chemical_symbols()
    li = [i for i, s in enumerate(syms) if s == 'Li' and i not in nd_pair]
    # distance to nearer Nd
    d = []
    for i in li:
        d1 = atoms.get_distance(i, nd_pair[0], mic=True)
        d2 = atoms.get_distance(i, nd_pair[1], mic=True)
        d.append((min(d1, d2), i))
    d.sort(reverse=True)   # farthest first
    return [i for _, i in d[:n_vac]]

# ---------------------- MLIP RUNS ----------------------
def single_point(atoms, calc):
    """Stage 1: SCF only, no relax. ~1 sec/config."""
    atoms.calc = calc
    return atoms.get_potential_energy()

def lbfgs_relax(atoms, calc, fmax=LBFGS_FMAX, steps=200):
    """Stage 2: LBFGS geometry relaxation."""
    atoms.calc = calc
    opt = LBFGS(atoms, logfile=None)
    opt.run(fmax=fmax, steps=steps)
    return atoms.get_potential_energy()

def md_anneal(atoms, calc, T=ANNEAL_T, ps=ANNEAL_PS, dt_fs=DT_FS):
    atoms.calc = calc
    dyn = Langevin(atoms, dt_fs * units.fs, temperature_K=T,
                   friction=0.01 / units.fs, logfile=None)
    dyn.run(int(ps * 1000 / dt_fs))
    # quench
    opt = LBFGS(atoms, logfile=None)
    opt.run(fmax=ANNEAL_FMAX, steps=400)
    return atoms.get_potential_energy()

# ---------------------- MAIN LOOP ----------------------
def main():
    base = read(BASE_CIF)
    li_idx, cl_idx = find_li_and_halogens(base)
    p_idx, ps4_groups, all_16e, all_free = find_p_and_corners(base)
    s_to_p = {s: p for p, group in ps4_groups.items() for s in group}

    # Enumerate Nd pairs
    nd_pairs = generate_nd_pairs(base, li_idx)
    print(f"# Nd pairs: {len(nd_pairs)}")
    for p in nd_pairs:
        print(f"  {p['bin']:10s} {p['pair']}  d = {p['d']:.2f} Å")

    # Enumerate O configs (same set for every Nd pair)
    o_configs, cat_count = enumerate_o_configs(all_16e, all_free, s_to_p)
    print(f"\n# O configs: {len(o_configs)}")
    print("Category distribution:")
    for c in 'ABCDEFG':
        print(f"  {c}: {cat_count[c]}")

    if DRY_RUN:
        print("\n=== DRY RUN: no MLIP execution ===")
        return

    calc = make_calc()
    WORK_DIR.mkdir(exist_ok=True)

    for ip, npair in enumerate(nd_pairs):
        pair_dir = WORK_DIR / f"pair_{ip:02d}_{npair['bin']}_{npair['pair'][0]}_{npair['pair'][1]}"
        pair_dir.mkdir(exist_ok=True)
        state_file = pair_dir / "state.json"
        state = (json.loads(state_file.read_text()) if state_file.exists()
                 else {'scf': {}, 'lbfgs': {}, 'annealed': {}})
        for k in ('scf', 'lbfgs', 'annealed'):
            state.setdefault(k, {})

        vac_li = select_vacancy_li(base, npair['pair'])

        print(f"\n=== Pair {ip}: {npair['pair']} d={npair['d']:.2f} ({npair['bin']}) ===")

        # ----- Stage 1: SCF single-point on all 2024 -----
        t0 = time.time()
        for ic, oc in enumerate(o_configs):
            key = f"{ic:04d}_{oc['category']}"
            if key in state['scf']:
                continue
            atoms = build_doped_structure(base, npair['pair'], vac_li, oc['o_sites'])
            try:
                E = single_point(atoms, calc)
            except Exception as e:
                E = float('nan')
                print(f"  SCF FAIL {key}: {e}")
            state['scf'][key] = {'E': E, 'cat': oc['category'],
                                  'o_sites': list(oc['o_sites'])}
            if ic % 100 == 0:
                state_file.write_text(json.dumps(state, indent=2))
                gc.collect()
        state_file.write_text(json.dumps(state, indent=2))
        print(f"  Stage 1 SCF: {len(state['scf'])} configs in {time.time()-t0:.0f} s")

        # ----- Stage 2: LBFGS relax top-K -----
        ranked = sorted(state['scf'].items(),
                         key=lambda kv: kv[1]['E'] if kv[1]['E'] == kv[1]['E'] else 1e9)
        top_lbfgs = ranked[:TOP_K_LBFGS]
        t0 = time.time()
        for key, info in top_lbfgs:
            if key in state['lbfgs']:
                continue
            ic = int(key.split('_')[0])
            oc = o_configs[ic]
            atoms = build_doped_structure(base, npair['pair'], vac_li, oc['o_sites'])
            try:
                E = lbfgs_relax(atoms, calc)
                write(str(pair_dir / f"lbfgs_{key}.cif"), atoms)
            except Exception as e:
                E = float('nan')
                print(f"  LBFGS FAIL {key}: {e}")
            state['lbfgs'][key] = {'E_lbfgs': E, 'cat': oc['category']}
            state_file.write_text(json.dumps(state, indent=2))
            gc.collect()
        print(f"  Stage 2 LBFGS: {len(state['lbfgs'])} configs in {time.time()-t0:.0f} s")

        # ----- Stage 3: MD anneal top-K -----
        ranked2 = sorted(state['lbfgs'].items(),
                          key=lambda kv: kv[1]['E_lbfgs'] if kv[1]['E_lbfgs'] == kv[1]['E_lbfgs'] else 1e9)
        top_anneal = ranked2[:TOP_K_ANNEAL]
        t0 = time.time()
        for key, info in top_anneal:
            if key in state['annealed']:
                continue
            ic = int(key.split('_')[0])
            oc = o_configs[ic]
            atoms = build_doped_structure(base, npair['pair'], vac_li, oc['o_sites'])
            try:
                E = md_anneal(atoms, calc)
                write(str(pair_dir / f"anneal_{key}.cif"), atoms)
            except Exception as e:
                E = float('nan')
                print(f"  anneal FAIL {key}: {e}")
            state['annealed'][key] = {'E_anneal': E, 'cat': oc['category']}
            state_file.write_text(json.dumps(state, indent=2))
            gc.collect()
        print(f"  Stage 3 anneal: {len(state['annealed'])} configs in {time.time()-t0:.0f} s")

        print(f"  done pair {ip}: SCF={len(state['scf'])}, LBFGS={len(state['lbfgs'])}, anneal={len(state['annealed'])}")

if __name__ == "__main__":
    main()
