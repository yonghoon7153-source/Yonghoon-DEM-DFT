#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""트랙 묶음 회귀 — 사이드바 '공유 보고서' 줄 + 접힘 토글 '트랙 페이지 N' · /reports 목록 · 보고서 보기 (iframe + 여백 메모 · 형광펜) ·
원본 · 내려받기 (1저자 11-25 *"이렇게 독립적인 우리 분야들 있잖아 이렇게 토글로 묶고 이렇게 안에서 html 나 웹페이지 등 킬 수 있게 해줘"*).

표 하나 = `webapp/track_pages.py` (TRACKS · REPORTS · NOT_REPORTS) — 사이드바 · /reports · 이 시험이 같은 표를 본다 (사본 금지).
이 시험이 지키는 것:

  ① 표 — 트랙 순서 = 용훈 포메이션 ① (Rint ② → DEM 우선 Ⓐ Ⓑ Ⓒ → DEM 우선 (수영) → LHS 접촉망 · LHS DEM 런 · 50kg · 이종기술) ·
     slug 유일 · 보고서 track = 표의 트랙 · rel 실재 · 제목 = 파일 <title> · 날짜 꼴 · 파일 이름 날짜 = 표 날짜 · 화면 링크 200
  ② 훑기 — git 이 아는 HTML (틀 폴더 webapp/templates 밖) 이 전부 '등록' 또는 '사유 있는 제외' · 규칙마다 실재 · Codex 증거 폴더 = 제외
  ③ 라우트 — /reports · /reports/<slug> 200 · raw = 파일 바이트 · ?download=1 = attachment · 없는 slug 404 ·
     자산 = 보고서가 상대 경로로 부르는 그림 · 자료가 200 · html · 폴더 밖 · 숨은 이름 · 허용 밖 확장자 404 · 심볼릭 링크 밖 = 거부
  ④ 사이드바 — '공유 보고서' 줄 (토글 밖 · 바로 앞) + <details> 토글 '트랙 페이지 N' · 트랙 N 줄 · 배지 = 표에서 센 수 ·
     화면 없는 트랙 = '화면 없음' · 옮긴 줄 (Rint 설명 · DEM 재설계 계획서 (수영) · MPM 설명 · Q&A · 믹서 · 이종기술) = 토글 안 · URL 그대로 ·
     일반 줄 = 토글 밖 · 순서 그대로 · 지금 화면이 토글 안이면 열림 · JS 없음 · 표를 못 읽으면 '못 읽었다' (빈 줄로 숨기지 않는다)
  ⑤ 보기 화면 — iframe = raw · docnote.js · 메모 저장 = 이 브라우저 (localStorage) · 파일이 없으면 '파일 없음' (빼지 않는다)
  ⑥ 묶음 규칙 — app.py 는 track_pages 를 함수 안에서만 import (import 직후 sys.modules 에 없다) · 194 실행기 지연 import 표 한 줄 ·
     분류 밖 0 · base.html 에 옮긴 줄 주소를 손으로 적지 않는다 · 게이트 · CI 한 단계 · docnote.js = 서버 저장 없음 · 문법 · CSS

  python3 webapp/test_track_reports.py
