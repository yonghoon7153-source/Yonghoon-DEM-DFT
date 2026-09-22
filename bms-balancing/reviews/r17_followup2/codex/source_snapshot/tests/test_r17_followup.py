"""R17 후속 재검토 (대상 `7c8f61f9`) — NO-GO · P1 3 · P2 2.

리뷰어가 인정한 것: `1/a` 수정과 명시 인자, 9개 chain-rule 회귀, absolute run_id 거부,
legacy None wildcard 거부, GC 의 A/100·A/200·B/100 원 반례(A/200 보존 독립 확인).
받지 못한 것: **파일 경계 · 비교 조건의 결속 · 영수증 완전성**.

| ID | 무엇이 틀렸나 | 자리 |
|---|---|---|
| FU-P1-01 | GC 가 **검사한 경로와 다른 경로를 지운다**. `path` 만 containment 검사를 받고, `rmtree` 는 `kind`/`attempt` 로 경로를 다시 만든다 — `kind=".."` 면 partial 밖이 지워진다. 중복 index 에서는 **보존 항목의 payload** 가 unlink 된다 | `scripts/gc_partial.py:91–98, 110–119` |
| FU-P1-02 | 행의 실행 조건과 sidecar 선언이 **결속되지 않는다**. 행만 v2 로 바꾸거나(파일 안 혼합 포함) `width_tol`·`cell`·`run_id` 를 어긋나게 해도 rc 0. `cycle` 은 `int(float(...))` 라 0.9 가 0 이 된다 | `scripts/width_report.py:96–117, 148–177` · `schema.cycles_key` |
| FU-P1-03 | 필수 키를 넣고 **`null` 로 채우면** 동일성 검사가 다시 열린다 — 양쪽 `git_commit=null` 이면 "동일 확인" 이 나온다. 키 존재는 typed 완전성이 아니다 | `scripts/width_report.py:85–88, 148–170` |
| FU-P2-01 | 근최적 폭에 **허용집합 밖의 점**이 들어간다. 상자 밖 seed 가 bounds 검사 없이 feasible 이 되고, stale `best_val` 이면 제약 밖 `best` 가 `vals` 에 재삽입된다 | `bms_balancing/verify.py:451, 468–481, 491` |
| FU-P2-02 | run receipt 의 "typed 완전성" 이 여전히 **필드 존재 검사**다. `runtime=null`·`materialized=17`·`produced_utc="not-a-date"`·`package.digest="not-a-digest"` 가 전부 `verified=true`. 실제 writer 는 `package_digest()` 의 **상태 dict** 를 `str()` 해서 digest 자리에 넣는다 | `scripts/verify_run_receipt.py:83–96` · `reviews/r11_repros/replay_codex_r11.py:335–351` |

**한 줄 요약**: 검사한 것과 사용한 것이 다르다 (P1-01 경로 · P1-02 선언 · P2-01 witness ·
P2-02 digest), 그리고 **부재를 닫았더니 `null` 로 옮겨 갔다** (P1-03).

리뷰어 재현기(`reviews/r17_followup/codex/repro_followup.py`)를 이 Linux 에서 먼저 돌려
다섯 건이 모두 재현되는 것을 확인했고(대조군 `gc_control` 0 · `width_seed_negative` 2 ·
`receipt_missing_runtime_negative` 3 도 정상), 그 관측을 아래 회귀로 고정한다.
"""
from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bms_balancing import schema as S          # noqa: E402
from bms_balancing import verify as V          # noqa: E402


def _run(script, *args, cwd=ROOT):
    return subprocess.run([sys.executable, str(ROOT / script), *map(str, args)], cwd=cwd,
                          capture_output=True, text=True, encoding="utf-8", timeout=600)


def _writecsv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


# ══════════════════════════════════════════════════════════════════════════════════════════════
# FU-P1-01 — GC 가 검사한 경로와 다른 경로를 지운다
# ══════════════════════════════════════════════════════════════════════════════════════════════

