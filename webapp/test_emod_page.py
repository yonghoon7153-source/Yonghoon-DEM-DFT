#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""유효 영률 · 응력 페이지 회귀 (`/emod` · 2026-11-06).

1저자 11-06 질문 (*"유효영률로 가압하면 응력은 1/20 이라 못 쓰는 값이 아닌가"*) 과 요청 (*"궁금증이 생기고 해결해 나가서
더 전극 형태에 맞게 · webapp 에 별도 페이지 · MPM 응력장도 더 재현성 있게 · 언로딩도 MPM 같은 프로세스로"*) 의 화면.
정본 = `docs/effective_modulus_stress.md` — 화면은 **그 파일을 읽어** 보인다 (템플릿 · 코드에 문장을 베끼지 않는다 ·
정본을 고치면 화면이 같이 바뀐다 · 규율 ④).  읽지 못하면 무엇이 깨졌는지 적고 옛 문장을 보이지 않는다 (fail-closed).

  python3 webapp/test_emod_page.py
"""
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
    here = Path(__file__).resolve().parent
    doc = here.parent / 'docs' / 'effective_modulus_stress.md'
    src = doc.read_text(encoding='utf-8') if doc.exists() else ''
    m = re.findall(r'<!-- EMOD:UPDATED (\d{4}-\d{2}-\d{2}) -->', src)

    # ① 정본이 있고 갱신 표지가 정확히 하나
    chk('① 정본 docs/effective_modulus_stress.md 가 있고 갱신 표지가 하나', bool(src) and len(m) == 1)

    r = c.get('/emod')
    body = r.get_data(as_text=True)
    # ② 페이지가 열린다
    chk('② GET /emod = 200', r.status_code == 200)
    # ③ 갱신 날짜를 정본에서 읽어 보인다
    chk('③ 갱신 날짜 = 정본 표지', bool(m) and f'갱신 {m[0]}' in body)
    # ④ 요약 표가 표로 그려진다 (markdown tables)
    chk('④ 요약 표 머리 "쓸 수 있나" 가 <th>', re.search(r'<th[^>]*>\s*쓸 수 있나\s*</th>', body) is not None)
    # ⑤ 질문 기록 행이 정본에서 온다
    rows = re.findall(r'\|\s*(EM-\d{2})\s*\|', src)
    chk('⑤ 정본의 질문 기록 행 (EM-NN) 이 모두 화면에', bool(rows) and all(x in body for x in rows))
    # ⑥ 메뉴에 링크
    rh = c.get('/hetero').get_data(as_text=True)
    chk('⑥ 다른 화면 메뉴에 /emod 링크', 'href="/emod"' in rh)

    # ⑦ 템플릿에 정본 문장을 베끼지 않는다
    tpl = (here / 'templates' / 'emod.html').read_text(encoding='utf-8')
    copied = [s for s in ('판 압력', '하중 제어', 'EM-01', 'Love–Weber', '쓸 수 있나') if s in tpl]
    chk(f'⑦ 템플릿에 정본 문장 없음 (발견 {copied})', not copied)

    # ⑧ – ⑪ 정본을 바꿔 끼우면 화면이 따라오고, 깨지면 fail-closed
    orig = webapp.EMOD_MD
    with tempfile.TemporaryDirectory() as td:
        try:
            p = Path(td) / 'effective_modulus_stress.md'
            p.write_text('# 시험\n\n<!-- EMOD:UPDATED 2031-01-02 -->\n\n고유문구-가나다-7731\n', encoding='utf-8')
            webapp.EMOD_MD = p
            b = c.get('/emod').get_data(as_text=True)
            chk('⑧ 다른 정본을 끼우면 그 문장과 날짜를 보인다', '고유문구-가나다-7731' in b and '갱신 2031-01-02' in b)

            webapp.EMOD_MD = Path(td) / 'none.md'
            r2 = c.get('/emod'); b = r2.get_data(as_text=True)
            chk('⑨ 파일 없음 = 200 + "읽지 못했다" · 옛 문장 없음',
                r2.status_code == 200 and '읽지 못했다' in b and '고유문구-가나다-7731' not in b)

            p.write_text('<!-- EMOD:UPDATED 2031-01-02 -->\n<!-- EMOD:UPDATED 2031-01-03 -->\n둘표지-3390\n', encoding='utf-8')
            webapp.EMOD_MD = p
            b = c.get('/emod').get_data(as_text=True)
            chk('⑩ 갱신 표지 둘 = 거부 · 본문 안 보임', '갱신 표지가 2 개' in b and '둘표지-3390' not in b)

            p.write_text('# 표지 없음\n\n본문만-5521\n', encoding='utf-8')
            b = c.get('/emod').get_data(as_text=True)
            chk('⑪ 갱신 표지 없음 = 거부 · 본문 안 보임', '갱신 표지가 0 개' in b and '본문만-5521' not in b)

            p.write_text('<!-- EMOD:UPDATED 2031-01-02 -->\n\n', encoding='utf-8')
            b = c.get('/emod').get_data(as_text=True)
            chk('⑫ 표지만 있고 본문 빔 = 거부', '본문이 비어 있다' in b)
        finally:
            webapp.EMOD_MD = orig

    print(f'\n{_ok} PASS · {len(_fail)} FAIL')
    return 1 if _fail else 0


if __name__ == '__main__':
    sys.exit(main())
