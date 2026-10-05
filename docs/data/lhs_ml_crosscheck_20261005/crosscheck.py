#!/usr/bin/env python3
"""수영 님 LHS ML 1차 결과 (주간보고 10-05) 를 배포 v1.1 CSV 만으로 대조한다 — 읽기 전용 · 설계 5 노브만 입력.

python3 docs/data/lhs_ml_crosscheck_20261005/crosscheck.py  →  같은 폴더 crosscheck_results.json

① 기공도 (`porosity_union_exact_pct`): GPR-ARD (RBF · 초매개변수 = 학습 fold 안 주변우도 최대) 10-fold OOF · 묶음별 · 묶음 단독 ·
   이차 Ridge (λ = 안쪽 CV) 대조 · 묶음 간 분산 몫
② AM–SE CN (`am_se_cn_mean` = 개수 가중): 설계만으로 만든 개수 가중 (r_AM/r_SE)² · SE 질량분율과 log-log 적합
③ 순위 상관 방향 (CN · τ) · ④ τ 빈칸 = 비관통 확인 · SE 수준별 비관통 수 · ⑤ 적격성 표지 수

mono 침대의 없는 상 입경은 있는 상 입경으로 채운다 (그 상 몫이 0 이라 값이 결과에 안 들어간다).
"""
import csv
import json
import os

import numpy as np
from scipy.linalg import cho_factor, cho_solve
from scipy.optimize import minimize
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
REL = os.path.join(HERE, '..', 'lhs_release_20261001_v11')


def load(f):
    with open(os.path.join(REL, f), encoding='utf-8') as fh:
        return list(csv.DictReader(fh))


ROWS = [(r, 0) for r in load('lhs_release_20261001_v11.csv')] + [(r, 1) for r in load('lhsx_release_20261001_v11.csv')]


def col(k):
    out = []
    for r, _ in ROWS:
        v = r.get(k, '')
        out.append(float(v) if v not in ('', None) else np.nan)
    return np.array(out)


AM, PS, DP, DS, DSE = col('am_pct'), col('ps_frac'), col('d_am_p_um'), col('d_am_s_um'), col('d_se_um')
COH = np.array([c for _, c in ROWS])
STATUS = np.array([r['physical_target_status'] for r, _ in ROWS])
DPE = np.where(np.isfinite(DP), DP, DS)
DSE_ = np.where(np.isfinite(DS), DS, DP)
X0 = np.c_[AM, PS, DPE, DSE_, DSE]


def r2(y, p):
    return float(1 - ((y - p) ** 2).sum() / ((y - y.mean()) ** 2).sum())


def mae(y, p):
    return float(np.abs(y - p).mean())


# ---------- GPR-ARD ----------
def _k(a, b, ls, sf):
    return sf ** 2 * np.exp(-0.5 * (((a[:, None, :] - b[None, :, :]) / ls) ** 2).sum(-1))


def _nll(th, z, y):
    ls, sf, sn = np.exp(th[:5]), np.exp(th[5]), np.exp(th[6])
    kx = _k(z, z, ls, sf) + (sn ** 2 + 1e-8) * np.eye(len(y))
    try:
        c = cho_factor(kx)
    except np.linalg.LinAlgError:
        return 1e10
    return 0.5 * y @ cho_solve(c, y) + np.log(np.diag(c[0])).sum()


def gpr(xtr, ytr, xte):
    mu, sd = xtr.mean(0), xtr.std(0)
    z, zt = (xtr - mu) / sd, (xte - mu) / sd
    ym, ys = ytr.mean(), ytr.std()
    yy = (ytr - ym) / ys
    best = None
    for s in ([0, 0, 0, 0, 0, 0, -2], [1, 1, 1, 1, 1, 0, -3], [-.5, 0, .5, .5, 0, .5, -1]):
        res = minimize(_nll, np.array(s, float), args=(z, yy), method='L-BFGS-B', bounds=[(-3, 4)] * 5 + [(-3, 3), (-7, 1)])
        if best is None or res.fun < best.fun:
            best = res
    ls, sf, sn = np.exp(best.x[:5]), np.exp(best.x[5]), np.exp(best.x[6])
    c = cho_factor(_k(z, z, ls, sf) + (sn ** 2 + 1e-8) * np.eye(len(yy)))
    return _k(zt, z, ls, sf) @ cho_solve(c, yy) * ys + ym, ls, float(sn * ys)


