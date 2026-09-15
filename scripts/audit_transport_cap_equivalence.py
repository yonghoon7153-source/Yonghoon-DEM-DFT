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
import subprocess
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


def real_solver_edges(nc_mod, r1_um=0.5, r2_um=6.0, delta_um=0.2, native_um2=0.04, scale=1000.0,
                      psi_placement=None):
    """실제 `build_network` 한 쌍 — Codex 대조 조건 (r .5/6 µm · δ .2 µm · native A .04 µm²).

    `psi_placement=None` 이면 솔버의 **기본값**을 쓴다 (인자를 아예 넘기지 않는다 — 옛 판
    소스로도 이 함수가 돌아야 하므로).
    """
    atoms = {1: {'type': 1, 'radius': r1_um / scale, 'x': 0.0, 'y': 0.0, 'z': 0.0},
             2: {'type': 3, 'radius': r2_um / scale, 'x': (r1_um + r2_um - delta_um) / scale, 'y': 0.0, 'z': 0.0}}
    rows = [{'id1': 1, 'id2': 2, 'contact_area': native_um2 / scale ** 2, 'delta': delta_um / scale}]
    tm = {1: 'AM_P', 3: 'SE'}
    kw = {} if psi_placement is None else {'psi_placement': psi_placement}
    n = nc_mod.build_network(atoms, rows, {1, 3}, scale, 10.0, box_x=1e3, box_y=1e3,
                             mode='thermal', type_map=tm, contact_mode='physics', **kw)
    return n['edges'] if isinstance(n, dict) else n[1]


def _psi(a_eff, r_min):
    """`network_conductivity.py:396` 과 같은 식."""
    return max(1.0 - a_eff / r_min, 0.0) ** 1.5


# ── S3 (`L2-01` ψ 배치) 보조 ────────────────────────────────────────────────────
#   픽스처는 `real_solver_edges` 기본과 같은 쌍이다 (r 0.5 / 6.0 µm · native A 0.04 µm²).
_FX_R1, _FX_R2, _FX_NATIVE = 0.5, 6.0, 0.04


def _a_from_delta(pc_mod, delta_um):
    """그 픽스처에서 `a_contact = √(A_physics/π)` (clamp **전**) — µm."""
    R_star = _FX_R1 * _FX_R2 / (_FX_R1 + _FX_R2)
    A, a_eff = a_eff_from(pc_mod, delta_um, R_star, R_min=min(_FX_R1, _FX_R2),
                          ligg_area=_FX_NATIVE)
    return math.sqrt(A / math.pi) if A > 0 else 0.0


def _bitwise_vs_head(pc_mod):
    """기본값(legacy)이 **git HEAD 의 솔버**와 비트 동일한지 — δ 를 전 구간에 뿌려 대조한다.

    ⚠ 옛 판에는 `psi_placement` 인자가 **없다** ⇒ 현재 판도 인자를 **넘기지 않고** 부른다
      (기본값 경로를 재는 것이 목적이다).
    HEAD 를 못 읽으면(얕은 클론·git 밖) `(0, 0, 0.0)` 을 돌려주고 호출부가 `n_cmp` 문턱으로
    **실패시킨다** — 조용히 초록이 되지 않는다.
    """
    try:
        head_src = subprocess.run(['git', 'show', 'HEAD:scripts/network_conductivity.py'],
                                  cwd=str(SCRIPTS.parent), capture_output=True, text=True,
                                  check=True, timeout=120).stdout
    except Exception:
        return 0, 0, 0.0
    if not head_src.strip():
        return 0, 0, 0.0
    mod = types.ModuleType('_nc_head')
    mod.__file__ = str(NC_SRC)
    sys.path.insert(0, str(SCRIPTS))
    exec(compile(head_src, str(NC_SRC), 'exec'), mod.__dict__)
    mod._film_area = pc_mod.film_area_from_overlap
    cur = _load_nc('_nc_cur_bit', pc_mod)
    #   ⚠ **전부 0 을 비교하면 공허하다** — `n_nonzero_rc` 를 따로 세어 호출부가 요구한다.
    _FIELDS = ('R_constriction', 'R_bulk', 'R_total', 'R_Maxwell', 'R_film',
               'A_contact', 'A_physics', 'A_hertzian', 'd_ij', 'regime')
    n_cmp = n_bad = n_nonzero_rc = 0
    worst = 0.0
    for d in (0.002, 0.005, 0.01, 0.02, 0.05, 0.08, 0.1, 0.1025, 0.12, 0.2, 0.4, 0.8):
        eo = real_solver_edges(mod, delta_um=d)[0]
        en = real_solver_edges(cur, delta_um=d)[0]
        if eo.get('R_constriction'):
            n_nonzero_rc += 1
        for k in _FIELDS:
            if k not in eo and k not in en:
                continue
            va, vb = eo.get(k), en.get(k)
            n_cmp += 1
            if va is None and vb is None:
                continue
            if va != vb:
                n_bad += 1
                try:
                    worst = max(worst, abs(float(va) - float(vb)))
                except (TypeError, ValueError):
                    worst = float('inf')
    return n_cmp, n_bad, worst, n_nonzero_rc


