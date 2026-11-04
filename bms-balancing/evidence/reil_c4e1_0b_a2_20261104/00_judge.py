"""REIL C4-E · E1-0b 판정기 (승인 요청 `docs/REIL_C4E_E1_0B_APPROVAL_REQUEST_20261030.md` §4-3 · 정정 범위안 `docs/REIL_C4E_E1_0B_RESULT_N1_SCOPE_20261103.md`
§4 A · 사용자 채택 §94) — stdlib · 읽기 전용 · 실행 전에 고정한 바이트.

    /usr/bin/python3.11 -I <E>/00_judge.py <E> <단계>     (<E> = 이 파일이 있는 증거 폴더 reil_c4e1_0b_a2_YYYYMMDD · 단계 = 01_red_e1_0b | 02_green_e1_0b)

읽기 = `<E>/<단계>.stdout.log` · `<단계>.meta.json` · `<단계>.outer_rc.txt` · `<단계>.stderr.log` (크기만) · 봉인된 시험 파일 (RED: launcher 대조 하나 ·
GREEN: 넷 — `bms-balancing/tests/`). 쓰기 = `<E>/<단계>.judge.json` 배타 생성 하나. 시험 · git · 네트워크 · 하위 프로세스 0. 판정의 정본은 요청서 §4-3
이고 이 출력은 그 기계 기록이다 — 실행자의 수동 대조와 다르면 멈춘다. 항목마다 ok · 관측값을 남기고, 하나라도 거짓이면 verdict STOP (반환 1) · 모두
참이면 MATCH (반환 0). 증거 폴더 이름 규칙 밖 · 이 파일이 그 폴더 밖 · 단계 이름 밖 · 출력 파일이 이미 있음 → 아무것도 쓰지 않고 멈춘다 (SystemExit ·
반환 2). 판정 중 예외는 `judge.exception` 항목 (거짓) 으로 남기고 기록은 쓴다.

stdout 읽기 규칙 (요청서 §4-3 의 "판정기의 읽기 규칙"):
- 줄 = stdout 을 UTF-8 로 읽어 "\\n" 으로 나눈 것 (끝의 빈 조각 하나는 버린다). 마지막 줄 = 그 마지막 줄 하나 (pytest 의 최종 요약 — `-q` 에서는 `=` 장식이
  없다). 마지막 줄은 수 (RED 3 · GREEN) 의 대상이고 절 머리줄 · 짧은 요약 절에 넣지 않는다 — 지난 시도의 작성자 스크립트가 이 줄을 짧은 요약의 "그 밖 줄"
  로 셌다 (상태 문서 §92 · §93).
- 절 머리줄 = 마지막 줄 앞의 `=+ <이름> =+` 꼴의 줄. 짧은 요약 절 · FAILURES 절 = 그 머리줄 다음 줄부터 다음 절 머리줄 (없으면 마지막 줄) 앞까지.
- 짧은 요약 줄 = 짧은 요약 절에서 `PASSED <nodeid>` · `FAILED <nodeid>` (뒤에 ` - <메시지>` 가 붙을 수 있다) 꼴의 줄. 그 밖 줄은 판정 조건이 아니고 수만
  남긴다 (요청서: 메시지의 유무 · 생략 · 줄바꿈 · 순서 · 폭은 판정 조건이 아니다).
- 실패 절 = FAILURES 절 안의 `_+ <시험명> _+` 머리줄 다음 줄부터 다음 실패 절 머리줄 앞까지. 첫 traceback 항목 = 실패 절에서 `<경로>:<줄>: in <이름>`
  꼴의 첫 줄. 예외 블록 = 실패 절에서 `E   ` 로 시작하는 줄들 (이어진 한 덩어리여야 한다) · 머리 = 그 첫 줄의 `E   ` 뒤를 `<예외 종류>: <메시지>` 로 읽은 것.
- `ERROR` 줄 = stdout 에서 낱말 `ERROR` 로 시작하는 줄 · `ERRORS` 절 머리줄. 중단 = `Interrupted` 또는 `!!!!` 가 든 줄. `INTERNALERROR` 가 든 줄.
- 판정기 자기 확인: 읽은 시험 파일의 sha256 · bytes = 실행기 meta 의 `source_end` 행 (실행기가 끝에 봉인 표와 대조한 바이트) 이고, RED 표 (9 + 24) =
  봉인된 launcher 대조의 최상위 `test_*` 함수 33, GREEN 의 기대 집합 = 봉인된 네 파일의 최상위 `test_*` 함수 (파일별 21 · 6 · 33 · 11).
"""
import ast
import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

