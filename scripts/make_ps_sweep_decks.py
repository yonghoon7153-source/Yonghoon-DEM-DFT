#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""기존 LIGGGHTS 덱 하나에서 **조성(P:S)만 다른** 덱 시리즈를 찍어낸다 (이종기술 6 mAh 계열).

═══ 무엇을 위한 것인가 ═════════════════════════════════════════════════════════════════
`make_pressure_sweep_decks.py` 의 조성판이다.  그쪽은 압력만 바꾸고 **시드를 얼린다**
(압력 효과와 패킹 효과를 섞지 않으려고).  이쪽은 반대다 — 조성이 바뀌면 삽입 스트림이
어차피 첫 입자부터 갈라지므로 "같은 패킹" 이라는 것이 **존재하지 않는다**.  그래서 케이스마다
독립적인 큰 소수 시드를 준다 (LIGGGHTS 관례 = 큰 소수; `--shared-seeds` 로 끌 수 있다).

바꾸는 것:
  1. `particledistribution/discrete` 의 **질량분율** (+ 그 위 주석)
  2. 시드 5개 (particletemplate ×3 · particledistribution · insert/pack) → 8자리 소수
  3. 출력 태그 (post_/restart_/plate_*.stl/print) — 런끼리 안 덮어쓰게
  4. `--r-am-p` 를 주면 AM_P 반지름 (+ 그 주석)

바꾸지 않는 것: 재료(property/global) · 접촉법칙 · dt · press_speed · target_press ·
volumefraction · run 스텝수 · RVE.  **E_SE 는 원본 그대로** (이 리포 규약은 연화된 1.35 GPa
= `0.135e7` 이고, 표에 적힌 실bulk 24 GPa 가 아니다 — CLAUDE.md E_SE calibration 절).

═══ 질량분율인가 개수분율인가 (이 스크립트가 막는 것) ═══════════════════════════════════
`particledistribution/discrete` 의 분율을 **개수**로 읽으면 SE 18.4 % 는 사실상 SE 가 없는
침대가 된다 (SE 입자 하나가 AM_P 의 1/4000 질량).  우리 덱은 **질량분율**이고, 그것은 추정이
아니라 실측으로 확인됐다 — 4/21 런의 입자수(AM_P 175 · SE 158,730)가 질량분율 계산
(170 · 158,765)과 맞고 개수분율 계산(4.43 : 1)과는 4자릿수 어긋난다.
그래서 이 스크립트는 **덱에서 읽은 분율로 입자수를 예측해 찍는다** — 런 뒤 실제 개수와
대조하면 규약이 뒤집혔는지 즉시 보인다.

  python3 scripts/make_ps_sweep_decks.py --deck docs/data/phase_a_6mah/in.real_4.liggghts \\
      --ratios 10:0,7:3,5:5,3:7,0:10 --r-am-p 4.5e-3 --tag-suffix _r45 --out dem_scripts/psweep
