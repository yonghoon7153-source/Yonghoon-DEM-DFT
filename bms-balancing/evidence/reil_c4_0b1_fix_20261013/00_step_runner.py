"""REIL C4-0b1 한정 보완 (N1–N3 · A1 · 상태 §49) 단계 실행기 — 명령 하나를 timeout 안에서 부르고 meta · stdout · stderr · porcelain 시작/끝을 증거 폴더에 쓴다 (stdlib).

    /usr/bin/python3.11 -I step.py <이름> <timeout_s> -- <argv…>

cwd 는 bms-balancing/. 자식 env 에서 비밀 형태 변수를 뺀다 (이름만 기록 · C4-ENV 와 같은 위생). 재시도 없음.
"""
import datetime
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

REPO = Path("/home/user/Yonghoon-DEM-DFT")
BMS = REPO / "bms-balancing"
E = BMS / "evidence" / "reil_c4_0b1_fix_20261013"
SP = Path("/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/b881d255-9513-5adc-9b14-3c0be18d7ad6/scratchpad")
SECRET = re.compile(r"TOKEN|SECRET|PASSW|ACCESS_KEY|CREDENTIAL|COOKIE|^GIT_CONFIG_", re.I)
EXTRA = {"PYTHONDONTWRITEBYTECODE": "1", "MPLBACKEND": "Agg", "MPLCONFIGDIR": str(SP / "c4_0b1_fix" / "mpl"),
         "TMPDIR": str(SP / "c4_0b1_fix" / "tmp"), "OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1"}


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def porcelain():
    return subprocess.run(["git", "-C", str(REPO), "status", "--porcelain=v1", "--untracked-files=all"],
                          capture_output=True, text=True, timeout=60).stdout


def main():
    name, timeout = sys.argv[1], float(sys.argv[2])
    assert sys.argv[3] == "--"
    argv = sys.argv[4:]
    for k in ("MPLCONFIGDIR", "TMPDIR"):
        Path(EXTRA[k]).mkdir(parents=True, exist_ok=True)
    for suffix in (".meta.json", ".stdout.log", ".stderr.log"):
        if (E / f"{name}{suffix}").exists():
            raise SystemExit(f"{name}{suffix} 가 이미 있다 — 덮어쓰지 않는다")
    env = {k: v for k, v in os.environ.items() if not SECRET.search(k)}
    env.update(EXTRA)
    env.update({"REIL_C4_0B1_FIX_EVIDENCE": str(E), "REIL_C4_0B1_FIX_STEP": name})   # 기록용 시험 (out) 이 outcome 을 쓸 위치
    (E / f"{name}.porcelain_start.txt").write_text(porcelain(), encoding="utf-8")
    head0 = subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    meta = {"step": name, "argv": argv, "cwd": str(BMS), "env_set": {**EXTRA, "REIL_C4_0B1_FIX_EVIDENCE": str(E), "REIL_C4_0B1_FIX_STEP": name}, "env_removed_names": sorted(k for k in os.environ if SECRET.search(k)),
            "timeout_s": timeout, "start_utc": utc(), "head_start": head0}
    t = time.monotonic()
    rc, timed_out = None, False
    with open(E / f"{name}.stdout.log", "wb") as fo, open(E / f"{name}.stderr.log", "wb") as fe:
        try:
            rc = subprocess.run(argv, cwd=str(BMS), env=env, stdout=fo, stderr=fe, timeout=timeout).returncode
        except subprocess.TimeoutExpired:
            timed_out = True
    meta.update({"end_utc": utc(), "elapsed_s": round(time.monotonic() - t, 3), "rc": rc, "timed_out": timed_out,
                 "head_end": subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()})
    (E / f"{name}.porcelain_end.txt").write_text(porcelain(), encoding="utf-8")
    (E / f"{name}.meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: meta[k] for k in ("step", "rc", "timed_out", "elapsed_s", "start_utc", "end_utc")}, ensure_ascii=False))
    return 0 if (rc == 0 and not timed_out) else 1


if __name__ == "__main__":
    sys.exit(main())
