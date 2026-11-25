#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""영상 섹션 (/videos) 회귀 — 1저자 11-24 (믹서 AVI 가 완성되면 웹앱에 영상 섹션 · 저장 · 재생 · 받기 · 세부 내용 토글 ·
유튜브 재생목록 꼴을 참고만 · 다른 가지에서도 보이게 AVI 스킬에).

  python3 webapp/test_video_page.py

보는 것 (합성 꾸러미만 쓴다 — 실제 영상 · 리포 밖 자료 없이 CI 에서 돈다):
  A 화면   편 0 개 = 안내 · 등록한 편 = video (controls · poster · 자막 track) · 제목 · 길이 · 갱신 · 받기 단추 셋 ·
           재생목록 판 (시리즈 · n / N · 지금 편 강조) · 토글 일곱 (챕터 · 대본 · 장면 · 참고 문헌 · QC · 기준표 · 해시)
  B 파일   재생 = Range 206 · 받기 = attachment · srt → WebVTT · 등록 밖 종류 · 경로 꼴 = 404
  C 등록부 깨짐 (JSON · 파일 없음 · 해시 · 폴더 이름 · 심볼릭 링크 · 모르는 스키마) = 200 + 안내 · 그 편 = 404 (fail-closed)
  D 내부판 INTERNAL 이름 = --internal 없이 거부 · 빨간 배지 · 공개판 꾸러미에 qc_report 의 internal 칸이 들어가지 않는다
  E 꾸러미 zip-slip · 하위 폴더 · 절대 경로 · 심볼릭 링크 · 해시 어긋남 · 목록 밖 항목 · 중복 · 크기 상한 · 이미 있는 편 (바꾸기 = 명시)
           공개 안전 검사 (홈 경로 · 철회값 · 내부 숫자 목록) — 공개판은 거부 · 내부판은 기록만
  F 올리기 같은 등록 함수 · 로컬 · 같은 출처만 · 깨진 꾸러미 400 · 이미 있음 409
  G 명령   scripts/avi_package_episode.py · scripts/avi_register_episode.py (꾸러미 · 폴더 = 같은 함수)
  H 위생   템플릿 · app.py · 라이브러리에 자료 값 · 문장 없음 · md 의 HTML · javascript: 링크 무력화 · GET 은 폴더를 만들지 않는다
