#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② Q2 (1저자 11-12) — 탄소 접합 원장 (기하) **저장본**: 한 번 지어 저장하고 다음 팔이 지문을 대조해 읽는다.

왜: 원장 (`carbon_junction.cjunc_registry`) 은 침대 · 격자 · origin · 문턱 · 코드 · 환경에만 달리고 R_j · 법칙 · c · SV 노브에는 달리지 않는다
(`docs/reviews/rint2_time_reestimate_20261111/README.md` A-2 · E-2 4 번) — ⑥ 실측 팔 하나의 준비 4,567 s 가운데 4,040 s.  계획 (R_j · 법칙 · c · SV)
은 팔마다 그대로 다시 만든다 (`ca_ext_cjunc.payload_prepare`).  산출 바이트 (팔 JSON · 매니페스트 · 영수증 · 이름) 는 끔과 같다 — 결과 = 화면 한 줄뿐.

열쇠 (`Store.key_parts` → sha256) = 꼴 판 · 모델 판 · 스키마 · 코드 파일 sha256 (`CODE_MODULES` 넷 = `carbon_junction.py` · `step3_sigma.py` ·
`fibre_segment_raster.py` · 이 파일 — 원장 짓기가 실제로 부르는 모듈 + 직렬화기 · 시험 T14 가 짓는 동안 돈 파일 (sys.setprofile) · 원장 모듈의 import 문
(AST) 이 이 넷 안인지 잰다 · ★ 11-12 내부 반박 리뷰 RCP-01 — 옛 판은 fibre_segment_raster 를 빠뜨려 선분 → 셀 차례만 바뀐 코드에서 옛 원장을 돌려줬다) ·
환경 (`run_contract.env_unit_now` = python 부 판 · numpy · scipy 판 글자 + 실행 자리 지문 = venv 접두 · numpy · scipy 패키지 폴더 실경로의 blake2b ·
RCP-05) · 기계 지문 (`/etc/machine-id` blake2b — 못 읽으면 저장본 꺼짐 = 매번 짓기) · sid 격자 지문 · lo · vox (실수 비트) · 입력 넷
(`carbon_junction._input_check` 의 정준 float64 · int64 값) · 문턱 칸 (이름 · 형 · 비트).  코드 칸의 파일 = `importlib.util.find_spec` 이 가리키는 자리 (불러온
모듈이면 그 파일 · 아니면 import 가 찾을 파일) 를 **불러오지 않고** 해시한다 — 저장본 켬 런의 로드 모듈 집합 (매니페스트 exec_env) 이 끔과 같게.

파일 = `<폴더>/cjreg_<열쇠>.npz` (zip · STORED · 멤버 = header.json · skeleton.json (형 표지 트리) · a<i>.npy (배열 · `allow_pickle=False`)) ·
0444 · 단일 작성자 (임시 파일 O_EXCL 0600 → fsync → 읽어 대조 → chmod 0444 → `os.link` (먼저 쓴 쪽이 이김 · 덮어쓰기 없음) → 폴더 fsync).

읽기 처분 (CLAUDE.md "재개 규칙 지적 처분 기준" 꼴):
  · 없음 → 짓고 쓴다 (built_written · 같은 열쇠를 남이 먼저 쓰면 그 파일을 읽어 엄격 지문 대조 = built_peer_same · 다르면 멈춤)
  · **못 읽음** (CRC 로 확인한 멤버 바이트를 손에 넣기 전의 실패 — 0 바이트 · zip 꼴 · 멤버 집합 · CRC) = 정직한 흐름 (끊긴 복사 · 디스크) →
    다시 짓는다 · 그 파일은 두고 덮어쓰지 않는다 · ⚠ 줄 (unreadable_rebuilt · 운영자가 지운다)
  · **어긋남** (그 뒤 — 머리 JSON · 꼴 판 · 열쇠 · 뼈대 sha · 복원 · 엄격 지문 · registry_fp · sid 지문 · 심볼릭 링크 · 폴더 · 파일 소유자 · 그룹 ·
    남 쓰기 (11-12 RCP-06) · ★ 11-13 머리 중복 칸 (key_parts 를 다시 센 열쇠 · 머리 registry_fp = 복원 원장 fp — RCPX-05) · CRC 뒤 배열 해석의 뜻밖의
    예외 (머리 shape 넘침 OverflowError 등 — RCPX-04 · MemoryError 만 그대로)) = 손으로 고친 · 서로 어긋난 기록 → **멈춤** (`StoreInconsistent` →
    payload `S2_CJUNC_STORE|INCONSISTENT|` · rc ≠ 0).  머리의 비권위 진단 칸 = writer · runtime 둘뿐 (읽을 때 대조하지 않는다).
  · 쓰기 실패 (자리 · 권한 · link 미지원) = 기록만 (팔 결과 무관 · 늘 새로 지은 원장을 쓴다)
