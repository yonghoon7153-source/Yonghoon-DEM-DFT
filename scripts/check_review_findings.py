#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""리뷰 finding 원장 검사 — "응답 문서는 있었는데 다음 작업 목록에서 사라짐" 을 막는다.

★ 왜 필요한가 (실제로 일어난 일): Codex 5회차 리뷰(2026-08-07)가 **4일간 처리되지
  않았다**.  응답 문서도 쓰고 회귀도 붙였는데, 다음 세션에서 그 문서가 큐에 없었다.
  사용자가 "이것도 반영이 된 건가?" 라고 묻기 전까지 아무도 몰랐다.  산문으로 상태를
  적으면 다시 새어나간다 — **기계가 읽는 단일 원장**이 필요하다 (Codex Q8).

원장: `docs/reviews/findings.json`
  {"findings": [ {id, severity, status, owner, opened_in, claimed_fixed_sha,
                  verified_sha, evidence_tests, supersedes, decision_note}, … ]}

이 검사가 강제하는 것:
  ① ID 중복 없음 · 형식(RC6-01 류) 준수
  ② `claimed_fixed` 는 fix SHA **와** 회귀 근거(evidence_tests)를 **둘 다** 가진다
  ③ `verified` 는 **구현자와 다른** 검증자(verified_by)가 있어야 한다
     — 자기가 고치고 자기가 검증했다고 닫는 것을 막는다 (이번 라운드의 교훈:
       "구현자의 회귀 PASS 와 결함 종료는 같은 뜻이 아니다")
  ④ 열린 항목(open/claimed_fixed)을 **항상 화면에 뽑는다** — 다음 리뷰 요청 문서가
     그 목록을 그대로 실을 수 있게

⚠ 이 검사는 원장의 **자기일관성**만 본다.  "정말 고쳐졌는가" 는 회귀와 독립 검증자의
  몫이다 — 원장이 그것을 대신한다고 착각하면 안 된다.

  python3 scripts/check_review_findings.py            # 검사 + 열린 항목 출력
  python3 scripts/check_review_findings.py --open     # 열린 항목만 (리뷰 요청서용)
  python3 scripts/check_review_findings.py --selftest
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

LEDGER_DEFAULT = os.path.join('docs', 'reviews', 'findings.json')

#: 실제로 쓰는 ID 형태를 전부 받는다 — RC6-01 · RR3-04 · F-18 · RC6-04b · RC6-Q7 · PD-02.
#: (첫 정의가 너무 좁아 우리 자신의 ID 를 거부했다 — 원장이 규약을 따라야지 반대가 아니다.)
ID_RE = re.compile(r'^[A-Z][A-Z0-9]{0,4}-[A-Za-z0-9]{1,4}$')
STATUSES = ('open', 'claimed_fixed', 'verified', 'wontfix')
SEVERITIES = ('P1', 'P2', 'P3')

#: 상태별로 **반드시** 있어야 하는 필드.  없으면 그 상태를 주장할 수 없다.
REQUIRED_BY_STATUS = {
    'claimed_fixed': ('claimed_fixed_sha', 'evidence_tests'),
    'verified': ('claimed_fixed_sha', 'evidence_tests', 'verified_sha', 'verified_by'),
    'wontfix': ('decision_note',),
}


def load(path):
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    return data.get('findings', []) if isinstance(data, dict) else list(data)


def check(findings, repo_root=None):
    """→ 문제 목록 (빈 리스트면 원장이 자기일관적).

    `repo_root` 를 주면 `opened_in` 이 **실재하는 파일**인지도 본다 — 원장이 유령
    문서를 가리키면 추적이 거기서 끊긴다 (실제로 RC6 원문이 붙여넣기라 리포에
    없었다 → 원문을 보존해 해소).
    """
    problems, seen = [], {}
    for i, f in enumerate(findings):
        where = f.get('id') or f'#{i}'
        fid = f.get('id')
        if not fid:
            problems.append(f'{where}: id 없음')
            continue
        if not ID_RE.match(fid):
            problems.append(f'{fid}: id 형식 (예: RC6-01)')
        if fid in seen:
            problems.append(f'{fid}: id 중복 (앞선 항목 #{seen[fid]})')
        seen[fid] = i

        st = f.get('status')
        if st not in STATUSES:
            problems.append(f'{fid}: status={st!r} (허용: {"/".join(STATUSES)})')
            continue
        if f.get('severity') not in SEVERITIES:
            problems.append(f'{fid}: severity={f.get("severity")!r}')
        if not f.get('opened_in'):
            problems.append(f'{fid}: opened_in 없음 (어느 리뷰에서 나왔는지)')
        elif repo_root and not os.path.exists(os.path.join(repo_root, f['opened_in'])):
            problems.append(f'{fid}: opened_in 이 실재하지 않는다 ({f["opened_in"]}) — '
                            '리뷰 원문을 리포에 보존할 것')

        for key in REQUIRED_BY_STATUS.get(st, ()):
            v = f.get(key)
            if not v:
                problems.append(f'{fid}: status={st} 인데 {key} 없음')
        # ★ 자기검증 금지 — 구현자와 검증자가 같으면 verified 로 닫을 수 없다.
        if st == 'verified' and f.get('verified_by') and f.get('owner') \
                and f['verified_by'] == f['owner']:
            problems.append(f'{fid}: verified_by == owner ({f["owner"]}) — '
                            '구현자 자신은 검증자가 될 수 없다')
        # supersedes 가 가리키는 id 는 실재해야 한다
        for sup in (f.get('supersedes') or []):
            if sup not in {x.get('id') for x in findings}:
                problems.append(f'{fid}: supersedes 대상 {sup} 이 원장에 없다')
    return problems


