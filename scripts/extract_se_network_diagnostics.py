#!/usr/bin/env python3
"""Phase C — Batch SE network diagnostics + paper-quality figure.

For every case in webapp/results/ + webapp/archive/:
  1. Load atoms.csv + contacts.csv
  2. Run compute_se_network_diagnostics() (Phase A5+A6 code path)
  3. Extract composition (AM:SE, P:S, scale, φ_SE)
  4. Aggregate per-case stats:
       - n_percolating, n_cut, n_bn
       - bn_min, bn_median areas (μm²)
       - dead-end cluster counts
       - cut_fraction (n_cut / n_percolating)

Writes:
  docs/data/se_diagnostics_82.csv         — full per-case table
  docs/figures/percolation_risk_scaling.png  — 4-panel paper figure

Usage:
  python3 scripts/extract_se_network_diagnostics.py
  python3 scripts/extract_se_network_diagnostics.py --csv-only
  python3 scripts/extract_se_network_diagnostics.py --no-plot
"""
from __future__ import annotations
import argparse, csv, hashlib as _hashlib, json, math, os, sys
from pathlib import Path

ROOT   = Path(__file__).resolve().parent.parent
WEBAPP = ROOT / 'webapp'
SCRIPTS = ROOT / 'scripts'
DATA_DIR = ROOT / 'docs' / 'data'
FIG_DIR  = ROOT / 'docs' / 'figures'
sys.path.insert(0, str(SCRIPTS))

import numpy as np

#  ★★ 지연 import — 이 모듈의 **로더**(discover_cases · load_case · load_contacts)를
#     쓰려고 import 하는 소비자가 matplotlib · networkx(viewer3d_data) 까지 끌고 오지
#     않게 한다.  그 둘은 `analyze_case`(진단 솔브)와 `make_figure`(그림)에만 필요하다.
#     ⚠ 실제 계기: S0 도구(`audit_constriction_deleted.py`)를 **kgy 에서** 돌려야 하는데
#     그 머신엔 pip install 이 금지다 — 무거운 의존이 import 단계에서 죽으면 로더까지
#     못 쓴다.  로더는 stdlib + numpy 만으로 돈다.
_plt = None


def _get_plt():
    """matplotlib 을 그림 그릴 때만 가져온다 (Agg 고정)."""
    global _plt
    if _plt is None:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        plt.rcParams.update(_RC)
        _plt = plt
    return _plt


_RC = {
    'font.family': 'DejaVu Serif',
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 11,
    'axes.titleweight': 'bold',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 8.5,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
}


_TS_PAT = __import__('re').compile(r'^\d{6}_\d{6}_[0-9a-f]{6,}$')

def _is_timestamp_name(name: str) -> bool:
    """True for archive timestamp IDs like 260421_213656_78ec86."""
    return bool(_TS_PAT.match(name))


def _pair_digest(d: Path) -> str:
    """atoms.csv + contacts.csv 의 **내용** 지문.

    ★ L4-06 — 옛 중복제거 키는 `(atoms 바이트, contacts 바이트)` 였다.  **같은 크기는
    같은 자료의 증거가 아니다**: 이 리포에서 재현했다 — 자리수만 맞춘 서로 다른 두
    사례(atoms 84 B · contacts 33 B 로 동일)를 넣으면 `discover_cases` 가 **하나만**
    돌려준다 (어느 쪽이 살아남는지는 rglob 순서에 달렸다 = 조용한 자료 손실).
    코퍼스가 grade 의 **백분위 기준**이 되므로 여기서 빠지면 그 기준까지 옮겨간다.

    ⚠ 크기 묶음이 **1개면 해시하지 않는다** — 흔한 경우의 비용을 0 으로 두고,
    실제로 충돌 후보가 생긴 묶음에서만 내용을 읽는다.
    """
    h = _hashlib.blake2b(digest_size=16)
    for fn in ('atoms.csv', 'contacts.csv'):
        h.update(fn.encode()); h.update(b'\0')
        with (d / fn).open('rb') as f:
            for chunk in iter(lambda: f.read(1 << 20), b''):
                h.update(chunk)
        h.update(b'\0')
    return h.hexdigest()


