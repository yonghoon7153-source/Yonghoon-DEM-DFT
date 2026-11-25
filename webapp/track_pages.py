#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""track_pages.py — 웹앱 '트랙 묶음' 의 표 하나 (사이드바 · /reports · 시험이 함께 본다 · 사본을 만들지 않는다).

1저자 11-25 *"이렇게 독립적인 우리 분야들 있잖아 이렇게 토글로 묶고 이렇게 안에서 html 나 웹페이지 등 킬 수 있게 해줘"* —
참고 = DFT 웹앱 사이드바의 '공유 보고서' 줄 + 접힘 토글 '캠페인 페이지 N' 과 /reports 화면 (꼴만 옮겼다).

  TRACKS       트랙 (slug · name · group · what · pages).  순서 = CLAUDE.md '용훈 포메이션' ① 의 순서.
               pages = 이미 있는 화면 (label · url · icon · title · active).  화면이 없으면 빈 묶음 → 사이드바 · /reports 에 '화면 없음'.
               active = 그 화면이 render_template 에 넘기는 active 값 (옛 사이드바 줄과 같은 켜짐 규칙) · 없으면 주소가 같을 때만 켜진다.
  REPORTS      공유 보고서 (slug · track · rel · title · date · note · earlier).  리포에 이미 있는 단독 HTML 만 ·
               title = 파일의 <title> · date = 파일 이름의 날짜 (YYYYMMDD) — 시험이 둘 다 파일과 대조한다.
  NOT_REPORTS  보고서로 올리지 않는 HTML 의 규칙과 사유.  시험 (webapp/test_track_reports.py) 이 git 이 아는 HTML 을 전부
               '등록' · '사유 있는 제외' · '틀 폴더 (webapp/templates · Jinja 틀)' 로 나눈다 — 새 HTML 이 생기면 둘 중 하나에 넣는다.

⛔ 이 모듈이 못 하는 것
  · 트랙 · 보고서의 지위를 판정하지 않는다.  배지는 이 표에 등록된 화면 · 보고서 수만 센다 ('페이지 n · 보고서 m') — 0 이면 그 칸을 안 쓴다.
  · 화면 (라우트) 이 살아 있는지 · 보고서 값이 원장과 맞는지 보지 않는다 — 앞의 것은 시험이 GET 으로 본다.
  · 메모 · 형광펜을 저장하지 않는다.  보기 화면의 docnote.js 가 **보는 사람 브라우저 (localStorage)** 에만 둔다 —
    다른 기기 · 다른 사람과 나누지 않고, 원본 · 내려받기는 파일 바이트 그대로다.
  · app.py 는 이 모듈을 **함수 안** (라우트 · context processor) 에서만 import 한다.  194 망 배치 워커가 app 을 import 하므로
    모듈 수준 import 는 봉인 밖 모듈을 망 정지 경로에 넣는다 (scripts/run_network_194_parallel.py DEP_LAZY_OFFPATH 한 줄).
    그래서 DFT 판처럼 '보고서마다 인자 없는 라우트를 표를 돌며 단다' 는 못 한다 (표를 읽으려면 import 때 이 모듈을 불러야 한다) —
    `/reports/<slug>` 하나에 표 대조 (없는 slug = 404) 로 한다.  DFT 판이 그 꼴을 쓴 이유 (자동 열거 시험) 는 이 웹앱에 없다.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

#: 보기 화면 iframe 이 상대 경로로 받는 자산 — 그림 · 스타일 · 표 데이터만.  HTML 은 표에 올려 원본 경로 (/reports/<slug>/raw) 로만 낸다.
ASSET_EXT = ('.png', '.jpg', '.svg', '.webp', '.gif', '.css', '.csv')

