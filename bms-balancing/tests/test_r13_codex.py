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
from conftest import fixture_env as _fixture_env   # noqa: E402  (R16: env 축은 한 자리에서)
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
         "run_id": "rid", "env": _fixture_env(python="3.11.0", numpy="1.26.0", scipy="1.11.0", pandas="2.0.0", openpyxl="3.1.0", platform="linux-x"),
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


# ---------------------------------------------------------------- §5 Q6 — shape 전용 kind · schema · sidecar 계약
#
# 리뷰어 실측(`r13_roster_schema_checks.py::fresh_shape_producer`): 현행 `ne_shape._write_csv` 를 선언된 GITT 상태
# 전부의 유한 합성 측정 + complete pairing 으로 부른 산출이 `check_u14 --schema-only` 에서 **rc 2, schema 27,
# provenance_cols 3, content 1, provenance 1** — `check_u14._kind` 가 matrix 아닌 CSV 를 전부 profile 로 읽어 shape 의
# 열 19 개가 "모르는 열" 이고 profile 의 γ/적합 열을 요구했으며, sidecar 도 U14 meta 계약(env·시작 provenance·argv·
# roster)에 안 맞았다. "과거 shape 만 낡은 것이 아니다 — 재생성만으로는 안 닫힌다."
#
# 닫힘 조건 (리뷰어 §Q6): shape 전용 kind · 행 key(state) · receipt/pairing/coverage 계약 · sidecar 요구를 **먼저**
# 배선하고, 그 다음 실제 producer→wrapper→U14 로 재생성. PROFILE_ROW 에 열 19 개를 허용하는 것은 답이 아니다.

def _shape_ns():
    from test_review_findings import _load_script
    return _load_script("ne_shape")


def _prov_shared():
    """`ne_shape` 가 함수 안에서 `from provenance import …` 로 쓰는 **바로 그** 모듈 객체 (`sys.modules`)."""
    import importlib
    root = pathlib.Path(__file__).resolve().parents[1] / "scripts"
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    return importlib.import_module("provenance")


def _clean_git(monkeypatch):
    """작업트리 상태와 무관하게 writer 의 provenance 를 clean 으로 — 검사하는 축은 계약이지 이 트리의 dirty 여부가 아니다."""
    prov = _prov_shared()
    monkeypatch.setattr(prov, "git_provenance", lambda *a, **k: {
        "git_commit": "0" * 40, "git_dirty": False, "git_modified_outputs": [], "git_modified_code": []})


def _shape_consumed(states):
    """production `main()` 이 만드는 모양 그대로 — 상태별 {matrix, half_cell} + pristine + literature."""
    import hashlib
    def hc(s):
        return {"path": f"data/half_cell/GITT/{s}.xlsx", "sha256": hashlib.sha256(f"hc{s}".encode()).hexdigest()}
    c = {s: {"matrix": {"file": f"synthetic-matrix/matrix_{s}.csv",
                        "sha256": hashlib.sha256(f"m{s}".encode()).hexdigest(),
                        "row": {"index": 8, "half_cell": "GITT", "si": "Li", "w_dqdv": "0.0", "run_id": "m"}},
             "half_cell": hc(s)} for s in states}
    c["pristine"] = {"half_cell": hc("pristine")}
    c["literature"] = {"gr": {"path": "gr.xlsx", "sha256": "3" * 64}, "si": {"path": "si.csv", "sha256": "4" * 64}}
    return c


def _pairing(states, authority=None, paired=None, missing_input=()):
    a = list(authority if authority is not None else states)
    r = list(states)
    avail = [s for s in r if s not in missing_input]
    p = list(paired if paired is not None else avail)
    return {"authority": a, "requested": r, "requested_from": "test", "available": avail,
            "missing_input": list(missing_input), "paired": p, "missing": [s for s in avail if s not in p],
            "rejected_matrix": {}, "note": "test"}


