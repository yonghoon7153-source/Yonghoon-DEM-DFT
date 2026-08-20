"""Electrode composition parsing and the active fraction it yields."""

import pytest

from wrdkit import CellSpec, Composition, Role, parse_composition
from wrdkit.composition import Component, infer_role


class TestParsing:
    def test_bare_ratio_gets_positional_names(self):
        composition = parse_composition("80:17:3")
        assert composition.label() == "AM:SE:VGCF = 80:17:3"
        assert composition.active_wt_percent == 80

    def test_named_ratio(self):
        composition = parse_composition("AM:SE:VGCF = 80:17:3")
        assert [c.name for c in composition.components] == ["AM", "SE", "VGCF"]
        assert [c.wt_percent for c in composition.components] == [80, 17, 3]

    def test_real_material_names_without_an_equals_sign(self):
        composition = parse_composition("NCM811:LPSCl:VGCF:PTFE 78:17:3:2")
        assert composition.active_wt_percent == 78
        assert composition.label() == "NCM811:LPSCl:VGCF:PTFE = 78:17:3:2"

    def test_slash_separated_pairs(self):
        composition = parse_composition("AM 80 / SE 17 / VGCF 3")
        assert composition.active_wt_percent == 80

    def test_decimal_fractions(self):
        composition = parse_composition("AM:SE:VGCF:PTFE = 77.5:17:3:2.5")
        assert composition.active_wt_percent == pytest.approx(77.5)
        assert composition.total_wt_percent == pytest.approx(100.0)

    def test_unreadable_text_returns_empty_rather_than_guessing(self):
        assert parse_composition("어제 만든 그 전극").is_empty()
        assert parse_composition("").is_empty()

    @pytest.mark.parametrize(
        "text",
        ["AM:SE:VGCF = 80:17", "NCM811:LPSCl:VGCF:PTFE 78:17:3"],
    )
    def test_a_missing_ratio_yields_nothing_rather_than_a_shifted_blend(self, text):
        """The old fallback carved a component out of the leftover digits."""
        assert parse_composition(text).is_empty()

    @pytest.mark.parametrize("text", ["cell 01", "sample 3"])
    def test_a_sample_label_is_not_a_composition(self, text):
        assert parse_composition(text).is_empty()

    def test_a_bare_number_is_never_a_component_name(self):
        composition = parse_composition("80 17 / VGCF 3")
        assert [c.name for c in composition.components] == []

    def test_parts_can_be_rescaled_to_percent(self):
        composition = parse_composition("AM:SE:VGCF = 8:1.7:0.3").normalized()
        assert composition.active_wt_percent == pytest.approx(80.0)
        assert composition.total_wt_percent == pytest.approx(100.0)


class TestRoles:
    @pytest.mark.parametrize(
        "name,role",
        [
            ("NCM811", Role.ACTIVE), ("AM", Role.ACTIVE), ("Graphite", Role.ACTIVE),
            ("LPSCl", Role.ELECTROLYTE), ("Li6PS5Cl", Role.ELECTROLYTE),
            ("SE", Role.ELECTROLYTE), ("VGCF", Role.CONDUCTIVE),
            ("Super P", Role.CONDUCTIVE), ("PTFE", Role.BINDER),
            ("PVDF", Role.BINDER), ("SBR", Role.BINDER),
        ],
    )
    def test_common_materials_are_classified(self, name, role):
        assert infer_role(name) == role

    def test_an_unknown_name_never_becomes_active_material(self):
        """It would silently enter the mAh/g denominator."""
        assert infer_role("Zzz-9") == Role.OTHER
        composition = Composition([Component("Zzz-9", 100)])
        assert composition.active_wt_percent is None

    @pytest.mark.parametrize(
        "name",
        ["LPS glass-ceramic", "LLZO ceramic", "amorphous carbon", "Li foam",
         "sample", "ceramic separator"],
    )
    def test_a_short_acronym_does_not_match_inside_another_word(self, name):
        """"am" buried in "cer-am-ic" would put the electrolyte in mAh/g."""
        assert infer_role(name) != Role.ACTIVE

    def test_llzo_ceramic_is_still_recognised_as_the_electrolyte(self):
        assert infer_role("LLZO ceramic") == Role.ELECTROLYTE

    @pytest.mark.parametrize(
        "name,role",
        [
            ("NCM-811", Role.ACTIVE), ("AM 1", Role.ACTIVE),
            ("SiO2", Role.ACTIVE), ("artificial graphite", Role.ACTIVE),
            ("LPSCl (argyrodite)", Role.ELECTROLYTE),
            ("VGCF-H", Role.CONDUCTIVE), ("Super P Li", Role.CONDUCTIVE),
            ("carbon black", Role.CONDUCTIVE),
            ("PVDF-HFP", Role.BINDER), ("PTFE binder", Role.BINDER),
        ],
    )
    def test_real_world_spellings_still_classify(self, name, role):
        assert infer_role(name) == role

    def test_an_unrecognised_electrolyte_stays_out_of_the_denominator(self):
        composition = parse_composition("NCM811:LPS glass-ceramic:VGCF = 80:17:3")
        assert composition.active_wt_percent == 80
        assert composition.components[1].role == Role.OTHER
        cell = CellSpec(total_mass_mg=31.6, composition=composition).resolve()
        assert cell.active_mass_g == pytest.approx(0.02528)


