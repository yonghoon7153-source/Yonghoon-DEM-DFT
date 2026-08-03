#!/usr/bin/env python3
"""structure_predictor — webapp 추론 어댑터: 설계 6 노브 → 구조 (sklearn 불요).

왜 이 모듈이 따로 있나
──────────────────────
`predictor_engine` 의 GPR/RF 경로는 **sklearn 이 있어야** 학습된다.  배포 호스트엔 없어서
예측기 페이지가 영구 "Not Trained" 였다.  이쪽은 `scripts/ml_design_structure.py` 가 떨군
계수 JSON 만 읽어 **numpy 로만** 추론한다 — 학습은 WSL, 서빙은 아무 데서나.

두 경로는 **대체가 아니라 분업**이다:
  · predictor_engine (GPR)  : 타깃 폭이 넓다.  sklearn 있는 곳에서만.
  · 이 모듈 (ridge JSON)     : 타깃은 좁지만 **판정·PI·외삽 게이트**가 붙어 있고 어디서나 돈다.

정직 규약 (§F1)
  · nested 기준 판정이 REJECT 인 타깃은 **내보내지 않는다**.
  · 학습 볼록포 밖 질의는 값과 함께 `extrapolation` 을 달아 보낸다 — 조용히 답하지 않는다.
  · porosity 는 회귀하지 않고 **ε = C − φ_SE − φ_AM** 로 계산한다.  게이트된
    `use_porosity_pct` 는 같은 행의 φ 와 다른 모델에서 와서 (닫힘 잔차 sd 가 ε sd 의 78 %)
    한 물리상태가 아니다 — 그 열은 아예 안 쓴다.
    ε 의 오차띠는 전파-가정이 아니라 학습 때 **측정한** 폴드-밖 잔차 sd 를 쓴다.
"""

import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if os.path.join(_ROOT, 'scripts') not in sys.path:
    sys.path.insert(0, os.path.join(_ROOT, 'scripts'))

# 사람이 읽을 이름 + 단위 (없는 타깃은 키 그대로 보여준다)
LABELS = {
    'phi_se': ('φ_SE  SE 부피분율', ''),
    'phi_am': ('φ_AM  AM 부피분율', ''),
    'cn': ('CN  SE-SE 배위수', ''),
    'am_cn': ('CN_AM  AM-AM 배위수', ''),
    'coverage': ('coverage  AM 표면 SE 피복', ''),
    'tau': ('τ  굴곡도', ''),
    'f_perc': ('f_perc  퍼콜레이션 분율', ''),
    'thickness': ('두께', 'µm'),
    'se_of_solid_pct': ('고체 중 SE 몫', '%'),
    'mpm_plastic_gain_AM_P_tabor_pp': ('MPM 소성 피복 증분 (AM_P, Tabor)', '%p'),
    'mpm_dg_mean': ('MPM 평균 소성변형', ''),
}
# 이 열은 절대 내보내지 않는다 — 게이트가 φ 와 다른 모델을 섞어 한 물리상태가 아니다
FORBIDDEN = ('use_porosity_pct',)

# ★ 물리적 하드 경계 — 가우시안 PI 는 이걸 모른다.
#   실제로 mpm_dg_mean 의 90 % PI 하한이 **−0.018** (음의 소성변형)로 나왔다.  선형-가우시안
#   모형이 하한 0 인 양에 붙으면 생기는 일이다.  참값이 경계 밖일 수 없다는 건 사전지식이므로
#   **띠는 잘라서 보이고, 잘랐다고 표시한다** — 잘린 사실 자체가 "여기서 적합이 헐겁다" 는 정보다.
#   점추정은 자르지 않는다 (점추정이 경계를 넘으면 그건 숨기면 안 되는 실패다).
BOUNDS = {
    'phi_se': (0.0, 1.0), 'phi_am': (0.0, 1.0), 'coverage': (0.0, 1.0),
    'f_perc': (0.0, 100.0), 'se_of_solid_pct': (0.0, 100.0),
    'tau': (1.0, None),                 # 굴곡도는 정의상 ≥ 1
    'thickness': (0.0, None), 'cn': (0.0, None), 'am_cn': (0.0, None),
    'mpm_dg_mean': (0.0, None),         # 누적 소성변형 ≥ 0
    'porosity_derived': (0.0, 100.0),
    # mpm_plastic_gain_* 는 의도적으로 무경계 — 소성 흐름이 일부 지점의 피복을 **뺄** 수도
    # 있어 부호를 단정할 근거가 없다 (§F1: 확신 없는 경계는 걸지 않는다).
}


