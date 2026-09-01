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
    #  ★★ 2026-08-31 — 이 엔드포인트는 이제 **거부하는 것이 정상**이다.
    #    2026-08-06 덱 안의 SDCP 수치는 08-13 적대 리뷰로 철회됐고, 앱에 철회 게이트가
    #    붙어 그 덱을 슬라이드로 내보내지 않는다.  옛 검사는 `200 + ok` 와 슬라이드를
    #    요구했으므로 **앱이 안전해진 그 순간부터 빨간불**이었고, 웹앱 테스트가
    #    `check_all` 에 배선돼 있지 않아 아무도 몰랐다.
    #  ⇒ 새 계약을 검사한다: **거부하고, 철회임을 말하고, 이유를 준다.**
    #  ⚠ 테스트를 "통과하게" 고친 것이 아니다 — 검사 대상이 바뀐 것이고, 아래는 옛
    #    검사보다 **강한** 요구다 (거부만으로는 부족하고 사유·표지까지 본다).
    r = c.get('/api/seminar/slides')
    j = r.get_json() or {}
    chk('1) ★ 철회된 덱을 슬라이드로 내보내지 않는다 (ok=False)',
        r.status_code == 200 and j.get('ok') is False)
    chk('2) ★ 철회 표지를 명시한다 (retracted)', j.get('retracted') is True)
    chk('3) ★ 사유가 비어 있지 않다 — 왜 막혔는지 화면이 말할 수 있어야 한다',
        len(str(j.get('error') or '')) > 40)
    chk('4) ★ 사유가 철회 사실을 말한다', '철회' in str(j.get('error') or ''))
    chk('5) ★ 슬라이드를 딸려 보내지 않는다 (부분 노출 금지)',
        not j.get('slides'))
    #  ⚠ 게이트가 철회값 자체를 본문에 흘리면 그것대로 문제다 — 등록부는
    #    `claims.json` 이고 검사는 `check_review_findings --ban-sweep` 이 한다.
    #    여기서는 **응답이 값을 나열하지 않는지**만 형태로 본다.
    chk('6) 사유가 힌트를 함께 준다 (다음 행동)', bool(j.get('hint')))
    slides = j.get('slides') or []

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

    # ══ 4) 덱 파일 자체는 그대로 있어야 한다 (이력이므로 지우지 않는다) ══
    chk('14) ★ 덱 파일은 남아 있다 — 철회는 배포 차단이지 삭제가 아니다',
        os.path.exists(os.path.join(repo, webapp._SEMINAR_DECK.replace('/', os.sep))))
    chk('15) ★ 다운로드 창구도 같은 덱을 가리킨다',
        webapp._SEMINAR_DECK.endswith('.pptx'))

    # ══ 5) 철회 근거가 리포에 실재하는가 (배지가 허구면 안 된다) ══
    #  ⚠ 옛 검사는 이 문구를 **슬라이드 JSON 안**에서 찾았다.  게이트가 슬라이드를
    #    안 내주므로 그 자리는 이제 비어 있고, 근거는 **문서 쪽**에 있어야 한다.
    _defect = os.path.join(repo, 'docs', 'mpm_platen_kinematic_stop_defect.md')
    chk('16) ★ platen 결함 정본이 실재한다 (배지의 근거)', os.path.exists(_defect))
    _txt = open(_defect, encoding='utf-8', errors='replace').read() if os.path.exists(_defect) else ''
    chk('17) ★ 그 정본이 실제로 그 결함을 다룬다',
        'platen' in _txt.lower() or '플래튼' in _txt)

    print(f'\ntest_seminar_page: {_ok}/{_ok + len(_fail)} PASS'
          + (f'   FAILED: {_fail}' if _fail else ''))
    return 0 if not _fail else 1


if __name__ == '__main__':
    raise SystemExit(main())
