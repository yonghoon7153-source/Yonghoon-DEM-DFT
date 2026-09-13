"""Codex R9 (2026-09-12, 대상 `29ef505`, NO-GO · P1 7 · P2 5) — 반례를 회귀로.

원문·패키지는 `reviews/r9_repros/codex/` (sha256 11/11). 수정 전 HEAD 에서 세 스크립트가 전부 재현됐다
(`reviews/r9_repros/replay_ours_29ef505_before/`). R8 이 "모집단을 먼저 세고, 검증 snapshot 만 검사하고, 부분은 부분이라
말한다" 였다면 R9 는 **그 불변식이 production 전체에서 성립하는가** — 인자 파싱·U18 승격·ne_shape 입력/게시·dd_eval.
"""
from __future__ import annotations
import contextlib, csv, hashlib, importlib.util, io, json, os, pathlib, subprocess, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np                                                        # noqa: E402
import pytest                                                             # noqa: E402
from bms_balancing import verify                                          # noqa: E402
from test_r6_internal import _synth_root, _prov, _cs                      # noqa: E402
from test_r7_codex import _args, _deg, _sign, _compare_states, _doc, _live  # noqa: E402
from test_r8_codex import _mod, _cli, _verdict, _full_matrix_rows, _shape_harness, _pair  # noqa: E402


# ── R9-01 ────────────────────────────────────────────────────────────────────────────────────
def test_d9_01_duplicate_or_unlabelled_root_arguments_are_rejected_not_collapsed(tmp_path):
    """[Codex R9-01 · P1] `roots[label] = path` 라 `same=<없는 root> same=<정상 root>` 에서 두 번째가 첫 요청을 지워
    "요청한 root 1 개 · 1/1 · 예 rc 0". label 없는 인자 여럿도 전부 `out` 이 된다.
    닫힘 조건: 인자를 ordered list 로 유지하고 중복 label(암묵적 `out` 포함)을 **사전에** 거부한다."""
    good, empty = tmp_path / "good", tmp_path / "empty"; good.mkdir(); empty.mkdir()
    art = good / "degeneracy_100_Li.json"
    verify.atomic_write_json(art, _deg("100", "r9-root", {"LAM_PE": 2.0, "LAM_NE": 3.0, "LLI": 1.0})); _sign(art, "r9-root", "100")
    def cs(*argv):
        r = subprocess.run([sys.executable, str(ROOT / "scripts/compare_states.py"), *map(str, argv)],
                           cwd=ROOT, capture_output=True, text=True, timeout=120)
        return r.returncode, r.stdout + r.stderr
    rc, out = cs(f"same={empty}", f"same={good}")
    assert rc != 0 and "중복" in out and "same" in out, (rc, out[-500:])
    assert not _verdict(out).rstrip().endswith("예"), out[-500:]
    rc, out = cs(empty, good)                                              # label 없는 인자 둘 = 둘 다 `out`
    assert rc != 0 and "중복" in out, (rc, out[-500:])
    rc, out = cs(f"a={empty}", f"b={good}")                                # 대조군: 고유 label 은 둘 다 센다
    assert rc == 2 and "요청한 root 2 개" in out and "미완" in out, (rc, out[-600:])


