#!/usr/bin/env python3
"""cov5 reasonableness — checks 1, 2, 5, 6 (bounds · counts · identities · ordering · harvester↔webapp · mono leakage).
Writes cr_checks.json (machine) and prints a compact summary."""
import json, math, pickle
import numpy as np

import os as _os, tempfile as _tf
HERE = _os.path.dirname(_os.path.abspath(__file__))
REPO = _os.path.abspath(_os.path.join(HERE, '..', '..', '..'))
SP = _os.environ.get('COV5_WORK') or _os.path.join(_tf.gettempdir(), 'cov5_work')   # 중간 산출 (리포 밖)
_os.makedirs(SP, exist_ok=True)
rows = pickle.load(open(SP + '/cr_rows.pkl', 'rb'))
isn = lambda v: v is None or (isinstance(v, float) and math.isnan(v))
fin = lambda v: (v is not None) and isinstance(v, (int, float)) and math.isfinite(v)
OUT = {}

# ------------------------------------------------------------------ slot mapping (J20-k (B): mono → design phase slot)
FAMS = ['hz', 'wh', 'we', 'lp', 'lr', 'v2']
FAM_NAME = {'hz': 'Hertz-geom (수확기)', 'wh': 'Hertz-geom (웹앱)', 'we': '벽 제외 (수확기)', 'lp': 'legacy Physics v1',
            'lr': 'legacy Physics rough', 'v2': 'physics v2 (후보)'}


def slots(r, fam):
    """→ dict P,S,T (+ P_sd,S_sd) in design-phase slots; mono single value goes to the design block slot."""
    mono = r['block'] != 'bimodal'
    dslot = 'P' if r['block'] == 'mono_AM_P' else 'S'
    o = dict(P=np.nan, S=np.nan, T=np.nan, P_sd=np.nan, S_sd=np.nan, name=None)
    if fam in ('hz', 'we'):
        if mono:
            o[dslot] = r[f'{fam}_A']
        else:
            o['P'], o['S'] = r[f'{fam}_P'], r[f'{fam}_S']
        o['T'] = r[f'{fam}_T']
        return o
    # webapp families: mono under radius name
    vP, vS = r[f'{fam}_P'], r[f'{fam}_S']
    sP, sS = r.get(f'{fam}_P_sd', np.nan), r.get(f'{fam}_S_sd', np.nan)
    if mono:
        if fin(vP) and not fin(vS):
            o[dslot], o[dslot + '_sd'], o['name'] = vP, sP, 'AM_P'
        elif fin(vS) and not fin(vP):
            o[dslot], o[dslot + '_sd'], o['name'] = vS, sS, 'AM_S'
        elif fin(vS) and fin(vP):
            o['name'] = 'BOTH'
        else:
            o['name'] = 'NONE'
    else:
        o['P'], o['S'], o['P_sd'], o['S_sd'] = vP, vS, sP, sS
    if fam == 'wh':   # webapp has no total — particle-weighted from phases (same rule as harvester, all AM valid)
        if mono:
            o['T'] = o[dslot]
        else:
            o['T'] = (r['n_P'] * vP + r['n_S'] * vS) / (r['n_P'] + r['n_S'])
    else:
        o['T'] = r[f'{fam}_T']
    return o


