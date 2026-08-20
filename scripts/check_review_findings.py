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

⚠ **아직 못 하는 것** (RC7-04 잔여, Codex 지적):
  · evidence 는 **파일 실재**만 본다 — `file.py::RC6-02` 의 **selector 가 실제로 선택
    가능한지**는 검사하지 않는다.  우리 테스트가 pytest 가 아니라 자체 `main()` 형식이라
    그 문자열은 실행 대상이 아니다.  최종형은 evidence 를 자유문자열이 아니라
    `{command, target_sha, expected_exit, selector}` 로 두고 **CI 가 실제 실행**하는 것.
  · identity 를 코드로 좁혔을 뿐, 구현자가 `verified_by: codex` 라고 **쓰는 것 자체**는
    막지 못한다.  그것은 branch protection / CODEOWNERS 의 몫이다.

  python3 scripts/check_review_findings.py            # 검사 + 열린 항목 출력
  python3 scripts/check_review_findings.py --open     # 열린 항목만 (리뷰 요청서용)
  python3 scripts/check_review_findings.py --selftest
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

# ★ RC7-04 (Codex): `--open` 이 Windows 기본 CP949 에서 세 번째 항목을 찍다 죽었다
#   (UnicodeEncodeError, exit 1).  "열린 항목을 **항상** 화면에 뽑는다" 가 이 도구의
#   존재 이유인데 기본 Windows 실행에서 그 계약이 성립하지 않았다.
#   → stdout/stderr 를 UTF-8 로 재구성하고, 그것이 불가능한 환경에서는 대체문자로 떨어뜨린다
#     (죽는 것보다 읽히는 것이 낫다).
for _stream in ('stdout', 'stderr'):
    _s = getattr(sys, _stream, None)
    if _s is not None and hasattr(_s, 'reconfigure'):
        try:
            _s.reconfigure(encoding='utf-8', errors='replace')
        except Exception:                                   # noqa: BLE001
            pass

LEDGER_DEFAULT = os.path.join('docs', 'reviews', 'findings.json')

#: 실제로 쓰는 ID 형태를 전부 받는다 — RC6-01 · RR3-04 · F-18 · RC6-04b · RC6-Q7 · PD-02.
#: (첫 정의가 너무 좁아 우리 자신의 ID 를 거부했다 — 원장이 규약을 따라야지 반대가 아니다.)
ID_RE = re.compile(r'^[A-Z][A-Z0-9]{0,4}-[A-Za-z0-9]{1,4}$')
STATUSES = ('open', 'claimed_fixed', 'verified', 'wontfix')
SEVERITIES = ('P1', 'P2', 'P3')

#: ★ RC7-04: identity 를 자유문자열로 두면 **case 변형으로 자기검증 금지를 우회**한다
#:   (Codex 실측: owner='claude' · verified_by='Claude' 가 통과했다).  정본 목록으로 좁힌다.
ACTORS = ('claude', 'codex', 'user')

#: git SHA 형식 (짧은 것도 허용하되 hex 여야 한다).
SHA_RE = re.compile(r'^[0-9a-f]{7,40}$')

#: 상태별로 **반드시** 있어야 하는 필드.  없으면 그 상태를 주장할 수 없다.
REQUIRED_BY_STATUS = {
    'claimed_fixed': ('claimed_fixed_sha', 'evidence_tests'),
    'verified': ('claimed_fixed_sha', 'evidence_tests', 'verified_sha', 'verified_by'),
    'wontfix': ('decision_note',),
}