LAUNCH_TESTS = "tests/test_reil_c4e1_launch.py"
#: 단계 → 외곽 반환 파일 · pytest rc 의 기대값
STEPS = {"01_red_e1_0b": 1, "02_green_e1_0b": 0}
#: RED 표 (요청서 §4-3) — 시험명 · 최종 예외 · exact | prefix · 메시지 첫 줄 · 예측 줄 (참고 · 판정 아님 — 대조 v8 바이트로 다시 적은 것)
RED_TABLE = (
    ("test_l14_independence_fixed_commands_constants_and_main_rules", "AssertionError", "exact",
     "('E1-0b: 승인 문구의 요청서 경로', 'docs/REIL_C4E_E1_APPROVAL_REQUEST_v5_20261027.md')", 465),
    ("test_l23_user_level_rewrite_proxy_and_tls_off_settings_reach_neither_the_fetch_checks_nor_the_child", "AssertionError", "prefix",
     "('rewrite', 'FUTURE-01: 사용자 설정이 fetch 사전 대조에 보였다', ", 712),
    ("test_l25_inherited_git_location_and_trace_variables_reach_neither_fixture_nor_launcher_git", "AssertionError", "exact",
     "('FUTURE-01: fetch 자식에 고정 설정 원천이 없다', [])", 754),
    ("test_l28_fetch_env_drops_every_inherited_config_source_and_adds_only_the_fixed_list", "AttributeError", "exact",
     "module 'scripts.reil_c4e1_launch' has no attribute 'fetch_env'", 902),
    ("test_l29_a_conditional_config_matching_only_the_fetch_folder_reaches_neither_the_checks_nor_the_child", "AssertionError", "prefix",
     "('FUTURE-01: 받은 저장소 폴더에만 걸린 조건부 설정이 fetch 에 닿았다', ", 951),
    ("test_l30_the_received_repository_may_hold_only_the_local_keys_that_init_remote_and_partial_fetch_write", "AssertionError", "exact",
     "('FUTURE-01: 받은 저장소의 local 설정 밖 키가 통과했다', 'localtls')", 993),
    ("test_l31_cleanup_starts_observations_only_before_one_common_deadline_and_reports_unverified_when_it_cannot_look", "AttributeError", "exact",
     "module 'scripts.reil_c4e1_launch' has no attribute 'cleanup_group'", 1004),
    ("test_l32_an_exception_inside_cleanup_is_caught_and_only_an_emergency_kill_and_observation_follow_under_the_same_deadline", "AttributeError", "exact",
     "module 'scripts.reil_c4e1_launch' has no attribute 'cleanup_group'", 1035),
    ("test_l33_postcheck_fails_the_stage_for_a_cleanup_that_reached_its_deadline_or_did_not_end_empty", "AssertionError", "exact",
     "('정리 기한에 닿은 기록을 사후 대조가 통과시켰다', [])", 1072),
)
#: RED 에서 통과할 24 (요청서 §4-3 의 목록)
PASS24 = (
    "test_l1_precheck_passes_only_with_fixed_list_exact_bytes_seal_binding_clean_interpreter_and_approved_specs",
    "test_l2_list_sha_schema_path_set_entry_format_and_non_json_each_block",
    "test_l3_changed_same_size_missing_symlinked_module_or_linked_parent_each_block",
    "test_l4_a_shadowing_scripts_package_module_zip_entry_or_our_init_blocks",
    "test_l5_interpreter_flags_fixed_argv_head_and_run_script_path_are_checked",
    "test_l6_stage_verdict_is_the_and_of_precheck_child_rc_timeout_and_postcheck",
    "test_l7_child_result_reads_the_last_stdout_line_and_needs_final_complete_for_run",
    "test_l8_identity_link_binds_the_run_import_paths_to_the_checked_paths",
    "test_l9_a_failed_precheck_never_starts_the_child_and_records_launched_false",
    "test_l10_a_passing_precheck_runs_the_fixed_child_and_completes_only_when_every_term_holds",
    "test_l11_timeout_kills_the_whole_process_group_including_grandchildren",
    "test_l12_refuses_to_overwrite_records_or_reuse_a_pycache_folder",
    "test_l13_postcheck_catches_a_module_changed_during_the_child_wrong_fetched_bytes_and_a_reused_data_folder",
    "test_l15_a_leaf_package_beside_an_approved_module_blocks_without_executing_it",
    "test_l16_a_leaf_extension_module_beside_an_approved_module_blocks",
    "test_l17_extra_executed_files_and_the_seal_lock_binding_each_block",
    "test_l18_process_observation_errors_stay_unknown_and_only_vanished_pids_are_gone",
    "test_l19_a_failed_kill_with_a_running_child_ends_within_bounded_waits_and_records_unexited",
    "test_l20_exceptions_in_precheck_start_and_postcheck_are_recorded_with_phase_and_launched_state",
    "test_l21_a_failed_start_record_never_starts_the_child_and_is_not_treated_as_empty_normal_output",
    "test_l22_child_env_keeps_only_the_ca_among_git_variables_and_removes_secrets",
    "test_l24_fetch_postcheck_binds_the_received_repository_to_the_fixed_source",
    "test_l26_preparation_failures_are_recorded_as_phase_prepare_and_never_start_the_child",
    "test_l27_decode_failures_in_proc_reads_and_git_output_are_recorded_not_escaped",
)
#: GREEN 의 네 파일 · 파일별 최상위 test_* 함수 수 (요청서 §4-3)
GREEN_FILES = (("tests/test_reil_c4e.py", 21), ("tests/test_reil_c4e_fix.py", 6), (LAUNCH_TESTS, 33), ("tests/test_reil_c4e1_runner.py", 11))
CHAIN = ("The above exception was the direct cause of the following exception", "During handling of the above exception, another exception occurred")
HEADER = re.compile(r"=+ (.+?) =+")
SUB = re.compile(r"_+ (\S+) _+")
ENTRY = re.compile(r"(\S+):([0-9]+): in (\S+)")
SUMMARY = re.compile(r"(PASSED|FAILED) (\S+)(?: - .*)?")
LAST = re.compile(r"(?:=+ )?(.+?) in [0-9]+(?:\.[0-9]+)?s(?: \([0-9:.]+\))?(?: =+)?")
ITEM = re.compile(r"([0-9]+) ([a-z]+)")
HEAD = re.compile(r"([A-Za-z_][A-Za-z0-9_.]*): (.*)")
ERROR_WORD = re.compile(r"ERROR\b")
WARNINGS = ("warning", "warnings")
CHECKS: list = []
INFO: dict = {}


