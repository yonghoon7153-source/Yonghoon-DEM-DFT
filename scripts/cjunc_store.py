#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② Q2 (1저자 11-12) — 탄소 접합 원장 (기하) **저장본**: 한 번 지어 저장하고 다음 팔이 지문을 대조해 읽는다.

왜: 원장 (`carbon_junction.cjunc_registry`) 은 침대 · 격자 · origin · 문턱 · 코드 · 환경에만 달리고 R_j · 법칙 · c · SV 노브에는 달리지 않는다
(`docs/reviews/rint2_time_reestimate_20261111/README.md` A-2 · E-2 4 번) — ⑥ 실측 팔 하나의 준비 4,567 s 가운데 4,040 s.  계획 (R_j · 법칙 · c · SV)
은 팔마다 그대로 다시 만든다 (`ca_ext_cjunc.payload_prepare`).  산출 바이트 (팔 JSON · 매니페스트 · 영수증 · 이름) 는 끔과 같다 — 결과 = 화면 한 줄뿐.

열쇠 (`Store.key_parts` → sha256) = 꼴 판 · 모델 판 · 스키마 · 코드 파일 sha256 (`carbon_junction.py` · `step3_sigma.py` · 이 파일) · 환경 같음 단위
(`run_contract.env_unit_now` = python 부 판 · numpy · scipy) · 기계 지문 (`/etc/machine-id` blake2b — 못 읽으면 저장본 꺼짐 = 매번 짓기) · sid 격자 지문 ·
lo · vox (실수 비트) · 입력 넷 (`carbon_junction._input_check` 의 정준 float64 · int64 값) · 문턱 칸 (이름 · 형 · 비트).

파일 = `<폴더>/cjreg_<열쇠>.npz` (zip · STORED · 멤버 = header.json · skeleton.json (형 표지 트리) · a<i>.npy (배열 · `allow_pickle=False`)) ·
0444 · 단일 작성자 (임시 파일 O_EXCL 0600 → fsync → 읽어 대조 → chmod 0444 → `os.link` (먼저 쓴 쪽이 이김 · 덮어쓰기 없음) → 폴더 fsync).

읽기 처분 (CLAUDE.md "재개 규칙 지적 처분 기준" 꼴):
  · 없음 → 짓고 쓴다 (built_written · 같은 열쇠를 남이 먼저 쓰면 그 파일을 읽어 엄격 지문 대조 = built_peer_same · 다르면 멈춤)
  · **못 읽음** (CRC 로 확인한 멤버 바이트를 손에 넣기 전의 실패 — 0 바이트 · zip 꼴 · 멤버 집합 · CRC) = 정직한 흐름 (끊긴 복사 · 디스크) →
    다시 짓는다 · 그 파일은 두고 덮어쓰지 않는다 · ⚠ 줄 (unreadable_rebuilt · 운영자가 지운다)
  · **어긋남** (그 뒤 — 머리 JSON · 꼴 판 · 열쇠 · 뼈대 sha · 복원 · 엄격 지문 · registry_fp · sid 지문 · 심볼릭 링크 · 폴더) = 손으로 고친 · 서로
    어긋난 기록 → **멈춤** (`StoreInconsistent` → payload `S2_CJUNC_STORE|INCONSISTENT|` · rc ≠ 0)
  · 쓰기 실패 (자리 · 권한 · link 미지원) = 기록만 (팔 결과 무관 · 늘 새로 지은 원장을 쓴다)
