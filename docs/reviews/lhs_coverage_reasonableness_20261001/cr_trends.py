#!/usr/bin/env python3
"""cov5 reasonableness — check 3 (trends · robust outliers) + check 4 (saturation / discrimination)."""
import json, math, pickle, sys
import numpy as np
from scipy.stats import spearmanr, rankdata

import os as _os, tempfile as _tf
HERE = _os.path.dirname(_os.path.abspath(__file__))
REPO = _os.path.abspath(_os.path.join(HERE, '..', '..', '..'))
SP = _os.environ.get('COV5_WORK') or _os.path.join(_tf.gettempdir(), 'cov5_work')   # 중간 산출 (리포 밖)
_os.makedirs(SP, exist_ok=True)
sys.path.insert(0, HERE)
rows = pickle.load(open(SP + '/cr_rows.pkl', 'rb'))
from cr_checks import slots, FAMS, FAM_NAME, isn, fin   # noqa: E402  (re-running cr_checks is harmless)

OUT = {}


def rz(x):
    x = np.asarray(x, float)
    med = np.median(x)
    mad = np.median(np.abs(x - med)) * 1.4826
    return (x - med) / (mad if mad > 0 else np.nan), med, mad


def partial_spearman(y, x1, x2):
    """rank-based partial correlation of y with x1 controlling x2."""
    ry, r1, r2 = rankdata(y), rankdata(x1), rankdata(x2)
    A = np.c_[np.ones_like(r2), r2]
    ey = ry - A @ np.linalg.lstsq(A, ry, rcond=None)[0]
    e1 = r1 - A @ np.linalg.lstsq(A, r1, rcond=None)[0]
    return float(np.corrcoef(ey, e1)[0, 1])


def design_x(r, ph):
    rSE = r['d_se'] / 2
    if ph == 'P':
        rAM = r['d_am_p'] / 2
    elif ph == 'S':
        rAM = r['d_am_s'] / 2
    else:
        if r['block'] == 'bimodal':
            rAM = (r['n_P'] * r['d_am_p'] / 2 + r['n_S'] * r['d_am_s'] / 2) / (r['n_P'] + r['n_S'])
        else:
            rAM = (r['d_am_p'] if r['block'] == 'mono_AM_P' else r['d_am_s']) / 2
    return r['se_of_solid'], 100 - r['am_pct'], rSE / rAM, rAM, rSE


def logit(v):
    p = np.clip(np.asarray(v, float) / 100.0, 5e-4, 1 - 5e-4)
    return np.log(p / (1 - p))


trend = {}
flags = []
for coh in ('LHS', 'lhsx'):
    R = [r for r in rows if r['cohort'] == coh]
    for fam in FAMS:
        for ph in ('P', 'S', 'T'):
            ids, y, se, sew, rat, rAM, rSE, nph, hz = [], [], [], [], [], [], [], [], []
            for r in R:
                v = slots(r, fam)[ph]
                if isn(v):
                    continue
                a, b, c, d, e = design_x(r, ph)
                ids.append(r['case']); y.append(v); se.append(a); sew.append(b); rat.append(c); rAM.append(d); rSE.append(e)
                n = (r['n_P'] if ph == 'P' else r['n_S'] if ph == 'S' else r['n_AMtot'])
                if r['block'] != 'bimodal' and ph != 'T':
                    n = r['n_A']
                nph.append(n)
                hz.append(slots(r, 'wh')[ph])
            y = np.array(y); se = np.array(se); sew = np.array(sew); rat = np.array(rat); nph = np.array(nph); hz = np.array(hz)
            if len(y) < 5:
                continue
            key = f'{coh}|{fam}|{ph}'
            q = np.percentile(y, [0, 25, 50, 75, 100])
            t = dict(n=len(y), q=[float(x) for x in q],
                     n100=int((y >= 99.9995).sum()), n99=int((y >= 99).sum()), n95=int((y >= 95).sum()),
                     rho_se=float(spearmanr(y, se)[0]), rho_sewt=float(spearmanr(y, sew)[0]),
                     rho_ratio=float(spearmanr(y, rat)[0]),
                     prho_se=partial_spearman(y, se, rat), prho_ratio=partial_spearman(y, rat, se),
                     rho_rAM=float(spearmanr(y, rAM)[0]), n_unique=int(len(np.unique(np.round(y, 3)))))
            # model: Hertz-like families → log y ~ log se + log ratio ; physics families → logit y ~ logit hz (same slot)
            if fam in ('hz', 'wh', 'we'):
                X = np.c_[np.ones_like(se), np.log(se), np.log(rat)]
                yy = np.log(y)
                beta = np.linalg.lstsq(X, yy, rcond=None)[0]
                res = yy - X @ beta
                t['model'] = 'ln y = a + b ln(se_of_solid) + c ln(r_SE/r_AM)'
            else:
                ok = np.isfinite(hz)
                X = np.c_[np.ones(ok.sum()), logit(hz[ok])]
                yy = logit(y[ok])
                fitm = y[ok] < 99.5
                beta = np.linalg.lstsq(X[fitm], yy[fitm], rcond=None)[0] if fitm.sum() >= 5 else np.array([np.nan, np.nan])
                res = np.full(len(y), np.nan); res[ok] = yy - X @ beta
                t['model'] = 'logit y = a + b logit(Hertz 같은 칸) [적합은 y<99.5 만]'
                t['n_fit'] = int(fitm.sum())
            if fam in ('hz', 'wh', 'we'):
                ss = np.sum((res - res.mean()) ** 2); tt = np.sum((yy - yy.mean()) ** 2)
                t['R2'] = float(1 - ss / tt) if tt > 0 else None
            else:
                if fitm.sum() >= 5 and np.all(np.isfinite(beta)):
                    rf = res[ok][fitm]; yf = yy[fitm]
                    t['R2'] = float(1 - np.sum((rf - rf.mean()) ** 2) / np.sum((yf - yf.mean()) ** 2))
                else:
                    t['R2'] = None
            t['beta'] = [float(b) for b in beta]
            zr, med, mad = rz(y)
            zres, _, madres = rz(res[np.isfinite(res)])
            zres_full = np.full(len(y), np.nan); zres_full[np.isfinite(res)] = zres
            t['mad_raw'] = float(mad); t['mad_res'] = float(madres)
            t['n_flag_raw'] = int(np.nansum(np.abs(zr) > 4)); t['n_flag_res'] = int(np.nansum(np.abs(zres_full) > 4))
            trend[key] = t
            for i in range(len(y)):
                fr = abs(zr[i]) > 4 if np.isfinite(zr[i]) else False
                fz = abs(zres_full[i]) > 4 if np.isfinite(zres_full[i]) else False
                if fr or fz:
                    flags.append(dict(cohort=coh, fam=fam, ph=ph, case=ids[i], value=float(y[i]), z_raw=float(zr[i]),
                                      z_res=(float(zres_full[i]) if np.isfinite(zres_full[i]) else None),
                                      se_of_solid=float(se[i]), se_wt=float(sew[i]), ratio=float(rat[i]), n_phase=int(nph[i]),
                                      se_pct_rank=float((se < se[i]).mean()), ratio_pct_rank=float((rat < rat[i]).mean())))
