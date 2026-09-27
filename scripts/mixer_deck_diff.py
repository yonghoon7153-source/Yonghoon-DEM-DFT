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
import math
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


def diff_decks(text_ref, text_new, allow='B', expect=None):
    """두 덱 → 판정 dict(verdict, non_ced_diffs, changed, outside, missing, wrong_direction, target_mismatch, table).

    2026-09-27 저녁 (Codex HBR2-05) 넓힌 것: CED 명령 머리 (fix id · group · style · n) 동일 · **양쪽** 행렬 유한 · 비음수 ·
    대칭 · 허용 쌍은 **증가** 방향 (고-Bo 확장) · `expect` = (n, 값) 을 주면 새 행렬이 그 목표와 1e-5 안에서 같아야 한다.
    ⚠ PASS 는 **덱 텍스트의 계약**이다 — 실제 STL 내용 · 바이너리 · 실행 환경은 발사 기록 (§2-5) 이 따로 묶는다.
    """
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


def collect_pairs(runs, arm, ref_arm, expect_seeds=None):
    """runs 디렉터리 → ([(기준 덱, 새 덱)…], 찾은 시드 집합, 빠진 시드 집합).  <arm>_s<시드>/in.mixer 만 (gen.log 등은 건너뛴다)."""
    pairs, found = [], set()
    for d in sorted(glob.glob(os.path.join(runs, f'{arm}_s*'))):
        sd = os.path.basename(d).split('_s', 1)[1]
        if not (os.path.isdir(d) and sd.isdigit()):
            continue
        pairs.append((os.path.join(runs, f'{ref_arm}_s{sd}', 'in.mixer'), os.path.join(d, 'in.mixer')))
        found.add(int(sd))
    missing = set(int(s) for s in (expect_seeds or ())) - found
    return pairs, found, missing


def report(label, r):
    print(f'── {label}  (허용목록 {r["allow"]}) → {r["verdict"]}')
    for row in r['table']:
        mark = '≠' if abs(row['ratio'] - 1.0) > REL_TOL else ' '
        print(f'   {mark} {row["pair"]:12s} {row["ref"]:14.6g} → {row["new"]:14.6g}   ×{row["ratio"]:.4g}')
    for k, msg in (('non_ced_diffs', 'CED 밖 차이'), ('outside', '허용목록 밖 CED 변화'), ('missing', '개입 누락 (허용 쌍인데 안 바뀜)'),
                   ('wrong_direction', '개입 방향 반대 (증가여야 한다)'), ('target_mismatch', '목표 행렬과 불일치')):
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
    print(f'\nmixer_deck_diff selftest: {ok}/{ok + len(fail)} PASS' + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


def main():
    ap = argparse.ArgumentParser(description='믹서 실행 덱 두 벌의 CED 차이 = 허용목록인가 (Codex HB-03)')
    ap.add_argument('decks', nargs='*', help='<기준 덱> <새 덱>')
    ap.add_argument('--allow', choices=sorted(ALLOW), default='B')
    ap.add_argument('--runs', help='runs 디렉터리 — <ref-arm>_s<시드>/in.mixer 와 <arm>_s<시드>/in.mixer 를 같은 시드끼리')
    ap.add_argument('--ref-arm', default='LC')
    ap.add_argument('--arm', default='LH')
    ap.add_argument('--expect-seeds', default=None,
                    help='(--runs) 있어야 할 시드 목록 "a,b,c" — 기본 = 생성기 CAMPAIGN_SEEDS.  하나라도 빠지면 FAIL (n/N 을 기계가 센다)')
    ap.add_argument('--expect-deck', default=None,
                    help='지금 생성기로 새로 만든 같은 팔 덱 — 그 CED 행렬을 목표값으로 대조 (발사 덱이 손대지지 않았나)')
    ap.add_argument('--json')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    expect = parse_deck(open(a.expect_deck, encoding='utf-8').read())['ced'] if a.expect_deck else None
    pairs, missing_seeds = [], set()
    if a.runs:
        from make_mixer_deck import CAMPAIGN_SEEDS
        want = [int(x) for x in a.expect_seeds.split(',')] if a.expect_seeds else list(CAMPAIGN_SEEDS)
        pairs, found, missing_seeds = collect_pairs(a.runs, a.arm, a.ref_arm, want)
        print(f'── {a.runs}: {a.arm}_s* {len(pairs)}/{len(want)} 짝 (찾음 {sorted(found)} · 빠짐 {sorted(missing_seeds)})')
        if not pairs:
            ap.error(f'{a.runs} 에 {a.arm}_s* 가 없다')
    elif len(a.decks) == 2:
        pairs = [tuple(a.decks)]
    else:
        ap.error('덱 두 개 또는 --runs 를 주세요')
    out = []
    for ref, new in pairs:
        r = diff_decks(open(ref, encoding='utf-8').read(), open(new, encoding='utf-8').read(), a.allow, expect=expect)
        r.update(ref=ref, new=new)
        report(f'{ref}  →  {new}', r)
        out.append(r)
    if a.json:
        json.dump(out, open(a.json, 'w'), ensure_ascii=False, indent=1)
        print(f'→ {a.json}')
    bad = sum(r['verdict'] != 'PASS' for r in out)
    print(f'\n{len(out) - bad}/{len(out)} PASS' + ('' if not bad else '  ⛔ 짝짓기 근거 없음 — 발사 금지')
          + (f'  ⛔ 예정 시드 {sorted(missing_seeds)} 가 없다 — {len(out)} 짝으로는 3/3 이 아니다' if missing_seeds else ''))
    raise SystemExit(1 if (bad or missing_seeds) else 0)


if __name__ == '__main__':
    main()