def _fresh_shape(d, states, *, consumed="auto", pairing=None, status="complete", **kw):
    """리뷰어 `fresh_shape_producer` 그대로 — **실제 writer**, 유한 합성 측정, solver 없음."""
    from types import SimpleNamespace
    shape = _shape_ns()
    rows = [(s, 12.0, 6.0, 0.5, 10.0, 5.0, 0.25, 0.2, 1.0, 0.5) for s in states]
    cap = {s: 99.0 for s in states}
    cwhere = {s: (s, 0.3, 10.0) for s in states}
    headroom = {s: {"dneg": -0.25, "dpos": 0.25, "fam_max": 20.0, "g_at_max": 0.5, "witness": 0.3, "wdelta": 0.1}
                for s in states}
    return shape._write_csv(d, SimpleNamespace(source="GITT", si_source="Li", out_dir="synthetic-matrix"),
                            rows, cap, 100.0, cwhere, headroom=headroom,
                            consumed=(_shape_consumed(states) if consumed == "auto" else consumed),
                            pairing=(pairing if pairing is not None else _pairing(states)), status=status, **kw)


def _u14(new, old=None):
    import subprocess
    root = pathlib.Path(__file__).resolve().parents[1]
    args = ["--new", str(new)] + (["--old", str(old)] if old is not None else ["--schema-only"])
    r = subprocess.run([sys.executable, str(root / "scripts/check_u14.py"), *args],
                       cwd=root, capture_output=True, text=True, timeout=180)
    line = next((l for l in r.stdout.splitlines() if l.startswith("PROMOTION ")), None)
    assert line, (r.returncode, r.stdout[-1500:], r.stderr[-1500:])
    return r.returncode, r.stdout + r.stderr, json.loads(line[len("PROMOTION "):])


def _shape_unit(art):
    import csv
    rows = list(csv.DictReader(art.open(encoding="utf-8")))
    meta = json.loads(art.with_name(art.name + ".meta.json").read_text(encoding="utf-8"))
    return rows, (list(rows[0]) if rows else []), meta


def test_g18_kind_routing_is_one_fail_closed_function():
    """`check_u14._kind` 와 `schema.body_roster` 가 각자 "matrix 아니면 profile" 이었다 — 모르는 이름이 profile 로
    읽혔다. 종류는 한 함수가 정하고, 모르면 **예외**다 (조용히 profile 이 아니라)."""
    from test_review_findings import _load_script
    for name, kind in (("matrix_100.csv", "matrix"), ("matrix_300_0009_v2.csv", "matrix"),
                       ("profile_gamma_100_Li.csv", "profile"), ("degeneracy_100_Li.json", "degeneracy"),
                       ("ne_shape_GITT_Li.csv", "shape"), ("out/ne_shape_step_005C_Li.csv", "shape")):
        assert S.kind_of(name) == kind, name
    for bad in ("foo.csv", "matrix_100.json", "ne_shape_GITT_Li.json", "notes.txt", ""):
        with pytest.raises(ValueError):
            S.kind_of(bad)
    with pytest.raises(ValueError):
        S.body_roster("foo.csv", b"state,run_id\n100,r\n")
    U = _load_script("check_u14")
    assert U._kind(pathlib.Path("x/ne_shape_GITT_Li.csv")) == "shape"
    with pytest.raises(ValueError):
        U._kind(pathlib.Path("foo.csv"))
    assert S.required_columns("shape") == S.SHAPE_ROW and "state" in S.SHAPE_ROW and "consumed_inputs" in S.SHAPE_ROW
    with pytest.raises(KeyError):
        S.required_columns("degeneracy")


def test_g19_unknown_artifact_name_is_a_structured_problem_not_a_profile(tmp_path):
    """디렉터리에 모르는 이름의 CSV 가 있으면 gate 는 그것을 profile 로 읽어 열 21 개를 요구하는 대신 **종류를
    모른다고** 말해야 한다."""
    import hashlib
    d = tmp_path / "u"; d.mkdir()
    f = d / "foo.csv"
    f.write_text("state,run_id\n100,R\n", encoding="utf-8")
    f.with_name("foo.csv.meta.json").write_text(json.dumps(
        {"artifact": "foo.csv", "run_id": "R", "sha256": hashlib.sha256(f.read_bytes()).hexdigest()}),
        encoding="utf-8")
    rc, out, promo = _u14(d)
    assert rc == 2 and "foo.csv: 모르는 산출 종류" in out, out[-1200:]
    assert "foo.csv: gamma_Si" not in out and "foo.csv: obj_ratio_to_best" not in out, out[-1200:]


