#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""②b TAU-03 — 등급 τ · overhead 축 = Hertz 원 솔버 σ + 짝 σ₀ (한 도우미) · COMSOL 2D 두 모드 행 · regime DB · 웹앱 같은 묶음.

1저자 비준 10-04 밤 (*"권고대로 진행해"*): ① 등급 τ · overhead 축 = Hertz · 이름 "(Hertz)" · 문턱 "내부 등급선" · σ₀ = 웹앱과 같은 짝 σ₀
(L4-04 함께 닫힘) ② COMSOL 2D = Hertz · physics 두 모드 행 (`f_ion_<mode>` · `tau2_ion_<mode>`) + Stage-E σ 는 τ 이름 없이 "재료 인자 포함" 행
③ ④a/④b 축 전환 보류 ④ ASR · σ_ionic Stage E 축은 τ 가 아니라 그대로.  근거 = τ 판정 v2 결정 6 · 결정 11 (FULL/CF 이름) · TAU-03 · TAU-16 · L4-04.

  G  등급 엔진
     G1 같은 metrics → 등급 τ = 웹앱 τ 블록 Hertz 칸 (stage_e_physics ≠ physics ≠ hertz 합성 — 옛 코드는 stage_e_physics 를 골랐다)
     G2 σ (σ_full · σ_bulk) 와 짝 provenance 배수를 함께 ×4 → 등급 τ · τ_bulk · overhead 불변 (L4-04 · Codex 반례 3.4641 → 1.7321)
     G3 Stage-E 키만 있는 metrics → τ · overhead 축 값 없음 (Stage-E 값에 τ 이름을 붙이지 않는다 · 결정 6)
     G4 overhead = √(σ_bulk_net / σ_full,H) — 분자 · 분모 같은 망 · 같은 모드 (옛 = 분자 Stage-E physics ÷ 분모 raw CF · TAU-08)
     G5 축 이름표 · 식 · 설명 — "(Hertz)" · 짝 σ₀ · 내부 등급선 · "Stage E physics 우선" · "3.0 고정" 없음 · overhead = 모델 내부 협착 비 (원기둥 bulk 기준)
     G6 τ 세 축 계산부에 σ₀ 리터럴 3.0 이 없다 (한 도우미 경유)
     G7 헤더 문턱 출처 — "τ_Laplace,eff ≤ 2.5 — Tippens 2019, Famprikis 2019" 를 근거처럼 적지 않는다 (내부 등급선 · TAU-16)
     G8 ASR 축 · σ_ionic Stage E 축은 그대로 (Stage-E physics σ 우선 — τ 아님 · 범위 밖)
  W  웹앱
     W1 `_sigma_grain_context` = se_material.sigma_grain_context (온도 키 조합 여섯 — 값 · 경고 같음)
     W2 τ 블록 tau2 = 같은 도우미 (`tau_flux.tau2_value`) — 값 비트 동일
     W3 쉬운 툴팁 __tau_lap_eff — Hertz · 짝 σ₀ 를 말한다
  C  COMSOL 2D 내보내기
     C1 f_ion_hertz · f_ion_physics = σ_mode/σ₀ · tau2_ion_<mode> = φ·σ₀/σ_mode (= φ/f) · tau_ion_<mode> = √ · 단위 1
     C2 physics σ 없음 → physics 행 빈칸 (Hertz 복사 없음 · TAU-21 규칙)
     C3 Stage-E 행 = `sigma_ionic_stage_e` · 설명 "재료 인자 포함" · 옛 `tau2` · `f_ion` · `tau_Laplace_eff` · `sigma_ionic_eff` 행 없음 (Stage-E 로 만든 τ 없음)
     C4 σ₀ 행 = 짝 σ₀ (온도 런이면 배수 · tau2 · f 와 같은 σ₀)
     C5 README [B] — 모드별 행 · `sigma_i_stageE` 는 f · tau2 와 짝이 아니라는 경고
  R  regime DB — τ_Lap,eff · τ_Lap,geom = 같은 도우미 (Hertz · 짝 σ₀) · 25 °C 값 불변

  python3 webapp/test_tau_grade_unify.py
