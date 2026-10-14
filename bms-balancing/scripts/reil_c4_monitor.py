"""REIL C4 감시 · 기록 (C4 v2 §4-4 · 사전 검토 C4-N2 · C4-N3 보완 · 상태 문서 §39 C4-0a).

C5 의 `reil_c5_pilot.orchestrate` · `disk_sample` · `split_dirty` 는 **고치지 않는다** (실행된 증거). C4 실행기는 이 모듈을 쓴다. 고친 것 셋:

1. **공백 검사** (C4-N2) — 표본이 *도착한* 시각으로, 성공 여부와 무관하게 마지막 유효 표본 (없으면 감시 시작) 과의 간격을 본 뒤에야 마지막
   유효 시각을 갱신한다. 늦게 도착한 성공 표본도 공백을 덮지 못한다. None · 예외 · 첫 표본 지연을 따로 적는다. 예외는 기다리지 않는다.
2. **마감** (C4-N2) — 표본 수집 뒤 현재 시각으로 마감을 다시 본다. 작업자도 절대 마감 시각을 받아 **마감 뒤에는 새 작업을 시작하지 않는다**.
3. **산출량 · 소유 경로** (C4-N3) — 본체 · 래퍼 · 임시 · 최종 기록의 소유 루트를 미리 열거해 합산한다 (겹친 루트는 한 번). 최종 쓰기 뒤에 같은
   루트 집합으로 다시 잰다. 경로는 정확 일치 또는 구분자 뒤 하위 경로만 소유로 본다. Git 원문은 분류와 따로 남기고, 따옴표 · 이름 바꿈처럼
   모호한 줄은 소유로 보지 않는다.

C4-0a 결과 검토 (2026-10-13) 의 한정 보완 셋:

- **N2** — 최종 기록은 마지막 쓰기 · 재읽기 · 해시 · 용량 조회 **뒤** snapshot 하나로 시간 한도를 판정하고 그 값을 그대로 반환한다. 넘으면
  파일 · 해시는 보존하고 미완 (`RECORD_INCOMPLETE`) 이다.
- **N3** — 느릴 수 있는 조회 (RSS · 디스크) 뒤와 정상 종료 직전에 두 감시기의 freshness 를 확인한다 (`Watch.stale`). 확인은 표본이 아니라서
  마지막 유효 시각을 바꾸지 않는다.
- **N4** — 구조 오류의 `partial` (이미 모은 계수) 을 작업자 경계 너머 부모까지 보낸다. 그 작업은 여전히 중단 (`STARTED_INTERRUPTED`) 이다.

C4-E (v3 §3 · 상태 문서 §66) 의 선택 인자 하나:

- **`stop_rule`** — 기본값 None 이면 지금과 같은 동작이다. 주면 매 tick (RSS 표본 · freshness 확인 뒤) 에 `rule_snapshot` 으로 부른다
  (원점 t0 의 상대 시각 · 작업자 start 사건 · 완료 행의 wall / n_eval / termination · progress · 계획 — X · F · G 없음). 문자열이면 전역
  중지 사유 · 예외 · 형식 오류는 우리 구조 오류 (사유 원문 · `apply_rule`). 규칙은 상태를 바꾸지 않는다 (done 우선 분류 그대로).

OS 조회가 영구히 막히는 경우의 강제 종료나 OS 하드 한도를 증명하지 않는다 (C4 v2 §4-4).
"""
from __future__ import annotations

import hashlib
import json
import os
import queue
import shutil
import time
from pathlib import Path


class Structural(Exception):
    """구조 오류 — 전역 중단 (행을 만들지 않는다)."""

    def __init__(self, info, partial=None):
        super().__init__(info.get("message") if isinstance(info, dict) else info)
        self.info, self.partial = info, partial


