"""92차 단계 4 (묶음 6) — 구 필드 부재 고정 · consumer × key 음성 증거 · `provider_edges_sha256` 정의 하나.

고정 표 `docs/22p_gap/STAGE3_IMPL_ROUND1_SPEC.md` §16 · 매트릭스 `docs/22p_gap/GATE92_EVIDENCE_MATRIX.md` §13 의 node.

- **결함 증거 (RED 예상)**: k03 (`run_spec.stage3` 닫힘 · 자료형) · k04 (`candidate_map.json` 닫힘 · 자료형 · 실패한 객체의
  재유도 차단 — G92-N2) · k05[9] (s3 사본 9 키: helper 투영 6 + env 직접 3 — G92-N3) · k07 (warm edge 의 run_spec edge sha ==
  승인 축 값). `AttributeError` · `TypeError` 로 떨어진 RED 는 결함 증거와 따로 센다 (시험은 실패 결과의 **이유**를 단언한다).
- **대조 (GREEN 예상)**: k00 (정상 v6 · warm · v5) · k01 (재귀 부재) · k02 (이미 닫힌 자리에 구 필드) · k06 (기존 독립 재계산
  키의 s3 단독 node) · k08–k12 (매트릭스 "보강" 행 — 이유 단언). 처음부터 GREEN 인 대조는 정상이다 — "무는가" 는 위치 변이가 증명.

자기일관 위조 도구는 재사용한다: `G82._forge_stage3` · `_reseal_fits` · `_rewrite_record` · `G85._resign` ·
`G81._rewrite_map_and_record`. native 계산은 tiny curves 의 모듈 공유 실행 (no-warm · warm · v5) 셋 · COMSOL 0.
"""
from __future__ import annotations

import copy
import hashlib
import json
import shutil
import uuid
from pathlib import Path

import pandas as pd
import pytest
import yaml

from src import fitting as F
from src import io as IO
from tests import test_gate81_stage3_wire as G81
from tests import test_gate82_residuals as G82
from tests import test_gate84_round2a as G84
from tests import test_gate85_closure_members as G85
from tests import test_gate87_round2b as G87
from tools import design_wire as DW
from tools import preserve as PV

ROOT = Path(__file__).resolve().parents[1]
OBJS = G81.OBJS
OLD = ("pairing_design_id", "inference_status")          # 구 필드 — 어느 닫힌 자리에도 나타나면 안 된다
THIRD = "zz_unlisted_key"                                 # 이름과 무관한 임의 제3 키 (deny-list 가 아니라 닫힌 집합인지)
HEX64 = "ab" * 32
S3_DERIVED = "stage3_축_유도"                             # k05 의 새 검사 이름 (사본 9 키 ↔ envelope)


# ─────────────────────────────────────────────────────────────────────────────
# 도구
# ─────────────────────────────────────────────────────────────────────────────
def _smoke_dir(tag: str) -> Path:
    """`run_fit` 을 부르는 자리 — smoke namespace 안 (승인 면제 · conftest 의 gated tmp_path 와 같은 뿌리)."""
    d = ROOT / "results" / "_smoke" / "_unit" / f"g92_{tag}_{uuid.uuid4().hex[:8]}"
    d.mkdir(parents=True)
    return d


@pytest.fixture(scope="module")
def runs():
    """모듈 공유 실물 산출: no-warm v6 (`base`) · warm v6 (`warm`, provider = base) · v5 legacy (`v5`).
    각 시험은 사본을 고친다 (원본 불변)."""
    from tests.test_fitting import _BOUNDS_MIN, _obj_cfg_min, _tiny_curves
    root = _smoke_dir("mod")
    in_dir = _tiny_curves(root / "in")
    base = G81._run_v6(root, "base", G81._v6_context(in_dir), in_dir)
    warm = G81._run_v6(root, "warm", G81._warm_context(in_dir, base, root / "plan"), in_dir)
    v5 = root / "v5"
    F.run_fit(in_dir, v5, _obj_cfg_min(), {"aa": {"w_pocv": 1.0}}, _BOUNDS_MIN, "expanded", 2, nproc=1, adaptive=False)
    yield {"root": root, "in": in_dir, "base": base, "warm": warm, "v5": v5}
    shutil.rmtree(root, ignore_errors=True)


def _copy(src: Path, tmp_path: Path, name: str = "o") -> Path:
    dst = tmp_path / name
    shutil.copytree(src, dst, symlinks=True)
    return dst


def _man(out: Path) -> dict:
    return yaml.safe_load((out / "manifest.yaml").read_text(encoding="utf-8"))


def _edit_s3(out: Path, mutate) -> None:
    """run_spec.stage3 만 바꾸고 (계획 사슬은 손대지 않는다) run_signature 를 다시 맞춘다 — 그 키 하나만의 자기일관 위조."""
    mp = out / "manifest.yaml"
    man = _man(out)
    res = mutate(man["run_spec"]["stage3"])
    if res is not None:
        man["run_spec"]["stage3"] = res
    mp.write_text(yaml.safe_dump(man, allow_unicode=True), encoding="utf-8")
    G85._resign(out)


def _flip(h: str) -> str:
    return ("0" if h[0] != "0" else "1") + h[1:]


