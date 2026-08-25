#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""대리모델 해석 층 — **정확한 Shapley 기여도** + **다목적 Pareto/하이퍼볼륨**.

출처: 양수영 (BML) 연구세미나 2026-08-18, "Multiphysics and machine-learning-guided design of
radial cathode microstructures" (litdb 정본 카드 `litdb/talks/yang2026_bml_ml_radial_cathode.md`).
그 발표의 **방법 3단**(설계공간 샘플링 → 대리모델 → SHAP + 다목적 최적화) 중, **우리에게 없던
두 단**(SHAP 중요도 · Pareto/HV)을 우리 규약으로 옮긴 것이다.

★ 우리가 **그대로 베끼지 않은** 두 곳 (그 자리가 그 방법의 약점이라서):

  ① **근사 SHAP → 정확 Shapley.**  발표는 배경표본 32개로 KernelSHAP 을 근사했다.  우리는
     자유노브가 **6개**뿐이라 2⁶ = 64 연합을 **전수 열거**할 수 있다 ⇒ 근사 오차가 0 이다.
     (샘플링 SHAP 의 분산은 보고되지 않는 것이 보통이고, 그러면 "이 인자가 저 인자보다 크다"
     를 잡음과 구분할 수 없다.)

  ② **상관된 특징에 SHAP 를 걸지 않는다.**  발표 질의응답에서 정확히 이 지적이 나왔고
     ("설계 인자끼리 리니어리티가 없어야 의미가 있는 분석 아니냐") 답이 열려 있었다.
     우리 `DESIGN_FEATURES` 13개 중 **7개는 자유노브 6개의 대수적 함수**다 (`se_density_proxy`
     = (100−am_pct)/d_se 등, CLAUDE.md `free_products` 절).  그 유도량에 interventional SHAP 을
     걸면 **한 노브의 기여가 자기 유도량들에 쪼개져** 중요도가 물리적으로 무의미해진다.
     ⇒ 이 모듈은 **자유노브에만** Shapley 를 건다.  유도량을 축으로 요청하면 거부한다.
     ⚠ interventional(주변) 규약이 정당한 이유는 노브가 **우리가 정하는 설계 입력(DOE)** 이라
       서다 — 관측 공변량이면 이 규약이 상관을 통해 거짓 기여를 만든다.  그래서 배경 코퍼스의
       노브 상관을 **재서 경고**한다 (`corr_warn`).

★ 발표에서 그대로 가져온 것: 타깃별 `mean|φ|` 를 **100 % 로 정규화**한 중요도 히트맵
  (발표 p16) · 다목적 Pareto + 하이퍼볼륨 추적 (p18) · **목적당 하나씩** 대리모델을 두는 구성.

⚠ **이 모듈은 물리를 만들지 않는다.**  대리모델이 맞는 만큼만 맞다 —
  · REJECT 판정 타깃은 목적에 넣을 수 없다 (`use_porosity_pct` 는 `FORBIDDEN`)
  · WEAK 타깃은 넣을 수 있으나 결과에 표시된다
  · 외삽 게이트(leverage)를 넘은 Pareto 점은 **버리지 않고 표시**한다 (버리면 왜 없는지 모른다)
  · σ 삼중항은 애초에 이 모델의 타깃이 아니다 (스케일링법칙 소관) — 목적으로 못 넣는다

  python3 scripts/ml_shap_pareto.py --selftest
  python3 scripts/ml_shap_pareto.py --shap --n-explain 128
  python3 scripts/ml_shap_pareto.py --pareto --objectives 'tau:min,f_perc:max,phi_se:max'
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import ml_design_structure as M                                    # noqa: E402


# ══════════════════════════════════════════════════════════════════════════════════
#  도메인 레지스트리 — **DEM 과 DFT 가 섞이지 않게 하는 장치**
# ══════════════════════════════════════════════════════════════════════════════════
#  왜 필요한가: 이 해석 층은 도메인 중립이다 (Shapley·Pareto 는 어느 대리모델에나 걸린다).
#  그래서 나중에 DFT 축이 들어오면 **같은 함수에 다른 노브·다른 타깃**이 흘러들 수 있고,
#  그때 둘이 조용히 섞이면 "무엇의 중요도인가" 가 사라진다.
#  ⇒ 도메인을 **명시 등록**으로만 받는다.  미등록 이름은 오류다 (fail-closed).
#  ⇒ 노브·타깃·번들 경로가 도메인마다 **완전히 분리**되고, 한 호출은 한 도메인만 본다.

class DomainSpec:
    """한 도메인의 계약 — 자유노브 · 특징 벡터 · 예측기 · 번들."""

    def __init__(self, name, knobs, features, derive, bundle_path, forbidden=(),
                 knob_labels=None, note=''):
        self.name = name
        self.knobs = tuple(knobs)
        self.features = tuple(features)
        self.derive = derive                    # (*knobs) -> {feature: value}
        self.bundle_path = bundle_path
        self.forbidden = frozenset(forbidden)
        self.knob_labels = dict(knob_labels or {})
        self.note = note

    def load(self):
        if not os.path.isfile(self.bundle_path):
            return None
        with open(self.bundle_path, encoding='utf-8') as f:
            return json.load(f)


def _dem_bundle_path():
    return os.path.join(os.path.dirname(_HERE), 'docs', 'data', 'structure_model.json')


