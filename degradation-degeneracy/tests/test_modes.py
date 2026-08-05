"""modes 검증 — ★ Phase 2에서 가장 중요한 테스트.

원본 update_fn(reference/degrade_mode_sim_original.py L134~L216)을 문자 그대로
재현한 람다와 single_mode_overrides()의 출력을 대조한다.
완방상태 fixture는 원본 하드코딩 값(36.7/3446.3/58439.9)을 쓰므로,
수식 구조가 같으면 dict가 정확히 일치해야 한다.
"""

from __future__ import annotations

import pytest

from src.modes import (P_NE1_INIT, P_NE1_VF, P_NE2_INIT, P_NE2_VF, P_NE_POR,
                       P_PE_INIT, P_PE_POR, P_PE_VF, InfeasibleConditionError,
                       build_overrides, single_mode_overrides)

VALUES = [0, 0.1, 0.2, 0.3]

# 원본 update_fn 문자 그대로 (하드코딩 포함 — 테스트 기준값으로만 사용)
ORIGINAL_UPDATE_FNS = {
    "lli": lambda i: {
        P_NE1_INIT: 27700 * (1 - i),
        P_NE2_INIT: 276610 * (1 - i),
    },
    "lam_pe_de": lambda i: {
        P_PE_POR: 0.335 + 0.665 * i,
        P_PE_VF: 0.665 * (1 - i),
        P_PE_INIT: 17038.0 / (1 - i),
    },
    "lam_ne_de": lambda i: {
        P_NE_POR: 0.25 + (0.735 + 0.015) * i,
        P_NE1_VF: 0.735 * (1 - i),
        P_NE2_VF: 0.015 * (1 - i),
        P_NE1_INIT: 36.7 / (1 - i),
        P_NE2_INIT: 3446.3 / (1 - i),
        P_PE_INIT: 58439.9,
    },
    "lam_pe_li": lambda i: {
        P_PE_POR: 0.335 + 0.665 * i,
        P_PE_VF: 0.665 * (1 - i),
        P_NE1_INIT: 36.7,
        P_NE2_INIT: 3446.3,
        P_PE_INIT: 58439.9,
    },
    "lam_ne_li": lambda i: {
        P_NE_POR: 0.25 + (0.735 + 0.015) * i,
        P_NE1_VF: 0.735 * (1 - i),
        P_NE2_VF: 0.015 * (1 - i),
    },
}


@pytest.mark.parametrize("mode", list(ORIGINAL_UPDATE_FNS))
@pytest.mark.parametrize("value", VALUES)
def test_single_mode_matches_original(mode, value, baseline, d_orig):
    ours = single_mode_overrides(mode, value, baseline, d_orig)
    orig = ORIGINAL_UPDATE_FNS[mode](value)
    assert set(ours) == set(orig), f"{mode}: 키 불일치"
    for k in orig:
        assert ours[k] == pytest.approx(orig[k], rel=1e-12), f"{mode}[{k}]"


def test_reference_is_empty(baseline, d_orig):
    assert single_mode_overrides("reference", 0.0, baseline, d_orig) == {}


def test_unknown_mode_raises(baseline, d_orig):
    with pytest.raises(KeyError):
        single_mode_overrides("lam_xx", 0.1, baseline, d_orig)


# ---------------------------------------------------------------- 조합(build_overrides)

def test_zero_condition_stays_in_discharged_frame(baseline, d_orig):
    """★ 리뷰 F15: 영 조건도 완방 프레임에 있어야 한다 (빈 dict 아님).

    예전 구현은 lli=lam_pe=lam_ne=0 에서 {}를 반환했고, 그러면 그 조건만
    완충 baseline에서 시작해 나머지(완방→CC충전)와 프레임이 어긋났다.
    실측 결과 reference가 1.74% 더 충전된 상태가 되어, 참값 0인 조건의
    LAM_PE·LLI가 ~1.6%p로 추정되는 계통 편향이 생겼다.
    """
    ov = build_overrides(0, 0, 0, "de", "de", baseline, d_orig)
    assert ov != {}, "영 조건이 완충 baseline으로 새면 프레임 불일치가 재발한다"
    # 농도는 완방 상태 그대로, 구조 파라미터는 건드리지 않음
    assert ov[P_NE1_INIT] == pytest.approx(d_orig.ne_primary, rel=1e-12)
    assert ov[P_NE2_INIT] == pytest.approx(d_orig.ne_secondary, rel=1e-12)
    assert ov[P_PE_INIT] == pytest.approx(d_orig.pe, rel=1e-12)
    for k in (P_PE_VF, P_PE_POR, P_NE1_VF, P_NE2_VF, P_NE_POR):
        assert k not in ov


