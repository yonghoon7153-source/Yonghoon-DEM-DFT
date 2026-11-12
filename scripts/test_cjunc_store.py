#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② Q2 (1저자 11-12) — 탄소 접합 원장 저장본 (`scripts/cjunc_store.py`) · 시험 먼저 (규율 ② · CPU · GPU · 킷 없음).

정본 = 묶음 설계 메모 (본 세션 scratch `rint/codepkg/design.md` (나)) · 근거 표 = `docs/reviews/rint2_time_reestimate_20261111/README.md` A-2 · E-2 4 번.
원장 (기하 · `carbon_junction.cjunc_registry`) 은 R_j · 법칙 · c 에 달리지 않는다 → 같은 침대 · 격자 · origin · 문턱 · 코드 · 환경 · 기계면 한 번 지어
저장하고 다음 팔이 **지문을 대조해** 읽는다.  계획 (R_j · 법칙 · c · SV) 은 팔마다 그대로 다시 만든다.

묶음:
  T0  모듈 · API (고치기 전 = 모듈 없음)
  T1  왕복 (메모리) — 원장 픽스처 넷 + 형 모둠 (dict 키 차례 · list/tuple · Python/numpy 스칼라 형 · −0 · NaN 비트 · 큰 정수 · 외톨이 대리 ·
      C/F 차례 · 바이트 차례 · 0 차원 · 빈 배열 · 객체 배열) → 시험 쪽 독립 비교 (형 · dtype · 모양 · 차례 표지 · 바이트) · 엄격 지문 · registry_fp
  T2  엄격 지문 판별력 — 형 · 차례 · 바이트 차례 · 부호 있는 0 · 키 형 하나씩 다르면 다른 지문
  T3  받지 않는 꼴 (별칭 · 메모리 겹침 · 비연속 · 읽기 전용 · 구조체 · dict 하위형 · 집합 · 모르는 객체) = Unsupported · 저장 안 함 (팔 결과 그대로)
  T4  열쇠 결속 — 침대 (sid 한 칸 · dtype) · lo · vox (1 ulp) · 점 (1 ulp) · phase · fid · kind · 문턱 열 칸 · 코드 · 환경 · 기계 · 모델 판 · 꼴 판
  T5  흐름 — 없음 → 짓고 씀 (0444 · 이름 · 임시 파일 없음) → 새 Store 적중 (짓기 0 회) · 읽은 원장 = 지은 원장 (비트) · 계획 · 풀이 σ 비트 같음 ·
      payload_prepare 끔 / 빗나감 / 적중 같음 (끔 = 'store' 칸 없음) · 화면 줄 (probe6 실패 낱말 없음)
  T6  못 읽음 (정직한 흐름 = 다시 짓는다 · 파일 그대로 · 덮어쓰지 않음 · ⚠ 줄) — 0 바이트 · 잘림 · 배열 · 뼈대 한 바이트 (CRC) · 중앙 목록 한 바이트 ·
      멤버 빠짐 · 같은 이름 둘
  T7  어긋남 (손으로 고친 · 어긋난 기록 = 멈춤 StoreInconsistent · 짓지 않음 · 파일 그대로) — 다른 열쇠 파일 이름 바꿈 · 뼈대 바꿔 끼움 · 머리
      엄격 지문 · 배열 바꿈 · 배열 + 엄격 지문 다시 셈 (registry_fp) · sid 지문 · 머리 JSON · 꼴 판 · 심볼릭 링크 · 폴더
  T8  다른 침대 · 문턱 · 코드 · 기계의 저장본 = 열쇠가 달라 읽지 않음 → 새로 짓고 씀 (옛 파일 그대로)
  T9  같은 열쇠 동시 쓰기 — 남이 같은 원장 = peer_same · 남이 다른 원장 = 멈춤 · 실제 프로세스 둘 경주 = written 하나 + peer_same 하나 · 파일 하나
  T10 끊김 (PID 이름공간 `unshare -pf --mount-proc --kill-child` 안에서만 · kill = 직접 만든 자식) — 쓰는 도중 (임시 파일 뒤 · link 전) · 읽는 도중
  T11 쓰기 실패 · 끔 — 디스크 여유 · link EPERM · 쓰는 중 ENOSPC · 기계 id 못 읽음 · 폴더 꼴 (상대 · 없음 · 파일 · 남이 쓸 수 있음) · 입력 오류 = 옛 오류
  P   payload 끝-끝 (`test_ca_ext_b6` 픽스처 · 실제 payload · CPU) — 입구 거부 넷 · 끔 / 빗나감 / 적중 팔 JSON 바이트 같음 · 못 읽음 (⚠ · 같음) ·
      어긋남 (rc ≠ 0 · S2_CJUNC_STORE|INCONSISTENT| · 출력 없음)
  R   러너 (`test_ca_ext_runner` 틀 · 실제 셸 · 실제 payload) — CJUNC=1 없이 · 조립만과 함께 · 상대 · 허용 밖 글자 · 개행 · 없는 폴더 = 발사 전 ABORT ·
      켬 = payload 인자 · 팔 JSON · 영수증 · OUTDIR = 끔과 같음 · 둘째 런 = 적중
  C   사슬 배선 — `--cjunc-store` (ladder · predict 만 · 절대 · 있는 폴더 · 남이 못 씀) · Runner env · 봉인 원천 (RunnerGraphSource) 은 절대 안 받음 ·
      부모 셸 값은 지운다 · CODE_FILES · 규율 검사기 격리 목록 · CLI 회계
⚠ PASS = 저장 · 읽기 · 거부 배선이 계약대로라는 증거이지 원장 (기하) 의 물리 검증이 아니다.  저장본 자신은 **자기 일관 위조** (같은 열쇠 이름 ·
   다시 센 지문) 를 가리지 못한다 — 그 몫 = 봉인 원천 재조립 대조 (판정 단계 · 저장본을 읽지 않는다) · 한정 (T7 보고 줄).

  python3 scripts/test_cjunc_store.py                 # 전부 (CPU · 몇 분 — P · R 는 실제 payload · 러너)
  python3 scripts/test_cjunc_store.py --only T,C      # 이름 접두로 고르기 (빠른 묶음)
