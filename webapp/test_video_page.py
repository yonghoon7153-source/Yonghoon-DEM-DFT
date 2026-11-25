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
  K 공개판 다시 짜기 (Codex 11-25 AVI-02 · 1저자 11-25 Q1 · Q2 (가))
           K1 git 커밋 식별자 (임시 저장소 커밋 · git 을 못 쓰면 걸림) · K2 제작 표지 · K3 공개판 역할 (제작 기록 뺌 · excluded · derived) ·
           K4 시청자 대본 (장면 제목 · 문장 글 · 공개 참고 문헌 목록 줄) · K5 장면 공개 투영 (챕터 · 장면 목록 그대로) · K6 내부판 = 그대로 ·
           K7 내부 숫자 목록 = 수 경계 · K8 등록도 같은 기준 (공개판 역할 · 투영 꼴) · K9 docs/avi/tools 옮긴 도구 (같은 폴더 모듈 · torch 늦게) ·
           K10 걸린 공개판 = 공개 보류 (다른 컴퓨터에는 없는 편 · 이 컴퓨터에는 빨간 배지 · Q4 P1-2) ·
           K10d–f 공개 보류 가드 (장면 투영 · 캐시 열쇠 = SHA256SUMS · TTL = 시계 주입 · Q4 3 회차 M5 · M6 · M6b) ·
           K11 영상 ↔ 시간표 ↔ 자막 판 대조 (MP4 길이 · 자막 수 · 자막 마지막 줄 · 자막 끝 ≤ MP4 · Q4 P2-6 · N4) ·
           K11c 공개판 = MP4 길이를 못 재면 거부 · 내부판 = 미측정 기록 (Q4 3 회차 P2-1) ·
           K12 장면 파일 문장 ↔ 시간표 문장 (Q4 3 회차 P2-2) · K12b 공개판 = 대조 다섯을 다 잰다 ·
           K13 등록 = 공개판은 판 대조 기록 (다 잰 통과) 필수 · K13b 기록 없는 등록된 공개판 = 공개 보류 (Q4 3 회차 N10)
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
#: 장면 파일 · 제작 대본의 칸 (K4 · K5) — 문장 글 · 자막 = 공개판에 남고, 읽는 꼴 · 메모 · 화면 개체 · 제작 이력 · 참고 문헌 머리 설명 ·
#: 목록 밖 줄 · 들여쓴 줄 · README = 공개판 어디에도 없어야 한다.
T_LINE1, T_LINE2, T_LINE3 = '첫 문장 VDT-LINE1-2231', '둘째 문장 VDT-LINE2-3342', '셋째 문장 VDT-LINE3-4453'
T_CAP = 'VDT-CAP-4342'
T_SAY = 'VDT-SAY-5564'
T_MEMO = 'VDT-MEMO-6675'
T_ELEM = 'VDT-ELEM-7786'
T_HIST = 'VDT-HIST-8897'
T_REF2 = 'VDT-REF2-2041 외 (2032)'
T_REFHEAD = 'VDT-REFHEAD-9908'
T_REFNOTE = 'VDT-REFNOTE-1019'
T_SUBNOTE = 'VDT-SUBNOTE-2120'
T_README = 'VDT-README-3231'
T_VOICE = 'tc_' + '0f' * 12                # 목소리 ID 꼴 (합성 · 실제 ID 아님)
ALL_TOKENS = (T_TITLE, T_SUB, T_SERIES, T_SC1, T_SC2, T_REF, T_OTHER, T_SCRIPT, T_QC, T_RUB, T_SECRET, T_FOUND, T_CUE,
              T_I_TITLE, T_I_SERIES, T_LINE1, T_LINE2, T_LINE3, T_CAP, T_SAY, T_MEMO, T_ELEM, T_HIST, T_REF2, T_REFHEAD,
              T_REFNOTE, T_SUBNOTE, T_README)
#: 공개판 꾸러미에 있으면 안 되는 제작 쪽 글 (K3 · K4 · K5)
PROD_ONLY = (T_SCRIPT, T_OTHER, T_HIST, T_REFHEAD, T_REFNOTE, T_SUBNOTE, T_SAY, T_MEMO, T_ELEM, T_QC, T_RUB, T_SECRET, T_FOUND,
             T_README, T_VOICE)
#: ep01 (믹서) 실제 글의 조각 — 템플릿 · 코드에 베껴 두면 안 된다 (자료를 고치면 화면이 같이 바뀌어야 한다).
EP01_SNIPS = ('가루는 왜', '끼리끼리', '전고체 배터리 연구 노트', '본드 수', '정렬 혼합')
#: 합성 영상의 "잰 길이" (ffprobe 흉내) — 합성 바이트는 진짜 mp4 가 아니라 ffprobe 가 못 잰다.  공개판은 MP4 길이를 못 재면 거부하므로
#: (Q4 3 회차 P2-1) 시험 안의 꾸러미는 이 값으로 잰 것처럼 만든다 (= 합성 시간표 끝 12.5 s).  진짜 ffprobe 길 = K11c (PATH 에 ffprobe 없음).
FAKE_MP4_S = 12.5
_REAL_PROBE = []                            # main() 이 진짜 video_library._probe_duration 을 담는다 (K11c)
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


def make_ep(d, *, internal=False, mp4_name=None, extra_md=None, extra_text=None, qc_secret=True, history_sha=None):
    """합성 편 폴더 → 경로.  internal=True 면 INTERNAL 이름 파일 (내부판 꼴).

    제작 대본 = 제작 이력 줄 (제작 표지 · history_sha 가 있으면 커밋 식별자) · 참고 문헌 절 (머리 괄호 설명 · 목록 줄 둘 · 들여쓴 줄 ·
    목록 밖 줄) · 다른 절.  장면 파일 = 제작 칸 (읽는 꼴 · 메모 · 감정 · 강조 · 빠르기 · 쉼 · 화면 개체 · 목소리 모형 · 썸네일) 이 든 꼴.
    extra_md = 제작 대본 끝에 붙인다 (공개판의 시청자 대본에는 안 들어간다 — 내부판 · 제작 쪽 글) ·
    extra_text = 장면 문장 글 하나를 더한다 (공개판 글 = 시청자 대본 · 공개 장면 — 공개 안전 검사가 보는 자리)."""
    d = Path(d)
    d.mkdir(parents=True, exist_ok=True)
    vb = _video_bytes()
    name = mp4_name or ('clip_INTERNAL_x.mp4' if internal else 'preview.mp4')
    (d / name).write_bytes(vb)
    if not internal:
        (d / 'thumbnail.png').write_bytes(_png())
    (d / (name[:-4] + '.srt' if internal else 'ep99.srt')).write_text(SRT, encoding='utf-8', newline='')
    hist = (f'- v1 ({T_HIST} · 1저자 11-25 지시) · 목소리 {T_VOICE} · voice-auto · DECISIONS.md · internal/ 폴더'
            + (f' · 커밋 `{history_sha}`' if history_sha else ''))
    head = f'## 참고 문헌 (시험 {T_REFHEAD}' + (f' · v1 = `{history_sha}` 에서 확인' if history_sha else '') + ')'
    script = (f'# 대본 {T_SCRIPT}\n\n## 판 · 바뀐 것\n\n{hist}\n\n{head}\n\n'
              f'1. {T_REF} · *가짜 학술지* 1, 2 (2031)\n   - 들여쓴 메모 {T_SUBNOTE}\n2. {T_REF2} · *가짜 학술지* 3, 4 (2032)\n\n'
              f'주: 목록 밖 줄 {T_REFNOTE}\n\n## 다른 절\n\n{T_OTHER}\n')
    if extra_md:
        script += '\n' + extra_md + '\n'
    (d / 'script.md').write_text(script, encoding='utf-8')
    l01 = dict(id='s01_l01', text=T_LINE1, say=T_SAY, captions=[T_CAP, '자막 둘'], pause_after=0.4, speed=1.0, emotion='차분',
               emphasis=['첫'], memo=T_MEMO)
    l02 = dict(id='s01_l02', text=T_LINE2, say='둘째 읽는 꼴', captions=['자막 셋'], pause_after=0.4, memo='메모 둘')
    l03 = dict(id='s02_l01', text=T_LINE3, say='셋째 읽는 꼴', captions=['자막 넷'], joins_prev=True)
    s2_lines = [l03] + ([dict(id='s02_l02', text=extra_text, say='덧 읽는 꼴', captions=['덧 자막'])] if extra_text else [])
    scenes = dict(episode='ep99_test', title=T_I_TITLE if internal else T_TITLE, subtitle=T_SUB,
                  series=T_I_SERIES if internal else T_SERIES, fps=30, width=1920, height=1080,
                  voice_model=dict(lead_in=0.7, base_rate=7.2), caption_max_chars=22, end_card_s=5.5,
                  thumb=dict(lines=['썸네일 줄'], highlight='줄'),
                  scenes=[dict(id='s01', title=T_SC1, lines=[l01, l02],
                               shots=[dict(id='s01a', pre=0.6, elements=[dict(id='e1', type='text', text=T_ELEM)],
                                           **{'from': 's01_l01'})]),
                          dict(id='s02', title=T_SC2, lines=s2_lines,
                               shots=[dict(id='s02a', **{'from': 's02_l01'}), dict(id='s02b', **{'from': 's02_l01'})])])
    (d / 'scenes.json').write_text(json.dumps(scenes, ensure_ascii=False), encoding='utf-8')
    #  시간표 = 장면 파일의 문장을 그대로 잇는다 (avi_timeline.all_lines 꼴 — id · 글) · extra_text 문장도 (같은 빌드 · K12)
    tl_lines = [dict(id='s01_l01', text=T_LINE1, scene='s01', t0=0.7, t1=2.0, pause=0.4),
                dict(id='s01_l02', text=T_LINE2, scene='s01', t0=2.4, t1=4.0, pause=0.4),
                dict(id='s02_l01', text=T_LINE3, scene='s02', t0=6.2, t1=9.0, pause=0.5)]
    if extra_text:
        tl_lines.append(dict(id='s02_l02', text=extra_text, scene='s02', t0=9.4, t1=11.0, pause=0.4))
    tl = dict(summary=dict(duration_s=12.5),
              lines=tl_lines,
              shots=[dict(id='s01a', scene='s01', t_start=0.1, t_end=6.0)],
              captions=[dict(line='s01_l01', k=0, text='첫 자막', on=0.5, off=2.0),
                        dict(line='s01_l02', k=0, text='A & B', on=2.0, off=4.25),
                        dict(line='s02_l01', k=0, text='둘째 줄', on=4.25, off=6.0)])
    (d / 'timeline.json').write_text(json.dumps(tl), encoding='utf-8')
    if internal:
        (d / 'qc_internal.md').write_text(f'# QC {T_QC}\n\n- 내부 점검\n', encoding='utf-8')
        rep_i = dict(version='v9', internal=dict(video=name, sha256=_sha(vb), duration_s=12.5,
                                                 checks=[dict(what='전체 0.5 s', frames=25, viewed_frames=25,
                                                              static_over_5s=[], flicker=[], edge_band_frames=0)],
                                                 found=[dict(t='3-4 s', scene='s01a', what=T_FOUND, fixed_in=None)]))
        (d / 'qc_report_internal.json').write_text(json.dumps(rep_i, ensure_ascii=False), encoding='utf-8')
        (d / 'rubric_internal.md').write_text(f'# 기준표 {T_RUB}\n\n| 항목 | 점수 |\n|---|---|\n| 대본 | 8 |\n', encoding='utf-8')
        (d / 'README_INTERNAL.md').write_text(f'# 내부판 설명 {T_README}\n', encoding='utf-8')
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
        (d / 'README_ep99.md').write_text(f'# 편 설명 {T_README}\n', encoding='utf-8')
    (d / 'build_scenes.py').write_text('# 넣지 않는 파일\n', encoding='utf-8')
    (d / 'notes').mkdir(exist_ok=True)
    (d / 'notes' / 'deep.md').write_text('하위 폴더 — 넣지 않는다\n', encoding='utf-8')
    return d


