"""grid 순수 로직 테스트 (solve 없음 — 빠름)."""

from __future__ import annotations

import numpy as np
import pytest

from src.grid import (Condition, axis_from_config, build_conditions,
                      conditions_from_config, parse_axis)



def _tok() -> str:
    """이 시험이 쓰는 소유 증명.

    ★ 54차 P0-6 — 발급은 소유 증명을 **caller 에게서** 받는다. 암묵적 생성은
      메모리에만 있는 credential 을 만들고, 실패 한 번이면 그 다리는 재개도
      되돌림도 못 하는 상태로 굳는다 (리뷰어 실측).
    """
    from tools.preserve import _new_token

    return _new_token()


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


# ─────────────────────────────────────────────────────────────────────────────
# 49차 P0-3 — `--dry-run` 이 계획을 `running` 에 영구히 남겼다
# ─────────────────────────────────────────────────────────────────────────────

def _plan_for_live_grid(led, leg, out_dir, cfg, src_digest):
    """지금 코드가 만들 **살아 있는** grid spec 을 그대로 승인하는 계획 원장.

    사람이 계획을 적을 때 하는 일과 같다 — 무엇을 돌릴지 선언하고 그 digest 를
    봉인한다. 조건이 없는 dry-run 이므로 조건 집합은 빈 목록이다.
    """
    import yaml

    import src.grid as G
    from tools.preserve import leg_run_spec, run_spec_digest

    # ★ 51차 — 계획 축은 production 과 **같은 함수**로 만든다. 손으로 적으면
    #   축이 하나 늘 때마다 시험이 낡은 축을 승인하고, 그 낡음이 곧 false green
    #   이다 (49차에 fit 축에서 같은 일이 있었다).
    grid_axis = G.live_grid_axis(cfg, [], out_dir)
    fit_axis = {"config_digest": "0" * 16, "objective_order": ["pocv_dvdq"],
                "objectives_digest": "0" * 16,
                "reference": "grid",
                "halfcell_recipe": {"method": "ocp", "kw": {}},
                "halfcell_cache_sha256": None, "base_config_digest": "0" * 16,
                "bounds_preset": "expanded", "bounds_digest": "0" * 16,
                "optimizer": {"method": "Nelder-Mead", "n_restarts": 5,
                              "adaptive": True, "warm_start": True},
                "use_noisy": True, "smoothing_backend": "banded_cache",
                "row_selection": {"mode": "full", "limit": None,
                                  "subset_sha256": None},
                "in": G.leg_out_key(out_dir), "in_digest": None,
                "out": G.leg_out_key(out_dir)}
    spec = leg_run_spec(leg, grid_axis, fit_axis)
    doc = {
        "schema_version": 4,
        "cohorts": [{"cohort_id": "g49", "dir": "docs/22p_gap/coh",
                     "status": "active", "legs": [],
                     "prospective_legs": [leg],
                     "cross_leg_comparison": "allowed_within_cohort",
                     "pin": {"schema_version": 3,
                             "compute_sha256": "a" * 16,
                             "row_projection_py_sha256": "b" * 16,
                             "src_scoring_py_sha256": "c" * 16,
                             "analysis_spec_sha256": "d" * 16,
                             "producer_semantic_sha256": "e" * 16}}],
        "planned": [{"leg_id": leg, "cohort_id": "g49", "status": "planned",
                     "authorization_kind": "prospective",
                     "authorized_source_digest": src_digest,
                     "run_spec_digest": run_spec_digest(spec),
                     "run_spec": spec,
                     "recorded_on": "2026-08-28",
                     "근거": "시험용 — dry-run lifecycle"}],
        "legs": []}
    led.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False),
                   encoding="utf-8")
    return spec


def test_a_dry_run_does_not_strand_the_plan_in_running(monkeypatch, tmp_path):
    """★ 49차 P0-3 — dry-run 은 실행권을 **되돌린다.**

    47차가 dry-run 면제를 없앤 것은 옳다 — `run_grid(dry_run=True)` 는 최대 세
    조건에 solver 를 실제로 부른다. 그런데 48차가 claim 에 원장 전이를
    붙이면서, dry-run 은 계획을 `planned → running` 으로 옮겨 놓고 phase 를
    하나도 닫지 않고 끝나게 됐다. `finalize_leg()` 은 "phase 가 남았다" 며
    거부하므로 그 다리는 **다시 시작할 수도 닫을 수도 없는** terminal 상태로
    굳는다. 면제가 아니라 되돌림이 답이다.
    """
    import pathlib
    import tempfile

    import src.grid as G
    from src.baseline import DischargedState
    from src.config import load_config
    from src.io import source_digest
    from tools import preserve as P

    # smoke namespace **밖**이어야 gate 가 실제로 걸린다 (conftest 의 tmp_path
    # 는 gated entrypoint 시험을 위해 smoke 안으로 옮겨져 있다).
    out_dir = pathlib.Path(tempfile.mkdtemp(prefix="dd49-dry-"))
    led = pathlib.Path(tempfile.mkstemp(prefix="dd49-led-", suffix=".yaml")[1])
    claims = out_dir / "_claims"
    monkeypatch.setattr(P, "DEFAULT_LEDGER", led)
    monkeypatch.setattr(P, "DEFAULT_CLAIMS_ROOT", claims)
    monkeypatch.setattr(G, "get_discharged_state",
                        lambda cfg, *a, **k: DischargedState(1.0, 2.0, 3.0))

    cfg = load_config("configs/grid_coarse.yaml")
    _plan_for_live_grid(led, "L49", out_dir, cfg, source_digest())

    tok = out_dir / "L49.token"
    summary = G.run_grid(cfg, [], nproc=1, chunk_size=1, out_dir=out_dir,
                         dry_run=True, leg="L49", token_file=tok)
    assert summary["dry_run"] is True

    assert P.planned_index(ledger=led)["L49"]["status"] == "planned", (
        "dry-run 이 계획을 running 에 남겼다 — 그 다리는 다시 시작할 수도 "
        "닫을 수도 없다")
    assert not (claims / "L49.claim").exists(), "dry-run 이 claim 을 남겼다"
    assert not tok.exists(), "dry-run 이 소유 증명 파일을 남겼다"

    # 되돌렸으므로 **진짜 실행**이 바로 시작될 수 있다 — 되돌림의 유일한 증명
    P.claim_planned_leg("L49", P.declared_leg_run_spec("L49", ledger=led),
                        source_digest(), ledger=led, token=_tok())


