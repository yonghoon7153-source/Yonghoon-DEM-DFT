#!/usr/bin/env python3
"""codoping_ml.py — co-doping 가설 생성기 v2 (ML-보조, numpy 전용).

*** NOT VALIDATED — co-doping 실측/계산 라벨은 존재하지 않는다 ***
(db/properties/doping_cascade_verified.json 은 단일 도펀트 결과만 보유.)
따라서 이 산출물은 '검증된 예측기'가 아니라 **가설 생성기 v2**다.
v1(cascade_v23_synergy_pairs.csv, 휴리스틱)과 같은 지위 — 실험/계산 후보 제안용.

설계 (4단계, 전부 결정론 · 난수 없음):
  1단계  단일도펀트 ridge 회귀(닫힌형 해, λ는 LOOCV 최소화로 선택):
         표준화 특징 16종 + group one-hot(4, 기준=main-group)으로 cascade score 재현.
         → LOOCV R²와 계수 = '캐스케이드 score가 실제로 뭘 보고 있나'의 해부.
  2단계  pair 특징 1081쌍 = C(47,2). 상보성 명시:
         joint_window_V = max(ox_A,ox_B) − min(red_A,red_B)  (한쪽이 양극측, 다른쪽이
         음극측 커버 = anode–cathode 상보), transport_min = min(bvs_x005) (약한 고리),
         blocking_max, mass_avg, cost_max, air_max(soft-acid 하나면 보호),
         gap_min(전자누설 약한 고리), disorder_max, dose_slope_min, group_cross, de_avg.
  3단계  교호작용(2차): 표준화 pair 특징의 곱항 8종(물리적 조합만).
         단일항 가중치는 1단계 계수를 그대로 이식(단일도펀트 스케일러 유지),
         교호작용항 가중치는 v1 휴리스틱 synergy를 약한 타깃으로 **가중 ridge** 증류
         (v1 수록 40쌍 가중 1.0, 미수록 1041쌍은 synergy≈0 근사·가중 0.1 —
         0-근사의 신뢰가 낮으므로. 비가중 시 0 홍수로 계수가 과축소되는 것 확인).
         ml_score = base_z(이식) + Σ v_j·inter_j(증류).
  4단계  불확실성: 1단계 LOOCV 잔차 std(leverage 보정)를 base_z 단위로 정합해 두 도펀트에
         전파 + 3단계 ridge 계수 공분산의 쌍별 사영(x'Cov(v)x) → quadrature 합 ±.
         수치상 **stage3 사영이 지배**(stage1 성분 ~0.02 수준 — 무시 가능).
         이 ±는 **모델 내부 적합 노이즈만** 반영 — 물리적 타당성 불확실성 아님(라벨 부재).

입력:  db/properties/cascade_v23_ranked.csv, oxidation_stability_cascade.csv,
       cascade_v23_litransport.csv, cascade_v23_themes.json, cascade_v23_synergy_pairs.csv
출력:  db/properties/codoping_ml_v2.csv  (1081쌍 랭킹, 헤더에 NOT-validated 명시)
       db/properties/codoping_ml_v2_meta.json  (계수·λ·LOOCV R²·v1 대비·가정·한계)
"""
import csv
import json
import re
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
PROP = ROOT / "db" / "properties"

# ---------------------------------------------------------------- 데이터 적재

