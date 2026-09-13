"""Codex R13 (대상 `94add7b`) NO-GO — P1 4 · P2 5 의 회귀.

리뷰어의 반례를 그대로 옮긴다. 패키지는 `reviews/r13_repros/codex/`
(zip sha256 `c4d51fcff1e6843d69302d870784ce6d80181e9454a5ca5664de8832055f6f60`,
manifest 163/163 일치 실측).

핵심 축 하나: **두 산출이 서로 같다는 것과 각각이 올바른 과학 산출이라는 것은 다르다.**
전 판은 roster 의 *개수*만 봤고 *구성원*을 독립적으로 정하지 않았다 — 잘못된 모집단을
양쪽에 두 번 적으면 승격 가능이었다.
"""
from __future__ import annotations

import json
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from bms_balancing import data as D          # noqa: E402
from bms_balancing import schema as S        # noqa: E402
from test_review_findings import matrix_row, seal_combo   # noqa: E402
from test_r12_selfreview import _meta, _receipt           # noqa: E402


# ---------------------------------------------------------------- helpers

def _profile_rows(gammas, *, roster=None):
    """profile 본문 + gamma_roster. roster 를 안 주면 '정직한 전수' 를 만든다."""
    n = len(gammas)
    r = roster if roster is not None else {
        "authority": S.CANONICAL_GAMMA_GRID_N, "requested": S.CANONICAL_GAMMA_GRID_N,
        "succeeded": n, "missing": [],
    }
    raw = json.dumps(r, sort_keys=True)
    rec_d, ref_d = _receipt(), _receipt("5", "6", "7", "8")
    rec, ref = json.dumps(rec_d, sort_keys=True), json.dumps(ref_d, sort_keys=True)
    rows = []
    for g in gammas:
        rows.append({c: "" for c in S.PROFILE_ROW} | {
            "gamma_Si": repr(float(g)), "obj": "1.0", "obj_ratio_to_best": "1.0",
            "rmse_pocv": "1.0", "a_PE": "1.1", "b_PE": "-0.1", "a_NE": "1.0", "b_NE": "0.0",
            "bounds": "ok", "LAM_PE_pct": "1.0", "LAM_NE_pct": "1.0", "LLI_pct": "1.0",
            "n_ok": "1", "n_tried": "1", "run_id": "R", "profile_scale": "global",
            "inputs_sha": S.inputs_digest(rec_d), "ref_inputs_sha": S.inputs_digest(ref_d),
            "consumed_inputs": rec, "ref_consumed_inputs": ref,
            "gamma_roster": raw,
        })
    return rows


def _canonical_combo_rows(state="100"):
    keys = sorted(S.canonical_combo_keys(state))
    return [matrix_row(half_cell=hc, si=si, w_dqdv=repr(w)) for hc, si, w in keys]


# ---------------------------------------------------------------- P1-1

def test_g01_profile_wrong_grid_is_rejected():
    """`profile_wrong_grid` — γ 21 개를 0~0.4 간격 0.02 로. 개수는 정본과 같다.

    전 판: `authority == CANONICAL_GAMMA_GRID_N` 이 **숫자끼리**의 비교라 통과.
    """
    good = S.canonical_gamma_grid()
    assert len(good) == S.CANONICAL_GAMMA_GRID_N
    assert not S.check_rows("profile", _profile_rows(good), list(S.PROFILE_ROW)), "정본 격자 대조군이 막혔다"

    wrong = [round(0.02 * i, 10) for i in range(S.CANONICAL_GAMMA_GRID_N)]      # 0 ~ 0.40
    assert len(wrong) == len(good) and wrong != good
    probs = S.check_rows("profile", _profile_rows(wrong), list(S.PROFILE_ROW))
    assert probs, "개수만 같은 잘못된 γ 격자가 canonical 로 통과했다 (Codex R13 P1-1)"
    assert any("격자" in p or "γ" in p for p in probs), probs


