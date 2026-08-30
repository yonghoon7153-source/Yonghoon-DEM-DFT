#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LHS 확장 64런의 **성공 게이트** — 상태를 세지, 총수를 세지 않는다 (R15 §6).

    sacct -X -u $USER -S <제출일> -n -P -o JobName,State,ExitCode > /tmp/sacct.psv
    python3 scripts/lhs_ext_submit_gate.py \\
        --manifest /tmp/lhsx_decks/deck_manifest.json --sacct /tmp/sacct.psv
    python3 scripts/lhs_ext_submit_gate.py --selftest

⚠⚠ **왜 이 파일이 있나** — 종결문(2026-08-30 초판)이 성공 조건을
`RUNNING + COMPLETED + CANCELLED = 64` 라고 적었다.  그것은 성공 게이트가 **아니다**:
  · `CANCELLED` 를 성공처럼 세고,
  · `FAILED` · `TIMEOUT` · `OUT_OF_MEMORY` · `NODE_FAIL` · `PREEMPTED` 를 **놓친다**.
합이 맞는다는 것은 잡이 사라지지 않았다는 뜻일 뿐, 끝났다는 뜻이 아니다.
08-18 에 25건이 죽었을 때도 `afterany` chain 은 **합을 맞춰 가며** 지나갔다.

⇒ 성공은 **하나뿐**이다: 등록된 64 ID 가 **전부 `COMPLETED`** 이고, 각 ID 의 기대
  산출물이 존재하며 매니페스트 해시와 일치할 것.  그 밖의 모든 상태는 **HOLD** 다.
  ★ 부분 성공은 없다 — LHS 는 점이 고르게 깔린 것이 전제라, 한쪽만 살아남으면
    커버리지가 **계통적으로** 편향된다 (무작위 결손과 다르다).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

#: 성공으로 세는 유일한 상태.  나머지는 전부 미완이다.
OK_STATE = 'COMPLETED'
#: 명시적으로 **실패**로 분류하는 상태 (있으면 그 ID 를 다시 돌려야 한다).
FAIL_STATES = ('FAILED', 'TIMEOUT', 'OUT_OF_MEMORY', 'NODE_FAIL', 'PREEMPTED',
               'BOOT_FAIL', 'DEADLINE', 'REVOKED', 'CANCELLED')
#: 아직 진행 중.
BUSY_STATES = ('RUNNING', 'PENDING', 'REQUEUED', 'RESIZING', 'SUSPENDED')


def parse_sacct(text: str) -> dict:
    """`sacct -n -P -o JobName,State[,ExitCode]` → {job_name: state}.

    ⚠ `-X` 로 **잡 단계(step)를 빼야** 한다 — 안 그러면 `batch`·`extern` 단계가 같은
      이름으로 섞여 상태가 둘이 된다.  여기서는 이름이 중복되면 **가장 나쁜 상태**를
      남긴다 (낙관적으로 고르면 게이트가 무의미해진다).
    """
    rank = {s: 0 for s in BUSY_STATES}
    rank.update({s: 1 for s in FAIL_STATES})
    rank[OK_STATE] = 2                       # 낮을수록 나쁘다 → min 을 남긴다
    out = {}
    for ln in text.splitlines():
        ln = ln.strip()
        if not ln:
            continue
        parts = ln.split('|')
        if len(parts) < 2:
            continue
        name, state = parts[0].strip(), parts[1].strip().split()[0]
        state = state.rstrip('+')            # `CANCELLED+` → `CANCELLED`
        prev = out.get(name)
        if prev is None or rank.get(state, 0) < rank.get(prev, 0):
            out[name] = state
    return out


