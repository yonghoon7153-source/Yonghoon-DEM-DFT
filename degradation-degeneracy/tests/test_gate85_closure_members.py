"""85차 G85-N1 — 사후 base-config closure **구성원** 결속 (고정 표 `STAGE3_IMPL_ROUND1_SPEC.md` §12).

84차 2a 의 validator `base_config_결속` 은 봉인 스냅샷을 다시 해시하지만, **어느 파일이 closure 구성원인지**는
검사 대상 `run_spec.stage3.base_config_closure_keys` 를 그대로 믿었다. 그래서 스냅샷 · 입력 봉인은 그대로 둔 채
키에서 부모를 빼고 계획 · run_spec 의 두 digest 를 leaf-only 값으로 **함께** 바꾸면 두 동등 비교가 모두 성립했다
(85차 리뷰어 `CLOSURE_COUNTERMODEL.json`). 요청문 §6-f 의 "위조하면 재계산이 달라져 실패" 는 digest 를 고정했을
때만 맞았다.

여기서는 실제 leaf → parent (`configs/grid_coarse.yaml` extends `base.yaml`) v6 실행을 만들고, 자기일관 위조가
**다른 검사가 아니라 이 검사 하나**에서 거부되는지 잰다 (m01–m04). 구성원 유도의 경계 (순환 · 봉인 없는 부모 ·
밖 경로 …) 는 합성 스냅샷으로 직접 잰다 (m05). native 계산 0 · COMSOL 0.
"""
from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

import pytest
import yaml

from src import fitting as F
from src import io as IO
from tests import test_gate81_stage3_wire as G81
from tests import test_gate82_residuals as G82
from tests import test_gate84_round2a as G84
from tools import preserve as PV

ROOT = Path(__file__).resolve().parents[1]
PARENT = "configs/base.yaml"
LEAF = "configs/grid_coarse.yaml"      # 실제 저장소 config · `extends: base.yaml`
CHECK = "base_config_결속"


# ─────────────────────────────────────────────────────────────────────────────
# 도구
# ─────────────────────────────────────────────────────────────────────────────
def _leaf_run(tmp_path, name="o"):
    """leaf → parent 로 도는 유효한 v6 실행 (계획 digest = 실제 closure hex64)."""
    from tests.test_fitting import _tiny_curves
    in_dir = _tiny_curves(tmp_path / "in")
    ctx = G81._v6_context(in_dir)
    p = ctx["planned"]
    inputs = {**p.inputs, "base_config_digest": F.config_closure_sha256(LEAF)}
    ctx["planned"] = PV.PlannedLegV4(**{**p.__dict__, "inputs": inputs})
    return G84._run(tmp_path, name, ctx, in_dir, base_config=LEAF)


def _closure_of(keys) -> str:
    """주어진 논리 키들의 (저장소 바이트 = 봉인 스냅샷 바이트) closure hex64 — 위조자가 계산하는 값."""
    return F.closure_sha256_from_parts({k: hashlib.sha256((ROOT / k).read_bytes()).hexdigest() for k in keys})


def _forge_members(out: Path, keys: list, digest: str | None) -> None:
    """스냅샷 · 입력 봉인은 **그대로** 두고, 키 목록과 (주면) 계획 · run_spec 의 두 digest 를 함께 바꾼다.
    계획 사슬 (planned_id · record) 은 `G82._forge_stage3` 가 다시 맞춘다 — 자기일관 위조."""
    mp = out / "manifest.yaml"
    man = yaml.safe_load(mp.read_text(encoding="utf-8"))
    s3 = man["run_spec"]["stage3"]
    s3["base_config_closure_keys"] = list(keys)
    if digest is not None:
        s3["base_config_closure_sha256"] = digest
    mp.write_text(yaml.safe_dump(man, allow_unicode=True), encoding="utf-8")
    if digest is not None:
        G82._forge_stage3(out, env_mutate=lambda e: e["inputs"].update(base_config_digest=digest))
    _resign(out)


