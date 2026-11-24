#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""믹서 문제 · 공백 (/mixer/story) 회귀 — 1저자 11-24 (믹서 원고의 문제 · 공백 · 새로움 문서를 웹앱에서 · 읽기 전용).

  python3 webapp/test_mixer_story_page.py

정본 = docs/reviews/mixer_problem_gap_novelty_20261124.md — 화면은 **그 파일을 읽어** 보인다 (템플릿 · 코드에 문장 · 숫자를
베끼지 않는다 · 정본을 고치면 화면이 같이 바뀐다 · 규율 ④).  /emod 와 같은 관문: 갱신 표지 (MIXSTORY:UPDATED) 가 정확히 하나 ·
빈 본문 거부 · markdown 변환 **전에** ledger_view.redact · 읽지 못하면 무엇이 깨졌는지 적고 옛 문장을 보이지 않는다 (fail-closed).
증거 표 = docs/reviews/mixer_b2_flow_20261124/b1_b2_u_contacts.json (지표 이름 · 값 = 자료 그대로 · 개발 자료 · 한 시드 · 판정 아님 ·
Codex 판독 그대로) · 자료가 없거나 깨져도 200 + 안내 · 정본은 그대로.  그림 둘 = 등록부 (MIXSTORY_FIGS) 만 · 등록부 밖 이름
(경로 꼴 포함) = 404 · 밑글 = 같은 폴더 frame_caption.md (있으면 · redact → markdown).
⚠ 정본은 v1 → v2 로 고쳐지는 중이다 — 이 시험은 문구에 기대지 않는다 (갱신 표지 · '## 2.' 제목 줄 · '## ' 절 수만 정본에서 읽는다).
⚠ 금지값 (claims.json quotation_ban) 을 이 파일에 적지 않는다 — redact 실물 검사는 등록부에서 실행 중에 읽는다.
"""
import json
import math
import os
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
_ok, _fail = 0, []

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DOC = ROOT / 'docs' / 'reviews' / 'mixer_problem_gap_novelty_20261124.md'
DATA = 'docs/reviews/mixer_b2_flow_20261124'
EVJ = ROOT / DATA / 'b1_b2_u_contacts.json'
CAP = ROOT / DATA / 'frame_caption.md'
TPL = HERE / 'templates' / 'mixer_story.html'
FIGS = ('b2_u_cross_section.png', 'b2_u_second_turn.png')
MARK = re.compile(r'<!-- MIXSTORY:UPDATED (\d{4}-\d{2}-\d{2}) -->')
LABEL = '개발 자료 · 한 시드 · 판정 아님 (Codex 판독 그대로)'
#: 등록부 밖 이름 · 경로 꼴 — 전부 404 여야 한다 (같은 폴더의 다른 파일 · 대소문자 · 확장자 없음 · 인코딩한 '..' · 구분자)
BAD_FIG_URLS = (
    '/mixer/story/fig/nope.png',
    '/mixer/story/fig/frame_caption.md',
    '/mixer/story/fig/b1_b2_u_contacts.json',
    '/mixer/story/fig/README.md',
    '/mixer/story/fig/B2_U_CROSS_SECTION.PNG',
    '/mixer/story/fig/b2_u_cross_section',
    '/mixer/story/fig/..',
    '/mixer/story/fig/',
    '/mixer/story/fig/../../app.py',
    '/mixer/story/fig/..%2f..%2f..%2fwebapp%2fapp.py',
    '/mixer/story/fig/%2e%2e%2f%2e%2e%2f%2e%2e%2fCLAUDE.md',
    '/mixer/story/fig/b2_u_cross_section.png%2f..%2fREADME.md',
    '/mixer/story/fig/%2fetc%2fpasswd',
)
#: 탈출이 성공했다면 보일 글 (app.py 의 Flask 객체 줄 · README 첫 줄 머리)
LEAK_MARKS = ('app = Flask(', '# B2-U', 'root:x:0:0')


def chk(name, cond):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}')


def _esc(s):
    """Jinja 자동 이스케이프와 같은 꼴 (& < > " ')."""
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            .replace('"', '&#34;').replace("'", '&#39;'))


def _num_txt(v):
    """화면이 숫자 칸에 쓰는 꼴 — 실수 = 유효 숫자 4 자리 (%.4g) · 정수 = 그대로.  숫자가 아니면 None."""
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return None
    if isinstance(v, float) and not math.isfinite(v):
        return None
    return str(v) if isinstance(v, int) else '%.4g' % v


