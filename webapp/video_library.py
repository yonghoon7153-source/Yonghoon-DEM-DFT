#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""웹앱 영상 섹션 (/videos) 의 라이브러리 — AVI 편 꾸러미 만들기 · 등록 · 읽기 (1저자 11-24).

1저자 11-24: *"믹서 avi 관련해서 완성되면 webapp에 영상 섹션을 추가해서 거기에 저장을 해서 실행하고 다운도 가능하게 …
세부내용들도 밑에 토글 등으로 … 유튜브 재생목록 인터페이스를 reference화"*.

  · 꾸러미 (bundle.zip) = **납작한** zip — episode.json + SHA256SUMS + 역할 파일 (ROLES: 영상 · 썸네일 · 자막 · 대본 · 장면 ·
    시간표 · QC · QC 기록 · 기준표 · README).  편 폴더의 **맨 위 일반 파일만** 넣는다 (하위 폴더 · 심볼릭 링크 · 역할 밖 파일 = 안 넣음).
  · 등록 (register_bundle) = 검사를 **다 지난 뒤에만** <폴더>/<ep_id>/ 에 쓴다 — 이름 꼴 (zip-slip · 구분자 · 점 파일) · 일반 파일 ·
    크기 상한 · SHA256SUMS ↔ episode.json ↔ 실제 바이트 · INTERNAL 표지 · 공개 안전 검사.  이미 있으면 거부 · 바꾸기는 명시
    (옛 판 = <폴더>/.replaced/ 에 보관 · 지우지 않는다).
  · 읽기 (library · episode_page · resolve_file) = 편마다 episode.json · SHA256SUMS · 파일 (일반 파일 · 크기 · sha256) 대조 —
    하나라도 어긋나면 그 편은 목록에서 빠지고 무엇이 깨졌는지 안내한다 (fail-closed).  파일 주소 = 등록된 편 · 등록된 역할만.
  · scripts/avi_package_episode.py · scripts/avi_register_episode.py · webapp/app.py (POST /videos/upload) 가 **같은 함수**를 부른다.
  · 지우기 (delete_episode · 1저자 11-25) = 영구 삭제가 아니다 — 편 폴더를 <폴더>/.deleted/<id>__<UTC 시각>/ 로 옮기고 (지우지 않는다 ·
    .replaced/ 보관과 같은 정신) 옆에 기록 <id>__<UTC 시각>.json (무엇 · 언제 · 명령 / web) · 되돌리기 = 그 폴더를 손으로 옮김.
    명령 (avi_register_episode.py --delete) · 화면 (POST /videos/<id>/delete · 이 컴퓨터 · 같은 출처 · 확인 창) 이 같은 함수를 부른다.
  · 내부판 (visibility internal) = 화면에 빨간 배지 · 공개 안전 검사는 기록만 · 공개판 = 검사 통과해야 꾸러미 · 등록.
  · 공개판 꾸러미 (Codex 11-25 AVI-02 · 1저자 11-25 Q1 · Q2 (가)) = 영상 · 썸네일 · 자막 · **시청자 대본** (장면 파일에서 만든다 ·
    제작 대본은 넣지 않는다) · **공개 장면** (장면 파일의 공개 투영) · 시간표만.  제작 기록 (QC · 점검 기록 · 기준표 · README) 은
    넣지 않고 episode.json `excluded` 에 이름 · 역할 · 사유 · 만든 두 파일은 `derived` (원본 sha256) 에 적는다.  내부판 = 그대로.
  · 공개 안전 검사 = 글 규칙 (IP · 주소 · 홈 경로 · 내부판 파일 이름 · 잡 번호 · 제작 표지) + 철회값 + git 커밋 식별자 (리포에서 실제
    커밋으로 풀리는 7–40 hex · git 을 못 쓰면 걸림) + 내부 숫자 목록 (수 경계로 맞춤).
  · 공개 보류 (Q4 P1-2 · fail-closed) = 등록된 공개판이 지금 공개판 기준 (공개 안전 검사 · 역할 · 장면 투영 · 판 대조 기록) 에 맞지 않으면
    다른 컴퓨터에는 등록 안 된 편과 같다 (목록 · 화면 · 재생 · 받기 · 자막) · 이 컴퓨터에는 빨간 '공개 보류 · 걸림' 배지와 까닭 (규칙 · 파일
    이름만).
  · 판 대조 (Q4 P2-6 · 3 회차 P2-1 · P2-2) = 꾸러미가 다섯을 대조한다 — MP4 길이 (ffprobe) ↔ 시간표 끝 · 자막 수 ↔ 시간표 자막 수 ·
    자막 마지막 줄 ↔ 시간표 마지막 자막 · 자막 마지막 줄 ≤ MP4 길이 (허용 0.5 s) · 장면 파일 문장 (id · 글) ↔ 시간표 문장.  어긋나면
    만들지 않는다 (공개판 · 내부판 둘 다).  공개판은 다섯을 다 재야 꾸린다 (ffprobe 없음 · --no-probe · 시간표 · 자막 · 장면 파일 없음 = 거부) ·
    내부판 (검토 후보) 은 못 잰 대조를 episode.json build_check 의 미측정으로 적는다.  공개판 등록 = 지금 판의 다 잰 통과 기록이 있어야
    (기록을 본다 — 등록 때 영상을 다시 재지 않는다).

⚠ Flask 를 import 하지 않는다 (명령에서도 쓴다).  app.py 는 이 모듈을 **라우트 함수 안에서만** import 한다 — 194 실행기
  (`scripts/run_network_194_parallel.py` DEP_LAZY_OFFPATH) 에 "웹앱 화면 · 라우트 전용" 으로 분류 (망 정지 경로 밖 · 봉인 32 밖).
