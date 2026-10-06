"""[RED 껍데기 — 함수 몸체 없음] REIL C5 비용 파일럿 — 셀 #1 · A0 · J_V = sqrt(f2) · Phase A 128 지역 실행 (COBYQA) 의 **비용**만 잰다.

승인 · 범위: `docs/REIL_C5_PILOT_APPROVAL_REQUEST_v2_20261006.md` (§1–§8) + 부록 `…_v2_ADDENDUM_20261006.md` (A1–A4) · 상태 §28.
결과는 확인적 분석에 쓰지 않는다 (바꿀 수 있는 것은 C4 의 벽시계 예산표와 병렬 수뿐 — v2 §8).

    <venv>/bin/python -I bms-balancing/scripts/reil_c5_pilot.py identity --venv <venv> --out <file.json>
    <venv>/bin/python -I bms-balancing/scripts/reil_c5_pilot.py dryrun   --venv <venv> --out <dir>
    <venv>/bin/python -I bms-balancing/scripts/reil_c5_pilot.py measure  --venv <venv> --out <dir> --xlsx <xlsx> --util <util_LFP.py> --approval <상태 문서 절>

- `identity` 는 **계산 없는 환경 식별**이다 (부록 A1): 실제 interpreter · 설치 파일 RECORD 해시 대조 (`lock_text`) · 판 메타데이터
  (`profile`) · COBYQA 옵션 표 · 구현 파일 재해시 · 봉인 MANIFEST. 합성 최적화 (`cobyqa_options`) · Sobol 생성 (`sobol`) · `emit` ·
  full C6 `check` 는 부르지 않는다 — full check 는 `NOT_RUN` 으로 남는다.
- `dryrun` 은 보존된 util 사본 · 해석식 합성 곡선 · fixture Sobol (rng 20261006 · 정식 배열 아님) 로 경로만 지난다 (시간 숫자는 비용 근거 아님).
- `measure` 는 v2 §10 (2) 의 별도 승인 뒤에만 쓴다. 측정 단계의 Sobol 은 A0 seed 0 · 1 배열만 다시 만들어 봉인과 바이트 대조한다.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.machinery
import importlib.util
import io
import json
import math
import os
import queue
import shutil
import subprocess
import sys
import time
import traceback
import warnings
from collections import Counter
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve()
BMS = HERE.parents[1]
REPO = HERE.parents[2]


def _sibling(name: str):
    """같은 폴더의 봉인 · P0 스크립트를 경로로 읽는다 (`-I` 실행에서도 · 패키지 import 에 기대지 않음)."""
    spec = importlib.util.spec_from_file_location(f"reil_c5_sibling_{name}", HERE.parent / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


prof = _sibling("reil_c6_profile")
p0 = _sibling("reil_p0")

#: v2 §1 — C6 봉인 `COBYQA_OPTIONS.json` 의 `options` 와 같은 8 개 (실행 때 대조 · 판 기본값에 기대지 않음)
OPTIONS = dict(prof.COBYQA_OPTIONS)
#: A0 상자 (십진 문자열 = 정확 유리수) · G: d_P − d_N ≥ 1e-4 · 증인 허용치 1e-10 (부속 A §2-1)
LO = ("0.6", "0.5", "0.005", "0")
HI = ("1.1", "1.1", "0.5", "1")
G_LB = Fraction("1e-4")
TOL = Fraction("1e-10")
SEALED = BMS / "reil_c6_rebuild_20261006"
PILOT_ARRAYS = {0: "sobol_A0_their_box_seed0.npy", 1: "sobol_A0_their_box_seed1.npy"}
SOBOL_N = 64
UTIL_SHA = p0.SHA_UTIL
XLSX_SHA = p0.SHA_XLSX
UTIL_COPY = BMS / "reviews" / "prereview_pybamm_reil_20261003" / "external" / "util_LFP.py.txt"
UTIL_COPY_SHA = "bdf78273d50f40ce3154d01a3ef8d36f0f5ea5ec1b04539584809d7b19b46f9c"
P0_RESULT = BMS / "evidence" / "reil_p0_20261006" / "P0_RESULT.json"
CELL_ROW = 1                       # #1 LLI-1 (v2 §1 · 규칙으로 다시 고른다)
BOUNDARY_ROWS = frozenset({0, 4, 5})
FIXTURE_SOBOL_RNG = 20261006       # 건조 실행 · 시험용 — 정식 배열 아님
BLAS_VARS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")
DATA_SUFFIXES = (".xlsx", ".pkl", ".ipynb")
STRUCTURAL = (MemoryError, OSError, KeyboardInterrupt, SystemExit, RecursionError)
STATES = ("NOT_STARTED", "STARTED_INTERRUPTED", "RETURNED_REEVAL_INTERRUPTED", "COMPLETED")
#: v2 §3 — 원점 = 부모 단조 시계 시작 (초)
LIMITS_MEASURE = {"prep": 600.0, "measure": 6300.0, "workers": 6420.0, "record": 6720.0, "total": 7200.0, "grace": 60.0,
                  "rss": 4 * 2 ** 30, "rss_gap": 5.0, "disk_new": 2 ** 30, "disk_free": 5 * 2 ** 30, "disk_gap": 15.0}
#: v2 §5 — 건조 실행: 벽시계 ≤ 300 s · 출력 ≤ 10 MB
LIMITS_DRY = {"prep": 60.0, "measure": 240.0, "workers": 255.0, "record": 280.0, "total": 300.0, "grace": 10.0,
              "rss": 4 * 2 ** 30, "rss_gap": 5.0, "disk_new": 10 * 2 ** 20, "disk_free": 5 * 2 ** 30, "disk_gap": 15.0}
DRY_OPTIONS = dict(OPTIONS, maxfev=50, maxiter=100)
N_WORKERS_MEASURE, N_WORKERS_DRY = 4, 2


class Structural(Exception):
    """구조 오류 — 파일럿 전체 중단 (v2 §2). `info` 는 `classify_exception` 의 결과."""

    def __init__(self, info: dict, partial: dict | None = None):
        super().__init__(info.get("message"))
        self.info = info
        self.partial = partial


class GlobalStop(Exception):
    """전역 중단 (v2 §6) — 식별 · 봉인 · 셀 규칙 · 경계 · 자원."""


# ---------------------------------------------------------------- RED 껍데기 (구현 전)
def _sibling(*a, **k):
    raise NotImplementedError('_sibling')


def _sha(*a, **k):
    raise NotImplementedError('_sha')


def frac_str(*a, **k):
    raise NotImplementedError('frac_str')


def _jsonable(*a, **k):
    raise NotImplementedError('_jsonable')


def dump(*a, **k):
    raise NotImplementedError('dump')


def model_digest(*a, **k):
    raise NotImplementedError('model_digest')


def exact_residuals(*a, **k):
    raise NotImplementedError('exact_residuals')


def witness(*a, **k):
    raise NotImplementedError('witness')


def feasibility_class(*a, **k):
    raise NotImplementedError('feasibility_class')


def termination_of(*a, **k):
    raise NotImplementedError('termination_of')


def _frame_kind(*a, **k):
    raise NotImplementedError('_frame_kind')


def classify_exception(*a, **k):
    raise NotImplementedError('classify_exception')


def n_out_labels(*a, **k):
    raise NotImplementedError('n_out_labels')


def run_one(*a, **k):
    raise NotImplementedError('run_one')


def _threads(*a, **k):
    raise NotImplementedError('_threads')


def rss_bytes(*a, **k):
    raise NotImplementedError('rss_bytes')


def disk_sample(*a, **k):
    raise NotImplementedError('disk_sample')


def _worker(*a, **k):
    raise NotImplementedError('_worker')


def assemble_states(*a, **k):
    raise NotImplementedError('assemble_states')


def orchestrate(*a, **k):
    raise NotImplementedError('orchestrate')


def _stats(*a, **k):
    raise NotImplementedError('_stats')


def summarize(*a, **k):
    raise NotImplementedError('summarize')


def _write_bytes(*a, **k):
    raise NotImplementedError('_write_bytes')


def final_record(*a, **k):
    raise NotImplementedError('final_record')


def git_state(*a, **k):
    raise NotImplementedError('git_state')


def split_dirty(*a, **k):
    raise NotImplementedError('split_dirty')


def source_hashes(*a, **k):
    raise NotImplementedError('source_hashes')


def source_changed(*a, **k):
    raise NotImplementedError('source_changed')


def check_options(*a, **k):
    raise NotImplementedError('check_options')


def env_identity(*a, **k):
    raise NotImplementedError('env_identity')


def pilot_arrays(*a, **k):
    raise NotImplementedError('pilot_arrays')


def plan_runs(*a, **k):
    raise NotImplementedError('plan_runs')


def fixture_starts(*a, **k):
    raise NotImplementedError('fixture_starts')


def select_cell(*a, **k):
    raise NotImplementedError('select_cell')


def require_cell(*a, **k):
    raise NotImplementedError('require_cell')


def guard_paths(*a, **k):
    raise NotImplementedError('guard_paths')


def load_util(*a, **k):
    raise NotImplementedError('load_util')


def synthetic_inputs(*a, **k):
    raise NotImplementedError('synthetic_inputs')


def run_pilot(*a, **k):
    raise NotImplementedError('run_pilot')


def _new_out(*a, **k):
    raise NotImplementedError('_new_out')


def cmd_identity(*a, **k):
    raise NotImplementedError('cmd_identity')


def cmd_dryrun(*a, **k):
    raise NotImplementedError('cmd_dryrun')


def load_measure_inputs(*a, **k):
    raise NotImplementedError('load_measure_inputs')


def cmd_measure(*a, **k):
    raise NotImplementedError('cmd_measure')


def main(*a, **k):
    raise NotImplementedError('main')


class Objective:
    def __init__(self, *a, **k):
        raise NotImplementedError('Objective')