def _only(v: dict, check: str, *needles: str, also: tuple = ()) -> None:
    """실패 검사가 **정확히 이것 하나** (+ 명시한 `also`) · 이유에 needle (키 이름) — 다른 검사에 가려진 반례는 키별 증거가
    아니다. `also` 는 위조한 행 값을 **다른 독립 검사도 정당하게 센다**는 실측 사실이다 (그 검사의 이름까지 고정 집합으로)."""
    got = str(v["checks"].get(check, "검사 없음"))
    assert check in v["fail"], f"자기일관 위조가 {check} 를 통과했다: {got} · fail={v['fail']}"
    assert sorted(G81._fails(v)) == sorted([check, *also]), f"실패 검사 집합이 다르다: {v['fail']}"
    for n in needles:
        assert n in got, f"이유에 {n!r} 가 없다: {got}"


def _validate_no_rederive(out: Path, monkeypatch) -> tuple[dict, list]:
    """validator 를 실제 경로로 부르되 `_stage3_rederive` 호출을 기록한다 (G92-N2 — 실패한 객체를 넘기지 않는다).
    임의 `AttributeError` · `TypeError` 는 음성 PASS 가 아니다 — 여기서 그대로 올라와 node 를 error/fail 로 만든다."""
    calls: list = []
    real = IO._stage3_rederive

    def spy(*a, **k):
        calls.append(1)
        return real(*a, **k)
    monkeypatch.setattr(IO, "_stage3_rederive", spy)
    return IO.validate_provenance(out), calls