# ── R9-02 ────────────────────────────────────────────────────────────────────────────────────
def test_d9_02_check_u14_compares_the_exact_artifact_roster_not_just_what_new_contains(tmp_path):
    """[Codex R9-02 · P1] new 에 있는 파일만 순회해 old 12 개 중 1 개만 재실행해도 "산출 1 개 · 전부 같다 · rc 0".
    닫힘 조건: old/new canonical basename 의 합집합으로 exact roster 를 정하고 missing·extra 를 거부한다; 부분
    재실행은 명시적 subset 계약과 범위를 출력한다."""
    old, new = tmp_path / "old", tmp_path / "new"; old.mkdir(); new.mkdir()
    for st in ("100", "200"):
        a = _deg(st, f"old-{st}", {"LAM_PE": 1.0, "LAM_NE": 2.0, "LLI": 0.5}, schema=True)
        f = old / f"degeneracy_{st}_Li.json"; verify.atomic_write_json(f, a); _sign(f, f"old-{st}", st, full=True)
    a = _deg("100", "new-100", {"LAM_PE": 1.0, "LAM_NE": 2.0, "LLI": 0.5}, schema=True)
    f = new / "degeneracy_100_Li.json"; verify.atomic_write_json(f, a); _sign(f, "new-100", "100", full=True)
    rc, out, _ = _cli("check_u14.py", "--new", new, "--old", old)
    assert rc != 0 and "전부 같다" not in out, (rc, out[-600:])
    assert "roster" in out.lower() or "명부" in out, out[-600:]
    assert "degeneracy_200_Li.json" in out and ("없" in out or "missing" in out), out[-600:]
    rc, out, _ = _cli("check_u14.py", "--new", new, "--old", old, "--subset")   # 명시적 부분 계약
    # ⚠ Codex R10 P2-1 로 계약이 바뀌었다: 부분은 성공 종료가 아니다 (rc 3) 이고 판정은 machine-readable 로도 나온다.
    assert rc == 3 and ("subset" in out or "부분" in out) and "1/2" in out, (rc, out[-600:])
    promo = json.loads(next(l for l in out.splitlines() if l.startswith("PROMOTION "))[len("PROMOTION "):])
    assert promo["promotion_eligible"] is False and promo["subset"] is True, promo


# ── R9-03 ────────────────────────────────────────────────────────────────────────────────────
def test_d9_03_check_u14_validates_content_science_columns_and_run_controls(tmp_path):
    """[Codex R9-03 · P1] (A) 서명된 matrix 에서 `LLI_pct` 를 지워도 rc 0 (B) 출처 열 값을 전부 비워도 "전부 갖췄다"
    (C) degeneracy 의 실행 조건 {n_starts,seed,n_grid,n_samples,tol} 을 바꿔 다시 서명해도 "게시·서명만 바뀌었다".
    `--schema-only` 는 중복 key 검사도 건너뛴다.
    닫힘 조건: producer 에서 파생한 artifact 별 exact schema 를 한 정본으로 — 필수 셀 nonempty/type, receipt 의 역할·
    path·64-hex digest, 재계산한 aggregate digest, 실행 조건 비교, 구조 검사는 schema-only 에서도."""
    from bms_balancing import schema as S
    old, new = tmp_path / "old", tmp_path / "new"; old.mkdir(); new.mkdir()
    # (A) 과학 열 삭제
    rows = _full_matrix_rows("r9-A")
    f_old = old / "matrix_100.csv"; verify.atomic_write_csv(f_old, rows, list(rows[0])); _sign(f_old, "r9-A", "100", full=True)
    dropped = [{k: v for k, v in r.items() if k != "LLI_pct"} for r in rows]
    f_new = new / "matrix_100.csv"; verify.atomic_write_csv(f_new, dropped, list(dropped[0])); _sign(f_new, "r9-A", "100", full=True)
    rc, out, _ = _cli("check_u14.py", "--new", new, "--old", old)
    assert rc != 0 and "LLI_pct" in out, (rc, out[-500:])
    # (B) 출처 셀이 비었다 / 형식이 틀렸다 — 서명은 맞아도 provenance-incomplete
    blank = _full_matrix_rows("r9-B")
    for r in blank:
        r["ref_inputs_sha"] = ""; r["consumed_inputs"] = ""; r["ref_consumed_inputs"] = ""
    verify.atomic_write_csv(f_new, blank, list(blank[0])); _sign(f_new, "r9-B", "100", full=True)
    rc, out, _ = _cli("check_u14.py", "--new", new, "--schema-only")
    assert rc != 0 and ("비어" in out or "빈" in out or "empty" in out), (rc, out[-500:])
    bogus = _full_matrix_rows("r9-C")
    for r in bogus:
        r["ref_inputs_sha"] = "f" * 64; r["consumed_inputs"] = "{}"; r["ref_consumed_inputs"] = "{}"
    verify.atomic_write_csv(f_new, bogus, list(bogus[0])); _sign(f_new, "r9-C", "100", full=True)
    rc, out, _ = _cli("check_u14.py", "--new", new, "--schema-only")
    assert rc != 0 and ("digest" in out or "sha" in out), (rc, out[-500:])
    # 진짜 receipt 는 통과한다 — 대조군 (역할·path·64-hex·재계산 aggregate 가 맞는 행)
    real = _full_matrix_rows("r9-D")
    ci = {"half_cell": {"path": "h.xlsx", "sha256": "1" * 64}, "full_cell": {"path": "f.xlsx", "sha256": "2" * 64},
          "literature": {"gr": {"path": "g.xlsx", "sha256": "3" * 64}, "si": {"path": "s.csv", "sha256": "4" * 64}}}
    rci = {"half_cell": {"path": "p.xlsx", "sha256": "5" * 64}, "full_cell": ci["full_cell"], "literature": ci["literature"]}
    for r in real:
        r["consumed_inputs"] = json.dumps(ci); r["ref_consumed_inputs"] = json.dumps(rci)
        r["inputs_sha"] = S.inputs_digest(ci); r["ref_inputs_sha"] = S.inputs_digest(rci)
    verify.atomic_write_csv(f_new, real, list(real[0])); _sign(f_new, "r9-D", "100", full=True)
    rc, out, _ = _cli("check_u14.py", "--new", new, "--schema-only")
    assert rc == 0, (rc, out[-600:])
    # (C) 실행 조건이 바뀐 재실행은 "같은 실행" 이 아니다
    a = _deg("100", "r9-ctl", {"LAM_PE": 1.0, "LAM_NE": 2.0, "LLI": 0.5}, schema=True) | {"n_starts": 24, "seed": 0, "tol_percent_of_best": 1.0}
    fo = old / "degeneracy_100_Li.json"; verify.atomic_write_json(fo, a); _sign(fo, "r9-ctl", "100", full=True)
    b = dict(a, n_starts=1, seed=731, n_grid=999, n_samples=1, tol_percent_of_best=50.0)
    fn = new / "degeneracy_100_Li.json"; verify.atomic_write_json(fn, b); _sign(fn, "r9-ctl", "100", full=True)
    f_new.unlink(); (new / "matrix_100.csv.meta.json").unlink(); f_old.unlink(); (old / "matrix_100.csv.meta.json").unlink()
    rc, out, _ = _cli("check_u14.py", "--new", new, "--old", old)
    assert rc != 0 and "n_starts" in out and "seed" in out, (rc, out[-700:])
    # (D) schema-only 도 구조 검사(중복 key)를 한다
    dup = _full_matrix_rows("r9-dup") + _full_matrix_rows("r9-dup")[:1]
    for r in dup:
        r["consumed_inputs"] = json.dumps(ci); r["ref_consumed_inputs"] = json.dumps(rci)
        r["inputs_sha"] = S.inputs_digest(ci); r["ref_inputs_sha"] = S.inputs_digest(rci)
    verify.atomic_write_csv(f_new, dup, list(dup[0])); _sign(f_new, "r9-dup", "100", full=True); fn.unlink(); (new / "degeneracy_100_Li.json.meta.json").unlink()
    rc, out, _ = _cli("check_u14.py", "--new", new, "--schema-only")
    assert rc != 0 and "중복" in out, (rc, out[-500:])


