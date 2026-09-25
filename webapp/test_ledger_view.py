#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v3 원장 렌더 회귀 — **화면이 원장을 따라가는가**, 그리고 **금지값이 안 새는가**.

계기 (2026-09-09 전수 감사, 원장 CL-89):
  · 웹앱 8 영역 전부에서 기계는 최신인데 라벨이 3~15 개월 뒤였다.  원인은 상태 문장이
    전부 손으로 적힌 산문이고 `webapp/` 이 `claims.json` 을 **읽은 적이 없다**는 것.
  · 그 산문이 실제로 틀렸다 — 철회 배너 둘이 **같은 문장에서 다른 금지 세트**를 현행
    결론으로 적고 있었다 (`app.py:4035` · `seminar_deck.json`).

⇒ v3 는 상태를 원장에서 렌더한다.  이 회귀가 고정하는 계약 셋:
  ① 렌더된 HTML 에 **인용 금지 패턴이 하나도 없다** — 이 페이지가 곧 누수가 되는 것이
     가장 그럴듯한 실패 양식이다 (금지 등록부를 보여 주는 페이지이므로).
  ② 원장이 없으면 **상태를 주장하지 않는다** (있는 척하지 않는다).
  ③ 신선도 비교가 실제로 뒤처짐을 잡는다 — 감사를 기다리지 않고 화면이 스스로 말한다.

  python3 webapp/test_ledger_view.py
