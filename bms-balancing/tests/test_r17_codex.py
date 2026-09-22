"""Codex R17 (대상 `dfc1fc78`, NO-GO · P1 5 · P2 2) — 리뷰어 반례를 **그대로** 회귀로 고정한다 (2026-09-22).

원문: `reviews/r17_repros/codex/pkg/R17_REVIEW.md` · 반례 스크립트 `repro_r17.py` · `science_repro.py`.
각 시험의 docstring 첫 줄이 리뷰어 항목 번호다. 시험은 **의도한 거부**를 기대한다 — 고치기 전에는 전부
빨개야 한다 (그것이 RED 관측이고, 처음부터 초록이면 fixture 가 진실을 가리고 있다는 뜻이다).

P1-05(과학 결론의 과잉 추론)는 코드가 아니라 `BML_R1_RESPONSE.md` 의 문장이므로 여기 없다 —
`R17_RESPONSE.md` 가 다룬다. chain rule 도 여기 없다 — 명시 objective 계약이 먼저다.
"""
from __future__ import annotations

import copy
import csv
import hashlib
import io
import json
import pathlib
import shutil
import subprocess
import sys

import numpy as np
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tests"))
from bms_balancing import verify as V, schema as S, cycles, model      # noqa: E402

sys.path.insert(0, str(ROOT / "reviews"))
import evidence_gate as gate                                            # noqa: E402


def _run(script, *args, cwd=ROOT):
    return subprocess.run([sys.executable, str(ROOT / script), *map(str, args)], cwd=cwd,
                          capture_output=True, text=True, encoding="utf-8", timeout=600)


def _writecsv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


# ──────────────────────────────────────────────────────────────────────────────────────────────
# P1-01 — GC 의 보관 단위 (kind, artifact) 와 삭제 단위 (kind, attempt) 가 다르다
# ──────────────────────────────────────────────────────────────────────────────────────────────

def _gc_fixture(tmp_path):
    """리뷰어 fixture — 한 시도 A 가 두 산출(100·200)을 내고, 다른 시도 B 가 100 만 다시 낸다.

    `record_partial` (실제 producer) 로 index 를 만든다 — Linux 라 fcntl 이 있다. GC 코드는 건드리지 않는다.
    """
    out = tmp_path / "gc-safe-fixture"; out.mkdir()
    for name, rid, body in [("matrix_100.csv", "A", "100-old"), ("matrix_200.csv", "A", "200-only"),
                            ("matrix_100.csv", "B", "100-new")]:
        canonical = out / name
        d = V.publish_target(canonical, "partial", run_id=rid)
        d.write_text(body, encoding="utf-8")
        V.record_partial(canonical, d, status="partial", run_id=rid)
    return out


def test_r17_01_gc_keeps_an_attempt_dir_that_a_retained_artifact_still_references(tmp_path):
    """[P1-01] `--keep 1 --apply` 는 100 의 A 만 버려야 하고 **200 의 유일한 결과(A)는 남아야 한다**."""
    out = _gc_fixture(tmp_path)
    victim = out / "partial" / "matrix" / "A" / "matrix_200.csv"
    assert victim.is_file()
    r = _run("scripts/gc_partial.py", "--root", out, "--keep", "1", "--apply")
    assert r.returncode == 0, r.stderr
    assert victim.is_file(), "retained artifact 가 참조하는 attempt 디렉터리를 통째로 지웠다 (P1-01)"
    idx = json.loads((out / "partial" / "index.json").read_text(encoding="utf-8"))
    kept = {(e["attempt"], e["artifact"]) for e in idx["attempts"]}
    assert ("A", "matrix_200.csv") in kept, kept
    assert ("B", "matrix_100.csv") in kept, kept
    assert ("A", "matrix_100.csv") not in kept, "버려야 할 100 의 구 시도가 index 에 남았다"


def test_r17_02_gc_dry_run_names_files_not_whole_attempts(tmp_path):
    """[P1-01 · 대조군] dry-run 도 같은 모델을 말해야 한다 — 지울 것은 `matrix/A/matrix_100.csv` 하나다."""
    out = _gc_fixture(tmp_path)
    r = _run("scripts/gc_partial.py", "--root", out, "--keep", "1")
    assert r.returncode == 0, r.stderr
    assert "matrix_100.csv" in r.stdout and "matrix_200.csv" not in r.stdout, r.stdout
    assert (out / "partial" / "matrix" / "A" / "matrix_200.csv").is_file()