def _psi_sweep(nc_mod):
    """δ 를 키우며 두 배치의 `R_constriction` 을 나란히 — `L2-01` 의 비단조·절벽 재현.

    ⚠ *"접촉을 키운다"* 를 δ 로 대리한다 — 이 픽스처에서 `a_contact` 는 δ 에 단조 증가다
      (`⑦g` 의 전제이므로 같은 함수가 그것도 확인한다).
    """
    ds = [0.002 * (1.06 ** i) for i in range(80)]          # 0.002 → ~0.2
    div, mul, a_prev = [], [], -1.0
    div_last_pos = mul_last_pos = 0.0
    mono_a = True
    for d in ds:
        a = _a_from_delta(_PC_SWEEP[0], d)
        if a < a_prev:
            mono_a = False
        a_prev = a
        ro = real_solver_edges(nc_mod, delta_um=d, psi_placement=nc_mod.PSI_DIVIDE)[0]['R_constriction']
        rn = real_solver_edges(nc_mod, delta_um=d, psi_placement=nc_mod.PSI_MULTIPLY)[0]['R_constriction']
        div.append(ro)
        mul.append(rn)
        if ro > 0:
            div_last_pos = ro
        if rn > 0:
            mul_last_pos = rn
    return dict(div=div, mul=mul, div_last_pos=div_last_pos, mul_last_pos=mul_last_pos,
                a_monotone=mono_a)


#: `_psi_sweep` 이 쓰는 plastic 모듈 (호출부가 채운다 — 감사가 면적을 재구현하지 않게).
_PC_SWEEP = [None]

#: oracle 이 못박는 두 상수.  ⛔ 계약 §C·§⑥ 이 **동결**한 값이다 — 여기를 바꿔서 초록을
#: 만들면 그 순간 이 검사가 무의미해진다 (`R4-08` 이 정확히 그 부류를 보고했다).
PSI_EXPONENT_ORACLE = 1.5
PSI_FLOOR_ORACLE = 1e-4