def _apply_bounds(row):
    """PI 를 물리 경계로 자르고 잘랐다고 표시.  점추정 위반은 자르지 않고 표시만.

    log 타깃(τ·두께)은 역변환이 비대칭이라 "± 한 숫자" 로 쓸 수 없다 — 실측 두께가
    −30.7 / +49.4 (38 % 차) 였다.  `asymmetric` 을 달아 UI 가 양쪽을 따로 쓰게 한다.
    """
    lo_b, hi_b = BOUNDS.get(row['target'], (None, None))
    row['lo_raw'], row['hi_raw'], row['clipped'] = row['lo'], row['hi'], []
    if lo_b is not None and row['lo'] < lo_b:
        row['lo'] = lo_b
        row['clipped'].append(f'하한 {lo_b:g}')
    if hi_b is not None and row['hi'] > hi_b:
        row['hi'] = hi_b
        row['clipped'].append(f'상한 {hi_b:g}')
    row['value_out_of_bounds'] = bool(
        (lo_b is not None and row['value'] < lo_b) or (hi_b is not None and row['value'] > hi_b))
    dn, up = row['value'] - row['lo'], row['hi'] - row['value']
    row['asymmetric'] = bool(abs(up - dn) > 0.02 * max(abs(up), abs(dn), 1e-12))
    return row

_CACHE = {'path': None, 'mtime': None, 'bundle': None}


def model_path():
    return (os.environ.get('STRUCTURE_MODEL_JSON')
            or os.path.join(_ROOT, 'docs', 'data', 'structure_model.json'))


def load_bundle(force=False):
    """계수 JSON 을 읽어 캐시.  파일이 바뀌면 자동 재로딩 (mtime 비교)."""
    p = model_path()
    if not os.path.isfile(p):
        return None
    mt = os.path.getmtime(p)
    if force or _CACHE['bundle'] is None or _CACHE['path'] != p or _CACHE['mtime'] != mt:
        with open(p, encoding='utf-8') as fh:
            _CACHE['bundle'] = json.load(fh)
        _CACHE['path'], _CACHE['mtime'] = p, mt
    return _CACHE['bundle']


def status():
    """페이지 상단 배지용 — 모델이 있나, 무엇을 내보낼 수 있나."""
    b = load_bundle()
    if b is None:
        return {'ready': False, 'path': model_path(),
                'hint': ('계수 JSON 이 없습니다.  WSL 에서: python3 scripts/ml_design_structure.py '
                         '--csv docs/data/design_performance_corpus.csv '
                         '--out docs/data/structure_model.json  → 커밋하면 여기서 바로 씁니다.')}
    ms = b.get('models', {})
    rows = []
    for t, m in ms.items():
        if t in FORBIDDEN:
            continue
        rows.append({'target': t, 'label': LABELS.get(t, (t, ''))[0], 'unit': LABELS.get(t, (t, ''))[1],
                     'verdict': m.get('verdict', '?'), 'n': m.get('n'), 'k': m.get('k'),
                     'nested': m.get('nested_cv_r2'), 'naive': m.get('loocv_r2_naive'),
                     'bias': m.get('selection_bias'), 'pi90': m.get('pi90_coverage')})
    order = {'USABLE': 0, 'WEAK': 1, 'REJECT': 2}
    rows.sort(key=lambda r: (order.get(r['verdict'], 3), -(r['nested'] or -9)))
    cl = (b.get('closure') or {}).get('porosity')
    return {'ready': True, 'path': model_path(), 'n_cases': b.get('n_cases'),
            'method': b.get('method', {}), 'rows': rows,
            'n_usable': sum(1 for r in rows if r['verdict'] == 'USABLE'),
            'n_weak': sum(1 for r in rows if r['verdict'] == 'WEAK'),
            'n_reject': sum(1 for r in rows if r['verdict'] == 'REJECT'),
            'closure': cl,
            'physics_audit': b.get('physics_audit'),
            'note': ('σ 삼중항은 이 모델의 타깃이 아니다 — 스케일링법칙(LOOCV .975/.953/.90) '
                     '소관.  ML 은 그 법칙의 **입력**(구조)만 예측한다.')}