"""
from __future__ import annotations

import argparse
import math
import os
import re
import sys

RE_MKDIR = re.compile(r'^\s*shell\s+mkdir\s+post_(\S+)\s*$', re.M)
RE_VAR = re.compile(r'^(\s*variable\s+{}\s+equal\s+)([0-9.eE+-]+)(.*)$', re.M)
RE_PTS = re.compile(r'^(\s*fix\s+(\S+)\s+all\s+particletemplate/sphere\s+)(\d+)'
                    r'(\s+atom_type\s+(\d+).*)$', re.M)
#  ⚠ `\s` 는 개행도 먹는다 — 처음 판이 분포 줄 **뒤의 빈 줄을 삼켜** 원본과 쓸데없는 diff 를
#    냈다.  의도한 변경만 diff 에 남아야 검산이 된다 ⇒ 줄 안에서만 움직이는 `[ \t]` 로 고정.
RE_PDD = re.compile(r'^([ \t]*fix[ \t]+\S+[ \t]+all[ \t]+particledistribution/discrete[ \t]+)'
                    r'(\d+)[ \t]+(\d+)[ \t]+'
                    r'(\S+(?:[ \t]+[0-9.eE+-]+[ \t]*\S*)*?)[ \t]*$', re.M)
RE_INS = re.compile(r'^(\s*fix\s+\S+\s+all\s+insert/pack\s+seed\s+)(\d+)(.*)$', re.M)
RE_VF = re.compile(r'volumefraction_region\s+([0-9.eE+-]+)')
RE_REGMIX = re.compile(r'^\s*region\s+\S+\s+block\s+([0-9.eE+-]+)\s+([0-9.eE+-]+)\s+'
                       r'([0-9.eE+-]+)\s+([0-9.eE+-]+)\s+([0-9.eE+-]+)\s+([0-9.eE+-]+)', re.M)
RE_DENS = re.compile(r'density\s+constant\s+([0-9.eE+-]+)')
RE_RAD = re.compile(r'radius\s+constant\s+\$\{(\w+)\}')

#: 시드 = 8자리 소수.  LAMMPS/LIGGGHTS RNG(RanPark)가 9자리(9e8) 위를 거부하는 판이 있어
#: 원본 덱과 같은 자릿수 대역(1e7~1e8)에 둔다.  ⚠ 아래 세 상수를 바꾸면 시드가 전부 바뀐다
#: = 다른 침대가 된다.  바꾸지 말 것 (재현성).
SEED_BASE, SEED_STEP, SEED_SUB = 20_000_000, 7_000_000, 1_300_000


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    f = 3
    while f * f <= n:
        if n % f == 0:
            return False
        f += 2
    return True


def next_prime(n: int) -> int:
    n = max(3, n | 1)
    while not is_prime(n):
        n += 2
    return n


def seeds_for(case_idx: int, n: int = 5):
    """케이스 하나가 쓰는 시드 n 개 — 결정적이라 재생성이 멱등이다."""
    return [next_prime(SEED_BASE + case_idx * SEED_STEP + j * SEED_SUB) for j in range(n)]


def fmt_frac(v: float) -> str:
    """0.5712 / 0.184 / 0.816 처럼 원본 표기(불필요한 0 없음)로."""
    return f'{v:.6f}'.rstrip('0').rstrip('.') or '0'


def parse_ratio(tok: str):
    p, s = tok.split(':')
    p, s = int(p), int(s)
    if p < 0 or s < 0 or p + s == 0:
        sys.exit(f'말이 안 되는 P:S {tok!r}')
    return p, s


def compose(p: int, s: int, am_mass: float):
    """AM_P · AM_S · SE 의 **질량분율**.  P:S 는 AM 안의 질량 분할이다."""
    if not 0 < am_mass < 1:
        sys.exit(f'AM 질량분율이 (0,1) 밖: {am_mass} — SE 분율이 음수/0 이 된다')
    t = p + s
    fr = {'AM_P': am_mass * p / t, 'AM_S': am_mass * s / t, 'SE': 1.0 - am_mass}
    if abs(sum(fr.values()) - 1.0) > 1e-12:                    # LIGGGHTS 는 합 1 을 요구한다
        sys.exit(f'질량분율 합이 1 이 아님: {fr}')
    return fr


def read_deck(text: str):
    """덱에서 **실물**을 읽는다 (이름 조각으로 추측하지 않는다 — 규율 ⑤)."""
    tpl = {}                                                    # fixname → (seed, atom_type)
    for m in RE_PTS.finditer(text):
        tpl[m.group(2)] = dict(seed=int(m.group(3)), atype=int(m.group(5)),
                               dens=float(RE_DENS.search(m.group(0)).group(1))
                               if RE_DENS.search(m.group(0)) else 0.0,
                               rvar=RE_RAD.search(m.group(0)).group(1)
                               if RE_RAD.search(m.group(0)) else '')
    m = RE_PDD.search(text)
    if not m or not tpl:
        sys.exit('덱에 particletemplate/sphere 또는 particledistribution/discrete 가 없습니다')
    toks = m.group(4).split()
    ent = [(toks[i], float(toks[i + 1])) for i in range(0, len(toks) - 1, 2)]
    if int(m.group(3)) != len(ent):
        sys.exit(f'분포의 템플릿 개수 {m.group(3)} 가 실제 항목 {len(ent)} 와 다릅니다')
    return tpl, ent


def region_solid_volume(text: str):
    """삽입 구역의 고체 부피 = 구역 부피 × volumefraction.  입자수 예측용."""
    vf = RE_VF.search(text)
    regs = RE_REGMIX.findall(text)
    if not vf or not regs:
        return 0.0
    x0, x1, y0, y1, z0, z1 = (float(v) for v in regs[-1])       # 삽입 region 이 마지막
    return abs((x1 - x0) * (y1 - y0) * (z1 - z0)) * float(vf.group(1))


def predict_counts(text: str, tpl, entries, radii):
    """질량분율 → 입자수.  규약이 개수분율로 뒤집히면 이 예측이 4자릿수 틀려 바로 보인다."""
    v_solid = region_solid_volume(text)
    if v_solid <= 0:
        return {}
    vol = {n: 4 / 3 * math.pi * radii.get(tpl[n]['rvar'], 0.0) ** 3 for n, _ in entries}
    denom = sum(f * vol[n] / (tpl[n]['dens'] * vol[n]) if False else f / tpl[n]['dens']
                for n, f in entries)                            # Σ w_i/ρ_i = 단위질량당 부피
    out = {}
    for n, f in entries:
        if f <= 0 or vol[n] <= 0:
            out[n] = 0
            continue
        out[n] = int(round(v_solid * (f / tpl[n]['dens']) / denom / vol[n]))
    return out


def _sub_line(text: str, fn):
    """주석(`#`)과 `print` 문에만 치환을 적용한다 — 숫자 변수는 건드리지 않는다."""
    return '\n'.join(fn(ln) if (ln.lstrip().startswith('#') or 'print "' in ln) else ln
                     for ln in text.split('\n'))


def make_deck(text, tag_old, tag_new, p, s, seeds, r_am_p='', am_mass=0.816, note=''):
    tpl, ent = read_deck(text)
    by_type = {v['atype']: k for k, v in tpl.items()}
    want = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}
    if set(by_type) != set(want):
        sys.exit(f'atom_type 구성이 예상과 다릅니다: {sorted(by_type)} (1=AM_P,2=AM_S,3=SE 가정)')
    fr = compose(p, s, am_mass)
    out = text

    # ── 1) AM_P 반지름 (주면) ──
    radii = {}
    for var in ('r_AM_P', 'r_AM_S', 'r_SE'):
        m = RE_VAR.format(var) if False else re.compile(RE_VAR.pattern.format(var), re.M)
        g = m.search(out)
        if g:
            radii[var] = float(g.group(2))
    if r_am_p:
        rx = re.compile(RE_VAR.pattern.format('r_AM_P'), re.M)
        old_um = radii.get('r_AM_P', 0.0) * 1e3                 # Sim m → 실 µm (scale ×1000)
        new_um = float(r_am_p) * 1e3
        out = rx.sub(lambda m: f'{m.group(1)}{r_am_p}{m.group(3)}', out, count=1)
        radii['r_AM_P'] = float(r_am_p)
        if old_um and abs(old_um - new_um) > 1e-12:             # 주석의 µm 표기도 같이
            pat = re.compile(rf'(AM_P\s+r=){old_um:g}(\s*(?:µ|μ)m)')
            out = pat.sub(lambda m: f'{m.group(1)}{new_um:g}{m.group(2)}', out)
            out = out.replace(f'Sim {old_um:g}mm', f'Sim {new_um:g}mm')

    # ── 2) 시드 (템플릿 3 · 분포 · 삽입) ──
    it = iter(seeds)
    out = RE_PTS.sub(lambda m: f'{m.group(1)}{next(it)}{m.group(4)}', out)
    pdd_seed, ins_seed = next(it), next(it)

    # ── 3) 질량분율 ──
    keep = [(n, fr[want[tpl[n]['atype']]]) for n, _ in ent if fr[want[tpl[n]['atype']]] > 0]
    body = ' '.join(f'{n} {fmt_frac(f)}' for n, f in keep)
    out = RE_PDD.sub(lambda m: f'{m.group(1)}{pdd_seed} {len(keep)} {body}', out, count=1)
    out = RE_INS.sub(lambda m: f'{m.group(1)}{ins_seed}{m.group(3)}', out, count=1)
    #   빠진 템플릿은 정의만 남고 안 쓰인다 (LIGGGHTS 무해) — 덱이 스스로 밝히게 한다
    drop = [n for n, _ in ent if n not in dict(keep)]
    for n in drop:
        out = re.sub(rf'^(\s*fix\s+{re.escape(n)}\s+all\s+particletemplate/sphere.*)$',
                     lambda m: f'{m.group(1)}   # (이 케이스 질량분율 0 — 분포에서 제외)',
                     out, count=1, flags=re.M)

    # ── 4) 태그 · 주석·print 의 조성 표기 ──
    if tag_old and tag_new != tag_old:
        out = out.replace(tag_old, tag_new).replace(tag_old.upper(), tag_new.upper())
    ratio_new = f'{p}:{s}'
    out = _sub_line(out, lambda ln: re.sub(r'(P:S\s*=\s*)\d+:\d+', rf'\g<1>{ratio_new}', ln))
    out = _sub_line(out, lambda ln: re.sub(r'(P:S=)\d+:\d+', rf'\g<1>{ratio_new}', ln))
    modal = ('Bimodal' if p and s else
             'Monomodal AM_P' if p else 'Monomodal AM_S')
    out = _sub_line(out, lambda ln: re.sub(r'\((?:Bimodal|Monomodal AM_[PS])\)',
                                           f'({modal})', ln))
    #   질량비 주석 — 덱 머리가 거짓말하지 않게 (압력 스윕에서 배운 것)
    out = re.sub(r'^#\s*질량비:.*$',
                 '# 질량비: ' + ', '.join(f'{want[tpl[n]["atype"]]}:{fmt_frac(f)}'
                                          for n, f in keep), out, count=1, flags=re.M)

    # ── 5) 생성본 헤더 ──
    cnt = predict_counts(out, tpl, keep, radii)
    rline = ' · '.join(f'{want[tpl[n]["atype"]]} r={radii.get(tpl[n]["rvar"], 0) * 1e3:g}µm'
                       for n, _ in ent)
    head = [f'# ===== P:S 스윕 생성본 (make_ps_sweep_decks.py) =====',
            f'#   P:S = {ratio_new}   ({modal})   ·  AM:SE = '
            f'{am_mass * 100:g}:{(1 - am_mass) * 100:g} (질량)',
            f'#   {rline}   (규약 Scale r×1000 · E×0.001 · P×0.001)',
            f'#   질량분율 → 예상 입자수  ' +
            ' · '.join(f'{want[tpl[n]["atype"]]} {cnt.get(n, 0):,}' for n, _ in ent) +
            f'  (합 {sum(cnt.values()):,})',
            f'#     ⇒ 런 뒤 실제 개수와 대조할 것.  4자릿수 어긋나면 분포가 **개수분율**로',
            f'#       읽힌 것이다 (질량분율 규약이 깨진 것 = 침대가 다른 물건).',
            f'#   시드(큰 소수, 케이스마다 독립): ' + ', '.join(str(x) for x in seeds),
            f'#   원본 덱에서 **조성·시드·태그' + ('·AM_P 반지름' if r_am_p else '') +
            '만** 변경.  재료(E_SE 포함) · 접촉법칙 ·',
            f'#   dt · press_speed · target_press · volumefraction · RVE · run 스텝수 전부 불변.']
    if note:
        head.append(f'#   {note}')
    return '\n'.join(head) + '\n' + out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--deck', help='원본 .liggghts 덱')
    ap.add_argument('--ratios', default='10:0,7:3,5:5,3:7,0:10', help='P:S, 쉼표 구분')
    ap.add_argument('--am-mass', type=float, default=0.816, help='AM 질량분율 (기본 0.816)')
    ap.add_argument('--r-am-p', default='', help='AM_P 반지름을 덱 단위로 덮어쓴다 (예 4.5e-3)')
    ap.add_argument('--tag', default='', help='원본 태그 (기본 = 덱에서 자동 검출)')
    ap.add_argument('--tag-prefix', default='ps', help='새 태그 머리 (기본 ps)')
    ap.add_argument('--tag-suffix', default='', help='새 태그 꼬리 (옛 세대와 출력 충돌 방지)')
    ap.add_argument('--shared-seeds', action='store_true',
                    help='다섯 케이스가 같은 시드를 쓴다 (기본: 케이스마다 독립)')
    ap.add_argument('--note', default='', help='헤더에 한 줄 덧붙인다')
    ap.add_argument('--out', default='psweep', help='덱을 쓸 디렉터리')
    ap.add_argument('--mpi', type=int, default=10, help='실행 명령에 찍을 MPI 랭크 수')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)

    if a.selftest:
        return _selftest()
    if not a.deck:
        ap.error('--deck 이 필요합니다 (또는 --selftest)')

    text = open(a.deck).read()
    m = RE_MKDIR.search(text)
    tag = a.tag or (m.group(1) if m else '')
    if not tag:
        sys.exit('출력 태그를 찾지 못했습니다 (`shell mkdir post_<TAG>` 부재) → --tag 로 주세요')
    os.makedirs(a.out, exist_ok=True)
    print(f'원본 {a.deck}\n  태그 {tag}\n')

    cmds = []
    for i, tok in enumerate([t for t in a.ratios.split(',') if t.strip()]):
        p, s = parse_ratio(tok)
        seeds = seeds_for(0 if a.shared_seeds else i)
        tag_new = f'{a.tag_prefix}_{p}_{s}{a.tag_suffix}'
        path = os.path.join(a.out, f'in.{tag_new}.liggghts')
        deck = make_deck(text, tag, tag_new, p, s, seeds, a.r_am_p, a.am_mass, a.note)
        with open(path, 'w') as f:
            f.write(deck)
        head = [l for l in deck.split('\n') if '예상 입자수' in l]
        print(f'  {p:2d}:{s:<3d} → {path}')
        print(f'      {head[0].lstrip("# ") if head else ""}')
        cmds.append(f'mpirun --oversubscribe -np {a.mpi} liggghts -in {os.path.basename(path)} '
                    f'2>&1 | tee log_{tag_new}.out')

    print('\n실행 (덱이 있는 디렉터리에서 — post_/restart_ 를 거기에 만든다):')
    for c in cmds:
        print(f'  {c}')
    print('\n★ 케이스마다 시드가 다릅니다 — 조성이 바뀌면 삽입 스트림이 첫 입자부터 갈라져')
    print('  "같은 패킹" 이 존재하지 않기 때문입니다 (--shared-seeds 로 끌 수 있음).')
    return 0


def _selftest():
    ok, fail = 0, []

    def chk(name, cond):
        nonlocal ok
        if cond:
            ok += 1
        else:
            fail.append(name)

    # ── 시드: 큰 소수 · 전부 다름 · RNG 상한 아래 ──
    allseeds = [x for i in range(5) for x in seeds_for(i)]
    chk('시드 25개가 전부 소수', all(is_prime(x) for x in allseeds))
    chk('시드가 전부 다르다', len(set(allseeds)) == 25)
    chk('시드가 8자리 (원본 덱과 같은 대역)', all(1e7 <= x < 1e8 for x in allseeds))
    chk('★ RanPark 상한 9e8 아래', all(x < 900_000_000 for x in allseeds))
    chk('시드가 결정적 (재생성 멱등)', seeds_for(2) == seeds_for(2))
    chk('소수 판정기 자신', is_prime(15485863) and is_prime(49979687)
        and not is_prime(15485865) and not is_prime(1))

    # ── 조성 ──
    fr = compose(7, 3, 0.816)
    chk('7:3 이 원본 덱 값을 재현 (0.5712/0.2448/0.184)',
        abs(fr['AM_P'] - 0.5712) < 1e-12 and abs(fr['AM_S'] - 0.2448) < 1e-12
        and abs(fr['SE'] - 0.184) < 1e-12)
    chk('분율 합 = 1 (모든 비)', all(abs(sum(compose(p, s, 0.816).values()) - 1) < 1e-12
                                   for p, s in ((10, 0), (5, 5), (3, 7), (0, 10))))
    chk('10:0 은 AM_S 가 0', compose(10, 0, 0.816)['AM_S'] == 0.0)
    chk('표기가 원본 스타일 (0.184, 0.816)', fmt_frac(0.184) == '0.184'
        and fmt_frac(0.816) == '0.816' and fmt_frac(0.0) == '0')

    deck = (
        '# Real Condition 4: 후막전극 복합양극 (Bimodal)\n'
        '# P:S = 7:3 (AM_P r=6µm, AM_S r=2µm)\n'
        'variable r_AM_P  equal 6.0e-3            # AM_P r=6µm → Sim 6mm\n'
        'variable r_AM_S  equal 2.0e-3\n'
        'variable r_SE    equal 0.5e-3\n'
        'region reg_box block 0.0 0.05 0.0 0.05 -0.01 1.0 units box\n'
        'fix m1 all property/global youngsModulus peratomtype 1.4e8 1.4e8 0.135e7\n'
        'fix pts1 all particletemplate/sphere 15485863 atom_type 1 density constant 4800 '
        'radius constant ${r_AM_P}\n'
        'fix pts2 all particletemplate/sphere 15485867 atom_type 2 density constant 4800 '
        'radius constant ${r_AM_S}\n'
        'fix pts3 all particletemplate/sphere 32452843 atom_type 3 density constant 2000 '
        'radius constant ${r_SE}\n'
        '# 질량비: AM_P:0.5712, AM_S:0.2448, SE:0.184\n'
        'fix pdd_mix all particledistribution/discrete 49979687 3 pts1 0.5712 pts2 0.2448 '
        'pts3 0.184\n'
        '\n'                                                     # ← 회귀 재현용 빈 줄
        'region reg_mix block 0.0 0.05 0.0 0.05 0.005 0.30 units box\n'
        'fix ins_mix all insert/pack seed 80363 distributiontemplate pdd_mix &\n'
        '    volumefraction_region 0.321\n'
        'shell mkdir post_real_4\n'
        'restart 50000 restart_real_4/restart_settling_*.bin\n'
        'print "====== INSERTING (REAL_4: P:S=7:3) ====="\n')

    tpl, ent = read_deck(deck)
    chk('덱 실물 읽기: 템플릿 3 · atom_type 1/2/3',
        len(tpl) == 3 and sorted(v['atype'] for v in tpl.values()) == [1, 2, 3])
    chk('덱 실물 읽기: 밀도 4800/4800/2000',
        sorted(v['dens'] for v in tpl.values()) == [2000.0, 4800.0, 4800.0])
    chk('삽입 구역 고체부피 (2.367e-4 m³)',
        abs(region_solid_volume(deck) - 2.3668e-4) / 2.3668e-4 < 1e-3)

    # ★ 질량분율 규약 — 4/21 실측(AM_P 175 · SE 158,730)을 되짚는다
    cnt = predict_counts(deck, tpl, ent, {'r_AM_P': 6.0e-3, 'r_AM_S': 2.0e-3, 'r_SE': 0.5e-3})
    chk('★ 질량분율 예측이 4/21 실측과 맞는다 (7:3 AM_P 예측 119 vs 실측 126)',
        abs(cnt['pts1'] - 119) <= 3)
    #   10:0 은 AM 질량이 전부 AM_P 로 — 4/21 실측 175
    chk('★ 10:0 예측 170 vs 4/21 실측 175',
        abs(predict_counts(deck, tpl, [('pts1', 0.816), ('pts3', 0.184)],
                           {'r_AM_P': 6.0e-3, 'r_SE': 0.5e-3})['pts1'] - 170) <= 3)
    chk('★ SE 개수 예측이 실측 158,730 의 1 % 안', abs(cnt['pts3'] - 158730) / 158730 < 0.01)
    chk('★ 개수분율로 읽었다면 나올 값(SE ≈ AM_P 의 0.23배)이 **아니다**',
        cnt['pts3'] > 100 * cnt['pts1'])

    d73 = make_deck(deck, 'real_4', 'ps_7_3', 7, 3, seeds_for(1))
    chk('같은 비면 질량분율 문자열이 원본 그대로',
        'pts1 0.5712 pts2 0.2448 pts3 0.184' in d73)
    #  ★ 회귀: 분포 정규식의 `\s*$` 가 **뒤의 빈 줄을 삼켜** 의도 밖 diff 를 냈었다.
    #    의도한 변경만 diff 에 남아야 검산이 되므로 줄 수가 보존돼야 한다.
    chk('★ 본문 줄 수 보존 (생성기가 빈 줄을 삼키지 않는다)',
        len(d73.split('\n')) - 9 == len(deck.split('\n')))
    chk('★ 분포 줄 뒤의 빈 줄이 살아 있다',
        re.search(r'particledistribution/discrete[^\n]*\n\n', d73) is not None)
    chk('시드가 전부 갈렸다 (원본 시드가 하나도 안 남는다)',
        not any(str(x) in d73 for x in (15485863, 15485867, 32452843, 49979687, 80363)))
    chk('갈린 시드가 소수', all(is_prime(x) for x in seeds_for(1)))
    chk('출력 태그가 전부 갈림 (post_/restart_/print 대문자까지)',
        'post_ps_7_3' in d73 and 'restart_ps_7_3/' in d73 and 'PS_7_3' in d73
        and 'real_4' not in d73 and 'REAL_4' not in d73)
    chk('원본 덱은 그대로 (in-place 아님)', 'post_real_4' in deck and '15485863' in deck)
    chk('★ E_SE 는 불변 (0.135e7 = 1.35 GPa, 표의 2.4e7 아님)',
        'peratomtype 1.4e8 1.4e8 0.135e7' in d73 and '2.4e7' not in d73)
    chk('★ volumefraction · RVE · dt 류 불변', 'volumefraction_region 0.321' in d73)

    d55 = make_deck(deck, 'real_4', 'ps_5_5', 5, 5, seeds_for(2))
    chk('5:5 질량분율 (0.408/0.408/0.184)',
        'pts1 0.408 pts2 0.408 pts3 0.184' in d55)
    chk('주석의 P:S 표기도 갱신 (덱 머리가 거짓말하지 않게)', '# P:S = 5:5 ' in d55)
    chk('print 문의 조성 표기도 갱신', 'P:S=5:5' in d55)
    chk('질량비 주석도 갱신', '# 질량비: AM_P:0.408, AM_S:0.408, SE:0.184' in d55)

    d100 = make_deck(deck, 'real_4', 'ps_10_0', 10, 0, seeds_for(0))
    chk('★ 10:0 은 분포에서 AM_S 를 뺀다 (0 분율 금지)',
        'particledistribution/discrete' in d100 and ' 2 pts1 0.816 pts3 0.184' in d100)
    chk('10:0 은 pts2 정의가 남되 미사용이라고 밝힌다',
        'fix pts2 all particletemplate/sphere' in d100 and '질량분율 0 — 분포에서 제외' in d100)
    chk('10:0 은 Monomodal AM_P 로 라벨', '(Monomodal AM_P)' in d100)
    d010 = make_deck(deck, 'real_4', 'ps_0_10', 0, 10, seeds_for(4))
    chk('★ 0:10 은 AM_P 를 뺀다', ' 2 pts2 0.816 pts3 0.184' in d010)
    chk('0:10 은 Monomodal AM_S 로 라벨', '(Monomodal AM_S)' in d010)

    # ★ 반지름 덮어쓰기 — 값과 **주석**이 같이 움직여야 한다
    dr = make_deck(deck, 'real_4', 'ps_7_3_r45', 7, 3, seeds_for(1), r_am_p='4.5e-3')
    chk('AM_P 반지름이 덱 변수에서 바뀐다',
        'variable r_AM_P  equal 4.5e-3' in dr and '6.0e-3' not in dr)
    chk('★ 반지름 주석의 µm 표기도 같이 (r=6µm → r=4.5µm)',
        'AM_P r=4.5µm' in dr and 'r=6µm' not in dr)
    chk('AM_S/SE 반지름은 불변',
        'variable r_AM_S  equal 2.0e-3' in dr and 'variable r_SE    equal 0.5e-3' in dr)
    chk('★ 헤더가 예상 입자수를 밝힌다 (런 뒤 대조용)', '예상 입자수' in dr)
    chk('★ 헤더가 불변항을 명시 (E_SE · dt · press_speed)',
        'E_SE' in dr and 'press_speed' in dr)
    chk('헤더는 전부 주석 — LIGGGHTS 파싱 무해',
        all(l.startswith('#') for l in dr.split('\n')[:9]))
    #   r=4.5 로 AM_P 가 (6/4.5)³ = 2.37배 많아져야 한다
    t2, e2 = read_deck(dr)
    c6 = predict_counts(deck, tpl, ent, {'r_AM_P': 6.0e-3, 'r_AM_S': 2.0e-3, 'r_SE': 0.5e-3})
    c45 = predict_counts(dr, t2, e2, {'r_AM_P': 4.5e-3, 'r_AM_S': 2.0e-3, 'r_SE': 0.5e-3})
    chk('★ 반지름 6→4.5 이면 AM_P 개수가 (6/4.5)³ = 2.37배',
        abs(c45['pts1'] / c6['pts1'] - (6.0 / 4.5) ** 3) < 0.03)
    chk('AM_S·SE 개수는 불변', c45['pts2'] == c6['pts2'] and c45['pts3'] == c6['pts3'])

    # ── 가드가 실제로 죽는가 ──
    for bad, why in ((deck.replace('atom_type 3', 'atom_type 4'), 'atom_type 구성 오류'),
                     (deck.replace('discrete 49979687 3', 'discrete 49979687 2'),
                      '분포 개수 ≠ 항목 수')):
        try:
            make_deck(bad, 'real_4', 'x', 7, 3, seeds_for(0))
            fail.append(f'가드 미작동: {why}')
        except SystemExit:
            ok += 1
    #   ⚠ am_mass=1.4 는 **분율 합이 여전히 1** 이라 합 검사로는 못 잡힌다 (selftest 가
    #     실제로 그 구멍을 잡았다) → 범위 가드가 따로 있어야 한다
    chk('합 검사만으로는 am_mass=1.4 를 못 잡는다 (범위 가드가 필요한 이유)',
        abs(sum({'AM_P': 1.4 * .7, 'AM_S': 1.4 * .3, 'SE': 1 - 1.4}.values()) - 1.0) < 1e-12)
    for bad_m in (1.4, 0.0, 1.0, -0.1):
        try:
            compose(7, 3, bad_m)
            fail.append(f'가드 미작동: am_mass={bad_m}')
        except SystemExit:
            ok += 1

    print(f'make_ps_sweep_decks SELFTEST {ok} PASS',
          'ALL GREEN' if not fail else f'FAIL {fail}')
    return 0 if not fail else 1


if __name__ == '__main__':
    raise SystemExit(main())
