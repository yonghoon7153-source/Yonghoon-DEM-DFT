#!/usr/bin/env python3
"""LIGGGHTS atom-type ↔ 상(phase) 매핑을 **덱에서 읽고 덤프로 검증**한다.

★ 왜 이것이 있나 (2026-09-22, 케이스 260922_092001_0853b1):
  `ps_sweep` 세대 덱은 `create_box 3` 에 **1:AM_P · 2:AM_S · 3:SE** 인데,
  웹앱 업로드 기본값(`app.py`)이 `2:SE` 를 **박아** 있었다.  그래서 P:S=10:0 덱
  (AM_S 질량분율 0 ⇒ type 2 가 **0개**, SE 는 type 3 에 158,749개)을 올리자
    · type 3 = 원자의 **99.75 %** 가 아무 상에도 매핑되지 않아 `?` 가 되고
    · 그런데도 분석은 **멈추지 않고** porosity 15.82 % · AM-AM CN 3.64 ·
      파괴지수 0.218 같은 **그럴듯한 숫자를 전부 뽑았고**
    · `save_results` 가 빈 배열에 `np.min` 을 걸어 **우연히** 터졌다.
  ⇒ 크래시가 false-green 을 **우연히** 막고 있었다.  안 터졌으면 상(phase) 없이
    계산된 리포트가 초록으로 나갔다 (CLAUDE.md 규율 ⑤).

★ 설계 원칙 — **추측하지 않는다.  덱이 선언한 것을 읽고, 덤프로 대조한다.**
  덤프에는 "SE" 라는 글자가 없다 (`id type x y z radius …` 뿐).  그러나 덱에는 있다:
      fix pts3 all particletemplate/sphere <seed> atom_type 3 \
          density constant 2000 radius constant ${r_SE}
  `atom_type 3` ↔ `${r_SE}` 는 **추정이 아니라 선언**이다.  그리고 덱은 매번 같이
  업로드된다.  ⇒ 이 모듈은 그 줄을 읽고, **덤프의 실제 타입·반지름과 대조**한 뒤,
  하나라도 어긋나면 **거부**한다.

⚠ **기존 코퍼스를 깨뜨리지 않는 것**이 제약이다: 옛 세대 덱(`create_box 2`)은 변수가
  `r_AM` 하나뿐이고, 지금까지 `app.py` 가 그것을 반지름 `> 0.004`(sim) 로 AM_P/AM_S 로
  갈라 왔다.  170여 케이스의 상 라벨이 그 규칙에 걸려 있으므로 **그대로 보존**하고,
  `r_AM_P`/`r_AM_S`/`r_SE` 처럼 **덱이 명시한 경우에만** 그 이름을 쓴다.
"""
from __future__ import annotations

import argparse
import csv as _csv
import os
import re
import sys

#: 덱 변수 이름 → 상 이름 (명시적인 것만.  추측은 하지 않는다)
PHASE_FROM_VAR = {
    'r_SE': 'SE',
    'r_AM_P': 'AM_P',
    'r_AM_S': 'AM_S',
}

#: 옛 세대 덱의 총칭 변수.  이때만 반지름으로 가른다 (기존 app.py 규칙 보존)
GENERIC_AM_VAR = 'r_AM'

#: sim 단위 반지름 문턱 — `app.py` 의 기존 상수와 **같은 값**이어야 한다.
#: (6 µm AM_P → sim 6.0e-3 > 0.004 · 2 µm AM_S → 2.0e-3 < 0.004)
AM_P_RADIUS_CUT_SIM = 0.004

#: 덱 반지름 ↔ 덤프 반지름 허용 상대오차
RADIUS_TOL = 0.01