# ─────────────────────────────────────────────────────────────────────────
# 1) 트랙 — 순서 = 용훈 포메이션 ① · 옮긴 줄은 옛 사이드바 (base.html) 의 주소 · 글 · title 그대로
# ─────────────────────────────────────────────────────────────────────────
TRACKS = (
    dict(slug='rint2', name='[Rint ②]', group=None,
         what='맞닿은 자리의 저항 (접촉 · 계면 저항) 을 전도도 계산에 넣는 일',
         pages=(
             # 10-21: Rint 설명 (1저자 *"이것도 dem webapp에 추가해줭"*).  정적 페이지 (webapp/static/explain/) 를 링크한다 ·
             #   11-25 사이드바 트랙 묶음으로 옮김 (주소 그대로) · 시험 webapp/test_rint_explainer_page.py
             dict(label='Rint 설명', url='/static/explain/rint_overview_20261021.html', icon='\U0001F517',
                  title='Rint (접촉 · 계면 저항) 을 시뮬레이션에 넣는 일 — 무엇을 넣나 · 어디서 막히나 · 그림 6 장 (10-21)'),
         )),
    dict(slug='dem-a', name='Ⓐ DEM 신뢰성', group='[DEM 우선]',
         what='언로딩 · 고체량 맞춤 · 실험 원측정 · SEM 단면 — 실제 전극과 맞추기',
         pages=()),
    dict(slug='dem-b', name='Ⓑ DEM → MPM 연계', group='[DEM 우선]',
         what='DEM 침대를 MPM 으로 넘겨 SE 소성 변형 · 입자 형태 · 피복 보기',
         pages=(
             # 11-16: MPM 쉬운 설명 + 우리 MPM Q&A (1저자 *"이 내용 MPM으로 웹앱에 넣어줘용 잘 크롭해서"* ·
             #   *"우리 누적되어 있던 Q 관련해서도 Q&A 형식으로 쌓아놓으면 좋을듯"*).  정적 페이지 (webapp/static/explain/) 를 링크한다 ·
             #   그림 = webapp/static/explain/mpm_basics_figs/ · 11-25 사이드바 트랙 묶음으로 옮김 (주소 그대로) · 시험 webapp/test_mpm_basics_page.py
             dict(label='MPM 설명 · Q&A', url='/static/explain/mpm_basics_20261116.html', icon='\U0001F535',
                  title='MPM (물질점법) 쉬운 설명 — 물질점 · 격자 · 점→격자→점 · DEM 과 다른 점 + 우리 MPM 에서 쌓인 질문 Q&A (11-16)'),
         )),
    dict(slug='dem-c', name='Ⓒ 코팅 활물질 믹싱', group='[DEM 우선]',
         what='코팅 활물질의 건식 혼합 (믹서 DEM) — 개발 이력 · 침대 · 문제 · 공백 · 문헌',
         pages=(
             dict(label='믹서 (이력 · 침대)', url='/mixer', icon='\U0001F300', active='mixer'),
             # 순서 = /mixer 화면의 단추 순서 (문헌 지도 → 문제 · 공백)
             dict(label='믹서 문헌 지도', url='/mixer/lit', icon='\U0001F4DA',
                  title='믹서 원고의 문제 정의 · 공백 (G1–G4) 근거 — 문헌 매트릭스 (예비 판정)'),
             dict(label='믹서 문제 · 공백', url='/mixer/story', icon='\U0001F9ED',
                  title='믹서 원고의 문제 정의 · 공백 · 새로움 — 정본 문서를 그대로 읽는다 · 접촉 지표 표 · 그림 (개발 자료 · 한 시드 · 판정 아님)'),
         )),
    dict(slug='suyoung', name='[DEM 우선 (수영)]', group=None,
         what='가압부터 탈압까지 한 모델로 (재설계 · 2D 시험 먼저)',
         pages=(
             # 11-10: DEM 재설계 (수영) 계획서 (1저자 *"좀더 계획서 같은 느낌으로 마감성있게 웹앱에 별도 페이지"*).
             #   정적 페이지 (webapp/static/explain/) 를 링크한다 · 글 = 생성기 scripts/build_dem_redesign_plan.py 가 원문에서
             #   (--check = 바이트 같음) · 그 페이지 머리에서 "처음 보는 분을 위한 설명" 으로 간다 ·
             #   11-25 사이드바 트랙 묶음으로 옮김 (주소 그대로) · 시험 webapp/test_dem_redesign_plan_page.py
             dict(label='DEM 재설계 계획서 (수영)', url='/static/explain/dem_redesign_plan_20261110.html', icon='\U0001F4CB',
                  title='DEM 재설계 (수영) 계획서: 2D 시험으로 먼저 가르기 · 단계 0-7 · 1저자 결정 · Codex 판정 (11-10)'),
             dict(label='처음 보는 분을 위한 설명', url='/static/explain/dem_redesign_plan_newcomer_20261110.html', icon='\U0001F4D6',
                  title='DEM 재설계 (수영) 계획서 · 처음 보는 분을 위한 설명'),
         )),
    dict(slug='lhs-net', name='LHS 접촉망', group=None,
         what='LHS 침대의 접촉망 계산 → ML 인계표',
         pages=()),
    dict(slug='lhs-dem', name='LHS DEM 런', group=None,
         what='LHS 설계점의 DEM 침대 런',
         pages=()),
    dict(slug='kg50', name='50kg (후막)', group=None,
         what='50 kg 과제 후막 전극 DEM — 4 차년도 보고',
         pages=(
             # 11-02: 2D DEM 방법 그림 (50kg 4차년도 보고 0쪽 · 1저자 11-01 *"2d로 지금 그림 넣은것들 webapp에 넣고 뽑을거야"*).
             #   정적 페이지 (webapp/static/dem_method_figs/) 를 링크한다 · 그림 사본 = scripts/sync_dem_method_figs_to_webapp.py
             #   (--check = docs 원본과 바이트 같음) · 11-25 사이드바 트랙 묶음으로 옮김 (주소 그대로 · 1저자 *"이것도 트랙 페이지에 넣어"* ·
             #   일반 자리 줄은 뺐다) · 시험 webapp/test_dem_method_figs_page.py
             dict(label='DEM 방법 그림 (2D)', url='/static/dem_method_figs/index.html', icon='\U0001F5BC️',
                  title='50kg 4차년도 보고 0쪽 — DEM 해석 절차 · 접촉 모델 그림 (2D 모식 계산 · 그림용) · PNG · SVG 내려받기'),
         )),
    dict(slug='hetero', name='이종기술', group=None,
         what='코팅 · 분산 · 시뮬레이션을 잇는 과제 — 논지 · 실험 라인 · 회의록',
         pages=(
             dict(label='이종기술', url='/hetero', icon='\U0001F9EA', active='hetero'),
             dict(label='이종기술 회의록 해체', url='/hetero/transcript', icon='\U0001F4DD',
                  title='회의록 해체 분석 — 원문 · 해독 · 주장 세 층 (최신 회의)'),
         )),
)