# ------------------------------------------------------------------ CHECK 1 — bounds, NaN/inf, std, Bhatia–Davis, counts
c1 = {}
BD_ALL = []
for coh in ('LHS', 'lhsx'):
    R = [r for r in rows if r['cohort'] == coh]
    res = {}
    for fam in FAMS:
        nval = nnan_expected = 0
        bad_range, bad_nonfinite, bad_sd_neg, bad_sd_popo, bad_bd = [], [], [], [], []
        bd_margin_min = np.inf
        for r in R:
            s = slots(r, fam)
            for ph in ('P', 'S', 'T'):
                v = s[ph]
                if isn(v):
                    continue
                nval += 1
                if not math.isfinite(v):
                    bad_nonfinite.append((r['case'], ph, v)); continue
                if v < 0 or v > 100:
                    bad_range.append((r['case'], ph, v))
                if ph in ('P', 'S') and fam != 'hz' and fam != 'we':
                    sd = s[ph + '_sd']
                    if isn(sd):
                        if fam in ('wh', 'lp', 'lr', 'v2'):
                            bad_nonfinite.append((r['case'], ph + '_sd', 'missing'))
                        continue
                    if sd < 0:
                        bad_sd_neg.append((r['case'], ph, sd))
                    if sd > 50 + 1e-9:
                        bad_sd_popo.append((r['case'], ph, sd))
                    # Bhatia–Davis: σ² ≤ (100−μ)(μ−0) ; tolerance for 3-decimal rounding of μ, σ
                    lim = math.sqrt(max(v * (100 - v), 0.0))
                    bd_margin_min = min(bd_margin_min, lim - sd)
                    if fam == 'wh':
                        okbd = sd <= lim + 1e-9
                    else:   # 3-decimal rounding: exists (m, s) in the rounding boxes with s² ≤ m(100−m)
                        mlo, mhi = v - 5e-4, v + 5e-4
                        mbest = min(max(50.0, mlo), mhi)
                        okbd = (max(sd - 5e-4, 0.0)) ** 2 <= mbest * (100 - mbest) + 1e-12
                    if not okbd:
                        bad_bd.append((r['case'], ph, v, sd, lim))
                    BD_ALL.append((r['cohort'], fam, r['case'], ph, v, sd, lim - sd))
        res[fam] = dict(n_values=nval, out_of_range=bad_range, nonfinite_or_missing=bad_nonfinite, sd_negative=bad_sd_neg,
                        sd_gt_50=bad_sd_popo, bhatia_davis_violations=bad_bd,
                        bd_margin_min=(None if bd_margin_min == np.inf else bd_margin_min))
    c1[coh] = res
OUT['check1_bounds'] = c1
OUT['bd_worst'] = sorted(BD_ALL, key=lambda t: t[6])[:12]