def _git_env():
    """시험용 git 환경 — GIT_DIR · GIT_WORK_TREE · GIT_INDEX_FILE 를 넘기지 않는다 (임시 저장소만 건드린다)."""
    return {k: v for k, v in os.environ.items() if k not in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE')}


def _git(*args):
    try:
        return subprocess.run(['git', *map(str, args)], capture_output=True, text=True, env=_git_env(), timeout=60)
    except (OSError, subprocess.SubprocessError):
        return subprocess.CompletedProcess(args, 127, '', '')


def _mk_repo(d):
    """임시 git 저장소 (커밋 하나 · 그 폴더 안에서 따로 init) → (경로, 커밋 sha 40) · git 을 못 쓰면 (경로, None).
    짧은 sha (앞 7 자) 에 글자 a–f 와 숫자가 둘 다 들 때까지 커밋 글을 바꾼다 (후보 꼴 = 공개 검사의 규칙)."""
    d = Path(d)
    d.mkdir(parents=True, exist_ok=True)
    cfg = ['-c', 'user.name=vdt', '-c', 'user.email=vdt@example.invalid', '-c', 'commit.gpgsign=false', '-c', 'core.hooksPath=/dev/null']
    if _git('init', '-q', d).returncode != 0:
        return d, None
    (d / 'a.txt').write_text('vdt\n', encoding='utf-8')
    if _git('-C', d, 'add', 'a.txt').returncode != 0:
        return d, None
    for k in range(64):
        if _git('-C', d, *cfg, 'commit', '-q', '-m', f'vdt {k}', *(['--amend'] if k else [])).returncode != 0:
            return d, None
        sha = _git('-C', d, 'rev-parse', 'HEAD').stdout.strip()
        if re.fullmatch(r'[0-9a-f]{40}', sha) and re.search('[a-f]', sha[:7]) and re.search('[0-9]', sha[:7]):
            return d, sha
    return d, None


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
        public_check=dict(ok=True, rules=[], hits=[], files=len(files), deny_list=None), build_check=_bc_record(3.0))
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


def _bc_record(mp4_s):
    """손 꾸러미의 판 대조 기록 — 꾸러미 도구가 다 재어 통과한 꼴 (공개판 등록의 조건 · K13).  ⚠ 등록은 기록을 본다 (다시 재지 않는다)."""
    return dict(ok=True, method='build_check/2', mp4_s=mp4_s, timeline_end_s=mp4_s, srt_cues=1, timeline_captions=1,
                srt_last_end_s=mp4_s, timeline_last_off_s=mp4_s, scene_lines=1, timeline_lines=1, tol_s=0.5, not_measured=[])


def _set_man(epdir, edit):
    """등록된 편의 episode.json 을 고치고 SHA256SUMS 를 맞춘다 (옛 도구로 등록된 판 흉내 · K13b)."""
    epdir = Path(epdir)
    m = json.loads((epdir / 'episode.json').read_text(encoding='utf-8'))
    edit(m)
    mb = json.dumps(m, ensure_ascii=False).encode('utf-8')
    (epdir / 'episode.json').write_bytes(mb)
    (epdir / 'SHA256SUMS').write_text('\n'.join([f'{_sha(mb)}  episode.json'] + [f"{f['sha256']}  {f['name']}" for f in m['files']])
                                     + '\n', encoding='utf-8')


def _rezip(src, dst, edit):
    """꾸러미 zip 의 episode.json 을 고쳐 다시 묶는다 (SHA256SUMS 맞춤 · 반례 (d) · K13)."""
    with zipfile.ZipFile(src) as zf:
        items = {n: zf.read(n) for n in zf.namelist()}
    m = json.loads(items['episode.json'].decode('utf-8'))
    edit(m)
    mb = json.dumps(m, ensure_ascii=False).encode('utf-8')
    items['episode.json'] = mb
    items['SHA256SUMS'] = ('\n'.join([f'{_sha(mb)}  episode.json'] + [f"{f['sha256']}  {f['name']}" for f in m['files']])
                           + '\n').encode('utf-8')
    with zipfile.ZipFile(dst, 'w') as zf:
        for n in ['episode.json'] + [f['name'] for f in m['files']] + ['SHA256SUMS']:
            zf.writestr(n, items[n])
    return dst


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
    if V is not None:
        _REAL_PROBE.append(V._probe_duration)
        V._probe_duration = lambda p: FAKE_MP4_S         # 합성 영상 = 시간표 끝과 같게 잰 것처럼 (진짜 길 = K11c)
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
        if V is not None and _REAL_PROBE:
            V._probe_duration = _REAL_PROBE[0]
        shutil.rmtree(td_all, ignore_errors=True)


