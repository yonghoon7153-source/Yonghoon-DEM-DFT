"""R6 내부 자체 리뷰 회귀 테스트 (2026-09-11, 대상 1049894 — Codex 토큰 소진으로 `/self-review` 4 렌즈 + 적대적 검증).

원장: `reviews/R6_LEDGER.md`. 렌즈 보고·재현 스크립트 사본: `reviews/r6_repros/`.
ID 규약 — V: validator 우회 · T: 순서/TOCTOU · D: 파생 보고서·공정성 · P: sig 완전성·이식성.

공통 반례(validator 렌즈): MATLAB rmse 가 Python 과 상대차 1e-3 ~ 1e-2 (`MODEL_REL` 의 10⁶ 배 이상) 인데
`%.2g` 로 찍으면 두 값이 같은 문자열 — 형식이 실제보다 거칠다고 **주장**하기만 하면 차이가 사라진다.
"""
from __future__ import annotations
import csv, json, pathlib, shutil, sys
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from conftest import fixture_env as _fixture_env   # noqa: E402  (R16: env 축은 한 자리에서)
from bms_balancing import verify                                      # noqa: E402
from test_review_findings import _r2_base, _r2_csv, _r2_run, audit_json   # noqa: E402


def _prov():
    import importlib.util
    spec = importlib.util.spec_from_file_location("provenance", ROOT / "scripts" / "provenance.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def _same_cell_but_different(pv, fmt=".2g"):
    """`fmt` 로 찍으면 pv 와 **같은 문자열**이지만 값은 상대차 ≥ 1e-6 (MODEL_REL 의 1000 배 이상) 만큼 다른 값.
    2 유효자리 칸의 마지막 자리 0.45 배만큼 위로 — 칸 안이라 거친 형식 아래서는 차이가 보이지 않는다."""
    import math
    t = format(pv, fmt); base = float(t)
    unit = 10 ** (math.floor(math.log10(abs(base))) - 1)
    mv = base + 0.45 * unit
    assert format(mv, fmt) == t and abs(mv - pv) / abs(pv) > 1e-6, (pv, mv, t)
    return mv


def _mat_rows(rows, fmt=".2g"):
    """파라미터 다섯은 그대로, rmse 값은 `%.2g` 칸 안에서 다른 값 — 'MATLAB 쪽이 다른 모델' 을 흉내낸다."""
    return [r[:5] + [_same_cell_but_different(x, fmt) for x in r[5:]] for r in rows]


def _rewrite(p, lines):
    p.write_text("\n".join(lines) + "\n", encoding="utf-8"); return p


# ── V6-01 · 헤더가 데이터 행 뒤에 오면 행별 검사(R4-04 열 수 · R5-01 재출력)가 한 번도 돌지 않는다 ──────────
def test_i6v_01_header_after_data_rows_is_malformed(tmp_path):
    """[R6 내부 V6-01] audit 의 행별 검사는 `header is not None` 뒤에만 돌고, header 는 스캔 순서로 정해진다.
    헤더가 위면 `%.2g` 선언 + 17 자리 토큰 → invalid 인데, 같은 파일의 헤더를 맨 아래로 옮기면 complete 였다
    (1.5 % 차이가 "적힌 자리수 안"). 어떤 writer 도 그 순서로 안 쓴다 — 그래서 옛 스키마가 아니라 malformed 다."""
    anchors, cols, P, py, rows = _r2_base()
    top = _r2_csv(tmp_path, anchors, cols, _mat_rows(rows), head=("# printed_format,%.2g",), name="top.csv")
    res_top, _ = _r2_run(anchors, P, py, top)
    assert res_top["status"] == "invalid"                                   # 대조군: 헤더 위 → 이미 invalid
    lines = top.read_text(encoding="utf-8").splitlines()
    hdr = next(l for l in lines if l.startswith("a_PE")); lines.remove(hdr); lines.append(hdr)
    bottom = _rewrite(tmp_path / "bottom.csv", lines)
    probs = verify.dd_eval_csv_audit(bottom, spec=verify.parse_precision_spec("%.2g"))
    assert probs and any("헤더" in m for m in probs), probs
    res, txt = _r2_run(anchors, P, py, bottom)
    assert res["status"] == "invalid", (res["status"], txt[-400:])


# ── V6-02 · `--precision` 옵션은 파일의 토큰과 대조되지 않았다 ────────────────────────────────────────
@pytest.mark.parametrize("head", [(), ("# printed_format,%.17e",), ("# printed_format,17",)],
                         ids=["no-declaration", "unparseable-declaration", "numeric-declaration"])
def test_i6v_02_precision_option_must_reproduce_the_tokens(tmp_path, head):
    """[R6 내부 V6-02] 선언이 없거나 해석 불가인 파일의 17 자리 토큰에 `--precision sig:2` 를 주면 complete 였다
    (audit 은 `declared_spec` 만 받고, '옵션이 느슨' 판정은 해석 가능한 선언이 있을 때만). 옵션은 "이 파일은 이
    형식으로 찍혔다" 는 주장이므로 토큰이 그 형식으로 재출력되지 않으면 그 주장이 틀린 것 → invalid."""
    anchors, cols, P, py, rows = _r2_base()
    p = _r2_csv(tmp_path, anchors, cols, _mat_rows(rows), head=head)
    res, txt = _r2_run(anchors, P, py, p, precision="sig:2")
    assert res["status"] == "invalid", (head, res["status"], txt[-400:])
    assert any("sig:2" in m or ".2g" in m for m in res["problems"]), res["problems"]
    # 대조군 (R4-02 Q3 그대로): 선언 `%.17g` 이 있으면 느슨한 옵션은 partial 이고 선언과의 충돌이 기록된다
    ctl = _r2_csv(tmp_path, anchors, cols, _mat_rows(rows), name="ctl.csv")
    res_c, _ = _r2_run(anchors, P, py, ctl, precision="sig:2")
    assert res_c["status"] == "partial" and res_c["precision_override_looser"], res_c["status"]


# ── V6-03 · 헤더 없는 파일: audit 전무 + 앞 두 열을 위치로 rmse 로 본다 — 존재한 적 없는 스키마 ────────────
def test_i6v_03_missing_header_is_malformed_not_old_schema(tmp_path):
    """[R6 내부 V6-03] `dd_eval.m` 은 첫 판(56a35a8:118)부터 헤더를 썼다. 헤더 없는 파일은 옛 산출이 아니라
    malformed 인데, 비교기는 앞 두 열을 rmse 로 보고 partial 을 주었고 `--allow-partial` 이면 0 이었다."""
    anchors, cols, P, py, rows = _r2_base()
    p = _r2_csv(tmp_path, anchors, cols, _mat_rows(rows), head=("# printed_format,%.2g",))
    _rewrite(p, [l for l in p.read_text(encoding="utf-8").splitlines() if not l.startswith("a_PE")])
    res, txt = _r2_run(anchors, P, py, p)
    assert res["status"] == "invalid", (res["status"], txt[-400:])
    assert any("헤더" in m for m in res["problems"]), res["problems"]


# ── V6-04 · `--allow-partial` 의 "스키마 누락" 에 하한이 없었다 ───────────────────────────────────────
def test_i6v_04_partial_needs_the_first_schema_columns(tmp_path):
    """[R6 내부 V6-04] rmse 열이 0 개(헤더 = 파라미터 다섯뿐)여도, 앵커까지 없어도 partial → `--allow-partial` 로 0
    ("앵커 0개와 rmse 0개가 전부 일치", compared=0/0). 첫 판(56a35a8) 도 `rmse_pocv,rmse_dvdq` 두 열은 썼다 —
    그 둘이 없으면 옛 스키마가 아니라 비교할 것이 없는 파일이다."""
    anchors, cols, P, py, rows = _r2_base()
    par = ["a_PE,b_PE,a_NE,b_NE,gamma_Si"] + [",".join(format(x, ".6f") for x in r[:5]) for r in rows]
    anc = ["# printed_format,%.17g"] + [f"# {k},{v:.17g}" for k, v in anchors.items()]
    res0, txt0 = _r2_run(anchors, P, py, _rewrite(tmp_path / "p0.csv", anc + par))       # rmse 열 0
    assert res0["status"] == "invalid", (res0["status"], txt0[-400:])
    res1, txt1 = _r2_run(anchors, P, py, _rewrite(tmp_path / "p1.csv", anc[:1] + par))   # 앵커도 0
    assert res1["status"] == "invalid", (res1["status"], txt1[-400:])
    p2 = _r2_csv(tmp_path, anchors, ["rmse_pocv"], [r[:6] for r in rows], name="p2.csv")  # dvdq 열 없음
    res2, txt2 = _r2_run(anchors, P, py, p2)
    assert res2["status"] == "invalid", (res2["status"], txt2[-400:])
    # 대조군: 진짜 옛 스키마 (rmse 2 열) 는 그대로 partial 이고 그 두 열은 비교된다
    p3 = _r2_csv(tmp_path, anchors, ["rmse_pocv", "rmse_dvdq"], [r[:7] for r in rows], name="p3.csv")
    res3, _ = _r2_run(anchors, P, py, p3)
    assert res3["status"] == "partial" and res3["compared"] == 2 * len(P), res3["status"]


# ── V6-05 · `verify_unit` 은 meta 의 run_id·sha256 만 보고 `artifact` 이름은 안 본다 ─────────────────────
def test_i6v_05_verify_unit_binds_the_meta_to_the_artifact_name(tmp_path):
    """[R6 내부 V6-05] `matrix_100.csv` + meta(`artifact=matrix_100.csv, state=100`) 를 `matrix_200.csv` 이름으로
    복사하면 `--verify-unit matrix_200.csv` 가 0 '일치' 였다. matrix 행에는 state 열이 없어 이름·meta 가
    상태 identity 의 전부다 — meta 의 `artifact` 가 파일 이름과 같아야 한 묶음이다."""
    prov = _prov(); rid = "r6-v05-run"
    art = tmp_path / "matrix_100.csv"; art.write_text(f"a,run_id\n1,{rid}\n", encoding="utf-8")
    meta = {"artifact": "matrix_100.csv", "state": "100", "run_id": rid, "sha256": prov.sha256_file(art)}
    (tmp_path / "matrix_100.csv.meta.json").write_text(json.dumps(meta), encoding="utf-8")
    assert prov.verify_unit(art) == (True, "일치")
    shutil.copy(art, tmp_path / "matrix_200.csv")
    shutil.copy(tmp_path / "matrix_100.csv.meta.json", tmp_path / "matrix_200.csv.meta.json")
    ok, why = prov.verify_unit(tmp_path / "matrix_200.csv")
    assert ok is False and "artifact" in why, (ok, why)


# ── V6-06 · `# printed_format,17` — audit 는 선언으로 세는데 meta 리더는 숫자라 버린다 ─────────────────
def test_i6v_06_numeric_printed_format_declaration_is_unparseable_not_absent(tmp_path):
    """[R6 내부 V6-06] `read_dd_eval_meta` 가 값이 숫자면 버려서 `resolve_precision` 은 '선언 없음(추정)' 으로 갔다
    → auto 에서 invalid(2) 가 아니라 partial/model_mismatch. R5-02 의 "역할은 값 변환 전에 이름으로" 를 meta
    리더에도 적용한다: `printed_format` 은 값이 무엇이든 선언이고, 해석 못 하면 invalid."""
    anchors, cols, P, py, rows = _r2_base()
    p = _r2_csv(tmp_path, anchors, cols, rows, head=("# printed_format,17",))
    assert verify.read_dd_eval_meta(p).get(verify.PRINTED_FORMAT_KEY) == "17"
    assert verify.declared_precision(p) == "invalid"
    pol = verify.resolve_precision(p)
    assert pol["source"] == "invalid" and pol["declared_raw"] == "17", pol
    res, txt = _r2_run(anchors, P, py, p)                   # 값은 전부 같아도 선언 해석 불가 → invalid
    assert res["status"] == "invalid", (res["status"], txt[-300:])


# ── V6-07 · `--compare` 경로가 없으면 traceback 으로 종료 1 = README 의 "1 갈림" ────────────────────────
def test_i6v_07_unreadable_compare_path_is_incomplete_not_a_model_mismatch(tmp_path):
    """[R6 내부 V6-07] `cmd_eval` 은 ValueError 만 잡았다 — 없는 경로·디렉터리는 OSError traceback 으로 rc 1
    (판정 줄 없음). 못 읽은 파일은 '갈림' 이 아니라 대조 미완(2) 이다."""
    anchors, cols, P, py, rows = _r2_base()
    res, txt = _r2_run(anchors, P, py, tmp_path / "does_not_exist.csv")
    assert verify.EXIT_BY_STATUS[res["status"]] == 2, (res["status"], txt[-300:])
    res_d, txt_d = _r2_run(anchors, P, py, tmp_path)         # 디렉터리
    assert verify.EXIT_BY_STATUS[res_d["status"]] == 2, (res_d["status"], txt_d[-300:])


# ── V6-08 · `check_run_id` 의 CSV 분기는 DictReader — `run_id` 열이 둘이면 마지막 열만 본다 ─────────────
def test_i6v_08_duplicate_run_id_column_is_not_a_match(tmp_path):
    """[R6 내부 V6-08] 첫 `run_id` 열이 다른 시도의 id 여도 '전 행 일치'. dd_eval audit 의 '중복 열' 과 비대칭이었다."""
    prov = _prov()
    p = tmp_path / "dup.csv"; p.write_text("run_id,x,run_id\nother-run,1,the-run\n", encoding="utf-8")
    ok, why = prov.check_run_id(p, "the-run")
    assert ok is False and "run_id" in why, (ok, why)


# ═══════════════════════════════════════════════════════════════════════════════════════════════════════
# D · 파생 보고서 · 공정성 렌즈 (DF-01…DF-10; 검증 판정 `reviews/r6_repros/derived/VERDICT.md`)
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════
import csv, inspect, re                                                   # noqa: E402
import numpy as np                                                        # noqa: E402
from test_review_findings import NOT_A_CLAIM, _section                    # noqa: E402

OUT = ROOT / "out"


def _doc(name): return (ROOT / name).read_text(encoding="utf-8")
def _live(txt): return NOT_A_CLAIM.sub("", txt)                           # 취소선·따옴표 인용은 주장이 아니다
def _rows(p): return list(csv.DictReader((ROOT / p).open(encoding="utf-8", newline="")))


def test_i6d_01_section_3_4_says_the_profile_grid_contains_the_constrained_endpoints():
    """[R6 내부 DF-01] 힌트 격자는 `pad = span/2`, 21 점 → grid[5]·grid[15] 가 **정확히** 제약 최적화의 min·max 다.
    LLI 의 "정확히 일치 (15.1517 / 16.2350)" 는 두 방법이 독립적으로 같은 값에 닿은 것이 아니라 같은 격자점을
    되돌려 준 것이다 — 세 mode 모두 profile.max == ext.max 가 비트 단위로 같다. §3-4 는 힌트는 밝혔지만
    "끝점 = 격자점" 은 밝히지 않은 채 '독립 수렴' 이라고 적었다. 폭 1.0832 와 `is_lower_bound` 는 그대로다."""
    j = json.loads((OUT / "degeneracy_300_0009_Li.json").read_text(encoding="utf-8"))     # Codex R6-04: 정본은 unversioned
    for k in ("LAM_PE", "LAM_NE", "LLI"):
        sp = j[f"{k}_percent"]; ext = sp["from_constrained_extrema"]; prof = sp["from_mode_profile"]
        g_lo, g_hi = prof["grid_range_pct"]; grid = np.linspace(g_lo, g_hi, 21)
        assert abs(grid[5] - ext["min"]) < 1e-9 and abs(grid[15] - ext["max"]) < 1e-9, (k, grid[5], ext, grid[15])
        assert prof["max"] == ext["max"], (k, prof["max"], ext["max"])
    sec = _live(_section(_doc("FINDINGS.md"), "### 3-4"))
    assert "격자점" in sec and "독립 수렴이 아니" in sec, sec[:400]
    for stale in ("두 경로에서 독립적으로 나온다", "두 독립 방법이 수렴했다", "같은 값에 수렴**했다"):
        assert stale not in sec, stale
    assert "두 독립 방법이 수렴했다" not in _live(_doc("FINDINGS.md")).split("### 3-4")[1].split("\n")[0]


def test_i6d_02_secondary_docs_do_not_keep_the_retracted_cell_conclusions():
    """[R6 내부 DF-02] §0-2 가 철회한 결론("대체를 배제했다", "정확히 반대", "식별 가능성은 두 셀에서 똑같다",
    "순위가 통째로 뒤집힌다", "우리 대체 탓이 아니다", "대조가 배제한 것은 반쪽전지 대체 하나") 이 HANDOFF §5 ·
    INTRO §6-2 에 취소선 없이 남아 같은 문서의 정정판(HANDOFF §4 · INTRO §6-1) 과 모순됐다. R2 C13/C14 는 그 두
    절만 고쳤다."""
    stale = ("대체를 배제했다", "정확히 반대", "식별 가능성은 두 셀에서", "똑같다**", "순위가 통째로 뒤집힌다",
             "우리 대체 탓이 아니다", "대조가 배제한 것은")
    for name in ("HANDOFF_TO_GATE.md", "INTRO.md"):
        live = _live(_doc(name))
        hits = [s for s in stale if s in live]
        assert not hits, (name, hits)


def test_i6d_03_raw_lli_ratio_names_its_statistic():
    """[R6 내부 DF-03] "원통형 LLI 하한 폭이 raw 로 5~10 배" — §1-12 의 raw 행은 max/max 10.52 · min/min 9.66 ·
    med/med 10.04 이고 상태별 쌍 비는 5.1~18.3 배다. 문서가 이름붙인 어느 통계량도 '5~10' 을 주지 않는다 →
    요약문은 통계량 이름과 함께 §1-12 표의 값을 적는다."""
    raw_row = next(l for l in _doc("FINDINGS.md").splitlines() if l.startswith("| raw |"))
    mm = re.search(r"\|\s*([0-9.]+)x\s*\|\s*([0-9.]+)x\s*\|\s*([0-9.]+)x", raw_row)
    assert mm, raw_row
    max_max = float(mm.group(1))
    for name in ("FINDINGS.md", "HANDOFF_TO_GATE.md", "WORKING_STATE.md"):
        live = _live(_doc(name))
        assert "5~10 배" not in live and "5 ~ 10 배" not in live, name
        assert f"max/max {max_max:.1f}" in live, (name, max_max)


def test_i6d_04_working_state_test_count_matches_the_collection():
    """[R6 내부 DF-04] "86 passed 기대" 가 87 개짜리 트리에 남았다 (Codex R5 §1 이 지난 라운드에 74/75 로 같은
    종류를 짚었다). 문서의 기대 수는 수집된 테스트 수와 같아야 한다."""
    import subprocess
    out = subprocess.run([sys.executable, "-m", "pytest", "tests/", "--collect-only", "-q", "-p", "no:cacheprovider"],
                         cwd=ROOT, capture_output=True, text=True).stdout
    n = int(re.search(r"(\d+) tests? collected", out).group(1))          # 매개변수화된 항목까지 센 수 = "N passed"
    m = re.search(r"# (\d+) passed 기대", _doc("WORKING_STATE.md"))
    assert m and int(m.group(1)) == n, (m and m.group(0), n)


def test_i6d_05_the_192_values_are_raw_rmse_and_the_docs_do_not_tie_u13_to_them():
    """[R6 내부 DF-05] `cmd_eval` 은 `obj.rmse_*` (raw) 를 찍고 그 정의는 `scales` 를 안 본다 — scale 은 `__call__`
    만 소비한다. 그러니 scale 동치(U13) 는 적합 산출의 목적함수 조건이지 192 값의 조건이 아니고, R5-09 가 말한
    "96/192 빈틈" 은 192 값에는 없던 빈틈이다. §0-1·§1-13 은 U13 을 192 값에 묶었다."""
    from bms_balancing import model
    for fn in ("rmse_pocv", "rmse_dvdq", "rmse_dqdv"):
        assert "scales" not in inspect.getsource(getattr(model.Objective, fn)), fn
    assert "scales" in inspect.getsource(model.Objective.__call__)
    live = _live(_doc("FINDINGS.md"))
    assert "192 값의 Python 쪽 build 는 그 조건 안" not in live
    assert "빈틈은 이 실측으로 메워졌다" not in live
    assert "scale 을 소비하지 않" in live


def test_i6d_06_section_4_0_states_the_tolerance_behind_its_counts():
    """[R6 내부 DF-06] "6 개에서 목적함수가 나빠졌다 · 17 조합은 더 좋아졌다 · 나빠진 6 개는 전부 w_dqdv=1" 은 상대
    변화 1e-9 초과만 셀 때의 숫자다 — 부호만 보면 10·22·0 이고 w=0 도 (1e-9 아래로) 나빠진다. 본문에 문턱이 없었다."""
    k = lambda r: (r["half_cell"], r["si"], float(r["w_dqdv"]))
    # ⚠ U14-05: 수정 **전** 산출은 `out/archive/matrix_300_0009_premultistart.csv` 에 있다 — U14 재실행이
    #   `out/matrix_300_0009.csv` 를 덮으면서 그 자리의 v1 이 사라졌다 (재실행은 수정된 코드라 v2 를 재현한다).
    d1 = {k(r): float(r["obj"]) for r in _rows("out/archive/matrix_300_0009_premultistart.csv")}
    d2 = {k(r): float(r["obj"]) for r in _rows("out/matrix_300_0009.csv")}          # = 옛 _v2 (U14 가 비트 단위 재현)
    def count(tol):
        w = [kk for kk in d2 if (d2[kk] - d1[kk]) / d1[kk] > tol]; b = [kk for kk in d2 if (d2[kk] - d1[kk]) / d1[kk] < -tol]
        return len(w), len(b), len(d2) - len(w) - len(b), all(kk[2] == 1.0 for kk in w)
    assert count(1e-9) == (6, 17, 9, True), count(1e-9)
    assert count(0.0)[:3] == (10, 22, 0) and count(0.0)[3] is False, count(0.0)
    sec = _live(_section(_doc("FINDINGS.md"), "### 4-0"))
    assert "1e-9" in sec and "부호만" in sec, sec[-600:]


def test_i6d_07_section_1_10_carries_the_lower_bound_qualifier():
    """[R6 내부 DF-07] §1-10 은 네 JSON 이 전부 `is_lower_bound: true` 인데 "다른 세 상태는 전부 양수 구간이다",
    "순위가 완전히 일관된다 — 이것이 … 답이다" 를 탐색 하한 한정어 없이 적었다 (§0-1·§1-12 에는 있음)."""
    for st in ("100", "200", "300_0009", "300_0147"):
        j = json.loads((OUT / f"degeneracy_{st}_Li.json").read_text(encoding="utf-8"))
        assert j["LLI_percent"]["is_lower_bound"] is True, st
    sec = _live(_section(_doc("FINDINGS.md"), "### 1-10"))
    hdr = next(l for l in sec.splitlines() if l.startswith("| state |"))
    assert "하한" in hdr, hdr
    assert sec.count("탐색 하한") >= 3, sec.count("탐색 하한")
    assert "전부 양수 구간이다" not in sec


def test_i6d_08_section_4_1_free_reference_width_is_the_width_of_the_values():
    """[R6 내부 DF-08] 기준 자유 3 종(Jiang·Kunz·Li) 의 LAM_NE 폭은 원값으로 2.1016 — "2.11" 은 두 자리로 반올림한
    표값끼리의 차(7.90 − 5.79) 였다."""
    g = [r for r in _rows("out/matrix_300_0009.csv") if r["half_cell"] == "GITT" and float(r["w_dqdv"]) == 0 and r["ref_bounds"] == "-"]
    v = [float(r["LAM_NE_pct"]) for r in g]
    assert len(v) == 3 and abs(max(v) - min(v) - 2.1016) < 5e-5, v
    sec = _live(_section(_doc("FINDINGS.md"), "### 4-1"))
    assert "2.10 %p" in sec and "2.11 %p" not in sec, sec[-400:]


def test_i6d_09_section_3_3_cites_the_matrix_row_that_actually_matches():
    """[R6 내부 DF-09] `best` 의 LAM/LLI 가 "`out/matrix_300_0009.csv` 의 GITT/Li/w0 행과 일치" — DF-09 당시 그 이름은
    v1(수정 전) 이라 Δ 5.5e-5 %p 였고 비트 단위로 같은 것은 `_v2` 행이었다. U14-05 로 v1 은 archive 에, U14 재실행이
    `_v2` 를 비트 단위로 재현해 지금은 unversioned 이름이 Δ 0 인 정본이다 (Codex R6-04) — 인용은 그 이름으로."""
    bm = json.loads((OUT / "degeneracy_300_0009_Li.json").read_text(encoding="utf-8"))["best_modes_percent"]
    pick = lambda p: next(r for r in _rows(p) if r["half_cell"] == "GITT" and r["si"] == "Li" and float(r["w_dqdv"]) == 0)
    d1 = max(abs(bm[k] - float(pick("out/archive/matrix_300_0009_premultistart.csv")[k + "_pct"])) for k in bm)      # U14-05: 수정 전 판은 archive 에
    d2 = max(abs(bm[k] - float(pick("out/matrix_300_0009.csv")[k + "_pct"])) for k in bm)
    assert d2 == 0.0 and d1 > 1e-6, (d1, d2)
    sec = _live(_section(_doc("FINDINGS.md"), "### 3-3"))
    assert "`out/matrix_300_0009.csv` 의 GITT/Li/w0 행과 일치" in sec, sec[-500:]
    assert "_v2.csv` 의 GITT/Li/w0 행과 일치" not in sec                    # Codex R6-04: 인용은 정본 이름으로


def test_i6d_10_intro_6_3_does_not_keep_the_retracted_n_equals_1_sentence():
    """[R6 내부 DF-10] INTRO §6-3 "n=1 에서는 분산을 추정할 수 없다 … 산수다" 와 제목 "산수라서 진짜 못 한다" 는
    같은 절 마지막 문단과 FINDINGS §7-3 ("그건 틀렸다") 이 철회한 문장이다."""
    live = _live(_doc("INTRO.md"))
    assert "분산을 추정할 수 없다" not in live and "산수라서 진짜 못 한다" not in live
    assert "고차 차분" in live


# ═══════════════════════════════════════════════════════════════════════════════════════════════════════
# T · 순서/TOCTOU 렌즈 (F01…F08; 검증 판정 `reviews/r6_repros/toctou/VERDICT.md`)
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════
import hashlib, os, subprocess, time                                     # noqa: E402
from test_review_findings import (_fixture_repo, _shell_helpers, _load_script,   # noqa: E402
                                  _r5_matrix, _r5_ne_shape_real_pairs)


def _degeneracy_block() -> str:
    """run_states.sh 의 degeneracy 게시 블록 **원문** (matrix 블록 직전까지)."""
    sh = (ROOT / "scripts" / "run_states.sh").read_text(encoding="utf-8")
    start_key = 'tmp="$OUT/.degeneracy_' if 'tmp="$OUT/.degeneracy_' in sh else 'run "degeneracy $st"'
    start = sh.rfind("\n", 0, sh.index(start_key)) + 1
    end = sh.rfind("\n", 0, sh.index('run "matrix $st"')) + 1
    return sh[start:end]


_DEG_STUB = r'''
import json, os, sys, time, pathlib
args = sys.argv[1:]
def opt(name, default=None):
    return args[args.index(name) + 1] if name in args else default
if os.environ.get("STUB_STARTED"):
    pathlib.Path(os.environ["STUB_STARTED"]).write_text("x")
if os.environ.get("STUB_WAIT"):
    t = time.monotonic() + 60
    while not pathlib.Path(os.environ["STUB_WAIT"]).exists():
        assert time.monotonic() < t, "wait timeout"
        time.sleep(0.02)
obj = {"run_id": os.environ["BMS_RUN_ID"], "role": os.environ["ROLE"], "state": opt("--state"),
       "n_starts": int(opt("--starts", "0")), "LLI_percent": {"is_lower_bound": True}, "pad": "x" * int(os.environ.get("STUB_PAD", "0"))}
out = opt("--out")
if out:
    sys.path.insert(0, os.environ["ROOTDIR"])
    from bms_balancing.verify import atomic_write_json
    atomic_write_json(out, obj); print(f"wrote {out}")
else:
    print(json.dumps(obj))
'''


def _python_wrapper(tmp_path, stub):
    """PATH 맨 앞의 `python3`: `-m bms_balancing.verify degeneracy …` 만 stub 으로 보내고 나머지는 진짜 python."""
    b = tmp_path / "bin"; b.mkdir(exist_ok=True)
    w = b / "python3"
    w.write_text(f'''#!/usr/bin/env bash
if [ "$1" = "-m" ] && [ "$2" = "bms_balancing.verify" ] && [ "$3" = "degeneracy" ]; then shift 3; exec "$REAL_PY" "{stub}" "$@"; fi
exec "$REAL_PY" "$@"
''', encoding="utf-8"); w.chmod(0o755)
    return b


def test_i6t_01_degeneracy_publish_survives_a_slow_earlier_attempt(tmp_path):
    """[R6 내부 F01] degeneracy 의 `.part` 는 시도마다 **같은 이름**이고 producer 의 **stdout fd** 였다. 느린 B 가 계산
    중일 때 빠른 A 가 검사→`flock mv`→write_meta→verify-unit 을 전부 통과한 뒤 B 가 JSON 을 찍으면, B 의 fd 는
    rename 된 inode = 이미 게시된 JSON 이라 잠금·검사 밖에서 게시 파일이 B 의 bytes 로 바뀐다: JSON=B · meta=A ·
    A "전부 통과" · B FAIL (R5-04 의 "마지막 온전한 묶음만 남는다" 가 이 경로에서 거짓). 이제 degeneracy 도 `--out`
    으로 잠금 안에서 원자적으로 게시하고 stdout 은 로그다 — 마지막 게시자(B)의 묶음이 온전하게 남는다."""
    root = tmp_path / "repo"; _fixture_repo(root, outputs=())
    stub = tmp_path / "deg_stub.py"; stub.write_text(_DEG_STUB, encoding="utf-8")
    body = ('\nst=100; SI=Li; SRC=GITT; fail=0\n' + _degeneracy_block() + '\necho "FAIL_COUNT $fail"\n')
    def env(role, **extra):
        return dict(os.environ, PATH=f"{_python_wrapper(tmp_path, stub)}:{os.environ['PATH']}", REAL_PY=sys.executable,
                    ROLE=role, ROOTDIR=str(ROOT), OUT=str(root / "out"), SI="Li", BMS_DATA_ROOT="synthetic", **extra)
    cmd = ["bash", "-c", _shell_helpers() + body, "t01"]
    b = subprocess.Popen(cmd, cwd=root, env=env("B", STARTS="24", STUB_WAIT=str(tmp_path / "B.go"), STUB_STARTED=str(tmp_path / "B.started")),
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    t = time.monotonic() + 30
    while not (tmp_path / "B.started").exists():
        assert time.monotonic() < t and b.poll() is None, b.communicate()
        time.sleep(0.02)
    a = subprocess.run(cmd, cwd=root, env=env("A", STARTS="4"), capture_output=True, text=True, timeout=120)
    (tmp_path / "B.go").write_text("go")
    bo, be = b.communicate(timeout=120)
    art = root / "out" / "degeneracy_100_Li.json"
    prov = _prov(); ok, why = prov.verify_unit(art)
    j = json.loads(art.read_text(encoding="utf-8")); meta = json.loads((root / "out" / "degeneracy_100_Li.json.meta.json").read_text(encoding="utf-8"))
    assert ok is True and j["run_id"] == meta["run_id"], (ok, why, j.get("role"), j.get("run_id"), meta["run_id"], a.stderr[-400:], be[-400:])
    assert j["role"] == "B" and meta["starts"] == 24, (j["role"], meta["starts"])       # 마지막 게시자의 묶음
    assert a.returncode == 0 and "FAIL_COUNT 0" in a.stdout, (a.stdout, a.stderr[-500:])
    assert b.returncode == 0 and "FAIL_COUNT 0" in bo, (bo, be[-500:])
    assert not list((root / "out").glob(".degeneracy_*")), list((root / "out").iterdir())   # 고정 이름 .part 없음


def test_i6t_02_ne_shape_publishes_csv_and_meta_as_one_locked_attempt(tmp_path, monkeypatch):
    """[R6 내부 F02] `ne_shape._write_csv` 는 최종 경로를 `open("w")` 로 직접 쓰고(비원자) git 조회 뒤 meta 를 따로
    썼다 — 잠금·run_id·sha256 셋 다 없어 두 시도가 끼어들면 CSV=B · meta(consumed_inputs)=A 가 남고 `verify_unit`
    은 '옛 meta' 로 검출 불가였다. 이제 run_states 의 게시 규약과 같다: 행마다 run_id, meta 에 sha256, 같은 잠금 안."""
    cwd = tmp_path / "repo"; _fixture_repo(cwd, outputs=())
    _r5_matrix(cwd / "out" / "matrix_100.csv", 0.16)
    row, meta = _r5_ne_shape_real_pairs(tmp_path, monkeypatch, cwd)
    art = cwd / "out" / "ne_shape_GITT_Li.csv"
    assert _prov().verify_unit(art) == (True, "일치"), (_prov().verify_unit(art), meta)
    rows = list(csv.DictReader(art.open(encoding="utf-8")))
    assert rows and all(r["run_id"] == meta["run_id"] for r in rows), (rows[0], meta.get("run_id"))
    assert meta["sha256"] == hashlib.sha256(art.read_bytes()).hexdigest()


def test_i6t_03_fitted_pair_info_hashes_the_bytes_it_parsed(tmp_path, monkeypatch):
    """[R6 내부 F03] `fitted_pair_info` 는 `f.open()` 으로 행을 고른 **뒤** `f.read_bytes()` 로 다시 열어 해시했다 —
    그 사이 matrix 가 다시 게시되면 행은 옛 파일, sha256 은 새 파일. bytes 를 한 번 읽어 그것을 파싱하고 해시한다."""
    m = _load_script("ne_shape")
    out = tmp_path / "out"; out.mkdir()
    _r5_matrix(out / "matrix_100.csv", 0.16)
    old = (out / "matrix_100.csv").read_bytes()
    new = old.replace(b"0.160000", b"0.450000").replace(b"0.16,", b"0.45,")
    assert new != old
    # ⚠ 재게시는 CSV·meta 를 **한 묶음**으로 바꾼다 (Codex R5-04) — 시나리오를 그대로 두려면 sidecar 도 새 bytes 것이다.
    #   (전 판 fixture 는 옛 meta 를 남겨 뒀는데, R11 P1-7 로 reader 가 묶음 검사를 하면서 거기서 먼저 멈췄다.)
    import hashlib as _h, json as _j
    from bms_balancing import schema as _S
    m_path = out / "matrix_100.csv.meta.json"
    meta = _j.loads(m_path.read_text(encoding="utf-8"))
    meta["sha256"] = _h.sha256(new).hexdigest(); meta["roster"] = _S.body_roster("matrix_100.csv", new)
    m_path.write_text(_j.dumps(meta), encoding="utf-8")
    real = pathlib.Path.read_bytes
    monkeypatch.setattr(pathlib.Path, "read_bytes", lambda self: new if self.name == "matrix_100.csv" else real(self))
    info = m.fitted_pair_info(out, "100", "GITT", "Li")
    src = new if info["gamma_target"] == 0.45 else old
    assert info["sha256"] == hashlib.sha256(src).hexdigest(), (info["gamma_target"], info["sha256"][:12])


def test_i6t_04_meta_records_the_git_state_at_start_and_flags_a_change_during_the_run(tmp_path):
    """[R6 내부 F04] meta 의 `git_commit`/`git_dirty` 는 계산 **뒤** write_meta 에서 한 번 샘플됐다 — 10 시간 실행 중
    트리를 정리하거나 커밋하면 "돌린 코드가 commit 과 같았나" 에 거짓 답이 가능. `run` 이 명령 **전** 상태와 시작
    시각을 찍고 write_meta 가 둘을 비교해 `git_state_changed_during_run` 을 남긴다."""
    root = tmp_path / "repo"; git = _fixture_repo(root, outputs=())
    art = root / "out" / "matrix_100.csv"
    worker = tmp_path / "worker.py"
    worker.write_text('''import os, sys, subprocess, pathlib
out = pathlib.Path(sys.argv[1]); out.write_text("a,run_id\\n1," + os.environ["BMS_RUN_ID"] + "\\n", encoding="utf-8")
pathlib.Path("code.py").write_text("value = 2\\n", encoding="utf-8")           # 실행 중 코드가 바뀌고 커밋된다
subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qam", "during"], check=True)
''', encoding="utf-8")
    body = '\nrun "matrix 100" "$1" - "$2" "$REAL_PY" "$WORKER" "$1" && write_meta "$1" 100 GITT && echo WRITER_OK\n'
    env = dict(os.environ, STARTS="1", SI="Li", BMS_DATA_ROOT="synthetic", OUT=str(root / "out"),
               REAL_PY=sys.executable, WORKER=str(worker))
    sha_before = git("rev-parse", "HEAD").strip()
    r = subprocess.run(["bash", "-c", _shell_helpers() + body, "t04", str(art), str(tmp_path / "t04.log")],
                       cwd=root, env=env, capture_output=True, text=True, timeout=60)
    assert r.returncode == 0 and "WRITER_OK" in r.stdout, (r.stdout, r.stderr[-500:])
    meta = json.loads((root / "out" / "matrix_100.csv.meta.json").read_text(encoding="utf-8"))
    assert meta["git_commit_at_start"] == sha_before and meta["git_commit"] != sha_before, meta
    assert meta["git_state_changed_during_run"] is True and meta["started_utc"] <= meta["created_utc"], meta


def test_i6t_05a_verify_unit_can_require_this_attempts_run_id(tmp_path):
    """[R6 내부 F05a] `--verify-unit` 은 디스크 meta ↔ 디스크 bytes 만 봤다 — 이 시도의 id 를 받지 않아, A 의 write_meta
    뒤 B 가 CSV+meta 를 다 게시하면 A 의 verify-unit 이 B/B 를 보고 통과해 A 가 "OK [run_id A] · 전부 통과" 를 찍었다."""
    prov = _prov(); art = tmp_path / "x.csv"; art.write_text("a,run_id\n1,bbbb\n", encoding="utf-8")
    (tmp_path / "x.csv.meta.json").write_text(json.dumps({"artifact": "x.csv", "run_id": "bbbb", "sha256": prov.sha256_file(art)}), encoding="utf-8")
    assert prov.verify_unit(art) == (True, "일치")
    ok, why = prov.verify_unit(art, "aaaa")
    assert ok is False and "aaaa" in why, (ok, why)
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "provenance.py"), "--verify-unit", str(art), "aaaa"], capture_output=True, text=True)
    assert r.returncode == 1 and "aaaa" in r.stdout, (r.returncode, r.stdout, r.stderr[-300:])


