"""
DEM Analysis Web Application
- Single mode: Upload one case → full analysis pipeline → figures + MD report
- Group mode: Upload multiple cases → comparison plots + summary report
"""
import os
import sys
import re
import csv
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
    redirect, url_for, send_file, make_response, abort,
)
import storage_sync
import predictor_engine
import structure_predictor
import mpm_lab_register           # MPM payload 등록 훅과 meta 스키마 공유 (single source of truth)

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
    # ★ sigma_grain / sigma_grain_note 는 **함수**로 주입한다 (값이 아니라).  값을 route 마다
    #   render_template(..., sigma_grain=...) 로 넘기는 방식이면 새 route 가 하나 생길 때
    #   조용히 빠지고 템플릿은 그대로 옛 bare 3.0 을 쓰게 된다 — 실제로 single.html 이
    #   그 상태였다(2026-07-28 재검증 HIGH-e: app.py 는 깨끗한데 템플릿에 3.0 이 살아있음).
    #   전역 함수면 어떤 route 로 렌더되든 템플릿이 스스로 정본을 호출한다.
    return {'asset_version': _ASSET_VERSION,
            'sigma_grain': lambda m=None: _sigma_grain_context(m)[0],
            'sigma_grain_note': lambda m=None: _sigma_grain_context(m)[1]}


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

_here = os.path.dirname(__file__)
# Data folders are env-overridable so a SECOND checkout (e.g. a git-worktree
# webapp runner) can point at a SHARED data dir WITHOUT symlinking results/ —
# symlinking webapp/results breaks `git pull` because the repo tracks
# webapp/results/reports/*.md ("beyond a symbolic link").  Set WEBAPP_*_FOLDER
# (env or .env) to the shared absolute path; defaults stay in-tree.
app.config['UPLOAD_FOLDER'] = os.environ.get('WEBAPP_UPLOAD_FOLDER') or os.path.join(_here, 'uploads')
app.config['RESULTS_FOLDER'] = os.environ.get('WEBAPP_RESULTS_FOLDER') or os.path.join(_here, 'results')
app.config['SCRIPTS_FOLDER'] = os.path.join(os.path.dirname(_here), 'scripts')
app.config['ARCHIVE_FOLDER'] = os.environ.get('WEBAPP_ARCHIVE_FOLDER') or os.path.join(_here, 'archive')
# standalone MPM/도전재 payload viewer — independent of the DEM case list (upload mpm_payload.json,
# view in 3D, keep an accumulating saved list).  Each saved payload = a subfolder with payload.json + meta.json.
app.config['MPM_LAB_FOLDER'] = os.environ.get('WEBAPP_MPM_LAB_FOLDER') or os.path.join(_here, 'mpm_lab')

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)
os.makedirs(app.config['ARCHIVE_FOLDER'], exist_ok=True)
os.makedirs(app.config['MPM_LAB_FOLDER'], exist_ok=True)

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

def _contained_join(base, sub):
    """Join `sub` under `base` and REJECT path-traversal escapes (defense-in-depth for
    user-supplied case_id).  Legit ids (timestamp_uuid, 'archive:a/b') stay inside base →
    allowed; anything resolving outside base (e.g. '../etc') → 400.  Checked BEFORE makedirs
    so a traversal id cannot even create a stray directory tree."""
    base_r = os.path.realpath(base)
    d = os.path.realpath(os.path.join(base_r, str(sub)))
    if d != base_r and not d.startswith(base_r + os.sep):
        abort(400, 'invalid case id')
    return d

def get_case_dir(case_id):
    d = _contained_join(app.config['UPLOAD_FOLDER'], case_id)
    os.makedirs(d, exist_ok=True)
    return d

def get_results_dir(case_id):
    d = _contained_join(app.config['RESULTS_FOLDER'], case_id)
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
        meta['has_mpm'] = os.path.exists(os.path.join(results_dir, 'mpm_payload.json'))  # MPM result uploaded?
        meta['mpm_regime'] = ''   # filled below (cross-validated / SE-rich / SE-poor) when DEM+MPM porosity both exist
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

            # Stage E completion — for the 3 channels.  Missing Stage E means
            # network_solver ran but run_network_full_corrections.py post-
            # processing didn't fill in *_stage_e_physics keys.  Common for
            # cases analyzed before /analyze was wired to run Stage E, or
            # when Stage E physics-mode failed silently.
            #
            # Distinguish:
            #   - Has Hertz Stage E but missing Physics → backfill possible (orange ⚠)
            #   - No Stage E at all → needs full re-analysis (no badge — covered by
            #     NET ✗ / PHYS ∅ already)
            #   - All 3 Physics channels present → green ✓
            _has_i_h = bool(m.get('sigma_full_mScm_stage_e'))
            _has_e_h = bool(m.get('electronic_sigma_full_mScm_stage_e'))
            _has_k_h = bool(m.get('thermal_sigma_full_mScm_stage_e'))
            _any_hertz_se = _has_i_h or _has_e_h or _has_k_h
            _has_i_p = bool(m.get('sigma_full_mScm_stage_e_physics'))
            _has_e_p = bool(m.get('electronic_sigma_full_mScm_stage_e_physics'))
            _has_k_p = bool(m.get('thermal_sigma_full_mScm_stage_e_physics'))
            meta['stage_e_physics_complete'] = (_has_i_p and _has_e_p and _has_k_p)
            # Only flag ⚠ if BOTH (a) the case has Hertz Stage E AND
            # (b) some Physics channels missing.  Otherwise the case either
            # needs full re-analysis (already covered by NET/PHYS badges) or
            # is fully complete.
            meta['stage_e_physics_missing'] = []
            if _any_hertz_se and not (_has_i_p and _has_e_p and _has_k_p):
                if not _has_i_p: meta['stage_e_physics_missing'].append('σ_ionic')
                if not _has_e_p: meta['stage_e_physics_missing'].append('σ_e')
                if not _has_k_p: meta['stage_e_physics_missing'].append('κ')

            # MPM regime — DEM↔MPM porosity cross-check (gap = DEM − MPM).  Splits the binary
            # "MPM ✓" badge into 3 intuitive states + tells which porosity value to trust:
            #   gap > +4  → SE-poor (out-of-envelope): MPM over-compresses → use DEM   (orange ⚠)
            #   gap < −4  → SE-rich: DEM ε_sphere over-compresses          → use MPM   (blue)
            #   |gap| ≤ 4 → cross-validated (in-envelope)                  → use MPM   (green ✓)
            # docs/data/mpm_dem_porosity_reliability.csv + troubleshooting §16/§17.
            if meta.get('has_mpm'):
                _dem_por = m.get('porosity_spheresum')
                if _dem_por is None:
                    _dem_por = m.get('porosity')
                _mpm_por = None
                _mmf = os.path.join(results_dir, 'mpm_metrics.json')
                if os.path.exists(_mmf):
                    try:
                        with open(_mmf) as _mf:
                            _mpm_por = (json.load(_mf) or {}).get('porosity_mpm_pct')
                    except Exception:
                        _mpm_por = None
                if _dem_por is not None and _mpm_por is not None:
                    _gap = float(_dem_por) - float(_mpm_por)
                    meta['mpm_dem_porosity'] = round(float(_dem_por), 1)
                    meta['mpm_porosity'] = round(float(_mpm_por), 1)
                    meta['mpm_gap'] = round(_gap, 1)
                    if _gap > 4.0:
                        meta['mpm_regime'] = 'SE-poor';        meta['mpm_use_source'] = 'DEM'
                    elif _gap < -4.0:
                        meta['mpm_regime'] = 'SE-rich';        meta['mpm_use_source'] = 'MPM'
                    else:
                        meta['mpm_regime'] = 'cross-validated'; meta['mpm_use_source'] = 'MPM'

            # Composite score (overall grade) — used for the 랭킹 filter.
            # Cheap to compute (no SE-aux dependency at the list level;
            # corpus-relative axes drop to N/A here, which is fine).
            try:
                import sys as _sys
                scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
                if scripts_dir not in _sys.path:
                    _sys.path.insert(0, scripts_dir)
                from grade_engine import build_overall_grade
                aux_path = os.path.join(results_dir, 'viewer_aux.json')
                se_aux = None
                if os.path.exists(aux_path):
                    try:
                        with open(aux_path) as af:
                            _aux = json.load(af)
                        se_aux = {
                            'n_percolating':         _aux.get('se_n_percolating'),
                            'articulation_points':   _aux.get('se_articulation_points', []),
                            'n_bn_below_threshold':  _aux.get('se_n_bn_below_threshold'),
                            'n_perc_edges':          _aux.get('se_n_perc_edges'),
                            'bn_median_norm':        _aux.get('se_bn_median_norm'),
                        }
                    except (OSError, ValueError):
                        pass
                corpus_csv = os.path.join(os.path.dirname(__file__), '..',
                                          'docs', 'data', 'se_diagnostics_82.csv')
                if not os.path.exists(corpus_csv):
                    corpus_csv = None
                _gres = build_overall_grade(
                    _inject_input_params(m, results_dir),
                    corpus_csv, se_aux, case_id=case_id)
                meta['overall_score']    = _gres['composite']['score']
                meta['overall_grade']    = _gres['composite']['grade']
                meta['overall_n_axes']   = _gres['composite']['n_axes']
                meta['is_unit_cell']     = _gres['composite'].get('is_unit_cell', False)
                meta['rve_area_um2']     = _gres['composite'].get('rve_area_um2')
                meta['base_case']        = _gres['composite'].get('base_case')
            except Exception:
                meta['overall_score']    = None
                meta['overall_grade']    = '—'
                meta['overall_n_axes']   = 0
                meta['is_unit_cell']     = False
                meta['rve_area_um2']     = None
                meta['base_case']        = None

            # Porosity for the list view (prefer recomputed sphere-sum; fall
            # back to legacy 'porosity').  union + overlap shown in the row
            # tooltip.  (Inside the metrics-exist guard so `m` is always defined;
            # cases with no full_metrics.json simply have no porosity keys.)
            meta['porosity'] = (m.get('porosity_spheresum')
                                if m.get('porosity_spheresum') is not None
                                else m.get('porosity'))
            meta['porosity_union']        = m.get('porosity_union')
            meta['overlap_fraction_pct']  = m.get('overlap_fraction_pct')
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


def _inject_input_params(metrics, results_dir):
    """Pull am_se_ratio (and other input-side parameters needed by the
    grade engine) from input_params.json when not already in metrics.

    Also pulls box_x / box_y so the grade engine can compute the RVE
    cross-section area (μm²) — used as a finite-size noise indicator
    in the dashboard so cases that differ ONLY in RVE size (e.g.
    *_real_x  vs *_real40_x) can be grouped or filtered."""
    if not results_dir:
        return metrics
    ip_path = os.path.join(results_dir, 'input_params.json')
    if not os.path.exists(ip_path):
        return metrics
    try:
        with open(ip_path) as f:
            ip = json.load(f)
    except (OSError, ValueError):
        return metrics
    inj = {}
    ratio = ip.get('am_se_ratio') or ip.get('AM_SE_ratio')
    if ratio:
        inj['_input_am_se_ratio'] = str(ratio)
    # Box dimensions — stored in sim units; convert to μm via scale (default 1000).
    bx = ip.get('box_x'); by = ip.get('box_y')
    scale = ip.get('scale') or 1000
    try:
        if bx is not None and by is not None:
            inj['_input_box_x'] = float(bx) * float(scale)
            inj['_input_box_y'] = float(by) * float(scale)
    except (TypeError, ValueError):
        pass
    # Particle radii (sim units) — convert to μm using scale.  Used by
    # grade_engine's r_SE / λ_eff design axes.
    for k_src, k_dst in (('r_SE', '_input_r_SE_um'),
                          ('r_AM_P', '_input_r_AM_P_um'),
                          ('r_AM_S', '_input_r_AM_S_um')):
        v = ip.get(k_src) or ip.get(k_src + '_sim')
        try:
            if v is not None:
                inj[k_dst] = float(v) * float(scale)
        except (TypeError, ValueError):
            continue
    # Target sintering pressure (sim → MPa via × 1000 historical convention)
    tp = ip.get('target_press_sim') or ip.get('target_pressure_MPa')
    try:
        if tp is not None:
            inj['_input_target_press_MPa'] = float(tp) * 1000 if float(tp) < 10 else float(tp)
    except (TypeError, ValueError):
        pass
    # Mode + ps_ratio from meta.json (for bimodal vs standard detection)
    meta_path = os.path.join(os.path.dirname(results_dir),
                              os.path.basename(results_dir).replace('webapp/results','webapp/uploads')
                              if 'results' in results_dir else os.path.basename(results_dir),
                              'meta.json')
    # Cleaner: look for meta.json near results_dir
    for mp in (os.path.join(results_dir, 'meta.json'),
               os.path.join(os.path.dirname(results_dir), 'meta.json')):
        if os.path.exists(mp):
            try:
                with open(mp) as mf:
                    md = json.load(mf)
                if 'mode' in md:    inj['_meta_mode']     = md['mode']
                if 'ps_ratio' in md: inj['_meta_ps_ratio'] = md['ps_ratio']
                break
            except (OSError, ValueError):
                pass
    if not inj:
        return metrics
    return {**metrics, **inj}


def _se_aux_to_corpus_row(aux):
    """Derive a grade-corpus row (cut_fraction / bn_below_frac / bn_median_norm
    / n_percolating) from a case's viewer_aux.json — same formulas the grade
    engine uses for the case's own value (grade_engine._derived_value)."""
    n_perc = aux.get('se_n_percolating') or aux.get('n_percolating')
    apts = aux.get('se_articulation_points') or aux.get('articulation_points')
    n_cut = aux.get('se_n_articulation_points')
    if n_cut is None and isinstance(apts, list):
        n_cut = len(apts)
    nb = aux.get('se_n_bn_below_threshold')
    ne = aux.get('se_n_perc_edges')
    bmn = aux.get('se_bn_median_norm')
    if not n_perc:
        return None
    row = {'n_percolating': n_perc}
    if n_cut is not None:
        row['cut_fraction'] = n_cut / n_perc
    if nb is not None and ne:
        row['bn_below_frac'] = nb / ne
    if bmn is not None:
        row['bn_median_norm'] = bmn
    return row


_DYN_CORPUS_CACHE = {'rows': None, 'ts': 0.0}
_DYN_CORPUS_TTL = 120  # seconds — re-scan live cases at most this often


def _build_dynamic_corpus_rows(static_csv):
    """Corpus for percentile-ranked grade axes = static baseline (paper's
    se_diagnostics_82.csv) ∪ every live case's SE-diagnostics (viewer_aux.json
    under results/ + archive/).  This makes corpus-relative grades reflect the
    growing dataset and lets sparse columns (e.g. bn_below_frac) become
    scorable once ≥5 cases have them.  Cached for _DYN_CORPUS_TTL seconds."""
    import time
    now = time.time()
    if (_DYN_CORPUS_CACHE['rows'] is not None
            and now - _DYN_CORPUS_CACHE['ts'] < _DYN_CORPUS_TTL):
        return _DYN_CORPUS_CACHE['rows']

    rows = []
    if static_csv and os.path.exists(static_csv):
        try:
            with open(static_csv, newline='') as f:
                rows.extend(list(csv.DictReader(f)))
        except OSError:
            pass

    seen = set()  # dedup live cases by case-dir basename (results preferred)
    for root in (app.config.get('RESULTS_FOLDER'), app.config.get('ARCHIVE_FOLDER')):
        if not root or not os.path.isdir(root):
            continue
        for aux_path in globmod.glob(os.path.join(root, '**', 'viewer_aux.json'),
                                     recursive=True):
            cid = os.path.basename(os.path.dirname(aux_path))
            if cid in seen:
                continue
            try:
                with open(aux_path) as f:
                    aux = json.load(f)
            except (OSError, ValueError):
                continue
            r = _se_aux_to_corpus_row(aux)
            if r:
                rows.append(r)
                seen.add(cid)

    _DYN_CORPUS_CACHE['rows'] = rows
    _DYN_CORPUS_CACHE['ts'] = now
    return rows


def _grade_engine_result(metrics, results_dir=None, carbon_wt_pct=None):
    """Run scripts/grade_engine.build_overall_grade with a DYNAMIC corpus
    (static baseline ∪ live cases) + SE-diagnostics aux wired in (shared by
    the 종합 등급 table and the grade guide).  Returns the result dict or None."""
    if not metrics:
        return None
    try:
        import sys as _sys
        scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
        if scripts_dir not in _sys.path:
            _sys.path.insert(0, scripts_dir)
        from grade_engine import build_overall_grade
    except ImportError:
        return None

    static_csv = os.path.join(os.path.dirname(__file__), '..',
                              'docs', 'data', 'se_diagnostics_82.csv')
    corpus_rows = _build_dynamic_corpus_rows(static_csv)

    # Pull SE diag aux from viewer_aux.json cache if present (avoids
    # recomputing here — the 3D viewer endpoint already populated it).
    se_aux = None
    if results_dir:
        aux_path = os.path.join(results_dir, 'viewer_aux.json')
        if os.path.exists(aux_path):
            try:
                with open(aux_path) as f:
                    _aux = json.load(f)
                se_aux = {
                    'n_percolating':         _aux.get('se_n_percolating'),
                    'articulation_points':   _aux.get('se_articulation_points', []),
                    'n_bn_below_threshold':  _aux.get('se_n_bn_below_threshold'),
                    'n_perc_edges':          _aux.get('se_n_perc_edges'),
                    'bn_median_norm':        _aux.get('se_bn_median_norm'),
                }
            except (OSError, ValueError):
                pass

    metrics = _inject_input_params(metrics, results_dir)
    return build_overall_grade(metrics, se_aux=se_aux,
                               carbon_wt_pct=carbon_wt_pct,
                               corpus_rows=corpus_rows)


def build_overall_grade_table(metrics, results_dir=None, carbon_wt_pct=None):
    """Build a 'overall_grade' table by calling scripts/grade_engine.

    Layout (4 columns) matches the other analysis-summary tabs:
        지표  |  값  |  등급  |  근거
    The 'category' label of each axis becomes a section header row
    (prefix '── … ──') so the template renders as a separator.

    When `carbon_wt_pct` is set (>0), the grade engine applies the
    What-if carbon-additive model so σ_e + ASR_electronic axes use
    the hypothetical σ_e_new.  This is what powers the live ON/OFF
    toggle in the 종합 등급 tab.

    Returns None if metrics is empty or the engine couldn't score any axis.
    """
    if not metrics:
        return None
    try:
        import sys as _sys
        scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
        if scripts_dir not in _sys.path:
            _sys.path.insert(0, scripts_dir)
        from grade_engine import GRADE_COLOR
    except ImportError:
        return None

    result = _grade_engine_result(metrics, results_dir, carbon_wt_pct)
    if result is None:
        return None

    rows = []
    last_cat = None
    for ax in result['axes']:
        if ax['category'] != last_cat:
            rows.append([f"── {ax['category']} ──"])
            last_cat = ax['category']
        v = ax['value']
        if v is None:
            val_str = '—'
        elif abs(v) >= 100:
            val_str = f"{v:.1f}"
        elif abs(v) >= 1:
            val_str = f"{v:.3g}"
        else:
            val_str = f"{v:.4g}"
        score = ax['score']
        score_str = f"{score:.0f}" if score is not None else '—'
        # 등급 cell carries colour + composite hover info via inline span
        color = GRADE_COLOR.get(ax['grade'], '#6b7280')
        grade_html = (f'<span class="grade-badge" '
                      f'style="background:{color}1f;color:{color};'
                      f'border:1px solid {color}55;border-radius:4px;'
                      f'padding:1px 6px;font-weight:600;'
                      f'font-family:ui-monospace,Menlo,monospace">'
                      f'{ax["grade"]}'
                      f'<span style="opacity:.7;font-weight:400;font-size:.85em;'
                      f'margin-left:4px">({score_str})</span></span>')
        # Hover-only basis: tooltip span — same tooltip-row mechanism in
        # single.html picks up data-tip on .metric-label.
        tip = (
            f"<b>{ax['label']}</b><br>"
            f"<span style='color:#9ca3af'>category:</span> {ax['category']}<br>"
            f"<span style='color:#9ca3af'>direction:</span> "
            f"{'higher = better' if ax['direction'] == 'higher' else 'lower = better' if ax['direction'] == 'lower' else ax['direction']}<br>"
            f"<span style='color:#9ca3af'>formula:</span> {ax['formula']}<br>"
            f"<span style='color:#9ca3af'>basis:</span> {ax['basis']}<br>"
            f"<span style='color:#9ca3af'>meaning:</span> {ax['meaning']}"
        )
        rows.append([ax['label'], val_str, grade_html, tip])

    # Composite at the bottom
    comp = result['composite']
    color = GRADE_COLOR.get(comp['grade'], '#6b7280')
    rows.append(['── 종합 ──'])
    rows.append([
        '<b>Overall (가중평균)</b>',
        f"<b>{comp['score']} / 100</b>",
        f'<span class="grade-badge" '
        f'style="background:{color}1f;color:{color};border:2px solid {color};'
        f'border-radius:5px;padding:2px 10px;font-weight:700;font-size:1.05em;'
        f'font-family:ui-monospace,Menlo,monospace">{comp["grade"]}</span>',
        f"<b>{comp['n_axes']} / {comp['n_total']} axes scored</b><br>"
        f"<span style='color:#9ca3af;font-size:.92em'>"
        f"GPA-equivalent: {comp['gpa']} / 4.3 — "
        f"axes carry weights {{1.5 (σ_ionic), 1.4 (ASR_ionic), "
        f"1.2 (활성도/percolation), 0.3 (κ)}} etc.</span>"
    ])

    # Category summary section
    rows.append(['── 카테고리 평균 ──'])
    for cat, score in result['category_scores'].items():
        from grade_engine import score_to_grade  # re-import in-scope
        g = score_to_grade(score)
        c = GRADE_COLOR.get(g, '#6b7280')
        rows.append([cat, f'{score:.1f}',
                      f'<span class="grade-badge" '
                      f'style="background:{c}1f;color:{c};border:1px solid {c}55;'
                      f'border-radius:4px;padding:1px 6px;font-weight:600;'
                      f'font-family:ui-monospace,Menlo,monospace">{g}</span>',
                      ''])

    return {
        'columns': ['지표', '값', '등급', '근거 (hover)'],
        'data':    rows,
        '_composite': comp,
        '_category_scores': result['category_scores'],
    }


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

    return {'columns': ['지표', 'δ-based', 'Force-based ★'], 'data': rows}


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
    # Physics-baseline Stage E
    sigma_i_e_p  = metrics.get('sigma_full_mScm_stage_e_physics')
    sigma_e_e_p  = metrics.get('electronic_sigma_full_mScm_stage_e_physics')
    sigma_th_e_p = metrics.get('thermal_sigma_full_mScm_stage_e_physics')
    # ── PHANTOM σ_e SUPPRESSION (2026-05-28, v2 with fallback-aware) ────
    # If the network-solver electronic pathway didn't actually run, Stage E
    # σ_e is a Bruggeman/Trevisanello phantom fallback (e.g. 1mAh_100_2/_3
    # showed 54-68 mS/cm).  Two phantom flavors:
    #   1. raw electronic_sigma_full_mScm = missing/0  → solver didn't run
    #   2. stage_e_source['sigma_e' / 'sigma_e_physics'] = 'fallback_weighted_factor'
    #      → solver ran but Stage E filled in via Bruggeman fallback
    # Suppress BOTH so the case-detail page reads '—' for the phantom cells.
    # Same for thermal κ pathway.  Ionic σ untouched (ionic pathway hasn't
    # silently failed in the corpus).
    src_fb = metrics.get('stage_e_source') or {}
    raw_e   = metrics.get('electronic_sigma_full_mScm')
    raw_e_p = metrics.get('electronic_sigma_full_mScm_physics')
    e_hertz_phantom = (
        not (isinstance(raw_e, (int, float)) and raw_e and raw_e > 0)
        or src_fb.get('sigma_e') == 'fallback_weighted_factor'
    )
    e_phys_phantom = (
        not (isinstance(raw_e_p, (int, float)) and raw_e_p and raw_e_p > 0)
        or src_fb.get('sigma_e_physics') == 'fallback_weighted_factor'
    )
    if e_hertz_phantom:
        sigma_e_e = None
    if e_phys_phantom:
        sigma_e_e_p = None
    raw_th   = metrics.get('thermal_sigma_full_mScm')
    raw_th_p = metrics.get('thermal_sigma_full_mScm_physics')
    th_hertz_phantom = (
        not (isinstance(raw_th, (int, float)) and raw_th and raw_th > 0)
        or src_fb.get('sigma_thermal') == 'fallback_weighted_factor'
    )
    th_phys_phantom = (
        not (isinstance(raw_th_p, (int, float)) and raw_th_p and raw_th_p > 0)
        or src_fb.get('sigma_thermal_physics') == 'fallback_weighted_factor'
    )
    if th_hertz_phantom:
        sigma_th_e = None
    if th_phys_phantom:
        sigma_th_e_p = None
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
        # Source tags appended (e.g. '⚡ H-fb' if Hertzian fallback fired).
        # 2026-05-28: skip the badge when the value itself was suppressed
        # (val_h/val_p = None) — phantom indicator alongside '—' is redundant.
        tag_parts = []
        if val_h is not None and src_h == 'fallback_weighted_factor':
            tag_parts.append('H:⚡')
        if val_p is not None and src_p == 'fallback_weighted_factor':
            tag_parts.append('P:⚡')
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

    # Phantom σ suppression mirror — must match inject_stage_e_into_metrics
    # 2026-05-28: if the network-solver pathway didn't run OR Stage E used
    # the Bruggeman fallback, suppress the corresponding ASR Stage E cell
    # so the dashboard doesn't report ASR derived from phantom σ.
    _src_fb = metrics.get('stage_e_source') or {}
    def _is_phantom_h(raw_key, src_key):
        rv = metrics.get(raw_key)
        if not (isinstance(rv, (int, float)) and rv and rv > 0):
            return True
        return _src_fb.get(src_key) == 'fallback_weighted_factor'
    _phantom = {
        'electronic_sigma_full_mScm_stage_e':
            _is_phantom_h('electronic_sigma_full_mScm', 'sigma_e'),
        'electronic_sigma_full_mScm_stage_e_physics':
            _is_phantom_h('electronic_sigma_full_mScm_physics', 'sigma_e_physics'),
        'thermal_sigma_full_mScm_stage_e':
            _is_phantom_h('thermal_sigma_full_mScm', 'sigma_thermal'),
        'thermal_sigma_full_mScm_stage_e_physics':
            _is_phantom_h('thermal_sigma_full_mScm_physics', 'sigma_thermal_physics'),
    }

    def _row_for(label, k_h, k_p, k_eh, k_ep, unit='Ω·cm²'):
        """Hertzian / Physics + their Stage E counterparts.
        4-col layout: ASR_H | ASR_P | Δ% (Physics-vs-Hertzian, with Stage E
        side-info). Stage E ASRs (Hertzian + Physics) are reported in the
        Δ-column text so reviewers can read the full picture in one row."""
        asr_h  = _asr_ohm_cm2(metrics.get(k_h))
        asr_p  = _asr_ohm_cm2(metrics.get(k_p) if k_p else None)
        # Stage E ASRs: skip if phantom (mirrors σ-suppression upstream)
        _eh_val = None if (k_eh and _phantom.get(k_eh)) else (metrics.get(k_eh) if k_eh else None)
        _ep_val = None if (k_ep and _phantom.get(k_ep)) else (metrics.get(k_ep) if k_ep else None)
        asr_eh = _asr_ohm_cm2(_eh_val)
        asr_ep = _asr_ohm_cm2(_ep_val)
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


def _suppress_phantom_sigma_rows(data, metrics, debug=False):
    """In-place suppression of σ_e / κ phantom row values.
    Called after layout normalization merges Hertz + Physics rows.
    If stage_e_source flags fallback OR raw network solver output is
    missing, replace the value cells with '—' so dashboard never shows
    Bruggeman-fallback values as if they were real solver output."""
    if debug:
        print(f"[phantom_suppress] called, data has {len(data)} rows")
        print(f"[phantom_suppress] src_fb={metrics.get('stage_e_source')}")
        print(f"[phantom_suppress] raw_e_p={metrics.get('electronic_sigma_full_mScm_physics')}")
        # show σ_e/κ-like rows
        for i, r in enumerate(data):
            if r and len(r) >= 1 and isinstance(r[0], str):
                lbl = r[0]
                if ('σ_e' in lbl or 'σ_electronic' in lbl or
                    'κ' in lbl or 'σ_thermal' in lbl or 'electronic' in lbl):
                    print(f"[phantom_suppress] row {i}: {r}")
    src_fb = metrics.get('stage_e_source') or {}
    p_e_h = (src_fb.get('sigma_e') == 'fallback_weighted_factor'
             or not metrics.get('electronic_sigma_full_mScm'))
    p_e_p = (src_fb.get('sigma_e_physics') == 'fallback_weighted_factor'
             or not metrics.get('electronic_sigma_full_mScm_physics'))
    p_th_h = (src_fb.get('sigma_thermal') == 'fallback_weighted_factor'
              or not metrics.get('thermal_sigma_full_mScm'))
    p_th_p = (src_fb.get('sigma_thermal_physics') == 'fallback_weighted_factor'
              or not metrics.get('thermal_sigma_full_mScm_physics'))
    LABEL_PHANTOM = {
        'σ_electronic (mS/cm)':                              (p_e_h, p_e_p),
        'σ_e — electronic conductivity (mS/cm)':             (p_e_h, p_e_p),
        'σ_electronic [physics] (mS/cm)':                    (p_e_h, p_e_p),
        'σ_e^physics — Tabor plastic film (mS/cm)':          (p_e_h, p_e_p),
        'σ_thermal (mS/cm equiv)':                           (p_th_h, p_th_p),
        'κ — thermal conductivity (mS/cm equiv)':            (p_th_h, p_th_p),
        'σ_thermal [physics] (mS/cm equiv)':                 (p_th_h, p_th_p),
        'κ^physics — Tabor plastic film (mS/cm equiv)':      (p_th_h, p_th_p),
    }
    for r in data:
        if not r or not isinstance(r, list) or len(r) < 2: continue
        lbl = str(r[0]).strip() if r[0] else ''
        if lbl not in LABEL_PHANTOM: continue
        h_phantom, p_phantom = LABEL_PHANTOM[lbl]
        if len(r) >= 2 and h_phantom: r[1] = '—'
        if len(r) >= 3 and p_phantom: r[2] = '—'
        if len(r) >= 4 and (h_phantom or p_phantom): r[3] = '—'


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

    # ── Phantom σ_e / κ suppression (v6 final, 2026-05-28) ──
    # Run AFTER Hertz+Physics merge so we suppress in the unified row.
    # Catches phantom values written from Bruggeman fallback into the raw
    # network solver keys (e.g. 1mAh_100_2 σ_e=61.83).
    _suppress_phantom_sigma_rows(data, metrics)

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
        # full_metrics.json is the source of truth for these baseline σ values.
        # Render None (solver returned no value — didn't converge / didn't
        # percolate) as '—' so "not computed" is visually distinct from a
        # genuine ~0.  Refresh any pre-existing (possibly stale) CSV row from
        # metrics rather than leaving a misleading '0.00'.
        h_val = metrics.get(h_key) if metrics else None
        p_val = metrics.get(p_key) if metrics else None
        h_str = f'{h_val:{fmt[1:]}}' if h_val else '—'
        if p_val is not None:
            p_str = f'{p_val:{fmt[1:]}}'
            d_str = f'{(p_val - h_val) / h_val * 100:+.1f}%' if h_val else '0%'
        else:
            p_str = h_str
            d_str = '0%'
        new_cells = [h_str, p_str, d_str]
        for r in data:
            if (isinstance(r, list) and r and isinstance(r[0], str)
                    and r[0].strip() == label and len(r) >= 4):
                r[1], r[2], r[3] = new_cells
                return
        new_row = [label, *new_cells]
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


