#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DEM 방법 그림 (2D) 페이지 회귀 — 웹앱 정적 페이지 + 사이드바 링크 + 내려받기
(1저자 11-01 *"2d로 지금 그림 넣은것들 webapp에 넣고 뽑을거야"*).

`webapp/app.py` 는 봉인 32 (`scripts/run_network_194_parallel.py` CODE_FILES) 라 라우트를 새로 만들 수 없다.
그래서 Rint 설명 페이지와 같은 길로 간다 — Flask 기본 정적 폴더 (`webapp/static/dem_method_figs/`) 에 페이지와
그림 사본 (`files/`) 을 두고, 사이드바 (`templates/base.html` · 봉인 밖) 에서 링크한다.  사본은
`scripts/sync_dem_method_figs_to_webapp.py` 가 원본 (`docs/50kg/report_y4/figs/p0_dem_method/`) 에서 복사하고
`--check` 가 바이트 대조한다.  이 시험이 지키는 것:

  ① 페이지 파일이 그 자리에 있고 한 파일로 닫혀 있다 (스크립트 · 외부 자원 없음 · 태그 짝) · 웹앱으로 돌아가는 링크
  ② 실제 앱이 페이지를 200 · text/html 로 서빙 · 서빙 바이트 = 리포 파일
  ③ 맨 위 표지 "2D 모식 계산 (그림용 · 실제 3D 침대 결과 아님)" · 씨앗 공개 (쓴 씨앗 = p0_figs_meta.json · 네 씨앗 표 =
     scan_seeds_20261101.txt 값 · 판 정지 뒤 판 힘이 오르는 씨앗 둘)
  ④ 그림 여섯 — 이름 · 미리보기 · 크기 (in) = README 표 = PNG 픽셀 / dpi = SVG pt / 72 · 설명 = README 표의 그 줄 그대로 ·
     PNG · SVG 내려받기 링크 (download)
  ⑤ 페이지가 거는 모든 파일 = 200 · 원본과 바이트 같음 · 원본 폴더의 모든 파일이 걸려 있다
  ⑥ 사이드바 (base.html) 에 링크 · 렌더된 화면 (/worklog) 에 보인다 · app.py 에 이 페이지 라우트 없음
  ⑦ `../` 경로 탈출 = 404 · 새는 글 없음
  ⑧ 사본 대조 (sync 스크립트 함수 · `--check` CLI) = 같음 · 음성 대조 (바이트 하나 바뀜 · 빠짐 · 남음 · 빈 원본) 를 잡는다
  ⑨ 보이는 글에 천 단위 콤마 없음 · SVG 사본에 스크립트 없음 (정적 경로 = 인증 면제)

  python3 webapp/test_dem_method_figs_page.py