CASE_REQUIRED = ('atoms.csv', 'contacts.csv', ('input_params.json', 'meta.json'))


def case_layout_report(root: Path, limit: int = 3) -> str:
    """`root` 아래 첫 몇 하위 폴더의 파일 목록 — **왜 케이스를 못 찾았는지**를 사용자가
    그대로 붙일 수 있게 찍는다 (경로를 두 번 물어보지 않기 위해)."""
    lines = [f'  {root} 의 하위 폴더 (처음 {limit}개):']
    subs = sorted([d for d in root.iterdir() if d.is_dir()])[:limit] if root.is_dir() else []
    if not subs:
        lines.append('    (하위 폴더 없음)')
    for d in subs:
        names = sorted(x.name for x in d.iterdir())[:12]
        lines.append(f'    {d.name}/  →  {", ".join(names)}{" …" if len(list(d.iterdir())) > 12 else ""}')
    lines.append('  필요한 것: 케이스 폴더마다 atoms.csv + contacts.csv + (input_params.json | meta.json)')
    return '\n'.join(lines)


def discover_cases(flat: bool = False) -> list[Path]:
    """Walk both results/ and archive/, dedup by the **content digest** of
    (atoms.csv, contacts.csv).  Prefer NAMED case_ids (input_*, etc.) over
    timestamp-style IDs when both exist for the same analysis.

    `flat=True` — `WEBAPP` 자체가 케이스 폴더들을 **직접** 담고 있을 때 (예: `~/lhs_local/
    lhs00_100/atoms.csv`).  results/·archive/ 층이 없는 로컬 보관 폴더용.
    """
    # Pass 1: collect every candidate dir
    cands = []
    for base in (('.',) if flat else ('results', 'archive')):
        root = WEBAPP if base == '.' else WEBAPP / base
        if not root.exists():
            continue
        for atoms_p in root.rglob('atoms.csv'):
            d = atoms_p.parent
            if not ((d / 'contacts.csv').exists() and
                    ((d / 'input_params.json').exists() or
                     (d / 'meta.json').exists())):
                continue
            try:
                size = atoms_p.stat().st_size
                ct_size = (d / 'contacts.csv').stat().st_size
            except OSError:
                continue
            cands.append((d, size, ct_size))

    # Pass 2: dedup by the **content** digest; within a key, prefer
    # non-timestamp names (i.e., human-readable input_* over hex IDs).
    #  L4-06 — 크기가 겹치는 묶음에서만 내용을 읽는다 (묶음 1개 = 해시 불필요).
    _size_groups: dict[tuple, int] = {}
    for _d, _a, _c in cands:
        _size_groups[(_a, _c)] = _size_groups.get((_a, _c), 0) + 1
    by_key: dict[tuple, Path] = {}
    for d, asize, csize in cands:
        if _size_groups[(asize, csize)] > 1:
            try:
                key = (asize, csize, _pair_digest(d))
            except OSError:
                continue
        else:
            key = (asize, csize, None)
        if key not in by_key:
            by_key[key] = d
        else:
            cur = by_key[key]
            cur_is_ts = _is_timestamp_name(cur.name)
            new_is_ts = _is_timestamp_name(d.name)
            if cur_is_ts and not new_is_ts:
                by_key[key] = d   # named wins over timestamp
    return sorted(by_key.values())


class MetaConflict(ValueError):
    """두 메타데이터 파일이 같은 필드를 **다르게** 말한다 — 추측하지 않고 거부한다."""


