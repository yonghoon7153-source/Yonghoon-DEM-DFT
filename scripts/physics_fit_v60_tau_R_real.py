#!/usr/bin/env python3
"""Physics-mode v60 — τ_Dij_R with REAL per-edge resistance weighting.

v59 used a proxy (constriction_share-scaled τ_geom). v60 does it
properly:

  For each case:
    1. Load atoms.csv + contacts.csv
    2. Build SE-SE network (calls network_conductivity.build_network in
       physics mode → per-edge R_bulk + R_constr available)
    3. Build NetworkX graph with TWO edge weights:
         'distance' (Euclidean)
         'R_total'  (R_bulk + R_constr_Mikic)
    4. Run Dijkstra TWO ways:
         path_geom = shortest by 'distance' → τ_Dij_geom
         path_R    = shortest by 'R_total'  → τ_Dij_R
    5. For each path, compute Euclidean length, divide by Δz

  Compare:
    - τ_Dij_geom (existing): path of MIN GEOMETRIC LENGTH
    - τ_Dij_R    (new):      path of MIN ELECTRICAL RESISTANCE
    - τ_Lap_eff  (derived):  Laplacian-effective from σ_full

If τ_Dij_R differs substantially from τ_Dij_geom, our v29 form using
geometric τ is using the wrong path. The R-weighted path is what an
ion actually flows along.

Output:
  - tau_3way_real.csv: per-case τ_geom, τ_R, τ_Lap, σ_P
  - fig6_tau_R_real.png: scatter τ_R vs τ_geom + σ_P prediction
"""
from __future__ import annotations
import sys, json, warnings
from pathlib import Path
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))
from physics_fit_v33_binding import load_phys_rows  # noqa: E402
from v32_exhaustive_refit import load_cases  # noqa: E402
from physics_fit_v53_lasso import enrich_full        # noqa: E402

# Re-use network_conductivity for edge resistance computation
from network_conductivity import build_network          # noqa: E402

WEBAPP = SCRIPTS.parent / 'webapp'
warnings.filterwarnings('ignore')
plt.rcParams.update({'font.size': 10, 'savefig.dpi': 300, 'savefig.bbox': 'tight'})

SIGMA_GRAIN = 3.0
PHI_C = 0.20


def parse_type_map(s):
    """e.g. '1:AM_P,2:AM_S,3:SE' → {1:'AM_P', 2:'AM_S', 3:'SE'}"""
    out = {}
    for tok in s.split(','):
        if ':' in tok:
            k, v = tok.split(':', 1)
            try: out[int(k.strip())] = v.strip()
            except: pass
    return out


def find_case_dir(cid):
    for base in ('webapp/results', 'webapp/archive'):
        for p in Path(base).rglob(f'{cid}'):
            if p.is_dir() and (p / 'atoms.csv').exists():
                return p
    return None