def test_g02_profile_missing_may_not_be_duplicates():
    """`profile_twenty_duplicate_missing` — 본문 1 행 + `missing` 20 개가 전부 같은 값.

    산술(1 + 20 == 21)은 맞아서 전 판은 통과했다. 본문 ∪ missing 이 정본 격자여야 한다.
    """
    good = S.canonical_gamma_grid()
    rows = _profile_rows(good[:1], roster={
        "authority": S.CANONICAL_GAMMA_GRID_N, "requested": S.CANONICAL_GAMMA_GRID_N,
        "succeeded": 1, "missing": [good[1]] * 20,
    })
    probs = S.check_rows("profile", rows, list(S.PROFILE_ROW))
    assert probs, "중복 missing 으로 산술만 맞춘 1 행짜리가 통과했다 (Codex R13 P1-1)"


def test_g03_matrix_self_declared_authority_is_rejected():
    """`matrix_self_declared_one_row_authority` — 1 행이 authority=requested=succeeded=1.

    전 판: `requested == authority` 만 봤고 둘 다 산출이 스스로 적은 수라 통과.
    """
    ok = _canonical_combo_rows("100")
    assert len(ok) == 32, len(ok)
    assert not S.check_rows("matrix", seal_combo(ok), list(S.MATRIX_ROW), name="matrix_100.csv"), \
        S.check_rows("matrix", seal_combo(ok), list(S.MATRIX_ROW), name="matrix_100.csv")

    one = [matrix_row(half_cell="GITT", si="Li", w_dqdv="0.0")]
    rows = seal_combo(one, authority=1)
    probs = S.check_rows("matrix", rows, list(S.MATRIX_ROW), name="matrix_100.csv")
    assert probs, "스스로 authority=1 이라 적은 1 행이 canonical 로 통과했다 (Codex R13 P1-1)"


def test_g04_matrix_undeclared_member_is_rejected():
    """`matrix_wrong_member` — 32 행이지만 Si 하나가 미등록 `Li2`."""
    rows = _canonical_combo_rows("100")
    assert any(r["si"] == "Li" for r in rows)
    for r in rows:
        if r["si"] == "Li":
            r["si"] = "Li2"
            break
    probs = S.check_rows("matrix", seal_combo(rows), list(S.MATRIX_ROW), name="matrix_100.csv")
    assert probs, "선언되지 않은 Si 소스가 개수만 맞아 통과했다 (Codex R13 P1-1)"
    assert any("Li2" in p for p in probs), probs


def test_g05_canonical_contract_is_shared_with_producer():
    """정본 모집단은 **한 곳**에서 나와야 한다 — producer 와 checker 가 같은 함수를 쓴다."""
    import inspect

    from bms_balancing import verify as V
    src = inspect.getsource(V.cmd_matrix) + inspect.getsource(V.cmd_profile)
    assert "canonical_combo_keys" in src, "producer 가 matrix 모집단을 따로 만든다 (두 벌이면 갈린다)"
    assert "canonical_gamma_grid" in src, "producer 가 γ 격자를 따로 만든다"


# ---------------------------------------------------------------- P1-2

def _deg(**over):
    """producer 모양의 degeneracy JSON 한 벌."""
    ci = _receipt()
    j = {"state": "100", "si_source": "Li", "half_cell": "GITT", "w_dqdv": 0.0,
         "tol_percent_of_best": 1.0, "n_starts": 24, "seed": 0, "n_grid": 21, "n_samples": 400,
         "run_id": "rid", "env": {"python": "3.11.0", "numpy": "1.26.0", "scipy": "1.11.0",
                                  "pandas": "2.0.0", "platform": "linux-x"},
         "consumed_inputs": ci, "ref_consumed_inputs": _receipt("5", "6", "7", "8"),
         "inputs_sha": S.inputs_digest(ci), "n_accepted": 5,
         "best_obj": 1.5, "best_p": [1.0, 2.0, 3.0, 4.0, 5.0], "ref_p": [1.0, 2.0, 3.0, 4.0, 5.0],
         "best_modes_percent": {"LLI": 1.5},
         "LAM_PE_percent": {"min": 0.0, "max": 1.0, "is_lower_bound": True},
         "LAM_NE_percent": {"min": 0.0, "max": 1.0, "is_lower_bound": True},
         "LLI_percent": {"min": 1.0, "max": 2.0, "is_lower_bound": True}}
    j.update(over)
    return j


