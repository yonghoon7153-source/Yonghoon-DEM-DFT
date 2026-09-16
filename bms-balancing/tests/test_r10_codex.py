"""Codex R10 (2026-09-13, 대상 `bd6ba47`, NO-GO · P1 8 · P2 7) — 반례를 회귀로.

원문·패키지는 `reviews/r10_repros/codex/` (sha256 10/10). 수정 전 HEAD 에서 세 스크립트가 전부 재현됐다
(`reviews/r10_repros/replay_ours_bd6ba47_before/`, clean 트리). R9 가 "모집단을 먼저 세고, 검증 snapshot 만 검사하고,
부분은 부분이라 말한다" 였다면 R10 은 **그 문장이 게시 경계·승격 gate·증거 기계에서도 참인가** — 출력이 비교 근거를
덮지 않는가, 축소된 roster 가 complete 를 참칭하지 않는가, `error` 한 칸이 검증을 끄지 않는가, 증거 러너가 자기가
실행한 bytes 를 봉인하는가.
"""
from __future__ import annotations
import contextlib, csv, hashlib, io, json, os, pathlib, shutil, subprocess, sys
from types import SimpleNamespace

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from conftest import fixture_env as _fixture_env   # noqa: E402  (R16: env 축은 한 자리에서)

import numpy as np                                                        # noqa: E402
import pytest                                                             # noqa: E402
from bms_balancing import schema as S                                     # noqa: E402
from bms_balancing import verify                                          # noqa: E402
from test_r7_codex import _sign, _doc, _live                              # noqa: E402
from test_r8_codex import _mod, _cli, _full_matrix_rows, _shape_harness, _pair   # noqa: E402
from test_r9_codex import _read_shape                                     # noqa: E402


from test_review_findings import audit_json  # noqa: E402


def _receipt(seed="1"):
    d = {"half_cell": {"path": "half.xlsx", "sha256": seed * 64},
         "full_cell": {"path": "full.xlsx", "sha256": "2" * 64},
         "literature": {"gr": {"path": "gr.xlsx", "sha256": "3" * 64},
                        "si": {"path": "si.csv", "sha256": "4" * 64}}}
    return d, S.inputs_digest(d)


def _publish(directory, rows, rid, fields=None):
    directory.mkdir(parents=True, exist_ok=True)
    f = directory / "matrix_100.csv"
    verify.atomic_write_csv(f, rows, fields or list(rows[0]))
    _sign(f, rid, "100", full=True)
    return f


def _shell(script, extra_env=None, defs_only=True):
    """`run_states.sh` 의 **정의부만** 읽어 production 함수를 그대로 부른다 (main loop 는 안 돈다)."""
    text = (ROOT / "scripts/run_states.sh").read_text(encoding="utf-8")
    env = dict(os.environ, STARTS="2", SI="Li", BMS_DATA_ROOT="synthetic",
               PATH=str(pathlib.Path(sys.executable).parent) + os.pathsep + os.environ.get("PATH", ""))
    env.update(extra_env or {})
    begin = text.index("# ══ DEFS BEGIN ══")                             # 전처리(set -u · BASH_SOURCE · cd)는 빼고
    body = text[begin:text.index("\nfail=0")] if defs_only else text
    return subprocess.run(["bash", "-c", body + "\n" + script], cwd=ROOT, env=env,
                          capture_output=True, text=True, timeout=300)


# ── P1-1 ─────────────────────────────────────────────────────────────────────────────────────
class _FakeObj:
    scale_audit = None

    def __init__(self):
        self.consumed_inputs, self.inputs_sha = _receipt()

    def rmse_pocv(self, q): return 1.0 + float(q[0]) / 100.0
    def rmse_dvdq(self, q): return 2.0 + float(q[1]) / 100.0
    def rmse_dqdv(self, q, weighted=True): return (4.0 if weighted else 3.0) + float(q[2]) / 100.0


def _eval_args(t, out, compare):
    return SimpleNamespace(data_root=str(t), source="GITT", state="100", si_source="Li", w_dqdv=0.0,
                           seed=0, out=str(out) if out else None, compare=str(compare) if compare else None,
                           precision="auto", allow_partial=False)