def check(cid: str, ok, observed=None) -> None:
    CHECKS.append({"id": cid, "ok": bool(ok), "observed": observed})


def refuse(msg: str):
    """의도된 거부 — 아무것도 쓰지 않고 반환 2 (STOP 의 1 과 구분)."""
    sys.stderr.write(msg + "\n")
    raise SystemExit(2)


def read(path: Path):
    """(바이트, None) 또는 (None, 사유)."""
    try:
        return path.read_bytes(), None
    except OSError as ex:
        return None, f"{ex.__class__.__name__}: {ex}"


def digest(b) -> dict:
    return {"sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}


def is_int(x, want: int) -> bool:
    return isinstance(x, int) and not isinstance(x, bool) and x == want


def test_names(src: bytes) -> list:
    """최상위 `test_*` 함수 이름 (정의 순서)."""
    return [n.name for n in ast.parse(src).body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name.startswith("test_")]


def sealed(bms: Path, rel: str, meta: dict):
    """봉인된 시험 파일 하나 → (바이트 또는 None, 관측). 실행기 meta 의 `source_end` 행과 sha256 · bytes 가 같아야 쓴다."""
    b, why = read(bms / rel)
    row = ((meta.get("source_end") or {}) if isinstance(meta, dict) else {}).get(f"{bms.name}/{rel}")
    if b is None:
        return None, {"why": why, "source_end": row}
    got = digest(b)
    same = isinstance(row, dict) and row.get("sha256") == got["sha256"] and row.get("bytes") == got["bytes"]
    return (b if same else None), {**got, "source_end": row, "same": same}


def split_lines(text: str) -> list:
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    return lines


def section(lines: list, heads: list, name: str):
    """이름이 같은 절 머리줄이 정확히 하나면 (본문 줄, 1) · 아니면 (None, 개수)."""
    idx = [k for k, (_, t) in enumerate(heads) if t == name]
    if len(idx) != 1:
        return None, len(idx)
    k = idx[0]
    end = heads[k + 1][0] if k + 1 < len(heads) else len(lines) - 1
    return lines[heads[k][0] + 1:end], 1


def summary_ids(body: list):
    ids, other = {"PASSED": [], "FAILED": []}, []
    for line in body:
        m = SUMMARY.fullmatch(line)
        if m:
            ids[m.group(1)].append(m.group(2))
        else:
            other.append(line)
    return ids, other


def same_set(got: list, want: list) -> dict:
    return {"ok": sorted(got) == sorted(want) and len(set(got)) == len(got), "count": len(got),
            "missing": sorted(set(want) - set(got)), "extra": sorted(set(got) - set(want)),
            "duplicates": sorted({x for x in got if got.count(x) > 1})}


def last_items(line: str):
    m = LAST.fullmatch(line)
    if not m:
        return None
    items = {}
    for part in m.group(1).split(", "):
        im = ITEM.fullmatch(part)
        if not im or im.group(2) in items:
            return None
        items[im.group(2)] = int(im.group(1))
    return items


def failure_parts(body: list) -> dict:
    """FAILURES 절 → {시험명: [실패 절 본문, …]} (같은 이름이 둘이면 둘)."""
    heads = [(i, m.group(1)) for i, line in enumerate(body) if (m := SUB.fullmatch(line))]
    parts: dict = {}
    for k, (i, name) in enumerate(heads):
        end = heads[k + 1][0] if k + 1 < len(heads) else len(body)
        parts.setdefault(name, []).append(body[i + 1:end])
    return parts


def common(meta: dict, outer, want: int) -> None:
    """요청서 §4-3 공통 — 외곽 실행기 meta · 외곽 반환 파일."""
    cl = meta.get("cleanup") if isinstance(meta.get("cleanup"), dict) else {}
    check("common.started", meta.get("started") is True, meta.get("started"))
    check("common.timed_out", meta.get("timed_out") is False, meta.get("timed_out"))
    check("common.cleanup_status", cl.get("status") == "empty", cl.get("status"))
    check("common.cleanup_deadline_hit", cl.get("deadline_hit") is False, cl.get("deadline_hit"))
    check("common.cleanup_errors", cl.get("errors") == [], cl.get("errors"))
    check("common.end_problems", meta.get("end_problems") == [], meta.get("end_problems"))
    check("common.errors", meta.get("errors") == [], meta.get("errors"))
    check("common.runner_ok", meta.get("runner_ok") is True, meta.get("runner_ok"))
    check("common.outer_rc", outer == f"{want}\n".encode(), None if outer is None else outer.decode("utf-8", "replace"))


def stdout_markers(lines: list, heads: list, kind: str) -> None:
    """수집 오류 (`ERROR` 줄) · INTERNALERROR · 중단."""
    err = [line for line in lines if ERROR_WORD.match(line)]
    err_heads = [t for _, t in heads if t == "ERRORS"]
    check(f"{kind}.error_lines", not err and not err_heads, {"lines": err[:3], "errors_headers": len(err_heads)})
    check(f"{kind}.internalerror", not any("INTERNALERROR" in line for line in lines), None)
    stops = [line for line in lines if "Interrupted" in line or "!!!!" in line]
    check(f"{kind}.interrupted", not stops, stops[:3])


def judge_red(lines: list, heads: list, meta: dict, bms: Path) -> None:
    names = [r[0] for r in RED_TABLE]
    src, obs = sealed(bms, LAUNCH_TESTS, meta)
    defined = test_names(src) if src is not None else None
    check("red.table_bound", defined is not None and sorted(defined) == sorted(names + list(PASS24)) and len(defined) == 33,
          {"file": obs, "defined": None if defined is None else len(defined)})
    summ, n_summ = section(lines, heads, "short test summary info")
    fails, n_fail = section(lines, heads, "FAILURES")
    check("red.sections", n_summ == 1 and n_fail == 1, {"short test summary info": n_summ, "FAILURES": n_fail})
    ids, other = summary_ids(summ or [])
    INFO["summary_other_lines"] = {"count": len(other), "first": other[:3]}
    fs = same_set(ids["FAILED"], [f"{LAUNCH_TESTS}::{n}" for n in names])
    check("red.failed_set", fs["ok"], fs)
    ps = same_set(ids["PASSED"], [f"{LAUNCH_TESTS}::{n}" for n in PASS24])
    check("red.passed_set", ps["ok"], ps)
    parts = failure_parts(fails or [])
    check("red.failure_sections", sorted(parts) == sorted(names) and all(len(v) == 1 for v in parts.values()),
          {"extra": sorted(set(parts) - set(names)), "missing": sorted(set(names) - set(parts)),
           "repeated": sorted(k for k, v in parts.items() if len(v) > 1)})
    INFO["red_lines"] = {}
    for name, etype, mode, msg, pred in RED_TABLE:
        tag = name.split("_")[1]
        got = parts.get(name, [])
        check(f"red.{tag}.one_section", len(got) == 1, len(got))
        if len(got) != 1:
            continue
        part = got[0]
        entry = next((line for line in part if ENTRY.fullmatch(line)), None)
        em = ENTRY.fullmatch(entry) if entry is not None else None
        check(f"red.{tag}.first_entry", em is not None and em.group(1) == LAUNCH_TESTS and em.group(3) == name, entry)
        seen = int(em.group(2)) if em is not None else None
        INFO["red_lines"][tag] = {"observed": seen, "predicted": pred, "same": seen == pred}
        chained = [line for line in part if any(c in line for c in CHAIN)]
        check(f"red.{tag}.no_chain", not chained, chained[:2])
        eidx = [j for j, line in enumerate(part) if line.startswith("E   ")]
        check(f"red.{tag}.one_block", bool(eidx) and eidx == list(range(eidx[0], eidx[-1] + 1)), {"e_lines": len(eidx)})
        head = part[eidx[0]][4:] if eidx else None
        hm = HEAD.fullmatch(head) if head is not None else None
        gtype, gmsg = (hm.group(1), hm.group(2)) if hm else (None, None)
        ok_msg = gmsg is not None and (gmsg == msg if mode == "exact" else gmsg.startswith(msg))
        check(f"red.{tag}.exception", gtype == etype and ok_msg, {"head": None if head is None else head[:300], "want": [etype, mode, msg]})
        check(f"red.{tag}.not_unexpected", gmsg is None or not gmsg.startswith("('UNEXPECTED_RED_CAUSE'"), None)
    unexpected = [line[:200] for line in lines if "UNEXPECTED_RED_CAUSE" in line]
    check("red.unexpected_anywhere", not unexpected, unexpected[:2])
    check("red.pytest_rc", is_int(meta.get("rc"), 1), meta.get("rc"))
    items = last_items(lines[-1]) if lines else None
    core = None if items is None else {k: v for k, v in items.items() if k not in WARNINGS}
    INFO["warnings"] = None if items is None else sum(v for k, v in items.items() if k in WARNINGS)
    check("red.last_line", core == {"failed": 9, "passed": 24}, lines[-1] if lines else None)
    stdout_markers(lines, heads, "red")


def judge_green(lines: list, heads: list, meta: dict, bms: Path) -> None:
    want, per_file = [], {}
    for rel, n in GREEN_FILES:
        src, obs = sealed(bms, rel, meta)
        defined = test_names(src) if src is not None else None
        per_file[rel] = {"file": obs, "defined": None if defined is None else len(defined), "want": n}
        want += [f"{rel}::{x}" for x in (defined or [])]
    check("green.files_bound", all(v["defined"] == v["want"] for v in per_file.values()) and len(want) == 71, per_file)
    summ, n_summ = section(lines, heads, "short test summary info")
    _, n_fail = section(lines, heads, "FAILURES")
    check("green.sections", n_summ == 1 and n_fail == 0, {"short test summary info": n_summ, "FAILURES": n_fail})
    ids, other = summary_ids(summ or [])
    INFO["summary_other_lines"] = {"count": len(other), "first": other[:3]}
    ps = same_set(ids["PASSED"], want)
    check("green.passed_set", ps["ok"] and len(want) == 71, ps)
    check("green.failed_lines", ids["FAILED"] == [], ids["FAILED"][:3])
    check("green.pytest_rc", is_int(meta.get("rc"), 0), meta.get("rc"))
    items = last_items(lines[-1]) if lines else None
    core = None if items is None else {k: v for k, v in items.items() if k not in WARNINGS}
    INFO["warnings"] = None if items is None else sum(v for k, v in items.items() if k in WARNINGS)
    check("green.last_line", core == {"passed": 71}, lines[-1] if lines else None)
    stdout_markers(lines, heads, "green")


def main(argv: list) -> int:
    if len(argv) != 2 or argv[1] not in STEPS:
        refuse(f"사용: 00_judge.py <E> <{' | '.join(STEPS)}>")
    e, step = Path(argv[0]).resolve(), argv[1]
    here = Path(__file__).resolve()
    if not re.fullmatch(r"reil_c4e1_0b_a2_20[0-9]{6}", e.name) or e.parent.name != "evidence" or here.parent != e:
        refuse(f"증거 폴더 이름 규칙 밖이거나 판정기가 그 폴더 밖이다 — 쓰지 않는다: {e} · {here}")
    out_path = e / f"{step}.judge.json"
    if out_path.exists() or out_path.is_symlink():
        refuse(f"이미 있다 — 덮어쓰지 않는다: {out_path}")
    bms, want = e.parent.parent, STEPS[step]
    inputs = {}
    try:
        raw = {}
        for k in ("stdout.log", "meta.json", "outer_rc.txt", "stderr.log"):
            b, why = read(e / f"{step}.{k}")
            raw[k] = b
            inputs[k] = digest(b) if b is not None else {"why": why}
        try:
            text = raw["stdout.log"].decode("utf-8") if raw["stdout.log"] is not None else None
        except UnicodeDecodeError as ex:
            text = None
            inputs["stdout.log"]["why"] = f"UnicodeDecodeError: {ex}"
        check("input.stdout", text is not None, inputs["stdout.log"])
        try:
            meta = json.loads(raw["meta.json"].decode("utf-8")) if raw["meta.json"] is not None else None
        except ValueError as ex:
            meta = None
            inputs["meta.json"]["why"] = f"{ex.__class__.__name__}: {ex}"
        check("input.meta", isinstance(meta, dict), inputs["meta.json"])
        meta = meta if isinstance(meta, dict) else {}
        lines = split_lines(text) if text is not None else []
        heads = [(i, m.group(1)) for i, line in enumerate(lines[:-1]) if (m := HEADER.fullmatch(line))]
        INFO["stdout_lines"] = len(lines)
        INFO["stderr_bytes"] = None if raw["stderr.log"] is None else len(raw["stderr.log"])
        common(meta, raw["outer_rc.txt"], want)
        (judge_red if want == 1 else judge_green)(lines, heads, meta, bms)
    except Exception as ex:  # noqa: BLE001 — 판정기 자신의 예외도 거짓 항목으로 남기고 기록은 쓴다
        check("judge.exception", False, f"{ex.__class__.__name__}: {ex}"[:500])
    failed = [c["id"] for c in CHECKS if not c["ok"]]
    doc = {"kind": "REIL_C4E1_0B_JUDGE", "step": step, "utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "judge": {"path": str(here), **digest(here.read_bytes())}, "evidence": str(e), "inputs": inputs, "checks": CHECKS, "info": INFO,
           "failed": failed, "verdict": "STOP" if failed else "MATCH",
           "note": "판정의 정본은 요청서 §4-3 · 이 기록은 그 기계 기록 · 실행자의 수동 대조와 다르면 멈춘다"}
    with open(out_path, "x", encoding="utf-8") as f:
        f.write(json.dumps(doc, ensure_ascii=False, indent=1) + "\n")
    print(json.dumps({"written": str(out_path), "verdict": doc["verdict"], "checks": len(CHECKS), "failed": failed}, ensure_ascii=False))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