class TestProblems:
    def test_percentages_that_do_not_add_up_are_reported(self):
        composition = parse_composition("AM:SE:VGCF = 80:17:5")
        assert any("102" in problem for problem in composition.problems())

    def test_a_blend_with_no_active_material_is_reported(self):
        composition = Composition([Component("SE", 100, Role.ELECTROLYTE)])
        assert any("active material" in p for p in composition.problems())

    def test_a_repeated_component_is_reported(self):
        composition = parse_composition("AM:AM = 50:50")
        assert any("repeated" in p for p in composition.problems())

    def test_a_valid_blend_has_no_problems(self):
        assert parse_composition("AM:SE:VGCF = 80:17:3").problems() == []


class TestCellSpecIntegration:
    def test_composition_supplies_the_active_fraction(self):
        cell = CellSpec(
            total_mass_mg=31.6,
            composition=parse_composition("AM:SE:VGCF = 80:17:3"),
        ).resolve()
        assert cell.active_mass_g == pytest.approx(0.02528)
        assert cell.active_wt_percent == 80
        assert "AM:SE:VGCF = 80:17:3" in cell.notes["active_mass"]

    def test_an_explicit_weight_percent_wins_over_the_composition(self):
        cell = CellSpec(
            total_mass_mg=31.6,
            active_wt_percent=70,
            composition=parse_composition("AM:SE:VGCF = 80:17:3"),
        ).resolve()
        assert cell.active_mass_g == pytest.approx(0.02212)
        assert cell.active_wt_percent == 70

    def test_no_composition_and_no_percent_assumes_the_whole_film_and_says_so(self):
        cell = CellSpec(total_mass_mg=31.6).resolve()
        assert cell.active_mass_g == pytest.approx(0.0316)
        assert "assuming the whole electrode" in cell.notes["active_mass"]

    def test_composition_problems_surface_on_the_resolved_cell(self):
        cell = CellSpec(
            total_mass_mg=31.6,
            composition=parse_composition("AM:SE:VGCF = 80:17:9"),
        ).resolve()
        assert cell.composition_problems
        assert "composition" in cell.notes

    def test_the_label_is_carried_through_for_display(self):
        cell = CellSpec(composition=parse_composition("AM:SE = 70:30")).resolve()
        assert cell.composition_label == "AM:SE = 70:30"


class TestSerialisation:
    def test_round_trips_through_json(self):
        original = parse_composition("NCM811:LPSCl:VGCF:PTFE = 78:17:3:2")
        restored = Composition.from_json(original.to_json())
        assert restored.label() == original.label()
        assert restored.active_wt_percent == original.active_wt_percent

    def test_malformed_json_entries_are_skipped_not_fatal(self):
        restored = Composition.from_json(
            [{"name": "AM", "wt_percent": 80}, {"wt_percent": 20}, "junk",
             {"name": "SE", "wt_percent": "x"}]
        )
        assert [c.name for c in restored.components] == ["AM"]


