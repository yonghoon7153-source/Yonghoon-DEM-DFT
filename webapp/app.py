"""
DEM Analysis Web Application
- Single mode: Upload one case → full analysis pipeline → figures + MD report
- Group mode: Upload multiple cases → comparison plots + summary report
"""
import os
import json
import uuid
import shutil
import subprocess
import glob as globmod
import threading
from datetime import datetime
from pathlib import Path

# Network solver semaphore: only 1 at a time to prevent OOM
_network_solver_lock = threading.Semaphore(1)

# Load .env file if exists (for local development)
_env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(_env_path):
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith('#') and '=' in _line:
                _k, _v = _line.split('=', 1)
                os.environ.setdefault(_k.strip(), _v.strip())

from flask import (
    Flask, render_template, request, jsonify, send_from_directory,
    redirect, url_for, send_file
)
import storage_sync
import predictor_engine

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 * 1024  # 2GB max
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['RESULTS_FOLDER'] = os.path.join(os.path.dirname(__file__), 'results')
app.config['SCRIPTS_FOLDER'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts')
app.config['ARCHIVE_FOLDER'] = os.path.join(os.path.dirname(__file__), 'archive')

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)
os.makedirs(app.config['ARCHIVE_FOLDER'], exist_ok=True)

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'error': '파일 크기가 너무 큽니다. 최대 2GB까지 업로드 가능합니다.'}), 413

# ─── Supabase Storage: restore in background (don't block server start) ───
storage_sync.init()

def _bg_restore():
    storage_sync.restore_all(
        app.config['UPLOAD_FOLDER'],
        app.config['RESULTS_FOLDER'],
        app.config['ARCHIVE_FOLDER'],
    )

_restore_thread = threading.Thread(target=_bg_restore, daemon=True)
_restore_thread.start()

# ─── Helpers ────────────────────────────────────────────────────────────────

def get_case_dir(case_id):
    d = os.path.join(app.config['UPLOAD_FOLDER'], case_id)
    os.makedirs(d, exist_ok=True)
    return d

def get_results_dir(case_id):
    d = os.path.join(app.config['RESULTS_FOLDER'], case_id)
    os.makedirs(d, exist_ok=True)
    return d

def detect_mode(case_dir):
    """Detect if bimodal (3 types) or standard (2 types) from atom file type count."""
    # Count unique atom types from atom dump file (most reliable)
    for f in sorted(os.listdir(case_dir)):
        if f.startswith('atom') and f.endswith('.liggghts'):
            with open(os.path.join(case_dir, f)) as fh:
                lines = fh.readlines()
                types = set()
                in_data = False
                for line in lines:
                    stripped = line.strip()
                    if stripped.startswith('ITEM: ATOMS'):
                        in_data = True
                        continue
                    if stripped.startswith('ITEM:'):
                        in_data = False
                        continue
                    if in_data:
                        parts = stripped.split()
                        if len(parts) >= 2:
                            try:
                                t = int(parts[1])
                                types.add(t)
                            except ValueError:
                                continue
                # 3 types = bimodal (AM_P + AM_S + SE)
                # 2 types = standard (AM + SE)
                if len(types) >= 3:
                    return 'bimodal'
                return 'standard'
    return 'standard'

def list_cases():
    """List all uploaded cases with metadata."""
    cases = []
    upload_dir = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_dir):
        return cases
    for case_id in sorted(os.listdir(upload_dir), reverse=True):
        case_dir = os.path.join(upload_dir, case_id)
        if not os.path.isdir(case_dir):
            continue
        meta_file = os.path.join(case_dir, 'meta.json')
        if os.path.exists(meta_file):
            with open(meta_file) as f:
                meta = json.load(f)
        else:
            meta = {'name': case_id, 'created': '', 'mode': 'unknown', 'status': 'uploaded'}
        meta['id'] = case_id
        # Check for results
        results_dir = os.path.join(app.config['RESULTS_FOLDER'], case_id)
        meta['has_results'] = os.path.isdir(results_dir) and len(os.listdir(results_dir)) > 0
        figures_dir = os.path.join(results_dir, 'figures')
        meta['has_figures'] = os.path.isdir(figures_dir) and len(globmod.glob(os.path.join(figures_dir, '*.png'))) > 0
        report_file = os.path.join(results_dir, 'report.md')
        meta['has_report'] = os.path.exists(report_file)
        # Check for warnings
        metrics_file = os.path.join(results_dir, 'full_metrics.json')
        if os.path.exists(metrics_file):
            with open(metrics_file) as f:
                m = json.load(f)
            meta['warning_count'] = m.get('warning_count', 0)
            meta['warning_msgs'] = [w['msg'] for w in m.get('warnings', [])]
            meta['network_solver_status'] = m.get('network_solver_status', meta.get('network_solver_status', ''))
            # Physics solver state — three explicit values for UI badges:
            #   'mikic' / 'maxwell+film' → upgraded (PHYS ✓, green)
            #   'maxwell' or any legacy tag → PHYS legacy (orange)
            #   missing physics σ → PHYS ∅ (gray)
            phys_model = m.get('physics_resistance_model')
            if phys_model in ('mikic', 'maxwell+film'):
                pass  # upgraded state — keep as-is
            elif phys_model == 'maxwell' or 'sigma_full_mScm_physics' in m:
                phys_model = 'maxwell'
            else:
                phys_model = 'no_physics'
            meta['physics_resistance_model'] = phys_model
            meta['physics_solver_at'] = m.get('physics_solver_at', '')
        cases.append(meta)
    return cases

# Keys mirrored from the physics-mode solution for dual-column display.
# When the dual JSON is present, these are copied with a '_physics' suffix.
_NET_PHYSICS_MIRROR_KEYS = ['sigma_full', 'sigma_full_mScm',
                            'sigma_bulk_net', 'sigma_bulk_net_mScm',
                            'electronic_sigma_full_mScm', 'thermal_sigma_full_mScm',
                            'R_brug_over_full', 'bulk_resistance_fraction']


def _pct_delta(h, p):
    """Format Δ% between Hertzian and physics values. '+X.X%' / '-X.X%' / '0%'."""
    try:
        if h is None or p is None or float(h) == 0:
            return '0%'
        d = (float(p) / float(h) - 1.0) * 100.0
        if abs(d) < 0.05:
            return '0%'
        sign = '+' if d >= 0 else ''
        return f"{sign}{d:.1f}%"
    except Exception:
        return '0%'


def _dual_row(label, h_val, p_val, fmt=None):
    """[label, Hertzian, Physics, Δ%] row. If p_val is None, Physics=Hertzian."""
    if fmt is None:
        fmt = lambda x: x
    h_disp = fmt(h_val) if h_val is not None else '—'
    p_disp = fmt(p_val) if p_val is not None else h_disp
    return [label, h_disp, p_disp, _pct_delta(h_val, p_val)]


def _same_row(label, val):
    """[label, val, val, '0%'] — metric not affected by contact mode."""
    return [label, val, val, '0%']


def build_fracture_summary_table(metrics):
    """Build a 'fracture_summary' table from full_metrics.json keys.

    Returns a {columns, data} dict in the same format as the CSV-derived
    tables, ready to be injected into the analysis-summary tabs in
    single.html. Section-header rows start with '──' so the template
    renders them as full-width separators.

    Two-classifier display: each metric shown in both δ-based (Hertzian-
    equivalent) and force-based (Hooke-correct, model-agnostic) columns.
    Returns None if the case has no AM-AM contacts (empty metrics).
    """
    if not metrics:
        return None
    n_total = metrics.get('n_total_AM_AM') or 0
    n_total_force = metrics.get('n_total_AM_AM_force') or 0
    if n_total == 0 and n_total_force == 0:
        return None

    def f(v, prec=2):
        if v is None or v == '': return '-'
        try:
            return round(float(v), prec)
        except (TypeError, ValueError):
            return v

    rows = []

    # ── Stage distribution (%) ──
    rows.append(['── 단계별 분포 (%) ──'])
    for stage, label in [('intact',        'Intact'),
                          ('microcrack',    'Microcrack'),
                          ('multicrack',    'Multi-crack'),
                          ('fragmentation', 'Fragmentation'),
                          ('pulverization', 'Pulverization')]:
        d = metrics.get(f'frac_{stage}_pct')
        ff = metrics.get(f'frac_{stage}_force_pct')
        rows.append([f'  {label}', f(d), f(ff)])

    # ── Severe summary ──
    rows.append(['── Severe (frag + pulv) ──'])
    sev_d = ((metrics.get('frac_fragmentation_pct') or 0)
             + (metrics.get('frac_pulverization_pct') or 0))
    sev_f = ((metrics.get('frac_fragmentation_force_pct') or 0)
             + (metrics.get('frac_pulverization_force_pct') or 0))
    rows.append(['  Severe %',                       f(sev_d), f(sev_f)])
    rows.append(['  fracture_index (severe/total)',
                 f(metrics.get('fracture_index'),       4),
                 f(metrics.get('fracture_index_force'), 4)])

    # ── Per-pair-type severe % ──
    rows.append(['── Pair-type Severe % ──'])
    for pt in ('AM_P-AM_P', 'AM_P-AM_S', 'AM_S-AM_S'):
        n_pt = metrics.get(f'n_total_{pt}') or 0
        n_pt_force = metrics.get(f'n_total_force_{pt}') or 0
        d_sev = ((metrics.get(f'frac_fragmentation_{pt}_pct') or 0)
                 + (metrics.get(f'frac_pulverization_{pt}_pct') or 0))
        f_sev = ((metrics.get(f'frac_fragmentation_force_{pt}_pct') or 0)
                 + (metrics.get(f'frac_pulverization_force_{pt}_pct') or 0))
        if n_pt == 0 and n_pt_force == 0:
            continue
        rows.append([f'  {pt}', f(d_sev), f(f_sev)])

    # ── Auerbach P_c (mN) — material physics, single value per pair ──
    rows.append(['── Auerbach P_c (mN) ──'])
    for pt in ('AM_P-AM_P', 'AM_S-AM_S', 'AM_P-AM_S'):
        v = metrics.get(f'P_c_mN_median_{pt}')
        if v is None: continue
        rows.append([f'  {pt}', f(v, 3), '-'])

    # ── F_DEM medians (mN, real units) ──
    rows.append(['── F_DEM (mN, real units) ──'])
    for pt in ('AM_P-AM_P', 'AM_S-AM_S', 'AM_P-AM_S'):
        v = metrics.get(f'F_mN_median_{pt}')
        if v is None: continue
        rows.append([f'  {pt}', f(v, 3), '-'])

    # ── F / P_c ratios (key indicator) ──
    rows.append(['── F / P_c ratio ──'])
    for pt in ('AM_P-AM_P', 'AM_S-AM_S', 'AM_P-AM_S'):
        v = metrics.get(f'F_over_Pc_median_{pt}')
        if v is None: continue
        rows.append([f'  {pt}', f(v, 3), '-'])

    # ── Counts ──
    rows.append(['── Contact counts ──'])
    rows.append(['  Total AM-AM contacts',
                 int(n_total)       if n_total       else '-',
                 int(n_total_force) if n_total_force else '-'])

    return {'columns': ['지표', 'δ-based', 'Force-based'], 'data': rows}


def inject_tier1_patch_rows(tables, metrics):
    """Append a 'Tier 1 patches' section to network_summary listing the new
    keys added by the post-Auerbach analysis pipeline:

      Coverage  rough (B3 shape factor)        coverage_AM_*_mean_physics_rough
      SE-SE CN  perc-only         (F2)         se_se_cn_perc
      SE-SE CN  area-weighted     (F2)         se_se_cn_eff_area
      SE-SE CN  perc + area-w     (F2)         se_se_cn_eff_area_perc
      SE-SE CN  plastic-aug       (F1)         se_se_cn_aug (+ n_extra)

    These keys are written automatically by the auto-DB pipeline
    (dem_analysis_core.calc_se_se_cn / calc_coverage with shape factor),
    so every freshly analysed case will populate them. Cases predating
    the Tier 1 patches will leave the keys missing → the rows are
    silently skipped.
    """
    if 'network_summary' not in tables or not metrics:
        return
    data = tables['network_summary']['data']
    if not isinstance(data, list):
        return

    section_label = '── Tier 1 patches (post-Auerbach refinements) ──'
    if any(isinstance(r, list) and r and r[0] == section_label for r in data):
        return  # already injected on a prior call

    rows: list = []
    rows.append([section_label, '', '', ''])

    # Rough coverage (B3 shape factor: AM_P=1.40, AM_S=1.10, SE=1.05)
    for label, key in [
        ('Coverage AM rough(%)   [B3]',   'coverage_AM_mean_physics_rough'),
        ('Coverage AM_P rough(%) [B3]', 'coverage_AM_P_mean_physics_rough'),
        ('Coverage AM_S rough(%) [B3]', 'coverage_AM_S_mean_physics_rough'),
    ]:
        v = metrics.get(key)
        if v is None:
            continue
        try:
            rows.append([label, '-', round(float(v), 2), ''])
        except (TypeError, ValueError):
            pass

    # F2 / F1 CN variants
    cn_specs = [
        ('SE-SE CN (perc-only)        [F2]', 'se_se_cn_perc',          4),
        ('SE-SE CN (area-weighted)    [F2]', 'se_se_cn_eff_area',      4),
        ('SE-SE CN (perc area-w)      [F2]', 'se_se_cn_eff_area_perc', 4),
        ('SE-SE CN (plastic-augmented) [F1]', 'se_se_cn_aug',          3),
    ]
    for label, key, prec in cn_specs:
        v = metrics.get(key)
        if v is None:
            continue
        try:
            rows.append([label, round(float(v), prec), '-', ''])
        except (TypeError, ValueError):
            pass
    n_extra = metrics.get('se_se_cn_aug_n_extra')
    if n_extra is not None:
        try:
            rows.append(['  (F1 extra near-contact pairs)', int(n_extra), '-', ''])
        except (TypeError, ValueError):
            pass

    # Only inject if at least one Tier 1 row populated
    if len(rows) > 1:
        # Place after the existing AM-AM section if present, else at the end
        anchor_idx = len(data)
        for i, r in enumerate(data):
            if (isinstance(r, list) and r and isinstance(r[0], str)
                    and ('AM-AM' in r[0] or '응력' in r[0])):
                anchor_idx = i
                break
        for j, nr in enumerate(rows):
            data.insert(anchor_idx + j, nr)


