"""82차 잔여 G82-N1 · N2 · N3 — 시작 전 고정 표 `docs/22p_gap/STAGE3_IMPL_ROUND1_SPEC.md` §10.

N1 관측 roster 를 **출력에서** 재구성한다 (봉인 curves 스냅샷 ↔ fits 행 ↔ 계획 · record).
N2 bank 선언 (설계 · envelope) 이 실제 구현 profile 과 같아야 한다 (시작 전 소비자 · validator 양쪽).
N3 sig 6 ↔ 계획 · record protocol_generation ↔ 행 record_generation 선언 연결.

음성 자료는 **봉인 · record 해시를 일관되게 다시 맞춘** 위조다 — 봉인이 깨져서 걸리는 것은 이 시험의 축이 아니다
(검토자 §2 "파일 봉인만 정상 방식으로 갱신한 경우"). 각 음성은 새 검사의 이름과 이유 문장을 함께 본다.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
from types import SimpleNamespace

import pandas as pd
import pytest
import yaml

from src import fitting as F
from src import io as IO
from tests import test_gate81_stage3_wire as G81
from tools import design_wire as DW
from tools import preserve as PV

OBJS = G81.OBJS


# ─────────────────────────────────────────────────────────────────────────────
# 위조 도구 — 봉인 · record digest 를 다시 맞춘다
# ─────────────────────────────────────────────────────────────────────────────
def _reseal_fits(out: Path) -> None:
    """fits.parquet 을 고친 뒤 manifest 의 `fits_seal` 을 실물에서 다시 계산해 맞춘다."""
    mp = out / "manifest.yaml"
    man = yaml.safe_load(mp.read_text(encoding="utf-8"))
    now = IO.fits_seal(out / "fits.parquet", cond_ids=None, objective_order=None)
    for k in ("file_sha256", "n_rows", "key_sha256", "cond_sha256", "n_conditions", "n_objectives"):
        man["fits_seal"][k] = now[k]
    mp.write_text(yaml.safe_dump(man, allow_unicode=True), encoding="utf-8")


def _rewrite_record(out: Path, mutate) -> dict:
    rec = json.loads((out / "execution_record.json").read_text(encoding="utf-8"))
    mutate(rec)
    rec["record_digest"] = PV.digest({k: v for k, v in rec.items() if k != "record_digest"})
    (out / "execution_record.json").write_bytes(PV.canonical_bytes(rec))
    return rec


def _forge_stage3(out: Path, *, env_mutate=None, design_mutate=None) -> None:
    """run_spec.stage3 의 계획 envelope · 설계를 바꾸고 digest 사슬 (설계 sha · planned_id · record) 을 다시 맞춘다."""
    mp = out / "manifest.yaml"
    man = yaml.safe_load(mp.read_text(encoding="utf-8"))
    s3 = man["run_spec"]["stage3"]
    if design_mutate is not None:
        design_mutate(s3["pairing_design"])
        d_sha = DW.pairing_design_sha256(s3["pairing_design"])
        s3["pairing_design_sha256"] = d_sha
        s3["planned_envelope"]["pairing_design_sha256"] = d_sha
    if env_mutate is not None:
        env_mutate(s3["planned_envelope"])
    s3["planned_id"] = PV.digest(s3["planned_envelope"])
    mp.write_text(yaml.safe_dump(man, allow_unicode=True), encoding="utf-8")
    env = s3["planned_envelope"]
    _rewrite_record(out, lambda r: r.update(planned_id=s3["planned_id"],
                                            protocol_generation=env["protocol_generation"]))


def _two_noise_run(tmp_path, name="o"):
    in_dir = G81._two_noise_curves(tmp_path / "in")
    ctx = G81._v6_context(in_dir, budget=2)
    out = G81._run_v6(tmp_path, name, ctx, in_dir)
    return in_dir, ctx, out


def _pair_cond_ids(fits: pd.DataFrame) -> list[str]:
    """같은 pair_group (lli 0.02) 의 두 noise 실현 cond_id — noise 0 먼저."""
    sub = fits[fits["lli"] == 0.02].drop_duplicates("cond_id").sort_values("noise")
    assert len(sub) == 2, sub
    return list(sub["cond_id"])


# ═════════════════════════════════════════════════════════════════════════════
# N1 관측 roster 재구성
# ═════════════════════════════════════════════════════════════════════════════
def test_g82_n1_00_two_noise_realizations_rebuild_the_planned_roster_from_outputs(tmp_path):
    """양성: 같은 pair_group 의 두 noise 실현 · 두 objective. 새 검사가 있고 통과하며, record 의 roster SHA 는
    출력에서 재구성한 값과 같다 (시작 전 SHA 복사가 아니다)."""
    in_dir, ctx, out = _two_noise_run(tmp_path)
    v = IO.validate_provenance(out)
    assert v["checks"].get("관측_roster_재구성") == "통과", v["checks"].get("관측_roster_재구성", "검사 없음")
    assert G81._fails(v) == [], v["fail"]
    fits = pd.read_parquet(out / "fits.parquet")
    cur = pd.read_parquet(in_dir / "curves.parquet")
    entries, problems = IO.observed_roster(fits, cur, design=ctx["design"], planned_env=ctx["planned"].envelope())
    assert problems == []
    rec = json.loads((out / "execution_record.json").read_text(encoding="utf-8"))
    assert rec["realized"]["roster_observed_sha256"] == DW.roster_sha256(entries) \
        == ctx["planned"].envelope()["roster"]["roster_sha256"]


def test_g82_n1_01_one_objective_row_with_a_changed_noise_is_refused_after_a_consistent_reseal(tmp_path):
    """음성: 한 objective 행의 noise 만 다른 유한 값으로 · cond_id · 물리좌표 · map · restart · record 보존 · fits 봉인은
    정상 방식으로 다시 맞춤 (검토자 §2 정적 반례)."""
    _, _, out = _two_noise_run(tmp_path)
    fits = pd.read_parquet(out / "fits.parquet")
    _, b = _pair_cond_ids(fits)
    idx = fits.index[(fits["cond_id"] == b) & (fits["objective"] == OBJS[1])][0]
    fits.loc[idx, "noise"] = 0.002
    fits.to_parquet(out / "fits.parquet", index=False)
    _reseal_fits(out)
    v = IO.validate_provenance(out)
    assert v["checks"]["출력봉인_재계산"] == "통과", "봉인은 일관되게 다시 맞췄다 — 이 음성은 봉인으로 걸리면 안 된다"
    assert "관측_roster_재구성" in v["fail"], v["fail"]
    assert "noise" in v["checks"]["관측_roster_재구성"], v["checks"]["관측_roster_재구성"]


def test_g82_n1_02_crossed_noise_realizations_are_refused_after_a_consistent_reseal(tmp_path):
    """음성: 같은 pair_group 두 실현의 noise 를 맞바꾼다 (두 objective 행 모두) — 개수 · 집합 · pair_group 은 그대로."""
    _, _, out = _two_noise_run(tmp_path)
    fits = pd.read_parquet(out / "fits.parquet")
    a, b = _pair_cond_ids(fits)
    na = float(fits.loc[fits["cond_id"] == a, "noise"].iloc[0])
    nb = float(fits.loc[fits["cond_id"] == b, "noise"].iloc[0])
    fits.loc[fits["cond_id"] == a, "noise"] = nb
    fits.loc[fits["cond_id"] == b, "noise"] = na
    fits.to_parquet(out / "fits.parquet", index=False)
    _reseal_fits(out)
    v = IO.validate_provenance(out)
    assert v["checks"]["출력봉인_재계산"] == "통과"
    assert "관측_roster_재구성" in v["fail"], v["fail"]
    assert "noise" in v["checks"]["관측_roster_재구성"], v["checks"]["관측_roster_재구성"]


def test_g82_n1_03_a_record_roster_of_the_same_size_but_another_observation_set_is_refused(tmp_path):
    """음성: record 의 roster_observed_sha256 를 같은 n_obs 의 **다른 유효 roster** 로 (record_digest 재계산)."""
    from src.grid import Condition
    in_dir, ctx, out = _two_noise_run(tmp_path)
    cur = pd.read_parquet(in_dir / "curves.parquet")
    conds = [Condition(float(g["lli"].iloc[0]), float(g["lam_pe"].iloc[0]), float(g["lam_ne"].iloc[0]),
                       str(g["lam_pe_type"].iloc[0]), str(g["lam_ne_type"].iloc[0]), float(g["noise"].iloc[0]),
                       int(g["seed"].iloc[0]) + 100) for _, g in cur.groupby("cond_id")]
    other = DW.roster_from_conditions(conds, design=ctx["design"], comparison_family_id="p22_grid_primary_v6",
                                      treatment_id="none", replicate_id=0)
    assert len(other) == ctx["planned"].envelope()["roster"]["n_obs"]
    _rewrite_record(out, lambda r: r["realized"].update(roster_observed_sha256=DW.roster_sha256(other)))
    v = IO.validate_provenance(out)
    assert "관측_roster_재구성" in v["fail"], v["fail"]
    assert "record" in v["checks"]["관측_roster_재구성"], v["checks"]["관측_roster_재구성"]


def test_g82_n1_04_without_the_sealed_curves_snapshot_the_roster_cannot_be_rebuilt(tmp_path):
    """음성 (fail-closed): 봉인 curves 스냅샷이 없으면 관측 roster 를 재구성하지 못한다 — 추론으로 채우지 않는다."""
    _, _, out = _two_noise_run(tmp_path)
    snaps = sorted((out / "_inputs").glob("*_curves.parquet"))
    assert snaps, "v6 산출에는 봉인 curves 스냅샷이 있다"
    for s in snaps:
        s.unlink()
    v = IO.validate_provenance(out)
    assert "관측_roster_재구성" in v["fail"], v["fail"]
    assert "스냅샷" in v["checks"]["관측_roster_재구성"], v["checks"]["관측_roster_재구성"]


def test_g82_n1_05_the_writer_computes_the_observed_roster_and_refuses_rows_that_disagree_with_the_inputs(tmp_path):
    """writer: roster_observed 는 fits + 실행이 읽은 curves 에서 계산한다 · 봉인 입력과 다른 행이면 기록을 쓰지 않는다."""
    in_dir, ctx, out = _two_noise_run(tmp_path)
    fits = pd.read_parquet(out / "fits.parquet")
    cur = pd.read_parquet(in_dir / "curves.parquet")
    env = ctx["planned"].envelope()
    d = tmp_path / "w"; d.mkdir()
    rec = F.write_execution_record(d, fits, planned_env=env, objective_order=OBJS, curves_df=cur, design=ctx["design"])
    assert rec["realized"]["roster_observed_sha256"] == env["roster"]["roster_sha256"]
    bad = fits.copy()
    _, b = _pair_cond_ids(bad)
    bad.loc[bad["cond_id"] == b, "noise"] = 0.002
    d2 = tmp_path / "w2"; d2.mkdir()
    with pytest.raises((ValueError, RuntimeError), match="noise"):
        F.write_execution_record(d2, bad, planned_env=env, objective_order=OBJS, curves_df=cur, design=ctx["design"])
    assert not (d2 / "execution_record.json").exists()


# ═════════════════════════════════════════════════════════════════════════════
# N2 지원 bank profile
# ═════════════════════════════════════════════════════════════════════════════
#: 변경 전 실측 (STAGE3_IMPL_ROUND1_SPEC §10-2) — 정상 bank 바이트는 이번 보완으로 움직이지 않는다
_GOLDEN_PG = "c6fc40f168f0af2943a8322ce5b5727a3dbf209c393321c85d438e2a153297b3"
_GOLDEN_BANK_SHA = "c3009d16773fe211abfc54a6e48d731dcfa8cbef17867d9190a2b39e139a9894"


def test_g82_n2_00_the_supported_profile_passes_and_names_the_implementation():
    """양성: fixture 설계 · envelope 는 지원 profile 과 같다 (설계 · envelope · 서로)."""
    design = G81._design()
    env = G81._planned_v4().envelope()
    assert DW.check_bank_profile(design["bank"], env["bank"]) == []
    assert DW.check_bank_profile(design_bank=design["bank"]) == []
    assert DW.check_bank_profile(envelope_bank=env["bank"]) == []


def test_g82_n2_00b_normal_bank_bytes_are_unchanged():
    """대조군 (처음부터 GREEN): 정상 profile 의 bank 바이트 골든 — 이번 보완은 생성 방식을 바꾸지 않는다."""
    assert G81._pair_group() == _GOLDEN_PG
    assert DW.unit_cube_bank_sha256(DW.unit_cube_bank(_GOLDEN_PG, "v6.0", 8, 4)) == _GOLDEN_BANK_SHA


@pytest.mark.parametrize("field,value", [
    ("generator", "philox"), ("version", "v6.1"), ("seed_derivation", "H(cond_id)"),
    ("dtype", "float32"), ("endian", "big")])
def test_g82_n2_01_an_unsupported_design_declaration_is_refused_by_the_checker(field, value):
    """음성: 설계 bank 의 각 필드가 지원 profile 과 다르면 거부 (별칭 없음 · 새 generator 구현 없음)."""
    b = dict(G81._design()["bank"]); b[field] = value
    probs = DW.check_bank_profile(design_bank=b)
    assert probs and any("bank profile" in p and field in p for p in probs), probs


def test_g82_n2_02_an_envelope_declaring_another_generator_is_refused_before_it_is_sealed():
    """음성: 설계는 pcg64 인데 envelope 만 philox — 계획 봉인 (`PlannedLegV4`) 단계에서 거부 · 양쪽 같은 미지원도 거부."""
    with pytest.raises(PV.PreserveError, match="bank profile"):
        G81._planned_v4(bank={"generator": "philox", "version": "v6.0", "length": 8, "n_params": 4,
                              "exact_bounds_sha256": DW.exact_bounds_sha256(G81.LB, G81.UB)})
    env = G81._planned_v4().envelope()
    env["bank"]["version"] = "v6.1"
    assert any("bank profile" in p for p in PV.check_planned_envelope(env))


def _stub_planned(env: dict):
    return SimpleNamespace(envelope=lambda: copy.deepcopy(env), planned_id=lambda: PV.digest(env))


def test_g82_n2_03_the_consumer_refuses_to_start_on_a_design_envelope_profile_mismatch(tmp_path):
    """음성 (시작 전 소비자): 설계 dtype float32 · 양쪽 philox · 설계 v6.0 ↔ envelope v6.1 → fits 를 만들기 전에 거부."""
    from tests.test_fitting import _tiny_curves
    in_dir = _tiny_curves(tmp_path / "in")
    # (a) 설계만 미지원 dtype — 계획은 그 설계 digest 로 정상 봉인된다
    d = G81._design(); d["bank"]["dtype"] = "float32"
    with pytest.raises(ValueError, match="bank profile"):
        G81._run_v6(tmp_path, "a", G81._v6_context(in_dir, design=d), in_dir)
    assert not (tmp_path / "a" / "fits.parquet").exists()
    # (b) envelope 가 봉인 검사를 우회해 들어와도 (stub) 시작 전 검사가 막는다
    ctx = G81._v6_context(in_dir)
    env = ctx["planned"].envelope(); env["bank"]["generator"] = "philox"
    with pytest.raises(ValueError, match="bank profile"):
        G81._run_v6(tmp_path, "b", {**ctx, "planned": _stub_planned(env)}, in_dir)
    assert not (tmp_path / "b" / "fits.parquet").exists()


def test_g82_n2_04_the_validator_refuses_a_forged_design_or_envelope_profile(tmp_path):
    """음성 (validator): 정상 v6 산출의 run_spec 설계 dtype · envelope generator 를 바꾸고 digest 사슬을 다시 맞춘다."""
    from tests.test_fitting import _tiny_curves
    in_dir = _tiny_curves(tmp_path / "in")
    out = G81._run_v6(tmp_path, "o", G81._v6_context(in_dir), in_dir)
    restore = G81._snapshot(out)
    _forge_stage3(out, design_mutate=lambda d: d["bank"].update(dtype="float32"))
    v = IO.validate_provenance(out)
    assert "후보_재유도" in v["fail"] and "bank profile" in v["checks"]["후보_재유도"], v["checks"].get("후보_재유도")
    restore()
    _forge_stage3(out, env_mutate=lambda e: e["bank"].update(generator="philox"))
    v = IO.validate_provenance(out)
    assert "stage3_planned_envelope" in v["fail"] and "bank profile" in v["checks"]["stage3_planned_envelope"], \
        v["checks"].get("stage3_planned_envelope")
    restore()
    v0 = IO.validate_provenance(out)
    assert G81._fails(v0) == [], v0["fail"]


# ═════════════════════════════════════════════════════════════════════════════
# N3 선언 세대 연결
# ═════════════════════════════════════════════════════════════════════════════
def test_g82_n3_00_a_v6_run_links_sig_plan_record_and_row_generations(tmp_path):
    """양성: sig 6 · 계획 v6 · record v6 · 행 v6 — 새 검사가 있고 통과."""
    from tests.test_fitting import _tiny_curves
    in_dir = _tiny_curves(tmp_path / "in")
    out = G81._run_v6(tmp_path, "o", G81._v6_context(in_dir), in_dir)
    v = IO.validate_provenance(out)
    assert v["checks"].get("세대_연결") == "통과", v["checks"].get("세대_연결", "검사 없음")
    assert DW.STAGE3_PROTOCOL_GENERATION == "v6"


def test_g82_n3_01_a_plan_declaring_v5_does_not_start_the_v6_path(tmp_path):
    """음성 (시작 전): 계획 protocol_generation 이 문법상 유효한 v5 — v6 실행은 시작하지 않는다 (선언 충돌)."""
    from tests.test_fitting import _tiny_curves
    in_dir = _tiny_curves(tmp_path / "in")
    ctx = G81._v6_context(in_dir)
    p5 = PV.PlannedLegV4(**{**ctx["planned"].__dict__, "protocol_generation": "v5"})
    with pytest.raises(ValueError, match="protocol_generation"):
        G81._run_v6(tmp_path, "o", {**ctx, "planned": p5}, in_dir)
    assert not (tmp_path / "o" / "fits.parquet").exists()


def test_g82_n3_02_the_validator_refuses_plan_and_record_that_agree_on_v5_under_sig6(tmp_path):
    """음성 (validator): 계획 · record 가 함께 v5 (planned_id · record_digest 재계산) — 서로는 일치하지만 sig 6 · 행 v6 와
    충돌. 한 행만 v5 인 자료도 같은 검사가 거부한다."""
    from tests.test_fitting import _tiny_curves
    in_dir = _tiny_curves(tmp_path / "in")
    out = G81._run_v6(tmp_path, "o", G81._v6_context(in_dir), in_dir)
    restore = G81._snapshot(out)
    _forge_stage3(out, env_mutate=lambda e: e.update(protocol_generation="v5"))
    rec = json.loads((out / "execution_record.json").read_text(encoding="utf-8"))
    man = yaml.safe_load((out / "manifest.yaml").read_text(encoding="utf-8"))
    assert PV.check_execution_record(rec, man["run_spec"]["stage3"]["planned_envelope"]) == [], \
        "계획 ↔ record 문자열 일치만으로는 이 충돌이 보이지 않는다"
    v = IO.validate_provenance(out)
    assert "세대_연결" in v["fail"] and "protocol_generation" in v["checks"]["세대_연결"], v["checks"].get("세대_연결")
    restore()
    fits = pd.read_parquet(out / "fits.parquet")
    fits.loc[fits.index[0], "record_generation"] = "v5"
    fits.to_parquet(out / "fits.parquet", index=False)
    _reseal_fits(out)
    v = IO.validate_provenance(out)
    assert "세대_연결" in v["fail"] and "record_generation" in v["checks"]["세대_연결"], v["checks"].get("세대_연결")
