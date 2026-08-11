#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CLAUDE.md 컨텍스트 예산 — 섹션별 토큰 비용을 재고, **닫힌 이력**을 안전하게 발췌한다.

왜 (2026-08-11 실측):
  CLAUDE.md 는 매 세션 **전부** 로드된다 — 147 KB · 2054 줄 · ~44,100 토큰.
  그 중 최대 소비 섹션 다수가 **이미 닫힌 파생 이력**이다.  극단적 예:
  `σ_electronic Stage 21` 3,361 토큰은 같은 파일이 스스로 "SUPERSEDED by Stage 22.5"
  라고 적어 놓은 폐기본인데, 매 세션 그대로 실린다.

  ⚠ 그런데 **산문 압축(caveman 류)은 우리에게 위험하다** — 이 파일의 가치는 정확히
  한정어에 있다 ("DO NOT re-screen φc", "기울기는 하한", "relative-only",
  "φ_AM<0.3 외삽 금지").  요약하면 제일 먼저 깎이는 것이 그것들이다.

  ⇒ 압축이 아니라 **발췌**: 본문(파생 과정·표·이력)은 docs/ 로 옮기고, CLAUDE.md 에는
    ① 제목 ② 한 줄 요지 ③ 포인터 ④ **제약 줄 전부를 원문 그대로** 남긴다.
    제약이 한 줄이라도 사라지면 이 도구가 **거부**한다 (그게 이 도구의 존재 이유다).

토큰 추정: 한글 1자≈1.2 tok · 그 외 3.5자≈1 tok — 거칠지만 **일관**되므로 상대비교와
예산 판단에는 충분하다.  절대 토큰 수를 인용하지 말 것 (등급 B).

사용:
    python3 scripts/context_budget.py                     # 섹션별 예산표
    python3 scripts/context_budget.py --closed            # 발췌 후보만
    python3 scripts/context_budget.py --extract "Stage 21" --to docs/sigma_e_stage21_history.md
    python3 scripts/context_budget.py --extract "Stage 21" --to ... --dry-run
    python3 scripts/context_budget.py --selftest
