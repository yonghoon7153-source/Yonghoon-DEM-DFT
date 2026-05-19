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
    redirect, url_for, send_file, make_response,
)
import storage_sync
import predictor_engine

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 * 1024  # 2GB max
# Disable browser caching of static assets — viewer3d.js evolves often and
# stale caches were masking server-side fixes (e.g. fracture classifier
# update reaching server but not the rendered view).
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Server start time — exposed to templates as a cache-busting version stamp
# so `?v={{ asset_version }}` on script/asset URLs invalidates on every
# Flask restart even if the browser ignored Cache-Control.
_ASSET_VERSION = str(int(datetime.now().timestamp()))


@app.context_processor
def _inject_asset_version():
    return {'asset_version': _ASSET_VERSION}


# ── Trust-card self-report (validation_flags → 5 LED dots) ────────────
# `validation_flags` is written into full_metrics.json by Stage E
# (`run_network_full_corrections._compute_validation_flags`).
# Five gates: within_bielefeld_range, fracture_distribution_realistic,
# solver_input_intact, stage_e_le_baseline_sigma_e, bruggeman_fallback_fired_any.
# This helper returns a render-ready dict for the trust-card template.
#
# Each LED definition (key) carries the rich tooltip metadata:
#   label      — text inside the LED chip
#   value_key  — which validation_flags entry holds the *measured value*
#                so the tooltip can show "ASR = 42.3 Ω·cm²" not just pass/fail
#   value_fmt  — printf-style format ('{:.2f}', or callable)
#   value_unit — appended to the formatted value
#   criterion  — pass criterion in plain English (Bielefeld envelope etc.)
#   desc_kr    — Korean one-liner explaining the gate's purpose
#   na_reason  — Korean explanation of why a gate is N/A when data is missing
#   pass_kr    — Korean explanation when gate passes
#   fail_kr    — Korean explanation when gate fails
#   ref        — paper section / reference for the gate definition
#   polarity   — 'positive' = True is pass, 'negative' = True is fail (Brugg)
_TRUST_LEDS = [
    {
        'key':       'within_bielefeld_range',
        'label':     'ASR',
        'value_key': 'asr_ionic_Ohm_cm2',
        'value_fmt': '{:.2f}',
        'value_unit': ' Ω·cm²',
        'criterion': '10 ≤ ASR ≤ 200 Ω·cm² (literature envelope)',
        'desc_kr':   'Cathode ASR가 sulfide ASSB 문헌 (Bielefeld 2022 / '
                     'Lee 2020 / Minnmann 2021) 범위 안에 있는지. '
                     'Stage E σ_ionic 의 first-line sanity check.',
        'pass_kr':   '✓ 측정값이 문헌 envelope 안에 있음 — '
                     'σ_ionic 계산이 비현실적 값으로 빠지지 않았다는 뜻.',
        'fail_kr':   '✗ ASR이 문헌 범위를 벗어남. Stage E factor가 너무 '
                     '많이 깎아냈거나 baseline σ가 비정상일 수 있음.',
        'na_reason': '두께 또는 σ_ionic 정보가 full_metrics에 없어서 '
                     'ASR 계산 불가 (대부분 baseline-only 케이스).',
        'ref':       'paper §5.2 · Bielefeld 2022 / Lee 2020 / Minnmann 2021',
        'polarity':  'positive',
    },
    {
        'key':       'fracture_distribution_realistic',
        'label':     'Frac',
        'value_key': 'fracture_severe_pct',
        'value_fmt': '{:.1f}',
        'value_unit': '% severe',
        'criterion': 'severe % ≤ 50 & ≥1 Lawn stage populated',
        'desc_kr':   '심한 fracture (fragmentation + pulverization) 비율이 '
                     '50%를 넘으면 classifier가 한 bucket으로 몰린 거. '
                     '1 GPa 압축 실험에서도 보통 40% 안 넘음.',
        'pass_kr':   '✓ Lawn 1998 cone-crack envelope 안에 있음 — '
                     'fracture classifier가 정상 분포 출력.',
        'fail_kr':   '✗ Severe fracture 비율 비정상. classifier threshold '
                     '검토 또는 contact force unit 변환 (sim → real) 확인 필요.',
        'na_reason': 'fracture_stage_counts가 비어있음 — '
                     'fracture 분석이 아직 안 돌았거나 contact 없음.',
        'ref':       'paper §5.2 · Lawn 1998',
        'polarity':  'positive',
    },
    {
        'key':       'solver_input_intact',
        'label':     'Solver',
        'value_key': 'edge_drop_ratio_e',
        'value_fmt': '{:.2%}',
        'value_unit': ' edges dropped',
        'criterion': 'edge_drop_ratio_e ≤ 0.5',
        'desc_kr':   'Stage E factor가 5% cutoff (MIN_FACTOR_CUTOFF) '
                     '아래로 떨어진 AM-AM electronic edge를 얼마나 버렸나. '
                     '절반 넘게 버리면 direct solver 대신 Bruggeman '
                     'fallback이 거의 다 하고 있다는 뜻.',
        'pass_kr':   '✓ Direct Laplacian solver가 conductance의 대부분을 '
                     '실제로 계산 — Stage E 결과 신뢰 가능.',
        'fail_kr':   '✗ Edge 절반 이상이 cutoff 아래로 깎여나감. '
                     'Bruggeman fallback이 over-active. fracture index '
                     '재검토 또는 Stage E factor 분포 조사 필요.',
        'na_reason': 'n_dropped_e 또는 n_am_am_total 메트릭 없음 — '
                     'Stage E 완전히 안 돌아간 케이스.',
        'ref':       'paper §6 · MIN_FACTOR_CUTOFF = 0.05',
        'polarity':  'positive',
    },
    {
        'key':       'stage_e_le_baseline_sigma_e',
        'label':     'σ ≤ base',
        'value_key': None,
        'value_fmt': None,
        'value_unit': '',
        'criterion': 'σ_e^(Stage E) ≤ 1.05 × σ_e^(baseline)',
        'desc_kr':   'Stage E factor가 1 이하라는 invariant (factor는 '
                     'conductance를 절대 늘릴 수 없다)가 지켜졌나. '
                     'Bruggeman fallback은 by construction 보장하지만 '
                     'direct solver 경로는 수치 오차로 약간 넘을 수 있음.',
        'pass_kr':   '✓ Factor-≤-1 invariant 유지됨 — Stage E σ가 baseline을 '
                     '넘지 않음. paper §6 Bruggeman bound 증명과 일관.',
        'fail_kr':   '✗ Stage E σ_e > baseline σ_e. 수치 불안정성 또는 '
                     'high-contrast Laplacian 발산. 7-layer 방어선 재검토.',
        'na_reason': 'Stage E σ_e 또는 baseline σ_e가 없음 — '
                     '비교 불가.',
        'ref':       'paper §6 · Bruggeman bound proof',
        'polarity':  'positive',
    },
    {
        'key':       'bruggeman_fallback_fired_any',
        'label':     'Brugg',
        'value_key': None,
        'value_fmt': None,
        'value_unit': '',
        'criterion': 'no channel fell back to EMT',
        'desc_kr':   'σ_ionic / σ_e / κ 세 channel 중 하나라도 Bruggeman '
                     'EMT fallback으로 풀렸나. Fallback은 정답을 보장하지만 '
                     'high-contrast 케이스에서 conservative한 upper-bound. '
                     'orange = EMT가 일부 채널 운반.',
        'pass_kr':   '✓ 세 channel 모두 direct Laplacian solver로 수렴 — '
                     'EMT 보정 필요 없었음.',
        'fail_kr':   '⚠ 적어도 한 channel이 Bruggeman으로 fallback. 결과는 '
                     '안전한 upper-bound이지만 direct solver 결과는 아님. '
                     'paper §6 self-report로 명시 권장.',
        'na_reason': 'stage_e_source 메트릭 없음 — Stage E 안 돌아간 케이스.',
        'ref':       'paper §6 · 7-layer defence Layer 6',
        'polarity':  'negative',  # True = fired = fail (orange)
    },
]


def _format_led_value(led_def: dict, flags: dict) -> str | None:
    """Pull the measured value for an LED's tooltip. Returns formatted
    string or None if no value tracked / data missing."""
    vk = led_def.get('value_key')
    if not vk:
        return None
    raw = flags.get(vk)
    if raw is None:
        return None
    try:
        fmt = led_def.get('value_fmt') or '{}'
        return fmt.format(raw) + led_def.get('value_unit', '')
    except (TypeError, ValueError):
        return str(raw)