def _resign(out: Path) -> None:
    """run_spec 을 바꾼 위조자는 run_signature 도 다시 만든다 — manifest 의 서명 · fits 행의 `run_sig` 열 · fits 봉인을
    실물에서 다시 맞춘다 (서명 정의는 `src/fitting.py` 와 같다: sha1(json(run_spec, sort_keys))[:12])."""
    import json

    import pandas as pd
    mp = out / "manifest.yaml"
    man = yaml.safe_load(mp.read_text(encoding="utf-8"))
    sig = hashlib.sha1(json.dumps(man["run_spec"], sort_keys=True, default=str).encode()).hexdigest()[:12]
    man["run_signature"] = sig
    mp.write_text(yaml.safe_dump(man, allow_unicode=True), encoding="utf-8")
    fits = pd.read_parquet(out / "fits.parquet")
    fits["run_sig"] = sig
    fits.to_parquet(out / "fits.parquet", index=False)
    G82._reseal_fits(out)


def _only_this_check_fails(out: Path, *needles: str) -> None:
    v = IO.validate_provenance(out)
    got = str(v["checks"].get(CHECK, "검사 없음"))
    assert CHECK in v["fail"], f"자기일관 위조가 {CHECK} 를 통과했다: {got}"
    assert G81._fails(v) == [CHECK], f"다른 검사에 가려졌다 — 구성원 결속 자체를 재지 못한다: {v['fail']}"
    for n in needles:
        assert n in got, f"이유에 {n!r} 가 없다: {got}"


# ═════════════════════════════════════════════════════════════════════════════
# m00 · m06 — 양성
# ═════════════════════════════════════════════════════════════════════════════
def test_g85_m00_a_real_leaf_to_parent_run_binds_both_members(tmp_path):
    out = _leaf_run(tmp_path)
    man = yaml.safe_load((out / "manifest.yaml").read_text(encoding="utf-8"))
    assert man["run_spec"]["base_config"] == LEAF
    s3 = man["run_spec"]["stage3"]
    assert sorted(s3["base_config_closure_keys"]) == [PARENT, LEAF]
    assert s3["base_config_closure_sha256"] == _closure_of([PARENT, LEAF]) == F.config_closure_sha256(LEAF)
    v = IO.validate_provenance(out)
    assert v["checks"].get(CHECK) == "통과", v["checks"].get(CHECK, "검사 없음")
    assert G81._fails(v) == [], v["fail"]


def test_g85_m06_a_relocated_run_directory_still_binds_its_members(tmp_path):
    """논리 키와 봉인 스냅샷만 쓰므로 산출 디렉터리를 옮겨도 같다 (현재 디스크 경로에 기대지 않는다)."""
    out = _leaf_run(tmp_path)
    moved = tmp_path / "moved" / "o"
    shutil.copytree(out, moved, symlinks=True)
    v = IO.validate_provenance(moved)
    assert v["checks"].get(CHECK) == "통과", v["checks"].get(CHECK, "검사 없음")


# ═════════════════════════════════════════════════════════════════════════════
# m01–m04 — 자기일관 위조 (스냅샷 · 봉인 불변 · 목록과 두 digest 를 함께)
# ═════════════════════════════════════════════════════════════════════════════
def test_g85_m01_dropping_the_parent_and_forging_both_digests_is_refused_by_the_member_check(tmp_path):
    out = _leaf_run(tmp_path)
    _forge_members(out, [LEAF], _closure_of([LEAF]))
    _only_this_check_fails(out, PARENT)


def test_g85_m02_dropping_the_leaf_and_forging_both_digests_is_refused_by_the_member_check(tmp_path):
    out = _leaf_run(tmp_path)
    _forge_members(out, [PARENT], _closure_of([PARENT]))
    _only_this_check_fails(out, LEAF)


