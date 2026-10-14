"""REIL C4-E — E3a 66 호출 실행 진입점 (`fetch` · `plan-e` · `run`) · 호출당 상한 · 비용 투영 규칙 (v3 · 상태 문서 §66).

    <venv>/bin/python -I bms-balancing/scripts/reil_c4e_run.py plan-e --venv V --seal S --seal-manifest-sha256 H --out <새 폴더>
    <venv>/bin/python -I bms-balancing/scripts/reil_c4e_run.py fetch  --dest <저장소 밖 새 폴더>
    <venv>/bin/python -I bms-balancing/scripts/reil_c4e_run.py run    --venv V --seal S --seal-manifest-sha256 H --xlsx X --util U
                                                                      --out <새 폴더> --approval <상태 문서 절>

승인 · 범위: `docs/REIL_C4E_APPROVAL_REQUEST_v3_20261014.md` (§3 · §4 · §5 · §6 · 수용 §65) · 상태 문서 §66. **E0 은 대조와 `plan-e` 만
부른다 — `fetch` · `run` 은 E1 (E0 결과 검토 수용 뒤 별도 GO) 에서만 쓴다.** 봉인 경로 · MANIFEST sha256 은 기본값이 없다 (C4 규칙).

- **`fetch`** (v3 §3 2): 저장소 밖 새 폴더에 `git init` → 이름 있는 remote `origin` (= 고정 공개 URL) → `fetch --depth 1 --filter=blob:none`
  고정 커밋 → `git show <커밋>:<경로>` 를 두 경로에만. checkout · 전체 clone 없음. 부분 clone 의 지연 blob 읽기는 등록된 promisor remote 를
  쓰므로 URL 을 이름 있는 remote 로 둔다 (같은 URL · 커밋 · filter · 경로). sha · bytes 대조. 기록은 argv · cwd · 시각 · sha · bytes 만.
- **`plan-e`** (E0 건조): identity · 원천 sha · P0 · 발췌 · 계획 · 규칙 매개변수 · 기대 자료 식별 → `PLAN_E.json` 하나. util import · 자료 ·
  optimizer · 네트워크 0.
- **`run`** (v3 §3 2 의 1–13): 원점 → identity · 원천 / 입력 시작 sha → 경로 → util import → 적재 → P0 정확 대조 → 소비 digest → 계획 →
  감시 (`stop_rule` = 호출당 상한 + 비용 투영) → 사후 집계 → 끝 식별 재해시 → 사전 판정 → `final_record` 한 번 (끝 기록 포함 · 단계 안
  마지막 쓰기) → 최종 판정 stdout (snapshot 뒤 외부 반환 · 산출 루트 밖 · 루트 안에는 더 쓰지 않는다).
- 판정 (v3 §4-7): 관측 집계와 E3a COMPLETE 를 나눈다. 사전 판정 = 조건 1–4 · 6 · 최종 판정 = 사전 AND `final_record` COMPLETE AND 위반 0 ·
  단계 판정 = 최종 AND 단계 실행기 rc 0 · timeout 없음 (`stage_verdict` — run 밖의 meta 로).
"""
from __future__ import annotations

import argparse
import datetime
import json
import math
import os
import struct
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve()
BMS = HERE.parents[1]
REPO = HERE.parents[2]
if str(BMS) not in sys.path:      # `-I` 실행은 스크립트 폴더를 sys.path 에 넣지 않는다 — 시험과 같은 `scripts.` 모듈 객체를 쓴다
    sys.path.insert(0, str(BMS))
from scripts import reil_c4_e3a as e3a  # noqa: E402
from scripts import reil_c4_monitor as mon  # noqa: E402
from scripts import reil_c5_pilot as c5  # noqa: E402

p0 = c5.p0
E3aStop = e3a.E3aStop
_sha = c5._sha

#: 원자료 출처 (P0 고정 · 상태 문서 §20 · v3 §1) — 다른 출처는 쓰지 않는다
SOURCE_URL = "https://github.com/REIL-UConn/Multi-Objective-Optimization-for-Lithium-Ion-Battery-Degradation-Diagnostics.git"
SOURCE_COMMIT = "1188c371e5836df4a7e5f5acf336a34ffd4027e6"
UTIL_BYTES = 33_754                                         # 고정 커밋의 util 원본 (CRLF 846 · 끝 줄바꿈 없음 · §11-3 = 원본)
FETCH_FILES = {"LFP_Data.xlsx": {"bytes": p0.SIZE_XLSX, "sha256": p0.SHA_XLSX},
               "util_LFP.py": {"bytes": UTIL_BYTES, "sha256": p0.SHA_UTIL}}
FETCH_TIMEOUT_S = 240.0
P0_RESULT = BMS / "evidence" / "reil_p0_20261006" / "P0_RESULT.json"
P0_RESULT_SHA = "3875e65092b38c9b08c907926bd8d1f4ee25674c97c28b5ada935e9027d12a90"
MODULES = (HERE, Path(e3a.__file__).resolve(), Path(mon.__file__).resolve(), Path(c5.__file__).resolve(), Path(p0.__file__).resolve())

N_WORKERS = 4
TICK_S = 1.0
CALL_CAP_S = 1800.0
COST_MIN_SAMPLES = 8
#: v3 §4-1 · §4-4 — 원점 t0 = run 시작 (monotonic). record = final_record 최종 snapshot 의 한도 · stage = 단계 실행기의 run timeout (기록만)
LIMITS = {"prep": 900.0, "measure": 9000.0, "record": 9900.0, "stage": 10800.0, "grace": 60.0,
          "rss": 4 * 2 ** 30, "rss_gap": 5.0, "disk_new": 2 ** 30, "disk_free": 5 * 2 ** 30, "disk_gap": 15.0}
COST_REASON = "비용 중단 — 고정 비용 투영 모형에서 측정 마감 초과로 추정"
#: final_record 의 쓰기 순서 — 끝 기록 (사전 판정과 근거) 이 단계 안의 마지막 쓰기다 (v3 §3 2 의 12)
RECORD_FILES = ("ROWS.json", "AGGREGATE.json", "OPERATION.json", "RESOURCES.json", "RULE.json", "IDENTITY.json", "HEADER.json",
                "END_RECORD.json")
OPERATION_KEYS = ("global_stop", "structural", "workers", "worker_end", "worker_deadline", "exitcodes", "owned_alive_after",
                  "drain_ok", "t_stop", "deadline_rel")