def _build_trust_card(metrics: dict) -> dict | None:
    """Translate metrics['validation_flags'] into the LED + verdict
    structure consumed by the single.html template. Returns None when
    the flags block is absent so the card simply isn't rendered.

    Each LED carries a rich tooltip payload (value + criterion + Korean
    description + pass/fail one-liners + reference) so the hover surface
    on the page header is a self-contained explanation of the gate."""
    flags = (metrics or {}).get('validation_flags')
    if not isinstance(flags, dict):
        return None

    leds = []
    n_pass = n_fail = n_na = 0
    for led_def in _TRUST_LEDS:
        v = flags.get(led_def['key'])
        polarity = led_def.get('polarity', 'positive')
        if v is None:
            cls, state_kr = 'na', 'N/A · 측정 불가'
            n_na += 1
        elif (v if polarity == 'positive' else not v):
            cls, state_kr = 'pass', led_def['pass_kr']
            n_pass += 1
        else:
            cls, state_kr = 'fail', led_def['fail_kr']
            n_fail += 1

        value_str = _format_led_value(led_def, flags)
        # Build the rich tooltip payload.  Template renders this as a
        # styled <div class="trust-tip"> child of each <span class="trust-led">.
        leds.append({
            'label':     led_def['label'],
            'cls':       cls,
            'value':     value_str or '—',
            'criterion': led_def['criterion'],
            'desc_kr':   led_def['desc_kr'],
            'state_kr':  state_kr if cls != 'na' else led_def['na_reason'],
            'ref':       led_def['ref'],
        })

    # Verdict: 4 gates excluding the Bruggeman warning indicator.  Trust
    # requires all assessable gates pass; any fail flips to warn/fail.
    core_keys = ['within_bielefeld_range',
                 'fracture_distribution_realistic',
                 'solver_input_intact',
                 'stage_e_le_baseline_sigma_e']
    core_vals = [flags.get(k) for k in core_keys]
    core_fail = sum(1 for v in core_vals if v is False)
    core_assess = sum(1 for v in core_vals if v is not None)
    if core_assess == 0:
        verdict, verdict_cls = 'N/A', 'na'
        verdict_kr = ('이 케이스는 Stage E가 돌지 않아 trust gate를 평가할 '
                       '수 없습니다. Stage E를 실행하면 5-LED 카드가 활성화됩니다.')
    elif core_fail == 0:
        verdict, verdict_cls = '✓ Trust', 'trust'
        verdict_kr = (f'{core_assess}/{core_assess} core gate 통과 — '
                       'paper §5.2 trustworthy 케이스로 분류 가능.')
    elif core_fail <= 1:
        verdict, verdict_cls = '~ Warn', 'warn'
        verdict_kr = (f'{core_assess - core_fail}/{core_assess} core gate 통과 — '
                       '1개 gate 실패. 결과 사용 시 caveat 명시 권장.')
    else:
        verdict, verdict_cls = '✗ Untrust', 'fail'
        verdict_kr = (f'{core_fail}/{core_assess} core gate 실패 — '
                       '결과 신뢰 곤란. paper §5.2 audit에서 제외 권장 케이스.')

    return {
        'leds': leds,
        'verdict': verdict,
        'verdict_cls': verdict_cls,
        'verdict_kr': verdict_kr,
        'verdict_summary': (f'{core_assess - core_fail}/{core_assess} core '
                             f'gates passed'),
    }

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
    # Older b2_b4_diagnostic.py emitted only the four damage-stage shares
    # and omitted intact (which is the implicit complement). When we backfill
    # those cases, frac_intact_pct is missing → recover as 100 minus the
    # sum of the four explicit stages so the UI shows a complete distribution.
    other_d = sum(metrics.get(f'frac_{s}_pct') or 0
                  for s in ('microcrack', 'multicrack',
                            'fragmentation', 'pulverization'))
    other_f = sum(metrics.get(f'frac_{s}_force_pct') or 0
                  for s in ('microcrack', 'multicrack',
                            'fragmentation', 'pulverization'))
    # When no damage stage fraction is positive we still want to say
    # "100 % intact" *if* the case has any AM-AM contacts at all —
    # previously the UI fell back to "-" which read as missing data.
    intact_d = (metrics.get('frac_intact_pct')
                if metrics.get('frac_intact_pct') is not None
                else (round(100.0 - other_d, 2) if other_d > 0
                      else (100.0 if (n_total or 0) > 0 else None)))
    intact_f = (metrics.get('frac_intact_force_pct')
                if metrics.get('frac_intact_force_pct') is not None
                else (round(100.0 - other_f, 2) if other_f > 0
                      else (100.0 if (n_total_force or 0) > 0 else None)))

    rows.append(['── 단계별 분포 (%) ──'])
    rows.append(['  Intact', f(intact_d), f(intact_f)])
    for stage, label in [('microcrack',    'Microcrack'),
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

    # ── Per-pair-type full stage distribution (%) ──
    # b2_b4_diagnostic writes frac_{stage}_{pair}_pct and the force variant
    # frac_{stage}_force_{pair}_pct; intact% isn't stored explicitly so
    # recover it as 100 − Σ(damage stages) when at least one damage % is
    # known.  Skip pair types absent from the case (e.g. P:S = 0:10 cases
    # have no AM_P-AM_P or AM_P-AM_S contacts).
    rows.append(['── Pair-type 단계별 분포 (%) ──'])
    for pt in ('AM_P-AM_P', 'AM_P-AM_S', 'AM_S-AM_S'):
        n_pt       = metrics.get(f'n_total_{pt}')       or 0
        n_pt_force = metrics.get(f'n_total_force_{pt}') or 0
        if n_pt == 0 and n_pt_force == 0:
            continue
        rows.append([f'  [{pt}]'])
        sum_d = sum(metrics.get(f'frac_{s}_{pt}_pct') or 0
                    for s in ('microcrack', 'multicrack',
                               'fragmentation', 'pulverization'))
        sum_f = sum(metrics.get(f'frac_{s}_force_{pt}_pct') or 0
                    for s in ('microcrack', 'multicrack',
                               'fragmentation', 'pulverization'))
        intact_pt_d = (round(100.0 - sum_d, 2) if sum_d > 0 else
                        (100.0 if n_pt else None))
        intact_pt_f = (round(100.0 - sum_f, 2) if sum_f > 0 else
                        (100.0 if n_pt_force else None))
        rows.append(['    Intact',        f(intact_pt_d), f(intact_pt_f)])
        for stage, label in [('microcrack',    'Microcrack'),
                              ('multicrack',    'Multi-crack'),
                              ('fragmentation', 'Fragmentation'),
                              ('pulverization', 'Pulverization')]:
            d  = metrics.get(f'frac_{stage}_{pt}_pct')
            ff = metrics.get(f'frac_{stage}_force_{pt}_pct')
            rows.append([f'    {label}', f(d), f(ff)])

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
    keys added by the post-Auerbach analysis pipeline. ALWAYS emits the
    section + all 7 rows (— placeholder for cases predating the Tier-1
    pipeline) so every case has identical layout.

      Coverage  rough (B3 shape factor)        coverage_AM_*_mean_physics_rough
      SE-SE CN  perc-only         (F2)         se_se_cn_perc
      SE-SE CN  area-weighted     (F2)         se_se_cn_eff_area
      SE-SE CN  perc + area-w     (F2)         se_se_cn_eff_area_perc
      SE-SE CN  plastic-aug       (F1)         se_se_cn_aug (+ n_extra)
    """
    if 'network_summary' not in tables:
        return
    data = tables['network_summary']['data']
    if not isinstance(data, list):
        return

    section_label = '── Tier 1 patches (post-Auerbach refinements) ──'
    if any(isinstance(r, list) and r and r[0] == section_label for r in data):
        return  # already injected on a prior call

    metrics = metrics or {}

    def _fmt_num(v, prec):
        if v is None: return '—'
        try: return round(float(v), prec)
        except (TypeError, ValueError): return '—'

    rows: list = [[section_label, '', '', '']]

    # Rough coverage (B3 shape factor) — always emit all 3
    for label, key in [
        ('Coverage AM rough(%)   ⭐ [B3]',   'coverage_AM_mean_physics_rough'),
        ('Coverage AM_P rough(%) ⭐ [B3]', 'coverage_AM_P_mean_physics_rough'),
        ('Coverage AM_S rough(%) ⭐ [B3]', 'coverage_AM_S_mean_physics_rough'),
    ]:
        rows.append([label, '-', _fmt_num(metrics.get(key), 2), ''])

    # F2 / F1 CN variants — always emit all 4 + the F1 extras count
    cn_specs = [
        ('SE-SE CN (perc-only)        [F2]', 'se_se_cn_perc',          4),
        ('SE-SE CN (area-weighted)    [F2]', 'se_se_cn_eff_area',      4),
        ('SE-SE CN (perc area-w)      [F2]', 'se_se_cn_eff_area_perc', 4),
        ('SE-SE CN (plastic-augmented) [F1]', 'se_se_cn_aug',          3),
    ]
    for label, key, prec in cn_specs:
        rows.append([label, _fmt_num(metrics.get(key), prec), '-', ''])
    n_extra = metrics.get('se_se_cn_aug_n_extra')
    extra_str = int(n_extra) if (n_extra is not None
                                 and not isinstance(n_extra, bool)) else '—'
    rows.append(['  (F1 extra near-contact pairs)', extra_str, '-', ''])

    # Place after the existing AM-AM / 응력 section if present, else at the end
    anchor_idx = len(data)
    for i, r in enumerate(data):
        if (isinstance(r, list) and r and isinstance(r[0], str)
                and ('AM-AM' in r[0] or '응력' in r[0])):
            anchor_idx = i
            break
    for j, nr in enumerate(rows):
            data.insert(anchor_idx + j, nr)


def inject_stage_e_rows(tables, metrics):
    """Append a 'Stage E (literature-grounded grain corrections)' section
    showing the per-channel σ_grain factors applied + corrected σ values.

    Three orthogonal corrections per Cronau 2022 / Trevisanello 2021 / Wang 2022:
      σ_ionic : SE r_SE-dependent (size-invariant ≥ 0.3 μm in our range)
      σ_e     : AM crystallinity (AM_S=1.0, AM_P=0.65)
      κ       : AM crystallinity (AM_S=1.0, AM_P=0.50), SE size-invariant

    Cases predating Stage E auto-pipeline leave the keys missing → silently
    skipped. Newly analyzed cases (post-Stage-E auto-integration) populate.
    """
    if 'network_summary' not in tables or not metrics:
        return
    data = tables['network_summary']['data']
    if not isinstance(data, list):
        return

    section_label = '── Stage E (literature-grounded σ_grain corrections) ──'
    if any(isinstance(r, list) and r and r[0] == section_label for r in data):
        return  # already injected

    factors = metrics.get('stage_e_factors_used') or {}
    # Hertzian-baseline Stage E (existing)
    sigma_i_e    = metrics.get('sigma_full_mScm_stage_e')
    sigma_e_e    = metrics.get('electronic_sigma_full_mScm_stage_e')
    sigma_th_e   = metrics.get('thermal_sigma_full_mScm_stage_e')
    # Physics-baseline Stage E (NEW — added in run_network_full_corrections
    # so the UI can show the 4-col Hertzian | Physics | Δ% format mirroring
    # the Network Solver section)
    sigma_i_e_p  = metrics.get('sigma_full_mScm_stage_e_physics')
    sigma_e_e_p  = metrics.get('electronic_sigma_full_mScm_stage_e_physics')
    sigma_th_e_p = metrics.get('thermal_sigma_full_mScm_stage_e_physics')
    if not (factors or sigma_i_e is not None or sigma_e_e is not None):
        return  # no Stage E data on this case

    src = metrics.get('stage_e_source') or {}
    src_i  = src.get('sigma_ionic',   'solver')
    src_e  = src.get('sigma_e',       'solver')
    src_th = src.get('sigma_thermal', 'solver')
    # Physics-baseline source flags (cases analyzed before Physics-Stage E
    # was added will silently default to 'solver' — UI shows '—' Physics
    # column for those, no fallback tag)
    src_i_p  = src.get('sigma_ionic_physics',   'solver')
    src_e_p  = src.get('sigma_e_physics',       'solver')
    src_th_p = src.get('sigma_thermal_physics', 'solver')
    def _src_tag(s):
        if s == 'fallback_weighted_factor':
            return ' [⚡Bruggeman fallback]'
        return ''

    rows: list = [[section_label, '', '', '']]

    # Applied factors header — size-dependent breakdown (stable labels so
    # tooltips can match; dynamic per-channel values go in value column)
    r_se = factors.get('r_SE_um')
    r_am_p = factors.get('r_AM_P_um')
    r_am_s = factors.get('r_AM_S_um')
    f_se_ionic = factors.get('f_SE_ionic')
    am_factors = factors.get('AM_factors') or {}
    kappa_factors = factors.get('kappa_factors') or {}

    if r_se is not None and f_se_ionic is not None:
        rows.append([
            '  σ_ionic — SE size factor',
            '',
            f'r_SE={r_se:.2f}μm   ×{f_se_ionic:.2f}',
            'Cronau 2022 — size-invariant ≥0.5μm' if f_se_ionic >= 0.99
            else f'Cronau 2022 — sub-μm amorphization'
        ])

    # σ_e correction — always emit (— placeholder for missing factors)
    am_s = am_factors.get('AM_S') if am_factors else None
    am_p = am_factors.get('AM_P') if am_factors else None
    am_s_lbl = (f'AM_S(r={r_am_s:.1f}μm)×{am_s:.2f}'
                 if am_s is not None and r_am_s else 'AM_S — n/a')
    am_p_lbl = (f'AM_P(r={r_am_p:.1f}μm)×{am_p:.2f}'
                 if am_p is not None and r_am_p else 'AM_P — n/a')
    rows.append([
        '  σ_e — AM crystal × size', '',
        f'{am_s_lbl} / {am_p_lbl}',
        'Trevisanello 2021 + size-dependent internal-GB density'
    ])

    # κ correction — always emit (— placeholder when kappa_factors missing)
    k_s  = kappa_factors.get('AM_S') if kappa_factors else None
    k_p  = kappa_factors.get('AM_P') if kappa_factors else None
    k_se = kappa_factors.get('SE')   if kappa_factors else None
    k_s_lbl  = (f'AM_S(r={r_am_s:.1f}μm)×{k_s:.2f}'
                if k_s is not None and r_am_s else 'AM_S — n/a')
    k_p_lbl  = (f'AM_P(r={r_am_p:.1f}μm)×{k_p:.2f}'
                if k_p is not None and r_am_p else 'AM_P — n/a')
    k_se_lbl = (f'SE×{k_se:.2f}' if k_se is not None else 'SE — n/a')
    rows.append([
        '  κ — AM crystal × size + SE', '',
        f'{k_s_lbl} / {k_p_lbl} / {k_se_lbl}',
        'Wang 2022 + phonon GB scatter (∝ AM secondary R)'
    ])

    # Corrected σ values — 4-col format (Hertzian | Physics | Δ%) mirroring
    # the Network Solver section. Stage E factor (Lawn × Cronau / Trev /
    # Wang) is grain-level and applies equally to both Hertzian and
    # Tabor-plastic-film baselines, so we report both side-by-side.
    def _stage_e_row(label, val_h, val_p, base_h_key, base_p_key,
                     src_h, src_p, fmt='%.4f', unit='mS/cm'):
        baseline_h = metrics.get(base_h_key)
        baseline_p = metrics.get(base_p_key)
        # Hertzian column — show value or '—' if missing
        if val_h is None:
            h_str = '—'
        else:
            h_str = f'{val_h:{fmt[1:]}}'
        # Physics column
        if val_p is None:
            p_str = '—'
        else:
            p_str = f'{val_p:{fmt[1:]}}'
        # Δ% column — Physics vs Hertzian (mode contrast, not loss-vs-baseline)
        if val_h is not None and val_p is not None and val_h:
            delta_pp = (val_p - val_h) / val_h * 100
            d_str = f'{delta_pp:+.1f}%'
        else:
            d_str = '—'
        # Source tags appended (e.g. '⚡ H-fb' if Hertzian fallback fired)
        tag_parts = []
        if src_h == 'fallback_weighted_factor': tag_parts.append('H:⚡')
        if src_p == 'fallback_weighted_factor': tag_parts.append('P:⚡')
        if tag_parts:
            d_str += '  [' + ' '.join(tag_parts) + ']'
        return [f'  {label}', h_str, p_str, d_str + f'  {unit}']

    rows.append(_stage_e_row('σ_ionic (Stage E corrected)',
                             sigma_i_e,  sigma_i_e_p,
                             'sigma_full_mScm', 'sigma_full_mScm_physics',
                             src_i,  src_i_p,
                             fmt='%.4f', unit='mS/cm'))
    rows.append(_stage_e_row('σ_electronic (Stage E corrected)',
                             sigma_e_e,  sigma_e_e_p,
                             'electronic_sigma_full_mScm',
                             'electronic_sigma_full_mScm_physics',
                             src_e, src_e_p,
                             fmt='%.3f', unit='mS/cm'))
    rows.append(_stage_e_row('σ_thermal (Stage E corrected)',
                             sigma_th_e, sigma_th_e_p,
                             'thermal_sigma_full_mScm',
                             'thermal_sigma_full_mScm_physics',
                             src_th, src_th_p,
                             fmt='%.3f', unit='mS/cm equiv'))

    # Stage counts (audit trail)
    sc = metrics.get('stage_e_fracture_stage_counts')
    if sc and isinstance(sc, dict):
        n_intact = int(sc.get('intact', 0))
        n_mc     = int(sc.get('microcrack', 0))
        n_mu     = int(sc.get('multicrack', 0))
        n_fr     = int(sc.get('fragmentation', 0))
        n_pu     = int(sc.get('pulverization', 0))
        n_total  = n_intact + n_mc + n_mu + n_fr + n_pu
        if n_total:
            rows.append([
                '  Fracture stage counts (intact/MC/Multi/Frag/Pulv)',
                '',
                f'{n_intact}/{n_mc}/{n_mu}/{n_fr}/{n_pu}',
                f'Lawn 1998 force multipliers (1/3/11/32)'
            ])

    # 7-Layer solver defence summary — visible audit trail of which (channel,
    # mode) pairs used the Bruggeman fallback. Format: '(σ_ionic, σ_e) on
    # Hertzian; (κ) on Physics' for clear scope.
    fb_h = []
    fb_p = []
    if src_i  == 'fallback_weighted_factor': fb_h.append('σ_ionic')
    if src_e  == 'fallback_weighted_factor': fb_h.append('σ_e')
    if src_th == 'fallback_weighted_factor': fb_h.append('κ')
    if src_i_p  == 'fallback_weighted_factor': fb_p.append('σ_ionic')
    if src_e_p  == 'fallback_weighted_factor': fb_p.append('σ_e')
    if src_th_p == 'fallback_weighted_factor': fb_p.append('κ')
    parts = []
    if fb_h: parts.append(f"Hertzian: ({', '.join(fb_h)})")
    if fb_p: parts.append(f"Physics: ({', '.join(fb_p)})")
    if parts:
        rows.append([
            '  7-Layer solver status', '',
            'Bruggeman fallback fired — ' + '  ·  '.join(parts),
            'Paper §6 Layer-6 (commit 7a11682) — σ ≈ σ_baseline·Σ(g·f)/Σg'
        ])
    else:
        rows.append([
            '  7-Layer solver status', '',
            'Direct solver (all channels + both modes valid)',
            'Paper §6 Layer-1~4 passed all sanity checks'
        ])

    if len(rows) <= 1:
        return  # only header — nothing to add

    # Anchor at end of network_summary (after Tier 1 patches if present)
    data.extend(rows)


def inject_cell_asr_rows(tables, metrics, input_params):
    """Append a 'Cell-level ASR (Area-Specific Resistance)' section showing
    the cell-scale impedance derived from intrinsic σ via Ohm's-law slab:

        R_cathode = L_cathode / σ
        G_cathode = σ · A_RVE / L_cathode
        ASR       = L_cathode / σ        [Ω·cm²]      (per unit area)

    L_cathode (μm) comes from metrics['thickness_um'] (DEM compaction-
    measured cathode thickness — mesh-z reference).
    A_RVE (μm²) comes from input_params box_x × box_y × scale².

    For each transport channel (σ_ionic, σ_e, κ) we compute ASR for all
    three solver modes that exist in metrics:
        Hertzian (DEM-native)
        Physics (Tabor + volume conservation)
        Stage E (literature-grounded σ_grain corrections — if present)

    Reviewer-grade context: Bielefeld 2022 / Minnmann 2021 / Lee 2020 all
    report cathode-ASR (not σ alone) because experimental EIS gives R·A
    directly. Adding this row makes the σ → ASR conversion transparent
    in the same table and lets reviewers cross-check against literature
    values (typical sulfide cathode ASR_ionic ≈ 10–100 Ω·cm² @ 1 mAh/cm²
    loading, depending on σ_eff and L).
    """
    if 'network_summary' not in tables or not metrics:
        return
    data = tables['network_summary']['data']
    if not isinstance(data, list):
        return

    section_label = '── Cell-level ASR (Ohm slab: R = L_cathode / σ) ──'
    if any(isinstance(r, list) and r and r[0] == section_label for r in data):
        return

    L_um = metrics.get('thickness_um')
    if not L_um or L_um <= 0:
        return  # no cathode thickness — can't compute slab resistance

    # RVE cross-section: box_x × box_y × scale² → μm². scale comes from
    # case.scale (used elsewhere as input_params.box_x × scale to get μm).
    scale = input_params.get('scale') or 1
    box_x_um = (input_params.get('box_x') or 0) * scale
    box_y_um = (input_params.get('box_y') or 0) * scale
    A_um2 = box_x_um * box_y_um if (box_x_um and box_y_um) else None

    # Conversion factor: σ (mS/cm) → ASR (Ω·cm²)
    #   σ [mS/cm] × 1e-3 = σ [S/cm];  ASR = L [cm] / σ [S/cm]  →  Ω·cm²
    #   With L in μm: ASR_Ωcm2 = (L_um × 1e-4) / (σ_mScm × 1e-3) = L_um × 0.1 / σ_mScm
    def _asr_ohm_cm2(sigma_mScm):
        if sigma_mScm is None or sigma_mScm <= 0:
            return None
        return L_um * 0.1 / sigma_mScm   # Ω·cm² (or K·cm²/W for thermal)

    rows = [[section_label, '', '', '']]
    geom_str = (f'L_cathode = {L_um:.1f} μm   (DEM thickness)'
                + (f',   A_RVE = {A_um2:.0f} μm²' if A_um2 else ''))
    rows.append([
        '  Cathode geometry (L, A)', '', geom_str,
        'L = thickness_um (mesh-z), A = box_x × box_y × scale²',
    ])

    def _row_for(label, k_h, k_p, k_eh, k_ep, unit='Ω·cm²'):
        """Hertzian / Physics + their Stage E counterparts.
        4-col layout: ASR_H | ASR_P | Δ% (Physics-vs-Hertzian, with Stage E
        side-info). Stage E ASRs (Hertzian + Physics) are reported in the
        Δ-column text so reviewers can read the full picture in one row."""
        asr_h  = _asr_ohm_cm2(metrics.get(k_h))
        asr_p  = _asr_ohm_cm2(metrics.get(k_p) if k_p else None)
        asr_eh = _asr_ohm_cm2(metrics.get(k_eh) if k_eh else None)
        asr_ep = _asr_ohm_cm2(metrics.get(k_ep) if k_ep else None)
        h_str = f'{asr_h:.2f}' if asr_h is not None else '—'
        p_str = f'{asr_p:.2f}' if asr_p is not None else '—'
        # Δ% (Physics-vs-Hertzian baseline, mirrors Network Solver section)
        if asr_h and asr_p:
            d_pp = (asr_p - asr_h) / asr_h * 100
            d_str = f'{d_pp:+.1f}%'
        else:
            d_str = '—'
        # Stage E inline summary (both modes when available)
        eh_str = f'{asr_eh:.2f}' if asr_eh is not None else '—'
        ep_str = f'{asr_ep:.2f}' if asr_ep is not None else '—'
        d_str += f'   |  Stage E: H={eh_str}, P={ep_str} ({unit})'
        return [f'  {label}', h_str, p_str, d_str]

    rows.append(_row_for('ASR_ionic (Ω·cm²)',
                 'sigma_full_mScm',
                 'sigma_full_mScm_physics',
                 'sigma_full_mScm_stage_e',
                 'sigma_full_mScm_stage_e_physics',
                 unit='Ω·cm²'))
    rows.append(_row_for('ASR_electronic (Ω·cm²)',
                 'electronic_sigma_full_mScm',
                 'electronic_sigma_full_mScm_physics',
                 'electronic_sigma_full_mScm_stage_e',
                 'electronic_sigma_full_mScm_stage_e_physics',
                 unit='Ω·cm²'))
    rows.append(_row_for('ASR_thermal (K·cm²/W equiv)',
                 'thermal_sigma_full_mScm',
                 'thermal_sigma_full_mScm_physics',
                 'thermal_sigma_full_mScm_stage_e',
                 'thermal_sigma_full_mScm_stage_e_physics',
                 unit='K·cm²/W equiv'))

    if len(rows) <= 2:
        return  # nothing meaningful

    data.extend(rows)


def normalize_network_summary_layout(tables, metrics):
    """Final structural normalizer — guarantees every case has identical
    row placement regardless of network_summary.csv vintage. Different
    analyze_contacts.py versions produced different CSV layouts:

      • Old format: SPLIT '── Network Solver (Hertzian) ──' AND
        '── Physics (Plastic film, Tabor+volume) ──' as two sections.
        Each row only fills col 2 OR col 3 — wastes the Δ% column.
      • New format: COMBINED '── Network Solver (DEM-native vs
        Tabor+volume physics) ──' single section with proper 4-col
        Hertzian | Physics | Δ% layout.
      • Some old cases also have σ_e missing, κ in wrong section,
        σ_Bruggeman duplicated, etc.

    This pass runs AFTER all injectors, BEFORE paper-label rename:
      Pass A: merge split Hertzian + Physics sections into one combined
              section (4-col format: Hertzian | Physics | Δ%).
      Pass B: relocate σ_electronic / σ_thermal rows that ended up under
              '── τ 비교 ──' back to network solver section.
      Pass C: de-duplicate σ_Bruggeman.
      Pass D: insert σ_e baseline row if missing (using metrics value or 0).
    """
    if 'network_summary' not in tables:
        return
    data = tables['network_summary']['data']
    if not isinstance(data, list) or not data:
        return

    SIGMA_LABELS = {
        'σ_electronic (mS/cm)',
        'σ_thermal (mS/cm equiv)',
        'σ_electronic [physics] (mS/cm)',
        'σ_thermal [physics] (mS/cm equiv)',
    }

    def _is_section_hdr(label):
        return isinstance(label, str) and label.strip().startswith('──')

    def _section_of(idx):
        for j in range(idx - 1, -1, -1):
            r = data[j]
            if r and isinstance(r[0], str) and _is_section_hdr(r[0]):
                return r[0].strip()
        return None

    # ── Pass A: merge split Hertzian + Physics sections into combined ──
    # Pre-rename headers we look for:
    HERT_HDR = '── Network Solver (Hertzian DEM-native) ──'
    PHYS_HDR = '── Physics (Plastic film, Tabor+volume) ──'
    COMBINED_HDR = '── Network Solver (DEM-native vs Tabor+volume physics) ──'

    hert_idx = phys_idx = None
    for i, r in enumerate(data):
        if not r or not isinstance(r[0], str): continue
        lbl = r[0].strip()
        if lbl == HERT_HDR and hert_idx is None: hert_idx = i
        elif lbl == PHYS_HDR and phys_idx is None: phys_idx = i

    if hert_idx is not None and phys_idx is not None and phys_idx > hert_idx:
        # Find Physics section end (next section header or end-of-data)
        phys_end = len(data)
        for j in range(phys_idx + 1, len(data)):
            rr = data[j]
            if rr and isinstance(rr[0], str) and _is_section_hdr(rr[0]):
                phys_end = j
                break
        physics_rows = data[phys_idx + 1:phys_end]

        # Pair (Physics-row → Hertzian-row) labels for value merging
        PAIRS = {
            'σ_ionic [physics] (mS/cm)':                   'σ_ionic (mS/cm)',
            'σ_electronic [physics] (mS/cm)':              'σ_electronic (mS/cm)',
            'σ_thermal [physics] (mS/cm equiv)':           'σ_thermal (mS/cm equiv)',
        }
        pair_values = {}     # {hert_label: physics_value_str}
        standalone_rows = [] # rows in Physics section that are dual-mode (e.g. plastic amp)
        for r in physics_rows:
            if not r or not isinstance(r[0], str): continue
            lbl = r[0].strip()
            if lbl in PAIRS:
                phys_v = r[2] if len(r) > 2 and r[2] not in ('', '-') else r[1]
                pair_values[PAIRS[lbl]] = phys_v
            else:
                standalone_rows.append(r)

        # Update Hertzian-section rows: set Physics col + Δ%
        # (Hertzian section spans hert_idx+1 to phys_idx)
        for hi in range(hert_idx + 1, phys_idx):
            r = data[hi]
            if not r or not isinstance(r[0], str): continue
            lbl = r[0].strip()
            if lbl not in pair_values: continue
            phys_v = pair_values[lbl]
            try:
                h = float(str(r[1]).replace(',', ''))
                p = float(str(phys_v).replace(',', ''))
                r[2] = phys_v
                r[3] = f'{(p - h) / h * 100:+.1f}%' if h else '0%'
            except (ValueError, TypeError):
                r[2] = phys_v

        # Move standalone Physics rows (plastic amp, contact-free, etc.)
        # to the end of the Hertzian section (i.e., right before phys_idx)
        # while still preserving their Hertzian-vs-Physics 4-col content.
        # Insert at phys_idx (which is now the end-of-Hertzian boundary).
        for sr in standalone_rows:
            data.insert(phys_idx, sr)
            phys_idx += 1

        # Now delete the entire Physics section (header + remaining rows)
        # — but recompute phys_idx since we just inserted standalone rows.
        for i, r in enumerate(data):
            if r and isinstance(r[0], str) and r[0].strip() == PHYS_HDR:
                # Find end of physics section
                pe = len(data)
                for j in range(i + 1, len(data)):
                    rr = data[j]
                    if rr and isinstance(rr[0], str) and _is_section_hdr(rr[0]):
                        pe = j; break
                del data[i:pe]
                break

        # Rename Hertzian header to combined header
        for i, r in enumerate(data):
            if r and isinstance(r[0], str) and r[0].strip() == HERT_HDR:
                r[0] = COMBINED_HDR
                break

    # ── Pass B: relocate σ rows wrongly stuck in τ section ──
    misplaced = []
    for i, r in enumerate(data):
        if not r or not isinstance(r, list): continue
        lbl = r[0] if r else None
        if not isinstance(lbl, str): continue
        if lbl.strip() not in SIGMA_LABELS: continue
        sec = _section_of(i)
        if sec and ('τ 비교' in sec or 'Tortuosity comparison' in sec
                    or 'Dijkstra vs Laplace' in sec):
            misplaced.append(i)

    if misplaced:
        moved_rows = [data[i] for i in misplaced]
        for i in reversed(misplaced):
            data.pop(i)
        tau_idx = None
        for i, r in enumerate(data):
            if r and isinstance(r[0], str) and (
                'τ 비교' in r[0] or 'Tortuosity comparison' in r[0]
                or 'Dijkstra vs Laplace' in r[0]):
                tau_idx = i; break
        if tau_idx is not None:
            for m in reversed(moved_rows):
                data.insert(tau_idx, m)

    # ── Pass C: de-duplicate σ_Bruggeman ──
    seen_bruggeman = False
    drop_indices = []
    for i, r in enumerate(data):
        if not r or not isinstance(r, list): continue
        lbl = r[0] if r else None
        if not isinstance(lbl, str): continue
        if lbl.strip() == 'σ_Bruggeman (mS/cm)':
            if seen_bruggeman:
                drop_indices.append(i)
            else:
                seen_bruggeman = True
    for i in reversed(drop_indices):
        data.pop(i)

    # ── Pass E: insert placeholder rows for layout consistency ──
    # Some rows are bimodal-only (AM-SE CN sub-rows, AM Vulnerable sub-rows),
    # particle-type-specific (Coverage AM_P/AM_S, von-Mises stress ratios),
    # or path-dependent (R_brug, Plastic amplification). Insert — placeholders
    # so all 160 cases have the same row count + order.
    def _label_at(idx):
        r = data[idx] if 0 <= idx < len(data) else None
        if r and isinstance(r[0], str): return r[0].strip()
        return ''

    def _find_row(label):
        for i, r in enumerate(data):
            if r and isinstance(r[0], str) and r[0].strip() == label:
                return i
        return None

    def _insert_after(anchor_label, new_row):
        ai = _find_row(anchor_label)
        if ai is None: return False
        # Skip past any existing children (rows starting with ├ or └)
        j = ai + 1
        while j < len(data):
            r = data[j]
            if not r or not isinstance(r[0], str): break
            stripped = r[0].lstrip()
            if not (stripped.startswith('├') or stripped.startswith('└')):
                break
            if stripped == new_row[0].lstrip():
                return True  # already present — nothing to do
            j += 1
        data.insert(j, new_row)
        return True

    # AM-SE CN sub-rows (always emit ├ AM_P-SE / ├ AM_S-SE / └ surface-weighted)
    for child_label in ('  ├ AM_P-SE CN mean',
                        '  ├ AM_S-SE CN mean',
                        '  └ AM-SE CN (surface-weighted)'):
        if _find_row(child_label) is None:
            _insert_after('AM-SE CN mean', [child_label, '—', '—', '0%'])

    # AM Vulnerable sub-rows (├ AM_P Vulnerable / └ AM_S Vulnerable)
    for child_label in ('  ├ AM_P Vulnerable(%)',
                        '  └ AM_S Vulnerable(%)'):
        if _find_row(child_label) is None:
            _insert_after('AM Vulnerable(%)', [child_label, '—', '—', '0%'])

    # Coverage AM_P / AM_S — always emit even when particle type absent
    if _find_row('Coverage AM_P(%)') is None:
        _insert_after('SE-SE Total(μm²)',
                      ['Coverage AM_P(%)', '—', '—', '0%'])
    if _find_row('Coverage AM_S(%)') is None:
        # Insert after Coverage AM_P (or after SE-SE Total if AM_P just added)
        anchor = 'Coverage AM_P(%)' if _find_row('Coverage AM_P(%)') else 'SE-SE Total(μm²)'
        _insert_after(anchor, ['Coverage AM_S(%)', '—', '—', '0%'])

    # von-Mises stress ratio rows — always emit AM_P / AM_S / SE
    for label in ('σ_AM_P/σ_mean', 'σ_AM_S/σ_mean', 'σ_SE/σ_mean'):
        if _find_row(label) is None:
            _insert_after('Stress CV(%)', [label, '—', '—', '0%'])

    # R_brug + Plastic amplification — always emit
    if _find_row('R_brug (과대추정 배수)') is None:
        rb = metrics.get('R_brug_over_full') if metrics else None
        rb_str = f'{rb:.1f}×' if isinstance(rb, (int, float)) and rb else '—'
        _insert_after('σ_ionic (mS/cm)',
                      ['R_brug (과대추정 배수)', rb_str, rb_str, '0%'])
    if _find_row('σ_ionic ratio (physics/Hertzian)') is None:
        sh = metrics.get('sigma_full_mScm') if metrics else None
        sp = metrics.get('sigma_full_mScm_physics') if metrics else None
        if sh and sp:
            r = sp / sh
            ratio_str = f'{r:.2f}×'
        else:
            ratio_str = '—'
        _insert_after('σ_ionic (mS/cm)',
                      ['σ_ionic ratio (physics/Hertzian)',
                       ratio_str, ratio_str, '0%'])

    # ── Pass D: ensure σ_e and κ baseline rows exist ──
    # Some legacy/freshly-analysed cases write σ_e or κ as None when the
    # respective channel was numerically zero. We still want a placeholder
    # row for layout uniformity (audit-ui = 1 variant goal).
    def _ensure_baseline_row(label, h_key, p_key, fmt='%.2f'):
        present = any(
            r and isinstance(r[0], str) and r[0].strip() == label
            for r in data if isinstance(r, list))
        if present:
            return
        h_val = metrics.get(h_key) if metrics else None
        p_val = metrics.get(p_key) if metrics else None
        h_str = f'{h_val:{fmt[1:]}}' if h_val else '0.00'
        if p_val is not None:
            p_str = f'{p_val:{fmt[1:]}}'
            if h_val:
                d_str = f'{(p_val - h_val) / h_val * 100:+.1f}%'
            else:
                d_str = '0%'
        else:
            p_str = h_str; d_str = '0%'
        new_row = [label, h_str, p_str, d_str]
        tau_idx = None
        for i, r in enumerate(data):
            if r and isinstance(r[0], str) and (
                'τ 비교' in r[0] or 'Tortuosity comparison' in r[0]
                or 'Dijkstra vs Laplace' in r[0]):
                tau_idx = i; break
        if tau_idx is not None:
            data.insert(tau_idx, new_row)
        else:
            data.append(new_row)

    _ensure_baseline_row('σ_electronic (mS/cm)',
                         'electronic_sigma_full_mScm',
                         'electronic_sigma_full_mScm_physics', fmt='%.2f')
    _ensure_baseline_row('σ_thermal (mS/cm equiv)',
                         'thermal_sigma_full_mScm',
                         'thermal_sigma_full_mScm_physics', fmt='%.3f')

    # ── Pass F: sort rows within each section by canonical order ──
    # All 160 cases now have identical row CONTENT after passes A-E, but
    # different injection paths leave them in inconsistent ORDER. This
    # final pass enforces a single canonical ordering.
    _CANONICAL_ROW_ORDER = [
        # 구조
        'Porosity(%)', '전극두께(μm)',
        # 계면
        'AM-SE Total(μm²)', 'SE-SE Total(μm²)',
        'Binding % — AM-SE (H/L/T/V/G)', 'Binding % — Total (H/L/T/V/G)',
        'Coverage AM_P(%)', 'Coverage AM_S(%)',
        # 이온경로 · 연결성
        'SE-SE CN mean', 'SE-SE CN std', 'SE Cluster 수',
        'SE Percolation(%)', 'Top Reachable(%)',
        # 이온경로 · 경로 효율
        'Tortuosity mean', 'Tortuosity median', 'Tortuosity std',
        'GB Density(hops/μm)',
        # 이온경로 · 경로 품질
        'Path Hop Area mean(μm²)', 'Path Bottleneck(μm²)', 'Path Conductance(μm²)',
        # 활성도
        'AM-SE CN mean',
        '├ AM_P-SE CN mean', '├ AM_S-SE CN mean',
        '└ AM-SE CN (surface-weighted)',
        'Ionic Active AM(%)', 'AM Vulnerable(%)',
        '├ AM_P Vulnerable(%)', '└ AM_S Vulnerable(%)',
        # 이온전도 (Bruggeman EMT)
        'SE Volume Fraction', 'σ_Bruggeman (mS/cm)',
        'σ_brug/σ_grain (Bruggeman)',
        # Network Solver — combined Hertzian vs Physics
        'σ_ionic (mS/cm)',
        'R_brug (과대추정 배수)',
        'σ_ionic ratio (physics/Hertzian)',
        'Constriction 비율(%)',
        'σ_electronic (mS/cm)',
        'σ_thermal (mS/cm equiv)',
        'Contact-free / Full',
        'σ_brug / σ_ionic',
        # τ 비교
        'τ_Dij (Dijkstra, 기하만)',
        'τ_Lap_geom (Laplace, GB 제외)',
        'τ_Lap_eff ⭐ (Laplace, GB 포함 — COMSOL/EIS)',
        'τ_Lap_eff / τ_Dij',
        'AM Percolation (%)',
        'Electronic Active AM (%)',
        # Tier-1
        'Coverage AM rough(%)   ⭐ [B3]',
        'Coverage AM_P rough(%) ⭐ [B3]',
        'Coverage AM_S rough(%) ⭐ [B3]',
        'SE-SE CN (perc-only)        [F2]',
        'SE-SE CN (area-weighted)    [F2]',
        'SE-SE CN (perc area-w)      [F2]',
        'SE-SE CN (plastic-augmented) [F1]',
        '(F1 extra near-contact pairs)',
        # AM-AM
        'AM-AM CN mean', 'AM-AM 접촉 수',
        '접촉 반경(µm)', '침투 깊이 δ(µm)', '법선력(µN)',
        '접촉 압력(MPa)', 'Hop 거리(µm)',
        # 응력
        'Stress CV(%)',
        'σ_AM_P/σ_mean', 'σ_AM_S/σ_mean', 'σ_SE/σ_mean',
        # Stage E
        'σ_ionic — SE size factor',
        'σ_e — AM crystal × size',
        'κ — AM crystal × size + SE',
        'σ_ionic (Stage E corrected)',
        'σ_electronic (Stage E corrected)',
        'σ_thermal (Stage E corrected)',
        'Fracture stage counts (intact/MC/Multi/Frag/Pulv)',
        '7-Layer solver status',
        # Cell-level ASR
        'Cathode geometry (L, A)',
        'ASR_ionic (Ω·cm²)',
        'ASR_electronic (Ω·cm²)',
        'ASR_thermal (K·cm²/W equiv)',
    ]
    _canon_idx = {lbl: i for i, lbl in enumerate(_CANONICAL_ROW_ORDER)}

    def _sort_key(row):
        if not row or not isinstance(row[0], str): return (1, 0)
        lbl = row[0].strip()
        i = _canon_idx.get(lbl)
        if i is None:
            return (1, 0)  # unknown labels go to end (preserve relative order via stable sort)
        return (0, i)

    # Group rows by section
    sections = []   # list of [header_idx, [row_indices...]]
    current = None
    for i, r in enumerate(data):
        if r and isinstance(r[0], str) and r[0].strip().startswith('──'):
            if current is not None:
                sections.append(current)
            current = [i, []]
        elif current is not None:
            current[1].append(i)
    if current is not None:
        sections.append(current)

    # Stable-sort each section's rows by canonical index
    for _hdr_idx, row_idxs in sections:
        if len(row_idxs) <= 1: continue
        rows_in_section = [data[ri] for ri in row_idxs]
        sorted_rows = sorted(rows_in_section, key=_sort_key)
        for offset, sr in enumerate(sorted_rows):
            data[row_idxs[0] + offset] = sr


# ──────────────────────────────────────────────────────────────────────────
#  Paper-style label renaming (advisor feedback — formal academic language)
#
#  Both analyze_contacts.py CSV outputs and webapp injectors use mixed
#  Korean/informal labels (e.g., '── 이온경로: 연결성 ──', 'σ_brug/σ_grain
#  (Bruggeman)'). Paper / reviewer-facing UI needs proper academic notation
#  (LaTeX-friendly symbols, English section headers, explicit units).
#
#  We rename at render time (not in CSV) so:
#    - Historical CSVs in archive/ keep their original labels on disk
#    - Tooltips still match via the LABEL_ALIASES reverse map (single.html JS)
#    - One-line revert if reviewers want different terminology
# ──────────────────────────────────────────────────────────────────────────
_PAPER_SECTION_MAP = {
    '── 구조 ──': '── 구조 (Structure — DEM compaction state) ──',
    '── 계면 ──':
        '── 계면 (Interfacial contact area — AM-SE / SE-SE) ──',
    '── 이온경로: 연결성 ──':
        '── 이온 전달 · 연결성 (Ionic transport — Network connectivity) ──',
    '── 이온경로: 경로 효율 ──':
        '── 이온 전달 · 경로 효율 (Ionic transport — Geodesic tortuosity) ──',
    '── 이온경로: 경로 품질 ──':
        '── 이온 전달 · 경로 품질 (Ionic transport — Path quality, bottleneck & conductance) ──',
    '── 활성도 ──':
        '── 활성도 (Electrochemically-active surface) ──',
    '── 이온전도 ──':
        '── 이온 전도 (Ionic conductivity — Bruggeman EMT estimate) ──',
    '── Network Solver (Hertzian DEM-native) ──':
        '── 네트워크 솔버 · Hertzian (Network solver — DEM native contact area) ──',
    '── Network Solver (DEM-native vs Tabor+volume physics) ──':
        '── 네트워크 솔버 · Hertzian vs Physics (Network solver — DEM native vs Tabor + volume) ──',
    '── Physics (Plastic film, Tabor+volume) ──':
        '── 네트워크 솔버 · Physics (Network solver — Tabor plastic film + volume conservation) ──',
    '── τ 비교 (Dijkstra vs Laplace, COMSOL input = τ_Lap_eff) ──':
        '── 굴곡도 비교 (Tortuosity — Dijkstra vs Laplacian; COMSOL/EIS input = τ_Laplace,eff) ──',
    '── Tier 1 patches (post-Auerbach refinements) ──':
        '── Tier-1 보정 (Tier-1 corrections — post-Auerbach refinements) ──',
    '── AM-AM 접촉 역학 ──':
        '── AM-AM 접촉 역학 (AM-AM contact mechanics) ──',
    '── 응력 ──':
        '── 응력 분포 (Particle-stress distribution — von Mises) ──',
    '── Stage E (literature-grounded σ_grain corrections) ──':
        '── Stage E · 문헌 기반 σ_grain 보정 (Stage E — Literature-grounded σ_grain corrections, Cronau / Trevisanello / Wang) ──',
    '── Cell-level ASR (Ohm slab: R = L_cathode / σ) ──':
        '── 셀 단위 ASR · 두께·전도도 슬랩 (Cell-level area-specific resistance — Ohm slab: R = L_cathode / σ) ──',
}

_PAPER_LABEL_MAP = {
    # Structure
    'Porosity(%)':                 'Porosity ε (%)',
    '전극두께(μm)':                 'Electrode thickness T (μm)',
    # Interface
    'AM-SE Total(μm²)':            'Total AM-SE contact area, A_AM-SE (μm²)',
    'SE-SE Total(μm²)':            'Total SE-SE contact area, A_SE-SE (μm²)',
    'Binding % — AM-SE (H/L/T/V/G)':
        'Binding regime share — AM-SE (Hertz / LIGGGHTS / Tabor / Volume / Geom)',
    'Binding % — Total (H/L/T/V/G)':
        'Binding regime share — All contacts (Hertz / LIGGGHTS / Tabor / Volume / Geom)',
    'Coverage AM_P(%)':            'Coverage of AM_P by SE, cov_AM_P (%)',
    'Coverage AM_S(%)':            'Coverage of AM_S by SE, cov_AM_S (%)',
    'Coverage AM(%)':              'Coverage of AM by SE, cov_AM (%)',
    # Connectivity
    'SE-SE CN mean':               'SE-SE coordination number ⟨z_SE-SE⟩',
    'SE-SE CN std':                'SE-SE coordination number σ(z_SE-SE)',
    'SE Cluster 수':               'SE percolating clusters (n≥10 / total)',
    'SE Percolation(%)':           'SE percolation, top↔bottom (%)',
    'Top Reachable(%)':            'Separator-side SE connectivity, f_SE^sep (%)',
    # Tortuosity
    'Tortuosity mean':             'Tortuosity ⟨τ_Dijkstra⟩ (geodesic)',
    'Tortuosity median':           'Tortuosity median(τ_Dijkstra)',
    'Tortuosity std':              'Tortuosity σ(τ_Dijkstra)',
    'GB Density(hops/μm)':         'Grain-boundary density (hops/μm)',
    # Path quality
    'Path Hop Area mean(μm²)':     'Mean per-hop contact area, ⟨A_hop⟩ (μm²)',
    'Path Bottleneck(μm²)':        'Path bottleneck min(A_contact) (μm²)',
    'Path Conductance(μm²)':       'Effective path conductance Σ(A/ℓ) (μm²)',
    # Active surface
    'AM-SE CN mean':               'AM-SE coordination number ⟨z_AM-SE⟩',
    '  ├ AM_P-SE CN mean':         '  ├ AM_P-SE coordination number ⟨z_AM_P-SE⟩',
    '  ├ AM_S-SE CN mean':         '  ├ AM_S-SE coordination number ⟨z_AM_S-SE⟩',
    '  └ AM-SE CN (surface-weighted)':
        '  └ AM-SE coordination number (surface-area weighted)',
    'Ionic Active AM(%)':          'Ionically-active AM, SE-touching (%)',
    'AM Vulnerable(%)':            'Ionically-vulnerable AM, low-coverage (%)',
    '  ├ AM_P Vulnerable(%)':      '  ├ AM_P ionically-vulnerable (%)',
    '  └ AM_S Vulnerable(%)':      '  └ AM_S ionically-vulnerable (%)',
    # Bruggeman EMT
    'SE Volume Fraction':          'SE volume fraction, φ_SE',
    'σ_Bruggeman (mS/cm)':         'σ_Bruggeman — EMT estimate (mS/cm)',
    'σ_brug/σ_grain (Bruggeman)':  'Bruggeman coefficient, σ_Bruggeman / σ_grain',
    # Network solver — Hertzian
    'σ_ionic (mS/cm)':             'σ_ionic — full network solver (mS/cm)',
    'R_brug (과대추정 배수)':       'Bruggeman overestimation, R_brug = σ_Bruggeman / σ_ionic',
    'Constriction 비율(%)':         'Constriction-resistance fraction (%)',
    'σ_electronic (mS/cm)':        'σ_e — electronic conductivity (mS/cm)',
    'σ_thermal (mS/cm equiv)':     'κ — thermal conductivity (mS/cm equiv)',
    # Physics (Tabor)
    'σ_ionic [physics] (mS/cm)':
        'σ_ionic^physics — Tabor plastic film (mS/cm)',
    'σ_ionic ratio (physics/Hertzian)':
        'Plastic amplification, σ_ionic^physics / σ_ionic^Hertzian',
    'σ_electronic [physics] (mS/cm)':
        'σ_e^physics — Tabor plastic film (mS/cm)',
    'σ_thermal [physics] (mS/cm equiv)':
        'κ^physics — Tabor plastic film (mS/cm equiv)',
    'Contact-free / Full':
        'σ_contact-free / σ_full — constriction overestimation',
    'σ_brug / σ_ionic':
        'σ_Bruggeman / σ_ionic — EMT vs Network solver',
    # Tortuosity comparison
    'τ_Dij (Dijkstra, 기하만)':
        'τ_Dijkstra — geodesic-only (geometric)',
    'τ_Lap_geom (Laplace, GB 제외)':
        'τ_Laplace,bulk — Laplacian without constriction',
    'τ_Lap_eff ⭐ (Laplace, GB 포함 — COMSOL/EIS)':
        'τ_Laplace,eff ⭐ — Laplacian + constriction (COMSOL / EIS input)',
    'τ_Lap_eff / τ_Dij':
        'Constriction overhead, τ_Laplace,eff / τ_Dijkstra',
    'AM Percolation (%)':          'AM percolation, top↔bottom (%)',
    'Electronic Active AM (%)':    'Current-collector-connected AM, f_AM^cc (%)',
    # Tier-1 corrections
    'Coverage AM rough(%)   ⭐ [B3]':
        'Coverage of AM, shape-corrected ⭐ (B3)',
    'Coverage AM_P rough(%) ⭐ [B3]':
        'Coverage of AM_P, shape-corrected ⭐ (B3)',
    'Coverage AM_S rough(%) ⭐ [B3]':
        'Coverage of AM_S, shape-corrected ⭐ (B3)',
    'SE-SE CN (perc-only)        [F2]':
        'SE-SE ⟨z⟩ — percolating-only (F2)',
    'SE-SE CN (area-weighted)    [F2]':
        'SE-SE ⟨z⟩ — surface-area weighted (F2)',
    'SE-SE CN (perc area-w)      [F2]':
        'SE-SE ⟨z⟩ — percolating + area-weighted (F2)',
    'SE-SE CN (plastic-augmented) [F1]':
        'SE-SE ⟨z⟩ — plastic-augmented (F1)',
    '(F1 extra near-contact pairs)':
        'F1 near-contact pairs (gap < 10 nm)',
    # AM-AM mechanics
    'AM-AM CN mean':               'AM-AM coordination number ⟨z_AM-AM⟩',
    'AM-AM 접촉 수':                'AM-AM contact count',
    '접촉 반경(µm)':                'Mean Hertzian contact radius, ⟨a⟩ (μm)',
    '침투 깊이 δ(µm)':              'Mean overlap depth, ⟨δ⟩ (μm)',
    '법선력(µN)':                   'Mean normal force, ⟨F_n⟩ (μN)',
    '접촉 압력(MPa)':               'Mean contact pressure, ⟨p⟩ (MPa)',
    'Hop 거리(µm)':                 'Mean inter-particle hop distance (μm)',
    # Stress
    'Stress CV(%)':
        'Particle-stress coefficient of variation, CV(σ_VM) (%)',
    'σ_AM_P/σ_mean':
        'von-Mises stress ratio, ⟨σ_VM⟩_AM_P / ⟨σ_VM⟩_all',
    'σ_AM_S/σ_mean':
        'von-Mises stress ratio, ⟨σ_VM⟩_AM_S / ⟨σ_VM⟩_all',
    'σ_SE/σ_mean':
        'von-Mises stress ratio, ⟨σ_VM⟩_SE / ⟨σ_VM⟩_all',
    # Stage E (already paper-style; tightened wording only)
    'σ_ionic — SE size factor':
        'σ_ionic correction — SE-size factor (Cronau 2022)',
    'σ_e — AM crystal × size':
        'σ_e correction — AM-crystallinity × size factor (Trevisanello 2021)',
    'κ — AM crystal × size + SE':
        'κ correction — AM-crystallinity + SE factor (Wang 2022)',
    'σ_ionic (Stage E corrected)':
        '⭐ σ_ionic — Stage E final (full literature-grounded corrections, mS/cm)',
    'σ_electronic (Stage E corrected)':
        '⭐ σ_e — Stage E final (fracture × AM-crystallinity, mS/cm)',
    'σ_thermal (Stage E corrected)':
        '⭐ κ — Stage E final (Wang grain corrections, mS/cm equiv)',
    'Fracture stage counts (intact/MC/Multi/Frag/Pulv)':
        'Per-contact fracture-stage distribution (intact / micro / multi / frag / pulv)',
    '7-Layer solver status':
        '7-Layer solver defence — channel status',
}


def apply_paper_labels(tables):
    """Replace informal/Korean labels with formal academic notation. Acts on
    network_summary table in-place. Preserves leading whitespace (used for
    indentation under section headers) and updates tooltip data-metric via
    JS LABEL_ALIASES (single.html) so existing tooltip definitions still
    match without requiring 90-key rename across the JS dict.

    Called from /single/<case_id> and /archive/view/<folder> routes after
    all section injectors finish."""
    if 'network_summary' not in tables:
        return
    tbl = tables['network_summary']
    data = tbl.get('data')
    if not isinstance(data, list):
        return
    for row in data:
        if not row or not isinstance(row, list):
            continue
        label = row[0] if row else None
        if not isinstance(label, str):
            continue
        stripped = label.lstrip()
        prefix = label[: len(label) - len(stripped)]
        if stripped.startswith('──'):
            new = _PAPER_SECTION_MAP.get(stripped)
        else:
            new = _PAPER_LABEL_MAP.get(stripped)
        if new and new != stripped:
            row[0] = prefix + new


def transform_network_summary_4col(tables, metrics, meta):
    """Convert network_summary table to 4-column (지표 | Hertzian | Physics | Δ%)
    and inject Network Solver + AM-AM sections from full_metrics.json.

    Shared helper for /single/<case_id> and /archive/view/<folder> routes."""
    if 'network_summary' not in tables:
        return
    tbl = tables['network_summary']

    # Step 1: expand existing rows to 4 cols (default Physics = Hertzian, Δ = 0%)
    tbl['columns'] = ['지표 (Metric)', 'Hertzian (DEM native)', 'Physics (Tabor + volume)', 'Δ (%)']
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

    # Step 4b: τ_Lap + supplementary rows that analyze_contacts.py does NOT write
    # to the CSV (σ_Bruggeman, Contact-free/Full, σ_brug/σ_ionic, τ-comparison,
    # AM Percolation, Electronic Active AM). When analyze_contacts wrote its own
    # "── Network Solver (Hertzian DEM-native) ──" header to the CSV, Step 4
    # above is skipped (has_net_section=True) — so we ALWAYS run this second
    # pass that adds only the rows missing from the CSV-written section.
    # Each row uses _has_label() to avoid duplicates.
    if metrics:
        def _has_label(lbl):
            for r in data:
                if isinstance(r, list) and r and str(r[0]).strip() == lbl.strip():
                    return True
            return False

        # Anchor: insert after the existing Network Solver section header
        net_anchor = None
        for i, r in enumerate(data):
            if (isinstance(r, list) and r
                    and isinstance(r[0], str)
                    and r[0].startswith('── Network Solver')):
                net_anchor = i
                break

        # Find anchor for the *END* of Network Solver section (= start of next section)
        net_end = len(data)
        if net_anchor is not None:
            for i in range(net_anchor + 1, len(data)):
                r = data[i]
                if (isinstance(r, list) and r
                        and isinstance(r[0], str)
                        and r[0].startswith('──')
                        and not r[0].startswith('── Network Solver')
                        and not r[0].startswith('── Physics')):
                    net_end = i
                    break

        new_rows: list = []

        # σ_Bruggeman (mS/cm)
        if (not _has_label('σ_Bruggeman (mS/cm)')
                and metrics.get('sigma_bruggeman_mScm')):
            new_rows.append(_same_row('σ_Bruggeman (mS/cm)',
                                       round(metrics['sigma_bruggeman_mScm'], 4)))

        # Contact-free / Full
        if (not _has_label('Contact-free / Full')
                and metrics.get('R_brug_over_full')):
            r_h = metrics.get('R_brug_over_full')
            r_p = metrics.get('R_brug_over_full_physics', r_h)
            new_rows.append(_dual_row('Contact-free / Full',
                                       r_h, r_p,
                                       fmt=lambda x: f"{x:.1f}×"))

        # σ_brug / σ_ionic
        if (not _has_label('σ_brug / σ_ionic')
                and metrics.get('sigma_ratio') and metrics.get('sigma_full_mScm')):
            sig_brug = 3.0 * metrics['sigma_ratio']
            sig_ion_h = metrics.get('sigma_full_mScm')
            sig_ion_p = metrics.get('sigma_full_mScm_physics') or sig_ion_h
            ratio_h = sig_brug / sig_ion_h if sig_ion_h > 0 else 0
            ratio_p = sig_brug / sig_ion_p if sig_ion_p and sig_ion_p > 0 else ratio_h
            new_rows.append(_dual_row('σ_brug / σ_ionic',
                                       ratio_h, ratio_p,
                                       fmt=lambda x: f"{x:.1f}×"))

        # ── τ 3종 비교 ── (always-inject if absent)
        import math as _math
        phi_se   = metrics.get('phi_se')
        sig_full = metrics.get('sigma_full_mScm')
        sig_bulk = metrics.get('sigma_bulk_net_mScm')
        tau_dij  = metrics.get('tortuosity_mean')
        SIGMA_GRAIN_MS = 3.0
        tau_section_label = '── τ 비교 (Dijkstra vs Laplace, COMSOL input = τ_Lap_eff) ──'
        if (not _has_label(tau_section_label)
                and phi_se and sig_full and sig_full > 0):
            sig_full_p = metrics.get('sigma_full_mScm_physics')
            tau_lap_eff_h = _math.sqrt(phi_se * SIGMA_GRAIN_MS / sig_full)
            tau_lap_eff_p = (_math.sqrt(phi_se * SIGMA_GRAIN_MS / sig_full_p)
                             if sig_full_p and sig_full_p > 0 else tau_lap_eff_h)
            tau_lap_geom = (_math.sqrt(phi_se * SIGMA_GRAIN_MS / sig_bulk)
                            if sig_bulk and sig_bulk > 0 else None)
            new_rows.append([tau_section_label, '', '', ''])
            if tau_dij:
                new_rows.append(_same_row('τ_Dij (Dijkstra, 기하만)', round(tau_dij, 2)))
            if tau_lap_geom:
                new_rows.append(_same_row('τ_Lap_geom (Laplace, GB 제외)', round(tau_lap_geom, 2)))
            new_rows.append(_dual_row('τ_Lap_eff ⭐ (Laplace, GB 포함 — COMSOL/EIS)',
                                       tau_lap_eff_h, tau_lap_eff_p,
                                       fmt=lambda x: round(x, 2)))
            if tau_dij and tau_dij > 0:
                ratio_h = tau_lap_eff_h / tau_dij
                ratio_p = tau_lap_eff_p / tau_dij
                new_rows.append(_dual_row('τ_Lap_eff / τ_Dij',
                                           ratio_h, ratio_p,
                                           fmt=lambda x: f"{x:.2f}×"))

        # AM Percolation (electronic)
        if (not _has_label('AM Percolation (%)')
                and metrics.get('electronic_percolating_fraction') is not None):
            v = f"{metrics['electronic_percolating_fraction']*100:.1f}"
            new_rows.append(_same_row('AM Percolation (%)', v))

        # Electronic Active AM
        if (not _has_label('Electronic Active AM (%)')
                and metrics.get('electronic_active_fraction') is not None):
            v = f"{metrics['electronic_active_fraction']*100:.1f}"
            new_rows.append(_same_row('Electronic Active AM (%)', v))

        # Insert at the end of the Network Solver section
        if new_rows:
            for j, nr in enumerate(new_rows):
                data.insert(net_end + j, nr)

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

        # Step 2c: Network solver (both contact modes) → sigma_*_mScm
        cmd = ['python3', os.path.join(scripts, 'network_conductivity.py'),
               atoms_csv, contacts_csv, '-o', results_dir,
               '-t', type_map, '-s', str(scale),
               '--contact-mode', 'both']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
        log.append({'step': 'Network Solver (both modes)', 'stdout': result.stdout,
                    'stderr': result.stderr, 'rc': result.returncode})
        try:
            net_json = os.path.join(results_dir, 'network_conductivity.json')
            fm_json  = os.path.join(results_dir, 'full_metrics.json')
            if os.path.exists(net_json) and os.path.exists(fm_json):
                with open(net_json) as _f: net_data = json.load(_f)
                with open(fm_json)  as _f: fm_data  = json.load(_f)
                for k in _NET_MERGE_KEYS:
                    if k in net_data and net_data[k] is not None:
                        fm_data[k] = net_data[k]
                fm_data = _merge_dual_into_metrics(results_dir, fm_data)
                fm_data = _refresh_post_network_warnings(fm_data)
                fm_data['network_solver_status'] = (
                    'success' if result.returncode == 0 else 'failed')
                with open(fm_json, 'w') as _f:
                    json.dump(fm_data, _f, indent=2, default=str)
        except Exception:
            pass

        # Step 2d: Stage E — Literature-grounded full grain corrections
        # (mirrors Standard mode pipeline at line ~2024). Auto-applies
        # size/crystallinity factors per channel:
        #   σ_ionic : SE σ_grain(r_SE) — Cronau 2022 (size-invariant ≥ 0.3 μm)
        #   σ_e     : AM crystallinity (Trevisanello 2021) AM_S=1.0, AM_P=0.65
        #   κ       : AM crystallinity (Wang 2022) AM_S=1.0, AM_P=0.50
        # Includes 7-Layer defence + Bruggeman fallback when solver is
        # numerically unstable. Writes *_stage_e + stage_e_source into
        # full_metrics.json so the UI Stage E section auto-populates.
        try:
            stage_e_cmd = ['python3',
                            os.path.join(scripts, 'run_network_full_corrections.py'),
                            os.path.basename(results_dir), '--quiet']
            stage_e_result = subprocess.run(stage_e_cmd, capture_output=True,
                                              text=True, timeout=3600)
            log.append({'step': 'Stage E (literature-grounded grain corrections)',
                        'stdout': stage_e_result.stdout,
                        'stderr': stage_e_result.stderr,
                        'rc': stage_e_result.returncode})
        except Exception as _e:
            log.append({'step': 'Stage E (literature-grounded grain corrections)',
                        'stdout': '', 'stderr': str(_e), 'rc': 1})

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

        # Network solver (ionic + electronic + thermal, both contact modes).
        # Writes sigma_full_mScm, sigma_bulk_net_mScm, electronic_*, thermal_*
        # into network_conductivity_*.json, then merges into full_metrics.json
        # so the analysis-summary tab Network Solver section auto-populates.
        cmd = ['python3', os.path.join(scripts, 'network_conductivity.py'),
               atoms_csv, contacts_csv, '-o', results_dir,
               '-t', type_map, '-s', str(scale),
               '--contact-mode', 'both']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
        log.append({'step': 'Network Solver (both modes)', 'stdout': result.stdout,
                    'stderr': result.stderr, 'rc': result.returncode})
        # Merge network_conductivity.json → full_metrics.json
        try:
            net_json = os.path.join(results_dir, 'network_conductivity.json')
            fm_json  = os.path.join(results_dir, 'full_metrics.json')
            if os.path.exists(net_json) and os.path.exists(fm_json):
                with open(net_json) as _f: net_data = json.load(_f)
                with open(fm_json)  as _f: fm_data  = json.load(_f)
                for k in _NET_MERGE_KEYS:
                    if k in net_data and net_data[k] is not None:
                        fm_data[k] = net_data[k]
                fm_data = _merge_dual_into_metrics(results_dir, fm_data)
                fm_data = _refresh_post_network_warnings(fm_data)
                fm_data['network_solver_status'] = (
                    'success' if result.returncode == 0 else 'failed')
                with open(fm_json, 'w') as _f:
                    json.dump(fm_data, _f, indent=2, default=str)
                log.append({'step': 'Network Solver Merge',
                            'stdout': f'merged {len(_NET_MERGE_KEYS)} σ-keys',
                            'stderr': '', 'rc': 0})
        except Exception as _e:
            log.append({'step': 'Network Solver Merge',
                        'stdout': '', 'stderr': str(_e), 'rc': 1})

        # Stage E — Literature-grounded full grain corrections
        # Auto-applies size/crystallinity factors per channel:
        #   σ_ionic : SE σ_grain(r_SE) — Cronau 2022 (size-invariant ≥ 0.3 μm)
        #   σ_e     : AM crystallinity (Trevisanello 2021) AM_S=1.0, AM_P=0.65
        #   κ       : AM crystallinity (Wang 2022) AM_S=1.0, AM_P=0.50
        #            SE size-invariant (sulfide already glassy)
        try:
            stage_e_cmd = ['python3',
                            os.path.join(scripts, 'run_network_full_corrections.py'),
                            os.path.basename(results_dir), '--quiet']
            stage_e_result = subprocess.run(stage_e_cmd, capture_output=True,
                                              text=True, timeout=3600)
            log.append({'step': 'Stage E (literature-grounded grain corrections)',
                        'stdout': stage_e_result.stdout,
                        'stderr': stage_e_result.stderr,
                        'rc': stage_e_result.returncode})
        except Exception as _e:
            log.append({'step': 'Stage E (literature-grounded grain corrections)',
                        'stdout': '', 'stderr': str(_e), 'rc': 1})

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
                      'sigma_bruggeman', 'sigma_bruggeman_mScm', 'R_bruggeman_over_full',
                      # Physics-mode (Tabor + volume) baselines — required for
                      # Stage E Physics column. Without merging these, the UI
                      # 4-col layout shows '—' Physics even when the solver
                      # successfully computed both modes.
                      'sigma_full_physics', 'sigma_full_mScm_physics',
                      'sigma_bulk_net_physics', 'sigma_bulk_net_mScm_physics',
                      'electronic_sigma_full_mScm_physics',
                      'thermal_sigma_full_mScm_physics',
                      'bulk_resistance_fraction_physics',
                      'R_brug_over_full_physics']

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
                        # Stage E refresh — the network solver just rewrote
                        # the baseline σ_* keys, so Stage E σ_*_stage_e and
                        # the validation_flags self-report card must be
                        # regenerated to stay in sync.  Same call shape as
                        # /analyze and archive_reanalyze.
                        try:
                            subprocess.run(['python3',
                                             os.path.join(app.config['SCRIPTS_FOLDER'],
                                                          'run_network_full_corrections.py'),
                                             case_id, '--quiet'],
                                            capture_output=True, text=True,
                                            timeout=3600)
                        except Exception as _se:
                            print(f"  [Stage E] retry-network refresh failed: {_se}")
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

                # 5) Stage E refresh — writes σ_ionic/σ_e/κ _stage_e keys +
                #    validation_flags self-report card.  Idempotent (overwrites
                #    previous Stage E with fresh-baseline-derived corrections).
                #    Same call shape as the /analyze pipeline; without this the
                #    Trust card stays blank and the /audit dashboard shows the
                #    case as 'no-stage-e' after a batch rerun.
                subprocess.run(['python3',
                                 os.path.join(scripts, 'run_network_full_corrections.py'),
                                 c['cid'], '--quiet'],
                               capture_output=True, text=True, timeout=3600)

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

    # Load input_params.json first — needed by inject_cell_asr_rows for
    # RVE area (box_x × box_y × scale²)
    input_params = {}
    params_path = os.path.join(results_dir, 'input_params.json')
    if os.path.exists(params_path):
        with open(params_path) as f:
            input_params = json.load(f)
    if input_params and 'scale' not in input_params:
        input_params['scale'] = meta.get('scale', 1)

    # 4-column transform + section injection (Network Solver + AM-AM) — shared helper
    transform_network_summary_4col(tables, metrics, meta)
    inject_tier1_patch_rows(tables, metrics)
    inject_stage_e_rows(tables, metrics)
    inject_cell_asr_rows(tables, metrics, input_params)
    # Final pre-rename pass: enforce identical row layout across all cases
    normalize_network_summary_layout(tables, metrics)
    # Final pass: replace informal labels with paper-style academic notation
    apply_paper_labels(tables)

    # Brittle-fracture summary tab (auto-built from full_metrics.json keys)
    fracture_tbl = build_fracture_summary_table(metrics)
    if fracture_tbl is not None:
        tables['fracture_summary'] = fracture_tbl

    return render_template('single.html', case=meta, figures=figures,
                         report=report, tables=tables, metrics=metrics,
                         input_params=input_params, archive_path=archive_path,
                         trust_card=_build_trust_card(metrics))

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
        'am_se_stress_pairs': [],
        'se_states': {}, 'tabor_stats': {}, 'all_se_ids': [],
        'se_engagement': {},
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
            import time as _t
            # Aux cache — particulate cases with sub-μm SE balloon to
            # 2-3 M contacts; recomputing aux on every page load would
            # be a 60-90 s endpoint.  Cache the aggregate dict on disk
            # under viewer_aux.json keyed by contacts.csv mtime; next
            # load is then instant.
            cache_path = os.path.join(results_dir, 'viewer_aux.json')
            contacts_mtime = os.path.getmtime(contacts_csv)
            cache_valid = False
            if os.path.exists(cache_path):
                try:
                    with open(cache_path) as _cf:
                        cached = json.load(_cf)
                    if cached.get('_contacts_mtime') == contacts_mtime:
                        for k in ('stress_max', 'dr_max', 'brittle_pairs',
                                   'se_stress_pairs', 'am_se_stress_pairs',
                                   'se_states', 'tabor_stats', 'all_se_ids',
                                   'se_engagement'):
                            if k in cached:
                                # JSON dicts come back with str keys —
                                # convert int-keyed dicts back to ints
                                # so the frontend's `engagement[p.id]`
                                # numeric-key lookup works.
                                if k in ('stress_max', 'dr_max',
                                         'se_engagement'):
                                    aux[k] = {int(kk): v for kk, v
                                               in cached[k].items()}
                                else:
                                    aux[k] = cached[k]
                        cache_valid = True
                        print(f'  [3d-data aux] cache HIT')
                except (OSError, ValueError, KeyError) as _ce:
                    print(f'  [3d-data aux] cache invalid: {_ce}')

            if not cache_valid:
                _t0 = _t.time()
                contacts_df = pd.read_csv(contacts_csv, low_memory=False)
                _t1 = _t.time()
                n_rows = len(contacts_df)
                print(f'  [3d-data aux] contacts.csv: {n_rows} rows, '
                      f'read in {_t1-_t0:.1f}s')
                # 5 M rows ≈ 2-3 GB peak via to_dict; switching to a
                # streaming itertuples → dict generator drops peak
                # memory to ~200 MB and runs in ~30-90 s on commodity
                # workstations.  Cases above 5 M stay skipped (still
                # very rare — would require sub-100 nm SE).
                if n_rows > 5_000_000:
                    print(f'  [3d-data aux] skipping aggregate '
                          f'(> 5 M rows; out-of-budget)')
                else:
                    _cols = list(contacts_df.columns)
                    def _stream_records(df, cols=_cols):
                        # yield one dict per row — lazy, no upfront
                        # materialisation of 2-3 M dicts in memory.
                        for tup in df.itertuples(index=False, name=None):
                            yield dict(zip(cols, tup))
                    _t2 = _t.time()
                    agg = aggregate_particle_metrics(
                        _stream_records(contacts_df),
                        atoms_by_id, type_map, scale=scale)
                    _t3 = _t.time()
                    print(f'  [3d-data aux] streaming aggregate '
                          f'in {_t3-_t2:.1f}s (total {_t3-_t0:.1f}s)')
                    aux['stress_max']         = agg['stress_max']
                    aux['dr_max']             = agg['dr_max']
                    aux['brittle_pairs']      = agg['brittle_pairs']
                    aux['se_stress_pairs']    = agg['se_stress_pairs']
                    aux['am_se_stress_pairs'] = agg.get('am_se_stress_pairs', [])
                    aux['se_states']          = agg.get('se_states', {})
                    aux['tabor_stats']        = agg.get('tabor_stats', {})
                    aux['all_se_ids']         = agg.get('all_se_ids', [])
                    aux['se_engagement']      = agg.get('se_engagement', {})

                    # Write cache so subsequent page loads are instant.
                    try:
                        cache_blob = dict(aux)
                        cache_blob['_contacts_mtime'] = contacts_mtime
                        with open(cache_path, 'w') as _cf:
                            json.dump(cache_blob, _cf, default=str)
                        print(f'  [3d-data aux] cache WROTE → '
                              f'{os.path.basename(cache_path)}')
                    except OSError as _we:
                        print(f'  [3d-data aux] cache write failed: {_we}')
        aux['cluster_meta']      = classify_clusters(clusters)
        aux['cluster_id_per_se'] = {str(k): v for k, v in
                                     build_cluster_id_map(clusters).items()}
        aux['coverage_per_am']   = {str(k): v for k, v in build_coverage_map(
            os.path.join(results_dir, 'coverage_per_am.csv')).items()}
    except Exception as _e:
        # Aux data is best-effort — don't break the viewer if it fails.
        import traceback
        print(f'  [3d-data aux] FAILED: {type(_e).__name__}: {_e}')
        traceback.print_exc()

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


def _brittle_z_csv_response(case_dir, case_name):
    """Compute brittle z-profile on demand and stream as CSV download.
    Shared helper for /results/<id> and /archive/results/<path> endpoints.
    """
    import csv as _csv
    import io as _io
    import sys as _sys
    _scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
    if _scripts_dir not in _sys.path:
        _sys.path.insert(0, _scripts_dir)
    if not (os.path.exists(os.path.join(case_dir, 'atoms.csv'))
            and os.path.exists(os.path.join(case_dir, 'contacts.csv'))):
        return ('atoms.csv or contacts.csv missing', 404)
    # meta.json optional — _load_case has its own fallbacks.
    from plot_brittle_z_distribution import (
        compute_brittle_zprofile, profile_to_csv_rows,
    )
    bins = int(request.args.get('bins', 25))
    try:
        profile = compute_brittle_zprofile(case_dir, bins=bins)
        buf = _io.StringIO()
        _csv.writer(buf).writerows(profile_to_csv_rows(profile))
    except Exception as e:
        import traceback
        traceback.print_exc()
        return (f'{type(e).__name__}: {e}', 500)
    resp = make_response(buf.getvalue())
    resp.headers['Content-Type'] = 'text/csv; charset=utf-8'
    resp.headers['Content-Disposition'] = (
        f'attachment; filename="brittle_z_{case_name}.csv"')
    return resp


def _brittle_z_profile_compute(case_dir, bins=25):
    """Shared loader used by data / png / csv helpers."""
    import sys as _sys
    _scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
    if _scripts_dir not in _sys.path:
        _sys.path.insert(0, _scripts_dir)
    from plot_brittle_z_distribution import compute_brittle_zprofile
    return compute_brittle_zprofile(case_dir, bins=bins)


def _brittle_z_data_response(case_dir, case_name):
    """Return brittle z-profile as JSON for the modal's table."""
    if not (os.path.exists(os.path.join(case_dir, 'atoms.csv'))
            and os.path.exists(os.path.join(case_dir, 'contacts.csv'))):
        return jsonify({'error': 'atoms.csv or contacts.csv missing'}), 404
    # meta.json is optional — _load_case now falls back to
    # input_params.json or project defaults (scale=1000,
    # type_map={1:AM_P,2:AM_S,3:SE}).
    bins = int(request.args.get('bins', 25))
    try:
        profile = _brittle_z_profile_compute(case_dir, bins=bins)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': f'{type(e).__name__}: {e}',
        }), 500
    # numpy arrays → plain lists for JSON
    return jsonify({
        'case_name':      case_name,
        'thickness_um':   float(profile['thickness_um']),
        'n_total':        int(profile['n_total']),
        'n_damaged':      int(profile['n_damaged']),
        'damaged_pct':    float(profile['damaged_pct']),
        'bin_centers_um': [float(x) for x in profile['bin_centers_um']],
        'bin_edges_um':   [float(x) for x in profile['bin_edges_um']],
        'counts': {k: [int(x) for x in v] for k, v in profile['counts'].items()},
        'mean_m':         [float(x) for x in profile['mean_m']],
        'stage_totals':   {k: int(v) for k, v in profile['stage_totals'].items()},
        'counts_by_pair': {
            pt: {s: [int(x) for x in arr] for s, arr in stages.items()}
            for pt, stages in (profile.get('counts_by_pair') or {}).items()
        },
        'pair_totals':    {k: int(v) for k, v in
                            (profile.get('pair_totals') or {}).items()},
    })


