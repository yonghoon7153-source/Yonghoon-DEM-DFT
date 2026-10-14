"""REIL C4-E — E3a 66 호출 실행 진입점 (`fetch` · `plan-e` · `run`) · 호출당 상한 · 비용 투영 규칙 (v3 · 상태 문서 §66).

**골격 (E0 RED 용 · v3 §6-1 3)** — 이름 · 상수만 있고 함수 · 클래스 본문은 NotImplementedError 다. 구현은 RED 1 회 뒤에 넣는다.
승인 · 범위: `docs/REIL_C4E_APPROVAL_REQUEST_v3_20261014.md` (§3 · §4 · §5 · §6 · 수용 §65) · 상태 문서 §66.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve()
BMS = HERE.parents[1]
REPO = HERE.parents[2]
if str(BMS) not in sys.path:      # `-I` 실행은 스크립트 폴더를 sys.path 에 넣지 않는다 — 시험과 같은 `scripts.` 모듈 객체를 쓴다
    sys.path.insert(0, str(BMS))
from scripts import reil_c4_e3a as e3a  # noqa: E402
from scripts import reil_c4_monitor as mon  # noqa: E402,F401
from scripts import reil_c5_pilot as c5  # noqa: E402

p0 = c5.p0
E3aStop = e3a.E3aStop

SOURCE_URL = "https://github.com/REIL-UConn/Multi-Objective-Optimization-for-Lithium-Ion-Battery-Degradation-Diagnostics.git"
SOURCE_COMMIT = "1188c371e5836df4a7e5f5acf336a34ffd4027e6"
UTIL_BYTES = 33_754
FETCH_FILES = {"LFP_Data.xlsx": {"bytes": p0.SIZE_XLSX, "sha256": p0.SHA_XLSX},
               "util_LFP.py": {"bytes": UTIL_BYTES, "sha256": p0.SHA_UTIL}}
FETCH_TIMEOUT_S = 240.0
P0_RESULT = BMS / "evidence" / "reil_p0_20261006" / "P0_RESULT.json"
P0_RESULT_SHA = "3875e65092b38c9b08c907926bd8d1f4ee25674c97c28b5ada935e9027d12a90"
N_WORKERS = 4
TICK_S = 1.0
CALL_CAP_S = 1800.0
COST_MIN_SAMPLES = 8
LIMITS = {"prep": 900.0, "measure": 9000.0, "record": 9900.0, "stage": 10800.0, "grace": 60.0,
          "rss": 4 * 2 ** 30, "rss_gap": 5.0, "disk_new": 2 ** 30, "disk_free": 5 * 2 ** 30, "disk_gap": 15.0}
COST_REASON = "비용 중단 — 고정 비용 투영 모형에서 측정 마감 초과로 추정"
RECORD_FILES = ("ROWS.json", "AGGREGATE.json", "OPERATION.json", "RESOURCES.json", "RULE.json", "IDENTITY.json", "HEADER.json",
                "END_RECORD.json")
OPERATION_KEYS = ("global_stop", "structural", "workers", "worker_end", "worker_deadline", "exitcodes", "owned_alive_after",
                  "drain_ok", "t_stop", "deadline_rel")
REQUIRED_FIELDS = ("task_id", "call_id", "case", "row", "obj_selection", "algorithm", "worker",
                   "n_eval", "n_nonfinite", "n_nonfinite_any_of_4", "n_out_eval_PE", "n_out_eval_NE", "n_out_eval_any",
                   "n_out_unknown_eval", "n_dvdq_observed", "n_eval_x_out_of_box", "n_eval_G_violated",
                   "extraction", "model_digest", "halfcell_digest", "warnings_count", "warnings_distinct_overflow",
                   "success_is_evidence", "n_eval_minus_expected",
                   "termination", "error", "X", "F", "G", "G_status", "n_solutions", "F_nonfinite_count", "G_violation_recomputed",
                   "G_violation_exact", "box_violation_exact", "success_reported",
                   "wall", "cpu", "state", "t_start_rel")
ROW_KEYS = ("n_points", "V_first", "V_last", "Q_first", "Q_exp_max")
REF_KEYS = ("sheet", "step_idx", "cell_idx", "n_points", "V_first", "V_last", "Q_first", "Q_last")


class RuleInputError(ValueError):
    """규칙 입력 검증 실패 (v3 §4-3) — 감시가 우리 구조 오류로 기록한다. 표본을 빼거나 0 으로 채우지 않는다."""


def _todo(*args, **kwargs):
    raise NotImplementedError("C4-E E0 골격 — 구현 전 (v3 §6-1 3)")


plan = validate = call_cap = cost_projection = aggregate = _todo
identity_table = identity_problems = identity_changed = pre_verdict = final_verdict = stage_verdict = _todo
check_paths = load_inputs = binding_problems = consumed = expected_identity = _todo
prepare = record_parts = finalize = execute = run = _todo
fetch_steps = show_argv = fetch = plan_e = main = _todo


class StopRule:
    """감시가 tick 마다 부르는 규칙 (v3 §4-2 · §4-3) — 골격."""

    def __init__(self, *args, **kwargs):
        raise NotImplementedError("C4-E E0 골격 — 구현 전 (v3 §6-1 3)")


if __name__ == "__main__":
    sys.exit(main())