"""
from __future__ import annotations

import argparse
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DOC = os.path.join(REPO, 'CLAUDE.md')

#: 이 표식이 있는 줄은 **제약**이다 — 발췌해도 CLAUDE.md 에 원문 그대로 남아야 한다.
#   경험칙이 아니라 이 리포에서 실제로 사고를 막아 온 표식들.
CONSTRAINT_MARK = re.compile(
    r'(⚠|★|DO NOT|NEVER|금지|하지 말|말 것|인용 금지|재적합|동결|FROZEN|LOCKED|주의)')

#: 섹션이 "닫혔다" 는 신호 — 발췌 **후보** 판정용 (자동 발췌는 하지 않는다).
CLOSED_MARK = re.compile(
    r'(SUPERSEDED|FINALIZED|FINAL\b|CLOSED|COMPLETE|DONE|RESOLVED|기각|닫힘|완료|폐기)')

#: 아직 도는 일이라는 신호 — 닫힘 표식이 있어도 이게 있으면 후보에서 뺀다.
ACTIVE_MARK = re.compile(r'(진행중|진행 중|대기|PENDING|TODO|남은 것|예정|실행중|active)')


def est_tokens(text):
    ko = sum(1 for c in text if '가' <= c <= '힣')
    return int(ko * 1.2 + (len(text) - ko) / 3.5)


def sections(text):
    """→ [(heading, body, start_idx, end_idx)] — `##`/`###` 기준.  본문 순서 보존."""
    hits = [m for m in re.finditer(r'^(#{2,3} .*)$', text, re.M)]
    out = []
    for i, m in enumerate(hits):
        end = hits[i + 1].start() if i + 1 < len(hits) else len(text)
        out.append((m.group(1), text[m.end():end], m.start(), end))
    return out


def constraints_of(body):
    """제약 **문단**들 — 표식이 든 문단을 통째로, 원문 그대로.

    ⚠ 줄 단위로 뽑으면 안 된다 (2026-08-11 dry-run 에서 실제로 당했다):
      `⚠ DO NOT add more form terms.  The form is at the joint info-theoretic`
    에서 끊기고 다음 줄 "ceiling of: (a) …" 이 사라졌다.  **잘린 경고는 없느니만 못하다**
    — 읽는 쪽은 완결된 문장으로 착각한다.  `Sub-definitions (all FROZEN):` 도 같은
    문제로 정작 정의 본문을 잃었다.
    → 빈 줄로 나눈 블록 중 표식이 **하나라도** 든 블록을 통째로 보존한다.
      과다 포착 쪽으로 틀리는 것이 안전한 방향이다 (제약은 잃으면 안 되므로).
    """
    out, cur = [], []
    for ln in body.splitlines():
        if ln.strip():
            cur.append(ln.rstrip())
        else:
            if cur and any(CONSTRAINT_MARK.search(x) for x in cur):
                out.append('\n'.join(cur))
            cur = []
    if cur and any(CONSTRAINT_MARK.search(x) for x in cur):
        out.append('\n'.join(cur))
    return out


def classify(heading, body):
    """→ 'closed' | 'active' | 'plain'."""
    blob = heading + '\n' + body
    if ACTIVE_MARK.search(blob):
        return 'active'
    return 'closed' if CLOSED_MARK.search(blob) else 'plain'


def budget(text):
    rows = []
    for h, b, s, e in sections(text):
        rows.append({'heading': h, 'tok': est_tokens(b), 'kind': classify(h, b),
                     'n_constraint': len(constraints_of(b)), 'start': s, 'end': e})
    return rows


def make_stub(heading, body, doc_rel, summary=None):
    """발췌 후 CLAUDE.md 에 남길 스텁.  제약 줄은 **원문 그대로** 전부 보존."""
    cons = constraints_of(body)
    first = next((ln.strip() for ln in body.splitlines() if ln.strip()), '')
    lines = [heading, '',
             (summary or first)[:300], '',
             f'전문(파생·표·이력) → `{doc_rel}`.  아래는 **구속력 있는 문단만** 원문 그대로:', '']
    lines += cons
    return '\n'.join(lines) + '\n\n'


def extract(text, needle, doc_rel, summary=None, force=False):
    """→ (새 CLAUDE.md, 발췌된 섹션 원문, 통계).

    두 가지를 **거부**한다:
      ① 제약 줄 유실 (그게 이 도구의 존재 이유)
      ② **절감이 0 이하** — 스텁에도 보일러플레이트(포인터·요지)가 들고, 제약 줄은
         전부 남으므로 제약 밀도가 높거나 짧은 섹션은 발췌하면 **되레 늘어난다**.
         selftest 6 이 이걸 잡았다: 작은 fixture 섹션에서 실제로 증가했다.
         → 이득이 없으면 옮기지 않는 게 맞다 (ponytail 사다리 1: 필요한가).
    """
    cand = [r for r in budget(text) if needle in r['heading']]
    if not cand:
        raise SystemExit(f'ABORT — 그 제목을 못 찾음: {needle!r}')
    if len(cand) > 1:
        raise SystemExit('ABORT — 여러 섹션이 걸림:\n  ' +
                         '\n  '.join(r['heading'][:80] for r in cand))
    r = cand[0]
    h, b = r['heading'], text[r['start'] + len(r['heading']):r['end']]
    stub = make_stub(h, b, doc_rel, summary)
    new = text[:r['start']] + stub + text[r['end']:]

    # ★ 계약 검증: 제약 줄이 하나라도 새 본문에서 사라지면 거부한다.
    lost = [c for c in constraints_of(b) if c.strip() not in new]
    if lost:
        raise SystemExit('ABORT — 제약 문단이 유실됩니다 (발췌 거부):\n  ' +
                         '\n  '.join(x.strip()[:100] for x in lost[:5]))
    stats = {'before': est_tokens(text), 'after': est_tokens(new),
             'section': r['tok'], 'kept_constraints': len(constraints_of(b)),
             # ★ 미리보기는 **스텁 자체**를 돌려준다.  needle 로 새 본문을 다시 찾으면
             #   다른 섹션의 언급("… section below" 등)에 걸려 엉뚱한 자리를 보여준다
             #   (2026-08-11 dry-run 에서 실제로 그랬다).
             'stub': stub}
    stats['saved'] = stats['before'] - stats['after']
    if stats['saved'] <= 0 and not force:
        raise SystemExit(
            f'ABORT — 절감이 없습니다 ({stats["saved"]:+,} tok).  이 섹션은 {r["tok"]:,} tok 인데 '
            f'제약 {stats["kept_constraints"]} 문단이 전부 남아야 해서 스텁이 원본만큼 큽니다.\n'
            '       옮기지 않는 것이 맞습니다 (--force 로 무시 가능하나 권하지 않음).')
    return new, h + b, stats


# ───────────────────────────── selftest ─────────────────────────────

_DOC = """# Root