def test_d10_01_eval_never_lets_its_own_output_replace_the_comparison_evidence(tmp_path, monkeypatch):
    """[Codex R10 P1-1 · P1] `--out X --compare X` 에서 `args.out` 이 X 를 **먼저 교체**한 뒤 comparator 가 처음 읽는다 —
    일부러 invalid 로 만든 독립 MATLAB 근거가 사라지고 16/16 앵커·32/32 RMSE 가 `complete` rc 0 이 된다.

    닫힘 조건: `--compare` 가 있으면 **모든 쓰기 전에** snapshot 을 읽고 그 typed snapshot 만 comparator 에 넘긴다.
    경로 문자열이 아니라 같은 object(alias·symlink·hardlink)인지로 판정한다."""
    anchors = [(k, float(i + 1)) for i, (k, _) in enumerate(verify.ANCHOR_STAGE)]
    monkeypatch.setattr(verify.D, "data_root", lambda *a, **k: tmp_path)
    monkeypatch.setattr(verify, "build", lambda *a, **k: _FakeObj())
    monkeypatch.setattr(verify, "dd_eval_anchors", lambda *a, **k: anchors)
    ev = tmp_path / "matlab.csv"
    original = b"THIS IS DELIBERATELY NOT A VALID MATLAB RECEIPT\n"

    def run(out, compare):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            rc = verify.cmd_eval(_eval_args(tmp_path, out, compare))
        return rc, buf.getvalue()

    ev.write_bytes(original)
    rc, text = run(ev, ev)                                                 # 같은 경로
    assert rc != 0 and ev.read_bytes() == original, (rc, text[-400:])
    assert "같은" in text or "alias" in text or "덮" in text, text[-600:]
    link = tmp_path / "alias.csv"
    link.symlink_to(ev)
    rc, text = run(link, ev)                                               # 경로 문자열은 다르지만 같은 object
    assert rc != 0 and ev.read_bytes() == original, (rc, text[-400:])
    # 대조군: 서로 다른 파일이면 돈다 — 그리고 판정은 **쓰기 전** bytes 로 한다 (이 근거 파일은 비교할 것이 없다)
    other = tmp_path / "out.csv"
    rc, text = run(other, ev)
    assert rc == 2 and "종료 코드 2 (empty)" in text, (rc, text[-400:])
    assert ev.read_bytes() == original and other.is_file(), "출력은 따로 써야 한다"
    # 그리고 그 판정은 출력이 아니라 **근거**를 읽은 것이다 — 출력 bytes 는 유효한 eval 산출이다
    assert "dd_eval" in other.read_text(encoding="utf-8").splitlines()[0]


# ── P1-2 ─────────────────────────────────────────────────────────────────────────────────────
def _run_shape(ns, monkeypatch, matrix, out, states=None):
    argv = ["ne_shape.py", "--out-dir", str(matrix), "--write", str(out)]
    if states is not None:
        argv += ["--states", states]
    buf = io.StringIO()
    monkeypatch.setattr(sys, "argv", argv)
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        rc = ns.main()
    return rc, buf.getvalue()


def test_d10_02_ne_shape_states_option_cannot_narrow_the_authority_roster(tmp_path, monkeypatch):
    """[Codex R10 P1-2 · P1] 선언 상태 100·200 의 complete canonical 을 만든 뒤 같은 destination 에 `--states 100` 을
    돌리면 rc 0 · status `complete` 로 **2 행 파일을 1 행으로 교체**한다. `--states 100,100` 은 requested/paired 2/2 ·
    중복 2 행 · rc 0 complete.

    닫힘 조건: canonical completeness 는 source 별 **정본 roster**(선언 − 알려진 부재)에 상대적이다. subset 은 별도
    identity 와 비승격 status 로만 남고, 중복·미선언 상태는 거부한다."""
    base = tmp_path; matrix, out = base / "matrix", base / "shape"; matrix.mkdir()
    ns = _shape_harness(monkeypatch, base, {"pristine": 0.0, "100": 0.01, "200": 0.10})
    monkeypatch.setattr(ns.D, "HALF_FILE", {"GITT": {"pristine": "p", "100": "a", "200": "b"}})
    _pair(matrix, "100"); _pair(matrix, "200")
    rc, _ = _run_shape(ns, monkeypatch, matrix, out)
    art, rows, meta = _read_shape(out)
    assert rc == 0 and sorted(rows) == ["100", "200"] and meta["status"] == "complete"
    complete_bytes = art.read_bytes()

    rc, text = _run_shape(ns, monkeypatch, matrix, out, "100")             # 축소는 canonical 이 아니다
    assert rc == 3, (rc, text[-500:])
    assert art.read_bytes() == complete_bytes, "축소한 roster 가 complete canonical 을 덮었다"
    _, rows_s, meta_s = _read_shape(out, "partial")
    assert meta_s["status"] == "subset" and rows_s.keys() == {"100"}, meta_s.get("status")
    assert meta_s["pairing"]["authority"] == ["100", "200"], meta_s["pairing"]
    assert "subset" in text or "축소" in text, text[-500:]

    rc, text = _run_shape(ns, monkeypatch, matrix, out, "100,100")         # 중복
    assert rc == 2 and "중복" in text, (rc, text[-400:])
    rc, text = _run_shape(ns, monkeypatch, matrix, out, "999")             # 선언에 없는 상태
    assert rc == 2 and ("선언" in text or "999" in text), (rc, text[-400:])
    assert art.read_bytes() == complete_bytes


# ── P1-3 ─────────────────────────────────────────────────────────────────────────────────────
class _ProfObj:
    scale_audit = None
    n_scale_samples = 50
    c_cell = 1.0

    def __init__(self):
        self.consumed_inputs, self.inputs_sha = _receipt()
        self.scales = {"pocv": 1.0, "dvdq": 1.0, "dqdv": 1.0}

    def __call__(self, _q): return 1.0
    def rmse_pocv(self, _q): return 1.0
    def _auto_scales(self, *a, **k): return dict(self.scales)


def _prof_args(t, out, grid=S.CANONICAL_GAMMA_GRID_N):
    """⚠ Codex R11 P1-3: 정본 γ 격자(21)가 아니면 그 실행은 caller 가 좁힌 subset 이고 canonical 이 아니다 —
    격자 자체가 주제가 아닌 시험은 정본 격자로 돈다."""
    return SimpleNamespace(data_root=str(t), source="GITT", state="100", si_source="Li", w_dqdv=0.0,
                           seed=0, starts=0, grid=grid, profile_scale="global", tol=0.01,
                           out=str(out), run_id="r10-profile")