def test_g20_fresh_shape_writer_output_passes_the_schema_gate(tmp_path, monkeypatch):
    """리뷰어 반례 그대로 (receipt 만 production 모양으로): 실제 writer 의 산출이 `--schema-only` 에서
    schema 0 · provenance_cols 0 · content 0 · unit 0 · provenance 0 이어야 한다."""
    _clean_git(monkeypatch)
    states = D.declared_states("GITT")
    d = tmp_path / "fresh"
    art = _fresh_shape(d, states)
    assert art.name == "ne_shape_GITT_Li.csv" and art.parent == d
    rc, out, promo = _u14(d)
    b = promo["blocked_by"]
    assert rc == 0 and promo["promotion_eligible"] is False and b["baseline_absent"] == 1, (rc, out[-2000:])
    assert all(b[k] == 0 for k in ("schema", "provenance_cols", "content", "unit", "provenance", "stale")), (b, out[-2000:])
    rows, header, meta = _shape_unit(art)
    assert header == list(S.SHAPE_ROW), header
    assert not S.check_rows("shape", rows, header, name=art.name)
    assert not S.check_shape_meta(meta, rows, art.name)


def test_g21_reviewer_literal_repro_is_rejected_only_for_its_missing_receipts(tmp_path, monkeypatch):
    """리뷰어 스크립트는 `consumed={"synthetic": True}` 를 넘긴다 — 그것은 receipt 가 아니다. 그 호출은 **receipt
    축에서만** 막혀야 한다 (열·sidecar·provenance 는 이제 맞는다)."""
    _clean_git(monkeypatch)
    states = D.declared_states("GITT")
    d = tmp_path / "lit"
    _fresh_shape(d, states, consumed={"synthetic": True})
    rc, out, promo = _u14(d)
    b = promo["blocked_by"]
    assert b["schema"] == 0 and b["provenance_cols"] == 0 and b["provenance"] == 0 and b["unit"] == 0, (b, out[-2000:])
    assert rc == 2 and b["content"] >= len(states), (b, out[-2000:])
    words = ("consumed_inputs", "inputs_sha", "receipt", "출처", "역할")
    lines = [l.strip() for l in out.splitlines() if l.strip().startswith("- ne_shape_GITT_Li.csv:")]
    assert lines and all(any(w in l for w in words) for l in lines), lines