"""
import argparse
import contextlib
import errno
import glob
import importlib.util
import io
import json
import os
import shutil
import signal
import stat
import struct
import subprocess
import sys
import tempfile
import time
import zipfile

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, 'scripts')
sys.path.insert(0, SCRIPTS)

import carbon_junction as CJ                               # noqa: E402
import step3_sigma as S3                                   # noqa: E402
import ca_ext_cjunc as CW                                  # noqa: E402
import test_carbon_junction as TC                          # noqa: E402 — 원장 픽스처 (사본 없음)

try:
    import cjunc_store as CS                               # noqa: E402
    CS_ERR = None
except ImportError as _e:                                  # 고치기 전 판 = 모듈 없음 (시험 단위로 실패를 기록한다)
    CS, CS_ERR = None, _e

TC.S3, TC.CJ = S3, CJ
PROBE6_READ = os.path.join(ROOT, 'docs', 'reviews', 'rint2_probe6_prep_20261110', 'tools', 'probe6_read.py')
REQ = dict(R_j_ohm=1.0e6, len_law='len_scaled_v0', unreg_law='cut', s_min_um=0.5, tol_ff_um=0.3, ptfe_jlaw='P0')

ARGS = None
TD = None
_ok, _fail = 0, []
CASES = []


def chk(name, cond, why=''):
    global _ok
    cond = bool(cond)
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'  ({str(why)[:500]})' if why != '' else ''))
    return cond


def case(tag):
    def deco(fn):
        CASES.append((tag, fn))
        return fn
    return deco


def quiet(fn, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*a, **k)


def need_cs(tag):
    if CS is None:
        chk(f'{tag} cjunc_store 모듈이 있다', False, f'고치기 전 판 — {CS_ERR}')
        return False
    return True


# ═════════════════════════ 시험 쪽 독립 비교 (모듈의 엄격 지문을 쓰지 않는다) ═════════════════════════
def deep_diff(a, b, path='$'):
    """같으면 None · 다르면 첫 차이 자리 (형 · dict 키 차례 · 배열 dtype · 모양 · C/F 표지 · 바이트 · 실수 비트)."""
    if type(a) is not type(b):
        return f'{path}: 형 {type(a).__name__} ≠ {type(b).__name__}'
    if isinstance(a, np.ndarray):
        if a.dtype.str != b.dtype.str or a.shape != b.shape:
            return f'{path}: dtype/모양 {a.dtype.str}{a.shape} ≠ {b.dtype.str}{b.shape}'
        if (a.flags.c_contiguous, a.flags.f_contiguous) != (b.flags.c_contiguous, b.flags.f_contiguous):
            return f'{path}: 차례 표지'
        if a.dtype.hasobject:
            for i, (x, y) in enumerate(zip(a.reshape(-1, order='C'), b.reshape(-1, order='C'))):
                r = deep_diff(x, y, f'{path}[{i}]')
                if r:
                    return r
            return None
        return None if np.ascontiguousarray(a).tobytes() == np.ascontiguousarray(b).tobytes() else f'{path}: 바이트'
    if isinstance(a, np.generic):
        return None if (a.dtype.str == b.dtype.str and a.tobytes() == b.tobytes()) else f'{path}: numpy 스칼라 {a!r} ≠ {b!r}'
    if isinstance(a, dict):
        if list(a) != list(b):
            return f'{path}: 키 차례 {list(a)[:5]} ≠ {list(b)[:5]}'
        for k in a:
            r = deep_diff(a[k], b[k], f'{path}.{k}')
            if r:
                return r
        return None
    if isinstance(a, (list, tuple)):
        if len(a) != len(b):
            return f'{path}: 길이 {len(a)} ≠ {len(b)}'
        for i, (x, y) in enumerate(zip(a, b)):
            r = deep_diff(x, y, f'{path}[{i}]')
            if r:
                return r
        return None
    if isinstance(a, float):
        return None if struct.pack('>d', a) == struct.pack('>d', b) else f'{path}: 실수 비트 {a!r} ≠ {b!r}'
    return None if a == b else f'{path}: 값 {a!r} ≠ {b!r}'


# ═════════════════════════ 픽스처 ═════════════════════════
def f1_inputs(sdcp=True):
    """test_carbon_junction F1 (직렬 사슬 · 관통 · SDCP 근접 하나) → (입력 dict, 짓기 함수) · 문턱 = 시험 값."""
    parts = [TC.rows(TC.F1)]
    if sdcp:
        parts.append(TC.rows([[(1.5, 2.5, 3.5)]], phase=5, kind=0, fid0=700))
    P, PH, F, K = TC.cat_rows(*parts)
    sid, _ = TC.bed((P, PH, F, K), TC.F1_N)
    thr = TC.reg_kw(dict(r_f_um=TC.RF, tol_ff_um=TC.TOL, L_par_um=TC.LPAR, r_port_um=TC.RPORT, gap_tol=2.0, s_min_um=TC.S_MIN,
                         tol_sj_um=0.5, r_sdcp_um=0.5))
    return dict(sid=sid, lo=(0.0, 0.0, 0.0), vox=float(TC.H), pts=P, phase=PH, fid=F, kind=K, thresholds=dict(thr))


def rand_inputs(seed):
    """test_carbon_junction `_random_bed` (VGCF · PTFE · SDCP · vox 0.25) — rasterize 인자를 잡아 원장 입력으로."""
    cap = {}
    orig = S3.rasterize

    def rr(*a, **k):
        cap.update(P=a[3], PH=a[4], F=k['add_fid'], K=k['add_kind'])
        return orig(*a, **k)
    S3.rasterize = rr
    try:
        sid, _pid, _box = TC._random_bed(seed, S3)
    finally:
        S3.rasterize = orig
    thr = CW.registry_thresholds(s_min_um=REQ['s_min_um'], tol_ff_um=REQ['tol_ff_um'])
    return dict(sid=sid, lo=(0.0, 0.0, 0.0), vox=0.25, pts=cap['P'], phase=cap['PH'], fid=cap['F'], kind=cap['K'], thresholds=thr)


def build_of(inp, counter=None):
    def build():
        if counter is not None:
            counter[0] += 1
        return quiet(CJ.cjunc_registry, inp['sid'], inp['lo'], inp['vox'], inp['pts'], inp['phase'], inp['fid'], inp['kind'],
                     **inp['thresholds'])
    return build


def kinds_object():
    """형 모둠 (원장에 지금 없는 형도 — 직렬화기가 형을 잃지 않는지)."""
    nan_payload = struct.unpack('>d', bytes.fromhex('7ff8000000000123'))[0]
    objarr = np.empty(4, dtype=object)
    objarr[:] = ['p', None, 3, 2.5]
    obj2 = np.empty((2, 2), dtype=object)
    obj2[0, 0], obj2[0, 1], obj2[1, 0], obj2[1, 1] = ('t', 1), [1, 'x'], {'k': -0.0}, b'\x00\xff'
    return {'scal': [1, -2 ** 100, 2.5, -0.0, nan_payload, float('inf'), True, False, None, 'x', 'é\ud800', b'\x00\xff', (1, 2), [], {}],
            7: 'int 키', 'z_first': 1, 'a_second': 2,
            'np': [np.float32(1.5), np.float64(-0.0), np.int16(-3), np.int64(2 ** 62), np.uint8(255), np.bool_(True), np.str_('ab'),
                   np.bytes_(b'q'), np.datetime64('2026-11-12', 'D'), np.complex128(1 - 2j)],
            'arr': [np.arange(6, dtype='<i4').reshape(2, 3), np.asfortranarray(np.arange(6.0).reshape(2, 3)), np.zeros(0), np.array(5),
                    np.array([1.0, -0.0], dtype='>f8'), np.array([True, False]), np.array(['a', 'bc']), np.array([b'x', b'yz']),
                    np.array(['2026-01-01'], dtype='M8[D]'), np.zeros((0, 3), np.int64), np.arange(24, dtype=np.int8).reshape(2, 3, 4)],
            'obj': objarr, 'obj2': obj2, 'nested': {'d': {'e': [np.arange(3), (np.float64(1.0),)]}}}


def new_store_dir(name):
    d = os.path.join(TD, 'stores', name)
    os.makedirs(d)
    os.chmod(d, 0o755)
    return d


def store_files(d):
    return sorted(os.listdir(d))


def finger(p):
    st = os.lstat(p)
    with open(p, 'rb') as f:
        data = f.read()
    return (st.st_ino, st.st_mtime_ns, stat.S_IMODE(st.st_mode), len(data), hash(data))


def machine_file(name, text):
    p = os.path.join(TD, f'machine_{name}')
    with open(p, 'w', encoding='ascii') as f:
        f.write(text + '\n')
    return p


def mk_store(d, mach='A'):
    return CS.Store(d, machine_paths=(machine_file(mach, ('%032x' % (abs(hash(mach)) % (16 ** 32)))),))


def write_one(d, inp, mach='A'):
    """저장본 하나 쓰기 → (경로, 원장)."""
    st = mk_store(d, mach)
    reg, out = st.get_or_build(build_of(inp), **inp)
    assert out['status'] == 'built_written', out
    return os.path.join(d, out['file']), reg, out


def writable(p):
    os.chmod(p, 0o644)


def ro(p):
    os.chmod(p, 0o444)


def rezip(src, dst, edit=None, extra=()):
    """zip 멤버를 읽어 (원 차례) edit(name, data) → 새 data (None = 뺌) 로 새 zip (CRC 새로 · STORED) — 손으로 고친 꼴."""
    with zipfile.ZipFile(src) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    tmp = dst + '.rz'
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_STORED) as z:
        for nm, data in items:
            nd = data if edit is None else edit(nm, data)
            if nd is not None:
                z.writestr(nm, nd)
        for nm, data in extra:
            z.writestr(nm, data)
    if os.path.exists(dst):
        writable(dst)
    os.replace(tmp, dst)
    ro(dst)


def member_data_offset(p, name):
    with zipfile.ZipFile(p) as z:
        info = z.getinfo(name)
    with open(p, 'rb') as f:
        f.seek(info.header_offset)
        h = f.read(30)
    n_name, n_extra = struct.unpack('<HH', h[26:30])
    return info.header_offset + 30 + n_name + n_extra, info.file_size


def flip_byte(p, off):
    writable(p)
    with open(p, 'r+b') as f:
        f.seek(off)
        b = f.read(1)
        f.seek(off)
        f.write(bytes([b[0] ^ 0x5A]))
    ro(p)


def load_fail_mark():
    spec = importlib.util.spec_from_file_location('probe6_read_t', PROBE6_READ)
    m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(m)
    return m.FAIL_MARK


def raises_inconsistent(fn):
    """→ (멈춤 예외였나, 예외 글)."""
    try:
        fn()
    except Exception as e:                                 # noqa: BLE001
        return (CS is not None and isinstance(e, CS.StoreInconsistent)), f'{type(e).__name__}: {e}'
    return False, '예외 없음'


# ═════════════════════════ T0 ═════════════════════════
@case('T0 모듈 · API')
def t0():
    if not need_cs('T0'):
        return
    names = ('STORE_FORMAT', 'Store', 'StoreInconsistent', 'Unsupported', 'strict_digest', 'encode', 'decode', 'outcome_line',
             'machine_fp', 'file_name', 'STATUSES', 'WARN_STATUSES')
    miss = [n for n in names if not hasattr(CS, n)]
    chk('T0 cjunc_store API (Store · StoreInconsistent · Unsupported · strict_digest · encode · decode · outcome_line · machine_fp · file_name · '
        '상태 어휘)', not miss, miss)
    chk('T0 상태 어휘 = 적중 · 지어 씀 · 남이 같은 원장 · 못 읽어 다시 지음 · 저장 건너뜀 · 저장 실패 · 꺼짐 · 열쇠 못 셈 (경고 = 뒤 다섯)',
        tuple(CS.STATUSES) == ('hit', 'built_written', 'built_peer_same', 'unreadable_rebuilt', 'built_write_skipped',
                               'built_write_failed', 'disabled', 'key_unavailable')
        and tuple(CS.WARN_STATUSES) == ('unreadable_rebuilt', 'built_write_skipped', 'built_write_failed', 'disabled', 'key_unavailable'),
        (getattr(CS, 'STATUSES', None), getattr(CS, 'WARN_STATUSES', None)))


# ═════════════════════════ T1 ═════════════════════════
@case('T1 왕복 (메모리) — 원장 픽스처 · 형 모둠')
def t1():
    if not need_cs('T1'):
        return
    objs = {'f1': quiet(build_of(f1_inputs())), 'f1_nosdcp': quiet(build_of(f1_inputs(sdcp=False))),
            'rand3': build_of(rand_inputs(3))(), 'rand7': build_of(rand_inputs(7))(), 'kinds': kinds_object()}
    bad = {}
    for nm, o in objs.items():
        skel, arrs = CS.encode(o)
        back = CS.decode(skel, arrs)
        d = deep_diff(o, back)
        if d or CS.strict_digest(o) != CS.strict_digest(back):
            bad[nm] = d or 'strict'
        if nm != 'kinds' and CJ.registry_fp(back) != o['fp']['registry']:
            bad[nm] = 'registry_fp'
        if not isinstance(skel, bytes) or any(not isinstance(a, np.ndarray) or a.dtype.hasobject for a in arrs):
            bad[nm] = '꼴 (뼈대 bytes · 배열 = 객체 아닌 ndarray)'
    n_inst = {nm: len(o['instances']['fi']) for nm, o in objs.items() if nm != 'kinds'}
    print(f'    보고 T1 — 원장 instance 수 {n_inst}')
    chk('T1 encode → decode = 시험 쪽 독립 비교 같음 (형 · dict 키 차례 · dtype · 모양 · C/F · 바이트 · 실수 비트 · 객체 원소) · 엄격 지문 같음 · '
        'registry_fp 같음 (원장 넷 + 형 모둠)', not bad and all(v > 0 for k, v in n_inst.items() if k != 'rand3') and len(objs) == 5, bad)


# ═════════════════════════ T2 ═════════════════════════
@case('T2 엄격 지문 판별력')
def t2():
    if not need_cs('T2'):
        return
    a = np.arange(6.0).reshape(2, 3)
    variants = {
        'list': [1, 2], 'tuple': (1, 2), 'int1': 1, 'float1': 1.0, 'true': True, 'np_int64_1': np.int64(1), 'np_f32': np.float32(1.0),
        'np_f64': np.float64(1.0), 'pz': 0.0, 'nz': -0.0, 'str_a': 'a', 'bytes_a': b'a', 'np_str_a': np.str_('a'),
        'dict_ab': {'a': 1, 'b': 2}, 'dict_ba': {'b': 2, 'a': 1}, 'key_int': {1: 'x'}, 'key_str': {'1': 'x'},
        'arr_le': np.array([1.0, 2.0], '<f8'), 'arr_be': np.array([1.0, 2.0], '>f8'), 'arr_C': a, 'arr_F': np.asfortranarray(a),
        'arr_6': np.arange(6.0), 'arr_23': np.arange(6.0).reshape(2, 3).copy(), 'obj_a': np.array(['a'], dtype=object),
        'ustr_a': np.array(['a']), 'none': None, 'None_s': 'None', 'nest1': [[1]], 'nest0': [1], 'empty_l': [], 'empty_t': (),
        'empty_d': {}, 'arr0d': np.array(1.0), 'arr1': np.array([1.0]),
    }
    dig = {k: CS.strict_digest(v) for k, v in variants.items()}
    dup = {}
    for k, v in dig.items():
        dup.setdefault(v, []).append(k)
    clash = [ks for ks in dup.values() if len(ks) > 1 and set(ks) != {'arr_C', 'arr_23'}]
    chk('T2 형 · 차례 · 바이트 차례 · 부호 있는 0 · 키 형 · 0 차원 ↔ 1 원소 가 하나씩 다르면 엄격 지문이 다르다 (같은 값 · 같은 꼴만 같다 — '
        'arr_C = arr_23)', not clash and dig['arr_C'] == dig['arr_23'], clash)


# ═════════════════════════ T3 ═════════════════════════
@case('T3 받지 않는 꼴 = Unsupported · 저장 안 함')
def t3():
    if not need_cs('T3'):
        return
    import collections
    base = np.zeros(10)
    x = np.zeros(3)
    ro_arr = np.zeros(3)
    ro_arr.setflags(write=False)
    lst = [1]

    class Odd:
        pass
    bad_objs = {'별칭 배열': {'a': x, 'b': x}, '별칭 목록': {'a': lst, 'b': lst}, '메모리 겹침': {'a': base[:5], 'b': base[3:8]},
                '비연속': {'a': base[::2]}, '읽기 전용': {'a': ro_arr}, '구조체': {'a': np.zeros(2, dtype=[('x', 'f8'), ('y', 'i4')])},
                'OrderedDict': collections.OrderedDict(a=1), '집합': {'a': {1, 2}}, '모르는 객체': {'a': Odd()}, 'tuple 키': {(1, 2): 1},
                'float 키': {1.5: 1}, '객체 배열 안 모르는 객체': {'a': np.array([Odd()], dtype=object)}}
    got = {}
    for nm, o in bad_objs.items():
        try:
            CS.encode(o)
            got[nm] = 'encode 통과'
        except CS.Unsupported:
            try:
                CS.strict_digest(o)
                got[nm] = 'strict_digest 통과'
            except CS.Unsupported:
                pass
    ok_disjoint = True
    try:
        CS.encode({'a': base[:5], 'b': base[5:]})               # 겹치지 않는 조각 둘 = 받는다 (원장의 base ≠ None 배열 꼴)
    except CS.Unsupported:
        ok_disjoint = False
    chk('T3 받지 않는 꼴 열둘 = encode · strict_digest 둘 다 Unsupported (조용히 다른 꼴로 저장하지 않는다) · 겹치지 않는 조각 둘 = 받는다',
        not got and ok_disjoint, (got, ok_disjoint))
    d = new_store_dir('t3')
    inp = f1_inputs()
    reg0 = build_of(inp)()
    weird = dict(reg0)
    weird['census'] = dict(reg0['census'], _alias_a=x, _alias_b=x)
    st = mk_store(d)
    got_reg, out = st.get_or_build(lambda: weird, **inp)
    chk('T3 지은 원장이 받지 않는 꼴 → 상태 built_write_skipped (사유 unsupported) · 돌려준 원장 = 지은 그 객체 · 폴더에 파일 없음',
        out['status'] == 'built_write_skipped' and 'unsupported' in str(out.get('why')) and got_reg is weird and store_files(d) == [],
        (out, store_files(d)))


# ═════════════════════════ T4 ═════════════════════════
@case('T4 열쇠 결속')
def t4():
    if not need_cs('T4'):
        return
    d = new_store_dir('t4')
    inp = f1_inputs()
    st = mk_store(d)
    k0 = st.key(**inp)
    k0b = mk_store(d).key(**inp)

    def var(**over):
        x = dict(inp)
        x.update(over)
        return x
    sid1 = inp['sid'].copy()
    sid1.flat[sid1.size // 2] = (sid1.flat[sid1.size // 2] + 1) % 3
    pts1 = inp['pts'].copy()
    pts1[3, 1] = np.nextafter(pts1[3, 1], np.inf)
    ph1, f1_, k1 = inp['phase'].copy(), inp['fid'].copy(), inp['kind'].copy()
    ph1[0] = 4
    f1_[0] = f1_[0] + 1
    k1[-1] = 1 - k1[-1]
    keys = {'기준': k0, 'sid 한 칸': st.key(**var(sid=sid1)), 'sid dtype int16': st.key(**var(sid=inp['sid'].astype(np.int16))),
            'lo 1 ulp': st.key(**var(lo=(float(np.nextafter(0.0, 1.0)), 0.0, 0.0))),
            'vox 1 ulp': st.key(**var(vox=float(np.nextafter(inp['vox'], np.inf)))), '점 1 ulp': st.key(**var(pts=pts1)),
            'phase 하나': st.key(**var(phase=ph1)), 'fid 하나': st.key(**var(fid=f1_)), 'kind 하나': st.key(**var(kind=k1))}
    for tk in sorted(inp['thresholds']):
        t = dict(inp['thresholds'])
        v = t[tk]
        t[tk] = (0.5 if v is None else float(np.nextafter(float(v), np.inf)))
        keys[f'문턱 {tk}'] = st.key(**var(thresholds=t))
    t = dict(inp['thresholds'])
    t['s_min_um'] = None
    keys['문턱 s_min None'] = st.key(**var(thresholds=t))
    t = dict(inp['thresholds'])
    t.pop('gap_tol')
    keys['문턱 칸 빠짐'] = st.key(**var(thresholds=t))
    s2 = mk_store(d)
    s2.code = dict(s2.code, **{'carbon_junction.py': '0' * 64})
    keys['코드 (carbon_junction sha)'] = s2.key(**inp)
    s3 = mk_store(d)
    s3.env = dict(s3.env, numpy='0.0.0')
    keys['환경 (numpy 판)'] = s3.key(**inp)
    keys['기계'] = mk_store(d, 'B').key(**inp)
    old_mv = CJ.CJUNC_MODEL_VERSION
    try:
        CJ.CJUNC_MODEL_VERSION = old_mv + '-x'
        keys['모델 판'] = st.key(**inp)
    finally:
        CJ.CJUNC_MODEL_VERSION = old_mv
    old_fmt = CS.STORE_FORMAT
    try:
        CS.STORE_FORMAT = old_fmt + '-x'
        keys['꼴 판'] = st.key(**inp)
    finally:
        CS.STORE_FORMAT = old_fmt
    same_canon = st.key(**var(pts=np.asfortranarray(inp['pts']), phase=inp['phase'].astype(np.int32), fid=inp['fid'].astype(np.int32),
                              kind=inp['kind'].astype(np.int8)))   # 같은 정준 값 (float64 · int64) · 다른 메모리 차례 · 정수 폭
    vals = list(keys.values())
    chk('T4 열쇠 = 64 hex · 같은 입력 · 새 Store 도 같은 열쇠 (결정적)', isinstance(k0, str) and len(k0) == 64
        and all(c in '0123456789abcdef' for c in k0) and k0 == k0b, (k0, k0b))
    chk(f'T4 열쇠 결속 {len(keys) - 1} 갈래 (침대 · lo · vox · 점 · phase · fid · kind · 문턱 열 칸 · s_min None · 칸 빠짐 · 코드 · 환경 · 기계 · 모델 · '
        '꼴) — 하나씩 바꾸면 모두 다른 열쇠 (서로도 다름)', len(set(vals)) == len(vals), [k for k, v in keys.items() if vals.count(v) > 1])
    chk('T4 열쇠는 정준 입력 (원장이 실제로 쓰는 float64 · int64 값) 에 묶인다 — 같은 값이면 메모리 차례 (F) · 정수 폭 (int32 · int8) 이 달라도 '
        '같은 열쇠 (한정: 입력 dtype 은 열쇠 밖 = 원장도 정준 값만 본다)',
        same_canon == k0, (same_canon, k0))


# ═════════════════════════ T5 ═════════════════════════
@case('T5 흐름 — 짓고 씀 → 적중 · 계획 · σ · payload_prepare')
def t5():
    if not need_cs('T5'):
        return
    d = new_store_dir('t5')
    inp = f1_inputs()
    n = [0]
    s1 = mk_store(d)
    reg1, o1 = s1.get_or_build(build_of(inp, n), **inp)
    fn = CS.file_name(s1.key(**inp))
    files1 = store_files(d)
    mode = stat.S_IMODE(os.lstat(os.path.join(d, fn)).st_mode) if fn in files1 else None
    chk('T5a 없음 → 짓기 1 회 · 상태 built_written · 파일 cjreg_<열쇠>.npz 하나 (0444 · 임시 파일 없음) · 기록 칸 (열쇠 · 파일 · 초 · 바이트)',
        n[0] == 1 and o1['status'] == 'built_written' and files1 == [fn] and mode == 0o444 and o1['key'] == s1.key(**inp)
        and o1['file'] == fn and isinstance(o1.get('bytes'), int) and o1['bytes'] > 0 and o1.get('seconds_build') is not None,
        (n, o1, files1, oct(mode or 0)))
    s2 = mk_store(d)
    reg2, o2 = s2.get_or_build(build_of(inp, n), **inp)
    chk('T5b 새 Store (다음 팔 흉내) → 적중 · 짓기 0 회 · 읽은 원장 = 지은 원장 (시험 쪽 독립 비교) · registry_fp 같음 · 파일 그대로',
        o2['status'] == 'hit' and n[0] == 1 and deep_diff(reg1, reg2) is None and CJ.registry_fp(reg2) == reg1['fp']['registry']
        and store_files(d) == files1, (o2, n, deep_diff(reg1, reg2)))
    p1, p2 = TC.plan(reg1, 1e3), TC.plan(reg2, 1e3)
    r1, r2 = TC.solve(inp['sid'], TC.sig_e(), TC.F1_N, p1), TC.solve(inp['sid'], TC.sig_e(), TC.F1_N, p2)
    chk('T5c 적중 원장의 계획 = 새로 지은 원장의 계획 (비트) · 풀이 결과 dict 비트 같음 (σ > 0 · 관통 픽스처)',
        deep_diff(p1, p2) is None and deep_diff(r1, r2) is None and float(r1['sigma_eff']) > 0.0, (deep_diff(p1, p2), deep_diff(r1, r2)))
    # payload_prepare (생산 배선) — 끔 · 빗나감 · 적중
    ri = rand_inputs(7)
    kw = dict(lo=ri['lo'], vox=ri['vox'], pts=ri['pts'], phase=ri['phase'], fid=ri['fid'], kind=ri['kind'], cjunc=dict(REQ), ptfe_stamp='off')
    po = CW.payload_prepare(ri['sid'], **kw)
    dp = new_store_dir('t5p')
    try:
        pm = CW.payload_prepare(ri['sid'], store=mk_store(dp), **kw)
        ph = CW.payload_prepare(ri['sid'], store=mk_store(dp), **kw)
    except TypeError as e:
        chk('T5d payload_prepare 가 store 를 받는다', False, f'고치기 전 판 — {e}')
        return

    def strip(p):
        return {k: v for k, v in p.items() if k != 'store'}
    chk("T5d payload_prepare — 끔 = 'store' 칸 없음 (옛 칸 집합 그대로) · 빗나감 / 적중 = 'store' 기록 (built_written · hit) · 그 칸 밖 전부 "
        '(계획 · protocol · 지문 · 수 · census) 끔과 비트 같음',
        set(po) == {'plan', 'protocol', 'sdcp_protocol', 'fp', 'counts', 'census'} and pm['store']['status'] == 'built_written'
        and ph['store']['status'] == 'hit' and deep_diff(po, strip(pm)) is None and deep_diff(po, strip(ph)) is None,
        (sorted(po), pm.get('store'), ph.get('store'), deep_diff(po, strip(ph))))
    fm = None
    try:
        fm = load_fail_mark()
    except Exception as e:                                     # noqa: BLE001
        chk('T5e probe6 실패 낱말 정규식을 읽는다', False, f'{type(e).__name__}: {e}')
    if fm is not None:
        lines = {s: CS.outcome_line(dict(o2, status=s, why=('ENOSPC' if s in CS.WARN_STATUSES else None))) for s in CS.STATUSES}
        normal_bad = [s for s in ('hit', 'built_written', 'built_peer_same') if fm.search(lines[s]) or not lines[s].startswith('  STEP3:')]
        warn_bad = [s for s in CS.WARN_STATUSES if '⚠' not in lines[s]]
        chk('T5e 화면 줄 — 정상 셋 (적중 · 지어 씀 · 남이 같은 원장) = probe6 실패 낱말 없음 · "  STEP3:" 로 시작 · 경고 다섯 = ⚠',
            not normal_bad and not warn_bad, (normal_bad, warn_bad, lines))


# ═════════════════════════ T6 ═════════════════════════
@case('T6 못 읽음 = 다시 짓는다 · 파일 그대로')
def t6():
    if not need_cs('T6'):
        return
    inp = f1_inputs()
    ref = build_of(inp)()

    def corrupt_zero(p):
        writable(p)
        open(p, 'wb').close()
        ro(p)

    def corrupt_half(p):
        writable(p)
        sz = os.path.getsize(p)
        with open(p, 'r+b') as f:
            f.truncate(sz // 2)
        ro(p)

    def corrupt_array(p):
        off, size = member_data_offset(p, 'a0.npy')
        flip_byte(p, off + size - 1)

    def corrupt_skel(p):
        off, size = member_data_offset(p, 'skeleton.json')
        flip_byte(p, off + size // 2)

    def corrupt_cdir(p):
        with open(p, 'rb') as f:
            data = f.read()
        i = data.rfind(b'PK\x01\x02')                             # 마지막 중앙 목록 항목의 이름 첫 글자
        flip_byte(p, i + 46)

    def drop_member(p):
        rezip(p, p, edit=lambda nm, b: None if nm == 'a1.npy' else b)

    def dup_member(p):
        with contextlib.redirect_stderr(io.StringIO()), _warnings_off():
            rezip(p, p, extra=(('a0.npy', b'x'),))
    cases_ = {'0 바이트': corrupt_zero, '잘림 (절반)': corrupt_half, '배열 멤버 한 바이트 (CRC)': corrupt_array,
              '뼈대 멤버 한 바이트 (CRC)': corrupt_skel, '중앙 목록 이름 한 바이트': corrupt_cdir, '멤버 빠짐': drop_member,
              '같은 이름 멤버 둘': dup_member}
    bad = {}
    for nm, fn in cases_.items():
        d = new_store_dir('t6_' + str(len(bad)) + '_' + str(abs(hash(nm)) % 10 ** 6))
        p, _reg, _o = write_one(d, inp)
        fn(p)
        before = finger(p)
        n = [0]
        try:
            reg, out = mk_store(d).get_or_build(build_of(inp, n), **inp)
        except Exception as e:                                     # noqa: BLE001
            bad[nm] = f'예외 {type(e).__name__}: {e}'
            continue
        if not (out['status'] == 'unreadable_rebuilt' and n[0] == 1 and deep_diff(reg, ref) is None and finger(p) == before
                and store_files(d) == [os.path.basename(p)] and out.get('why')):
            bad[nm] = (out, n, store_files(d))
    chk(f'T6 못 읽음 {len(cases_)} 갈래 (0 바이트 · 잘림 · CRC 둘 · 중앙 목록 · 멤버 빠짐 · 같은 이름 둘) → 상태 unreadable_rebuilt (사유 기록) · '
        '짓기 1 회 · 돌려준 원장 = 새로 지은 것 · 파일 그대로 (inode · mtime · 모드 · 내용) · 새 파일 · 임시 파일 없음', not bad, bad)


@contextlib.contextmanager
def _warnings_off():
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        yield


# ═════════════════════════ T7 ═════════════════════════
@case('T7 어긋남 = 멈춤 (StoreInconsistent) · 짓지 않음 · 파일 그대로')
def t7():
    if not need_cs('T7'):
        return
    inp = f1_inputs()
    inp_b = dict(inp, thresholds=dict(inp['thresholds'], tol_ff_um=float(np.nextafter(inp['thresholds']['tol_ff_um'], np.inf))))

    def hdr_edit(fn_):
        def edit(nm, b):
            if nm != 'header.json':
                return b
            h = json.loads(b.decode('utf-8'))
            fn_(h)
            return json.dumps(h).encode('utf-8')
        return edit

    def arr_bump(nm, b):
        """배열 멤버의 마지막 바이트 (자료 끝) 한 비트 — 내용만 바뀐다 (zip CRC 는 rezip 이 새로 센다)."""
        return (b[:-1] + bytes([b[-1] ^ 1])) if nm == 'a0.npy' else b

    def bump_and_restrict(p):
        """배열 하나 바꾸고 머리의 엄격 지문 · 뼈대 sha 를 다시 셈 (위조) — registry_fp 는 원장 안 기록과 어긋난다."""
        with zipfile.ZipFile(p) as z:
            items = {i.filename: z.read(i.filename) for i in z.infolist()}
        items['a0.npy'] = arr_bump('a0.npy', items['a0.npy'])
        names = sorted(k for k in items if k.startswith('a'))
        arrs = [np.lib.format.read_array(io.BytesIO(items[f'a{i}.npy']), allow_pickle=False) for i in range(len(names))]
        obj = CS.decode(items['skeleton.json'], arrs)
        h = json.loads(items['header.json'].decode('utf-8'))
        h['strict'] = CS.strict_digest(obj)
        rezip(p, p, edit=lambda nm, b: (json.dumps(h).encode('utf-8') if nm == 'header.json' else items[nm]))

    def sid_forgery(p):
        """다른 sid 격자 (한 칸 다름) 로 지은 원장을 이 열쇠 이름 · 머리로 (엄격 지문 · registry_fp 일관) — 원장 안 sid 지문 ≠ 지금 격자."""
        sid2 = inp['sid'].copy()
        sid2.flat[0] = (sid2.flat[0] + 1) % 3
        reg2 = build_of(dict(inp, sid=sid2))()
        skel, arrs = CS.encode(reg2)
        with zipfile.ZipFile(p) as z:
            h = json.loads(z.read('header.json').decode('utf-8'))
        import hashlib
        h.update(strict=CS.strict_digest(reg2), skeleton_sha256=hashlib.sha256(skel).hexdigest(), n_arrays=len(arrs))
        writable(p)
        tmp = p + '.f'
        with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_STORED) as z:
            z.writestr('header.json', json.dumps(h).encode('utf-8'))
            z.writestr('skeleton.json', skel)
            for i, a in enumerate(arrs):
                b = io.BytesIO()
                np.lib.format.write_array(b, a, allow_pickle=False)
                z.writestr(f'a{i}.npy', b.getvalue())
        os.replace(tmp, p)
        ro(p)

    def renamed(p):
        """다른 열쇠 (문턱 1 ulp) 의 정상 파일을 이 열쇠 이름으로 (이름 바꿈 · 복사)."""
        dB = os.path.dirname(p) + '_B'
        os.makedirs(dB)
        pB, _r, _o = write_one(dB, inp_b)
        writable(p)
        os.unlink(p)
        shutil.copy2(pB, p)
        ro(p)

    def skel_swap(p):
        dB = os.path.dirname(p) + '_B'
        os.makedirs(dB)
        pB, _r, _o = write_one(dB, inp_b)
        with zipfile.ZipFile(pB) as z:
            sk = z.read('skeleton.json')
        sk2 = sk if sk != zipfile.ZipFile(p).read('skeleton.json') else sk + b' '
        rezip(p, p, edit=lambda nm, b: sk2 if nm == 'skeleton.json' else b)

    def to_symlink(p):
        real = p + '.real'
        writable(p)
        os.rename(p, real)
        os.symlink(os.path.basename(real), p)

    def to_dir(p):
        writable(p)
        os.unlink(p)
        os.makedirs(p)
    cases_ = {'다른 열쇠 파일 이름 바꿈': renamed, '뼈대 바꿔 끼움 (CRC 새로)': skel_swap,
              '머리 엄격 지문 고침': lambda p: rezip(p, p, edit=hdr_edit(lambda h: h.update(strict='0' * 64))),
              '배열 바꿈 (CRC 새로 · 머리 그대로)': lambda p: rezip(p, p, edit=arr_bump),
              '배열 바꿈 + 엄격 지문 다시 셈': bump_and_restrict, 'sid 지문 (다른 격자의 원장 · 지문 일관)': sid_forgery,
              '머리 JSON 깨짐': lambda p: rezip(p, p, edit=lambda nm, b: b'{' if nm == 'header.json' else b),
              '꼴 판 다름': lambda p: rezip(p, p, edit=hdr_edit(lambda h: h.update(format='cjstore-v0'))),
              '심볼릭 링크': to_symlink, '폴더': to_dir}
    bad = {}
    for i, (nm, fn) in enumerate(cases_.items()):
        d = new_store_dir(f't7_{i}')
        p, _reg, _o = write_one(d, inp)
        fn(p)
        listing = store_files(d)
        before = None if os.path.isdir(p) or os.path.islink(p) else finger(p)
        n = [0]
        st = mk_store(d)
        ok, why = raises_inconsistent(lambda: st.get_or_build(build_of(inp, n), **inp))
        after = None if os.path.isdir(p) or os.path.islink(p) else finger(p)
        if not (ok and n[0] == 0 and store_files(d) == listing and before == after):
            bad[nm] = (ok, why, n, store_files(d))
    chk(f'T7 어긋남 {len(cases_)} 갈래 → StoreInconsistent (짓기 0 회 · 폴더 · 파일 그대로) — 이름 바꿈 · 뼈대 · 머리 지문 · 배열 · 배열 + 지문 위조 '
        '(registry_fp) · sid 지문 · 머리 JSON · 꼴 판 · 심볼릭 링크 · 폴더', not bad, bad)
    # 한정 (보고) — 자기 일관 위조: 다른 원장 내용 + 같은 sid + 머리 · 지문 모두 다시 셈 → 저장본 혼자는 가리지 못한다 (봉인 원천 재조립 대조의 몫)
    d = new_store_dir('t7_limit')
    p, _reg, _o = write_one(d, inp)
    regB = build_of(inp_b)()
    skel, arrs = CS.encode(regB)
    import hashlib
    with zipfile.ZipFile(p) as z:
        h = json.loads(z.read('header.json').decode('utf-8'))
    h.update(strict=CS.strict_digest(regB), skeleton_sha256=hashlib.sha256(skel).hexdigest(), n_arrays=len(arrs))
    writable(p)
    with zipfile.ZipFile(p + '.f', 'w', zipfile.ZIP_STORED) as z:
        z.writestr('header.json', json.dumps(h).encode('utf-8'))
        z.writestr('skeleton.json', skel)
        for i, a in enumerate(arrs):
            b = io.BytesIO()
            np.lib.format.write_array(b, a, allow_pickle=False)
            z.writestr(f'a{i}.npy', b.getvalue())
    os.replace(p + '.f', p)
    ro(p)
    try:
        _r, o = mk_store(d).get_or_build(build_of(inp), **inp)
        res = o['status']
    except Exception as e:                                         # noqa: BLE001
        res = f'{type(e).__name__}'
    print(f'    보고 T7 한정 — 같은 침대 · 다른 문턱 (1 ulp) 의 원장을 이 열쇠의 머리 · 지문으로 다시 싼 자기 일관 위조 → {res} '
          f'(저장본 혼자 가리지 못함 · 봉인 원천 재조립 대조 = 판정 단계)')


# ═════════════════════════ T8 ═════════════════════════
@case('T8 다른 침대 · 문턱 · 코드 · 기계의 저장본 = 읽지 않음 → 새로 짓고 씀')
def t8():
    if not need_cs('T8'):
        return
    inp = f1_inputs()
    bad = {}
    for nm in ('다른 침대 (SDCP 없음)', '다른 문턱', '다른 코드', '다른 기계', '다른 origin (lo)'):
        d = new_store_dir('t8_' + str(len(bad)) + str(abs(hash(nm)) % 10 ** 6))
        p, _reg, _o = write_one(d, inp)
        before = finger(p)
        other = inp
        st = mk_store(d)
        if nm.startswith('다른 침대'):
            other = f1_inputs(sdcp=False)
        elif nm == '다른 문턱':
            other = dict(inp, thresholds=dict(inp['thresholds'], r_port_um=float(inp['thresholds']['r_port_um']) * 1.5))
        elif nm == '다른 코드':
            st.code = dict(st.code, **{'step3_sigma.py': 'f' * 64})
        elif nm == '다른 기계':
            st = mk_store(d, 'C')
        else:
            other = dict(inp, lo=(0.0, 0.0, float(np.nextafter(0.0, 1.0))))
        n = [0]
        try:
            _r, o = st.get_or_build(build_of(other, n), **other)
        except Exception as e:                                     # noqa: BLE001
            bad[nm] = f'{type(e).__name__}: {e}'
            continue
        if not (o['status'] == 'built_written' and n[0] == 1 and finger(p) == before and len(store_files(d)) == 2):
            bad[nm] = (o, n, store_files(d))
    chk('T8 다른 침대 · 문턱 · 코드 · 기계 · origin = 다른 열쇠 → 옛 저장본을 읽지 않고 새로 짓고 씀 (옛 파일 그대로 · 파일 둘)', not bad, bad)


# ═════════════════════════ T9 ═════════════════════════
RACE_DRIVER = r'''
import json, os, sys, time
cfg = json.load(open(sys.argv[1], encoding='utf-8'))
sys.path.insert(0, cfg['scripts'])
import numpy as np
import cjunc_store as CS
import carbon_junction as CJ
z = np.load(cfg['inputs'])
inp = dict(sid=z['sid'], lo=tuple(cfg['lo']), vox=cfg['vox'], pts=z['pts'], phase=z['phase'], fid=z['fid'], kind=z['kind'],
           thresholds=cfg['thr'])

def plain():
    return CJ.cjunc_registry(inp['sid'], inp['lo'], inp['vox'], inp['pts'], inp['phase'], inp['fid'], inp['kind'], **inp['thresholds'])

build = plain
if cfg['mode'] == 'race':
    def build():
        open(cfg['ready'], 'w').close()
        t0 = time.time()
        while not all(os.path.exists(q) for q in cfg['all_ready']):
            if time.time() - t0 > 120:
                raise SystemExit('barrier timeout')
            time.sleep(0.005)
        return plain()
elif cfg['mode'] == 'kill_write':
    _orig = CS._link
    def _slow(a, b):
        open(cfg['marker'], 'w').close()
        time.sleep(300)
        return _orig(a, b)
    CS._link = _slow
elif cfg['mode'] == 'kill_read':
    import zipfile
    _orig_t = zipfile.ZipFile.testzip
    def _slow_t(self):
        open(cfg['marker'], 'w').close()
        time.sleep(300)
        return _orig_t(self)
    zipfile.ZipFile.testzip = _slow_t
st = CS.Store(cfg['root'], machine_paths=tuple(cfg['machine']))
reg, out = st.get_or_build(build, **inp)
print('RESULT ' + json.dumps({'status': out['status']}))
'''


def driver_cfg(name, inp, mode, root, **extra):
    wd = os.path.join(TD, 'drv', name)
    os.makedirs(wd)
    np.savez(os.path.join(wd, 'inputs.npz'), sid=inp['sid'], pts=inp['pts'], phase=inp['phase'], fid=inp['fid'], kind=inp['kind'])
    with open(os.path.join(wd, 'driver.py'), 'w', encoding='utf-8') as f:
        f.write(RACE_DRIVER)
    cfg = dict(scripts=SCRIPTS, inputs=os.path.join(wd, 'inputs.npz'), lo=list(inp['lo']), vox=inp['vox'],
               thr={k: (None if v is None else float(v)) for k, v in inp['thresholds'].items()}, mode=mode, root=root,
               machine=[machine_file('A', ('%032x' % (abs(hash('A')) % (16 ** 32))))], **extra)
    cp = os.path.join(wd, 'cfg.json')
    with open(cp, 'w', encoding='utf-8') as f:
        json.dump(cfg, f)
    return os.path.join(wd, 'driver.py'), cp, wd


@case('T9 같은 열쇠 동시 쓰기')
def t9():
    if not need_cs('T9'):
        return
    inp = f1_inputs()
    # (a) 남이 같은 원장을 먼저 씀
    d = new_store_dir('t9a')
    mine = [None]

    def build_same():
        mk_store(d).get_or_build(build_of(inp), **inp)           # 남 (다른 Store) 이 먼저 쓴다
        mine[0] = build_of(inp)()
        return mine[0]
    reg, o = mk_store(d).get_or_build(build_same, **inp)
    chk('T9a 남이 같은 열쇠에 같은 원장을 먼저 씀 → 상태 built_peer_same · 파일 하나 · 돌려준 원장 = 내가 지은 것 · 임시 파일 없음',
        o['status'] == 'built_peer_same' and reg is mine[0] and len(store_files(d)) == 1, (o, store_files(d)))
    # (b) 남이 같은 열쇠에 다른 원장 (census 한 칸 — registry_fp 밖) 을 먼저 씀
    d = new_store_dir('t9b')

    def peer_diff():
        r = build_of(inp)()
        r['census'] = dict(r['census'], n_instances_same_fid_pieces=int(r['census']['n_instances_same_fid_pieces']) + 1)
        return r

    def build_diff():
        mk_store(d).get_or_build(peer_diff, **inp)
        return build_of(inp)()
    listing = None
    ok, why = raises_inconsistent(lambda: mk_store(d).get_or_build(build_diff, **inp))
    listing = store_files(d)
    chk('T9b 남이 같은 열쇠에 다른 원장 → 멈춤 (StoreInconsistent · 같은 입력 두 원장 = 비결정 또는 열쇠 결함) · 남의 파일 그대로 · 임시 파일 없음',
        ok and len(listing) == 1 and listing[0].startswith('cjreg_'), (why, listing))
    # (c) 실제 프로세스 둘 경주
    d = new_store_dir('t9c')
    procs = []
    readies = [os.path.join(TD, 'drv', f'ready_{i}') for i in range(2)]
    for i in range(2):
        drv, cp, _wd = driver_cfg(f'race{i}', inp, 'race', d, ready=readies[i], all_ready=readies)
        procs.append(subprocess.Popen([sys.executable, drv, cp], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True))
    outs = []
    for p in procs:
        so, _ = p.communicate(timeout=300)
        m = [ln for ln in so.splitlines() if ln.startswith('RESULT ')]
        outs.append((p.returncode, json.loads(m[-1][7:])['status'] if m else so[-300:]))
    stats = sorted(s for _rc, s in outs)
    chk('T9c 실제 프로세스 둘이 같은 열쇠를 함께 지어 씀 (장벽 뒤 동시) → rc 0 둘 · 상태 {built_written, built_peer_same} · 파일 하나 · 임시 파일 없음',
        all(rc == 0 for rc, _s in outs) and stats == ['built_peer_same', 'built_written'] and len(store_files(d)) == 1, (outs, store_files(d)))


# ═════════════════════════ T10 ═════════════════════════
def ns_kill_run(drv, cp, marker, timeout=120):
    """PID 이름공간 안에서 드라이버 → 표지가 생기면 **직접 만든 자식** (unshare) 을 SIGKILL (--kill-child = 안의 python 도 죽음) → rc."""
    p = subprocess.Popen(['unshare', '-pf', '--mount-proc', '--kill-child', sys.executable, drv, cp],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    t0 = time.time()
    seen = False
    while time.time() - t0 < timeout:
        if os.path.exists(marker):
            seen = True
            break
        if p.poll() is not None:
            break
        time.sleep(0.05)
    if p.poll() is None and isinstance(p.pid, int) and p.pid > 1 and p.pid != os.getpid() and p.pid != os.getppid():
        os.kill(p.pid, signal.SIGKILL)
    rc = p.wait(timeout=60)
    return seen, rc


@case('T10 끊김 (PID 이름공간) — 쓰는 도중 · 읽는 도중')
def t10():
    if not need_cs('T10'):
        return
    inp = f1_inputs()
    d = new_store_dir('t10w')
    marker = os.path.join(TD, 'drv', 'mark_w')
    drv, cp, _wd = driver_cfg('kill_w', inp, 'kill_write', d, marker=marker)
    seen, rc = ns_kill_run(drv, cp, marker)
    left = store_files(d)
    tmps = [f for f in left if f.startswith('.')]
    n = [0]
    _r, o = mk_store(d).get_or_build(build_of(inp, n), **inp)
    after = store_files(d)
    chk('T10a 쓰는 도중 끊김 (임시 파일을 다 쓰고 link 전에 SIGKILL) → 남은 것 = 임시 파일뿐 (최종 이름 없음) · 다음 팔 = 빗나감 → 짓고 씀 '
        '(임시 파일은 그대로 · 읽지 않음)', seen and rc != 0 and len(tmps) >= 1 and not [f for f in left if f.startswith('cjreg_')]
        and o['status'] == 'built_written' and n[0] == 1 and set(tmps) <= set(after)
        and len([f for f in after if f.startswith('cjreg_')]) == 1, (seen, rc, left, o, after))
    d = new_store_dir('t10r')
    p, reg0, _o = write_one(d, inp)
    before = finger(p)
    marker = os.path.join(TD, 'drv', 'mark_r')
    drv, cp, _wd = driver_cfg('kill_r', inp, 'kill_read', d, marker=marker)
    seen, rc = ns_kill_run(drv, cp, marker)
    n = [0]
    reg1, o = mk_store(d).get_or_build(build_of(inp, n), **inp)
    chk('T10b 읽는 도중 끊김 (CRC 대조 안에서 SIGKILL) → 파일 그대로 (inode · mtime · 내용) · 폴더 그대로 · 다음 팔 = 적중 (짓기 0 회 · 같은 원장)',
        seen and rc != 0 and finger(p) == before and store_files(d) == [os.path.basename(p)] and o['status'] == 'hit' and n[0] == 0
        and deep_diff(reg0, reg1) is None, (seen, rc, o, store_files(d)))


# ═════════════════════════ T11 ═════════════════════════
@case('T11 쓰기 실패 · 끔 · 폴더 꼴 · 입력 오류')
def t11():
    if not need_cs('T11'):
        return
    inp = f1_inputs()
    ref = build_of(inp)()
    res = {}

    class _SV:
        f_bavail, f_frsize, f_bsize = 1, 4096, 4096
    old = (CS._statvfs, CS._link, CS._write_zip)
    try:
        d = new_store_dir('t11a')
        CS._statvfs = lambda path: _SV()
        r, o = mk_store(d).get_or_build(build_of(inp), **inp)
        res['디스크 여유'] = (o['status'] == 'built_write_skipped' and 'disk' in str(o.get('why')) and store_files(d) == []
                         and deep_diff(r, ref) is None, o, store_files(d))
        CS._statvfs = old[0]
        d = new_store_dir('t11b')

        def _eperm(a, b):
            raise PermissionError(errno.EPERM, 'link 안 됨 (시험)')
        CS._link = _eperm
        r, o = mk_store(d).get_or_build(build_of(inp), **inp)
        res['link EPERM'] = (o['status'] == 'built_write_failed' and 'EPERM' in str(o.get('why')) and store_files(d) == []
                            and deep_diff(r, ref) is None, o, store_files(d))
        CS._link = old[1]
        d = new_store_dir('t11c')

        def _enospc(f, *a, **k):
            f.write(b'PK\x03\x04partial')
            raise OSError(errno.ENOSPC, '자리 없음 (시험)')
        CS._write_zip = _enospc
        r, o = mk_store(d).get_or_build(build_of(inp), **inp)
        res['쓰는 중 ENOSPC'] = (o['status'] == 'built_write_failed' and 'ENOSPC' in str(o.get('why')) and store_files(d) == []
                              and deep_diff(r, ref) is None, o, store_files(d))
    finally:
        CS._statvfs, CS._link, CS._write_zip = old
    d = new_store_dir('t11d')
    st = CS.Store(d, machine_paths=(os.path.join(TD, 'no_such_machine_id'),))
    n = [0]
    r, o = st.get_or_build(build_of(inp, n), **inp)
    res['기계 id 못 읽음'] = (o['status'] == 'disabled' and n[0] == 1 and store_files(d) == [] and deep_diff(r, ref) is None, o)
    bad_dirs = {}
    gw = new_store_dir('t11_gw')
    os.chmod(gw, 0o775)
    fpth = os.path.join(TD, 'stores', 'a_file')
    open(fpth, 'w').close()
    for nm, pth in (('상대 경로', 'stores/rel'), ('없는 폴더', os.path.join(TD, 'stores', 'nope')), ('파일', fpth),
                    ('그룹이 쓸 수 있음', gw)):
        try:
            CS.Store(pth)
            bad_dirs[nm] = '받았다'
        except ValueError:
            pass
    res['폴더 꼴 거부 (상대 · 없음 · 파일 · 남이 씀)'] = (not bad_dirs, bad_dirs)
    bad_inp = dict(inp, kind=None)
    try:
        quiet(CJ.cjunc_registry, inp['sid'], inp['lo'], inp['vox'], inp['pts'], inp['phase'], inp['fid'], None, **inp['thresholds'])
        want = None
    except ValueError as e:
        want = str(e)
    try:
        mk_store(new_store_dir('t11e')).get_or_build(build_of(bad_inp), **bad_inp)
        got = None
    except ValueError as e:
        got = str(e)
    res['입력 오류 = 옛 오류 그대로 (열쇠 못 셈 → 그냥 짓기 → 같은 ValueError)'] = (want is not None and got == want, want, got)
    bad = {k: v[1:] for k, v in res.items() if not v[0]}
    chk(f'T11 {len(res)} 갈래 — 디스크 여유 (건너뜀) · link EPERM · 쓰는 중 ENOSPC (실패 · 임시 파일 지움) · 기계 id 못 읽음 (꺼짐 · 매번 짓기) · '
        '폴더 꼴 거부 · 입력 오류 = 옛 오류 — 팔 결과 (돌려준 원장) 는 늘 새로 지은 것과 같다', not bad, bad)


# ═════════════════════════ P — payload 끝-끝 ═════════════════════════
@case('P payload 끝-끝 (실제 payload · CPU)')
def t_payload():
    import test_ca_ext_b6 as B6
    wd = os.path.join(TD, 'payload')
    os.makedirs(wd)
    B6.make_fixture(wd, sdcp=True)
    base = B6.OFF + B6.LEAN2 + B6.CJ
    sd = new_store_dir('pay')
    gw = new_store_dir('pay_gw')
    os.chmod(gw, 0o775)
    refuse = {'FLAG_WITHOUT_CJUNC': (B6.OFF + B6.LEAN2 + ['--step3-cjunc-store', sd], 'FLAG_WITHOUT_CJUNC'),
              'STORE_GRAPH_ONLY': (base + ['--step3-cjunc-graph-only', '--step3-cjunc-store', sd], 'STORE_GRAPH_ONLY'),
              'STORE_PATH 상대': (base + ['--step3-cjunc-store', 'rel_store'], 'STORE_PATH'),
              'STORE_PATH 없음': (base + ['--step3-cjunc-store', os.path.join(sd, 'nope')], 'STORE_PATH'),
              'STORE_PATH 남이 씀': (base + ['--step3-cjunc-store', gw], 'STORE_PATH')}
    bad = {}
    for i, (nm, (extra, code)) in enumerate(refuse.items()):
        rc, log, _d = B6.run_payload(wd, extra, out=f'refuse_{i}.json')
        if not (rc != 0 and f'S2_CJUNC_REFUSED|{code}|' in log and not os.path.exists(os.path.join(wd, f'refuse_{i}.json'))):
            bad[nm] = (rc, log.strip()[-200:])
    chk('P1 입구 거부 다섯 (접합 없이 · 조립만과 함께 · 상대 · 없는 폴더 · 남이 쓸 수 있는 폴더) → rc ≠ 0 · S2_CJUNC_REFUSED|<코드>| · 출력 없음 · '
        '저장 폴더 빈 채', not bad and store_files(sd) == [], (bad, store_files(sd)))
    rc0, log0, d0 = B6.run_payload(wd, base, out='p_off.json')
    rc1, log1, d1 = B6.run_payload(wd, base + ['--step3-cjunc-store', sd], out='p_on1.json')
    files1 = store_files(sd)
    rc2, log2, d2 = B6.run_payload(wd, base + ['--step3-cjunc-store', sd], out='p_on2.json')

    def rb(nm):
        p = os.path.join(wd, nm)
        return open(p, 'rb').read() if os.path.exists(p) else None
    b0, b1, b2 = rb('p_off.json'), rb('p_on1.json'), rb('p_on2.json')
    sig = (((d0 or {}).get('mpm_metrics') or {}).get('step3') or {}).get('sigma_e_eff_S_cm')
    chk('P2 끔 · 켬 (빗나감 → 짓고 씀) · 켬 (적중) — rc 0 셋 · 팔 JSON 바이트 같음 셋 (σ > 0) · 저장본 파일 하나 (0444) · 둘째 = 적중 줄 · '
        '끔 = 저장본 줄 없음', rc0 == rc1 == rc2 == 0 and b0 is not None and b0 == b1 == b2 and isinstance(sig, float) and sig > 0
        and len(files1) == 1 and store_files(sd) == files1 and '저장본' not in log0 and '새로 지어 저장' in log1 and '읽음' in log2,
        (rc0, rc1, rc2, b0 == b1, b1 == b2, sig, files1, [ln for ln in (log1 + log2).splitlines() if '저장본' in ln]))
    if len(files1) == 1:
        sp = os.path.join(sd, files1[0])
        writable(sp)
        with open(sp, 'wb'):
            pass
        ro(sp)
        rc3, log3, _d3 = B6.run_payload(wd, base + ['--step3-cjunc-store', sd], out='p_on3.json')
        chk('P3 저장본 0 바이트 (정직한 흐름) → rc 0 · 팔 JSON 바이트 = 끔 · ⚠ 못 읽음 줄 · 파일 그대로 (0 바이트)',
            rc3 == 0 and rb('p_on3.json') == b0 and '⚠' in log3 and '못 읽음' in log3 and os.path.getsize(sp) == 0, (rc3, log3[-300:]))
        writable(sp)
        os.unlink(sp)
        rc4, _l4, _d4 = B6.run_payload(wd, base + ['--step3-cjunc-store', sd], out='p_on4.json')
        sp = os.path.join(sd, (store_files(sd) or ['?'])[0])
        rezip(sp, sp, edit=lambda nm, b: (json.dumps(dict(json.loads(b.decode('utf-8')), strict='0' * 64)).encode('utf-8')
                                          if nm == 'header.json' else b))
        rc5, log5, _d5 = B6.run_payload(wd, base + ['--step3-cjunc-store', sd], out='p_on5.json')
        chk('P4 저장본 어긋남 (머리 엄격 지문 고침 · CRC 새로) → rc ≠ 0 · S2_CJUNC_STORE|INCONSISTENT| · 팔 JSON 없음',
            rc4 == 0 and rc5 != 0 and 'S2_CJUNC_STORE|INCONSISTENT|' in log5 and not os.path.exists(os.path.join(wd, 'p_on5.json')),
            (rc4, rc5, log5[-300:]))


# ═════════════════════════ R — 러너 ═════════════════════════
@case('R 러너 (실제 셸 · 실제 payload)')
def t_runner():
    import test_ca_ext_runner as NR
    NR.TD = os.path.join(TD, 'nr')
    os.makedirs(os.path.join(NR.TD, '_probe'))
    NR.SHIMDIR = os.path.join(NR.TD, '_bin')
    os.makedirs(NR.SHIMDIR)
    with open(os.path.join(NR.SHIMDIR, 'python3'), 'w', encoding='utf-8') as f:
        f.write(NR.SHIM.replace('__REAL__', os.path.abspath(sys.executable)))
    os.chmod(os.path.join(NR.SHIMDIR, 'python3'), 0o755)
    ws = NR.make_ws('r_store')
    sd = new_store_dir('runner')
    bad = {}
    for nm, env, want in (('CJUNC=1 없이', {'CJUNC_STORE': sd}, 'CJUNC_STORE 는 CJUNC=1'),
                          ('조립만과 함께', dict(NR.CJ_RT_ENV, CJUNC_SV_CF='1', CJUNC_GRAPH_ONLY='1', CJUNC_STORE=sd), 'CJUNC_GRAPH_ONLY'),
                          ('상대 경로', dict(NR.CJ_RT_ENV, CJUNC_STORE='rel/store'), 'CJUNC_STORE 는 절대 경로'),
                          ('허용 밖 글자 (빈칸)', dict(NR.CJ_RT_ENV, CJUNC_STORE=sd + ' x'), 'CJUNC_STORE 에 허용 밖'),
                          ('개행', dict(NR.CJ_RT_ENV, CJUNC_STORE=sd + '\n/tmp'), 'CJUNC_STORE 에 허용 밖'),
                          ('없는 폴더', dict(NR.CJ_RT_ENV, CJUNC_STORE=os.path.join(sd, 'nope')), 'CJUNC_STORE 폴더가 없다')):
        r = NR.run_runner(ws, env)
        if not (r.rc != 0 and '[p2] ABORT' in r.log and want in r.log and not r.new_dirs and not r.argv):
            bad[nm] = (r.rc, r.log.strip()[-240:], r.new_dirs)
        NR.reset_ws(ws)
    chk('R1 발사 전 ABORT 여섯 (CJUNC=1 없이 · 조립만 · 상대 · 빈칸 · 개행 · 없는 폴더) — rc ≠ 0 · 사유 글 · OUTDIR · payload 없음', not bad, bad)
    r0 = NR.run_runner(ws, NR.CJ_RT_ENV)
    arms0 = {a: open(os.path.join(r0.outdir, a), 'rb').read() for a in r0.arms} if r0.outdir else {}
    rcp0, od0 = r0.receipt_bytes, (os.path.basename(r0.outdir) if r0.outdir else None)
    NR.reset_ws(ws)
    r1 = NR.run_runner(ws, dict(NR.CJ_RT_ENV, CJUNC_STORE=sd))
    arms1 = {a: open(os.path.join(r1.outdir, a), 'rb').read() for a in r1.arms} if r1.outdir else {}
    files1 = store_files(sd)
    argv1 = list(r1.argv.values())
    NR.reset_ws(ws)
    r2 = NR.run_runner(ws, dict(NR.CJ_RT_ENV, CJUNC_STORE=sd))
    arms2 = {a: open(os.path.join(r2.outdir, a), 'rb').read() for a in r2.arms} if r2.outdir else {}
    flag_ok = bool(argv1) and all(NR.opt(t, '--step3-cjunc-store') == sd for t in argv1) \
        and not any('--step3-cjunc-store' in t for t in r0.argv.values())
    chk('R2 켬 — rc 0 · payload 인자 --step3-cjunc-store <폴더> (끔 = 없음) · 팔 이름 · 팔 JSON 바이트 · 영수증 바이트 · OUTDIR 이름 = 끔과 같음 · '
        '저장본 파일 ≥ 1 · 둘째 런 = 적중 (팔 JSON 바이트 같음 · 새 파일 없음)',
        r0.rc == r1.rc == r2.rc == 0 and flag_ok and arms0 and arms0 == arms1 == arms2 and rcp0 == r1.receipt_bytes == r2.receipt_bytes
        and od0 == os.path.basename(r1.outdir or '') == os.path.basename(r2.outdir or '') and len(files1) >= 1 and store_files(sd) == files1
        and '새로 지어 저장' in r1.log and '읽음' in r2.log,
        (r0.rc, r1.rc, r2.rc, flag_ok, sorted(arms0) == sorted(arms1), arms0 == arms1, arms1 == arms2, files1, r1.log[-300:]))
    #  고치기 전 러너의 거동 기록 (옛 env 게이트 = "읽지 않는 축" ABORT — 옳은 이유의 실패 · 새 사유 글이 없다)
    NR.reset_ws(ws)


# ═════════════════════════ C — 사슬 배선 ═════════════════════════
@case('C 사슬 배선 (--cjunc-store · Runner env · 봉인 원천 · 격리 · 회계)')
def t_chain():
    import rint_r_chain as RR
    import run_contract as RC
    import check_method_discipline as CMD
    sd = new_store_dir('chain')
    gw = new_store_dir('chain_gw')
    os.chmod(gw, 0o775)
    errs = {}
    for nm, argv, want in (('verdict 에 줌', ['--stage', 'verdict', '--cjunc-store', sd], '--cjunc-store 는'),
                           ('plan-doc 에 줌', ['--stage', 'plan-doc', '--cjunc-store', sd], '--cjunc-store 는'),
                           ('상대 경로', ['--stage', 'ladder', '--cjunc-store', 'rel'], '--cjunc-store 는'),
                           ('없는 폴더', ['--stage', 'ladder', '--cjunc-store', os.path.join(sd, 'nope')], '--cjunc-store 는'),
                           ('남이 쓸 수 있음', ['--stage', 'ladder', '--cjunc-store', gw], '--cjunc-store 는')):
        buf = io.StringIO()
        with contextlib.redirect_stderr(buf), contextlib.redirect_stdout(buf):
            try:
                RR.main(argv)
                code = 0
            except SystemExit as e:
                code = e.code
        if not (code == 2 and want in buf.getvalue()):
            errs[nm] = (code, buf.getvalue().strip()[-200:])
    chk('C1 --cjunc-store 거부 다섯 (verdict · plan-doc · 상대 · 없는 폴더 · 남이 쓸 수 있음) → argparse 오류 (rc 2 · 사유 글)', not errs, errs)
    old = RR.runner_env_delta
    try:
        RR.runner_env_delta = lambda plan, variant, req, outdir: {'BASE': '1', 'CJUNC_STORE': '/leak'}
        g = RR.RunnerGraphSource('/r', '/root', None, parent_env={'CJUNC_STORE': '/parent'})
        gd = g.env_delta({'name': 'x', 'variant': None}, 0, '/o', {})
        RR.runner_env_delta = lambda plan, variant, req, outdir: {'BASE': '1'}
        ron = roff = don = doff = None
        try:
            ron = RR.Runner('/r', '/root', '/out', {}, None, 0.0, None, dry=True, parent_env={'CJUNC_STORE': '/parent', 'PATH': '/bin'},
                            cjunc_store=sd)
            roff = RR.Runner('/r', '/root', '/out', {}, None, 0.0, None, dry=True, parent_env={'CJUNC_STORE': '/parent', 'PATH': '/bin'})
            don, doff = ron.env_delta({}, '/o'), roff.env_delta({}, '/o')
        except TypeError as e:
            chk('C2 Runner 가 cjunc_store 를 받는다', False, f'고치기 전 판 — {e}')
    finally:
        RR.runner_env_delta = old
    if ron is not None:
        chk('C2 Runner — 켬 = env CJUNC_STORE <폴더> · 끔 = 칸 없음 · 부모 셸의 CJUNC_STORE 는 지운다 (env_base 에 없음)',
            don.get('CJUNC_STORE') == sd and 'CJUNC_STORE' not in doff and 'CJUNC_STORE' not in ron.env_base
            and 'CJUNC_STORE' not in roff.env_base, (don, doff))
    chk('C3 봉인 원천 (RunnerGraphSource) — env 에 CJUNC_STORE 없음 (계획 env 가 실어도 지운다 · 부모 셸 값도 지운다) · 조립만 표지 있음',
        'CJUNC_STORE' not in gd and gd.get('CJUNC_GRAPH_ONLY') == '1' and 'CJUNC_STORE' not in g.env_base, gd)
    chk('C4 같은 판 파일 — 사슬 CODE_FILES 에 cjunc_store.py · S0 일곱 파일 그대로 (저장본 모듈은 S0 밖)',
        'cjunc_store.py' in RR.CODE_FILES and 'cjunc_store.py' not in RR.S0_SAME_FILES and len(RR.S0_SAME_FILES) == 7,
        (RR.CODE_FILES, RR.S0_SAME_FILES))
    chk('C5 규율 검사기 격리 목록 (_RUNNER_AXES) 에 CJUNC_STORE · CLI 회계 --step3-cjunc-store = mode (산출물 · 해 바이트 그대로)',
        'CJUNC_STORE' in CMD._RUNNER_AXES and RC.CLI_ACCOUNTING.get('--step3-cjunc-store') == ('mode', None),
        ('CJUNC_STORE' in CMD._RUNNER_AXES, RC.CLI_ACCOUNTING.get('--step3-cjunc-store')))


def main():
    global ARGS, TD
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--only', default='', help='쉼표로 이름 접두 (예: T,C)')
    ap.add_argument('--keep', action='store_true', help='임시 폴더를 남긴다')
    ARGS = ap.parse_args()
    TD = tempfile.mkdtemp(prefix='cjunc_store_t_')
    os.makedirs(os.path.join(TD, 'stores'))
    os.makedirs(os.path.join(TD, 'drv'))
    t0 = time.time()
    sel = [x.strip() for x in ARGS.only.split(',') if x.strip()]
    try:
        for tag, fn in CASES:
            if sel and not any(tag.startswith(s) for s in sel):
                continue
            print(f'\n── {tag}')
            try:
                fn()
            except Exception as e:                                 # noqa: BLE001 — 시험 안의 예외 = 그 묶음 실패
                import traceback
                chk(f'{tag.split()[0]} 예외 없이', False, f'{type(e).__name__}: {e} @ {traceback.format_exc().splitlines()[-3].strip()[:300]}')
    finally:
        if ARGS.keep:
            print(f'  (임시 폴더 남김: {TD})')
        else:
            for r, ds, fs in os.walk(TD):
                for x in ds + fs:
                    q = os.path.join(r, x)
                    if not os.path.islink(q):
                        try:
                            os.chmod(q, 0o755 if os.path.isdir(q) else 0o644)
                        except OSError:
                            pass
            shutil.rmtree(TD, ignore_errors=True)
    print(f'\ntest_cjunc_store: {_ok} PASS · {len(_fail)} FAIL ({time.time() - t0:.1f} s)')
    for n in _fail:
        print(f'  - {n}')
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
