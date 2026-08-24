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

from tools.design_wire import (ARM_REGISTRY, EXCLUDED_FROM_PAIR_ID, SCHEMA,
                               WireError, bank_id, candidate_id,
                               canonical_design_spec, pair_group_id,
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
            got = candidate_id(bk, golden["exact_bounds_sha256"], src, {"i": 0})
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