⚠ 금지값 (claims.json quotation_ban) 을 이 파일에 적지 않는다 — 철회값 검사는 등록부에서 실행 중에 읽는다.
"""
import hashlib
import io
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import zipfile
import zlib
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
_ok, _fail = 0, []

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TPL = HERE / 'templates' / 'videos.html'
LIB = HERE / 'video_library.py'
APP = HERE / 'app.py'
BASE = HERE / 'templates' / 'base.html'
PKG = ROOT / 'scripts' / 'avi_package_episode.py'
REG = ROOT / 'scripts' / 'avi_register_episode.py'

#: 합성 자료의 고유 표지 — 화면에는 나와야 하고 (자료를 읽어 보인다) 템플릿 · 코드에는 없어야 한다 (베끼지 않는다).
T_TITLE = '시험 편 VDT-TITLE-8812'
T_SUB = '부제 VDT-SUB-3317'
T_SERIES = '시험 시리즈 VDT-SER-4471'
T_SC1, T_SC2 = '장면 하나 VDT-SC1-1190', '장면 둘 VDT-SC2-2281'
T_REF = 'VDT-REF-7151 외 (2031)'
T_OTHER = 'VDT-OTHER-7262'
T_SCRIPT = 'VDT-SCRIPT-6043'
T_QC = 'VDT-QC-5521'
T_RUB = 'VDT-RUB-6612'
T_SECRET = 'VDT-INTERNAL-SECRET-9931'
T_FOUND = 'VDT-FOUND-4410'
T_CUE = 'VDT-CUE-3305'
T_I_TITLE = '[내부] 시험 내부 VDT-ITITLE-5160'
T_I_SERIES = '내부 시험 시리즈 VDT-ISER-0912'
T_DENY = '77.123'                           # 합성 "내부 숫자" — 공개판 글에 넣으면 걸려야 한다
ALL_TOKENS = (T_TITLE, T_SUB, T_SERIES, T_SC1, T_SC2, T_REF, T_OTHER, T_SCRIPT, T_QC, T_RUB, T_SECRET, T_FOUND, T_CUE,
              T_I_TITLE, T_I_SERIES)
#: ep01 (믹서) 실제 글의 조각 — 템플릿 · 코드에 베껴 두면 안 된다 (자료를 고치면 화면이 같이 바뀌어야 한다).
EP01_SNIPS = ('가루는 왜', '끼리끼리', '전고체 배터리 연구 노트', '본드 수', '정렬 혼합')
#: 탈출이 성공했다면 보일 글
LEAK_MARKS = ('app = Flask(', 'root:x:0:0', '"schema": "avi-episode', 'avi-episode/1')


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


def _png(w=4, h=3, rgb=(78, 68, 226)):
    """작은 PNG (zlib · struct 만)."""
    raw = b''.join(b'\x00' + bytes(rgb) * w for _ in range(h))

    def chunk(t, d):
        c = struct.pack('>I', len(d)) + t + d
        return c + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(raw)) + chunk(b'IEND', b''))


def _video_bytes(n=300_000):
    """가짜 mp4 (머리 + 결정적 바이트) — 서버는 mp4 를 풀지 않는다 (Range · 받기만 본다)."""
    head = b'\x00\x00\x00\x18ftypmp42\x00\x00\x00\x00mp42isom'
    body = hashlib.sha256(b'vdt').digest() * (n // 32 + 1)
    return (head + body)[:n]


def _sha(b):
    return hashlib.sha256(b).hexdigest()


SRT = ('﻿1\r\n00:00:00,500 --> 00:00:02,000\r\n첫 자막 ' + T_CUE + '\r\n\r\n'
       '2\r\n0:00:02,000 --> 00:00:04,250\r\nA & B <i>기울임</i>\r\n\r\n'
       '깨진 덩어리 (시각 줄 없음)\r\n\r\n'
       '3\r\n00:00:04,250 --> 00:00:06,000\r\n둘째 줄 하나\r\n둘째 줄 둘\r\n')


def make_ep(d, *, internal=False, mp4_name=None, extra_md=None, qc_secret=True):
    """합성 편 폴더 → 경로.  internal=True 면 INTERNAL 이름 파일 (내부판 꼴)."""
    d = Path(d)
    d.mkdir(parents=True, exist_ok=True)
    vb = _video_bytes()
    name = mp4_name or ('clip_INTERNAL_x.mp4' if internal else 'preview.mp4')
    (d / name).write_bytes(vb)
    if not internal:
        (d / 'thumbnail.png').write_bytes(_png())
    (d / (name[:-4] + '.srt' if internal else 'ep99.srt')).write_text(SRT, encoding='utf-8', newline='')
    script = (f'# 대본 {T_SCRIPT}\n\n## 참고 문헌 (시험)\n\n1. {T_REF} · *가짜 학술지* 1, 2 (2031)\n\n'
              f'## 다른 절\n\n{T_OTHER}\n')
    if extra_md:
        script += '\n' + extra_md + '\n'
    (d / 'script.md').write_text(script, encoding='utf-8')
    scenes = dict(episode='ep99_test', title=T_I_TITLE if internal else T_TITLE, subtitle=T_SUB,
                  series=T_I_SERIES if internal else T_SERIES, voice_model=dict(lead_in=0.7),
                  scenes=[dict(id='s01', title=T_SC1, lines=[dict(id='s01_l01'), dict(id='s01_l02')],
                               shots=[dict(id='s01a')]),
                          dict(id='s02', title=T_SC2, lines=[dict(id='s02_l01')], shots=[dict(id='s02a'), dict(id='s02b')])])
    (d / 'scenes.json').write_text(json.dumps(scenes, ensure_ascii=False), encoding='utf-8')
    tl = dict(summary=dict(duration_s=12.5),
              lines=[dict(id='s01_l01', scene='s01', t0=0.7, t1=2.0, pause=0.4),
                     dict(id='s01_l02', scene='s01', t0=2.4, t1=4.0, pause=0.4),
                     dict(id='s02_l01', scene='s02', t0=6.2, t1=9.0, pause=0.5)],
              shots=[dict(id='s01a', scene='s01', t_start=0.1, t_end=6.0)])
    (d / 'timeline.json').write_text(json.dumps(tl), encoding='utf-8')
    if internal:
        (d / 'qc_internal.md').write_text(f'# QC {T_QC}\n\n- 내부 점검\n', encoding='utf-8')
    else:
        (d / 'qc.md').write_text(f'# QC {T_QC}\n\n- 점검 한 줄\n', encoding='utf-8')
        rep = dict(version='v9', public=dict(video=name, sha256=_sha(vb), duration_s=12.5,
                                             checks=[dict(what='전체 0.5 s', frames=25, viewed_frames=25,
                                                          static_over_5s=[], flicker=[], edge_band_frames=0)],
                                             found=[dict(t='3-4 s', scene='s01a', what=T_FOUND, fixed_in=None)]))
        if qc_secret:
            rep['internal'] = dict(video='internal/x_INTERNAL_y.mp4', note=T_SECRET)
        (d / 'qc_report_v2.json').write_text(json.dumps(rep, ensure_ascii=False), encoding='utf-8')
        (d / 'rubric_ep99.md').write_text(f'# 기준표 {T_RUB}\n\n| 항목 | 점수 |\n|---|---|\n| 대본 | 8 |\n', encoding='utf-8')
    (d / 'build_scenes.py').write_text('# 넣지 않는 파일\n', encoding='utf-8')
    (d / 'notes').mkdir(exist_ok=True)
    (d / 'notes' / 'deep.md').write_text('하위 폴더 — 넣지 않는다\n', encoding='utf-8')
    return d


def zip_names(p):
    with zipfile.ZipFile(p) as z:
        return z.namelist()


_CRAFT_ROLE = (('.mp4', 'video'), ('.md', 'script'), ('.srt', 'subtitles'), ('.json', 'scenes'), ('.png', 'thumbnail'))


def craft_zip(path, entries, *, sums=True, manifest=None, sums_override=None, links=(), not_in_manifest=(), bad_sum_for=()):
    """손으로 만든 꾸러미 — entries = [(이름, 바이트)] · manifest = episode.json dict (없으면 만든다 · 역할 = 이름 끝 ·
    시험이 역할이 겹치지 않게 이름을 고른다 → 꾸러미는 **그 결함 하나만** 빼면 정상)."""
    def role(n):
        return next((r for ext, r in _CRAFT_ROLE if n.lower().endswith(ext)), 'readme')
    files = [dict(name=n, role=role(n), size=len(b), sha256=_sha(b)) for n, b in entries
             if n not in ('episode.json', 'SHA256SUMS') and n not in not_in_manifest]
    man = manifest if manifest is not None else dict(
        schema='avi-episode/1', id='ep77_craft', title='손 꾸러미', subtitle='', series='손 시리즈', episode=77,
        visibility='public', duration_s=3.0, updated='2031-01-01', files=files,
        public_check=dict(ok=True, rules=[], hits=[], files=len(files), deny_list=None))
    mb = json.dumps(man, ensure_ascii=False).encode('utf-8')
    with zipfile.ZipFile(path, 'w') as z:
        z.writestr('episode.json', mb)
        lines = [f'{_sha(mb)}  episode.json']
        for n, b in entries:
            if n in ('episode.json', 'SHA256SUMS'):
                continue
            if n in links:
                zi = zipfile.ZipInfo(n)
                zi.create_system = 3
                zi.external_attr = (0o120777 << 16)
                z.writestr(zi, b)
            else:
                z.writestr(n, b)
            lines.append(f"{'0' * 64 if n in bad_sum_for else _sha(b)}  {n}")
        if sums:
            z.writestr('SHA256SUMS', sums_override if sums_override is not None else ('\n'.join(lines) + '\n'))
    return path


def _details(html):
    """<details …> 의 data-vd 이름 목록 (화면 순서)."""
    return re.findall(r'<details[^>]*data-vd="([a-z_]+)"', html)


def _region(html, key):
    m = re.search(r'<details[^>]*data-vd="' + key + r'"[^>]*>(.*?)</details>', html, re.S)
    return m.group(1) if m else ''


def _snapshot(folder):
    out = []
    for r, ds, fs in os.walk(folder):
        out += [os.path.relpath(os.path.join(r, x), folder) for x in ds + fs]
    return sorted(out)


def main():
    try:
        import app as webapp
    except Exception as e:                                  # noqa: BLE001
        print(f'  FAIL  app import — {type(e).__name__}: {e}')
        return 1
    try:
        import video_library as V
    except Exception as e:                                  # noqa: BLE001
        print(f'  (video_library import 실패 — {type(e).__name__}: {e})')
        V = None
    c = webapp.app.test_client()
    tpl = TPL.read_text(encoding='utf-8') if TPL.is_file() else ''
    app_src = APP.read_text(encoding='utf-8')
    lib_src = LIB.read_text(encoding='utf-8') if LIB.is_file() else ''
    td_all = tempfile.mkdtemp(prefix='vdt_')
    orig_folder = webapp.app.config.get('VIDEO_FOLDER')
    try:
        return _run(webapp, V, c, tpl, app_src, lib_src, Path(td_all))
    finally:
        if orig_folder is not None:
            webapp.app.config['VIDEO_FOLDER'] = orig_folder
        shutil.rmtree(td_all, ignore_errors=True)


def _run(webapp, V, c, tpl, app_src, lib_src, td):
    cfg = webapp.app.config
    have = V is not None
    BE = getattr(V, 'BundleError', ValueError) if have else ValueError

    def pkg(ep_dir, ep_id, out, **kw):
        kw.setdefault('probe', False)
        return V.package_episode(ep_dir, ep_id, out, **kw)

    def refused(fn, *a, **kw):
        """→ (거부됐나, 사유 글)."""
        try:
            fn(*a, **kw)
        except BE as e:
            return True, str(e)
        except Exception as e:                              # noqa: BLE001
            return False, f'다른 예외 {type(e).__name__}: {e}'
        return False, '거부 안 함'

    # ═══ A0. 편 0 개 · 폴더 없음 — 안내 · 부작용 없음 ═══
    empty = td / 'lib_empty'
    empty.mkdir()
    cfg['VIDEO_FOLDER'] = str(empty)
    r = c.get('/videos')
    h = r.get_data(as_text=True)
    chk('① 편 0 개 — GET /videos = 200 · 안내 "등록된 편이 없습니다" · <video> 없음 · 올리기 칸 있음',
        r.status_code == 200 and '등록된 편이 없습니다' in h and '<video' not in h and 'name="bundle"' in h)
    chk('①b 올리기 블록 = 맨 위 (머리 바로 뒤 · 안내보다 앞) · 안내 문장 = 위 "꾸러미 올리기" (1저자 11-25)',
        0 <= h.find('class="vd-top"') < h.find('class="vd-upload"') < h.find('class="vd-empty"')
        and '위 "꾸러미 올리기"' in h and '아래 "꾸러미 올리기"' not in h)
    nofolder = td / 'lib_none'
    cfg['VIDEO_FOLDER'] = str(nofolder)
    r = c.get('/videos')
    h = r.get_data(as_text=True)
    chk('② 폴더가 없어도 200 + 같은 안내 · GET 이 폴더를 만들지 않는다',
        r.status_code == 200 and '등록된 편이 없습니다' in h and not nofolder.exists())
    chk('③ 사이드바에 영상 항목 (/videos · active = videos)',
        'href="/videos"' in BASE.read_text(encoding='utf-8') and "active == 'videos'" in BASE.read_text(encoding='utf-8'))

    # ═══ A1. 꾸러미 → 등록 → 화면 ═══
    lib = td / 'lib'
    ep = make_ep(td / 'src' / 'ep99_test')
    bun = td / 'b' / 'ep99.zip'
    bun.parent.mkdir()
    man = {}
    if have:
        try:
            man = pkg(ep, 'ep99_test', bun) or {}
        except Exception as e:                              # noqa: BLE001
            print(f'    package_episode 예외 — {type(e).__name__}: {e}')
    names = zip_names(bun) if bun.is_file() else []
    want = {'episode.json', 'SHA256SUMS', 'preview.mp4', 'thumbnail.png', 'ep99.srt', 'script.md', 'scenes.json',
            'timeline.json', 'qc.md', 'qc_report.json', 'rubric_ep99.md'}
    chk(f'④ 꾸러미 = 납작한 zip · 역할 파일 + episode.json + SHA256SUMS · 넣지 않는 파일 (build_scenes.py · 하위 폴더) 없음 ({sorted(names)})',
        set(names) == want)
    zman = {}
    if bun.is_file():
        with zipfile.ZipFile(bun) as z:
            zman = json.loads(z.read('episode.json').decode('utf-8')) if 'episode.json' in z.namelist() else {}
            qrep = json.loads(z.read('qc_report.json').decode('utf-8')) if 'qc_report.json' in z.namelist() else {}
            ztext = b''.join(z.read(n) for n in z.namelist() if not n.endswith(('.mp4', '.png'))).decode('utf-8', 'replace')
    else:
        qrep, ztext = {}, ''
    chk('⑤ episode.json — 스키마 avi-episode/1 · id · 제목 · 시리즈 · 편 번호 99 · 공개 · 길이 = timeline 12.5 · 파일 목록 sha256 = 실제',
        zman.get('schema') == 'avi-episode/1' and zman.get('id') == 'ep99_test' and zman.get('title') == T_TITLE
        and zman.get('series') == T_SERIES and zman.get('episode') == 99 and zman.get('visibility') == 'public'
        and zman.get('duration_s') == 12.5
        and {f.get('name'): f.get('sha256') for f in zman.get('files') or []}.get('preview.mp4') == _sha(_video_bytes()))
    chk('⑥ 공개판 꾸러미 — qc_report 의 internal 칸이 빠진 사본 (원본 sha256 기록) · 내부 표지 글이 꾸러미 어디에도 없다',
        bool(qrep) and 'internal' not in qrep and 'public' in qrep and T_SECRET not in ztext
        and any(dd.get('from') == 'qc_report_v2.json' and 'internal' in (dd.get('dropped_keys') or [])
                for dd in zman.get('derived') or []))
    chk('⑦ episode.json 에 절대 경로 · 원본 폴더 경로 없음 (/home · 임시 폴더 · 역슬래시)',
        bool(zman) and str(td) not in json.dumps(zman, ensure_ascii=False) and '/home/' not in json.dumps(zman)
        and '\\\\' not in json.dumps(zman))
    reg = {}
    if have and bun.is_file():
        try:
            reg = V.register_bundle(bun, lib, via='cli') or {}
        except Exception as e:                              # noqa: BLE001
            print(f'    register_bundle 예외 — {type(e).__name__}: {e}')
    epd = lib / 'ep99_test'
    chk('⑧ 등록 — <폴더>/ep99_test/ 에 episode.json · SHA256SUMS · 파일들 · registration.json (via cli)',
        (epd / 'episode.json').is_file() and (epd / 'preview.mp4').is_file() and (epd / 'SHA256SUMS').is_file()
        and json.loads((epd / 'registration.json').read_text(encoding='utf-8')).get('via') == 'cli'
        if (epd / 'registration.json').is_file() else False)
    cfg['VIDEO_FOLDER'] = str(lib)
    snap0 = _snapshot(lib)
    r = c.get('/videos')
    h = r.get_data(as_text=True)
    r2 = c.get('/videos/ep99_test')
    h2 = r2.get_data(as_text=True)
    chk('⑨ GET /videos = 200 = 첫 편 · GET /videos/ep99_test = 200 · 제목 · 부제 = 자료',
        r.status_code == 200 and r2.status_code == 200 and _esc(T_TITLE) in h and _esc(T_TITLE) in h2 and _esc(T_SUB) in h2)
    vtag = re.search(r'<video\b[^>]*>', h2)
    vt = vtag.group(0) if vtag else ''
    chk('⑩ <video controls> · poster = 썸네일 주소 · <source src=…/media/video type=video/mp4> · <track kind=subtitles src=…/subtitles.vtt>',
        'controls' in vt and 'poster="/videos/ep99_test/media/thumbnail"' in vt
        and '<source src="/videos/ep99_test/media/video" type="video/mp4">' in h2
        and re.search(r'<track kind="subtitles"[^>]*src="/videos/ep99_test/subtitles\.vtt"', h2) is not None)
    chk('⑪ 한 줄 — 길이 0:12 · 갱신 날짜 · 공개판 배지 (공개 안전 검사 통과) · 내부 배지 없음',
        '0:12' in h2 and f'갱신 {zman.get("updated", "?")}' in h2 and 'data-badge="public"' in h2 and '공개 안전 검사 통과' in h2
        and 'data-badge="internal"' not in h2 and '내부용 · 공개 금지' not in h2)
    chk('⑫ 받기 단추 셋 — mp4 · 자막 srt · 대본 md (주소 = /download/<종류>)',
        'href="/videos/ep99_test/download/video"' in h2 and 'href="/videos/ep99_test/download/subtitles"' in h2
        and 'href="/videos/ep99_test/download/script"' in h2 and 'mp4 받기' in h2 and '자막 srt' in h2 and '대본 md' in h2)
    chk(f'⑬ 재생목록 판 — 시리즈 이름 · 1 / 1 · 지금 편 강조 (is-current) · 판이 본문 뒤 (폰 폭에서 아래)',
        'class="vd-list"' in h2 and _esc(T_SERIES) in h2 and '1 / 1' in h2 and 'class="vd-item is-current"' in h2
        and h2.find('class="vd-main"') < h2.find('class="vd-list"'))
    chk('⑬b 올리기 블록 = 맨 위 — 편 화면에서도 머리 바로 뒤 · 재생기 · 재생목록보다 앞 (1저자 11-25) · 편이 있으면 닫힌 채',
        0 <= h2.find('class="vd-top"') < h2.find('class="vd-upload"') < h2.find('class="vd-grid"')
        and '<details class="vd-upload">' in h2)
    dd = _details(h2)
    chk(f'⑭ 토글 일곱 (details) — 챕터 · 대본 · 장면 · 참고 문헌 · QC · 기준표 · 해시 (화면 {dd})',
        dd == ['chapters', 'script', 'scenes', 'refs', 'qc', 'rubric', 'hashes'])
    ch = _region(h2, 'chapters')
    chk('⑮ 챕터 — 장면 첫 문장 시각 − lead_in (0.0 · 5.5 s) · 글 = 0:00 · 0:05 + 장면 제목 · 누르면 그 시각 (data-t)',
        'data-t="0.0"' in ch and 'data-t="5.5"' in ch and '0:00' in ch and '0:05' in ch and _esc(T_SC1) in ch and _esc(T_SC2) in ch)
    sc = _region(h2, 'scenes')
    chk('⑯ 장면 목록 — 행 = scenes.json 장면 수 (2) · 제목 · 문장 수 · 샷 수',
        sc.count('class="vd-scene-row"') == 2 and _esc(T_SC1) in sc and _esc(T_SC2) in sc)
    rf = _region(h2, 'refs')
    chk('⑰ 참고 문헌 — script.md 의 "## 참고 문헌" 절만 (다른 절 글 없음)', _esc(T_REF).split(' ')[0] in rf and T_OTHER not in rf)
    chk('⑱ 대본 토글 = script.md 렌더 (다른 절 포함)', T_SCRIPT in _region(h2, 'script') and T_OTHER in _region(h2, 'script'))
    qc = _region(h2, 'qc')
    chk('⑲ QC 요약 — qc_report 의 public 칸 (점검 · 발견) + qc.md · QC 가 본 영상 = 이 영상 (sha256 같음) 표지',
        T_FOUND in qc and T_QC in qc and 'vd-qc-match' in qc)
    chk('⑳ 내부 표지 글 (qc_report internal 칸) 이 공개판 화면 어디에도 없다 (화면이 실제로 그려진 상태에서)',
        r2.status_code == 200 and T_QC in h2 and T_SECRET not in h2 and T_SECRET not in h)
    chk('㉑ 10 점 기준표 토글 = rubric md 렌더 (표)', T_RUB in _region(h2, 'rubric') and '<table' in _region(h2, 'rubric'))
    hs = _region(h2, 'hashes')
    chk('㉒ 파일 해시 — 파일마다 sha256 전체 · 대조 표지',
        _sha(_video_bytes()) in hs and _sha(_png()) in hs and 'vd-hash-ok' in hs)
    chk('㉓ GET 화면이 등록 폴더를 바꾸지 않는다 (파일 목록 그대로)', bool(snap0) and r2.status_code == 200 and _snapshot(lib) == snap0)

    # ═══ B. 파일 — 재생 · 받기 · 자막 ═══
    vb = _video_bytes()
    r = c.get('/videos/ep99_test/media/video')
    chk('㉔ 재생 — 200 · video/mp4 · Accept-Ranges bytes · 본문 = 파일',
        r.status_code == 200 and r.mimetype == 'video/mp4' and r.headers.get('Accept-Ranges') == 'bytes' and r.data == vb)
    r = c.get('/videos/ep99_test/media/video', headers={'Range': 'bytes=0-99'})
    r_tail = c.get('/videos/ep99_test/media/video', headers={'Range': f'bytes={len(vb) - 50}-'})
    chk('㉕ Range — bytes=0-99 = 206 · Content-Range 0-99/전체 · 100 바이트 · 끝 열린 범위 = 꼬리 50 바이트',
        r.status_code == 206 and r.headers.get('Content-Range') == f'bytes 0-99/{len(vb)}' and r.data == vb[:100]
        and r_tail.status_code == 206 and r_tail.data == vb[-50:])
    r = c.get('/videos/ep99_test/media/thumbnail')
    chk('㉖ 썸네일 (poster) = image/png · 바이트 그대로', r.status_code == 200 and r.mimetype == 'image/png' and r.data == _png())
    rv = c.get('/videos/ep99_test/download/video')
    rs = c.get('/videos/ep99_test/download/subtitles')
    rm = c.get('/videos/ep99_test/download/script')
    cd = [x.headers.get('Content-Disposition') or '' for x in (rv, rs, rm)]
    chk(f'㉗ 받기 — attachment · 파일 이름 = 등록 이름 (mp4 · srt · md) ({cd})',
        all(x.status_code == 200 for x in (rv, rs, rm)) and all(s.startswith('attachment') for s in cd)
        and 'preview.mp4' in cd[0] and 'ep99.srt' in cd[1] and 'script.md' in cd[2] and rv.data == vb)
    r = c.get('/videos/ep99_test/subtitles.vtt')
    vtt = r.get_data(as_text=True)
    chk('㉘ 자막 — text/vtt · WEBVTT 머리 · 시각 쉼표 → 점 · 한 자리 시 → 두 자리 · 자막 글 그대로',
        r.status_code == 200 and r.mimetype == 'text/vtt' and vtt.startswith('WEBVTT')
        and '00:00:00.500 --> 00:00:02.000' in vtt and '00:00:02.000 --> 00:00:04.250' in vtt and T_CUE in vtt)
    s2v = getattr(V, 'srt_to_vtt', None) if have else None
    u = s2v(SRT) if s2v else ''
    chk('㉙ srt_to_vtt — BOM · CRLF · 깨진 덩어리 건너뜀 (큐 3 개) · & < 이스케이프 · 여러 줄 큐 · --> 를 글에서 막음',
        bool(u) and u.count(' --> ') == 3 and 'A &amp; B &lt;i&gt;' in u and '둘째 줄 하나\n둘째 줄 둘' in u
        and '﻿' not in u and '\r' not in u
        and ' --> ' not in (s2v('1\n00:00:01,000 --> 00:00:02,000\n화살 --> 글\n') if s2v else ' --> ').split('\n', 3)[-1])
    bad_urls = (
        '/videos/ep99_test/media/script', '/videos/ep99_test/media/scenes', '/videos/ep99_test/media/SHA256SUMS',
        '/videos/ep99_test/media/episode.json', '/videos/ep99_test/download/scenes', '/videos/ep99_test/download/qc',
        '/videos/ep99_test/download/qc_report', '/videos/ep99_test/download/timeline', '/videos/ep99_test/download/episode.json',
        '/videos/ep99_test/media/../../app.py', '/videos/ep99_test/media/..%2f..%2f..%2fapp.py',
        '/videos/ep99_test/download/%2e%2e%2fepisode.json', '/videos/..%2fep99_test/media/video', '/videos/%2e%2e/media/video',
        '/videos/nope_ep/media/video', '/videos/EP99_TEST/media/video', '/videos/ep99_test/media/Video',
        '/videos/ep99_test/media/', '/videos/ep99_test/download/', '/videos/nope_ep', '/videos/nope_ep/subtitles.vtt',
        '/videos/ep99_test/media/%2fetc%2fpasswd', '/videos/upload',
    )
    bad = []
    for u_ in bad_urls:
        rr = c.get(u_)
        body = rr.get_data(as_text=True) if rr.status_code < 500 else 'x'
        if rr.status_code != 404 or any(m in body for m in LEAK_MARKS):
            bad.append((u_, rr.status_code))
    chk(f'㉚ 등록 밖 종류 · 경로 꼴 · 모르는 편 · 대소문자 = 404 · 새는 글 없음 (같은 편의 바른 주소는 200) ({bad[:4]})',
        not bad and c.get('/videos/ep99_test/media/video').status_code == 200)

    # ═══ C. 등록부 깨짐 = fail-closed ═══
    def _copy_ep(dst_name, mut):
        d = lib / dst_name
        shutil.copytree(epd, d)
        mut(d)
        return d

    def _set_id(d, new_id):
        m = json.loads((d / 'episode.json').read_text(encoding='utf-8'))
        m['id'] = new_id
        mb = json.dumps(m, ensure_ascii=False).encode('utf-8')
        (d / 'episode.json').write_bytes(mb)
        sums = (d / 'SHA256SUMS').read_text(encoding='utf-8').splitlines()
        (d / 'SHA256SUMS').write_text('\n'.join(f'{_sha(mb)}  episode.json' if ln.endswith('  episode.json') else ln
                                                for ln in sums) + '\n', encoding='utf-8')
    cases = {
        'ep91_badjson': lambda d: (_set_id(d, 'ep91_badjson'), (d / 'episode.json').write_text('{"schema": ', encoding='utf-8')),
        'ep92_nofile': lambda d: (_set_id(d, 'ep92_nofile'), (d / 'preview.mp4').unlink()),
        'ep93_tamper': lambda d: (_set_id(d, 'ep93_tamper'),
                                  (d / 'script.md').write_bytes(b'X' + (d / 'script.md').read_bytes()[1:])),
        'ep94_wrongid': lambda d: None,                         # 폴더 이름 ≠ episode.json id (ep99_test)
        'ep95_link': lambda d: (_set_id(d, 'ep95_link'), (d / 'qc.md').unlink(), os.symlink(str(APP), d / 'qc.md')),
        'ep96_schema': lambda d: _set_schema(d, 'ep96_schema'),
    }

    def _set_schema(d, new_id):
        _set_id(d, new_id)
        m = json.loads((d / 'episode.json').read_text(encoding='utf-8'))
        m['schema'] = 'avi-episode/999'
        mb = json.dumps(m, ensure_ascii=False).encode('utf-8')
        (d / 'episode.json').write_bytes(mb)
        sums = (d / 'SHA256SUMS').read_text(encoding='utf-8').splitlines()
        (d / 'SHA256SUMS').write_text('\n'.join(f'{_sha(mb)}  episode.json' if ln.endswith('  episode.json') else ln
                                                for ln in sums) + '\n', encoding='utf-8')
    if epd.is_dir():                                    # 등록이 안 됐으면 (고치기 전) 복사할 원본이 없다 — 아래 검사가 실패로 남는다
        for k, mut in cases.items():
            _copy_ep(k, mut)
    r = c.get('/videos')
    h = r.get_data(as_text=True)
    notes = re.findall(r'<li class="vd-problem"[^>]*data-ep="([^"]+)"', h)
    chk(f'㉛ 깨진 편 여섯 = 200 + 안내 (편마다 무엇이 깨졌는지) · 재생목록에 없다 ({sorted(notes)})',
        r.status_code == 200 and sorted(notes) == sorted(cases) and all(f'href="/videos/{k}"' not in h for k in cases))
    why = {k: re.search(r'<li class="vd-problem"[^>]*data-ep="' + k + r'"[^>]*>(.*?)</li>', h, re.S) for k in cases}
    why = {k: (m.group(1) if m else '') for k, m in why.items()}
    chk('㉜ 안내 문구 — JSON 못 읽음 · 파일 없음 · sha256 다름 · 폴더 이름 ≠ id · 심볼릭 링크 · 모르는 스키마',
        '읽지 못했다' in why['ep91_badjson'] and '없다' in why['ep92_nofile'] and 'sha256' in why['ep93_tamper']
        and '폴더 이름' in why['ep94_wrongid'] and '심볼릭 링크' in why['ep95_link'] and '스키마' in why['ep96_schema'])
    bad = [k for k in cases if c.get(f'/videos/{k}/media/video').status_code != 404
           or c.get(f'/videos/{k}/download/script').status_code != 404 or c.get(f'/videos/{k}').status_code != 404]
    chk(f'㉝ 깨진 편의 화면 · 파일 주소 = 404 ({bad})', epd.is_dir() and not bad)
    leak = c.get('/videos/ep95_link/download/qc').get_data(as_text=True) + c.get('/videos/ep95_link/media/video').get_data(as_text=True)
    chk('㉞ 심볼릭 링크 편에서 링크 대상 (app.py) 글이 새지 않는다', epd.is_dir() and 'app = Flask(' not in leak)
    okv = False
    if epd.is_dir():
        vd_ = _copy_ep('ep90_vidtamper', lambda d: (_set_id(d, 'ep90_vidtamper'),
                                                    (d / 'preview.mp4').write_bytes(b'Z' + (d / 'preview.mp4').read_bytes()[1:])))
        rp_ = c.get('/videos/ep90_vidtamper')
        okv = (rp_.status_code == 404 and 'data-ep="ep90_vidtamper"' in rp_.get_data(as_text=True)
               and 'sha256' in rp_.get_data(as_text=True)
               and c.get('/videos/ep90_vidtamper/media/video').status_code == 404
               and c.get('/videos/ep90_vidtamper/download/video').status_code == 404)
        shutil.rmtree(vd_, ignore_errors=True)
    chk('㉞b 영상만 바뀐 편 (같은 크기) — 그 편 화면 = 404 + 안내 (sha256) · 영상 재생 · 받기 주소 = 404', okv)
    chk('㉟ 깨진 편이 있어도 멀쩡한 편은 그대로 재생 (200 · Range 206)',
        c.get('/videos/ep99_test').status_code == 200
        and c.get('/videos/ep99_test/media/video', headers={'Range': 'bytes=0-9'}).status_code == 206)
    for k in cases:
        p_ = lib / k
        if p_.is_symlink():
            p_.unlink()
        shutil.rmtree(p_, ignore_errors=True)

    # ═══ D. 내부판 ═══
    iep = make_ep(td / 'src' / 'internal', internal=True)
    ib = td / 'b' / 'int.zip'
    ok_r, why_r = refused(pkg, iep, 'ep98_int', ib) if have else (False, 'no lib')
    chk(f'㊱ INTERNAL 이 든 파일 이름 · internal 폴더 = --internal 없이 꾸러미 거부 ({why_r[:60]})',
        ok_r and 'INTERNAL' in why_r and not ib.exists())
    iman = {}
    if have:
        try:
            iman = pkg(iep, 'ep98_int', ib, internal=True) or {}
            V.register_bundle(ib, lib, via='cli')
        except Exception as e:                              # noqa: BLE001
            print(f'    내부판 꾸러미 · 등록 예외 — {type(e).__name__}: {e}')
    chk('㊲ --internal 이면 꾸러미 · 등록 (visibility internal)', iman.get('visibility') == 'internal' and (lib / 'ep98_int').is_dir())
    r = c.get('/videos/ep98_int')
    h = r.get_data(as_text=True)
    chk('㊳ 내부판 화면 — 빨간 배지 "내부용 · 공개 금지" · 공개 안전 배지 없음 · 받기는 된다 · 썸네일 없으면 poster 없음',
        r.status_code == 200 and 'data-badge="internal"' in h and '내부용 · 공개 금지' in h and 'data-badge="public"' not in h
        and 'href="/videos/ep98_int/download/video"' in h and 'poster=' not in (re.search(r'<video\b[^>]*>', h) or [''])[0]
        and c.get('/videos/ep98_int/download/video').status_code == 200)
    r = c.get('/videos/ep99_test')
    h = r.get_data(as_text=True)
    chk('㊴ 다른 시리즈 (내부) 는 공개 편 재생목록에 섞이지 않고 "다른 시리즈" 로 · 내부 편 목록 표지',
        _esc(T_I_TITLE) not in (re.search(r'<ol class="vd-items">(.*?)</ol>', h, re.S) or [''] * 2)[1]
        and 'href="/videos/ep98_int"' in h and 'class="vd-other"' in h)
    hi = c.get('/videos').get_data(as_text=True)
    chk('㊴b 내부판 시리즈 이름이 앞서 정렬돼도 /videos 첫 편 = 공개판 (내부판은 뒤 · 다른 시리즈로)',
        '<source src="/videos/ep99_test/media/video"' in hi and '<source src="/videos/ep98_int/media/video"' not in hi
        and T_I_SERIES < T_SERIES)

    # ═══ I. 내부판 = 이 컴퓨터에서만 (1저자 11-24 Q1 — 루프백 · 프록시 머리 없음 · 다른 컴퓨터에는 있다는 사실도 흘리지 않는다) ═══
    far = {'REMOTE_ADDR': '10.9.8.7'}

    def _far(u, **kw):
        return c.get(u, environ_base=far, **kw)
    r_int, r_none = _far('/videos/ep98_int'), _far('/videos/nope_ep')
    chk('I1 다른 컴퓨터 — 내부판 편 화면 = 404 · 등록 안 된 편과 같은 응답 (본문 바이트까지 같음)',
        r_int.status_code == 404 and r_none.status_code == 404 and r_int.get_data() == r_none.get_data()
        and T_I_TITLE.split(' ')[-1] not in r_int.get_data(as_text=True))
    bad_far = []
    for suf in ('/media/video', '/media/thumbnail', '/download/video', '/download/subtitles', '/download/script', '/subtitles.vtt'):
        a_, b_ = _far('/videos/ep98_int' + suf), _far('/videos/nope_ep' + suf)
        if a_.status_code != 404 or a_.get_data() != b_.get_data():
            bad_far.append((suf, a_.status_code))
    chk(f'I2 다른 컴퓨터 — 내부판 재생 · 받기 · 자막 주소 = 404 · 등록 안 된 편과 같은 본문 ({bad_far})', not bad_far)
    hf = _far('/videos').get_data(as_text=True)
    hf2 = _far('/videos/ep99_test').get_data(as_text=True)
    chk('I3 다른 컴퓨터 — /videos · 공개 편 화면의 목록 · 재생목록 · 다른 시리즈에 내부판 없음 (id · 제목 · 시리즈 · 내부 배지) · 첫 편 = 공개판',
        all('ep98_int' not in x and _esc(T_I_TITLE) not in x and _esc(T_I_SERIES) not in x and 'data-badge="internal"' not in x
            and 'vd-badge vd-badge-internal' not in x and 'class="vd-other"' not in x for x in (hf, hf2))
        and '<source src="/videos/ep99_test/media/video"' in hf)
    hx_ = c.get('/videos', headers={'X-Forwarded-For': '203.0.113.9'}).get_data(as_text=True)
    rx_ = c.get('/videos/ep98_int', headers={'X-Forwarded-For': '203.0.113.9'})
    rf_ = c.get('/videos/ep98_int/media/video', headers={'Forwarded': 'for=203.0.113.9'})
    chk('I4 루프백이라도 프록시를 거친 요청 (X-Forwarded-For · Forwarded) = 다른 컴퓨터와 같다 (내부판 없음 · 404)',
        'ep98_int' not in hx_ and rx_.status_code == 404 and rf_.status_code == 404)
    hl = c.get('/videos/ep98_int').get_data(as_text=True)
    chk('I5 이 컴퓨터 — 내부판 그대로 보이고 (화면 · 재생) 배지 옆 "이 컴퓨터에서만 보임"',
        'data-badge="internal"' in hl and '이 컴퓨터에서만 보임' in hl and c.get('/videos/ep98_int/media/video').status_code == 200
        and 'href="/videos/ep98_int"' in c.get('/videos/ep99_test').get_data(as_text=True))
    ok_i6 = False
    if have and ib.is_file():
        only = td / 'lib_only_internal'
        try:
            V.register_bundle(ib, only)
            cfg['VIDEO_FOLDER'] = str(only)
            ho = _far('/videos').get_data(as_text=True)
            hl2 = c.get('/videos').get_data(as_text=True)
            ok_i6 = ('등록된 편이 없습니다' in ho and 'ep98_int' not in ho and _esc(T_I_TITLE) not in ho
                     and '<source src="/videos/ep98_int/media/video"' in hl2)
        except Exception as e:                              # noqa: BLE001
            print(f'    내부판만 있는 폴더 예외 — {type(e).__name__}: {e}')
        finally:
            cfg['VIDEO_FOLDER'] = str(lib)
    chk('I6 내부판만 있는 폴더 — 다른 컴퓨터에는 "등록된 편이 없습니다" (흔적 없음) · 이 컴퓨터에는 첫 편으로 보인다', ok_i6)
    ok_i7 = False
    if (lib / 'ep98_int').is_dir():
        bi_ = lib / 'ep97_ibroken'
        shutil.copytree(lib / 'ep98_int', bi_)
        _set_id(bi_, 'ep97_ibroken')
        (bi_ / 'script.md').write_bytes(b'X' + (bi_ / 'script.md').read_bytes()[1:])
        hb_far = _far('/videos').get_data(as_text=True)
        hb_loc = c.get('/videos').get_data(as_text=True)
        ok_i7 = 'ep97_ibroken' not in hb_far and 'data-ep="ep97_ibroken"' in hb_loc
        shutil.rmtree(bi_, ignore_errors=True)
    chk('I7 깨진 내부판 편의 안내 (등록부에서 뺀 편) 도 다른 컴퓨터에는 안 보인다 · 이 컴퓨터에는 보인다', ok_i7)
    crafted = td / 'b' / 'pub_internal_name.zip'
    craft_zip(crafted, [('x_INTERNAL_y.mp4', _video_bytes(5000)), ('script.md', '# 손\n'.encode('utf-8'))])
    ok_r, why_r = refused(V.register_bundle, crafted, lib) if have else (False, '')
    chk(f'㊵ 공개판인데 INTERNAL 이름 파일 = 등록 거부 ({why_r[:50]})', ok_r and not (lib / 'ep77_craft').exists())

    # ═══ E. 꾸러미 안전 ═══
    good = [('a.mp4', _video_bytes(5000)), ('script.md', '# 손 꾸러미\n'.encode('utf-8'))]
    ok_good = False
    if have:
        craft_zip(td / 'b' / 'e0.zip', good)
        try:
            V.register_bundle(td / 'b' / 'e0.zip', td / 'lib_craft_ok')
            ok_good = (td / 'lib_craft_ok' / 'ep77_craft' / 'a.mp4').is_file()
        except Exception as e:                              # noqa: BLE001
            print(f'    손 꾸러미 (정상) 예외 — {type(e).__name__}: {e}')
    chk('㊶a 손 꾸러미 (결함 없음) 는 등록된다 — 아래 반례는 결함 **하나씩만** 다르다', ok_good)
    evil = []
    tries = {     # 이름: (꾸러미, 거부 사유에 있어야 할 낱말)
        'zipslip': (craft_zip(td / 'b' / 'e1.zip', good + [('../evil.srt', b'evil')]), '이름 꼴'),
        'subdir': (craft_zip(td / 'b' / 'e2.zip', good + [('sub/x.srt', b'x')]), '이름 꼴'),
        'absolute': (craft_zip(td / 'b' / 'e3.zip', good + [('/tmp/vdt_abs.srt', b'x')]), '이름 꼴'),
        'symlink': (craft_zip(td / 'b' / 'e4.zip', good + [('link.srt', b'/etc/passwd')], links=('link.srt',)), '일반 파일이 아니다'),
        'badsum': (craft_zip(td / 'b' / 'e5.zip', good, sums_override='0' * 64 + '  a.mp4\n'), 'SHA256SUMS'),
        'wronghash': (craft_zip(td / 'b' / 'e5b.zip', good, bad_sum_for=('script.md',)), 'sha256'),
        'nosums': (craft_zip(td / 'b' / 'e6.zip', good, sums=False), 'SHA256SUMS 가 없다'),
        'backslash': (craft_zip(td / 'b' / 'e7.zip', good + [('..\\evil.srt', b'x')]), '이름 꼴'),
        'dotfile': (craft_zip(td / 'b' / 'e8.zip', good + [('.hidden.srt', b'x')]), '이름 꼴'),
        'unlisted': (craft_zip(td / 'b' / 'e9b.zip', good + [('extra.srt', b'not listed')], not_in_manifest=('extra.srt',)), '목록'),
    }
    # SHA256SUMS 에도 없는 항목
    p9 = td / 'b' / 'e9.zip'
    craft_zip(p9, good)
    with zipfile.ZipFile(p9, 'a') as z:
        z.writestr('extra.srt', b'not listed')
    tries['unlisted_sums'] = (p9, '목록')
    # 중복 이름
    p10 = td / 'b' / 'e10.zip'
    craft_zip(p10, good)
    with zipfile.ZipFile(p10, 'a') as z:
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            z.writestr('script.md', b'dup')
    tries['duplicate'] = (p10, '같은 이름 두 번')
    # episode.json 의 크기 · sha256 이 실제와 다름
    gs = '# 손 꾸러미\n'.encode()
    m11 = dict(schema='avi-episode/1', id='ep77_craft', title='t', series='s', episode=77, visibility='public',
               duration_s=1.0, updated='2031-01-01',
               files=[dict(name='a.mp4', role='video', size=1, sha256=_sha(_video_bytes(5000))),
                      dict(name='script.md', role='script', size=len(gs), sha256=_sha(gs))],
               public_check=dict(ok=True))
    tries['badsize'] = (craft_zip(td / 'b' / 'e11.zip', good, manifest=m11), '크기')
    m11b = dict(m11, files=[dict(m11['files'][0], size=5000), dict(m11['files'][1], sha256='f' * 64)])
    tries['badmanhash'] = (craft_zip(td / 'b' / 'e11b.zip', good, manifest=m11b), 'episode.json 과 다르다')
    m12 = dict(m11, files=[dict(m11['files'][0], size=5000), m11['files'][1]], id='../../evil')
    tries['badid'] = (craft_zip(td / 'b' / 'e12.zip', good, manifest=m12), '편 id 꼴')
    m13 = dict(m11, files=[dict(m11['files'][0], size=5000), m11['files'][1]], visibility='secret')
    tries['badvis'] = (craft_zip(td / 'b' / 'e13.zip', good, manifest=m13), '공개 범위')
    (td / 'b' / 'e14.zip').write_bytes(b'not a zip at all')
    tries['notzip'] = (td / 'b' / 'e14.zip', 'zip 이 아니다')
    before = _snapshot(lib)
    for k, (p_, word) in tries.items():
        ok_r, why_r = refused(V.register_bundle, p_, lib) if have else (False, '')
        if not ok_r or word not in why_r:
            evil.append((k, why_r[:70]))
    chk(f'㊶ 위험한 꾸러미 열여덟 (zip-slip · 하위 폴더 · 절대 경로 · 심볼릭 링크 · 해시 둘 · SHA256SUMS 없음 · 역슬래시 · 점 파일 · '
        f'목록 밖 둘 · 중복 · 크기 · episode.json sha256 · id 꼴 · 공개 범위 · zip 아님) = 전부 거부 · 사유 = 그 결함 ({evil[:3]})',
        have and not evil)
    chk('㊷ 거부된 꾸러미는 아무것도 남기지 않는다 (등록 폴더 그대로 · 폴더 밖 evil 없음 · 임시 자리 비움)',
        have and bool(before) and _snapshot(lib) == before and not (td / 'evil.srt').exists()
        and not (lib.parent / 'evil.srt').exists() and not Path('/tmp/vdt_abs.srt').exists())
    # 크기 상한 (낮춘 상한으로)
    ok_r, why_r = refused(V.register_bundle, bun, td / 'lib_cap', caps=dict(max_file=1000)) if have else (False, '')
    chk(f'㊸ 크기 상한 — 파일 하나가 상한을 넘으면 거부 ({why_r[:50]})', ok_r and not (td / 'lib_cap' / 'ep99_test').exists())
    # 이미 있는 편
    ok_r, why_r = refused(V.register_bundle, bun, lib) if have else (False, '')
    chk(f'㊹ 이미 있는 편 = 거부 (바꾸기는 명시) ({why_r[:50]})', ok_r and '이미' in why_r)
    rep = {}
    if have:
        try:
            rep = V.register_bundle(bun, lib, replace=True, via='cli') or {}
        except Exception as e:                              # noqa: BLE001
            print(f'    replace 예외 — {type(e).__name__}: {e}')
    olds = sorted((lib / '.replaced').glob('ep99_test__*')) if (lib / '.replaced').is_dir() else []
    chk('㊺ replace=True — 새 판 설치 · 옛 판은 .replaced/ 로 옮겨 보관 (지우지 않음) · 목록에 .replaced 가 안 나온다',
        bool(rep) and (lib / 'ep99_test' / 'episode.json').is_file() and len(olds) == 1 and (olds[0] / 'episode.json').is_file()
        and '.replaced' not in c.get('/videos').get_data(as_text=True))
    # 공개 안전 검사
    hp = make_ep(td / 'src' / 'homepath', extra_md='작업 폴더 /home/someone/avi_work/x 를 본다', qc_secret=False)
    ok_r, why_r = refused(pkg, hp, 'ep89_home', td / 'b' / 'home.zip') if have else (False, '')
    chk(f'㊻ 공개 안전 검사 — 공개판 글에 홈 경로 = 꾸러미 거부 (규칙 이름 · 파일 · 줄) ({why_r[:70]})',
        ok_r and '홈 경로' in why_r and 'script.md' in why_r)
    ok_i = False
    if have:
        hpi = make_ep(td / 'src' / 'homepath_i', internal=True, extra_md='작업 폴더 /home/someone/x')
        try:
            mi = pkg(hpi, 'ep88_homei', td / 'b' / 'homei.zip', internal=True)
            ok_i = (mi or {}).get('public_check', {}).get('ok') is False
        except Exception as e:                              # noqa: BLE001
            print(f'    내부판 공개 검사 예외 — {type(e).__name__}: {e}')
    chk('㊼ 내부판은 같은 검사를 기록만 한다 (걸려도 꾸러미 · ok False)', ok_i)
    port_ep = make_ep(td / 'src' / 'port', extra_md='주소 example.org:8443 · localhost 에서', qc_secret=False)
    ok_r, why_r = refused(pkg, port_ep, 'ep87_port', td / 'b' / 'port.zip') if have else (False, '')
    chk(f'㊽ 주소 · 포트 · localhost = 공개판 거부 ({why_r[:60]})', ok_r and ('포트' in why_r or 'localhost' in why_r))
    deny = td / 'deny.txt'
    deny.write_text(f'# 시험 내부 숫자\n{T_DENY}\n', encoding='utf-8')
    dep = make_ep(td / 'src' / 'deny', extra_md=f'숫자 {T_DENY} %', qc_secret=False)
    ok_r, why_r = refused(pkg, dep, 'ep86_deny', td / 'b' / 'deny.zip', deny_list=deny) if have else (False, '')
    chk(f'㊾ 내부 숫자 목록 (--deny-list) — 공개판 글에 있으면 거부 · 사유에 값을 적지 않는다 ({why_r[:60]})',
        ok_r and T_DENY not in why_r and '내부 숫자 목록' in why_r)
    ok50 = False
    if have:
        try:
            m50 = pkg(ep, 'ep85_deny_ok', td / 'b' / 'denyok.zip', deny_list=deny) or {}
            pc = m50.get('public_check') or {}
            ok50 = pc.get('ok') is True and (pc.get('deny_list') or {}).get('n') == 1 and T_DENY not in json.dumps(m50)
        except Exception as e:                              # noqa: BLE001
            print(f'    deny 통과 예외 — {type(e).__name__}: {e}')
    chk('㊿ 내부 숫자 목록에 안 걸리면 통과 · episode.json 에 목록 개수 · sha256 만 (값 없음)', ok50)
    bans = []
    try:
        import ledger_view
        bans = [b.get('pattern') for b in ledger_view._load()['bans'] if b.get('pattern')]
    except Exception:                                        # noqa: BLE001
        pass
    ok51 = False
    if have and bans:
        bp = make_ep(td / 'src' / 'ban', extra_md='인용: ' + bans[0], qc_secret=False)
        r51, w51 = refused(pkg, bp, 'ep84_ban', td / 'b' / 'ban.zip')
        ok51 = r51 and '철회값' in w51 and bans[0] not in w51
    chk(f'51 철회값 (claims.json quotation_ban · 실행 중에 읽음 · {len(bans)} 개) — 공개판 글에 있으면 거부 · 사유에 값 없음', ok51)
    ok52 = ok52b = False
    if have:
        d2 = make_ep(td / 'src' / 'two_mp4')
        (d2 / 'other.mp4').write_bytes(b'x')
        ok52, _w = refused(pkg, d2, 'ep83_two', td / 'b' / 'two.zip')
        try:
            m52 = pkg(d2, 'ep83_two', td / 'b' / 'two.zip', video=d2 / 'preview.mp4') or {}
            ok52b = [f['name'] for f in m52.get('files', []) if f.get('role') == 'video'] == ['preview.mp4']
        except Exception as e:                              # noqa: BLE001
            print(f'    --video 예외 — {type(e).__name__}: {e}')
    chk('52 mp4 가 둘이면 거부 · --video 로 고르면 그 하나만', ok52 and ok52b)
    ok53 = False
    if have:
        ok53 = all(refused(pkg, ep, bad_id, td / 'b' / 'x.zip')[0] for bad_id in ('EP01', '../x', 'a', 'upload', 'ep 1', 'ep01/x', ''))
    chk('53 편 id 꼴 — 소문자 · 숫자 · 밑줄 (2–64) · 예약어 upload 거부', ok53)

    # ═══ F. 웹 올리기 — 같은 함수 ═══
    up_lib = td / 'lib_up'
    cfg['VIDEO_FOLDER'] = str(up_lib)

    def _post(p_, **kw):
        data = {'bundle': (io.BytesIO(Path(p_).read_bytes() if Path(p_).is_file() else b''), Path(p_).name)}
        data.update(kw.pop('form', {}))
        return c.post('/videos/upload', data=data, content_type='multipart/form-data', **kw)
    r = _post(bun)
    chk('54 올리기 (로컬) — 303 → /videos/ep99_test · 등록됨 · registration.json via web',
        r.status_code in (302, 303) and r.headers.get('Location', '').endswith('/videos/ep99_test')
        and (up_lib / 'ep99_test' / 'preview.mp4').is_file()
        and json.loads((up_lib / 'ep99_test' / 'registration.json').read_text(encoding='utf-8')).get('via') == 'web'
        if (up_lib / 'ep99_test' / 'registration.json').is_file() else False)
    r = _post(bun)
    chk('55 이미 있는 편 = 409 + 안내 (바꾸기 표시 없이)', r.status_code == 409 and '이미' in r.get_data(as_text=True))
    chk('55b 올리기 오류 화면 = 올리기 블록이 열린 채 (안내 바로 위 · 다시 고르기)',
        '<details class="vd-upload" open>' in r.get_data(as_text=True))
    r = _post(bun, form={'replace': '1'})
    chk('56 바꾸기 표시 (replace=1) = 303 · 옛 판 보관', r.status_code in (302, 303) and len(list((up_lib / '.replaced').glob('ep99_test__*'))) == 1)
    snap = _snapshot(up_lib)
    r = _post(bun, environ_base={'REMOTE_ADDR': '10.1.2.3'})
    r_fwd = _post(bun, headers={'X-Forwarded-For': '203.0.113.9'}, form={'replace': '1'})
    r_xo = _post(bun, headers={'Origin': 'http://evil.example'}, form={'replace': '1'})
    chk('57 로컬 밖 · 프록시 거친 요청 · 다른 출처 = 403 · 아무것도 바뀌지 않음',
        r.status_code == 403 and r_fwd.status_code == 403 and r_xo.status_code == 403 and _snapshot(up_lib) == snap)
    r = _post(tries['zipslip'][0])
    r2_ = _post(tries['notzip'][0])
    chk('58 깨진 · 위험한 꾸러미 = 400 + 안내 · 아무것도 바뀌지 않음 · 임시 파일 안 남음',
        r.status_code == 400 and r2_.status_code == 400 and _snapshot(up_lib) == snap)
    r = c.post('/videos/upload', data={}, content_type='multipart/form-data')
    chk('59 파일 없이 올리기 = 400', r.status_code == 400)
    tests_lib_ok = False
    if have:
        old_cap = getattr(V, 'MAX_BUNDLE_BYTES', None)
        try:
            V.MAX_BUNDLE_BYTES = 1000
            r = _post(bun, form={'replace': '1'})
            tests_lib_ok = r.status_code == 413 and _snapshot(up_lib) == snap
        finally:
            if old_cap is not None:
                V.MAX_BUNDLE_BYTES = old_cap
    chk('60 꾸러미 크기 상한 넘음 = 413 · 아무것도 바뀌지 않음', tests_lib_ok)

    # ═══ G. 명령 ═══
    cli_lib = td / 'lib_cli'
    env = dict(os.environ)
    for k in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE'):
        env.pop(k, None)
    env['WEBAPP_VIDEO_FOLDER'] = str(td / 'lib_env_default')

    def run(*args):
        p = subprocess.run([sys.executable, '-I', *map(str, args)], capture_output=True, text=True, env=env, cwd=str(td))
        return p.returncode, p.stdout + p.stderr
    out_zip = td / 'b' / 'cli.zip'
    rc1, o1 = run(PKG, ep, '--id', 'ep97_cli', '-o', out_zip, '--no-probe') if PKG.is_file() else (99, 'no script')
    rc2, o2 = run(REG, out_zip, '--folder', cli_lib) if REG.is_file() else (99, 'no script')
    rc3, o3 = run(REG, out_zip, '--folder', cli_lib) if REG.is_file() else (99, 'no script')
    rc4, o4 = run(REG, out_zip, '--folder', cli_lib, '--replace') if REG.is_file() else (99, 'no script')
    chk(f'61 명령 — 꾸러미 rc 0 · 등록 rc 0 · 같은 꾸러미 다시 rc 1 (이미 있음) · --replace rc 0 ({rc1, rc2, rc3, rc4})',
        (rc1, rc2, rc3, rc4) == (0, 0, 1, 0) and (cli_lib / 'ep97_cli' / 'episode.json').is_file() and '이미' in o3)
    rc5, o5 = run(REG, ep, '--id', 'ep96_dir', '--folder', cli_lib, '--no-probe') if REG.is_file() else (99, '')
    reg5 = cli_lib / 'ep96_dir' / 'registration.json'
    chk('62 폴더를 바로 등록 (같은 함수 — 꾸러미를 만들어 같은 등록) rc 0 · bundle_sha256 기록',
        rc5 == 0 and reg5.is_file() and len(json.loads(reg5.read_text(encoding='utf-8')).get('bundle_sha256', '')) == 64)
    rc6, o6 = run(PKG, iep, '--id', 'ep95_cli', '-o', td / 'b' / 'cli_i.zip', '--no-probe') if PKG.is_file() else (99, '')
    no_zip6 = not (td / 'b' / 'cli_i.zip').exists()
    rc7, o7 = run(PKG, iep, '--id', 'ep95_cli', '-o', td / 'b' / 'cli_i.zip', '--no-probe', '--internal') if PKG.is_file() else (99, '')
    chk(f'63 명령 — INTERNAL 이름 = --internal 없이 rc 1 (꾸러미 안 만듦) · 있으면 rc 0 ({rc6, rc7})',
        rc6 == 1 and 'INTERNAL' in o6 and no_zip6 and rc7 == 0 and (td / 'b' / 'cli_i.zip').is_file())
    rc8, o8 = run(REG, out_zip) if REG.is_file() else (99, '')
    chk('64 --folder 없으면 WEBAPP_VIDEO_FOLDER (환경) 를 쓴다 — app.py 와 같은 규칙',
        rc8 == 0 and (td / 'lib_env_default' / 'ep97_cli' / 'episode.json').is_file()
        and "os.environ.get('WEBAPP_VIDEO_FOLDER')" in app_src)
    chk('65 명령 출력에 원본 폴더 절대 경로 · 홈 경로를 episode.json 에 남기지 않는다 (명령 꾸러미 검사)',
        rc1 == 0 and str(td) not in zipfile.ZipFile(out_zip).read('episode.json').decode('utf-8'))

    # ═══ J. 내부 숫자 목록 = 편 폴더 internal/ 의 목록을 늘 (1저자 11-24 Q2 — --deny-list 없이도 · fail-closed · 목록 파일은 꾸러미 · 리포 밖) ═══
    DN = getattr(V, 'DENY_LIST_NAME', 'public_deny_list.txt') if have else 'public_deny_list.txt'

    def _ztext(p):
        with zipfile.ZipFile(p) as z:
            return b''.join(z.read(n) for n in z.namelist() if not n.endswith(('.mp4', '.png'))).decode('utf-8', 'replace')
    aj = make_ep(td / 'src' / 'auto_deny', extra_md=f'내부 숫자 {T_DENY} 를 실수로 적었다', qc_secret=False)
    (aj / 'internal').mkdir()
    (aj / 'internal' / DN).write_text(f'# 시험 내부 숫자\n{T_DENY}\n', encoding='utf-8')
    ok_r, why_r = refused(pkg, aj, 'ep80_auto', td / 'b' / 'auto.zip') if have else (False, '')
    chk(f'J1 편 폴더 internal/{DN} = --deny-list 없이도 늘 검사 · 걸리면 꾸러미 안 만듦 · 사유에 값 없음 ({why_r[:50]})',
        ok_r and '내부 숫자 목록' in why_r and T_DENY not in why_r and not (td / 'b' / 'auto.zip').exists())
    ok_j2 = False
    if have:
        aj2 = make_ep(td / 'src' / 'auto_deny_ok', qc_secret=False)
        (aj2 / 'internal').mkdir()
        (aj2 / 'internal' / DN).write_text(f'{T_DENY}\n88.456\n', encoding='utf-8')
        try:
            mj = pkg(aj2, 'ep79_auto', td / 'b' / 'auto_ok.zip') or {}
            dl_ = (mj.get('public_check') or {}).get('deny_list') or {}
            nm_ = zip_names(td / 'b' / 'auto_ok.zip')
            zt_ = _ztext(td / 'b' / 'auto_ok.zip')
            ok_j2 = (dl_.get('n') == 2 and [x.get('source') for x in dl_.get('lists') or []] == ['auto'] and DN not in nm_
                     and not any(DN in n or n.startswith('internal') for n in nm_) and T_DENY not in zt_ and '88.456' not in zt_)
        except Exception as e:                              # noqa: BLE001
            print(f'    자동 목록 통과 예외 — {type(e).__name__}: {e}')
    chk(f'J2 안 걸리면 꾸러미 · episode.json = 목록 개수 2 · 출처 auto · 꾸러미 파일 목록에 {DN} 없음 · 목록 값 없음', ok_j2)
    vh = td / 'src' / 'vidhome'
    (vh / 'internal').mkdir(parents=True)
    (vh / 'internal' / DN).write_text(f'{T_DENY}\n', encoding='utf-8')
    (vh / 'final.mp4').write_bytes(_video_bytes())
    aj3 = make_ep(td / 'src' / 'textonly', extra_md=f'값 {T_DENY}', qc_secret=False)
    ok_r3, why_r3 = refused(pkg, aj3, 'ep76_vid', td / 'b' / 'vid.zip', video=vh / 'final.mp4') if have else (False, '')
    chk('J3 --video 로 고른 영상의 폴더 internal/ 목록도 늘 검사 (글 = 리포 사본 · 영상 = 작업 폴더 꼴)',
        ok_r3 and '내부 숫자 목록' in why_r3 and not (td / 'b' / 'vid.zip').exists())
    aj4 = make_ep(td / 'src' / 'bad_list', qc_secret=False)
    (aj4 / 'internal').mkdir()
    (aj4 / 'internal' / DN).write_text('ab\n', encoding='utf-8')
    ok_r4, why_r4 = refused(pkg, aj4, 'ep75_badlist', td / 'b' / 'badlist.zip') if have else (False, '')
    aj5 = make_ep(td / 'src' / 'dir_list', qc_secret=False)
    (aj5 / 'internal' / DN).mkdir(parents=True)
    ok_r5, why_r5 = refused(pkg, aj5, 'ep74_dirlist', td / 'b' / 'dirlist.zip') if have else (False, '')
    chk(f'J4 목록 자리가 깨졌으면 (너무 짧은 줄 · 파일이 아닌 것) 꾸러미 안 만듦 (fail-closed) ({why_r4[:40]} / {why_r5[:40]})',
        ok_r4 and ok_r5 and '내부 숫자 목록' in why_r4 and '내부 숫자 목록' in why_r5)
    ok_j5 = False
    if have:
        ij = make_ep(td / 'src' / 'int_with_list', internal=True, extra_md=f'내부 값 {T_DENY}')
        (ij / 'internal').mkdir()
        (ij / 'internal' / DN).write_text(f'{T_DENY}\n', encoding='utf-8')
        (ij / DN).write_text(f'{T_DENY}\n', encoding='utf-8')          # 내부판 폴더 맨 위에 목록 (작업 폴더 꼴)
        try:
            mi_ = pkg(ij, 'ep73_int', td / 'b' / 'int_list.zip', internal=True) or {}
            ok_j5 = (mi_.get('visibility') == 'internal' and (mi_.get('public_check') or {}).get('deny_list') is None
                     and DN not in zip_names(td / 'b' / 'int_list.zip'))
        except Exception as e:                              # noqa: BLE001
            print(f'    내부판 목록 예외 — {type(e).__name__}: {e}')
    chk(f'J5 내부판 꾸러미 = 목록 검사 안 함 (지금과 같음) · 목록 파일 ({DN}) 은 내부판 꾸러미에도 안 들어간다', ok_j5)
    rcj, oj = run(PKG, aj, '--id', 'ep72_autocli', '-o', td / 'b' / 'autocli.zip', '--no-probe') if PKG.is_file() else (99, '')
    chk('J6 명령도 같다 — --deny-list 없이 rc 1 · 사유 = 내부 숫자 목록 · 값 없음 · 꾸러미 없음',
        rcj == 1 and '내부 숫자 목록' in oj and T_DENY not in oj and not (td / 'b' / 'autocli.zip').exists())
    genv = {k: v for k, v in os.environ.items() if k not in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE')}
    ign = [subprocess.run(['git', '-C', str(ROOT), 'check-ignore', '-q', pth], env=genv).returncode == 0
           for pth in (f'docs/avi/ep01_mixer/internal/{DN}', f'docs/avi/{DN}', f'webapp/{DN}', 'docs/avi/ep02_x/internal/a.md')]
    chk(f'J7 리포 — docs/avi 아래 internal/ 와 목록 파일 이름 ({DN}) 은 어디서나 git 이 무시한다 ({ign})', all(ign))

    # ═══ H. 위생 ═══
    in_tpl = [t for t in ALL_TOKENS + EP01_SNIPS if t in tpl]
    in_code = [t for t in ALL_TOKENS + EP01_SNIPS if t in lib_src or t in app_src]
    chk(f'66 템플릿 · app.py · 라이브러리에 자료 값 · 문장 없음 (발견 {in_tpl + in_code})',
        bool(tpl) and bool(lib_src) and not in_tpl and not in_code)
    xss = make_ep(td / 'src' / 'xss', qc_secret=False,
                  extra_md="<script>alert('VDX1')</script>\n\n[누름](javascript:alert('VDX2'))\n\n"
                           "<img src=x onerror=alert('VDX3')>\n\n<a href=\"data:text/html,VDX4\">d</a>\n\n<!-- VDX5 -->")
    xlib = td / 'lib_xss'
    ok67 = False
    if have:
        try:
            pkg(xss, 'ep82_xss', td / 'b' / 'xss.zip')
            V.register_bundle(td / 'b' / 'xss.zip', xlib)
            cfg['VIDEO_FOLDER'] = str(xlib)
            hx = c.get('/videos/ep82_xss').get_data(as_text=True)
            ok67 = ("<script>alert('VDX1')" not in hx and re.search(r'<[a-zA-Z][^>]*\son[a-z]+\s*=', hx) is None
                    and re.search(r'(?:href|src)\s*=\s*["\']?\s*(?:javascript|data):', hx, re.I) is None
                    and '<img src=x' not in hx and '<img src="x"' not in hx and '<!-- VDX5' not in hx and 'VDX1' in hx)
        except Exception as e:                              # noqa: BLE001
            print(f'    xss 예외 — {type(e).__name__}: {e}')
    chk('67 md 속 HTML · javascript: · data: 링크 · on… 속성 · img · 주석 = 무력화 (글은 글로 보인다)', ok67)
    ok68 = False
    if have:
        tdir = make_ep(td / 'src' / 'esc', qc_secret=False)
        sj = json.loads((tdir / 'scenes.json').read_text(encoding='utf-8'))
        sj['title'] = '<b>VDX6</b> & 제목'
        (tdir / 'scenes.json').write_text(json.dumps(sj, ensure_ascii=False), encoding='utf-8')
        try:
            pkg(tdir, 'ep81_esc', td / 'b' / 'esc.zip')
            V.register_bundle(td / 'b' / 'esc.zip', xlib)
            he = c.get('/videos/ep81_esc').get_data(as_text=True)
            ok68 = '&lt;b&gt;VDX6&lt;/b&gt; &amp; 제목' in he and '<b>VDX6</b>' not in he
        except Exception as e:                              # noqa: BLE001
            print(f'    이스케이프 예외 — {type(e).__name__}: {e}')
    chk('68 제목 · 시리즈 같은 자료 글은 이스케이프된다', ok68)
    pl_ok = False
    if have:
        a2 = make_ep(td / 'src' / 'ep02x', qc_secret=False)
        sj = json.loads((a2 / 'scenes.json').read_text(encoding='utf-8'))
        sj['title'] = 'VDX-SECOND'
        (a2 / 'scenes.json').write_text(json.dumps(sj, ensure_ascii=False), encoding='utf-8')
        a1 = make_ep(td / 'src' / 'ep01x', qc_secret=False)
        sj1 = json.loads((a1 / 'scenes.json').read_text(encoding='utf-8'))
        sj1['title'] = 'VDX-FIRST'
        (a1 / 'scenes.json').write_text(json.dumps(sj1, ensure_ascii=False), encoding='utf-8')
        pl = td / 'lib_pl'
        try:
            pkg(a2, 'ep02_x', td / 'b' / 'p2.zip')
            pkg(a1, 'ep01_x', td / 'b' / 'p1.zip')
            V.register_bundle(td / 'b' / 'p2.zip', pl)
            V.register_bundle(td / 'b' / 'p1.zip', pl)
            cfg['VIDEO_FOLDER'] = str(pl)
            hp_ = c.get('/videos').get_data(as_text=True)
            hq = c.get('/videos/ep02_x').get_data(as_text=True)
            items = re.search(r'<ol class="vd-items">(.*?)</ol>', hp_, re.S)
            items = items.group(1) if items else ''
            pl_ok = (0 <= items.find('VDX-FIRST') < items.find('VDX-SECOND') and 'VDX-FIRST' in hp_.split('class="vd-list"')[0]
                     and '2 / 2' in hq and '1 / 2' in hp_)
        except Exception as e:                              # noqa: BLE001
            print(f'    재생목록 예외 — {type(e).__name__}: {e}')
    chk('69 재생목록 — 편 번호 순 (ep01 → ep02) · /videos = 첫 편 · n / N', pl_ok)
    chk('70 app.py 는 영상 라이브러리를 라우트 안에서만 부른다 (모듈 수준 import 없음 — 망 정지 경로 밖) · 194 실행기 분류표에 사유',
        re.search(r'^import video_library|^from video_library', app_src, re.M) is None
        and re.search(r'^\s+import video_library', app_src, re.M) is not None
        and "('webapp/app.py', 'video_library')" in (ROOT / 'scripts' / 'run_network_194_parallel.py').read_text(encoding='utf-8'))

    print(f'\ntest_video_page: {_ok}/{_ok + len(_fail)} PASS' + (f'   FAILED: {_fail}' if _fail else ''))
    return 1 if _fail else 0


if __name__ == '__main__':
    raise SystemExit(main())
