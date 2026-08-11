#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""--am-jam quantile 스윕 판정기 — **2026-08-11 재계약** (Codex 적대리뷰 블로커 #1).

`mpm3d_compaction.py --am-jam-quantile` docstring 이 요구한 사전등록 검증:
"90~95 % 가 real_14 **한 케이스**에서 DEM 두께를 감쌌다 — 여러 케이스에서 같은
백분위수가 재현되지 않으면 한 케이스에 맞춘 fitting 이다."

★★ 옛 계약(2026-08-07)의 결함과 수정 — 이 파일의 존재 이유 ★★
옛 판정기는 P100/P300/P600 을 요구했고, jam 이 안 걸린 런(P100-q90)을 **사후에
제외**했다.  그것이 곧 결함이다:

  잘 작동한 q 만 분모에 남는 **post-treatment selection**.

`stop_mode` 도 MPM porosity 도 **q 가 바꾸는 출력**이다.  출력으로 표본을 거르면
"어떤 q 가 좋은가"를 그 q 의 성공 여부로 판정하게 된다.  그래서 새 계약은:

  ① 압력 제외는 **q 와 무관한 사전 정보**(DEM ε_union)로만 한다.
  ② q 가 만든 결과(jam 미발화·축퇴)는 **제외가 아니라 FAIL** 이다.
  ③ 런이 하나라도 없으면 그 q 가 아니라 **스윕 전체가 incomplete** 다.

★ 주장 한계 (사전 명시): 세 q 중 하나를 **같은 3 압력에서** 고르면 그것은
  "압력-독립 검증"이 아니라 **후보군 내 screening** 이다.  일반화를 주장하려면
  선택에 쓰지 않은 holdout(다른 압력 또는 독립 DEM realization)이 하나 더 필요하다.
  이 판정기는 그 구분을 출력에 박아 넣는다.

★ 두께가 지표인 이유이자 한계: 얼린-AM 스캐폴드에서 두께는 **예측 대상이 아니다**
  (느슨=AM 못 움직임 / 압축=DEM 답이 이미 들어감).  여기서 묻는 것은 하나뿐이다 —
  "퍼콜 AM 상위 q % 가 만드는 지지평면이 실제 플래튼 정지 높이인가."

사용:  python3 scripts/summarize_jam_sweep.py [--dir <se_curve>]
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re

#: 판정 압력 — DEM 최종 두께 (µm).  원장 docs/data/heckel_real14_composite_multiP.csv.
#: P200 = mesh_1940000.stl plate_z 0.0307597 (덱 단위 ×1000).
DEM_THICKNESS_UM = {100: 33.024, 200: 30.760, 300: 27.724}

#: ★ 사전 제외 (q 와 무관한 정보로만).  P600 은 DEM ε_union 0.69 % = 축퇴 —
#: 공극이 거의 없어 "잼 평면이 정지 높이인가"라는 질문 자체가 성립하지 않는다.
#: 이 판정은 **어떤 런보다 먼저** 내려졌고 q 출력에 의존하지 않는다.
PRE_EXCLUDED = {600: 'DEM ε_union 0.69 % (축퇴 — q 무관 사전정보)'}

#: 케이스-독립으로 인정하는 두께 문턱 (%).
PASS_PCT = 1.0

#: 축퇴 FAIL 문턱 — MPM porosity 가 이보다 낮으면 압밀이 아니라 붕괴다.
MIN_POROSITY_PCT = 2.0

QS = (90, 95, 100)


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