def transform_network_summary_4col(tables, metrics, meta):
    """Convert network_summary table to 4-column (지표 | Hertzian | Physics | Δ%)
    and inject Network Solver + AM-AM sections from full_metrics.json.

    Shared helper for /single/<case_id> and /archive/view/<folder> routes."""
    if 'network_summary' not in tables:
        return
    tbl = tables['network_summary']

    # Step 1: expand existing rows to 4 cols (default Physics = Hertzian, Δ = 0%)
    tbl['columns'] = ['지표', 'Hertzian (DEM-native)', 'Physics (Tabor+volume)', 'Δ (%)']
    def _is_section_header(label):
        if not isinstance(label, str):
            return False
        s = label.strip()
        return s.startswith('──') or (s.startswith('─') and s.endswith('─'))

    # Rows produced by older analyze_contacts.py runs that we no longer want
    # to render (header + binding format have been redesigned, area rows
    # superseded by per-contact selection % distribution).
    _drop_labels = {
        '─ AM-SE 5-case (Tabor/volume/geom decomposition) ─',
        '── AM-SE 5-case (Tabor/volume/geom decomposition) ──',
        'A_binding (Tabor / vol / geom %)',
        'A_5case ÷ A_final (H / L / T / V / G)',
        'AM-SE A_Hertzian(μm²)',
        'AM-SE A_LIGGGHTS(μm²)',
        'AM-SE A_Tabor(μm²)',
        'AM-SE A_volume(μm²)',
        'AM-SE A_geom(μm²)',
        'AM-SE A_final(μm²)',
    }

    expanded = []
    for row in tbl['data']:
        if not row:
            continue
        label = row[0] if len(row) > 0 else ''
        if isinstance(label, str) and label.strip() in _drop_labels:
            continue
        if _is_section_header(label):
            expanded.append([label, '', '', ''])
        elif len(row) >= 4:
            expanded.append(list(row))  # already 4-col
        else:
            value = row[1] if len(row) > 1 else ''
            expanded.append([label, value, value, '0%'])
    tbl['data'] = expanded
    data = tbl['data']

    # Step 2: section headers if missing
    has_headers = any(isinstance(r[0], str) and r[0].startswith('──') for r in data)
    if not has_headers:
        section_map = {
            'Porosity(%)': '── 구조 ──',
            'AM-SE Total(μm²)': '── 계면 ──',
            'SE-SE CN mean': '── 이온경로: 연결성 ──',
            'Tortuosity mean': '── 이온경로: 경로 효율 ──',
            'Path Hop Area mean(μm²)': '── 이온경로: 경로 품질 ──',
            'Ionic Active AM(%)': '── 활성도 ──',
            'Stress CV(%)': '── 응력 ──',
        }
        new_data = []
        for r in data:
            lbl = str(r[0])
            if lbl in section_map:
                new_data.append([section_map[lbl], '', '', ''])
            new_data.append(r)
        tbl['data'] = new_data
        data = tbl['data']

    # Step 3: populate Physics values for metrics where data exists
    # (coverage metrics get populated by merge_coverage_into_metrics in pipeline)
    def _find_row(label_match):
        for r in data:
            if str(r[0]) == label_match:
                return r
        return None

    if metrics:
        # Interface-area rows that have dual Hertzian/Physics values — both
        # coverage percentages (per AM type) and total contact areas.
        # Each entry maps the UI row label to (hertzian_keys, physics_keys);
        # each key is a tuple of fallbacks so old and new schemas coexist.
        # Physics values are written by scripts/coverage_physics_vs_hertzian.py.
        cov_map = {
            # Coverage (% of AM surface covered by SE contacts)
            'Coverage AM(%)':   (('coverage_AM_mean',   'am_se_coverage_elastic_pct'),
                                 ('coverage_AM_mean_physics',   'am_se_coverage_physics_pct')),
            'Coverage AM_P(%)': (('coverage_AM_P_mean', 'am_p_se_coverage_elastic_pct'),
                                 ('coverage_AM_P_mean_physics', 'am_p_se_coverage_physics_pct')),
            'Coverage AM_S(%)': (('coverage_AM_S_mean', 'am_s_se_coverage_elastic_pct'),
                                 ('coverage_AM_S_mean_physics', 'am_s_se_coverage_physics_pct')),
            # Global interface-area totals (μm²) — linear in A so large Δ
            'AM-SE Total(μm²)': (('area_AM전체_SE_total',),
                                 ('area_AM전체_SE_total_physics',)),
            'SE-SE Total(μm²)': (('area_SE_SE_total',),
                                 ('area_SE_SE_total_physics',)),
            # Percolation-path hop metrics (SE-SE area-dependent)
            'Path Hop Area mean(μm²)': (('path_hop_area_mean',),
                                        ('path_hop_area_mean_physics',)),
            'Path Bottleneck(μm²)':    (('path_hop_area_min_mean',),
                                        ('path_hop_area_min_mean_physics',)),
            'Path Conductance(μm²)':   (('path_conductance_mean',),
                                        ('path_conductance_mean_physics',)),
        }
        def _first_present(keys):
            for k in keys:
                if metrics.get(k) is not None:
                    return metrics.get(k)
            return None
        for row_label, (h_keys, p_keys) in cov_map.items():
            r = _find_row(row_label)
            if r is None:
                continue
            h_val = _first_present(h_keys)
            if h_val is None:
                h_val = r[1]  # keep whatever analyze_contacts already wrote
            p_val = _first_present(p_keys)
            if p_val is not None:
                try:
                    h_num = float(h_val) if not isinstance(h_val, (int, float)) else h_val
                    p_num = float(p_val)
                    # Preserve original Hertzian cell formatting (analyze_contacts
                    # already wrote it with case-appropriate precision). Only
                    # inject the Physics value + Δ% columns. For totals this
                    # keeps 2-decimal precision; for percentages the rounding
                    # tolerance is wide enough.
                    if 'Path Conductance' in row_label:
                        decimals = 5
                    elif 'Path' in row_label:
                        decimals = 4
                    elif '총' in row_label or 'Total' in row_label:
                        decimals = 2
                    else:
                        decimals = 1
                    r[2] = round(p_num, decimals)
                    r[3] = _pct_delta(h_num, p_num)
                except Exception:
                    pass

        # ── Per-contact 5-case binding distribution rows ──
        # film_area_from_overlap labels each contact with the case (one of:
        # hertzian, liggghts, tabor, volume, geom, elastic) that supplied the
        # selected area. coverage_physics_vs_hertzian.py aggregates those
        # labels into A_binding_share_AM_SE_pct (AM-SE only) and
        # A_binding_share_total_pct (every contact pair). We render each as
        # a single row: 'H/L/T/V/G %' formatted string in the Physics column.
        def _fmt_share(share_dict):
            if not isinstance(share_dict, dict):
                return None
            parts = [
                share_dict.get('hertzian', 0.0),
                share_dict.get('liggghts', 0.0),
                share_dict.get('tabor',    0.0),
                share_dict.get('volume',   0.0),
                share_dict.get('geom',     0.0),
            ]
            return ' / '.join(f"{float(p):.1f}" for p in parts)

        def _ensure_row(label, anchor_label, value):
            """Update or insert a row by label, anchored after another row."""
            r = _find_row(label)
            if r is not None:
                r[1] = '-'
                r[2] = value
                r[3] = ''
                return
            anchor_idx = None
            for i, row in enumerate(data):
                if isinstance(row, list) and row and row[0] == anchor_label:
                    anchor_idx = i + 1
                    break
            new_row = [label, '-', value, '']
            if anchor_idx is not None:
                data.insert(anchor_idx, new_row)
            else:
                data.append(new_row)

        amse_share = metrics.get('A_binding_share_AM_SE_pct') if metrics else None
        total_share = metrics.get('A_binding_share_total_pct') if metrics else None
        amse_str  = _fmt_share(amse_share)
        total_str = _fmt_share(total_share)
        # Anchor the binding rows after the SE-SE Total row so they sit at
        # the bottom of the 계면 section — same place the legacy area rows
        # appeared.
        if amse_str is not None:
            _ensure_row('Binding % — AM-SE (H/L/T/V/G)',
                        'SE-SE Total(μm²)', amse_str)
        if total_str is not None:
            _ensure_row('Binding % — Total (H/L/T/V/G)',
                        'Binding % — AM-SE (H/L/T/V/G)', total_str)

    # Step 4: inject Network Solver section (σ rows with physics)
    has_net_section = any(isinstance(r[0], str) and r[0].startswith('── Network Solver') for r in data)
    if not has_net_section:
        insert_idx = len(data)
        for idx, r in enumerate(data):
            if isinstance(r[0], str) and r[0].startswith('── 응력'):
                insert_idx = idx
                break
        net_rows = [['── Network Solver (DEM-native vs Tabor+volume physics) ──', '', '', '']]
        if metrics and metrics.get('sigma_full_mScm'):
            net_rows.append(_dual_row('σ_ionic (mS/cm)',
                                      metrics.get('sigma_full_mScm'),
                                      metrics.get('sigma_full_mScm_physics'),
                                      fmt=lambda x: round(x, 4)))
            if metrics.get('sigma_bruggeman_mScm'):
                v = round(metrics['sigma_bruggeman_mScm'], 4)
                net_rows.append(_same_row('σ_Bruggeman (mS/cm)', v))
            if metrics.get('R_brug_over_full'):
                # R_brug/R_full = σ_Bruggeman / σ_ionic. σ_Bruggeman is mode-
                # agnostic but σ_ionic changes with Physics, so the ratio changes.
                r_h = metrics.get('R_brug_over_full')
                r_p = metrics.get('R_brug_over_full_physics', r_h)
                net_rows.append(_dual_row('Contact-free / Full',
                                          r_h, r_p,
                                          fmt=lambda x: f"{x:.1f}×"))
            if metrics.get('bulk_resistance_fraction') is not None:
                # Constriction % = (1 - bulk_fraction) × 100. bulk_fraction shifts
                # in Physics mode because σ_ionic moves while σ_bulk stays fixed.
                bf_h = metrics.get('bulk_resistance_fraction')
                bf_p = metrics.get('bulk_resistance_fraction_physics', bf_h)
                cstr_h = (1 - bf_h) * 100 if bf_h is not None else None
                cstr_p = (1 - bf_p) * 100 if bf_p is not None else None
                net_rows.append(_dual_row('Constriction 비율(%)',
                                          cstr_h, cstr_p,
                                          fmt=lambda x: round(x, 1)))
            if metrics.get('sigma_ratio') and metrics.get('sigma_full_mScm'):
                sig_brug = 3.0 * metrics['sigma_ratio']
                sig_ion_h = metrics.get('sigma_full_mScm')
                sig_ion_p = metrics.get('sigma_full_mScm_physics') or sig_ion_h
                ratio_h = sig_brug / sig_ion_h if sig_ion_h > 0 else 0
                ratio_p = sig_brug / sig_ion_p if sig_ion_p and sig_ion_p > 0 else ratio_h
                net_rows.append(_dual_row('σ_brug / σ_ionic',
                                          ratio_h, ratio_p,
                                          fmt=lambda x: f"{x:.1f}×"))

            # ── τ 3종 비교 (Dijkstra vs Laplace geom vs Laplace eff) ──
            # Derivation only, no re-analysis needed; uses σ_grain = 3.0 mS/cm (LPSCl bulk).
            import math as _math
            phi_se = metrics.get('phi_se')
            sig_full = metrics.get('sigma_full_mScm')
            sig_bulk = metrics.get('sigma_bulk_net_mScm')
            tau_dij = metrics.get('tortuosity_mean')
            SIGMA_GRAIN_MS = 3.0  # bulk LPSCl [mS/cm]
            if phi_se and sig_full and sig_full > 0:
                # τ_Lap_eff = √(φ_SE × σ_grain / σ_full) ← COMSOL input (GB 포함)
                # σ_full IS mode-dependent, so τ_Lap_eff shifts in Physics mode.
                # τ_Lap_geom uses σ_bulk_net (mode-agnostic) so it stays fixed.
                sig_full_p = metrics.get('sigma_full_mScm_physics')
                tau_lap_eff_h = _math.sqrt(phi_se * SIGMA_GRAIN_MS / sig_full)
                tau_lap_eff_p = (_math.sqrt(phi_se * SIGMA_GRAIN_MS / sig_full_p)
                                 if sig_full_p and sig_full_p > 0 else tau_lap_eff_h)
                tau_lap_geom = (_math.sqrt(phi_se * SIGMA_GRAIN_MS / sig_bulk)
                                if sig_bulk and sig_bulk > 0 else None)
                net_rows.append(['── τ 비교 (Dijkstra vs Laplace, COMSOL input = τ_Lap_eff) ──', '', '', ''])
                if tau_dij:
                    net_rows.append(_same_row('τ_Dij (Dijkstra, 기하만)', round(tau_dij, 2)))
                if tau_lap_geom:
                    net_rows.append(_same_row('τ_Lap_geom (Laplace, GB 제외)', round(tau_lap_geom, 2)))
                net_rows.append(_dual_row('τ_Lap_eff ⭐ (Laplace, GB 포함 — COMSOL/EIS)',
                                          tau_lap_eff_h, tau_lap_eff_p,
                                          fmt=lambda x: round(x, 2)))
                if tau_dij and tau_dij > 0:
                    ratio_h = tau_lap_eff_h / tau_dij
                    ratio_p = tau_lap_eff_p / tau_dij
                    net_rows.append(_dual_row('τ_Lap_eff / τ_Dij',
                                              ratio_h, ratio_p,
                                              fmt=lambda x: f"{x:.2f}×"))

            if metrics.get('electronic_sigma_full_mScm'):
                net_rows.append(_dual_row('σ_electronic (mS/cm)',
                                          metrics.get('electronic_sigma_full_mScm'),
                                          metrics.get('electronic_sigma_full_mScm_physics'),
                                          fmt=lambda x: round(x, 2)))
            if metrics.get('electronic_percolating_fraction') is not None:
                v = f"{metrics['electronic_percolating_fraction']*100:.1f}"
                net_rows.append(_same_row('AM Percolation (%)', v))
            if metrics.get('electronic_active_fraction') is not None:
                v = f"{metrics['electronic_active_fraction']*100:.1f}"
                net_rows.append(_same_row('Electronic Active AM (%)', v))
            if metrics.get('thermal_sigma_full_mScm'):
                net_rows.append(_dual_row('σ_thermal (mS/cm equiv)',
                                          metrics.get('thermal_sigma_full_mScm'),
                                          metrics.get('thermal_sigma_full_mScm_physics'),
                                          fmt=lambda x: round(x, 3)))
        else:
            ns = (meta or {}).get('network_solver_status', 'unknown')
            ns_err = (meta or {}).get('network_solver_error', '')
            if ns in ('failed', 'error', 'timeout', 'no_input', 'no_output'):
                net_rows.append(_same_row('상태', f"❌ {ns}"))
                if ns_err:
                    net_rows.append(_same_row('에러', ns_err[:200]))
            elif ns == 'running':
                net_rows.append(_same_row('상태', '⏳ 실행중...'))
            elif ns == 'waiting':
                net_rows.append(_same_row('상태', '⏳ 대기중'))
            elif ns == 'not_run':
                net_rows.append(_same_row('상태', '미실행'))
            else:
                ms = metrics.get('network_solver_status', '') if metrics else ''
                net_rows.append(_same_row('상태', f"{ms or ns or '결과 없음'}"))
        for i, r in enumerate(net_rows):
            data.insert(insert_idx + i, r)

    # Step 5: inject AM-AM contact mechanics section (invariant under contact_mode)
    has_am_am = any(isinstance(r[0], str) and r[0].startswith('── AM-AM 접촉 역학') for r in data)
    if not has_am_am and metrics:
        am_insert_idx = len(data)
        for idx, r in enumerate(data):
            if isinstance(r[0], str) and r[0].startswith('── 응력'):
                am_insert_idx = idx
                break
        am_rows = [['── AM-AM 접촉 역학 ──', '', '', '']]
        if metrics.get('am_am_cn') is not None:
            am_rows.append(_same_row('AM-AM CN mean', round(metrics['am_am_cn'], 2)))
        if metrics.get('am_am_n_contacts') is not None:
            am_rows.append(_same_row('AM-AM 접촉 수', metrics['am_am_n_contacts']))
        if metrics.get('am_am_mean_contact_radius') is not None:
            am_rows.append(_same_row('접촉 반경(µm)', round(metrics['am_am_mean_contact_radius'], 4)))
        if metrics.get('am_am_mean_delta') is not None:
            am_rows.append(_same_row('침투 깊이 δ(µm)', round(metrics['am_am_mean_delta'], 4)))
        if metrics.get('am_am_mean_force') is not None:
            am_rows.append(_same_row('법선력(µN)', round(metrics['am_am_mean_force'], 2)))
        if metrics.get('am_am_mean_pressure') is not None:
            am_rows.append(_same_row('접촉 압력(MPa)', round(metrics['am_am_mean_pressure'], 1)))
        if metrics.get('am_am_mean_hop') is not None:
            am_rows.append(_same_row('Hop 거리(µm)', round(metrics['am_am_mean_hop'], 2)))
        if len(am_rows) > 1:
            for i, r in enumerate(am_rows):
                data.insert(am_insert_idx + i, r)