# counts
cnt = {'LHS': {}, 'lhsx': {}}
for coh in ('LHS', 'lhsx'):
    R = [r for r in rows if r['cohort'] == coh]
    e = dict(hz_counts=[], we_counts=[], we_bad_sum=[], webapp_n=[], v2_nam=[], v2_nclip=[], v2_clip_mean=[],
             v2_allclip=[], hz_clip_mean=[], we_clip_mean=[], lp_T_weight=[], lr_T_weight=[], v2_T_weight=[],
             hz_T_weight=[], we_T_weight=[], wall_split=[], dpct_phys=[], dpct_rough=[], lp_internal_hz=[])
    stats = dict(hz_ncap=[], we_ncap=[], we_nbad=[], v2_clipfrac=[], dpct_phys_maxabs=0.0, dpct_rough_maxabs=0.0,
                 lpT_w_maxabs=0.0, lrT_w_maxabs=0.0, v2T_w_maxabs=0.0, hzT_w_maxabs=0.0, weT_w_maxabs=0.0,
                 ws_hz_maxabs=0.0, ws_we_maxabs=0.0, lp_int_hz_maxabs=0.0, lp_int_hz_maxrel=0.0)
    for r in R:
        cid = r['case']
        pc = {'AM_P': r['n_P'], 'AM_S': r['n_S'], 'AM': r['n_A']}
        for fam in ('hz', 'we'):
            nb = 0
            for lab in ('AM_P', 'AM_S', 'AM'):
                npart, nvalid = r[f'{fam}_cnt_{lab}']
                if npart != pc[lab] or nvalid > npart or nvalid < 0:
                    e[f'{fam}_counts'].append((cid, lab, npart, nvalid, pc[lab]))
                nb += npart - nvalid
            if nb != r[f'{fam}_nbad']:
                e['we_bad_sum' if fam == 'we' else 'hz_counts'].append((cid, fam, nb, r[f'{fam}_nbad']))
        # webapp particle counts vs harvester
        if r['block'] == 'bimodal':
            if not (r['w_nP'] == r['n_P'] and r['w_nS'] == r['n_S']):
                e['webapp_n'].append((cid, r['w_nP'], r['w_nS'], r['n_P'], r['n_S']))
        else:
            got = [v for v in (r['w_nP'], r['w_nS']) if fin(v)]
            if got != [r['n_A']]:
                e['webapp_n'].append((cid, r['w_nP'], r['w_nS'], r['n_A']))
        # v2 counts
        if r['v2_nam'] != r['n_AMtot']:
            e['v2_nam'].append((cid, r['v2_nam'], r['n_AMtot']))
        nden = r['v2_nam'] - r['v2_nfree0'] - r['v2_nrinv']
        if not (0 <= r['v2_nclip'] <= nden):
            e['v2_nclip'].append((cid, r['v2_nclip'], nden))
        stats['v2_clipfrac'].append((cid, r['v2_nclip'] / nden if nden > 0 else np.nan, r['v2_status'] == 'ok'))
        if r['v2_status'] == 'ok':
            lb = 100.0 * r['v2_nclip'] / r['v2_nam']
            if r['v2_T'] < lb - 1e-3:
                e['v2_clip_mean'].append((cid, r['v2_T'], lb))
            if r['v2_nclip'] == r['v2_nam']:
                s = slots(r, 'v2')
                ok = abs(r['v2_T'] - 100) < 1e-9 and all((isn(s[p]) or abs(s[p] - 100) < 1e-9) for p in 'PS') \
                    and all((isn(s[p + '_sd']) or s[p + '_sd'] == 0) for p in 'PS')
                if not ok:
                    e['v2_allclip'].append((cid, r['v2_T'], s['P'], s['S'], s['P_sd'], s['S_sd']))
        # Hertz / wall-excl clip count vs mean
        for fam in ('hz', 'we'):
            nv = sum(r[f'{fam}_cnt_{lab}'][1] for lab in ('AM_P', 'AM_S', 'AM'))
            ncap = r[f'{fam}_ncap']
            stats[f'{fam}_ncap'].append((cid, ncap, nv))
            if r[f'{fam}_T'] < 100.0 * ncap / nv - 1e-9:
                e[f'{fam}_clip_mean'].append((cid, r[f'{fam}_T'], 100.0 * ncap / nv))
            # total = valid-count weighted mean of phases
            num = den = 0.0
            for lab, key in (('AM_P', 'P'), ('AM_S', 'S'), ('AM', 'A')):
                nvl = r[f'{fam}_cnt_{lab}'][1]
                if nvl > 0:
                    num += nvl * r[f'{fam}_{key}']; den += nvl
            d = abs(num / den - r[f'{fam}_T'])
            stats[f'{fam}T_w_maxabs'] = max(stats[f'{fam}T_w_maxabs'], d)
            if d > 1e-9:
                e[f'{fam}_T_weight'].append((cid, num / den, r[f'{fam}_T']))
        stats['we_nbad'].append((cid, r['we_nbad']))
        # webapp totals = particle-weighted phase means (all AM counted by webapp families; v2 ok beds have no invalid AM)
        nP = r['w_nP'] if fin(r['w_nP']) else 0
        nS = r['w_nS'] if fin(r['w_nS']) else 0
        for fam in ('lp', 'lr', 'v2'):
            vP, vS, vT = r[f'{fam}_P'], r[f'{fam}_S'], r[f'{fam}_T']
            if isn(vT):
                continue
            num = (nP * vP if nP else 0) + (nS * vS if nS else 0)
            wv = num / (nP + nS)
            d = abs(wv - vT)
            stats[f'{fam}T_w_maxabs'] = max(stats[f'{fam}T_w_maxabs'], d)
            if d > 1e-3:
                e[f'{fam}_T_weight'].append((cid, wv, vT))
        # delta columns
        for ph in ('P', 'S'):
            h, p, rg = r[f'wh_{ph}'], r[f'lp_{ph}'], r[f'lr_{ph}']
            if fin(h) and fin(p):
                exp = (p - h) / h * 100
                d = abs(exp - r[f'lp_{ph}_dpct'])
                tol = 0.006 + 100 * 5e-4 / h
                stats['dpct_phys_maxabs'] = max(stats['dpct_phys_maxabs'], d)
                if d > tol:
                    e['dpct_phys'].append((cid, ph, exp, r[f'lp_{ph}_dpct']))
            if fin(p) and fin(rg):
                exp = (rg - p) / p * 100
                d = abs(exp - r[f'lr_{ph}_dpct'])
                tol = 0.006 + 100 * 1e-3 / p
                stats['dpct_rough_maxabs'] = max(stats['dpct_rough_maxabs'], d)
                if d > tol:
                    e['dpct_rough'].append((cid, ph, exp, r[f'lr_{ph}_dpct']))
        # legacy script's own Hertz total (backed out of delta) vs harvester Hertz total
        hz_int = r['lp_T'] / (1 + r['lp_T_dpct'] / 100)
        d = abs(hz_int - r['hz_T'])
        stats['lp_int_hz_maxabs'] = max(stats['lp_int_hz_maxabs'], d)
        stats['lp_int_hz_maxrel'] = max(stats['lp_int_hz_maxrel'], d / r['hz_T'])
        tol = r['hz_T'] * (0.005 / (100 + r['lp_T_dpct'])) + 5e-4 + 1e-6
        if d > tol:
            e['lp_internal_hz'].append((cid, hz_int, r['hz_T']))
        # wall split aggregation
        ws = r['wall_split']
        for grp, (hk, wk, labs) in {'AM_P': ('hz_P', 'we_P', ['AM_P']), 'AM_S': ('hz_S', 'we_S', ['AM_S']),
                                    'AM': ('hz_A', 'we_A', ['AM']), 'total': ('hz_T', 'we_T', ['AM_P', 'AM_S', 'AM'])}.items():
            if grp not in ws:
                if (grp != 'total' and pc.get(grp, 0) > 0):
                    e['wall_split'].append((cid, grp, 'missing'))
                continue
            npart = sum(pc[l] for l in labs)
            for wall in ('any', 'floor', 'plate'):
                cl = ws[grp][wall]
                n = sum(cl[c]['n'] for c in cl)
                if n != npart:
                    e['wall_split'].append((cid, grp, wall, 'n', n, npart))
                nv = sum(cl[c]['n_valid'] for c in cl)
                m = sum(cl[c]['n_valid'] * cl[c]['mean_pct'] for c in cl if cl[c]['n_valid']) / nv
                d0 = abs(m - r[hk])
                nvw = sum(cl[c]['n_valid_wallexcl'] for c in cl)
                mw = sum(cl[c]['n_valid_wallexcl'] * cl[c]['mean_wallexcl_pct'] for c in cl if cl[c]['n_valid_wallexcl']) / nvw
                d1 = abs(mw - r[wk])
                stats['ws_hz_maxabs'] = max(stats['ws_hz_maxabs'], d0)
                stats['ws_we_maxabs'] = max(stats['ws_we_maxabs'], d1)
                if d0 > 1e-9 or d1 > 1e-9:
                    e['wall_split'].append((cid, grp, wall, 'mean', d0, d1))
                if cl['fully_out']['n_valid_wallexcl'] != 0:
                    e['wall_split'].append((cid, grp, wall, 'fully_out_valid', cl['fully_out']['n_valid_wallexcl']))
    cnt[coh] = dict(errors={k: v for k, v in e.items()}, stats=stats)
