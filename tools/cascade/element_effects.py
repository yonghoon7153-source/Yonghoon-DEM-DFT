#!/usr/bin/env python3
"""element_effects.py — 전구체 91 개 자료에서 '원소 X 의 효과' 를 읽는 틀 (라벨만 바꿔 끼우면 다시 돈다).

왜 (2026-10-14 · 트랙 cascade · 1저자 = 사용자)
  사용자: "어떤 원소에 의한 효과가 어땠다 이런 식의 인사이트를 못얻나" · "4축말고 여러개 빨리 뽑을 수 있는 디스크립터" ·
  "잘못된 구조여도 저걸 적용하는 코드는 정립할 수 있잖아 지금". 1단계 라벨은 결함이 있다 (잡음 · 조성 오염 · 표본 91).
  그래서 이 도구는 **라벨을 먼저 검사**하고, 통과한 라벨에만 효과 · 예측을 해석하게 만든다. 2단계 D_rel · 기준을 고친
  에너지가 나오면 `--label_csv` 로 바꿔 끼운다.

하는 일 (라벨 하나마다 · 순서대로)
  ① 라벨 관문 — 같은 전구체 안 SD ÷ 전구체 사이 SD (배치 잡음비 · 1 근처면 전구체를 못 가른다) · 음이온족 하나로 설명되는
     몫 (일원 R² · 조성 효과가 섞였는지) · 표본 수.
  ② 가법 효과 — 전구체 값 ≈ μ + 양이온 효과 + 음이온 효과 (최소제곱 · 합이 0 이 되게 중심화). 음이온 효과는 같은 양이온의
     다른 음이온 짝 (Al · Li · Mg 는 일곱 족) 으로 정해진다. 양이온 효과는 두 족 이상에 나온 양이온만 보고한다 (한 번 나온
     양이온은 잔차와 못 가른다). 구성별 라벨이면 구성을 다시 뽑는 부트스트랩으로 5–95 % 구간.
  ③ 예측 검사 — 원소 성질 특징 12 개 (≤ n/5) · ridge (λ 는 학습 폴드 안 GCV) · **양이온 통째로 빼기** · **음이온족 통째로
     빼기** · 무작위 5 겹 (누수가 얼마나 부풀리는지 비교용). Q² · 순위 상관 · 라벨 섞기 시험 (p) · 상위 10 농축.
  ④ (--dissolution) 녹아 들어가는 에너지 — 구성 − 호스트 의 조성차를 전구체 + 교환상 (Li₂S · LiCl · Li₃PS₄) 으로 정확히 닫고
     ΔE = [E(구성) + Σν E(교환상) − E(호스트) − n·E(전구체)] / n. E(구성) = N·(de + e_host). 같은 모델 (UMA) 에너지 JSON 필요.

특징 (원소 성질 · 바로 뽑는 값): 양이온 원자가 z · Shannon 반지름 r (CN6 · 그 원자가) · z/r · Pauling 전기음성도 · 주기 ·
  음이온 전하 · 음이온 반지름 · 음이온 전기음성도 · 전기음성도 차 · 양이온/음이온 비 · 화학식 원자 수 · 음이온이 호스트 음이온
  (S · Cl) 인가. 반지름 · 전기음성도는 tools/figures/plot_cascade_deep.py 의 표와 같은 값 + As³⁺ 0.58 · Sb³⁺ 0.76 (Shannon 1976).
  구조에서 뽑는 특징 (결합 길이 · 배위수 · 다면체 부피) 은 구조 파일이 있는 기계에서 만들어 `--features_csv` 로 더한다
  (열 `precursor` + 숫자 열 · 빈 값 거부 · 특징 합계 ≤ n/5 아니면 거부).

⛔ 이 도구가 못 하는 것
  · 라벨이 맞는지 모른다 — ① 관문은 잡음과 조성 효과를 재지만, 통과해도 물리적으로 옳다는 뜻이 아니다.
  · 인과를 말하지 않는다 — 효과 · 중요도는 이 표본 · 이 모델 안의 연관이다 (Honrao 2021 의 경고와 같다).
  · 농도 효과를 모른다 — 1단계는 한 농도뿐이다 (라벨 x002/x005/x010 은 농도가 아니다).
  · 구조 특징을 스스로 계산하지 않는다 · DFT · UMA 를 돌리지 않는다 (④ 는 에너지 JSON 을 받는다).
  · 1단계 라벨로 낸 숫자는 **데모**다 — 인용 금지 (`--out` 의 README 와 각 파일 머리말에 박는다).

  python3 tools/cascade/element_effects.py --selftest
  python3 tools/cascade/element_effects.py --demo --out db/raw/cascade_element_effects_demo_2026_10_14
  python3 tools/cascade/element_effects.py --label_csv <precursor,value> --better low --out <dir>
"""
import argparse
import csv
import io
import json
import math
import os
import re
import sys

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
P = os.path.join(ROOT, 'db', 'properties')
MASTER = os.path.join(P, 'cascade_all_302_2026_08_25.csv')
MAIN_FAMILIES = ('multi_category_2026_05_26_v23', 'as2s3_recover')   # x = 0.25 set (dualx_v23 is another level)
HOST_CELL = {'Li': 24, 'P': 4, 'S': 20, 'Cl': 4}                      # Stage-1 host: 4 f.u. Li6PS5Cl

# anion: formal charge · Shannon radius (CN6; N³⁻ CN4 — the only Shannon value) · Pauling EN
ANION = {'O': (2, 1.40, 3.44), 'S': (2, 1.84, 2.58), 'N': (3, 1.46, 3.04), 'F': (1, 1.33, 3.98),
         'Cl': (1, 1.81, 3.16), 'Br': (1, 1.96, 2.96), 'I': (1, 2.20, 2.66)}
HOST_ANIONS = ('S', 'Cl')
# cation Shannon radius at the valence it has in the precursor (CN6) — values of plot_cascade_deep.RAD, keyed by valence
RADIUS = {('Li', 1): 0.76, ('Na', 1): 1.02, ('Ag', 1): 1.15, ('Cu', 1): 0.77, ('Mg', 2): 0.72, ('Ca', 2): 1.00,
          ('Sr', 2): 1.18, ('Ba', 2): 1.35, ('Mn', 2): 0.83, ('Co', 2): 0.745, ('Ni', 2): 0.69, ('Zn', 2): 0.74,
          ('Al', 3): 0.535, ('Ga', 3): 0.62, ('In', 3): 0.80, ('Sc', 3): 0.745, ('Y', 3): 0.90, ('Cr', 3): 0.615,
          ('Fe', 3): 0.645, ('B', 3): 0.27, ('La', 3): 1.032, ('Nd', 3): 0.983, ('Sm', 3): 0.958, ('Gd', 3): 0.938,
          ('As', 3): 0.58, ('Sb', 3): 0.76, ('Ti', 4): 0.605, ('Zr', 4): 0.72, ('Hf', 4): 0.71, ('Si', 4): 0.40,
          ('Ge', 4): 0.53, ('Sn', 4): 0.69, ('Nb', 5): 0.64, ('Ta', 5): 0.64, ('V', 5): 0.54, ('Sb', 5): 0.60,
          ('Cr', 6): 0.44, ('Mo', 6): 0.59, ('W', 6): 0.60}