DOMAINS = {
    'dem_structure': DomainSpec(
        name='dem_structure',
        knobs=M.FREE_KNOBS,                     # d_se d_am am_pct ps_frac rve loading
        features=M.DESIGN_FEATURES,
        derive=M.derive_features,
        bundle_path=_dem_bundle_path(),
        #  ⚠ `use_porosity_pct` 는 학습·노출 금지 열이다 (CLAUDE.md — 게이트가 porosity 만
        #    MPM 으로 바꾸고 φ 는 DEM 것을 남겨 한 물리상태가 아니다).  목적으로도 금지.
        forbidden=('use_porosity_pct',),
        knob_labels={'d_se': 'SE 직경 (µm)', 'd_am': 'AM 직경 (µm)',
                     'am_pct': 'AM 함량 (wt%)', 'ps_frac': 'P:S 비',
                     'rve': 'RVE 크기 (µm)', 'loading': '로딩 (mAh/cm²)'},
        note='DEM/MPM 전극 미세구조 — 설계 6 노브 → 구조 12 타깃.  σ 삼중항은 타깃이 아니다.'),
    #  ── DFT 축은 **아직 등록하지 않는다** ────────────────────────────────────────────
    #  사용자 지시 (2026-08-25): "우선 여기서는 dem 위주로 할거고 나중에 dft section 에서도
    #  관련해서 올거거든 그 둘이 충돌 안 되게 잘 분리해서 써줘."
    #  ⇒ 자리만 비워 둔다.  DFT 가 오면 **여기에 새 DomainSpec 을 추가**하고, DEM 것은
    #    한 글자도 건드리지 않는다.  노브·타깃·번들이 통째로 갈리므로 섞일 경로가 없다.
    #  ⚠ 아래 selftest `D-3` 이 "DFT 슬롯이 비어 있고, 미등록 이름은 오류" 를 상주 검증한다.
}

#: 아직 안 온 도메인 — 이름을 **미리 예약**해 두어 오타로 새 도메인이 생기는 것을 막는다.
RESERVED = ('dft_material',)


def get_domain(name):
    """등록된 도메인만 돌려준다.  미등록·예약은 **오류** (fail-closed)."""
    if name in DOMAINS:
        return DOMAINS[name]
    if name in RESERVED:
        raise KeyError(
            f"도메인 `{name}` 은 **예약돼 있으나 아직 등록되지 않았다**.  DFT 축이 준비되면 "
            f"`DOMAINS` 에 새 `DomainSpec` 을 추가할 것 — DEM 항목을 재사용하면 "
            f"두 축의 노브·타깃이 섞인다 (이 파일 §도메인 레지스트리).")
    raise KeyError(f"알 수 없는 도메인 `{name}`.  등록된 것: {sorted(DOMAINS)} · "
                   f"예약된 것: {list(RESERVED)}")


# ══════════════════════════════════════════════════════════════════════════════════
#  정확 Shapley — 2^k 연합 전수 열거 (근사 아님)
# ══════════════════════════════════════════════════════════════════════════════════
#: 이보다 노브가 많으면 전수 열거를 포기한다 — 그때는 **근사임을 밝히고** 써야 하므로
#: 조용히 근사로 내려가지 않고 오류를 낸다 (2^12 = 4096 연합까지가 실용 한계).
MAX_EXACT_KNOBS = 12


def _coalition_weights(k):
    """Shapley 가중 |S|!(k−|S|−1)!/k! 를 |S| 별로 미리 계산."""
    return np.array([math.factorial(s) * math.factorial(k - s - 1) / math.factorial(k)
                     for s in range(k)])


def exact_shapley(dom, models, x_knob, bg_knob, targets):
    """한 설계점 `x_knob` 의 **정확한** interventional Shapley 기여도.

    → {target: np.array(k)}  ·  φ 의 합 = f(x) − E_bg[f]  (효율성 공리, selftest 가 검증)

    ⚠ 근사가 아니다: 2^k 연합을 전부 돌고, 각 연합에서 배경 전체에 대해 평균한다.
      비용 = 2^k × |bg| 번의 특징 유도 (타깃 간에는 **재사용**하므로 타깃 수와 무관).
    """
    k = len(dom.knobs)
    if k > MAX_EXACT_KNOBS:
        raise ValueError(f'노브가 {k}개 — 전수 열거 한계 {MAX_EXACT_KNOBS} 초과.  '
                         f'근사 Shapley 가 필요하면 **근사임을 출력에 명시**하도록 따로 구현할 것 '
                         f'(조용히 근사로 내려가지 않는다)')
    x_knob = np.asarray(x_knob, float)
    bg = np.asarray(bg_knob, float)
    nb = len(bg)
    subsets = [frozenset(c) for s in range(k + 1) for c in itertools.combinations(range(k), s)]
    #  ── v(S) = E_bg[ f(x_S, bg_{~S}) ] — 특징 유도는 여기서 **한 번만** 한다 ──────────
    feat_cache = {}
    for S in subsets:
        hyb = np.repeat(bg[None, :, :], 1, axis=0)[0].copy()       # (nb, k)
        for i in S:
            hyb[:, i] = x_knob[i]
        F = np.empty((nb, len(dom.features)))
        for r in range(nb):
            d = dom.derive(*hyb[r])
            F[r] = [float(d[f]) for f in dom.features]
        feat_cache[S] = F
    w = _coalition_weights(k)
    out = {}
    for t, m in models.items():
        v = {S: float(np.mean([M.predict(m, F[r])['value'] for r in range(nb)]))
             for S, F in feat_cache.items()}
        phi = np.zeros(k)
        for i in range(k):
            rest = [j for j in range(k) if j != i]
            for s in range(k):
                for c in itertools.combinations(rest, s):
                    S = frozenset(c)
                    phi[i] += w[s] * (v[S | {i}] - v[S])
        out[t] = phi
    return out, {S: None for S in ()}          # 두 번째 반환은 자리표시 (API 안정)