def _brittle_z_png_response(case_dir, case_name):
    """Render the 3-panel brittle z-profile figure server-side and stream PNG."""
    import io as _io
    if not (os.path.exists(os.path.join(case_dir, 'atoms.csv'))
            and os.path.exists(os.path.join(case_dir, 'contacts.csv'))):
        return ('atoms.csv or contacts.csv missing', 404)
    # meta.json optional — _load_case has its own fallbacks.
    bins = int(request.args.get('bins', 25))
    try:
        profile = _brittle_z_profile_compute(case_dir, bins=bins)
        import sys as _sys
        _scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
        if _scripts_dir not in _sys.path:
            _sys.path.insert(0, _scripts_dir)
        from plot_brittle_z_distribution import render_brittle_figure
        fig = render_brittle_figure(profile)
        buf = _io.BytesIO()
        fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        import matplotlib.pyplot as plt
        plt.close(fig)
        buf.seek(0)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return (f'{type(e).__name__}: {e}', 500)
    return send_file(buf, mimetype='image/png', as_attachment=False,
                      download_name=f'brittle_z_{case_name}.png')


@app.route('/results/<case_id>/brittle-z-csv')
def serve_brittle_z_csv(case_id):
    results_dir = get_results_dir(case_id)
    return _brittle_z_csv_response(results_dir, case_id)


