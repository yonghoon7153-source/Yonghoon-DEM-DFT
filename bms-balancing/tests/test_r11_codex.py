"""Codex R11 (2026-09-13, 대상 `2add074` · 코드 정본 `665c87e`, NO-GO · P1 12 · P2 6) — 반례를 회귀로.

원문·패키지는 `reviews/r11_repros/codex/` (sha256 13/13). 수정 전 clean 체크아웃에서 네 스크립트가 전부 재현됐다
(`reviews/r11_repros/replay_ours_2add074_before/`). R10 이 "게시는 완전성 판정 뒤에, receipt 는 역할을 묶고, 증거는
자기가 실행한 bytes 를 봉인한다" 였다면 R11 은 **그 셋이 identity 까지 가는가** — 입력 bytes 가 달라도 승격되는가,
caller 옵션이 authority 를 줄이는가, 비유한 값이 과학 값으로 통과하는가, 증거 러너가 import 전에 격리하는가.
"""
from __future__ import annotations
import contextlib, csv, hashlib, io, json, math, os, pathlib, shutil, subprocess, sys
from types import SimpleNamespace

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np                                                        # noqa: E402
import pytest                                                             # noqa: E402
from bms_balancing import data as D                                       # noqa: E402
from bms_balancing import schema as S                                     # noqa: E402
from bms_balancing import verify                                          # noqa: E402
from test_r7_codex import _sign, _doc, _live                              # noqa: E402
from test_r8_codex import _cli, _full_matrix_rows, _shape_harness, _pair   # noqa: E402
from test_review_findings import _fixture_repo                            # noqa: E402
from test_r10_codex import _receipt, _shell, _run_shape                   # noqa: E402


def _rec(tag):
    """역할 넷을 갖춘 receipt — `tag` 마다 **입력 bytes 가 다르다** (identity 비교용)."""
    def leaf(x):
        return {"path": f"/data/{x}.xlsx", "sha256": hashlib.sha256(f"{tag}-{x}".encode()).hexdigest()}
    d = {"full_cell": leaf("full"), "half_cell": leaf("half"),
         "literature": {"gr": leaf("gr"), "si": leaf("si")}}
    return d, S.inputs_digest(d)


def _matrix_unit(directory, rid, target_tag="A", ref_tag="A", **cell):
    """서명된 matrix 묶음 하나 — receipt 를 태그로 갈아 끼울 수 있다."""
    ci, dg = _rec(target_tag)
    rci, rdg = _rec(ref_tag + "-ref")
    rows = _full_matrix_rows(rid)
    for r in rows:
        r["consumed_inputs"], r["inputs_sha"] = json.dumps(ci), dg
        r["ref_consumed_inputs"], r["ref_inputs_sha"] = json.dumps(rci), rdg
        r.update(cell)
    directory.mkdir(parents=True, exist_ok=True)
    f = directory / "matrix_100.csv"
    verify.atomic_write_csv(f, rows, list(rows[0]))
    _sign(f, rid, "100", full=True)
    return f


def _promotion(out):
    line = next((l for l in out.splitlines() if l.startswith("PROMOTION ")), "")
    return json.loads(line[len("PROMOTION "):]) if line else None


# ── P1-1 ─────────────────────────────────────────────────────────────────────────────────────
def test_e11_01_promotion_compares_the_input_identity_of_both_runs(tmp_path):
    """[Codex R11 P1-1 · P1] 각자 유효한 receipt 를 갖되 old/new 의 target·reference SHA 를 **넷 다** 다르게 두면
    과학 숫자·control·env·run id 가 같다는 이유로 rc 0 · `promotion_eligible: true` 였다 — `ROW_SKIP` 이 입력
    identity 를 대조에서 빼기 때문이다.

    닫힘 조건: 양쪽 receipt 를 `{역할: sha256}` 로 정규화해 대조하고, 하나라도 다르면 숫자 비교 전에 막는다."""
    old, new = tmp_path / "old", tmp_path / "new"
    _matrix_unit(old, "same-run-id", "bytes-A", "bytes-A")
    _matrix_unit(new, "same-run-id", "bytes-B", "bytes-B")
    rc, out, _ = _cli("check_u14.py", "--new", new, "--old", old)
    assert rc == 2, (rc, out[-600:])
    p = _promotion(out)
    assert p and p["promotion_eligible"] is False and p["blocked_by"].get("inputs"), p
    assert "입력" in out and ("half_cell" in out or "full_cell" in out), out[-800:]
    # 대조군: 같은 입력 bytes 면 통과한다
    # ⚠ 자체 리뷰 C02 뒤: **독립 실행이면 run id 가 달라야 한다** (같으면 같은 시도의 사본이라 alias 다).
    #   전 판 fixture 는 양쪽에 같은 `"r"` 을 줘서 그 축을 구조적으로 못 쟀다.
    old2, new2 = tmp_path / "o2", tmp_path / "n2"
    _matrix_unit(old2, "r-old", "same", "same"); _matrix_unit(new2, "r-new", "same", "same")
    rc, out, _ = _cli("check_u14.py", "--new", new2, "--old", old2)
    assert rc == 0 and _promotion(out)["promotion_eligible"] is True, (rc, out[-500:])


# ── P1-2 ─────────────────────────────────────────────────────────────────────────────────────
class _Obj:
    scale_audit = None
    c_cell = 1.0
    n_scale_samples = 50

    def __init__(self):
        self.consumed_inputs, self.inputs_sha = _rec("fixture")
        self.scales = {"pocv": 1.0, "dvdq": 1.0, "dqdv": 1.0}

    def __call__(self, _p): return 1.0
    def rmse_pocv(self, _p): return 1.0
    def _auto_scales(self, *a, **k): return dict(self.scales)


