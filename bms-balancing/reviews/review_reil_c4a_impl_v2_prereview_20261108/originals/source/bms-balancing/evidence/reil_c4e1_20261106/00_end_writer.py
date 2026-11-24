"""REIL C4-E · E1-1–3 끝 기록 작성기 초안 v2 (2026-11-04 · 정정 범위안 v2 §3 · 사용자 채택 §109) — 고정 뒤 `<E>/00_end_writer.py` 로 복사해 쓴다.

python -I <E>/00_end_writer.py <E> '<절차 Git 이름 확인 JSON>'

읽기 (파일마다 한 번의 보호된 읽기 — 같은 버퍼에서 sha256 · bytes · 작은 파일의 본문 · 사유를 만든다. 그 버퍼가 쓰는 중인 원본의 한 시점이라는 뜻은
아니다): 복사본 넷 (`00_outer.py` · `00_judge.py` · `00_end_writer.py` · `00_identity_c4.py`) 과 launcher · `00_overall.json` · `00_start.txt` · 탐침 사본
`01_probe/` · 읽기 경로 기록 `03_read_path.json` · 세 단계마다 기산점 · 외곽 기록 (시작 또는 묘비 · 끝 · 반환 · 오류 · 임시) · 감시 기록 (호출 · 조각 · 끝 ·
임시 — 있는 대로) · launcher meta 의 요약 · 판정 기록 · 잔류 관측 (1 · 2) · kill · frozen 목록 · 디스크 · 시각. Git · 네트워크 · 하위 프로세스 · 신호 0.

기록을 모을 뿐 판정하지 않는다. 읽지 못한 파일 · 항목 · 단계의 예외는 그 자리에 사유로 남긴다 (대신 채우지 않는다). 이름 확인 결과는 받은 JSON 의 이름
목록만 담는다. 쓰기 = `06_end.json` 의 배타 생성 **시도** 하나 (임시 → fsync → link). 기록 자체가 실패하면 (임시 생성 · 쓰기 · fsync · link · 임시 제거
중 어느 단계든) stdout 한 줄 (`end_written` · 단계 · 오류) · 반환 5 → 미완. 부분 임시 파일은 지우거나 고치지 않고 다시 하지 않는다. stdout 마저 쓸 수
없으면 미확인이지 성공이 아니다. 폴더 이름 규칙 밖 · 이 파일이 그 폴더의 `00_end_writer.py` 가 아님 · `06_end.json` 또는 그 임시 파일이 이미 있음이면
아무것도 쓰지 않고 반환 2.
"""
import hashlib
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

BMS = Path("/home/user/Yonghoon-DEM-DFT/bms-balancing")
LAUNCHER = BMS / "scripts" / "reil_c4e1_launch.py"
EVIDENCE_NAME = re.compile(r"^reil_c4e1_20[0-9]{6}$")
STEPS = {"identity": "03_identity", "fetch": "04_fetch", "run": "05_run"}
COPIES = ("00_outer.py", "00_judge.py", "00_end_writer.py", "00_identity_c4.py")
OUT = "06_end.json"
TEXT_MAX = 200


def utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def take(p: Path):
    """한 번의 보호된 읽기 → (행, 바이트 또는 None). 행의 sha · bytes · 본문은 그 한 버퍼에서만 만든다."""
    row = {"path": str(p)}
    try:
        if p.is_symlink() or not p.is_file():
            row["why"] = "없음 또는 일반 파일 아님"
            return row, None
        b = p.read_bytes()
    except OSError as e:
        row["why"] = f"읽지 못함 {e.__class__.__name__}: {e}"[:300]
        return row, None
    row.update(sha256=hashlib.sha256(b).hexdigest(), bytes=len(b))
    if len(b) <= TEXT_MAX:
        row["text"] = b.decode("utf-8", "replace")
    return row, b