@app.route('/results/<case_id>/brittle-z-data')
def serve_brittle_z_data(case_id):
    return _brittle_z_data_response(get_results_dir(case_id), case_id)


@app.route('/results/<case_id>/brittle-z-png')
def serve_brittle_z_png(case_id):
    return _brittle_z_png_response(get_results_dir(case_id), case_id)


# ── Stress-hotspot z-profile (analogous to brittle z-profile) ───────
def _stress_z_profile_compute(case_dir, bins=25):
    import sys as _sys
    _scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
    if _scripts_dir not in _sys.path:
        _sys.path.insert(0, _scripts_dir)
    from plot_stress_z_distribution import compute_stress_zprofile
    return compute_stress_zprofile(case_dir, bins=bins)


def _stress_z_data_response(case_dir, case_name):
    if not (os.path.exists(os.path.join(case_dir, 'atoms.csv'))
            and os.path.exists(os.path.join(case_dir, 'contacts.csv'))):
        return jsonify({'error': 'atoms.csv or contacts.csv missing'}), 404
    bins = int(request.args.get('bins', 25))
    try:
        profile = _stress_z_profile_compute(case_dir, bins=bins)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'{type(e).__name__}: {e}'}), 500
    return jsonify({
        'case_name':       case_name,
        'thickness_um':    float(profile['thickness_um']),
        'n_total':         int(profile['n_total']),
        'n_with_stress':   int(profile['n_with_stress']),
        'bin_centers_um':  [float(x) for x in profile['bin_centers_um']],
        'bin_edges_um':    [float(x) for x in profile['bin_edges_um']],
        'counts_per_type': {k: [int(x) for x in v]
                             for k, v in profile['counts_per_type'].items()},
        'counts_by_bracket': {k: [int(x) for x in v]
                              for k, v in profile['counts_by_bracket'].items()},
        'mean_MPa':        [float(x) for x in profile['mean_MPa']],
        'median_MPa':      [float(x) for x in profile['median_MPa']],
        'p95_MPa':         [float(x) for x in profile['p95_MPa']],
        'max_MPa':         [float(x) for x in profile['max_MPa']],
        'bracket_edges_MPa': [float(x) for x in profile['bracket_edges_MPa']],
        'type_totals':     {k: int(v) for k, v in profile['type_totals'].items()},
        'sLo':  float(profile['sLo']),  'sMed': float(profile['sMed']),
        'sHi':  float(profile['sHi']),  'sMax': float(profile['sMax']),
    })


