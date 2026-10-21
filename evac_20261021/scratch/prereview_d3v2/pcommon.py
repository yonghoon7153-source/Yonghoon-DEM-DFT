"""PRE-D3V2 공용 — 규칙 검사 스크립트 (설계 v2 의 '실행 가능한 명세') 를 모듈로 불러온다 (읽기만 · 파일 쓰기 0).

REPO 환경변수 = 검토 대상 작업 트리 (기본 = 이 에이전트의 작업 트리 · 커밋 2f1d29d09).
"""
import importlib.util
import json
import math
import os
import sys

sys.dont_write_bytecode = True
REPO = os.environ.get('REPO', '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-adc256e40f2b17660')
EVID = os.path.join(REPO, 'docs/reviews/mixer_d3_design_v2_evidence_20261021/d3_v2_rule_checks.py')
HERE = os.path.dirname(os.path.abspath(__file__))


def load_checks():
    spec = importlib.util.spec_from_file_location('d3chk', EVID)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)            # 모듈 수준 = 생성기 · 검사기 함수 적재뿐 (main 은 __main__ 에서만)
    return mod


def dump(name, obj):
    with open(os.path.join(HERE, name), 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1, default=lambda o: repr(o))


def monotone_envelope_accept(xs, I, h, mm):
    """대조용 '정답' 규칙 (칸 안 단조 + 통계 띠 h): 칸 [x_k, x_k+1] 전체를 받는 것은 m ∈ [min − h, max + h] 일 때만.
    (칸 안 단조 곡선은 칸 안 아무 x 에서나 두 끝값 사이 어떤 값도 낼 수 있다 — 칸 밖 값은 못 낸다.)"""
    segs = []
    for k in range(len(xs) - 1):
        lo, hi = min(I[k], I[k + 1]) - h, max(I[k], I[k + 1]) + h
        if lo <= mm <= hi:
            segs.append((xs[k], xs[k + 1]))
    out = []
    for a, b in sorted(segs):
        if out and a <= out[-1][1] + 1e-12:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out