def inject_dual_porosity_rows(tables, metrics):
    """Insert ε_union + overlap rows directly under the Porosity row of the
    network_summary structure section.  Values from recompute_porosity_dual.py
    (porosity_union, overlap_fraction_pct).  Porosity is contact-model-
    independent → both columns carry the same value, Δ = 0%.  No-op until the
    dual-porosity fields exist (run recompute_porosity_dual.py or re-analyze).
    Called LAST (after apply_paper_labels) so layout/relabel passes do not move
    the rows; matches the renamed 'Porosity ε (%)' label via startswith."""
    if 'network_summary' not in tables:
        return
    data = tables['network_summary'].get('data')
    if not isinstance(data, list):
        return
    eps_u = metrics.get('porosity_union')
    ov = metrics.get('overlap_fraction_pct')
    if eps_u is None and ov is None:
        return
    ncol = len(tables['network_summary'].get('columns') or []) or 4
    for i, row in enumerate(data):
        if (isinstance(row, list) and row and isinstance(row[0], str)
                and row[0].lstrip().startswith('Porosity')):
            prefix = row[0][: len(row[0]) - len(row[0].lstrip())]
            ins = []
            if eps_u is not None:
                u = f'{eps_u:.1f}'
                ins.append([prefix + 'Porosity ε_union (overlap-corrected, %)', u, u, '0%'])
            if ov is not None:
                o = f'{ov:.2f}'
                ins.append([prefix + 'Overlap fraction (plastic deformation, %)', o, o, '0%'])
            ins = [r[:ncol] + [''] * (ncol - len(r)) for r in ins]
            for k, nr in enumerate(ins):
                data.insert(i + 1 + k, nr)
            break


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

    # ── Phantom σ_e/κ row suppression (2026-05-28, v5 — handles rows
    # built earlier by analyze_contacts.py and saved to disk).
    # If stage_e_source flags fallback, the σ_e / κ row values stored
    # in the pre-built tables were also written from fallback — replace
    # with '—' here so Network Solver row shows '—' consistently.
    _src_fb_n = metrics.get('stage_e_source') or {}
    _phantom_e_h = (_src_fb_n.get('sigma_e') == 'fallback_weighted_factor'
                    or not metrics.get('electronic_sigma_full_mScm'))
    _phantom_e_p = (_src_fb_n.get('sigma_e_physics') == 'fallback_weighted_factor'
                    or not metrics.get('electronic_sigma_full_mScm_physics'))
    _phantom_th_h = (_src_fb_n.get('sigma_thermal') == 'fallback_weighted_factor'
                     or not metrics.get('thermal_sigma_full_mScm'))
    _phantom_th_p = (_src_fb_n.get('sigma_thermal_physics') == 'fallback_weighted_factor'
                     or not metrics.get('thermal_sigma_full_mScm_physics'))
    _e_label_keys = {
        'σ_electronic (mS/cm)':        ('e', 'h'),
        'σ_e — electronic conductivity (mS/cm)': ('e', 'h'),
        'σ_electronic [physics] (mS/cm)': ('e', 'p'),
        'σ_e^physics — Tabor plastic film (mS/cm)': ('e', 'p'),
        'σ_thermal (mS/cm equiv)':     ('th', 'h'),
        'κ — thermal conductivity (mS/cm equiv)': ('th', 'h'),
        'σ_thermal [physics] (mS/cm equiv)': ('th', 'p'),
        'κ^physics — Tabor plastic film (mS/cm equiv)': ('th', 'p'),
    }
    expanded = []
    for row in tbl['data']:
        if not row:
            continue
        label = row[0] if len(row) > 0 else ''
        if isinstance(label, str) and label.strip() in _drop_labels:
            continue
        # Suppress phantom σ_e / κ row VALUES (label stays for layout)
        label_clean = str(label).strip() if label else ''
        if label_clean in _e_label_keys:
            kind, mode = _e_label_keys[label_clean]
            is_phantom = ((kind == 'e' and mode == 'h' and _phantom_e_h)
                          or (kind == 'e' and mode == 'p' and _phantom_e_p)
                          or (kind == 'th' and mode == 'h' and _phantom_th_h)
                          or (kind == 'th' and mode == 'p' and _phantom_th_p))
            if is_phantom:
                # zero out value column(s)
                if len(row) >= 4:
                    row = [row[0], '—', '—', '—']
                else:
                    row = [row[0], '—']
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
                sig_brug = _sigma_grain_mS_cm(metrics) * metrics['sigma_ratio']
                sig_ion_h = metrics.get('sigma_full_mScm')
                sig_ion_p = metrics.get('sigma_full_mScm_physics') or sig_ion_h
                ratio_h = sig_brug / sig_ion_h if sig_ion_h > 0 else 0
                ratio_p = sig_brug / sig_ion_p if sig_ion_p and sig_ion_p > 0 else ratio_h
                net_rows.append(_dual_row('σ_brug / σ_ionic',
                                          ratio_h, ratio_p,
                                          fmt=lambda x: f"{x:.1f}×"))

            # ── τ 3종 비교 (Dijkstra vs Laplace geom vs Laplace eff) ──
            # Derivation only, no re-analysis needed; σ_grain 은 se_material 단일 출처 +
            # 이 런의 온도 provenance 를 따른다 (σ_full 과 같은 T 여야 τ 가 옳다 — _sigma_grain_mS_cm 참조).
            import math as _math
            phi_se = metrics.get('phi_se')
            sig_full = metrics.get('sigma_full_mScm')
            sig_bulk = metrics.get('sigma_bulk_net_mScm')
            tau_dij = metrics.get('tortuosity_mean')
            SIGMA_GRAIN_MS, _sg_note = _sigma_grain_context(metrics)  # [mS/cm] @ 이 런의 T + 혼합경고
            if _sg_note:                                  # ★ S-8: 경고가 표에도 도달해야 한다
                net_rows.append(_dual_row('⚠ σ_grain 온도 정합', _sg_note, _sg_note,
                                          fmt=lambda x: x))
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
            sig_brug = _sigma_grain_mS_cm(metrics) * metrics['sigma_ratio']
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
        SIGMA_GRAIN_MS = _sigma_grain_mS_cm(metrics)   # se_material 단일 출처 + 런의 T provenance
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
                cmd = [sys.executable, os.path.join(scripts, 'parse_liggghts.py')]
                cmd += atom_files + mesh_files + input_files + ['-o', results_dir]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=None)
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
        cmd = [sys.executable, os.path.join(scripts, 'parse_liggghts.py')]
        cmd += atom_files + contact_files + mesh_files + input_files + ['-o', results_dir]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=None)
        log.append({'step': 'Parse', 'stdout': result.stdout, 'stderr': result.stderr, 'rc': result.returncode})
        if result.returncode != 0:
            return {'error': f'Parse failed: {result.stderr}', 'log': log}
    elif has_pre_atoms_only and contact_files:
        # Hybrid: atoms.csv (pre-copied into results_dir above) + contact_*.liggghts.
        # parse_liggghts detects the existing atoms.csv and skips atom parsing.
        cmd = [sys.executable, os.path.join(scripts, 'parse_liggghts.py')]
        cmd += contact_files + mesh_files + input_files + ['-o', results_dir]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=None)
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
        cmd = [sys.executable, os.path.join(scripts, 'analyze_contacts_bimodal.py'),
               atoms_csv, contacts_csv, '-o', results_dir,
               '-t', type_map, '-s', str(scale)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=None)
        log.append({'step': 'Bimodal Contact Analysis', 'stdout': result.stdout, 'stderr': result.stderr, 'rc': result.returncode})

        # Step 2b: Dual-mode coverage + AM-SE/SE-SE totals (Hertzian vs Physics).
        # Writes coverage_AM_*_mean_physics, area_AM전체_SE_total_physics,
        # area_SE_SE_total_physics into full_metrics.json + coverage_per_am.csv.
        cmd = [sys.executable, os.path.join(scripts, 'coverage_physics_vs_hertzian.py'), case_id]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=None)
        log.append({'step': 'Coverage Physics vs Hertzian', 'stdout': result.stdout,
                    'stderr': result.stderr, 'rc': result.returncode})

        # Step 2c: Network solver (both contact modes) → sigma_*_mScm
        cmd = [sys.executable, os.path.join(scripts, 'network_conductivity.py'),
               atoms_csv, contacts_csv, '-o', results_dir,
               '-t', type_map, '-s', str(scale),
               '--contact-mode', 'both']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=None)
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
            stage_e_cmd = [sys.executable,
                            os.path.join(scripts, 'run_network_full_corrections.py'),
                            os.path.basename(results_dir), '--quiet']
            stage_e_result = subprocess.run(stage_e_cmd, capture_output=True,
                                              text=True, timeout=None)
            log.append({'step': 'Stage E (literature-grounded grain corrections)',
                        'stdout': stage_e_result.stdout,
                        'stderr': stage_e_result.stderr,
                        'rc': stage_e_result.returncode})
        except Exception as _e:
            log.append({'step': 'Stage E (literature-grounded grain corrections)',
                        'stdout': '', 'stderr': str(_e), 'rc': 1})

        # Step 2e: Dual porosity (sphere-sum + union + overlap%) — auto-compute
        # so the UI shows ε_sphere / ε_union / overlap without a manual rerun.
        try:
            dual_cmd = [sys.executable,
                        os.path.join(scripts, 'recompute_porosity_dual.py'),
                        '--dir', results_dir]
            dual_res = subprocess.run(dual_cmd, capture_output=True, text=True, timeout=None)
            log.append({'step': 'Dual porosity (sphere-sum / union / overlap)',
                        'stdout': dual_res.stdout, 'stderr': dual_res.stderr,
                        'rc': dual_res.returncode})
        except Exception as _e:
            log.append({'step': 'Dual porosity (sphere-sum / union / overlap)',
                        'stdout': '', 'stderr': str(_e), 'rc': 1})

        # Step 3: Basic figures
        cmd = [sys.executable, os.path.join(scripts, 'generate_figures_bimodal.py'),
               results_dir, '-o', figures_dir, '-s', str(scale)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=None)
        log.append({'step': 'Basic Figures', 'stdout': result.stdout, 'stderr': result.stderr, 'rc': result.returncode})

        # Step 4: Advanced
        atoms_analyzed = os.path.join(results_dir, 'atoms_analyzed.csv')
        contacts_analyzed = os.path.join(results_dir, 'contacts_analyzed.csv')
        cmd = [sys.executable, os.path.join(scripts, 'advanced_analysis_bimodal.py'),
               atoms_analyzed, contacts_analyzed, '-o', results_dir, '-s', str(scale)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=None)
        log.append({'step': 'Advanced Analysis', 'stdout': result.stdout, 'stderr': result.stderr, 'rc': result.returncode})

        cmd = [sys.executable, os.path.join(scripts, 'generate_advanced_figures_bimodal.py'),
               results_dir, '-o', figures_dir, '-s', str(scale)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=None)
        log.append({'step': 'Advanced Figures', 'stdout': result.stdout, 'stderr': result.stderr, 'rc': result.returncode})

        # Step 5: Bimodal specific
        cmd = [sys.executable, os.path.join(scripts, 'bimodal_specific_analysis.py'),
               atoms_analyzed, contacts_analyzed, '-o', results_dir, '-s', str(scale)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=None)
        log.append({'step': 'Bimodal Specific', 'stdout': result.stdout, 'stderr': result.stderr, 'rc': result.returncode})

    else:
        # Standard mode
        cmd = [sys.executable, os.path.join(scripts, 'analyze_contacts.py'),
               atoms_csv, contacts_csv, '-o', results_dir,
               '-t', type_map, '-s', str(scale)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=None)
        log.append({'step': 'Contact Analysis', 'stdout': result.stdout, 'stderr': result.stderr, 'rc': result.returncode})

        # Dual-mode coverage + AM-SE/SE-SE totals (Hertzian vs Physics).
        # Populates *_mean_physics and area_*_total_physics keys in
        # full_metrics.json + coverage_per_am.csv (COMSOL-ready).
        cmd = [sys.executable, os.path.join(scripts, 'coverage_physics_vs_hertzian.py'), case_id]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=None)
        log.append({'step': 'Coverage Physics vs Hertzian', 'stdout': result.stdout,
                    'stderr': result.stderr, 'rc': result.returncode})

        # Network solver (ionic + electronic + thermal, both contact modes).
        # Writes sigma_full_mScm, sigma_bulk_net_mScm, electronic_*, thermal_*
        # into network_conductivity_*.json, then merges into full_metrics.json
        # so the analysis-summary tab Network Solver section auto-populates.
        cmd = [sys.executable, os.path.join(scripts, 'network_conductivity.py'),
               atoms_csv, contacts_csv, '-o', results_dir,
               '-t', type_map, '-s', str(scale),
               '--contact-mode', 'both']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=None)
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
            stage_e_cmd = [sys.executable,
                            os.path.join(scripts, 'run_network_full_corrections.py'),
                            os.path.basename(results_dir), '--quiet']
            stage_e_result = subprocess.run(stage_e_cmd, capture_output=True,
                                              text=True, timeout=None)
            log.append({'step': 'Stage E (literature-grounded grain corrections)',
                        'stdout': stage_e_result.stdout,
                        'stderr': stage_e_result.stderr,
                        'rc': stage_e_result.returncode})
        except Exception as _e:
            log.append({'step': 'Stage E (literature-grounded grain corrections)',
                        'stdout': '', 'stderr': str(_e), 'rc': 1})

        # Step 2e: Dual porosity (sphere-sum + union + overlap%) — auto-compute
        # so the UI shows ε_sphere / ε_union / overlap without a manual rerun.
        try:
            dual_cmd = [sys.executable,
                        os.path.join(scripts, 'recompute_porosity_dual.py'),
                        '--dir', results_dir]
            dual_res = subprocess.run(dual_cmd, capture_output=True, text=True, timeout=None)
            log.append({'step': 'Dual porosity (sphere-sum / union / overlap)',
                        'stdout': dual_res.stdout, 'stderr': dual_res.stderr,
                        'rc': dual_res.returncode})
        except Exception as _e:
            log.append({'step': 'Dual porosity (sphere-sum / union / overlap)',
                        'stdout': '', 'stderr': str(_e), 'rc': 1})

        cmd = [sys.executable, os.path.join(scripts, 'generate_figures.py'),
               results_dir, '-o', figures_dir, '-s', str(scale)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=None)
        log.append({'step': 'Basic Figures', 'stdout': result.stdout, 'stderr': result.stderr, 'rc': result.returncode})

        atoms_analyzed = os.path.join(results_dir, 'atoms_analyzed.csv')
        contacts_analyzed = os.path.join(results_dir, 'contacts_analyzed.csv')

        cmd = [sys.executable, os.path.join(scripts, 'advanced_analysis.py'),
               atoms_analyzed, contacts_analyzed, '-o', results_dir, '-s', str(scale)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=None)
        log.append({'step': 'Advanced Analysis', 'stdout': result.stdout, 'stderr': result.stderr, 'rc': result.returncode})

        cmd = [sys.executable, os.path.join(scripts, 'generate_advanced_figures.py'),
               results_dir, '-o', figures_dir, '-s', str(scale)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=None)
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
            [sys.executable, os.path.join(scripts, 'build_metrics_db.py')],
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
        ('Porosity union(%)', 'porosity_union'),
        ('Overlap(%)', 'overlap_fraction_pct'),
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

@app.route('/api/se_corpus.json')
def api_se_corpus():
    """Return docs/data/se_diagnostics_82.csv parsed as JSON for the viewer.

    Used by SE Diagnostics export buttons (PNG stats card) to embed
    corpus-percentile context per case.  Cached in-memory so repeated
    viewer hits don't re-parse.
    """
    csv_path = os.path.join(os.path.dirname(__file__), '..',
                             'docs', 'data', 'se_diagnostics_82.csv')
    if not os.path.exists(csv_path):
        return jsonify({'error': 'corpus CSV not found — run '
                                  'scripts/extract_se_network_diagnostics.py first.',
                        'rows': []}), 200
    # Tiny in-process cache keyed on mtime
    global _se_corpus_cache
    try:
        _se_corpus_cache
    except NameError:
        _se_corpus_cache = {'mtime': 0, 'rows': []}
    mt = os.path.getmtime(csv_path)
    if _se_corpus_cache['mtime'] != mt:
        with open(csv_path, newline='') as f:
            _se_corpus_cache = {'mtime': mt,
                                 'rows': list(csv.DictReader(f))}
    return jsonify({'rows': _se_corpus_cache['rows']})


@app.route('/api/all-grades')
def api_all_grades():
    """Batch grade re-computation for every uploaded case at a given
    carbon wt%.  Used by the index-page 🏆 랭킹 toggle so the ranking
    re-sorts itself when the user flips the What-if switch.

    Returns:
      { 'carbon_wt_pct': N,
        'cases': [ {case_id, score, grade, n_axes}, … ] }
    """
    try:
        carbon_wt = float(request.args.get('carbon_wt', 0))
    except ValueError:
        carbon_wt = 0.0
    carbon_wt = max(0.0, min(10.0, carbon_wt))

    try:
        import sys as _sys
        scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
        if scripts_dir not in _sys.path:
            _sys.path.insert(0, scripts_dir)
        from grade_engine import build_overall_grade
    except ImportError:
        return jsonify({'error': 'grade_engine import failed'}), 500

    corpus_csv = os.path.join(os.path.dirname(__file__), '..',
                              'docs', 'data', 'se_diagnostics_82.csv')
    if not os.path.exists(corpus_csv):
        corpus_csv = None

    rows = []
    upload_dir = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_dir):
        return jsonify({'carbon_wt_pct': carbon_wt, 'cases': []})

    for case_id in os.listdir(upload_dir):
        results_dir = os.path.join(app.config['RESULTS_FOLDER'], case_id)
        metrics_path = os.path.join(results_dir, 'full_metrics.json')
        if not os.path.exists(metrics_path):
            continue
        try:
            with open(metrics_path) as f:
                metrics = json.load(f)
        except (OSError, ValueError):
            continue
        # Reuse cached SE aux if present
        se_aux = None
        aux_path = os.path.join(results_dir, 'viewer_aux.json')
        if os.path.exists(aux_path):
            try:
                with open(aux_path) as af:
                    _aux = json.load(af)
                se_aux = {
                    'n_percolating':         _aux.get('se_n_percolating'),
                    'articulation_points':   _aux.get('se_articulation_points', []),
                    'n_bn_below_threshold':  _aux.get('se_n_bn_below_threshold'),
                    'n_perc_edges':          _aux.get('se_n_perc_edges'),
                }
            except (OSError, ValueError):
                pass
        try:
            r = build_overall_grade(
                _inject_input_params(metrics, results_dir),
                corpus_csv, se_aux,
                carbon_wt_pct=carbon_wt if carbon_wt > 0 else None,
                case_id=case_id)
            rows.append({
                'case_id':      case_id,
                'score':        r['composite']['score'],
                'grade':        r['composite']['grade'],
                'n_axes':       r['composite']['n_axes'],
                'is_unit_cell': r['composite'].get('is_unit_cell', False),
                'rve_area_um2': r['composite'].get('rve_area_um2'),
                'base_case':    r['composite'].get('base_case'),
            })
        except Exception:
            continue
    return jsonify({'carbon_wt_pct': carbon_wt, 'cases': rows})


@app.route('/case/<path:case_id>/grade')
def case_grade_json(case_id):
    """Return the full overall-grade structure as JSON, with optional
    `carbon_wt` query parameter (default 0 → no override).  Used by the
    What-if ON/OFF toggle in the 종합 등급 tab to re-render the table
    without a page reload."""
    try:
        carbon_wt = float(request.args.get('carbon_wt', 0))
    except ValueError:
        carbon_wt = 0.0
    carbon_wt = max(0.0, min(10.0, carbon_wt))

    # Resolve metrics + results_dir (dashboard vs archive)
    if case_id.startswith('archive:'):
        rel = case_id[len('archive:'):]
        target = _safe_path(rel)
        if not target:
            return jsonify({'error': 'archive path not allowed'}), 400
        results_dir = target
    else:
        results_dir = get_results_dir(case_id)
    metrics_path = os.path.join(results_dir, 'full_metrics.json')
    if not os.path.exists(metrics_path):
        return jsonify({'error': 'metrics not found'}), 404
    with open(metrics_path) as f:
        metrics = json.load(f)

    try:
        import sys as _sys
        scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
        if scripts_dir not in _sys.path:
            _sys.path.insert(0, scripts_dir)
        from grade_engine import build_overall_grade, GRADE_COLOR
    except ImportError:
        return jsonify({'error': 'grade_engine import failed'}), 500

    corpus_csv = os.path.join(os.path.dirname(__file__), '..',
                              'docs', 'data', 'se_diagnostics_82.csv')
    if not os.path.exists(corpus_csv):
        corpus_csv = None

    # SE diag aux (same as the build_overall_grade_table path)
    se_aux = None
    aux_path = os.path.join(results_dir, 'viewer_aux.json')
    if os.path.exists(aux_path):
        try:
            with open(aux_path) as af:
                _aux = json.load(af)
            se_aux = {
                'n_percolating':         _aux.get('se_n_percolating'),
                'articulation_points':   _aux.get('se_articulation_points', []),
                'n_bn_below_threshold':  _aux.get('se_n_bn_below_threshold'),
                'n_perc_edges':          _aux.get('se_n_perc_edges'),
            }
        except (OSError, ValueError):
            pass

    result = build_overall_grade(
        _inject_input_params(metrics, results_dir),
        corpus_csv, se_aux,
        carbon_wt_pct=carbon_wt if carbon_wt > 0 else None,
        case_id=case_id)

    # Attach the grade-colour map so the client doesn't need its own copy.
    return jsonify({
        'carbon_wt_pct': carbon_wt,
        'grade_colors':  GRADE_COLOR,
        **result,
    })


@app.route('/case/<path:case_id>/whatif-carbon')
def case_whatif_carbon(case_id):
    """Return σ_e / ASR_e estimate for a hypothetical carbon-additive
    cathode at wt% (default 1.0).  Backs the What-if panel in the
    종합 등급 tab.  Supports both dashboard cases ('<id>') and archive
    cases ('archive:<folder>')."""
    try:
        wt = float(request.args.get('wt', 1.0))
    except ValueError:
        wt = 1.0
    wt = max(0.0, min(10.0, wt))

    # Resolve metrics path (dashboard vs archive)
    if case_id.startswith('archive:'):
        rel = case_id[len('archive:'):]
        target = _safe_path(rel)
        metrics_path = os.path.join(target, 'full_metrics.json') if target else None
    else:
        metrics_path = os.path.join(get_results_dir(case_id), 'full_metrics.json')

    if not metrics_path or not os.path.exists(metrics_path):
        return jsonify({'available': False,
                        'reason': 'full_metrics.json not found'}), 200
    with open(metrics_path) as f:
        metrics = json.load(f)

    try:
        import sys as _sys
        scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
        if scripts_dir not in _sys.path:
            _sys.path.insert(0, scripts_dir)
        from grade_engine import whatif_carbon_additive
        out = whatif_carbon_additive(metrics, wt_pct=wt)
    except Exception as e:
        return jsonify({'available': False,
                        'reason': f'{type(e).__name__}: {e}'}), 200
    return jsonify(out)


def _add_recipe_str(vgcf, superp, ptfe, sdcp=0.0):
    """Serialize chosen additive wt% into an --add-recipe string for
    additives.parse_recipe (only the additive wt% are load-bearing downstream;
    AM:SE are ignored by additive_wt).  Returns '' if no additive selected."""
    parts = [(k, v) for k, v in (('VGCF', vgcf), ('SuperP', superp), ('PTFE', ptfe),
                                 ('SDCP', sdcp)) if v and v > 0]
    if not parts:
        return ''
    keys = ':'.join(k for k, _ in parts)
    vals = ':'.join(f'{v:g}' for _, v in parts)
    return f'{keys}={vals}'


@app.route('/case/<path:case_id>/whatif-additives')
def case_whatif_additives(case_id):
    """Literature-anchored with/without estimate of σ_e / σ_ion / porosity for
    VGCF / Super P / PTFE at a mixing protocol.  Backs the 첨가제 적용 section.
    Query: ?vgcf=&superp=&ptfe= (wt%, 0–10) &mixing=ballmill|thinky|handmix."""
    def _f(name):
        try:
            return max(0.0, min(10.0, float(request.args.get(name, 0.0))))
        except ValueError:
            return 0.0
    vgcf, superp, ptfe = _f('vgcf'), _f('superp'), _f('ptfe')
    mixing = request.args.get('mixing', 'ballmill')
    if mixing not in ('ballmill', 'thinky', 'handmix'):
        mixing = 'ballmill'

    if case_id.startswith('archive:'):
        target = _safe_path(case_id[len('archive:'):])
        metrics_path = os.path.join(target, 'full_metrics.json') if target else None
    else:
        metrics_path = os.path.join(get_results_dir(case_id), 'full_metrics.json')
    if not metrics_path or not os.path.exists(metrics_path):
        return jsonify({'available': False, 'reason': 'full_metrics.json not found'}), 200
    with open(metrics_path) as f:
        metrics = json.load(f)
    try:
        import sys as _sys
        scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
        if scripts_dir not in _sys.path:
            _sys.path.insert(0, scripts_dir)
        from grade_engine import whatif_additives
        out = whatif_additives(metrics, vgcf_wt=vgcf, superp_wt=superp,
                               ptfe_wt=ptfe, mixing=mixing)
    except Exception as e:
        return jsonify({'available': False, 'reason': f'{type(e).__name__}: {e}'}), 200
    out['recipe'] = _add_recipe_str(vgcf, superp, ptfe)
    return jsonify(out)


@app.route('/step5')
def step5():
    """STEP5 사이클 열화 fade(N) 인터랙티브 패널 — 총 R_int(N) 정직 분해
    (접촉 ledger 하한 + 화학 CEI[√N Park2023] + OTHER 모델밖).  ASSUMED-shape 라벨 상시 노출."""
    return render_template('step5.html')


@app.route('/api/step5/fade')
def api_step5_fade():
    """fade(N) 궤적 계산 — b1_chem_fade.trajectory_scalar (단일 소스, CLI와 동일 코어).
    Query: rint0, exp_x, n_exp, r_contact0, ledger_end_x, shape=sqrt|linear, chem_x(빈값=bare 나머지)."""
    import math as _math

    def _f(name, default, lo, hi):
        # ★리뷰 MAJOR: non-finite(inf/nan) 차단 + 상한(finite) — 아니면 jsonify가 NaN/Infinity 방출 →
        #   브라우저 JSON.parse 거부 → 패널이 잘못된 'fetch 실패'로 죽음.
        try:
            v = float(request.args.get(name, default))
        except (ValueError, TypeError):
            return default
        if not _math.isfinite(v):
            return default
        return min(hi, max(lo, v))
    rint0 = _f('rint0', 18.0, 0.1, 1e6)
    exp_x = _f('exp_x', 6.1, 1.0, 1e6)
    n_exp = int(_f('n_exp', 1000, 1, 100000))
    r_contact0 = _f('r_contact0', 2.0, 0.0, 1e6)
    ledger_end_x = _f('ledger_end_x', 1.1, 1.0, 1e4)
    chem_p = _f('chem_p', 1.5, 0.2, 6.0)
    shape = request.args.get('shape', 'sqrt')
    if shape not in ('sqrt', 'linear', 'power'):
        shape = 'sqrt'
    chem_x_raw = (request.args.get('chem_x', '') or '').strip().lower()
    chem_x = None
    if chem_x_raw not in ('', 'none', 'auto', 'bare'):
        try:
            cx = float(chem_x_raw)
            chem_x = min(1e6, max(1.0, cx)) if _math.isfinite(cx) else None
        except ValueError:
            chem_x = None
    try:
        import sys as _sys
        scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
        if scripts_dir not in _sys.path:
            _sys.path.insert(0, scripts_dir)
        import b1_chem_fade
        # #33 이종기술: 코팅 프리셋 → bare chem_x 에 CEI 억제 적용 (coating_presets, 크기=앵커·shape=ASSUMED)
        coating = (request.args.get('coating', 'none') or 'none').strip()
        coat_info = None
        if coating.lower() != 'none' and chem_x is not None:
            import coating_presets as _cp
            _p = _cp.get_preset(coating)
            _eff = _cp.coated_chem_x(coating, chem_x)
            coat_info = {'coating': coating, 'chem_x_bare': chem_x, 'chem_x_coated': round(_eff, 4),
                         'cei_suppress': _p.get('cei_suppress'), 'anchor': _p['anchor'], 'shape': _p['shape']}
            chem_x = _eff
        out = b1_chem_fade.trajectory_scalar(rint0, exp_x, n_exp, r_contact0, shape,
                                             chem_x=chem_x, ledger_end_x=ledger_end_x, chem_p=chem_p)
        if coat_info:
            out['coating_info'] = coat_info
    except Exception as e:
        return jsonify({'available': False, 'reason': f'{type(e).__name__}: {e}'}), 200
    out['available'] = True
    return jsonify(out)


# ─────────────────────────── litdb (논문 에이전트 digest) ───────────────────────────
# 2026-07-28: digest 가 세 서랍(정본 브랜치 litdb/papers · 작업 브랜치 docs/lit_* · 이 브랜치 동결
#   스냅샷)에 흩어져 "이용민 논문이 없다"는 오진을 낳았다.  litdb_sync 가 git plumbing 으로 전
#   브랜치를 체크아웃 없이 읽어 캐시+인덱스를 만들고, 여기서 그걸 서빙한다 (읽기 전용 — 정본은
#   여전히 각 브랜치의 원본; 캐시는 재생성 가능하므로 gitignore).
def _litdb_mod():
    import importlib
    import sys as _sys
    _sp = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts')
    if _sp not in _sys.path:
        _sys.path.insert(0, _sp)
    return importlib.import_module('litdb_sync')


@app.route('/litdb')
def litdb_page():
    """논문 digest 통합 검색 — 전 브랜치의 litdb 카드 + 작업노트를 한 화면에서."""
    return render_template('litdb.html')


@app.route('/api/litdb/index')
def api_litdb_index():
    """인덱스 메타 + 서랍별 통계 (본문 제외 — 가벼움)."""
    try:
        m = _litdb_mod()
        idx = m.load_index()
    except SystemExit as e:
        return jsonify({'ok': False, 'error': str(e),
                        'hint': 'python3 scripts/litdb_sync.py --sync 를 먼저 실행'}), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': f'{type(e).__name__}: {e}'}), 200
    by = {}
    for rec in idx['entries']:
        by[rec['drawer']] = by.get(rec['drawer'], 0) + 1
        for a in rec['also_in']:
            by[a['drawer']] = by.get(a['drawer'], 0) + 1
    return jsonify({'ok': True, 'n_slugs': idx['n_slugs'], 'n_files': idx['n_files'],
                    'drawers': idx['drawers'], 'by_drawer': by,
                    'context_docs': idx['context_docs'],
                    'missing_branches': idx.get('missing_branches', []),
                    'entries': [{k: r[k] for k in ('slug', 'title', 'drawer', 'branch', 'lines')}
                                | {'also_in': [a['drawer'] for a in r['also_in']]}
                                for r in idx['entries']]})


@app.route('/api/litdb/search')
def api_litdb_search():
    """전문 검색 (토큰 AND).  &q= · &limit="""
    q = (request.args.get('q', '') or '').strip()
    if not q:
        return jsonify({'ok': True, 'q': '', 'results': []})
    try:
        limit = max(1, min(int(request.args.get('limit', 20)), 100))
    except (TypeError, ValueError):
        limit = 20
    try:
        m = _litdb_mod()
        res = m.search(q, limit=limit)
    except SystemExit as e:
        return jsonify({'ok': False, 'error': str(e)}), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': f'{type(e).__name__}: {e}'}), 200
    return jsonify({'ok': True, 'q': q, 'n': len(res), 'results': res})


@app.route('/api/litdb/card/<slug>')
def api_litdb_card(slug):
    """카드 본문 (마크다운 원문).  &drawer= 로 특정 서랍 판본 선택."""
    try:
        m = _litdb_mod()
        c = m.get_card(slug, drawer=(request.args.get('drawer') or None))
    except SystemExit as e:
        return jsonify({'ok': False, 'error': str(e)}), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': f'{type(e).__name__}: {e}'}), 200
    if not c:
        return jsonify({'ok': False, 'error': f'슬러그 없음: {slug}'}), 404
    return jsonify({'ok': True, 'card': {k: v for k, v in c.items() if k != 'rank'}})


@app.route('/eis')
def eis_page():
    """v3-1 EIS/DRT 인터랙티브 패널 — 물리-기반 Randles(우리 σ·i0·D_s 유도) Nyquist + DRT.
    실험 EIS(eis_fit R0-p(R1,CPE1)-Wo1)와 같은 회로 = frame[4] 대조."""
    return render_template('eis.html')


@app.route('/api/eis')
def api_eis():
    """물리-EIS Z(ω) + DRT.  Query: sigma_e, sigma_ion, thickness_um, r_int, i0, d_s, r_p_um,
    c_dl_uf, coverage.  eis_drt_ica.physics_eis + drt (단일 소스, CLI와 동일 코어).
    ★C_dl 은 앵커(§F1) — 사용자 입력(실험 EIS CPE 또는 문헌 1-10 µF/cm²)."""
    import math as _math
    import numpy as _np

    def _f(name, default, lo, hi):
        try:
            v = float(request.args.get(name, default))
        except (TypeError, ValueError):
            return default
        if not _math.isfinite(v):
            return default
        return min(hi, max(lo, v))
    try:
        import sys as _sys
        _sd = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts')
        if _sd not in _sys.path:                              # 리뷰 LOW: 매 요청 중복 insert 방지
            _sys.path.insert(0, _sd)
        import eis_drt_ica as _eis
    except Exception as e:
        return jsonify({'error': f'eis_drt_ica import 실패: {type(e).__name__}: {e}'}), 200
    kw = dict(sigma_e_S_cm=_f('sigma_e', 2.0, 1e-6, 1e3), sigma_ion_S_cm=_f('sigma_ion', 2e-4, 1e-9, 1e2),
              thickness_um=_f('thickness_um', 72.0, 1.0, 1000.0), r_int_ohm_cm2=_f('r_int', 50.0, 0.0, 1e4),
              i0_A_m2=_f('i0', 2.0, 1e-3, 1e3), d_s_m2_s=_f('d_s', 3e-14, 1e-18, 1e-10),
              r_p_um=_f('r_p_um', 3.0, 0.1, 50.0), c_dl_uF_cm2=_f('c_dl_uf', 10.0, 0.01, 1000.0),
              coverage_frac=_f('coverage', 0.5, 0.01, 1.0), porosity=_f('porosity', 8.0, 0.1, 60.0))
    # ── 케이스 자동로드 (&case=): STEP3 미세구조(σ-triad·두께·porosity)만 로드.  R_int(실험앵커)·
    #    i0/D_s(스윕)·C_dl(앵커)은 UI 유지 — 케이스의 R_geom 은 µΩ급 기하값이라 실험 R_int 아님. ──
    case_loaded = None
    _case = (request.args.get('case') or '').strip()
    if _case:
        def _apply(_p):                                       # STEP3 σ-triad·두께·porosity 만 override
            # 리뷰 LOW: is not None (σ=0 비퍼콜 케이스도 로드; 클램프 floor 가 처리) — truthiness 스킵 안 함
            if _p.get('sigma_e_S_cm') is not None:
                kw['sigma_e_S_cm'] = min(1e3, max(1e-6, float(_p['sigma_e_S_cm'])))
            if _p.get('sigma_ion_S_cm') is not None:
                kw['sigma_ion_S_cm'] = min(1e2, max(1e-9, float(_p['sigma_ion_S_cm'])))
            if _p.get('thickness_um') is not None:
                kw['thickness_um'] = min(1000.0, max(1.0, float(_p['thickness_um'])))
            if _p.get('porosity') is not None:
                kw['porosity'] = min(60.0, max(0.1, float(_p['porosity'])))
        try:                                                  # 1) DEM 케이스 (results/<case>/*metrics.json)
            _rd = _contained_join(app.config['RESULTS_FOLDER'], _case)   # 리뷰 LOW: makedirs 안 함(GET 부작용 방지)
            for _mf in ('mpm_metrics.json', 'full_metrics.json'):
                _mp = os.path.join(_rd, _mf)
                if os.path.exists(_mp):
                    _apply(_eis._load_step3_params(_mp)); case_loaded = _case; break
        except Exception:
            pass
        if not case_loaded:                                   # 2) mpm_lab 저장 payload (mpm_lab/<pid>/meta.json → mpm_metrics)
            try:
                import json as _json
                _mj = os.path.join(_contained_join(app.config['MPM_LAB_FOLDER'], _case), 'meta.json')
                if os.path.exists(_mj):
                    _mm = (_json.loads(open(_mj).read()).get('mpm_metrics')) or {}
                    if _mm:
                        _apply(_eis._step3_params_from_metrics(_mm)); case_loaded = _case
            except Exception:
                pass
    # ── 실험앵커 (&expanchor=1): eis_fit CPE→Brug C_dl + Wo1_R → physics_eis 앵커 (frame[4]) ──
    exp_anchor = None
    if (request.args.get('expanchor') or '').strip() in ('1', 'true', 'yes', 'on'):
        try:
            exp_anchor = _eis.load_experimental_anchors()
        except Exception:
            exp_anchor = None
        if exp_anchor:
            kw['c_dl_areal_uF_cm2'] = exp_anchor['c_dl_areal_uF_cm2']
            if exp_anchor.get('r_w_ohm_cm2') is not None:
                kw['r_w_ohm_cm2'] = exp_anchor['r_w_ohm_cm2']
    try:
        freqs = _eis.lab_freq_grid()   # 랩 EC-Lab PEIS: 7 MHz→10 mHz, 10 pts/dec (full/sym .mps 정합)
        Z, el = _eis.physics_eis(freqs, **kw)
        tau, g, R0f, Zr = _eis.drt(freqs, Z)
        peaks = _eis.drt_peaks(tau, g)
    except Exception as e:
        return jsonify({'error': f'EIS 계산 실패: {type(e).__name__}: {e}'}), 200
    # jsonify NaN/Inf 방출 방지 — finite 만
    def _cl(x):
        return float(x) if _math.isfinite(float(x)) else None
    try:                                                      # 리뷰 LOW: 직렬화 예외도 500 대신 JSON error
        return jsonify({
            'nyquist': [{'f': _cl(fr), 'zre': _cl(z.real), 'zim': _cl(-z.imag)} for fr, z in zip(freqs, Z)],
            'drt': [{'tau': _cl(t), 'gamma': _cl(gg)} for t, gg in zip(tau, g)],
            'elements': {k: _cl(v) for k, v in el.items() if isinstance(v, (int, float))},
            'peaks': [{'f_Hz': _cl(p['f_Hz']), 'tau_s': _cl(p['tau_s']), 'R': _cl(p['R_ohm_cm2']),
                       **_eis.assign_drt_peak(p['tau_s'], el)} for p in peaks],
            'bands': _eis.drt_band_map(el),   # τ-대역 물리지도 (hover-anywhere, 전고체 복합양극)
            'provenance': el.get('provenance', {}),
            'params': {k: kw[k] for k in kw},
            'case_loaded': case_loaded,
            'exp_anchor': exp_anchor,
        })
    except Exception as e:
        return jsonify({'error': f'직렬화 실패: {type(e).__name__}: {e}'}), 200


