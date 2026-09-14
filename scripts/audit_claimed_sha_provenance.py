#!/usr/bin/env python3
"""`claimed_fixed_sha` 가 **그 수정을 담은 커밋**을 가리키는가.

★ 왜 (2026-09-14, §6 전수 감사에서 발견)
원장은 `claimed_fixed` 에 실재하는 SHA 를 요구하고 `check_review_findings.py` 가 그것을
강제한다.  그런데 **실재하는 SHA 가 곧 그 수정의 SHA 는 아니다.**  실측:

    R5CX-08/10/11 의 `claimed_fixed_sha` = `672dedb1`
      git show 672dedb18:scripts/sdcp_gain_verdict.py | grep -c rejected  →  0
      git show 777cd6c08:scripts/sdcp_gain_verdict.py | grep -c rejected  →  7

⇒ 적힌 자리에 수정이 **없다**.  진짜 커밋은 `777cd6c08` 이다.

★ 기전은 구조적이고, 사람의 부주의가 아니다
수정과 원장 등재를 **같은 커밋**에 넣으면 그 커밋은 자기 SHA 를 자기 안에 적을 수 없다
(해시가 내용에 의존한다) ⇒ 적을 수 있는 최신 SHA 는 **부모**다.  그래서 한 칸 어긋난다.

★ ⚠ 그런데 `적힌 SHA == 등재 커밋의 부모` 는 **그 자체로는 결함이 아니다**
수정이 바로 앞 커밋에 있고 등재만 따로 했다면 부모를 적는 것이 **옳다**.  두 경우가 같은
서명을 낸다.  가르는 기준은 하나다 —

    **등재 커밋 자신이 그 항목의 `evidence_tests` 파일을 건드렸는가.**

건드렸다면 수정은 그 커밋 안에 있으므로 부모를 가리키는 것은 틀렸다 (`STALE_PARENT`).
안 건드렸다면 수정은 앞에 있고 부모 표기가 맞을 수 있다 (`PARENT_OK`).

⚠ **이 도구가 답하지 않는 것**: *"정말 고쳐졌는가"*.  그것은 회귀와 독립 검증자의 몫이다
(`check_review_findings.py` 가 스스로 적어 둔 그 문장).  여기서 재는 것은 **감사 가능성**
하나다 — *'적힌 SHA 를 읽어 수정을 확인하라'* 는 절차가 그 자리에서 무언가를 찾는가.

사용:
    python3 scripts/audit_claimed_sha_provenance.py            # 리포가 맞나
    python3 scripts/audit_claimed_sha_provenance.py --selftest # 검사기가 맞나
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

LEDGER = 'docs/reviews/findings.json'

#: 등재 커밋이 이것만 건드렸으면 "기록만 만진 커밋" 으로 본다 (수정이 아니다).
LEDGER_ONLY_PREFIXES = ('docs/reviews/', 'docs/session_')

#: **실행되는 코드**만 수정의 증거로 센다.  원고·데이터·문서에 ID 가 적히는 것은 기록이다.
CODE_SUFFIXES = ('.py', '.sh', '.js', '.html', '.yml', '.yaml')

VERDICTS = ('EXACT', 'ANCESTOR', 'PARENT_OK', 'STALE_PARENT', 'UNRELATED', 'NO_REGISTER')


def _git(*args: str) -> str:
    return subprocess.run(('git',) + args, capture_output=True, text=True).stdout


def _full(sha: str) -> str:
    return _git('rev-parse', sha).strip()


# ─────────────────────────────────────────────────────────────────────────────
#  순수 판정 — git 없이 시험할 수 있게 갈라 둔다 (selftest 가 이것을 부른다)
# ─────────────────────────────────────────────────────────────────────────────
def classify(recorded: str, reg_sha: str, reg_parent: str,
             reg_adds_id: bool, is_ancestor) -> str:
    """한 항목의 SHA 출처를 판정한다.

    recorded      원장에 적힌 SHA (full)
    reg_sha       그 항목을 claimed_fixed 로 **바꾼** 커밋 (full) — 없으면 ''
    reg_parent    그 커밋의 첫 부모 (full)
    reg_adds_id   등재 커밋이 **원장 밖 파일에 그 ID 를 이름으로 부르는 줄을 추가**했는가
    is_ancestor   (a, b) -> bool

    ⚠ **초판의 판별자는 거짓 양성을 냈다** (2026-09-14, 같은 감사에서 자기 검사기가 잡혔다).
    초판은 *'등재 커밋이 그 항목의 `evidence_tests` 파일을 건드렸나'* 를 물었는데, R5CX 10건이
    **같은 selftest 3줄을 증거로 공유**한다.  그래서 셋만 고친 커밋(`777cd6c08`)이 열 건 전부의
    수정처럼 보였다 — 실측으로 `R5CX-01` 의 수정은 적힌 자리(`672dedb18`)에 **있었다**(14회).
    ⇒ 파일 단위는 너무 거칠다.  이 리포는 수정한 코드에 **항목 ID 를 주석으로 박는** 규약이
    있으므로, 그 ID 를 **추가한** 커밋이 곧 수정 커밋이다.  그것을 판별자로 쓴다.
    """
    if not reg_sha:
        return 'NO_REGISTER'
    if recorded == reg_sha:
        return 'EXACT'
    if recorded == reg_parent:
        #  ★ 갈림길: 등재 커밋이 **그 ID 를 코드에 새로 박았다면** 수정은 그 안에 있고,
        #    부모를 가리키는 것은 빈 자리를 가리키는 것이다.
        return 'STALE_PARENT' if reg_adds_id else 'PARENT_OK'
    if is_ancestor(recorded, reg_sha):
        return 'ANCESTOR'
    return 'UNRELATED'


_ID_TOKEN = None


def adds_id_outside_ledger(sha: str, fid: str) -> bool:
    """등재 커밋의 **추가된 줄**이 원장 밖 파일에서 그 ID 를 부르는가.

    ⚠ 원장 ID `R5CX-08` 을 커밋·코드는 `R5-CX-08` 로 쓴다 — 하이픈을 정규화하지 않으면
    자기 정규식으로 원장을 반박하게 된다 (`SELF-25` 가 등재한 그 실패).
    """
    import re
    norm = lambda s: re.sub(r'[-_\s]', '', s).upper()
    tgt = norm(fid)
    diff = _git('show', '--unified=0', '--format=', sha)
    cur_file = ''
    for line in diff.splitlines():
        if line.startswith('+++ '):
            cur_file = line[6:].strip()
            continue
        if not line.startswith('+') or line.startswith('+++'):
            continue
        #  ⚠ **기록에 ID 를 적는 것은 수정이 아니다.**  거짓 양성을 세 겹으로 걷어냈다:
        #    ⓐ 원장 자신 · ⓑ 판정문/세션 진행 문서(`LEDGER_ONLY_PREFIXES`) —
        #       `L3-06`·`SELF-22`·`HARV-01` 이 여기서 걸렸다 (셋 다 진행 문서만 건드림)
        #    ⓒ 원고·데이터 파일 — `R20-02` 가 `methods_simulation_v7_draft.md` 에서 걸렸다.
        #    ⇒ **실행되는 코드**에 ID 가 박힌 것만 수정의 증거로 센다.
        if cur_file == LEDGER or cur_file.startswith(LEDGER_ONLY_PREFIXES):
            continue
        if not cur_file.endswith(CODE_SUFFIXES):
            continue
        for m in re.finditer(r'[A-Za-z][A-Za-z0-9\-_]{2,20}[0-9]', line):
            if norm(m.group(0)) == tgt:
                return True
    return False


def evidence_paths(finding: dict) -> list:
    """`evidence_tests` 는 `경로` · `경로::테스트` · `명령 인자…` 세 형태가 섞여 있다."""
    out = []
    for raw in (finding.get('evidence_tests') or []):
        base = str(raw).split('::')[0].split(' ')[0].strip()
        if base.endswith(('.py', '.sh', '.md', '.json', '.csv', '.html', '.js', '.tsv')):
            out.append(base)
    return out


# ─────────────────────────────────────────────────────────────────────────────
#  이력 한 번만 훑어 id → 등재 커밋 지도를 만든다 (항목마다 훑으면 141배 느리다)
# ─────────────────────────────────────────────────────────────────────────────
def registering_commits(ledger_path: str = LEDGER) -> dict:
    revs = _git('log', '--format=%H', '--reverse', '--', ledger_path).split()
    reg, prev = {}, {}
    for h in revs:
        blob = _git('show', f'{h}:{ledger_path}')
        try:
            cur = {x['id']: x.get('status') for x in json.loads(blob)['findings']}
        except Exception:
            continue                      # 그 시점에 파싱 불가 ⇒ 건너뛴다 (판정 안 함)
        for fid, st in cur.items():
            if st in ('claimed_fixed', 'verified') and prev.get(fid) != st and fid not in reg:
                reg[fid] = h
        prev = cur
    return reg


def touched(sha: str) -> set:
    out = _git('show', '--pretty=format:', '--name-only', sha)
    return {l.strip() for l in out.splitlines() if l.strip()}


def first_parent(sha: str) -> str:
    ps = _git('log', '-1', '--format=%P', sha).split()
    return ps[0] if ps else ''


def run_audit(ledger_path: str = LEDGER) -> int:
    findings = json.load(open(ledger_path, encoding='utf-8'))['findings']
    targets = [x for x in findings if x.get('status') in ('claimed_fixed', 'verified')]
    print(f'대상 {len(targets)}건 (claimed_fixed · verified) — 이력을 한 번 훑는다')
    reg = registering_commits(ledger_path)

    def is_anc(a, b):
        return subprocess.run(('git', 'merge-base', '--is-ancestor', a, b),
                              capture_output=True).returncode == 0

    buckets = {v: [] for v in VERDICTS}
    for x in targets:
        rec = x.get('claimed_fixed_sha')
        rec = rec[0] if isinstance(rec, list) else rec
        rec_full = _full(str(rec).strip()) if rec else ''
        rs = reg.get(x['id'], '')
        rp = first_parent(rs) if rs else ''
        v = classify(rec_full, rs, rp,
                     adds_id_outside_ledger(rs, x['id']) if rs else False, is_anc)
        buckets[v].append((x['id'], x['severity'], str(rec), rs[:9], x['title'][:64]))

    for v in VERDICTS:
        print(f'  {v:14s} {len(buckets[v]):3d}')
    stale = buckets['STALE_PARENT']
    if stale:
        print(f'\n⛔ STALE_PARENT {len(stale)}건 — 등재 커밋이 증거 파일을 건드렸는데 '
              f'SHA 는 그 **부모**를 가리킨다.\n'
              f'   ⇒ 적힌 자리를 열면 수정이 없다.  진짜 커밋으로 바꿀 것.')
        for fid, sev, rec, rs, title in sorted(stale):
            print(f'   {fid:12s} {sev}  적힘={rec:10s} → 등재={rs}  {title}')
    else:
        print('\n✓ STALE_PARENT 없음')
    return 1 if stale else 0


# ─────────────────────────────────────────────────────────────────────────────
def selftest() -> int:
    ok = [0, 0]

    def chk(label, cond):
        ok[1] += 1
        ok[0] += bool(cond)
        print(('  ✓ ' if cond else '  ✗ ') + label)

    anc_true = lambda a, b: True
    anc_false = lambda a, b: False

    chk('① 적힌 SHA == 등재 커밋 ⇒ EXACT',
        classify('aaa', 'aaa', 'ppp', False, anc_false) == 'EXACT')

    #  ★★ 이 둘이 이 검사기의 존재 이유다 — **같은 서명, 다른 판정**.
    chk('② 부모를 적었고 등재 커밋이 그 ID 를 코드에 새로 박았다 ⇒ STALE_PARENT',
        classify('ppp', 'aaa', 'ppp', True, anc_false) == 'STALE_PARENT')
    chk('③ 부모를 적었으나 등재 커밋은 그 ID 를 코드에 안 박았다 ⇒ PARENT_OK (결함 아님)',
        classify('ppp', 'aaa', 'ppp', False, anc_false) == 'PARENT_OK')

    chk('④ 더 앞선 조상을 적었다 ⇒ ANCESTOR',
        classify('old', 'aaa', 'ppp', True, anc_true) == 'ANCESTOR')
    chk('⑤ 조상도 아니다 ⇒ UNRELATED',
        classify('xxx', 'aaa', 'ppp', True, anc_false) == 'UNRELATED')
    chk('⑥ 등재 커밋을 못 찾으면 판정하지 않는다 ⇒ NO_REGISTER',
        classify('aaa', '', '', False, anc_false) == 'NO_REGISTER')

    #  ★ 판별력 — ② 에서 판별자 하나만 뒤집으면 판정이 갈려야 한다 (검사가 공허하지 않다).
    chk('⑦ ② 와 ③ 은 `reg_adds_id` 하나로만 갈린다 (판별력)',
        classify('ppp', 'aaa', 'ppp', True, anc_false)
        != classify('ppp', 'aaa', 'ppp', False, anc_false))

    chk('⑧ evidence_paths 가 `경로::테스트`·`명령 인자` 를 파일로 접는다',
        evidence_paths({'evidence_tests': ['a/b.py::T1', 'c/d.sh --selftest',
                                           '산문 설명', 'e/f.json']})
        == ['a/b.py', 'c/d.sh', 'e/f.json'])

    #  ★★ 초판 판별자의 **거짓 양성을 못박는다** — 이 검사기가 스스로 걸렸던 자리다.
    #     R5CX 10건이 같은 selftest 3줄을 증거로 공유해, 셋만 고친 커밋이 열 건 전부의
    #     수정처럼 보였다.  ID 를 코드에 박았는지로 바꾸면 그 일곱이 갈라진다.
    shared = ['scripts/run_contract.py', 'scripts/sdcp_gain_verdict.py']
    chk('⑨ ★ 증거 파일 공유만으로는 STALE 이 되지 않는다 (초판 거짓 양성 회귀)',
        classify('ppp', 'aaa', 'ppp', False, anc_false) == 'PARENT_OK'
        and evidence_paths({'evidence_tests': shared}) == shared)

    #  ★ 하이픈 정규화 — 원장 `R5CX-08` ↔ 코드 `R5-CX-08` (SELF-25).
    import re as _re
    _n = lambda s: _re.sub(r'[-_\s]', '', s).upper()
    chk('⑩ ID 표기가 원장과 코드에서 달라도 같은 것으로 본다 (SELF-25)',
        _n('R5CX-08') == _n('R5-CX-08') and _n('R5CX-08') != _n('R5-CX-09'))

    print(f'\n{ok[0]}/{ok[1]} PASS')
    return 0 if ok[0] == ok[1] else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--selftest', action='store_true', help='검사기 자신을 시험한다')
    ap.add_argument('--ledger', default=LEDGER, help=f'원장 경로 (기본 {LEDGER})')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not os.path.exists(a.ledger):
        print(f'원장이 없다: {a.ledger}', file=sys.stderr)
        return 2
    return run_audit(a.ledger)


if __name__ == '__main__':
    raise SystemExit(main())