#: ── 철회-문자열 스윕 (2026-08-20) ────────────────────────────────────────────────
#:   왜: 원장은 SR-01 축에서 실질 정본으로 작동하는데 **정본성이 바깥으로 강제되지 않는다**.
#:   실증 — 2026-08-12 에 반증된 `~9.4 %` 가 **08-19 신규 문서에서 재주장**됐고, 독립 리뷰가
#:   그것을 (역시 낡은) 정본에 대조해 "일치"로 **통과**시켰다.  ⇒ 대조 검증조차 정본 신선도에
#:   종속된다.  발견: `docs/reviews/fable_audit_docs_20260820.md` (a)-1.
#:   등록부는 `docs/reviews/claims.json` 의 `quotation_ban` (CLAUDE.md ★★ 인용 금지 목록의
#:   기계 판).  ⚠ 이 파일 목록이 비면 규칙이 조용히 사라지므로 selftest 가 비었는지도 본다.
CLAIMS_DEFAULT = os.path.join('docs', 'reviews', 'claims.json')

#: ⚠⚠ 2026-08-20 (Codex CDX-IJ-04) — 초판 범위는 **md/html/js 뿐**이라 두 곳이 새고 있었다:
#:   · `docs/seminar/seminar_deck.json` — 웹앱 `/api/seminar/slides`(`webapp/app.py`)가 **직접
#:     서빙**하는 활성 산출물인데 `+52%`·`+5.6%` 를 현행 결론으로 말한다.
#:   · `scripts/sr01_gate5_2x2.sh` — 철회된 `f_artifact` 를 여전히 출력한다.
#:   그런데 스윕은 "누수 0" 을 냈다 = false-green.  ⇒ **사용자에게 노출되는 산출물**을 전부 넣는다
#:   (JSON 덱·러너 셸·덱 생성기).  scripts/*.py 는 넣지 않는다 — 그쪽 등장은 대부분 철회를
#:   설명하는 주석이고, 필요하면 줄-근처 표지 규칙으로 개별 통과한다.
BAN_SCAN_GLOBS = ('CLAUDE.md', 'docs/**/*.md', 'wiki/**/*.md',
                  'webapp/templates/*.html', 'webapp/static/js/*.js',
                  'scripts/seminar_deck/*.js',
                  'docs/**/*.json', 'webapp/**/*.json', 'scripts/*.sh')

#: 이 경로들은 **박제된 원문**이라 철회값이 들어 있는 것이 정상이다 (원장 자신 · 감사 원문 ·
#: 사전등록 계약 · 외부 리뷰 요청서 = 리뷰 시점의 상태를 보존해야 하는 문서).
BAN_ALLOW_ALWAYS = ('docs/reviews/claims.json',
                    # finding 원장도 "무엇을 철회했나" 를 적는 등록부다 (claims.json 과 같은 층).
                    'docs/reviews/findings.json',
                    'docs/reviews/fable_audit_docs_20260820.md',
                    'docs/reviews/fable_audit_code_20260820.md',
                    # ⚠ 외부 리뷰 **원문 박제** — 리뷰어가 인용한 철회값이 그대로 있어야 한다
                    #   (고치면 그 리뷰가 무엇을 보고 판정했는지 알 수 없게 된다).
                    'docs/reviews/codex_crosscheck_IJ_20260820.md')

#: 파일 머리 이 줄 수 안에 배너가 있으면 그 파일 전체를 이력 문서로 본다.
BAN_BANNER_HEAD_LINES = 12
#: 배너·근처 표지로 인정하는 표시.
BAN_BANNER_MARKS = ('HISTORICAL', '⛔', '인용 금지', '철회', '반증', 'retired', 'RETIRED',
                    '~~', '폐기', '무효')
#: 해당 줄 위아래 이 범위에 표지가 있으면 "철회를 밝히고 인용" 으로 본다.
BAN_NEAR_LINES = 2


def load_bans(claims_path):
    """→ (bans, why).  등록부가 없거나 비면 빈 리스트."""
    if not os.path.exists(claims_path):
        return [], f'등록부 없음: {claims_path}'
    with open(claims_path, encoding='utf-8') as f:
        d = json.load(f)
    return list(d.get('quotation_ban') or []), ''


def _ban_files(repo_root):
    import glob as _glob
    out = []
    for pat in BAN_SCAN_GLOBS:
        out += _glob.glob(os.path.join(repo_root, pat), recursive=True)
    return sorted(set(out))


