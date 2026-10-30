"""REIL C4-E · E1-0b 끝 기록 03_end.json (승인 요청 `docs/REIL_C4E_E1_0B_APPROVAL_REQUEST_20261030.md` §4-5) — stdlib 한 번 · 실행 전에 고정한 바이트.

    /usr/bin/python3.11 -I <E>/00_end_writer.py <E> '<단계 e 의 절차 Git 이름 확인 JSON>'

읽기 = 단계 둘의 meta · 단계 둘의 외곽 반환 (`<단계>.outer_rc.txt` — 셸이 실행기 반환을 바로 배타 생성한 파일) · 복사본 다섯 · 디스크 · 시각.
쓰기 = <E>/03_end.json 배타 생성. git · 네트워크 0. 이름 확인 결과는 이름만 담는다 (값은 처음부터 받지 않는다). 읽지 못한 파일 (중간에 멈춰 없는
meta · 외곽 반환 등) 은 그 자리에 사유를 남긴다 — 기록을 대신 채우지 않는다. 증거 폴더 이름 규칙 밖이면 아무것도 쓰지 않고 멈춘다.
"""
import datetime
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

STEPS = ("01_red_e1_0b", "02_green_e1_0b")


def read(path: Path):
    """(바이트, None) 또는 (None, 사유)."""
    try:
        return path.read_bytes(), None
    except OSError as e:
        return None, f"{e.__class__.__name__}: {e}"


def outer_rc(path: Path) -> dict:
    b, why = read(path)
    if b is None:
        return {"why": why}
    text = b.decode("utf-8", "replace")
    return {"text": text, "rc": int(text.strip()) if text.strip().lstrip("-").isdigit() else None}


def meta(path: Path):
    b, why = read(path)
    if b is None:
        return None, why
    try:
        return json.loads(b.decode("utf-8")), None
    except ValueError as e:
        return None, f"{e.__class__.__name__}: {e}"


e = Path(sys.argv[1])
if not re.fullmatch(r"reil_c4e1_0b_20[0-9]{6}", e.name) or e.parent.name != "evidence":
    raise SystemExit(f"증거 폴더 이름 규칙 밖 — 쓰지 않는다: {e}")
check = json.loads(sys.argv[2])
repo = e.parent.parent.parent
copies = ("bms-balancing/tests/test_reil_c4e1_launch.py", "bms-balancing/tests/test_reil_c4e1_runner.py", "bms-balancing/scripts/reil_c4e1_launch.py",
          f"bms-balancing/evidence/{e.name}/00_step_runner.py", f"bms-balancing/evidence/{e.name}/00_end_writer.py")
digests = {}
for c in copies:
    b, why = read(repo / c)
    digests[c] = hashlib.sha256(b).hexdigest() if b is not None else {"why": why}
out = {"kind": "REIL_C4E1_0B_END",
       "utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
       "disk_avail_bytes": shutil.disk_usage(repo).free,
       "copies_sha256": digests,
       "git_name_check_e": {"git_env_names": check["git_env_names"], "outside_allowlist": check["outside_allowlist"]},
       "steps": {}}
for step in STEPS:
    m, why = meta(e / f"{step}.meta.json")
    row = {"outer_rc": outer_rc(e / f"{step}.outer_rc.txt")}
    if m is None:
        row["meta_why"] = why
    else:
        rec = m.get("records") or {}
        cl = m.get("cleanup") or {}
        row.update(started=m.get("started"), runner_ok=m.get("runner_ok"), rc=m.get("rc"), timed_out=m.get("timed_out"),
                   cleanup_status=cl.get("status"), deadline_hit=cl.get("deadline_hit"), times=m.get("times"),
                   head_start=(rec.get("head_start") or {}).get("out"), head_end=(rec.get("head_end") or {}).get("out"))
    out["steps"][step] = row
with open(e / "03_end.json", "x", encoding="utf-8") as f:
    f.write(json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True) + "\n")
print(json.dumps({"written": str(e / "03_end.json"), "runner_ok": {s: out["steps"][s].get("runner_ok") for s in STEPS},
                  "outer_rc": {s: out["steps"][s]["outer_rc"].get("rc") for s in STEPS}}, ensure_ascii=False))