class TestZeroWeightComponents:
    """A binder-free or additive-free electrode is a normal thing to record."""

    def test_a_zero_component_parses_and_does_not_break_the_active_fraction(self):
        composition = parse_composition("AM:SE:VGCF:PTFE = 80:17:3:0")
        assert composition.active_wt_percent == 80
        assert composition.total_wt_percent == pytest.approx(100.0)

    def test_a_zero_component_is_not_a_problem(self):
        assert parse_composition("AM:SE:VGCF:PTFE = 80:17:3:0").problems() == []

    def test_zero_components_are_kept_as_deliberate_metadata(self):
        composition = parse_composition("AM:SE:VGCF:PTFE = 80:17:3:0")
        assert [c.name for c in composition.absent] == ["PTFE"]
        assert [c.name for c in composition.present] == ["AM", "SE", "VGCF"]
        # ...and survive a round trip, so "this batch had no PTFE" is recorded.
        assert len(Composition.from_json(composition.to_json()).components) == 4

    def test_the_compact_label_can_drop_the_zeros(self):
        composition = parse_composition("AM:SE:VGCF:PTFE = 80:17:3:0")
        assert composition.label() == "AM:SE:VGCF:PTFE = 80:17:3:0"
        assert composition.label(skip_zero=True) == "AM:SE:VGCF = 80:17:3"

    def test_rescaling_leaves_zeros_at_zero(self):
        composition = parse_composition("AM:SE:VGCF:PTFE = 8:1.7:0.3:0").normalized()
        assert composition.active_wt_percent == pytest.approx(80.0)
        assert composition.components[-1].wt_percent == 0

    def test_the_mass_is_unaffected_by_a_zero_component(self):
        with_binder = CellSpec(
            total_mass_mg=31.6,
            composition=parse_composition("AM:SE:VGCF:PTFE = 80:17:3:0"),
        ).resolve()
        without = CellSpec(
            total_mass_mg=31.6,
            composition=parse_composition("AM:SE:VGCF = 80:17:3"),
        ).resolve()
        assert with_binder.active_mass_g == without.active_mass_g

    def test_an_all_zero_composition_is_reported_rather_than_dividing_by_zero(self):
        composition = parse_composition("AM:SE = 0:0")
        assert composition.active_wt_percent == 0
        assert any("0 wt%" in p for p in composition.problems())
        cell = CellSpec(total_mass_mg=31.6, composition=composition).resolve()
        assert cell.active_mass_g == 0 or cell.active_mass_g is None
        assert cell.divisor("mAh/g") is None   # unusable, and says so


# --- 토큰 경계 규칙 ---------------------------------------------------------
#
# `am` 부분 문자열 오탐을 막으려고 접미사를 숫자로만 제한했더니, SiOx 계열이
# 통째로 other 로 떨어졌다. 조용한 실패다 — 음극이 활물질 질량에서 빠지고
# mAh/g 만 높게 나온다. 양방향을 함께 고정한다.

def test_stoichiometric_tails_stay_the_same_substance():
    """SiOx 와 SiO2 와 SiO 는 같은 물질이다."""
    for name in ("SiO", "SiO2", "SiOx", "SiOx-C", "NCM", "NCM811", "NCM622"):
        assert infer_role(name) == Role.ACTIVE, name


def test_a_real_word_starting_with_a_hint_is_not_that_hint():
    """`am` 은 amorphous 안에서 발화하면 안 된다 — 분모로 조용히 들어간다."""
    for name in ("amorphous", "foam", "LPS glass-ceramic", "ceramic", "grease"):
        assert infer_role(name) != Role.ACTIVE, name


def test_common_anodes_are_recognised():
    """미인식 음극은 활물질 질량에서 빠져 mAh/g 를 부풀린다."""
    for name in ("Si", "Si-C", "Gr", "Graphite", "LTO", "Hard carbon"):
        assert infer_role(name) == Role.ACTIVE, name


def test_graphene_is_a_conductive_additive_not_the_anode():
    """`Gr` 은 흑연이지만 graphene 은 도전재다."""
    assert infer_role("graphene") == Role.CONDUCTIVE
    assert infer_role("SiC") == Role.OTHER


def test_siox_blend_puts_only_the_anode_in_the_denominator():
    """회귀의 실제 피해: 분모가 전극 전체가 되는지."""
    blend = parse_composition("SiOx:Super P:CMC = 90:5:5")
    assert blend.active_wt_percent == 90.0
