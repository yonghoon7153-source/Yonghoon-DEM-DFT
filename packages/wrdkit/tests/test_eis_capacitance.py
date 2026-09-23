"""Reading an arc as a capacitor, and asking what it can be (ADR 0040).

The anchor is a real cell: `2600922_No1_55_sym_60um_#1_C01`, 60 µm thick,
10 mm across, whose two arcs were called bulk and grain boundary.
"""

import math

import numpy as np
import pytest

from wrdkit.eis.capacitance import (
    BOUNDARY,
    BULK,
    DETERMINED_SPREAD,
    FACE,
    LOWEST_N,
    PROCESSES,
    UNDETERMINED_SPREAD,
    arc_capacitances,
    candidate_processes,
    effective_capacitance,
    peak_frequency,
    size_class,
    spread_for,
)
from wrdkit.eis.circuit import parse_circuit

EPS0_F_PER_CM = 8.8541878128e-14

#: 그 셀의 맞춤값 (2026-09-23) 과 모양.
USER_R1, USER_Q1, USER_N1 = 10.42, 3.06e-5, 0.658
USER_R2, USER_Q2, USER_N2 = 6.635, 1.36e-3, 0.757
USER_THICKNESS_CM = 60e-4
USER_AREA_CM2 = math.pi * 1.0 ** 2 / 4


def keys(found):
    return None if found is None else [one.key for one in found]


def test_an_ideal_capacitor_is_its_own_capacitance():
    assert effective_capacitance(100.0, 3.3e-9, 1.0) == pytest.approx(3.3e-9)


def test_the_apex_of_the_arc_is_where_the_formula_puts_it():
    """Checked against the impedance itself, not against the formula again:
    the frequency of the largest -Im(Z) is the apex, and ``R·C_eff`` must be
    its time constant."""
    r, q, n = 50.0, 2e-6, 0.8
    frequency = np.logspace(-2, 8, 20001)
    z = r / (1 + r * q * (2j * np.pi * frequency) ** n)
    apex = frequency[np.argmax(-z.imag)]
    assert peak_frequency(r, q, n) == pytest.approx(apex, rel=2e-3)
    capacitance = effective_capacitance(r, q, n)
    assert 1 / (2 * np.pi * r * capacitance) == pytest.approx(apex, rel=2e-3)


def test_the_users_cell_capacitances():
    assert effective_capacitance(USER_R1, USER_Q1, USER_N1) == pytest.approx(
        4.66e-7, rel=0.01)
    assert effective_capacitance(USER_R2, USER_Q2, USER_N2) == pytest.approx(
        3.00e-4, rel=0.01)


def test_the_users_first_arc_cannot_be_bulk():
    """``C·l/A = 3.6e-9`` is a boundary, ``C/A = 5.9e-7`` an interface -- the
    measurement cannot choose between them.  What it can say is *not bulk*:
    that needs ``C·l/A`` below 1e-11, and this is three hundred times over."""
    capacitance = effective_capacitance(USER_R1, USER_Q1, USER_N1)
    found = keys(candidate_processes(capacitance, thickness_cm=USER_THICKNESS_CM,
                                     area_cm2=USER_AREA_CM2))
    assert found == ["grain_boundary", "interface"]
    assert "bulk" not in found


def test_the_users_second_arc_is_on_an_electrode_not_a_boundary():
    capacitance = effective_capacitance(USER_R2, USER_Q2, USER_N2)
    found = keys(candidate_processes(capacitance, thickness_cm=USER_THICKNESS_CM,
                                     area_cm2=USER_AREA_CM2))
    assert found == ["reaction"]


def test_a_real_bulk_capacitance_reads_as_bulk():
    """A dielectric of εr = 20 across the pellet: ``ε₀ εr A / l``."""
    bulk = EPS0_F_PER_CM * 20 * USER_AREA_CM2 / USER_THICKNESS_CM
    assert keys(candidate_processes(bulk, thickness_cm=USER_THICKNESS_CM,
                                    area_cm2=USER_AREA_CM2)) == ["bulk"]