EN = {'Li': 0.98, 'Na': 0.93, 'Ag': 1.93, 'Cu': 1.90, 'Mg': 1.31, 'Ca': 1.00, 'Sr': 0.95, 'Ba': 0.89, 'Mn': 1.55,
      'Fe': 1.83, 'Co': 1.88, 'Ni': 1.91, 'Zn': 1.65, 'Al': 1.61, 'Ga': 1.81, 'In': 1.78, 'Sc': 1.36, 'Y': 1.22,
      'Cr': 1.66, 'B': 2.04, 'La': 1.10, 'Nd': 1.14, 'Sm': 1.17, 'Gd': 1.20, 'Ti': 1.54, 'Zr': 1.33, 'Hf': 1.30,
      'Si': 1.90, 'Ge': 2.01, 'Sn': 1.96, 'Nb': 1.6, 'Ta': 1.5, 'V': 1.63, 'Sb': 2.05, 'Mo': 2.16, 'W': 2.36, 'As': 2.18}
ZNUM = {'Li': 3, 'B': 5, 'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14, 'Ca': 20, 'Sc': 21, 'Ti': 22, 'V': 23, 'Cr': 24,
        'Mn': 25, 'Fe': 26, 'Co': 27, 'Ni': 28, 'Cu': 29, 'Zn': 30, 'Ga': 31, 'Ge': 32, 'As': 33, 'Sr': 38, 'Y': 39,
        'Zr': 40, 'Nb': 41, 'Mo': 42, 'Ag': 47, 'In': 49, 'Sn': 50, 'Sb': 51, 'Ba': 56, 'La': 57, 'Nd': 60, 'Sm': 62,
        'Gd': 64, 'Hf': 72, 'Ta': 73, 'W': 74}
FEATURES = ['z_cat', 'r_cat', 'z_over_r', 'en_cat', 'period_cat', 'z_an', 'r_an', 'en_an', 'd_en',
            'cat_per_an', 'atoms_per_fu', 'host_anion']
RESERVOIRS = {'Li2S': {'Li': 2, 'S': 1}, 'LiCl': {'Li': 1, 'Cl': 1}, 'Li3PS4': {'Li': 3, 'P': 1, 'S': 4}}


def base(name):
    return name.split('+')[0]


def parse_precursor(f):
    """'Al2O3' → cation Al ×2, anion O ×3, valences. Refuses a formula without exactly one anion of the table."""
    toks = [(e, int(n) if n else 1) for e, n in re.findall(r'([A-Z][a-z]?)(\d*)', f)]
    an = [t for t in toks if t[0] in ANION]
    ca = [t for t in toks if t[0] not in ANION]
    if len(an) != 1 or len(ca) != 1:
        raise ValueError(f'{f}: expected one cation and one anion of {sorted(ANION)}')
    (m, a), (x, b) = ca[0], an[0]
    zx = ANION[x][0]
    z = zx * b / a
    if abs(z - round(z)) > 1e-9:
        raise ValueError(f'{f}: non-integer cation valence {z}')
    return {'cation': m, 'anion': x, 'a': a, 'b': b, 'z_cat': int(round(z)), 'z_an': zx}


def period(zn):
    return 1 if zn <= 2 else 2 if zn <= 10 else 3 if zn <= 18 else 4 if zn <= 36 else 5 if zn <= 54 else 6


def features(f):
    d = parse_precursor(f)
    m, x, z = d['cation'], d['anion'], d['z_cat']
    if (m, z) not in RADIUS or m not in EN or m not in ZNUM:
        raise KeyError(f'{f}: no radius/EN/Z for {m}{z}+ — add it to the tables with its source, never a default')
    r = RADIUS[(m, z)]
    zx, rx, ex = ANION[x]
    return {'z_cat': z, 'r_cat': r, 'z_over_r': z / r, 'en_cat': EN[m], 'period_cat': period(ZNUM[m]),
            'z_an': zx, 'r_an': rx, 'en_an': ex, 'd_en': ex - EN[m], 'cat_per_an': d['a'] / d['b'],
            'atoms_per_fu': d['a'] + d['b'], 'host_anion': 1.0 if x in HOST_ANIONS else 0.0}


# ---------------------------------------------------------------- labels
def load_stage1(path=MASTER, report=None):
    """Main-family rows, one per configuration name. as2s3_recover re-ran the 15 AlI3 configurations of v23 (same names ·
    de equal to ≤ 1e-4 eV/atom) — the v23 row is kept (MAIN_FAMILIES order). `report` (dict) gets the dropped names."""
    with open(path, encoding='utf-8') as fh:
        rows = [r for r in csv.DictReader(fh) if r['family'] in MAIN_FAMILIES]
    rows.sort(key=lambda r: MAIN_FAMILIES.index(r['family']))          # stable: file order kept inside a family
    seen, out, dropped = set(), [], []
    for r in rows:
        if r['name'] in seen:
            dropped.append((r['family'], r['name']))
            continue
        seen.add(r['name'])
        out.append(r)
    if report is not None:
        report['dropped_duplicates'] = dropped
    return out


def slot(name):
    """Stage-1 x020 · x050 · x100 are not concentrations: the three names of a (precursor · site variant · seed) slot carry
    the same composition (1,220 slots × 3 · 2026-10-14). 807 slots agree to 0.1 meV/atom, 127 differ by > 1 meV/atom."""
    return re.sub(r'_x\d{3}(?=_|$)', '', name)


def config_label(rows, col, collapse=True):
    """{precursor: [one value per configuration]} for a Stage-1 column (blank / non-numeric skipped). collapse=True takes the
    median of the x-label copies of a slot — counting the copies as three configurations made bootstrap bands too narrow."""
    by = {}
    for r in rows:
        try:
            v = float(r[col])
        except (TypeError, ValueError):
            continue
        if math.isfinite(v):
            by.setdefault((base(r['dopant']), slot(r['name']) if collapse else r['name']), []).append(v)
    out = {}
    for (p, _), vals in sorted(by.items()):
        out.setdefault(p, []).append(float(np.median(vals)))
    return out


