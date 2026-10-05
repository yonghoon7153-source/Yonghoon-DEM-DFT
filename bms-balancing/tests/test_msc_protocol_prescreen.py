"""msc_protocol_prescreen 의 모델 명제 고정 — `docs/MSC_PROTOCOL_DESIGNS_REVIEW_2026-10-05.md` §3 이 인용하는 방향 · 크기 비.

수치 그 자체가 아니라 검토 문장이 기대는 정성 결론을 잡는다 (PyBaMM SPMe · Chen2020 · 외부 병렬 옴 누설).
"""
import pytest

pybamm = pytest.importorskip("pybamm")

from scripts.msc_protocol_prescreen import e1, e4_dcir, e4_dcir_bias  # noqa: E402


def test_potentiostatic_pairs_half_first_step_removes_start_transient():
    """(+δ, −δ) 로 시작하면 첫 짝이 크게 음이다 — 누설 0 인 셀에서도. 첫 계단을 반 길이로 하면 거의 사라진다."""
    plus = e1("base", None, "from_below", n_pairs=3)
    half = e1("base", None, "from_below", n_pairs=3, half_first=True)
    assert plus["HI_Q_first_mAh"] < -0.5
    assert abs(half["HI_Q_first_mAh"]) < 0.2 * abs(plus["HI_Q_first_mAh"])


def test_potentiostatic_pairs_see_the_leak_only_after_the_leak_history_relaxes():
    """누설 셀: 처음 짝들은 누설을 크게 과소평가하고 (휴지 중 누설이 만든 분극이 풀리는 동안), 2 h 뒤에야 제 크기."""
    msc = e1("MSC", 100.0, "from_below", n_pairs=60, half_first=True)
    truth = msc["truth_leak_per_pair_mAh"]
    assert msc["HI_Q_mean_1_5"] < 0.5 * truth
    assert msc["HI_Q_mean_last5"] == pytest.approx(truth, rel=0.02)


def test_potentiostatic_pairs_barely_see_anode_sei_on_the_graphite_plateau():
    """같은 크기의 리튬 손실이라도 음극 SEI 는 정전위 짝에 몇 % 만 보인다 (흑연 평탄부 SOC 0.5 — 전압 장부와 같은 이유)."""
    sei = e1("SEI", None, "from_below", n_pairs=20, half_first=True)
    assert sei["truth_sei_per_pair_mAh"] > 1.0
    assert sei["HI_Q_mean_16_20"] < 0.05 * sei["truth_sei_per_pair_mAh"]


def test_pulse_resistance_drop_under_a_strong_leak_is_mostly_operating_point():
    """≈C/4 누설(3 Ω)에서 펄스 저항이 10 % 넘게 내려가는데, 같은 바이어스 전류만 흘린 base 셀도 거의 같다 — 병렬 경로 몫은 작다."""
    base = e4_dcir(None)["R_app_mOhm"]
    msc = e4_dcir(3.0)["R_app_mOhm"]
    bias = e4_dcir_bias(1.23)["R_app_mOhm"]
    assert msc < 0.9 * base
    assert msc == pytest.approx(bias, rel=0.015)