def oof(fit, idx, y, k=10, seed=1):
    rng = np.random.default_rng(seed)
    perm = rng.permutation(idx)
    p = np.full(len(y), np.nan)
    for f in np.array_split(perm, k):
        tr = np.setdiff1d(perm, f)
        p[f] = fit(X0[tr], y[tr], X0[f])[0]
    return p


# ---------- 이차 Ridge ----------
def ridge2(xtr, ytr, xte, lams=(1e-3, 1e-2, 0.1, 1, 3, 10), seed=0):
    def feats(x, mu, sd):
        z = (x - mu) / sd
        return np.hstack([z] + [z[:, [i]] * z[:, [j]] for i in range(5) for j in range(i, 5)])

    rng = np.random.default_rng(seed)
    best = None
    for lam in lams:
        err = 0.0
        for g in np.array_split(rng.permutation(len(ytr)), 5):
            t = np.setdiff1d(np.arange(len(ytr)), g)
            mu, sd = xtr[t].mean(0), xtr[t].std(0)
            f = feats(xtr[t], mu, sd)
            m = ytr[t].mean()
            w = np.linalg.solve(f.T @ f + lam * np.eye(f.shape[1]), f.T @ (ytr[t] - m))
            err += ((feats(xtr[g], mu, sd) @ w + m - ytr[g]) ** 2).sum()
        if best is None or err < best[0]:
            best = (err, lam)
    mu, sd = xtr.mean(0), xtr.std(0)
    f = feats(xtr, mu, sd)
    m = ytr.mean()
    w = np.linalg.solve(f.T @ f + best[1] * np.eye(f.shape[1]), f.T @ (ytr - m))
    return feats(xte, mu, sd) @ w + m, None, None