def knob_correlation(bg_knob, knobs):
    """배경 코퍼스에서 **노브끼리** 얼마나 상관돼 있나.

    ★ 왜 재는가: interventional Shapley 는 노브가 서로 독립일 때 해석이 깨끗하다.
      발표 질의응답에서 정확히 이 점이 물어졌고 답이 열려 있었다 — 우리는 **재서 보고**한다.
      노브가 설계 입력(DOE)이면 보통 |r| 이 작다.  크면 그 쌍의 기여 분해를 믿지 말 것.
    """
    X = np.asarray(bg_knob, float)
    if X.shape[0] < 3:
        return {'max_abs_r': None, 'pairs': [], 'warn': '배경 표본이 3개 미만 — 상관을 못 잰다'}
    C = np.corrcoef(X, rowvar=False)
    pairs = []
    for a in range(len(knobs)):
        for b in range(a + 1, len(knobs)):
            r = float(C[a, b])
            if np.isfinite(r):
                pairs.append({'pair': f'{knobs[a]} × {knobs[b]}', 'r': round(r, 3)})
    pairs.sort(key=lambda p: -abs(p['r']))
    mx = abs(pairs[0]['r']) if pairs else 0.0
    warn = ''
    if mx >= 0.5:
        warn = (f'노브 상관 |r| 최대 {mx:.2f} ≥ 0.5 — interventional Shapley 가 그 쌍에서 '
                f'**실현 불가능한 조합**을 평가한다.  그 두 노브 사이의 기여 분해는 인용하지 말 것')
    elif mx >= 0.3:
        warn = f'노브 상관 |r| 최대 {mx:.2f} — 주의해서 읽을 것 (0.5 넘으면 인용 금지)'
    return {'max_abs_r': round(mx, 3), 'pairs': pairs[:6], 'warn': warn}


def shap_importance(domain='dem_structure', n_explain=128, n_bg=32, seed=0,
                    include_weak=True, csv_path=None):
    """타깃별 정확 Shapley → **mean|φ| 100 % 정규화 히트맵** (발표 p16 형식).

    → {'knobs', 'targets', 'heatmap'(타깃×노브 %), 'signed'(부호 = 방향), 'corr', ...}
    """
    dom = get_domain(domain)
    b = dom.load()
    if b is None:
        return {'ready': False, 'error': f'번들이 없다: {dom.bundle_path}',
                'hint': 'WSL 에서 ml_design_structure.py 로 학습해 커밋할 것'}
    models = {t: m for t, m in (b.get('models') or {}).items()
              if t not in dom.forbidden and m.get('verdict') != 'REJECT'
              and (include_weak or m.get('verdict') == 'USABLE')}
    if not models:
        return {'ready': False, 'error': 'REJECT/FORBIDDEN 을 빼고 나면 타깃이 없다'}
    lo, hi = _knob_box(b, dom)
    rs = np.random.RandomState(int(seed))
    bg = rs.uniform(lo, hi, size=(int(n_bg), len(dom.knobs)))
    xs = rs.uniform(lo, hi, size=(int(n_explain), len(dom.knobs)))
    corp = _corpus_knobs(csv_path, dom)
    if corp is not None and len(corp) >= max(8, int(n_bg)):
        #  코퍼스가 있으면 **실제 설계 분포**를 배경으로 쓴다 (균등 상자보다 정직하다)
        idx = rs.choice(len(corp), size=int(n_bg), replace=False)
        bg = corp[idx]
        jdx = rs.choice(len(corp), size=min(int(n_explain), len(corp)), replace=False)
        xs = corp[jdx]
    acc = {t: np.zeros(len(dom.knobs)) for t in models}
    sgn = {t: np.zeros(len(dom.knobs)) for t in models}
    for x in xs:
        phis, _ = exact_shapley(dom, models, x, bg, list(models))
        for t, p in phis.items():
            acc[t] += np.abs(p)
            sgn[t] += p
    heat, signed = {}, {}
    for t in models:
        mabs = acc[t] / len(xs)
        tot = float(mabs.sum())
        heat[t] = [round(100.0 * v / tot, 1) if tot > 0 else 0.0 for v in mabs]
        signed[t] = [round(float(v / len(xs)), 6) for v in sgn[t]]
    return {'ready': True, 'domain': dom.name, 'knobs': list(dom.knobs),
            'knob_labels': [dom.knob_labels.get(k, k) for k in dom.knobs],
            'targets': list(models),
            'verdicts': {t: models[t].get('verdict') for t in models},
            'heatmap': heat, 'signed_mean': signed,
            'n_explain': len(xs), 'n_bg': len(bg),
            'exact': True, 'n_coalitions': 2 ** len(dom.knobs),
            'corr': knob_correlation(bg, dom.knobs),
            'note': ('행 합 = 100 %.  **정확 Shapley** (2^k 연합 전수, 근사 아님).  '
                     '유도 특징이 아니라 **자유노브**에만 걸었다 — 유도량은 노브의 함수라 '
                     '거기 걸면 한 노브의 기여가 자기 유도량들에 쪼개진다.  '
                     'signed_mean 의 부호는 평균 방향이고, 크기 비교는 heatmap 으로 할 것.')}