# ── R9-04 ────────────────────────────────────────────────────────────────────────────────────
def _run_shape(ns, monkeypatch, matrix, out):
    buf = io.StringIO()
    monkeypatch.setattr(sys, "argv", ["ne_shape.py", "--out-dir", str(matrix), "--write", str(out)])
    with contextlib.redirect_stdout(buf):
        rc = ns.main()
    return rc, buf.getvalue()


def _read_shape(out, sub=""):
    f = (out / sub / "ne_shape_GITT_Li.csv") if sub else (out / "ne_shape_GITT_Li.csv")
    rows = {r["state"]: r for r in csv.DictReader(io.StringIO(f.read_text(encoding="utf-8")))}
    return f, rows, json.loads(f.with_name(f.name + ".meta.json").read_text(encoding="utf-8"))


def test_d9_04_ne_shape_keeps_a_state_with_a_missing_half_cell_in_the_requested_roster(tmp_path, monkeypatch):
    """[Codex R9-04 · P1] 선언 상태 pristine·100·200 에서 200 반쪽전지 파일만 없으면 200 은 requested 에 들기 **전에**
    사라져 `{requested:[100], paired:[100], missing:[]}` · 1/1 · rc 0.
    닫힘 조건: 파일 존재 확인 전에 requested roster 를 고정하고 requested/available/missing_input/paired/missing_pair
    를 각각 기록한다."""
    base = tmp_path; matrix, out = base / "matrix", base / "shape"; matrix.mkdir()
    ns = _shape_harness(monkeypatch, base, {"pristine": 0.0, "100": 0.01, "200": 0.10})
    class P:
        def __init__(self, state): self.state = state
        def is_file(self): return self.state != "200"
    monkeypatch.setattr(ns.D, "half_cell_path", lambda root, src, state: P(state))
    monkeypatch.setattr(ns.D, "HALF_FILE", {"GITT": {"pristine": "p", "100": "a", "200": "b"}})
    _pair(matrix, "100")
    rc, text = _run_shape(ns, monkeypatch, matrix, out)
    assert rc != 0 and "200" in text and ("입력 없음" in text or "missing_input" in text), (rc, text[-800:])
    _, rows, meta = _read_shape(out, "partial")
    census = meta["pairing"]
    assert census["requested"] == ["100", "200"] and census["missing_input"] == ["200"], census
    assert census["available"] == ["100"] and census["paired"] == ["100"], census
    assert not (out / "ne_shape_GITT_Li.csv").exists(), "부분 결과가 canonical 자리에 게시됐다"