def _gc_index(root: Path, entries: list) -> None:
    """index 를 직접 쓴다 — 이 반례의 전제가 **malformed index** 이므로 정상 producer 로는 만들 수 없다.
    (리뷰어도 같은 이유로 합성했다. GC 코드 자체는 건드리지 않는다.)"""
    (root / "partial").mkdir(parents=True, exist_ok=True)
    (root / "partial" / "index.json").write_text(
        json.dumps({"index_version": 1, "attempts": entries}, ensure_ascii=False), encoding="utf-8")


def _entry(kind, attempt, artifact, path, body_sha="0" * 64, when="2026-09-22T00:00:00Z"):
    return {"kind": kind, "attempt": attempt, "artifact": artifact, "status": "partial",
            "path": path, "sha256": body_sha, "recorded_utc": when}


def test_fu_01_gc_refuses_an_index_whose_attempt_escapes_partial(tmp_path):
    """★ FU-P1-01 A — `path` 는 partial 안이지만 `kind='..'`·`attempt='victim'` 이면 `rmtree` 가
    **partial 밖**을 지운다. 첫 삭제 **전에** rc 2 로 거부해야 하고 바이트는 전부 남아야 한다."""
    out = tmp_path / "out"
    (out / "partial" / "matrix" / "A").mkdir(parents=True)
    (out / "partial" / "matrix" / "B").mkdir(parents=True)
    (out / "partial" / "matrix" / "A" / "matrix_100.csv").write_text("old", encoding="utf-8")
    (out / "partial" / "matrix" / "B" / "matrix_100.csv").write_text("new", encoding="utf-8")
    victim = out / "victim" / "sentinel.txt"
    victim.parent.mkdir(parents=True)
    victim.write_text("건드리면 안 되는 바이트", encoding="utf-8")

    _gc_index(out, [
        # 버려질 항목 — path 는 합법인데 kind/attempt 가 partial 밖을 가리킨다
        _entry("..", "victim", "matrix_100.csv", "matrix/A/matrix_100.csv"),
        # 같은 묶음의 최신 항목 (이것이 남는다)
        _entry("matrix", "B", "matrix_100.csv", "matrix/B/matrix_100.csv"),
        # 디스크의 A 디렉터리를 index 가 안다고 알려 주는 항목 (③ unknown 검사를 통과시키려고)
        _entry("matrix", "A", "matrix_keep.csv", "matrix/A/matrix_100.csv"),
    ])
    r = _run("scripts/gc_partial.py", "--root", out, "--keep", "1", "--apply")
    assert victim.exists(), ("GC 가 partial 밖의 파일을 지웠다 — 검사한 경로와 지운 경로가 다르다 "
                             "(FU-P1-01 A)", r.stdout[-400:], r.stderr[-400:])
    assert r.returncode == 2, ("partial 밖을 가리키는 index 를 rc 2 로 거부하지 않았다 (FU-P1-01 A)",
                               r.returncode, r.stderr[-400:])


def test_fu_02_gc_does_not_unlink_a_payload_a_retained_entry_still_references(tmp_path):
    """★ FU-P1-01 B — 같은 payload 를 가리키는 index 항목 둘. 하나가 버려져도 **보존 항목이 참조하는
    파일**은 남아야 한다 (`retained_attempts` 는 디렉터리만 막고 `f.unlink()` 는 막지 않았다)."""
    out = tmp_path / "out"
    (out / "partial" / "matrix" / "A").mkdir(parents=True)
    shared = out / "partial" / "matrix" / "A" / "matrix_100.csv"
    shared.write_text("둘이 같이 가리키는 payload", encoding="utf-8")
    _gc_index(out, [
        _entry("matrix", "A", "matrix_100.csv", "matrix/A/matrix_100.csv", when="2026-09-22T00:00:00Z"),
        _entry("matrix", "A", "matrix_100.csv", "matrix/A/matrix_100.csv", when="2026-09-22T01:00:00Z"),
    ])
    r = _run("scripts/gc_partial.py", "--root", out, "--keep", "1", "--apply")
    assert shared.exists(), ("보존 항목이 참조하는 payload 를 GC 가 지웠다 (FU-P1-01 B)",
                             r.returncode, r.stdout[-400:], r.stderr[-400:])