def test_i6t_05b_shell_reports_why_the_unit_check_failed(tmp_path):
    """[R6 내부 F05b] wrapper 는 verify-unit 의 이유를 `>/dev/null` 로 버려 stderr 에 한 줄도 없었고 요약이 가리킨 `.log` 는
    다른 시도가 덮어쓴 것이었다. `verify_unit_or_say` 가 이유를 stderr 로 말한다."""
    root = tmp_path / "repo"; _fixture_repo(root, outputs=())
    art = root / "out" / "x.csv"; art.write_text("a,run_id\n1,bbbb\n", encoding="utf-8")
    (root / "out" / "x.csv.meta.json").write_text(json.dumps({"artifact": "x.csv", "run_id": "bbbb", "sha256": "0" * 64}), encoding="utf-8")
    r = subprocess.run(["bash", "-c", _shell_helpers() + '\nverify_unit_or_say "$1" bbbb\n', "t05b", str(art)],
                       cwd=root, env=dict(os.environ, OUT=str(root / "out")), capture_output=True, text=True, timeout=60)
    assert r.returncode == 1 and "sha256" in r.stderr, (r.returncode, r.stdout, r.stderr[-400:])


def test_i6t_06_lock_and_temp_names_are_ignored_by_git():
    """[R6 내부 F06] `<산출>.lock` 과 `atomic_write_csv`/write_meta 의 임시 이름은 `.gitignore` 밖이라 `??` 로 남고
    `git clean -fd` 대상이었다 — 잠금 파일이 지워지면 다음 시도가 새 inode 를 잠가 배타가 사라진다."""
    for rel in ("out/matrix_100.csv.lock", "out/matrix_100.csv.ab12cd.part", "out/matrix_100.csv.meta.ab12cd.part",
                "out/recompare/x.csv.lock"):
        r = subprocess.run(["git", "check-ignore", "-q", rel], cwd=ROOT, capture_output=True, text=True)
        assert r.returncode == 0, (rel, r.stdout, r.stderr)