"""
import hashlib
import html as _html
import importlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / 'scripts'))

BASE = HERE / 'templates' / 'base.html'
APP = HERE / 'app.py'
CSS = HERE / 'static' / 'css' / 'style.css'
DOCNOTE = HERE / 'static' / 'js' / 'docnote.js'
TPL_LIST = HERE / 'templates' / 'reports.html'
TPL_VIEW = HERE / 'templates' / 'report.html'
MOD = HERE / 'track_pages.py'

#: 트랙 순서 = CLAUDE.md '용훈 포메이션' ① (이 시험이 따로 적는 기대 — 표를 베끼지 않는다).
FORMATION = ['[Rint ②]', 'Ⓐ DEM 신뢰성', 'Ⓑ DEM → MPM 연계', 'Ⓒ 코팅 활물질 믹싱', '[DEM 우선 (수영)]',
             'LHS 접촉망', 'LHS DEM 런', '50kg (후막)', '이종기술']
#: 토글 안으로 옮긴 트랙 전용 줄 — 옛 사이드바의 URL · 글 그대로 (즐겨찾기가 안 깨지게).
MOVED = [('/hetero', '이종기술'), ('/mixer', '믹서 (이력 · 침대)'),
         ('/static/explain/rint_overview_20261021.html', 'Rint 설명'),
         ('/static/explain/dem_redesign_plan_20261110.html', 'DEM 재설계 계획서 (수영)'),
         ('/static/explain/mpm_basics_20261116.html', 'MPM 설명 · Q&amp;A')]
#: 제자리에 남는 일반 도구 줄 — 옛 사이드바 순서 그대로.
GENERAL = [('/', 'Dashboard'), ('/group', 'Group 비교'), ('/archive', '보관함'), ('/mpm-lab', 'MPM 뷰어'),
           ('/step5', 'STEP5 열화'), ('/eis', 'EIS / DRT'), ('/emod', '유효 영률 · 응력'), ('/predictor', 'ML Predictor'),
           ('/litdb', '논문 litdb'), ('/seminar', '연구 세미나'), ('/worklog', '작업일지 · 주간보고'), ('/videos', '영상 (AVI)'),
           ('/static/dem_method_figs/index.html', 'DEM 방법 그림 (2D)'), ('/audit', 'Trust Audit'), ('/ledger', '판정 원장'),
           ('/ledger/before-after', '비포 / 애프터')]
#: 지금 화면이 토글 안 화면이면 토글이 열린 채로 와야 하는 주소 · 닫힌 채로 와야 하는 주소.
OPEN_ON = ['/mixer', '/mixer/story', '/mixer/lit', '/hetero', '/hetero/transcript']
CLOSED_ON = ['/seminar', '/reports', '/worklog']
SLUG_RE = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*')
DATE_RE = re.compile(r'(\d{4})-(\d{2})-(\d{2})')
RE_ABS = re.compile(r'(?:/home/|/root/|/tmp/|/mnt/|/Users/|[A-Za-z]:\\)')
RE_ADDR = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b|[\w.+-]+@[\w-]+\.[\w.]+')
HANGUL = re.compile(r'[가-힣]')

_ok, _fail = 0, []


def chk(name, cond):
    global _ok
    try:
        v = bool(cond() if callable(cond) else cond)
    except Exception as e:                       # noqa: BLE001 — 검사 자체가 죽으면 그 칸은 실패로 센다 (조용히 넘기지 않는다)
        v = False
        name = f'{name}  (검사 중 {type(e).__name__}: {e})'
    if v:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}')
    return v


def _read(p):
    try:
        return Path(p).read_text(encoding='utf-8')
    except OSError:
        return ''


def _title_of(p):
    m = re.search(r'<title[^>]*>(.*?)</title>', _read(p), re.S | re.I)
    return re.sub(r'\s+', ' ', _html.unescape(m.group(1))).strip() if m else None


def _sidebar(html):
    m = re.search(r'<nav class="sidebar"[^>]*>(.*?)</nav>', html, re.S)
    return m.group(1) if m else ''


def _split_toggle(side):
    """사이드바 → (토글 <details> 블록, 토글을 뺀 나머지)."""
    m = re.search(r'<details\b[^>]*class="[^"]*\bnav-subfold\b[^"]*"[^>]*>.*?</details>', side, re.S)
    if not m:
        return '', side
    return m.group(0), side[:m.start()] + side[m.end():]


def _link_text(html, url):
    m = re.search(r'<a href="%s"[^>]*>(.*?)</a>' % re.escape(url), html, re.S)
    return _html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', m.group(1))).strip()) if m else None


def _git_html():
    """git 이 아는 .html · .htm (리포 상대 · 틀 폴더 포함 — 분류는 표가 한다).  git 을 못 쓰면 None (빈 목록과 구분)."""
    try:
        out = subprocess.run(['git', 'ls-files', '-z', '--', '*.html', '*.htm'], cwd=str(ROOT),
                             capture_output=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    return sorted(x for x in out.stdout.decode('utf-8', 'replace').split('\0') if x)


def _rel_refs(src):
    """보고서 HTML 이 상대 경로로 부르는 것 (src · href) — 조각 (#) · 절대 (/) · 바깥 (scheme:) · data: 는 뺀다."""
    out = []
    for v in re.findall(r'''(?:src|href)\s*=\s*["']([^"']+)["']''', src):
        v = _html.unescape(v).split('#')[0].split('?')[0]
        if not v or v.startswith(('/', '#')) or re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', v):
            continue
        out.append(v)
    return sorted(set(out))


def main():
    print('── ⓪ 앱 import — track_pages 는 함수 안에서만 (import 직후 sys.modules 에 없어야 한다)')
    try:
        import app as webapp
    except Exception as e:                       # noqa: BLE001
        print(f'        (앱 import 실패: {type(e).__name__}: {e})')
        webapp = None
    chk('app import 성공', webapp is not None)
    chk('app import 직후 track_pages 가 아직 안 실렸다 (모듈 수준 import 없음 · 194 워커 경로 밖)',
        webapp is not None and 'track_pages' not in sys.modules)
    c = webapp.app.test_client() if webapp else None

    print('── ① 표 (webapp/track_pages.py)')
    try:
        import track_pages as T
    except Exception as e:                       # noqa: BLE001
        print(f'        (track_pages import 실패: {type(e).__name__}: {e})')
        T = None
    chk('track_pages import · TRACKS · REPORTS · NOT_REPORTS 가 있다',
        T is not None and all(hasattr(T, k) for k in ('TRACKS', 'REPORTS', 'NOT_REPORTS')))
    tracks = list(getattr(T, 'TRACKS', ()) or ())
    reports = list(getattr(T, 'REPORTS', ()) or ())
    t_slugs = [t.get('slug') for t in tracks]
    chk(f'트랙 순서 = 용훈 포메이션 ① ({len(FORMATION)} 트랙)', [t.get('name') for t in tracks] == FORMATION)
    chk('Ⓐ Ⓑ Ⓒ 의 무리 = [DEM 우선] · 다른 트랙은 무리 없음',
        len(tracks) == len(FORMATION)
        and [t.get('group') for t in tracks] == [None, '[DEM 우선]', '[DEM 우선]', '[DEM 우선]', None, None, None, None, None])
    chk('트랙 slug 유일 · 꼴 (소문자 · 숫자 · 하이픈)', bool(t_slugs) and len(set(t_slugs)) == len(t_slugs)
        and all(isinstance(s, str) and SLUG_RE.fullmatch(s) for s in t_slugs))
    chk('트랙마다 한 줄 (what) = 한국어 · 80 자 이하', bool(tracks) and all(
        isinstance(t.get('what'), str) and HANGUL.search(t['what']) and len(t['what']) <= 80 for t in tracks))
    pages = [(t.get('slug'), p) for t in tracks for p in (t.get('pages') or ())]
    urls = [p.get('url') for _s, p in pages]
    chk('화면 링크 주소 유일 (한 화면 = 한 트랙)', bool(urls) and len(set(urls)) == len(urls))
    chk('화면마다 label · icon · url (/ 로 시작)', bool(pages) and all(
        p.get('label') and p.get('icon') and isinstance(p.get('url'), str) and p['url'].startswith('/') for _s, p in pages))
    for url, label in MOVED:
        lab = _html.unescape(label)
        chk(f'옮긴 줄이 표에 있다 — {lab} ({url}) · 글 그대로', any(p.get('url') == url and p.get('label') == lab for _s, p in pages))
    no_page = [t.get('name') for t in tracks if not (t.get('pages') or ())]
    print(f'        화면 없는 트랙: {no_page}')
    chk('화면 없는 트랙은 줄을 남긴다 (표에서 빼지 않는다)', len(tracks) == len(FORMATION))
    for _s, p in pages:
        r = c.get(p['url']) if c else None
        chk(f'화면 GET {p["url"]} → 200', r is not None and r.status_code == 200)
        if r is not None:
            r.close()

    r_slugs = [r.get('slug') for r in reports]
    chk('보고서가 하나 이상 · slug 유일 · 꼴', bool(r_slugs) and len(set(r_slugs)) == len(r_slugs)
        and all(isinstance(s, str) and SLUG_RE.fullmatch(s) for s in r_slugs))
    chk('보고서 slug 가 예약 낱말 (raw) 이 아니다', 'raw' not in r_slugs)
    for r in reports:
        sl, rel = r.get('slug'), r.get('rel') or ''
        p = ROOT / rel
        chk(f'[{sl}] track = 표의 트랙', r.get('track') in t_slugs)
        chk(f'[{sl}] rel = 리포 안 .html 파일 ({rel})', rel.endswith('.html') and not rel.startswith('/') and '..' not in rel and p.is_file())
        chk(f'[{sl}] rel 이 틀 폴더 · 증거 폴더 밖', not rel.startswith('webapp/templates/') and 'evidence' not in rel)
        t = _title_of(p)
        chk(f'[{sl}] 제목 = 파일 <title> ({t!r})', t is not None and r.get('title') == t)
        m = DATE_RE.fullmatch(r.get('date') or '')
        chk(f'[{sl}] 날짜 꼴 YYYY-MM-DD ({r.get("date")})', bool(m) and 1 <= int(m.group(2)) <= 12 and 1 <= int(m.group(3)) <= 31)
        fm = re.search(r'(20\d{6})', Path(rel).name)
        chk(f'[{sl}] 파일 이름 날짜 = 표 날짜', fm is None or (r.get('date') or '').replace('-', '') == fm.group(1))
        chk(f'[{sl}] note = 글 (빈 값이면 줄 없음)', isinstance(r.get('note', ''), str))
        chk(f'[{sl}] earlier = 실재하는 옛 판 (label · rel)', all(e.get('label') and (ROOT / (e.get('rel') or '')).is_file()
                                                            for e in (r.get('earlier') or ())))

    if T is not None and hasattr(T, 'badge'):
        for t in tracks:
            n = len(t.get('pages') or ())
            m_ = sum(1 for r in reports if r.get('track') == t.get('slug'))
            want = ' · '.join(x for x in ((f'페이지 {n}' if n else ''), (f'보고서 {m_}' if m_ else '')) if x) or None
            chk(f'배지 [{t.get("name")}] = 표에서 센 수 ({want})', T.badge(t) == want)
    else:
        chk('배지 함수 track_pages.badge 가 있다', False)

    print('── ② 훑기 — git 이 아는 HTML 이 전부 등록 또는 사유 있는 제외')
    files = _git_html()
    chk('git ls-files 로 HTML 목록을 읽었다 (못 읽음 ≠ 없음)', files is not None and len(files) > 0)
    files = files or []
    cl = T.classify(files) if T is not None and hasattr(T, 'classify') else None
    chk('track_pages.classify 가 (registered · excluded · unlisted · skipped) 를 낸다',
        isinstance(cl, dict) and all(k in cl for k in ('registered', 'excluded', 'unlisted', 'skipped')))
    cl = cl if isinstance(cl, dict) else dict(registered=[], excluded=[], unlisted=list(files), skipped=[])
    print(f'        훑은 HTML {len(files)} · 등록 {len(cl["registered"])} · 제외 {len(cl["excluded"])} · '
          f'틀 폴더 {len(cl["skipped"])} · 표 밖 {len(cl["unlisted"])}')
    for rel, why in cl['excluded']:
        print(f'        제외: {rel}  ← {why}')
    chk(f'표 밖 HTML 0 개 (새 HTML 은 REPORTS 또는 NOT_REPORTS 에) {cl["unlisted"]}', not cl['unlisted'])
    chk('넷으로 빈틈 · 겹침 없이 나뉜다', sorted(cl['registered'] + [x for x, _ in cl['excluded']] + cl['unlisted'] + cl['skipped'])
        == sorted(files) and len(set(cl['registered']) & {x for x, _ in cl['excluded']}) == 0)
    chk('등록 = REPORTS 의 rel 전부 (git 이 아는 파일)', sorted(cl['registered']) == sorted(r.get('rel') for r in reports))
    chk('제외마다 사유 = 한국어 글', all(isinstance(w, str) and HANGUL.search(w) for _x, w in cl['excluded']))
    codex_ev = [f for f in files if re.match(r'docs/reviews/codex_[^/]*evidence[^/]*/', f)]
    chk(f'Codex 증거 폴더 HTML ({len(codex_ev)}) = 전부 규칙으로 제외', bool(codex_ev) and set(codex_ev) <= {x for x, _ in cl['excluded']})
    rules = list(getattr(T, 'NOT_REPORTS', ()) or ())
    chk('제외 규칙 꼴 = (kind file · rel) 또는 (kind dir · prefix · part) + why', bool(rules) and all(
        (r.get('kind') == 'file' and r.get('rel')) or (r.get('kind') == 'dir' and r.get('prefix') and r.get('part')) for r in rules)
        and all(isinstance(r.get('why'), str) and HANGUL.search(r['why']) for r in rules))
    for r in rules:
        if r.get('kind') == 'file':
            chk(f'파일 규칙의 rel 이 git 이 아는 파일이다 (낡은 규칙 없음) — {r.get("rel")}', r.get('rel') in files)
        else:
            hit = [f for f in files if T.excluded_reason(f) == r.get('why')] if T is not None else []
            chk(f'폴더 규칙이 실제로 하나 이상 잡는다 — {r.get("prefix")}…{r.get("part")}… ({len(hit)})', len(hit) >= 1)
    chk('틀 폴더 (webapp/templates) 만 범위 밖', all(f.startswith('webapp/templates/') for f in cl['skipped']))

    print('── ③ 라우트 — 목록 · 보기 · 원본 · 내려받기 · 자산')
    r = c.get('/reports') if c else None
    lst = r.get_data(as_text=True) if r is not None else ''
    chk('GET /reports → 200 · text/html', r is not None and r.status_code == 200 and (r.mimetype or '') == 'text/html')
    chk('목록에 트랙 이름 전부', bool(tracks) and all(_html.escape(t['name']) in lst for t in tracks))
    chk('목록 트랙 표에 줄마다 id="track-<slug>" (사이드바 트랙 줄이 여기로 온다)',
        bool(tracks) and all(f'id="track-{t["slug"]}"' in lst for t in tracks))
    chk(f'목록 트랙 표에 화면 없는 트랙마다 "화면 없음" ({len(no_page)})', bool(no_page) and all(
        re.search(r'id="track-%s".*?화면 없음.*?</tr>' % re.escape(t['slug']), lst, re.S) for t in tracks if not t.get('pages')))
    for t in tracks:
        for p in (t.get('pages') or ()):
            chk(f'목록 트랙 표에 화면 링크 — {p["label"]}', f'href="{p["url"]}"' in lst)
    for rp in reports:
        sl = rp['slug']
        b = (ROOT / rp['rel']).read_bytes() if (ROOT / rp['rel']).is_file() else b''
        sha16 = hashlib.sha256(b).hexdigest()[:16]
        chk(f'[{sl}] 목록에 제목 · 보기 링크 · 날짜', _html.escape(rp['title']) in lst and f'href="/reports/{sl}"' in lst and rp['date'] in lst)
        chk(f'[{sl}] 목록에 원본 sha16 · 새 탭 · 내려받기', sha16 in lst and f'href="/reports/{sl}/raw"' in lst
            and f'href="/reports/{sl}/raw?download=1"' in lst)
        v = c.get(f'/reports/{sl}') if c else None
        vh = v.get_data(as_text=True) if v is not None else ''
        chk(f'[{sl}] GET /reports/{sl} → 200', v is not None and v.status_code == 200)
        chk(f'[{sl}] 보기 = iframe src = 원본 · docnote.js · 메모 자리 (rel)',
            f'src="/reports/{sl}/raw"' in vh and '/static/js/docnote.js' in vh and rp['rel'] in vh)
        chk(f'[{sl}] 보기에 저장 자리 안내 (이 브라우저에만) · 원본 · 내려받기 단추', '이 브라우저에만' in vh
            and f'href="/reports/{sl}/raw"' in vh and f'href="/reports/{sl}/raw?download=1"' in vh)
        w = c.get(f'/reports/{sl}/raw') if c else None
        chk(f'[{sl}] 원본 200 · text/html · 바이트 = 파일', w is not None and w.status_code == 200
            and (w.mimetype or '') == 'text/html' and w.get_data() == b and bool(b))
        chk(f'[{sl}] 원본은 받기 아님 (inline)', w is not None and 'attachment' not in (w.headers.get('Content-Disposition') or ''))
        d = c.get(f'/reports/{sl}/raw?download=1') if c else None
        cd = (d.headers.get('Content-Disposition') or '') if d is not None else ''
        chk(f'[{sl}] 내려받기 = attachment · 파일 이름 · 바이트 같음', d is not None and d.status_code == 200 and 'attachment' in cd
            and Path(rp['rel']).name in cd and d.get_data() == b)
        for x in (v, w, d):
            if x is not None:
                x.close()
        src = b.decode('utf-8', 'replace')
        refs = _rel_refs(src)
        okext = tuple(getattr(T, 'ASSET_EXT', ()) or ())
        bad = [x for x in refs if not x.lower().endswith(okext)]
        chk(f'[{sl}] 상대 참조가 전부 자산 규칙 안 (보기 틀에서 안 깨진다) {bad}', bool(okext) and not bad)
        for x in refs:
            if x.lower().endswith(okext):
                a = c.get(f'/reports/{sl}/{x}') if c else None
                want = (ROOT / rp['rel']).parent / x
                chk(f'[{sl}] 자산 {x} → 200 · 바이트 같음', a is not None and a.status_code == 200 and want.is_file()
                    and a.get_data() == want.read_bytes())
                if a is not None:
                    a.close()
        own = Path(rp['rel']).name
        bad_names = [own, own.upper(), own[:-5] + '.htm', '../' + own, '..%2f' + own, '%2e%2e/%2e%2e/webapp/app.py',
                     '../../../webapp/app.py', 'x/../../' + own, '.hidden.png', 'nope_not_here.png', 'a\\b.png',
                     '../../../CLAUDE.md', 'README.md', 'x.py', 'x.json', 'x.js']
        for nm in bad_names:
            a = c.get(f'/reports/{sl}/{nm}') if c else None
            chk(f'[{sl}] 자산 거부 {nm!r} → 404', a is not None and a.status_code == 404)
            if a is not None:
                a.close()
    sibling = [(a, b_) for a in reports for b_ in reports if a is not b_
               and Path(a['rel']).parent == Path(b_['rel']).parent]
    if sibling:
        a, b_ = sibling[0]
        x = c.get(f'/reports/{a["slug"]}/{Path(b_["rel"]).name}') if c else None
        chk(f'같은 폴더의 다른 보고서 HTML 도 자산 경로로는 안 낸다 ({a["slug"]} → {Path(b_["rel"]).name}) → 404',
            x is not None and x.status_code == 404)
    for path in ('/reports/no-such-report', '/reports/no-such-report/raw', '/reports/no-such-report/x.png',
                 '/reports/RINT-OVERVIEW', '/reports/raw'):
        x = c.get(path) if c else None
        chk(f'없는 slug {path} → 404', x is not None and x.status_code == 404)

    print('── ③b 자산 해석 함수 — 심볼릭 링크로 폴더 밖 = 거부 (임시 뿌리)')
    if T is not None and hasattr(T, 'asset_file'):
        td = Path(tempfile.mkdtemp(prefix='trk_'))
        try:
            (td / 'rep').mkdir()
            (td / 'rep' / 'r.html').write_text('<title>x</title>', encoding='utf-8')
            (td / 'rep' / 'ok.png').write_bytes(b'\x89PNG')
            (td / 'outside.png').write_bytes(b'\x89PNG')
            (td / 'rep' / '.secret.png').write_bytes(b'\x89PNG')
            (td / 'rep' / 'sub').mkdir()
            (td / 'rep' / 'sub' / 'f.svg').write_text('<svg/>', encoding='utf-8')
            os.symlink(td / 'outside.png', td / 'rep' / 'link.png')
            os.symlink(td, td / 'rep' / 'up')
            tbl = {'tmp': dict(slug='tmp', rel='rep/r.html')}
            chk('임시 뿌리 — 폴더 안 그림 = 경로', T.asset_file('tmp', 'ok.png', root=td, table=tbl) == (td / 'rep' / 'ok.png').resolve())
            chk('임시 뿌리 — 아래 폴더의 svg = 경로', T.asset_file('tmp', 'sub/f.svg', root=td, table=tbl) == (td / 'rep' / 'sub' / 'f.svg').resolve())
            chk('⛔ 숨은 이름 (.secret.png · 파일이 있어도) → None', T.asset_file('tmp', '.secret.png', root=td, table=tbl) is None)
            chk('⛔ 심볼릭 링크가 폴더 밖 파일 → None', T.asset_file('tmp', 'link.png', root=td, table=tbl) is None)
            chk('⛔ 심볼릭 링크 폴더를 지나 밖 → None', T.asset_file('tmp', 'up/outside.png', root=td, table=tbl) is None)
            chk('⛔ html → None', T.asset_file('tmp', 'r.html', root=td, table=tbl) is None)
            chk('⛔ 표에 없는 slug → None', T.asset_file('nope', 'ok.png', root=td, table=tbl) is None)
        finally:
            shutil.rmtree(td, ignore_errors=True)
    else:
        chk('자산 해석 함수 track_pages.asset_file 가 있다', False)

    print('── ④ 사이드바 — 공유 보고서 줄 + 토글 트랙 페이지 N')
    pages_html = {}
    for path in OPEN_ON + CLOSED_ON:
        x = c.get(path) if c else None
        pages_html[path] = x.get_data(as_text=True) if (x is not None and x.status_code == 200) else ''
        chk(f'GET {path} → 200 (사이드바를 그린다)', x is not None and x.status_code == 200)
    side = _sidebar(pages_html.get('/seminar', ''))
    tog, rest = _split_toggle(side)
    chk('사이드바에 접힘 토글 <details class="nav-subfold"> 하나', side.count('<details') == 1 and bool(tog))
    sm = re.search(r'<summary[^>]*>(.*?)</summary>', tog, re.S)
    sm_t = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', sm.group(1))).strip() if sm else ''
    chk(f'토글 머리 = "트랙 페이지 {len(FORMATION)}" ({sm_t!r})', sm_t == f'트랙 페이지 {len(FORMATION)}')
    rows = re.findall(r'<li class="nav-track"[^>]*>(.*?)</li>', tog, re.S)
    names = [re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', re.search(r'<span class="nav-tname">(.*?)</span>', x, re.S).group(1))).strip()
             if re.search(r'<span class="nav-tname">(.*?)</span>', x, re.S) else '' for x in rows]
    chk(f'토글 안 트랙 {len(FORMATION)} 줄 · 순서 = 용훈 포메이션 ① ({names})', [_html.unescape(n) for n in names] == FORMATION)
    chk('트랙 줄 링크 = /reports#track-<slug>', len(rows) == len(FORMATION) and all(
        f'href="/reports#track-{s}"' in x for s, x in zip(t_slugs, rows)) if t_slugs else False)
    chk('무리 머리 [DEM 우선] 한 번 (Ⓐ 앞)', tog.count('class="nav-tgroup"') == 1
        and tog.find('[DEM 우선]</li>') < tog.find('Ⓐ DEM 신뢰성') if '[DEM 우선]</li>' in tog else False)
    blocks = re.split(r'(?=<li class="nav-track")', tog)[1:]
    for t, blk in zip(tracks, blocks):
        n = len(t.get('pages') or ())
        if not n:
            chk(f'화면 없는 트랙 = "화면 없음" — {t["name"]}', '화면 없음' in blk and blk.count('<li class="nav-sub"') == 0)
        else:
            chk(f'트랙 {t["name"]} 밑 화면 {n} 줄', blk.count('<li class="nav-sub"') == n)
        if T is not None and hasattr(T, 'badge'):
            want = T.badge(t)
            chk(f'트랙 {t["name"]} 배지 = {want}', (want is None and 'nav-badge' not in blk.split('</li>')[0])
                or (want is not None and f'>{want}</span>' in blk))
    for url, label in MOVED:
        lab = _html.unescape(label)
        chk(f'옮긴 줄 = 토글 안 · URL 그대로 · 글 그대로 — {lab}', (_link_text(tog, url) or '').endswith(lab))
        chk(f'옮긴 줄이 토글 밖에 남지 않는다 — {lab}', f'href="{url}"' not in rest)
    pos = []
    for url, label in GENERAL:
        t_ = _link_text(rest, url)
        chk(f'일반 줄 = 토글 밖 · 제자리 — {label}', t_ is not None and t_.endswith(label))
        pos.append(rest.find(f'href="{url}"'))
    chk('일반 줄 순서 = 옛 순서 그대로', all(p >= 0 for p in pos) and pos == sorted(pos))
    rep_at = rest.find('href="/reports"')
    chk('"공유 보고서" 줄 = 토글 밖 · 글 "공유 보고서"', rep_at >= 0 and (_link_text(rest, '/reports') or '').endswith('공유 보고서'))
    chk('"공유 보고서" 줄이 토글 바로 앞 (같은 묶음 · 영상 (AVI) 뒤 · DEM 방법 그림 앞)',
        rep_at >= 0 and side.find('href="/reports"') < side.find('<details')
        and side.find('href="/videos"') < side.find('href="/reports"')
        and side.find('</details>') < side.find('href="/static/dem_method_figs/index.html"', side.find('</details>')))
    chk('토글에 JS 없음 (on…= 속성 · script 없음 · <details> 만)', bool(tog) and not re.search(r'\son[a-z]+\s*=', tog)
        and '<script' not in side)
    for path in OPEN_ON:
        tg, _r = _split_toggle(_sidebar(pages_html.get(path, '')))
        chk(f'지금 화면이 토글 안 ({path}) → 토글이 열린 채로 온다', bool(re.match(r'<details\b[^>]*\sopen\b', tg)))
    for path in CLOSED_ON:
        tg, _r = _split_toggle(_sidebar(pages_html.get(path, '')))
        chk(f'토글 밖 화면 ({path}) → 토글은 닫힌 채', bool(tg) and not re.match(r'<details\b[^>]*\sopen\b', tg))
    st = _sidebar(pages_html.get('/mixer/story', ''))
    chk('/mixer/story 에서 믹서 줄 활성 그대로 (href="/mixer" class="active") · 그 화면 줄도 활성',
        'href="/mixer" class="active"' in st and 'href="/mixer/story" class="active"' in st)
    rs = _sidebar(pages_html.get('/reports', ''))
    chk('/reports 에서 "공유 보고서" 줄 활성', 'href="/reports" class="active"' in rs)
    if T is not None and c is not None and hasattr(T, 'sidebar'):
        real = T.sidebar

        def boom(*_a, **_k):
            raise RuntimeError('시험용 고장')
        T.sidebar = boom
        try:
            x = c.get('/seminar')
            xs = _sidebar(x.get_data(as_text=True))
            chk('⛔ 표를 못 읽으면 사이드바에 "트랙 목록을 못 읽었다" (빈 줄로 숨기지 않는다) · 화면은 200',
                x.status_code == 200 and '트랙 목록을 못 읽었다' in xs and 'href="/reports"' in xs)
        finally:
            T.sidebar = real
    else:
        chk('track_pages.sidebar 가 있다 (fail-closed 시험)', False)

    print('── ⑤ 보기 화면 — 파일이 없으면 "파일 없음" (빼지 않는다)')
    if T is not None and reports and c is not None and hasattr(T, 'REPORTS_BY_SLUG'):
        sl = reports[0]['slug']
        ent = T.REPORTS_BY_SLUG[sl]
        old = ent['rel']
        ent['rel'] = 'webapp/static/explain/__no_such_report__.html'
        try:
            a = c.get('/reports')
            b_ = c.get(f'/reports/{sl}')
            w = c.get(f'/reports/{sl}/raw')
            chk('파일이 없는 보고서 — 목록 200 · 그 줄에 "파일 없음" (줄을 빼지 않는다)',
                a.status_code == 200 and re.search(r'id="row-%s".*?파일 없음' % re.escape(sl), a.get_data(as_text=True), re.S))
            chk('파일이 없는 보고서 — 보기 200 · "파일 없음" 안내 · iframe 없음',
                b_.status_code == 200 and '파일 없음' in b_.get_data(as_text=True) and '<iframe' not in b_.get_data(as_text=True))
            chk('파일이 없는 보고서 — 원본 404', w.status_code == 404)
        finally:
            ent['rel'] = old
    else:
        chk('보고서 표 (REPORTS_BY_SLUG) 로 파일 없음 시험', False)

    print('── ⑥ 묶음 규칙 — app.py · 194 실행기 · base.html · 게이트 · CI · docnote.js · CSS')
    app_src = _read(APP)
    chk('app.py 에 모듈 수준 import track_pages 없음 · 함수 안 import 있음',
        re.search(r'^(?:import|from) track_pages', app_src, re.M) is None
        and re.search(r'^\s+import track_pages', app_src, re.M) is not None)
    chk('app.py 에 보고서 파일 이름 · 트랙 주소를 손으로 적지 않는다 (표 = track_pages)',
        all(Path(r['rel']).name not in app_src for r in reports) and 'dem_method_figs' not in app_src)
    try:
        import run_network_194_parallel as NP
        lz = NP.DEP_LAZY_OFFPATH
        cen = NP.lazy_import_census()
    except Exception as e:                       # noqa: BLE001
        print(f'        (실행기 import 실패: {type(e).__name__}: {e})')
        lz, cen = {}, dict(unclassified=['?'])
    chk('194 실행기 지연 import 표에 (webapp/app.py, track_pages) 한 줄 · 사유', ('webapp/app.py', 'track_pages') in lz
        and HANGUL.search(lz.get(('webapp/app.py', 'track_pages'), '')))
    chk(f'지연 import 분류 밖 0 {cen.get("unclassified")}', cen.get('unclassified') == [])
    base = _read(BASE)
    chk('base.html 에 옮긴 줄 주소를 손으로 적지 않는다 (표에서 그린다)',
        all(f'href="{u}"' not in base for u, _l in MOVED))
    chk('base.html 이 표를 부른다 (TRACK_NAV) · 공유 보고서 줄 · 토글', 'TRACK_NAV' in base and 'href="/reports"' in base
        and 'nav-subfold' in base)
    gate = _read(ROOT / 'scripts' / 'check_all.sh')
    chk('게이트 (scripts/check_all.sh) 에 이 시험 단계 한 줄',
        len(re.findall(r"(?m)^run 'webapp: track_reports[^']*'\s+python3 webapp/test_track_reports\.py", gate)) == 1)
    ci = _read(ROOT / '.github' / 'workflows' / 'discipline.yml')
    chk('CI (discipline.yml) 에 이 시험 단계 한 줄', len(re.findall(r'(?m)^\s+run: python webapp/test_track_reports\.py\s*$', ci)) == 1)
    js = _read(DOCNOTE)
    chk('docnote.js 가 있다 · mountDocNotes · localStorage', 'mountDocNotes' in js and 'localStorage' in js)
    chk('docnote.js 에 서버 저장 없음 (fetch · /api/comments · /api/highlights 없음)',
        bool(js) and 'fetch(' not in js and '/api/comments' not in js and '/api/highlights' not in js)
    node = shutil.which('node')
    if node:
        rr = subprocess.run([node, '--check', str(DOCNOTE)], capture_output=True, text=True)
        chk('docnote.js 문법 (node --check)', DOCNOTE.is_file() and rr.returncode == 0)
    else:
        print('  SKIP  node 없음 — docnote.js 문법 검사를 건너뜀 (세지 않는다)')
    css = _read(CSS)
    chk('style.css 에 여백 메모 격자 (.dn-host.dnote-on) · 카드 · 형광 · 사이드바 토글',
        '.dn-host.dnote-on' in css and '.dn-card' in css and 'mark.dn-pen' in css and '.nav-subfold' in css)
    chk('style.css 사이드바 목록이 길면 그 안에서 굴린다 (overflow-y)', re.search(r'\.nav-links\s*\{[^}]*overflow-y:\s*auto', css) is not None)
    depth, stray = 0, 0
    for ch in re.sub(r'/\*.*?\*/', '', css, flags=re.S):
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth < 0:
                stray, depth = stray + 1, 0
    chk(f'style.css 괄호 짝 (남는 }} 없음 · 끝 깊이 0) — 짝이 어긋나면 뒤 규칙이 @media 안에 빨려 든다 ({stray} · {depth})',
        bool(css) and stray == 0 and depth == 0)
    for p in (MOD, TPL_LIST, TPL_VIEW, DOCNOTE):
        s = _read(p)
        chk(f'{p.relative_to(ROOT)} 에 홈 경로 · 주소 · 계정 없음', bool(s) and not RE_ABS.search(s) and not RE_ADDR.search(s))

    print(f'\n== test_track_reports: {_ok}/{_ok + len(_fail)} PASS')
    if _fail:
        print('   실패: ' + ' · '.join(_fail[:40]) + (' …' if len(_fail) > 40 else ''))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