def test_d10_03_profile_seals_its_gamma_roster_and_partial_never_reaches_canonical(tmp_path, monkeypatch):
    """[Codex R10 P1-3 · P1] γ 둘 중 하나의 optimizer 만 실패시키면 실패 γ 는 행에서 빠지고 **1 행이 canonical 을 교체**
    한다 — rc 0, `schema.check_rows` 문제 0, 실제 `run_states.sh` 의 `write_meta` 서명과 `provenance --verify-unit` 까지
    통과한다. missing 목록은 사라지는 stdout 요약에만 있었다.

    닫힘 조건: γ roster 를 계산 **전에** 고정하고 requested/succeeded/missing 을 artifact 에 봉인한다. exact complete 만
    canonical, 나머지는 typed partial 과 비영 종료."""
    art = tmp_path / "profile_gamma_100_Li.csv"
    old = b"PREVIOUS COMPLETE CANONICAL\n"
    art.write_bytes(old)
    calls = {"n": 0}

    def fake_minimize(_f, _s, **_k):
        calls["n"] += 1
        return SimpleNamespace(success=calls["n"] != 1, fun=1.0, x=np.array([1.0, 0.0, 1.0, 0.0]))

    monkeypatch.setattr(verify.D, "data_root", lambda *a, **k: tmp_path)
    monkeypatch.setattr(verify, "build", lambda *a, **k: _ProfObj())
    monkeypatch.setattr(verify, "multistart", lambda *a, **k: (np.array([1.0, 0.0, 1.0, 0.0, 0.2]), 1.0, []))
    monkeypatch.setattr(verify, "minimize", fake_minimize)
    monkeypatch.setattr(verify, "degradation_modes", lambda *a, **k: {"LAM_PE": 0.1, "LAM_NE": 0.2, "LLI": 0.3})
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        rc = verify.cmd_profile(_prof_args(tmp_path, art))
    assert rc == 3, (rc, buf.getvalue()[-500:])
    assert art.read_bytes() == old, "부분 실행이 완전 canonical 을 덮었다"
    # ⚠ R16 (조건 8 축 ④): 부분은 `partial/<종류>/<attempt-id>/` 로 간다 — 평면 자리는 더 이상 없다.
    #   index 에서 찾는다 (그것이 index 가 있는 이유다).
    part = verify.latest_partial(art) or (art.parent / "partial" / art.name)
    assert part.is_file(), sorted(p.name for p in art.parent.rglob("*"))
    rows = list(csv.DictReader(io.StringIO(part.read_text(encoding="utf-8"))))
    n = S.CANONICAL_GAMMA_GRID_N
    assert len(rows) == n - 1
    roster = json.loads(rows[0]["gamma_roster"])                           # artifact 가 스스로 모집단을 말한다
    assert roster["requested"] == n and roster["succeeded"] == n - 1 and len(roster["missing"]) == 1, roster
    assert "gamma_roster" in S.PROFILE_ROW

    calls["n"] = 0                                                         # 대조군: 전부 성공하면 canonical
    monkeypatch.setattr(verify, "minimize", lambda *a, **k: SimpleNamespace(success=True, fun=1.0, x=np.array([1.0, 0.0, 1.0, 0.0])))
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        rc = verify.cmd_profile(_prof_args(tmp_path, art))
    assert rc == 0 and art.read_bytes() != old
    rows = list(csv.DictReader(io.StringIO(art.read_text(encoding="utf-8"))))
    assert len(rows) == S.CANONICAL_GAMMA_GRID_N and json.loads(rows[0]["gamma_roster"])["missing"] == []


# ── P1-4 ─────────────────────────────────────────────────────────────────────────────────────
def test_d10_04_matrix_failures_do_not_destroy_canonical_and_are_not_process_success(tmp_path, monkeypatch):
    """[Codex R10 P1-4 · P1] 모든 `build` 가 실패하면 4 열짜리 error 행 16 개가 기존 complete canonical 을 교체하고
    (스키마 문제 36 건) 함수가 `None` 으로 끝나 process rc 0 이었다.

    닫힘 조건: 기대 조합 roster 와 typed status 를 게시 전에 계산하고, exact success 만 canonical 로 원자 교체한다."""
    art = tmp_path / "matrix_100.csv"
    old = b"PREVIOUS COMPLETE CANONICAL\n"
    art.write_bytes(old)

    class Exists:
        def is_file(self): return True

    monkeypatch.setattr(verify.D, "data_root", lambda *a, **k: tmp_path)
    monkeypatch.setattr(verify.D, "half_cell_path", lambda *a, **k: Exists())
    monkeypatch.setattr(verify, "build", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("forced")))
    args = SimpleNamespace(data_root=str(tmp_path), state="100", source="GITT", only_source=True,
                           only_wdqdv=False, w_dqdv=0.0, seed=0, starts=0, out=str(art), run_id="r10-matrix")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        rc = verify.cmd_matrix(args)
    assert rc == 1, (rc, buf.getvalue()[-500:])                            # 짝 0 = none (부분이 아니다)
    assert art.read_bytes() == old, "전부 실패한 실행이 canonical 을 파괴했다"
    # ⚠ R16 (조건 8 축 ④): 부분은 `partial/<종류>/<attempt-id>/` 로 간다 — 평면 자리는 더 이상 없다.
    #   index 에서 찾는다 (그것이 index 가 있는 이유다).
    part = verify.latest_partial(art) or (art.parent / "partial" / art.name)
    assert part.is_file(), sorted(p.name for p in art.parent.rglob("*"))
    rows = list(csv.DictReader(io.StringIO(part.read_text(encoding="utf-8"))))
    assert rows and all(r.get("error") for r in rows), rows[:1]
    assert S.check_rows("matrix", rows, list(rows[0])), "error 행 묶음은 스키마 통과가 아니다"


