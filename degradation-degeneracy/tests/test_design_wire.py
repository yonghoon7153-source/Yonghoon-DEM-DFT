"""pairing design wire schema · ID 도메인 회귀 (계약 v4 묶음 2).

25차 Q3 이 묶음 2 를 앞당기라고 했다. 묶음 9 가 `planned leg index` 를 key 로
쓰는데, 그 key 를 만드는 것이 여기 ID 사슬이기 때문이다.

golden vector 가 있는 이유: 직렬화 규칙·arm registry·ID 구성이 **조용히**
바뀌면 이미 만든 모든 `pair_group_id` 가 무효가 되는데, 그것을 알아차릴 방법이
없다. 입력→digest 쌍을 커밋해 두고 매번 다시 계산한다.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from tools.design_wire import (ARM_REGISTRY, CANDIDATE_PAYLOAD_SCHEMA,
                               EXCLUDED_FROM_PAIR_ID, SCHEMA, WireError,
                               assert_wire_safe, bank_id, candidate_id,
                               canonical_design_spec, coords_from_condition,
                               decimal_from_float, pair_group_id,
                               pairing_design_sha256, parameter_order_sha256)

GOLDEN = Path(__file__).resolve().parent.parent / "tools" / "design_golden.yaml"


@pytest.fixture(scope="module")
def golden() -> dict:
    assert GOLDEN.is_file(), f"golden vector 파일이 없다: {GOLDEN}"
    return yaml.safe_load(GOLDEN.read_text(encoding="utf-8"))


def _spec(label: str, arms: list[str], order: list[str]) -> dict:
    return canonical_design_spec(
        label=label, arms=arms, parameter_order=order,
        bounds_policy="exact_ordered_bounds_digest",
        objective_plan=["pocv_dvdq", "pocv_dvdq_dqdv"],
        bank_generator="pcg64", bank_version="v6.0",
        seed_derivation="H(pair_group_id, bank_version)", dtype="float64",
        endian="little", coordinate_unit="fraction")


def test_golden_vectors_recompute_exactly(golden):
    """커밋된 digest 가 지금 코드로 다시 나오는가.

    하나라도 어긋나면 ID 도메인이 바뀐 것이다 — 그때 할 일은 golden 을
    덮는 것이 아니라, **이미 만든 ID 가 전부 무효**라는 것을 인정하고
    새 스키마 버전으로 올리는 것이다.
    """
    order = golden["parameter_order"]
    assert parameter_order_sha256(order) == golden["parameter_order_sha256"]

    shas = {}
    for label, d in golden["designs"].items():
        shas[label] = pairing_design_sha256(_spec(label, d["arms"], order))
        assert shas[label] == d["pairing_design_sha256"], (
            f"{label}: design digest 가 움직였다")

    hc = shas["p22_halfcell_2x2_v6"]
    pos = golden["parameter_order_sha256"]
    for v in golden["vectors"]:
        pg = pair_group_id(hc, v["coords"], pos)
        assert pg == v["pair_group_id"], f"{v['name']}: pair_group_id 가 움직였다"
        bk = bank_id(pg, "v6.0", golden["unit_cube_bank_sha256"])
        assert bk == v["bank_id"], f"{v['name']}: bank_id 가 움직였다"
        for src, want in v["candidate_ids"].items():
            got = candidate_id(bk, golden["exact_bounds_sha256"], src,
                               v["candidate_payloads"][src])
            assert got == want, f"{v['name']}/{src}: candidate_id 가 움직였다"


def test_trailing_zeros_do_not_split_a_condition(golden):
    """`0.17` 과 `0.170` 은 같은 조건이다.

    이진 float 를 금지하는 것만으로는 부족하다 — 후행 0 이 남으면 같은 수가
    다른 `pair_group_id` 를 받아 조건이 **조용히 split** 된다. 계약 §4.2 가
    경고한 "오타 하나로 조용히 merge/split" 의 숫자판이다.

    (초판 golden 이 실제로 둘을 다른 ID 로 냈다. 그것을 보고 고쳤다.)
    """
    order = golden["parameter_order"]
    hc = pairing_design_sha256(_spec("p22_halfcell_2x2_v6", ["A", "B", "C", "D"], order))
    pos = parameter_order_sha256(order)
    base = {"lli": "0.17", "lam_pe": "0.13", "lam_ne": "0.13",
            "lam_pe_type": "capacity", "lam_ne_type": "capacity"}
    padded = dict(base, lli="0.170")
    assert pair_group_id(hc, base, pos) == pair_group_id(hc, padded, pos)
    # 그러나 **다른 수**는 다른 ID 여야 한다
    assert pair_group_id(hc, base, pos) != pair_group_id(hc, dict(base, lli="0.171"), pos)


def test_binary_floats_are_refused_at_the_wire(golden):
    """float 를 실으면 즉시 거부한다 — 조용히 통과하면 ID 가 갈린다."""
    order = golden["parameter_order"]
    hc = pairing_design_sha256(_spec("p22_halfcell_2x2_v6", ["A", "B", "C", "D"], order))
    pos = parameter_order_sha256(order)
    with pytest.raises(WireError) as e:
        pair_group_id(hc, {"lli": 0.17, "lam_pe": "0.13", "lam_ne": "0.13",
                           "lam_pe_type": "capacity", "lam_ne_type": "capacity"}, pos)
    assert "부동소수" in str(e.value)

    for bad in ("1e-3", "0.1.2", ".5", "01", "abc", ""):
        with pytest.raises(WireError):
            pair_group_id(hc, {"lli": bad, "lam_pe": "0.13", "lam_ne": "0.13",
                               "lam_pe_type": "capacity",
                               "lam_ne_type": "capacity"}, pos)


def test_the_same_coordinates_under_a_different_design_are_a_different_group(golden):
    """설계가 다르면 같은 좌표라도 같은 짝이 아니다."""
    cd = golden["cross_design_same_coords"]
    assert cd["halfcell"] != cd["grid"]
    order = golden["parameter_order"]
    pos = parameter_order_sha256(order)
    coords = golden["vectors"][0]["coords"]
    grid = pairing_design_sha256(_spec("p22_grid_primary_v6", ["G_A", "G_C"], order))
    assert pair_group_id(grid, coords, pos) == cd["grid"]


def test_excluded_axes_cannot_sneak_into_a_pair_id(golden):
    """제외하기로 한 축을 좌표에 넣으면 거부한다.

    제외 결정 자체가 설계다 (계약 §4.2). 조용히 받아 주면 `arm` 이 들어간
    순간 짝이 arm 마다 갈리고, 짝을 만드는 목적 자체가 부서진다.
    """
    order = golden["parameter_order"]
    hc = pairing_design_sha256(_spec("p22_halfcell_2x2_v6", ["A", "B", "C", "D"], order))
    pos = parameter_order_sha256(order)
    coords = dict(golden["vectors"][0]["coords"])
    for axis in EXCLUDED_FROM_PAIR_ID:
        with pytest.raises(WireError) as e:
            pair_group_id(hc, dict(coords, **{axis: "x"}), pos)
        assert "없어야 할 키" in str(e.value)


def test_the_arm_registry_matches_the_contract_2x2():
    """계약 §5 의 2×2 가 registry 와 같은가 — 표와 코드가 갈리면 안 된다."""
    contract = (Path(__file__).resolve().parent.parent / "docs" / "22p_gap"
                / "STAGE3_CONTRACT.md").read_text(encoding="utf-8")
    rows = {
        "A": ("off", "off"), "B": ("on", "off"),
        "C": ("off", "on"), "D": ("on", "on"),
    }
    for arm, (p_ini, cond) in rows.items():
        line = f"| {arm} | {p_ini} | {cond} |"
        assert line in contract, f"계약 §5 에 `{line}` 가 없다"
        r = ARM_REGISTRY[arm]
        assert r["p_ini_warm_start"] is (p_ini == "on")
        assert r["condition_warm_start"] is (cond == "on")
        assert r["reference"] == "halfcell"
    for arm in ("G_A", "G_C"):
        assert ARM_REGISTRY[arm]["p_ini_warm_start"] is None, (
            "격자 기준에는 `p_ini` 가 없다 (계약 §5)")


def test_unknown_arms_and_duplicate_parameters_are_refused():
    order = ["lli", "lam_pe", "lam_ne"]
    with pytest.raises(WireError):
        _spec("x", ["A", "Z"], order)
    with pytest.raises(WireError):
        _spec("x", ["A", "A"], order)
    with pytest.raises(WireError):
        _spec("x", ["A"], ["lli", "lli"])
    with pytest.raises(WireError):
        candidate_id("b", "e", "grid", {})          # 모르는 restart source


def test_design_schema_version_is_pinned_in_the_golden_file(golden):
    """스키마 문자열이 바뀌면 golden 이 먼저 깨져야 한다."""
    order = golden["parameter_order"]
    spec = _spec("p22_halfcell_2x2_v6", ["A", "B", "C", "D"], order)
    assert spec["schema"] == SCHEMA
    with pytest.raises(WireError):
        pairing_design_sha256(dict(spec, schema="pairing-design/v99"))


def test_candidate_payloads_follow_a_closed_per_source_schema(golden):
    """★ 26차 P1-8 — 초판은 source enum 만 보고 임의 dict 를 해시했다.

    golden 도 셋 다 placeholder `{"i": 0}` 이었으므로 "candidate provenance 를
    고정했다" 는 말이 성립하지 않았다. 계약 §4.2 는 source 마다 다른 것을
    요구한다.
    """
    bank, bounds = "a" * 64, "b" * 64
    good = golden["vectors"][0]["candidate_payloads"]
    for src, payload in good.items():
        assert candidate_id(bank, bounds, src, payload)          # 정상
        # 키 하나를 빼면 거부
        for k in payload:
            with pytest.raises(WireError):
                candidate_id(bank, bounds, src, {x: v for x, v in payload.items()
                                                 if x != k})
        # 남는 키도 거부 (닫힌 schema)
        with pytest.raises(WireError):
            candidate_id(bank, bounds, src, dict(payload, __extra__="x"))
    # 빈 payload · float · 다른 source 의 payload 전부 거부
    for src in CANDIDATE_PAYLOAD_SCHEMA:
        with pytest.raises(WireError):
            candidate_id(bank, bounds, src, {})
    with pytest.raises(WireError):
        candidate_id(bank, bounds, "random",
                     {"bank_index": 1.0, "unit_cube_bytes_sha256": "c" * 64})
    with pytest.raises(WireError):
        candidate_id(bank, bounds, "warm", good["random"])
    with pytest.raises(WireError):
        candidate_id("짧은-id", bounds, "base_init", good["base_init"])


def test_a_design_alias_change_does_not_move_any_id(golden):
    """★ 26차 P1-7 — 사람용 label 이 정본 hash 안에 있었다.

    뜻이 같은 설계의 별칭만 바꿔도 모든 pair ID 가 바뀌면, label 을 분리한
    의미가 없다 (계약 §4.2).
    """
    order = golden["parameter_order"]
    a = _spec("p22_halfcell_2x2_v6", ["A", "B", "C", "D"], order)
    b = _spec("완전히-다른-별칭", ["A", "B", "C", "D"], order)
    assert pairing_design_sha256(a) == pairing_design_sha256(b)
    with pytest.raises(WireError):
        pairing_design_sha256(dict(a, label="사람용"))


def test_wire_refuses_binary_floats_anywhere_not_just_coordinates():
    """좌표만 막아도 payload 로 들어오면 같은 문제다 — 재귀로 본다."""
    assert_wire_safe({"a": [1, {"b": "c"}], "d": None, "e": True})
    for bad in ({"a": 0.5}, {"a": [1, [2, 3.0]]}, {"a": {"b": {"c": 1e-3}}}):
        with pytest.raises(WireError):
            assert_wire_safe(bad)
    with pytest.raises(WireError):
        assert_wire_safe({1: "int key"})


def test_grid_conditions_bridge_to_wire_coordinates(golden):
    """★ 26차 P1-8 — 실제 `src.grid.Condition` (float) 과 결속한다.

    이 다리가 없으면 ID 체계가 격자와 무관한 장난감이다. 그리고 변환은
    **왕복 검증**을 한다 — 조용히 반올림하면 다른 조건이 같은 ID 로 합쳐진다.
    """
    from src.grid import Condition

    places = golden["decimal_places"]
    order = golden["parameter_order"]
    hc = pairing_design_sha256(_spec("p22_halfcell_2x2_v6", ["A", "B", "C", "D"], order))
    pos = parameter_order_sha256(order)

    for row in golden["grid_linkage"]["rows"]:
        wc = row["wire_coords"]
        c = Condition(lli=float(wc["lli"]), lam_pe=float(wc["lam_pe"]),
                      lam_ne=float(wc["lam_ne"]),
                      lam_pe_type=wc["lam_pe_type"], lam_ne_type=wc["lam_ne_type"],
                      noise=0.001, seed=404)
        assert coords_from_condition(c, places) == wc
        assert pair_group_id(hc, wc, pos) == row["pair_group_id"]

    # 왕복하지 않는 값은 **거부**한다 (조용한 반올림 금지)
    with pytest.raises(WireError) as e:
        decimal_from_float(0.1 + 0.2, 3)
    assert "왕복" in str(e.value)

    # noise·seed 는 조건 정체성에 들어가지 않는다 — 같은 좌표면 같은 ID
    c1 = Condition(lli=0.17, lam_pe=0.13, lam_ne=0.13, lam_pe_type="capacity",
                   lam_ne_type="capacity", noise=0.0, seed=1)
    c2 = Condition(lli=0.17, lam_pe=0.13, lam_ne=0.13, lam_pe_type="capacity",
                   lam_ne_type="capacity", noise=0.005, seed=999)
    assert c1.cond_id != c2.cond_id, "전제: 격자 cond_id 는 noise·seed 를 본다"
    assert coords_from_condition(c1, places) == coords_from_condition(c2, places)


def test_the_design_spec_key_set_is_closed(golden):
    """★ 27차 P1-9 — `{"schema": ...}` 하나로도 정상 digest 가 나왔다.

    extra key 도 통과했다. schema 문자열과 label 부재만 봤기 때문이다.
    """
    order = golden["parameter_order"]
    spec = _spec("p22_halfcell_2x2_v6", ["A", "B", "C", "D"], order)
    assert pairing_design_sha256(spec)

    with pytest.raises(WireError):
        pairing_design_sha256({"schema": SCHEMA})
    with pytest.raises(WireError):
        pairing_design_sha256(dict(spec, __extra__="x"))
    for k in ("arms", "parameter_order", "objective_plan", "bank",
              "parameter_coordinate_schema"):
        with pytest.raises(WireError):
            pairing_design_sha256({x: v for x, v in spec.items() if x != k})


def test_objective_order_is_part_of_design_identity(golden):
    """★ 27차 P1-9 — 초판은 `objective_plan` 을 정렬해 **순서를 지웠다.**

    계약의 objective order 와 warm provider 의미를 design identity 가 잃는다.
    """
    order = golden["parameter_order"]
    a = canonical_design_spec(
        label="x", arms=["A"], parameter_order=order,
        bounds_policy="p", objective_plan=["pocv_dvdq", "pocv_dvdq_dqdv"],
        bank_generator="pcg64", bank_version="v6.0", seed_derivation="s",
        dtype="float64", endian="little", coordinate_unit="fraction")
    b = canonical_design_spec(
        label="x", arms=["A"], parameter_order=order,
        bounds_policy="p", objective_plan=["pocv_dvdq_dqdv", "pocv_dvdq"],
        bank_generator="pcg64", bank_version="v6.0", seed_derivation="s",
        dtype="float64", endian="little", coordinate_unit="fraction")
    assert pairing_design_sha256(a) != pairing_design_sha256(b)

    with pytest.raises(WireError):          # 중복 objective
        canonical_design_spec(
            label="x", arms=["A"], parameter_order=order, bounds_policy="p",
            objective_plan=["o", "o"], bank_generator="g", bank_version="v",
            seed_derivation="s", dtype="float64", endian="little",
            coordinate_unit="fraction")


def test_numeric_and_unicode_domains_are_closed(golden):
    """음수 bank index · 이상한 decimal_places · 비-NFC 문자열을 거부한다."""
    with pytest.raises(WireError):
        candidate_id("a" * 64, "b" * 64, "random",
                     {"bank_index": -1, "unit_cube_bytes_sha256": "c" * 64})
    for places in (True, 0, -3, 99, 2.5):
        with pytest.raises(WireError):
            canonical_design_spec(
                label="x", arms=["A"], parameter_order=["lli"], bounds_policy="p",
                objective_plan=["o"], bank_generator="g", bank_version="v",
                seed_derivation="s", dtype="float64", endian="little",
                coordinate_unit="fraction", decimal_places=places)
    # NFC — 같은 글자의 두 표현이 다른 digest 를 내면 안 된다
    import unicodedata
    comp = unicodedata.normalize("NFC", "\u00e9")
    deco = unicodedata.normalize("NFD", "\u00e9")
    assert comp != deco, "전제: 두 표현이 실제로 달라야 한다"
    assert_wire_safe({"a": comp})                     # NFC 는 통과
    with pytest.raises(WireError) as e:
        assert_wire_safe({"a": deco})                 # 분해형 **값**은 거부
    assert "NFC" in str(e.value)
    with pytest.raises(WireError) as e:                # 분해형 **키**도 거부
        assert_wire_safe({deco: "x"})
    assert "NFC" in str(e.value)


def test_nested_design_blocks_are_validated_not_just_top_level_keys(golden):
    """★ 28차 P1-6 — 초판 validator 는 top-level 키만 닫았다.

    factory 는 엄격했지만 **역직렬화한 외부 spec** 을 해시하는 validator 는
    nested 를 다시 보지 않았다. 리뷰가 준 다섯 변이가 전부 정상 digest 를 냈다.
    """
    order = golden["parameter_order"]
    spec = _spec("p22_halfcell_2x2_v6", ["A", "B", "C", "D"], order)
    assert pairing_design_sha256(spec)

    muts = {
        "empty_coordinate": dict(spec, coordinate={}),
        "fake_arm": dict(spec, arms=dict(spec["arms"], ZZ={"arm_id": "ZZ"})),
        "duplicate_objectives": dict(spec, objective_plan=["o", "o"]),
        "open_serialization": dict(spec, serialization={"encoding": "utf-8"}),
        "empty_candidate_schema": dict(spec, candidate_payload_schema={}),
        "empty_parameter_order": dict(spec, parameter_order=[]),
        "bogus_bank": dict(spec, bank={"generator": "g"}),
        "arm_content_changed": dict(
            spec, arms=dict(spec["arms"],
                            A=dict(spec["arms"]["A"], role="다른 역할"))),
    }
    for name, m in muts.items():
        with pytest.raises(WireError):
            pairing_design_sha256(m)


def test_parent_digest_domains_and_type_axis_nfc_are_checked(golden):
    """부모 digest 가 64-hex 인지, type 축이 NFC 인지 검사한다."""
    order = golden["parameter_order"]
    hc = pairing_design_sha256(_spec("p22_halfcell_2x2_v6", ["A", "B", "C", "D"], order))
    pos = parameter_order_sha256(order)
    coords = dict(golden["vectors"][0]["coords"])

    with pytest.raises(WireError):
        pair_group_id("짧다", coords, pos)
    with pytest.raises(WireError):
        pair_group_id(hc, coords, "짧다")
    with pytest.raises(WireError):
        bank_id("짧다", "v6.0", "f" * 64)
    with pytest.raises(WireError):
        parameter_order_sha256([])
    with pytest.raises(WireError):
        parameter_order_sha256(["a", "a"])

    # type 축의 분해형 문자열 — 같은 글자가 다른 ID 를 받으면 안 된다.
    # (리터럴로 쓰면 편집기·heredoc 이 NFC 로 합쳐 버리므로 만들어 쓴다.)
    import unicodedata
    decomposed = unicodedata.normalize("NFD", "capacit\u00e9")
    assert decomposed != unicodedata.normalize("NFC", decomposed), "전제"
    with pytest.raises(WireError) as e:
        pair_group_id(hc, dict(coords, lam_pe_type=decomposed), pos)
    assert "NFC" in str(e.value)


def test_a_warm_candidate_must_name_an_objective_in_the_design(golden):
    """★ 28차 P1-6 — `provider_objective='not-in-design'` 이 통과했다."""
    plan = ["pocv_dvdq", "pocv_dvdq_dqdv"]
    good = {"provider_objective": "pocv_dvdq",
            "provider_artifact_sha256": "2" * 64, "solution_map_sha256": "3" * 64}
    assert candidate_id("a" * 64, "b" * 64, "warm", good, objective_plan=plan)
    with pytest.raises(WireError) as e:
        candidate_id("a" * 64, "b" * 64, "warm",
                     dict(good, provider_objective="not-in-design"),
                     objective_plan=plan)
    assert "objective" in str(e.value)