def main():
    out = {'what': '배포 v1.1 CSV (130 + 64) 만 · 입력 = 설계 5 노브 (am_pct · ps_frac · d_am_p_um · d_am_s_um · d_se_um)',
           'n': {'130': int((COH == 0).sum()), '64': int((COH == 1).sum())}}
    # ① 기공도
    y = col('porosity_union_exact_pct')
    allidx = np.arange(len(y))
    p = oof(gpr, allidx, y)
    _, ls, sn = gpr(X0, y, X0[:1])
    po = {'gpr_ard_10fold_oof': {'all': {'R2': r2(y, p), 'MAE_pp': mae(y, p)}},
          'gpr_full_fit': {'length_scales_std_units': dict(zip(['am_pct', 'ps_frac', 'd_am_p', 'd_am_s', 'd_se'], map(float, ls))),
                           'noise_sd_pp': sn}}
    for c, name in ((0, '130'), (1, '64')):
        m = COH == c
        po['gpr_ard_10fold_oof'][name] = {'R2': r2(y[m], p[m]), 'MAE_pp': mae(y[m], p[m]),
                                          'y_min': float(y[m].min()), 'y_max': float(y[m].max()), 'y_sd': float(y[m].std())}
        ps_ = oof(gpr, np.where(m)[0], y, seed=2)
        po.setdefault('gpr_ard_cohort_only_model', {})[name] = {'R2': r2(y[m], ps_[m]), 'MAE_pp': mae(y[m], ps_[m])}
    for s in ('OK', 'HOLD'):
        m = STATUS == s
        po['gpr_ard_10fold_oof'][f'status_{s}'] = {'n': int(m.sum()), 'MAE_pp': mae(y[m], p[m])}
    pr = oof(ridge2, allidx, y)
    po['quadratic_ridge_10fold_oof'] = {'R2': r2(y, pr), 'MAE_pp': mae(y, pr)}
    within = sum(((y[COH == c] - y[COH == c].mean()) ** 2).sum() for c in (0, 1))
    po['between_cohort_variance_share'] = float(1 - within / ((y - y.mean()) ** 2).sum())
    se = 100 - AM
    po['se_wt_range'] = {'130': [float(se[COH == 0].min()), float(se[COH == 0].max())],
                         '64': [float(se[COH == 1].min()), float(se[COH == 1].max())]}
    out['porosity'] = po
    # ② AM–SE CN
    cn = col('am_se_cn_mean')
    rp, rs, rse = DPE / 2, DSE_ / 2, DSE / 2
    with np.errstate(divide='ignore', invalid='ignore'):
        nr = np.where(PS >= 1, np.inf, np.where(PS <= 0, 0.0, (PS / (1 - PS)) * (rs / rp) ** 3))  # N_P / N_S (같은 밀도)
        fp = np.where(np.isinf(nr), 1.0, nr / (1 + nr))
    geo = fp * (rp / rse) ** 2 + (1 - fp) * (rs / rse) ** 2
    sef = (100 - AM) / 100
    a1 = np.c_[np.ones(len(cn)), np.log(geo)]
    w1 = np.linalg.lstsq(a1, np.log(cn), rcond=None)[0]
    a2 = np.c_[np.ones(len(cn)), np.log(geo), np.log(sef)]
    w2 = np.linalg.lstsq(a2, np.log(cn), rcond=None)[0]
    out['am_se_cn_mean_geometry'] = {
        'feature': '개수 가중 (r_AM/r_SE)² — N_P/N_S = (ps/(1−ps))·(r_S/r_P)³ (설계만)',
        'log_R2_size_ratio_sq_only': r2(np.log(cn), a1 @ w1), 'exponent_only': float(w1[1]),
        'log_R2_with_se_mass_fraction': r2(np.log(cn), a2 @ w2), 'exponents': [float(w2[1]), float(w2[2])]}
    # ③ 순위 상관
    tau = col('tortuosity_SE_wall')
    feats = {'se_wt': se, 'd_se_um': DSE, 'd_am_s_um': DS, 'd_am_p_um': DP, 'ps_frac': PS}
    sp = {}
    for tname, t in (('am_se_cn_mean', cn), ('tortuosity_SE_wall', tau)):
        sp[tname] = {}
        for k, v in feats.items():
            m = np.isfinite(t) & np.isfinite(v)
            sp[tname][k] = {'n': int(m.sum()), 'spearman': float(spearmanr(v[m], t[m]).correlation)}
    out['spearman'] = sp
    # ④ τ 빈칸
    perc = col('percolation_pct')
    blank = ~np.isfinite(tau)
    by = {}
    for lv in sorted(set(np.round(se[COH == 0], 6))):
        m = (COH == 0) & (np.round(se, 6) == lv)
        by[f'{lv:g}'] = {'n': int(m.sum()), 'non_percolating': int((blank & m).sum())}
    out['tortuosity'] = {'blank': int(blank.sum()), 'blank_all_non_percolating': bool(np.all(perc[blank] == 0)),
                         'percolating_rows': int((~blank).sum()), 'mean_percolating': float(np.nanmean(tau)),
                         'min': float(np.nanmin(tau)), 'max': float(np.nanmax(tau)), 'by_se_wt_130': by}
    # ⑤ 적격성
    out['eligibility'] = {name: {s: int(((COH == c) & (STATUS == s)).sum()) for s in ('OK', 'HOLD')}
                          for c, name in ((0, '130'), (1, '64'))}
    path = os.path.join(HERE, 'crosscheck_results.json')
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
