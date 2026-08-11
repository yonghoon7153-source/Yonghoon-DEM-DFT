#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""세미나 페이지 회귀 — 덱 JSON 계약 · 출처 파일 창구 · 화면 배선.

`/seminar` 을 md 뷰어에서 **슬라이드 콘솔**로 개편하면서 생긴 계약을 고정한다.
특히 `/api/seminar/file` 은 리포 파일을 평문으로 내주는 창구라 **임의 파일 열람으로
번지지 않는지**가 핵심이다 (접두어·확장자 화이트리스트 + 경로탈출 거부).

  python3 webapp/test_seminar_page.py
"""
import json
import os
import sys

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
    repo = os.path.dirname(os.path.dirname(os.path.abspath(webapp.__file__)))

    # ══ 1) 덱 JSON 계약 ══
    r = c.get('/api/seminar/slides')
    j = r.get_json()
    chk('1) /api/seminar/slides 가 200 + ok', r.status_code == 200 and j.get('ok'))
    slides = j.get('slides') or []
    chk('2) 슬라이드가 있다', len(slides) >= 10 and j.get('n_slides') == len(slides))
    chk('3) 각 슬라이드에 계약 키가 다 있다',
        all({'n', 'kicker', 'title', 'lead', 'tables', 'charts',
             'figure_slots', 'extra', 'notes', 'sources'} <= set(s) for s in slides))
    chk('4) ★ 대본(notes)이 대부분 있다 — 이 페이지의 존재 이유',
        sum(1 for s in slides if s['notes']) >= len(slides) - 1)
    chk('5) ★ 차트가 보존됐다 (σ_SDCP 민감도가 차트로만 들어 있다)',
        j.get('n_charts', 0) >= 1
        and any(s['charts'] and s['charts'][0].get('series') for s in slides))
    chk('6) 슬라이드 번호가 1..N 로 연속',
        [s['n'] for s in slides] == list(range(1, len(slides) + 1)))

    # ══ 2) ★ 출처 파일 창구 — 임의 파일 열람이 되면 안 된다 ══
    r = c.get('/api/seminar/file?p=docs/mpm_platen_kinematic_stop_defect.md')
    chk('7) 화이트리스트 안 파일은 열린다', r.status_code == 200 and len(r.data) > 100)

    #   (a) 접두어/확장자 밖 → 400
    for bad in ('CLAUDE.md', 'README.md', 'docs/x.exe', '/etc/passwd', 'venv/pyvenv.cfg'):
        rr = c.get('/api/seminar/file?p=' + bad)
        chk(f'8) 화이트리스트 밖 거부: {bad}', rr.status_code == 400)

    #   (b) ★ 접두어·확장자를 **만족하면서** 탈출하는 경로 → 400 (여기가 진짜 위험한 자리)
    for bad in ('docs/../../etc/passwd.md', 'scripts/../../CLAUDE.md',
                'docs/%2e%2e/%2e%2e/etc/x.md', 'docs/../CLAUDE.md'):
        rr = c.get('/api/seminar/file?p=' + bad)
        chk(f'9) ★ 탈출 거부(확장자 통과해도): {bad}',
            rr.status_code == 400)

    #   (c) 거부와 결손을 **구분**한다 — 로그에서 시도가 보여야 한다
    rr = c.get('/api/seminar/file?p=docs/definitely_absent_xyz.md')
    chk('10) ★ 없는 파일은 404 (400 거부와 구분된다)',
        rr.status_code == 404 and '없음' in rr.data.decode('utf-8', 'replace'))
    chk('11) 빈 파라미터도 안전', c.get('/api/seminar/file').status_code == 400)

    # ══ 3) 화면 배선 — 구현과 배선은 다르다 (오늘 세 번 겪었다) ══
    r = c.get('/seminar')
    html = r.data.decode('utf-8', 'replace')
    chk('12) /seminar 200', r.status_code == 200)
    for probe, why in (('/api/seminar/slides', '덱 API 를 실제로 부른다'),
                       ('/api/seminar/file', '출처 칩이 파일 창구를 쓴다'),
                       ('sm-notes', '대본 영역이 있다'),
                       ('ArrowRight', '←/→ 슬라이드 이동'),
                       ('sm-flag', '한계/철회 배지')):
        chk(f'13) 배선: {probe} ({why})', probe in html)

    # ══ 4) 덱 파일과 JSON 이 같은 덱을 가리키는가 (어긋나면 화면이 옛 덱을 설명한다) ══
    chk('14) ★ JSON 의 deck 경로가 실제 파일이다',
        os.path.exists(os.path.join(repo, (j.get('deck') or '').replace('/', os.sep))))
    chk('15) ★ 다운로드 덱과 JSON 덱이 같은 파일',
        os.path.basename(j.get('deck') or '') == os.path.basename(webapp._SEMINAR_DECK))

    # ══ 5) 슬라이드 5·6 의 한계 공개가 실제 덱에 있는가 (배지가 허구면 안 된다) ══
    blob = json.dumps(slides, ensure_ascii=False)
    chk('16) ★ platen 결함 공개가 덱 안에 실재한다 (배지의 근거)',
        'kinematic-stop' in blob or 'platen' in blob.lower())
    chk('17) ★ 독립성 철회 문구가 덱 안에 실재한다',
        'not an independent' in blob or 'one-way' in blob)

    print(f'\ntest_seminar_page: {_ok}/{_ok + len(_fail)} PASS'
          + (f'   FAILED: {_fail}' if _fail else ''))
    return 0 if not _fail else 1


if __name__ == '__main__':
    raise SystemExit(main())