def jtake(p: Path):
    """한 번 읽은 같은 버퍼를 JSON 으로 → (행, 객체 또는 None)."""
    row, b = take(p)
    if b is None:
        return row, None
    try:
        doc = json.loads(b)
    except ValueError as e:
        row["why"] = f"JSON: {e}"[:200]
        return row, None
    if not isinstance(doc, dict):
        row["why"] = "JSON 객체 아님"
        return row, None
    return row, doc


def pick(doc, keys) -> dict:
    return {"fields": {k: doc.get(k) for k in keys}} if isinstance(doc, dict) else {}


def step_row(ev: Path, name: str) -> dict:
    row = {}
    r, d = jtake(ev / f"{name}.outer_start.json")
    row["outer_start"] = r | pick(d, ("kind", "utc", "epoch", "deadline_epoch", "launch_epoch", "sid", "overall_sha256"))
    r, d = jtake(ev / f"{name}.outer_end.json")
    row["outer_end"] = r | pick(d, ("kind", "rc", "start_sha256", "launcher_exit_epoch", "end_snapshot_epoch"))
    r, d = jtake(ev / f"{name}.outer_error.json")
    row["outer_error"] = r | pick(d, ("kind", "phase", "message"))
    for k in ("launch_epoch.txt", "outer_rc.txt", "outer_stderr.txt", "wrapper_output.txt"):
        row[k] = take(ev / f"{name}.{k}")[0]
    row["outer_tmp"] = {x.name: take(x)[0] for x in sorted(ev.glob(f"{name}.outer_*.tmp"))}
    watch = {}
    for x in sorted(ev.glob(f"{name}.watch*")):
        if x.suffix == ".json":
            r, d = jtake(x)
            watch[x.name] = r | pick(d, ("kind", "k", "state", "observed_epoch", "deadline_epoch", "rc", "prev_sha256", "begin_sha256"))
        else:
            watch[x.name] = take(x)[0]
    row["watch"] = watch
    r, m = jtake(ev / f"{name}.meta.json")
    if m is None:
        row["meta"] = r
    else:
        child = m.get("child") if isinstance(m.get("child"), dict) else {}
        stage = m.get("stage") if isinstance(m.get("stage"), dict) else {}
        group = child.get("group") if isinstance(child.get("group"), dict) else {}
        row["meta"] = r | {
            "start_utc": m.get("start_utc"), "end_utc": m.get("end_utc"), "stage_complete": stage.get("complete"),
            "stage_terms": stage.get("terms"), "child_rc": child.get("rc"), "child_timed_out": child.get("timed_out"),
            "child_group_status": group.get("status"), "child_deadline_hit": child.get("deadline_hit"),
            "errors": len(m.get("errors") or []), "child_maxrss_kib": m.get("child_maxrss_kib")}
    r, j = jtake(ev / f"{name}.judge.json")
    row["judge"] = r | pick(j, ("verdict", "failed", "execution_validity", "experimental_result"))
    for k in ("leftover_1.json", "leftover_2.json"):
        r, d = jtake(ev / f"{name}.{k}")
        row[k] = r | ({"alive_count": d.get("alive_count"), "errors": len(d.get("errors") or []), "sid": d.get("sid"),
                       "sid_error": d.get("sid_error", "(키 없음)")} if d else {})
    r, d = jtake(ev / f"{name}.kill.json")
    row["kill.json"] = r | ({"actions": [x.get("action") for x in d.get("results") or [] if isinstance(x, dict)]} if d else {})
    r, d = jtake(ev / f"frozen_{name}.json")
    row["frozen"] = r | ({"rows": len(d.get("rows") or []), "counts": d.get("counts")} if d else {})
    fz = ev / f"frozen_{name}"
    if fz.is_dir() and not fz.is_symlink():
        row["frozen_files"] = {str(x.relative_to(ev)): take(x)[0] for x in sorted(fz.rglob("*")) if x.is_file() or x.is_symlink()}
    return row