def _matrix_args(t, out, **kw):
    a = SimpleNamespace(data_root=str(t), state="100", source="GITT", only_source=False, only_wdqdv=False,
                        w_dqdv=0.0, seed=0, starts=0, out=str(out), run_id="r11-matrix")
    for k, v in kw.items():
        setattr(a, k, v)
    return a


def _patch_matrix(monkeypatch, tmp_path):
    class Exists:
        def is_file(self): return True
    monkeypatch.setattr(verify.D, "data_root", lambda *a, **k: tmp_path)
    monkeypatch.setattr(verify.D, "half_cell_path", lambda *a, **k: Exists())
    monkeypatch.setattr(verify, "build", lambda *a, **k: _Obj())
    monkeypatch.setattr(verify, "multistart", lambda *a, **k: (np.array([1.0, 0.0, 1.0, 0.0, 0.2]), 1.0, []))
    monkeypatch.setattr(verify, "degradation_modes", lambda *a, **k: {"LAM_PE": 0.1, "LAM_NE": 0.2, "LLI": 0.3})
    monkeypatch.setattr(verify, "active_bounds", lambda _p: [])


def test_e11_02_matrix_diagnostic_axes_cannot_claim_complete(tmp_path, monkeypatch):
    """[Codex R11 P1-2 · P1] 정본 authority 는 `2 소스 × 8 Si × 2 가중 = 32` 인데 `--only-source --only-wdqdv` 가 8 개만
    돌고 그것을 `complete` · canonical · rc 0 으로 게시했다 (독립 fixture 에서는 8 → 2 canonical 교체도 재현됐다).

    닫힘 조건: canonical roster 를 **옵션 적용 전에** 고정한다. 진단 selector 가 authority 를 하나라도 줄이면
    `subset` · rc 3 · partial namespace 다."""
    art = tmp_path / "matrix_100.csv"
    _patch_matrix(monkeypatch, tmp_path)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc_full = verify.cmd_matrix(_matrix_args(tmp_path, art))
    assert rc_full == 0 and art.is_file(), (rc_full, buf.getvalue()[-400:])
    full_bytes = art.read_bytes()

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = verify.cmd_matrix(_matrix_args(tmp_path, art, only_source=True, only_wdqdv=True))
    text = buf.getvalue()
    assert rc == 3, (rc, text[-500:])
    assert art.read_bytes() == full_bytes, "축소한 진단 실행이 complete canonical 을 덮었다"
    # ⚠ R16 (조건 8 축 ④): 부분은 `partial/<종류>/<attempt-id>/` 로 간다 — 평면 자리는 더 이상 없다.
    #   index 에서 찾는다 (그것이 index 가 있는 이유다).
    part = verify.latest_partial(art) or (art.parent / "partial" / art.name)
    assert part.is_file() and "subset" in text, text[-500:]
    rows = list(csv.DictReader(io.StringIO(part.read_text(encoding="utf-8"))))
    assert len(rows) == 8 < 32


# ── P1-3 ─────────────────────────────────────────────────────────────────────────────────────
def _profile_args(t, out, grid):
    return SimpleNamespace(data_root=str(t), source="GITT", state="100", si_source="Li", w_dqdv=0.0,
                           seed=0, starts=0, grid=grid, profile_scale="global", tol=0.01,
                           out=str(out), run_id="r11-profile")


def test_e11_03_profile_grid_must_match_the_canonical_gamma_grid(tmp_path, monkeypatch):
    """[Codex R11 P1-3 · P1] `--grid 1` 이 γ 한 점만 계산하고 `requested:1, succeeded:1 · status complete · canonical ·
    rc 0` 을 냈다 (모든 span 은 당연히 0.0). production canonical grid 는 21 점이다.

    닫힘 조건: exact γ 값과 개수를 담은 canonical grid 를 계약에 고정하고, 다른 `--grid` 는 subset · rc 3 · partial."""
    art = tmp_path / "profile_gamma_100_Li.csv"
    monkeypatch.setattr(verify.D, "data_root", lambda *a, **k: tmp_path)
    monkeypatch.setattr(verify, "build", lambda *a, **k: _Obj())
    monkeypatch.setattr(verify, "multistart", lambda *a, **k: (np.array([1.0, 0.0, 1.0, 0.0, 0.2]), 1.0, []))
    monkeypatch.setattr(verify, "degradation_modes", lambda *a, **k: {"LAM_PE": 0.1, "LAM_NE": 0.2, "LLI": 0.3})
    monkeypatch.setattr(verify, "minimize",
                        lambda *a, **k: SimpleNamespace(success=True, fun=1.0, x=np.array([1.0, 0.0, 1.0, 0.0])))
    assert S.CANONICAL_GAMMA_GRID_N == 21, S.CANONICAL_GAMMA_GRID_N
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = verify.cmd_profile(_profile_args(tmp_path, art, grid=1))
    text = buf.getvalue()
    assert rc == 3 and not art.is_file(), (rc, text[-500:])
    # ⚠ R16 (조건 8 축 ④): 부분은 `partial/<종류>/<attempt-id>/` 로 간다 — 평면 자리는 더 이상 없다.
    #   index 에서 찾는다 (그것이 index 가 있는 이유다).
    part = verify.latest_partial(art) or (art.parent / "partial" / art.name)
    assert part.is_file() and "subset" in text, text[-500:]
    rows = list(csv.DictReader(io.StringIO(part.read_text(encoding="utf-8"))))
    roster = json.loads(rows[0]["gamma_roster"])
    assert roster["authority"] == 21 and roster["requested"] == 1, roster
    buf = io.StringIO()                                                    # 대조군: 정본 격자는 canonical
    with contextlib.redirect_stdout(buf):
        rc = verify.cmd_profile(_profile_args(tmp_path, art, grid=21))
    assert rc == 0 and art.is_file(), (rc, buf.getvalue()[-400:])