# ─────────────────────────────────────────────────────────────────────────────
# 51차 P0-A4 — 완방상태 cache 가 grid 승인 밖에서 실제 곡선을 바꾼다
# ─────────────────────────────────────────────────────────────────────────────

def test_the_grid_axis_binds_the_discharged_state_cache(tmp_path, monkeypatch):
    """★ 51차 P0-A4 — 승인 축이 완방상태 캐시의 **바이트**를 담는다.

    리뷰어 실측: 두 캐시 모두 production reader 의 baseline/solver/
    effective-solver/source/runtime 검사를 통과하고 값도 finite 인데, 숫자만
    다르게 두고 같은 config·Condition·out 으로 real PyBaMM 을 돌렸다.

        authorization_digest_A == authorization_digest_B   (같다)
        q_mah_A=5621.148...    q_mah_B=5540.776...         (다르다)

    사후 grid signature 에는 `discharged_sha` 가 있다. **사전 승인에는 없었다** —
    실행 뒤에 무엇을 읽었는지 적는 것과 실행 전에 무엇을 읽을지 승인하는 것은
    다른 명제다.
    """
    import src.grid as G
    from src.config import load_config

    cfg = load_config("configs/grid_coarse.yaml")
    cache = tmp_path / "discharged.json"

    cache.write_text('{"ne_primary": 1.0, "ne_secondary": 2.0, "pe": 3.0}',
                     encoding="utf-8")
    monkeypatch.setattr(G, "discharged_cache_path_for", lambda c: cache)
    a = G.live_grid_axis(cfg, [], tmp_path)

    cache.write_text('{"ne_primary": 9.0, "ne_secondary": 2.0, "pe": 3.0}',
                     encoding="utf-8")
    b = G.live_grid_axis(cfg, [], tmp_path)

    assert a != b, ("완방상태 캐시를 갈아도 승인 digest 가 같다 — 승인 밖에서 "
                    "격자 truth 의 기준점이 움직인다")


# ─────────────────────────────────────────────────────────────────────────────
# 52차 P0-5 — 승인한 cache bytes 가 authoritative 하지 않다
# ─────────────────────────────────────────────────────────────────────────────

def test_the_approved_cache_bytes_are_authoritative(tmp_path, monkeypatch):
    """★ 52차 P0-5 — 승인한 바이트를 주면 **그것을 쓰거나 거부**한다.

    리뷰어 반례: `src/grid.py` 는 승인 digest 와 맞는 bytes 를 넘기지만
    `src/baseline.py` 는 runtime/source 불일치를 **cache miss 로 바꿔 재계산**한다.

        APPROVED_SHA_MATCH=True
        APPROVED_STATE=(1.0, 2.0, 3.0)
        RECOMPUTE_CALLS=1
        CONSUMED_STATE=(101.0, 202.0, 303.0)

    "그 파일이 stale 이면 다시 계산한다" 는 캐시로서는 옳은 정책이지만,
    **승인이 그 바이트를 가리킬 때는** 아니다. 승인한 것과 다른 것을 계산하는
    셋째 길이 있으면 승인은 승인이 아니다.
    """
    import json

    import src.baseline as B

    cfg = {"discharged_state": {"cache": True},
           "baseline": {}, "solver": {"kind": "casadi"}}
    monkeypatch.setattr(B, "baseline_hash", lambda c: "bh")
    monkeypatch.setattr(B, "_cache_path", lambda c, d: tmp_path / "d.json")
    calls = {"n": 0}

    def _boom(c, solver=None):
        calls["n"] += 1
        return B.DischargedState(101.0, 202.0, 303.0)

    monkeypatch.setattr(B, "compute_discharged_state", _boom)

    raw = json.dumps({"ne_primary": 1.0, "ne_secondary": 2.0, "pe": 3.0,
                      "baseline_hash": "bh", "solver": {"kind": "casadi"},
                      "effective_solver": {"cls": "다른 것"},
                      "source_digest": "다른 코드",
                      "env": {"python": "다른 runtime"}}).encode("utf-8")

    with pytest.raises(RuntimeError) as ei:
        B.get_discharged_state(cfg, cache_bytes=raw)
    assert calls["n"] == 0, (
        "승인한 바이트를 주었는데 재계산했다 — 승인 밖의 값이 격자 truth 가 된다")
    assert "승인" in str(ei.value) or "authoritative" in str(ei.value), str(ei.value)
