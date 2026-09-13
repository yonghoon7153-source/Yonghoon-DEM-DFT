#!/usr/bin/env python3
"""S2 검사 — **면적 cap 전환이 솔버의 `a_eff` 를 바꾸는가**.

정본 계약 = `docs/area_contract_20260913.md` (§2 · §4 의 S2) · 원장 = `AREA-12`.

★ 왜: 계약은 *"`A_surface`(상한 2πR_min²) 와 `A_transport`(상한 πR_min²) 로 쪼개면
  삭제됐던 협착 항이 되살아난다"* 를 전제했다.  그런데 솔버에는 **이미 clamp** 가 있다
  (`network_conductivity.py:395` `a_eff = min(a_contact, r_min_real)`).  clamp 는
  `a ≤ R_min` ⟺ `A ≤ πR_min²` 과 **같은 말**이다.  ⇒ 전환이 무엇을 바꾸는지 먼저 잰다.

★ **주장 (산술)** — 모든 입력에서 `a_eff` 가 같다:
      Lo   = max(A_hertz, A_ligg)                      (하한, `plastic_coverage.py:307`)
      A    = max(Lo, min(A_tabor, A_volume, 2πR²))     현행
      A'   = max(Lo, min(A_tabor, A_volume, 1πR²))     S2 전환
      a_eff = min(√(A/π), R)   ·   a'_eff = min(√(A'/π), R)
  `√(A/π) ≥ R  ⟺  A ≥ πR²` 이므로
   · `A' ≥ πR²` 이면 `a' = R`.  `A ≥ A' ≥ πR²` 이므로 `a = R`.  **같다.**
   · `A' < πR²` 이면 `Lo < πR²` 이고 `min(A_tabor, A_volume, πR²) < πR²` 라 그 min 은
     πR² 항이 아닌 데서 나온다 ⇒ `= min(A_tabor, A_volume)`.  그 값이 πR² 보다 작으니
     2πR² 보다도 작아 현행 min 과 같다 ⇒ `A' = A`.  **같다.**
  ⇒ **clamp 가 이미 수송 원판 상한을 강제하고 있다.**

⚠ **이것이 뜻하는 것**: S2 는 `network_conductivity` 의 σ 에 대해 **항등 변환**이다.
   *"협착 복원 → σ 하향"* 은 이 축에서 나오지 않는다.  ⛔ 그러나 **`A_physics` 자체는
   바뀐다** — coverage·반응면적·B3 가 그것을 읽으므로 **S2 는 표면 지표 쪽에서만** 효과가 있다
   (그리고 `AREA-03` 대로 그쪽은 **동결**해야 하므로, S2 는 결국 **아무 데도 안 남는다**).
⚠ **답하지 않는 것**: ψ 배치(`S3`) · flux-tube `b` · 이종쌍 σ 분할 — 전부 별개 축이다.

사용:
  python3 scripts/audit_transport_cap_equivalence.py            # 무작위 스윕
  python3 scripts/audit_transport_cap_equivalence.py --selftest
"""
from __future__ import annotations
import argparse
import math
import pathlib
import sys
import types

import numpy as np

SCRIPTS = pathlib.Path(__file__).resolve().parent
PC_SRC = SCRIPTS / 'plastic_coverage.py'

CAP_LINE = 'A_geom = 2.0 * np.pi * (r_min_eff ** 2)'
CAP_LINE_S2 = 'A_geom = 1.0 * np.pi * (r_min_eff ** 2)'


def _load(name: str, subs=()):
    """`plastic_coverage.py` 를 **격리 메모리에서** 로드한다 (필요하면 소스 치환).

    ⚠ 디스크의 생산 파일은 건드리지 않는다.
    """
    src = PC_SRC.read_text(encoding='utf-8')
    for old, new in subs:
        if src.count(old) != 1:
            raise SystemExit(f'치환 대상이 유일하지 않다 ({src.count(old)}건): {old!r}')
        src = src.replace(old, new, 1)
    mod = types.ModuleType(name)
    mod.__file__ = str(PC_SRC)
    exec(compile(src, str(PC_SRC), 'exec'), mod.__dict__)
    return mod


