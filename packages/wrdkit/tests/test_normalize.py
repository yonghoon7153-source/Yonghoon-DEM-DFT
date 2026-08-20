"""Mass/area resolution and capacity bases."""

import pytest

from wrdkit import Basis, CellSpec, c_rate, normalize_capacity, parse_composition
from wrdkit.normalize import retention


def test_active_mass_from_total_mass_and_composition():
    cell = CellSpec(total_mass_mg=31.6, active_wt_percent=80).resolve()
    assert cell.active_mass_g == pytest.approx(0.02528)
    assert "80 wt%" in cell.notes["active_mass"]


def test_explicit_active_mass_wins():
    cell = CellSpec(active_mass_mg=25.0, total_mass_mg=31.6,
                    active_wt_percent=80).resolve()
    assert cell.active_mass_g == pytest.approx(0.025)
    assert cell.notes["active_mass"] == "entered directly"


def test_current_collector_mass_is_subtracted():
    cell = CellSpec(total_mass_mg=40.0, current_collector_mass_mg=8.4,
                    active_wt_percent=80).resolve()
    assert cell.active_mass_g == pytest.approx(0.02528)


def test_collector_heavier_than_electrode_yields_no_mass():
    cell = CellSpec(total_mass_mg=5.0, current_collector_mass_mg=8.0).resolve()
    assert cell.active_mass_g is None
    assert "exceeds" in cell.notes["active_mass"]


def test_area_from_punch_diameter():
    cell = CellSpec(diameter_mm=13).resolve()
    assert cell.area_cm2 == pytest.approx(1.32732, rel=1e-4)


def test_loading_combines_mass_and_area():
    cell = CellSpec(total_mass_mg=31.6, active_wt_percent=80, diameter_mm=13).resolve()
    assert cell.loading_mg_cm2 == pytest.approx(19.045, rel=1e-3)


def test_specific_and_areal_capacity():
    cell = CellSpec(total_mass_mg=31.6, active_wt_percent=80, diameter_mm=13).resolve()
    assert normalize_capacity(5.25, cell, Basis.SPECIFIC) == pytest.approx(207.67, rel=1e-3)
    assert normalize_capacity(5.25, cell, Basis.AREAL) == pytest.approx(3.9553, rel=1e-3)


def test_utilisation_against_nominal_capacity():
    cell = CellSpec(total_mass_mg=31.6, active_wt_percent=80,
                    nominal_specific_capacity_mah_g=205.9).resolve()
    assert cell.nominal_capacity_mah == pytest.approx(5.205152)
    # A measurement that exactly meets the nominal capacity is 100 % utilised.
    assert normalize_capacity(cell.nominal_capacity_mah, cell,
                              Basis.NORMALIZED) == pytest.approx(100.0)
    assert normalize_capacity(cell.nominal_capacity_mah / 2, cell,
                              Basis.NORMALIZED) == pytest.approx(50.0)


def test_missing_inputs_are_reported_not_guessed():
    cell = CellSpec(diameter_mm=13).resolve()
    assert cell.divisor(Basis.SPECIFIC) is None
    assert cell.missing_for(Basis.SPECIFIC) == "active mass not set"
    assert Basis.SPECIFIC not in cell.available_bases()
    with pytest.raises(ValueError, match="active mass not set"):
        normalize_capacity(5.0, cell, Basis.SPECIFIC)


def test_volumetric_needs_thickness():
    without = CellSpec(diameter_mm=13).resolve()
    assert without.volume_cm3 is None
    with_thickness = CellSpec(diameter_mm=13, thickness_um=120).resolve()
    assert with_thickness.volume_cm3 == pytest.approx(1.32732 * 0.012, rel=1e-4)


def test_c_rate_uses_the_nominal_capacity():
    cell = CellSpec(total_mass_mg=31.6, active_wt_percent=80,
                    nominal_specific_capacity_mah_g=205.9).resolve()
    assert c_rate(1.0410e-3, cell) == pytest.approx(0.2, rel=1e-3)


def test_c_rate_falls_back_to_a_measured_capacity():
    cell = CellSpec().resolve()
    assert c_rate(1.0e-3, cell, measured_capacity_mah=5.0) == pytest.approx(0.2)
    assert c_rate(1.0e-3, cell) is None


def test_retention_against_a_chosen_reference():
    values = [5.0, 4.9, 4.8, 4.0]
    assert retention(values, 1) == pytest.approx(
        [102.04, 100.0, 97.96, 81.63], rel=1e-3)


def test_retention_of_an_empty_or_zero_series():
    assert retention([]) == []
    assert retention([0.0, 1.0]) == [None, None]


def test_retention_never_falls_back_to_the_formation_cycle():
    """ADR 0004: no cycle 3 in the series means no retention, not cycle 1."""
    assert retention([5.0, 4.0], 2) == [None, None]
    assert retention([5.0, 4.0], -1) == [None, None]