def test_i6t_07_readers_refuse_a_mixed_artifact_meta_pair(tmp_path):
    """[R6 내부 F07] `compare_states.py` 는 meta 를 `starts` 만 보려고 읽고 run_id·sha256 을 안 봤다 (ne_shape 도) —
    게시와 write_meta 사이에서 시도가 죽으면 남는 CSV=B · meta=A 묶음이 §1-10 표에 경고 없이 들어갔다. Codex R5-04
    최소 조건의 reader 절: 불일치를 성공으로 소비하지 않는다."""
    out = tmp_path / "out"; out.mkdir(); prov = _prov()
    j = json.loads((OUT / "degeneracy_100_Li.json").read_text(encoding="utf-8")); j["run_id"] = "bbbb"
    art = out / "degeneracy_100_Li.json"; art.write_text(json.dumps(j), encoding="utf-8")
    (out / "degeneracy_100_Li.json.meta.json").write_text(json.dumps({"artifact": art.name, "run_id": "aaaa", "sha256": prov.sha256_file(art), "starts": 24}), encoding="utf-8")
    assert prov.verify_unit(art)[0] is False
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "compare_states.py"), str(out)], capture_output=True, text=True, timeout=60)
    assert "묶음 불일치" in r.stderr and "degeneracy_100_Li.json" in r.stderr, (r.returncode, r.stdout[-300:], r.stderr[-300:])
    assert not re.search(r"^\s*100\s", r.stdout, re.M), r.stdout
    # ne_shape 의 소비 입력도 같은 검사: 섞인 matrix 묶음은 조용히 소비되지 않는다
    _r5_matrix(out / "matrix_100.csv", 0.16)
    mart = out / "matrix_100.csv"
    (out / "matrix_100.csv.meta.json").write_text(json.dumps({"artifact": mart.name, "run_id": "zzzz", "sha256": prov.sha256_file(mart)}), encoding="utf-8")
    with pytest.raises(RuntimeError, match="묶음 불일치"):
        _load_script("ne_shape").fitted_pair_info(out, "100", "GITT", "Li")