def check(manifest: dict, states: dict, outroot: str | None = None,
          expect_outputs: tuple[str, ...] = ()) -> tuple[list[str], dict]:
    """→ (막는 사유 목록, 요약).  사유가 비어야 GO 다."""
    ids = list(manifest.get('ids') or [])
    blocks, summary = [], {}
    if not ids:
        return ['매니페스트에 ID 가 없다'], summary

    seen = {i: states.get(i) for i in ids}
    by_state = {}
    for i, st in seen.items():
        by_state.setdefault(st or '(기록없음)', []).append(i)
    summary['n_ids'] = len(ids)
    summary['by_state'] = {k: len(v) for k, v in sorted(by_state.items())}
    summary['extra_jobs'] = sorted(set(states) - set(ids))

    done = [i for i, st in seen.items() if st == OK_STATE]
    summary['n_completed'] = len(done)
    if len(done) != len(ids):
        for st, lst in sorted(by_state.items()):
            if st != OK_STATE:
                blocks.append(f'{st}: {len(lst)}건 — 예: {", ".join(sorted(lst)[:3])}')
    #  ★ 등록 밖 잡이 섞이면 어느 세대를 보고 있는지 알 수 없다
    if summary['extra_jobs']:
        blocks.append(f'매니페스트에 없는 잡 {len(summary["extra_jobs"])}건 — '
                      f'예: {", ".join(summary["extra_jobs"][:3])}')

    #  ── 입력 해시가 그대로인가 (돌린 것이 봉인한 것과 같은가) ──────────────
    if outroot:
        drift = []
        for d in manifest.get('decks') or []:
            fp = os.path.join(outroot, d['file'])
            if not os.path.exists(fp):
                drift.append(f'{d["id"]}: 덱 파일 없음')
                continue
            h = hashlib.sha256(open(fp, 'rb').read()).hexdigest()
            if h != d['sha256']:
                drift.append(f'{d["id"]}: 덱 해시 불일치')
            rp = d.get('runner') and os.path.join(outroot, d['runner'])
            if rp and os.path.exists(rp):
                rh = hashlib.sha256(open(rp, 'rb').read()).hexdigest()
                if rh != d.get('runner_sha256'):
                    drift.append(f'{d["id"]}: 러너 해시 불일치')
            elif rp:
                drift.append(f'{d["id"]}: 러너 파일 없음')
        if drift:
            blocks.append(f'봉인 입력이 바뀌었다 ({len(drift)}건): ' + '; '.join(drift[:3]))
        summary['input_drift'] = len(drift)

        #  기대 산출물 (호출자가 지정)
        if expect_outputs:
            miss = []
            for i in ids:
                for pat in expect_outputs:
                    fp = os.path.join(outroot, i, pat.format(id=i))
                    if not os.path.exists(fp):
                        miss.append(f'{i}/{pat.format(id=i)}')
            if miss:
                blocks.append(f'기대 산출물 없음 ({len(miss)}건): ' + '; '.join(miss[:3]))
            summary['missing_outputs'] = len(miss)
    return blocks, summary


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--manifest', help='materializer 가 낸 deck_manifest.json')
    ap.add_argument('--sacct', help='`sacct -X -n -P -o JobName,State` 출력 파일')
    ap.add_argument('--outroot', help='덱 디렉터리 (해시·산출물 확인)')
    ap.add_argument('--expect-output', action='append', default=[],
                    help='ID 별 기대 산출물 경로 패턴 (`{id}` 치환).  여러 번 줄 수 있다')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    if not (a.manifest and a.sacct):
        ap.error('--manifest 와 --sacct 가 필요하다')

    man = json.load(open(a.manifest, encoding='utf-8'))
    states = parse_sacct(open(a.sacct, encoding='utf-8').read())
    blocks, summ = check(man, states, a.outroot, tuple(a.expect_output))

    print(f'등록 ID {summ.get("n_ids")}개 · COMPLETED {summ.get("n_completed")}개')
    for st, n in (summ.get('by_state') or {}).items():
        print(f'  {st:<16} {n}')
    if blocks:
        print('\n⛔ HOLD — 제출 결과를 성공으로 볼 수 없다:')
        for b in blocks:
            print('  ·', b)
        print('\n⚠ 부분 성공은 없다 — LHS 는 점이 고르게 깔린 것이 전제라, 계통적으로 '
              '빠진 점은 무작위 결손과 다르다.')
        return 1
    print('\n✓ GO — 64/64 COMPLETED · 봉인 입력 불변 · 기대 산출물 존재')
    return 0