def a_eff_from(mod, delta, R_star, R_min, ligg_area):
    """생산 사슬 그대로: `A_physics` → `a = √(A/π)` → `a_eff = min(a, R_min)`.

    (`network_conductivity.py:323` · `:386` · `:395`)
    """
    A, _regime, _comp = mod.film_area_from_overlap(
        delta, R_star, R_min=R_min, ligg_area=ligg_area,
        mode='physics', return_components=True)
    a = math.sqrt(A / math.pi) if A > 0 else 0.0
    return A, min(a, R_min)


def sample(n, seed=0):
    """무작위 접촉 (µm 단위 아님 — `film_area_from_overlap` 은 단위 무관 스케일)."""
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(n):
        r1 = float(10.0 ** rng.uniform(-0.6, 0.9))      # 0.25 ~ 8
        r2 = float(10.0 ** rng.uniform(-0.6, 0.9))
        R_star = r1 * r2 / (r1 + r2)
        R_min = min(r1, r2)
        # δ/R* 를 탄성·전이·소성 전 구간에 걸쳐 뿌린다 (0 과 음수도 넣는다)
        dr = float(10.0 ** rng.uniform(-4.0, 0.3))
        delta = dr * R_star
        # LIGGGHTS 면적: 없음 / 0 / 교차 원판 근처 / 과대
        pick = rng.integers(0, 4)
        if pick == 0:
            ligg = None
        elif pick == 1:
            ligg = 0.0
        elif pick == 2:
            ligg = float(math.pi * max(delta, 0.0) * (2 * R_min - max(delta, 0.0)) / 2.0)
        else:
            ligg = float(rng.uniform(0.5, 4.0) * math.pi * R_min ** 2)
        out.append((delta, R_star, R_min, ligg))
    return out


def run(n, seed, verbose=True):
    """스윕 1회 → `classify` 결과.  ⚠ **selftest 와 같은 판정기를 쓴다** — 두 경로가
    서로 다른 문턱을 쓰면 한쪽이 거짓 빨간불/초록을 낸다 (규율 ⑤)."""
    st = classify(n, seed)
    if verbose:
        print(f'접촉 {n}건 (seed {seed})')
        print(f'  A_physics 가 **바뀐** 접촉   : {st["n_A_diff"]} / {n} '
              f'({100.0 * st["n_A_diff"] / n:.2f} % · 최대 상대차 {st["dA_max"]:.6g})')
        print(f'  a_eff 비트 동일              : {st["n_same"]} / {n}')
        print(f'  a_eff 가 clamp 에서 ULP 차   : {st["n_ulp"]} (최대 {st["max_ulp"]:.3g} ULP)')
        print(f'  **설명 안 되는 a_eff 차이**  : {st["n_bad"]}')
        print(f'  ψ 분기가 갈린 접촉           : {st["n_psi_branch_diff"]}')
        if st['worst']:
            (d, Rs, Rm, lg), A0, A1, a0, a1 = st['worst']
            print(f'    최대 차 사례: δ={d:.6g} R*={Rs:.6g} R_min={Rm:.6g} ligg={lg}')
            print(f'          A {A0:.12g} → {A1:.12g} · a_eff {a0:.17g} → {a1:.17g}')
    return st


NC_SRC = SCRIPTS / 'network_conductivity.py'
PC_ONLY_ANCHOR = "from plastic_coverage import film_area_from_overlap"