# ── P1-5 ─────────────────────────────────────────────────────────────────────────────────────
def test_d10_05_an_error_cell_cannot_switch_off_row_validation(tmp_path):
    """[Codex R10 P1-5 · P1] 정상 수치 행에 `error=skip` 한 칸을 붙이고 receipt 네 칸을 전부 비워도 `check_rows` 가
    `continue` 로 전부 건너뛰어 U18 gate 가 "전부 갖췄다 · 전부 같다" rc 0 이었다.

    닫힘 조건: success/error **exact tagged union** — success 행에는 `error` 가 없어야 하고, error 행이 하나라도 있으면
    그 묶음은 승격 대상이 아니다."""
    ci, digest = _receipt()
    row = {k: "1" for k in S.MATRIX_ROW}
    # 자체 리뷰 C05: matrix 도 모집단을 행에 봉인한다 — 한 행 묶음의 정직한 주장
    row["combo_roster"] = json.dumps({"authority": 1, "requested": 1, "succeeded": 1,
                                      "missing_input": [], "failed": [], "absent": []})
    row.update(half_cell="GITT", si="Li", w_dqdv="0", run_id="r10", inputs_sha=digest, ref_inputs_sha=digest,
               consumed_inputs=json.dumps(ci), ref_consumed_inputs=json.dumps(ci),
               # 자체 리뷰 C33: `scale_audit_*` 는 더 이상 빈 칸이 허용되지 않는다 (`MAY_BE_EMPTY` 와 `ROW_SKIP`
               #   양쪽에 있어서 정본에 있고 재실행에 없어도 "전부 같다" 였다 — 감사 없이 돌면 그것이 문제다)
               scale_audit_target=audit_json(), scale_audit_ref=audit_json(), bounds="-", ref_bounds="-")
    ok = {k: row[k] for k in S.MATRIX_ROW}
    assert not S.check_rows("matrix", [ok], list(S.MATRIX_ROW)), "대조군(정상 행)은 통과해야 한다"
    attacked = dict(ok, error="skip all validation", inputs_sha="", ref_inputs_sha="",
                    consumed_inputs="", ref_consumed_inputs="")
    problems = S.check_rows("matrix", [attacked], [*S.MATRIX_ROW, "error"])
    assert problems and any("error" in p for p in problems), problems
    old, new = tmp_path / "old", tmp_path / "new"
    _publish(old, [ok], "r10-old")
    fn = new / "matrix_100.csv"; new.mkdir(parents=True, exist_ok=True)
    verify.atomic_write_csv(fn, [attacked], [*S.MATRIX_ROW, "error"]); _sign(fn, "r10-new", "100", full=True)
    rc, out, _ = _cli("check_u14.py", "--new", new, "--old", old)
    assert rc == 2 and "전부 같다" not in out, (rc, out[-600:])
    assert "error" in out, out[-600:]


# ── P1-6 ─────────────────────────────────────────────────────────────────────────────────────
def test_d10_06_receipts_bind_each_digest_to_its_input_role(tmp_path):
    """[Codex R10 P1-6 · P1] aggregate digest 가 sha 값만 정렬해 half_cell↔full_cell 을 **바꿔치기해도 같은 값**(`76be1dcab00e`)
    이고, `{"decoy": …}` 하나뿐인 receipt 도 validator 문제 0 · gate rc 0 이었다.

    닫힘 조건: artifact kind 와 target/ref 별 **exact 역할**(half_cell · full_cell · literature.gr · literature.si)을
    요구하고 역할을 digest 에 묶는다."""
    good, dg = _receipt()
    swapped = dict(good, half_cell=good["full_cell"], full_cell=good["half_cell"])
    assert S.inputs_digest(swapped) != dg, "역할을 바꿨는데 digest 가 같다"
    assert not S.validate_receipt(good, dg, "good"), S.validate_receipt(good, dg, "good")
    decoy = {"decoy": {"path": "not-a-model-input.bin", "sha256": "a" * 64}}
    problems = S.validate_receipt(decoy, S.inputs_digest(decoy), "decoy")
    assert problems and any("half_cell" in p for p in problems), problems
    missing_si = {k: v for k, v in good.items() if k != "literature"} | {"literature": {"gr": good["literature"]["gr"]}}
    assert S.validate_receipt(missing_si, S.inputs_digest(missing_si), "missing"), "빠진 역할을 못 잡는다"
    # U18 gate 도 같은 판정 — decoy 만 든 재실행은 승격 대상이 아니다
    old, new = tmp_path / "old", tmp_path / "new"
    _publish(old, _full_matrix_rows("r10-r-old"), "r10-r-old")
    rows = _full_matrix_rows("r10-r-new")
    for r in rows:
        r["consumed_inputs"] = r["ref_consumed_inputs"] = json.dumps(decoy)
        r["inputs_sha"] = r["ref_inputs_sha"] = S.inputs_digest(decoy)
    _publish(new, rows, "r10-r-new")
    rc, out, _ = _cli("check_u14.py", "--new", new, "--old", old)
    assert rc == 2 and "전부 같다" not in out, (rc, out[-600:])
    assert "half_cell" in out and ("역할" in out or "role" in out), out[-800:]