def test_a_double_layer_is_scaled_by_area_not_by_thickness():
    """1 µF/cm² on a 60 µm pellet.  Scaled by ``l/A`` like a bulk it is
    ``6e-9`` -- a grain boundary and nothing else, and the interface it really
    is would fall off the list.  Scaled by area it stays on it."""
    double_layer = 1e-6 * USER_AREA_CM2
    found = keys(candidate_processes(double_layer, thickness_cm=USER_THICKNESS_CM,
                                     area_cm2=USER_AREA_CM2))
    assert "interface" in found


def test_no_geometry_no_verdict():
    capacitance = effective_capacitance(USER_R1, USER_Q1, USER_N1)
    assert candidate_processes(capacitance, thickness_cm=None,
                               area_cm2=USER_AREA_CM2) is None
    assert candidate_processes(capacitance, thickness_cm=USER_THICKNESS_CM,
                               area_cm2=None) is None


@pytest.mark.parametrize("args", [(0.0, 1e-6, 0.9), (10.0, -1e-6, 0.9),
                                  (10.0, 1e-6, 1.2), (10.0, 1e-6, 0.0),
                                  (float("nan"), 1e-6, 0.9)])
def test_numbers_that_are_not_an_arc_give_nothing(args):
    assert effective_capacitance(*args) is None
    assert peak_frequency(*args) is None


def test_the_table_has_no_gap_for_a_pellet_up_to_a_centimetre():
    """Every capacitance falls somewhere as long as ``l ≤ 1 cm``: when
    ``C·l/A`` leaves the boundary range, ``C/A = (C·l/A)/l`` is already past
    the start of the surface-layer range."""
    for thickness_cm in (10e-4, 60e-4, 0.1, 1.0):
        for capacitance in np.logspace(-14, -1, 131):
            assert candidate_processes(capacitance, thickness_cm=thickness_cm,
                                       area_cm2=1.0), (thickness_cm, capacitance)


def test_the_arcs_of_a_fitted_circuit_in_circuit_order():
    values = {"R0": 4.897, "R1": USER_R1, "CPE1_Q": USER_Q1, "CPE1_n": USER_N1,
              "R2": USER_R2, "CPE2_Q": USER_Q2, "CPE2_n": USER_N2,
              "CPE3_Q": 1000.0, "CPE3_n": 1.0}
    arcs = arc_capacitances("R0-p(R1,CPE1)-p(R2,CPE2)-CPE3", values,
                            thickness_cm=USER_THICKNESS_CM, area_cm2=USER_AREA_CM2)
    # CPE3 는 직렬이다 — 아크가 아니다.
    assert [(a.resistor, a.element) for a in arcs] == [("R1", "CPE1"), ("R2", "CPE2")]
    first, second = arcs
    assert first.candidates == ("grain_boundary", "interface")
    assert second.candidates == ("reaction",)
    assert first.per_length == pytest.approx(3.56e-9, rel=0.02)
    assert first.per_area == pytest.approx(5.93e-7, rel=0.02)
    # 둘 다 잰 구간(7 MHz – 10 mHz) 안에 꼭지가 있다.
    assert first.peak_hz == pytest.approx(3.27e4, rel=0.02)
    assert second.peak_hz == pytest.approx(80.0, rel=0.02)


def test_a_capacitor_arc_and_a_backwards_pair_are_both_read():
    values = {"R1": 100.0, "C1": 2e-11, "R2": 50.0, "CPE2_Q": 1e-5, "CPE2_n": 0.9}
    arcs = arc_capacitances("p(C1,R1)-p(CPE2,R2)", values)
    assert [(a.resistor, a.element, a.element_kind) for a in arcs] == [
        ("R1", "C1", "C"), ("R2", "CPE2", "CPE")]
    assert arcs[0].capacitance_f == pytest.approx(2e-11)
    assert arcs[0].n == 1.0
    # 두께·면적이 없으면 판정 없이 값만.
    assert arcs[0].candidates is None
    assert "두께" in arcs[0].reason


def test_a_diffusion_like_cpe_is_not_read_as_a_capacitor():
    values = {"R1": 100.0, "CPE1_Q": 1e-3, "CPE1_n": LOWEST_N - 0.05}
    (arc,) = arc_capacitances("p(R1,CPE1)", values, thickness_cm=0.06,
                              area_cm2=0.785)
    assert arc.candidates is None
    assert "확산" in arc.reason
    assert arc.capacitance_f is not None          # 값은 낸다, 판정만 안 한다