def interface_delta(cathode, voltage=None):
    """MP-phase interface reaction energy of each doped composition minus that of the host Li6PS5Cl (same
    condition): dopant's change of reactivity. Rank-1 first row per precursor (the cascade rule)."""
    if cathode in ('Li_metal', 'carbon'):
        src = 'cascade_interface_li.jsonl' if cathode == 'Li_metal' else 'cascade_interface_carbon.jsonl'
        rec = [json.loads(x) for x in open(os.path.join(P, src), encoding='utf-8') if x.strip()]
        host = [json.loads(x) for x in open(os.path.join(P, 'cascade_interface_baseline_closed.jsonl'), encoding='utf-8')
                if x.strip()]
        h = [float(r['dE_eV_per_atom']) for r in host if r['species'] == 'LPSCl' and r['cathode'] == cathode]
        val = {r['species']: float(r['dE_eV_per_atom']) for r in rec}
    else:
        rec = [json.loads(x) for x in open(os.path.join(P, 'cascade_interface_90.jsonl'), encoding='utf-8') if x.strip()]
        host = [json.loads(x) for x in open(os.path.join(P, 'cascade_interface_baseline.jsonl'), encoding='utf-8')
                if x.strip()]
        h = [float(r['by_voltage'][voltage]['dE_eV_per_atom']) for r in host if r['species'] == 'LPSCl' and r['cathode'] == cathode]
        bad = sorted(r['species'] for r in rec if r['cathode'] == cathode and 'error' in r)
        if bad:
            raise ValueError(f'{cathode}: {len(bad)} rows carry an error ({bad[:4]} …) — rerun them, never drop them silently')
        val = {r['species']: float(r['by_voltage'][voltage]['dE_eV_per_atom']) for r in rec if r['cathode'] == cathode}
    if len(h) != 1:
        raise ValueError(f'host baseline for {cathode} {voltage}: {len(h)} rows')
    return {k: v - h[0] for k, v in val.items()}


def composition_probe(rows, col):
    """Configuration-level Spearman of a label with the net atoms swapped (N_cell − 52) and the Li removed (Li − 24).
    For a per-atom energy without element references this is the confound's signature; for transport it is physics
    (Li vacancies) — so it is reported next to the gate, not used as a verdict."""
    v, dn, dli = [], [], []
    for r in rows:
        try:
            y = float(r[col])
        except (TypeError, ValueError):
            continue
        if not math.isfinite(y):
            continue
        comp = {k[12:]: float(r[k]) for k in r if k.startswith('composition_') and r[k] not in ('', None)}
        v.append(y)
        dn.append(sum(comp.values()) - sum(HOST_CELL.values()))
        dli.append(comp.get('Li', 0.0) - HOST_CELL['Li'])
    return {'n_configs': len(v), 'spearman_vs_dN_atoms': spearman(v, dn), 'spearman_vs_dLi': spearman(v, dli)}


# ---------------------------------------------------------------- ① gate
def label_gate(per_config, prec_value):
    """within-precursor SD ÷ between-precursor SD (configuration labels only) and the one-way R² of anion family."""
    out = {'n_precursors': len(prec_value)}
    multi = {k: v for k, v in (per_config or {}).items() if len(v) >= 2}
    if multi:
        within = math.sqrt(float(np.mean([np.var(v) for v in multi.values()])))
        between = float(np.std([np.mean(v) for v in multi.values()]))
        out.update(noise_ratio=within / between if between > 0 else float('inf'), within_sd=within, between_sd=between,
                   n_configs=sum(len(v) for v in multi.values()))
    y = np.array([prec_value[k] for k in prec_value])
    fam = [parse_precursor(k)['anion'] for k in prec_value]
    ss = float(((y - y.mean()) ** 2).sum())
    ssw = sum(float(((y[[i for i, f in enumerate(fam) if f == g]] - y[[i for i, f in enumerate(fam) if f == g]].mean()) ** 2).sum())
              for g in set(fam))
    out['anion_family_R2'] = 1 - ssw / ss if ss > 0 else float('nan')
    out['family_means'] = {g: float(np.mean([prec_value[k] for k, f in zip(prec_value, fam) if f == g])) for g in sorted(set(fam))}
    return out


# ---------------------------------------------------------------- ② additive effects
def additive_effects(prec_value):
    """y_p = μ + a_cation + b_anion, least squares (minimum norm), effects centred to sum zero within each factor."""
    keys = sorted(prec_value)
    info = {k: parse_precursor(k) for k in keys}
    cats = sorted({info[k]['cation'] for k in keys})
    ans = sorted({info[k]['anion'] for k in keys})
    X = np.zeros((len(keys), 1 + len(cats) + len(ans)))
    X[:, 0] = 1
    for i, k in enumerate(keys):
        X[i, 1 + cats.index(info[k]['cation'])] = 1
        X[i, 1 + len(cats) + ans.index(info[k]['anion'])] = 1
    y = np.array([prec_value[k] for k in keys])
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    a, b = beta[1:1 + len(cats)], beta[1 + len(cats):]
    a, b = a - a.mean(), b - b.mean()
    n_fam = {c: len({info[k]['anion'] for k in keys if info[k]['cation'] == c}) for c in cats}
    resid = y - X @ beta
    return ({c: float(v) for c, v in zip(cats, a)}, {x: float(v) for x, v in zip(ans, b)}, n_fam,
            float(np.sqrt((resid ** 2).sum() / max(1, len(y) - np.linalg.matrix_rank(X)))))


def bootstrap_effects(per_config, agg, n_boot, rng):
    """5–95 % band of the anion / cation effects by resampling configurations within each precursor."""
    A, B = {}, {}
    for _ in range(n_boot):
        pv = {k: agg(rng.choice(v, size=len(v), replace=True)) for k, v in per_config.items()}
        a, b, _, _ = additive_effects(pv)
        for k, v in a.items():
            A.setdefault(k, []).append(v)
        for k, v in b.items():
            B.setdefault(k, []).append(v)
    band = lambda d: {k: (float(np.percentile(v, 5)), float(np.percentile(v, 95))) for k, v in d.items()}
    return band(A), band(B)


# ---------------------------------------------------------------- ③ prediction
def ridge_gcv(X, y, grid=np.logspace(-3, 3, 25), lam=None):
    """Ridge on standardized X with λ by generalized cross-validation (or a fixed `lam`); returns (coef, intercept, λ)."""
    mu, sd = X.mean(0), X.std(0)
    sd[sd == 0] = 1
    Z = (X - mu) / sd
    ym = y.mean()
    yc = y - ym
    U, s, Vt = np.linalg.svd(Z, full_matrices=False)
    if lam is None:
        best = None
        for g in grid:
            d = s ** 2 / (s ** 2 + g)
            fit = U @ (d * (U.T @ yc))
            gcv = len(y) * ((yc - fit) ** 2).sum() / (len(y) - d.sum()) ** 2
            if best is None or gcv < best[0]:
                best = (gcv, g)
        lam = best[1]
    w = Vt.T @ ((s / (s ** 2 + lam)) * (U.T @ yc))
    return w / sd, ym - (mu / sd) @ w, lam


def grouped_cv(X, y, groups, lam=None):
    """Each group is held out whole; λ is chosen inside the training part only (no peeking at the held-out group)."""
    pred = np.full(len(y), np.nan)
    for g in sorted(set(groups)):
        te = np.array([gg == g for gg in groups])
        if te.all():
            continue
        coef, icpt, _ = ridge_gcv(X[~te], y[~te], lam=lam)
        pred[te] = X[te] @ coef + icpt
    ok = np.isfinite(pred)
    q2 = 1 - ((y[ok] - pred[ok]) ** 2).sum() / ((y[ok] - y[ok].mean()) ** 2).sum()
    return pred, float(q2), spearman(pred[ok], y[ok])


