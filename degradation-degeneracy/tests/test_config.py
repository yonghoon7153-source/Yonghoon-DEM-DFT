"""config 로드/병합/검증/해시 테스트 (빠름)."""

from __future__ import annotations

import pytest

from src.config import ConfigError, baseline_hash, config_hash, load_config, validate_config
from tests.conftest import ROOT


def test_base_loads_and_validates(cfg):
    assert cfg["parameter_set"] == "Chen2020_composite"
    assert cfg["baseline"]["ne_primary_init_conc"] == 27700.0


def test_extends_merge():
    c = load_config(ROOT / "configs" / "grid_coarse.yaml")
    validate_config(c)                       # base 키가 상속됨
    assert c["grid"]["lli"]["step"] == 0.05  # 자식 키
    assert c["baseline"]["pe_vf"] == 0.665   # 부모 키


def test_missing_key_raises(cfg):
    broken = {k: v for k, v in cfg.items() if k != "baseline"}
    with pytest.raises(ConfigError, match="baseline"):
        validate_config(broken)


def test_hash_stable_and_sensitive(cfg):
    h1 = config_hash(cfg)
    assert h1 == config_hash(dict(cfg))
    changed = {**cfg, "baseline": {**cfg["baseline"], "pe_vf": 0.7}}
    assert config_hash(changed) != h1
    assert baseline_hash(changed) != baseline_hash(cfg)


def test_baseline_hash_ignores_grid(cfg):
    """grid 축이 바뀌어도 완방상태 캐시는 무효화되지 않아야 한다."""
    changed = {**cfg, "grid": {"lli": {"start": 0, "stop": 1, "step": 0.5}}}
    assert baseline_hash(changed) == baseline_hash(cfg)
