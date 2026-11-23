#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""주간보고 금지어 검사 — 교수님이 읽는 덱에 내부 운영 말이 남았는지 본다.

    python3 lint_weekly.py deck.pptx          # 금지어 0 이면 rc 0
    python3 lint_weekly.py --selftest

★ 1저자 11-23: "교수님한테 제출하는건데 뭔 나만 알 수 있는 내용으로 주간보고를 하냐".
  금지어 = 우리 작업 기록에서만 뜻이 있는 말 (시도 번호 · 원장 · 넘김 · rc · 서버 이름 · 커밋 ·
  내부 단계 코드 …).  교수님이 아는 분야 말 (DEM · MPM · SE · SBE · DBE · PTFE · SDCP ·
  porosity · tortuosity · σ) 은 금지가 아니다.
★ 빈칸 (이름이 'SLOT ' 으로 시작하는 상자) 은 1저자에게 주는 지시라 검사에서 빼고, 남은 수만 센다.
  '1저자 작성' 표시도 남은 수만 센다 — 제출 전에 0 이어야 한다.
★ pptx 는 한 낱말을 여러 run 으로 쪼개므로 문단 단위로 붙여 읽는다 (run 단위로 읽으면 놓친다).
"""
from __future__ import annotations

import argparse
import re
import sys

#: (이름, 정규식) — 하나라도 걸리면 rc 1
BANNED = [
    ('시도 번호', r'시도\s*\d|\battempts?\b'),
    ('원장 · 회복 · 넘김', r'원장|ledger|회복 대기|RECOVER|넘김|\brelay'),
    ('종료 코드', r'\brc\s*\d|exit\s*code|ExitCode|COMPLETED|RESTORED'),
    ('잡 · 작업 번호', r'\bjob\b|잡\s*(번호|\d)|(?<![\d.,])\d{6,}(?![\d.,])'),
    ('서버 이름', r'\b(kgy|gabia|ibb|v100|uma|WSL)\b'),
    ('커밋 · 해시', r'커밋|\bcommit\b|\bsha\d*\b|해시|\b(?=[0-9a-f]*[a-f])(?=[0-9a-f]*\d)[0-9a-f]{7,40}\b'),
    ('게이트 · 봉인', r'게이트|\bgate\b|봉인'),
    ('파일 · 경로', r'\.(py|json|md|sh|txt|liggghts)\b|\bdocs/|\bscripts/|~/'),
    ('결함 원장 번호', r'\b(SELF|RCA2?|PC5|KG50R?|ULKR?|L214[A-Z]*|G2RR?\d?|HBR\d?|SEM\d*|RINT[A-Z]*|SUPR?|LHSC?)-[A-Z0-9]*\d+'),
    ('내부 단계 코드', r'\bP[01]\b|\bc[01]\b|R_?j|\bU6|\bU[BTCV]\b|\bB[123](-?[UC])?\b|\bW9\b|\bE0\b|\bN0\b|\bS0\b|\bRJ\b|\bF(8|12|16|24)\b|\bA5\b'),
    ('리뷰 판정 말', r'\bCodex\b|\bHOLD\b|\bGO\b|\bPASS\b|\bFAIL|\bTECH\b|claimed_fixed|verified'),
    ('운영 말', r'판독|(?<![가-힣])팔(?![가-힣])|팔\s*\d|예측 단위|개발 자료|사다리|단위\s*\d+\s*/'),
]
TODO = r'1저자 작성'


def deck_paragraphs(path):
    """→ [(장 번호, 모양 이름, 문단 글)] — 발표 순서 · 문단 단위로 붙여 읽음 · 표 · 메모 포함."""
    from pptx import Presentation
    prs = Presentation(path)
    out = []
    for i, s in enumerate(prs.slides, start=1):
        def walk(shapes):
            for sh in shapes:
                if sh.shape_type == 6:                   # 묶음
                    yield from walk(sh.shapes)
                    continue
                if sh.has_text_frame:
                    for p in sh.text_frame.paragraphs:
                        yield sh.name, ''.join(r.text for r in p.runs)
                if getattr(sh, 'has_table', False) and sh.has_table:
                    for row in sh.table.rows:
                        for c in row.cells:
                            for p in c.text_frame.paragraphs:
                                yield sh.name, ''.join(r.text for r in p.runs)
                if getattr(sh, 'has_chart', False) and sh.has_chart:
                    ch = sh.chart
                    for pl in ch.plots:
                        yield sh.name, ' '.join(str(c) for c in pl.categories)
                        for se in pl.series:
                            yield sh.name, se.name
        for name, txt in walk(s.shapes):
            out.append((i, name, txt))
        if s.has_notes_slide:
            for p in s.notes_slide.notes_text_frame.paragraphs:
                out.append((i, '메모', ''.join(r.text for r in p.runs)))
    return out


def lint(paras):
    hits, slots, todos = [], 0, 0
    seen_slot = set()
    for i, name, txt in paras:
        if name.startswith('SLOT '):
            seen_slot.add((i, name))
            continue
        if re.search(TODO, txt):
            todos += 1
        for label, rx in BANNED:
            for m in re.finditer(rx, txt):
                hits.append((i, label, m.group(0), txt.strip()[:70]))
    slots = len(seen_slot)
    return hits, slots, todos


def _selftest():
    bad = [(1, 'x', '시도 4 채택 · 원장 회복 대기'), (2, 'x', 'kgy rc 3 · job 368469'),
           (3, 'x', '커밋 5ad5a30be7 · docs/a.md'), (4, 'x', 'P0 · c1 · R_j lo · UB → UT'),
           (5, 'x', 'Codex HOLD · 판독 20/20 · 팔 하나'), (6, 'x', 'SELF-183 · RCA2-05')]
    good = [(1, 'x', 'SBE 실측 1.63 mS/cm · DBE 4.68 mS/cm · PTFE · SDCP'),
            (2, 'x', '원판 49 개 · 1.2 MPa · 16×16×4 · 접촉 약 56 만 쌍'),
            (3, 'x', 'MPM 2D 격자 해상도 · porosity · tortuosity · DEM'),
            (4, 'SLOT 그림 ①', 'ibb 덤프 → 렌더 (빈칸 지시는 검사 밖)')]
    h, _, _ = lint(bad)
    labels = {x[1] for x in h}
    need = {'시도 번호', '원장 · 회복 · 넘김', '서버 이름', '종료 코드', '잡 · 작업 번호', '커밋 · 해시',
            '파일 · 경로', '내부 단계 코드', '리뷰 판정 말', '운영 말', '결함 원장 번호'}
    miss = need - labels
    h2, slots, _ = lint(good)
    ok = (not miss) and (not h2) and slots == 1
    print(f'selftest {"✓" if ok else "✗"} — 나쁜 예 {len(labels)}/{len(need)} 부류 잡음 · 좋은 예 걸림 {len(h2)} · 빈칸 {slots}'
          + (f' · 놓친 부류 {sorted(miss)}' if miss else '') + (f' · 오탐 {h2}' if h2 else ''))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description='주간보고 금지어 검사')
    ap.add_argument('deck', nargs='?')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if not a.deck:
        ap.error('deck.pptx 필요')
    hits, slots, todos = lint(deck_paragraphs(a.deck))
    for i, label, word, ctx in hits:
        print(f'  ✗ {i:2d} 장 · {label:10s} · "{word}"  ← {ctx}')
    print(f'금지어 {len(hits)} · 빈칸 그림 {slots} · 1저자 작성 표시 {todos}'
          + ('  → 제출 전 빈칸 · 표시를 채울 것' if (slots or todos) else ''))
    return 1 if hits else 0


if __name__ == '__main__':
    sys.exit(main())