def test_g06_empty_reference_receipt_is_a_candidate_violation():
    """`both_reference_receipts_empty` — 양쪽 `{}` 면 candidate 계약 검사까지 사라졌다.

    전 판: `check_degeneracy` 가 `j.get("ref_consumed_inputs")` truthy 일 때만 검증했고
    (빈 dict 는 falsy), 필수 키 검사도 `in (None, "")` 이라 `{}` 를 통과시켰다.
    """
    assert not S.check_degeneracy(_deg()), S.check_degeneracy(_deg())
    probs = S.check_degeneracy(_deg(ref_consumed_inputs={}))
    assert probs, "빈 reference receipt 가 candidate 계약 검사를 통째로 건너뛰었다 (Codex R13 P1-2)"


def test_g07_string_reference_receipt_is_validated_like_a_dict():
    """`reference_receipt_string_missing_locator` — JSON **문자열** reference 는 검증을 생략했다.

    같은 불완전 reference 가 dict 면 path 누락을 보고하고 문자열이면 아무 말도 안 했다 (비대칭).
    """
    bad = _receipt()
    del bad["half_cell"]["path"]                      # locator 누락
    as_dict = S.check_degeneracy(_deg(ref_consumed_inputs=bad))
    as_text = S.check_degeneracy(_deg(ref_consumed_inputs=json.dumps(bad)))
    assert as_dict, "dict 쪽 대조군이 안 걸린다"
    assert as_text, "같은 결함이 JSON 문자열이면 검증을 건너뛰었다 (Codex R13 P1-2)"


# ---------------------------------------------------------------- P2-1

def test_g08_numeric_fields_reject_bool_and_wrong_shape():
    """`degeneracy_boolean_vs_numeric_baseline` — 정상 `best_obj=1.0` 을 `true` 로 바꿔도 통과했다.

    `float(True) == 1.0` 이라 비교기도 같다고 읽는다. 유한성 검사 **앞에** 타입·모양 계약이 필요하다.
    """
    assert not S.check_degeneracy(_deg())
    for label, over in (("bool objective", {"best_obj": True}),
                        ("non-numeric string", {"best_obj": "not-computed"}),
                        ("empty parameter vector", {"best_p": []}),
                        ("short parameter vector", {"best_p": [1.0, 2.0]}),
                        ("empty statistics object", {"LLI_percent": {}})):
        assert S.check_degeneracy(_deg(**over)), f"{label} 이 과학 값으로 통과했다 (Codex R13 P2-1)"


# ---------------------------------------------------------------- P2-4

def test_g09_required_env_axes_are_checked_without_a_baseline():
    """`schema_only_missing_env_fields` — env 에서 numpy/scipy/pandas/platform 을 지워도 schema 0 이었다.

    필수 env 축의 존재는 baseline 없이도 candidate 혼자 만족해야 하는 계약이다.
    """
    assert not S.check_degeneracy(_deg())
    probs = S.check_degeneracy(_deg(env={"python": "3.11.0"}))
    assert probs, "필수 env 축이 빠졌는데 schema 검사가 통과했다 (Codex R13 P2-4)"
    assert any("env" in p for p in probs), probs


# ---------------------------------------------------------------- P1-4

RUNNERS = ("r7_repros/replay_codex_r7.py", "r9_repros/replay_codex_r9.py",
           "r10_repros/replay_codex_r10.py", "r11_repros/replay_codex_r11.py")


