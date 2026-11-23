#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""믹서 문헌 지도 (/mixer/lit) 회귀 — 1저자 11-23 Q4 (믹서 문헌 매트릭스를 웹앱에 · 읽기 전용 · 예비 판정).

  python3 webapp/test_mixer_lit_page.py

자료 = docs/data/mixer_lit_matrix_20261123/ (matrix.json · gap_summary.json · gap_check.md · excluded.md · README.md).
보는 것: 표 행 수 = JSON 행 수 (순서 그대로) · 카드 전 표지 · 카드 행의 slug · 공백 카드 G1–G4 (판정 · 예비 · 좁힌 문장) ·
기준 커밋 · 거르기 (연구 꼴 · 점착 처리 · 황화물 SE · DEM · 카드 / 카드 전) · 빈칸 지도 칸 수 · 행마다 G 표지 · /mixer 링크 ·
자료 없음 · 경로 탈출 · 깨진 JSON · 꼴이 다른 자료 = 200 + 안내 · redact 관문 (파싱 전) · 이스케이프 ·
gap_summary.json ↔ gap_check.md · matrix.json 대조 (판정 낱말 · 좁힌 문장 그대로 · 반례 = 카드 행 · 후보 = 카드 전 행).
"""
import json
import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
_ok, _fail = 0, []

DATA = 'docs/data/mixer_lit_matrix_20261123'
STUDY = ('method_comparison', 'one_factor_sweep', 'multi_factor_doe', 'process_window', 'dem_model',
         'dem_validation', 'mechanism_theory', 'definition_index', 'review', 'coating_effect')


def chk(name, cond):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}')


def _rows_html(html):
    """표의 데이터 행 → [(slug, card, 행 조각)] (`<tr class="lit-row" …>` 만 · 화면 순서)."""
    out = []
    for p in html.split('<tr class="lit-row"')[1:]:
        seg = p.split('</tr>')[0]
        ms, mc = re.search(r'data-slug="([^"]*)"', seg), re.search(r'data-card="([^"]*)"', seg)
        out.append((ms.group(1) if ms else None, mc.group(1) if mc else None, seg))
    return out


def _gap_html(html, gid):
    m = re.search(r'<article class="lit-gap" id="gap-%s"(.*?)</article>' % gid, html, re.S)
    return m.group(1) if m else ''


def _esc(s):
    """Jinja 자동 이스케이프와 같은 꼴 (& < > " ')."""
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            .replace('"', '&#34;').replace("'", '&#39;'))


def _gap_check_sections(text):
    """gap_check.md → {G: dict(claim, head_line, word, narrowed, narrowed_line, verdict_line)} · 요약 표 {G: 첫 칸 첫 낱말}."""
    lines = text.splitlines()
    sec, cur = {}, None
    for i, l in enumerate(lines, 1):
        m = re.match(r'^## (G\d) — "(.+)"$', l)
        if m:
            cur = m.group(1)
            sec[cur] = dict(claim=m.group(2), head_line=i)
            continue
        if l.startswith('## '):
            cur = None
        if cur and l.startswith('**판정: '):
            sec[cur]['word'] = l[len('**판정: '):].split()[0].rstrip('.*')
            sec[cur]['verdict_line'] = i
        mn = re.match(r'^\*\*좁힌 문장 \(권고\)\*\*: \*"(.+)"\*$', l)
        if cur and mn:
            sec[cur]['narrowed'] = mn.group(1)
            sec[cur]['narrowed_line'] = i
    table = {}
    for l in lines:
        m = re.match(r'^\| (G\d) \| ([^|]+) \|', l)
        if m:
            table[m.group(1)] = m.group(2).split()[0]
    return sec, table