# ──────────────────────────────────────────────────────────────────────────────────────────────
# P1-02 — absolute attempt-id 하나로 partial 목적지가 canonical 이 된다
# ──────────────────────────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("bad", [
    pytest.param("ABS", id="absolute-path"),
    pytest.param("../escape", id="parent-traversal"),
    pytest.param("a/b", id="separator"),
    pytest.param("", id="empty"),
    pytest.param(".", id="dot"),
    pytest.param("..", id="dotdot"),
])
def test_r17_03_publish_target_rejects_non_simple_attempt_ids_before_touching_disk(tmp_path, bad):
    """[P1-02] attempt-id 는 **단일 경로 성분**이어야 한다 — 절대경로·상위 이동·구분자·alias 는 첫 mkdir 전에 거부."""
    canonical = tmp_path / "canonical-fixture" / "matrix_100.csv"
    canonical.parent.mkdir()
    rid = str(canonical.parent.resolve()) if bad == "ABS" else bad
    with pytest.raises(ValueError):
        V.publish_target(canonical, "partial", run_id=rid)
    assert not (canonical.parent / "partial").exists(), "거부하기 전에 디렉터리를 만들었다"


def test_r17_04_publish_target_never_resolves_onto_canonical(tmp_path):
    """[P1-02 · 리뷰어 반례 그대로] `run_id=str(canonical.parent)` 가 canonical 자체를 돌려주면 안 된다."""
    canonical = tmp_path / "canonical-fixture" / "matrix_100.csv"
    canonical.parent.mkdir()
    try:
        dest = V.publish_target(canonical, "partial", run_id=str(canonical.parent))
    except ValueError:
        return                                            # 의도한 거부
    assert dest.resolve() != canonical.resolve(), "partial 목적지가 canonical 이다 (P1-02)"
    assert dest.resolve().is_relative_to((canonical.parent / "partial").resolve())


# ──────────────────────────────────────────────────────────────────────────────────────────────
# P1-03 — `--old <dir>` 에는 과거 revision 결속 없이 일회성 이관 승인이 붙는다
# ──────────────────────────────────────────────────────────────────────────────────────────────