def predict_structure(d_se, d_am, am_pct, ps_frac, rve, loading, include_weak=True):
    """설계 6 노브 → 구조 예측.  REJECT 타깃은 제외, 외삽은 표시, porosity 는 유도."""
    import ml_design_structure as M

    b = load_bundle()
    if b is None:
        return {'ready': False, **status()}
    feats = M.derive_features(float(d_se), float(d_am), float(am_pct),
                              float(ps_frac), float(rve), float(loading))
    x = [float(feats[f]) for f in b.get('features', M.DESIGN_FEATURES)]
    out, any_extrap = [], False
    got = {}
    for t, m in b.get('models', {}).items():
        vd = m.get('verdict', 'WEAK')
        if t in FORBIDDEN or vd == 'REJECT':
            continue                                  # 못 맞히는 걸 내보내면 그건 거짓말이다
        if vd == 'WEAK' and not include_weak:
            continue
        p = M.predict(m, x)
        got[t] = p
        any_extrap = any_extrap or bool(p['extrapolation'])
        lab, unit = LABELS.get(t, (t, ''))
        out.append({'target': t, 'label': lab, 'unit': unit, 'verdict': vd,
                    'value': p['value'], 'lo': p['lo'], 'hi': p['hi'],
                    'extrapolation': bool(p['extrapolation']),
                    'leverage': p['leverage'], 'nested': m.get('nested_cv_r2'),
                    'source': 'ML (ridge, nested-CV 검증)'})
        _apply_bounds(out[-1])
    # ── porosity = 유도.  회귀하지 않는다 ────────────────────────────────────────────
    cl = (b.get('closure') or {}).get('porosity')
    if cl and 'phi_se' in got and 'phi_am' in got:
        eps = 100.0 * (cl['closure_const'] - got['phi_se']['value'] - got['phi_am']['value'])
        half = 1.6448536269514722 * float(cl['derived_resid_sd_pct'])   # 90 %, **측정된** 잔차
        amp = cl.get('amplification')
        out.append({
            'target': 'porosity_derived', 'label': 'ε  공극률 (φ 에서 계산)', 'unit': '%',
            'verdict': 'DERIVED', 'value': eps, 'lo': eps - half, 'hi': eps + half,
            'extrapolation': bool(got['phi_se']['extrapolation']
                                  or got['phi_am']['extrapolation']),
            'leverage': max(got['phi_se']['leverage'], got['phi_am']['leverage']),
            'nested': cl.get('derived_nested'),
            'source': 'ε = C − φ_SE − φ_AM (회귀 아님)',
            'caveat': (f"띠는 학습 때 **측정한** 폴드-밖 잔차 sd {cl['derived_resid_sd_pct']:.2f} %p "
                       f"(전파-가정 아님).  넓은 이유: ε 은 큰 두 수의 작은 차라 증폭률 "
                       f"{amp:.0f}× — φ 합의 1 % 오차가 ε 을 {0.01 * amp:.2f} σ 흔든다."
                       if amp else '띠는 학습 때 측정한 폴드-밖 잔차 sd.')})
        _apply_bounds(out[-1])
    order = {'USABLE': 0, 'DERIVED': 1, 'WEAK': 2}
    out.sort(key=lambda r: (order.get(r['verdict'], 3), r['target']))
    return {'ready': True, 'rows': out, 'any_extrapolation': any_extrap,
            'design': {'d_se': d_se, 'd_am': d_am, 'am_pct': am_pct,
                       'ps_frac': ps_frac, 'rve': rve, 'loading': loading},
            'derived_features': feats,
            'note': ('REJECT 판정 타깃은 아예 내보내지 않는다.  σ 는 이 모델 소관이 아니라 '
                     '스케일링법칙(.975/.953/.90) 소관.')}