# ── P1-4 ─────────────────────────────────────────────────────────────────────────────────────
def test_e11_04_a_declared_absence_that_exists_is_a_hard_failure(tmp_path, monkeypatch):
    """[Codex R11 P1-4 · P1] `GITT/300_0147.xlsx` 가 실제로 있는데 `HALF_CELL_ABSENT` 가 GITT 를 먼저 지워 32 개가 아니라
    step-only 16 개를 `complete` · canonical · rc 0 으로 게시했다 — 오래된 부재 선언이 **생긴 측정을 조용히 숨긴다**.

    닫힘 조건: 부재 선언과 실제 파일이 모순되면 invalid rc 2 로 실패한다."""
    art = tmp_path / "matrix_300_0147.csv"
    _patch_matrix(monkeypatch, tmp_path)                                   # 모든 반쪽전지 파일이 존재한다고 본다
    assert ("GITT", "300_0147") in D.HALF_CELL_ABSENT
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        rc = verify.cmd_matrix(_matrix_args(tmp_path, art, state="300_0147"))
    text = buf.getvalue()
    assert rc == 2, (rc, text[-600:])
    assert not art.is_file(), "부재 선언과 모순되는 상태로 canonical 을 썼다"
    assert "300_0147" in text and ("부재" in text or "선언" in text), text[-600:]


# ── P1-5 ─────────────────────────────────────────────────────────────────────────────────────
def test_e11_05_paired_artifacts_that_are_the_same_inode_are_not_independent(tmp_path):
    """[Codex R11 P1-5 · P1] 디렉터리는 `samefile: false` 인데 data·meta 파일 각각이 hardlink 라 같은 inode 였다 —
    비교는 rc 0 · `promotion_eligible: true`.

    닫힘 조건: 짝지은 data/meta object 마다 samefile/hardlink/symlink 별칭을 거부한다."""
    old, new = tmp_path / "old", tmp_path / "new"
    f_old = _matrix_unit(old, "alias")
    new.mkdir(parents=True, exist_ok=True)
    f_new = new / f_old.name
    os.link(f_old, f_new)
    os.link(f_old.with_name(f_old.name + ".meta.json"), f_new.with_name(f_new.name + ".meta.json"))
    assert not os.path.samefile(new, old) and os.path.samefile(f_new, f_old)
    rc, out, _ = _cli("check_u14.py", "--new", new, "--old", old)
    assert rc == 2 and "전부 같다" not in out, (rc, out[-600:])
    assert "같은" in out or "alias" in out or "hardlink" in out, out[-600:]
    assert _promotion(out)["promotion_eligible"] is False


# ── P1-6 ─────────────────────────────────────────────────────────────────────────────────────
def test_e11_06_schema_only_is_never_a_promotion_certificate(tmp_path):
    """[Codex R11 P1-6 · P1] baseline 이 `null`, roster 0, compared 0 인데 rc 0 과 `promotion_eligible: true` 였다.
    schema-only 에서는 env·control·argv·roster 도 건너뛰었다.

    닫힘 조건: schema-only 는 **구조상 언제나** `promotion_eligible: false` 이고, 그래도 exact schema 검증은 한다
    (`baseline_absent` 를 명시적 blocker 로)."""
    d = tmp_path / "unit"
    _matrix_unit(d, "schema-only")
    rc, out, _ = _cli("check_u14.py", "--new", d, "--schema-only")
    p = _promotion(out)
    assert p["promotion_eligible"] is False and p["blocked_by"].get("baseline_absent"), p
    assert rc == 0, (rc, out[-400:])                                       # 스키마 자체는 통과 (진단은 유효하다)
    # control·argv·roster 는 schema-only 에서도 필수다
    m = (d / "matrix_100.csv.meta.json")
    meta = json.loads(m.read_text(encoding="utf-8"))
    for k in ("state", "starts", "argv", "roster"):
        meta.pop(k, None)
    meta["env"] = {}
    m.write_text(json.dumps(meta), encoding="utf-8")
    rc, out, _ = _cli("check_u14.py", "--new", d, "--schema-only")
    assert rc == 2, (rc, out[-600:])
    assert "argv" in out and "roster" in out and "starts" in out, out[-800:]