# ═══════════════════════════════════════════════════════════════════════════════════════════════════════
# P · sig-완전성 · archive-이식성 렌즈 (F1…F11; 검증 판정 `reviews/r6_repros/sig_port/VERDICT.md`)
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════
import urllib.parse                                                       # noqa: E402
from types import SimpleNamespace                                         # noqa: E402


def _synth_root(tmp_path):
    src = tmp_path / "src"
    subprocess.run([sys.executable, str(ROOT / "matlab/tests/gen_synth_xlsx.py"), str(src)], check=True, capture_output=True)
    return src


def test_i6p_01_scale_audit_line_root_label_survives_spaces_and_names_the_inputs(tmp_path):
    """[R6 내부 F1] `root=<basename>` 은 `degradation mode` 처럼 공백이 있으면 사본 파서(`\\S+`)가 `degradation` 만
    잡고, `cells/c168`·`cells_v2/c168` 은 같은 라벨이며 `--data-root .` 은 `.` 이었다 — 식별자가 아니었다. 라벨은
    URL 인코딩으로 공백을 살리고, 진짜 identity 는 소비한 입력의 digest(`inputs=`) 가 준다."""
    root = tmp_path / "degradation mode"; root.mkdir()
    audit = {"pocv": {"n": 50, "n_finite": 50, "n_inf": 0, "n_nan": 0, "n_exception": 0, "eps_rel": 1e-15,
                      "equivalent_within_rel": True}}
    a = SimpleNamespace(state="pristine", source="GITT", si_source="Li", seed=0)
    line = verify.scale_audit_line(root, a, audit, inputs_sha="abc123def456")
    m = re.search(r"root=(\S+) state=(\S+) source=(\S+) si=(\S+) seed=(\d+) n=(\d+)", line)
    assert m and urllib.parse.unquote(m.group(1)) == "degradation mode" and m.group(2) == "pristine", line
    assert re.search(r"\binputs=abc123def456\b", line), line
    assert line.startswith("# scale_audit,") and "pocv:n=50/finite=50/inf=0/nan=0/exc=0/eps_rel=1e-15/equiv=1" in line, line


def test_i6p_03_environment_signature_is_recorded_in_meta(tmp_path):
    """[R6 내부 F3] 라이브러리 버전이 어디에도 없었다 — scipy 1.11.4↔1.17.1 에서 savgol 13/500 ULP → L-BFGS-B 최적점이
    갈리는데(nit 25↔27, a_NE 1.5e-5) 다른 기계의 숫자가 왜 다른지 알 길이 없었다. `env_signature` 가 meta·JSON 에."""
    import numpy, scipy
    prov = _prov(); env = prov.env_signature()
    assert env["numpy"] == numpy.__version__ and env["scipy"] == scipy.__version__ and env["platform"], env
    assert env["python"].startswith(f"{sys.version_info[0]}.{sys.version_info[1]}."), env
    root = tmp_path / "repo"; _fixture_repo(root, outputs=())
    art = root / "out" / "matrix_100.csv"; art.write_text("a,run_id\n1,rid1\n", encoding="utf-8")
    r = subprocess.run(["bash", "-c", _shell_helpers() + '\nLAST_RUN_ID=rid1; write_meta "$1" 100 GITT\n', "t", str(art)],
                       cwd=root, env=dict(os.environ, STARTS="1", SI="Li", BMS_DATA_ROOT="synthetic", OUT=str(root / "out")),
                       capture_output=True, text=True, timeout=60)
    meta = json.loads((root / "out" / "matrix_100.csv.meta.json").read_text(encoding="utf-8"))
    assert meta.get("env", {}).get("numpy") == numpy.__version__ and meta["env"]["scipy"] == scipy.__version__, (meta.get("env"), r.stderr[-300:])


def test_i6p_04_build_records_the_inputs_it_consumed(tmp_path):
    """[R6 내부 F4] `build` 가 읽는 풀셀 워크북은 폴더의 이름순 첫 xlsx 이고 이름·sha256 이 JSON·행·meta 어디에도 없었다
    — `fullcell_states - 복사본.xlsx` 하나로 scale 이 바뀌어도 `data_root`·run_id·commit 은 그대로였다 (R5-05 는
    ne_shape 만 닫았다). 이제 `Objective.consumed_inputs` 에 반쪽전지·풀셀·문헌 입력의 경로와 sha256 이 남는다."""
    src = _synth_root(tmp_path); prov = _prov()
    wb = src / "data/full_cell/large_cell_033C/fullcell_states.xlsx"
    ci = verify.build(src, "GITT", "pristine", "Li").consumed_inputs
    assert ci["full_cell"]["path"].endswith("fullcell_states.xlsx") and ci["full_cell"]["sha256"] == prov.sha256_file(wb), ci
    assert ci["half_cell"]["sha256"] == prov.sha256_file(src / "data/half_cell/GITT/pristine.xlsx")
    assert ci["literature"]["si"]["sha256"] == prov.sha256_file(src / "data/literature/Si_OCP_sources/Li.csv")
    assert ci["literature"]["gr"]["sha256"] == prov.sha256_file(src / "data/literature/Si_Gr_literature_OCP.xlsx")
    d1 = verify.inputs_digest(ci)
    shutil.copy(wb, wb.with_name("fullcell_states - 복사본.xlsx"))          # 이름순 앞 (' ' < '.')
    ci2 = verify.build(src, "GITT", "pristine", "Li").consumed_inputs
    assert ci2["full_cell"]["path"].endswith("복사본.xlsx"), ci2["full_cell"]       # 무엇을 읽었는지 남는다
    assert len(d1) == 12 and d1 == verify.inputs_digest(ci2)                    # 같은 bytes 면 같은 digest


def test_i6p_05_profile_rows_and_degeneracy_json_carry_their_arguments(tmp_path):
    """[R6 내부 F5] `profile --profile-scale` 은 행 스키마·run_id·meta 가 같고 숫자만 달랐다(`profile_scale` 은 stdout
    SUMMARY 에만); `degeneracy --samples/--grid` 는 JSON 어디에도 없었다. 산출이 자기 인자를 말한다."""
    src = _synth_root(tmp_path); out = tmp_path / "out"; out.mkdir()
    base = ["--data-root", str(src), "--state", "100", "--si-source", "Li", "--source", "GITT", "--w-dqdv", "0",
            "--starts", "1", "--seed", "0"]
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        rc = verify.main(["profile", *base, "--grid", str(verify.S.CANONICAL_GAMMA_GRID_N),
                          "--profile-scale", "per-gamma", "--out", str(out / "p.csv")])
    assert rc in (0, None), rc     # 정본 격자라야 canonical — 좁힌 격자는 subset(rc 3, partial/) 이다 (R11 P1-3)
    rows = list(csv.DictReader((out / "p.csv").open(encoding="utf-8")))
    assert rows and all(r["profile_scale"] == "per-gamma" for r in rows), rows[0]
    assert all(len(r["inputs_sha"]) == 12 for r in rows), rows[0]
    with contextlib.redirect_stdout(io.StringIO()):
        rc = verify.main(["degeneracy", *base, "--tol", "0.01", "--grid", "3", "--samples", "5", "--out", str(out / "d.json")])
    j = json.loads((out / "d.json").read_text(encoding="utf-8"))
    assert j["n_grid"] == 3 and j["n_samples"] == 5, {k: j.get(k) for k in ("n_grid", "n_samples")}
    assert j["env"]["numpy"] and j["consumed_inputs"]["full_cell"]["sha256"] and len(j["inputs_sha"]) == 12, j.get("env")
    # eval 의 `--out` 헤더도 같은 서명을 싣고, 비교기는 그 줄들을 meta 로 넘긴다 (invalid 가 되지 않는다)
    with contextlib.redirect_stdout(io.StringIO()):
        rc = verify.main(["eval", *base, "--out", str(out / "e.csv")])
    head = (out / "e.csv").read_text(encoding="utf-8").splitlines()[:8]
    assert any(l.startswith("# env,") and "numpy=" in l for l in head) and any(l.startswith("# inputs,sha=") for l in head), head
    assert verify.dd_eval_csv_audit(out / "e.csv", spec=verify.parse_precision_spec("%.17g")) == []


def test_i6p_07_git_provenance_does_not_depend_on_the_callers_cwd(tmp_path):
    """[R6 내부 F7] `git_provenance` 가 cwd 기준이라 같은 수정 산출이 `bms-balancing/` 에서 False · 저장소 루트에서 True
    (코드로 분류) · `/tmp` 에서 None 이었다. 기본 base 는 이 스크립트가 속한 `bms-balancing/` 이다."""
    prov = _prov()
    here = prov.git_provenance(cwd=str(ROOT))
    old = os.getcwd(); os.chdir(tmp_path)
    try:
        elsewhere = prov.git_provenance()
    finally:
        os.chdir(old)
    assert here["git_commit"] and elsewhere["git_commit"] == here["git_commit"], (here["git_commit"], elsewhere)
    assert elsewhere["git_dirty"] == here["git_dirty"] and elsewhere["git_modified_code"] == here["git_modified_code"]


def test_i6p_09_provenance_cli_and_check_artifact_survive_a_non_utf8_default(tmp_path):
    """[R6 내부 F9] 비-UTF-8 기본 인코딩에서 `check_artifact` 의 `open()` 이 한글 JSON 을 못 읽고, `--check-run-id` 는
    `print("일치")` 에서 죽어 bound=0 이었다 (WSL 기본 UTF-8 에서는 안 남 — 사본이 다른 기계로 갈 때의 축)."""
    env = dict(os.environ, PYTHONUTF8="0", PYTHONCOERCECLOCALE="0", LC_ALL="C", LANG="C", PYTHONIOENCODING="ascii:strict")
    art = tmp_path / "x.csv"; art.write_text("a,run_id\n1,rid\n", encoding="utf-8")
    r = subprocess.run([sys.executable, str(ROOT / "scripts/provenance.py"), "--check-run-id", str(art), "rid"],
                       env=env, capture_output=True, text=True)
    assert r.returncode == 0, (r.returncode, r.stderr[-300:])
    j = tmp_path / "k.json"; j.write_text(json.dumps({"run_id": "rid", "note": "한글"}, ensure_ascii=False), encoding="utf-8")
    r2 = subprocess.run(["bash", "-c", _shell_helpers() + '\ncheck_artifact "$1"\n', "t", str(j)],
                        cwd=ROOT, env=dict(env, OUT=str(tmp_path)), capture_output=True, text=True)
    assert r2.returncode == 0, (r2.returncode, r2.stderr[-300:])


def test_i6p_10_atomic_writers_keep_the_computed_rows_when_the_lock_fails(tmp_path, monkeypatch):
    """[R6 내부 F10] ENOLCK(잠금을 못 거는 파일시스템) 면 `atomic_write_csv` 가 `.part` 를 지우고 예외 → 계산된 행 전부
    소실. 잠금 실패에는 `.part` 를 보존하고 그 경로를 예외에 적는다 (재계산 대신 손으로 게시할 수 있게)."""
    import errno, fcntl
    def boom(*a, **k): raise OSError(errno.ENOLCK, "No locks available")
    monkeypatch.setattr(fcntl, "flock", boom)
    with pytest.raises(OSError) as ei:
        verify.atomic_write_csv(tmp_path / "p.csv", [{"a": 1}], ["a"])
    parts = list(tmp_path.glob("p.csv.*.part"))
    assert parts and parts[0].read_text(encoding="utf-8").startswith("a\n1") and parts[0].name in str(ei.value), (parts, str(ei.value))
    with pytest.raises(OSError) as ej:
        verify.atomic_write_json(tmp_path / "d.json", {"x": 1})
    jparts = list(tmp_path.glob("d.json.*.part"))
    assert jparts and jparts[0].name in str(ej.value), (jparts, str(ej.value))