def _run(webapp, V, c, tpl, app_src, lib_src, td):
    cfg = webapp.app.config
    have = V is not None
    BE = getattr(V, 'BundleError', ValueError) if have else ValueError

    def pkg(ep_dir, ep_id, out, **kw):
        kw.setdefault('probe', True)                        # 합성 영상 = FAKE_MP4_S 로 잰다 (main 의 ffprobe 흉내)
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
    repo, csha = _mk_repo(td / 'gitrepo')                   # K1 · K3 — 임시 저장소의 커밋 (제작 대본의 이력 줄 · 참고 문헌 머리에 넣는다)
    ep = make_ep(td / 'src' / 'ep99_test', history_sha=csha)
    bun = td / 'b' / 'ep99.zip'
    bun.parent.mkdir()
    man = {}
    if have:
        try:
            man = pkg(ep, 'ep99_test', bun) or {}
        except Exception as e:                              # noqa: BLE001
            print(f'    package_episode 예외 — {type(e).__name__}: {e}')
    names = zip_names(bun) if bun.is_file() else []
    #  공개판 = 영상 · 썸네일 · 자막 · 시청자 대본 (만든 것) · 공개 장면 (투영) · 시간표만 (Codex 11-25 AVI-02 · 제작 기록 = 뺌 · K3)
    want = {'episode.json', 'SHA256SUMS', 'preview.mp4', 'thumbnail.png', 'ep99.srt', 'script.md', 'scenes.json', 'timeline.json'}
    chk(f'④ 꾸러미 = 납작한 zip · 공개판 역할 파일 + episode.json + SHA256SUMS · 넣지 않는 파일 (build_scenes.py · 하위 폴더 · '
        f'제작 기록) 없음 ({sorted(names)})', set(names) == want)
    zman = {}
    if bun.is_file():
        with zipfile.ZipFile(bun) as z:
            zman = json.loads(z.read('episode.json').decode('utf-8')) if 'episode.json' in z.namelist() else {}
            ztext = b''.join(z.read(n) for n in z.namelist() if not n.endswith(('.mp4', '.png'))).decode('utf-8', 'replace')
    else:
        ztext = ''
    chk('⑤ episode.json — 스키마 avi-episode/1 · id · 제목 · 시리즈 · 편 번호 99 · 공개 · 길이 = timeline 12.5 · 파일 목록 sha256 = 실제',
        zman.get('schema') == 'avi-episode/1' and zman.get('id') == 'ep99_test' and zman.get('title') == T_TITLE
        and zman.get('series') == T_SERIES and zman.get('episode') == 99 and zman.get('visibility') == 'public'
        and zman.get('duration_s') == 12.5
        and {f.get('name'): f.get('sha256') for f in zman.get('files') or []}.get('preview.mp4') == _sha(_video_bytes()))
    exc = {e.get('name'): e for e in zman.get('excluded') or [] if isinstance(e, dict)}
    leak6 = [t for t in PROD_ONLY if t in ztext] + ([csha[:7]] if csha and csha[:7] in ztext else [])
    chk(f'⑥ 공개판 꾸러미 — 제작 기록 (qc.md · qc_report · 기준표 · README) 을 넣지 않고 episode.json excluded 에 이름 · 역할 · 사유 · '
        f'내부 표지 글 · 제작 쪽 글 · 제작 이력의 커밋 식별자가 꾸러미 어디에도 없다 (새는 것 {len(leak6)})',
        set(exc) == {'qc.md', 'qc_report_v2.json', 'rubric_ep99.md', 'README_ep99.md'}
        and [exc[n].get('role') for n in sorted(exc)] == ['readme', 'qc', 'qc_report', 'rubric']
        and all(isinstance(e.get('reason'), str) and e['reason'].strip() for e in exc.values())
        and bool(ztext) and not leak6)
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
    chk('⑰ 참고 문헌 — 대본의 "## 참고 문헌" 절만 (다른 절 글 없음 · 공개판 = 제작 대본의 목록 줄 둘)',
        _esc(T_REF).split(' ')[0] in rf and _esc(T_REF2).split(' ')[0] in rf and T_OTHER not in rf)
    sr = _region(h2, 'script')
    chk('⑱ 대본 토글 (공개판) = 시청자 대본 렌더 — 장면 제목 머리 · 문장 글 · 참고 문헌 · 제작 대본의 다른 절 · 이력 · 읽는 꼴 · 메모 없음',
        '<h2>' + _esc(T_SC1) + '</h2>' in sr and '<h2>' + _esc(T_SC2) + '</h2>' in sr and _esc(T_LINE1) in sr
        and _esc(T_LINE3) in sr and _esc(T_REF).split(' ')[0] in sr
        and not any(t in sr for t in (T_SCRIPT, T_OTHER, T_HIST, T_REFHEAD, T_REFNOTE, T_SAY, T_MEMO)))
    qc = _region(h2, 'qc')
    chk('⑲ QC 토글 (공개판) = "이 편에는 QC 파일이 없습니다" 안내 · QC 글 없음 (QC 렌더는 내부판 ㊳b 에서 본다)',
        '이 편에는 QC 파일이 없습니다' in qc and T_FOUND not in qc and T_QC not in qc and 'vd-qc-match' not in qc)
    chk('⑳ 내부 표지 글 (qc_report internal 칸) 이 공개판 화면 어디에도 없다 (화면이 실제로 그려진 상태에서)',
        r2.status_code == 200 and _esc(T_LINE1) in h2 and T_SECRET not in h2 and T_SECRET not in h)
    chk('㉑ 기준표 토글 (공개판) = "이 편에는 기준표 파일이 없습니다" 안내 (기준표 렌더는 내부판 ㊳b 에서 본다)',
        '이 편에는 기준표 파일이 없습니다' in _region(h2, 'rubric') and T_RUB not in h2 and 'data-vd="readme"' not in h2)
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
        'ep95_link': lambda d: (_set_id(d, 'ep95_link'), (d / 'script.md').unlink(), os.symlink(str(APP), d / 'script.md')),
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
    leak = (c.get('/videos/ep95_link/download/script').get_data(as_text=True) + c.get('/videos/ep95_link/download/qc').get_data(as_text=True)
            + c.get('/videos/ep95_link/media/video').get_data(as_text=True))
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
    qi, sci, rbi = _region(h, 'qc'), _region(h, 'script'), _region(h, 'rubric')
    chk('㊳b 내부판 토글 = 제작 기록 그대로 — QC (qc_report 의 그 편 칸 · 점검 · 발견 + qc 문서 · QC 가 본 영상 sha256 같음) · '
        '기준표 (표) · 편 설명 (README) · 대본 = 제작 대본 (이력 · 다른 절 포함)',
        T_FOUND in qi and T_QC in qi and 'vd-qc-match' in qi and T_RUB in rbi and '<table' in rbi
        and _details(h)[:1] == ['readme'] and T_README in _region(h, 'readme')
        and T_SCRIPT in sci and T_OTHER in sci and T_HIST in sci)
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
    hp = make_ep(td / 'src' / 'homepath', extra_text='작업 폴더 /home/someone/avi_work/x 를 본다', qc_secret=False)
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
    port_ep = make_ep(td / 'src' / 'port', extra_text='주소 example.org:8443 · localhost 에서', qc_secret=False)
    ok_r, why_r = refused(pkg, port_ep, 'ep87_port', td / 'b' / 'port.zip') if have else (False, '')
    chk(f'㊽ 주소 · 포트 · localhost = 공개판 거부 ({why_r[:60]})', ok_r and ('포트' in why_r or 'localhost' in why_r))
    deny = td / 'deny.txt'
    deny.write_text(f'# 시험 내부 숫자\n{T_DENY}\n', encoding='utf-8')
    dep = make_ep(td / 'src' / 'deny', extra_text=f'숫자 {T_DENY} %', qc_secret=False)
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
        bp = make_ep(td / 'src' / 'ban', extra_text='인용: ' + bans[0], qc_secret=False)
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
    #  명령 시험의 합성 영상은 ffprobe 가 못 잰다 → 공개판은 거부 (61b) · 꾸러미 · 등록 기계 일은 검토 후보 (--internal) 로 본다
    rc1, o1 = run(PKG, ep, '--id', 'ep97_cli', '-o', out_zip, '--no-probe', '--internal') if PKG.is_file() else (99, 'no script')
    rc2, o2 = run(REG, out_zip, '--folder', cli_lib) if REG.is_file() else (99, 'no script')
    rc3, o3 = run(REG, out_zip, '--folder', cli_lib) if REG.is_file() else (99, 'no script')
    rc4, o4 = run(REG, out_zip, '--folder', cli_lib, '--replace') if REG.is_file() else (99, 'no script')
    chk(f'61 명령 — 꾸러미 rc 0 · 등록 rc 0 · 같은 꾸러미 다시 rc 1 (이미 있음) · --replace rc 0 · 판 대조 줄 (못 잰 대조 = 미측정) '
        f'({rc1, rc2, rc3, rc4})',
        (rc1, rc2, rc3, rc4) == (0, 0, 1, 0) and (cli_lib / 'ep97_cli' / 'episode.json').is_file() and '이미' in o3
        and '판 대조' in o1 and '미측정' in o1)
    pub_zip = td / 'b' / 'cli_pub.zip'
    rc1p, o1p = run(PKG, ep, '--id', 'ep97_clip', '-o', pub_zip, '--no-probe') if PKG.is_file() else (99, '')
    chk('61b 명령 — 공개판 + --no-probe (MP4 길이를 못 잼) = rc 1 · 사유 = 다 재지 못한 대조 이름 (값 없음) · 꾸러미 없음 (Q4 3 회차 P2-1)',
        rc1p == 1 and 'MP4 길이' in o1p and '다 재지 못했다' in o1p and not re.search(r'\d+\.\d', o1p) and not pub_zip.exists())
    rc5, o5 = run(REG, ep, '--id', 'ep96_dir', '--folder', cli_lib, '--no-probe', '--internal') if REG.is_file() else (99, '')
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
    aj = make_ep(td / 'src' / 'auto_deny', extra_text=f'내부 숫자 {T_DENY} 를 실수로 적었다', qc_secret=False)
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
    aj3 = make_ep(td / 'src' / 'textonly', extra_text=f'값 {T_DENY}', qc_secret=False)
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
    #  공개판 글 = 시청자 대본 (장면 문장 글) — 그 글 속 HTML · 링크 꼴이 글로만 보여야 한다 (11-25 · extra_text)
    xss = make_ep(td / 'src' / 'xss', qc_secret=False,
                  extra_text="<script>alert('VDX1')</script>\n\n[누름](javascript:alert('VDX2'))\n\n"
                             "<img src=x onerror=alert('VDX3')>\n\n<a href=\"data:text/html,VDX4\">d</a>\n\n<!-- VDX5 -->")
    xlib = td / 'lib_xss'
    ok67 = ok67b = False

    def _xss_ok(hx):
        return ("<script>alert('VDX1')" not in hx and re.search(r'<[a-zA-Z][^>]*\son[a-z]+\s*=', hx) is None
                and re.search(r'(?:href|src)\s*=\s*["\']?\s*(?:javascript|data):', hx, re.I) is None
                and '<img src=x' not in hx and '<img src="x"' not in hx and '<!-- VDX5' not in hx and 'VDX1' in hx)
    if have:
        try:
            pkg(xss, 'ep82_xss', td / 'b' / 'xss.zip')
            V.register_bundle(td / 'b' / 'xss.zip', xlib)
            cfg['VIDEO_FOLDER'] = str(xlib)
            ok67 = _xss_ok(c.get('/videos/ep82_xss').get_data(as_text=True))
            #  내부판 = 제작 대본 md 그대로 → 허용 태그 · 속성만 남기는 소독 (sanitize) 이 실제로 도는 자리 (지키는 범위 그대로)
            xi = make_ep(td / 'src' / 'xss_i', internal=True,
                         extra_md="<script>alert('VDX1')</script>\n\n[누름](javascript:alert('VDX2'))\n\n"
                                  "<img src=x onerror=alert('VDX3')>\n\n<a href=\"data:text/html,VDX4\">d</a>\n\n<!-- VDX5 -->")
            pkg(xi, 'ep82_xssi', td / 'b' / 'xssi.zip', internal=True)
            V.register_bundle(td / 'b' / 'xssi.zip', xlib)
            ok67b = _xss_ok(c.get('/videos/ep82_xssi').get_data(as_text=True))
        except Exception as e:                              # noqa: BLE001
            print(f'    xss 예외 — {type(e).__name__}: {e}')
    chk('67 md 속 HTML · javascript: · data: 링크 · on… 속성 · img · 주석 = 무력화 (글은 글로 보인다) — 공개판 시청자 대본 · '
        f'내부판 제작 대본 둘 다 ({ok67} · {ok67b})', ok67 and ok67b)
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

    _run_k(webapp, V, c, td, have, pkg, refused, lib, ep, bun, zman, ib, iman, repo, csha)

    print(f'\ntest_video_page: {_ok}/{_ok + len(_fail)} PASS' + (f'   FAILED: {_fail}' if _fail else ''))
    return 1 if _fail else 0


def _man_for(entries, roles, *, ep_id='ep69_k8', visibility='public'):
    """손 꾸러미용 episode.json — 역할을 이름 끝이 아니라 직접 준다 (K8)."""
    files = [dict(name=n, role=roles[n], size=len(b), sha256=_sha(b)) for n, b in entries]
    return dict(schema='avi-episode/1', id=ep_id, title='손 꾸러미', subtitle='', series='손 시리즈', episode=69,
                visibility=visibility, duration_s=3.0, updated='2031-01-01', files=files,
                public_check=dict(ok=True, rules=[], hits=[], files=len(files), deny_list=None), build_check=_bc_record(3.0))


