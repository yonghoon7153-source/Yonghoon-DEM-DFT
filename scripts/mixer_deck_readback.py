#!/usr/bin/env python3
"""믹서 **실행 덱 되읽기** — 내보낸 `in.mixer` 텍스트만 읽어 강성 축 (표 E) 과 LC↔LH 공동 개입 (표 B) 을 독립 검산한다 (2026-09-30).

왜
  Codex 9 차 §3 (표 B · 표 E 형식) · §6-2 · 7 차 §5 · 6 차 HBR6-02.  생성기 함수의 기대값 표는 **출력 과정 · 옵션 배선 · 타입 순서**가
  틀렸는지까지 확인하지 못한다 — *"문서의 올바른 공식 ≠ 출력 덱의 올바른 값 ≠ 실제 실행물과 봉인의 동일성"*.  이 도구는 둘째를 본다:
  **실제로 봉인할 덱**의 타입별 E · ν · 반지름 (템플릿) · CED 를 덱 텍스트에서 되읽고, 쌍별 E* · R* · F₀ 를 **덱 값에서** 다시 계산한다.
  ⛔ 생성기 (`make_mixer_deck.py`) 를 import 하지 않는다 (셀프테스트의 고정물 덱을 만들 때만 쓴다).  등록 상수 (타입 사전 · 템플릿
    시드 · 인쇄 정밀도 · 덤프/체크포인트 규칙 · Codex 7 차 §5 산술) 는 **사본**이다 — 생성기가 바뀌면 여기서 어긋나 드러난다 (fail-closed).

표 (`--table KIND OLD NEW` 여러 번)
  E    같은 팔 · 다른 강성 (soft → ×14 · ×14 → ×28): 9 비영 항 F₀ 비 = 1 · 0 은 정확히 0 · SE 영률만 · 물리 시간 · 덤프/체크포인트 규칙
  E0   E0 팔 · 다른 강성: 위 + 두 덱 모두 **전 점착 0** (정확히)
  DT   같은 강성 · dt 만 1/k: E · ν · CED 정확히 같다 · dt 정확히 1/k (k = 2 등록) · 정착 · 회전 · 덤프 step 정확히 k 배 · 계획 t₀ 시각 같다
  B    같은 강성 · LC ↔ LH (OLD = LC · NEW = LH): 다섯 쌍 (AM–AM 셋 · AM–벽 둘) 만 증가 · 나머지 전부 **정확히** 같다 · 0 기준 비 N/A
  공통: 파싱 (필수 명령 · run 구조 [1, F, F, N]) · 타입 사전 (밀도 · 반지름 비 · 템플릿 시드 · 메시 타입) = 등록 · 대칭 · 벽–벽 0 ·
        dt = Rayleigh 규칙을 **이 덱의** E · ν · 반지름 · 밀도로 다시 낸 값 (E · E0 · DT 옛 덱: 그대로 · B: 정확히 1/k) ·
        허용 밖 명령은 토큰까지 같다 (주석은 **메타**로 따로 센다 — 판정 밖)

허용오차 — 인쇄 형식에서 **비교 전에** 정한다 (결과를 보고 넓히지 않는다 · `TOL`)
  CED `%g` = 6 유효숫자 → 한 값 ≤ 5e-6 · 두 값 배수 ≤ 1e-5 · F₀ ∝ CED³ → 비 ≤ 3e-5
  E · ν 는 **덱 값이 곧 시뮬레이션 값**이라 오차로 치지 않는다 (생성기가 4 유효숫자 밖 경화 배수를 거부 — ST⑧)
  dt `.4g` → 5e-4 (생성기는 반올림 **전** dt 로 step 을 센다) ⇒ 표 E 의 물리 시간 대조 = 2 × 5e-4 × T + 반올림 step
    ⚠ 한계: 그보다 작은 step 변조는 표 E 가 못 잡는다 — `mixer_deck_diff.py --allow E --expect-deck` (재생성 덱 · 전 명령 토큰 동일) 의 몫
  DT 는 정확 (인쇄된 ref dt 의 1/k · 정수배 step) — 1e-12

usage
  python3 scripts/mixer_deck_readback.py --table E  <LC_soft/in.mixer> <LC_ref/in.mixer> \\
                                         --table B  <LC_ref/in.mixer>  <LH_ref/in.mixer> --json out.json --md out.md
  python3 scripts/mixer_deck_readback.py --selftest
"""
import argparse
import collections
import hashlib
import json
import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = 'scripts/mixer_deck_readback.py'
TOOL_VERSION = 'mixer_deck_readback/1 (2026-09-30)'
KINDS = ('E', 'E0', 'DT', 'B')

#: ── 등록 상수 (사본 — 생성기를 import 하지 않는다) ─────────────────────────────────────────────────────────────
#: 사전등록 docs/reviews/mixer_highbo_stiffness_prereg_20260929.md §3 · 모체 §2-2 · 생성기 TPL_SEED · D_REAL_UM · E_PHASE · PHASE_MECH
REG_TYPES = {1: 'AM_P', 2: 'AM_S', 3: 'SE', 4: 'WALL'}
REG_TPL_SEED = {10487: 'AM_P', 11887: 'AM_S', 13901: 'SE'}
REG_DENSITY = {'AM': 4800.0, 'SE': 2000.0}
REG_D_UM = {'AM_P': 9.0, 'AM_S': 4.0, 'SE': 1.0}                      # 소재 지름 — 반지름 **비**만 대조한다 (CGF 무관)
REG_E_FIXED = {'AM_P': 1.037e9, 'AM_S': 1.037e9, 'WALL': 1.48e9}      # 강성 축에서 불변이어야 할 영률 (SE 만 경화)
REG_E_SE = {1.0e7: 'soft (×1)', 1.4e8: 'ref (×14)', 2.8e8: 'ref2 (×28)'}
REG_NU = {'AM_P': 0.25, 'AM_S': 0.25, 'SE': 0.30, 'WALL': 0.30}
REG_DT_K = 2                                                          # DEV `E0_ref@dt/2`
PAIRS = (('AM_P', 'AM_P'), ('AM_P', 'AM_S'), ('AM_S', 'AM_S'), ('AM_P', 'SE'), ('AM_S', 'SE'), ('SE', 'SE'),
         ('AM_P', 'WALL'), ('AM_S', 'WALL'), ('SE', 'WALL'), ('WALL', 'WALL'))
B_PAIRS = {('AM_P', 'AM_P'), ('AM_P', 'AM_S'), ('AM_S', 'AM_S'), ('AM_P', 'WALL'), ('AM_S', 'WALL')}
#: Codex 7 차 §5 독립 산술 (E* 배수, 필요한 CED 배수) — soft → ×F.  AM–AM · AM–벽 은 E* 불변 ⇒ (1, 1).
_UNITY = {p: (1.0, 1.0) for p in (('AM_P', 'AM_P'), ('AM_P', 'AM_S'), ('AM_S', 'AM_S'), ('AM_P', 'WALL'), ('AM_S', 'WALL'))}
CODEX = {14.0: {**_UNITY, ('AM_P', 'SE'): (12.412672571, 5.360971926), ('AM_S', 'SE'): (12.412672571, 5.360971926),
                ('SE', 'SE'): (14.0, 5.808785734), ('SE', 'WALL'): (12.876543210, 5.493715853)},
         28.0: {**_UNITY, ('AM_P', 'SE'): (22.123962626, 7.880890212), ('AM_S', 'SE'): (22.123962626, 7.880890212),
                ('SE', 'SE'): (28.0, 9.220872584), ('SE', 'WALL'): (23.704545455, 8.251908834)}}

#: ── 허용오차 — 인쇄 형식에서 비교 **전에** (결과를 보고 넓히지 않는다) ─────────────────────────────────────────
CED_SIG, DT_SIG, RADIUS_SIG = 6, 4, 6
TOL = dict(
    ced_value_rel=0.5 * 10.0 ** (1 - CED_SIG),                # 5e-6  — CED 한 값 (`%g` 6 유효숫자)
    ced_mult_rel=2 * 0.5 * 10.0 ** (1 - CED_SIG),             # 1e-5  — 두 CED 의 배수
    f0_ratio=3 * 2 * 0.5 * 10.0 ** (1 - CED_SIG),             # 3e-5  — F₀ ∝ CED³ 의 비
    radius_ratio_rel=2 * 0.5 * 10.0 ** (1 - RADIUS_SIG),      # 1e-5  — 반지름 비 (`:.6g`)
    rayleigh_rel=0.5 * 10.0 ** (1 - DT_SIG) + 0.5 * 10.0 ** (1 - RADIUS_SIG),   # 5.05e-4 — 덱 dt (.4g) ↔ 덱 값으로 다시 낸 Rayleigh dt
    codex_estar_rel=1e-9,                                     # Codex 산술 (9–10 자리) ↔ 덱 E 로 계산한 E* 배수
    dt_print_rel=0.5 * 10.0 ** (1 - DT_SIG),                  # 5e-4  — dt `.4g` (생성기는 반올림 전 dt 로 step 을 센다)
    exact_rel=1e-12,                                          # DT 표 · 정수배 · 같은 인쇄 토큰
)
TOL_WHY = dict(
    ced_value_rel='CED 는 %g (6 유효숫자) 로 찍힌다 — 한 값의 반올림 상한 0.5×10^(1−6)',
    ced_mult_rel='두 CED 의 배수 = 두 반올림',
    f0_ratio='F₀ ∝ CED³ ⇒ 비의 상한 = 3 × 두 반올림.  E · ν 는 덱 값 = 시뮬레이션 값 (생성기가 인쇄 밖 배수를 거부) 이라 넣지 않는다',
    radius_ratio_rel='템플릿 반지름 :.6g 두 값',
    rayleigh_rel='덱 dt 는 .4g · 다시 낸 규칙 dt 는 반지름 :.6g 에서 — 둘의 인쇄 반올림 (dt 가 규칙과 2 배 넘게 어긋나는 것을 잡는 검사다)',
    codex_estar_rel='Codex 7 차 §5 표는 9–10 자리로 적혀 있다',
    dt_print_rel='timestep 은 .4g — 생성기가 반올림 전 dt 로 step 을 세므로 두 덱의 물리 시간이 이만큼 어긋날 수 있다',
    exact_rel='DT 표 (dt 정확히 1/k · step 정확히 k 배) · 부동소수 비교 여유',
)
DUMP_RULE = 'dump 간격 = max(1000, 회전 step // 200)'
RAYLEIGH_RULE = 'dt = min_t 0.2·π·r_t·√(ρ_t/G_t)/(0.1631ν_t + 0.8766) · G = E/(2(1+ν)) (생성기 plan() 의 식 사본)'
RESTART_RULE = 'restart 간격 = max(50000, min(200000, (회전 step 또는 2·정착 step) // 20))'