def _has_banner(lines):
    head = '\n'.join(lines[:BAN_BANNER_HEAD_LINES])
    return any(m in head for m in BAN_BANNER_MARKS)


def ban_sweep(repo_root, claims_path=None, files=None):
    """→ (문제 목록, 검사한 파일 수, 등록부 크기).

    한 출현이 **허용**되려면 셋 중 하나: ⓐ 파일이 allowed_in / 상시허용 목록 ⓑ 파일 머리
    배너가 있음(이력 문서) ⓒ 그 줄 ±2 줄에 철회 표지가 있음(철회를 밝히고 인용).
    """
    import fnmatch as _fn
    claims_path = claims_path or os.path.join(repo_root, CLAIMS_DEFAULT)
    bans, err = load_bans(claims_path)
    probs = []
    if err:
        return [err], 0, 0
    files = files if files is not None else _ban_files(repo_root)
    for path in files:
        rel = os.path.relpath(path, repo_root).replace(os.sep, '/')
        if rel in BAN_ALLOW_ALWAYS:
            continue
        try:
            with open(path, encoding='utf-8', errors='replace') as f:
                lines = f.read().split('\n')
        except OSError:
            continue
        banner = _has_banner(lines)
        for b in bans:
            pat = b.get('pattern')
            if not pat:
                continue
            if any(_fn.fnmatch(rel, g) for g in (b.get('allowed_in') or [])):
                continue
            for i, ln in enumerate(lines):
                if pat not in ln:
                    continue
                if banner:
                    continue
                lo = max(0, i - BAN_NEAR_LINES)
                near = '\n'.join(lines[lo:i + BAN_NEAR_LINES + 1])
                if any(m in near for m in BAN_BANNER_MARKS):
                    continue
                probs.append(f'BAN| {rel}:{i + 1} — 철회값 "{pat}" 이 표지 없이 살아 있다 '
                             f'({b.get("claim", "?")}: {b.get("why", "")[:70]})')
    return probs, len(files), len(bans)


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
        # ★ identity 는 정본 목록으로만 (RC7-04: case 변형 우회 차단)
        for key in ('owner', 'verified_by'):
            v = f.get(key)
            if v is not None and v not in ACTORS:
                problems.append(f'{fid}: {key}={v!r} 는 정본 actor 가 아니다 '
                                f'(허용: {"/".join(ACTORS)}) — 대소문자 변형 우회 차단')
        # ★ 자기검증 금지 — 구현자와 검증자가 같으면 verified 로 닫을 수 없다.
        #   ⚠ 정규화해서 비교한다 (Codex 실측: 'claude' vs 'Claude' 가 통과했다).
        _own = (f.get('owner') or '').strip().casefold()
        _ver = (f.get('verified_by') or '').strip().casefold()
        if st == 'verified' and _ver and _own and _ver == _own:
            problems.append(f'{fid}: verified_by == owner ({f["owner"]}) — '
                            '구현자 자신은 검증자가 될 수 없다')
        # ★ SHA 는 형식 + (repo 가 있으면) **실재하는 커밋**이어야 한다 (RC7-04)
        for key in ('claimed_fixed_sha', 'verified_sha'):
            sha = f.get(key)
            if not sha:
                continue
            if not SHA_RE.match(str(sha)):
                problems.append(f'{fid}: {key}={sha!r} 가 SHA 형식이 아니다')
            elif repo_root and not _commit_exists(repo_root, sha):
                problems.append(f'{fid}: {key}={sha} 가 이 리포에 없는 커밋이다')
        # ★ evidence 가 가리키는 **파일이 실재**해야 한다 (RC7-04: 유령 evidence 통과)
        for ev in (f.get('evidence_tests') or []):
            path = str(ev).split('::', 1)[0].split()[0] if ev else ''
            if repo_root and path and not os.path.exists(os.path.join(repo_root, path)):
                problems.append(f'{fid}: evidence 가 실재하지 않는다 ({ev})')
        # supersedes 가 가리키는 id 는 실재해야 한다
        for sup in (f.get('supersedes') or []):
            if sup not in {x.get('id') for x in findings}:
                problems.append(f'{fid}: supersedes 대상 {sup} 이 원장에 없다')
    return problems


