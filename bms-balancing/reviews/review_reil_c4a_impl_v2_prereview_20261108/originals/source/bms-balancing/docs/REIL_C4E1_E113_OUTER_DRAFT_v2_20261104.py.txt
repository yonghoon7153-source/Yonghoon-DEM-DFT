"""REIL C4-E · E1-1–3 외곽 도구 초안 v2 (2026-11-04 · 정정 범위안 v2 · 사용자 채택 §109) — 고정 뒤 `<E>/00_outer.py` 로 복사해 쓴다.

세 launcher 단계 (identity · fetch · run) 의 분리 실행 wrapper · 감시 · 잔류 관측 · R1 정리 · F3 고정 사본 · 커밋 전 공개 검사. 모드 여섯:

  start   <step> <E> <§NN>   띄우는 셸 줄이 `set -C` 로 `<name>.launch_epoch.txt` 를 만든 뒤 `setsid nohup` 으로만 띄운다. 착수 전 확인 — 기존 기록 →
                             기산점 · `00_overall.json` · launcher sha → 시작 창 (0 ≤ t − 기산점 ≤ 60 s) · 단계 기한 (t + 감시 여유 ≤ T_end − R) → 시작
                             기록을 배타 link (시작 경로의 소유 — 감시의 묘비가 먼저면 실패) → link 가 성공했을 때만 launcher 를 자식으로 띄운다. launcher
                             반환 뒤 끝 기록 (`outer_end.json`) → 반환 (`outer_rc.txt`) 순서로 배타 게시. launcher 를 죽이지 않는다.
                             반환 0 = 게시 · 2 = 거부 (기존 기록 · 아무것도 쓰지 않음) · 3 = 착수 전 / 띄우기 실패 (외곽 오류 게시) · 4 = 게시 실패.
  wait    <step> <E>         감시 호출 하나 (정정 범위안 v2 §2-2 · §2-5). 진입 규칙 → 호출 기록 → 시작 대기 (기산점 + 60 s · 없으면 묘비) → 관측 → 끝 기록
                             (`watch.json`) 또는 조각 기록 (`watch_<k>.slice.json` · 조각 6,600 s). 정상 수용은 rc 와 끝 기록을 검증한 직후의 관측 시각 ≤
                             기한일 때만. run 에 개입하지 않는다 (신호 · launcher 파일 쓰기 없음 — 묘비는 시작 기록이 없을 때만 생긴다). 반환은 §2-5 의 표
                             (0 · 10–21 · 2).
  observe <step> <E> <1|2>   /proc 의 잔류 관측 (읽기) → `<name>.leftover_<n>.json` 배타 생성. 표지 = 시작 기록의 세션 id · cmdline 의
                             `pycache_prefix=<WORK>/pycache/<name>` · cmdline 의 `<E>` 경로. 자기와 조상은 뺀다. 반환 0 = 살아 있는 것 0 · 읽기 오류 0 · 세션
                             id 확인 (`sid_error` null) · 1 = 그 밖.
  kill    <step> <E>         R1. `leftover_1` 의 살아 있는 (Z 아닌) 그룹마다, 관측한 구성원 하나의 시작 시각 · 그룹이 그대로일 때만 SIGKILL 한 번 →
                             `<name>.kill.json` 배타 생성. pgid ≤ 1 · 자기 · 조상의 그룹은 건드리지 않는다. 반환 0.
  freeze  <step> <E>         F3. 그 단계의 가변 파일을 읽은 그대로 `frozen_<name>/` 에 사본 · 파일마다 성공 / 실패 · 사유 · 읽은 시각 → 목록
                             `frozen_<name>.json` 배타 게시. 목록을 게시하지 못하면 stdout 한 줄 · 반환 5. 부분 사본은 지우거나 고치지 않고 다시 하지 않는다.
  check   <E> <cached|-> <index|-> <path>…
                             커밋 전 공개 검사 (쓰기 0). 파일마다 한 번 읽은 버퍼에서 원자료 sha · 확장자 · 크기 · URL 계정 형태와 git blob id 를 만든다
                             (`.py` 는 `<E>` 바로 아래의 고정 사본 넷만 — 그 sha 는 `00_start.txt` 가 묶는다). `git diff --cached --name-only -z` · `git
                             ls-files -s -z --full-name -- <path>…` 의 출력 파일을 받으면 staged 집합 = 경로 집합 · staged blob = 검사한 버퍼의 blob 까지
                             본다. 반환 0 = 통과 · 1 = 어긋남 · 2 = 거부.

공통: 증거 폴더 = BMS/evidence/reil_c4e1_YYYYMMDD (있는 폴더 · 링크 아님) 이고 이 파일이 그 폴더의 `00_outer.py` 일 때만 움직인다. 기록은 모두 배타
생성이다 (덮어쓰지 않는다 · 임시 → fsync → link · 실패한 게시의 임시 파일은 지우지 않는다). 의도된 거부는 아무것도 쓰지 않고 반환 2. 네트워크 · Git 0
(check 는 Git 이 이미 쓴 출력 파일을 읽기만 한다). 한 번 읽기는 같은 버퍼에서 sha · 본문을 만든다는 뜻이지 쓰는 중인 원본의 한 시점이라는 뜻이 아니다.
같은 호스트의 실시간 시계 · 로컬 파일 시스템의 원자적 link · O_EXCL 의 공개 의미에 기댄다 (실제 동작을 이 초안이 관측한 것은 아니다).
"""
import hashlib
import json
import os
import re
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path("/home/user/Yonghoon-DEM-DFT")
BMS = REPO / "bms-balancing"
SP = Path("/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/b881d255-9513-5adc-9b14-3c0be18d7ad6/scratchpad")
WORK = SP / "c4e1"
PROC = Path("/proc")
PY = "/usr/bin/python3.11"
LAUNCHER = BMS / "scripts" / "reil_c4e1_launch.py"
LAUNCHER_SHA256 = "2c70712381aec657f81c8e72c85e8c06e654364aefe9e38e5254ecfece9e4ebf"
STEPS = {"identity": "03_identity", "fetch": "04_fetch", "run": "05_run"}
ALLOW_S = {"identity": 900.0, "fetch": 1800.0, "run": 12600.0}
START_WAIT_S = 60.0
START_POLL_S = 1.0
POLL_S = 5.0
WAIT_SLICE_S = 6600.0
WRAPPER_EXIT_S = 10.0
TOTAL_S = 21600
RESERVE_S = 1800
OVERALL = "00_overall.json"
FIXED_COPIES = ("00_identity_c4.py", "00_outer.py", "00_judge.py", "00_end_writer.py")
DATA_SHA256 = {"fd50e09542be7adb2270963d65a6e7b5ccae1473a512f68462c2dd419d620ee1",
               "3c19e45ef8a64ce67cda1f623551e758d4c0f67086bbae02b978428d78de1c76"}