OUT['check1_counts'] = cnt

# ------------------------------------------------------------------ CHECK 2 — ordering
c2 = {}
PAIRS = [('lp', 'wh', '≥', 'legacy Physics ≥ Hertz'), ('lp', 'lr', '≥', 'legacy Physics ≥ rough (구성상)'),
         ('lp', 'v2', '≤', 'v2 ≥ legacy Physics'), ('hz', 'we', '≤', '벽 제외 ≥ Hertz (구성상 · 입자 단위)'),
         ('wh', 'v2', '≤', 'v2 ≥ Hertz'), ('we', 'lp', '≤', 'legacy Physics ≥ 벽 제외 (정보용)'),
         ('wh', 'lr', '≤', 'rough ≥ Hertz (정보용)')]
for coh in ('LHS', 'lhsx'):
    R = [r for r in rows if r['cohort'] == coh]
    res = {}
    for a, b, op, label in PAIRS:
        for ph in ('P', 'S', 'T'):
            n = 0; viol = []; dmin = np.inf; dmed = []
            for r in R:
                va, vb = slots(r, a)[ph], slots(r, b)[ph]
                if isn(va) or isn(vb):
                    continue
                n += 1
                d = (va - vb) if op == '≥' else (vb - va)     # d ≥ 0 means ordering holds
                dmed.append(d)
                dmin = min(dmin, d)
                # rounding tolerance: webapp physics families rounded to 3 dp
                tol = 5e-4 + 1e-9 if (a in ('lp', 'lr', 'v2') or b in ('lp', 'lr', 'v2')) else 1e-9
                if d < -tol:
                    viol.append((r['case'], round(va, 4), round(vb, 4), round(d, 4)))
            res[f'{a}|{b}|{ph}'] = dict(label=label, n=n, n_viol=len(viol), viol=viol[:30],
                                         d_min=(None if dmin == np.inf else dmin),
                                         d_median=(float(np.median(dmed)) if dmed else None),
                                         n_equal=int(sum(abs(x) <= 5e-4 for x in dmed)))
    c2[coh] = res