def main(argv=None) -> int:
    a = list(sys.argv[1:] if argv is None else argv)
    me = Path(__file__)
    if len(a) != 2:
        sys.stderr.write("거부: 인자 — <E> '<이름 확인 JSON>'\n")
        return 2
    ev = Path(a[0])
    if ev.parent != BMS / "evidence" or not EVIDENCE_NAME.match(ev.name) or ev.is_symlink() or not ev.is_dir():
        sys.stderr.write(f"거부: 증거 폴더 규칙 밖: {ev}\n")
        return 2
    if me.is_symlink() or me.resolve() != (ev / "00_end_writer.py").resolve():
        sys.stderr.write(f"거부: 이 파일이 그 증거 폴더의 00_end_writer.py 가 아니다: {me}\n")
        return 2
    outp = ev / OUT
    tmp = outp.with_name(outp.name + ".tmp")
    if os.path.lexists(outp) or os.path.lexists(tmp):
        sys.stderr.write(f"거부: 이미 있다 (자동 재시도 없음): {outp} 또는 {tmp}\n")
        return 2
    try:
        chk = json.loads(a[1])
        name_check = {"git_env_names": list(chk.get("git_env_names") or []), "outside_allowlist": list(chk.get("outside_allowlist") or [])}
    except (ValueError, AttributeError, TypeError) as e:
        name_check = {"why": f"이름 확인 JSON 을 읽지 못함 {e.__class__.__name__}"}
    rec = {"kind": "REIL_E113_END", "utc": utc(), "evidence": str(ev), "git_name_check": name_check,
           "note": "모으기만 한다 (판정 아님) · 파일마다 한 번 읽은 같은 버퍼 · 원자 snapshot 아님 · push 전 기록이라 g3 의 반환을 담지 않는다"}
    sections = {
        "copies": lambda: {c: take(ev / c)[0] for c in COPIES},
        "launcher": lambda: take(LAUNCHER)[0],
        "overall": lambda: (lambda r_d: r_d[0] | pick(r_d[1], ("kind", "section", "T_a", "T_end", "R")))(jtake(ev / "00_overall.json")),
        "start_seal": lambda: take(ev / "00_start.txt")[0],
        "probe": lambda: {str(x.relative_to(ev)): take(x)[0] for x in sorted((ev / "01_probe").rglob("*")) if x.is_file() or x.is_symlink()},
        "read_path": lambda: (lambda r_d: r_d[0] | pick(r_d[1], ("status",)))(jtake(ev / "03_read_path.json")),
        "disk_avail_bytes": lambda: shutil.disk_usage(BMS).free,
    }
    for key, fn in sections.items():
        try:
            rec[key] = fn()
        except Exception as e:  # noqa: BLE001 — 항목마다 예외를 사유로 남기고 다음 항목으로
            rec[key] = {"why": f"예외 {e.__class__.__name__}: {e}"[:300]}
    rec["steps"] = {}
    for step, name in STEPS.items():
        try:
            rec["steps"][step] = step_row(ev, name)
        except Exception as e:  # noqa: BLE001 — 단계마다 예외를 사유로 남기고 다음 단계로
            rec["steps"][step] = {"why": f"예외 {e.__class__.__name__}: {e}"[:300]}
    phase = "encode"
    try:
        data = (json.dumps(rec, ensure_ascii=False, indent=1, sort_keys=True, default=str) + "\n").encode("utf-8")
        phase = "tmp_create"
        with open(tmp, "xb") as f:
            phase = "write"
            f.write(data)
            phase = "fsync"
            f.flush()
            os.fsync(f.fileno())
        phase = "link"
        os.link(tmp, outp)
        phase = "unlink_tmp"
        os.unlink(tmp)
    except Exception as e:  # noqa: BLE001 — 기록 자체의 실패 = 미완 (부분 임시 파일은 그대로 · 다시 하지 않는다)
        print(json.dumps({"end_written": False, "final_exists": os.path.lexists(outp), "phase": phase,
                          "error": f"{e.__class__.__name__}: {e}"[:300], "path": str(outp)}, ensure_ascii=False))
        return 5
    judges = {s: (r.get("judge") or {}).get("fields", {}).get("verdict") if isinstance(r, dict) else None for s, r in rec["steps"].items()}
    print(json.dumps({"end_written": True, "written": str(outp), "judge": judges}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