"""
import html as _html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('WEBAPP_DISABLE_AUTH', '1')

_ok, _fail = 0, []


def chk(name, cond):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}')


#: 화면에 **안 나오는** 것 — 여기 든 표지는 면제 근거가 될 수 없다.
_RE_HIDDEN = re.compile(r'<(script|style)\b[^>]*>.*?</\1\s*>', re.S | re.I)
_RE_COMMENT = re.compile(r'<!--.*?-->', re.S)
#: **덩어리(카드)** 경계 — 블록 요소만.  `span`·`a`·`b`·`code` 같은 인라인은 자르지
#:   않는다 (자르면 한 문장 안의 표지를 놓쳐 거짓 검출이 난다).
_RE_BLOCK = re.compile(r'</?(?:p|div|li|tr|td|th|h[1-6]|section|article|header|footer|'
                       r'ul|ol|table|thead|tbody|blockquote|pre|main|nav|aside|form|'
                       r'figure|figcaption|details|summary|dl|dt|dd|option|hr)\b[^>]*>',
                       re.I)
_RE_TAG = re.compile(r'<[^>]+>')


def _visible_blocks(page_html):
    """독자가 **실제로 보는** 덩어리들.

    ⚠⚠ 2026-09-09 (Codex Q3-2 · 원장 AUD-05) — 떼는 것이 요점이다.  `<script>`·
    `<style>`·**HTML 주석**은 화면에 안 나오므로 그 안의 철회 표지는 면제 근거가 아니다.
    """
    #  ⚠ 소스의 줄바꿈은 **덩어리 경계가 아니다** — 한 문장이 여러 줄에 걸쳐 적히면
    #    표지와 값이 갈라져 거짓 검출이 난다 (실측: `/eis` 의 철회 안내 한 문장).
    #    ⇒ 블록 경계만 sentinel 로 찍고, 원래 줄바꿈은 공백으로 눕힌다.
    t = _RE_HIDDEN.sub(' ', page_html)
    t = _RE_COMMENT.sub(' ', t)
    t = _RE_BLOCK.sub('\x00', t)
    t = _RE_TAG.sub(' ', t)
    t = _html.unescape(t)
    return [re.sub(r'\s+', ' ', b).strip() for b in t.split('\x00') if b.strip()]


def _unmarked_bans(CRF, bans, page_html, where):
    """화면에 **표지 없이** 사는 금지값.

    ⚠⚠ 옛 판은 **원본 HTML 을 줄 단위로** 보고 ±2 줄 안의 표지를 인정했다.  구멍 둘:
      ⓐ `<!-- 철회 -->` 는 화면에 안 나오는데 면제가 됐다 (주석·스크립트도 마찬가지),
      ⓑ **다른 카드**의 표지가 "이웃 줄" 이라는 이유로 면제 근거가 됐다.
    ⇒ 보이는 덩어리로 자르고, 표지는 **같은 덩어리 안**에 있어야 한다.  소스 스윕의
      "같은 출력 문장" 규칙(`check_review_findings` AUD-05)과 같은 취지다.
    """
    out = []
    for j, blk in enumerate(_visible_blocks(page_html)):
        norm = CRF._ban_norm(blk)
        for b in bans:
            pat = b.get('pattern')
            if not pat or CRF._ban_norm(pat) not in norm:
                continue
            if any(m in blk for m in CRF.BAN_NEAR_MARKS):
                continue
            out.append(f'{where}#블록{j + 1} {pat!r}')
    return out


def main():
    import ledger_view as LV

    # ── 모듈 계약 ─────────────────────────────────────────────
    chk('1) 원장을 읽는다', LV.available())
    n = LV.counts()
    chk('2) 상태 집계가 총계와 맞는다',
        sum(v for k, v in n.items() if k != 'total') == n['total'])

    live = LV.claims('live')
    chk('3) 상태 필터가 실제로 거른다',
        live and all(c.get('status') == 'live' for c in live))

    #  ★ 최신 먼저 — v3 의 전제("가장 최근·가장 중요한 것이 앞에")를 코드로 고정한다.
    order = [(c.get('date') or '', LV._num(c.get('id'))) for c in LV.claims()]
    chk('4) ★ 최신이 먼저다 (날짜 → id 번호 내림차순)', order == sorted(order, reverse=True))

    chk('5) 모르는 id 는 지어내지 않고 미등재라고 말한다',
        LV.chip('CL-99999')['known'] is False)
    known = LV.chip(LV.claims(limit=1)[0]['id'])
    chk('6) 아는 id 는 상태·날짜를 돌려준다', known['known'] and known['date'])

    #  ── 신선도 ────────────────────────────────────────────────
    newest = LV.newest_date()
    stale = LV.freshness('2020-01-01', ledger_ids=[LV.claims(limit=1)[0]['id']])
    chk('7) ★ 뒤처진 페이지를 뒤처졌다고 말한다', stale['stale'] and stale['behind'])
    fresh = LV.freshness('2999-01-01', ledger_ids=[LV.claims(limit=1)[0]['id']])
    chk('8) 앞선 페이지는 경고하지 않는다', not fresh['stale'])
    #  ⛔ **정정 2026-09-14 (감사 D-2)** — 기준선이 `newest_date()`(클레임 전용) 였고,
    #    그래서 `/single` 이 초록을 띄우는 동안 그 화면을 만드는 코드에 09-13 자 결함이
    #    6건(P1 4건) 열려 있었다.  기준선은 **클레임 ∪ 결함**이다.
    chk('9) 기준선이 클레임과 결함 **둘 다**의 최신 등재다',
        stale['newest'] == LV.newest_ledger_date()
        and LV.newest_ledger_date() >= newest)
    #  ★ 판별력 — 결함 축이 실제로 기준선을 움직이는가 (안 움직이면 이 검사는 공허하다).
    #  ⛔ 정정 2026-09-25 — 옛 판은 **실데이터**가 "결함이 클레임보다 최신" 이기를 요구했다.
    #    같은 날 클레임과 결함이 함께 등재되면 (CL-90 · SELF-51, 둘 다 09-25) 구현이 옳아도
    #    빨간불이 난다 = 판별력을 데이터의 우연에 맡긴 것.  ⇒ 클레임보다 하루 늦은 결함 **픽스처**를
    #    캐시에 잠깐 넣어 기준선이 그 날짜로 움직이는지 본다 (원장 파일은 건드리지 않는다).
    import datetime as _dt
    _d0 = LV._load()
    _base = _dt.date.fromisoformat(newest) if newest else _dt.date(2000, 1, 1)
    _next = _base + _dt.timedelta(days=1)
    _fake = {'id': 'TEST-9A', 'status': 'open',
             'opened_in': f"docs/reviews/_fixture_{_next.strftime('%Y%m%d')}.md"}
    _saved = LV._cache['data']
    try:
        LV._cache['data'] = dict(_d0, findings=list(_d0['findings']) + [_fake])
        _moved = LV.newest_ledger_date() == _next.isoformat()
    finally:
        LV._cache['data'] = _saved
    chk('9a) ★ 결함 축이 기준선을 실제로 움직인다 (클레임보다 하루 늦은 결함 픽스처 → 기준선이 그 날짜)',
        LV.newest_finding_date() is not None and _moved
        and LV.newest_ledger_date() == max(newest, LV.newest_finding_date()))
    #  ★★ 이 검사가 이번 감사의 본체다 — **날짜가 최신이어도** 선언된 결함이 열려 있으면
    #    초록이 나오면 안 된다.  옛 판은 여기서 초록이었다.
    _f_open = LV.freshness('2999-01-01', ledger_ids=[],
                           finding_ids=[_o['id'] for _o in LV.open_findings(limit=1)])
    chk('9c) ★★ 날짜가 앞서도 열린 결함이 선언돼 있으면 초록이 아니다',
        _f_open['stale'] is True and _f_open['open_findings'])
    chk('9d) ★ 없는 결함 id 는 초록이 아니라 unknown 이다',
        LV.freshness('2026-09-09', finding_ids=['ZZ-99999']).get('unknown') is True)
    #  ⚠ 2026-09-09 (Codex Q3-1) — 옛 판은 **없는 의존 ID** 를 조용히 통과시켰다
    #    (오타·삭제된 클레임이 영원히 초록).  이제 `unknown` 이어야 한다.
    ghost = LV.freshness('2026-09-09', ledger_ids=['CL-99999'])
    chk('9b) ★ 없는 의존 클레임은 초록이 아니라 unknown 이다',
        ghost.get('unknown') is True and ghost.get('stale') is None)

    #  ── 금지 등록부 ───────────────────────────────────────────
    bans = LV.banned()
    chk('10) 등록부가 비어 있지 않다 (비면 이 규칙이 조용히 사라진다)', len(bans) > 0)
    summ = LV.banned_summary()
    chk('11) ★ 요약은 개수와 클레임 id 만 준다 — 값을 안 싣는다',
        all(set(r) == {'claim', 'n', 'why'} for r in summ))
    #  요약 안에 금지 문자열이 섞여 들어오지 않았는가 (why 는 원장 산문이라 값이 있을 수 있다 →
    #  그래서 화면은 why 를 **잘라서** 쓰고, 아래 ⑬ 이 최종 방어선이다).
    chk('12) 요약의 claim 필드가 클레임 id 형태다',
        all(str(r['claim']).startswith('CL-') or r['claim'] == '?' for r in summ))

    #  ── 렌더된 화면 ───────────────────────────────────────────
    import app as A
    c = A.app.test_client()
    r_led = c.get('/ledger')
    r_home = c.get('/')
    chk('13) /ledger 가 뜬다', r_led.status_code == 200)
    chk('14) / 가 뜬다', r_home.status_code == 200)

    html_led = r_led.data.decode('utf-8', 'replace')
    html_home = r_home.data.decode('utf-8', 'replace')

    #  ★★ 가장 중요한 검사 — 금지값을 보여 주는 페이지가 금지값을 **찍지 않는가.**
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    '..', 'scripts'))
    import check_review_findings as CRF
    leaked = []
    for page, html in (('/ledger', html_led), ('/', html_home)):
        norm = CRF._ban_norm(html)
        for b in bans:
            pat = b.get('pattern')
            if pat and CRF._ban_norm(pat) in norm:
                leaked.append(f'{page}: {pat!r} ({b.get("claim")})')
    chk('15) ★★ 렌더된 HTML 에 인용 금지 패턴이 하나도 없다'
        + (f'  ← 누수 {leaked}' if leaked else ''), not leaked)

    #  앞문이 실제로 세 가지를 말하는가 (감사가 없다고 지적한 바로 그것들)
    chk('16) 앞문이 "이게 뭔가" 를 말한다', '양극 복합체' in html_home)
    chk('17) ★ 앞문이 파이프라인이 둘이라고 말한다',
        'CONTACT_FREE' in html_home and 'run_mpm.sh' in html_home)
    chk('18) 앞문이 원장으로 가는 길을 준다', '/ledger' in html_home)
    chk('19) 항해에 원장이 있다', '판정 원장' in html_home)

    #  원장 페이지가 실제로 클레임을 싣는가 (빈 표를 초록으로 내면 최악)
    newest_id = LV.claims(limit=1)[0]['id']
    chk('20) /ledger 가 최신 클레임을 싣는다', newest_id in html_led)
    chk('21) /ledger 가 열린 결함을 싣는다', 'findings' in html_led)

    #  ── 신선도 배선이 실제로 화면에 닿는가 ────────────────────
    #    선언만 해 두고 템플릿이 안 부르면 아무 일도 안 일어난다 (규칙 K: 안 도는 검사).
    #  ⚠⚠ 2026-09-09 (Codex Q3-2 부수 · 원장 AUD-05) — 옛 판은 페이지 **다섯 개를
    #    손으로 적고** `set(pages) <= set(PAGE_FRESHNESS)` 를 봤다.  그 방향으로는
    #    *"선언한 모든 페이지"* 를 증명할 수 없다 — 실제로 `single` 이 빠져 있었고,
    #    새 페이지를 선언해도 이 시험은 아무 말을 안 한다.  ⇒ **선언에서 파생**한다.
    #    URL 이 None 인 페이지는 실물 데이터가 있어야 열리므로 여기서 해석해 채운다.
    _urls = {'single': None, 'group': '/group', 'predictor': '/predictor',
             'eis': '/eis', 'mpm_lab': '/mpm-lab', 'step5': '/step5'}
    _cases = []
    try:
        _cases = [c for c in A.list_cases() if c.get('id')]
    except Exception:                                          # noqa: BLE001
        _cases = []
    if _cases:
        _urls['single'] = '/single/' + str(_cases[0]['id'])
    _undeclared = sorted(set(A.PAGE_FRESHNESS) - set(_urls))
    chk('26) ★ 선언한 **모든** 페이지가 이 시험의 등록부에 있다 '
        '(부분집합으로는 "선언한 전부" 를 증명할 수 없다)'
        + (f'  ← 빠진 것 {_undeclared}' if _undeclared else ''),
        not _undeclared)
    pages = {k: u for k, u in _urls.items() if u and k in A.PAGE_FRESHNESS}
    _dataless = sorted(k for k, u in _urls.items() if not u and k in A.PAGE_FRESHNESS)
    if _dataless:
        #  통과로 세지 않는다 — 못 연 페이지를 초록으로 적는 것이 false-green 이다.
        print(f'  SKIP  26b) 실물 케이스가 있어야 열리는 페이지 {_dataless} — '
              '이 트리에 분석된 케이스가 없어 27·28 이 그 페이지를 못 봤다')
    bars, leaks2 = [], []
    for key, url in pages.items():
        r = c.get(url)
        html = r.data.decode('utf-8', 'replace')
        bars.append((key, r.status_code == 200 and
                     ('마지막 갱신은' in html or '검토됐다' in html)))
        leaks2 += _unmarked_bans(CRF, bans, html, url)
    chk('27) ★ 선언한 모든 페이지가 신선도 줄을 실제로 렌더한다'
        + (f'  ← {[k for k, v in bars if not v]}' if not all(v for _, v in bars) else ''),
        all(v for _, v in bars))
    #  ⚠ 여기는 15) 보다 **느슨하다** — 그리고 그것이 맞다.  리포의 규칙은 "표지 없이"
    #    금지값이 사는 것을 막는 것이지, *철회를 알리는 문장*까지 막는 것이 아니다.
    #    실제로 `/eis` 는 *"옛 문구의 +52% 는 … 철회 — claims.json CL-24"* 라고 적는데,
    #    그 문장을 지우면 독자가 옛 발표자료와 대조할 근거를 잃는다.
    #    ⇒ 스윕과 **같은 기준**(±2 줄 철회 표지)을 렌더된 화면에 적용한다.
    #    15) 만 엄격한 이유: 그 두 페이지는 **원장 산문을 통째로** 렌더하므로
    #    `redact()` 를 지나야 하고, 지나면 남을 이유가 없다.
    chk('28) ★★ 그 페이지들에 **표지 없는** 금지값이 없다 (스윕과 같은 기준)'
        + (f'  ← {leaks2}' if leaks2 else ''), not leaks2)

    #  ── 28f~28i ★★ 2026-09-14 (webapp 감사 A-1/A-2 · D-3) ────────────────────
    #    ⚠ 27·28 은 `pages` 를 `PAGE_FRESHNESS` 키로 좁혀서, 리포에서 **철회 자료를 가장
    #    많이 서빙하는 두 창구**(`/api/seminar/*`)를 한 번도 안 봤다.  실측: 같은 세미나의
    #    산출물 셋 중 `slides`·`deck` 만 `?historical=1` fail-closed 였고 **`doc/<key>` 는
    #    게이트가 없어** 75 KB 원문이 등록부 값을 담은 채 그대로 나갔다.
    #    파일 머리의 철회 배너가 `_has_banner` 로 **파일 전체를 스윕에서 면제**시켜
    #    `--ban-sweep` 은 그동안 초록이었다 — 배너가 파일을 면제해도 **창구는 면제되지 않는다**.
    def _api_bans(url):
        t = c.get(url).data.decode('utf-8', 'replace')
        return sorted({b['claim'] for b in bans
                       if b['pattern'] in t or CRF._ban_norm(b['pattern'])
                       in CRF._ban_norm(t)})
    _doc = _api_bans('/api/seminar/doc/script')
    chk('28f) ★★ 세미나 문서 창구가 게이트 없이 금지값을 내주지 않는다'
        + (f'  ← {_doc}' if _doc else ''), not _doc)
    #  ★ 판별력 — 게이트를 **명시적으로 풀면** 원문이 나와야 한다.  안 나오면 이 검사는
    #    "그 문서에 원래 금지값이 없다" 를 확인한 것일 뿐 공허하다.
    chk('28g) ★ 그러나 `?historical=1` 로는 원문이 나온다 (검사가 공허하지 않다)',
        bool(_api_bans('/api/seminar/doc/script?historical=1')))
    #  ★ 과잉차단 음성 대조 — 금지값이 없는 문서는 게이트에 안 걸려야 한다.
    import json as _J
    chk('28h) ★ 금지값이 없는 문서는 막지 않는다 (과잉차단 음성 대조)',
        _J.loads(c.get('/api/seminar/doc/glossary').data.decode('utf-8')).get('ok') is True)
    #  ★ 게이트가 **경로 목록이 아니라 내용**에 걸려 있는가 — 새 문서를 얹어도 자동으로
    #    걸려야 한다 (규율 ⑤: 후보를 고르는 코드가 곧 사각지대다).
    import inspect as _insp
    _src = _insp.getsource(A.api_seminar_doc)
    chk('28i) ★★ 그 게이트가 내용 기반이다 (경로 목록이면 새 문서가 샌다)',
        'redact(' in _src and 'historical' in _src)

    #  ── 28 의 기준 자체가 옳은가 — 음성 대조 넷 (AUD-05) ──────────
    #    통과만 하는 검사는 없는 것과 같다.  아래 넷은 **합성 HTML** 이라 서버가 필요 없다.
    _p0 = bans[0]['pattern']
    _syn = [
        ('28a) ★★ HTML 주석의 표지는 면제가 아니다 (화면에 안 나온다)',
         f'<div class="card"><!-- 철회 --><p>비 {_p0} 달성</p></div>', True),
        ('28b) ★★ **다른 카드**의 표지는 면제가 아니다 (옛 ±2 줄 규칙은 통과시켰다)',
         f'<div class="card"><p>이 값은 철회됐다</p></div>'
         f'<div class="card"><p>비 {_p0} 달성</p></div>', True),
        ('28c) 같은 카드 안의 표지는 면제한다 (철회를 알리는 문장까지 막지 않는다)',
         f'<div class="card"><p>옛 문구의 {_p0} 는 <b>철회</b> — claims.json</p></div>', False),
        ('28d) `<script>` 안의 표지도 면제가 아니다 (독자가 못 본다)',
         f'<script>/* 철회 */</script><div class="card"><p>비 {_p0}</p></div>', True),
    ]
    for _name, _html_frag, _want_leak in _syn:
        _got = _unmarked_bans(CRF, bans, _html_frag, 'synthetic')
        chk(_name + ('' if bool(_got) == _want_leak else f'  ← {_got}'),
            bool(_got) == _want_leak)
    #    한 문장이 소스에서 여러 줄에 걸쳐도 한 덩어리다 (실측 거짓 검출 자리).
    chk('28e) 소스 줄바꿈은 덩어리를 가르지 않는다 (거짓 검출 방지)',
        not _unmarked_bans(CRF, bans,
                           f'<div class="card"><p>옛 문구의 {_p0} 는\n    <b>철회</b>\n'
                           f'    — claims.json</p></div>', 'synthetic'))

    #  선언 날짜가 미래면 경고가 영원히 안 뜬다 = 조용한 거짓 초록.
    import datetime as _dt
    today = _dt.date.today().isoformat()
    future = [k for k, v in A.PAGE_FRESHNESS.items() if (v.get('updated') or '') > today]
    chk('29) ★ 신선도 선언에 미래 날짜가 없다 (미래로 적으면 경고가 영원히 안 뜬다)'
        + (f'  ← {future}' if future else ''), not future)

    #  ── 원장이 없을 때 ────────────────────────────────────────
    saved_claims, saved_findings = LV.CLAIMS_PATH, LV.FINDINGS_PATH
    try:
        LV.CLAIMS_PATH = '/nonexistent/claims.json'
        LV.FINDINGS_PATH = '/nonexistent/findings.json'
        LV._cache['stamp'] = None
        chk('22) ★ 원장이 없으면 available()=False (있는 척하지 않는다)',
            LV.available() is False)
        chk('23) 없어도 안 죽는다', LV.context()['counts']['total'] == 0)
        r = c.get('/ledger')
        chk('24) ★ 원장 없이도 페이지가 뜨고 "주장하지 않는다" 고 적는다',
            r.status_code == 200 and '주장하지 않는다' in r.data.decode('utf-8', 'replace'))

        #  ⚠⚠ 2026-09-09 (Codex Q3-3) — 옛 22-24 는 `/ledger` 만 봤고 그 페이지에는
        #    freshness bar 가 없어서 29/29 초록이 유지됐다.  실제로는 **선언한 페이지들이
        #    "판정 상태를 주장하지 않는다" 와 초록 "✓ … 검토됐다" 를 동시에** 렌더했다.
        #    ⇒ 원장 부재를 **초록으로 칠하지 않는지** 를 선언 페이지에서 직접 본다.
        green, unknown = [], []
        for key, url in pages.items():
            h = c.get(url).data.decode('utf-8', 'replace')
            if '검토됐다' in h:
                green.append(key)
            if '판정할 수 없다' in h:
                unknown.append(key)
        chk(f'24b) ★★ 원장이 없으면 어느 페이지도 초록 "검토됐다" 를 안 띄운다 ({green})',
            not green)
        chk(f'24c) ★ 대신 "판정할 수 없다" 를 띄운다 ({len(unknown)}/{len(pages)})',
            len(unknown) == len(pages))
    finally:
        LV.CLAIMS_PATH, LV.FINDINGS_PATH = saved_claims, saved_findings
        LV._cache['stamp'] = None

    #  ⚠ 결함 원장만 못 읽는 경우 — `[]` 와 구별되는가 (Codex Q3-3 두 번째).
    try:
        LV.FINDINGS_PATH = '/nonexistent/findings.json'
        LV._cache['stamp'] = None
        chk('24d) ★ 결함 원장 읽기 실패를 "열린 결함 없음" 으로 위장하지 않는다',
            LV.available() and LV.findings_error() is not None)
    finally:
        LV.CLAIMS_PATH, LV.FINDINGS_PATH = saved_claims, saved_findings
        LV._cache['stamp'] = None
    chk('25) 복구 후 다시 읽는다 (캐시가 실패를 붙들지 않는다)', LV.available())

    # ── 비포/애프터 라우트 (2026-09-15, `L2-01` 작업에서 붙였다) ────────────────
    #   ★ 핵심 계약은 *"커밋된 사본을 서빙하지 않는다"* 다.  원장이 움직인 뒤 낡은 페이지를
    #     조용히 띄우는 것이 이 리포가 반복해 맞은 부류(규율 ④)이므로, 그 성질을 시험한다.
    import importlib.util as _ilu
    import pathlib as _pl
    _rba_path = _pl.Path(__file__).resolve().parent.parent / 'scripts' / 'build_review_before_after.py'
    _spec = _ilu.spec_from_file_location('_rba_t', _rba_path)
    _rba = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_rba)
    import app as _APP
    _cli = _APP.app.test_client()
    _r = _cli.get('/ledger/before-after')
    chk(f'46) 비포/애프터 라우트가 200 을 낸다 (실제 {_r.status_code})', _r.status_code == 200)
    _body = _r.data.decode('utf-8')
    chk('46b) 그 본문이 생성기의 현재 렌더와 **정확히 같다** (요청 시 재렌더)',
        _body == _rba.render(nav_home='/ledger'))
    #   ★ 독립 HTML 이라 항해가 없다 — 돌아가는 길이 실제로 있는가 (없으면 갇힌다).
    chk('46f) ★ 앱이 띄우는 판에는 원장으로 돌아가는 링크가 있다',
        'href="/ledger"' in _body)
    #   ⛔ 커밋되는 docs 사본에는 그 링크를 달지 않는다 (파일로 열면 죽은 링크다).
    chk('46g) 커밋 사본에는 그 링크가 없다 (판별력: 두 판이 실제로 다르다)',
        'href="/ledger"' not in _rba.render() and _rba.render() != _body)
    #   ★ 판별력 — 커밋된 파일에 표시를 넣고 응답에 그것이 **없어야** 한다.
    _out = _rba.OUT
    _saved = _out.read_text(encoding='utf-8') if _out.is_file() else None
    try:
        _out.write_text('<!-- STALE-COPY-MARKER -->' + (_saved or ''), encoding='utf-8')
        _b2 = _cli.get('/ledger/before-after').data.decode('utf-8')
        chk('46c) ★ 판별력: 커밋된 사본에 표시를 넣어도 응답에 안 나온다 (파일을 안 읽는다)',
            'STALE-COPY-MARKER' not in _b2)
    finally:
        if _saved is not None:
            _out.write_text(_saved, encoding='utf-8')
    #   ★ 원장에 닻을 내렸는지 — 새로 쓴 서술의 인용이 페이지에 실재하는가.
    chk('46d) L2-01 의 재현 수치가 페이지에 실린다',
        '150.90474195844345' in _body and '99.436 %' in _body)
    #   ⚠ 이 페이지도 스윕 범위다 — 금지값이 새면 여기서 새는 것이다.
    _ba_leak = _unmarked_bans(CRF, bans, _body, '/ledger/before-after')
    chk('46e) ★★ 비포/애프터 본문에 표지 없는 금지값이 없다'
        + (f'  ← 누수 {_ba_leak}' if _ba_leak else ''), not _ba_leak)

    print(f'\nledger_view: {_ok}/{_ok + len(_fail)} PASS')
    if _fail:
        for f in _fail:
            print(f'  ✗ {f}')
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