def test_fu_03_gc_still_keeps_the_reviewer_original_case(tmp_path):
    """대조군 — 리뷰어가 **닫혔다고 인정한** 원 반례(A/100 · A/200 · B/100)는 계속 통과해야 한다.
    이번 수정이 그것을 되돌리면 여기서 잡힌다."""
    out = tmp_path / "gc-safe"; out.mkdir()
    for name, rid, body in [("matrix_100.csv", "A", "100-old"), ("matrix_200.csv", "A", "200-only"),
                            ("matrix_100.csv", "B", "100-new")]:
        canonical = out / name
        d = V.publish_target(canonical, "partial", run_id=rid)
        d.write_text(body, encoding="utf-8")
        V.record_partial(canonical, d, status="partial", run_id=rid)
    survivor = out / "partial" / "matrix" / "A" / "matrix_200.csv"
    r = _run("scripts/gc_partial.py", "--root", out, "--keep", "1", "--apply")
    assert r.returncode == 0, (r.returncode, r.stderr[-400:])
    assert survivor.exists(), "A/200 이 사라졌다 — R17 P1-01 의 수정이 되돌아갔다"


# ══════════════════════════════════════════════════════════════════════════════════════════════
# FU-P1-02 · FU-P1-03 — 본문 ↔ sidecar 결속, null 동일성
# ══════════════════════════════════════════════════════════════════════════════════════════════

_CONSUMED = {"full_cell": {"path": "cell.xlsx", "sha256": "a" * 64},
             "half_cell": {"path": "half.xlsx", "sha256": "c" * 64},
             "literature": {"gr": {"path": "gr.xlsx", "sha256": "d" * 64},
                            "si": {"path": "si.xlsx", "sha256": "e" * 64}}}


def _base_row():
    base = {k: "1" for k in S.CYCLES_ROW}
    base.update(cell="syn", cycle="0", width_status="measured", width_tol="0.01",
                width_is_lower_bound="True", objective_version="legacy_matlab")
    base.update(consumed_inputs=json.dumps(_CONSUMED), inputs_sha=S.inputs_digest(_CONSUMED))
    for m in ("LAM_PE", "LAM_NE", "LLI"):
        base.update({m: "0", m + "_lo": "-0.01", m + "_hi": "0.01"})
    return base


def _meta(i):
    return {"lb": [0.1, -0.2, 0.1, -0.2, 0], "ub": [2, 0.5, 2, 0.5, 1],
            "initial": [1, 0, 1, 0, 0.25], "gamma_prefit": False, "gamma_lb": 0,
            "n_multistart": 20, "seed": 0, "scale_seed": 0, "w_pocv": 1, "w_dvdq": 1,
            "w_dqdv": i, "objective_version": "legacy_matlab", "optimizer": "SLSQP",
            "widths": True, "width_tol": 0.01, "width_starts": 4,
            "width_method": "constrained-extrema", "width_grid": 0,
            "cell": "syn", "si_source": "external", "starts": 20, "cycles": [0, 1],
            "consumed_inputs": copy.deepcopy(_CONSUMED),
            "env": {"python": "3.11", "numpy": "1", "scipy": "1", "pandas": "1",
                    "openpyxl": "3", "platform": "Linux"},
            "git_commit": "0" * 40, "run_id": f"r{i}", "dataset_manifest": {"id": "fake-manifest"}}