# ═══════════════════════════════════════════════════════════════════════════════════════════════════════
# U14 점검 스크립트 — 재실행이 새 스키마를 담았고 정본과 같은 숫자인가 (`scripts/check_u14.py`)
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════

def _u14_dirs(tmp_path, *, schema=True, bump=None):
    """정본(old)과 재실행(new) 한 쌍. `schema=False` 면 new 가 옛 스키마, `bump` 면 그만큼 숫자를 옮긴다.

    ⚠ R9-03 뒤: new 는 producer 스키마(`schema.DEGENERACY_KEYS`·`MATRIX_ROW`)를 **전부** 갖추고 receipt 는 진짜 모양이다 —
      열 이름만 맞는 부분집합 fixture 는 checker 가 내용을 안 본다는 사실을 가리고 있었다."""
    from bms_balancing import schema as S
    old, new = tmp_path / "out", tmp_path / "out_u14"   # new 만 새 스키마 (옛 정본은 meta 가 없다)
    old.mkdir(parents=True); new.mkdir(parents=True)
    ci = {"half_cell": {"path": "h.xlsx", "sha256": "1" * 64}, "full_cell": {"path": "f.xlsx", "sha256": "2" * 64},
          "literature": {"gr": {"path": "g.xlsx", "sha256": "3" * 64}, "si": {"path": "s.csv", "sha256": "4" * 64}}}
    rci = {"half_cell": {"path": "p.xlsx", "sha256": "5" * 64}, "full_cell": ci["full_cell"], "literature": ci["literature"]}
    for d, is_new in ((old, False), (new, True)):
        # ⚠ Codex R13 P2-1: `best_p` 는 5-파라미터 벡터다 (전 판 fixture 는 2 개였고, 모양 계약이
        #   없던 시절엔 통과했다 — 그래서 이 회귀가 모양 축을 한 번도 재지 않았다).
        j = {"state": "100", "n_accepted": 5, "best_obj": 1.5, "best_p": [1.0, 2.0, 3.0, 4.0, 5.0],
             "LLI_percent": {"min": 1.0, "max": 2.0 + (bump or 0.0) * is_new, "is_lower_bound": True}}
        if is_new and schema:
            j |= {"run_id": "rid", "si_source": "Li", "half_cell": "GITT", "w_dqdv": 0.0, "tol_percent_of_best": 1.0,
                  "n_starts": 24, "seed": 0, "n_grid": 21, "n_samples": 400, "env": _fixture_env(python="3.11.0", numpy="2.0", scipy="1.11.0", pandas="2.0.0", openpyxl="3.1.0", platform="linux-x"),
                  "consumed_inputs": ci, "ref_consumed_inputs": rci, "inputs_sha": S.inputs_digest(ci),
                  "ref_p": [1.0, 2.0, 3.0, 4.0, 5.0], "best_modes_percent": {"LLI": 1.5},
                  "LAM_PE_percent": {"min": 0.0, "max": 1.0}, "LAM_NE_percent": {"min": 0.0, "max": 1.0}}
        (d / "degeneracy_100_Li.json").write_text(json.dumps(j), encoding="utf-8")
        if is_new and schema:
            # R8-02: checker 가 요구하는 열 = producer 가 쓰는 열 — R9-03: 값까지 (진짜 receipt·숫자·nonempty)
            v = dict(half_cell="GITT", si="Li", w_dqdv="0", run_id="rid", inputs_sha=S.inputs_digest(ci),
                     ref_inputs_sha=S.inputs_digest(rci), consumed_inputs=json.dumps(ci), ref_consumed_inputs=json.dumps(rci),
                     scale_seed="0", n_scale_samples="50", scale_pocv_target="1.0", scale_dvdq_target="1.0",
                     scale_dqdv_target="1.0", scale_pocv_ref="1.0", scale_dvdq_ref="1.0", scale_dqdv_ref="1.0",
                     # 자체 리뷰 C33: `scale_audit_*` 는 빈 칸이 허용되지 않는다 (감사 없이 돌면 그것이 문제다)
                     scale_audit_target=audit_json(), scale_audit_ref=audit_json(), obj="1.5", rmse_pocv="0.002", a_PE="1.0", b_PE="0.0",
                     a_NE="1.1", b_NE="0.0", gamma_Si="0.3", c_cell="1.0", bounds="-", ref_a_PE="1.0", ref_b_PE="0.0",
                     ref_a_NE="1.0", ref_b_NE="0.0", ref_gamma_Si="0.2", ref_obj="1.0", ref_rmse_pocv="0.002",
                     ref_c_cell="1.0", ref_bounds="-", LAM_PE_pct="1.0", LAM_NE_pct="2.0",
                     LLI_pct=str(3.0 + (bump or 0.0) * is_new),
                     combo_roster="")
            # ⚠ Codex R13 P1-1: 전 판은 **한 행**에 `authority=1` 을 적어 canonical 을 주장했다 — 구성원 검사가
            #   없던 시절엔 통과했고, 그래서 U14 회귀가 정본 모집단을 한 번도 밟지 않았다. 정본 32 조합으로 만든다.
            keys = sorted(S.canonical_combo_keys("100"))
            roster = json.dumps({"authority": len(keys), "requested": len(keys), "succeeded": len(keys),
                                 "missing_input": [], "failed": [], "absent": []})
            mrows = [{k: v[k] for k in S.MATRIX_ROW} | {"half_cell": hc, "si": si, "w_dqdv": repr(w),
                                                        "combo_roster": roster} for hc, si, w in keys]
            verify.atomic_write_csv(d / "matrix_100.csv", mrows, list(S.MATRIX_ROW))
        else:
            # ⚠ Codex R13 P1-1: 옛 정본 쪽도 같은 정본 모집단을 담아야 "숫자는 같고 스키마만 다르다" 가 된다
            #   (전 판은 old 1 행 vs new 1 행이라 우연히 맞았다).
            cols = ["half_cell", "si", "w_dqdv", "obj", "LLI_pct"]
            body = [",".join([hc, si, repr(w), "1.5", str(3.0 + (bump or 0.0) * is_new)])
                    for hc, si, w in sorted(S.canonical_combo_keys("100"))]
            (d / "matrix_100.csv").write_text(",".join(cols) + "\n" + "\n".join(body) + "\n", encoding="utf-8")
        if is_new and schema:
            # ⚠ Codex R8-02 뒤: meta 는 **진짜** 묶음이어야 한다 (전 판 fixture 는 sha256="v" 인 가짜 meta 였고, 그것이
            #   "data 와 meta 를 따로 읽는" checker 를 가려 주고 있었다 — fixture 가 진실을 가린 통로)
            # ⚠ 자체 리뷰 C02 뒤: 정본과 재실행은 **독립 실행**이므로 run id 가 달라야 한다 (같으면 alias).
            for name in ("degeneracy_100_Li.json", "matrix_100.csv"):
                _u14_sign(d / name, "rid")
    return old, new


def _u14_sign(art, rid):
    """check_u14 의 META_KEYS 를 갖춘, 실제 bytes 에 결속된 meta."""
    (art.parent / (art.name + ".meta.json")).write_text(json.dumps(
        {"run_id": rid, "sha256": _prov().sha256_file(art), "artifact": art.name,
         # Codex R10 P1-7: 실제 `write_meta` 가 쓰는 실행 조건·환경을 그대로 — 없으면 승격 gate 가 **비교를 못 한다**
         "env": _fixture_env(),
         "state": "100", "half_cell_source": "GITT", "si_source": "Li", "starts": 24, "seed": 0,
         "started_utc": "2026-09-12T00:00:00Z", "git_commit_at_start": "0" * 40,
         "git_state_changed_during_run": False, "git_dirty": False, "git_modified_code": [],
         # Codex R11 P1-6: 승격 증명서는 실제 argv 와 본문에서 유도한 명부를 요구한다 (`write_meta` 가 쓰는 전부)
         "argv": ["python3", "-m", "bms_balancing.verify", "fixture"],
         "roster": __import__("bms_balancing.schema", fromlist=["body_roster"]).body_roster(
             art.name, art.read_bytes())}), encoding="utf-8")


def _u14_run(old, new, *extra):
    return subprocess.run([sys.executable, str(ROOT / "scripts/check_u14.py"), "--new", str(new), "--old", str(old), *extra],
                          capture_output=True, text=True, timeout=60)


def test_i6u_14_check_script_separates_schema_from_moved_numbers(tmp_path):
    """[R6 내부 후속] R6 는 게시·서명만 고치고 계산 경로는 안 건드렸다 — 그러니 U14 재실행의 숫자는 정본과 같아야
    하고, 다르면 그것이 발견이다 (먼저 볼 축은 F3 의 라이브러리 버전). 손으로 15 개 산출을 대는 것은 못 믿으므로
    `check_u14.py` 가 (a) 새 스키마 누락과 (b) 움직인 숫자를 **따로** 말하고 종료 코드로 가른다: 0 같음 · 1 숫자가
    다름 · 2 스키마 누락."""
    old, new = _u14_dirs(tmp_path)
    ok = _u14_run(old, new)
    # ⚠ 자체 리뷰 C11 뒤: 정본이 옛 스키마라 입력 identity 를 댈 수 없으면 **승격 자격이 없다** → rc 4.
    #   숫자·스키마 판정은 그대로 나온다 (그것이 이 시험의 주제다).
    assert ok.returncode == 4 and "전부 갖췄다" in ok.stdout and "전부 같다" in ok.stdout, (ok.returncode, ok.stdout)

    old2, new2 = _u14_dirs(tmp_path / "b", bump=1e-9)          # 스키마는 맞고 숫자만 1e-9 움직였다
    moved = _u14_run(old2, new2)
    assert moved.returncode == 1 and "다른 숫자" in moved.stdout, (moved.returncode, moved.stdout)
    assert "LLI_percent.max" in moved.stdout and "matrix_100.csv" in moved.stdout, moved.stdout
    assert "env" in moved.stdout and "scipy" in moved.stdout, "숫자가 움직였을 때 먼저 볼 축(F3)을 말해야 한다"

    old3, new3 = _u14_dirs(tmp_path / "c", schema=False)        # 옛 코드로 돈 재실행
    stale = _u14_run(old3, new3)
    assert stale.returncode == 2 and "새 스키마 누락" in stale.stdout, (stale.returncode, stale.stdout)
    for k in ("inputs_sha", "n_samples", "env", "meta.json 없음"):
        assert k in stale.stdout, (k, stale.stdout)
    assert _u14_run(old3, new3, "--schema-only").returncode == 2      # 숫자 대조 없이도 스키마는 본다
    assert _u14_run(old, tmp_path / "nope").returncode == 2           # 없는 디렉터리

    # 필드를 **하나씩** 빼서 그 축을 정말 보는지 (전부 빠진 fixture 는 다른 필드가 가려 준다 — 변이 시험에서 샜다)
    for i, (fname, drop) in enumerate([("degeneracy_100_Li.json", "inputs_sha"), ("degeneracy_100_Li.json", "n_samples"),
                                       ("degeneracy_100_Li.json", "env"), ("matrix_100.csv", "scale_seed"),
                                       ("degeneracy_100_Li.json.meta.json", "git_commit_at_start")]):
        o, n = _u14_dirs(tmp_path / f"d{i}")
        f = n / fname
        if fname.endswith(".csv"):
            rows_ = list(csv.DictReader(f.open(encoding="utf-8", newline="")))      # receipt 열은 JSON 이라 쉼표가 있다
            for r_ in rows_:
                r_.pop(drop)
            verify.atomic_write_csv(f, rows_, list(rows_[0]))
        else:
            j = json.loads(f.read_text(encoding="utf-8")); j.pop(drop)
            f.write_text(json.dumps(j), encoding="utf-8")
        if not fname.endswith(".meta.json"):
            _u14_sign(f, "rid")                       # R8-02: 산출을 고쳤으면 다시 서명 — 아니면 '묶음 불일치' 가 먼저 잡는다
        r = _u14_run(o, n)
        assert r.returncode == 2 and drop in r.stdout, (fname, drop, r.returncode, r.stdout)


# ═══════════════════════════════════════════════════════════════════════════════════════════════════════
# U15 · MATLAB `sprintf` 기준선 — R6 내부 원장이 "검증 못 한 전제" 로 남겼던 것 (2026-09-11 실측)
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════

#: 사용자 기계 MATLAB 이 찍은 것 그대로 (2026-09-11). R5-01 의 구간 규칙은 "Python 의 `format` 이 MATLAB 의
#: `sprintf` 와 같은 문자열을 낸다" 를 전제로 하는데, 이 저장소에 MATLAB 이 없어 못 재고 있던 두 축이다:
#: 반올림 타이(half-to-even 인가 half-away 인가)와 지수 자릿수(`e-05` 인가 Windows 식 `e-005` 인가).
MATLAB_SPRINTF = {(".2f", 0.125): "0.12", (".17g", 1e-5): "1.0000000000000001e-05"}