def surface(target='tau', x_knob='am_pct', y_knob='d_am', n=25, fixed=None, csv_path=None):
    """2 인자 응답면 (주간보고 8 쪽 형식) + 실제 코퍼스 산점.  CSV 없으면 면만."""
    import numpy as np

    import ml_design_structure as M

    b = load_bundle()
    if b is None:
        return {'error': '계수 JSON 이 없습니다 — 먼저 학습하세요.'}
    if target in FORBIDDEN or (b.get('models', {}).get(target, {}).get('verdict') == 'REJECT'):
        return {'error': f'{target} 은 판정 REJECT 이거나 금지 열입니다 — 면을 그리지 않습니다.'}
    csv_path = csv_path or os.path.join(_ROOT, 'docs', 'data', 'design_performance_corpus.csv')
    if os.path.isfile(csv_path):
        X, _ys, _nm, rows = M.load_corpus(csv_path)
    else:
        # 코퍼스가 없으면 학습 때 저장해 둔 표준화 통계로 범위를 복원한다 (면만, 산점 없음)
        m = b['models'].get(target) or next(iter(b['models'].values()))
        mu, sd = np.asarray(m['mu']), np.asarray(m['sd'])
        X, rows = np.vstack([mu - 2 * sd, mu + 2 * sd]), None
    return M.response_surface(b, np.asarray(X, float), target, x_knob, y_knob,
                              n=int(n), fixed=fixed, rows=rows)


def suggest_batch(csv_path=None, n=10, target='tau', allow_weak=False):
    """다음 DEM 배치 (순차 D-최적).  코퍼스 CSV 가 있어야 후보 상자를 잡을 수 있다."""
    import numpy as np

    import ml_design_structure as M

    b = load_bundle()
    if b is None:
        return {'error': '계수 JSON 이 없습니다 — 먼저 학습하세요.', 'rows': []}
    csv_path = csv_path or os.path.join(_ROOT, 'docs', 'data', 'design_performance_corpus.csv')
    if not os.path.isfile(csv_path):
        return {'error': f'코퍼스 CSV 가 없습니다 ({csv_path}) — 후보의 실현가능 범위를 '
                         '코퍼스에서 잡으므로 필요합니다.', 'rows': []}
    X, _ys, _n, _r = M.load_corpus(csv_path)
    if not len(X):
        return {'error': '코퍼스가 비었습니다.', 'rows': []}
    r = M.suggest(b, np.asarray(X, float), target, n_out=int(n), allow_weak=allow_weak)
    return r