# ── R9-05 ────────────────────────────────────────────────────────────────────────────────────
def test_d9_05_ne_shape_refuses_duplicate_matrix_keys_instead_of_taking_the_first_row(tmp_path):
    """[Codex R9-05 · P1] `fitted_pair_info` 가 첫 match 를 즉시 반환해 서명된 matrix 에 (GITT,Li,0) 이 두 행이면 행 순서에
    따라 γ 0.10 ↔ 0.40 이 바뀌고(γ 변화 17.59 ↔ 35.73 mV) 둘 다 paired 1/1 rc 0.
    닫힘 조건: production reader 가 정규화한 (half_cell, si, numeric w_dqdv) 가 정확히 한 행인지 강제한다 — checker 와
    같은 typed validator 를 공유한다."""
    ns = _mod("ne_shape_r9", ROOT / "scripts/ne_shape.py")
    d = tmp_path / "out"; d.mkdir()
    from bms_balancing import schema as _S
    from test_review_findings import matrix_row
    # ⚠ Codex R11 P1-7: reader 가 checker 와 같은 validator 를 쓴다 — 중복 판정에 닿으려면 행이 온전해야 한다
    rows = [matrix_row(gamma_Si=g, ref_gamma_Si="0.2", run_id="r9-dup") for g in ("0.10", "0.40")]
    f = d / "matrix_100.csv"; verify.atomic_write_csv(f, rows, list(_S.MATRIX_ROW)); _sign(f, "r9-dup", "100")
    with pytest.raises(RuntimeError, match="중복"):
        ns.fitted_pair_info(d, "100", "GITT", "Li")
    rows = [dict(rows[0], w_dqdv="0.0"), dict(rows[1], w_dqdv="0")]           # 정규화 뒤 같은 key 도 중복이다
    verify.atomic_write_csv(f, rows, list(_S.MATRIX_ROW)); _sign(f, "r9-dup", "100")
    with pytest.raises(RuntimeError, match="중복"):
        ns.fitted_pair_info(d, "100", "GITT", "Li")
    from bms_balancing import schema as S
    assert S.unique_rows                                                     # checker 와 같은 validator