def _width_pair(tmp_path, name, row_change=None, meta_change=None, both_meta=None):
    """리뷰어 fixture — `w_dqdv` 만 다른 정상 두 실행에 축 하나를 더 흔든다.
    본문 sha256 과 입력 receipt 는 **항상 정확하게** 갱신한다 (무결성 위조가 아니다)."""
    base = _base_row()
    d = tmp_path / name; d.mkdir()
    paths = []
    for i in (0, 1):
        # 행의 `run_id`·`cell` 은 production(`cycles.py`)이 실제로 쓰는 열이다 — sidecar 의 선언과
        # 같아야 한다. 채움값 "1" 로 두면 fixture 가 본문↔sidecar 모순을 숨긴다.
        rows = [dict(base, cycle=str(k), run_id=f"r{i}") for k in (0, 1)]
        meta = _meta(i)
        if i and row_change:
            row_change(rows)
        if i and meta_change:
            meta_change(meta)
        if both_meta:
            both_meta(meta)
        for row in rows:
            row.update(consumed_inputs=json.dumps(meta["consumed_inputs"]),
                       inputs_sha=S.inputs_digest(meta["consumed_inputs"]))
        p = d / f"{i}.csv"; _writecsv(p, rows)
        meta["sha256"] = hashlib.sha256(p.read_bytes()).hexdigest()   # ← 정확하게 갱신
        p.with_name(p.name + ".meta.json").write_text(json.dumps(meta), encoding="utf-8")
        paths.append(p)
    return _run("scripts/width_report.py", *paths, "--axis", "w_dqdv")


def test_fu_04_width_positive_control_still_passes(tmp_path):
    """대조군 — 정상 두 실행(`w_dqdv` 만 0→1)은 계속 rc 0 이어야 한다."""
    r = _width_pair(tmp_path, "positive")
    assert r.returncode == 0, (r.returncode, r.stderr[-500:])


def test_fu_05_width_negative_control_still_rejects_a_second_axis(tmp_path):
    """대조군 — sidecar 의 seed 까지 다르면 계속 rc 2 여야 한다."""
    r = _width_pair(tmp_path, "seed", meta_change=lambda m: m.update(seed=1))
    assert r.returncode == 2, (r.returncode, r.stdout[-300:])


@pytest.mark.parametrize("label,row_change", [
    ("body_version", lambda rows: [r.update(objective_version="chain_rule_v2") for r in rows]),
    ("body_mixed_version", lambda rows: rows[0].update(objective_version="chain_rule_v2")),
    ("body_tol", lambda rows: [r.update(width_tol="0.90") for r in rows]),
    ("body_cell", lambda rows: [r.update(cell="DIFFERENT_CELL") for r in rows]),
])
def test_fu_06_width_rejects_a_body_that_contradicts_its_sidecar(tmp_path, label, row_change):
    """★ FU-P1-02 — 본문 행이 sidecar 선언과 어긋나면 rc 2 여야 한다.

    본문 sha256 도 입력 receipt 도 정확하다 — **무결성이 아니라 내용의 모순**이다. 한 파일 안에서
    버전이 섞인 경우(`body_mixed_version`)도 같다: 비교 조건은 파일당 하나여야 한다.
    """
    r = _width_pair(tmp_path, label, row_change=row_change)
    assert r.returncode == 2, (f"본문↔sidecar 모순({label})을 통과시켰다 (FU-P1-02)",
                               r.returncode, r.stdout[-400:])


def test_fu_07_width_rejects_a_fractional_cycle(tmp_path):
    """★ FU-P1-02 — `cycle` 0.9/1.9 는 `int(float(...))` 로 접히면 선언 [0,1] 과 같아 보인다.
    정수성을 **먼저** 검사해 rc 2 여야 한다."""
    r = _width_pair(tmp_path, "fractional",
                    row_change=lambda rows: [r.update(cycle=str(float(r["cycle"]) + 0.9)) for r in rows])
    assert r.returncode == 2, ("정수가 아닌 cycle 을 절단해서 받아들였다 (FU-P1-02)",
                               r.returncode, r.stdout[-400:])


