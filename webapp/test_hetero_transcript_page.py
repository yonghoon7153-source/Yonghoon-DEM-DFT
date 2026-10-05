#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""이종기술 회의록 해체 페이지 회귀 — 회의 둘 (09-18 · 10-02) 을 고를 수 있는가 · 회의 종합이 보이는가.

`/hetero/transcript` 는 원래 09-18 회의 하나만 보였다 (경로 상수 하나).  10-02 회의 (음성 336 · 1저자 10-05
*"낱낱이 정리해서 이종기술 관련 원장에"*) 를 넣으면서 회의 키 (8 자리 날짜) 로 고르게 했다 — 키는 등록부
(`app.HETERO_TRANSCRIPTS`) 에 있는 것만 받는다 (모르는 키 = 404 · 조용히 다른 회의를 보이지 않는다).

⑨–⑬ (10-05) — `/hetero` 가 **이종기술 논지 정본** (`docs/hetero_thesis.md` · 1저자 비준 10-05 *"이거 비준이고"*) 의
비준 블록 (`<!-- THESIS:BEGIN ratified=<날짜> -->` … `<!-- THESIS:END -->`) 과 비준 날짜를 **그 파일에서 읽어** 띄우는가.  고정 문장은 한 곳에만 있다 —
템플릿 · 코드에 베껴 두면 정본을 고쳐도 화면이 옛 문장을 계속 보인다 (규율 ④ — 요약층은 강제되지 않으면 낡는다).
표지가 없거나 둘 이상이면 **읽지 못했다고 적는다** (조용히 비우거나 옛 문장을 보이지 않는다).

  python3 webapp/test_hetero_transcript_page.py
"""
import html as _html
import os
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

_ok, _fail = 0, []


def chk(name, cond):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}')


def main():
    import app as webapp
    c = webapp.app.test_client()
    reg = getattr(webapp, 'HETERO_TRANSCRIPTS', None)
    chk('① 회의 등록부 HETERO_TRANSCRIPTS 에 09-18 · 10-02 둘', isinstance(reg, dict) and {'20260918', '20261002'} <= set(reg or {}))

    r = c.get('/hetero/transcript?m=20261002')
    h = r.get_data(as_text=True)
    chk('② ?m=20261002 → 200 · 음성 336 · 발화 90 · 계약 통과 문구', r.status_code == 200 and '음성 336' in h
        and '발화 90' in h and '계약 여섯 통과' in h)
    chk('③ 10-02 회의 종합이 화면에 보인다 (논문 둘로 분리 · 정합도 지시 · 논지 물음)',
        '논문 둘로 분리' in h and '정합도 지시' in h and '논지 물음' in h)

    r = c.get('/hetero/transcript?m=20260918')
    h = r.get_data(as_text=True)
    chk('④ ?m=20260918 → 200 · 발화 61 (옛 회의 그대로)', r.status_code == 200 and '발화 61' in h)

    r = c.get('/hetero/transcript')
    h = r.get_data(as_text=True)
    chk('⑤ 키 없음 → 최신 회의 (10-02)', r.status_code == 200 and '음성 336' in h and '발화 90' in h)
    chk('⑥ 회의 고르기 링크 둘 (?m=20260918 · ?m=20261002)', '?m=20260918' in h and '?m=20261002' in h)

    bad = [k for k in ('20991231', '../etc', 'x', '2026100') if c.get('/hetero/transcript?m=' + k).status_code != 404]
    chk(f'⑦ 등록부 밖 키는 404 (조용히 다른 회의를 보이지 않는다) {bad or ""}', not bad)

    r = c.get('/hetero')
    h = r.get_data(as_text=True)
    chk('⑧ /hetero 에 두 회의 링크', r.status_code == 200 and '/hetero/transcript?m=20260918' in h
        and '/hetero/transcript?m=20261002' in h)

    # ── ⑨–⑬ 논지 정본 (10-05) ──────────────────────────────────────────────
    thesis_md = Path(__file__).resolve().parent.parent / 'docs' / 'hetero_thesis.md'
    src = thesis_md.read_text(encoding='utf-8')
    blocks = re.findall(r'<!-- THESIS:BEGIN ratified=(\d{4}-\d{2}-\d{2}) -->\n(.*?)\n<!-- THESIS:END -->', src, re.S)
    date = blocks[0][0] if blocks else ''
    first = next((ln for ln in (blocks[0][1].splitlines() if blocks else []) if ln.strip()), '')
    sentence = first.strip().strip('*').strip()          # **"…"** → "…"  (시험이 정본에서 직접 뽑는다)

    def _text(page):
        return re.sub(r'\s+', ' ', _html.unescape(re.sub(r'<[^>]+>', ' ', page)))

    r = c.get('/hetero')
    h = r.get_data(as_text=True)
    ht = _text(h)
    chk('⑨ /hetero 에 비준 블록의 고정 문장 그대로 (정본 파일에서 뽑아 대조)',
        len(blocks) == 1 and len(sentence) > 40 and sentence in ht)
    chk('⑩ 하지 않는 말 · 예측 P1 · P2 · P3 이 함께 (비준 셋)',
        '하지 않는 말' in ht and all(f'P{i}.' in ht for i in (1, 2, 3)))
    chk(f'⑪ 정본 경로 docs/hetero_thesis.md · 비준 날짜 = 정본 표지의 날짜 ({date or "없음"})',
        bool(date) and 'docs/hetero_thesis.md' in ht and f'비준 {date}' in ht)

    probe = '혼합 응집(특히 SE–SE)이 줄어 분산이 좋아지고'
    tpl = (Path(__file__).resolve().parent / 'templates' / 'hetero.html').read_text(encoding='utf-8')
    code = Path(webapp.__file__).read_text(encoding='utf-8')
    chk('⑫ 고정 문장을 템플릿 · 코드에 베끼지 않는다 (정본 한 곳)',
        probe in src and probe not in tpl and probe not in code)

    orig = getattr(webapp, 'HETERO_THESIS_MD', None)
    bad = []
    with tempfile.TemporaryDirectory() as td:
        cases = {
            'no_marker': re.sub(r'<!-- THESIS:(BEGIN[^>]*|END) -->', '', src),
            'no_date': src.replace(f'<!-- THESIS:BEGIN ratified={date} -->', '<!-- THESIS:BEGIN -->'),
            'two_blocks': src + f'\n<!-- THESIS:BEGIN ratified={date} -->\n**"딴 문장"**\n<!-- THESIS:END -->\n',
            'empty_block': re.sub(r'(<!-- THESIS:BEGIN[^>]*-->\n).*?(\n<!-- THESIS:END -->)', r'\1 \2', src, flags=re.S),
            'missing_file': None,
        }
        for name, body in cases.items():
            fp = Path(td) / f'{name}.md'
            if body is not None:
                fp.write_text(body, encoding='utf-8')
            webapp.HETERO_THESIS_MD = fp
            try:
                t2 = _text(c.get('/hetero').get_data(as_text=True))
            finally:
                webapp.HETERO_THESIS_MD = orig
            if '논지 정본을 읽지 못했다' not in t2 or sentence in t2:
                bad.append(name)
    chk(f'⑬ 표지 없음 · 날짜 없음 · 둘 · 빈 블록 · 파일 없음 → "논지 정본을 읽지 못했다" (옛 문장 안 보임) {bad or ""}', not bad)

    print(f'\ntest_hetero_transcript_page: {_ok}/{_ok + len(_fail)} PASS' + (f'   FAILED: {_fail}' if _fail else ''))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