"""
import ast
import json
import math
import os
import sys
import tempfile
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'scripts'))

_ok, _fail = 0, []


def chk(name, cond, why=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'  ({why})' if why else ''))
    return cond


def _read(rel):
    with open(os.path.join(ROOT, rel), encoding='utf-8') as f:
        return f.read()


import grade_engine as GE   # noqa: E402
import se_material as SEM   # noqa: E402


def axis(key):
    return next((a for a in GE.AXES if a.get('key') == key), None)


def text(ax):
    return ' '.join(str(ax.get(k, '')) for k in ('label', 'formula', 'meaning')) if ax else ''


# 합성 metrics — 세 σ 가 서로 다르다 (stage_e_physics 0.20 · physics 0.30 · hertz 0.12)
BASE = {'phi_se': 0.30, 'sigma_full_mScm': 0.12, 'sigma_full_mScm_physics': 0.30,
        'sigma_full_mScm_stage_e_physics': 0.20, 'sigma_full_mScm_stage_e': 0.11,
        'sigma_bulk_net_mScm': 0.50, 'thickness_um': 80.0}
SIG0 = SEM.SIGMA_GRAIN_MS_CM_25C

# ── G  등급 엔진 ──────────────────────────────────────────────────────────────
print('G  등급 엔진')
t_h = math.sqrt(0.30 * SIG0 / 0.12)
v1 = GE._derived_value('__tau_lap_eff', dict(BASE))
chk('G1 등급 τ = √(φ·σ₀/σ_full,H) (= 웹앱 τ 블록 Hertz 칸) — Stage-E · physics 를 고르지 않는다',
    v1 is not None and abs(v1 - t_h) < 1e-12, f'{v1} vs {t_h}')

PROV4 = {'sigma_ion_T_factor': 4.0, 'T_C': 60.0}
M4 = dict(BASE)
for k in ('sigma_full_mScm', 'sigma_full_mScm_physics', 'sigma_bulk_net_mScm'):
    M4[k] = BASE[k] * 4.0
M4['temperature_provenance'] = PROV4
G2v = [(GE._derived_value(k, dict(BASE)), GE._derived_value(k, M4))
       for k in ('__tau_lap_eff', '__tau_lap_bulk', '__constriction_overhead')]
chk('G2 σ 와 짝 provenance 배수를 함께 ×4 → τ · τ_bulk · overhead 불변 (L4-04 · 공통 스케일 불변성)',
    all(a is not None and b is not None and abs(a - b) < 1e-12 for a, b in G2v), repr(G2v))

M3 = {'phi_se': 0.30, 'sigma_full_mScm_stage_e_physics': 0.20, 'sigma_full_mScm_stage_e': 0.11, 'sigma_bulk_net_mScm': 0.50}
G3v = (GE._derived_value('__tau_lap_eff', M3), GE._derived_value('__constriction_overhead', M3))
chk('G3 Stage-E 키만 있으면 τ · overhead 축 값 없음 (Stage-E 값에 τ 이름 없음 · 결정 6)', G3v == (None, None), repr(G3v))

ov = GE._derived_value('__constriction_overhead', dict(BASE))
chk('G4 overhead = √(σ_bulk_net/σ_full,H) — 같은 망 · 같은 모드 (FULL ÷ CF)',
    ov is not None and abs(ov - math.sqrt(0.50 / 0.12)) < 1e-12, f'{ov}')

ax_t, ax_b, ax_o = axis('__tau_lap_eff'), axis('__tau_lap_bulk'), axis('__constriction_overhead')
chk('G5a τ 축 — "(Hertz)" · 짝 σ₀ · 내부 등급선 · "Stage E physics 우선" · "3.0 고정" 없음',
    ax_t is not None and '(Hertz)' in ax_t['label'] and '짝 σ₀' in text(ax_t) and '내부 등급선' in text(ax_t)
    and 'Stage E physics 우선' not in text(ax_t) and '3.0 고정' not in text(ax_t), text(ax_t)[:240])
chk('G5b τ_bulk 축 — 짝 σ₀ · "3.0 고정" 없음 · Dijkstra 대체 열 아님 유지',
    ax_b is not None and '짝 σ₀' in text(ax_b) and '3.0 고정' not in text(ax_b) and 'Dijkstra' in text(ax_b), text(ax_b)[:240])
chk('G5c overhead 축 — "모델 내부 협착 비" · "원기둥 bulk" · Hertz · √저항비 · 물리 협착 배수 아님',
    ax_o is not None and '모델 내부 협착 비' in ax_o['label'] and '원기둥 bulk' in text(ax_o) and 'Hertz' in text(ax_o)
    and '√' in text(ax_o) and '물리 협착 배수' in text(ax_o), text(ax_o)[:240])

GSRC = _read('scripts/grade_engine.py')
_tree = ast.parse(GSRC)
_dv = next(n for n in ast.walk(_tree) if isinstance(n, ast.FunctionDef) and n.name == '_derived_value')
_tau_lits = []
for n in ast.walk(_dv):
    if isinstance(n, ast.If) and isinstance(n.test, ast.Compare) and isinstance(n.test.comparators[0], ast.Constant) \
            and n.test.comparators[0].value in ('__tau_lap_eff', '__tau_lap_bulk', '__constriction_overhead'):
        for c in ast.walk(n):
            if isinstance(c, ast.Constant) and c.value == 3.0:
                _tau_lits.append((n.test.comparators[0].value, getattr(c, 'lineno', '?')))
chk('G6 τ 세 축 계산부에 σ₀ 리터럴 3.0 없음 (한 도우미 경유)', not _tau_lits, repr(_tau_lits))
_hdr = GSRC[:GSRC.find('"""', 3)]
chk('G7 헤더 — "τ_Laplace,eff ≤ 2.5 — Tippens 2019, Famprikis 2019" 를 근거처럼 적지 않음 · 내부 등급선 (TAU-16)',
    'τ_Laplace,eff ≤ 2.5         — Tippens 2019, Famprikis 2019' not in _hdr and '내부 등급선' in _hdr, _hdr[:0])
