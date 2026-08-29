#!/usr/bin/env python3
"""AM 입자당 전도성-첨가제(CBD) 접촉 수 — Table S3 의 `Median CBD contacts per AM`.

    python3 scripts/cbd_contacts_per_am.py --bed <run_dir> --scaffold am_scaffold.csv
    python3 scripts/cbd_contacts_per_am.py --selftest

★ 왜 이 스크립트가 필요한가.  침대는 **복셀 배열**로만 저장돼 있다 (`phase.npy` 등,
침대당 ≈ 1.9 GB).  `phase.npy` 는 int8 이라 *"이 복셀은 VGCF"* 는 알아도 *"몇 번 AM 입자"*
는 모른다.  AM 개체 정보는 런 디렉터리 **밖의** `am_scaffold.csv` (AM 1,271개) 에 있다.
⇒ 둘을 합쳐야 **입자별** 접촉 수가 나온다.

세는 방법 (규약을 여기 못박는다 — 나중에 바꾸면 값이 바뀐다):

  · **접촉** = AM 구 표면에서 `--band` (기본 1 복셀) 안에 있는 복셀 중 첨가제 상인 것.
  · **접촉 수** = 그 복셀들이 속한 **서로 다른 첨가제 개체(object)의 개수**.
    ⚠ 복셀 개수가 아니다 — 굵은 섬유 하나가 여러 복셀을 차지해도 접촉 1 이다.
    개체 구분은 `fibre.npy` (복셀별 개체 id) 로 한다.
  · **CBD 구성**: 기본은 **전도성** 첨가제만 = VGCF(2) + SDCP(5).  PTFE(4)는 절연이라
    기본에서 뺀다.  `--include-ptfe` 로 넣을 수 있다 — v6 의 433/517 이 어느 구성인지
    모르므로 **두 구성을 다 내고** 어느 쪽이 v6 과 맞는지 보고한다.

⚠⚠ **이 값은 규약 의존이다.**  band 폭·개체 정의·PTFE 포함 여부가 각각 값을 바꾼다.
그래서 산출물에 규약을 함께 적고, 원고에는 규약과 함께 인용한다.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

PHASE = {'VGCF': 2, 'PTFE': 4, 'SDCP': 5}
CONDUCTIVE = ('VGCF', 'SDCP')


def _load_scaffold(path):
    """AM 중심·반지름 (µm).  열 이름은 관용적인 것들을 받아들인다."""
    import csv
    xs, ys, zs, rs = [], [], [], []
    with open(path, newline='', encoding='utf-8') as fh:
        rd = csv.DictReader(fh)
        cols = {c.lower().strip(): c for c in (rd.fieldnames or [])}

        def pick(*names):
            for n in names:
                if n in cols:
                    return cols[n]
            raise SystemExit(f'am_scaffold 에 {names} 중 어느 열도 없다: {rd.fieldnames}')
        cx, cy, cz = pick('x', 'x_um'), pick('y', 'y_um'), pick('z', 'z_um')
        cr = pick('r', 'radius', 'r_um', 'radius_um')
        for row in rd:
            xs.append(float(row[cx])); ys.append(float(row[cy]))
            zs.append(float(row[cz])); rs.append(float(row[cr]))
    return xs, ys, zs, rs


def count_contacts(bed_dir, scaffold, vox_um, band_vox=1.0,
                   include_ptfe=False, max_am=None):
    """AM 입자별 접촉 개체 수를 센다.  numpy memmap 으로 읽어 전부 올리지 않는다."""
    import numpy as np

    phase = np.load(os.path.join(bed_dir, 'phase.npy'), mmap_mode='r')
    fid = np.load(os.path.join(bed_dir, 'fibre.npy'), mmap_mode='r')
    meta = json.load(open(os.path.join(bed_dir, 'mpm_metrics.json'), encoding='utf-8'))
    n_grid, nz = int(meta['n_grid']), int(meta['nz'])
    box_um = float(meta['um_box_um'])
    dx = box_um / n_grid                      # 가로 복셀 크기 (µm)

    if phase.size != n_grid * n_grid * nz:
        raise SystemExit(f'phase.npy 크기 {phase.size} != n_grid²·nz '
                         f'{n_grid}²·{nz} = {n_grid*n_grid*nz} — 격자 해석이 틀렸다')
    phase = phase.reshape(n_grid, n_grid, nz)
    fid = np.asarray(fid).reshape(n_grid, n_grid, nz)

    kinds = list(CONDUCTIVE) + (['PTFE'] if include_ptfe else [])
    codes = [PHASE[k] for k in kinds]

    xs, ys, zs, rs = _load_scaffold(scaffold)
    if max_am:
        xs, ys, zs, rs = xs[:max_am], ys[:max_am], zs[:max_am], rs[:max_am]

    band = band_vox * dx
    out = []
    for x, y, z, r in zip(xs, ys, zs, rs):
        #  AM 구를 감싸는 껍질만 훑는다 — 전체 격자를 도는 대신
        lo = [int(np.floor((c - r - band) / dx)) for c in (x, y, z)]
        hi = [int(np.ceil((c + r + band) / dx)) for c in (x, y, z)]
        i0, j0, k0 = (max(0, v) for v in lo)
        i1 = min(n_grid, hi[0] + 1); j1 = min(n_grid, hi[1] + 1)
        k1 = min(nz, hi[2] + 1)
        if i0 >= i1 or j0 >= j1 or k0 >= k1:
            out.append(0)
            continue
        sub_p = np.asarray(phase[i0:i1, j0:j1, k0:k1])
        sub_f = fid[i0:i1, j0:j1, k0:k1]
        ii, jj, kk = np.meshgrid(np.arange(i0, i1), np.arange(j0, j1),
                                 np.arange(k0, k1), indexing='ij')
        d = np.sqrt(((ii + 0.5) * dx - x) ** 2 + ((jj + 0.5) * dx - y) ** 2
                    + ((kk + 0.5) * dx - z) ** 2)
        shell = (d >= r) & (d <= r + band)
        m = shell & np.isin(sub_p, codes)
        out.append(int(np.unique(sub_f[m]).size) if m.any() else 0)
    return out, dict(vox_um=dx, band_um=band, band_vox=band_vox,
                     kinds=kinds, n_am=len(out), box_um=box_um,
                     n_grid=n_grid, nz=nz)


def summarise(counts):
    import statistics as st
    s = sorted(counts)
    return dict(n=len(s), median=st.median(s), mean=round(st.fmean(s), 2),
                p10=s[len(s) // 10], p90=s[-max(1, len(s) // 10)],
                min=s[0], max=s[-1], zero=sum(1 for v in s if v == 0))


# =========================================================================
def selftest() -> int:
    fails = []

    def chk(name, cond, detail=''):
        (print(f'  ok   {name}') if cond
         else (fails.append(name), print(f'  FAIL {name} {detail}')))

    print('cbd_contacts selftest')
    try:
        import numpy as np
    except ImportError:
        print('  numpy 없음 — 렌더 검사 생략'); return 0
    import tempfile, csv

    #  합성 침대: 32³ 격자, 가운데 AM 구 하나, 첨가제 개체 3개를 그 표면에 붙인다
    n, nz = 32, 32
    with tempfile.TemporaryDirectory() as td:
        phase = np.zeros((n, n, nz), dtype=np.int8)
        fidv = np.zeros((n, n, nz), dtype=np.float32)
        box = 32.0                      # µm → dx = 1.0 µm
        cx = cy = cz = 16.0
        r = 5.0
        ii, jj, kk = np.meshgrid(np.arange(n), np.arange(n), np.arange(nz), indexing='ij')
        d = np.sqrt(((ii + .5) - cx) ** 2 + ((jj + .5) - cy) ** 2 + ((kk + .5) - cz) ** 2)
        shell = (d >= r) & (d <= r + 1.0)
        idx = np.argwhere(shell)
        #  세 개체를 껍질에 심는다 — 하나는 복셀 여러 개 (개체 수 ≠ 복셀 수 검사)
        for oid, cells in ((11, idx[:5]), (12, idx[10:11]), (13, idx[20:21])):
            for c in cells:
                phase[tuple(c)] = PHASE['VGCF']; fidv[tuple(c)] = oid
        #  PTFE 개체 하나 — 기본에서 빠져야 한다
        c = idx[30]; phase[tuple(c)] = PHASE['PTFE']; fidv[tuple(c)] = 99
        #  껍질 **밖**이지만 넓힌 band 안에는 드는 첨가제 — 기본에선 빠지고 band↑ 면 들어와야
        #  한다.  ⚠ `argwhere(d > r+3)[0]` 로 뽑으면 격자 코너(거리 ≈ 27)가 잡혀 band 6
        #  으로도 안 들어온다 — 거리를 **구간으로** 지정해 뽑는다.
        far = np.argwhere((d > r + 3.0) & (d < r + 4.0))[0]
        phase[tuple(far)] = PHASE['VGCF']; fidv[tuple(far)] = 77

        np.save(os.path.join(td, 'phase.npy'), phase.ravel())
        np.save(os.path.join(td, 'fibre.npy'), fidv.ravel())
        json.dump(dict(n_grid=n, nz=nz, um_box_um=box),
                  open(os.path.join(td, 'mpm_metrics.json'), 'w'))
        sc = os.path.join(td, 'am.csv')
        with open(sc, 'w', newline='') as fh:
            w = csv.writer(fh); w.writerow(['x', 'y', 'z', 'r'])
            w.writerow([cx, cy, cz, r])

        cnt, info = count_contacts(td, sc, vox_um=1.0, band_vox=1.0)
        chk('전도성 개체 3개만 센다 (복셀 7개 → 개체 3)', cnt == [3], str(cnt))
        chk('PTFE 는 기본에서 빠진다', PHASE['PTFE'] not in
            [PHASE[k] for k in info['kinds']])
        chk('격자 크기가 metrics 에서 유도된다', abs(info['vox_um'] - 1.0) < 1e-9)

        cnt2, info2 = count_contacts(td, sc, vox_um=1.0, band_vox=1.0, include_ptfe=True)
        chk('--include-ptfe 면 4개', cnt2 == [4], str(cnt2))

        #  껍질 밖 개체가 안 세어지는지 (band 를 넓히면 세어져야 한다)
        cnt3, _ = count_contacts(td, sc, vox_um=1.0, band_vox=6.0)
        chk('band 를 넓히면 멀리 있는 개체가 들어온다', cnt3[0] > cnt[0],
            f'{cnt3} vs {cnt}')

        #  격자 불일치는 조용히 넘어가지 않는다
        json.dump(dict(n_grid=n + 1, nz=nz, um_box_um=box),
                  open(os.path.join(td, 'mpm_metrics.json'), 'w'))
        try:
            count_contacts(td, sc, vox_um=1.0)
            chk('격자 불일치를 잡는다', False, '예외가 안 났다')
        except SystemExit:
            chk('격자 불일치를 잡는다 (fail-closed)', True)

    s = summarise([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    chk('summarise: 중앙값·0 개수', s['median'] == 4.5 and s['zero'] == 1, str(s))
    print(f'\n{len(fails)} failure(s)')
    return 1 if fails else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--bed', help='침대 런 디렉터리 (phase.npy · fibre.npy · mpm_metrics.json)')
    ap.add_argument('--scaffold', help='am_scaffold.csv')
    ap.add_argument('--band-vox', type=float, default=1.0, help='접촉 판정 껍질 두께 (복셀)')
    ap.add_argument('--include-ptfe', action='store_true')
    ap.add_argument('--max-am', type=int, help='앞 N 개만 (시험용)')
    ap.add_argument('--out', help='결과 JSON')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not (a.bed and a.scaffold):
        ap.error('--bed 와 --scaffold 가 필요하다')

    res = {}
    for inc in (False, True):
        cnt, info = count_contacts(a.bed, a.scaffold, vox_um=None,
                                   band_vox=a.band_vox, include_ptfe=inc,
                                   max_am=a.max_am)
        tag = 'conductive+PTFE' if inc else 'conductive only (VGCF+SDCP)'
        res[tag] = dict(summary=summarise(cnt), convention=info)
        s = res[tag]['summary']
        print(f'── {tag}')
        print(f'   median {s["median"]}  mean {s["mean"]}  p10–p90 {s["p10"]}–{s["p90"]}  '
              f'min–max {s["min"]}–{s["max"]}  접촉 0 인 AM {s["zero"]}/{s["n"]}')
    print(f'\n규약: band {a.band_vox} vox = {res[tag]["convention"]["band_um"]:.4f} µm · '
          f'접촉 = 서로 다른 개체 수 (복셀 수 아님)')
    print('⚠ 이 값은 규약 의존이다 — band 폭·개체 정의·PTFE 포함 여부가 각각 값을 바꾼다.')
    if a.out:
        json.dump(res, open(a.out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f'wrote {a.out}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