def test_zero_condition_matches_tiny_degradation_limit(baseline, d_orig):
    """연속성: 영 조건과 극소 열화 조건의 override가 매끄럽게 이어져야 한다."""
    ov0 = build_overrides(0, 0, 0, "de", "de", baseline, d_orig)
    ov1 = build_overrides(1e-6, 0, 0, "de", "de", baseline, d_orig)
    for k in (P_NE1_INIT, P_NE2_INIT, P_PE_INIT):
        assert ov1[k] == pytest.approx(ov0[k], rel=1e-5)


def test_single_lam_ne_de_equals_original(baseline, d_orig):
    """조합 함수도 lam_ne_de 단독이면 원본 update_fn과 일치해야 한다.

    (lam_ne_de는 원본도 charge_first(완방 프레임)라 프레임 변환 없이 대조 가능)
    """
    for i in [0.1, 0.2, 0.3]:
        ours = build_overrides(0, 0, i, "de", "de", baseline, d_orig)
        orig = ORIGINAL_UPDATE_FNS["lam_ne_de"](i)
        assert set(ours) == set(orig)
        for k in orig:
            assert ours[k] == pytest.approx(orig[k], rel=1e-12), k


def test_single_lam_pe_li_equals_original(baseline, d_orig):
    """lam_pe_li 단독 (원본도 charge_first) — 원본 update_fn과 일치."""
    for i in [0.1, 0.2, 0.3]:
        ours = build_overrides(0, i, 0, "li", "de", baseline, d_orig)
        orig = ORIGINAL_UPDATE_FNS["lam_pe_li"](i)
        assert set(ours) == set(orig)
        for k in orig:
            assert ours[k] == pytest.approx(orig[k], rel=1e-12), k


def test_composition_order(baseline, d_orig):
    """LAM_NE + LLI 동시 적용: 적용 순서(LAM→LLI) 결과 농도 검증.

    lam_ne=0.1(de), lli=0.1 → NE 농도 = D/(1-0.1)×(1-0.1) = D (정확히 상쇄),
    PE 농도 = D.pe×(1-0.1).
    """
    ov = build_overrides(0.1, 0, 0.1, "de", "de", baseline, d_orig)
    assert ov[P_NE1_INIT] == pytest.approx(d_orig.ne_primary, rel=1e-12)
    assert ov[P_NE2_INIT] == pytest.approx(d_orig.ne_secondary, rel=1e-12)
    assert ov[P_PE_INIT] == pytest.approx(d_orig.pe * 0.9, rel=1e-12)
    # 구조 파라미터는 LAM_NE만 반영
    assert ov[P_NE1_VF] == pytest.approx(0.735 * 0.9, rel=1e-12)
    assert ov[P_NE_POR] == pytest.approx(0.25 + 0.75 * 0.1, rel=1e-12)


def test_lli_scales_total_inventory(baseline, d_orig):
    """LLI 단독: 모든 저장소 농도가 (1-lli)배 → 전체 재고가 정확히 lli만큼 감소."""
    ov = build_overrides(0.2, 0, 0, "de", "de", baseline, d_orig)
    assert ov[P_NE1_INIT] == pytest.approx(d_orig.ne_primary * 0.8, rel=1e-12)
    assert ov[P_NE2_INIT] == pytest.approx(d_orig.ne_secondary * 0.8, rel=1e-12)
    assert ov[P_PE_INIT] == pytest.approx(d_orig.pe * 0.8, rel=1e-12)
    # 구조 파라미터(vf/porosity)는 건드리지 않음
    for k in (P_PE_VF, P_PE_POR, P_NE1_VF, P_NE2_VF, P_NE_POR):
        assert k not in ov


def test_infeasible_pe_de_flagged(baseline, d_orig):
    """PE-limited 영역: lam_pe_de가 크고 lli가 작으면 PE 농도 > c_max → 불능 판정."""
    with pytest.raises(InfeasibleConditionError, match="PE"):
        build_overrides(0.0, 0.2, 0.0, "de", "de", baseline, d_orig)


def test_feasible_when_lli_compensates(baseline, d_orig):
    """같은 lam_pe_de=0.2라도 lli=0.2면 (1-lli)/(1-lam_pe)=1 → 성립."""
    ov = build_overrides(0.2, 0.2, 0.0, "de", "de", baseline, d_orig)
    assert ov[P_PE_INIT] == pytest.approx(d_orig.pe, rel=1e-12)


def test_out_of_range_raises(baseline, d_orig):
    with pytest.raises(InfeasibleConditionError):
        build_overrides(0.95, 0, 0, "de", "de", baseline, d_orig)
    with pytest.raises(InfeasibleConditionError):
        build_overrides(0, 0, 0.1, "de", "xx", baseline, d_orig)