def load_meta_merged(case_dir: Path):
    """`input_params.json` ∪ `meta.json` — **필드별 병합, 충돌은 거부**.

    ★ L4-07 — 옛 코드는 존재하는 **첫 파일을 읽자마자 `break`** 했다.  그래서
    `input_params.json` 에 `scale` 만 있고 `meta.json` 에 `1:AM_P, 2:SE` 가 있는
    정상적인 배치에서 **상 지도를 아예 못 본다**.  이 리포에서 재현: 실제 입자 5개가
    전부 type 2 인데 3-type 기본 지도가 들어가 `type_map = {1:AM_P, 2:AM_S, 3:SE}` ·
    **추론 SE = 0개**.
    ⚠ *'모든 mono 가 잘못된다'* 는 얘기가 아니다 — **정상적으로 표현 가능한 메타데이터
    배치에서 상이 사라진다**는 반례다.

    병합 뒤 같은 키를 두 파일이 다르게 말하면 `MetaConflict` 로 **거부**한다 —
    한쪽을 조용히 이기게 하면 어느 쪽을 계산했는지 사후에 알 수 없다.
    """
    merged: dict = {}
    origin: dict = {}
    for fname in ('input_params.json', 'meta.json'):
        p = case_dir / fname
        if not p.exists():
            continue
        try:
            got = json.loads(p.read_text())
        except Exception:
            continue
        if not isinstance(got, dict):
            continue
        for k, v in got.items():
            if k in merged and merged[k] != v:
                raise MetaConflict(
                    f'{case_dir.name}: 필드 {k!r} 를 {origin[k]} 는 {merged[k]!r} 로, '
                    f'{fname} 는 {v!r} 로 말한다 — 어느 쪽을 계산했는지 알 수 없어 거부한다')
            merged[k] = v
            origin.setdefault(k, fname)
    return merged, origin


def load_case(case_dir: Path):
    """Returns (atoms_by_id, type_map, scale, meta)."""
    meta, _meta_origin = load_meta_merged(case_dir)
    scale = float(meta.get('scale') or 1000.0)
    # type_map: prefer "1:AM_P,2:AM_S,3:SE" string format
    type_map = {}
    tm = meta.get('type_map')
    if isinstance(tm, str):
        for tok in tm.split(','):
            if ':' in tok:
                k, v = tok.split(':', 1)
                try:
                    type_map[int(k.strip())] = v.strip()
                except Exception:
                    pass
    elif isinstance(tm, dict):
        for k, v in tm.items():
            try:
                type_map[int(k)] = str(v)
            except Exception:
                pass
    if not type_map:
        type_map = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}

    atoms = {}
    with (case_dir / 'atoms.csv').open() as f:
        for r in csv.DictReader(f):
            try:
                aid = int(r['id'])
            except Exception:
                continue
            atoms[aid] = {
                'type':   int(r.get('type', 0) or 0),
                'radius': float(r.get('radius', 0) or 0),
                'x':      float(r.get('x', 0) or 0),
                'y':      float(r.get('y', 0) or 0),
                'z':      float(r.get('z', 0) or 0),
            }
    return atoms, type_map, scale, meta


def load_contacts(case_dir: Path):
    out = []
    p = case_dir / 'contacts.csv'
    if not p.exists():
        return out
    with p.open() as f:
        for r in csv.DictReader(f):
            try:
                i1 = int(r['id1']); i2 = int(r['id2'])
            except Exception:
                continue
            area = float(r.get('contact_area', 0) or 0)
            delta = float(r.get('delta', 0) or 0)
            out.append({
                'id1': i1, 'id2': i2,
                'contact_area': area, 'delta': delta,
            })
    return out


def estimate_plate_z(atoms: dict) -> float:
    """Topmost z + radius among all particles (sim units)."""
    if not atoms:
        return 0.0
    return max(a['z'] + a['radius'] for a in atoms.values())