# ─────────────────────────────────────────────────────────────────────────
# 2) 공유 보고서 — 리포에 이미 있는 단독 HTML 만 (title = 파일 <title> · date = 파일 이름의 날짜)
# ─────────────────────────────────────────────────────────────────────────
REPORTS = (
    dict(slug='mpm-basics', track='dem-b', rel='webapp/static/explain/mpm_basics_20261116.html',
         title='MPM 쉬운 설명 · 우리 MPM Q&A', date='2026-11-16',
         note='물질점 · 격자 · DEM 과 다른 점 + 우리 MPM 에서 쌓인 질문'),
    dict(slug='dem-redesign-plan', track='suyoung', rel='webapp/static/explain/dem_redesign_plan_20261110.html',
         title='DEM 재설계 (수영) 계획서', date='2026-11-10',
         note='2D 시험으로 먼저 가르기 · 단계 · 1저자 결정 · 판정 (11-13 갱신)'),
    dict(slug='dem-redesign-newcomer', track='suyoung', rel='webapp/static/explain/dem_redesign_plan_newcomer_20261110.html',
         title='DEM 재설계 (수영) 계획서 · 처음 보는 분을 위한 설명', date='2026-11-10',
         note='가압부터 탈압까지 한 모델로 계산하기 — 쉬운 말 판'),
    dict(slug='rint-overview', track='rint2', rel='webapp/static/explain/rint_overview_20261021.html',
         title='Rint 적용 현황', date='2026-10-21',
         note='무엇을 넣고, 어디서 막히나 — 아주 쉬운 설명 (11-03) + 자세한 기록'),
)