# ── P1-7 ─────────────────────────────────────────────────────────────────────────────────────
def test_e11_07_the_shape_reader_refuses_units_the_shared_validator_rejects(tmp_path):
    """[Codex R11 P1-7 · P1] `error="optimizer failed"` 인 서명 행을 `S.check_rows` 는 실패로 판정하는데
    `fitted_pair_info` 는 그 행의 `(0.4, 0.2)` 를 정상 과학 입력으로 돌려줬다.

    닫힘 조건: production reader 가 exact header 와 shared validator 를 통과한 묶음만 고른다."""
    ns = _shape_harness.__globals__["_load_script"]("ne_shape")
    d = tmp_path / "out"; d.mkdir()
    ci, dg = _rec("reader")
    rows = _full_matrix_rows("reader-r11")
    for r in rows:
        r["consumed_inputs"] = r["ref_consumed_inputs"] = json.dumps(ci)
        r["inputs_sha"] = r["ref_inputs_sha"] = dg
    rows[0].update(gamma_Si="0.4", ref_gamma_Si="0.2", error="optimizer failed")
    f = d / "matrix_100.csv"
    verify.atomic_write_csv(f, rows, [*S.MATRIX_ROW, "error"])
    _sign(f, "reader-r11", "100")
    assert S.check_rows("matrix", rows, [*S.MATRIX_ROW, "error"]), "shared validator 는 이미 거부한다"
    with pytest.raises(RuntimeError, match="error|스키마|검증"):
        ns.fitted_pair_info(d, "100", "GITT", "Li")


# ── P1-8 ─────────────────────────────────────────────────────────────────────────────────────
def test_e11_08_non_finite_science_values_are_never_valid(tmp_path):
    """[Codex R11 P1-8 · P1] matrix `obj=inf` · degeneracy `best_obj=Infinity` · profile `a_NE="not-a-number"` 가
    스키마 문제 0 · 숫자 차이 0 · rc 0 · promotion true 였다 (`float()` 이 inf 를 받고 `inf == inf` 라서).

    닫힘 조건: 과학 스칼라에 `math.isfinite` 를 걸고 JSON 은 NaN/Infinity 를 거부한다 — producer 와 consumer 가 같은 검사."""
    rows = _full_matrix_rows("inf")
    ci, dg = _rec("inf")
    for r in rows:
        r["consumed_inputs"] = r["ref_consumed_inputs"] = json.dumps(ci)
        r["inputs_sha"] = r["ref_inputs_sha"] = dg
    rows[0]["obj"] = "inf"
    probs = S.check_rows("matrix", rows, list(S.MATRIX_ROW))
    assert probs and any("유한" in p or "finite" in p or "inf" in p for p in probs), probs
    rows[0]["obj"] = "nan"
    assert S.check_rows("matrix", rows, list(S.MATRIX_ROW)), "nan 도 과학 값이 아니다"
    prof = {k: "1.0" for k in S.PROFILE_ROW}
    prof.update(consumed_inputs=json.dumps(ci), ref_consumed_inputs=json.dumps(ci), inputs_sha=dg,
                ref_inputs_sha=dg, bounds="-", run_id="p", profile_scale="global",
                gamma_roster=json.dumps({"authority": 21, "requested": 21, "succeeded": 21, "missing": []}),
                a_NE="not-a-number")
    assert S.check_rows("profile", [prof], list(S.PROFILE_ROW)), "숫자가 아닌 셀"
    # degeneracy JSON 은 Infinity 를 담을 수 없다 — producer 도 consumer 도
    j = {k: 1 for k in S.DEGENERACY_KEYS}
    j.update(consumed_inputs=ci, ref_consumed_inputs=ci, inputs_sha=dg, best_obj=float("inf"))
    assert any("유한" in p or "finite" in p for p in S.check_degeneracy(j)), S.check_degeneracy(j)
    with pytest.raises(ValueError):
        verify.atomic_write_json(tmp_path / "x.json", {"a": float("inf")})


# ── P1-9 ─────────────────────────────────────────────────────────────────────────────────────
def test_e11_09_unsafe_provenance_blocks_promotion_and_untracked_code_is_visible(tmp_path):
    """[Codex R11 P1-9 · P1] candidate 가 `git_dirty: true` · 바뀐 `verify.py` · bogus start commit ·
    `git_state_changed_during_run: true` 를 **명시해도** rc 0 · promotion true 였고, untracked 저장소 루트
    `sitecustomize.py` 는 실제로 실행되는데 provenance 는 `git_dirty: false` 를 적었다.

    닫힘 조건: 승격은 safe 값 자체를 강제하고, 산출 root 밖의 untracked importable/executable 은 code dirtiness 다."""
    old, new = tmp_path / "old", tmp_path / "new"
    _matrix_unit(old, "prov")
    f = _matrix_unit(new, "prov")
    m = f.with_name(f.name + ".meta.json")
    meta = json.loads(m.read_text(encoding="utf-8"))
    meta.update(git_dirty=True, git_modified_code=["bms_balancing/verify.py"],
                git_commit_at_start="attacker-commit", git_state_changed_during_run=True)
    m.write_text(json.dumps(meta), encoding="utf-8")
    rc, out, _ = _cli("check_u14.py", "--new", new, "--old", old)
    assert rc == 2, (rc, out[-600:])
    p = _promotion(out)
    assert p["promotion_eligible"] is False and p["blocked_by"].get("provenance"), p
    assert "git_dirty" in out or "더러" in out, out[-700:]

    repo = tmp_path / "repo"
    _fixture_repo(repo, outputs=())
    (repo / "sitecustomize.py").write_text("MARKER = 1\n", encoding="utf-8")   # untracked · importable
    prov = {}
    exec(compile((ROOT / "scripts/provenance.py").read_text(encoding="utf-8"), "provenance", "exec"), prov)
    got = prov["git_provenance"](cwd=str(repo), output_roots=("out",))
    assert got["git_dirty"] is True and any("sitecustomize" in x for x in got["git_modified_code"]), got


# ── P1-10 ────────────────────────────────────────────────────────────────────────────────────
def _runner(name):
    return ROOT / {"r7": "reviews/r7_repros/replay_codex_r7.py",
                   "r9": "reviews/r9_repros/replay_codex_r9.py",
                   "r10": "reviews/r10_repros/replay_codex_r10.py"}[name]