def test_g10_reexec_comes_before_any_hijackable_import():
    """격리 재실행이 **앱 의존성 import 보다 앞**이어야 한다.

    전 판은 `import argparse, contextlib, …, traceback` 이 먼저 돌았다 — `sys.path[0]` 이
    저장소 안이라 untracked `traceback.py` 하나가 봉인 앞에서 실행될 수 있었다 (C08 의 남은 절반).
    `os`·`sys` 는 인터프리터 시작 때 이미 로드돼 `sys.path` 로 가로챌 수 없으므로 예외다.
    """
    import ast

    root = pathlib.Path(__file__).resolve().parents[1] / "reviews"
    safe = {"os", "sys", "__future__"}
    for rel in RUNNERS:
        tree = ast.parse((root / rel).read_text(encoding="utf-8"))
        reexec_at = None
        for node in tree.body:
            if isinstance(node, ast.If) and "execv" in ast.dump(node):
                reexec_at = node.lineno
                break
        assert reexec_at is not None, f"{rel}: 최상위에 재실행 블록이 없다"
        early = [n for n in tree.body
                 if isinstance(n, (ast.Import, ast.ImportFrom)) and n.lineno < reexec_at]
        names = set()
        for n in early:
            names |= ({a.name.split(".")[0] for a in n.names} if isinstance(n, ast.Import)
                      else {(n.module or "").split(".")[0]})
        assert names <= safe, (f"{rel}: 재실행({reexec_at}행) **앞**에 가로챌 수 있는 import 가 있다 "
                               f"{sorted(names - safe)} (Codex R13 P1-4)")


# ---------------------------------------------------------------- P2-2

def _audit(**over):
    m = {"n": 50, "n_finite": 50, "n_inf": 0, "n_nan": 0, "n_exception": 0,
         "raw_lower_half_mean": 0.5, "scale": 0.5, "eps_rel": 1e-15, "equivalent_within_rel": True}
    a = {k: dict(m) for k in ("pocv", "dvdq", "dqdv")}
    a.update(over)
    return json.dumps(a)


def test_g11_scale_audit_content_is_validated():
    """`candidate_audit_empty_object` — 감사 두 열을 `{}` 로 바꿔도 rc 0 · promotion true 였다.

    빈 **문자열**은 막았지만 빈 **객체**는 감사로 인정했다. 표본·유한성·eps 근거가
    사라져도 차이를 기록하지 않았다.
    """
    ok = [matrix_row(scale_audit_target=_audit(), scale_audit_ref=_audit(),
                     scale_pocv_target="0.5", scale_dvdq_target="0.5", scale_dqdv_target="0.5",
                     scale_pocv_ref="0.5", scale_dvdq_ref="0.5", scale_dqdv_ref="0.5")]
    def _content(rows):
        # 정본 **자리** 규칙(1 행 subset)은 이 시험의 축이 아니다 — reader 처럼 걸러 낸다.
        return [q for q in S.check_rows("matrix", rows, list(S.MATRIX_ROW))
                if not q.startswith(S.CANONICAL_SLOT_PREFIX)]

    assert not _content(ok), _content(ok)

    for label, over in (("빈 객체", {"scale_audit_target": "{}"}),
                        ("metric 누락", {"scale_audit_target": _audit(dqdv={})}),
                        ("표본 산술 불일치", {"scale_audit_target": _audit(
                            pocv={"n": 50, "n_finite": 40, "n_inf": 0, "n_nan": 0, "n_exception": 0,
                                  "raw_lower_half_mean": 0.5, "scale": 0.5, "eps_rel": 1e-15,
                                  "equivalent_within_rel": True})}),
                        ("열과 결속 안 됨", {"scale_audit_target": _audit(
                            pocv={"n": 50, "n_finite": 50, "n_inf": 0, "n_nan": 0, "n_exception": 0,
                                  "raw_lower_half_mean": 0.5, "scale": 9.9, "eps_rel": 1e-15,
                                  "equivalent_within_rel": True})})):
        bad = [matrix_row(**(dict(ok[0]) | over))]
        assert _content(bad), f"{label} 인 감사가 통과했다 (Codex R13 P2-2)"


# ---------------------------------------------------------------- P2-3

