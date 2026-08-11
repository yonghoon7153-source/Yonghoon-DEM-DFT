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


def test_grid_cli_noise_seed_reaches_signed_spec(monkeypatch, tmp_path):
    """★ 10차 자체 리뷰 — CLI `--noise-seed` 가 조건 생성에만 쓰이고 서명
    (grid_run_spec)·curves_manifest 는 config 의 seed(42)를 봉인했다.
    재현 기록이 거짓이 되므로, CLI 값은 cfg 로 일원화돼야 한다."""
    import sys

    import src.grid as G

    captured = {}

    def fake_run_grid(cfg, conditions, **kw):
        captured["cfg"] = cfg
        captured["conds"] = conditions
        return {"dry_run": True}

    monkeypatch.setattr(G, "run_grid", fake_run_grid)
    monkeypatch.setattr(sys, "argv",
                        ["grid", "--config", "configs/grid_coarse.yaml",
                         "--noise-seed", "7", "--out", str(tmp_path)])
    G.main()

    # 서명이 읽는 cfg 에 CLI seed 가 반영됐다
    assert captured["cfg"]["grid"]["noise_seed"] == 7
    spec, _ = G.grid_run_spec(captured["cfg"], captured["conds"],
                              discharged={"ne_primary": 1.0}, discharged_sha="0" * 64)
    assert spec["noise_seed"] == 7
    # 조건별 seed 도 같은 값에서 유도된다 (조건 생성과 기록의 일원화)
    ref = G.conditions_from_config(captured["cfg"], cli={})
    assert [c.seed for c in captured["conds"]] == [c.seed for c in ref]