def _stress_z_png_response(case_dir, case_name):
    import io as _io
    if not (os.path.exists(os.path.join(case_dir, 'atoms.csv'))
            and os.path.exists(os.path.join(case_dir, 'contacts.csv'))):
        return ('atoms.csv or contacts.csv missing', 404)
    bins = int(request.args.get('bins', 25))
    try:
        profile = _stress_z_profile_compute(case_dir, bins=bins)
        import sys as _sys
        _scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
        if _scripts_dir not in _sys.path:
            _sys.path.insert(0, _scripts_dir)
        from plot_stress_z_distribution import render_stress_figure
        fig = render_stress_figure(profile)
        buf = _io.BytesIO()
        fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        import matplotlib.pyplot as plt
        plt.close(fig); buf.seek(0)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return (f'{type(e).__name__}: {e}', 500)
    return send_file(buf, mimetype='image/png', as_attachment=False,
                      download_name=f'stress_z_{case_name}.png')


def _stress_z_csv_response(case_dir, case_name):
    import csv as _csv
    import io as _io
    if not (os.path.exists(os.path.join(case_dir, 'atoms.csv'))
            and os.path.exists(os.path.join(case_dir, 'contacts.csv'))):
        return ('atoms.csv or contacts.csv missing', 404)
    bins = int(request.args.get('bins', 25))
    try:
        profile = _stress_z_profile_compute(case_dir, bins=bins)
        import sys as _sys
        _scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
        if _scripts_dir not in _sys.path:
            _sys.path.insert(0, _scripts_dir)
        from plot_stress_z_distribution import profile_to_csv_rows
        buf = _io.StringIO()
        _csv.writer(buf).writerows(profile_to_csv_rows(profile))
    except Exception as e:
        import traceback
        traceback.print_exc()
        return (f'{type(e).__name__}: {e}', 500)
    resp = make_response(buf.getvalue())
    resp.headers['Content-Type'] = 'text/csv; charset=utf-8'
    resp.headers['Content-Disposition'] = (
        f'attachment; filename="stress_z_{case_name}.csv"')
    return resp


