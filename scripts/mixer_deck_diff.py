#!/usr/bin/env python3
"""믹서 **실행 덱** 두 벌의 물리 차이를 파싱해 허용목록과 대조한다 (2026-09-27, Codex HB-03).

왜
  골든 해시 (`make_mixer_deck.py` 셀프테스트 ㉟) 는 '같은 생성 결과' 를 잡는 회귀 장치이지 두 **실행 덱**의
  물리 동등성 증명이 아니다.  고-Bo 확장 `LH` 를 이미 돌고 있는 `LC` 와 짝짓는 근거 = *"허용된 CED 요소만
  다르다"* 를 **실제 덱 파일**에서 보이는 것이다 (사전등록 `docs/reviews/mixer_highbo_prereg_20260927.md`).

규칙
  ① 주석을 뺀 모든 논리 명령 (fix · pair_style · timestep · region · insert · dump · run …) 이 **토큰 단위로 같다**.
     단 `fix mC … cohesionEnergyDensity` 한 명령만 따로 본다.  (팔 설명은 주석이라 무시된다.)
  ② CED 행렬 — 타입 번호에 상 이름을 붙인다 (덱의 `particletemplate` 시드 → `make_mixer_deck.TPL_SEED`, 마지막
     타입 = 벽).  달라진 쌍 ⊆ 허용목록, 그리고 허용목록의 쌍은 **전부 실제로 달라야** 한다 (개입이 들어 있는가).
       B (저자 결정 09-27): AM_P–AM_P · AM_P–AM_S · AM_S–AM_S · AM_P–WALL · AM_S–WALL   (AM–AM + AM–벽 공동 개입)
       A (조건부 팔)      : AM_P–AM_P · AM_P–AM_S · AM_S–AM_S                              (AM–AM 단독)
  ③ (--runs, 2026-09-28 Codex 3차 HBR3-07) 시드 서명 — 덱이 **실제로 쓰는** RNG 시드 명령 전부 (fix ID 별:
     insert/* 의 `seed <n>` · particledistribution/* <n> · particletemplate/* <n>).  디렉터리마다
       · 실제 서명 = 그 디렉터리 시드 · 팔로 **생성기 CLI 가 쓰는 덱** (gen_all.sh 인자, 메모리에서 생성) 의 서명
       · 같은 시드의 기준 팔 · 새 팔 서명이 같다
       · 서로 다른 시드 디렉터리에 같은 실제 서명이 없다 (코호트 고유성)
     예정 밖 `<arm>_s*` · `<ref-arm>_s*` 디렉터리는 짝 수에 넣지 않고 '예정 밖' 으로 보고하며 rc 를 1 로 만든다.
     (옛 판은 짝 **안** 만 비교하고 디렉터리 **이름**만 셌다 → seed 32452843 한 쌍을 예정 세 디렉터리에 복사하면 3/3 PASS.)
  ④ (--allow E · EB, 2026-09-30 — 강성 축 사전등록 docs/reviews/mixer_highbo_stiffness_prereg_20260929.md §3 · Codex 7 차 §5 · 9 차 §3)
     E  = 같은 팔 · 다른 강성 (soft → ×14 · ×14 → ×28) **또는** 같은 강성 · dt 만 1/k (E0_ref@dt/2).  달라도 되는 것은
          SE 영률 (영률 줄의 SE 칸만) · timestep · run · dump 간격 · restart 간격 · CED 뿐이고, 각각 **규칙대로만**:
          CED_new = CED_old · (E*_new/E*_old)^(2/3) (쌍별 · 0 은 0 · AM–AM · AM–벽은 E* 불변이라 그대로) · dt = 이 덱의 Rayleigh 규칙
          (경화) 또는 정확히 1/k (dt 경로) · 정착 · 회전 물리 시간 불변 · 덤프 · 체크포인트 = 생성기 규칙 (dt 경로는 정확히 k 배).
          나머지 명령 (ν · 중력 · 이웃 · 삽입 · 기구 …) 은 토큰까지 같다.  SE 영률도 dt 도 같으면 FAIL (빈 E 비교).
     EB = E 와 B 를 **동시에**: LC (한 강성) → LH (다른 강성) 에서 B 다섯 쌍은 증가 · 나머지 쌍은 E 규칙.  B 는 그대로 같은 강성
          LC → LH 전용 (E 필드가 다르면 FAIL).  --expect-deck 를 주면 E · EB 는 새 덱이 재생성 덱과 **전 명령 토큰 동일**이어야 한다
          (필드 규칙의 물리 시간 허용 1e-3 보다 작은 step 변조까지 잡는다 — 셀프테스트 ㉜).
  ⑤ (2026-09-30 · 강성 축 코드 선행조건 2 단계 piece 2) 강성 축 셀 이름 `<E0|LC|LH|LHx10|LHx30|LU212|LU637>_<soft|ref|ref2>[_dthalf][_r<N>]_s<seed>`
     (DEV 증거 README §6 · LHx10 · LHx30 = 10-02 개발 탐색 dev-bo 팔 · §11 · LU212 · LU637 = 10-05 개발 탐색 dev-u 팔 · §12) — parse_cell ·
     cell_expected_deck (이름 → 생성 인자 → 바이트 동일 덱 · ㉟ · ㊸ · U①).
     --runs 는 --ref-arm · --arm 에 **꼬리표** (예 LC_soft_r2 → LC_ref_r2) 를 받아 E · EB · B · U 를 적용하고 폴더마다 덱 전체를 재생성 덱과
     바이트 대조한다 (옛 생성기 팔 이름 LC · LH 는 그대로 A · B 전용).  --cohort dev-e0 · dev-rot · dev-bo · dev-u · confirm = 등록 코호트 (COHORTS ·
     cohort_pairs — 런처 launch_highbo.sh 의 새 단계가 읽는 단일 출처) 의 셀마다 재생성 바이트 동일 · deck_meta.json · 등록 쌍.
  ⑥ (--allow U, 2026-10-05 — 강성 축 사전등록 §12 dev-u) U = **균일 γ 배율**: 같은 강성에서 CED **비영 원소 전부**가 한 공통 배율 r > 1 로
     (0 은 정확히 0 · 퍼짐 max/min − 1 ≤ U_SPREAD_REL = 두 덱 %g 인쇄 반올림) 바뀌고 CED 밖 명령은 토큰까지 같다.  쌍 집합이 아니라 **배율 하나**를
     허용하므로 SE–SE 한 원소만 바뀐 덱 · 배율이 둘인 덱 · 줄어든 덱 · 빈 비교는 FAIL — LC → LU212 · LU637 에서 B · A 는 FAIL (SE 낀 쌍이 목록 밖)
     이고 U 만 PASS 한다 (셀프테스트 U③ · U④).
  ⚠ 이 도구는 덱만 본다 — 실행 바이너리 · 재개 이력 · 판독 규약은 사전등록의 발사 기록이 맡는다.

usage
  python3 scripts/mixer_deck_diff.py <기준 덱 (LC)> <새 덱 (LH)> --allow B [--json out.json]
  python3 scripts/mixer_deck_diff.py --runs <runs 디렉터리> --ref-arm LC --arm LH --allow B    # 같은 시드끼리 전부
  python3 scripts/mixer_deck_diff.py <LC_soft/in.mixer> <LC_ref/in.mixer> --allow E [--expect-deck <재생성 LC_ref 덱>]
  python3 scripts/mixer_deck_diff.py <LC_soft/in.mixer> <LH_ref/in.mixer> --allow EB
  python3 scripts/mixer_deck_diff.py --runs <runs> --ref-arm LC_soft_r8 --arm LC_ref_r8 --allow E --expect-seeds 15485863,86028121,104395301
  python3 scripts/mixer_deck_diff.py <LC_ref_r2/in.mixer> <LU212_ref_r2/in.mixer> --allow U [--expect-deck <재생성 LU212 덱>]
  python3 scripts/mixer_deck_diff.py --runs <runs> --cohort dev-e0 [--json out.json]           # dev-e0 · dev-rot · dev-bo · dev-u · confirm
  python3 scripts/mixer_deck_diff.py --selftest
"""
import argparse
import glob
import json
import math
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
from make_mixer_resume import logical_commands, _tokens      # noqa: E402  덱 논리 명령 파서 — 한 벌만 둔다
from make_mixer_deck import TPL_SEED                          # noqa: E402  템플릿 시드 → 상 이름 (정본)
import make_mixer_deck as _gen                                # noqa: E402  기대 시드 서명의 출처 = 생성기 자신 (HBR3-07)

ALLOW = {
    'B': {('AM_P', 'AM_P'), ('AM_P', 'AM_S'), ('AM_S', 'AM_S'), ('AM_P', 'WALL'), ('AM_S', 'WALL')},
    'A': {('AM_P', 'AM_P'), ('AM_P', 'AM_S'), ('AM_S', 'AM_S')},
}
REL_TOL = 1e-6          # 덱은 CED 를 유효숫자 몇 자리로 찍는다 — 같은 값의 재생성 잡음보다 크고 개입보다 훨씬 작게
#: E · EB 규칙 허용오차 (2026-09-30) — 인쇄 형식에서 비교 **전에** 정한다 (결과를 보고 넓히지 않는다)
E_RULE = dict(
    ced_rel=1.0e-5,          # CED %g 6 유효숫자 두 값 — 쌍별 규칙 대조
    dt_print_rel=5.0e-4,     # timestep .4g — 생성기는 반올림 전 dt 로 step 을 센다 (물리 시간 대조: 2 × 이 값 × T + 반올림 step)
    rayleigh_rel=5.05e-4,    # 덱 dt (.4g) ↔ 덱 값 (반지름 .6g) 으로 다시 낸 Rayleigh dt
    exact_rel=1e-12,         # dt 경로 (정수배)
)
_E_VAR = {'timestep': {1}, 'run': {1}, 'restart': {1}, 'dump': {4}}      # E 에서 달라도 되는 토큰 위치 (값은 규칙으로 따로 본다)
#: U 규칙 허용오차 (2026-10-05 · dev-u) — 인쇄 형식에서 비교 **전에** 정한다.  CED 는 %g 6 유효숫자 ⇒ 원소 하나의 배율 오차 ≤ E_RULE['ced_rel'] (1e-5)
#:   ⇒ 같은 참 배율인 두 원소의 배율은 max/min − 1 ≤ 2 × 1e-5.  그보다 크면 배율이 하나가 아니다.
U_SPREAD_REL = 2.0 * E_RULE['ced_rel']