def _ev_columns(mx):
    """자료의 metrics → (arms, stats, extras) — 첫 출현 순서 (화면 열 순서와 같아야 한다)."""
    arms, stats, extras = [], [], []
    for m in mx.values():
        if not isinstance(m, dict):
            continue
        for k, v in m.items():
            if isinstance(v, dict):
                if k not in arms:
                    arms.append(k)
                for s in v:
                    if s not in stats:
                        stats.append(s)
            elif k not in extras:
                extras.append(k)
    return arms, stats, extras


def _ev_rows_html(html):
    """증거 표의 행 → [(지표 키, [(열 키, 글, title)])] (화면 순서)."""
    out = []
    for p in html.split('<tr class="ms-ev-row"')[1:]:
        seg = p.split('</tr>')[0]
        m = re.search(r'data-metric="([^"]*)"', seg)
        cells = re.findall(r'<td data-col="([^"]*)"(?: title="([^"]*)")?[^>]*>([^<]*)</td>', seg)
        out.append((m.group(1) if m else None, [(c, t.strip(), ti) for c, ti, t in cells]))
    return out


def _doc_region(html):
    """화면에서 정본 본문 자리만 (`<!--MSDOC-->` … `<!--/MSDOC-->`) — 없으면 ''."""
    m = re.search(r'<!--MSDOC-->(.*?)<!--/MSDOC-->', html, re.S)
    return m.group(1) if m else ''


def _numbers(o):
    """자료 안 숫자 전부 (bool 제외 · 재귀)."""
    if isinstance(o, bool):
        return []
    if isinstance(o, (int, float)):
        return [o]
    if isinstance(o, dict):
        return [x for v in o.values() for x in _numbers(v)]
    if isinstance(o, list):
        return [x for v in o for x in _numbers(v)]
    return []


def _strings(o):
    """자료 안 문자열 값 전부 (키 제외 · 재귀)."""
    if isinstance(o, str):
        return [o]
    if isinstance(o, dict):
        return [x for v in o.values() for x in _strings(v)]
    if isinstance(o, list):
        return [x for v in o for x in _strings(v)]
    return []


