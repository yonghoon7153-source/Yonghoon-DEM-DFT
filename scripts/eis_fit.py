#!/usr/bin/env python3
"""CNLS equivalent-circuit fit of the 이종기술 EIS archive.

Reads the tidy CSVs in `이종기술/eis/extracted/`, fits a circuit per cell type,
and writes `이종기술/eis/fits/eis_fit_results.csv` + a per-file fit figure.

MODELS (chosen from the measured shape, see README):
  - symmetric cell  (arc closes to a resistance at LF, phase->0)  -> `R0-p(R1,CPE1)`
        R0 = series/bulk, R1 = transport-arc resistance (R_ion if electron-blocking).
  - full cell       (semicircle + Warburg diffusion tail, phase ~ -6..-11 deg at LF)
        -> `R0-p(R1,CPE1)-Wo1`   R0 = series, R1 = interfacial (R_int), Wo1_0 = R_w (diffusion).

Impedances are fit in Ω, then resistive params are area-normalized to Ω·cm²
(symmetric 10pi = 0.7854 cm², full 13pi = 1.3273 cm²; lab-note geometry).

⚠ The physical label of R1 (R_ion vs R_ct) depends on the symmetric-cell blocking
condition, which is NOT encoded in the files — confirm before calling a σ.
Requires `impedance` (pip install impedance) + numpy/scipy/matplotlib.
"""
import csv
import math
import os
import warnings

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EIS = os.path.join(ROOT, '이종기술', 'eis')
EXTRACTED = os.path.join(EIS, 'extracted')
FITS = os.path.join(EIS, 'fits')
AREA = {'symmetric': round(math.pi * 0.5 ** 2, 4), 'full': round(math.pi * 0.65 ** 2, 4)}
# Cathode-electrolyte COMPOSITE thickness (µm) — the transport path.  At areal-cap 3 the
# composite is ~40–50 µm (user, 2026-07); the filename "70 µm" INCLUDES the ~15–20 µm
# SUS/c-SUS collector and must NOT be used for σ.  Symmetric cell = SUS|cathode|SUS =
# ION-BLOCKING (SUS passes e⁻, blocks Li⁺) → the DC arc R1 = ELECTRONIC resistance R_e
# → σ_e = L_composite / R1  (Hebb-Wagner).  L range → σ_e carries ±~11 %.
_THICK_UM = 45.0            # composite mid (40–50); collector excluded — DEFAULT (셀별 미지정 시)
_THICK_RANGE_UM = (40.0, 50.0)
# ★셀별 두께 override (filename stem → composite µm) — webapp 두께 입력이 여기 씀.  σ_e ∝ L 이라
#   두께가 σ_e 절대값을 바로 정함.  없으면 위 45µm 기본.
_THICK_OVERRIDES_PATH = os.path.join(EIS, 'thickness_overrides.json')


def _load_thickness_overrides():
    """이종기술/eis/thickness_overrides.json ({stem: µm}) → dict.  없으면 빈 dict."""
    import json
    try:
        return {str(k): float(v) for k, v in json.load(open(_THICK_OVERRIDES_PATH)).items()
                if v not in (None, '') and float(v) > 0}
    except Exception:
        return {}


def _load(csv_path):
    f, re_z, im_z = [], [], []
    for row in csv.DictReader(open(csv_path)):
        f.append(float(row['freq_Hz']))
        re_z.append(float(row['ReZ_ohm']))
        im_z.append(float(row['negImZ_ohm']))     # -Im(Z), positive = capacitive
    f = np.array(f)
    Z = np.array(re_z) - 1j * np.array(im_z)       # Z = Re + j Im,  Im = -negImZ
    return f, Z


def _crop_capacitive(f, Z):
    """Drop the leading high-freq inductive points (Im(Z) > 0) that the RC/Warburg
    models can't represent; keep from the first capacitive point downward in freq."""
    neg_im = -Z.imag                                # = negImZ (capacitive > 0)
    keep = neg_im > 0
    if keep.any():
        first = int(np.argmax(keep))                # first capacitive index (data is HF->LF)
        return f[first:], Z[first:]
    return f, Z