def dump_rule(n_run):
    return max(1000, n_run // 200)


def restart_rule(n_fill, n_run):
    return max(50_000, min(200_000, (n_run or 2 * n_fill) // 20))


def rayleigh_dt(D):
    """덱의 E · ν · 템플릿 반지름 · 밀도로 다시 낸 Rayleigh 규칙 dt 와 그것을 정한 상 (생성기 plan() 의 식 **사본**).

    ⚠ 이 검사가 없으면 SE 를 경화하고 dt 를 다시 안 센 덱 (soft dt 0.7055 µs = 경화 SE 한계 0.3132 µs 의 2.25 배 → 적분 불안정) 이
      물리 시간 · 덤프 · 체크포인트 규칙 · 쌍별 CED 를 **전부 통과**한다 (셀프테스트 ⑱ — 2026-09-30 C 설계 중 발견)."""
    best = None
    for k, tpl in sorted(D['templates'].items()):
        E, nu = D['E'][k - 1], D['nu'][k - 1]
        G = E / (2.0 * (1.0 + nu))
        dt = 0.2 * math.pi * tpl['radius'] * math.sqrt(tpl['density'] / G) / (0.1631 * nu + 0.8766)
        if best is None or dt < best[0]:
            best = (dt, D['names'].get(k, str(k)))
    return best


def planned_t0(n_fill, dump_every):
    """계획 t₀ = 정착 끝 직전 덤프 격자점 ⌊2F/D⌋·D (판독기 measure_mixing_index.planned_t0 와 같은 정의 — 사본)."""
    return (2 * n_fill // dump_every) * dump_every


# ══ 파서 (덱 텍스트만) ══════════════════════════════════════════════════════════════════════════════════════════
def _logical(text):
    """덱 → [(첫 줄 번호, 토큰, 주석)].  LIGGGHTS 규칙: 줄의 마지막 인쇄 문자가 `&` 면 다음 줄과 잇는다 · `#` 부터 끝은 주석."""
    lines = text.split('\n')
    out, i = [], 0
    while i < len(lines):
        start, buf = i, [lines[i]]
        while buf[-1].rstrip().endswith('&') and i + 1 < len(lines):
            i += 1
            buf.append(lines[i])
        joined = ' '.join(b.rstrip()[:-1] if b.rstrip().endswith('&') else b for b in buf)
        code, _, com = joined.partition('#')
        out.append((start + 1, code.split(), com.strip()))
        i += 1
    return out


def read_deck(text, label=None, path=None):
    """덱 텍스트 → dict (E · ν · CED (토큰 · 값) · 템플릿 · 메시 타입 · dt · run · 덤프 · 체크포인트 · Drum 주기 · 타입 사전 · 문제)."""
    raw = text.encode('utf-8')
    D = dict(label=label, path=path, sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw), problems=[], type_problems=[],
             n_types=None, E=None, nu=None, ced=None, ced_tok=None, ced_n=None, templates={}, mesh_types=[], dt_txt=None, dt=None,
             runs=[], dump_every=None, restart_every=None, period=None, cmds=[], comments=[], names={})
    seen = collections.Counter()
    for ln, t, com in _logical(text):
        if com:
            D['comments'].append(com)
        if not t:
            continue
        D['cmds'].append((ln, t))
        try:
            key = None
            if t[0] == 'create_box':
                key = 'create_box'
                D['n_types'] = int(t[1])
            elif t[0] == 'timestep':
                key = 'timestep'
                D['dt_txt'], D['dt'] = t[1], float(t[1])
            elif t[0] == 'run':
                D['runs'].append(int(t[1]))
            elif t[0] == 'dump':
                key = 'dump'
                D['dump_every'] = int(t[4])
            elif t[0] == 'restart':
                key = 'restart'
                D['restart_every'] = int(t[1])
            elif t[0] == 'fix' and len(t) >= 4:
                st = t[3]
                if st == 'property/global' and len(t) >= 6:
                    if t[4] in ('youngsModulus', 'poissonsRatio') and t[5] == 'peratomtype':
                        key = t[4]
                        D['E' if key == 'youngsModulus' else 'nu'] = [float(x) for x in t[6:]]
                    elif t[4] == 'cohesionEnergyDensity' and t[5] == 'peratomtypepair':
                        key = 'cohesionEnergyDensity'
                        n = int(t[6])
                        vals = t[7:]
                        if len(vals) != n * n:
                            raise ValueError(f'CED 값 {len(vals)} 개 ≠ {n}×{n}')
                        D['ced_n'] = n
                        D['ced_tok'] = {(i + 1, j + 1): vals[i * n + j] for i in range(n) for j in range(n)}
                        D['ced'] = {k: float(v) for k, v in D['ced_tok'].items()}
                elif st.startswith('particletemplate/'):
                    at = int(t[t.index('atom_type') + 1])
                    if at in D['templates']:
                        raise ValueError(f'atom_type {at} 템플릿이 둘이다')
                    D['templates'][at] = dict(style=st, seed=int(t[4]),
                                              density=float(t[t.index('density') + 2]) if 'density' in t else None,
                                              radius=float(t[t.index('radius') + 2]) if 'radius' in t else None)
                elif st == 'mesh/surface' and 'type' in t:
                    D['mesh_types'].append(int(t[t.index('type') + 1]))
                elif st == 'move/mesh' and len(t) > 5 and t[5] == 'Drum' and 'period' in t:
                    key = 'Drum 주기'
                    D['period'] = float(t[t.index('period') + 1])
            if key:
                seen[key] += 1
        except (ValueError, IndexError) as e:
            D['problems'].append(f'줄 {ln}: `{" ".join(t)[:70]}` — 읽을 수 없다 ({e})')
    for k_, n_ in seen.items():
        if n_ > 1:
            D['problems'].append(f'{k_} 명령이 {n_} 개 — 하나여야 한다')
    for fld, name in (('n_types', 'create_box'), ('E', 'youngsModulus'), ('nu', 'poissonsRatio'), ('ced', 'cohesionEnergyDensity'),
                      ('dt', 'timestep'), ('dump_every', 'dump'), ('restart_every', 'restart'), ('period', 'Drum 회전 주기')):
        if D[fld] is None:
            D['problems'].append(f'{name} 이 없다')
    R = D['runs']
    if not (len(R) == 4 and R[0] == 1 and R[1] == R[2] and R[1] > 0 and R[3] >= 0):
        D['problems'].append(f'run 구조 {R} ≠ [1, F, F, N] (삽입 · 정착 ×2 · 회전)')
    N = D['n_types']
    if N is not None:
        for fld, name in (('E', '영률'), ('nu', 'ν')):
            if D[fld] is not None and len(D[fld]) != N:
                D['problems'].append(f'{name} 값 {len(D[fld])} 개 ≠ create_box {N}')
        if D['ced_n'] is not None and D['ced_n'] != N:
            D['problems'].append(f'CED 행렬 {D["ced_n"]}×{D["ced_n"]} ≠ create_box {N}')
    if not D['problems']:
        D['names'], D['type_problems'] = _type_dict(D)
    return D


def _type_dict(D):
    """타입 번호 → 상 이름 — **밀도 · 반지름 · 메시**로 판정하고 템플릿 시드 (등록 사본) 로 교차 대조한다.  → (이름 사전, 문제)."""
    probs, names = [], {}
    N, tpl = D['n_types'], D['templates']
    walls = sorted(set(D['mesh_types']))
    if walls != [N]:
        probs.append(f'메시 (벽) 타입 {walls} ≠ [create_box {N}] — 벽 = 마지막 타입이어야 한다')
    if N in tpl:
        probs.append(f'벽 타입 {N} 에 입자 템플릿이 있다')
    names[N] = 'WALL'
    if any(v['style'] != 'particletemplate/sphere' for v in tpl.values()):
        probs.append('구가 아닌 템플릿 (섬유 multisphere) — 등록 3 상 밖')
    am = sorted((k for k, v in tpl.items() if v['density'] == REG_DENSITY['AM']), key=lambda k: -(tpl[k]['radius'] or 0.0))
    se = [k for k, v in tpl.items() if v['density'] == REG_DENSITY['SE']]
    if len(am) != 2 or len(se) != 1 or len(tpl) != 3 or sorted(tpl) != list(range(1, N)):
        probs.append(f'입자 템플릿이 등록 3 상 (밀도 4800 둘 · 2000 하나 · 타입 1..{N - 1}) 이 아니다: '
                     f'{ {k: (v["density"], v["radius"]) for k, v in sorted(tpl.items())} }')
        return names, probs
    if tpl[am[0]]['radius'] == tpl[am[1]]['radius']:
        probs.append('AM 두 상의 반지름이 같다 — AM_P / AM_S 를 가를 수 없다')
    names[am[0]], names[am[1]], names[se[0]] = 'AM_P', 'AM_S', 'SE'
    r = {names[k]: tpl[k]['radius'] for k in tpl}
    for a, b in (('AM_P', 'AM_S'), ('SE', 'AM_P')):
        want, got = REG_D_UM[a] / REG_D_UM[b], r[a] / r[b]
        if abs(got / want - 1.0) > TOL['radius_ratio_rel']:
            probs.append(f'반지름 비 {a}/{b} {got:.7g} ≠ 등록 {want:.7g}')
    for k, v in sorted(tpl.items()):
        sn = REG_TPL_SEED.get(v['seed'])
        if sn != names.get(k):
            probs.append(f'타입 {k}: 템플릿 시드 {v["seed"]} (등록 → {sn}) ≠ 밀도 · 반지름 판정 {names.get(k)}')
    if names != REG_TYPES:
        probs.append(f'타입-상 대응 {dict(sorted(names.items()))} ≠ 등록 {REG_TYPES}')
    return dict(sorted(names.items())), probs


# ══ 쌍 물리 (덱 값에서) ══════════════════════════════════════════════════════════════════════════════════════════
def _phases(D):
    """상 이름 → dict(type, E, nu, r) — r 는 템플릿 반지름 (벽 None)."""
    return {ph: dict(type=k, E=D['E'][k - 1], nu=D['nu'][k - 1], r=None if ph == 'WALL' else D['templates'][k]['radius'])
            for k, ph in D['names'].items()}


def estar(a, b):
    """E*_ij = [(1−ν_i²)/E_i + (1−ν_j²)/E_j]⁻¹ (벽 = 덱에 선언된 벽 E · ν)."""
    return 1.0 / ((1.0 - a['nu'] ** 2) / a['E'] + (1.0 - b['nu'] ** 2) / b['E'])


def rstar(a, b):
    """R* — 입자쌍 r_i·r_j/(r_i+r_j) · 벽 (평면) = r_입자."""
    if a['r'] is None:
        a, b = b, a
    if b['r'] is None:
        return a['r']
    return a['r'] * b['r'] / (a['r'] + b['r'])


def f0(ced, rs, es):
    """명목 소겹침 점착 힘 척도 F₀ = B³/A² = (9/2)π³R*²CED³/E*² (N) — A = (4/3)E*√R* · B = 2πR*·CED."""
    return 4.5 * math.pi ** 3 * rs ** 2 * ced ** 3 / es ** 2


# ══ 표 ═══════════════════════════════════════════════════════════════════════════════════════════════════════
def _var_positions(t, kind):
    """이 표 종류에서 **달라도 되는** 토큰 위치 (값은 따로 검사한다).  나머지 토큰은 전부 같아야 한다."""
    steps = kind in ('E', 'E0', 'DT')
    if steps:
        if t[0] in ('timestep', 'run', 'restart'):
            return {1}
        if t[0] == 'dump':
            return {4}
    if t[0] == 'fix' and len(t) > 5 and t[3] == 'property/global':
        if kind in ('E', 'E0') and t[4] == 'youngsModulus':
            return set(range(6, len(t)))
        if kind in ('E', 'E0', 'B') and t[4] == 'cohesionEnergyDensity':
            return set(range(7, len(t)))
    return set()


def _cmd_diff(A, B, kind):
    ca, cb = A['cmds'], B['cmds']
    out = []
    if len(ca) != len(cb):
        out.append(f'명령 수 {len(ca)} ≠ {len(cb)}')
    for (la, ta), (lb, tb) in zip(ca, cb):
        if ta[0] != tb[0] or len(ta) != len(tb):
            out.append(f'줄 {la}/{lb}: `{" ".join(ta)[:80]}` ⇄ `{" ".join(tb)[:80]}`')
            continue
        var = _var_positions(ta, kind)
        if any(x != y for q, (x, y) in enumerate(zip(ta, tb)) if q not in var):
            out.append(f'줄 {la}/{lb}: `{" ".join(ta)[:80]}` ⇄ `{" ".join(tb)[:80]}`')
    return out


def _final(T):
    head = f"{T['kind']} {T['old']} → {T['new']}"
    T['failures'] = ([f"{head}: {c['check']}" + (f" ({c['detail']})" if c['detail'] else '') for c in T['checks'] if not c['ok']]
                     + [f"{head}: 쌍 {r_['pair']} — {r_.get('reason') or '실패'}" for r_ in T['rows'] if not r_.get('ok')])
    T['verdict'] = 'PASS' if not T['failures'] else 'FAIL'
    return T


def compare(kind, A, B):
    """두 되읽은 덱 → 표 dict (kind · rows · checks · meta · failures · verdict).  kind ∈ E · E0 · DT · B."""
    T = dict(kind=kind, old=A['label'], new=B['label'], old_sha256=A['sha256'], new_sha256=B['sha256'],
             rows=[], checks=[], meta={}, k=None, level=None, verdict=None, failures=[])

    def check(name, cond, detail=''):
        T['checks'].append(dict(check=name, ok=bool(cond), detail=str(detail)))
        return bool(cond)
    if kind not in KINDS:
        check(f'표 종류 {kind!r} ∈ {KINDS}', False)
        return _final(T)
    for X in (A, B):
        check(f'덱 파싱 — {X["label"]} (필수 명령 · run 구조 [1, F, F, N] · 행렬 크기)', not X['problems'], '; '.join(X['problems']))
    if A['problems'] or B['problems']:
        return _final(T)
    for X in (A, B):
        check(f'타입 사전 = 등록 1 AM_P · 2 AM_S · 3 SE · 4 WALL (밀도 · 반지름 비 · 템플릿 시드 · 메시 타입) — {X["label"]}',
              not X['type_problems'], '; '.join(X['type_problems']))
    if A['type_problems'] or B['type_problems']:
        return _final(T)
    check('두 덱의 템플릿 (시드 · 밀도 · 반지름) · 타입 사전 동일', A['templates'] == B['templates'] and A['names'] == B['names'])
    N = A['n_types']
    VA, VB = _phases(A), _phases(B)
    for X, V in ((A, VA), (B, VB)):
        tok = X['ced_tok']
        check(f'CED 행렬 대칭 (인쇄 토큰까지) · 벽–벽 = 0 — {X["label"]}',
              all(tok[(i, j)] == tok[(j, i)] for i in range(1, N + 1) for j in range(1, N + 1)) and X['ced'][(N, N)] == 0.0)
        check(f'CED 전부 유한 · 비음수 — {X["label"]}', all(math.isfinite(v) and v >= 0.0 for v in X['ced'].values()))
        check(f'ν = 등록 (AM 0.25 · SE 0.30 · 벽 0.30) — {X["label"]}', all(V[ph]['nu'] == REG_NU[ph] for ph in REG_NU))
        check(f'AM · 벽 영률 = 등록 (1.037e9 · 1.037e9 · 1.48e9) · SE 영률 = 등록 수준 (1e7 · 1.4e8 · 2.8e8) — {X["label"]}',
              all(V[ph]['E'] == REG_E_FIXED[ph] for ph in REG_E_FIXED) and V['SE']['E'] in REG_E_SE,
              f"SE {V['SE']['E']:g} · AM_P {V['AM_P']['E']:g} · AM_S {V['AM_S']['E']:g} · 벽 {V['WALL']['E']:g}")
    rule_k = {}
    for X in (A, B):
        rule, by = rayleigh_dt(X)
        k_ = max(1, int(round(rule / X['dt'])))
        rule_k[X['label']] = k_
        if kind in ('E', 'E0') or (kind == 'DT' and X is A):
            check(f'dt = Rayleigh 규칙 (이 덱의 E · ν · 반지름 · 밀도 · 상별 최소) — {X["label"]}',
                  abs(X['dt'] / rule - 1.0) <= TOL['rayleigh_rel'],
                  f"덱 {X['dt_txt']} vs 규칙 {rule:.6g} s ({by} 가 정함 · 비 {X['dt'] / rule:.6f} · 허용 ±{TOL['rayleigh_rel']:.2e})")
        elif kind == 'B':
            check(f'dt = Rayleigh 규칙의 정확히 1/k (k 정수 ≥ 1 · k = 1 이면 규칙 그대로) — {X["label"]}',
                  abs(X['dt'] * k_ / rule - 1.0) <= TOL['rayleigh_rel'],
                  f"덱 {X['dt_txt']} × {k_} vs 규칙 {rule:.6g} s ({by})")
    if kind == 'B':
        T['k'] = rule_k[A['label']] if rule_k[A['label']] == rule_k[B['label']] else None
    ca, cb = collections.Counter(A['comments']), collections.Counter(B['comments'])
    only_a, only_b = ca - cb, cb - ca
    T['meta'] = dict(comment_only_old=sum(only_a.values()), comment_only_new=sum(only_b.values()),
                     examples_new=[c[:100] for c in list(only_b)[:3]],
                     note='주석 (팔 설명 · 강성 머리 블록 · 출처) — 허용 메타 (판정 밖)')
    diffs = _cmd_diff(A, B, kind)
    allowed = {'E': 'SE 영률 · CED 값 · timestep · run · dump 간격 · restart 간격',
               'E0': 'SE 영률 · CED 값 · timestep · run · dump 간격 · restart 간격',
               'DT': 'timestep · run · dump 간격 · restart 간격', 'B': 'CED 값'}[kind]
    check(f'허용 밖 명령은 토큰까지 같다 (허용: {allowed})', not diffs, '; '.join(diffs[:4]) + (f' … 외 {len(diffs) - 4}' if len(diffs) > 4 else ''))
    FA, FB, NA, NB = A['runs'][1], B['runs'][1], A['runs'][3], B['runs'][3]
    DA, DB, dtA, dtB = A['dump_every'], B['dump_every'], A['dt'], B['dt']
    if kind in ('E', 'E0'):
        F = VB['SE']['E'] / VA['SE']['E']
        T['level'] = dict(old=REG_E_SE.get(VA['SE']['E'], '미등록'), new=REG_E_SE.get(VB['SE']['E'], '미등록'), F=F)
        check('SE 영률만 바뀌었다 — AM_P · AM_S · 벽 영률 정확히 같다 · ν 전부 같다 · SE 는 **달라야** 한다 (E 비교)',
              all(VA[ph]['E'] == VB[ph]['E'] for ph in ('AM_P', 'AM_S', 'WALL')) and A['nu'] == B['nu'] and F != 1.0,
              f'SE ×{F:g}')
        codex = next((CODEX[c] for c in CODEX if VA['SE']['E'] == 1.0e7 and abs(F - c) <= TOL['exact_rel'] * c), None)
        T['codex_level'] = None if codex is None else F
        for ti, tj in PAIRS:
            a, b, a2, b2 = VA[ti], VA[tj], VB[ti], VB[tj]
            key = (a['type'], b['type'])
            co, cn = A['ced'][key], B['ced'][key]
            r_ = dict(pair=f'{ti}–{tj}', types=f'{key[0]}-{key[1]}', CED_old=co, CED_new=cn, codex='N/A', reason='')
            if ti == tj == 'WALL':
                r_.update(ok=(co == 0.0 and cn == 0.0), F0_ratio=None)
                r_['reason'] = '' if r_['ok'] else f'벽–벽 ≠ 0 ({co:g} → {cn:g})'
                T['rows'].append(r_)
                continue
            rs, eo, en = rstar(a, b), estar(a, b), estar(a2, b2)
            fo, fn = f0(co, rs, eo), f0(cn, rs, en)
            r_.update(R_star=rs, Estar_old=eo, Estar_new=en, Estar_mult=en / eo, CED_mult=(cn / co) if co else None,
                      F0_old=fo, F0_new=fn, F0_ratio=None, tol=TOL['f0_ratio'])
            if co == 0.0:
                r_['ok'] = cn == 0.0
                r_['reason'] = '' if r_['ok'] else f'0 → {cn:g} (0 은 정확히 0 이어야 한다)'
            elif not (cn > 0.0 and math.isfinite(cn)):
                r_['ok'], r_['reason'] = False, f'{co:g} → {cn:g} (비영 항이 0 · 음수 · 비유한)'
            else:
                r_['F0_ratio'] = fn / fo
                r_['ok'] = abs(r_['F0_ratio'] - 1.0) <= TOL['f0_ratio']
                r_['reason'] = '' if r_['ok'] else f"F₀ 비 {r_['F0_ratio']:.6f} (허용 ±{TOL['f0_ratio']:.0e})"
            if codex is not None and (ti, tj) in codex:
                em, cm = codex[(ti, tj)]
                cok = abs(r_['Estar_mult'] / em - 1.0) <= TOL['codex_estar_rel'] and (co == 0.0 or abs(r_['CED_mult'] / cm - 1.0) <= TOL['ced_mult_rel'])
                r_['codex'] = 'PASS' if cok else 'FAIL'
                r_['codex_expect'] = dict(Estar_mult=em, CED_mult=cm)
                if not cok:
                    r_['ok'] = False
                    r_['reason'] = (r_['reason'] + ' · ' if r_['reason'] else '') + \
                        f"Codex 배수 불일치 (E* ×{r_['Estar_mult']:.9f} vs {em} · CED ×{(r_['CED_mult'] or 0):.6f} vs {cm})"
            T['rows'].append(r_)
        if kind == 'E0':
            check('전 점착 0 — 두 덱 CED 전 원소 정확히 0 (E0)', all(v == 0.0 for v in A['ced'].values()) and all(v == 0.0 for v in B['ced'].values()))
        tsA, tsB = 2 * FA * dtA, 2 * FB * dtB
        tol_s = 2 * TOL['dt_print_rel'] * max(tsA, tsB) + dtA + dtB
        check('물리 시간 — 정착 2F·dt 같다 (허용 = dt 인쇄 2 × 5e-4 · T + 반올림 1 step 씩)', abs(tsA - tsB) <= tol_s,
              f'{tsA:.9g} → {tsB:.9g} s (차 {tsB - tsA:+.3g} · 허용 {tol_s:.3g})')
        trA, trB = NA * dtA, NB * dtB
        tol_r = 2 * TOL['dt_print_rel'] * max(trA, trB) + 0.5 * (dtA + dtB)
        check('물리 시간 — 회전 N·dt 같다 (= 바퀴 수 같다 · Drum 주기는 명령 대조로 같다)', abs(trA - trB) <= tol_r,
              f'{trA:.9g} → {trB:.9g} s = {trA / A["period"]:.6f} → {trB / B["period"]:.6f} 바퀴 (차 {trB - trA:+.3g} s · 허용 {tol_r:.3g})')
        check(f'덤프 간격 = 등록 규칙 ({DUMP_RULE}) — 두 덱', DA == dump_rule(NA) and DB == dump_rule(NB),
              f'{DA} (규칙 {dump_rule(NA)}) → {DB} (규칙 {dump_rule(NB)})')
        check(f'체크포인트 간격 = 등록 규칙 ({RESTART_RULE}) — 두 덱',
              A['restart_every'] == restart_rule(FA, NA) and B['restart_every'] == restart_rule(FB, NB),
              f"{A['restart_every']} (규칙 {restart_rule(FA, NA)}) → {B['restart_every']} (규칙 {restart_rule(FB, NB)})")
        t0A, t0B = planned_t0(FA, DA) * dtA, planned_t0(FB, DB) * dtB
        check('계획 t₀ 물리 시각 — 차 ≤ 덤프 간격 하나 (t₀ = 정착 끝 직전 덤프 격자점)', abs(t0A - t0B) <= max(DA * dtA, DB * dtB) + tol_s,
              f'{t0A:.9g} → {t0B:.9g} s (step {planned_t0(FA, DA)} → {planned_t0(FB, DB)})')
    elif kind == 'DT':
        kr = dtA / dtB
        k = int(round(kr))
        T['k'] = k
        check('dt 가 정확히 1/k (k 정수 ≥ 2 · 인쇄된 dt 대조 1e-12)', k >= 2 and abs(dtB * k / dtA - 1.0) <= TOL['exact_rel'],
              f"{A['dt_txt']} → {B['dt_txt']} (비 {kr:.12g})")
        check(f'k = {REG_DT_K} (등록 E0_ref@dt/2)', k == REG_DT_K, f'k {k}')
        check('E · ν · CED (인쇄 토큰) · 템플릿 정확히 같다 — dt 만 다르다',
              A['E'] == B['E'] and A['nu'] == B['nu'] and A['ced_tok'] == B['ced_tok'] and A['templates'] == B['templates'])
        check('run 1 (삽입 step) 그대로 · 정착 · 회전 step 정확히 k 배',
              A['runs'][0] == B['runs'][0] == 1 and B['runs'][1:] == [k * x for x in A['runs'][1:]], f"{A['runs']} → {B['runs']}")
        check('덤프 간격 step 정확히 k 배 (덤프 시각 불변)', DB == k * DA, f'{DA} → {DB}')
        check(f'체크포인트 간격 = 등록 규칙 (새 step · {RESTART_RULE})', B['restart_every'] == restart_rule(FB, NB),
              f"{B['restart_every']} (규칙 {restart_rule(FB, NB)})")
        t0A, t0B = planned_t0(FA, DA) * dtA, planned_t0(FB, DB) * dtB
        check('계획 t₀ 물리 시각 같다 (1e-12)', abs(t0B / t0A - 1.0) <= TOL['exact_rel'] if t0A else t0B == 0.0,
              f'step {planned_t0(FA, DA)} → {planned_t0(FB, DB)} · {t0A:.12g} → {t0B:.12g} s')
        sA, sB = A['period'] / dtA, B['period'] / dtB
        check('바퀴당 step 정확히 k 배 (bin 경계 물리 시각 같다)', abs(sB / sA - k) <= TOL['exact_rel'] * max(k, 1), f'{sA:.9g} → {sB:.9g}')
        for ti, tj in PAIRS:
            key = (VA[ti]['type'], VA[tj]['type'])
            same = A['ced_tok'][key] == B['ced_tok'][key]
            T['rows'].append(dict(pair=f'{ti}–{tj}', types=f'{key[0]}-{key[1]}', CED_old=A['ced'][key], CED_new=B['ced'][key],
                                  ok=same, reason='' if same else '같아야 할 CED 가 다르다'))
    else:                                                   # B
        check('같은 강성 — E · ν 정확히 같다', A['E'] == B['E'] and A['nu'] == B['nu'])
        for ti, tj in PAIRS:
            key = (VA[ti]['type'], VA[tj]['type'])
            lc, lh = A['ced'][key], B['ced'][key]
            exp = (ti, tj) in B_PAIRS
            r_ = dict(pair=f'{ti}–{tj}', types=f'{key[0]}-{key[1]}', LC=lc, LH=lh, diff=lh - lc,
                      ratio=(lh / lc) if lc else None, expect_change=exp)
            if ti == tj == 'WALL':
                r_['ok'] = lc == 0.0 and lh == 0.0
                r_['reason'] = '' if r_['ok'] else '벽–벽 ≠ 0'
            elif exp:
                r_['ok'] = lh > lc and (lh - lc) > TOL['ced_mult_rel'] * max(lc, lh)
                r_['reason'] = '' if r_['ok'] else ('방향 반대 (LH < LC)' if lh < lc else '개입 누락 (LH = LC)')
            else:
                r_['ok'] = A['ced_tok'][key] == B['ced_tok'][key]
                r_['reason'] = '' if r_['ok'] else f'바뀌면 안 되는 항이 바뀌었다 ({A["ced_tok"][key]} → {B["ced_tok"][key]})'
            T['rows'].append(r_)
    return _final(T)


# ══ 보고 (JSON · markdown) ══════════════════════════════════════════════════════════════════════════════════════
def _gen_cmd(path):
    """덱 옆 `gen_cmd.txt` (없으면 `deck_meta.json` 의 argv) — 없으면 None ('미기록')."""
    d = os.path.dirname(os.path.abspath(path))
    p1, p2 = os.path.join(d, 'gen_cmd.txt'), os.path.join(d, 'deck_meta.json')
    if os.path.exists(p1):
        return open(p1, encoding='utf-8').read().strip()
    if os.path.exists(p2):
        try:
            return 'python3 scripts/make_mixer_deck.py ' + ' '.join(json.load(open(p2, encoding='utf-8')).get('argv', []))
        except (OSError, ValueError):
            return None
    return None


def load(path):
    text = open(path, encoding='utf-8').read()
    base = os.path.basename(path)
    label = os.path.basename(os.path.dirname(os.path.abspath(path))) if base == 'in.mixer' else base
    D = read_deck(text, label=label, path=path)
    D['gen_cmd'] = _gen_cmd(path)
    return D


def deck_summary(D):
    s = dict(label=D['label'], path=D['path'], sha256=D['sha256'], bytes=D['bytes'], gen_cmd=D.get('gen_cmd'),
             problems=D['problems'], type_problems=D['type_problems'], types={str(k): v for k, v in D['names'].items()},
             E=D['E'], nu=D['nu'], dt_txt=D['dt_txt'], runs=D['runs'], dump_every=D['dump_every'],
             restart_every=D['restart_every'], period_s=D['period'],
             templates={str(k): v for k, v in sorted(D['templates'].items())},
             ced={f'{i}-{j}': D['ced_tok'][(i, j)] for (i, j) in sorted(D['ced_tok'] or {}) if i <= j} if D['ced_tok'] else None,
             comment_lines=len(D['comments']))
    if not D['problems'] and D['dt']:
        t0 = planned_t0(D['runs'][1], D['dump_every'])
        s.update(t0_planned=t0, t0_planned_s=t0 * D['dt'], steps_per_rev=D['period'] / D['dt'],
                 settle_s=2 * D['runs'][1] * D['dt'], rotation_s=D['runs'][3] * D['dt'])
    return s


def make_report(decks, tables, argv=None):
    me = os.path.abspath(__file__)
    fails = [f for T in tables for f in T['failures']]
    return dict(tool=TOOL, tool_version=TOOL_VERSION, tool_sha256=hashlib.sha256(open(me, 'rb').read()).hexdigest(),
                argv=list(argv or []), tolerances=TOL, tolerances_why=TOL_WHY,
                registered=dict(types={str(k): v for k, v in REG_TYPES.items()},
                                template_seeds={str(k): v for k, v in REG_TPL_SEED.items()}, density=REG_DENSITY, d_um=REG_D_UM,
                                E_fixed=REG_E_FIXED, E_SE_levels={f'{k:g}': v for k, v in REG_E_SE.items()}, nu=REG_NU,
                                B_pairs=sorted(f'{a}–{b}' for a, b in B_PAIRS), dt_k=REG_DT_K, dump_rule=DUMP_RULE,
                                restart_rule=RESTART_RULE, rayleigh_rule=RAYLEIGH_RULE,
                                codex_section5={f'{F:g}': {f'{a}–{b}': list(v) for (a, b), v in c.items()} for F, c in CODEX.items()}),
                decks={p: deck_summary(D) for p, D in decks.items()}, tables=tables,
                verdict='PASS' if not fails and tables else 'FAIL', failures=fails)


def _g(v, spec='.6g'):
    return '—' if v is None else format(v, spec)


def to_markdown(rep):
    n = len(rep['tables'])
    npass = sum(T['verdict'] == 'PASS' for T in rep['tables'])
    t = rep['tolerances']
    L = [f"# 믹서 실행 덱 되읽기 — `{rep['tool']}` ({rep['tool_version']})", '',
         f"- 판정 **{rep['verdict']}** — 표 {npass}/{n} PASS · 도구 sha256 `{rep['tool_sha256'][:16]}…`",
         f"- 허용오차 (비교 **전** · 인쇄 형식에서): F₀ 비 ±{t['f0_ratio']:.0e} · CED 배수 ±{t['ced_mult_rel']:.0e} · "
         f"Codex E* ±{t['codex_estar_rel']:.0e} · dt 인쇄 {t['dt_print_rel']:.0e} (표 E 물리 시간) · DT 표 정확 {t['exact_rel']:.0e}",
         '- 계산: 덱 텍스트에서 되읽은 E · ν · 반지름 (템플릿) · CED 로 E*_ij = [(1−ν_i²)/E_i + (1−ν_j²)/E_j]⁻¹ · '
         'R* (입자쌍 r_i r_j/(r_i+r_j) · 벽 = r) · F₀ = (9/2)π³R*²CED³/E*² — **생성기를 import 하지 않는다**',
         '', '## 덱', '',
         '| 라벨 | sha256 (앞 16) | bytes | SE 영률 | dt | run (삽입 · 정착 · 정착 · 회전) | 덤프 | 체크포인트 | 생성 명령 |',
         '|---|---|---:|---:|---:|---|---:|---:|---|']
    for p, d in rep['decks'].items():
        se = d['E'][2] if d['E'] and len(d['E']) > 2 else None
        L.append(f"| `{d['label']}` | `{d['sha256'][:16]}` | {d['bytes']:,} | {_g(se, '.4g')} | {d['dt_txt']} | "
                 f"{' · '.join(f'{x:,}' for x in d['runs'])} | {_g(d['dump_every'], ',')} | {_g(d['restart_every'], ',')} | "
                 f"{('`' + d['gen_cmd'] + '`') if d['gen_cmd'] else '미기록'} |")
    for T in rep['tables']:
        L += ['', f"## 표 {T['kind']} — `{T['old']}` → `{T['new']}` — **{T['verdict']}**", '']
        if T['kind'] in ('E', 'E0'):
            lv = T.get('level') or {}
            L += [f"SE 영률 {lv.get('old', '?')} → {lv.get('new', '?')} (×{_g(lv.get('F'), 'g')}) · "
                  f"Codex 7 차 §5 대조: {'×' + format(T['codex_level'], 'g') if T.get('codex_level') else 'N/A (soft → ×14 · ×28 만 등록)'}", '',
                  '| 쌍 | 타입 | R* (m) | E*_old → E*_new (Pa) | E* 배수 | CED_old → CED_new (J/m³) | CED 배수 | F₀_old → F₀_new (N) | F₀ 비 | 허용 | Codex | 판정 |',
                  '|---|---|---:|---|---:|---|---:|---|---:|---:|---|---|']
            for r_ in T['rows']:
                L.append(f"| {r_['pair']} | {r_['types']} | {_g(r_.get('R_star'))} | {_g(r_.get('Estar_old'))} → {_g(r_.get('Estar_new'))} | "
                         f"{_g(r_.get('Estar_mult'), '.9g')} | {_g(r_['CED_old'])} → {_g(r_['CED_new'])} | {_g(r_.get('CED_mult'), '.7g')} | "
                         f"{_g(r_.get('F0_old'))} → {_g(r_.get('F0_new'))} | {_g(r_.get('F0_ratio'), '.9f')} | "
                         f"{('±' + format(r_['tol'], '.0e')) if r_.get('tol') else ('0 = 0' if r_['CED_old'] == 0 else '—')} | "
                         f"{r_.get('codex', 'N/A')} | {'PASS' if r_['ok'] else 'FAIL · ' + r_['reason']} |")
        elif T['kind'] == 'DT':
            L += [f"k = {T.get('k')} (등록 {REG_DT_K})", '', '| 쌍 | 타입 | CED (ref) | CED (dt/2) | 판정 |', '|---|---|---:|---:|---|']
            for r_ in T['rows']:
                L.append(f"| {r_['pair']} | {r_['types']} | {_g(r_['CED_old'])} | {_g(r_['CED_new'])} | "
                         f"{'PASS (같다)' if r_['ok'] else 'FAIL · ' + r_['reason']} |")
        else:
            L += ['| 쌍 | 타입 | LC CED (J/m³) | LH CED (J/m³) | 차 (LH−LC) | LH/LC | 바뀌어야 | 판정 |', '|---|---|---:|---:|---:|---:|---|---|']
            for r_ in T['rows']:
                L.append(f"| {r_['pair']} | {r_['types']} | {_g(r_['LC'])} | {_g(r_['LH'])} | {_g(r_['diff'])} | "
                         f"{_g(r_['ratio'], '.6g') if r_['ratio'] is not None else 'N/A (LC = 0)'} | {'예 (B)' if r_['expect_change'] else '아니오'} | "
                         f"{'PASS' if r_['ok'] else 'FAIL · ' + r_['reason']} |")
        L += ['', '검사:', '']
        L += [f"- {'✓' if c['ok'] else '✗'} {c['check']}" + (f" — {c['detail']}" if c['detail'] else '') for c in T['checks']]
        m = T.get('meta') or {}
        if m:
            L.append(f"- (메타 · 판정 밖) 주석 줄 — 옛 덱에만 {m.get('comment_only_old', 0)} · 새 덱에만 {m.get('comment_only_new', 0)} "
                     f"({m.get('note', '')})")
    if rep['failures']:
        L += ['', '## 실패 항', ''] + [f'- {f}' for f in rep['failures']]
    return '\n'.join(L) + '\n'


def _selftest():
    """고정물 (fixture) 덱은 생성기로 만든다 — **검산은 생성기를 쓰지 않는다** (이 파일의 파서 · 산술만).
    반례 (Codex 9 차 §3 · §6-2 음성대조): 혼합쌍 하나 · SE–벽만 · 타입 순서 · 0 행렬 변조 · 덤프 간격 변조 + 비대칭 · 영률/ν · 명령 ·
    step 미재계산 · dt 비정수배 · B 몰래 변경/누락/방향 — 전부 **잡아야** 한다."""
    import re
    import subprocess
    import tempfile
    sys.path.insert(0, _HERE)
    import make_mixer_deck as gen                      # 고정물 전용 (검산 경로 밖)
    ok, fail = 0, []

    def chk(name, cond):
        nonlocal ok
        if cond:
            ok += 1
        else:
            fail.append(name)
        print(('  PASS  ' if cond else '  FAIL  ') + name)

    def _ok(fn):
        try:
            return bool(fn())
        except (Exception, SystemExit):
            return False

    pc = gen.plan(100000, cgf=151.4)
    rpm = gen.resolve_rpm(pc['R'])
    P = {F: gen.plan(100000, cgf=151.4, stiffen_se=F) for F in (1.0, 14.0, 28.0)}

    def mk(arm, F, rev, dtf=1.0):
        return gen.deck(P[F], rpm, rev, seed=32452843, arm=arm, hold_bo_pairwise=(F != 1.0), dt_factor=dtf)
    D = {'LC_soft': mk('LC', 1.0, 2), 'LH_soft': mk('LH', 1.0, 2), 'LC_ref': mk('LC', 14.0, 2), 'LH_ref': mk('LH', 14.0, 2),
         'LC_ref2': mk('LC', 28.0, 2), 'LH_ref2': mk('LH', 28.0, 2), 'LC_refdt': mk('LC', 14.0, 2, 0.5),
         'LH_refdt': mk('LH', 14.0, 2, 0.5),
         'E0_soft': mk('E0', 1.0, 0), 'E0_ref': mk('E0', 14.0, 0), 'E0_ref2': mk('E0', 28.0, 0), 'E0_refdt': mk('E0', 14.0, 0, 0.5)}

    def cmp_(kind, a, b, ta=None, tb=None):
        return compare(kind, read_deck(D[a] if ta is None else ta, a), read_deck(D[b] if tb is None else tb, b + ('*' if tb else '')))

    def row(T, pair):
        return next((r_ for r_ in T['rows'] if r_.get('pair') == pair), None)

    def failed_pairs(T):
        return sorted(r_['pair'] for r_ in T['rows'] if not r_.get('ok'))

    def sub1(text, pat, rep, flags=re.M):
        new, n = re.subn(pat, rep, text, count=1, flags=flags)
        assert n == 1, pat
        return new

    def set_ced(text, i, j, val, sym=True):
        """CED 행렬 (1-based 타입) 칸을 val 문자열로 — sym 이면 (j, i) 도.  줄 끝 `&` 는 그대로 둔다."""
        lines = text.split('\n')
        k0 = next(k for k, l in enumerate(lines) if l.startswith('fix ') and 'cohesionEnergyDensity' in l)
        for a_, b_ in dict.fromkeys(((i, j), (j, i)) if sym else ((i, j),)):
            raw = lines[k0 + a_].rstrip()
            amp = raw.endswith('&')
            vals = raw.rstrip('&').split()
            vals[b_ - 1] = val
            lines[k0 + a_] = '    ' + ' '.join(vals) + (' &' if amp else '')
        return '\n'.join(lines)

    def get_ced(text, i, j):
        lines = text.split('\n')
        k0 = next(k for k, l in enumerate(lines) if l.startswith('fix ') and 'cohesionEnergyDensity' in l)
        return float(lines[k0 + i].rstrip().rstrip('&').split()[j - 1])

    # ── 양성 (등록 설계대로 만든 덱) ─────────────────────────────────────────────────────────
    T = cmp_('E', 'LC_soft', 'LC_ref')
    chk(f"① 표 E LC soft → ×14: PASS · 9 비영 항 F₀ 비 = 1 (허용 {TOL['f0_ratio']:.0e}) · 벽–벽 0 · Codex ×14 배수 대조 PASS "
        f"(실패 {failed_pairs(T)})",
        _ok(lambda: T['verdict'] == 'PASS' and len(T['rows']) == 10
            and all(abs(r_['F0_ratio'] - 1.0) <= TOL['f0_ratio'] for r_ in T['rows'] if r_['pair'] != 'WALL–WALL')
            and row(T, 'AM_P–SE')['codex'] == 'PASS' and row(T, 'SE–WALL')['codex'] == 'PASS'
            and row(T, 'AM_P–AM_P')['codex'] == 'PASS'))
    Ts = [cmp_('E', 'LH_soft', 'LH_ref'), cmp_('E', 'LC_soft', 'LC_ref2'), cmp_('E', 'LH_soft', 'LH_ref2'),
          cmp_('E', 'LC_ref', 'LC_ref2')]
    chk('② 표 E LH soft → ×14 · LC/LH soft → ×28 (Codex ×28 대조) · LC ×14 → ×28 (배수 2 — Codex 대조 N/A) 모두 PASS',
        _ok(lambda: all(t_['verdict'] == 'PASS' for t_ in Ts) and row(Ts[1], 'SE–SE')['codex'] == 'PASS'
            and row(Ts[3], 'SE–SE')['codex'] == 'N/A'))
    Ts = [cmp_('E0', 'E0_soft', 'E0_ref'), cmp_('E0', 'E0_ref', 'E0_ref2'), cmp_('E0', 'E0_soft', 'E0_ref2')]
    #  ⚠ 적색 단계에서 이 항이 **빈 표**로 통과했다 (아무것도 안 하는 스텁 · 행 0 개에 all() = True) ⇒ 행 10 개 · 명시 검사 항을 요구한다
    chk('③ 표 E0 soft → ×14 · ×14 → ×28 · soft → ×28: 두 덱 모두 전 점착 0 (정확히 · 행 10 개 · 명시 검사) · 물리 시간 · '
        '덤프/체크포인트 규칙 PASS',
        _ok(lambda: all(t_['verdict'] == 'PASS' and len(t_['rows']) == 10
                        and any('전 점착 0' in c_['check'] and c_['ok'] for c_ in t_['checks']) for t_ in Ts)
            and all(r_['CED_old'] == 0.0 and r_['CED_new'] == 0.0 for t_ in Ts for r_ in t_['rows'])))
    Ts = [cmp_('DT', 'E0_ref', 'E0_refdt'), cmp_('DT', 'LC_ref', 'LC_refdt')]
    chk('④ 표 DT E0 ×14 → dt/2 · LC ×14 → dt/2: E · ν · CED 동일 · dt 정확히 ½ · step · 덤프 ×2 · 계획 t₀ 물리 시각 동일 → PASS',
        _ok(lambda: all(t_['verdict'] == 'PASS' for t_ in Ts) and all(t_['k'] == 2 for t_ in Ts)))
    Ts = [cmp_('B', 'LC_soft', 'LH_soft'), cmp_('B', 'LC_ref', 'LH_ref'), cmp_('B', 'LC_ref2', 'LH_ref2')]
    chk('⑤ 표 B soft · ×14 · ×28: LC↔LH 다섯 쌍 (AM–AM 셋 · AM–벽 둘) 만 증가 · 나머지 전부 정확히 같다 · 벽–벽 0 → PASS',
        _ok(lambda: all(t_['verdict'] == 'PASS' for t_ in Ts)
            and all(sorted(r_['pair'] for r_ in t_['rows'] if r_['expect_change']) ==
                    sorted(['AM_P–AM_P', 'AM_P–AM_S', 'AM_S–AM_S', 'AM_P–WALL', 'AM_S–WALL']) for t_ in Ts)
            and all(row(t_, 'SE–SE')['LH'] == row(t_, 'SE–SE')['LC'] for t_ in Ts)
            and row(Ts[0], 'WALL–WALL')['ratio'] is None))
    # ── 음성대조 (반례 — 전부 잡아야 한다) ─────────────────────────────────────────────────────
    c13 = get_ced(D['LC_soft'], 1, 3)
    bad6 = set_ced(D['LC_ref'], 1, 3, f'{c13 * 14 ** (2.0 / 3.0):g}')        # 옛 동일상 규칙 = SE 배수를 혼합쌍에
    T6 = cmp_('E', 'LC_soft', 'LC_ref', tb=bad6)
    chk(f"⑥ 반례 혼합쌍 하나 (AM_P–SE 를 옛 규칙 ×14^(2/3)) → FAIL · 그 쌍만 짚는다 {failed_pairs(T6)} · F₀ 비 "
        f"{(row(T6, 'AM_P–SE') or {}).get('F0_ratio', float('nan')):.4f} (Codex 1.272)",
        _ok(lambda: T6['verdict'] == 'FAIL' and failed_pairs(T6) == ['AM_P–SE']
            and abs(row(T6, 'AM_P–SE')['F0_ratio'] - 1.272112360) < 1e-4))
    c33 = get_ced(D['LC_ref'], 3, 3)
    bad7 = set_ced(D['LC_ref'], 3, 4, f'{c33 / 6.25 ** (1.0 / 3.0):g}')       # 옛 규칙: SE–벽 = 새 대각 ÷ 1.842
    T7 = cmp_('E', 'LC_soft', 'LC_ref', tb=bad7)
    chk(f"⑦ 반례 SE–벽만 (새 SE 대각 ÷ 1.842 로 다시) → FAIL · SE–WALL 만 {failed_pairs(T7)} · F₀ 비 "
        f"{(row(T7, 'SE–WALL') or {}).get('F0_ratio', float('nan')):.4f} (Codex 1.182)",
        _ok(lambda: T7['verdict'] == 'FAIL' and failed_pairs(T7) == ['SE–WALL']
            and abs(row(T7, 'SE–WALL')['F0_ratio'] - 1.182108914) < 1e-4))
    sw = D['LC_ref'].replace('atom_type 1 ', 'atom_type 9 ').replace('atom_type 2 ', 'atom_type 1 ').replace('atom_type 9 ', 'atom_type 2 ')
    sw_lh = D['LH_ref'].replace('atom_type 1 ', 'atom_type 9 ').replace('atom_type 2 ', 'atom_type 1 ').replace('atom_type 9 ', 'atom_type 2 ')
    e_sw = sub1(D['LC_ref'], r'(youngsModulus peratomtype \S+) (\S+) (\S+)', r'\1 \3 \2')
    T8 = [cmp_('E', 'LC_soft', 'LC_ref', tb=sw), cmp_('B', 'LC_ref', 'LH_ref', tb=sw_lh), cmp_('E', 'LC_soft', 'LC_ref', tb=e_sw)]
    chk('⑧ 반례 타입 순서 — 템플릿 atom_type 1↔2 (표 E · 표 B) · 영률 줄의 AM_S ↔ SE 자리 바꿈 → 셋 다 FAIL (타입 사전 · 영률 대조)',
        _ok(lambda: all(t_['verdict'] == 'FAIL' for t_ in T8)
            and any('타입' in c_['check'] and not c_['ok'] for c_ in T8[0]['checks'])
            and any('영률' in c_['check'] and not c_['ok'] for c_ in T8[2]['checks'])))
    z1 = set_ced(D['E0_ref'], 3, 3, '1000')
    z2 = set_ced(D['LC_ref'], 4, 4, '1')
    T9 = [cmp_('E0', 'E0_soft', 'E0_ref', tb=z1), cmp_('E', 'LC_soft', 'LC_ref', tb=z2), cmp_('E0', 'E0_soft', 'E0_ref', ta=z1)]
    chk('⑨ 반례 0 행렬 변조 — E0 ×14 의 SE–SE = 1000 (새 쪽 · 옛 쪽) · LC ×14 의 벽–벽 = 1 → 셋 다 FAIL',
        _ok(lambda: all(t_['verdict'] == 'FAIL' for t_ in T9) and 'SE–SE' in failed_pairs(T9[0])
            and 'WALL–WALL' in failed_pairs(T9[1])))
    dmp = lambda t, f: sub1(t, r'^(dump dmp all custom )(\d+)', lambda m: m.group(1) + str(f(int(m.group(2)))))
    T10 = [cmp_('E', 'LC_soft', 'LC_ref', tb=dmp(D['LC_ref'], lambda x: x + 1)),
           cmp_('DT', 'E0_ref', 'E0_refdt', tb=dmp(D['E0_refdt'], lambda x: x - 1000)),
           cmp_('E0', 'E0_soft', 'E0_ref', tb=dmp(D['E0_ref'], lambda x: 2 * x))]
    chk('⑩ 반례 덤프 간격 변조 — LC ×14 +1 step (규칙 밖) · E0 dt/2 가 2 배가 아님 · E0 ×14 를 2 배로 → 셋 다 FAIL',
        _ok(lambda: all(t_['verdict'] == 'FAIL' for t_ in T10)
            and all(any('덤프' in c_['check'] and not c_['ok'] for c_ in t_['checks']) for t_ in T10)))
    asym = set_ced(D['LC_ref'], 1, 3, f'{get_ced(D["LC_ref"], 1, 3) * 1.001:g}', sym=False)
    T11 = cmp_('E', 'LC_soft', 'LC_ref', tb=asym)
    chk('⑪ 반례 비대칭 (AM_P–SE 한쪽 칸만 ×1.001) → FAIL (대칭 검사)',
        _ok(lambda: T11['verdict'] == 'FAIL' and any('대칭' in c_['check'] and not c_['ok'] for c_ in T11['checks'])))
    se_se = set_ced(D['LH_ref'], 3, 3, f'{get_ced(D["LH_ref"], 3, 3) + 0.1:.1f}')
    miss = set_ced(D['LH_ref'], 1, 1, f'{get_ced(D["LC_ref"], 1, 1):g}')
    down = set_ced(D['LH_ref'], 2, 4, f'{get_ced(D["LC_ref"], 2, 4) / 2:g}')
    grav = sub1(D['LH_ref'], r'(gravity )9\.81', r'\g<1>9.80')
    T12 = [cmp_('B', 'LC_ref', 'LH_ref', tb=x) for x in (se_se, miss, down, grav)]
    chk(f"⑫ 반례 표 B — LH SE–SE +0.1 (몰래 변경) · AM_P–AM_P = LC (개입 누락) · AM_S–벽 ÷2 (방향 반대) · 중력 9.80 (명령) → 넷 다 FAIL "
        f"{[failed_pairs(t_) for t_ in T12]}",
        _ok(lambda: all(t_['verdict'] == 'FAIL' for t_ in T12) and failed_pairs(T12[0]) == ['SE–SE']
            and failed_pairs(T12[1]) == ['AM_P–AM_P'] and failed_pairs(T12[2]) == ['AM_S–WALL']
            and any('명령' in c_['check'] and not c_['ok'] for c_ in T12[3]['checks'])))
    am_e = sub1(D['LC_ref'], r'(youngsModulus peratomtype )1\.037e\+09', r'\g<1>1.1e+09')
    nu = sub1(D['LC_ref'], r'(poissonsRatio peratomtype \S+ \S+ )0\.30', r'\g<1>0.31')
    nb = sub1(D['LC_ref'], r'^(neighbor\s+)(\S+)', lambda m: m.group(1) + f'{float(m.group(2)) * 1.5:.6g}')
    soft_runs = re.findall(r'^run (\d+)$', D['LC_soft'], re.M)
    it = iter(soft_runs)
    norescale = re.sub(r'^run (\d+)$', lambda m: 'run ' + next(it), D['LC_ref'], flags=re.M)
    T13 = [cmp_('E', 'LC_soft', 'LC_ref', tb=x) for x in (am_e, nu, nb, norescale)]
    chk('⑬ 반례 표 E — AM_P 영률 변경 · SE ν 변경 · neighbor 변경 (허용 밖 명령) · step 을 새 dt 로 다시 안 셈 (soft step 그대로) → 넷 다 FAIL',
        _ok(lambda: all(t_['verdict'] == 'FAIL' for t_ in T13)
            and any('물리 시간' in c_['check'] and not c_['ok'] for c_ in T13[3]['checks'])))
    r1 = sub1(D['E0_refdt'], r'^run (\d+)$\n(?=unfix ins)', lambda m: f'run {int(m.group(1)) + 1}\n')
    dtx = sub1(D['E0_refdt'], r'^timestep\s+1\.566e-07$', 'timestep        1.567e-07')
    T14 = [cmp_('DT', 'E0_ref', 'E0_refdt', tb=x) for x in (r1, dtx)] + [cmp_('DT', 'LC_soft', 'LC_ref')]
    chk('⑭ 반례 표 DT — 정착 step +1 (정수배 아님) · dt 1.567e-07 (정확히 ½ 아님) · soft → ×14 를 DT 로 (k 비정수 · 영률 다름) → 셋 다 FAIL',
        _ok(lambda: all(t_['verdict'] == 'FAIL' for t_ in T14)))
    T15 = cmp_('E', 'LC_ref', 'LC_ref')
    chk('⑮ 같은 덱 둘을 표 E 로 → FAIL (SE 영률이 같다 = E 비교가 아니다 — 빈 비교를 PASS 로 내지 않는다)',
        _ok(lambda: T15['verdict'] == 'FAIL'))
    #  ⑱ 반례 (C 설계 중 발견 — 2026-09-30): SE 를 경화하고 **dt 를 다시 안 셌다** — soft 의 dt · step · 덤프 · 체크포인트를 그대로 두면
    #     물리 시간 · 덤프/체크포인트 규칙 · 쌍별 CED 가 **전부 맞아** 보인다.  그런데 dt 0.7055 µs 는 경화한 SE 의 Rayleigh 한계
    #     0.3132 µs 의 2.25 배 = 적분 불안정.  ⇒ dt 를 이 덱의 E · ν · 반지름 · 밀도로 다시 낸 Rayleigh 규칙과 대조해야 한다.
    def stale_dt(ref, soft):
        out = sub1(ref, r'^timestep\s+\S+$', re.search(r'^timestep\s+\S+$', soft, re.M).group(0))
        it2 = iter(re.findall(r'^run (\d+)$', soft, re.M))
        out = re.sub(r'^run (\d+)$', lambda m: 'run ' + next(it2), out, flags=re.M)
        de = re.search(r'^dump dmp all custom (\d+)', soft, re.M).group(1)
        out = sub1(out, r'^(dump dmp all custom )\d+', lambda m: m.group(1) + de)
        rs = re.search(r'^restart (\d+) ', soft, re.M).group(1)
        return sub1(out, r'^(restart )\d+', lambda m: m.group(1) + rs)
    T18 = [cmp_('E', 'LC_soft', 'LC_ref', tb=stale_dt(D['LC_ref'], D['LC_soft'])),
           cmp_('E0', 'E0_soft', 'E0_ref', tb=stale_dt(D['E0_ref'], D['E0_soft']))]
    bad18 = [[c_['check'] for c_ in t_['checks'] if not c_['ok']] for t_ in T18]
    chk(f'⑱ ★ 반례 — SE ×14 인데 dt · step · 덤프 · 체크포인트를 soft 그대로 (LC · E0): 물리 시간 · 규칙 · 쌍별 CED 는 다 맞아도 '
        f'**Rayleigh dt 대조 하나로** FAIL (적분 불안정 덱) {[len(b_) for b_ in bad18]}',
        _ok(lambda: all(t_['verdict'] == 'FAIL' for t_ in T18) and all(b_ and all('Rayleigh' in x for x in b_) for b_ in bad18)
            and all(r_['ok'] for t_ in T18 for r_ in t_['rows'])))
    T19 = cmp_('B', 'LC_refdt', 'LH_refdt')
    chk('⑲ 표 B 는 dt/2 짝 (LC ×14 dt/2 ↔ LH ×14 dt/2) 도 PASS — dt = Rayleigh 규칙의 정확히 1/k (k 정수) 는 허용 · k 를 적는다',
        _ok(lambda: T19['verdict'] == 'PASS' and T19.get('k') == 2))
    chk('⑳ Rayleigh 사본 = 생성기 plan() 의 dt (F 1 · 14 · 28 × CGF 151.4 · 200 — 덱에 찍힌 반지름 · 밀도 · E · ν 에서 다시 낸 값 · '
        '허용 rayleigh_rel) — 식이 갈리면 여기서 드러난다',
        _ok(lambda: all(abs(rayleigh_dt(read_deck(gen.deck(gen.plan(100000, cgf=c_, stiffen_se=F_), rpm, 0, arm='E0',
                                                           hold_bo_pairwise=True), 'x'))[0]
                            / gen.plan(100000, cgf=c_, stiffen_se=F_)['dt'] - 1.0) <= TOL['rayleigh_rel']
                        for F_ in (1.0, 14.0, 28.0) for c_ in (151.4, 200.0))))
    rd = read_deck(D['LC_ref'], 'x')
    chk('⑯ 되읽기 = 덱 텍스트: sha256 · 타입 사전 (1 AM_P · 2 AM_S · 3 SE · 4 WALL — 밀도 · 반지름 · 템플릿 시드 · 메시 타입) · '
        'E · ν · dt · run · 덤프 · 체크포인트',
        _ok(lambda: rd['sha256'] == hashlib.sha256(D['LC_ref'].encode('utf-8')).hexdigest()
            and rd['names'] == REG_TYPES and rd['E'] == [1.037e9, 1.037e9, 1.4e8, 1.48e9] and rd['nu'] == [0.25, 0.25, 0.30, 0.30]
            and rd['dt_txt'] == '3.132e-07' and rd['runs'] == [int(x) for x in re.findall(r'^run (\d+)$', D['LC_ref'], re.M)]
            and rd['dump_every'] == int(re.search(r'^dump dmp all custom (\d+)', D['LC_ref'], re.M).group(1))
            and not rd['problems'] and not rd['type_problems']))
    with tempfile.TemporaryDirectory() as td:
        paths = {}
        for k in ('LC_soft', 'LC_ref', 'LH_ref'):
            os.makedirs(os.path.join(td, k))
            paths[k] = os.path.join(td, k, 'in.mixer')
            open(paths[k], 'w', encoding='utf-8').write(D[k] if k != 'LH_ref' else se_se)
            open(os.path.join(td, k, 'gen_cmd.txt'), 'w', encoding='utf-8').write(f'python3 scripts/make_mixer_deck.py … ({k})\n')
        js, md = os.path.join(td, 'r.json'), os.path.join(td, 'r.md')
        me = os.path.abspath(__file__)
        a = subprocess.run([sys.executable, me, '--table', 'E', paths['LC_soft'], paths['LC_ref'], '--json', js, '--md', md],
                           capture_output=True, text=True)
        rep = json.load(open(js, encoding='utf-8')) if os.path.exists(js) else {}
        mdt = open(md, encoding='utf-8').read() if os.path.exists(md) else ''
        b = subprocess.run([sys.executable, me, '--table', 'E', paths['LC_soft'], paths['LC_ref'],
                            '--table', 'B', paths['LC_ref'], paths['LH_ref'], '--json', js], capture_output=True, text=True)
        rep_b = json.load(open(js, encoding='utf-8')) if os.path.exists(js) else {}
        chk('⑰ CLI: PASS 면 rc 0 · JSON (도구 sha256 · 버전 · 허용오차 · 덱 sha256 · 생성 명령 (gen_cmd.txt) · 타입 사전 · 표) · '
            'markdown 표 · FAIL 이 섞이면 rc 1 이고 실패 항 목록이 남는다',
            _ok(lambda: a.returncode == 0 and rep['verdict'] == 'PASS' and rep['tool_version'] == TOOL_VERSION
                and rep['tool_sha256'] == hashlib.sha256(open(me, 'rb').read()).hexdigest()
                and set(rep['tolerances']) >= {'f0_ratio', 'ced_mult_rel', 'dt_print_rel', 'exact_rel'}
                and rep['decks'][paths['LC_ref']]['sha256'] == hashlib.sha256(D['LC_ref'].encode('utf-8')).hexdigest()
                and rep['decks'][paths['LC_ref']]['gen_cmd'].endswith('(LC_ref)')
                and rep['decks'][paths['LC_ref']]['types'] == {str(k_): v_ for k_, v_ in REG_TYPES.items()}
                and '| AM_P–SE |' in mdt and 'F₀' in mdt
                and b.returncode == 1 and rep_b['verdict'] == 'FAIL'
                and any(f_.startswith('B ') and 'SE–SE' in f_ for f_ in rep_b['failures'])))
    print(f'\nmixer_deck_readback selftest: {ok}/{ok + len(fail)} PASS' + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description='믹서 실행 덱 되읽기 — 덱 텍스트에서 E · ν · CED · dt · step 을 읽어 표 E · E0 · DT · B 를 독립 검산')
    ap.add_argument('--table', nargs=3, action='append', metavar=('KIND', 'OLD', 'NEW'),
                    help='KIND ∈ E · E0 · DT · B — OLD · NEW = in.mixer 경로 (B 는 LC 다음 LH).  여러 번 줄 수 있다')
    ap.add_argument('--json', help='JSON 보고 (도구 sha256 · 허용오차 · 등록 상수 · 덱 sha256 · 생성 명령 · 표 · 실패 항)')
    ap.add_argument('--md', help='사람이 읽는 표 (markdown)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        raise SystemExit(_selftest())
    if not a.table:
        ap.error('--table KIND OLD NEW 가 하나도 없다')
    decks, tables = {}, []
    for kind, old, new in a.table:
        if kind not in KINDS:
            ap.error(f'표 종류 {kind!r} — {KINDS} 중 하나')
        for pth in (old, new):
            if pth not in decks:
                try:
                    decks[pth] = load(pth)
                except OSError as e:
                    ap.error(f'덱을 못 읽는다: {pth} ({e})')
        tables.append(compare(kind, decks[old], decks[new]))
    rep = make_report(decks, tables, sys.argv[1:] if argv is None else argv)
    for T in tables:
        print(f"── 표 {T['kind']:2s} {T['old']} → {T['new']}  {T['verdict']}")
        for f in T['failures'][:6]:
            print(f'     ⛔ {f}')
    if a.json:
        with open(a.json, 'w', encoding='utf-8') as f:
            json.dump(rep, f, ensure_ascii=False, indent=1)
            f.write('\n')
        print(f'→ {a.json}')
    if a.md:
        with open(a.md, 'w', encoding='utf-8') as f:
            f.write(to_markdown(rep))
        print(f'→ {a.md}')
    print(f"\n{sum(T['verdict'] == 'PASS' for T in tables)}/{len(tables)} 표 PASS" + ('' if rep['verdict'] == 'PASS' else '  ⛔ 되읽기 실패 — 봉인 · 발사 근거 없음'))
    raise SystemExit(0 if rep['verdict'] == 'PASS' else 1)


if __name__ == '__main__':
    main()