def test_g12_bom_json_is_a_structured_schema_error_not_a_crash(tmp_path):
    """`bom_json_schema_only` — 정상 JSON 에 UTF-8 BOM 을 붙이면 CLI 가 rc 1 로 죽었다.

    `JSONDecodeError` 가 그대로 올라와 `PROMOTION` 도 안 찍혔다 — 자동 소비자가 실패 원인을
    분류할 수 없다. 스키마 오류의 구조화된 rc 2 여야 한다.
    """
    import subprocess

    root = pathlib.Path(__file__).resolve().parents[1]
    new = tmp_path / "new"
    new.mkdir()
    art = new / "degeneracy_100_Li.json"
    # ⚠ 처음 쓴 판은 meta 없이 데이터만 두어 "묶음 미완" 으로 **먼저** 거부됐다 — BOM 파싱 경로에
    #   닿지도 않으면서 통과했다 (아홉 번 반복된 fixture 패턴). 온전한 묶음으로 만든다.
    art.write_bytes(b"\xef\xbb\xbf" + json.dumps(_deg()).encode("utf-8"))
    _meta(art, run_id="rid")
    p = subprocess.run([sys.executable, str(root / "scripts" / "check_u14.py"),
                        "--new", str(new), "--schema-only"],
                       capture_output=True, text=True, timeout=120)
    assert "PROMOTION" in p.stdout, (f"BOM JSON 에서 PROMOTION 이 안 나왔다 — 구조화된 결과가 아니다 "
                                     f"(Codex R13 P2-3)\nrc={p.returncode}\n{p.stderr[-400:]}")
    assert p.returncode != 1, f"숫자 불일치(rc 1)로 분류됐다 — 스키마 오류여야 한다: rc={p.returncode}"


# ---------------------------------------------------------------- P1-3

def test_g13_closure_summary_separates_report_completion_from_closure():
    """보관 증거는 전제 변경·환경상 불가·우리 코드 밖이 있는데 `closed: true` · "모든 case 가 닫혔다" 였다.

    리뷰어 조건: 실행 유효성 · 개별 판정 · 적용 제외 · 전체 종결을 **별도 필드**로 둔다. 미실행/전제 변경은
    대체 증거 없이 `closed:true` 의 근거가 될 수 없다. rc 0 이 "보고 완료" 라면 `rc_reason` 도 그 뜻이어야 한다.
    """
    import importlib.util

    root = pathlib.Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location("gate", root / "reviews" / "evidence_gate.py")
    gate = importlib.util.module_from_spec(spec); spec.loader.exec_module(gate)

    rec = lambda s, **k: {"상태": s, "멈춘_곳": None, "세부": k.get("why", "")}   # noqa: E731
    R = {"a": rec("반례 소멸"), "b": rec("전제 변경", why="원본이 전제한 파일이 없다"),
         "c": rec("환경상 불가", why="wsl.exe"), "d": rec("우리 코드 밖", why="bash $*")}
    s = gate.summarize_verdicts(R, requested=["a", "b", "c", "d"],
                                substitutes={"b": "test_x", "c": "publish:shape_step"})
    assert s["report_complete"] is True
    assert s["closed"] is False, "전제 변경·환경상 불가가 있는데 closed 가 참이다 (Codex R13 P1-3)"
    assert s["closed_with_substitutes"] is False, "대체 증거 없는 제외(d)가 있는데 참이다"
    assert set(s["excluded"]) == {"b", "c", "d"} and s["excluded"]["b"]["대체"] == "test_x"
    assert "모든 case 가 닫혔다" not in s["rc_reason"] and "반례 소멸 1/4" in s["rc_reason"], s["rc_reason"]

    # 대체 증거가 전부 이름 붙으면 closed_with_substitutes 만 참, closed 는 여전히 거짓
    s2 = gate.summarize_verdicts(R, requested=["a", "b", "c", "d"],
                                 substitutes={"b": "test_x", "c": "publish:shape_step", "d": "adapted:argv-vector"})
    assert s2["closed"] is False and s2["closed_with_substitutes"] is True

    # 요청한 leaf 가 기록에 없으면 보고 미완
    s3 = gate.summarize_verdicts({"a": rec("반례 소멸")}, requested=["a", "z"])
    assert s3["report_complete"] is False and s3["leaf_cases"]["z"] == "미실행"

    # 오류가 하나라도 있으면 보고 미완
    s4 = gate.summarize_verdicts({"a": rec("오류")}, requested=["a"])
    assert s4["report_complete"] is False and s4["closed"] is False