def _hf_intercept(f, Z):
    """Series resistance R_s = high-freq real-axis intercept (-Im crosses 0)."""
    neg_im = -Z.imag
    for i in range(len(neg_im) - 1):
        if neg_im[i] <= 0 and neg_im[i + 1] > 0:
            t = -neg_im[i] / (neg_im[i + 1] - neg_im[i])
            return float(Z.real[i] + t * (Z.real[i + 1] - Z.real[i]))
    return float(Z.real[int(np.argmin(np.abs(neg_im)))])


def _cell_type(stem):
    return 'symmetric' if 'sym' in stem else 'full' if 'full' in stem else 'unknown'


def _rmse_pct(Z, Zf):
    return float(100.0 * np.sqrt(np.mean(np.abs(Z - Zf) ** 2)) / np.mean(np.abs(Z)))


def _cpe_to_cdl_uF_cm2(Q, a, R1_ohm, area_cm2):
    """CPE(Q,α) ‖ R1 아크 → 유효 이중층 정전용량 (Brug/Hsu-Mansfeld):
        C_eff = Q^(1/α) · R1^((1−α)/α)  [F]   (분산표면 대표 C; α<1 depressed arc)
    면적정규화 → µF/cm²geo.  R1 = 아크 병렬저항[Ω] (비정규화 — CPE Q 도 Ω기반 피팅값이라 정합).
    ★ 이것이 physics_eis C_dl 앵커(§F1): 실험 EIS 의 실측 이중층 → 모델 C_dl 을 문헌 대신 실측으로 고정."""
    try:
        Q = float(Q); a = float(a); R1_ohm = float(R1_ohm); area_cm2 = float(area_cm2)
    except (TypeError, ValueError):
        return ''
    if not (Q > 0 and 0 < a <= 1 and R1_ohm > 0 and area_cm2 > 0):
        return ''
    C_eff_F = (Q ** (1.0 / a)) * (R1_ohm ** ((1.0 - a) / a))
    if not math.isfinite(C_eff_F):
        return ''
    return round(C_eff_F / area_cm2 * 1e6, 1)                   # F → µF/cm²geo


def fit_one(CustomCircuit, stem, f, Z, cell_type, r0_fixed):
    """Fit with R0 FIXED to the measured HF intercept (well-determined from data);
    only the arc (+Warburg) is free.  Return (params, Zfit, circuit, rmse_pct)."""
    neg_im = -Z.imag
    r1 = max(float(Z.real.max() - r0_fixed), 1.0)
    f_pk = f[int(np.argmax(neg_im))]
    q = 1.0 / (2 * math.pi * max(f_pk, 1e-3) * r1)          # C ~ 1/(w_pk R)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        if cell_type == 'symmetric':
            circ = 'R0-p(R1,CPE1)'
            guess = [r1, q, 0.7]
            names = ['R1', 'CPE1_Q', 'CPE1_a']
        else:
            circ = 'R0-p(R1,CPE1)-Wo1'
            guess = [r1 * 0.5, q, 0.7, r1 * 0.5, 1.0]
            names = ['R1', 'CPE1_Q', 'CPE1_a', 'Wo1_R', 'Wo1_tau']
        try:
            cc = CustomCircuit(initial_guess=guess, circuit=circ,
                               constants={'R0': float(r0_fixed)})
            cc.fit(f, Z, global_opt=False)
            Zf = cc.predict(f)
            p = dict(zip(names, [float(x) for x in cc.parameters_]))
            p['R0'] = float(r0_fixed)
            return p, Zf, circ, _rmse_pct(Z, Zf)
        except Exception as e:
            return {'error': str(e)[:60]}, None, circ, float('nan')