def _rehash(epdir, name, data, role=None):
    """등록된 편의 파일 하나를 바꾸거나 더하고 episode.json · SHA256SUMS 를 맞춘다 — 옛 규칙으로 등록된 편 흉내
    (해시는 다 맞아 등록부에서 빠지지 않는데, 글이 지금 공개 검사에 걸리거나 공개판에 없어야 할 역할이 있다 · K10)."""
    epdir = Path(epdir)
    (epdir / name).write_bytes(data)
    m = json.loads((epdir / 'episode.json').read_text(encoding='utf-8'))
    ent = next((f for f in m['files'] if f['name'] == name), None)
    if ent is None:
        m['files'].append(dict(name=name, role=role, size=len(data), sha256=_sha(data)))
    else:
        ent.update(size=len(data), sha256=_sha(data))
    mb = json.dumps(m, ensure_ascii=False).encode('utf-8')
    (epdir / 'episode.json').write_bytes(mb)
    (epdir / 'SHA256SUMS').write_text('\n'.join([f'{_sha(mb)}  episode.json'] + [f"{f['sha256']}  {f['name']}" for f in m['files']])
                                     + '\n', encoding='utf-8')


def _run_k(webapp, V, c, td, have, pkg, refused, lib, ep, bun, zman, ib, iman, repo, csha):
    """K. 공개판 다시 짜기 (Codex 11-25 AVI-02 · 1저자 11-25 Q1 · Q2 (가) · 덧붙임)."""
    cfg = webapp.app.config
    CR, CF, MK = 'git 커밋 식별자', 'git 커밋 식별자 검사 못 함', '제작 표지'

    def rules_of(pc_):
        return [h.get('rule') for h in (pc_ or {}).get('hits') or []]

    def pc(texts, **kw):
        if not have:
            return dict(ok=None, hits=[])
        try:
            return V.public_check(texts, **kw)
        except Exception as e:                              # noqa: BLE001
            print(f'    public_check 예외 — {type(e).__name__}: {e}')
            return dict(ok=None, hits=[])

    # ═══ K1. git 커밋 식별자 — 리포에서 실제 커밋으로 풀리는 7–40 hex (글자 a–f + 숫자) · 값은 적지 않는다 · git 을 못 쓰면 걸림 ═══
    nogit = td / 'nogit_dir'
    nogit.mkdir(exist_ok=True)
    objs = _git('-C', repo, 'cat-file', '--batch-all-objects', '--batch-check=%(objectname)').stdout.split() if csha else []
    fake = next((t for t in ('deadbee1', 'c0ffee12', 'abc12345', 'f00d1234', '1a2b3c4d') if not any(o.startswith(t) for o in objs)),
                'deadbee1')
    ok_k1 = False
    if have and csha:
        res = {n: pc([('a.md', f'판 {csha[:n]} 에서 고쳤다')], repo_root=repo) for n in (7, 8, 9, 10, 11, 12, 40)}
        glued = pc([('b.md', f'꼬리표 commit_{csha[:9]}')], repo_root=repo)
        ok_k1 = (all(r.get('ok') is False and any(h.get('rule') == CR and h.get('file') == 'a.md' and h.get('line') == 1
                                                  for h in r.get('hits') or []) for r in res.values())
                 and CR in rules_of(glued)
                 and all(csha[:7] not in json.dumps(r, ensure_ascii=False) for r in list(res.values()) + [glued])
                 and CR in (res[7].get('rules') or []))
    chk(f'K1 커밋 식별자 — 임시 저장소 커밋의 짧은 sha (7–12 자 · 40 자 · 밑줄에 붙은 꼴) 가 든 글 = 걸림 (규칙 {CR} · 파일 · 줄만 · 값 없음)', ok_k1)
    ok_k1b = False
    if have and csha:
        neg = pc([('a.md', f'아무 hex {fake} 끝'), ('b.md', f'sha256 {hashlib.sha256(b"vdt").hexdigest()}'),
                  ('c.md', '날짜 20261125 · 숫자만 12345678 · 9876543210'), ('d.md', f'글자에 붙은 x{csha[:8]} 낱말'),
                  ('e.md', '짧은 abc123 · 대문자 아님 GHIJKLM')], repo_root=repo)
        ok_k1b = neg.get('ok') is True and not neg.get('hits')
    chk('K1b 커밋이 아닌 무작위 8 hex · 64 hex sha256 · 숫자만 · 글자에 붙은 hex · 6 자 이하 = 안 걸림', ok_k1b)
    ok_k1c = False
    if have:
        f1 = pc([('a.md', f'판 {fake}')], repo_root=nogit)
        old_exe = getattr(V, 'GIT_EXE', 'git')
        try:
            V.GIT_EXE = str(td / 'no-such-git-binary')
            f2 = pc([('a.md', f'판 {fake}')], repo_root=repo)
        finally:
            V.GIT_EXE = old_exe
        f3 = pc([('a.md', '후보 낱말이 없는 글 VDT 12345678')], repo_root=nogit)
        ok_k1c = (f1.get('ok') is False and CF in rules_of(f1) and f2.get('ok') is False and CF in rules_of(f2)
                  and f3.get('ok') is True)
    chk(f'K1c git 을 못 쓰면 (저장소 아님 · git 없음) 후보 낱말이 있는 글 = 걸림 ({CF} · fail-closed) · 후보가 없으면 git 을 부르지 않는다', ok_k1c)
    ok_k1d = False
    if have and csha:
        try:
            gl = make_ep(td / 'src' / 'k_gitleak', extra_text=f'판 {csha[:9]} 에서 고쳤다', qc_secret=False)
            r_, w_ = refused(pkg, gl, 'ep70_gitleak', td / 'b' / 'k_gitleak.zip', repo_root=repo)
            gx = make_ep(td / 'src' / 'k_gitx', extra_text=f'문장 속 {fake} 낱말', qc_secret=False)
            r2_, w2_ = refused(pkg, gx, 'ep71_gitx', td / 'b' / 'k_gitx_nogit.zip', repo_root=nogit)
            m3 = pkg(gx, 'ep71_gitx', td / 'b' / 'k_gitx_ok.zip', repo_root=repo) or {}
            m4 = pkg(gx, 'ep71_gitxi', td / 'b' / 'k_gitx_int.zip', internal=True, repo_root=nogit) or {}
            ok_k1d = (r_ and CR in w_ and csha[:9] not in w_ and 'script.md' in w_ and not (td / 'b' / 'k_gitleak.zip').exists()
                      and r2_ and '검사 못 함' in w2_ and not (td / 'b' / 'k_gitx_nogit.zip').exists()
                      and (m3.get('public_check') or {}).get('ok') is True
                      and m4.get('visibility') == 'internal' and CF in rules_of(m4.get('public_check')))
        except Exception as e:                              # noqa: BLE001
            print(f'    K1d 예외 — {type(e).__name__}: {e}')
    chk('K1d 꾸러미 — 공개판 글 (시청자 대본) 에 커밋 식별자 = 거부 (사유에 값 없음) · git 을 못 쓰면 공개판 거부 · 내부판은 기록만', ok_k1d)

    # ═══ K2. 제작 표지 (1저자 · Codex · Claude · 조수 · internal/ · 목소리 ID · voice-auto · DECISIONS) ═══
    pos = {'1저자': '1저자 11-25 지시대로 고쳤다', 'Codex': 'Codex 반박 리뷰를 받았다', 'Claude': 'Claude 가 정리했다',
           'claude 소문자': 'claude.ai 에서 본다', '조수': '대본 조수가 고쳤다', '조수 (줄머리)': '조수가 정한 것',
           'internal/': '자료는 ep01/internal/ 에 둔다', 'tc_<hex 20+>': f'목소리 tc_{"a1" * 11}',
           'voice-auto': 'voice-auto 를 돌렸다', 'voice_auto': 'avi_voice_auto.py 의 보고', 'DECISIONS': 'DECISIONS.md 에 적었다'}
    miss = [k for k, s in pos.items() if MK not in rules_of(pc([('x.md', s)]))]
    neg2 = ['전고체 배터리의 양극은, 두 가지 가루를 섞어서 만듭니다.', '제1저자 외 · 가짜 학술지 1 (2031)', '제조수율 · 구조수정 · 보조수단',
            'design decisions matter', 'internal resistance 가 크다', 'tc_12ab 는 짧다', '저자들은, 부착이 중요한 역할을 한다고 제안했습니다.']
    fp = [s for s in neg2 if pc([('x.md', s)]).get('hits')]
    r2pc = pc([('x.md', pos['1저자'])])
    chk(f'K2 제작 표지 = 걸림 (못 잡음 {miss}) · 보통 내레이션 · 제1저자 · 제조수율 · 소문자 decisions · internal resistance · 짧은 tc_ = 안 걸림 '
        f'(거짓 경보 {len(fp)}) · 규칙 목록에 {MK} · 목록 상수 (PRODUCTION_MARKS) 마다 걸리는 보기가 있다',
        have and not miss and not fp and MK in (r2pc.get('rules') or []) and set(getattr(V, 'PRODUCTION_MARKS', ('?',))) <= set(pos))

    # ═══ K3. 공개판 꾸러미 역할 — 영상 · 썸네일 · 자막 · 시청자 대본 · 공개 장면 · 시간표만 · excluded · derived (from_sha256) ═══
    der = {d.get('name'): d for d in zman.get('derived') or [] if isinstance(d, dict)}
    s_src, sc_src = (ep / 'script.md').read_bytes(), (ep / 'scenes.json').read_bytes()
    dsc, dsn = der.get('script.md') or {}, der.get('scenes.json') or {}
    ok_k3 = (set(der) == {'script.md', 'scenes.json'} and dsc.get('role') == 'script' and dsc.get('from') == 'scenes.json'
             and dsc.get('from_sha256') == _sha(sc_src) and dsc.get('refs_from') == 'script.md'
             and dsc.get('refs_from_sha256') == _sha(s_src) and dsn.get('role') == 'scenes' and dsn.get('from') == 'scenes.json'
             and dsn.get('from_sha256') == _sha(sc_src)
             and {'voice_model', 'thumb', 'lines.say', 'lines.memo', 'shots.elements'} <= set(dsn.get('dropped_keys') or []))
    chk('K3 episode.json derived — 시청자 대본 (← scenes.json · 참고 문헌 ← 제작 script.md · 원본 sha256 둘) · 공개 장면 (← scenes.json · '
        '뺀 칸 목록)', ok_k3)
    ok_k3b = False
    if have and csha:
        try:
            m5 = pkg(ep, 'ep68_hist', td / 'b' / 'k_hist.zip', repo_root=repo) or {}
            m6 = pkg(ep, 'ep68_histi', td / 'b' / 'k_hist_int.zip', internal=True, repo_root=repo) or {}
            h6 = [h for h in (m6.get('public_check') or {}).get('hits') or [] if h.get('rule') == CR]
            ok_k3b = ((m5.get('public_check') or {}).get('ok') is True and bool(h6)
                      and all(h.get('file') == 'script.md' for h in h6) and len({h.get('line') for h in h6}) == 2)
        except Exception as e:                              # noqa: BLE001
            print(f'    K3b 예외 — {type(e).__name__}: {e}')
    chk('K3b 제작 대본의 이력 줄 · 참고 문헌 머리에 실제 커밋 식별자가 있어도 공개판은 통과 (그 글은 공개판에 안 들어간다) · '
        '같은 편의 내부판 = 그 두 줄을 기록', ok_k3b)

    # ═══ K4. 시청자 대본 (Q2 (가)) — 장면 제목 = 머리 · 문장 text 순서대로 · 공개 참고 문헌 = 목록 줄만 ═══
    vs = ''
    if bun.is_file():
        with zipfile.ZipFile(bun) as z:
            vs = z.read('script.md').decode('utf-8') if 'script.md' in z.namelist() else ''
    L = vs.splitlines()

    def at(s):
        return next((i for i, x in enumerate(L) if s in x), -1)
    i_sc1 = L.index('## ' + T_SC1) if '## ' + T_SC1 in L else -1
    i_sc2 = L.index('## ' + T_SC2) if '## ' + T_SC2 in L else -1
    i_ref = L.index('## 참고 문헌') if '## 참고 문헌' in L else -1
    refs = L[i_ref + 1:] if i_ref >= 0 else []
    ok_k4 = (bool(L) and L[0] == '# ' + T_TITLE and T_SUB in vs and T_SERIES in vs
             and 0 < i_sc1 < at(T_LINE1) < at(T_LINE2) < i_sc2 < at(T_LINE3) < i_ref
             and [x for x in refs if x.strip()] == [f'1. {T_REF} · *가짜 학술지* 1, 2 (2031)', f'2. {T_REF2} · *가짜 학술지* 3, 4 (2032)']
             and not any(t in vs for t in PROD_ONLY) and not (csha and csha[:7] in vs)
             and not any(m in vs for m in ('1저자', 'voice-auto', 'DECISIONS', 'internal/'))
             and pc([('script.md', vs)]).get('ok') is True)
    chk('K4 시청자 대본 — 제목 · 부제 · 시리즈 머리 · 장면 제목 = "## " 머리 · 그 장면 문장 글 순서대로 · "## 참고 문헌" (머리 괄호 설명 · '
        '커밋 식별자 없음) 아래 목록 줄 둘만 (들여쓴 줄 · 목록 밖 줄 없음) · 제작 이력 · 읽는 꼴 · 메모 없음 · 새 공개 검사 통과', ok_k4)
    ok_k4b = False
    gv = getattr(V, 'viewer_script', None) if have else None
    if gv:
        try:
            t_ = gv(dict(title='<b>T</b>', scenes=[dict(id='s1', title='# 머리 [링크](x)', lines=[
                dict(id='a', text='1. 목록 같은 문장'), dict(id='b', text='- 줄머리 표지 · *별* · <i>기울임</i> & `코드`'),
                dict(id='c', say='읽는 꼴만 있고 글은 없다'), dict(id='d', text='여러 줄\n> 인용 꼴\n~~~ 울타리 꼴')])]), None)
            h_ = V.md_html(t_)
            ok_k4b = ('<b>T</b>' not in h_ and '&lt;b&gt;T&lt;/b&gt;' in h_ and '<ol' not in h_ and '<ul' not in h_
                      and '<em>' not in h_ and '<code>' not in h_ and '<pre' not in h_ and '<a ' not in h_ and '<i>' not in h_
                      and '<blockquote' not in h_ and '읽는 꼴만' not in t_ and h_.count('<h2>') == 1 and '## 참고 문헌' not in t_
                      and '목록 같은 문장' in h_ and '울타리 꼴' in h_)
        except Exception as e:                              # noqa: BLE001
            print(f'    viewer_script 예외 — {type(e).__name__}: {e}')
    chk('K4b 시청자 대본의 글은 글로 보인다 — 태그 · 목록 · 강조 · 코드 · 울타리 · 링크 · 인용 꼴이 md 로 바뀌지 않는다 · 글 (text) 없는 문장 = '
        '넣지 않는다 · 참고 문헌이 없으면 그 절도 없다', ok_k4b)

    # ═══ K5. 장면 공개 투영 — 머리 일곱 · 장면 = id · title · lines[id · text · captions] · shots[id · from] · 챕터 · 장면 목록 그대로 ═══
    pj = {}
    if bun.is_file():
        with zipfile.ZipFile(bun) as z:
            pj = json.loads(z.read('scenes.json').decode('utf-8')) if 'scenes.json' in z.namelist() else {}
    pjt = json.dumps(pj, ensure_ascii=False)
    sc_ = pj.get('scenes') if isinstance(pj.get('scenes'), list) else []
    ok_k5 = (set(pj) == {'episode', 'title', 'subtitle', 'series', 'fps', 'width', 'height', 'scenes'} and len(sc_) == 2
             and all(set(s) == {'id', 'title', 'lines', 'shots'} for s in sc_)
             and all(set(x) <= {'id', 'text', 'captions'} for s in sc_ for x in s['lines'])
             and sc_[0]['lines'][0] == dict(id='s01_l01', text=T_LINE1, captions=[T_CAP, '자막 둘'])
             and all(set(x) <= {'id', 'from'} for s in sc_ for x in s['shots']) and sc_[0]['shots'] == [{'id': 's01a', 'from': 's01_l01'}]
             and not any(t in pjt for t in (T_SAY, T_MEMO, T_ELEM, '차분', 'voice_model', 'thumb', 'lead_in', 'pause_after'))
             and zman.get('chapter_lead_s') == 0.7)
    chk('K5 공개 장면 = 투영 — 머리 (episode · title · subtitle · series · fps · width · height) · 장면 · 문장 (id · text · captions) · '
        '샷 (id · from) 만 · 읽는 꼴 · 메모 · 감정 · 강조 · 빠르기 · 쉼 · 목소리 모형 · 화면 개체 · 썸네일 없음 · 챕터 앞당김 = episode.json', ok_k5)
    ok_k5b = False
    if have:
        try:
            pkg(ep, 'ep78_full', td / 'b' / 'k_full.zip', internal=True)
            V.register_bundle(td / 'b' / 'k_full.zip', td / 'lib_full')
            cfg['VIDEO_FOLDER'] = str(td / 'lib_full')
            hf_ = c.get('/videos/ep78_full').get_data(as_text=True)
            cfg['VIDEO_FOLDER'] = str(lib)
            hp_ = c.get('/videos/ep99_test').get_data(as_text=True)
            ok_k5b = (_region(hf_, 'chapters') == _region(hp_, 'chapters') and 'data-t="5.5"' in _region(hp_, 'chapters')
                      and _region(hf_, 'scenes') == _region(hp_, 'scenes') and _region(hp_, 'scenes').count('vd-scene-row') == 2)
        except Exception as e:                              # noqa: BLE001
            print(f'    K5b 예외 — {type(e).__name__}: {e}')
        finally:
            cfg['VIDEO_FOLDER'] = str(lib)
    chk('K5b 웹앱 챕터 · 장면 목록 — 공개 투영 (공개판) 과 제작 장면 파일 (같은 편의 내부판) 이 화면에서 같다', ok_k5b)

    # ═══ K6. 내부판 = 지금과 같음 — 모든 역할 · 제작 대본 · 장면 파일 그대로 · 검사는 기록만 ═══
    iep = Path(ib).parent.parent / 'src' / 'internal'
    ok_k6 = False
    if Path(ib).is_file() and iep.is_dir():
        with zipfile.ZipFile(ib) as z:
            nm = set(z.namelist())
            same = all(z.read(n) == (iep / n).read_bytes() for n in nm - {'episode.json', 'SHA256SUMS'})
        want_i = {'episode.json', 'SHA256SUMS', 'clip_INTERNAL_x.mp4', 'clip_INTERNAL_x.srt', 'script.md', 'scenes.json', 'timeline.json',
                  'qc_internal.md', 'qc_report_internal.json', 'rubric_internal.md', 'README_INTERNAL.md'}
        ipc = iman.get('public_check') or {}
        ok_k6 = (nm == want_i and same and iman.get('visibility') == 'internal' and not iman.get('excluded')
                 and not iman.get('derived') and ipc.get('ok') is False
                 and any(h.get('rule') == MK and h.get('file') == 'script.md' for h in ipc.get('hits') or []))
    chk('K6 내부판 꾸러미 = 지금과 같음 — 모든 역할 (QC · 점검 기록 · 기준표 · README) · 제작 대본 · 장면 파일 · 점검 기록 바이트 그대로 · '
        'excluded · derived 없음 · 공개 검사 (제작 표지) 는 기록만', ok_k6)

    # ═══ K7. 내부 숫자 목록 = 수 경계로만 맞춤 ═══
    ok_k7 = False
    if have:
        r7 = pc([('a.md', '값 10.5 · 0.55 · 1.0.5 · 20.50'), ('b.md', '크기 0.5 µm'), ('c.md', '(0.5)'), ('d.md', '끝 0.5.'),
                 ('e.md', '-0.5 와 0.5,0.6')], deny=(['0.5'], 'x' * 64))
        hit_f = sorted({h.get('file') for h in r7.get('hits') or [] if h.get('rule') == '내부 숫자 목록'})
        ok_k7 = hit_f == ['b.md', 'c.md', 'd.md', 'e.md'] and '0.5' not in json.dumps(r7.get('hits'), ensure_ascii=False)
    chk('K7 내부 숫자 목록 = 수 경계 — 목록 "0.5" 가 10.5 · 0.55 · 1.0.5 안에서 안 걸리고 0.5 µm · (0.5) · 문장 끝 · 부호 · 쉼표 목록에서는 걸림', ok_k7)
    ok_k7b = False
    if have:
        dl7 = td / 'deny_k7.txt'
        dl7.write_text('0.137\n', encoding='utf-8')
        e1 = make_ep(td / 'src' / 'k7_ok', extra_text='값 10.137 · 0.1375 · 0.1370', qc_secret=False)
        e2 = make_ep(td / 'src' / 'k7_hit', extra_text='전도도 0.137 mS/cm', qc_secret=False)
        try:
            m7 = pkg(e1, 'ep67_k7', td / 'b' / 'k7_ok.zip', deny_list=dl7) or {}
        except Exception as e:                              # noqa: BLE001
            m7 = {}
            print(f'    K7b 예외 — {type(e).__name__}: {e}')
        r7b, w7b = refused(pkg, e2, 'ep66_k7', td / 'b' / 'k7_hit.zip', deny_list=dl7)
        ok_k7b = (m7.get('public_check') or {}).get('ok') is True and r7b and '내부 숫자 목록' in w7b and '0.137' not in w7b
    chk('K7b 꾸러미에서도 — 목록 0.137 이 10.137 · 0.1375 · 0.1370 에는 안 걸려 통과 · "0.137 mS/cm" 는 거부 (값 없음)', ok_k7b)

    # ═══ K8. 등록도 같은 기준 — 공개판 꾸러미에 제작 기록 역할 · 투영이 아닌 장면 파일 = 거부 (내부판은 그대로) ═══
    ok_k8 = False
    if have:
        vb5 = _video_bytes(5000)
        e_qc = [('a.mp4', vb5), ('script.md', '# 손\n'.encode('utf-8')), ('qc.md', '# QC\n'.encode('utf-8'))]
        p_qc = craft_zip(td / 'b' / 'k8_qc.zip', e_qc, manifest=_man_for(e_qc, {'a.mp4': 'video', 'script.md': 'script', 'qc.md': 'qc'}))
        full_sc = json.dumps(dict(title='t', voice_model=dict(lead_in=0.7), scenes=[dict(id='s1', title='a', lines=[dict(id='l', say='x')])]),
                             ensure_ascii=False).encode('utf-8')
        e_sc = [('a.mp4', vb5), ('scenes.json', full_sc)]
        p_sc = craft_zip(td / 'b' / 'k8_sc.zip', e_sc, manifest=_man_for(e_sc, {'a.mp4': 'video', 'scenes.json': 'scenes'}))
        p_int = craft_zip(td / 'b' / 'k8_int.zip', e_qc, manifest=_man_for(e_qc, {'a.mp4': 'video', 'script.md': 'script', 'qc.md': 'qc'},
                                                                           ep_id='ep69_k8i', visibility='internal'))
        k8lib = td / 'lib_k8'
        r_a, w_a = refused(V.register_bundle, p_qc, k8lib)
        r_b, w_b = refused(V.register_bundle, p_sc, k8lib)
        try:
            V.register_bundle(p_int, k8lib)
            int_ok = (k8lib / 'ep69_k8i' / 'qc.md').is_file()
        except Exception as e:                              # noqa: BLE001
            int_ok = False
            print(f'    K8 내부판 예외 — {type(e).__name__}: {e}')
        ok_k8 = (r_a and '제작 기록' in w_a and r_b and '투영' in w_b and not (k8lib / 'ep69_k8').exists() and int_ok)
    chk('K8 등록 — 공개판 꾸러미에 제작 기록 역할 (qc) = 거부 · 공개판 장면 파일이 투영 꼴이 아니면 거부 · 내부판은 그대로 등록', ok_k8)

    # ═══ K9. docs/avi/tools — 옮긴 도구 (avi_audio v3.1 · avi_prosody · avi_xtts · avi_melo) ═══
    import ast
    tools = ROOT / 'docs' / 'avi' / 'tools'
    local = {p.stem for p in tools.glob('*.py')}
    missing, top_heavy, homes = [], [], []
    for p in sorted(tools.glob('*.py')):
        src = p.read_text(encoding='utf-8')
        tree = ast.parse(src)
        for node in ast.walk(tree):
            mods = ([a.name.split('.')[0] for a in node.names] if isinstance(node, ast.Import)
                    else [node.module.split('.')[0]] if isinstance(node, ast.ImportFrom) and node.module and not node.level else [])
            for m in mods:
                if (m.startswith('avi_') or m in ('korean_text', 'audio_measure')) and m not in local:
                    missing.append(f'{p.name}→{m}')
        if p.stem in ('avi_xtts', 'avi_melo'):
            for node in tree.body:
                mods = ([a.name.split('.')[0] for a in node.names] if isinstance(node, ast.Import)
                        else [node.module.split('.')[0]] if isinstance(node, ast.ImportFrom) and node.module else [])
                top_heavy += [f'{p.name}:{m}' for m in mods if m in ('torch', 'TTS', 'melo', 'transformers')]
        if p.stem in ('avi_audio', 'avi_prosody', 'avi_xtts', 'avi_melo') and re.search(r'/home/|/root/|[A-Za-z]:\\\\Users', src):
            homes.append(p.name)
    stub_n = None
    if (tools / 'avi_melo.py').is_file():
        for node in ast.parse((tools / 'avi_melo.py').read_text(encoding='utf-8')).body:
            if isinstance(node, ast.Assign) and any(getattr(t, 'id', '') == 'STUBBED' for t in node.targets):
                stub_n = len(getattr(node.value, 'elts', []))
    xt = (tools / 'avi_xtts.py').read_text(encoding='utf-8') if (tools / 'avi_xtts.py').is_file() else ''
    au = (tools / 'avi_audio.py').read_text(encoding='utf-8') if (tools / 'avi_audio.py').is_file() else ''
    ok_k9 = ({'avi_audio', 'avi_prosody', 'avi_xtts', 'avi_melo'} <= local and not missing and not top_heavy and not homes
             and stub_n == 9 and 'CPML' in xt and '내부판' in xt and 'soften_breaths' in au and 'line_gain' in au)
    chk(f'K9 docs/avi/tools — avi_audio (v3.1 · 숨 · 문장 음량) · avi_prosody · avi_xtts (CPML · 내부판 전용) · avi_melo (언어 앞단 대역 9) 가 있다 · '
        f'같은 폴더 모듈이 다 있다 (빠짐 {missing}) · 음성 모델 도구는 모듈 첫머리에서 torch 를 부르지 않는다 ({top_heavy}) · '
        f'홈 경로 없음 ({homes})', ok_k9)

    # ═══ K10. 걸린 공개판 = 공개 보류 (Q4 P1-2) — 다른 컴퓨터 = 없는 편과 같다 (목록 · 화면 · 재생 · 받기 · 자막) · 이 컴퓨터 = 빨간 배지 ═══
    hl = td / 'lib_held'
    far = {'REMOTE_ADDR': '10.9.8.7'}
    ok_k10 = ok_k10b = ok_k10c = False
    if have:
        try:
            for nm_, id_, ttl in (('k10_ok', 'ep64_ok', None), ('k10_held', 'ep65_held', 'VDX-HELD-TITLE'),
                                  ('k10_role', 'ep63_role', 'VDX-ROLE-TITLE')):
                d_ = make_ep(td / 'src' / nm_, qc_secret=False)
                if ttl:
                    sj = json.loads((d_ / 'scenes.json').read_text(encoding='utf-8'))
                    sj['title'] = ttl
                    (d_ / 'scenes.json').write_text(json.dumps(sj, ensure_ascii=False), encoding='utf-8')
                pkg(d_, id_, td / 'b' / f'{id_}.zip')
                V.register_bundle(td / 'b' / f'{id_}.zip', hl)
            sp_ = hl / 'ep65_held' / 'script.md'
            _rehash(hl / 'ep65_held', 'script.md', sp_.read_bytes() + '\n1저자 11-25 메모 VDX-HELD-MARK\n'.encode('utf-8'))
            _rehash(hl / 'ep63_role', 'qc.md', '# QC 옛 꾸러미\n'.encode('utf-8'), role='qc')
            cfg['VIDEO_FOLDER'] = str(hl)
            hfar = c.get('/videos', environ_base=far).get_data(as_text=True)
            hfar2 = c.get('/videos/ep64_ok', environ_base=far).get_data(as_text=True)
            none_ = c.get('/videos/nope_ep', environ_base=far)
            same404 = []
            for e_ in ('ep65_held', 'ep63_role'):
                for suf in ('', '/media/video', '/media/thumbnail', '/download/video', '/download/subtitles', '/download/script',
                            '/subtitles.vtt'):
                    a_ = c.get(f'/videos/{e_}{suf}', environ_base=far)
                    b_ = c.get(f'/videos/nope_ep{suf}', environ_base=far)
                    same404.append(a_.status_code == 404 and a_.get_data() == b_.get_data())
            ok_k10 = (all(same404) and none_.status_code == 404
                      and all(t not in x for x in (hfar, hfar2) for t in ('ep65_held', 'ep63_role', 'VDX-HELD-TITLE', 'VDX-ROLE-TITLE',
                                                                           'VDX-HELD-MARK', 'public-held'))
                      and '<source src="/videos/ep64_ok/media/video"' in hfar and 'data-badge="public"' in hfar2)
            hh = c.get('/videos/ep65_held')
            hh_t = hh.get_data(as_text=True)
            why_h = (re.search(r'<ul class="vd-held">(.*?)</ul>', hh_t, re.S) or [None, ''])[1]
            ok_k10b = (hh.status_code == 200 and 'data-badge="public-held"' in hh_t and '공개 보류 · 걸림' in hh_t
                       and 'data-badge="public"' not in hh_t and '이 컴퓨터에서만 보임' in hh_t
                       and '제작 표지' in why_h and 'script.md' in why_h and 'VDX-HELD-MARK' not in why_h
                       and c.get('/videos/ep65_held/media/video').status_code == 200)
            hr = c.get('/videos/ep63_role').get_data(as_text=True)
            why_r = (re.search(r'<ul class="vd-held">(.*?)</ul>', hr, re.S) or [None, ''])[1]
            hok = c.get('/videos/ep64_ok').get_data(as_text=True)
            items_ = (re.search(r'<ol class="vd-items">(.*?)</ol>', hok, re.S) or [None, ''])[1]
            held_item = (re.search(r'href="/videos/ep65_held".*?</a>', items_, re.S) or [''])[0]
            ok_k10c = ('data-badge="public-held"' in hr and '넣지 않는 역할' in why_r and 'qc' in why_r
                       and 'data-badge="public"' in hok and 'vd-held-mini' in held_item and '보류' in held_item)
        except Exception as e:                              # noqa: BLE001
            print(f'    K10 예외 — {type(e).__name__}: {e}')
        finally:
            cfg['VIDEO_FOLDER'] = str(lib)
    chk('K10 걸린 공개판 (지금 공개 검사에 걸림 · 공개판에 없어야 할 역할) = 다른 컴퓨터에는 없는 편 — 목록 · 첫 편 · 재생목록 · 화면 · 재생 · '
        '받기 · 자막 = 등록 안 된 편과 같은 404 (fail-closed)', ok_k10)
    chk('K10b 이 컴퓨터 = 빨간 "공개 보류 · 걸림" 배지 + "이 컴퓨터에서만 보임" · 까닭 = 규칙 · 파일 이름만 (값 없음) · 재생은 된다 (1저자가 고친다)', ok_k10b)
    chk('K10c 공개판에 없어야 할 역할 (qc) 이 든 옛 공개판 = 같은 보류 · 까닭 = 그 역할 · 이 컴퓨터의 재생목록에 "보류" 작은 배지', ok_k10c)

    # ═══ K10d–f. 공개 보류의 가드 셋 (Q4 3 회차 M5 · M6 · M6b) ═══
    gl_ = td / 'lib_guard'
    ok_k10d = ok_k10e = ok_k10f = False
    if have:
        old_clock = V.__dict__.get('_clock')
        old_pc = V.public_check
        try:
            for nm_, id_ in (('k10d', 'ep52_proj'), ('k10e', 'ep51_key'), ('k10f', 'ep50_ttl')):
                d_ = make_ep(td / 'src' / nm_, qc_secret=False)
                pkg(d_, id_, td / 'b' / f'{id_}.zip')
                V.register_bundle(td / 'b' / f'{id_}.zip', gl_)
            cfg['VIDEO_FOLDER'] = str(gl_)
            #  M5 — 장면 파일만 공개 투영 꼴이 아니다 (제작 칸이 든 원본으로 바꿈 · 공개 검사 · 역할 · 판 대조 기록은 그대로 통과)
            _rehash(gl_ / 'ep52_proj', 'scenes.json', (td / 'src' / 'k10d' / 'scenes.json').read_bytes())
            ep_d = V.load_episode(gl_ / 'ep52_proj')[0]
            why_d = V.public_problems(ep_d)[0] if ep_d else ['(읽지 못함)']
            hd_ = c.get('/videos/ep52_proj').get_data(as_text=True)
            ok_k10d = (len(why_d) == 1 and '투영' in why_d[0] and 'data-badge="public-held"' in hd_
                       and c.get('/videos/ep52_proj', environ_base=far).status_code == 404
                       and c.get('/videos/ep52_proj/media/video', environ_base=far).status_code == 404)
            #  M6 — 캐시 열쇠 = (폴더 · SHA256SUMS sha) — 시계를 멈춘 채 (TTL 안) 같은 폴더를 나쁜 판으로 바꿔 넣으면 바로 보류
            V._clock = lambda: 5000.0
            V._HELD_CACHE.clear()
            s1_ = c.get('/videos/ep51_key/media/video', environ_base=far).status_code          # 통과 · 캐시를 채운다
            sp_ = gl_ / 'ep51_key' / 'script.md'
            _rehash(gl_ / 'ep51_key', 'script.md', sp_.read_bytes() + '\n1저자 메모 VDX-KEY-MARK\n'.encode('utf-8'))
            s2_ = c.get('/videos/ep51_key/media/video', environ_base=far).status_code
            ok_k10e = (s1_, s2_) == (200, 404)
            #  M6b — TTL: 파일 · SHA256SUMS 는 그대로 · 규칙만 바뀜 (철회값 · 커밋 목록 흉내) → TTL 안 = 그 판단 · TTL 뒤 = 새로 재어 보류
            t_ = [7000.0]
            V._clock = lambda: t_[0]
            V._HELD_CACHE.clear()
            f1_ = c.get('/videos/ep50_ttl', environ_base=far).status_code

            def _pc_hit(texts, deny=None, repo_root=None):
                r_ = old_pc(texts, deny=deny, repo_root=repo_root)
                return dict(r_, ok=False, hits=list(r_.get('hits') or []) + [dict(file='script.md', line=1, rule='시험 규칙')])
            V.public_check = _pc_hit
            t_[0] = 7000.0 + 29                             # 등록 30 s (스킬 §13-3) 안 = 그 판단 그대로
            f2_ = c.get('/videos/ep50_ttl', environ_base=far).status_code
            t_[0] = 7000.0 + 31                             # 30 s 뒤 = 새로 잰다 (시험은 모듈 값이 아니라 정한 30 s 를 본다)
            f3_ = c.get('/videos/ep50_ttl', environ_base=far).status_code
            ok_k10f = (f1_, f2_, f3_) == (200, 200, 404)
        except Exception as e:                              # noqa: BLE001
            print(f'    K10d–f 예외 — {type(e).__name__}: {e}')
        finally:
            V.public_check = old_pc
            if old_clock is None:
                V.__dict__.pop('_clock', None)
            else:
                V._clock = old_clock
            V._HELD_CACHE.clear()
            cfg['VIDEO_FOLDER'] = str(lib)
    chk('K10d 장면 파일만 공개 투영 꼴이 아닌 공개판 = 보류 (까닭 하나 = 투영 · 다른 컴퓨터 404 · 이 컴퓨터 빨간 배지 · M5)', ok_k10d)
    chk('K10e 보류 캐시 열쇠 = (편 폴더 · SHA256SUMS sha) — TTL 안이라도 바꿔 넣은 나쁜 판은 바로 보류 (M6)', ok_k10e)
    chk('K10f 보류 캐시 TTL 30 s (시계 주입) — 규칙만 바뀌면 29 s = 그 판단 · 31 s = 새로 재어 보류 (M6b)', ok_k10f)

    # ═══ K11. 영상 ↔ 시간표 ↔ 자막 판 대조 (Q4 P2-6) — MP4 길이 · 자막 수 · 자막 마지막 줄 (허용 0.5 s) · 다르면 꾸러미 거부 ═══
    ok_k11 = ok_k11b = ok_k11c = ok_k11d = False
    if have:
        old_probe = V._probe_duration
        try:
            e11 = make_ep(td / 'src' / 'k11_ok', qc_secret=False)
            V._probe_duration = lambda p_: FAKE_MP4_S
            m11 = pkg(e11, 'ep62_bc', td / 'b' / 'k11_ok.zip', probe=True) or {}
            bc = m11.get('build_check') or {}
            V._probe_duration = lambda p_: 30.0
            r_len, w_len = refused(pkg, e11, 'ep62_bc', td / 'b' / 'k11_len.zip', probe=True)
            V._probe_duration = lambda p_: 12.5
            e11b = make_ep(td / 'src' / 'k11_cnt', qc_secret=False)
            (e11b / 'ep99.srt').write_text(SRT + '\r\n4\r\n00:00:06,000 --> 00:00:06,500\r\n덧붙은 자막\r\n', encoding='utf-8', newline='')
            r_cnt, w_cnt = refused(pkg, e11b, 'ep61_cnt', td / 'b' / 'k11_cnt.zip', probe=True)
            e11c = make_ep(td / 'src' / 'k11_end', qc_secret=False)
            (e11c / 'ep99.srt').write_text(SRT.replace('00:00:04,250 --> 00:00:06,000', '00:00:04,250 --> 00:00:09,000'),
                                           encoding='utf-8', newline='')
            r_end, w_end = refused(pkg, e11c, 'ep60_end', td / 'b' / 'k11_end.zip', probe=True)
            ok_k11 = (bc.get('ok') is True and bc.get('mp4_s') == 12.5 and bc.get('timeline_end_s') == 12.5
                      and bc.get('srt_cues') == 3 and bc.get('timeline_captions') == 3 and not bc.get('not_measured')
                      and r_len and 'MP4 길이' in w_len and not (td / 'b' / 'k11_len.zip').exists()
                      and r_cnt and '자막 수' in w_cnt and r_end and '자막 마지막 줄' in w_end)
            V._probe_duration = lambda p_: FAKE_MP4_S
            ri, wi = refused(pkg, e11b, 'ep61_cnti', td / 'b' / 'k11_cnti.zip', probe=True, internal=True)
            ok_k11b = ri and '자막 수' in wi
            #  N4 — 자막 마지막 줄이 MP4 길이 + 0.5 s 를 넘는다 (시간표 · 자막은 서로 맞음 · MP4 ↔ 시간표 끝도 맞음)
            e11d = make_ep(td / 'src' / 'k11_over', qc_secret=False)
            (e11d / 'ep99.srt').write_text(SRT.replace('00:00:04,250 --> 00:00:06,000', '00:00:04,250 --> 00:00:13,400'),
                                           encoding='utf-8', newline='')
            tl_d = json.loads((e11d / 'timeline.json').read_text(encoding='utf-8'))
            tl_d['captions'][-1]['off'] = 13.4
            (e11d / 'timeline.json').write_text(json.dumps(tl_d), encoding='utf-8')
            r_ov, w_ov = refused(pkg, e11d, 'ep59_over', td / 'b' / 'k11_over.zip', probe=True)
            ok_k11d = r_ov and '자막 마지막 줄 ↔ MP4 길이' in w_ov and not (td / 'b' / 'k11_over.zip').exists()
        except Exception as e:                              # noqa: BLE001
            print(f'    K11 예외 — {type(e).__name__}: {e}')
        finally:
            V._probe_duration = old_probe
        try:
            #  공개판 · --no-probe = 거부 · 공개판 · ffprobe 없음 (진짜 _probe_duration · PATH 에 ffprobe 없음) = 거부 · 사유에 값 없음
            r_np, w_np = refused(pkg, e11, 'ep62_bcn', td / 'b' / 'k11_np.zip', probe=False)
            old_path = os.environ.get('PATH', '')
            V._probe_duration = _REAL_PROBE[0] if _REAL_PROBE else old_probe
            os.environ['PATH'] = str(td / 'no_bin')
            try:
                r_nf, w_nf = refused(pkg, e11, 'ep62_bcf', td / 'b' / 'k11_nf.zip', probe=True)
            finally:
                os.environ['PATH'] = old_path
                V._probe_duration = old_probe
            #  내부판 (검토 후보) = 미측정 기록 · 자막 ↔ 시간표 대조는 그대로
            m11n = pkg(e11, 'ep62_bcni', td / 'b' / 'k11_npi.zip', probe=False, internal=True) or {}
            bcn = m11n.get('build_check') or {}
            r_npi, w_npi = refused(pkg, e11b, 'ep61_cntn', td / 'b' / 'k11_cntn.zip', probe=False, internal=True)
            ok_k11c = (r_np and r_nf and all('MP4 길이' in w_ and '다 재지 못했다' in w_ and not re.search(r'\d+\.\d', w_)
                                             for w_ in (w_np, w_nf))
                       and not (td / 'b' / 'k11_np.zip').exists() and not (td / 'b' / 'k11_nf.zip').exists()
                       and m11n.get('visibility') == 'internal' and bcn.get('ok') is True and bcn.get('mp4_s') is None
                       and {'MP4 길이 ↔ 시간표 끝', '자막 마지막 줄 ↔ MP4 길이'} <= set(bcn.get('not_measured') or [])
                       and r_npi and '자막 수' in w_npi)
        except Exception as e:                              # noqa: BLE001
            print(f'    K11c 예외 — {type(e).__name__}: {e}')
    chk('K11 판 대조 — MP4 길이 ↔ 시간표 끝 · 자막 수 ↔ 시간표 자막 수 · 자막 마지막 줄 ↔ 시간표 마지막 자막 (허용 0.5 s) 이 맞으면 꾸러미 · '
        'episode.json build_check 기록 · 어긋나면 거부 (MP4 길이 · 자막 수 · 자막 마지막 줄)', ok_k11)
    chk('K11b 내부판 꾸러미도 같은 판 대조 (검토 후보 = 1저자가 듣는 판)', ok_k11b)
    chk('K11c 공개판 = MP4 길이를 못 재면 (ffprobe 없음 · --no-probe) 거부 (사유 = 대조 이름 · 값 없음 · 꾸러미 없음) · 내부판 (검토 후보) = '
        'build_check 에 미측정으로 적고 꾸린다 · 자막 ↔ 시간표 대조는 그대로 (Q4 3 회차 P2-1)', ok_k11c)
    chk('K11d 자막 마지막 줄 > MP4 길이 + 0.5 s = 거부 (시간표 · 자막이 서로 맞아도 · N4)', ok_k11d)

    # ═══ K12. 장면 파일 문장 ↔ 시간표 문장 (Q4 3 회차 P2-2 · 반례 (b)) — 공개판 · 내부판 둘 다 ═══
    ok_k12 = ok_k12b = False
    if have:
        try:
            e12 = make_ep(td / 'src' / 'k12_ahead', qc_secret=False)
            sj = json.loads((e12 / 'scenes.json').read_text(encoding='utf-8'))
            sj['scenes'][1]['lines'].append(dict(id='s02_l02', text='영상에 없는 문장 VDX-NOT-IN-VIDEO', captions=['덧']))
            (e12 / 'scenes.json').write_text(json.dumps(sj, ensure_ascii=False), encoding='utf-8')
            r_a, w_a = refused(pkg, e12, 'ep49_ahead', td / 'b' / 'k12_a.zip')
            r_ai, w_ai = refused(pkg, e12, 'ep49_aheadi', td / 'b' / 'k12_ai.zip', internal=True)
            e12t = make_ep(td / 'src' / 'k12_text', qc_secret=False)
            sj = json.loads((e12t / 'scenes.json').read_text(encoding='utf-8'))
            sj['scenes'][0]['lines'][1]['text'] = T_LINE2 + ' (고친 글)'
            (e12t / 'scenes.json').write_text(json.dumps(sj, ensure_ascii=False), encoding='utf-8')
            r_t, w_t = refused(pkg, e12t, 'ep48_text', td / 'b' / 'k12_t.zip')
            m12 = pkg(make_ep(td / 'src' / 'k12_ok', qc_secret=False), 'ep47_same', td / 'b' / 'k12_ok.zip') or {}
            b12 = m12.get('build_check') or {}
            ok_k12 = (r_a and r_ai and r_t and all('장면 파일 문장 ↔ 시간표 문장' in w_ for w_ in (w_a, w_ai, w_t))
                      and 'VDX-NOT-IN-VIDEO' not in w_a + w_ai + w_t and '고친 글' not in w_t
                      and not any((td / 'b' / n_).exists() for n_ in ('k12_a.zip', 'k12_ai.zip', 'k12_t.zip'))
                      and b12.get('ok') is True and b12.get('scene_lines') == 3 and b12.get('timeline_lines') == 3
                      and not b12.get('not_measured'))
        except Exception as e:                              # noqa: BLE001
            print(f'    K12 예외 — {type(e).__name__}: {e}')
        try:
            res12 = {}
            for nm_, gone, want_nm in (('k12_notl', 'timeline.json', ('MP4 길이 ↔ 시간표 끝', '장면 파일 문장 ↔ 시간표 문장')),
                                       ('k12_nosrt', 'ep99.srt', ('자막 수 ↔ 시간표 자막 수',)),
                                       ('k12_nosc', 'scenes.json', ('장면 파일 문장 ↔ 시간표 문장',))):
                d_ = make_ep(td / 'src' / nm_, qc_secret=False)
                (d_ / gone).unlink()
                rp_, wp_ = refused(pkg, d_, 'ep46_' + nm_[4:], td / 'b' / f'{nm_}.zip', title='제목 VDX-K12B')
                mi_ = pkg(d_, 'ep45_' + nm_[4:], td / 'b' / f'{nm_}_i.zip', internal=True, title='제목 VDX-K12B') or {}
                nm_got = (mi_.get('build_check') or {}).get('not_measured') or []
                res12[gone] = (rp_ and '다 재지 못했다' in wp_ and not (td / 'b' / f'{nm_}.zip').exists()
                               and all(w_ in nm_got for w_ in want_nm) and (mi_.get('build_check') or {}).get('ok') is True)
            ok_k12b = len(res12) == 3 and all(res12.values())
            if not ok_k12b:
                print(f'    K12b — {res12}')
        except Exception as e:                              # noqa: BLE001
            print(f'    K12b 예외 — {type(e).__name__}: {e}')
    chk('K12 장면 파일 문장 (id · 글) ↔ 시간표 문장 — 장면 파일이 한 문장 앞서거나 글이 다르면 꾸러미 거부 (공개판 · 내부판 둘 다 · 사유에 '
        '문장 글 없음) · 같으면 build_check 에 문장 수 기록 (Q4 3 회차 P2-2)', ok_k12)
    chk('K12b 공개판 = 판 대조 다섯을 다 잰다 (시간표 · 자막 · 장면 파일이 없으면 거부) · 내부판 = 못 잰 대조를 미측정으로 적고 꾸린다', ok_k12b)

    # ═══ K13. 등록 = 공개판은 판 대조 기록 (다 잰 통과 · 지금 판) 이 있어야 (Q4 3 회차 N10 · 반례 (d)) · 등록된 옛 판 = 공개 보류 ═══
    ok_k13 = ok_k13b = False
    if have:
        l13 = td / 'lib_k13'
        try:
            e13 = make_ep(td / 'src' / 'k13', qc_secret=False)
            pkg(e13, 'ep44_bc', td / 'b' / 'k13.zip')
            pkg(e13, 'ep44_bci', td / 'b' / 'k13i.zip', internal=True)
            variants = {
                'none': lambda m_: m_.pop('build_check', None),
                'unmeasured': lambda m_: m_['build_check'].update(not_measured=['MP4 길이 ↔ 시간표 끝']),
                'nomp4': lambda m_: m_['build_check'].update(mp4_s=None),
                'oldtool': lambda m_: m_['build_check'].pop('method', None),
            }
            res13 = {k_: refused(V.register_bundle, _rezip(td / 'b' / 'k13.zip', td / 'b' / f'k13_{k_}.zip', ed_), l13)
                     for k_, ed_ in variants.items()}
            V.register_bundle(_rezip(td / 'b' / 'k13i.zip', td / 'b' / 'k13i_none.zip', variants['none']), l13)
            V.register_bundle(td / 'b' / 'k13.zip', l13)
            ok_k13 = (all(r_ and '판 대조 기록' in w_ for r_, w_ in res13.values())
                      and (l13 / 'ep44_bci' / 'episode.json').is_file() and (l13 / 'ep44_bc' / 'episode.json').is_file())
            if not ok_k13:
                print(f'    K13 — {[(k_, r_, w_[:60]) for k_, (r_, w_) in res13.items()]}')
            _set_man(l13 / 'ep44_bc', lambda m_: m_.pop('build_check', None))
            cfg['VIDEO_FOLDER'] = str(l13)
            V._HELD_CACHE.clear()
            h13 = c.get('/videos/ep44_bc').get_data(as_text=True)
            why13 = (re.search(r'<ul class="vd-held">(.*?)</ul>', h13, re.S) or [None, ''])[1]
            ok_k13b = ('data-badge="public-held"' in h13 and '판 대조 기록' in why13
                       and c.get('/videos/ep44_bc', environ_base=far).status_code == 404
                       and c.get('/videos/ep44_bc/media/video', environ_base=far).status_code == 404)
        except Exception as e:                              # noqa: BLE001
            print(f'    K13 예외 — {type(e).__name__}: {e}')
        finally:
            cfg['VIDEO_FOLDER'] = str(lib)
    chk('K13 등록 — 공개판은 판 대조 기록 (다 잰 통과 · 지금 판) 이 있어야 (기록 없음 · 미측정 · MP4 못 잼 · 옛 도구 = 거부 · 반례 (d)) · '
        '내부판은 기록이 없어도 등록 · 기록이 있으면 등록', ok_k13)
    chk('K13b 판 대조 기록이 없는 등록된 공개판 = 공개 보류 (까닭 = 판 대조 기록 · 다른 컴퓨터 404 · 이 컴퓨터 빨간 배지)', ok_k13b)


if __name__ == '__main__':
    raise SystemExit(main())