@app.route('/results/<case_id>/stress-z-data')
def serve_stress_z_data(case_id):
    return _stress_z_data_response(get_results_dir(case_id), case_id)

@app.route('/results/<case_id>/stress-z-png')
def serve_stress_z_png(case_id):
    return _stress_z_png_response(get_results_dir(case_id), case_id)

@app.route('/results/<case_id>/stress-z-csv')
def serve_stress_z_csv(case_id):
    return _stress_z_csv_response(get_results_dir(case_id), case_id)


# ── Combined (Brittle + Stress) z-profile — overlay PNG / merged CSV ──
def _combined_z_png_response(case_dir, case_name):
    import io as _io
    if not (os.path.exists(os.path.join(case_dir, 'atoms.csv'))
            and os.path.exists(os.path.join(case_dir, 'contacts.csv'))):
        return ('atoms.csv or contacts.csv missing', 404)
    bins = int(request.args.get('bins', 25))
    try:
        import sys as _sys
        _scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
        if _scripts_dir not in _sys.path:
            _sys.path.insert(0, _scripts_dir)
        from plot_combined_z_distribution import (
            compute_combined_zprofile, render_combined_figure,
        )
        profile = compute_combined_zprofile(case_dir, bins=bins)
        fig = render_combined_figure(profile)
        buf = _io.BytesIO()
        fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        import matplotlib.pyplot as plt
        plt.close(fig); buf.seek(0)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return (f'{type(e).__name__}: {e}', 500)
    return send_file(buf, mimetype='image/png', as_attachment=False,
                      download_name=f'combined_z_{case_name}.png')