# ── R9-06 ────────────────────────────────────────────────────────────────────────────────────
def test_d9_06_partial_ne_shape_run_does_not_overwrite_the_complete_canonical_unit(tmp_path, monkeypatch):
    """[Codex R9-06 · P1] 완전 실행(100·200 짝)을 canonical 에 게시한 뒤 200 짝을 없애고 다시 돌리면 rc 3 이지만 이미
    canonical CSV/meta 를 부분 묶음으로 **교체**했다 (`read_unit` True).
    닫힘 조건: 완전성 판정을 게시보다 먼저; partial 은 별도 attempt namespace 에 typed 상태로; canonical 승격은
    complete 만."""
    base = tmp_path; matrix, out = base / "matrix", base / "shape"; matrix.mkdir()
    ns = _shape_harness(monkeypatch, base, {"pristine": 0.0, "100": 0.01, "200": 0.10})
    _pair(matrix, "100"); _pair(matrix, "200")
    rc1, _ = _run_shape(ns, monkeypatch, matrix, out)
    art, _, meta1 = _read_shape(out)
    assert rc1 == 0 and meta1["pairing"]["missing"] == [] and meta1.get("status") == "complete"
    bytes1 = art.read_bytes()
    (matrix / "matrix_200.csv").unlink(); (matrix / "matrix_200.csv.meta.json").unlink()
    rc2, text2 = _run_shape(ns, monkeypatch, matrix, out)
    assert rc2 == 3, (rc2, text2[-400:])
    assert art.read_bytes() == bytes1, "부분 실행이 완전 canonical 을 덮었다"
    assert _prov().read_unit(art)[0] is True
    _, rows_p, meta_p = _read_shape(out, "partial")
    assert meta_p.get("status") == "partial" and meta_p["pairing"]["missing"] == ["200"], meta_p
    assert "partial" in text2 or "부분" in text2


# ── R9-07 ────────────────────────────────────────────────────────────────────────────────────
def _eval_fixture(path):
    P = np.asarray(verify.DD_EVAL_P, dtype=float)
    anchors = {k: float(i + 1) for i, (k, _) in enumerate(verify.ANCHOR_STAGE)}
    cols = ["rmse_pocv", "rmse_dvdq", "rmse_dqdv", "rmse_dqdv_w"]
    vals = {c: [0.001 * (j + 1) * (i + 1) for i in range(len(P))] for j, c in enumerate(cols)}
    lines = ["# printed_format,%.17g"] + [f"# {k},{v:.17g}" for k, v in anchors.items()]
    header = "a_PE,b_PE,a_NE,b_NE,gamma_Si," + ",".join(cols)
    lines.append(header)
    for i, q in enumerate(P):
        lines.append(",".join([f"{x:.6f}" for x in q] + [f"{vals[c][i]:.17g}" for c in cols]))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return anchors, P, vals, header


def test_d9_07_eval_compare_parses_resolves_and_audits_one_immutable_snapshot(tmp_path, monkeypatch):
    """[Codex R9-07 · P1] `_compare_dd_eval` 이 경로를 세 번 연다 (parse · precision · audit). 첫 read 가 중복 header 인
    malformed A 이고 직후 정상 B 로 원자 교체되면 단독 A 는 invalid 인데 race 는 A 의 32 셀을 B 의 precision/audit 로
    승인해 complete.
    닫힘 조건: 한 번 읽은 immutable bytes/text 와 digest 를 parse·precision·audit·compare 전부에 전달하고 검증 뒤
    pathname 을 다시 열지 않는다."""
    p = tmp_path / "matlab_eval.csv"
    anchors, P, vals, header = _eval_fixture(p)
    valid = p.read_text(encoding="utf-8")
    malformed = valid.replace(header + "\n", header + "\n" + header + "\n", 1)
    p.write_text(malformed, encoding="utf-8")
    with contextlib.redirect_stdout(io.StringIO()):
        control = verify._compare_dd_eval(anchors, P, vals, p)
    assert control["status"] == "invalid"
    original = pathlib.Path.read_text; reads = {"n": 0}
    def racing(self, *a, **k):
        data = original(self, *a, **k)
        if pathlib.Path(self).resolve() == p.resolve():
            reads["n"] += 1
            if reads["n"] == 1:
                p.write_text(valid, encoding="utf-8")                      # 첫 읽기 직후 정상 B 로 교체
        return data
    monkeypatch.setattr(pathlib.Path, "read_text", racing)
    with contextlib.redirect_stdout(io.StringIO()):
        raced = verify._compare_dd_eval(anchors, P, vals, p)
    monkeypatch.undo()
    assert reads["n"] == 1, f"경로를 {reads['n']} 번 읽었다 — 한 번이어야 한다"
    assert raced["status"] == "invalid", raced["status"]                    # A 를 읽었으면 A 로 판정한다