def rank_avg(a):
    """Ranks with ties averaged (blocking fractions tie often — ordinal ranks would order ties by row)."""
    a = np.asarray(a, float)
    r = np.empty(len(a))
    r[np.argsort(a, kind='mergesort')] = np.arange(len(a))
    _, inv, cnt = np.unique(a, return_inverse=True, return_counts=True)
    return (np.bincount(inv, weights=r) / cnt)[inv]


def spearman(a, b):
    return float(np.corrcoef(rank_avg(a), rank_avg(b))[0, 1])


def enrichment(pred, y, better, k=10, top_frac=0.25):
    """How many of the true best quarter are in the predicted best k, over the random expectation."""
    sgn = 1 if better == 'low' else -1
    true_top = set(np.argsort(sgn * y)[:max(1, int(round(top_frac * len(y))))])
    pick = np.argsort(sgn * pred)[:k]
    hit = sum(1 for i in pick if i in true_top)
    return hit / (k * top_frac)


def permutation_p(X, y, groups, n, rng, obs):
    null = [grouped_cv(X, rng.permutation(y), groups)[1] for _ in range(n)]
    return (1 + sum(1 for v in null if v >= obs)) / (1 + n), float(np.mean(null))


def load_extra(path):
    """Extra per-precursor features (structure descriptors made elsewhere): CSV with a `precursor` column + numeric columns."""
    with open(path, encoding='utf-8') as fh:
        rows = list(csv.DictReader(l for l in fh if not l.startswith('#')))
    names = [c for c in rows[0] if c != 'precursor']
    clash = sorted(set(names) & set(FEATURES))
    if clash:
        raise ValueError(f'{path}: columns {clash} shadow the element features')
    return {'names': names, 'values': {r['precursor']: [float(r[c]) for c in names] for r in rows}}


def design(keys, extra=None, use=None):
    """Feature matrix: the element features in `use` (default all 12) + extra columns. Refuses an unknown name, a
    missing extra value, and more than n/5 columns — a 40-candidate Stage-2 label must pick ≤ 8 with --features."""
    use = list(use or FEATURES)
    unknown = [f for f in use if f not in FEATURES]
    if unknown:
        raise ValueError(f'unknown element features {unknown} — choose from {FEATURES}')
    names = use + (extra['names'] if extra else [])
    X = [[features(k)[f] for f in use] for k in keys]
    if extra:
        miss = [k for k in keys if k not in extra['values'] or not all(map(math.isfinite, extra['values'][k]))]
        if miss:
            raise ValueError(f'extra features missing for {len(miss)} precursors ({miss[:4]} …) — never filled with a default')
        X = [x + extra['values'][k] for x, k in zip(X, keys)]
    X = np.array(X, float)
    if X.shape[1] != len(names):
        raise RuntimeError(f'design matrix has {X.shape[1]} columns for {len(names)} names')
    if len(names) > len(keys) // 5:
        raise ValueError(f'{len(names)} features for {len(keys)} precursors — keep it ≤ n/5 = {len(keys) // 5} '
                         f'(Sendek 2017): pick a subset with --features')
    return X, names


def predict_report(prec_value, better, n_perm, rng, extra=None, use=None):
    keys = sorted(prec_value)
    X, names = design(keys, extra, use)
    y = np.array([prec_value[k] for k in keys])
    info = [parse_precursor(k) for k in keys]
    rep = {'n': len(keys), 'n_features': len(names), 'features': names}
    for name, groups in (('leave_one_cation_out', [i['cation'] for i in info]),
                         ('leave_one_anion_family_out', [i['anion'] for i in info]),
                         ('random_5fold', [i % 5 for i in rng.permutation(len(keys))])):
        pred, q2, rho = grouped_cv(X, y, groups)
        r = {'Q2': q2, 'spearman': rho}
        if name == 'leave_one_cation_out':
            r['enrichment_top10'] = enrichment(pred, y, better)
            r['perm_p'], r['perm_null_Q2_mean'] = permutation_p(X, y, groups, n_perm, rng, q2)
        rep[name] = r
    coef, _, lam = ridge_gcv(X, y)
    sd = X.std(0)
    rep['ridge_lambda_full'] = lam
    rep['standardized_coef'] = {f: float(c * s) for f, c, s in zip(names, coef, sd)}
    return rep


# ---------------------------------------------------------------- ④ dissolution energy
def key_element(prec):
    """The element that counts precursor units: its first element no reservoir carries (cation first, then anion);
    Li only when every element is a host element (Li₂S · LiCl). Li₂O · LiF · Li₃N are counted by O · F · N — counting them
    by Li gave n = 0 whenever the anion swaps onto a host anion site."""
    res = {e for r in RESERVOIRS.values() for e in r}
    foreign = [e for e in prec if e not in res]
    return ([e for e in foreign if e not in ANION] + [e for e in foreign if e in ANION] + ['Li'])[0]


def balance(config, host, prec):
    """config − host = n·precursor − Σ ν_k reservoir_k. Returns (n, {reservoir: ν}); raises if it does not close."""
    els = sorted(set(config) | set(host) | set(prec) | {e for r in RESERVOIRS.values() for e in r})
    d = np.array([config.get(e, 0) - host.get(e, 0) for e in els], float)
    pv = np.array([prec.get(e, 0) for e in els], float)
    k = key_element(prec)
    n = d[els.index(k)] / prec[k]
    R = np.array([[RESERVOIRS[k].get(e, 0) for k in RESERVOIRS] for e in els], float)
    rhs = -(d - n * pv)
    nu, *_ = np.linalg.lstsq(R, rhs, rcond=None)
    if np.abs(R @ nu - rhs).max() > 1e-8 or n <= 0:
        raise ValueError(f'composition does not close with {list(RESERVOIRS)} (n = {n})')
    return float(n), {k: float(v) for k, v in zip(RESERVOIRS, nu)}


def dissolution_energy(config, de_per_atom, e_host_per_atom, prec, e_prec_fu, e_res_fu, host=HOST_CELL):
    """ΔE per precursor unit for host + n·precursor → configuration + Σν reservoirs (energies of one model)."""
    n, nu = balance(config, host, prec)
    n_c, n_h = sum(config.values()), sum(host.values())
    e_conf = n_c * (de_per_atom + e_host_per_atom)
    e_host = n_h * e_host_per_atom
    return (e_conf + sum(v * e_res_fu[k] for k, v in nu.items()) - e_host - n * e_prec_fu) / n, n, nu


# ---------------------------------------------------------------- run
def write_csv(path, header, cols, rows):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        for h in header:
            f.write('# ' + h + '\n')
        w = csv.writer(f)
        w.writerow(cols)
        w.writerows(rows)


def _band(band, k):
    """Two CSV cells for a 5–95 % band — blank when the label has one value per precursor (nothing to resample)."""
    return [f'{q:.5g}' for q in band[k]] if band else ['', '']


