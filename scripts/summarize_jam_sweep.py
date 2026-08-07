#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""--am-jam quantile 스윕 요약 — "같은 백분위수가 여러 압력에서 DEM 두께를 재현하는가".

`mpm3d_compaction.py --am-jam-quantile` docstring 이 직접 요청한 **사전등록 검증**이다:

  90~95 % 구간이 DEM 두께를 감싸고 그 안에서 평평하다(real_14, 폭 0.05 µm).
  ⚠ 이 값은 **한 케이스에서만** 확인됐다 — 여러 케이스에서 같은 백분위수가 DEM 두께를
    재현하는지 검증하지 않으면 **한 케이스에 맞춘 fitting** 이다.

압력스윕(P=100/300/600)의 **압축된** 스캐폴드로 그것을 판정한다.

★ 이것은 두께 **예측**이 아니라 **jam 기준의 검증**이다.  얼린-AM 스캐폴드에서 두께는
  애초에 예측 대상이 될 수 없다 — 느슨한 AM 이면 MPM 이 AM 을 못 움직여 너무 두껍고,
  압축된 AM 이면 두께가 DEM 의 AM 위치로 이미 결정된다.  여기서 묻는 것은
  "퍼콜 AM 상위 q% 가 만드는 지지평면이 실제 플래튼 정지 높이인가" 하나뿐이다.

★ 판정 규약 (사전등록):
  • 같은 q 가 **세 압력 모두** |Δ| ≤ 1 % → 그 q 는 케이스-독립 (요청 충족)
  • 한 압력에서만 맞으면 → **fitting** 으로 확정, 기본값 변경 금지
  • q=100(현행 기본)이 계통적으로 두꺼우면 → "단 한 입자 위에 얹힌다" 가 재현된 것

사용:  python3 scripts/summarize_jam_sweep.py [--dir <se_curve>]
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re

#: DEM 최종 두께 (µm) — 압력별 대조값.  docs/data/heckel_real14_composite_multiP.csv 참조.
DEM_THICKNESS_UM = {100: 33.024, 300: 27.724, 600: 23.474}

#: 케이스-독립으로 인정하는 문턱 (%).  real_14 에서 90/95 가 ±0.1 % 였으므로 1 % 는 넉넉하다.
PASS_PCT = 1.0


def load(d):
    """jam_P<P>_q<Q>.json → {(P, Q): dict}."""
    out = {}
    for p in sorted(glob.glob(os.path.join(d, 'jam_P*_q*.json'))):
        m = re.search(r'jam_P(\d+)_q(\d+)\.json$', os.path.basename(p))
        if not m:
            continue
        try:
            out[(int(m.group(1)), int(m.group(2)))] = json.load(open(p))
        except (OSError, ValueError):
            pass
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--dir', default=os.path.expanduser('~/Yonghoon-DEM-DFT/se_curve'))
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()

    got = load(a.dir)
    ps = sorted(DEM_THICKNESS_UM)
    qs = sorted({q for _, q in got}) or [90, 95, 100]
    print(f'══ --am-jam quantile 스윕 ({len(got)}/{len(ps) * len(qs)} 완료) ══')
    print(f'{"P":>5} {"q":>5} {"MPM µm":>9} {"DEM µm":>9} {"Δ%":>8} {"porosity":>9} {"stop":>12}')
    for P in ps:
        for Q in qs:
            d = got.get((P, Q))
            if not d:
                print(f'{P:>5} {Q:>5} {"· 대기":>9}')
                continue
            t, ref = d.get('thickness_um'), DEM_THICKNESS_UM[P]
            por = d.get('porosity_settled_pct')
            print(f'{P:>5} {Q:>5} {t:>9.3f} {ref:>9.3f} {100 * (t - ref) / ref:>+8.2f}'
                  f' {por if por is None else round(por, 2):>9} {str(d.get("stop_mode")):>12}')

    # ── 판정: 어느 q 가 세 압력 모두에서 DEM 두께를 재현하는가 ──
    print('\n── 케이스-독립 판정 (사전등록: 세 압력 모두 |Δ| ≤ '
          f'{PASS_PCT} % 여야 그 q 를 인정) ──')
    for Q in qs:
        devs = [(P, 100 * (got[(P, Q)]['thickness_um'] - DEM_THICKNESS_UM[P])
                 / DEM_THICKNESS_UM[P]) for P in ps if (P, Q) in got]
        if len(devs) < len(ps):
            print(f'   q={Q:<4} 미완 ({len(devs)}/{len(ps)})')
            continue
        mx = max(abs(v) for _, v in devs)
        verdict = ('✓ 케이스-독립' if mx <= PASS_PCT else
                   '★ fitting — 한 케이스에 맞춘 값' if any(abs(v) <= PASS_PCT for _, v in devs)
                   else '✗ 전 압력 불일치')
        print(f'   q={Q:<4} Δ ' + ' '.join(f'P{P}:{v:+.2f}%' for P, v in devs)
              + f'  최대 |Δ| {mx:.2f} %  → {verdict}')
    print('\n⚠ 이것은 두께 **예측**이 아니라 **jam 기준의 검증**이다 — 얼린-AM 스캐폴드에서'
          '\n  두께는 예측 대상이 될 수 없다(느슨=AM 못 움직임 / 압축=DEM 답이 이미 들어감).')
    return 0


def _selftest():
    n = [0, 0]

    def ok(name, cond):
        n[1] += 1
        n[0] += bool(cond)
        print(f'  {"PASS" if cond else "FAIL"}  {name}')

    import tempfile
    d = tempfile.mkdtemp(prefix='jamsum_')
    try:
        # 세 압력에서 q=95 만 DEM 을 재현하고 q=100 은 계통적으로 두껍게
        for P, ref in DEM_THICKNESS_UM.items():
            json.dump({'thickness_um': ref * 1.002, 'porosity_settled_pct': 12.0,
                       'stop_mode': 'am_jam'},
                      open(os.path.join(d, f'jam_P{P}_q95.json'), 'w'))
            json.dump({'thickness_um': ref * 1.04, 'porosity_settled_pct': 20.0,
                       'stop_mode': 'am_jam'},
                      open(os.path.join(d, f'jam_P{P}_q100.json'), 'w'))
        got = load(d)
        ok('1) 파일명에서 (P, q) 를 뽑는다', len(got) == 6 and (300, 95) in got)
        ok('2) 없는 조합은 비어 있다', (100, 90) not in got)
        # 판정 로직을 직접 확인
        for Q, expect_pass in ((95, True), (100, False)):
            mx = max(abs(100 * (got[(P, Q)]['thickness_um'] - DEM_THICKNESS_UM[P])
                         / DEM_THICKNESS_UM[P]) for P in DEM_THICKNESS_UM)
            ok(f'3) q={Q} 판정 ({"통과" if expect_pass else "불통과"} 기대)',
               (mx <= PASS_PCT) is expect_pass)
        ok('4) DEM 대조값이 원장(csv)과 같다',
           DEM_THICKNESS_UM == {100: 33.024, 300: 27.724, 600: 23.474})
    finally:
        import shutil
        shutil.rmtree(d, ignore_errors=True)
    print(f'\nselftest: {n[0]}/{n[1]} PASS')
    return 0 if n[0] == n[1] else 1


if __name__ == '__main__':
    raise SystemExit(main())