def _head():
    return subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()


def _run_runner(name, *extra, env=None, timeout=1800):
    e = dict(os.environ); e.update(env or {})
    e.pop("PYTHONPYCACHEPREFIX", None)
    r = subprocess.run([sys.executable, str(_runner(name)), "--target", str(ROOT),
                        "--expected-head", _head(), *extra], cwd=ROOT, capture_output=True,
                       text=True, timeout=timeout, env=e)
    return r.returncode, r.stdout, r.stderr


def test_e11_10_the_gate_is_isolated_before_it_is_imported_and_the_snapshot_bytes_are_checked(tmp_path):
    """[Codex R11 P1-10 · P1] (A) timestamp/size 가 맞는 ignored `reviews/__pycache__/evidence_gate…pyc` 가 source 보다
    **먼저** load 돼 marker 를 실행했는데 `instrument_sealed`·`evidence_eligible`·`closed` 가 전부 true 였다.
    (B) committed `.gitattributes` + smudge driver 가 materialize 된 `verify.py` bytes 를 바꿔도 같았다.

    닫힘 조건: gate import **전에** bytecode 를 격리하고, materialize 한 트리의 tracked object 를 expected tree 의 blob
    bytes 와 다시 대조한다."""
    import importlib.util
    from importlib import _bootstrap_external as be
    src = ROOT / "reviews/evidence_gate.py"
    pyc = pathlib.Path(importlib.util.cache_from_source(str(src)))
    marker = tmp_path / "gate-pyc-executed"
    backup = pyc.read_bytes() if pyc.exists() else None
    st = src.stat()
    pyc.parent.mkdir(parents=True, exist_ok=True)
    altered = src.read_text(encoding="utf-8") + f"\npathlib.Path({str(marker)!r}).write_text('x', encoding='utf-8')\n"
    pyc.write_bytes(be._code_to_timestamp_pyc(compile(altered, str(src), "exec"), int(st.st_mtime), st.st_size))
    try:
        rc, out, err = _run_runner("r7", "--probes", "R7-06", "--allow-dirty",
                                   env={"PYTHONDONTWRITEBYTECODE": "1"})
        assert not marker.is_file(), "gate 의 위조 bytecode 가 import 전에 격리되지 않았다"
    finally:
        pyc.unlink(missing_ok=True)
        if backup is not None:
            pyc.write_bytes(backup)
    # (B) snapshot 의 bytes 를 blob 과 대조하는 검증기가 있다 — 한 파일을 바꾸면 잡는다
    sys.path.insert(0, str(ROOT / "reviews"))
    import evidence_gate as gate
    snap, cleanup = gate.materialize(ROOT, _head())
    try:
        assert gate.verify_snapshot_bytes(snap, _head()) == []
        victim = snap / "bms_balancing" / "verify.py"
        victim.write_text(victim.read_text(encoding="utf-8") + "\n# smudged\n", encoding="utf-8")
        bad = gate.verify_snapshot_bytes(snap, _head())
        assert bad and any("verify.py" in b for b in bad), bad
    finally:
        cleanup()


# ── P1-11 ────────────────────────────────────────────────────────────────────────────────────
def test_e11_11_the_r10_parent_requires_child_exit_zero(tmp_path):
    """[Codex R11 P1-11 · P1] checksum 에 든 child 일곱 개의 직접 rc 가 7 이었는데 기대 boolean 만 찍자 parent 가 rc 0 ·
    22-case closed · `evidence_eligible: true` 를 냈다.

    닫힘 조건: payload 를 parse 하기 **전에** child rc 0 을 강제하고, timeout/signal/nonzero/누락/초과는 unresolved 다."""
    src = (_runner("r10")).read_text(encoding="utf-8")
    assert "proc.returncode" in src, "child rc 를 보지 않는다"
    ns = {"__file__": str(_runner("r10"))}
    exec(compile(src.split("def main(")[0], str(_runner("r10")), "exec"), ns)
    # 러너가 child 결과를 받아들이는 술어를 직접 부른다
    assert "child_ok" in ns, "child rc 판정을 함수로 꺼내지 않았다"
    assert ns["child_ok"](SimpleNamespace(returncode=0, stdout='{"cases": {}}', stderr="")) is True
    for rc in (1, 2, 7, -9):
        assert ns["child_ok"](SimpleNamespace(returncode=rc, stdout='{"cases": {}}', stderr="")) is False, rc


# ── P1-12 ────────────────────────────────────────────────────────────────────────────────────
def test_e11_12_the_r10_classifier_requires_the_case_s_own_counterexample(tmp_path):
    """[Codex R11 P1-12 · P1] `schema.inputs_digest` 가 `AssertionError("UNRELATED production invariant")` 를 내게 하자
    parent 가 `도달: true · 상태: 반례 소멸` 로 기록했다 — 아무 assertion 이나 닫힘으로 읽었다.

    닫힘 조건: case 마다 기대하는 반례 assertion 의 fingerprint 를 봉인하고 그 밖의 예외는 오류다."""
    src = (_runner("r10")).read_text(encoding="utf-8")
    ns = {"__file__": str(_runner("r10"))}
    exec(compile(src.split("def main(")[0], str(_runner("r10")), "exec"), ns)
    assert "COUNTEREXAMPLE_LINES" in ns and ns["COUNTEREXAMPLE_LINES"], "case 별 fingerprint 가 없다"

    def unrelated():
        raise AssertionError("UNRELATED production invariant")

    rec = ns["_classify"](unrelated, ROOT / "reviews/r10_repros/codex", "snapshot:receipt-roles")
    assert rec["상태"] == "오류", rec


