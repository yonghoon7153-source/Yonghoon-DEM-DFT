#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SE 단독 펠릿 대칭셀 EIS (10-26 · BioLogic VSP-300 PEIS `.mpr` 4) → 나이퀴스트 핵심 점 · 실수축 절편 R (읽기만).

  python3 -I docs/data/se_pellet_eis_20261026/read_se_eis.py            # raw/ → extracted/*.csv · readings.json

판독기 = 자체 코드.  `.mpr` 형식 (머리 · 모듈 · 열 번호 → 자료형) 은 galvani 0.5.0 `BioLogic.py` 소스를 **읽어** 확인했고
그 코드는 실행하지 않았다 (열 번호 표의 값만 같다).  원자료 sha256 이 기록과 다르면 멈춘다.

절편 R (펠릿 = bulk + 입계 + 접촉 · 리드 · 7 MHz 위라 나눌 수 없다) 을 세 방법으로 적는다:
  ① −Im 이 0 을 지나는 점 (`scripts/eis_archive._rs_intercept` 와 같은 규칙)
  ② Z = R + jωL + 1/(Q(jω)^α) 맞춤 (|Z| 가중 · 창 7 MHz → 1 kHz · 100 Hz · 10 Hz) — 주 값 = 100 Hz 창
  ③ 꼬리 직선 외삽 (−Im 20–300 Ω 의 Re 대 −Im 직선 → −Im = 0)