asr = GE._derived_value('__asr_ionic_Ohm_cm2', dict(BASE))
ax_s = axis('sigma_full_mScm_stage_e_physics')
chk('G8 ASR · σ_ionic Stage E 축은 그대로 — Stage-E physics σ 우선 (τ 아님 · 범위 밖)',
    asr is not None and abs(asr - 80.0 * 0.1 / 0.20) < 1e-12 and ax_s is not None, f'{asr}')

# ── W  웹앱 ───────────────────────────────────────────────────────────────────
print('W  웹앱')
import app as webapp   # noqa: E402
CASES = [None, {}, {'temperature_provenance': {'sigma_ion_T_factor': 1.0}},
         {'temperature_provenance': {'sigma_ion_T_factor': 2.5}},
         {'temperature_provenance': {'sigma_ion_T_factor': 1.0},
          'stage_e_temperature_provenance': {'sigma_ion_T_factor': 4.44, 'T_C': 60}},
         {'sigma_grain_S_cm': 0.0045}]
_shared = getattr(SEM, 'sigma_grain_context', None)
W1 = [(webapp._sigma_grain_context(c), _shared(c) if _shared else None) for c in CASES]
chk('W1 웹앱 _sigma_grain_context = se_material.sigma_grain_context (온도 키 조합 여섯 · 값 · 경고 같음)',
    _shared is not None and all(a == b for a, b in W1), repr(W1[:2]))
_tb = ast.parse(_read('webapp/app.py'))
_fn = next((n for n in ast.walk(_tb) if isinstance(n, ast.FunctionDef) and n.name == '_tau_block_rows'), None)
_calls = {getattr(c.func, 'attr', getattr(c.func, 'id', None)) for c in ast.walk(_fn) if isinstance(c, ast.Call)} if _fn else set()
rows = webapp._tau_block_rows(0.30, SIG0, 0.12, 0.30, 0.50, 1.5, None)
t2row = next((r for r in rows if isinstance(r[0], str) and r[0].startswith('tau2')), None)
chk('W2 τ 블록 tau2 = 같은 도우미 (tau2_value) · 값 = φ·σ₀/σ (H · P) 반올림 3 자리 그대로',
    'tau2_value' in _calls and t2row is not None and float(t2row[1]) == round(0.30 * SIG0 / 0.12, 3)
    and float(t2row[2]) == round(0.30 * SIG0 / 0.30, 3), f'calls={sorted(c for c in _calls if c)[:8]} row={t2row}')
ASRC = _read('webapp/app.py')
_i = ASRC.find("'__tau_lap_eff': '")
easy = ASRC[_i:_i + 600] if _i >= 0 else ''
chk('W3 쉬운 툴팁 __tau_lap_eff — Hertz · 짝 σ₀ 언급', 'Hertz' in easy and '짝' in easy, easy[:200])

# ── C  COMSOL 2D 내보내기 ─────────────────────────────────────────────────────
print('C  COMSOL 2D 내보내기')
import export_comsol_2d as EC   # noqa: E402


def _rows(fm):
    with tempfile.TemporaryDirectory() as td:
        cid = 'caseX'
        d = Path(td) / 'webapp' / 'results' / cid
        d.mkdir(parents=True)
        (d / 'full_metrics.json').write_text(json.dumps(fm))
        _old = EC.ROOT
        try:
            EC.ROOT = Path(td)
            out = EC.numerical_parameters(Path(td) / cid, {'phase_fracs': {'SE': 30.0, 'void': 15.0}, 'coverage_2d_pct': 50.0})
        except Exception as e:   # noqa: BLE001
            print('    numerical_parameters 실패:', type(e).__name__, e)
            out = []
        finally:
            EC.ROOT = _old
    return {r['parameter']: r for r in out}


by = _rows(dict(BASE))


def _v(name, rows=None):
    r = (rows or by).get(name)
    return float(r['value']) if (r and r.get('value') not in ('', None)) else None