# ─────────────────────────────────────────────────────────────────────────
# 3) 보고서로 올리지 않는 HTML — 규칙 · 사유 (시험이 리포 HTML 전부를 이 표 · 위 표로 나눈다)
# ─────────────────────────────────────────────────────────────────────────
#: 훑는 범위 밖 — Jinja 틀 (단독 HTML 이 아니다 · 앱이 그려서 낸다).
SKIP_PREFIXES = ('webapp/templates/',)
NOT_REPORTS = (
    dict(kind='dir', prefix='docs/reviews/', part='evidence',
         why='증거 폴더 — Codex · 우리 탐침이 떠 둔 웹앱 화면 사본 · 출력 (보고서 아님)'),
    dict(kind='file', rel='docs/reviews/review_before_after.html',
         why='원장에서 요청마다 다시 그리는 화면 (/ledger/before-after · 사이드바 비포 / 애프터) 의 커밋 사본 — 원장보다 늦을 수 있어 올리지 않는다'),
    dict(kind='file', rel='scripts/_review_page_css.html',
         why='비포 / 애프터 생성기의 CSS 조각 — 단독 문서가 아니다'),
    dict(kind='file', rel='docs/50kg/report_y4/meeting_20261104/tools/stress_prerelax/render.html',
         why='3D 응력 그림을 그리는 렌더 틀 (글 없음 · 도구)'),
    dict(kind='file', rel='webapp/static/dem_method_figs/index.html',
         why='그림 · 자료 받기 화면 — 사이드바 트랙 묶음 50kg (후막) 아래 화면 줄로 연다 (11-25 · 일반 줄은 뺐다) · 보기 틀에서는 json · txt · md 받기 링크가 막힌다 (자산 규칙 밖)'),
)

TRACKS_BY_SLUG = {t['slug']: t for t in TRACKS}
REPORTS_BY_SLUG = {r['slug']: r for r in REPORTS}


def badge(t: dict):
    """트랙 배지 — 표에 등록된 화면 · 보고서 수만 센다 ('페이지 n · 보고서 m').  0 인 칸은 안 쓰고, 둘 다 0 이면 None (배지 없음)."""
    n = len(t.get('pages') or ())
    m = sum(1 for r in REPORTS if r.get('track') == t.get('slug'))
    bits = ([f'페이지 {n}'] if n else []) + ([f'보고서 {m}'] if m else [])
    return ' · '.join(bits) or None


def track_label(slug: str) -> str:
    """보고서 줄에 적을 트랙 이름 — 무리가 있으면 '[DEM 우선] Ⓐ …' 꼴.  표에 없으면 slug 그대로 (지어내지 않는다)."""
    t = TRACKS_BY_SLUG.get(slug)
    if not t:
        return slug
    return f"{t['group']} {t['name']}" if t.get('group') else t['name']


def sidebar(path: str = '', active: str = '') -> dict:
    """base.html 이 받는 토글 묶음 — 트랙 줄 + 화면 줄 (켜짐) + 토글을 열지.

    켜짐: 화면에 active 가 있으면 옛 사이드바와 같은 규칙 (active 값이 같으면) · 없으면 주소가 같을 때.
    열림: 지금 화면 (path · active) 이 토글 안 화면이면 열린 채로 보낸다 (JS 없이 · 접힘 기억 없음)."""
    rows, any_on, seen_group = [], False, set()
    for t in TRACKS:
        pg = []
        for p in (t.get('pages') or ()):
            on = bool((p.get('active') and active and p['active'] == active) or (path and p['url'] == path))
            any_on = any_on or on
            pg.append(dict(p, on=on))
        g = t.get('group')
        head = g if (g and g not in seen_group) else None
        if g:
            seen_group.add(g)
        rows.append(dict(slug=t['slug'], name=t['name'], group_head=head, what=t.get('what') or '',
                         href=f"/reports#track-{t['slug']}", badge=badge(t), pages=pg))
    return dict(ok=True, n=len(TRACKS), open=any_on, tracks=rows)