def judge_run(rec, P):
    """한 (P, q) 런 → (pass?, 사유, Δ%).  ★ 제외는 없다 — 못 하면 FAIL 이다."""
    if rec is None:
        return None, '런 없음', None                      # → 스윕 incomplete
    t = rec.get('thickness_um')
    if not isinstance(t, (int, float)) or not (t == t) or t <= 0:
        return False, 'FAIL 두께 비정상', None
    dev = 100.0 * (t - DEM_THICKNESS_UM[P]) / DEM_THICKNESS_UM[P]
    if rec.get('stop_mode') != 'am_jam':
        # ★ 옛 계약은 이것을 '제외' 했다.  jam 이 안 걸린 것은 그 q 가 그 압력에서
        #   정지 기준으로 **작동하지 않았다**는 결과다 → FAIL.
        return False, f'FAIL jam 미발화 (stop_mode={rec.get("stop_mode")})', dev
    por = rec.get('porosity_settled_pct')
    if isinstance(por, (int, float)) and por < MIN_POROSITY_PCT:
        return False, f'FAIL 축퇴 (porosity {por:.2f} < {MIN_POROSITY_PCT})', dev
    if abs(dev) > PASS_PCT:
        return False, f'FAIL 두께 |Δ| {abs(dev):.2f} > {PASS_PCT}', dev
    return True, 'PASS', dev


def summarize(got, ps=None, qs=QS):
    """→ (verdict, per_q dict).  런 누락이 하나라도 있으면 verdict='incomplete'."""
    ps = sorted(DEM_THICKNESS_UM) if ps is None else sorted(ps)
    per_q, missing = {}, []
    for Q in qs:
        rows = []
        for P in ps:
            ok, why, dev = judge_run(got.get((P, Q)), P)
            if ok is None:
                missing.append((P, Q))
            rows.append((P, ok, why, dev))
        per_q[Q] = rows
    if missing:
        return 'incomplete', per_q
    winners = [Q for Q in qs if all(r[1] for r in per_q[Q])]
    return ('screened' if winners else 'none'), per_q


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
    need = len(ps) * len(QS)
    print(f'══ --am-jam quantile 스윕 — 재계약판 ({len(got)}/{need} 런) ══')
    print(f'   판정 압력 {ps}   ·   사전 제외 ' +
          '; '.join(f'P{p} = {why}' for p, why in PRE_EXCLUDED.items()))
    print(f'   문턱: 두께 |Δ| ≤ {PASS_PCT} % · porosity ≥ {MIN_POROSITY_PCT} % · stop_mode = am_jam')
    print(f'\n{"P":>5} {"q":>5} {"MPM µm":>9} {"DEM µm":>9} {"Δ%":>8} {"porosity":>9} {"판정":>34}')
    for P in ps:
        for Q in QS:
            rec = got.get((P, Q))
            ok, why, dev = judge_run(rec, P)
            t = (rec or {}).get('thickness_um')
            por = (rec or {}).get('porosity_settled_pct')
            print(f'{P:>5} {Q:>5} '
                  f'{(f"{t:.3f}" if isinstance(t, (int, float)) else "·"):>9} '
                  f'{DEM_THICKNESS_UM[P]:>9.3f} '
                  f'{(f"{dev:+.2f}" if dev is not None else "·"):>8} '
                  f'{(f"{por:.2f}" if isinstance(por, (int, float)) else "·"):>9} '
                  f'{why:>34}')

    verdict, per_q = summarize(got)
    print('\n── 판정 (사전등록 2026-08-11) ──')
    if verdict == 'incomplete':
        print('   ⛔ INCOMPLETE — 런이 빠졌다.  빠진 런은 "제외"가 아니라 **미완**이다.')
        print('      부분 결과로 q 를 고르면 그것이 곧 selection bias 다.')
        for Q in QS:
            miss = [P for P, ok, _w, _d in per_q[Q] if ok is None]
            if miss:
                print(f'      q={Q:<4} 누락 P{miss}')
        return 2
    for Q in QS:
        rows = per_q[Q]
        n_pass = sum(1 for r in rows if r[1])
        mark = '✓' if n_pass == len(rows) else '✗'
        print(f'   {mark} q={Q:<4} {n_pass}/{len(rows)} 통과   ' +
              ' · '.join(f'P{P}:{("PASS" if ok else w.split()[1])}' for P, ok, w, _d in rows))
    winners = [Q for Q in QS if all(r[1] for r in per_q[Q])]
    print()
    if not winners:
        print('   ⇒ 어느 q 도 세 압력을 통과하지 못했다.  --am-jam-quantile 기본값 변경 금지.')
    else:
        print(f'   ⇒ 통과 q: {winners}')
        print('   ⚠ 이것은 **압력-독립의 증명이 아니다**.  세 q 를 같은 3 압력에서 고른 것이므로')
        print('     후보군 내 screening 이다.  일반화 주장에는 선택에 쓰지 않은 holdout')
        print('     (다른 압력 또는 독립 DEM realization) 이 하나 더 필요하다.')
    print('\n⚠ 두께는 **예측 대상이 아니라 jam 기준의 검증 지표**다 (얼린-AM 스캐폴드).')
    return 0 if winners else 1