def test_fu_08_width_rejects_a_body_run_id_that_is_not_the_declared_run(tmp_path):
    """★ FU-P1-02 — 행의 `run_id` 가 sidecar 의 선언과 다르면 그 행은 이 실행의 것이 아니다."""
    if "run_id" not in S.CYCLES_ROW:
        pytest.skip("cycles 행에 run_id 열이 없다 — 이 축은 행에서 선언되지 않는다")
    r = _width_pair(tmp_path, "body_run",
                    row_change=lambda rows: [r.update(run_id="unrelated-run") for r in rows])
    assert r.returncode == 2, (r.returncode, r.stdout[-400:])


@pytest.mark.parametrize("label,keys", [
    ("null_identity", ("git_commit", "env", "dataset_manifest")),
    ("null_settings", ("seed", "lb", "ub", "initial", "objective_version")),
])
def test_fu_09_width_rejects_null_filled_required_meta(tmp_path, label, keys):
    """★ FU-P1-03 — 필수 키를 **양쪽 다 `null`** 로 채우면 지금은 "동일 확인" 이 나온다.
    키 존재는 typed 완전성이 아니다 — 필수 값의 타입·형식까지 봐야 한다."""
    def both(m):
        for k in keys:
            m[k] = None
    r = _width_pair(tmp_path, label, both_meta=both)
    assert r.returncode == 2, (f"필수 meta 를 null 로 채운 두 실행을 '동일 확인' 으로 비교했다 "
                               f"(FU-P1-03 {label})", r.returncode, r.stdout[-400:])
    assert "동일 확인" not in r.stdout, ("null identity 에서 '동일 확인' 을 출력했다", r.stdout[-300:])


def test_fu_10_width_keeps_a_legitimate_nullable_field(tmp_path):
    """대조군 — 합법적으로 nullable 한 항목(`gamma_lb`)은 **양성으로 남아야** 한다.
    "null 이면 전부 거부" 로 넓히면 이 시험이 잡는다."""
    r = _width_pair(tmp_path, "nullable_ok", both_meta=lambda m: m.update(gamma_lb=None))
    assert r.returncode == 0, ("합법 nullable 을 거부했다 — 필수 값과 구분해야 한다",
                               r.returncode, r.stdout[-400:], r.stderr[-400:])


# ══════════════════════════════════════════════════════════════════════════════════════════════
# FU-P2-01 — 근최적 폭에 허용집합 밖의 점이 들어간다
# ══════════════════════════════════════════════════════════════════════════════════════════════

_LB5 = [1.0, -0.2, 0.1, -0.2, 0.0]
_UB5 = [1.4, 0.5, 2.0, 0.5, 1.0]
_REF = np.array([1.2, 0.0, 1.0, 0.0, 0.25])


def _extrema(obj, best, best_val, seeds, tol=0.01):
    return V.near_optimal_extrema(obj=obj, best=np.asarray(best, float), best_val=best_val,
                                  ref_p=_REF, ref_c=1.0, c_cell=1.0, lb=_LB5, ub=_UB5,
                                  tol=tol, seeds=[np.asarray(s, float) for s in seeds],
                                  n_starts=2, seed=0)


def test_fu_11_a_seed_outside_the_box_can_not_become_a_witness():
    """★ FU-P2-01 A — 상자 밖 seed(`a_PE=10`)가 bounds 검사 없이 feasible 이 된다.
    참 범위는 ±16.67 %p 인데 −733 %p 가 하한으로 나온다."""
    out = _extrema(obj=lambda p: 1.0, best=[1.2, 0, 1, 0, 0.25], best_val=1.0,
                   seeds=[[10.0, 0.0, 1.0, 0.0, 0.25]])
    lo = float(out["LAM_PE"]["min"])
    assert lo > -20.0, ("상자 밖 seed 가 하한 witness 가 됐다 (FU-P2-01 A) — "
                        f"LAM_PE 하한 {lo:.4f} %p, 상자 안 참 범위는 ±16.67 %p")