def open_items(findings):
    """아직 닫히지 않은 것 (open · claimed_fixed).  다음 리뷰 요청서에 그대로 싣는다."""
    return [f for f in findings if f.get('status') in ('open', 'claimed_fixed')]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument('--ledger', default=os.path.join(here, LEDGER_DEFAULT))
    ap.add_argument('--open', action='store_true', help='열린 항목만 출력')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    if not os.path.exists(a.ledger):
        sys.exit(f'원장 없음: {a.ledger}')
    findings = load(a.ledger)
    probs = check(findings, repo_root=here)

    if not a.open:
        by = {}
        for f in findings:
            by.setdefault(f.get('status', '?'), []).append(f)
        print(f'══ finding 원장 — {len(findings)} 건 ══')
        for st in STATUSES:
            if by.get(st):
                print(f'   {st:<14} {len(by[st])}')
        print()

    ops = open_items(findings)
    print(f'── 열린 항목 {len(ops)} 건 (open · claimed_fixed) ──')
    for f in ops:
        ev = ', '.join(f.get('evidence_tests') or []) or '—'
        print(f"  [{f.get('severity')}] {f['id']:<8} {f.get('status'):<13} "
              f"{(f.get('title') or '')[:52]}")
        print(f"        회귀: {ev}   opened_in: {f.get('opened_in')}")

    if probs:
        print(f'\n★★ 원장 불일치 {len(probs)} 건 ★★')
        for p in probs:
            print('   ' + p)
        return 1
    print('\n원장 자기일관 ✓  (⚠ "정말 고쳐졌는가" 는 회귀와 독립 검증자의 몫이다)')
    return 0


def _selftest():
    n = [0, 0]

    def ok(name, cond):
        n[1] += 1
        n[0] += bool(cond)
        print(f'  {"PASS" if cond else "FAIL"}  {name}')

    base = {'id': 'RC6-01', 'severity': 'P1', 'status': 'open',
            'owner': 'claude', 'opened_in': 'docs/reviews/x.md'}
    ok('1) 최소 항목은 통과', check([base]) == [])
    ok('2) id 중복을 잡는다', any('중복' in p for p in check([base, dict(base)])))
    ok('3) id 형식을 잡는다', any('형식' in p for p in check([dict(base, id='bad')])))
    ok('3b) ★ 우리가 실제로 쓰는 ID 형태를 전부 받는다',
       all(ID_RE.match(x) for x in ('RC6-01', 'RR3-04', 'F-18', 'RC6-04b', 'RC6-Q7', 'PD-02')))
    ok('4) 모르는 status 를 잡는다', any('status=' in p for p in check([dict(base, status='done')])))
    ok('5) ★ claimed_fixed 는 SHA + 회귀를 둘 다 요구한다',
       len([p for p in check([dict(base, status='claimed_fixed')])]) == 2)
    ok('6) 둘 다 있으면 통과',
       check([dict(base, status='claimed_fixed', claimed_fixed_sha='abc',
                   evidence_tests=['t1'])]) == [])
    ok('7) ★ verified 는 검증자까지 요구한다',
       any('verified_by' in p for p in check([dict(base, status='verified',
                                                   claimed_fixed_sha='a',
                                                   evidence_tests=['t'],
                                                   verified_sha='b')])))
    ok('8) ★ 자기검증(verified_by == owner)을 거부한다',
       any('검증자가 될 수 없다' in p for p in check([
           dict(base, status='verified', claimed_fixed_sha='a', evidence_tests=['t'],
                verified_sha='b', verified_by='claude')])))
    ok('9) 다른 검증자면 통과',
       check([dict(base, status='verified', claimed_fixed_sha='a', evidence_tests=['t'],
                   verified_sha='b', verified_by='codex')]) == [])
    ok('10) wontfix 는 사유를 요구한다',
       any('decision_note' in p for p in check([dict(base, status='wontfix')])))
    ok('11) opened_in 이 없으면 잡는다',
       any('opened_in' in p for p in check([{k: v for k, v in base.items()
                                             if k != 'opened_in'}])))
    ok('12) supersedes 대상이 없으면 잡는다',
       any('supersedes' in p for p in check([dict(base, supersedes=['RC5-99'])])))
    ok('13) 열린 항목만 골라낸다',
       [f['id'] for f in open_items([
           base, dict(base, id='RC6-02', status='verified'),
           dict(base, id='RC6-03', status='claimed_fixed')])] == ['RC6-01', 'RC6-03'])

    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    led = os.path.join(here, LEDGER_DEFAULT)
    if os.path.exists(led):
        ok('14) ★ 실제 원장이 자기일관적이다', check(load(led), repo_root=here) == [])
        ok('15) ★ opened_in 이 유령 문서면 잡는다 (추적이 거기서 끊긴다)',
           any('실재하지' in p for p in check(
               [dict(base, opened_in='docs/reviews/nope.md')], repo_root=here)))
    else:
        print('  SKIP 14) 원장 파일 없음')
    print(f'\ncheck_review_findings selftest: {n[0]}/{n[1]} PASS')
    return 0 if n[0] == n[1] else 1


if __name__ == '__main__':
    raise SystemExit(main())