# ───────────────────────────── 덱 읽기 ─────────────────────────────────────
def _eval_expr(expr, variables):
    """`parse_liggghts._eval_liggghts_expr` 를 재사용한다 (규율 ①: 새로 짜지 않는다)."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from parse_liggghts import _eval_liggghts_expr
    return _eval_liggghts_expr(expr, variables)


def deck_variables(text: str) -> dict:
    """`variable NAME equal EXPR` 전수 → {이름: 값}."""
    out = {}
    for raw in text.splitlines():
        line = raw.split('#', 1)[0].strip()
        if not line.startswith('variable'):
            continue
        parts = line.split()
        if len(parts) >= 4 and parts[2] == 'equal':
            val = _eval_expr(' '.join(parts[3:]), out)
            if val is not None:
                out[parts[1]] = val
    return out


def deck_templates(text: str) -> dict:
    """`particletemplate/sphere … atom_type N … radius constant X` 전수.

    반환 {타입번호: {'var': 원본토큰, 'radius': float|None, 'density': float|None}}
    """
    variables = deck_variables(text)
    out = {}
    for raw in text.splitlines():
        line = raw.split('#', 1)[0].strip()
        if 'particletemplate/sphere' not in line:
            continue
        toks = line.split()
        t = rad_tok = dens_tok = None
        for i, tk in enumerate(toks):
            if tk == 'atom_type' and i + 1 < len(toks):
                try:
                    t = int(toks[i + 1])
                except ValueError:
                    pass
            elif tk == 'radius' and i + 2 < len(toks) and toks[i + 1] == 'constant':
                rad_tok = toks[i + 2]
            elif tk == 'density' and i + 2 < len(toks) and toks[i + 1] == 'constant':
                dens_tok = toks[i + 2]
        if t is None:
            continue
        out[t] = {
            'var': rad_tok,
            'radius': _eval_expr(rad_tok, variables) if rad_tok else None,
            'density': _eval_expr(dens_tok, variables) if dens_tok else None,
        }
    return out


def _var_name(tok):
    """`${r_SE}` · `v_r_SE` · `r_SE` → `r_SE`.  리터럴이면 None."""
    if not tok:
        return None
    m = re.fullmatch(r'\$\{([A-Za-z_][A-Za-z0-9_]*)\}', tok)
    if m:
        return m.group(1)
    if tok.startswith('v_'):
        return tok[2:]
    if re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', tok):
        return tok
    return None


def phase_for(var_token, radius):
    """(상 이름 | None, 사유).  ⛔ 모르면 **추측하지 않고 None** 을 낸다."""
    name = _var_name(var_token)
    if name is None:
        return None, f'반지름이 변수가 아니라 리터럴이다 ({var_token!r}) — 상을 알 수 없다'
    if name in PHASE_FROM_VAR:
        return PHASE_FROM_VAR[name], f'덱이 선언했다 (${{{name}}})'
    if name == GENERIC_AM_VAR:
        if radius is None:
            return None, f'${{{name}}} 인데 반지름을 못 구했다'
        who = 'AM_P' if radius > AM_P_RADIUS_CUT_SIM else 'AM_S'
        return who, (f'옛 세대 총칭 ${{{name}}} — 반지름 {radius:g} '
                     f'{">" if radius > AM_P_RADIUS_CUT_SIM else "≤"} '
                     f'{AM_P_RADIUS_CUT_SIM:g} 규칙 (기존 동작 보존)')
    return None, f'모르는 변수 ${{{name}}} — 상을 추측하지 않는다'


# ───────────────────────────── 덤프 읽기 ───────────────────────────────────
def types_in_dump(path: str) -> dict:
    """원자 덤프(.liggghts) 또는 atoms.csv → {타입: {'n', 'r_min', 'r_max'}}."""
    if path.lower().endswith('.csv'):
        return _types_from_csv(path)
    return _types_from_liggghts(path)


def _acc(out, t, r):
    d = out.setdefault(t, {'n': 0, 'r_min': None, 'r_max': None})
    d['n'] += 1
    if r is not None:
        d['r_min'] = r if d['r_min'] is None else min(d['r_min'], r)
        d['r_max'] = r if d['r_max'] is None else max(d['r_max'], r)


def _types_from_liggghts(path: str) -> dict:
    out, cols, in_data = {}, None, False
    with open(path, encoding='utf-8', errors='replace') as fh:
        for line in fh:
            s = line.strip()
            if s.startswith('ITEM: ATOMS'):
                cols = s.split()[2:]
                in_data = True
                continue
            if s.startswith('ITEM:'):
                in_data = False
                continue
            if not in_data or not cols:
                continue
            parts = s.split()
            if len(parts) < len(cols):
                continue
            rec = dict(zip(cols, parts))
            try:
                t = int(float(rec['type']))
            except (KeyError, ValueError):
                continue
            try:
                r = float(rec['radius']) if 'radius' in rec else None
            except ValueError:
                r = None
            _acc(out, t, r)
    return out


def types_from_pairs(pairs) -> dict:
    """(type, radius) 쌍들 → types_in_dump 와 **같은 모양**.

    이미 원자를 메모리에 읽은 호출자가 파일을 다시 읽지 않도록 (규율 ①).
    """
    out = {}
    for t, r in pairs:
        _acc(out, int(t), None if r is None else float(r))
    return out


def _types_from_csv(path: str) -> dict:
    out = {}
    with open(path, encoding='utf-8', errors='replace', newline='') as fh:
        for rec in _csv.DictReader(fh):
            try:
                t = int(float(rec['type']))
            except (KeyError, ValueError, TypeError):
                continue
            try:
                r = float(rec['radius'])
            except (KeyError, ValueError, TypeError):
                r = None
            _acc(out, t, r)
    return out


# ───────────────────────────── 매핑 문자열 ─────────────────────────────────
def parse_map(s: str) -> dict:
    out = {}
    for item in (s or '').split(','):
        item = item.strip()
        if not item:
            continue
        k, _, v = item.partition(':')
        out[int(k.strip())] = v.strip()
    return out


def format_map(m: dict) -> str:
    return ','.join(f'{t}:{m[t]}' for t in sorted(m))


# ───────────────────────────── 판정 ────────────────────────────────────────
def validate(type_map: dict, dump: dict) -> tuple:
    """(errors, notes) — ⛔ **덤프에 있는데 map 에 없는 타입 = 치명**.

    반대(map 에 있는데 덤프에 0개)는 **정상**일 수 있다: P:S=10:0 은 설계상
    AM_S 가 0개다.  그래서 그쪽은 note 로만 낸다.
    """
    errors, notes = [], []
    total = sum(d['n'] for d in dump.values()) or 1
    for t in sorted(dump):
        if t not in type_map:
            n = dump[t]['n']
            errors.append(
                f'⛔ 덤프의 type {t} 이 type_map 에 없다 — {n:,}개 '
                f'({100.0 * n / total:.2f} %), 반지름 {dump[t]["r_min"]:.4e}'
                f'~{dump[t]["r_max"]:.4e}.  이대로 돌면 그 원자들이 상(phase) 없이 '
                f'`?` 로 계산된다.')
    for t in sorted(type_map):
        if t not in dump:
            notes.append(f'· type {t} ({type_map[t]}) 은 덤프에 0개 — '
                         f'설계상 빌 수 있다 (예: P:S=10:0 의 AM_S).  배위수는 `—`.')
    return errors, notes


def resolve(deck_text: str, dump: dict) -> tuple:
    """(type_map, notes, errors).  덱에서 읽고 덤프로 대조한다."""
    notes, errors = [], []
    tmpl = deck_templates(deck_text)
    if not tmpl:
        return {}, notes, ['⛔ 덱에서 particletemplate/sphere 를 하나도 못 찾았다']

    mapping = {}
    for t in sorted(tmpl):
        name, why = phase_for(tmpl[t]['var'], tmpl[t]['radius'])
        if name is None:
            errors.append(f'⛔ type {t}: {why}')
            continue
        mapping[t] = name
        notes.append(f'· type {t} → {name}  ({why})')

    # ★ 덱만 믿지 않는다 — 덤프의 반지름과 대조한다 (덱·덤프 불일치 잡기)
    for t in sorted(set(mapping) & set(dump)):
        rd, dd = tmpl[t]['radius'], dump[t]['r_max']
        if rd and dd and abs(rd - dd) > RADIUS_TOL * max(rd, dd):
            errors.append(
                f'⛔ type {t}: 덱 반지름 {rd:.4e} 과 덤프 {dd:.4e} 가 다르다 '
                f'({100.0 * abs(rd - dd) / max(rd, dd):.1f} %) — 덱과 덤프가 '
                f'같은 런이 아닐 수 있다')

    # 덤프에 0개인 타입은 **뺀다** (넣으면 배위수 계산이 빈 배열을 만난다)
    dropped = [t for t in mapping if t not in dump]
    for t in dropped:
        notes.append(f'· type {t} ({mapping[t]}) 은 덤프에 0개 → map 에서 뺀다')
        del mapping[t]

    errors += validate(mapping, dump)[0]
    return mapping, notes, errors


def resolve_from_files(deck_path: str, atom_path: str) -> tuple:
    with open(deck_path, encoding='utf-8', errors='replace') as fh:
        deck = fh.read()
    return resolve(deck, types_in_dump(atom_path))


def app_wiring_errors(src, exists=True) -> list:
    """`webapp/app.py` 가 이 모듈을 **실제로** 쓰는가 → 오류 목록 (빈 = 통과).

    ★★★ 2026-09-22 (병합 검증에서 잡힘) — **초판 ⑩ 은 공허했다.**
      옛 판은 `(not src) or 'type_map_resolve' in src` 였다.  두 구멍:
        ⓐ `(not src) or …` = app.py 가 **없거나 못 읽히면 통과** (fail-OPEN).
           실측: `webapp/app.py` 를 통째로 지워도 ⑩ 이 초록이었다.
        ⓑ 부분문자열 검사라 메타 키 이름 `type_map_resolved` **하나만** 남아도
           통과한다.  실측: app.py 를 `meta = {'type_map_resolved': None}` 한 줄로
           바꿔도 초록이었다 ⇒ 배선을 다 뜯어내도 못 잡는다.
      *"배선 전에는 FAIL 이었다"* 는 사실이지만 그것은 **아무 출현도 없던 순간**의
      이야기이고, 회귀 가드로는 작동하지 않았다.  규율 ⑤ 의 그 자리다.
    ⇒ 이제 ⓐ 를 fail-CLOSED 로 바꾸고, ⓑ 를 **import · 호출 · 문턱 단일화** 세
      가지로 쪼갠다.  각 항목의 음성 대조는 selftest ⑩c 가 직접 돌린다.

    ★ 문턱 단일화가 왜 여기 있나 — ⑩ 의 라벨이 *"문턱 상수를 두 곳에 두지 않는다"*
      인데 실제로는 `0.004` 가 app.py 에 **리터럴**로, 여기 `AM_P_RADIUS_CUT_SIM` 에
      상수로 **두 곳**에 있었고 검사가 그것을 보지 않았다.  하필 그 되돌림 경로에
      170여 케이스 코퍼스의 상 라벨이 걸려 있어 조용한 분기가 가장 비싼 자리다."""
    if not exists:
        return ['⛔ webapp/app.py 를 읽을 수 없다 — 경계 계약을 확인할 수 없다']
    errs = []
    if not re.search(r'^\s*import\s+type_map_resolve\b', src, re.M):
        errs.append('⛔ app.py 에 `import type_map_resolve` 가 없다')
    if 'resolve_from_files(' not in src:
        errs.append('⛔ app.py 가 `resolve_from_files(` 를 부르지 않는다 (이름만 있고 배선이 없다)')
    if re.search(r'[<>]=?\s*0\.004\b', src):
        errs.append(f'⛔ 반지름 문턱 0.004 가 app.py 에 리터럴로 박혀 있다 — '
                    f'`AM_P_RADIUS_CUT_SIM`({AM_P_RADIUS_CUT_SIM}) 를 쓸 것 (두 곳 금지)')
    return errs


# ───────────────────────────── selftest ────────────────────────────────────
_DECK_PS_10_0 = '''
variable r_AM_P  equal 4.5e-3
variable r_AM_S  equal 2.0e-3
variable r_SE    equal 0.5e-3
create_box      3 reg_box
fix pts1 all particletemplate/sphere 20000003 atom_type 1 density constant 4800 radius constant ${r_AM_P}
fix pts2 all particletemplate/sphere 21300029 atom_type 2 density constant 4800 radius constant ${r_AM_S}
fix pts3 all particletemplate/sphere 22600001 atom_type 3 density constant 2000 radius constant ${r_SE}
fix pdd_mix all particledistribution/discrete 23900027 2 pts1 0.816 pts3 0.184
'''

_DECK_OLD_2TYPE = '''
variable r_AM    equal 3.0e-3
variable r_SE    equal 1.0e-3
create_box      2 reg_box
fix pts1 all particletemplate/sphere 15485863 atom_type 1 density constant 4800 radius constant ${r_AM}
fix pts2 all particletemplate/sphere 32452843 atom_type 2 density constant 2000 radius constant ${r_SE}
'''

_DECK_OLD_BIG_AM = _DECK_OLD_2TYPE.replace('r_AM    equal 3.0e-3',
                                           'r_AM    equal 6.0e-3')

_DECK_UNKNOWN_VAR = '''
variable r_MYSTERY equal 1.0e-3
fix pts1 all particletemplate/sphere 11 atom_type 1 density constant 4800 radius constant ${r_MYSTERY}
'''


def _dump(**kw):
    """{타입: 개수} + 반지름 → types_in_dump 와 같은 모양."""
    out = {}
    for t, (n, r) in kw.items():
        out[int(t.lstrip('t'))] = {'n': n, 'r_min': r, 'r_max': r}
    return out


_N_CHECKS = [0]


def selftest() -> int:
    fails = []
    _N_CHECKS[0] = 0

    def chk(name, cond, extra=''):
        _N_CHECKS[0] += 1
        print(('  ok  ' if cond else '  FAIL') + '  ' + name +
              (('   ' + str(extra)) if extra else ''))
        if not cond:
            fails.append(name)

    print('type_map_resolve selftest')

    # ── ① 실사고 재현: ps_10_0 (type 2 가 0개, SE 는 type 3) ────────────────
    d = _dump(t1=(403, 4.5e-3), t3=(158749, 0.5e-3))
    m, notes, errs = resolve(_DECK_PS_10_0, d)
    chk('① ★ 실사고 재현 — ps_10_0 덱+덤프 → 1:AM_P,3:SE', format_map(m) == '1:AM_P,3:SE',
        format_map(m))
    chk('①b 빈 type 2 는 오류가 아니라 note 다 (설계상 비는 팔)', not errs, errs)

    # ── ② 기존 동작 보존 — 옛 2타입 덱 ────────────────────────────────────
    m2, _, e2 = resolve(_DECK_OLD_2TYPE, _dump(t1=(500, 3.0e-3), t2=(9000, 1.0e-3)))
    chk('② 옛 덱 r_AM 3.0e-3 → 1:AM_S,2:SE  (반지름 ≤ 0.004 규칙 보존)',
        format_map(m2) == '1:AM_S,2:SE' and not e2, format_map(m2))
    m3, _, _ = resolve(_DECK_OLD_BIG_AM, _dump(t1=(500, 6.0e-3), t2=(9000, 1.0e-3)))
    chk('②b 옛 덱 r_AM 6.0e-3 → 1:AM_P,2:SE', format_map(m3) == '1:AM_P,2:SE',
        format_map(m3))

    # ── ③ 세 타입이 다 있는 팔 ────────────────────────────────────────────
    m4, _, e4 = resolve(_DECK_PS_10_0,
                        _dump(t1=(300, 4.5e-3), t2=(900, 2.0e-3), t3=(120000, 0.5e-3)))
    chk('③ 세 타입 다 있으면 1:AM_P,2:AM_S,3:SE',
        format_map(m4) == '1:AM_P,2:AM_S,3:SE' and not e4, format_map(m4))

    # ── ④ ★★ 음성 대조: 사고 당시의 틀린 map 을 검증하면 **반드시** 거부 ──
    bad = parse_map('1:AM_P,2:SE')
    errs_bad, notes_bad = validate(bad, d)
    chk('④ ★★ 음성 대조: 사고 당시 map(1:AM_P,2:SE)을 그 덤프에 대면 거부한다',
        len(errs_bad) == 1 and 'type 3' in errs_bad[0])
    chk('④b 거부 메시지가 **몫**을 말한다 (99.75 %)',
        any('99.7' in e for e in errs_bad), errs_bad[:1])
    chk('④c 빈 type 2 는 note 로만 (같은 호출에서 치명이 아니다)',
        len(notes_bad) == 1 and 'type 2' in notes_bad[0])

    # ── ⑤ ★ 판별력: 올바른 map 은 통과해야 한다 (검사가 공허하지 않음) ────
    good_errs, _ = validate(parse_map('1:AM_P,3:SE'), d)
    chk('⑤ ★ 올바른 map 은 통과 — 검사가 무조건 거부하는 것이 아니다', not good_errs)

    # ── ⑥ 덱·덤프 불일치 (다른 런의 덤프를 붙인 경우) ─────────────────────
    _, _, e6 = resolve(_DECK_PS_10_0, _dump(t1=(403, 6.0e-3), t3=(158749, 0.5e-3)))
    chk('⑥ 덱 반지름과 덤프 반지름이 다르면 거부',
        any('덱 반지름' in e for e in e6), e6[:1])

    # ── ⑦ 모르는 변수는 **추측하지 않고** 거부 ────────────────────────────
    _, _, e7 = resolve(_DECK_UNKNOWN_VAR, _dump(t1=(10, 1.0e-3)))
    chk('⑦ ★ 모르는 변수 ${r_MYSTERY} 는 추측하지 않고 거부', any('모르는 변수' in e for e in e7),
        e7[:1])

    # ── ⑧ 덤프 리더가 실물 형식을 읽는가 (합성 파일로) ────────────────────
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, 'atom_1.liggghts')
        with open(p, 'w') as fh:
            fh.write('ITEM: TIMESTEP\n1\nITEM: NUMBER OF ATOMS\n3\n'
                     'ITEM: BOX BOUNDS pp pp ff\n0 1\n0 1\n0 1\n'
                     'ITEM: ATOMS id type x y z radius\n'
                     '1 1 0 0 0 4.5e-3\n2 3 0 0 0 5.0e-4\n3 3 0 0 0 5.0e-4\n')
        got = types_in_dump(p)
        c = os.path.join(td, 'atoms.csv')
        with open(c, 'w') as fh:
            fh.write('id,type,x,y,z,radius\n1,1,0,0,0,0.0045\n'
                     '2,3,0,0,0,0.0005\n3,3,0,0,0,0.0005\n')
        got_csv = types_in_dump(c)
    chk('⑧ LIGGGHTS 덤프를 읽는다 (type 1:1개 · 3:2개)',
        got.get(1, {}).get('n') == 1 and got.get(3, {}).get('n') == 2, got)
    chk('⑧b atoms.csv 도 같은 답을 낸다 (파이프라인 두 지점에서 같은 판정)',
        {t: v['n'] for t, v in got_csv.items()} == {t: v['n'] for t, v in got.items()},
        got_csv)

    # ── ⑨ 문자열 왕복 ─────────────────────────────────────────────────────
    chk('⑨ parse_map ∘ format_map 왕복',
        format_map(parse_map(' 1:AM_P , 3:SE ')) == '1:AM_P,3:SE')

    # ── ⑩b 메모리 경로와 파일 경로가 같은 답을 내는가 (두 지점 일관성) ──
    pairs = [(1, 4.5e-3)] + [(3, 5.0e-4)] * 2
    chk('⑩b types_from_pairs 가 파일 리더와 같은 답',
        {t: v['n'] for t, v in types_from_pairs(pairs).items()} == {1: 1, 3: 2})

    # ── ⑩ app.py 경계 계약 — import · 호출 · 문턱 단일화 (fail-CLOSED) ────
    ap = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      'webapp', 'app.py')
    _ap_ok = os.path.exists(ap)
    _src = open(ap, encoding='utf-8', errors='replace').read() if _ap_ok else ''
    _werr = app_wiring_errors(_src, exists=_ap_ok)
    chk('⑩ ★ app.py 가 이 모듈을 실제로 쓴다 (import · 호출 · 문턱 단일화)',
        not _werr, _werr)

    # ── ⑩c ★★ 그 검사가 공허하지 않은가 — 음성 대조 넷 + 양성 대조 하나 ──
    #   초판 ⑩ 은 아래 넷을 **전부 통과**시켰다 (부분문자열 + fail-open).
    _GOOD = ('import type_map_resolve as _t\n'
             'm, n, e = _t.resolve_from_files(d, a)\n'
             'x = r > _t.AM_P_RADIUS_CUT_SIM\n')
    for _label, _args, _want_fail in (
            ('메타 키 이름만 남은 app.py', ("meta = {'type_map_resolved': None}\n",), True),
            ('app.py 자체가 없음 (fail-closed)', ('', False), True),
            ('import 만 있고 호출이 없음', ('import type_map_resolve as _t\n',), True),
            ('문턱 0.004 를 리터럴로 다시 박음', (_GOOD + "y = r > 0.004\n",), True),
            ('올바른 배선 (양성 대조)', (_GOOD,), False)):
        _e = app_wiring_errors(*_args)
        chk(f'⑩c {"거부" if _want_fail else "통과"}: {_label}',
            bool(_e) == _want_fail, _e if bool(_e) != _want_fail else '')

    print()
    if fails:
        print(f'⛔ {len(fails)} FAIL: ' + ' · '.join(fails))
        return 1
    print(f'✅ selftest {_N_CHECKS[0]}/{_N_CHECKS[0]}')
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description='덱에서 atom-type ↔ 상 매핑을 읽고 덤프로 검증한다')
    ap.add_argument('--deck', help='LIGGGHTS 입력 덱 (in.*.liggghts)')
    ap.add_argument('--atoms', help='원자 덤프(.liggghts) 또는 atoms.csv')
    ap.add_argument('--check-map', help='이 type_map 이 덤프와 맞는지만 본다 (예: 1:AM_P,3:SE)')
    ap.add_argument('--quiet', action='store_true', help='최종 매핑 한 줄만 출력')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()

    if a.selftest:
        return selftest()
    if not a.atoms:
        ap.error('--atoms 가 필요하다')
    dump = types_in_dump(a.atoms)

    if a.check_map:
        errs, notes = validate(parse_map(a.check_map), dump)
        for n in notes:
            print(n)
        for e in errs:
            print(e)
        return 1 if errs else 0

    if not a.deck:
        ap.error('--deck 이 필요하다 (또는 --check-map)')
    m, notes, errs = resolve_from_files(a.deck, a.atoms)
    if a.quiet:
        if errs:
            for e in errs:
                print(e, file=sys.stderr)
            return 1
        print(format_map(m))
        return 0
    print('덤프의 타입:')
    for t in sorted(dump):
        print(f'  type {t}: {dump[t]["n"]:,}개  r {dump[t]["r_min"]:.4e}'
              f'~{dump[t]["r_max"]:.4e}')
    print('\n덱 판독:')
    for n in notes:
        print('  ' + n)
    if errs:
        print()
        for e in errs:
            print('  ' + e)
        return 1
    print(f'\n✅ type_map = {format_map(m)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
