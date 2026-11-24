"""REIL C4-ENV 새 세대 재봉인 — 바깥 하네스. 실행기 (`reil_c4_env_reseal_run.py`) 를 정확한 argv · cwd 로 **한 번** 부르고, 절대 시간
상한에서 프로세스 그룹째 끊고, 바깥 반환 (stdout · stderr 원문 · rc · 시각) 을 저장소 **밖**에 남긴다. 이 파일은 저장소에 쓰지 않는다.

  /usr/bin/python3.11 -I bms-balancing/scripts/reil_c4_env_reseal_harness.py precheck   → SP/c4env18_outer/precheck/
  /usr/bin/python3.11 -I bms-balancing/scripts/reil_c4_env_reseal_harness.py run        → SP/c4env18_outer/run/

- 절대 반환 보장 (검토 §137: subprocess timeout 과 전체의 절대 반환을 구분): precheck 90 s (실행기 자신의 한도 60 s + 30) · run 1,860 s
  (전체 1,800 s + 60). 상한에 닿으면 TERM → 10 s → KILL (그룹째) · `killed_at_limit` 을 적는다 · rc 124.
- 출력 폴더가 이미 있으면 시작하지 않는다 (덮어쓰기 · 재시도 없음). 실행기에는 하네스의 env 를 그대로 넘긴다 (이름만 기록 · 자식 env 정리는
  실행기가 한다). 실행기 argv = `/usr/bin/python3.11 -I -B <실행기> <precheck|run>` (-B — 저장소 안 pyc 쓰기 0).
- `outer_return.json` 은 실행기가 끝난 **뒤**에 쓴다. 이 파일 자신의 쓰기 · 하네스를 부른 쪽의 반환은 증명하지 않는다 (그것은 부른 쪽의 기록).
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path


def production() -> dict:
    sp = Path("/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/b881d255-9513-5adc-9b14-3c0be18d7ad6/scratchpad")
    return {"repo": Path(__file__).resolve().parents[2], "py": "/usr/bin/python3.11",
            "runner_rel": "bms-balancing/scripts/reil_c4_env_reseal_run.py", "outer": sp / "c4env18_outer",
            "limits": {"precheck": 90.0, "run": 1860.0}, "grace": 10.0}


def utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def kill_group(p: subprocess.Popen, grace: float) -> None:
    for sig, wait in ((signal.SIGTERM, grace), (signal.SIGKILL, grace)):
        try:
            os.killpg(p.pid, sig)
        except ProcessLookupError:
            break
        end = time.monotonic() + wait
        while time.monotonic() < end:
            p.poll()
            try:
                os.killpg(p.pid, 0)
            except ProcessLookupError:
                break
            time.sleep(0.05)
        else:
            continue
        break
    if p.poll() is None:
        p.wait()


def main(argv=None, cfg=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv not in (["precheck"], ["run"]):
        print(__doc__, file=sys.stderr)
        return 2
    cfg = cfg or production()
    mode = argv[0]
    out = cfg["outer"] / mode
    if out.exists():
        print(f"이미 있다 — 시작하지 않는다 (덮어쓰기 · 재시도 없음): {out}", file=sys.stderr)
        return 2
    out.mkdir(parents=True)
    runner = cfg["repo"] / cfg["runner_rel"]
    cmd = [cfg["py"], "-I", "-B", str(runner), mode]     # -B: 저장소 안에 pyc 를 쓰지 않는다 (샌드박스 시험이 잡은 것)
    rec = {"kind": "C4ENV_RESEAL_OUTER_RETURN", "mode": mode, "argv": cmd, "cwd": str(cfg["repo"]), "env_names": sorted(os.environ),
           "limit_s": cfg["limits"][mode], "grace_s": cfg["grace"], "harness_sha256": sha(Path(__file__)),
           "runner_sha256_at_launch": sha(runner), "start_utc": utc()}
    t = time.monotonic()
    with open(out / "stdout.log", "xb") as fo, open(out / "stderr.log", "xb") as fe:
        p = subprocess.Popen(cmd, cwd=str(cfg["repo"]), stdout=fo, stderr=fe, start_new_session=True)
        killed = False
        try:
            p.wait(timeout=cfg["limits"][mode])
        except subprocess.TimeoutExpired:
            killed = True
            kill_group(p, cfg["grace"])
    rec.update({"end_utc": utc(), "elapsed_s": round(time.monotonic() - t, 3), "rc": p.returncode, "killed_at_limit": killed,
                "stdout": {"bytes": (out / "stdout.log").stat().st_size, "sha256": sha(out / "stdout.log")},
                "stderr": {"bytes": (out / "stderr.log").stat().st_size, "sha256": sha(out / "stderr.log")}})
    with open(out / "outer_return.json", "x", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False, sort_keys=True, indent=1) + "\n")
    print(f"harness {mode}: rc={p.returncode} killed_at_limit={killed} elapsed={rec['elapsed_s']}s → {out}", flush=True)
    if killed:
        return 124
    return p.returncode if p.returncode is not None else 1


if __name__ == "__main__":
    sys.exit(main())