def compute_tau_R(case_dir, type_map, scale=1000.0, n_pairs=200):
    """Compute τ_Dij_geom and τ_Dij_R for one case."""
    atoms_csv = case_dir / 'atoms.csv'
    contacts_csv = case_dir / 'contacts.csv'
    if not (atoms_csv.exists() and contacts_csv.exists()):
        return None

    # Load raw atoms+contacts as the network builder expects
    atoms_df = pd.read_csv(atoms_csv)
    contacts_df = pd.read_csv(contacts_csv, low_memory=False)

    # build_network expects atoms_raw as a dict (id → row), contacts as list.
    atoms_raw = {int(r['id']): {k: r[k] for k in r.index}
                 for _, r in atoms_df.iterrows()}
    contacts_raw = contacts_df.to_dict('records')

    se_types = {k for k, v in type_map.items() if v == 'SE'}
    target_types = se_types

    # Plate z: prefer mesh_info.json if available, else atoms-derived bound.
    mesh_info_p = case_dir / 'mesh_info.json'
    if mesh_info_p.exists():
        try:
            plate_z = float(json.load(open(mesh_info_p))['plate_z'])
        except Exception:
            plate_z = float(atoms_df['z'].max()) + 0.001
    else:
        plate_z = float(atoms_df['z'].max()) + 0.001

    # box_x/box_y from input_params.json (case-specific RVE)
    box_x = box_y = 0.05  # default
    ip_p = case_dir / 'input_params.json'
    if ip_p.exists():
        try:
            ip = json.load(open(ip_p))
            box_x = float(ip.get('box_x', box_x))
            box_y = float(ip.get('box_y', box_y))
        except Exception:
            pass
    try:
        net = build_network(atoms_raw, contacts_raw, target_types,
                             scale=scale, plate_z=plate_z,
                             box_x=box_x, box_y=box_y,
                             contact_mode='physics', mode='ionic',
                             type_map=type_map)
    except Exception as e:
        print(f'  build_network failed: {e}', flush=True)
        return None

    edges = net['edges']
    if not edges:
        return None

    # Build NetworkX graph with two weights
    G = nx.Graph()
    # Atom positions for distance computation (atoms_raw is dict id→row)
    pos = {aid: (a['x'], a['y'], a['z']) for aid, a in atoms_raw.items()}
    radii = {aid: a['radius'] for aid, a in atoms_raw.items()}

    for e in edges:
        i, j = e['id1'], e['id2']
        if i not in pos or j not in pos: continue
        dx = pos[i][0] - pos[j][0]
        dy = pos[i][1] - pos[j][1]
        dz = pos[i][2] - pos[j][2]
        # Periodic distance in xy
        if abs(dx) > box_x / 2: dx -= np.sign(dx) * box_x
        if abs(dy) > box_y / 2: dy -= np.sign(dy) * box_y
        d = np.sqrt(dx*dx + dy*dy + dz*dz) * scale  # μm
        R = float(e.get('R_total', 1.0))
        if R <= 0: R = 1e-9
        G.add_edge(i, j, distance=d, R=R)

    # Find percolating component
    bottom = set(net['bottom']); top = set(net['top'])
    perc_nodes = set()
    for comp in nx.connected_components(G):
        if (comp & bottom) and (comp & top):
            perc_nodes |= comp
    if not perc_nodes:
        return None
    Gp = G.subgraph(perc_nodes)
    src_list = list(bottom & perc_nodes)
    tgt_list = list(top & perc_nodes)
    if not src_list or not tgt_list:
        return None

    # Sample pairs
    import random
    random.seed(42)
    pairs = [(s, t) for s in src_list for t in tgt_list if s != t]
    random.shuffle(pairs)
    pairs = pairs[:n_pairs]

    taus_geom, taus_R = [], []
    for src, tgt in pairs:
        try:
            # τ_Dij_geom: min Euclidean distance path
            path_g = nx.shortest_path(Gp, src, tgt, weight='distance')
            len_g = sum(Gp[path_g[k]][path_g[k+1]]['distance']
                         for k in range(len(path_g) - 1))
            # τ_Dij_R: min resistance path
            path_R = nx.shortest_path(Gp, src, tgt, weight='R')
            len_R = sum(Gp[path_R[k]][path_R[k+1]]['distance']
                         for k in range(len(path_R) - 1))
            z_dist = abs(pos[tgt][2] - pos[src][2]) * scale  # μm
            if z_dist > 0:
                tg = len_g / z_dist
                tR = len_R / z_dist
                if 1.0 <= tg < 30 and 1.0 <= tR < 30:
                    taus_geom.append(tg); taus_R.append(tR)
        except nx.NetworkXNoPath:
            pass

    if not taus_geom:
        return None
    return {
        'tau_geom_mean':   float(np.mean(taus_geom)),
        'tau_geom_median': float(np.median(taus_geom)),
        'tau_R_mean':      float(np.mean(taus_R)),
        'tau_R_median':    float(np.median(taus_R)),
        'n_pairs_used':    len(taus_geom),
    }