def _knob_box(bundle, dom):
    """번들이 기록한 학습 범위 → (lo, hi).  없으면 코퍼스/기본 상자."""
    rng = (bundle.get('knob_range') or {})
    lo, hi = [], []
    for k in dom.knobs:
        r = rng.get(k)
        if r and len(r) == 2:
            lo.append(float(r[0])), hi.append(float(r[1]))
        else:
            d = {'d_se': (0.5, 1.5), 'd_am': (2.0, 8.0), 'am_pct': (60.0, 90.0),
                 'ps_frac': (0.0, 1.0), 'rve': (30.0, 80.0), 'loading': (1.0, 8.0)}.get(k)
            if d is None:
                raise KeyError(f'노브 `{k}` 의 범위를 모른다 — 번들에 `knob_range` 를 넣을 것')
            lo.append(d[0]), hi.append(d[1])
    return np.array(lo), np.array(hi)


def _corpus_knobs(csv_path, dom):
    """설계 코퍼스 CSV 에서 노브 열만 읽는다.  없으면 None."""
    p = csv_path or os.path.join(os.path.dirname(_HERE), 'docs', 'data',
                                 'design_performance_corpus.csv')
    if not os.path.isfile(p):
        return None
    import csv as _csv
    rows = []
    with open(p, encoding='utf-8') as f:
        for r in _csv.DictReader(f):
            try:
                rows.append([float(r[k]) for k in dom.knobs])
            except (KeyError, TypeError, ValueError):
                continue
    return np.array(rows) if rows else None


# ══════════════════════════════════════════════════════════════════════════════════
#  다목적 — Pareto front + 하이퍼볼륨 (발표 p18)
# ══════════════════════════════════════════════════════════════════════════════════
def _nondominated(P):
    """최소화 규약.  Pareto 비지배 집합."""
    P = np.atleast_2d(P)
    keep = np.ones(len(P), bool)
    for i in range(len(P)):
        if not keep[i]:
            continue
        dom_i = np.all(P <= P[i], axis=1) & np.any(P < P[i], axis=1)
        if dom_i.any():
            keep[i] = False
    return P[keep]


def hypervolume(P, ref):
    """최소화 규약의 **정확한** 하이퍼볼륨 (재귀 슬라이싱).

    ⚠ 몬테카를로를 쓰지 않는다 — HV **추이**를 그릴 것이라 잡음이 곧 가짜 수렴/발산이 된다.
    """
    P = np.atleast_2d(np.asarray(P, float))
    ref = np.asarray(ref, float)
    P = P[np.all(P <= ref, axis=1)]
    if len(P) == 0:
        return 0.0
    P = _nondominated(P)
    return float(_hv_rec(P, ref))


def _hv_rec(P, ref):
    m = P.shape[1]
    if m == 1:
        return max(0.0, float(ref[0] - P[:, 0].min()))
    order = np.argsort(P[:, -1])
    P = P[order]
    hv, n = 0.0, len(P)
    for i in range(n):
        z = P[i, -1]
        z_next = P[i + 1, -1] if i + 1 < n else ref[-1]
        if z_next <= z:
            continue
        sub = _nondominated(P[:i + 1, :-1])
        hv += _hv_rec(sub, ref[:-1]) * (z_next - z)
    return hv