def load_composition(case_dir: Path, meta: dict):
    """Extract AM_wt fraction, P:S ratio, λ_eff, φ_SE, campaign.

    Falls back to all_dem_porosity.csv lookup if meta is incomplete."""
    am_wt = meta.get('am_wt')
    se_wt = meta.get('se_wt')
    p_vol = meta.get('p_vol') or 0
    s_vol = meta.get('s_vol') or 0
    r_AM_P = meta.get('r_AM_P_um') or 0
    r_AM_S = meta.get('r_AM_S_um') or 0
    r_SE   = meta.get('r_SE_um') or 0
    campaign = meta.get('campaign') or '?'

    # Lookup in all_dem_porosity.csv (canonical source — also has campaign)
    porosity_csv = ROOT / 'all_dem_porosity.csv'
    if porosity_csv.exists():
        case_id = case_dir.name
        for r in csv.DictReader(porosity_csv.open()):
            if r.get('case_id', '').strip() == case_id:
                am_wt  = float(r.get('am_wt', am_wt or 0) or 0)
                se_wt  = float(r.get('se_wt', se_wt or 0) or 0)
                p_vol  = float(r.get('p_vol', 0) or 0)
                s_vol  = float(r.get('s_vol', 0) or 0)
                r_AM_P = float(r.get('r_AM_P_um', 0) or 0)
                r_AM_S = float(r.get('r_AM_S_um', 0) or 0)
                r_SE   = float(r.get('r_SE_um', 0) or 0)
                campaign = (r.get('campaign') or '').strip() or campaign
                break

    # Effective r_AM (volume-weighted)
    if p_vol + s_vol > 0:
        r_eff = (p_vol*r_AM_P + s_vol*r_AM_S) / (p_vol + s_vol)
        f_AMP = p_vol / (p_vol + s_vol)
    elif r_AM_S > 0:
        r_eff = r_AM_S; f_AMP = 0.0
    else:
        r_eff = r_AM_P; f_AMP = 1.0
    lam_eff = (r_eff / r_SE) if r_SE > 0 else 0
    # Volume fraction (ρ_AM=4.8, ρ_SE=2.0 g/cm³)
    V_AM = (am_wt or 0) / 4.8
    V_SE = (se_wt or (100 - (am_wt or 0))) / 2.0
    phi_SE = V_SE / (V_AM + V_SE) if (V_AM + V_SE) > 0 else 0
    return {
        'campaign': campaign,
        'am_wt':   am_wt or 0,
        'se_wt':   se_wt or (100 - (am_wt or 0)),
        'p_vol':   p_vol,
        's_vol':   s_vol,
        'f_AMP':   f_AMP,
        'r_AM_P':  r_AM_P,
        'r_AM_S':  r_AM_S,
        'r_SE':    r_SE,
        'lam_eff': lam_eff,
        'phi_SE':  phi_SE,
    }


def analyze_case(case_dir: Path, debug: bool = False) -> dict | None:
    case_id = case_dir.name
    try:
        atoms, type_map, scale, meta = load_case(case_dir)
        contacts = load_contacts(case_dir)
        plate_z = estimate_plate_z(atoms)
        if debug:
            se_types = {k for k, v in type_map.items() if v == 'SE'}
            n_se = sum(1 for a in atoms.values() if a['type'] in se_types)
            n_se_contacts = sum(1 for c in contacts
                                  if (c['id1'] in atoms and c['id2'] in atoms and
                                      atoms[c['id1']]['type'] in se_types and
                                      atoms[c['id2']]['type'] in se_types))
            zs = sorted(a['z'] for a in atoms.values())
            zmin, zmax = zs[0], zs[-1]
            zp99 = zs[int(len(zs)*0.99)] if zs else 0
            print(f'    DEBUG: n_atoms={len(atoms)}, n_SE={n_se}, '
                   f'n_SE-SE contacts={n_se_contacts}')
            print(f'           z range: [{zmin:.5f}, {zmax:.5f}], '
                   f'z@99%={zp99:.5f}, plate_z(max)={plate_z:.5f}')
            print(f'           scale={scale}, type_map={type_map}')
        from viewer3d_data import compute_se_network_diagnostics
        diag = compute_se_network_diagnostics(
            contacts, atoms, type_map, plate_z=plate_z, scale=scale,
            verbose=debug)
    except Exception as e:
        print(f'  [{case_id}] SKIP — load/diag fail: {e}')
        return None
    comp = load_composition(case_dir, meta)
    bn = diag.get('bottleneck_edges') or []
    bn_sn = diag.get('bn_stats_norm') or {}
    bn_sa = diag.get('bn_stats_area') or {}
    return {
        'case_id': case_id,
        **comp,                            # campaign is in comp now
        'scale_factor': scale,
        'n_percolating': diag.get('n_percolating', 0),
        'n_perc_edges':  diag.get('n_perc_edges', 0),
        'n_cut':         len(diag.get('articulation_points') or []),
        'n_bn_capped':   len(bn),          # what viewer renders (capped at bn_max)
        # uncapped count of edges below A/r² threshold (true # of narrow contacts)
        'n_bn_below_threshold': diag.get('n_bn_below_threshold', 0),
        # Full-distribution stats over ALL percolating edges (NOT capped) —
        # these are the scientific numbers for cross-case comparison
        'bn_area_min':   bn_sa.get('min_um2'),
        'bn_area_p10':   bn_sa.get('p10_um2'),
        'bn_area_p50':   bn_sa.get('p50_um2'),
        'bn_norm_min':   bn_sn.get('min'),
        'bn_norm_p1':    bn_sn.get('p1'),
        'bn_norm_p5':    bn_sn.get('p5'),
        'bn_norm_p10':   bn_sn.get('p10'),
        'bn_norm_p25':   bn_sn.get('p25'),
        'bn_norm_p50':   bn_sn.get('p50'),
        'bn_norm_p75':   bn_sn.get('p75'),
        'bn_norm_max':   bn_sn.get('max'),
        'bn_median_norm':    diag.get('bn_median_norm', 0),
        'bn_threshold_norm': diag.get('bn_threshold_norm', 0),
        'n_dead_end_clusters': len(diag.get('dead_end_clusters') or []),
        'n_dead_end_top':      sum(1 for d in (diag.get('dead_end_clusters') or [])
                                     if d.get('type') == 'top_only'),
        'n_dead_end_bot':      sum(1 for d in (diag.get('dead_end_clusters') or [])
                                     if d.get('type') == 'bottom_only'),
        'cut_fraction':        round(len(diag.get('articulation_points') or [])
                                       / max(1, diag.get('n_percolating', 0)), 4),
    }