FILE_MAX = 50 * 2 ** 20
COMMIT_MAX = 100 * 2 ** 20
EVIDENCE_NAME = re.compile(r"^reil_c4e1_20[0-9]{6}$")
SECTION = re.compile(r"^§[0-9]{2,3}$")
RC_FORMAT = re.compile(rb"[0-9]+\n")
EPOCH_FORMAT = re.compile(rb"[0-9]{10}\n")
URL_ACCOUNT = re.compile(rb"[A-Za-z][A-Za-z0-9+.-]*://[^/\s\"@]+@")
LAUNCHER_FILES = ("precheck.json", "meta.json", "stdout.log", "stderr.log", "porcelain_start.txt", "porcelain_end.txt")
OUTER_RECORDS = ("outer_start.json", "outer_end.json", "outer_rc.txt", "outer_error.json")
OUTER_FILES = OUTER_RECORDS + tuple(f"{k}.tmp" for k in OUTER_RECORDS) + ("outer_stdout.txt", "outer_stderr.txt")
SHELL_FILES = ("launch_epoch.txt", "wrapper_output.txt")
WATCH = ("watch.json", "watch.json.tmp")
MODES = ("start", "wait", "observe", "kill", "freeze", "check")
K_START, K_MISSING, K_END, K_ERROR = "REIL_E113_OUTER_START", "REIL_E113_START_MISSING", "REIL_E113_OUTER_END", "REIL_E113_OUTER_ERROR"
K_BEGIN, K_SLICE, K_WATCH, K_OVERALL = "REIL_E113_WATCH_BEGIN", "REIL_E113_WATCH_SLICE", "REIL_E113_WATCH", "REIL_E113_OVERALL"


class Refusal(Exception):
    """의도된 거부 — 아무것도 쓰지 않고 반환 2."""


def utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def blob_id(b: bytes) -> str:
    """git 의 blob id (`blob <길이>\\0` + 바이트의 sha1) — git 을 부르지 않고 같은 버퍼에서 만든다."""
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


def dump(obj) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n").encode("utf-8")


def is_int(x) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)


def is_num(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool) and x == x and abs(x) != float("inf")


def write_new(path, data: bytes) -> None:
    """배타 생성 (있으면 FileExistsError)."""
    with open(path, "xb") as f:
        f.write(data)