def analyse(name, per_config, prec_value, better, out, n_boot, n_perm, rng, demo_note, probe=None, extra=None, use=None):
    gate = label_gate(per_config, prec_value)
    if probe:
        gate['composition_probe'] = probe
    a, b, n_fam, rmse = additive_effects(prec_value)
    band_a = band_b = None
    if per_config:
        agg = np.median
        band_a, band_b = bootstrap_effects(per_config, agg, n_boot, rng)
    pred = predict_report(prec_value, better, n_perm, rng, extra, use)
    res = {'label': name, 'better': better, 'demo_note': demo_note, 'gate': gate, 'additive_rmse': rmse, 'prediction': pred,
           'anion_effects': {x: {'effect': v, 'band_5_95': band_b.get(x) if band_b else None} for x, v in b.items()},
           'cation_effects_multi_family': {c: {'effect': v, 'n_families': n_fam[c], 'band_5_95': band_a.get(c) if band_a else None}
                                           for c, v in a.items() if n_fam[c] >= 2}}
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, f'{name}.json'), 'w', encoding='utf-8') as f:
        json.dump(res, f, indent=1, ensure_ascii=False)
    write_csv(os.path.join(out, f'{name}_anion_effects.csv'), [demo_note, f'label {name} · additive model · effects centred'],
              ['anion', 'effect', 'band5', 'band95'],
              [[x, f'{v:.5g}', *_band(band_b, x)] for x, v in sorted(b.items(), key=lambda t: t[1])])
    write_csv(os.path.join(out, f'{name}_cation_effects.csv'), [demo_note, 'cations seen in >= 2 anion families only'],
              ['cation', 'n_families', 'effect', 'band5', 'band95'],
              [[c, n_fam[c], f'{v:.5g}', *_band(band_a, c)] for c, v in sorted(a.items(), key=lambda t: t[1]) if n_fam[c] >= 2])
    return res


TITLES = {'energy_de_per_atom': ('Energy per atom vs host', 'eV/atom'),
          'dopant_blocking_fraction': ('Dopant blocking fraction', 'fraction'),
          'young_modulus_GPa': ("Young's modulus", 'GPa'),
          'interface_vs_Li_metal_minus_host': ('Li-metal interface, doped − host', 'eV/atom'),
          'interface_vs_LCO_4V_minus_host': ('LCO interface at 4.0 V, doped − host', 'eV/atom')}
CV_COLS = (('leave_one_cation_out', 'leave one cation out', '#374151'),
           ('leave_one_anion_family_out', 'leave one anion family out', '#9ca3af'),
           ('random_5fold', 'random 5-fold', '#e5e7eb'))


def summary_rows(results):
    """One row per label: gate + cross-validation numbers (the figure's last panel and the Origin CSV)."""
    out = []
    for r in results:
        g, p_ = r['gate'], r['prediction']
        nr = g.get('noise_ratio')
        out.append([r['label'], g['n_precursors'], '' if nr is None else f'{nr:.4g}', f"{g['anion_family_R2']:.4g}",
                    *(f"{p_[k]['Q2']:.4g}" for k, _, _ in CV_COLS),
                    f"{p_['leave_one_cation_out']['perm_p']:.4g}", f"{p_['leave_one_cation_out']['enrichment_top10']:.4g}"])
    return out