비트 같음 보증 = 엄격 지문 (노드마다 형 · dtype · 모양 · C/F · 바이트 · dict 키 차례 · **별칭 구조**) 을 쓰는 쪽이 짓자마자 세어 머리에 적고, 읽는
쪽이 복원한 원장을 같은 함수로 세어 같아야 쓴다 · `registry_fp` 다시 셈 = 기록 · 쓰는 쪽은 발행 전에 임시 파일을 같은 읽기 길로 다시 읽어 대조한다.
별칭 = 같은 변하는 객체 (ndarray · dict · list) 가 두 자리 이상에 — 되가리킴 노드로 싣고 복원본도 같은 객체를 그 자리들에 둔다 (원장의
`instances.pair_i` · `pair_j` = `[빈 배열] * instance 수` — instance 가 둘 이상인 원장은 늘 별칭이 있다 · `carbon_junction._merge_instances`).  서로
다른 배열 객체가 메모리를 나눠 쓰는 꼴 (보기 · 조각) 은 받지 않는다 (저장 안 함).  규모: 실침대 원장 = instance 십수만 × 작은 배열 넷 (약 47 만
멤버 · zip64) — 겹침 검사는 주소 구간 정렬 (배열 수 n 에 n log n).
⚠ 한정: 같은 열쇠 이름 아래 **자기 일관 위조** (내용 · 머리 · 지문을 모두 다시 센 파일) 는 저장본 혼자 가리지 못한다.  저장본 밖 독립 대조 = 봉인 원천
재조립 (`rint_r_chain.RunnerGraphSource` · 저장본을 읽지 않는다) 이고 그것은 **SV 모서리 팔 (끝 그래프 지문) 만** 덮는다 — 사다리 · 비 SV 예측 · 단위
팔은 독립 대조가 없다 (같은 코드 · 환경의 결정성 + 열쇠 + 폴더 권한 (소유자 = 이 사용자 · 그룹 · 남 쓰기 없음 · 심볼릭 링크 아님) + 파일 권한 (소유자 ·
그룹 · 남 쓰기 없음 · 0444 로 발행) 에 기댄다 · ★ 11-12 내부 반박 리뷰 RCP-03 — S0 단계 2 봉인 원장 지문 ↔ DBE arm 0 팔 대조 · SBE 사다리 팔의
대조 길 = 1저자 결정 · 2 회차 = 그 대조는 여전히 없다 (한정 그대로) — 다만 재리뷰 RCP2-01 꼴 (런 도중 코드 바뀜 → 옛 코드 원장이 새 코드 열쇠로 저장
→ 뒤 런 적중) 은 아래 '런 시작 코드 칸' 이 막는다 · 같은 코드 · 환경의 결정성 가정은 남는다).
★ 11-12 2 회차 (내부 반박 리뷰 재확인 RCP2-01) — **런 시작 코드 칸**: 이 모듈을 처음 불러온 때 (`_START` · payload = 입구 계약 · 러너 꼴
`--expect-physics` 의 ca_ext 칸 풀이 둘 다 원장 모듈 셋보다 먼저 부른다 — 시험 P6 · P6b) 열쇠 코드 파일 넷의 자리 · sha256 · **stat 신원** 을 잰다.
`get_or_build` 시작 · 적중 반환 직전 (★ 11-13 Codex 반박 1/2 RCPX-01) · 발행 직전 (`os.link` 바로 앞) 에 다시 세어 (`code_drift`) 파일 자리 · 내용 ·
stat 신원이 하나라도 다르면 그 런은 읽지도
(꺼짐 'disabled') 쓰지도 ('built_write_skipped') 않는다 · 사유 = `code_changed: …` (팔 결과 = 새로 지은 원장 그대로 · 다음 런부터 새 코드의 열쇠).  옛 판 =
코드 칸이 Store() 때의 디스크 해시라 런 도중 코드가 바뀌면 옛 코드로 지은 원장이 새 코드 열쇠로 저장되고 뒤의 정직한 런이 적중으로 받았다 (재리뷰 반례
CE-A · 시험 T15).
★ 11-12 3 회차 (내부 반박 리뷰 재확인 2 RCP3-02 · 본 세션 결정) — stat 신원 = 파일마다 (장치 · inode · 크기 · 수정 시각 ns · 상태 바뀐 시각 ns) 를 **정확히**
대조한다 (여유 없음 · 벽시계와 견주지 않는다 — 2 회차 판 = 수정 시각을 시작 + 1 s 와 견줘 같은 초 뒤집기 · 수정 시각을 되돌린 뒤집기를 놓치고, 수정
시각이 미래인 사본 (다른 기계에서 rsync -t) 의 정직한 런을 껐다 · 재확인 2 ce01 · 시험 T15g–j) · 시작 때 해시 앞뒤 stat 이 다르면 (재는 도중 바뀜) 못 셈 =
저장본 꺼짐 · Store 의 열쇠 코드 칸이 런 시작 코드 칸과 다르면 (변이판일 때 Store 를 만든 꼴) 읽지도 쓰지도 않는다 (시험 T15h · T15k).
⚠ 한정 (RCP2-01 · 3 회차 사실대로): (가) 이 모듈보다 **먼저** 불린 열쇠 모듈 (`_START['preloaded']`) 이 이 모듈을 부르기 전에 바뀐 것은 못 가린다 — payload
(두 꼴) · S0 감싸개는 그런 모듈이 없다 (P6 · P6b) · 원장 모듈을 먼저 부르는 다른 호출자 (시험 · 손 실행) 에는 남는다 (나) 시계 (상태 바뀐 시각의 바탕)
를 되돌린 뒤 같은 inode · 크기 · 시각으로 다시 쓴 뒤집기는 못 가린다 (특권 · 시계 조작 — 수정 시각 되돌리기 (`cp -p` · `rsync -t` · utime) 는 상태 바뀐
시각 · inode 가 잡는다) (다) 코드 칸 = 소스 sha256 — 낡은 `.pyc` 가 도는 것은 가리지 못한다 (라) 같은 프로세스 안에서 함수 객체를 바꿔 끼우는 것 (파일
그대로) 은 못 가린다 (마) 정직하게 다시 쓴 같은 내용 (`git checkout` · `touch` 꼴) 도 꺼짐 (보수 쪽 · 틀린 결과 아님).
★ 11-12 2 회차 (재리뷰 RCP2-02) — 뿌리 = 정규화된 꼴만 (`run_contract.normal_path_problem` — 빈 성분 · `.` · `..` 성분 = 마지막 글자 성분의 링크 판정을
비켜 간다 · 사슬 · 러너 같은 규칙).  ⚠ 한정 (RCP-06 남은 몫): 링크 판정은 마지막 성분뿐 (중간 성분 링크는 따른다) · 뿌리 · 파일 검사는 경로 기준이다
(검사 ↔ 사용 사이 바꿔치기 = fd 기준 아님) — 막는 것 = 이 사용자만 쓰는 폴더 (소유자 · 모드 검사).
⚠ Python 3.8 (kgy) 에서 돈다 — 3.9+ 문법 · 새 라이브러리 함수 없음.
"""
import errno
import hashlib
import json
import os
import re
import secrets
import struct
import time
import zipfile

import numpy as np

STORE_FORMAT = 'cjstore-v1'
STORE_KIND = 'cjunc_registry_store'
FILE_PREFIX = 'cjreg_'
FILE_SUFFIX = '.npz'
FILE_RE = re.compile(r'cjreg_[0-9a-f]{64}\.npz')
MACHINE_ID_PATHS = ('/etc/machine-id', '/var/lib/dbus/machine-id')
DISK_MARGIN_BYTES = 1 << 30
MEMBER_OVERHEAD_BYTES = 512                                  # zip 멤버 하나의 머리 (지역 · 중앙 목록 · npy 머리) 넉넉한 어림 — 쓰기 전 자리 검사
HEADER_MEMBER, SKELETON_MEMBER = 'header.json', 'skeleton.json'
_ARRAY_MEMBER_RE = re.compile(r'a(0|[1-9][0-9]*)\.npy')
#: 원장 코드 = 이 파일들의 바이트 (열쇠 칸) — 원장 함수 · 격자 지문 함수 (`step3_sigma._grid_fp`) · 원장의 선분 → 셀 함수
#  (`fibre_segment_raster.segment_cells` · `carbon_junction._positions` 가 부른다) · 이 직렬화기.  ★ 11-12 (내부 반박 리뷰 RCP-01) — 옛 판은 셋
#  (fibre_segment_raster 빠짐) 이라 그 파일만 바뀐 코드 판이 같은 열쇠로 옛 원장을 읽었다 (리뷰 반례 CE1 · 시험 T14c).  이 목록 ⊇ 원장 짓기가
#  실제로 부르는 프로젝트 모듈 = 시험 T14a (짓는 동안 돈 파일) · T14b (원장 모듈 둘의 import 문) 가 잰다 — 원장 코드가 새 모듈을 부르기 시작하면 거기서 터진다.
CODE_MODULES = ('carbon_junction', 'step3_sigma', 'fibre_segment_raster', 'cjunc_store')
STATUSES = ('hit', 'built_written', 'built_peer_same', 'unreadable_rebuilt', 'built_write_skipped', 'built_write_failed', 'disabled',
            'key_unavailable')
WARN_STATUSES = ('unreadable_rebuilt', 'built_write_skipped', 'built_write_failed', 'disabled', 'key_unavailable')
_NP_SCALAR_KINDS = 'biufcSUMm'

#: 시험 고리 (모듈 전역 · 단원 시험이 바꿔 끼운다) — 생산 동작 그대로
_statvfs = os.statvfs
_link = os.link


class Unsupported(TypeError):
    """저장할 수 없는 꼴 (서로 다른 배열의 메모리 겹침 · 비연속 · 읽기 전용 · 구조체 · 하위형 · 모르는 객체) — 저장하지 않는다 (팔 결과 무관).
    ★ 별칭 (같은 객체가 두 자리에) 은 받는다 — 되가리킴으로 싣는다 (`_Walk`)."""


class StoreInconsistent(RuntimeError):
    """손으로 고친 · 서로 어긋난 저장본 (또는 같은 열쇠 다른 원장) = 멈춤."""

    def __init__(self, code, why, path=None):
        super().__init__(f'{code}: {why}' + (f' ({os.path.basename(path)})' if path else ''))
        self.code, self.why, self.path = code, why, path


class _Unreadable(Exception):
    """못 읽음 (정직한 흐름) — 다시 짓는다."""


class _VerifyFailed(Exception):
    """쓰는 쪽 발행 전 대조 실패 (이 코드의 직렬화 결함) — 발행하지 않는다 (기록만 · 팔 결과 무관)."""


# ═════════════════════════ 엄격 지문 · 직렬화 (같은 걸음) ═════════════════════════
def _f8(x):
    return struct.pack('>d', float(x)).hex()


def _order(a):
    if a.flags.c_contiguous:
        return 'C'
    if a.flags.f_contiguous:
        return 'F'
    raise Unsupported(f'비연속 배열 (모양 {a.shape}) — 저장 꼴 밖')


def _check_array(a):
    if type(a) is not np.ndarray:
        raise Unsupported(f'배열 하위형 {type(a).__name__}')
    if a.dtype.fields is not None or a.dtype.subdtype is not None:
        raise Unsupported(f'구조체 · 하위 dtype {a.dtype}')
    if not a.flags.writeable:
        raise Unsupported('읽기 전용 배열 (복원본은 쓸 수 있다 — 꼴이 다르다)')
    if not a.dtype.hasobject and a.dtype.kind not in _NP_SCALAR_KINDS:
        raise Unsupported(f'배열 dtype 종류 {a.dtype.kind}')
    return _order(a)


class _Walk:
    """한 걸음 = 엄격 지문 (hash) + 뼈대 노드 + 배열 목록 + 메모리 구간 — 같은 규칙 (받지 않는 꼴은 Unsupported).
    ★ 별칭 — 변하는 객체 (ndarray · dict · list) 를 **처음 만난 차례**로 번호를 매기고 (자식보다 먼저), 같은 객체를 다시 만나면 되가리킴
      (지문 b'R' + 번호 · 뼈대 ['r', 번호]) — `decode` 가 같은 차례로 번호를 매겨 같은 객체를 그 자리에 다시 둔다.  튜플 · 스칼라 · 글은 불변이라
      번호를 매기지 않는다 (값만).  자기 자신을 담은 목록 (고리) 도 같은 길로 끝난다."""

    def __init__(self, want_skel):
        self.h = hashlib.sha256()
        self.want_skel = want_skel
        self.arrays = []                                     # 객체 dtype 아닌 배열 (처음 만난 차례 = zip 멤버 a<i>) — want_skel 일 때만
        self.spans = []                                      # 빈 배열이 아닌 배열 (객체 dtype 포함) 의 메모리 구간 [시작, 끝) — 겹침 검사
        self.seen = {}                                       # id → 번호 (변하는 객체 · 걷는 동안 살아 있다 = id 가 다시 쓰이지 않는다)

    def _u(self, tag, b=b''):
        self.h.update(tag)
        self.h.update(len(b).to_bytes(8, 'big'))
        self.h.update(b)

    def _back(self, x):
        """변하는 객체 x 를 다시 만났나 → 처음 = 번호를 매기고 None · 다시 = 되가리킴 노드 (지문에도)."""
        k = self.seen.get(id(x))
        if k is None:
            self.seen[id(x)] = len(self.seen)
            return None
        self._u(b'R', str(k).encode('ascii'))
        return ['r', k]

    def node(self, x):
        t = type(x)
        if t is np.ndarray:
            ref = self._back(x)
            if ref is not None:
                return ref
            order = _check_array(x)
            if x.size:
                p = x.__array_interface__['data'][0]
                self.spans.append((p, p + x.nbytes))
            dstr, shape = x.dtype.str, [int(s) for s in x.shape]
            self._u(b'A', json.dumps([dstr, shape, order, bool(x.dtype.hasobject)]).encode('ascii'))
            if x.dtype.hasobject:
                items = [self.node(v) for v in x.reshape(-1, order='C')]
                return ['o', dstr, shape, order, items] if self.want_skel else None
            c = x if x.flags.c_contiguous else np.ascontiguousarray(x)
            self._u(b'D', memoryview(c.reshape(-1).view(np.uint8)) if c.size else b'')
            if self.want_skel:
                self.arrays.append(x)
                return ['a', len(self.arrays) - 1, dstr, shape, order]
            return None
        if isinstance(x, np.generic):
            if x.dtype.kind not in _NP_SCALAR_KINDS or t is not x.dtype.type:
                raise Unsupported(f'numpy 스칼라 {t.__name__} ({x.dtype})')
            self._u(b'G', json.dumps([x.dtype.str]).encode('ascii') + b'|' + x.tobytes())
            return ['g', x.dtype.str, x.tobytes().hex()] if self.want_skel else None
        if t is dict:
            ref = self._back(x)
            if ref is not None:
                return ref
            self._u(b'{', str(len(x)).encode('ascii'))
            out = []
            for k, v in x.items():
                if type(k) is str:
                    kn = ['s', k]
                    self._u(b'k', k.encode('utf-8', 'surrogatepass'))
                elif type(k) is int:
                    kn = ['i', str(k)]
                    self._u(b'K', str(k).encode('ascii'))
                else:
                    raise Unsupported(f'dict 키 형 {type(k).__name__}')
                vn = self.node(v)
                out.append([kn, vn])
            return ['d', out] if self.want_skel else None
        if t is list or t is tuple:
            if t is list:                                    # 튜플은 불변 (빈 튜플 = 한 객체) — 별칭은 안의 변하는 객체마다 따로 본다
                ref = self._back(x)
                if ref is not None:
                    return ref
            self._u(b'[' if t is list else b'(', str(len(x)).encode('ascii'))
            items = [self.node(v) for v in x]
            return [('l' if t is list else 't'), items] if self.want_skel else None
        if x is None:
            self._u(b'N')
            return ['n']
        if t is bool:
            self._u(b'B', b'1' if x else b'0')
            return ['b', bool(x)]
        if t is int:
            self._u(b'I', str(x).encode('ascii'))
            return ['i', str(x)]
        if t is float:
            self._u(b'F', struct.pack('>d', x))
            return ['f', _f8(x)]
        if t is str:
            self._u(b'S', x.encode('utf-8', 'surrogatepass'))
            return ['s', x]
        if t is bytes:
            self._u(b'Y', x)
            return ['y', x.hex()]
        raise Unsupported(f'모르는 형 {t.__module__}.{t.__qualname__}')


def _no_overlap(spans):
    """서로 다른 배열 객체가 메모리를 나눠 쓰면 (보기 · 조각) 복원본이 둘로 갈린다 → 거부.  받는 배열은 연속 (C · F) 뿐이라 배열의 메모리 =
    구간 [자료 주소, + nbytes) 그대로다 — 구간을 주소 차례로 놓고 앞 구간들의 끝과만 견준다 (배열 수 n 에 n log n).
    ★ 대피 세션 11-12 — 옛 판 = 배열 쌍마다 `np.shares_memory` (n²) · 실침대 원장 (instance 117,583 × 작은 배열 넷 = 약 47 만 배열) 에서 끝나지
      않는다 · 객체 dtype 배열은 보지 않았다 (지금은 본다)."""
    end = -1
    for s, e in sorted(spans):
        if s < end:
            raise Unsupported('메모리가 겹치는 배열 둘 (복원본은 둘로 갈린다)')
        if e > end:
            end = e


def _walk(obj, want_skel):
    w = _Walk(want_skel)
    skel = w.node(obj)
    _no_overlap(w.spans)
    return w, skel


def _skel_bytes(skel):
    return json.dumps(skel, ensure_ascii=True, separators=(',', ':'), allow_nan=False).encode('ascii')


def strict_digest(obj):
    """엄격 지문 (sha256 hex) — 형 · dict 키 차례 · dtype · 모양 · C/F · 바이트 · 실수 비트 · 객체 원소 · 별칭 구조.  받지 않는 꼴 = Unsupported."""
    return _walk(obj, False)[0].h.hexdigest()


def encode(obj):
    """→ (뼈대 바이트 (ASCII JSON), 배열 목록 (객체 dtype 없음 · 같은 객체는 한 번)).  받지 않는 꼴 = Unsupported."""
    w, skel = _walk(obj, True)
    return _skel_bytes(skel), list(w.arrays)


def encode_strict(obj):
    """한 걸음으로 → (엄격 지문, 뼈대 바이트, 배열 목록) — `strict_digest` · `encode` 를 따로 부른 것과 같은 값 (쓰는 쪽 · 큰 원장을 한 번만 센다)."""
    w, skel = _walk(obj, True)
    return w.h.hexdigest(), _skel_bytes(skel), list(w.arrays)


def _dec(n, arrays, nodes):
    """뼈대 노드 → 객체.  nodes = 변하는 객체 (ndarray · dict · list) 를 만든 차례 (`_Walk` 의 번호와 같은 차례 — 자식보다 먼저 올린다)."""
    tag = n[0]
    if tag == 'n':
        return None
    if tag == 'b':
        if type(n[1]) is not bool:
            raise ValueError('bool 노드')
        return n[1]
    if tag == 'i':
        if type(n[1]) is not str or not re.fullmatch(r'-?(0|[1-9][0-9]*)', n[1]):
            raise ValueError('int 노드')
        return int(n[1])
    if tag == 'f':
        return struct.unpack('>d', bytes.fromhex(n[1]))[0]
    if tag == 's':
        if type(n[1]) is not str:
            raise ValueError('str 노드')
        return n[1]
    if tag == 'y':
        return bytes.fromhex(n[1])
    if tag == 'r':
        k = n[1]
        if type(k) is not int or not 0 <= k < len(nodes):
            raise ValueError('되가리킴 노드 (아직 없는 번호)')
        return nodes[k]
    if tag == 'l':
        out = []
        nodes.append(out)
        for v in n[1]:
            out.append(_dec(v, arrays, nodes))
        return out
    if tag == 't':
        return tuple([_dec(v, arrays, nodes) for v in n[1]])
    if tag == 'd':
        out = {}
        nodes.append(out)
        for kn, vn in n[1]:
            if kn[0] not in ('s', 'i'):
                raise ValueError('dict 키 노드')
            k = _dec(kn, arrays, nodes)
            if type(k) not in (str, int) or k in out:
                raise ValueError('dict 키 노드')
            out[k] = _dec(vn, arrays, nodes)
        return out
    if tag == 'g':
        dt = np.dtype(n[1])
        raw = bytes.fromhex(n[2])
        if dt.kind not in _NP_SCALAR_KINDS or len(raw) != dt.itemsize:
            raise ValueError('numpy 스칼라 노드')
        return np.frombuffer(raw, dtype=dt)[0]
    if tag == 'a':
        idx, dstr, shape, order = n[1], n[2], n[3], n[4]
        if type(idx) is not int or not 0 <= idx < len(arrays):
            raise ValueError('배열 노드 번호')
        a = arrays[idx]
        if a.dtype.str != dstr or list(a.shape) != list(shape) or a.dtype.hasobject:
            raise ValueError(f'배열 노드 {idx} dtype/모양')
        if order == 'C' and not a.flags.c_contiguous or order == 'F' and not (a.flags.f_contiguous and not a.flags.c_contiguous):
            raise ValueError(f'배열 노드 {idx} 차례')
        nodes.append(a)
        return a
    if tag == 'o':
        dstr, shape, order, items = n[1], n[2], n[3], n[4]
        if np.dtype(dstr) != np.dtype(object) or order not in ('C', 'F'):
            raise ValueError('객체 배열 노드')
        out = np.empty(tuple(shape), dtype=object, order=order)
        if len(items) != out.size:
            raise ValueError('객체 배열 원소 수')
        nodes.append(out)
        vals = [_dec(v, arrays, nodes) for v in items]
        flat = out.reshape(-1, order='C') if order == 'C' else None
        if flat is not None:
            for i, v in enumerate(vals):
                flat[i] = v
        else:
            for i, idx in enumerate(np.ndindex(*out.shape)):
                out[idx] = vals[i]
        return out
    raise ValueError(f'모르는 노드 {tag!r}')


def decode(skel_bytes, arrays):
    """뼈대 + 배열 → 객체 (encode 의 역 · 배열은 그대로 꽂는다 · 되가리킴 = 같은 객체)."""
    n = json.loads(skel_bytes.decode('ascii'))
    used = []
    obj = _dec(n, arrays, [])

    def count(m):
        if isinstance(m, list) and m:
            if m[0] == 'a':
                used.append(m[1])
            elif m[0] in ('l', 't'):
                for v in m[1]:
                    count(v)
            elif m[0] == 'd':
                for kv in m[1]:
                    count(kv[1])
            elif m[0] == 'o':
                for v in m[4]:
                    count(v)
    count(n)
    if sorted(used) != list(range(len(arrays))):
        raise ValueError('배열 노드 ↔ 멤버 (한 번씩)')
    return obj


# ═════════════════════════ 열쇠 ═════════════════════════
def machine_fp(paths=MACHINE_ID_PATHS):
    """기계 지문 (blake2b 16 바이트 hex) — 처음 읽힌 machine-id (빈 줄 아님) · 못 읽으면 None (저장본 꺼짐)."""
    for p in paths:
        try:
            with open(p, 'rb') as f:
                raw = f.read(4096).strip()
        except OSError:
            continue
        if raw:
            return hashlib.blake2b(raw, digest_size=16).hexdigest()
    return None


def _file_sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def code_file(name):
    """열쇠 코드 칸의 모듈 → 파일 경로 (`importlib.util.find_spec` — 불러온 모듈이면 그 `__spec__` 의 파일 · 아니면 import 가 찾을 파일) · **불러오지
    않는다** (★ 11-12 RCP-01 — 저장본 켬 런이 끔 런에 없는 모듈을 부르면 매니페스트 exec_env 의 로드 모듈 집합 · 내용 해시가 갈린다 · 시험 T14d).
    못 찾음 = ValueError (Store 를 만들지 않는다 — payload 가 구조화 거부 STORE_PATH 로 멈춘다)."""
    import importlib.util
    try:
        spec = importlib.util.find_spec(name)
    except (ImportError, ValueError) as e:
        raise ValueError(f'열쇠 코드 모듈 {name} 을 못 찾는다 ({type(e).__name__}: {e})') from None
    origin = getattr(spec, 'origin', None) if spec is not None else None
    if not origin or not os.path.isfile(origin):
        raise ValueError(f'열쇠 코드 모듈 {name} 의 파일이 없다 ({origin!r})')
    return origin


def env_paths_fp():
    """실행 자리 지문 (blake2b 16 바이트 hex) — 인터프리터 접두 (`sys.prefix` = venv) · numpy · scipy 패키지 폴더의 실경로.  ★ 11-12 (내부 반박 리뷰
    RCP-05) — 판 글자가 같은 두 venv · 두 설치 (빌드 · BLAS 가 다를 수 있다 · 원장 길의 1 차원 `np.linalg.norm` = BLAS dot) 를 가른다 · 경로 글 대신 지문
    (머리 · 열쇠에 계정 · 집 폴더 글을 남기지 않는다).  ⚠ 같은 자리에서 다시 빌드한 설치 · 같은 machine-id 를 가진 복제 기계는 가르지 못한다 (한정)."""
    import sys
    import scipy
    parts = (os.path.realpath(sys.prefix), os.path.dirname(os.path.realpath(np.__file__)), os.path.dirname(os.path.realpath(scipy.__file__)))
    return hashlib.blake2b('\0'.join(parts).encode('utf-8', 'surrogatepass'), digest_size=16).hexdigest()


def root_last(p):
    """폴더 경로의 끝 빗금을 걷은 꼴 (심볼릭 링크 판정용 — `lstat('링크/')` 은 링크를 따라간다) · '/' 는 그대로 (사슬 `cjunc_store_dir_problem` 과 같은 식)."""
    return p.rstrip('/') or '/'


# ═════════════════════════ 런 시작 코드 칸 (★ 11-12 2 회차 · 내부 반박 리뷰 재확인 RCP2-01) ═════════════════════════
#: 런 도중 코드 바뀜 사유의 머리 (기록 `why` · 상태 = 'disabled' (get_or_build 시작) · 'built_write_skipped' (발행 직전))
CODE_CHANGED = 'code_changed'
def _stat_id(path):
    """★ 3 회차 (RCP3-02) — 파일 stat 신원 = [장치 · inode · 크기 · 수정 시각 ns · 상태 바뀐 시각 ns] (내용을 그대로 다시 써도 · 수정 시각을 되돌려도
    달라진다 — 상태 바뀐 시각은 utime 으로 못 되돌린다 · 벽시계와 견주지 않는다)."""
    st = os.stat(path)
    return [st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns]


def _code_column():
    """열쇠 코드 칸 지금 값 → ({파일 이름: sha256}, {파일 이름: 실경로}, {파일 이름: stat 신원}) — `code_file` (불러오지 않는다) · 못 찾음 = ValueError ·
    못 읽음 = OSError · 해시 앞뒤 stat 신원이 다름 (재는 도중 바뀜) = OSError."""
    code, paths, ids = {}, {}, {}
    for m in CODE_MODULES:
        f = code_file(m)
        b = os.path.basename(f)
        real = os.path.realpath(f)
        s1 = _stat_id(real)
        code[b] = _file_sha(real)
        s2 = _stat_id(real)
        if s1 != s2:
            raise OSError(f'{b} 를 재는 도중 바뀌었다 (stat 신원)')
        paths[b] = real
        ids[b] = s2
    return code, paths, ids


def _start_record():
    """이 모듈을 처음 불러온 때 = 런 시작 (payload = 입구 계약 · 러너 꼴 ca_ext 칸 풀이 둘 다 원장 모듈보다 먼저 · 시험 P6 · P6b) → {시각 ns · 코드 칸 ·
    실경로 · stat 신원 · 먼저 불린 열쇠 모듈 · 못 셈 사유}.  못 세면 (모듈 · 파일 없음 · 재는 도중 바뀜) 오류만 적는다 (접합 끔 런에서도 불리는 모듈 —
    예외를 올리지 않는다 · 저장본은 그때 꺼진다)."""
    import sys
    rec = {'t_ns': time.time_ns(), 'code': None, 'paths': None, 'stat': None, 'error': None,
           'preloaded': sorted(m for m in CODE_MODULES if m != 'cjunc_store' and m in sys.modules)}
    try:
        rec['code'], rec['paths'], rec['stat'] = _code_column()
    except (ValueError, OSError) as e:
        rec['error'] = f'{type(e).__name__}: {e}'
    return rec


_START = _start_record()


def code_drift():
    """런 시작 (`_START`) 뒤 열쇠 코드 파일이 바뀌었는가 → 사유 목록 (빈 목록 = 그대로).  본다: 파일 자리 (`code_file` 이 지금 가리키는 실경로 — 같은
    프로세스에서 모듈을 바꿔 끼운 꼴 포함) · 내용 sha256 · stat 신원 (장치 · inode · 크기 · 수정 · 상태 바뀐 시각 ns — 정확히 같아야 · ★ 3 회차 RCP3-02 ·
    내용이 같아도 다시 쓰면 다르다).  시작 때 못 셌으면 그 사유 하나 (= 저장본 꺼짐)."""
    s = _START
    if s.get('error') or not s.get('code') or not s.get('stat'):
        return [f'런 시작 때 코드 칸을 못 셌다 ({s.get("error")})']
    try:
        now, paths, ids = _code_column()
    except (ValueError, OSError) as e:
        return [f'지금 코드 칸을 못 센다 ({type(e).__name__}: {e})']
    why = []
    for b in sorted(set(now) | set(s['code'])):
        a, c = s['code'].get(b), now.get(b)
        if s['paths'].get(b) != paths.get(b):
            why.append(f'{b} 자리 바뀜')
        elif a != c:
            why.append(f'{b} sha {str(a)[:12]} → {str(c)[:12]}')
        elif s['stat'].get(b) != ids.get(b):
            why.append(f'{b} stat 신원 바뀜 (다시 씀 · 시각 — 내용 같음)')
    return why


def _tag(v):
    if v is None:
        return ['none']
    if isinstance(v, (bool, np.bool_)):
        return ['bool', bool(v)]
    if isinstance(v, (int, np.integer)):
        return ['int', str(int(v))]
    if isinstance(v, (float, np.floating)):
        return ['float', _f8(v)]
    raise TypeError(f'문턱 값 형 {type(v).__name__}')


def _inputs_fp(pts, phase, fid, kind):
    import carbon_junction as CJ
    P, PH, F, K = CJ._input_check(pts, phase, fid, kind)
    h = hashlib.blake2b(digest_size=32)
    for a in (P, PH, F, K):
        c = np.ascontiguousarray(a)
        h.update(c.dtype.str.encode('ascii'))
        h.update(repr(c.shape).encode('ascii'))
        h.update(c.reshape(-1).view(np.uint8).tobytes() if c.size else b'')
    return h.hexdigest()


def file_name(key):
    return f'{FILE_PREFIX}{key}{FILE_SUFFIX}'


def _errname(e):
    return errno.errorcode.get(getattr(e, 'errno', None) or 0, type(e).__name__)


# ═════════════════════════ 저장본 ═════════════════════════
class Store:
    """저장본 폴더 하나 (절대 경로 · 정규화된 꼴 · 있는 폴더 · 심볼릭 링크 아님 · 소유자 = 이 사용자 · 그룹 · 남 쓰기 없음).  열쇠의 코드 · 환경 · 기계
    칸은 만들 때 한 번 읽는다 (코드 칸 = 그때의 디스크 파일 — 불러온 코드 자체가 아니다 · ★ 2 회차 RCP2-01 = 런 시작 (`_START`) 과 다르면 get_or_build
    가 읽지도 쓰지도 않고 · 발행 직전에 다시 센다 · `code_drift` · ★ 3 회차 RCP3-02 = 코드 칸 자체가 런 시작 코드 칸과 같을 때만 읽고 쓴다)."""

    def __init__(self, root, machine_paths=MACHINE_ID_PATHS):
        if not isinstance(root, str) or not os.path.isabs(root):
            raise ValueError(f'저장본 폴더 = 절대 경로 ({root!r})')
        import stat as _stat
        import run_contract as RC
        #  ★ 11-12 2 회차 (재리뷰 RCP2-02) — 정규화된 꼴만 (`<링크>/.` · `/./` · `//` · `/../` 이 아래 마지막 성분 링크 판정을 비켜 갔다 · 사슬 · 러너 같은 규칙)
        _np = RC.normal_path_problem(root)
        if _np is not None:
            raise ValueError(f'저장본 폴더 경로가 정규화된 꼴이 아니다 ({root}) — {_np}')
        try:
            lst = os.lstat(root_last(root))
            st = os.stat(root)
        except OSError as e:
            raise ValueError(f'저장본 폴더가 없다 ({root} · {_errname(e)})') from None
        #  ★ 11-12 (내부 반박 리뷰 RCP-06) — 뿌리 = 링크를 따르지 않는다 (남이 바꿀 수 있는 링크 너머 폴더에 쓰지 않는다 · 끝 빗금도 · 사슬 · 러너도 같은 규칙)
        if _stat.S_ISLNK(lst.st_mode):
            raise ValueError(f'저장본 폴더가 심볼릭 링크다 ({root}) — 실제 폴더 경로를 준다')
        if not _stat.S_ISDIR(st.st_mode):
            raise ValueError(f'저장본 자리가 폴더가 아니다 ({root})')
        if st.st_mode & 0o022:
            raise ValueError(f'저장본 폴더를 그룹 · 남이 쓸 수 있다 (모드 {oct(st.st_mode & 0o777)} · 단일 작성자 · umask 022 셸에서 만든다)')
        if hasattr(os, 'getuid') and st.st_uid != os.getuid():
            raise ValueError(f'저장본 폴더 소유자 ({st.st_uid}) ≠ 이 사용자 ({os.getuid()})')
        self.root = root
        self.code = {}
        for m in CODE_MODULES:                               # ★ 11-12 (RCP-01) — find_spec 으로 파일만 (불러오지 않는다 · `code_file`)
            f = code_file(m)
            self.code[os.path.basename(f)] = _file_sha(f)
        self.env = dict(RC.env_unit_now(), paths=env_paths_fp())   # ★ 11-12 (RCP-05) — 판 글자 + 실행 자리 지문
        self.machine = machine_fp(machine_paths)

    # ── 열쇠 ──
    def key_parts(self, *, sid, lo, vox, pts, phase, fid, kind, thresholds):
        import carbon_junction as CJ
        if self.machine is None:
            raise ValueError('기계 id 를 못 읽었다')
        return {'format': STORE_FORMAT, 'model': CJ.CJUNC_MODEL_VERSION, 'schema': CJ.CJUNC_SCHEMA, 'code': dict(self.code),
                'env': dict(self.env), 'machine': self.machine, 'sid': CJ._grid_fp(sid),
                'lo': [_f8(x) for x in np.asarray(lo, np.float64).reshape(3)], 'vox': _f8(float(vox)),
                'inputs': _inputs_fp(pts, phase, fid, kind), 'thresholds': [[k, _tag(thresholds[k])] for k in sorted(thresholds)]}

    @staticmethod
    def key_of(parts):
        return hashlib.sha256(json.dumps(parts, sort_keys=True, separators=(',', ':')).encode('ascii')).hexdigest()

    def key(self, **kw):
        return self.key_of(self.key_parts(**kw))

    def path(self, key):
        return os.path.join(self.root, file_name(key))

    # ── 읽기 ──
    def _read(self, path, key, sid, check_name=True):
        """→ 원장 (적중) · None (없음) · _Unreadable (못 읽음) · StoreInconsistent (어긋남).
        두 단 — ① 그릇 (`_read_members` · CRC 로 확인한 멤버 바이트를 손에 넣기 전의 실패 = 못 읽음) ② 내용 (그 뒤는 전부 어긋남 — 뜻밖의
        오류도 · 쓰는 쪽이 발행 전에 같은 길로 읽어 봤으므로 발행된 파일이 여기서 걸리면 그 뒤에 바뀐 것이다 · 메모리 부족만 그대로 올린다)."""
        got = _read_members(path)
        if got is None:
            return None
        hb, sb, arrays = got
        try:
            return self._content(path, key, sid, check_name, hb, sb, arrays)
        except (StoreInconsistent, MemoryError):
            raise
        except Exception as e:                                 # noqa: BLE001 — CRC 를 지난 바이트에서 난 뜻밖의 오류 = 어긋남 (멈춤)
            raise StoreInconsistent('content', f'내용 대조 중 뜻밖의 오류 ({type(e).__name__}: {str(e)[:80]})', path) from None

    def _content(self, path, key, sid, check_name, hb, sb, arrays):
        try:
            h = json.loads(hb.decode('utf-8'))
        except (UnicodeDecodeError, ValueError) as e:
            raise StoreInconsistent('header', f'머리 JSON ({type(e).__name__})', path) from None
        if not isinstance(h, dict) or h.get('format') != STORE_FORMAT or h.get('kind') != STORE_KIND:
            raise StoreInconsistent('format', f'꼴 판 · 종류 ({h.get("format") if isinstance(h, dict) else None!r})', path)
        if h.get('key') != key or (check_name and os.path.basename(path) != file_name(key)):
            raise StoreInconsistent('key', f'머리 열쇠 {str(h.get("key"))[:12]} ≠ 이 열쇠 {key[:12]} (이름 바꿈 · 복사)', path)
        #  ★ 11-13 (Codex 반박 1/2 RCPX-05) — 머리의 중복 칸도 대조한다: 열쇠 칸 (key_parts) 을 다시 센 열쇠 = 머리 열쇠 (옛 = key_parts 만 바꾼 파일을
        #    적중으로 받았다 · 진단 · 출처 칸의 모순) · 머리 registry_fp = 복원 원장 fp (아래 · 원장 대조 뒤).  비권위 진단 칸 = writer · runtime 뿐
        #    (대조하지 않는다 · 모듈 머리 글)
        _kp = h.get('key_parts')
        if not isinstance(_kp, dict) or self.key_of(_kp) != key:
            raise StoreInconsistent('header', '머리 key_parts 를 다시 센 열쇠 ≠ 머리 열쇠 (머리 열쇠 칸 손댐)', path)
        if h.get('skeleton_sha256') != hashlib.sha256(sb).hexdigest() or h.get('n_arrays') != len(arrays):
            raise StoreInconsistent('skeleton', '뼈대 sha256 · 배열 수 ≠ 머리', path)
        try:
            obj = decode(sb, arrays)
        except (ValueError, KeyError, IndexError, TypeError, UnicodeDecodeError, RecursionError, OverflowError) as e:
            raise StoreInconsistent('decode', f'뼈대 복원 ({type(e).__name__}: {str(e)[:80]})', path) from None
        try:
            sd = strict_digest(obj)
        except Unsupported as e:
            raise StoreInconsistent('decode', f'복원본 꼴 ({e})', path) from None
        if sd != h.get('strict'):
            raise StoreInconsistent('strict', '복원한 원장의 엄격 지문 ≠ 머리 (내용 · 직렬화 어긋남)', path)
        import carbon_junction as CJ
        try:
            fp_ok = CJ.registry_fp(obj) == obj['fp']['registry']
            sid_ok = obj['fp']['sid'] == CJ._grid_fp(sid)
        except MemoryError:
            raise
        except Exception as e:                                 # noqa: BLE001 — 원장 꼴이 아니다 = 어긋남
            raise StoreInconsistent('registry', f'원장 꼴 ({type(e).__name__}: {str(e)[:80]})', path) from None
        if not fp_ok:
            raise StoreInconsistent('registry_fp', '원장 지문 다시 셈 ≠ 원장 안 기록', path)
        if not sid_ok:
            raise StoreInconsistent('sid', '원장 sid 지문 ≠ 지금 격자', path)
        if h.get('registry_fp') != obj['fp']['registry']:      # ★ 11-13 (RCPX-05) — 머리 중복 칸 (원장 대조 뒤 · 앞 갈래의 판별을 가리지 않게)
            raise StoreInconsistent('header', '머리 registry_fp ≠ 복원 원장 fp (머리 중복 칸 손댐)', path)
        return obj

    # ── 쓰기 ──
    def _publish(self, key, reg, parts, strict, skel, arrays, build_s, sid):
        """→ (상태, 사유, 바이트).  실패는 기록만 (예외 없음) · 같은 열쇠 다른 원장 = StoreInconsistent."""
        final = self.path(key)
        size = len(skel) + sum(int(a.nbytes) for a in arrays) + MEMBER_OVERHEAD_BYTES * (len(arrays) + 2)
        try:
            sv = _statvfs(self.root)
            free = int(sv.f_bavail) * int(sv.f_frsize)
        except OSError as e:
            return 'built_write_failed', f'statvfs {_errname(e)}', None
        if free < 2 * size + DISK_MARGIN_BYTES:
            return 'built_write_skipped', f'disk 여유 {free} < 2 × {size} + 1 GiB', None
        #  ★ 11-12 (내부 반박 리뷰 RCP-11) — 쓴 쪽 칸에 호스트 이름을 싣지 않는다 (사슬은 기계를 실행자가 넣는 짧은 이름표로만 남긴다 · 호스트
        #    이름은 FQDN · 주소일 수 있다) · 기계 구별 = 열쇠의 machine-id 지문
        #  ★ 11-13 (Q2 · 1저자 "권고대로") — runtime = 지은 프로세스의 실행 환경 기록 (열쇠 아님 · 읽을 때 대조 안 함 = 비권위 진단 · "R 동안 고정" 계약의
        #    대조 자료 · `runtime_record`)
        header = {'format': STORE_FORMAT, 'kind': STORE_KIND, 'key': key, 'key_parts': parts,
                  'skeleton_sha256': hashlib.sha256(skel).hexdigest(), 'n_arrays': len(arrays), 'strict': strict,
                  'registry_fp': reg['fp']['registry'],
                  'writer': {'pid': os.getpid(), 'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                             'build_seconds': round(float(build_s), 3)},
                  'runtime': runtime_record()}
        hb = json.dumps(header, ensure_ascii=True, sort_keys=True, separators=(',', ':')).encode('ascii')
        tmp = os.path.join(self.root, f'.{FILE_PREFIX}{key}.{os.getpid()}.{secrets.token_hex(4)}.tmp')
        made = False
        try:
            fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            made = True
            with os.fdopen(fd, 'wb') as f:
                _write_zip(f, hb, skel, arrays)
                f.flush()
                os.fsync(f.fileno())
            try:                                                           # 발행 전 같은 읽기 길로 대조 (직렬화기 결함 = 발행 안 함 · 멈춤 아님)
                got = self._read(tmp, key, sid, check_name=False)
                ok_back = got is not None and strict_digest(got) == strict
            except (_Unreadable, StoreInconsistent, Unsupported) as e:
                raise _VerifyFailed(f'{type(e).__name__}: {e}') from None
            if not ok_back:
                raise _VerifyFailed('다시 읽은 엄격 지문 ≠ 쓴 원장')
            del got                                                        # 대조용 사본 (원장만큼의 메모리) 을 발행 전에 놓는다
            os.chmod(tmp, 0o444)
            nbytes = os.path.getsize(tmp)
            #  ★ 11-12 2 회차 (RCP2-01) — 발행 직전 열쇠 코드 칸 다시 셈 ≠ 런 시작 → 발행 안 함 (짓는 · 쓰는 도중 바뀜 · 짓기가 바뀐 판을 불렀을 수 있다 ·
            #    임시 파일 = 아래 finally 가 지운다)
            _dr = code_drift()
            if _dr:
                return 'built_write_skipped', (f'{CODE_CHANGED}: 발행 직전 다시 센 열쇠 코드 칸 ≠ 런 시작 ({"; ".join(_dr)}) — 저장 안 함 · '
                                               f'런 도중 코드 바뀜'), None
            try:
                _link(tmp, final)
            except FileExistsError:
                os.unlink(tmp)
                made = False
                try:
                    peer = self._read(final, key, sid)
                except _Unreadable as e:
                    return 'built_write_failed', f'같은 열쇠를 남이 먼저 씀 · 그 파일 못 읽음 ({e})', None
                if peer is None:
                    return 'built_write_failed', '같은 열쇠 EEXIST 뒤 파일 없음', None
                if strict_digest(peer) != strict:
                    raise StoreInconsistent('peer_differs', '같은 열쇠를 남이 먼저 썼는데 원장이 다르다 (같은 입력 두 원장 = 비결정 또는 열쇠 결함)',
                                            final)
                return 'built_peer_same', None, None
            made = False                                                   # 발행됨 — 아래 정리가 실패해도 최종 파일은 그대로다
            try:
                os.unlink(tmp)
                dfd = os.open(self.root, os.O_RDONLY)
                try:
                    os.fsync(dfd)
                finally:
                    os.close(dfd)
            except OSError:
                pass
            return 'built_written', None, nbytes
        except StoreInconsistent:
            raise
        except _VerifyFailed as e:
            return 'built_write_failed', f'발행 전 대조 ({e})', None
        except OSError as e:
            return 'built_write_failed', f'{_errname(e)} ({type(e).__name__})', None
        finally:
            if made:
                try:
                    os.unlink(tmp)
                except OSError:
                    pass

    def get_or_build(self, build, *, sid, lo, vox, pts, phase, fid, kind, thresholds):
        """→ (원장, 기록).  build() = 원장 짓기 (예외는 그대로).  기록 칸 = status · key · file · why · seconds_read · seconds_build ·
        seconds_write · bytes.
        ★ 저장 쪽 (엄격 지문 · 싣기 · 쓰기 · 발행 전 대조) 의 오류는 팔 결과와 무관하다 — 뜻밖의 예외도 기록만 (built_write_failed) 하고 새로
          지은 원장을 돌려준다.  올리는 예외 = 짓기 (build) 의 것 · 어긋난 저장본 (StoreInconsistent) · 읽는 중 메모리 부족."""
        out = {'status': None, 'key': None, 'file': None, 'why': None, 'seconds_read': None, 'seconds_build': None, 'seconds_write': None,
               'bytes': None}

        def built():
            t0 = time.time()
            r = build()
            out['seconds_build'] = round(time.time() - t0, 3)
            return r
        if self.machine is None:
            out.update(status='disabled', why='기계 id 를 못 읽었다 (/etc/machine-id) — 저장본 꺼짐 · 매번 짓기')
            return built(), out
        #  ★ 11-12 2 회차 (내부 반박 리뷰 재확인 RCP2-01) — 런 시작 (이 모듈을 불러온 때) 뒤 열쇠 코드 파일이 바뀌었으면 이 런은 읽지도 쓰지도 않는다
        #    (불러온 코드 ↔ 열쇠의 코드 칸이 어긋날 수 있다 — 옛 판 = 옛 코드 원장을 새 코드 열쇠로 저장 → 뒤 런 적중 · 재리뷰 CE-A · 시험 T15)
        #  ★ 3 회차 (재확인 2 RCP3-02) — Store 의 열쇠 코드 칸 = 런 시작 코드 칸일 때만 읽고 쓴다 (변이판일 때 Store 를 만든 꼴 · 시험 T15h · T15k)
        _dr = code_drift()
        _sc = _START.get('code') or {}
        if not _dr and self.code != _sc:
            _dr = ['Store 열쇠 코드 칸 ≠ 런 시작 코드 칸 (' + ', '.join(sorted(b for b in set(self.code) | set(_sc) if self.code.get(b) != _sc.get(b))) + ')']
        if _dr:
            out.update(status='disabled', why=(f'{CODE_CHANGED}: 런 시작 (cjunc_store 를 불러온 때) 뒤 열쇠 코드 파일이 바뀌었다 ({"; ".join(_dr)}) — '
                                               f'이 런은 저장본을 읽지도 쓰지도 않는다 · 매번 짓기'))
            return built(), out
        try:
            parts = self.key_parts(sid=sid, lo=lo, vox=vox, pts=pts, phase=phase, fid=fid, kind=kind, thresholds=thresholds)
            key = self.key_of(parts)
        except Exception as e:                                 # noqa: BLE001 — 입력 오류 = 그냥 짓는다 (원장 함수가 옛 오류를 낸다)
            out.update(status='key_unavailable', why=f'{type(e).__name__}: {str(e)[:120]}')
            return built(), out
        out.update(key=key, file=file_name(key))
        path = self.path(key)
        t0 = time.time()
        try:
            got = self._read(path, key, sid)
        except _Unreadable as e:
            out['seconds_read'] = round(time.time() - t0, 3)
            out.update(status='unreadable_rebuilt', why=f'못 읽음 ({e}) — 파일 그대로 · 덮어쓰지 않음 · 운영자 확인')
            return built(), out
        out['seconds_read'] = round(time.time() - t0, 3)
        if got is not None:
            #  ★ 11-13 (Codex 반박 1/2 RCPX-01) — 적중을 돌려주기 직전 열쇠 코드 칸 다시 셈 ≠ 런 시작 → 저장본을 쓰지 않는다 (꺼짐 · 새로 짓기 · 쓰지도
            #    않는다).  옛 판 = 시작 검사 뒤 (열쇠 셈 · 파일 읽기 도중) 디스크 소스가 바뀌어도 적중으로 돌려줬다 (판정문 반례: 저장본 = 원판 원장 · 같은
            #    프로세스의 저장본 없는 재조립 = 새 판).  ⚠ 한정: 검사 한 번 더 = 경계 검사 — 이 줄과 반환 사이 · 그 뒤의 동시 변경을 원자적으로 막지
            #    않는다 (고정 소스 · 지원된 import 경로 전제 · 모듈 머리 한정 (가)–(마) 그대로)
            _dr = code_drift()
            if _dr:
                del got
                out.update(status='disabled', bytes=None,
                           why=(f'{CODE_CHANGED}: 적중 직전 다시 센 열쇠 코드 칸 ≠ 런 시작 ({"; ".join(_dr)}) — 저장본을 쓰지 않는다 · 새로 짓기 · '
                                f'런 도중 코드 바뀜'))
                return built(), out
            try:
                nb = os.path.getsize(path)
            except OSError:
                nb = None
            out.update(status='hit', bytes=nb)
            return got, out
        reg = built()
        t1 = time.time()
        try:
            strict, skel, arrays = encode_strict(reg)
        except Unsupported as e:
            out.update(status='built_write_skipped', why=f'unsupported: {e}')
            return reg, out
        except Exception as e:                                 # noqa: BLE001 — 저장 쪽 뜻밖의 오류 = 기록만 (팔 결과 무관)
            out.update(status='built_write_failed', why=f'싣기 {type(e).__name__}: {str(e)[:120]}')
            return reg, out
        try:
            st, why, nbytes = self._publish(key, reg, parts, strict, skel, arrays, out['seconds_build'] or 0.0, sid)
        except StoreInconsistent:
            raise
        except Exception as e:                                 # noqa: BLE001 — 같은 까닭 (메모리 부족 포함 · 임시 파일은 _publish 가 지웠다)
            st, why, nbytes = 'built_write_failed', f'{type(e).__name__}: {str(e)[:120]}', None
        out.update(status=st, why=why, bytes=nbytes, seconds_write=round(time.time() - t1, 3))
        return reg, out


def _read_members(path):
    """저장본 파일의 **그릇** 을 연다 → (머리 바이트, 뼈대 바이트, 배열 목록) · 없음 = None.
    못 읽음 (`_Unreadable` — 정직한 흐름 · 다시 짓는다) = CRC 로 확인한 멤버 바이트를 손에 넣기 전의 실패: lstat · 0 바이트 · zip 꼴 · 멤버
    집합 (머리 · 뼈대 · a0 … a<n−1> 정확히 한 번씩) · CRC.  어긋남 (`StoreInconsistent`) = 보통 파일이 아님 (심볼릭 링크 · 폴더 — 이 코드는 만들지
    않는다) · 파일 소유자 ≠ 이 사용자 · 그룹 · 남 쓰기 (★ 11-12 RCP-06) · CRC 를 지난 배열 멤버가 npy 로 읽히지 않음 · 뒤에 남는 바이트."""
    import stat as _stat
    try:
        st = os.lstat(path)
    except FileNotFoundError:
        return None
    except OSError as e:
        raise _Unreadable(f'lstat {_errname(e)}') from None
    if _stat.S_ISLNK(st.st_mode) or not _stat.S_ISREG(st.st_mode):
        raise StoreInconsistent('not_regular', '저장본 자리가 보통 파일이 아니다 (심볼릭 링크 · 폴더 — 이 코드는 만들지 않는다)', path)
    #  ★ 11-12 (내부 반박 리뷰 RCP-06) — 이 코드는 이 사용자 소유 · 그룹 · 남 쓰기 없는 파일만 만든다 (임시 0600 → 0444 → link) · 다른 소유자 (폴더가 0777
    #    이던 때 남이 넣은 파일) · 손으로 0666 이 된 파일 = 자기 일관이어도 받지 않는다 (멈춤).  링크 수는 보지 않는다 (발행 중 임시 이름 + 최종 이름 = 2 인
    #    순간을 다른 팔이 읽을 수 있다 — 정직한 흐름 · 한정).
    if hasattr(os, 'getuid') and st.st_uid != os.getuid():
        raise StoreInconsistent('file_owner', f'저장본 파일 소유자 ({st.st_uid}) ≠ 이 사용자 ({os.getuid()}) — 이 코드는 남의 파일을 만들지 않는다', path)
    if st.st_mode & 0o022:
        raise StoreInconsistent('file_mode', f'저장본 파일을 그룹 · 남이 쓸 수 있다 (모드 {oct(st.st_mode & 0o777)} — 이 코드는 0444 로 발행한다)', path)
    if st.st_size == 0:
        raise _Unreadable('0 바이트')
    try:
        with open(path, 'rb') as f:
            zf = zipfile.ZipFile(f)
            names = zf.namelist()
            n_arr = sum(1 for x in names if _ARRAY_MEMBER_RE.fullmatch(x))
            want = {HEADER_MEMBER, SKELETON_MEMBER} | {f'a{i}.npy' for i in range(n_arr)}
            if len(names) != len(want) or set(names) != want:
                raise _Unreadable(f'멤버 집합 ({len(names)} 개)')
            bad = zf.testzip()
            if bad is not None:
                raise _Unreadable(f'CRC ({bad})')
            hb = zf.read(HEADER_MEMBER)
            sb = zf.read(SKELETON_MEMBER)
            arrays = []
            for i in range(n_arr):                             # 여기부터는 CRC 를 지난 바이트 — npy 로 안 읽히면 어긋남
                with zf.open(f'a{i}.npy') as m:
                    try:
                        a = np.lib.format.read_array(m, allow_pickle=False)
                    except MemoryError:
                        raise
                    except Exception as e:                     # noqa: BLE001 — ★ 11-13 (Codex 반박 1/2 RCPX-04) CRC 뒤 배열 해석의 뜻밖의 예외 (머리 shape
                        #    (2**100,) = OverflowError 등 · 옛 = ValueError · OSError · EOFError 만 → 날 예외가 새었다) 도 어긋남 · MemoryError 만 그대로
                        raise StoreInconsistent('array', f'배열 멤버 a{i} ({type(e).__name__})', path) from None
                    if m.read(1):
                        raise StoreInconsistent('array', f'배열 멤버 a{i} 뒤 남는 바이트', path)
                arrays.append(a)
    except (StoreInconsistent, _Unreadable):
        raise
    except (zipfile.BadZipFile, zipfile.LargeZipFile, OSError, EOFError, ValueError, KeyError, struct.error, NotImplementedError,
            RuntimeError) as e:
        raise _Unreadable(f'zip ({type(e).__name__})') from None
    return hb, sb, arrays


def _write_zip(f, header_bytes, skel_bytes, arrays):
    """임시 파일에 zip (STORED · 멤버 차례 = 머리 · 뼈대 · a0 …) — 시험 고리 (모듈 전역)."""
    with zipfile.ZipFile(f, 'w', zipfile.ZIP_STORED, allowZip64=True) as z:
        z.writestr(zipfile.ZipInfo(HEADER_MEMBER, date_time=(1980, 1, 1, 0, 0, 0)), header_bytes)
        z.writestr(zipfile.ZipInfo(SKELETON_MEMBER, date_time=(1980, 1, 1, 0, 0, 0)), skel_bytes)
        for i, a in enumerate(arrays):
            zi = zipfile.ZipInfo(f'a{i}.npy', date_time=(1980, 1, 1, 0, 0, 0))
            with z.open(zi, 'w', force_zip64=True) as m:
                np.lib.format.write_array(m, a, allow_pickle=False)


# ═════════════════════════ 실행 환경 기록 · 팔 audit 기록 (★ 11-13 · 1저자 "권고대로" Q2 · Codex 반박 1/2 §3 RCP-07) ═════════════════════════
#: 실행 환경 기록의 env 이름 — 원장 길의 BLAS 계산 경로 (OPENBLAS_CORETYPE) · numpy SIMD 선택 (NPY_DISABLE · ENABLE_CPU_FEATURES) · 스레드 수.  **기록만**
#  (열쇠 아님 · 읽을 때 대조 안 함) — 같은 기계 · venv 에서 이 값을 R 동안 바꾸지 않는다는 계약의 대조 자료 (묶음 README · 판정문 Q2).
RUNTIME_ENV_NAMES = ('OPENBLAS_CORETYPE', 'NPY_DISABLE_CPU_FEATURES', 'NPY_ENABLE_CPU_FEATURES', 'OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS',
                     'MKL_NUM_THREADS', 'BLIS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS')
#: 팔 audit 기록 (과학 payload 밖 곁 파일 · 사슬 요약 팔별 표시) — 꼴 판 · 곁 파일 이름 앞자리 (`p2_` 아님 = 팔 · 결과 흔적 낱말과 겹치지 않는다) · 칸
AUDIT_SCHEMA = 'cjstore-audit-v1'
AUDIT_PREFIX = 'cjstore_audit_'
AUDIT_KEYS = ('schema', 'status', 'key', 'file', 'file_sha256', 'why', 'seconds_read', 'seconds_build', 'seconds_write', 'bytes', 'runtime')
#: 파일 sha256 을 싣는 상태 (그 파일을 읽었거나 · 썼거나 · 남이 쓴 같은 원장 · 못 읽은 파일의 신원) — 꺼짐 · 쓰기 실패 · 열쇠 못 셈 = None
_AUDIT_FILE_STATUSES = ('hit', 'built_written', 'built_peer_same', 'unreadable_rebuilt')


def runtime_record():
    """이 프로세스의 실행 환경 기록 → {python · numpy · scipy · env {이름: 값 | None} · numpy_simd {features · baseline · dispatch} | None}.
    열쇠 칸이 아니다 (판 글자 · 자리 지문은 열쇠의 env 칸 · 이것은 그 밖의 BLAS · SIMD · 스레드 선택) — 저장본 머리 (비권위 진단) · 팔 audit 기록에 싣는다.
    ⚠ SIMD 칸 = numpy 가 고른 기능 목록 (CPU 모델 이름 하나로 산술 결정성이 증명되지 않는다 · 판정문 Q2) · BLAS 의 실제 코어 선택은 OPENBLAS_CORETYPE 이
    없으면 기록되지 않는다 (사슬 `env_record` 의 threadpoolctl 칸이 그 몫 · 이 함수는 새 프로세스를 띄우지 않는다)."""
    import importlib
    import sys
    import scipy
    simd = None
    for nm in ('numpy._core._multiarray_umath', 'numpy.core._multiarray_umath'):
        try:
            mod = importlib.import_module(nm)
        except Exception:                                      # noqa: BLE001 — 기록 칸 (못 읽음 = None)
            continue
        feats = getattr(mod, '__cpu_features__', None)
        if isinstance(feats, dict):
            simd = {'features': sorted(str(k) for k, v in feats.items() if v),
                    'baseline': [str(x) for x in (getattr(mod, '__cpu_baseline__', ()) or ())],
                    'dispatch': [str(x) for x in (getattr(mod, '__cpu_dispatch__', ()) or ())]}
            break
    return {'python': '%d.%d.%d' % tuple(sys.version_info[:3]), 'numpy': str(np.__version__), 'scipy': str(scipy.__version__),
            'env': {k: os.environ.get(k) for k in RUNTIME_ENV_NAMES}, 'numpy_simd': simd}


def audit_record(out, root=None):
    """`Store.get_or_build` 기록 → 팔 audit 기록 (칸 = `AUDIT_KEYS` · 과학 payload 밖 · 판정 무관).  file_sha256 = 저장본 파일 (root 아래 · 보통 파일) 의
    sha256 — 그 파일을 읽었거나 썼거나 (`_AUDIT_FILE_STATUSES`) 일 때만 · runtime = `runtime_record` (지금 프로세스)."""
    import stat as _stat
    o = out if isinstance(out, dict) else {}
    fn = o.get('file')
    fsha = None
    if root and o.get('status') in _AUDIT_FILE_STATUSES and isinstance(fn, str) and FILE_RE.fullmatch(fn):
        p = os.path.join(root, fn)
        try:
            if _stat.S_ISREG(os.lstat(p).st_mode):
                fsha = _file_sha(p)
        except OSError:
            fsha = None
    rec = {k: o.get(k) for k in ('status', 'key', 'file', 'why', 'seconds_read', 'seconds_build', 'seconds_write', 'bytes')}
    rec.update(schema=AUDIT_SCHEMA, file_sha256=fsha, runtime=runtime_record())
    return {k: rec[k] for k in AUDIT_KEYS}


def audit_path(out_path):
    """팔 출력 경로 → 곁 파일 경로 (같은 폴더 · `cjstore_audit_<출력 이름>` — 러너가 팔과 함께 OUTDIR 로 옮긴다 · 사슬이 읽는다)."""
    return os.path.join(os.path.dirname(out_path), AUDIT_PREFIX + os.path.basename(out_path))


class AuditSupersessionError(OSError):
    """Previous audit could not be retired; publishing a new arm must stop."""


def write_audit(out_path, rec):
    """Retire old audit before constructing/writing this attempt's record.

    rec may be a lazy zero-argument builder. An old record is preserved in a
    unique sibling; failure to retire it is fatal, other I/O failures leave no
    previous canonical record to be collected as this attempt's audit.
    The containing run directory must remain unchanged by other processes.
    """
    import uuid
    p = audit_path(out_path)
    try:
        try:
            os.lstat(p)
            exists = True
        except FileNotFoundError:
            exists = False
        if exists:
            previous = p + '.previous.' + uuid.uuid4().hex
            os.rename(p, previous)
    except OSError as exc:
        raise AuditSupersessionError('cannot retire previous arm audit') from exc
    if callable(rec):
        rec = rec()
    part = p + '.part'
    with open(part, 'w', encoding='utf-8') as f:
        json.dump(rec, f, ensure_ascii=False, sort_keys=True, indent=1)
        f.write('\n')
    os.replace(part, p)
    return p


def outcome_line(out):
    """payload 화면 한 줄 — 정상 셋 = probe6 실패 낱말 없음 · 경고 다섯 = ⚠ (사유 글)."""
    st = out.get('status')
    k = str(out.get('key') or '')[:12] or '—'

    def s(x):
        return '—' if x is None else f'{float(x):.0f}s'
    mb = '—' if out.get('bytes') is None else f'{int(out["bytes"]) / 1e6:.1f} MB'
    head = '  STEP3: S2 탄소 접합 원장 저장본 — '
    if st == 'hit':
        return f'{head}읽음 (열쇠 {k} · 지문 대조 통과 · 읽기 {s(out.get("seconds_read"))} · {mb} · 원장을 다시 짓지 않음)'
    if st == 'built_written':
        return f'{head}새로 지어 저장 (열쇠 {k} · 짓기 {s(out.get("seconds_build"))} · 쓰기 {s(out.get("seconds_write"))} · {mb})'
    if st == 'built_peer_same':
        return f'{head}새로 지음 · 같은 열쇠를 다른 런이 먼저 저장 (원장 엄격 지문 같음 · 열쇠 {k} · 짓기 {s(out.get("seconds_build"))})'
    why = out.get('why') or '—'
    if st == 'unreadable_rebuilt':
        return f'  STEP3: ⚠ S2 탄소 접합 원장 저장본 — {why} · 새로 지음 (열쇠 {k})'
    if st in ('built_write_skipped', 'built_write_failed'):
        return f'  STEP3: ⚠ S2 탄소 접합 원장 저장본 — 새로 지음 · 저장 안 함 ({why} · 열쇠 {k})'
    return f'  STEP3: ⚠ S2 탄소 접합 원장 저장본 — 꺼짐 ({why}) · 새로 지음'