def test_g14_runners_use_the_shared_summary_and_never_claim_all_closed():
    import ast

    root = pathlib.Path(__file__).resolve().parents[1] / "reviews"
    for rel in RUNNERS:
        src = (root / rel).read_text(encoding="utf-8")
        assert "summarize_verdicts(" in src, f"{rel}: 공용 집계를 안 쓴다 (네 벌이면 갈린다)"
        for bad in ('"모든 case 가 닫혔다"', "모든 요청 probe 가 자기 반례 assertion 에서 멈췄다"):
            assert bad not in src, f"{rel}: 제외를 종결로 세는 문구가 남아 있다 — {bad}"
        # rc 0 이 closed 가 아니라 report_complete 에 묶여야 한다
        tree = ast.parse(src)
        rets = [ast.unparse(n) for n in ast.walk(tree) if isinstance(n, ast.Return)]
        assert not any('out["closed"]' in r for r in rets), f"{rel}: rc 가 closed 를 본다 — report_complete 여야 한다"


# ---------------------------------------------------------------- P2-5

def test_g15_r10_premise_change_requires_a_fingerprint():
    """r10 은 `PREMISE_CHANGED` 의 case 가 `오류` 면 **아무 예외나** 전제 변경으로 바꿨다."""
    import importlib.util

    root = pathlib.Path(__file__).resolve().parents[1] / "reviews"
    spec = importlib.util.spec_from_file_location("r10", root / "r10_repros" / "replay_codex_r10.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    assert hasattr(m, "PREMISE_FINGERPRINT"), "r10 에 fingerprint 표가 없다 (Codex R13 P2-5)"
    assert set(m.PREMISE_CHANGED) <= set(m.PREMISE_FINGERPRINT), "fingerprint 없는 전제 변경 case"
    for key, fp in m.PREMISE_FINGERPRINT.items():
        assert isinstance(fp, tuple) and fp and all(isinstance(x, str) and x for x in fp), (key, fp)


def test_g16_r11_environment_limited_is_structured_and_leaves_are_enumerated():
    """`ENVIRONMENT_LIMITED[key][0]` 이 문자열의 첫 글자("원")를 냈다. 값은 구조여야 하고
    환경상 불가는 **구체적 의존성**(`wsl.exe`)에만 붙어야 한다. 그리고 leaf 명부는 37 이다."""
    import importlib.util

    root = pathlib.Path(__file__).resolve().parents[1] / "reviews"
    spec = importlib.util.spec_from_file_location("r11", root / "r11_repros" / "replay_codex_r11.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    for key, v in m.ENVIRONMENT_LIMITED.items():
        assert isinstance(v, dict) and {"why", "substitute", "fingerprint"} <= set(v), (key, v)
        assert isinstance(v["fingerprint"], tuple) and any("wsl" in x for x in v["fingerprint"]), (key, v)
    assert hasattr(m, "EXPECTED_LEAVES") and len(m.EXPECTED_LEAVES) == 37, getattr(m, "EXPECTED_LEAVES", None)
    for leaf in ("publish:matrix_filtered_canonical", "publish:profile_grid1_canonical", "publish:profile_partial_stdout"):
        assert leaf in m.EXPECTED_LEAVES, leaf
    assert "publish:*" not in m.EXPECTED_LEAVES


# ---------------------------------------------------------------- 러너 안 fixture (열한 번째 감사)

def test_g17_runner_inline_fixtures_pass_the_content_contract():
    """R7-05 · R9-05 가 `오류` 로 바뀐 원인 — 러너 안 fixture 가 `scale_audit_*="{}"` · `authority:1` 이었다."""
    import importlib.util

    root = pathlib.Path(__file__).resolve().parents[1] / "reviews"

    def load(name, rel):
        spec = importlib.util.spec_from_file_location(name, root / rel)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

    def content(rows):
        return [q for q in S.check_rows("matrix", rows, list(S.MATRIX_ROW), name="matrix_100.csv")
                if not q.startswith(S.CANONICAL_SLOT_PREFIX)]

    r9 = load("r9", "r9_repros/replay_codex_r9.py")
    assert not content([r9._full_row(None, "rid", "0.3")]), content([r9._full_row(None, "rid", "0.3")])

    r6 = load("r6a", "r6_repros/codex/replay_codex_r6_adapted.py")
    import tempfile
    p = pathlib.Path(tempfile.mkdtemp()) / "matrix_100.csv"
    r6._full_matrix(p, 0.16)
    import csv
    rows = list(csv.DictReader(p.open(encoding="utf-8")))
    assert not content(rows), content(rows)