def test_missing_values_are_skipped_not_invented():
    arcs = arc_capacitances("R0-p(R1,CPE1)", {"R0": 1.0, "R1": 10.0})
    assert arcs == []


def test_three_member_parallel_blocks_are_not_read_as_one_arc():
    circuit = parse_circuit("p(R1,CPE1,C1)")
    assert circuit.capacitive_arcs() == []


def test_series_kinds_name_the_blocking_end():
    circuit = parse_circuit("L1-R0-p(R1,CPE1)-Wo2")
    assert circuit.series_element_kinds() == [("L1", "L"), ("R0", "R"),
                                              ("Wo2", "Wo")]


def test_the_table_is_ordered_high_frequency_first():
    """Candidates come back in table order, and the table goes from the fast
    process to the slow one -- the order arcs appear in a sweep."""
    assert [one.key for one in PROCESSES] == [
        "bulk", "grain_boundary", "surface_layer", "interface", "reaction"]


# -- 어느 쪽인가: 벌크 / 입계 / 면 (ADR 0041) -----------------------------------------

PELLET_CM, PELLET_AREA = 0.07, math.pi / 4          # 700 µm, 10 mm — l/A 0.0891


def one_arc(capacitance_f, thickness_cm=PELLET_CM, area_cm2=PELLET_AREA):
    (arc,) = arc_capacitances("p(R1,C1)", {"R1": 10.0, "C1": capacitance_f},
                              thickness_cm=thickness_cm, area_cm2=area_cm2)
    return arc


@pytest.mark.parametrize(("capacitance_f", "side"), [
    (1e-11, BULK),              # C·l/A 8.9e-13
    (5e-9, BOUNDARY),           # C·l/A 4.5e-10 (C/A 6.4e-9 은 표면층이기도)
    (2e-6, FACE),               # C/A 2.5e-6 — 이중층
    (5e-4, FACE),               # C/A 6.4e-4 — 반응
])
def test_the_side_of_a_clear_capacitance(capacitance_f, side):
    assert size_class(one_arc(capacitance_f), spread=DETERMINED_SPREAD) == side


def test_a_capacitance_near_a_boundary_of_the_table_is_not_judged():
    """C·l/A 2e-11 은 벌크 상한의 두 배 — 식이 분포 가정에 따라 0.3–2 배
    흔들리므로 (Hirschorn 2010) 벌크가 아니라고 못 한다."""
    near = one_arc(2.24e-10)
    assert size_class(near) == BOUNDARY                      # 흔들림 없이는
    assert size_class(near, spread=DETERMINED_SPREAD) is None


def test_a_thin_pellets_double_layer_is_a_boundary_too_and_kept():
    """60 µm 펠릿의 1 µF/cm² 는 입계이자 전극 계면 — 모르는 아크를 전해질에서
    빼지 않는다."""
    arc = one_arc(0.785e-6, thickness_cm=60e-4)
    assert set(arc.candidates) >= {"grain_boundary", "interface"}
    assert size_class(arc) == BOUNDARY


def test_only_an_undetermined_r_or_q_widens_the_spread():
    arc = one_arc(5e-9)
    assert spread_for(arc, set()) == DETERMINED_SPREAD
    assert spread_for(arc, {"C1"}) == UNDETERMINED_SPREAD
    assert spread_for(arc, {"R1"}) == UNDETERMINED_SPREAD
    (cpe,) = arc_capacitances("p(R1,CPE1)", {"R1": 10.0, "CPE1_Q": 5e-9,
                                             "CPE1_n": 1.0})
    assert spread_for(cpe, {"CPE1_n"}) == DETERMINED_SPREAD  # 이상적 축전기
    assert spread_for(cpe, {"CPE1_Q"}) == UNDETERMINED_SPREAD


def test_no_geometry_no_side():
    arc = one_arc(2e-6, thickness_cm=None, area_cm2=None)
    assert size_class(arc) is None