def main():
    import app as webapp
    import ledger_view
    rp = webapp._repo_path
    mx = json.load(open(rp(DATA + '/matrix.json'), encoding='utf-8'))
    gs = json.load(open(rp(DATA + '/gap_summary.json'), encoding='utf-8'))
    rows, meta = mx['rows'], mx['meta']
    title_slugs = {r['slug'] for r in rows if r['card'] == 'none'}
    canon_slugs = {r['slug'] for r in rows if r['card'] == 'canon'}
    loader = getattr(webapp, '_mixer_lit_data', None)

    c = webapp.app.test_client()
    r = c.get('/mixer/lit')
    chk('① /mixer/lit 200', r.status_code == 200)
    html = r.get_data(as_text=True)
    th = _rows_html(html)
    chk(f'② 표 데이터 행 수 = matrix.json 행 수 ({len(rows)}) · 순서 그대로', [s for s, _c, _g in th] == [x['slug'] for x in rows])
    by_slug = {s: (cd, seg) for s, cd, seg in th}
    chk('③ 카드 전 (card none) 행마다 보이는 "카드 전" 표지 · 카드 행에는 없음',
        len(th) == len(rows)
        and all(('class="lit-pre"' in by_slug.get(s, ('', ''))[1] and '카드 전' in by_slug.get(s, ('', ''))[1]) for s in title_slugs)
        and all('class="lit-pre"' not in by_slug.get(s, ('', 'class="lit-pre"'))[1] for s in canon_slugs))
    chk('④ 카드 행마다 slug 가 근거 칸에 글로 보인다',
        all(f'<code class="lit-slug">{s}</code>' in by_slug.get(s, ('', ''))[1] for s in canon_slugs))
    chk('⑤ 행마다 data-card = matrix.json card', all(by_slug.get(x['slug'], ('?', ''))[0] == x['card'] for x in rows))
    #  공백 카드
    ok5 = len(gs) == 4
    for g in gs:
        seg = _gap_html(html, g['id'])
        ok5 = ok5 and bool(seg) and f'data-verdict="{g["verdict"]}"' in seg and g['verdict'] in seg and '예비' in seg
    chk('⑥ 공백 카드 G1–G4 넷 — 각자 판정 낱말 · "예비" 표지', ok5)
    g2 = next((g for g in gs if g['id'] == 'G2'), {})
    chk('⑦ G2 카드에 분야 한정 메모 (verdict_note — 전지 · 황화물로 좁히면 holds)',
        bool(g2.get('verdict_note')) and _esc(g2['verdict_note']) in _gap_html(html, 'G2'))
    chk('⑧ 공백 카드마다 좁힌 문장 (그대로) · 가장 강한 반례 slug (also 포함) · 카드 전 후보 번호가 보인다',
        all(_esc(g['narrowed_wording']) in _gap_html(html, g['id'])
            and all(x['slug'] in _gap_html(html, g['id'])
                    for x in [g['strongest_counterexample']] + g['strongest_counterexample'].get('also', []))
            and all(f'>{p["slug"]}<' in _gap_html(html, g['id']) for p in g['pending_cards'])
            for g in gs))
    chk('⑨ 기준 커밋 (meta.ref_sha 40 자리) 이 화면에 있다', bool(re.fullmatch(r'[0-9a-f]{40}', meta['ref_sha'])) and meta['ref_sha'] in html)
    n_card, n_title = len(canon_slugs), len(title_slugs)
    chk(f'⑩ 행 수 표기 — 카드 {n_card} · 카드 전 {n_title} · 전체 {len(rows)}',
        f'카드 {n_card}' in html and f'카드 전 {n_title}' in html and f'{len(rows)} 행' in html)
    chk('⑪ 제목 · 지위 문구 — "믹서 문헌 지도" · "개발 자료 · 예비 판정" · "1저자 11-23 Q4"',
        '믹서 문헌 지도' in html and '개발 자료 · 예비 판정' in html and '1저자 11-23 Q4' in html)
    #  거르기
    sel = {k: re.search(r'<select[^>]*id="%s"[^>]*>(.*?)</select>' % k, html, re.S) for k in
           ('f-study', 'f-adh', 'f-sulfide', 'f-dem', 'f-card')}
    chk('⑫ 거르기 select 다섯 — 연구 꼴 · 점착 처리 · 황화물 SE · DEM · 카드 / 카드 전', all(sel.values()))
    opts = {k: set(re.findall(r'<option value="([^"]*)"', m.group(1))) if m else set() for k, m in sel.items()}
    chk('⑬ 거르기 선택지 — 연구 꼴 = 자료의 모든 값 · 점착 처리 = 범례 여섯 · 황화물 / DEM = 1 · 0 · 카드 = canon · none',
        {x['study_type'] for x in rows} <= opts['f-study']
        and set(meta['legend']['adhesion_handling']) <= opts['f-adh']
        and {'1', '0'} <= opts['f-sulfide'] and {'1', '0'} <= opts['f-dem'] and {'canon', 'none'} <= opts['f-card'])
    #  빈칸 지도
    cells = {(a, b): int(n) for a, b, n in re.findall(r'class="lit-cell[^"]*" data-st="([^"]+)" data-ah="([^"]+)"[^>]*>(\d+)<', html)}
    want = {(st, ah): sum(1 for x in rows if x['study_type'] == st and x['adhesion_handling'] == ah)
            for st in sorted({x['study_type'] for x in rows} | set(STUDY)) for ah in meta['legend']['adhesion_handling']}
    chk('⑭ 빈칸 지도 — 칸 (연구 꼴 × 점착 처리 여섯) 마다 숫자 = 자료에서 센 수 · 0 인 칸도 그린다 · 칸 합 = 행 수',
        cells == want and sum(cells.values()) == len(rows))
    #  행마다 G 표지
    ok15 = len(th) == len(rows)
    for x in rows:
        seg = by_slug.get(x['slug'], ('', ''))[1]
        got = re.findall(r'data-g="(G\d)" data-v="(\w+)"', seg)
        ok15 = ok15 and got == [(gid, x['gap'][gid]['verdict']) for gid in ('G1', 'G2', 'G3', 'G4')]
    chk('⑮ 행마다 G1–G4 표지 넷 (data-v = 그 행의 판정)', ok15)
    chk('⑯ 표 머리 열 — 논문 · 계 · 장치 · 연구 꼴 · 바꾼 변수 · 점착 처리 · 혼합 지표 · DEM · 핵심 결과 · 근거 · G1–G4',
        all(f'>{h}' in html for h in ('논문', '계 (AM / SE)', '장치', '연구 꼴', '바꾼 변수 (수준)', '점착 처리', '혼합 지표', 'DEM',
                                       '핵심 결과', '근거', 'G1–G4')))
    chk('⑰ 바닥글 — 자료 경로 · README 안내 · 표는 가로 스크롤 틀 안 · 메뉴 믹서 활성',
        DATA in html and 'README.md' in html and 'class="lit-tablewrap"' in html and 'overflow-x:auto' in html
        and 'href="/mixer" class="active"' in html)
    r2 = c.get('/mixer')
    chk('⑱ /mixer 에 /mixer/lit 링크', r2.status_code == 200 and 'href="/mixer/lit"' in r2.get_data(as_text=True))

    #  자료 없음 · 경로 탈출 — 모듈 변수 (_MIXER_LIT_DIR) 를 바꿔 본다
    orig_dir = getattr(webapp, '_MIXER_LIT_DIR', None)
    try:
        webapp._MIXER_LIT_DIR = 'docs/data/__mixer_lit_missing__'
        r3 = c.get('/mixer/lit')
        h3 = r3.get_data(as_text=True)
        chk('⑲ 자료 폴더가 없으면 200 + 안내 ("자료 파일이 없다") · 표 행 0',
            orig_dir is not None and r3.status_code == 200 and '자료 파일이 없다' in h3 and 'class="lit-notice"' in h3
            and not _rows_html(h3))
        webapp._MIXER_LIT_DIR = '../__mixer_lit_escape__'
        r4 = c.get('/mixer/lit')
        h4 = r4.get_data(as_text=True)
        chk('⑳ 리포 밖 경로 (탈출) 면 200 + 안내 · 표 행 0',
            orig_dir is not None and r4.status_code == 200 and 'class="lit-notice"' in h4 and not _rows_html(h4))
    finally:
        if orig_dir is not None:
            webapp._MIXER_LIT_DIR = orig_dir

    #  깨진 JSON · 꼴이 다른 JSON · 요약 없음 — 읽기 함수에 임시 폴더 (리포 밖) 를 준다
    ok21 = ok22 = ok23 = False
    if loader:
        with tempfile.TemporaryDirectory(prefix='mixer_lit_') as td:
            with open(os.path.join(td, 'matrix.json'), 'w', encoding='utf-8') as f:
                f.write('{"meta": {"ref_sha": ')
            d = loader(folder=td)
            ok21 = d.get('ok') is False and bool(d.get('notice')) and d.get('rows') == []
            with open(os.path.join(td, 'matrix.json'), 'w', encoding='utf-8') as f:
                f.write('[1, 2, 3]')
            d = loader(folder=td)
            ok22 = d.get('ok') is False and bool(d.get('notice')) and d.get('rows') == []
            with open(os.path.join(td, 'matrix.json'), 'w', encoding='utf-8') as f:
                json.dump({'meta': {'ref_sha': 'f' * 40}, 'rows': [rows[0], 'not-a-row']}, f)
            d = loader(folder=td)
            ok23 = (d.get('ok') is True and [x.get('slug') if isinstance(x, dict) else x for x in d.get('rows') or []] == [rows[0]['slug']]
                    and bool(d.get('notice')) and d.get('gaps') == [] and bool(d.get('gap_notice')))
    chk('㉑ 깨진 JSON → ok False + 안내 (예외 없음)', ok21)
    chk('㉒ 꼴이 다른 JSON (meta · rows 없음) → ok False + 안내', ok22)
    chk('㉓ 객체가 아닌 행은 빼고 안내 · gap_summary.json 이 없으면 공백 칸에만 안내 (표는 그대로)', ok23)

    #  화면 fallback — 꼴이 다른 자료가 템플릿까지 가도 500 이 아니다 · 요약 없음 안내가 화면에 뜬다
    if loader:
        try:
            webapp._mixer_lit_data = lambda folder=None: dict(
                ok=True, notice='', meta={'ref_sha': 'f' * 40, 'legend': 5}, rows=[{'slug': 'bad', 'card': 'canon', 'gap': 7,
                                                                                    'system': 'x', 'varied': 3}],
                gaps=[{'id': 'G9', 'strongest_counterexample': 5}], gap_notice='', redacted=False, data_dir=DATA)
            r5 = c.get('/mixer/lit')
            h5 = r5.get_data(as_text=True)
            ok24 = r5.status_code == 200 and ('그리지 못했다' in h5 or 'data-slug="bad"' in h5)
            webapp._mixer_lit_data = lambda folder=None: dict(loader(), gaps=[], gap_notice='MXLIT 공백 요약 없음')
            r6 = c.get('/mixer/lit')
            h6 = r6.get_data(as_text=True)
            ok25 = r6.status_code == 200 and 'MXLIT 공백 요약 없음' in h6 and len(_rows_html(h6)) == len(rows)
        finally:
            webapp._mixer_lit_data = loader
    else:
        ok24 = ok25 = False
    chk('㉔ 꼴이 다른 자료가 화면까지 가도 200 (안내 또는 그대로)', ok24)
    chk('㉕ 공백 요약이 없으면 안내 + 표는 그대로', ok25)

    #  redact 관문 · 이스케이프 — 파싱 전에 ledger_view.redact 를 지난다 (JSON 안 글에 표지 주입)
    _orig = ledger_view.redact
    ledger_view.redact = lambda t: _orig(t).replace(meta['ref_sha'], meta['ref_sha'] + '·MXLITREDACT<script>MXLITX</script>')
    try:
        h7 = c.get('/mixer/lit').get_data(as_text=True)
    finally:
        ledger_view.redact = _orig
    chk('㉖ 화면 글이 파싱 전에 ledger_view.redact 를 지난다 (표지가 화면에 보인다)', 'MXLITREDACT' in h7)
    chk('㉗ 자료 글은 이스케이프된다 (<script> 가 그대로 나가지 않는다)',
        '<script>MXLITX' not in h7 and '&lt;script&gt;MXLITX' in h7)

    #  gap_summary.json ↔ gap_check.md · matrix.json
    gtext = open(rp(DATA + '/gap_check.md'), encoding='utf-8').read()
    glines = gtext.splitlines()
    sec, table = _gap_check_sections(gtext)
    chk('㉘ gap_summary.json = G1–G4 넷 (순서) · 판정 = weakened / broken / holds',
        [g.get('id') for g in gs] == ['G1', 'G2', 'G3', 'G4'] and all(g.get('verdict') in ('weakened', 'broken', 'holds') for g in gs))
    chk('㉙ 판정 낱말 = gap_check.md 요약 표 첫 낱말 = 절 판정 줄 첫 낱말 · 주장 = 절 제목',
        all(g['verdict'] == table.get(g['id']) == sec.get(g['id'], {}).get('word') and g['claim'] == sec[g['id']]['claim'] for g in gs))
    chk('㉚ 좁힌 문장 = 절 끝 "좁힌 문장 (권고)" 그대로 · source 줄 번호가 그 줄을 가리킨다',
        all(g['narrowed_wording'] == sec[g['id']].get('narrowed')
            and g['source']['narrowed_line'] == sec[g['id']].get('narrowed_line')
            and g['source']['verdict_line'] == sec[g['id']].get('verdict_line')
            and g['source']['section_lines'][0] == sec[g['id']]['head_line']
            and g['narrowed_wording'] in glines[g['source']['narrowed_line'] - 1] for g in gs))
    chk('㉛ 가장 강한 반례 (also 포함) = 카드 행 · 요약 표에 그 slug 와 줄이 있다 · 후보 = 카드 전 행',
        all(x['slug'] in canon_slugs and f"{x['line_ref']} ({x['summary_ko']})" in glines[g['source']['summary_table_line'] - 1]
            for g in gs for x in [g['strongest_counterexample']] + g['strongest_counterexample'].get('also', []))
        and all(p['slug'] in title_slugs for g in gs for p in g['pending_cards']))
    chk('㉜ G2 만 분야 한정 메모 (broken · 좁히면 holds) — 나머지는 null',
        g2.get('verdict') == 'broken' and 'holds' in (g2.get('verdict_note') or '')
        and all(g.get('verdict_note') is None for g in gs if g['id'] != 'G2'))
    tsv = open(rp(DATA + '/matrix.tsv'), encoding='utf-8').read().splitlines()
    chk('㉝ matrix.tsv ↔ matrix.json — 머리 + 76 행 · slug 순서 같음 · meta 행 수 = 실제',
        len(tsv) == len(rows) + 1 and [l.split('\t')[0] for l in tsv[1:]] == [x['slug'] for x in rows]
        and meta['n_rows'] == len(rows) and meta['n_card_rows'] == n_card and meta['n_title_rows'] == n_title)
    readme = open(rp(DATA + '/README.md'), encoding='utf-8').read()
    chk('㉞ README — 기준 커밋 · "예비 판정" · "scratch 도구 · 리포 밖" · 1저자 11-23 Q4',
        meta['ref_sha'] in readme and '예비 판정' in readme and 'scratch 도구 · 리포 밖' in readme and '1저자 11-23 Q4' in readme)

    print(f'\ntest_mixer_lit_page: {_ok}/{_ok + len(_fail)} PASS' + (f'   FAILED: {_fail}' if _fail else ''))
    return 1 if _fail else 0


if __name__ == '__main__':
    raise SystemExit(main())