def test_g85_m03_an_extra_sealed_member_with_forged_digests_is_refused_by_the_member_check(tmp_path):
    out = _leaf_run(tmp_path)
    man = yaml.safe_load((out / "manifest.yaml").read_text(encoding="utf-8"))
    extra = next(k for k in man["run_spec"]["sealed_inputs"] if k.endswith("/curves_manifest.yaml"))
    keys = [PARENT, LEAF, extra]
    sealed = man["run_spec"]["sealed_inputs"]
    snap = out / "_inputs" / f"{sealed[extra][:12]}_{Path(extra).name}"
    parts = {k: hashlib.sha256((ROOT / k).read_bytes()).hexdigest() for k in (PARENT, LEAF)}
    parts[extra] = hashlib.sha256(snap.read_bytes()).hexdigest()
    _forge_members(out, keys, F.closure_sha256_from_parts(parts))
    _only_this_check_fails(out, Path(extra).name)


def test_g85_m04_a_duplicated_member_key_is_refused_even_with_the_true_digests(tmp_path):
    """중복 키 — dict 로 합치면 진짜 closure 와 같은 값이 나와 통과했다. 목록은 **유일**해야 한다."""
    out = _leaf_run(tmp_path)
    _forge_members(out, [PARENT, LEAF, LEAF], None)
    _only_this_check_fails(out, "중복")


# ═════════════════════════════════════════════════════════════════════════════
# m05 — 구성원 유도의 경계 (합성 스냅샷 · 실행 없음)
# ═════════════════════════════════════════════════════════════════════════════
def _snapdir(tmp_path, docs: dict, *, unsealed=(), unsnapped=()) -> tuple:
    """{논리 키: YAML 텍스트} → (봉인 map, 스냅샷 디렉터리). `unsealed` 는 봉인 map 에서 · `unsnapped` 는 스냅샷에서 뺀다."""
    snap = tmp_path / "_inputs"
    snap.mkdir(parents=True, exist_ok=True)
    sealed = {}
    for k, text in docs.items():
        b = text.encode("utf-8")
        d = hashlib.sha256(b).hexdigest()
        if k not in unsealed:
            sealed[k] = d
        if k not in unsnapped:
            (snap / f"{d[:12]}_{Path(k).name}").write_bytes(b)
    return sealed, snap


def test_g85_m05_member_derivation_refuses_cycles_unsealed_or_missing_parents_escapes_and_bad_extends(tmp_path):
    derive = IO.base_config_closure_members

    ok_sealed, ok_snap = _snapdir(tmp_path / "ok", {"configs/p.yaml": "a: 1\n",
                                                   "configs/l.yaml": "extends: p.yaml\nb: 2\n"})
    members, problems = derive("configs/l.yaml", ok_sealed, ok_snap)
    assert (members, problems) == (["configs/l.yaml", "configs/p.yaml"], []), (members, problems)

    cases = {
        "순환": ({"configs/a.yaml": "extends: b.yaml\n", "configs/b.yaml": "extends: a.yaml\n"}, {}, "configs/a.yaml"),
        "봉인": ({"configs/p.yaml": "a: 1\n", "configs/l.yaml": "extends: p.yaml\n"},
                 {"unsealed": ("configs/p.yaml",)}, "configs/l.yaml"),
        "스냅샷": ({"configs/p.yaml": "a: 1\n", "configs/l.yaml": "extends: p.yaml\n"},
                   {"unsnapped": ("configs/p.yaml",)}, "configs/l.yaml"),
        "밖": ({"configs/l.yaml": "extends: ../../outside.yaml\n"}, {}, "configs/l.yaml"),
        "extends": ({"configs/l.yaml": "extends: [p.yaml]\n"}, {}, "configs/l.yaml"),
        "root": ({"configs/p.yaml": "a: 1\n"}, {}, "configs/absent.yaml"),
    }
    for i, (needle, (docs, kw, root)) in enumerate(cases.items()):
        sealed, snap = _snapdir(tmp_path / f"c{i}", docs, **kw)
        members, problems = derive(root, sealed, snap)
        assert problems, f"{needle}: 거부하지 않았다 (members={members})"
        assert any(needle in p for p in problems), f"{needle}: 이유가 다르다 — {problems}"