#: C4-0a 기록 필드 (`e3a.run_e3a_call` 의 returned 행 + 감시 `_states` 의 t_start_rel) — 조건 2
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


def _utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def _is_int(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def _finite(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def _same(a, b) -> bool:
    """정확 일치 — float 는 비트까지 (1 ulp 도 다르다) · 그 밖은 형과 값."""
    if isinstance(a, float) or isinstance(b, float):
        return isinstance(a, float) and isinstance(b, float) and struct.pack("<d", a) == struct.pack("<d", b)
    return type(a) is type(b) and a == b


def _tid_key(t):
    """task 번호 정렬 — 정수는 수 순서 · 그 밖 (검증에서 걸러질 값) 은 뒤에 문자열 순서."""
    return (0, t, "") if _is_int(t) else (1, 0, str(t))


def _stop(message: str, record=None):
    err = E3aStop(message)
    err.record = record
    return err


# ---------------------------------------------------------------- 계획 (C4-0a 그대로)
def plan() -> list:
    """C4-0a 계획 (`e3a.plan_calls(4)`) — 66 호출 · 번호 = case × 11 + 행 · 작업자 = 번호 mod 4 · 알고리즘 · 기대 평가 (산술 · 한도 아님)."""
    return e3a.plan_calls(N_WORKERS)


# ---------------------------------------------------------------- 규칙 (v3 §4-2 · §4-3) — 결과값 (X · F · G) 은 읽지 않는다
def validate(snap, plan_by_id) -> None:
    """계산 전 입력 검증 — 하나라도 어긋나면 `RuleInputError` (빼기 · 0 채우기 없음). 완료 행에서는 wall · n_eval · termination 만 본다."""
    planned = list(snap["planned"])
    pset = set(planned)
    if len(pset) != len(planned) or pset != set(plan_by_id):
        raise RuleInputError(f"계획 집합이 다르다 (snapshot {len(planned)} · 계획 {len(plan_by_id)})")
    started, done, prog = snap["started"], snap["done"], snap["progress"]
    if not _finite(snap["now_rel"]):
        raise RuleInputError(f"now_rel 이 유한하지 않다: {snap['now_rel']!r}")
    out = sorted(set(started) - pset, key=_tid_key)
    if out:
        raise RuleInputError(f"계획 밖 task 가 시작됐다: {out}")
    out = sorted(set(done) - set(started), key=_tid_key)
    if out:
        raise RuleInputError(f"done ⊄ started — 시작 사건 없이 완료: {out}")
    if set(prog) != pset:
        raise RuleInputError("progress 의 task 집합이 계획과 다르다")
    for tid in planned:
        if not _is_int(prog[tid]) or prog[tid] < 0:
            raise RuleInputError(f"task {tid} progress {prog[tid]!r} — 정수 ≥ 0 이 아니다")
    for tid in sorted(started, key=_tid_key):
        if not _finite(started[tid]):
            raise RuleInputError(f"task {tid} 시작 상대 시각 {started[tid]!r} 이 유한하지 않다")
    for tid in sorted(done, key=_tid_key):
        d = done[tid]
        term, wall = d.get("termination"), d.get("wall")
        if term not in ("returned", "error"):
            raise RuleInputError(f"task {tid} termination {term!r} — returned / error 가 아니다")
        if not _finite(wall) or wall < 0:
            raise RuleInputError(f"task {tid} wall {wall!r} — 유한 · ≥ 0 이 아니다")
        if term == "returned":
            n = d.get("n_eval")
            if not _is_int(n) or n < 1:
                raise RuleInputError(f"task {tid} n_eval {n!r} — returned 행은 정수 ≥ 1")


def call_cap(snap, cap=CALL_CAP_S) -> dict:
    """호출당 상한 (v3 §4-2) — 진행 중 = now_rel − started · 완료 = 행의 wall · 엄격한 > (같으면 넘지 않음). 늦은 완료를 먼저 적는다."""
    now, started, done = snap["now_rel"], snap["started"], snap["done"]
    active = [{"task_id": tid, "elapsed_observed": now - started[tid], "detected_rel": now}
              for tid in sorted(started, key=_tid_key) if tid not in done and now - started[tid] > cap]
    late = [{"task_id": tid, "wall": done[tid]["wall"], "detected_rel": now}
            for tid in sorted(done, key=_tid_key) if done[tid]["wall"] > cap]
    parts = []
    if late:
        parts.append("호출당 상한 (늦은 완료 · " + ", ".join(f"{x['task_id']}: wall {x['wall']:.3f} s" for x in late) + f" > {cap} s)")
    if active:
        parts.append("호출당 상한 (진행 중 · " + ", ".join(f"{x['task_id']}: {x['elapsed_observed']:.3f} s" for x in active)
                     + f" > {cap} s)")
    return {"cap": cap, "active_over": active, "late": late, "reason": " · ".join(parts) if parts else None}


def cost_projection(snap, plan, *, min_samples=COST_MIN_SAMPLES, measure=LIMITS["measure"]) -> dict:
    """비용 투영 (v3 §4-3) — 완료 returned 의 c = wall / n_eval · 위쪽 중앙 순서통계 m (오름차순 0-기반 ⌊n/2⌋) · 최소 표본 · 누적 창 ·
    작업자 w 마다 R_w = (미착수 배정 호출의 기대 평가 합 + 진행 중 호출의 max(기대 평가 − progress, 0)) × m · now_rel + max R_w > 경계 → 중지."""
    by_id = plan if isinstance(plan, dict) else {t["task_id"]: t for t in plan}
    done, started, prog = snap["done"], snap["started"], snap["progress"]
    ret = sorted((tid for tid in done if done[tid]["termination"] == "returned"), key=_tid_key)
    samples = [{"task_id": tid, "wall": done[tid]["wall"], "n_eval": done[tid]["n_eval"],
                "c": done[tid]["wall"] / done[tid]["n_eval"]} for tid in ret]
    rec = {"now_rel": snap["now_rel"], "returned_ids": ret, "n_samples": len(samples), "samples": samples,
           "min_samples": int(min_samples), "boundary": float(measure), "m": None, "judged": False,
           "remaining_expected_evals": None, "R": None, "value": None, "stop": False, "reason": None}
    if len(samples) < min_samples:
        return rec
    cs = sorted(s["c"] for s in samples)
    m = cs[len(cs) // 2]
    rem = {}
    for tid in snap["planned"]:
        t = by_id[tid]
        w, exp = t["worker"], t["algorithm"]["expected_evals"]
        rem.setdefault(w, 0)
        if tid not in started:
            rem[w] += exp
        elif tid not in done:
            rem[w] += max(exp - prog[tid], 0)
    r_w = {w: v * m for w, v in rem.items()}
    value = snap["now_rel"] + (max(r_w.values()) if r_w else 0.0)
    stop = value > measure
    rec.update(m=m, judged=True, remaining_expected_evals={str(w): rem[w] for w in sorted(rem)},
               R={str(w): r_w[w] for w in sorted(r_w)}, value=value, stop=stop,
               reason=(f"{COST_REASON} (now_rel {snap['now_rel']:.3f} + max R_w {value - snap['now_rel']:.3f} = {value:.3f} s > "
                       f"{measure} s · m {m:.6g} s/평가 · 표본 {len(samples)})") if stop else None)
    return rec


class StopRule:
    """감시가 tick 마다 부르는 규칙 (v3 §4-2 · §4-3): 입력 검증 → 호출당 상한 → 비용 투영. 상태는 바꾸지 않고 사유와 기록만 남긴다.
    진행 중 초과는 '중단 요청 대상' 으로 적고, 최종 상태는 감시의 마지막 drain 뒤 사후 집계 (`aggregate`) 가 붙인다."""

    def __init__(self, plan, *, cap=CALL_CAP_S, min_samples=COST_MIN_SAMPLES, measure=LIMITS["measure"]):
        self.plan = {t["task_id"]: t for t in plan}
        self.cap, self.min_samples, self.measure = float(cap), int(min_samples), float(measure)
        self.active_over: list = []
        self.late_seen: list = []
        self.stop = None
        self.last = None
        self.n_calls = 0

    def __call__(self, snap):
        self.n_calls += 1
        validate(snap, self.plan)
        cap = call_cap(snap, self.cap)
        if cap["reason"] is not None:
            self.active_over += cap["active_over"]
            self.late_seen += cap["late"]
            self.stop = {"kind": "call_cap", "now_rel": snap["now_rel"], **cap}
            return cap["reason"]
        cost = cost_projection(snap, self.plan, min_samples=self.min_samples, measure=self.measure)
        self.last = cost
        if cost["stop"]:
            self.stop = {"kind": "cost", **cost}
            return cost["reason"]
        return None

    def params(self) -> dict:
        return {"cap_s": self.cap, "compare": "엄격한 > (같으면 넘지 않음)", "min_samples": self.min_samples, "measure_s": self.measure,
                "statistic": "위쪽 중앙 순서통계 — returned 의 c = wall / n_eval 오름차순 0-기반 index ⌊n/2⌋",
                "window": "누적 (완료된 returned 전부) · tick 마다 다시 계산",
                "projection": "R_w = (미착수 배정 호출의 기대 평가 합 + 진행 중 호출의 max(기대 평가 − progress, 0)) × m",
                "boundary": "now_rel + max_w R_w > measure 이면 중지", "inputs": "snapshot 의 wall · n_eval · termination · progress 만"}

    def record(self) -> dict:
        return {"params": self.params(), "n_calls": self.n_calls, "stop": self.stop, "last": self.last,
                "active_over": list(self.active_over), "late_seen": list(self.late_seen)}


# ---------------------------------------------------------------- 사후 집계 · 판정 (v3 §4-2 · §4-7)
def aggregate(sup, plan, rule) -> dict:
    """감시의 마지막 drain 뒤 상태 (done 우선 · 원행) 위의 사후 집계 — 상태 · 행은 바꾸지 않는다. 관측 집계 · 모든 COMPLETED 행의 wall 대조
    (마지막 drain 에서 처음 받은 행 포함) · 중단 요청 대상에 최종 상태를 붙인다. 이미 걸린 global_stop 은 그대로 둔다."""
    states = list(sup["states"])
    planned = [t["task_id"] for t in plan]
    ids = [s.get("task_id") for s in states]
    problems = []
    if len(ids) != len(set(ids)) or sorted(ids, key=_tid_key) != sorted(planned, key=_tid_key):
        problems.append(f"감시 상태의 task 집합이 계획과 다르다 (상태 {len(ids)} · 고유 {len(set(ids))} · 계획 {len(planned)})")
    obs = {"planned": len(planned), "COMPLETED_returned": 0, "COMPLETED_error": 0, "STARTED_INTERRUPTED": 0, "NOT_STARTED": 0,
           "other": 0}
    for s in states:
        st, term = s.get("state"), s.get("termination")
        if st == "COMPLETED" and term in ("returned", "error"):
            obs[f"COMPLETED_{term}"] += 1
        elif st in ("STARTED_INTERRUPTED", "NOT_STARTED"):
            obs[st] += 1
        else:
            obs["other"] += 1
    obs["sum"] = obs["COMPLETED_returned"] + obs["COMPLETED_error"] + obs["STARTED_INTERRUPTED"] + obs["NOT_STARTED"] + obs["other"]
    if obs["other"] or obs["sum"] != len(planned):
        problems.append(f"관측 집계가 계획을 나누지 않는다: {obs}")
    late = []
    for s in states:
        if s.get("state") != "COMPLETED":
            continue
        w = s.get("wall")
        if not _finite(w) or w < 0:
            problems.append(f"task {s.get('task_id')} COMPLETED 행의 wall {w!r} — 상한 대조 불가")
        elif w > rule.cap:
            late.append({"task_id": s.get("task_id"), "wall": w, "termination": s.get("termination")})
    by_id = {s.get("task_id"): s for s in states}
    over = []
    for rec in rule.active_over:
        s = by_id.get(rec["task_id"], {})
        fin = s.get("state")
        over.append({**rec, "final_state": fin, "termination": s.get("termination") if fin == "COMPLETED" else None})
    return {"observed": obs, "late_completions": late, "over_cap_active": over, "cap_s": rule.cap,
            "global_stop": sup.get("global_stop"), "structural_n": len(sup.get("structural") or []), "problems": problems}


def identity_table(files: dict, expected: dict) -> dict:
    """{이름: 경로} → {이름: 경로 · 기대 · sha256 · bytes} (읽기만 · 못 읽으면 sha256 None)."""
    out = {}
    for name, p in files.items():
        try:
            b = Path(p).read_bytes()
            sha, n = _sha(b), len(b)
        except OSError:
            sha, n = None, None
        out[name] = {"path": str(p), "expected": expected.get(name), "sha256": sha, "bytes": n}
    return out


def identity_problems(table: dict) -> list:
    probs = []
    for name, row in table.items():
        exp = row.get("expected")
        if exp is None:
            continue
        if row.get("sha256") != exp.get("sha256") or ("bytes" in exp and row.get("bytes") != exp["bytes"]):
            probs.append(f"{name}: sha256 {row.get('sha256')} · {row.get('bytes')} B ≠ 기대 {exp}")
    return probs


def identity_changed(start: dict, end: dict) -> list:
    return sorted(n for n in set(start) | set(end)
                  if (start.get(n) or {}).get("sha256") != (end.get(n) or {}).get("sha256") or (start.get(n) or {}).get("sha256") is None)


def pre_verdict(plan, agg, sup, ident_start, ident_end, *, n_workers=N_WORKERS) -> dict:
    """사전 판정 (v3 §4-7 조건 1–4 · 6) — `final_record` 전의 판정이다. 최종 판정은 끝 기록까지 쓴 final_record 뒤에만 (`final_verdict`)."""
    states, reasons = sup["states"], []
    ret = [s for s in states if s.get("state") == "COMPLETED" and s.get("termination") == "returned"]
    c1 = len(ret) == len(plan) and not agg["problems"]
    if not c1:
        reasons.append(f"조건 1: returned {len(ret)} / {len(plan)} · 관측 {agg['observed']} · {agg['problems']}")
    missing = {s.get("task_id"): [k for k in REQUIRED_FIELDS if k not in s] for s in ret}
    missing = {k: v for k, v in missing.items() if v}
    c2 = not missing
    if not c2:
        reasons.append(f"조건 2: 기록 필드 누락 {missing}")
    c3 = sup.get("global_stop") is None and not sup.get("structural")
    if not c3:
        reasons.append(f"조건 3: global_stop {sup.get('global_stop')!r} · structural {len(sup.get('structural') or [])}")
    ws = set(range(n_workers))
    ends = {int(k) for k in (sup.get("worker_end") or {})}
    codes = {int(k): v for k, v in (sup.get("exitcodes") or {}).items()}
    c4 = (ends == ws and not sup.get("worker_deadline") and codes == {w: 0 for w in ws}
          and sup.get("owned_alive_after") == 0 and sup.get("drain_ok") is True)
    if not c4:
        reasons.append(f"조건 4: worker_end {sorted(ends)} · worker_deadline {sup.get('worker_deadline')} · exitcodes {codes} · "
                       f"owned_alive_after {sup.get('owned_alive_after')} · drain_ok {sup.get('drain_ok')}")
    changed, probs = identity_changed(ident_start, ident_end), identity_problems(ident_start)
    c6 = not changed and not probs and not agg["late_completions"] and not agg["over_cap_active"]
    if not c6:
        reasons.append(f"조건 6: 시작 / 끝 식별 변화 {changed} · 시작 식별 문제 {probs} · 늦은 완료 "
                       f"{[x['task_id'] for x in agg['late_completions']]} · 진행 중 초과 {[x['task_id'] for x in agg['over_cap_active']]}")
    complete = c1 and c2 and c3 and c4 and c6
    return {"kind": "사전 판정 (v3 §4-7 조건 1–4 · 6) — 최종 판정이 아니다", "complete": complete,
            "conditions": {"1": c1, "2": c2, "3": c3, "4": c4, "6": c6}, "reasons": reasons}


def final_verdict(pre, fr) -> dict:
    """run 최종 판정 = 사전 판정 AND `final_record` COMPLETE AND 위반 0 (v3 §4-7 조건 5). 앞선 판정으로 뒤의 실패를 가리지 않는다."""
    rec_ok = fr.get("record_state") == "COMPLETE" and not fr.get("limit_violations")
    complete = bool(pre.get("complete")) and rec_ok
    reasons = list(pre.get("reasons") or [])
    if not rec_ok:
        reasons.append(f"조건 5: record_state {fr.get('record_state')} · 위반 {fr.get('limit_violations')} · {fr.get('problems')}")
    return {"kind": "run 최종 판정 (조건 1–6) — 단계 판정은 단계 실행기 meta 와 AND (stage_verdict)", "complete": complete,
            "E3a": "COMPLETE" if complete else "INCOMPLETE", "c4a_gate": complete, "record_state": fr.get("record_state"),
            "limit_violations": fr.get("limit_violations"), "final_snapshot_s": fr.get("final_snapshot_s"), "reasons": reasons}


def stage_verdict(final, meta) -> dict:
    """단계 판정 = run 최종 판정 AND 단계 실행기 rc 0 · timeout 없음 (v3 §4-7 조건 7 — run 자신이 아니라 단계 실행기 meta 로)."""
    runner_ok = meta.get("rc") == 0 and meta.get("timed_out") is False
    complete = bool((final or {}).get("complete")) and runner_ok
    return {"kind": "단계 판정 (v3 §4-7 조건 7)", "complete": complete, "E3a": "COMPLETE" if complete else "INCOMPLETE",
            "c4a_gate": complete, "runner": {"rc": meta.get("rc"), "timed_out": meta.get("timed_out"), "elapsed_s": meta.get("elapsed_s")},
            "final_received": final is not None}


# ---------------------------------------------------------------- 자료 결속 (v3 §4-6)
def check_paths(*, xlsx, util, out) -> None:
    """경로 경계 (v3 §3 2 의 3): 자료 파일은 저장소 밖 · `.pkl` · `.ipynb` 거부 · 출력 폴더는 새로."""
    for name, p in (("xlsx", xlsx), ("util", util)):
        rp = Path(p).resolve()
        if mon.owned(rp, [REPO.resolve()]):
            raise E3aStop(f"{name} 경로가 저장소 안이다: {rp} — 원자료는 저장소 밖에서만 읽는다")
    for p in (xlsx, util, out):
        if str(p).lower().endswith((".pkl", ".ipynb")):
            raise E3aStop(f"금지 경로 (.pkl · .ipynb): {p}")
    if Path(out).exists():
        raise E3aStop(f"출력 폴더가 이미 있다: {out} — 새로 만든다 (덮어쓰기 · 재사용 없음)")


def load_inputs(util, xlsx) -> dict:
    """P0 (`reil_p0.py:341–380`) · C5 (`reil_c5_pilot.py:871–885`) 와 같은 그들 함수 · 같은 인자 — Model 11 · halfcell · 대조용 기록."""
    import numpy as np
    area = 0.25 * np.pi * 1.2 ** 2
    lfp_mass_12, gr_mass_12 = 13.5 * area, 5.77 * area
    refs, ref_rec = {}, []
    for sheet in p0.SHEETS_REF:
        arr = util.visualize_LFP_data(data_file=str(xlsx), sheet_name=sheet, step_idx=p0.REF_STEP)[p0.REF_CELL]
        refs[sheet] = arr
        ref_rec.append({"sheet": sheet, "kind": "reference", "step_idx": p0.REF_STEP, "cell_idx": p0.REF_CELL,
                        "n_points": int(arr.shape[1]), "V_first": float(arr[1][0]), "V_last": float(arr[1][-1]),
                        "Q_first": float(arr[0][0]), "Q_last": float(arr[0][-1])})
    pe, ne = refs[p0.SHEETS_REF[0]], refs[p0.SHEETS_REF[1]]
    q_pe = pe[0][np.argmin(pe[0]):np.argmax(pe[0])] / lfp_mass_12 * 20.16
    v_pe = pe[1][np.argmin(pe[0]):np.argmax(pe[0])]
    q_ne = ne[0][np.argmin(ne[0]):np.argmax(ne[0])] / gr_mass_12 * 11.4
    v_ne = ne[1][np.argmin(ne[0]):np.argmax(ne[0])]
    models, rows = {}, []
    for i in e3a.ROWS:
        d = util.visualize_LFP_data(data_file=str(xlsx), sheet_name=p0.SHEETS_ANALYSIS[i], step_idx=p0.STEP_IDX[i], visualize=False)
        m = util.extract_battery_data(data=d, idx=p0.CELL_IDX[i])
        models[i] = m
        rows.append({"row": i, "sheet": p0.SHEETS_ANALYSIS[i], "cell_idx": p0.CELL_IDX[i], "step_idx": p0.STEP_IDX[i],
                     "n_points": int(len(m["Q_exp"])), "V_first": float(m["V_exp"][0]), "V_last": float(m["V_exp"][-1]),
                     "Q_first": float(m["Q_exp"][0]), "Q_exp_max": float(m["Q_exp_max"])})
    return {"models": models, "halfcell": [q_pe, v_pe, q_ne, v_ne], "rows": rows, "references": ref_rec,
            "PE": {"max_q": float(np.max(q_pe.flatten())), "n_q_PE_hc": int(q_pe.size)},
            "NE": {"q_NE_hc_max_record_only": float(np.max(q_ne))}}


def binding_problems(loaded, res) -> list:
    """P0 기록과 정확 대조 (float 비트 동일 · 조정 · 재추출 없음) — 분석 11 행 · reference 둘 · PE max_q / 길이 · NE 최대."""
    probs, ext = [], res.get("extraction") or []
    ana = {e.get("row"): e for e in ext if e.get("kind") == "analysis"}
    refs = {e.get("sheet"): e for e in ext if e.get("kind") == "reference"}
    if set(ana) != set(e3a.ROWS) or any(e.get("status") != "OK" for e in ana.values()):
        probs.append(f"P0 분석 기록이 #0–#10 전부 OK 가 아니다: {sorted(ana, key=str)}")
    for r in loaded["rows"]:
        want = ana.get(r["row"]) or {}
        for k in ROW_KEYS:
            if k not in want or not _same(want[k], r[k]):
                probs.append(f"분석 행 #{r['row']} {k}: 적재 {r[k]!r} ≠ P0 {want.get(k)!r}")
    if set(refs) != set(p0.SHEETS_REF) or any(e.get("status") != "OK" for e in refs.values()):
        probs.append(f"P0 reference 기록이 둘 다 OK 가 아니다: {sorted(refs, key=str)}")
    for r in loaded["references"]:
        want = refs.get(r["sheet"]) or {}
        for k in REF_KEYS:
            if k not in want or not _same(want[k], r[k]):
                probs.append(f"reference {r['sheet']} {k}: 적재 {r[k]!r} ≠ P0 {want.get(k)!r}")
    mq = res.get("max_q") or {}
    if not _same(mq.get("float"), loaded["PE"]["max_q"]):
        probs.append(f"PE max_q: 적재 {loaded['PE']['max_q']!r} ≠ P0 {mq.get('float')!r}")
    if not _same(mq.get("n_q_PE_hc"), loaded["PE"]["n_q_PE_hc"]):
        probs.append(f"PE n_q_PE_hc: 적재 {loaded['PE']['n_q_PE_hc']!r} ≠ P0 {mq.get('n_q_PE_hc')!r}")
    if not _same(res.get("q_NE_hc_max_record_only"), loaded["NE"]["q_NE_hc_max_record_only"]):
        probs.append(f"NE q_NE_hc_max_record_only: 적재 {loaded['NE']['q_NE_hc_max_record_only']!r} ≠ P0 "
                     f"{res.get('q_NE_hc_max_record_only')!r}")
    return probs


def consumed(models, halfcell) -> dict:
    """실제로 넘긴 입력의 digest 와 선택 인자 (v3 §4-6) — 기록만으로 잘못된 적재가 교정되지는 않는다 (d_3 의 합성 대조가 함께 필요)."""
    import numpy as np
    area = 0.25 * np.pi * 1.2 ** 2
    return {"models": {str(r): c5.model_digest(models[r]) for r in sorted(models)}, "halfcell": c5.model_digest(halfcell),
            "selection": {"call": "visualize_LFP_data(data_file, sheet_name, step_idx, visualize=False) → extract_battery_data(data, idx)",
                          "sheets": list(p0.SHEETS_ANALYSIS), "step_idx": list(p0.STEP_IDX), "cell_idx": list(p0.CELL_IDX),
                          "reference": {"sheets": list(p0.SHEETS_REF), "step_idx": p0.REF_STEP, "cell_idx": p0.REF_CELL},
                          "mass": {"area": "0.25 π 1.2²", "LFP_mass_12": 13.5 * area, "Gr_mass_12": 5.77 * area},
                          "scale": {"PE": 20.16, "NE": 11.4}, "slice": "[argmin(Q) : argmax(Q)]",
                          "halfcell": "[q_PE, v_PE, q_NE, v_NE]"}}


def expected_identity(manifest_sha256, override=None) -> dict:
    exp = {"LFP_Data.xlsx": dict(FETCH_FILES["LFP_Data.xlsx"]), "util_LFP.py": dict(FETCH_FILES["util_LFP.py"]),
           "P0_RESULT.json": {"sha256": P0_RESULT_SHA}, "NOTEBOOK_SOURCE_EXCERPTS.json": {"sha256": e3a.EXCERPTS_SHA},
           "MANIFEST.json": {"sha256": manifest_sha256}}
    exp.update(override or {})
    return exp


def _module_files() -> dict:
    return {f"scripts/{m.name}": m for m in MODULES}


# ---------------------------------------------------------------- run (v3 §3 2 의 1–13)
def prepare(*, venv, seal, manifest_sha256, xlsx, util_path, out, p0_result=P0_RESULT, excerpts=e3a.EXCERPTS, expected=None,
            env_identity=None, load_util=None, header=None) -> dict:
    """run 의 2–7: identity → 원천 · 입력 시작 sha → 경로 (출력 폴더 새로) → util import → 적재 → P0 정확 대조 → 소비 digest → 계획.
    앞에서 어긋나면 `E3aStop` — 뒤 단계 (util import · 그들 적재 함수 · optimizer) 는 부르지 않는다."""
    seal, out = Path(seal), Path(out)
    ident = e3a.identity(venv=venv, seal=seal, manifest_sha256=manifest_sha256, env_identity=env_identity)
    if not ident["ok"]:
        raise E3aStop(f"identity 실패: {ident['problems']}")
    files = {"LFP_Data.xlsx": Path(xlsx), "util_LFP.py": Path(util_path), "P0_RESULT.json": Path(p0_result),
             "NOTEBOOK_SOURCE_EXCERPTS.json": Path(excerpts), "MANIFEST.json": seal / "MANIFEST.json", **_module_files()}
    exp = expected_identity(manifest_sha256, expected)
    id_start = identity_table(files, exp)
    probs = identity_problems(id_start)
    if probs:
        raise E3aStop("시작 식별 불일치 — " + "; ".join(probs))
    nb = e3a.notebook_case_table(excerpts)
    check_paths(xlsx=xlsx, util=util_path, out=out)
    out.mkdir(parents=True)
    res = json.loads(Path(p0_result).read_bytes())
    util, uf = (load_util or c5.load_util)(util_path, exp["util_LFP.py"]["sha256"])
    loaded = load_inputs(util, xlsx)
    probs = binding_problems(loaded, res)
    if probs:
        raise E3aStop("P0 적재 대조 불일치 — optimizer 를 부르지 않는다: " + "; ".join(probs[:20]))
    ext = {e["row"]: e for e in res["extraction"] if e.get("kind") == "analysis"}
    ctx = {"util": util, "util_file": uf, "models": loaded["models"], "halfcell": loaded["halfcell"],
           "extraction": {r: ext[r] for r in e3a.ROWS}}
    calls = plan()
    hdr = {"argv": list(sys.argv), "cwd": os.getcwd(), "identity": ident, "notebook": nb, "expected": exp,
           "consumed": consumed(loaded["models"], loaded["halfcell"]),
           "binding": {"equal": True, "rows": loaded["rows"], "references": loaded["references"], "PE": loaded["PE"],
                       "NE": loaded["NE"], "p0_result": str(p0_result)},
           "util_file": uf, "xlsx": str(xlsx), "out": str(out), "blas_env_set": {k: os.environ.get(k) for k in c5.BLAS_VARS},
           **(header or {})}
    return {"out": out, "plan": calls, "ctx": ctx, "files": files, "expected": exp, "id_start": id_start, "header": hdr}


def record_parts(*, header, sup, agg, rule, ident_start, ident_end, pre) -> dict:
    """final_record 에 넘길 기록 (쓰기 순서 = `RECORD_FILES`) — 시각 값은 넣지 않는다 (snapshot 은 final_record 가 잰다)."""
    return {"ROWS.json": sup["states"], "AGGREGATE.json": agg, "OPERATION.json": {k: sup.get(k) for k in OPERATION_KEYS},
            "RESOURCES.json": sup.get("samples"), "RULE.json": rule.record(),
            "IDENTITY.json": {"start": ident_start, "end": ident_end, "changed": identity_changed(ident_start, ident_end)},
            "HEADER.json": header,
            "END_RECORD.json": {"pre_verdict": pre, "note": "사전 판정 — 최종 판정은 이 파일까지 쓴 final_record 의 snapshot 뒤 (stdout)"}}


def finalize(out, *, plan, sup, rule, ident_start, rehash, header, limits, roots, clock=time.monotonic, t0=0.0,
             n_workers=N_WORKERS) -> dict:
    """run 의 9–13: 사후 집계 → 끝 식별 재해시 → 사전 판정 → `final_record` 한 번 (끝 기록 포함 · 단계 안 마지막 쓰기 · 재읽기 · 해시 →
    같은 산출 루트 크기 · 최종 snapshot) → 최종 판정. 그 뒤 산출 루트 안에는 쓰지 않는다 (반환값은 호출자가 stdout 으로)."""
    agg = aggregate(sup, plan, rule)
    ident_end = rehash()
    pre = pre_verdict(plan, agg, sup, ident_start, ident_end, n_workers=n_workers)
    parts = record_parts(header=header, sup=sup, agg=agg, rule=rule, ident_start=ident_start, ident_end=ident_end, pre=pre)
    fr = mon.final_record(out, parts, roots=roots, limit_bytes=limits["disk_new"], clock=clock, t0=t0, limit_s=limits["record"])
    return {"final": final_verdict(pre, fr), "pre": pre, "final_record": fr, "observed": agg["observed"],
            "global_stop": sup.get("global_stop")}


def execute(prep, *, t0, clock=time.monotonic, limits=None, n_workers=N_WORKERS, tick=TICK_S, disk_every=5.0, supervise=None,
            rss_fn=None, disk_fn=None, rehash=None) -> dict:
    """prep 경계 → 감시 (stop_rule) → 종결. 원점 t0 는 run 시작 — 측정 마감 = t0 + measure (감시가 상대로 계산)."""
    limits = dict(LIMITS if limits is None else limits)
    if clock() - t0 > limits["prep"]:
        raise E3aStop(f"단계 경계 — prep {limits['prep']} s 초과 (원점 기준) · 작업자를 시작하지 않는다")
    rule = StopRule(prep["plan"], cap=CALL_CAP_S, min_samples=COST_MIN_SAMPLES, measure=limits["measure"])
    out = Path(prep["out"])
    sup = (supervise or mon.supervise)(prep["plan"], prep["ctx"], e3a.run_e3a_call, n_workers=n_workers, limits=limits, t0=t0,
                                       clock=clock, rss_fn=rss_fn, disk_fn=disk_fn, out_roots=[out], free_path=out, tick=tick,
                                       disk_every=disk_every, stop_rule=rule)
    header = {**prep["header"], "limits": limits, "rule": rule.params(), "n_workers": n_workers, "tick_s": tick, "t0_monotonic": t0}
    return finalize(out, plan=prep["plan"], sup=sup, rule=rule, ident_start=prep["id_start"],
                    rehash=rehash or (lambda: identity_table(prep["files"], prep["expected"])), header=header, limits=limits,
                    roots=[out], clock=clock, t0=t0, n_workers=n_workers)


def run(out, *, venv, seal, manifest_sha256, xlsx, util_path, approval, p0_result=P0_RESULT, excerpts=e3a.EXCERPTS, expected=None,
        env_identity=None, load_util=None, n_workers=N_WORKERS, tick=TICK_S, limits=None, clock=time.monotonic, rss_fn=None,
        disk_fn=None) -> dict:
    """E1 의 run 1 회 (v3 §3 2 의 1–13). 반환값 = 최종 판정 (호출자가 stdout 으로 · 산출 루트 밖)."""
    t0 = clock()
    if not approval:
        raise E3aStop("run 은 별도 GO 의 승인 기록 (--approval) 없이 시작하지 않는다")
    prep = prepare(venv=venv, seal=seal, manifest_sha256=manifest_sha256, xlsx=xlsx, util_path=util_path, out=out,
                   p0_result=p0_result, excerpts=excerpts, expected=expected, env_identity=env_identity, load_util=load_util,
                   header={"approval": approval, "start_utc": _utc(), "source": {"url": SOURCE_URL, "commit": SOURCE_COMMIT}})
    return execute(prep, t0=t0, clock=clock, limits=limits, n_workers=n_workers, tick=tick, rss_fn=rss_fn, disk_fn=disk_fn)


# ---------------------------------------------------------------- fetch (E1 · E0 에서는 가짜 로컬 git 저장소로만 시험)
def fetch_steps(git_dir, repo_url, commit) -> list:
    """`git init` → 이름 있는 remote `origin` → `fetch --depth 1 --filter=blob:none origin <커밋>` (checkout · clone 없음)."""
    gd = str(git_dir)
    return [["git", "init", "-q", gd], ["git", "-C", gd, "remote", "add", "origin", str(repo_url)],
            ["git", "-C", gd, "fetch", "--depth", "1", "--filter=blob:none", "origin", str(commit)]]


def show_argv(git_dir, commit, path) -> list:
    return ["git", "-C", str(git_dir), "show", f"{commit}:{path}"]


def fetch(dest, *, repo_url=SOURCE_URL, commit=SOURCE_COMMIT, files=None, allow_protocol="https", run=subprocess.run,
          timeout=FETCH_TIMEOUT_S) -> dict:
    """저장소 밖 새 폴더에 고정 커밋의 두 경로만 받는다 — sha · bytes 대조 · 기록 (파일 바이트 없음). GIT_ALLOW_PROTOCOL 로 프로토콜을 하나로 묶는다."""
    files = dict(FETCH_FILES if files is None else files)
    extra = sorted(set(files) - set(FETCH_FILES))
    if extra or not files:
        raise E3aStop(f"fetch 는 두 경로 ({sorted(FETCH_FILES)}) 만 — 요청 밖 {extra}")
    dest = Path(dest).resolve()
    if dest.exists():
        raise E3aStop(f"fetch 목적지가 이미 있다: {dest} — 새 폴더만")
    if mon.owned(dest, [REPO.resolve()]):
        raise E3aStop(f"fetch 목적지가 저장소 안이다: {dest}")
    dest.mkdir(parents=True)
    gd = dest / "git"
    env = dict(os.environ, GIT_ALLOW_PROTOCOL=allow_protocol, GIT_TERMINAL_PROMPT="0")
    rec = {"repo_url": str(repo_url), "commit": str(commit), "dest": str(dest), "cwd": str(dest), "allow_protocol": allow_protocol,
           "start_utc": _utc(), "steps": [], "files": {}}
    t = time.monotonic()

    def step(argv, stdout):
        s = {"argv": list(argv), "start_utc": _utc()}
        t1 = time.monotonic()
        r = run(argv, cwd=str(dest), env=env, stdout=stdout, stderr=subprocess.PIPE, timeout=timeout)
        s.update(rc=r.returncode, elapsed_s=round(time.monotonic() - t1, 3),
                 stderr=(r.stderr or b"").decode("utf-8", "replace")[-2000:])
        rec["steps"].append(s)
        if r.returncode != 0:
            raise _stop(f"git 단계 실패 (rc {r.returncode}): {' '.join(argv)} — {s['stderr'][-300:]}", rec)

    for argv in fetch_steps(gd, repo_url, commit):
        step(argv, subprocess.PIPE)
    for name, want in files.items():
        target = dest / name
        with open(target, "xb") as fo:
            step(show_argv(gd, commit, name), fo)
        b = target.read_bytes()
        rec["files"][name] = {"path": str(target), "sha256": _sha(b), "bytes": len(b), "expected": dict(want)}
        if _sha(b) != want["sha256"] or len(b) != want["bytes"]:
            raise _stop(f"fetch 대조 불일치 — {name}: sha256 {_sha(b)} · {len(b)} B ≠ 기대 {want}", rec)
    rec.update(end_utc=_utc(), elapsed_s=round(time.monotonic() - t, 3), ok=True)
    return rec


# ---------------------------------------------------------------- plan-e (E0 건조)
def _p0_record_problems(res) -> list:
    ext = res.get("extraction") or []
    ana = {e.get("row"): e for e in ext if e.get("kind") == "analysis"}
    refs = {e.get("sheet"): e for e in ext if e.get("kind") == "reference"}
    probs = []
    if set(ana) != set(e3a.ROWS) or any(e.get("status") != "OK" for e in ana.values()):
        probs.append("분석 기록 #0–#10 이 전부 OK 가 아니다")
    if set(refs) != set(p0.SHEETS_REF) or any(e.get("status") != "OK" for e in refs.values()):
        probs.append("reference 기록 둘이 OK 가 아니다")
    if not _finite((res.get("max_q") or {}).get("float")) or not _is_int((res.get("max_q") or {}).get("n_q_PE_hc")):
        probs.append("PE max_q / n_q_PE_hc 가 없다")
    if not _finite(res.get("q_NE_hc_max_record_only")):
        probs.append("NE q_NE_hc_max_record_only 가 없다")
    if (res.get("notebook_check") or {}).get("ok") is not True:
        probs.append("P0 의 노트북 대조가 ok 가 아니다")
    return probs


def plan_e(out, *, venv, seal, manifest_sha256, p0_result=P0_RESULT, excerpts=e3a.EXCERPTS, env_identity=None) -> dict:
    """E0 건조 — identity · 원천 sha · P0 · 발췌 · 계획 · 규칙 매개변수 · 기대 자료 식별 → `PLAN_E.json` 하나 (util import · 자료 · optimizer ·
    네트워크 0)."""
    out, seal = Path(out), Path(seal)
    e3a._guard([out, seal, p0_result, excerpts])
    if out.exists():
        raise E3aStop(f"{out} 가 이미 있다 — 덮어쓰지 않는다")
    t0 = time.monotonic()
    ident = e3a.identity(venv=venv, seal=seal, manifest_sha256=manifest_sha256, env_identity=env_identity)
    if not ident["ok"]:
        raise E3aStop(f"identity 실패: {ident['problems']}")
    files = {"P0_RESULT.json": Path(p0_result), "NOTEBOOK_SOURCE_EXCERPTS.json": Path(excerpts), "MANIFEST.json": seal / "MANIFEST.json",
             **_module_files()}
    table = identity_table(files, expected_identity(manifest_sha256))
    probs = identity_problems(table)
    if probs:
        raise E3aStop("식별 불일치 — " + "; ".join(probs))
    nb = e3a.notebook_case_table(excerpts)
    res = json.loads(Path(p0_result).read_bytes())
    probs = _p0_record_problems(res)
    if probs:
        raise E3aStop("P0 기록 — " + "; ".join(probs))
    calls = plan()
    by_worker: dict = {}
    for c in calls:
        by_worker[c["worker"]] = by_worker.get(c["worker"], 0) + c["algorithm"]["expected_evals"]
    doc = {
        "schema": "reil-c4e-plan-e-v1",
        "scope": "C4-E · E0 건조 (v3 §3 · 상태 문서 §66) — 계획 · 규칙 매개변수 · 기대 자료 식별만. util import · 자료 · optimizer · 네트워크 0",
        "util_imported": False, "data_opened": False, "optimizer_calls": 0, "objective_calls": 0, "network": 0,
        "identity": ident, "identity_table": table, "notebook": nb,
        "p0": {"path": str(p0_result), "sha256": table["P0_RESULT.json"]["sha256"], "max_q": res["max_q"]["float"],
               "n_q_PE_hc": res["max_q"]["n_q_PE_hc"], "q_NE_hc_max_record_only": res["q_NE_hc_max_record_only"],
               "references": [{k: e.get(k) for k in REF_KEYS} for e in res["extraction"] if e.get("kind") == "reference"],
               "analysis_rows": len([e for e in res["extraction"] if e.get("kind") == "analysis"])},
        "plan": calls, "n_calls": len(calls), "n_workers": N_WORKERS,
        "expected_evals_total": sum(c["algorithm"]["expected_evals"] for c in calls),
        "expected_evals_by_worker": {str(w): v for w, v in sorted(by_worker.items())},
        "optimizer_runs_total": sum(len(c["algorithm"]["seeds"]) for c in calls),
        "limits": LIMITS, "tick_s": TICK_S, "rule": StopRule(calls).params(), "cost_reason": COST_REASON,
        "expected_data": FETCH_FILES, "util_choice": "고정 커밋 원본 (v3 §11-3 · 상태 문서 §66)",
        "source": {"url": SOURCE_URL, "commit": SOURCE_COMMIT},
        "fetch_steps_template": fetch_steps("<dest>/git", SOURCE_URL, SOURCE_COMMIT)
        + [show_argv("<dest>/git", SOURCE_COMMIT, n) for n in FETCH_FILES],
        "record_files": list(RECORD_FILES), "required_fields": list(REQUIRED_FIELDS),
        "not_this_step": "E1 (fetch · run 66 호출) — E0 결과 검토 수용 뒤 별도 GO",
        "elapsed_s": time.monotonic() - t0,
    }
    data = mon._dump(doc)
    out.mkdir(parents=True)
    (out / "PLAN_E.json").write_bytes(data)
    if (out / "PLAN_E.json").read_bytes() != data:
        raise E3aStop("PLAN_E.json 을 다시 읽은 바이트가 쓴 것과 다르다")
    return {"ok": True, "out": str(out), "plan_e_sha256": _sha(data), "n_calls": len(calls), "optimizer_calls": 0,
            "util_imported": False, "identity_ok": True}


# ---------------------------------------------------------------- CLI
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="reil_c4e_run", description=(__doc__ or "").splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("plan-e", "run"):
        s = sub.add_parser(name)
        s.add_argument("--venv", required=True)
        s.add_argument("--seal", required=True, type=Path)
        s.add_argument("--seal-manifest-sha256", required=True)
        s.add_argument("--out", required=True, type=Path)
        if name == "run":
            s.add_argument("--xlsx", required=True, type=Path)
            s.add_argument("--util", required=True, type=Path)
            s.add_argument("--approval", required=True)
    f = sub.add_parser("fetch")
    f.add_argument("--dest", required=True, type=Path)
    a = ap.parse_args(argv)
    try:
        if a.cmd == "plan-e":
            summary = plan_e(a.out, venv=a.venv, seal=a.seal, manifest_sha256=a.seal_manifest_sha256)
        elif a.cmd == "fetch":
            summary = fetch(a.dest)
        else:
            for k in c5.BLAS_VARS:
                os.environ[k] = "1"
            res = run(a.out, venv=a.venv, seal=a.seal, manifest_sha256=a.seal_manifest_sha256, xlsx=a.xlsx, util_path=a.util,
                      approval=a.approval)
            summary = {"ok": res["final"]["complete"], **res}
    except E3aStop as e:
        print(json.dumps(c5._jsonable({"ok": False, "stop": str(e), "record": getattr(e, "record", None)}), ensure_ascii=False,
                         sort_keys=True))
        return 3
    print(json.dumps(c5._jsonable(summary), ensure_ascii=False, sort_keys=True))
    return 0 if summary.get("ok") else 2


if __name__ == "__main__":
    sys.exit(main())