def _merge_dual_into_metrics(results_dir, met_data):
    """If network_conductivity_dual.json exists (contact-mode=both run),
    copy physics-mode fields into met_data with '_physics' suffix, plus
    a compact nested 'network_dual' block for webapp display."""
    dual_path = os.path.join(results_dir, 'network_conductivity_dual.json')
    if not os.path.exists(dual_path):
        return met_data
    try:
        with open(dual_path) as _df:
            dual = json.load(_df)
    except Exception:
        return met_data
    rH = dual.get('hertzian') or {}
    rP = dual.get('physics') or {}
    ratio = dual.get('ratio_physics_over_hertzian') or {}
    for k in _NET_PHYSICS_MIRROR_KEYS:
        if rP.get(k) is not None:
            met_data[f'{k}_physics'] = rP[k]
    met_data['network_dual'] = {
        'hertzian': {k: rH.get(k) for k in _NET_PHYSICS_MIRROR_KEYS},
        'physics':  {k: rP.get(k) for k in _NET_PHYSICS_MIRROR_KEYS},
        'ratio_physics_over_hertzian': ratio,
    }
    # Stamp the Physics resistance model + timestamp so every caller (batch,
    # per-case retry, archive reanalyze) propagates the same state to the UI.
    phys_model = rP.get('resistance_model')
    if phys_model:
        met_data['physics_resistance_model'] = phys_model
        met_data['physics_solver_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return met_data


def _refresh_post_network_warnings(met_data):
    """Refresh metrics['warnings'] for checks that depend on fields populated
    by the network solver (electronic_active_fraction etc.). Called AFTER
    network_conductivity.json is merged into full_metrics.json.

    Preserves any existing warnings that were emitted by analyze_contacts.py
    (keyed by 'type' to avoid duplicates) and appends network-dependent ones.

    Respects met_data.disabled_warnings — entries whose type is in that list
    are filtered out.
    """
    existing = list(met_data.get('warnings') or [])
    known_types = {w.get('type') for w in existing if isinstance(w, dict)}
    disabled = set(met_data.get('disabled_warnings') or [])

    new_warnings = []

    def _add(tag, severity, msg):
        if tag not in known_types:
            new_warnings.append({'type': tag, 'severity': severity, 'msg': msg})

    # ─── Electronic Active AM (AM-AM percolation, from network solver) ───
    el_active = met_data.get('electronic_active_fraction')
    if el_active is not None:
        el_pct = el_active * 100
        if el_pct < 10:
            _add('electronic_dead', 'critical',
                 f"Electronic Active AM={el_pct:.0f}% (<10%): 도전재 필수! AM-AM percolation 없음")
        elif el_pct < 50:
            _add('electronic_low', 'critical',
                 f"Electronic Active AM={el_pct:.0f}% (<50%): 대량 dead AM, 도전재 강력 권장")
        elif el_pct < 80:
            _add('electronic_marginal', 'warning',
                 f"Electronic Active AM={el_pct:.0f}% (<80%): 일부 dead AM, 도전재 권장")

    # ─── σ_ionic (ionic conductivity from network solver) ───
    sig = met_data.get('sigma_full_mScm')
    if sig is not None:
        if sig < 0.005:
            _add('sigma_ionic_too_low', 'critical',
                 f"σ_ionic={sig*1000:.2f} μS/cm (<5 μS/cm): 네트워크 거의 비전도 — 병목 극단 또는 솔버 이상")
        elif sig < 0.03:
            _add('sigma_ionic_low', 'warning',
                 f"σ_ionic={sig:.3f} mS/cm (<0.03): 낮은 이온전도도 — bottleneck regime 의심")

    # ─── τ_Lap_eff (effective tortuosity from network solver) ───
    tau_le = met_data.get('tortuosity_lap_eff') or met_data.get('tau_lap_eff')
    if tau_le is not None:
        if tau_le > 15:
            _add('tau_lap_eff_extreme', 'critical',
                 f"τ_Lap_eff={tau_le:.1f} (>15): 극단 bottleneck regime, Wang 70% CAM 레짐 상당")
        elif tau_le > 8:
            _add('tau_lap_eff_high', 'warning',
                 f"τ_Lap_eff={tau_le:.1f} (>8): bottleneck regime, scaling law ±20% 범위 밖 가능성")

    # ─── Constriction dominance ───
    cstr = met_data.get('constriction_pct') or met_data.get('constriction_fraction_pct')
    if cstr is not None:
        if cstr > 90:
            _add('constriction_dominant', 'warning',
                 f"Constriction 비율={cstr:.0f}% (>90%): 접촉 저항이 bulk 저항을 10배 이상 지배")

    # ─── τ_Lap_eff / τ_Dij gap (geometric vs effective divergence) ───
    tau_dij = met_data.get('tortuosity_mean') or met_data.get('tau_dij')
    if tau_le is not None and tau_dij is not None and tau_dij > 0:
        ratio = tau_le / tau_dij
        if ratio > 10:
            _add('tau_ratio_extreme', 'warning',
                 f"τ_Lap_eff/τ_Dij={ratio:.1f}× (>10×): 기하 경로와 실제 전도도 경로 완전 분리")

    # ─── Physics vs Hertzian divergence (sensitivity sanity) ───
    sig_h = met_data.get('sigma_full_mScm')
    sig_p = met_data.get('sigma_full_mScm_physics')
    if sig_h and sig_p and sig_h > 0:
        rel = abs(sig_p - sig_h) / sig_h
        if rel > 0.5:
            _add('physics_hertzian_divergence', 'warning',
                 f"Physics σ / Hertzian σ = {sig_p/sig_h:.2f}× (|Δ|>50%): "
                 "접촉 모델 민감도 큼 — upper bound 해석 권장")

    # ─── Porosity range (post-compaction physicality) ───
    poro = met_data.get('porosity')
    if poro is not None:
        if poro < 8:
            _add('porosity_too_low', 'critical',
                 f"Porosity={poro:.1f}% (<8%): 과압축 — 물리적 한계 근접")
        elif poro > 30:
            _add('porosity_too_high', 'warning',
                 f"Porosity={poro:.1f}% (>30%): 압축 미완료 — DEM settling 재확인")

    merged = [w for w in (existing + new_warnings) if w.get('type') not in disabled]
    if merged:
        met_data['warnings'] = merged
        met_data['warning_count'] = len(merged)
    else:
        met_data['warnings'] = []
        met_data['warning_count'] = 0
    return met_data


def run_pipeline(case_id, mode, type_map, scale=1000):
    """Run the DEM analysis pipeline for a case."""
    # Clear pyc cache to ensure latest code runs
    import glob as globmod
    scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
    for pyc in globmod.glob(os.path.join(scripts_dir, '__pycache__', '*.pyc')):
        os.remove(pyc)

    case_dir = get_case_dir(case_id)
    results_dir = get_results_dir(case_id)
    figures_dir = os.path.join(results_dir, 'figures')
    os.makedirs(figures_dir, exist_ok=True)
    scripts = app.config['SCRIPTS_FOLDER']

    # Find atom, contact, mesh, and input files
    atom_files = sorted(globmod.glob(os.path.join(case_dir, 'atom_*.liggghts')))
    contact_files = sorted(globmod.glob(os.path.join(case_dir, 'contact_*.liggghts')))
    mesh_files = sorted(globmod.glob(os.path.join(case_dir, '*.stl')))
    input_files = sorted(globmod.glob(os.path.join(case_dir, 'input*.liggghts')))

    # Pre-parsed CSV fallback: webapp/uploads may have only atoms.csv/contacts.csv
    # (archive-migrated cases retain CSVs but not original LIGGGHTS dumps).
    pre_atoms_csv = os.path.join(case_dir, 'atoms.csv')
    pre_contacts_csv = os.path.join(case_dir, 'contacts.csv')
    pre_mesh_info = os.path.join(case_dir, 'mesh_info.json')
    has_pre_parsed = os.path.exists(pre_atoms_csv) and os.path.exists(pre_contacts_csv)
    has_pre_atoms_only = os.path.exists(pre_atoms_csv) and not os.path.exists(pre_contacts_csv)

    # HYBRID mode: atoms.csv (no atom_*.liggghts) + contact_*.liggghts.
    # User lost the atom dump but still has the pre-parsed atoms.csv and
    # raw contact dump. Copy atoms.csv in first so parse_liggghts knows to
    # skip atom parsing, then proceed to the normal full pipeline below.
    if (has_pre_atoms_only and contact_files) and not atom_files:
        import shutil as _sh
        _sh.copy2(pre_atoms_csv, os.path.join(results_dir, 'atoms.csv'))
        print(f"  [Hybrid] Copied pre-existing atoms.csv; will parse contacts from LIGGGHTS")

    if not atom_files or not contact_files:
        if not has_pre_parsed:
            # ATOMS-ONLY mode: if atom_*.liggghts exists but no contacts,
            # parse atoms alone and return — webapp will still serve 3D viewer.
            if atom_files and not contact_files:
                log = []
                cmd = ['python3', os.path.join(scripts, 'parse_liggghts.py')]
                cmd += atom_files + mesh_files + input_files + ['-o', results_dir]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                log.append({'step': 'Parse (atoms only)', 'stdout': result.stdout,
                            'stderr': result.stderr, 'rc': result.returncode})
                if result.returncode != 0:
                    return {'error': f'Atoms parse failed: {result.stderr}', 'log': log}
                # Minimal full_metrics so UI doesn't explode
                atoms_only_meta = {
                    'mode_note': 'atoms_only — 3D viewer enabled, contact-based metrics skipped',
                    'has_contacts': False,
                }
                fm_path = os.path.join(results_dir, 'full_metrics.json')
                with open(fm_path, 'w') as f:
                    json.dump(atoms_only_meta, f, indent=2)
                return {'success': True, 'log': log, 'atoms_only': True}
            # Hybrid mode falls through to the full pipeline below — atoms.csv
            # is already in results_dir, and parse_liggghts will skip atom parsing.
            if has_pre_atoms_only and contact_files:
                pass
            # ATOMS-ONLY CSV mode: user uploaded atoms.csv only (LIGGGHTS dump
            # was deleted). Copy CSV into results_dir so 3D viewer works.
            elif has_pre_atoms_only:
                import shutil as _sh
                log = []
                _sh.copy2(pre_atoms_csv, os.path.join(results_dir, 'atoms.csv'))
                if os.path.exists(pre_mesh_info):
                    _sh.copy2(pre_mesh_info, os.path.join(results_dir, 'mesh_info.json'))
                log.append({'step': 'Parse (atoms.csv only)', 'stdout':
                            'atoms.csv copied from case_dir (no contacts)',
                            'stderr': '', 'rc': 0})
                atoms_only_meta = {
                    'mode_note': 'atoms_only_csv — 3D viewer enabled, contact-based metrics skipped',
                    'has_contacts': False,
                }
                fm_path = os.path.join(results_dir, 'full_metrics.json')
                with open(fm_path, 'w') as f:
                    json.dump(atoms_only_meta, f, indent=2)
                return {'success': True, 'log': log, 'atoms_only': True}
            else:
                return {'error': 'atom_*.liggghts 또는 contact_*.liggghts 파일을 찾을 수 없습니다 (CSV fallback도 없음).'}

    log = []

    # Step 1: Parse (atom + contact + mesh) — skip if CSV already exists
    atoms_csv = os.path.join(results_dir, 'atoms.csv')
    contacts_csv = os.path.join(results_dir, 'contacts.csv')

    if atom_files and contact_files:
        # Normal path: parse LIGGGHTS dumps
        cmd = ['python3', os.path.join(scripts, 'parse_liggghts.py')]
        cmd += atom_files + contact_files + mesh_files + input_files + ['-o', results_dir]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        log.append({'step': 'Parse', 'stdout': result.stdout, 'stderr': result.stderr, 'rc': result.returncode})
        if result.returncode != 0:
            return {'error': f'Parse failed: {result.stderr}', 'log': log}
    elif has_pre_atoms_only and contact_files:
        # Hybrid: atoms.csv (pre-copied into results_dir above) + contact_*.liggghts.
        # parse_liggghts detects the existing atoms.csv and skips atom parsing.
        cmd = ['python3', os.path.join(scripts, 'parse_liggghts.py')]
        cmd += contact_files + mesh_files + input_files + ['-o', results_dir]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        log.append({'step': 'Parse (hybrid: atoms.csv + contact LIGGGHTS)',
                    'stdout': result.stdout, 'stderr': result.stderr, 'rc': result.returncode})
        if result.returncode != 0:
            return {'error': f'Hybrid parse failed: {result.stderr}', 'log': log}
    else:
        # CSV fallback: copy pre-parsed CSVs into results_dir
        import shutil as _sh
        _sh.copy2(pre_atoms_csv, atoms_csv)
        _sh.copy2(pre_contacts_csv, contacts_csv)
        if os.path.exists(pre_mesh_info):
            _sh.copy2(pre_mesh_info, os.path.join(results_dir, 'mesh_info.json'))
        log.append({'step': 'Parse (CSV fallback)', 'stdout': 'CSVs copied from case_dir', 'stderr': '', 'rc': 0})

    if mode == 'bimodal':
        # Step 2: Bimodal contact analysis
        cmd = ['python3', os.path.join(scripts, 'analyze_contacts_bimodal.py'),
               atoms_csv, contacts_csv, '-o', results_dir,
               '-t', type_map, '-s', str(scale)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        log.append({'step': 'Bimodal Contact Analysis', 'stdout': result.stdout, 'stderr': result.stderr, 'rc': result.returncode})

        # Step 2b: Dual-mode coverage + AM-SE/SE-SE totals (Hertzian vs Physics).
        # Writes coverage_AM_*_mean_physics, area_AM전체_SE_total_physics,
        # area_SE_SE_total_physics into full_metrics.json + coverage_per_am.csv.
        cmd = ['python3', os.path.join(scripts, 'coverage_physics_vs_hertzian.py'), case_id]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        log.append({'step': 'Coverage Physics vs Hertzian', 'stdout': result.stdout,
                    'stderr': result.stderr, 'rc': result.returncode})

        # Step 3: Basic figures
        cmd = ['python3', os.path.join(scripts, 'generate_figures_bimodal.py'),
               results_dir, '-o', figures_dir, '-s', str(scale)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        log.append({'step': 'Basic Figures', 'stdout': result.stdout, 'stderr': result.stderr, 'rc': result.returncode})

        # Step 4: Advanced
        atoms_analyzed = os.path.join(results_dir, 'atoms_analyzed.csv')
        contacts_analyzed = os.path.join(results_dir, 'contacts_analyzed.csv')
        cmd = ['python3', os.path.join(scripts, 'advanced_analysis_bimodal.py'),
               atoms_analyzed, contacts_analyzed, '-o', results_dir, '-s', str(scale)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        log.append({'step': 'Advanced Analysis', 'stdout': result.stdout, 'stderr': result.stderr, 'rc': result.returncode})

        cmd = ['python3', os.path.join(scripts, 'generate_advanced_figures_bimodal.py'),
               results_dir, '-o', figures_dir, '-s', str(scale)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        log.append({'step': 'Advanced Figures', 'stdout': result.stdout, 'stderr': result.stderr, 'rc': result.returncode})

        # Step 5: Bimodal specific
        cmd = ['python3', os.path.join(scripts, 'bimodal_specific_analysis.py'),
               atoms_analyzed, contacts_analyzed, '-o', results_dir, '-s', str(scale)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        log.append({'step': 'Bimodal Specific', 'stdout': result.stdout, 'stderr': result.stderr, 'rc': result.returncode})

    else:
        # Standard mode
        cmd = ['python3', os.path.join(scripts, 'analyze_contacts.py'),
               atoms_csv, contacts_csv, '-o', results_dir,
               '-t', type_map, '-s', str(scale)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        log.append({'step': 'Contact Analysis', 'stdout': result.stdout, 'stderr': result.stderr, 'rc': result.returncode})

        # Dual-mode coverage + AM-SE/SE-SE totals (Hertzian vs Physics).
        # Populates *_mean_physics and area_*_total_physics keys in
        # full_metrics.json + coverage_per_am.csv (COMSOL-ready).
        cmd = ['python3', os.path.join(scripts, 'coverage_physics_vs_hertzian.py'), case_id]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        log.append({'step': 'Coverage Physics vs Hertzian', 'stdout': result.stdout,
                    'stderr': result.stderr, 'rc': result.returncode})

        cmd = ['python3', os.path.join(scripts, 'generate_figures.py'),
               results_dir, '-o', figures_dir, '-s', str(scale)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        log.append({'step': 'Basic Figures', 'stdout': result.stdout, 'stderr': result.stderr, 'rc': result.returncode})

        atoms_analyzed = os.path.join(results_dir, 'atoms_analyzed.csv')
        contacts_analyzed = os.path.join(results_dir, 'contacts_analyzed.csv')

        cmd = ['python3', os.path.join(scripts, 'advanced_analysis.py'),
               atoms_analyzed, contacts_analyzed, '-o', results_dir, '-s', str(scale)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        log.append({'step': 'Advanced Analysis', 'stdout': result.stdout, 'stderr': result.stderr, 'rc': result.returncode})

        cmd = ['python3', os.path.join(scripts, 'generate_advanced_figures.py'),
               results_dir, '-o', figures_dir, '-s', str(scale)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        log.append({'step': 'Advanced Figures', 'stdout': result.stdout, 'stderr': result.stderr, 'rc': result.returncode})

    # ── Auto-DB hook ─────────────────────────────────────────────────────
    # Trigger an incremental rebuild of docs/db/metrics_master.csv so the
    # new case (and its fracture-stage data emitted by analyze_contacts.py
    # under the 'fracture' results block) lands in the master table without
    # any manual run. Background Popen — does not block the upload UI.
    # Incremental mode reuses unchanged cases via the mtime cache, so the
    # actual work is bounded by the new/changed full_metrics.json files
    # (typically a few seconds for one case).
    try:
        subprocess.Popen(
            ['python3', os.path.join(scripts, 'build_metrics_db.py')],
            cwd=os.path.dirname(scripts),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        log.append({'step': 'Auto-DB Rebuild (background)',
                    'stdout': 'incremental build_metrics_db dispatched',
                    'stderr': '', 'rc': 0})
    except Exception as e:
        log.append({'step': 'Auto-DB Rebuild (background)',
                    'stdout': '', 'stderr': str(e), 'rc': 1})

    return {'success': True, 'log': log}

def generate_report(case_id, case_name='', notes=''):
    """Generate markdown report from analysis results."""
    results_dir = get_results_dir(case_id)
    figures_dir = os.path.join(results_dir, 'figures')

    now = datetime.now().strftime('%y%m%d')
    title = case_name or case_id

    lines = []
    lines.append(f'# {now}_{title}_DEM_Analysis\n')
    lines.append(f'> **날짜**: {datetime.now().strftime("%Y-%m-%d")}')
    lines.append(f'> **케이스**: {title}')
    if notes:
        lines.append(f'> **메모**: {notes}')
    lines.append('')
    lines.append('---\n')

    # Load summary CSV if exists
    summary_file = os.path.join(results_dir, 'contact_summary.csv')
    if os.path.exists(summary_file):
        import pandas as pd
        df = pd.read_csv(summary_file)
        lines.append('## 1. Contact Summary\n')
        lines.append(df.to_markdown(index=False))
        lines.append('')

    # Load atom stats
    atom_stats = os.path.join(results_dir, 'atom_statistics.csv')
    if os.path.exists(atom_stats):
        import pandas as pd
        df = pd.read_csv(atom_stats)
        lines.append('## 2. Particle Statistics\n')
        lines.append(df.to_markdown(index=False))
        lines.append('')

    # Figures
    if os.path.isdir(figures_dir):
        pngs = sorted(globmod.glob(os.path.join(figures_dir, '*.png')))
        if pngs:
            lines.append('## 3. Generated Figures\n')
            for png in pngs:
                fname = os.path.basename(png)
                lines.append(f'### {fname}\n')
                lines.append(f'![{fname}](figures/{fname})\n')

    # Tags
    lines.append('---\n')
    lines.append('#DEM #analysis #ASSB #composite-cathode\n')

    report = '\n'.join(lines)
    report_path = os.path.join(results_dir, 'report.md')
    with open(report_path, 'w') as f:
        f.write(report)
    return report

# ─── Claude AI Analysis ────────────────────────────────────────────────────

def _generate_ai_analysis(all_metrics, case_names, title, notes):
    """Use Claude API to generate deep analysis of comparison data."""
    api_key = os.environ.get('ANTHROPIC_API_KEY', '')
    if not api_key:
        return None

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
    except ImportError:
        return None
    except Exception:
        return None

    # Build data summary for Claude
    import pandas as pd
    display_keys = [
        ('P:S', 'ps_ratio'), ('Porosity(%)', 'porosity'),
        ('Thickness(μm)', 'thickness_um'),
        ('AM-SE Total(μm²)', 'area_AM전체_SE_total'),
        ('SE-SE Total(μm²)', 'area_SE_SE_total'),
        ('SE-SE N', 'area_SE_SE_n'),
        ('SE-SE Mean Area(μm²)', 'area_SE_SE_mean'),
        ('SE-SE CN', 'se_se_cn'),
        ('SE-SE CN std', 'se_se_cn_std'),
        ('SE Cluster', 'n_components'),
        ('Percolation(%)', 'percolation_pct'),
        ('Top Reachable(%)', 'top_reachable_pct'),
        ('Tortuosity', 'tortuosity_mean'),
        ('Ionic Active AM(%)', 'ionic_active_pct'),
        ('Coverage AM_P(%)', 'coverage_AM_P_mean'),
        ('Coverage AM_S(%)', 'coverage_AM_S_mean'),
    ]
    rows = []
    for i, name in enumerate(case_names):
        row = {'Case': name}
        for label, key in display_keys:
            val = all_metrics[i].get(key, '-')
            if isinstance(val, float):
                val = round(val, 2)
            row[label] = val
        rows.append(row)
    df = pd.DataFrame(rows)
    data_table = df.to_markdown(index=False)

    prompt = f"""당신은 고체전지 복합양극 DEM 시뮬레이션 전문가입니다.
아래는 bimodal AM (AM_P: 대립자 6μm, AM_S: 소립자 2μm) + SE (고체전해질) 복합 양극의 DEM 분석 비교 데이터입니다.

제목: {title}
{f'메모: {notes}' if notes else ''}

## 데이터

{data_table}

## 분석 원칙 (반드시 준수)

1. **자의적 가중치 사용 금지**: "종합 점수"를 만들 때 근거 없는 가중치(예: 0.4/0.6)를 부여하지 마세요.
2. **물리적 근거 기반 판단**: 각 주장에는 반드시 물리적 메커니즘 설명이 필요합니다.
3. **Percolation 포화 효과**: 95% 이상에서는 diminishing return. 93%→97% 차이보다 tortuosity 차이가 실제 성능에 더 큰 영향.
4. **병목 결정 원칙**: 고체전지에서는 일반적으로 ionic transport이 charge transfer보다 훨씬 큰 저항. AM-SE 계면이 "충분"하면 SE 네트워크 효율(tortuosity↓)이 핵심.
5. **데이터에 없는 값을 추정하지 마세요**: 주어진 수치만으로 분석.
6. **핵심 지표 우선순위**: Tortuosity > SE-SE Total Area > Percolation > Porosity > AM-SE Total (ionic transport limited 시스템 기준)

## 분석 내용 (한국어)

### 1. 핵심 발견
- AM_P 비율 변화에 따른 주요 경향 3-5개
- 각 경향의 물리적 원인 (입자 크기, 공간 배치 관점)

### 2. SE Contact Network Trade-off
- SE-SE 접촉 개수 vs 평균 면적의 trade-off 관계
- Total Area = N × Mean → 최적점 분석
- 직관적 비유 활용

### 3. AM-SE vs SE-SE 상위 Trade-off
- AM-SE 계면 (charge transfer) vs SE 네트워크 (ionic transport)
- 어느 쪽이 실제 병목인지 데이터 기반으로 판단
- 최적 P:S 비율 제안 (근거 명시)

### 4. 결론 및 제언
- 종합 최적 조건과 그 이유
- 주의사항, 추가 검증 필요 사항

마크다운 형식으로, 표/수치를 적극 활용하되 근거 없는 수치 생성은 금지."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    except Exception as e:
        return f"*AI 분석 생성 실패: {str(e)}*"


# ─── Routes ─────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    cases = list_cases()
    return render_template('index.html', cases=cases)

@app.route('/upload', methods=['POST'])
def upload():
    """Upload files for a new case."""
    case_name = request.form.get('case_name', '').strip()
    mode = request.form.get('mode', 'auto')
    type_map = request.form.get('type_map', '')
    ps_ratio = request.form.get('ps_ratio', '').strip()
    scale = request.form.get('scale', '1000')

    case_id = datetime.now().strftime('%y%m%d_%H%M%S') + '_' + str(uuid.uuid4())[:6]
    case_dir = get_case_dir(case_id)

    files = request.files.getlist('files')
    if not files:
        return jsonify({'error': '파일을 선택해주세요.'}), 400

    filenames = []
    for f in files:
        if f.filename:
            safe_name = f.filename.replace('/', '_').replace('\\', '_')
            f.save(os.path.join(case_dir, safe_name))
            filenames.append(safe_name)

    # Detect mode
    if mode == 'auto':
        mode = detect_mode(case_dir)

    # Default type maps
    if not type_map:
        if mode == 'bimodal':
            type_map = '1:AM_P,2:AM_S,3:SE'
        else:
            # Standard: detect AM_P vs AM_S from radius in atom file
            am_type_name = 'AM_S'  # default: small AM
            for f in sorted(os.listdir(case_dir)):
                if f.startswith('atom') and f.endswith('.liggghts'):
                    with open(os.path.join(case_dir, f)) as fh:
                        in_data = False
                        for line in fh:
                            stripped = line.strip()
                            if stripped.startswith('ITEM: ATOMS'):
                                in_data = True
                                continue
                            if stripped.startswith('ITEM:'):
                                in_data = False
                                continue
                            if in_data:
                                parts = stripped.split()
                                if len(parts) >= 6:
                                    try:
                                        t = int(parts[1])
                                        r = float(parts[5])
                                        if t == 1:
                                            # sim r > 0.004 → AM_P (6μm), else AM_S (2μm)
                                            am_type_name = 'AM_P' if r > 0.004 else 'AM_S'
                                            break
                                    except (ValueError, IndexError):
                                        continue
                    break
            type_map = f'1:{am_type_name},2:SE'

    meta = {
        'name': case_name or case_id,
        'created': datetime.now().isoformat(),
        'mode': mode,
        'type_map': type_map,
        'ps_ratio': ps_ratio,
        'scale': int(scale),
        'files': filenames,
        'status': 'uploaded'
    }
    with open(os.path.join(case_dir, 'meta.json'), 'w') as f:
        json.dump(meta, f, indent=2)

    # Sync to Supabase
    storage_sync.sync_dir_to_remote(case_dir, f'uploads/{case_id}')

    return jsonify({'case_id': case_id, 'mode': mode, 'files': filenames})

@app.route('/analyze/<case_id>', methods=['POST'])
def analyze(case_id):
    """Run analysis pipeline for a case (background thread).

    Optional POST body: {"force_network": true}  → skips the network-result
    backup/restore dance, forcing the solver to re-run from scratch. Use
    this after solver algorithm updates (e.g. 3-stage CG/ILU/spsolve fix)
    to refresh σ values on cases that were previously solved with the old
    code path.
    """
    case_dir = get_case_dir(case_id)
    meta_file = os.path.join(case_dir, 'meta.json')
    if not os.path.exists(meta_file):
        return jsonify({'error': '케이스를 찾을 수 없습니다.'}), 404

    _req = request.get_json(silent=True) or {}
    force_network = bool(_req.get('force_network', False))

    with open(meta_file) as f:
        meta = json.load(f)

    meta['status'] = 'running'
    with open(meta_file, 'w') as f:
        json.dump(meta, f, indent=2)

    _NET_MERGE_KEYS = ['sigma_full', 'sigma_full_mScm', 'sigma_bulk_net',
                      'sigma_bulk_net_mScm', 'R_brug_over_full', 'bulk_resistance_fraction',
                      'electronic_sigma_full_mScm', 'electronic_R_brug',
                      'electronic_active_fraction', 'electronic_percolating_fraction',
                      'thermal_sigma_full_mScm', 'thermal_R_brug',
                      'sigma_bruggeman', 'sigma_bruggeman_mScm', 'R_bruggeman_over_full']

    def _run():
        results_dir = get_results_dir(case_id)
        net_json_path = os.path.join(results_dir, 'network_conductivity.json')

        # ── Step 1: Backup network results before clearing ──
        #   Skipped when force_network=True so the solver is forced to re-run
        #   with the current code (e.g. after 3-stage CG/ILU/spsolve fix).
        #
        #   BUG FIX (this commit): previously only network_conductivity.json was
        #   backed up → every non-force reanalyze silently wiped the dual
        #   results (*_dual.json, *_physics.json, raw edge/node dumps) causing
        #   the Physics column to disappear from the UI. Now the entire set of
        #   network-solver artefacts is snapshotted and restored.
        import tempfile
        _net_backup_dir = None
        _NET_BACKUP_GLOBS = (
            'network_conductivity.json',
            'network_conductivity_dual.json',
            'network_conductivity_hertzian.json',
            'network_conductivity_physics.json',
            'network_summary.csv',
            'network_raw_*',            # per-contact edge dumps (hertzian_ionic/...)
        )
        if not force_network:
            to_backup = []
            for pat in _NET_BACKUP_GLOBS:
                to_backup += globmod.glob(os.path.join(results_dir, pat))
            if to_backup:
                _net_backup_dir = tempfile.mkdtemp(prefix=f'net_bk_{case_id}_')
                for src in to_backup:
                    rel = os.path.relpath(src, results_dir)
                    dst = os.path.join(_net_backup_dir, rel)
                    os.makedirs(os.path.dirname(dst) or _net_backup_dir, exist_ok=True)
                    if os.path.isdir(src):
                        shutil.copytree(src, dst)
                    else:
                        shutil.copy2(src, dst)
                print(f"  [Reanalysis] Network backup saved ({len(to_backup)} items) ({case_id})")
        else:
            print(f"  [Reanalysis] force_network=True → skipping network backup ({case_id})")

        # ── Step 2: Clear & re-run contact analysis ──
        if os.path.exists(results_dir):
            shutil.rmtree(results_dir)
        os.makedirs(results_dir, exist_ok=True)
        result = run_pipeline(case_id, meta['mode'], meta['type_map'], meta.get('scale', 1000))

        # ── Step 3: Restore network backup (skipped on force) ──
        if _net_backup_dir and os.path.isdir(_net_backup_dir):
            os.makedirs(results_dir, exist_ok=True)
            for name in os.listdir(_net_backup_dir):
                src = os.path.join(_net_backup_dir, name)
                dst = os.path.join(results_dir, name)
                if os.path.isdir(src):
                    if os.path.exists(dst):
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)
            shutil.rmtree(_net_backup_dir, ignore_errors=True)
            print(f"  [Reanalysis] Network backup restored ({case_id})")

        # ── Step 4: Handle contact analysis result ──
        if not result.get('success'):
            meta['status'] = 'done' if os.path.exists(net_json_path) else 'error'
            meta['network_solver_status'] = 'success' if os.path.exists(net_json_path) else 'not_run'
            meta['analysis_log'] = result.get('log', [])
            with open(meta_file, 'w') as f:
                json.dump(meta, f, indent=2)
            print(f"  [Reanalysis] Contact analysis failed, network={'preserved' if os.path.exists(net_json_path) else 'none'} ({case_id})")
            return

        meta['status'] = 'done'
        meta['analysis_log'] = result.get('log', [])
        with open(meta_file, 'w') as f:
            json.dump(meta, f, indent=2)

        # ── Step 5: Merge network results into new full_metrics ──
        if os.path.exists(net_json_path):
            met_json = os.path.join(results_dir, 'full_metrics.json')
            if os.path.exists(met_json):
                with open(net_json_path) as _nf:
                    net_data = json.load(_nf)
                with open(met_json) as _mf:
                    met_data = json.load(_mf)
                for k in _NET_MERGE_KEYS:
                    if k in net_data and net_data[k] is not None:
                        met_data[k] = net_data[k]
                met_data = _merge_dual_into_metrics(results_dir, met_data)
                met_data = _refresh_post_network_warnings(met_data)
                met_data['network_solver_status'] = 'success'
                with open(met_json, 'w') as _mf:
                    json.dump(met_data, _mf, indent=2, default=str)
            meta['network_solver_status'] = 'success'
            meta['status'] = 'done'
            with open(meta_file, 'w') as f:
                json.dump(meta, f, indent=2)
            print(f"  [Reanalysis] Done — network SKIPPED, metrics merged ({case_id})")
            generate_report(case_id, meta.get('name', ''))
            return

        # ── Step 6: No previous network results → run network solver ──
        generate_report(case_id, meta.get('name', ''))

        # Semaphore: only 1 network solver at a time to prevent OOM crash
        meta['status'] = 'network_solving'
        meta['network_solver_status'] = 'waiting'
        with open(meta_file, 'w') as f:
            json.dump(meta, f, indent=2)

        net_status = 'not_run'
        net_error_msg = ''
        print(f"  [Network] Waiting for lock ({case_id})...")
        with _network_solver_lock:
            print(f"  [Network] Lock acquired, starting solver ({case_id})")
            meta['network_solver_status'] = 'running'
            with open(meta_file, 'w') as f:
                json.dump(meta, f, indent=2)
            try:
                atoms_csv = os.path.join(results_dir, 'atoms.csv')
                contacts_csv = os.path.join(results_dir, 'contacts.csv')
                if not os.path.exists(atoms_csv) or not os.path.exists(contacts_csv):
                    net_status = 'no_input'
                    net_error_msg = f"Missing: atoms.csv={os.path.exists(atoms_csv)}, contacts.csv={os.path.exists(contacts_csv)}"
                    print(f"  Network solver skipped: {net_error_msg}")
                else:
                    import time as _time
                    _t0 = _time.time()
                    net_cmd = ['python3', os.path.join(app.config['SCRIPTS_FOLDER'], 'network_conductivity.py'),
                               atoms_csv, contacts_csv, '-o', results_dir,
                               '-t', meta['type_map'], '-s', str(meta.get('scale', 1000)),
                               '--contact-mode', 'both']
                    print(f"  [Network] CMD: {' '.join(net_cmd)}")
                    net_result = subprocess.run(net_cmd, capture_output=True, text=True, timeout=None)
                    _elapsed = _time.time() - _t0
                    print(f"  [Network] Finished in {_elapsed:.1f}s, returncode={net_result.returncode}")
                    if net_result.stdout:
                        print(f"  [Network] stdout (last 500):\n{net_result.stdout[-500:]}")
                    if net_result.returncode != 0:
                        net_status = 'failed'
                        net_error_msg = net_result.stderr[-500:] if net_result.stderr else 'No stderr'
                        print(f"  Network solver FAILED: {net_error_msg}")
                    else:
                        net_status = 'success'
                    # Merge into full_metrics.json
                    net_json = os.path.join(results_dir, 'network_conductivity.json')
                    met_json = os.path.join(results_dir, 'full_metrics.json')
                    if os.path.exists(net_json) and os.path.exists(met_json):
                        with open(net_json) as _nf:
                            net_data = json.load(_nf)
                        with open(met_json) as _mf:
                            met_data = json.load(_mf)
                        for k in _NET_MERGE_KEYS:
                            if k in net_data and net_data[k] is not None:
                                met_data[k] = net_data[k]
                        met_data = _merge_dual_into_metrics(results_dir, met_data)
                        met_data = _refresh_post_network_warnings(met_data)
                        met_data['network_solver_status'] = net_status
                        with open(met_json, 'w') as _mf:
                            json.dump(met_data, _mf, indent=2, default=str)
                        print(f"  [Network] Merged keys into full_metrics.json (incl. physics dual)")
                    elif net_status == 'success':
                        net_status = 'no_output'
            except Exception as e:
                net_status = 'error'
                net_error_msg = str(e)
                import traceback
                print(f"  Network solver error: {e}")
                traceback.print_exc()
            meta['network_solver_status'] = net_status
            if net_error_msg:
                meta['network_solver_error'] = net_error_msg
            meta['status'] = 'done'
            with open(meta_file, 'w') as f:
                json.dump(meta, f, indent=2)
            print(f"  [Network] Lock released ({case_id}), status={net_status}")

        # Sync results + updated meta to Supabase
        storage_sync.sync_dir_to_remote(case_dir, f'uploads/{case_id}')
        storage_sync.sync_dir_to_remote(results_dir, f'results/{case_id}')

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
    return jsonify({'success': True, 'status': 'running'})

@app.route('/analyze-status/<case_id>')
def analyze_status(case_id):
    """Check if analysis is still running."""
    meta_file = os.path.join(get_case_dir(case_id), 'meta.json')
    if os.path.exists(meta_file):
        with open(meta_file) as f:
            meta = json.load(f)
        return jsonify({'status': meta.get('status', 'unknown')})
    return jsonify({'status': 'unknown'})

@app.route('/analyze-cancel/<case_id>', methods=['POST'])
def analyze_cancel(case_id):
    """Cancel running analysis by setting status to done."""
    meta_file = os.path.join(get_case_dir(case_id), 'meta.json')
    if os.path.exists(meta_file):
        with open(meta_file) as f:
            meta = json.load(f)
        if meta.get('status') in ('running', 'network_solving'):
            meta['status'] = 'done'
            meta['network_solver_status'] = meta.get('network_solver_status', 'cancelled')
            with open(meta_file, 'w') as f:
                json.dump(meta, f, indent=2)
            return jsonify({'ok': True, 'msg': 'Cancelled'})
    return jsonify({'ok': False, 'msg': 'Not running'})

@app.route('/retry-network/<case_id>', methods=['POST'])
def retry_network(case_id):
    """Manually retry network solver for a case."""
    case_dir = get_case_dir(case_id)
    results_dir = get_results_dir(case_id)
    meta_file = os.path.join(case_dir, 'meta.json')

    if not os.path.exists(meta_file):
        return jsonify({'success': False, 'error': 'Case not found'})

    with open(meta_file) as f:
        meta = json.load(f)

    def _run_net():
        import time as _time
        net_status = 'not_run'
        net_error_msg = ''
        meta['status'] = 'network_solving'
        meta['network_solver_status'] = 'waiting'
        with open(meta_file, 'w') as f:
            json.dump(meta, f, indent=2)

        print(f"  [Network Retry] Waiting for lock ({case_id})...")
        with _network_solver_lock:
            print(f"  [Network Retry] Lock acquired ({case_id})")
            meta['network_solver_status'] = 'running'
            with open(meta_file, 'w') as f:
                json.dump(meta, f, indent=2)
            try:
                atoms_csv = os.path.join(results_dir, 'atoms.csv')
                contacts_csv = os.path.join(results_dir, 'contacts.csv')
                if not os.path.exists(atoms_csv) or not os.path.exists(contacts_csv):
                    net_status = 'no_input'
                    net_error_msg = f"Missing CSV files"
                else:
                    _t0 = _time.time()
                    net_cmd = ['python3', os.path.join(app.config['SCRIPTS_FOLDER'], 'network_conductivity.py'),
                               atoms_csv, contacts_csv, '-o', results_dir,
                               '-t', meta.get('type_map', '1:AM,2:SE'), '-s', str(meta.get('scale', 1000)),
                               '--contact-mode', 'both']
                    net_result = subprocess.run(net_cmd, capture_output=True, text=True, timeout=None)
                    _elapsed = _time.time() - _t0
                    print(f"  [Network Retry] Finished in {_elapsed:.1f}s, rc={net_result.returncode}")
                    if net_result.stdout:
                        print(f"  [Network Retry] stdout:\n{net_result.stdout[-500:]}")
                    if net_result.returncode != 0:
                        net_status = 'failed'
                        net_error_msg = net_result.stderr[-500:] if net_result.stderr else 'No stderr'
                        print(f"  [Network Retry] FAILED: {net_error_msg}")
                    else:
                        net_status = 'success'
                    # Merge into full_metrics.json
                    net_json = os.path.join(results_dir, 'network_conductivity.json')
                    met_json = os.path.join(results_dir, 'full_metrics.json')
                    if os.path.exists(net_json) and os.path.exists(met_json):
                        with open(net_json) as _nf:
                            net_data = json.load(_nf)
                        with open(met_json) as _mf:
                            met_data = json.load(_mf)
                        for k in ['sigma_full', 'sigma_full_mScm', 'sigma_bulk_net',
                                  'sigma_bulk_net_mScm', 'R_brug_over_full', 'bulk_resistance_fraction',
                                  'electronic_sigma_full_mScm', 'electronic_R_brug',
                                  'electronic_active_fraction', 'electronic_percolating_fraction',
                                  'thermal_sigma_full_mScm', 'thermal_R_brug',
                              'sigma_bruggeman', 'sigma_bruggeman_mScm', 'R_bruggeman_over_full']:
                            if k in net_data and net_data[k] is not None:
                                met_data[k] = net_data[k]
                        met_data = _merge_dual_into_metrics(results_dir, met_data)
                        met_data = _refresh_post_network_warnings(met_data)
                        met_data['network_solver_status'] = net_status
                        # AM-AM contact mechanics backfill (retry path)
                        try:
                            sys.path.insert(0, app.config['SCRIPTS_FOLDER'])
                            from backfill_am_metrics import calc_am_am_stats, calc_am_am_paths
                            am_stats = calc_am_am_stats(atoms_csv, contacts_csv,
                                                        meta.get('type_map', '1:AM,2:SE'),
                                                        scale=meta.get('scale', 1000))
                            if am_stats:
                                for k, v in am_stats.items():
                                    met_data[k] = v
                                print(f"  [AM-AM] Backfilled (retry): CN={am_stats.get('am_am_cn',0):.2f}")
                            try:
                                path_stats = calc_am_am_paths(atoms_csv, contacts_csv,
                                                              meta.get('type_map', '1:AM,2:SE'),
                                                              scale=meta.get('scale', 1000))
                                if path_stats:
                                    for k, v in path_stats.items():
                                        met_data[k] = v
                                    print(f"  [AM-AM] Paths (retry): Gd={path_stats.get('am_gb_density_mean',0):.2f}")
                            except Exception as _pe:
                                print(f"  [AM-AM] Path analysis failed: {_pe}")
                        except Exception as _e:
                            print(f"  [AM-AM] Backfill failed: {_e}")
                        with open(met_json, 'w') as _mf:
                            json.dump(met_data, _mf, indent=2, default=str)
                    elif net_status == 'success':
                        net_status = 'no_output'
            except subprocess.TimeoutExpired:
                net_status = 'timeout'
                net_error_msg = 'Timed out after 3600s'
            except Exception as e:
                net_status = 'error'
                net_error_msg = str(e)
            meta['network_solver_status'] = net_status
            if net_error_msg:
                meta['network_solver_error'] = net_error_msg
            meta['status'] = 'done'
            with open(meta_file, 'w') as f:
                json.dump(meta, f, indent=2)
            print(f"  [Network Retry] Done ({case_id}), status={net_status}")

    thread = threading.Thread(target=_run_net, daemon=True)
    thread.start()
    return jsonify({'success': True, 'status': 'started'})


# Global status for the batch rerun (single-shot, last run wins).
_batch_status = {'running': False, 'total': 0, 'done': 0,
                 'current': '', 'failures': [], 'started_at': '', 'finished_at': ''}


def _find_all_cases():
    """Return list of cases to batch-process.
    Scans webapp/results/<cid>/ (meta.json lives in webapp/uploads/<cid>/ —
    NOT in the same dir as atoms.csv) and webapp/archive/<category>/<name>/
    (meta.json lives next to atoms.csv). Deduplicated by cid.
    """
    out = []
    seen = set()
    uploads_root = Path(app.config['UPLOAD_FOLDER'])
    rroot = Path(app.config['RESULTS_FOLDER'])
    if rroot.is_dir():
        for d in sorted(rroot.iterdir()):
            if not d.is_dir() or d.name in ('reports', 'group_plots'): continue
            atoms = d / 'atoms.csv'; contacts = d / 'contacts.csv'
            # meta.json is in uploads/<cid>/, not in results/<cid>/
            meta = uploads_root / d.name / 'meta.json'
            if atoms.exists() and contacts.exists() and meta.exists():
                if d.name in seen: continue
                seen.add(d.name)
                out.append(dict(cid=d.name, case_dir=str(d), results_dir=str(d),
                                meta=str(meta), atoms=str(atoms),
                                contacts=str(contacts), source='results'))
    aroot = Path(app.config['ARCHIVE_FOLDER'])
    if aroot.is_dir():
        for meta in sorted(aroot.rglob('meta.json')):
            d = meta.parent
            atoms = d / 'atoms.csv'; contacts = d / 'contacts.csv'
            if atoms.exists() and contacts.exists():
                if d.name in seen: continue
                seen.add(d.name)
                out.append(dict(cid=d.name, case_dir=str(d), results_dir=str(d),
                                meta=str(meta), atoms=str(atoms),
                                contacts=str(contacts), source='archive'))
    return out


@app.route('/batch-rerun-physics', methods=['POST'])
def batch_rerun_physics():
    """Re-run analyze_contacts + Network solver (both modes) + Physics coverage
    on every case. Keeps raw CSVs, only refreshes the analysis summary and
    solver output. Use after changing the solver resistance model."""
    global _batch_status
    if _batch_status['running']:
        return jsonify({'success': False, 'error': 'Already running', 'status': _batch_status})

    cases = _find_all_cases()
    _batch_status = {'running': True, 'total': len(cases), 'done': 0,
                     'current': '', 'failures': [],
                     'started_at': datetime.now().strftime('%H:%M:%S'),
                     'finished_at': ''}

    def _worker():
        scripts = app.config['SCRIPTS_FOLDER']
        # Dedup (archive + results may both point to the same case).
        seen = set(); dedup_cases = []
        for c in cases:
            key = c['cid']
            if key in seen: continue
            seen.add(key); dedup_cases.append(c)
        _batch_status['total'] = len(dedup_cases)

        for c in dedup_cases:
            _batch_status['current'] = c['cid']
            try:
                with open(c['meta']) as f: meta = json.load(f)
                mode = meta.get('mode', 'standard')
                type_map = meta.get('type_map', '1:AM,2:SE')
                scale = str(meta.get('scale', 1000))

                # Order matters. analyze_contacts writes full_metrics.json from
                # scratch, so it MUST run before the physics merge — otherwise
                # it wipes the physics_resistance_model / sigma_full_mScm_physics
                # keys we just wrote. The τ_Lap_eff-style σ-derived metrics are
                # rendered on-the-fly by the webapp template using the stored
                # σ values, so order here does not affect that.

                # 1) Structure summary (τ_Dij, CN, coverage_hertz, path_hop_hertz, ...)
                ac_script = 'analyze_contacts_bimodal.py' if mode == 'bimodal' else 'analyze_contacts.py'
                subprocess.run(['python3', os.path.join(scripts, ac_script),
                                c['atoms'], c['contacts'], '-o', c['results_dir'],
                                '-t', type_map, '-s', scale],
                               capture_output=True, text=True, timeout=900)

                # 2) Network solver in BOTH modes. Idempotent for Hertzian
                #    (our solver patch only adds R_film when contact_mode ==
                #    'physics', so Hertzian σ is unchanged) but it guarantees
                #    that network_conductivity_{hertzian,physics,dual}.json +
                #    legacy network_conductivity.json are all rewritten fresh
                #    — no stale pre-patch data slipping into the merge.
                with _network_solver_lock:
                    subprocess.run(['python3', os.path.join(scripts, 'network_conductivity.py'),
                                    c['atoms'], c['contacts'], '-o', c['results_dir'],
                                    '-t', type_map, '-s', scale,
                                    '--contact-mode', 'both'],
                                   capture_output=True, text=True, timeout=1800)

                # 3) Merge BOTH Hertzian and Physics keys back into full_metrics.json.
                #    analyze_contacts.py rewrites the file from scratch in step 1,
                #    so we MUST repopulate both baseline (sigma_full_mScm, etc.)
                #    and _physics-suffixed keys here, or those fields end up as None.
                hertz_json = os.path.join(c['results_dir'], 'network_conductivity_hertzian.json')
                phys_json  = os.path.join(c['results_dir'], 'network_conductivity_physics.json')
                legacy_json = os.path.join(c['results_dir'], 'network_conductivity.json')
                met_json   = os.path.join(c['results_dir'], 'full_metrics.json')
                hertz_data = {}
                phys_data  = {}
                if os.path.exists(hertz_json):
                    try: hertz_data = json.load(open(hertz_json))
                    except Exception: pass
                elif os.path.exists(legacy_json):
                    # Fallback: legacy file = Hertzian result
                    try: hertz_data = json.load(open(legacy_json))
                    except Exception: pass
                if os.path.exists(phys_json):
                    try: phys_data = json.load(open(phys_json))
                    except Exception: pass
                if os.path.exists(met_json) and (hertz_data or phys_data):
                    with open(met_json) as _mf: met_data = json.load(_mf)
                    hertz_keys = ['sigma_full', 'sigma_full_mScm', 'sigma_bulk_net',
                                  'sigma_bulk_net_mScm', 'R_brug_over_full',
                                  'bulk_resistance_fraction', 'electronic_sigma_full_mScm',
                                  'electronic_R_brug', 'electronic_active_fraction',
                                  'electronic_percolating_fraction',
                                  'thermal_sigma_full_mScm', 'thermal_R_brug',
                                  'sigma_bruggeman', 'sigma_bruggeman_mScm',
                                  'R_bruggeman_over_full']
                    for k in hertz_keys:
                        if k in hertz_data and hertz_data[k] is not None:
                            met_data[k] = hertz_data[k]
                    phys_remap = [
                        ('sigma_full',            'sigma_full_physics'),
                        ('sigma_full_mScm',       'sigma_full_mScm_physics'),
                        ('sigma_bulk_net',        'sigma_bulk_net_physics'),
                        ('sigma_bulk_net_mScm',   'sigma_bulk_net_mScm_physics'),
                        ('R_brug_over_full',      'R_brug_over_full_physics'),
                        ('bulk_resistance_fraction',
                                                  'bulk_resistance_fraction_physics'),
                        ('electronic_sigma_full_mScm',
                                                  'electronic_sigma_full_mScm_physics'),
                        ('thermal_sigma_full_mScm',
                                                  'thermal_sigma_full_mScm_physics'),
                    ]
                    for src, dst in phys_remap:
                        if src in phys_data and phys_data[src] is not None:
                            met_data[dst] = phys_data[src]
                    if phys_data:
                        met_data['physics_resistance_model'] = phys_data.get(
                            'resistance_model', 'maxwell+film')
                        met_data['physics_solver_at'] = datetime.now().strftime(
                            '%Y-%m-%d %H:%M:%S')
                    # --contact-mode=both writes network_conductivity_dual.json
                    # freshly, so _merge_dual_into_metrics picks up consistent
                    # Hertzian+Physics pair here without stale leftovers.
                    met_data = _merge_dual_into_metrics(c['results_dir'], met_data)
                    with open(met_json, 'w') as f: json.dump(met_data, f, indent=2, default=str)

                # 4) Physics coverage + path-physics metrics (read-modify-write,
                #    preserves everything above).
                subprocess.run(['python3', os.path.join(scripts, 'coverage_physics_vs_hertzian.py'),
                                '--case-dir', c['case_dir']],
                               capture_output=True, text=True, timeout=600)

                _batch_status['done'] += 1
            except Exception as e:
                _batch_status['failures'].append({'cid': c['cid'], 'err': str(e)[:200]})
                _batch_status['done'] += 1
        _batch_status['running'] = False
        _batch_status['current'] = '(done)'
        _batch_status['finished_at'] = datetime.now().strftime('%H:%M:%S')

    threading.Thread(target=_worker, daemon=True).start()
    return jsonify({'success': True, 'count': len(cases)})


@app.route('/batch-rerun-physics/status')
def batch_rerun_physics_status():
    # Scan all cases (already deduplicated by _find_all_cases) and summarise
    # which resistance model each one is on. Four states:
    #   'maxwell+film' → new formula applied (PHYS ✓)
    #   'maxwell'      → legacy Physics σ, needs rerun (PHYS legacy)
    #   'no_physics'   → Physics solver never ran (PHYS ∅)
    #   'no_metrics'   → full_metrics.json missing (shouldn't normally happen)
    counts = {'upgraded': 0, 'maxwell': 0,
              'no_physics': 0, 'no_metrics': 0}
    latest_at = ''
    for c in _find_all_cases():
        fm_path = os.path.join(c['results_dir'], 'full_metrics.json')
        if not os.path.exists(fm_path):
            counts['no_metrics'] += 1; continue
        try:
            with open(fm_path) as f: m = json.load(f)
        except Exception:
            counts['no_metrics'] += 1; continue
        model = m.get('physics_resistance_model')
        if model in ('mikic', 'maxwell+film'):
            counts['upgraded'] += 1
        elif model == 'maxwell' or 'sigma_full_mScm_physics' in m:
            counts['maxwell'] += 1
        else:
            counts['no_physics'] += 1
        ts = m.get('physics_solver_at', '')
        if ts > latest_at: latest_at = ts
    status = dict(_batch_status)
    status['model_counts'] = counts
    status['latest_physics_at'] = latest_at
    status['total_cases'] = sum(counts.values())
    return jsonify(status)


@app.route('/single/<case_id>')
def single(case_id):
    """View single case results.
    Falls back to archive/<folder>/<case_id>/ if results/ is empty (archive-migrated cases)."""
    case_dir = get_case_dir(case_id)
    results_dir = get_results_dir(case_id)
    meta_file = os.path.join(case_dir, 'meta.json')

    if not os.path.exists(meta_file):
        return redirect(url_for('index'))

    with open(meta_file) as f:
        meta = json.load(f)
    meta['id'] = case_id

    # ── Archive fallback: if results/ is empty, find case in archive/ ──
    def _results_has_data(d):
        if not os.path.isdir(d): return False
        return any(os.path.exists(os.path.join(d, n + '.csv'))
                   for n in ['atom_statistics', 'contact_summary', 'coordination_summary', 'network_summary']) \
            or os.path.exists(os.path.join(d, 'full_metrics.json'))

    archive_path = None  # relative path under archive/ if fallback triggered
    if not _results_has_data(results_dir):
        archive_root = app.config.get('ARCHIVE_FOLDER')
        if archive_root and os.path.isdir(archive_root):
            # Try case_id (timestamp) first, then meta.name/label/case_id/case_name
            # (webapp manages cases by timestamp but archive dirs use display names)
            search_keys = [case_id]
            for k in ('name', 'label', 'case_id', 'case_name'):
                v = meta.get(k)
                if isinstance(v, str) and v and v not in search_keys:
                    search_keys.append(v)
            for dirpath, dirs, _ in os.walk(archive_root):
                for key in search_keys:
                    if key in dirs:
                        candidate = os.path.join(dirpath, key)
                        if _results_has_data(candidate):
                            results_dir = candidate
                            archive_path = os.path.relpath(candidate, archive_root)
                            break
                if archive_path:
                    break

    # Collect figures
    figures = []
    figures_dir = os.path.join(results_dir, 'figures')
    if os.path.isdir(figures_dir):
        for png in sorted(globmod.glob(os.path.join(figures_dir, '*.png'))):
            figures.append(os.path.basename(png))

    # Load report
    report = ''
    report_path = os.path.join(results_dir, 'report.md')
    if os.path.exists(report_path):
        with open(report_path) as f:
            report = f.read()

    # Load CSVs for tables (atom_statistics first, no force_summary)
    tables = {}
    for csv_name in ['atom_statistics', 'contact_summary', 'coordination_summary',
                     'network_summary']:
        csv_path = os.path.join(results_dir, f'{csv_name}.csv')
        if os.path.exists(csv_path):
            import pandas as pd
            df = pd.read_csv(csv_path)
            tables[csv_name] = {
                'columns': df.columns.tolist(),
                'data': df.values.tolist()
            }

    # Load full_metrics.json (needed for placeholder patching + physics injection)
    metrics = {}
    metrics_path = os.path.join(results_dir, 'full_metrics.json')
    if os.path.exists(metrics_path):
        with open(metrics_path) as f:
            metrics = json.load(f)

    # Patch placeholder '-' values from full_metrics.json BEFORE 4-col transform
    # (transform copies row[1] → row[2], so placeholders must be filled first)
    if 'network_summary' in tables and metrics:
        n_large = metrics.get('n_large_components')
        if n_large is not None:
            for row in tables['network_summary']['data']:
                if str(row[0]) == 'SE Cluster 수' and '≥10' not in str(row[1]):
                    row[1] = f"{n_large}(≥10) / {row[1]}"
        placeholder_map = {
            'GB Density(hops/μm)': 'gb_density_mean',
            'Path Hop Area mean(μm²)': 'path_hop_area_mean',
            'Path Bottleneck(μm²)': 'path_hop_area_min_mean',
            'Path Conductance(μm²)': 'path_conductance_mean',
        }
        for row in tables['network_summary']['data']:
            label = str(row[0])
            if label in placeholder_map and str(row[1]).strip() in ('-', ''):
                val = metrics.get(placeholder_map[label])
                if val is not None:
                    row[1] = val
            if label == 'σ_eff/σ_bulk':
                row[0] = 'σ_brug/σ_grain (Bruggeman)'
        has_brug_abs = any(str(row[0]) == 'σ_Bruggeman (mS/cm)'
                           for row in tables['network_summary']['data'])
        if not has_brug_abs and metrics.get('sigma_ratio'):
            sigma_brug_mScm = round(3.0 * metrics['sigma_ratio'], 4)
            for idx, row in enumerate(tables['network_summary']['data']):
                if 'σ_brug/σ_grain' in str(row[0]):
                    tables['network_summary']['data'].insert(
                        idx, ['σ_Bruggeman (mS/cm)', sigma_brug_mScm])
                    break

    # 4-column transform + section injection (Network Solver + AM-AM) — shared helper
    transform_network_summary_4col(tables, metrics, meta)
    inject_tier1_patch_rows(tables, metrics)

    # Brittle-fracture summary tab (auto-built from full_metrics.json keys)
    fracture_tbl = build_fracture_summary_table(metrics)
    if fracture_tbl is not None:
        tables['fracture_summary'] = fracture_tbl

    # Load input_params.json
    input_params = {}
    params_path = os.path.join(results_dir, 'input_params.json')
    if os.path.exists(params_path):
        with open(params_path) as f:
            input_params = json.load(f)

    return render_template('single.html', case=meta, figures=figures,
                         report=report, tables=tables, metrics=metrics,
                         input_params=input_params, archive_path=archive_path)

@app.route('/group', methods=['GET', 'POST'])
def group():
    """Group comparison page."""
    cases = list_cases()
    selected = request.args.getlist('cases')
    case_groups_param = request.args.get('case_groups', '[]')

    comparison_data = {}
    case_groups_parsed = []
    try:
        case_groups_parsed = json.loads(case_groups_param)
    except:
        pass
    if selected:
        # Key metrics grouped by category
        # (label, unit, key, category)
        display_keys_raw = [
            # ── 구조/계면 ──
            ('P:S', '', 'ps_ratio', '구조/계면'),
            ('Porosity', '(%)', 'porosity', '구조/계면'),
            ('두께', '(μm)', 'thickness_um', '구조/계면'),
            ('AM-SE Total', '(μm²)', 'area_AM전체_SE_total', '구조/계면'),
            ('SE-SE N', '', 'area_SE_SE_n', '구조/계면'),
            ('SE-SE Mean', '(μm²)', 'area_SE_SE_mean', '구조/계면'),
            ('SE-SE Total', '(μm²)', 'area_SE_SE_total', '구조/계면'),
            ('Coverage P', '(%)', 'coverage_AM_P_mean', '구조/계면'),
            ('Coverage S', '(%)', 'coverage_AM_S_mean', '구조/계면'),
            # ── 이온경로 ──
            ('SE-SE CN', '', 'se_se_cn', '이온경로'),
            ('SE-SE CN std', '', 'se_se_cn_std', '이온경로'),
            ('SE Cluster', '', 'n_components', '이온경로'),
            ('Large(≥10)', '', 'n_large_components', '이온경로'),
            ('Percolation', '(%)', 'percolation_pct', '이온경로'),
            ('Top Reachable', '(%)', 'top_reachable_pct', '이온경로'),
            ('Tortuosity', '', 'tortuosity_mean', '이온경로'),
            ('τ std', '', 'tortuosity_std', '이온경로'),
            ('GB Density', '(hops/μm)', 'gb_density_mean', '이온경로'),
            ('Hop Area', '(μm²)', 'path_hop_area_mean', '이온경로'),
            ('Bottleneck', '(μm²)', 'path_hop_area_min_mean', '이온경로'),
            ('Path Conductance', '(μm²)', 'path_conductance_mean', '이온경로'),
            # ── 활성도/전도 ──
            ('Ionic Active', '(%)', 'ionic_active_pct', '활성도'),
            ('AM-SE CN', '', 'am_se_cn_mean', '활성도'),
            ('Vulnerable', '(%)', 'am_vulnerable_pct', '활성도'),
            ('φ_SE', '', 'phi_se', '활성도'),
            ('σ_brug/σ_grain', '', 'sigma_ratio', '이온전도'),
            # ── Network Solver ──
            ('σ_ionic', '(mS/cm)', 'sigma_full_mScm', 'Network Solver'),
            ('R_brug', '(×)', 'R_brug_over_full', 'Network Solver'),
            ('Constriction', '(%)', '_constriction_pct', 'Network Solver'),
            ('σ_electronic', '(mS/cm)', 'electronic_sigma_full_mScm', 'Network Solver'),
            ('σ_thermal', '(mS/cm)', 'thermal_sigma_full_mScm', 'Network Solver'),
            # ── 접촉력/응력 ──
            ('Fn AM-AM', '(μN)', 'fn_AM_P_AM_P_mean', '접촉력/응력'),
            ('Fn AM-SE', '(μN)', 'fn_AM_P_SE_mean', '접촉력/응력'),
            ('Fn SE-SE', '(μN)', 'fn_SE_SE_mean', '접촉력/응력'),
            ('CP mean', '(MPa)', 'contact_pressure_mean', '접촉력/응력'),
            ('CP max', '(MPa)', 'contact_pressure_max', '접촉력/응력'),
            ('Stress CV', '(%)', 'stress_cv', '접촉력/응력'),
            ('σ_AM_P/σ_mean', '', 'stress_ratio_AM_P', '접촉력/응력'),
            ('σ_AM_S/σ_mean', '', 'stress_ratio_AM_S', '접촉력/응력'),
            ('σ_SE/σ_mean', '', 'stress_ratio_SE', '접촉력/응력'),
        ]
        display_keys = [(l, u, k) for l, u, k, _ in display_keys_raw]
        # Track category boundaries for column separators
        col_categories = [''] + [cat for _, _, _, cat in display_keys_raw]
        rows = []
        for cid in selected:
            # Handle archive: prefix
            if cid.startswith('archive:'):
                archive_rel = cid[len('archive:'):]
                case_path = os.path.join(app.config['ARCHIVE_FOLDER'], archive_rel)
                meta_file = os.path.join(case_path, 'meta.json')
                metrics_path = os.path.join(case_path, 'full_metrics.json')
                case_name = os.path.basename(archive_rel)
            else:
                case_path = get_results_dir(cid)
                meta_file = os.path.join(get_case_dir(cid), 'meta.json')
                metrics_path = os.path.join(case_path, 'full_metrics.json')
                case_name = cid

            if os.path.exists(meta_file):
                with open(meta_file) as f:
                    meta = json.load(f)
                case_name = meta.get('name', case_name)

            metrics = {}
            if os.path.exists(metrics_path):
                with open(metrics_path) as f:
                    metrics = json.load(f)
            else:
                continue

            # Derived: constriction percentage
            bf = metrics.get('bulk_resistance_fraction')
            if bf is not None and bf > 0:
                metrics['_constriction_pct'] = round((1 - bf) * 100, 1)

            # Standard 모드: coverage_AM_mean → P:S에 따라 P 또는 S에 매핑
            if 'coverage_AM_mean' in metrics:
                ps = metrics.get('ps_ratio', '')
                if ps in ('P only', '10:0'):
                    metrics.setdefault('coverage_AM_P_mean', metrics['coverage_AM_mean'])
                else:
                    metrics.setdefault('coverage_AM_S_mean', metrics['coverage_AM_mean'])
            # Standard 모드: area_AM_SE_total → P:S에 따라 매핑
            if 'area_AM_SE_total' in metrics and 'area_AM_P_SE_total' not in metrics:
                ps = metrics.get('ps_ratio', '')
                if ps in ('P only', '10:0'):
                    metrics['area_AM_P_SE_total'] = metrics['area_AM_SE_total']
                else:
                    metrics['area_AM_S_SE_total'] = metrics['area_AM_SE_total']

            # Force metric fallbacks: AM_P↔AM_S
            if 'fn_AM_P_AM_P_mean' not in metrics and 'fn_AM_S_AM_S_mean' in metrics:
                metrics['fn_AM_P_AM_P_mean'] = metrics['fn_AM_S_AM_S_mean']
            if 'fn_AM_P_SE_mean' not in metrics and 'fn_AM_S_SE_mean' in metrics:
                metrics['fn_AM_P_SE_mean'] = metrics['fn_AM_S_SE_mean']

            row = {'케이스': case_name}
            for label, unit, key in display_keys:
                val = metrics.get(key, '')
                if isinstance(val, float):
                    if key in ('path_conductance_mean', 'path_hop_area_min_mean'):
                        val = f"{val:.2e}" if val > 0 else '-'
                    else:
                        val = round(val, 2)
                row[label] = val if val != '' else '-'
            rows.append(row)

        if rows:
            # Build columns with unit subtitles
            col_headers = [{'name': '케이스', 'unit': ''}]
            for label, unit, key in display_keys:
                col_headers.append({'name': label, 'unit': unit})

            # Split into case group tables
            if case_groups_parsed and len(case_groups_parsed) > 1:
                tables = []
                row_idx = 0
                for gi, g in enumerate(case_groups_parsed):
                    gname = g.get('name', '') or f"Case {chr(65+gi)}"
                    group_rows = []
                    for _ in g.get('cases', []):
                        if row_idx < len(rows):
                            group_rows.append(rows[row_idx])
                            row_idx += 1
                    # Mark best values per column
                    # lower_better: Porosity, 두께, Tortuosity, τ std, Stress CV, GB Density, Vulnerable, CP mean, CP max
                    # higher_better: everything else (except P:S, 케이스 which are labels)
                    lower_better = {'Porosity', '두께', 'Tortuosity', 'τ std', 'Stress CV',
                                    'GB Density', 'Vulnerable', 'CP mean', 'CP max', 'SE Cluster',
                                    'R_brug', 'Constriction'}
                    skip_cols = {'P:S', '케이스'}
                    best_marks = {}  # col -> best row index
                    for label, unit, key in display_keys:
                        if label in skip_cols:
                            continue
                        vals = []
                        for ri, r in enumerate(group_rows):
                            v = r.get(label, '-')
                            try:
                                vals.append((ri, float(str(v).replace('e', 'E').strip())))
                            except (ValueError, TypeError):
                                pass
                        if vals:
                            if label in lower_better:
                                best_val = min(vals, key=lambda x: x[1])
                                worst_val = max(vals, key=lambda x: x[1])
                            else:
                                best_val = max(vals, key=lambda x: x[1])
                                worst_val = min(vals, key=lambda x: x[1])
                            # Skip if all same value
                            if best_val[1] != worst_val[1]:
                                best_marks[(label, best_val[0])] = True
                    for ri, r in enumerate(group_rows):
                        r['__best__'] = {label for (label, idx), _ in best_marks.items() if idx == ri}

                    tables.append({'name': gname, 'rows': group_rows, 'color': ['#6c8cff','#ff6b6b','#51cf66','#ffd43b'][gi % 4]})
                comparison_data = {
                    'columns': [c['name'] for c in col_headers],
                    'units': [c['unit'] for c in col_headers],
                    'categories': col_categories,
                    'tables': tables
                }
            else:
                comparison_data = {
                    'columns': [c['name'] for c in col_headers],
                    'units': [c['unit'] for c in col_headers],
                    'categories': col_categories,
                    'tables': [{'name': '', 'rows': rows, 'color': ''}]
                }

    # Scan archive for folders with full_metrics.json
    archive_folders = []
    archive_root = app.config['ARCHIVE_FOLDER']
    if os.path.isdir(archive_root):
        for dirpath, dirnames, filenames in os.walk(archive_root):
            # Count cases in this folder (subfolders with full_metrics.json)
            case_count = 0
            for d in dirnames:
                if os.path.exists(os.path.join(dirpath, d, 'full_metrics.json')):
                    case_count += 1
            if case_count > 0:
                rel = os.path.relpath(dirpath, archive_root)
                archive_folders.append({'path': rel if rel != '.' else '(최상위)', 'case_count': case_count})

    return render_template('group.html', cases=cases, selected=selected,
                         comparison=comparison_data, archive_folders=archive_folders,
                         case_groups_json=case_groups_param)

@app.route('/group/archive-cases')
def group_archive_cases():
    """Return cases in an archive folder that have full_metrics.json."""
    folder = request.args.get('folder', '')
    archive_root = app.config['ARCHIVE_FOLDER']
    if folder == '(최상위)':
        base = archive_root
    else:
        base = os.path.join(archive_root, folder)
    if not os.path.isdir(base):
        return jsonify({'cases': []})

    cases = []
    for name in sorted(os.listdir(base)):
        case_dir = os.path.join(base, name)
        metrics_path = os.path.join(case_dir, 'full_metrics.json')
        if os.path.isdir(case_dir) and os.path.exists(metrics_path):
            with open(metrics_path) as f:
                m = json.load(f)
            # Use archive: prefix to distinguish from dashboard cases
            case_id = f"archive:{os.path.relpath(case_dir, archive_root)}"
            cases.append({
                'id': case_id,
                'name': name,
                'ps_ratio': m.get('ps_ratio', ''),
                'warning_count': m.get('warning_count', 0),
                'warning_msgs': [w['msg'] for w in m.get('warnings', [])],
            })
    return jsonify({'cases': cases})

@app.route('/group/plots', methods=['POST'])
def group_plots():
    """Generate comparison plots for selected cases."""
    selected = request.form.getlist('cases')
    plots = request.form.getlist('plots')
    if not selected or not plots:
        return jsonify({'error': '케이스와 플롯을 선택하세요.'}), 400

    session_id = datetime.now().strftime('%y%m%d_%H%M%S') + '_' + str(uuid.uuid4())[:4]
    plot_dir = os.path.join(app.config['RESULTS_FOLDER'], 'group_plots', session_id)
    os.makedirs(plot_dir, exist_ok=True)

    # Collect metrics files and names
    input_files = []
    names = []
    for cid in selected:
        if cid.startswith('archive:'):
            archive_rel = cid[len('archive:'):]
            case_path = os.path.join(app.config['ARCHIVE_FOLDER'], archive_rel)
            metrics_path = os.path.join(case_path, 'full_metrics.json')
            case_name = os.path.basename(archive_rel)
        else:
            case_path = get_results_dir(cid)
            metrics_path = os.path.join(case_path, 'full_metrics.json')
            meta_file = os.path.join(get_case_dir(cid), 'meta.json')
            case_name = cid
            if os.path.exists(meta_file):
                with open(meta_file) as f:
                    case_name = json.load(f).get('name', cid)
        if os.path.exists(metrics_path):
            input_files.append(metrics_path)
            names.append(case_name)

    if not input_files:
        return jsonify({'error': '메트릭 데이터가 없습니다.'}), 400

    # Pass case groups info
    case_groups_json = request.form.get('case_groups', '[]')
    try:
        case_groups_raw = json.loads(case_groups_json)
    except:
        case_groups_raw = []

    # Build group sizes string: "3,5" means first 3 cases = group A, next 5 = group B
    # Build group names string
    # Filter against ACTUAL surviving cases — if a case was deleted from disk,
    # the main loop below silently drops it from input_files. Without mirroring
    # that filter here, group_sizes would over-count by the number of missing
    # cases and the vertical group separators drift by that amount.
    surviving = set()
    for cid in selected:
        if cid.startswith('archive:'):
            case_path = os.path.join(app.config['ARCHIVE_FOLDER'], cid[len('archive:'):])
        else:
            case_path = get_results_dir(cid)
        if os.path.exists(os.path.join(case_path, 'full_metrics.json')):
            surviving.add(cid)

    group_sizes = []
    group_names_list = []
    for g in case_groups_raw:
        count = sum(1 for c in g.get('cases', []) if c in surviving)
        if count == 0:
            continue
        group_sizes.append(str(count))
        group_names_list.append(g.get('name', '') or f"Case {chr(65 + len(group_names_list))}")

    global_rgb = request.form.get('global_rgb', '')
    global_c_ion = request.form.get('global_c_ion', '')
    y_max_sigma = request.form.get('y_max_sigma', '')  # optional unified σ y-axis (mS/cm)

    scripts = app.config['SCRIPTS_FOLDER']
    cmd = ['python3', os.path.join(scripts, 'generate_comparison_plots.py'),
           '-i'] + input_files + ['-n'] + names + ['-o', plot_dir, '-p'] + plots
    if group_sizes and len(group_sizes) > 1:
        cmd += ['--group-sizes', ','.join(group_sizes),
                '--group-names', ','.join(group_names_list)]
    if global_rgb:
        cmd += ['--global-rgb', global_rgb]
    if global_c_ion:
        cmd += ['--global-c-ion', global_c_ion]
    if y_max_sigma:
        try:
            # Validate it's a positive number before passing
            _yms = float(y_max_sigma)
            if _yms > 0:
                cmd += ['--y-max-sigma', str(_yms)]
        except ValueError:
            pass  # invalid → ignore, fall back to auto
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.stdout:
        print(f"[plots] stdout:\n{result.stdout}")
    if result.stderr:
        print(f"[plots] stderr:\n{result.stderr}")

    if result.returncode != 0:
        return jsonify({'error': f'Plot 생성 실패: {result.stderr}'}), 500

    # Load plot info
    info_path = os.path.join(plot_dir, 'plot_info.json')
    plot_list = []
    if os.path.exists(info_path):
        with open(info_path) as f:
            info = json.load(f)
        # particle_info always first
        if 'particle_info' in info:
            plot_list.append(info['particle_info'])
        for key in plots:
            if key in info:
                plot_list.append(info[key])

    return jsonify({'session': session_id, 'plots': plot_list})

@app.route('/group/plot-image/<session>/<filename>')
def serve_group_plot(session, filename):
    plot_dir = os.path.join(app.config['RESULTS_FOLDER'], 'group_plots', session)
    return send_from_directory(plot_dir, filename)

@app.route('/group/report', methods=['POST'])
def group_report():
    """Generate comprehensive group comparison markdown report."""
    selected = request.form.getlist('cases')
    title = request.form.get('title', 'DEM_Bimodal_Comparison')
    notes = request.form.get('notes', '')

    now = datetime.now().strftime('%y%m%d')
    L = []  # lines

    # Header
    L.append(f'# {now}_{title}\n')
    L.append(f'> **날짜**: {datetime.now().strftime("%Y-%m-%d")}')
    L.append(f'> **비교 케이스**: {len(selected)}개')
    if notes:
        L.append(f'> **메모**: {notes}')
    L.append('')
    L.append('---\n')

    # Load all metrics
    all_metrics = []
    case_names = []
    for cid in selected:
        if cid.startswith('archive:'):
            archive_rel = cid[len('archive:'):]
            case_path = os.path.join(app.config['ARCHIVE_FOLDER'], archive_rel)
            meta_file = os.path.join(case_path, 'meta.json')
            metrics_path = os.path.join(case_path, 'full_metrics.json')
            name = os.path.basename(archive_rel)
        else:
            case_path = get_results_dir(cid)
            meta_file = os.path.join(get_case_dir(cid), 'meta.json')
            metrics_path = os.path.join(case_path, 'full_metrics.json')
            name = cid
        if os.path.exists(meta_file):
            with open(meta_file) as f:
                name = json.load(f).get('name', name)
        metrics = {}
        if os.path.exists(metrics_path):
            with open(metrics_path) as f:
                metrics = json.load(f)
        all_metrics.append(metrics)
        case_names.append(name)

    if not all_metrics:
        return jsonify({'report': '메트릭 데이터가 없습니다.', 'path': ''})

    # 1. System Overview
    L.append('## 1. System Overview\n')
    import pandas as pd
    overview_rows = []
    display_keys = [
        ('P:S', 'ps_ratio'), ('Porosity(%)', 'porosity'),
        ('Thickness(μm)', 'thickness_um'),
        ('AM-SE Total(μm²)', 'area_AM전체_SE_total'),
        ('SE-SE Total(μm²)', 'area_SE_SE_total'),
        ('SE-SE CN', 'se_se_cn'), ('SE-SE CN std', 'se_se_cn_std'), ('SE Cluster', 'n_components'),
        ('Percolation(%)', 'percolation_pct'),
        ('Top Reachable(%)', 'top_reachable_pct'),
        ('Tortuosity', 'tortuosity_mean'),
        ('Ionic Active(%)', 'ionic_active_pct'),
    ]
    for i, name in enumerate(case_names):
        row = {'Case': name}
        for label, key in display_keys:
            val = all_metrics[i].get(key, '-')
            if isinstance(val, float):
                val = round(val, 2)
            row[label] = val
        overview_rows.append(row)
    df = pd.DataFrame(overview_rows)
    L.append(df.to_markdown(index=False))
    L.append('')

    # 2. Key Findings (자동 분석)
    L.append('\n## 2. Key Findings\n')

    porosities = [(case_names[i], m.get('porosity', 0)) for i, m in enumerate(all_metrics) if m.get('porosity')]
    if porosities:
        min_p = min(porosities, key=lambda x: x[1])
        L.append(f'- **Porosity 최저**: {min_p[0]} ({min_p[1]:.2f}%)')

    percs = [(case_names[i], m.get('percolation_pct', 0)) for i, m in enumerate(all_metrics) if m.get('percolation_pct')]
    if percs:
        max_perc = max(percs, key=lambda x: x[1])
        L.append(f'- **Percolation 최대**: {max_perc[0]} ({max_perc[1]:.1f}%)')

    torts = [(case_names[i], m.get('tortuosity_mean', 99)) for i, m in enumerate(all_metrics) if m.get('tortuosity_mean')]
    if torts:
        min_tort = min(torts, key=lambda x: x[1])
        L.append(f'- **Tortuosity 최저**: {min_tort[0]} ({min_tort[1]:.2f})')

    ionics = [(case_names[i], m.get('ionic_active_pct', 0)) for i, m in enumerate(all_metrics) if m.get('ionic_active_pct')]
    if ionics:
        max_ionic = max(ionics, key=lambda x: x[1])
        L.append(f'- **Ionic Active 최대**: {max_ionic[0]} ({max_ionic[1]:.1f}%)')

    se_totals = [(case_names[i], m.get('area_SE_SE_total', 0)) for i, m in enumerate(all_metrics) if m.get('area_SE_SE_total')]
    if se_totals:
        max_se = max(se_totals, key=lambda x: x[1])
        L.append(f'- **SE-SE Total Area 최대**: {max_se[0]} ({max_se[1]:,.1f} μm²)')

    L.append('')

    # 3. Trade-off Analysis
    L.append('\n## 3. Trade-off Analysis\n')
    L.append('### AM-SE vs SE-SE Trade-off\n')
    L.append('| AM_P ↑ | AM-SE 계면 | SE-SE 네트워크 |')
    L.append('|---|---|---|')
    L.append('| 변화 | **감소** | **개선** (percolation↑, tortuosity↓) |')
    L.append('| 의미 | 반응 면적 감소 | 이온 경로 확보 |')
    L.append('| 제한 요인 | charge transfer | ionic transport |')
    L.append('')
    L.append('> **전극 성능 = 병목(bottleneck)이 결정**')
    L.append('> - SE 네트워크 부족 (P 적음) → ionic transport limited')
    L.append('> - AM-SE 계면 부족 (P 많음) → charge transfer limited')
    L.append('')

    # 4. SE-SE Contact Network Trade-off
    L.append('### SE-SE Contact: Quality vs Quantity\n')
    L.append('AM_P↑ → SE-SE 접촉 개수↑ (넓은 공간에 분산) + 개별 접촉 면적↓ (느슨하게 배치)')
    L.append('')
    se_n = [(case_names[i], m.get('area_SE_SE_n', 0), m.get('area_SE_SE_mean', 0))
            for i, m in enumerate(all_metrics) if m.get('area_SE_SE_n')]
    if se_n:
        L.append('| Case | SE-SE N | SE-SE Mean Area(μm²) | SE-SE Total(μm²) |')
        L.append('|---|---|---|---|')
        for name, n, mean in se_n:
            total = n * mean
            L.append(f'| {name} | {int(n):,} | {mean:.4f} | {total:,.1f} |')
    L.append('')

    # 5. Conclusion
    L.append('\n## 4. Conclusion\n')
    if porosities and len(porosities) > 2:
        L.append(f'- Porosity: {porosities[0][0]} ({porosities[0][1]:.1f}%) → {porosities[-1][0]} ({porosities[-1][1]:.1f}%)')
    if percs and torts:
        L.append(f'- 이온경로: Percolation {percs[0][1]:.0f}%→{percs[-1][1]:.0f}%, Tortuosity {torts[0][1]:.1f}→{torts[-1][1]:.1f}')
    L.append('')

    # Tags
    L.append('---\n')

    # Claude AI 심층 분석
    ai_analysis = _generate_ai_analysis(all_metrics, case_names, title, notes)
    if ai_analysis:
        L.append('\n## 5. AI 심층 분석 (Claude)\n')
        L.append(ai_analysis)
        L.append('')

    L.append('---\n')
    L.append('#DEM #bimodal #comparison #percolation #tortuosity #coverage #ASSB\n')

    report = '\n'.join(L)

    # Save report
    group_dir = os.path.join(app.config['RESULTS_FOLDER'], 'group_reports')
    os.makedirs(group_dir, exist_ok=True)
    report_path = os.path.join(group_dir, f'{now}_{title.replace(" ", "_")}.md')
    with open(report_path, 'w') as f:
        f.write(report)

    return jsonify({'report': report, 'path': report_path})

@app.route('/results/<case_id>/figures/<filename>')
def serve_figure(case_id, filename):
    figures_dir = os.path.join(get_results_dir(case_id), 'figures')
    return send_from_directory(figures_dir, filename)

@app.route('/results/<case_id>/3d-data')
def serve_3d_data(case_id):
    """Serve particle + percolation data for 3D viewer."""
    import pandas as pd
    results_dir = get_results_dir(case_id)
    case_dir = get_case_dir(case_id)
    meta_file = os.path.join(case_dir, 'meta.json')

    if not os.path.exists(meta_file):
        return jsonify({'error': 'Case not found'}), 404

    with open(meta_file) as f:
        meta = json.load(f)
    scale = meta.get('scale', 1000)
    type_map_str = meta.get('type_map', '1:AM,2:SE')
    type_map = {}
    for item in type_map_str.split(','):
        k, v = item.split(':')
        type_map[int(k)] = v.strip()

    # Load atoms
    atoms_csv = os.path.join(results_dir, 'atoms.csv')
    if not os.path.exists(atoms_csv):
        return jsonify({'error': 'No atom data'}), 404

    # atoms-only flag: no contacts.csv OR full_metrics.has_contacts=False
    contacts_csv = os.path.join(results_dir, 'contacts.csv')
    atoms_only_mode = not os.path.exists(contacts_csv)
    fm_path = os.path.join(results_dir, 'full_metrics.json')
    if os.path.exists(fm_path):
        try:
            with open(fm_path) as f:
                _fm = json.load(f)
            if _fm.get('has_contacts') is False:
                atoms_only_mode = True
        except Exception:
            pass

    df = pd.read_csv(atoms_csv)
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    particles = []
    for _, row in df.iterrows():
        t = int(row['type'])
        particles.append({
            'id': int(row['id']),
            'type': type_map.get(t, f'T{t}'),
            'x': round(float(row['x']) * scale, 2),
            'y': round(float(row['y']) * scale, 2),
            'z': round(float(row['z']) * scale, 2),
            'r': round(float(row['radius']) * scale, 2),
        })

    # Box bounds — read from input_params.json if available
    _box_x, _box_y = 0.05, 0.05
    _ip_path = os.path.join(results_dir, 'input_params.json')
    if os.path.exists(_ip_path):
        with open(_ip_path) as f:
            _ip = json.load(f)
        _box_x = _ip.get('box_x', 0.05)
        _box_y = _ip.get('box_y', 0.05)
    box = {
        'x_min': 0, 'x_max': round(_box_x * scale, 1),
        'y_min': 0, 'y_max': round(_box_y * scale, 1),
        'z_min': 0,
    }
    # box.z_max = tight fit to actual particles (ignores stale mesh_info plate_z
    # which can drift from the real packed height after DEM re-analysis).
    particle_z_top = max(p['z'] + p['r'] for p in particles) if particles else 0
    mesh_file = os.path.join(results_dir, 'mesh_info.json')
    mesh_triangles = []
    if os.path.exists(mesh_file):
        try:
            with open(mesh_file) as f:
                _mesh_data = json.load(f)
            plate_z_mesh = _mesh_data['plate_z'] * scale
            # Use whichever is smaller — avoids oversized bounding box when
            # mesh_info.plate_z is a stale pre-compaction value
            box['z_max'] = round(min(plate_z_mesh, particle_z_top), 1)
            # Pull triangles (raw sim units) and scale to display μm
            for tri in _mesh_data.get('triangles', []):
                mesh_triangles.append([
                    [round(v[0] * scale, 3), round(v[1] * scale, 3), round(v[2] * scale, 3)]
                    for v in tri
                ])
        except Exception:
            box['z_max'] = round(particle_z_top, 1)
    else:
        box['z_max'] = round(particle_z_top, 1)

    # Percolation data from full_metrics
    percolation = {'top_reachable': [], 'bottom_se': [], 'top_se': []}
    metrics_path = os.path.join(results_dir, 'full_metrics.json')

    # Try to load percolation sets from a saved file
    perc_path = os.path.join(results_dir, 'percolation_sets.json')
    if os.path.exists(perc_path):
        with open(perc_path) as f:
            percolation = json.load(f)

    # Paths (tortuosity sample paths)
    paths = []
    paths_path = os.path.join(results_dir, 'tortuosity_paths.json')
    if os.path.exists(paths_path):
        with open(paths_path) as f:
            paths = json.load(f)

    # SE clusters for click interaction
    clusters = {}
    clusters_path = os.path.join(results_dir, 'se_clusters.json')
    if os.path.exists(clusters_path):
        with open(clusters_path) as f:
            clusters = json.load(f)

    # ── 3D viewer auxiliary data: stress / brittle / cluster classification ──
    # Lightweight recompute over contacts.csv on each request — small CSV
    # (<100k rows typical) so this stays fast (< 200 ms).
    aux = {
        'stress_max': {}, 'dr_max': {},
        'brittle_pairs': [], 'se_stress_pairs': [],
        'cluster_meta': {}, 'cluster_id_per_se': {},
        'coverage_per_am': {},
    }
    try:
        import sys as _sys
        _scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
        if _scripts_dir not in _sys.path:
            _sys.path.insert(0, _scripts_dir)
        from viewer3d_data import (
            aggregate_particle_metrics, classify_clusters,
            build_cluster_id_map, build_coverage_map,
        )
        # Build atoms_by_id from atoms.csv we already loaded.
        atoms_by_id = {int(r['id']): {
            'type':   int(r['type']),
            'radius': float(r['radius']),
        } for _, r in df.iterrows()}
        if os.path.exists(contacts_csv):
            contacts_df = pd.read_csv(contacts_csv, low_memory=False)
            contacts_iter = contacts_df.to_dict('records')
            agg = aggregate_particle_metrics(
                contacts_iter, atoms_by_id, type_map, scale=scale)
            aux['stress_max']      = agg['stress_max']
            aux['dr_max']          = agg['dr_max']
            aux['brittle_pairs']   = agg['brittle_pairs']
            aux['se_stress_pairs'] = agg['se_stress_pairs']
        aux['cluster_meta']      = classify_clusters(clusters)
        aux['cluster_id_per_se'] = {str(k): v for k, v in
                                     build_cluster_id_map(clusters).items()}
        aux['coverage_per_am']   = {str(k): v for k, v in build_coverage_map(
            os.path.join(results_dir, 'coverage_per_am.csv')).items()}
    except Exception as _e:
        # Aux data is best-effort — don't break the viewer if it fails.
        print(f'  [3d-data aux] {_e}')

    return jsonify({
        'particles': particles,
        'box': box,
        'percolation': percolation,
        'paths': paths,
        'clusters': clusters,
        'mesh_triangles': mesh_triangles,
        'atoms_only': atoms_only_mode,
        'aux': aux,
    })

@app.route('/toggle-warning/<case_id>', methods=['POST'])
def toggle_warning(case_id):
    """Toggle a warning on/off in full_metrics.json."""
    data = request.get_json()
    warn_type = data.get('warning_type', '')
    if not warn_type:
        return jsonify({'error': 'No warning type'}), 400

    # Try dashboard results first, then archive
    metrics_path = os.path.join(get_results_dir(case_id), 'full_metrics.json')
    if case_id.startswith('archive:'):
        archive_rel = case_id[len('archive:'):]
        target = _safe_path(archive_rel)
        if target:
            metrics_path = os.path.join(target, 'full_metrics.json')

    if not os.path.exists(metrics_path):
        return jsonify({'error': 'Metrics not found'}), 404

    with open(metrics_path) as f:
        metrics = json.load(f)

    disabled = metrics.get('disabled_warnings', [])
    if warn_type in disabled:
        disabled.remove(warn_type)
        is_disabled = False
    else:
        disabled.append(warn_type)
        is_disabled = True
    metrics['disabled_warnings'] = disabled

    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2, default=str)

    return jsonify({'success': True, 'disabled': is_disabled})


@app.route('/results/<case_id>/save-screenshot', methods=['POST'])
def save_screenshot(case_id):
    """Save 3D viewer screenshot to figures folder."""
    import base64
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({'error': 'No image data'}), 400
    figures_dir = os.path.join(get_results_dir(case_id), 'figures')
    os.makedirs(figures_dir, exist_ok=True)
    filename = data.get('filename', 'screenshot.png')
    filename = filename.replace('/', '_').replace('\\', '_')
    img_data = data['image'].split(',')[1]  # strip data:image/png;base64,
    with open(os.path.join(figures_dir, filename), 'wb') as f:
        f.write(base64.b64decode(img_data))
    return jsonify({'success': True, 'filename': filename})


@app.route('/results/<case_id>/force-chains')
def serve_force_chains(case_id):
    """Serve force chain data for 3D viewer."""
    results_dir = get_results_dir(case_id)
    fc_path = os.path.join(results_dir, 'force_chains.json')
    if os.path.exists(fc_path):
        with open(fc_path) as f:
            return jsonify(json.load(f))
    return jsonify([])

@app.route('/results/<case_id>/report')
def serve_report(case_id):
    """Generate comprehensive MD report v2.0 from analysis results."""
    import pandas as pd
    results_dir = get_results_dir(case_id)
    case_dir = get_case_dir(case_id)
    meta_file = os.path.join(case_dir, 'meta.json')

    meta = {}
    if os.path.exists(meta_file):
        with open(meta_file) as f:
            meta = json.load(f)

    metrics = {}
    metrics_path = os.path.join(results_dir, 'full_metrics.json')
    if os.path.exists(metrics_path):
        with open(metrics_path) as f:
            metrics = json.load(f)

    input_params = {}
    params_path = os.path.join(results_dir, 'input_params.json')
    if os.path.exists(params_path):
        with open(params_path) as f:
            input_params = json.load(f)

    name = meta.get('name', case_id)
    now = datetime.now().strftime('%y%m%d')
    L = []

    # Header
    L.append(f'# DEM Analysis Report: {name}')
    L.append(f'> DEM Analyzer v2.0 | {datetime.now().strftime("%Y-%m-%d")}')
    L.append('')
    L.append('| Parameter | Value |')
    L.append('|-----------|-------|')
    L.append(f'| Mode | {meta.get("mode", "-")} |')
    if metrics.get('ps_ratio'):
        L.append(f'| P:S ratio | {metrics["ps_ratio"]} |')
    if input_params.get('am_se_ratio'):
        L.append(f'| AM:SE ratio | {input_params["am_se_ratio"]} |')
    if metrics.get('thickness_um'):
        L.append(f'| Thickness | {metrics["thickness_um"]:.1f} μm |')
    if metrics.get('porosity'):
        L.append(f'| Porosity | {metrics["porosity"]:.1f}% |')
    if input_params.get('target_press_sim'):
        L.append(f'| Target Pressure | {input_params["target_press_sim"] * 1000:.1f} MPa |')
    L.append('')
    L.append('---\n')

    section = 1

    # ── 구조/접촉 ──
    L.append(f'## {section}. Structure & Contact\n')
    struct_items = [
        ('SE-SE CN', metrics.get('se_se_cn')),
        ('SE-SE CN std', metrics.get('se_se_cn_std')),
        ('AM-SE CN', metrics.get('am_se_cn_mean')),
        ('AM-AM CN', metrics.get('am_am_cn')),
        ('SE Volume Fraction', metrics.get('phi_se')),
        ('AM Volume Fraction', metrics.get('phi_am')),
    ]
    for label, val in struct_items:
        if val is not None:
            L.append(f'- **{label}**: {val:.3f}' if isinstance(val, float) else f'- **{label}**: {val}')
    L.append('')
    section += 1

    # ── Percolation & Tortuosity ──
    L.append(f'## {section}. Percolation & Tortuosity\n')
    perc_items = [
        ('SE Percolation', metrics.get('percolation_pct'), '%'),
        ('Top Reachable', metrics.get('top_reachable_pct'), '%'),
        ('Ionic Active AM', metrics.get('ionic_active_pct'), '%'),
        ('Tortuosity (mean)', metrics.get('tortuosity_mean'), ''),
        ('Tortuosity (median)', metrics.get('tortuosity_median'), ''),
        ('Tortuosity (std)', metrics.get('tortuosity_std'), ''),
        ('GB Density', metrics.get('gb_density_mean'), ' hops/μm'),
    ]
    for label, val, unit in perc_items:
        if val is not None:
            L.append(f'- **{label}**: {val:.2f}{unit}' if isinstance(val, float) else f'- **{label}**: {val}{unit}')
    L.append('')
    section += 1

    # ── Ionic Conductivity ──
    L.append(f'## {section}. Ionic Conductivity\n')
    sigma_ratio = metrics.get('sigma_ratio')
    sigma_brug = sigma_ratio * 3.0 if sigma_ratio else None
    sigma_net = metrics.get('sigma_full_mScm')

    L.append('### Bruggeman Estimate (접촉 저항 무시)')
    L.append('```')
    L.append('σ_Bruggeman = σ_grain × φ_SE × f_perc / τ²')
    if sigma_ratio and metrics.get('phi_se') and metrics.get('tortuosity_mean'):
        tau = metrics.get('tortuosity_recommended', metrics.get('tortuosity_mean', 1))
        f_perc = metrics.get('percolation_pct', 100) / 100
        L.append(f'           = 3.0 × {metrics["phi_se"]:.3f} × {f_perc:.3f} / {tau:.2f}²')
        L.append(f'           = {sigma_brug:.4f} mS/cm')
    L.append('```')
    L.append('')

    if sigma_net:
        L.append('### Network Solver (Ground Truth)')
        L.append('```')
        L.append(f'σ_ionic = {sigma_net:.4f} mS/cm  (Kirchhoff solver, Holm 1967)')
        L.append(f'σ_brug / σ_ionic = {sigma_brug/sigma_net:.1f}×  (Bruggeman overestimation)' if sigma_brug else '')
        if metrics.get('bulk_resistance_fraction'):
            L.append(f'Constriction fraction = {(1-metrics["bulk_resistance_fraction"])*100:.1f}%')
        L.append('```')
        L.append('')
    section += 1

    # ── Electronic Conductivity ──
    sigma_el = metrics.get('electronic_sigma_full_mScm')
    if sigma_el is not None:
        L.append(f'## {section}. Electronic Conductivity\n')
        L.append(f'- **σ_electronic**: {sigma_el:.2f} mS/cm')
        if metrics.get('electronic_percolating_fraction') is not None:
            L.append(f'- **AM Percolation**: {metrics["electronic_percolating_fraction"]*100:.1f}%')
        if metrics.get('electronic_active_fraction') is not None:
            L.append(f'- **Electronic Active AM**: {metrics["electronic_active_fraction"]*100:.1f}%')
            dead = (1 - metrics['electronic_active_fraction']) * 100
            if dead > 10:
                L.append(f'- **Dead AM**: {dead:.1f}% → 도전재 추가 검토 필요')
        L.append('')
        section += 1

    # ── Thermal Conductivity ──
    sigma_th = metrics.get('thermal_sigma_full_mScm')
    if sigma_th is not None:
        L.append(f'## {section}. Thermal Conductivity\n')
        L.append(f'- **σ_thermal**: {sigma_th:.3f} mS/cm equiv')
        L.append('')
        section += 1

    # ── Stress ──
    if metrics.get('stress_cv'):
        L.append(f'## {section}. Mechanical Stress\n')
        L.append(f'- **Stress CV**: {metrics["stress_cv"]:.1f}%')
        for key in ['sigma_AM_P_ratio', 'sigma_AM_S_ratio', 'sigma_SE_ratio']:
            val = metrics.get(key)
            if val:
                label = key.replace('sigma_', 'σ_').replace('_ratio', '/σ_mean')
                L.append(f'- **{label}**: {val:.3f}')
        L.append('')
        section += 1

    # ── Warnings ──
    warnings = metrics.get('warnings', [])
    if warnings:
        L.append(f'## {section}. Warnings\n')
        for w in warnings:
            icon = '🔴' if w.get('severity') == 'critical' else '🟡'
            L.append(f'- {icon} {w.get("msg", "")}')
        L.append('')
        section += 1

    # ── Scaling Law Predictions ──
    L.append(f'## {section}. Scaling Law Reference\n')
    L.append('| Formula | R² |')
    L.append('|---------|-----|')
    L.append('| σ_ion = σ_brug × C × (G_path × GB_d²)^(1/4) × CN² | 0.947 |')
    L.append('| σ_el = 0.015 × σ_AM × φ_AM^(3/2) × CN_AM² × exp(π/(T/d)) | 0.89 |')
    L.append('| σ_th = 286 × σ_ion^(3/4) × φ_AM² / CN_SE | 0.90 |')
    L.append('')

    L.append('---\n')
    L.append('*Generated by DEM Analyzer v2.0 — Kirchhoff Network Solver + Physics Scaling Laws*\n')

    report = '\n'.join(L)

    # Return as downloadable MD
    from io import BytesIO
    fmt = request.args.get('format', 'md')
    if fmt == 'pdf':
        return _generate_pdf_report(report, name)

    buf = BytesIO(report.encode('utf-8'))
    return send_file(buf, mimetype='text/markdown', as_attachment=True,
                    download_name=f'{name}_report.md')


def _generate_pdf_report(md_text, name):
    """Convert markdown report to PDF."""
    from io import BytesIO
    try:
        import markdown
        html_body = markdown.markdown(md_text, extensions=['tables', 'fenced_code'])
    except ImportError:
        html_body = md_text.replace('\n', '<br>')

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  body {{ font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 11pt; line-height: 1.6; margin: 40px; color: #222; }}
  h1 {{ font-size: 18pt; border-bottom: 2px solid #333; padding-bottom: 6px; }}
  h2 {{ font-size: 14pt; color: #1a56db; margin-top: 24px; }}
  h3 {{ font-size: 12pt; color: #444; }}
  table {{ border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 10pt; }}
  th, td {{ border: 1px solid #ccc; padding: 6px 10px; text-align: left; }}
  th {{ background: #f0f4ff; font-weight: 600; }}
  code, pre {{ background: #f5f5f5; padding: 2px 6px; border-radius: 3px; font-size: 10pt; }}
  pre {{ padding: 12px; overflow-x: auto; }}
  blockquote {{ border-left: 3px solid #1a56db; padding-left: 12px; color: #555; margin: 8px 0; }}
  hr {{ border: none; border-top: 1px solid #ddd; margin: 20px 0; }}
  ul {{ padding-left: 20px; }}
  li {{ margin: 3px 0; }}
</style>
</head><body>{html_body}</body></html>"""

    # Try weasyprint first, fallback to HTML download
    try:
        from weasyprint import HTML
        pdf_buf = BytesIO()
        HTML(string=html).write_pdf(pdf_buf)
        pdf_buf.seek(0)
        return send_file(pdf_buf, mimetype='application/pdf', as_attachment=True,
                        download_name=f'{name}_report.pdf')
    except ImportError:
        # Fallback: return HTML (browser can print to PDF)
        buf = BytesIO(html.encode('utf-8'))
        return send_file(buf, mimetype='text/html', as_attachment=True,
                        download_name=f'{name}_report.html')

@app.route('/download-file/<case_id>/<filename>')
def download_case_file(case_id, filename):
    """Download an uploaded file from a case."""
    case_dir = get_case_dir(case_id)
    return send_from_directory(case_dir, filename, as_attachment=True)

@app.route('/rename/<case_id>', methods=['POST'])
def rename_case(case_id):
    """Rename a case."""
    new_name = request.form.get('name', '').strip()
    if not new_name:
        return jsonify({'error': '이름을 입력하세요.'}), 400
    case_dir = get_case_dir(case_id)
    meta_file = os.path.join(case_dir, 'meta.json')
    if not os.path.exists(meta_file):
        return jsonify({'error': '케이스를 찾을 수 없습니다.'}), 404
    with open(meta_file) as f:
        meta = json.load(f)
    meta['name'] = new_name
    with open(meta_file, 'w') as f:
        json.dump(meta, f, indent=2)
    storage_sync.upload_file(f'uploads/{case_id}/meta.json', meta_file)
    return jsonify({'success': True})

@app.route('/favorite/<case_id>', methods=['POST'])
def toggle_favorite(case_id):
    meta_file = os.path.join(get_case_dir(case_id), 'meta.json')
    if not os.path.exists(meta_file):
        return jsonify({'success': False}), 404
    with open(meta_file) as f:
        meta = json.load(f)
    meta['favorite'] = not meta.get('favorite', False)
    with open(meta_file, 'w') as f:
        json.dump(meta, f, indent=2)
    return jsonify({'success': True, 'favorite': meta['favorite']})

@app.route('/delete/<case_id>', methods=['POST'])
def delete_case(case_id):
    case_dir = get_case_dir(case_id)
    results_dir = get_results_dir(case_id)
    if os.path.exists(case_dir):
        shutil.rmtree(case_dir)
    if os.path.exists(results_dir):
        shutil.rmtree(results_dir)
    storage_sync.delete_prefix(f'uploads/{case_id}')
    storage_sync.delete_prefix(f'results/{case_id}')
    return jsonify({'success': True})

# ─── Archive (보관함) ───────────────────────────────────────────────────────

def _archive_root():
    return app.config['ARCHIVE_FOLDER']

def _safe_path(rel):
    """Prevent path traversal.

    BUG FIX: the old `startswith(base)` check accepted siblings like
    `<base_parent>/archive_evil/...` when the archive root is e.g.
    `/app/archive` — `/app/archive_evil/secret` also starts with the
    base string. Anchor the boundary to `base + os.sep` (or require
    exact equality) so only true descendants are allowed.
    """
    base = os.path.realpath(_archive_root())
    target = os.path.realpath(os.path.join(base, rel))
    if target != base and not target.startswith(base + os.sep):
        return None
    return target

def _scan_folder(abs_path, rel_prefix=''):
    """Recursively scan a folder and return tree structure."""
    items = []
    if not os.path.isdir(abs_path):
        return items
    for name in sorted(os.listdir(abs_path)):
        full = os.path.join(abs_path, name)
        rel = os.path.join(rel_prefix, name) if rel_prefix else name
        if os.path.isdir(full):
            children = _scan_folder(full, rel)
            file_count = sum(1 for c in children if c['type'] == 'file') + \
                         sum(c.get('file_count', 0) for c in children if c['type'] == 'folder')
            items.append({
                'type': 'folder', 'name': name, 'path': rel,
                'children': children, 'file_count': file_count
            })
        else:
            size = os.path.getsize(full)
            items.append({
                'type': 'file', 'name': name, 'path': rel,
                'size': size, 'ext': os.path.splitext(name)[1].lower()
            })
    return items

@app.route('/archive')
def archive():
    tree = _scan_folder(_archive_root())
    current = request.args.get('folder', '')
    # List files in current folder
    if current:
        target = _safe_path(current)
        if not target or not os.path.isdir(target):
            current = ''
    folder_path = _safe_path(current) if current else _archive_root()
    files = []
    folders = []
    for name in sorted(os.listdir(folder_path)):
        full = os.path.join(folder_path, name)
        rel = os.path.join(current, name) if current else name
        if os.path.isdir(full):
            cnt = len([f for f in os.listdir(full) if os.path.isfile(os.path.join(full, f))])
            sub = len([f for f in os.listdir(full) if os.path.isdir(os.path.join(full, f))])
            has_metrics = os.path.exists(os.path.join(full, 'full_metrics.json'))
            folders.append({'name': name, 'path': rel, 'file_count': cnt, 'subfolder_count': sub,
                           'has_metrics': has_metrics})
        else:
            size = os.path.getsize(full)
            files.append({'name': name, 'path': rel, 'size': size,
                         'ext': os.path.splitext(name)[1].lower()})

    # Sort: 0-file folders first, then by name
    folders.sort(key=lambda f: (0 if f['file_count'] == 0 and f['subfolder_count'] == 0 else 1, f['name']))

    # Breadcrumb
    breadcrumb = []
    if current:
        parts = current.split(os.sep)
        for i, p in enumerate(parts):
            breadcrumb.append({'name': p, 'path': os.sep.join(parts[:i+1])})

    return render_template('archive.html', tree=tree, folders=folders, files=files,
                         current=current, breadcrumb=breadcrumb)

@app.route('/archive/create-folder', methods=['POST'])
def archive_create_folder():
    parent = request.form.get('parent', '')
    name = request.form.get('name', '').strip()
    if not name:
        return jsonify({'error': '폴더 이름을 입력하세요.'}), 400
    # Sanitize
    name = name.replace('/', '_').replace('\\', '_').replace('..', '')
    base = _safe_path(parent) if parent else _archive_root()
    if not base:
        return jsonify({'error': '잘못된 경로입니다.'}), 400
    target = os.path.join(base, name)
    os.makedirs(target, exist_ok=True)
    return jsonify({'success': True, 'path': os.path.join(parent, name) if parent else name})

@app.route('/archive/delete', methods=['POST'])
def archive_delete():
    path = request.form.get('path', '')
    target = _safe_path(path)
    if not target or target == os.path.realpath(_archive_root()):
        return jsonify({'error': '삭제할 수 없습니다.'}), 400
    rel = os.path.relpath(target, app.config['ARCHIVE_FOLDER'])
    if os.path.isdir(target):
        storage_sync.delete_prefix(f'archive/{rel}')
        shutil.rmtree(target)
    elif os.path.isfile(target):
        storage_sync.delete_path(f'archive/{rel}')
        os.remove(target)
    return jsonify({'success': True})

@app.route('/archive/rename', methods=['POST'])
def archive_rename():
    old_path = request.form.get('path', '')
    new_name = request.form.get('new_name', '').strip()
    if not new_name:
        return jsonify({'error': '새 이름을 입력하세요.'}), 400
    new_name = new_name.replace('/', '_').replace('\\', '_').replace('..', '')
    target = _safe_path(old_path)
    if not target:
        return jsonify({'error': '잘못된 경로입니다.'}), 400
    parent = os.path.dirname(target)
    new_full = os.path.join(parent, new_name)
    os.rename(target, new_full)
    return jsonify({'success': True})

@app.route('/archive/move', methods=['POST'])
def archive_move():
    src = request.form.get('src', '')
    dst_folder = request.form.get('dst', '')
    src_full = _safe_path(src)
    dst_full = _safe_path(dst_folder) if dst_folder else _archive_root()
    if not src_full or not dst_full:
        return jsonify({'error': '잘못된 경로입니다.'}), 400
    name = os.path.basename(src_full)
    shutil.move(src_full, os.path.join(dst_full, name))
    return jsonify({'success': True})

@app.route('/archive/folders-list')
def archive_folders_list():
    """Return list of archive folder names for save dialog."""
    root = _archive_root()
    folders = []
    if os.path.isdir(root):
        for name in sorted(os.listdir(root)):
            if os.path.isdir(os.path.join(root, name)):
                folders.append(name)
    return jsonify({'folders': folders})

@app.route('/archive/save-case', methods=['POST'])
def archive_save_case():
    """Save a case's results to archive folder."""
    case_id = request.form.get('case_id', '')
    folder = request.form.get('folder', '')
    results_dir = get_results_dir(case_id)
    case_dir = get_case_dir(case_id)
    meta_file = os.path.join(case_dir, 'meta.json')

    if not os.path.exists(meta_file):
        return jsonify({'error': '케이스를 찾을 수 없습니다.'}), 404

    with open(meta_file) as f:
        meta = json.load(f)

    case_name = meta.get('name', case_id)
    dst = _safe_path(folder) if folder else _archive_root()
    if not dst:
        return jsonify({'error': '잘못된 경로입니다.'}), 400

    save_dir = os.path.join(dst, case_name)
    if os.path.exists(save_dir):
        save_dir = save_dir + '_' + datetime.now().strftime('%H%M%S')
    shutil.copytree(results_dir, save_dir, dirs_exist_ok=True)
    # Also copy meta
    shutil.copy2(meta_file, os.path.join(save_dir, 'meta.json'))
    # Also copy original uploaded files (atom, contact, mesh, input .liggghts)
    raw_dir = os.path.join(save_dir, 'raw_files')
    os.makedirs(raw_dir, exist_ok=True)
    for fname in os.listdir(case_dir):
        fpath = os.path.join(case_dir, fname)
        if os.path.isfile(fpath) and fname != 'meta.json':
            shutil.copy2(fpath, os.path.join(raw_dir, fname))
    # Sync archive to Supabase
    rel = os.path.relpath(save_dir, app.config['ARCHIVE_FOLDER'])
    storage_sync.sync_dir_to_remote(save_dir, f'archive/{rel}')
    return jsonify({'success': True, 'saved_to': save_dir})

@app.route('/archive/reanalyze/<path:folder>', methods=['POST'])
def archive_reanalyze(folder):
    """Re-run analysis on an archive case using raw_files."""
    target = _safe_path(folder)
    if not target or not os.path.isdir(target):
        return jsonify({'error': 'Not found'}), 404

    meta_file = os.path.join(target, 'meta.json')
    if not os.path.exists(meta_file):
        return jsonify({'error': 'No meta.json'}), 404

    with open(meta_file) as f:
        meta = json.load(f)

    # Find source files: raw_files/ or directly in folder
    raw_dir = os.path.join(target, 'raw_files')
    source_dir = raw_dir if os.path.isdir(raw_dir) else target

    atom_files = sorted(globmod.glob(os.path.join(source_dir, 'atom*.liggghts')))
    contact_files = sorted(globmod.glob(os.path.join(source_dir, 'contact*.liggghts')))
    mesh_files = sorted(globmod.glob(os.path.join(source_dir, '*.stl')))
    input_files = sorted(globmod.glob(os.path.join(source_dir, 'input*.liggghts')))

    if not atom_files or not contact_files:
        return jsonify({'error': 'No atom/contact files in raw_files/'}), 400

    # Write a status file for polling
    status_file = os.path.join(target, '.reanalyze_status')
    with open(status_file, 'w') as f:
        f.write('running')

    def _run():
        scripts = app.config['SCRIPTS_FOLDER']
        mode = meta.get('mode', 'standard')
        type_map = meta.get('type_map', '1:AM,2:SE')
        scale = meta.get('scale', 1000)

        for pyc in globmod.glob(os.path.join(scripts, '__pycache__', '*.pyc')):
            os.remove(pyc)

        cmd = ['python3', os.path.join(scripts, 'parse_liggghts.py')]
        cmd += atom_files + contact_files + mesh_files + input_files + ['-o', target]
        subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        atoms_csv = os.path.join(target, 'atoms.csv')
        contacts_csv = os.path.join(target, 'contacts.csv')
        script = 'analyze_contacts_bimodal.py' if mode == 'bimodal' else 'analyze_contacts.py'
        cmd = ['python3', os.path.join(scripts, script),
               atoms_csv, contacts_csv, '-o', target,
               '-t', type_map, '-s', str(scale)]
        subprocess.run(cmd, capture_output=True, text=True, timeout=600)

        # Dual-mode (Hertzian vs Physics) coverage + path-hop metrics.
        # Uses --case-dir because archive layouts can be nested under
        # webapp/archive/<category>/<case>, so find_case_dir(basename) may fail.
        cmd = ['python3', os.path.join(scripts, 'coverage_physics_vs_hertzian.py'),
               '--case-dir', target]
        subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        with open(status_file, 'w') as f:
            f.write('done')

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
    return jsonify({'success': True, 'status': 'running'})


@app.route('/archive/reanalyze-status/<path:folder>')
def archive_reanalyze_status(folder):
    target = _safe_path(folder)
    if not target:
        return jsonify({'status': 'unknown'})
    status_file = os.path.join(target, '.reanalyze_status')
    if os.path.exists(status_file):
        with open(status_file) as f:
            return jsonify({'status': f.read().strip()})
    return jsonify({'status': 'done'})


@app.route('/archive/view/<path:folder>')
def archive_view(folder):
    """View archive case results like single page."""
    import pandas as pd
    target = _safe_path(folder)
    if not target or not os.path.isdir(target):
        return redirect(url_for('archive'))

    results_dir = target
    case_name = os.path.basename(folder)

    # Load meta
    meta = {'name': case_name, 'mode': 'unknown', 'status': 'done'}
    meta_file = os.path.join(results_dir, 'meta.json')
    if os.path.exists(meta_file):
        with open(meta_file) as f:
            meta = json.load(f)
    meta['id'] = f'archive:{folder}'
    meta['name'] = meta.get('name', case_name)

    # Figures
    figures = []
    figures_dir = os.path.join(results_dir, 'figures')
    if os.path.isdir(figures_dir):
        for png in sorted(globmod.glob(os.path.join(figures_dir, '*.png'))):
            figures.append(os.path.basename(png))

    # Report
    report = ''
    report_path = os.path.join(results_dir, 'report.md')
    if os.path.exists(report_path):
        with open(report_path) as f:
            report = f.read()

    # CSVs
    tables = {}
    for csv_name in ['atom_statistics', 'contact_summary', 'coordination_summary', 'network_summary']:
        csv_path = os.path.join(results_dir, f'{csv_name}.csv')
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            tables[csv_name] = {'columns': df.columns.tolist(), 'data': df.values.tolist()}

    # Metrics
    metrics = {}
    metrics_path = os.path.join(results_dir, 'full_metrics.json')
    if os.path.exists(metrics_path):
        with open(metrics_path) as f:
            metrics = json.load(f)

    # Patch placeholder '-' values from full_metrics.json BEFORE 4-col transform
    if 'network_summary' in tables and metrics:
        n_large = metrics.get('n_large_components')
        if n_large is not None:
            for row in tables['network_summary']['data']:
                if str(row[0]) == 'SE Cluster 수' and '≥10' not in str(row[1]):
                    row[1] = f"{n_large}(≥10) / {row[1]}"
        placeholder_map = {
            'GB Density(hops/μm)': 'gb_density_mean',
            'Path Hop Area mean(μm²)': 'path_hop_area_mean',
            'Path Bottleneck(μm²)': 'path_hop_area_min_mean',
            'Path Conductance(μm²)': 'path_conductance_mean',
        }
        for row in tables['network_summary']['data']:
            label = str(row[0])
            if label in placeholder_map and str(row[1]).strip() in ('-', ''):
                val = metrics.get(placeholder_map[label])
                if val is not None:
                    row[1] = val

    # 4-column transform + section injection (Network Solver + AM-AM) — shared helper
    transform_network_summary_4col(tables, metrics, meta)

    # Brittle-fracture summary tab (built from full_metrics.json keys produced
    # by dem_analysis_core.calc_fracture_stages — auto-DB pipeline). Empty
    # for cases without AM-AM contacts; UI hides the tab when None.
    fracture_tbl = build_fracture_summary_table(metrics)
    if fracture_tbl is not None:
        tables['fracture_summary'] = fracture_tbl

    input_params = {}
    params_path = os.path.join(results_dir, 'input_params.json')
    if os.path.exists(params_path):
        with open(params_path) as f:
            input_params = json.load(f)

    return render_template('single.html', case=meta, figures=figures,
                         report=report, tables=tables, metrics=metrics,
                         input_params=input_params, archive_path=folder)


@app.route('/archive/results/<path:folder>/figures/<filename>')
def serve_archive_figure(folder, filename):
    target = _safe_path(os.path.join(folder, 'figures'))
    if not target:
        return 'Not found', 404
    return send_from_directory(target, filename)


@app.route('/archive/results/<path:folder>/3d-data')
def serve_archive_3d_data(folder):
    """Serve 3D data for archive case."""
    import pandas as pd
    target = _safe_path(folder)
    if not target:
        return jsonify({'error': 'Not found'}), 404

    meta = {}
    meta_file = os.path.join(target, 'meta.json')
    if os.path.exists(meta_file):
        with open(meta_file) as f:
            meta = json.load(f)
    scale = meta.get('scale', 1000)
    type_map_str = meta.get('type_map', '1:AM,2:SE')
    type_map = {}
    for item in type_map_str.split(','):
        k, v = item.split(':')
        type_map[int(k)] = v.strip()

    atoms_csv = os.path.join(target, 'atoms.csv')
    if not os.path.exists(atoms_csv):
        return jsonify({'error': 'No atom data'}), 404

    contacts_csv = os.path.join(target, 'contacts.csv')
    atoms_only_mode = not os.path.exists(contacts_csv)
    fm_path = os.path.join(target, 'full_metrics.json')
    if os.path.exists(fm_path):
        try:
            with open(fm_path) as f:
                _fm = json.load(f)
            if _fm.get('has_contacts') is False:
                atoms_only_mode = True
        except Exception:
            pass

    df = pd.read_csv(atoms_csv)
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    particles = []
    for _, row in df.iterrows():
        t = int(row['type'])
        particles.append({
            'id': int(row['id']),
            'type': type_map.get(t, f'T{t}'),
            'x': round(float(row['x']) * scale, 2),
            'y': round(float(row['y']) * scale, 2),
            'z': round(float(row['z']) * scale, 2),
            'r': round(float(row['radius']) * scale, 2),
        })

    # Box bounds from input_params.json
    _box_x, _box_y = 0.05, 0.05
    _ip_path = os.path.join(target, 'input_params.json')
    if os.path.exists(_ip_path):
        with open(_ip_path) as f:
            _ip = json.load(f)
        _box_x = _ip.get('box_x', 0.05)
        _box_y = _ip.get('box_y', 0.05)
    box = {
        'x_min': 0, 'x_max': round(_box_x * scale, 1),
        'y_min': 0, 'y_max': round(_box_y * scale, 1),
        'z_min': 0,
    }
    particle_z_top = max(p['z'] + p['r'] for p in particles) if particles else 0
    mesh_file = os.path.join(target, 'mesh_info.json')
    mesh_triangles = []
    if os.path.exists(mesh_file):
        try:
            with open(mesh_file) as f:
                _mesh_data = json.load(f)
            plate_z_mesh = _mesh_data['plate_z'] * scale
            box['z_max'] = round(min(plate_z_mesh, particle_z_top), 1)
            for tri in _mesh_data.get('triangles', []):
                mesh_triangles.append([
                    [round(v[0] * scale, 3), round(v[1] * scale, 3), round(v[2] * scale, 3)]
                    for v in tri
                ])
        except Exception:
            box['z_max'] = round(particle_z_top, 1)
    else:
        box['z_max'] = round(particle_z_top, 1)

    percolation = {'top_reachable': [], 'bottom_se': [], 'top_se': []}
    perc_path = os.path.join(target, 'percolation_sets.json')
    if os.path.exists(perc_path):
        with open(perc_path) as f:
            percolation = json.load(f)

    paths = []
    paths_path = os.path.join(target, 'tortuosity_paths.json')
    if os.path.exists(paths_path):
        with open(paths_path) as f:
            paths = json.load(f)

    clusters = {}
    clusters_path = os.path.join(target, 'se_clusters.json')
    if os.path.exists(clusters_path):
        with open(clusters_path) as f:
            clusters = json.load(f)

    # ── Auxiliary data for new view modes (mirrors /results/<id>/3d-data) ──
    aux = {
        'stress_max': {}, 'dr_max': {},
        'brittle_pairs': [], 'se_stress_pairs': [],
        'cluster_meta': {}, 'cluster_id_per_se': {},
        'coverage_per_am': {},
    }
    try:
        import sys as _sys
        _scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
        if _scripts_dir not in _sys.path:
            _sys.path.insert(0, _scripts_dir)
        from viewer3d_data import (
            aggregate_particle_metrics, classify_clusters,
            build_cluster_id_map, build_coverage_map,
        )
        atoms_by_id = {int(r['id']): {
            'type':   int(r['type']),
            'radius': float(r['radius']),
        } for _, r in df.iterrows()}
        if os.path.exists(contacts_csv):
            contacts_df = pd.read_csv(contacts_csv, low_memory=False)
            agg = aggregate_particle_metrics(
                contacts_df.to_dict('records'),
                atoms_by_id, type_map, scale=scale)
            aux['stress_max']      = agg['stress_max']
            aux['dr_max']          = agg['dr_max']
            aux['brittle_pairs']   = agg['brittle_pairs']
            aux['se_stress_pairs'] = agg['se_stress_pairs']
        aux['cluster_meta']      = classify_clusters(clusters)
        aux['cluster_id_per_se'] = {str(k): v for k, v in
                                     build_cluster_id_map(clusters).items()}
        aux['coverage_per_am']   = {str(k): v for k, v in build_coverage_map(
            os.path.join(target, 'coverage_per_am.csv')).items()}
    except Exception as _e:
        print(f'  [3d-data aux/archive] {_e}')

    return jsonify({
        'particles': particles, 'box': box,
        'percolation': percolation, 'paths': paths, 'clusters': clusters,
        'mesh_triangles': mesh_triangles,
        'atoms_only': atoms_only_mode,
        'aux': aux,
    })


@app.route('/archive/results/<path:folder>/save-screenshot', methods=['POST'])
def archive_save_screenshot(folder):
    """Save 3D screenshot to archive figures folder."""
    import base64
    target = _safe_path(folder)
    if not target:
        return jsonify({'error': 'Not found'}), 404
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({'error': 'No image data'}), 400
    figures_dir = os.path.join(target, 'figures')
    os.makedirs(figures_dir, exist_ok=True)
    filename = data.get('filename', 'screenshot.png')
    filename = filename.replace('/', '_').replace('\\', '_')
    img_data = data['image'].split(',')[1]
    with open(os.path.join(figures_dir, filename), 'wb') as f:
        f.write(base64.b64decode(img_data))
    return jsonify({'success': True, 'filename': filename})


@app.route('/archive/results/<path:folder>/force-chains')
def serve_archive_force_chains(folder):
    target = _safe_path(folder)
    if not target:
        return jsonify([])
    fc_path = os.path.join(target, 'force_chains.json')
    if os.path.exists(fc_path):
        with open(fc_path) as f:
            return jsonify(json.load(f))
    return jsonify([])


@app.route('/archive/download/<path:filepath>')
def archive_download(filepath):
    target = _safe_path(filepath)
    if not target or not os.path.isfile(target):
        return 'File not found', 404
    return send_file(target, as_attachment=True)

@app.route('/archive/preview/<path:filepath>')
def archive_preview(filepath):
    target = _safe_path(filepath)
    if not target or not os.path.isfile(target):
        return 'File not found', 404
    ext = os.path.splitext(target)[1].lower()
    if ext == '.md':
        with open(target) as f:
            content = f.read()
        return jsonify({'type': 'markdown', 'content': content})
    elif ext == '.csv':
        import pandas as pd
        df = pd.read_csv(target)
        return jsonify({'type': 'csv', 'columns': df.columns.tolist(),
                       'data': df.head(100).values.tolist()})
    elif ext == '.png':
        return send_file(target, mimetype='image/png')
    elif ext == '.json':
        with open(target) as f:
            content = f.read()
        return jsonify({'type': 'json', 'content': content})
    return jsonify({'type': 'unknown', 'message': '미리보기를 지원하지 않는 파일 형식입니다.'})

@app.route('/download-doc/<path:filename>')
def download_doc(filename):
    """Download documentation files from project root."""
    doc_dir = os.path.dirname(os.path.dirname(__file__))
    return send_from_directory(doc_dir, filename, as_attachment=True)


@app.route('/group/fitting-report', methods=['POST'])
def group_fitting_report():
    """Generate GB correction fitting analysis report (downloadable MD)."""
    selected = request.form.getlist('cases')
    if not selected:
        return jsonify({'error': '케이스를 선택하세요.'}), 400

    # Collect metrics
    input_files = []
    names = []
    for cid in selected:
        if cid.startswith('archive:'):
            archive_rel = cid[len('archive:'):]
            case_path = os.path.join(app.config['ARCHIVE_FOLDER'], archive_rel)
            metrics_path = os.path.join(case_path, 'full_metrics.json')
            case_name = os.path.basename(archive_rel)
        else:
            case_path = get_results_dir(cid)
            metrics_path = os.path.join(case_path, 'full_metrics.json')
            meta_file = os.path.join(get_case_dir(cid), 'meta.json')
            case_name = cid
            if os.path.exists(meta_file):
                with open(meta_file) as f:
                    case_name = json.load(f).get('name', cid)
        if os.path.exists(metrics_path):
            input_files.append(metrics_path)
            names.append(case_name)

    if len(input_files) < 3:
        return jsonify({'error': '최소 3개 케이스가 필요합니다.'}), 400

    session_id = datetime.now().strftime('%y%m%d_%H%M%S') + '_fit'
    report_dir = os.path.join(app.config['RESULTS_FOLDER'], 'fitting_reports', session_id)
    os.makedirs(report_dir, exist_ok=True)

    scripts = app.config['SCRIPTS_FOLDER']
    cmd = ['python3', os.path.join(scripts, 'generate_fitting_report.py'),
           '-i'] + input_files + ['-n'] + names + ['-o', report_dir]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

    if result.returncode != 0:
        return jsonify({'error': f'리포트 생성 실패: {result.stderr}'}), 500

    report_path = os.path.join(report_dir, 'fitting_report.md')
    if not os.path.exists(report_path):
        return jsonify({'error': '리포트 파일이 생성되지 않았습니다.'}), 500

    with open(report_path, encoding='utf-8') as f:
        content = f.read()

    return jsonify({
        'success': True,
        'content': content,
        'download_url': f'/group/fitting-report-download/{session_id}'
    })


@app.route('/group/fitting-report-download/<session_id>')
def download_fitting_report(session_id):
    """Download fitting report as markdown file."""
    report_dir = os.path.join(app.config['RESULTS_FOLDER'], 'fitting_reports', session_id)
    return send_from_directory(report_dir, 'fitting_report.md', as_attachment=True,
                              download_name='GB_correction_fitting_report.md')


@app.route('/scaling-report')
def scaling_report():
    """Generate and download scaling law report."""
    import subprocess
    scripts = app.config['SCRIPTS_FOLDER']
    cmd = ['python3', os.path.join(scripts, 'generate_scaling_report.py')]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        return jsonify({'error': result.stderr[-500:]}), 500
    report_path = os.path.join(app.config['RESULTS_FOLDER'], 'reports', 'scaling_law_report.md')
    if os.path.exists(report_path):
        return send_file(report_path, as_attachment=True,
                        download_name='Scaling_Law_Report.md')
    return jsonify({'error': 'Report generation failed'}), 500

@app.route('/docs/full-report')
def full_report():
    """Download full scaling law report."""
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'docs', 'Scaling_Law_Report_Full.md')
    if os.path.exists(path):
        return send_file(path, as_attachment=True, download_name='Scaling_Law_Report_Full.md')
    return jsonify({'error': 'Not found'}), 404

@app.route('/docs/formula-catalog')
def formula_catalog():
    """Download formula catalog."""
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'docs', 'Formula_Catalog.md')
    if os.path.exists(path):
        return send_file(path, as_attachment=True, download_name='Formula_Catalog.md')
    return jsonify({'error': 'Not found'}), 404


# ─── ML Predictor ──────────────────────────────────────────────────────────

@app.route('/predictor')
def predictor_page():
    """ML-based electrode property predictor page."""
    data_count = predictor_engine.get_data_count(
        app.config['RESULTS_FOLDER'], app.config['ARCHIVE_FOLDER'])
    models_ready = predictor_engine._cached_models is not None
    return render_template('predictor.html', active='predictor',
                           data_count=data_count, models_ready=models_ready)


@app.route('/predictor/train')
def predictor_train():
    """Train GPR models from existing data."""
    result = predictor_engine.train_models(
        app.config['RESULTS_FOLDER'], app.config['ARCHIVE_FOLDER'])
    return jsonify(result)


@app.route('/predictor/predict', methods=['POST'])
def predictor_predict():
    """Predict electrode properties from design parameters."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data'}), 400
    try:
        result = predictor_engine.predict(
            d_se=float(data.get('d_se', 1.0)),
            d_am=float(data.get('d_am', 5.0)),
            am_pct=float(data.get('am_pct', 80)),
            ps_frac=float(data.get('ps_frac', 0.5)),
            loading=float(data.get('loading', 6)),
            rve=float(data.get('rve', 50)),
            temperature=float(data.get('temperature', 298)),
            additive=data.get('additive', 'none'),
            ptfe=bool(data.get('ptfe', False)),
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/predictor/optimal')
def predictor_optimal():
    """Find optimal design by sweeping parameter space."""
    try:
        fixed = json.loads(request.args.get('fixed', '{}'))
        sweep = json.loads(request.args.get('sweep', '[]'))
        defaults = {}
        for k, v in request.args.items():
            if k in ('fixed', 'sweep'): continue
            try:
                defaults[k] = float(v)
            except (ValueError, TypeError):
                defaults[k] = v  # keep string for additive, ptfe etc.
        result = predictor_engine.sweep_optimal(
            top_n=10, fixed_params=fixed, sweep_keys=sweep if sweep else None, defaults=defaults
        )
        if isinstance(result, dict) and 'error' in result:
            return jsonify(result), 400
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/predictor/heatmap', methods=['POST'])
def predictor_heatmap():
    """Generate 2D heatmap data for two parameters vs a target."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data'}), 400
    try:
        fixed = {}
        for k in ['d_se', 'd_am', 'am_pct', 'ps_frac', 'loading', 'rve']:
            if k in data.get('fixed', {}):
                fixed[k] = float(data['fixed'][k])
        result = predictor_engine.generate_heatmap(
            x_param=data.get('x_param', 'd_se'),
            y_param=data.get('y_param', 'am_pct'),
            target=data.get('target', 'sigma_ionic'),
            fixed_params=fixed,
            n_points=int(data.get('n_points', 15)),
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/predictor/phase-diagram', methods=['POST'])
def predictor_phase_diagram():
    """Generate phase diagram with contour boundaries."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data'}), 400
    try:
        fixed = {}
        for k in ['d_se', 'd_am', 'am_pct', 'ps_frac', 'loading', 'rve']:
            if k in data.get('fixed', {}):
                fixed[k] = float(data['fixed'][k])
        result = predictor_engine.generate_phase_diagram(
            x_param=data.get('x_param', 'd_se'),
            y_param=data.get('y_param', 'am_pct'),
            fixed_params=fixed,
            n_points=int(data.get('n_points', 30)),
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/predictor/sensitivity', methods=['POST'])
def predictor_sensitivity():
    """Sensitivity analysis: vary each param +/-30%."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data'}), 400
    try:
        result = predictor_engine.sensitivity_analysis(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/predictor/pareto', methods=['POST'])
def predictor_pareto():
    """Compute Pareto front for sigma_ionic vs energy density."""
    data = request.get_json() or {}
    try:
        fixed = {}
        for k in ['d_am', 'ps_frac', 'rve']:
            if k in data:
                fixed[k] = float(data[k])
        result = predictor_engine.compute_pareto(fixed_params=fixed, n_points=int(data.get('n_points', 8)))
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/predictor/suggest')
def predictor_suggest():
    """Suggest next DEM conditions using Bayesian optimization."""
    try:
        result = predictor_engine.suggest_next(
            app.config['RESULTS_FOLDER'], app.config['ARCHIVE_FOLDER'])
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/predictor/export')
def predictor_export():
    """Export training data as CSV download."""
    try:
        csv_str = predictor_engine.export_training_csv(
            app.config['RESULTS_FOLDER'], app.config['ARCHIVE_FOLDER'])
        if not csv_str:
            return jsonify({'error': 'No training data available'}), 404
        import io
        buf = io.BytesIO(csv_str.encode('utf-8'))
        buf.seek(0)
        return send_file(buf, mimetype='text/csv', as_attachment=True,
                         download_name='predictor_training_data.csv')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