def load_dopants():
    """themes JSON(이미 평탄화된 도펀트별 특징)을 기준으로 적재하고 원본 CSV와 교차검증."""
    themes = json.loads((PROP / "cascade_v23_themes.json").read_text())
    dops = {d["dopant"]: d for d in themes["dopants"]}

    # ranked.csv 교차검증 (score/de/E/pugh)
    with open(PROP / "cascade_v23_ranked.csv") as f:
        rows = [r for r in csv.DictReader(x for x in f if not x.startswith("#"))]
    assert len(rows) == len(dops) == 47, "도펀트 수 불일치"
    for r in rows:
        d = dops[r["dopant"]]
        assert abs(d["score"] - float(r["score"])) < 1e-6, r["dopant"]
        assert abs(d["de"] - float(r["de"])) < 1e-6, r["dopant"]
        assert abs(d["E_GPa"] - float(r["E_GPa"])) < 1e-6, r["dopant"]

    # ESW CSV 교차검증 (ox/red/window)
    with open(PROP / "oxidation_stability_cascade.csv") as f:
        for r in csv.DictReader(x for x in f if not x.startswith("#")):
            if r["dopant"] in dops:
                d = dops[r["dopant"]]
                assert abs(d["ox_V"] - float(r["ox_V"])) < 1e-6, r["dopant"]
                assert abs(d["red_V"] - float(r["red_V"])) < 1e-6, r["dopant"]

    # litransport CSV 교차검증 (bvs x005 / blocking)
    with open(PROP / "cascade_v23_litransport.csv") as f:
        for r in csv.DictReader(x for x in f if not x.startswith("#")):
            name, x = r["_dir"].rsplit("_x", 1)
            if name in dops and x == "005":
                d = dops[name]
                assert abs(d["bvs_x005"] - float(r["bvs_li_proxy_score"])) < 1e-9, name
    return dops


def load_v1_pairs():
    with open(PROP / "cascade_v23_synergy_pairs.csv") as f:
        rdr = csv.reader(f)
        rows = [r for r in rdr if r and not r[0].startswith("#") and not r[0].startswith('"#')]
    hdr = rows[0]
    out = {}
    for r in rows[1:]:
        d = dict(zip(hdr, r))
        out[frozenset((d["pairA"], d["pairB"]))] = float(d["synergy"])
    return out

# ---------------------------------------------------------------- ridge + LOOCV

LAMBDA_GRID = np.logspace(-4, 3, 71)  # 결정론: 고정 그리드

def ridge_loocv(Z, yc, sw=None, rule="min"):
    """표준화 Z·중심화 yc에 대해 닫힌형 (가중) ridge + LOOCV.
    rule="min": LOOCV MSE 최소 λ. rule="1se": 최소 MSE + 1SE 이내 최대 λ —
    정확 공선 특징(window=ox-red, slope=x010-x002)에서 계수 귀속을 안정화.
    sw: 표본 가중 (None=균등). 반환: w, λ*, e_loo, h(leverage), R²_loo."""
    if sw is None:
        sw = np.ones(len(yc))
    ZW = Z * sw[:, None]
    fits = []
    for lam in LAMBDA_GRID:
        A = np.linalg.solve(Z.T @ ZW + lam * np.eye(Z.shape[1]), ZW.T)
        H = Z @ A            # 가중 hat 행렬
        e = (yc - H @ yc) / (1.0 - np.diag(H))
        mse = float(np.sum(sw * e**2) / np.sum(sw))
        fits.append((mse, lam, A @ yc, e, np.diag(H).copy()))
    mses = np.array([f[0] for f in fits])
    imin = int(mses.argmin())
    if rule == "1se":
        e2 = sw * fits[imin][3]**2
        se = float(e2.std() / np.sqrt(len(yc)) / np.mean(sw))
        pick = max(i for i in range(len(fits)) if mses[i] <= mses[imin] + se)
    else:
        pick = imin
    mse, lam, w, e_loo, h = fits[pick]
    r2 = 1.0 - float(np.sum(sw * e_loo**2)) / float(np.sum(sw * yc**2))
    return w, lam, e_loo, h, r2


def ridge_coef_cov(Z, lam, sigma2, sw=None):
    """ridge 계수 공분산 (sandwich): σ²·(Z'WZ+λI)⁻¹ Z'WZ (Z'WZ+λI)⁻¹.
    ridge 축소 때문에 하한 추정치임 — meta에 명시."""
    if sw is None:
        sw = np.ones(Z.shape[0])
    M = Z.T @ (Z * sw[:, None])
    Minv = np.linalg.inv(M + lam * np.eye(Z.shape[1]))
    return sigma2 * (Minv @ M @ Minv)


def zscore(X):
    mu = X.mean(axis=0)
    sd = X.std(axis=0)
    sd[sd == 0] = 1.0
    return (X - mu) / sd, mu, sd


