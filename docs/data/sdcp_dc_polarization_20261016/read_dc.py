#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SBE · DBE DC 분극 원자료 (`raw/dc_polarization_20261016.zip` · BioLogic .mpr 16) → 정상 상태 저항 · σ_e (읽기만).

  pip download galvani==0.5.0 --no-deps --no-binary :all: -d <빈 폴더>    # sdist sha256 da0e3b34b114bf615caf3061fc72ef0ab59d2e175bbfd580a22977c290928270
  tar -xzf <빈 폴더>/galvani-0.5.0.tar.gz -C <다른 빈 폴더>
  python3 -I docs/data/sdcp_dc_polarization_20261016/read_dc.py --galvani <다른 빈 폴더>/galvani-0.5.0 --out dc_reading.json

규약 (1저자 10-19): 두께 SBE 90 µm · DBE 80 µm · 지름 10 mm (`10pi`) · 지그 · 리드 저항은 빼지 않는다.
판독: 파일마다 마지막 60 s 평균 (E · I) · 시료마다 8 점 (±5 · 10 · 15 · 20 mV) 최소제곱 I = G·E + b → R = 1/G (오프셋 = −b/G) ·
쌍 저항 R_pair = (E₊ − E₋)/(I₊ − I₋) · σ = L/(R·A) · A = π (0.5 cm)².  ZIP 은 임시 빈 폴더에 풀어 읽기만 한다 (안의 것을 실행하지 않는다).
"""
import argparse
import hashlib
import json
import math
import os
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ZIP_SHA256 = '50076bb02462fe57b2f249ffe19d5a954502ce23e10ee657c8b0b3ef4c81ad48'
L_UM = {'SBE': 90.0, 'DBE': 80.0}
D_MM = 10.0
WINDOW_S = 60.0
NAME = re.compile(r'(SBE|DBE)_10pi_2_0_(\d+)V(_minus)?_(C\d+)\.mpr$')


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--galvani', required=True, help='galvani 0.5.0 소스 폴더 (galvani/ 를 담은 곳)')
    ap.add_argument('--zip', default=str(HERE / 'raw' / 'dc_polarization_20261016.zip'))
    ap.add_argument('--out', default='')
    a = ap.parse_args(argv)
    raw = Path(a.zip).read_bytes()
    if hashlib.sha256(raw).hexdigest() != ZIP_SHA256:
        sys.exit(f'ZIP sha256 ≠ 기록 ({ZIP_SHA256[:16]}…) — 다른 파일')
    sys.path.insert(0, a.galvani)
    import numpy as np
    from galvani import BioLogic as B
    A_cm2 = math.pi * (D_MM / 20.0) ** 2
    td = Path(tempfile.mkdtemp(prefix='dc_read_'))
    rows = []
    try:
        with zipfile.ZipFile(a.zip) as z:
            for n in z.namelist():
                if '/' in n or n.startswith('.') or not NAME.match(n):
                    sys.exit(f'모르는 항목 {n!r}')
            z.extractall(td)
        for n in sorted(os.listdir(td)):
            m = NAME.match(n)
            x = B.MPRfile(str(td / n)).data
            t, E, I = x['time/s'], x['Ewe/V'] * 1e3, x['<I>/mA']
            last = t >= t[-1] - WINDOW_S
            slope = np.polyfit(t[last], I[last], 1)[0]
            rows.append(dict(file=n, sample=m.group(1), channel=m.group(4), v_mV=float('0.' + m.group(2)) * 1000, minus=bool(m.group(3)),
                             npts=int(len(x)), dur_s=float(t[-1] - t[0]), E_ss_mV=float(E[last].mean()), I_ss_mA=float(I[last].mean()),
                             drift_pct_per_min=float(slope * 60 / I[last].mean() * 100)))
    finally:
        shutil.rmtree(td, ignore_errors=True)
    out = {'zip_sha256': ZIP_SHA256, 'thickness_um': L_UM, 'diameter_mm': D_MM, 'area_cm2': A_cm2, 'window_s': WINDOW_S,
           'galvani': '0.5.0', 'rows': rows, 'samples': {}}
    for smp in ('SBE', 'DBE'):
        rr = [r for r in rows if r['sample'] == smp]
        E = np.array([r['E_ss_mV'] for r in rr])
        I = np.array([r['I_ss_mA'] for r in rr])
        G, b = np.polyfit(E, I, 1)
        pred = G * E + b
        r2 = 1 - float(((I - pred) ** 2).sum() / ((I - I.mean()) ** 2).sum())
        R = 1.0 / G
        pairs = {}
        for v in sorted({r['v_mV'] for r in rr}):
            p_ = next(r for r in rr if r['v_mV'] == v and not r['minus'])
            m_ = next(r for r in rr if r['v_mV'] == v and r['minus'])
            Rp = (p_['E_ss_mV'] - m_['E_ss_mV']) / (p_['I_ss_mA'] - m_['I_ss_mA'])
            pairs[f'{v:g}'] = {'R_ohm': Rp, 'sigma_mScm': L_UM[smp] * 1e-4 / (Rp * A_cm2) * 1e3}
        out['samples'][smp] = {'n': len(rr), 'R_ohm': R, 'offset_mV': float(-b / G), 'r2': r2,
                               'sigma_mScm': L_UM[smp] * 1e-4 / (R * A_cm2) * 1e3, 'pairs': pairs}
        print(f"{smp}: R {R:.4f} Ω · r² {r2:.6f} · 오프셋 {-b / G:+.3f} mV · σ_e {out['samples'][smp]['sigma_mScm']:.3f} mS/cm "
              f"(L {L_UM[smp]:g} µm · Ø {D_MM:g} mm) · 쌍 R {min(q['R_ohm'] for q in pairs.values()):.4f}–{max(q['R_ohm'] for q in pairs.values()):.4f} Ω")
    s, d = out['samples']['SBE']['sigma_mScm'], out['samples']['DBE']['sigma_mScm']
    out['ratio_dbe_sbe'] = d / s
    print(f'비 DBE/SBE {d / s:.3f}')
    if a.out:
        Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
