"""C1 메모리 경비 (§8-11 ③ — 규칙 7 같은 자원 중단 · 과학 규칙 아님). 진단 전용.

watch: 0.2 s 마다 /proc 를 읽어 뿌리 프로세스와 그 자손 전체의 VmRSS 합 (감시자 자신 제외) 을 잰다. 합이 상한 (기본 12 × 10⁹ B) 을 넘으면
trip 기록 → 뿌리의 자손 (뿌리 · 감시자 제외) 을 SIGKILL → rc 5 로 끝난다. SIGTERM 을 받으면 최대값 요약을 쓰고 끝난다.

사용: python -I c1_memguard.py watch --root PID --log FILE.jsonl --trip FILE.json [--cap-bytes N] [--interval S]
"""
from __future__ import annotations

import argparse
import json
import os
import resource
import signal
import sys
import time

CAP_BYTES = 12_000_000_000


def read_proc_table() -> dict:
    """{pid: (ppid, rss_bytes)} — /proc/<pid>/stat (4 번째 필드 ppid) · /proc/<pid>/status (VmRSS kB)."""
    table = {}
    for d in os.listdir("/proc"):
        if not d.isdigit():
            continue
        try:
            with open(f"/proc/{d}/stat") as fh:
                st = fh.read()
            ppid = int(st[st.rindex(")") + 2:].split()[1])
            rss = 0
            with open(f"/proc/{d}/status") as fh:
                for line in fh:
                    if line.startswith("VmRSS:"):
                        rss = int(line.split()[1]) * 1024
                        break
            table[int(d)] = (ppid, rss)
        except (OSError, ValueError, IndexError):
            continue
    return table


def _descendants(root: int, table: dict) -> list:
    kids = {}
    for pid, (ppid, _) in table.items():
        kids.setdefault(ppid, []).append(pid)
    out, stack = [], [root]
    while stack:
        p = stack.pop()
        for c in kids.get(p, []):
            out.append(c)
            stack.append(c)
    return out


def tree_rss(root: int, table: dict, exclude=()) -> int:
    """뿌리 + 자손의 RSS 합 (exclude 제외)."""
    pids = [root] + _descendants(root, table)
    return int(sum(table[p][1] for p in pids if p in table and p not in exclude))


def kill_targets(root: int, table: dict, exclude=()) -> list:
    """죽일 대상 = 뿌리의 자손 (뿌리 · exclude 제외)."""
    return [p for p in _descendants(root, table) if p not in exclude and p != root]


class Watcher:
    def __init__(self, cap_bytes: int = CAP_BYTES):
        self.cap = int(cap_bytes)
        self.peak = 0
        self.tripped = False
        self.trip_value = None

    def observe(self, total: int) -> bool:
        """표본 하나 → 이번에 처음 상한을 넘었으면 True."""
        self.peak = max(self.peak, int(total))
        if not self.tripped and total > self.cap:
            self.tripped = True
            self.trip_value = int(total)
            return True
        return False


def write_rusage(path: str) -> dict:
    """단계 끝의 교차 확인: ru_maxrss (자기 · 자식) [B] — Linux 는 kB 로 준다."""
    me = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024
    ch = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss * 1024
    rec = {"ru_maxrss_self_B": me, "ru_maxrss_children_B": ch, "cap_B": CAP_BYTES,
           "exceeded": bool(max(me, ch) > CAP_BYTES), "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    try:
        with open(path, "w") as fh:
            json.dump(rec, fh)
    except OSError:
        pass
    return rec


def rusage_exit_hook():
    """Python 단계 main 에서 부른다: C1_RUN · C1_STEP 이 있으면 <C1_RUN>/<C1_STEP>.rusage.json · 상한 초과면 rc 5."""
    run, step = os.environ.get("C1_RUN"), os.environ.get("C1_STEP")
    if not (run and step):
        return None
    rec = write_rusage(os.path.join(run, f"{step}.rusage.json"))
    if rec["exceeded"]:
        print(f"MEMORY CAP (ru_maxrss) exceeded: {rec}", flush=True)
        return 5
    return None


def watch(root: int, log: str, trip: str, cap: int, interval: float) -> int:
    me = os.getpid()
    w = Watcher(cap)
    stop = {"flag": False}

    def _term(signum, frame):
        stop["flag"] = True
    signal.signal(signal.SIGTERM, _term)
    t0 = time.time()
    last_log = 0.0
    n = 0
    with open(log, "a") as lf:
        while not stop["flag"]:
            table = read_proc_table()
            if root not in table:
                break
            total = tree_rss(root, table, exclude=(me,))
            n += 1
            if w.observe(total):
                top = sorted(((table[p][1], p) for p in [root] + _descendants(root, table) if p in table and p != me),
                             reverse=True)[:5]
                targets = kill_targets(root, table, exclude=(me,))
                rec = {"tripped": True, "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "total_B": total,
                       "cap_B": cap, "top": top, "killed": targets}
                with open(trip, "w") as tf:
                    json.dump(rec, tf)
                for p in targets:
                    try:
                        os.kill(p, signal.SIGKILL)
                    except OSError:
                        pass
                lf.write(json.dumps({"t": round(time.time() - t0, 2), "total_B": total, "event": "TRIP"}) + "\n")
                lf.flush()
                break
            if time.time() - last_log >= 5.0:
                lf.write(json.dumps({"t": round(time.time() - t0, 2), "total_B": total}) + "\n")
                lf.flush()
                last_log = time.time()
            time.sleep(interval)
        lf.write(json.dumps({"summary": True, "peak_B": w.peak, "n_samples": n, "duration_s": round(time.time() - t0, 2),
                             "tripped": w.tripped, "cap_B": cap, "interval_s": interval}) + "\n")
    return 5 if w.tripped else 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["watch"])
    ap.add_argument("--root", type=int, required=True)
    ap.add_argument("--log", required=True)
    ap.add_argument("--trip", required=True)
    ap.add_argument("--cap-bytes", type=int, default=CAP_BYTES)
    ap.add_argument("--interval", type=float, default=0.2)
    a = ap.parse_args(argv)
    return watch(a.root, a.log, a.trip, a.cap_bytes, a.interval)


if __name__ == "__main__":
    sys.exit(main())