def spearman(a, b):
    """Spearman ρ 직접 구현 (동순위 평균 랭크)."""
    def rank(v):
        order = np.argsort(v, kind="stable")
        r = np.empty(len(v))
        r[order] = np.arange(1, len(v) + 1, dtype=float)
        # 동순위 평균
        for val in np.unique(v):
            m = v == val
            if m.sum() > 1:
                r[m] = r[m].mean()
        return r
    ra, rb = rank(np.asarray(a)), rank(np.asarray(b))
    ra -= ra.mean(); rb -= rb.mean()
    return float((ra @ rb) / np.sqrt((ra @ ra) * (rb @ rb)))

# ---------------------------------------------------------------- 특징 정의

SINGLE_FEATS = ["de", "ox_V", "red_V", "window_V", "E_GPa", "pugh",
                "bvs_x002", "bvs_x005", "bvs_x010", "bvs_slope",
                "blocking", "disorder_std", "mass_per_cation",
                "cost_tier", "gap_lit_eV", "air_hsab"]
GROUPS_OH = ["TM", "lanthanide", "alk.earth", "alkali"]  # 기준(drop) = main-group

ELEM_RE = re.compile(r"([A-Z][a-z]?)(\d*)")

def has_fluorine(formula):
    return any(el == "F" for el, _ in ELEM_RE.findall(formula))


