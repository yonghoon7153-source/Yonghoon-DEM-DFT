#!/usr/bin/env python3
"""접촉 유효성 검사 — **점착을 올리면 접촉모델이 먼저 죽는다**.

왜 이 검사가 필요한가 (실측 근거, 2026-09-19)
  믹서 팔 `E4`(CED 3e7 J/m³)를 정착시켰더니 지표는 멀쩡한 숫자를 냈는데
  (`H/R 2.023`) 그 밑에서 접촉모델이 무너져 있었다:
      겹침 δ/r_min  중앙 3.25 % · 90 % 3.92 % · **최대 197 %**
      드럼 벽 밖 입자 79 개 · 이미 삭제된 원자 2,296 개 (8,002 → 5,703)
  δ/r = 1.97 은 한 구의 중심이 상대 구의 **반대편 바깥**에 있다는 뜻이다
  = 겹침이 아니라 **통과**.  그 상태의 H/R 은 물리가 아니라 붕괴의 그림자다.

⚠ SJKR 은 겹침에 **선형**이고(`F = CED·2π·R*·δ`) Hertz 반발은 `δ^1.5` 다.
  ⇒ 평형은 언제나 존재하지만 CED 가 크면 **터무니없는 δ** 에서 잡힌다.
  ⇒ 연화된 영률(계산비용용 1e7 Pa)이 **점착 스윕의 천장을 정한다**.
     천장을 올리려면 E 를 올려야 하고 dt ∝ 1/√G 라 비용이 √E 로 는다.

⛔ 이 검사를 통과하지 못한 팔의 지표는 **인용하지 않는다**.

usage
  python3 scripts/check_contact_validity.py <덤프디렉터리> [...] [--label L]
  python3 scripts/check_contact_validity.py --selftest
"""
import argparse
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from measure_bed_aspect import frames, read_dump          # noqa: E402

#  판정선 — DEM 연질구 관례.  ⚠ 문턱이지 물리 상수가 아니다.
OVL_MEDIAN_WARN = 0.01      # 중앙 겹침 1 % 넘으면 경고
OVL_MAX_FAIL = 0.50         # 최대 겹침 50 % 넘으면 **기각** (통과 직전)
LOST_FAIL_PCT = 1.0         # 원자 1 % 넘게 잃으면 기각


def contacts(P, r, mol=None):
    """겹친 쌍의 (쌍, δ/r_min, 강체내부쌍수).

    ⚠⚠ **강체(multisphere) 내부 쌍을 빼야 한다** — 2026-09-19 실측으로 잡은 결함.
      섬유는 구를 `0.8·d` 간격으로 꿴 사슬이라 **설계상** `δ/r = 0.4` 로 겹쳐 있다.
      그것을 접촉으로 세면 다섯 팔 전부가 *"최대 겹침 40.0 %"* 를 내놓고, 그 값은
      점착과 아무 상관이 없다 (점착 0 인 `E0` 도 똑같이 40.0 %).
      ★ 그래서 나쁜 이유는 **보기 싫어서가 아니라 검사가 눈이 머는 것**이다:
        기각 문턱이 50 % 인데 섬유가 40 % 에 상주하면 **40~50 % 구간의 진짜 통과를
        못 본다**.  반대로 문턱을 조금만 내리면 모든 팔이 거짓 기각된다.
      ⇒ `mol` 이 같고 **양수**인 쌍만 제외한다.  LIGGGHTS 는 평범한 구에 `mol = -1`
        을 주므로 `> 0` 조건이 없으면 **평범한 구 쌍을 전부 지워** 버린다
        (실측: type 1·2·3 은 mol 고유값 1개 = −1).
      ★ 제외한 개수는 **보고한다** — 조용히 버리지 않는다.
    """
    try:
        from scipy.spatial import cKDTree
        pr = cKDTree(P).query_pairs(2 * r.max(), output_type='ndarray')
    except Exception:                                       # scipy 없으면 전수
        n = len(r)
        pr = np.array([(i, j) for i in range(n) for j in range(i + 1, n)])
    if len(pr) == 0:
        return pr, np.zeros(0), 0
    i, j = pr[:, 0], pr[:, 1]
    d = np.linalg.norm(P[i] - P[j], axis=1)
    ov = (r[i] + r[j]) - d
    m = ov > 0
    if mol is not None:
        same = (mol[i] == mol[j]) & (mol[i] > 0)            # ★ > 0 이 필수
        n_intra = int((m & same).sum())
        m = m & ~same
    else:
        n_intra = 0
    return pr[m], ov[m] / np.minimum(r[i], r[j])[m], n_intra