def _commit_exists(repo_root, sha):
    """그 SHA 가 이 리포의 **실재하는 커밋**인가 (RC7-04).  git 이 없으면 검사 생략."""
    try:
        r = subprocess.run(['git', '-C', repo_root, 'cat-file', '-e', f'{sha}^{{commit}}'],
                           capture_output=True, timeout=10)
        return r.returncode == 0
    except Exception:                                       # noqa: BLE001
        return True            # git 을 못 쓰는 환경에서 **거짓 실패**를 만들지 않는다


def open_items(findings):
    """아직 닫히지 않은 것 (open · claimed_fixed).  다음 리뷰 요청서에 그대로 싣는다."""
    return [f for f in findings if f.get('status') in ('open', 'claimed_fixed')]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument('--ledger', default=os.path.join(here, LEDGER_DEFAULT))
    ap.add_argument('--open', action='store_true', help='열린 항목만 출력')
    ap.add_argument('--claims', default=os.path.join(here, CLAIMS_DEFAULT))
    ap.add_argument('--ban-sweep', action='store_true',
                    help='철회-문자열 스윕만 실행 (claims.json quotation_ban 등록부)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    if a.ban_sweep:
        bprobs, nfile, nban = ban_sweep(here, a.claims)
        print(f'── 철회-문자열 스윕 — 등록 {nban} 개 × 파일 {nfile} 개 ──')
        for p in bprobs:
            print('   ' + p)
        if not nban:
            print('   ⚠ 등록부가 비었다 — 이 규칙은 지금 아무것도 강제하지 않는다')
            return 1
        print(('\n★★ 철회값 누수 %d 건 ★★' % len(bprobs)) if bprobs
              else '\n철회값 누수 없음 ✓')
        return 1 if bprobs else 0
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
    # ★ SHA 형식 검사가 생긴 뒤로는 fixture 도 진짜 형태여야 한다 (fixture-drift 교정).
    #   repo_root 를 안 주므로 **실재 검사는 생략**되고 형식만 본다.
    ok('6) 둘 다 있으면 통과',
       check([dict(base, status='claimed_fixed', claimed_fixed_sha='0123abc',
                   evidence_tests=['t1'])]) == [])
    ok('7) ★ verified 는 검증자까지 요구한다',
       any('verified_by' in p for p in check([dict(base, status='verified',
                                                   claimed_fixed_sha='0123abc',
                                                   evidence_tests=['t'],
                                                   verified_sha='abc0123')])))
    ok('8) ★ 자기검증(verified_by == owner)을 거부한다',
       any('검증자가 될 수 없다' in p for p in check([
           dict(base, status='verified', claimed_fixed_sha='0123abc', evidence_tests=['t'],
                verified_sha='abc0123', verified_by='claude')])))
    ok('9) 다른 검증자면 통과',
       check([dict(base, status='verified', claimed_fixed_sha='0123abc',
                   evidence_tests=['t'], verified_sha='abc0123', verified_by='codex')]) == [])
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

    # ══ RC7-04 (Codex 6→7회차): 검사기 자신이 통과시키던 손상 원장 ══
    _corrupt = {'id': 'RC6-01', 'severity': 'P1', 'status': 'verified', 'owner': 'claude',
                'opened_in': 'docs/reviews/x.md', 'verified_by': 'Claude',
                'claimed_fixed_sha': 'not-a-sha', 'verified_sha': 'also-not-a-sha',
                'evidence_tests': ['missing.py::ghost']}
    _probs = check([_corrupt])
    ok('16) ★ case 변형 자기검증 우회를 잡는다 (claude vs Claude)',
       any('정본 actor' in p for p in _probs) and any('검증자가 될 수 없다' in p for p in _probs))
    ok('17) ★ SHA 형식 위반을 잡는다 (not-a-sha)',
       len([p for p in _probs if 'SHA 형식' in p]) == 2)
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ok('18) ★ 유령 evidence 를 잡는다',
       any('evidence 가 실재하지' in p for p in check([_corrupt], repo_root=here)))
    ok('19) ★ 형식은 맞지만 리포에 없는 커밋을 잡는다',
       any('없는 커밋' in p for p in check(
           [dict(_corrupt, verified_by='codex', claimed_fixed_sha='deadbeef',
                 verified_sha='cafebabe',
                 evidence_tests=['webapp/test_pipeline_provenance.py'])], repo_root=here)))
    ok('20) 정본 actor 세 개는 통과', set(ACTORS) == {'claude', 'codex', 'user'})

    led = os.path.join(here, LEDGER_DEFAULT)
    if os.path.exists(led):
        ok('14) ★ 실제 원장이 자기일관적이다', check(load(led), repo_root=here) == [])
        ok('15) ★ opened_in 이 유령 문서면 잡는다 (추적이 거기서 끊긴다)',
           any('실재하지' in p for p in check(
               [dict(base, opened_in='docs/reviews/nope.md')], repo_root=here)))
    else:
        print('  SKIP 14) 원장 파일 없음')

    # ── 철회-문자열 스윕 (2026-08-20) ────────────────────────────────────────────
    #   ★ 음성 대조가 핵심이다 — 규칙 D 의 교훈("한 번도 발동한 적이 없는 검사")대로,
    #     "지금 리포가 깨끗하다" 만으로는 검사기가 **정말 잡는지** 증명되지 않는다.
    import tempfile as _tf
    _claims = os.path.join(here, CLAIMS_DEFAULT)
    _bans, _err = load_bans(_claims)
    ok('16) 등록부가 비어 있지 않다 (비면 이 규칙이 조용히 사라진다)',
       not _err and len(_bans) >= 5)
    if _bans:
        _pat = _bans[0]['pattern']
        with _tf.TemporaryDirectory() as _d:
            _bad = os.path.join(_d, 'bad.md')
            with open(_bad, 'w', encoding='utf-8') as _f:
                _f.write(f'# 제목\n\n본문에서 {_pat} 를 현행 사실로 쓴다\n')
            _p1, _, _ = ban_sweep(_d, _claims, files=[_bad])
            ok('17) ★ 음성 대조 — 표지 없는 철회값을 **정말** 잡는다', len(_p1) == 1)

            _good = os.path.join(_d, 'good.md')
            with open(_good, 'w', encoding='utf-8') as _f:
                _f.write(f'# 제목\n\n> ⛔ HISTORICAL — 아래는 이력이다\n\n{_pat} 는 옛 값\n')
            _p2, _, _ = ban_sweep(_d, _claims, files=[_good])
            ok('18) 파일 머리 배너가 있으면 통과 (이력 문서를 죽이지 않는다)', _p2 == [])

            _near = os.path.join(_d, 'near.md')
            with open(_near, 'w', encoding='utf-8') as _f:
                _f.write(f'# 제목\n\n옛 헤드라인 {_pat} 는 **철회**됐다 (CL-24)\n')
            _p3, _, _ = ban_sweep(_d, _claims, files=[_near])
            ok('19) 같은 줄에 철회 표지가 있으면 통과 (철회를 밝히고 인용)', _p3 == [])
    ok('21) ★ 리포 전체가 지금 깨끗하다 (누수 0)',
       ban_sweep(here, _claims)[0] == [])

    print(f'\ncheck_review_findings selftest: {n[0]}/{n[1]} PASS')
    return 0 if n[0] == n[1] else 1


if __name__ == '__main__':
    raise SystemExit(main())