def test_i6u_15_matlab_sprintf_baseline_matches_our_formatter():
    """[R6 내부 원장 '검증 못 한 전제' → 닫힘] 갈렸다면 비교기가 **거짓 invalid** 를 냈을 자리다 (fail-closed 라
    조용한 통과는 아니지만 멀쩡한 산출을 malformed 로 거절했을 것이다).

    이 테스트는 발견 수정이 아니라 **외부 기준선 고정**이라 처음부터 통과하는 것이 정상이다 — 지키는 것은
    "우리 formatter 가 그 기준선에서 벗어나지 않는다" 이고, `token_format` 을 바꾸면 여기서 걸린다.
    """
    for (fmt, value), matlab in MATLAB_SPRINTF.items():
        assert format(value, fmt) == matlab, (fmt, value, format(value, fmt), matlab)

    # ① 반올림 타이 — 이 축은 비교기가 실제로 재출력하는 경로(`token_format`)에 걸려 있다.
    #    0.125 를 `%.2f` 로 찍을 때 MATLAB 이 '0.13'(half-away) 이었다면, '0.12' 를 쓴 멀쩡한 산출을
    #    audit 이 "선언 형식으로 찍은 것과 다르다" 며 invalid 로 거절했을 것이다.
    f2 = verify.parse_precision_spec("%.2f")
    assert format(0.125, verify.token_format(f2)) == MATLAB_SPRINTF[(".2f", 0.125)]
    assert verify.dd_eval_csv_audit  # (audit 이 그 형식으로 토큰을 다시 찍는다 — `test_i6v_*` 가 경로를 덮는다)

    # ② 지수 자릿수 — `%.17g` 는 `exact` 라 재출력하지 않는다(`token_format` → None). 대신 전제는
    #    "MATLAB 이 찍은 17 자리 토큰이 원래 double 로 되돌아온다" 이고, Windows 식 3 자리 지수였다면
    #    파싱은 됐겠지만 우리가 같은 토큰을 쓸 때 문자열이 갈렸을 것이다.
    g17 = verify.parse_precision_spec("%.17g")
    assert verify.token_format(g17) is None, g17
    assert float(MATLAB_SPRINTF[(".17g", 1e-5)]) == 1e-5

    # 그 기준선 위에서 R5-01 의 구간 판정: 같은 칸이면 차이 0, 칸 밖이면 초과분이 잡힌다
    assert verify.token_excess(f2, 0.125, 0.1249) == 0.0
    assert verify.token_excess(f2, 0.125, 0.13) > 0.0
    assert verify.token_excess(g17, 1e-5, 1e-5) == 0.0


# ═══════════════════════════════════════════════════════════════════════════════════════════════════════
# U14 실행이 드러낸 것 (2026-09-12, 사용자 기계 네 상태 재실행) — `reviews/R6_LEDGER.md` U14 절
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════

def test_i6w_01_published_csv_survives_a_git_round_trip(tmp_path):
    """[U14-01] `atomic_write_csv` 는 `csv` 기본 lineterminator 라 **CRLF** 를 쓰는데 git 은 `.gitattributes` 가
    csv 를 안 덮어 LF 로 정규화해 저장한다 (`git add` 가 "CRLF will be replaced by LF" 경고). 그러면 meta 의
    sha256 은 CRLF bytes 의 것이라 **fresh clone 에서 `verify_unit` 이 False** 가 되고, F07 수정 때문에
    `compare_states` 가 그 상태를 표에서 조용히 뺀다 — 저장소를 새로 받은 리뷰어에게는 상태가 사라진 표가 간다.

    2026-09-12 사용자 기계 U14 커밋에서 실제로 경고가 났다 (matrix_100·200·300_0147, profile 셋).
    산출은 LF 로 쓰고 `.gitattributes` 로 고정한다 — 디스크 bytes 와 커밋 bytes 가 같아야 서명이 산다.
    """
    p = tmp_path / "m.csv"
    verify.atomic_write_csv(p, [{"a": 1, "run_id": "rid"}], ["a", "run_id"])
    raw = p.read_bytes()
    assert b"\r\n" not in raw, raw[:40]
    # ne_shape 도 같은 규약 (이미 lineterminator="\n" — 두 writer 가 갈리지 않는지 고정한다)
    assert b"\r\n" not in (ROOT / "out" / "ne_shape_GITT_Li.csv").read_bytes()[:400]
    # `.gitattributes` 가 서명 대상 확장자를 덮는가 (작업사본이 CRLF 로 체크아웃되면 같은 일이 난다)
    attrs = (ROOT / ".gitattributes").read_text(encoding="utf-8")
    for ext in ("*.csv", "*.json"):
        assert re.search(rf"^{re.escape(ext)}\s+text\s+eol=lf", attrs, re.M), (ext, attrs)


def test_i6w_02_verify_unit_says_line_endings_when_only_they_changed(tmp_path):
    """[U14-01 후속] sha256 만 다르다고 말하면 리뷰어가 "다른 시도가 게시했다" 로 읽는다 — 줄끝만 바뀐 경우는
    원인을 짚어 줘야 한다 (git 정규화·Windows 체크아웃). 내용이 같다는 것은 bytes 정규화로 확인한다."""
    prov = _prov()
    p = tmp_path / "m.csv"
    verify.atomic_write_csv(p, [{"a": 1, "run_id": "rid"}], ["a", "run_id"])
    (tmp_path / "m.csv.meta.json").write_text(json.dumps(
        {"artifact": "m.csv", "run_id": "rid", "sha256": prov.sha256_file(p)}), encoding="utf-8")
    assert prov.verify_unit(p) == (True, "일치")
    p.write_bytes(p.read_bytes().replace(b"\n", b"\r\n"))          # Windows 체크아웃이 하는 것
    ok, why = prov.verify_unit(p)
    assert ok is False and "줄끝" in why, (ok, why)
    p.write_bytes(p.read_bytes().replace(b"rid", b"xxx"))          # 대조군: 내용이 바뀌면 줄끝 얘기 안 한다
    ok2, why2 = prov.verify_unit(p)
    assert ok2 is False and "줄끝" not in why2, (ok2, why2)


def test_i6w_03_check_u14_uses_the_versioned_baseline_and_separates_new_fields(tmp_path):
    """[U14-02] `check_u14.py` 가 파일 **이름**으로만 정본을 골라 `degeneracy_300_0009_Li.json`(v1, 힌트 격자
    이전)과 댔다 — 그 리비전의 정본은 `_v2` 였다 (옛 out/ 규칙; 현행 out/ 은 Codex R6-04 로 unversioned 하나).
    그래서 재실행이 v2 를 그대로
    재현했는데도 span 0.0908 → 2.5826 이 "숫자가 움직였다" 로 나왔다.

    또 정본에 **없던 필드**(`grid_pct` 등 스키마 추가분)가 `None → [값]` 으로 전부 diff 에 섞여 618 건을 만들었다 —
    새 필드는 스키마 얘기지 숫자가 움직인 것이 아니다. 둘을 갈라 보고한다.
    """
    old, new = tmp_path / "out", tmp_path / "out_u14"
    old.mkdir(); new.mkdir()
    base = {"state": "300_0009", "n_accepted": 5, "best_obj": 1.5,
            "LLI_percent": {"min": 1.0, "max": 2.0, "is_lower_bound": True}}
    (old / "degeneracy_300_0009_Li.json").write_text(json.dumps(      # v1 — 정본이 아니다
        base | {"LLI_percent": {"min": 9.0, "max": 9.5, "is_lower_bound": True}}), encoding="utf-8")
    (old / "degeneracy_300_0009_Li_v2.json").write_text(json.dumps(base), encoding="utf-8")
    # R9-03: receipt 는 진짜 모양이어야 하고, R10 P1-6 뒤로는 **역할 전부**가 있어야 한다 (producer 가 그렇게 쓴다)
    ci = {"half_cell": {"path": "h.xlsx", "sha256": "1" * 64}, "full_cell": {"path": "f.xlsx", "sha256": "2" * 64},
          "literature": {"gr": {"path": "g.xlsx", "sha256": "3" * 64}, "si": {"path": "s.csv", "sha256": "4" * 64}}}
    (new / "degeneracy_300_0009_Li.json").write_text(json.dumps(      # 재실행 = v2 재현 + 새 필드 (producer 스키마 전부)
        base | {"run_id": "r", "si_source": "Li", "half_cell": "GITT", "w_dqdv": 0.0, "tol_percent_of_best": 1.0,
                "n_starts": 24, "seed": 0, "n_grid": 21, "n_samples": 400, "env": _fixture_env(python="3.11.0", numpy="2.0", scipy="1.11.0", pandas="2.0.0", openpyxl="3.1.0", platform="linux-x"),
                "consumed_inputs": ci, "ref_consumed_inputs": ci,
                "inputs_sha": __import__("bms_balancing.schema", fromlist=["x"]).inputs_digest(ci),
                "best_p": [1.0] * 5, "ref_p": [1.0] * 5, "best_modes_percent": {"LLI": 1.5},
                "LAM_PE_percent": {"min": 0.0, "max": 1.0}, "LAM_NE_percent": {"min": 0.0, "max": 1.0},
                "LLI_percent": {"min": 1.0, "max": 2.0, "is_lower_bound": True, "grid_pct": [1.0, 2.0]}}),
        encoding="utf-8")
    _u14_sign(new / "degeneracy_300_0009_Li.json", "r")                 # R8-02: 진짜 묶음 (가짜 meta 는 이제 미완이다)
    r = _u14_run(old, new, "--baseline-policy", "historical")        # 옛 커밋의 out/ 을 손으로 푼 경우 (Codex R7-04)
    # ⚠ 자체 리뷰 C11 뒤: 숫자는 안 움직였지만(그것이 이 시험의 주제다) 정본이 옛 스키마라 입력 identity 를
    #   댈 수 없다 → 승격 자격 없음(rc 4). 계약 위반(2)도 숫자 차이(1)도 아니다.
    assert r.returncode == 4, (r.returncode, r.stdout)
    assert "_v2" in r.stdout and "정본에 없던 필드" in r.stdout, r.stdout
    # 같은 디렉터리라도 **현행 정책**(기본)에서는 `_v2` 를 쓰지 않는다 — 그래서 v1 과 대조해 숫자가 움직인다
    cur = _u14_run(old, new)
    assert "current" in cur.stdout and "쓰지 않았다" in cur.stdout and cur.returncode == 1, (cur.returncode, cur.stdout)


def test_i6w_04_renormalize_resigns_only_when_the_cells_are_identical(tmp_path):
    """[U14-01 뒷수습] 이미 CRLF 로 게시·커밋된 산출을 재실행(수 시간) 없이 살리려면 LF 로 고치고 meta 를 다시
    서명해야 한다. 재실행 없이 bytes 를 바꾸는 것이므로 **줄끝만 다르다는 증명**(파싱한 셀이 완전히 같다)이
    조건이고, 무엇을 했는지 meta 에 남긴다. 다른 것이 다르면 손대지 않는다 — 그때는 재실행이 답이다."""
    prov = _prov(); out = tmp_path / "out"; out.mkdir()
    def publish(name, body_lf, sign=None):
        f = out / name; f.write_bytes(body_lf.replace(b"\n", b"\r\n"))
        (out / (name + ".meta.json")).write_text(json.dumps(
            {"artifact": name, "run_id": "rid", "sha256": sign or prov.sha256_file(f)}), encoding="utf-8")
        return f
    good = publish("matrix_100.csv", b"a,run_id\n1,rid\n")
    stale = publish("matrix_200.csv", b"a,run_id\n2,rid\n", sign="0" * 64)   # meta 가 지금 bytes 의 것이 아니다
    r = subprocess.run([sys.executable, str(ROOT / "scripts/check_u14.py"), "--new", str(out), "--renormalize"],
                       capture_output=True, text=True, timeout=60)
    assert r.returncode == 1, (r.returncode, r.stdout)           # 하나를 거절했으니 0 이 아니다
    assert b"\r\n" not in good.read_bytes() and prov.verify_unit(good) == (True, "일치"), r.stdout
    meta = json.loads((out / "matrix_100.csv.meta.json").read_text(encoding="utf-8"))
    assert meta["bytes_renormalized"]["what"] == "CRLF→LF" and meta["bytes_renormalized"]["utc"], meta
    assert b"\r\n" in stale.read_bytes() and "matrix_200.csv" in r.stdout, r.stdout   # 거절된 쪽은 그대로