def main():
    dops = load_dopants()
    names = sorted(dops)  # 결정론적 순서
    n = len(names)

    # ---------- 1단계: 단일도펀트 ridge (cascade score 해부) ----------
    X = np.array([[dops[d][k] for k in SINGLE_FEATS] for d in names])
    G = np.array([[1.0 if dops[d]["group"] == g else 0.0 for g in GROUPS_OH] for d in names])
    y = np.array([dops[d]["score"] for d in names])

    Xz, mu_s, sd_s = zscore(X)          # 단일도펀트 스케일러 — pair 이식에 재사용
    Gz, mu_g, sd_g = zscore(G)
    Z1 = np.hstack([Xz, Gz])
    yc = y - y.mean()

    w1, lam1, e1, h1, r2_1 = ridge_loocv(Z1, yc, rule="1se")
    sigma1 = float(np.sqrt(np.mean(e1**2)))          # score 단위
    u1_score = sigma1 * np.sqrt(1.0 + h1)            # 도펀트별 leverage 보정 예측 불확실성 (score 단위)
    feat_names1 = SINGLE_FEATS + [f"group={g}" for g in GROUPS_OH]

    # ---------- 2단계: pair 특징 (1081쌍) ----------
    pairs = [(names[i], names[j]) for i in range(n) for j in range(i + 1, n)]

    def agg(a, b):
        A, B = dops[a], dops[b]
        ox_join = max(A["ox_V"], B["ox_V"])
        red_join = min(A["red_V"], B["red_V"])
        return {
            "de": 0.5 * (A["de"] + B["de"]),                       # de_avg
            "ox_V": ox_join,                                        # 산화한계 = max(ox)
            "red_V": red_join,                                      # 환원한계 = min(red)
            "window_V": ox_join - red_join,                         # 합동창 (상보)
            "E_GPa": 0.5 * (A["E_GPa"] + B["E_GPa"]),
            "pugh": 0.5 * (A["pugh"] + B["pugh"]),
            "bvs_x002": min(A["bvs_x002"], B["bvs_x002"]),          # 약한 고리
            "bvs_x005": min(A["bvs_x005"], B["bvs_x005"]),          # transport_min
            "bvs_x010": min(A["bvs_x010"], B["bvs_x010"]),
            "bvs_slope": min(A["bvs_slope"], B["bvs_slope"]),       # dose_slope_min
            "blocking": max(A["blocking"], B["blocking"]),          # blocking_max
            "disorder_std": max(A["disorder_std"], B["disorder_std"]),
            "mass_per_cation": 0.5 * (A["mass_per_cation"] + B["mass_per_cation"]),
            "cost_tier": max(A["cost_tier"], B["cost_tier"]),
            "gap_lit_eV": min(A["gap_lit_eV"], B["gap_lit_eV"]),    # 전자누설 약한 고리
            "air_hsab": max(A["air_hsab"], B["air_hsab"]),          # 하나면 보호
            # ml-3: 합동창이 단일 도펀트 창보다 실제로 얼마나 넓어졌나. 0 이면 '상보' 가정이
            #   발동하지 않고 더 나은 한쪽 창을 그대로 물려받은 것 (전체 쌍의 ~70%).
            "window_gain": (ox_join - red_join) - max(A["ox_V"] - A["red_V"],
                                                      B["ox_V"] - B["red_V"]),
        }

    P = np.array([[agg(a, b)[k] for k in SINGLE_FEATS] for a, b in pairs])
    # group 지분 (pair 중 해당 그룹 비율 0/0.5/1) — one-hot 계수 이식용
    PG = np.array([[(float(dops[a]["group"] == g) + float(dops[b]["group"] == g)) / 2.0
                    for g in GROUPS_OH] for a, b in pairs])
    group_cross = np.array([1.0 if dops[a]["group"] != dops[b]["group"] else 0.0
                            for a, b in pairs])

    # ---------- 3단계: 이식 + 교호작용 증류 ----------
    # 단일항: 1단계 계수를 **단일도펀트 스케일러**로 표준화한 pair 특징에 이식
    Pz_s = (P - mu_s) / sd_s
    PGz_s = (PG - mu_g) / sd_g
    base_raw = Pz_s @ w1[:len(SINGLE_FEATS)] + PGz_s @ w1[len(SINGLE_FEATS):]
    base_z = (base_raw - base_raw.mean()) / base_raw.std()
    # stage1 예측 불확실성을 ml_score의 base 성분 스케일(base_z 단위)로 정합 —
    # y.std()로 나누면 1.26x 과소 (2026-07-27 리뷰 수정)
    u_single = u1_score / float(base_raw.std())

    # 교호작용용: pair 분포 기준 z-score
    Pz_p, _, _ = zscore(P)
    col = {k: Pz_p[:, i] for i, k in enumerate(SINGLE_FEATS)}
    gx = (group_cross - group_cross.mean()) / group_cross.std()

    INTERACTIONS = [
        # (이름, 곱항, 물리적 근거)
        ("air_max*gap_min", col["air_hsab"] * col["gap_lit_eV"],
         "soft-acid 공기보호 <-> 전자절연 트레이드오프"),
        ("joint_window*transport_min", col["window_V"] * col["bvs_x005"],
         "넓은 합동창이 수송 약한 고리와 동반되는가"),
        ("disorder_max*dose_slope_min", col["disorder_std"] * col["bvs_slope"],
         "무질서 유도 <-> 농도 강건성"),
        ("transport_min*blocking_max", col["bvs_x005"] * col["blocking"],
         "수송 약한 고리 x 채널 차단 최악치"),
        ("joint_window*gap_min", col["window_V"] * col["gap_lit_eV"],
         "전기화학 창을 전자누설이 잠식하는가"),
        ("group_cross*joint_window", gx * col["window_V"],
         "이종 그룹 조합의 창 상보성"),
        ("de_avg*joint_window", col["de"] * col["window_V"],
         "열역학 도핑 안정성이 동반된 합동창"),
        ("air_max*transport_min", col["air_hsab"] * col["bvs_x005"],
         "공기보호와 수송의 겸비"),
    ]
    Xi = np.column_stack([v for _, v, _ in INTERACTIONS])
    Xi_z, _, _ = zscore(Xi)

    # v1 증류 타깃: 미수록 쌍 synergy≈0 근사 + 가중 0.1 (0-근사 신뢰 낮음 —
    # 비가중이면 0 홍수(1041/1081)로 LOOCV가 λ 과대 선택 → 계수 전멸 확인)
    v1 = load_v1_pairs()
    listed = np.array([frozenset(p) in v1 for p in pairs])
    t = np.array([v1.get(frozenset(p), 0.0) for p in pairs])
    t_z = (t - t.mean()) / t.std()
    sw = np.where(listed, 1.0, 0.1)

    # 특징도 sw-가중 중심화 — 타깃만 가중중심화하면 잔존 절편(~0.12 t_z)이 계수에 흡수됨 (2026-07-27 리뷰 수정)
    Xi_z = Xi_z - (sw[:, None] * Xi_z).sum(axis=0) / sw.sum()
    w3, lam3, e3, _, r2_3 = ridge_loocv(Xi_z, t_z - (sw * t_z).sum() / sw.sum(), sw)
    sigma3 = float(np.sqrt(np.sum(sw * e3**2) / np.sum(sw)))
    inter_contrib = Xi_z * w3           # (1081, 8) 쌍별 교호작용 기여
    inter_sum = inter_contrib.sum(axis=1)
    ml_score = base_z + inter_sum

    # ---------- 4단계: 불확실성 (모델 내부 노이즈만 — 물리 검증 아님) ----------
    idx = {d: i for i, d in enumerate(names)}
    cov3 = ridge_coef_cov(Xi_z, lam3, sigma3**2, sw)
    var_inter = np.einsum("ij,jk,ik->i", Xi_z, cov3, Xi_z)   # 쌍별 x'Cov(v)x
    unc = np.array([np.sqrt(u_single[idx[a]]**2 + u_single[idx[b]]**2 + var_inter[i])
                    for i, (a, b) in enumerate(pairs)])

    # ---------- v1 대비 진단 ----------
    v1_keys = list(v1)
    pair_ix = {frozenset(p): i for i, p in enumerate(pairs)}
    ml_on_v1 = [ml_score[pair_ix[k]] for k in v1_keys]
    rho40 = spearman(ml_on_v1, [v1[k] for k in v1_keys])
    order = np.argsort(-ml_score)
    top10 = [frozenset(pairs[i]) for i in order[:10]]
    v1_top10 = sorted(v1, key=lambda k: -v1[k])[:10]
    overlap10 = len(set(top10) & set(v1_top10))
    corr_base_t = float(np.corrcoef(base_z, t_z)[0, 1])

    # 교호작용 기여로 인한 순위 이동 (base 단독 대비) — '끌어올린 쌍' 진단
    rank_full = np.empty(len(pairs), dtype=int)
    rank_full[order] = np.arange(1, len(pairs) + 1)
    order_base = np.argsort(-base_z)
    rank_base = np.empty(len(pairs), dtype=int)
    rank_base[order_base] = np.arange(1, len(pairs) + 1)
    lift = rank_base - rank_full        # +N = 교호작용이 N계단 끌어올림
    lifted = sorted((i for i in order[:50] if lift[i] > 0),
                    key=lambda i: -lift[i])[:5]

    # ---------- 태그 ----------
    q25_transport = float(np.quantile([dops[d]["bvs_x005"] for d in names], 0.25))

    def tags_for(i):
        a, b = pairs[i]
        A, B = dops[a], dops[b]
        f = agg(a, b)
        tg = []
        ox_carrier = a if A["ox_V"] >= B["ox_V"] else b
        red_carrier = a if A["red_V"] <= B["red_V"] else b
        if (ox_carrier != red_carrier
                and f["ox_V"] - min(A["ox_V"], B["ox_V"]) >= 0.05
                and max(A["red_V"], B["red_V"]) - f["red_V"] >= 0.05):
            tg.append("anode<->cathode")
        if has_fluorine(a) != has_fluorine(b):
            tg.append("oxyfluoride")
        if group_cross[i]:
            tg.append("cross-group")
        if f["air_hsab"] >= 0.8:
            tg.append("air-protect")
        if f["gap_lit_eV"] >= 7.0:
            tg.append("insulating")
        if f["bvs_x005"] < q25_transport:
            tg.append("weak-transport")   # 경고 태그
        if "collapse" in (A["esw_note"] or "") or "collapse" in (B["esw_note"] or ""):
            tg.append("collapse-member")  # 경고: ESW collapse 도펀트 포함 (창<0.05 V)
        return "|".join(tg)

    inter_names = [nm for nm, _, _ in INTERACTIONS]
    # 가장 '끌어올린'(서명 기여 최대) 항 — 전부 음이면 접두사 '-'로 최대 감점 항 표기
    top_inter = []
    for i in range(len(pairs)):
        c = inter_contrib[i]
        if c.max() > 0:
            top_inter.append(inter_names[int(np.argmax(c))])
        else:
            top_inter.append("-" + inter_names[int(np.argmin(c))])

    # ---------- 출력 CSV ----------
    out_csv = PROP / "codoping_ml_v2.csv"
    with open(out_csv, "w", newline="") as fo:
        fo.write("# co-doping HYPOTHESIS GENERATOR v2 (ML-assisted). NOT validated — "
                 "co-doping 실측/계산 라벨 없음. 후보 제안용이며 예측기가 아님.\n")
        fo.write("# method: ridge(47 single dopants, LOOCV lambda) coefficients transplanted "
                 "to pair features + 8 physics interaction terms distilled from v1 heuristic "
                 "(weighted ridge: listed 1.0 / unlisted~0 weight 0.1). ml_score = base_z + "
                 "sum(v_j*inter_j); uncertainty = internal LOOCV-residual propagation only.\n")
        fo.write("# columns: gap_min = min(gap_lit_eV) 문헌 큐레이션 값(우리 계산 갭 아님); "
                 "air_max = HSAB 정성등급 큐레이션; transport_min = min(bvs_x005) BVS proxy(절대 σ 아님); "
                 "joint_window_V = max(ox)-min(red) 상보 가정; "
                 "window_gain = joint_window_V - max(단일 도펀트 창) — 0 이면 상보가 발동하지 않고 "
                 "더 나은 한쪽 창을 그대로 물려받은 것(전체 1081쌍의 ~70%가 정확히 0).\n")
        w = csv.writer(fo)
        w.writerow(["rank", "pairA", "pairB", "ml_score", "uncertainty",
                    "joint_window_V", "window_gain", "transport_min", "gap_min", "air_max",
                    "top_interaction", "tags"])
        for rk, i in enumerate(order, 1):
            a, b = pairs[i]
            f = agg(a, b)
            w.writerow([rk, a, b, f"{ml_score[i]:.4f}", f"{unc[i]:.3f}",
                        f"{f['window_V']:.3f}", f"{f['window_gain']:.3f}", f"{f['bvs_x005']:.4f}",
                        f"{f['gap_lit_eV']:.1f}", f"{f['air_hsab']:.2f}",
                        top_inter[i], tags_for(i)])

    # ---------- 진단 (ml-2 / ml-4) ----------
    _li = listed
    def _rank_corr(x, y):
        rx, ry = x.argsort().argsort().astype(float), y.argsort().argsort().astype(float)
        return float(np.corrcoef(rx, ry)[0, 1])

    if _li.sum() >= 3:
        _obs = t[_li]                              # 실측 v1 synergy (원 스케일)
        _stage3 = (Xi_z @ w3)[_li]                 # 증류 모델의 예측(교호작용 항만)
        _full = ml_score[_li]                      # base_z + inter_sum (배포 점수)
        # ⚠ 스케일이 다른 두 양(원 synergy vs z-단위 점수)의 R² 는 의미가 없다 —
        #   스케일 불변인 상관/순위상관만 보고한다.
        _r_listed = float(np.corrcoef(_stage3, _obs)[0, 1])
        _sp_listed = _rank_corr(_stage3, _obs)
        _r_full = float(np.corrcoef(_full, _obs)[0, 1])
        _sp_full = _rank_corr(_full, _obs)
    else:
        _r_listed = _sp_listed = _r_full = _sp_full = float("nan")
    from collections import Counter as _C
    _cnt10 = dict(_C([d for i in order[:10] for d in pairs[i]]).most_common())
    _cnt50 = dict(_C([d for i in order[:50] for d in pairs[i]]).most_common())

    # ---------- 출력 meta JSON ----------
    meta = {
        "property": "codoping_ml_v2_meta",
        "date": "2026-07-27",
        "status": "HYPOTHESIS GENERATOR — NOT VALIDATED (co-doping 라벨 부재; "
                  "doping_cascade_verified.json 은 단일 도펀트만)",
        "inputs": ["cascade_v23_ranked.csv", "oxidation_stability_cascade.csv",
                   "cascade_v23_litransport.csv", "cascade_v23_themes.json",
                   "cascade_v23_synergy_pairs.csv (v1, 증류 타깃)"],
        "stage1_single_dopant_ridge": {
            "target": "cascade v23 score (합성 지표 — 물성 실측 아님)",
            "n": n, "lambda": float(lam1), "lambda_rule": "1se",
            "loocv_r2": round(r2_1, 4),
            "loocv_residual_std_score_units": round(sigma1, 4),
            "loocv_note": "표준화(mu/sd)·y평균·λ선택은 전표본 고정(폴드 밖 재사용) — 폴드별 재계산으로 "
                          "누수 정량화: σ_loo +3.4%(0.00178→0.00184), R² Δ<1e-4, λ 폴드별 재선택(nested)도 "
                          "R²=0.9998 (타깃이 특징의 정확 선형합성이라 결과 왜곡 없음)",
            "coefficients_std_units": {k: round(float(v), 4)
                                       for k, v in zip(feat_names1, w1)},
            "note": "계수 = 표준화 특징 1σ당 score 변화. λ는 1-SE 규칙 — score가 5성분 "
                    "정확 선형합성이라 min-λ에선 정확공선 트리오(window=ox-red, "
                    "slope=x010-x002)에 스퓨리어스 가중이 새는 것 확인. "
                    "one-hot 기준그룹=main-group.",
        },
        "stage3_interaction_distillation": {
            "target": "v1 synergy (top40 수록값 가중 1.0, 미수록 1041쌍=0 근사·가중 0.1)",
            "n_pairs": len(pairs), "lambda": float(lam3),
            "weighted_loocv_r2": round(r2_3, 4),
            "weighted_loocv_residual_std_tz_units": round(sigma3, 4),
            "loocv_note": "stage1과 동일 — 표준화·λ는 전표본 고정 (누수 영향 무시 수준, stage1 loocv_note 참조)",
            "intercept_note": "특징·타깃 모두 sw-가중 중심화로 절편 정합 (2026-07-27 수정 — 비중심화 대비 "
                              "계수 max|Δ|≈0.013, top10 집합 동일, top50 순위이동 ≤1계단)",
            "interaction_coefficients": {nm: round(float(c), 4)
                                         for nm, c in zip(inter_names, w3)},
            "interaction_rationale": {nm: why for nm, _, why in INTERACTIONS},
            # ml-2: weighted_loocv_r2 는 1041개 downweighted 0-근사가 지배하는 값이라
            #   '실제 synergy 설명분산'이 아니다. 40개 실측 라벨에만 걸어보면 아래와 같다.
            "diagnostics_on_listed_labels": {
                "n_listed": int(_li.sum()),
                "stage3_pearson_r": round(float(_r_listed), 4),
                "stage3_spearman_r": round(float(_sp_listed), 4),
                "full_score_pearson_r": round(float(_r_full), 4),
                "full_score_spearman_r": round(float(_sp_full), 4),
                "note": "weighted_loocv_r2(위)를 '실제 synergy 설명분산'으로 읽으면 안 된다 — "
                        "가중치의 ~72%(1041×0.1)가 v1 미수록 쌍의 0-근사에 실려 있어서, 그 값은 "
                        "주로 '0 을 0 으로 맞추는' 성능이다. 실측 라벨에 대한 신호는 여기 "
                        "상관/순위상관으로만 판단할 것 (원 synergy 와 z-단위 점수는 스케일이 달라 "
                        "R² 자체가 정의상 무의미하므로 싣지 않는다). 상태: HYPOTHESIS GENERATOR.",
            },
            # ml-4: top10/top50 이 특정 도펀트에 몰리는지 (base_z 상속분 포함)
            "dopant_concentration": {
                "top10_counts": _cnt10, "top50_counts": _cnt50,
                "distinct_in_top10": len(_cnt10),
                "note": "편중의 출처는 교호작용이 아니라 base_z(단일도펀트 cascade score)다 — "
                        "base_z 단독 랭킹도 top10 중 7개를 그대로 재현하고 "
                        "corr(base_z, ml_score)≈0.86. 다양성이 필요하면 '도펀트당 최상위 쌍' "
                        "목록을 따로 뽑을 것.",
            },
        },
        "vs_v1": {
            "spearman_on_v1_top40_pairs": round(rho40, 3),
            "top10_overlap_count": overlap10,
            "corr_base_z_vs_v1_target": round(corr_base_t, 3),
            "v1_top10": [sorted(k) for k in v1_top10],
            "v2_top10": [sorted(k) for k in top10],
            "interaction_lifted_pairs": [
                {"pair": sorted(pairs[i]), "rank_v2": int(rank_full[i]),
                 "rank_base_only": int(rank_base[i]), "lift": int(lift[i]),
                 "top_interaction": top_inter[i]} for i in lifted],
        },
        "assumptions": [
            "co-doping 상호작용은 단일도펀트 특징의 집계(min/max/avg)+2차 곱항으로 근사 가능",
            "합동 ESW = max(ox) - min(red): 두 상이 각각 양극측/음극측을 커버한다는 상보 가정 "
            "(실제 계면상 형성/혼상 반응 미반영)",
            "1단계 계수의 pair 이식: 단일도펀트 스케일러 유지 시 물리 방향성 보존 가정",
            "v1 미수록 쌍 synergy=0 근사 (v1은 top40만 저장; 실제는 0~0.059 사이) — "
            "0-근사 신뢰가 낮아 증류 가중 0.1 부여 (가중 1.0이면 0 홍수로 계수 전멸)",
            "불확실성 ±는 모델 내부 적합 노이즈만 (stage1 LOOCV leverage 전파를 base_z 단위로 정합 + "
            "stage3 ridge 계수 공분산 사영, ridge 축소로 하한 추정) — 수치상 stage3 사영이 지배"
            "(stage1 성분 ~0.02 수준으로 무시 가능)이며 물리적 타당성 불확실성 아님",
            "cost_tier/gap_lit_eV/air_hsab 는 큐레이션 값(문헌 전형/정성 등급) — 우리 계산 아님",
        ],
        "limitations": [
            "타깃(cascade score, v1 synergy) 자체가 휴리스틱 합성 지표 — 이 모델은 그 휴리스틱의 "
            "해부+확장이지 물성 예측이 아님",
            "co-doping 시 도펀트간 화학 상호작용(공석 보상, 상분리, 계면상)은 특징에 없음",
            "검증 경로: top 후보 소수를 UMA cascade(공동 치환 슈퍼셀)로 직접 계산해 라벨 확보 후 재학습",
            "ml_score 절대값은 무의미(z 단위 합성) — 순위와 ±만 사용",
        ],
    }
    out_meta = PROP / "codoping_ml_v2_meta.json"
    out_meta.write_text(json.dumps(meta, ensure_ascii=False, indent=1) + "\n")

    # ---------- 콘솔 요약 ----------
    print(f"[1단계] ridge λ={lam1:.4g}  LOOCV R²={r2_1:.3f}  σ_loo={sigma1:.4f} (score 단위)")
    top_coef = sorted(zip(feat_names1, w1), key=lambda kv: -abs(kv[1]))[:8]
    for k, v in top_coef:
        print(f"    {k:20s} {v:+.4f}")
    print(f"[3단계] 가중 증류 λ={lam3:.4g}  wLOOCV R²={r2_3:.3f}  (v1 근사 타깃)")
    for nm, c in zip(inter_names, w3):
        print(f"    {nm:28s} {c:+.4f}")
    print(f"[v1 대비] Spearman(top40)={rho40:.3f}  top10 겹침={overlap10}/10  "
          f"corr(base,v1)={corr_base_t:.3f}")
    print("[v2 top10]")
    for rk, i in enumerate(order[:10], 1):
        a, b = pairs[i]
        print(f"  {rk:2d}. {a:7s}+{b:7s} score={ml_score[i]:+.3f}±{unc[i]:.3f} "
              f"win={agg(a,b)['window_V']:.3f}V int={inter_sum[i]:+.3f} "
              f"top_int={top_inter[i]} [{tags_for(i)}]")
    print("[교호작용이 끌어올린 쌍 (v2 top50 내, base 단독 대비)]")
    for i in lifted:
        a, b = pairs[i]
        print(f"    {a}+{b}: base {rank_base[i]}위 -> v2 {rank_full[i]}위 "
              f"(+{lift[i]}) via {top_inter[i]}")
    print(f"저장: {out_csv}\n저장: {out_meta}")


if __name__ == "__main__":
    main()