def _combined_z_csv_response(case_dir, case_name):
    import csv as _csv
    import io as _io
    if not (os.path.exists(os.path.join(case_dir, 'atoms.csv'))
            and os.path.exists(os.path.join(case_dir, 'contacts.csv'))):
        return ('atoms.csv or contacts.csv missing', 404)
    bins = int(request.args.get('bins', 25))
    try:
        import sys as _sys
        _scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
        if _scripts_dir not in _sys.path:
            _sys.path.insert(0, _scripts_dir)
        from plot_combined_z_distribution import (
            compute_combined_zprofile, profile_to_csv_rows,
        )
        profile = compute_combined_zprofile(case_dir, bins=bins)
        buf = _io.StringIO()
        _csv.writer(buf).writerows(profile_to_csv_rows(profile))
    except Exception as e:
        import traceback
        traceback.print_exc()
        return (f'{type(e).__name__}: {e}', 500)
    resp = make_response(buf.getvalue())
    resp.headers['Content-Type'] = 'text/csv; charset=utf-8'
    resp.headers['Content-Disposition'] = (
        f'attachment; filename="combined_z_{case_name}.csv"')
    return resp


@app.route('/results/<case_id>/combined-z-png')
def serve_combined_z_png(case_id):
    return _combined_z_png_response(get_results_dir(case_id), case_id)

@app.route('/results/<case_id>/combined-z-csv')
def serve_combined_z_csv(case_id):
    return _combined_z_csv_response(get_results_dir(case_id), case_id)


# ── Coverage z-profile (per-AM SE-coverage %) ───────────────────────
def _coverage_z_profile_compute(case_dir, bins=25):
    import sys as _sys
    _scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
    if _scripts_dir not in _sys.path:
        _sys.path.insert(0, _scripts_dir)
    from plot_coverage_z_distribution import compute_coverage_zprofile
    return compute_coverage_zprofile(case_dir, bins=bins)


def _coverage_z_data_response(case_dir, case_name):
    if not (os.path.exists(os.path.join(case_dir, 'atoms.csv'))
            and os.path.exists(os.path.join(case_dir, 'coverage_per_am.csv'))):
        return jsonify({'error': 'atoms.csv or coverage_per_am.csv missing'}), 404
    bins = int(request.args.get('bins', 25))
    try:
        profile = _coverage_z_profile_compute(case_dir, bins=bins)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'{type(e).__name__}: {e}'}), 500
    return jsonify({
        'case_name':       case_name,
        'thickness_um':    float(profile['thickness_um']),
        'n_with_cov':      int(profile['n_with_cov']),
        'bin_centers_um':  [float(x) for x in profile['bin_centers_um']],
        'bin_edges_um':    [float(x) for x in profile['bin_edges_um']],
        'counts_per_type': {k: [int(x) for x in v]
                             for k, v in profile['counts_per_type'].items()},
        'counts_by_band':  {k: [int(x) for x in v]
                             for k, v in profile['counts_by_band'].items()},
        'mean_pct':        [float(x) for x in profile['mean_pct']],
        'median_pct':      [float(x) for x in profile['median_pct']],
        'p5_pct':          [float(x) for x in profile['p5_pct']],
        'p95_pct':         [float(x) for x in profile['p95_pct']],
        'band_edges_pct':  [float(x) for x in profile['band_edges_pct']],
        'type_totals':     {k: int(v) for k, v in profile['type_totals'].items()},
        'cLo':  float(profile['cLo']),  'cMed': float(profile['cMed']),
        'cHi':  float(profile['cHi']),  'cMean': float(profile['cMean']),
    })


def _coverage_z_png_response(case_dir, case_name):
    import io as _io
    if not (os.path.exists(os.path.join(case_dir, 'atoms.csv'))
            and os.path.exists(os.path.join(case_dir, 'coverage_per_am.csv'))):
        return ('atoms.csv or coverage_per_am.csv missing', 404)
    bins = int(request.args.get('bins', 25))
    try:
        profile = _coverage_z_profile_compute(case_dir, bins=bins)
        import sys as _sys
        _scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
        if _scripts_dir not in _sys.path:
            _sys.path.insert(0, _scripts_dir)
        from plot_coverage_z_distribution import render_coverage_figure
        fig = render_coverage_figure(profile)
        buf = _io.BytesIO()
        fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        import matplotlib.pyplot as plt
        plt.close(fig); buf.seek(0)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return (f'{type(e).__name__}: {e}', 500)
    return send_file(buf, mimetype='image/png', as_attachment=False,
                      download_name=f'coverage_z_{case_name}.png')


def _coverage_z_csv_response(case_dir, case_name):
    import csv as _csv
    import io as _io
    if not (os.path.exists(os.path.join(case_dir, 'atoms.csv'))
            and os.path.exists(os.path.join(case_dir, 'coverage_per_am.csv'))):
        return ('atoms.csv or coverage_per_am.csv missing', 404)
    bins = int(request.args.get('bins', 25))
    try:
        profile = _coverage_z_profile_compute(case_dir, bins=bins)
        import sys as _sys
        _scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
        if _scripts_dir not in _sys.path:
            _sys.path.insert(0, _scripts_dir)
        from plot_coverage_z_distribution import profile_to_csv_rows
        buf = _io.StringIO()
        _csv.writer(buf).writerows(profile_to_csv_rows(profile))
    except Exception as e:
        import traceback
        traceback.print_exc()
        return (f'{type(e).__name__}: {e}', 500)
    resp = make_response(buf.getvalue())
    resp.headers['Content-Type'] = 'text/csv; charset=utf-8'
    resp.headers['Content-Disposition'] = (
        f'attachment; filename="coverage_z_{case_name}.csv"')
    return resp


@app.route('/results/<case_id>/coverage-z-data')
def serve_coverage_z_data(case_id):
    return _coverage_z_data_response(get_results_dir(case_id), case_id)

@app.route('/results/<case_id>/coverage-z-png')
def serve_coverage_z_png(case_id):
    return _coverage_z_png_response(get_results_dir(case_id), case_id)