# ── P2-1 ─────────────────────────────────────────────────────────────────────────────────────
def test_e11_13_profile_partial_returns_three_even_without_a_sink(tmp_path, monkeypatch):
    """[Codex R11 P2-1 · P2] `out=None` 이면 summary 는 `partial`·roster 1/2 인데 rc 가 0 이었다 — sink 유무가 semantic
    status 를 바꾼다.

    닫힘 조건: semantic status 에서 rc 를 먼저 정하고 sink 처리 뒤 공통 return."""
    monkeypatch.setattr(verify.D, "data_root", lambda *a, **k: tmp_path)
    monkeypatch.setattr(verify, "build", lambda *a, **k: _Obj())
    monkeypatch.setattr(verify, "multistart", lambda *a, **k: (np.array([1.0, 0.0, 1.0, 0.0, 0.2]), 1.0, []))
    monkeypatch.setattr(verify, "degradation_modes", lambda *a, **k: {"LAM_PE": 0.1, "LAM_NE": 0.2, "LLI": 0.3})
    calls = {"n": 0}

    def half(_f, _s, **_k):
        calls["n"] += 1
        return SimpleNamespace(success=calls["n"] == 1, fun=1.0, x=np.array([1.0, 0.0, 1.0, 0.0]))

    monkeypatch.setattr(verify, "minimize", half)
    a = _profile_args(tmp_path, tmp_path / "p.csv", grid=S.CANONICAL_GAMMA_GRID_N)
    a.out = None
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = verify.cmd_profile(a)
    assert rc == 3, (rc, buf.getvalue()[-400:])