def test_g22_shape_coverage_and_pairing_are_bound_to_the_declared_roster(tmp_path, monkeypatch):
    """모집단은 산출 안에서 닫히지 않는다 (P1-1 과 같은 축): 본문의 상태 집합은 `D.declared_states(source)` 와
    exact 로 대고, sidecar 의 pairing 은 그 명부·본문·typed status 와 산술적으로 맞아야 한다."""
    _clean_git(monkeypatch)
    states = D.declared_states("GITT")
    assert len(states) >= 2
    # (a) 좁힌 실행이 자기 authority 를 스스로 적고 complete 로 canonical 이름에 앉음
    sub = states[:1]
    art = _fresh_shape(tmp_path / "a", sub, pairing=_pairing(sub, authority=sub))
    rows, header, meta = _shape_unit(art)
    p = S.check_rows("shape", rows, header, name=art.name)
    assert any(q.startswith(S.CANONICAL_SLOT_PREFIX) for q in p), p        # 자리 규칙 (내용 결함이 아니다)
    assert not [q for q in p if not q.startswith(S.CANONICAL_SLOT_PREFIX)], p  # 내용은 멀쩡하다
    pm = S.check_shape_meta(meta, rows, art.name)
    assert any("authority" in q for q in pm), pm                             # 자기 선언 authority 는 정본이 아니다
    rc, out, promo = _u14(tmp_path / "a")
    assert rc == 2 and promo["blocked_by"]["content"] >= 2, out[-1500:]
    # (b) 선언에 없는 상태
    art = _fresh_shape(tmp_path / "b", states + ["999"], pairing=_pairing(states + ["999"], authority=states + ["999"]))
    rows, header, meta = _shape_unit(art)
    p = S.check_rows("shape", rows, header, name=art.name)
    assert any("999" in q and not q.startswith(S.CANONICAL_SLOT_PREFIX) for q in p), p
    # (c) pairing 이 본문과 다르다: paired 에 있는 상태의 행에 γ 짝이 없다 · status 가 pairing 의 뜻과 다르다
    art = _fresh_shape(tmp_path / "c", states)
    rows, header, meta = _shape_unit(art)
    assert not S.check_shape_meta(meta, rows, art.name)
    rows2 = [dict(r, gamma_target="", gamma_ref="") if r["state"] == states[0] else r for r in rows]
    assert any("paired" in q for q in S.check_shape_meta(meta, rows2, art.name))
    meta2 = dict(meta, status="partial")
    assert any("status" in q for q in S.check_shape_meta(meta2, rows, art.name))
    meta3 = dict(meta, pairing=dict(meta["pairing"], missing=[states[0]]))
    assert S.check_shape_meta(meta3, rows, art.name)
    meta4 = dict(meta); meta4.pop("pairing")
    assert any("pairing" in q for q in S.check_shape_meta(meta4, rows, art.name))
    # (d) 그리고 gate 가 sidecar 의 pairing 을 실제로 읽는다 — 파일에서 지우면 content 로 막힌다
    m = art.with_name(art.name + ".meta.json")
    j = json.loads(m.read_text(encoding="utf-8")); j["pairing"]["paired"] = []
    m.write_text(json.dumps(j, ensure_ascii=False), encoding="utf-8")
    rc, out, promo = _u14(tmp_path / "c")
    assert rc == 2 and "paired" in out, out[-1500:]


def test_g23_shape_sidecar_carries_the_u14_meta_contract(tmp_path, monkeypatch):
    """sidecar 는 U14 가 요구하는 전부를 담는다 — env · started_utc · git_commit_at_start ·
    git_state_changed_during_run · argv · roster(본문에서 유도) · shape 의 실행 조건 (state/starts/seed 가 아니라
    half_cell_source · si_source · grid_n · grid_range · gamma_grid)."""
    import re
    from test_review_findings import _load_script
    _clean_git(monkeypatch)
    U = _load_script("check_u14")
    states = D.declared_states("GITT")
    art = _fresh_shape(tmp_path / "m", states)
    rows, header, meta = _shape_unit(art)
    for k in (*U.META_KEYS, *U.META_REQUIRED, *S.meta_controls("shape")):
        assert meta.get(k) not in (None, ""), (k, sorted(meta))
    assert all(str(meta["env"].get(k) or "").strip() for k in S.ENV_KEYS), meta["env"]
    assert meta["git_state_changed_during_run"] is False and re.fullmatch(r"[0-9a-f]{40}", meta["git_commit_at_start"])
    assert meta["started_utc"] <= meta["created_utc"]
    assert isinstance(meta["argv"], list) and meta["argv"]
    assert meta["roster"] == S.body_roster(art.name, art.read_bytes())
    assert meta["roster"]["kind"] == "shape" and meta["roster"]["rows"] == len(states)
    assert meta["roster"]["state"] == sorted(states) and meta["roster"]["paired"] == sorted(states)
    assert S.meta_controls("shape") == ("half_cell_source", "si_source", "grid_n", "grid_range", "gamma_grid")
    for kind in ("matrix", "profile", "degeneracy"):
        assert S.meta_controls(kind) == S.META_CONTROLS
    # roster 를 바꾸면 gate 가 "본문에서 유도한 명부와 다르다" 로 막는다 (matrix·profile 과 같은 규칙)
    m = art.with_name(art.name + ".meta.json")
    j = json.loads(m.read_text(encoding="utf-8")); j["roster"]["paired"] = []
    m.write_text(json.dumps(j, ensure_ascii=False), encoding="utf-8")
    rc, out, promo = _u14(tmp_path / "m")
    assert rc == 2 and "roster" in out and promo["blocked_by"]["content"] >= 1, out[-1500:]