@app.route('/results/<case_id>/coverage-z-csv')
def serve_coverage_z_csv(case_id):
    return _coverage_z_csv_response(get_results_dir(case_id), case_id)


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

        # Stage E (literature-grounded grain corrections) — MUST run after
        # analyze_contacts so the baseline σ_* keys exist for Cronau /
        # Trevisanello / Wang multipliers to scale against.  Same call shape
        # as the /analyze pipeline (line ~2291).  Auto-writes σ_*_stage_e
        # AND the validation_flags self-report card → Trust card on the
        # single.html page header is populated immediately.
        try:
            stage_e_cmd = ['python3',
                            os.path.join(scripts, 'run_network_full_corrections.py'),
                            os.path.basename(target), '--quiet']
            subprocess.run(stage_e_cmd, capture_output=True, text=True,
                            timeout=3600)
        except Exception:
            # Non-fatal — case still has baseline metrics; the audit script
            # will surface this as 'no-stage-e' later.
            pass

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

    # Load input_params first — needed for cell-ASR RVE area
    input_params = {}
    params_path = os.path.join(results_dir, 'input_params.json')
    if os.path.exists(params_path):
        with open(params_path) as f:
            input_params = json.load(f)
    if input_params and 'scale' not in input_params:
        input_params['scale'] = meta.get('scale', 1)

    # 4-column transform + section injection (Network Solver + AM-AM) — shared helper
    transform_network_summary_4col(tables, metrics, meta)

    # Stage E (literature-grounded σ_grain corrections + 7-Layer solver
    # defence + Bruggeman fallback). Mirrors the /single route so archive
    # views surface the same Stage E rows / fallback tags.
    inject_stage_e_rows(tables, metrics)
    # Cell-level ASR (Ohm slab using L_cathode and RVE area)
    inject_cell_asr_rows(tables, metrics, input_params)
    # Final pre-rename pass: enforce identical row layout across all cases
    normalize_network_summary_layout(tables, metrics)
    # Paper-style label rename (mirror /single ordering)
    apply_paper_labels(tables)

    # Brittle-fracture summary tab (built from full_metrics.json keys produced
    # by dem_analysis_core.calc_fracture_stages — auto-DB pipeline). Empty
    # for cases without AM-AM contacts; UI hides the tab when None.
    fracture_tbl = build_fracture_summary_table(metrics)
    if fracture_tbl is not None:
        tables['fracture_summary'] = fracture_tbl

    return render_template('single.html', case=meta, figures=figures,
                         report=report, tables=tables, metrics=metrics,
                         input_params=input_params, archive_path=folder,
                         trust_card=_build_trust_card(metrics))


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
        'am_se_stress_pairs': [],
        'se_states': {}, 'tabor_stats': {}, 'all_se_ids': [],
        'se_engagement': {},
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
            import time as _t
            # Aux cache (same logic as /results/<id>/3d-data above —
            # 2-3 M contact cases would otherwise re-aggregate per page
            # load).  Keyed on contacts.csv mtime.
            cache_path = os.path.join(target, 'viewer_aux.json')
            contacts_mtime = os.path.getmtime(contacts_csv)
            cache_valid = False
            if os.path.exists(cache_path):
                try:
                    with open(cache_path) as _cf:
                        cached = json.load(_cf)
                    if cached.get('_contacts_mtime') == contacts_mtime:
                        for k in ('stress_max', 'dr_max', 'brittle_pairs',
                                   'se_stress_pairs', 'am_se_stress_pairs',
                                   'se_states', 'tabor_stats', 'all_se_ids',
                                   'se_engagement'):
                            if k in cached:
                                if k in ('stress_max', 'dr_max',
                                         'se_engagement'):
                                    aux[k] = {int(kk): v for kk, v
                                               in cached[k].items()}
                                else:
                                    aux[k] = cached[k]
                        cache_valid = True
                        print(f'  [3d-data aux/archive] cache HIT')
                except (OSError, ValueError, KeyError) as _ce:
                    print(f'  [3d-data aux/archive] cache invalid: {_ce}')

            if not cache_valid:
                _t0 = _t.time()
                contacts_df = pd.read_csv(contacts_csv, low_memory=False)
                _t1 = _t.time()
                n_rows = len(contacts_df)
                print(f'  [3d-data aux/archive] contacts.csv: {n_rows} rows, '
                      f'read in {_t1-_t0:.1f}s')
                if n_rows > 5_000_000:
                    print(f'  [3d-data aux/archive] skipping aggregate '
                          f'(> 5 M rows; out-of-budget)')
                else:
                    _cols = list(contacts_df.columns)
                    def _stream_records(df, cols=_cols):
                        for tup in df.itertuples(index=False, name=None):
                            yield dict(zip(cols, tup))
                    _t2 = _t.time()
                    agg = aggregate_particle_metrics(
                        _stream_records(contacts_df),
                        atoms_by_id, type_map, scale=scale)
                    _t3 = _t.time()
                    print(f'  [3d-data aux/archive] streaming aggregate '
                          f'in {_t3-_t2:.1f}s (total {_t3-_t0:.1f}s)')
                    aux['stress_max']         = agg['stress_max']
                    aux['dr_max']             = agg['dr_max']
                    aux['brittle_pairs']      = agg['brittle_pairs']
                    aux['se_stress_pairs']    = agg['se_stress_pairs']
                    aux['am_se_stress_pairs'] = agg.get('am_se_stress_pairs', [])
                    aux['se_states']          = agg.get('se_states', {})
                    aux['tabor_stats']        = agg.get('tabor_stats', {})
                    aux['all_se_ids']         = agg.get('all_se_ids', [])
                    aux['se_engagement']      = agg.get('se_engagement', {})
                    try:
                        cache_blob = dict(aux)
                        cache_blob['_contacts_mtime'] = contacts_mtime
                        with open(cache_path, 'w') as _cf:
                            json.dump(cache_blob, _cf, default=str)
                        print(f'  [3d-data aux/archive] cache WROTE')
                    except OSError as _we:
                        print(f'  [3d-data aux/archive] cache write failed: '
                              f'{_we}')
        aux['cluster_meta']      = classify_clusters(clusters)
        aux['cluster_id_per_se'] = {str(k): v for k, v in
                                     build_cluster_id_map(clusters).items()}
        aux['coverage_per_am']   = {str(k): v for k, v in build_coverage_map(
            os.path.join(target, 'coverage_per_am.csv')).items()}
    except Exception as _e:
        import traceback
        print(f'  [3d-data aux/archive] FAILED: '
              f'{type(_e).__name__}: {_e}')
        traceback.print_exc()

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


@app.route('/archive/results/<path:folder>/brittle-z-csv')
def serve_archive_brittle_z_csv(folder):
    target = _safe_path(folder)
    if not target:
        return ('Not found', 404)
    return _brittle_z_csv_response(target, os.path.basename(target.rstrip('/')))


@app.route('/archive/results/<path:folder>/brittle-z-data')
def serve_archive_brittle_z_data(folder):
    target = _safe_path(folder)
    if not target:
        return jsonify({'error': 'Not found'}), 404
    return _brittle_z_data_response(target, os.path.basename(target.rstrip('/')))


@app.route('/archive/results/<path:folder>/brittle-z-png')
def serve_archive_brittle_z_png(folder):
    target = _safe_path(folder)
    if not target:
        return ('Not found', 404)
    return _brittle_z_png_response(target, os.path.basename(target.rstrip('/')))


@app.route('/archive/results/<path:folder>/stress-z-data')
def serve_archive_stress_z_data(folder):
    target = _safe_path(folder)
    if not target:
        return jsonify({'error': 'Not found'}), 404
    return _stress_z_data_response(target, os.path.basename(target.rstrip('/')))


@app.route('/archive/results/<path:folder>/stress-z-png')
def serve_archive_stress_z_png(folder):
    target = _safe_path(folder)
    if not target:
        return ('Not found', 404)
    return _stress_z_png_response(target, os.path.basename(target.rstrip('/')))


@app.route('/archive/results/<path:folder>/stress-z-csv')
def serve_archive_stress_z_csv(folder):
    target = _safe_path(folder)
    if not target:
        return ('Not found', 404)
    return _stress_z_csv_response(target, os.path.basename(target.rstrip('/')))


@app.route('/archive/results/<path:folder>/combined-z-png')
def serve_archive_combined_z_png(folder):
    target = _safe_path(folder)
    if not target:
        return ('Not found', 404)
    return _combined_z_png_response(target, os.path.basename(target.rstrip('/')))


@app.route('/archive/results/<path:folder>/combined-z-csv')
def serve_archive_combined_z_csv(folder):
    target = _safe_path(folder)
    if not target:
        return ('Not found', 404)
    return _combined_z_csv_response(target, os.path.basename(target.rstrip('/')))


@app.route('/archive/results/<path:folder>/coverage-z-data')
def serve_archive_coverage_z_data(folder):
    target = _safe_path(folder)
    if not target:
        return jsonify({'error': 'Not found'}), 404
    return _coverage_z_data_response(target, os.path.basename(target.rstrip('/')))


@app.route('/archive/results/<path:folder>/coverage-z-png')
def serve_archive_coverage_z_png(folder):
    target = _safe_path(folder)
    if not target:
        return ('Not found', 404)
    return _coverage_z_png_response(target, os.path.basename(target.rstrip('/')))


@app.route('/archive/results/<path:folder>/coverage-z-csv')
def serve_archive_coverage_z_csv(folder):
    target = _safe_path(folder)
    if not target:
        return ('Not found', 404)
    return _coverage_z_csv_response(target, os.path.basename(target.rstrip('/')))


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


# ── Trust Audit dashboard ────────────────────────────────────────────
# Walks every case under webapp/results/** + webapp/archive/** that has
# both atoms.csv and full_metrics.json, then renders the 5-gate matrix.
# This is the live counterpart to scripts/audit_validation_flags.py
# (which produces the CSV / LaTeX for the paper).
_AUDIT_GATE_TIPS = {
    'within_bielefeld_range':
        'ASR_ionic ∈ literature range (Bielefeld 2022 / Lee 2020 / Minnmann 2021)',
    'fracture_distribution_realistic':
        'severe % ≤ 50 and ≥1 Lawn stage populated (Lawn 1998 envelope)',
    'solver_input_intact':
        'Stage-E edge-drop ratio ≤ 0.5 (direct Laplacian dominates)',
    'stage_e_le_baseline_sigma_e':
        'Stage-E σ_e ≤ baseline (factor-≤-1 invariant; Bruggeman bound)',
}
_AUDIT_GATES = list(_AUDIT_GATE_TIPS.keys())


def _audit_discover_cases():
    """Yield (display_id, url, results_dir) for every case that has a
    full_metrics.json regardless of archive vs results location."""
    out = []
    archive_root = app.config.get('ARCHIVE_FOLDER')
    results_root = app.config.get('RESULTS_FOLDER')
    seen = set()

    # archive cases (path-based view URL)
    if archive_root and os.path.isdir(archive_root):
        for dirpath, _, files in os.walk(archive_root):
            if 'full_metrics.json' in files and 'atoms.csv' in files:
                rel = os.path.relpath(dirpath, archive_root)
                if rel in seen:
                    continue
                seen.add(rel)
                out.append((os.path.basename(dirpath),
                            url_for('archive_view', folder=rel),
                            dirpath, rel))

    # local results cases (id-based view URL)
    if results_root and os.path.isdir(results_root):
        for case_id in os.listdir(results_root):
            d = os.path.join(results_root, case_id)
            if (os.path.isdir(d)
                    and os.path.exists(os.path.join(d, 'full_metrics.json'))):
                if case_id in seen:
                    continue
                seen.add(case_id)
                out.append((case_id,
                            url_for('single', case_id=case_id),
                            d, None))
    return out


def _audit_load_row(display_id, url, results_dir, archive_rel):
    try:
        with open(os.path.join(results_dir, 'full_metrics.json')) as f:
            fm = json.load(f)
    except (OSError, ValueError):
        return None

    flags = fm.get('validation_flags') or {}
    campaign = fm.get('campaign') or fm.get('source_case')
    source_case = fm.get('source_case')

    # Pull campaign / source_case from meta.json or input_params.json
    # if missing in full_metrics
    for fname in ('meta.json', 'input_params.json'):
        if campaign and source_case:
            break
        p = os.path.join(results_dir, fname)
        if not os.path.exists(p):
            continue
        try:
            with open(p) as f:
                meta = json.load(f)
            campaign = campaign or meta.get('campaign')
            source_case = source_case or meta.get('source_case') \
                or meta.get('name') or meta.get('case_id')
        except (OSError, ValueError):
            continue

    # Build per-gate cells
    gates = []
    n_fail = n_assess = 0
    for k in _AUDIT_GATES:
        v = flags.get(k)
        if v is None:
            gates.append({'cls': 'na', 'symbol': '—', 'tip': _AUDIT_GATE_TIPS[k] + ' (not assessable)'})
        elif v:
            gates.append({'cls': 'pass', 'symbol': '✓', 'tip': _AUDIT_GATE_TIPS[k]})
            n_assess += 1
        else:
            gates.append({'cls': 'fail', 'symbol': '✗', 'tip': _AUDIT_GATE_TIPS[k] + ' — FAILED'})
            n_fail += 1
            n_assess += 1

    # Bruggeman indicator (5th column, polarity flipped)
    brugg = flags.get('bruggeman_fallback_fired_any')
    if brugg is None:
        gates.append({'cls': 'na', 'symbol': '—', 'tip': 'Bruggeman fallback status unknown'})
    elif brugg:
        gates.append({'cls': 'fail', 'symbol': '●', 'tip': 'Bruggeman fallback fired (EMT carried part of solve)'})
    else:
        gates.append({'cls': 'pass', 'symbol': '○', 'tip': 'Direct solver throughout (no EMT fallback)'})

    if n_assess == 0:
        verdict, verdict_cls = 'N/A', 'na'
    elif n_fail == 0:
        verdict, verdict_cls = '✓ Trust', 'trust'
    elif n_fail == 1:
        verdict, verdict_cls = '~ Warn', 'warn'
    else:
        verdict, verdict_cls = '✗ Untrust', 'fail'

    return {
        'case_dir': display_id,
        'display_id': source_case or display_id,
        'campaign': campaign,
        'source_case': source_case,
        'url': url,
        'gates': gates,
        'brugg_fired': bool(brugg),
        'verdict': verdict,
        'verdict_cls': verdict_cls,
        'archive_rel': archive_rel,
    }


@app.route('/audit')
def audit():
    rows = []
    counts = {'trust': 0, 'warn': 0, 'fail': 0, 'na': 0}
    for display_id, url, results_dir, archive_rel in _audit_discover_cases():
        row = _audit_load_row(display_id, url, results_dir, archive_rel)
        if row is None:
            continue
        rows.append(row)
        counts[row['verdict_cls']] = counts.get(row['verdict_cls'], 0) + 1

    rows.sort(key=lambda r: (r['verdict_cls'] != 'fail',
                              r['verdict_cls'] != 'warn',
                              (r['campaign'] or ''),
                              r['display_id']))

    return render_template('audit.html',
                           rows=rows, counts=counts, total=len(rows))


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