def test_fu_12_a_best_outside_the_feasible_set_is_not_reinserted():
    """★ FU-P2-01 B — 전달된 `best_val` 이 stale 이면 `obj(best)` 가 한계 밖인데도
    `vals` 가 `best` 를 다시 넣는다. 그 점은 허용집합의 원소가 아니다."""
    obj = lambda p: 1.0 + (float(p[0]) - 1.0) ** 2
    with pytest.raises((RuntimeError, ValueError)):
        _extrema(obj=obj, best=[1.4, 0, 1, 0, 0.25], best_val=1.0, seeds=[])


def test_fu_13_a_consistent_best_still_works():
    """대조군 — `best_val` 이 실제로 `obj(best)` 면 계속 동작해야 한다 (전부 거부로 넓히지 않는다)."""
    obj = lambda p: 1.0 + (float(p[0]) - 1.2) ** 2
    out = _extrema(obj=obj, best=[1.2, 0, 1, 0, 0.25], best_val=obj([1.2, 0, 1, 0, 0.25]),
                   seeds=[[1.25, 0, 1, 0, 0.25]])
    lo, hi = float(out["LAM_PE"]["min"]), float(out["LAM_PE"]["max"])
    assert np.isfinite(lo) and np.isfinite(hi) and lo <= hi, out


def test_fu_14_width_fields_marks_an_invalid_call_failed_not_measured(tmp_path):
    """★ FU-P2-01 — 위 두 반례가 `_width_fields()` 를 타면 `measured` 가 아니라 `failed` 여야 한다."""
    from bms_balancing import cycles as C

    obj = lambda p: 1.0 + (float(p[0]) - 1.0) ** 2
    got = C._width_fields(widths=True, obj=obj, ref_p=_REF, ref_c=1.0, c_cell=1.0,
                          best=np.array([1.4, 0, 1, 0, 0.25]), best_val=1.0, tol=0.01,
                          starts=2, seed=0, lb5=_LB5, say=lambda *a, **k: None)
    assert got.get("width_status") == "failed", ("허용집합 밖 best 로 계산한 폭을 measured 로 적었다 "
                                                 "(FU-P2-01)", got)


# ══════════════════════════════════════════════════════════════════════════════════════════════
# FU-P2-02 — receipt 의 typed 완전성
# ══════════════════════════════════════════════════════════════════════════════════════════════

def _receipt(tmp_path, **over):
    """실제 코드 참조(commit/tree/blob)를 담은 **양성** 영수증을 만들고 한 축만 흔든다."""
    sys.path.insert(0, str(ROOT / "reviews"))
    import evidence_gate as G                                    # noqa: PLC0415

    git = lambda *a: subprocess.check_output(["git", *a], cwd=ROOT, text=True).strip()
    r = {"receipt_version": G.RUN_RECEIPT_VERSION,
         "code": {"commit": git("rev-parse", "HEAD"), "tree": git("rev-parse", "HEAD^{tree}")},
         "instrument": {"reviews/evidence_gate.py": git("rev-parse", "HEAD:./reviews/evidence_gate.py")},
         "package": {"digest": "b" * 64},
         "materialized": {"mode": "sparse detached worktree"},   # 생산자가 내는 모양 (None 도 합법)
         "runtime": {"python": "3.11.15", "platform": "Linux"},
         "produced_utc": "2026-09-22T00:00:00Z"}
    r.update(over)
    r["signature"] = G.receipt_signature(r)                      # 서명은 **정확하게** 다시 계산한다
    p = tmp_path / "receipt.json"
    p.write_text(json.dumps(r, ensure_ascii=False), encoding="utf-8")
    return p


