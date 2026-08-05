#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""기존 LIGGGHTS 덱 하나에서 **압력만 다른** 덱 시리즈를 찍어낸다 (Heckel/하중평형 검증용).

═══ 무엇을 위한 것인가 ═════════════════════════════════════════════════════════════════
`am_load_balance_jam.py` 의 비순환 검증은 **하나의 H_AM 이 여러 압력의 DEM 두께를 동시에
재현**하는지 보는 것이다.  그러려면 같은 베드·같은 시드로 P 만 바꾼 DEM 런이 필요하다.
시드가 다르면 패킹이 달라져 압력 효과와 시드 효과가 섞인다 → **시드는 절대 건드리지 않는다**
(heckel/ 덱이 이미 "Same insert seed across the series → paired compaction snapshots" 규약).

바꾸는 것은 딱 둘:
  1. `variable target_press equal <P>`  (덱 단위)
  2. 출력 태그 (post_<TAG>/ · restart_<TAG>/ · plate_<TAG>.stl …) — 런끼리 안 덮어쓰게

═══ 단위 함정 (이 스크립트가 막는 것) ══════════════════════════════════════════════════
이 리포의 덱은 스케일 규약이 `r×1000, E×0.001, P×0.001` 이라 **300 MPa 가 덱에서는 0.300**
이다.  손으로 고치면 1000× 틀리기 딱 좋다.  그래서 이 스크립트는 원본 덱의 target_press 와
태그에 박힌 숫자(예 `..._300`)를 **교차검증**하고, 안 맞으면 덱을 만들지 않고 죽는다.

  python3 scripts/make_pressure_sweep_decks.py --deck heckel/input_SE_heckel_300.liggghts \\
      --pressures 100,300,600 --out /tmp/psweep
  python3 scripts/make_pressure_sweep_decks.py --deck ~/dem/input_real_14.liggghts \\
      --pressures 100,300,600 --tag real_14 --current-mpa 300 --out ~/dem/psweep