OUT['trend'] = trend
OUT['flags'] = flags

# ---------------------------------------------------------------- check 4 — saturation (AM-level clip counts where available)
sat = {}
for coh in ('LHS', 'lhsx'):
    R = [r for r in rows if r['cohort'] == coh]
    f_hz = np.array([r['hz_ncap'] / sum(r[f'hz_cnt_{l}'][1] for l in ('AM_P', 'AM_S', 'AM')) for r in R])
    f_we = np.array([r['we_ncap'] / sum(r[f'we_cnt_{l}'][1] for l in ('AM_P', 'AM_S', 'AM')) for r in R])
    v2c = np.array([r['v2_nclip'] / (r['v2_nam'] - r['v2_nfree0'] - r['v2_nrinv']) for r in R])
    v2ok = np.array([r['v2_status'] == 'ok' for r in R])
    sat[coh] = dict(
        hz_clipfrac_q=[float(x) for x in np.percentile(f_hz, [0, 50, 100])], hz_beds_any_clip=int((f_hz > 0).sum()),
        hz_total_clipped=int(sum(r['hz_ncap'] for r in R)), n_am_total=int(sum(r['n_AMtot'] for r in R)),
        we_clipfrac_q=[float(x) for x in np.percentile(f_we, [0, 50, 100])], we_beds_any_clip=int((f_we > 0).sum()),
        we_total_clipped=int(sum(r['we_ncap'] for r in R)),
        v2_clipfrac_q_all=[float(x) for x in np.percentile(v2c, [0, 25, 50, 75, 100])],
        v2_clipfrac_q_ok=[float(x) for x in np.percentile(v2c[v2ok], [0, 25, 50, 75, 100])],
        v2_beds_allclip=int((v2c >= 1).sum()), v2_beds_ge99=int((v2c >= 0.99).sum()), v2_beds_ge50=int((v2c >= 0.5).sum()),
        v2_am_clipped=int(sum(r['v2_nclip'] for r in R)))
    # which Hertz level corresponds to legacy physics ≥ 99 (per bed, total)
    hzT = np.array([r['hz_T'] for r in R]); lpT = np.array([r['lp_T'] for r in R]); v2T = np.array([r['v2_T'] for r in R])
    sat[coh]['hzT_min_where_lp_ge99'] = float(hzT[lpT >= 99].min()) if (lpT >= 99).any() else None
    sat[coh]['hzT_max_where_lp_lt90'] = float(hzT[lpT < 90].max()) if (lpT < 90).any() else None
    sat[coh]['v2_clipfrac_vs_hzT_spearman'] = float(spearmanr(v2c, hzT)[0])
    # ratio legacy Physics / Hertz (unsaturated beds) per slot
    for ph in ('P', 'S', 'T'):
        rr = []
        for r in R:
            a, b = slots(r, 'lp')[ph], slots(r, 'wh')[ph]
            if fin(a) and fin(b) and a < 95:
                rr.append(a / b)
        if rr:
            sat[coh][f'ratio_lp_over_hz_{ph}_unsat'] = [len(rr)] + [float(x) for x in np.percentile(rr, [0, 25, 50, 75, 100])]
OUT['saturation'] = sat
json.dump(OUT, open(SP + '/cr_trends.json', 'w'), ensure_ascii=False, indent=1, default=str)

if __name__ == '__main__':
    for k, t in trend.items():
        print(k, 'n', t['n'], 'q', [round(x, 2) for x in t['q']], 'n100', t['n100'], 'n99', t['n99'],
              'ρse', round(t['rho_se'], 3), 'ρrat', round(t['rho_ratio'], 3), 'pρse', round(t['prho_se'], 3), 'pρrat', round(t['prho_ratio'], 3),
              'R2', None if t['R2'] is None else round(t['R2'], 3), 'flag', t['n_flag_raw'], t['n_flag_res'], 'uniq', t['n_unique'])
    print('flags', len(flags))
    for coh in sat:
        print(coh, {k: v for k, v in sat[coh].items()})