def _selftest():
    ok, fail = 0, []

    def chk(name, cond, extra=''):
        nonlocal ok
        if cond:
            ok += 1
        else:
            fail.append(f'{name} {extra}')

    man = dict(ids=[f'lhsx_{i:03d}' for i in range(1, 5)], decks=[])

    def sacct(pairs):
        return '\n'.join(f'{n}|{s}|0:0' for n, s in pairs)

    all_done = [(i, 'COMPLETED') for i in man['ids']]
    b, s = check(man, parse_sacct(sacct(all_done)))
    chk('① 전부 COMPLETED 면 GO', b == [], str(b))
    chk('① 요약이 4/4', s['n_completed'] == 4)

    #  ★★ 종결문이 틀렸던 자리 — CANCELLED 를 성공으로 세면 안 된다
    mixed = [(man['ids'][0], 'CANCELLED')] + [(i, 'COMPLETED') for i in man['ids'][1:]]
    b, _ = check(man, parse_sacct(sacct(mixed)))
    chk('★② CANCELLED 가 있으면 HOLD', b != [] and any('CANCELLED' in x for x in b))
    for st in ('FAILED', 'TIMEOUT', 'OUT_OF_MEMORY', 'NODE_FAIL', 'PREEMPTED'):
        m = [(man['ids'][0], st)] + [(i, 'COMPLETED') for i in man['ids'][1:]]
        b, _ = check(man, parse_sacct(sacct(m)))
        chk(f'★② {st} 가 있으면 HOLD', b != [] and any(st in x for x in b))
    b, _ = check(man, parse_sacct(sacct(
        [(man['ids'][0], 'RUNNING')] + [(i, 'COMPLETED') for i in man['ids'][1:]])))
    chk('② RUNNING 이면 아직 HOLD', b != [])

    #  ★ 합만 맞는 경우 — 옛 규칙이면 통과했을 자리
    tot = [(man['ids'][0], 'CANCELLED'), (man['ids'][1], 'RUNNING'),
           (man['ids'][2], 'COMPLETED'), (man['ids'][3], 'COMPLETED')]
    b, s2 = check(man, parse_sacct(sacct(tot)))
    chk('★★② RUNNING+COMPLETED+CANCELLED = 4 여도 HOLD (옛 규칙 반례)',
        b != [] and s2['n_completed'] == 2)

    #  ③ 기록이 아예 없는 ID
    b, _ = check(man, parse_sacct(sacct(all_done[:3])))
    chk('★③ sacct 에 없는 ID 는 HOLD', b != [] and any('기록없음' in x for x in b))
    #  ④ 등록 밖 잡
    b, _ = check(man, parse_sacct(sacct(all_done + [('lhsx_099', 'COMPLETED')])))
    chk('★④ 매니페스트에 없는 잡이 섞이면 HOLD', b != [] and any('없는 잡' in x for x in b))
    #  ⑤ 중복 이름은 **나쁜 쪽**을 남긴다 (step 이 섞였을 때 낙관하지 않는다)
    dup = parse_sacct(sacct([('lhsx_001', 'COMPLETED'), ('lhsx_001', 'FAILED')]))
    chk('★⑤ 같은 이름이 두 상태면 나쁜 쪽을 남긴다', dup['lhsx_001'] == 'FAILED', str(dup))
    chk('⑤ `CANCELLED+` 를 CANCELLED 로 읽는다',
        parse_sacct('lhsx_001|CANCELLED by 9248|0:0')['lhsx_001'] == 'CANCELLED')

    #  ⑥ 봉인 입력이 바뀌면 HOLD
    import tempfile
    d = tempfile.mkdtemp(prefix='gate_')
    os.makedirs(os.path.join(d, 'lhsx_001'), exist_ok=True)
    fp = os.path.join(d, 'lhsx_001', 'input_lhsx_001.liggghts')
    open(fp, 'w').write('x\n')
    good = hashlib.sha256(b'x\n').hexdigest()
    m2 = dict(ids=['lhsx_001'],
              decks=[dict(id='lhsx_001', file='lhsx_001/input_lhsx_001.liggghts',
                          sha256=good)])
    b, _ = check(m2, parse_sacct(sacct([('lhsx_001', 'COMPLETED')])), outroot=d)
    chk('⑥ 해시가 같으면 통과', b == [], str(b))
    open(fp, 'w').write('tampered\n')
    b, _ = check(m2, parse_sacct(sacct([('lhsx_001', 'COMPLETED')])), outroot=d)
    chk('★⑥ 덱이 바뀌었으면 HOLD (돌린 것이 봉인한 것이 아니다)',
        b != [] and any('해시' in x for x in b))

    print(f'lhs_ext_submit_gate selftest: {ok}/{ok + len(fail)} PASS')
    for f in fail:
        print('  ✗', f)
    return 1 if fail else 0


if __name__ == '__main__':
    raise SystemExit(main())