ok_c1 = all(_v(n) is not None for n in ('f_ion_hertz', 'f_ion_physics', 'tau2_ion_hertz', 'tau2_ion_physics', 'tau_ion_hertz', 'tau_ion_physics'))
if ok_c1:
    ok_c1 = (_v('f_ion_hertz') == round(0.12 / SIG0, 6) and _v('f_ion_physics') == round(0.30 / SIG0, 6)
             and _v('tau2_ion_hertz') == round(0.30 * SIG0 / 0.12, 6) and _v('tau2_ion_physics') == round(0.30 * SIG0 / 0.30, 6)
             and _v('tau_ion_hertz') == round(math.sqrt(0.30 * SIG0 / 0.12), 6)
             and all(by[n]['unit'] == '1' for n in ('f_ion_hertz', 'tau2_ion_physics')))
chk('C1 f_ion_<mode> = σ_mode/σ₀ · tau2_ion_<mode> = φ·σ₀/σ_mode · tau_ion_<mode> = √ · 단위 1', ok_c1,
    repr({k: by.get(k, {}).get('value') for k in ('f_ion_hertz', 'f_ion_physics', 'tau2_ion_hertz', 'tau2_ion_physics')}))
fm2 = dict(BASE); fm2.pop('sigma_full_mScm_physics')
by2 = _rows(fm2)
chk('C2 physics σ 없음 → physics 행 빈칸 (Hertz 복사 없음)',
    all(n in by2 and by2[n]['value'] == '' for n in ('f_ion_physics', 'tau2_ion_physics', 'tau_ion_physics', 'sigma_ionic_physics'))
    and _v('f_ion_hertz', by2) is not None, repr({k: by2.get(k, {}).get('value') for k in ('f_ion_physics', 'tau2_ion_physics')}))
se_row = by.get('sigma_ionic_stage_e')
chk('C3 Stage-E 행 = sigma_ionic_stage_e · 설명 "재료 인자 포함" · 옛 tau2 · f_ion · tau_Laplace_eff · sigma_ionic_eff 행 없음',
    se_row is not None and _v('sigma_ionic_stage_e') == 0.20 and '재료 인자 포함' in se_row['source']
    and not any(n in by for n in ('tau2', 'f_ion', 'tau_Laplace_eff', 'sigma_ionic_eff')), repr(sorted(by)[:12]))
fm4 = dict(M4)
by4 = _rows(fm4)
chk('C4 σ₀ 행 = 짝 σ₀ (온도 런 ×4) · 그 σ₀ 로 f · tau2 (σ 와 같이 ×4 → f · tau2 불변)',
    _v('sigma_grain', by4) == round(SIG0 * 4.0, 6) and _v('tau2_ion_hertz', by4) == _v('tau2_ion_hertz')
    and _v('f_ion_hertz', by4) == _v('f_ion_hertz'), repr((_v('sigma_grain', by4), _v('tau2_ion_hertz', by4))))
ESRC = _read('scripts/export_comsol_2d.py')
_rb = ESRC[ESRC.find('[B] MATERIAL — Global'):ESRC.find('[C] BOUNDARY — coverage')]
chk('C5 README [B] — 모드별 행 (f_ion_hertz · tau2_ion_hertz · physics) · sigma_i_stageE 짝 아님 경고',
    all(k in _rb for k in ('f_ion_hertz', 'tau2_ion_hertz', 'f_ion_physics', 'sigma_i_stageE')) and '짝이 아니' in _rb, _rb[:300])

# ── R  regime DB ──────────────────────────────────────────────────────────────
print('R  regime DB')
import build_tau_regime_db as RDB   # noqa: E402
RSRC = _read('scripts/build_tau_regime_db.py')
with tempfile.TemporaryDirectory() as td:
    p = Path(td) / 'caseR'
    p.mkdir()
    (p / 'full_metrics.json').write_text(json.dumps(dict(BASE, tortuosity_mean=1.5)))
    try:
        rec = RDB.load_case(str(p))
    except Exception as e:   # noqa: BLE001
        rec = None
        print('    regime 행 실패:', type(e).__name__, e)
chk('R1 regime DB — tau2 도우미 경유 (tau2_from_metrics · 짝 σ₀) · 25 °C τ_Lap,eff = √(φ·3.0/σ_full,H) 그대로',
    'tau2_from_metrics' in RSRC and rec is not None and float(rec.get('tau_Lap_eff')) == round(t_h, 3)   # DB = 소수 3 자리
    and float(rec.get('tau_Lap_geom')) == round(math.sqrt(0.30 * SIG0 / 0.50), 3),
    repr(rec and {k: rec.get(k) for k in ('tau_Lap_eff', 'tau_Lap_geom')}))

print(f'\n{_ok} PASS · {len(_fail)} FAIL')
if _fail:
    for n in _fail:
        print('  -', n)
    sys.exit(1)