@app.route('/api/ica', methods=['POST'])
def api_ica():
    """ICA(dQ/dV): 방전(또는 충전) 곡선 V,Q → dQ/dV(V) + OCP 상전이 피크.  eis_drt_ica.ica_dqdv.
    POST JSON {v:[...], q:[...]} 또는 {csv:'V,Q\\n…'}.  기존 STEP4 방전곡선 후처리 = 공짜."""
    import math as _math
    try:
        import sys as _sys
        _sd = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts')
        if _sd not in _sys.path:
            _sys.path.insert(0, _sd)
        import eis_drt_ica as _eis
        import numpy as _np
    except Exception as e:
        return jsonify({'error': f'import 실패: {type(e).__name__}: {e}'}), 200
    body = request.get_json(silent=True) or {}
    _cs = body.get('csv')
    if isinstance(_cs, str) and len(_cs) > 5_000_000:         # 리뷰 MED: body cap (~5MB≈25만행) — 방전곡선은 수천점
        return jsonify({'error': f'CSV 너무 큼 ({len(_cs) // 1000}KB > 5MB)'}), 200
    v, q = body.get('v'), body.get('q')
    if isinstance(v, list) and len(v) > 500_000:
        return jsonify({'error': f'점 과다 ({len(v)} > 50만) — 방전곡선은 수천 점'}), 200
    if (not v or not q) and _cs:                              # CSV 텍스트 폴백 (헤더/구분자 관대)
        vv, qq = [], []
        for line in str(_cs).strip().splitlines():
            parts = [p for p in line.replace(',', ' ').replace('\t', ' ').split() if p]
            try:                                              # ★리뷰 MED: 양쪽 파싱 성공 후 append (desync 방지)
                a = float(parts[0]); b = float(parts[1])
            except (ValueError, IndexError):
                continue                                      # 헤더/빈줄/결측셀 스킵 (행 통째로)
            vv.append(a); qq.append(b)
        v, q = vv, qq
    try:
        v = _np.asarray(v, float); q = _np.asarray(q, float)
        m = _np.isfinite(v) & _np.isfinite(q)
        if int(m.sum()) < 4:
            return jsonify({'error': f'유효 (V,Q) 점 부족(<4): {int(m.sum())}'}), 200
        vg, dq, peaks = _eis.ica_dqdv(v[m], q[m])
    except Exception as e:
        return jsonify({'error': f'ICA 계산 실패: {type(e).__name__}: {e}'}), 200

    def _cl(x):
        return float(x) if _math.isfinite(float(x)) else None
    try:
        return jsonify({
            'ica': [{'v': _cl(a), 'dqdv': _cl(b)} for a, b in zip(vg, dq)],
            'peaks': [{'v': _cl(p['V']), 'dqdv': _cl(p['dQdV'])} for p in peaks],
            'n_in': int(m.sum()),
        })
    except Exception as e:
        return jsonify({'error': f'직렬화 실패: {type(e).__name__}: {e}'}), 200


@app.route('/api/ica_case')
def api_ica_case():
    """케이스의 저장된 STEP4 방전곡선(st4_viz.json)에서 V_terminal·용량을 뽑아 dQ/dV 자동 산출 —
    붙여넣기 없이 &case=<pid> 로 ICA.  V = V_terminal(측정 전압) 우선.  용량 = |Δx_mean|/|x100−x0|×100
    (정규화 %, §F1: 면적/질량 앵커가 viz 에 없어 절대 mAh/cm² 못 만듦 → 정규화 진행률만 = 정직)."""
    import math as _math
    import glob as _glob
    _case = (request.args.get('case') or '').strip()
    if not _case:
        return jsonify({'available': False, 'error': 'case 파라미터 없음'}), 200
    # st4_viz.json 위치: mpm_lab/<pid>/(뷰어 st4 자동저장) 우선 → results/<case>/ → step4_viz*.json glob
    _paths = []
    for _base_key in ('MPM_LAB_FOLDER', 'RESULTS_FOLDER'):
        _base = app.config.get(_base_key)
        if not _base:
            continue
        try:
            _d = _contained_join(_base, _case)                # 경로탈출 거부 (GET 부작용 없음: makedirs 안 함)
        except Exception:
            continue
        _paths.append(os.path.join(_d, 'st4_viz.json'))
        try:
            _paths += sorted(_glob.glob(os.path.join(_d, 'step4_viz*.json')))
        except Exception:
            pass
    _viz = None
    for _p in _paths:
        if os.path.isfile(_p):
            try:
                _cand = json.loads(open(_p).read())
            except Exception:
                continue
            if isinstance(_cand, dict) and _cand.get('kind') == 'step4_viz':
                _viz = _cand
                break
    if not _viz:
        return jsonify({'available': False,
                        'hint': '이 케이스엔 저장된 STEP4 방전곡선이 없음 — 뷰어 STEP4-v2 모드에서 📂로 '
                                '한 번 열면 자동 저장됨 (또는 아래에 V,Q 직접 붙여넣기)'}), 200
    cu = _viz.get('curve') or {}
    Vt = cu.get('V_terminal') or cu.get('V') or []
    xm = cu.get('x_mean') or []
    if not Vt or not xm or len(Vt) != len(xm) or len(Vt) < 4:
        return jsonify({'available': False,
                        'hint': f'방전곡선 점 부족({len(Vt)}) — 최신 step4_dyn(--viz-out)로 재생성 필요'}), 200
    try:
        import sys as _sys
        _sd = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts')
        if _sd not in _sys.path:
            _sys.path.insert(0, _sd)
        import eis_drt_ica as _eis
        import numpy as _np
    except Exception as e:
        return jsonify({'available': False, 'error': f'import 실패: {type(e).__name__}: {e}'}), 200
    v = _np.asarray(Vt, float); x = _np.asarray(xm, float)
    m = _np.isfinite(v) & _np.isfinite(x)
    v, x = v[m], x[m]
    if len(v) < 4:
        return jsonify({'available': False, 'error': f'유효 (V,x) 점 부족(<4): {len(v)}'}), 200
    x0, x100 = _viz.get('x0'), _viz.get('x100')                # 용량 진행률 정규화 창
    _win = (abs(float(x100) - float(x0)) if (x0 is not None and x100 is not None) else 0.0)
    if not (_win and _math.isfinite(_win) and _win > 1e-6):
        _win = max(abs(float(x.max() - x.min())), 1e-6)        # 폴백: 관측 x 스팬
    q = _np.abs(x - x[0]) / _win * 100.0                       # 전달 용량 % (0→진행)
    try:
        vg, dq, peaks = _eis.ica_dqdv(v, q)
    except Exception as e:
        return jsonify({'available': False, 'error': f'ICA 계산 실패: {type(e).__name__}: {e}'}), 200

    def _cl(z):
        return float(z) if _math.isfinite(float(z)) else None
    try:
        return jsonify({
            'available': True, 'case': _case, 'q_unit': '용량 % (정규화)',
            'v': [_cl(a) for a in v], 'q': [round(float(b), 3) for b in q],
            'ica': [{'v': _cl(a), 'dqdv': _cl(b)} for a, b in zip(vg, dq)],
            'peaks': [{'v': _cl(p['V']), 'dqdv': _cl(p['dQdV'])} for p in peaks],
            'n_in': int(len(v)),
            'meta': {'c_rate': _viz.get('c_rate'), 'charge': bool(_viz.get('charge')),
                     'end_reason': _viz.get('end_reason'),
                     'v_span': [round(float(v.min()), 3), round(float(v.max()), 3)]},
        })
    except Exception as e:
        return jsonify({'available': False, 'error': f'직렬화 실패: {type(e).__name__}: {e}'}), 200


@app.route('/api/eis_cycle')
def api_eis_cycle():
    """사이클-N EIS/DRT 궤적 (열화 기전 진단, D5).  base σ-triad + R_int 끝점(r0→rc@ntot) → 각 N 의
    Nyquist+DRT (성장 ΔR 을 R_ct/R0/R_w 분배, ASSUMED §F1).  eis_drt_ica.cycle_eis_trajectory 단일소스."""
    import math as _math

    def _f(name, default, lo, hi):
        try:
            v = float(request.args.get(name, default))
        except (TypeError, ValueError):
            return default
        return default if not _math.isfinite(v) else min(hi, max(lo, v))
    try:
        import sys as _sys
        _sd = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts')
        if _sd not in _sys.path:
            _sys.path.insert(0, _sd)
        import eis_drt_ica as _eis
        import numpy as _np
    except Exception as e:
        return jsonify({'error': f'eis_drt_ica import 실패: {type(e).__name__}: {e}'}), 200
    kw = dict(sigma_e_S_cm=_f('sigma_e', 2.0, 1e-6, 1e3), sigma_ion_S_cm=_f('sigma_ion', 2e-4, 1e-9, 1e2),
              thickness_um=_f('thickness_um', 72.0, 1.0, 1000.0), r_int_ohm_cm2=_f('r_int', 50.0, 0.0, 1e4),
              i0_A_m2=_f('i0', 2.0, 1e-3, 1e3), d_s_m2_s=_f('d_s', 3e-14, 1e-18, 1e-10),
              r_p_um=_f('r_p_um', 3.0, 0.1, 50.0), c_dl_uF_cm2=_f('c_dl_uf', 10.0, 0.01, 1000.0),
              coverage_frac=_f('coverage', 0.5, 0.01, 1.0), porosity=_f('porosity', 8.0, 0.1, 60.0))
    if (request.args.get('expanchor') or '').strip() in ('1', 'true', 'yes', 'on'):
        try:
            _anc = _eis.load_experimental_anchors()
        except Exception:
            _anc = None
        if _anc:
            kw['c_dl_areal_uF_cm2'] = _anc['c_dl_areal_uF_cm2']
            if _anc.get('r_w_ohm_cm2') is not None:
                kw['r_w_ohm_cm2'] = _anc['r_w_ohm_cm2']
    r0c, rcc = _f('cycle_r0', 50.0, 1e-3, 1e4), _f('cycle_rc', 125.0, 1e-3, 1e4)
    ntot = int(_f('cycle_ntot', 1000, 1, 1e6))
    shape = 'linear' if (request.args.get('cycle_shape') == 'linear') else 'sqrt'
    jump = _f('cycle_jump', 0.5, 0.0, 1.0)
    try:
        ns = [int(float(x)) for x in (request.args.get('cycle_ns') or '0,100,300,500,1000').split(',') if x.strip()][:24]
        sh = [float(x) for x in (request.args.get('cycle_shares') or '0.7,0.2,0.1').split(',')][:3]
        while len(sh) < 3:
            sh.append(0.0)
    except Exception:
        ns, sh = [0, 100, 300, 500, 1000], [0.7, 0.2, 0.1]
    if not ns:
        ns = [0, ntot]
    try:
        freqs = _eis.lab_freq_grid()   # 랩 EC-Lab PEIS 주파수축 (frame[4] 정합)
        _Z, el = _eis.physics_eis(freqs, **kw)
        mult = _eis.rint_growth_mult(ns, r0c, rcc, ntot, shape, jump)
        traj = _eis.cycle_eis_trajectory(freqs, el, ns, mult, rct_share=sh[0], r0_share=sh[1], rw_share=sh[2])
    except Exception as e:
        return jsonify({'error': f'궤적 계산 실패: {type(e).__name__}: {e}'}), 200

    def _cl(x):
        return float(x) if _math.isfinite(float(x)) else None
    try:
        series = [{
            'N': t['N'], 'mult': round(t['mult'], 3),
            'R0': round(t['R0_ohm_cm2'], 2), 'R_ct': round(t['R_ct_ohm_cm2'], 2),
            'R_int': round(t.get('R_int_ohm_cm2', 0.0), 2),
            'R_w': round(t['R_w_ohm_cm2'], 2), 'R_dc': round(t['R_dc_ohm_cm2'], 2), 'f_ct_Hz': _cl(t['f_ct_Hz']),
            'nyquist': [{'zre': _cl(z.real), 'zim': _cl(-z.imag)} for z in t['Z']],
            'drt': [{'tau': _cl(tt), 'gamma': _cl(gg)} for tt, gg in zip(t['tau'], t['gamma'])],
            'peaks': [{'f_Hz': _cl(p['f_Hz']), 'R': _cl(p['R_ohm_cm2'])} for p in t['peaks']],
        } for t in traj]
        return jsonify({'series': series, 'shares': {'R_ct': sh[0], 'R0': sh[1], 'R_w': sh[2]},
                        'cycle': {'r0': r0c, 'rc': rcc, 'ntot': ntot, 'shape': shape, 'jump': jump},
                        'note': 'ΔR_int(N) 분배(R_ct/R0/R_w)=ASSUMED §F1; R_int 끝점=측정, 사이=assumed-form'})
    except Exception as e:
        return jsonify({'error': f'직렬화 실패: {type(e).__name__}: {e}'}), 200


@app.route('/api/eis_fig')
def api_eis_fig():
    """발표/논문용 EIS 그림 다운로드 (matplotlib png/svg, 흰 배경 ASCII 라벨).  kind=eis(Nyquist+DRT) |
    cycle(사이클 오버레이 + R(N) 성장).  /api/eis 와 동일 σ 파라미터 + kind·fmt·cycle_*.
    eis_drt_ica.save_eis_figures 단일소스 (CLI --fig 와 동일 코어) = 랩 규약 svg/png/csv 동시."""
    import math as _math
    import shutil as _sh
    import tempfile as _tf

    def _f(name, default, lo, hi):
        try:
            v = float(request.args.get(name, default))
        except (TypeError, ValueError):
            return default
        return default if not _math.isfinite(v) else min(hi, max(lo, v))
    try:
        import sys as _sys
        _sd = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts')
        if _sd not in _sys.path:
            _sys.path.insert(0, _sd)
        import eis_drt_ica as _eis
        import numpy as _np
    except Exception as e:
        return jsonify({'error': f'eis_drt_ica import 실패: {type(e).__name__}: {e}'}), 200
    kw = dict(sigma_e_S_cm=_f('sigma_e', 2.0, 1e-6, 1e3), sigma_ion_S_cm=_f('sigma_ion', 2e-4, 1e-9, 1e2),
              thickness_um=_f('thickness_um', 72.0, 1.0, 1000.0), r_int_ohm_cm2=_f('r_int', 50.0, 0.0, 1e4),
              i0_A_m2=_f('i0', 2.0, 1e-3, 1e3), d_s_m2_s=_f('d_s', 3e-14, 1e-18, 1e-10),
              r_p_um=_f('r_p_um', 3.0, 0.1, 50.0), c_dl_uF_cm2=_f('c_dl_uf', 10.0, 0.01, 1000.0),
              coverage_frac=_f('coverage', 0.5, 0.01, 1.0), porosity=_f('porosity', 8.0, 0.1, 60.0))
    if (request.args.get('expanchor') or '').strip() in ('1', 'true', 'yes', 'on'):
        try:
            _anc = _eis.load_experimental_anchors()
        except Exception:
            _anc = None
        if _anc:
            kw['c_dl_areal_uF_cm2'] = _anc['c_dl_areal_uF_cm2']
            if _anc.get('r_w_ohm_cm2') is not None:
                kw['r_w_ohm_cm2'] = _anc['r_w_ohm_cm2']
    kind = 'cycle' if request.args.get('kind') == 'cycle' else 'eis'
    fmt = 'svg' if request.args.get('fmt') == 'svg' else 'png'
    tmp = _tf.mkdtemp()
    try:
        freqs = _eis.lab_freq_grid()   # 랩 EC-Lab PEIS 주파수축 (frame[4] 정합)
        Z, el = _eis.physics_eis(freqs, **kw)
        tau, g, _r0, _zr = _eis.drt(freqs, Z)
        traj = None
        if kind == 'cycle':
            r0c, rcc = _f('cycle_r0', 50.0, 1e-3, 1e4), _f('cycle_rc', 125.0, 1e-3, 1e4)
            ntot = int(_f('cycle_ntot', 1000, 1, 1e6))
            shape = 'linear' if request.args.get('cycle_shape') == 'linear' else 'sqrt'
            jump = _f('cycle_jump', 0.5, 0.0, 1.0)
            ns = [int(float(x)) for x in (request.args.get('cycle_ns') or '0,100,300,500,1000').split(',')
                  if x.strip()][:24] or [0, ntot]
            sh = [float(x) for x in (request.args.get('cycle_shares') or '0.7,0.2,0.1').split(',')][:3]
            while len(sh) < 3:
                sh.append(0.0)
            mult = _eis.rint_growth_mult(ns, r0c, rcc, ntot, shape, jump)
            traj = _eis.cycle_eis_trajectory(freqs, el, ns, mult, rct_share=sh[0], r0_share=sh[1], rw_share=sh[2])
        prefix = os.path.join(tmp, 'eis')
        _eis.save_eis_figures(prefix, freqs, Z, el, tau, g, _eis.drt_peaks(tau, g), traj=traj, fmt=(fmt,))
        path = f'{prefix}_{kind}.{fmt}'
        if not os.path.isfile(path):
            return jsonify({'error': f'그림 생성 실패 ({kind}.{fmt})'}), 200
        with open(path, 'rb') as fh:
            data = fh.read()
    except Exception as e:
        return jsonify({'error': f'그림 생성 실패: {type(e).__name__}: {e}'}), 200
    finally:
        _sh.rmtree(tmp, ignore_errors=True)
    return app.response_class(data, mimetype=('image/svg+xml' if fmt == 'svg' else 'image/png'),
                              headers={'Content-Disposition': f'attachment; filename="eis_{kind}.{fmt}"'})