# ── P1-7 ─────────────────────────────────────────────────────────────────────────────────────
def test_d10_07_promotion_requires_the_same_environment_and_present_controls(tmp_path):
    """[Codex R10 P1-7 · P1] `env` 는 **존재만** 요구하고 비교하지 않았고, control 비교는 양쪽에 key 가 있을 때만 돌아
    candidate 에서 `state`·`starts` 를 지우면 검사가 잠들었다 — 두 경우 모두 rc 0 "전부 같다".

    닫힘 조건: artifact kind 별 필수 control exact schema 와 canonical environment signature 를 숫자 비교 **전에**
    강제한다."""
    def pair(sub, mutate):
        old, new = tmp_path / sub / "old", tmp_path / sub / "new"
        _publish(old, _full_matrix_rows(sub + "-old"), sub + "-old")
        f = _publish(new, _full_matrix_rows(sub + "-new"), sub + "-new")
        m = f.with_name(f.name + ".meta.json")
        meta = json.loads(m.read_text(encoding="utf-8"))
        mutate(meta)
        m.write_text(json.dumps(meta), encoding="utf-8")
        return _cli("check_u14.py", "--new", new, "--old", old)

    rc, out, _ = pair("env", lambda m: m.update(env=_fixture_env(python="9.9", numpy="999", scipy="999", pandas="9.9", openpyxl="9.9", platform="alien")))
    assert rc == 2 and "전부 같다" not in out, (rc, out[-500:])
    assert "env" in out and ("환경" in out or "numpy" in out), out[-700:]
    rc, out, _ = pair("controls", lambda m: [m.pop("state", None), m.pop("starts", None)])
    assert rc == 2 and "전부 같다" not in out, (rc, out[-500:])
    assert "starts" in out and ("없" in out or "missing" in out), out[-700:]
    # 대조군: 같은 환경·control 이면 통과한다
    old, new = tmp_path / "ok" / "old", tmp_path / "ok" / "new"
    _publish(old, _full_matrix_rows("ok-old"), "ok-old")
    _publish(new, _full_matrix_rows("ok-new"), "ok-new")
    rc, out, _ = _cli("check_u14.py", "--new", new, "--old", old)
    assert rc == 0 and "전부 같다" in out, (rc, out[-700:])


# ── P1-8 ─────────────────────────────────────────────────────────────────────────────────────
def test_d10_08_candidate_and_baseline_must_be_independent(tmp_path):
    """[Codex R10 P1-8 · P1] 같은 signed directory 를 `--new` 와 `--old` 에 함께 주면 rc 0 · roster 1/1 · "전부 같다" —
    baseline 을 이미 덮었거나 애초에 없던 상태와 구별되지 않는다.

    닫힘 조건: resolved/samefile identity 를 거부한다 (`--old-rev` 의 immutable bytes 는 허용)."""
    d = tmp_path / "candidate"
    _publish(d, _full_matrix_rows("same-root"), "same-root")
    rc, out, _ = _cli("check_u14.py", "--new", d, "--old", d)
    assert rc == 2 and "전부 같다" not in out, (rc, out[-500:])
    assert "같은" in out or "samefile" in out or "독립" in out, out[-500:]
    link = tmp_path / "alias"
    link.symlink_to(d)
    rc, out, _ = _cli("check_u14.py", "--new", d, "--old", link)           # 경로 문자열만 다른 별칭
    assert rc == 2, (rc, out[-500:])


# ── P2-1 ─────────────────────────────────────────────────────────────────────────────────────
def test_d10_09_subset_is_not_a_success_exit_and_says_so_machine_readably(tmp_path):
    """[Codex R10 P2-1 · P2] `--subset` 이 "부분 · 승격 아님" 을 **글자로만** 말하고 rc 0 이었다 — 자동 소비자는 full
    equality 와 구분할 구조가 없다. rc 3 과 typed `promotion_eligible: false`."""
    old, new = tmp_path / "old", tmp_path / "new"
    # ⚠ 자체 리뷰 C02 뒤: 정본과 재실행의 run id 는 달라야 한다 (같으면 같은 시도의 사본 = alias).
    #   본문의 `run_id` 열과 사이드카가 **같은 id** 여야 하므로(묶음 검사) 둘을 함께 바꾼다.
    for st in ("100", "200"):
        rid = f"sub-{st}-old"
        rows = _full_matrix_rows(rid)
        d = old; d.mkdir(parents=True, exist_ok=True)
        f = d / f"matrix_{st}.csv"; verify.atomic_write_csv(f, rows, list(rows[0]))
        _sign(f, rid, st, full=True)
    rows = _full_matrix_rows("sub-100-new"); new.mkdir(parents=True, exist_ok=True)
    f = new / "matrix_100.csv"; verify.atomic_write_csv(f, rows, list(rows[0]))
    _sign(f, "sub-100-new", "100", full=True)
    rc, out, _ = _cli("check_u14.py", "--new", new, "--old", old, "--subset")
    assert rc == 3, (rc, out[-600:])
    line = next((l for l in out.splitlines() if l.startswith("PROMOTION ")), "")
    assert line, out[-600:]
    d = json.loads(line[len("PROMOTION "):])
    assert d["promotion_eligible"] is False and d["subset"] is True and d["roster"]["old"] == 2, d
    rc, out, _ = _cli("check_u14.py", "--new", old, "--old", old.parent / "old2")   # 없는 baseline
    assert rc == 2, rc