# ── P2-2 ─────────────────────────────────────────────────────────────────────────────────────
def test_e11_14_shape_step_reads_the_artifact_it_just_wrote_and_partial_is_not_success(tmp_path):
    """[Codex R11 P2-2 · P2] stale canonical 과 fresh partial 이 함께 있으면 wildcard `ls | head -1` 이 **stale** status 를
    골랐고, 실제 rc 3 도 바깥 wrapper 의 실패 수를 안 늘려 "전부 통과" rc 0 이 됐다. rc 0 + meta partial 인 shim 도
    "complete" 로 찍혔다.

    닫힘 조건: producer 가 `SHAPE_RESULT {…}` 로 **자기가 쓴 경로·run_id·status** 를 말하고 wrapper 가
    `rc ↔ status ↔ namespace ↔ run_id` 를 대조한다. partial 은 top-level 성공으로 세탁되지 않는다."""
    d = tmp_path / "w"
    (d / "partial").mkdir(parents=True)
    # 옆에 놓인 **stale canonical** — 이번 시도의 산출이 아니다. 어떤 경로로도 이것을 읽으면 안 된다.
    (d / "ne_shape_A_Li.csv").write_text("state,run_id\n100,stale\n", encoding="utf-8")
    (d / "ne_shape_A_Li.csv.meta.json").write_text(json.dumps(
        {"status": "complete", "run_id": "stale", "artifact": "ne_shape_A_Li.csv",
         "sha256": hashlib.sha256((d / "ne_shape_A_Li.csv").read_bytes()).hexdigest()}), encoding="utf-8")

    def _shim(name, rc, result, art=None, status=None):
        """producer 흉내 — **실행 시점에** 자기 산출과 사이드카를 쓰고 `SHAPE_RESULT` 를 찍는다.

        ⚠ 자체 리뷰 C15 뒤: `shape_step` 이 이번 시도의 `BMS_RUN_ID` 를 주입하고 다른 세 단계처럼 묶음 검사를
          건다. 진짜 producer(`ne_shape._write_csv`)가 그 환경값을 쓰므로 shim 도 같게 해야 그 축을 잰다 —
          전 판 shim 은 테스트가 미리 써 둔 `state\n100\n` 이라 구조적으로 못 쟀다.
        """
        f = tmp_path / name
        f.write_text(
            "import hashlib, json, os, pathlib, sys\n"
            f"art = pathlib.Path({str(art)!r}) if {art is not None!r} else None\n"
            "rid = os.environ.get('BMS_RUN_ID', '')\n"
            "if art is not None:\n"
            "    art.parent.mkdir(parents=True, exist_ok=True)\n"
            "    art.write_text(f'state,run_id\\n100,{rid}\\n', encoding='utf-8')\n"
            f"    meta = {{'status': {status!r}, 'run_id': rid, 'artifact': art.name,\n"
            "            'sha256': hashlib.sha256(art.read_bytes()).hexdigest()}\n"
            "    art.with_name(art.name + '.meta.json').write_text(json.dumps(meta), encoding='utf-8')\n"
            f"r = dict({result!r})\n"
            "r['run_id'] = rid or r.get('run_id')\n"
            "print('SHAPE_RESULT ' + json.dumps(r, ensure_ascii=False))\n"
            f"sys.exit({rc})\n", encoding="utf-8")
        return f

    # (1) 정직한 partial: rc 3 · status partial · partial/ 네임스페이스 · run_id 일치 → STEP_RC=3, 모순 없음
    fresh = d / "partial" / "ne_shape_GITT_Li.csv"
    ok = _shim("ok.py", 3, {"status": "partial", "artifact": str(fresh),
                            "authority": 2, "requested": 2, "paired": 1},
               art=fresh, status="partial")
    p = _shell(f'shape_step "{d}" python3 {ok}; echo "STEP_RC=$?"', {"OUT": str(d)})
    text = p.stdout + p.stderr
    assert "STEP_RC=3" in text, text[-800:]
    assert "부분(partial)" in text, text[-800:]
    assert "ne_shape_A_Li" not in text, "stale canonical 을 읽었다:\n" + text[-800:]

    # (2) rc 0 인데 status 는 partial — 모순이다 (전 판은 "complete" 로 찍었다)
    lie = _shim("lie.py", 0, {"status": "partial", "artifact": str(fresh)}, art=fresh, status="partial")
    p = _shell(f'shape_step "{d}" python3 {lie}; echo "STEP_RC=$?"', {"OUT": str(d)})
    text = p.stdout + p.stderr
    assert "STEP_RC=0" not in text, text[-800:]
    assert "모순" in text, text[-800:]

    # (3) rc 3 인데 아무것도 안 찍는다 — 무엇을 읽을지 모르니 넘기지 않는다 (전 판은 wildcard 로 훑었다)
    mute = tmp_path / "mute.py"; mute.write_text("import sys; sys.exit(3)\n", encoding="utf-8")
    p = _shell(f'shape_step "{d}" python3 {mute}; echo "STEP_RC=$?"', {"OUT": str(d)})
    text = p.stdout + p.stderr
    assert "STEP_RC=3" not in text and "STEP_RC=0" not in text, text[-800:]
    assert "SHAPE_RESULT" in text, text[-800:]

    # (4) rc 0 인데 canonical 이 아니라 partial/ 을 가리킨다 — namespace 모순
    ns = _shim("ns.py", 0, {"status": "complete", "artifact": str(fresh)}, art=fresh, status="complete")
    p = _shell(f'shape_step "{d}" python3 {ns}; echo "STEP_RC=$?"', {"OUT": str(d)})
    text = p.stdout + p.stderr
    assert "STEP_RC=0" not in text and "모순" in text, text[-800:]

    # (5) meta 의 run_id 가 보고한 것과 다르면 — 이번 시도의 산출이 아니다
    other = d / "partial" / "ne_shape_GITT_other.csv"
    # meta 의 run_id 가 보고한 것과 다르면 — 이번 시도의 산출이 아니다 (shim 이 일부러 어긋나게 쓴다)
    rid = tmp_path / "rid.py"
    rid.write_text(
        "import hashlib, json, os, pathlib, sys\n"
        f"art = pathlib.Path({str(other)!r})\n"
        "art.parent.mkdir(parents=True, exist_ok=True)\n"
        "art.write_text('state,run_id\\n100,다른-시도\\n', encoding='utf-8')\n"
        "meta = {'status': 'partial', 'run_id': '다른-시도', 'artifact': art.name,\n"
        "        'sha256': hashlib.sha256(art.read_bytes()).hexdigest()}\n"
        "art.with_name(art.name + '.meta.json').write_text(json.dumps(meta), encoding='utf-8')\n"
        "print('SHAPE_RESULT ' + json.dumps({'status': 'partial', 'artifact': str(art),\n"
        "                                    'run_id': os.environ.get('BMS_RUN_ID', '')}, ensure_ascii=False))\n"
        "sys.exit(3)\n", encoding="utf-8")
    p = _shell(f'shape_step "{d}" python3 {rid}; echo "STEP_RC=$?"', {"OUT": str(d)})
    text = p.stdout + p.stderr
    assert "STEP_RC=3" not in text and "run_id" in text, text[-800:]

    # 바깥 wrapper: partial 은 전체 성공으로 바뀌지 않는다
    src = (ROOT / "scripts/run_states.sh").read_text(encoding="utf-8")
    tail = src[src.index("shape_rc=0"):]
    assert "partial=$((partial+1))" in tail, tail[:600]
    assert 'if [ "$fail" -eq 0 ] && [ "${partial:-0}" -eq 0 ]; then' in tail, tail[:900]
    assert "partial:-0} > 0 ? 3 : 0" in tail, tail[-400:]


# ── P2-3 ─────────────────────────────────────────────────────────────────────────────────────
def test_e11_15_receipt_roles_are_an_exact_typed_tree(tmp_path):
    """[Codex R11 P2-3 · P2] nested `literature.gr` 와 top-level dotted `"literature.gr"` 를 **다른 SHA 로** 함께 둬도
    validator 가 문제 0 을 냈다 (역할 검사가 set 이라 cardinality 를 안 본다).

    닫힘 조건: exact typed tree 하나만 허용하고 flatten 전에 unknown·nonleaf·중복 논리 역할을 거부한다."""
    good, dg = _rec("ok")
    dup = json.loads(json.dumps(good))
    dup["literature.gr"] = {"path": "conflicting/direct-gr.xlsx", "sha256": "f" * 64}
    probs = S.validate_receipt(dup, S.inputs_digest(dup), "dup")
    assert probs and any("중복" in p or "duplicate" in p or "literature.gr" in p for p in probs), probs
    # 경로만 바꿔치기한 receipt 는 digest 가 같아도 **역할별 path** 가 다르다는 것을 말한다
    swapped = json.loads(json.dumps(good))
    swapped["full_cell"]["path"], swapped["half_cell"]["path"] = (swapped["half_cell"]["path"],
                                                                  swapped["full_cell"]["path"])
    assert S.receipt_map(good) != S.receipt_map(swapped) or S.receipt_paths(good) != S.receipt_paths(swapped)