"""
from __future__ import annotations

import argparse
import os
import re
import sys

RE_TARGET = re.compile(r'^(\s*variable\s+target_press\s+equal\s+)([0-9.eE+-]+)\s*$', re.M)
RE_MKDIR = re.compile(r'^\s*shell\s+mkdir\s+post_(\S+)\s*$', re.M)


def detect_tag(text):
    """덱이 실제로 쓰는 출력 태그 (`shell mkdir post_<TAG>`)."""
    m = RE_MKDIR.search(text)
    return m.group(1) if m else ''


def read_target(text):
    m = RE_TARGET.search(text)
    if not m:
        sys.exit('덱에 `variable target_press equal <값>` 이 없습니다 — 압력 스윕을 만들 수 없음')
    return float(m.group(2))


def infer_scale(target_deck, current_mpa):
    """덱 단위 / MPa.  이 리포 규약은 0.001 이지만 **추정하지 않고 검증한다**."""
    if current_mpa <= 0:
        sys.exit('--current-mpa 를 알 수 없습니다 (태그에 숫자가 없으면 직접 주세요)')
    s = target_deck / current_mpa
    for cand, name in ((1e-3, 'P×0.001 (이 리포 규약)'), (1.0, '덱이 MPa 그대로'),
                       (1e-6, '덱이 Pa→?')):
        if abs(s - cand) / cand < 0.02:
            return cand, name
    sys.exit(f'단위 규약을 인식 못 함: target_press={target_deck} vs {current_mpa} MPa '
             f'→ 비 {s:.6g}.  덱을 확인하세요 (1000× 실수 방지용 가드)')


def _fmt_like(sample, value):
    """원본 표기 스타일을 따라 값을 찍는다 (0.300 → 0.100, 0.3 → 0.1).

    손으로 만든 heckel 덱들과 **바이트 동일**하게 나오는지가 이 생성기의 검산이므로
    소수 자릿수까지 맞춘다 — 표기만 다른 diff 는 검산을 무력화한다.
    """
    if '.' in sample and 'e' not in sample.lower():
        return f'{value:.{len(sample.split(".")[1])}f}'
    return f'{value:.6g}'


def make_deck(text, tag_old, tag_new, p_deck, mpa_old=0.0, mpa_new=0.0):
    # 값이 같으면 원문 문자열을 보존한다 (0.300 → 0.3 같은 표기 변화만으로 diff 가 뜨면
    # "덱이 바뀐 건가?" 를 매번 다시 확인하게 된다 — 재생성이 멱등이어야 한다)
    def sub(m):
        return (m.group(0) if float(m.group(2)) == p_deck
                else f'{m.group(1)}{_fmt_like(m.group(2), p_deck)}')
    out = RE_TARGET.sub(sub, text, count=1)
    if tag_old and tag_new != tag_old:
        out = out.replace(tag_old, tag_new)
    # 주석과 print 문에 박힌 압력도 같이 고친다.  안 고치면 100 MPa 덱 머리에 "at 300 MPa" 가,
    # 로그에 "COMPRESSION to 300 MPa" 가 남아 **어느 런이 어느 압력인지 로그로 판단하다 틀린다**
    # (실제로 손수 만든 100 MPa 덱과 대조해 발견한 누락).  숫자 변수는 건드리지 않는다.
    if mpa_old > 0 and mpa_new > 0 and mpa_old != mpa_new:
        pat = re.compile(rf'\b{re.escape(f"{mpa_old:g}")}(\s*MPa)')
        lines = []
        for ln in out.split('\n'):
            if ln.lstrip().startswith('#') or 'print "' in ln:
                ln = pat.sub(lambda m: f'{mpa_new:g}{m.group(1)}', ln)
            lines.append(ln)
        out = '\n'.join(lines)
    # ★ 헤더가 자기 압력을 밝히게 한다.  원본 주석에 "300 MPa" 같은 문자열이 아예 없는 덱이
    #   흔한데(real_14 이 그렇다 — 헤더에 압력 언급 자체가 없다), 그러면 생성본 셋이 겉보기에
    #   구분되지 않아 나중에 파일을 잘못 짚는다.  압력·원본·불변항을 한 블록으로 맨 위에 박는다.
    if mpa_new > 0:
        out = (f'# ===== 압력 스윕 생성본 (make_pressure_sweep_decks.py) =====\n'
               f'#   P = {mpa_new:g} MPa   (덱 단위 target_press = {_fmt_like("0.000", p_deck)};'
               f'  규약 Scale r×1000 · E×0.001 · P×0.001)\n'
               f'#   원본 {mpa_old:g} MPa 덱에서 **P 와 출력 태그만** 변경.\n'
               f'#   시드 · 재료(property/global) · 접촉법칙 · press_speed · dt · 삽입조건 전부\n'
               f'#   불변 — 압력 효과와 패킹/rate 효과를 섞지 않기 위함.\n') + out
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--deck', help='원본 .liggghts 덱')
    ap.add_argument('--pressures', default='100,300,600', help='MPa, 쉼표 구분')
    ap.add_argument('--tag', default='', help='출력 태그 (기본 = 덱에서 자동 검출)')
    ap.add_argument('--current-mpa', type=float, default=0.0,
                    help='원본 덱의 압력 (MPa).  기본 = 태그 끝 숫자에서 읽음')
    ap.add_argument('--out', default='psweep', help='덱을 쓸 디렉터리')
    ap.add_argument('--mpi', type=int, default=10, help='실행 명령에 찍을 MPI 랭크 수')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)

    if a.selftest:
        return _selftest()
    if not a.deck:
        ap.error('--deck 이 필요합니다 (또는 --selftest)')

    text = open(a.deck).read()
    tag = a.tag or detect_tag(text)
    if not tag:
        sys.exit('출력 태그를 찾지 못했습니다 (`shell mkdir post_<TAG>` 부재) → --tag 로 주세요')
    m = re.search(r'(\d+)\s*$', tag)
    tail = float(m.group(1)) if m else None
    cur = a.current_mpa if a.current_mpa > 0 else (tail or 0.0)
    scale, how = infer_scale(read_target(text), cur)

    os.makedirs(a.out, exist_ok=True)
    # ★ 태그 끝 숫자가 **압력**인 경우에만 떼어낸다.  `SE_heckel_300` 은 압력이지만
    #   `real_14` 의 14 는 **케이스 번호**다 — 그걸 떼면 real_100/real_300 이 되어 케이스
    #   정체성이 사라지고 다른 케이스와 충돌할 수도 있다.  판별: 끝 숫자가 원본 압력과
    #   같을 때만 압력으로 본다.  아니면 태그를 통째로 두고 `_P<압력>` 을 덧붙인다.
    tail_is_pressure = tail is not None and abs(tail - cur) < 1e-9
    base = re.sub(r'_?\d+$', '', tag) if tail_is_pressure else tag
    print(f'  태그 끝 숫자 {("= 압력 → 교체" if tail_is_pressure else "≠ 압력(케이스 번호) → 보존하고 _P 접미")}'
          f'  ·  새 태그 몸통 "{base}"')
    print(f'원본 {a.deck}\n  태그 {tag}  ·  현재 압력 {cur:g} MPa  ·  단위 {how}\n')
    cmds = []
    for p in [float(x) for x in a.pressures.split(',') if x.strip()]:
        tag_new = (f'{base}_{int(round(p))}' if tail_is_pressure
                   else f'{base}_P{int(round(p))}')
        path = os.path.join(a.out, f'input_{tag_new}.liggghts')
        with open(path, 'w') as f:
            f.write(make_deck(text, tag, tag_new, p * scale, cur, p))
        print(f'  {p:6.0f} MPa → {path}   (target_press={p * scale:g}, 태그 {tag_new})')
        cmds.append(f'mpirun --oversubscribe -np {a.mpi} liggghts -in {path} '
                    f'2>&1 | tee log_{tag_new}.out')

    print('\n실행 (직렬 — 같은 머신에서 동시에 돌리면 서로 느려집니다):')
    for c in cmds:
        print(f'  {c}')
    print('\n끝난 뒤: 각 런의 마지막 atom/contact 덤프 → 케이스 폴더 → '
          '`mpm_input_from_case.py` 로\n  am_scaffold.csv / se_scaffold.csv 를 뽑고, '
          '두께와 함께 매니페스트에 적어\n  `am_load_balance_jam.py --cases` 로 판정합니다.')
    print('\n★ 시드는 건드리지 않았습니다 — 세 런이 같은 초기 패킹에서 갈라져야 '
          '압력 효과와 시드 효과가 섞이지 않습니다.')
    return 0


def _selftest():
    ok, fail = 0, []

    def chk(name, cond):
        nonlocal ok
        if cond:
            ok += 1
        else:
            fail.append(name)

    deck = ('# demo\nvariable target_press equal 0.300\nshell mkdir post_SE_heckel_300\n'
            'restart 50000 restart_SE_heckel_300/r_*.bin\nfix pts1 all particletemplate/sphere '
            '32452843 atom_type 1\n')
    chk('태그 자동 검출', detect_tag(deck) == 'SE_heckel_300')
    chk('target_press 읽기', abs(read_target(deck) - 0.300) < 1e-12)
    sc, _ = infer_scale(0.300, 300.0)
    chk('단위 규약 P×0.001 인식', abs(sc - 1e-3) < 1e-12)

    # ★ 1000× 사고 방지 가드가 실제로 죽는지
    try:
        infer_scale(300.0, 300.0)
        chk('덱이 MPa 그대로인 경우도 인식', True)
    except SystemExit:
        fail.append('MPa-그대로 규약이 거부됨')
    try:
        infer_scale(0.300, 47.0)                # 어느 규약에도 안 맞음
        fail.append('말이 안 되는 비율이 통과됨 (가드 미작동)')
    except SystemExit:
        ok += 1

    out600 = make_deck(deck, 'SE_heckel_300', 'SE_heckel_600', 0.600, 300.0, 600.0)
    chk('압력이 덱 단위로 치환 (원본 자릿수 유지)',
        'variable target_press equal 0.600\n' in out600)
    chk('출력 태그가 전부 갈림 (post_)', 'post_SE_heckel_600' in out600
        and 'post_SE_heckel_300' not in out600)
    chk('출력 태그가 전부 갈림 (restart_)', 'restart_SE_heckel_600/' in out600)
    chk('★ 시드는 불변 — 압력 효과와 시드 효과를 섞지 않는다', '32452843' in out600)
    chk('원본 덱은 그대로 (in-place 수정 아님)', 'equal 0.300' in deck)

    cmt = make_deck('# Heckel point at 300 MPa\nvariable target_press equal 0.300\n'
                    'variable foo equal 300\n', '', '', 0.100, 300.0, 100.0)
    chk('주석의 압력 표기도 함께 갱신 (덱 머리가 거짓말하지 않게)',
        '# Heckel point at 100 MPa' in cmt)
    chk('주석이 아닌 줄의 300 은 건드리지 않는다', 'variable foo equal 300' in cmt)

    # ★ print 문도 고쳐야 한다 — 안 고치면 로그가 "COMPRESSION to 300 MPa" 라고 거짓말한다
    pr = make_deck('print "====== COMPRESSION to 300 MPa ======"\n'
                   'variable target_press equal 0.300\n', '', '', 0.600, 300.0, 600.0)
    chk('print 문의 압력 표기도 갱신 (로그가 거짓말하지 않게)',
        'COMPRESSION to 600 MPa' in pr)
    chk('표기 자릿수를 원본에 맞춘다 (0.300 → 0.600)',
        'variable target_press equal 0.600' in pr)

    same = make_deck(deck, 'SE_heckel_300', 'SE_heckel_300', 0.300, 300.0, 300.0)
    chk('같은 압력·같은 태그면 본문 바이트 동일 (헤더만 추가)', same.endswith(deck))
    chk('★ 생성본 헤더가 자기 압력을 밝힌다 (원본에 MPa 문자열이 없어도)',
        'P = 600 MPa' in out600 and 'target_press = 0.600' in out600)
    chk('헤더가 불변항을 명시 (시드/재료/rate)', '시드' in out600 and 'press_speed' in out600)
    chk('헤더는 전부 주석 — LIGGGHTS 파싱에 영향 없음',
        all(l.startswith('#') for l in out600.split('\n')[:5]))

    # ★ 태그 끝 숫자가 압력일 때만 떼어낸다.  `real_14` 의 14 는 케이스 번호다 —
    #   그걸 압력으로 오인해 떼면 real_100/real_300 이 되어 케이스 정체성이 사라진다.
    def tag_for(tag, cur, p):
        m = re.search(r'(\d+)\s*$', tag)
        tail = float(m.group(1)) if m else None
        is_p = tail is not None and abs(tail - cur) < 1e-9
        b = re.sub(r'_?\d+$', '', tag) if is_p else tag
        return f'{b}_{int(p)}' if is_p else f'{b}_P{int(p)}'
    chk('끝 숫자 = 압력이면 교체 (SE_heckel_300 @300 → SE_heckel_100)',
        tag_for('SE_heckel_300', 300, 100) == 'SE_heckel_100')
    chk('★ 끝 숫자 ≠ 압력이면 보존하고 _P 접미 (real_14 @300 → real_14_P100)',
        tag_for('real_14', 300, 100) == 'real_14_P100')
    chk('★ 케이스 번호가 사라지지 않는다', 'real_14' in tag_for('real_14', 300, 600))
    chk('숫자 없는 태그도 _P 접미', tag_for('bimodal', 300, 600) == 'bimodal_P600')

    print(f'selftest: {ok}/{ok + len(fail)} PASS' + (f'   FAILED: {fail}' if fail else ''))
    return 0 if not fail else 1


if __name__ == '__main__':
    sys.exit(main())
