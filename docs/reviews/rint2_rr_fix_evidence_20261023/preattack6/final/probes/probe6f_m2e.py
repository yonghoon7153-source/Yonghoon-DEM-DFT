#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""변이 M2e (다시 셈 칸에서 resume_ok 뺌) 가 상주 시험에서 살아남은 뜻 — 같은 프로세스 안에서 RECOUNT_KEYS 를 바꾼 사슬로 R11 꼴 (resume_ok 만 바꾼 끝 줄)
을 돌린다 (사슬 파일은 고치지 않는다 · 모듈 값만 이 프로세스에서).

  python3 -I docs/reviews/rint2_rr_fix_evidence_20261023/preattack6/final/probes/probe6f_m2e.py <임시 폴더 바탕>
"""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
spec = importlib.util.spec_from_file_location('probe6f_real', HERE.parent / 'probe6f_real.py')
P = importlib.util.module_from_spec(spec)
sys.argv = [sys.argv[0], sys.argv[1] if len(sys.argv) > 1 else '/tmp', 'R11']
spec.loader.exec_module(P)
P.RR.RECOUNT_KEYS = ('status', 'stop', 'side', 'cause')          # 변이 M2e
P.setup()
P.out('env_m2e', recount_keys=list(P.RR.RECOUNT_KEYS))
P.r11()