def _dump_rule(n_run):
    """생성기 run_steps 의 덤프 간격 규칙 **사본** (셀프테스트 ㉞ 가 생성기와 대조)."""
    return max(1000, n_run // 200)


def _restart_rule(n_fill, n_run):
    """생성기 run_steps 의 체크포인트 간격 규칙 사본."""
    return max(50_000, min(200_000, (n_run or 2 * n_fill) // 20))


def _e_fields(p):
    """parse_deck 결과 → 강성 축 필드 (영률 · ν (타입 순) · dt · run · 덤프 · 체크포인트 · Drum 주기 · 템플릿 (반지름, 밀도))."""
    f = dict(E=None, nu=None, dt=None, dt_txt=None, runs=[], dump=None, restart=None, period=None, tpl={})
    for t in p['cmds']:
        if t[0] == 'fix' and len(t) > 5 and t[3] == 'property/global' and t[5] == 'peratomtype' and t[4] in ('youngsModulus', 'poissonsRatio'):
            f['E' if t[4] == 'youngsModulus' else 'nu'] = [float(x) for x in t[6:]]
        elif t[0] == 'timestep':
            f['dt_txt'], f['dt'] = t[1], float(t[1])
        elif t[0] == 'run':
            f['runs'].append(int(t[1]))
        elif t[0] == 'dump' and len(t) > 4:
            f['dump'] = int(t[4])
        elif t[0] == 'restart':
            f['restart'] = int(t[1])
        elif t[0] == 'fix' and len(t) > 5 and t[3] == 'move/mesh' and t[5] == 'Drum' and 'period' in t:
            f['period'] = float(t[t.index('period') + 1])
        elif t[0] == 'fix' and len(t) > 6 and t[3].startswith('particletemplate/') and 'atom_type' in t:
            f['tpl'][int(t[t.index('atom_type') + 1])] = (float(t[t.index('radius') + 2]) if 'radius' in t else None,
                                                          float(t[t.index('density') + 2]) if 'density' in t else None)
    return f


def _rayleigh_dt(f):
    """생성기 plan() 의 Rayleigh 시간스텝 규칙 **사본** — 덱의 영률 · ν · 반지름 · 밀도에서 → (dt, 정한 타입).
    ⚠ 이 대조가 없으면 SE 를 경화하고 dt 를 다시 안 센 덱 (soft 0.7055 µs = 경화 SE 한계 0.3132 µs 의 2.25 배) 이 E 필드 규칙을 전부 통과한다 (㉙)."""
    best = None
    for k, (r, rho) in sorted(f['tpl'].items()):
        if r is None or rho is None:
            continue
        E, nu = f['E'][k - 1], f['nu'][k - 1]
        G = E / (2.0 * (1.0 + nu))
        dt = 0.2 * math.pi * r * math.sqrt(rho / G) / (0.1631 * nu + 0.8766)
        if best is None or dt < best[0]:
            best = (dt, k)
    return best


def _estar(Ei, nui, Ej, nuj):
    """E*_ij = [(1−ν_i²)/E_i + (1−ν_j²)/E_j]⁻¹ — 벽은 덱에 선언된 벽 영률 · ν."""
    return 1.0 / ((1.0 - nui ** 2) / Ei + (1.0 - nuj ** 2) / Ej)


def parse_deck(text):
    """덱 텍스트 → dict(cmds=[비-CED 토큰 목록…], ced=(n, 값 목록), names={타입: 상 이름})."""
    cmds, ced, names, ntypes, head = [], None, {}, None, None
    inv = {v: k for k, v in TPL_SEED.items()}
    for _, blk in logical_commands(text):
        t = _tokens(blk)
        if not t:
            continue
        if t[0] == 'fix' and len(t) > 5 and t[4] == 'cohesionEnergyDensity':
            if ced is not None:
                raise ValueError('cohesionEnergyDensity 명령이 둘 이상이다')
            n = int(t[6])
            vals = [float(x) for x in t[7:]]
            if len(vals) != n * n:
                raise ValueError(f'CED 행렬 값 {len(vals)} 개 ≠ {n}×{n}')
            ced = (n, vals)
            head = t[:7]                            # fix <id> <group> property/global cohesionEnergyDensity peratomtypepair <n>
            continue
        if t[0] == 'create_box':
            ntypes = int(t[1])
        if t[0] == 'fix' and len(t) > 6 and t[3].startswith('particletemplate/') and 'atom_type' in t:
            seed = int(t[4])
            names[int(t[t.index('atom_type') + 1])] = inv.get(seed, f'?seed{seed}')
        cmds.append(t)
    if ced is None:
        raise ValueError('덱에 cohesionEnergyDensity 가 없다')
    if ntypes is not None:
        names.setdefault(ntypes, 'WALL')
    return dict(cmds=cmds, ced=ced, names=names, ced_head=head)


def diff_decks(text_ref, text_new, allow='B', expect=None, expect_text=None):
    """두 덱 → 판정 dict(verdict, non_ced_diffs, changed, outside, missing, wrong_direction, target_mismatch, table).

    ★ allow ∈ E · EB (2026-09-30) 는 _diff_decks_E 로 — 강성 축 규칙 (모듈 설명 ④).  `expect_text` = 재생성 덱 텍스트 (E · EB 는 전 명령 대조).
      A · B 경로는 아래 그대로다 (expect = CED 목표만).

    2026-09-27 저녁 (Codex HBR2-05) 넓힌 것: CED 명령 머리 (fix id · group · style · n) 동일 · **양쪽** 행렬 유한 · 비음수 ·
    대칭 · 허용 쌍은 **증가** 방향 (고-Bo 확장) · `expect` = (n, 값) 을 주면 새 행렬이 그 목표와 1e-5 안에서 같아야 한다.
    ⚠ PASS 는 **덱 텍스트의 계약**이다 — 실제 STL 내용 · 바이너리 · 실행 환경은 발사 기록 (§2-5) 이 따로 묶는다.
    """
    if allow in ('E', 'EB'):
        return _diff_decks_E(text_ref, text_new, allow, expect_text=expect_text)
    if allow == 'U':
        return _diff_decks_U(text_ref, text_new, expect=expect)
    a, b = parse_deck(text_ref), parse_deck(text_new)
    out = dict(allow=allow, non_ced_diffs=[], changed=[], outside=[], missing=[], wrong_direction=[], target_mismatch=[], table=[])
    if len(a['cmds']) != len(b['cmds']):
        out['non_ced_diffs'].append(f'명령 수 {len(a["cmds"])} ≠ {len(b["cmds"])}')
    for i, (x, y) in enumerate(zip(a['cmds'], b['cmds'])):
        if x != y:
            out['non_ced_diffs'].append(f'#{i}: {" ".join(x)[:120]}  ⇄  {" ".join(y)[:120]}')
    if a['names'] != b['names']:
        out['non_ced_diffs'].append(f'타입 이름 {a["names"]} ≠ {b["names"]}')
    if a['ced_head'] != b['ced_head']:
        out['non_ced_diffs'].append(f'CED 명령 머리가 다르다: {" ".join(a["ced_head"])}  ⇄  {" ".join(b["ced_head"])}')
    (na, va), (nb, vb) = a['ced'], b['ced']
    if na != nb:
        out['non_ced_diffs'].append(f'CED 행렬 크기 {na} ≠ {nb}')
        out['verdict'] = 'FAIL'
        return out
    nm = [a['names'].get(k + 1, f't{k + 1}') for k in range(na)]
    for lab, v_ in (('기준', va), ('새', vb)):
        nbad = sum(not math.isfinite(x) for x in v_)
        if nbad:
            out['non_ced_diffs'].append(f'{lab} 덱 CED 에 비유한 값 {nbad} 개')
        if any(math.isfinite(x) and x < 0 for x in v_):
            out['non_ced_diffs'].append(f'{lab} 덱 CED 에 음수')
        for i in range(na):
            for j in range(i + 1, na):
                p_, q_ = v_[i * na + j], v_[j * na + i]
                if math.isfinite(p_) and math.isfinite(q_) and abs(p_ - q_) > REL_TOL * max(abs(p_), 1e-30):
                    out['non_ced_diffs'].append(f'{lab} 덱 CED 비대칭 ({nm[i]},{nm[j]}): {p_:.6g} vs {q_:.6g}')
    changed, vals = set(), {}
    for i in range(na):
        for j in range(na):
            x, y = va[i * na + j], vb[i * na + j]
            pair = tuple(sorted((nm[i], nm[j])))
            if (math.isfinite(x) and math.isfinite(y) and abs(y - x) > REL_TOL * max(abs(x), abs(y), 1e-30)) or (math.isfinite(x) != math.isfinite(y)):
                changed.add(pair)
            if j >= i:
                vals[pair] = (x, y)
                out['table'].append(dict(pair=f'{nm[i]}–{nm[j]}', ref=x, new=y,
                                         ratio=(y / x) if x else (float('inf') if y else 1.0)))
    allowed = ALLOW[allow]
    out['changed'] = sorted(changed)
    out['outside'] = sorted(changed - allowed)
    out['missing'] = sorted(allowed - changed)
    out['wrong_direction'] = sorted(p_ for p_ in (changed & allowed)
                                    if p_ in vals and math.isfinite(vals[p_][1]) and vals[p_][1] < vals[p_][0])
    if expect is not None:
        ne, ve = expect
        if ne != nb:
            out['target_mismatch'].append(f'목표 행렬 크기 {ne} ≠ {nb}')
        else:
            for i in range(na):
                for j in range(i, na):
                    x, y = ve[i * na + j], vb[i * na + j]
                    if not (math.isfinite(x) and math.isfinite(y)) or abs(y - x) > 1e-5 * max(abs(x), abs(y), 1e-30):
                        out['target_mismatch'].append(f'{nm[i]}–{nm[j]}: 목표 {x:.6g} vs 새 {y:.6g}')
    out['verdict'] = 'PASS' if not (out['non_ced_diffs'] or out['outside'] or out['missing']
                                    or out['wrong_direction'] or out['target_mismatch']) else 'FAIL'
    return out


def _diff_decks_E(text_ref, text_new, allow, expect_text=None):
    """E · EB 판정 (2026-09-30) — 모듈 설명 ④.  반환 = diff_decks 와 같은 키 + e_rule (규칙 위반) · e_case (경화 ×F · dt ×1/k)."""
    a, b = parse_deck(text_ref), parse_deck(text_new)
    out = dict(allow=allow, non_ced_diffs=[], changed=[], outside=[], missing=[], wrong_direction=[], target_mismatch=[], table=[],
               e_rule=[], e_case=None)
    er = out['e_rule']
    fa, fb = _e_fields(a), _e_fields(b)
    if a['names'] != b['names']:
        out['non_ced_diffs'].append(f'타입 이름 {a["names"]} ≠ {b["names"]}')
    if a['ced_head'] != b['ced_head']:
        out['non_ced_diffs'].append(f'CED 명령 머리가 다르다: {" ".join(a["ced_head"])}  ⇄  {" ".join(b["ced_head"])}')
    se = [k for k, v in a['names'].items() if v == 'SE']
    need = ('E', 'nu', 'dt', 'dump', 'restart', 'period')
    if len(se) != 1 or any(fx[k] is None for fx in (fa, fb) for k in need):
        out['non_ced_diffs'].append(f'E 필드를 못 읽었다 (SE 타입 {se} · {[k for fx in (fa, fb) for k in need if fx[k] is None]})')
        out['verdict'] = 'FAIL'
        return out
    se = se[0]
    #  ① 명령 — E 허용 위치 (영률 줄은 **SE 칸만**) 를 빼고 토큰까지 같다
    if len(a['cmds']) != len(b['cmds']):
        out['non_ced_diffs'].append(f'명령 수 {len(a["cmds"])} ≠ {len(b["cmds"])}')
    for i, (x, y) in enumerate(zip(a['cmds'], b['cmds'])):
        var = set(_E_VAR.get(x[0], ()))
        if x[0] == 'fix' and len(x) > 5 and x[3] == 'property/global' and x[4] == 'youngsModulus':
            var = {5 + se}
        if len(x) != len(y) or any(p_ != q_ for j, (p_, q_) in enumerate(zip(x, y)) if j not in var):
            out['non_ced_diffs'].append(f'#{i}: {" ".join(x)[:120]}  ⇄  {" ".join(y)[:120]}')
    (na, va), (nb, vb) = a['ced'], b['ced']
    if na != nb or len(fa['E']) != na or len(fb['E']) != nb or len(fa['nu']) != na:
        out['non_ced_diffs'].append(f'CED {na}×{na} · {nb}×{nb} ↔ 영률 {len(fa["E"])} · {len(fb["E"])} · ν {len(fa["nu"])} 개가 안 맞는다')
        out['verdict'] = 'FAIL'
        return out
    nm = [a['names'].get(k + 1, f't{k + 1}') for k in range(na)]
    for lab, v_ in (('기준', va), ('새', vb)):
        if any(not math.isfinite(x) for x in v_):
            out['non_ced_diffs'].append(f'{lab} 덱 CED 에 비유한 값')
        if any(math.isfinite(x) and x < 0 for x in v_):
            out['non_ced_diffs'].append(f'{lab} 덱 CED 에 음수')
        for i in range(na):
            for j in range(i + 1, na):
                if v_[i * na + j] != v_[j * na + i]:
                    out['non_ced_diffs'].append(f'{lab} 덱 CED 비대칭 ({nm[i]},{nm[j]})')
    #  ② 경우 — 경화 (SE 영률 다름) · dt 경로 (영률 같고 dt 정확히 1/k) · 없음 (FAIL)
    F = fb['E'][se - 1] / fa['E'][se - 1]
    Ra, Rb = fa['runs'], fb['runs']
    struct = len(Ra) == len(Rb) == 4 and Ra[0] == Rb[0] == 1 and Ra[1] == Ra[2] and Rb[1] == Rb[2]
    if not struct:
        er.append(f'run 구조 {Ra} → {Rb} ≠ [1, F, F, N] (삽입 · 정착 ×2 · 회전)')
    rule_a = _rayleigh_dt(fa)
    if rule_a is None or abs(fa['dt'] / rule_a[0] - 1.0) > E_RULE['rayleigh_rel']:
        er.append(f'기준 덱 dt {fa["dt_txt"]} ≠ Rayleigh 규칙 {rule_a[0] if rule_a else float("nan"):.6g} s')
    if F != 1.0:
        out['e_case'] = f'경화 ×{F:g} (SE {fa["E"][se - 1]:g} → {fb["E"][se - 1]:g})'
        rule_b = _rayleigh_dt(fb)
        if rule_b is None or abs(fb['dt'] / rule_b[0] - 1.0) > E_RULE['rayleigh_rel']:
            er.append(f'새 덱 dt {fb["dt_txt"]} ≠ Rayleigh 규칙 {rule_b[0] if rule_b else float("nan"):.6g} s (타입 {rule_b[1] if rule_b else "?"} 가 정함) — '
                      f'경화했으면 dt 를 새 영률로 다시 세야 한다 (적분 안정)')
        if struct:
            ts_a, ts_b = 2 * Ra[1] * fa['dt'], 2 * Rb[1] * fb['dt']
            tol_s = 2 * E_RULE['dt_print_rel'] * max(ts_a, ts_b) + fa['dt'] + fb['dt']
            if abs(ts_a - ts_b) > tol_s:
                er.append(f'물리 시간 — 정착 2F·dt {ts_a:.9g} → {ts_b:.9g} s (허용 {tol_s:.3g})')
            tr_a, tr_b = Ra[3] * fa['dt'], Rb[3] * fb['dt']
            tol_r = 2 * E_RULE['dt_print_rel'] * max(tr_a, tr_b) + 0.5 * (fa['dt'] + fb['dt'])
            if abs(tr_a - tr_b) > tol_r:
                er.append(f'물리 시간 — 회전 N·dt {tr_a:.9g} → {tr_b:.9g} s (허용 {tol_r:.3g})')
            for lab, fx, R in (('기준', fa, Ra), ('새', fb, Rb)):
                if fx['dump'] != _dump_rule(R[3]):
                    er.append(f'{lab} 덱 덤프 간격 {fx["dump"]} ≠ 생성기 규칙 {_dump_rule(R[3])}')
                if fx['restart'] != _restart_rule(R[1], R[3]):
                    er.append(f'{lab} 덱 체크포인트 간격 {fx["restart"]} ≠ 생성기 규칙 {_restart_rule(R[1], R[3])}')
    elif fb['dt'] != fa['dt']:
        kr = fa['dt'] / fb['dt']
        k = int(round(kr))
        out['e_case'] = f'dt ×1/{k} (영률 같음)'
        if k < 2 or abs(fb['dt'] * k / fa['dt'] - 1.0) > E_RULE['exact_rel']:
            er.append(f'dt {fa["dt_txt"]} → {fb["dt_txt"]} (비 {kr:.12g}) — 정확히 1/k (k 정수 ≥ 2) 가 아니다')
        if struct and Rb[1:] != [k * x for x in Ra[1:]]:
            er.append(f'dt ×1/{k}: run 이 정확히 {k} 배가 아니다 ({Ra} → {Rb} · run 1 은 그대로)')
        if fb['dump'] != k * fa['dump']:
            er.append(f'dt ×1/{k}: 덤프 간격 {fa["dump"]} → {fb["dump"]} (정확히 {k} 배여야 덤프 시각이 같다)')
        if struct and fb['restart'] != _restart_rule(Rb[1], Rb[3]):
            er.append(f'새 덱 체크포인트 간격 {fb["restart"]} ≠ 생성기 규칙 {_restart_rule(Rb[1], Rb[3])}')
    else:
        er.append('E 비교인데 SE 영률도 dt 도 같다 — 강성 · dt 변화가 없다 (같은 강성의 LC↔LH 는 --allow B)')
    #  ③ CED — 쌍별 규칙 (EB 의 B 다섯 쌍은 증가)
    changed = set()
    for i in range(na):
        for j in range(i, na):
            x, y = va[i * na + j], vb[i * na + j]
            pair = tuple(sorted((nm[i], nm[j])))
            ek = _estar(fb['E'][i], fb['nu'][i], fb['E'][j], fb['nu'][j]) / _estar(fa['E'][i], fa['nu'][i], fa['E'][j], fa['nu'][j])
            want = x * ek ** (2.0 / 3.0) if x else 0.0
            in_b = allow == 'EB' and pair in ALLOW['B']
            if math.isfinite(x) and math.isfinite(y) and abs(y - x) > REL_TOL * max(abs(x), abs(y), 1e-30):
                changed.add(pair)
            out['table'].append(dict(pair=f'{nm[i]}–{nm[j]}', ref=x, new=y, rule=None if in_b else want,
                                     ratio=(y / x) if x else None, abs_diff=y - x))     # 0 기준 비 = N/A (0/0 을 1 로 만들지 않는다 · Codex 9 차 §3)
            if in_b:
                if not (math.isfinite(y) and y > x * (1.0 + REL_TOL)):
                    (out['wrong_direction'] if y < x else out['missing']).append(pair)
            elif x == 0.0:
                if y != 0.0:
                    er.append(f'{nm[i]}–{nm[j]}: 0 → {y:g} (0 은 정확히 0 이어야 한다)')
            elif not (math.isfinite(y) and abs(y / want - 1.0) <= E_RULE['ced_rel']):
                er.append(f'{nm[i]}–{nm[j]}: {x:g} → {y:g} (쌍별 규칙 {want:.6g} · E* ×{ek:.6g} → CED ×{ek ** (2.0 / 3.0):.6g})')
    out['changed'] = sorted(changed)
    #  ④ 재생성 덱 — 전 명령 토큰 동일 (CED 포함)
    if expect_text is not None:
        pe = parse_deck(expect_text)
        if pe['cmds'] != b['cmds'] or pe['ced'] != b['ced'] or pe['ced_head'] != b['ced_head']:
            bad = [f'#{i}: {" ".join(x)[:100]}  ⇄  {" ".join(y)[:100]}' for i, (x, y) in enumerate(zip(pe['cmds'], b['cmds'])) if x != y]
            if len(pe['cmds']) != len(b['cmds']):
                bad.append(f'명령 수 {len(pe["cmds"])} ≠ {len(b["cmds"])}')
            if pe['ced'] != b['ced'] or pe['ced_head'] != b['ced_head']:
                bad.append('CED 행렬 (또는 명령 머리) 이 재생성 덱과 다르다')
            out['target_mismatch'] += bad or ['재생성 덱과 다르다']
    out['verdict'] = 'PASS' if not (out['non_ced_diffs'] or er or out['missing'] or out['wrong_direction']
                                    or out['target_mismatch']) else 'FAIL'
    return out


def _diff_decks_U(text_ref, text_new, expect=None):
    """U 판정 (2026-10-05 · 개발 탐색 dev-u · 강성 축 사전등록 §12) — **균일 γ 배율**.  반환 = diff_decks 와 같은 키 + u_rule · u_ratio · u_spread.

    ① CED 밖 명령 (E · ν · timestep · run · 덤프 · 기하 · 시드 · 삽입) 은 토큰까지 같다 — B 와 같은 비교 (같은 강성).
    ② CED 명령 머리 · 행렬 크기 같다 · **양쪽** 행렬 유한 · 비음수 · 대칭.
    ③ CED **비영 원소 전부**가 한 공통 배율 r 로 바뀐다 — 원소 배율의 퍼짐 max/min − 1 ≤ U_SPREAD_REL (두 덱의 %g 인쇄 반올림 · 비교 전에 정함) ·
       0 은 정확히 0 (벽–벽) · r > 1 (같은 γ 세계를 **키운다** — 줄어든 덱 = 방향 반대 · r = 1 = 빈 비교).
    ④ `expect` = (n, 값) 을 주면 새 행렬이 그 목표와 1e-5 안에서 같다 (B 와 같은 목표 대조).
    A · B 처럼 **쌍 집합**을 허용하는 목록이 아니라 **배율 하나**를 허용한다 — 한 원소만 바뀐 덱 (S 형) · 배율이 둘인 덱 · LH 사다리의 덱은 FAIL."""
    a, b = parse_deck(text_ref), parse_deck(text_new)
    out = dict(allow='U', non_ced_diffs=[], changed=[], outside=[], missing=[], wrong_direction=[], target_mismatch=[], table=[],
               u_rule=[], u_ratio=None, u_spread=None)
    ur = out['u_rule']
    if len(a['cmds']) != len(b['cmds']):
        out['non_ced_diffs'].append(f'명령 수 {len(a["cmds"])} ≠ {len(b["cmds"])}')
    for i, (x, y) in enumerate(zip(a['cmds'], b['cmds'])):
        if x != y:
            out['non_ced_diffs'].append(f'#{i}: {" ".join(x)[:120]}  ⇄  {" ".join(y)[:120]}')
    if a['names'] != b['names']:
        out['non_ced_diffs'].append(f'타입 이름 {a["names"]} ≠ {b["names"]}')
    if a['ced_head'] != b['ced_head']:
        out['non_ced_diffs'].append(f'CED 명령 머리가 다르다: {" ".join(a["ced_head"])}  ⇄  {" ".join(b["ced_head"])}')
    (na, va), (nb, vb) = a['ced'], b['ced']
    if na != nb:
        out['non_ced_diffs'].append(f'CED 행렬 크기 {na} ≠ {nb}')
        out['verdict'] = 'FAIL'
        return out
    nm = [a['names'].get(k + 1, f't{k + 1}') for k in range(na)]
    for lab, v_ in (('기준', va), ('새', vb)):
        nbad = sum(not math.isfinite(x) for x in v_)
        if nbad:
            out['non_ced_diffs'].append(f'{lab} 덱 CED 에 비유한 값 {nbad} 개')
        if any(math.isfinite(x) and x < 0 for x in v_):
            out['non_ced_diffs'].append(f'{lab} 덱 CED 에 음수')
        for i in range(na):
            for j in range(i + 1, na):
                p_, q_ = v_[i * na + j], v_[j * na + i]
                if math.isfinite(p_) and math.isfinite(q_) and abs(p_ - q_) > REL_TOL * max(abs(p_), 1e-30):
                    out['non_ced_diffs'].append(f'{lab} 덱 CED 비대칭 ({nm[i]},{nm[j]}): {p_:.6g} vs {q_:.6g}')
    changed, ratios = set(), {}
    for i in range(na):
        for j in range(i, na):
            x, y = va[i * na + j], vb[i * na + j]
            pair, lab = tuple(sorted((nm[i], nm[j]))), f'{nm[i]}–{nm[j]}'
            if (math.isfinite(x) and math.isfinite(y) and abs(y - x) > REL_TOL * max(abs(x), abs(y), 1e-30)) or (math.isfinite(x) != math.isfinite(y)):
                changed.add(pair)
            out['table'].append(dict(pair=lab, ref=x, new=y, ratio=(y / x) if x else (float('inf') if y else 1.0)))
            if x == 0.0:
                if y != 0.0:
                    ur.append(f'{lab}: 0 → {y:g} (0 은 정확히 0 이어야 한다)')
            elif math.isfinite(x) and x > 0.0 and math.isfinite(y) and y > 0.0:
                ratios[lab] = y / x
            else:
                ur.append(f'{lab}: {x:g} → {y:g} (배율을 낼 수 없다 — 비유한 · 0 · 음수)')
    out['changed'] = sorted(changed)
    if ratios:
        lo, hi = min(ratios.values()), max(ratios.values())
        med = sorted(ratios.values())[len(ratios) // 2]
        out['u_ratio'] = math.exp(sum(math.log(v) for v in ratios.values()) / len(ratios))      # 기하평균 (보고) · 판정 = 퍼짐 + 방향
        out['u_spread'] = hi / lo - 1.0
        if out['u_spread'] > U_SPREAD_REL:
            far = sorted(ratios, key=lambda k_: -abs(math.log(ratios[k_] / med)))
            far = [k_ for k_ in far if abs(ratios[k_] / med - 1.0) > U_SPREAD_REL] or far[:1]
            ur.append(f'배율이 하나가 아니다 — 퍼짐 {out["u_spread"]:.3g} > 허용 {U_SPREAD_REL:.0e} (×{lo:.7g} … ×{hi:.7g} · 중앙값 ×{med:.7g} 에서 먼 쌍 '
                      + ', '.join(f'{k_} ×{ratios[k_]:.7g}' for k_ in far[:4]) + ')')
        if med < 1.0 - REL_TOL:
            out['wrong_direction'].append(f'공통 배율 ×{med:.7g} < 1 — U 는 같은 γ 세계를 키운다 (증가여야 한다)')
        elif med <= 1.0 + REL_TOL:
            out['missing'].append(f'공통 배율 ×{med:.7g} = 1 — 개입 없음 (빈 비교)')
    else:
        ur.append('비영 CED 원소가 없다 — 배율을 낼 수 없다 (점착 0 팔 · 깨진 덱은 U 비교 대상 아님)')
    if expect is not None:
        ne, ve = expect
        if ne != nb:
            out['target_mismatch'].append(f'목표 행렬 크기 {ne} ≠ {nb}')
        else:
            for i in range(na):
                for j in range(i, na):
                    x, y = ve[i * na + j], vb[i * na + j]
                    if not (math.isfinite(x) and math.isfinite(y)) or abs(y - x) > 1e-5 * max(abs(x), abs(y), 1e-30):
                        out['target_mismatch'].append(f'{nm[i]}–{nm[j]}: 목표 {x:.6g} vs 새 {y:.6g}')
    out['verdict'] = 'PASS' if not (out['non_ced_diffs'] or ur or out['missing'] or out['wrong_direction'] or out['target_mismatch']) else 'FAIL'
    return out


# ══ 시드 서명 (2026-09-28, Codex 3차 HBR3-07) ══════════════════════════════════════════════════════════════
#  왜: 짝 비교는 짝 **안** 에서 같은지만 보고, --runs 의 n/N 은 **디렉터리 이름**만 셌다.  seed 32452843 의 LC/LH 한 쌍을
#    예정 세 디렉터리 (s32452843 · s49979687 · s67867967) 에 복사하고 --expect-deck 까지 주어도 3/3 PASS · rc 0 이었다
#    (실제 고유 덱 2 개).  예정 밖 디렉터리는 4/3 으로 셌다.  ⇒ 덱이 실제로 쓰는 RNG 시드 명령을 읽어 ① 생성기가 그 시드 ·
#    팔로 내는 기대 서명과 같은가 ② 같은 시드의 기준 팔 · 새 팔 서명이 같은가 ③ 서로 다른 시드 디렉터리에 같은 서명이
#    없는가 를 보고, 예정 밖 디렉터리는 센 수에서 빼고 '예정 밖' 으로 rc 1.
#  ⚠ 시드 유도 (삽입 B = 다음 소수 · pdd 시드 · 템플릿 시드) 를 여기서 **다시 짜지 않는다** — 기대값은 생성기가 쓰는 덱을
#    메모리에서 만들어 거기서 뽑는다 (셀프테스트 ㉒ 가 CLI 출력과 바이트 동일을 강제).
SEED_STYLES = ('insert/', 'particledistribution/', 'particletemplate/')
#: 생성기 CLI 인자 — dem_scripts/mixer_20260921/gen_all.sh 의 N_TOTAL · CGF · REV 기본값 (--arm · --seed 는 디렉터리에서).
#  ⚠ 시드 명령은 이 셋에 의존하지 않지만, "생성기가 쓰는 덱" 을 그대로 재현하려고 같은 값으로 부른다.
GEN_ARGS = dict(n_total=100000, cgf=151.4, revolutions=8)


def seed_signature(text):
    """덱 텍스트 → 실제로 쓰는 RNG 시드 전부 = ((fix ID, style, 시드), …) 덱 순서.

    insert/* 는 `seed <n>` 키워드, particledistribution/* · particletemplate/* 는 style 바로 뒤 첫 인자.
    정수가 아니면 (변수 치환 등) 문자열 그대로, 시드가 없으면 None — 어느 쪽이든 기대 서명과 안 맞아 FAIL 이다 (fail-closed).
    """
    sig = []
    for _, blk in logical_commands(text):
        t = _tokens(blk)
        if len(t) < 4 or t[0] != 'fix' or not t[3].startswith(SEED_STYLES):
            continue
        if t[3].startswith('insert/'):
            k = t.index('seed', 4) if 'seed' in t[4:] else None
            v = t[k + 1] if k is not None and k + 1 < len(t) else None
        else:
            v = t[4] if len(t) > 4 else None
        sig.append((t[1], t[3], int(v) if v is not None and re.fullmatch(r'[0-9]+', v) else v))
    return tuple(sig)


def sig_summary(sig):
    """서명 → 한 줄 (style 별로 묶어 덱 순서): 'particletemplate/sphere pt1=10487 … · insert/pack insA=… insB=…'."""
    if sig is None:
        return '(in.mixer 없음)'
    groups = {}
    for f, st, v in sig:
        groups.setdefault(st, []).append(f'{f}={v}')
    return ' · '.join(f'{st} {" ".join(xs)}' for st, xs in groups.items()) or '(시드 명령 없음)'


def _sig_delta(got, want, label='기대'):
    """두 서명에서 다른 칸만 → ['insA(insert/pack) 15485863 (기대 32452843)', …]."""
    g, w = {}, {}
    for f, st, v in got:
        g.setdefault((f, st), []).append(v)
    for f, st, v in want:
        w.setdefault((f, st), []).append(v)
    out = [f'{k[0]}({k[1]}) {"/".join(map(str, g.get(k, ["없음"])))} ({label} {"/".join(map(str, w.get(k, ["없음"])))})'
           for k in dict.fromkeys(list(w) + list(g)) if g.get(k) != w.get(k)]
    return out or (['시드 명령 순서가 다르다'] if tuple(got) != tuple(want) else [])


def _sig_json(sig):
    return None if sig is None else [dict(fix=f, style=st, seed=v) for f, st, v in sig]


def expected_deck(arm, seed, n_total=GEN_ARGS['n_total'], cgf=GEN_ARGS['cgf'], revolutions=GEN_ARGS['revolutions'],
                  stiffen_se=1.0, hold_bo_pairwise=False, dt_factor=1.0):
    """생성기 CLI `make_mixer_deck.py --n-total … --cgf … --arm <arm> --seed <seed> --revolutions … [--stiffen-se F]
    [--hold-bo-pairwise] [--dt-factor X]` 가 쓰는 in.mixer 와 **같은 텍스트**를 메모리에서 만든다.  호출은 그 CLI 의 main 그대로다:
    --fr 기본 FR_ANCHOR · --rpm 없음 · --allow-off-band 없음 · --settle-s 없음 · --baffles 0 · --baffle-h 0.10
    (셀프테스트 ㉒ = CLI 출력과 바이트 동일 · ㉟ = 커밋된 DEV 강성 덱 14 와 바이트 동일).
    ★ 2026-09-30 (piece 2) — 강성 인자 (stiffen_se · hold_bo_pairwise · dt_factor) 를 CLI 와 같은 자리로 넘긴다.  기본값 = 옛 호출 그대로
      (중립 옵션이면 생성기가 바이트 동일 덱을 낸다 — 생성기 ST①)."""
    p = _gen.plan(n_total, cgf=cgf, stiffen_se=stiffen_se)
    rpm = _gen.resolve_rpm(p['R'], _gen.FR_ANCHOR, None, False)
    return _gen.deck(p, rpm, revolutions, arm=arm, settle_s=None, seed=seed, n_baffles=0, baffle_h=0.10,
                     hold_bo_pairwise=hold_bo_pairwise, dt_factor=dt_factor)


# ══ 강성 축 셀 이름 · 등록 코호트 (2026-09-30 · 코드 선행조건 2 단계 piece 1 · 2) ══════════════════════════════════════════
#  이름 규약 (docs/data/mixer_highbo_dev_decks_20260930/README.md §6) — `<팔>_<수준>[_dthalf][_r<바퀴>]_s<seed>`
#    팔 E0 · LC · LH (+ 10-02 dev-bo 팔 LHx10 · LHx30 · 10-05 dev-u 팔 LU212 · LU637 = 생성기 팔 이름 그대로) / 수준 soft (×1) · ref (×20 · v2.6) · ref2 (×40) / `_dthalf` = --dt-factor 0.5 /
#    `_r<N>` = --revolutions N
#    (LC · LH 는 필수 · E0 는 금지 = 회전 0) / seed = 십진 (앞자리 0 없음).  이름 → 생성 인자는 build.sh 의 gen_cmd 와 같다:
#    경화 (ref · ref2) 면 --stiffen-se F --hold-bo-pairwise · soft 는 강성 옵션 없음 (§3 "생성기 옵션 --stiffen-se 14 --hold-bo-pairwise").
#  NP 프로브 폴더 = `npprobe<NP>_<셀 이름>` — 같은 덱 (사전등록 §8-2 ②: "NP 프로브 = E0_ref 첫 시드를 NP 5/10/20 으로 1 h 씩 (같은 덱 ·
#    처리량만 · 확인 자료 전용 금지)").  parse_cell 은 프로브를 **거부**한다 (자료 셀이 아니다) — parse_run 만 받는다.
STIFF_LEVELS = {'soft': 1.0, 'ref': 20.0, 'ref2': 40.0}           # 사전등록 §3 v2.6 (09-30 밤 · 1저자 비준) — E_ref = SE ×20 · E_ref2 = SE ×40 (옛 v2.5: ×14 · ×28 = DEV7 ×14 실측 뒤 개정)
#: ★ 셀 이름의 팔 (생성기 ARMS 의 이름 그대로) — 2026-10-02 개발 탐색 dev-bo 팔 둘을 더했다 (사전등록 §11 v2.8 · LH 의 AM–AM Bo_code ×10 · ×30).
#:   ⚠ 한 벌이어야 한다: dem_scripts/mixer_20260921/run_all.sh · resume_all.sh 의 강성 축 셀 정규식이 같은 목록을 쓴다 (test_launcher.sh DB⑧ 가 대조) —
#:   옛 판은 그 정규식이 E0 · LC · LH 만 알아 LHx10_* · LHx30_* 를 로컬로 띄우고 잇는 구멍이 있었다 (DB⑦ 재현).
DEV_BO_ARMS = ('LHx10', 'LHx30')
#: ★ 2026-10-05 개발 탐색 dev-u 팔 둘 (사전등록 §12 v2.9 · LC 의 9 비영 CED 를 한 배율 ×10 · ×14.422496 로 = 균일 γ 배율) — 같은 한 벌 규칙 (DU⑧).
DEV_U_ARMS = ('LU212', 'LU637')
STIFF_ARMS = ('E0', 'LC', 'LH') + DEV_BO_ARMS + DEV_U_ARMS
_TAG_PAT = r'(' + '|'.join(sorted(STIFF_ARMS, key=len, reverse=True)) + r')_(soft|ref|ref2)(_dthalf)?(?:_r([1-9][0-9]*))?'
_TAG_RE = re.compile(_TAG_PAT)
_CELL_RE = re.compile(_TAG_PAT + r'_s([1-9][0-9]*)')
_PROBE_RE = re.compile(r'npprobe([1-9][0-9]*)_(.+)')
DEV_SEEDS = tuple(_gen.CAMPAIGN_SEEDS)                            # §7 — "개발 시드 = 기존 (32452843 · 49979687 · 67867967)"
HOLDOUT_SEEDS = (15485863, 86028121, 104395301)                   # §7 — "확인 (holdout) 시드 = 15485863 · 86028121 · 104395301 … 결과 전 고정"


def parse_tag(tag):
    """셀 꼬리표 (seed 앞까지) → dict(tag, arm, level, stiffen_se, hold_bo_pairwise, dt_factor, revolutions).  문법 밖이면 ValueError."""
    m_ = _TAG_RE.fullmatch(tag) if isinstance(tag, str) else None
    if not m_:
        raise ValueError(f'강성 축 셀 꼬리표가 아니다: {tag!r} — `<{"|".join(STIFF_ARMS)}>_<soft|ref|ref2>[_dthalf][_r<N>]`')
    arm, level, dth, rev = m_.groups()
    if arm == 'E0' and rev is not None:
        raise ValueError(f'{tag}: E0 는 회전 0 이다 — `_r<N>` 을 붙이지 않는다')
    if arm != 'E0' and rev is None:
        raise ValueError(f'{tag}: {arm} 는 회전 팔이다 — `_r<N>` (바퀴 수) 가 있어야 한다')
    F = STIFF_LEVELS[level]
    return dict(tag=tag, arm=arm, level=level, stiffen_se=F, hold_bo_pairwise=(F != 1.0),
                dt_factor=0.5 if dth else 1.0, revolutions=int(rev) if rev else 0)


def parse_cell(name):
    """셀 폴더 이름 → parse_tag + name · seed.  NP 프로브 · 옛 생성기 팔 이름 (LC_s…) · 문법 밖은 ValueError."""
    m_ = _CELL_RE.fullmatch(name) if isinstance(name, str) else None
    if not m_:
        raise ValueError(f'강성 축 셀 이름이 아니다: {name!r} — `<{"|".join(STIFF_ARMS)}>_<soft|ref|ref2>[_dthalf][_r<N>]_s<seed>`')
    tag = name[:name.rindex('_s')]
    return dict(parse_tag(tag), name=name, seed=int(m_.group(5)))


def parse_run(name):
    """런 폴더 이름 (셀 또는 NP 프로브) → parse_cell + probe_np (프로브가 아니면 None) · folder."""
    m_ = _PROBE_RE.fullmatch(name) if isinstance(name, str) else None
    if m_:
        return dict(parse_cell(m_.group(2)), probe_np=int(m_.group(1)), folder=name)
    return dict(parse_cell(name), probe_np=None, folder=name)


def cell_expected_deck(name):
    """셀 (또는 NP 프로브) 이름 → 그 이름이 뜻하는 등록 덱 텍스트 (생성기 CLI 와 바이트 동일)."""
    c_ = parse_run(name)
    return expected_deck(c_['arm'], c_['seed'], revolutions=c_['revolutions'], stiffen_se=c_['stiffen_se'],
                         hold_bo_pairwise=c_['hold_bo_pairwise'], dt_factor=c_['dt_factor'])


#: ★ 등록 코호트 (단일 출처 — 런처 `launch_highbo.sh` · `scripts/mixer_stage_gate.py` 가 여기서 읽는다).
#:   사전등록 §8-2 ②: "① E0 5 런 (E0_ref ×3 · E0_ref2 · E0_ref@dt/2 · 회전 없음) → 1 % 계약 · 정규화 · 완주 진단 … → ② 통과 시에만
#:   LC_ref · LH_ref 회전 2 런 … NP 프로브 = E0_ref 첫 시드를 NP 5/10/20 으로 1 h 씩 … DEV 권한으로 확인 셀 실행 불가"
#:   §2 확인 블록 · §8-2 ④: "첫 holdout 시드 블록 (6 런: LC/LH × soft/ref + E0 둘) 은 즉시 · 나머지 두 시드 블록 (12 런) 은 sbatch --hold"
DEV_E0 = ('E0_ref_s32452843', 'E0_ref_s49979687', 'E0_ref_s67867967', 'E0_ref2_s32452843', 'E0_ref_dthalf_s32452843')
DEV_ROT = ('LC_ref_r2_s32452843', 'LH_ref_r2_s32452843')
#: ★ 개발 탐색 dev-bo (2026-10-02 · 사전등록 §11 v2.8 · 1저자 "ㄱㄱ") — DEV seed 1 의 2 바퀴 M 열람 뒤 정한 두 개발 팔 (같은 seed · ×20 · 2 바퀴 ·
#:   같은 OUT).  비교 상대 = 이미 돈 DEV_ROT 의 LC_ref_r2 · S_R² 기준 = E0_ref_s32452843.  확인 블록 · 확인 seed 와 섞지 않는다 (cohort_guard).
DEV_BO = tuple(f'{a_}_ref_r2_s32452843' for a_ in DEV_BO_ARMS)
#: ★ 개발 탐색 dev-u (2026-10-05 · 사전등록 §12 v2.9 · 1저자 "ㅇㅇ 그러자" · 망 수정보다 낮은 우선순위) — dev-rot · dev-bo M 열람 뒤 정한 두 개발 팔
#:   (같은 seed · ×20 · 2 바퀴 · 같은 OUT).  비교 상대 = 이미 돈 DEV_ROT 의 LC_ref_r2 · S_R² 기준 = E0_ref_s32452843.  확인 블록과 섞지 않는다 (cohort_guard).
DEV_U = tuple(f'{a_}_ref_r2_s32452843' for a_ in DEV_U_ARMS)
#: 개발 탐색 코호트 ↔ 그 코호트만 쓰는 팔 (cohort_guard 의 배타 규칙 — 개발 탐색 팔이 다른 단계 · 확인으로 새지 않게)
EXCLUSIVE_ARMS = {'dev-bo': DEV_BO_ARMS, 'dev-u': DEV_U_ARMS}
NP_PROBE = dict(base='E0_ref_s32452843', nps=(5, 10, 20), time='01:00:00')
DEV_PROBES = tuple(f'npprobe{n_}_{NP_PROBE["base"]}' for n_ in NP_PROBE['nps'])
CONFIRM_TAGS = ('LC_soft_r8', 'LH_soft_r8', 'LC_ref_r8', 'LH_ref_r8', 'E0_soft', 'E0_ref')


def confirm_block(seed):
    """한 holdout seed 의 확인 블록 6 셀 (§2 — LC/LH × soft/ref 8 바퀴 + E0 soft/ref)."""
    return tuple(f'{t_}_s{seed}' for t_ in CONFIRM_TAGS)


CONFIRM_FIRST = confirm_block(HOLDOUT_SEEDS[0])
CONFIRM_REST = confirm_block(HOLDOUT_SEEDS[1]) + confirm_block(HOLDOUT_SEEDS[2])
COHORTS = {'dev-e0': DEV_E0 + DEV_PROBES, 'dev-rot': DEV_ROT, 'dev-bo': DEV_BO, 'dev-u': DEV_U, 'confirm': CONFIRM_FIRST + CONFIRM_REST}
#: DEV 코호트 (DEV seed · ref 만 · 확인 꼬리표 없음 — cohort_guard · 관문 _classify 가 같은 목록을 쓴다)
DEV_COHORTS = ('dev-e0', 'dev-rot', 'dev-bo', 'dev-u')


def cohort_pairs(cohort):
    """코호트 안의 등록 덱 계약 쌍 (허용목록, 기준, 새) — §3: 같은 E 의 LC↔LH = B · E 사이 (같은 팔) = E · soft LC → ref LH = EB (동시).
    dev-bo (10-02 · §11): 코호트 안 쌍 = LHx10 → LHx30 (B — AM–AM 셋 · AM–벽 둘만 증가 · 나머지 정확히 같다).  LC_ref_r2 · LH_ref_r2 대비 B 는
    커밋 증거 (docs/data/mixer_highbo_dev_decks_20261002_bo/ deck_diff) — 그 둘은 dev-rot 코호트의 이미 돈 덱이라 여기서 다시 읽지 않는다.
    dev-u (10-05 · §12): 코호트 안 쌍 = LU212 → LU637 (U — 9 비영 CED 가 한 배율 3^(1/3) · 나머지 토큰 동일).  LC_ref_r2 대비 U 는 커밋 증거
    (docs/data/mixer_highbo_dev_decks_20261005_u/ deck_diff) — LC_ref_r2 는 dev-rot 의 이미 돈 덱이라 여기서 다시 읽지 않는다."""
    if cohort == 'dev-e0':
        return [('E', 'E0_ref_s32452843', 'E0_ref2_s32452843'), ('E', 'E0_ref_s32452843', 'E0_ref_dthalf_s32452843')]
    if cohort == 'dev-rot':
        return [('B', 'LC_ref_r2_s32452843', 'LH_ref_r2_s32452843')]
    if cohort == 'dev-bo':
        return [('B', DEV_BO[0], DEV_BO[1])]
    if cohort == 'dev-u':
        return [('U', DEV_U[0], DEV_U[1])]
    if cohort == 'confirm':
        out = []
        for s_ in HOLDOUT_SEEDS:
            c_ = {t_: f'{t_}_s{s_}' for t_ in CONFIRM_TAGS}
            out += [('B', c_['LC_soft_r8'], c_['LH_soft_r8']), ('B', c_['LC_ref_r8'], c_['LH_ref_r8']),
                    ('E', c_['LC_soft_r8'], c_['LC_ref_r8']), ('E', c_['LH_soft_r8'], c_['LH_ref_r8']),
                    ('EB', c_['LC_soft_r8'], c_['LH_ref_r8']), ('E', c_['E0_soft'], c_['E0_ref'])]
        return out
    raise ValueError(f'모르는 코호트 {cohort!r} — {sorted(COHORTS)}')


def cohort_guard():
    """등록 코호트의 자기 검사 — DEV 는 DEV seed 만 (holdout 금지 · soft 없음 · 확인 꼬리표 없음) · 확인은 holdout 만 · 정확히 3 × 6 ·
    ref2/dthalf 없음 · 회전 8 바퀴.  하나라도 어긋나면 ValueError (런처가 발사 전에 부른다).
    ★ 10-02 (dev-bo · §11): dev-bo 팔 (LHx10 · LHx30) 은 **dev-bo 코호트에만** · dev-bo 코호트는 그 팔만 (개발 탐색이 다른 단계 · 확인으로 새지 않게).
    ★ 10-05 (dev-u · §12): 같은 배타 규칙을 dev-u 팔 (LU212 · LU637) 에도 — 표 EXCLUSIVE_ARMS 한 벌로 본다."""
    why = []
    dev = tuple(n_ for k_ in DEV_COHORTS for n_ in COHORTS[k_])
    sec = {'dev-bo': '§11', 'dev-u': '§12'}
    for k_, names_ in COHORTS.items():
        for n_ in names_:
            try:
                arm_ = parse_run(n_)['arm']
            except ValueError:
                continue                                        # 이름 문법 위반은 아래 코호트별 검사가 짚는다
            for ck_, arms_ in EXCLUSIVE_ARMS.items():
                if arm_ in arms_ and k_ != ck_:
                    why.append(f'{k_} 코호트에 {ck_} 팔 셀 {n_} ({ck_} 팔은 {ck_} 코호트에만 — {sec.get(ck_, "")} 개발 탐색 · 확인 팔 아님)')
                if k_ == ck_ and arm_ not in arms_:
                    why.append(f'{ck_} 코호트에 {ck_} 팔이 아닌 셀 {n_} ({ck_} = {list(arms_)} 만)')
    for n_ in dev:
        c_ = parse_run(n_)
        if c_['seed'] in HOLDOUT_SEEDS:
            why.append(f'DEV 코호트에 holdout seed 셀 {n_}')
        elif c_['seed'] not in DEV_SEEDS:
            why.append(f'DEV 코호트에 개발 seed 가 아닌 셀 {n_}')
        if c_['level'] == 'soft':
            why.append(f'DEV 코호트에 soft 셀 {n_} (DEV7 = ref/ref2 만 · Codex 9 차 §6-1)')
        if c_['tag'] in CONFIRM_TAGS and c_['revolutions'] == 8:
            why.append(f'DEV 코호트에 확인 꼬리표 셀 {n_}')
    for n_ in dev:
        if parse_run(n_)['probe_np'] is not None and parse_run(n_)['name'] != NP_PROBE['base']:
            why.append(f'NP 프로브 {n_} 의 기준 셀이 등록 ({NP_PROBE["base"]}) 과 다르다')
    cf = COHORTS['confirm']
    for n_ in cf:
        try:
            c_ = parse_cell(n_)
        except ValueError as e_:
            why.append(f'확인 코호트에 셀이 아닌 이름 {n_} ({e_})')
            continue
        if c_['seed'] not in HOLDOUT_SEEDS:
            why.append(f'확인 코호트에 holdout 이 아닌 seed 셀 {n_} (DEV 셀 · 개발 seed 금지)')
        if c_['tag'] not in CONFIRM_TAGS:
            why.append(f'확인 코호트에 등록 밖 꼬리표 {n_} (ref2 · dthalf · 다른 바퀴 금지)')
    if sorted(cf) != sorted(set(cf)) or len(cf) != len(HOLDOUT_SEEDS) * len(CONFIRM_TAGS):
        why.append(f'확인 코호트 {len(cf)} 셀 (중복 포함) ≠ 3 seed × 6 = 18')
    if set(dev) & set(cf):
        why.append('DEV · 확인 코호트가 겹친다')
    if why:
        raise ValueError('등록 코호트 가드: ' + '; '.join(why))


DECK_META_SCHEMA = 'mixer_deck_meta/1'


def _sha_text(t):
    import hashlib
    return hashlib.sha256(t.encode('utf-8') if isinstance(t, str) else t).hexdigest()


def cell_deck_problems(d, name, expected=None):
    """셀 (또는 프로브) 폴더의 **덱 계약** → (문제 목록, 정보 dict).  ① in.mixer 가 이름이 뜻하는 등록 덱과 **바이트 동일**
    ② 경화 · dt 셀 (생성기가 deck_meta.json 을 쓰는 셀) 은 deck_meta.json 필수 — 스키마 · deck_sha256 = 이 덱 · 팔 · seed · 바퀴 ·
    stiffen_se · hold_bo_pairwise · dt_factor = 이름 (soft 셀은 있으면 같은 대조).  폴더 계약 (STL · n_expected · r_container) 은
    런처 쪽 (`scripts/mixer_stage_gate.py`) 이 본다 — 이 도구는 덱만."""
    pr, info = [], dict(name=name)
    try:
        c_ = parse_run(name)
    except ValueError as e_:
        return [str(e_)], info
    want = cell_expected_deck(name) if expected is None else expected
    info['expected_sha256'] = _sha_text(want)
    p_ = os.path.join(d, 'in.mixer')
    try:
        raw = open(p_, 'rb').read()
    except OSError:
        return [f'{name}: in.mixer 없음'], info
    info['deck_sha256'] = _sha_text(raw)
    if raw != want.encode('utf-8'):
        try:
            pe_, pg_ = parse_deck(want), parse_deck(raw.decode('utf-8', errors='replace'))
            first = next((f'#{i}: {" ".join(x)[:90]}  ⇄  {" ".join(y)[:90]}' for i, (x, y) in enumerate(zip(pe_['cmds'], pg_['cmds'])) if x != y),
                         'CED 행렬 · 명령 수 · 주석')
        except ValueError as e_:
            first = f'덱 파싱 불가 ({e_})'
        pr.append(f'{name}: in.mixer ≠ 재생성 등록 덱 (이름 → 생성 인자 · 바이트 비교) — 첫 차이 {first}')
    need_meta = c_['stiffen_se'] != 1.0 or c_['dt_factor'] != 1.0
    mp = os.path.join(d, 'deck_meta.json')
    if os.path.isfile(mp):
        try:
            mj = json.load(open(mp, encoding='utf-8'))
        except (OSError, ValueError) as e_:
            mj = None
            pr.append(f'{name}: deck_meta.json 을 읽을 수 없다 ({type(e_).__name__})')
        if mj is not None:
            info['deck_meta_sha256'] = _sha_text(open(mp, 'rb').read())
            want_m = dict(schema=DECK_META_SCHEMA, deck_sha256=info['deck_sha256'], arm=c_['arm'], seed=c_['seed'],
                          revolutions=c_['revolutions'], stiffen_se=c_['stiffen_se'], hold_bo_pairwise=c_['hold_bo_pairwise'],
                          dt_factor=c_['dt_factor'])
            off = [k_ for k_, v_ in want_m.items() if not isinstance(mj, dict) or mj.get(k_) != v_]
            if off:
                pr.append(f'{name}: deck_meta.json 이 덱 · 이름과 맞지 않는다 {off}')
    elif need_meta:
        pr.append(f'{name}: 경화 · dt 셀인데 deck_meta.json 이 없다 (생성기가 쓰는 봉인 가능한 메타 — README §6 "봉인은 deck_meta.json 의 deck_sha256 과 대조")')
    return pr, info


def check_cohort(runs, cohort):
    """등록 코호트 (dev-e0 · dev-rot · confirm) 의 덱 계약 → dict(verdict, cohort, dirs={이름: dict(problems, …)}, pairs=[…]).
    ① 코호트 가드 (cohort_guard) ② 셀마다 cell_deck_problems (재생성 바이트 동일 · deck_meta) ③ 등록 쌍마다 diff_decks (E · EB 는
    재생성 덱과 전 명령 토큰 동일 · B 는 CED 목표).  예정 밖 폴더는 보지 않는다 (코호트 = 이름 목록 그대로 — 복사본은 ① ② 에서 걸린다)."""
    out = dict(cohort=cohort, verdict='FAIL', dirs={}, pairs=[], guard=None)
    try:
        cohort_guard()
        names = COHORTS[cohort]
    except (ValueError, KeyError) as e_:
        out['guard'] = str(e_) if not isinstance(e_, KeyError) else f'모르는 코호트 {cohort!r}'
        return out
    texts, exp = {}, {}
    for n_ in names:
        d_ = os.path.join(runs, n_)
        exp[n_] = cell_expected_deck(n_)
        pr, info = cell_deck_problems(d_, n_, expected=exp[n_])
        out['dirs'][n_] = dict(info, problems=pr)
        texts[n_] = _read(os.path.join(d_, 'in.mixer'))
    for allow, a_, b_ in cohort_pairs(cohort):
        if texts.get(a_) is None or texts.get(b_) is None:
            out['pairs'].append(dict(allow=allow, ref=a_, new=b_, verdict='FAIL', problems=['덱 없음']))
            continue
        try:
            if allow in ('E', 'EB'):
                r_ = diff_decks(texts[a_], texts[b_], allow, expect_text=exp[b_])
            else:
                r_ = diff_decks(texts[a_], texts[b_], allow, expect=parse_deck(exp[b_])['ced'])
        except ValueError as e_:
            r_ = dict(verdict='FAIL', non_ced_diffs=[str(e_)])
        probs = [f'{k_}: {r_[k_][:4]}' for k_ in ('non_ced_diffs', 'outside', 'missing', 'wrong_direction', 'target_mismatch', 'e_rule', 'u_rule')
                 if r_.get(k_)]
        out['pairs'].append(dict(allow=allow, ref=a_, new=b_, verdict=r_['verdict'], e_case=r_.get('e_case'), problems=probs,
                                 **({'u_ratio': r_.get('u_ratio')} if allow == 'U' else {})))
    ok_ = all(not v_['problems'] for v_ in out['dirs'].values()) and all(p_['verdict'] == 'PASS' for p_ in out['pairs'])
    out['verdict'] = 'PASS' if ok_ else 'FAIL'
    return out


def report_cohort(r):
    print(f'── 등록 코호트 {r["cohort"]} (덱 계약: 재생성 바이트 동일 · deck_meta · 등록 쌍) → {r["verdict"]}')
    if r.get('guard'):
        print(f'   ⛔ {r["guard"]}')
    for n_, v_ in r['dirs'].items():
        print(f'   {n_:<32s} ' + ('✓ 재생성 덱과 바이트 동일' + (' · deck_meta ✓' if v_.get('deck_meta_sha256') else '')
                                   if not v_['problems'] else '⛔ ' + '; '.join(v_['problems'])[:220]))
    for p_ in r['pairs']:
        print(f'   {p_["allow"]:<2s} {p_["ref"]} → {p_["new"]}  {p_["verdict"]}' + (f'  ({p_["e_case"]})' if p_.get('e_case') else '')
              + (f'  (공통 배율 ×{p_["u_ratio"]:.7g})' if p_.get('u_ratio') is not None else '')
              + ('' if not p_['problems'] else '  ⛔ ' + '; '.join(p_['problems'])[:220]))


def _read(path):
    try:
        return open(path, encoding='utf-8').read()
    except OSError:
        return None


def is_stiff_tag(tag):
    """강성 축 셀 꼬리표 (`LC_ref_r2` · `E0_soft` …) 인가 — 옛 생성기 팔 이름 (`LC` · `LH` · `E0`) 은 아니다."""
    try:
        parse_tag(tag)
        return True
    except ValueError:
        return False


def expected_for_tag(tag, seed):
    """--runs 의 꼬리표 + seed → 기대 덱.  옛 생성기 팔 이름 = GEN_ARGS (8 바퀴 · soft) 그대로 · 강성 축 꼬리표 = 이름의 생성 인자."""
    if is_stiff_tag(tag):
        c_ = parse_tag(tag)
        return expected_deck(c_['arm'], seed, revolutions=c_['revolutions'], stiffen_se=c_['stiffen_se'],
                             hold_bo_pairwise=c_['hold_bo_pairwise'], dt_factor=c_['dt_factor'])
    return expected_deck(tag, seed)


def _seed_dirs(runs, arm):
    """runs/<arm>_s<숫자>/ 디렉터리 → [(이름, 시드 문자열, 경로)…] 이름순.  gen.log (파일) · .new 같은 것은 건너뛴다."""
    out = []
    for d in sorted(glob.glob(os.path.join(glob.escape(runs), f'{glob.escape(arm)}_s*'))):
        name = os.path.basename(d)
        sd = name[len(arm) + 2:]
        if os.path.isdir(d) and re.fullmatch(r'[0-9]+', sd):
            out.append((name, sd, d))
    return out


def seed_cohort(runs, arm, ref_arm, want):
    """--runs 코호트의 시드 서명 검사 (2026-09-28, Codex 3차 HBR3-07).

    반환 dict(dirs={이름: dict(seed, arm, sig, expected, problems)}, problems={예정 시드: [문구…]},
              unplanned=[dict(dir, sig)…], duplicates=[dict(seeds, dirs, sig)…]).
    예정 시드 = `want` 의 십진 표기 그대로 (앞자리 0 등 다른 표기의 디렉터리는 예정 밖).
    """
    planned = {str(int(s)): int(s) for s in want}
    dirs, unplanned, exp_cache = {}, [], {}
    problems = {s: [] for s in planned.values()}
    for a_ in dict.fromkeys((ref_arm, arm)):
        for name, sd, d in _seed_dirs(runs, a_):
            text = _read(os.path.join(d, 'in.mixer'))
            sig = seed_signature(text) if text is not None else None
            if sd not in planned:
                unplanned.append(dict(dir=name, sig=sig))
                continue
            s = planned[sd]
            if (a_, s) not in exp_cache:
                try:
                    t_exp = expected_for_tag(a_, s)
                    exp_cache[(a_, s)] = (seed_signature(t_exp), None, t_exp)
                except (Exception, SystemExit) as e:          # 합성수 시드면 생성기가 SystemExit — 기대가 없으면 FAIL
                    exp_cache[(a_, s)] = (None, f'{type(e).__name__}: {e}', None)
            exp, err, t_exp = exp_cache[(a_, s)]
            pr = []
            if sig is None:
                pr.append(f'{name}: in.mixer 없음')
            elif err is not None:
                pr.append(f'{name}: 기대 서명을 생성기로 만들 수 없다 ({err})')
            elif sig != exp:
                pr.append(f'{name}: 기대 서명과 다르다 — ' + '; '.join(_sig_delta(sig, exp)))
            #  ★ 강성 축 꼬리표 (2026-09-30 · piece 2) — 시드 서명은 강성 · dt · 바퀴를 안 본다 ⇒ 새 이름은 덱 전체를 재생성 덱과 바이트 대조한다
            if is_stiff_tag(a_) and text is not None and t_exp is not None and text != t_exp:
                pr.append(f'{name}: in.mixer ≠ 재생성 등록 덱 ({a_} · seed {s} → 생성 인자 · 바이트 비교)')
            dirs[name] = dict(seed=s, arm=a_, sig=sig, expected=exp, problems=pr)
            problems[s] += pr
    #  같은 시드의 기준 팔 · 새 팔 서명이 같아야 한다
    for s in problems:
        x, y = dirs.get(f'{ref_arm}_s{s}'), dirs.get(f'{arm}_s{s}')
        if x and y and x['sig'] is not None and y['sig'] is not None and x['sig'] != y['sig']:
            problems[s].append(f'{ref_arm}·{arm} 서명이 다르다 (시드 {s} · 앞 = {arm}, 괄호 = {ref_arm}) — '
                               + '; '.join(_sig_delta(y['sig'], x['sig'], label=ref_arm)))
    #  코호트 고유성 — 서로 다른 시드 디렉터리에 같은 실제 서명이 있으면 (복사본) 그 시드 전부 FAIL
    by_sig = {}
    for name, v in dirs.items():
        if v['sig'] is not None:
            by_sig.setdefault(v['sig'], []).append((v['seed'], name))
    duplicates = []
    for sig, lst in by_sig.items():
        seeds = sorted({s for s, _ in lst})
        if len(seeds) > 1:
            names = sorted(n for _, n in lst)
            duplicates.append(dict(seeds=seeds, dirs=names, sig=sig_summary(sig)))
            for s in seeds:
                problems[s].append(f'같은 실제 서명이 다른 시드 디렉터리에도 있다 (복사본?) — {names}')
    return dict(dirs=dirs, problems=problems, unplanned=unplanned, duplicates=duplicates)


def report_seeds(coh, want):
    """디렉터리마다 실제 시드 서명 한 줄 (✓ = 기대 일치) + 예정 밖."""
    print(f'── 실제 시드 서명 (덱이 쓰는 RNG 시드 명령 전부 · 기대 = 생성기 CLI 가 그 시드 · 팔로 쓰는 덱, '
          f'--n-total {GEN_ARGS["n_total"]} --cgf {GEN_ARGS["cgf"]} --revolutions {GEN_ARGS["revolutions"]})')
    for name in sorted(coh['dirs'], key=lambda n: (coh['dirs'][n]['seed'], n)):
        v = coh['dirs'][name]
        print(f'   {name:<16s} {sig_summary(v["sig"])}   ' + ('✓ 기대 일치' if not v['problems'] else '⛔ 기대와 다름'))
    for u in coh['unplanned']:
        print(f'   {u["dir"]:<16s} {sig_summary(u["sig"])}   ⛔ 예정 밖 (예정 시드 {sorted(int(s) for s in want)} 에 없다)')


def collect_pairs(runs, arm, ref_arm, expect_seeds=None):
    """runs 디렉터리 → ([(기준 덱, 새 덱)…], 찾은 시드 집합, 빠진 시드 집합).  <arm>_s<시드>/in.mixer 만 (gen.log 등은 건너뛴다).

    ★ 2026-09-28 (Codex 3차 HBR3-07): expect_seeds 를 주면 **예정 시드 디렉터리만** 짝으로 센다 — 예정 밖은 seed_cohort 가
      '예정 밖' 으로 보고하고 rc 를 1 로 만든다 (옛 판은 4/3 으로 셌다).
    """
    pairs, found = [], set()
    planned = None if expect_seeds is None else {str(int(s)) for s in expect_seeds}
    for _, sd, d in _seed_dirs(runs, arm):
        if planned is not None and sd not in planned:
            continue
        pairs.append((os.path.join(runs, f'{ref_arm}_s{sd}', 'in.mixer'), os.path.join(d, 'in.mixer')))
        found.add(int(sd))
    missing = set(int(s) for s in (expect_seeds or ())) - found
    return pairs, found, missing


def report(label, r):
    print(f'── {label}  (허용목록 {r["allow"]}) → {r["verdict"]}')
    for row in r['table']:
        if row['ratio'] is None:                             # E · EB: 0 기준 (2026-09-30) — 비 대신 절대차
            mark = '≠' if row['new'] != row['ref'] else ' '
            print(f'   {mark} {row["pair"]:12s} {row["ref"]:14.6g} → {row["new"]:14.6g}   비 N/A (0 기준 · 차 {row["new"] - row["ref"]:+.6g})')
            continue
        mark = '≠' if abs(row['ratio'] - 1.0) > REL_TOL else ' '
        print(f'   {mark} {row["pair"]:12s} {row["ref"]:14.6g} → {row["new"]:14.6g}   ×{row["ratio"]:.4g}'
              + (f'   (규칙 {row["rule"]:.6g})' if row.get('rule') is not None and row['rule'] != row['ref'] else ''))
    if r.get('e_case'):
        print(f'   경우: {r["e_case"]}')
    if r.get('u_ratio') is not None:                         # U (2026-10-05 · dev-u)
        print(f'   공통 배율 ×{r["u_ratio"]:.7g} (기하평균 · 퍼짐 {r["u_spread"]:.2e} · 허용 {U_SPREAD_REL:.0e})')
    for k, msg in (('non_ced_diffs', 'CED 밖 차이'), ('outside', '허용목록 밖 CED 변화'), ('missing', '개입 누락 (허용 쌍인데 안 바뀜)'),
                   ('wrong_direction', '개입 방향 반대 (증가여야 한다)'), ('target_mismatch', '목표 행렬과 불일치'),
                   ('e_rule', 'E 규칙 위반'), ('u_rule', 'U 규칙 위반 (배율 하나 · 0 은 0)')):
        if r.get(k):
            print(f'   ⛔ {msg}: {r[k][:8]}')
    for p_ in r.get('seed_problems') or ():                 # --runs 만 (2026-09-28, Codex 3차 HBR3-07)
        print(f'   ⛔ 시드 서명: {p_}')


def _selftest():
    import importlib.util
    ok, fail = 0, []

    def chk(name, cond):
        nonlocal ok
        if cond:
            ok += 1
        else:
            fail.append(name)
        print(('  PASS  ' if cond else '  FAIL  ') + name)

    spec = importlib.util.spec_from_file_location('mmd', os.path.join(_HERE, 'make_mixer_deck.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    p8 = m.plan(8000)
    lc = m.deck(p8, rpm=60, revolutions=2, seed=32452843, arm='LC')
    lh = m.deck(p8, rpm=60, revolutions=2, seed=32452843, arm='LH')
    r = diff_decks(lc, lh, 'B')
    chk(f'① LC → LH (B): CED 밖 차이 0 · 바뀐 쌍 = 허용 다섯 쌍 ({len(r["changed"])})',
        r['verdict'] == 'PASS' and len(r['changed']) == 5 and not r['non_ced_diffs'])
    r = diff_decks(lc, lh, 'A')
    chk(f'② 같은 두 덱을 A (AM–AM 단독) 로 보면 AM–벽 변화가 허용목록 밖 = FAIL ({r["outside"]})',
        r['verdict'] == 'FAIL' and set(r['outside']) == {('AM_P', 'WALL'), ('AM_S', 'WALL')})
    #  변이 ③ — SE–SE CED 를 몰래 바꾸면 허용목록 밖 (행렬의 SE 행 · SE 열 한 칸만)
    se = 2
    lines = lh.split('\n')
    k0 = next(i for i, l in enumerate(lines) if l.startswith('fix mC '))
    row = lines[k0 + 1 + se].split()
    row[se] = f'{float(row[se]) * 2:.6g}'
    lines[k0 + 1 + se] = '    ' + ' '.join(row)
    bad = '\n'.join(lines)
    r = diff_decks(lc, bad, 'B')
    chk(f'③ 변이: SE–SE CED 를 바꾸면 허용목록 밖 = FAIL ({r["outside"]})',
        r['verdict'] == 'FAIL' and ('SE', 'SE') in r['outside'])
    #  변이 ④ — CED 밖 명령 (timestep) 을 바꾸면 FAIL
    bad2 = re.sub(r'^timestep\s+(\S+)', lambda mm: f'timestep {float(mm.group(1)) * 1.01:.4g}', lh, flags=re.M)
    r = diff_decks(lc, bad2, 'B')
    chk(f'④ 변이: timestep 이 다르면 CED 밖 차이 = FAIL ({len(r["non_ced_diffs"])} 건)',
        r['verdict'] == 'FAIL' and any('timestep' in d_ for d_ in r['non_ced_diffs']))
    #  ⑤ 주석 (팔 설명) 만 다른 것은 차이가 아니다
    r = diff_decks(lh, lh.replace('고-Bo 확장', '고-Bo 확장 (주석 수정)'), 'B')
    chk('⑤ 주석만 다르면 CED 밖 차이 0 (개입 없음 → 허용 쌍 누락으로 FAIL 이 정상)',
        not r['non_ced_diffs'] and r['changed'] == [] and r['verdict'] == 'FAIL' and len(r['missing']) == 5)
    #  ⑥ 실제 캠페인 조건 (10 만 원자 · CGF 151.4 · Fr 기본 rpm · 8 바퀴) — 세 시드 모두
    pc = m.plan(100000, cgf=151.4)
    rpm = m.resolve_rpm(pc['R'])
    res = []
    for sd in m.CAMPAIGN_SEEDS:
        res.append(diff_decks(m.deck(pc, rpm, 8, seed=sd, arm='LC'), m.deck(pc, rpm, 8, seed=sd, arm='LH'), 'B'))
    chk('⑥ 캠페인 조건 LC_s* → LH_s* 세 시드 모두 PASS (바뀐 쌍 다섯)',
        all(x['verdict'] == 'PASS' and len(x['changed']) == 5 for x in res))
    #  ⑦ 시드가 다르면 삽입 명령이 달라 FAIL — 같은 시드끼리만 짝짓는다
    r = diff_decks(m.deck(pc, rpm, 8, seed=32452843, arm='LC'), m.deck(pc, rpm, 8, seed=49979687, arm='LH'), 'B')
    chk('⑦ 시드가 다르면 CED 밖 차이 = FAIL (짝은 같은 시드끼리)', r['verdict'] == 'FAIL' and r['non_ced_diffs'])

    # ══ ⑧~⑬ 2026-09-27 저녁 Codex 재리뷰 HBR2-05 — 비교기 PASS 의 뜻을 등록 계약까지 넓힌다 (반례를 먼저 재현하고 고쳤다) ══
    def _mutrow(text, i, j, fn, sym=False):
        """새 덱의 CED 행렬 (i, j) 칸을 fn(값) 문자열로 (sym 이면 (j, i) 도)."""
        lines_ = text.split('\n')
        k0_ = next(k for k, l in enumerate(lines_) if l.startswith('fix mC '))
        for a_, b_ in dict.fromkeys(((i, j), (j, i)) if sym else ((i, j),)):       # 대각 칸은 한 번만 (두 번 적용 = 원상복구)
            row_ = lines_[k0_ + 1 + a_].split(); row_[b_] = fn(float(row_[b_])); lines_[k0_ + 1 + a_] = '    ' + ' '.join(row_)
        return '\n'.join(lines_)
    r = diff_decks(lc, _mutrow(lh, 0, 1, lambda v: f'{2 * v:.6g}'), 'B')
    chk('⑧ 변이: 새 덱 P–S 한 방향만 ×2 (비대칭) → FAIL (기준 덱만 대칭 검사하던 구멍)',
        r['verdict'] == 'FAIL' and any('비대칭' in d_ for d_ in r['non_ced_diffs']))
    r = diff_decks(lc, _mutrow(lh, 2, 2, lambda v: 'nan', sym=True), 'B')
    chk('⑨ 변이: 고정이어야 할 SE–SE 를 NaN 으로 → FAIL (비유한)', r['verdict'] == 'FAIL' and any('비유한' in d_ for d_ in r['non_ced_diffs']))
    r = diff_decks(lc, _mutrow(lh, 0, 0, lambda v: f'{-v:.6g}', sym=True), 'B')
    chk('⑩ 변이: 새 P–P 를 음수로 → FAIL (물리 범위)', r['verdict'] == 'FAIL' and any('음수' in d_ for d_ in r['non_ced_diffs']))
    r = diff_decks(lc, lh.replace('fix mC all property/global', 'fix bogus nonexisting property/global'), 'B')
    chk('⑪ 변이: CED fix 의 ID/group 을 바꾸면 → FAIL (명령 머리도 비교)',
        r['verdict'] == 'FAIL' and any('머리' in d_ for d_ in r['non_ced_diffs']))
    r = diff_decks(lc, _mutrow(lh, 0, 0, lambda v: f'{v / 1e3:.6g}', sym=True), 'B')
    chk(f'⑫ 변이: 허용 쌍이 바뀌었어도 **방향이 반대** (P–P 가 LC 보다 작아짐) 면 FAIL ({r.get("wrong_direction")})',
        r['verdict'] == 'FAIL' and r.get('wrong_direction'))
    exp_ = parse_deck(lh)['ced']
    r_ok = diff_decks(lc, lh, 'B', expect=exp_)
    r_no = diff_decks(lc, _mutrow(lh, 0, 0, lambda v: f'{v * 1.01:.6g}', sym=True), 'B', expect=exp_)
    chk('⑬ 목표 행렬 (생성기가 낸 LH) 을 주면 일치할 때만 PASS (1 % 어긋나면 FAIL)',
        r_ok['verdict'] == 'PASS' and r_no['verdict'] == 'FAIL' and r_no.get('target_mismatch'))
    import tempfile as _tf
    with _tf.TemporaryDirectory() as td_:
        for a_ in ('LC', 'LH'):
            os.makedirs(os.path.join(td_, f'{a_}_s32452843'))
            open(os.path.join(td_, f'{a_}_s32452843', 'in.mixer'), 'w').write(lc if a_ == 'LC' else lh)
        pairs_, found_, missing_ = collect_pairs(td_, 'LH', 'LC', m.CAMPAIGN_SEEDS)
        chk(f'⑭ --runs: 예정 세 시드 중 하나만 있으면 1/3 로 세고 빠진 시드를 보고한다 ({sorted(missing_)})',
            len(pairs_) == 1 and found_ == {32452843} and len(missing_) == 2)

    # ══ ⑮~㉓ 2026-09-28, Codex 3차 HBR3-07 — 예정 디렉터리 셋을 '서로 다른 실제 시드 셋' 으로 인증하던 구멍 ══
    #  반례: seed 32452843 의 LC/LH 한 쌍을 예정 세 디렉터리에 복사 + --expect-deck → 3/3 PASS · rc 0 (실제 고유 덱 2 개).
    #  짝 비교는 짝 **안** 에서만 같은지 보고, 코호트 수는 **디렉터리 이름**만 셌다.  예정 밖 디렉터리는 4/3 으로 세거나
    #  (짝이 있으면) 기준 덱을 열다 예외로 죽거나 (LH 만) 아예 안 봤다 (LC 만).
    #  ⇒ 반례를 셀프테스트로 먼저 옮기고 (고치기 전 FAIL 을 확인) 고쳤다.  코호트는 **생성기 CLI 를 실제로 돌려** 만든다
    #    (gen_all.sh · test_launcher.sh 와 같은 인자) — 기대 서명도 생성기에서 오므로 ㉒ 가 '메모리 재현 = CLI 출력' 을 따로 묶는다.
    import contextlib
    import io
    import shutil
    import subprocess

    def _cli(argv):
        """실제 CLI (main) 를 같은 프로세스에서 돌린다 → (종료 코드 | 'EXC:…', stdout+stderr)."""
        buf, old, code = io.StringIO(), sys.argv, 0
        try:
            sys.argv = ['mixer_deck_diff.py'] + list(argv)
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                main()
        except SystemExit as e:
            code = 0 if e.code is None else (e.code if isinstance(e.code, int) else f'EXIT:{e.code}')
        except Exception as e:                  # 옛 판: 예정 밖 LH 하나에 기준 덱을 열다 FileNotFoundError
            code = f'EXC:{type(e).__name__}: {e}'
        finally:
            sys.argv = old
        return code, buf.getvalue()

    def _ok(fn):
        try:
            return bool(fn())
        except Exception:
            return False

    gen_cli = ['--n-total', '100000', '--cgf', '151.4', '--revolutions', '8']   # gen_all.sh 기본 N_TOTAL · CGF · REV
    s0, other = m.CAMPAIGN_SEEDS[0], 91648301          # 예정 밖 시드 = 소수 (생성기 셀프테스트가 쓰는 값)
    with _tf.TemporaryDirectory() as td_:
        gold = os.path.join(td_, 'gold')
        for sd in m.CAMPAIGN_SEEDS:
            for a_ in ('LC', 'LH'):
                subprocess.run([sys.executable, os.path.join(_HERE, 'make_mixer_deck.py'), '--out',
                                os.path.join(gold, f'{a_}_s{sd}'), '--arm', a_, '--seed', str(sd)] + gen_cli,
                               check=True, capture_output=True)

        def _co(name):
            d_ = os.path.join(td_, name)
            shutil.copytree(gold, d_)
            return d_

        def _rd(d_, a_, sd):
            return open(os.path.join(d_, f'{a_}_s{sd}', 'in.mixer'), encoding='utf-8').read()

        def _wr(d_, a_, sd, text):
            os.makedirs(os.path.join(d_, f'{a_}_s{sd}'), exist_ok=True)
            open(os.path.join(d_, f'{a_}_s{sd}', 'in.mixer'), 'w', encoding='utf-8').write(text)

        #  ⑮ (a) Codex 반례 그대로 — 한 쌍을 예정 세 디렉터리에 복사 + 실제 CLI + --expect-deck
        ra = _co('a')
        lc0, lh0 = _rd(ra, 'LC', s0), _rd(ra, 'LH', s0)
        for sd in m.CAMPAIGN_SEEDS:
            _wr(ra, 'LC', sd, lc0)
            _wr(ra, 'LH', sd, lh0)
        code, txt = _cli(['--runs', ra, '--allow', 'B', '--expect-deck', os.path.join(ra, f'LH_s{s0}', 'in.mixer')])
        chk(f'⑮ Codex 반례: seed {s0} 의 LC/LH 한 쌍을 예정 세 디렉터리에 복사 + --expect-deck → FAIL '
            f'(rc {code!r} · 0/3 · 기대 서명 불일치 · 같은 서명이 다른 시드에) [옛 판: 3/3 PASS · rc 0]',
            code == 1 and '0/3 PASS' in txt and '기대 서명과 다르다' in txt and '같은 실제 서명' in txt)
        #  ⑯~⑱ (b) 예정 밖 디렉터리 — 옳은 코호트 옆에 (그 시드로는 옳게 만든 덱)
        rb = _co('b1')
        _wr(rb, 'LH', other, m.deck(pc, rpm, 8, seed=other, arm='LH'))
        code, txt = _cli(['--runs', rb, '--allow', 'B'])
        chk(f'⑯ 옳은 코호트 옆 예정 밖 LH_s{other} 하나 → FAIL (rc {code!r}) · "예정 밖" 보고 [옛 판: 기준 덱을 열다 예외]',
            code == 1 and '예정 밖' in txt and f'LH_s{other}' in txt)
        rb = _co('b2')
        _wr(rb, 'LC', other, m.deck(pc, rpm, 8, seed=other, arm='LC'))
        code, txt = _cli(['--runs', rb, '--allow', 'B'])
        chk(f'⑰ 옳은 코호트 옆 예정 밖 LC_s{other} (기준 팔) 하나 → FAIL (rc {code!r}) [옛 판: 보지도 않고 rc 0]',
            code == 1 and '예정 밖' in txt and f'LC_s{other}' in txt)
        _wr(rb, 'LH', other, m.deck(pc, rpm, 8, seed=other, arm='LH'))
        code, txt = _cli(['--runs', rb, '--allow', 'B'])
        chk(f'⑱ 예정 밖 짝 (LC+LH_s{other}) 을 더해도 4/3 이 아니라 3/3 짝 + 예정 밖 → FAIL (rc {code!r}) [옛 판: 4/4 PASS · rc 0]',
            code == 1 and 'LH_s* 3/3 짝' in txt and '예정 밖' in txt and '4/4 PASS' not in txt)
        #  ⑲ (c) LH 의 삽입 시드만 다른 값으로 — 짝 비교도 잡지만, 서명 검사가 **무엇이** 틀렸는지 짚어야 한다
        rc_ = _co('c')
        _wr(rc_, 'LH', s0, _rd(rc_, 'LH', s0).replace(f'insert/pack seed {s0} ', 'insert/pack seed 15485863 ', 1))
        code, txt = _cli(['--runs', rc_, '--allow', 'B'])
        chk(f'⑲ LH_s{s0} 의 삽입 시드만 15485863 으로 → FAIL (rc {code!r}) · 서명이 기대와 다르다며 insA 를 짚는다',
            code == 1 and '기대 서명과 다르다' in txt and 'insA(insert/pack) 15485863' in txt)
        #  ⑳ (c′) LC·LH 둘 다 같은 시드 명령을 같게 고친다 — 짝 비교로는 **안 보인다** (삽입 A · B · 분포 · 템플릿)
        s_b = m._next_prime(s0 + 2)
        edits = {'insA': (f'insert/pack seed {s0} ', 'insert/pack seed 15485863 '),
                 'insB': (f'insert/pack seed {s_b} ', 'insert/pack seed 15485867 '),
                 'pddA': ('particledistribution/discrete 32452867 ', 'particledistribution/discrete 15485863 '),
                 'pt3': (f'particletemplate/sphere {m.TPL_SEED["SE"]} ', f'particletemplate/sphere {m.TPL_SEED["VGCF"]} ')}
        got_ = {}
        for key, (old_, new_) in edits.items():
            d_ = _co(f'c2_{key}')
            n_ = 0
            for a_ in ('LC', 'LH'):
                t_ = _rd(d_, a_, s0)
                n_ += t_.count(old_)
                _wr(d_, a_, s0, t_.replace(old_, new_, 1))
            code, txt = _cli(['--runs', d_, '--allow', 'B'])
            got_[key] = (n_, code, '기대 서명과 다르다' in txt and f'{key}(' in txt)
        chk(f'⑳ LC·LH 둘 다 같은 시드 명령을 고치면 (짝 비교는 못 본다) → 넷 다 FAIL · 고친 fix 를 짚는다 {got_}',
            all(v == (2, 1, True) for v in got_.values()))
        #  ㉑ (d) 생성기 CLI 로 만든 옳은 세 시드 코호트 — 전과 같이 PASS
        rd_ = _co('d')
        js_ = os.path.join(td_, 'd.json')
        code, txt = _cli(['--runs', rd_, '--allow', 'B', '--expect-deck', os.path.join(rd_, f'LH_s{s0}', 'in.mixer'), '--json', js_])
        chk(f'㉑ 생성기 CLI 로 만든 옳은 세 시드 코호트 → 3/3 PASS · rc {code!r} (예정 밖 · ⛔ 없음)',
            code == 0 and '3/3 PASS' in txt and '예정 밖' not in txt and '⛔' not in txt)
        chk('㉑b 디렉터리 여섯의 실제 시드 서명을 한 줄씩 찍고 (✓) --json 에 짝마다 시드 · 서명 (실제 · 기대) · 코호트를 남긴다',
            _ok(lambda: sum(ln.lstrip().startswith(f'{a_}_s{sd} ') and '✓' in ln for ln in txt.split('\n')
                            for a_ in ('LC', 'LH') for sd in m.CAMPAIGN_SEEDS) == 6
                and sorted(r_['seed'] for r_ in json.load(open(js_))) == sorted(m.CAMPAIGN_SEEDS)
                and all(r_['seed_sig']['ref'] == r_['seed_sig']['expected_ref'] == r_['seed_sig']['new'] == r_['seed_sig']['expected_new']
                        and len(r_['seed_sig']['new']) == 7 and not r_['seed_problems']
                        and r_['cohort']['unplanned'] == [] and r_['cohort']['duplicate_signatures'] == []
                        for r_ in json.load(open(js_)))))
        #  ㉒ 기대 서명의 출처 — 메모리에서 만든 덱이 생성기 CLI 가 쓴 in.mixer 와 **바이트 동일** (여섯 덱)
        chk('㉒ expected_deck(팔, 시드) = 생성기 CLI 가 쓴 in.mixer (바이트 동일 · 여섯 덱) — 시드 유도를 다시 짜지 않는다',
            _ok(lambda: all(globals()['expected_deck'](a_, sd) == _rd(gold, a_, sd) for a_ in ('LC', 'LH') for sd in m.CAMPAIGN_SEEDS)))

    #  ㉓ 서명 추출 — 층상 (삽입 둘) · 균일 (삽입 하나) · 섬유 multisphere 템플릿.  대조 = 원문 줄 정규식 (독립 신탁)
    def _oracle(text):
        return [(f_, st_, int(v_)) for f_, st_, v_ in re.findall(
            r'^fix +(\S+) +\S+ +((?:insert|particledistribution|particletemplate)/\S+) +(?:seed +)?(\d+)', text, re.M)]

    def _t23():
        ss = globals()['seed_signature']
        dl, du = m.deck(pc, rpm, 8, seed=s0, arm='LC'), m.deck(pc, rpm, 8, seed=s0, arm='E1')
        m.set_phases(m.ALL_TYPES)
        try:
            df = m.deck(m.plan(8000), rpm=60, revolutions=1, seed=s0, arm='E1')
        finally:
            m.set_phases(('AM_P', 'AM_S', 'SE'))
        sl = ss(dl)
        return (list(sl) == _oracle(dl) and [f_ for f_, _, _ in sl] == ['pt1', 'pt2', 'pt3', 'pddA', 'pddB', 'insA', 'insB']
                and dict((f_, v_) for f_, _, v_ in sl)['insA'] == s0
                and list(ss(du)) == _oracle(du) and len(ss(du)) == 5
                and list(ss(df)) == _oracle(df) and sum(st_ == 'particletemplate/multisphere' for _, st_, _ in ss(df)) == 2)
    chk('㉓ seed_signature: 층상 LC (pt1-3 · pddA/B · insA/B, insA = 설계 시드) · 균일 E1 (다섯) · 섬유 multisphere 템플릿 — 원문 정규식과 일치',
        _ok(_t23))

    # ══ ㉔~㉞ 2026-09-30 — 강성 축 허용목록 E · EB (사전등록 docs/reviews/mixer_highbo_stiffness_prereg_20260929.md §3 ·
    #    Codex 7 차 §5 · 9 차 §3/§6).  ★ 반례를 먼저 옮겼다: 옛 판에는 E 허용목록이 **없었다** (ALLOW = A · B 뿐 — 사전등록 §8-3 표의
    #    "`--allow E` (있음)" 은 사실이 아니었다) ⇒ ㉔~㉞ 은 옛 판에서 전부 FAIL (KeyError 'E' · argparse choices).
    PE = {F_: m.plan(100000, cgf=151.4, stiffen_se=F_) for F_ in (1.0, 14.0, 28.0)}
    rpmE = m.resolve_rpm(PE[1.0]['R'])

    def mkE(arm, F_, rev, dtf=1.0):
        return m.deck(PE[F_], rpmE, rev, seed=32452843, arm=arm, hold_bo_pairwise=(F_ != 1.0), dt_factor=dtf)
    DE = {'LC_soft': mkE('LC', 1.0, 2), 'LH_soft': mkE('LH', 1.0, 2), 'LC_ref': mkE('LC', 14.0, 2), 'LH_ref': mkE('LH', 14.0, 2),
          'LC_ref2': mkE('LC', 28.0, 2), 'E0_soft': mkE('E0', 1.0, 0), 'E0_ref': mkE('E0', 14.0, 0), 'E0_ref2': mkE('E0', 28.0, 0),
          'E0_refdt': mkE('E0', 14.0, 0, 0.5), 'LC_refdt': mkE('LC', 14.0, 2, 0.5)}

    def _sub1(text, pat, rep):
        new_, n_ = re.subn(pat, rep, text, count=1, flags=re.M)
        assert n_ == 1, pat
        return new_

    def _ced(text, i, j):
        lines_ = text.split('\n')
        k0_ = next(k for k, l in enumerate(lines_) if l.startswith('fix mC '))
        return float(lines_[k0_ + 1 + i].rstrip().rstrip('&').split()[j])
    pos = [('E', 'LC_soft', 'LC_ref'), ('E', 'LH_soft', 'LH_ref'), ('E', 'LC_ref', 'LC_ref2'), ('E', 'E0_soft', 'E0_ref'),
           ('E', 'E0_ref', 'E0_ref2'), ('E', 'E0_ref', 'E0_refdt'), ('E', 'LC_ref', 'LC_refdt'), ('EB', 'LC_soft', 'LH_ref'),
           ('B', 'LC_ref', 'LH_ref')]
    res_ = {(a_, x_, y_): _ok(lambda: diff_decks(DE[x_], DE[y_], a_)['verdict'] == 'PASS') for a_, x_, y_ in pos}
    chk(f'㉔ ★ 등록 설계대로 만든 덱 → PASS: E (soft→×14 LC · LH · ×14→×28 · E0 soft→×14 · ×14→×28 · dt/2 E0 · LC) · '
        f'EB (LC soft → LH ×14) · B (×14 LC→LH) — 실패 {[k for k, v in res_.items() if not v]}', all(res_.values()))
    nu_ = _sub1(DE['LC_ref'], r'(poissonsRatio peratomtype \S+ \S+ )0\.30', r'\g<1>0.31')
    nb_ = _sub1(DE['LC_ref'], r'^(neighbor\s+)(\S+)', lambda mm: mm.group(1) + f'{float(mm.group(2)) * 1.5:.6g}')
    gv_ = _sub1(DE['LC_ref'], r'(gravity )9\.81', r'\g<1>9.80')
    chk('㉕ 반례 E 밖 필드 변경 — ν · neighbor · 중력 (×14 덱에서) → 셋 다 FAIL (CED 밖 차이)',
        _ok(lambda: all((lambda r_: r_['verdict'] == 'FAIL' and r_['non_ced_diffs'])(diff_decks(DE['LC_soft'], x_, 'E'))
                        for x_ in (nu_, nb_, gv_))))
    c13 = _ced(DE['LC_soft'], 0, 2)
    one_ = _mutrow(DE['LC_ref'], 0, 2, lambda v: f'{c13 * 14 ** (2.0 / 3.0):.6g}', sym=True)
    chk('㉖ 반례 한 쌍만 다른 CED — ×14 덱의 AM_P–SE 만 옛 동일상 규칙 값 (soft × 14^(2/3)) → FAIL · E 규칙 위반이 그 쌍을 짚는다',
        _ok(lambda: (lambda r_: r_['verdict'] == 'FAIL' and any('AM_P' in e_ and 'SE' in e_ for e_ in r_['e_rule'])
                     and not any('AM_S–SE' in e_ or 'SE–SE' in e_ for e_ in r_['e_rule']))(diff_decks(DE['LC_soft'], one_, 'E'))))
    se_ = _mutrow(DE['LH_ref'], 2, 2, lambda v: f'{v * 1.01:.6g}', sym=True)
    am_ = _mutrow(DE['LC_ref'], 0, 0, lambda v: f'{v * 2:.6g}', sym=True)
    chk('㉗ 반례 B 다섯 항 밖 CED — EB (LC soft → LH ×14) 에서 SE–SE ×1.01 · E (LC soft → LC ×14) 에서 AM_P–AM_P ×2 (E 는 AM–AM 을 '
        '못 바꾼다) → 둘 다 FAIL',
        _ok(lambda: diff_decks(DE['LC_soft'], se_, 'EB')['verdict'] == 'FAIL' and diff_decks(DE['LC_soft'], am_, 'E')['verdict'] == 'FAIL'))
    ame_ = _sub1(DE['LC_ref'], r'(youngsModulus peratomtype )1\.037e\+09', r'\g<1>1.1e+09')
    wle_ = _sub1(DE['LC_ref'], r'(youngsModulus peratomtype \S+ \S+ \S+ )1\.48e\+09', r'\g<1>2.96e+09')
    chk('㉘ 반례 AM 영률 변경 (AM_P 1.037e9 → 1.1e9) · 벽 영률 변경 → E FAIL (SE 영률만 허용)',
        _ok(lambda: all(diff_decks(DE['LC_soft'], x_, 'E')['verdict'] == 'FAIL' for x_ in (ame_, wle_))))

    def _stale(ref, soft):
        out_ = _sub1(ref, r'^timestep\s+\S+$', re.search(r'^timestep\s+\S+$', soft, re.M).group(0))
        it_ = iter(re.findall(r'^run (\d+)$', soft, re.M))
        out_ = re.sub(r'^run (\d+)$', lambda mm: 'run ' + next(it_), out_, flags=re.M)
        out_ = _sub1(out_, r'^(dump dmp all custom )\d+', lambda mm: mm.group(1) + re.search(r'^dump dmp all custom (\d+)', soft, re.M).group(1))
        return _sub1(out_, r'^(restart )\d+', lambda mm: mm.group(1) + re.search(r'^restart (\d+) ', soft, re.M).group(1))
    chk('㉙ ★ 반례 stale dt — SE ×14 인데 dt · step · 덤프 · 체크포인트를 soft 그대로 (LC · E0) → FAIL (Rayleigh 규칙 · 적분 불안정 덱)',
        _ok(lambda: all((lambda r_: r_['verdict'] == 'FAIL' and any('Rayleigh' in e_ for e_ in r_['e_rule']))(
            diff_decks(DE[s_], _stale(DE[t_], DE[s_]), 'E')) for s_, t_ in (('LC_soft', 'LC_ref'), ('E0_soft', 'E0_ref')))))
    r1_ = _sub1(DE['E0_refdt'], r'^run (\d+)$\n(?=unfix ins)', lambda mm: f'run {int(mm.group(1)) + 1}\n')
    d1_ = _sub1(DE['E0_refdt'], r'^(dump dmp all custom )(\d+)', lambda mm: mm.group(1) + str(int(mm.group(2)) - 1000))
    chk('㉚ 반례 dt/2 경로 — 정착 step +1 (정확히 2 배 아님) · 덤프 간격이 2 배 아님 → 둘 다 FAIL',
        _ok(lambda: all(diff_decks(DE['E0_ref'], x_, 'E')['verdict'] == 'FAIL' for x_ in (r1_, d1_))))
    chk('㉛ 빈 비교 · 범주 혼동 — 같은 덱을 E · EB 로 (개입 없음) · soft LC → ×14 LH 를 B 로 (E 필드 차이) → 셋 다 FAIL',
        _ok(lambda: diff_decks(DE['LC_ref'], DE['LC_ref'], 'E')['verdict'] == 'FAIL'
            and diff_decks(DE['LC_ref2'], DE['LC_ref2'], 'EB')['verdict'] == 'FAIL'
            and diff_decks(DE['LC_soft'], DE['LH_ref'], 'B')['verdict'] == 'FAIL'))
    tweak_ = re.sub(r'^run (\d+)$\n(?=unfix insA|unfix insB|\n)', lambda mm: f'run {int(mm.group(1)) + 100}\n', DE['LC_ref'], flags=re.M)
    tw_n = sum(1 for a_, b_ in zip(re.findall(r'^run (\d+)$', DE['LC_ref'], re.M), re.findall(r'^run (\d+)$', tweak_, re.M)) if a_ != b_)
    chk(f'㉜ --expect-deck (E) = 재생성 덱과 **전 명령 토큰 동일** — 정착 step +100 ({tw_n} 줄 · 물리 시간 허용 안) 은 필드 규칙으로는 PASS 이지만 '
        f'expect 로 FAIL · 재생성 덱 그대로면 PASS',
        _ok(lambda: tw_n == 2 and diff_decks(DE['LC_soft'], tweak_, 'E')['verdict'] == 'PASS'
            and diff_decks(DE['LC_soft'], tweak_, 'E', expect_text=DE['LC_ref'])['verdict'] == 'FAIL'
            and diff_decks(DE['LC_soft'], DE['LC_ref'], 'E', expect_text=mkE('LC', 14.0, 2))['verdict'] == 'PASS'))
    with _tf.TemporaryDirectory() as td_:
        pa_, pb_, pc_ = (os.path.join(td_, n_) for n_ in ('soft.mixer', 'ref.mixer', 'bad.mixer'))
        open(pa_, 'w').write(DE['LC_soft']); open(pb_, 'w').write(DE['LC_ref']); open(pc_, 'w').write(one_)
        c_ok, t_ok = _cli([pa_, pb_, '--allow', 'E'])
        c_bad, t_bad = _cli([pa_, pc_, '--allow', 'E'])
        c_runs, t_runs = _cli(['--runs', td_, '--allow', 'E'])
    chk(f'㉝ CLI --allow E: 옳은 짝 rc 0 · 한 쌍 틀린 덱 rc 1 · --runs 와 E 는 거부 (rc {c_runs!r} — 짝 모드 전용, dev 정책 단계 몫)',
        c_ok == 0 and 'PASS' in t_ok and c_bad == 1 and c_runs == 2 and '--runs' in t_runs)
    chk('㉞ 규칙 사본 = 생성기 — Rayleigh dt (F 1 · 14 · 28 · CGF 151.4 · 200) · 덤프 · 체크포인트 간격 (run_steps) 이 생성기와 같다',
        _ok(lambda: all(abs(_rayleigh_dt(_e_fields(parse_deck(m.deck(m.plan(100000, cgf=c_, stiffen_se=F_), rpmE, 0, arm='E0',
                                                                          hold_bo_pairwise=True))))[0]
                            / m.plan(100000, cgf=c_, stiffen_se=F_)['dt'] - 1.0) <= E_RULE['rayleigh_rel']
                        for F_ in (1.0, 14.0, 28.0) for c_ in (151.4, 200.0))
            and all(_dump_rule(st_['steps_run']) == st_['dump_every'] and _restart_rule(st_['steps_fill'], st_['steps_run']) == st_['restart_every']
                    for F_ in (1.0, 14.0) for rv_ in (0, 2, 8) for st_ in (m.run_steps(PE[F_], rpmE, rv_),))))

    # ══ ㉟~㊷ 2026-09-30 — 코드 선행조건 2 단계 piece 2: 강성 축 셀 이름 · --runs 새 이름 + E/EB · expected_deck 강성 인자 · 등록 코호트
    #    ★ 반례를 먼저 옮겼다 — 옛 판: expected_deck 에 강성 인자가 없다 (TypeError) · parse_cell · check_cohort · --cohort 없음 ·
    #      --runs 는 `<생성기 팔>_s<seed>` 만 읽고 E · EB 를 거부 (rc 2) ⇒ ㉟~㊷ 전부 FAIL.
    G = globals()
    EVD = os.path.normpath(os.path.join(_HERE, '..', 'docs', 'data', 'mixer_highbo_dev_decks_20260930_v26'))   # v2.6 ×20 · ×40 (옛 ×14 폴더는 이력)

    def _evd_dirs():
        out_ = []
        for sub in ('decks', 'compare', 'check_only'):
            for d_ in sorted(glob.glob(os.path.join(EVD, sub, '*'))):
                if os.path.isfile(os.path.join(d_, 'in.mixer')):
                    out_.append(d_)
        return out_

    def _t35():
        ds = _evd_dirs()
        return (len(ds) == 14 and all(G['cell_expected_deck'](os.path.basename(d_)) == open(os.path.join(d_, 'in.mixer'), encoding='utf-8').read()
                                      for d_ in ds)
                and G['expected_deck']('E0', 32452843, revolutions=0, stiffen_se=20.0, hold_bo_pairwise=True, dt_factor=0.5)
                == open(os.path.join(EVD, 'decks', 'E0_ref_dthalf_s32452843', 'in.mixer'), encoding='utf-8').read())
    chk('㉟ ★ expected_deck(팔, seed, revolutions, stiffen_se, hold_bo_pairwise, dt_factor) · cell_expected_deck(이름) = 커밋된 DEV 증거 덱 14 '
        '(decks 7 · compare 5 · check_only 2) 와 **바이트 동일** — 이름에서 생성 인자를 다시 낸다 (build.sh 의 gen_cmd 와 같은 규칙)', _ok(_t35))

    def _t36():
        pc = G['parse_cell']
        good = {'E0_ref_s32452843': ('E0', 'ref', 20.0, True, 1.0, 0, 32452843),
                'E0_ref_dthalf_s32452843': ('E0', 'ref', 20.0, True, 0.5, 0, 32452843),
                'E0_ref2_s32452843': ('E0', 'ref2', 40.0, True, 1.0, 0, 32452843),
                'LC_ref_r2_s32452843': ('LC', 'ref', 20.0, True, 1.0, 2, 32452843),
                'LH_soft_r8_s15485863': ('LH', 'soft', 1.0, False, 1.0, 8, 15485863),
                'E0_soft_s104395301': ('E0', 'soft', 1.0, False, 1.0, 0, 104395301)}
        bad = ('E0_ref_r2_s32452843', 'LC_ref_s32452843', 'LC_ref_r0_s32452843', 'LC_ref_r02_s32452843', 'LC_ref_r2_s032452843',
               'LX_ref_r2_s32452843', 'LC_hard_r2_s32452843', 'LC_ref_r2_dthalf_s32452843', 'LC_s32452843', 'LC_ref_r2', 'E0_ref_s',
               'E0_ref_s32452843 ', 'npprobe5_E0_ref_s32452843')
        ok_good = all((lambda c_: (c_['arm'], c_['level'], c_['stiffen_se'], c_['hold_bo_pairwise'], c_['dt_factor'], c_['revolutions'],
                                   c_['seed']) == v_)(pc(k_)) for k_, v_ in good.items())

        def rej(x_):
            try:
                pc(x_)
            except ValueError:
                return True
            return False
        pr = G['parse_run']('npprobe10_E0_ref_s32452843')
        return (ok_good and all(rej(x_) for x_ in bad) and pr['probe_np'] == 10 and pr['name'] == 'E0_ref_s32452843'
                and G['parse_run']('E0_ref_s32452843')['probe_np'] is None)
    chk('㊱ 셀 이름 문법 `<E0|LC|LH>_<soft|ref|ref2>[_dthalf][_r<N>]_s<seed>` — E0 는 _r 금지 · LC/LH 는 _r 필수 · 0/앞자리 0 · 모르는 팔/수준 · '
        '순서 뒤바뀜 · seed 없음 · 공백 거부 · NP 프로브 폴더 `npprobe<NP>_<셀>` 는 parse_run 만 받는다 (parse_cell 은 거부)', _ok(_t36))

    def _cp_evd(dst, names):
        os.makedirs(dst, exist_ok=True)
        for n_ in names:
            src_ = next(d_ for d_ in _evd_dirs() if os.path.basename(d_) == n_)
            shutil.copytree(src_, os.path.join(dst, n_))
        return dst
    with _tf.TemporaryDirectory() as td_:
        rE = _cp_evd(os.path.join(td_, 'rE'), ['LC_soft_r2_s32452843', 'LC_ref_r2_s32452843', 'LH_soft_r2_s32452843', 'LH_ref_r2_s32452843'])
        cE = _cli(['--runs', rE, '--ref-arm', 'LC_soft_r2', '--arm', 'LC_ref_r2', '--allow', 'E', '--expect-seeds', '32452843'])
        cEB = _cli(['--runs', rE, '--ref-arm', 'LC_soft_r2', '--arm', 'LH_ref_r2', '--allow', 'EB', '--expect-seeds', '32452843'])
        cB = _cli(['--runs', rE, '--ref-arm', 'LC_ref_r2', '--arm', 'LH_ref_r2', '--allow', 'B', '--expect-seeds', '32452843'])
        chk(f'㊲ ★ --runs 가 새 이름을 읽고 E · EB · B 를 받는다 (DEV 증거 사본: LC_soft_r2 → LC_ref_r2 E · → LH_ref_r2 EB · LC_ref_r2 → LH_ref_r2 B) '
            f'— rc {cE[0]!r} · {cEB[0]!r} · {cB[0]!r} (옛 판: E · EB rc 2 "--runs 는 A · B 전용")',
            all(c_[0] == 0 and '1/1 PASS' in c_[1] for c_ in (cE, cEB, cB)))
        #  ㊳ 반례 — 새 이름 폴더에 다른 seed (holdout) 의 덱 · stale dt 덱 · --expect-deck 혼용
        hold_ = G['expected_deck']('LC', 15485863, revolutions=2, stiffen_se=20.0, hold_bo_pairwise=True)
        open(os.path.join(rE, 'LC_ref_r2_s32452843', 'in.mixer'), 'w', encoding='utf-8').write(hold_)
        c1 = _cli(['--runs', rE, '--ref-arm', 'LC_soft_r2', '--arm', 'LC_ref_r2', '--allow', 'E', '--expect-seeds', '32452843'])
        soft_ = open(os.path.join(rE, 'LC_soft_r2_s32452843', 'in.mixer'), encoding='utf-8').read()
        ref_ = G['cell_expected_deck']('LC_ref_r2_s32452843')
        stale_ = _stale(ref_, soft_)
        open(os.path.join(rE, 'LC_ref_r2_s32452843', 'in.mixer'), 'w', encoding='utf-8').write(stale_)
        c2 = _cli(['--runs', rE, '--ref-arm', 'LC_soft_r2', '--arm', 'LC_ref_r2', '--allow', 'E', '--expect-seeds', '32452843'])
        open(os.path.join(rE, 'LC_ref_r2_s32452843', 'in.mixer'), 'w', encoding='utf-8').write(ref_)
        c3 = _cli(['--runs', rE, '--ref-arm', 'LC_soft_r2', '--arm', 'LC_ref_r2', '--allow', 'E', '--expect-seeds', '32452843',
                   '--expect-deck', os.path.join(rE, 'LC_ref_r2_s32452843', 'in.mixer')])
        c4 = _cli(['--runs', rE, '--ref-arm', 'LC', '--arm', 'LH', '--allow', 'E'])
        chk(f'㊳ 반례 (--runs 새 이름): holdout seed 덱을 DEV 이름 폴더에 → FAIL (rc {c1[0]!r} · 서명 · 재생성) · stale dt 덱 → FAIL (rc {c2[0]!r}) · '
            f'새 이름에 --expect-deck (한 파일 = 한 seed) 혼용 → rc {c3[0]!r} · 옛 팔 이름 (LC · LH) 으로 E → rc {c4[0]!r}',
            c1[0] == 1 and '재생성' in c1[1] and c2[0] == 1 and c3[0] == 2 and c4[0] == 2 and '--runs' in c4[1])

    def _dev_out(td_):
        o_ = _cp_evd(os.path.join(td_, 'dev'), list(G['DEV_E0']) + list(G['DEV_ROT']))
        base_ = G['NP_PROBE']['base']
        for n_ in G['DEV_PROBES']:
            shutil.copytree(os.path.join(o_, base_), os.path.join(o_, n_))
        return o_

    def _t39():
        with _tf.TemporaryDirectory() as td_:
            o_ = _dev_out(td_)
            r_ok = G['check_cohort'](o_, 'dev-e0')
            r_rot = G['check_cohort'](o_, 'dev-rot')
            c_ok = _cli(['--runs', o_, '--cohort', 'dev-e0'])
            bad = {}
            p_ = os.path.join(o_, G['DEV_PROBES'][0], 'in.mixer')                  # (a) 프로브 덱 ≠ 기준 셀 (다른 seed 의 E0_ref)
            keep = open(p_, encoding='utf-8').read()
            open(p_, 'w', encoding='utf-8').write(open(os.path.join(o_, 'E0_ref_s49979687', 'in.mixer'), encoding='utf-8').read())
            bad['probe'] = G['check_cohort'](o_, 'dev-e0')['verdict']
            open(p_, 'w', encoding='utf-8').write(keep)
            mp_ = os.path.join(o_, 'E0_ref2_s32452843', 'deck_meta.json')          # (b) deck_meta 의 deck_sha256 이 덱과 다름
            mk_ = open(mp_, encoding='utf-8').read()
            mj_ = json.loads(mk_)
            mj_['deck_sha256'] = '0' * 64
            open(mp_, 'w', encoding='utf-8').write(json.dumps(mj_))
            bad['meta_sha'] = G['check_cohort'](o_, 'dev-e0')['verdict']
            os.remove(mp_)                                                          # (c) 경화 셀인데 deck_meta 없음
            bad['meta_missing'] = G['check_cohort'](o_, 'dev-e0')['verdict']
            open(mp_, 'w', encoding='utf-8').write(mk_)
            dk_ = os.path.join(o_, 'E0_ref_dthalf_s32452843', 'in.mixer')         # (d) dt/2 폴더에 dt 그대로 덱 (E0_ref)
            kd_ = open(dk_, encoding='utf-8').read()
            open(dk_, 'w', encoding='utf-8').write(open(os.path.join(o_, 'E0_ref_s32452843', 'in.mixer'), encoding='utf-8').read())
            bad['dthalf'] = G['check_cohort'](o_, 'dev-e0')['verdict']
            open(dk_, 'w', encoding='utf-8').write(kd_)
            shutil.rmtree(os.path.join(o_, 'E0_ref_s67867967'))                   # (e) 셀 폴더 없음
            bad['missing'] = G['check_cohort'](o_, 'dev-e0')['verdict']
            c_bad = _cli(['--runs', o_, '--cohort', 'dev-e0'])
            return (r_ok['verdict'] == 'PASS' and r_rot['verdict'] == 'PASS' and len(r_ok['dirs']) == 8 and len(r_ok['pairs']) == 2
                    and all(p_['verdict'] == 'PASS' for p_ in r_ok['pairs']) and c_ok[0] == 0
                    and all(v_ == 'FAIL' for v_ in bad.values()) and c_bad[0] == 1), bad
    _r39 = (lambda: _t39())
    chk('㊴ ★ --cohort dev-e0 · dev-rot (DEV 증거 사본 + NP 프로브 셋 = 기준 셀 사본) → PASS (8 폴더 · E 쌍 둘 · B 쌍 하나) · 반례 → FAIL: '
        '프로브 덱 ≠ 기준 셀 · deck_meta sha256 ≠ 덱 · 경화 셀 deck_meta 없음 · dt/2 폴더에 dt 그대로 덱 · 셀 폴더 없음 (CLI rc 1)',
        _ok(lambda: _r39()[0]))

    def _confirm_out(td_):
        o_ = os.path.join(td_, 'cf')
        for n_ in G['COHORTS']['confirm']:
            c_ = G['parse_cell'](n_)
            d_ = os.path.join(o_, n_)
            os.makedirs(d_)
            t_ = G['cell_expected_deck'](n_)
            open(os.path.join(d_, 'in.mixer'), 'w', encoding='utf-8').write(t_)
            if c_['stiffen_se'] != 1.0 or c_['dt_factor'] != 1.0:
                p_ = m.plan(GEN_ARGS['n_total'], cgf=GEN_ARGS['cgf'], stiffen_se=c_['stiffen_se'])
                rp_ = m.resolve_rpm(p_['R'], m.FR_ANCHOR, None, False)
                json.dump(m.deck_meta(p_, rp_, c_['revolutions'], c_['seed'], c_['arm'], t_, argv=['(selftest)'],
                                      hold_bo_pairwise=c_['hold_bo_pairwise'], dt_factor=c_['dt_factor']),
                          open(os.path.join(d_, 'deck_meta.json'), 'w', encoding='utf-8'))
        return o_

    def _t40():
        with _tf.TemporaryDirectory() as td_:
            o_ = _confirm_out(td_)
            r_ok = G['check_cohort'](o_, 'confirm')
            n0 = 'LC_ref_r8_s15485863'
            t0_ = open(os.path.join(o_, n0, 'in.mixer'), encoding='utf-8').read()
            dev_ = open(os.path.join(EVD, 'decks', 'LC_ref_r2_s32452843', 'in.mixer'), encoding='utf-8').read()
            open(os.path.join(o_, n0, 'in.mixer'), 'w', encoding='utf-8').write(dev_)       # DEV 덱을 확인 셀 폴더에
            v_dev = G['check_cohort'](o_, 'confirm')['verdict']
            open(os.path.join(o_, n0, 'in.mixer'), 'w', encoding='utf-8').write(open(os.path.join(o_, 'LC_soft_r8_s15485863', 'in.mixer'),
                                                                                     encoding='utf-8').read())  # soft 덱을 ref 이름에
            v_soft = G['check_cohort'](o_, 'confirm')['verdict']
            open(os.path.join(o_, n0, 'in.mixer'), 'w', encoding='utf-8').write(t0_)
            return (r_ok['verdict'] == 'PASS' and len(r_ok['dirs']) == 18 and len(r_ok['pairs']) == 18
                    and sorted({p_['allow'] for p_ in r_ok['pairs']}) == ['B', 'E', 'EB'] and v_dev == 'FAIL' and v_soft == 'FAIL')
    chk('㊵ ★ --cohort confirm (holdout 3 seed × 6 셀 = 18 · 생성기로 만든 덱 + deck_meta) → PASS · 쌍 18 (seed 마다 B 둘 · E 셋 · EB 하나) · '
        '반례: DEV 덱 (LC_ref_r2_s32452843) 을 확인 셀 폴더에 · soft 덱을 ref 이름에 → FAIL', _ok(_t40))

    def _t41():
        gd = G['cohort_guard']
        gd()                                                     # 등록 코호트는 통과해야 한다
        saved = G['COHORTS']['dev-e0']
        try:
            G['COHORTS']['dev-e0'] = saved + ('E0_ref_s15485863',)   # holdout seed 를 DEV 에
            try:
                gd()
                return False
            except ValueError as e_:
                m1 = str(e_)
            G['COHORTS']['dev-e0'] = saved
            s2 = G['COHORTS']['confirm']
            G['COHORTS']['confirm'] = s2[:-1] + ('LC_ref_r2_s32452843',)      # DEV 셀을 확인에
            try:
                gd()
                return False
            except ValueError as e_:
                m2 = str(e_)
            finally:
                G['COHORTS']['confirm'] = s2
        finally:
            G['COHORTS']['dev-e0'] = saved
        return 'holdout' in m1 and ('DEV' in m2 or 'holdout' in m2)
    chk('㊶ 등록 코호트 가드 — DEV 코호트는 DEV seed 만 (holdout 금지 · soft 없음) · 확인 코호트는 holdout seed 만 · 정확히 3 × 6 · ref2/dthalf 없음 · '
        '회전 8 바퀴 — 코호트에 holdout 셀을 넣거나 DEV 셀을 확인에 넣으면 거부 (ValueError)', _ok(_t41))
    chk('㊷ --cohort 에 모르는 이름 · --cohort 와 --ref-arm/--allow 혼용 → rc 2',
        _ok(lambda: _cli(['--runs', EVD, '--cohort', 'nope'])[0] == 2
            and _cli(['--runs', EVD, '--cohort', 'dev-e0', '--allow', 'E'])[0] == 2))

    # ══ ㊸~㊼ 2026-10-02 — 개발 탐색 dev-bo (강성 축 사전등록 docs/reviews/mixer_highbo_stiffness_prereg_20260929.md §11 · v2.8)
    #    팔 LHx10 · LHx30 (LH 의 AM–AM Bo_code ×10 · ×30 · 공동 개입 B) · 코호트 dev-bo.
    #    ★ 반례를 먼저 옮겼다 — 옛 판: 셀 이름 문법이 E0 · LC · LH 만 받아 LHx10_ref_r2_s… 를 거부 · COHORTS 에 dev-bo 없음 ⇒ ㊸~㊼ 전부 FAIL.
    BO_EVD = os.path.normpath(os.path.join(_HERE, '..', 'docs', 'data', 'mixer_highbo_dev_decks_20261002_bo'))
    BO_CELLS = ('LHx10_ref_r2_s32452843', 'LHx30_ref_r2_s32452843')

    def _t43():
        return all(G['cell_expected_deck'](n_) == open(os.path.join(BO_EVD, 'decks', n_, 'in.mixer'), encoding='utf-8').read()
                   for n_ in BO_CELLS)
    chk('㊸ ★ cell_expected_deck(LHx10_ref_r2 · LHx30_ref_r2 · seed 32452843) = 커밋된 dev-bo 증거 덱 (바이트 동일 — build.sh 의 gen_cmd 와 같은 규칙)',
        _ok(_t43))

    def _t44():
        pc = G['parse_cell']
        good = {'LHx10_ref_r2_s32452843': ('LHx10', 'ref', 20.0, True, 1.0, 2, 32452843),
                'LHx30_ref_r2_s32452843': ('LHx30', 'ref', 20.0, True, 1.0, 2, 32452843),
                'LH_ref_r2_s32452843': ('LH', 'ref', 20.0, True, 1.0, 2, 32452843),
                'LC_ref_r2_s32452843': ('LC', 'ref', 20.0, True, 1.0, 2, 32452843),
                'E0_ref_s32452843': ('E0', 'ref', 20.0, True, 1.0, 0, 32452843)}
        bad = ('LHx10_ref_s32452843', 'LHx20_ref_r2_s32452843', 'LHX10_ref_r2_s32452843', 'LHx_ref_r2_s32452843',
               'LHx10ref_r2_s32452843', 'LH_x10_ref_r2_s32452843', 'LHx10_ref_r2_s032452843', 'LHx3_ref_r2_s32452843')

        def rej(x_):
            try:
                pc(x_)
            except ValueError:
                return True
            return False
        return (all((lambda c_: (c_['arm'], c_['level'], c_['stiffen_se'], c_['hold_bo_pairwise'], c_['dt_factor'], c_['revolutions'],
                                 c_['seed']) == v_)(pc(k_)) for k_, v_ in good.items())
                and all(rej(x_) for x_ in bad) and tuple(G['STIFF_ARMS'])[:5] == ('E0', 'LC', 'LH', 'LHx10', 'LHx30')
                and tuple(G['DEV_BO_ARMS']) == ('LHx10', 'LHx30'))
    #  ★ 10-05 — STIFF_ARMS 의 정확한 전체 목록 대조는 U② 로 옮겼다 (dev-u 팔 LU212 · LU637 이 뒤에 붙는다) · 여기서는 dev-bo 때의 앞 다섯을 본다.
    chk('㊹ 셀 이름 문법 확장 — 팔 LHx10 · LHx30 (회전 팔 · _r 필수) 을 받고 옛 팔 (E0 · LC · LH) 파싱은 그대로 · 모르는 배수 (LHx20 · LHx3) · '
        '대문자 X · 구분자 어긋남 · seed 앞자리 0 거부 · 팔 목록 STIFF_ARMS 앞 다섯 = E0 · LC · LH · LHx10 · LHx30 (run_all · resume_all 정규식과 한 벌)',
        _ok(_t44))

    def _t45():
        with _tf.TemporaryDirectory() as td_:
            o_ = os.path.join(td_, 'bo')
            for n_ in BO_CELLS:
                shutil.copytree(os.path.join(BO_EVD, 'decks', n_), os.path.join(o_, n_))
            r_ok = G['check_cohort'](o_, 'dev-bo')
            c_ok = _cli(['--runs', o_, '--cohort', 'dev-bo'])
            bad = {}
            pa, pb = (os.path.join(o_, n_, 'in.mixer') for n_ in BO_CELLS)
            ka, kb = open(pa, encoding='utf-8').read(), open(pb, encoding='utf-8').read()
            open(pa, 'w', encoding='utf-8').write(kb)                                   # (a) LHx30 덱을 LHx10 폴더에
            bad['swap'] = G['check_cohort'](o_, 'dev-bo')['verdict']
            open(pa, 'w', encoding='utf-8').write(open(os.path.join(EVD, 'decks', 'LH_ref_r2_s32452843', 'in.mixer'), encoding='utf-8').read())
            bad['lh_deck'] = G['check_cohort'](o_, 'dev-bo')['verdict']                # (b) LH_ref_r2 덱 (Bo 38.4) 을 LHx10 폴더에
            open(pa, 'w', encoding='utf-8').write(ka)
            mp_ = os.path.join(o_, BO_CELLS[1], 'deck_meta.json')                       # (c) 경화 셀인데 deck_meta 없음
            km = open(mp_, encoding='utf-8').read()
            os.remove(mp_)
            bad['meta'] = G['check_cohort'](o_, 'dev-bo')['verdict']
            open(mp_, 'w', encoding='utf-8').write(km)
            shutil.rmtree(os.path.join(o_, BO_CELLS[1]))                                # (d) 셀 폴더 없음
            bad['missing'] = G['check_cohort'](o_, 'dev-bo')['verdict']
            c_bad = _cli(['--runs', o_, '--cohort', 'dev-bo'])
            ok_ = (r_ok['verdict'] == 'PASS' and sorted(r_ok['dirs']) == sorted(BO_CELLS) and
                   [(p_['allow'], p_['ref'], p_['new'], p_['verdict']) for p_ in r_ok['pairs']] == [('B',) + BO_CELLS + ('PASS',)]
                   and c_ok[0] == 0 and all(v_ == 'FAIL' for v_ in bad.values()) and c_bad[0] == 1)
            if not ok_:
                print(f'        {r_ok["verdict"]} · {bad} · rc {c_ok[0]} / {c_bad[0]}')
            return ok_
    chk('㊺ ★ --cohort dev-bo (커밋 증거 덱 사본) → PASS (2 폴더 · B 쌍 하나 = LHx10 → LHx30 · 재생성 바이트 동일 · deck_meta) · 반례 → FAIL: '
        '덱 바꿔치기 · LH_ref_r2 덱 · deck_meta 없음 · 셀 폴더 없음 (CLI rc 1)', _ok(_t45))

    def _t46():
        gd = G['cohort_guard']
        gd()                                                     # 등록 코호트는 통과해야 한다
        cases = [('dev-bo', BO_CELLS + ('LC_ref_r2_s32452843',), 'dev-bo'),             # dev-rot 셀을 dev-bo 에
                 ('dev-bo', (BO_CELLS[0], 'LHx30_ref_r2_s15485863'), 'holdout'),         # holdout seed
                 ('dev-bo', (BO_CELLS[0], 'LHx30_soft_r2_s32452843'), 'soft'),           # soft 수준
                 ('dev-rot', G['DEV_ROT'] + (BO_CELLS[0],), 'dev-bo'),                   # dev-bo 팔을 dev-rot 에
                 ('confirm', G['COHORTS']['confirm'][:-1] + ('LHx10_ref_r8_s15485863',), '확인')]
        hit = []
        for k_, v_, need in cases:
            saved = G['COHORTS'][k_]
            try:
                G['COHORTS'][k_] = v_
                try:
                    gd()
                    hit.append(False)
                except ValueError as e_:
                    hit.append(need in str(e_))
                    if need not in str(e_):
                        print(f'        ({k_}: {str(e_)[:120]})')
            finally:
                G['COHORTS'][k_] = saved
        gd()
        return all(hit) and len(hit) == len(cases)
    chk('㊻ 코호트 가드 확장 — dev-bo 팔 (LHx10 · LHx30) 은 dev-bo 코호트에만 · dev-bo 코호트는 그 팔 · DEV seed · ref 만: dev-bo 에 LC_ref_r2 · '
        'holdout seed · soft · dev-rot 에 LHx10 · 확인에 LHx10_ref_r8 → 거부 (ValueError · 문구가 원인을 짚는다)', _ok(_t46))
    #  ★ 10-05 — 코호트 이름 전체의 정확한 대조는 U⑦ 로 옮겼다 (dev-u 가 더해졌다) · 여기서는 dev-bo 때의 넷이 그대로 있는지 본다.
    chk('㊼ 등록 코호트 ⊇ confirm · dev-bo · dev-e0 · dev-rot — 옛 셋은 그대로 (DEV_E0 + 프로브 · DEV_ROT · 확인 18 · 쌍) · dev-bo = LHx10_ref_r2 · '
        'LHx30_ref_r2 (seed 32452843) 정확히 · 쌍 = B (LHx10 → LHx30)',
        _ok(lambda: {'confirm', 'dev-bo', 'dev-e0', 'dev-rot'} <= set(G['COHORTS'])
            and G['COHORTS']['dev-e0'] == G['DEV_E0'] + G['DEV_PROBES'] and G['COHORTS']['dev-rot'] == ('LC_ref_r2_s32452843', 'LH_ref_r2_s32452843')
            and len(G['COHORTS']['confirm']) == 18 and G['COHORTS']['dev-bo'] == BO_CELLS == tuple(G['DEV_BO'])
            and G['cohort_pairs']('dev-rot') == [('B', 'LC_ref_r2_s32452843', 'LH_ref_r2_s32452843')]
            and G['cohort_pairs']('dev-bo') == [('B',) + BO_CELLS]))

    # ══ U①~U⑦ 2026-10-05 — 개발 탐색 dev-u (강성 축 사전등록 docs/reviews/mixer_highbo_stiffness_prereg_20260929.md §12 · v2.9) · 허용목록 U
    #    (균일 γ 배율 — CED 비영 원소 **전부**가 한 공통 배율 r > 1 · 0 은 정확히 0 · CED 밖 명령은 토큰까지 같다) · 코호트 dev-u.
    #    ★ 반례를 먼저 옮겼다 — 옛 판: 셀 이름 문법이 LU212 · LU637 을 거부 · COHORTS 에 dev-u 없음 · --allow U 없음 (diff_decks 가 ALLOW['U'] 에서
    #      KeyError · argparse choices) ⇒ U①~U⑦ 전부 FAIL.
    U_EVD = os.path.normpath(os.path.join(_HERE, '..', 'docs', 'data', 'mixer_highbo_dev_decks_20261005_u'))
    U_CELLS = ('LU212_ref_r2_s32452843', 'LU637_ref_r2_s32452843')
    _lcr = open(os.path.join(EVD, 'decks', 'LC_ref_r2_s32452843', 'in.mixer'), encoding='utf-8').read()   # ibb dev-rot 에서 돈 덱 (비교 상대)
    _lhr = open(os.path.join(EVD, 'decks', 'LH_ref_r2_s32452843', 'in.mixer'), encoding='utf-8').read()

    def _udeck(arm, F=20.0):
        """생성기 CLI 와 같은 덱 (2 바퀴 · seed 32452843 · F = 1 이면 soft · 아니면 ×F + hold) — 증거 폴더에 기대지 않는다."""
        return G['expected_deck'](arm, 32452843, revolutions=2, stiffen_se=F, hold_bo_pairwise=(F != 1.0))

    def _t_u1():
        return all(G['cell_expected_deck'](n_) == open(os.path.join(U_EVD, 'decks', n_, 'in.mixer'), encoding='utf-8').read() for n_ in U_CELLS)
    chk('U① ★ cell_expected_deck(LU212_ref_r2 · LU637_ref_r2 · seed 32452843) = 커밋된 dev-u 증거 덱 (바이트 동일 — build.sh 의 gen_cmd 와 같은 규칙)',
        _ok(_t_u1))

    def _t_u2():
        pc = G['parse_cell']
        good = {'LU212_ref_r2_s32452843': ('LU212', 'ref', 20.0, True, 1.0, 2, 32452843),
                'LU637_ref_r2_s32452843': ('LU637', 'ref', 20.0, True, 1.0, 2, 32452843),
                'LHx10_ref_r2_s32452843': ('LHx10', 'ref', 20.0, True, 1.0, 2, 32452843),
                'LC_ref_r2_s32452843': ('LC', 'ref', 20.0, True, 1.0, 2, 32452843),
                'E0_ref_s32452843': ('E0', 'ref', 20.0, True, 1.0, 0, 32452843)}
        bad = ('LU212_ref_s32452843', 'LU850_ref_r2_s32452843', 'LU21_ref_r2_s32452843', 'LU2120_ref_r2_s32452843', 'lu212_ref_r2_s32452843',
               'LU_ref_r2_s32452843', 'LU212ref_r2_s32452843', 'LU_212_ref_r2_s32452843', 'LU212_ref_r2_s032452843', 'LU637_hard_r2_s32452843')

        def rej(x_):
            try:
                pc(x_)
            except ValueError:
                return True
            return False
        return (all((lambda c_: (c_['arm'], c_['level'], c_['stiffen_se'], c_['hold_bo_pairwise'], c_['dt_factor'], c_['revolutions'],
                                 c_['seed']) == v_)(pc(k_)) for k_, v_ in good.items())
                and all(rej(x_) for x_ in bad) and tuple(G['STIFF_ARMS']) == ('E0', 'LC', 'LH', 'LHx10', 'LHx30', 'LU212', 'LU637')
                and tuple(G['DEV_U_ARMS']) == ('LU212', 'LU637'))
    chk('U② 셀 이름 문법 확장 — 팔 LU212 · LU637 (회전 팔 · _r 필수) 을 받고 옛 팔 파싱은 그대로 · 모르는 수준 (LU850 · LU21 · LU2120) · 소문자 · '
        '구분자 어긋남 · seed 앞자리 0 · 모르는 강성 거부 · 팔 목록 STIFF_ARMS = E0 · LC · LH · LHx10 · LHx30 · LU212 · LU637 (run_all · resume_all 정규식과 한 벌)',
        _ok(_t_u2))

    def _t_u3():
        e2, e6 = _udeck('LU212'), _udeck('LU637')
        r2, r6, r26 = diff_decks(_lcr, e2, 'U'), diff_decks(_lcr, e6, 'U'), diff_decks(e2, e6, 'U')
        rs = diff_decks(_udeck('LC', 1.0), _udeck('LU212', 1.0), 'U')                          # soft 짝도 같은 규칙
        sp = G['U_SPREAD_REL']
        with _tf.TemporaryDirectory() as td_:
            pa, pb = os.path.join(td_, 'a.mixer'), os.path.join(td_, 'b.mixer')
            open(pa, 'w', encoding='utf-8').write(_lcr)
            open(pb, 'w', encoding='utf-8').write(e2)
            c2 = _cli([pa, pb, '--allow', 'U', '--expect-deck', pb])
            for n_, t_ in (('LC_ref_r2_s32452843', _lcr), ('LU212_ref_r2_s32452843', e2)):
                os.makedirs(os.path.join(td_, 'runs', n_))
                open(os.path.join(td_, 'runs', n_, 'in.mixer'), 'w', encoding='utf-8').write(t_)
            cr = _cli(['--runs', os.path.join(td_, 'runs'), '--ref-arm', 'LC_ref_r2', '--arm', 'LU212_ref_r2', '--allow', 'U', '--expect-seeds', '32452843'])
        ok_ = (all(r_['verdict'] == 'PASS' for r_ in (r2, r6, r26, rs)) and len(r2['changed']) == len(r6['changed']) == 9
               and abs(r2['u_ratio'] / 10.0 - 1.0) <= sp and abs(r6['u_ratio'] / 3000.0 ** (1.0 / 3.0) - 1.0) <= sp
               and abs(r26['u_ratio'] / 3.0 ** (1.0 / 3.0) - 1.0) <= sp and max(r_['u_spread'] for r_ in (r2, r6, r26, rs)) <= sp
               and c2[0] == 0 and '공통 배율' in c2[1] and cr[0] == 0 and '1/1 PASS' in cr[1])
        if not ok_:
            print(f'        {[(r_["verdict"], r_.get("u_ratio"), r_.get("u_spread"), r_.get("u_rule")) for r_ in (r2, r6, r26, rs)]} · rc {c2[0]} / {cr[0]}')
        return ok_
    chk('U③ ★ --allow U (균일 γ 배율) — LC_ref_r2 (ibb dev-rot 실행 덱) → LU212 · LU637 (×20 · 생성기 덱) · LU212 → LU637 · soft LC → LU212 = PASS · '
        '바뀐 쌍 9 · 공통 배율 ×10 · ×14.422496 · ×3^(1/3) (퍼짐 ≤ 2e-5 = %g 인쇄 반올림 둘) · CLI 두 덱 rc 0 · --runs 새 꼬리표 U rc 0', _ok(_t_u3))

    def _t_u4():
        lu2 = _udeck('LU212')
        c01 = _ced(_lcr, 0, 1)
        bad = {'se_only': diff_decks(_lcr, _mutrow(_lcr, 2, 2, lambda v: f'{v * 10:.6g}', sym=True), 'U'),           # SE–SE 한 원소만 ×10
               'E': diff_decks(_lcr, re.sub(r'(youngsModulus peratomtype \S+ \S+ )2e\+08', r'\g<1>2.2e+08', lu2, count=1), 'U'),   # 균일 ×10 + SE 영률
               'two_ratios': diff_decks(_lcr, _mutrow(lu2, 0, 1, lambda v: f'{c01 * 11:.6g}', sym=True), 'U'),        # AM_P–AM_S 만 ×11
               'as_B': diff_decks(_lcr, lu2, 'B'), 'as_A': diff_decks(_lcr, lu2, 'A'),                              # U 덱을 B · A 로
               'same': diff_decks(_lcr, _lcr, 'U'),                                                                # 빈 비교
               'down': diff_decks(lu2, _lcr, 'U'),                                                                 # 방향 반대 (×0.1)
               'wallwall': diff_decks(_lcr, _mutrow(lu2, 3, 3, lambda v: '1'), 'U'),                               # 벽–벽 0 → 1
               'dt': diff_decks(_lcr, re.sub(r'^timestep\s+(\S+)', lambda mm: f'timestep {float(mm.group(1)) * 1.01:.4g}', lu2,
                                            count=1, flags=re.M), 'U'),                                           # 균일 ×10 + timestep
               'vs_LH': diff_decks(_lhr, lu2, 'U'),                                                                # LH 사다리 위가 아니다
               'nan': diff_decks(_lcr, _mutrow(lu2, 2, 2, lambda v: 'nan', sym=True), 'U'),
               'target': diff_decks(_lcr, lu2, 'U', expect=parse_deck(_udeck('LU637'))['ced'])}                  # 목표 = LU637 인데 LU212 덱
        ur = {k_: ' · '.join(r_.get('u_rule') or []) for k_, r_ in bad.items()}
        why = dict(se_only='배율이 하나가 아니다' in ur['se_only'] and 'SE–SE' in ur['se_only'],
                   E=any('youngsModulus' in x_ for x_ in bad['E']['non_ced_diffs']),
                   two_ratios='배율이 하나가 아니다' in ur['two_ratios'] and 'AM_P–AM_S' in ur['two_ratios'],
                   as_B=('SE', 'SE') in bad['as_B']['outside'], as_A=('SE', 'SE') in bad['as_A']['outside'] and ('AM_P', 'WALL') in bad['as_A']['outside'],
                   same=bool(bad['same']['missing']), down=bool(bad['down']['wrong_direction']), wallwall='정확히 0' in ur['wallwall'],
                   dt=any('timestep' in x_ for x_ in bad['dt']['non_ced_diffs']), vs_LH='배율이 하나가 아니다' in ur['vs_LH'],
                   nan=any('비유한' in x_ for x_ in bad['nan']['non_ced_diffs']), target=bool(bad['target']['target_mismatch']))
        ok_ = all(r_['verdict'] == 'FAIL' for r_ in bad.values()) and all(why.values())
        if not ok_:
            print('        ' + ' · '.join(f'{k_}:{bad[k_]["verdict"]}/{"✓" if why[k_] else "✗"}' for k_ in bad))
        return ok_
    chk('U④ ★ 반례 → FAIL (사유를 짚는다): SE–SE 한 원소만 ×10 · 균일 ×10 인데 SE 영률 다름 · 두 배율 (AM_P–AM_S 만 ×11) · U 덱을 --allow B · A 로 '
        '(SE 낀 쌍이 허용목록 밖 = U 가 통과하는 가장 좁은 목록) · 같은 덱 (빈 비교) · 줄어든 덱 · 벽–벽 0 → 1 · 균일 ×10 인데 timestep 다름 · LH 덱 대비 · NaN · '
        '목표 행렬 불일치', _ok(_t_u4))

    def _t_u5():
        if not os.path.isdir(os.path.join(U_EVD, 'decks')):
            return False
        with _tf.TemporaryDirectory() as td_:
            o_ = os.path.join(td_, 'u')
            for n_ in U_CELLS:
                shutil.copytree(os.path.join(U_EVD, 'decks', n_), os.path.join(o_, n_))
            r_ok = G['check_cohort'](o_, 'dev-u')
            c_ok = _cli(['--runs', o_, '--cohort', 'dev-u'])
            bad = {}
            pa, pb = (os.path.join(o_, n_, 'in.mixer') for n_ in U_CELLS)
            ka, kb = open(pa, encoding='utf-8').read(), open(pb, encoding='utf-8').read()
            open(pa, 'w', encoding='utf-8').write(kb)                                  # (a) LU637 덱을 LU212 폴더에
            bad['swap'] = G['check_cohort'](o_, 'dev-u')['verdict']
            open(pa, 'w', encoding='utf-8').write(_lcr)                                # (b) LC_ref_r2 덱 (비교 상대) 을 LU212 폴더에
            bad['lc_deck'] = G['check_cohort'](o_, 'dev-u')['verdict']
            open(pa, 'w', encoding='utf-8').write(ka)
            mp_ = os.path.join(o_, U_CELLS[1], 'deck_meta.json')                       # (c) 경화 셀인데 deck_meta 없음
            km = open(mp_, encoding='utf-8').read()
            os.remove(mp_)
            bad['meta'] = G['check_cohort'](o_, 'dev-u')['verdict']
            open(mp_, 'w', encoding='utf-8').write(km)
            shutil.rmtree(os.path.join(o_, U_CELLS[1]))                               # (d) 셀 폴더 없음
            bad['missing'] = G['check_cohort'](o_, 'dev-u')['verdict']
            c_bad = _cli(['--runs', o_, '--cohort', 'dev-u'])
            ok_ = (r_ok['verdict'] == 'PASS' and sorted(r_ok['dirs']) == sorted(U_CELLS)
                   and [(p_['allow'], p_['ref'], p_['new'], p_['verdict']) for p_ in r_ok['pairs']] == [('U',) + U_CELLS + ('PASS',)]
                   and c_ok[0] == 0 and all(v_ == 'FAIL' for v_ in bad.values()) and c_bad[0] == 1)
            if not ok_:
                print(f'        {r_ok["verdict"]} · {bad} · rc {c_ok[0]} / {c_bad[0]}')
            return ok_
    chk('U⑤ ★ --cohort dev-u (커밋 증거 덱 사본) → PASS (2 폴더 · U 쌍 하나 = LU212 → LU637 · 재생성 바이트 동일 · deck_meta) · 반례 → FAIL: '
        '덱 바꿔치기 · LC_ref_r2 덱 · deck_meta 없음 · 셀 폴더 없음 (CLI rc 1)', _ok(_t_u5))

    def _t_u6():
        gd = G['cohort_guard']
        gd()                                                     # 등록 코호트는 통과해야 한다
        cases = [('dev-u', U_CELLS + ('LHx10_ref_r2_s32452843',), 'dev-u'),            # dev-bo 셀을 dev-u 에
                 ('dev-bo', G['DEV_BO'] + (U_CELLS[0],), 'dev-u'),                     # dev-u 셀을 dev-bo 에
                 ('dev-u', (U_CELLS[0], 'LU637_ref_r2_s15485863'), 'holdout'),          # holdout seed
                 ('dev-u', (U_CELLS[0], 'LU637_soft_r2_s32452843'), 'soft'),            # soft 수준
                 ('dev-rot', G['DEV_ROT'] + (U_CELLS[0],), 'dev-u'),                   # dev-u 팔을 dev-rot 에
                 ('confirm', G['COHORTS']['confirm'][:-1] + ('LU212_ref_r8_s15485863',), '확인')]
        hit = []
        for k_, v_, need in cases:
            saved = G['COHORTS'][k_]
            try:
                G['COHORTS'][k_] = v_
                try:
                    gd()
                    hit.append(False)
                except ValueError as e_:
                    hit.append(need in str(e_))
                    if need not in str(e_):
                        print(f'        ({k_}: {str(e_)[:120]})')
            finally:
                G['COHORTS'][k_] = saved
        gd()
        return all(hit) and len(hit) == len(cases)
    chk('U⑥ 코호트 가드 확장 — dev-u 팔 (LU212 · LU637) 은 dev-u 코호트에만 · dev-u 코호트는 그 팔 · DEV seed · ref 만: dev-u 에 LHx10_ref_r2 · dev-bo 에 '
        'LU212 · holdout seed · soft · dev-rot 에 LU212 · 확인에 LU212_ref_r8 → 거부 (ValueError · 문구가 원인을 짚는다)', _ok(_t_u6))
    chk('U⑦ 등록 코호트 = confirm · dev-bo · dev-e0 · dev-rot · dev-u — 옛 넷 그대로 · dev-u = LU212_ref_r2 · LU637_ref_r2 (seed 32452843) 정확히 · '
        '쌍 = U (LU212 → LU637)',
        _ok(lambda: sorted(G['COHORTS']) == ['confirm', 'dev-bo', 'dev-e0', 'dev-rot', 'dev-u']
            and G['COHORTS']['dev-u'] == U_CELLS == tuple(G['DEV_U']) and G['cohort_pairs']('dev-u') == [('U',) + U_CELLS]
            and G['cohort_pairs']('dev-bo') == [('B',) + tuple(G['DEV_BO'])]))
    print(f'\nmixer_deck_diff selftest: {ok}/{ok + len(fail)} PASS' + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


def main():
    ap = argparse.ArgumentParser(description='믹서 실행 덱 두 벌의 CED 차이 = 허용목록인가 (Codex HB-03)')
    ap.add_argument('decks', nargs='*', help='<기준 덱> <새 덱>')
    ap.add_argument('--allow', choices=sorted(ALLOW) + ['E', 'EB', 'U'], default='B',
                    help='B = 같은 강성 LC→LH (다섯 쌍) · A = AM–AM 셋 · E = 같은 팔 · 다른 강성 (또는 dt 만 1/k) · '
                         'EB = LC→LH 이면서 다른 강성 (E 와 B 동시) · U = 같은 강성 · CED 비영 원소 전부 한 공통 배율 > 1 (균일 γ 배율 · dev-u).  '
                         'E · EB 는 두 덱 모드 전용')
    ap.add_argument('--runs', help='runs 디렉터리 — <ref-arm>_s<시드>/in.mixer 와 <arm>_s<시드>/in.mixer 를 같은 시드끼리 '
                                   '+ 디렉터리마다 실제 시드 서명 = 생성기 기대 서명 · 시드 간 고유 (HBR3-07).  ★ --ref-arm · --arm 에 강성 축 '
                                   '꼬리표 (예 LC_soft_r2 · LH_ref_r2 · E0_ref) 를 주면 E · EB 도 받고 폴더마다 덱 전체를 재생성 덱과 바이트 대조한다')
    ap.add_argument('--ref-arm', default='LC', help='기준 팔 — 생성기 팔 이름 (LC) 또는 강성 축 꼬리표 (LC_soft_r8)')
    ap.add_argument('--arm', default='LH', help='새 팔 — 생성기 팔 이름 (LH) 또는 강성 축 꼬리표 (LH_ref_r8)')
    ap.add_argument('--cohort', choices=sorted(COHORTS), default=None,
                    help='(--runs 와 함께) 등록 코호트 dev-e0 · dev-rot · dev-bo · dev-u · confirm 의 덱 계약 — 셀마다 재생성 바이트 동일 · deck_meta · '
                         '등록 쌍 (B · E · EB · U).  런처 launch_highbo.sh 의 새 단계 관문')
    ap.add_argument('--expect-seeds', default=None,
                    help='(--runs) 있어야 할 시드 목록 "a,b,c" — 기본 = 생성기 CAMPAIGN_SEEDS.  하나라도 빠지면 FAIL (n/N 을 기계가 센다) · '
                         '목록 밖 <arm>_s* · <ref-arm>_s* 디렉터리가 있어도 FAIL (예정 밖 — 짝 수에 넣지 않는다)')
    ap.add_argument('--expect-deck', default=None,
                    help='지금 생성기로 새로 만든 같은 팔 덱 — 그 CED 행렬을 목표값으로 대조 (발사 덱이 손대지지 않았나)')
    ap.add_argument('--json')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    if a.cohort is not None:
        #  ★ 등록 코호트 모드 (2026-09-30 · piece 1 · 2) — 이름 목록 · 쌍 · 허용목록은 등록 (COHORTS · cohort_pairs) 이 정한다.
        #    다른 짝 인자를 섞으면 무엇을 검사했는지가 흐려지므로 거부한다.
        def _given(f_):
            return any(x_ == f_ or x_.startswith(f_ + '=') for x_ in sys.argv[1:])
        if not a.runs or a.decks or a.expect_deck or a.expect_seeds or any(_given(f_) for f_ in ('--allow', '--arm', '--ref-arm')):
            ap.error('--cohort 는 --runs <디렉터리> 와만 쓴다 (--allow · --arm · --ref-arm · --expect-seeds · --expect-deck · 덱 인자 없이)')
        r = check_cohort(a.runs, a.cohort)
        report_cohort(r)
        if a.json:
            json.dump(r, open(a.json, 'w'), ensure_ascii=False, indent=1)
            print(f'→ {a.json}')
        print(f'\n등록 코호트 {a.cohort}: {"PASS" if r["verdict"] == "PASS" else "⛔ FAIL — 발사 금지"}')
        raise SystemExit(0 if r['verdict'] == 'PASS' else 1)
    stiff = is_stiff_tag(a.arm) or is_stiff_tag(a.ref_arm)
    if a.runs and stiff and not (is_stiff_tag(a.arm) and is_stiff_tag(a.ref_arm)):
        ap.error(f'--runs: --ref-arm {a.ref_arm} · --arm {a.arm} — 강성 축 꼬리표와 옛 생성기 팔 이름을 섞지 않는다')
    if a.runs and a.allow in ('E', 'EB') and not stiff:
        ap.error(f'--runs 의 --allow {a.allow} 는 강성 축 꼬리표 (예 --ref-arm LC_soft_r2 --arm LC_ref_r2) 에서만 — 옛 생성기 팔 이름 '
                 f'({a.ref_arm} · {a.arm}) 은 같은 강성이라 A · B 전용이다 (두 덱 모드 <기준 덱> <새 덱> 도 된다)')
    if a.runs and stiff and a.expect_deck:
        ap.error('--runs 강성 축 꼬리표에는 --expect-deck 를 주지 않는다 — 한 파일은 한 seed 의 덱이다.  폴더마다 이름에서 재생성한 덱과 '
                 '바이트 대조한다 (자동)')
    expect_text = open(a.expect_deck, encoding='utf-8').read() if a.expect_deck else None
    expect = parse_deck(expect_text)['ced'] if expect_text is not None else None
    pairs, missing_seeds, coh, cohort, unplanned, orphan = [], set(), None, None, [], {}
    if a.runs:
        from make_mixer_deck import CAMPAIGN_SEEDS
        want = [int(x) for x in a.expect_seeds.split(',')] if a.expect_seeds else list(CAMPAIGN_SEEDS)
        pairs, found, missing_seeds = collect_pairs(a.runs, a.arm, a.ref_arm, want)     # 예정 시드만 센다 (HBR3-07)
        coh = seed_cohort(a.runs, a.arm, a.ref_arm, want)
        unplanned = [u['dir'] for u in coh['unplanned']]
        print(f'── {a.runs}: {a.arm}_s* {len(pairs)}/{len(want)} 짝 (찾음 {sorted(found)} · 빠짐 {sorted(missing_seeds)})'
              + (f' · ⛔ 예정 밖 {unplanned}' if unplanned else ''))
        report_seeds(coh, want)
        #  짝이 없는 예정 시드 (새 팔이 빠짐) 의 기준 팔 문제도 버리지 않는다 — 찍고 rc 1
        orphan = {s: pr for s, pr in coh['problems'].items() if pr and s not in found}
        for s, pr in sorted(orphan.items()):
            for p_ in pr:
                print(f'   ⛔ 시드 {s} (짝 없음): {p_}')
        cohort = dict(planned=want, found=sorted(found), missing=sorted(missing_seeds), gen_args=GEN_ARGS,
                      unplanned=[dict(dir=u['dir'], sig=_sig_json(u['sig'])) for u in coh['unplanned']],
                      duplicate_signatures=coh['duplicates'], problems_without_pair={str(s): pr for s, pr in orphan.items()})
        if not pairs:
            ap.error(f'{a.runs} 에 예정 시드의 {a.arm}_s* 가 없다' + (f' (예정 밖 {unplanned})' if unplanned else ''))
    elif len(a.decks) == 2:
        pairs = [tuple(a.decks)]
    else:
        ap.error('덱 두 개 또는 --runs 를 주세요')
    out = []
    for ref, new in pairs:
        t_ref, t_new = _read(ref), _read(new)
        try:
            if t_ref is None or t_new is None:
                raise ValueError('덱 없음: ' + ' · '.join(p_ for p_, t_ in ((ref, t_ref), (new, t_new)) if t_ is None))
            if a.runs and stiff:
                #  ★ 강성 축 꼬리표 (piece 2) — 기대 = 이 seed 에서 재생성한 새 팔 덱 (E · EB 는 전 명령 토큰 · B 는 CED 목표)
                s_ = int(os.path.basename(os.path.dirname(new))[len(a.arm) + 2:])
                t_exp = expected_for_tag(a.arm, s_)
                r = diff_decks(t_ref, t_new, a.allow, expect=parse_deck(t_exp)['ced'] if a.allow not in ('E', 'EB') else None,
                               expect_text=t_exp if a.allow in ('E', 'EB') else None)
            else:
                r = diff_decks(t_ref, t_new, a.allow, expect=expect, expect_text=expect_text)
        except ValueError as e:                     # 없는 덱 · 파싱 불가 덱 = 짝 FAIL (옛 판은 예외로 죽었다)
            r = dict(allow=a.allow, verdict='FAIL', non_ced_diffs=[str(e)], changed=[], outside=[], missing=[],
                     wrong_direction=[], target_mismatch=[], table=[])
        r.update(ref=ref, new=new)
        if coh is not None:
            s = int(os.path.basename(os.path.dirname(new))[len(a.arm) + 2:])
            dr, dn = coh['dirs'].get(f'{a.ref_arm}_s{s}', {}), coh['dirs'].get(f'{a.arm}_s{s}', {})
            r.update(seed=s, seed_problems=list(coh['problems'].get(s, [])), cohort=cohort,
                     seed_sig=dict(ref=_sig_json(dr.get('sig')), new=_sig_json(dn.get('sig')),
                                   expected_ref=_sig_json(dr.get('expected')), expected_new=_sig_json(dn.get('expected'))))
            if r['seed_problems']:
                r['verdict'] = 'FAIL'
        report(f'{ref}  →  {new}', r)
        out.append(r)
    if a.json:
        json.dump(out, open(a.json, 'w'), ensure_ascii=False, indent=1)
        print(f'→ {a.json}')
    bad = sum(r['verdict'] != 'PASS' for r in out)
    print(f'\n{len(out) - bad}/{len(out)} PASS' + ('' if not bad else '  ⛔ 짝짓기 근거 없음 — 발사 금지')
          + (f'  ⛔ 예정 시드 {sorted(missing_seeds)} 가 없다 — {len(out)} 짝으로는 3/3 이 아니다' if missing_seeds else '')
          + (f'  ⛔ 예정 밖 디렉터리 {unplanned} — 예정 코호트가 아니다 · 발사 금지' if unplanned else '')
          + (f'  ⛔ 짝 없는 예정 시드 {sorted(orphan)} 에 시드 서명 문제' if orphan else ''))
    raise SystemExit(1 if (bad or missing_seeds or unplanned or orphan) else 0)


if __name__ == '__main__':
    main()