⚠ 두께 · 지름 미측정 → σ 는 계산하지 않는다 (README §3).
"""
import csv
import hashlib
import json
import os
import struct
import sys

import numpy as np
from scipy.optimize import least_squares

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, 'raw')
EXT = os.path.join(HERE, 'extracted')
SHA = {
    '261026_SE_big_sym_01_C02.mpr': 'dea4cc17ebaeb2bf7c59b14fc0f625cf147451790a6be46a2f3dc269d302e101',
    '261026_SE_big_sym_02_C02.mpr': '5b3a64d5b2f136189818946fa4066f0bdcb575d8ee2b4b85b0905ea0ce54b22d',
    '261026_SE_small_sym_01_C01.mpr': '0c7f3c000c2901fc0147db8d1c58934d0744acb645f433b1ea04695bc1a3da1c',
    '261026_SE_small_sym_02_C01.mpr': '93668e4646de318c22dd8a3940882e1e983c365374ee2c47cd570815cb021bc4',
}
MAGIC = b'BIO-LOGIC MODULAR FILE\x1a'.ljust(48) + b'\x00\x00\x00\x00'
# 이 파일들에 나오는 열 번호만 (값 = galvani 0.5.0 VMPdata_colID_dtype_map) — 모르는 번호면 멈춘다
COLS = {32: ('freq', '<f4'), 37: ('re', '<f4'), 38: ('nim', '<f4'), 36: ('absz', '<f4'), 35: ('phase', '<f4'),
        4: ('t', '<f8'), 77: ('ewe', '<f4'), 76: ('i_mA', '<f4'), 169: ('cs_uF', '<f4'), 172: ('cp_uF', '<f4'),
        24: ('cycle', '<f8'), 39: ('irange', '<u2'), 33: ('abs_ewe', '<f4'), 34: ('abs_i', '<f4'), 131: ('ns', '<u2'),
        13: ('q', '<f8')}


def modules(raw):
    if raw[:len(MAGIC)] != MAGIC:
        raise SystemExit('BioLogic .mpr 머리가 아니다')
    p, out = len(MAGIC), []
    while p < len(raw):
        if raw[p:p + 6] != b'MODULE':
            raise SystemExit(f'MODULE 표지가 없다 (바이트 {p})')
        p += 6
        h = raw[p:p + 59]
        if h[35:39] == b'\xff\xff\xff\xff':                  # EC-Lab ≥ 11.50 머리
            length, version = struct.unpack('<2I', h[39:47])
            p += 59
        else:
            length, version = struct.unpack('<2I', h[35:43])
            p += 51
        out.append(dict(short=h[:10], length=length, version=version, data=raw[p:p + length]))
        p += length
    return out


def read_mpr(path):
    raw = open(path, 'rb').read()
    dm = [m for m in modules(raw) if m['short'] == b'VMP data  ']
    if len(dm) != 1:
        raise SystemExit('VMP data 모듈이 하나가 아니다')
    d, ver = dm[0]['data'], dm[0]['version']
    n, nc = struct.unpack('<I', d[:4])[0], d[4]
    if ver == 0 and not d[5]:
        ids, rem, start = list(d[5:5 + 2 * nc][1::2]), d[6 + 2 * nc:1006], 1007
    elif ver == 0:
        ids, rem, start = list(d[5:5 + nc]), d[5 + nc:100], 100
    elif ver in (2, 3):
        ids = list(struct.unpack('<%dH' % nc, d[5:5 + 2 * nc]))
        rem, start = d[5 + 2 * nc:405], (406 if ver == 3 else 405)
    else:
        raise SystemExit(f'모르는 데이터 모듈 판 {ver}')
    if any(rem):
        raise SystemExit('열 머리 뒤 남은 바이트가 0 이 아니다')
    if any(i not in COLS for i in ids):
        raise SystemExit(f'모르는 열 번호 {[i for i in ids if i not in COLS]}')
    dt = np.dtype([COLS[i] for i in ids])
    if len(d) - start != n * dt.itemsize:
        raise SystemExit('점 수 × 기록 길이 ≠ 데이터 길이')
    return np.frombuffer(d[start:], dtype=dt)


def zero_cross(re_, nim):
    for i in range(len(nim) - 1):
        if nim[i] <= 0 < nim[i + 1]:
            t = -nim[i] / (nim[i + 1] - nim[i])
            return float(re_[i] + t * (re_[i + 1] - re_[i]))
    return None


def fit_rlcpe(f, z, fmin):
    w, m = 2 * np.pi * f, f >= fmin

    def res(p):
        R, L, lq, a = p
        d = (R + 1j * w[m] * L + 1.0 / (10 ** lq * (1j * w[m]) ** a) - z[m]) / np.abs(z[m])
        return np.concatenate([d.real, d.imag])

    best = None
    for R0 in (20.0, 40.0):
        for lq0 in (-6.0, -5.0):
            s = least_squares(res, [R0, 1e-7, lq0, 0.85], bounds=([0, 0, -12, 0.3], [1e3, 1e-4, 0, 1.0]))
            if best is None or s.cost < best.cost:
                best = s
    R, L, lq, a = best.x
    return dict(R_ohm=round(float(R), 3), L_uH=round(float(L) * 1e6, 4), Q=float(f'{10 ** lq:.4g}'),
                alpha=round(float(a), 4), rel_rms=round(float(np.sqrt(np.mean(best.fun ** 2))), 4), npts=int(m.sum()))


def main():
    os.makedirs(EXT, exist_ok=True)
    out = {}
    for fn in sorted(SHA):
        p = os.path.join(RAW, fn)
        if hashlib.sha256(open(p, 'rb').read()).hexdigest() != SHA[fn]:
            raise SystemExit(f'{fn} sha256 ≠ 기록')
        x = read_mpr(p)
        f, re_, nim = x['freq'].astype(float), x['re'].astype(float), x['nim'].astype(float)
        z = re_ - 1j * nim
        lin = (nim >= 20) & (nim <= 300)
        c = np.polyfit(nim[lin], re_[lin], 1)
        out[fn] = dict(
            n=int(len(f)), f_max_Hz=float(f[0]), f_min_Hz=float(f[-1]), duration_s=round(float(x['t'][-1] - x['t'][0]), 1),
            ewe_mV=round(float(np.mean(x['ewe'])) * 1e3, 2),
            R_zero_cross_ohm=round(zero_cross(re_, nim), 3),
            R_fit={f'{fm:g}Hz': fit_rlcpe(f, z, fm) for fm in (1e3, 1e2, 10.0)},
            R_lin_extrap_ohm=round(float(c[1]), 3),
            nIm_monotone_after_cross=bool(np.all(np.diff(nim[nim > 0]) > 0)),
            phase_deg_at={f'{fq:g}Hz': round(float(x['phase'][int(np.argmin(np.abs(np.log10(f) - np.log10(fq))))]), 2)
                          for fq in (1e4, 1e3, 1e2, 10, 1, 0.1)},
            phase_deg_last=round(float(x['phase'][-1]), 2),
            Cs_uF_last=round(float(x['cs_uF'][-1]), 4), Cp_uF_last=round(float(x['cp_uF'][-1]), 4))
        with open(os.path.join(EXT, fn[:-4] + '.csv'), 'w', newline='') as fh:
            wr = csv.writer(fh, lineterminator='\n')
            wr.writerow(['freq_Hz', 'ReZ_ohm', 'negImZ_ohm', 'absZ_ohm', 'phase_deg', 'time_s', 'Ewe_V', 'I_mA', 'Cs_uF', 'Cp_uF', 'cycle'])
            for k in range(len(f)):
                wr.writerow([f'{x["freq"][k]:.7g}', f'{x["re"][k]:.7g}', f'{x["nim"][k]:.7g}', f'{x["absz"][k]:.7g}',
                             f'{x["phase"][k]:.7g}', f'{x["t"][k]:.9g}', f'{x["ewe"][k]:.7g}', f'{x["i_mA"][k]:.7g}',
                             f'{x["cs_uF"][k]:.7g}', f'{x["cp_uF"][k]:.7g}', int(x['cycle'][k])])
    with open(os.path.join(HERE, 'readings.json'), 'w', encoding='utf-8') as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1, sort_keys=True)
    for fn, v in out.items():
        print(fn, 'R(0교차)', v['R_zero_cross_ohm'], 'R(맞춤100Hz)', v['R_fit']['100Hz']['R_ohm'],
              'α', v['R_fit']['100Hz']['alpha'], 'R(직선)', v['R_lin_extrap_ohm'], '위상끝', v['phase_deg_last'], 'Ewe', v['ewe_mV'])
    return 0


if __name__ == '__main__':
    sys.exit(main())