def main():
    cases = load_cases()
    rows = enrich_full(load_phys_rows(cases))
    df = pd.DataFrame(rows)
    print(f'Loaded {len(df)} cases.', flush=True)

    # τ_Lap_eff already computable
    df['tau_lap_eff'] = np.sqrt(np.maximum(
        df['phi'].values * SIGMA_GRAIN /
        np.maximum(df['sigma'].values, 1e-12), 1e-9))

    # Compute τ_Dij_R for each case (slow — re-runs build_network)
    print('\nComputing τ_Dij_R per case (rebuilds network with R weights) …',
          flush=True)
    results = []
    for i, row in df.iterrows():
        cid = row['case_id']
        case_dir = find_case_dir(cid)
        if case_dir is None:
            results.append(None); continue
        # type_map from meta.json
        meta_p = case_dir / 'meta.json'
        if not meta_p.exists():
            # try webapp/uploads
            up = WEBAPP / 'uploads' / cid / 'meta.json'
            meta_p = up if up.exists() else None
        type_map = {}
        if meta_p:
            try:
                m = json.load(open(meta_p))
                type_map = parse_type_map(m.get('type_map', ''))
            except Exception: pass
        if not type_map:
            type_map = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}  # default
        scale = (json.load(open(meta_p)).get('scale', 1000)
                 if meta_p else 1000)
        try:
            r = compute_tau_R(case_dir, type_map, scale=scale, n_pairs=80)
        except Exception as e:
            print(f'  case {cid}: {e}', flush=True)
            r = None
        results.append(r)
        if (i + 1) % 10 == 0:
            print(f'  {i+1}/{len(df)} done', flush=True)

    # Pack results
    df['tau_geom_real']   = [r['tau_geom_mean']   if r else np.nan for r in results]
    df['tau_R_real']      = [r['tau_R_mean']      if r else np.nan for r in results]

    valid = df.dropna(subset=['tau_geom_real', 'tau_R_real']).copy()
    print(f'\n  Successful τ_R computation: {len(valid)}/{len(df)} cases',
          flush=True)

    # Stats
    print(f'\n=== Tortuosity comparison ===', flush=True)
    for col, label in [('tau', 'τ existing (in metrics)'),
                        ('tau_geom_real', 'τ_Dij_geom (recomputed)'),
                        ('tau_R_real', 'τ_Dij_R (R-weighted)'),
                        ('tau_lap_eff', 'τ_Lap_eff (Laplacian)')]:
        if col not in valid.columns: continue
        v = valid[col].values
        print(f'  {label:32s}  '
              f'min={v.min():.2f}  median={np.median(v):.2f}  '
              f'max={v.max():.2f}  mean={v.mean():.2f}', flush=True)

    # ── Save CSV first (so partial results survive any later failure) ──
    out = Path('docs/figures/physics_regime')
    out.mkdir(parents=True, exist_ok=True)
    valid[['case_id', 'name', 'tau', 'tau_geom_real', 'tau_R_real',
           'tau_lap_eff', 'sigma']].to_csv(out / 'tau_3way_real.csv',
                                              index=False)
    print(f'\n→ {out}/tau_3way_real.csv  (saved early)', flush=True)

    # Single-feature LOOCV: which τ best predicts σ_P?
    # Manual implementation — avoids sklearn binary-incompatibility issues.
    log_P = np.log(np.maximum(valid['sigma'].values, 1e-12))
    print(f'\n=== Single-feature LOOCV R² (σ_P prediction) ===', flush=True)
    for col, label in [('tau', 'τ existing'),
                        ('tau_geom_real', 'τ_Dij_geom recomputed'),
                        ('tau_R_real', 'τ_Dij_R'),
                        ('tau_lap_eff', 'τ_Lap_eff')]:
        x = np.log(np.maximum(valid[col].values, 1e-3))
        n = len(x); pred = np.empty(n)
        for i in range(n):
            mask = np.ones(n, dtype=bool); mask[i] = False
            xt = x[mask]; yt = log_P[mask]
            denom = np.sum((xt - xt.mean()) ** 2)
            if denom <= 0:
                pred[i] = yt.mean()
                continue
            c = np.sum((xt - xt.mean()) * (yt - yt.mean())) / denom
            it = yt.mean() - c * xt.mean()
            pred[i] = c * x[i] + it
        ss_r = np.sum((log_P - pred) ** 2)
        ss_t = np.sum((log_P - log_P.mean()) ** 2)
        r2_loo = 1 - ss_r / ss_t if ss_t > 0 else float('nan')
        # in-sample slope
        denom_full = np.sum((x - x.mean()) ** 2)
        c_full = (np.sum((x - x.mean()) * (log_P - log_P.mean())) / denom_full
                  if denom_full > 0 else 0.0)
        print(f'  {label:30s}  LOOCV R²={r2_loo:.4f}  '
              f'effective τ exponent: {c_full:+.3f}', flush=True)

    # ── Plot ──
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Subplot 1: τ_Dij_R vs τ_Dij_geom
    ax = axes[0]
    ax.plot([1, 5], [1, 5], 'k--', alpha=0.4, label='τ_R = τ_geom')
    name = valid['name'].astype(str)
    colors = {'1mAh': '#1f77b4', '6mAh': '#2ca02c', '8mAh': '#d62728',
              'particulate': '#ff7f0e'}
    for b, c in colors.items():
        m = name.str.contains(b, case=False, na=False).values
        if m.sum():
            ax.scatter(valid['tau_geom_real'].values[m],
                       valid['tau_R_real'].values[m],
                       c=c, s=40, alpha=0.7, edgecolor='k',
                       linewidth=0.4, label=f'{b} (n={m.sum()})')
    ax.set_xlabel('τ_Dij_geom (Euclidean-weighted)')
    ax.set_ylabel('τ_Dij_R (resistance-weighted)')
    ax.set_title('τ_R vs τ_geom\n(equal if no resistive bottleneck)')
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    # Subplot 2: σ_P vs τ_Dij_geom
    ax = axes[1]
    for b, c in colors.items():
        m = name.str.contains(b, case=False, na=False).values
        if m.sum():
            ax.scatter(valid['tau_geom_real'].values[m],
                       valid['sigma'].values[m],
                       c=c, s=40, alpha=0.7, edgecolor='k',
                       linewidth=0.4, label=b)
    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_xlabel('τ_Dij_geom'); ax.set_ylabel('σ_P (mS/cm)')
    ax.set_title('σ_P vs τ_Dij_geom')
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    # Subplot 3: σ_P vs τ_Dij_R
    ax = axes[2]
    for b, c in colors.items():
        m = name.str.contains(b, case=False, na=False).values
        if m.sum():
            ax.scatter(valid['tau_R_real'].values[m],
                       valid['sigma'].values[m],
                       c=c, s=40, alpha=0.7, edgecolor='k',
                       linewidth=0.4, label=b)
    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_xlabel('τ_Dij_R'); ax.set_ylabel('σ_P (mS/cm)')
    ax.set_title('σ_P vs τ_Dij_R')
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(out / 'fig6_tau_R_real.png', dpi=300)
    plt.close(fig)
    print(f'\n→ {out}/fig6_tau_R_real.png', flush=True)


if __name__ == '__main__':
    main()