"""
import importlib.util
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

PAGE_DIR_URL = '/static/dem_method_figs/'
PAGE_URL = PAGE_DIR_URL + 'index.html'
PAGE = os.path.join(HERE, 'static', 'dem_method_figs', 'index.html')
DST = os.path.join(HERE, 'static', 'dem_method_figs', 'files')
SRC = os.path.join(ROOT, 'docs', '50kg', 'report_y4', 'figs', 'p0_dem_method')
README = os.path.join(SRC, 'README.md')
SCAN = os.path.join(SRC, 'scan_seeds_20261101.txt')
META = os.path.join(SRC, 'p0_figs_meta.json')
BASE = os.path.join(HERE, 'templates', 'base.html')
APP = os.path.join(HERE, 'app.py')
SYNC = os.path.join(ROOT, 'scripts', 'sync_dem_method_figs_to_webapp.py')
SIDEBAR_LABEL = 'DEM 방법 그림 (2D)'
NOTE = '2D 모식 계산 (그림용 · 실제 3D 침대 결과 아님)'
FIGS = ('p0_process_grid_labeled', 'p0_process_grid_nolabel', 'p0_process_labeled',
        'p0_process_nolabel', 'p0_contact_model_labeled', 'p0_contact_model_nolabel')
#: 경로 탈출 — 전부 404 여야 한다 (Flask 정적 경로 · safe_join)
BAD_PATHS = (
    PAGE_DIR_URL + '../../app.py',
    PAGE_DIR_URL + 'files/../../../app.py',
    PAGE_DIR_URL + 'files/../../../templates/base.html',
    PAGE_DIR_URL + 'files/../../../../CLAUDE.md',
    PAGE_DIR_URL + 'files/../../../../docs/50kg/report_y4/figs/p0_dem_method/README.md',
    PAGE_DIR_URL + 'files/..%2f..%2f..%2fapp.py',
    PAGE_DIR_URL + 'files/%2e%2e/%2e%2e/%2e%2e/app.py',
    PAGE_DIR_URL + 'files/..%2F..%2F..%2F..%2FCLAUDE.md',
    PAGE_DIR_URL + '..%2f..%2fapp.py',
    '/static/../app.py',
    '/static/..%2fapp.py',
    PAGE_DIR_URL + 'files/%00',
)
#: 탈출이 성공했다면 보일 글 (app.py 의 Flask 객체 줄 · CLAUDE.md 첫 줄 · base.html 블록 · README 머리)
LEAK_MARKERS = ('app = Flask(', '# Project conventions for Claude Code sessions',
                '{% block content %}', '# 50kg 4차년도 보고 0쪽 그림')

_ok, _fail = 0, []


def chk(name, cond):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}')


_VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta',
         'source', 'track', 'wbr'}


class _Scan(HTMLParser):
    """태그 짝 · 보이는 글 · 링크 · 금지 요소를 한 번에 본다."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.unbalanced, self.text = [], [], []
        self.scripts, self.ext, self.links = 0, [], []
        self._skip = 0

    def _attrs(self, tag, attrs):
        a = dict(attrs)
        for k in ('src', 'href'):
            v = (a.get(k) or '').strip()
            if v.lower().startswith(('http:', 'https:', '//', 'javascript:', 'data:')):
                self.ext.append(f'{tag} {k}={v}')
            if k in a:
                self.links.append((tag, k, v, a))
        return a

    def handle_starttag(self, tag, attrs):
        self._attrs(tag, attrs)
        if tag == 'script':
            self.scripts += 1
        if tag in ('style', 'script'):
            self._skip += 1
        if tag not in _VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        self._attrs(tag, attrs)

    def handle_endtag(self, tag):
        if tag in ('style', 'script'):
            self._skip = max(0, self._skip - 1)
        if tag in _VOID:
            return
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        else:
            self.unbalanced.append(tag)

    def handle_data(self, data):
        if not self._skip:
            self.text.append(data)


def _squash(s):
    return ' '.join(s.split())


def _vis(fragment):
    """HTML 조각의 보이는 글 (태그 = 빈칸 · 문자 참조 풀기 · 공백 하나로)."""
    sc = _Scan()
    sc.feed(fragment)
    sc.close()
    return _squash(' '.join(sc.text))


def readme_rows():
    """README §1 표 → {이름 (확장자 없는 그림 이름 또는 파일 이름): (크기, 설명)}."""
    out = {}
    if not os.path.isfile(README):
        return out
    for ln in open(README, encoding='utf-8'):
        m = re.match(r'^\|\s*`([^`]+)`(?:\s*·\s*`\.svg`)?\s*\|\s*([^|]*?)\s*\|\s*(.*?)\s*\|\s*$', ln)
        if not m:
            continue
        name = m.group(1)
        if name.endswith('.png'):
            name = name[:-4]
        out[name] = (m.group(2), _squash(m.group(3).replace('`', '')))
    return out


def png_inches(path):
    """PNG 머리 (IHDR · pHYs) → (가로 in, 세로 in) — pHYs 가 m 단위가 아니면 None."""
    b = open(path, 'rb').read()
    if b[:8] != b'\x89PNG\r\n\x1a\n':
        return None
    w, h = struct.unpack('>II', b[16:24])
    i = b.find(b'pHYs')
    if i < 0:
        return None
    px, py, unit = struct.unpack('>IIB', b[i + 4:i + 13])
    if unit != 1 or not px or not py:
        return None
    return w / (px * 0.0254), h / (py * 0.0254)


