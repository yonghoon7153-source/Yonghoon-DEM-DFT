#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PC6-02 라이브러리 표지 (1저자 11-02) 뒤 — 열린 질문 꼴의 지금 분류 (읽기만 · 사슬 함수 `words_cause` · 값 · σ 없음 · 결정 아님).

  python3 -I docs/reviews/rint2_rr_fix_evidence_20261023/pc6_13_fix/probe_open_q.py

메모리 실패인데 자원 낱말 다섯 (`RESOURCE_WORDS`) 이 없는 꼴 → 이제 CUDA 표지 (runner_rc · 자동 재실행 없음) — 1저자 결정 문장 "자원 낱말 (out of memory 등)
을 먼저 보므로 메모리 부족은 그대로 resource" 는 자원 낱말이 함께 찍힌 줄 (cupy 꼴) 에서만 선다.  기본값 'D' = 그 길의 기본 원인 자리 표시.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / 'scripts'))
import rint_r_chain as RR  # noqa: E402

LINES = {
    'cupy_oom_class': 'cupy.cuda.memory.OutOfMemoryError: Out of memory allocating 4,000,000 bytes (allocated so far: 0 bytes).',
    'cupy_runtime_oom': 'cupy_backends.cuda.api.runtime.CUDARuntimeError: cudaErrorMemoryAllocation: out of memory',
    'cupy_driver_oom': 'cupy_backends.cuda.api.driver.CUDADriverError: CUDA_ERROR_OUT_OF_MEMORY: out of memory',
    'bare_cuda_error_oom': 'RuntimeError: CUDA error: out of memory',
    'torch_cuda_oom_class': 'torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 20.00 MiB',
    'cublas_alloc': 'cupy_backends.cuda.libs.cublas.CUBLASError: CUBLAS_STATUS_ALLOC_FAILED',
    'cusolver_alloc': 'cupy_backends.cuda.libs.cusolver.CUSOLVERError: CUSOLVER_STATUS_ALLOC_FAILED',
    'cusparse_alloc': 'cupy_backends.cuda.libs.cusparse.CuSparseError: CUSPARSE_STATUS_ALLOC_FAILED',
    'cusparse_insufficient': 'cupy_backends.cuda.libs.cusparse.CuSparseError: CUSPARSE_STATUS_INSUFFICIENT_RESOURCES',
    'cufft_alloc': 'cupy.cuda.cufft.CuFFTError: CUFFT_ALLOC_FAILED',
    'cuda_error_capital_E': 'CUDA Error: an illegal memory access was encountered',
    'cufft_benign_mention': 'env CUFFT_PLAN_CACHE_SIZE=16',
}
out = {'resource_words': list(RR.RESOURCE_WORDS), 'not_resource_words': list(RR.NOT_RESOURCE_WORDS), 'cuda_error_words': list(RR.CUDA_ERROR_WORDS),
       'rows': {k: RR.words_cause(v, 'D') for k, v in LINES.items()}}
print(json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True))
