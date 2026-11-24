#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""믹서 문헌 지도 (/mixer/lit) 회귀 — 1저자 11-23 Q4 (믹서 문헌 매트릭스를 웹앱에 · 읽기 전용 · 예비 판정).

  python3 webapp/test_mixer_lit_page.py

자료 = docs/data/mixer_lit_matrix_20261123/ (matrix.json · gap_summary.json · gap_check.md · excluded.md · README.md).
보는 것: 표 행 수 = JSON 행 수 (순서 그대로) · 카드 전 표지 · 카드 행의 slug · 공백 카드 G1–G4 (판정 · 예비 · 좁힌 문장) ·
기준 커밋 · 거르기 (연구 꼴 · 점착 처리 · 황화물 SE · DEM · 카드 / 카드 전) · 빈칸 지도 칸 수 · 행마다 G 표지 · /mixer 링크 ·
자료 없음 · 경로 탈출 · 깨진 JSON · 꼴이 다른 자료 = 200 + 안내 · redact 관문 (파싱 전) · 이스케이프 ·
gap_summary.json ↔ gap_check.md · matrix.json 대조 (판정 낱말 · 좁힌 문장 그대로 · 반례 = 카드 행 · 후보 = 카드 전 행).
11-24 갱신 (1저자 11-24 — litdb 새 카드 14 편 반영 · G1–G4 좁힌 판정 · 시험 먼저 · 웹앱 같은 묶음): ㉟ 행 수 77 = 카드 67 + 카드 전 10 ·
㊱ 큐 14 편 = 정본 카드 행 (옛 큐 번호 행 없음 · 행이 큐 번호를 적는다) · ㊲ 화면 = 카드 행 · ㊳ 카드 실재 (기준 커밋 · 줄 번호 ≤ 카드 줄 수 ·
git 기준 커밋을 못 읽으면 SKIP) · ㊴ 좁힌 판정 문구 · ㊵ 가장 강한 반례 갱신 · ㊶ 근거 카드 (evidence_cards ↔ matrix.json ↔ gap_check.md) ·
㊷ 화면 근거 카드 · ㊸ 카드 전 후보 없음 · ㊹ 고친 날 · 갱신 메모 · ㊺ README · ㊻ matrix.tsv 칸 대조 · ㊼ N-157 (D'Amore 2022) 의 조심스러운 함의.
"""
import json
import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
_ok, _fail = 0, []

DATA = 'docs/data/mixer_lit_matrix_20261123'
STUDY = ('method_comparison', 'one_factor_sweep', 'multi_factor_doe', 'process_window', 'dem_model',
         'dem_validation', 'mechanism_theory', 'definition_index', 'review', 'coating_effect')
#  11-24 갱신 — 큐 번호 → litdb 정본 카드 slug (1저자 11-23 요청 14 편 · 인계 docs/handoff_return_to_stoic_knuth_20261124.md §3-3 · §3-5)
NEW_1124 = {
    'N-110': 'figueroa2009_vdw_adhesion_mixing_segregation_bond_number_phase_diagram',
    'N-111': 'capece2015_multicomponent_granular_bond_number_cohesive_blend_flow_function',
    'N-112-1': 'li2003_cohesive_mixing_segregation_pairwise_bond_hierarchy',
    'N-112-2': 'li2005_cohesive_mixing_phase_diagrams_bond_ratio_dem_validation',
    'N-113': 'egermann1980_ordered_vs_random_adhesion_pseudorandom_mixture_homogeneity',
    'N-118': 'khakhar1999_chaotic_mixing_granular_2d_tumbling_mixers_flowing_layer',
    'N-150': 'chaudhuri2006_cohesive_mixing_tumbling_blender_bond_number_rotation_speed',
    'N-151': 'li2006_cohesive_mixing_shear_cell_collision_number_phase_diagram',
    'N-152': 'jones2008_cohesive_adhesive_balance_carrier_dpi_performance_slightly_cohesive_optimum',
    'N-153': 'liu2013_wet_cohesive_particles_transverse_mixing_rotating_drum_circulation_period',
    'N-154': 'mellmann2001_transverse_bed_motion_rotating_cylinders_slumping_rolling_cascading_froude',
    'N-155': 'chen2004_mechanofusion_dry_coating_dem_2d_host_scraper_inner_piece_collision_frequency',
    'N-156': 'dave2003_dry_coating_dem_mechanofusion_hybridizer_maic_three_devices',
    'N-157': 'damore2022_lpscl_symmetry_breaking_surface_energy_wulff_pbe0',
}
N_ROWS_1124, N_CARD_1124, N_TITLE_1124 = 77, 67, 10      # 76 (53 + 23) → 큐 13 이 카드 행으로 · N-157 새 행
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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


def _git_show(ref, path):
    """기준 커밋의 파일 글 (읽기만 · 네트워크 없음).  ref 를 못 읽으면 None — 부르는 쪽이 SKIP 으로 적는다."""
    try:
        r = subprocess.run(['git', '-C', REPO, 'show', f'{ref}:{path}'], capture_output=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    return r.stdout.decode('utf-8', 'replace') if r.returncode == 0 else None


def _own_line_refs(card_refs):
    """card_refs 가운데 그 행 자신의 카드를 가리키는 줄 번호 ('L7 제목줄' · 'L28–L33 …' 꼴 · 다른 파일 · 카드 줄은 뺀다)."""
    out = []
    for c in card_refs:
        m = re.match(r'^L(\d+)(?:[–-]L(\d+))?\b', c)
        if m:
            out += [int(x) for x in m.groups() if x]
    return out


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
    chk(f'㉝ matrix.tsv ↔ matrix.json — 머리 + {len(rows)} 행 · slug 순서 같음 · meta 행 수 = 실제',
        len(tsv) == len(rows) + 1 and [l.split('\t')[0] for l in tsv[1:]] == [x['slug'] for x in rows]
        and meta['n_rows'] == len(rows) and meta['n_card_rows'] == n_card and meta['n_title_rows'] == n_title)
    readme = open(rp(DATA + '/README.md'), encoding='utf-8').read()
    chk('㉞ README — 기준 커밋 · "예비 판정" · "scratch 도구 · 리포 밖" · 1저자 11-23 Q4',
        meta['ref_sha'] in readme and '예비 판정' in readme and 'scratch 도구 · 리포 밖' in readme and '1저자 11-23 Q4' in readme)

    #  ═══ 11-24 갱신 — litdb 새 카드 14 편 · G1–G4 좁힌 판정 (1저자 11-24 · 시험 먼저) ═══
    by_row = {x['slug']: x for x in rows}
    G = {g['id']: g for g in gs}

    def _t(gid, k):
        return (G.get(gid) or {}).get(k) or ''

    chk(f'㉟ 11-24 행 수 — {N_ROWS_1124} 행 = 카드 {N_CARD_1124} + 카드 전 {N_TITLE_1124} · meta.updated = 2026-11-24',
        len(rows) == N_ROWS_1124 and n_card == N_CARD_1124 and n_title == N_TITLE_1124 and meta.get('updated') == '2026-11-24')
    ok36 = len(NEW_1124) == 14
    for nid, slug in NEW_1124.items():
        x = by_row.get(slug)
        ok36 = (ok36 and x is not None and x.get('card') == 'canon' and x.get('classified_by') == 'card' and nid not in by_row
                and (nid in ' '.join(x.get('card_refs') or []) or nid in (x.get('inclusion_reason') or '')))
    chk('㊱ 큐 14 편 = 정본 카드 행 (card canon · classified_by card · slug = 카드 slug) · 옛 큐 번호 행 없음 · 행이 큐 번호를 적는다', ok36)
    chk('㊲ 화면 — 14 행이 카드 행 (data-card canon · slug 글 · 카드 전 표지 없음)',
        all(by_slug.get(s, ('', ''))[0] == 'canon' and f'<code class="lit-slug">{s}</code>' in by_slug.get(s, ('', ''))[1]
            and 'class="lit-pre"' not in by_slug.get(s, ('', 'class="lit-pre"'))[1] for s in NEW_1124.values()))
    ref = meta.get('ref_sha', '')
    try:
        have_ref = bool(re.fullmatch(r'[0-9a-f]{40}', ref)) and subprocess.run(
            ['git', '-C', REPO, 'cat-file', '-e', ref + '^{commit}'], capture_output=True, timeout=60).returncode == 0
    except (OSError, subprocess.SubprocessError):
        have_ref = False
    if not have_ref:
        print(f'  SKIP  ㊳ 카드 실재 — 기준 커밋 {ref[:9]} 을 이 리포에서 못 읽는다 (litdb 정본 가지를 fetch 한 뒤 다시)')
    else:
        bad38 = []
        for x in rows:
            if x['card'] != 'canon':
                continue
            t = _git_show(ref, f"litdb/papers/{x['slug']}.md")
            if t is None:
                bad38.append(x['slug'] + ' (기준 커밋에 없음)')
                continue
            n_l, own = len(t.splitlines()), _own_line_refs(x['card_refs'])
            if any(L < 1 or L > n_l for L in own) or (x['slug'] in NEW_1124.values() and len(own) < 3):
                bad38.append(f"{x['slug']} (줄 {own} · 카드 {n_l} 줄)")
        chk(f'㊳ 카드 실재 — 카드 행 {n_card} 장 전부 기준 커밋의 litdb/papers/<slug>.md · card_refs 의 줄 번호 ≤ 카드 줄 수 · 새 행 줄 근거 ≥ 3',
            not bad38)
        if bad38:
            print('         ', bad38[:6])
    chk('㊴ 좁힌 판정 (11-24) — G1 "직접 반례 없음" · G2 "전지 · 황화물" (+ 같은 SE 탐침 AFM 쌍별 · 압밀 뒤 이온 경로) · '
        'G3 "점착 대비가 있는 계에서 rpm 축" · "한 운동 꼴 안" · G4 "점착 축을 넣은 상태도" · 판정 낱말 weakened / broken / weakened / weakened · 이유가 화면에',
        '직접 반례 없음' in _t('G1', 'verdict_reason')
        and '전지 · 황화물' in _t('G2', 'narrowed_wording') and '같은 SE 탐침 AFM 쌍별' in _t('G2', 'verdict_note')
        and '압밀 뒤 이온 경로' in _t('G2', 'verdict_note')
        and '점착 대비가 있는 계에서 rpm 축' in _t('G3', 'narrowed_wording') and '한 운동 꼴 안' in _t('G3', 'narrowed_wording')
        and '점착 축을 넣은 상태도' in _t('G4', 'narrowed_wording')
        and [_t(k, 'verdict') for k in ('G1', 'G2', 'G3', 'G4')] == ['weakened', 'broken', 'weakened', 'weakened']
        and all(_t(k, 'verdict_reason') and _esc(_t(k, 'verdict_reason')) in _gap_html(html, k) for k in ('G1', 'G2', 'G3', 'G4')))

    def _ce(gid):
        s = (G.get(gid) or {}).get('strongest_counterexample') or {}
        return [s] + (s.get('also') or [])
    chk('㊵ 가장 강한 반례 갱신 — G3 에 chen2004 · dave2003 (벽 부착 ↔ 충돌 세기) · G4 = mellmann2001 (공정 × 흐름 물성 상태도 · 반례에 가까움) · '
        '그 자리의 새 카드는 그 G 에서 반례 · 부분인 카드 행',
        {NEW_1124['N-155'], NEW_1124['N-156']} <= {x.get('slug') for x in _ce('G3')}
        and _ce('G4')[0].get('slug') == NEW_1124['N-154']
        and all(by_row[x['slug']]['gap'][gid]['verdict'] in ('contradicts', 'partial')
                for gid in G for x in _ce(gid) if x.get('slug') in NEW_1124.values()))
    ok41, why41 = bool(G), []
    for gid, g in G.items():
        ev = g.get('evidence_cards')
        if not isinstance(ev, list) or not ev:
            ok41 = False
            why41.append(f'{gid} 근거 카드 없음')
            continue
        lo, hi = g['source']['section_lines']
        sec_txt = '\n'.join(glines[lo - 1:hi])
        evs = [e.get('slug') for e in ev]
        need = {x['slug'] for x in rows if x['card'] == 'canon' and x['gap'][gid]['verdict'] in ('contradicts', 'partial')}
        if not need <= set(evs):
            ok41 = False
            why41.append(f'{gid} 빠짐 {sorted(need - set(evs))[:3]}')
        if len(set(evs)) != len(evs):
            ok41 = False
            why41.append(f'{gid} 중복')
        for e in ev:
            x = by_row.get(e.get('slug'))
            nid = next((k for k, v in NEW_1124.items() if v == e.get('slug')), None)
            if not (x and x['card'] == 'canon' and e.get('verdict') == x['gap'][gid]['verdict'] and f"`{e.get('slug')}`" in sec_txt
                    and e.get('since') == ('2026-11-24' if nid else '2026-11-23') and e.get('n_id') == nid
                    and e.get('line_ref') and e.get('note_ko')):
                ok41 = False
                why41.append(f'{gid} {e.get("slug")}')
    chk('㊶ 근거 카드 (evidence_cards) — 공백마다: 항목 = 카드 행 · 판정 = 그 행의 G 판정 · 그 G 에서 반례 · 부분인 카드 행 전부 · '
        '11-24 새 카드 = since 2026-11-24 · n_id = 큐 번호 · slug 가 gap_check.md 그 절 안 · 중복 없음', ok41)
    if why41:
        print('         ', why41[:6])
    ok42 = bool(G)
    for gid, g in G.items():
        seg = _gap_html(html, gid)
        evl = g.get('evidence_cards') or []
        ok42 = (ok42 and bool(evl)
                and all(re.search(r'data-ev="%s" data-v="%s"' % (re.escape(str(e.get('slug'))), re.escape(str(e.get('verdict')))), seg)
                        for e in evl)
                and seg.count('class="lit-new"') == sum(1 for e in evl if e.get('since') == '2026-11-24'))
    chk('㊷ 화면 — 공백 카드마다 근거 카드 목록 (data-ev = slug · data-v = 판정) · 11-24 새 카드 표지 수 = 자료', ok42)
    rest = [x for x in rows if x['card'] == 'none']
    chk('㊸ 카드 전 후보 — 공백마다 pending_cards 빈 목록 (남은 카드 전 행은 어느 공백에서도 반례 · 부분이 아니다) · 화면에 "없음" 안내',
        bool(G) and all(g.get('pending_cards') == [] for g in gs)
        and all(x['gap'][gid]['verdict'] in ('supports', 'unrelated') for x in rest for gid in ('G1', 'G2', 'G3', 'G4'))
        and all('카드 전 후보가 남지 않았다' in _gap_html(html, gid) for gid in G))
    chk('㊹ 화면 — 고친 날 (meta.updated) · 갱신 메모 (meta.update_note — 자료에서 그대로) · 옛 고정 문장 ("N-110 · N-112 · N-150–N-153 카드가 나오면") 없음',
        bool(meta.get('update_note')) and f'고친 날 {meta.get("updated")}' in html and _esc(meta['update_note']) in html
        and 'N-110 · N-112 · N-150–N-153 카드가 나오면' not in html)
    chk(f'㊺ README — 11-24 갱신 줄 · "{N_ROWS_1124} 행 = 정본 카드 {N_CARD_1124} + 카드 전 (제목만) {N_TITLE_1124}" · 기준 커밋 · 옛 기준 a65bbdb24',
        '2026-11-24' in readme and f'{N_ROWS_1124} 행 = 정본 카드 {N_CARD_1124} + 카드 전 (제목만) {N_TITLE_1124}' in readme
        and meta['ref_sha'] in readme and 'a65bbdb24' in readme)
    hdr = tsv[0].split('\t') if tsv else []
    col = {h: i for i, h in enumerate(hdr)}
    ok46 = len(hdr) == 37 and len(tsv) == len(rows) + 1
    for l, x in zip(tsv[1:], rows):
        f = l.split('\t')
        ok46 = (ok46 and len(f) == 37 and f[col['card']] == x['card'] and f[col['classified_by']] == x['classified_by']
                and f[col['title']] == x['title'] and f[col['key_finding']] == x['key_finding']
                and f[col['card_refs']] == ' | '.join(x['card_refs'])
                and all(f[col[gid]] == x['gap'][gid]['verdict'] and f[col[gid + '_reason']] == x['gap'][gid]['reason']
                        for gid in ('G1', 'G2', 'G3', 'G4')))
    chk('㊻ matrix.tsv ↔ matrix.json 칸 대조 (37 열 · 카드 / 카드 전 · 제목 · 핵심 결과 · 근거 · G 판정 · 이유)', ok46)
    d57 = by_row.get(NEW_1124['N-157']) or {}
    g57 = d57.get('gap') if isinstance(d57.get('gap'), dict) else {}
    blob57 = ' '.join([d57.get('key_finding') or '', d57.get('adhesion_note') or '']
                      + [(g57.get(k) or {}).get('reason') or '' for k in ('G1', 'G2', 'G3', 'G4')])
    chk("㊼ N-157 (D'Amore 2022) — 황화물 SE 있음 · G1–G4 = 무관 넷 · 인쇄값 0.297 · 0.344 · 0.291 ([인쇄 …] 표지) · 함의 = [카드 산술] · "
        "'총 표면 에너지' 한정 ('점착 일 W 로 바로 쓰지 않는다') · 판가름 수 0.31 대조 · '공백 판정을 바꾸지 않는다'",
        (d57.get('sulfide_se') or {}).get('value') is True
        and [(g57.get(k) or {}).get('verdict') for k in ('G1', 'G2', 'G3', 'G4')] == ['unrelated'] * 4
        and all(v in (d57.get('key_finding') or '') for v in ('0.297', '0.344', '0.291', '[인쇄'))
        and '[카드 산술]' in blob57 and '총 표면 에너지' in blob57 and '점착 일 W 로 바로 쓰지 않는다' in blob57
        and '0.31' in blob57 and '공백 판정을 바꾸지 않는다' in blob57)

    print(f'\ntest_mixer_lit_page: {_ok}/{_ok + len(_fail)} PASS' + (f'   FAILED: {_fail}' if _fail else ''))
    return 1 if _fail else 0


if __name__ == '__main__':
    raise SystemExit(main())