# ---------------------------------------------------------------- (1) 공백 검사
class Watch:
    """표본 하나마다 `observe(t_before, value, t_after, error)` — 멈춰야 하면 이유 문자열, 아니면 None."""

    def __init__(self, name: str, gap_limit: float, t_start: float):
        self.name, self.gap_limit = name, float(gap_limit)
        self.last_valid = float(t_start)
        self.has_valid = False
        self.samples: list = []

    def observe(self, t_before: float, value, t_after: float, error: str | None = None):
        gap = t_after - self.last_valid
        self.samples.append({"t_before": t_before, "t_after": t_after, "latency": t_after - t_before,
                             "value": value, "error": error, "gap_since_valid": gap})
        if error is not None:
            return f"{self.name} 감시 실패 (표본 예외): {error}"
        if gap > self.gap_limit:
            if not self.has_valid:
                kind = "첫 표본 지연"
            elif value is None:
                kind = "표본 없음"
            else:
                kind = "늦은 성공 표본"
            return f"{self.name} {kind} — 마지막 유효 표본 뒤 {gap:.2f} s > {self.gap_limit} s"
        if value is not None:
            self.last_valid, self.has_valid = t_after, True
        return None

    def stale(self, now: float):
        """확인만 (C4-0A-N3) — 지금 시각에서 마지막 유효 표본 (없으면 감시 시작) 까지의 공백이 한도를 넘었으면 이유, 아니면 None.
        표본이 아니므로 `last_valid` · `samples` 를 바꾸지 않는다."""
        gap = now - self.last_valid
        if gap > self.gap_limit:
            return f"{self.name} 공백 (확인 · 표본 아님) — 마지막 유효 표본 뒤 {gap:.2f} s > {self.gap_limit} s"
        return None


# ---------------------------------------------------------------- (3) 소유 경로 · 산출량
def _norm(p) -> str:
    s = str(p).replace("\\", "/")
    while s.endswith("/") and len(s) > 1:
        s = s[:-1]
    return s


def owned(path, roots) -> bool:
    p = _norm(path)
    return any(p == r or p.startswith(r + "/") for r in (_norm(x) for x in roots))


def split_dirty(porcelain: str, roots) -> dict:
    """`git status --porcelain=v1` 줄을 소유 산출 · 그 밖 · 모호로 — 원문은 `raw` 에 그대로."""
    own, other, amb = [], [], []
    for ln in porcelain.splitlines():
        if not ln.strip():
            continue
        path = ln[3:]
        if path.startswith('"') or " -> " in path:
            amb.append(ln)
        elif owned(path, roots):
            own.append(ln)
        else:
            other.append(ln)
    return {"own_output": own, "other": other, "ambiguous": amb, "raw": porcelain}


def output_bytes(roots) -> int:
    real = []
    for r in roots:
        p = Path(r)
        if p.exists():
            real.append(p.resolve())
    keep = [p for p in real if not any(q != p and q in p.parents for q in real)]
    total, seen = 0, set()
    for root in sorted(set(keep)):
        for f in ([root] if root.is_file() else root.rglob("*")):
            if f.is_file() and f not in seen:
                seen.add(f)
                total += f.stat().st_size
    return total


def disk_sample(roots, free_path) -> tuple:
    return output_bytes(roots), shutil.disk_usage(str(free_path)).free


def rss_bytes(pids) -> int:
    """부모 + 작업자 VmRSS 합 (표본 · `reil_c5_pilot.rss_bytes` 와 같은 식 — 그 모듈을 import 하지 않으려고 값으로 둔다)."""
    tot = 0
    for pid in pids:
        try:
            txt = Path(f"/proc/{pid}/status").read_text()
        except FileNotFoundError:
            continue
        for ln in txt.splitlines():
            if ln.startswith("VmRSS:"):
                tot += int(ln.split()[1]) * 1024
    return tot