# ── P2 ───────────────────────────────────────────────────────────────────────────────────────
def test_d9_08_r7_runner_rejects_unknown_empty_or_duplicate_probes_and_wrong_head():
    """[Codex R9 P2-1·2] `--probes DOES_NOT_EXIST` 를 조용히 버리고 `probes: {}` rc 0; expected SHA·clean·패키지 bytes 를
    대조하지 않아 임의 HEAD 에서도 '반례 소멸' rc 0.
    닫힘 조건: 빈/오타/중복/valid+unknown 거부, 출력 key == 요청 집합; `--expected-head` 필수, mismatch·dirty·재현·오류
    중 하나라도 있으면 nonzero."""
    runner = ROOT / "reviews/r7_repros/replay_codex_r7.py"
    head = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()
    def run(*extra):
        r = subprocess.run([sys.executable, str(runner), "--target", str(ROOT), *extra], cwd=ROOT,
                           capture_output=True, text=True, timeout=600)
        return r.returncode, r.stdout, r.stderr
    for bad in ("DOES_NOT_EXIST", "", "R7-01,R7-01", "R7-01,NOPE"):
        rc, out, err = run("--probes", bad, "--expected-head", head)
        assert rc != 0 and "probes" not in out[:2], (bad, rc, out[:200], err[-300:])
    rc, out, err = run("--probes", "R7-06")                                # expected-head 없이는 안 돈다
    assert rc != 0 and "expected-head" in (out + err), (rc, err[-300:])
    rc, out, err = run("--probes", "R7-06", "--expected-head", "0" * 40)   # SHA 불일치
    assert rc != 0 and ("mismatch" in (out + err) or "다르" in (out + err)), (rc, err[-300:])
    # ⚠ Codex R10 P2-5 로 계약이 바뀌었다: dirty 를 **거부**하는 대신 expected commit 의 격리 snapshot 에서 돈다
    #   (working tree 가 어떻든 실행 bytes 는 그 커밋이다). dirty 여부는 결과에 그대로 기록된다.
    rc, out, err = run("--probes", "R7-06", "--expected-head", head)
    snap = json.loads(out)
    # ⚠ 자체 리뷰 C19 뒤: 종료 코드가 `evidence_eligible` 을 반영한다 — 증거가 아닌 실행은 0 이 아니다 (3).
    #   개발 중 트리에서는 도구 자신이 HEAD 의 blob 과 달라 eligible false 가 정상이므로 계약으로 단언한다.
    assert rc == (0 if snap["evidence_eligible"] else 3), (rc, snap["evidence_eligible"], err[-400:])
    assert snap["ran_in"] == "격리 snapshot" and snap["materialized"]["head"] == head, snap.get("materialized")
    rc, out, err = run("--probes", "R7-06", "--expected-head", head, "--allow-dirty")   # 시험 중 트리는 dirty 다 — 명시하고 기록
    # ⚠ 자체 리뷰 C19 뒤: 종료 코드가 `evidence_eligible` 을 반영한다 (증거면 0, 아니면 3)
    assert rc == (0 if json.loads(out)["evidence_eligible"] else 3), (rc, err[-400:])
    d = json.loads(out)
    assert list(d["probes"]) == ["R7-06"] and d["expected_head"] == head and d["package_digest_ok"] is True, d.keys()
    assert d["dirty_allowed"] is True and isinstance(d["dirty"], bool) and isinstance(d["dirty_paths"], list), d.keys()


def test_d9_09_mutation_audit_classifies_pytest_rc_2_3_4_as_audit_errors():
    """[Codex R9 P2-3] 같은 `1 failed` summary 에 rc 2·3·4 도 CAUGHT — CAUGHT 는 rc 1 과 failure fingerprint 에만."""
    mod = _mod("r6_audit_r9", ROOT / "reviews/r6_repros/codex_r6_mutation_audit.py")
    s = "1 failed, 51 deselected in 1.4s"
    assert mod.classify(1, s) == "CAUGHT"
    for rc in (2, 3, 4, 5, -9, 124):
        assert mod.classify(rc, s) == "오류", rc
    assert mod.classify(0, "1 passed, 51 deselected in 1.4s") == "MISSED"
    assert mod.classify(1, "1 passed, 51 deselected in 1.4s") == "오류"     # rc 1 인데 failed 가 없다 — fingerprint 불일치