def test_fu_15_receipt_positive_control(tmp_path):
    """대조군 — 온전한 영수증은 계속 rc 0 이어야 한다."""
    r = _run("scripts/verify_run_receipt.py", "--receipt", _receipt(tmp_path), "--target", ROOT)
    assert r.returncode == 0, (r.returncode, r.stdout[-400:], r.stderr[-400:])


@pytest.mark.parametrize("label,over", [
    ("null_runtime", {"runtime": None}),
    ("bad_runtime", {"runtime": "not-a-runtime-object"}),
    ("bad_materialized", {"materialized": 17}),
    ("bad_date", {"produced_utc": "not-a-date"}),
    ("non_digest", {"package": {"digest": "not-a-digest"}}),
])
def test_fu_16_receipt_rejects_wrong_types(tmp_path, label, over):
    """★ FU-P2-02 — 키가 **있기만** 하면 통과한다. 타입·형식이 틀린 값은 `verified=false` 여야 한다.

    서명은 정확하게 다시 계산했으므로 암호학적 위조가 아니다 — **typed 완전성**의 문제다.
    """
    r = _run("scripts/verify_run_receipt.py", "--receipt", _receipt(tmp_path, **over), "--target", ROOT)
    assert r.returncode == 3, (f"잘못된 타입({label})을 통과시켰다 (FU-P2-02)",
                               r.returncode, r.stdout[-400:])


def _pkg(tmp_path, body: bytes):
    d = tmp_path / f"pkg_{body.decode()}"
    d.mkdir()
    (d / "one.txt").write_bytes(body)
    sums = d / "SHA256SUMS"
    sums.write_text(f"{hashlib.sha256(body).hexdigest()}  one.txt\n", encoding="utf-8")
    return d, sums


def test_fu_17_package_status_is_not_a_content_address(tmp_path):
    """★ FU-P2-02 — `package_digest()` 의 두 번째 반환값은 **검사 상태 dict** 다
    (`{파일: ok|mismatch|missing}`). bytes 가 다른 두 정상 패키지가 같은 값을 낸다.
    이 시험은 그 사실을 **고정**한다 — 상태는 상태로 두되, digest 자리에 쓰면 안 된다."""
    sys.path.insert(0, str(ROOT / "reviews"))
    import evidence_gate as G                                    # noqa: PLC0415

    a_ok, a_status = G.package_digest(*_pkg(tmp_path, b"AAA"))
    b_ok, b_status = G.package_digest(*_pkg(tmp_path, b"BBB"))
    assert a_ok and b_ok, (a_status, b_status)
    assert a_status == b_status == {"one.txt": "ok"}, (a_status, b_status)


def test_fu_18_a_package_content_digest_separates_different_bytes(tmp_path):
    """★ FU-P2-02 — receipt 의 `package.digest` 는 **실제 내용 주소**여야 한다.
    bytes 가 다르면 값이 달라야 하고, 같으면 같아야 한다 (정규 내용 digest)."""
    sys.path.insert(0, str(ROOT / "reviews"))
    import evidence_gate as G                                    # noqa: PLC0415

    fn = getattr(G, "package_content_digest", None)
    assert fn is not None, ("패키지의 내용 digest 를 발행하는 함수가 없다 — 검사 상태와 내용 주소가 "
                            "분리되지 않았다 (FU-P2-02)")
    again = tmp_path / "again"
    again.mkdir()
    da = fn(*_pkg(tmp_path, b"AAA"))
    db = fn(*_pkg(tmp_path, b"BBB"))
    da2 = fn(*_pkg(again, b"AAA"))                 # 다른 자리, 같은 bytes
    assert isinstance(da, str) and len(da) == 64 and all(c in "0123456789abcdef" for c in da), da
    assert da != db, ("bytes 가 다른 두 패키지가 같은 내용 digest 를 냈다 (FU-P2-02)", da, db)
    assert da2 == da, ("같은 bytes 가 다른 내용 digest 를 냈다 — 정규화가 안 됐다", da, da2)