def pareto_explore(domain='dem_structure', objectives=None, n=4000, seed=0,
                   include_weak=True, trace_points=40, csv_path=None):
    """대리모델로 설계공간을 훑어 **Pareto front + HV 추이**를 낸다 (발표 p17–18 형식).

    `objectives` = [(target, 'min'|'max'), …].  REJECT/FORBIDDEN 은 거부한다.

    ⚠ HV 는 **선언된 기준점**이 있어야 뜻이 있다.  자동으로 잡아 놓고 "100 % 로 수렴" 이라
      쓰면 그 100 % 는 자기가 만든 상자의 100 % 일 뿐이다.  ⇒ nadir/utopia 를 **표본에서
      한 번 정하고 출력에 적어** 재현 가능하게 한다 (그 뒤 추이 내내 고정).
    """
    dom = get_domain(domain)
    b = dom.load()
    if b is None:
        return {'ready': False, 'error': f'번들이 없다: {dom.bundle_path}'}
    all_m = b.get('models') or {}
    objectives = objectives or [('tau', 'min'), ('f_perc', 'max')]
    bad = []
    for t, _s in objectives:
        m = all_m.get(t)
        if t in dom.forbidden:
            bad.append(f'{t}: 노출 금지 타깃')
        elif m is None:
            bad.append(f'{t}: 모델에 없다 (가능: {sorted(k for k in all_m if k not in dom.forbidden)})')
        elif m.get('verdict') == 'REJECT':
            bad.append(f'{t}: REJECT 판정 — 못 맞히는 것을 목적으로 삼을 수 없다')
        elif m.get('verdict') != 'USABLE' and not include_weak:
            bad.append(f'{t}: WEAK 인데 include_weak=False')
    if bad:
        return {'ready': False, 'error': '목적 거부: ' + ' · '.join(bad)}
    lo, hi = _knob_box(b, dom)
    rs = np.random.RandomState(int(seed))
    K = rs.uniform(lo, hi, size=(int(n), len(dom.knobs)))
    B = phys_bounds()
    vals, lev, extr, oob = [], [], [], []
    for row in K:
        d = dom.derive(*row)
        x = [float(d[f]) for f in dom.features]
        v, lv, ex, ob = [], 0.0, False, []
        for t, sense in objectives:
            p = M.predict(all_m[t], x)
            v.append(p['value'] if sense == 'min' else -p['value'])
            lv = max(lv, float(p['leverage']))
            ex = ex or bool(p['extrapolation'])
            if _oob(t, p['value'], B):
                ob.append(t)
        vals.append(v), lev.append(lv), extr.append(ex), oob.append(ob)
    V = np.array(vals, float)
    extr = np.array(extr, bool)
    #  ★★ 물리 경계 위반은 **외삽보다 나쁘다** — 최적화기가 그런 점을 *선호*하기 때문이다.
    #    (f_perc 103 % 는 100 % 보다 "좋아 보인다".)  ⇒ front 에는 남겨 표시하되,
    #    **추천(균형점)은 경계 안 점 중에서만** 고른다.  자르지 않는다: 자르면 실패가 숨는다.
    oob_any = np.array([bool(o) for o in oob], bool)
    #  ★ 기준점을 **한 번** 정하고 고정 (표본의 최악/최선 모서리).  출력에 적는다.
    nadir = V.max(axis=0)
    utopia = V.min(axis=0)
    box = float(np.prod(np.maximum(nadir - utopia, 1e-12)))
    #  HV 추이 — 표본을 점진적으로 넣으며 (발표 p18 의 trial-number 축과 같은 뜻)
    steps = np.unique(np.linspace(max(8, n // trace_points), n, trace_points).astype(int))
    trace = [{'n': int(s), 'hv_pct': round(100.0 * hypervolume(V[:s], nadir) / box, 4)}
             for s in steps]
    front_idx = _front_indices(V)
    front = []
    for i in front_idx:
        front.append({'design': {k: round(float(v), 4) for k, v in zip(dom.knobs, K[i])},
                      'objectives': {t: round(float(V[i][j] if s == 'min' else -V[i][j]), 6)
                                     for j, (t, s) in enumerate(objectives)},
                      'leverage': round(float(lev[i]), 4),
                      'extrapolation': bool(extr[i]),
                      'out_of_bounds': list(oob[i])})
    #  ★ "균형점" = 정규화 거리 최소 (발표의 balanced design 과 같은 취지).
    #    ⚠ 단 **물리 경계 안 · 외삽 아님** 인 점 중에서 고른다 — 경계를 넘은 예측을 설계로
    #      추천하는 것은 환상을 추천하는 것이다.  없으면 `balanced=None` 이고 이유를 적는다.
    Vn = (V[front_idx] - utopia) / np.maximum(nadir - utopia, 1e-12)
    adm = [j for j, f in enumerate(front) if not f['out_of_bounds'] and not f['extrapolation']]
    if adm:
        bal = int(adm[int(np.argmin(np.linalg.norm(Vn[adm], axis=1)))])
        bal_why = '물리 경계 안 · 외삽 아님 인 front 점 중 정규화 거리 최소'
    elif [j for j, f in enumerate(front) if not f['out_of_bounds']]:
        _a2 = [j for j, f in enumerate(front) if not f['out_of_bounds']]
        bal = int(_a2[int(np.argmin(np.linalg.norm(Vn[_a2], axis=1)))])
        bal_why = ('⚠ 경계 안 점은 있으나 **전부 외삽**이다 — 그 중에서 골랐다.  '
                   '학습 범위 밖이므로 설계로 옮기기 전에 실런 확인 필수')
        bal = int(bal)
    else:
        bal, bal_why = None, ('⚠ front 전체가 **물리 경계 밖**이다 — 추천할 점이 없다.  '
                              '대리모델이 이 목적 조합에서 경계를 못 지킨다는 뜻이므로 '
                              '목적을 바꾸거나 그 타깃의 적합을 먼저 볼 것')
    n_ex = int(sum(f['extrapolation'] for f in front))
    n_ob = int(sum(bool(f['out_of_bounds']) for f in front))
    return {'ready': True, 'domain': dom.name,
            'objectives': [{'target': t, 'sense': s,
                            'verdict': all_m[t].get('verdict'),
                            'nested_cv_r2': all_m[t].get('nested_cv_r2')} for t, s in objectives],
            'n_sampled': int(n), 'n_front': len(front), 'front': front,
            'balanced_index': bal,
            'balanced': (front[bal] if (bal is not None and front) else None),
            'balanced_why': bal_why,
            'hv_trace': trace, 'hv_final_pct': trace[-1]['hv_pct'] if trace else None,
            'reference': {'nadir': [round(float(v), 6) for v in nadir],
                          'utopia': [round(float(v), 6) for v in utopia],
                          'convention': 'HV % = 표본 상자(nadir−utopia) 대비.  '
                                        '이 상자는 **이 표본에서 한 번 정해 고정**했다 — '
                                        '다른 표본과 % 를 직접 비교하지 말 것'},
            'n_front_extrapolated': n_ex, 'n_front_out_of_bounds': n_ob,
            'note': ('⚠ Pareto 점은 **대리모델의 예측**이다 — 물리가 아니다.  '
                     f'front {len(front)}점 중 외삽 {n_ex}점 · **물리 경계 밖 {n_ob}점** '
                     '(둘 다 버리지 않고 표시한다: 버리면 왜 없는지 알 수 없다).  '
                     '경계 밖 점이 나오는 것은 정상이다 — 최적화기는 그런 점을 *선호*한다 '
                     '(f_perc 103 % 가 100 % 보다 좋아 보이므로).  그래서 **추천은 경계 안에서만** '
                     '고른다.  실제 설계로 옮기기 전에 그 점에서 DEM/MPM 을 한 번 돌려 확인할 것.')}


def phys_bounds():
    """물리 하드 경계 — **`webapp/structure_predictor.BOUNDS` 를 그대로 쓴다 (사본 금지).**

    ⚠ 여기에 값을 다시 적으면 CDXIJ-6/규칙 I 가 겨냥하는 **사본 표류**가 생긴다.
      가져오지 못하면 **오류**다 (조용히 경계 없이 최적화하면 최적화기가 곧장 경계 밖으로 간다).
    """
    wp = os.path.join(os.path.dirname(_HERE), 'webapp')
    if wp not in sys.path:
        sys.path.insert(0, wp)
    try:
        import structure_predictor as SP                          # noqa: PLC0415
    except Exception as e:                                        # noqa: BLE001
        raise RuntimeError(
            f'물리 경계를 가져올 수 없다 ({type(e).__name__}: {e}).  '
            f'`webapp/structure_predictor.BOUNDS` 가 정본이고 여기서 **사본을 만들지 않는다** — '
            f'경계 없이 최적화하면 최적화기가 f_perc 103 % 같은 점을 최적해로 고른다') from e
    return dict(SP.BOUNDS)


def _oob(target, value, B):
    """점추정이 물리 경계 밖인가.  **자르지 않는다** — 자르면 실패가 숨는다
    (`structure_predictor._apply_bounds` 의 규약 그대로)."""
    lo, hi = B.get(target, (None, None))
    return bool((lo is not None and value < lo) or (hi is not None and value > hi))


def _front_indices(V):
    keep = []
    for i in range(len(V)):
        dom_i = np.all(V <= V[i], axis=1) & np.any(V < V[i], axis=1)
        if not dom_i.any():
            keep.append(i)
    return keep


# ══════════════════════════════════════════════════════════════════════════════════
def _selftest():                                                   # noqa: C901
    n = [0, 0]

    def chk(msg, ok):
        n[1] += 1
        n[0] += bool(ok)
        print(f'  {"PASS" if ok else "FAIL"}  {msg}')

    # ── 도메인 분리 (사용자 지시: DEM ↔ DFT 충돌 금지) ────────────────────────────────
    chk('D-1 DEM 도메인이 등록돼 있다', get_domain('dem_structure').name == 'dem_structure')
    try:
        get_domain('dft_material'); ok = False
    except KeyError as e:
        ok = '예약' in str(e) and 'DomainSpec' in str(e)
    chk('D-2 ★ 예약된 DFT 이름은 **오류**다 (조용히 DEM 을 재사용하지 않는다)', ok)
    try:
        get_domain('오타난이름'); ok = False
    except KeyError as e:
        ok = '등록된 것' in str(e)
    chk('D-3 ★ 미등록 도메인은 오류이고 무엇이 있는지 알려준다', ok)
    chk('D-4 ★ DFT 슬롯이 아직 비어 있다 (등록되면 이 검사가 바뀌어야 한다)',
        'dft_material' not in DOMAINS and 'dft_material' in RESERVED)

    # ── 정확 Shapley — 효율성 공리 + 알려진 해석해 ────────────────────────────────────
    class _Lin:
        """f = 3·a + 0·b − 2·a·c 를 흉내내는 가짜 도메인 (해석해를 안다)."""

    fake = DomainSpec('fake', knobs=('a', 'b', 'c'), features=('a', 'b', 'c', 'ac'),
                      derive=lambda a, b, c: {'a': a, 'b': b, 'c': c, 'ac': a * c},
                      bundle_path='/dev/null')
    mdl = {'y': {'terms': None}}

    #  M.predict 를 안 쓰고 직접 계약을 흉내내는 대신, **진짜 M.predict 규약**을 쓰는 최소 모델
    #  을 만들 수 없으므로 여기서는 v(S) 경로만 검증한다 (아래 효율성은 실모델로).
    def _f(row):
        a, b, c = row
        return 3.0 * a + 0.0 * b - 2.0 * a * c

    k = 3
    rs = np.random.RandomState(0)
    bgk = rs.uniform(0, 1, size=(24, k))
    xk = np.array([0.8, 0.3, 0.6])
    w = _coalition_weights(k)
    v = {}
    for s in range(k + 1):
        for cmb in itertools.combinations(range(k), s):
            S = frozenset(cmb)
            hyb = bgk.copy()
            for i in S:
                hyb[:, i] = xk[i]
            v[S] = float(np.mean([_f(r) for r in hyb]))
    phi = np.zeros(k)
    for i in range(k):
        rest = [j for j in range(k) if j != i]
        for s in range(k):
            for cmb in itertools.combinations(rest, s):
                S = frozenset(cmb)
                phi[i] += w[s] * (v[S | {i}] - v[S])
    chk(f'S-1 ★ 효율성 공리 Σφ = f(x) − E[f]  ({phi.sum():.6f} vs {v[frozenset(range(k))] - v[frozenset()]:.6f})',
        abs(phi.sum() - (v[frozenset(range(k))] - v[frozenset()])) < 1e-9)
    chk(f'S-2 ★ 모델에 안 들어간 노브 b 의 기여가 정확히 0 ({phi[1]:.2e})', abs(phi[1]) < 1e-12)
    chk('S-3 ★ 교호작용(a·c)이 있어도 두 노브에 나뉘어 배분된다 (선형 근사가 아니다)',
        abs(phi[0]) > 1e-6 and abs(phi[2]) > 1e-6)
    chk('S-4 노브 상관 계측기가 돈다', knob_correlation(bgk, ('a', 'b', 'c'))['max_abs_r'] is not None)
    _hc = knob_correlation(np.c_[bgk[:, 0], bgk[:, 0] * 0.99 + 0.01, bgk[:, 2]], ('a', 'b', 'c'))
    chk(f'S-5 ★ 노브가 상관되면 **경고한다** (|r| {_hc["max_abs_r"]})',
        _hc['max_abs_r'] >= 0.5 and '인용하지 말' in _hc['warn'])
    try:
        exact_shapley(DomainSpec('big', knobs=tuple('abcdefghijklmn'), features=(),
                                 derive=lambda *a: {}, bundle_path='/dev/null'),
                      {}, np.zeros(14), np.zeros((2, 14)), [])
        ok = False
    except ValueError as e:
        ok = '전수 열거 한계' in str(e)
    chk('S-6 ★ 노브가 많으면 **조용히 근사로 내려가지 않고** 오류 (근사임을 숨기지 않는다)', ok)

    # ── 하이퍼볼륨 — 손으로 아는 값 ──────────────────────────────────────────────────
    hv2 = hypervolume(np.array([[1.0, 3.0], [2.0, 2.0], [3.0, 1.0]]), np.array([4.0, 4.0]))
    #  (4−1)(4−3) + (4−2)(4−2) − 겹침…  슬라이싱으로: 3*1 + 2*1 + 1*1 = 6
    chk(f'H-1 ★ 2D HV 가 손계산과 같다 ({hv2})', abs(hv2 - 6.0) < 1e-9)
    hv1 = hypervolume(np.array([[1.0, 1.0]]), np.array([3.0, 3.0]))
    chk(f'H-2 단일점 HV = 사각형 넓이 ({hv1})', abs(hv1 - 4.0) < 1e-9)
    chk('H-3 ★ 기준점 밖의 점은 HV 에 기여하지 않는다',
        abs(hypervolume(np.array([[5.0, 5.0]]), np.array([4.0, 4.0]))) < 1e-12)
    hv3 = hypervolume(np.array([[1.0, 1.0, 1.0]]), np.array([2.0, 3.0, 4.0]))
    chk(f'H-4 3D HV = 1×2×3 = 6 ({hv3})', abs(hv3 - 6.0) < 1e-9)
    chk('H-5 ★ 지배되는 점을 넣어도 HV 가 안 변한다 (비지배 필터가 산다)',
        abs(hypervolume(np.array([[1.0, 1.0], [2.0, 2.0]]), np.array([3.0, 3.0]))
            - hypervolume(np.array([[1.0, 1.0]]), np.array([3.0, 3.0]))) < 1e-9)
    chk('H-6 ★ 점을 더하면 HV 는 줄지 않는다 (단조) — 추이 그래프의 전제',
        hypervolume(np.array([[1.0, 3.0], [3.0, 1.0]]), np.array([4.0, 4.0]))
        <= hypervolume(np.array([[1.0, 3.0], [3.0, 1.0], [2.0, 2.0]]), np.array([4.0, 4.0])) + 1e-12)

    # ── Pareto 계약 — 못 맞히는 타깃을 목적으로 못 삼는다 ──────────────────────────────
    _b = get_domain('dem_structure').load()
    if _b is None:
        chk('P-0 (번들 없음 — 실모델 검사 생략, 클라우드에선 정상)', True)
    else:
        r = pareto_explore(objectives=[('use_porosity_pct', 'min'), ('tau', 'min')], n=32)
        chk('P-1 ★ 노출 금지 타깃을 목적으로 주면 거부한다',
            not r['ready'] and 'use_porosity_pct' in r['error'])
        r = pareto_explore(objectives=[('없는타깃', 'min')], n=32)
        chk('P-2 ★ 없는 타깃은 가능 목록과 함께 거부', not r['ready'] and '가능' in r['error'])
        r = pareto_explore(objectives=[('tau', 'min'), ('f_perc', 'max')], n=64, seed=1)
        chk(f'P-3 정상 목적이면 front 가 나온다 (front {r.get("n_front")})',
            r['ready'] and r['n_front'] >= 1)
        chk('P-4 ★ 기준점을 출력에 적는다 (HV % 가 자기가 만든 상자의 % 임을 숨기지 않는다)',
            r['ready'] and 'nadir' in r['reference'] and '직접 비교하지 말' in r['reference']['convention'])
        chk('P-5 ★ 외삽 점을 **버리지 않고 센다**',
            r['ready'] and 'n_front_extrapolated' in r)
        chk('P-6 ★ HV 추이가 단조 비감소',
            r['ready'] and all(a['hv_pct'] <= b_['hv_pct'] + 1e-6
                               for a, b_ in zip(r['hv_trace'], r['hv_trace'][1:])))
        s = shap_importance(n_explain=4, n_bg=6, seed=2)
        chk('P-7 ★ SHAP 히트맵 행 합이 100 %', s['ready'] and all(
            abs(sum(v) - 100.0) < 0.6 for v in s['heatmap'].values()))
        chk('P-8 ★ 유도 특징이 아니라 **자유노브**에 걸렸다',
            s['ready'] and list(s['knobs']) == list(M.FREE_KNOBS))
        chk('P-9 ★ 정확 Shapley 임을 출력이 말한다',
            s['ready'] and s['exact'] and s['n_coalitions'] == 2 ** len(M.FREE_KNOBS))
        # ── 물리 경계 계약 (2026-08-25 실사고: front 가 f_perc 103 % 를 최적해로 골랐다) ──
        B = phys_bounds()
        chk('B-1 ★ 경계는 `structure_predictor.BOUNDS` 에서 **가져온다** (사본 없음)',
            B.get('f_perc') == (0.0, 100.0) and B.get('tau') == (1.0, None))
        chk('B-2 ★ 경계 위반 판정이 양방향으로 작동',
            _oob('f_perc', 103.0, B) and not _oob('f_perc', 99.0, B)
            and _oob('tau', 0.9, B) and not _oob('tau', 1.5, B))
        chk('B-3 무경계 타깃은 위반이 없다 (§F1 — 확신 없는 경계는 걸지 않는다)',
            not _oob('mpm_plastic_gain_AM_P_tabor_pp', -5.0, B))
        r2 = pareto_explore(objectives=[('tau', 'min'), ('f_perc', 'max'), ('phi_se', 'max')],
                            n=400, seed=3)
        chk(f"B-4 ★ 경계 밖 점을 **세어 보고한다** ({r2.get('n_front_out_of_bounds')}점)",
            r2['ready'] and 'n_front_out_of_bounds' in r2)
        _ok = (r2['ready'] and (r2['balanced'] is None
                                or not r2['balanced']['out_of_bounds']))
        chk('B-5 ★★ **추천(균형점)은 경계 밖에서 안 고른다** — 최적화기는 그런 점을 선호한다',
            _ok)
        chk('B-6 ★ 왜 그 점을 골랐는지 출력에 적는다',
            r2['ready'] and isinstance(r2.get('balanced_why'), str) and r2['balanced_why'])

    print(f'\nml_shap_pareto selftest: {n[0]}/{n[1]} PASS')
    return 0 if n[0] == n[1] else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--domain', default='dem_structure')
    ap.add_argument('--shap', action='store_true', help='타깃별 정확 Shapley 중요도 히트맵')
    ap.add_argument('--pareto', action='store_true', help='다목적 Pareto front + HV 추이')
    ap.add_argument('--objectives', default='tau:min,f_perc:max',
                    help="쉼표 구분 `target:min|max` (예: 'tau:min,f_perc:max,phi_se:max')")
    ap.add_argument('--n', type=int, default=4000, help='Pareto 표본 수')
    ap.add_argument('--n-explain', type=int, default=64)
    ap.add_argument('--n-bg', type=int, default=32)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--out', default='')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    res = {}
    if a.shap:
        res['shap'] = shap_importance(a.domain, n_explain=a.n_explain, n_bg=a.n_bg, seed=a.seed)
        s = res['shap']
        if s.get('ready'):
            w = max(len(t) for t in s['targets'])
            print(f'{"타깃":{w}} ' + ' '.join(f'{k:>10}' for k in s['knobs']))
            for t in s['targets']:
                print(f'{t:{w}} ' + ' '.join(f'{v:>9.1f}%' for v in s['heatmap'][t]))
            print(f"\n  정확 Shapley · 연합 {s['n_coalitions']} · 설명점 {s['n_explain']} · 배경 {s['n_bg']}")
            if s['corr'].get('warn'):
                print(f"  ⚠ {s['corr']['warn']}")
        else:
            print('  ' + str(s.get('error')))
    if a.pareto:
        objs = [(p.split(':')[0], p.split(':')[1]) for p in a.objectives.split(',') if ':' in p]
        res['pareto'] = pareto_explore(a.domain, objectives=objs, n=a.n, seed=a.seed)
        p = res['pareto']
        if p.get('ready'):
            print(f"\n  Pareto front {p['n_front']}점 / 표본 {p['n_sampled']} · "
                  f"HV {p['hv_final_pct']}% · 외삽 {p['n_front_extrapolated']}점 · "
                  f"**물리 경계 밖 {p['n_front_out_of_bounds']}점**")
            if p['balanced']:
                print(f"  균형점: {p['balanced']['design']}")
                print(f"       →  {p['balanced']['objectives']}")
            print(f"  ({p['balanced_why']})")
        else:
            print('  ' + str(p.get('error')))
    if a.out and res:
        with open(a.out, 'w', encoding='utf-8') as f:
            json.dump(res, f, ensure_ascii=False, indent=1)
        print(f'\n  → {a.out}')
    if not (a.shap or a.pareto):
        ap.print_help()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