def test_d9_10_matrix_sidecar_seals_the_exact_roster_and_argv(tmp_path):
    """[Codex R9 P2-4] `run_states.sh` 의 sidecar 는 matrix 에도 singular `GITT/Li` 를 적지만 본문은 2 반쪽전지 × 8 Si ×
    2 가중 = 32 행이다. exact roster 와 argv 를 본문에서 유도해 sidecar 에 봉인한다."""
    rows = _full_matrix_rows("r9-side")
    art = tmp_path / "matrix_100.csv"; verify.atomic_write_csv(art, rows, list(rows[0]))
    shell = (ROOT / "scripts/run_states.sh").read_text(encoding="utf-8")
    code = shell[shell.index("write_meta ()"):shell.index('\nmkdir -p "$OUT"')]
    code += "\n" + shell[shell.index("\nsay ()") + 1:shell.index("\nfail=0")]
    # ⚠ Codex R10 P2-3: argv 는 `$*` 문자열이 아니라 **vector** 다. 이 시험은 roster 봉인을 보고, `run()` 을 통한
    #   production 결속(위조하면 깨지는 자리)은 `test_d10_11` 이 본다.
    code += ('\nLAST_RUN_ID="$2"; LAST_ARGV_JSON=\'["python3","-m","bms_balancing.verify","matrix","--state","100"]\';'
             ' write_meta "$1" 100 GITT\n')
    env = dict(os.environ, STARTS="2", SI="Li", BMS_DATA_ROOT="synthetic", OUT=str(tmp_path),
               PATH=str(pathlib.Path(sys.executable).parent) + os.pathsep + os.environ.get("PATH", ""))
    p = subprocess.run(["bash", "-c", code, "r9", str(art), "r9-side"], cwd=ROOT, env=env, capture_output=True, text=True, timeout=60)
    assert p.returncode == 0, (p.stdout, p.stderr)
    meta = json.loads(art.with_name(art.name + ".meta.json").read_text(encoding="utf-8"))
    assert meta["argv"][:4] == ["python3", "-m", "bms_balancing.verify", "matrix"], meta.get("argv")
    roster = meta["roster"]
    # ⚠ Codex R13 P1-1: 기대치를 손으로 적지 않고 **정본 모집단에서 유도**한다 (fixture 가 2 행이던 시절의
    #   하드코딩은 모집단이 틀려도 통과했다).
    from bms_balancing import schema as S
    keys = sorted(S.canonical_combo_keys("100"))
    assert roster["rows"] == len(keys), roster
    assert roster["half_cell"] == sorted({k[0] for k in keys}), roster
    assert roster["si"] == sorted({k[1] for k in keys}), roster
    assert meta["si_source"] != "Li" or "roster" in meta                    # singular 가 본문을 대신하지 않는다


def test_d9_11_zero_pair_and_partial_are_distinct_typed_states(tmp_path, monkeypatch):
    """[Codex R9 P2-5] 요청문은 "missing pair 면 rc 3" 이라 했으나 pair 가 전부 없으면 rc 1 이 먼저 난다 — 계약과 wrapper
    가 1/3 을 명시적으로 구분해야 한다. meta 의 typed `status` 로 none/partial/complete 를 갈라 남긴다."""
    base = tmp_path; matrix, out = base / "matrix", base / "shape"; matrix.mkdir()
    ns = _shape_harness(monkeypatch, base, {"pristine": 0.0, "100": 0.01})
    rc, text = _run_shape(ns, monkeypatch, matrix, out)                     # 짝 0
    assert rc == 1 and not (out / "ne_shape_GITT_Li.csv").exists(), (rc, text[-300:])
    _, _, meta = _read_shape(out, "partial")
    assert meta.get("status") == "none" and meta["pairing"]["paired"] == [], meta.get("status")
    doc = _live(_doc("scripts/ne_shape.py"))
    assert "rc 1" in doc and "rc 3" in doc or "종료 코드 1" in doc          # 계약이 코드에 적혀 있다


def test_d9_12_docs_record_the_r9_closure():
    led = _live(_doc("reviews/R6_LEDGER.md"))
    assert "Codex R9" in led and "R9-01" in led and "R9-07" in led
    req = _live(_doc("reviews/R10_REQUEST.md"))
    assert "R9-0" in req and "expected-head" in req
    ws = _live(_doc("WORKING_STATE.md"))
    assert "9차" in ws and "provenance-incomplete" in ws