## ★ 활성 트랙 (진행중)
지금 도는 일.  ⚠ 이건 활성이라 발췌 금지.

## σ_x Stage 9 FINALIZED — 옛 파생
파생 과정 한 줄.
표: a b c
자잘한 이력이 길게 이어진다.

⚠ DO NOT re-screen φc — 이건 반드시 남아야 한다.
★ 기울기는 하한으로만 인용할 것.

평범한 서술 줄.

## 그냥 섹션
표식 없는 본문.
"""


def _selftest():
    ok = fail = 0

    def chk(m, c):
        nonlocal ok, fail
        print(('  PASS  ' if c else '  FAIL  ') + m)
        ok, fail = ok + (1 if c else 0), fail + (0 if c else 1)

    rows = budget(_DOC)
    kinds = {r['heading'][:12]: r['kind'] for r in rows}
    chk('1) FINALIZED 섹션 = closed', rows[1]['kind'] == 'closed')
    chk('2) ★ 진행중 표식이 있으면 closed 로 안 센다 (활성 보호)', rows[0]['kind'] == 'active')
    chk('3) 표식 없는 섹션 = plain', rows[2]['kind'] == 'plain')
    chk('4) 토큰 추정이 양수·단조', all(r['tok'] > 0 for r in rows))

    body = _DOC.split('## σ_x Stage 9 FINALIZED — 옛 파생')[1].split('## 그냥')[0]
    cons = constraints_of(body)
    chk('5) 붙어 있는 두 경고 = 한 문단 (원문 구조 보존)',
        len(cons) == 1 and 'DO NOT re-screen φc' in cons[0] and '기울기는 하한' in cons[0])
    # ★ 여러 줄 경고: 표식 없는 이어지는 줄까지 통째로 (잘린 경고 방지)
    multi = "본문.\n\n⚠ DO NOT 이렇게 하라.  이 문장은\n   다음 줄로 이어진다.\n\n딴 문단.\n"
    mc = constraints_of(multi)
    chk('5b) ★ 여러 줄 경고를 통째로 보존 (문장 중간 절단 금지)',
        len(mc) == 1 and '다음 줄로 이어진다' in mc[0] and '딴 문단' not in mc[0])
    chk('5c) 표식 없는 문단은 안 잡는다', '본문.' not in '\n'.join(mc))

    # ★ 작은 섹션은 발췌해도 이득이 없다 → 거부해야 한다 (selftest 6 이 처음 잡은 것)
    try:
        extract(_DOC, 'Stage 9', 'docs/hist.md')
        chk('6) ★ 절감 없는 발췌는 거부 (스텁 보일러플레이트 > 이득)', False)
    except SystemExit as e:
        chk('6) ★ 절감 없는 발췌는 거부 (스텁 보일러플레이트 > 이득)', '절감이 없습니다' in str(e))

    # 이득이 나는 큰 섹션 — 파생 본문을 길게 (제약 밀도는 낮게)
    big = _DOC.replace('자잘한 이력이 길게 이어진다.',
                       '자잘한 이력이 길게 이어진다.\n' + '파생 유도 문장이 계속된다. ' * 120)
    new, cut, st = extract(big, 'Stage 9', 'docs/hist.md')
    chk(f'6b) 큰 섹션은 절감 (−{st["saved"]:,} tok)', st['saved'] > 0)
    chk('7) ★ 제약 문단이 원문 그대로 남는다',
        'DO NOT re-screen φc' in new and '기울기는 하한으로만' in new)
    chk('8) 본문(파생·표)은 빠진다', '표: a b c' not in new and '표: a b c' in cut)
    chk('9) 포인터가 스텁에 있다', 'docs/hist.md' in new)
    chk('10) 제목은 유지', '## σ_x Stage 9 FINALIZED' in new)

    # ★ 계약: 제약을 지우도록 조작하면 거부해야 한다
    import types
    orig = globals()['make_stub']
    globals()['make_stub'] = lambda h, b, d, s=None: h + '\n\n(제약 다 날림)\n\n'
    try:
        extract(big, 'Stage 9', 'docs/hist.md')
        chk('11) ★ 제약 유실 시 거부', False)
    except SystemExit as e:
        chk('11) ★ 제약 유실 시 거부', '제약 문단이 유실' in str(e))
    finally:
        globals()['make_stub'] = orig

    try:
        extract(big, '없는제목', 'docs/x.md')
        chk('12) 없는 제목 = 중단', False)
    except SystemExit:
        chk('12) 없는 제목 = 중단', True)
    try:
        extract(big, '## ', 'docs/x.md')
        chk('13) 모호한 제목 = 중단 (여러 섹션)', False)
    except SystemExit as e:
        chk('13) 모호한 제목 = 중단 (여러 섹션)', '여러 섹션' in str(e))

    # 실제 CLAUDE.md 에 대한 위생 검사
    if os.path.exists(DEFAULT_DOC):
        real = open(DEFAULT_DOC, encoding='utf-8').read()
        rr = budget(real)
        chk(f'14) 실제 CLAUDE.md 파싱 ({len(rr)} 섹션 · ~{est_tokens(real):,} tok)', len(rr) > 20)
        chk('15) ★ 활성 트랙이 발췌 후보에 안 들어간다',
            not any('활성 트랙' in r['heading'] and r['kind'] == 'closed' for r in rr))
    print(f'\ncontext_budget selftest: {ok}/{ok + fail} PASS')
    return 0 if fail == 0 else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--doc', default=DEFAULT_DOC)
    ap.add_argument('--closed', action='store_true', help='발췌 후보(closed)만 표시')
    ap.add_argument('--top', type=int, default=15)
    ap.add_argument('--extract', help='발췌할 섹션 제목의 일부')
    ap.add_argument('--to', help='발췌 본문을 쓸 리포-상대 경로 (docs/...)')
    ap.add_argument('--summary', help='스텁에 넣을 한 줄 요지')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--force', action='store_true', help='절감 0 이하여도 강행 (권하지 않음)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    text = open(a.doc, encoding='utf-8').read()

    if a.extract:
        if not a.to:
            ap.error('--extract 에는 --to 가 필요합니다')
        new, cut, st = extract(text, a.extract, a.to, a.summary, a.force)
        print(f'섹션 ~{st["section"]:,} tok · 제약 {st["kept_constraints"]} 문단 보존 · '
              f'전체 {st["before"]:,} → {st["after"]:,} tok  (−{st["saved"]:,})')
        if a.dry_run:
            print('\n(dry-run — 아무것도 안 씀).  CLAUDE.md 에 남을 스텁:\n')
            print('\n'.join('  | ' + ln for ln in st['stub'].rstrip().splitlines()))
            return 0
        dest = os.path.join(REPO, a.to)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, 'w', encoding='utf-8') as fh:
            fh.write(f'# {a.extract} — CLAUDE.md 에서 발췌한 전문\n\n'
                     f'> {os.path.basename(a.doc)} 의 컨텍스트 예산을 위해 본문을 옮긴 것.\n'
                     f'> 구속력 있는 줄은 {os.path.basename(a.doc)} 에 원문 그대로 남아 있다.\n'
                     f'> 발췌 도구: `scripts/context_budget.py` (제약 유실 시 거부).\n\n' + cut)
        with open(a.doc, 'w', encoding='utf-8') as fh:
            fh.write(new)
        print(f'→ 본문 {a.to} · 스텁은 {os.path.basename(a.doc)} 에 남김')
        return 0

    rows = budget(text)
    tot = est_tokens(text)
    print(f'{os.path.basename(a.doc)} — ~{tot:,} tok · {len(rows)} 섹션 (매 세션 전부 로드)\n')
    sel = [r for r in rows if r['kind'] == 'closed'] if a.closed else rows
    sel = sorted(sel, key=lambda r: -r['tok'])[:a.top]
    print(f'{"tok":>7}  {"상태":6s} {"제약문단":>6}  섹션')
    for r in sel:
        print(f'{r["tok"]:7,}  {r["kind"]:6s} {r["n_constraint"]:4d}  {r["heading"][:66]}')
    closed = [r for r in rows if r['kind'] == 'closed']
    print(f'\n닫힌 섹션 {len(closed)}개 · ~{sum(r["tok"] for r in closed):,} tok '
          f'({sum(r["tok"] for r in closed) / max(tot, 1) * 100:.0f}% of CLAUDE.md)')
    print('  발췌: --extract "<제목 일부>" --to docs/<파일>.md  (제약 줄은 자동 보존, '
          '유실되면 거부)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