def _selftest():                                                   # noqa: C901
    """python3 webapp/structure_predictor.py --selftest"""
    import csv as _csv
    import tempfile

    import numpy as np

    import ml_design_structure as M

    ok = tot = 0

    def chk(name, cond, extra=''):
        nonlocal ok, tot
        tot += 1
        ok += 1 if cond else 0
        print(f"  {'✓' if cond else '✗ FAIL'} {name}" + (f' — {extra}' if extra else ''))

    # 모델이 없을 때 — 크래시가 아니라 안내여야 한다 (배포서 실제로 겪는 상태)
    _save = os.environ.get('STRUCTURE_MODEL_JSON')
    os.environ['STRUCTURE_MODEL_JSON'] = '/nonexistent/structure_model.json'
    _CACHE.update(path=None, mtime=None, bundle=None)
    st0 = status()
    chk('★모델 파일이 없으면 크래시 대신 안내 (배포 기본 상태)',
        st0['ready'] is False and 'ml_design_structure' in (st0.get('hint') or ''))
    chk('모델 없을 때 예측 호출도 안전', predict_structure(1, 5, 80, .5, 50, 6)['ready'] is False)

    rng = np.random.default_rng(11)
    n = 240
    kn = np.column_stack([rng.uniform(a, b, n) for a, b in
                          ((0.3, 2.0), (2, 12), (50, 90), (0, 1), (30, 80), (1, 8))])
    X = np.array([[float(M.derive_features(*k)[f]) for f in M.DESIGN_FEATURES] for k in kn])
    phi_am = 0.006 * X[:, 2] + rng.normal(0, 0.008, n)
    phi_se = 0.86 - phi_am + rng.normal(0, 0.008, n)
    por = 100 * (1.0 - phi_se - phi_am)
    with tempfile.NamedTemporaryFile('w', suffix='.csv', delete=False, newline='') as fh:
        cols = (['name', 'use_source'] + M.DESIGN_FEATURES
                + ['phi_se', 'phi_am', 'porosity', 'use_porosity_pct', 'tau', 'thickness'])
        w = _csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for i in range(n):
            r = {'name': f's{i}', 'use_source': 'DEM'}
            r.update({f: X[i, j] for j, f in enumerate(M.DESIGN_FEATURES)})
            r.update({'phi_se': phi_se[i], 'phi_am': phi_am[i], 'porosity': por[i],
                      # ★게이트된 열은 일부러 **오염**시킨다 — 새어나오면 안 되는 열이다
                      'use_porosity_pct': por[i] + rng.normal(0, 5),
                      'tau': float(np.exp(0.01 * X[i, 2] + 0.05 * X[i, 5])),
                      'thickness': 20 + 3 * X[i, 5]})
            w.writerow(r)
        cp = fh.name
    mp = cp.replace('.csv', '.json')
    M.train(cp, mp, verbose=False, folds=5)
    os.environ['STRUCTURE_MODEL_JSON'] = mp
    load_bundle(force=True)

    st = status()
    chk('학습 산출물을 읽어 상태를 낸다', st['ready'] and st['n_cases'] == n and st['n_usable'] >= 3,
        f"USABLE {st['n_usable']} · WEAK {st['n_weak']}")
    chk('★판정표에 use_porosity_pct 가 없다 (게이트 혼합열은 노출 금지)',
        not any(r['target'] in FORBIDDEN for r in st['rows']))
    r = predict_structure(1.2, 6.0, 78.0, 0.6, 55.0, 4.0)
    chk('예측이 행을 낸다', r['ready'] and len(r['rows']) >= 3, f"{len(r['rows'])} 행")
    chk('★REJECT 판정 타깃은 예측에 안 나온다',
        not any(x['verdict'] == 'REJECT' for x in r['rows']))
    chk('★FORBIDDEN 열은 예측에 안 나온다',
        not any(x['target'] in FORBIDDEN for x in r['rows']))
    g = {x['target']: x for x in r['rows']}
    chk('★porosity 는 회귀가 아니라 유도 — 항등식과 정확히 일치',
        'porosity_derived' in g
        and abs(g['porosity_derived']['value']
                - 100 * (st['closure']['closure_const']
                         - g['phi_se']['value'] - g['phi_am']['value'])) < 1e-9,
        f"{g.get('porosity_derived', {}).get('value', float('nan')):.4f} %")
    chk('★유도 porosity 의 띠가 **측정된** 잔차 sd 에서 온다 (전파-가정 아님)',
        'porosity_derived' in g and '측정한' in (g['porosity_derived'].get('caveat') or ''))
    chk('모든 행이 PI 로 값을 감싼다',
        all(x['lo'] <= x['value'] <= x['hi'] for x in r['rows']))
    # ★ 물리 경계 — 실측에서 mpm_dg_mean 의 PI 하한이 −0.018 (음의 소성변형) 이었다
    chk('★어떤 행의 PI 도 물리 경계를 벗어나지 않는다 (음의 소성변형·τ<1 등)',
        all(not (BOUNDS.get(x['target'], (None, None))[0] is not None
                 and x['lo'] < BOUNDS[x['target']][0] - 1e-12) for x in r['rows'])
        and all(not (BOUNDS.get(x['target'], (None, None))[1] is not None
                     and x['hi'] > BOUNDS[x['target']][1] + 1e-12) for x in r['rows']))
    chk('★잘랐으면 잘랐다고 표시하고 원값을 남긴다 (조용한 클리핑 금지)',
        all(('clipped' in x and 'lo_raw' in x and 'hi_raw' in x) for x in r['rows'])
        and all((not x['clipped']) or (x['lo_raw'] < x['lo'] - 1e-12
                                       or x['hi_raw'] > x['hi'] + 1e-12) for x in r['rows']))
    # 판별력: 경계 밖으로 뻗는 행을 만들어 실제로 잘리는지
    _fake = {'target': 'mpm_dg_mean', 'value': 0.02, 'lo': -0.05, 'hi': 0.09}
    _apply_bounds(_fake)
    chk('★경계 밖 PI 는 실제로 잘리고 표시된다 (돌연변이 검사)',
        _fake['lo'] == 0.0 and _fake['clipped'] and _fake['lo_raw'] == -0.05,
        f"lo −0.05 → {_fake['lo']} · {_fake['clipped']}")
    _asym = {'target': 'thickness', 'value': 80.9, 'lo': 50.2, 'hi': 130.3}
    _apply_bounds(_asym)
    chk('★log 타깃의 비대칭 PI 를 asymmetric 으로 표시 (± 한 숫자로 쓰면 양쪽 다 틀린다)',
        _asym['asymmetric'] is True,
        f"−{_asym['value']-_asym['lo']:.1f} / +{_asym['hi']-_asym['value']:.1f}")
    _sym = {'target': 'phi_se', 'value': 0.32, 'lo': 0.28, 'hi': 0.36}
    _apply_bounds(_sym)
    chk('대칭 PI 는 asymmetric 이 아니다', _sym['asymmetric'] is False)
    r2 = predict_structure(9.9, 0.6, 130.0, 0.5, 300.0, 40.0)
    chk('★학습 범위 밖 설계 → extrapolation 표시 (조용히 답하지 않는다)',
        r2['any_extrapolation'])
    chk('범위 안 설계는 표시 없음', not r['any_extrapolation'])
    sg = suggest_batch(csv_path=cp, n=4, target='tau')
    chk('다음 DEM 배치 제안이 돈다 (순차 D-최적)',
        sg.get('error') is None and len(sg.get('rows', [])) == 4)
    chk('★배치 제안이 자유노브 6 개만 낸다 (그대로 시뮬 입력)',
        list(sg['rows'][0]['design'].keys()) == M.FREE_KNOBS)

    for f in (cp, mp):
        try:
            os.unlink(f)
        except OSError:
            pass
    if _save:
        os.environ['STRUCTURE_MODEL_JSON'] = _save
    else:
        os.environ.pop('STRUCTURE_MODEL_JSON', None)
    _CACHE.update(path=None, mtime=None, bundle=None)
    print(f"STRUCTURE-PREDICTOR SELFTEST {ok}/{tot} {'PASS' if ok == tot else 'FAIL'}")
    return 0 if ok == tot else 1


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        raise SystemExit(_selftest())
    print(json.dumps(status(), ensure_ascii=False, indent=1))
