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
  ⚠ 이 도구는 덱만 본다 — 실행 바이너리 · 재개 이력 · 판독 규약은 사전등록의 발사 기록이 맡는다.

usage
  python3 scripts/mixer_deck_diff.py <기준 덱 (LC)> <새 덱 (LH)> --allow B [--json out.json]
  python3 scripts/mixer_deck_diff.py --runs <runs 디렉터리> --ref-arm LC --arm LH --allow B    # 같은 시드끼리 전부
  python3 scripts/mixer_deck_diff.py --selftest
"""
import argparse
import glob
import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
from make_mixer_resume import logical_commands, _tokens      # noqa: E402  덱 논리 명령 파서 — 한 벌만 둔다
from make_mixer_deck import TPL_SEED                          # noqa: E402  템플릿 시드 → 상 이름 (정본)

ALLOW = {
    'B': {('AM_P', 'AM_P'), ('AM_P', 'AM_S'), ('AM_S', 'AM_S'), ('AM_P', 'WALL'), ('AM_S', 'WALL')},
    'A': {('AM_P', 'AM_P'), ('AM_P', 'AM_S'), ('AM_S', 'AM_S')},
}
REL_TOL = 1e-6          # 덱은 CED 를 유효숫자 몇 자리로 찍는다 — 같은 값의 재생성 잡음보다 크고 개입보다 훨씬 작게


def parse_deck(text):
    """덱 텍스트 → dict(cmds=[비-CED 토큰 목록…], ced=(n, 값 목록), names={타입: 상 이름})."""
    cmds, ced, names, ntypes = [], None, {}, None
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
    return dict(cmds=cmds, ced=ced, names=names)


def diff_decks(text_ref, text_new, allow='B'):
    """두 덱 → 판정 dict(verdict, non_ced_diffs, changed, outside, missing, table)."""
    a, b = parse_deck(text_ref), parse_deck(text_new)
    out = dict(allow=allow, non_ced_diffs=[], changed=[], outside=[], missing=[], table=[])
    if len(a['cmds']) != len(b['cmds']):
        out['non_ced_diffs'].append(f'명령 수 {len(a["cmds"])} ≠ {len(b["cmds"])}')
    for i, (x, y) in enumerate(zip(a['cmds'], b['cmds'])):
        if x != y:
            out['non_ced_diffs'].append(f'#{i}: {" ".join(x)[:120]}  ⇄  {" ".join(y)[:120]}')
    if a['names'] != b['names']:
        out['non_ced_diffs'].append(f'타입 이름 {a["names"]} ≠ {b["names"]}')
    (na, va), (nb, vb) = a['ced'], b['ced']
    if na != nb:
        out['non_ced_diffs'].append(f'CED 행렬 크기 {na} ≠ {nb}')
        out['verdict'] = 'FAIL'
        return out
    nm = [a['names'].get(k + 1, f't{k + 1}') for k in range(na)]
    changed = set()
    for i in range(na):
        for j in range(na):
            x, y = va[i * na + j], vb[i * na + j]
            if abs(y - x) > REL_TOL * max(abs(x), abs(y), 1e-30):
                changed.add(tuple(sorted((nm[i], nm[j]))))
            if j >= i:
                out['table'].append(dict(pair=f'{nm[i]}–{nm[j]}', ref=x, new=y,
                                         ratio=(y / x) if x else (float('inf') if y else 1.0)))
            if abs(va[i * na + j] - va[j * na + i]) > REL_TOL * max(abs(va[i * na + j]), 1e-30):
                out['non_ced_diffs'].append(f'기준 덱 CED 비대칭 ({nm[i]},{nm[j]})')
    allowed = ALLOW[allow]
    out['changed'] = sorted(changed)
    out['outside'] = sorted(changed - allowed)
    out['missing'] = sorted(allowed - changed)
    out['verdict'] = 'PASS' if not (out['non_ced_diffs'] or out['outside'] or out['missing']) else 'FAIL'
    return out


def report(label, r):
    print(f'── {label}  (허용목록 {r["allow"]}) → {r["verdict"]}')
    for row in r['table']:
        mark = '≠' if abs(row['ratio'] - 1.0) > REL_TOL else ' '
        print(f'   {mark} {row["pair"]:12s} {row["ref"]:14.6g} → {row["new"]:14.6g}   ×{row["ratio"]:.4g}')
    for k, msg in (('non_ced_diffs', 'CED 밖 차이'), ('outside', '허용목록 밖 CED 변화'), ('missing', '개입 누락 (허용 쌍인데 안 바뀜)')):
        if r[k]:
            print(f'   ⛔ {msg}: {r[k][:8]}')


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
    print(f'\nmixer_deck_diff selftest: {ok}/{ok + len(fail)} PASS' + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


def main():
    ap = argparse.ArgumentParser(description='믹서 실행 덱 두 벌의 CED 차이 = 허용목록인가 (Codex HB-03)')
    ap.add_argument('decks', nargs='*', help='<기준 덱> <새 덱>')
    ap.add_argument('--allow', choices=sorted(ALLOW), default='B')
    ap.add_argument('--runs', help='runs 디렉터리 — <ref-arm>_s<시드>/in.mixer 와 <arm>_s<시드>/in.mixer 를 같은 시드끼리')
    ap.add_argument('--ref-arm', default='LC')
    ap.add_argument('--arm', default='LH')
    ap.add_argument('--json')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    pairs = []
    if a.runs:
        for d in sorted(glob.glob(os.path.join(a.runs, f'{a.arm}_s*'))):
            sd = os.path.basename(d).split('_s', 1)[1]
            if not (os.path.isdir(d) and sd.isdigit()):          # gen_all 이 옆에 남기는 <런>.gen.log 등은 건너뛴다
                continue
            pairs.append((os.path.join(a.runs, f'{a.ref_arm}_s{sd}', 'in.mixer'), os.path.join(d, 'in.mixer')))
        if not pairs:
            ap.error(f'{a.runs} 에 {a.arm}_s* 가 없다')
    elif len(a.decks) == 2:
        pairs = [tuple(a.decks)]
    else:
        ap.error('덱 두 개 또는 --runs 를 주세요')
    out = []
    for ref, new in pairs:
        r = diff_decks(open(ref, encoding='utf-8').read(), open(new, encoding='utf-8').read(), a.allow)
        r.update(ref=ref, new=new)
        report(f'{ref}  →  {new}', r)
        out.append(r)
    if a.json:
        json.dump(out, open(a.json, 'w'), ensure_ascii=False, indent=1)
        print(f'→ {a.json}')
    bad = sum(r['verdict'] != 'PASS' for r in out)
    print(f'\n{len(out) - bad}/{len(out)} PASS' + ('' if not bad else '  ⛔ 짝짓기 근거 없음 — 발사 금지'))
    raise SystemExit(1 if bad else 0)


if __name__ == '__main__':
    main()