# ── P2-2 ─────────────────────────────────────────────────────────────────────────────────────
def test_d10_10_invalid_degeneracy_is_nonzero_in_every_sink(tmp_path, monkeypatch):
    """[Codex R10 P2-2 · P2] schema 강제가 `--out` 에만 걸려 stdout 모드는 receipt·`inputs_sha` 가 빠진 JSON 을 내고
    stderr 경고 뒤 rc 0 이었다. sink 는 semantic validity 의 경계가 아니다."""
    class Bare:
        c_cell = 1.0
        scale_audit = None
        def __call__(self, _q): return 1.0

    modes = {"LAM_PE": 0.1, "LAM_NE": 0.2, "LLI": 0.3}
    ext = {k: {"min": v * 100, "max": v * 100} for k, v in modes.items()}
    monkeypatch.setattr(verify.D, "data_root", lambda *a, **k: tmp_path)
    monkeypatch.setattr(verify, "build", lambda *a, **k: Bare())
    monkeypatch.setattr(verify, "multistart", lambda *a, **k: (np.array([1.0, 0.0, 1.0, 0.0, 0.2]), 1.0, []))
    monkeypatch.setattr(verify, "degradation_modes", lambda *a, **k: dict(modes))
    monkeypatch.setattr(verify, "near_optimal_extrema", lambda *a, **k: ext)
    monkeypatch.setattr(verify, "mode_profile_extrema", lambda *a, **k: ext)
    args = SimpleNamespace(data_root=str(tmp_path), source="GITT", state="100", si_source="Li", w_dqdv=0.0,
                           seed=0, starts=0, grid=2, samples=0, tol=0.01, out=None, run_id="r10-stdout")
    so, se = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(so), contextlib.redirect_stderr(se):
        rc = verify.cmd_degeneracy(args)
    assert rc == 2, (rc, se.getvalue()[-400:])
    j = json.loads(so.getvalue())
    assert j.get("status") == "invalid" and j.get("problems"), list(j)[:6]   # bare artifact 가 아니다
    assert "LLI_percent" not in j, "invalid 산출을 그대로 흘리면 소비자가 artifact 로 읽는다"


# ── P2-3 ─────────────────────────────────────────────────────────────────────────────────────
def test_d10_11_sidecar_argv_is_a_vector_and_the_regression_runs_the_real_run(tmp_path):
    """[Codex R10 P2-3 · P2] `LAST_ARGV="$*"` 라 `['cmd','a b','c']` 와 `['cmd','a','b c']` 가 같은 문자열로 기록됐고,
    d9_10 은 `run()` 을 부르지 않고 `LAST_ARGV` 를 직접 주입해 production 결속을 한 번도 안 돌았다 (`LAST_ARGV=
    "FORGED-BY-MUTANT"` 변이가 살아남았다).

    닫힘 조건: `"$@"` 경계를 JSON array 로 기록하고, 회귀가 실제 `run()` + shim producer 를 통과한다."""
    shim = tmp_path / "shim.py"
    shim.write_text("import os, sys\n"
                    "open(sys.argv[1], 'w').write('a,run_id\\n' + sys.argv[2].replace(',', ';') + ',' + os.environ['BMS_RUN_ID'] + '\\n')\n",
                    encoding="utf-8")
    script = f'''
for vec in one two; do
  ART="{tmp_path}/matrix_$vec.csv"
  if [ "$vec" = one ]; then
    run "shim $vec" "$ART" - "$ART.log" python3 {shim} "$ART" "A B" C
  else
    run "shim $vec" "$ART" - "$ART.log" python3 {shim} "$ART" A "B C"
  fi
  write_meta "$ART" 100 GITT || echo "write_meta failed for $vec" >&2
done
'''
    p = _shell(script, {"OUT": str(tmp_path)})
    metas = {}
    for vec in ("one", "two"):
        m = tmp_path / f"matrix_{vec}.csv.meta.json"
        assert m.is_file(), (p.stdout[-500:], p.stderr[-800:])
        metas[vec] = json.loads(m.read_text(encoding="utf-8"))
    for vec, meta in metas.items():
        assert isinstance(meta["argv"], list), (vec, meta["argv"])
        assert meta["argv"][0] == "python3" and meta["argv"][1] == str(shim), meta["argv"]
    assert metas["one"]["argv"] != metas["two"]["argv"], metas["one"]["argv"]
    assert metas["one"]["argv"][-2:] == ["A B", "C"] and metas["two"]["argv"][-2:] == ["A", "B C"], metas
    # 회귀가 production 줄을 정말 통과하는가 — 그 줄을 위조하면 이 시험이 깨져야 한다
    src = (ROOT / "scripts/run_states.sh").read_text(encoding="utf-8")
    assert src.count('LAST_ARGV_JSON="$(') == 1, "argv 직렬화가 run() 안 한 자리여야 변이가 잡힌다"


# ── P2-4 ─────────────────────────────────────────────────────────────────────────────────────
def _runner(name):
    return ROOT / ("reviews/r9_repros/replay_codex_r9.py" if name == "r9" else "reviews/r7_repros/replay_codex_r7.py")


def _head():
    return subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()


def _run_runner(name, *extra, env=None, timeout=900):
    e = dict(os.environ); e.update(env or {})
    r = subprocess.run([sys.executable, str(_runner(name)), "--target", str(ROOT),
                        "--expected-head", _head(), *extra], cwd=ROOT, capture_output=True, text=True,
                       timeout=timeout, env=e)
    return r.returncode, r.stdout, r.stderr


