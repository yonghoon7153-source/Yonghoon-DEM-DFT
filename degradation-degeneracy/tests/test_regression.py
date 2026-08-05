"""회귀 검증 (Phase 2) — 원본 코드의 디버그 블록과 동일한 검증.

원본 L142-152: Reference와 LLI=0(동일 파라미터)의 실측 용량이 같아야 한다.
차이 < 0.01 mAh. (원본 저자가 baseline 오염을 실제로 겪었다는 증거이므로
이 테스트가 특히 중요 — 02_CODE_AUDIT.md 5절)
"""

from __future__ import annotations

import pytest

from src.curves import extract_curves
from src.modes import single_mode_overrides
from src.runner import run_one


@pytest.mark.slow
def test_reference_equals_lli_zero(cfg, baseline):
    from src.baseline import get_discharged_state

    d = get_discharged_state(cfg)
    n_trim = cfg["postprocess"]["n_trim"]
    n_interp = cfg["postprocess"]["n_interp"]

    ref = run_one(cfg, None, "discharge_first")
    assert ref.ok, ref.error
    lli0 = run_one(cfg, single_mode_overrides("lli", 0.0, baseline, d),
                   "discharge_first")
    assert lli0.ok, lli0.error

    q_ref = extract_curves(ref.solution, n_trim, n_interp)["q_end_mah"]
    q_lli0 = extract_curves(lli0.solution, n_trim, n_interp)["q_end_mah"]
    assert abs(q_ref - q_lli0) < 0.01, (
        f"Reference {q_ref:.4f} mAh vs LLI=0 {q_lli0:.4f} mAh — 오염 발생")