# ────────────────────────────────────────────────────────────────────────
def write_csv(rows: list[dict], out_path: Path):
    if not rows:
        print('No rows to write.'); return
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with out_path.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f'CSV → {out_path}  ({len(rows)} rows)')


# ── 4-panel paper figure ──────────────────────────────────────────────
def make_figure(rows: list[dict], out_path: Path):
    if not rows:
        print('No data for figure.'); return
    R = [r for r in rows if r['n_percolating'] > 0]
    if not R:
        print('No percolating cases — figure skipped.'); return
    phi   = np.array([r['phi_SE']     for r in R])
    lam   = np.array([r['lam_eff']    for r in R])
    f_AM  = np.array([r['am_wt'] / 100 for r in R])
    n_cut = np.array([r['n_cut']      for r in R])
    cutf  = np.array([r['cut_fraction'] for r in R])
    bnmin = np.array([r['bn_area_min'] or np.nan for r in R])
    bnp50 = np.array([r['bn_area_p50'] or np.nan for r in R])
    # Normalized A/r² — scale-invariant
    bnnorm_min = np.array([r['bn_norm_min'] or np.nan for r in R])
    bnnorm_p50 = np.array([r['bn_norm_p50'] or np.nan for r in R])
    bn_med     = np.array([r['bn_median_norm'] or np.nan for r in R])
    # Uncapped count of below-threshold edges (RVE-size-dependent — for
    # cross-case comparison we use the *fraction* below).
    n_bn_below = np.array([r.get('n_bn_below_threshold', 0) or 0 for r in R],
                          dtype=float)
    n_perc     = np.array([r['n_percolating'] for r in R], dtype=float)
    n_perc_e   = np.array([r.get('n_perc_edges', 0) or 0 for r in R], dtype=float)
    # ★ Scale-invariant: fraction of SE-SE edges in percolating subgraph that
    # are below the A/r² threshold.  This removes the RVE-size bias seen in
    # raw counts (e.g. real40 vs baseline have wildly different RVE volumes).
    bn_below_frac = np.where(n_perc_e > 0, n_bn_below / n_perc_e, np.nan)
    # Cut node fraction (per panel c) but also used elsewhere if helpful
    cutf_arr  = np.array([r['cut_fraction'] for r in R])
    camp  = [r['campaign'] for r in R]

    camp_colors = {'particulate': '#d62728', '박막(1mAh)': '#1f77b4',
                   '후막(6mAh)': '#ff7f0e', '후막(8mAh)': '#2ca02c'}
    camp_lab = {'particulate': 'particulate', '박막(1mAh)': 'thin 1mAh',
                '후막(6mAh)': 'thick 6mAh', '후막(8mAh)': 'thick 8mAh'}

    plt = _get_plt()
    fig = plt.figure(figsize=(13, 9))
    gs = fig.add_gridspec(2, 2, hspace=0.32, wspace=0.28,
                          left=0.07, right=0.985, top=0.93, bottom=0.07)

    def scatter(ax, x, y, ylog=False, xlog=False,
                 xlabel='', ylabel='', title=''):
        for c in sorted(set(camp)):
            idx = np.array([i for i, cc in enumerate(camp) if cc == c])
            if len(idx) == 0: continue
            ax.scatter(x[idx], y[idx], c=camp_colors.get(c, '#999'),
                        s=42, edgecolors='black', linewidths=0.5,
                        label=camp_lab.get(c, c))
        # Only set log scale when data has positive values (avoid matplotlib
        # warning on cases where x/y is all zero or NaN)
        if ylog and np.nanmax(y) > 0:
            ax.set_yscale('log')
        if xlog and np.nanmax(x) > 0:
            ax.set_xscale('log')
        ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)
        ax.set_title(title, loc='left')
        ax.grid(alpha=0.25)

    # (a) cut fraction vs φ_SE (scale-invariant — was raw count)
    ax = fig.add_subplot(gs[0, 0])
    scatter(ax, phi, cutf_arr,
            xlabel=r'SE volume fraction  $\phi_{\mathrm{SE}}$',
            ylabel=r'$n_{\mathrm{cut}} / n_{\mathrm{percolating}}$',
            title=r'(a)  Cut fraction vs $\phi_{\mathrm{SE}}$')
    ax.legend(loc='best', fontsize=7.5)

    # (b) Below-threshold bottleneck FRACTION vs φ_SE — RVE-size invariant
    # Previously used raw count which scaled trivially with RVE size
    # (real40 cases have ~50× smaller RVE → ~50× fewer narrow contacts
    # even at identical fragility).  Fraction = scale-invariant.
    ax = fig.add_subplot(gs[0, 1])
    scatter(ax, phi, bn_below_frac, ylog=True,
            xlabel=r'SE volume fraction  $\phi_{\mathrm{SE}}$',
            ylabel=r'$n_{\mathrm{bn}}^{<\!\mathrm{thr}} / n_{\mathrm{perc\,edges}}$',
            title=r'(b)  Below-threshold bottleneck fraction vs $\phi_{\mathrm{SE}}$')

    # (c) cut fraction vs λ_eff (skip log if no positive λ)
    ax = fig.add_subplot(gs[1, 0])
    scatter(ax, lam, cutf, xlog=True,
            xlabel=r'Size ratio  $\lambda_{\mathrm{eff}} = r_{\mathrm{AM,eff}}/r_{\mathrm{SE}}$',
            ylabel=r'$n_{\mathrm{cut}} / n_{\mathrm{percolating}}$',
            title=r'(c)  Cut fraction (network fragility) vs $\lambda_{\mathrm{eff}}$')
    if np.nanmax(lam) > 0:
        ax.set_xticks([2, 3, 5, 7, 10, 15, 20])
        ax.set_xticklabels(['2', '3', '5', '7', '10', '15', '20'])

    # (d) bn median A/r² vs AM weight fraction
    ax = fig.add_subplot(gs[1, 1])
    scatter(ax, f_AM*100, bnnorm_p50, ylog=True,
            xlabel='AM weight fraction (%)',
            ylabel=r'Bottleneck median  $A/r_{\min}^2$',
            title=r'(d)  Bottleneck median  $A/r^2$  vs AM weight fraction')

    fig.suptitle(
        f'SE percolation-risk descriptors across DEM corpus  —  '
        f'{len(R)} percolating cases  '
        f'(cut nodes = topology, bottleneck = transport)',
        fontsize=12, fontweight='bold', y=0.985)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path)
    plt.close(fig)
    print(f'Figure → {out_path}')