def _selftest():
    n = [0, 0]

    def ok(name, cond):
        n[1] += 1
        n[0] += bool(cond)
        print(f'  {"PASS" if cond else "FAIL"}  {name}')

    import shutil
    import tempfile
    d = tempfile.mkdtemp(prefix='jamsum_')
    try:
        def put(P, Q, t_mult=1.002, por=12.0, stop='am_jam'):
            json.dump({'thickness_um': DEM_THICKNESS_UM[P] * t_mult,
                       'porosity_settled_pct': por, 'stop_mode': stop},
                      open(os.path.join(d, f'jam_P{P}_q{Q}.json'), 'w'))

        for P in DEM_THICKNESS_UM:
            put(P, 95)
            put(P, 100, t_mult=1.04)
            put(P, 90)
        got = load(d)
        ok('1) (P, q) 파싱 + 9 런 전부 인식', len(got) == 9 and (200, 95) in got)
        ok('2) ★ 판정 압력이 P200 을 포함한다 (옛 계약은 P600 이었다)',
           sorted(DEM_THICKNESS_UM) == [100, 200, 300])
        ok('3) P600 은 사전 제외로 명시 (q 무관 사유)', 600 in PRE_EXCLUDED and 600 not in DEM_THICKNESS_UM)
        v, per = summarize(got)
        ok('4) q95/q90 통과 · q100 불통과', v == 'screened'
           and all(r[1] for r in per[95]) and not all(r[1] for r in per[100]))

        # ★ 핵심 회귀: jam 미발화는 제외가 아니라 FAIL
        put(100, 90, stop='legacy_moving')
        got = load(d)
        _v, per = summarize(got)
        row = [r for r in per[90] if r[0] == 100][0]
        ok('5) ★ jam 미발화 = FAIL (옛 계약의 사후 제외가 아님)',
           row[1] is False and 'jam 미발화' in row[2])
        ok('6) ★ 그 q 는 통과 목록에서 빠진다 (분모에 남는다)',
           not all(r[1] for r in per[90]))

        # ★ 축퇴도 제외가 아니라 FAIL
        put(100, 90)                                   # 되돌리고
        put(300, 90, por=0.5)
        got = load(d)
        _v, per = summarize(got)
        row = [r for r in per[90] if r[0] == 300][0]
        ok('7) ★ porosity < 2 % = 축퇴 FAIL (제외 아님)',
           row[1] is False and '축퇴' in row[2])

        # ★ 런 누락 = 스윕 전체 incomplete
        os.unlink(os.path.join(d, 'jam_P200_q95.json'))
        v2, _p = summarize(load(d))
        ok('8) ★ 런 하나가 없으면 스윕 전체가 incomplete (부분 판정 금지)',
           v2 == 'incomplete')

        ok('9) DEM 대조값이 원장과 같다',
           DEM_THICKNESS_UM == {100: 33.024, 200: 30.760, 300: 27.724})
        ok('10) 두께 비정상(None) 은 FAIL 이지 통과가 아니다',
           judge_run({'thickness_um': None, 'stop_mode': 'am_jam'}, 100)[1].startswith('FAIL'))
    finally:
        shutil.rmtree(d, ignore_errors=True)
    print(f'\nselftest: {n[0]}/{n[1]} PASS')
    return 0 if n[0] == n[1] else 1


if __name__ == '__main__':
    raise SystemExit(main())