def report_file(slug: str, root=None, table=None):
    """표에 있는 보고서의 파일 경로 (Path) — 표에 없거나 파일이 없으면 None."""
    tbl = REPORTS_BY_SLUG if table is None else table
    r = tbl.get(slug)
    if not r:
        return None
    p = Path(root or ROOT) / r['rel']
    return p if p.is_file() else None


def report_info(r: dict, root=None) -> dict:
    """화면에 싣는 한 줄 — 표 값 + 파일 실재 · 크기 (KB) · sha256 앞 16 자리 · 원본 · 내려받기 주소 · 옛 판 실재."""
    base = Path(root or ROOT)
    p = base / r['rel']
    info = dict(r, ok=p.is_file(), track_label=track_label(r.get('track', '')),
                raw=f"/reports/{r['slug']}/raw", download=f"/reports/{r['slug']}/raw?download=1",
                earlier=[dict(e, ok=(base / e['rel']).is_file()) for e in (r.get('earlier') or ())])
    if info['ok']:
        b = p.read_bytes()
        info['sha16'] = hashlib.sha256(b).hexdigest()[:16]
        info['kb'] = max(1, round(len(b) / 1024))
    return info


def reports_page(root=None) -> dict:
    """/reports 화면 — 트랙 표 (배지 · 화면 · 딸린 보고서) + 보고서 표 (날짜 내림차순)."""
    infos = [report_info(r, root) for r in REPORTS]
    by_track = {}
    for i in infos:
        by_track.setdefault(i.get('track'), []).append(i)
    tracks = [dict(slug=t['slug'], label=track_label(t['slug']), what=t.get('what') or '', badge=badge(t),
                   pages=list(t.get('pages') or ()), reports=by_track.get(t['slug'], [])) for t in TRACKS]
    return dict(tracks=tracks, reports=sorted(infos, key=lambda i: i.get('date') or '', reverse=True))


def asset_file(slug: str, name: str, root=None, table=None):
    """보고서 폴더 안의 자산 파일 (Path · resolve 된 것) 또는 None.

    None = 표에 없는 slug · 허용 밖 확장자 (HTML 포함) · 빈 · 점 · 숨은 마디 (. 으로 시작) · 역슬래시 · 폴더 밖 (심볼릭 링크로 나가는 것 포함) ·
    없는 파일.  ⚠ 호출하는 쪽은 None 을 404 로 낸다 (왜 없는지는 밖에 말하지 않는다)."""
    tbl = REPORTS_BY_SLUG if table is None else table
    r = tbl.get(slug)
    if not r or not isinstance(name, str) or not name.lower().endswith(ASSET_EXT):
        return None
    if '\\' in name or '\x00' in name:
        return None
    parts = name.split('/')
    if any(x in ('', '.', '..') or x.startswith('.') for x in parts):
        return None
    folder = (Path(root or ROOT) / r['rel']).parent.resolve()
    p = (folder / name).resolve()
    try:
        p.relative_to(folder)
    except ValueError:
        return None
    return p if p.is_file() else None


def excluded_reason(rel: str):
    """NOT_REPORTS 의 사유 (첫 규칙) 또는 None.  dir 규칙 = prefix 아래 · 폴더 마디 이름에 part 가 든 것 (파일 이름은 안 본다)."""
    for x in NOT_REPORTS:
        if x['kind'] == 'file' and rel == x['rel']:
            return x['why']
        if x['kind'] == 'dir' and rel.startswith(x['prefix']):
            dirs = rel[len(x['prefix']):].split('/')[:-1]
            if any(x['part'] in d for d in dirs):
                return x['why']
    return None


def classify(rels) -> dict:
    """리포 상대 HTML 경로 목록 → dict(registered · excluded [(rel, 사유)] · unlisted · skipped (틀 폴더)).  시험이 쓴다."""
    reg = {r['rel'] for r in REPORTS}
    out = dict(registered=[], excluded=[], unlisted=[], skipped=[])
    for rel in sorted(set(rels)):
        if rel.startswith(SKIP_PREFIXES):
            out['skipped'].append(rel)
        elif rel in reg:
            out['registered'].append(rel)
        else:
            why = excluded_reason(rel)
            if why:
                out['excluded'].append((rel, why))
            else:
                out['unlisted'].append(rel)
    return out