# ────────────────────────────────────────────────────────────────────────
def _selftest() -> int:
    """★ L4-06 · L4-07 — **코퍼스가 코퍼스인가**.

    둘 다 *"조용히 줄어드는"* 부류다: 하나는 사례가 사라지고(중복제거), 다른 하나는
    상이 사라진다(메타 병합).  어느 쪽도 오류를 내지 않고, 뒤의 표는 정상으로 보인다.
    ⚠ 대조 없이는 이 검사도 거짓 초록이 된다 — 중복제거를 **아예 꺼도** ①②는 통과한다.
    그래서 ①c 가 *"같은 자료는 여전히 하나로 접힌다"* 를 잡는다.
    """
    import tempfile
    global WEBAPP
    ok = True

    def chk(name, cond, extra=''):
        nonlocal ok
        print(('  ✓ ' if cond else '  ✗ ') + name + (f'   {extra}' if extra else ''))
        ok = ok and bool(cond)

    def _mk(root: Path, nm: str, atoms: str, contacts: str, **files):
        d = root / 'results' / nm
        d.mkdir(parents=True, exist_ok=True)
        (d / 'atoms.csv').write_text(atoms)
        (d / 'contacts.csv').write_text(contacts)
        for fn, obj in files.items():
            (d / f'{fn}.json').write_text(json.dumps(obj))
        return d

    print('SE 진단 코퍼스 계약 (L4-06 · L4-07)')
    _saved = WEBAPP
    try:
        # ── ① L4-06: 크기는 같고 내용은 다른 두 사례 ────────────────────────
        tmp = Path(tempfile.mkdtemp())
        A = ("id,type,radius,x,y,z\n"
             "1,3,0.50,1.0,1.0,1.0\n2,3,0.50,1.0,1.0,2.0\n3,3,0.50,1.0,1.0,3.0\n")
        B = A.replace('1.0,1.0,', '9.0,9.0,')
        CA = "id1,id2,area\n1,2,0.100\n2,3,0.100\n"
        CB = CA.replace('0.100', '0.900')
        chk('① 픽스처가 **바이트 수까지 같다** (옛 키가 못 가르는 조건)',
            len(A) == len(B) and len(CA) == len(CB) and A != B,
            f'atoms {len(A)} B · contacts {len(CA)} B')
        _mk(tmp, 'case_a', A, CA, input_params={'scale': 1000})
        _mk(tmp, 'case_b', B, CB, input_params={'scale': 1000})
        WEBAPP = tmp
        got = sorted(p.name for p in discover_cases())
        chk('①a L4-06: 내용이 다르면 **둘 다 살아남는다** (옛 코드는 하나만; '
            '어느 쪽이 사라지는지는 rglob 순서에 달렸다)',
            got == ['case_a', 'case_b'], str(got))

        # ①b 대조 — 같은 내용은 여전히 하나로 접히고, **이름 있는 쪽**이 이긴다
        tmp2 = Path(tempfile.mkdtemp())
        _mk(tmp2, '260421_213656_78ec86', A, CA, input_params={'scale': 1000})
        _mk(tmp2, 'input_twin', A, CA, input_params={'scale': 1000})
        WEBAPP = tmp2
        got = [p.name for p in discover_cases()]
        chk('①b 대조: **같은 내용**은 하나로 접힌다 (중복제거가 꺼진 것이 아니다)',
            len(got) == 1, str(got))
        chk('①c 대조: 접힐 때 timestamp 가 아니라 **이름 있는 쪽**이 남는다',
            got == ['input_twin'], str(got))

        # ── ② L4-07: input_params 에 scale 만 · meta 에 상 지도 ─────────────
        tmp3 = Path(tempfile.mkdtemp())
        atoms5 = ("id,type,radius,x,y,z\n"
                  + "".join(f"{i},2,0.5,{i}.0,0.0,{i}.0\n" for i in range(1, 6)))
        d = _mk(tmp3, 'mono', atoms5, "id1,id2,area\n1,2,0.1\n",
                input_params={'scale': 1000}, meta={'type_map': '1:AM_P,2:SE'})
        atoms, type_map, scale, meta = load_case(d)
        se_types = {k for k, v in type_map.items() if v == 'SE'}
        n_se = sum(1 for a in atoms.values() if a['type'] in se_types)
        chk('②a L4-07: 두 파일을 **병합**해 meta 의 상 지도를 본다 (옛 코드는 '
            'input_params 를 읽고 break → 3-type 기본 지도)',
            type_map == {1: 'AM_P', 2: 'SE'}, str(type_map))
        chk('②b L4-07: 실제 type2 입자 5개가 **SE 로 센다** (옛 코드는 0개)',
            n_se == 5, f'n_se={n_se}')
        chk('②c 두 파일이 함께 읽힌다 — scale 은 input_params 쪽',
            float(scale) == 1000.0, f'scale={scale}')

        # ②d 대조 — 같은 필드를 다르게 말하면 **거부**
        d2 = _mk(tmp3, 'clash', atoms5, "id1,id2,area\n1,2,0.1\n",
                 input_params={'scale': 1000}, meta={'scale': 2000})
        try:
            load_meta_merged(d2)
            raised = False
        except MetaConflict:
            raised = True
        chk('②d 대조: 같은 필드를 두 파일이 다르게 말하면 **MetaConflict 로 거부** '
            '(한쪽을 조용히 이기게 하지 않는다)', raised)

        # ②e 대조 — 파일이 하나뿐인 흔한 배치는 그대로 동작
        d3 = _mk(tmp3, 'only_meta', atoms5, "id1,id2,area\n1,2,0.1\n",
                 meta={'type_map': '2:SE', 'scale': 500})
        _a, _tm, _sc, _m = load_case(d3)
        chk('②e 대조: meta 하나뿐인 배치도 그대로 읽힌다',
            _tm == {2: 'SE'} and float(_sc) == 500.0, f'{_tm} scale={_sc}')
    finally:
        WEBAPP = _saved

    print('SE 진단 코퍼스 SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--csv-only', action='store_true',
                     help='Only write CSV, skip figure.')
    ap.add_argument('--no-plot', action='store_true',
                     help='Same as --csv-only.')
    ap.add_argument('--debug', nargs='*', default=None,
                     help='Case substrings to print debug info for. '
                          'Empty = no debug. "all" = every case.')
    ap.add_argument('--out-csv', default=str(DATA_DIR / 'se_diagnostics_82.csv'))
    ap.add_argument('--out-fig', default=str(FIG_DIR / 'percolation_risk_scaling.png'))
    args = ap.parse_args()

    cases = discover_cases()
    print(f'Found {len(cases)} candidate case dirs')

    rows = []
    debug_filters = args.debug or []
    for i, case_dir in enumerate(cases):
        want_debug = any(s in case_dir.name for s in debug_filters) \
                     or 'all' in debug_filters
        result = analyze_case(case_dir, debug=want_debug)
        if result is None: continue
        rows.append(result)
        print(f'  [{i+1:>3}/{len(cases)}] {case_dir.name:35s}  '
              f'perc={result["n_percolating"]:>5d}  cut={result["n_cut"]:>4d}  '
              f'bn_min={result["bn_area_min"] if result["bn_area_min"] is not None else "-"}')

    # Summary diagnostics
    n_total = len(rows)
    n_perc  = sum(1 for r in rows if r['n_percolating'] > 0)
    n_with_comp = sum(1 for r in rows if r['lam_eff'] > 0)
    print(f'\nSummary:')
    print(f'  total cases:                 {n_total}')
    print(f'  with percolating SE (>0):    {n_perc}')
    print(f'  with composition (lam>0):    {n_with_comp}')
    print(f'  → figure uses intersection (both)')

    write_csv(rows, Path(args.out_csv))
    if not (args.csv_only or args.no_plot):
        make_figure(rows, Path(args.out_fig))


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(_selftest())
    main()
