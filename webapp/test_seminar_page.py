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
    #  ★★ R19 Q1b — 거부 사유가 **확인할 자리**를 지목하는가.  산문만 주면 "이 배지가
    #    허구인가" 를 물을 곳이 없다.  아래 26~27 이 그 파일과 항목을 원자료에서 본다.
    chk('6b) ★★ 거부가 근거 파일을 지목한다 (evidence_ref)', bool(j.get('evidence_ref')))
    chk('6c) ★★ 근거 항목 번호도 준다 (evidence_claim)', bool(j.get('evidence_claim')))

    # ══ 1b) ★★ R19 P1-01 — **긍정 계약**.  거부만 검사하면 게이트를 켜 둔 채 덱이
    #     썩어도 초록이다.  `?historical=1` 은 여전히 온전한 덱을 줘야 한다.
    r = c.get('/api/seminar/slides?historical=1')
    jh = r.get_json() or {}
    slides = jh.get('slides') or []
    chk('18) ★ historical=1 은 덱을 준다 (ok=True)',
        r.status_code == 200 and jh.get('ok') is True)
    chk('19) ★ 이력으로 줄 때도 철회 표지를 단다',
        jh.get('retracted') is True and len(str(jh.get('retracted_banner') or '')) > 40)
    chk('20) ★ 슬라이드가 실제로 온다 (10장 이상)', len(slides) >= 10)
    chk('21) ★ n_slides 가 실제 장수와 맞는다', jh.get('n_slides') == len(slides))
    chk('22) ★ 모든 슬라이드가 스키마를 지킨다 (n·title·notes 자리)',
        all(isinstance(s, dict) and 'title' in s and 'notes' in s and 'n' in s
            for s in slides))
    chk('23) ★ 장 번호가 1..N 로 이어진다 (발표 순서 = 화면 순서)',
        [s.get('n') for s in slides] == list(range(1, len(slides) + 1)))
    chk('23b) ★ 대본이 실제로 실려 있다 (빈 껍데기 금지)',
        sum(1 for s in slides if s.get('notes')) >= 5)
    chk('23c) ★ 표나 차트가 하나 이상 살아 있다',
        any(s.get('tables') or s.get('charts') for s in slides))

    # ══ 1b-2) ★★ 화면이 설명하는 덱과 **내려받는 덱이 같은가** ══
    #  ⚠ 실사고 (2026-09-01 발견): `56dcbca1` 이 pptx 1번 장에 철회 배너를 끼웠는데
    #    `seminar_deck.json` 을 다시 안 뽑아, 화면은 **배너 없는 14장짜리 옛 덱**을 계속
    #    보여주고 pptx 만 15장이었다.  경로 비교(옛 검사 14·15)로는 못 잡는다 —
    #    두 산출물이 같은 파일을 **가리키면서** 내용이 갈라진 것이라서.
    _deck_fp = os.path.join(repo, webapp._SEMINAR_DECK.replace('/', os.sep))
    _n_pptx = None
    try:
        import zipfile
        with zipfile.ZipFile(_deck_fp) as _z:      # python-pptx 없이 장 수만 센다
            _n_pptx = sum(1 for n in _z.namelist()
                          if n.startswith('ppt/slides/slide') and n.endswith('.xml'))
    except Exception:                              # noqa: BLE001
        pass
    chk('17) ★★ JSON 의 장 수 = pptx 의 장 수 (표지 하나가 통째로 어긋나 있었다)',
        _n_pptx is not None and jh.get('n_slides') == _n_pptx)
    chk('17b) ★★ 철회 표지가 JSON 에도 살아 있다 (추출기를 다시 돌려도 안 사라진다)',
        len(str(jh.get('_RETRACTED') or '')) > 40)

    # ══ 1c) ★ 한계 공개가 **덱 안에** 실재하는가 — 배지가 허구면 안 된다 ══
    #  ⚠ 이 두 검사는 원래 있었는데 게이트가 붙어 슬라이드가 안 오자 내가 "문서 실재" 로
    #    **바꿔치기**했다 (R19 Q1b 지적).  데이터가 있는 자리에서 원래 계약을 복구한다.
    blob = json.dumps(slides, ensure_ascii=False)
    chk('24) ★ platen 결함 공개가 덱 안에 실재한다 (배지의 근거)',
        'kinematic-stop' in blob or 'platen' in blob.lower())
    chk('25) ★ 독립성 철회 문구가 덱 안에 실재한다',
        'not an independent' in blob or 'one-way' in blob)

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

    # ══ 5) ★★ R19 P1-01 — pptx 창구.  여기는 **검사가 아예 없었다** ══
    #  ⚠ 그 사이 `sed -i '…/    if False:/' webapp/app.py` 한 줄이면 표지 없는 철회
    #    pptx 가 기본 경로로 나가는데도 이 파일은 초록이었다.  두 방향을 다 고정한다.
    r = c.get('/api/seminar/deck')
    chk('26) ★★ 기본 경로는 pptx 를 주지 않는다 (fail-closed)', r.status_code == 403)
    jd = r.get_json() or {}
    chk('27) ★★ 거부가 기계가 읽을 형태다 (평문 403 이면 화면이 그 주소로 이동해 버린다)',
        (r.headers.get('Content-Type') or '').startswith('application/json'))
    chk('28) ★★ 거부가 철회임을 말한다',
        jd.get('retracted') is True and '철회' in str(jd.get('error') or ''))
    chk('29) ★★ 거부가 근거와 다음 행동을 준다',
        bool(jd.get('evidence_ref')) and bool(jd.get('hint')))
    chk('30) ★★ 거부 본문에 pptx 바이트가 섞여 나가지 않는다',
        b'PK\x03\x04' not in r.data)

    r = c.get('/api/seminar/deck?historical=1')
    chk('31) ★★ historical=1 은 실제로 내려받게 해 준다 (200)', r.status_code == 200)
    chk('32) ★★ 그것이 진짜 pptx 다 (zip 매직)', r.data[:4] == b'PK\x03\x04')
    chk('33) ★★ 첨부로 내려간다 (브라우저가 렌더하지 않게)',
        'attachment' in (r.headers.get('Content-Disposition') or ''))

    # ══ 6) 철회 근거가 리포에 실재하는가 — **응답이 지목한 그 파일**을 본다 ══
    #  ⚠ 파일명 접미어만 보던 옛 검사(15)와 다르다.  응답이 가리키는 경로를 열고,
    #    그 항목 번호가 등록부에 실제로 있는지 **원자료에서** 확인한다.
    ev = j.get('evidence_ref') or ''
    ev_path = os.path.join(repo, ev.replace('/', os.sep))
    chk('34) ★★ 응답이 지목한 근거 파일이 실재한다', bool(ev) and os.path.exists(ev_path))
    _ev = open(ev_path, encoding='utf-8', errors='replace').read() if os.path.exists(ev_path) else ''
    chk('35) ★★ 그 등록부에 이 항목이 실제로 등재돼 있다',
        str(j.get('evidence_claim') or '\0') in _ev)
    chk('36) ★★ 두 창구가 같은 근거를 가리킨다 (슬라이드 ↔ pptx)',
        jd.get('evidence_ref') == j.get('evidence_ref'))

    print(f'\ntest_seminar_page: {_ok}/{_ok + len(_fail)} PASS'
          + (f'   FAILED: {_fail}' if _fail else ''))
    return 0 if not _fail else 1


if __name__ == '__main__':
    raise SystemExit(main())