def main():
    import app as webapp
    import ledger_view
    c = webapp.app.test_client()
    src = DOC.read_text(encoding='utf-8') if DOC.is_file() else ''
    marks = MARK.findall(src)
    h2_lines = [ln for ln in src.splitlines() if ln.startswith('## ')]
    ev_json = json.loads(EVJ.read_text(encoding='utf-8')) if EVJ.is_file() else {}
    mx = ev_json.get('metrics') if isinstance(ev_json.get('metrics'), dict) else {}
    arms, stats, extras = _ev_columns(mx)
    doc_fn = getattr(webapp, '_mixstory_doc', None)
    ev_fn = getattr(webapp, '_mixstory_evidence', None)
    tpl = TPL.read_text(encoding='utf-8') if TPL.is_file() else ''

    # ═══ A. 실물 화면 — 정본을 읽어 보인다 ═══
    r = c.get('/mixer/story')
    html = r.get_data(as_text=True)
    chk('① GET /mixer/story = 200 · 제목 "믹서 — 문제 · 공백"', r.status_code == 200 and '믹서 — 문제 · 공백' in html)
    chk(f'② 정본 전제 — 갱신 표지 하나 ({marks}) · "## 2." 로 시작하는 제목 줄 있음 · "## " 절 {len(h2_lines)} 개',
        len(marks) == 1 and any(ln.startswith('## 2.') for ln in h2_lines))
    d = doc_fn() if doc_fn else {}
    dh = d.get('html') or ''
    chk('③ 읽기 함수 (_mixstory_doc) — ok · 갱신 날짜 = 정본 표지 · 키 다섯 (ok · html · updated · error · redacted)',
        d.get('ok') is True and bool(marks) and d.get('updated') == marks[0]
        and set(d) == {'ok', 'html', 'updated', 'error', 'redacted'})
    chk('④ 렌더된 정본 — <h2> 수 = 정본의 "## " 줄 수 · "2." 로 시작하는 <h2> 가 있다',
        bool(h2_lines) and len(re.findall(r'<h2[\s>]', dh)) == len(h2_lines) and re.search(r'<h2[^>]*>\s*2\.', dh) is not None)
    region = _doc_region(html)
    chk('⑤ 화면 = 렌더된 정본을 그대로 싣는다 (본문 자리 = 읽기 함수 html) · 그 안에 "2." <h2> · 갱신 날짜 표시',
        bool(dh) and dh in region and re.search(r'<h2[^>]*>\s*2\.', region) is not None
        and bool(marks) and f'갱신 {marks[0]}' in html)
    chk('⑥ 갱신 표지는 화면에 없다 (HTML 주석으로도 · 읽기 함수 html 에도)',
        r.status_code == 200 and 'MIXSTORY:UPDATED' not in html and 'MIXSTORY:UPDATED' not in dh)
    chk('⑦ 정본에 없는 옛 안내 없음 — 성공 화면에 ⛔ 읽기 실패 안내가 없다', r.status_code == 200 and '정본을 읽지 못했다' not in html)

    # ═══ B. fail-closed — 임시 파일 넷 + 화면 ═══
    ok8 = ok9 = ok10 = ok11 = ok12 = False
    route_bad = []
    if doc_fn:
        with tempfile.TemporaryDirectory(prefix='mixstory_') as td:
            p = Path(td) / 'story.md'
            missing = Path(td) / 'none.md'
            cases = (
                ('missing', None, 'none.md 을 읽지 못했다', 'MSNOFILE-0000'),
                ('zero', '# 시험\n\n표지없음-MS1101\n', '갱신 표지가 0 개', '표지없음-MS1101'),
                ('two', '<!-- MIXSTORY:UPDATED 2031-01-02 -->\n<!-- MIXSTORY:UPDATED 2031-01-03 -->\n둘표지-MS2202\n',
                 '갱신 표지가 2 개', '둘표지-MS2202'),
                ('empty', '<!-- MIXSTORY:UPDATED 2031-01-02 -->\n\n   \n', '본문이 비어 있다', 'MSEMPTY-0000'),
            )
            res = {}
            for key, text, want, sentinel in cases:
                if text is None:
                    target = missing
                else:
                    p.write_text(text, encoding='utf-8')
                    target = p
                dd = doc_fn(path=str(target))
                res[key] = (dd.get('ok') is False and want in (dd.get('error') or '') and dd.get('html') == ''
                            and sentinel not in (dd.get('html') or ''))
                orig = webapp.MIXSTORY_MD if hasattr(webapp, 'MIXSTORY_MD') else None
                try:
                    webapp.MIXSTORY_MD = target
                    rr = c.get('/mixer/story')
                    bb = rr.get_data(as_text=True)
                    if not (rr.status_code == 200 and want in bb and 'class="ms-notice"' in bb and sentinel not in bb
                            and '<!--MSDOC-->' not in bb):
                        route_bad.append(key)
                finally:
                    if orig is not None:
                        webapp.MIXSTORY_MD = orig
                    else:
                        del webapp.MIXSTORY_MD
            ok8, ok9, ok10, ok11 = res['missing'], res['zero'], res['two'], res['empty']
            p.write_bytes(b'<!-- MIXSTORY:UPDATED 2031-01-02 -->\n\xff\xfe\x00bad\n')
            try:
                dd = doc_fn(path=str(p))
                ok12 = dd.get('ok') is False and bool(dd.get('error'))
            except Exception:                                   # noqa: BLE001
                ok12 = False
    chk('⑧ 파일 없음 → ok False · "읽지 못했다" · 본문 없음', ok8)
    chk('⑨ 갱신 표지 0 개 → ok False · "갱신 표지가 0 개" · 본문 안 보임', ok9)
    chk('⑩ 갱신 표지 2 개 → ok False · "갱신 표지가 2 개" · 본문 안 보임', ok10)
    chk('⑪ 표지만 있고 본문 빔 → ok False · "본문이 비어 있다"', ok11)
    chk('⑫ UTF-8 이 아닌 바이트 → 예외 없이 ok False + 안내', ok12)
    chk(f'⑬ 위 넷을 화면에 끼우면 200 + 안내 (무엇이 깨졌는지) · 본문 자리 없음 · 옛 문장 없음 (깨진 경우 {route_bad})',
        bool(doc_fn) and not route_bad)
    ok14 = False
    if doc_fn:
        with tempfile.TemporaryDirectory(prefix='mixstory_') as td:
            p = Path(td) / 'story.md'
            p.write_text('# 시험 문서\n\n<!-- MIXSTORY:UPDATED 2031-04-05 -->\n\n## 2. 절-MS7731\n\n고유문구-가나다-MS7731\n', encoding='utf-8')
            orig = webapp.MIXSTORY_MD
            try:
                webapp.MIXSTORY_MD = p
                bb = c.get('/mixer/story').get_data(as_text=True)
                ok14 = ('고유문구-가나다-MS7731' in _doc_region(bb) and '갱신 2031-04-05' in bb
                        and re.search(r'<h2[^>]*>\s*2\. 절-MS7731', bb) is not None and 'MIXSTORY:UPDATED' not in bb)
            finally:
                webapp.MIXSTORY_MD = orig
    chk('⑭ 다른 정본을 끼우면 화면이 그 문장 · 날짜를 따라간다 (베낀 문장이 아니다)', ok14)

    # ═══ C. redact = markdown 변환 전 ═══
    ok15 = ok16 = ok17 = False
    if doc_fn:
        _orig = ledger_view.redact
        with tempfile.TemporaryDirectory(prefix='mixstory_') as td:
            p = Path(td) / 'story.md'
            p.write_text('# 시험\n\n<!-- MIXSTORY:UPDATED 2031-01-02 -->\n\n앞 MXSTORYTOK 뒤\n', encoding='utf-8')
            ledger_view.redact = lambda t: _orig(t).replace('MXSTORYTOK', '**MXSTORYBOLD**')
            try:
                dd = doc_fn(path=str(p))
            finally:
                ledger_view.redact = _orig
            ok15 = (dd.get('ok') is True and '<strong>MXSTORYBOLD</strong>' in (dd.get('html') or '')
                    and '**MXSTORYBOLD**' not in (dd.get('html') or '') and dd.get('redacted') is True)
            bans = [b.get('pattern') for b in ledger_view.banned() if b.get('pattern')]
            if bans:
                pat = max(bans, key=len)
                p.write_text('# 시험\n\n<!-- MIXSTORY:UPDATED 2031-01-02 -->\n\n옛 값 ' + pat + ' 끝\n', encoding='utf-8')
                dd = doc_fn(path=str(p))
                ok16 = (dd.get('ok') is True and '⟨인용금지·' in (dd.get('html') or '') and pat not in (dd.get('html') or '')
                        and dd.get('redacted') is True)
        if marks:
            line = f'<!-- MIXSTORY:UPDATED {marks[0]} -->'
            ledger_view.redact = lambda t: _orig(t).replace(line, line + '\n\nMXSTORYPAGEMARK\n')
            try:
                bb = c.get('/mixer/story').get_data(as_text=True)
            finally:
                ledger_view.redact = _orig
            ok17 = 'MXSTORYPAGEMARK' in _doc_region(bb)
    chk('⑮ redact 가 markdown 변환 전에 돈다 (redact 가 넣은 **굵게** 가 <strong> 으로 · redacted 표지 True)', ok15)
    chk('⑯ 실물 redact — 등록부의 금지값을 넣은 정본은 ⟨인용금지·…⟩ 로 가려지고 원래 값은 화면 html 에 없다', ok16)
    chk('⑰ 화면 경로도 redact 를 지난다 (정본 실물 + 표지 주입이 본문 자리에 보인다)', ok17)

    # ═══ D. 증거 표 — 자료 그대로 ═══
    ev = ev_fn() if ev_fn else {}
    chk('⑱ 증거 자료 전제 — JSON = 객체 · metrics 객체 · 지표마다 팔 (객체) 둘 이상 · 칸 숫자',
        bool(mx) and len(arms) >= 2 and bool(stats))
    chk('⑲ 읽기 함수 (_mixstory_evidence) — ok · 팔 · 통계 · 덧칸 · 행 = 자료 순서',
        ev.get('ok') is True and ev.get('arms') == arms and ev.get('stats') == stats and ev.get('extras') == extras
        and [x.get('name') for x in ev.get('rows') or []] == list(mx))
    rows_html = _ev_rows_html(html)
    want_cols = [f'{a}.{s}' for a in arms for s in stats] + list(extras)
    bad20 = []
    for (name, cells), key in zip(rows_html, list(mx)):
        m = mx.get(key) or {}
        if name != key or [cc for cc, _t, _ti in cells] != want_cols:
            bad20.append(f'{key} 열')
            continue
        for cc, t, ti in cells:
            a, _, s = cc.partition('.')
            v = m.get(a, {}).get(s) if a in arms else m.get(cc)
            if t != (_num_txt(v) or '—') or (_num_txt(v) is not None and ti != repr(v)):
                bad20.append(f'{key} {cc} {t!r} {ti!r}')
    chk(f'⑳ 화면 표 — 행 = 자료 지표 (순서) · 열 = 팔 × 통계 + 덧칸 · 칸 글 = 자료 값 (유효 4 자리) · 칸 title = 자료 전체 값 ({bad20[:3]})',
        len(rows_html) == len(mx) > 0 and not bad20)
    chk('㉑ 표 머리 = 자료의 팔 · 통계 · 덧칸 이름 (자료 키 그대로)',
        all(f'>{_esc(x)}<' in html for x in arms + stats + extras) and bool(arms))
    chk(f'㉒ 패널 표지 "{LABEL}" · 제목 = 자료의 팔 이름 (↔)', LABEL in html and _esc(' ↔ '.join(arms)) in html and bool(arms))
    meta_keys = [k for k in ev_json if k != 'metrics']
    chk('㉓ 자료 머리 (metrics 밖 키) 가 화면에 그대로 — label · n_independent_seeds 등 · 정수 · 문자열 값',
        bool(meta_keys) and all(f'data-meta="{_esc(k)}"' in html for k in meta_keys)
        and all(str(v) in html for k in meta_keys for v in _numbers(ev_json[k]))
        and all(_esc(s) in html for k in meta_keys for s in _strings(ev_json[k])))
    chk('㉔ 표 자료 경로 · 같은 폴더 README 안내가 화면에 있다', f'{DATA}/b1_b2_u_contacts.json' in html and f'{DATA}/README.md' in html)

    ok25 = ok26 = ok27 = ok28 = ok29 = ok30 = ok31 = False
    if ev_fn:
        orig_name = getattr(webapp, '_MIXSTORY_EV_NAME', None)
        try:
            webapp._MIXSTORY_EV_NAME = '__mixstory_missing__.json'
            rr = c.get('/mixer/story')
            bb = rr.get_data(as_text=True)
            ok25 = (orig_name is not None and rr.status_code == 200 and '자료 파일이 없다' in bb and 'class="ms-notice"' in bb
                    and not _ev_rows_html(bb) and re.search(r'<h2[^>]*>\s*2\.', _doc_region(bb)) is not None)
        finally:
            if orig_name is not None:
                webapp._MIXSTORY_EV_NAME = orig_name
        with tempfile.TemporaryDirectory(prefix='mixstory_ev_') as td:
            jp = os.path.join(td, 'ev.json')

            def _w(obj_or_text):
                with open(jp, 'w', encoding='utf-8') as f:
                    f.write(obj_or_text if isinstance(obj_or_text, str) else json.dumps(obj_or_text))
                return ev_fn(path=jp)
            e1 = _w('{"label": "DEVELOPMENT_DATA_ONLY", "metrics": {')
            ok26 = e1.get('ok') is False and bool(e1.get('notice')) and e1.get('rows') == []
            e2a, e2b, e2c = _w([1, 2, 3]), _w({'label': 'x', 'metrics': [1]}), _w({'metrics': {}})
            ok27 = all(e.get('ok') is False and bool(e.get('notice')) and e.get('rows') == [] for e in (e2a, e2b, e2c))
            base = {'label': 'DEVELOPMENT_DATA_ONLY', 'n_independent_seeds': 1,
                    'metrics': {'m_good': {'A': {'s': 0.5, 't': 'x'}, 'B': {'s': float('nan'), 't': 2}, 'diff': True},
                                'm_two': {'A': {'s': 1.25}}, 'm_bad': 7}}
            e3 = _w(base)
            r3 = {x['name']: x for x in e3.get('rows') or []}
            ok28 = (e3.get('ok') is True and list(r3) == ['m_good', 'm_two'] and '객체가 아닌 지표 1 개' in (e3.get('notice') or '')
                    and [(x or {}).get('txt') for x in r3['m_good'].get('cols', [])] == ['0.5', None, None, '2', None]
                    and [(x or {}).get('txt') for x in r3['m_two'].get('cols', [])] == ['1.25', None, None, None, None]
                    and '3 칸' in (e3.get('notice') or ''))
            e4 = _w(dict(base, n_independent_seeds=2, metrics={'m_good': base['metrics']['m_good']}))
            e5 = _w(dict(base, label='CONFIRMATORY', metrics={'m_good': base['metrics']['m_good']}))
            e6 = _w(dict(base, metrics={'m_good': base['metrics']['m_good']}))
            e7 = _w({'metrics': {'m_good': base['metrics']['m_good']}})
            ok29 = ('n_independent_seeds' in (e4.get('label_notice') or '') and 'label' in (e5.get('label_notice') or '')
                    and not e6.get('label_notice') and e4.get('ok') is True and e5.get('ok') is True
                    and 'n_independent_seeds' in (e7.get('label_notice') or '') and 'label' in (e7.get('label_notice') or ''))
            _ev_orig = webapp._mixstory_evidence
            try:
                webapp._mixstory_evidence = lambda path=None: _ev_orig(path=jp)
                _w('{"metrics": {"broken": ')
                rr = c.get('/mixer/story')
                bb = rr.get_data(as_text=True)
                ok30 = (rr.status_code == 200 and '자료를 읽지 못했다' in bb and not _ev_rows_html(bb)
                        and re.search(r'<h2[^>]*>\s*2\.', _doc_region(bb)) is not None)
                _w(dict(base, n_independent_seeds=2, metrics={'m_good': base['metrics']['m_good']}))
                bb = c.get('/mixer/story').get_data(as_text=True)
                ok31 = 'n_independent_seeds' in bb and '표지와 다르다' in bb
            finally:
                webapp._mixstory_evidence = _ev_orig
    chk('㉕ 증거 자료 파일이 없으면 200 + 안내 ("자료 파일이 없다") · 표 행 0 · 정본은 그대로 렌더', ok25)
    chk('㉖ 깨진 JSON → ok False + 안내 · 행 없음 (예외 없음)', ok26)
    chk('㉗ 꼴이 다른 JSON (목록 · metrics 가 객체 아님 · 지표 0 개) → ok False + 안내', ok27)
    chk('㉘ 객체가 아닌 지표는 빼고 안내 · 숫자가 아닌 칸 (글 · NaN · 참거짓) = "—" + 그 수 안내 · 없는 칸도 "—"', ok28)
    chk('㉙ 표지 대조 — 독립 시드 수 ≠ 1 · label ≠ DEVELOPMENT_DATA_ONLY · 두 키가 없으면 안내 (패널 표지가 자료와 어긋남을 숨기지 않는다)', ok29)
    chk('㉚ 깨진 JSON 을 화면에 끼우면 200 + 안내 ("자료를 읽지 못했다") · 정본은 그대로', ok30)
    chk('㉛ 표지 어긋남 안내가 화면에 뜬다 ("표지와 다르다")', ok31)
    ok32 = False
    _orig = ledger_view.redact
    ledger_view.redact = lambda t: (_orig(t).replace('"DEVELOPMENT_DATA_ONLY"', '"DEVELOPMENT_DATA_ONLY·MXSTORYJR<script>MXSX</script>"')
                                    if t.lstrip().startswith('{') else _orig(t))
    try:
        bb = c.get('/mixer/story').get_data(as_text=True)
        ok32 = 'MXSTORYJR' in bb and '&lt;script&gt;MXSX' in bb and '<script>MXSX' not in bb
    finally:
        ledger_view.redact = _orig
    chk('㉜ 증거 JSON 도 파싱 전에 redact 를 지난다 · 자료 글은 이스케이프된다 (<script> 가 그대로 나가지 않는다)', ok32)
    ok33 = False
    if ev_fn:
        _ev_orig = webapp._mixstory_evidence
        try:
            webapp._mixstory_evidence = lambda path=None: dict(_ev_orig(), rows=[7, {'name': 'x', 'cols': 5}], columns=3, meta=9)
            rr = c.get('/mixer/story')
            bb = rr.get_data(as_text=True)
            ok33 = (rr.status_code == 200 and '그리지 못했다' in bb and '보일 그림이 없다' in bb and not _ev_rows_html(bb)
                    and re.search(r'<h2[^>]*>\s*2\.', _doc_region(bb)) is not None)
        finally:
            webapp._mixstory_evidence = _ev_orig
    chk('㉝ 꼴이 다른 자료가 화면까지 가도 200 — 안내 ("그리지 못했다" · "보일 그림이 없다") · 표 행 없음 · 정본은 그대로 렌더', ok33)

    # ═══ E. 그림 둘 — 등록부만 ═══
    good = []
    for fn in FIGS:
        rr = c.get(f'/mixer/story/fig/{fn}')
        good.append(rr.status_code == 200 and (rr.mimetype == 'image/png')
                    and rr.get_data() == (ROOT / DATA / fn).read_bytes() and rr.get_data()[:8] == b'\x89PNG\r\n\x1a\n')
    chk('㉞ 등록 그림 둘 → 200 · image/png · 바이트 = 자료 폴더 파일', all(good) and len(good) == 2)
    bad = []
    for u in BAD_FIG_URLS:
        rr = c.get(u)
        body = rr.get_data(as_text=True)
        if rr.status_code != 404 or any(m in body for m in LEAK_MARKS):
            bad.append((u, rr.status_code))
    chk(f'㉟ 등록부 밖 이름 · 경로 꼴 {len(BAD_FIG_URLS)} 개 → 404 · 다른 파일 글 없음 (등록 그림이 200 일 때만 뜻이 있다 · 어긋남 {bad[:3]})',
        all(good) and not bad)
    imgs = re.findall(r'<img[^>]*src="(/mixer/story/fig/[^"]*)"', html)
    chk('㊱ 화면 그림 = 등록 그림 둘 (그 밖 그림 없음)', sorted(imgs) == sorted(f'/mixer/story/fig/{fn}' for fn in FIGS))
    cap = CAP.read_text(encoding='utf-8') if CAP.is_file() else ''
    cap_title = next((ln[2:].strip() for ln in cap.splitlines() if ln.startswith('# ')), '')
    caps = re.findall(r'<figure class="ms-fig" data-fig="([^"]*)".*?</figure>', html, re.S)
    figblocks = dict(zip(caps, re.findall(r'<figure class="ms-fig" data-fig="[^"]*"(.*?)</figure>', html, re.S)))
    chk('㊲ 밑글 frame_caption.md (있음) → 단면 그림의 figcaption · 제목 줄 = 파일에서 (베끼지 않는다) · 다른 그림에는 밑글 없음',
        bool(cap_title) and (cap_title in figblocks.get(FIGS[0], '') or _esc(cap_title) in figblocks.get(FIGS[0], ''))
        and '<figcaption' in figblocks.get(FIGS[0], '')
        and '<figcaption' not in figblocks.get(FIGS[1], 'x<figcaption') and cap_title not in tpl)
    ok38 = ok39 = ok40 = False
    figs_orig = getattr(webapp, 'MIXSTORY_FIGS', None)
    if isinstance(figs_orig, dict):
        _orig = ledger_view.redact
        ledger_view.redact = lambda t: _orig(t).replace(cap_title, cap_title + ' **MXSTORYCAP**') if cap_title else _orig(t)
        try:
            bb = c.get('/mixer/story').get_data(as_text=True)
            ok38 = bool(cap_title) and '<strong>MXSTORYCAP</strong>' in bb
        finally:
            ledger_view.redact = _orig
        try:
            webapp.MIXSTORY_FIGS = {k: (v[0], '__no_caption__.md') if v[1] else v for k, v in figs_orig.items()}
            rr = c.get('/mixer/story')
            bb = rr.get_data(as_text=True)
            ok39 = (rr.status_code == 200 and '<figcaption' not in bb and 'class="ms-notice"' not in bb
                    and len(re.findall(r'<img[^>]*src="/mixer/story/fig/', bb)) == len(FIGS))
            webapp.MIXSTORY_FIGS = dict(figs_orig, **{FIGS[1]: ('__no_such_figure__.png', None)})
            rr = c.get('/mixer/story')
            bb = rr.get_data(as_text=True)
            ok40 = (rr.status_code == 200 and '그림 파일이 없다' in bb and f'src="/mixer/story/fig/{FIGS[1]}"' not in bb
                    and c.get(f'/mixer/story/fig/{FIGS[1]}').status_code == 404)
        finally:
            webapp.MIXSTORY_FIGS = figs_orig
    chk('㊳ 밑글도 markdown 변환 전에 redact 를 지난다', ok38)
    chk('㊴ 밑글 파일이 없으면 아무것도 더 보이지 않는다 (figcaption 없음 · 안내 없음 · 그림은 그대로)', ok39)
    chk('㊵ 등록 그림 파일이 없으면 화면에 "그림 파일이 없다" (깨진 그림 대신) · 그 그림 주소는 404', ok40)

    # ═══ F. 템플릿 · 메뉴 ═══
    page_nums = [_num_txt(v) for v in _numbers(mx) if _num_txt(v)]
    cand = set()
    for v in _numbers(mx):
        for s in (_num_txt(v), repr(v)):
            if s and len(re.sub(r'\D', '', s)) >= 3:
                cand.add(s)
    for k in meta_keys:
        for v in _numbers(ev_json[k]):
            s = str(v)
            if len(re.sub(r'\D', '', s)) >= 3:
                cand.add(s)
    in_tpl = sorted(s for s in cand if s in tpl)
    chk(f'㊶ 템플릿에 자료 숫자 없음 — 화면의 꼴 (유효 4 자리) · 전체 값 · 머리 숫자 {len(cand)} 개 (발견 {in_tpl[:5]}) · 화면에는 그 숫자가 있다',
        bool(tpl) and bool(cand) and not in_tpl and all(s in html for s in page_nums))
    ids = [x for x in list(mx) + arms + stats + extras + meta_keys if '_' in x or any(ch.isdigit() for ch in x)]
    ids += [s for k in meta_keys for s in _strings(ev_json[k]) if len(s) >= 4]
    in_tpl2 = sorted(s for s in set(ids) if s in tpl)
    chk(f'㊷ 템플릿에 자료 키 · 이름 · 문자열 값 없음 (지표 · 팔 · 통계 · 머리 · 잡 번호 · sha256 · 발견 {in_tpl2[:5]})', bool(tpl) and bool(ids) and not in_tpl2)
    heads = [re.sub(r'[*`_]', '', ln.lstrip('#').strip()) for ln in src.splitlines() if ln.startswith('#')]
    copied = sorted(h for h in heads if len(h) >= 6 and h in tpl)
    chk(f'㊸ 템플릿에 정본 제목 · 절 이름 없음 (발견 {copied[:3]})', bool(tpl) and bool(heads) and not copied)
    chk('㊹ 템플릿 = base.html 확장 · 메뉴 믹서 활성 · 화면에 정본 · 자료 경로 바닥글',
        '{% extends "base.html" %}' in tpl and 'href="/mixer" class="active"' in html
        and 'docs/reviews/mixer_problem_gap_novelty_20261124.md' in html)
    r2 = c.get('/mixer')
    h2 = r2.get_data(as_text=True)
    a = re.search(r'<a href="/mixer/story"([^>]*)>([^<]*)</a>', h2)
    chk('㊺ /mixer 에 /mixer/story 링크 (글 "문제 · 공백" · title 속성) · 문헌 지도 링크 옆',
        r2.status_code == 200 and bool(a) and a.group(2).strip() == '문제 · 공백' and 'title="' in a.group(1)
        and 'href="/mixer/lit"' in h2 and 0 < h2.find('href="/mixer/story"') - h2.find('href="/mixer/lit"') < 800)

    #  markdown 이 없을 때 — _emod_doc 과 같은 대체 (<pre> · & < 이스케이프 · 본문은 그대로)
    ok46 = False
    if doc_fn:
        with tempfile.TemporaryDirectory(prefix='mixstory_') as td:
            p = Path(td) / 'story.md'
            p.write_text('# 시험\n\n<!-- MIXSTORY:UPDATED 2031-01-02 -->\n\n<b>꺾쇠-MS9</b> & 끝\n', encoding='utf-8')
            had = 'markdown' in sys.modules
            saved = sys.modules.get('markdown')
            sys.modules['markdown'] = None              # import markdown → ImportError
            try:
                dd = doc_fn(path=str(p))
            finally:
                if had:
                    sys.modules['markdown'] = saved
                else:
                    sys.modules.pop('markdown', None)
            hh = dd.get('html') or ''
            ok46 = (dd.get('ok') is True and hh.startswith('<pre>') and '&lt;b>꺾쇠-MS9&lt;/b> &amp; 끝' in hh
                    and '<b>꺾쇠' not in hh and 'MIXSTORY:UPDATED' not in hh)
    chk('㊻ markdown 이 없으면 <pre> 대체 (& < 이스케이프 · 표지 없음) — _emod_doc 과 같은 대체', ok46)

    print(f'\ntest_mixer_story_page: {_ok}/{_ok + len(_fail)} PASS' + (f'   FAILED: {_fail}' if _fail else ''))
    return 1 if _fail else 0


if __name__ == '__main__':
    raise SystemExit(main())
