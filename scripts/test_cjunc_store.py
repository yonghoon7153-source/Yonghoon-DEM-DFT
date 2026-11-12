#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② Q2 (1저자 11-12) — 탄소 접합 원장 저장본 (`scripts/cjunc_store.py`) · 시험 먼저 (규율 ② · CPU · GPU · 킷 없음).

정본 = 묶음 설계 메모 (본 세션 scratch `rint/codepkg/design.md` (나)) · 근거 표 = `docs/reviews/rint2_time_reestimate_20261111/README.md` A-2 · E-2 4 번.
원장 (기하 · `carbon_junction.cjunc_registry`) 은 R_j · 법칙 · c 에 달리지 않는다 → 같은 침대 · 격자 · origin · 문턱 · 코드 · 환경 · 기계면 한 번 지어
저장하고 다음 팔이 **지문을 대조해** 읽는다.  계획 (R_j · 법칙 · c · SV) 은 팔마다 그대로 다시 만든다.

묶음:
  T0  모듈 · API (고치기 전 = 모듈 없음)
  T1  왕복 (메모리) — 원장 픽스처 (instance 하나 넷 + **instance 여럿** 셋 = F5 직렬 · 조밀 침대 둘 (자기 접합 · 긴 접촉 · 고리 · PTFE · SDCP)) +
      형 모둠 (dict 키 차례 · list/tuple · Python/numpy 스칼라 형 · −0 · NaN 비트 · 큰 정수 · 외톨이 대리 · C/F 차례 · 바이트 차례 · 0 차원 ·
      빈 배열 · 객체 배열) + 별칭 모둠 → 시험 쪽 독립 비교 (형 · dtype · 모양 · 차례 표지 · 바이트) · 별칭 서명 · 엄격 지문 · registry_fp
  T2  엄격 지문 판별력 — 형 · 차례 · 바이트 차례 · 부호 있는 0 · 키 형 · 별칭 (같은 객체 ↔ 사본) 하나씩 다르면 다른 지문
  T3  받지 않는 꼴 (메모리 겹침 · 같은 메모리의 두 보기 · 비연속 · 읽기 전용 · 구조체 · dict 하위형 · 집합 · 모르는 객체) = Unsupported ·
      저장 안 함 (팔 결과 그대로).  ★ 별칭 (같은 객체가 두 자리에) 은 받는다 — 되가리킴으로 그대로 복원 (T1 · 원장의 pair_i · pair_j 가
      `[빈 배열] * instance 수` 꼴 = instance 가 둘 이상인 원장은 늘 별칭이 있다 · 대피 세션 11-12 발견)
  T4  열쇠 결속 — 침대 (sid 한 칸 · dtype) · lo · vox (1 ulp) · 점 (1 ulp) · phase · fid · kind · 문턱 열 칸 · 코드 · 환경 · 기계 · 모델 판 · 스키마 ·
      꼴 판 (스키마 = 대피 4 덧 · 열쇠 칸마다 하나씩) · 환경 자리 (venv 접두 · numpy · scipy 폴더 — 11-12 내부 반박 리뷰 RCP-05)
  T5  흐름 — 없음 → 짓고 씀 (0444 · 이름 · 임시 파일 없음) → 새 Store 적중 (짓기 0 회) · 읽은 원장 = 지은 원장 (비트) · 계획 · 풀이 σ 비트 같음 ·
      payload_prepare 끔 / 빗나감 / 적중 같음 (끔 = 'store' 칸 없음) · 화면 줄 (probe6 실패 낱말 없음) · 머리의 쓴 쪽 칸 = 호스트 이름 없음 (RCP-11)
  T6  못 읽음 (정직한 흐름 = 다시 짓는다 · 파일 그대로 · 덮어쓰지 않음 · ⚠ 줄) — 0 바이트 · 잘림 · 배열 · 뼈대 한 바이트 (CRC) · 중앙 목록 한 바이트 ·
      멤버 빠짐 · 같은 이름 둘
  T7  어긋남 (손으로 고친 · 어긋난 기록 = 멈춤 StoreInconsistent · 짓지 않음 · 파일 그대로) — 다른 열쇠 파일 이름 바꿈 · 뼈대 바꿔 끼움 · 머리
      엄격 지문 · 배열 바꿈 · 배열 + 엄격 지문 다시 셈 (registry_fp) · sid 지문 · 머리 JSON · 꼴 판 · 심볼릭 링크 · 폴더 · 파일 모드 (그룹 · 남 쓰기 ·
      그룹 쓰기만 · 남 쓰기만 = 2 회차 RCP2-03) · 파일 소유자 (RCP-06)
  T8  다른 침대 · 문턱 · 기계 · origin 의 저장본 = 열쇠가 달라 읽지 않음 → 새로 짓고 씀 (옛 파일 그대로) · ★ 3 회차 (RCP3-02) Store 코드 칸만 바꾼 꼴 =
      꺼짐 (읽지도 쓰지도 않음 · 다른 코드 = 다른 열쇠는 T4 · T14c · T15a)
  T9  같은 열쇠 동시 쓰기 — 남이 같은 원장 = peer_same · 남이 다른 원장 = 멈춤 · 실제 프로세스 둘 경주 = written 하나 + peer_same 하나 · 파일 하나
  T10 끊김 (PID 이름공간 `unshare -pf --mount-proc --kill-child` 안에서만 · kill = 직접 만든 자식) — 쓰는 도중 (임시 파일 뒤 · link 전) · 읽는 도중
  T11 쓰기 실패 · 끔 — 디스크 여유 · link EPERM · 쓰는 중 ENOSPC · 기계 id 못 읽음 · 폴더 꼴 (상대 · 없음 · 파일 · 그룹 · 남 쓰기 (남만 = 2 회차
      RCP2-03) · 다른 소유자 · 심볼릭 링크 (끝 빗금 포함 · RCP-06) · 정규화 안 된 꼴 (`.` · `..` · 빈 성분 — 2 회차 RCP2-02)) · 입력 오류 = 옛 오류
  T12 쓰는 쪽 발행 전 대조 (직렬화 결함 = 발행 안 함 · 멈춤 아님) — 구현 커밋에서 더함 (고치기 전 판 = 모듈 없음)
  T13 규모 (실침대 꼴 = instance 마다 작은 배열 넷 · 별칭 빈 배열) — 겹침 검사가 배열 쌍마다 돌지 않는다 (배열 수에 선형 · 옛 = 쌍마다
      np.shares_memory = 배열 47 만 개에서 끝나지 않음) · 작은 배열 12 만 개 + 별칭 6 만 자리 왕복 = 시간 안 — 구현 커밋에서 더함
  T14 열쇠 코드 칸 = 원장 짓기가 실제로 부르는 코드 (11-12 내부 반박 리뷰 RCP-01 · 2 회차 RCP2-05) — 원장 짓기 동안 돈 파일 (sys.setprofile) =
      표준 라이브러리 · numpy · scipy · 열쇠 코드 칸뿐 (그 밖 = 실패 · 옛 판은 scripts/ 안만 봤다) · 원장 모듈 둘의 import 문 (AST 전수) ⊆ 표준 ∪ {numpy,
      scipy} ∪ 열쇠 코드 넷 · 리뷰 반례 CE1 (fibre_segment_raster 의 선분 → 셀 차례만 뒤집은 판 · sid 같음 · 새 프로세스) = 다른 열쇠 · 새로 지음 · 새
      프로세스에서 Store() 가 모듈을 새로 부르지 않는다 (매니페스트 exec_env 그대로) · 코드 칸 = 네 파일의 디스크 sha256
  T15 런 도중 코드 바뀜 (11-12 2 회차 재리뷰 RCP2-01 · 새 프로세스 · 코드 사본 폴더) — 재리뷰 CE-A (원장 모듈을 먼저 불러 두고 그 파일이 바뀐 뒤 Store) ·
      cjunc_store 만 불러 둔 뒤 바뀜 · 짓는 도중 바뀜 (짓기가 새 판을 부른다) · 쓰는 도중 바뀜 · 내용 그대로 다시 씀 (수정 시각 = 시작 뒤) = 저장 안 함
      (꺼짐 · 건너뜀 · 사유 code_changed) · 뒤의 정직한 런 = 적중 아님 · 정직한 흐름 = 지어 씀 → 적중 · 런 시작 기록 (cjunc_store 를 불러온 때) ·
      ★ 3 회차 (재확인 2 RCP3-02) 같은 초 뒤집기 (수정 시각 = 런 시작) · 변이판일 때 Store 뒤 되돌림 · 수정 시각을 되돌린 뒤집기 (os.utime) · Store 코드
      칸 ≠ 런 시작 = 저장 안 함 · 수정 시각이 미래인 사본 (rsync -t 꼴) 의 정직한 런 = 지어 씀 → 적중 (코드 칸 = 파일별 stat 신원 정확 대조) ·
      ★ 3 회차 변이 보강: 제자리 되돌림 (`cp -p` 꼴 · 같은 inode · 크기 · 수정 시각 = 상태 바뀐 시각만 다름 · T15l) · 재는 도중 바뀜 = 못 셈 (T15m)
  P   payload 끝-끝 (`test_ca_ext_b6` 픽스처 · 실제 payload · CPU) — 입구 거부 (접합 없이 · 조립만 · rasterize-only (RCP-10) · 상대 · 없음 · 남이 씀 ·
      Store() 의 뜻밖의 예외 둘 = 입구 · 본 길 (RCP-10)) · 끔 / 빗나감 / 적중 팔 JSON 바이트 같음 · 못 읽음 (⚠ · 같음) · 어긋남 (rc ≠ 0 ·
      S2_CJUNC_STORE|INCONSISTENT| · 출력 없음) · instance 둘인 침대 (세 가닥 직렬) 도 지어 씀 → 적중 (P5 · 구현 커밋에서 더함) · 정규화 안 된 폴더
      꼴 = 입구 거부 (P1 · 2 회차 RCP2-02) · cjunc_store 를 원장 모듈 셋보다 먼저 불러온다 (P6 · `python -X importtime` · 2 회차 RCP2-01) · 러너 꼴 인자
      (`--expect-physics` 에 ca_ext.cjunc 칸) 에서도 (P6b · 먼저 불린 열쇠 모듈 없음 · 3 회차 RCP3-03)
  R   러너 (`test_ca_ext_runner` 틀 · 실제 셸 · 실제 payload) — CJUNC=1 없이 · 조립만과 함께 · 상대 · 허용 밖 글자 · 개행 · 없는 폴더 · 심볼릭 링크
      (끝 빗금 포함 · RCP-06) · 정규화 안 된 꼴 (2 회차 RCP2-02) = 발사 전 ABORT · 켬 = payload 인자 · 팔 JSON · 영수증 · OUTDIR = 끔과 같음 · 둘째
      런 = 적중
  C   사슬 배선 — `--cjunc-store` (ladder · predict 만 · 절대 · 있는 폴더 · 남이 못 씀 · 이 사용자 소유 · 심볼릭 링크 아님 (RCP-06) · 정규화된 꼴
      (2 회차 RCP2-02)) · Runner env ·
      봉인 원천 (RunnerGraphSource) 은 절대 안 받음 · 부모 셸 값은 지운다 · CODE_FILES · 규율 검사기 격리 목록 · CLI 회계 (이 사용자 소유 = 대피 4 덧)
⚠ PASS = 저장 · 읽기 · 거부 배선이 계약대로라는 증거이지 원장 (기하) 의 물리 검증이 아니다.  저장본 자신은 **자기 일관 위조** (같은 열쇠 이름 ·
   다시 센 지문) 를 가리지 못한다 — 그 몫 = 봉인 원천 재조립 대조이고 **SV 모서리 팔 (끝 그래프 지문) 만** 덮는다 (사다리 · 비 SV 예측 · 단위 팔은
   독립 대조가 없다 — 같은 코드 · 환경의 결정성 + 열쇠 (T14) + 폴더 · 파일 권한에 기댄다 · 11-12 내부 반박 리뷰 RCP-03) · 한정 (T7 보고 줄).

  python3 scripts/test_cjunc_store.py                 # 전부 (CPU · 몇 분 — P · R 는 실제 payload · 러너)
  python3 scripts/test_cjunc_store.py --only T,C      # 이름 접두로 고르기 (빠른 묶음)