# ---------------------------------------------------------------- 작업자 · 조정
def _jsonable(o):
    try:
        json.dumps(o)
        return o
    except TypeError:
        if isinstance(o, dict):
            return {str(k): _jsonable(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [_jsonable(v) for v in o]
        if hasattr(o, "tolist"):
            return o.tolist()
        return repr(o)


def worker_loop(wid, tasks, ctx, task_fn, q, stop, prog, deadline_abs: float, clock=time.monotonic):
    """작업자 — 작업을 시작하기 **직전마다** 정지 신호와 절대 마감을 본다 (마감 뒤 신규 시작 없음)."""
    try:
        q.put(("worker_start", wid, {"pid": os.getpid(), "t": clock()}))
        for task in tasks:
            if stop.is_set():
                break
            if clock() >= deadline_abs:
                q.put(("worker_deadline", wid, {"t": clock(), "next_task": task["task_id"]}))
                break
            tid = task["task_id"]
            q.put(("start", tid, {"worker": wid, "t": clock()}))

            def progress(n, tid=tid):
                prog[tid] = n

            def notify(kind, payload, tid=tid):
                q.put((kind, tid, _jsonable({**payload, "t": clock()})))
            try:
                row = task_fn(task, ctx, notify=notify, progress=progress)
            except Structural as s:                       # partial (이미 모은 계수) 도 부모까지 보낸다 (C4-0A-N4) — 완료 행으로 바꾸지 않는다
                q.put(("structural", tid, {**(s.info if isinstance(s.info, dict) else {"message": str(s.info)}),
                                           "partial": _jsonable(s.partial), "t": clock()}))
                return
            q.put(("done", tid, _jsonable(row)))
        q.put(("worker_end", wid, {"t": clock()}))
    except BaseException as e:  # noqa: BLE001 — 작업자 자체의 예외 = 우리 코드 = 구조 오류
        q.put(("structural", None, {"kind": "structural", "origin": "worker", "type": type(e).__name__,
                                    "message": str(e)[:300], "t": clock()}))


def _states(tasks, ev, prog, reason, t_stop, t0) -> list:
    partial = {s.get("task_id"): s["partial"] for s in ev.get("structural", []) if s.get("partial") is not None}
    out = []
    for task in tasks:
        tid = task["task_id"]
        st = ev["started"].get(tid)
        rel = (st["t"] - t0) if st else None
        if tid in ev["done"]:
            out.append({**ev["done"][tid], "task_id": tid, "state": "COMPLETED", "t_start_rel": rel})
        elif st:
            row = {"task_id": tid, "worker": task.get("worker"), "state": "STARTED_INTERRUPTED", "t_start_rel": rel,
                   "n_eval_observed": f"≥ {int(prog.get(tid, 0) if isinstance(prog, dict) else prog[tid])} · 미확인",
                   "elapsed_s": t_stop - st["t"], "interrupt_reason": reason}
            if tid in partial:
                row["structural_partial"] = partial[tid]        # 구조 오류 직전까지의 계수 — 상태는 중단 그대로
            out.append(row)
        else:
            out.append({"task_id": tid, "worker": task.get("worker"), "state": "NOT_STARTED", "t_start_rel": None,
                        "interrupt_reason": reason or "작업자가 끝난 뒤 남은 작업"})
    return out


def rule_snapshot(tasks, ev, prog, now_rel: float, t0: float) -> dict:
    """규칙 입력 (C4-E v3 §3 의 좌표 계약) — 원점 t0 의 상대 시각 · 작업자 start 사건 t − t0 · 완료 행의 wall / n_eval / termination 만."""
    return {"now_rel": now_rel,
            "started": {tid: s["t"] - t0 for tid, s in ev["started"].items()},
            "done": {tid: {k: d.get(k) for k in ("wall", "n_eval", "termination")} for tid, d in ev["done"].items()},
            "progress": {t["task_id"]: int(prog[t["task_id"]]) for t in tasks},
            "planned": [t["task_id"] for t in tasks]}


def apply_rule(stop_rule, snap, ev, clock=time.monotonic):
    """규칙 한 번 — 문자열이면 전역 중지 사유 · None 이면 계속. 예외 · 형식 오류는 우리 구조 오류로 기록하고 그 사유를 돌려준다."""
    try:
        r = stop_rule(snap)
        if r is not None and not isinstance(r, str):
            raise TypeError(f"stop_rule 반환 {type(r).__name__} — 문자열 또는 None 이어야 한다")
        return r
    except Exception as e:  # noqa: BLE001 — 규칙의 예외 = 우리 코드 = 구조 오류
        ev["structural"].append({"task_id": None, "kind": "structural", "origin": "ours", "stage": "stop_rule",
                                 "type": type(e).__name__, "message": str(e)[:300], "t": clock()})
        return f"구조 오류: {type(e).__name__} (ours · stop_rule) {e}"[:400]


def supervise(tasks, ctx, task_fn, *, n_workers, limits, t0, clock=time.monotonic, rss_fn=None, disk_fn=None,
              out_roots=(), free_path=".", tick=1.0, disk_every=5.0, stop_rule=None) -> dict:
    """작업 → 작업자 배정은 `task["worker"]` 로 고정. 표본 감시 (Watch) · 마감 · 전역 중단 → 소유 작업자만 종료.
    `stop_rule` (C4-E) 은 매 tick RSS 표본 · freshness 확인 뒤에 부른다 — 기본값 None 이면 부르지 않는다."""
    import multiprocessing as mp
    mpc = mp.get_context("fork")
    q, stop = mpc.Queue(), mpc.Event()
    shared_prog = mpc.Array("q", (max(t["task_id"] for t in tasks) + 1) if tasks else 1, lock=False)
    deadline_abs = t0 + float(limits["measure"])
    rss_fn = rss_fn or rss_bytes
    disk_fn = disk_fn or (lambda roots: disk_sample(roots, free_path))
    ev = {"started": {}, "done": {}, "worker_start": {}, "worker_end": {}, "worker_deadline": {}, "structural": []}
    rss_w = Watch("메모리", limits["rss_gap"], clock() - t0)      # 표본 시각은 원점 기준 상대값
    disk_w = Watch("디스크", limits["disk_gap"], clock() - t0)
    reason = None

    def fresh(now):
        """두 감시기 freshness 확인 (C4-0A-N3) — 확인만 · 유효 시각을 바꾸지 않는다."""
        return rss_w.stale(now) or disk_w.stale(now)

    def handle(msg):
        kind, key, payload = msg
        if kind in ("start", "done", "worker_start", "worker_end", "worker_deadline"):
            ev["started" if kind == "start" else kind][key] = payload
        elif kind == "structural":
            ev["structural"].append({"task_id": key, **payload})

    def drain(timeout=0.05):
        while True:
            try:
                handle(q.get(timeout=timeout))
            except queue.Empty:
                return True
            except Exception:  # noqa: BLE001 — 강제 종료 뒤 깨진 메시지 → 기록 미완
                return False

    procs = {w: mpc.Process(target=worker_loop, args=(w, [t for t in tasks if t["worker"] == w], ctx, task_fn, q, stop,
                                                       shared_prog, deadline_abs), daemon=True) for w in range(n_workers)}
    if clock() >= deadline_abs:
        reason = f"단계 경계 — 측정 마감 ({limits['measure']} s) 전에 시작하지 못했다"
    else:
        for p in procs.values():
            p.start()
    last_disk_try = -1e18
    while reason is None:
        try:
            handle(q.get(timeout=tick))
        except queue.Empty:
            pass
        if ev["structural"]:
            s = ev["structural"][0]
            reason = f"구조 오류: {s.get('type')} ({s.get('origin')} · {s.get('stage')}) {s.get('message')}"[:400]
            break
        if clock() >= deadline_abs:
            reason = f"단계 경계 — 측정 마감 {limits['measure']} s · 신규 시작 중지 · 진행 중 작업 중단"
            break
        dead = [w for w, p in procs.items() if p.exitcode is not None and w not in ev["worker_end"]
                and w not in ev["worker_deadline"]]
        if dead:
            drain()
            dead = [w for w in dead if w not in ev["worker_end"] and w not in ev["worker_deadline"]]
            if ev["structural"] or dead:
                if dead and not ev["structural"]:
                    reason = f"작업자 {dead[0]} 비정상 종료 (exitcode {procs[dead[0]].exitcode}) — 종료 메시지 없음"
                continue
        tb = clock()
        try:
            v, err = rss_fn([os.getpid()] + [p.pid for p in procs.values() if p.is_alive()]), None
        except Exception as e:  # noqa: BLE001
            v, err = None, f"{type(e).__name__}: {e}"
        ta = clock()
        reason = rss_w.observe(tb - t0, v, ta - t0, err)
        if reason is None and v is not None and v > limits["rss"]:
            reason = f"메모리 표본 {v} B > 상한 {limits['rss']} B"
        if reason is None and clock() >= deadline_abs:               # 표본 수집 뒤 마감 재검사
            reason = f"단계 경계 — 측정 마감 {limits['measure']} s (표본 수집 뒤 재검사) · 신규 시작 중지"
        if reason is None:
            reason = fresh(clock() - t0)                              # 느린 RSS 조회 뒤 — 디스크 감시기 freshness (C4-0A-N3)
        if reason is None and stop_rule is not None:                  # C4-E: 규칙 (호출당 상한 · 비용) — 사유면 전역 중지
            reason = apply_rule(stop_rule, rule_snapshot(tasks, ev, shared_prog, clock() - t0, t0), ev, clock)
        if reason is not None:
            break
        if ta - last_disk_try >= disk_every:
            last_disk_try = ta
            tb = clock()
            try:
                d, err = disk_fn(list(out_roots)), None
            except Exception as e:  # noqa: BLE001
                d, err = None, f"{type(e).__name__}: {e}"
            ta = clock()
            reason = disk_w.observe(tb - t0, d, ta - t0, err)
            if reason is None and d is not None and (d[0] > limits["disk_new"] or d[1] < limits["disk_free"]):
                reason = f"디스크 표본: 새 산출 {d[0]} B (상한 {limits['disk_new']}) · 여유 {d[1]} B (하한 {limits['disk_free']})"
            if reason is None and clock() >= deadline_abs:
                reason = f"단계 경계 — 측정 마감 {limits['measure']} s (디스크 표본 뒤 재검사) · 신규 시작 중지"
            if reason is None:
                reason = fresh(clock() - t0)                          # 느린 디스크 조회 뒤 — RSS 감시기 freshness (C4-0A-N3)
            if reason is not None:
                break
        if len(set(ev["worker_end"]) | set(ev["worker_deadline"])) == n_workers:   # 마감을 본 작업자는 둘 다 보낸다 — 합집합으로 센다
            drain()
            if ev["worker_deadline"] and any(t["task_id"] not in ev["started"] for t in tasks):
                reason = f"단계 경계 — 작업자가 마감 ({limits['measure']} s) 을 보고 신규 시작을 멈췄다"
            if reason is None:
                reason = fresh(clock() - t0)                          # 정상 종료 직전 — 두 감시기 freshness (C4-0A-N3)
            break
    t_stop = clock()
    if reason is not None:
        stop.set()
        for p in procs.values():
            if p.is_alive():
                p.terminate()
        deadline = time.monotonic() + limits["grace"]
        for p in procs.values():
            if p.pid is not None:
                p.join(max(0.0, deadline - time.monotonic()))
        for p in procs.values():
            if p.is_alive():
                p.kill()
                p.join(5)
    else:
        for p in procs.values():
            p.join(limits["grace"])
    drained_ok = drain(0.1)
    prog = {t["task_id"]: int(shared_prog[t["task_id"]]) for t in tasks}
    alive_after = sum(1 for p in procs.values() if p.is_alive())
    return {"states": _states(tasks, ev, prog, reason, t_stop, t0), "global_stop": reason,
            "samples": {"rss": rss_w.samples, "disk": disk_w.samples}, "workers": ev["worker_start"],
            "worker_end": ev["worker_end"], "worker_deadline": ev["worker_deadline"], "structural": ev["structural"],
            "owned_alive_after": alive_after, "drain_ok": drained_ok, "t_stop": t_stop - t0, "deadline_rel": deadline_abs - t0,
            "exitcodes": {w: p.exitcode for w, p in procs.items()}}


# ---------------------------------------------------------------- (3) 최종 기록 — 쓰기 뒤 같은 루트로 다시 잰다
def _dump(obj) -> bytes:
    return (json.dumps(_jsonable(obj), ensure_ascii=False, sort_keys=True, indent=1) + "\n").encode("utf-8")


def final_record(out_dir, parts: dict, *, roots, limit_bytes, clock=time.monotonic, t0=0.0, limit_s=float("inf")) -> dict:
    out_dir = Path(out_dir)
    state, files, problems = "COMPLETE", {}, []
    for name, obj in parts.items():
        if clock() - t0 > limit_s:
            state = "RECORD_INCOMPLETE"
            problems.append(f"최종 기록 단계 경계 {limit_s} s 초과 — {name} 부터 쓰지 않았다")
            break
        data = _dump(obj)
        try:
            (out_dir / name).write_bytes(data)
            back = (out_dir / name).read_bytes()
        except OSError as e:
            state = "RECORD_INCOMPLETE"
            problems.append(f"{name} 쓰기 실패: {type(e).__name__}: {e}")
            break
        if back != data:
            state = "RECORD_INCOMPLETE"
            problems.append(f"{name} 다시 읽은 바이트가 다르다")
            break
        files[name] = hashlib.sha256(back).hexdigest()
    after = output_bytes(roots)
    snap = clock() - t0       # 마지막 쓰기 · 재읽기 · 해시 · 용량 조회 뒤 snapshot 하나 — 시간 판정과 반환에 같은 값 (C4-0A-N2)
    violations = []
    if snap > limit_s:
        violations.append("time")
        problems.append(f"최종 snapshot {snap:.3f} s > 기록 한도 {limit_s} s — 파일 · 해시는 보존하고 미완으로 둔다")
        if state == "COMPLETE":
            state = "RECORD_INCOMPLETE"
    if after > limit_bytes:
        violations.append("size")
        problems.append(f"최종 쓰기 뒤 산출 {after} B > 상한 {limit_bytes} B — 성공으로 종결하지 않는다")
        if state == "COMPLETE":
            state = "OUTPUT_LIMIT_EXCEEDED"
    return {"record_state": state, "files": files, "problems": problems, "output_bytes_after": after,
            "output_roots": [str(r) for r in roots], "final_snapshot_s": snap, "limit_violations": violations}