def check(d, n_expected=None, label=None):
    step, path = frames(d)[-1]
    D = read_dump(path)
    P = np.c_[D['x'], D['y'], D['z']]
    r = D['radius']
    pr, rel, n_intra = contacts(P, r, D.get('mol'))
    lost = (100.0 * (n_expected - len(r)) / n_expected) if n_expected else 0.0
    bad = []
    if len(rel) and float(np.max(rel)) > OVL_MAX_FAIL:
        bad.append(f'최대 겹침 {np.max(rel)*100:.0f} % > {OVL_MAX_FAIL*100:.0f} %')
    if lost > LOST_FAIL_PCT:
        bad.append(f'원자 손실 {lost:.1f} % > {LOST_FAIL_PCT} %')
    return dict(label=label or d, step=step, n=len(r), n_contact=len(pr),
                n_intra=n_intra,
                cn=(2.0 * len(pr) / len(r) if len(r) else float('nan')),
                ovl_med=(float(np.median(rel)) if len(rel) else 0.0),
                ovl_p90=(float(np.percentile(rel, 90)) if len(rel) else 0.0),
                ovl_max=(float(np.max(rel)) if len(rel) else 0.0),
                lost_pct=lost, reject=bad)


def report(rs):
    print(f'{"팔":14s} {"n":>6s} {"CN":>5s}  겹침 δ/r_min  중앙/90 %/최대      손실   강체내부   판정')
    for m in rs:
        v = '⛔ 기각' if m['reject'] else ('⚠ 경고' if m['ovl_med'] > OVL_MEDIAN_WARN else '✓')
        print(f'{m["label"]:14s} {m["n"]:6d} {m["cn"]:5.2f}  '
              f'{m["ovl_med"]*100:6.2f} / {m["ovl_p90"]*100:6.2f} / {m["ovl_max"]*100:7.1f} %'
              f'  {m["lost_pct"]:5.1f} %  {m.get("n_intra", 0):7d}   {v}')
        for b in m['reject']:
            print(f'{"":14s}   ⛔ {b}')
    if any(m['reject'] for m in rs):
        print('\n⛔ 기각된 팔이 있다 — 그 팔의 H/R 은 접촉모델이 푼 값이 아니다.  인용 금지.')
    return 1 if any(m['reject'] for m in rs) else 0