"""
import argparse
import contextlib
import errno
import importlib.util
import io
import json
import os
import re
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
import run_contract as _RCG                                # noqa: E402 — ★ 11-12 2 회차 (재리뷰 RCP2-06) 이 시험 프로세스와 그 자식 (git · payload ·
_RCG.drop_git_env()                                        #   러너) 은 부르는 쪽 환경의 GIT_* 를 물려받지 않는다 (scripts/test_git_env_isolation.py G6)

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


def alias_sig(obj):
    """시험 쪽 독립 걸음 — 변하는 객체 (ndarray · dict · list) 를 처음 만난 차례 번호로 적은 별칭 서명.  같은 객체가 두 자리에 있으면 둘째부터
    ('ref', 번호) — 복원본의 서명이 같아야 별칭 구조가 그대로다 (모듈의 되가리킴 구현을 쓰지 않는다).  → (서명 목록, 되가리킴 수)."""
    seen, out = {}, []

    def walk(x):
        if isinstance(x, (np.ndarray, dict, list)):
            k = seen.get(id(x))
            if k is not None:
                out.append(('ref', k))
                return
            seen[id(x)] = len(seen)
            out.append(('new', seen[id(x)]))
        if isinstance(x, np.ndarray):
            if x.dtype.hasobject:
                for v in x.reshape(-1, order='C'):
                    walk(v)
        elif isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, (list, tuple)):
            for v in x:
                walk(v)
    walk(obj)
    return out, sum(1 for t, _k in out if t == 'ref')


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


def f5_inputs():
    """test_carbon_junction F5 (직렬 A → B → C · 접합 둘 = instance 2) — instance 가 둘 이상인 가장 작은 원장 (pair_i · pair_j 가 별칭)."""
    P, PH, F, K = TC.rows(TC.F5)
    sid, _ = TC.bed((P, PH, F, K), TC.F5_N)
    thr = TC.reg_kw(dict(r_f_um=TC.RF, tol_ff_um=TC.TOL, L_par_um=TC.LPAR, r_port_um=TC.RPORT, gap_tol=2.0, s_min_um=TC.S_MIN))
    return dict(sid=sid, lo=(0.0, 0.0, 0.0), vox=float(TC.H), pts=P, phase=PH, fid=F, kind=K, thresholds=dict(thr))


def dense_inputs(seed, nfib=40, vox=0.25, n=(24, 24, 32)):
    """조밀 침대 (실침대 꼴의 작은 판) — VGCF 경로 nfib (다섯째마다 꺾임 = 자기 접합 후보 · 하나는 닫힌 고리) + PTFE 경로 셋 + SDCP 점 80
    (구 스탬프) → instance 수십 (서로 다른 섬유 · 자기 접합 · 긴 접촉 = 간선 여럿 · PTFE 덮임 · SDCP 근접).  문턱 = 생산 식
    (`ca_ext_cjunc.registry_thresholds`)."""
    rng = np.random.default_rng(seed)
    box = np.array(n, float) * vox
    polys, ph = [], []
    for i in range(nfib):
        p0 = rng.uniform(0.3, box - 0.3)
        d = rng.normal(size=3)
        d /= np.linalg.norm(d)
        p1 = np.clip(p0 + d * rng.uniform(2.0, 5.0), 0.05, box - 0.05)
        if i % 5 == 0:
            polys.append([p0, p1, np.clip(p0 + (p1 - p0) * 0.15 + rng.normal(size=3) * 0.05, 0.05, box - 0.05)])
        else:
            polys.append([p0, p1])
        ph.append(2)
    c0 = box * 0.5
    polys.append([c0 + (0.6, 0.0, 0.0), c0 + (0.0, 0.6, 0.0), c0 + (-0.6, 0.0, 0.0), c0 + (0.0, -0.6, 0.0), c0 + (0.6, 0.0, 0.0)])
    ph.append(2)                                                  # 닫힌 고리 (첫 점 = 끝 점)
    for _ in range(3):
        p0 = rng.uniform(0.2, box - 0.2)
        d = rng.normal(size=3)
        d /= np.linalg.norm(d)
        polys.append([p0, np.clip(p0 + 3.0 * d, 0.05, box - 0.05)])
        ph.append(4)
    P, PH, F, K = [], [], [], []
    for i, (v, p) in enumerate(zip(polys, ph)):
        pts = TC.densify(v, 0.1)
        if p == 2 and i == nfib:
            pts[-1] = pts[0]                                      # 고리 = 좌표 비트 같음
        P.append(pts)
        PH.append(np.full(len(pts), p))
        F.append(np.full(len(pts), 100 + i))
        K.append(np.full(len(pts), 1))
    sd = rng.uniform(0.2, box - 0.2, (80, 3))
    P.append(sd)
    PH.append(np.full(len(sd), 5))
    F.append(np.arange(len(sd)) + 500)
    K.append(np.zeros(len(sd), int))
    P, PH, F, K = np.vstack(P), np.concatenate(PH), np.concatenate(F), np.concatenate(K)
    sid, _pid = quiet(S3.rasterize, np.zeros((0, 3)), np.zeros(0), np.zeros(0, np.int64), P, PH, (0.0, 0.0, 0.0), tuple(box), vox,
                      sdcp_sphere_d_um=0.5, add_fid=F, add_kind=K, bridge_um=0.3)
    thr = CW.registry_thresholds(s_min_um=REQ['s_min_um'], tol_ff_um=REQ['tol_ff_um'])
    return dict(sid=sid, lo=(0.0, 0.0, 0.0), vox=float(vox), pts=P, phase=PH, fid=F, kind=K, thresholds=thr)


def inst_stats(reg):
    I = reg['instances']
    return {'n': int(len(I['fi'])), 'self': int(np.sum(I['self'])), 'long': int(np.sum(I['long'])),
            'nsub_max': (int(np.max(I['nsub'])) if len(I['nsub']) else 0), 'ptfe': int(np.sum(I['ptfe_cov'])),
            'sdcp': int(np.sum(I['a_sdcp'])), 'unrealized': int(np.sum(~I['realized'])), 'ring': int(reg['census'].get('n_ring_pieces') or 0)}


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


def alias_object():
    """별칭 모둠 — 같은 객체가 두 자리에 (배열 · 빈 배열을 n 번 (원장 pair_i · pair_j 꼴) · 목록 · dict · 객체 배열 원소 · 객체 배열 자신 · 튜플 안)
    + 값이 같은 사본 (별칭 아님)."""
    x = np.arange(5.0)
    lst = [1, 2]
    dd = {'k': np.arange(3)}
    oa = np.empty(3, dtype=object)
    oa[0], oa[1], oa[2] = lst, lst, x
    return {'a': x, 'b': x, 'pair_i': [np.zeros(0, np.int64)] * 5, 'pair_j': [np.zeros(0, np.int64)] * 5, 'l': [lst, lst],
            'd': {'p': dd, 'q': dd}, 'o': oa, 'oo': [oa, oa], 't': (x, dd), 'copy': x.copy()}


def new_store_dir(name):
    d = os.path.join(TD, 'stores', name)
    os.makedirs(d)
    os.chmod(d, 0o755)
    return d


@contextlib.contextmanager
def other_owner(d):
    """★ 대피 4 덧 — 폴더 d 를 '이 사용자 소유 아님' 으로 (root = 진짜 chown 다른 번호 · root 아님 = `os.getuid` 를 잠깐 다른 번호로 · 같은 비교 줄을
    거친다).  d = None 이면 아무것도 안 한다.  끝나면 되돌린다."""
    if d is None:
        yield
        return
    real = os.getuid
    st0 = os.stat(d)
    chowned = patched = False
    try:
        try:
            os.chown(d, real() + 12345, -1)
            chowned = True
        except (PermissionError, OSError):
            os.getuid = lambda: real() + 12345
            patched = True
        yield
    finally:
        if patched:
            os.getuid = real
        if chowned:
            os.chown(d, st0.st_uid, -1)


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
             'machine_fp', 'file_name', 'STATUSES', 'WARN_STATUSES', 'code_drift', 'CODE_CHANGED')
    miss = [n for n in names if not hasattr(CS, n)]
    chk('T0 cjunc_store API (Store · StoreInconsistent · Unsupported · strict_digest · encode · decode · outcome_line · machine_fp · file_name · '
        '상태 어휘 · 런 도중 코드 바뀜 (code_drift · CODE_CHANGED — 2 회차 RCP2-01))', not miss, miss)
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
            'rand3': build_of(rand_inputs(3))(), 'rand7': build_of(rand_inputs(7))(), 'f5': build_of(f5_inputs())(),
            'dense1': build_of(dense_inputs(1))(), 'dense2': build_of(dense_inputs(2))(), 'kinds': kinds_object(), 'alias': alias_object()}
    plain = ('kinds', 'alias')
    bad = {}
    for nm, o in objs.items():
        try:
            skel, arrs = CS.encode(o)
            back = CS.decode(skel, arrs)
            d = deep_diff(o, back)
            if d or CS.strict_digest(o) != CS.strict_digest(back):
                bad[nm] = d or 'strict'
            if alias_sig(o) != alias_sig(back):
                bad[nm] = '별칭 서명 (같은 객체가 두 자리 ↔ 복원본)'
            if nm not in plain and CJ.registry_fp(back) != o['fp']['registry']:
                bad[nm] = 'registry_fp'
            if not isinstance(skel, bytes) or any(not isinstance(a, np.ndarray) or a.dtype.hasobject for a in arrs):
                bad[nm] = '꼴 (뼈대 bytes · 배열 = 객체 아닌 ndarray)'
        except CS.Unsupported as e:                              # 넘겨받은 판 = instance 둘 이상 (pair_i · pair_j 별칭) 을 거부했다
            bad[nm] = f'Unsupported: {e}'
    st = {nm: inst_stats(o) for nm, o in objs.items() if nm not in plain}
    n_inst = {nm: v['n'] for nm, v in st.items()}
    print(f'    보고 T1 — 원장 instance 수 {n_inst} · 조밀 침대 {st["dense1"]} · {st["dense2"]} · 별칭 자리 (되가리킴) '
          f'{ {nm: alias_sig(o)[1] for nm, o in objs.items()} }')
    chk('T1 encode → decode = 시험 쪽 독립 비교 같음 (형 · dict 키 차례 · dtype · 모양 · C/F · 바이트 · 실수 비트 · 객체 원소) · 별칭 서명 같음 · '
        '엄격 지문 같음 · registry_fp 같음 (원장 일곱 + 형 모둠 + 별칭 모둠)', not bad and all(v > 0 for v in n_inst.values()) and len(objs) == 9, bad)
    chk('T1 픽스처 덮임 — instance 둘 이상인 원장 셋 (F5 = 2 · 조밀 둘 ≥ 10) · 조밀 침대에 자기 접합 · 긴 접촉 (간선 여럿) · 고리 · PTFE 덮임이 '
        '있다 · instance 둘 이상 = 별칭 자리 있음 (pair_i · pair_j)',
        n_inst['f5'] == 2 and all(st[k]['n'] >= 10 and st[k]['self'] >= 1 and st[k]['long'] >= 1 and st[k]['nsub_max'] >= 2
                                  and st[k]['ring'] >= 1 for k in ('dense1', 'dense2'))
        and any(st[k]['ptfe'] >= 1 for k in ('dense1', 'dense2'))
        and all(alias_sig(objs[k])[1] >= 2 for k in ('f5', 'dense1', 'dense2')), st)
    cyc = [np.arange(3)]
    cyc.append(cyc)
    try:
        skel, arrs = CS.encode(cyc)
        bk = CS.decode(skel, arrs)
        cyc_ok = (type(bk) is list and len(bk) == 2 and bk[1] is bk and bk[0].tobytes() == cyc[0].tobytes()
                  and CS.strict_digest(cyc) == CS.strict_digest(bk))
        why = ''
    except Exception as e:                                         # noqa: BLE001
        cyc_ok, why = False, f'{type(e).__name__}: {e}'
    chk('T1 자기 자신을 담은 목록 (고리) — 걸음이 끝난다 · 복원본도 자기 자신을 담는다 · 엄격 지문 같음', cyc_ok, why)


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
    #  별칭 (같은 객체가 두 자리) ↔ 값이 같은 사본 둘 — 꼴이 다르다 (복원본의 별칭 구조가 지문에 든다)
    x5, l2, z0 = np.arange(5.0), [1, 2], np.zeros(0, np.int64)
    variants.update({'alias_arr': {'a': x5, 'b': x5}, 'copy_arr': {'a': x5, 'b': x5.copy()}, 'alias_list': [l2, l2],
                     'copy_list': [l2, list(l2)], 'alias_empty': [z0, z0, z0], 'copy_empty': [z0, z0.copy(), z0.copy()],
                     'alias_empty_12': [z0, z0.copy(), z0], 'alias_empty_23': [z0.copy(), z0, z0]})
    try:
        dig = {k: CS.strict_digest(v) for k, v in variants.items()}
    except CS.Unsupported as e:                                  # 넘겨받은 판 = 별칭을 거부했다
        chk('T2 별칭 꼴의 엄격 지문을 센다 (같은 객체가 두 자리 = 받는다)', False, f'Unsupported: {e}')
        return
    dup = {}
    for k, v in dig.items():
        dup.setdefault(v, []).append(k)
    clash = [ks for ks in dup.values() if len(ks) > 1 and set(ks) != {'arr_C', 'arr_23'}]
    chk('T2 형 · 차례 · 바이트 차례 · 부호 있는 0 · 키 형 · 0 차원 ↔ 1 원소 · 별칭 ↔ 사본 (배열 · 목록 · 빈 배열 · 어느 자리끼리 같은 객체인가) 가 '
        '하나씩 다르면 엄격 지문이 다르다 (같은 값 · 같은 꼴만 같다 — arr_C = arr_23)', not clash and dig['arr_C'] == dig['arr_23'], clash)


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
    oarr = np.empty(4, dtype=object)
    oarr[:] = ['a', 'b', 'c', 'd']

    class Odd:
        pass
    #  ★ 별칭 (같은 객체가 두 자리) 은 여기 없다 — 받는다 (T1 · T2).  서로 다른 배열 객체가 메모리를 나눠 쓰는 꼴 (보기) 은 복원본이 둘로
    #    갈리므로 거부 그대로다.
    bad_objs = {'메모리 겹침': {'a': base[:5], 'b': base[3:8]}, '같은 메모리의 두 보기': {'a': x, 'b': x.view()},
                '한 배열과 그 조각': {'a': base, 'b': base[2:4]}, '객체 배열 겹침': {'a': oarr, 'b': oarr[:2]},
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
        CS.encode({'a': base[:5], 'b': base[5:]})               # 겹치지 않는 조각 둘 (맞닿음) = 받는다 (원장의 base ≠ None 배열 꼴)
        CS.encode({'a': base[5:], 'b': base[:5], 'c': np.zeros(0), 'd': base[5:5]})   # 주소 차례가 거꾸로 · 빈 조각 = 받는다
    except CS.Unsupported:
        ok_disjoint = False
    chk(f'T3 받지 않는 꼴 {len(bad_objs)} = encode · strict_digest 둘 다 Unsupported (조용히 다른 꼴로 저장하지 않는다) · 겹치지 않는 조각 둘 '
        '(맞닿음 · 주소 차례 거꾸로 · 빈 조각) = 받는다', not got and ok_disjoint and len(bad_objs) == 13, (got, ok_disjoint))
    d = new_store_dir('t3')
    inp = f1_inputs()
    reg0 = build_of(inp)()
    weird = dict(reg0)
    weird['census'] = dict(reg0['census'], _ov_a=base[:5], _ov_b=base[3:8])
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
    old_sc = CJ.CJUNC_SCHEMA                                 # ★ 대피 4 덧 — 열쇠의 스키마 칸 (코드 sha 와 겹 방어 · 칸 하나씩)
    try:
        CJ.CJUNC_SCHEMA = old_sc + '-x'
        keys['스키마'] = st.key(**inp)
    finally:
        CJ.CJUNC_SCHEMA = old_sc
    old_fmt = CS.STORE_FORMAT
    try:
        CS.STORE_FORMAT = old_fmt + '-x'
        keys['꼴 판'] = st.key(**inp)
    finally:
        CS.STORE_FORMAT = old_fmt
    #  ★ 11-12 (내부 반박 리뷰 RCP-05) — 환경 칸에 실행 자리 (venv 접두 `sys.prefix` · numpy · scipy 패키지 폴더 실경로) 의 지문: 판 글자가 같은 두 venv ·
    #    두 설치 (빌드 · BLAS 가 다를 수 있다) 는 다른 열쇠 (고치기 전 = 판 글자뿐 → 같은 열쇠).  Store() 가 만들 때 읽으므로 새 Store 로 센다.
    import scipy as _sp
    old_env = (sys.prefix, np.__file__, _sp.__file__)
    try:
        sys.prefix = os.path.join(TD, 'other_venv')
        keys['환경 자리 (venv 접두)'] = mk_store(d).key(**inp)
        sys.prefix = old_env[0]
        np.__file__ = os.path.join(TD, 'other_site', 'numpy', '__init__.py')
        keys['환경 자리 (numpy 폴더)'] = mk_store(d).key(**inp)
        np.__file__ = old_env[1]
        _sp.__file__ = os.path.join(TD, 'other_site', 'scipy', '__init__.py')
        keys['환경 자리 (scipy 폴더)'] = mk_store(d).key(**inp)
    finally:
        sys.prefix, np.__file__, _sp.__file__ = old_env
    same_canon = st.key(**var(pts=np.asfortranarray(inp['pts']), phase=inp['phase'].astype(np.int32), fid=inp['fid'].astype(np.int32),
                              kind=inp['kind'].astype(np.int8)))   # 같은 정준 값 (float64 · int64) · 다른 메모리 차례 · 정수 폭
    vals = list(keys.values())
    chk('T4 열쇠 = 64 hex · 같은 입력 · 새 Store 도 같은 열쇠 (결정적)', isinstance(k0, str) and len(k0) == 64
        and all(c in '0123456789abcdef' for c in k0) and k0 == k0b, (k0, k0b))
    chk(f'T4 열쇠 결속 {len(keys) - 1} 갈래 (침대 · lo · vox · 점 · phase · fid · kind · 문턱 열 칸 · s_min None · 칸 빠짐 · 코드 · 환경 · 기계 · 모델 · '
        '스키마 · 꼴 · 환경 자리 셋 (RCP-05)) — 하나씩 바꾸면 모두 다른 열쇠 (서로도 다름)', len(set(vals)) == len(vals),
        [k for k, v in keys.items() if vals.count(v) > 1])
    env_v = mk_store(d).env
    pth = env_v.get('paths')
    chk('T4 환경 칸 = 판 글자 + 실행 자리 지문 (32 hex · 머리 · 열쇠에 경로 글 (계정 · 집 폴더) 을 싣지 않는다 · RCP-05)',
        isinstance(pth, str) and len(pth) == 32 and all(c in '0123456789abcdef' for c in pth)
        and not any(os.sep in str(v) for v in env_v.values()), env_v)
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
    #  ★ 11-12 (내부 반박 리뷰 RCP-11) — 머리의 쓴 쪽 칸 = pid · 시각 · 짓기 초뿐 (호스트 이름 없음 — 사슬은 기계를 실행자가 넣는 짧은 이름표로만 남기고
    #    (`rint_r_chain.MACHINE_RE` · IP · 주소 금지) 호스트 이름은 FQDN · 주소일 수 있다 · 기계 구별 = 열쇠의 machine-id 지문)
    hdr = None
    if fn in files1:
        with zipfile.ZipFile(os.path.join(d, fn)) as z:
            hdr = json.loads(z.read('header.json').decode('utf-8'))
    import socket
    hn = socket.gethostname() or ''
    htxt = json.dumps(hdr, ensure_ascii=False) if isinstance(hdr, dict) else ''
    chk('T5i 저장본 머리의 쓴 쪽 칸 = build_seconds · pid · utc 뿐 (호스트 이름 칸 없음) · 머리 글 어디에도 이 기계의 호스트 이름 없음 (RCP-11)',
        isinstance(hdr, dict) and sorted(hdr.get('writer') or {}) == ['build_seconds', 'pid', 'utc'] and (len(hn) < 3 or hn not in htxt),
        (hdr or {}).get('writer'))
    p1, p2 = TC.plan(reg1, 1e3), TC.plan(reg2, 1e3)
    r1, r2 = TC.solve(inp['sid'], TC.sig_e(), TC.F1_N, p1), TC.solve(inp['sid'], TC.sig_e(), TC.F1_N, p2)
    chk('T5c 적중 원장의 계획 = 새로 지은 원장의 계획 (비트) · 풀이 결과 dict 비트 같음 (σ > 0 · 관통 픽스처)',
        deep_diff(p1, p2) is None and deep_diff(r1, r2) is None and float(r1['sigma_eff']) > 0.0, (deep_diff(p1, p2), deep_diff(r1, r2)))
    #  ★ instance 여럿 (실침대 꼴 · 대피 세션 11-12) — 넘겨받은 판은 pair_i · pair_j 의 별칭 (`[빈 배열] * instance 수`) 을 거부해 저장을
    #    건너뛰었다 (built_write_skipped · 저장본이 영영 안 생김).  지어 씀 → 적중 · 읽은 원장 = 지은 원장 (비트 · 별칭 서명) · 계획 같음.
    multi_bad = {}
    for nm, mi in (('f5', f5_inputs()), ('dense3', dense_inputs(3))):
        dm = new_store_dir('t5m_' + nm)
        nb = [0]
        rg1, om1 = mk_store(dm).get_or_build(build_of(mi, nb), **mi)
        rg2, om2 = mk_store(dm).get_or_build(build_of(mi, nb), **mi)
        fresh = build_of(mi)()
        ok = (om1['status'] == 'built_written' and om2['status'] == 'hit' and nb[0] == 1 and len(store_files(dm)) == 1
              and len(rg1['instances']['fi']) >= 2 and deep_diff(rg1, rg2) is None and deep_diff(fresh, rg2) is None
              and alias_sig(rg1) == alias_sig(rg2) and alias_sig(rg2)[1] >= 2
              and rg2['instances']['pair_i'][0] is rg2['instances']['pair_i'][1])

        def plan_of(rg):
            try:
                return ('plan', CJ.cjunc_plan(rg, 1.0e6, unreg_law='cut', ptfe_stamp='off'))
            except ValueError as e:
                return ('ValueError', str(e))
        if ok:
            (k1, v1), (k2, v2) = plan_of(fresh), plan_of(rg2)
            ok = k1 == k2 == 'plan' and deep_diff(v1, v2) is None
        if not ok:
            multi_bad[nm] = (om1, om2, nb, deep_diff(rg1, rg2), inst_stats(rg1))
    chk('T5f instance 여럿 (F5 = 2 · 조밀 침대) — 없음 → 지어 씀 (built_written · 건너뛰지 않는다) → 새 Store 적중 (짓기 0 회) · 읽은 원장 = 지은 '
        '원장 = 따로 새로 지은 원장 (시험 쪽 독립 비교) · 별칭 서명 같음 (pair_i 의 두 자리 = 같은 객체) · 계획 (R_j 1e6 · cut) 비트 같음',
        not multi_bad, multi_bad)
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
    #  ★ T5g (대피 세션 11-12) — 저장본의 쓰임 그 자체: 원장은 R_j · 법칙 · c · 극한 · SV 반사실 · PTFE 스탬프 (off ↔ face_alpha = 같은 sid 격자)
    #    에 달리지 않는다 → 한 침대 (instance 수십) 의 팔 여덟이 저장본 **하나**를 같이 쓴다 (첫 팔 = 지어 씀 · 나머지 = 적중) · 팔마다 결과 =
    #    저장본 끔의 같은 요청과 비트 같음 (계획은 팔마다 다시 만든다).
    di = dense_inputs(3)
    bkw = dict(lo=di['lo'], vox=di['vox'], pts=di['pts'], phase=di['phase'], fid=di['fid'], kind=di['kind'])
    arms = {'R_j 1e6 · P0 · off': dict(cjunc=dict(REQ), ptfe_stamp='off'),
            'R_j 3e5 · P0 · face_alpha': dict(cjunc=dict(REQ, R_j_ohm=3.0e5), ptfe_stamp='face_alpha'),
            'R_j 1e6 · P1': dict(cjunc=dict(REQ, ptfe_jlaw='P1'), ptfe_stamp='face_alpha'),
            'c 0': dict(cjunc=dict(REQ), ptfe_stamp='face_alpha', sdcp_mod={'c': 0.0}),
            'c 1': dict(cjunc=dict(REQ), ptfe_stamp='face_alpha', sdcp_mod={'c': 1.0}),
            '바닥 (R_j → ∞)': dict(cjunc=dict(REQ, R_j_ohm=None, rj_limit='inf'), ptfe_stamp='face_alpha'),
            '천장 (R_j → 0)': dict(cjunc=dict(REQ, R_j_ohm=0.0, rj_limit='zero'), ptfe_stamp='face_alpha'),
            'SV 반사실': dict(cjunc=dict(REQ), ptfe_stamp='face_alpha', sv_counterfactual={'threshold': None})}
    dg = new_store_dir('t5g')
    stats_g, bad_g, plans_g = [], {}, []
    n_built = [0]
    orig_reg = CJ.cjunc_registry

    def counting_reg(*a_, **k_):
        n_built[0] += 1
        return orig_reg(*a_, **k_)
    for nm, akw in arms.items():
        off_ = CW.payload_prepare(di['sid'], **bkw, **akw)
        CJ.cjunc_registry = counting_reg                         # 켬 길에서 원장을 실제로 몇 번 짓나 (적중 = 0 번)
        try:
            on_ = CW.payload_prepare(di['sid'], store=mk_store(dg), **bkw, **akw)
        finally:
            CJ.cjunc_registry = orig_reg
        stats_g.append(on_['store']['status'])
        plans_g.append(off_['fp']['plan_rows'])
        if deep_diff(off_, strip(on_)) is not None:
            bad_g[nm] = deep_diff(off_, strip(on_))
    chk(f'T5g 한 침대 (instance {int(off_["counts"]["n_instances"])}) 의 팔 {len(arms)} (R_j 둘 · P0 / P1 · c 0 / 1 · 바닥 · 천장 · SV 반사실 · off ↔ '
        'face_alpha) 이 저장본 하나를 같이 쓴다 — 첫 팔 = built_written · 나머지 = hit · 켬 길에서 원장을 지은 횟수 = 1 (적중 팔은 짓지 않는다) · '
        '파일 하나 · 팔마다 결과 = 저장본 끔과 비트 같음 · 계획 지문은 팔마다 다르다 (≥ 4 가지 = 계획을 다시 만든다)',
        stats_g == ['built_written'] + ['hit'] * (len(arms) - 1) and n_built[0] == 1 and not bad_g and len(store_files(dg)) == 1
        and len(set(plans_g)) >= 4 and int(off_['counts']['n_instances']) >= 10,
        (stats_g, n_built, bad_g, len(set(plans_g)), store_files(dg)))
    #  ★ T5h — 원장 문턱이 다른 팔 (tol_ff · s_min — 선언 값) = 다른 열쇠: 적중이 아니라 새로 짓고 쓴다 · 결과 = 끔과 같음 (payload_prepare 가
    #    열쇠에 넘기는 문턱 = 원장에 넘기는 문턱)
    stats_h, bad_h = [], {}
    for nm, req in (('tol_ff 0.31', dict(REQ, tol_ff_um=0.31)), ('s_min 0.6', dict(REQ, s_min_um=0.6)), ('처음 문턱 다시', dict(REQ))):
        off_h = CW.payload_prepare(di['sid'], cjunc=req, ptfe_stamp='off', **bkw)
        on_h = CW.payload_prepare(di['sid'], store=mk_store(dg), cjunc=req, ptfe_stamp='off', **bkw)
        stats_h.append(on_h['store']['status'])
        if deep_diff(off_h, strip(on_h)) is not None:
            bad_h[nm] = deep_diff(off_h, strip(on_h))
    chk('T5h 원장 문턱이 다른 팔 (tol_ff 0.3 → 0.31 · s_min 0.5 → 0.6) = 다른 열쇠 → 적중 아님 (built_written 둘 · 파일 셋) · 처음 문턱으로 돌아오면 '
        '적중 · 셋 다 결과 = 저장본 끔과 비트 같음', stats_h == ['built_written', 'built_written', 'hit'] and not bad_h
        and len(store_files(dg)) == 3, (stats_h, bad_h, store_files(dg)))
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
        '짓기 1 회 · 돌려준 원장 = 새로 지은 것 · 파일 그대로 (inode · mtime · 모드 · 내용) · 새 파일 · 임시 파일 없음', not bad and len(cases_) == 7, bad)
    #  ★ 큰 배열 멤버의 npy 머리 한 바이트 (구현 커밋에서 더함) — zip 은 멤버를 **끝까지** 읽어야 CRC 를 본다 (작은 멤버는 첫 읽기에서 끝에 닿아
    #    CRC 가 먼저 걸린다 · 한 번에 읽는 덩이 4096 바이트보다 큰 멤버는 아니다) → CRC 를 먼저 (testzip) 보지 않으면 깨진 npy 머리가 "npy 꼴 오류"
    #    = 어긋남 (멈춤) 으로 읽힌다.  끊긴 복사 · 디스크 = 정직한 흐름 = 못 읽음 (다시 짓는다) 이어야 한다.
    inp_big = dense_inputs(1)
    ref_big = build_of(inp_big)()
    d = new_store_dir('t6_big')
    p, _reg, _o = write_one(d, inp_big)
    with zipfile.ZipFile(p) as z:
        big = max((i for i in z.infolist() if i.filename.startswith('a')), key=lambda i: i.file_size)
    off, _size = member_data_offset(p, big.filename)
    flip_byte(p, off + 1)                                          # npy 마법 글자 ('NUMPY' 의 N)
    before = finger(p)
    n = [0]
    try:
        reg, out = mk_store(d).get_or_build(build_of(inp_big, n), **inp_big)
        got_big = (out['status'], n[0], deep_diff(reg, ref_big), finger(p) == before, store_files(d) == [os.path.basename(p)])
    except Exception as e:                                         # noqa: BLE001
        got_big = (f'{type(e).__name__}: {e}',)
    chk(f'T6b 큰 배열 멤버 ({big.file_size:,} 바이트 > 읽기 덩이 4,096) 의 npy 머리 한 바이트 → CRC 가 먼저 걸린다 = 못 읽음 (unreadable_rebuilt · '
        '짓기 1 회 · 새로 지은 원장 · 파일 그대로) — npy 꼴 오류 (어긋남 · 멈춤) 로 읽지 않는다',
        big.file_size > 8192 and got_big == ('unreadable_rebuilt', 1, None, True, True), got_big)


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
    def skel_space(p):
        """뼈대 끝에 빈칸 하나 (JSON 으로는 같은 내용 · 복원본 · 엄격 지문 같음) — 머리의 뼈대 sha256 과만 어긋난다."""
        rezip(p, p, edit=lambda nm, b: (b + b' ') if nm == 'skeleton.json' else b)
    cases_ = {'다른 열쇠 파일 이름 바꿈': renamed, '뼈대 바꿔 끼움 (CRC 새로)': skel_swap, '뼈대 바이트만 다름 (빈칸 하나 · 내용 같음)': skel_space,
              '배열 멤버 뒤 남는 바이트 (CRC 새로 · 내용 같음)': lambda p: rezip(p, p, edit=lambda nm, b: (b + b'\x00') if nm == 'a0.npy' else b),
              '머리 엄격 지문 고침': lambda p: rezip(p, p, edit=hdr_edit(lambda h: h.update(strict='0' * 64))),
              '배열 바꿈 (CRC 새로 · 머리 그대로)': lambda p: rezip(p, p, edit=arr_bump),
              '배열 바꿈 + 엄격 지문 다시 셈': bump_and_restrict, 'sid 지문 (다른 격자의 원장 · 지문 일관)': sid_forgery,
              '머리 JSON 깨짐': lambda p: rezip(p, p, edit=lambda nm, b: b'{' if nm == 'header.json' else b),
              '꼴 판 다름': lambda p: rezip(p, p, edit=hdr_edit(lambda h: h.update(format='cjstore-v0'))),
              '심볼릭 링크': to_symlink, '폴더': to_dir,
              #  ★ 11-12 (내부 반박 리뷰 RCP-06) — 이 코드는 0444 로만 발행한다 · 손으로 0666 이 된 파일 = 남이 바꿀 수 있었다
              '파일 모드 0666 (그룹 · 남 쓰기)': lambda p: os.chmod(p, 0o666),
              #  ★ 11-12 2 회차 (재리뷰 RCP2-03) — 그룹 쓰기만 · 남 쓰기만 갈래 (0666 하나로는 검사가 둘 중 하나만 보는 변이 (0o022 → 0o002 · 0o020) 를
              #    못 가른다 — 재리뷰 변이 N9 안 잡힘)
              '파일 모드 0664 (그룹 쓰기만)': lambda p: os.chmod(p, 0o664), '파일 모드 0464 (그룹 쓰기만 · 소유자 읽기만)': lambda p: os.chmod(p, 0o464),
              '파일 모드 0646 (남 쓰기만)': lambda p: os.chmod(p, 0o646), '파일 모드 0446 (남 쓰기만 · 소유자 읽기만)': lambda p: os.chmod(p, 0o446)}
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
    chk(f'T7 어긋남 {len(cases_)} 갈래 → StoreInconsistent (짓기 0 회 · 폴더 · 파일 그대로) — 이름 바꿈 · 뼈대 (바꿔 끼움 · 바이트만) · 머리 지문 · '
        '배열 · 배열 뒤 남는 바이트 · 배열 + 지문 위조 (registry_fp) · sid 지문 · 머리 JSON · 꼴 판 · 심볼릭 링크 · 폴더 · 파일 모드 0666 (RCP-06) · '
        '그룹 쓰기만 둘 · 남 쓰기만 둘 (2 회차 RCP2-03)',
        not bad and len(cases_) == 17, bad)
    #  ★ 11-12 (내부 반박 리뷰 RCP-06) — 파일 소유자 ≠ 이 사용자 (이 코드는 남의 파일을 만들지 않는다 · 폴더가 0777 이던 때 남이 넣은 파일 꼴) = 멈춤.
    #    root = 진짜 chown · 아니면 os.getuid 를 잠깐 다른 번호로 (`other_owner` — Store 는 그 전에 만든다 = 폴더 검사는 지난다)
    d = new_store_dir('t7_owner')
    p, _reg, _o = write_one(d, inp)
    st_o = mk_store(d)
    n = [0]
    with other_owner(p):
        ok_o, why_o = raises_inconsistent(lambda: st_o.get_or_build(build_of(inp, n), **inp))
    chk('T7c 저장본 파일의 소유자 ≠ 이 사용자 → StoreInconsistent (짓기 0 회 · 사유 = 소유자 · RCP-06)', ok_o and n[0] == 0 and '소유자' in why_o,
        (ok_o, n, why_o))
    #  내용 단 (CRC 를 지난 뒤) 의 뜻밖의 오류 = 어긋남 (멈춤) · 메모리 부족만 그대로 올린다 — 구현 커밋에서 더함
    d = new_store_dir('t7_unexpected')
    p, _reg, _o = write_one(d, inp)
    before = finger(p)
    got7 = {}
    old_dec = CS.decode
    for nm, exc in (('ZeroDivisionError', ZeroDivisionError('뜻밖 (시험)')), ('MemoryError', MemoryError('메모리 (시험)'))):
        def boom(*a_, _e=exc, **k_):
            raise _e
        CS.decode = boom
        n = [0]
        try:
            mk_store(d).get_or_build(build_of(inp, n), **inp)
            got7[nm] = ('예외 없음', n[0])
        except Exception as e:                                     # noqa: BLE001
            got7[nm] = (type(e).__name__, n[0], getattr(e, 'code', None))
        finally:
            CS.decode = old_dec
    chk('T7b 내용 단의 뜻밖의 오류 (복원 중 ZeroDivisionError) → StoreInconsistent (code content · 짓기 0 회) · MemoryError 는 그대로 '
        'MemoryError (어긋남으로 바꾸지 않는다 · 짓기 0 회) · 파일 그대로',
        got7.get('ZeroDivisionError') == ('StoreInconsistent', 0, 'content') and got7.get('MemoryError') == ('MemoryError', 0, None)
        and finger(p) == before, got7)
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
          f'(저장본 혼자 가리지 못함 · 저장본 밖 독립 대조 = 봉인 원천 재조립 — SV 모서리 팔만 · 다른 팔은 대조 없음 (RCP-03 · 1저자 결정))')


# ═════════════════════════ T8 ═════════════════════════
@case('T8 다른 침대 · 문턱 · 기계 · origin 의 저장본 = 읽지 않음 → 새로 짓고 씀 · Store 코드 칸만 바꿈 = 꺼짐')
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
        if nm == '다른 코드':
            #  ★ 3 회차 (재확인 2 RCP3-02) — Store 코드 칸만 바꾼 꼴 (디스크 · 런 시작 그대로) = Store 코드 칸 ≠ 런 시작 코드 칸 → 이 런은 읽지도 쓰지도 않는다
            #    (꺼짐 · 짓기 1 회 · 옛 파일 그대로 · 파일 하나).  다른 코드 = 다른 열쇠는 T4 (열쇠 칸) · T14c · T15a (새 프로세스 · 디스크 변이판 = 새로 지어 씀)
            if not (o['status'] == 'disabled' and str(o.get('why') or '').startswith('code_changed') and n[0] == 1 and finger(p) == before
                    and len(store_files(d)) == 1):
                bad[nm] = (o, n, store_files(d))
            continue
        if not (o['status'] == 'built_written' and n[0] == 1 and finger(p) == before and len(store_files(d)) == 2):
            bad[nm] = (o, n, store_files(d))
    chk('T8 다른 침대 · 문턱 · 기계 · origin = 다른 열쇠 → 옛 저장본을 읽지 않고 새로 짓고 씀 (옛 파일 그대로 · 파일 둘) · 다른 코드 (Store 코드 칸만 바꿈) = '
        '꺼짐 (읽지도 쓰지도 않음 · 옛 파일 그대로 · 3 회차 RCP3-02 — 다른 코드의 열쇠 = T4 · 새 프로세스 = T14c · T15a)', not bad, bad)


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


#: ★ 11-12 (내부 반박 리뷰 RCP-10) — payload 감싸개: `cjunc_store.Store.__init__` 의 __WHICH__ 번째 부름부터 OSError (코드 파일을 못 읽음 꼴) → 같은
#    payload 를 runpy 로 (__main__).  1 = 입구 계약의 Store · 2 = 본 길 (접합 준비 직전) 의 Store.
STORE_BOOM_DRIVER = r'''
import errno, runpy, sys
SCRIPTS, PAYLOAD, WHICH = __SCRIPTS__, __PAYLOAD__, __WHICH__
sys.path.insert(0, SCRIPTS)
import cjunc_store as CS
_orig, _n = CS.Store.__init__, [0]


def _boom(self, *a, **k):
    _n[0] += 1
    if _n[0] >= WHICH:
        raise OSError(errno.EIO, '입출력 오류 (시험 — 코드 파일을 못 읽음 꼴)')
    return _orig(self, *a, **k)
CS.Store.__init__ = _boom
sys.argv = [PAYLOAD] + sys.argv[1:]
runpy.run_path(PAYLOAD, run_name='__main__')
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
        d = new_store_dir('t11c2')

        def _boom(f, *a, **k):                                     # OSError 가 아닌 뜻밖의 예외 (저장 쪽 결함 흉내)
            f.write(b'PK\x03\x04partial')
            raise RuntimeError('뜻밖 (시험)')
        CS._write_zip = _boom
        r, o = mk_store(d).get_or_build(build_of(inp), **inp)
        res['쓰는 중 뜻밖의 예외 (RuntimeError)'] = (o['status'] == 'built_write_failed' and 'RuntimeError' in str(o.get('why'))
                                               and store_files(d) == [] and deep_diff(r, ref) is None, o, store_files(d))
        CS._write_zip = old[2]
        d = new_store_dir('t11c3')
        old_enc = CS.encode_strict

        def _enc_boom(obj):
            raise ValueError('싣기 결함 (시험)')
        CS.encode_strict = _enc_boom
        try:
            r, o = mk_store(d).get_or_build(build_of(inp), **inp)
        finally:
            CS.encode_strict = old_enc
        res['싣는 중 뜻밖의 예외 (ValueError — 팔의 PLAN 거부로 새지 않는다)'] = (
            o['status'] == 'built_write_failed' and 'ValueError' in str(o.get('why')) and store_files(d) == []
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
    rel_ok = new_store_dir('t11_rel')                          # 있는 폴더의 상대 경로 (절대 경로 검사만 걸리게)
    lk = os.path.join(TD, 'stores', 't11_link')                # ★ 11-12 (내부 반박 리뷰 RCP-06) — 뿌리가 심볼릭 링크 (가리키는 폴더는 꼴이 맞다)
    os.symlink(new_store_dir('t11_link_target'), lk)
    ow2 = new_store_dir('t11_ow')                              # ★ 11-12 2 회차 (재리뷰 RCP2-03) — 남 쓰기만 (그룹 쓰기만 = gw 0775)
    os.chmod(ow2, 0o757)
    nd = new_store_dir('t11_norm')                              # ★ 11-12 2 회차 (재리뷰 RCP2-02) — 정규화 안 된 꼴 (`.` · `..` · 빈 성분) = 링크 검사를 비켜 간다
    sdir = os.path.join(TD, 'stores')
    for nm, pth, word in (('상대 경로 (있는 폴더)', os.path.relpath(rel_ok), '절대 경로'), ('없는 폴더', os.path.join(TD, 'stores', 'nope'), None),
                          ('파일', fpth, None), ('그룹이 쓸 수 있음', gw, '그룹 · 남'), ('남만 쓸 수 있음 (0757 · RCP2-03)', ow2, '그룹 · 남'),
                          ('심볼릭 링크 폴더', lk, '심볼릭'),
                          ('심볼릭 링크 폴더 (끝 빗금)', lk + '/', '심볼릭'), ('심볼릭 링크 폴더 (끝 빗금 둘)', lk + '//', '심볼릭'),
                          ('심볼릭 링크 + /. (RCP2-02)', lk + '/.', '정규화'), ('심볼릭 링크 + /./ (RCP2-02)', lk + '/./', '정규화'),
                          ('심볼릭 링크 + /../<이름>/. (RCP2-02)', lk + '/../t11_link/.', '정규화'),
                          ('실제 폴더 + /. (RCP2-02)', nd + '/.', '정규화'), ('실제 폴더 · 가운데 // (RCP2-02)', sdir + '//t11_norm', '정규화'),
                          ('실제 폴더 · 가운데 /./ (RCP2-02)', sdir + '/./t11_norm', '정규화'),
                          ('실제 폴더 · 가운데 /../ (RCP2-02)', sdir + '/../stores/t11_norm', '정규화')):
        try:
            CS.Store(pth)
            bad_dirs[nm] = '받았다'
        except ValueError as e:
            if word is not None and word not in str(e):
                bad_dirs[nm] = f'다른 사유로 거부: {e}'
    #  ★ 11-12 2 회차 변이 보강 (W14) — 점 없는 상대 경로 (cwd = 그 부모 · `.` · `..` · 빈 성분 없음 = 정규화 검사가 못 막는 꼴) → 절대 경로 검사만
    #  막는다 (위 relpath 꼴은 보통 `..` 를 품어 정규화 검사 (RCP2-02) 에도 걸린다 — 그 꼴만으로는 절대 경로 검사를 끈 변이가 안 잡혔다)
    _cwd = os.getcwd()
    try:
        os.chdir(sdir)
        try:
            CS.Store('t11_rel')
            bad_dirs['상대 경로 (점 없는 꼴 · cwd = 부모)'] = '받았다'
        except ValueError as e:
            if '절대 경로' not in str(e):
                bad_dirs['상대 경로 (점 없는 꼴 · cwd = 부모)'] = f'다른 사유로 거부: {e}'
    finally:
        os.chdir(_cwd)
    ow, why_own = new_store_dir('t11_owner'), None             # ★ 대피 4 덧 — 다른 소유자 (root = 진짜 chown · 아니면 이 프로세스 사용자 번호를 바꿔 보인다)
    with other_owner(ow):
        try:
            CS.Store(ow)
            bad_dirs['다른 소유자'] = '받았다'
        except ValueError as e:
            why_own = str(e)
    if why_own is not None and '소유자' not in why_own:
        bad_dirs['다른 소유자'] = f'다른 사유로 거부: {why_own}'
    #  정규화된 꼴은 그대로 받는다 (과잉 거부 없음 — 끝 빗금은 걷는다)
    for nm, pth in (('정규화된 실제 폴더', nd), ('정규화된 실제 폴더 + 끝 빗금', nd + '/')):
        try:
            CS.Store(pth)
        except ValueError as e:
            bad_dirs[nm] = f'거부됨: {e}'
    res['폴더 꼴 거부 (상대 둘 = 절대 경로 사유 (점 없는 꼴 = 변이 보강) · 없음 · 파일 · 그룹 · 남 쓰기 (남만 = RCP2-03) · 다른 소유자 · 심볼릭 링크 셋 '
        '(RCP-06) · 정규화 안 된 꼴 일곱 (RCP2-02)) · '
        '정규화된 꼴 둘은 받음'] = (not bad_dirs, bad_dirs)
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
    chk(f'T11 {len(res)} 갈래 — 디스크 여유 (건너뜀) · link EPERM · 쓰는 중 ENOSPC · 쓰는 중 · 싣는 중 뜻밖의 예외 (실패 · 임시 파일 지움 · 예외가 '
        '팔로 새지 않는다) · 기계 id 못 읽음 (꺼짐 · 매번 짓기) · 폴더 꼴 거부 · 입력 오류 = 옛 오류 — 팔 결과 (돌려준 원장) 는 늘 새로 지은 것과 같다',
        not bad and len(res) == 8, bad)


# ═════════════════════════ T12 (구현 커밋에서 더함) ═════════════════════════
@case('T12 쓰는 쪽 발행 전 대조 — 직렬화가 어긋나면 발행하지 않는다 (멈춤 아님)')
def t12():
    if not need_cs('T12'):
        return
    inp = f1_inputs()
    ref = build_of(inp)()
    d = new_store_dir('t12')
    old = CS._write_zip

    def bad(f, hb, sb, arrays):                               # 뼈대 한 글자 (머리의 뼈대 sha 와 어긋남 — 직렬화 결함 흉내)
        return old(f, hb, sb.replace(b'cjunc_registry', b'cjunc_registrx', 1), arrays)
    CS._write_zip = bad
    try:
        r, o = mk_store(d).get_or_build(build_of(inp), **inp)
    finally:
        CS._write_zip = old
    chk('T12 직렬화 결함 (뼈대 ≠ 머리) → 상태 built_write_failed (사유 = 발행 전 대조) · 폴더 빈 채 (임시 파일 지움) · 돌려준 원장 = 새로 지은 것 · '
        '다음 팔 = 빗나감 → 짓고 씀 (멈춤 없음)', o['status'] == 'built_write_failed' and '발행 전 대조' in str(o.get('why'))
        and store_files(d) == [] and deep_diff(r, ref) is None
        and mk_store(d).get_or_build(build_of(inp), **inp)[1]['status'] == 'built_written', (o, store_files(d)))


# ═════════════════════════ T13 (구현 커밋에서 더함 · 대피 세션 11-12) ═════════════════════════
def ledger_like(n, rng, alias=True):
    """실침대 원장 꼴의 합성 객체 — instance n 개 · instance 마다 작은 int64 배열 넷 (seg_i · seg_j · self_A · self_B) · pair_i · pair_j =
    같은 빈 배열을 n 번 (alias) · 큰 배열 몇."""
    lens = rng.integers(1, 40, size=4 * n)
    obj = {k: [np.arange(int(m), dtype=np.int64) + i for i, m in enumerate(lens[j * n:(j + 1) * n])]
           for j, k in enumerate(('seg_i', 'seg_j', 'self_A', 'self_B'))}
    if alias:
        obj['pair_i'] = [np.zeros(0, np.int64)] * n
        obj['pair_j'] = [np.zeros(0, np.int64)] * n
    obj['Lc'] = rng.normal(size=n)
    obj['Ci'] = rng.normal(size=(n, 3))
    reason = np.empty(n, dtype=object)
    reason[:] = ''
    reason[::7] = 'covered_SDCP'
    obj['reason'] = reason
    return obj


@case('T13 규모 — 작은 배열 수만 개 · 별칭 빈 배열 (실침대 꼴)')
def t13():
    if not need_cs('T13'):
        return
    rng = np.random.default_rng(13)
    small = ledger_like(500, rng, alias=False)                 # 배열 2,000 + 3 (별칭 없음 — 넘겨받은 판도 걷는다)
    calls = [0]
    orig = np.shares_memory

    def counting(*a, **k):
        calls[0] += 1
        return orig(*a, **k)
    np.shares_memory = counting
    try:
        _sk, arrs_s = CS.encode(small)
        CS.strict_digest(small)
    finally:
        np.shares_memory = orig
    linear = chk('T13a 겹침 검사가 배열 쌍마다 돌지 않는다 — 배열 2,002 개 (+ 객체 배열 하나) 에서 np.shares_memory 부름 ≤ 배열 수 (옛 = 쌍마다 · 약 2 백만 번 × 2 = '
                 '배열 47 만 개인 실침대 원장에서 끝나지 않는다)', calls[0] <= len(arrs_s) and len(arrs_s) == 2002, (calls[0], len(arrs_s)))
    if not linear:
        chk('T13b 큰 규모 왕복 (작은 배열 12 만 + 별칭 6 만 자리)', False, 'T13a 실패 = 쌍마다 도는 판 — 큰 규모는 돌리지 않는다 (끝나지 않는다)')
        return
    n = 30000
    big = ledger_like(n, rng)
    t0 = time.time()
    try:
        d1 = CS.strict_digest(big)
        skel, arrs = CS.encode(big)
        back = CS.decode(skel, arrs)
        d2 = CS.strict_digest(back)
        why = ''
    except CS.Unsupported as e:
        d1, d2, arrs, back, why = 1, 2, [], None, f'Unsupported: {e}'
    dt = time.time() - t0
    print(f'    보고 T13b — 배열 {len(arrs):,} · 뼈대 {len(skel) / 1e6 if back is not None else 0:.1f} MB · 지문 둘 + 싣기 + 풀기 {dt:.1f} s')
    chk('T13b 큰 규모 왕복 — instance 3 만 꼴 (작은 배열 12 만 + 별칭 빈 배열 6 만 자리 + 객체 배열 3 만 원소) 지문 · 싣기 · 풀기 · 지문 = 같음 · '
        '저장 배열 = 12 만 + 4 (별칭 빈 배열은 한 번씩만) · 복원본의 pair_i 첫 · 끝 자리 = 같은 객체 · pair_i ≠ pair_j 객체 · 120 s 안',
        d1 == d2 and len(arrs) == 4 * n + 4 and back is not None and back['pair_i'][0] is back['pair_i'][-1]
        and back['pair_j'][0] is back['pair_j'][-1] and back['pair_i'][0] is not back['pair_j'][0] and dt < 120.0, (why, len(arrs), dt))
    if back is None or not hasattr(CS, '_read_members'):
        chk('T13c 그릇 (zip) 왕복 — 멤버 6 만 5 천 넘음', False, '앞 단계 실패 · 또는 그릇 읽기 함수 없음')
        return
    #  그릇 (zip) — 멤버 수가 옛 zip 한도 (65,535) 를 넘는 파일을 쓰는 길 (`_write_zip`) · 읽는 길 (`_read_members` = `Store._read` 의 첫 단) 로
    #  왕복 (실침대 원장 = 약 47 만 멤버 · 공개 API 는 원장 꼴만 받으므로 그릇 단을 직접 부른다 — 단원 시험이 바꿔 끼우는 고리와 같은 층)
    zp = os.path.join(TD, 't13c.npz')
    t0 = time.time()
    with open(zp, 'wb') as f:
        CS._write_zip(f, b'{"t13c":1}', skel, arrs)
    t1 = time.time()
    nbytes = os.path.getsize(zp)
    hb, sb, arrs2 = CS._read_members(zp)
    t2 = time.time()
    back2 = CS.decode(sb, arrs2)
    with zipfile.ZipFile(zp) as z:
        n_mem = len(z.namelist())
    os.unlink(zp)
    print(f'    보고 T13c — 멤버 {n_mem:,} · 파일 {nbytes / 1e6:.1f} MB · 쓰기 {t1 - t0:.1f} s · 읽기 (CRC + 배열) {t2 - t1:.1f} s')
    chk('T13c 그릇 (zip) 왕복 — 멤버 12 만 + 6 (> 65,535 = zip64 끝 기록) 쓰기 → 읽기 (멤버 집합 · CRC · 배열) → 풀기 = 시험 쪽 독립 비교 같음 · '
        '별칭 서명 같음 · 엄격 지문 같음 · 머리 · 뼈대 바이트 그대로',
        n_mem == 4 * n + 6 and n_mem > 65535 and hb == b'{"t13c":1}' and sb == skel and len(arrs2) == len(arrs)
        and deep_diff(big, back2) is None and alias_sig(big) == alias_sig(back2) and CS.strict_digest(back2) == d1,
        (n_mem, len(arrs2), deep_diff(big, back2)))


# ═════════════════════════ T14 (11-12 내부 반박 리뷰 RCP-01 · 2 회차 재리뷰 RCP2-05) ═════════════════════════
#: 원장 (기하) 을 짓는 코드 = 열쇠의 코드 칸 (모듈 넷 — 원장 함수 · 그 선분 → 셀 함수 · 격자 지문 함수 · 직렬화기)
KEY_CODE_FILES = ('carbon_junction.py', 'step3_sigma.py', 'fibre_segment_raster.py', 'cjunc_store.py')
#: 시험 쪽 독립 목록 (모듈의 CODE_MODULES 를 읽지 않는다 — 그 목록을 바꾼 변이가 T14b 허용을 조용히 넓히지 못하게)
KEY_MODULES = tuple(f[:-3] for f in KEY_CODE_FILES)
#: 새 프로세스 탐침 — payload 가 저장본 (Store) 을 만들기 전에 이미 부른 모듈만 있는 꼴에서 Store() 가 프로젝트 모듈을 새로 부르는가
T14_PROBE = r'''
import json, os, sys
scripts, root, mfile = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, scripts)
import numpy, scipy                                                     # noqa: F401
import run_contract, carbon_junction, step3_sigma, ca_ext_cjunc, cjunc_store   # noqa: F401 — payload 가 접합 준비 전에 부른 것
sd = os.path.abspath(scripts)


def proj():
    out = set()
    for n, m in list(sys.modules.items()):
        f = getattr(m, '__file__', None)
        if f and os.path.dirname(os.path.abspath(f)) == sd:
            out.add(n)
    return out
before = proj()
fsr_before = 'fibre_segment_raster' in sys.modules
st = cjunc_store.Store(root, machine_paths=(mfile,))
print('T14PROBE ' + json.dumps({'new_project': sorted(proj() - before), 'fsr_before': fsr_before,
                                'fsr_after': 'fibre_segment_raster' in sys.modules, 'code': st.code}))
'''


def _pkg_dir(mod):
    return os.path.dirname(os.path.realpath(mod.__file__))


def _std_dirs():
    import sysconfig
    out = set()
    for k in ('stdlib', 'platstdlib'):
        p = sysconfig.get_paths().get(k)
        if p:
            out.add(os.path.realpath(p))
    return out


def file_kind(f):
    """원장 짓기 동안 돈 파일 하나의 출처 → 'key' (scripts/ 의 열쇠 코드 넷) · 'test' (이 시험 파일 — 짓기 함수 · quiet) · 'frozen' (`<frozen …>` ·
    `<string>`) · 'stdlib' (표준 라이브러리 폴더 · site-/dist-packages 밖) · 'numpy' · 'scipy' (그 패키지 폴더) · 'other' (그 밖 전부 = 열쇠 밖 코드).
    ★ 11-12 2 회차 (재리뷰 RCP2-05) — 옛 판은 scripts/ 안 파일만 봐서 scripts/ 밖 모듈 · numpy · scipy 밖 제3자 패키지 (판이 열쇠 밖) 를 걸렀다 (부분집합
    필터 · 규율 ⑤) → 이제 허용 목록 밖 = 'other' = 실패."""
    if f.startswith('<'):
        return 'frozen'
    a = os.path.realpath(f)
    if os.path.dirname(a) == os.path.realpath(SCRIPTS) and os.path.basename(a) in KEY_CODE_FILES:
        return 'key'
    if a == os.path.realpath(__file__):
        return 'test'
    import scipy
    for nm, d in (('numpy', _pkg_dir(np)), ('scipy', _pkg_dir(scipy))):
        if a.startswith(d + os.sep):
            return nm
    parts = a.split(os.sep)
    if 'site-packages' not in parts and 'dist-packages' not in parts and any(a.startswith(d + os.sep) for d in _std_dirs()):
        return 'stdlib'
    return 'other'


def mod_kind(name):
    """import 문의 꼭대기 모듈 이름 → '__future__' · 'stdlib' · 'numpy' · 'scipy' · 'key' (열쇠 코드 넷) · 'other' (프로젝트 모듈 · 제3자 패키지 ·
    못 찾음).  찾기 = `importlib.util.find_spec` (꼭대기 이름 = 불러오지 않는다) 의 파일 출처 → `file_kind` 와 같은 표준 라이브러리 판정."""
    if name == '__future__':
        return '__future__'
    if name in ('numpy', 'scipy'):
        return name
    if name in KEY_MODULES:
        return 'key'
    if name in sys.builtin_module_names:
        return 'stdlib'
    try:
        spec = importlib.util.find_spec(name)
    except (ImportError, ValueError):
        return 'other'
    origin = getattr(spec, 'origin', None) if spec is not None else None
    if origin in ('built-in', 'frozen'):
        return 'stdlib'
    if not origin:
        return 'other'
    return 'stdlib' if file_kind(origin) == 'stdlib' else 'other'


def ran_files(fn):
    """fn() 을 부르는 동안 실제로 돈 (sys.setprofile 'call' 사건 — 모듈 본문 실행 포함) 파일 전부 (실경로 · `<…>` 는 그대로) → (값, 파일 집합)."""
    seen = set()

    def hook(frame, event, arg):
        if event == 'call':
            seen.add(frame.f_code.co_filename)
    old = sys.getprofile()
    with contextlib.redirect_stdout(io.StringIO()):
        sys.setprofile(hook)
        try:
            val = fn()
        finally:
            sys.setprofile(old)
    return val, {f if f.startswith('<') else os.path.realpath(f) for f in seen}


def import_names(src):
    """소스의 import 문 (함수 안 포함 · AST 전수) → (꼭대기 모듈 이름 집합 · 상대 import 있음 · 동적 import 흔적 (importlib · __import__ · import_module))."""
    import ast
    mods, rel = set(), False
    for nd in ast.walk(ast.parse(src)):
        if isinstance(nd, ast.Import):
            mods |= {al.name.split('.')[0] for al in nd.names}
        elif isinstance(nd, ast.ImportFrom):
            if nd.level:
                rel = True
            else:
                mods.add((nd.module or '').split('.')[0])
    dyn = 'importlib' in mods or '__import__' in src or 'import_module' in src
    return mods, rel, dyn


def import_violations(src):
    """허용 (표준 라이브러리 ∪ {numpy, scipy} ∪ 열쇠 코드 넷 ∪ __future__) 밖 import → 정렬 목록 (상대 import · 동적 import 흔적 포함)."""
    mods, rel, dyn = import_names(src)
    bad = sorted(m for m in mods if mod_kind(m) == 'other')
    return bad + (['<상대 import>'] if rel else []) + (['<동적 import>'] if dyn else [])


@case('T14 열쇠 코드 칸 = 원장 짓기가 실제로 부르는 코드 (11-12 내부 반박 리뷰 RCP-01 · 2 회차 RCP2-05)')
def t14():
    if not need_cs('T14'):
        return
    import json as _json_mod
    d = new_store_dir('t14')
    code_names = set(mk_store(d).code)
    #  (판별력) 분류기 — 열쇠 밖 프로젝트 모듈 · site-packages 꼴 파일 · 못 찾는 모듈 = other · 표준 · numpy · frozen 은 그 이름
    cls_ok = (file_kind(os.path.join(SCRIPTS, 'run_contract.py')) == 'other' and file_kind(os.path.join(SCRIPTS, 'carbon_junction.py')) == 'key'
              and file_kind(np.__file__) == 'numpy' and file_kind(_json_mod.__file__) == 'stdlib'
              and file_kind(os.path.join(os.sep, 'x', 'site-packages', 'foo.py')) == 'other' and file_kind('<frozen importlib._bootstrap>') == 'frozen'
              and mod_kind('json') == 'stdlib' and mod_kind('numpy') == 'numpy' and mod_kind('run_contract') == 'other'
              and mod_kind('se_material') == 'other' and mod_kind('zz_no_such_module_t14') == 'other' and mod_kind('step3_sigma') == 'key'
              and import_violations('import json\nimport zz_no_such_module_t14\nfrom run_contract import x\nimport numpy.linalg\n'
                                    'from . import y\ndef f():\n    import scipy.sparse\n') == ['run_contract', 'zz_no_such_module_t14', '<상대 import>'])
    chk('T14 (판별력) 분류기 — scripts/ 의 열쇠 밖 모듈 · site-packages 꼴 · 못 찾는 이름 = 허용 밖 · 표준 · numpy · frozen · 열쇠 = 그 이름 · 합성 소스의 '
        '허용 밖 import (제3자 · 프로젝트 · 상대) 를 잡는다 (2 회차 RCP2-05)', cls_ok,
        (file_kind(os.path.join(SCRIPTS, 'run_contract.py')), file_kind(np.__file__), file_kind(_json_mod.__file__), mod_kind('json'),
         mod_kind('run_contract')))
    #  (a) 동적 — 원장 짓기 동안 실제로 돈 파일 전부 (픽스처 넷: instance 하나 (SDCP) · 둘 · 조밀 (자기 · 긴 접촉 · 고리 · PTFE · SDCP) · 무작위)
    ran, per = set(), {}
    for nm, inp in (('f1', f1_inputs()), ('f5', f5_inputs()), ('dense3', dense_inputs(3)), ('rand7', rand_inputs(7))):
        _reg, files = ran_files(lambda inp=inp: CJ.cjunc_registry(inp['sid'], inp['lo'], inp['vox'], inp['pts'], inp['phase'], inp['fid'],
                                                                   inp['kind'], **inp['thresholds']))
        per[nm] = sorted({file_kind(f) for f in files})
        ran |= files
    kinds = {f: file_kind(f) for f in ran}
    other = sorted(f for f, k in kinds.items() if k == 'other')
    key_seen = {os.path.basename(f) for f, k in kinds.items() if k == 'key'}
    chk('T14a 원장 짓기 동안 실제로 돈 파일 (sys.setprofile · 픽스처 넷) = 표준 라이브러리 · numpy · scipy · 열쇠 코드 칸 · 이 시험 파일뿐 (그 밖 = scripts/ '
        '밖 모듈 · 제3자 패키지도 실패 · 2 회차 RCP2-05) · 알려진 셋 (carbon_junction · step3_sigma (_grid_fp) · fibre_segment_raster (segment_cells)) 이 '
        '잡힌다 (갈고리 판별력) — 1 회차 고치기 전 = fibre_segment_raster 가 열쇠 밖 (리뷰 반례 CE1 의 뿌리)',
        not other and key_seen <= code_names and {'carbon_junction.py', 'step3_sigma.py', 'fibre_segment_raster.py'} <= key_seen,
        f'허용 밖 {other[:6]} · 열쇠로 잡힌 것 {sorted(key_seen)} · 열쇠 코드 칸 {sorted(code_names)} · 픽스처별 출처 {per}')
    #  (b) 정적 — 원장 모듈 둘의 import 문 전수 (픽스처가 안 지나는 갈래도 덮는다 · step3_sigma 는 _grid_fp 한 함수만 쓰므로 (a) 가 본다 · cjunc_store 의
    #      run_contract import = 열쇠의 환경 칸 · 폴더 꼴 검사뿐 (원장 바이트 밖))
    st_bad = {}
    for fn in ('carbon_junction.py', 'fibre_segment_raster.py'):
        v = import_violations(open(os.path.join(SCRIPTS, fn), encoding='utf-8').read())
        if v:
            st_bad[fn] = v
    chk('T14b 원장 모듈 둘 (carbon_junction · fibre_segment_raster) 의 import 문 (함수 안 포함 · AST 전수) ⊆ 표준 라이브러리 ∪ {numpy, scipy} ∪ 열쇠 코드 넷 '
        '(그 밖 = 프로젝트 · 제3자 패키지 · 상대 · 동적 import = 실패 · 2 회차 RCP2-05 — 옛 판은 scripts/ 파일이 있는 이름만 봤다)', not st_bad, st_bad)
    #  (c) 리뷰 반례 CE1 — 원 코드로 지어 쓴 폴더를, 선분 → 셀 차례만 뒤집은 fibre_segment_raster (칸 집합 · sid 지문 그대로) 로 돈 **새 프로세스**가 연다
    #      (★ 2 회차 RCP2-01 — 같은 프로세스에서 모듈을 바꿔 끼우면 이제 '런 도중 코드 바뀜' 으로 저장본이 꺼진다 = T15 · 다른 코드 판 = 다른 프로세스)
    inp = dense_inputs(7)
    d2 = new_store_dir('t14_ce1')
    s_o = mk_store(d2)
    k_o = s_o.key(**inp)
    reg_o, o1 = s_o.get_or_build(build_of(inp), **inp)
    mut_src, n_line = t15_mutant_text()
    cdir = t15_code_dir('t14c', fsr_text=mut_src)
    got = t15_run(cdir, d2, 'honest')
    chk('T14c 리뷰 반례 CE1 — 원 코드로 지어 쓴 저장본 폴더를 fibre_segment_raster 의 선분 → 셀 차례만 뒤집은 판 (칸 집합 · sid 지문 그대로) 으로 돈 새 '
        '프로세스가 연다 → 다른 열쇠 · 적중 아님 (새로 지어 씀 · 짓기 1 회) · 돌려준 원장 = 그 판으로 따로 지은 원장 (registry_fp) ≠ 옛 저장 원장 · 파일 둘 '
        '(옛 파일 그대로)',
        n_line == 1 and o1['status'] == 'built_written' and got.get('status') == 'built_written' and got.get('builds') == 1
        and got.get('key') != k_o[:16] and got.get('reg_fp') == got.get('fresh_fp') and got.get('reg_fp') != reg_o['fp']['registry'][:16]
        and len(store_files(d2)) == 2, (o1['status'], got, k_o[:16], reg_o['fp']['registry'][:16]))
    #  (d) 새 프로세스 — Store() 가 열쇠 코드 칸을 셀 때 프로젝트 모듈을 새로 부르지 않는다 (find_spec · 매니페스트 exec_env 의 로드 모듈 집합 ·
    #      내용 해시가 저장본 켬 ↔ 끔에서 같게) · 코드 칸 = 네 파일 = 디스크의 지금 sha256
    import hashlib
    probe = os.path.join(TD, 'drv', 't14_probe.py')
    with open(probe, 'w', encoding='utf-8') as f:
        f.write(T14_PROBE)
    mfile = machine_file('A', ('%032x' % (abs(hash('A')) % (16 ** 32))))
    r = subprocess.run([sys.executable, probe, SCRIPTS, d, mfile], capture_output=True, text=True, timeout=300, stdin=subprocess.DEVNULL)
    m = [ln for ln in (r.stdout or '').splitlines() if ln.startswith('T14PROBE ')]
    got = json.loads(m[-1][9:]) if m else {}
    want = {fn: hashlib.sha256(open(os.path.join(SCRIPTS, fn), 'rb').read()).hexdigest() for fn in KEY_CODE_FILES}
    chk('T14d 새 프로세스 (payload 가 저장본 전에 부른 모듈만) — Store() 가 프로젝트 모듈을 새로 부르지 않는다 (fibre_segment_raster 는 안 불린 채 · '
        '매니페스트 exec_env 그대로) · 코드 칸 = carbon_junction · step3_sigma · fibre_segment_raster · cjunc_store 네 파일 = 디스크의 지금 sha256',
        r.returncode == 0 and got.get('new_project') == [] and got.get('fsr_before') is False and got.get('fsr_after') is False
        and got.get('code') == want, (r.returncode, got, (r.stderr or '')[-400:]))


# ═════════════════════════ T15 (11-12 2 회차 재리뷰 RCP2-01) ═════════════════════════
#: 새 프로세스 — 코드 사본 폴더 (열쇠 코드 파일 넷) 를 sys.path 맨 앞에 두고 저장본을 쓴다.  mode = 그 런 도중 (cjunc_store 를 불러온 뒤 = 런 시작
#  뒤) 에 무엇을 바꾸나: honest (안 바꿈) · ce_a (재리뷰 CE-A 꼴 — fibre_segment_raster 를 먼저 불러 두고 그 파일을 바꾼 뒤 Store) · before_store
#  (cjunc_store 만 불러 두고 바꾼 뒤 Store) · during_build (Store 뒤 짓는 도중 — fibre_segment_raster 는 아직 안 불림 = 짓기가 새 판을 부른다) ·
#  during_write (쓰는 도중 — 발행 직전 다시 셈만 잡는다) · touch (내용 그대로 다시 씀 · 수정 시각 = 시작 뒤 5 s — 뒤집었다 되돌린 꼴).
T15_DRIVER = r'''
import json, os, sys, time
code_dir, scripts, store, mfile, inp_path, mode, mut_path = sys.argv[1:8]
sys.path.insert(0, scripts)
sys.path.insert(0, code_dir)
if mode == 'ce_a':
    import fibre_segment_raster                       # noqa: F401 — payload 의 래스터화 꼴 (원장 모듈을 먼저 불러 둔다 · 재리뷰 CE-A)
import cjunc_store as CS                              # 런 시작 (payload = 입구 계약이 원장 모듈보다 먼저 부른다 · 시험 P6)
t_after_import = time.time_ns()
fsr = os.path.join(code_dir, 'fibre_segment_raster.py')


def swap():                                           # 같은 자리 · 새 내용 (CE1 변이 = 선분 -> 셀 차례만 뒤집음)
    data = open(mut_path, encoding='utf-8').read()
    os.unlink(fsr)
    with open(fsr, 'w', encoding='utf-8') as f:
        f.write(data)


def put_back(b):                                      # 원판 바이트로 되돌려 씀 (같은 자리 · 새 파일)
    os.unlink(fsr)
    with open(fsr, 'wb') as f:
        f.write(b)


start = getattr(CS, '_START', None)
st = None
if mode in ('samesec', 'samesec_store', 'mtime_restore', 'inplace_restore'):
    #  ★ 3 회차 (재확인 2 RCP3-02) — 뒤집었다 되돌린 꼴 (원장 모듈 적재 전 · 결정적): samesec = 변이판 → 불러옴 → 원판 바이트로 되돌려 씀 · 수정 시각 =
    #    런 시작 (옛 판의 1 s 여유 안 · 재확인 2 samesec 318 ms) · samesec_store = 변이판일 때 Store (코드 칸 = 변이판) → 원판으로 되돌려 씀 · 수정 시각 =
    #    런 시작 · mtime_restore = 변이판 → 불러옴 → 1.2 s 뒤 원판 바이트 + 원래 수정 시각 (os.utime · 옛 한정 (나) 꼴)
    #  inplace_restore (★ 3 회차 변이 보강) = mtime_restore 를 **제자리** 로 (`cp -p` 가 있는 파일에 쓰는 꼴 — 같은 inode · 같은 크기 · 원래 수정 시각 →
    #    다른 것은 상태 바뀐 시각 하나뿐 · 그것을 뺀 변이가 inode 바뀌는 T15i 에서 안 잡혔다)
    orig = open(fsr, 'rb').read()
    st0 = os.stat(fsr)
    if mode == 'inplace_restore':
        with open(fsr, 'r+b') as f:
            f.truncate(0)
            f.write(open(mut_path, 'rb').read())
    else:
        swap()
    if mode == 'samesec_store':
        st = CS.Store(store, machine_paths=(mfile,))
    else:
        import fibre_segment_raster                   # noqa: F401 — 변이판이 불린다
    if mode in ('mtime_restore', 'inplace_restore'):
        time.sleep(1.2)
    if mode == 'inplace_restore':
        with open(fsr, 'r+b') as f:
            f.truncate(0)
            f.write(orig)
    else:
        put_back(orig)
    if mode in ('mtime_restore', 'inplace_restore'):
        os.utime(fsr, ns=(st0.st_atime_ns, st0.st_mtime_ns))
        st1 = os.stat(fsr)
        same_id = {'ino': st1.st_ino == st0.st_ino, 'size': st1.st_size == st0.st_size, 'mtime': st1.st_mtime_ns == st0.st_mtime_ns,
                   'ctime': st1.st_ctime_ns == st0.st_ctime_ns}
    else:
        t0 = (start or {}).get('t_ns') or time.time_ns()
        os.utime(fsr, ns=(t0, t0))
import numpy as np
import carbon_junction as CJ
import step3_sigma                                    # noqa: F401
z = np.load(inp_path, allow_pickle=False)
inp = dict(sid=z['sid'], lo=tuple(float(x) for x in z['lo']), vox=float(z['vox']), pts=z['pts'], phase=z['phase'], fid=z['fid'],
           kind=z['kind'], thresholds=json.loads(str(z['thr'])))


def reg_of():
    return CJ.cjunc_registry(inp['sid'], inp['lo'], inp['vox'], inp['pts'], inp['phase'], inp['fid'], inp['kind'], **inp['thresholds'])


n = [0]


def build():
    n[0] += 1
    if mode == 'during_build':
        swap()
    return reg_of()


if mode in ('ce_a', 'before_store'):
    swap()
elif mode == 'touch':
    data = open(fsr, 'rb').read()
    os.unlink(fsr)
    with open(fsr, 'wb') as f:
        f.write(data)
    t = ((start or {}).get('t_ns') or time.time_ns()) + 5000000000
    os.utime(fsr, ns=(t, t))
elif mode == 'during_write':
    _old = CS._write_zip

    def _wz(*a, **k):
        swap()
        return _old(*a, **k)
    CS._write_zip = _wz
if st is None:
    st = CS.Store(store, machine_paths=(mfile,))
if mode == 'store_code_differs':                      # ★ 3 회차 (RCP3-02) — Store 코드 칸 ≠ 런 시작 (손으로 고친 꼴 · 디스크 그대로 — 그 가드만 판별)
    st.code['fibre_segment_raster.py'] = '0' * 64
reg, out = st.get_or_build(build, **inp)
fresh = reg_of()
files = sorted(os.listdir(store))
st_rec = None if start is None else {k: start.get(k) for k in ('t_ns', 'code', 'preloaded', 'error')}
print('T15DRV ' + json.dumps({'mode': mode, 'status': out['status'], 'why': out.get('why'), 'key': (out.get('key') or '')[:16],
                              'builds': n[0], 'reg_fp': reg['fp']['registry'][:16], 'fresh_fp': fresh['fp']['registry'][:16],
                              'files': files, 'code_fsr': st.code.get('fibre_segment_raster.py', '')[:16], 'start': st_rec,
                              'same_id': globals().get('same_id'),
                              't_after_import': t_after_import}, ensure_ascii=False))
'''
T15_FX = {}


def t15_mutant_text():
    """CE1 변이 (fibre_segment_raster 의 선분 → 셀 차례만 뒤집음 · 칸 집합 · sid 지문 그대로) → (소스, 바뀐 줄 수)."""
    src = open(os.path.join(SCRIPTS, 'fibre_segment_raster.py'), encoding='utf-8').read()
    old_line = '    return np.asarray(out[::-1] if _swap else out, np.int64)\n'
    return src.replace(old_line, '    return np.asarray(out if _swap else out[::-1], np.int64)   # T14c · T15 (CE1) 변이\n', 1), src.count(old_line)


def t15_code_dir(name, fsr_text=None):
    """열쇠 코드 파일 넷의 사본 폴더 (fsr_text = 그 fibre_segment_raster 소스) — 새 프로세스의 sys.path 맨 앞 (나머지 모듈은 scripts/)."""
    d = os.path.join(TD, 'code_' + name)
    os.makedirs(d)
    for fn in KEY_CODE_FILES:
        if fn == 'fibre_segment_raster.py' and fsr_text is not None:
            with open(os.path.join(d, fn), 'w', encoding='utf-8') as f:
                f.write(fsr_text)
        else:
            shutil.copyfile(os.path.join(SCRIPTS, fn), os.path.join(d, fn))
    return d


def t15_inputs_file():
    """조밀 침대 dense_inputs(7) → npz (새 프로세스가 같은 입력을 읽는다 · 문턱 = JSON)."""
    p = T15_FX.get('inp')
    if p is None:
        inp = dense_inputs(7)
        p = os.path.join(TD, 'drv', 't15_inp.npz')
        np.savez(p, sid=inp['sid'], lo=np.asarray(inp['lo'], np.float64), vox=np.float64(inp['vox']), pts=inp['pts'], phase=inp['phase'],
                 fid=inp['fid'], kind=inp['kind'], thr=np.array(json.dumps(inp['thresholds'])))
        T15_FX['inp'] = p
    return p


def t15_run(code_dir, store, mode, mut=None):
    """드라이버 한 번 (새 프로세스) → 결과 dict (+ rc · stderr 끝 · 띄우기 직전 시각)."""
    drv = os.path.join(TD, 'drv', 't15_drv.py')
    if not os.path.exists(drv):
        with open(drv, 'w', encoding='utf-8') as f:
            f.write(T15_DRIVER)
    if mut is None:
        mut = T15_FX.get('mut')
        if mut is None:
            mut = os.path.join(TD, 'drv', 't15_mut_fsr.py')
            with open(mut, 'w', encoding='utf-8') as f:
                f.write(t15_mutant_text()[0])
            T15_FX['mut'] = mut
    mfile = machine_file('A', ('%032x' % (abs(hash('A')) % (16 ** 32))))
    t_launch = time.time_ns()
    r = subprocess.run([sys.executable, drv, code_dir, SCRIPTS, store, mfile, t15_inputs_file(), mode, mut], capture_output=True, text=True,
                       timeout=600, stdin=subprocess.DEVNULL)
    m = [ln for ln in (r.stdout or '').splitlines() if ln.startswith('T15DRV ')]
    got = json.loads(m[-1][7:]) if m else {}
    got.update(rc=r.returncode, err=(r.stderr or '')[-300:], t_launch=t_launch)
    return got


@case('T15 런 도중 코드 바뀜 = 저장하지 않음 (11-12 2 회차 재리뷰 RCP2-01)')
def t15():
    if not need_cs('T15'):
        return
    import hashlib
    mut_src, n_line = t15_mutant_text()
    orig_fp = build_of(dense_inputs(7))()['fp']['registry'][:16]

    def cc(g):
        return isinstance(g.get('why'), str) and g['why'].startswith('code_changed')
    #  (a) 재리뷰 CE-A — fibre_segment_raster 를 원판으로 불러 둔 뒤 같은 자리를 CE1 변이판으로 바꾸고 Store → 옛 판 = 변이판 열쇠에 원판 원장을 저장 ·
    #      뒤의 정직한 런 (디스크 = 변이판) 이 적중으로 받았다 (재리뷰 실측 f24cbd6245dc · 833 위치 ↔ 그 판의 원장 202eb91e965d · 1,911)
    sa, ca = new_store_dir('t15_a'), t15_code_dir('t15_a')
    ga = t15_run(ca, sa, 'ce_a')
    ga2 = t15_run(ca, sa, 'honest')                             # 새 프로세스 · 디스크 = 변이판 (정직한 런)
    ga3 = t15_run(ca, sa, 'honest')
    chk('T15a 재리뷰 CE-A (fibre_segment_raster 를 먼저 불러 둠 → 런 시작 뒤 그 파일이 변이판으로 → Store) → 저장 안 함 (꺼짐 · 사유 code_changed · 짓기 1 회 · '
        '폴더 빈 채) · 뒤의 정직한 새 프로세스 (변이판) = 적중 아님 (새로 지어 씀) · 그 다음 = 적중 · 받은 원장 = 변이판으로 지은 원장 (≠ 원판 원장)',
        n_line == 1 and ga.get('rc') == 0 and ga.get('status') == 'disabled' and cc(ga) and ga.get('builds') == 1 and ga.get('files') == []
        and ga2.get('status') == 'built_written' and ga2.get('reg_fp') == ga2.get('fresh_fp') != orig_fp
        and ga3.get('status') == 'hit' and ga3.get('builds') == 0 and ga3.get('reg_fp') == ga3.get('fresh_fp') and len(ga3.get('files') or []) == 1,
        (ga, ga2.get('status'), ga2.get('reg_fp'), ga3.get('status'), ga3.get('reg_fp'), ga3.get('fresh_fp'), orig_fp))
    #  (b) cjunc_store 만 불러 둔 뒤 (원장 모듈 아직 안 불림) 바꿈 → Store → 저장 안 함 (브리프 꼴: 시작 뒤 열쇠 코드 파일 하나를 바꿈)
    sb, cb = new_store_dir('t15_b'), t15_code_dir('t15_b')
    gb = t15_run(cb, sb, 'before_store')
    chk('T15b 런 시작 (cjunc_store 를 불러온 때) 뒤 열쇠 코드 파일 하나 (fibre_segment_raster) 를 바꾸고 Store → 저장 안 함 (꺼짐 · code_changed · 짓기 1 회 · '
        '폴더 빈 채 · 런 결과 = 지은 원장)',
        gb.get('rc') == 0 and gb.get('status') == 'disabled' and cc(gb) and gb.get('builds') == 1 and gb.get('files') == []
        and gb.get('reg_fp') == gb.get('fresh_fp'), gb)
    #  (c) Store 뒤 짓는 도중 바뀜 (fibre_segment_raster 는 아직 안 불림 → 짓기가 변이판을 부른다 = 열쇠 (원판) ↔ 원장 (변이판)) → 발행 직전 다시 셈이
    #      잡는다 · 그 폴더를 원판 코드로 다시 연 정직한 런 = 적중 아님 (옛 판 = 원판 열쇠로 변이판 원장을 적중으로 받았다)
    sc, cc_dir = new_store_dir('t15_c'), t15_code_dir('t15_c')
    gc_ = t15_run(cc_dir, sc, 'during_build')
    gc2 = t15_run(t15_code_dir('t15_c_orig'), sc, 'honest')
    chk('T15c Store 뒤 짓는 도중 열쇠 코드 파일이 바뀜 (짓기가 새 판을 불러 씀) → 발행 직전 다시 셈 ≠ 런 시작 → 저장 안 함 (건너뜀 · code_changed · 임시 파일 '
        '없음) · 그 폴더를 원판 코드의 정직한 새 프로세스가 열면 새로 지어 씀 (받은 원장 = 원판 원장)',
        gc_.get('rc') == 0 and gc_.get('status') == 'built_write_skipped' and cc(gc_) and gc_.get('builds') == 1 and gc_.get('files') == []
        and gc2.get('status') == 'built_written' and gc2.get('reg_fp') == gc2.get('fresh_fp') == orig_fp,
        (gc_, gc2.get('status'), gc2.get('reg_fp'), orig_fp))
    #  (d) 쓰는 도중 바뀜 (발행 직전 다시 셈만 잡는다 — 짓기 · 열쇠는 같은 판)
    sd_, cd_ = new_store_dir('t15_d'), t15_code_dir('t15_d')
    gd = t15_run(cd_, sd_, 'during_write')
    chk('T15d 쓰는 도중 (임시 파일 쓰기 · 발행 전) 열쇠 코드 파일이 바뀜 → 발행 직전 다시 셈이 잡는다 → 저장 안 함 (건너뜀 · code_changed · 임시 파일 없음 · '
        '런 결과 = 지은 원장)', gd.get('rc') == 0 and gd.get('status') == 'built_write_skipped' and cc(gd) and gd.get('files') == []
        and gd.get('reg_fp') == gd.get('fresh_fp') == orig_fp, gd)
    #  (e) 내용 그대로 다시 씀 · 수정 시각 = 런 시작 뒤 (뒤집었다 되돌린 꼴 — 그 사이에 불린 모듈은 다른 판일 수 있다) → 꺼짐
    se_, ce_ = new_store_dir('t15_e'), t15_code_dir('t15_e')
    ge = t15_run(ce_, se_, 'touch')
    chk('T15e 열쇠 코드 파일을 내용 그대로 다시 씀 · 수정 시각 = 런 시작 뒤 (뒤집었다 되돌린 꼴) → 저장 안 함 (꺼짐 · code_changed)',
        ge.get('rc') == 0 and ge.get('status') == 'disabled' and cc(ge) and ge.get('files') == [], ge)
    #  (f) 정직한 흐름 그대로 + 런 시작 기록 (모듈을 불러온 때의 시각 · 디스크 sha · 먼저 불린 원장 모듈)
    sf, cf = new_store_dir('t15_f'), t15_code_dir('t15_f')
    gf = t15_run(cf, sf, 'honest')
    gf2 = t15_run(cf, sf, 'honest')
    want = {fn: hashlib.sha256(open(os.path.join(cf, fn), 'rb').read()).hexdigest() for fn in KEY_CODE_FILES}
    s1 = gf.get('start') or {}
    chk('T15f 정직한 흐름 (코드 안 바뀜) = 지어 씀 → 다음 새 프로세스 적중 (짓기 0 회 · 같은 원장) · 런 시작 기록 = cjunc_store 를 불러온 때 (띄우기 직전 ≤ 시각 ≤ '
        '불러온 직후) · 코드 칸 = 네 파일의 디스크 sha256 · 먼저 불린 원장 모듈 없음 (CE-A 꼴 = fibre_segment_raster 하나)',
        gf.get('status') == 'built_written' and gf2.get('status') == 'hit' and gf2.get('builds') == 0 and gf2.get('reg_fp') == gf.get('reg_fp') == orig_fp
        and isinstance(s1.get('t_ns'), int) and gf['t_launch'] <= s1['t_ns'] <= gf['t_after_import'] and s1.get('code') == want
        and s1.get('preloaded') == [] and s1.get('error') is None
        and ((ga.get('start') or {}).get('preloaded') == ['fibre_segment_raster']),
        (gf.get('status'), gf2.get('status'), s1, gf.get('t_launch'), gf.get('t_after_import'), (ga.get('start') or {}).get('preloaded')))
    #  ★ 3 회차 (내부 반박 리뷰 재확인 2 RCP3-02) — 코드 칸 = 파일별 stat 신원 (장치 · inode · 크기 · 수정 시각 ns · 상태 시각 ns) 정확 대조 + Store 코드 칸 =
    #    런 시작 코드 칸일 때만 읽고 쓴다.  옛 판 = 수정 시각을 시작 + 1 s 와 견줌 (벽시계) → 아래 (g) (h) (i) 를 놓치고 (j) 를 거짓으로 껐다.
    #  (g) 같은 초 뒤집기 — 변이판을 불러 쓴 뒤 원판 바이트로 되돌려 씀 · 수정 시각 = 런 시작 (재확인 2 samesec: 변이판 원장을 원판 열쇠로 저장 → 원판 정직한 런 적중)
    sg, cg_ = new_store_dir('t15_g'), t15_code_dir('t15_g')
    gg = t15_run(cg_, sg, 'samesec')
    gg2 = t15_run(t15_code_dir('t15_g_orig'), sg, 'honest')
    chk('T15g 같은 초 뒤집기 (런 시작 뒤 변이판 → 불러옴 → 원판 바이트로 되돌려 씀 · 수정 시각 = 런 시작 — 옛 1 s 여유 안) → 저장 안 함 (꺼짐 · code_changed · '
        '폴더 빈 채) · 그 폴더를 원판 코드로 연 정직한 새 프로세스 = 새로 지어 씀 (받은 원장 = 원판 원장 · 옛 판 = 변이판 원장 적중)',
        gg.get('rc') == 0 and gg.get('status') in ('disabled', 'built_write_skipped') and cc(gg) and gg.get('files') == []
        and gg2.get('status') == 'built_written' and gg2.get('reg_fp') == gg2.get('fresh_fp') == orig_fp,
        (gg.get('status'), gg.get('why'), gg.get('files'), gg2.get('status'), gg2.get('reg_fp'), orig_fp, gg.get('err')))
    #  (h) 변이판일 때 Store (열쇠 코드 칸 = 변이판) → 같은 초 안에 원판으로 되돌림 → 짓기 = 원판 (재확인 2 samesec_store)
    sh_, ch_ = new_store_dir('t15_h'), t15_code_dir('t15_h')
    gh = t15_run(ch_, sh_, 'samesec_store')
    gh2 = t15_run(t15_code_dir('t15_h_mut', fsr_text=mut_src), sh_, 'honest')
    chk('T15h Store 를 변이판일 때 만들고 (열쇠 코드 칸 = 변이판) 원판으로 되돌려 씀 (수정 시각 = 런 시작) → 저장 안 함 (꺼짐 · code_changed — Store 코드 칸 '
        '≠ 런 시작 · stat 신원) · 그 폴더를 변이판 코드로 연 정직한 런 = 새로 지어 씀 (받은 원장 = 변이판 원장 · 옛 판 = 원판 원장 적중)',
        gh.get('rc') == 0 and gh.get('status') == 'disabled' and cc(gh) and gh.get('files') == []
        and gh2.get('status') == 'built_written' and gh2.get('reg_fp') == gh2.get('fresh_fp') != orig_fp,
        (gh.get('status'), gh.get('why'), gh.get('files'), gh2.get('status'), gh2.get('reg_fp'), gh2.get('fresh_fp'), gh.get('err')))
    #  (i) 수정 시각을 되돌린 뒤집기 (os.utime — 옛 한정 (나)) — ctime · inode 는 utime 으로 못 되돌린다
    si, ci = new_store_dir('t15_i'), t15_code_dir('t15_i')
    gi = t15_run(ci, si, 'mtime_restore')
    gi2 = t15_run(t15_code_dir('t15_i_orig'), si, 'honest')
    chk('T15i 수정 시각을 되돌린 뒤집기 (변이판 → 불러옴 → 1.2 s 뒤 원판 바이트 + 원래 수정 시각 · os.utime — 옛 한정 (나)) → 저장 안 함 (꺼짐 · code_changed · '
        'inode · 상태 시각) · 원판 코드의 정직한 런 = 새로 지어 씀 (받은 원장 = 원판 원장)',
        gi.get('rc') == 0 and gi.get('status') in ('disabled', 'built_write_skipped') and cc(gi) and gi.get('files') == []
        and gi2.get('status') == 'built_written' and gi2.get('reg_fp') == gi2.get('fresh_fp') == orig_fp,
        (gi.get('status'), gi.get('why'), gi.get('files'), gi2.get('status'), gi2.get('reg_fp'), gi.get('err')))
    #  (j) 수정 시각이 미래인 사본 (다른 기계에서 rsync -t 로 옮긴 꼴 · 내용 · 자리 그대로) 의 정직한 런 — 옛 판 = 정직한 런마다 꺼짐 (재확인 2 future mtime)
    sj, cj_ = new_store_dir('t15_j'), t15_code_dir('t15_j')
    fut = time.time_ns() + 3600 * 10 ** 9
    for fn in KEY_CODE_FILES:
        os.utime(os.path.join(cj_, fn), ns=(fut, fut))
    gj = t15_run(cj_, sj, 'honest')
    gj2 = t15_run(cj_, sj, 'honest')
    chk('T15j 열쇠 코드 파일 넷의 수정 시각이 미래 (+1 h · 다른 기계에서 rsync -t 로 옮긴 꼴 · 내용 · 자리 그대로) 인 정직한 런 = 지어 씀 → 다음 새 프로세스 '
        '적중 (짓기 0 회 · 같은 원장 — 벽시계와 견주지 않는다 · 옛 판 = 정직한 런마다 꺼짐)',
        gj.get('status') == 'built_written' and gj2.get('status') == 'hit' and gj2.get('builds') == 0
        and gj2.get('reg_fp') == gj.get('reg_fp') == orig_fp, (gj.get('status'), gj.get('why'), gj2.get('status'), gj2.get('why')))
    #  (k) Store 코드 칸 ≠ 런 시작 코드 칸 (손으로 고친 꼴 · 디스크 그대로) — 그 가드만 판별
    sk, ck = new_store_dir('t15_k'), t15_code_dir('t15_k')
    gk = t15_run(ck, sk, 'store_code_differs')
    chk('T15k Store 코드 칸 ≠ 런 시작 코드 칸 (Store 를 만든 뒤 칸 하나를 손으로 바꿈 · 디스크 그대로) → 저장 안 함 (꺼짐 · code_changed · 짓기 1 회 · 폴더 빈 채)',
        gk.get('rc') == 0 and gk.get('status') == 'disabled' and cc(gk) and gk.get('builds') == 1 and gk.get('files') == [],
        (gk.get('status'), gk.get('why'), gk.get('files'), gk.get('err')))
    #  (l) ★ 3 회차 변이 보강 — 제자리 되돌림 (`cp -p` 꼴 · 같은 inode · 같은 크기 · 원래 수정 시각 = 다른 것은 상태 바뀐 시각뿐)
    sl, cl = new_store_dir('t15_l'), t15_code_dir('t15_l')
    gl = t15_run(cl, sl, 'inplace_restore')
    gl2 = t15_run(t15_code_dir('t15_l_orig'), sl, 'honest')
    chk('T15l 제자리 되돌림 (있는 파일에 변이판 → 불러옴 → 1.2 s 뒤 원판 바이트 + 원래 수정 시각 · inode · 크기 같음 = 상태 바뀐 시각만 다름) → 저장 안 함 '
        '(꺼짐 · code_changed) · 원판 코드의 정직한 런 = 새로 지어 씀 (받은 원장 = 원판 원장)',
        gl.get('rc') == 0 and gl.get('same_id') == {'ino': True, 'size': True, 'mtime': True, 'ctime': False}
        and gl.get('status') in ('disabled', 'built_write_skipped') and cc(gl) and gl.get('files') == []
        and gl2.get('status') == 'built_written' and gl2.get('reg_fp') == gl2.get('fresh_fp') == orig_fp,
        (gl.get('same_id'), gl.get('status'), gl.get('why'), gl.get('files'), gl2.get('status'), gl.get('err')))
    #  (m) ★ 3 회차 변이 보강 — 코드 칸을 재는 도중 파일이 바뀌면 (해시 앞뒤 stat 신원 다름) 못 셈 = OSError (시작 기록 = 오류 → 저장본 꺼짐) · 같은 프로세스 ·
    #      코드 사본 (code_file 을 사본으로 돌린다 · 리포 파일은 건드리지 않는다)
    cm = t15_code_dir('t15_m')
    o_cf, o_fs = CS.code_file, CS._file_sha
    race_err, plain = None, None
    try:
        CS.code_file = lambda m: os.path.join(cm, m + '.py')

        def racy(p):
            h = o_fs(p)
            if os.path.basename(p) == 'fibre_segment_raster.py':
                s_ = os.stat(p)
                os.utime(p, ns=(s_.st_atime_ns, s_.st_mtime_ns + 1000))
            return h
        CS._file_sha = racy
        try:
            CS._code_column()
        except OSError as e:
            race_err = str(e)
        CS._file_sha = o_fs
        plain = CS._code_column()
    finally:
        CS.code_file, CS._file_sha = o_cf, o_fs
    chk('T15m 코드 칸을 재는 도중 열쇠 코드 파일이 바뀜 (해시 앞뒤 stat 신원 다름) → OSError (런 시작이면 못 셈 = 저장본 꺼짐) · 안 바뀌면 칸 셋 (sha · 실경로 · '
        'stat 신원) 을 낸다 (3 회차 변이 보강 — 그 검사를 지운 변이가 안 잡혔다)',
        isinstance(race_err, str) and '재는 도중' in race_err and isinstance(plain, tuple) and len(plain) == 3
        and set(plain[2]) == set(KEY_CODE_FILES), (race_err, None if plain is None else sorted(plain[2])))


# ═════════════════════════ P — payload 끝-끝 ═════════════════════════
def make_fixture_series3(B6, d):
    """b6 픽스처 (세로 VGCF 두 가닥 · 접합 하나) 의 위 가닥을 둘로 가른 침대 — 세 가닥 직렬 (아래 판 ↔ 접합 ↔ 접합 ↔ 위 판) = instance 둘
    (실침대처럼 pair_i · pair_j 가 별칭인 원장).  행 차례 = SE · V1 · V2 · V3 · PTFE · SDCP (fid 마다 붙어 있다)."""
    B6.make_fixture(d, sdcp=True)
    pts, ph = np.load(os.path.join(d, 'se.npy')), np.load(os.path.join(d, 'phase.npy'))
    fid, kind = np.load(os.path.join(d, 'fibre.npy')), np.load(os.path.join(d, 'fibre_kind.npy'))
    v2 = np.flatnonzero((ph == 2) & (fid == 1))
    assert len(v2) == 37 and np.all(np.diff(v2) == 1), 'b6 픽스처 꼴이 바뀌었다 (V2 = 37 점 한 덩어리)'
    a, b = int(v2[0]), int(v2[-1]) + 1
    n2a = B6._box(B6.line((24.5, 24.5, 12.5), (24.5, 24.5, 18.5), 21))
    n2b = B6._box(B6.line((24.5, 24.5, 18.5), (24.5, 24.5, 23.2), 17))
    new_fid = int(fid.max()) + 1

    def splice(arr, mid_a, mid_b):
        return np.concatenate([arr[:a], mid_a, mid_b, arr[b:]])
    np.save(os.path.join(d, 'se.npy'), splice(pts, n2a, n2b))
    np.save(os.path.join(d, 'phase.npy'), splice(ph, np.full(len(n2a), 2, ph.dtype), np.full(len(n2b), 2, ph.dtype)))
    np.save(os.path.join(d, 'fibre.npy'), splice(fid, np.full(len(n2a), 1, fid.dtype), np.full(len(n2b), new_fid, fid.dtype)))
    np.save(os.path.join(d, 'fibre_kind.npy'), splice(kind, np.full(len(n2a), 1, kind.dtype), np.full(len(n2b), 1, kind.dtype)))
    np.save(os.path.join(d, 'fibre_dia.npy'), np.ones(len(pts) - (b - a) + len(n2a) + len(n2b)))
    return d


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
    os.makedirs(os.path.join(wd, 'rel_store'))                 # 있는 폴더 (payload cwd 기준 상대 경로) — 절대 경로 검사만 걸린다
    os.chmod(os.path.join(wd, 'rel_store'), 0o755)
    sdn = new_store_dir('pay_norm')                            # ★ 2 회차 RCP2-02 — 정규화 안 된 꼴 갈래의 폴더 (따로 · 고치기 전 판이 받아 쓰더라도 sd 를 안 건드린다)
    refuse = {'FLAG_WITHOUT_CJUNC': (B6.OFF + B6.LEAN2 + ['--step3-cjunc-store', sd], 'FLAG_WITHOUT_CJUNC'),
              'STORE_GRAPH_ONLY': (base + ['--step3-cjunc-graph-only', '--step3-cjunc-store', sd], 'STORE_GRAPH_ONLY'),
              #  ★ 11-12 (내부 반박 리뷰 RCP-10) — rasterize-only 는 접합 준비 전에 끝난다 = 저장본 인자가 조용히 안 쓰인다 → 거부 (조립만과 같은 줄)
              'STORE_RASTERIZE_ONLY': (base + ['--step3-rasterize-only', 'rast_refuse.json', '--step3-cjunc-store', sd], 'STORE_RASTERIZE_ONLY'),
              'STORE_PATH 상대': (base + ['--step3-cjunc-store', 'rel_store'], 'STORE_PATH'),
              'STORE_PATH 없음': (base + ['--step3-cjunc-store', os.path.join(sd, 'nope')], 'STORE_PATH'),
              'STORE_PATH 남이 씀': (base + ['--step3-cjunc-store', gw], 'STORE_PATH'),
              #  ★ 11-12 2 회차 (재리뷰 RCP2-02) — 정규화 안 된 꼴 (`<폴더>/.`) = 링크 검사를 비켜 가는 꼴 → 런 전 거부
              'STORE_PATH 정규화 아님': (base + ['--step3-cjunc-store', sdn + '/.'], 'STORE_PATH')}
    bad = {}
    rast = os.path.join(wd, 'rast_refuse.json')
    for i, (nm, (extra, code)) in enumerate(refuse.items()):
        rc, log, _d = B6.run_payload(wd, extra, out=f'refuse_{i}.json')
        made_rast = os.path.exists(rast)
        if made_rast:
            os.unlink(rast)                                        # 다음 갈래가 이 파일을 보지 않게 (이 갈래의 실패로만 센다)
        if not (rc != 0 and f'S2_CJUNC_REFUSED|{code}|' in log and not os.path.exists(os.path.join(wd, f'refuse_{i}.json')) and not made_rast):
            bad[nm] = (rc, made_rast, log.strip()[-200:])
    chk('P1 입구 거부 일곱 (접합 없이 · 조립만과 함께 · rasterize-only 와 함께 (RCP-10) · 상대 · 없는 폴더 · 남이 쓸 수 있는 폴더 · 정규화 안 된 꼴 '
        '(2 회차 RCP2-02)) → rc ≠ 0 · S2_CJUNC_REFUSED|<코드>| · 출력 없음 (rasterize 원장도) · 저장 폴더 빈 채',
        not bad and len(refuse) == 7 and store_files(sd) == [] and store_files(sdn) == [], (bad, store_files(sd), store_files(sdn)))
    #  ★ 11-12 (내부 반박 리뷰 RCP-10) — Store() 의 ValueError 밖 예외 (코드 파일을 못 읽음 OSError 꼴) 도 구조화 거부 STORE_PATH (traceback 아님) —
    #    입구 계약 (첫 Store) · 본 길 (둘째 Store · 접합 준비 직전) 두 자리 다.  감싸개 = Store.__init__ 을 바꿔 끼운 뒤 같은 payload 를 runpy 로.
    bad_b = {}
    for which in (1, 2):
        drv = os.path.join(TD, 'drv', f'store_boom_{which}.py')
        with open(drv, 'w', encoding='utf-8') as f:
            f.write(STORE_BOOM_DRIVER.replace('__SCRIPTS__', repr(SCRIPTS)).replace('__PAYLOAD__', repr(os.path.join(SCRIPTS, 'mpm_webapp_payload.py')))
                    .replace('__WHICH__', str(which)))
        rc, log, _d = B6.run_payload(wd, base + ['--step3-cjunc-store', sd], out=f'boom_{which}.json', payload=drv)
        if not (rc != 0 and 'S2_CJUNC_REFUSED|STORE_PATH|' in log and 'OSError' in log and 'Traceback' not in log
                and not os.path.exists(os.path.join(wd, f'boom_{which}.json'))):
            bad_b[which] = (rc, log.strip()[-300:])
    chk('P1b Store() 의 뜻밖의 예외 (OSError · 코드 파일을 못 읽음 꼴) → 입구 계약 · 본 길 둘 다 rc ≠ 0 · S2_CJUNC_REFUSED|STORE_PATH| (예외 형 이름 포함) · '
        'traceback 없음 · 출력 없음 · 저장 폴더 빈 채 (RCP-10)', not bad_b and store_files(sd) == [], (bad_b, store_files(sd)))
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
    #  ★ P5 (대피 세션 11-12) — instance 둘 (세 가닥 직렬 = pair_i · pair_j 별칭이 있는 원장 · 실침대 꼴) 도 지어 쓰고 다음 팔이 읽는다
    wd3 = os.path.join(TD, 'payload3')
    os.makedirs(wd3)
    make_fixture_series3(B6, wd3)
    sd3 = new_store_dir('pay3')
    rca, loga, _da = B6.run_payload(wd3, base, out='q_off.json')
    rcb, logb, _db = B6.run_payload(wd3, base + ['--step3-cjunc-store', sd3], out='q_on1.json')
    files3 = store_files(sd3)
    rcc, logc, _dc = B6.run_payload(wd3, base + ['--step3-cjunc-store', sd3], out='q_on2.json')

    def rb3(nm):
        p = os.path.join(wd3, nm)
        return open(p, 'rb').read() if os.path.exists(p) else None
    qa, qb, qc = rb3('q_off.json'), rb3('q_on1.json'), rb3('q_on2.json')
    chk('P5 instance 둘인 침대 (세 가닥 직렬) — 끔 · 켬 (빗나감) · 켬 (적중) rc 0 셋 · payload 가 instance 2 를 찍는다 · 팔 JSON 바이트 같음 셋 · '
        '첫 켬 = 새로 지어 저장 (⚠ 줄 없음 — 넘겨받은 판 = 별칭 거부로 저장 안 함) · 둘째 = 읽음 · 저장본 파일 하나',
        rca == rcb == rcc == 0 and 'instance 2 (' in loga and qa is not None and qa == qb == qc and '새로 지어 저장' in logb
        and not [ln for ln in logb.splitlines() if '저장본' in ln and '⚠' in ln] and '읽음' in logc and len(files3) == 1
        and store_files(sd3) == files3,
        (rca, rcb, rcc, 'instance 2 (' in loga, qa == qb, qb == qc, files3, [ln for ln in (logb + logc).splitlines() if '저장본' in ln]))
    #  ★ P6 (11-12 2 회차 · 재리뷰 RCP2-01) — 런 시작 코드 칸 = cjunc_store 를 처음 불러온 때.  payload (저장본 켬) 는 입구 계약에서 cjunc_store 를
    #    원장 모듈 셋 (carbon_junction · step3_sigma · fibre_segment_raster) 보다 **먼저** 부른다 — 그래야 시작 칸이 런의 모든 원장 코드 적재 앞이다
    #    (`python -X importtime` 의 끝난 차례 · 실제 payload).  이 차례가 바뀌면 (먼저 불린 원장 모듈의 시작 전 바뀜) 저장본이 못 가린다 = 한정.
    sd6 = new_store_dir('pay6')
    pargs = ['--scaffold', 'am.csv', '--se', 'se.npy', '--phase', 'phase.npy', '--fibre', 'fibre.npy', '--fibre-dia', 'fibre_dia.npy',
             '--n-vox', '24', '--step3-vox', '1.0', '--step3-fibre-stamp', 'segment']
    r6 = subprocess.run([sys.executable, '-X', 'importtime', os.path.join(SCRIPTS, 'mpm_webapp_payload.py'), *pargs, '--out', 'p_order.json',
                         '--show-results', *base, '--step3-cjunc-store', sd6], capture_output=True, text=True, timeout=900, cwd=wd,
                        stdin=subprocess.DEVNULL)
    order = []
    for ln in (r6.stderr or '').splitlines():
        mm = re.match(r'import time:\s+\d+ \|\s+\d+ \|\s*(\S+)\s*$', ln)
        if mm and mm.group(1) in KEY_MODULES and mm.group(1) not in order:
            order.append(mm.group(1))
    chk('P6 payload (저장본 켬) 가 cjunc_store 를 원장 모듈 셋보다 먼저 불러온다 (python -X importtime 끝난 차례 · 넷 다 불림) · rc 0 · 새로 지어 저장 줄 '
        '(런 시작 코드 칸 = 원장 코드 적재 앞 · 2 회차 RCP2-01)',
        r6.returncode == 0 and len(order) == 4 and order[0] == 'cjunc_store' and '새로 지어 저장' in (r6.stdout or ''),
        (r6.returncode, order, (r6.stdout or '')[-200:]))
    #  ★ P6b (3 회차 · 내부 반박 리뷰 재확인 2 RCP3-03) — 러너 꼴 인자 (`--expect-physics` 에 ca_ext.cjunc 칸 = 러너 NG_DECL) 의 payload 도 cjunc_store 를
    #    carbon_junction 보다 먼저 부른다 (옛 차례 = `ca_ext_protocol_fields` → ca_ext_cjunc 가 carbon_junction 먼저 → `_START['preloaded']` =
    #    ['carbon_junction'] · cjunc_store 머리 한정 (가) 의 "payload 는 그런 모듈이 없다" 가 거짓이었다) · 입구에서 멈춤 (솔브 없음)
    key6 = sorted(k for k in _RCG.ca_ext_protocol_fields() if k.startswith('ca_ext.cjunc.'))[0]
    sd6b = new_store_dir('pay6b')
    r6b = subprocess.run([sys.executable, '-c', P6B_CODE, SCRIPTS, sd6b, key6], capture_output=True, text=True, timeout=600, cwd=wd,
                         stdin=subprocess.DEVNULL)
    o6b = [ln for ln in (r6b.stdout or '').splitlines() if ln.startswith('P6B ')]
    o6b = json.loads(o6b[-1][4:]) if o6b else None
    chk('P6b 러너 꼴 인자 (--step3-cjunc --step3-cjunc-store <폴더> --expect-physics <ca_ext.cjunc 칸>=…) 의 payload — cjunc_store 가 carbon_junction 보다 '
        '먼저 불린다 (sys.modules 넣은 차례) · 런 시작 기록의 먼저 불린 열쇠 모듈 = 없음 · 입구에서 멈춤 (3 회차 RCP3-03)',
        isinstance(o6b, dict) and (o6b.get('start_order') or [None])[0] == 'cjunc_store' and 'carbon_junction' in (o6b.get('start_order') or [])
        and o6b.get('preloaded') == [] and o6b.get('exited') is True, (o6b, key6, (r6b.stderr or '')[-300:]))


#: ★ P6b (3 회차 RCP3-03) — 실제 payload 를 runpy (__main__) 로 러너 꼴 인자에 띄워 입구에서 멈춘 뒤 열쇠 모듈 넷의 불린 차례 (sys.modules 넣은 차례 =
#  import 시작 차례) · cjunc_store 런 시작 기록의 먼저 불린 열쇠 모듈을 적는다 (GPU · 솔브 없음)
P6B_CODE = r'''
import json, runpy, sys
scripts, store, key = sys.argv[1:4]
sys.path.insert(0, scripts)
sys.argv = ['mpm_webapp_payload.py', '--step3-cjunc', '--step3-cjunc-store', store, '--expect-physics', key + '=1']
exited = False
try:
    runpy.run_path(scripts + '/mpm_webapp_payload.py', run_name='__main__')
except SystemExit:
    exited = True
KEYM = ('carbon_junction', 'step3_sigma', 'fibre_segment_raster', 'cjunc_store')
cs = sys.modules.get('cjunc_store')
print('P6B ' + json.dumps({'start_order': [m for m in sys.modules if m in KEYM], 'exited': exited,
                           'preloaded': (cs._START.get('preloaded') if cs is not None else None)}))
'''


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
    sl = os.path.join(TD, 'stores', 'runner_link')               # ★ 11-12 (내부 반박 리뷰 RCP-06) — 뿌리가 심볼릭 링크 (가리키는 폴더는 꼴이 맞다)
    os.symlink(new_store_dir('runner_link_target'), sl)
    sdn = new_store_dir('runner_norm')                           # ★ 2 회차 RCP2-02 — 정규화 안 된 꼴 갈래의 실제 폴더 (sd 와 따로)
    bad = {}
    for nm, env, want in (('심볼릭 링크 폴더', dict(NR.CJ_RT_ENV, CJUNC_STORE=sl), 'CJUNC_STORE 가 심볼릭 링크'),
                          ('심볼릭 링크 폴더 (끝 빗금)', dict(NR.CJ_RT_ENV, CJUNC_STORE=sl + '/'), 'CJUNC_STORE 가 심볼릭 링크'),
                          ('CJUNC=1 없이', {'CJUNC_STORE': sd}, 'CJUNC_STORE 는 CJUNC=1'),
                          ('조립만과 함께', dict(NR.CJ_RT_ENV, CJUNC_SV_CF='1', CJUNC_GRAPH_ONLY='1', CJUNC_STORE=sd), 'CJUNC_GRAPH_ONLY'),
                          ('상대 경로', dict(NR.CJ_RT_ENV, CJUNC_STORE='rel/store'), 'CJUNC_STORE 는 절대 경로'),
                          ('허용 밖 글자 (빈칸)', dict(NR.CJ_RT_ENV, CJUNC_STORE=sd + ' x'), 'CJUNC_STORE 에 허용 밖'),
                          ('개행', dict(NR.CJ_RT_ENV, CJUNC_STORE=sd + '\n/tmp'), 'CJUNC_STORE 에 허용 밖'),
                          ('영문 아닌 글자', dict(NR.CJ_RT_ENV, CJUNC_STORE=sd + '/저장'), 'CJUNC_STORE 에 허용 밖'),
                          ('없는 폴더', dict(NR.CJ_RT_ENV, CJUNC_STORE=os.path.join(sd, 'nope')), 'CJUNC_STORE 폴더가 없다'),
                          #  ★ 11-12 2 회차 (재리뷰 RCP2-02) — 정규화 안 된 꼴 = 마지막 글자 성분의 링크 검사를 비켜 간다 (링크 · 실제 폴더 둘 다 거부)
                          ('심볼릭 링크 + /.', dict(NR.CJ_RT_ENV, CJUNC_STORE=sl + '/.'), 'CJUNC_STORE 경로가 정규화'),
                          ('심볼릭 링크 + /./', dict(NR.CJ_RT_ENV, CJUNC_STORE=sl + '/./'), 'CJUNC_STORE 경로가 정규화'),
                          ('실제 폴더 · 가운데 //', dict(NR.CJ_RT_ENV, CJUNC_STORE=sdn.replace('/stores/', '/stores//')), 'CJUNC_STORE 경로가 정규화'),
                          ('실제 폴더 · 가운데 /../', dict(NR.CJ_RT_ENV, CJUNC_STORE=sdn.replace('/stores/', '/stores/../stores/')),
                           'CJUNC_STORE 경로가 정규화')):
        r = NR.run_runner(ws, env)
        if not (r.rc != 0 and '[p2] ABORT' in r.log and want in r.log and not r.new_dirs and not r.argv):
            bad[nm] = (r.rc, r.log.strip()[-240:], r.new_dirs)
        NR.reset_ws(ws)
    chk('R1 발사 전 ABORT 열셋 (심볼릭 링크 둘 (RCP-06) · CJUNC=1 없이 · 조립만 · 상대 · 빈칸 · 개행 · 영문 아닌 글자 · 없는 폴더 · 정규화 안 된 꼴 넷 '
        '(2 회차 RCP2-02)) — rc ≠ 0 · 사유 글 · OUTDIR · payload 없음', not bad, bad)
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
    sp_dir = new_store_dir('chain has space')                  # 있는 폴더 · 허용 밖 글자 (빈칸 — 러너가 생성 스크립트에 박는 글자 규칙)
    ow = new_store_dir('chain_owner')                          # ★ 대피 4 덧 — 다른 소유자
    cl = os.path.join(TD, 'stores', 'chain_link')              # ★ 11-12 (내부 반박 리뷰 RCP-06) — 뿌리가 심볼릭 링크 (가리키는 폴더는 꼴이 맞다)
    os.symlink(new_store_dir('chain_link_target'), cl)
    errs = {}
    for nm, argv, want in (('심볼릭 링크 폴더', ['--stage', 'ladder', '--cjunc-store', cl], '--cjunc-store 는 심볼릭 링크'),
                           ('심볼릭 링크 폴더 (끝 빗금)', ['--stage', 'ladder', '--cjunc-store', cl + '/'], '--cjunc-store 는 심볼릭 링크'),
                           ('verdict 에 줌', ['--stage', 'verdict', '--cjunc-store', sd], '--cjunc-store 는 --stage ladder'),
                           ('plan-doc 에 줌', ['--stage', 'plan-doc', '--cjunc-store', sd], '--cjunc-store 는 --stage ladder'),
                           ('합치기 (predict --merge) 에 줌', ['--stage', 'predict', '--merge', 'x', '--cjunc-store', sd],
                            '--cjunc-store 는 --stage ladder'),
                           ('상대 경로 (있는 폴더)', ['--stage', 'ladder', '--cjunc-store', os.path.relpath(sd)], '--cjunc-store 는 절대 경로'),
                           ('허용 밖 글자 (빈칸 · 있는 폴더)', ['--stage', 'ladder', '--cjunc-store', sp_dir], '--cjunc-store 는 영문'),
                           ('없는 폴더', ['--stage', 'ladder', '--cjunc-store', os.path.join(sd, 'nope')], '--cjunc-store 는 있는 폴더'),
                           ('남이 쓸 수 있음', ['--stage', 'ladder', '--cjunc-store', gw], '--cjunc-store 는 그룹'),
                           ('다른 소유자', ['--stage', 'ladder', '--cjunc-store', ow], '--cjunc-store 는 이 사용자 소유'),
                           #  ★ 11-12 2 회차 (재리뷰 RCP2-02) — 정규화 안 된 꼴 (링크 · 실제 폴더) = 마지막 글자 성분의 링크 검사를 비켜 간다
                           ('심볼릭 링크 + /.', ['--stage', 'ladder', '--cjunc-store', cl + '/.'], '--cjunc-store 는 정규화된'),
                           ('심볼릭 링크 + /./', ['--stage', 'ladder', '--cjunc-store', cl + '/./'], '--cjunc-store 는 정규화된'),
                           ('실제 폴더 · 가운데 //', ['--stage', 'ladder', '--cjunc-store', sd.replace('/stores/', '/stores//')],
                            '--cjunc-store 는 정규화된'),
                           ('실제 폴더 · 가운데 /../', ['--stage', 'ladder', '--cjunc-store', sd.replace('/stores/', '/stores/../stores/')],
                            '--cjunc-store 는 정규화된')):
        buf = io.StringIO()
        with contextlib.redirect_stderr(buf), contextlib.redirect_stdout(buf), other_owner(ow if nm == '다른 소유자' else None):
            try:
                RR.main(argv)
                code = 0
            except SystemExit as e:
                code = e.code
        if not (code == 2 and want in buf.getvalue()):
            errs[nm] = (code, buf.getvalue().strip()[-200:])
    chk('C1 --cjunc-store 거부 열넷 (심볼릭 링크 둘 (RCP-06) · verdict · plan-doc · 합치기 · 상대 (있는 폴더) · 허용 밖 글자 · 없는 폴더 · 남이 쓸 수 '
        '있음 · 다른 소유자 · 정규화 안 된 꼴 넷 (2 회차 RCP2-02)) → argparse 오류 (rc 2 · 갈래마다 그 사유 글)', not errs, errs)
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