def test_r17_05_legacy_transition_needs_a_recorded_old_revision_not_a_wildcard():
    """[P1-03 · 함수] `old_rev_full=None` 은 **미검증**이지 wildcard 가 아니다 — 승인을 주지 않는다."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import importlib
    C = importlib.import_module("check_u14")
    dec = C.load_decisions()
    e = dec["legacy_transitions"][-1]
    roster, commits = set(e["new"]["roster"]), set(e["code_commits"])
    blocked = {"env_contract_legacy": 13}
    assert C.legacy_transition(roster, commits, e["old"]["rev"], blocked, dec) == e["id"], "정상 대조군이 깨졌다"
    assert C.legacy_transition(roster, commits, "f" * 40, blocked, dec) is None, "다른 revision 대조군이 깨졌다"
    assert C.legacy_transition(roster, commits, None, blocked, dec) is None, \
        "old revision 이 None 인데 승인이 붙었다 (P1-03)"


def test_r17_06_check_u14_old_directory_without_identity_gets_no_legacy_approval(tmp_path):
    """[P1-03 · CLI] 현행 `out/` 사본에서 sidecar·run_id 만 지운 `--old` 는 rc 4 여도 `legacy_transition_approved` 가 false."""
    old = tmp_path / "current-as-old"
    shutil.copytree(ROOT / "out", old, ignore=shutil.ignore_patterns("*.meta.json", "archive", "partial"))
    for p in old.iterdir():
        if p.suffix == ".csv":
            rows = list(csv.DictReader(io.StringIO(p.read_text(encoding="utf-8-sig"))))
            if rows and "run_id" in rows[0]:
                for row in rows:
                    row.pop("run_id", None)
                _writecsv(p, rows)
        elif p.suffix == ".json":
            body = json.loads(p.read_text(encoding="utf-8-sig"))
            if isinstance(body, dict):
                body.pop("run_id", None)
                p.write_text(json.dumps(body, ensure_ascii=False), encoding="utf-8")
    r = _run("scripts/check_u14.py", "--new", "out", "--old", old)
    line = next((x for x in r.stdout.splitlines() if x.startswith("PROMOTION ")), None)
    assert line, r.stdout[-2000:] + r.stderr[-2000:]
    verdict = json.loads(line[len("PROMOTION "):])
    assert verdict["promotion_eligible"] is False
    assert verdict.get("legacy_transition_approved") is not True, \
        f"revision 결속 없는 디렉터리 대조에 일회성 승인이 붙었다 (P1-03): {verdict}"


# ──────────────────────────────────────────────────────────────────────────────────────────────
# P1-04 — width_report rc 0 은 "한 축만 달랐다" 또는 "전수 cycle" 증거가 아니다
# ──────────────────────────────────────────────────────────────────────────────────────────────

_CONSUMED = {"full_cell": {"path": "cell.xlsx", "sha256": "a" * 64},
             "half_cell": {"path": "half.xlsx", "sha256": "c" * 64},
             "literature": {"gr": {"path": "gr.xlsx", "sha256": "d" * 64},
                            "si": {"path": "si.xlsx", "sha256": "e" * 64}}}


def _base_row():
    base = {k: "1" for k in S.CYCLES_ROW}
    base.update(cell="syn", cycle="0", width_status="measured", width_tol="0.01", width_is_lower_bound="True",
                objective_version="legacy_matlab")                 # ⑥ — 행이 어느 미분인지 말해야 완전한 행이다
    base.update(consumed_inputs=json.dumps(_CONSUMED), inputs_sha=S.inputs_digest(_CONSUMED))
    for m in ("LAM_PE", "LAM_NE", "LLI"):
        base.update({m: "0", m + "_lo": "-0.01", m + "_hi": "0.01"})
    return base


def _width_pair(tmp_path, name, change=None, meta_change=None):
    """리뷰어 `pair()` 그대로 — 모든 production 열을 채운 두 실행, `w_dqdv` 만 다르고 한 축을 더 흔든다."""
    base = _base_row()
    d = tmp_path / name; d.mkdir()
    paths = []
    for i in (0, 1):
        rows = [dict(base, cycle=str(k)) for k in (0, 1)]
        meta = {"lb": [0.1, -0.2, 0.1, -0.2, 0], "ub": [2, 0.5, 2, 0.5, 1],
                "initial": [1, 0, 1, 0, 0.25], "gamma_prefit": False, "gamma_lb": 0,
                "n_multistart": 20, "seed": 0, "scale_seed": 0, "w_pocv": 1, "w_dvdq": 1,
                "w_dqdv": i, "objective_version": "legacy_matlab", "optimizer": "SLSQP", "widths": True, "width_tol": 0.01,
                "width_starts": 4, "width_method": "constrained-extrema", "width_grid": 0,
                "cell": "syn", "si_source": "external", "starts": 20, "cycles": [0, 1],
                "consumed_inputs": copy.deepcopy(_CONSUMED),
                "env": {"python": "3.11", "numpy": "1", "scipy": "1", "pandas": "1", "openpyxl": "3", "platform": "Linux"},
                # 실제 producer(`fit_cycles` → `sidecar_dict`)의 결속 키 — 리뷰어 fixture 의 `code` 대신 `git_commit`
                "git_commit": "0" * 40, "run_id": f"r{i}", "dataset_manifest": {"id": "fake-manifest"}}
        if i and change:
            change(rows)
        if i and meta_change:
            meta_change(meta)
        for row in rows:
            row.update(consumed_inputs=json.dumps(meta["consumed_inputs"]),
                       inputs_sha=S.inputs_digest(meta["consumed_inputs"]))
        p = d / f"{i}.csv"; _writecsv(p, rows)
        meta["sha256"] = hashlib.sha256(p.read_bytes()).hexdigest()
        p.with_name(p.name + ".meta.json").write_text(json.dumps(meta), encoding="utf-8")
        paths.append(p)
    return _run("scripts/width_report.py", *paths, "--axis", "w_dqdv")


def test_r17_07_width_report_positive_and_negative_controls(tmp_path):
    """[P1-04 · 대조군] 축 하나만 다르면 rc 0, seed 까지 다르면 rc 2 — 이 둘은 지금도 맞아야 한다."""
    assert _width_pair(tmp_path, "positive").returncode == 0
    assert _width_pair(tmp_path, "seed", meta_change=lambda m: m.update(seed=1)).returncode == 2


@pytest.mark.parametrize("label,change,meta_change", [
    pytest.param("different-inputs", None,
                 lambda m: m["consumed_inputs"]["full_cell"].update(sha256="b" * 64), id="input-sha-changed"),
    pytest.param("missing-cycle", lambda rows: rows.pop(), None, id="cycle-dropped"),
    pytest.param("duplicate-cycle", lambda rows: rows.append(dict(rows[0], LAM_NE_hi="0.9")), None, id="duplicate-cycle"),
    pytest.param("nan", lambda rows: rows[0].update(LAM_NE_hi="nan"), None, id="nan-endpoint"),
    pytest.param("blank-tol", lambda rows: rows[0].update(width_tol=""), None, id="blank-tol"),
])
def test_r17_08_width_report_refuses_input_roster_and_finite_violations(tmp_path, label, change, meta_change):
    """[P1-04] 입력 SHA 변경 · cycle 누락 · cycle 중복 · NaN 끝점 · 빈 tol — 전부 **거부(rc 2)** 여야 한다."""
    r = _width_pair(tmp_path, label, change=change, meta_change=meta_change)
    assert r.returncode == 2, f"{label}: rc {r.returncode} 로 비교를 허용했다 (P1-04)\n{r.stdout}\n{r.stderr}"


# ──────────────────────────────────────────────────────────────────────────────────────────────
# P2-01 — 폭 tagged union 이 의미를 닫지 못하고, 빈 허용집합을 measured 0 으로 낸다
# ──────────────────────────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("change", [
    pytest.param({"width_is_lower_bound": "False"}, id="lower-bound-False"),
    pytest.param({"width_is_lower_bound": "banana"}, id="lower-bound-garbage"),
    pytest.param({"width_tol": "-0.5"}, id="negative-tol"),
    pytest.param({"width_tol": "nan"}, id="nan-tol"),
    pytest.param({"LAM_NE_lo": "0.2", "LAM_NE_hi": "-0.2"}, id="inverted-interval"),
    pytest.param({"LAM_NE_hi": "nan"}, id="nan-endpoint"),
    pytest.param({"LAM_NE_lo": "0.5", "LAM_NE_hi": "0.6"}, id="point-outside-interval"),
])
def test_r17_09_width_union_closes_semantics_not_just_presence(change):
    """[P2-01 · consumer] 칸이 차 있어도 **뜻이 틀리면** 거부 — 정상 대조군은 그대로 통과한다."""
    base = _base_row()
    assert S.check_rows("cycles", [base], list(S.CYCLES_ROW), "cycles_syn.csv") == [], "정상 대조군이 깨졌다"
    row = dict(base, **change)
    assert S.check_width_union(row) or S.check_rows("cycles", [row], list(S.CYCLES_ROW), "cycles_syn.csv"), \
        f"{change} 가 통과했다 (P2-01)"


def test_r17_10_width_producer_refuses_an_empty_feasible_set_instead_of_measured_zero():
    """[P2-01 · producer · 리뷰어 반례 그대로] `tol=-0.5` 로 허용집합이 공집합이면 `measured/폭 0` 이 아니라 `failed`."""
    bp = (model.LB5 + model.UB5) / 2
    w = cycles._width_fields(True, lambda p: 1.0, bp, 1.0, 1.0, bp, 1.0, -0.5, 0, 0, model.LB5, lambda *a: None)
    assert w["width_status"] != "measured", f"빈 허용집합을 measured 로 냈다 (P2-01): {w}"


def test_r17_11_near_optimal_extrema_does_not_fall_back_to_best_when_nothing_is_feasible():
    """[P2-01 · core] `feasible` 이 비면 `best` 를 조용히 넣지 않는다 — 결과가 아니라 실패다."""
    bp = (model.LB5 + model.UB5) / 2
    with pytest.raises(Exception):
        V.near_optimal_extrema(lambda p: 1.0, bp, 1.0, 1.0, bp, 1.0, tol=-0.5, seeds=[], n_starts=0,
                               seed=0, lb=model.LB5, ub=model.UB5)


# ──────────────────────────────────────────────────────────────────────────────────────────────
# P2-02 — run receipt 필수 결속을 제거한 객체도 verified=true
# ──────────────────────────────────────────────────────────────────────────────────────────────

def test_r17_12_incomplete_run_receipt_is_not_reported_as_fully_verified(tmp_path):
    """[P2-02] code/instrument/signature 만 있는 객체 — 서명·ancestry 는 맞아도 **전체 verified** 를 주면 안 된다."""
    git = lambda *a: subprocess.check_output(["git", *a], cwd=ROOT, text=True).strip()  # noqa: E731
    receipt = {"code": {"commit": git("rev-parse", "HEAD"), "tree": git("rev-parse", "HEAD^{tree}")},
               "instrument": {"reviews/evidence_gate.py": git("rev-parse", "HEAD:./reviews/evidence_gate.py")}}
    receipt["signature"] = gate.receipt_signature(receipt)
    rp = tmp_path / "incomplete-receipt.json"; rp.write_text(json.dumps(receipt), encoding="utf-8")
    r = _run("scripts/verify_run_receipt.py", "--receipt", rp, "--target", ROOT)
    line = next((x for x in r.stdout.splitlines() if x.startswith("RUN_RECEIPT_VERIFY ")), None)
    assert line, r.stdout + r.stderr
    v = json.loads(line[len("RUN_RECEIPT_VERIFY "):])
    assert r.returncode != 0 and v["verified"] is not True, \
        f"receipt_version·package·runtime 없는 객체를 verified=true 로 냈다 (P2-02): {v}"