def test_i6w_05_renormalize_resigns_when_git_already_normalized_the_file(tmp_path):
    """[U14-01 뒷수습 ②] 실제로 난 순서는 반대였다 — git 이 **이미** LF 로 정규화해 체크아웃했고 meta 에는 CRLF
    시절의 sha256 이 남았다. 그때 디스크에는 CRLF 가 없으니 "고칠 것 없음" 으로 지나가면 서명이 영영 안 맞는다.
    기록된 해시가 지금 bytes 의 줄끝 변형 중 하나와 맞으면 그것이 "내용은 같다" 의 증명이다."""
    prov = _prov(); out = tmp_path / "out"; out.mkdir()
    f = out / "matrix_100.csv"
    lf = b"a,run_id\n1,rid\n"
    f.write_bytes(lf)                                            # 디스크는 LF (git 이 정규화함)
    crlf_hash = hashlib.sha256(lf.replace(b"\n", b"\r\n")).hexdigest()
    (out / "matrix_100.csv.meta.json").write_text(json.dumps(
        {"artifact": "matrix_100.csv", "run_id": "rid", "sha256": crlf_hash}), encoding="utf-8")
    assert prov.verify_unit(f)[0] is False
    r = subprocess.run([sys.executable, str(ROOT / "scripts/check_u14.py"), "--new", str(out), "--renormalize"],
                       capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, (r.returncode, r.stdout)
    assert prov.verify_unit(f) == (True, "일치"), (prov.verify_unit(f), r.stdout)
    assert f.read_bytes() == lf                                  # 내용은 손대지 않는다
    # 내용이 진짜 다르면 거절한다 (줄끝 변형 어느 것과도 안 맞는다)
    f.write_bytes(b"a,run_id\n9,rid\n")
    bad = subprocess.run([sys.executable, str(ROOT / "scripts/check_u14.py"), "--new", str(out), "--renormalize"],
                         capture_output=True, text=True, timeout=60)
    assert bad.returncode == 1 and "내용이 다르다" in bad.stdout, bad.stdout


def test_i6w_06_baseline_can_be_read_from_a_git_revision(tmp_path):
    """[2026-09-12] 재실행이 `out/` 을 이미 덮었으면 정본은 git 에만 있다. 손으로 `git show` 를 엮다가
    `git show <rev> --name-only`(그 커밋이 **바꾼** 파일)를 트리로 착각해 빈 디렉터리와 대조했다 — 14 건이 전부
    "정본에 없음" 으로 나왔다. 트리는 `git ls-tree -r` 고, 그 엮음을 도구가 한다."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("cu14", ROOT / "scripts" / "check_u14.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    dest = tmp_path / "base"
    n = m.extract_rev("HEAD", dest, ROOT)
    assert n >= 10, n
    for name in ("degeneracy_300_0147_Li.json", "matrix_300_0009.csv"):
        assert (dest / name).is_file(), sorted(p.name for p in dest.iterdir())[:5]
    assert json.loads((dest / "degeneracy_300_0147_Li.json").read_text(encoding="utf-8"))["state"] == "300_0147"
    assert m.extract_rev("nonexistent-rev-xyz", tmp_path / "b2", ROOT) == 0     # 없는 리비전은 0


def test_i6w_07_ne_shape_reader_survives_the_provenance_columns(tmp_path):
    """[2026-09-12] R6 내부 F02 가 `ne_shape` 행에 `run_id` 를 붙였는데 소비 helper 는 모든 열을 `float()` 로 읽어
    사용자 기계에서 세 테스트가 `ValueError: could not convert string to float: '17749f76…'` 로 깨졌다.

    이 트리에서 안 깨진 이유가 중요하다 — 커밋된 `out/ne_shape_GITT_Li.csv` 가 **아직 옛 스키마**라 fixture 가
    진실을 가리고 있었다 (이 저장소에서 다섯 번째로 실측된 패턴). 그래서 helper 를 경로 인자로 열어 **새 스키마
    파일**로 직접 건다 — 커밋된 산출이 재생성되기 전에도 회귀가 잡히도록.
    """
    from test_review_findings import _ne_shape_csv, NE_SHAPE_TEXT_COLS
    src = (ROOT / "out" / "ne_shape_GITT_Li.csv").read_text(encoding="utf-8").splitlines()
    hdr, rows = src[0], src[1:]
    new = tmp_path / "ne_shape_GITT_Li.csv"
    new.write_text("\n".join([hdr + ",run_id"] + [r + ",17749f76588f4138a0e846318a1bdc39" for r in rows]) + "\n",
                   encoding="utf-8")
    R = _ne_shape_csv(new)
    assert R and all(v["run_id"] == "17749f76588f4138a0e846318a1bdc39" for v in R.values()), R
    assert isinstance(next(iter(R.values()))["measured_shape_mV"], float)      # 숫자 열은 그대로 숫자
    assert "run_id" in NE_SHAPE_TEXT_COLS


def test_i6w_08_committed_artifacts_carry_no_merge_conflict_markers():
    """[2026-09-12] rebase 충돌이 해결되지 않은 채 `out/matrix_300_0009.csv` 에 `<<<<<<< HEAD` 가 박혔고, 그 결과가
    여덟 개의 `KeyError: 'half_cell'` 로 나왔다 — 원인에서 먼 오류다. 산출은 기계가 읽는 정본이므로 표식 하나로
    바로 말한다."""
    marks = ("<<<<<<<", "=======", ">>>>>>>")
    def scan(text):
        return [m for m in marks if any(l.startswith(m) for l in text.splitlines())]
    bad = {}
    for f in sorted(list((ROOT / "out").glob("*.csv")) + list((ROOT / "out").glob("*.json"))):
        hits = scan(f.read_text(encoding="utf-8", errors="replace"))
        if hits:
            bad[f.name] = hits
    assert not bad, f"산출에 충돌 표식이 남았다 — 해결하고 다시 커밋할 것: {bad}"
    assert scan("a,b\n<<<<<<< HEAD\n1,2\n") == ["<<<<<<<"]      # 탐지기가 실제로 잡는다 (변이 대신 자체 증명)


# ═══════════════════════════════════════════════════════════════════════════════════════════════════════
# C · Codex R6 (2026-09-12, 대상 d431404, NO-GO: P1 3 · P2 3) — `reviews/R6_CODEX.md`
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════
import builtins, io as _io                                                # noqa: E402


def _cs():
    import importlib.util
    spec = importlib.util.spec_from_file_location("compare_states", ROOT / "scripts" / "compare_states.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def _c6_meta(art, rid, starts=24):
    prov = _prov()
    (art.parent / (art.name + ".meta.json")).write_text(json.dumps(
        {"artifact": art.name, "state": "100", "run_id": rid, "sha256": prov.sha256_file(art), "starts": starts}),
        encoding="utf-8")


def _c6_deg(out, rid, span, meta=True):
    obj = {"run_id": rid, "state": "100", "si_source": "Li", "half_cell": "GITT", "n_starts": 24,
           "best_modes_percent": {"LAM_PE": 1.0, "LAM_NE": 1.0, "LLI": 1.0},
           **{f"{k}_percent": {"min": 0.0, "max": span, "span": span, "is_lower_bound": True} for k in ("LAM_PE", "LAM_NE", "LLI")}}
    f = out / "degeneracy_100_Li.json"; verify.atomic_write_json(f, obj)
    if meta: _c6_meta(f, rid)
    return f


def _c6_matrix(out, rid, width, meta=True, name="matrix_100.csv"):
    rows = [dict(half_cell="GITT", si=s, w_dqdv="0", LAM_PE_pct=str(i * width), LAM_NE_pct=str(i * width),
                 LLI_pct=str(i * width), bounds="-", ref_bounds="-", gamma_Si="0.3", ref_gamma_Si="0.2", run_id=rid)
            for i, s in enumerate(("Li", "Kunz"))]
    f = out / name; verify.atomic_write_csv(f, rows, list(rows[0]))
    if meta: _c6_meta(f, rid)
    return f


def _hook_open(monkeypatch, target_name, k, on_k):
    """`target_name` 파일의 k 번째 **읽기** open 직전에 `on_k()` — 파일 읽기 경계에 다른 정상 게시가 끼는 순서.
    pandas·zipfile·pathlib 이 각각 `builtins.open`/`io.open` 을 쓰므로 둘 다 건다."""
    real = _io.open; n = {"v": 0, "published": 0}
    def fake(file, mode="r", *a, **kw):
        if pathlib.Path(str(file)).name == target_name and "r" in str(mode) and "+" not in str(mode):
            n["v"] += 1
            if n["v"] == k:
                n["published"] += 1                                       # ⚠ Codex R8-08: 읽기 수와 **게시(callback) 수**는 다르다
                on_k()
        return real(file, mode, *a, **kw)
    monkeypatch.setattr(_io, "open", fake); monkeypatch.setattr(builtins, "open", fake)
    return n                                                              # v = 읽기 횟수 · published = callback 실행 횟수


def test_c6_01_readers_consume_only_the_snapshot_they_verified(tmp_path, monkeypatch):
    """[Codex R6-01 · P1] `load_degeneracy` 가 A 의 JSON bytes 를 읽은 뒤 다른 정상 시도 B 가 B/B 를 게시하면, 독자는
    pathname 의 B/B 를 검증하고 **A 데이터에 B meta** 를 붙였다. matrix 는 반대 순서 — A/A 를 검증한 직후 B 의 CSV 만
    게시되면 B 의 폭 79 를 읽어 표에 넣었다 (그 순간 디스크 묶음은 B/A 라 false). 검사는 "이 경로가 검사할 때
    맞았는가" 만 말하고 따로 읽은 bytes 를 보증하지 않는다.

    독자는 data bytes 와 meta 를 **한 번씩** 읽어 그 둘을 서로 대조하고 그것만 소비한다 — 게시가 어느 읽기 경계에
    끼든 결과는 A/A · B/B · 명시적 미완 뿐이어야 한다 (A/B 나 검증 안 한 B 의 성공 소비 금지).
    """
    W_DEG = {"attempt-A": 1.0, "attempt-B": 20.0}; W_MAT = {"attempt-A": 3.0, "attempt-B": 79.0}

    def setup(out, kind, how):
        if kind == "deg":
            _c6_deg(out, "attempt-A", W_DEG["attempt-A"])
            return lambda: _c6_deg(out, "attempt-B", W_DEG["attempt-B"], meta=True)
        _c6_matrix(out, "attempt-A", W_MAT["attempt-A"])
        return lambda: _c6_matrix(out, "attempt-B", W_MAT["attempt-B"], meta=(how == "full"))

    def read(out, kind):
        m = _cs()
        return m.load_degeneracy(out) if kind == "deg" else m.load_matrix_axis(out)

    # ⚠ Codex R7 §4: 전 판은 k 를 1~4 로 **가정**했는데 degeneracy 데이터는 한 번만 열린다 — k≥2 인 건들은 훅이
    #   아예 안 걸린 채 통과했다. 경계 수를 먼저 **세고** 그 수만큼만 돈다 (그리고 매 건 주입을 확인한다).
    cases = []
    for kind, target, how in (("deg", "degeneracy_100_Li.json", "full"),
                              ("mat", "matrix_100.csv", "csv-only"), ("mat", "matrix_100.csv", "full"),
                              ("deg", "degeneracy_100_Li.json.meta.json", "full"),
                              ("mat", "matrix_100.csv.meta.json", "full")):
        probe = tmp_path / f"probe-{len(cases)}"; probe.mkdir()
        setup(probe, kind, how)
        with monkeypatch.context() as mp:
            counter = _hook_open(mp, target, 10 ** 6, lambda: None)
            read(probe, kind)
        n_reads = counter["v"]
        assert n_reads >= 1 and counter["published"] == 0, (kind, target, how, counter)
        cases += [(kind, target, k, how) for k in range(1, n_reads + 1)]
    seen = set(); schedules = {}                                          # schedule 별 (기대 게시 id, 관측) 을 따로 적는다
    for i, (kind, target, k, how) in enumerate(cases):
        out = tmp_path / f"c{i}"; out.mkdir()
        pub_b = setup(out, kind, how)
        with monkeypatch.context() as mp:
            fired = _hook_open(mp, target, k, pub_b)
            got = read(out, kind)
        # ⚠ Codex R7 §4 · R8-08: 읽기 수(`v`)가 아니라 **게시 callback 수**로 주입을 건별 확인한다 — metadata 경계의
        #   callback 만 꺼도 다른 schedule 의 B/B·미완이 합집합을 채워 통과했다.
        assert fired["v"] >= k, (kind, target, k, how, fired["v"])
        assert fired["published"] == 1, (kind, target, k, how, fired)
        if "100" not in got:
            seen.add("미완"); schedules[(kind, target, k, how)] = ("attempt-B", "미완"); continue   # 명시적 미완 — 허용
        e = got["100"]
        rid = e["j"]["run_id"] if kind == "deg" else e["run_id"]
        width = e["j"]["LLI_percent"]["span"] if kind == "deg" else e["per"]["GITT"]["LLI"]
        assert e.get("meta") and e["meta"]["run_id"] == rid, (kind, target, k, how, rid, e.get("meta"))
        assert width == (W_DEG if kind == "deg" else W_MAT)[rid], (kind, target, k, how, rid, width)
        seen.add(rid); schedules[(kind, target, k, how)] = ("attempt-B", rid)
    # schedule 마다: 게시된 것은 B 이고, 관측은 B/B 아니면 명시적 미완이어야 한다 (A 를 그대로 소비하면 그 schedule 이
    # 게시를 못 본 것 — 다른 schedule 의 관측이 대신 채우지 못하게 **건별로** 건다)
    for sched, (expected, observed) in schedules.items():
        assert observed in (expected, "미완"), (sched, expected, observed)
    # 주입 지점은 전부 **읽기 직전**이라 이 묶음에서 살아남는 것은 B/B 아니면 명시적 미완이다. A/A 는 (a) 아무도
    # 안 끼어든 대조군과 (b) 검증이 **끝난 뒤** 게시하는 순서에서 나온다 — 후자는 적응판 replay 의 `검증_후_게시`.
    assert {"attempt-B", "미완"} <= seen, seen
    for kind, how in (("deg", "full"), ("mat", "full")):
        out = tmp_path / f"ctl-{kind}"; out.mkdir()
        setup(out, kind, how)
        got = read(out, kind)                                             # 대조군: 아무도 안 끼어들면 A/A
        e = got["100"]
        rid = e["j"]["run_id"] if kind == "deg" else e["run_id"]
        assert rid == "attempt-A" and e["meta"]["run_id"] == "attempt-A", (kind, rid, e.get("meta"))
        seen.add(rid)
    assert {"attempt-A", "attempt-B", "미완"} <= seen, seen                # 세 결과가 다 관측됐다


def test_c6_02_modern_artifact_without_meta_is_incomplete_not_legacy(tmp_path):
    """[Codex R6-02 · P1] 빈 out/ 에 `run_id` 가 있는 **현행** 산출을 게시하고 첫 write_meta 전에 중단하면 `verify_unit`
    이 `(None, "meta 없음")` 을 주고 세 독자가 전부 소비에 성공했다 — "옛 파일 허용" 예외가 현행 생산자의 미완을
    못 가렸다. 현행 schema(run_id 있음)에는 현행 meta 가 필수고, legacy 호환은 진짜 legacy(run_id 없음)에만."""
    prov = _prov(); m = _cs(); ne = _load_script("ne_shape")
    out = tmp_path / "out"; out.mkdir()
    fj = _c6_deg(out, "rid-x", 5.0, meta=False); fm = _c6_matrix(out, "rid-x", 4.0, meta=False)
    for f in (fj, fm):
        ok, why = prov.verify_unit(f)
        assert ok is False and ("미완" in why or "현행" in why), (f.name, ok, why)
    assert m.load_degeneracy(out) == {} and m.load_matrix_axis(out) == {}
    with pytest.raises(RuntimeError):
        ne.fitted_pair_info(out, "100", "GITT", "Li")
    # 대조군 ① 진짜 legacy (run_id 없음) 는 호환 경로로 읽힌다
    leg = tmp_path / "leg"; leg.mkdir()
    (leg / "degeneracy_100_Li.json").write_text(json.dumps({"state": "100", "best_modes_percent": {},
        **{f"{k}_percent": {"span": 1.0} for k in ("LAM_PE", "LAM_NE", "LLI")}}), encoding="utf-8")
    _r5_matrix(leg / "matrix_100.csv", 0.16)                               # run_id 열 없는 옛 모양
    assert prov.verify_unit(leg / "degeneracy_100_Li.json")[0] is None
    assert "100" in m.load_degeneracy(leg) and ne.fitted_pair_info(leg, "100", "GITT", "Li") is not None
    # 대조군 ② 현행 + 제대로 된 meta → 일치
    _c6_meta(fj, "rid-x"); _c6_meta(fm, "rid-x")
    assert prov.verify_unit(fj) == (True, "일치") and prov.verify_unit(fm) == (True, "일치")
    assert "100" in m.load_degeneracy(out) and "100" in m.load_matrix_axis(out)


def _bump_xlsx(path, delta=0.02, header=None):
    """같은 경로에 전압을 +delta 한 유효한 xlsx 를 다시 내보낸다 (Codex R6-03 의 재-export)."""
    import pandas as pd
    if header is None:
        df = pd.read_excel(path, header=None)
        for c in range(1, df.shape[1], 2):
            df.iloc[2:, c] = pd.to_numeric(df.iloc[2:, c], errors="coerce") + delta
        df.to_excel(path, header=False, index=False)
    else:
        df = pd.read_excel(path)
        for c in df.columns:
            if "volt" in str(c).lower():
                df[c] = df[c] + delta
        df.to_excel(path, index=False)


def test_c6_03_build_and_ne_shape_hash_the_bytes_they_computed_with(tmp_path, monkeypatch):
    """[Codex R6-03 · P1] `build` 는 풀셀 워크북 A 를 읽고 **나중에** 경로를 다시 열어 해시했다 — 그 사이 같은 이름으로
    +20 mV 인 B 가 재-export 되면 Objective 는 A 로 만들고 `consumed_inputs`·`inputs_sha` 는 B 를 적는다.
    `ne_shape.main` 도 반쪽전지를 HalfCell·raw_ne_capacity·identity 로 세 번 열어 같은 자리가 있다. 입력마다 bytes
    snapshot 을 한 번 잡고 그 bytes 로 파싱과 해시를 함께 한다 — A값/A서명 · B값/B서명 · 중단만 허용."""
    import hashlib
    src = _synth_root(tmp_path)
    wb = src / "data/full_cell/large_cell_033C/fullcell_states.xlsx"
    a_bytes = wb.read_bytes(); sha_a = hashlib.sha256(a_bytes).hexdigest()   # A 의 bytes 를 한 번 잡아 둔다 (합성 재생성은 byte-결정적이지 않다)
    ref = verify.build(src, "GITT", "100", "Li")                          # 깨끗한 A 로 만든 기준
    for k in (1, 2, 3):
        # 훅이 실제로 B 를 쓰면 이후 반복은 B 를 읽으므로 매번 A 로 되돌린다
        wb.write_bytes(a_bytes)
        assert hashlib.sha256(wb.read_bytes()).hexdigest() == sha_a
        with monkeypatch.context() as mp:
            _hook_open(mp, wb.name, k, lambda: _bump_xlsx(wb))
            obj = verify.build(src, "GITT", "100", "Li")
        got = obj.consumed_inputs["full_cell"]["sha256"]; v_same = bool((obj.voltage == ref.voltage).all()) if obj.voltage.shape == ref.voltage.shape else False
        sha_now = hashlib.sha256(wb.read_bytes()).hexdigest()
        # 허용: (A값, A서명) 또는 (B값, B서명). 금지: A값에 B서명
        assert (v_same and got == sha_a) or (not v_same and got == sha_now and got != sha_a), (k, v_same, got[:12], sha_a[:12], sha_now[:12])
    # ne_shape: 반쪽전지 100.xlsx 의 세 번째 열기(옛 코드의 identity 읽기) 직전에 PE +20 mV 재-export
    wb.write_bytes(a_bytes)
    hc = src / "data/half_cell/GITT/100.xlsx"; hc_a = hashlib.sha256(hc.read_bytes()).hexdigest()
    ne = _load_script("ne_shape")
    import contextlib
    def run_ne(outd, hook):
        outd.mkdir()
        with monkeypatch.context() as mp:
            if hook:
                _hook_open(mp, hc.name, hook, lambda: _bump_xlsx(hc, header=0))
            mp.setattr(sys, "argv", ["ne_shape", "--data-root", str(src), "--out-dir", str(outd), "--write", str(outd)])
            with contextlib.redirect_stdout(_io.StringIO()):
                ne.main()
        sub = outd / "partial"                                            # γ 짝이 없는 실행(status none)은 canonical 에 안 쓴다 (Codex R9-06)
        meta = json.loads((sub / "ne_shape_GITT_Li.csv.meta.json").read_text(encoding="utf-8"))
        rows = {r["state"]: r for r in csv.DictReader((sub / "ne_shape_GITT_Li.csv").open(encoding="utf-8"))}
        assert meta["status"] == "none" and not (outd / "ne_shape_GITT_Li.csv").exists()
        return meta["consumed_inputs"]["100"]["half_cell"]["sha256"], float(rows["100"]["pe_shape_max_mV"])
    hc_a_bytes = hc.read_bytes()
    rec_a, pe_a = run_ne(tmp_path / "ne_out_a", hook=False)              # 깨끗한 A 의 기준 (합성 100 은 자체 PE 편차가 있다)
    assert rec_a == hc_a
    # 두 번째·세 번째 open 직전에 재-export: 옛 코드는 세 번(HalfCell·raw_ne_capacity·identity), "파싱 뒤 다시 열어
    # 해시" 류의 변이는 두 번 연다. 올바른 코드는 한 번만 열어 어느 훅도 안 맞는다.
    for k in (2, 3):
        hc.write_bytes(hc_a_bytes)
        rec, pe = run_ne(tmp_path / f"ne_out_{k}", hook=k)
        hc_now = hashlib.sha256(hc.read_bytes()).hexdigest()
        # 허용: (A값, A서명) 또는 (B값 = +20 mV, B서명). 금지: A값에 B서명
        assert (rec == hc_a and abs(pe - pe_a) < 1e-9) or (rec == hc_now and rec != hc_a and pe > pe_a + 15.0), \
            (k, rec[:12], hc_a[:12], hc_now[:12], pe, pe_a)


def test_c6_04_reader_uses_the_unversioned_canon_and_flags_versioned_siblings(tmp_path, capsys):
    """[Codex R6-04 · P2] "가장 높은 `_vN`" 규칙 때문에 U14 가 정본을 다시 만든 뒤에도 독자는 옛 `_v2`(meta 없음)를
    골랐다 — 새 서명·환경 필드가 소비 경로에 안 실린다. 정본은 **unversioned 이름 하나**이고 `_vN` 은 역사 자료라
    `out/archive/` 에 있어야 한다; out/ 에 남은 `_vN` 은 시끄럽게 건너뛴다."""
    m = _cs(); d = tmp_path / "out"; d.mkdir()
    _c6_deg(d, "rid-new", 111.0)
    (d / "degeneracy_100_Li_v2.json").write_text(json.dumps({"state": "100", "best_modes_percent": {},
        **{f"{k}_percent": {"span": 222.0} for k in ("LAM_PE", "LAM_NE", "LLI")}}), encoding="utf-8")
    _c6_matrix(d, "rid-new", 3.0)
    _c6_matrix(d, "rid-old", 50.0, meta=False, name="matrix_100_v2.csv")
    got = m.load_degeneracy(d); mx = m.load_matrix_axis(d); err = capsys.readouterr().err
    assert got["100"]["file"] == "degeneracy_100_Li.json" and got["100"]["j"]["LLI_percent"]["span"] == 111.0, got["100"]["file"]
    assert mx["100"]["file"] == "matrix_100.csv" and mx["100"]["per"]["GITT"]["LLI"] == 3.0, mx["100"]["file"]
    assert "_v2" in err and "archive" in err, err
    # 실제 out/ 에는 `_vN` **산출**이 없어야 한다 (U14 가 v2 를 비트 단위로 재현했으므로 옛 판은 archive 로).
    # ⚠ 산출은 .csv/.json 뿐이다 (`check_u14.ARTIFACT_SUFFIXES`) — 사용자 기계의 gitignored `out/matrix_v2.log` 가 이 glob 에
    #   잡혀 이 테스트가 깨졌고, 변이 감사가 이 테스트를 case 로 쓰므로 R7-06(no-op 변이 → MISSED 기대)까지 연쇄로 깨졌다.
    stale = [p.name for p in (ROOT / "out").glob("*_v[0-9]*") if p.suffix.lower() in (".csv", ".json")]
    assert not stale, stale
    assert (ROOT / "out" / "archive" / "degeneracy_300_0009_Li_v2.json").is_file()


def test_c6_05_git_provenance_keeps_a_path_containing_the_arrow_notation(tmp_path):
    """[Codex R6-05 · P2] `-z` 레코드로 정확히 읽은 경로를 후단의 `.split(" -> ")[-1].strip()` 이 다시 훼손했다 —
    rename 이 아닌 정상 파일명 `out/a -> b.csv` 의 수치 하나를 고치면 `git_modified_code=["b.csv"]`, dirty=True.
    NUL 레코드의 path 필드를 그대로 쓴다 (사람용 rename 표기로 분해하거나 공백을 깎지 않는다)."""
    root = tmp_path / "repo"; git = _fixture_repo(root, outputs=("out/a -> b.csv",))
    (root / "out" / "a -> b.csv").write_text("a,b\n1,3\n", encoding="utf-8")
    pv = _prov().git_provenance(cwd=str(root), output_roots=("out",))
    assert pv["git_modified_outputs"] == ["out/a -> b.csv"], pv
    assert pv["git_modified_code"] == [] and pv["git_dirty"] is False, pv


def test_c6_06_profile_budget_is_stated_as_it_is_run():
    """[Codex R6-06 · P2] U14 판정문이 "γ profile 은 적은 시작으로 풀어서" 움직였다고 설명했는데 실제 경로는
    `best[:4] + 무작위 24` = **γ당 25 회** 4변수 L-BFGS-B 다 (SLSQP 등식 프로파일의 3 시작과 섞었다). 산출의
    `n_tried` 와 코드가 그렇게 말하고, 문서는 그 예산을 적되 "적은 시작 때문" 을 말하지 않는다."""
    import inspect
    src = inspect.getsource(verify.cmd_profile)
    assert "rng.random((args.starts, 4))" in src and "[best[:4]]" in src
    n = 0
    for f in (ROOT / "out").glob("profile_gamma_*.csv"):
        for r in csv.DictReader(f.open(encoding="utf-8")):
            if r.get("n_tried"):
                assert int(r["n_tried"]) == 25 and int(r["n_ok"]) <= 25, (f.name, r["gamma_Si"], r["n_tried"]); n += 1
    assert n >= 80, n                                                    # U14 네 상태 84 행
    for name in ("reviews/R6_LEDGER.md", "reviews/R6_REQUEST.md", "WORKING_STATE.md", "FINDINGS.md"):
        live = _live(_doc(name))
        assert "적은 시작" not in live, name
    assert "γ당 25" in _live(_doc("reviews/R6_LEDGER.md"))


def test_c6_q3_precision_conflict_is_partial_only_when_the_option_absorbed_a_difference(tmp_path):
    """[Codex R6 Q3] "충돌이면 항상 partial" 은 코드와 다르다. `%.17g` 선언 + `--precision fixed:1` 에서 `.125` 와 `.125`
    는 conflict=true 지만 complete/0 이고, `.125` 와 `.126` 은 partial/3 이다 — partial 은 **옵션이 선언은 못 흡수하는
    차이를 흡수한 셀이 있을 때만** 이다 (`precision_override_looser`). 문서(§1-8)는 그 실제 의미를 적는다."""
    anchors, cols, P, py, rows = _r2_base()
    for r in rows:
        r[5] = 0.125
    loose = _r2_csv(tmp_path, anchors, cols, rows, name="loose.csv")            # 기본 head = %.17g 선언
    same = {c: list(v) for c, v in py.items()}; same["rmse_pocv"] = [0.125] * len(P)
    res, txt = _r2_run(anchors, P, same, loose, precision="fixed:1")
    assert res["precision_conflict"] and not res["precision_override_looser"], (res, txt)
    assert res["status"] == "complete", (res["status"], txt)                   # 같은 값: 충돌은 기록되고 complete
    diff = {c: list(v) for c, v in py.items()}; diff["rmse_pocv"] = [0.125] * len(P); diff["rmse_pocv"][3] = 0.126
    res, txt = _r2_run(anchors, P, diff, loose, precision="fixed:1")
    assert res["precision_conflict"] and res["precision_override_looser"], (res, txt)
    assert res["status"] == "partial", (res["status"], txt)                    # 옵션이 흡수한 차이: partial
    sec = _live(_section(_doc("FINDINGS.md"), "### 1-8"))
    assert "못 흡수하는 차이를 흡수한 셀이 있을 때만" in sec and "충돌은 R4-02 Q3 대로 partial" not in sec