비트 같음 보증 = 엄격 지문 (노드마다 형 · dtype · 모양 · C/F · 바이트 · dict 키 차례 · **별칭 구조**) 을 쓰는 쪽이 짓자마자 세어 머리에 적고, 읽는
쪽이 복원한 원장을 같은 함수로 세어 같아야 쓴다 · `registry_fp` 다시 셈 = 기록 · 쓰는 쪽은 발행 전에 임시 파일을 같은 읽기 길로 다시 읽어 대조한다.
별칭 = 같은 변하는 객체 (ndarray · dict · list) 가 두 자리 이상에 — 되가리킴 노드로 싣고 복원본도 같은 객체를 그 자리들에 둔다 (원장의
`instances.pair_i` · `pair_j` = `[빈 배열] * instance 수` — instance 가 둘 이상인 원장은 늘 별칭이 있다 · `carbon_junction._merge_instances`).  서로
다른 배열 객체가 메모리를 나눠 쓰는 꼴 (보기 · 조각) 은 받지 않는다 (저장 안 함).  규모: 실침대 원장 = instance 십수만 × 작은 배열 넷 (약 47 만
멤버 · zip64) — 겹침 검사는 주소 구간 정렬 (배열 수 n 에 n log n).
⚠ 한정: 같은 열쇠 이름 아래 **자기 일관 위조** (내용 · 머리 · 지문을 모두 다시 센 파일) 는 저장본 혼자 가리지 못한다 — 그 몫 = 봉인 원천 재조립 대조
(`rint_r_chain.RunnerGraphSource` · 저장본을 읽지 않는다) · 폴더 권한 (소유자 = 이 사용자 · 그룹 · 남 쓰기 없음 · 파일 0444).
⚠ Python 3.8 (kgy) 에서 돈다 — 3.9+ 문법 · 새 라이브러리 함수 없음.
"""
import errno
import hashlib
import json
import os
import re
import secrets
import socket
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
#: 원장 코드 = 이 파일들의 바이트 (열쇠 칸) — 원장 함수 · 격자 지문 함수 · 이 직렬화기
CODE_MODULES = ('carbon_junction', 'step3_sigma', 'cjunc_store')
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
    """저장본 폴더 하나 (절대 경로 · 있는 폴더 · 소유자 = 이 사용자 · 그룹 · 남 쓰기 없음).  열쇠의 코드 · 환경 · 기계 칸은 만들 때 한 번 읽는다."""

    def __init__(self, root, machine_paths=MACHINE_ID_PATHS):
        if not isinstance(root, str) or not os.path.isabs(root):
            raise ValueError(f'저장본 폴더 = 절대 경로 ({root!r})')
        try:
            st = os.stat(root)
        except OSError as e:
            raise ValueError(f'저장본 폴더가 없다 ({root} · {_errname(e)})') from None
        import stat as _stat
        if not _stat.S_ISDIR(st.st_mode):
            raise ValueError(f'저장본 자리가 폴더가 아니다 ({root})')
        if st.st_mode & 0o022:
            raise ValueError(f'저장본 폴더를 그룹 · 남이 쓸 수 있다 (모드 {oct(st.st_mode & 0o777)} · 단일 작성자 · umask 022 셸에서 만든다)')
        if hasattr(os, 'getuid') and st.st_uid != os.getuid():
            raise ValueError(f'저장본 폴더 소유자 ({st.st_uid}) ≠ 이 사용자 ({os.getuid()})')
        self.root = root
        import importlib
        import run_contract as RC
        self.code = {}
        for m in CODE_MODULES:
            mod = importlib.import_module(m)
            self.code[os.path.basename(mod.__file__)] = _file_sha(mod.__file__)
        self.env = RC.env_unit_now()
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
        header = {'format': STORE_FORMAT, 'kind': STORE_KIND, 'key': key, 'key_parts': parts,
                  'skeleton_sha256': hashlib.sha256(skel).hexdigest(), 'n_arrays': len(arrays), 'strict': strict,
                  'registry_fp': reg['fp']['registry'],
                  'writer': {'host': socket.gethostname(), 'pid': os.getpid(), 'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                             'build_seconds': round(float(build_s), 3)}}
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
    않는다) · CRC 를 지난 배열 멤버가 npy 로 읽히지 않음 · 뒤에 남는 바이트."""
    import stat as _stat
    try:
        st = os.lstat(path)
    except FileNotFoundError:
        return None
    except OSError as e:
        raise _Unreadable(f'lstat {_errname(e)}') from None
    if _stat.S_ISLNK(st.st_mode) or not _stat.S_ISREG(st.st_mode):
        raise StoreInconsistent('not_regular', '저장본 자리가 보통 파일이 아니다 (심볼릭 링크 · 폴더 — 이 코드는 만들지 않는다)', path)
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
                    except (ValueError, OSError, EOFError) as e:
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