OUT['check2_order'] = c2

# ------------------------------------------------------------------ CHECK 5 — harvester vs webapp (same Hertz quantity)
c5 = {}
for coh in ('LHS', 'lhsx'):
    R = [r for r in rows if r['cohort'] == coh]
    res = {}
    for ph in ('P', 'S', 'T'):
        ds = []
        for r in R:
            a, b = slots(r, 'hz')[ph], slots(r, 'wh')[ph]
            if isn(a) and isn(b):
                continue
            if isn(a) != isn(b):
                ds.append(np.inf); continue
            ds.append(abs(a - b))
        res[ph] = dict(n=len(ds), max_abs=max(ds) if ds else None)
    c5[coh] = res
OUT['check5_hz_vs_webapp'] = c5

# ------------------------------------------------------------------ CHECK 6 — mono leakage + naming
c6 = {}
for coh in ('LHS', 'lhsx'):
    R = [r for r in rows if r['cohort'] == coh]
    res = dict(n_mono=0, harvester_leak=[], webapp_leak=[], name_vs_block={}, value_mismatch=[], bimodal_only_leak=[],
               rough_sf=[])
    for r in R:
        if r['block'] == 'bimodal':
            if not isn(r['hz_A']) or not isn(r['we_A']) or r['n_A'] != 0:
                res['bimodal_only_leak'].append(r['case'])
            for fam in ('wh', 'lp', 'lr'):
                if isn(r[f'{fam}_P']) or isn(r[f'{fam}_S']):
                    res['bimodal_only_leak'].append((r['case'], fam, 'phase missing'))
            continue
        res['n_mono'] += 1
        # harvester: AM_P/AM_S None with N_A status, AM_only present and == total
        if not (isn(r['hz_P']) and isn(r['hz_S']) and r['hz_P_st'] == 'N_A_PHASE_ABSENT' and r['hz_S_st'] == 'N_A_PHASE_ABSENT'
                and isn(r['we_P']) and isn(r['we_S']) and fin(r['hz_A']) and fin(r['we_A'])
                and abs(r['hz_A'] - r['hz_T']) < 1e-12 and abs(r['we_A'] - r['we_T']) < 1e-12):
            res['harvester_leak'].append(r['case'])
        names = set()
        for fam in ('wh', 'lp', 'lr', 'v2'):
            s = slots(r, fam)
            if fam == 'v2' and r['v2_status'] != 'ok':
                if not (isn(r['v2_P']) and isn(r['v2_S'])):
                    res['webapp_leak'].append((r['case'], fam, 'blank bed has value'))
                continue
            if s['name'] in ('BOTH', 'NONE'):
                res['webapp_leak'].append((r['case'], fam, s['name']))
            else:
                names.add(s['name'])
            # std columns of the absent phase must be blank too
            other = 'S' if s['name'] == 'AM_P' else 'P'
            if fin(r.get(f'{fam}_{other}_sd', np.nan)):
                res['webapp_leak'].append((r['case'], fam, 'absent-phase std present'))
        nm = names.pop() if len(names) == 1 else ('MIXED:' + ','.join(sorted(names)))
        rad = r['d_am_p'] / 2 if r['block'] == 'mono_AM_P' else r['d_am_s'] / 2
        key = f"{r['block']}→{nm}"
        res['name_vs_block'].setdefault(key, []).append((r['case'], rad))
        # value: harvester AM_only vs webapp single
        d = abs(r['hz_A'] - slots(r, 'wh')['P' if r['block'] == 'mono_AM_P' else 'S'])
        if d > 1e-9:
            res['value_mismatch'].append((r['case'], d))
        # rough shape factor actually applied (from delta_pct_rough ~ −(1−(S−A)/(SF·S−A)); unclipped → ≤ −(1−1/SF))
        dsl = 'P' if nm == 'AM_P' else 'S'
        res['rough_sf'].append((r['case'], r['block'], nm, rad, r[f'lp_{dsl}'], r[f'lr_{dsl}_dpct']))
    c6[coh] = res