def _selftest():
    import tempfile
    ok, fail = 0, []

    def chk(name, cond):
        nonlocal ok
        if cond:
            ok += 1
        else:
            fail.append(name)
        print(('  PASS  ' if cond else '  FAIL  ') + name)

    def write(td, pts, name='t_100.liggghts'):
        with open(os.path.join(td, name), 'w') as fh:
            fh.write(f'ITEM: TIMESTEP\n100\nITEM: NUMBER OF ATOMS\n{len(pts)}\n')
            fh.write('ITEM: BOX BOUNDS mm mm mm\n-1 1\n-1 1\n-1 1\n')
            fh.write('ITEM: ATOMS id type x y z radius\n')
            for i, (X, Y, Z, R) in enumerate(pts):
                fh.write(f'{i+1} 1 {X} {Y} {Z} {R}\n')

    R = 0.001
    with tempfile.TemporaryDirectory() as td:               # 겹침 정확히 10 %
        write(td, [(0, 0, 0, R), (0.0019, 0, 0, R)])
        m = check(td)
        chk('① 겹침 δ/r 을 정확히 낸다 (설계 10 %)', abs(m['ovl_max'] - 0.10) < 1e-9)
        chk('② 10 % 는 기각이 아니다 (경고 영역)', not m['reject'])
    with tempfile.TemporaryDirectory() as td:               # 통과 — 중심이 반대편
        write(td, [(0, 0, 0, R), (0.0002, 0, 0, R)])
        m = check(td)
        chk(f'③ 통과(δ/r {m["ovl_max"]*100:.0f} %)를 **기각**한다', bool(m['reject']))
    with tempfile.TemporaryDirectory() as td:               # 닿지 않음
        write(td, [(0, 0, 0, R), (0.01, 0, 0, R)])
        m = check(td)
        chk('④ 안 닿으면 접촉 0 · 기각 없음',
            m['n_contact'] == 0 and not m['reject'] and m['ovl_max'] == 0.0)
    with tempfile.TemporaryDirectory() as td:               # 원자 손실
        write(td, [(0, 0, 0, R), (0.01, 0, 0, R)])
        m = check(td, n_expected=100)
        chk(f'⑤ 원자 손실을 기각한다 ({m["lost_pct"]:.0f} % 잃음)', bool(m['reject']))
    with tempfile.TemporaryDirectory() as td:               # ★ 변이 — 다분산에서 작은 쪽 기준
        write(td, [(0, 0, 0, 0.01), (0.0105, 0, 0, 0.001)])
        m = check(td)
        #  δ = 0.011 − 0.0105 = 0.0005 ;  r_min = 0.001 → 50 %  (큰 쪽 기준이면 5 %)
        chk(f'⑥ 변이: 겹침을 **작은 쪽 반경**으로 잰다 (50 %, 큰 쪽이면 5 %)',
            abs(m['ovl_max'] - 0.50) < 1e-9)
    #  ★★ ⑦ 강체 내부 쌍 — **실제로 검사를 멀게 했던 결함** (2026-09-19)
    #     섬유 사슬은 설계상 δ/r = 0.4 로 겹쳐 있다.  그것을 접촉으로 세면 다섯 팔
    #     전부가 "최대 40.0 %" 를 내놓고 40~50 % 구간의 진짜 통과를 못 본다.
    def write_mol(td, rows):
        with open(os.path.join(td, 'm_100.liggghts'), 'w') as fh:
            fh.write(f'ITEM: TIMESTEP\n100\nITEM: NUMBER OF ATOMS\n{len(rows)}\n')
            fh.write('ITEM: BOX BOUNDS mm mm mm\n-1 1\n-1 1\n-1 1\n')
            fh.write('ITEM: ATOMS id type mol x y z radius\n')
            for i, (ty, mo, X, Y, Z, RR) in enumerate(rows):
                fh.write(f'{i+1} {ty} {mo} {X} {Y} {Z} {RR}\n')
    with tempfile.TemporaryDirectory() as td:
        #  강체 2구는 40 % 겹침(mol 7) · 평범한 구 2개는 mol −1 로 5 % 겹침
        #  강체쌍: 중심거리 0.0016 → δ = 0.0004 → δ/r = 40 % (섬유 사슬과 같은 값)
        #  평구쌍: 중심거리 0.00195 → δ = 0.00005 → δ/r = 5 %
        write_mol(td, [(4, 7, 0.0, 0, 0, R), (4, 7, 0.0016, 0, 0, R),
                       (1, -1, 0.01, 0, 0, R), (1, -1, 0.01195, 0, 0, R)])
        m = check(td)
        chk(f'⑦ 강체 내부 쌍(40 %)을 빼고 잰다 (남은 최대 {m["ovl_max"]*100:.0f} %)',
            abs(m['ovl_max'] - 0.05) < 1e-9 and m['n_intra'] == 1 and m['n_contact'] == 1)
        #  ★ 변이 — mol>0 조건이 없으면 평범한 구 쌍(mol −1 끼리)도 지워진다
        import numpy as _np
        P = _np.array([[0., 0, 0], [0.01, 0, 0], [0.01195, 0, 0]])
        rr = _np.array([R, R, R])
        mol_all = _np.array([-1., -1., -1.])
        _, rel_ok, _ = contacts(P, rr, mol_all)
        chk('⑦b 변이: mol = −1 끼리는 **같은 강체가 아니다** (평범한 구를 지우지 않는다)',
            len(rel_ok) == 1)
    print(f'\ncheck_contact_validity selftest: {ok}/{ok+len(fail)} PASS'
          + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('dirs', nargs='*')
    ap.add_argument('--label', action='append', default=None)
    ap.add_argument('--n-expected', type=int, default=None,
                    help='삽입 계획 원자 수 — 손실 판정에 쓴다')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    if not a.dirs:
        ap.error('디렉터리를 하나 이상 주세요')
    labs = a.label or [None] * len(a.dirs)
    raise SystemExit(report([check(d, a.n_expected, labs[i] if i < len(labs) else None)
                             for i, d in enumerate(a.dirs)]))
