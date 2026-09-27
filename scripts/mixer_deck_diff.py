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
import make_mixer_deck as _gen                                # noqa: E402  기대 시드 서명의 출처 = 생성기 자신 (HBR3-07)

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


def expected_deck(arm, seed, n_total=GEN_ARGS['n_total'], cgf=GEN_ARGS['cgf'], revolutions=GEN_ARGS['revolutions']):
    """생성기 CLI `make_mixer_deck.py --n-total … --cgf … --arm <arm> --seed <seed> --revolutions …` 가 쓰는 in.mixer 와
    **같은 텍스트**를 메모리에서 만든다.  호출은 그 CLI 의 main 그대로다: --fr 기본 FR_ANCHOR · --rpm 없음 ·
    --allow-off-band 없음 · --settle-s 없음 · --baffles 0 · --baffle-h 0.10 (셀프테스트 ㉒ = CLI 출력과 바이트 동일)."""
    p = _gen.plan(n_total, cgf=cgf)
    rpm = _gen.resolve_rpm(p['R'], _gen.FR_ANCHOR, None, False)
    return _gen.deck(p, rpm, revolutions, arm=arm, settle_s=None, seed=seed, n_baffles=0, baffle_h=0.10)


def _read(path):
    try:
        return open(path, encoding='utf-8').read()
    except OSError:
        return None


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
                    exp_cache[(a_, s)] = (seed_signature(expected_deck(a_, s)), None)
                except (Exception, SystemExit) as e:          # 합성수 시드면 생성기가 SystemExit — 기대가 없으면 FAIL
                    exp_cache[(a_, s)] = (None, f'{type(e).__name__}: {e}')
            exp, err = exp_cache[(a_, s)]
            pr = []
            if sig is None:
                pr.append(f'{name}: in.mixer 없음')
            elif err is not None:
                pr.append(f'{name}: 기대 서명을 생성기로 만들 수 없다 ({err})')
            elif sig != exp:
                pr.append(f'{name}: 기대 서명과 다르다 — ' + '; '.join(_sig_delta(sig, exp)))
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
        mark = '≠' if abs(row['ratio'] - 1.0) > REL_TOL else ' '
        print(f'   {mark} {row["pair"]:12s} {row["ref"]:14.6g} → {row["new"]:14.6g}   ×{row["ratio"]:.4g}')
    for k, msg in (('non_ced_diffs', 'CED 밖 차이'), ('outside', '허용목록 밖 CED 변화'), ('missing', '개입 누락 (허용 쌍인데 안 바뀜)'),
                   ('wrong_direction', '개입 방향 반대 (증가여야 한다)'), ('target_mismatch', '목표 행렬과 불일치')):
        if r[k]:
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
    print(f'\nmixer_deck_diff selftest: {ok}/{ok + len(fail)} PASS' + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


def main():
    ap = argparse.ArgumentParser(description='믹서 실행 덱 두 벌의 CED 차이 = 허용목록인가 (Codex HB-03)')
    ap.add_argument('decks', nargs='*', help='<기준 덱> <새 덱>')
    ap.add_argument('--allow', choices=sorted(ALLOW), default='B')
    ap.add_argument('--runs', help='runs 디렉터리 — <ref-arm>_s<시드>/in.mixer 와 <arm>_s<시드>/in.mixer 를 같은 시드끼리 '
                                   '+ 디렉터리마다 실제 시드 서명 = 생성기 기대 서명 · 시드 간 고유 (HBR3-07)')
    ap.add_argument('--ref-arm', default='LC')
    ap.add_argument('--arm', default='LH')
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
    expect = parse_deck(open(a.expect_deck, encoding='utf-8').read())['ced'] if a.expect_deck else None
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
            r = diff_decks(t_ref, t_new, a.allow, expect=expect)
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