OUT['check6_mono'] = c6

json.dump(OUT, open(SP + '/cr_checks.json', 'w'), ensure_ascii=False, indent=1, default=str)

# ------------------------------------------------------------------ compact print
if __name__ == '__main__':
    for coh in ('LHS', 'lhsx'):
        print('==', coh)
        for fam, v in c1[coh].items():
            print(f"  C1 {fam}: n={v['n_values']} range={len(v['out_of_range'])} nonfin={len(v['nonfinite_or_missing'])} "
                  f"sd<0={len(v['sd_negative'])} sd>50={len(v['sd_gt_50'])} BD={len(v['bhatia_davis_violations'])} "
                  f"BDmargin_min={v['bd_margin_min']}")
        er = cnt[coh]['errors']
        print('  counts errors:', {k: len(v) for k, v in er.items() if v})
        st = cnt[coh]['stats']
        print('  maxabs:', {k: (round(v, 12) if isinstance(v, float) else None) for k, v in st.items() if isinstance(v, float)})
        for k, v in c2[coh].items():
            print(f"  C2 {k}: n={v['n']} viol={v['n_viol']} dmin={v['d_min'] if v['d_min'] is None else round(v['d_min'],4)} eq={v['n_equal']}")
        print('  C5', c5[coh])
        m = c6[coh]
        print('  C6 mono', m['n_mono'], 'hleak', len(m['harvester_leak']), 'wleak', len(m['webapp_leak']), 'bimodal_leak', len(m['bimodal_only_leak']),
              'names', {k: len(v) for k, v in m['name_vs_block'].items()}, 'val_mismatch', len(m['value_mismatch']))