def _load_nc(name: str, pc_mod, nc_subs=()):
    """`network_conductivity.py` 를 격리 로드하되 그 안의 `_film_area` 를 **주어진 plastic 모듈**의
    함수로 바꿔 끼운다 → cap 을 바꾼 plastic 판을 실제 솔버에 물릴 수 있다.  (P2-R2-06: 감사가
    clamp/ψ 를 다시 구현하면 솔버 호출부의 변이를 못 본다 — 그래서 **솔버 자신**을 부른다.)"""
    src = NC_SRC.read_text(encoding='utf-8')
    for old_, new_ in nc_subs:
        if src.count(old_) != 1:
            raise SystemExit(f'솔버 치환 대상이 유일하지 않다 ({src.count(old_)}건): {old_!r}')
        src = src.replace(old_, new_, 1)
    mod = types.ModuleType(name)
    mod.__file__ = str(NC_SRC)
    sys.path.insert(0, str(SCRIPTS))
    exec(compile(src, str(NC_SRC), 'exec'), mod.__dict__)
    mod._film_area = pc_mod.film_area_from_overlap          # 솔버가 쓰는 이름
    return mod


def real_solver_edges(nc_mod, r1_um=0.5, r2_um=6.0, delta_um=0.2, native_um2=0.04, scale=1000.0):
    """실제 `build_network` 한 쌍 — Codex 대조 조건 (r .5/6 µm · δ .2 µm · native A .04 µm²)."""
    atoms = {1: {'type': 1, 'radius': r1_um / scale, 'x': 0.0, 'y': 0.0, 'z': 0.0},
             2: {'type': 3, 'radius': r2_um / scale, 'x': (r1_um + r2_um - delta_um) / scale, 'y': 0.0, 'z': 0.0}}
    rows = [{'id1': 1, 'id2': 2, 'contact_area': native_um2 / scale ** 2, 'delta': delta_um / scale}]
    tm = {1: 'AM_P', 3: 'SE'}
    n = nc_mod.build_network(atoms, rows, {1, 3}, scale, 10.0, box_x=1e3, box_y=1e3,
                             mode='thermal', type_map=tm, contact_mode='physics')
    return n['edges'] if isinstance(n, dict) else n[1]


def _psi(a_eff, r_min):
    """`network_conductivity.py:396` 과 같은 식."""
    return max(1.0 - a_eff / r_min, 0.0) ** 1.5


def classify(n, seed):
    """`a_eff` 차이를 **비트 동일 / clamp ULP / 설명 안 됨** 으로 가른다.

    ⚠ 느슨한 허용오차 대신 이렇게 가르는 이유: 허용오차는 **무엇이 달랐는지**를 숨긴다.
    """
    base = _load('_pc_c_base')
    s2 = _load('_pc_c_s2', [(CAP_LINE, CAP_LINE_S2)])
    st = dict(n_same=0, n_ulp=0, n_bad=0, max_ulp=0.0, n_A_diff=0,
              dA_max=0.0, da_max=0.0, n_psi_branch_diff=0, worst=None)
    for c in sample(n, seed):
        _delta, _Rs, R_min, _lg = c
        A0, a0 = a_eff_from(base, *c)
        A1, a1 = a_eff_from(s2, *c)
        dA = abs(A1 - A0) / max(A0, 1e-300)
        if dA > 1e-15:
            st['n_A_diff'] += 1
        st['dA_max'] = max(st['dA_max'], dA)
        da = abs(a1 - a0) / max(a0, 1e-300)
        if da > st['da_max']:
            st['da_max'], st['worst'] = da, (c, A0, A1, a0, a1)
        if a0 == a1:
            st['n_same'] += 1
        else:
            u = max(abs(a0 - R_min), abs(a1 - R_min)) / math.ulp(R_min)
            st['max_ulp'] = max(st['max_ulp'], u)
            if u <= 2.0:
                st['n_ulp'] += 1
            else:
                st['n_bad'] += 1
        # ψ 분기 (≤ 1e-4 이면 R_c = 0) 가 갈리는가
        if (_psi(a0, R_min) > 1e-4) != (_psi(a1, R_min) > 1e-4):
            st['n_psi_branch_diff'] += 1
    return st


