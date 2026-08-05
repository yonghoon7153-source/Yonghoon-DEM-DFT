"""grid 순수 로직 테스트 (solve 없음 — 빠름)."""

from __future__ import annotations

import numpy as np
import pytest

from src.grid import (Condition, axis_from_config, build_conditions,
                      conditions_from_config, parse_axis)


def test_parse_axis_range():
    np.testing.assert_allclose(parse_axis("0:0.2:0.05"), [0, 0.05, 0.1, 0.15, 0.2])
    np.testing.assert_allclose(parse_axis("0:0.2:0.02"),
                               np.round(np.arange(0, 0.21, 0.02), 10))


def test_parse_axis_list_scalar_none():
    np.testing.assert_allclose(parse_axis("0,0.05,0.1"), [0, 0.05, 0.1])
    np.testing.assert_allclose(parse_axis("0.1"), [0.1])
    np.testing.assert_allclose(parse_axis("none"), [0.0])
    np.testing.assert_allclose(parse_axis(None), [0.0])
    np.testing.assert_allclose(parse_axis(0.3), [0.3])


def test_parse_axis_errors():
    with pytest.raises(ValueError):
        parse_axis("0:0.2")           # step 누락
    with pytest.raises(ValueError):
        parse_axis("0:0.2:-0.1")      # 음수 step


def test_axis_from_config_dict():
    np.testing.assert_allclose(
        axis_from_config({"start": 0.0, "stop": 0.20, "step": 0.05}),
        [0, 0.05, 0.1, 0.15, 0.2])


def test_build_conditions_product_and_seed():
    conds = build_conditions(parse_axis("0:0.2:0.05"), parse_axis("0:0.2:0.05"),
                             parse_axis("0:0.2:0.05"), ["de"], ["de"],
                             parse_axis("0"), noise_seed=42)
    assert len(conds) == 125
    # cond_id 고유 + 결정적
    ids = {c.cond_id for c in conds}
    assert len(ids) == 125
    again = build_conditions(parse_axis("0:0.2:0.05"), parse_axis("0:0.2:0.05"),
                             parse_axis("0:0.2:0.05"), ["de"], ["de"],
                             parse_axis("0"), noise_seed=42)
    assert [c.cond_id for c in conds] == [c.cond_id for c in again]
    # seed도 조건별 결정적
    assert conds[7].seed == again[7].seed


def test_both_types_multiply():
    conds = build_conditions(parse_axis("0"), parse_axis("0,0.1"), parse_axis("0"),
                             ["de", "li"], ["de"], parse_axis("0"), 42)
    assert len(conds) == 4  # lam_pe 2 × type 2


def test_conditions_from_config_coarse(cfg):
    from src.config import load_config
    from tests.conftest import ROOT

    c = load_config(ROOT / "configs" / "grid_coarse.yaml")
    conds = conditions_from_config(c)
    assert len(conds) == 125
    assert all(x.lam_pe_type == "de" and x.lam_ne_type == "de" for x in conds)


def test_cli_axis_overrides_config():
    from src.config import load_config
    from tests.conftest import ROOT

    c = load_config(ROOT / "configs" / "grid_coarse.yaml")
    conds = conditions_from_config(c, cli={"lli": "0", "lam_pe": "0,0.1",
                                           "lam_ne": "none"})
    assert len(conds) == 2


def test_condition_id_stable_repr():
    c = Condition(0.1, 0.05, 0.2, "de", "de", 0.0, 42)
    assert c.cond_id == Condition(0.1, 0.05, 0.2, "de", "de", 0.0, 42).cond_id
    assert c.cond_id != Condition(0.1, 0.05, 0.2, "de", "li", 0.0, 42).cond_id