@app.route('/api/eis_exp')
def api_eis_exp():
    """실험 EIS Nyquist (이종기술/eis/extracted) → Ω·cm² 정규화 = physics-EIS 위 오버레이(frame[4]).
    ★files=<stem1,stem2,…> 지정 시 그 측정만(표 체크박스 선택), 없으면 cell=full|sym 전체.
    Z(Ω)×area = ASR(eis_fit 규약; area 는 파일명 sym/full 로 파일별 결정).  데이터 부재 시 available:false."""
    import csv as _csv
    import glob as _glob
    import math as _math
    cell = 'sym' if request.args.get('cell') == 'sym' else 'full'
    _files = set(x.strip() for x in (request.args.get('files') or '').split(',') if x.strip())
    _want_drt = (request.args.get('drt') or '1') not in ('0', 'false', 'no')   # 실험 DRT 계산(기본 on)
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    exdir = os.path.join(root, '이종기술', 'eis', 'extracted')
    if not os.path.isdir(exdir):
        return jsonify({'available': False, 'hint': '실험 EIS 추출본 없음 (이종기술/eis/extracted) — 랩 데이터'}), 200
    try:
        import sys as _sys
        _sd = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts')
        if _sd not in _sys.path:
            _sys.path.insert(0, _sd)
        import eis_drt_ica as _eis
        import numpy as _np
    except Exception:
        _eis, _np, _want_drt = None, None, False
    curves = []
    for p in sorted(_glob.glob(os.path.join(exdir, '*.csv'))):
        name = os.path.basename(p)[:-4]
        if _files:                                            # 선택 측정만 (셀타입 무관, 파일별 area)
            if name not in _files:
                continue
        elif ('sym' in name) != (cell == 'sym'):              # 선택 없으면 full/sym 전체
            continue
        area = 0.7854 if ('sym' in name) else 1.3273          # 파일별 AREA (10π sym / 13π full)
        fs, zr_l, zi_l = [], [], []
        try:
            for row in _csv.DictReader(open(p)):
                try:
                    fv = float(row['freq_Hz']); zr = float(row['ReZ_ohm']) * area; zi = float(row['negImZ_ohm']) * area
                except (KeyError, ValueError, TypeError):
                    continue
                if all(_math.isfinite(v) for v in (fv, zr, zi)) and fv > 0 and abs(zr) < 1e6 and abs(zi) < 1e6:
                    fs.append(fv); zr_l.append(zr); zi_l.append(zi)
        except Exception:
            continue
        if len(fs) < 4:
            continue
        pts = [{'zre': round(a, 3), 'zim': round(b, 3)} for a, b in zip(zr_l, zi_l)]
        if len(pts) > 80:
            pts = pts[::(len(pts) // 80 + 1)]
        cobj = {'name': name, 'pts': pts}
        if _want_drt and _eis is not None:                    # 실험 DRT (분포 = 눌린 Nyquist 보다 프로세스 명확)
            try:
                # DRT 안정화: 선두 인덕턴스(zim<0=Im(Z)>0) crop → 첫 용량성부터.  Z=Re+jIm, Im=-zim.
                _fa, _Za = _np.asarray(fs, float), _np.asarray(zr_l, float) - 1j * _np.asarray(zi_l, float)
                _cap = _np.asarray(zi_l, float) > 0
                if _cap.any():
                    _k0 = int(_np.argmax(_cap))
                    _fa, _Za = _fa[_k0:], _Za[_k0:]
                if len(_fa) >= 6:
                    _tau, _g, _r0, _zr = _eis.drt(_fa, _Za, n_tau=60, lam=1e-2)
                    _dpts = list(zip(_tau, _g))
                    if len(_dpts) > 70:
                        _dpts = _dpts[::(len(_dpts) // 70 + 1)]
                    cobj['drt'] = [{'tau': float(t), 'gamma': (float(gg) if _math.isfinite(float(gg)) else 0.0)}
                                   for t, gg in _dpts]
            except Exception:
                pass
        curves.append(cobj)
    if not curves:
        return jsonify({'available': False, 'hint': ('선택 측정 추출본 없음' if _files else f'{cell} 셀 추출본 없음')}), 200
    return jsonify({'available': True, 'cell': cell, 'selected': bool(_files), 'curves': curves,
                    'note': 'Z(Ω)×area→Ω·cm²(ASR, eis_fit 규약); 방울=실측 Nyquist, physics-EIS 선과 겹치면 frame[4] '
                            '(반쪽셀 모델 vs primer-SUS 풀셀 = 배치 다름, 자릿수-대조)'})


def _eis_archive_paths():
    """이종기술/eis 아카이브 경로 (raw/extracted/catalog/fits).

    ★ WEBAPP_EIS_FOLDER 로 override 가능 (2026-08-03).  이 경로는 다른 폴더들과 달리
      env 를 안 봐서 **리포 안 실제 측정 아카이브로 고정**돼 있었다 — 그 결과 이 라우트를
      부르는 테스트가 WEBAPP_* 를 tmp 로 다 돌려놔도 **진짜 fits CSV·두께 override 를
      덮어썼다** (실제로 발생: eis_fit_results.csv 12행 → 테스트 1행으로 소실.
      extracted/*.csv 는 git tracked 라 무손상이었고 eis_fit.py 재실행으로 전량 복구).
      derived 산출물은 재생성되지만 테스트가 실데이터를 만지는 구조 자체가 결함이다.
    """
    _root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    a = os.environ.get('WEBAPP_EIS_FOLDER') or os.path.join(_root, '이종기술', 'eis')
    return {'root': _root, 'archive': a, 'raw': os.path.join(a, 'raw'),
            'extracted': os.path.join(a, 'extracted'), 'catalog': os.path.join(a, 'eis_catalog.csv'),
            'fits': os.path.join(a, 'fits', 'eis_fit_results.csv')}


def _eis_exp_table():
    """실험 EIS 측정 목록 = eis_catalog.csv(메타) ⋈ eis_fit_results.csv(도출값) by filename.
    반환 {rows:[...], n, fitted, summary}.  파일 없으면 빈 리스트 (graceful)."""
    import csv as _csv
    import json as _json
    P = _eis_archive_paths()
    try:                                                  # 사용자가 L 을 명시 지정한 stem 집합
        _ovr = set(_json.load(open(os.path.join(P['archive'], 'thickness_overrides.json'))))
    except Exception:
        _ovr = set()
    cat = {}
    if os.path.isfile(P['catalog']):
        try:
            for r in _csv.DictReader(open(P['catalog'])):
                cat[r.get('filename', '')] = r
        except Exception:
            pass
    fit = {}
    if os.path.isfile(P['fits']):
        try:
            for r in _csv.DictReader(open(P['fits'])):
                fit[r.get('filename', '')] = r
        except Exception:
            pass

    def _num(d, k):
        try:
            v = d.get(k, '')
            return round(float(v), 4) if v not in ('', None) else None
        except (TypeError, ValueError):
            return None
    rows = []
    for fn in sorted(set(cat) | set(fit)):
        c, f = cat.get(fn, {}), fit.get(fn, {})
        rows.append({
            'filename': fn, 'date': c.get('date', ''), 'cell_type': c.get('cell_type', '') or f.get('cell_type', ''),
            'blend': c.get('blend', ''), 'state': c.get('state', ''), 'Ewe_V': _num(c, 'Ewe_V'),
            'n_points': _num(c, 'n_points'), 'f_max_Hz': _num(c, 'f_max_Hz'), 'f_min_Hz': _num(c, 'f_min_Hz'),
            # 파일명이 알려주는 두께(예 '70um') — ⚠집전체(SUS/c-SUS ~15-20µm) 포함 총두께라 σ_e 에
            # 그대로 쓰면 안 됨(eis_fit.py:32-36).  σ_e 용 L 은 합제만(기본 45).  표에 병기해 오입력 방지.
            'filename_thickness_um': _num(c, 'thickness_um'),
            # L 이 사용자 지정인지(override JSON 에 키 존재) — ⚠경고는 '지정했을 때만' 띄워야 한다.
            # 기본 45 와 파일명 45um 이 우연히 같아도 경고가 뜨던 오탐 차단 (감사 L1).
            'L_is_user_set': fn in _ovr,
            'R_s_ohmcm2': _num(f, 'R_s_ohmcm2'), 'R_int_ohmcm2': _num(f, 'R1_ohmcm2'),
            'R_w_ohmcm2': _num(f, 'R_w_ohmcm2'), 'C_dl_uF_cm2': _num(f, 'C_dl_uF_cm2'),
            'sigma_e_mScm': _num(f, 'sigma_e_mScm'), 'L_composite_um': _num(f, 'L_composite_um'),
            'rmse_pct': _num(f, 'rmse_pct'),
            'circuit': f.get('circuit', ''), 'fitted': bool(f.get('R1_ohm')),
            'area_cm2': _num(c, 'area_cm2') or _num(f, 'area_cm2'), 'note': c.get('note', '') or f.get('note', ''),
        })
    fitted = sum(1 for r in rows if r['fitted'])
    # 대표값 (frame[4] 앵커) — load_experimental_anchors 와 동일 소스
    summ = None
    try:
        import sys as _sys
        _sd = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts')
        if _sd not in _sys.path:
            _sys.path.insert(0, _sd)
        import eis_drt_ica as _eis
        summ = _eis.load_experimental_anchors()
    except Exception:
        summ = None
    return {'rows': rows, 'n': len(rows), 'fitted': fitted, 'anchor': summ}


@app.route('/api/eis_exp_list')
def api_eis_exp_list():
    """이미 먹인 + 업로드된 실험 EIS 측정 목록(표) + 도출값 + frame[4] 대표앵커."""
    try:
        return jsonify(_eis_exp_table())
    except Exception as e:
        return jsonify({'error': f'목록 실패: {type(e).__name__}: {e}', 'rows': []}), 200


@app.route('/api/eis_exp_thickness', methods=['POST'])
def api_eis_exp_thickness():
    """대칭셀 σ_e 두께 설정 (site 두께 입력) → thickness_overrides.json 저장 + σ_e 즉시 재계산
    (σ_e = L/R1, R1 은 이미 fit된 값 재사용 → CNLS 재fit 불필요, 즉답).  기본 45µm."""
    import csv as _csv
    import json as _json
    P = _eis_archive_paths()
    body = request.get_json(silent=True) or {}
    fn = (body.get('filename') or '').strip()
    if not fn:
        return jsonify({'error': 'filename 없음'}), 200
    try:
        thick = float(body.get('thickness_um'))
    except (TypeError, ValueError):
        return jsonify({'error': '두께 숫자 아님'}), 200
    if not (0.5 <= thick <= 300):
        return jsonify({'error': f'두께 범위 벗어남 ({thick} — 0.5~300µm)'}), 200
    # ★대상 검증 (2026-07-27 감사 M3/M4): 예전엔 존재하지 않는 filename 도, σ_e 에 두께를 안 쓰는
    #   full-cell 도 무조건 ok:true 를 돌려줘 UI 가 "✓ σ_e 재계산됨" 초록 메시지를 띄웠다 —
    #   실제론 아무것도 안 바뀌고 override JSON 만 오염.  존재·셀타입을 먼저 확인한다.
    _rows = {r['filename']: r for r in (_eis_exp_table().get('rows') or [])}
    _row = _rows.get(fn)
    if _row is None:
        return jsonify({'error': f'그런 측정 없음: {fn}'}), 200
    # ★ 2026-08-03 정정: 예전엔 full 셀을 **거부**했다.  σ_e=L/R1 이 대칭셀 전용인 것은 맞지만,
    #   "full 셀은 두께가 필요없다" 는 과한 진술이었다 — full 셀의 R_s(HF 절편)에는 이온 TL 저항
    #   ∝ L/σ_ion 이 들어있고, R_int(Ω·cm²geo) 도 1/(a_spec·L) 로 스케일한다.  즉 **두께가 다른
    #   full 셀끼리 R_int 를 비교하려면 L 이 필요**하고, physics-EIS 대조도 같은 L 에서만 의미가 있다.
    #   ⇒ 거부하지 말고 **기록**한다.  단 σ_e 는 계산하지 않고 '—' 로 둔다 (정의되지 않으므로).
    _is_sym = (_row.get('cell_type') or '') == 'symmetric'
    ov_path = os.path.join(P['archive'], 'thickness_overrides.json')
    try:                                                      # override JSON 갱신
        ov = _json.load(open(ov_path)) if os.path.isfile(ov_path) else {}
    except Exception:
        ov = {}
    ov[fn] = round(thick, 2)
    try:
        with open(ov_path, 'w') as fh:
            _json.dump(ov, fh, ensure_ascii=False, indent=1)
    except Exception as e:
        return jsonify({'error': f'override 저장 실패: {e}'}), 200
    # fits CSV 의 해당 대칭셀 행 σ_e 즉시 재계산 (R1 재사용)
    fits = P['fits']
    if os.path.isfile(fits):
        try:
            with open(fits, newline='') as fh:
                rd = _csv.DictReader(fh); cols = rd.fieldnames; rows = list(rd)
            for r in rows:
                if r.get('filename') == fn and not _is_sym:
                    r['L_composite_um'] = round(thick, 2)     # 메타데이터 (σ_e 엔 안 씀)
                    r['note'] = ((r.get('note') or '') + f'  · L={thick:g}µm 기록(σ_e 미사용 — '
                                 f'full 셀 R1=R_int 는 계면 ASR)').strip()
                if r.get('filename') == fn and _is_sym:
                    try:
                        r1 = float(r.get('R1_ohmcm2', ''))
                        if r1 > 0:
                            r['L_composite_um'] = round(thick, 2)
                            r['sigma_e_mScm'] = round(thick * 1e-4 / r1 * 1e3, 4)
                            _lo = round(max(thick - 2, 0.1) * 1e-4 / r1 * 1e3, 4)
                            _hi = round((thick + 2) * 1e-4 / r1 * 1e3, 4)
                            r['sigma_e_range_mScm'] = f'{_lo}-{_hi}'
                            r['note'] = f'SUS ion-blocking → R1=R_e; σ_e=L/R1 (L={thick:g}µm 지정)'
                    except (TypeError, ValueError):
                        pass
            with open(fits, 'w', newline='') as fh:
                w = _csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)
        except Exception as e:
            return jsonify({'error': f'σ_e 재계산 실패: {e}', **_eis_exp_table()}), 200
    return jsonify({'ok': True, 'filename': fn, 'thickness_um': round(thick, 2),
                    'sigma_e_recomputed': _is_sym,
                    'note': ('σ_e=L/R1 재계산됨' if _is_sym else
                             'L 기록됨 — σ_e 는 full 셀에서 정의되지 않아 계산하지 않음 '
                             '(R1=R_int 는 계면 ASR).  두께가 다른 full 셀 비교·physics-EIS '
                             '대조에 쓰입니다'),
                    **_eis_exp_table()})


@app.route('/api/eis_exp_upload', methods=['POST'])
def api_eis_exp_upload():
    """실험 EIS 파일 업로드 → 아카이브 → 추출(.mpr=galvani/WSL) → CNLS fit(eis_fit) → 값도출.
    허용: .mpr(BioLogic 바이너리)·.mps(설정)·.csv(우리 tidy: freq_Hz,ReZ_ohm,negImZ_ohm).
    galvani 부재(클라우드) 시 .mpr 은 raw 저장+파싱대기(WSL), .csv 는 즉시 fit."""
    import csv as _csv
    import subprocess as _sp
    P = _eis_archive_paths()
    os.makedirs(P['raw'], exist_ok=True); os.makedirs(P['extracted'], exist_ok=True)
    files = request.files.getlist('files')
    if not files:
        return jsonify({'error': '파일 없음'}), 200
    saved, notes = [], []
    for fs in files:
        raw_name = (fs.filename or '').strip()
        if not raw_name:
            continue
        base = os.path.basename(raw_name).replace('\\', '_').replace('/', '_')
        stem, ext = os.path.splitext(base); ext = ext.lower()
        base = stem + ext          # ★확장자 소문자로 정규화 (감사 L2): 대문자 .CSV 는 저장은 되지만
        #                            eis_archive/eis_fit 의 endswith('.csv')(대소문자 구분)에 안 걸려
        #                            표에 영영 안 나타나는데 업로드 응답은 성공을 알렸다.
        if ext not in ('.mpr', '.mps', '.csv'):
            notes.append(f'{base}: 확장자 미지원 (.mpr/.mps/.csv)'); continue
        # 셀타입 미상시 파일명으로 추정 (sym/full) — 없으면 사용자 접두어 권장
        if ext == '.csv':
            dst = _contained_join(P['extracted'], base)
            fs.save(dst)
            # tidy 검증 (필수 열)
            try:
                hdr = next(_csv.reader(open(dst)), [])
                if not ({'freq_Hz', 'ReZ_ohm', 'negImZ_ohm'} <= set(h.strip() for h in hdr)):
                    notes.append(f'{base}: CSV 열 부족 (freq_Hz,ReZ_ohm,negImZ_ohm 필요) — 저장은 됨')
            except Exception:
                pass
            saved.append(base)
        else:                                                 # .mpr / .mps → raw
            dst = _contained_join(P['raw'], base)
            fs.save(dst)
            saved.append(base)
    if not saved:
        return jsonify({'error': '저장된 파일 없음', 'notes': notes, **_eis_exp_table()}), 200
    # 업로드 시 두께 지정(선택) → fit 실행 전에 thickness_overrides.json 기록 (stem 키 = eis_fit 규약)
    # ⇒ 같은 pass 의 CNLS fit 이 바로 이 L 로 σ_e=L/R1 계산 (사후 /api/eis_exp_thickness 재계산 불필요)
    import json as _json
    try:
        _th = float(request.form.get('thickness_um') or '')
    except (TypeError, ValueError):
        _th = None
    if _th is not None and 0.5 <= _th <= 300:
        ov_path = os.path.join(P['archive'], 'thickness_overrides.json')
        try:
            ov = _json.load(open(ov_path)) if os.path.isfile(ov_path) else {}
        except Exception:
            ov = {}
        for b in saved:
            ov[os.path.splitext(b)[0]] = round(_th, 2)
        try:
            with open(ov_path, 'w') as fh:
                _json.dump(ov, fh, ensure_ascii=False, indent=1)
            notes.append(f'L={_th:g}µm 지정 → 대칭셀 σ_e=L/R1 이 이 두께로 즉시 계산됨')
        except Exception as e:
            notes.append(f'두께 저장 실패: {e}')
    elif _th is not None:
        # ★기존 override 가 있으면 45 가 아니라 그게 쓰인다 — "기본 45µm 로 fit" 은 거짓이었음 (감사 M6)
        try:
            _ov0 = _json.load(open(os.path.join(P['archive'], 'thickness_overrides.json')))
        except Exception:
            _ov0 = {}
        _kept = {os.path.splitext(b)[0]: _ov0[os.path.splitext(b)[0]]
                 for b in saved if os.path.splitext(b)[0] in _ov0}
        notes.append(f'두께 {_th}µm 범위 밖(0.5~300) — 무시.  '
                     + (f'기존 지정 L={"/".join(f"{v:g}" for v in _kept.values())}µm 유지'
                        if _kept else '기본 45µm 로 fit'))
    # 추출(.mpr, galvani 있으면) + 카탈로그 재생성
    # 두 스크립트는 **다른 패키지**를 요구한다 (archive=galvani[.mpr 파싱], fit=impedance[CNLS])
    # → 각자 그 패키지를 가진 인터프리터로 돌린다.  둘이 서로 다른 venv 에 있어도 동작.
    arch_msg = ''
    try:
        r = _sp.run([_eis_python('galvani'), os.path.join(P['root'], 'scripts', 'eis_archive.py')],
                    capture_output=True, text=True, timeout=180, cwd=P['root'])
        arch_msg = _subproc_msg(r, 'archive(추출)')
        arch_ok = (r.returncode == 0)
    except Exception as e:
        arch_msg, arch_ok = f'⛔ archive 실행 실패: {e}', False
    # CNLS fit (impedance 있으면) → 값도출
    fit_msg = ''
    try:
        r = _sp.run([_eis_python('impedance'), os.path.join(P['root'], 'scripts', 'eis_fit.py')],
                    capture_output=True, text=True, timeout=300, cwd=P['root'])
        fit_msg = _subproc_msg(r, 'fit(CNLS)')
        fit_ok = (r.returncode == 0)
    except Exception as e:
        fit_msg, fit_ok = f'⛔ fit 실행 실패: {e}', False
    tab = _eis_exp_table()
    # ★ 2026-08-03: 옛 코드는 fit 이 죽어도 ok:True 를 돌려줘 UI 가 초록 ✓ 를 띄웠고, 표는 **옛
    #   결과**를 그대로 그렸다 — 사용자에겐 "저장은 됐는데 값이 안 뜬다 / L 지정이 안 먹는다" 로
    #   보인다 (실제 신고).  실패를 실패로 돌려준다.
    return jsonify({'ok': bool(fit_ok and arch_ok), 'saved': saved, 'notes': notes,
                    'archive': arch_msg, 'fit': fit_msg,
                    'stale_table': not fit_ok,       # True = 아래 표는 이번 업로드 반영 전 값
                    **tab})


_EIS_PY_CACHE = {}


def _eis_python(need_mod=None):
    """EIS 하위 스크립트를 돌릴 인터프리터 — `need_mod` 를 **실제로 import 할 수 있는** 것을 고른다.

    ★ 왜 (2026-08-03): 옛 코드는 `os.environ.get('PYTHON','python3')` 였다.  그런데 webapp 이
      venv 로 뜨면 그 안의 python3 가 잡히는데, 사용자가 셸에서 `python3 scripts/eis_fit.py` 를
      돌리면 **시스템 python3**(~/.local 사이트패키지 포함)가 잡힌다.  실제로 셸에서는 fit 15/15
      로 성공하는데 webapp 에서는 `No module named 'impedance'` 로 죽는 상황이 나왔다 — 같은
      기계, 같은 스크립트, 다른 인터프리터.  사람이 "어느 pip 이냐"를 추적하게 두지 않는다.

    순서: $PYTHON → 이 프로세스(sys.executable) → PATH 의 python3 → 흔한 사용자 venv.
    전부 실패하면 첫 후보를 돌려주고 (오류 메시지는 _subproc_msg 가 설치법까지 안내한다).
    """
    key = need_mod or ''
    if key in _EIS_PY_CACHE:
        return _EIS_PY_CACHE[key]
    import subprocess as _sp
    cands = [os.environ.get('PYTHON'), sys.executable, 'python3',
             os.path.expanduser('~/.venv/bin/python3'),
             os.path.expanduser('~/venv/bin/python3')]
    cands = [c for i, c in enumerate(cands) if c and c not in cands[:i]]
    chosen = cands[0]
    if need_mod:
        for c in cands:
            try:
                if _sp.run([c, '-c', f'import {need_mod}'], capture_output=True,
                           timeout=25).returncode == 0:
                    chosen = c
                    break
            except Exception:                                 # 없는 실행파일·타임아웃 → 다음 후보
                continue
    _EIS_PY_CACHE[key] = chosen
    return chosen


def _subproc_msg(r, label):
    """서브프로세스 결과 → 사람이 고칠 수 있는 한 줄.  (2026-08-03)

    ★ 왜 필요한가: 옛 코드는 `(r.stderr or '').strip()[:200]` = traceback 의 **앞** 200자를
      보여줬다.  파이썬 traceback 의 앞부분은 `Traceback… File "…", line 261, in <module>`
      이고 **정작 원인인 마지막 줄**(`ModuleNotFoundError: No module named 'impedance'`)이
      잘려나간다.  실제로 화면에 `…line 142, in main from i` 까지만 떠서 원인 판독이
      불가능했다.  게다가 returncode 를 안 봐서 실패인데 ok:True + 초록 ✓ 가 떴다.
    """
    if r.returncode == 0:
        _out = (r.stdout or '').strip().splitlines()
        return _out[-1] if _out else ''
    err = (r.stderr or '').strip()
    lines = [l for l in err.splitlines() if l.strip()]
    last = lines[-1] if lines else f'(stderr 없음, exit {r.returncode})'
    m = re.search(r"No module named '([^']+)'", err)          # 가장 흔한 원인 → 처방까지
    if m:
        return (f'⛔ {label} 실패 — 파이썬 패키지 **{m.group(1)}** 미설치.  '
                f'설치: pip install {m.group(1)}   (webapp 이 쓰는 인터프리터에: '
                f'$PYTHON -m pip install {m.group(1)})')
    return f'⛔ {label} 실패 (exit {r.returncode}): {last[:300]}'


@app.route('/api/eis_exp_rename', methods=['POST'])
def api_eis_exp_rename():
    """실험 EIS 측정 **이름 변경** — raw/extracted 파일 + fits CSV 행 + 두께 override 를 함께 옮긴다.

    부분 개명은 데이터를 잃는다: 파일만 바꾸고 fits 행을 안 옮기면 표에서 사라지고,
    override 만 남으면 다음 재fit 이 **남의 두께**를 상속한다 (삭제 경로가 이미 겪은 문제,
    2026-07-27 감사 M5).  ⇒ 네 곳을 한 번에, 실패하면 아무것도 안 바꾼다.
    POST JSON {filename, new_name}.  확장자는 유지 (사용자가 줘도 무시).
    """
    import csv as _csv
    import json as _json
    P = _eis_archive_paths()
    body = request.get_json(silent=True) or {}
    fn = (body.get('filename') or '').strip()
    new = (body.get('new_name') or '').strip()
    if not fn or not new:
        return jsonify({'error': 'filename / new_name 필요'}), 200
    stem, ext = os.path.splitext(fn)
    new_stem = os.path.splitext(new)[0].strip()
    # 파일명 안전성: 경로구분자·상위참조 거부 (표시용 이름이 곧 파일명이라 여기서 막는다)
    if not new_stem or not re.fullmatch(r'[A-Za-z0-9가-힣 ._+#()\-]{1,120}', new_stem):
        return jsonify({'error': '이름은 영문/숫자/한글/공백/._+#()- 만, 1~120자 '
                                 '(경로구분자·상위참조 금지)'}), 200
    if new_stem == stem:
        return jsonify({'error': '같은 이름입니다', **_eis_exp_table()}), 200
    new_fn = new_stem + ext
    # 대상 존재 확인 + 중복 거부 (덮어쓰면 남의 측정을 조용히 파괴한다)
    _rows = {r['filename']: r for r in (_eis_exp_table().get('rows') or [])}
    if fn not in _rows:
        return jsonify({'error': f'그런 측정 없음: {fn}'}), 200
    if new_fn in _rows:
        return jsonify({'error': f'이미 있는 이름: {new_fn}'}), 200
    moved = []
    try:
        for folder in ('raw', 'extracted'):
            for _e in ({ext, '.csv', '.mpr', '.mps'} if folder == 'raw' else {'.csv'}):
                src = _contained_join(P[folder], stem + _e)
                if os.path.isfile(src):
                    dst = _contained_join(P[folder], new_stem + _e)
                    if os.path.exists(dst):
                        raise RuntimeError(f'대상이 이미 있음: {os.path.basename(dst)}')
                    os.rename(src, dst)
                    moved.append((dst, src))                  # 되돌리기용 (dst→src)
    except Exception as e:
        for dst, src in reversed(moved):                      # 부분 개명 롤백
            try:
                os.rename(dst, src)
            except Exception:
                pass
        return jsonify({'error': f'파일 이름변경 실패(되돌림): {e}'}), 200
    # 두께 override 이관 (남기면 다음 재fit 이 남의 두께를 상속)
    ov_path = os.path.join(P['archive'], 'thickness_overrides.json')
    try:
        ov = _json.load(open(ov_path)) if os.path.isfile(ov_path) else {}
        for _k in (stem, fn):
            if _k in ov:
                ov[new_stem] = ov.pop(_k)
        with open(ov_path, 'w') as fh:
            _json.dump(ov, fh, ensure_ascii=False, indent=1)
    except Exception:
        pass
    # fits CSV 행 이관 (안 옮기면 표에서 사라진다 = 값 손실로 보임)
    fits = P['fits']
    if os.path.isfile(fits):
        try:
            with open(fits, newline='') as fh:
                rd = _csv.DictReader(fh); cols = rd.fieldnames; rows = list(rd)
            for r in rows:
                if r.get('filename') in (fn, stem):
                    r['filename'] = new_fn
                if r.get('stem') == stem:
                    r['stem'] = new_stem
            with open(fits, 'w', newline='') as fh:
                w = _csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)
        except Exception as e:
            return jsonify({'error': f'파일은 바뀌었으나 fit 기록 이관 실패: {e}',
                            **_eis_exp_table()}), 200
    return jsonify({'ok': True, 'filename': fn, 'new_filename': new_fn, **_eis_exp_table()})


@app.route('/api/eis_exp_delete', methods=['POST'])
def api_eis_exp_delete():
    """실험 EIS 측정 파일 삭제 — 원본·추출·fit 기록 제거.
    POST JSON {filename: 'name.csv'}."""
    import csv as _csv
    P = _eis_archive_paths()
    body = request.get_json(silent=True) or {}
    fn = (body.get('filename') or '').strip()
    if not fn:
        return jsonify({'error': 'filename 없음'}), 200
    # path traversal 방지
    try:
        safe_fn = _contained_join(P['archive'], fn)
        if not safe_fn.startswith(P['archive']):
            return jsonify({'error': 'invalid path'}), 403
    except Exception:
        return jsonify({'error': 'path error'}), 400
    # 1) 원본/추출 파일 삭제
    deleted = []
    for folder in ['raw', 'extracted']:
        path = _contained_join(P[folder], fn)
        if os.path.isfile(path):
            try:
                os.remove(path)
                deleted.append(folder)
            except Exception:
                pass
    # 1-b) 두께 override 도 제거 (2026-07-27 감사 M5): 안 지우면 같은 셀을 다시 재서 업로드할 때
    #      옛 L 을 조용히 상속해 σ_e=L/R1 이 틀린 두께로 산출된다 (재측정 워크플로에서 실제로 발생).
    import json as _json
    _ovp = os.path.join(P['archive'], 'thickness_overrides.json')
    if os.path.isfile(_ovp):
        try:
            _ov = _json.load(open(_ovp))
            if _ov.pop(os.path.splitext(fn)[0], None) is not None:
                with open(_ovp, 'w') as _fh:
                    _json.dump(_ov, _fh, ensure_ascii=False, indent=1)
                deleted.append('thickness_override')
        except Exception:
            pass
    # 2) fit 기록에서 행 제거
    fits = P['fits']
    if os.path.isfile(fits):
        try:
            with open(fits, newline='') as fh:
                rd = _csv.DictReader(fh)
                cols = rd.fieldnames
                rows = [r for r in rd if r.get('filename') != fn]
            with open(fits, 'w', newline='') as fh:
                w = _csv.DictWriter(fh, fieldnames=cols)
                w.writeheader()
                w.writerows(rows)
            deleted.append('fit_record')
        except Exception:
            pass
    # 3) 카탈로그에서 행 제거
    cat = P['catalog']
    if os.path.isfile(cat):
        try:
            with open(cat, newline='') as fh:
                rd = _csv.DictReader(fh)
                cols = rd.fieldnames
                rows = [r for r in rd if r.get('filename') != fn]
            with open(cat, 'w', newline='') as fh:
                w = _csv.DictWriter(fh, fieldnames=cols)
                w.writeheader()
                w.writerows(rows)
            deleted.append('catalog')
        except Exception:
            pass
    return jsonify({'ok': True, 'filename': fn, 'deleted': deleted, **_eis_exp_table()})


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

    # Return the auto-DETECTED mode so the frontend can show a confirm popup
    # ("감지된 모드: bimodal — 실행할까요?") and the user can verify bimodal vs standard
    # BEFORE committing the run.  The run itself is then triggered by that confirm → POST
    # /analyze, which spawns the SAME daemon-thread full pipeline (incl. Step 7 Stage E) that
    # survives a tab close — so a confirmed run still always gets Stage E.  If the user cancels,
    # the case stays status 'uploaded' (대기중) and is runnable any time from the list via
    # '재분석' (so a cancel is recoverable, not a silently-broken case).
    return jsonify({'case_id': case_id, 'mode': mode, 'files': filenames, 'analyzing': False})

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
                    net_cmd = [sys.executable, os.path.join(app.config['SCRIPTS_FOLDER'], 'network_conductivity.py'),
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

        # ── Step 7: Stage E — literature-grounded grain corrections ──
        # Mirrors the archive-reanalyze pipeline (line ~2540) so that EVERY
        # analysis path — new upload, 재분석, 재분석(NET) — applies Stage E.
        # Without this, cases analysed via /analyze had no *_stage_e σ values
        # and the 종합 등급 'Stage E 보정 적용' axis flagged them B-.
        #   σ_ionic : Cronau 2022 SE-size factor (×1.0 for r_SE ≥ 0.5 μm)
        #   σ_e     : Trevisanello 2021 AM-crystallinity × size
        #   κ       : Wang 2022 phonon GB-scatter
        # Idempotent — re-running just overwrites *_stage_e keys.
        try:
            scripts_dir = app.config['SCRIPTS_FOLDER']
            stage_e_cmd = [sys.executable,
                            os.path.join(scripts_dir, 'run_network_full_corrections.py'),
                            os.path.basename(results_dir), '--quiet']
            _se = subprocess.run(stage_e_cmd, capture_output=True,
                                  text=True, timeout=None)
            print(f"  [Stage E] rc={_se.returncode} ({case_id})")
            if _se.returncode != 0 and _se.stderr:
                print(f"  [Stage E] stderr (last 300): {_se.stderr[-300:]}")
            # POST-CHECK: verify Stage E populated all 3 channels in BOTH
            # contact modes (Hertz + Physics).  If any channel-mode missing,
            # log a warning so user can see in case list (Stage-E-P badge).
            # Common missed case: thermal_sigma_full_mScm_stage_e_physics fell
            # through silently when physics-mode solver returned None.
            try:
                fm_path = os.path.join(results_dir, 'full_metrics.json')
                if os.path.exists(fm_path):
                    with open(fm_path) as _f:
                        _fm = json.load(_f)
                    _missing = []
                    for _k in ('sigma_full_mScm_stage_e_physics',
                                'electronic_sigma_full_mScm_stage_e_physics',
                                'thermal_sigma_full_mScm_stage_e_physics'):
                        if not _fm.get(_k):
                            _missing.append(_k.replace('_stage_e_physics', '').replace('_full_mScm', ''))
                    if _missing:
                        print(f"  [Stage E] ⚠ Physics-mode incomplete: {', '.join(_missing)} "
                              f"({case_id}) — will show 'Stage-E-P ⚠' badge in case list")
            except Exception as _exc:
                print(f"  [Stage E post-check] {type(_exc).__name__}: {_exc}")
            # Refresh validation flags self-report card after Stage E.
            # backfill_validation_flags.py takes case NAMES as positional args.
            bf_cmd = [sys.executable,
                       os.path.join(scripts_dir, 'backfill_validation_flags.py'),
                       os.path.basename(results_dir)]
            try:
                subprocess.run(bf_cmd, capture_output=True, text=True, timeout=None)
            except Exception:
                pass   # backfill is best-effort
        except Exception as _se_e:
            print(f"  [Stage E] FAILED ({case_id}): {_se_e}")

        # Sync results + updated meta to Supabase
        storage_sync.sync_dir_to_remote(case_dir, f'uploads/{case_id}')
        storage_sync.sync_dir_to_remote(results_dir, f'results/{case_id}')

    def _run_guarded():
        # Without this, any uncaught error in _run kills the daemon thread and
        # the case is stuck at status 'running' forever (no failure shown).
        try:
            _run()
        except Exception as _e:
            import traceback
            traceback.print_exc()
            try:
                meta['status'] = 'error'
                meta['analysis_error'] = f'{type(_e).__name__}: {_e}'
                with open(meta_file, 'w') as f:
                    json.dump(meta, f, indent=2)
            except Exception:
                pass

    thread = threading.Thread(target=_run_guarded, daemon=True)
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
                    net_cmd = [sys.executable, os.path.join(app.config['SCRIPTS_FOLDER'], 'network_conductivity.py'),
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
                            subprocess.run([sys.executable,
                                             os.path.join(app.config['SCRIPTS_FOLDER'],
                                                          'run_network_full_corrections.py'),
                                             case_id, '--quiet'],
                                            capture_output=True, text=True,
                                            timeout=None)
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
                subprocess.run([sys.executable, os.path.join(scripts, ac_script),
                                c['atoms'], c['contacts'], '-o', c['results_dir'],
                                '-t', type_map, '-s', scale],
                               capture_output=True, text=True, timeout=None)

                # 2) Network solver in BOTH modes. Idempotent for Hertzian
                #    (our solver patch only adds R_film when contact_mode ==
                #    'physics', so Hertzian σ is unchanged) but it guarantees
                #    that network_conductivity_{hertzian,physics,dual}.json +
                #    legacy network_conductivity.json are all rewritten fresh
                #    — no stale pre-patch data slipping into the merge.
                with _network_solver_lock:
                    subprocess.run([sys.executable, os.path.join(scripts, 'network_conductivity.py'),
                                    c['atoms'], c['contacts'], '-o', c['results_dir'],
                                    '-t', type_map, '-s', scale,
                                    '--contact-mode', 'both'],
                                   capture_output=True, text=True, timeout=None)

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
                subprocess.run([sys.executable, os.path.join(scripts, 'coverage_physics_vs_hertzian.py'),
                                '--case-dir', c['case_dir']],
                               capture_output=True, text=True, timeout=None)

                # 5) Stage E refresh — writes σ_ionic/σ_e/κ _stage_e keys +
                #    validation_flags self-report card.  Idempotent (overwrites
                #    previous Stage E with fresh-baseline-derived corrections).
                #    Same call shape as the /analyze pipeline; without this the
                #    Trust card stays blank and the /audit dashboard shows the
                #    case as 'no-stage-e' after a batch rerun.
                subprocess.run([sys.executable,
                                 os.path.join(scripts, 'run_network_full_corrections.py'),
                                 c['cid'], '--quiet'],
                               capture_output=True, text=True, timeout=None)

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


def _resolve_results_dir(case_id, meta):
    """Return (results_dir, archive_rel) for a case, falling back to archive/
    when the live results/ dir has no analysis data (archive-migrated cases).
    archive_rel is the path under archive/ when the fallback triggered, else
    None.  Shared by the /single dashboard and the report exporter so both see
    the same data."""
    results_dir = get_results_dir(case_id)

    def _has_data(d):
        if not os.path.isdir(d):
            return False
        return any(os.path.exists(os.path.join(d, n + '.csv'))
                   for n in ['atom_statistics', 'contact_summary',
                             'coordination_summary', 'network_summary']) \
            or os.path.exists(os.path.join(d, 'full_metrics.json'))

    if _has_data(results_dir):
        return results_dir, None

    archive_root = app.config.get('ARCHIVE_FOLDER')
    if archive_root and os.path.isdir(archive_root):
        search_keys = [case_id]
        for k in ('name', 'label', 'case_id', 'case_name'):
            v = meta.get(k)
            if isinstance(v, str) and v and v not in search_keys:
                search_keys.append(v)
        for dirpath, dirs, _ in os.walk(archive_root):
            for key in search_keys:
                if key in dirs:
                    candidate = os.path.join(dirpath, key)
                    if _has_data(candidate):
                        return candidate, os.path.relpath(candidate, archive_root)
    return results_dir, None


def _load_case_tables(results_dir, meta):
    """Assemble the analysis-summary `tables` dict (입자 정보 / 접촉 요약 /
    배위수 / 네트워크 지표 / 취성 파괴 / 종합 등급) plus the metrics and
    input_params exactly as the single-case dashboard does, so MD/PDF reports
    stay byte-for-byte consistent with what the page shows.

    Returns (tables, metrics, input_params)."""
    import pandas as pd
    tables = {}
    for csv_name in ['atom_statistics', 'contact_summary', 'coordination_summary',
                     'network_summary']:
        csv_path = os.path.join(results_dir, f'{csv_name}.csv')
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            tables[csv_name] = {
                'columns': df.columns.tolist(),
                'data': df.values.tolist(),
            }

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
            sigma_brug_mScm = round(_sigma_grain_mS_cm(metrics) * metrics['sigma_ratio'], 4)
            for idx, row in enumerate(tables['network_summary']['data']):
                if 'σ_brug/σ_grain' in str(row[0]):
                    tables['network_summary']['data'].insert(
                        idx, ['σ_Bruggeman (mS/cm)', sigma_brug_mScm])
                    break

    # input_params (RVE area for inject_cell_asr_rows)
    input_params = {}
    params_path = os.path.join(results_dir, 'input_params.json')
    if os.path.exists(params_path):
        with open(params_path) as f:
            input_params = json.load(f)
    if input_params and 'scale' not in input_params:
        input_params['scale'] = meta.get('scale', 1)

    # ── PHANTOM σ_e/κ STRIP (2026-05-28, v4 unified) ────────────────────
    # If the Stage E pipeline used Bruggeman fallback (stage_e_source flags
    # 'fallback_weighted_factor'), the value was ALSO written to the raw
    # network-solver key — causing the Network Solver row to display the
    # phantom value (e.g. 1mAh_100_2 showed σ_e Physics=61.83 even though
    # raw electronic was suppressed elsewhere).  Strip those raw keys here
    # so EVERY downstream renderer (Network Solver row, ASR row, Stage E
    # row, predictor) sees '—' consistently.
    _src_fb_global = metrics.get('stage_e_source') or {}
    _phantom_strip_pairs = [
        ('electronic_sigma_full_mScm',          'sigma_e'),
        ('electronic_sigma_full_mScm_physics',  'sigma_e_physics'),
        ('thermal_sigma_full_mScm',             'sigma_thermal'),
        ('thermal_sigma_full_mScm_physics',     'sigma_thermal_physics'),
    ]
    for _rk, _sk in _phantom_strip_pairs:
        if _src_fb_global.get(_sk) == 'fallback_weighted_factor':
            metrics[_rk] = None
            # also strip Stage E + Stage E physics counterparts
            metrics[_rk + '_stage_e'] = None
            metrics[_rk + '_stage_e_physics'] = None

    # 4-column transform + section injection — shared helpers
    transform_network_summary_4col(tables, metrics, meta)
    inject_tier1_patch_rows(tables, metrics)
    inject_stage_e_rows(tables, metrics)
    inject_cell_asr_rows(tables, metrics, input_params)
    normalize_network_summary_layout(tables, metrics)
    apply_paper_labels(tables)
    inject_dual_porosity_rows(tables, metrics)
    # ── Phantom σ_e / κ suppression (v7 — unconditional, AFTER label rename) ──
    # v6 placed inside normalize's Hertz+Phys merge if-block, which doesn't
    # run for already-merged cases.  Now called from the route handler so
    # it runs for EVERY case, scanning the FINAL paper-labeled rows.
    if 'network_summary' in tables:
        _suppress_phantom_sigma_rows(tables['network_summary'].get('data', []),
                                     metrics)

    fracture_tbl = build_fracture_summary_table(metrics)
    if fracture_tbl is not None:
        tables['fracture_summary'] = fracture_tbl

    overall_tbl = build_overall_grade_table(metrics, results_dir)
    if overall_tbl is not None:
        tables['overall_grade'] = overall_tbl

    return tables, metrics, input_params


def _load_mpm_metrics(results_dir):
    """MPM result params for the case page — the compact mpm_metrics.json written on
    upload (falls back to extracting from the heavier mpm_payload.json).  {} when no
    MPM result has been uploaded yet (→ the result table stays hidden).

    MERGE (2026-07-14): the sim이 뽑는 mpm_metrics.json에는 payload 파생 지표(step3 σ/
    pore-τ/additive_dispersion 등)가 없어서, 그 파일이 small을 덮으면 카드의 STEP3 행들이
    사라진다 → small에 payload 지표가 빠져 있으면 payload에서 1회 추출해 병합하고 small을
    다시 써서 캐시 (다음 뷰부터는 무거운 payload를 안 읽음).  sim 키가 우선(authoritative)."""
    small = os.path.join(results_dir, 'mpm_metrics.json')
    out = {}
    if os.path.exists(small):
        try:
            with open(small) as f:
                out = json.load(f) or {}
        except Exception:
            out = {}
    # payload-파생 지표 마커 = se_surface_tris (payload mpm_metrics에는 항상 있고 sim 파일엔 없음)
    if 'se_surface_tris' not in out:
        payload = os.path.join(results_dir, 'mpm_payload.json')
        if os.path.exists(payload):
            try:
                with open(payload) as f:
                    pm = (json.load(f) or {}).get('mpm_metrics', {}) or {}
                if pm:
                    pm.update(out)                          # sim(small) 키가 payload 키를 덮음
                    out = pm
                    try:
                        with open(small, 'w') as f:
                            json.dump(out, f)               # 병합 캐시 — 재스캔 방지
                    except Exception:
                        pass
            except Exception:
                pass
    return out


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
    results_dir, archive_path = _resolve_results_dir(case_id, meta)

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

    # Summary tables + metrics + input_params (shared with the report exporter)
    tables, metrics, input_params = _load_case_tables(results_dir, meta)

    return render_template('single.html', case=meta, figures=figures,
                         report=report, tables=tables, metrics=metrics,
                         input_params=input_params, archive_path=archive_path,
                         mpm_metrics=_load_mpm_metrics(results_dir),
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
        # Categories ordered to mirror the σ_ionic/σ_e production forms' inputs:
        #   composition → structure → SE interface (ionic) → AM interface
        #   (electronic, Stage 15) → transport (Stage E, all 3 channels) →
        #   contact mechanics → stress.  Each transport channel shows the
        #   Stage E value (phantom-filtered) — what the production fit targets.
        display_keys_raw = [
            # ── 조성/구조 ──
            ('P:S', '', 'ps_ratio', '조성/구조'),
            ('φ_AM', '', 'phi_am', '조성/구조'),
            ('φ_SE', '', 'phi_se', '조성/구조'),
            ('Porosity', '(%)', 'porosity', '조성/구조'),
            ('Porosity (union)', '(%)', 'porosity_union', '조성/구조'),
            ('Overlap fraction', '(%)', 'overlap_fraction_pct', '조성/구조'),
            ('두께', '(μm)', 'thickness_um', '조성/구조'),
            # ── SE 계면/네트워크 (σ_ionic form inputs) ──
            ('SE-SE CN', '', 'se_se_cn', 'SE 네트워크'),
            ('SE-SE CN std', '', 'se_se_cn_std', 'SE 네트워크'),
            ('SE-SE Total', '(μm²)', 'area_SE_SE_total', 'SE 네트워크'),
            ('Coverage P', '(%)', 'coverage_AM_P_mean', 'SE 네트워크'),
            ('Coverage S', '(%)', 'coverage_AM_S_mean', 'SE 네트워크'),
            ('Percolation', '(%)', 'percolation_pct', 'SE 네트워크'),
            ('Tortuosity', '', 'tortuosity_mean', 'SE 네트워크'),
            ('Hop Area', '(μm²)', 'path_hop_area_mean', 'SE 네트워크'),
            ('Bottleneck', '(μm²)', 'path_hop_area_min_mean', 'SE 네트워크'),
            # ── AM 네트워크 (σ_e Stage 15 form inputs) ──
            ('AM-AM CN', '', 'am_am_cn', 'AM 네트워크'),
            ('AM-AM Mean Area', '(μm²)', 'am_am_mean_area', 'AM 네트워크'),
            ('AM-AM N contacts', '', 'am_am_n_contacts', 'AM 네트워크'),
            ('AM-SE CN', '', 'am_se_cn_mean', 'AM 네트워크'),
            ('AM Vulnerable', '(%)', 'am_vulnerable_pct', 'AM 네트워크'),
            ('Ionic Active', '(%)', 'ionic_active_pct', 'AM 네트워크'),
            # ── Transport (Stage E — production form targets) ──
            ('σ_ionic (Stage E)', '(mS/cm)', '_sigma_i_stage_e_display', '전송 (Stage E)'),
            ('σ_electronic (Stage E)', '(mS/cm)', '_sigma_e_stage_e_display', '전송 (Stage E)'),
            ('σ_thermal (Stage E)', '(mS/cm)', '_sigma_k_stage_e_display', '전송 (Stage E)'),
            ('R_brug', '(×)', 'R_brug_over_full', '전송 (Stage E)'),
            ('Constriction', '(%)', '_constriction_pct', '전송 (Stage E)'),
            # ── 접촉력 (force chain) ──
            ('Fn AM-AM', '(μN)', 'fn_AM_P_AM_P_mean', '접촉력'),
            ('Fn AM-SE', '(μN)', 'fn_AM_P_SE_mean', '접촉력'),
            ('Fn SE-SE', '(μN)', 'fn_SE_SE_mean', '접촉력'),
            ('CP mean', '(MPa)', 'contact_pressure_mean', '접촉력'),
            ('CP max', '(MPa)', 'contact_pressure_max', '접촉력'),
            # ── 응력 분포 ──
            ('Stress CV', '(%)', 'stress_cv', '응력'),
            ('σ_AM_P/σ_mean', '', 'stress_ratio_AM_P', '응력'),
            ('σ_AM_S/σ_mean', '', 'stress_ratio_AM_S', '응력'),
            ('σ_SE/σ_mean', '', 'stress_ratio_SE', '응력'),
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

            # Stage E σ display (phantom-aware) — matches what production form fits.
            # For σ_e: requires raw > 0 AND not both-fallback (input_1mAh_5 raw=51.89
            # would otherwise be misleading vs Stage E=9.014).  Same logic for σ_ionic
            # and σ_thermal Stage E columns.
            src = metrics.get('stage_e_source') or {}
            # σ_e Stage E
            raw_e = metrics.get('electronic_sigma_full_mScm')
            if (isinstance(raw_e, (int, float)) and raw_e > 0
                    and not (src.get('sigma_e') == 'fallback_weighted_factor'
                             and src.get('sigma_e_physics') == 'fallback_weighted_factor')):
                stE_e = metrics.get('electronic_sigma_full_mScm_stage_e')
                metrics['_sigma_e_stage_e_display'] = (
                    stE_e if isinstance(stE_e, (int, float)) and 0 < stE_e <= 100
                    else (raw_e if raw_e <= 100 else None))
            else:
                metrics['_sigma_e_stage_e_display'] = None
            # σ_thermal Stage E
            raw_k = metrics.get('thermal_sigma_full_mScm')
            if (isinstance(raw_k, (int, float)) and raw_k > 0
                    and src.get('sigma_thermal') != 'fallback_weighted_factor'):
                stE_k = metrics.get('thermal_sigma_full_mScm_stage_e')
                metrics['_sigma_k_stage_e_display'] = (
                    stE_k if isinstance(stE_k, (int, float)) and stE_k > 0
                    else raw_k)
            else:
                metrics['_sigma_k_stage_e_display'] = None
            # σ_ionic Stage E (prefer stage_e value; raw fallback)
            stE_i = metrics.get('sigma_full_mScm_stage_e')
            raw_i = metrics.get('sigma_full_mScm')
            metrics['_sigma_i_stage_e_display'] = (
                stE_i if isinstance(stE_i, (int, float)) and stE_i > 0
                else (raw_i if isinstance(raw_i, (int, float)) and raw_i > 0 else None))

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
    cid_to_name = {}  # case ID → the name the generator receives (for focus matching)
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
            cid_to_name[cid] = case_name

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
    cmd = [sys.executable, os.path.join(scripts, 'generate_comparison_plots.py'),
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
    # σ_e Y-axis max — user-set σ_AM(e) (mS/cm) ONLY controls plot y-axis ceiling
    # for σ_e plots.  Does NOT change form σ_S/σ_P anchors (those stay locked
    # at Trevisanello 10/5 literature defaults per Stage 22 design).
    sigma_AM_e = request.form.get('sigma_AM_e', '').strip()
    if sigma_AM_e:
        try:
            _sAM = float(sigma_AM_e)
            if _sAM > 0:
                cmd += ['--y-max-sigma-e', str(_sAM)]
        except ValueError:
            pass  # invalid → ignore, auto-scale
    # Generic parameter-comparison selections (param_scatter/bar/corr)
    param_x = request.form.get('param_x', '').strip()
    param_y = request.form.get('param_y', '').strip()
    param_list = request.form.get('param_list', '').strip()
    if param_x:
        cmd += ['--param-x', param_x]
    if param_y:
        cmd += ['--param-y', param_y]
    if param_list:
        cmd += ['--param-list', param_list]
    if request.form.get('param_norm') in ('1', 'true', 'on'):
        cmd += ['--param-norm']
    # "1-1" focus: saved case names to show as a focus parity (tab-separated,
    # since names can contain commas/colons). Fit stays on the full set.
    # focus_cases arrive as case IDs → translate to the exact names the
    # generator sees (archive names are basename'd, so name-matching is fragile).
    focus_cids = request.form.getlist('focus_cases')
    focus_names = [cid_to_name[c] for c in focus_cids if c in cid_to_name]
    if focus_names:
        cmd += ['--focus-cases', '\t'.join(focus_names)]
        focus_label = request.form.get('focus_label', '').strip()
        if focus_label:
            cmd += ['--focus-label', focus_label]
    # Full-corpus metrics for global (n=all) fit stats on per-group fit plots.
    fit_corpus_paths = []
    for cid in request.form.getlist('fit_corpus_cases'):
        if cid.startswith('archive:'):
            mp = os.path.join(app.config['ARCHIVE_FOLDER'], cid[len('archive:'):], 'full_metrics.json')
        else:
            mp = os.path.join(get_results_dir(cid), 'full_metrics.json')
        if os.path.exists(mp):
            fit_corpus_paths.append(mp)
    if fit_corpus_paths:
        cmd += ['--fit-corpus-inputs'] + fit_corpus_paths
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
            # Append the "1-1" focus variant (if any) right after its parent
            if f"{key}_focus" in info:
                plot_list.append(info[f"{key}_focus"])

    return jsonify({'session': session_id, 'plots': plot_list})

@app.route('/group/param-options', methods=['POST'])
def group_param_options():
    """Return the union of comparable numeric parameters across the selected
    cases — full_metrics.json scalars + derived 3D-viewer (viewer_aux.json)
    diagnostics — for the generic parameter-comparison picker."""
    selected = request.form.getlist('cases')
    keys = set()
    for cid in selected:
        if cid.startswith('archive:'):
            case_path = os.path.join(app.config['ARCHIVE_FOLDER'], cid[len('archive:'):])
        else:
            case_path = get_results_dir(cid)
        fm = os.path.join(case_path, 'full_metrics.json')
        if os.path.exists(fm):
            try:
                with open(fm) as f:
                    d = json.load(f)
            except (OSError, ValueError):
                d = {}
            for k, v in d.items():
                if (not k.startswith('_') and isinstance(v, (int, float))
                        and not isinstance(v, bool)):
                    keys.add(k)
        aux = os.path.join(case_path, 'viewer_aux.json')
        if os.path.exists(aux):
            try:
                with open(aux) as f:
                    a = json.load(f)
            except (OSError, ValueError):
                a = {}
            for k, v in a.items():
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    keys.add(f'aux:{k}')
            apts = a.get('se_articulation_points')
            if a.get('se_n_percolating') and (
                    a.get('se_n_articulation_points') is not None
                    or isinstance(apts, list)):
                keys.add('cut_fraction')
            if a.get('se_n_bn_below_threshold') is not None and a.get('se_n_perc_edges'):
                keys.add('bn_below_frac')
            if a.get('se_bn_median_norm') is not None:
                keys.add('bn_median_norm')
        # Grade-engine derived metrics (Q/ASR/τ_Laplace/cycle-stable …) →
        # 'grade:<label>' params (mirrors generate_comparison_plots._merged_params)
        if os.path.exists(fm):
            try:
                import sys as _sys
                _sd = os.path.join(os.path.dirname(__file__), '..', 'scripts')
                if _sd not in _sys.path:
                    _sys.path.insert(0, _sd)
                import grade_engine as _ge
                with open(fm) as f:
                    _m = json.load(f)
                _ip = {}
                _ipp = os.path.join(case_path, 'input_params.json')
                if os.path.exists(_ipp):
                    with open(_ipp) as f:
                        _ip = json.load(f)
                _meta = {}
                _mp = os.path.join(case_path, 'meta.json')
                if os.path.exists(_mp):
                    with open(_mp) as f:
                        _meta = json.load(f)
                _se = None
                _ap = os.path.join(case_path, 'viewer_aux.json')
                if os.path.exists(_ap):
                    with open(_ap) as f:
                        _a = json.load(f)
                    _apts = _a.get('se_articulation_points')
                    _se = {
                        'n_percolating': _a.get('se_n_percolating'),
                        'n_articulation_points': (_a.get('se_n_articulation_points')
                            if _a.get('se_n_articulation_points') is not None
                            else (len(_apts) if isinstance(_apts, list) else None)),
                        'n_bn_below_threshold': _a.get('se_n_bn_below_threshold'),
                        'n_perc_edges': _a.get('se_n_perc_edges'),
                        'bn_median_norm': _a.get('se_bn_median_norm'),
                    }
                _prepared = {**_m, **_ge.map_input_params(_ip, _meta)}
                for _lbl in _ge.axis_values(_prepared, _se):
                    keys.add(f'grade:{_lbl}')
            except Exception:
                pass
    return jsonify({'params': sorted(keys)})


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
        ('Porosity union(%)', 'porosity_union'),
        ('Overlap(%)', 'overlap_fraction_pct'),
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

@app.route('/results/<case_id>/3d-mpm-data')
def serve_3d_mpm_data(case_id):
    """Serve the pre-built MPM continuum payload (AM spheres + SE plastic-continuum
    surface mesh + mpm_metrics), in the SAME schema the DEM viewer already renders.
    Built off-line by scripts/mpm_webapp_payload.py and dropped into
    results/<case_id>/mpm_payload.json.  ?state=seed swaps in the loose pre-compaction
    SE surface (before/after view)."""
    results_dir = get_results_dir(case_id)
    payload_path = os.path.join(results_dir, 'mpm_payload.json')
    if not os.path.exists(payload_path):
        return jsonify({'error': 'No MPM payload for this case', 'kind': 'mpm', 'available': False}), 404
    with open(payload_path) as f:
        payload = json.load(f)
    if request.args.get('state') == 'seed' and payload.get('seed_mesh_triangles'):
        payload['mesh_triangles'] = payload['seed_mesh_triangles']     # before/after swap
    payload.pop('seed_mesh_triangles', None)                            # ship only the active mesh
    return jsonify(payload)


def _rint_anchor_pair(key):
    """R_int 시나리오 (pristine, cycled) Ω·cm² — 정본 docs/data/rint_eis_anchors.csv에서 읽음
    (scripts/rint_cycle_traj.load_scenario 재사용 = 단일 출처).  CSV/키 불가 시 2026-07-21 스냅샷
    fallback.  ⚠ load_scenario는 SystemExit를 던지므로 Exception만 잡으면 앱이 죽음."""
    if key not in ('sbe', 'dbe', 'csus', 'sus'):  # fallback dict에 없는 키가 CSV-실패 경로에서
        raise ValueError(f'unknown R_int scenario key: {key!r}')   # KeyError 500 되던 것 조기 차단
    try:
        import sys as _s
        _sd = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts')
        if _sd not in _s.path:
            _s.path.insert(0, _sd)
        from rint_cycle_traj import load_scenario
        r0, rc, _nt, _pr = load_scenario(key)
        return float(r0), float(rc)
    except (Exception, SystemExit):
        return {'sbe': (18.0, 110.0), 'dbe': (12.0, 46.0), 'csus': (10.0, 30.0),
                'sus': (50.0, 150.0)}[key]               # 이종기술 SUS = 실측 50 / 문헌투영 150 (SC √N)


@app.route('/rint-anchors')
def rint_anchors():
    """kit-gen UI 힌트 — 정본 anchors CSV의 시나리오 (pristine, cycled) R_int Ω·cm² (단일 출처)."""
    return jsonify({k: dict(zip(('pristine', 'cycled'), _rint_anchor_pair(k)))
                    for k in ('sbe', 'dbe', 'csus', 'sus')})


# ── ★ 운전조건 축 (온도 · 구동 스택압) — docs/temp_pressure_capability.md ──────────────────
#    두 축 모두 "미지정 = 현행" 이 절대 규약이다: &tempc=/&pop= 를 안 주면 킷 방출물은 예전과
#    **바이트 동일**하고, 이 블록은 코드 경로에 들어오지도 않는다.
#    ⚠ 온도는 σ_ion(SE) 하나만 움직인다 (Kraft 2017 σ·T Arrhenius, T_ref=25 °C 규약).
#      i0/R_ct · D_s · OCP dU/dT · σ_e · κ · SE 경도 H/σ_y 는 앵커가 없어(§F1) 25 °C 상수로
#      남는다 → **전-물리 온도 스윕이 아니다**.  UI 경고( #kit-op-warn )가 이 사실을 화면에 적는다.
def _se_material():
    """scripts/se_material.py (σ_grain + 온도 규약 단일 출처) 지연 임포트."""
    import sys as _s
    _sd = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts')
    if _sd not in _s.path:
        _s.path.insert(0, _sd)
    import se_material
    return se_material


def _sigma_grain_mS_cm(metrics=None):
    """σ_grain [mS/cm] — 이 파일에서 파생량(σ_Bruggeman, τ_Laplace)을 만들 때 쓰는 단 하나의 값.

    ★ 2026-07-28 적대검증(담당 C-1) 수정: 이 파일에는 bare `3.0` 이 7곳 박혀 있었다
    (`σ_brug = 3.0 × sigma_ratio` ×3, `SIGMA_GRAIN_MS = 3.0` ×2, MD 리포트 ×2 — 검증이 지목한
    `:2418`/`:2550` 은 그중 둘이고, **7곳 전부가 살아있는 Flask 요청 경로**다).  즉
    `se_material.py` 가 자기 헤더에서 주장하는 "SINGLE SOURCE OF TRUTH" 가 webapp 에서는
    성립하지 않았다.  이제 전부 이 함수를 통한다 (잔존 범위는 docs §9-2 인벤토리 참조).

    ★ 온도 정합이 핵심이다.  τ_Lap_eff = √(φ_SE·σ_grain/σ_full) 은 σ_grain 과 σ_full 이 **같은
    온도**일 때만 옳다.  런이 `--temp-c` 로 풀렸다면 σ_full 은 Arrhenius 로 커져 있는데 여기서
    25 °C 상수 3.0 을 쓰면 τ 가 √factor 배 (60 °C 면 ×0.46) 만큼 **조용히 틀린다.**  그래서 런이
    남긴 provenance(= se_material.provenance) 의 `sigma_ion_T_factor` 를 그대로 따라간다.

    ★ 기본값 불변: T 를 안 준 런(=현존 전 코퍼스)은 provenance 가 없거나 factor 가 **정확히 1.0**
    이므로 `3.0 * 1.0` → bitwise 3.0.  `sigma_grain_S_cm` 폴백도 3.0e-3 이면 곱셈을 아예 하지 않고
    상수를 돌려준다(0.003*1000 = 3.0000000000000004 라 bitwise 가 깨지기 때문).
    """
    return _sigma_grain_context(metrics)[0]


def _sigma_grain_context(metrics=None):
    """(σ_grain [mS/cm], mixed_T_note|None) — 값과 "왜 이 값인가" 를 함께 돌려준다.

    ★ 2026-07-28 재검증(HIGH, e-follow-on) 수정: 위 C-1 중앙화가 두 provenance 키를
      **같은 것처럼** 취급했는데, 둘은 스케일한 σ 가 다르다.

        temperature_provenance          — network_conductivity.py / mpm_webapp_payload.py.
                                          `sigma_full_mScm` **자체**가 Arrhenius 로 스케일됨.
        stage_e_temperature_provenance  — run_network_full_corrections.py --temp-c.
                                          `sigma_full_mScm_stage_e` 만 스케일하고
                                          **베이스라인 `sigma_full_mScm` 은 25 °C 로 남긴다**
                                          (그 스크립트 selftest 가 "T 런도 베이스라인은 25 °C
                                          그대로" 를 명시적으로 검증한다).

      그런데 이 헬퍼의 **모든** 소비자(app.py:2402/2419/2536/2551/5311/8004)는 σ_grain 을
      `metrics['sigma_full_mScm']`(= 베이스라인)와 짝지어 나눈다:
          σ_brug/σ_ionic = σ_grain·ratio / σ_full        τ_Lap_eff = √(φ_SE·σ_grain/σ_full)
      따라서 Stage-E 키를 따라 분자만 ×4.44(60 °C) 하면 분모는 25 °C 그대로라 비율이 ×4.44,
      τ 가 ×2.1 로 **조용히 틀린다** — 이 함수가 막으려던 바로 그 오류를 반대 방향으로
      새로 만든 셈이다.  ⇒ 짝이 맞는 `temperature_provenance` 만 따르고, Stage-E-only 런은
      25 °C 상수를 쓴 뒤(= 25 °C 베이스라인과 정확히 짝이 맞음) 혼합상태를 note 로 노출한다.

    ★ 기본값 불변: 온도 키가 없는 런(=현존 전 코퍼스)은 bitwise 3.0, note=None.
    """
    base = _se_material().SIGMA_GRAIN_MS_CM_25C
    if not isinstance(metrics, dict):
        return base, None

    def _fac(key):
        prov = metrics.get(key)
        if isinstance(prov, dict):
            f = prov.get('sigma_ion_T_factor')
            if isinstance(f, (int, float)) and not isinstance(f, bool) and f > 0:
                return float(f)
        return None

    # ★ S-4 (2026-07-29 적대리뷰 CONFIRMED): `is not None` 은 **존재**를 짝맞음으로 오판한다.
    #   network_conductivity.py:1106 은 `temperature_provenance` 를 factor 1.0 이어도 **무조건**
    #   발행하므로, 실제 프로덕션 산출물은 거의 항상 {1.0 인 paired 키} + {60 °C 인 Stage-E 키}
    #   형태다.  옛 코드는 그 조합에서 paired 를 "있다"고 보고 `(3.0, None)` 을 돌려줘 → 아래
    #   혼합-온도 경고 분기가 **실재하는 유일한 조합에서 절대 실행되지 않았다**.  값(3.0)은 25 °C
    #   베이스라인과 짝이 맞아 옳으므로 어떤 수치 검증에도 안 걸렸다 — 잃는 건 경고뿐이었다.
    #   ⇒ 판정을 "존재" 가 아니라 **배수가 실제로 1 이 아닌가** 로 바꾼다.
    f_paired = _fac('temperature_provenance')          # σ_full 이 같이 움직인 경우만
    if f_paired is not None and abs(f_paired - 1.0) > 1e-12:
        return base * f_paired, None                   # 짝맞는 T 런 → 그대로 스케일

    f_stage_e = _fac('stage_e_temperature_provenance')
    if f_stage_e is not None and abs(f_stage_e - 1.0) > 1e-12:
        # (paired 키가 1.0 으로 함께 있어도 여기 도달한다 — S-4 수정의 요점)
        prov = metrics['stage_e_temperature_provenance']
        t_c = prov.get('T_C', prov.get('temp_C'))
        return base, (
            f'⚠ 혼합 온도: 이 런은 Stage-E σ_ion 만 {t_c if t_c is not None else "?"} °C 로 '
            f'스케일(×{f_stage_e:.3g})했고 베이스라인 σ_full 은 25 °C 입니다.  σ_brug·τ_Laplace 는 '
            f'그 25 °C 베이스라인과 짝을 맞추려고 σ_grain = {base:g} mS/cm(25 °C)를 씁니다 — '
            f'Stage-E 값과 직접 비교하지 마세요.')

    s_cm = metrics.get('sigma_grain_S_cm')
    if isinstance(s_cm, (int, float)) and not isinstance(s_cm, bool) and s_cm > 0:
        if float(s_cm) == _se_material().SIGMA_GRAIN_S_CM_25C:
            return base, None              # bitwise-safe (0.003*1000 ≠ 3.0)
        return float(s_cm) * 1000.0, None
    return base, None


# 킷 run_mpm.sh 안의 STEP3(σ) 호출 = 온도를 주입할 유일한 지점.  생성기(scripts/mpm_input_from_case.py)
# 는 다른 에이전트 담당이라 --temp-c 인자를 갖지 않으므로, webapp 이 생성 직후 이 한 줄에 플래그를
# 덧붙인다.  마커가 정확히 1회가 아니면 **조용히 무시하지 않고 500 으로 실패**한다 (침묵 no-op 금지).
_KIT_STEP3_CALL = 'python3 "$SCR/mpm_webapp_payload.py" \\\n'


def _kit_apply_temperature(tmp, t_c, ea_ev):
    """킷에 운전 온도를 굽는다 — run_mpm.sh 의 STEP3 σ 호출에 --temp-c/--ea-ion-ev 를 주입하고
    mpm_input.json 에 temperature_provenance 를 남긴다.  실패 시 RuntimeError (호출부가 500)."""
    se_material = _se_material()
    rp = os.path.join(tmp, 'run_mpm.sh')
    if not os.path.exists(rp):
        raise RuntimeError('run_mpm.sh 없음 — 킷 생성기 산출물 구조가 바뀜')
    src = open(rp).read()
    if src.count(_KIT_STEP3_CALL) != 1:
        raise RuntimeError('run_mpm.sh 의 STEP3(payload) 호출 마커를 찾지 못함 — 생성기가 바뀌었으니 '
                           'webapp/app.py _KIT_STEP3_CALL 을 갱신해야 한다 (온도 주입 침묵실패 방지)')
    flags = f' --temp-c {t_c:g}' + (f' --ea-ion-ev {ea_ev:g}' if ea_ev is not None else '')
    note = (f'# ★ 운전 온도 {t_c:g} °C (webapp &tempc=) — σ_ion(SE) 은 Kraft-2017 σ·T Arrhenius,\n'
            f'#   i0 는 kim2025 R_ct(T) 앵커로 스케일 (STEP4 에 --temp-k {t_c + 273.15:g} '
            f'--i0-temp-scale 을 **한 쌍으로** 주입 — 한쪽만 주면 부호역전/거짓라벨).\n'
            f'#   D_s/OCP dU/dT/σ_e/κ/SE-경도는 앵커 없어 25 °C 상수 → 전-물리 온도 스윕 아님 '
            f'(docs/temp_pressure_capability.md §3).  Eₐ 는 밴드 0.29/0.41/0.46 eV 를 쓸어 보고할 것.\n')
    src = src.replace(
        _KIT_STEP3_CALL, note + _KIT_STEP3_CALL.replace(' \\\n', flags + ' \\\n'))
    # ── ★ 2026-07-29: STEP4 에도 온도를 굽는다 ──────────────────────────────────────────────
    #   이전에는 STEP3(σ 그리드)에만 --temp-c 를 넣었다.  그러면 그리드는 60 °C σ_ion 인데
    #   step4_dyn 은 기본 --temp-k 298.15 로 돌아가고, T1-d 가드가 GRID_T_MISMATCH 로
    #   **첫 STEP4 스텝에서 hard-fail** 한다 (실제 킷으로 재현 확인).  가드는 옳다 — 60 °C σ 위에서
    #   25 °C 반응속도를 돌리면 조용히 틀리니까.  틀린 건 킷이 그 짝을 안 맞춰준 것이었다.
    #   ⚠ (옛 주석 정정 2026-07-30) i0 는 앵커가 **있다** — kim2025 R_ct(T).  D_s/OCP 만 미앵커라
    #     이 런은 **"σ_ion 만 60 °C" 인 혼합 상태**다.  플래그는 그 사실을 승인하는 것이고,
    #     산출물에는 PARTIAL_sigma_ion_only@<T>C 로 박힌다 — 전-물리 온도 스윕이 아니다.
    _S4_CALL = 'python3 "$SCR/step4_dyn.py" --grid step4_grid.npz \\\n'
    _n_s4 = src.count(_S4_CALL)
    import sys as _s3
    _sd3 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts')
    if _sd3 not in _s3.path:
        _s3.path.insert(0, _sd3)
    import cam_kinetics as _ck
    _i0f = _ck.i0_temperature_factor(t_c, ea_ev if ea_ev else None)
    if _n_s4:
        # ★★ 규약 이력 (중요 — 되돌리지 말 것) ★★
        #   [옛 규약] --temp-k 를 **굽지 않았다** (§3-3① 부호역전).  Kinetics.T 는 BV 지수의
        #     f=F/(RT) 를 바꾸는데 i0 가 25 °C 상수로 남으면 T 를 올릴수록 같은 전류에 필요한
        #     η_ct 가 **커진다** — 실제 R_ct 는 30→60 °C 에 4.28× **감소**하므로 정확히 반대다.
        #     "온도를 반영했다는 인상을 주면서 반대 답을 내는 것" 이 가장 나쁜 실패라, 킷은
        #     kinetics 를 25 °C 로 두고 그리드 불일치만 --allow-grid-t-mismatch 로 승인했다.
        #   [HIGH-4, 2026-07-30] 그 결과 프로덕션 경로엔 i0(T) 가 아예 없었다 → --i0-temp-scale 추가.
        #   [자체검증 정정, 2026-07-30] ★그 수정이 반쪽이었다★ — --i0-temp-scale 은 **--temp-k 를
        #     읽어** 배수를 만든다.  --temp-k 를 기본(298.15 K)으로 둔 채 플래그만 주면 배수는
        #     **정확히 1.0** 인데 배너·provenance 는 ×6.25 를 광고하고 npz 엔
        #     kinetics_T_scaling=I0_ARRHENIUS_kim2025 가 찍힌다 = 새 거짓 진술.
        #   ⇒ **i0 앵커가 생긴 지금은 --temp-k 를 굽는 것이 옳다.**  옛 금지 사유(부호역전)는
        #     i0 가 미앵커일 때만 성립했고, --i0-temp-scale 과 **함께** 주면 부호역전이 해소된다
        #     (step4_dyn selftest A5: η_ct 60 °C 93.4 → 26.6 mV).  두 플래그는 **한 쌍**이다.
        #   ⇒ --allow-grid-t-mismatch 는 **뺀다**: σ_ion 도 kinetics 도 같은 t_c 라 혼합이 아니다.
        #     남겨두면 STEP3 가 --temp-c 를 못 구운 경우의 진짜 불일치까지 조용히 통과시킨다.
        src = src.replace(_S4_CALL,
                          _S4_CALL + f'    --temp-k {t_c + 273.15:g} --i0-temp-scale \\\n')
        src = src.replace('echo "[run_mpm] STEP4 솔버:',
                          f'echo "[run_mpm] ★ STEP4 온도: σ_ion = 그리드의 {t_c:g} °C · '
                          f'i0 = kim2025 R_ct(T) 앵커로 스케일(--temp-k {t_c + 273.15:g} '
                          f'--i0-temp-scale, x{_i0f:.3f}) · BV 열전압 f=F/RT 도 {t_c:g} °C. '
                          f'D_s/OCP dU/dT/sigma_e/kappa 는 앵커 없어 25 °C 상수 = PARTIAL. '
                          f'--temp-k 는 --i0-temp-scale 과 **한 쌍**이다 — 단독으로 주면 '
                          f'부호역전(§3-3①). 코팅계는 Ea 가 다름(kim2025 LNO 비-Arrhenius)"\n'
                          f'echo "[run_mpm] STEP4 솔버:', 1)
    open(rp, 'w').write(src)
    pj = os.path.join(tmp, 'mpm_input.json')
    if not os.path.exists(pj):
        raise RuntimeError('mpm_input.json 없음 — provenance 를 남길 수 없음')
    prov = json.load(open(pj))
    tp = se_material.provenance(t_c, ea_ev)
    tp['applied_to'] = ['run_mpm.sh: mpm_webapp_payload.py --temp-c '
                        '(STEP3 σ_ion 복셀 솔브 + step4_grid.npz σ 테이블)',
                        f'run_mpm.sh: step4_dyn.py --temp-k {t_c + 273.15:g} --i0-temp-scale '
                        f'({_n_s4} 개 STEP4 호출) — σ_ion 은 그리드의 {t_c:g} °C, '
                        f'i0 는 kim2025 R_ct(T) 앵커로 ×{_i0f:.4f} (RT 전인자 포함), '
                        f'BV 열전압 f=F/RT 도 {t_c:g} °C.  ★두 플래그는 **한 쌍**이다: '
                        f'--temp-k 단독 = 부호역전(§3-3①), --i0-temp-scale 단독 = 배수 1.0 인데 '
                        f'kinetics_T_scaling 만 찍히는 거짓 라벨.  '
                        f'⚠코팅계 Eₐ 는 다름(kim2025 LNO 비-Arrhenius — 앵커는 uncoated)']
    tp['not_applied_to'] = {
        'STEP1/2 MPM 압밀': 'SE 경도 H(T)/σ_y(T) 앵커 없음 (§F1) → 형상은 25 °C 값',
        'STEP4 kinetics (D_s/OCP만)': 'D_s(T) / OCP dU/dT 앵커 없음 (§F1) → 25 °C 상수.  '
                        '★i0 와 BV 열전압은 예외 — kim2025 R_ct(T) 앵커가 있어 '
                        '--temp-k + --i0-temp-scale 한 쌍으로 반영된다 '
                        '(i0 앵커가 생기기 전에는 --temp-k 를 굽지 않았다: f=F/RT 만 움직이면 '
                        '반응 과전압 부호가 실험과 반대, §3-3①)',
        'σ_e / κ': 'ohmic 은 T-무관 (Reisacher, 정성) — 상수가 오히려 정합',
        'STEP5 열화율': 'Arrhenius 앵커 0건 (§F1) — Joule v2 는 Eₐ-free 유지',
    }
    tp['injected_by'] = 'webapp/app.py mpm_input_package (&tempc=)'
    prov['temperature_provenance'] = tp
    json.dump(prov, open(pj, 'w'), indent=2)
    return tp


@app.route('/results/<case_id>/mpm-input')
def mpm_input_package(case_id):
    """[MPM input 변환]: build the per-case MPM input (am/se scaffolds + run_mpm.sh +
    provenance) from the case's atoms.csv and return it as a zip to run on a GPU box."""
    import subprocess
    import tempfile
    import zipfile
    import io
    import shutil
    results_dir = get_results_dir(case_id)
    if not os.path.exists(os.path.join(results_dir, 'atoms.csv')):
        return jsonify({'error': 'no atoms.csv for this case'}), 404
    repo = os.path.dirname(os.path.dirname(__file__))
    gen = os.path.join(repo, 'scripts', 'mpm_input_from_case.py')
    tmp = tempfile.mkdtemp()
    # the case's type map decides which atom type is SE (NOT always type 3)
    tmap = ''
    meta_p = os.path.join(get_case_dir(case_id), 'meta.json')
    if os.path.exists(meta_p):
        try:
            tmap = (json.load(open(meta_p)) or {}).get('type_map', '')
        except Exception:
            tmap = ''
    cmd = ['python3', gen, '--results', results_dir, '--case', case_id, '--out', tmp]
    if tmap:
        cmd += ['--type-map', tmap]
    # optional conductive-additive recipe baked into run_mpm.sh (첨가제 적용 section)
    def _addf(name):
        try:
            return max(0.0, min(10.0, float(request.args.get(name, 0.0))))
        except ValueError:
            return 0.0
    _vg, _sp, _pt, _sd = _addf('vgcf'), _addf('superp'), _addf('ptfe'), _addf('sdcp')
    # VGCF + Super P are both conductive carbon → mutually exclusive.
    if _vg > 0 and _sp > 0:
        shutil.rmtree(tmp, ignore_errors=True)
        return jsonify({'error': 'VGCF와 Super P는 함께 사용 불가 — 도전재는 하나만 '
                                 '(VGCF/Super P/PTFE/VGCF+PTFE/Super P+PTFE)'}), 400
    recipe = _add_recipe_str(_vg, _sp, _pt, _sd)
    mixing = request.args.get('mixing', 'thinky')
    if mixing not in ('ballmill', 'thinky', 'handmix'):
        mixing = 'thinky'
    if recipe:
        cmd += ['--add-recipe', recipe, '--mixing', mixing]
    # STEP3 collector selection.  R_int is an (ELECTRODE, collector) PAIR property — the Fig6e
    # anchors are (SBE,bare)=110 / (DBE,bare)=46 / (DBE,C-SUS)=30 Ω·cm² (post-cycling).  The UI
    # picks only the COLLECTOR; the electrode side is what the recipe already is (SDCP in the
    # recipe = DBE-class bottom interface).  (SBE,C-SUS) was not measured → DBE-anchored proxy,
    # labelled.  Every preset is still computed; this tags metrics.step3.collector.selected.
    _coll = request.args.get('collector', '')
    _dbe = _sd > 0                                       # recipe contains SDCP → DBE-class electrode
    _scn = ''                                            # anchors CSV scenario key (단일 출처)
    if _coll == 'bare':
        _scn = 'dbe' if _dbe else 'sbe'
        _rint = _rint_anchor_pair(_scn)[1]               # cycled (aged 민감도 — payload가 pristine 병기)
        _cname = 'bare_Al+DBE_electrode' if _dbe else 'bare_Al+SBE_electrode'
    elif _coll == 'csus':
        _scn = 'csus'
        _rint = _rint_anchor_pair('csus')[1]
        _cname = 'C-SUS_primer+DBE' if _dbe else 'C-SUS_primer+SBE(proxy_DBE-anchored)'
    elif _coll == 'sus':                                 # bare SUS (무코팅) — 추정 reference (미측정)
        _scn = 'sus'
        _rint = _rint_anchor_pair('sus')[1]              # cycled 추정 60 (pristine 20 병기); 밴드 CSV note
        _cname = 'SUS_bare_estimated'                    # shell-safe token (no space/paren)
    elif _coll == 'ideal':
        _rint, _cname = 0.0, 'ideal'
    else:
        _rint, _cname = -1.0, ''
    if _rint >= 0.0:
        cmd += ['--collector-rint', str(_rint), '--collector-name', _cname]
        if _scn:
            cmd += ['--collector-scenario', _scn]
    # STEP3 voxel resolution (µm).  ONLY the σ solve grid — NOT the MPM compaction (n_grid) nor the
    # porosity/thickness/coverage/econn (those are unchanged by vox).  Finer = neck/SDCP-channel detail
    # for the current-density FIELD figure; σ_e/σ_ion/R_geom can shift slightly (finite-volume grid
    # dependence).  Whitelisted so the UI can't request a runaway dof (∝1/vox³).
    _vox = request.args.get('vox', '0.4')
    if _vox not in ('0.4', '0.25', '0.2'):
        _vox = '0.4'
    cmd += ['--step3-vox', _vox]
    # ── ★ 운전조건 (미지정 = 현행, 방출물 바이트 동일) ─────────────────────────────────────
    #   &tempc= 운전 온도 [°C]  → 킷 STEP3 σ 호출에 --temp-c 주입 (아래 subprocess 성공 후)
    #   &eaion= 이온 Eₐ [eV]    → 밴드 스윕용 (0.29/0.41/0.46); 온도 없이 단독 지정은 무의미 → 400
    #   &pop=   구동 스택압 [MPa] → 생성기 --op-pressure-mpa (A-1 앵커를 2단 제작→구동으로)
    def _opnum(name, lo, hi, unit):
        _raw = (request.args.get(name, '') or '').strip()
        if not _raw:
            return None, None
        try:
            _v = float(_raw)
        except (ValueError, TypeError):
            return None, f'&{name}= 값이 숫자가 아님: {_raw!r}'
        if not (lo <= _v <= hi):
            return None, f'&{name}= 는 {lo:g}~{hi:g} {unit} 범위여야 함 (got {_v:g})'
        return _v, None
    _tempc, _te1 = _opnum('tempc', -20.0, 200.0, '°C')
    _eaion, _te2 = _opnum('eaion', 0.10, 1.00, 'eV')
    _oppress, _te3 = _opnum('pop', 0.1, 2000.0, 'MPa')
    _terr = next((e for e in (_te1, _te2, _te3) if e), None)
    if _terr is None and _eaion is not None and _tempc is None:
        _terr = '&eaion= (이온 Eₐ) 는 &tempc= 와 함께만 의미가 있음 — 온도를 먼저 지정하세요'
    if _terr:
        shutil.rmtree(tmp, ignore_errors=True)
        return jsonify({'error': _terr}), 400
    if _oppress is not None:
        cmd += ['--op-pressure-mpa', f'{_oppress:g}']
    # STEP4 체크박스 (중복 선택 가능): &step4=0.5,1 → run_mpm.sh가 payload 후 각 rate를
    # 순차 자동 실행 (미선택 = step4_grid.npz export까지만 — 나중에 step4_only.sh로 재개).
    def _rates_of(name):
        out = []
        for _tok in request.args.get(name, '').split(','):
            _tok = _tok.strip()
            if _tok:
                try:
                    _v = float(_tok)
                    if 0.02 <= _v <= 5.0 and _v not in out:
                        out.append(_v)
                except ValueError:
                    pass
        return out
    _s4_clean = _rates_of('step4')
    _s4chg_clean = _rates_of('step4chg')                # 충전(CCCV) 체크박스
    # ★Zive 스케줄 (&s4sched=JSON) — 지정 시 crates/charge 대신 순서대로 실행 (charge-first, per-step 컷오프).
    #   crates/charge 체크박스와 동시 지정 시 스케줄 우선 (kit이 s4_sched 있으면 그걸로 시퀀스 생성).
    _s4sched = request.args.get('s4sched', '')
    if _s4sched:
        import json as _json
        try:
            _sj = _json.loads(_s4sched)
            if isinstance(_sj, list) and _sj:
                cmd += ['--step4-sched', _json.dumps(_sj, separators=(',', ':'), ensure_ascii=True)]
            else:
                _s4sched = ''
        except Exception:
            _s4sched = ''                               # 파싱 실패 → 스케줄 무시 (체크박스 경로 유지)
    # ★STEP4 grid까지만 (&s4grid=1): step4_grid.npz 만 만들고 step4_dyn(v2) 스킵 — C-rate/충전/스케줄 무시
    _s4grid = request.args.get('s4grid', '') in ('1', 'true', 'yes', 'on')
    if _s4grid:
        cmd.append('--step4-grid-only')
        _s4_clean, _s4chg_clean, _s4sched = [], [], ''       # 아래 컷오프/R_int 주입 게이트도 함께 끔
    # ★s4cap 은 게이트 밖에서 먼저 읽는다 — 옛 구조는 STEP4 미선택 + cap 셀렉트 조합에서 태그 블록의
    #   _s4cap 참조가 NameError 500 (코드리뷰 chain#10, 기존 버그).  cmd 주입은 여전히 게이트 안.
    _s4cap = request.args.get('s4cap', '')
    if _s4_clean and not _s4sched:
        cmd += ['--step4-crates', ','.join(f'{v:g}' for v in _s4_clean)]
    if _s4chg_clean and not _s4sched:
        cmd += ['--step4-charge', ','.join(f'{v:g}' for v in _s4chg_clean)]

    def _cut(name, default, lo, hi):                    # 컷오프 스케줄 (화이트리스트 클램프)
        try:
            v = float(request.args.get(name, default))
            return min(max(v, lo), hi)
        except ValueError:
            return default
    if _s4_clean or _s4chg_clean or _s4sched:           # 컷오프·R_int·poly/SC는 STEP4 선택(또는 스케줄) 시 주입
        _vmin = _cut('s4vmin', 3.0, 1.5, 4.0)
        _vmax = _cut('s4vmax', 4.5, 3.5, 4.8)
        _icut = _cut('s4icut', 0.05, 0.01, 2.0)   # 절대 C (충전 rate와 독립) — 고율 충전의 '절반 종지' 허용 위해 2.0까지
        cmd += ['--step4-vmin', f'{_vmin:g}', '--step4-vmax', f'{_vmax:g}', '--step4-icut', f'{_icut:g}']
        # 방전끝 x100: UI 필드 제거됨 → 기본은 킷 생성기(mpm_input_from_case --step4-x100)의
        # 0.9084(NMC811 vs-Li GITT 실측 방전끝).  URL에 &s4x100= 를 주면 그때만 오버라이드(파워유저용).
        _x100 = request.args.get('s4x100', '')
        if _x100:
            try:
                cmd += ['--step4-x100', f'{max(0.85, min(0.99, float(_x100))):g}']
            except (ValueError, TypeError):
                pass
        # ★풀셀 축 (A11/R_int Phase 1): &s4rint= → STEP4 직렬 R_int.  기본 없음 = 전극-내부 R_int=0.
        #   숫자(Ω·cm²) 또는 키워드 'pristine'/'cycled' — 키워드는 선택된 collector+전극(SBE/DBE)에
        #   맞는 시나리오 값을 정본 anchors CSV에서 자동 해석 (예: &collector=bare + SDCP 레시피 +
        #   &s4rint=pristine → DBE bare-Al pristine 12).  collector 미선택 시 키워드는 무시(어느
        #   시나리오인지 모호 — 침묵 기본값 금지).  음수/비수치는 무시.
        _s4r = request.args.get('s4rint', '')
        if _s4r in ('pristine', 'cycled'):
            if _scn:
                _pr_v, _cy_v = _rint_anchor_pair(_scn)
                cmd += ['--step4-r-int', f'{(_pr_v if _s4r == "pristine" else _cy_v):g}']
        elif _s4r:
            try:
                _s4rv = float(_s4r)
                if _s4rv >= 0.0:
                    cmd += ['--step4-r-int', f'{_s4rv:g}']
            except (ValueError, TypeError):
                pass
        # ★STEP4 솔버 σ-대비 cap (&s4cap=) — near-null 수렴정체 완화 (docs/step4_bottleneck_analysis_20260727).
        #   화이트리스트만 허용(임의값 금지): 0=OFF 기본 · 200 권장(CG ×5.2, σ_eff −7.8%) · 1000/2000=보수적.
        #   킷은 이 값을 MPM_S4_CONTRAST_CAP 기본값으로 굽고, 런타임 env 가 다시 override 가능.
        if _s4cap in ('200', '1000', '2000'):
            cmd += ['--step4-solver-cap', _s4cap]
        # ★v2 chaining (&s4chain=1, 스케줄 전용) — 각 스텝이 직전 스텝 끝 셸-SOC에서 시작(연속
        #   사이클, Loop 반복도 상태 누적) + Rest 는 실제 I=0 완화 런.  미지정 = v1 독립런.
        if _s4sched and request.args.get('s4chain', '') in ('1', 'true', 'on'):
            cmd += ['--step4-chain']
        # ★bimodal poly/SC 전기화학 분리 (파워유저 URL, s4x100 문법): &s4dsp=&s4dss= (D_s [m²/s])
        #   &s4i0p=&s4i0s= (i0 [A/m²]) &s4split= (반경 문턱 µm, 기본 3.5).  반쪽 지정은 400으로
        #   명시 거부(생성기 ap.error를 500 stderr로 흘리지 않고 앞단에서 — 침묵/불명확 실패 금지).
        #   값 가이드: docs/ncm_sc_poly_electrochem_anchors.md (i0 분리값은 문헌 부재 — 스윕 전용).
        def _fpos(name):
            _t = request.args.get(name, '').strip()
            if not _t:
                return None, None
            try:
                _v = float(_t)
            except (ValueError, TypeError):
                return None, f'&{name}= 값이 숫자가 아님: {_t!r}'
            return (_v, None) if _v > 0 else (None, f'&{name}= 는 > 0 이어야 함: {_t}')
        _dsp, _e1 = _fpos('s4dsp'); _dss, _e2 = _fpos('s4dss')
        _i0p, _e3 = _fpos('s4i0p'); _i0s, _e4 = _fpos('s4i0s')
        _spl, _e5 = _fpos('s4split')
        _err = next((e for e in (_e1, _e2, _e3, _e4, _e5) if e), None)
        if _err:
            shutil.rmtree(tmp, ignore_errors=True)
            return jsonify({'error': _err}), 400
        if (_dsp is None) != (_dss is None) or (_i0p is None) != (_i0s is None):
            shutil.rmtree(tmp, ignore_errors=True)
            return jsonify({'error': 's4dsp/s4dss (또는 s4i0p/s4i0s)는 쌍으로만 — 반쪽 지정 거부'}), 400
        if _dsp is not None:
            cmd += ['--step4-ds-poly', f'{_dsp:g}', '--step4-ds-sc', f'{_dss:g}']
        if _i0p is not None:
            cmd += ['--step4-i0-poly', f'{_i0p:g}', '--step4-i0-sc', f'{_i0s:g}']
        if _spl is not None and (_dsp is not None or _i0p is not None):
            cmd += ['--step4-am-split-um', f'{_spl:g}']
        # ★문헌 프리셋 (&s4pp=1, UI 체크박스): 정본 docs/data/sc_poly_preset.csv를 생성기가 해석
        #   (D_s poly 4e-15 Chen2020 / SC 3e-15 Trevisanello 밴드 기하중앙; i0 분리 부재 확정 →
        #   공유).  명시 s4dsp와 동시 지정은 생성기가 모호-거부 → 여기서도 앞단 400.
        if request.args.get('s4pp', '') in ('1', 'true', 'on'):
            if _dsp is not None or _i0p is not None:
                shutil.rmtree(tmp, ignore_errors=True)
                return jsonify({'error': 's4pp(프리셋)와 명시 s4dsp/s4i0p 동시 지정 불가 — 하나만'}), 400
            cmd += ['--step4-sc-poly-preset']
    try:
        subprocess.run(cmd, check=True, cwd=repo, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        shutil.rmtree(tmp, ignore_errors=True)
        return jsonify({'error': 'generation failed', 'detail': (e.stderr or '')[-500:]}), 500
    if _tempc is not None:                              # 생성 직후 온도 주입 (미지정이면 이 줄도 안 탄다)
        try:
            _kit_apply_temperature(tmp, _tempc, _eaion)
        except Exception as e:                          # 침묵 no-op 금지 — 온도가 안 구워졌으면 킷을 주지 않는다
            shutil.rmtree(tmp, ignore_errors=True)
            return jsonify({'error': f'온도 배선 실패 — 킷을 만들지 않았습니다: {e}'}), 500
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(tmp)):
            z.write(os.path.join(tmp, fn), fn)
    shutil.rmtree(tmp, ignore_errors=True)
    buf.seek(0)
    # filename carries BOTH the recipe and the mixing, so a thinky vs ball-mill zip
    # of the same recipe are distinct files (mixing changes the baked run_mpm.sh).
    # zip 이름 = [A-Za-z0-9._] 만 사용 (자기서술형 재료+값 쌍).  ':'/'-' 구분자는 사용자
    # 환경(브라우저/OS 다운로드 새니타이즈)에서 삭제돼 JS 예측명과 실제 파일명이 계속
    # 어긋났음 (예: VGCF-PTFE-SDCP_2.97-0.495-0.495 → VGCFPTFESDCP_2.970.4950.495).
    _pairs = [('VGCF', _vg), ('SuperP', _sp), ('PTFE', _pt), ('SDCP', _sd)]
    tag = (('_' + '_'.join(f'{k}{v:g}' for k, v in _pairs if v > 0) + '_' + mixing)
           if recipe else '')
    if recipe and _vox != '0.4':                        # finer STEP3 vox → carried into the zip/name
        tag += '_vox' + _vox
    # ★스케줄 지정 시 체크박스 rate 는 킷에 안 들어가므로(위 게이트) 태그에서도 뺀다 —
    #   안 그러면 zip 이름은 '_s40.2C' 인데 내용은 스케줄이라 서로 어긋난다 (감사 L10).
    if _s4sched:
        _s4_clean = _s4chg_clean = []
    if _s4_clean:                                       # STEP4 선택 → zip 이름에 rate 표기
        tag += '_s4' + '_'.join(f'{v:g}C' for v in _s4_clean)
    if _s4chg_clean:
        tag += '_s4chg' + '_'.join(f'{v:g}C' for v in _s4chg_clean)
    if _s4sched:
        tag += '_sched'
        # ★체인 킷은 실행 의미가 다름(연속 사이클) → 독립런 킷과 파일명 구별 (cap 태그와 같은 규약)
        if request.args.get('s4chain', '') in ('1', 'true', 'on'):
            tag += '_chain'
    # ★솔버 cap 은 σ_eff 를 −7.8% 바꾸는 노브 → 같은 이름의 두 킷이 생기지 않게 태그 (감사 M10)
    #   STEP4 솔브가 실제로 있을 때만 (grid-only/미선택 킷엔 cap 이 안 구워짐 → 태그도 없음)
    if _s4cap in ('200', '1000', '2000') and (_s4_clean or _s4chg_clean or _s4sched):
        tag += '_cap' + _s4cap
    # ★poly/SC 크기-분리 프리셋 → run_mpm.sh 가 달라짐(σ_e 재료분류+D_s) → 파일명도 구별.
    #   클라이언트 _addTag 의 '_ppds' 와 반드시 일치 (예전 _sched7step/VGCFPTFESDCP 어긋남 교훈).
    if recipe and request.args.get('s4pp', '') in ('1', 'true', 'on'):
        tag += '_ppds'
    # ★운전조건 태그 — 온도/구동압은 킷 내용을 바꾸는 노브라 같은 이름의 두 킷이 생기면 안 된다.
    #   클라이언트 _tpTag() 와 **정확히** 미러 (순서: _T…C → _Ea… → _op…MPa; VGCFPTFESDCP 사건 교훈).
    if _tempc is not None:
        tag += f'_T{_tempc:g}C' + (f'_Ea{_eaion:g}' if _eaion is not None else '')
    if _oppress is not None:
        tag += f'_op{_oppress:g}MPa'
    return send_file(buf, mimetype='application/zip', as_attachment=True,
                     download_name=f'mpm_input_{case_id}{tag}.zip')


@app.route('/results/<case_id>/mpm-upload', methods=['POST'])
def mpm_upload(case_id):
    """Ingest the MPM result (mpm_payload.json produced on the GPU box) back into the
    case → results/<case_id>/mpm_payload.json, activating the MPM viewer + compare."""
    results_dir = get_results_dir(case_id)
    f = request.files.get('payload')
    if not f:
        return jsonify({'error': 'no payload file (field "payload")'}), 400
    try:
        data = json.load(f.stream)
    except Exception as e:
        return jsonify({'error': f'not valid JSON: {e}'}), 400
    if data.get('kind') != 'mpm' or 'particles' not in data:
        return jsonify({'error': 'not an MPM payload (expected kind=mpm + particles)'}), 400
    with open(os.path.join(results_dir, 'mpm_payload.json'), 'w') as out:
        json.dump(data, out)
    m = data.get('mpm_metrics', {}) or {}
    # ★provenance 승계 — payload 최상위의 temperature_provenance(= se_material.provenance, T1-a)는
    #   mpm_metrics 안에 없다(payload 가 step3 하위와 최상위에만 적는다).  사이드카에 함께 실어야
    #   케이스 페이지 배지가 "이 런이 몇 °C 규약으로 풀렸는지"를 말할 수 있다 (없으면 조용히 25 °C 가정).
    if isinstance(data.get('temperature_provenance'), dict):
        m.setdefault('temperature_provenance', data['temperature_provenance'])
    # compact sidecar → the case page's MPM result table reads this, not the 16 MB payload
    with open(os.path.join(results_dir, 'mpm_metrics.json'), 'w') as mf:
        json.dump(m, mf)
    return jsonify({'ok': True, 'mpm_metrics': m,
                    'porosity_mpm_pct': m.get('porosity_mpm_pct'),
                    'coverage_AM_P_mpm_pct': m.get('coverage_AM_P_mpm_pct'),
                    'n_am': m.get('n_am'), 'se_surface_tris': m.get('se_surface_tris')})


# ── Standalone MPM / 도전재 payload viewer (independent of the DEM case list) ─────────────
#    Upload an mpm_payload.json, view it in 3D, and keep an accumulating saved list — so an MPM
#    result that isn't tied to a known DEM case can still be viewed and compared on its own.
def _mpm_lab_slug(s):
    # Sanitize to a filesystem-safe token.  NO length cap here: this ALSO runs on LOOKUP, where the
    # pid passed in is already "<name-slug>_<uuid6>".  The old [:60] truncation chopped the uuid off
    # for long names (the _vox0.2 name suffix pushed the pid past 60 chars → wrong folder → 404).
    # The length cap now lives at CREATION (upload), on the NAME part only, so the uuid always survives.
    # `.` 는 유지(예: VGCF2.97)하되 연속점 `..` 는 붕괴 → 경로 traversal(부모 디렉토리) 차단.
    return re.sub(r'\.{2,}', '_', re.sub(r'[^A-Za-z0-9_.-]+', '_', str(s or ''))).strip('_') or 'payload'


def _mpm_lab_list():
    root = app.config['MPM_LAB_FOLDER']
    out = []
    if not os.path.isdir(root):
        return out
    for name in os.listdir(root):
        mp = os.path.join(root, name, 'meta.json')
        if os.path.isfile(mp):
            try:
                m = json.load(open(mp))
                m['id'] = name
                out.append(m)
            except Exception:
                pass
    out.sort(key=lambda x: x.get('uploaded_at', ''), reverse=True)  # 순수 시간순(최신 위) — 즐겨찾기 상단고정 제거
    return out


@app.route('/mpm-lab')
def mpm_lab():
    return render_template('mpm_lab.html', items=_mpm_lab_list())


@app.route('/mpm-lab/fav/<pid>', methods=['POST'])
def mpm_lab_fav(pid):
    """★ 즐겨찾기 토글 — meta.json의 fav 불리언; 목록에서 fav 그룹이 상단 고정."""
    mp = os.path.join(app.config['MPM_LAB_FOLDER'], _mpm_lab_slug(pid), 'meta.json')
    if not os.path.isfile(mp):
        return jsonify({'ok': False, 'error': 'payload not found'}), 404
    try:
        m = json.load(open(mp))
        m['fav'] = not m.get('fav')
        with open(mp, 'w') as f:
            json.dump(m, f)
        return jsonify({'ok': True, 'fav': m['fav']})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500


@app.route('/mpm-lab/upload', methods=['POST'])
def mpm_lab_upload():
    f = request.files.get('payload')
    if not f:
        return jsonify({'ok': False, 'error': 'no payload file (field "payload")'}), 400
    try:
        data = json.load(f.stream)
    except Exception as e:
        return jsonify({'ok': False, 'error': f'JSON 파싱 실패: {e}'}), 400
    name = (request.form.get('name') or data.get('case') or 'payload').strip()
    # 등록 로직은 mpm_lab_register.register_local 한 곳 — CLI 훅(원격 결과회수)과 meta 공유.
    try:
        pid, _d, meta = mpm_lab_register.register_local(data, name, app.config['MPM_LAB_FOLDER'])
    except ValueError as e:      # non-mpm payload
        return jsonify({'ok': False, 'error': str(e)}), 400
    meta['id'] = pid
    return jsonify({'ok': True, 'item': meta})


@app.route('/mpm-lab/data/<pid>')
def mpm_lab_data(pid):
    d = os.path.join(app.config['MPM_LAB_FOLDER'], _mpm_lab_slug(pid))
    p = os.path.join(d, 'payload.json')
    if not os.path.isfile(p):
        return jsonify({'error': 'payload not found', 'kind': 'mpm', 'available': False}), 404
    with open(p) as fh:
        payload = json.load(fh)
    if request.args.get('state') == 'seed' and payload.get('seed_mesh_triangles'):
        payload['mesh_triangles'] = payload['seed_mesh_triangles']
    payload.pop('seed_mesh_triangles', None)
    return jsonify(payload)


def _mpm_lab_payload_or_none(pid):
    p = os.path.join(app.config['MPM_LAB_FOLDER'], _mpm_lab_slug(pid), 'payload.json')
    if not os.path.isfile(p):
        return None
    with open(p) as fh:
        return json.load(fh)


def _mech_bins(raw, default=14):
    """Sanitize the ?bins query for the mech-reaction routes — invalid / out-of-range
    (incl. 0 → ZeroDivisionError, negative → IndexError) falls back to the default."""
    try:
        b = int(raw) if raw is not None else default
    except (TypeError, ValueError):
        return default
    return b if 2 <= b <= 200 else default


@app.route('/mpm-lab/mech-reaction/<pid>.png')
def mpm_lab_mech_reaction_png(pid):
    """Server-render the mechanics(SE plastic strain / AM contact-coverage) ↔
    reaction(j_rxn) spatial correlation figure for a saved MPM payload.
    OBSERVATIONAL (no stress→reaction coupling); see scripts/mech_reaction_correlation.py."""
    import sys as _sys
    import io as _io
    _sd = os.path.join(os.path.dirname(__file__), '..', 'scripts')
    if _sd not in _sys.path:
        _sys.path.insert(0, _sd)
    payload = _mpm_lab_payload_or_none(pid)
    if payload is None:
        return ('payload not found', 404)
    _bins = _mech_bins(request.args.get('bins'))
    import matplotlib.pyplot as _plt
    fig = None
    try:
        from mech_reaction_correlation import render_figure
        fig = render_figure(payload, _bins)
        buf = _io.BytesIO()
        fig.savefig(buf, format='png', dpi=150)
    except Exception:
        import traceback
        traceback.print_exc()
        return ('mech-reaction render failed', 500)   # no internal string in body
    finally:
        if fig is not None:
            _plt.close(fig)                            # close on success AND error → no fig leak
    buf.seek(0)
    return send_file(buf, mimetype='image/png', as_attachment=False,
                     download_name=f'mech_reaction_{_mpm_lab_slug(pid)}.png')


@app.route('/mpm-lab/mech-reaction/<pid>.csv')
def mpm_lab_mech_reaction_csv(pid):
    import sys as _sys
    import io as _io
    import csv as _csv
    _sd = os.path.join(os.path.dirname(__file__), '..', 'scripts')
    if _sd not in _sys.path:
        _sys.path.insert(0, _sd)
    payload = _mpm_lab_payload_or_none(pid)
    if payload is None:
        return ('payload not found', 404)
    _bins = _mech_bins(request.args.get('bins'))
    try:
        from mech_reaction_correlation import to_csv_rows, compute
        d = compute(payload, _bins)          # compute ONCE at the requested bins;
        rows = to_csv_rows(payload, _bins)   # header stats + rows now share n_bins
    except Exception:
        import traceback
        traceback.print_exc()
        return ('mech-reaction compute failed', 500)
    buf = _io.StringIO()
    w = _csv.writer(buf)
    w.writerow(['# reaction<->mechanics spatial correlation (OBSERVATIONAL, no stress->reaction coupling)'])
    w.writerow([f'# z-profile jrxn-coverage={d["corr_jrxn_coverage"]} (raw, z-confounded)',
                f'jrxn-strain={d["corr_jrxn_strain"]} (co-location)'])
    w.writerow([f'# reaction~z={d["corr_jrxn_z"]} (ion-limited)',
                f'jrxn-coverage z-controlled={d["corr_jrxn_coverage_partial_z"]}',
                f'within-slice={d["corr_jrxn_coverage_within_slice"]} (GENUINE coverage link)'])
    w.writerows(rows)
    resp = make_response(buf.getvalue())
    resp.headers['Content-Type'] = 'text/csv; charset=utf-8'
    resp.headers['Content-Disposition'] = (
        f'attachment; filename="mech_reaction_{_mpm_lab_slug(pid)}.csv"')
    return resp


@app.route('/mpm-lab/st4/<pid>', methods=['GET', 'POST'])
def mpm_lab_st4(pid):
    """STEP4-v2 viz(step4_viz*.json)를 lab 엔트리에 저장/서빙 — 뷰어가 st4 모드 진입 시
    자동 로드(GET)하고, 피커로 처음 연 파일은 자동 저장(POST)돼 다음부터 수동 선택이
    필요 없다.  엔트리당 1개(최근 저장본)."""
    d = os.path.join(app.config['MPM_LAB_FOLDER'], _mpm_lab_slug(pid))
    p = os.path.join(d, 'st4_viz.json')
    if request.method == 'POST':
        if not os.path.isdir(d):
            return jsonify({'ok': False, 'error': 'entry not found'}), 404
        try:
            data = json.loads(request.get_data(as_text=True))
        except Exception as e:
            return jsonify({'ok': False, 'error': f'JSON 파싱 실패: {e}'}), 400
        if not isinstance(data, dict) or data.get('kind') != 'step4_viz':
            return jsonify({'ok': False, 'error': 'step4_viz 형식이 아님 (kind 확인)'}), 400
        with open(p, 'w') as fh:
            json.dump(data, fh)
        return jsonify({'ok': True, 'size_mb': round(os.path.getsize(p) / 1e6, 1)})
    if not os.path.isfile(p):
        return jsonify({'available': False,          # 200: "아직 저장 안 됨"은 정상 autoload 상태 (404면 브라우저 콘솔 노이즈)
                        'hint': '뷰어 st4 모드에서 📂로 한 번 열면 자동 저장됩니다'}), 200
    return send_file(p, mimetype='application/json')


@app.route('/mpm-lab/gif', methods=['POST'])
def mpm_lab_gif():
    """PNG 프레임 시퀀스(data URL 배열) → 애니메이션 GIF (Pillow).  st4 시간전개
    (3D geometry · 두께방향 프로파일)를 뷰어가 체크포인트별로 캡처해 보내면 여기서 묶어 반환."""
    import base64
    import io
    try:
        from PIL import Image
    except Exception as e:                                    # webapp venv에 Pillow 없을 때
        return jsonify({'ok': False, 'error': f'Pillow 미설치 ({e}) — 🎞 PNG 프레임으로 외부 조립하세요'}), 500
    data = request.get_json(force=True, silent=True) or {}
    frames_b64 = data.get('frames') or []
    fps = float(data.get('fps') or 2) or 2.0
    name = _mpm_lab_slug(data.get('name') or 'st4')
    if not frames_b64:
        return jsonify({'ok': False, 'error': '프레임 없음'}), 400
    imgs = []
    for fb in frames_b64:
        if ',' in fb:
            fb = fb.split(',', 1)[1]                          # "data:image/png;base64," 접두 제거
        im = Image.open(io.BytesIO(base64.b64decode(fb))).convert('RGBA')
        bg = Image.new('RGBA', im.size, (255, 255, 255, 255))    # 투명 배경 → 흰색 합성
        imgs.append(Image.alpha_composite(bg, im).convert('RGB'))
    sz = imgs[0].size                                        # GIF는 프레임 크기 동일 필요 → 첫 프레임에 맞춤
    imgs = [im if im.size == sz else im.resize(sz) for im in imgs]
    buf = io.BytesIO()
    dur = max(20, int(round(1000.0 / max(fps, 0.1))))        # ms/frame
    imgs[0].save(buf, format='GIF', save_all=True, append_images=imgs[1:],
                 duration=dur, loop=0, optimize=True, disposal=2)
    buf.seek(0)
    return send_file(buf, mimetype='image/gif', as_attachment=True,
                     download_name=f'{name}.gif')


@app.route('/mpm-lab/summary/<pid>')
def mpm_lab_summary(pid):
    """Metrics-only fetch for the 요약 button — returns just mpm_metrics (a few KB) so the
    summary doesn't ship the whole multi-MB payload.  Reads the dict cached in meta.json
    (new uploads); falls back to parsing payload.json once for older uploads."""
    d = os.path.join(app.config['MPM_LAB_FOLDER'], _mpm_lab_slug(pid))
    mp = os.path.join(d, 'meta.json')
    if not os.path.isfile(mp):
        return jsonify({'ok': False, 'error': 'not found'}), 404
    meta = json.load(open(mp))
    mm = meta.get('mpm_metrics')
    if mm is None:                                       # pre-cache upload → read it out of the payload once
        pp = os.path.join(d, 'payload.json')
        try:
            mm = (json.load(open(pp)).get('mpm_metrics') or {}) if os.path.isfile(pp) else {}
        except Exception:
            mm = {}
    return jsonify({'ok': True, 'name': meta.get('name', pid),
                    'case': meta.get('source_case', ''), 'mpm_metrics': mm})


@app.route('/mpm-lab/rename/<pid>', methods=['POST'])
def mpm_lab_rename(pid):
    mp = os.path.join(app.config['MPM_LAB_FOLDER'], _mpm_lab_slug(pid), 'meta.json')
    if not os.path.isfile(mp):
        return jsonify({'ok': False, 'error': 'not found'}), 404
    name = ((request.get_json(silent=True) or {}).get('name') if request.is_json
            else request.form.get('name')) or ''
    name = name.strip()
    if not name:
        return jsonify({'ok': False, 'error': 'empty name'}), 400
    m = json.load(open(mp))
    m['name'] = name
    with open(mp, 'w') as f:
        json.dump(m, f)
    return jsonify({'ok': True, 'name': name})


@app.route('/mpm-lab/delete/<pid>', methods=['POST'])
def mpm_lab_delete(pid):
    root = os.path.realpath(app.config['MPM_LAB_FOLDER'])
    d = os.path.realpath(os.path.join(root, _mpm_lab_slug(pid)))
    if os.path.isdir(d) and os.path.dirname(d) == root:     # stay inside the lab folder
        shutil.rmtree(d, ignore_errors=True)
        return jsonify({'ok': True})
    return jsonify({'ok': False, 'error': 'not found'}), 404


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

    # Vectorized build (iterrows is ~100x slower and dominates load time on
    # particulate cases with 10^5+ atoms).
    ids = df['id'].astype('int64').tolist()
    ts = df['type'].astype('int64').tolist()
    xs = (df['x'] * scale).round(2).tolist()
    ys = (df['y'] * scale).round(2).tolist()
    zs = (df['z'] * scale).round(2).tolist()
    rs = (df['radius'] * scale).round(2).tolist()
    _tname = {}
    particles = []
    for i in range(len(ids)):
        t = ts[i]
        nm = _tname.get(t)
        if nm is None:
            nm = type_map.get(t, f'T{t}'); _tname[t] = nm
        particles.append({'id': ids[i], 'type': nm,
                          'x': xs[i], 'y': ys[i], 'z': zs[i], 'r': rs[i]})

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
        'se_states': {}, 'tabor_stats': {}, 'all_se_ids_count': 0,
        'se_engagement': {},
        'cluster_meta': {}, 'cluster_id_per_se': {},
        'coverage_per_am': {},
        # Phase A1/A3/A4 — per-particle fracture aggregates + stress chain
        'particle_max_fpc': {}, 'particle_worst_stage': {},
        'particle_n_brittle': {}, 'particle_worst_partner_brittle': {},
        'particle_worst_pair_type': {},
        'am_p_skeleton': [], 'stress_chain_segments': [],
        # Phase A5+A6 — SE network diagnostics
        'se_percolating': [], 'se_articulation_points': [],
        'se_bottleneck_edges': [], 'se_dead_end_clusters': [],
        'se_n_percolating': 0,
        'se_bn_median_norm': 0, 'se_bn_threshold_norm': 0,
        'se_n_bn_below_threshold': 0,
    }
    try:
        import sys as _sys
        _scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
        if _scripts_dir not in _sys.path:
            _sys.path.insert(0, _scripts_dir)
        from viewer3d_data import (
            aggregate_particle_metrics, classify_clusters,
            build_cluster_id_map, build_coverage_map,
            compute_se_network_diagnostics,
        )
        # Build atoms_by_id from atoms.csv we already loaded.
        # Include x/y/z so compute_se_network_diagnostics can identify
        # bottom/top SE for percolation boundary.  LIGGGHTS dump always
        # carries these columns; default 0 only as defensive fallback.
        atoms_by_id = {int(r['id']): {
            'type':   int(r['type']),
            'radius': float(r['radius']),
            'x':      float(r['x']) if 'x' in df.columns else 0.0,
            'y':      float(r['y']) if 'y' in df.columns else 0.0,
            'z':      float(r['z']) if 'z' in df.columns else 0.0,
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
                    if cached.get('_contacts_mtime') == contacts_mtime and cached.get('_schema') == 11:
                        # Restore every cached key except metadata.  Some
                        # int-keyed dicts (stress_max, dr_max, se_engagement,
                        # particle_max_fpc, particle_n_brittle) need their
                        # JSON-string keys coerced back to int so the
                        # frontend's numeric-key lookups (`engagement[p.id]`)
                        # work.
                        _INT_KEYED = {
                            'stress_max', 'dr_max', 'se_engagement',
                            'particle_max_fpc', 'particle_n_brittle',
                            'particle_worst_stage',
                            'particle_worst_partner_brittle',
                            'particle_worst_pair_type',
                        }
                        for k, v in cached.items():
                            if k.startswith('_'):
                                continue
                            if k in _INT_KEYED and isinstance(v, dict):
                                aux[k] = {int(kk): vv for kk, vv in v.items()}
                            else:
                                aux[k] = v
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
                    aux['all_se_ids_count']   = agg.get('all_se_ids_count', 0)
                    aux['se_engagement']      = agg.get('se_engagement', {})
                    # Phase A1/A3/A4
                    aux['particle_max_fpc']         = agg.get('particle_max_fpc', {})
                    aux['particle_worst_stage']     = agg.get('particle_worst_stage', {})
                    aux['particle_n_brittle']       = agg.get('particle_n_brittle', {})
                    aux['particle_worst_partner_brittle'] = agg.get('particle_worst_partner_brittle', {})
                    aux['particle_worst_pair_type'] = agg.get('particle_worst_pair_type', {})
                    aux['am_p_skeleton']            = agg.get('am_p_skeleton', [])
                    aux['stress_chain_segments']    = agg.get('stress_chain_segments', [])

                    # Phase A5+A6 — SE network diagnostics (re-stream contacts;
                    # NetworkX-based, ~1-2 s for typical 60k SE-SE contacts).
                    try:
                        _plate_z_sim = box.get('z_max', 0) / max(scale, 1)
                        _se_diag = compute_se_network_diagnostics(
                            _stream_records(contacts_df), atoms_by_id,
                            type_map, plate_z=_plate_z_sim, scale=scale)
                        aux['se_percolating']           = _se_diag.get('percolating_se', [])
                        aux['se_articulation_points']   = _se_diag.get('articulation_points', [])
                        aux['se_bottleneck_edges']      = _se_diag.get('bottleneck_edges', [])
                        aux['se_dead_end_clusters']     = _se_diag.get('dead_end_clusters', [])
                        aux['se_n_percolating']         = _se_diag.get('n_percolating', 0)
                        aux['se_bn_median_norm']        = _se_diag.get('bn_median_norm', 0)
                        aux['se_bn_threshold_norm']     = _se_diag.get('bn_threshold_norm', 0)
                        aux['se_n_bn_below_threshold']  = _se_diag.get('n_bn_below_threshold', 0)
                        aux['se_n_perc_edges']          = _se_diag.get('n_perc_edges', 0)
                        print(f'  [3d-data aux] SE diag: '
                              f'{aux["se_n_percolating"]} percolating, '
                              f'{len(aux["se_articulation_points"])} cut-pts, '
                              f'{len(aux["se_bottleneck_edges"])} narrow edges, '
                              f'{len(aux["se_dead_end_clusters"])} dead-ends')
                    except Exception as _ediag:
                        print(f'  [3d-data aux] SE diag failed: {_ediag}')

                    # Write cache so subsequent page loads are instant.
                    try:
                        cache_blob = dict(aux)
                        cache_blob['_contacts_mtime'] = contacts_mtime; cache_blob['_schema'] = 11
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

    # Defensive: try jsonify the full response.  If anything (numpy
    # types, NaN, huge dict serialisation, etc.) blows up here we'd
    # silently return either a 500 with HTML body or a truncated JSON,
    # which on the frontend looks like "Unexpected end of JSON input"
    # with no clue why.  Explicit fallback returns at least the base
    # geometry so the user sees particles instead of a red error box.
    payload = {
        'particles': particles,
        'box': box,
        'percolation': percolation,
        'paths': paths,
        'clusters': clusters,
        'mesh_triangles': mesh_triangles,
        'atoms_only': atoms_only_mode,
        'aux': aux,
    }
    try:
        resp = jsonify(payload)
        # Force compute Content-Length so chunked-encoding doesn't
        # mask a truncation downstream.
        body = resp.get_data()
        print(f'  [3d-data] response: {len(body)/1e6:.2f} MB')
        return resp
    except (TypeError, ValueError) as _je:
        import traceback
        traceback.print_exc()
        print(f'  [3d-data] jsonify FAILED ({type(_je).__name__}: {_je}) — '
              f'returning base geometry only, aux dropped')
        # Strip aux and retry — if particles+box+clusters serialise,
        # the viewer can at least show shapes.
        payload['aux'] = {}
        payload['_aux_error'] = f'{type(_je).__name__}: {_je}'[:200]
        return jsonify(payload)
    except Exception as _je:
        import traceback
        traceback.print_exc()
        print(f'  [3d-data] CATASTROPHIC FAIL: {type(_je).__name__}: {_je}')
        return jsonify({'error': str(_je)[:300],
                         'particles': [], 'aux': {},
                         'box': box, 'atoms_only': True}), 200

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


@app.route('/porosity-corpus.csv')
def porosity_corpus_csv():
    """Walk EVERY uploaded case, read its JSONs, and stream one row per case
    as CSV: MPM porosity (mpm_metrics.json) + DEM porosity (full_metrics) +
    composition (AM:SE) + P:S + radii + the SE-rich/SE-poor/cross-validated
    regime gate (gap = DEM - MPM, |gap|>4 splits the regime).  No form / no
    grid extrapolation — this is the raw per-case corpus dump the списку view
    already computes, exported flat.  Missing fields render blank.
    NOTE: `areal_mAh` is an IDENTIFIER (cell-design target parsed from the name),
    NOT a porosity driver — porosity is intensive, set by composition/P:S/radii/
    pressure; it does not depend on areal capacity (except at the thin-SE-poor
    corner where thickness enters the regime gate)."""
    import io as _io, csv as _csv, re as _re
    up = app.config['UPLOAD_FOLDER']
    res = app.config['RESULTS_FOLDER']

    def _j(p):
        try:
            with open(p) as f:
                return json.load(f) or {}
        except Exception:
            return {}

    def _ratio(s):
        if not s or ':' not in str(s):
            return (None, None)
        try:
            a, b = str(s).split(':')[:2]
            return float(a), float(b)
        except Exception:
            return (None, None)

    rows = []
    if os.path.isdir(up):
        for cid in sorted(os.listdir(up)):
            cdir = os.path.join(up, cid)
            if not os.path.isdir(cdir):
                continue
            meta = _j(os.path.join(cdir, 'meta.json'))
            rdir = os.path.join(res, cid)
            fm = _j(os.path.join(rdir, 'full_metrics.json'))
            mm = _j(os.path.join(rdir, 'mpm_metrics.json'))
            ip = _j(os.path.join(cdir, 'input_params.json')) \
                or _j(os.path.join(rdir, 'input_params.json'))

            dem = fm.get('porosity_spheresum')
            if dem is None:
                dem = fm.get('porosity')
            mpm = mm.get('porosity_mpm_pct')
            if dem is None and mpm is None:
                continue  # no porosity of any kind → skip

            name = meta.get('name') or cid
            _mm = (_re.search(r'(\d+(?:\.\d+)?)\s*mAh', str(name), _re.I)
                   or _re.search(r'(\d+(?:\.\d+)?)\s*mAh', str(cid), _re.I))
            areal = _mm.group(1) if _mm else ''
            am_wt, se_wt = _ratio(fm.get('am_se_ratio') or ip.get('am_se_ratio')
                                  or meta.get('am_se_ratio'))
            P, S = _ratio(fm.get('ps_ratio') or meta.get('ps_ratio'))
            def _rp(k):
                # full_metrics stores particle radii in PHYSICAL µm already
                # (cf. docs/data/dem_design_points.csv: r_AM_P=6 / r_AM_S=2 /
                # r_SE=0.5–1.5).  Use the value as-is; only collapse a stray
                # ×1000 sim-inflated legacy value (no real radius is ≥100 µm).
                r = fm.get(k)
                try:
                    r = float(r)
                except (TypeError, ValueError):
                    return ''
                if r == 0:
                    return 0.0
                while abs(r) >= 100:
                    r /= 1000.0
                return round(r, 3)

            gap = ''
            regime = ''
            _graw = None
            if dem is not None and mpm is not None:
                _graw = float(dem) - float(mpm)   # RAW gap for the threshold (match list view)
                gap = round(_graw, 1)             # rounded only for display
                regime = ('SE-poor' if _graw > 4.0
                          else 'SE-rich' if _graw < -4.0 else 'cross-validated')
            # reliability gate — WHICH porosity to trust per regime:
            #   SE-poor  (gap>+4): MPM over-compresses the mono-large/thin corner
            #                      (no rigid contact net to hold the bed open)
            #                      → use DEM (rigid loose-truth).  band ±4.9
            #   SE-rich  (gap<-4): DEM ε_sphere overlap over-compresses
            #                      → use MPM (true plastic void-fill).  band ±1.1
            #   cross-validated  : two independent models agree → use MPM.  ±2.4
            use_source, use_por = '', ''
            if dem is not None and mpm is not None:
                if _graw > 4.0:
                    use_source, use_por = 'DEM', round(float(dem), 2)
                else:
                    use_source, use_por = 'MPM', round(float(mpm), 2)
            elif mpm is not None:
                use_source, use_por = 'MPM', round(float(mpm), 2)
            elif dem is not None:
                use_source, use_por = 'DEM', round(float(dem), 2)
            rows.append({
                'case': name, 'case_id': cid, 'areal_mAh': areal,
                'am_wt': am_wt if am_wt is not None else '',
                'se_wt': se_wt if se_wt is not None else '',
                'ps': ('%g:%g' % (P, S)) if (P is not None and S is not None)
                      else (fm.get('ps_ratio') or meta.get('ps_ratio') or ''),
                'r_AM_P_um': _rp('r_AM_P'), 'r_AM_S_um': _rp('r_AM_S'),
                'r_SE_um': _rp('r_SE'),
                'mpm_porosity_pct': round(float(mpm), 2) if mpm is not None else '',
                'dem_porosity_pct': round(float(dem), 2) if dem is not None else '',
                'gap_dem_minus_mpm': gap, 'regime': regime,
                'use_source': use_source, 'use_porosity_pct': use_por,
                'thickness_um': mm.get('thickness_mpm_um', ''),
                'se_fraction_pct': mm.get('se_fraction_pct', ''),
            })
    rows.sort(key=lambda r: str(r['case']))

    buf = _io.StringIO()
    fn = ['case', 'case_id', 'areal_mAh', 'am_wt', 'se_wt', 'ps',
          'r_AM_P_um', 'r_AM_S_um', 'r_SE_um', 'mpm_porosity_pct',
          'dem_porosity_pct', 'gap_dem_minus_mpm', 'regime',
          'use_source', 'use_porosity_pct',
          'thickness_um', 'se_fraction_pct']
    w = _csv.DictWriter(buf, fieldnames=fn)
    w.writeheader()
    w.writerows(rows)
    resp = make_response(buf.getvalue())
    resp.headers['Content-Type'] = 'text/csv; charset=utf-8'
    resp.headers['Content-Disposition'] = 'attachment; filename="porosity_corpus.csv"'
    return resp


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


def _report_strip_html(s):
    """Plain-text a possibly-HTML cell for markdown: <br> → '; ', drop tags,
    unescape common entities, collapse whitespace, escape pipes."""
    if s is None:
        return ''
    s = str(s)
    s = re.sub(r'<\s*br\s*/?\s*>', '; ', s, flags=re.I)
    s = re.sub(r'<[^>]+>', '', s)
    s = (s.replace('&lt;', '<').replace('&gt;', '>')
          .replace('&amp;', '&').replace('&nbsp;', ' ')
          .replace('&#10;', ' '))
    s = re.sub(r'\s+', ' ', s).strip()
    return s.replace('|', '\\|')


def _report_fmt_cell(v):
    """Format one table cell for markdown output (nan→'-', trim floats,
    strip any HTML)."""
    if isinstance(v, float):
        if v != v:  # NaN
            return '-'
        v = f'{v:.4g}'
    return _report_strip_html(v)


def _report_md_table(tbl):
    """Render a dashboard `tables[...]` entry (columns + data, possibly with
    HTML cells and '── section ──' header rows) as a GitHub-flavoured
    markdown table.  Section-header rows become bold separator rows."""
    cols = [str(c) for c in tbl.get('columns', [])]
    ncol = max(len(cols), 1)
    out = ['| ' + ' | '.join(cols) + ' |',
           '|' + '|'.join(['---'] * ncol) + '|']
    for row in tbl.get('data', []):
        row = list(row)
        first = str(row[0]) if row else ''
        if first.strip().startswith('──') or len(row) == 1:
            label = _report_strip_html(first).strip().strip('─ ').strip()
            out.append(f'| **{label}** |' + ' |' * (ncol - 1))
            continue
        cells = [_report_fmt_cell(c) for c in row[:ncol]]
        cells += [''] * (ncol - len(cells))
        out.append('| ' + ' | '.join(cells) + ' |')
    return '\n'.join(out)


@app.route('/results/<case_id>/report')
def serve_report(case_id):
    """Generate a comprehensive MD/PDF report that mirrors the full single-case
    dashboard: 개요 badges, Trust card, every analysis-summary tab (입자/접촉/
    배위수/네트워크/취성/종합 등급), physics derivations and figures."""
    case_dir = get_case_dir(case_id)
    meta_file = os.path.join(case_dir, 'meta.json')
    meta = {}
    if os.path.exists(meta_file):
        with open(meta_file) as f:
            meta = json.load(f)

    results_dir, archive_rel = _resolve_results_dir(case_id, meta)
    tables, metrics, input_params = _load_case_tables(results_dir, meta)
    trust_card = _build_trust_card(metrics)

    name = meta.get('name', case_id)
    scale = meta.get('scale', 1) or 1
    L = []

    # ── Header ──
    L.append(f'# DEM Analysis Report: {name}')
    L.append(f'> DEM/MPM Analyzer v3.0 | {datetime.now().strftime("%Y-%m-%d")}'
             + (f' | archive: `{archive_rel}`' if archive_rel else ''))
    L.append('')

    section = 1

    # ── 1. 케이스 개요 (header badges) ──
    L.append(f'## {section}. 케이스 개요 (Overview)\n')
    L.append('| 항목 | 값 |')
    L.append('|------|-----|')
    L.append(f'| Mode | {meta.get("mode", "-")} |')
    L.append(f'| Scale | {scale}× |')
    if meta.get('type_map'):
        L.append(f'| Type map | {meta["type_map"]} |')
    ps = meta.get('ps_ratio') or metrics.get('ps_ratio')
    if ps:
        L.append(f'| P:S (AM_P:AM_S 부피비) | {ps} |')
    am_se = metrics.get('am_se_ratio') or input_params.get('am_se_ratio')
    if am_se:
        tgt = input_params.get('am_se_ratio')
        if tgt and metrics.get('am_se_ratio') and tgt != metrics.get('am_se_ratio'):
            L.append(f'| AM:SE (무게비, 실측/target) | {metrics["am_se_ratio"]} ({tgt}) |')
        else:
            L.append(f'| AM:SE (무게비) | {am_se} |')
    if input_params.get('box_x') is not None and input_params.get('box_y') is not None:
        L.append(f'| RVE 단면적 | {input_params["box_x"]*scale:.0f}×'
                 f'{input_params["box_y"]*scale:.0f} μm |')
    if metrics.get('porosity') is not None:
        L.append(f'| Porosity (sphere-sum, production) | {metrics["porosity"]:.1f}% |')
    if metrics.get('porosity_union') is not None:
        L.append(f'| Porosity (union, overlap-corrected) | {metrics["porosity_union"]:.1f}% |')
    if metrics.get('overlap_fraction_pct') is not None:
        L.append(f'| Overlap fraction (plastic deformation) | {metrics["overlap_fraction_pct"]:.2f}% |')
    if metrics.get('thickness_um') is not None:
        L.append(f'| 두께 (가압 후) | {metrics["thickness_um"]:.1f} μm |')
    if metrics.get('percolation_pct') is not None:
        L.append(f'| SE Percolation | {metrics["percolation_pct"]:.1f}% |')
    if metrics.get('ionic_active_pct') is not None:
        L.append(f'| Ionic Active AM | {metrics["ionic_active_pct"]:.1f}% |')
    if metrics.get('e_se_eff_gpa') is not None:
        L.append(f'| E_SE_eff | {metrics["e_se_eff_gpa"]:.2f} GPa (bulk LPSCl: 24 GPa) |')
    if metrics.get('target_pressure_mpa') is not None:
        L.append(f'| Target Pressure | {metrics["target_pressure_mpa"]} MPa |')
    elif input_params.get('target_press_sim') is not None:
        L.append(f'| Target Pressure | {input_params["target_press_sim"]*1000:.1f} MPa |')
    L.append('')

    # Warnings
    warnings = metrics.get('warnings', [])
    if warnings:
        L.append('**⚠ Warnings**')
        L.append('')
        for w in warnings:
            icon = '🔴' if w.get('severity') == 'critical' else '🟡'
            L.append(f'- {icon} {w.get("msg", "")}')
        L.append('')
    L.append('---\n')
    section += 1

    # ── 2. Trust Card ──
    if trust_card:
        L.append(f'## {section}. Trust Card (Stage E self-report)\n')
        L.append(f'**Verdict: {_report_strip_html(trust_card["verdict"])}** '
                 f'— {trust_card["verdict_summary"]}')
        L.append('')
        L.append(f'> {_report_strip_html(trust_card["verdict_kr"])}')
        L.append('')
        L.append('| Gate | 상태 | 값 | 기준 (criterion) |')
        L.append('|------|------|-----|------------------|')
        state_map = {'pass': '✓ PASS', 'fail': '✗ FAIL', 'na': '— N/A'}
        for g in trust_card['leds']:
            L.append(f'| {_report_strip_html(g["label"])} '
                     f'| {state_map.get(g["cls"], g["cls"])} '
                     f'| {_report_strip_html(g["value"])} '
                     f'| {_report_strip_html(g["criterion"])} |')
        L.append('')
        L.append('---\n')
        section += 1

    # ── Analysis-summary tables (mirror dashboard tab order) ──
    tab_titles = [
        ('atom_statistics',      '입자 정보 (Particle Statistics)'),
        ('contact_summary',      '접촉 요약 (Contact Summary)'),
        ('coordination_summary', '배위수 (Coordination Number)'),
        ('network_summary',      '네트워크 지표 (Network Metrics)'),
        ('fracture_summary',     '취성 파괴 (Auerbach Fracture)'),
        ('overall_grade',        '종합 등급 (Overall Grade)'),
    ]
    for key, title in tab_titles:
        tbl = tables.get(key)
        if not tbl or not tbl.get('data'):
            continue
        L.append(f'## {section}. {title}\n')
        L.append(_report_md_table(tbl))
        L.append('')
        section += 1

    # ── Physics derivations (formula-level detail beyond the tables) ──
    L.append(f'## {section}. Physics Derivations\n')
    sigma_ratio = metrics.get('sigma_ratio')
    _sg_mS, _sg_note_md = _sigma_grain_context(metrics)   # 단일 출처 + 혼합-온도 경고 (S-8)
    if _sg_note_md:
        L.append(f'> {_sg_note_md}\n')
    sigma_brug = sigma_ratio * _sg_mS if sigma_ratio else None
    sigma_net = metrics.get('sigma_full_mScm')

    L.append('### Ionic Conductivity — Bruggeman vs Network Solver\n')
    L.append('```')
    L.append('σ_Bruggeman = σ_grain × φ_SE × f_perc / τ²   (접촉 저항 무시)')
    if sigma_ratio and metrics.get('phi_se') and metrics.get('tortuosity_mean'):
        tau = metrics.get('tortuosity_recommended', metrics.get('tortuosity_mean', 1))
        f_perc = metrics.get('percolation_pct', 100) / 100
        L.append(f'            = {_sg_mS:.1f} × {metrics["phi_se"]:.3f} × {f_perc:.3f} / {tau:.2f}²')
        L.append(f'            = {sigma_brug:.4f} mS/cm')
    if sigma_net:
        L.append('')
        L.append(f'σ_ionic     = {sigma_net:.4f} mS/cm   (Kirchhoff network solver, Holm 1967)')
        if sigma_brug:
            L.append(f'σ_brug/σ_ionic = {sigma_brug/sigma_net:.1f}×   (Bruggeman overestimation)')
        if metrics.get('bulk_resistance_fraction') is not None:
            L.append(f'Constriction fraction = {(1-metrics["bulk_resistance_fraction"])*100:.1f}%')
    L.append('```')
    L.append('')

    sigma_el = metrics.get('electronic_sigma_full_mScm')
    sigma_th = metrics.get('thermal_sigma_full_mScm')
    if sigma_el is not None or sigma_th is not None or metrics.get('stress_cv'):
        L.append('### Electronic / Thermal / Mechanical\n')
        if sigma_el is not None:
            L.append(f'- **σ_electronic**: {sigma_el:.2f} mS/cm')
            if metrics.get('electronic_percolating_fraction') is not None:
                L.append(f'- **AM Percolation (전자)**: {metrics["electronic_percolating_fraction"]*100:.1f}%')
            if metrics.get('electronic_active_fraction') is not None:
                L.append(f'- **Electronic Active AM**: {metrics["electronic_active_fraction"]*100:.1f}%')
                dead = (1 - metrics['electronic_active_fraction']) * 100
                if dead > 10:
                    L.append(f'- **Dead AM**: {dead:.1f}% → 도전재 추가 검토 필요')
        if sigma_th is not None:
            L.append(f'- **σ_thermal**: {sigma_th:.3f} mS/cm equiv')
        if metrics.get('stress_cv'):
            L.append(f'- **Stress CV**: {metrics["stress_cv"]:.1f}%')
            for skey in ['sigma_AM_P_ratio', 'sigma_AM_S_ratio', 'sigma_SE_ratio']:
                val = metrics.get(skey)
                if val:
                    slabel = skey.replace('sigma_', 'σ_').replace('_ratio', '/σ_mean')
                    L.append(f'- **{slabel}**: {val:.3f}')
        L.append('')

    L.append('### Scaling Law Reference\n')
    L.append('| Channel | Formula | R² |')
    L.append('|---------|---------|-----|')
    L.append('| σ_ion (v12-clean v3, final) | σ_grain × √(φ−0.2) × CN^(3/2) × cov^(2/5) × f_p³ × C_blend(τ) | 0.981 |')
    L.append('| σ_el | 0.015 × σ_AM × φ_AM^(3/2) × CN_AM² × exp(π/(T/d)) | 0.89 |')
    L.append('| σ_th | 286 × σ_ion^(3/4) × φ_AM² / CN_SE | 0.90 |')
    L.append('')
    L.append('> σ_ion is the v12-clean v3 production model (n=57, LOOCV=0.979): '
             'σ_grain=3.0 mS/cm, φc=0.20; the τ dependence is carried by the '
             'sigmoid-blended prefactor C_blend(τ). See '
             'docs/ionic_scaling_law_experiments.md.')
    # 온도가 적용된 런에서만 한 줄 더 (미적용 = 전 코퍼스 = 이 줄 없음 → 리포트 바이트 동일).
    # 스케일링-법칙의 3.0 은 T_ref=25 °C 규약값이므로, T-스케일된 σ 와 나란히 두면 오독된다.
    if abs(_sg_mS - _se_material().SIGMA_GRAIN_MS_CM_25C) > 1e-12:
        L.append(f'>\n> ⚠ 이 런은 운전온도가 적용되어 σ_grain = {_sg_mS:.4f} mS/cm '
                 f'(= 25 °C 규약값 3.0 × Arrhenius)로 풀렸다. 위 스케일링-법칙 표의 3.0 은 '
                 f'**25 °C 규약값**이며 그 회귀(LOOCV 0.979)는 25 °C 코퍼스에서 적합된 것이다 '
                 f'— 온도축 비교에 그대로 쓰지 말 것 (docs/temp_pressure_capability.md §3-4).')
    L.append('')
    section += 1

    # ── Figures ──
    figures_dir = os.path.join(results_dir, 'figures')
    if os.path.isdir(figures_dir):
        pngs = sorted(os.path.basename(p)
                      for p in globmod.glob(os.path.join(figures_dir, '*.png')))
        if pngs:
            L.append(f'## {section}. Figures ({len(pngs)})\n')
            for fn in pngs:
                L.append(f'### {fn}\n')
                L.append(f'![{fn}](figures/{fn})\n')
            section += 1

    L.append('---\n')
    L.append('*Generated by DEM/MPM Analyzer v3.0 — Kirchhoff Network Solver + Physics Scaling Laws*\n')

    report = '\n'.join(L)

    from io import BytesIO
    fmt = request.args.get('format', 'md')
    if fmt == 'pdf':
        return _generate_pdf_report(report, name)

    buf = BytesIO(report.encode('utf-8'))
    return send_file(buf, mimetype='text/markdown', as_attachment=True,
                    download_name=f'{name}_report.md')


_GRADE_DIR_KR = {
    'higher':        '높을수록 ↑ 좋음',
    'lower':         '낮을수록 ↓ 좋음',
    'band':          '적정 band (optimum 근처일수록 좋음)',
    'higher_corpus': 'corpus 대비 높을수록 ↑ 좋음 (percentile)',
    'lower_corpus':  'corpus 대비 낮을수록 ↓ 좋음 (percentile)',
}


# Plain-language ("쉽게 말하면") explanations per grade axis (keyed by axis
# key), written for a first-time reader.  The technical `meaning` from
# grade_engine is kept intact; the guide shows this friendly version first.
_GRADE_PLAIN = {
    'porosity': '전극 안의 빈 공간 비율이에요 (sphere-sum 방식, production calibration anchor). '
        '빈틈이 너무 많으면 이온·전자가 지날 길이 끊기고, 너무 빽빽하면 충·방전 때 부풀다 깨질 수 있어요. '
        '그래서 적당한 값(약 13%)이 가장 좋습니다.',
    'porosity_union': '같은 빈 공간 비율인데, 입자끼리 겹친 부피(overlap)를 빼고 계산한 버전이에요 (문헌 비교용). '
        'Sphere-sum보다 항상 살짝 큽니다 — 겹친 만큼 빈공간이 더 보이니까요. 보조 지표이고, '
        'production form은 sphere-sum 값을 씁니다.',
    'overlap_fraction_pct': '입자들이 서로 얼마나 겹쳤는지(소성변형 정도)를 백분율로 나타낸 값이에요. '
        '380 MPa 압력에서 SE 입자는 문헌상 5-10% 정도 소성변형하는데, 그 범위 안이면 정상. '
        '10% 넘으면 과압축 의심.',
    'thickness_um': '전극을 얼마나 두껍게 쌓았는지예요. 너무 얇으면 실험용 샘플 수준이고, '
        '너무 두꺼우면 이온이 끝까지 가기 힘들어 저항이 커집니다. 60~130μm가 실제 배터리에 쓰는 범위예요.',
    'percolation_pct': '이온이 다니는 고체전해질 길이 위에서 아래까지 끊김 없이 이어진 비율이에요. '
        '100%에 가까울수록 모든 이온이 길을 찾고, 낮으면 막다른 골목(죽은 구역)이 생깁니다.',
    '__cut_fraction': '이온 길에서 "딱 하나 끊으면 전체가 둘로 갈라지는 핵심 길목"이 얼마나 많은지예요. '
        '적을수록 길이 여러 갈래로 튼튼하게 이어진 거라 좋습니다. (다리 하나뿐인 섬 vs 다리 여러 개)',
    '__bn_below_frac': '이온 길 중 "병목(아주 좁은 통로)"이 차지하는 비율이에요. 좁은 통로가 많으면 '
        '거기서 저항이 커져 이온이 느려집니다. 적을수록 좋아요. (고속도로에 좁은 1차선 구간이 적을수록 안 막힘)',
    '__bn_median_norm': '이온이 지나는 통로(접촉면)가 평균적으로 얼마나 넓은지예요. 넓을수록 잘 흐릅니다. '
        '(수도관이 굵을수록 물이 잘 나오는 것과 같아요)',
    'se_se_cn': '고체전해질 알갱이 하나가 평균 몇 개의 이웃과 맞닿아 있는지예요. 많을수록(4~6개) '
        '촘촘히 잘 쌓인 거고, 적으면(<3) 듬성듬성한 상태입니다.',
    'se_se_cn_std': '위 "이웃 수"가 알갱이마다 얼마나 들쭉날쭉한지예요. 작을수록 모두 고르게 쌓인 거라 '
        '좋고, 크면 어떤 건 외톨이·어떤 건 과밀이라 불균일합니다.',
    '__tau_lap_eff': '이온이 위→아래로 갈 때 실제로 얼마나 "돌아가고 좁아져서" 느려지는지를 한 숫자로 '
        '나타낸 거예요(굴곡도). 1이면 직선, 클수록 빙 돌아가 느립니다. 작을수록 좋고 COMSOL/EIS에 넣는 핵심 값.',
    '__tau_lap_bulk': '위 굴곡도에서 "좁아짐(병목)" 효과를 빼고 길이 순수하게 얼마나 돌아가는지만 본 값이에요. '
        '구조 자체의 우회 정도입니다.',
    '__constriction_overhead': '전체 굴곡도가 "순수 우회"보다 몇 배 더 나빠졌는지예요. 1배면 좁아짐 손해가 '
        '없는 거고, 클수록 좁은 통로 때문에 추가로 느려진 겁니다.',
    'tortuosity_recommended': '이온이 갈 수 있는 가장 짧은 길이 직선 대비 얼마나 더 돌아가는지(기하학적 우회만). '
        '1.0이면 거의 직선, 클수록 미로처럼 돌아갑니다.',
    'path_hop_area_mean_physics': '이온이 길을 한 칸씩 건널 때 거치는 접촉면의 평균 넓이예요. '
        '넓을수록 한 번에 더 많이 흘러서 좋습니다.',
    'coverage_AM_P_mean_physics': '큰 활물질 입자(AM_P) 표면 중 고체전해질이 닿아있는 비율이에요. '
        '많이 닿아야 그 부분에서 이온을 주고받습니다. 60% 이상 권장.',
    'coverage_AM_S_mean_physics': '작은 활물질 입자(AM_S) 표면이 고체전해질에 덮인 비율이에요. '
        '작은 입자는 더 고르게 덮일수록 좋습니다.',
    'coverage_AM_mean_physics_rough': '입자의 찌그러진 모양까지 반영해 계산한 "가장 믿을 만한" 전체 덮임 '
        '비율이에요. 활물질이 이온과 만나는 면적이 얼마나 되는지를 봅니다.',
    'am_se_cn_mean': '활물질 입자 하나가 평균 몇 개의 고체전해질과 닿아있는지예요. 많을수록 이온 공급 '
        '통로가 여러 개라 안정적입니다.',
    'ionic_active_pct': '이온이 실제로 도달할 수 있는 활물질의 비율이에요. 100%면 모든 활물질이 작동하고, '
        '낮으면 이온이 못 가는 "죽은 활물질"이 생겨 용량을 못 씁니다.',
    '__vulnerable_pct': '지금은 연결돼 있지만 고체전해질이 살짝만 덮여 있어서, 충·방전을 반복하면 끊길 '
        '위험이 큰 활물질 비율이에요. 적을수록 좋습니다.',
    '__am_percolation_pct': '활물질끼리 서로 닿아 전자가 위→아래로 통하는 비율이에요. 낮으면 도전재(탄소)를 '
        '넣어 보완할 수 있어 그렇게 치명적이진 않습니다.',
    '__electronic_active_pct': '전자가 아래 집전체(전류 받는 판)까지 도달할 수 있는 활물질 비율이에요. '
        '역시 도전재로 보완 가능합니다.',
    'electronic_sigma_full_mScm_stage_e_physics': '도전재(탄소) 없이 활물질만으로의 전자 전도도예요. '
        '낮아도 탄소 1~3%만 넣으면 크게 좋아지므로 점수 비중은 작게 둡니다.',
    '__frac_severe_force_pct': '압착하는 동안 입자가 "완전히 부서진" 비율이에요. 한번 부서지면 못 '
        '돌아오는 진짜 손상이라 적을수록 좋습니다.',
    'frac_multicrack_force_pct': '입자에 금이 여러 개 간(완전히 부서진 건 아닌) 비율이에요. 고체전지에선 '
        '일부 금이 오히려 새 접촉면을 만들어 그렇게 나쁘지만은 않아 비중을 작게 둡니다.',
    'fracture_index_force': '압착 중 생긴 균열을 종합한 점수예요(심할수록 큼). 단 사이클 중 손상이 아니라 '
        '제조 시점 손상이라 비중이 작습니다.',
    '__sigma_vm_cv_pct': '입자들이 받는 힘(응력)이 얼마나 들쭉날쭉한지예요. 작을수록 골고루 눌린 거고, '
        '크면 특정 입자에 힘이 몰리는 "핫스팟"이 있다는 뜻입니다.',
    'sigma_full_mScm_stage_e_physics': '이 전극의 이온 전도도 — 이온이 얼마나 잘 흐르는지를 나타내는 가장 '
        '중요한 값이에요(높을수록 좋음). 배터리 성능 1순위 지표입니다.',
    'thermal_sigma_full_mScm_stage_e_physics': '열을 얼마나 잘 퍼뜨리는지(냉각 능력)예요. 고체전지에서 '
        '성능을 좌우하는 1차 요소는 아니라 비중이 작습니다.',
    'R_brug_over_full_physics': '간단한 이론식이 실제보다 이온 전도도를 몇 배나 부풀려 예측하는지예요. '
        '작을수록 이상적 구조에 가깝다는 뜻입니다.',
    '__constriction_R_fraction_pct': '전체 저항 중 "좁은 통로(병목)"에서 생기는 저항의 비율이에요. '
        '작을수록 좁아짐 손해가 적습니다.',
    '__Q_gravimetric_mAhg': '무게 1g당 담을 수 있는 전기량(비용량)이에요. 같은 무게로 더 멀리 가는 배터리 '
        '= 높을수록 좋음. 업계에서 가장 중요한 지표 중 하나입니다.',
    '__Q_volumetric_mAhcc': '부피 1cc당 담을 수 있는 전기량이에요. 같은 크기로 더 오래 쓰는 배터리. '
        '상용화 목표는 500 이상입니다.',
    '__commercial_composition': '활물질:고체전해질 무게비가 상용 배터리들이 쓰는 "황금 비율(약 82%)"에 '
        '얼마나 가까운지예요. 한쪽으로 너무 치우치면 비용이나 에너지에서 손해입니다.',
    '__wt_am_pct': '전극에서 활물질이 차지하는 무게 비율이에요. 많을수록 에너지가 크지만, 너무 많으면 '
        '이온 길이 부족해집니다.',
    '__Q_target_match_pct': '이 케이스가 "목표로 한 용량(예: 6 mAh/cm²)"을 실제로 달성했는지 맞춰보는 '
        '거예요. 목표가 없는 케이스는 평가하지 않습니다(N/A).',
    '__ps_ratio_band': '큰 입자:작은 입자 비율이 여러 논문이 최적이라 보는 "7:3" 근처인지예요. 큰 입자 '
        '사이를 작은 입자가 채워 더 촘촘히 쌓입니다.',
    '__r_SE_um': '넣은 고체전해질 알갱이 크기(반지름)예요. 입력값일 뿐 성능 점수엔 거의 영향 없는 참고 정보입니다.',
    '__lambda_eff': '활물질 입자가 고체전해질 입자보다 몇 배 큰지예요. 설계 비율 참고용이고 점수 영향은 작습니다.',
    '__stage_e_available': '문헌 기반 보정(Stage E)이 적용됐는지 체크하는 품질 표시예요. 적용 안 되면 '
        '전도도가 부풀려졌을 수 있습니다.',
    '__compaction_efficiency': '300 MPa로 눌렀을 때 빈 공간이 적당히(12~18%) 줄었는지예요. 너무 누르면 '
        '깨지고, 덜 누르면 접촉이 부족합니다.',
    '__bimodal_design': '큰 입자+작은 입자를 섞은 설계(bimodal)인지예요. 상용 양극은 거의 이렇게 만들어 '
        '더 촘촘히 쌓입니다. 한 종류만 쓴 경우는 페널티 없이 따로 평가합니다.',
    '__volume_change_buffer': '충·방전 때 활물질이 ~5% 부풀어도 견딜 빈 공간(완충 여유)이 충분한지예요. '
        '10% 이상이면 안전, 6% 미만이면 박리 위험.',
    '__asr_ionic_Ohm_cm2': '이온이 전극을 통과할 때 받는 "면적당 저항"이에요(낮을수록 좋음). 100 이하면 '
        '실용 가능. 단 고체전해질이 많으면 자동으로 낮아지니 에너지밀도와 같이 봐야 합니다.',
    '__Q_areal_mAhcm2': '전극 1cm²가 내는 용량이에요. 클수록 같은 저항이라도 더 가치 있는 셀입니다. '
        '5 이상이 상용 목표.',
    '__ASR_per_capacity': '저항을 용량으로 나눈 값 — "용량 대비 저항 부담"이에요. 얇아서 용량이 작으면 같은 '
        '저항이라도 더 불리해지는 걸 잡아냅니다. 작을수록 좋음.',
    '__asr_electronic_Ohm_cm2': '전자가 받는 면적당 저항이에요. 도전재로 낮출 수 있어 비중은 작습니다.',
    '__asr_thermal_Kcm2_W': '열이 빠져나갈 때의 저항(냉각 효율)이에요. 1차 성능 요소는 아닙니다.',
    '__ASR_total_Ohm_cm2': '이온+전자 저항을 합친 전체 저항이에요. 한쪽만 보면 안 되니 합쳐서 봅니다. '
        '낮을수록 좋음.',
    '__c_rate_capability': '전체 저항의 역수 — "빠르게 충·방전할 수 있는 능력"을 직관적으로 본 값이에요. '
        '클수록 고출력에 유리합니다.',
    '__polarization_mV_at_C3': '실제 C/3 속도로 쓸 때 생기는 전압 손실(분극)이에요. 작을수록 효율적이고, '
        '실험(EIS)으로 바로 확인 가능한 값입니다.',
    '__am_am_short_risk_cn': '활물질끼리 얼마나 직접 붙어있는지예요. 2~3개가 적당 — 너무 적으면 전자전도가 '
        '약하고, 너무 많으면 전자가 지름길로 흘러 내부 단락(쇼트) 위험이 커집니다.',
    '__cycle_stable_AM_pct': '충·방전을 반복해도 안정적으로 살아남는 활물질 비율이에요(이온도 닿고, 전자도 '
        '통하고, 심한 손상도 없는 입자). 한번 부서지면 영구 손실이라 수명의 핵심 지표입니다.',
    '__sigma_e_fracture_loss_pct': '입자가 깨져서 전자 전도가 잃은 비율이에요. 단 이건 도전재로 회복 '
        '가능해서 비중은 작습니다.',
    '__validation_pass_pct': '이 분석 결과가 믿을 만한지 자체 점검(Stage E) 통과율이에요. 100%면 완전히 '
        '재현 가능, 60% 미만이면 결과를 의심해야 합니다.',
}


def _fmt_num(v):
    """Compact number formatting for grade-band cutoffs."""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return str(v)
    if f == int(f):
        return str(int(f))
    return f'{f:.4g}'


def _grade_band_desc(ax_meta):
    """Human-readable grade-band breakdown for one axis, derived from its
    thresholds / band / corpus definition.  Scores anchor at A95 B+88 B80
    B-72 C+64 C56 (see grade_engine._interp_score)."""
    direction = ax_meta.get('direction')
    grades = ['A', 'B+', 'B', 'B-', 'C+', 'C']
    if direction in ('higher', 'lower'):
        thr = ax_meta.get('thresholds') or []
        sym = '≥' if direction == 'higher' else '≤'
        tail = '그 미만 D' if direction == 'higher' else '그 초과 D'
        parts = [f'{g} {sym}{_fmt_num(t)}' for g, t in zip(grades, thr)]
        return ' · '.join(parts) + f' · {tail}'
    if direction == 'band':
        opt = ax_meta.get('optimum'); bw = ax_meta.get('band_width', 0)
        return (f'적정값 {_fmt_num(opt)} 기준 |값−optimum|: '
                f'A ≤{_fmt_num(0.2*bw)} · B+ ≤{_fmt_num(0.6*bw)} · '
                f'B ≤{_fmt_num(1.0*bw)} · C+ ≤{_fmt_num(1.5*bw)} · '
                f'C ≤{_fmt_num(2.0*bw)} · 그 밖 D')
    if direction in ('higher_corpus', 'lower_corpus'):
        better = '낮을수록' if direction == 'lower_corpus' else '높을수록'
        return (f'동적 corpus(기준 82개 + 현재 분석된 모든 케이스)의 백분위로 채점 — '
                f'{better} 좋은 백분위에 높은 등급. corpus가 케이스 추가 시 자동으로 '
                f'커집니다. (percolating 필터를 통과하는) 유효 케이스가 5개 미만이면 '
                f'비교 기준이 없어 "—" (채점 불가).')
    return '—'


def _build_grade_guide_md(case_id):
    """Build a per-case '평가표 상세 설명 / grade 근거' document: the grading
    rubric (scale, weighting, corpus rule) plus every axis with this case's
    value+grade+basis and its meaning/formula — pulled live from
    scripts/grade_engine so it never drifts from the 종합 등급 tab."""
    import sys as _sys
    scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
    if scripts_dir not in _sys.path:
        _sys.path.insert(0, scripts_dir)
    from grade_engine import AXES, GRADE_SCALE  # noqa: E402

    case_dir = get_case_dir(case_id)
    meta = {}
    meta_file = os.path.join(case_dir, 'meta.json')
    if os.path.exists(meta_file):
        with open(meta_file) as f:
            meta = json.load(f)
    results_dir, _arch = _resolve_results_dir(case_id, meta)
    metrics = {}
    mp = os.path.join(results_dir, 'full_metrics.json')
    if os.path.exists(mp):
        with open(mp) as f:
            metrics = json.load(f)

    result = _grade_engine_result(metrics, results_dir)
    name = meta.get('name', case_id)
    # axis metadata (weight/formula) by label for merging with scored axes
    meta_by_label = {ax['label']: ax for ax in AXES}

    L = [f'# 종합 등급 평가표 상세 설명: {name}',
         f'> Grade rubric & rationale | {datetime.now().strftime("%Y-%m-%d")}',
         '']
    # Grade scale
    L.append('## 등급 척도 (Grade scale)\n')
    L.append('| 등급 | 최소 점수 | GPA |')
    L.append('|------|-----------|-----|')
    for label, cutoff, gpa in GRADE_SCALE:
        L.append(f'| {label} | {cutoff} | {gpa} |')
    L.append('')
    # How scoring works
    L.append('## 채점 방식 (How each axis is scored)\n')
    L.append('- **higher / lower**: 고정 문헌-기반 임계값 6개(A→C)에 값을 보간해 점수화.')
    L.append('- **band**: optimum 근처일수록 A, |값−optimum| 이 커질수록 감점.')
    L.append('- **corpus (higher_corpus / lower_corpus)**: 고정 임계 대신 **백분위(등수)**'
             '로 채점. 비교 명단(corpus)은 **동적** — 기준 82개 baseline에 **현재까지 '
             '분석된(3D 뷰어가 로드된) 모든 케이스를 합쳐** 만들며, 케이스가 추가될수록 '
             '자동으로 커집니다. (percolating 필터를 통과하는) 유효 케이스가 '
             '**5개 미만이면 채점 불가 → "—"**. 예) *Bottleneck burden* 은 `bn_below_frac` '
             '값을 가진 케이스가 아직 5개 미만이면 "—" 로 나오며, 뷰어를 로드한 케이스가 '
             '쌓이면 자동으로 채점됩니다. 또 이 케이스 자체의 SE 진단값(viewer_aux.json)이 '
             '없으면(3D 뷰어 미로드) 값이 없어 "—" 가 됩니다.')
    L.append('- **종합**: 점수가 매겨진 axis들의 **가중평균** (weight 열). '
             '카테고리 평균은 해당 카테고리 axis 점수의 단순평균.')
    L.append('')

    # Quick-scan summary table, then a detailed narrative per axis
    if result and result.get('axes'):
        L.append('## 한눈에 보기 (요약)\n')
        L.append('| 카테고리 | 지표 | 값 | 등급 | 가중치 |')
        L.append('|----------|------|-----|------|--------|')
        for ax in result['axes']:
            v = ax['value']
            vstr = ('—' if v is None else f'{v:.1f}' if abs(v) >= 100
                    else f'{v:.3g}' if abs(v) >= 1 else f'{v:.4g}')
            sc = ax['score']
            gstr = f'{ax["grade"]}({sc:.0f})' if sc is not None else '—'
            wt = meta_by_label.get(ax['label'], {}).get('weight', ax.get('weight', '—'))
            L.append('| ' + ' | '.join(_report_strip_html(x) for x in [
                ax['category'], ax['label'], vstr, gstr, str(wt)]) + ' |')
        L.append('')

        L.append('---\n')
        L.append('# 지표별 상세 설명\n')
        last_cat = None
        for ax in result['axes']:
            cat = ax['category']
            if cat != last_cat:
                L.append(f'## {cat}\n')
                last_cat = cat
            v = ax['value']
            if v is None:
                vstr = '값 없음'
            elif abs(v) >= 100:
                vstr = f'{v:.1f}'
            elif abs(v) >= 1:
                vstr = f'{v:.3g}'
            else:
                vstr = f'{v:.4g}'
            score = ax['score']
            gstr = f'{ax["grade"]} ({score:.0f}점)' if score is not None else '— (채점 불가)'
            ax_meta = meta_by_label.get(ax['label'], {})
            wt = ax_meta.get('weight', ax.get('weight', '—'))
            dir_kr = _GRADE_DIR_KR.get(ax.get('direction'), ax.get('direction') or '—')
            L.append(f'### {_report_strip_html(ax["label"])}\n')
            L.append(f'**이 케이스: {gstr} · 값 = {vstr}**')
            L.append('')
            L.append(f'- **카테고리**: {_report_strip_html(cat)}')
            L.append(f'- **가중치**: {wt}  (종합 가중평균에서의 영향력 — 클수록 핵심 지표)')
            L.append(f'- **방향**: {dir_kr}')
            if ax.get('formula'):
                L.append(f'- **계산식**: `{_report_strip_html(ax["formula"])}`')
            L.append(f'- **등급 구간**: {_report_strip_html(_grade_band_desc(ax_meta))}')
            basis = ax.get('basis')
            if basis and basis != 'no data':
                L.append(f'- **이 케이스 채점 근거**: {_report_strip_html(basis)}')
            elif basis == 'no data':
                L.append('- **이 케이스 채점 근거**: 데이터 없음 — 값 또는 '
                         'corpus 비교군 부족으로 채점되지 않음.')
            plain = _GRADE_PLAIN.get(ax_meta.get('key'))
            if plain:
                L.append('')
                L.append(f'**쉽게 말하면**: {_report_strip_html(plain)}')
            meaning = ax.get('meaning', '')
            if meaning:
                L.append('')
                L.append(f'**자세히 (기술적 근거)**: {_report_strip_html(meaning)}')
            L.append('')
        comp = result.get('composite', {})
        L.append('## 종합 (Composite)\n')
        L.append(f'- **Overall**: {comp.get("grade","—")} '
                 f'({comp.get("score","—")} / 100, '
                 f'GPA {comp.get("gpa","—")} / 4.3) — '
                 f'{comp.get("n_axes","?")}/{comp.get("n_total","?")} axes scored')
        cs = result.get('category_scores', {})
        if cs:
            L.append('')
            L.append('| 카테고리 | 평균 점수 |')
            L.append('|----------|-----------|')
            for c, s in cs.items():
                L.append(f'| {_report_strip_html(c)} | {s:.1f} |')
        L.append('')
    else:
        L.append('> 이 케이스는 종합 등급을 산출할 수 없습니다 (full_metrics.json 없음 '
                 '또는 채점 가능한 axis 없음).')
        L.append('')

    L.append('---\n')
    L.append('*Generated by DEM/MPM Analyzer — grade rubric from scripts/grade_engine.py*')
    return '\n'.join(L), name


@app.route('/results/<case_id>/grade-guide')
def serve_grade_guide(case_id):
    """평가표 상세 설명 + grade 근거 문서 (MD 기본, ?format=pdf 로 PDF)."""
    from io import BytesIO
    report, name = _build_grade_guide_md(case_id)
    if request.args.get('format') == 'pdf':
        return _generate_pdf_report(report, f'{name}_grade_guide')
    buf = BytesIO(report.encode('utf-8'))
    return send_file(buf, mimetype='text/markdown', as_attachment=True,
                    download_name=f'{name}_grade_guide.md')


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

_2D_SCALAR_KEYS = (
    'case_id', 'case_name', 'mode', 'ps_ratio', 'phase_fracs',
    'coverage_2d_pct', 'coverage_3d_target_pct',
    'coverage_AM_P_pct', 'coverage_AM_S_pct',
    'coverage_AM_P_target_pct', 'coverage_AM_S_target_pct',
    'r_AM_P_d50_um', 'r_AM_S_d50_um', 'thickness_um',
    'a_extent', 'b_extent', 'n_pixels', 'pa_um', 'grain_size_um',
)


def _synth_2d_png_path(results_dir, seed=None):
    """Single canonical cache — the last generated figure is 'the existing one'
    shown on load; regenerating overwrites it."""
    return os.path.join(results_dir, 'microstructure_2d.png')


def _synth_2d(case_id, px=600, seed=0, force=False):
    """Synthesize + render the 2D representative microstructure, caching the
    PNG and a scalar summary JSON under the results dir.  Returns the scalar
    summary dict (or None if the case lacks the required data)."""
    import sys as _sys
    case_dir = get_case_dir(case_id)
    results_dir = get_results_dir(case_id)
    atoms_csv = os.path.join(results_dir, 'atoms.csv')
    if not os.path.exists(atoms_csv):
        return None
    png_path = _synth_2d_png_path(results_dir, seed)
    sum_path = png_path.replace('.png', '_summary.json')
    _scripts_dir = app.config['SCRIPTS_FOLDER']
    script_path = os.path.join(_scripts_dir, 'extract_2d_microstructure.py')

    def _stale():
        if not (os.path.exists(png_path) and os.path.exists(sum_path)):
            return True
        cm = os.path.getmtime(png_path)
        # invalidate when the source data OR the generator script changes
        if cm < os.path.getmtime(atoms_csv):
            return True
        if os.path.exists(script_path) and cm < os.path.getmtime(script_path):
            return True
        return False

    if not force and not _stale():
        try:
            with open(sum_path) as f:
                return json.load(f)
        except Exception:
            pass
    if _scripts_dir not in _sys.path:
        _sys.path.insert(0, _scripts_dir)
    import importlib
    import extract_2d_microstructure as ex2d
    ex2d = importlib.reload(ex2d)                    # pick up edits in a live process
    data, gap = ex2d.synthesize_adaptive(Path(case_dir), n_pixels=px, seed=seed)
    if data is None:
        return None
    ex2d.render_png(data, Path(png_path))
    # Clean geometry-only export (LEFT phase map, no axes/labels/legend), kept
    # in sync with the displayed figure.
    try:
        ex2d.render_geometry_png(data, Path(png_path.replace('.png', '_geometry.png')))
    except Exception:
        import traceback; traceback.print_exc()
    summary = {k: data.get(k) for k in _2D_SCALAR_KEYS}
    summary['seed'] = int(seed)                      # remember which seed is shown
    summary['gap_um'] = round(float(gap), 3)         # auto-picked per case
    with open(sum_path, 'w') as f:                   # np.float64 → float for JSON
        json.dump(summary, f, indent=2,
                  default=lambda o: float(o) if hasattr(o, '__float__') else str(o))
    # round-trip so returned scalars are plain Python (csv/format safe)
    return json.loads(json.dumps(summary,
                      default=lambda o: float(o) if hasattr(o, '__float__') else str(o)))


def _synth_2d_auto(case_id, seed=0, px=450, iters=3):
    """Closed-loop generate→check→fine-tune; caches PNG + a JSON report
    (achieved vs target coverage, SE connectivity, per-iteration trace)."""
    import sys as _sys
    import importlib
    case_dir = get_case_dir(case_id)
    results_dir = get_results_dir(case_id)
    if not os.path.exists(os.path.join(results_dir, 'atoms.csv')):
        return None
    _sd = app.config['SCRIPTS_FOLDER']
    if _sd not in _sys.path:
        _sys.path.insert(0, _sd)
    import extract_2d_microstructure as ex2d
    ex2d = importlib.reload(ex2d)
    data, report = ex2d.synthesize_calibrated(Path(case_dir), n_pixels=px,
                                              seed=seed, iters=iters)
    if data is None:
        return None
    png = os.path.join(results_dir, f'microstructure_2d_auto_s{seed}.png')
    ex2d.render_png(data, Path(png))
    out = {'report': report, 'se_conn': ex2d._se_connectivity_pct(data['labels']),
           'phase_fracs': data.get('phase_fracs'), 'ps_ratio': data.get('ps_ratio'),
           'covP': data.get('coverage_AM_P_pct'), 'tgtP': data.get('coverage_AM_P_target_pct'),
           'covS': data.get('coverage_AM_S_pct'), 'tgtS': data.get('coverage_AM_S_target_pct')}
    out = json.loads(json.dumps(out, default=lambda o: float(o) if hasattr(o, '__float__') else str(o)))
    with open(os.path.join(results_dir, f'microstructure_2d_auto_s{seed}.json'), 'w') as f:
        json.dump(out, f)
    return out


@app.route('/results/<case_id>/2d-auto.png')
def serve_2d_auto(case_id):
    """Generate with the auto-calibration loop and serve the figure."""
    seed = int(request.args.get('seed', 0))
    try:
        rep = _synth_2d_auto(case_id, seed=seed)
    except Exception as e:
        import traceback; traceback.print_exc()
        return (f'{type(e).__name__}: {e}', 500)
    if rep is None:
        return ('2D microstructure unavailable (need atoms.csv + meta/params)', 404)
    png = os.path.join(get_results_dir(case_id), f'microstructure_2d_auto_s{seed}.png')
    return send_file(png, mimetype='image/png', as_attachment=False,
                     download_name=f'microstructure_2d_auto_{case_id}_s{seed}.png')


@app.route('/results/<case_id>/2d-auto-report.json')
def serve_2d_auto_report(case_id):
    seed = int(request.args.get('seed', 0))
    p = os.path.join(get_results_dir(case_id), f'microstructure_2d_auto_s{seed}.json')
    if not os.path.exists(p):
        return jsonify({'error': 'not generated yet'}), 404
    return send_file(p, mimetype='application/json')


@app.route('/results/<case_id>/2d-microstructure.png')
def serve_2d_microstructure(case_id):
    """2D microstructure figure.  Without ?fresh=1 it serves the EXISTING
    cached figure (the last one generated); ?fresh=1 regenerates with the given
    (random) seed and overwrites the cache."""
    px = max(200, min(1200, int(request.args.get('px', 600))))
    seed = int(request.args.get('seed', 0))
    force = request.args.get('fresh') in ('1', 'true', 'yes')
    try:
        summary = _synth_2d(case_id, px=px, seed=seed, force=force)
    except Exception as e:
        import traceback; traceback.print_exc()
        return (f'{type(e).__name__}: {e}', 500)
    if summary is None:
        return ('2D microstructure unavailable (need atoms.csv + meta/params)', 404)
    png_path = _synth_2d_png_path(get_results_dir(case_id), seed)
    return send_file(png_path, mimetype='image/png', as_attachment=False,
                     download_name=f'microstructure_2d_{case_id}.png')


@app.route('/results/<case_id>/2d-geometry.png')
def serve_2d_geometry(case_id):
    """Clean geometry-only export of the LEFT phase map (4-phase raster +
    AM_P grain boundaries) — NO axes/ticks/labels/legend/title, high-res.
    Downloads as an attachment.  Stays in sync with the displayed figure."""
    px = max(200, min(1200, int(request.args.get('px', 600))))
    seed = int(request.args.get('seed', 0))
    geo_path = _synth_2d_png_path(get_results_dir(case_id), seed).replace('.png', '_geometry.png')
    force = request.args.get('fresh') in ('1', 'true', 'yes') or not os.path.exists(geo_path)
    try:
        summary = _synth_2d(case_id, px=px, seed=seed, force=force)
    except Exception as e:
        import traceback; traceback.print_exc()
        return (f'{type(e).__name__}: {e}', 500)
    if summary is None:
        return ('2D microstructure unavailable (need atoms.csv + meta/params)', 404)
    if not os.path.exists(geo_path):
        return ('geometry export unavailable', 404)
    return send_file(geo_path, mimetype='image/png', as_attachment=True,
                     download_name=f'microstructure_2d_geometry_{case_id}.png')


@app.route('/results/<case_id>/2d-summary.json')
def serve_2d_summary(case_id):
    """The cached figure's scalar summary (incl. the seed it was made with),
    so the client can keep the ZIP/regenerate in sync with what's shown."""
    p = os.path.join(get_results_dir(case_id), 'microstructure_2d_summary.json')
    if not os.path.exists(p):
        return jsonify({'exists': False}), 200
    try:
        with open(p) as f:
            s = json.load(f)
        s['exists'] = True
        return jsonify(s)
    except Exception:
        return jsonify({'exists': False}), 200


def _build_2d_readme(case_id, s):
    f = s.get('phase_fracs') or {}
    def g(k, d='—'):
        v = s.get(k)
        return d if v is None else v
    return f"""# 2D Representative Microstructure — {s.get('case_name', case_id)}

Procedurally synthesized from the 3D DEM statistics (NOT a literal slice).
A planar slice cannot show the true particle D50 and the correct area
fractions at the same time (Wicksell), so AM particles are placed with a
size distribution whose MEDIAN equals the analysis D50, at the measured
area fractions; SE forms a single connected matrix; porosity is carved to
the measured value; and the AM–SE coverage is matched separately for AM_P
and AM_S.

## Design parameters
- P:S (AM_P:AM_S): {g('ps_ratio')}  (weight; AM_P/AM_S are the same material,
  so weight ratio = volume ratio)
- AM_P D50 radius: {g('r_AM_P_d50_um')} um
- AM_S D50 radius: {g('r_AM_S_d50_um')} um
- electrode thickness: {g('thickness_um')} um

## Achieved (this figure)
- void (porosity): {f.get('void','—')} %
- AM_P: {f.get('AM_P','—')} %   AM_S: {f.get('AM_S','—')} %   SE: {f.get('SE','—')} %
- AM–SE coverage (all): {g('coverage_2d_pct')} %   (3D target {g('coverage_3d_target_pct')} %)
- AM_P coverage: {g('coverage_AM_P_pct')} %  (target {g('coverage_AM_P_target_pct')} %)
- AM_S coverage: {g('coverage_AM_S_pct')} %  (target {g('coverage_AM_S_target_pct')} %)
- domain: {g('a_extent')} x {g('b_extent')} um, {g('n_pixels')} px, {g('pa_um')} um/px

## Files in this archive
- microstructure_2d.png   — 4-phase microstructure (left) + AM–SE coverage (right)
- summary.csv             — all scalar metrics (key, value)
- phase_fractions.csv     — phase area fractions (%)

Coverage convention: covered = AM perimeter touching SE; uncovered = AM
perimeter facing void / another AM (interfacial pore).  Fully-inactive
particles occur only inside multi-particle clusters (held by neighbours);
isolated particles keep some SE contact (no floating particles).
"""


@app.route('/results/<case_id>/2d-export.zip')
def serve_2d_export_zip(case_id):
    """Bundle the full COMSOL-import package: geometry.dxf (vector domains +
    coverage-as-boundary layers), parameters.csv/json (3D effective materials),
    geometry.svg/png preview, microstructure.npy, phase_fractions.csv, and a
    README with COMSOL import steps."""
    import io as _io
    import zipfile
    import sys as _sys
    import importlib
    import tempfile
    px = max(200, min(1200, int(request.args.get('px', 600))))
    seed = int(request.args.get('seed', 0))
    case_dir = get_case_dir(case_id)
    results_dir = get_results_dir(case_id)
    if not os.path.exists(os.path.join(results_dir, 'atoms.csv')):
        return ('2D microstructure unavailable (need atoms.csv + meta/params)', 404)
    meta_file = os.path.join(case_dir, 'meta.json')
    case_name = case_id
    if os.path.exists(meta_file):
        try:
            case_name = json.load(open(meta_file)).get('name', case_id)
        except Exception:
            pass
    _scripts_dir = app.config['SCRIPTS_FOLDER']
    if _scripts_dir not in _sys.path:
        _sys.path.insert(0, _scripts_dir)
    out_dir = None
    try:
        import extract_2d_microstructure as ex2d
        import export_comsol_2d as expc
        ex2d = importlib.reload(ex2d)
        expc = importlib.reload(expc)
        sd, _gap = ex2d.synthesize_adaptive(Path(case_dir), n_pixels=px, seed=seed)
        if sd is None:
            return ('2D microstructure generation failed (missing meta/params)', 404)
        out_dir = tempfile.mkdtemp(prefix=f'comsol_{case_id}_')
        expc.write_comsol_package(case_name, Path(case_dir), sd, out_dir, axis='synth')
        # phase_fractions.csv (convenience; not in the package)
        fr = sd.get('phase_fracs') or {}
        with open(os.path.join(out_dir, 'phase_fractions.csv'), 'w') as f:
            f.write('phase,area_pct\n')
            for ph in ('void', 'AM_P', 'AM_S', 'SE'):
                f.write(f'{ph},{fr.get(ph, "")}\n')
        buf = _io.BytesIO()
        with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
            for fn in sorted(os.listdir(out_dir)):
                z.write(os.path.join(out_dir, fn), fn)
        buf.seek(0)
    except Exception as e:
        import traceback; traceback.print_exc()
        return (f'{type(e).__name__}: {e}', 500)
    finally:
        if out_dir:
            shutil.rmtree(out_dir, ignore_errors=True)
    return send_file(buf, mimetype='application/zip', as_attachment=True,
                     download_name=f'{case_name}_comsol_2d.zip')


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

def _save_case_to_archive(case_id, folder=''):
    """Copy a live case (results + meta + raw uploads) into the archive
    (보관함) so it survives results/uploads being cleared, and sync to remote.
    Returns (save_dir, None) on success or (None, error_message)."""
    results_dir = get_results_dir(case_id)
    case_dir = get_case_dir(case_id)
    meta_file = os.path.join(case_dir, 'meta.json')
    if not os.path.exists(meta_file):
        return None, '케이스를 찾을 수 없습니다.'
    with open(meta_file) as f:
        meta = json.load(f)
    case_name = meta.get('name', case_id)
    dst = _safe_path(folder) if folder else _archive_root()
    if not dst:
        return None, '잘못된 경로입니다.'
    save_dir = os.path.join(dst, case_name)
    if os.path.exists(save_dir):
        save_dir = save_dir + '_' + datetime.now().strftime('%H%M%S')
    shutil.copytree(results_dir, save_dir, dirs_exist_ok=True)
    shutil.copy2(meta_file, os.path.join(save_dir, 'meta.json'))
    raw_dir = os.path.join(save_dir, 'raw_files')
    os.makedirs(raw_dir, exist_ok=True)
    for fname in os.listdir(case_dir):
        fpath = os.path.join(case_dir, fname)
        if os.path.isfile(fpath) and fname != 'meta.json':
            shutil.copy2(fpath, os.path.join(raw_dir, fname))
    rel = os.path.relpath(save_dir, app.config['ARCHIVE_FOLDER'])
    storage_sync.sync_dir_to_remote(save_dir, f'archive/{rel}')
    return save_dir, None


@app.route('/archive/save-case', methods=['POST'])
def archive_save_case():
    """Save a case's results to archive folder."""
    save_dir, err = _save_case_to_archive(request.form.get('case_id', ''),
                                          request.form.get('folder', ''))
    if err:
        return jsonify({'error': err}), (404 if '찾을' in err else 400)
    return jsonify({'success': True, 'saved_to': save_dir})


@app.route('/group/save-cases', methods=['POST'])
def group_save_cases():
    """Save all selected LOCAL cases in the group view to the archive in one
    click (archive: cases are already persisted, so they're skipped)."""
    case_ids = request.form.getlist('cases')
    folder = request.form.get('folder', '')
    saved, skipped, errors = [], 0, []
    for cid in case_ids:
        cid = (cid or '').strip()
        if not cid or cid.startswith('archive:'):
            skipped += 1
            continue
        try:
            sd, err = _save_case_to_archive(cid, folder)
            if err:
                errors.append(f'{cid}: {err}')
            else:
                saved.append(os.path.basename(sd))
        except Exception as e:
            errors.append(f'{cid}: {type(e).__name__}: {e}')
    return jsonify({'success': True, 'saved': saved,
                    'skipped': skipped, 'errors': errors})

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

        cmd = [sys.executable, os.path.join(scripts, 'parse_liggghts.py')]
        cmd += atom_files + contact_files + mesh_files + input_files + ['-o', target]
        subprocess.run(cmd, capture_output=True, text=True, timeout=None)

        atoms_csv = os.path.join(target, 'atoms.csv')
        contacts_csv = os.path.join(target, 'contacts.csv')
        script = 'analyze_contacts_bimodal.py' if mode == 'bimodal' else 'analyze_contacts.py'
        cmd = [sys.executable, os.path.join(scripts, script),
               atoms_csv, contacts_csv, '-o', target,
               '-t', type_map, '-s', str(scale)]
        subprocess.run(cmd, capture_output=True, text=True, timeout=None)

        # Dual-mode (Hertzian vs Physics) coverage + path-hop metrics.
        # Uses --case-dir because archive layouts can be nested under
        # webapp/archive/<category>/<case>, so find_case_dir(basename) may fail.
        cmd = [sys.executable, os.path.join(scripts, 'coverage_physics_vs_hertzian.py'),
               '--case-dir', target]
        subprocess.run(cmd, capture_output=True, text=True, timeout=None)

        # Stage E (literature-grounded grain corrections) — MUST run after
        # analyze_contacts so the baseline σ_* keys exist for Cronau /
        # Trevisanello / Wang multipliers to scale against.  Same call shape
        # as the /analyze pipeline (line ~2291).  Auto-writes σ_*_stage_e
        # AND the validation_flags self-report card → Trust card on the
        # single.html page header is populated immediately.
        try:
            stage_e_cmd = [sys.executable,
                            os.path.join(scripts, 'run_network_full_corrections.py'),
                            os.path.basename(target), '--quiet']
            subprocess.run(stage_e_cmd, capture_output=True, text=True,
                            timeout=None)
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

    # Summary tables + metrics + input_params (shared with /single + report)
    tables, metrics, input_params = _load_case_tables(results_dir, meta)

    return render_template('single.html', case=meta, figures=figures,
                         report=report, tables=tables, metrics=metrics,
                         input_params=input_params, archive_path=folder,
                         mpm_metrics=_load_mpm_metrics(results_dir),
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

    # Vectorized build (iterrows is ~100x slower and dominates load time on
    # particulate cases with 10^5+ atoms).
    ids = df['id'].astype('int64').tolist()
    ts = df['type'].astype('int64').tolist()
    xs = (df['x'] * scale).round(2).tolist()
    ys = (df['y'] * scale).round(2).tolist()
    zs = (df['z'] * scale).round(2).tolist()
    rs = (df['radius'] * scale).round(2).tolist()
    _tname = {}
    particles = []
    for i in range(len(ids)):
        t = ts[i]
        nm = _tname.get(t)
        if nm is None:
            nm = type_map.get(t, f'T{t}'); _tname[t] = nm
        particles.append({'id': ids[i], 'type': nm,
                          'x': xs[i], 'y': ys[i], 'z': zs[i], 'r': rs[i]})

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
        'se_states': {}, 'tabor_stats': {}, 'all_se_ids_count': 0,
        'se_engagement': {},
        'cluster_meta': {}, 'cluster_id_per_se': {},
        'coverage_per_am': {},
        # Phase A1/A3/A4 — per-particle fracture aggregates + stress chain
        'particle_max_fpc': {}, 'particle_worst_stage': {},
        'particle_n_brittle': {}, 'particle_worst_partner_brittle': {},
        'particle_worst_pair_type': {},
        'am_p_skeleton': [], 'stress_chain_segments': [],
        # Phase A5+A6 — SE network diagnostics
        'se_percolating': [], 'se_articulation_points': [],
        'se_bottleneck_edges': [], 'se_dead_end_clusters': [],
        'se_n_percolating': 0,
        'se_bn_median_norm': 0, 'se_bn_threshold_norm': 0,
        'se_n_bn_below_threshold': 0,
    }
    try:
        import sys as _sys
        _scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
        if _scripts_dir not in _sys.path:
            _sys.path.insert(0, _scripts_dir)
        from viewer3d_data import (
            aggregate_particle_metrics, classify_clusters,
            build_cluster_id_map, build_coverage_map,
            compute_se_network_diagnostics,
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
                    if cached.get('_contacts_mtime') == contacts_mtime and cached.get('_schema') == 11:
                        for k in ('stress_max', 'dr_max', 'brittle_pairs',
                                   'se_stress_pairs', 'am_se_stress_pairs',
                                   'se_states', 'tabor_stats', 'all_se_ids_count',
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
                    aux['all_se_ids_count']   = agg.get('all_se_ids_count', 0)
                    aux['se_engagement']      = agg.get('se_engagement', {})
                    # Phase A1/A3/A4
                    aux['particle_max_fpc']         = agg.get('particle_max_fpc', {})
                    aux['particle_worst_stage']     = agg.get('particle_worst_stage', {})
                    aux['particle_n_brittle']       = agg.get('particle_n_brittle', {})
                    aux['particle_worst_partner_brittle'] = agg.get('particle_worst_partner_brittle', {})
                    aux['particle_worst_pair_type'] = agg.get('particle_worst_pair_type', {})
                    aux['am_p_skeleton']            = agg.get('am_p_skeleton', [])
                    aux['stress_chain_segments']    = agg.get('stress_chain_segments', [])
                    # Phase A5+A6 — SE network diagnostics
                    try:
                        _plate_z_sim = box.get('z_max', 0) / max(scale, 1)
                        _se_diag = compute_se_network_diagnostics(
                            _stream_records(contacts_df), atoms_by_id,
                            type_map, plate_z=_plate_z_sim, scale=scale)
                        aux['se_percolating']           = _se_diag.get('percolating_se', [])
                        aux['se_articulation_points']   = _se_diag.get('articulation_points', [])
                        aux['se_bottleneck_edges']      = _se_diag.get('bottleneck_edges', [])
                        aux['se_dead_end_clusters']     = _se_diag.get('dead_end_clusters', [])
                        aux['se_n_percolating']         = _se_diag.get('n_percolating', 0)
                        aux['se_bn_median_norm']        = _se_diag.get('bn_median_norm', 0)
                        aux['se_bn_threshold_norm']     = _se_diag.get('bn_threshold_norm', 0)
                        aux['se_n_bn_below_threshold']  = _se_diag.get('n_bn_below_threshold', 0)
                        aux['se_n_perc_edges']          = _se_diag.get('n_perc_edges', 0)
                    except Exception as _ediag:
                        print(f'  [3d-data aux/archive] SE diag failed: {_ediag}')
                    try:
                        cache_blob = dict(aux)
                        cache_blob['_contacts_mtime'] = contacts_mtime; cache_blob['_schema'] = 11
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

    payload = {
        'particles': particles, 'box': box,
        'percolation': percolation, 'paths': paths, 'clusters': clusters,
        'mesh_triangles': mesh_triangles,
        'atoms_only': atoms_only_mode,
        'aux': aux,
    }
    try:
        resp = jsonify(payload)
        body = resp.get_data()
        print(f'  [3d-data/archive] response: {len(body)/1e6:.2f} MB')
        return resp
    except (TypeError, ValueError) as _je:
        import traceback
        traceback.print_exc()
        print(f'  [3d-data/archive] jsonify FAILED — dropping aux')
        payload['aux'] = {}
        payload['_aux_error'] = f'{type(_je).__name__}: {_je}'[:200]
        return jsonify(payload)
    except Exception as _je:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(_je)[:300],
                         'particles': [], 'aux': {},
                         'box': box, 'atoms_only': True}), 200


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
    """Yield (display_id, url, results_dir, archive_rel) for each case that has
    a full_metrics.json, de-duplicated by case NAME across results + archive.
    A case present in both a local results dir and the archive (or under both an
    id- and a name-keyed entry) is listed ONCE; the live local results copy is
    preferred over the archived one."""
    out = []
    seen = set()                       # canonical case names already added
    results_root = app.config.get('RESULTS_FOLDER')
    archive_root = app.config.get('ARCHIVE_FOLDER')

    def _canon(name):
        return (name or '').strip().lower()

    def _results_name(case_id, results_dir):
        for p in (os.path.join(app.config['UPLOAD_FOLDER'], case_id, 'meta.json'),
                  os.path.join(results_dir, 'meta.json')):
            if os.path.exists(p):
                try:
                    nm = json.load(open(p)).get('name')
                    if nm:
                        return nm
                except Exception:
                    pass
        return case_id

    # local results FIRST (live/current copy preferred over an archived one)
    if results_root and os.path.isdir(results_root):
        for case_id in sorted(os.listdir(results_root)):
            d = os.path.join(results_root, case_id)
            if not (os.path.isdir(d)
                    and os.path.exists(os.path.join(d, 'full_metrics.json'))):
                continue
            nm = _results_name(case_id, d)
            key = _canon(nm)
            if key in seen:
                continue
            seen.add(key)
            out.append((nm, url_for('single', case_id=case_id), d, None))

    # archive cases — only if that NAME isn't already shown from results
    if archive_root and os.path.isdir(archive_root):
        for dirpath, _, files in os.walk(archive_root):
            if 'full_metrics.json' in files and 'atoms.csv' in files:
                rel = os.path.relpath(dirpath, archive_root)
                nm = os.path.basename(dirpath)
                key = _canon(nm)
                if key in seen:
                    continue
                seen.add(key)
                out.append((nm, url_for('archive_view', folder=rel), dirpath, rel))
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
    cmd = [sys.executable, os.path.join(scripts, 'generate_fitting_report.py'),
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
    cmd = [sys.executable, os.path.join(scripts, 'generate_scaling_report.py')]
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


@app.route('/predictor/structure/status')
def predictor_structure_status():
    """구조 예측기(sklearn 불요) 상태 + 타깃별 판정표."""
    try:
        return jsonify(structure_predictor.status())
    except Exception as e:                                     # noqa: BLE001 — 항상 JSON
        return jsonify({'ready': False, 'error': f'{type(e).__name__}: {e}'}), 200


@app.route('/predictor/structure', methods=['POST'])
def predictor_structure():
    """설계 6 노브 → 구조 (판정·PI·외삽 게이트 포함).  REJECT 타깃은 안 내보낸다."""
    d = request.get_json() or {}
    try:
        return jsonify(structure_predictor.predict_structure(
            d_se=float(d.get('d_se', 1.0)), d_am=float(d.get('d_am', 5.0)),
            am_pct=float(d.get('am_pct', 80.0)), ps_frac=float(d.get('ps_frac', 0.5)),
            rve=float(d.get('rve', 50.0)), loading=float(d.get('loading', 6.0)),
            include_weak=bool(d.get('include_weak', True))))
    except Exception as e:                                     # noqa: BLE001
        return jsonify({'ready': False, 'error': f'{type(e).__name__}: {e}'}), 200


@app.route('/predictor/structure/suggest')
def predictor_structure_suggest():
    """다음 DEM 배치 제안 (순차 D-최적)."""
    try:
        return jsonify(structure_predictor.suggest_batch(
            n=int(request.args.get('n', 10)),
            target=request.args.get('target', 'tau'),
            allow_weak=request.args.get('allow_weak', '') in ('1', 'true', 'yes')))
    except Exception as e:                                     # noqa: BLE001
        return jsonify({'error': f'{type(e).__name__}: {e}', 'rows': []}), 200


@app.route('/predictor/train')
def predictor_train():
    """Train GPR models from existing data.  sklearn 부재(클라우드) 시 raw 500 대신 JSON 안내."""
    try:
        result = predictor_engine.train_models(
            app.config['RESULTS_FOLDER'], app.config['ARCHIVE_FOLDER'])
    except ImportError as e:                                   # sklearn/joblib 미설치 → WSL 안내
        return jsonify({'success': False,
                        'error': f'학습 라이브러리 미설치 ({e}) — WSL/로컬서 pip install scikit-learn joblib 후 학습'}), 200
    except Exception as e:                                     # 그 외도 JSON (JS "Unexpected token <" 방지)
        return jsonify({'success': False, 'error': f'{type(e).__name__}: {e}'}), 200
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
            # ★온도 규약 (docs/temp_pressure_capability.md T1-c/T1-e): σ_e 는 기본 T-무관
            #   ('none' = 문헌 Reisacher + 솔버 정합).  'legacy_arrhenius' 는 2026-07-28 이전
            #   Ea_AM=0.50 eV('rough', 미앵커 §F1) 재현용.  ea_ion_ev 는 밴드 스윕(0.29/0.41/0.46)용
            #   — 미지정이면 엔진 기본(0.41) → 요청에 안 실으면 동작 불변.
            sigma_e_t_model=str(data.get('sigma_e_t_model', 'none')),
            ea_ion_ev=(float(data['ea_ion_ev']) if data.get('ea_ion_ev') not in (None, '') else None),
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
    # debug OFF by default — host=0.0.0.0 exposes the app, and Flask's debug=True enables the
    # Werkzeug debugger (remote code execution on a public IP).  Opt in locally with FLASK_DEBUG=1.
    debug = os.environ.get('FLASK_DEBUG', '').lower() in ('1', 'true', 'yes', 'on')
    app.run(debug=debug, host='0.0.0.0', port=port)
