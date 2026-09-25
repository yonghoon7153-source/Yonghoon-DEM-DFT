"""70차 게이트 (E3 · E5 · E6 · E10) — 리뷰어 반례를 그대로 옮기고, 실물 등록부·묶음을 양성 대조군으로 쓴다.

리뷰어(70차 §4)가 원본 reader·parser 에 넣어 **수용**을 실측한 것:

    E5  `_read_exec_class_at` 이 (1) `content_id`·`execution_class` 두 키만 있는 레코드,
        (2) 거기에 `sealed=[]`·`evidence=17`·`recorded_at=false`·임의 키가 붙은 레코드를 받았다.
        `resolve_execution_class` 는 `sealed` 의 truthiness 를 썼다.
    E3  `_declared_index_members` 가 비JSON index 에 `None` 을 돌려주고 호출부가 구성원 대조를
        건너뛰었다 — 실물 `payload_sha256.yaml` 은 YAML 이라 **production 묶음이 정확히 그 경로**였다.
        finalize/승격 경로는 typed 영수증을 소비하지 않았다.
    E6  시험이 운영 등록부에 synthetic canonical 을 만들 수 있고 session cleanup 이 소유권 구분 없이
        새 JSON 을 지웠다.
    E10 `test_a_smoke_run_cannot_be_promoted_to_a_canonical_report` 의 양성 경로가 ambient
        `results/grid_fit_v4` 에 의존했다.

여기의 시험은 전부 임시 원장(`ledger` fixture) 또는 conftest 가 격리한 시험 authority 아래에서 돈다.
운영 등록부·원장은 **읽기만** 한다.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

import tools.preserve as P                                      # noqa: E402

_REAL_LEDGER = REPO / "docs" / "22p_gap" / "LEG_PRESERVATION.yaml"
_REAL_REGISTRY = REPO / "docs" / "22p_gap" / "_exec_class"


# ── 공통 fixture (62차 `test_promotion_seal_62.py` 의 형태) ────────────────────
@pytest.fixture
def ledger(tmp_path, monkeypatch):
    led = tmp_path / "authority" / "LEG_PRESERVATION.yaml"
    led.parent.mkdir(parents=True)
    led.write_text("planned: []\nlegs: []\ncohorts: []\n", encoding="utf-8")
    monkeypatch.setattr(P, "canonical_ledger", lambda x=None: led)
    return led


def _grid_outputs(d: Path) -> None:
    d.mkdir(parents=True, exist_ok=True)
    (d / "curves_manifest_start.yaml").write_text("seed: 1\n", encoding="utf-8")
    (d / "curves_manifest.yaml").write_text("curves_sha256: aaaa\n", encoding="utf-8")


def _fit_finishes(d: Path) -> None:
    (d / "manifest_start.yaml").write_text("bounds: preset\n", encoding="utf-8")
    (d / "manifest.yaml").write_text("fits_sha256: first\n", encoding="utf-8")
    (d / "manifest_grid.yaml").write_text("curves_sha256: aaaa\n", encoding="utf-8")


def _commit(out: Path, led: Path, phase: str) -> None:
    cap = P.issue_execution_class(out, "L", phase, ledger=led)
    P.commit_run_outputs(cap, [out])


def _committed_run(tmp_path: Path, led: Path) -> tuple[Path, Path, str]:
    """production writer 가 등록한 canonical 산출 하나 — (run_dir, 레코드 경로, content_id)."""
    out = tmp_path / "results" / "run"
    _grid_outputs(out)
    _commit(out, led, "grid")
    _fit_finishes(out)
    _commit(out, led, "fit")
    cid = P.run_content_id(out)
    rec = P.exec_class_root_for_ledger(led) / f"{cid}.json"
    assert rec.is_file(), "writer 가 공유 등록부에 레코드를 남기지 않았다"
    return out, rec, cid


def _overwrite(rec: Path, body: dict) -> None:
    """같은 inode 에 덮어쓴다 (nlink 층을 건너뛰지 않기 위해 이름을 새로 만들지 않는다)."""
    rec.write_text(json.dumps(body, ensure_ascii=False) + "\n", encoding="utf-8")


def _promote(out: Path) -> None:
    P.assert_not_smoke_provenance([out], "보관 묶음")


# ═══════════════════════════════════════════════════════════════════════════
# E5 — typed reader
# ═══════════════════════════════════════════════════════════════════════════
def test_g70_e5_01_a_record_with_only_class_and_content_id_is_refused(tmp_path, ledger):
    """★ 리뷰어 레코드 1 — 두 키만. 원본 reader 는 이것을 canonical 로 읽었다."""
    out, rec, cid = _committed_run(tmp_path, ledger)
    _overwrite(rec, {"content_id": cid, "execution_class": P.EXEC_CLASS_CANONICAL})
    with pytest.raises(P.PreserveError) as ei:
        P._read_exec_class_at(rec, cid)
    msg = str(ei.value)
    assert "typed" in msg and "70차 E5" in msg, msg
    # 승격 sink 까지 같은 사유로 멈춘다 — "등록돼 있지 않다" 로 접지 않는다
    with pytest.raises(P.PreserveError) as ei2:
        _promote(out)
    assert "typed" in str(ei2.value) and "등록돼 있지 않다" not in str(ei2.value), str(ei2.value)


def test_g70_e5_02_wrongly_typed_fields_and_extra_keys_are_refused(tmp_path, ledger):
    """★ 리뷰어 레코드 2 — `sealed=[]`·`evidence=17`·`recorded_at=false`·임의 키."""
    out, rec, cid = _committed_run(tmp_path, ledger)
    _overwrite(rec, {"content_id": cid, "execution_class": P.EXEC_CLASS_CANONICAL,
                     "sealed": [], "evidence": 17, "recorded_at": False,
                     "anything": "goes"})
    with pytest.raises(P.PreserveError) as ei:
        P._read_exec_class_at(rec, cid)
    assert "키 집합" in str(ei.value), str(ei.value)


@pytest.mark.parametrize("field,value,why", [
    ("sealed", "yes", "bool"),
    ("sealed", 1, "bool"),
    ("sealed", [], "bool"),
    ("evidence", 17, "evidence"),
    ("evidence", "", "evidence"),
    ("recorded_at", False, "recorded_at"),
    ("recorded_at", "2026-09-24", "recorded_at"),
    ("execution_class", "canonical ", "execution_class"),
])
def test_g70_e5_03_each_field_is_typed_not_truthy(tmp_path, ledger, field, value, why):
    """★ 키 집합이 맞아도 **타입**이 틀리면 거부 — truthiness 로 읽지 않는다."""
    out, rec, cid = _committed_run(tmp_path, ledger)
    body = json.loads(rec.read_text(encoding="utf-8"))
    assert set(body) == set(P.EXEC_CLASS_RECORD_KEYS_MODERN), sorted(body)
    body[field] = value
    _overwrite(rec, body)
    with pytest.raises(P.PreserveError) as ei:
        P._read_exec_class_at(rec, cid)
    assert why in str(ei.value), str(ei.value)


def test_g70_e5_04_a_truthy_non_bool_sealed_cannot_pass_the_promotion_seal_rule(tmp_path, ledger):
    """★ `resolve_execution_class` 의 `sealed` truthiness — 봉인을 지운 뒤 `sealed: "yes"` 인
    레코드는 (a) typed reader 에서 멈춰야 하고, (b) 그 전에라도 봉인 없는 승격이 되면 안 된다."""
    out, rec, cid = _committed_run(tmp_path, ledger)
    body = json.loads(rec.read_text(encoding="utf-8"))
    body["sealed"] = "yes"
    _overwrite(rec, body)
    (out / P.RUN_SEAL_NAME).unlink()
    with pytest.raises(P.PreserveError):
        P.resolve_execution_class(out, for_promotion=True)


def test_g70_e5_05_the_writer_record_and_the_legacy_shape_are_the_two_accepted_variants(tmp_path, ledger):
    """양성 — writer 의 modern 레코드는 그대로 통과하고, 58~61차가 남긴 legacy 4키 형태도 통과한다.
    `schema` 같은 키가 하나만 더 붙어도(다른 clone 의 임의 형식) 거부."""
    out, rec, cid = _committed_run(tmp_path, ledger)
    modern = P._read_exec_class_at(rec, cid)
    assert modern["execution_class"] == P.EXEC_CLASS_CANONICAL and modern["sealed"] is True
    legacy = {"content_id": cid, "execution_class": P.EXEC_CLASS_CANONICAL,
              "evidence": "legacy 분류 (58차 P0-8): 시험", "recorded_at": "2026-09-04T07:34:51Z"}
    _overwrite(rec, legacy)
    got = P._read_exec_class_at(rec, cid)
    assert got == legacy and "sealed" not in got
    # legacy 레코드는 봉인 없는 승격을 허용한다 (62차 규칙 그대로)
    (out / P.RUN_SEAL_NAME).unlink()
    assert P.resolve_execution_class(out, for_promotion=True)["execution_class"] == "canonical"
    _overwrite(rec, {**legacy, "schema": "execution-class/v1"})
    with pytest.raises(P.PreserveError):
        P._read_exec_class_at(rec, cid)


def _tracked_registry_records() -> list[str]:
    """운영 등록부의 tracked 최상위 레코드 (저장소 상대 경로).

    git checkout 이 아닌 자리(변이 재생 sandbox 는 tree 의 **복사본**이다)에서는 `git ls-files` 가
    비므로 최상위 `*.json` 을 그대로 센다 — 70차 E6 격리 뒤 운영 최상위에는 미추적 레코드가 없다.
    """
    try:
        out = subprocess.run(["git", "ls-files", "docs/22p_gap/_exec_class"], cwd=REPO,
                             capture_output=True, text=True, check=True).stdout.split()
    except (OSError, subprocess.CalledProcessError):
        out = []
    tracked = [t for t in out if t.endswith(".json") and "/local/" not in t]
    if not tracked:
        tracked = sorted(p.relative_to(REPO).as_posix() for p in _REAL_REGISTRY.glob("*.json"))
    return tracked


def test_g70_e5_06_every_tracked_record_in_the_real_registry_is_a_typed_variant():
    """양성 대조군 (읽기 전용) — 운영 등록부의 **tracked** 레코드 전부가 두 variant 중 하나다.
    reader 를 닫으면서 과거 레코드를 다시 쓰지 않았다는 증거 (리뷰어: 과거 class 임의 재작성 금지)."""
    tracked = _tracked_registry_records()
    assert len(tracked) >= 300, len(tracked)
    variants = {"modern": 0, "legacy": 0}
    for rel in tracked:
        p = REPO / rel
        rec = json.loads(p.read_text(encoding="utf-8"))
        got = P._typed_exec_class_record(rec, p.stem, p)
        variants["modern" if "sealed" in got else "legacy"] += 1
    assert variants["modern"] > 0 and variants["legacy"] > 0, variants


def test_g70_e5_07_an_unreadable_record_is_corruption_not_absence(tmp_path, ledger):
    """★ 파일은 있는데 JSON 이 아니다 — `None`("없음") 으로 접으면 그 위에 새 판단이 얹힌다."""
    out, rec, cid = _committed_run(tmp_path, ledger)
    rec.write_text("{", encoding="utf-8")
    with pytest.raises(P.PreserveError) as ei:
        P._read_exec_class_at(rec, cid)
    assert "손상" in str(ei.value), str(ei.value)
    assert P._read_exec_class_at(rec.with_name("없는" + rec.name), cid) is None


# ═══════════════════════════════════════════════════════════════════════════
# E3 — payload index fail-closed · YAML · 구성원 sha
# ═══════════════════════════════════════════════════════════════════════════
def _bundle(root: Path, index_body: str, *, index_name="payload_sha256.yaml", tamper=None) -> dict:
    d = root / "artifacts" / "L"
    d.mkdir(parents=True, exist_ok=True)
    (d / "a.csv").write_text("a,b\n1,2\n", encoding="utf-8")
    (d / "sub").mkdir(exist_ok=True)
    (d / "sub" / "b.csv").write_text("c,d\n3,4\n", encoding="utf-8")
    idx = d / index_name
    idx.write_text(index_body, encoding="utf-8")
    if tamper:
        tamper(d)
    files = [x for x in sorted(d.rglob("*")) if x.is_file()]
    return {"bundle_uri": d.relative_to(root).as_posix(), "bundle_files": len(files),
            "payload_bytes": sum(x.stat().st_size for x in files),
            "payload_index": idx.relative_to(root).as_posix(),
            "payload_index_sha256": hashlib.sha256(idx.read_bytes()).hexdigest()}


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _yaml_index(root: Path) -> str:
    return yaml.safe_dump({"a.csv": _sha(b"a,b\n1,2\n"), "sub/b.csv": _sha(b"c,d\n3,4\n")},
                          sort_keys=True)


def test_g70_e3_01_an_index_that_enumerates_nothing_is_not_full_coverage(tmp_path):
    """★ `{}` index — 60차 reader 는 `None` 으로 대조를 건너뛰고 `[]`(통과) 를 냈다."""
    ev = _bundle(tmp_path, "{}\n", index_name="index.json")
    bad = P._verify_declared_bundle(ev, repo_root=tmp_path)
    assert bad and any("해석할 수 없다" in b and "70차 E3" in b for b in bad), bad


@pytest.mark.parametrize("body", ["not: [valid: yaml", "42\n", "- 1\n- 2\n", "a.csv: notahex\n"])
def test_g70_e3_02_unparseable_or_untyped_indexes_are_refused(tmp_path, body):
    ev = _bundle(tmp_path, body, index_name="index.yaml")
    bad = P._verify_declared_bundle(ev, repo_root=tmp_path)
    assert bad and any("해석할 수 없다" in b for b in bad), bad


def test_g70_e3_03_the_production_yaml_index_is_understood_and_binds_bytes(tmp_path):
    """양성 — `archive_bundle` 형식(YAML `경로: sha256`)은 통과하고, 같은 길이의 다른 바이트는 잡힌다."""
    ev = _bundle(tmp_path, _yaml_index(tmp_path))
    assert P._verify_declared_bundle(ev, repo_root=tmp_path) == []

    def swap(d: Path):
        (d / "a.csv").write_text("a,b\n1,3\n", encoding="utf-8")   # 같은 길이
    ev2 = _bundle(tmp_path / "t2", _yaml_index(tmp_path), tamper=swap)
    bad = P._verify_declared_bundle(ev2, repo_root=tmp_path / "t2")
    assert bad and any("바이트가 index 와 다르다" in b and "a.csv" in b for b in bad), bad


def test_g70_e3_04_the_yaml_index_must_agree_with_the_walk_both_ways(tmp_path):
    def extra(d: Path):
        (d / "extra.bin").write_bytes(b"x")
    ev = _bundle(tmp_path, _yaml_index(tmp_path), tamper=extra)
    bad = P._verify_declared_bundle(ev, repo_root=tmp_path)
    assert bad and any("index 가 모르는 구성원" in b and "extra.bin" in b for b in bad), bad
    # (`"0"*64` 는 YAML 이 정수로 읽는다 — 문자열 hex 가 되도록 글자를 섞는다)
    ev2 = _bundle(tmp_path / "t2", _yaml_index(tmp_path) + "ghost.csv: " + "ab" * 32 + "\n")
    bad2 = P._verify_declared_bundle(ev2, repo_root=tmp_path / "t2")
    assert bad2 and any("없는데 이름한 것" in b and "ghost.csv" in b for b in bad2), bad2


def test_g70_e3_05_the_list_shaped_test_index_still_names_members(tmp_path):
    """60차 fixture 형식(`{"members": [...]}`)은 이름만 열거한다 — 여전히 받되 sha 대조는 없다."""
    ev = _bundle(tmp_path, json.dumps({"members": ["a.csv", "sub/b.csv"]}) + "\n",
                 index_name="payload_index.json")
    assert P._verify_declared_bundle(ev, repo_root=tmp_path) == []


def test_g70_e3_06_the_real_paired_fixed5_v4_bundle_passes_the_closed_index_check():
    """양성 대조군 (읽기 전용) — 실물 원장의 `full_bundle` 증거가 YAML index 해석·양방향·구성원 sha
    까지 **처음으로** 통과한다 (60차까지는 이 경로가 `None` 으로 건너뛰어졌다)."""
    doc = yaml.safe_load(_REAL_LEDGER.read_text(encoding="utf-8"))
    legs = [e for e in doc["legs"] if e.get("preservation_status") == "full_bundle"]
    assert legs, "실물 원장에 full_bundle 다리가 없다"
    for e in legs:
        ev = {k: e["evidence"][k] for k in P.BUNDLE_EVIDENCE_KEYS}
        assert P._verify_declared_bundle(ev, repo_root=REPO) == [], e["leg_id"]
        declared, why = P._declared_index(REPO / ev["payload_index"])
        assert why is None and declared and all(v is not None for v in declared.values()), (
            f"{e['leg_id']}: 실물 index 가 sha 를 적지 않는다? {why}")


# ═══════════════════════════════════════════════════════════════════════════
# E3 — 검증 영수증의 typed 소비 (`attach_bundle_evidence`)
# ═══════════════════════════════════════════════════════════════════════════
_SEM = "a" * 64          # 두 summary 의 semantic digest — 생산 계약은 **같아야** 한다 (27차 P1-6)


def _production_outputs(root: Path, ev: dict, *, sem_rescored=None, sem_sealed=None,
                        source_fits=None) -> list[dict]:
    """`make_receipt._score_manifest` 가 만드는 그대로 — rescored_summary + sealed_summary 한 쌍.

    ★ 71차 E3-R — 초판 fixture 는 `rescored_summary` **하나**에 `outputs_agree=True` 를 얹었다.
      생산자(`_outputs_agree`)는 짝이 없으면 "비교 불가" 로 멈추므로 그런 영수증은 생산될 수
      없다 — 소비자가 생산 계약보다 약한 fixture 를 정답으로 삼고 있었다 (리뷰어 실측).
    """
    fits = root / ev["bundle_uri"] / "fits.parquet"
    sealed = root / ev["bundle_uri"] / "degeneracy_summary.yaml"
    return [
        {"role": "rescored_summary", "produced_from": "restored fits.parquet only",
         "source_file_sha256": source_fits or _sha(fits.read_bytes()),
         "relative_path": "_rescored_summary.yaml", "byte_size": 10, "file_sha256": "b" * 64,
         "n_rows": 3, "semantic_schema": "degeneracy-summary/v5", "canonicalizer": "score-semantic/v3",
         "semantic_view_drops": ["_채점원본"], "semantic_sha256": sem_rescored or _SEM},
        {"role": "sealed_summary", "relative_path": "degeneracy_summary.yaml",
         "byte_size": sealed.stat().st_size, "file_sha256": _sha(sealed.read_bytes()),
         "semantic_schema": "degeneracy-summary/v5", "canonicalizer": "score-semantic/v3",
         "semantic_view_drops": ["_채점원본"], "semantic_sha256": sem_sealed or _SEM},
    ]


def _receipt_core(root: Path, leg: str, ev: dict, *, validator=None, ok=True, fail=None,
                  outputs=None, mode="empty_root", conflicts=0, mismatches=0,
                  run_dir_relative=None) -> dict:
    from src.io import source_digest
    fits = root / ev["bundle_uri"] / "fits.parquet"
    return {
        "leg_id": leg,
        "bundle": {"uri": ev["bundle_uri"], "files": ev["bundle_files"], "bytes": ev["payload_bytes"],
                   "payload_index": ev["payload_index"], "payload_index_sha256": ev["payload_index_sha256"],
                   "member_rehash": "tools.archive_bundle.check", "member_mismatches": mismatches,
                   "fits_sha256": _sha(fits.read_bytes())},
        "restore": {"mode": mode, "command": "restore(...)", "files_written": ev["bundle_files"],
                    "run_dir_relative": run_dir_relative or f"results/{leg}", "conflicts": conflicts},
        "validation": {"validator": "src.io.validate_provenance", "ok": ok,
                       "fail": list(fail or []), "n_checks": 2,
                       "checks": {"a": "ok", "b": "ok"}},
        "identity": {"validator_source_digest": validator or source_digest(),
                     "src_io_sha256": "0" * 16, "src_scoring_sha256": "0" * 16,
                     "archive_bundle_sha256": "0" * 16, "make_receipt_sha256": "0" * 16,
                     "row_projection_sha256": "0" * 16, "row_projection_compute_sha256": "0" * 16},
        "outputs": outputs if outputs is not None else _production_outputs(root, ev),
        "outputs_agree": True,
    }


def _write_receipt(root: Path, leg: str, core: dict, *, extra_top=None, core_sha=None) -> str:
    rec = {"schema_version": 2, "_주의": "시험", "core_sha256": core_sha or P._receipt_core_sha256(core),
           "core": core, "stamp": {"validator_commit": "x"}}
    if extra_top:
        rec.update(extra_top)
    rp = root / "docs" / "22p_gap" / "receipts" / f"{leg}.validate.yaml"
    rp.parent.mkdir(parents=True, exist_ok=True)
    rp.write_text(yaml.safe_dump(rec, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return rp.relative_to(root).as_posix()


def _fixture_repo(tmp_path: Path, *, status="preservation_pending", with_lifecycle=True) -> tuple[Path, Path, dict]:
    """finalize 가 남긴 형태의 원장 + `fits.parquet` 이 있는 묶음 (YAML index)."""
    root = tmp_path / "repo"
    d = root / "artifacts" / "L"
    d.mkdir(parents=True)
    (d / "fits.parquet").write_bytes(b"PAR1-fits")
    (d / "manifest.yaml").write_text("fits_sha256: x\n", encoding="utf-8")
    # ★ 71차 E3-R — 실물 묶음이 가진 것: 복원 지도(어느 실행 자리로 돌아가는가)와 봉인 summary
    (d / "restore_map.yaml").write_text("run_dir: results/L\ninputs: {}\nnested: []\n", encoding="utf-8")
    (d / "degeneracy_summary.yaml").write_text("_채점원본: {canonical: true}\nn: 3\n", encoding="utf-8")
    idx = d / "payload_sha256.yaml"
    idx.write_text(yaml.safe_dump({n: _sha((d / n).read_bytes())
                                   for n in ("fits.parquet", "manifest.yaml", "restore_map.yaml",
                                             "degeneracy_summary.yaml")}), encoding="utf-8")
    files = [x for x in sorted(d.rglob("*")) if x.is_file()]
    ev = {"bundle_uri": "artifacts/L", "bundle_files": len(files),
          "payload_bytes": sum(x.stat().st_size for x in files),
          "payload_index": "artifacts/L/payload_sha256.yaml",
          "payload_index_sha256": _sha(idx.read_bytes())}
    leg_ev = {"leg_source_digest": "0123456789abcdef", "cohorts": ["gA"], "out": "results/L"}
    if with_lifecycle:
        leg_ev.update({"phases": {"grid": {}, "fit": {}}, "attempt_id": "a" * 32,
                       "run_spec_digest": "b" * 64, "attempt_verifier": "c" * 64,
                       "verifier_origin": "normal_finalize"})
    doc = {"schema_version": 4, "cohorts": [{"cohort_id": "gA", "status": "active", "legs": ["L"]}],
           "planned": [{"leg_id": "L", "cohort_id": "gA", "status": "executed"}],
           "legs": [{"leg_id": "L", "preservation_status": status, "validation_status": "unvalidated",
                     "inference_role": "diagnostic", "evidence": leg_ev}]}
    led = root / "docs" / "22p_gap" / "LEG_PRESERVATION.yaml"
    led.parent.mkdir(parents=True, exist_ok=True)
    led.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return root, led, ev


def _leg(led: Path) -> dict:
    return yaml.safe_load(led.read_text(encoding="utf-8"))["legs"][0]


def test_g70_e3_10_attach_consumes_a_typed_receipt_and_lifts_pending_to_full_bundle(tmp_path):
    """정상 경로 — 영수증 → 디스크 대조 → 원장 전이. lifecycle 소유 키는 그대로, inference_role 불변."""
    root, led, ev = _fixture_repo(tmp_path)
    rp = _write_receipt(root, "L", _receipt_core(root, "L", ev))
    r = P.attach_bundle_evidence("L", rp, ledger=led, repo_root=root)
    assert r["preservation_status"] == "full_bundle" and r["idempotent"] is False
    leg = _leg(led)
    assert (leg["preservation_status"], leg["validation_status"], leg["inference_role"]) == \
        ("full_bundle", "current_validated", "diagnostic")
    e = leg["evidence"]
    for k in ("bundle_uri", "payload_index_sha256", "payload_bytes", "bundle_files", "fits_sha256",
              "member_rehash_by", "verification_receipt", "verification_receipt_core_sha256",
              "validator_identity", "empty_root_restore", "bundle_content_id"):
        assert e.get(k), k                              # docs-lint 의 anchor 요구와 같은 키
    for k in P.LIFECYCLE_OWNED_EVIDENCE_KEYS:
        assert k in e, k                                # finalize 가 남긴 것을 지우지 않는다
    assert e["verification_receipt"] == rp
    # 멱등 — 같은 영수증으로 다시 붙이면 같은 답, 원장 바이트 불변
    before = led.read_bytes()
    r2 = P.attach_bundle_evidence("L", rp, ledger=led, repo_root=root)
    assert r2["idempotent"] is True and led.read_bytes() == before


@pytest.mark.parametrize("mutate,why", [
    (lambda c: c["validation"].update(ok=False, fail=["코드_identity"]), "통과를 말하지 않는다"),
    (lambda c: c["validation"].update(fail=["x"]), "통과를 말하지 않는다"),
    (lambda c: c.update(leg_id="M"), "다른 다리"),
    (lambda c: c["identity"].update(validator_source_digest="deadbeefdeadbeef"), "낡았다"),
    (lambda c: c["restore"].update(mode="in_place"), "empty-root"),
    (lambda c: c["restore"].update(conflicts=1), "empty-root"),
    (lambda c: c["bundle"].update(member_mismatches=1), "member 불일치"),
    (lambda c: c.update(outputs=[{"role": "other", "semantic_sha256": "1" * 64, "canonicalizer": "v"}]), "rescored_summary"),
    (lambda c: c.update(outputs_agree=False), "outputs_agree"),
    (lambda c: c.update(surplus=1), "core key 집합"),
    (lambda c: c["bundle"].pop("fits_sha256"), "core.bundle key 집합"),
    (lambda c: c["validation"].update(n_checks=3), "n_checks"),
])
def test_g70_e3_11_a_receipt_that_does_not_say_full_current_validation_is_refused(tmp_path, mutate, why):
    """부정 경로 — 실패·부분·다른 다리·낡은 검증기·열린 key 집합은 전부 원장에 쓰지 않는다."""
    root, led, ev = _fixture_repo(tmp_path)
    core = _receipt_core(root, "L", ev)
    mutate(core)
    rp = _write_receipt(root, "L", core)
    before = led.read_bytes()
    with pytest.raises(P.PreserveError) as ei:
        P.attach_bundle_evidence("L", rp, ledger=led, repo_root=root)
    assert why in str(ei.value), str(ei.value)
    assert led.read_bytes() == before, "거부하면서 원장을 건드렸다"


def test_g70_e3_12_a_receipt_whose_core_sha_does_not_match_its_core_is_refused(tmp_path):
    root, led, ev = _fixture_repo(tmp_path)
    core = _receipt_core(root, "L", ev)
    rp = _write_receipt(root, "L", core, core_sha="0" * 64)
    with pytest.raises(P.PreserveError, match="core_sha256"):
        P.attach_bundle_evidence("L", rp, ledger=led, repo_root=root)
    rp2 = _write_receipt(root, "L", core, extra_top={"note": "x"})
    with pytest.raises(P.PreserveError, match="최상위 key"):
        P.attach_bundle_evidence("L", rp2, ledger=led, repo_root=root)


def test_g70_e3_13_the_receipt_is_checked_against_the_disk_not_trusted(tmp_path):
    """영수증이 옳아 보여도 **묶음 바이트**가 다르면 거부 — 영수증은 주장이고 디스크가 실물이다."""
    root, led, ev = _fixture_repo(tmp_path)
    rp = _write_receipt(root, "L", _receipt_core(root, "L", ev))
    (root / "artifacts" / "L" / "fits.parquet").write_bytes(b"PAR1-fitz")     # 같은 길이
    with pytest.raises(P.PreserveError) as ei:
        P.attach_bundle_evidence("L", rp, ledger=led, repo_root=root)
    assert "실물과 다르다" in str(ei.value) and "fits.parquet" in str(ei.value), str(ei.value)


@pytest.mark.parametrize("status,why", [
    ("recorded_projection", "preservation_pending"),
    ("missing", "preservation_pending"),
])
def test_g70_e3_14_only_a_pending_finalized_leg_can_be_lifted(tmp_path, status, why):
    root, led, ev = _fixture_repo(tmp_path, status=status)
    rp = _write_receipt(root, "L", _receipt_core(root, "L", ev))
    with pytest.raises(P.PreserveError, match=why):
        P.attach_bundle_evidence("L", rp, ledger=led, repo_root=root)


def test_g70_e3_15_an_unperformed_leg_and_a_hand_written_record_are_refused(tmp_path):
    """`unperformed` — 실행 기록이 없으면 붙일 자리가 없다. lifecycle 소유 키가 없는(손으로 적은) 기록에도 안 붙인다."""
    root, led, ev = _fixture_repo(tmp_path)
    rp = _write_receipt(root, "L", _receipt_core(root, "L", ev))
    doc = yaml.safe_load(led.read_text(encoding="utf-8"))
    doc["legs"] = []
    led.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False), encoding="utf-8")
    with pytest.raises(P.PreserveError, match="unperformed"):
        P.attach_bundle_evidence("L", rp, ledger=led, repo_root=root)
    root2, led2, ev2 = _fixture_repo(tmp_path / "h", with_lifecycle=False)
    rp2 = _write_receipt(root2, "L", _receipt_core(root2, "L", ev2))
    with pytest.raises(P.PreserveError, match="lifecycle 소유 키"):
        P.attach_bundle_evidence("L", rp2, ledger=led2, repo_root=root2)


def test_g70_e3_16_a_second_different_receipt_does_not_replace_the_first(tmp_path):
    """이미 `full_bundle` 인 다리에 **다른** 영수증(다른 core sha)을 붙이려 하면 거부 — 영수증 교체는 사람의 일."""
    root, led, ev = _fixture_repo(tmp_path)
    rp = _write_receipt(root, "L", _receipt_core(root, "L", ev))
    P.attach_bundle_evidence("L", rp, ledger=led, repo_root=root)
    core2 = _receipt_core(root, "L", ev)
    core2["validation"]["checks"] = {"a": "ok", "c": "ok"}          # 다른 core → 다른 sha
    rec2 = {"schema_version": 2, "_주의": "시험", "core_sha256": P._receipt_core_sha256(core2),
            "core": core2, "stamp": {}}
    rp2_path = root / "docs" / "22p_gap" / "receipts" / "L.second.validate.yaml"
    rp2_path.write_text(yaml.safe_dump(rec2, allow_unicode=True, sort_keys=False), encoding="utf-8")
    before = led.read_bytes()
    with pytest.raises(P.PreserveError, match="갈아 끼우지"):
        P.attach_bundle_evidence("L", rp2_path.relative_to(root).as_posix(), ledger=led, repo_root=root)
    assert led.read_bytes() == before


def test_g70_e3_17_the_real_receipt_is_a_typed_receipt_of_the_current_validator():
    """양성 대조군 (읽기 전용) — 실물 `paired_fixed5_v4.validate.yaml` 이 닫힌 schema 를 지나고 현행 검증기의 것이다.
    (RUN_SCOPE 를 고치면 이 시험과 docs-lint 가 함께 '낡았다' 로 빨개진다 — 영수증을 다시 만들라는 뜻.)"""
    doc = yaml.safe_load(_REAL_LEDGER.read_text(encoding="utf-8"))
    for e in doc["legs"]:
        if e.get("preservation_status") != "full_bundle":
            continue
        core = P.read_verification_receipt(e["evidence"]["verification_receipt"], e["leg_id"], repo_root=REPO)
        assert P._receipt_core_sha256(core) == e["evidence"]["verification_receipt_core_sha256"], e["leg_id"]


# ═══════════════════════════════════════════════════════════════════════════
# E6 — 시험 authority 격리 · 운영 등록부 불변
# ═══════════════════════════════════════════════════════════════════════════
def test_g70_e6_01_the_test_session_does_not_use_the_tracked_ledger_as_default_authority():
    """conftest 가 세션 시작에 원장 **바이트 복사본**을 시험 authority 로 세운다 — 기본 인자(`ledger=None`)로
    쓰는 모든 등록(`_exec_class`·`_frozen_coords`·`_claims`·`_attempts`)이 거기로 간다."""
    led = Path(P.DEFAULT_LEDGER)
    assert led.resolve() != _REAL_LEDGER.resolve(), led
    assert led.is_file() and led.read_bytes() == _REAL_LEDGER.read_bytes(), "복사본이 원본 바이트와 다르다"
    for fn in (P.exec_class_root_for_ledger, P.frozen_coords_root_for_ledger,
               P.claims_root_for_ledger, P.attempts_root_for_ledger):
        got = fn()
        assert led.parent in got.parents, (fn.__name__, got)
        assert _REAL_REGISTRY.parent not in got.resolve().parents, (fn.__name__, got)


def test_g70_e6_02_a_default_ledger_registration_lands_in_the_isolated_registry(tmp_path):
    """`_complete_artifact` 류가 하는 것 — `ledger=None` 등록. 운영 `_exec_class/` 최상위 집합은 그대로다."""
    before = sorted(p.name for p in _REAL_REGISTRY.glob("*.json"))
    out = tmp_path / "results" / "run"
    _grid_outputs(out)
    cap = P.issue_execution_class(out, "L", "grid", ledger=None)
    P.commit_run_outputs(cap, [out])
    cid = P.run_content_id(out)
    assert (P.exec_class_root_for_ledger() / f"{cid}.json").is_file()
    assert not (_REAL_REGISTRY / f"{cid}.json").exists(), "운영 등록부에 시험 레코드가 생겼다 (E6)"
    assert sorted(p.name for p in _REAL_REGISTRY.glob("*.json")) == before


def test_g70_e6_03_the_impact_map_exists_and_matches_the_registry_census():
    """읽기 전용 영향 지도 `docs/22p_gap/registry_impact.md` — 문서의 수가 실물과 같아야 한다 (하드룰 4: 수치의 정본은 실물)."""
    doc = (REPO / "docs" / "22p_gap" / "registry_impact.md").read_text(encoding="utf-8")
    tracked = _tracked_registry_records()
    kinds = {"legacy": 0, "rekey": 0, "fixture": 0, "leg_L": 0, "other": 0}
    for rel in tracked:
        ev = json.loads((REPO / rel).read_text(encoding="utf-8"))["evidence"]
        if ev.startswith("legacy 분류"):
            kinds["legacy"] += 1
        elif "re-key" in ev:
            kinds["rekey"] += 1
        elif "_complete_artifact" in ev:
            kinds["fixture"] += 1
        elif "leg=L " in ev:
            kinds["leg_L"] += 1
        else:
            kinds["other"] += 1
    for key, n in (("tracked_total", len(tracked)), ("legacy", kinds["legacy"]), ("rekey", kinds["rekey"]),
                   ("fixture", kinds["fixture"]), ("leg_L", kinds["leg_L"]), ("other", kinds["other"])):
        assert f"<!-- census:{key}={n} -->" in doc, (key, n)


# ═══════════════════════════════════════════════════════════════════════════
# E10 — 양성 경로는 ambient 디렉터리가 아니라 등록된 fixture 로
# ═══════════════════════════════════════════════════════════════════════════
def test_g70_e10_01_a_registered_canonical_run_outside_the_namespace_is_promotable(tmp_path):
    """양성 대조군 — 격리 authority 에 canonical 로 등록·봉인된 산출은 승격 sink 를 지난다.
    (`results/grid_fit_v4` 가 있든 없든 상관없다.)"""
    from tests.test_compare import _complete_artifact
    d, _sig = _complete_artifact(tmp_path)
    assert not P.is_inside_namespace(d, P.SMOKE_NAMESPACE)
    P.assert_not_smoke_provenance([d], "정본 보고서")          # 예외 없음 = 통과
    assert P.resolve_execution_class(d, for_promotion=True)["execution_class"] == P.EXEC_CLASS_CANONICAL


def test_g70_e10_02_the_negative_control_still_refuses_a_smoke_run(tmp_path):
    d = REPO / "results" / "_smoke" / f"g70_{tmp_path.name}"
    d.mkdir(parents=True, exist_ok=True)
    try:
        (d / "manifest.yaml").write_text("run_spec: {}\n", encoding="utf-8")
        with pytest.raises(P.PreserveError, match="smoke namespace 산출은 승격 대상이 아니다"):
            P.assert_not_smoke_provenance([d], "정본 보고서")
    finally:
        import shutil
        shutil.rmtree(d, ignore_errors=True)