def test_a_negative_weight_percent_is_ignored_with_a_reason():
    cell = CellSpec(total_mass_mg=31.6, active_wt_percent=-80).resolve()
    assert cell.active_mass_g is None
    assert cell.divisor(Basis.SPECIFIC) is None
    assert "-80" in cell.notes["active_mass"]


def test_a_weight_percent_above_100_is_ignored_with_a_reason():
    cell = CellSpec(total_mass_mg=31.6, active_wt_percent=800).resolve()
    assert cell.active_mass_g is None
    assert Basis.SPECIFIC not in cell.available_bases()
    assert "800" in cell.notes["active_mass"]


def test_a_negative_entered_active_mass_does_not_slip_into_the_total_mass_path():
    cell = CellSpec(active_mass_mg=-25.0, total_mass_mg=31.6,
                    active_wt_percent=80).resolve()
    assert cell.active_mass_g is None
    assert "not positive" in cell.notes["active_mass"]


def test_a_negative_mass_is_never_a_divisor():
    """It would produce a negative mAh/g that reads like a measurement."""
    from wrdkit.normalize import ResolvedCell

    cell = ResolvedCell(active_mass_g=-0.02528, area_cm2=-1.3,
                        volume_cm3=-0.016, nominal_capacity_mah=-5.2)
    for basis in (Basis.SPECIFIC, Basis.AREAL, Basis.VOLUMETRIC, Basis.NORMALIZED):
        assert cell.divisor(basis) is None
        assert cell.missing_for(basis) is not None
    assert cell.available_bases() == [Basis.ABSOLUTE]


def test_the_reason_names_what_is_actually_missing():
    with_area = CellSpec(diameter_mm=13).resolve()
    assert with_area.missing_for(Basis.VOLUMETRIC) == "electrode thickness not set"
    assert CellSpec().resolve().missing_for(Basis.VOLUMETRIC) == \
        "electrode area and thickness not set"

    with_mass = CellSpec(total_mass_mg=31.6, active_wt_percent=80).resolve()
    assert with_mass.missing_for(Basis.NORMALIZED) == "nominal specific capacity not set"
    with_nominal = CellSpec(nominal_specific_capacity_mah_g=205.9).resolve()
    assert with_nominal.missing_for(Basis.NORMALIZED) == "active mass not set"
    assert CellSpec().resolve().missing_for(Basis.NORMALIZED) == \
        "active mass and nominal specific capacity not set"


def test_a_zero_percent_blend_says_so_instead_of_blaming_the_mass():
    from wrdkit import parse_composition

    cell = CellSpec(total_mass_mg=31.6,
                    composition=parse_composition("AM:SE = 0:100")).resolve()
    assert cell.missing_for(Basis.SPECIFIC) == \
        "active material is 0 wt% of the composition"


# --- 조성은 있는데 활물질이 없을 때 -------------------------------------------
#
# 아무것도 안 쓴 것과 "이게 전부 뭔지 적었는데 활물질로 알아본 게 없다" 는 다르다.
# 후자를 전자처럼 다루면 바인더·전해질·도전재가 전부 mAh/g 분모로 들어가고,
# 그 결과가 실측인 양 보고된다.

def test_a_composition_with_no_active_component_refuses_to_guess():
    spec = CellSpec(total_mass_mg=31.6,
                    composition=parse_composition("Zzz-9:Qqq:Www = 80:15:5"))
    resolved = spec.resolve()
    assert resolved.active_mass_g is None
    assert resolved.missing_for("mAh/g") is not None
    assert "no active material" in resolved.notes["active_mass"]
    assert "Zzz-9" in resolved.notes["active_mass"], "무엇을 못 알아봤는지 말해야 한다"


def test_no_composition_at_all_still_assumes_the_whole_electrode():
    """가정이지만 문장으로 밝힌다 — 기존 동작을 바꾸지 않는다."""
    resolved = CellSpec(total_mass_mg=31.6).resolve()
    assert resolved.active_mass_g == 0.0316
    assert "no composition given" in resolved.notes["active_mass"]


def test_an_explicit_active_wt_percent_wins_over_an_unrecognised_blend():
    """이름을 못 알아봐도 사람이 숫자를 넣었으면 그게 답이다."""
    resolved = CellSpec(total_mass_mg=31.6, active_wt_percent=90,
                        composition=parse_composition("Zzz-9:Qqq = 90:10")).resolve()
    assert resolved.active_mass_g == 0.02844


def test_a_recognised_blend_uses_only_the_active_fraction():
    resolved = CellSpec(
        total_mass_mg=31.6,
        composition=parse_composition("SiOx:Super P:CMC = 90:5:5")).resolve()
    assert resolved.active_mass_g == 0.02844