⚠ 자료 값 · 문장을 여기에 베끼지 않는다 — 화면 글은 꾸러미 파일에서 읽는다 (회귀 webapp/test_video_page.py ⑥⑥).
"""
from __future__ import annotations

import contextlib
import hashlib
import html as _html
import json
import math
import mimetypes
import os
import re
import shutil
import subprocess
import tempfile
import time
import unicodedata
import zipfile
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

try:                                    # 화면 · 검사 글의 철회값 가림 (claims.json quotation_ban) — 웹앱과 같은 관문
    import ledger_view
except ImportError:                     # pragma: no cover — webapp 폴더가 sys.path 에 없을 때
    ledger_view = None

try:
    import fcntl
except ImportError:                     # pragma: no cover — 윈도우 (웹앱은 WSL 에서 돈다)
    fcntl = None

HERE = Path(__file__).resolve().parent
SCHEMA = 'avi-episode/1'
REG_SCHEMA = 'avi-registration/1'
DEL_SCHEMA = 'avi-deletion/1'
#: 지운 편의 보관 자리 (<폴더>/.deleted/) — 점으로 시작해 목록 (library) 이 읽지 않고 (.replaced/ 와 같다) · 편 id 꼴이 아니라 어떤 주소로도 안 열린다
DELETED_DIR = '.deleted'
KST = timezone(timedelta(hours=9))
ID_RE = re.compile(r'[a-z0-9][a-z0-9_]{1,63}')
RESERVED_IDS = frozenset({'upload'})
META_NAMES = ('episode.json', 'SHA256SUMS')
LOCAL_NAMES = ('registration.json',)            # 등록이 더하는 파일 (꾸러미 안에 오면 거부)

#: 크기 상한 (바이트) — 웹앱 MAX_CONTENT_LENGTH (2 GiB) 아래.  register_bundle(caps=…) 로 낮출 수 있다 (시험).
MAX_BUNDLE_BYTES = 1536 * 1024 * 1024
MAX_FILE_BYTES = 1536 * 1024 * 1024            # 영상 하나
MAX_TEXT_BYTES = 16 * 1024 * 1024              # 글 · 그림 하나
MAX_TOTAL_BYTES = 1600 * 1024 * 1024           # 풀었을 때 합
MAX_ENTRIES = 64

#: 역할 — 꾸러미 파일 하나 = 역할 하나.  text = 글 (UTF-8 · 공개 안전 검사 대상) · inline = 화면에서 바로 (재생 · poster) ·
#: download = 받기 단추 · ext = 이름 끝.  역할 밖 이름은 꾸러미에 넣지 않는다.
ROLES = {
    'video':     dict(max=1, text=False, inline=True,  download=True,  mime='video/mp4',            ext=('.mp4',)),
    'thumbnail': dict(max=1, text=False, inline=True,  download=False, mime=None,                   ext=('.png', '.jpg', '.jpeg')),
    'subtitles': dict(max=1, text=True,  inline=False, download=True,  mime='application/x-subrip', ext=('.srt',)),
    'script':    dict(max=1, text=True,  inline=False, download=True,  mime='text/markdown',        ext=('.md',)),
    'scenes':    dict(max=1, text=True,  inline=False, download=False, mime=None,                   ext=('.json',)),
    'timeline':  dict(max=1, text=True,  inline=False, download=False, mime=None,                   ext=('.json',)),
    'qc':        dict(max=1, text=True,  inline=False, download=False, mime=None,                   ext=('.md',)),
    'qc_report': dict(max=1, text=True,  inline=False, download=False, mime=None,                   ext=('.json',)),
    'rubric':    dict(max=1, text=True,  inline=False, download=False, mime=None,                   ext=('.md',)),
    'readme':    dict(max=1, text=True,  inline=False, download=False, mime=None,                   ext=('.md',)),
}
DOWNLOAD_ORDER = ('video', 'subtitles', 'script')

#: 공개판 꾸러미에 넣는 역할 (Codex 11-25 AVI-02) — 영상 · 썸네일 · 자막 · 시청자 대본 (만든 것) · 공개 장면 (투영) · 시간표.
#: 그 밖 역할 (qc · qc_report · rubric · readme = 제작 기록) 은 공개판에 넣지 않는다 (꾸러미 = episode.json `excluded` · 등록 = 거부).
PUBLIC_ROLES = ('video', 'thumbnail', 'subtitles', 'script', 'scenes', 'timeline')
PUBLIC_EXCLUDE_REASON = '제작 기록 — 공개판에 넣지 않는다 (QC · 점검 기록 · 기준표 · 편 설명)'
#: 공개 장면 (scenes.json 공개 투영) 에 남는 칸 — 머리 · 장면 · 문장 · 샷.  그 밖 칸 (읽는 꼴 · 메모 · 감정 · 강조 · 빠르기 · 쉼 ·
#: 목소리 모형 · 화면 개체 · 썸네일 …) 은 뺀다 (뺀 칸 이름 = episode.json derived `dropped_keys`).
PUBLIC_SCENE_HEAD = ('episode', 'title', 'subtitle', 'series', 'fps', 'width', 'height')
PUBLIC_SCENE_KEYS = ('id', 'title', 'lines', 'shots')
PUBLIC_LINE_KEYS = ('id', 'text', 'captions')
PUBLIC_SHOT_KEYS = ('id', 'from')
VIEWER_SCRIPT = 'viewer_script/1'
PUBLIC_SCENES = 'public_scenes/1'
_DERIVED_HOW = {VIEWER_SCRIPT: '시청자 대본 — 장면 제목 · 문장 글 + 제작 대본의 참고 문헌 목록 줄',
                PUBLIC_SCENES: '공개 장면 — 장면 파일의 공개 투영'}


class BundleError(ValueError):
    """꾸러미 · 등록 거부 — 글 = 무엇이 왜 (한국어 · 값은 적지 않는다)."""
    status = 400


class BundleExists(BundleError):
    status = 409


class BundleTooLarge(BundleError):
    status = 413


class EpisodeMissing(BundleError):
    """지우기 — 그 id 의 편 폴더가 없다 (영상 폴더가 없을 때 포함)."""
    status = 404


# ─────────────────────────────  작은 도우미  ─────────────────────────────

def default_folder():
    """영상 폴더 — 환경 변수 WEBAPP_VIDEO_FOLDER · 없으면 <webapp>/videos (git 밖 · .gitignore).  app.py 의 VIDEO_FOLDER 와 같은 규칙."""
    return os.environ.get('WEBAPP_VIDEO_FOLDER') or os.path.join(str(HERE), 'videos')


def check_id(ep_id):
    if not isinstance(ep_id, str) or not ID_RE.fullmatch(ep_id) or ep_id in RESERVED_IDS:
        raise BundleError(f'편 id 꼴이 아니다 — {ep_id!r} (소문자 · 숫자 · 밑줄 2–64 자 · 첫 글자 = 영문 소문자 · 숫자 · 예약어 upload 금지)')
    return ep_id


_BAD_NAME = re.compile(r'[\x00-\x1f\x7f/\\:*?"<>|]')


def name_ok(n):
    """꾸러미 · 등록 파일 이름 — 납작한 이름 하나 (경로 · 구분자 · 점으로 시작 · 제어 문자 · 앞뒤 공백 금지 · NFC)."""
    return (isinstance(n, str) and 0 < len(n) <= 160 and not _BAD_NAME.search(n) and not n.startswith(('.', '-'))
            and n == n.strip() and n not in ('.', '..') and unicodedata.normalize('NFC', n) == n)


def role_of(name):
    """편 폴더 파일 이름 → 역할 (꾸러미에 넣을 것) · 없으면 None."""
    low = name.lower()
    if low.endswith('.mp4'):
        return 'video'
    if low in ('thumbnail.png', 'thumbnail.jpg', 'thumbnail.jpeg') or (low.startswith('thumb') and low.endswith(('.png', '.jpg', '.jpeg'))):
        return 'thumbnail'
    if low.endswith('.srt'):
        return 'subtitles'
    if low == 'script.md':
        return 'script'
    if low == 'scenes.json':
        return 'scenes'
    if low == 'timeline.json':
        return 'timeline'
    if low.startswith('qc_report') and low.endswith('.json'):
        return 'qc_report'
    if low == 'qc.md' or (low.startswith('qc_') and low.endswith('.md')):
        return 'qc'
    if low.startswith('rubric') and low.endswith('.md'):
        return 'rubric'
    if low.startswith('readme') and low.endswith('.md'):
        return 'readme'
    return None


def _finite(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def fmt_clock(t):
    """초 → m:ss (한 시간 넘으면 h:mm:ss) · 내림."""
    if not _finite(t) or t < 0:
        return '—'
    s = int(t)
    h, rem = divmod(s, 3600)
    m, s = divmod(rem, 60)
    return f'{h}:{m:02d}:{s:02d}' if h else f'{m}:{s:02d}'


def fmt_size(n):
    if not isinstance(n, int) or n < 0:
        return '—'
    for unit, div in (('GB', 1024 ** 3), ('MB', 1024 ** 2), ('KB', 1024)):
        if n >= div:
            return f'{n / div:.1f} {unit}'
    return f'{n} B'


def _sha_stream(fh, limit=None):
    """파일 객체 → (sha256 hex, 읽은 바이트 수) · limit 를 넘으면 BundleTooLarge."""
    h, n = hashlib.sha256(), 0
    while True:
        b = fh.read(1024 * 1024)
        if not b:
            break
        n += len(b)
        if limit is not None and n > limit:
            raise BundleTooLarge(f'상한 ({fmt_size(limit)}) 을 넘는 항목')
        h.update(b)
    return h.hexdigest(), n


_HASH_CACHE = {}


def _file_sha(path, st=None):
    """등록 폴더 파일의 sha256 — (장치 · inode · 크기 · mtime · ctime) 가 같으면 다시 재지 않는다 (재생 중 Range 요청마다 영상 전체를 읽지 않게)."""
    st = st or os.stat(path)
    key = (str(path), st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns)
    h = _HASH_CACHE.get(key)
    if h is None:
        with open(path, 'rb') as f:
            h = _sha_stream(f)[0]
        if len(_HASH_CACHE) > 512:
            _HASH_CACHE.clear()
        _HASH_CACHE[key] = h
    return h


def _r(s):
    """화면 글 — 철회값을 자리 표지로 (ledger_view.redact)."""
    s = '' if s is None else str(s)
    if ledger_view is None:
        return s
    try:
        return ledger_view.redact(s)
    except Exception:                    # noqa: BLE001 — 가림이 실패해도 화면은 그린다 (글 자체는 이미 등록 검사를 지났다)
        return s


def _now_kst():
    return datetime.now(KST)


# ─────────────────────────────  공개 안전 검사  ─────────────────────────────

#: (규칙 이름, 정규식) — 공개판 글 (자막 · 대본 · 장면 · QC · episode.json) 에 있으면 안 되는 것.  걸린 **값은 기록하지 않는다** (파일 · 줄 · 규칙만).
PUBLIC_RULES = (
    ('IP 주소', re.compile(r'(?<![\d.])(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)(?![\d.])')),
    ('localhost · 루프백', re.compile(r'\blocalhost\b|(?<![\d.])0\.0\.0\.0(?![\d.])|\[::1\]', re.I)),
    ('주소 · 포트', re.compile(r'\b(?:[A-Za-z0-9-]+\.)+(?!(?:py|md|json|sh|txt|csv|tsv|js|html?|xml|png|jpe?g|srt|vtt|mp4|zip)\b)'
                            r'[A-Za-z]{2,}:\d{2,5}\b|(?:\bport|포트)\s*[:=]?\s*\d{2,5}\b', re.I)),
    ('홈 경로', re.compile(r'/home/[A-Za-z0-9_.-]+|/mnt/[a-z]/Users\b|\b[A-Za-z]:\\Users\\|/Users/[A-Za-z0-9_.-]+|/root/')),
    ('내부판 파일 이름', re.compile(r'[\w.-]*INTERNAL[\w.-]*\.(?:mp4|mov|webm|srt|vtt|md|json|png|jpe?g|wav|zip)\b')),
    ('잡 번호', re.compile(r'\b(?:job|jobid)\s*[:#=]?\s*\d{4,}\b|잡\s*(?:번호\s*)?\d{4,}', re.I)),
)

#: 제작 표지 (Codex 11-25 AVI-02) — 제작 쪽 기록에만 있어야 할 낱말 · 꼴.  공개판 글에 있으면 거부 (값은 적지 않는다).
#: '1저자' 앞에 한글 · 숫자가 붙으면 다른 낱말 ('제1저자' = 일반 낱말) · '조수' 앞에 한글이 붙으면 다른 낱말 ('제조수율' · '구조수정' ·
#: '보조수단') · 'DECISIONS' 는 대문자만 (영어 'decisions' 는 보통 낱말) · 목소리 ID = Typecast 꼴 'tc_' + hex 20 자 이상.
PRODUCTION_MARKS = ('1저자', 'Codex', 'Claude', '조수', 'internal/', 'voice-auto', 'DECISIONS', 'tc_<hex 20+>')
PUBLIC_RULES += (
    ('제작 표지', re.compile(r'(?<![가-힣0-9])1저자'
                            r'|(?<![가-힣])조수'
                            r'|(?<![A-Za-z])(?i:codex|claude)(?![A-Za-z])'
                            r'|(?i:internal)[/\\]'
                            r'|(?i:voice[-_]auto)'
                            r'|DECISIONS'
                            r'|(?<![A-Za-z0-9])(?i:tc_[0-9a-f]{20,})')),
)
BAN_RULE = '철회값 (claims.json quotation_ban)'

#: git 커밋 식별자 (Codex 11-25 AVI-02 · 공개 script.md 34 행에 커밋 둘) — 7–40 자리 hex 낱말 중 글자 (a–f) 와 숫자가 **둘 다** 든 것만
#: 후보 (숫자만 = 날짜 · 수 · 64 hex = sha256 은 후보 아님 · 앞뒤에 영문 · 숫자가 붙으면 낱말이 아님) → `git cat-file --batch-check`
#: **한 번** 으로 `<낱말>^{commit}` (커밋으로 풀리나) 와 `<낱말>` (둘 넘는 개체의 앞자리 = 모호) 를 대조한다.  풀리거나 모호하면 걸림.
#: ⚠ `^{commit}` 만 물으면 커밋 둘이 앞자리를 나눠 가진 짧은 sha 가 'missing' 으로 나온다 (git 2.43 실측) — 그래서 `<낱말>` 도 묻는다.
#: git 을 못 쓰면 (없음 · 저장소 아님 · 시간 초과 · 출력 꼴) 후보가 있는 글 = 걸림 (fail-closed · COMMIT_FAIL_RULE).
COMMIT_RULE = 'git 커밋 식별자'
COMMIT_FAIL_RULE = 'git 커밋 식별자 검사 못 함'
GIT_EXE = 'git'
_HEX_TOKEN = re.compile(r'(?<![0-9A-Za-z])[0-9A-Fa-f]{7,40}(?![0-9A-Za-z])')
_GIT_ENV_DROP = ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'GIT_OBJECT_DIRECTORY', 'GIT_ALTERNATE_OBJECT_DIRECTORIES',
                 'GIT_COMMON_DIR', 'GIT_NAMESPACE', 'GIT_CEILING_DIRECTORIES')
_OID = re.compile(r'[0-9a-f]{40}|[0-9a-f]{64}')
_OBJ_TYPES = ('commit', 'tree', 'blob', 'tag')


def _commit_candidates(line):
    """한 줄 → 커밋 식별자 후보 낱말 (소문자) 목록."""
    out = []
    for m in _HEX_TOKEN.finditer(line):
        t = m.group(0)
        if re.search('[A-Fa-f]', t) and re.search('[0-9]', t):
            out.append(t.lower())
    return out


def _git_commit_tokens(tokens, repo_root=None):
    """후보 낱말 → (커밋 · 모호로 풀린 낱말 집합, 못 쓴 까닭 또는 None).  git 은 한 번만 부른다 (낱말마다 두 줄).

    저장소 = repo_root (없으면 이 라이브러리가 든 리포 뿌리 · 그 폴더 자신이 저장소여야 한다 — 위 폴더로 찾아 올라가지 않는다)."""
    toks = sorted(set(tokens))
    if not toks:
        return set(), None
    root = Path(repo_root) if repo_root is not None else HERE.parent
    env = {k: v for k, v in os.environ.items() if k not in _GIT_ENV_DROP}
    env['GIT_CEILING_DIRECTORIES'] = str(root.resolve().parent)
    env['GIT_TERMINAL_PROMPT'] = '0'
    inp = ''.join(f'{t}^{{commit}}\n{t}\n' for t in toks)
    try:
        p = subprocess.run([GIT_EXE, '-C', str(root), 'cat-file', '--batch-check'], input=inp, capture_output=True, text=True,
                           timeout=60, env=env)
    except (OSError, ValueError, subprocess.SubprocessError) as e:
        return set(), type(e).__name__
    out = p.stdout.splitlines()
    if p.returncode != 0:
        return set(), f'git rc {p.returncode}'
    if len(out) != 2 * len(toks):
        return set(), 'git 출력 줄 수'
    hits = set()
    for i, t in enumerate(toks):
        a, b = out[2 * i].split(), out[2 * i + 1].split()
        if len(a) == 3 and _OID.fullmatch(a[0]) and a[1] == 'commit':
            hits.add(t)
        elif a == [f'{t}^{{commit}}', 'ambiguous']:
            hits.add(t)
        elif a != [f'{t}^{{commit}}', 'missing']:
            return set(), 'git 출력 꼴'
        if b == [t, 'ambiguous']:
            hits.add(t)
        elif not (b == [t, 'missing'] or (len(b) == 3 and _OID.fullmatch(b[0]) and b[1] in _OBJ_TYPES)):
            return set(), 'git 출력 꼴'
    return hits, None


def _deny_rx(lit):
    """내부 숫자 목록의 글자열 하나 → 정규식 — **수 경계로만** 맞춘다 (Codex 11-25 · '0.5' 가 '10.5' · '0.55' · '1.0.5' 안에서 걸리지 않는다).
    글자열 끝이 숫자면 그 바깥에 숫자 · (소수점 + 숫자) 가 붙지 않아야 한다 · 끝이 숫자가 아니면 그쪽은 그냥 맞춘다."""
    pre = r'(?<![0-9])(?<![0-9]\.)' if lit[:1] in tuple('0123456789.') else ''
    post = r'(?![0-9])(?!\.[0-9])' if lit[-1:] in tuple('0123456789') else ''
    return re.compile(pre + re.escape(lit) + post)


_WS = {' ': ' ', ' ': ' ', ' ': ' ', ' ': ' ', '−': '-'}


def _norm(s):
    for a, b in _WS.items():
        s = s.replace(a, b)
    return unicodedata.normalize('NFC', s)


def load_deny_list(path):
    """내부 숫자 목록 (리포 · 꾸러미 밖에 두는 파일) → (글자열 목록, sha256).  한 줄에 하나 · # = 주석 · 4 자 이상 ·
    숫자 3 개 이상이거나 6 자 이상 (짧은 글자열은 거짓 경보가 많아 거부한다 — fail-closed)."""
    p = Path(path)
    try:
        raw = p.read_bytes()
        txt = raw.decode('utf-8')
    except (OSError, ValueError) as e:
        raise BundleError(f'내부 숫자 목록을 읽지 못했다 ({type(e).__name__})')
    lits = []
    for i, ln in enumerate(txt.splitlines(), 1):
        s = ln.strip()
        if not s or s.startswith('#'):
            continue
        s = _norm(s)
        if len(s) < 4 or (sum(ch.isdigit() for ch in s) < 3 and len(s) < 6):
            raise BundleError(f'내부 숫자 목록 {i} 째 줄이 너무 짧다 (4 자 이상 · 숫자 3 개 이상이거나 6 자 이상) — 거짓 경보를 막으려고 거부한다')
        lits.append(s)
    if not lits:
        raise BundleError('내부 숫자 목록이 비어 있다')
    return lits, hashlib.sha256(raw).hexdigest()


#: 1저자 11-24 Q2 — 편 폴더 (AVI 작업 폴더) 의 internal/ 안에 두는 내부 숫자 목록의 이름.  공개판을 꾸릴 때 이 파일이 있으면 **늘** 검사한다
#: (--deny-list 를 주지 않아도 · 걸리면 꾸러미를 만들지 않는다 · fail-closed).  찾는 자리 = <편 폴더>/internal/ 와 --video 로 고른 영상 폴더의
#: internal/ (글 = 리포 사본 · 영상 = 작업 폴더 꼴).  목록 파일은 꾸러미 (역할 밖 · 하위 폴더) 와 리포 (.gitignore) 에 들어가지 않는다.
DENY_LIST_NAME = 'public_deny_list.txt'


def find_deny_lists(ep_dir, video=None):
    """공개판 꾸러미가 늘 쓰는 내부 숫자 목록 자리 → [Path] (있는 것만 · 같은 파일은 한 번).  자리가 있는데 일반 파일이 아니면
    (폴더 · 심볼릭 링크) BundleError — 목록을 못 읽고 지나가지 않는다 (fail-closed)."""
    cands = [Path(ep_dir) / 'internal' / DENY_LIST_NAME]
    if video is not None:
        cands.append(Path(video).resolve().parent / 'internal' / DENY_LIST_NAME)
    out, seen = [], set()
    for p in cands:
        if not (p.exists() or p.is_symlink()):
            continue
        if p.is_symlink() or not p.is_file():
            raise BundleError(f'내부 숫자 목록 자리 (internal/{DENY_LIST_NAME}) 가 일반 파일이 아니다 — 고친 뒤 꾸린다 (fail-closed)')
        key = os.path.realpath(p)
        if key not in seen:
            seen.add(key)
            out.append(p)
    return out


def public_check(texts, deny=None, repo_root=None):
    """[(파일 이름, 글)] → dict(ok, rules, files, hits=[dict(file, line, rule, claim? · item? · n? · why?)], deny_list, ban_list).

    공개판에서 거부 · 내부판에서 기록만.  ⚠ 걸린 값은 어디에도 남기지 않는다 (철회값 · 내부 숫자 · 커밋 식별자는 값 자체가 누수다).
    repo_root = 커밋 식별자를 대조할 저장소 (없으면 이 라이브러리가 든 리포 뿌리)."""
    hits = []
    bans, ban_err = [], None
    if ledger_view is None:
        ban_err = 'ledger_view 를 읽지 못했다'
    else:
        try:
            if ledger_view.error():
                ban_err = '철회값 등록부 (claims.json) 를 읽지 못했다'
            bans = ledger_view._redactor()
        except Exception as e:           # noqa: BLE001
            ban_err = f'철회값 등록부를 읽지 못했다 ({type(e).__name__})'
    deny_lits, deny_sha = (deny or ([], None))
    deny_rx = [_deny_rx(lit) for lit in deny_lits]
    cands = []                            # (파일, 줄, 후보 낱말들) — git 은 아래에서 한 번만
    for name, text in texts:
        for i, ln in enumerate(str(text).splitlines(), 1):
            nl = _norm(ln)
            for rule, rx in PUBLIC_RULES:
                if rx.search(nl):
                    hits.append(dict(file=name, line=i, rule=rule))
            for rx, claim in bans:
                if rx.search(ln) or rx.search(nl):
                    hits.append(dict(file=name, line=i, rule=BAN_RULE, claim=str(claim)))
            for k, rx in enumerate(deny_rx, 1):
                if rx.search(nl):
                    hits.append(dict(file=name, line=i, rule='내부 숫자 목록', item=k))
            toks = _commit_candidates(nl)
            if toks:
                cands.append((name, i, toks))
    if cands:
        found, git_err = _git_commit_tokens([t for _, _, ts in cands for t in ts], repo_root)
        if git_err:
            hits.append(dict(file='', line=0, rule=COMMIT_FAIL_RULE, why=git_err))
        for name, i, ts in cands:
            n = len({t for t in ts if t in found})
            if n:
                hits.append(dict(file=name, line=i, rule=COMMIT_RULE, n=n))
    if ban_err:
        hits.append(dict(file='', line=0, rule=ban_err))
    return dict(ok=not hits, rules=[r for r, _ in PUBLIC_RULES] + [BAN_RULE, COMMIT_RULE], files=len(texts),
                hits=hits, deny_list=(dict(n=len(deny_lits), sha256=deny_sha) if deny_sha else None),
                ban_list=dict(n=len(bans), error=ban_err))


def _hits_text(pc, limit=8):
    out = []
    for h in pc.get('hits') or []:
        where = f"{h.get('file')}:{h.get('line')}" if h.get('file') else ''
        extra = (f" ({h['claim']})" if h.get('claim') else f" (목록 {h['item']} 째)" if h.get('item')
                 else f" ({h['n']} 개)" if h.get('n') else f" ({h['why']})" if h.get('why') else '')
        out.append(f"{h.get('rule')}{extra}{' · ' + where if where else ''}")
    more = len(out) - limit
    return ' · '.join(out[:limit]) + (f' · 그 밖 {more} 건' if more > 0 else '')


# ─────────────────────────────  시청자 대본 · 공개 장면 (공개판 · Codex 11-25 AVI-02 · 1저자 11-25 Q2 (가))  ─────────────────────────────

_MD_ESC = (('\\', '\\\\'), ('&', '&amp;'), ('<', '&lt;'), ('>', '&gt;'), ('"', '&quot;'), ('[', '\\['), ('`', '\\`'),
           ('*', '\\*'), ('_', '\\_'))
_MD_LEAD = re.compile(r'#|[-+]|\d{1,9}(?=[.)](?:\s|$))|~')
_REF_ITEM = re.compile(r'(?:\d{1,3}[.)]|[-*+])[ \t]+\S')
_HEADING = re.compile(r'#{1,6}(?:[ \t]|$)')


def _md_plain(s):
    """평문 한 줄 → md 에서 글 그대로 보이게 — 태그 · 링크 · 강조 · 코드 꼴을 막고 (문자 참조 · 역빗금) 줄머리 표지 (# - + 1. 1) ~) 를 막는다."""
    for a, b in _MD_ESC:
        s = s.replace(a, b)
    m = _MD_LEAD.match(s)
    if m:
        g = m.group(0)
        if g[0].isdigit():
            s = g + '\\' + s[len(g):]                    # '1. x' → '1\. x'
        elif g == '~':
            s = '&#126;' + s[1:]                          # 울타리 (~~~) 막음
        else:
            s = '\\' + s
    return s


def public_refs(script_md):
    """제작 대본 → 공개 참고 문헌 목록 줄 [str] — 첫 '## … 참고 문헌 …' 절의 **들여쓰지 않은 목록 줄만** (번호 · - · * · + 로 시작).
    머리 줄 (괄호 설명 · 판 기록 · 커밋 식별자) · 목록 밖 글 · 들여쓴 하위 줄 · 다음 머리 줄 뒤는 버린다."""
    if not isinstance(script_md, str):
        return []
    lines = script_md.splitlines()
    start = next((i for i, ln in enumerate(lines) if ln.startswith('## ') and '참고 문헌' in ln), None)
    if start is None:
        return []
    out = []
    for ln in lines[start + 1:]:
        if _HEADING.match(ln):
            break
        if _REF_ITEM.match(ln):
            out.append(ln.rstrip())
    return out


def viewer_script(scenes, script_md=None, *, title=None, subtitle=None, series=None):
    """장면 파일 (+ 제작 대본) → 시청자 대본 md 글 (공개판의 script.md · 1저자 11-25 Q2 (가)).

    # 제목 · 부제 · 시리즈 한 줄 → 장면마다 '## 장면 제목' + 그 장면 문장의 글 (text) 을 순서대로 (한 문장 = 한 문단 · 평문 그대로 보이게) →
    '## 참고 문헌' + 제작 대본 참고 문헌 절의 목록 줄 (public_refs · 없으면 절도 없음).  읽는 꼴 (say) · 메모 · 감정 · 제작 이력 = 넣지 않는다."""
    sc = scenes if isinstance(scenes, dict) else {}
    t = title if isinstance(title, str) and title.strip() else sc.get('title')
    out = ['# ' + (_md_plain(t.strip()) if isinstance(t, str) and t.strip() else '대본'), '']
    sub = subtitle if isinstance(subtitle, str) else sc.get('subtitle')
    ser = series if isinstance(series, str) else sc.get('series')
    head = ' · '.join(x.strip() for x in (sub, ser) if isinstance(x, str) and x.strip())
    if head:
        out += [_md_plain(head), '']
    for s in sc.get('scenes') if isinstance(sc.get('scenes'), list) else []:
        if not isinstance(s, dict):
            continue
        st = s.get('title') if isinstance(s.get('title'), str) and s.get('title').strip() else s.get('id')
        if not isinstance(st, str) or not st.strip():
            continue
        if '참고 문헌' in st:
            raise BundleError("장면 제목에 '참고 문헌' 이 들어 있다 — 시청자 대본의 참고 문헌 절과 헷갈린다 (장면 제목을 바꾼다)")
        out += ['## ' + _md_plain(st.strip()), '']
        for ln in s.get('lines') if isinstance(s.get('lines'), list) else []:
            if not isinstance(ln, dict) or not isinstance(ln.get('text'), str):
                continue
            for part in ln['text'].splitlines():
                if part.strip():
                    out += [_md_plain(part.strip()), '']
    refs = public_refs(script_md)
    if refs:
        out += ['## 참고 문헌', ''] + refs + ['']
    return '\n'.join(out).rstrip('\n') + '\n'


def public_scenes(scenes):
    """장면 파일 → (공개 투영 dict, 뺀 칸 [str]) — 머리 = PUBLIC_SCENE_HEAD · 장면 = id · title · lines[id · text · captions] ·
    shots[id · from].  글 칸은 글 (str) · captions = 글 목록 · fps · width · height = 수 — 꼴이 다르면 그 칸도 뺀다 (안에 제작 자료가 숨지 않게)."""
    dropped = set()
    out = {}
    for k, v in scenes.items():
        if k == 'scenes':
            continue
        if k in PUBLIC_SCENE_HEAD and (isinstance(v, str) if k in ('episode', 'title', 'subtitle', 'series') else _finite(v)):
            out[k] = v
        else:
            dropped.add(k)
    raw = scenes.get('scenes')
    if raw is not None and not isinstance(raw, list):
        dropped.add('scenes')
    scs = []
    for sc in raw if isinstance(raw, list) else []:
        if not isinstance(sc, dict):
            dropped.add('scenes[]')
            continue
        s2 = {}
        for k, v in sc.items():
            if k in PUBLIC_SCENE_KEYS and k not in ('lines', 'shots') and isinstance(v, str):
                s2[k] = v
            elif k not in PUBLIC_SCENE_KEYS or k in ('id', 'title') or not isinstance(v, list):
                dropped.add(f'scenes.{k}')
        for key, keep in (('lines', PUBLIC_LINE_KEYS), ('shots', PUBLIC_SHOT_KEYS)):
            rows = []
            for x in sc.get(key) if isinstance(sc.get(key), list) else []:
                if not isinstance(x, dict):
                    dropped.add(f'{key}[]')
                    continue
                r = {}
                for k, v in x.items():
                    if k in keep and k != 'captions' and isinstance(v, str):
                        r[k] = v
                    elif k == 'captions' and key == 'lines' and isinstance(v, list) and all(isinstance(c, str) for c in v):
                        r[k] = list(v)
                    else:
                        dropped.add(f'{key}.{k}')
                rows.append(r)
            s2[key] = rows
        scs.append(s2)
    out['scenes'] = scs
    return out, sorted(dropped)


# ─────────────────────────────  판 대조 (영상 ↔ 시간표 ↔ 자막 · Q4 P2-6)  ─────────────────────────────

#: 같은 빌드인지 보는 허용폭 (초) — MP4 길이 ↔ 시간표 끝 · 자막 마지막 줄 ↔ 시간표 마지막 자막 · 자막 마지막 줄 ≤ MP4 길이 + 이 값
BUILD_TOL_S = 0.5
#: 판 대조 기록의 판 — 2 = 대조 다섯 (장면 파일 문장 포함 · Q4 3 회차 P2-2).  공개판 등록 · 공개 보류는 이 판의 다 잰 통과 기록만 받는다.
BUILD_CHECK = 'build_check/2'
#: 판 대조 다섯 — 이름 = 거부 사유 · 미측정 목록의 낱말 (값이 아니다)
BUILD_CMP = ('MP4 길이 ↔ 시간표 끝', '자막 수 ↔ 시간표 자막 수', '자막 마지막 줄 ↔ 시간표 마지막 자막', '자막 마지막 줄 ↔ MP4 길이',
             '장면 파일 문장 ↔ 시간표 문장')
_LINE_ID = re.compile(r'[A-Za-z0-9_-]{1,40}')


def _srt_cues(text):
    """SRT 글 → [(시작 s, 끝 s)] — srt_to_vtt 와 같은 덩어리 규칙 (번호 줄 · 시각 줄 없는 덩어리는 건너뜀)."""
    t = str(text).lstrip('\ufeff').replace('\r\n', '\n').replace('\r', '\n')
    out = []
    for block in re.split(r'\n[ \t]*\n', t.strip()):
        lines = block.split('\n')
        if lines and lines[0].strip().isdigit():
            lines = lines[1:]
        if not lines:
            continue
        m = _SRT_TIME.search(lines[0])
        if not m:
            continue
        g = [int(x) for x in m.groups()]
        out.append((g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000.0, g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000.0))
    return out


def _line_pairs(lines):
    """문장 목록 → [(id, 글)] — 글이 있는 문장만 (객체 · 글 = 빈칸 아닌 str · 순서 그대로)."""
    return [(ln.get('id'), ln['text']) for ln in lines
            if isinstance(ln, dict) and isinstance(ln.get('text'), str) and ln['text'].strip()]


def _scene_line_pairs(scenes):
    """장면 파일 → 장면 순서 · 문장 순서의 [(id, 글)] · 꼴이 아니거나 글 있는 문장이 없으면 None (못 잼)."""
    if not isinstance(scenes, dict) or not isinstance(scenes.get('scenes'), list):
        return None
    out = []
    for sc in scenes['scenes']:
        if isinstance(sc, dict) and isinstance(sc.get('lines'), list):
            out += _line_pairs(sc['lines'])
    return out or None


def _timeline_line_pairs(timeline):
    """시간표 → lines 의 [(id, 글)] (avi_timeline.all_lines 가 장면 파일 문장을 그대로 잇는다) · 없으면 None (못 잼)."""
    tl = timeline if isinstance(timeline, dict) else {}
    return (_line_pairs(tl['lines']) or None) if isinstance(tl.get('lines'), list) else None


def build_check(mp4_s, timeline, srt_text, scenes=None):
    """영상 · 시간표 · 자막 · 장면 파일이 같은 판인가 → dict(ok, method, mp4_s, timeline_end_s, srt_cues, timeline_captions,
    srt_last_end_s, timeline_last_off_s, scene_lines, timeline_lines, tol_s, problems, not_measured).  못 잰 쪽이 있는 대조는
    미측정으로 남긴다 (짐작으로 채우지 않는다).

    대조 다섯 (BUILD_CMP) = MP4 길이 ↔ 시간표 끝 (summary.duration_s) · 자막 수 ↔ 시간표 자막 수 · 자막 마지막 줄 끝 ↔ 시간표 마지막 자막 끝 ·
    자막 마지막 줄 끝 ≤ MP4 길이 (허용 BUILD_TOL_S · 수는 같아야) · 장면 파일 문장 ↔ 시간표 문장 (글 있는 문장의 id · 글 · 순서가 같아야 ·
    시청자 대본 · 공개 장면의 원본이 영상과 같은 판인가 · Q4 3 회차 P2-2).  ⚠ 판이 다르면 (예: 리포의 옛 판 글 + 새 MP4 · 한 문장 앞선
    장면 파일) 여기서 걸린다 · 사유에 문장 글은 적지 않는다 (수 · 처음 다른 문장 id 만)."""
    tl = timeline if isinstance(timeline, dict) else {}
    summ = tl.get('summary') if isinstance(tl.get('summary'), dict) else {}
    t_end = float(summ['duration_s']) if _finite(summ.get('duration_s')) else None
    caps = tl.get('captions') if isinstance(tl.get('captions'), list) else None
    offs = [float(c['off']) for c in caps or [] if isinstance(c, dict) and _finite(c.get('off'))]
    cues = _srt_cues(srt_text) if isinstance(srt_text, str) else None
    mp4 = float(mp4_s) if _finite(mp4_s) else None
    s_n = len(cues) if cues is not None else None
    s_last = max(e for _, e in cues) if cues else None
    t_n = len(caps) if caps is not None else None
    t_last = max(offs) if offs else None
    problems, nm = [], []

    def cmp(name, a, b, good, fmt='{:g}'):
        if a is None or b is None:
            nm.append(name)
        elif not good(a, b):
            problems.append(f'{name} ({fmt.format(a)} ↔ {fmt.format(b)})')
    cmp(BUILD_CMP[0], mp4, t_end, lambda a, b: abs(a - b) <= BUILD_TOL_S, '{:.3f} s')
    cmp(BUILD_CMP[1], s_n, t_n, lambda a, b: a == b, '{}')
    cmp(BUILD_CMP[2], s_last, t_last, lambda a, b: abs(a - b) <= BUILD_TOL_S, '{:.3f} s')
    cmp(BUILD_CMP[3], s_last, mp4, lambda a, b: a <= b + BUILD_TOL_S, '{:.3f} s')
    sl, tlp = _scene_line_pairs(scenes), _timeline_line_pairs(timeline)
    if sl is None or tlp is None:
        nm.append(BUILD_CMP[4])
    elif sl != tlp:
        k = next((i for i, (a, b) in enumerate(zip(sl, tlp)) if a != b), min(len(sl), len(tlp)))
        pid = (sl[k] if k < len(sl) else tlp[k])[0]
        pid = pid if isinstance(pid, str) and _LINE_ID.fullmatch(pid) else '(꼴 밖 id)'
        problems.append(f'{BUILD_CMP[4]} ({len(sl)} ↔ {len(tlp)} 문장 · 처음 다른 문장 {pid})')
    return dict(ok=not problems, method=BUILD_CHECK, mp4_s=mp4, timeline_end_s=t_end, srt_cues=s_n, timeline_captions=t_n,
                srt_last_end_s=(round(s_last, 3) if s_last is not None else None),
                timeline_last_off_s=(round(t_last, 3) if t_last is not None else None),
                scene_lines=(len(sl) if sl is not None else None), timeline_lines=(len(tlp) if tlp is not None else None),
                tol_s=BUILD_TOL_S, problems=problems, not_measured=nm)


def build_record_ok(bc):
    """판 대조 기록이 공개판 기준인가 = 지금 판 (BUILD_CHECK) · 통과 · 미측정 없음 · MP4 를 ffprobe 로 잰 길이 (Q4 3 회차 N10).
    공개판 등록 · 공개 보류가 같은 함수.  ⚠ 기록을 본다 — 등록 때 영상을 다시 재지 않는다 (손으로 지은 기록까지 막는 자리는 아니다)."""
    return (isinstance(bc, dict) and bc.get('method') == BUILD_CHECK and bc.get('ok') is True
            and isinstance(bc.get('not_measured'), list) and not bc['not_measured'] and _finite(bc.get('mp4_s')))


# ─────────────────────────────  꾸러미 만들기  ─────────────────────────────

def _read_json_file(p, role):
    try:
        return json.loads(Path(p).read_text(encoding='utf-8'))
    except (OSError, ValueError) as e:
        raise BundleError(f'{Path(p).name} ({role}) 을 JSON 으로 읽지 못했다 ({type(e).__name__})')


def _probe_duration(video):
    """ffprobe 로 영상 길이 (초) · 없거나 실패하면 None."""
    exe = shutil.which('ffprobe')
    if not exe:
        return None
    try:
        p = subprocess.run([exe, '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nw=1:nk=1', str(video)],
                           capture_output=True, text=True, timeout=60)
        v = float(p.stdout.strip())
        return v if math.isfinite(v) and v >= 0 else None
    except (OSError, ValueError, subprocess.SubprocessError):
        return None


def package_episode(ep_dir, ep_id, out_zip, *, internal=False, video=None, title=None, series=None, number=None,
                    updated=None, deny_list=None, probe=True, repo_root=None):
    """편 폴더 → 꾸러미 zip (out_zip) → episode.json 내용 (dict).  거부 = BundleError (만들지 않는다).

    넣는 것 = 폴더 맨 위의 일반 파일 중 역할 있는 것 (role_of) · video = 폴더 밖 mp4 를 고를 때.
    공개판 (internal=False · Codex 11-25 AVI-02 · 1저자 11-25 Q1 · Q2 (가)) = INTERNAL 표지 이름 · internal 폴더 · id 거부 ·
      넣는 역할 = PUBLIC_ROLES (영상 · 썸네일 · 자막 · 시청자 대본 · 공개 장면 · 시간표) — script.md = viewer_script (장면 파일 +
      제작 대본의 참고 문헌 목록 줄 · 제작 대본 자체는 넣지 않는다) · scenes.json = public_scenes (투영) · 그 밖 역할 (제작 기록) = 뺌
      (episode.json `excluded` = 이름 · 역할 · 사유 · `derived` = 만든 두 파일의 원본 이름 · sha256) · 공개 안전 검사 통과 필수.
    내부판 (internal=True) = 모든 역할 · 파일 그대로 · 공개 안전 검사는 기록만 (지금과 같음).
    판 대조 (build_check · 둘 다 · Q4 P2-6 · 3 회차 P2-1 · P2-2) = 어긋나면 거부 · 공개판은 다섯을 다 재야 꾸린다 (MP4 = ffprobe 로 잰 길이만 ·
      못 재면 거부 · 사유 = 대조 이름) · 내부판은 못 잰 대조를 미측정으로 적는다 · 거부 차례 = 공개 안전 검사 → 판 대조.
    repo_root = 커밋 식별자를 대조할 저장소 (없으면 이 라이브러리가 든 리포 뿌리 · 시험이 임시 저장소를 줄 때)."""
    check_id(ep_id)
    ep_dir = Path(ep_dir)
    if not ep_dir.is_dir():
        raise BundleError(f'편 폴더가 없다 — {ep_dir.name}')
    picked, skipped = {}, []
    for p in sorted(ep_dir.iterdir(), key=lambda x: x.name):
        if p.is_symlink():
            skipped.append((p.name, '심볼릭 링크'))
            continue
        if not p.is_file():
            continue
        role = role_of(p.name)
        if role is None:
            skipped.append((p.name, '역할 밖'))
            continue
        if role == 'video' and video is not None:
            skipped.append((p.name, '--video 로 다른 영상을 골랐다'))
            continue
        picked.setdefault(role, []).append(p)
    if video is not None:
        vp = Path(video)
        if vp.is_symlink() or not vp.is_file() or role_of(vp.name) != 'video':
            raise BundleError(f'--video 가 mp4 일반 파일이 아니다 — {vp.name}')
        picked['video'] = [vp]
    for role, ps in picked.items():
        if len(ps) > ROLES[role]['max']:
            hint = ' — --video 로 하나를 고른다' if role == 'video' else ' — 하나만 남긴다'
            raise BundleError(f'{role} 역할 파일이 {len(ps)} 개 ({", ".join(x.name for x in ps)}){hint}')
    if 'video' not in picked:
        raise BundleError('mp4 가 없다 — 편 폴더에 넣거나 --video 로 고른다')
    names = [unicodedata.normalize('NFC', p.name) for ps in picked.values() for p in ps]
    marked = sorted({n for n in names if 'internal' in n.lower()}
                    | ({ep_dir.name} if 'internal' in ep_dir.name.lower() else set())
                    | ({ep_id} if 'internal' in ep_id else set()))
    if marked and not internal:
        raise BundleError(f'INTERNAL 표지 ({", ".join(marked)}) — 내부판이면 --internal 을 붙인다 (공개판으로 꾸리지 않는다)')
    bad = [n for n in names if not name_ok(n) or n in META_NAMES or n in LOCAL_NAMES]
    if bad:
        raise BundleError(f'꾸러미에 넣을 수 없는 이름 — {bad}')
    if len({n.casefold() for n in names}) != len(names):
        raise BundleError('대소문자만 다른 같은 이름이 있다')
    visibility = 'internal' if internal else 'public'
    # 글 파일 읽기 (UTF-8) · JSON 역할 파싱 — 역할마다 (이름, 바이트, 글, JSON)
    got = {}
    for role in ROLES:
        for p in picked.get(role, []):
            arc = unicodedata.normalize('NFC', p.name)
            size = p.stat().st_size
            limit = MAX_FILE_BYTES if role == 'video' else MAX_TEXT_BYTES
            if size > limit:
                raise BundleTooLarge(f'{arc} 가 상한 ({fmt_size(limit)}) 을 넘는다')
            if not ROLES[role]['text']:
                got[role] = dict(name=arc, path=p)
                continue
            raw = p.read_bytes()
            try:
                txt = raw.decode('utf-8-sig' if role == 'subtitles' else 'utf-8')
            except ValueError:
                raise BundleError(f'{arc} 가 UTF-8 글이 아니다')
            obj = None
            if ROLES[role]['ext'] == ('.json',):
                try:
                    obj = json.loads(txt)
                except ValueError as e:
                    raise BundleError(f'{arc} ({role}) 을 JSON 으로 읽지 못했다 ({type(e).__name__})')
            got[role] = dict(name=arc, path=p, raw=raw, txt=txt, obj=obj)
    scenes = got['scenes']['obj'] if 'scenes' in got and isinstance(got['scenes']['obj'], dict) else {}
    timeline = got['timeline']['obj'] if 'timeline' in got and isinstance(got['timeline']['obj'], dict) else {}
    if not internal and 'scenes' in got and not isinstance(got['scenes']['obj'], dict):
        raise BundleError('공개판은 scenes.json 이 JSON 객체여야 한다 — 시청자 대본 · 공개 장면을 거기서 만든다')
    # 머리 값
    the_title = title if title is not None else scenes.get('title')
    if not isinstance(the_title, str) or not the_title.strip():
        raise BundleError('제목이 없다 — scenes.json 의 title 또는 --title')
    the_series = series if series is not None else scenes.get('series')
    if not isinstance(the_series, str) or not the_series.strip():
        the_series = '(시리즈 없음)'
    sub = scenes.get('subtitle') if isinstance(scenes.get('subtitle'), str) else ''
    if number is None:
        m = re.match(r'ep(\d{1,4})', ep_id)
        number = int(m.group(1)) if m else None
    if number is not None and (not isinstance(number, int) or isinstance(number, bool) or number < 0):
        raise BundleError(f'편 번호가 0 이상 정수가 아니다 — {number!r}')
    # 꾸러미에 넣을 것 (역할 순서) — 공개판 = PUBLIC_ROLES 만 · 시청자 대본 · 공개 장면은 만든다 · 내부판 = 그대로
    items, derived, excluded, texts = [], [], [], []
    chapter_lead = None
    for role in ROLES:
        g = got.get(role)
        if not internal and role == 'script':
            if 'scenes' in got:
                vs = viewer_script(scenes, g['txt'] if g else None, title=the_title, subtitle=sub, series=the_series)
                raw = vs.encode('utf-8')
                d = dict(name='script.md', role='script', **{'from': got['scenes']['name']},
                         from_sha256=hashlib.sha256(got['scenes']['raw']).hexdigest(), method=VIEWER_SCRIPT)
                if g:
                    d.update(refs_from=g['name'], refs_from_sha256=hashlib.sha256(g['raw']).hexdigest())
                derived.append(d)
                items.append(dict(name='script.md', role='script', data=raw))
                texts.append(('script.md', vs))
            elif g:
                excluded.append(dict(name=g['name'], role='script',
                                     reason='장면 파일 (scenes.json) 이 없어 시청자 대본을 만들지 못했다 — 제작 대본은 공개판에 넣지 않는다'))
            continue
        if g is None:
            continue
        if not internal and role not in PUBLIC_ROLES:
            excluded.append(dict(name=g['name'], role=role, reason=PUBLIC_EXCLUDE_REASON))
            continue
        if 'raw' not in g:
            items.append(dict(name=g['name'], role=role, path=g['path']))
            continue
        arc, raw, txt = g['name'], g['raw'], g['txt']
        if not internal and role == 'scenes':
            proj, dropped = public_scenes(scenes)
            raw = (json.dumps(proj, ensure_ascii=False, indent=1) + '\n').encode('utf-8')
            txt = raw.decode('utf-8')
            derived.append(dict(name='scenes.json', role='scenes', **{'from': arc}, from_sha256=hashlib.sha256(g['raw']).hexdigest(),
                                dropped_keys=dropped, method=PUBLIC_SCENES))
            arc = 'scenes.json'
            vm = scenes.get('voice_model') if isinstance(scenes.get('voice_model'), dict) else {}
            if _finite(vm.get('lead_in')) and 0 <= vm['lead_in'] <= 30:
                chapter_lead = float(vm['lead_in'])         # 챕터 시각 = 첫 문장 − lead_in (투영에서 빠지는 값 · 화면 그대로)
        items.append(dict(name=arc, role=role, data=raw))
        texts.append((arc, txt))
    vid = next(x for x in items if x['role'] == 'video')
    dur, dsrc = None, None
    if probe:
        dur = _probe_duration(vid['path'])
        dsrc = 'ffprobe' if dur is not None else None
    if dur is None:
        dv = (timeline.get('summary') or {}).get('duration_s') if isinstance(timeline.get('summary'), dict) else None
        if _finite(dv) and dv >= 0:
            dur, dsrc = float(dv), 'timeline'
    #  판 대조 (Q4 P2-6 · 3 회차 P2-1 · P2-2 · 공개판 · 내부판 둘 다) — MP4 길이는 ffprobe 로 잰 값만 (시간표로 채운 길이로 시간표를
    #  대조하지 않는다) · 장면 파일 = 원본 (시청자 대본 · 공개 장면을 만드는 그 파일).  거부는 공개 안전 검사 뒤 (아래 — 걸린 글이 먼저 보인다)
    bc = build_check(dur if dsrc == 'ffprobe' else None, timeline, got['subtitles']['txt'] if 'subtitles' in got else None,
                     got['scenes']['obj'] if 'scenes' in got else None)
    upd = updated or _now_kst().date().isoformat()
    try:
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', upd):
            raise ValueError
        date.fromisoformat(upd)
    except ValueError:
        raise BundleError(f'갱신 날짜 꼴 (YYYY-MM-DD) 이 아니다 — {upd!r}')
    #  내부 숫자 목록 — --deny-list (arg) + 공개판이면 편 폴더 · 영상 폴더의 internal/<DENY_LIST_NAME> (auto · 늘 · 1저자 11-24 Q2).
    #  내부판은 자동 목록을 읽지 않는다 (지금과 같음).  episode.json 에는 목록마다 출처 · 개수 · sha256 만 (값 · 경로 없음).
    lists = ([('arg', Path(deny_list))] if deny_list else []) + ([] if internal else [('auto', p) for p in find_deny_lists(ep_dir, video)])
    deny, deny_meta = None, []
    if lists:
        lits, shas = [], []
        for src, p in lists:
            ls, sh = load_deny_list(p)
            lits += [x for x in ls if x not in lits]
            shas.append(sh)
            deny_meta.append(dict(source=src, n=len(ls), sha256=sh))
        deny = (lits, hashlib.sha256(' '.join(shas).encode('ascii')).hexdigest())
    files = []
    for it in items:
        if 'data' in it:
            files.append(dict(name=it['name'], role=it['role'], size=len(it['data']), sha256=hashlib.sha256(it['data']).hexdigest()))
        else:
            with open(it['path'], 'rb') as f:
                h, n = _sha_stream(f)
            files.append(dict(name=it['name'], role=it['role'], size=n, sha256=h))
    man = dict(schema=SCHEMA, id=ep_id, title=the_title.strip(), subtitle=sub.strip(), series=the_series.strip(), episode=number,
               visibility=visibility, duration_s=(round(dur, 3) if dur is not None else None), duration_source=dsrc,
               updated=upd, packaged_at=_now_kst().isoformat(timespec='seconds'), source=dict(folder=ep_dir.name),
               files=files, derived=derived, tool=dict(name='video_library.package_episode', schema=SCHEMA),
               build_check={k: v for k, v in bc.items() if k != 'problems'})
    if not internal:
        man['excluded'] = excluded
        if chapter_lead is not None:
            man['chapter_lead_s'] = chapter_lead
    pc = public_check(texts + [('episode.json', _head_text(man))], deny=deny, repo_root=repo_root)
    if pc.get('deny_list'):
        pc['deny_list']['lists'] = deny_meta
    man['public_check'] = pc
    if not internal and not pc['ok']:
        raise BundleError(f'공개 안전 검사 걸림 {len(pc["hits"])} 건 — {_hits_text(pc)} (공개판으로 꾸리지 않는다 · 값은 적지 않는다)')
    if bc['problems']:
        raise BundleError('영상 ↔ 시간표 ↔ 자막 ↔ 장면 파일 판이 다르다 — ' + ' · '.join(bc['problems'])
                          + ' (같은 빌드의 영상 · 시간표 · 자막 · 장면 파일로 꾸린다 · 리포의 옛 판 글에 새 MP4 를 붙이지 않는다)')
    if not internal and bc['not_measured']:
        raise BundleError('공개판인데 판 대조를 다 재지 못했다 — ' + ' · '.join(bc['not_measured'])
                          + ' (공개판은 ffprobe 로 잰 MP4 길이 · 시간표 · 자막 · 장면 파일이 다 있어야 꾸린다 · '
                            '--no-probe 와 미측정 기록은 검토 후보 (--internal) 만)')
    check_manifest(man)
    out = Path(out_zip)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_name(f'.{out.name}.part')
    mb = (json.dumps(man, ensure_ascii=False, indent=1) + '\n').encode('utf-8')
    sums = [f'{hashlib.sha256(mb).hexdigest()}  episode.json'] + [f"{f['sha256']}  {f['name']}" for f in files]
    stamp = _now_kst().timetuple()[:6]

    def _zi(name, compress):
        zi = zipfile.ZipInfo(name, date_time=stamp)
        zi.create_system = 3
        zi.external_attr = (0o100644 << 16)
        zi.compress_type = compress
        return zi
    try:
        with zipfile.ZipFile(tmp, 'w') as z:
            z.writestr(_zi('episode.json', zipfile.ZIP_DEFLATED), mb)
            for it in items:
                if 'data' in it:
                    z.writestr(_zi(it['name'], zipfile.ZIP_DEFLATED), it['data'])
                else:
                    with open(it['path'], 'rb') as src, z.open(_zi(it['name'], zipfile.ZIP_STORED), 'w', force_zip64=True) as dst:
                        shutil.copyfileobj(src, dst, 1024 * 1024)
            z.writestr(_zi('SHA256SUMS', zipfile.ZIP_DEFLATED), '\n'.join(sums) + '\n')
        os.replace(tmp, out)
    finally:
        if tmp.exists():
            tmp.unlink()
    man['_skipped'] = skipped                       # 명령 출력용 (episode.json 에는 없다)
    return man


# ─────────────────────────────  episode.json 검사  ─────────────────────────────

def _head_text(man):
    """episode.json 에서 공개 안전 검사에 넣는 글 — 머리 (id · 제목 · 부제 · 시리즈) · 원본 폴더 이름 · 파일 이름 · 뺀 파일 (이름 · 역할 ·
    사유) · 만든 파일 (이름 · 원본 이름 · 만든 법).  꾸러미 · 등록 · 화면이 같은 글을 본다."""
    src = man.get('source') if isinstance(man.get('source'), dict) else {}
    keep = {k: man.get(k) for k in ('id', 'title', 'subtitle', 'series')}
    keep['source'] = src.get('folder')
    keep['files'] = [f.get('name') for f in man.get('files') or [] if isinstance(f, dict)]
    keep['excluded'] = [{k: e.get(k) for k in ('name', 'role', 'reason')} for e in man.get('excluded') or [] if isinstance(e, dict)]
    keep['derived'] = [{k: d.get(k) for k in ('name', 'from', 'refs_from', 'method')} for d in man.get('derived') or []
                       if isinstance(d, dict)]
    return json.dumps(keep, ensure_ascii=False)


def check_manifest(man):
    """episode.json 내용 검사 — 어긋나면 BundleError (무엇이 왜)."""
    if not isinstance(man, dict):
        raise BundleError('episode.json 이 객체가 아니다')
    if man.get('schema') != SCHEMA:
        raise BundleError(f'모르는 스키마 ({str(man.get("schema"))[:40]}) — {SCHEMA} 만 읽는다')
    check_id(man.get('id'))
    for k, lim in (('title', 300), ('series', 200)):
        v = man.get(k)
        if not isinstance(v, str) or not v.strip() or len(v) > lim:
            raise BundleError(f'episode.json 의 {k} 가 없거나 너무 길다')
    if not isinstance(man.get('subtitle', ''), str) or len(man.get('subtitle', '')) > 300:
        raise BundleError('episode.json 의 subtitle 꼴')
    ep = man.get('episode')
    if ep is not None and (not isinstance(ep, int) or isinstance(ep, bool) or not 0 <= ep < 10000):
        raise BundleError('episode.json 의 편 번호 (episode) 꼴')
    if man.get('visibility') not in ('public', 'internal'):
        raise BundleError(f'공개 범위 (visibility) 가 public · internal 이 아니다 — {str(man.get("visibility"))[:20]}')
    d = man.get('duration_s')
    if d is not None and (not _finite(d) or not 0 <= d < 1e6):
        raise BundleError('episode.json 의 길이 (duration_s) 꼴')
    upd = man.get('updated')
    try:
        if not isinstance(upd, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', upd):
            raise ValueError
        date.fromisoformat(upd)
    except ValueError:
        raise BundleError('episode.json 의 갱신 날짜 (updated) 꼴')
    files = man.get('files')
    if not isinstance(files, list) or not files:
        raise BundleError('episode.json 의 파일 목록 (files) 이 없다')
    seen, count = set(), {}
    for f in files:
        if not isinstance(f, dict):
            raise BundleError('파일 목록 항목이 객체가 아니다')
        n, role = f.get('name'), f.get('role')
        if not name_ok(n) or n in META_NAMES or n in LOCAL_NAMES:
            raise BundleError(f'파일 이름 꼴 — {str(n)[:80]!r}')
        if role not in ROLES:
            raise BundleError(f'모르는 역할 — {str(role)[:20]}')
        if not n.lower().endswith(ROLES[role]['ext']):
            raise BundleError(f'{n} 의 이름 끝이 역할 {role} 과 맞지 않는다')
        if n.casefold() in seen:
            raise BundleError(f'파일 목록에 같은 이름 두 번 — {n}')
        seen.add(n.casefold())
        if not isinstance(f.get('size'), int) or isinstance(f.get('size'), bool) or f['size'] < 0:
            raise BundleError(f'{n} 의 크기 꼴')
        if not isinstance(f.get('sha256'), str) or not re.fullmatch(r'[0-9a-f]{64}', f['sha256']):
            raise BundleError(f'{n} 의 sha256 꼴')
        count[role] = count.get(role, 0) + 1
        if count[role] > ROLES[role]['max']:
            raise BundleError(f'역할 {role} 파일이 둘 이상')
    if count.get('video') != 1:
        raise BundleError('영상 (video) 이 정확히 하나여야 한다')
    pc = man.get('public_check')
    if pc is not None and not isinstance(pc, dict):
        raise BundleError('episode.json 의 public_check 꼴')
    if man['visibility'] == 'public' and not (isinstance(pc, dict) and pc.get('ok') is True):
        raise BundleError('공개판인데 꾸러미의 공개 안전 검사 기록이 통과가 아니다')
    if not isinstance(man.get('derived', []), list):
        raise BundleError('episode.json 의 derived 꼴')
    exc = man.get('excluded', [])
    if not isinstance(exc, list) or not all(
            isinstance(e, dict) and name_ok(e.get('name')) and e.get('role') in ROLES
            and isinstance(e.get('reason'), str) and 0 < len(e['reason']) <= 300 for e in exc):
        raise BundleError('episode.json 의 excluded 꼴 (뺀 파일마다 이름 · 역할 · 사유)')
    lead = man.get('chapter_lead_s')
    if lead is not None and (not _finite(lead) or not 0 <= lead <= 30):
        raise BundleError('episode.json 의 chapter_lead_s 꼴 (0–30 초)')
    bc = man.get('build_check')
    if bc is not None and not (isinstance(bc, dict) and bc.get('ok') is True):
        raise BundleError('episode.json 의 build_check 꼴 (판 대조 기록이 통과가 아니다)')
    if isinstance(bc, dict) and 'not_measured' in bc and not (
            isinstance(bc['not_measured'], list) and len(bc['not_measured']) <= len(BUILD_CMP)
            and all(isinstance(x, str) and 0 < len(x) <= 80 for x in bc['not_measured'])):
        raise BundleError('episode.json 의 build_check 꼴 (미측정 목록)')
    return man


def _parse_sums(txt):
    out = {}
    for ln in txt.splitlines():
        if not ln.strip():
            continue
        m = re.fullmatch(r'([0-9a-f]{64})  (.+)', ln)
        if not m:
            raise BundleError('SHA256SUMS 줄 꼴 (sha256 두 칸 이름)')
        if m.group(2) in out:
            raise BundleError(f'SHA256SUMS 에 같은 이름 두 번 — {m.group(2)}')
        out[m.group(2)] = m.group(1)
    return out


# ─────────────────────────────  등록  ─────────────────────────────

def _caps(caps):
    c = dict(max_bundle=MAX_BUNDLE_BYTES, max_file=MAX_FILE_BYTES, max_text=MAX_TEXT_BYTES, max_total=MAX_TOTAL_BYTES,
             max_entries=MAX_ENTRIES)
    c.update(caps or {})
    return c


@contextlib.contextmanager
def _lock(folder):
    if fcntl is None:
        yield
        return
    fd = os.open(os.path.join(folder, '.lock'), os.O_CREAT | os.O_RDWR, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        try:
            fcntl.flock(fd, fcntl.LOCK_UN)
        finally:
            os.close(fd)


def _check_zip(z, caps):
    """열린 zip → (episode.json dict, {이름: sha256}) · 어긋나면 BundleError.  폴더에 아무것도 쓰지 않는다."""
    infos = z.infolist()
    if len(infos) > caps['max_entries']:
        raise BundleError(f'항목이 {len(infos)} 개 — 상한 {caps["max_entries"]}')
    names, seen = [], set()
    for zi in infos:
        n = zi.filename
        if n.endswith('/') or zi.is_dir():
            raise BundleError(f'폴더 항목 {n[:80]!r} — 꾸러미는 납작해야 한다')
        if not name_ok(n):
            raise BundleError(f'이름 꼴 {n[:80]!r} — 경로 · 구분자 · 점으로 시작 · 제어 문자 금지 (zip-slip 막음)')
        mode = (zi.external_attr >> 16) & 0o170000
        if zi.create_system == 3 and mode not in (0, 0o100000):
            raise BundleError(f'{n} 가 일반 파일이 아니다 (심볼릭 링크 등)')
        if zi.flag_bits & 0x1:
            raise BundleError(f'{n} 가 암호 항목이다')
        if zi.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED):
            raise BundleError(f'{n} 의 압축 방식이 STORED · DEFLATED 가 아니다')
        if n.casefold() in seen:
            raise BundleError(f'같은 이름 두 번 — {n}')
        seen.add(n.casefold())
        names.append(n)
    for meta in META_NAMES:
        if meta not in names:
            raise BundleError(f'{meta} 가 없다 — avi_package_episode.py 로 만든 꾸러미가 아니다')
    total = 0
    for zi in infos:
        limit = caps['max_file'] if zi.filename.lower().endswith('.mp4') else caps['max_text']
        if zi.file_size > limit:
            raise BundleTooLarge(f'{zi.filename} 가 상한 ({fmt_size(limit)}) 을 넘는다')
        total += zi.file_size
    if total > caps['max_total']:
        raise BundleTooLarge(f'풀면 {fmt_size(total)} — 상한 {fmt_size(caps["max_total"])}')

    def _read_small(name):
        with z.open(name) as f:
            b = f.read(caps['max_text'] + 1)
        if len(b) > caps['max_text']:
            raise BundleTooLarge(f'{name} 가 너무 크다')
        return b
    try:
        mb = _read_small('episode.json')
        man = json.loads(mb.decode('utf-8'))
    except BundleError:
        raise
    except (ValueError, zipfile.BadZipFile, OSError) as e:
        raise BundleError(f'episode.json 을 읽지 못했다 ({type(e).__name__})')
    check_manifest(man)
    try:
        sums = _parse_sums(_read_small('SHA256SUMS').decode('utf-8'))
    except BundleError:
        raise
    except (ValueError, zipfile.BadZipFile, OSError) as e:
        raise BundleError(f'SHA256SUMS 를 읽지 못했다 ({type(e).__name__})')
    data = set(names) - set(META_NAMES)
    listed = {f['name'] for f in man['files']}
    if data != listed:
        extra, miss = sorted(data - listed), sorted(listed - data)
        raise BundleError(f'episode.json 파일 목록 ↔ zip 항목이 다르다 (목록 밖 {extra[:3]} · 없는 것 {miss[:3]})')
    if set(sums) != set(names) - {'SHA256SUMS'}:
        raise BundleError('SHA256SUMS 가 항목 전부 (SHA256SUMS 자신 빼고) 를 정확히 한 번씩 적지 않는다')
    by_name = {f['name']: f for f in man['files']}
    for zi in infos:
        n = zi.filename
        if n == 'SHA256SUMS':
            continue
        limit = caps['max_file'] if n.lower().endswith('.mp4') else caps['max_text']
        try:
            with z.open(zi) as f:
                h, size = _sha_stream(f, limit)
        except (zipfile.BadZipFile, OSError, EOFError) as e:
            raise BundleError(f'{n} 를 풀지 못했다 ({type(e).__name__})')
        if h != sums[n]:
            raise BundleError(f'{n} 의 sha256 이 SHA256SUMS 와 다르다')
        if n in by_name and (h != by_name[n]['sha256'] or size != by_name[n]['size']):
            raise BundleError(f'{n} 의 sha256 · 크기가 episode.json 과 다르다')
    if man['visibility'] == 'public':
        marked = sorted(n for n in data if 'internal' in n.lower()) + (['id'] if 'internal' in man['id'] else [])
        if marked:
            raise BundleError(f'공개판인데 INTERNAL 표지 이름 ({", ".join(marked)}) — 내부판이면 --internal 로 다시 꾸린다')
    texts = []
    for f in man['files']:
        if ROLES[f['role']]['text']:
            try:
                texts.append((f['name'], _read_small(f['name']).decode('utf-8-sig' if f['role'] == 'subtitles' else 'utf-8')))
            except ValueError:
                raise BundleError(f"{f['name']} 가 UTF-8 글이 아니다")
    if man['visibility'] == 'public':
        #  공개판 = 꾸러미 도구와 같은 기준 (Codex 11-25 AVI-02) — 제작 기록 역할 없음 · 장면 파일 = 공개 투영 꼴
        extra = sorted({f['role'] for f in man['files']} - set(PUBLIC_ROLES))
        if extra:
            raise BundleError(f'공개판 꾸러미에 제작 기록 역할 ({", ".join(extra)}) 이 있다 — 공개판은 영상 · 썸네일 · 자막 · 시청자 대본 · '
                              '공개 장면 · 시간표만 (avi_package_episode.py 로 다시 꾸린다)')
        roles_by = {f['name']: f['role'] for f in man['files']}
        for n, t in texts:
            if roles_by.get(n) != 'scenes':
                continue
            try:
                obj = json.loads(t)
            except ValueError:
                raise BundleError(f'{n} (scenes) 을 JSON 으로 읽지 못했다')
            left = public_scenes(obj)[1] if isinstance(obj, dict) else ['(객체 아님)']
            if left:
                raise BundleError(f'공개판 장면 파일 ({n}) 이 공개 투영 꼴이 아니다 (제작 칸 {len(left)} 종) — avi_package_episode.py 로 다시 꾸린다')
        #  판 대조 기록 (Q4 3 회차 N10) — 지금 판 · 다 잰 통과여야 (없음 = 옛 도구 · 손 꾸러미 · --no-probe = 공개판으로 등록하지 않는다)
        if not build_record_ok(man.get('build_check')):
            raise BundleError('공개판인데 꾸러미에 판 대조 기록 (build_check · 지금 판 · 다 잰 통과) 이 없다 — 같은 빌드의 편 폴더에서 '
                              'avi_package_episode.py 로 다시 꾸린다 (옛 도구 · 손 꾸러미 · --no-probe 꾸러미는 공개판으로 등록하지 않는다)')
    pc = public_check(texts + [('episode.json', _head_text(man))])
    if man['visibility'] == 'public' and not pc['ok']:
        raise BundleError(f'공개 안전 검사 걸림 {len(pc["hits"])} 건 — {_hits_text(pc)} (공개판으로 등록하지 않는다)')
    return man, sums


def register_bundle(source, folder, *, replace=False, via='cli', caps=None):
    """꾸러미 (경로 또는 바이너리 파일 객체) → <folder>/<id>/ 등록 → dict(id, path, replaced_to, bundle_sha256, manifest).

    검사를 다 지난 뒤에만 폴더에 쓴다 (거부 = 폴더 그대로).  이미 있으면 BundleExists · replace=True 면 옛 판을 .replaced/ 로."""
    if via not in ('cli', 'web'):
        raise BundleError('via 는 cli · web')
    c = _caps(caps)
    own = None
    if isinstance(source, (str, os.PathLike)):
        sp = Path(source)
        if sp.is_symlink() or not sp.is_file():
            raise BundleError(f'꾸러미 파일이 없다 — {sp.name}')
        fh = own = open(sp, 'rb')
    else:
        fh = source
    try:
        fh.seek(0, 2)
        size = fh.tell()
        fh.seek(0)
        if size > c['max_bundle']:
            raise BundleTooLarge(f'꾸러미 {fmt_size(size)} — 상한 {fmt_size(c["max_bundle"])}')
        bsha = _sha_stream(fh)[0]
        fh.seek(0)
        try:
            z = zipfile.ZipFile(fh)
        except (zipfile.BadZipFile, OSError, ValueError) as e:
            raise BundleError(f'zip 이 아니다 ({type(e).__name__})')
        with z:
            man, sums = _check_zip(z, c)
            ep_id = man['id']
            folder = Path(folder)
            folder.mkdir(parents=True, exist_ok=True)
            with _lock(str(folder)):
                dst = folder / ep_id
                exists = dst.exists() or dst.is_symlink()
                if exists and not replace:
                    raise BundleExists(f'이미 있는 편 — {ep_id} (바꾸려면 명시: 명령 --replace · 화면 "바꾸기")')
                stage = Path(tempfile.mkdtemp(prefix='.incoming-', dir=str(folder)))
                replaced_to = None
                try:
                    epd = stage / ep_id
                    epd.mkdir()
                    for zi in z.infolist():
                        limit = c['max_file'] if zi.filename.lower().endswith('.mp4') else c['max_text']
                        h, n = hashlib.sha256(), 0
                        with z.open(zi) as src, open(epd / zi.filename, 'xb') as out:
                            while True:
                                b = src.read(1024 * 1024)
                                if not b:
                                    break
                                n += len(b)
                                if n > limit:
                                    raise BundleTooLarge(f'{zi.filename} 가 풀면서 상한을 넘었다')
                                h.update(b)
                                out.write(b)
                        if zi.filename != 'SHA256SUMS' and h.hexdigest() != sums[zi.filename]:
                            raise BundleError(f'{zi.filename} 가 풀면서 sha256 이 달라졌다')
                    reg = dict(schema=REG_SCHEMA, id=ep_id, registered_at=_now_kst().isoformat(timespec='seconds'), via=via,
                               bundle_sha256=bsha, bundle_size=size, replaced=bool(exists))
                    (epd / 'registration.json').write_text(json.dumps(reg, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
                    if exists:
                        keep = folder / '.replaced'
                        keep.mkdir(exist_ok=True)
                        tag = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
                        replaced_to = keep / f'{ep_id}__{tag}'
                        os.replace(dst, replaced_to)
                    os.replace(epd, dst)
                finally:
                    shutil.rmtree(stage, ignore_errors=True)
    finally:
        if own is not None:
            own.close()
    return dict(id=ep_id, path=str(dst), replaced_to=(str(replaced_to) if replaced_to else None), bundle_sha256=bsha,
                manifest=man)


def register_dir(ep_dir, folder, *, ep_id, replace=False, via='cli', **pkg_kw):
    """편 폴더를 바로 등록 — package_episode 로 임시 꾸러미를 만들어 register_bundle (같은 함수 · 같은 검사)."""
    with tempfile.TemporaryDirectory(prefix='avi_pkg_') as td:
        out = Path(td) / f'{check_id(ep_id)}.zip'
        package_episode(ep_dir, ep_id, out, **pkg_kw)
        return register_bundle(out, folder, replace=replace, via=via)


# ─────────────────────────────  지우기 (보관 폴더로 옮김 · 1저자 11-25)  ─────────────────────────────

def delete_episode(folder, ep_id, *, via='cli'):
    """등록된 편 지우기 → dict(id, moved_to, record, restore_to, state).  ⚠ 영구 삭제가 아니다 — 편 폴더를 <folder>/.deleted/<id>__<UTC 시각>/
    로 옮기고 (os.replace 한 번 · 파일 · 바이트 그대로 · .replaced/ 보관과 같은 정신) 그 옆에 작은 기록 <id>__<UTC 시각>.json (무엇 · 언제 ·
    어떤 길 = cli · web) 을 남긴다.  되돌리기 = 그 폴더를 <folder>/<id>/ 로 손으로 옮긴다 (같은 id 편이 없을 때 · 기록은 역사로 남는다).

    명령 (scripts/avi_register_episode.py --delete) · 화면 (POST /videos/<id>/delete) 이 이 함수를 부른다 · 등록 (register_bundle) 과 같은 잠금.
    거부 = BundleError · 폴더 그대로: via 꼴 · 편 id 꼴 (check_id — 경로 · 구분자 · 빈 값 · 점 이름 · 예약어 upload) · 영상 폴더 · 편 폴더가
    없음 (EpisodeMissing · 404 · 폴더를 만들지 않는다) · 편 폴더가 심볼릭 링크 · 보관 자리 (.deleted) 가 폴더가 아님 (심볼릭 링크 · 파일 —
    링크 너머에 쓰지 않는다) · 같은 이름 보관본이 이미 있음.  옮긴 뒤 목록 (library) 에서 그 편만 빠진다 (점으로 시작하는 폴더는 읽지 않는다) —
    다른 편 · 깨진 편 안내 그대로 · 같은 id 를 다시 등록할 수 있다 (--replace 없이).  깨진 편 (목록에서 뺀 편) 도 옮긴다 (기록 state broken · 사유)."""
    if via not in ('cli', 'web'):
        raise BundleError('via 는 cli · web')
    check_id(ep_id)
    root = Path(folder)
    src = root / ep_id
    keep = root / DELETED_DIR

    def _target():
        if not root.is_dir():
            raise EpisodeMissing(f'없는 편 — {ep_id} (영상 폴더가 없다)')
        if src.is_symlink():
            raise BundleError(f'편 폴더가 심볼릭 링크다 — {ep_id} (옮기지 않는다 · 링크 · 대상은 손으로 정리한다)')
        if not src.is_dir():
            raise EpisodeMissing(f'없는 편 — {ep_id}')
    _target()                                       # 잠그기 전에 한 번 — 거부면 .lock 도 만들지 않는다 (폴더 그대로)
    with _lock(str(root)):
        _target()                                   # 잠근 뒤 다시 — 같은 때의 올리기 · 지우기와 엇갈리지 않게
        if keep.is_symlink() or (keep.exists() and not keep.is_dir()):
            raise BundleError(f'보관 자리 ({DELETED_DIR}) 가 폴더가 아니다 (심볼릭 링크 · 파일) — 고친 뒤 지운다 (fail-closed · 옮기지 않았다)')
        ep, why = load_episode(src)
        man = (ep or {}).get('man') or {}
        reg = (ep or {}).get('reg') or {}
        vid = next((f for f in man.get('files') or [] if isinstance(f, dict) and f.get('role') == 'video'), None)
        name = f"{ep_id}__{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')}"
        dst, rec_p, tmp = keep / name, keep / f'{name}.json', keep / f'.{name}.json.part'
        if any(p.exists() or p.is_symlink() for p in (dst, rec_p, tmp)):
            raise BundleError('같은 이름 보관본이 이미 있다 — 다시 지운다 (옮기지 않았다)')
        rec = dict(schema=DEL_SCHEMA, id=ep_id, deleted_at=_now_kst().isoformat(timespec='seconds'), via=via,
                   moved_to=f'{DELETED_DIR}/{name}', state=('ok' if ep else 'broken'))
        if ep:
            rec.update(visibility=man.get('visibility'), title=man.get('title'), series=man.get('series'), episode=man.get('episode'),
                       video=(dict(name=vid.get('name'), sha256=vid.get('sha256')) if vid else None), files=len(man.get('files') or []),
                       sums_sha256=ep.get('sums_sha'), bundle_sha256=reg.get('bundle_sha256'), registered_at=reg.get('registered_at'),
                       registered_via=reg.get('via'))
        else:
            rec.update(why=why, visibility=_peek_visibility(src))
        rec['restore'] = f'되돌리기 = 이 폴더를 <영상 폴더>/{ep_id}/ 로 손으로 옮긴다 (같은 id 편이 없을 때)'
        made_keep = not keep.exists()
        keep.mkdir(exist_ok=True)
        try:
            #  기록을 먼저 제 이름으로 (임시 → 이름 바꾸기) · 그다음 편 폴더를 한 번에 옮긴다 — 옮긴 뒤에는 실패할 일이 남지 않는다
            tmp.write_text(json.dumps(rec, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
            os.replace(tmp, rec_p)
            os.replace(src, dst)
        except OSError as e:
            for p in (tmp, rec_p):
                with contextlib.suppress(OSError):
                    p.unlink()
            if made_keep:
                with contextlib.suppress(OSError):
                    keep.rmdir()
            raise BundleError(f'편 폴더를 옮기지 못했다 ({type(e).__name__}) — 폴더 그대로')
    for k in [k for k in _HELD_CACHE if k[0] == str(src)]:
        _HELD_CACHE.pop(k, None)                   # 공개 보류 캐시 — 이 편 자리 열쇠는 비운다 (같은 id 를 다시 올리면 새로 잰다)
    return dict(id=ep_id, moved_to=str(dst), record=str(rec_p), restore_to=str(src), state=rec['state'])


# ─────────────────────────────  읽기 (화면)  ─────────────────────────────

def load_episode(epdir, deep_media=False):
    """등록 폴더의 편 하나 → (dict(man, dir, reg, reg_note, sums_sha), '') 또는 (None, 무엇이 깨졌나).

    글 · 그림 파일은 늘 sha256 대조 (캐시) · 영상은 deep_media 일 때만 (화면 · 파일 요청에서)."""
    epdir = Path(epdir)
    name = epdir.name
    if not ID_RE.fullmatch(name) or name in RESERVED_IDS:
        return None, '폴더 이름이 편 id 꼴이 아니다'
    if epdir.is_symlink():
        return None, '편 폴더가 심볼릭 링크다'
    mp = epdir / 'episode.json'
    if mp.is_symlink():
        return None, 'episode.json 이 심볼릭 링크다'
    try:
        mb = mp.read_bytes()
        if len(mb) > MAX_TEXT_BYTES:
            return None, 'episode.json 이 너무 크다'
        man = json.loads(mb.decode('utf-8'))
    except FileNotFoundError:
        return None, 'episode.json 이 없다'
    except (OSError, ValueError) as e:
        return None, f'episode.json 을 읽지 못했다 ({type(e).__name__})'
    try:
        check_manifest(man)
    except BundleError as e:
        return None, str(e)
    if man['id'] != name:
        return None, f'폴더 이름 ({name}) 이 episode.json 의 id ({man["id"]}) 와 다르다'
    sp = epdir / 'SHA256SUMS'
    try:
        if sp.is_symlink():
            return None, 'SHA256SUMS 가 심볼릭 링크다'
        sb = sp.read_bytes()
        sums = _parse_sums(sb.decode('utf-8'))
    except FileNotFoundError:
        return None, 'SHA256SUMS 가 없다'
    except BundleError as e:
        return None, str(e)
    except (OSError, ValueError) as e:
        return None, f'SHA256SUMS 를 읽지 못했다 ({type(e).__name__})'
    want = {'episode.json'} | {f['name'] for f in man['files']}
    if set(sums) != want:
        return None, 'SHA256SUMS 의 이름들이 episode.json 파일 목록과 다르다'
    if hashlib.sha256(mb).hexdigest() != sums['episode.json']:
        return None, 'episode.json 의 sha256 이 SHA256SUMS 와 다르다 (등록 뒤 바뀜)'
    for f in man['files']:
        fp = epdir / f['name']
        if fp.is_symlink():
            return None, f"{f['name']} 가 심볼릭 링크다"
        try:
            st = os.stat(fp)
        except FileNotFoundError:
            return None, f"{f['name']} 파일이 없다"
        except OSError as e:
            return None, f"{f['name']} 를 읽지 못했다 ({type(e).__name__})"
        if not os.path.isfile(fp):
            return None, f"{f['name']} 가 일반 파일이 아니다"
        if st.st_size != f['size']:
            return None, f"{f['name']} 의 크기가 episode.json 과 다르다 (등록 뒤 바뀜)"
        if sums[f['name']] != f['sha256']:
            return None, f"{f['name']} 의 sha256 이 SHA256SUMS 와 episode.json 에서 다르다"
        if f['role'] != 'video' or deep_media:
            try:
                h = _file_sha(fp, st)
            except OSError as e:
                return None, f"{f['name']} 를 읽지 못했다 ({type(e).__name__})"
            if h != f['sha256']:
                return None, f"{f['name']} 의 sha256 이 다르다 (등록 뒤 바뀜)"
    reg, reg_note = None, ''
    rp = epdir / 'registration.json'
    if rp.is_file() and not rp.is_symlink():
        try:
            reg = json.loads(rp.read_text(encoding='utf-8'))
            if not isinstance(reg, dict):
                reg, reg_note = None, '등록 기록 (registration.json) 꼴이 다르다'
        except (OSError, ValueError):
            reg_note = '등록 기록 (registration.json) 을 읽지 못했다'
    else:
        reg_note = '등록 기록 (registration.json) 이 없다'
    return dict(man=man, dir=epdir, reg=reg, reg_note=reg_note, sums_sha=hashlib.sha256(sb).hexdigest()), ''


def _peek_visibility(epdir):
    """깨진 편의 공개 범위 어림 — episode.json 이 객체로 읽히고 visibility 가 public · internal 이면 그 값 · 아니면 None (모름).
    다른 컴퓨터의 화면은 public 으로 확인된 깨진 편만 안내한다 (모름 · internal = 안 보임 — 내부판이 있다는 사실을 흘리지 않는다)."""
    try:
        mp = Path(epdir) / 'episode.json'
        if mp.is_symlink() or not mp.is_file() or mp.stat().st_size > MAX_TEXT_BYTES:
            return None
        man = json.loads(mp.read_bytes().decode('utf-8'))
        v = man.get('visibility') if isinstance(man, dict) else None
        return v if v in ('public', 'internal') else None
    except (OSError, ValueError):
        return None


#: 공개 보류 판정 캐시 — (편 폴더, SHA256SUMS sha256) → (때, 까닭, 공개 검사).  재생 중 Range 요청마다 글을 다시 재지 않게 · 등록부
#: 철회값 · 리포 커밋이 바뀌면 HELD_TTL_S 안에 따라간다 (편을 바꿔 등록하면 SHA256SUMS 가 바뀌어 바로 새로 잰다).
_HELD_CACHE = {}
HELD_TTL_S = 30.0
#: 캐시 시계 (초 · 단조) — 시험이 바꿔 끼운다 (TTL 시험 · K10f).
_clock = time.monotonic


def public_problems(ep):
    """등록된 편 → (공개 보류 까닭 [str], 지금 공개 안전 검사 dict).  까닭이 하나라도 있는 **공개판** = 공개 보류 (Q4 P1-2 · fail-closed):
    다른 컴퓨터에는 등록 안 된 편과 같다 · 이 컴퓨터에는 빨간 배지 + 까닭.  까닭 = 지금 공개 안전 검사 걸림 (규칙 · 파일 · 줄만 — 값 없음) ·
    공개판에 넣지 않는 역할 (제작 기록) · 공개 투영이 아닌 장면 파일 · 판 대조 기록이 없거나 다 재지 않음 (build_record_ok · 등록과 같은 함수).
    내부판 = 까닭 없음 (검사는 화면 기록용으로만 잰다)."""
    m = ep['man']
    key = (str(ep['dir']), ep.get('sums_sha'))
    t = _clock()
    hit = _HELD_CACHE.get(key)
    if hit and t - hit[0] < HELD_TTL_S:
        return list(hit[1]), hit[2]
    texts = [(f['name'], _text(ep, f['role']) or '') for f in m['files'] if ROLES[f['role']]['text']]
    pc = public_check(texts + [('episode.json', _head_text(m))])
    why = []
    if m.get('visibility') == 'public':
        if not pc['ok']:
            why.append(f'공개 안전 검사 걸림 {len(pc["hits"])} 건 — {_hits_text(pc)}')
        extra = sorted({f['role'] for f in m['files']} - set(PUBLIC_ROLES))
        if extra:
            why.append(f'공개판에 넣지 않는 역할 ({", ".join(extra)}) — 제작 기록')
        for f in m['files']:
            if f['role'] == 'scenes':
                obj = _json(ep, 'scenes')
                if not isinstance(obj, dict) or public_scenes(obj)[1]:
                    why.append(f"장면 파일 ({f['name']}) 이 공개 투영 꼴이 아니다")
        if not build_record_ok(m.get('build_check')):
            why.append('판 대조 기록 (build_check) 이 없거나 다 재지 않았다 — 같은 빌드인지 확인 안 된 공개판')
    if len(_HELD_CACHE) > 256:
        _HELD_CACHE.clear()
    _HELD_CACHE[key] = (t, why, pc)
    return list(why), pc


def library(folder):
    """영상 폴더 → dict(state ok|missing|unreadable, episodes=[편 dict], problems=[dict(ep, why, vis)]).  GET 은 폴더를 만들지 않는다.

    problems 의 vis = 그 편의 공개 범위 어림 (_peek_visibility · 폴더 자체 문제는 public — 편 이름이 아니다)."""
    out = dict(state='ok', episodes=[], problems=[])
    p = Path(folder)
    if not p.exists():
        out['state'] = 'missing'
        return out
    if not p.is_dir():
        out['state'] = 'unreadable'
        out['problems'].append(dict(ep='(영상 폴더)', why='영상 폴더 자리가 폴더가 아니다', vis='public'))
        return out
    try:
        ents = sorted(os.scandir(p), key=lambda e: e.name)
    except OSError as e:
        out['state'] = 'unreadable'
        out['problems'].append(dict(ep='(영상 폴더)', why=f'영상 폴더를 읽지 못했다 ({type(e).__name__})', vis='public'))
        return out
    for e in ents:
        if e.name.startswith('.'):
            continue
        if e.is_symlink():
            out['problems'].append(dict(ep=e.name, why='편 폴더가 심볼릭 링크다', vis=None))
            continue
        if not e.is_dir():
            continue
        ep, why = load_episode(p / e.name)
        if ep is None:
            out['problems'].append(dict(ep=e.name, why=why, vis=_peek_visibility(p / e.name)))
        else:
            out['episodes'].append(ep)
    #  순서 = 공개판 먼저 (첫 화면 /videos 가 내부판을 열지 않게 — 11-24 실제 화면에서 내부판 시리즈 이름이 앞서 정렬돼 첫 편이 됐다) ·
    #  시리즈 · 편 번호 · id
    out['episodes'].sort(key=lambda x: (x['man']['visibility'] != 'public', x['man']['series'],
                                         x['man']['episode'] if x['man']['episode'] is not None else 10 ** 6, x['man']['id']))
    return out


def _file(ep, role):
    return next((f for f in ep['man']['files'] if f['role'] == role), None)


def _text(ep, role):
    f = _file(ep, role)
    if f is None:
        return None
    try:
        return (ep['dir'] / f['name']).read_bytes().decode('utf-8-sig' if role == 'subtitles' else 'utf-8')
    except (OSError, ValueError):
        return None


def _json(ep, role):
    t = _text(ep, role)
    if t is None:
        return None
    try:
        return json.loads(t)
    except ValueError:
        return None


def resolve_file(folder, ep_id, role, mode, include_internal=True):
    """파일 주소 → (절대 경로, 파일 항목, MIME) 또는 None (404).  등록된 편 · 그 편에 있는 역할 · 그 쓰임 (inline · download) 만.

    include_internal=False (이 컴퓨터가 아닌 요청 · 1저자 11-24 Q1) = 내부판 편은 등록 안 된 편과 같다 (None → 같은 404)."""
    if not isinstance(ep_id, str) or not ID_RE.fullmatch(ep_id) or ep_id in RESERVED_IDS or role not in ROLES:
        return None
    if mode not in ('inline', 'download', 'vtt') or (mode != 'vtt' and not ROLES[role][mode]):
        return None
    if mode == 'vtt' and role != 'subtitles':
        return None
    ep, _why = load_episode(Path(folder) / ep_id)
    if ep is None:
        return None
    if not include_internal and (ep['man']['visibility'] != 'public' or public_problems(ep)[0]):
        return None                    # 내부판 · 공개 보류 (Q4 P1-2) = 다른 컴퓨터에는 등록 안 된 편과 같다
    ent = _file(ep, role)
    if ent is None:
        return None
    fp = ep['dir'] / ent['name']
    try:
        st = os.lstat(fp)
        if not os.path.isfile(fp) or os.path.islink(fp) or _file_sha(fp, st) != ent['sha256']:
            return None
    except OSError:
        return None
    mime = ROLES[role]['mime'] or mimetypes.guess_type(ent['name'])[0] or 'application/octet-stream'
    return str(fp), ent, mime


_SRT_TIME = re.compile(r'(\d{1,2}):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*(\d{1,2}):(\d{2}):(\d{2})[,.](\d{3})')


def srt_to_vtt(text):
    """SRT 글 → WebVTT 글 (BOM · CRLF · 번호 줄 · 한 자리 시 · 깨진 덩어리 건너뜀 · 큐 글의 & < > 와 --> 막음)."""
    t = str(text).lstrip('﻿').replace('\r\n', '\n').replace('\r', '\n')
    out = ['WEBVTT', '']
    for block in re.split(r'\n[ \t]*\n', t.strip()):
        lines = [ln for ln in block.split('\n')]
        if lines and lines[0].strip().isdigit():
            lines = lines[1:]
        if not lines:
            continue
        m = _SRT_TIME.search(lines[0])
        if not m:
            continue
        g = m.groups()
        out.append(f'{int(g[0]):02d}:{g[1]}:{g[2]}.{g[3]} --> {int(g[4]):02d}:{g[5]}:{g[6]}.{g[7]}')
        for ln in lines[1:]:
            ln = ln.replace('-->', '→').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            out.append(ln)
        out.append('')
    return '\n'.join(out)


# ── markdown → HTML (꾸러미 글은 사람이 올린 것 — 허용한 태그 · 속성만 남긴다) ──
_ALLOWED_TAGS = {'p', 'br', 'hr', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'blockquote', 'pre', 'code', 'em', 'strong',
                 'b', 'i', 'del', 'sup', 'sub', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'a', 'span', 'div'}
_TAG = re.compile(r'<!--.*?-->|<(/?)([A-Za-z][A-Za-z0-9]*)((?:[^>"\']|"[^"]*"|\'[^\']*\')*)>', re.S)
_ATTR = re.compile(r'([A-Za-z_:][-A-Za-z0-9_:.]*)\s*=\s*("[^"]*"|\'[^\']*\'|[^\s"\'>]+)')
_SAFE_ALIGN = re.compile(r'\s*text-align\s*:\s*(left|right|center)\s*;?\s*', re.I)


def _safe_href(v):
    u = _html.unescape(v).strip()
    low = re.sub(r'[\s\x00-\x1f]+', '', u).lower()
    if low.startswith(('http://', 'https://', 'mailto:', '#')) or not re.match(r'[a-z][a-z0-9+.-]*:', low):
        return u
    return '#'


def _sanitize(html_text):
    def rep(m):
        whole = m.group(0)
        if whole.startswith('<!--'):
            return _html.escape(whole)
        close, tag, attrs = m.group(1), m.group(2).lower(), m.group(3) or ''
        if tag not in _ALLOWED_TAGS:
            return _html.escape(whole)
        if close:
            return f'</{tag}>'
        keep = []
        for am in _ATTR.finditer(attrs):
            k, v = am.group(1).lower(), am.group(2)
            if v[:1] in ('"', "'"):
                v = v[1:-1]
            if k == 'href' and tag == 'a':
                keep.append(f'href="{_html.escape(_safe_href(v), quote=True)}"')
            elif k == 'title':
                keep.append(f'title="{_html.escape(_html.unescape(v), quote=True)}"')
            elif k == 'align' and tag in ('th', 'td') and v.lower() in ('left', 'right', 'center'):
                keep.append(f'align="{v.lower()}"')
            elif k == 'style' and tag in ('th', 'td') and _SAFE_ALIGN.fullmatch(_html.unescape(v)):
                keep.append(f'style="{_html.escape(_html.unescape(v).strip(), quote=True)}"')
        if tag == 'a':
            keep.append('rel="noopener noreferrer"')
        return f'<{tag}{"".join(" " + a for a in keep)}>'
    return _TAG.sub(rep, html_text)


def md_html(text):
    """꾸러미 md → 안전한 HTML (철회값 가림 → markdown → 허용 태그 · 속성만 · 링크 = http(s) · mailto · # · 상대 주소)."""
    body = _r(text)
    try:
        import markdown
        out = markdown.markdown(body, extensions=['tables', 'fenced_code'])
    except ImportError:                  # pragma: no cover
        return '<pre>' + _html.escape(body) + '</pre>'
    return _sanitize(out)


def _section(md, word):
    """md 에서 '## …word…' 절 하나 (제목 줄 빼고) → 글 · 없으면 None."""
    if md is None:
        return None
    lines = md.splitlines()
    start = next((i for i, ln in enumerate(lines) if ln.startswith('## ') and word in ln), None)
    if start is None:
        return None
    end = next((j for j in range(start + 1, len(lines)) if lines[j].startswith('## ') or lines[j].startswith('# ')), len(lines))
    body = '\n'.join(lines[start + 1:end]).strip()
    return body or None


def _chapters(scenes, timeline, lead_s=None):
    """챕터 = 장면 첫 문장 시각 − 앞당김 (scenes.json 의 voice_model.lead_in · 공개 투영이라 그 칸이 없으면 episode.json chapter_lead_s)."""
    if not isinstance(scenes, dict) or not isinstance(timeline, dict):
        return []
    vm = scenes.get('voice_model') if isinstance(scenes.get('voice_model'), dict) else {}
    lead = vm.get('lead_in', lead_s if lead_s is not None else 0.0)
    lead = float(lead) if _finite(lead) and 0 <= lead <= 30 else 0.0
    by_id, first = {}, {}
    for ln in timeline.get('lines') or []:
        if isinstance(ln, dict) and isinstance(ln.get('id'), str) and _finite(ln.get('t0')):
            by_id[ln['id']] = ln
            sc = ln.get('scene')
            if isinstance(sc, str) and (sc not in first or ln['t0'] < first[sc]):
                first[sc] = float(ln['t0'])
    out = []
    for sc in scenes.get('scenes') or []:
        if not isinstance(sc, dict) or not isinstance(sc.get('id'), str):
            continue
        t0 = None
        lines = sc.get('lines') if isinstance(sc.get('lines'), list) else []
        if lines and isinstance(lines[0], dict) and lines[0].get('id') in by_id:
            t0 = float(by_id[lines[0]['id']]['t0'])
        elif sc['id'] in first:
            t0 = first[sc['id']]
        if t0 is None:
            continue
        t = max(0.0, t0 - lead)
        out.append(dict(t=t, t_attr=f'{t:.1f}', t_txt=fmt_clock(t), title=_r(sc.get('title') or sc['id'])))
    return out


def _scene_rows(scenes, timeline):
    rows = []
    if not isinstance(scenes, dict):
        return rows
    tl = {}
    tlines = timeline.get('lines') if isinstance(timeline, dict) else None
    for ln in tlines if isinstance(tlines, list) else []:
        if isinstance(ln, dict) and isinstance(ln.get('id'), str):
            tl[ln['id']] = ln
    for sc in scenes.get('scenes') or []:
        if not isinstance(sc, dict):
            continue
        lines = sc.get('lines') if isinstance(sc.get('lines'), list) else []
        shots = sc.get('shots') if isinstance(sc.get('shots'), list) else []
        ts = [tl[x['id']] for x in lines if isinstance(x, dict) and x.get('id') in tl]
        t0 = ts[0].get('t0') if ts else None
        t1 = None
        if ts and _finite(ts[-1].get('t1')):
            pz = ts[-1].get('pause')
            t1 = ts[-1]['t1'] + (pz if _finite(pz) else 0)
        rows.append(dict(id=_r(sc.get('id') or ''), title=_r(sc.get('title') or ''), n_lines=len(lines), n_shots=len(shots),
                         span=(f'{fmt_clock(t0)}–{fmt_clock(t1)}' if _finite(t0) and _finite(t1) else '—')))
    return rows


def _qc_model(rep, visibility, video_sha):
    """qc_report JSON → 화면 dict (그 편의 공개 범위 칸 · 없으면 None)."""
    if not isinstance(rep, dict):
        return None
    if isinstance(rep.get(visibility), dict):
        side = rep[visibility]
    elif not any(k in rep for k in ('public', 'internal')):
        side = rep
    else:
        return None

    def cnt(v):
        return len(v) if isinstance(v, list) else (v if _finite(v) else '—')
    checks = []
    for ck in side.get('checks') or []:
        if isinstance(ck, dict):
            checks.append(dict(what=_r(ck.get('what', '')), frames=_r(ck.get('frames', '—')),
                               viewed=_r(ck.get('viewed_frames', '—')), static=cnt(ck.get('static_over_5s')),
                               flicker=cnt(ck.get('flicker')), edge=_r(ck.get('edge_band_frames', '—'))))
    found = []
    for fd in side.get('found') or []:
        if isinstance(fd, dict):
            found.append(dict(t=_r(fd.get('t', '')), scene=_r(fd.get('scene', '')), what=_r(fd.get('what', '')),
                              fixed=_r(fd.get('fixed_in')) if fd.get('fixed_in') else ''))
    vs = side.get('sha256')
    known = {'video', 'sha256', 'duration_s', 'checks', 'found'}
    extra = [dict(key=_r(k), text=_r(json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v))
             for k, v in side.items() if k not in known]
    return dict(version=_r(rep.get('version', '')), video=_r(side.get('video', '')),
                match=(None if not isinstance(vs, str) else vs == video_sha), duration_txt=fmt_clock(side.get('duration_s')),
                checks=checks, found=found, extra=extra)


def _item(ep, current_id, held=False):
    m = ep['man']
    thumb = _file(ep, 'thumbnail')
    return dict(id=m['id'], url=f"/videos/{m['id']}", title=_r(m['title']), visibility=m['visibility'],
                duration_txt=fmt_clock(m.get('duration_s')), current=(m['id'] == current_id), held=bool(held),
                thumb_url=(f"/videos/{m['id']}/media/thumbnail" if thumb else None))


def page(folder, ep_id=None, include_internal=True):
    """화면 모델 — dict(state, problems, current (편 dict 또는 None), playlist, other_series, not_found, n_episodes).

    ep_id 없음 = 첫 편 (시리즈 · 편 번호 순) · 있음 = 그 편.  보일 편은 영상까지 sha256 대조 — 깨지면 목록에서 빼고 안내 (fail-closed).
    include_internal=False (이 컴퓨터가 아닌 요청 · 1저자 11-24 Q1) = 내부판 편을 목록 · 재생목록 · 다른 시리즈 · 첫 편 고르기에서 빼고,
    그 편을 물으면 등록 안 된 편과 같이 답한다 · 깨진 편 안내도 공개판으로 확인된 것만 (모름 · 내부판 = 안 보임)."""
    lib = library(folder)
    held = {e['man']['id']: public_problems(e)[0] for e in lib['episodes'] if e['man']['visibility'] == 'public'}
    eps = [e for e in lib['episodes']
           if include_internal or (e['man']['visibility'] == 'public' and not held.get(e['man']['id']))]
    probs = [q for q in lib['problems'] if include_internal or q.get('vis') == 'public']
    out = dict(state=lib['state'], problems=probs, current=None, playlist=None, other_series=[],
               not_found=False, n_episodes=len(eps))
    if ep_id is None:
        cand = list(eps)
    elif isinstance(ep_id, str) and ID_RE.fullmatch(ep_id) and ep_id not in RESERVED_IDS:
        cand = [e for e in eps if e['man']['id'] == ep_id]
    else:
        cand = []
    cur = None
    for e in cand:
        full, why = load_episode(e['dir'], deep_media=True)
        if full is not None:
            cur = full
            break
        out['problems'].append(dict(ep=e['man']['id'], why=why, vis=e['man']['visibility']))
        eps = [x for x in eps if x['man']['id'] != e['man']['id']]
    out['n_episodes'] = len(eps)
    if cur is None:
        out['not_found'] = ep_id is not None
        return out
    m = cur['man']
    items = [_item(e, m['id'], held.get(e['man']['id'])) for e in eps if e['man']['series'] == m['series']]
    pos = next((i for i, it in enumerate(items, 1) if it['current']), 1)
    groups = {}
    for e in eps:
        if e['man']['series'] != m['series']:
            groups.setdefault(e['man']['series'], []).append(e)
    out['playlist'] = dict(series=_r(m['series']), items=items, pos=pos, total=len(items))
    out['other_series'] = [dict(series=_r(sr), n=len(g), url=f"/videos/{g[0]['man']['id']}",
                                internal=all(x['man']['visibility'] == 'internal' for x in g)) for sr, g in groups.items()]
    out['current'] = _episode_model(cur)
    return out


def _episode_model(ep):
    m = ep['man']
    vid = _file(ep, 'video')
    srt = _file(ep, 'subtitles')
    thumb = _file(ep, 'thumbnail')
    scenes, timeline = _json(ep, 'scenes'), _json(ep, 'timeline')
    script = _text(ep, 'script')
    refs = _section(script, '참고 문헌')
    qc_md, rubric, readme = _text(ep, 'qc'), _text(ep, 'rubric'), _text(ep, 'readme')
    why_held, now = public_problems(ep)
    pc_reg = m.get('public_check') if isinstance(m.get('public_check'), dict) else {}
    dl = pc_reg.get('deny_list') if isinstance(pc_reg.get('deny_list'), dict) else None
    reg = ep.get('reg') or {}
    downloads = []
    for role in DOWNLOAD_ORDER:
        f = _file(ep, role)
        if f is not None:
            downloads.append(dict(role=role, url=f"/videos/{m['id']}/download/{role}", name=f['name'], size_txt=fmt_size(f['size'])))
    files = [dict(name=f['name'], role=f['role'], size_txt=fmt_size(f['size']), sha256=f['sha256'], verified=True)
             for f in m['files']]
    derived = [dict(name=_r(d.get('name', '')), src=_r(d.get('from', '')), src_sha=_r(d.get('from_sha256', '')),
                    dropped=', '.join(map(_r, d.get('dropped_keys') or [])),
                    how=_r(_DERIVED_HOW.get(d.get('method'), d.get('method') or '')))
               for d in m.get('derived') or [] if isinstance(d, dict)]
    return dict(
        id=m['id'], title=_r(m['title']), subtitle=_r(m.get('subtitle', '')), series=_r(m['series']), number=m.get('episode'),
        visibility=m['visibility'], duration_txt=fmt_clock(m.get('duration_s')), updated=m['updated'],
        packaged_at=_r(m.get('packaged_at', '')),
        video_url=f"/videos/{m['id']}/media/video", video_name=vid['name'], video_sha=vid['sha256'],
        poster_url=(f"/videos/{m['id']}/media/thumbnail" if thumb else None),
        vtt_url=(f"/videos/{m['id']}/subtitles.vtt" if srt else None),
        downloads=downloads, chapters=_chapters(scenes, timeline, m.get('chapter_lead_s')), scenes=_scene_rows(scenes, timeline),
        script_html=(md_html(script) if script else ''), refs_html=(md_html(refs) if refs else ''),
        qc=_qc_model(_json(ep, 'qc_report'), m['visibility'], vid['sha256']), qc_html=(md_html(qc_md) if qc_md else ''),
        rubric_html=(md_html(rubric) if rubric else ''), readme_html=(md_html(readme) if readme else ''),
        public_ok=bool(m['visibility'] == 'public' and not why_held and now['ok'] and pc_reg.get('ok') is True),
        held=[_r(w) for w in why_held], public_hits=len(now['hits']),
        public_rules=len(now['rules']), public_files=now['files'], deny_n=(dl or {}).get('n'),
        files=files, sums_sha=ep.get('sums_sha', ''), derived=derived,
        reg=dict(at=_r(reg.get('registered_at', '')), via=_r(reg.get('via', '')), bundle_sha=_r(reg.get('bundle_sha256', '')),
                 replaced=bool(reg.get('replaced'))),
        reg_note=ep.get('reg_note', ''),
    )