def _walk_keys(obj, path="$"):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield f"{path}.{k}", k
            yield from _walk_keys(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _walk_keys(v, f"{path}[{i}]")


def _redigest(rec: dict) -> dict:
    rec["record_digest"] = PV.digest({k: v for k, v in rec.items() if k != "record_digest"})
    return rec


# ═════════════════════════════════════════════════════════════════════════════
# k00 · k01 — 양성 · 재귀 부재 (GREEN 대조)
# ═════════════════════════════════════════════════════════════════════════════
def test_g92_k00_a_normal_v6_warm_and_v5_run_validate_unchanged(runs):
    for name in ("base", "warm"):
        v = IO.validate_provenance(runs[name])
        assert G81._fails(v) == [], (name, v["fail"])
        for k in ("stage3_schema", "stage3_planned_envelope", "execution_record", "candidate_map",
                  "candidate_ids_결속", "후보_재유도", "실현_재계산", "base_config_결속"):
            assert v["checks"][k] == "통과", (name, k, v["checks"][k])
    v5 = IO.validate_provenance(runs["v5"])
    assert G81._fails(v5) == [], v5["fail"]
    assert not any(k.startswith("stage3") for k in v5["checks"]), "v5 검사 집합에 v6 검사가 섞였다"
    assert S3_DERIVED not in v5["checks"]


def test_g92_k01_no_old_field_appears_anywhere_in_normal_v6_outputs(runs):
    for name in ("base", "warm"):
        out = runs[name]
        docs = {"manifest": _man(out),
                "record": json.loads((out / "execution_record.json").read_text(encoding="utf-8")),
                "map": json.loads((out / "candidate_map.json").read_text(encoding="utf-8"))}
        fits = pd.read_parquet(out / "fits.parquet")
        docs["fits_columns"] = {c: None for c in fits.columns}
        docs["restarts"] = [json.loads(s) for s in fits["restarts_json"]]
        for p in sorted((out / "_inputs").rglob("*.json")):
            docs[str(p.relative_to(out))] = json.loads(p.read_text(encoding="utf-8"))
        hits = [(d, path) for d, obj in docs.items() for path, k in _walk_keys(obj) if k in OLD]
        assert hits == [], (name, hits[:5])


# ═════════════════════════════════════════════════════════════════════════════
# k02 — 이미 닫힌 자리에 구 필드 (GREEN 대조 · 각 자리의 실제 검사 함수)
# ═════════════════════════════════════════════════════════════════════════════
def _edge_ok():
    return {"stage": "condition", "arm": "G_C", "consumer_objective": OBJS[1], "provider_objective": OBJS[0],
            "provider_artifact_sha256": HEX64, "solution_map_sha256": HEX64, "provider_protocol_sha256": HEX64}


def _place_rejects(place: str, field: str, runs, tmp_path) -> str:
    """자리 하나에 field 를 더하고 그 자리의 실제 검사가 낸 거부 문장을 돌려준다 (거부가 없으면 "")."""
    env = G81._planned_v4().envelope()
    if place == "design":
        try:
            DW.pairing_design_sha256({**G81._design(), field: "x"})
        except DW.WireError as e:
            return str(e)
        return ""
    if place.startswith("envelope"):
        blk = place.split(":")[1] if ":" in place else None
        if blk is None:
            env[field] = "x"
        elif blk == "stage":
            env["stages"][0][field] = "x"
        else:
            env[blk][field] = "x"
        return "; ".join(PV.check_envelope_v4(env))
    if place == "v3_axis":
        try:
            PV.leg_run_spec_v3(G87.LEG, G87._grid_axis(), G87._fit_axis(), {**PV.stage3_axis_from_envelope(env), field: "x"})
        except PV.PreserveError as e:
            return str(e)
        return ""
    if place in ("index_entry", "stage3_context"):
        e = G87._v3_entry(G87._planned())
        if place == "index_entry":
            e[field] = "x"
        else:
            e["stage3_context"][field] = "x"
        led = G87._write(tmp_path / "L.yaml", G87._doc(e))
        try:
            PV.planned_index(ledger=led)
        except PV.PreserveError as ex:
            return str(ex)
        return ""
    if place in ("record", "realized"):
        p = G81._planned_v4()
        rec = G81._record_for(p)
        (rec if place == "record" else rec["realized"])[field] = "x"
        return "; ".join(PV.check_execution_record(_redigest(rec), p.envelope()))
    if place == "restart_row":
        fits = pd.read_parquet(runs["base"] / "fits.parquet")
        row = json.loads(fits["restarts_json"].iloc[0])[0]
        assert IO._restart_ok_v6(row)
        return "" if IO._restart_ok_v6({**row, field: "x"}) else f"restart 행 거부 ({field})"
    if place == "roster":
        ents = G81._roster_entries()
        ents[0] = {**ents[0], field: "x"}
        return "; ".join(DW.check_roster(ents))
    if place == "edge":
        return "; ".join(DW.check_provider_edges([{**_edge_ok(), field: "x"}], objective_order=list(OBJS),
                                                 warm_provider_map={OBJS[0]: None, OBJS[1]: OBJS[0]}, arm="G_C"))
    raise AssertionError(place)


_PLACES = ["design", "envelope", "envelope:stage", "envelope:bank", "envelope:inputs", "envelope:roster", "v3_axis",
           "index_entry", "stage3_context", "record", "realized", "restart_row", "roster", "edge"]


@pytest.mark.parametrize("field", OLD)
@pytest.mark.parametrize("place", _PLACES)
def test_g92_k02_an_old_field_in_an_already_closed_place_is_refused(place, field, runs, tmp_path):
    why = _place_rejects(place, field, runs, tmp_path)
    assert why, f"{place} 에 구 필드 {field!r} 를 넣었는데 거부되지 않았다"


# ═════════════════════════════════════════════════════════════════════════════
# k03 — run_spec.stage3 닫힘 · 자료형 (RED 예상 · G92-N2)
# ═════════════════════════════════════════════════════════════════════════════
_K03 = {
    "old_pairing_design_id": (lambda s: s.update(pairing_design_id="x"), "pairing_design_id"),
    "old_inference_status": (lambda s: s.update(inference_status="x"), "inference_status"),
    "third_key": (lambda s: s.update(**{THIRD: 1}), THIRD),
    "missing_arm": (lambda s: s.pop("arm"), "arm"),
    "container_list": (lambda s: [s], "dict"),
    "container_null": (None, "dict"),
    "container_str": (lambda s: "stage3", "dict"),
    "type_arm_int": (lambda s: s.update(arm=1), "arm"),
    "type_budget_list": (lambda s: s.update(budget_by_objective=list(s["budget_by_objective"].values())),
                         "budget_by_objective"),
    "type_bank_version_null": (lambda s: s.update(bank_version=None), "bank_version"),
    "type_closure_keys_str": (lambda s: s.update(base_config_closure_keys=s["base_config_closure_keys"][0]),
                              "base_config_closure_keys"),
    "type_pairing_sha_int": (lambda s: s.update(pairing_design_sha256=123), "pairing_design_sha256"),
}


@pytest.mark.parametrize("case", list(_K03))
def test_g92_k03_run_spec_stage3_is_closed_and_typed(case, runs, tmp_path, monkeypatch):
    mutate, needle = _K03[case]
    out = _copy(runs["base"], tmp_path)
    if case == "container_null":                             # None 은 "바꾸지 않음" 과 구별되지 않으므로 직접 쓴다
        mp = out / "manifest.yaml"
        man = _man(out)
        man["run_spec"]["stage3"] = None
        mp.write_text(yaml.safe_dump(man, allow_unicode=True), encoding="utf-8")
        G85._resign(out)
    elif case.startswith("container"):
        _edit_s3(out, mutate)                                # 대체 컨테이너를 돌려준다
    else:
        _edit_s3(out, lambda s: (mutate(s), None)[1])        # 제자리 수정 (pop 의 반환값을 대체로 읽지 않게)
    v, calls = _validate_no_rederive(out, monkeypatch)
    got = str(v["checks"].get("stage3_schema", "검사 없음"))
    assert "stage3_schema" in v["fail"], f"stage3 위조가 stage3_schema 를 통과했다: {got}"
    assert needle in got, f"이유에 {needle!r} 가 없다: {got}"
    assert calls == [], "닫힘 · 자료형 검사에 실패한 stage3 로 후보 재유도를 불렀다"


# ═════════════════════════════════════════════════════════════════════════════
# k04 — candidate_map.json 닫힘 · 자료형 · 실패 객체 재유도 차단 (RED 예상 · G92-N2)
# ═════════════════════════════════════════════════════════════════════════════
def _write_map_doc(out: Path, doc, entries_for_record) -> None:
    """map 파일을 통째로 쓰고 record 의 map sha · n · record_digest 를 그 entries 로 다시 맞춘다 (자기일관)."""
    (out / "candidate_map.json").write_bytes(PV.canonical_bytes(doc))
    if entries_for_record is None:
        return
    G82._rewrite_record(out, lambda r: r["realized"].update(candidate_map_sha256=PV.digest(entries_for_record),
                                                             n_candidates=len(entries_for_record)))


def _top(mutate):
    def go(out):
        cm = json.loads((out / "candidate_map.json").read_text(encoding="utf-8"))
        doc = mutate(cm)
        ents = doc.get("entries") if isinstance(doc, dict) and isinstance(doc.get("entries"), list) else \
            (doc if isinstance(doc, list) else None)
        _write_map_doc(out, doc, ents)
    return go


def _ent(mutate):
    return lambda out: G81._rewrite_map_and_record(out, mutate)


def _first(ents, pred):
    return next(m for m in ents if pred(m))


_K04 = {
    "top_old_pairing_design_id": (_top(lambda c: {**c, "pairing_design_id": "x"}), ("pairing_design_id",)),
    "top_old_inference_status": (_top(lambda c: {**c, "inference_status": "x"}), ("inference_status",)),
    "top_third_key": (_top(lambda c: {**c, THIRD: 1}), (THIRD,)),
    "top_missing_schema": (_top(lambda c: {"entries": c["entries"]}), ("schema",)),
    "top_entries_not_list": (_top(lambda c: {**c, "entries": {"0": c["entries"][0]}}), ("entries",)),
    "container_list": (_top(lambda c: c["entries"]), ("dict",)),
    "container_null": (_top(lambda c: None), ("dict",)),
    "container_str": (_top(lambda c: "candidate-map/v1"), ("dict",)),
    "entry_old_pairing_design_id": (_ent(lambda es: es[0].update(pairing_design_id="x")), ("entries[", "pairing_design_id")),
    "entry_old_inference_status": (_ent(lambda es: es[0].update(inference_status="x")), ("entries[", "inference_status")),
    "entry_third_key": (_ent(lambda es: es[0].update(**{THIRD: 1})), ("entries[", THIRD)),
    "entry_missing_x0": (_ent(lambda es: es[0].pop("x0_sha256")), ("entries[", "x0_sha256")),
    "entry_not_dict": (_ent(lambda es: es.__setitem__(0, 7)), ("entries[", "dict")),
    "entry_i_bool": (_ent(lambda es: _first(es, lambda m: m["i"] == 1).update(i=True)), ("entries[", "i")),
    "entry_i_str": (_ent(lambda es: es[0].update(i=str(es[0]["i"]))), ("entries[", "i")),
    "entry_bank_index_bool": (_ent(lambda es: _first(es, lambda m: m["source"] == "random").update(
        bank_index=bool(_first(es, lambda m: m["source"] == "random")["bank_index"]))), ("entries[", "bank_index")),
    "entry_bank_index_on_base": (_ent(lambda es: _first(es, lambda m: m["source"] == "base_init").update(bank_index=0)),
                                 ("entries[", "bank_index")),
    "entry_candidate_id_int": (_ent(lambda es: es[0].update(candidate_id=0)), ("entries[", "candidate_id")),
    "entry_x0_int": (_ent(lambda es: es[0].update(x0_sha256=0)), ("entries[", "x0_sha256")),
}


@pytest.mark.parametrize("case", list(_K04))
def test_g92_k04_candidate_map_is_closed_and_typed(case, runs, tmp_path, monkeypatch):
    forge, needles = _K04[case]
    out = _copy(runs["base"], tmp_path)
    forge(out)
    v, calls = _validate_no_rederive(out, monkeypatch)
    got = str(v["checks"].get("candidate_map", "검사 없음"))
    assert "candidate_map" in v["fail"], f"candidate_map 위조가 통과했다: {got}"
    for n in needles:
        assert n in got, f"이유에 {n!r} 가 없다: {got}"
    assert calls == [], "닫힘 · 자료형 검사에 실패한 candidate_map 으로 후보 재유도를 불렀다"


def test_g92_k04_env_a_failed_planned_envelope_is_not_passed_to_the_rederivation(runs, tmp_path, monkeypatch):
    """`stage3_planned_envelope` 가 실패한 뒤에도 그 env 로 재유도를 계속 부르던 경로 (io.py 재유도 호출) — 차단."""
    out = _copy(runs["base"], tmp_path)
    G82._forge_stage3(out, env_mutate=lambda e: e["bank"].update(generator="philox"))
    G85._resign(out)
    v, calls = _validate_no_rederive(out, monkeypatch)
    assert "stage3_planned_envelope" in v["fail"], v["fail"]
    assert calls == [], "유효하지 않은 계획 envelope 로 후보 재유도를 불렀다"
    assert "후보_재유도" in v["fail"], "재유도를 막았으면 그 검사는 통과가 아니라 실패로 남아야 한다"


# ═════════════════════════════════════════════════════════════════════════════
# k05 — s3 사본 9 키 ↔ envelope (RED 예상 · G92-N3: helper 투영 6 + env 직접 3)
# ═════════════════════════════════════════════════════════════════════════════
def _other_mode(m: str) -> str:
    return sorted(x for x in PV.candidate_modes() if x != m)[0]


_K05 = {
    # helper 투영 (`stage3_axis_from_envelope` 의 같은 이름 값)
    "parameter_order_sha256": lambda s: s.update(parameter_order_sha256=_flip(s["parameter_order_sha256"])),
    "roster_sha256": lambda s: s.update(roster_sha256=_flip(s["roster_sha256"])),
    "provider_edges_sha256": lambda s: s.update(provider_edges_sha256=_flip(s["provider_edges_sha256"])),
    "arm": lambda s: s.update(arm="G_C" if s["arm"] != "G_C" else "G_A"),
    "stage": lambda s: s.update(stage="p_ini"),
    "candidate_mode": lambda s: s.update(candidate_mode=_other_mode(s["candidate_mode"])),
    # env 직접
    "bank_version": lambda s: s.update(bank_version="v6.1"),
    "budget_by_objective": lambda s: s.update(budget_by_objective={k: v + 1 for k, v in s["budget_by_objective"].items()}),
    "warm_provider_map": lambda s: s.update(warm_provider_map={OBJS[0]: None, OBJS[1]: OBJS[0]}),
}


@pytest.mark.parametrize("key", list(_K05))
def test_g92_k05_a_copied_stage3_key_must_equal_the_envelope_value(key, runs, tmp_path):
    out = _copy(runs["base"], tmp_path)
    _edit_s3(out, _K05[key])
    _only(IO.validate_provenance(out), S3_DERIVED, key)


# ═════════════════════════════════════════════════════════════════════════════
# k06 — 기존 독립 재계산 키의 s3 단독 node (GREEN 대조 · 이 다섯은 새 루프가 비교하지 않는다)
# ═════════════════════════════════════════════════════════════════════════════
_K06 = {
    "planned_id": (lambda s: s.update(planned_id=_flip(s["planned_id"])), "stage3_planned_envelope", "planned_id"),
    "pairing_design_sha256": (lambda s: s.update(pairing_design_sha256=_flip(s["pairing_design_sha256"])),
                              "후보_재유도", "pairing_design"),
    "exact_bounds_sha256": (lambda s: s.update(exact_bounds_sha256=_flip(s["exact_bounds_sha256"])),
                            "후보_재유도", "exact_bounds_sha256"),
    "base_config_closure_sha256": (lambda s: s.update(base_config_closure_sha256=_flip(s["base_config_closure_sha256"])),
                                   "base_config_결속", "base_config_closure_sha256"),
    "base_config_closure_keys": (lambda s: s.update(base_config_closure_keys=[]), "base_config_결속",
                                 "base_config_closure_keys"),
}


@pytest.mark.parametrize("key", list(_K06))
def test_g92_k06_an_independently_recomputed_key_forged_alone_is_refused_by_its_own_check(key, runs, tmp_path):
    mutate, check, needle = _K06[key]
    out = _copy(runs["base"], tmp_path)
    _edit_s3(out, mutate)
    _only(IO.validate_provenance(out), check, needle)


# ═════════════════════════════════════════════════════════════════════════════
# k07 — provider_edges_sha256 정의 하나 (RED 예상 · warm edge 계획)
# ═════════════════════════════════════════════════════════════════════════════
def test_g92_k07_the_run_spec_edge_sha_of_a_warm_plan_is_the_approved_axis_value(runs):
    s3 = _man(runs["warm"])["run_spec"]["stage3"]
    env = s3["planned_envelope"]
    assert env["provider_edges"], "warm 계획이 아니다 — 빈 edge 는 두 정의가 우연히 같다"
    want = PV.stage3_axis_from_envelope(env)["provider_edges_sha256"]
    assert want == PV.digest(env["provider_edges"])
    # 메시지에 digest 를 넣지 않는다 — provider fits 바이트가 실행마다 달라 변이 증인이 결정적이지 않다 (G67-T1-b)
    assert s3["provider_edges_sha256"] == want, "writer 의 edge sha 가 승인 축 (canonical digest · stage3_axis_from_envelope) 과 다르다"


# ═════════════════════════════════════════════════════════════════════════════
# k08 — C3 계획 index: 축의 나머지 키 (GREEN 대조 · 이유에 키 이름)
# ═════════════════════════════════════════════════════════════════════════════
_K08 = {
    "pairing_design_sha256": (lambda a: a.update(pairing_design_sha256=_flip(a["pairing_design_sha256"])),
                              "pairing_design_sha256"),
    "parameter_order_sha256": (lambda a: a.update(parameter_order_sha256=_flip(a["parameter_order_sha256"])),
                               "parameter_order_sha256"),
    "bank.generator": (lambda a: a["bank"].update(generator="philox"), "bank"),
    "bank.version": (lambda a: a["bank"].update(version="v6.1"), "bank"),
    "bank.length": (lambda a: a["bank"].update(length=a["bank"]["length"] + 1), "bank"),
    "bank.n_params": (lambda a: a["bank"].update(n_params=a["bank"]["n_params"] + 1), "bank"),
    "bank.exact_bounds_sha256": (lambda a: a["bank"].update(exact_bounds_sha256=_flip(a["bank"]["exact_bounds_sha256"])),
                                 "bank"),
    "stage": (lambda a: a.update(stage="p_ini"), "stage"),
}


@pytest.mark.parametrize("key", list(_K08))
def test_g92_k08_a_plan_index_axis_key_not_derived_from_the_envelope_is_refused(key, tmp_path):
    mutate, needle = _K08[key]
    e = G87._v3_entry(G87._planned())
    mutate(e["run_spec"]["stage3"])
    G87._reseal(e)
    led = G87._write(tmp_path / "L.yaml", G87._doc(e))
    with pytest.raises(PV.PreserveError) as ei:
        PV.planned_index(ledger=led)
    msg = str(ei.value)
    assert "planned_envelope 에서 유도한 값과 다르다" in msg and needle in msg, msg


# ═════════════════════════════════════════════════════════════════════════════
# k09 — 단위 수준 (GREEN 대조): C1 envelope · C2 record (record_digest 재계산) · C4 진입점 · C11 roster/edge
# ═════════════════════════════════════════════════════════════════════════════
def _env_with(mutate) -> dict:
    env = G81._planned_v4(stages=G81._stages(budget=3)).envelope()
    mutate(env)
    return env


_K09_C1 = {
    "bank_length": (lambda e: e["bank"].update(length=1), "random prefix"),
    "budget_keys": (lambda e: e["stages"][0]["budget_by_objective"].pop(OBJS[1]), "budget_by_objective"),
    "warm_map_domain": (lambda e: e["stages"][0]["warm_provider_map"].update({OBJS[1]: "zz"}), "warm_provider_map"),
    "stage_p_ini": (lambda e: e["stages"][0].update(stage="p_ini"), "p_ini"),
    "fmt-pairing_design_sha256": (lambda e: e.update(pairing_design_sha256="x"), "pairing_design_sha256"),
    "fmt-parameter_order_sha256": (lambda e: e.update(parameter_order_sha256="x"), "parameter_order_sha256"),
    "fmt-exact_bounds_sha256": (lambda e: e["bank"].update(exact_bounds_sha256="x"), "exact_bounds_sha256"),
    "fmt-curves_sha256": (lambda e: e["inputs"].update(curves_sha256="x"), "curves_sha256"),
    "fmt-source_digest": (lambda e: e.update(source_digest="x"), "source_digest"),
    "fmt-protocol_generation": (lambda e: e.update(protocol_generation="v 6"), "protocol_generation"),
}


@pytest.mark.parametrize("case", list(_K09_C1))
def test_g92_k09_c1_envelope_checks_name_the_key(case):
    mutate, needle = _K09_C1[case]
    bad = PV.check_envelope_v4(_env_with(mutate))
    assert any(needle in b for b in bad), bad


def _c2_case(mutate):
    p = G81._planned_v4(stages=G81._stages(budget=3))
    rec = G81._record_for(p)
    assert PV.check_execution_record(rec, p.envelope()) == []
    mutate(rec)
    return PV.check_execution_record(_redigest(rec), p.envelope())


def _bo(rec, obj=OBJS[0]):
    return rec["realized"]["by_objective"][obj]


_K09_C2 = {
    "leg_id": (lambda r: r.update(leg_id="someone_else"), "leg_id"),
    "source_digest": (lambda r: r.update(source_digest="0" * 16), "source_digest"),
    "protocol_generation": (lambda r: r.update(protocol_generation="v5"), "protocol_generation"),
    "total": (lambda r: _bo(r).update(not_attempted=_bo(r)["not_attempted"] + 1), "계획 총합"),
    "source_le_plan": (lambda r: _bo(r)["counts_by_source"].update(
        warm=1, base_init=_bo(r)["counts_by_source"]["base_init"] - 1), "실현 warm"),
    "prefix": (lambda r: _bo(r).update(random_bank_prefix_len=_bo(r)["random_bank_prefix_len"] + 1),
               "random_bank_prefix_len"),
    "n_obs": (lambda r: r["realized"].update(n_obs_observed=r["realized"]["n_obs_observed"] + 1), "n_obs_observed"),
    "arith-attempted": (lambda r: _bo(r).update(failed=1, not_attempted=_bo(r)["not_attempted"]), "attempted"),
    "arith-source_sum": (lambda r: _bo(r)["counts_by_source"].update(
        base_init=_bo(r)["counts_by_source"]["base_init"] - 1), "counts_by_source 합"),
}


@pytest.mark.parametrize("case", list(_K09_C2))
def test_g92_k09_c2_record_checks_name_the_key_with_a_consistent_record_digest(case):
    mutate, needle = _K09_C2[case]
    bad = _c2_case(mutate)
    assert not any("record_digest" in b for b in bad), f"record_digest 마스킹: {bad}"
    assert any(needle in b for b in bad), bad


def test_g92_k09_c4_parameter_order_sha_of_the_design_file_is_compared(tmp_path):
    from tests.test_fitting import _tiny_curves
    ctx0 = G87._relabel(G81._v6_context(_tiny_curves(tmp_path / "in")))
    p = ctx0["planned"]
    p2 = PV.PlannedLegV4(**{**p.__dict__, "parameter_order_sha256": _flip(p.parameter_order_sha256)})
    root, led, _ = G87._entry_with_design(tmp_path, {**ctx0, "planned": p2})
    with pytest.raises(PV.PreserveError) as ei:
        F.stage3_context_from_plan(G87.LEG, ledger=led, repo_root=root)
    assert "parameter_order_sha256" in str(ei.value), str(ei.value)


def test_g92_k09_c4_an_unknown_leg_is_refused_with_its_reason(tmp_path):
    led = G87._write(tmp_path / "L.yaml", G87._doc(G87._v3_entry(G87._planned())))
    with pytest.raises(PV.PreserveError) as ei:
        F.stage3_context_from_plan("no_such_leg", ledger=led, repo_root=tmp_path)
    assert "계획 index 에 없는 다리" in str(ei.value), str(ei.value)


def _roster_case(mutate):
    ents = copy.deepcopy(G81._roster_entries())
    assert DW.check_roster(ents) == []
    mutate(ents)
    return DW.check_roster(ents)


def _edge_case(edges=None, wm=None, arm="G_C"):
    wm = wm if wm is not None else {OBJS[0]: None, OBJS[1]: OBJS[0]}
    edges = edges if edges is not None else [_edge_ok()]
    return DW.check_provider_edges(edges, objective_order=list(OBJS), warm_provider_map=wm, arm=arm)


_K09_C11 = {
    "objective_in_key": (lambda: _roster_case(lambda es: es[0]["obs_key"].update(objective=OBJS[0])), "objective"),
    "dup_obs_key": (lambda: _roster_case(lambda es: es.__setitem__(1, {**es[0], "cond_id": "cond_x"})), "obs_key 중복"),
    "cond_collision": (lambda: _roster_case(lambda es: es[1].update(cond_id=es[0]["cond_id"])), "충돌"),
    "pg_mismatch": (lambda: _roster_case(lambda es: es[0].update(pair_group_id=_flip(es[0]["pair_group_id"]))),
                    "pair_group_id 가 obs_key"),
    "warm_off_provider": (lambda: _edge_case(edges=[{**_edge_ok(), "arm": "G_A"}], arm="G_A"), "condition warm 이 꺼져"),
    "order": (lambda: _edge_case(edges=[], wm={OBJS[0]: OBJS[1], OBJS[1]: None}), "앞서지 않는다"),
    "edge_stage": (lambda: _edge_case(edges=[{**_edge_ok(), "stage": "p_ini"}]), "p_ini"),
    "edge_arm": (lambda: _edge_case(edges=[{**_edge_ok(), "arm": "G_A"}]), "arm 'G_A'"),
    "edge_consumer": (lambda: _edge_case(edges=[_edge_ok(), {**_edge_ok(), "consumer_objective": "zz"}]),
                      "objective_order 에 없다"),
    "edge_vs_map": (lambda: _edge_case(edges=[{**_edge_ok(), "provider_objective": OBJS[1]}]), "warm_provider_map["),
    "dup_edge": (lambda: _edge_case(edges=[_edge_ok(), _edge_ok()]), "중복"),
    "missing_edge": (lambda: _edge_case(edges=[]), "edge 가 없는 consumer"),
}


@pytest.mark.parametrize("case", list(_K09_C11))
def test_g92_k09_c11_roster_and_edge_checks_name_the_reason(case):
    make, needle = _K09_C11[case]
    bad = make()
    assert any(needle in b for b in bad), bad


# ═════════════════════════════════════════════════════════════════════════════
# k10 — 시작 전 (GREEN 대조): C5 `_prepare_stage3` · C8 `_assert_fit_authorized` — sentinel 0 · fits 미생성
# ═════════════════════════════════════════════════════════════════════════════
def _ctx_with(in_dir, **over):
    ctx = G81._v6_context(in_dir)
    p = ctx["planned"]
    fields = {**p.__dict__}
    for k, f in over.items():
        fields[k] = f(fields[k])
    return {**ctx, "planned": PV.PlannedLegV4(**fields)}


def _bank(**kw):
    return lambda b: {**b, **kw}


_K10_C5 = {
    "objective_order": (None, "objectives 순서"),
    "parameter_order_sha256": ({"parameter_order_sha256": _flip}, "parameter_order"),
    "n_params": ({"bank": lambda b: {**b, "n_params": b["n_params"] + 1}}, "n_params"),
    "exact_bounds": ({"bank": lambda b: {**b, "exact_bounds_sha256": _flip(b["exact_bounds_sha256"])}},
                     "exact_bounds_sha256"),
    "curves_sha256": ({"inputs": lambda i: {**i, "curves_sha256": _flip(i["curves_sha256"])}}, "curves_sha256"),
}


@pytest.mark.parametrize("case", list(_K10_C5))
def test_g92_k10_c5_prepare_stage3_refuses_before_any_fitting(case, runs, monkeypatch):
    from tests.test_fitting import _BOUNDS_MIN, _obj_cfg_min
    over, needle = _K10_C5[case]
    smk = _smoke_dir(f"k10_{case}")
    try:
        calls = G84._sentinel(monkeypatch)
        out = smk / "o"
        if over is None:
            ctx = G81._v6_context(runs["in"])
            rev = {OBJS[1]: G81._OBJ_W[OBJS[1]], OBJS[0]: G81._OBJ_W[OBJS[0]]}
            with pytest.raises((ValueError, RuntimeError)) as ei:
                F.run_fit(runs["in"], out, _obj_cfg_min(), rev, _BOUNDS_MIN, "expanded", 2, nproc=1,
                          adaptive=False, warm_start=False, stage3=ctx)
        else:
            ctx = _ctx_with(runs["in"], **over)
            with pytest.raises((ValueError, RuntimeError)) as ei:
                G84._run(smk, "o", ctx, runs["in"])
        assert needle in str(ei.value), str(ei.value)
        assert calls == [], "거부가 첫 수치 작업 뒤다"
        assert not (out / "fits.parquet").exists()
    finally:
        shutil.rmtree(smk, ignore_errors=True)


def test_g92_k10_c8_another_self_consistent_plan_is_not_the_approved_run_spec(tmp_path, monkeypatch):
    """C8 대표 node — envelope 의 어떤 키도 planned_id 로 접히므로 키별 독립 node 는 원리상 없다 (§16-2 C8)."""
    out = G87._scratch("g92_k10_c8")
    led = G87._isolated_authority(monkeypatch, out)
    in_dir, ctx, live, ind = G87._live_pair(tmp_path, out)
    p = ctx["planned"]
    spec = PV.leg_run_spec_v3(G87.LEG, G87._grid_for(live), dict(live, in_digest=ind), G87._axis(p.envelope()))
    G87._write(led, G87._doc(G87._entry(spec, src=G87.SRC, envelope=p.envelope(),
                                        context={"design": G87.DESIGN_REL, "provider_runs": {}})))
    other = G87._relabel(G81._v6_context(in_dir, budget=3))
    assert other["planned"].planned_id() != p.planned_id()
    with pytest.raises(PV.PreserveError) as ei:
        F._assert_fit_authorized(live, out, leg=G87.LEG, may_open=True, stage3=other)
    assert "승인된 계획과 다르다" in str(ei.value), str(ei.value)
    assert PV.planned_index(ledger=led)[G87.LEG]["status"] == "planned"


def test_g92_k10_c8_a_context_without_a_planned_leg_is_refused(tmp_path, monkeypatch):
    out = G87._scratch("g92_k10_c8n")
    led = G87._isolated_authority(monkeypatch, out)
    in_dir, ctx, live, ind = G87._live_pair(tmp_path, out)
    p = ctx["planned"]
    spec = PV.leg_run_spec_v3(G87.LEG, G87._grid_for(live), dict(live, in_digest=ind), G87._axis(p.envelope()))
    G87._write(led, G87._doc(G87._entry(spec, src=G87.SRC, envelope=p.envelope(),
                                        context={"design": G87.DESIGN_REL, "provider_runs": {}})))
    with pytest.raises(PV.PreserveError) as ei:
        F._assert_fit_authorized(live, out, leg=G87.LEG, may_open=True, stage3={**ctx, "planned": None})
    assert "PlannedLegV4 가 없다" in str(ei.value), str(ei.value)


# ═════════════════════════════════════════════════════════════════════════════
# k11 — C6 `provider_x0` header (GREEN 대조 · edge 의 solution_map_sha256 은 위조한 바이트로 다시 맞춘다)
# ═════════════════════════════════════════════════════════════════════════════
_K11 = {
    "schema": (lambda h: h.update(schema="solution-map/v0"), "schema"),
    "provider_objective": (lambda h: h.update(provider_objective=OBJS[1]), "provider_objective"),
    "provider_artifact_sha256": (lambda h: h.update(provider_artifact_sha256=_flip(h["provider_artifact_sha256"])),
                                 "provider_artifact_sha256"),
    "provider_protocol_sha256": (lambda h: h.update(provider_protocol_sha256=_flip(h["provider_protocol_sha256"])),
                                 "provider_protocol_sha256"),
    "parameter_order": (lambda h: h.update(parameter_order=list(reversed(h["parameter_order"]))), "parameter_order"),
}


@pytest.mark.parametrize("key", list(_K11))
def test_g92_k11_c6_a_forged_map_header_field_is_refused_by_name(key, tmp_path):
    mutate, needle = _K11[key]
    prov = G81._provider_fits(tmp_path / "prov", OBJS[0], {"c1": [1.0, 0.0, 1.0, 0.0]})
    mp = tmp_path / "m.json"
    F.make_solution_map(prov, OBJS[0], mp)
    edge = G81._edge(prov, mp)
    kw = dict(cond_id="c1", lb=G81.LB, ub=G81.UB, parameter_order=G81.ORDER)
    F.provider_x0(mp, edge=edge, **kw)                              # 양성 — 위조 전에는 통과
    doc = json.loads(mp.read_text(encoding="utf-8"))
    mutate(doc["header"])
    mp.write_text(json.dumps(doc, sort_keys=True), encoding="utf-8")
    edge2 = {**edge, "solution_map_sha256": hashlib.sha256(mp.read_bytes()).hexdigest()}
    with pytest.raises(ValueError) as ei:
        F.provider_x0(mp, edge=edge2, **kw)
    assert needle in str(ei.value) and "바이트 sha" not in str(ei.value), str(ei.value)


# ═════════════════════════════════════════════════════════════════════════════
# k12 — C7 행 단위 재유도 (GREEN 대조 · 행만 고치고 fits 봉인을 다시 맞춘다)
# ═════════════════════════════════════════════════════════════════════════════
def _fits_edit(out: Path, mutate) -> None:
    fits = pd.read_parquet(out / "fits.parquet")
    mutate(fits)
    fits.to_parquet(out / "fits.parquet", index=False)
    G82._reseal_fits(out)


def _restart_bank(fits):
    for idx, s in fits["restarts_json"].items():
        rows = json.loads(s)
        for r in rows:
            if r["source"] == "random":
                r["bank_index"] = r["bank_index"] + 1
                fits.at[idx, "restarts_json"] = json.dumps(rows)
                return
    raise AssertionError("random restart 행이 없다")


def _orphan(es):
    es.append({**es[0], "cond_id": "zz_orphan_cond"})


def _touch_map(out):
    p = out / "_inputs" / "provider_maps" / f"{OBJS[1]}.solution_map.json"
    p.write_bytes(p.read_bytes() + b" ")


_K12 = {
    "pair_group_id": ("base", lambda o: _fits_edit(o, lambda f: f.__setitem__(
        "pair_group_id", [_flip(x) if i == 0 else x for i, x in enumerate(f["pair_group_id"])])),
        "후보_재유도", "pair_group_id"),
    "bank_id": ("base", lambda o: _fits_edit(o, lambda f: f.__setitem__(
        "bank_id", [_flip(x) if i == 0 else x for i, x in enumerate(f["bank_id"])])), "후보_재유도", "bank_id"),
    "warm_provider_objective": ("warm", lambda o: _fits_edit(o, lambda f: f.__setitem__(
        "warm_provider_objective", ["" for _ in f["warm_provider_objective"]])), "후보_재유도", "warm_provider_objective",
        ("실현_재계산",)),       # provider_consumed 를 행의 warm_provider_objective 에서 다시 센다 (C7-r11 · 독립)
    "restart_row": ("base", lambda o: _fits_edit(o, _restart_bank), "후보_재유도", "restart 행",
                    ("실현_재계산",)),   # random_bank_prefix_len 을 행의 bank_index 에서 다시 센다 (C7-r11 · 독립)
    "warm_started": ("base", lambda o: _fits_edit(o, lambda f: f.__setitem__(
        "warm_started", [True if i == 0 else x for i, x in enumerate(f["warm_started"])])), "후보_재유도", "warm_started"),
    "provider_map_copy": ("warm", _touch_map, "후보_재유도", "provider map 사본"),
    "orphan_map_key": ("base", lambda o: G81._rewrite_map_and_record(o, _orphan), "후보_재유도", "fits 행이 없는"),
    "n_candidates": ("base", lambda o: G82._rewrite_record(o, lambda r: r["realized"].update(
        n_candidates=r["realized"]["n_candidates"] + 1)), "실현_재계산", "n_candidates"),
}


@pytest.mark.parametrize("key", list(_K12))
def test_g92_k12_c7_a_row_level_forgery_is_refused_by_its_own_check(key, runs, tmp_path):
    which, forge, check, needle, *also = _K12[key]
    out = _copy(runs[which], tmp_path)
    forge(out)
    _only(IO.validate_provenance(out), check, needle, also=tuple(also[0]) if also else ())