def test_d10_12_closure_runners_fail_closed_when_assertions_are_off():
    """[Codex R10 P2-4 · P2] 모든 runtime check 가 `assert` 라 `python -O` 에서 제거된다 — delegated pytest 가 usage
    error 인데 runner rc 0 · `closed: true` · P2-4 `반례 소멸` 이었다.

    닫힘 조건: 증거 판정에 `assert` 를 쓰지 않고 subprocess rc/fingerprint 를 최종 술어에 **값으로** 묶는다.
    optimize mode 자체를 fail-closed 한다."""
    for name in ("r9", "r7"):
        rc, out, err = _run_runner(name, "--probes", "P2-3" if name == "r9" else "R7-06",
                                   "--allow-dirty", env={"PYTHONOPTIMIZE": "1"})
        assert rc != 0, (name, rc, out[:300])
        assert "-O" in (out + err) or "assert" in (out + err), (name, err[-300:])
    rc, out, err = _run_runner("r9", "--probes", "P2-4", "--allow-dirty",
                               env={"PYTEST_ADDOPTS": "--definitely-invalid-option"})
    assert rc != 0, (rc, out[:400])
    d = json.loads(out) if out.strip().startswith("{") else {}
    assert d.get("closed") is not True, d.get("closed")
    assert d["probes"]["P2-4"]["상태"] != "반례 소멸", d["probes"]["P2-4"]


# ── P2-5 ─────────────────────────────────────────────────────────────────────────────────────
def test_d10_13_closure_runners_seal_the_bytes_they_execute(tmp_path):
    """[Codex R10 P2-5 · P2] HEAD + porcelain 은 실행 bytes 를 봉인하지 않는다 — `git status` 가 rc 128 이어도
    `dirty: false · closed: true`, `assume-unchanged` 로 고친 tracked module 이 실행돼도 clean, ignored `__pycache__`
    의 위조 bytecode 가 실행돼도 clean 이었다.

    닫힘 조건: status rc 비영은 즉시 오류. 증거 실행은 expected commit 에서 새로 materialize 한 격리 snapshot 에서 하고
    index skip flag 와 ignored importable bytes 를 배제한다."""
    rc, out, err = _run_runner("r9", "--probes", "P2-3", "--allow-dirty",
                               env={"GIT_INDEX_FILE": str(tmp_path)})     # 디렉터리를 index 로 → git status rc 128
    assert rc != 0 and ("status" in (out + err) or "git" in (out + err)), (rc, err[-300:])

    snap = tmp_path / "snap"
    planted = ROOT / "bms_balancing" / "__pycache__" / "zz_r10_planted.pyc"
    planted.parent.mkdir(parents=True, exist_ok=True)
    planted.write_bytes(b"planted-ignored-bytes")
    try:
        rc, out, err = _run_runner("r9", "--probes", "P2-3", "--keep-materialized", str(snap))
        # ⚠ 자체 리뷰 C19 뒤: 종료 코드가 `evidence_eligible` 을 반영한다 (증거면 0, 아니면 3) —
        #   개발 중 트리에서는 도구 자신이 HEAD 의 blob 과 달라 eligible false 가 정상이다.
        d = json.loads(out)
        assert rc == (0 if d["evidence_eligible"] else 3), (rc, err[-500:])
        assert d["materialized"]["head"] == _head(), d["materialized"]
        assert pathlib.Path(d["materialized"]["path"]) != ROOT
        # 증거 자격 = 격리 snapshot + 패키지 digest + **도구 자신도 그 커밋의 bytes** (러너가 아직 커밋 전이면 false —
        # 그 커밋의 증거는 그 커밋에서만 만든다). 커밋 전/후 둘 다에서 성립하는 항등식으로 고정한다.
        assert d["evidence_eligible"] == (d["instrument_sealed"] and d["package_digest_ok"]), d["instrument"]
        assert set(d["instrument"]) == {"reviews/r9_repros/replay_codex_r9.py", "reviews/evidence_gate.py"}
        tree = snap / "bms-balancing"
        assert (tree / "bms_balancing" / "verify.py").is_file(), sorted(p.name for p in snap.iterdir())
        assert not list(tree.rglob("zz_r10_planted.pyc")), "ignored bytes 가 격리 snapshot 에 새어 들어갔다"
        assert subprocess.check_output(["git", "-C", str(tree), "rev-parse", "HEAD"], text=True).strip() == _head()
    finally:
        planted.unlink(missing_ok=True)
        shutil.rmtree(snap, ignore_errors=True)
        subprocess.run(["git", "-C", str(ROOT), "worktree", "prune"], capture_output=True)
    rc, out, _ = _run_runner("r9", "--probes", "P2-3", "--allow-dirty")     # dev 모드는 증거가 아니다
    d = json.loads(out) if out.strip().startswith("{") else {}
    assert d.get("evidence_eligible") is False, d.get("evidence_eligible")