def figure(results, out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    sys.path.insert(0, ROOT)
    from tools.figures.house_style import INK, MUT, apply_axes
    n = len(results) + 1
    ncol = 3
    nrow = -(-n // ncol)
    fig, axes = plt.subplots(nrow, ncol, figsize=(3.3 * ncol, 3.0 * nrow), squeeze=False)
    flat = axes.ravel()
    order = ['O', 'F', 'N', 'Cl', 'S', 'Br', 'I']
    for ax, res in zip(flat, results):
        eff = res['anion_effects']
        xs = [x for x in order if x in eff]
        v = [eff[x]['effect'] for x in xs]
        col = ['#6b7280' if x in HOST_ANIONS else '#d1d5db' for x in xs]
        kw = {}
        if all(eff[x]['band_5_95'] for x in xs):
            kw = dict(yerr=[[eff[x]['effect'] - eff[x]['band_5_95'][0] for x in xs],
                            [eff[x]['band_5_95'][1] - eff[x]['effect'] for x in xs]],
                      capsize=3, error_kw={'ecolor': INK, 'lw': 0.8})
        ax.bar(range(len(xs)), v, 0.62, color=col, edgecolor=INK, linewidth=0.8, **kw)
        ax.axhline(0, color=MUT, lw=0.8)
        ax.set_xticks(range(len(xs)), xs)
        title, unit = TITLES.get(res['label'], (res['label'], 'label units'))
        apply_axes(ax, ylabel=f'anion effect ({unit})', fontsize=8.5)
        ax.tick_params(labelsize=8)
        ax.set_title(title, fontsize=9.5, color=INK, pad=16)
        g = res['gate']
        nr = g.get('noise_ratio')
        ax.text(0.5, 1.01, f"noise {'—' if nr is None else f'{nr:.2f}'} · family R² {g['anion_family_R2']:.2f} · "
                f"Q² {res['prediction']['leave_one_cation_out']['Q2']:.2f}",
                transform=ax.transAxes, ha='center', va='bottom', fontsize=7, color=MUT)
    ax = flat[len(results)]
    w = 0.26
    for j, (k, lab, c) in enumerate(CV_COLS):
        ax.barh([i + (j - 1) * w for i in range(len(results))], [r['prediction'][k]['Q2'] for r in results], w,
                color=c, edgecolor=INK, linewidth=0.6, label=lab)
    ax.set_yticks(range(len(results)), [TITLES.get(r['label'], (r['label'],))[0].replace(', doped − host', '')
                                        for r in results], fontsize=7)
    ax.set_ylim(len(results) - 0.5, -1.8)      # inverted, with a free strip on top for the legend
    ax.plot([0, 0], [len(results) - 0.5, -0.5], color=MUT, lw=0.8)
    apply_axes(ax, xlabel='cross-validated Q²', fontsize=8.5)
    ax.tick_params(axis='x', labelsize=8)
    ax.set_title('Prediction from element features', fontsize=9.5, color=INK, pad=16)
    ax.legend(fontsize=6.5, frameon=False, loc='upper left', bbox_to_anchor=(0.0, 1.0))
    for ax in flat[len(results) + 1:]:
        ax.axis('off')
    fig.suptitle('DEMO on flawed Stage-1 labels (code test, not a result) · dark bars = host anions S, Cl · '
                 'error bars = 5–95 % configuration bootstrap', fontsize=8, color=MUT)
    fig.tight_layout()
    p = os.path.join(out, 'anion_effects_demo.png')
    fig.savefig(p, dpi=300)
    write_csv(os.path.join(out, 'summary_gate_cv.csv'),
              ['DEMO on flawed Stage-1 labels — tests the code, not the chemistry. Not citable.',
               'noise_ratio = within-precursor SD / between-precursor SD (blank = one value per precursor)',
               'Q2 columns = cross-validated ridge on 12 element features; perm_p and enrichment are leave-one-cation-out'],
              ['label', 'n_precursors', 'noise_ratio', 'anion_family_R2', 'Q2_leave_one_cation_out',
               'Q2_leave_one_anion_family_out', 'Q2_random_5fold', 'perm_p_LOCO', 'enrichment_top10_LOCO'],
              summary_rows(results))
    return p


def demo(out, n_boot, n_perm, seed, extra=None):
    rng = np.random.default_rng(seed)
    rows = load_stage1()
    note = ('DEMO on Stage-1 labels (2026-10-14): the labels are flawed (configuration noise, composition-referenced '
            'energy, one dopant level, n = 91) — this tests the code, not the chemistry. Not citable.')
    runs = []
    for name, col, better in (('energy_de_per_atom', 'screen_de_per_atom', 'low'),
                              ('dopant_blocking_fraction', 'tier2_dopant_blocking_fraction', 'low'),
                              ('young_modulus_GPa', 'elastic_E_young_GPa', 'low')):
        pc = config_label(rows, col)
        pv = {k: float(np.median(v)) for k, v in pc.items()}
        runs.append(analyse(name, pc, pv, better, out, n_boot, n_perm, rng, note, composition_probe(rows, col), extra))
    for name, cat, volt in (('interface_vs_Li_metal_minus_host', 'Li_metal', None),
                            ('interface_vs_LCO_4V_minus_host', 'LCO', '4.00')):
        pv = interface_delta(cat, volt)
        runs.append(analyse(name, None, pv, 'high', out, n_boot, n_perm, rng,
                            note + ' MP-phase reaction energy per atom of the mixture, doped minus host Li6PS5Cl.', None, extra))
    fig = figure(runs, out)
    import hashlib
    src = [MASTER] + [os.path.join(P, f) for f in ('cascade_interface_90.jsonl', 'cascade_interface_li.jsonl',
                                                    'cascade_interface_baseline.jsonl', 'cascade_interface_baseline_closed.jsonl')]
    sha = {os.path.relpath(f, ROOT): hashlib.sha256(open(f, 'rb').read()).hexdigest() for f in src}
    with open(os.path.join(out, 'README.md'), 'w', encoding='utf-8') as f:
        f.write('# element_effects demo (2026-10-14)\n\n' + note + '\n\n'
                f'Made by `tools/cascade/element_effects.py --demo --seed {seed} --n_boot {n_boot} --n_perm {n_perm}`. '
                'One JSON + two CSVs per label; '
                f'`{os.path.basename(fig)}` = anion effects with 5–95 % bands (configuration bootstrap; interface labels have '
                'one value per precursor, so no band).\n\nConfigurations: one per slot — the x020 · x050 · x100 names of a '
                '(precursor · site variant · seed) are copies of one composition, so their median is one configuration; '
                'the 15 AlI3 rows that as2s3_recover re-ran are counted once (v23 rows).\n\nInputs (sha256):\n\n'
                + ''.join(f'- `{k}` {v}\n' for k, v in sha.items()))
    return runs


def _selftest():
    import tempfile
    rng = np.random.default_rng(0)
    ok = []

    def chk(c, m):
        ok.append(bool(c))
        print(('  ✓ ' if c else '  ✗ ') + m)
    # features: parsing, valence, refusals
    f = features('Al2O3')
    chk(f['z_cat'] == 3 and abs(f['r_cat'] - 0.535) < 1e-12 and f['host_anion'] == 0, 'Al2O3 → Al³⁺ 0.535 Å · O not a host anion')
    chk(features('Sb2S3')['r_cat'] == 0.76 and features('Sb2O5')['r_cat'] == 0.60, 'Sb³⁺ / Sb⁵⁺ get their own radii')
    for bad in ('LiClO4', 'Xx2O3', 'FeO'):   # FeO: Fe is known, Fe²⁺ radius is not in the table
        try:
            features(bad)
            chk(False, f'{bad} refused')
        except (ValueError, KeyError):
            chk(True, f'{bad} refused (no silent default)')
    # ② additive effects recover a planted anion effect; one-family cations are not reported
    eff = {'O': -0.3, 'S': 0.1, 'Cl': 0.2}
    cat = {'Al': 0.05, 'Mg': -0.05, 'Li': 0.0}
    pv = {}
    for c, z in (('Al', 3), ('Mg', 2), ('Li', 1)):
        for x, zx in (('O', 2), ('S', 2), ('Cl', 1)):
            a, b = (2, 3) if z * 2 == 6 and zx == 2 else (1, z) if zx == 1 else (zx // math.gcd(z, zx), z // math.gcd(z, zx))
            form = f'{c}{a if a > 1 else ""}{x}{b if b > 1 else ""}'
            pv[form] = 1.0 + eff[x] + cat[c]
    a_, b_, nf, rmse = additive_effects(pv)
    centred = {x: v - np.mean(list(eff.values())) for x, v in eff.items()}
    chk(all(abs(b_[x] - centred[x]) < 1e-9 for x in eff) and rmse < 1e-9, 'additive model recovers planted anion effects exactly')
    # ③ grouped CV: a real elemental signal is found; shuffled labels are not; random folds inflate when a cation repeats
    keys = sorted({'Al2O3', 'Al2S3', 'AlCl3', 'AlF3', 'AlBr3', 'AlI3', 'AlN', 'Li2O', 'Li2S', 'LiCl', 'LiF', 'LiBr', 'LiI', 'Li3N',
                   'MgO', 'MgS', 'MgCl2', 'MgF2', 'MgBr2', 'MgI2', 'Mg3N2', 'Sc2O3', 'Y2O3', 'La2O3', 'Ga2O3', 'In2O3', 'B2O3',
                   'SiO2', 'GeO2', 'SnO2', 'TiO2', 'ZrO2', 'HfO2', 'Nb2O5', 'Ta2O5', 'CaO', 'SrO', 'BaO', 'ZnO', 'NiO',
                   'CoO', 'MnO', 'CaCl2', 'SrCl2', 'BaCl2', 'YCl3', 'LaCl3', 'ScCl3', 'GaCl3', 'NdCl3', 'TiCl4', 'ZrCl4'})
    small = ['z_cat', 'r_cat', 'z_over_r', 'en_cat', 'z_an', 'r_an', 'en_an', 'cat_per_an', 'host_anion']   # 52 keys → ≤ 10
    sig = {k: 0.8 * features(k)['en_an'] - 0.5 * features(k)['z_over_r'] + rng.normal(0, 0.05) for k in keys}
    rep = predict_report(sig, 'low', 59, rng, use=small)
    chk(rep['leave_one_cation_out']['Q2'] > 0.5 and abs(rep['leave_one_cation_out']['perm_p'] - 1 / 60) < 1e-12,
        f"planted signal found under leave-one-cation-out (Q² {rep['leave_one_cation_out']['Q2']:.2f} · p {rep['leave_one_cation_out']['perm_p']:.3f})")
    noise = {k: float(rng.normal()) for k in keys}
    repn = predict_report(noise, 'low', 59, rng, use=small)
    chk(repn['leave_one_cation_out']['Q2'] < 0.2 and repn['leave_one_cation_out']['perm_p'] > 0.05,
        f"pure noise not found (Q² {repn['leave_one_cation_out']['Q2']:.2f} · p {repn['leave_one_cation_out']['perm_p']:.2f})")
    # held-out rows never reach the fit: with almost no shrinkage, 12 features fit noise in-sample (R² ≈ p/n) but not out of it
    Xs = np.array([[features(k)[f] for f in FEATURES] for k in keys[:24]], float)
    yn = rng.normal(size=24)
    q_out = grouped_cv(Xs, yn, list(range(24)), lam=1e-6)[1]
    coef, icpt, _ = ridge_gcv(Xs, yn, lam=1e-6)
    r2_in = 1 - ((yn - Xs @ coef - icpt) ** 2).sum() / ((yn - yn.mean()) ** 2).sum()
    chk(q_out < 0 < r2_in - 0.3, f'no leakage: noise in-sample R² {r2_in:.2f} · held-out Q² {q_out:.2f}')
    # enrichment: perfect ranking = 1/top_frac, reversed = 0, and 'better' flips it
    yy = rng.normal(size=60)
    yh = np.arange(60.0)
    ph = yh.copy()
    ph[:45] = rng.uniform(0, 40, 45)        # only the high end is ranked right — 'high' must see it, 'low' must not
    chk(enrichment(yy, yy, 'low') == 4 and enrichment(-yy, yy, 'low') == 0 and enrichment(ph, yh, 'high') == 4
        and enrichment(ph, yh, 'low') < 4, 'enrichment 4 for a perfect ranking · 0 reversed · direction honoured')
    chk(abs(spearman([1, 2, 2, 3], [1, 2, 2, 3]) - 1) < 1e-12 and abs(spearman([0, 0, 0, 1], [3, 2, 1, 4]) - 0.7745966692) < 1e-6,
        'Spearman averages ties')
    # ① gate: configuration SD 0.5 over a precursor spread of 1 gives a ratio ≈ 0.5; clean labels ≈ 0
    pc = {k: list(v + rng.normal(0, 0.5, 20)) for k, v in zip(keys, rng.normal(0, 1.0, len(keys)))}
    g = label_gate(pc, {k: float(np.median(v)) for k, v in pc.items()})
    pc2 = {k: list(v + rng.normal(0, 0.01, 20)) for k, v in zip(keys, rng.normal(0, 1.0, len(keys)))}
    g2 = label_gate(pc2, {k: float(np.median(v)) for k, v in pc2.items()})
    chk(0.38 < g['noise_ratio'] < 0.62 and g2['noise_ratio'] < 0.05, f"noise ratio ≈ 0.5 for SD 0.5 ({g['noise_ratio']:.2f}) · ≈ 0 for clean ({g2['noise_ratio']:.3f})")
    fam = {k: (-1.0 if parse_precursor(k)['anion'] == 'O' else 0.0) + rng.normal(0, 0.01) for k in keys}
    chk(label_gate(None, fam)['anion_family_R2'] > 0.95, 'a label made of the anion family alone shows family R² ≈ 1')
    # ④ balance: the Al2O3 example closes both ways; a foreign element does not
    n, nu = balance({'Li': 18, 'Al': 2, 'O': 3, 'Cl': 4, 'P': 4, 'S': 17}, HOST_CELL, {'Al': 2, 'O': 3})
    chk(abs(n - 1) < 1e-12 and abs(nu['Li2S'] - 3) < 1e-9 and abs(nu['LiCl']) < 1e-9 and abs(nu['Li3PS4']) < 1e-9,
        'Li18Al2O3Cl4P4S17: host + Al2O3 → config + 3 Li2S')
    n, nu = balance({'Li': 17, 'Al': 2, 'O': 3, 'Cl': 5, 'P': 4, 'S': 16}, HOST_CELL, {'Al': 2, 'O': 3})
    chk(abs(nu['Li2S'] - 4) < 1e-9 and abs(nu['LiCl'] + 1) < 1e-9, 'Li17Al2O3Cl5P4S16: + 4 Li2S − 1 LiCl')
    n, nu = balance({'Li': 24, 'O': 1, 'Cl': 4, 'P': 4, 'S': 19}, HOST_CELL, {'Li': 2, 'O': 1})
    chk(abs(n - 1) < 1e-12 and abs(nu['Li2S'] - 1) < 1e-9, 'Li2O with O on an S site counts by O: host + Li2O → config + Li2S')
    n, nu = balance({'Li': 25, 'Cl': 5, 'P': 4, 'S': 20}, HOST_CELL, {'Li': 1, 'Cl': 1})
    chk(abs(n - 1) < 1e-12 and all(abs(v) < 1e-9 for v in nu.values()), 'LiCl (host elements only) counts by Li')
    cr = [{'dopant': 'MgO', 'name': f'MgO_{x}_cLi24gaS16e_s0{k}', 'v': str(5.0 if (x, k) == ('x100', 1) else v)}
          for x in ('x020', 'x050', 'x100') for k, v in ((0, 1.0), (1, 2.0))]
    chk(slot('AlI3_x020_s04') == 'AlI3_s04' and slot('MgO_x050_cLi24gaS16e_s01') == 'MgO_cLi24gaS16e_s01'
        and sorted(config_label(cr, 'v')['MgO']) == [1.0, 2.0]
        and sorted(config_label(cr, 'v', collapse=False)['MgO']) == [1.0, 1.0, 1.0, 2.0, 2.0, 5.0],
        'x-label copies collapse to one configuration per slot (median · one odd copy does not move it)')
    with tempfile.TemporaryDirectory() as td:
        fake = os.path.join(td, 'm.csv')
        with open(fake, 'w', encoding='utf-8', newline='') as f:
            w = csv.writer(f)
            w.writerow(['name', 'family', 'dopant'])
            w.writerows([['A_s0', 'as2s3_recover', 'AlI3'], ['A_s0', MAIN_FAMILIES[0], 'AlI3'], ['B_s0', MAIN_FAMILIES[0], 'MgO'],
                         ['C_s0', 'dualx_v23', 'MgO']])
        rep_ = {}
        got = load_stage1(fake, rep_)
        chk([(r['name'], r['family']) for r in got] == [('A_s0', MAIN_FAMILIES[0]), ('B_s0', MAIN_FAMILIES[0])]
            and rep_['dropped_duplicates'] == [('as2s3_recover', 'A_s0')], 'duplicate names: v23 row kept, other family dropped')
    try:
        balance({'Li': 18, 'Al': 2, 'O': 3, 'Cl': 4, 'P': 4, 'S': 17, 'Br': 1}, HOST_CELL, {'Al': 2, 'O': 3})
        chk(False, 'unbalanceable composition refused')
    except ValueError:
        chk(True, 'unbalanceable composition refused')
    e, n, nu = dissolution_energy({'Li': 18, 'Al': 2, 'O': 3, 'Cl': 4, 'P': 4, 'S': 17}, -0.1, -4.0, {'Al': 2, 'O': 3},
                                  -30.0, {'Li2S': -12.0, 'LiCl': -7.0, 'Li3PS4': -35.0})
    exp = (48 * (-4.1) + 3 * (-12.0) - 52 * (-4.0) + 30.0)
    chk(abs(e - exp) < 1e-9, f'dissolution energy arithmetic ({e:.3f} eV per unit)')
    # analyse() end to end — with configurations (bands) and with one value per precursor (the --label_csv path)
    with tempfile.TemporaryDirectory() as td:
        pcs = {k: list(v + rng.normal(0, 0.05, 4)) for k, v in sig.items()}
        r1 = analyse('with_configs', pcs, {k: float(np.median(v)) for k, v in pcs.items()}, 'low', td, 20, 9, rng, 'test',
                     use=small)
        r2 = analyse('one_value', None, sig, 'high', td, 20, 9, rng, 'test', use=small)
        rows1 = [l for l in open(os.path.join(td, 'with_configs_anion_effects.csv'), encoding='utf-8') if not l.startswith('#')]
        rows2 = [l for l in open(os.path.join(td, 'one_value_cation_effects.csv'), encoding='utf-8') if not l.startswith('#')]
        chk(r1['anion_effects']['O']['band_5_95'] is not None and r2['anion_effects']['O']['band_5_95'] is None
            and len(rows1) == 1 + len(r1['anion_effects']) and len(rows2) == 1 + len(r2['cation_effects_multi_family'])
            and rows2[1].rstrip('\r\n').endswith(',,'), 'analyse() writes JSON + CSVs with and without bands')
    # extra features: a hidden per-precursor descriptor is used when supplied; gaps and too many columns are refused
    hid = {k: float(rng.normal()) for k in keys}
    lab = {k: 2 * hid[k] + rng.normal(0, 0.05) for k in keys}
    ex = {'names': ['hidden'], 'values': {k: [hid[k]] for k in keys}}
    Xs9, n9 = design(keys, None, small)
    chk(Xs9.shape == (len(keys), 9) and n9 == small and np.allclose(Xs9[:, 2], [features(k)['z_over_r'] for k in keys]),
        'a feature subset gives exactly those columns, in order')
    q_without = predict_report(lab, 'low', 9, rng, use=small)['leave_one_cation_out']['Q2']
    q_with = predict_report(lab, 'low', 9, rng, ex, small)['leave_one_cation_out']['Q2']
    chk(q_without < 0.3 < 0.9 < q_with, f'extra feature carries a hidden signal (Q² {q_without:.2f} → {q_with:.2f})')
    for bad_ex, use, why in (({'names': ['hidden'], 'values': {k: [hid[k]] for k in keys[1:]}}, small, 'missing value'),
                             ({'names': ['hidden'], 'values': {k: [hid[k]] for k in keys}}, None, '13 > n/5 = 10'),
                             (None, ['z_cat', 'radius'], 'unknown name')):
        try:
            design(keys, bad_ex, use)
            chk(False, f'feature set refused ({why})')
        except ValueError:
            chk(True, f'feature set refused ({why})')
    # composition probe: a label equal to the atoms swapped is caught, a random one is not
    fake = []
    for i in range(200):
        nli, ns = int(rng.integers(18, 25)), int(rng.integers(16, 21))
        fake.append({'composition_Li': str(nli), 'composition_P': '4', 'composition_S': str(ns), 'composition_Cl': '4',
                     'composition_Al': '1', 'y_swap': str(nli + ns + 9 - 52), 'y_rand': str(rng.normal())})
    pr1, pr2 = composition_probe(fake, 'y_swap'), composition_probe(fake, 'y_rand')
    chk(pr1['spearman_vs_dN_atoms'] > 0.999 and abs(pr2['spearman_vs_dN_atoms']) < 0.2,
        f"composition probe ρ {pr1['spearman_vs_dN_atoms']:.2f} (swap label) · {pr2['spearman_vs_dN_atoms']:.2f} (random)")
    try:
        interface_delta('NCM811', '4.00')        # 4 of its rows are MPRestError records
        chk(False, 'error rows refused')
    except ValueError as e:
        chk('carry an error' in str(e), 'error rows refused (NCM811: MPRestError rows)')
    # interface Δ: real files, host row found once; an unknown cathode is refused
    d = interface_delta('LCO', '4.00')
    chk(len(d) >= 89 and all(math.isfinite(v) for v in d.values()), f'interface Δ vs host read for {len(d)} precursors (LCO 4.00 V)')
    try:
        interface_delta('XYZ', '4.00')
        chk(False, 'unknown cathode refused')
    except ValueError:
        chk(True, 'unknown cathode refused')
    print(f'selftest: {sum(ok)}/{len(ok)}')
    return 0 if all(ok) else 1


def main():
    if '--selftest' in sys.argv[1:]:
        return _selftest()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--demo', action='store_true', help='run on the flawed Stage-1 labels (tests the code)')
    ap.add_argument('--label_csv', help='precursor-level label file: columns precursor,value')
    ap.add_argument('--features_csv', help='extra per-precursor features: column precursor + numeric columns')
    ap.add_argument('--features', help=f'comma list of element features to use (default all): {",".join(FEATURES)}')
    ap.add_argument('--name', default='label')
    ap.add_argument('--better', choices=['low', 'high'], default='low')
    ap.add_argument('--out', required=True)
    ap.add_argument('--n_boot', type=int, default=200)
    ap.add_argument('--n_perm', type=int, default=199)
    ap.add_argument('--seed', type=int, default=20261014)
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.demo:
        if a.features:
            ap.error('--features is for --label_csv; the demo uses all 12 element features (n = 91)')
        runs = demo(a.out, a.n_boot, a.n_perm, a.seed, load_extra(a.features_csv) if a.features_csv else None)
    elif a.label_csv:
        with open(a.label_csv, encoding='utf-8') as fh:
            rows = [r for r in csv.DictReader(l for l in fh if not l.startswith('#'))]
        pv = {r['precursor']: float(r['value']) for r in rows if r.get('value') not in (None, '')}
        runs = [analyse(a.name, None, pv, a.better, a.out, a.n_boot, a.n_perm, np.random.default_rng(a.seed),
                        f'label from {a.label_csv}', None, load_extra(a.features_csv) if a.features_csv else None,
                        a.features.split(',') if a.features else None)]
    else:
        ap.error('--demo or --label_csv')
    print(f"{'label':36s} {'n':>3} {'noise':>6} {'famR2':>6} {'LOCO Q2':>8} {'LOFO Q2':>8} {'rand Q2':>8} {'perm p':>7} {'enrich':>6}")
    for r in runs:
        g, p_ = r['gate'], r['prediction']
        nr = '—' if g.get('noise_ratio') is None else f"{g['noise_ratio']:.2f}"
        print(f"{r['label']:36s} {g['n_precursors']:>3} {nr:>6} {g['anion_family_R2']:>6.2f} "
              f"{p_['leave_one_cation_out']['Q2']:>8.2f} {p_['leave_one_anion_family_out']['Q2']:>8.2f} {p_['random_5fold']['Q2']:>8.2f} "
              f"{p_['leave_one_cation_out']['perm_p']:>7.3f} {p_['leave_one_cation_out']['enrichment_top10']:>6.2f}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