def test_g24_witness_columns_are_empty_together_and_science_cells_are_finite(tmp_path, monkeypatch):
    """R3-03: `gamma_witness`·`gamma_witness_delta` 의 빈 칸은 "격자에서 증인 없음" 이라 **둘이 함께** 비어야
    뜻이 있다. 나머지 과학 열은 비면 안 되고 유한해야 한다 (짝 없는 행의 nan 은 partial 의 증거지 success 가 아니다)."""
    _clean_git(monkeypatch)
    states = D.declared_states("GITT")
    art = _fresh_shape(tmp_path / "w", states)
    rows, header, _ = _shape_unit(art)
    ok = lambda rs: [q for q in S.check_rows("shape", rs, header, name=art.name)]   # noqa: E731
    assert not ok(rows)
    both = [dict(r, gamma_witness="", gamma_witness_delta="") for r in rows]
    assert not ok(both), ok(both)
    one = [dict(r, gamma_witness="") for r in rows]
    assert any("gamma_witness" in q for q in ok(one)), ok(one)
    unpaired = [dict(rows[0], gamma_target="", gamma_ref="", gamma_shape_mV="nan", ratio_b_over_a="nan")] + rows[1:]
    p = ok(unpaired)
    assert any("gamma_target" in q for q in p) and any("gamma_shape_mV" in q for q in p), p
    bad = [dict(rows[0], measured_shape_mV="inf")] + rows[1:]
    assert any("measured_shape_mV" in q for q in ok(bad))
    dup = rows + [rows[0]]
    assert any("중복" in q for q in ok(dup))


def test_g25_real_producer_through_the_wrapper_then_u14_and_a_second_run_reproduces(tmp_path):
    """producer→wrapper→U14 완주 (합성 원자료·fixture matrix, 실제 `ne_shape.py` · `shape_step` · `check_u14`):
    (1) 산출이 canonical 에 게시되고 schema-only 에서 계약 위반 0, (2) 두 번째 독립 실행은 첫 실행과 숫자·입력
    identity·조건이 같아 승격 자격(트리가 clean 이면)."""
    from test_r6_internal import _synth_root, _prov
    from test_r10_codex import _shell
    from test_r8_codex import _pair
    src = _synth_root(tmp_path)
    matrix = tmp_path / "matrix"; matrix.mkdir()
    for s in D.declared_states("GITT"):
        _pair(matrix, s)
    root = pathlib.Path(__file__).resolve().parents[1]

    def run(write):
        cmd = (f'shape_step "{write}" env PYTHONUNBUFFERED=1 {sys.executable} scripts/ne_shape.py --data-root "{src}" '
               f'--out-dir "{matrix}" --write "{write}" --source GITT --si-source Li; echo "STEP_RC=$?"')
        p = _shell(cmd, {"OUT": str(write)})
        text = p.stdout + p.stderr
        assert "STEP_RC=0" in text and "complete" in text, text[-2500:]
        assert (write / "ne_shape_GITT_Li.csv").is_file() and not (write / "partial").exists(), text[-800:]
        return text

    A, B = tmp_path / "A", tmp_path / "B"
    run(A); run(B)
    pv = _prov().git_provenance(cwd=str(root))
    dirty = 2 if pv["git_dirty"] else 0                   # SAFE_PROVENANCE 의 git_dirty · git_modified_code
    rc, out, promo = _u14(A)
    b = promo["blocked_by"]
    assert all(b[k] == 0 for k in ("schema", "provenance_cols", "content", "unit", "stale")), (b, out[-2500:])
    assert b["provenance"] == dirty, (b, out[-1500:])
    rc, out, promo = _u14(B, A)
    b = promo["blocked_by"]
    assert all(b[k] == 0 for k in ("schema", "provenance_cols", "content", "unit", "controls", "env", "numbers",
                                   "alias", "inputs", "inputs_uncomparable", "stale")), (b, out[-2500:])
    assert promo["roster"] == {"old": 1, "new": 1, "compared": 1, "missing_in_new": [], "extra_in_new": []}, promo
    if not pv["git_dirty"]:
        assert rc == 0 and promo["promotion_eligible"] is True, (rc, out[-1500:])