def _psi_oracle(nc_mod, pc_mod):
    """★★ `R4-08` — ψ 를 **기하에서 독립 계산**해 두 배치의 식을 각각 못박는다.

    `R_Maxwell = 1/(σ·k·2·a_contact)` 는 솔버가 이미 돌려주므로 재료·채널 계수를 다시
    구현할 필요가 없다.  활성 간선에서는 clamp 가 안 걸려 `a_eff == a_contact` 이므로
        legacy : `Rc·ψ_oracle == R_Maxwell`
        곱셈   : `Rc == R_Maxwell·ψ_oracle`
    이고, 이 두 식은 **ψ 의 지수와 floor 를 같이 못박는다** — 솔버의 ψ 를 빌리지 않기 때문이다.
    """
    r_min = min(_FX_R1, _FX_R2)
    n = bad_div = bad_mul = bad_floor = 0
    for d in (0.002, 0.005, 0.01, 0.02, 0.04, 0.06, 0.08, 0.1, 0.1025, 0.12, 0.2):
        a = _a_from_delta(pc_mod, d)
        a_eff = min(a, r_min)
        s = a_eff / r_min
        psi_o = max(1.0 - s, 0.0) ** PSI_EXPONENT_ORACLE
        eo = real_solver_edges(nc_mod, delta_um=d, psi_placement=nc_mod.PSI_DIVIDE)[0]
        en = real_solver_edges(nc_mod, delta_um=d, psi_placement=nc_mod.PSI_MULTIPLY)[0]
        rm = eo.get('R_Maxwell')
        ro, rn = eo.get('R_constriction') or 0.0, en.get('R_constriction') or 0.0
        active = psi_o > PSI_FLOOR_ORACLE
        #  ⓐ floor 판정 자체 — oracle 이 "활성" 이라 한 곳에서만 솔버가 양수를 내야 한다.
        if active != (ro > 0.0) or active != (rn > 0.0):
            bad_floor += 1
            continue
        if not active:
            continue
        n += 1
        #  ⓑ 두 식.  `a_eff == a_contact` 를 쓰므로 clamp 가 걸린 간선은 활성이 아니다.
        if rm is None or rm <= 0 or abs(ro * psi_o - rm) > 1e-12 * max(1.0, rm):
            bad_div += 1
        if rm is None or rm <= 0 or abs(rn - rm * psi_o) > 1e-12 * max(1.0, rm * psi_o):
            bad_mul += 1
    return dict(n=n, bad_div=bad_div, bad_mul=bad_mul, bad_floor=bad_floor,
                exponent=PSI_EXPONENT_ORACLE, floor=PSI_FLOOR_ORACLE)


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

    # ══ S3 대조 (R3-02, Codex 3라운드 §3.1 · 계약 §5-v4 C) ══════════════════════════
    #   등록된 음성 대조 둘(coverage 셀 불변 · hertzian Rc bitwise 불변)은 **no-op 도 통과**한다.
    #   통과 자체가 결함은 아니지만 **전환을 안 해도 통과**하므로 전환을 잡지 못한다.
    #   ⇒ 실제 build_network 의 활성 간선에서 Rc_new/Rc_old = ψ² 를 요구하는 **양성 대조**를
    #     두고, **no-op 변이는 반드시 실패**하게 한다.  ⛔ "전 코호트 σ 가 반드시 달라야 한다"
    #     는 게이트는 만들지 않는다 (활성 간선이 없는 망에서는 무변화가 정상이다).
    #   ★★ **2026-09-15 — 전환이 소스 문자열 치환에서 `psi_placement` 깃발로 옮겨졌다.**
    #      왜: 치환판으로는 **실제 런을 돌릴 수 없다** (감사 프로세스 안에서만 존재한다).
    #      S3 는 코호트 130 × 3 채널을 두 팔로 돌려야 하므로 생산 솔버에 인자가 있어야 한다.
    #      ⛔ 기본값은 `legacy_divide` 로 **비트 동일**이다 (아래 ⑦f 가 고정한다).
    S3_MUL = ('                    R_constriction = psi / '
              '(sigma_rel_contact * k_weight * 2 * a_eff)')
    S3_DIV = ('                    R_constriction = 1.0 / '
              '(sigma_rel_contact * k_weight * 2 * a_eff * psi)')
    #   ⚠ 기본 픽스처(δ .2 µm)는 **floor 아래**라 Rc = 0 이다 — 양성 대조는 활성 분기가
    #     필요하므로 겹침을 줄여 ψ > 1e-4 인 쌍을 쓴다 (δ .02 µm, 실측으로 고른 값).
    _pc = _load('_pc_s3')
    _PC_SWEEP[0] = _pc          # 스윕이 면적을 재구현하지 않고 이 모듈을 쓴다
    #   세 좌표: 활성(ψ>1e-4) · floor_only(s<1 인데 ψ≤1e-4) · clamp_zero(s_raw≥1 ⇒ ψ=0).
    #   ⚠ floor_only 띠는 **0.102338~0.102633 뿐**이다 (R2-08 실측) — 이 값을 넓히지 말 것.
    _D_ACT, _D_FLOOR_ONLY, _D_CLAMP = 0.02, 0.1025, 0.2
    _nc = _load_nc('_nc_s3_flag', _pc)
    e_old = real_solver_edges(_nc, delta_um=_D_ACT, psi_placement=_nc.PSI_DIVIDE)[0]
    e_s3 = real_solver_edges(_nc, delta_um=_D_ACT, psi_placement=_nc.PSI_MULTIPLY)[0]
    #   no-op 변이 = 곱셈 가지를 **legacy 식으로 되돌린다** ⇒ 깃발을 켜도 아무 일이 없다.
    #   음성 대조(coverage 셀 · hertzian bitwise)는 이것을 **통과시킨다** — 그래서 이 대조가 있다.
    _nc_nop = _load_nc('_nc_s3_nop', _pc, [(S3_MUL, S3_DIV)])
    e_nop = real_solver_edges(_nc_nop, delta_um=_D_ACT, psi_placement=_nc_nop.PSI_MULTIPLY)[0]
    #   ⚠ ψ 를 감사가 **다시 구현하면 안 된다** (이 파일 §_load_nc 의 교훈).  그렇다고 비의
    #     제곱근으로 읽으면 `ratio == sqrt(ratio)²` 라는 **항등식**이 되어 판별력이 0 이다.
    #     ⇒ 세 번째 변이로 **솔버가 ψ 를 직접 돌려주게** 해서 그 값과 비교한다.
    S3_PSI = '                    R_constriction = psi'
    _nc_psi = _load_nc('_nc_s3_psi', _pc, [(S3_MUL, S3_PSI)])
    psi_probe = real_solver_edges(_nc_psi, delta_um=_D_ACT,
                                 psi_placement=_nc_psi.PSI_MULTIPLY)[0]['R_constriction']
    ratio = e_s3['R_constriction'] / e_old['R_constriction']
    chk('⑦ ★ S3 양성 대조: 실제 build_network 에서 Rc_new/Rc_old = ψ² (ψ 는 솔버가 돌려준 값)',
        e_old['R_constriction'] > 0 and 0.0 < psi_probe < 1.0
        and abs(ratio - psi_probe ** 2) < 1e-12,
        f'비 = {ratio!r} · ψ(솔버) = {psi_probe!r} · ψ² = {psi_probe ** 2!r}')
    nop_ratio = e_nop['R_constriction'] / e_old['R_constriction']
    chk('⑦b ★ no-op 변이는 이 대조에서 **반드시 실패**한다 (음성 대조만으로는 못 잡던 자리)',
        nop_ratio == 1.0 and abs(nop_ratio - psi_probe ** 2) > 1e-6,
        f'no-op 비 = {nop_ratio!r} ≠ ψ² {psi_probe ** 2!r}')
    chk('⑦c σ 는 비감소 — 활성 분기에서 Rc_new ≤ Rc_old 이므로 R_total 이 안 늘어난다',
        e_s3['R_total'] <= e_old['R_total'],
        f"R_total {e_old['R_total']!r} → {e_s3['R_total']!r}")
    #   floor 아래(ψ ≤ 1e-4)는 **0 → 0** 이다 — floor 복원은 이 시험이 아니다 (R3-02).
    _fo_old = real_solver_edges(_nc, delta_um=_D_FLOOR_ONLY, psi_placement=_nc.PSI_DIVIDE)[0]
    _fo_s3 = real_solver_edges(_nc, delta_um=_D_FLOOR_ONLY, psi_placement=_nc.PSI_MULTIPLY)[0]
    chk('⑦d floor 아래(floor_only, s<1)는 전환해도 0 → 0 (복원은 별도 축)',
        _fo_old['R_constriction'] == 0.0 and _fo_s3['R_constriction'] == 0.0,
        f"{_fo_old['R_constriction']!r} / {_fo_s3['R_constriction']!r}")
    #   ★★ 계약 §C 가 등록한 **세 번째 핀 = clamp 경계** (2026-09-15 에 추가).  등록은
    #      *"floor 위·아래·clamp 경계를 각각 핀한다"* 인데 위 둘만 있었다.
    #      clamp 경계 = `a_contact ≥ r_min` ⇒ `a_eff = r_min` **정확히** ⇒ `ψ = 0`.
    #      ⇒ **양쪽 배치 모두 0** 이고 S3 는 여기서 항등이다.
    #      ★ 이것이 크기를 말한다 — 삭제 973,137 중 **99.436 %가 clamp_zero** (R2-08) 이므로
    #        S3 는 "협착이 삭제된 접촉" 의 거의 전부를 **건드리지 않는다**.  그 접촉들의 참값은
    #        `A` 의 정의(`AREA-03`/`AREA-09` STEP 2)가 정해져야 나온다.
    _cz_old = real_solver_edges(_nc, delta_um=_D_CLAMP, psi_placement=_nc.PSI_DIVIDE)[0]
    _cz_s3 = real_solver_edges(_nc, delta_um=_D_CLAMP, psi_placement=_nc.PSI_MULTIPLY)[0]
    _a_eff_cz = min(_a_from_delta(_pc, _D_CLAMP), 0.5)
    chk('⑦e ★ clamp 경계(clamp_zero, s_raw≥1 ⇒ ψ=0): 양쪽 다 0 — S3 는 삭제분의 99.436 % 를 안 건드린다',
        _cz_old['R_constriction'] == 0.0 and _cz_s3['R_constriction'] == 0.0
        and _a_eff_cz == 0.5,
        f"Rc {_cz_old['R_constriction']!r} / {_cz_s3['R_constriction']!r} · a_eff = r_min = {_a_eff_cz!r}")
    #   ★ ⑦f — **기본값이 옛 코드와 비트 동일**하다.  깃발을 넣은 것이 세대 1 의 σ 를
    #     조용히 움직였다면 봉인 전에 이미 오염된 것이다.  옛 판을 git 에서 불러 대조한다.
    _n_cmp, _n_bad_bit, _worst_bit, _n_nz = _bitwise_vs_head(_pc)
    chk('⑦f ★ 기본값(legacy_divide)은 변경 전 코드와 비트 동일 — 깃발 도입이 세대 1 을 안 움직였다',
        _n_bad_bit == 0 and _n_cmp >= 100 and _n_nz >= 5,
        f'대조한 (δ, 필드) {_n_cmp} · 그 중 Rc>0 인 δ {_n_nz} · 다른 것 {_n_bad_bit} '
        f'· 최대차 {_worst_bit!r}')
    #   ★ ⑦g — `L2-01` 이 보고한 **비단조·절벽**을 생산 코드에서 재현하고, 곱셈 배치가
    #     둘 다 없앤다는 것을 같은 스윕에서 보인다 (규율 ②: 재현 먼저, 그 다음 수리).
    _sw = _psi_sweep(_nc)
    _legacy_nonmono = any(_sw['div'][i + 1] > _sw['div'][i] > 0 for i in range(len(_sw['div']) - 1))
    _mul_mono = all(_sw['mul'][i + 1] <= _sw['mul'][i] for i in range(len(_sw['mul']) - 1))
    chk('⑦g ★ 재현: legacy 는 접촉을 키우는데 저항이 **오르는** 구간이 있고(비단조) 곱셈은 단조 비증가',
        _legacy_nonmono and _mul_mono and _sw['a_monotone'],
        f"legacy 최대 {max(_sw['div'])!r} (비단조 {_legacy_nonmono}) · 곱셈 단조 {_mul_mono} "
        f"· 전제 a(δ) 단조 {_sw['a_monotone']}")
    chk('⑦h ★ 절벽: legacy 는 floor 직전에 큰 양수에서 0 으로 떨어지고, 곱셈은 그 자리가 연속이다',
        _sw['div_last_pos'] > 1e2 * _sw['mul_last_pos'] and _sw['mul_last_pos'] > 0.0,
        f"floor 직전 Rc — legacy {_sw['div_last_pos']!r} vs 곱셈 {_sw['mul_last_pos']!r}")
    #   ★★ ⑦i — **독립 oracle** (`R4-08` 이 요구한 것).  위 ⑦ 은 ψ 를 **솔버에서 받아**
    #      기대식에도 쓰므로, ψ 가 잘못 바뀌면 기대값이 **같이 움직여** 통과한다 — 실제로
    #      `floor 1e-4 → 0` 과 `ψ 지수 1.5 → 1.0` 두 변이가 13/13 초록이었다.
    #      ⇒ 고정 기하에서 s 와 ψ 를 **독립 계산**해 두 배치의 식을 각각 못박는다.
    #      ⚠ 면적은 재구현하지 않는다 (생산 `plastic_coverage` 에서 받는다) — ψ 만 oracle 이다.
    _or = _psi_oracle(_nc, _pc)
    chk('⑦i ★★ 독립 oracle: ψ 를 기하에서 따로 계산해 legacy = R_M/ψ · 곱셈 = R_M·ψ 를 각각 못박는다',
        _or['n'] >= 3 and _or['bad_div'] == 0 and _or['bad_mul'] == 0 and _or['bad_floor'] == 0,
        f"활성 {_or['n']}건 · legacy 어긋남 {_or['bad_div']} · 곱셈 어긋남 {_or['bad_mul']} "
        f"· floor 판정 어긋남 {_or['bad_floor']} (ψ 지수 {_or['exponent']} · floor {_or['floor']})")

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