def _selftest() -> int:
    ok = True

    def chk(name, cond, extra=''):
        nonlocal ok
        print(('  ✓ ' if cond else '  ✗ ') + name + (f'   {extra}' if extra else ''))
        ok = ok and bool(cond)

    print('수송 cap 동치 (S2 전제 검사)')

    # ① 본 주장 — a_eff 는 안 바뀐다.
    #    ⚠ **비트 동일을 요구하지 않는다** — `√(πR²/π)` 가 `R` 과 1 ULP 어긋날 수 있다.
    #      느슨한 허용오차로 초록을 만드는 대신 **더 구체적인 주장**을 검사한다:
    #      다른 건은 전부 **양쪽 다 clamp 값(R_min) 에서 2 ULP 이내** 여야 한다.
    st = classify(4000, 0)
    chk('① S2 전환에서 `a_eff` 가 바뀌지 않는다 (비트 동일 · 또는 양쪽 다 clamp 2 ULP 이내)',
        st['n_bad'] == 0,
        f'비트 동일 {st["n_same"]} · clamp ULP 차 {st["n_ulp"]} (최대 {st["max_ulp"]:.3g} ULP) · '
        f'설명 안 되는 차이 {st["n_bad"]}')

    # ①b 그 1 ULP 가 **하류에서 같은 분기로 간다** (ψ ≤ 1e-4 → R_c = 0)
    chk('①b 그 ULP 차는 ψ 분기를 안 바꾼다 (둘 다 ψ ≤ 1e-4)', st['n_psi_branch_diff'] == 0,
        f'분기가 갈린 접촉 {st["n_psi_branch_diff"]}건')
    dA, da, nA = st['dA_max'], st['da_max'], st['n_A_diff']

    # ② 검사가 공허하지 않다 — A 자체는 실제로 바뀌어야 한다
    chk('② 대조: `A_physics` 자체는 바뀐다 (검사가 공허하지 않다)', nA > 0 and dA > 0.1,
        f'{nA}건 · 최대 {dA:.4g}')

    # ③ 판별력 — clamp 를 없애면 `a_eff` 가 **반드시** 달라진다
    base = _load('_pc_b3')
    s2 = _load('_pc_s3', [(CAP_LINE, CAP_LINE_S2)])
    diff = 0
    for c in sample(4000, 0):
        A0, _ = a_eff_from(base, *c)
        A1, _ = a_eff_from(s2, *c)
        # clamp 없는 세계: a = √(A/π) 그대로
        if abs(math.sqrt(A1 / math.pi) - math.sqrt(A0 / math.pi)) > 1e-15 * max(
                math.sqrt(A0 / math.pi), 1e-300):
            diff += 1
    chk('③ 판별력: clamp 를 빼면 `a` 가 달라진다 (동치는 clamp 덕분이다)', diff > 0,
        f'{diff}/4000 건이 달라진다')

    # ④ 다른 seed 에서도 같다
    st2 = classify(4000, 12345)
    chk('④ 다른 seed 에서도 같은 결론', st2['n_bad'] == 0 and st2['n_psi_branch_diff'] == 0,
        f'비트 동일 {st2["n_same"]} · clamp ULP {st2["n_ulp"]} · 설명 안 됨 {st2["n_bad"]}')

    # ⑤ 손으로 짚은 경계 — geom 결속이 되는 깊은 겹침
    r = 1.0
    c = (0.5 * r, r / 2.0, r, None)          # δ/R* = 1.0, 깊게
    A0, a0 = a_eff_from(base, *c)
    A1, a1 = a_eff_from(s2, *c)
    chk('⑤ geom 결속 경계: A 는 2πR²→πR² 로 절반, `a_eff` 는 R 로 동일',
        abs(A0 - 2 * math.pi * r * r) < 1e-12 and abs(A1 - math.pi * r * r) < 1e-12
        and a0 == a1 == r,
        f'A {A0:.10g} → {A1:.10g} · a_eff {a0:.10g} = {a1:.10g}')

    # ⑥ ★ P2-R2-06 — **실제 솔버**로 대조한다 (감사의 ψ 재구현이 아니라 build_network 자신).
    #    cap 2π→π 를 plastic 에 물린 솔버와 원판 솔버가 같은 Rc·R_total 을 내야 한다.
    pc_base = _load('_pc_s6b'); pc_s2 = _load('_pc_s6s', [(CAP_LINE, CAP_LINE_S2)])
    e0 = real_solver_edges(_load_nc('_nc_base', pc_base))[0]
    e1 = real_solver_edges(_load_nc('_nc_s2', pc_s2))[0]
    chk('⑥ 실제 build_network: cap 전환 전후 Rc·R_total 동일 (Codex 대조 조건 r .5/6 · δ .2 · A .04)',
        e0['R_constriction'] == e1['R_constriction'] and e0['R_total'] == e1['R_total'],
        f"Rc {e0['R_constriction']!r} → {e1['R_constriction']!r} · R_total {e0['R_total']!r} → {e1['R_total']!r}")
    chk('⑥b 그러나 진단 필드는 변한다 — A_physics 절반 · R_Maxwell 은 √2배 (σ 불변 ≠ 전 출력 불변)',
        abs(e1['A_physics'] / e0['A_physics'] - 0.5) < 1e-12
        and abs(e1['R_Maxwell'] / e0['R_Maxwell'] - math.sqrt(2.0)) < 1e-12,
        f"A {e0['A_physics']!r} → {e1['A_physics']!r} · R_Maxwell {e0['R_Maxwell']!r} → {e1['R_Maxwell']!r}")
    # ⑥c 판별력 — 솔버 호출부(Rc=0 분기)를 변이시키면 **이 대조가** 반드시 빨간불이 된다.
    #     Codex: 옛 감사는 이 변이에도 n_bad=0 이었다 (감사가 ψ 를 다시 구현했으므로).
    mut = [('                R_constriction = 0.0\n', '                R_constriction = R_Maxwell\n')]
    m0 = real_solver_edges(_load_nc('_nc_mb', pc_base, mut))[0]
    m1 = real_solver_edges(_load_nc('_nc_ms', pc_s2, mut))[0]
    chk('⑥c 판별력: 솔버의 Rc=0 분기를 R_Maxwell 로 바꾸면 cap 전환이 **실제로** 값을 움직인다 '
        '(Codex: Rc 0.7071 → 1.0)',
        m0['R_constriction'] != m1['R_constriction'],
        f"변이판 Rc {m0['R_constriction']!r} → {m1['R_constriction']!r}")

    print('수송 cap 동치 SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description='S2 면적 cap 전환의 솔버 영향 (AREA-12)')
    ap.add_argument('-n', type=int, default=20000)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    st = run(a.n, a.seed)
    print()
    if st['n_bad'] == 0 and st['n_psi_branch_diff'] == 0:
        print('⇒ **S2 는 솔버 `a_eff` 에 대해 항등 변환이다** (clamp 가 이미 하고 있다).')
        print(f'   차이가 난 {st["n_ulp"]} 건은 전부 `√(πR²/π) ≠ R` 의 **1 ULP 반올림**이고')
        print('   ψ 분기(≤ 1e-4 → R_c = 0)를 넘지 않는다.')
        print('⚠ `A_physics` 자체는 바뀐다 ⇒ coverage·반응면적·B3 쪽에서만 효과가 있고,')
        print('  `AREA-03` 대로 그쪽을 동결하면 **아무 데도 안 남는다**.')
        return 0
    print(f'⇒ ⚠ `a_eff` 가 실제로 움직인다 (설명 안 되는 차이 {st["n_bad"]} · '
          f'ψ 분기 차 {st["n_psi_branch_diff"]}) — 위 산술 주장을 재검토할 것.')
    return 1


if __name__ == '__main__':
    sys.exit(main())