# ── P2-6 ─────────────────────────────────────────────────────────────────────────────────────
def test_d10_14_package_byte_corruption_stops_the_runner_and_the_regression_sees_it():
    """[Codex R10 P2-6 · P2] `package_digest()` 를 mismatch 에도 True 로 만드는 변이가 `test_d9_08` 을 통과했다 —
    회귀가 source 에 문자열이 있는지만 봤기 때문이다. 실제 package byte 를 바꾸고 runner 가 **probe 를 안 돌리는지**
    본다."""
    victim = ROOT / "reviews/r7_repros/codex/HARNESS_R7_521BE85_CODEX_REVIEW.md"
    backup = victim.read_bytes()
    try:
        victim.write_bytes(backup + b"\nCORRUPTED BY REGRESSION\n")
        rc, out, err = _run_runner("r7", "--probes", "R7-06", "--allow-dirty")
        assert rc != 0, (rc, out[:400])
        d = json.loads(out) if out.strip().startswith("{") else {}
        assert d.get("package_digest_ok") is False, d.get("package_digest_ok")
        assert not d.get("probes"), d.get("probes")
        assert d.get("package_digest", {}).get(victim.name) == "mismatch", d.get("package_digest")
    finally:
        victim.write_bytes(backup)
    rc, out, _ = _run_runner("r7", "--probes", "R7-06", "--allow-dirty")
    _d = json.loads(out)
    assert rc == (0 if _d["evidence_eligible"] else 3) and _d["package_digest_ok"] is True


# ── P2-7 ─────────────────────────────────────────────────────────────────────────────────────
def test_d10_15_a_production_wrapper_consumes_the_typed_shape_status(tmp_path):
    """[Codex R10 P2-7 · P2] "wrapper 가 none/partial 을 가른다" 는 주장에 production path 가 0 개였다 — 회귀는
    `ne_shape.main()` 을 직접 부르고 meta 와 문서 문자열만 봤다.

    닫힘 조건: 실제 caller 를 만들고 회귀가 그것을 실행한다."""
    live = [ln for ln in (ROOT / "scripts/run_states.sh").read_text(encoding="utf-8").splitlines()
            if ln.strip() and not ln.lstrip().startswith("#")]
    assert any("ne_shape" in ln for ln in live), "production wrapper 에 ne_shape 소비 경로가 없다"

    def shim(rc, status):
        """producer 흉내 — **실행 시점에** 자기 산출·사이드카를 쓰고 `SHAPE_RESULT` 로 경로·run_id·status 를 말한다.

        ⚠ Codex R11 P2-2: 전 판은 wrapper 가 `ls | head -1` 로 훑어 옆의 stale canonical 을 읽었다.
        ⚠ 자체 리뷰 C15: 이제 `shape_step` 이 `BMS_RUN_ID` 를 주입하고 다른 세 단계와 같은 묶음 검사를 건다 —
          진짜 producer 가 그 환경값을 쓰므로 shim 도 같게 해야 그 축을 잰다 (전 판은 미리 써 둔 한 줄이었다).
        """
        sfile = tmp_path / f"shim{rc}.py"
        d = tmp_path / f"w{rc}"
        (d / "partial").mkdir(parents=True, exist_ok=True)
        art = (d / "partial" / "ne_shape_GITT_Li.csv") if status != "complete" else (d / "ne_shape_GITT_Li.csv")
        sfile.write_text(
            "import hashlib, json, os, pathlib, sys\n"
            f"art = pathlib.Path({str(art)!r})\n"
            "rid = os.environ.get('BMS_RUN_ID', '')\n"
            "art.parent.mkdir(parents=True, exist_ok=True)\n"
            "art.write_text(f'state,run_id\\n100,{rid}\\n', encoding='utf-8')\n"
            f"meta = {{'status': {status!r}, 'run_id': rid, 'artifact': art.name,\n"
            "        'sha256': hashlib.sha256(art.read_bytes()).hexdigest()}\n"
            "art.with_name(art.name + '.meta.json').write_text(json.dumps(meta), encoding='utf-8')\n"
            f"print('SHAPE_RESULT ' + json.dumps({{'status': {status!r}, 'artifact': str(art), 'run_id': rid}},\n"
            "                                   ensure_ascii=False))\n"
            f"sys.exit({rc})\n", encoding="utf-8")
        return sfile, d

    # rc 1(none) 은 게시된 산출이 없다 — producer 가 artifact: null 을 말한다 (아래 별도)
    for rc_in, status, word in ((3, "partial", "부분"), (0, "complete", "complete")):
        s, d = shim(rc_in, status)
        p = _shell(f'shape_step "{d}" python3 {s}; echo "STEP_RC=$?"', {"OUT": str(d)})
        text = p.stdout + p.stderr
        assert f"STEP_RC={rc_in}" in text, (rc_in, text[-500:])            # 종료 코드를 그대로 전파한다
        assert status in text or word in text, (rc_in, text[-500:])        # typed status 를 읽는다
    # none: 산출이 없다고 말하는 producer 도 rc 를 그대로 전파한다 (모르는 채 넘기지 않는다)
    none_sh, dn = shim(1, "none")
    p = _shell(f'shape_step "{dn}" python3 {none_sh}; echo "STEP_RC=$?"', {"OUT": str(dn)})
    assert "STEP_RC=1" in (p.stdout + p.stderr), (p.stdout + p.stderr)[-500:]


# ── 문서 ─────────────────────────────────────────────────────────────────────────────────────
def test_d10_16_docs_record_the_r10_closure():
    led = _live(_doc("reviews/R6_LEDGER.md"))
    assert "Codex R10" in led and "P1-1" in led and "P2-7" in led
    req = _live(_doc("reviews/R11_REQUEST.md"))
    assert "R10" in req and "materialize" in req
    ws = _live(_doc("WORKING_STATE.md"))
    assert "10차" in ws and "provenance-incomplete" in ws