def main():
    os.makedirs(FITS, exist_ok=True)
    from impedance.models.circuits import CustomCircuit
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    stems = sorted(s[:-4] for s in os.listdir(EXTRACTED) if s.endswith('.csv'))
    _tov = _load_thickness_overrides()                       # 셀별 두께 (webapp 입력; 없으면 45µm)
    rows, panels = [], []
    for stem in stems:
        ct = _cell_type(stem)
        area = AREA.get(ct, float('nan'))
        f_all, Z_all = _load(os.path.join(EXTRACTED, stem + '.csv'))
        r0 = _hf_intercept(f_all, Z_all)               # measured series R (fixed in fit)
        f, Z = _crop_capacitive(f_all, Z_all)
        p, Zf, circ, rmse = fit_one(CustomCircuit, stem, f, Z, ct, r0)
        row = {'filename': stem, 'cell_type': ct, 'area_cm2': area, 'circuit': circ,
               'rmse_pct': round(rmse, 2) if rmse == rmse else '',
               'R_s_ohm': '', 'R1_ohm': '', 'R_w_ohm': '',
               'R_s_ohmcm2': '', 'R1_ohmcm2': '', 'R_w_ohmcm2': '',
               'CPE_a': '', 'CPE_Q': '', 'C_dl_uF_cm2': '',
               'L_composite_um': '', 'sigma_e_mScm': '', 'sigma_e_range_mScm': '',
               'note': ''}
        if 'error' in p:
            row['note'] = 'fit_fail: ' + p['error']
        else:
            row['R_s_ohm'] = round(p['R0'], 3)
            row['R1_ohm'] = round(p['R1'], 3)
            row['CPE_a'] = round(p.get('CPE1_a', float('nan')), 3)
            row['CPE_Q'] = float(f"{p.get('CPE1_Q', float('nan')):.4e}")   # S·s^α (CPE 크기)
            # C_dl(Brug): full=파라데익 이중층(R1=R_int 아크) = C_dl 앵커; symmetric=SUS 블로킹/기하 C (라벨 구분)
            row['C_dl_uF_cm2'] = _cpe_to_cdl_uF_cm2(p.get('CPE1_Q'), p.get('CPE1_a'), p.get('R1'), area)
            row['R_s_ohmcm2'] = round(p['R0'] * area, 2)
            r1_asr = p['R1'] * area
            row['R1_ohmcm2'] = round(r1_asr, 2)
            if 'Wo1_R' in p:
                row['R_w_ohm'] = round(p['Wo1_R'], 3)
                row['R_w_ohmcm2'] = round(p['Wo1_R'] * area, 2)
            if ct == 'symmetric':                       # SUS ion-blocking → R1=R_e → σ_e=L/R1
                _meas = stem in _tov                     # 셀별 두께 지정되면 그걸로 (없으면 45µm 기본)
                thick = _tov[stem] if _meas else _THICK_UM
                t_lo, t_hi = (thick - 2.0, thick + 2.0) if _meas else _THICK_RANGE_UM
                row['L_composite_um'] = thick
                row['sigma_e_mScm'] = round(thick * 1e-4 / r1_asr * 1e3, 4)       # L[cm]/R[Ω·cm²]→S/cm→mS/cm
                lo = round(max(t_lo, 0.1) * 1e-4 / r1_asr * 1e3, 4)
                hi = round(t_hi * 1e-4 / r1_asr * 1e3, 4)
                row['sigma_e_range_mScm'] = f'{lo}-{hi}'
                row['note'] = ('SUS ion-blocking → R1=R_e; σ_e=L/R1 '
                               + (f'(L={thick:g}µm 지정)' if _meas else '(L=45µm 기본; 표서 두께 변경 가능)'))
            else:
                row['note'] = 'R1=R_int, Wo=R_w (primer-SUS full cell)'
        rows.append(row)
        panels.append((stem, f, Z, Zf, area, row))

    cols = ['filename', 'cell_type', 'area_cm2', 'circuit', 'rmse_pct',
            'R_s_ohm', 'R1_ohm', 'R_w_ohm', 'R_s_ohmcm2', 'R1_ohmcm2', 'R_w_ohmcm2',
            'CPE_a', 'CPE_Q', 'C_dl_uF_cm2', 'L_composite_um', 'sigma_e_mScm',
            'sigma_e_range_mScm', 'note']
    with open(os.path.join(FITS, 'eis_fit_results.csv'), 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    # ★ REPRESENTATIVE means — "유동적으로 열어두는" 대표값: recomputed every run, so adding cells
    #   (eis_archive → eis_fit) auto-updates the numbers the model anchors on.  full R_int = the
    #   4-cell SOC100 mean (range wide → representative, not final; see README re-experiment note).
    import statistics as _st

    def _meancol(ct, key):
        v = [float(r[key]) for r in rows if r['cell_type'] == ct and r.get(key, '') != '']
        return (round(_st.mean(v), 2), round(min(v), 2), round(max(v), 2), len(v)) if v else ('', '', '', 0)
    ri_mean, ri_lo, ri_hi, n_full = _meancol('full', 'R1_ohmcm2')
    se_mean, se_lo, se_hi, n_sym = _meancol('symmetric', 'sigma_e_mScm')
    summ = {'metric': ['full_R_int_ohmcm2', 'full_R_s_ohmcm2', 'full_R_w_ohmcm2',
                       'full_C_dl_uF_cm2', 'sym_R_e_ohmcm2', 'sym_sigma_e_mScm'],
            'src': ['SOC100 4-cell', 'SOC100 4-cell', 'SOC100 4-cell',
                    'SOC100 4-cell (CPE→Brug)', 'symmetric', 'symmetric']}
    keys = [('full', 'R1_ohmcm2'), ('full', 'R_s_ohmcm2'), ('full', 'R_w_ohmcm2'),
            ('full', 'C_dl_uF_cm2'), ('symmetric', 'R1_ohmcm2'), ('symmetric', 'sigma_e_mScm')]
    with open(os.path.join(FITS, 'summary_means.csv'), 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['metric', 'mean', 'min', 'max', 'n', 'src'])
        for (ct, k), m, s in zip(keys, summ['metric'], summ['src']):
            mn, lo, hi, n = _meancol(ct, k)
            w.writerow([m, mn, lo, hi, n, s])
    print(f"  ★ representative full-cell R_int = {ri_mean} Ω·cm² (range {ri_lo}-{ri_hi}, n={n_full}); "
          f"sym σ_e = {se_mean} mS/cm (n={n_sym})  → fits/summary_means.csv")

    # per-file fit figure (data pts + fit line), Ω·cm²
    n = len(panels)
    ncol = 4
    nrow = (n + ncol - 1) // ncol
    fig, ax = plt.subplots(nrow, ncol, figsize=(4 * ncol, 3.6 * nrow))
    ax = np.array(ax).reshape(-1)
    for i, (stem, f, Z, Zf, area, row) in enumerate(panels):
        a = ax[i]
        a.plot(Z.real * area, -Z.imag * area, 'o', ms=3, color='#1f77b4', label='data')
        if Zf is not None:
            a.plot(Zf.real * area, -Zf.imag * area, '-', color='#d62728', lw=1.3, label='fit')
        a.set_title(stem.replace('260719_', '').replace('260715_', ''), fontsize=7)
        rlbl = (f"Rs={row['R_s_ohmcm2']} R1={row['R1_ohmcm2']}"
                + (f" Rw={row['R_w_ohmcm2']}" if row['R_w_ohmcm2'] != '' else '')
                + f"\nrmse={row['rmse_pct']}%")
        a.text(0.03, 0.97, rlbl, transform=a.transAxes, fontsize=6.5, va='top',
               bbox=dict(boxstyle='round', fc='white', alpha=.7))
        a.set_xlabel("Z' (Ω·cm²)", fontsize=7)
        a.set_ylabel("-Z'' (Ω·cm²)", fontsize=7)
        a.tick_params(labelsize=6)
        a.axhline(0, color='k', lw=.4)
    for j in range(n, len(ax)):
        ax[j].axis('off')
    plt.tight_layout()
    plt.savefig(os.path.join(FITS, 'eis_fits.png'), dpi=120)
    ok = sum(1 for r in rows if r['note'].startswith('fit_fail') is False and r['R1_ohm'] != '')
    print(f'  fit {ok}/{len(rows)} -> {os.path.relpath(os.path.join(FITS, "eis_fit_results.csv"), ROOT)}')
    return rows


if __name__ == '__main__':
    main()