def test_g26_write_meta_refuses_an_unregistered_artifact_name(tmp_path):
    """production `write_meta` 는 명부를 `body_roster` 로 유도한다 — 등록되지 않은 이름이면 명부를 지어내지 않고
    **meta 도 쓰지 않는다** (fail-closed). 전 판은 `out/100.csv` 같은 이름을 profile 로 읽어 봉인했다 (열두 번째
    fixture 감사: `test_review_findings` 의 세 fixture 가 정확히 그 이름을 쓰고 있었다)."""
    import os, subprocess
    from test_review_findings import _fixture_repo, _shell_helpers
    root = tmp_path / "repo"; _fixture_repo(root, outputs=("out/foo.csv",))
    (root / "out" / "foo.csv").write_text("a,b,run_id\n3,4,rid-x\n", encoding="utf-8")
    env = dict(os.environ, STARTS="1", SI="Li", BMS_DATA_ROOT="synthetic")
    r = subprocess.run(["bash", "-c", _shell_helpers() + '\nLAST_RUN_ID=rid-x write_meta "$1" 100 GITT', "g26", "out/foo.csv"],
                       cwd=root, env=env, capture_output=True, text=True, encoding="utf-8")
    assert r.returncode != 0 and "등록된 종류" in r.stderr, (r.returncode, r.stderr[-600:])
    assert not (root / "out" / "foo.csv.meta.json").exists()
    # 등록된 이름은 같은 경로로 봉인된다 (대조군)
    (root / "out" / "matrix_100.csv").write_text("a,b,run_id\n3,4,rid-y\n", encoding="utf-8")
    r = subprocess.run(["bash", "-c", _shell_helpers() + '\nLAST_RUN_ID=rid-y write_meta "$1" 100 GITT', "g26", "out/matrix_100.csv"],
                       cwd=root, env=env, capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, r.stderr[-600:]
    meta = json.loads((root / "out" / "matrix_100.csv.meta.json").read_text(encoding="utf-8"))
    assert meta["roster"] == {"kind": "matrix", "rows": 1}, meta["roster"]


def test_g27_wrapper_shape_source_is_not_the_last_state_s_loop_variable(tmp_path):
    """[U18-01, 2026-09-13 실측] `STATES='100 200 300_0009 300_0147'` 본 실행(사용자 기계)이 shape 를
    **`ne_shape_step_005C_Li.csv`** 로 게시했다 — 정본은 `ne_shape_GITT_Li.csv` 다. main 의 호출이
    `--source "${SHAPE_SRC:-${SRC:-GITT}}"` 라서 loop 의 상태별 변수 `SRC` 가 **마지막 상태의 소스**(300_0147 은 step_005C
    전용)로 남아 새어 들어갔다. g25 는 `shape_step` 을 `--source GITT` 로 직접 불러 이 줄을 지나지 않았다.

    회귀는 production 스크립트를 **통째로** 돈다 — 적합 세 명령은 PATH shim 이 즉시 실패시키고(rc 7),
    `scripts/ne_shape.py` 호출은 argv 만 적는다. shape 소스는 SHAPE_SRC 없이는 GITT, 있으면 그것이고 요약 줄이 찍는다."""
    import os, subprocess
    repo = pathlib.Path(__file__).resolve().parents[1]
    root = tmp_path / "root"
    (root / "data/half_cell/GITT").mkdir(parents=True); (root / "data/half_cell/step_005C").mkdir(parents=True)
    (root / "data/half_cell/GITT/100.xlsx").write_bytes(b"")                  # 100 은 GITT 만
    (root / "data/half_cell/step_005C/300_0147_005C.xlsx").write_bytes(b"")   # 300_0147 은 step_005C 만 → pick_src 가 그리 고른다
    shim = tmp_path / "shim"; shim.mkdir()
    argv_out = tmp_path / "ne_shape_argv.txt"
    (shim / "python3").write_text(
        "#!/usr/bin/env bash\n"
        'for a in "$@"; do case "$a" in\n'
        "  bms_balancing.verify) exit 7 ;;\n"
        '  scripts/ne_shape.py) printf \'%s\\n\' "$@" > "$G27_ARGV"; echo "SHAPE_RESULT {}"; exit 1 ;;\n'
        "esac; done\n"
        'exec "$G27_REAL" "$@"\n', encoding="utf-8")
    (shim / "python3").chmod(0o755)

    def run(extra):
        env = dict(os.environ, BMS_DATA_ROOT=str(root), STATES="100 300_0147", STARTS="1", SI="Li",
                   OUT=str(tmp_path / "out"), G27_ARGV=str(argv_out), G27_REAL=sys.executable,
                   PATH=str(shim) + os.pathsep + str(pathlib.Path(sys.executable).parent) + os.pathsep
                        + os.environ.get("PATH", ""))
        env.pop("SHAPE_SRC", None); env.pop("SRC", None); env.update(extra)
        if argv_out.exists():
            argv_out.unlink()
        p = subprocess.run(["bash", str(repo / "scripts/run_states.sh")], cwd=repo, env=env,
                           capture_output=True, text=True, encoding="utf-8", timeout=600)
        text = p.stdout + p.stderr
        assert argv_out.exists(), text[-2500:]
        argv = argv_out.read_text(encoding="utf-8").splitlines()
        return argv[argv.index("--source") + 1], text

    src, text = run({})
    assert "100=GITT" in text and "300_0147=step_005C" in text, text[-1500:]   # 섞인 실행이 맞다
    assert src == "GITT", f"shape 소스가 마지막 상태의 loop 변수를 따랐다: {src!r}"
    assert "SHAPE_SRC=GITT" in text, text[-800:]                                # 요약 줄이 shape 소스를 찍는다
    src, text = run({"SHAPE_SRC": "step_005C"})                                  # 명시 override 는 그대로 따른다
    assert src == "step_005C" and "SHAPE_SRC=step_005C" in text, (src, text[-800:])


def test_g28_wrapper_start_provenance_knows_the_output_directory(tmp_path):
    """[U18-02, 2026-09-13 실측] `OUT=out_u18` 본 실행의 13 산출 중 **11 개**가
    `git_state_changed_during_run = True` 로 나와 승격이 막혔다. 트리는 실제로 깨끗했다 —
    `run` 의 시작 provenance 가 `python3 scripts/provenance.py "$art"` 라 CLI 기본값
    `output_roots=("out",)` 을 쓰고, `out_u18/` 은 그 밖의 **untracked 디렉터리**라 '코드 변경' 으로 잡혔다.
    끝 상태는 `write_meta` 가 `output_roots=(out_dir, "out")` 로 제대로 부르므로 False —
    그래서 "실행 중에 상태가 바뀌었다" 가 된다. 산출 하나당 한 번씩, 첫 산출만 빼고 (그때는 디렉터리가 비어
    있어 git 이 아무것도 보고하지 않는다 — 실측에서 `degeneracy_100` 만 clean 이었던 이유).

    이것은 위조 방향이 아니라 **거짓 양성**이다. 그러나 `provenance.py` 머리말이 경고하는 바로 그 고장 —
    "플래그가 늘 켜져 정보가 사라진다" — 을 wrapper 쪽에서 재현한 것이라 신호로서 죽는다.
    """
    import json as _json, os, subprocess
    from test_review_findings import _fixture_repo, _shell_helpers
    root = tmp_path / "repo"; _fixture_repo(root, outputs=("out/matrix_100.csv",))
    env = dict(os.environ, STARTS="1", SI="Li", BMS_DATA_ROOT="synthetic", OUT="out_alt")
    produce = ('python3 -c "import os,sys,pathlib; pathlib.Path(sys.argv[1]).write_text('
               "'a,b,run_id\\n3,4,' + os.environ['BMS_RUN_ID'] + '\\n')\" \"$1\"")
    body = ('mkdir -p "$OUT"\n'
            f'run "one" "$1" - "$3" {produce} && write_meta "$1" 100 GITT || exit 1\n'
            f'set -- "$2" "$1" "$3"\n'
            f'run "two" "$1" - "$3" {produce} && write_meta "$1" 200 GITT || exit 1\n'
            'echo BOTH_OK')
    one, two = root / "out_alt" / "matrix_100.csv", root / "out_alt" / "matrix_200.csv"
    r = subprocess.run(["bash", "-c", _shell_helpers() + "\n" + body, "g28", str(one), str(two),
                        str(tmp_path / "run.log")],
                       cwd=root, env=env, capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0 and "BOTH_OK" in r.stdout, (r.stdout[-1500:], r.stderr[-2500:])
    for art, when in ((one, "첫 산출 (디렉터리가 비어 있었다)"), (two, "둘째 산출 (앞 산출·로그가 이미 있다)")):
        m = _json.loads(art.with_name(art.name + ".meta.json").read_text(encoding="utf-8"))
        assert m["git_modified_code"] == [] and m["git_dirty"] is False, (when, m["git_modified_code"])
        assert m["git_dirty_at_start"] is False, (
            f"{when}: 산출 디렉터리가 시작 provenance 에서 코드 변경으로 잡혔다 — "
            f"{m.get('git_modified_code_at_start')}")
        assert m["git_state_changed_during_run"] is False, (when, m)


def test_g29_a_baseline_without_env_is_uncomparable_not_a_contract_violation(tmp_path):
    """[U18-03, 2026-09-13 실측] U18 대조가 rc **2**(계약 위반)를 냈고 그 근거는 정본 `ne_shape_GITT_Li.csv.meta`
    에 `env` 가 없다는 것 하나였다 — 옛 스키마로 만든 정본의 **나이**지 새 산출의 위반이 아니다. 자체 리뷰 C16 이
    입력 identity 축에서 닫은 것과 같은 비대칭이다: 정본이 안 적었으면 '대조 불가'(승격만 불가), 새 산출이 안
    적었으면 '계약 위반'. 새 산출 쪽의 존재는 `--schema-only` 에서도 도는 `env 가 비어 있다` 가 이미 요구한다.
    """
    import json as _json
    from test_r12_selfreview import _publish_matrix
    # ⚠ 열세 번째 fixture 감사: 3 행짜리 matrix 를 canonical 이름에 두면 R13 P1-1 이 막는다 (좁힌 실행은 정본이
    #   아니다) — env 축을 재려던 fixture 가 먼저 content 로 걸렸다. 정본 자리에는 정본 모집단을 둔다.
    rows = seal_combo(_canonical_combo_rows())
    old, new = tmp_path / "old", tmp_path / "new"
    _publish_matrix(old, rows, run_id="R-old"); _publish_matrix(new, rows, run_id="R-new")
    mp = old / "matrix_100.csv.meta.json"
    m = _json.loads(mp.read_text(encoding="utf-8")); m.pop("env")          # 옛 정본에는 키가 아예 없다
    mp.write_text(_json.dumps(m, ensure_ascii=False), encoding="utf-8")

    rc, out, promo = _u14(new, old)
    b = promo["blocked_by"]
    assert b["env"] == 0 and b.get("env_uncomparable") == 1, (b, out[-2500:])
    assert all(b[k] == 0 for k in ("schema", "provenance_cols", "content", "unit", "controls", "numbers",
                                   "alias", "inputs", "inputs_uncomparable", "provenance", "stale")), (b, out[-2500:])
    assert rc == 4 and promo["promotion_eligible"] is False, (rc, out[-2500:])

    # 대조군 — 새 산출이 env 를 안 적은 것은 그대로 계약 위반(rc 2)이다 (C16 의 비대칭)
    new2 = tmp_path / "new2"; _publish_matrix(new2, rows, run_id="R-new2")
    mp2 = new2 / "matrix_100.csv.meta.json"
    m2 = _json.loads(mp2.read_text(encoding="utf-8")); m2.pop("env")
    mp2.write_text(_json.dumps(m2, ensure_ascii=False), encoding="utf-8")
    rc2, out2, promo2 = _u14(new2, old)
    assert rc2 == 2 and promo2["blocked_by"]["schema"] >= 1, (rc2, promo2["blocked_by"], out2[-2000:])