def svg_inches(path):
    """SVG 머리 width · height (pt) → in."""
    head = open(path, 'rb').read(4000).decode('utf-8', 'replace')
    m = re.search(r'<svg\b[^>]*?\swidth="([\d.]+)pt"[^>]*?\sheight="([\d.]+)pt"', head, re.S)
    return (float(m.group(1)) / 72.0, float(m.group(2)) / 72.0) if m else None


def size_tuple(s):
    m = re.fullmatch(r'\s*([\d.]+)\s*×\s*([\d.]+)\s*', s or '')
    return (float(m.group(1)), float(m.group(2))) if m else None


def load_sync():
    if not os.path.isfile(SYNC):
        return None
    spec = importlib.util.spec_from_file_location('sync_dem_method_figs_to_webapp', SYNC)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as e:                                        # noqa: BLE001
        print(f'  (sync 스크립트 import 실패: {e!r})')
        return None
    return mod


def _section(src, fid):
    """그림 칸 `<section class="figcard" id="FID">…</section>` 의 HTML (없으면 '')."""
    m = re.search(r'<section class="figcard" id="' + re.escape(fid) + r'">(.*?)</section>', src, re.S)
    return m.group(1) if m else ''


def main():
    print('── ① 파일 · 한 파일로 닫힘')
    exists = os.path.isfile(PAGE)
    chk('정적 파일이 webapp/static/dem_method_figs/index.html 에 있다', exists)
    src = open(PAGE, encoding='utf-8').read() if exists else ''
    sc = _Scan()
    sc.feed(src)
    sc.close()
    text = _squash(' '.join(sc.text))
    chk('<html lang="ko"> · <title> 이 있다', '<html lang="ko">' in src and bool(re.search(r'<title>[^<]+</title>', src)))
    chk('태그 짝이 맞다 (닫히지 않은 · 엇갈린 태그 0)', exists and not sc.stack and not sc.unbalanced)
    chk('<script> 없음', exists and sc.scripts == 0)
    chk(f'외부 자원 · javascript: · data: 없음 (찾은 것 {sc.ext})', exists and not sc.ext)
    chk('웹앱으로 돌아가는 링크 href="/"', 'href="/"' in src)

    print('── ③ 표지 · 씨앗 공개')
    chk(f'맨 위 표지 "{NOTE}"', NOTE in text)
    note_pos = text.find(NOTE)
    first_fig = min([p for p in (text.find(f) for f in FIGS) if p >= 0] or [-1])
    chk('표지가 그림 목록보다 앞에 있다', note_pos >= 0 and (first_fig < 0 or note_pos < first_fig))
    meta = json.load(open(META, encoding='utf-8')) if os.path.isfile(META) else {}
    seed = meta.get('seed')
    chk(f'쓴 씨앗 = p0_figs_meta.json seed ({seed}) — "씨앗 {seed}"', seed is not None and f'씨앗 {seed}' in text)
    scan = [json.loads(ln) for ln in open(SCAN, encoding='utf-8') if ln.strip()] if os.path.isfile(SCAN) else []
    chk('scan_seeds_20261101.txt = 네 씨앗 (11 · 13 · 17 · 23)', [r.get('seed') for r in scan] == [11, 13, 17, 23])
    tbl = re.search(r'<table id="seeds">(.*?)</table>', src, re.S)
    rows = []
    if tbl:
        for tr in re.findall(r'<tr>(.*?)</tr>', tbl.group(1), re.S):
            cells = [_vis(c) for c in re.findall(r'<td[^>]*>(.*?)</td>', tr, re.S)]
            if cells:
                rows.append(cells)
    want_rows = [[str(r['seed']), f"{r['f_stop']:.1f}", f"{r['f_relax']:.1f}",
                  '내림' if r['drop'] else '오름'] for r in scan]
    chk(f'씨앗 표 (id seeds) = scan 파일 값 (1 자리 반올림 · 방향 = drop) {rows}', bool(want_rows) and rows == want_rows)
    rising = [str(r['seed']) for r in scan if not r['drop']]
    chk(f'판 정지 뒤 판 힘이 오르는 씨앗 = scan 의 drop false ({rising}) · 두 개', rising == ['11', '17'])
    chk('공개 문장 — "네 씨앗 (11 · 13 · 17 · 23) 중 둘 (11 · 17) 은 판 정지 뒤 판 힘이 오른다"',
        '네 씨앗 (11 · 13 · 17 · 23) 중 둘 (11 · 17) 은 판 정지 뒤 판 힘이 오른다' in text)
    chk('README 한정어 — "이완 뒤 판 힘 방향은 씨앗에 따라 다르다" · "그림 설명용이지 결과가 아니다"',
        '이완 뒤 판 힘 방향은 씨앗에 따라 다르다' in text and '그림 설명용이지 결과가 아니다' in text)

    print('── ④ 그림 여섯 — 이름 · 크기 · 설명 · 미리보기 · 내려받기')
    rd = readme_rows()
    for f in FIGS:
        sec = _section(src, f)
        svis = _vis(sec)
        size, what = rd.get(f, (None, None))
        chk(f'{f}: 그림 칸 (section.figcard id) 이 있고 이름이 보인다', bool(sec) and f in svis)
        chk(f'{f}: README 표에 줄이 있다 (크기 {size})', size is not None and what)
        #  ★ 칸의 그 요소와 **같아야** 한다 (포함만 보면 README 글 뒤에 덧붙인 문장이 통과한다 — 변이로 확인)
        p_size = re.search(r'<p class="size">(.*?)</p>', sec, re.S)
        p_what = re.search(r'<p class="what">(.*?)</p>', sec, re.S)
        chk(f'{f}: 크기 칸 (p.size) = "{size} in"', bool(size) and p_size is not None and _vis(p_size.group(1)) == f'{size} in')
        chk(f'{f}: 설명 칸 (p.what) = README 표의 그 줄 그대로', bool(what) and p_what is not None and _vis(p_what.group(1)) == what)
        st = size_tuple(size)
        pin = png_inches(os.path.join(SRC, f + '.png')) if os.path.isfile(os.path.join(SRC, f + '.png')) else None
        sin = svg_inches(os.path.join(SRC, f + '.svg')) if os.path.isfile(os.path.join(SRC, f + '.svg')) else None
        chk(f'{f}: README 크기 = PNG 픽셀 / dpi = SVG pt / 72 ({st} · {pin} · {sin})',
            st is not None and pin is not None and sin is not None
            and all(abs(a - b) < 0.006 for a, b in zip(st, pin)) and all(abs(a - b) < 0.006 for a, b in zip(st, sin)))
        chk(f'{f}: 미리보기 <img src="files/{f}.png"> · alt 있음',
            bool(re.search(r'<img\b[^>]*\bsrc="files/' + re.escape(f) + r'\.png"[^>]*\balt="[^"]+"', sec)
                 or re.search(r'<img\b[^>]*\balt="[^"]+"[^>]*\bsrc="files/' + re.escape(f) + r'\.png"', sec)))
        for ext in ('png', 'svg'):
            chk(f'{f}: {ext.upper()} 내려받기 링크 (href files/{f}.{ext} · download)',
                bool(re.search(r'<a\b[^>]*\bhref="files/' + re.escape(f) + r'\.' + ext + r'"[^>]*\bdownload\b', sec)))
    #  함께 받는 파일 표 — README 표에 줄이 있는 두 JSON 은 설명 칸 = README 그 줄 그대로
    for name in ('toy2d_seed23.json', 'p0_figs_meta.json'):
        want = rd.get(name, (None, None))[1]
        m = re.search(r'<tr><td><code>' + re.escape(name) + r'</code></td><td>(.*?)</td>', src, re.S)
        chk(f'함께 받는 파일 {name}: 설명 칸 = README 표의 그 줄 그대로', bool(want) and m is not None and _vis(m.group(1)) == want)

    print('── ② ⑤ 실제 서빙 · 거는 파일 = 원본 바이트 · 원본 전부가 걸림')
    import app as webapp
    c = webapp.app.test_client()
    r = c.get(PAGE_URL)
    chk(f'GET {PAGE_URL} → 200', r.status_code == 200)
    chk('text/html 로 서빙', r.status_code == 200 and (r.mimetype or '') == 'text/html')
    chk('서빙된 바이트 = 리포 파일', exists and r.status_code == 200 and r.get_data() == open(PAGE, 'rb').read())
    rel = sorted({v for _t, _k, v, _a in sc.links if v and not v.startswith(('/', '#'))})
    chk(f'상대 링크는 전부 files/ 아래 ({len(rel)} 개)', bool(rel) and all(v.startswith('files/') for v in rel))
    absl = sorted({v for _t, _k, v, _a in sc.links if v.startswith(('/', '#')) or not v})
    chk(f'그 밖의 링크는 웹앱으로 돌아가는 "/" 하나뿐 (찾은 것 {absl})', absl == ['/'])
    src_names = sorted(n for n in os.listdir(SRC) if os.path.isfile(os.path.join(SRC, n))) if os.path.isdir(SRC) else []
    linked = sorted({v[len('files/'):] for v in rel if v.startswith('files/')})
    chk(f'걸린 파일은 전부 원본 폴더에 있다 (남는 것 {sorted(set(linked) - set(src_names))})',
        bool(linked) and set(linked) <= set(src_names))
    for f in FIGS:
        for ext in ('png', 'svg'):
            chk(f'{f}.{ext} 가 원본 폴더에 있다', f'{f}.{ext}' in src_names)
    #  ★ 원본 폴더 기준으로 돈다 (검사 수가 페이지에 따라 바뀌지 않게) — 원본 파일마다: 걸려 있나 · 서빙 = 원본 바이트
    for name in src_names:
        want = open(os.path.join(SRC, name), 'rb').read()
        chk(f'files/{name} 가 페이지에 걸려 있다', name in linked)
        rr = c.get(PAGE_DIR_URL + 'files/' + name)
        chk(f'GET files/{name} → 200 · 원본과 바이트 같음', rr.status_code == 200 and rr.get_data() == want)
        if name.endswith('.png'):
            chk(f'files/{name} mimetype image/png', rr.status_code == 200 and (rr.mimetype or '') == 'image/png')
        if name.endswith('.svg'):
            chk(f'files/{name} mimetype image/svg+xml',
                rr.status_code == 200 and (rr.mimetype or '') == 'image/svg+xml')

    print('── ⑥ 사이드바 링크 · 렌더된 화면')
    base = open(BASE, encoding='utf-8').read()
    m = re.search(r'<a href="' + re.escape(PAGE_URL) + r'"[^>]*>(.*?)</a>', base, re.S)
    chk('base.html 사이드바에 링크', m is not None)
    chk(f'그 링크 글 = "{SIDEBAR_LABEL}"', m is not None and SIDEBAR_LABEL in m.group(1))
    r2 = c.get('/worklog')
    page2 = r2.get_data(as_text=True)
    m2 = re.search(r'<a href="' + re.escape(PAGE_URL) + r'"[^>]*>(.*?)</a>', page2, re.S)
    chk('렌더된 화면 (/worklog) 사이드바에 링크 · 글이 보인다',
        r2.status_code == 200 and m2 is not None and SIDEBAR_LABEL in m2.group(1))
    app_src = open(APP, encoding='utf-8').read()
    chk('app.py 에 이 페이지 라우트 · 경로 없음 (봉인 32 무변경 · 정적 폴더로만)', 'dem_method_figs' not in app_src)

    print('── ⑦ 경로 탈출 = 404 · 새는 글 없음')
    for p in BAD_PATHS:
        rr = c.get(p)
        txt = rr.get_data(as_text=True)
        chk(f'거부 {p} → 404', rr.status_code == 404)
        chk(f'새는 글 없음 {p}', not any(mk in txt for mk in LEAK_MARKERS))

    print('── ⑧ 사본 대조 (sync 스크립트) · 음성 대조')
    sync = load_sync()
    chk('scripts/sync_dem_method_figs_to_webapp.py 가 있고 import 된다', sync is not None)
    probs = sync.compare(SRC, DST) if sync else ['(sync 없음)']
    chk(f'compare(원본, 웹앱 사본) = 같음 (문제 {probs[:3]})', probs == [])
    if sync and os.path.isdir(DST):
        rc = subprocess.run([sys.executable, SYNC, '--check'], capture_output=True, text=True, timeout=120)
        chk(f'CLI --check rc 0 ({(rc.stdout or rc.stderr).strip().splitlines()[-1:]})', rc.returncode == 0)
        with tempfile.TemporaryDirectory(prefix='demfigs_') as td:
            s2, d2 = os.path.join(td, 'src'), os.path.join(td, 'dst')
            shutil.copytree(SRC, s2)
            shutil.copytree(DST, d2)
            victim = os.path.join(d2, FIGS[0] + '.png')
            b = bytearray(open(victim, 'rb').read())
            b[len(b) // 2] ^= 0x01
            open(victim, 'wb').write(bytes(b))
            p1 = sync.compare(s2, d2)
            chk(f'음성 ① 사본 바이트 하나 바뀜 → 잡는다 ({p1[:1]})', any(FIGS[0] + '.png' in x for x in p1))
            rcn = subprocess.run([sys.executable, SYNC, '--check', '--src', s2, '--dst', d2],
                                 capture_output=True, text=True, timeout=120)
            chk('음성 ① CLI --check (같은 반례) rc 1', rcn.returncode == 1)
            fixed = sync.sync(s2, d2)
            chk(f'sync() 가 고친다 → compare 같음 ({fixed[:1]})', fixed == [] and sync.compare(s2, d2) == [])
            os.remove(os.path.join(d2, FIGS[1] + '.svg'))
            p2 = sync.compare(s2, d2)
            chk(f'음성 ② 사본 하나 빠짐 → 잡는다 ({p2[:1]})', any(FIGS[1] + '.svg' in x for x in p2))
            sync.sync(s2, d2)
            open(os.path.join(d2, 'extra.png'), 'wb').write(b'x')
            p3 = sync.compare(s2, d2)
            chk(f'음성 ③ 원본에 없는 사본 → 잡는다 ({p3[:1]})', any('extra.png' in x for x in p3))
            sync.sync(s2, d2)
            chk('sync() 가 원본에 없는 사본을 지운다', not os.path.exists(os.path.join(d2, 'extra.png'))
                and sync.compare(s2, d2) == [])
            empty = os.path.join(td, 'empty')
            os.makedirs(empty)
            p4 = sync.compare(empty, os.path.join(td, 'empty_dst'))
            chk(f'음성 ④ 빈 원본 · 없는 사본 폴더 → 통과시키지 않는다 ({p4[:1]})', bool(p4))
    else:
        for name in ('CLI --check rc 0', '음성 ① 바이트', '음성 ① CLI', 'sync() 고침', '음성 ② 빠짐',
                     '음성 ③ 남음', 'sync() 지움', '음성 ④ 빈 원본'):
            chk(f'{name} (sync · 사본 폴더 없음)', False)

    print('── ⑨ 천 단위 콤마 · SVG 스크립트')
    commas = sorted(set(re.findall(r'\d{1,3}(?:,\d{3})+(?![\d])', text)))
    chk(f'보이는 글의 천 단위 콤마 0 (찾은 것 {commas})', exists and not commas)
    svgs = [n for n in (os.listdir(DST) if os.path.isdir(DST) else []) if n.endswith('.svg')]
    bad_svg = [n for n in svgs if re.search(r'<\s*script|javascript:|<[a-z][^<>]*\son[a-z]+\s*=',
                                            open(os.path.join(DST, n), encoding='utf-8', errors='replace').read(), re.I)]
    chk(f'SVG 사본 {len(svgs)} 개에 스크립트 · 이벤트 속성 없음 (찾은 것 {bad_svg})', len(svgs) == 6 and not bad_svg)

    print(f'\n== test_dem_method_figs_page: {_ok}/{_ok + len(_fail)} PASS')
    if _fail:
        print('   실패: ' + ' · '.join(_fail[:12]) + (' …' if len(_fail) > 12 else ''))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