# ── P2-4 ─────────────────────────────────────────────────────────────────────────────────────
def test_e11_16_gamma_roster_is_parsed_not_just_non_empty(tmp_path):
    """[Codex R11 P2-4 · P2] 유효한 profile 행의 `gamma_roster="not-json"` 이 문제 없이 통과했다 (비어 있지만 않으면 됐다).

    닫힘 조건: roster 를 exact JSON schema 로 parse 하고 행마다 같은지, 산술이 맞는지 본다."""
    ci, dg = _rec("roster")
    base = {k: "1.0" for k in S.PROFILE_ROW}
    base.update(consumed_inputs=json.dumps(ci), ref_consumed_inputs=json.dumps(ci), inputs_sha=dg,
                ref_inputs_sha=dg, bounds="-", run_id="p", profile_scale="global")
    # ⚠ 자체 리뷰 C04 뒤: roster 는 **본문과 묶인다** — 성공 수 = 행 수여야 하므로 전수 fixture 는 21 행이다
    #   (전 판은 1 행에 "21 성공" 을 적어 두고 통과했고, 그 사실이 이 시험에 가려져 있었다).
    n = S.CANONICAL_GAMMA_GRID_N
    full = json.dumps({"authority": n, "requested": n, "succeeded": n, "missing": []})
    # ⚠ Codex R13 P1-1: 전 판은 `i/(n-1)` = 0~1 이었다 (정본은 0~0.5).
    rows_ok = [dict(base, gamma_Si=repr(g), gamma_roster=full) for g in S.canonical_gamma_grid()]
    assert not S.check_rows("profile", rows_ok, list(S.PROFILE_ROW)), S.check_rows("profile", rows_ok, list(S.PROFILE_ROW))
    bad = [dict(r, gamma_roster="not-json") for r in rows_ok]
    assert S.check_rows("profile", bad, list(S.PROFILE_ROW)), "JSON 이 아닌 roster 를 통과시켰다"
    wrong = [dict(r, gamma_roster=json.dumps({"authority": n, "requested": n, "succeeded": 5, "missing": []}))
             for r in rows_ok]
    assert S.check_rows("profile", wrong, list(S.PROFILE_ROW)), "산술이 안 맞는 roster 를 통과시켰다"
    mixed = list(rows_ok)
    mixed[0] = dict(mixed[0], gamma_roster=json.dumps({"authority": n, "requested": n, "succeeded": n - 1,
                                                       "missing": [0.1]}))
    assert S.check_rows("profile", mixed, list(S.PROFILE_ROW)), "행마다 다른 roster 를 통과시켰다"


# ── P2-5 ─────────────────────────────────────────────────────────────────────────────────────
def test_e11_17_skip_worktree_is_detected(tmp_path):
    """[Codex R11 P2-5 · P2] git 은 `S reviews/evidence_gate.py` 를 찍는데 `index_skip_flags()` 는 빈 목록이었다 —
    소문자만 봤다. R7 러너는 rc 0 · eligible/closed true 였다."""
    sys.path.insert(0, str(ROOT / "reviews"))
    import evidence_gate as gate
    rel = "bms_balancing/schema.py"
    subprocess.run(["git", "-C", str(ROOT), "update-index", "--skip-worktree", rel], check=True)
    try:
        flags = gate.index_skip_flags(ROOT)
        assert any(rel in f for f in flags), flags
        rc, out, err = _run_runner("r7", "--probes", "R7-06", "--allow-dirty")
        assert rc != 0 and "skip" in (out + err).lower(), (rc, err[-300:])
    finally:
        subprocess.run(["git", "-C", str(ROOT), "update-index", "--no-skip-worktree", rel], check=True)


# ── P2-6 ─────────────────────────────────────────────────────────────────────────────────────
def test_e11_18_expected_head_must_be_the_full_object_id():
    """[Codex R11 P2-6 · P2] 7 자 prefix `2add074` 만 넘겨도 rc 0 이었고 그 짧은 값이 expected head 로 기록됐다.

    닫힘 조건: full canonical object id 로 resolve 해 exact 비교하고 tree id 까지 기록한다."""
    head = _head()
    for name in ("r7", "r9", "r10"):
        e = dict(os.environ); e.pop("PYTHONPYCACHEPREFIX", None)
        r = subprocess.run([sys.executable, str(_runner(name)), "--target", str(ROOT),
                            "--expected-head", head[:7], "--probes", "R7-06" if name == "r7" else "P2-3",
                            "--allow-dirty"] if name != "r10" else
                           [sys.executable, str(_runner(name)), "--target", str(ROOT),
                            "--expected-head", head[:7], "--allow-dirty"],
                           cwd=ROOT, capture_output=True, text=True, timeout=900, env=e)
        assert r.returncode != 0, (name, r.returncode, r.stdout[:300])
        assert "40" in (r.stdout + r.stderr) or "full" in (r.stdout + r.stderr) or "짧" in (r.stdout + r.stderr), \
            (name, r.stderr[-300:])


# ── 문서 ─────────────────────────────────────────────────────────────────────────────────────
def test_e11_19_docs_record_the_r11_closure():
    led = _live(_doc("reviews/R6_LEDGER.md"))
    assert "Codex R11" in led and "P1-1" in led and "P2-6" in led
    req = _live(_doc("reviews/R12_REQUEST.md"))
    assert "R11" in req and "identity" in req
    ws = _live(_doc("WORKING_STATE.md"))
    assert "11차" in ws and "provenance-incomplete" in ws