def publish(path: Path, data: bytes) -> None:
    """임시 이름에 쓰고 fsync · 닫은 뒤 최종 이름으로 배타 link (이미 있으면 FileExistsError) → 임시 이름을 지운다. 최종 이름이 보이는 순간 내용이
    완전하다. 어느 단계에서 실패하든 남은 임시 파일은 지우지 않는다 (부르는 쪽이 실패로 다룬다)."""
    tmp = path.with_name(path.name + ".tmp")
    with open(tmp, "xb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    os.link(tmp, path)
    os.unlink(tmp)


def read_once(p: Path):
    """한 번의 보호된 읽기 → (바이트, None) 또는 (None, 사유)."""
    try:
        if p.is_symlink() or not p.is_file():
            return None, "absent_or_not_regular"
        return p.read_bytes(), None
    except OSError as e:
        return None, f"{e.__class__.__name__}: {e}"[:300]


def load(p: Path):
    """한 번 읽어 (바이트, JSON 객체 또는 None, 사유)."""
    b, why = read_once(p)
    if b is None:
        return None, None, why
    try:
        doc = json.loads(b)
    except ValueError as e:
        return b, None, f"JSON: {e}"[:300]
    return (b, doc, None) if isinstance(doc, dict) else (b, None, "JSON 객체 아님")


def names(ev: Path, step: str) -> dict:
    name = STEPS[step]
    return {k: ev / f"{name}.{k}" for k in LAUNCHER_FILES + OUTER_FILES + SHELL_FILES + WATCH}


def watch_part(ev: Path, name: str, k: int, part: str) -> Path:
    return ev / f"{name}.watch_{k}.{part}.json"


def watch_numbers(ev: Path, name: str, part: str) -> list:
    pat = re.compile(rf"{re.escape(name)}\.watch_([1-9][0-9]*)\.{part}\.json")
    return sorted(int(m.group(1)) for m in (pat.fullmatch(x.name) for x in ev.iterdir()) if m)


def launch_epoch(p: dict) -> int:
    b, why = read_once(p["launch_epoch.txt"])
    if b is None or not EPOCH_FORMAT.fullmatch(b):
        raise ValueError(f"launch_epoch.txt — {why or b[:20].hex()}")
    return int(b)


def overall(ev: Path, section: str):
    b, d, why = load(ev / OVERALL)
    if d is None:
        raise ValueError(f"{OVERALL} — {why}")
    if not (d.get("kind") == K_OVERALL and d.get("section") == section and is_int(d.get("T_a")) and is_int(d.get("T_end"))
            and d["T_end"] == d["T_a"] + TOTAL_S and is_int(d.get("R")) and d["R"] == RESERVE_S):
        raise ValueError(f"{OVERALL} — 필수 키 · 값이 맞지 않다: {sorted(d)}")
    return d, b


def stat_fields(pid: int) -> dict:
    """/proc/<pid>/stat → 상태 · ppid · pgid · 세션 · 시작 시각 (괄호 안 comm 의 공백 · 괄호와 무관하게 마지막 ')' 뒤를 읽는다)."""
    raw = (PROC / str(pid) / "stat").read_bytes()
    rest = raw[raw.rindex(b")") + 2:].split()
    return {"state": rest[0].decode("ascii", "replace"), "ppid": int(rest[1]), "pgid": int(rest[2]), "sid": int(rest[3]),
            "starttime": int(rest[19])}


def ancestors() -> set:
    """자기와 조상 pid (셸 도구의 셸 포함) — 관측 · 정리에서 뺀다."""
    seen, pid = set(), os.getpid()
    while pid > 1 and pid not in seen:
        seen.add(pid)
        try:
            pid = stat_fields(pid)["ppid"]
        except (OSError, ValueError, IndexError):
            break
    return seen


# ---------------------------------------------------------------- start
def start(step: str, ev: Path, section: str) -> int:
    p, name = names(ev, step), STEPS[step]
    taken = [k for k in OUTER_FILES + WATCH if os.path.lexists(p[k])]
    if taken:
        raise Refusal(f"이 단계의 기록이 이미 있다 — 띄우지 않는다: {taken}")

    def fail(phase: str, message: str, code: int = 3, **kw) -> int:
        doc = {"kind": K_ERROR, "step": step, "name": name, "phase": phase, "utc": utc(), "epoch": time.time(), "message": message[:500], **kw}
        try:
            publish(p["outer_error.json"], dump(doc))
        except Exception as e:  # noqa: BLE001 — 외곽 오류마저 게시하지 못하면 stdout 한 줄 · 반환 4
            print(json.dumps({"step": step, "outer_error_published": False, "phase": phase, "message": message[:300],
                              "error": f"{e.__class__.__name__}: {e}"[:300]}, ensure_ascii=False))
            return 4
        return code

    try:
        le = launch_epoch(p)
        ov, ov_bytes = overall(ev, section)
        lb = LAUNCHER.read_bytes()
        me = Path(__file__).resolve()
        me_sha = sha256(me.read_bytes())
    except (OSError, ValueError) as e:
        return fail("precheck", f"{e.__class__.__name__}: {e}")
    lsha = sha256(lb)
    if lsha != LAUNCHER_SHA256:
        return fail("precheck", f"launcher sha256 {lsha} ≠ 고정 {LAUNCHER_SHA256}")
    argv = [PY, "-I", str(LAUNCHER), step, "--evidence", str(ev), "--approval-section", section]
    t = time.time()
    deadline = t + ALLOW_S[step]
    if not 0.0 <= t - le <= START_WAIT_S:
        return fail("window", f"시작 창 밖 — t − launch_epoch = {t - le:.3f} s", launch_epoch=le, epoch=t)
    if deadline > ov["T_end"] - ov["R"]:
        return fail("budget", f"단계 기한 {deadline:.3f} > T_end − R = {ov['T_end'] - ov['R']}", epoch=t, deadline_epoch=deadline)
    rec = {"kind": K_START, "step": step, "name": name, "section": section, "utc": utc(), "epoch": t, "deadline_epoch": deadline,
           "allow_s": ALLOW_S[step], "launch_epoch": le, "overall_sha256": sha256(ov_bytes), "T_a": ov["T_a"], "T_end": ov["T_end"],
           "R": ov["R"], "pid": os.getpid(), "ppid": os.getppid(), "sid": os.getsid(0), "pgid": os.getpgid(0), "argv": argv,
           "cwd": str(BMS), "outer": {"path": str(me), "sha256": me_sha},
           "launcher": {"path": str(LAUNCHER), "sha256": lsha, "expected": LAUNCHER_SHA256}, "python": sys.version}
    start_bytes = dump(rec)
    try:
        publish(p["outer_start.json"], start_bytes)
    except OSError as e:  # EEXIST = 감시의 묘비 (또는 다른 기록) 가 시작 경로를 먼저 가졌다 → launcher 를 띄우지 않는다
        return fail("claim", f"시작 경로를 가지지 못했다 — {e.__class__.__name__}: {e}")
    try:
        with open(p["outer_stdout.txt"], "xb") as fo, open(p["outer_stderr.txt"], "xb") as fe:
            child = subprocess.Popen(argv, cwd=str(BMS), stdin=subprocess.DEVNULL, stdout=fo, stderr=fe)
            raw_rc = child.wait()
    except Exception as e:  # noqa: BLE001 — 띄우기 · 기다리기의 실패는 외곽 오류로 남기고 반환을 게시하지 않는다
        return fail("launch", f"{e.__class__.__name__}: {e}")
    t_exit = time.time()
    ret = raw_rc if raw_rc >= 0 else 128 - raw_rc  # 시그널로 끝나면 셸 관례 128 + 번호
    end = {"kind": K_END, "step": step, "name": name, "start_sha256": sha256(start_bytes), "launcher_pid": child.pid, "rc": ret,
           "returncode": raw_rc, "launcher_exit_epoch": t_exit, "utc": utc(),
           "note": "end_snapshot_epoch 는 이 파일을 쓰기 직전의 값이다 — 그 뒤 이 파일 · outer_rc 의 게시 완료를 증명하지 않는다"}
    end["end_snapshot_epoch"] = time.time()
    try:
        publish(p["outer_end.json"], dump(end))
    except Exception as e:  # noqa: BLE001 — 끝 기록을 게시하지 못하면 rc 를 게시하지 않는다
        return fail("end_publish", f"{e.__class__.__name__}: {e}", code=4, rc=ret)
    try:
        publish(p["outer_rc.txt"], f"{ret}\n".encode("ascii"))
    except Exception as e:  # noqa: BLE001
        return fail("rc_publish", f"{e.__class__.__name__}: {e}", code=4, rc=ret)
    return 0


# ---------------------------------------------------------------- wait (감시 호출 하나)
def end_problems(end, step: str, name: str, start_sha: str, rc: int, epoch0) -> str:
    if end is None:
        return "끝 기록 없음 · 못 읽음"
    if end.get("kind") != K_END or end.get("step") != step or end.get("name") != name:
        return "kind · 단계 · 이름"
    if end.get("start_sha256") != start_sha:
        return "start_sha256 불일치 (같은 실행이 아니다)"
    if not is_int(end.get("rc")) or end["rc"] != rc:
        return "rc 불일치"
    a, b = end.get("launcher_exit_epoch"), end.get("end_snapshot_epoch")
    if not (is_num(a) and is_num(b) and epoch0 <= a <= b):
        return "시각 순서 (epoch ≤ launcher_exit_epoch ≤ end_snapshot_epoch)"
    return ""


def observe_return(step: str, p: dict, name: str, le: int, begin_sha: str, start_sha, slice_end: float):
    """시작 대기 → 관측. (상태, 반환, 필드). 쓰는 것은 묘비 하나뿐 (시작 창이 끝나도 시작 기록이 없을 때)."""
    while not os.path.lexists(p["outer_start.json"]):
        if os.path.lexists(p["outer_error.json"]):
            return "outer_error", 12, {"launch_epoch": le, "error": load(p["outer_error.json"])[1]}
        if time.time() >= le + START_WAIT_S:
            tomb = dump({"kind": K_MISSING, "step": step, "name": name, "utc": utc(), "epoch": time.time(), "launch_epoch": le,
                         "begin_sha256": begin_sha, "pid": os.getpid()})
            try:
                fd = os.open(p["outer_start.json"], os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
            except FileExistsError:
                break  # 그사이 wrapper 가 시작 경로를 가졌다 → 아래에서 읽어 확인한다
            with os.fdopen(fd, "wb") as f:
                f.write(tomb)
                f.flush()
                os.fsync(f.fileno())
            return "start_missing", 13, {"launch_epoch": le, "tombstone_sha256": sha256(tomb)}
        time.sleep(START_POLL_S)
    sb, st, why = load(p["outer_start.json"])
    ok = (st is not None and st.get("kind") == K_START and st.get("step") == step and st.get("name") == name
          and is_num(st.get("epoch")) and is_num(st.get("deadline_epoch")) and st["deadline_epoch"] == st["epoch"] + ALLOW_S[step]
          and is_int(st.get("launch_epoch")) and st["launch_epoch"] == le and 0.0 <= st["epoch"] - le <= START_WAIT_S
          and is_int(st.get("pid")) and (start_sha is None or sha256(sb) == start_sha))
    if not ok:
        return "start_unreadable", 14, {"launch_epoch": le, "why": why, "kind": None if st is None else st.get("kind"),
                                        "start_sha256": None if sb is None else sha256(sb)}
    s_sha, deadline, epoch0 = sha256(sb), st["deadline_epoch"], st["epoch"]
    base = {"deadline_epoch": deadline, "start_sha256": s_sha, "wrapper_pid": st["pid"]}
    while True:
        now = time.time()
        if os.path.lexists(p["outer_error.json"]):
            return "outer_error", 12, {**base, "observed_epoch": now, "error": load(p["outer_error.json"])[1]}
        if os.path.lexists(p["outer_rc.txt"]):
            rb, why = read_once(p["outer_rc.txt"])
            if rb is None or not RC_FORMAT.fullmatch(rb):
                return "malformed", 11, {**base, "observed_epoch": time.time(), "why": why,
                                         "raw_hex": None if rb is None else rb[:20].hex()}
            rc = int(rb)
            eb, end, why = load(p["outer_end.json"])
            bad = end_problems(end, step, name, s_sha, rc, epoch0)
            if bad:
                return "end_invalid", 18, {**base, "observed_epoch": time.time(), "rc": rc, "why": why or bad,
                                           "end_sha256": None if eb is None else sha256(eb)}
            t_obs = time.time()  # rc 와 끝 기록을 읽고 검증을 마친 직후 — 정상 수용의 유일한 시각
            state, code = ("published", 0) if t_obs <= deadline else ("late", 17)
            return state, code, {**base, "observed_epoch": t_obs, "rc": rc, "end_sha256": sha256(eb),
                                 "launcher_exit_epoch": end["launcher_exit_epoch"], "end_snapshot_epoch": end["end_snapshot_epoch"]}
        if now >= deadline:
            return "deadline", 10, {**base, "observed_epoch": now}
        if now >= slice_end:
            return "continue", 15, {**base, "last_poll_epoch": now, "slice_end_epoch": slice_end}
        time.sleep(POLL_S)


def wrapper_exit(pid) -> str:
    """게시 뒤 wrapper 가 끝날 때까지 (없음 또는 Z) 최대 WRAPPER_EXIT_S 를 읽기만 하며 기다린다 — 결과는 stdout 에만."""
    if not is_int(pid):
        return "unknown"
    t0 = time.time()
    while True:
        try:
            state = stat_fields(pid)["state"]
        except (OSError, ValueError, IndexError):
            return "absent"
        if state == "Z" or time.time() - t0 >= WRAPPER_EXIT_S:
            return state
        time.sleep(0.5)


def wait(step: str, ev: Path) -> int:
    p, name = names(ev, step), STEPS[step]
    t_begin = time.time()

    def say(state: str, code: int, **kw) -> int:
        print(json.dumps({"step": step, "state": state, "code": code, "utc": utc(), "waited_s": round(time.time() - t_begin, 1), **kw},
                         ensure_ascii=False, default=str))
        return code

    # 0. 기산점 — 없거나 형식이 틀리면 거부 (띄우는 줄보다 먼저 감시를 걸지 않는다)
    try:
        le = launch_epoch(p)
    except (OSError, ValueError) as e:
        raise Refusal(f"기산점: {e}") from e
    # 1. 끝 기록이 있으면 소비 (새로 쓰지 않는다)
    if os.path.lexists(p["watch.json"]):
        _, doc, why = load(p["watch.json"])
        if doc is None or doc.get("kind") != K_WATCH:
            return say("unknown", 16, why="watch.json 을 읽지 못함", detail=why)
        return say("consumed", 20, recorded=doc)
    # 2. 감시 기록의 임시 파일
    tmps = sorted(x.name for x in ev.glob(f"{name}.watch*.tmp"))
    if tmps:
        return say("unknown", 16, why="감시 기록의 임시 파일", tmp=tmps)
    # 3. 이전 호출의 사슬 — 모두 조각 기록 (continue) 으로 끝났어야 한다
    begins, slices = watch_numbers(ev, name, "begin"), watch_numbers(ev, name, "slice")
    if begins != list(range(1, len(begins) + 1)) or slices != begins:
        return say("unknown", 16, why="이전 호출의 결과 불명 (조각 기록 없음 · 번호 틈)", begins=begins, slices=slices)
    prev_sha, start_sha = None, None
    for k in begins:
        bb, bd, why1 = load(watch_part(ev, name, k, "begin"))
        sb, sd, why2 = load(watch_part(ev, name, k, "slice"))
        if (bd is None or sd is None or bd.get("kind") != K_BEGIN or bd.get("step") != step or bd.get("k") != k
                or "prev_sha256" not in bd or bd["prev_sha256"] != prev_sha or sd.get("kind") != K_SLICE or sd.get("k") != k
                or sd.get("state") != "continue" or sd.get("begin_sha256") != sha256(bb) or not isinstance(sd.get("start_sha256"), str)
                or (start_sha is not None and sd["start_sha256"] != start_sha)):
            return say("unknown", 16, why=f"호출 {k} 의 기록이 맞지 않다", detail=[why1, why2])
        prev_sha, start_sha = sha256(sb), sd["start_sha256"]
    k = len(begins) + 1
    # 4. 호출 기록 (무엇을 관측하기 전에)
    begin = {"kind": K_BEGIN, "step": step, "name": name, "k": k, "utc": utc(), "epoch": time.time(), "pid": os.getpid(),
             "launch_epoch": le, "prev_sha256": prev_sha, "slice_s": WAIT_SLICE_S}
    begin_bytes = dump(begin)
    try:
        publish(watch_part(ev, name, k, "begin"), begin_bytes)
    except FileExistsError:
        return say("unknown", 16, why=f"호출 {k} 를 다른 감시가 먼저 가졌다 (소유권)")
    except OSError as e:
        return say("publish_failed", 19, observed="begin", error=f"{e.__class__.__name__}: {e}"[:300])
    begin_sha = sha256(begin_bytes)
    try:
        state, code, fields = observe_return(step, p, name, le, begin_sha, start_sha, begin["epoch"] + WAIT_SLICE_S)
    except Exception as e:  # noqa: BLE001 — 관측 중 예상 밖 예외는 끝 상태 watch_error
        state, code, fields = "watch_error", 21, {"error": f"{e.__class__.__name__}: {e}"[:300]}
    kind, target = (K_SLICE, watch_part(ev, name, k, "slice")) if state == "continue" else (K_WATCH, p["watch.json"])
    doc = {"kind": kind, "step": step, "name": name, "k": k, "state": state, "begin_sha256": begin_sha, "utc": utc(), **fields}
    try:
        publish(target, dump(doc))
    except Exception as e:  # noqa: BLE001 — 관측했으나 기록을 게시하지 못함 (부분 임시 파일은 그대로)
        return say("publish_failed", 19, observed=state, error=f"{e.__class__.__name__}: {e}"[:300], record=doc)
    if state == "published":
        return say(state, code, wrapper_state=wrapper_exit(fields.get("wrapper_pid")), **fields)
    return say(state, code, **fields)


# ---------------------------------------------------------------- observe (읽기 · 기록 하나)
def observe(step: str, ev: Path, rnd: str) -> int:
    p, name = names(ev, step), STEPS[step]
    outp = ev / f"{name}.leftover_{rnd}.json"
    if os.path.lexists(outp):
        raise Refusal(f"이미 있다: {outp}")
    sid, sid_error = None, None
    _, st, why = load(p["outer_start.json"])
    if st is None or st.get("kind") != K_START:
        sid_error = f"시작 기록 없음 · 묘비 · 못 읽음: {why or (st or {}).get('kind')}"
    elif not is_int(st.get("sid")) or st["sid"] <= 1:
        sid_error = f"sid 가 1 보다 큰 정수가 아니다: {st.get('sid')!r}"
    else:
        sid = st["sid"]
    markers = [f"pycache_prefix={WORK / 'pycache' / name}".encode(), str(ev).encode()]
    skip = ancestors()
    rows, errors = [], []
    for d in sorted((x for x in PROC.iterdir() if x.name.isdigit()), key=lambda x: int(x.name)):
        pid = int(d.name)
        if pid in skip:
            continue
        try:
            stf = stat_fields(pid)
            argv = (d / "cmdline").read_bytes().split(b"\0")
        except (FileNotFoundError, ProcessLookupError):
            continue  # 관측 사이에 끝난 프로세스
        except (OSError, ValueError, IndexError) as e:
            errors.append({"pid": pid, "type": e.__class__.__name__, "message": str(e)[:200]})
            continue
        why_m = (["sid"] if sid is not None and stf["sid"] == sid else []) + \
                [f"marker{i}" for i, m in enumerate(markers) if any(m in a for a in argv)]
        if why_m:
            rows.append({"pid": pid, **stf, "matched": why_m, "argv": [a.decode("utf-8", "replace")[:300] for a in argv if a][:40]})
    alive = [r for r in rows if r["state"] != "Z"]
    write_new(outp, dump({"kind": "REIL_E113_LEFTOVER", "step": step, "round": rnd, "utc": utc(), "sid": sid, "sid_error": sid_error,
                          "markers": [m.decode() for m in markers], "skipped_self_and_ancestors": sorted(skip), "rows": rows,
                          "alive_count": len(alive), "errors": errors}))
    print(json.dumps({"step": step, "round": rnd, "rows": len(rows), "alive": len(alive), "errors": len(errors), "sid_error": sid_error},
                     ensure_ascii=False))
    return 0 if not alive and not errors and sid_error is None else 1


# ---------------------------------------------------------------- kill (R1)
def kill(step: str, ev: Path) -> int:
    name = STEPS[step]
    src, outp = ev / f"{name}.leftover_1.json", ev / f"{name}.kill.json"
    if os.path.lexists(outp):
        raise Refusal(f"이미 있다: {outp}")
    raw, obs, why = load(src)
    if obs is None:
        raise Refusal(f"잔류 관측 1 을 읽지 못함: {why}")
    skip = ancestors()
    own = {os.getpgid(0)}
    for a in skip:
        try:
            own.add(stat_fields(a)["pgid"])
        except (OSError, ValueError, IndexError):
            pass
    groups = {}
    for r in obs.get("rows") or []:
        if r.get("state") != "Z":
            groups.setdefault(int(r["pgid"]), []).append(r)
    results = []
    for pgid, members in sorted(groups.items()):
        if pgid <= 1 or pgid in own:
            results.append({"pgid": pgid, "action": "skip", "why": "1 이하 · 자기 · 조상의 그룹"})
            continue
        same = None
        for m in members:
            try:
                stf = stat_fields(int(m["pid"]))
            except (OSError, ValueError, IndexError):
                continue
            if stf["starttime"] == m.get("starttime") and stf["pgid"] == pgid:
                same = int(m["pid"])
                break
        if same is None:
            results.append({"pgid": pgid, "action": "skip", "why": "관측한 구성원이 없거나 시작 시각 · 그룹이 바뀌었다"})
            continue
        try:
            os.killpg(pgid, signal.SIGKILL)
            results.append({"pgid": pgid, "action": "SIGKILL", "ok": True, "verified_pid": same})
        except OSError as e:
            results.append({"pgid": pgid, "action": "SIGKILL", "ok": False, "verified_pid": same, "type": e.__class__.__name__,
                            "message": str(e)[:200]})
    write_new(outp, dump({"kind": "REIL_E113_KILL", "step": step, "utc": utc(), "source": {"path": str(src), "sha256": sha256(raw)},
                          "results": results}))
    print(json.dumps({"step": step, "groups": len(groups), "results": [r["action"] for r in results]}, ensure_ascii=False))
    return 0


# ---------------------------------------------------------------- freeze (F3)
def freeze(step: str, ev: Path) -> int:
    name = STEPS[step]
    dst, man = ev / f"frozen_{name}", ev / f"frozen_{name}.json"
    if os.path.lexists(dst) or os.path.lexists(man) or os.path.lexists(man.with_name(man.name + ".tmp")):
        raise Refusal(f"이미 있다: {dst} 또는 {man}")
    p = names(ev, step)
    files = [p[k] for k in LAUNCHER_FILES + OUTER_FILES + SHELL_FILES + WATCH]
    files += sorted(x for x in ev.glob(f"{name}.watch_*") if x not in files)
    if step == "identity":
        files.append(ev / "03_identity.json")
    if step == "run" and (ev / "run").is_dir() and not (ev / "run").is_symlink():
        files += sorted(x for x in (ev / "run").rglob("*") if x.is_file() or x.is_symlink())
    try:
        dst.mkdir()
    except OSError as e:
        print(json.dumps({"step": step, "manifest_written": False, "phase": "mkdir", "error": f"{e.__class__.__name__}: {e}"[:300]},
                         ensure_ascii=False))
        return 5
    rows = []
    for f in files:
        rel = f.relative_to(ev)
        t = utc()
        b, why = read_once(f)
        if b is None:
            rows.append({"path": str(rel), "state": "not_read", "why": why, "read_utc": t})
            continue
        row = {"path": str(rel), "bytes": len(b), "sha256": sha256(b), "read_utc": t}
        try:
            target = dst / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            write_new(target, b)
            row["state"] = "copied"
        except Exception as e:  # noqa: BLE001 — 파일마다 남기고 다음 파일로 (부분 사본은 지우지 않는다)
            row.update(state="copy_failed", why=f"{e.__class__.__name__}: {e}"[:300])
        rows.append(row)
    counts = {s: sum(1 for r in rows if r["state"] == s) for s in ("copied", "copy_failed", "not_read")}
    doc = {"kind": "REIL_E113_FROZEN", "step": step, "utc": utc(), "rows": rows, "counts": counts,
           "note": "읽은 범위의 고정 관측 사본 — 원본은 그대로 · 여러 파일의 원자적 · 동시 시점이 아니다 · 한 번 읽기는 같은 버퍼 결속일 뿐"}
    try:
        publish(man, dump(doc))
    except Exception as e:  # noqa: BLE001 — 목록을 게시하지 못함: 도구 반환으로만 남는다
        print(json.dumps({"step": step, "manifest_written": False, "phase": "manifest", "error": f"{e.__class__.__name__}: {e}"[:300],
                          **counts}, ensure_ascii=False))
        return 5
    print(json.dumps({"step": step, "manifest_written": True, **counts}, ensure_ascii=False))
    return 0


# ---------------------------------------------------------------- check (커밋 전 공개 검사 · 쓰기 0)
def staged(cached: str, index: str):
    """git 이 쓴 두 출력 파일 → (staged 이름 집합, {경로: (blob, stage)}) 또는 사유."""
    cb, why1 = read_once(Path(cached))
    ib, why2 = read_once(Path(index))
    if cb is None or ib is None:
        return None, None, f"git 출력을 읽지 못함: {why1} · {why2}"
    try:
        cached_names = sorted(x.decode("utf-8") for x in cb.split(b"\0") if x)
        entries = {}
        for e in (x for x in ib.split(b"\0") if x):
            meta, tab, path = e.partition(b"\t")
            mode, blob, stage = meta.decode("ascii").split(" ")
            if not tab or path.decode("utf-8") in entries:
                raise ValueError(f"index 항목 형식: {e[:80]!r}")
            entries[path.decode("utf-8")] = (blob, stage)
    except (ValueError, UnicodeDecodeError) as e:
        return None, None, f"git 출력 형식: {e}"[:300]
    return cached_names, entries, ""


def check(ev: Path, cached: str, index: str, paths: list) -> int:
    if not paths or (cached == "-") != (index == "-"):
        raise Refusal("check 는 <cached|-> <index|-> <경로 하나 이상> — cached · index 는 둘 다 주거나 둘 다 - 이다")
    rows, bad, total, rels = [], [], 0, []
    for a in paths:
        f = Path(a)
        if not f.is_absolute() or ev not in f.parents:
            raise Refusal(f"증거 폴더 밖의 경로: {a}")
        rel = str(f.relative_to(REPO))
        if rel in rels:
            raise Refusal(f"같은 경로가 두 번: {a}")
        rels.append(rel)
        b, why = read_once(f)
        if b is None:
            bad.append({"path": rel, "why": why})
            continue
        h = sha256(b)
        fixed = f.parent == ev and f.name in FIXED_COPIES
        why_b = (["원자료 sha"] if h in DATA_SHA256 else []) + (["확장자"] if f.suffix == ".xlsx" or (f.suffix == ".py" and not fixed) else []) \
            + (["50 MiB 초과"] if len(b) > FILE_MAX else []) + (["URL 계정 형태"] if URL_ACCOUNT.search(b) else [])
        if why_b:
            bad.append({"path": rel, "why": why_b})
        rows.append({"path": rel, "bytes": len(b), "sha256": h, "blob": blob_id(b)})
        total += len(b)
    if total > COMMIT_MAX:
        bad.append({"path": "(합)", "why": f"{total} B > 100 MiB"})
    out = {"files": len(rels), "total_bytes": total, "bad": bad, "staged_checked": cached != "-", "rows": rows}
    if cached != "-":
        cached_names, entries, why = staged(cached, index)
        if cached_names is None:
            bad.append({"path": "(git 출력)", "why": why})
        else:
            out["set_equal"] = cached_names == sorted(rels)
            out["blob_equal"] = len(rows) == len(rels) and sorted(entries) == sorted(rels) and all(
                entries.get(r["path"]) == (r["blob"], "0") for r in rows)
            if not out["set_equal"]:
                bad.append({"path": "(staged 집합)", "why": {"staged_only": sorted(set(cached_names) - set(rels)),
                                                           "listed_only": sorted(set(rels) - set(cached_names))}})
            if not out["blob_equal"]:
                bad.append({"path": "(staged blob)", "why": "staged blob ≠ 검사한 버퍼의 blob (또는 stage ≠ 0)"})
    print(json.dumps(out, ensure_ascii=False))
    return 0 if not bad else 1


# ---------------------------------------------------------------- main
def evidence(arg: str) -> Path:
    ev = Path(arg)
    if ev.parent != BMS / "evidence" or not EVIDENCE_NAME.match(ev.name) or ev.is_symlink() or not ev.is_dir():
        raise Refusal(f"증거 폴더 규칙 밖: {arg}")
    me = Path(__file__)
    if me.is_symlink() or me.resolve() != (ev / "00_outer.py").resolve():
        raise Refusal(f"이 파일이 그 증거 폴더의 00_outer.py 가 아니다: {me}")
    return ev


def main(argv=None) -> int:
    a = list(sys.argv[1:] if argv is None else argv)
    try:
        if a[:1] == ["check"]:
            if len(a) < 5:
                raise Refusal(f"인자 — check <E> <cached|-> <index|-> <경로…>: {a}")
            return check(evidence(a[1]), a[2], a[3], a[4:])
        if len(a) < 3 or a[0] not in MODES or a[1] not in STEPS:
            raise Refusal(f"인자 — <{'|'.join(MODES)}> <{'|'.join(STEPS)}> <E> …: {a}")
        mode, step, ev = a[0], a[1], evidence(a[2])
        if mode == "start":
            if len(a) != 4 or not SECTION.match(a[3]):
                raise Refusal(f"start 는 승인 절 §NN 하나를 더 받는다: {a[3:]}")
            return start(step, ev, a[3])
        if mode == "observe":
            if len(a) != 4 or a[3] not in ("1", "2"):
                raise Refusal(f"observe 는 차례 1 또는 2 를 더 받는다: {a[3:]}")
            return observe(step, ev, a[3])
        if len(a) != 3:
            raise Refusal(f"{mode} 는 인자 셋이다: {a}")
        return {"wait": wait, "kill": kill, "freeze": freeze}[mode](step, ev)
    except Refusal as e:
        sys.stderr.write(f"거부: {e}\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
