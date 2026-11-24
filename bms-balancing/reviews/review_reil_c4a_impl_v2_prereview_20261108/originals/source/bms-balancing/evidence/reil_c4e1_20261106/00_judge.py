"""REIL C4-E · E1-1–3 판정기 초안 v2 (2026-11-04 · 정정 범위안 v2 §2-4 · 사용자 채택 §109) — 고정 뒤 `<E>/00_judge.py` 로 복사해 쓴다.

python -I <E>/00_judge.py <E> <identity|fetch|run> <§NN>

읽기 (그 단계만 · 파일마다 한 번 · 같은 버퍼에서 sha 와 내용): `00_overall.json` · `<name>.launch_epoch.txt` · 외곽 기록 (`outer_start.json` ·
`outer_end.json` · `outer_rc.txt` · `outer_stdout.txt` · `outer_stderr.txt` · `wrapper_output.txt` · 오류 / 임시 이름의 부재) · 감시 기록
(`watch_<k>.begin.json` · `watch_<k>.slice.json` · `watch.json` · 임시의 부재) · 잔류 관측 `<name>.leftover_1.json` (`kill.json` · `leftover_2.json` ·
`frozen_<name>` 은 부재만) · launcher meta · identity 면 `03_identity.json` · run 이면 자식 `05_run.stdout.log` 의 마지막 JSON 과 `<E>/run/` 의 파일 이름.
쓰기 = `<name>.judge.json` 배타 생성 하나. 시험 · Git · 네트워크 · 하위 프로세스 · 신호 0. 환경 변수를 읽지 않는다 (`os` 를 import 하지 않는다).

항목마다 id · ok · 관측값. verdict = 모든 항목이 참이면 MATCH, 아니면 STOP. 필요한 파일 · 키가 없으면 그 항목은 거짓 ("미확인"). 누락과 명시적 null 을
나눈다 — null 이어야 하는 키는 셋뿐이고 키가 있어야 한다 (`meta.first_error` · `leftover_1.sid_error` · `watch_1.begin.prev_sha256`). 정상 수용의 시각은
`watch.json` 의 `observed_epoch` ≤ 시작 기록의 `deadline_epoch` 하나뿐이다 (끝 기록의 시각은 순서 검사에만). run 은 실행 유효성과 실험 결과
(자식의 `final.complete` · `final.E3a` · `final.c4a_gate`) 를 따로 적는다 — launcher 단계 판정도 `final.complete` 를 쓰므로 둘은 독립이 아니다.

반환 0 = MATCH · 1 = STOP · 2 = 의도된 거부 (폴더 이름 규칙 밖 · 판정기가 그 폴더 밖 · 단계 · 승인 절 형식 · 출력이 이미 있음 — 아무것도 쓰지 않음).
판정 중 예외는 거짓 항목 `judge.exception` 으로 남기고 기록은 쓴다.
"""
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

BMS = Path("/home/user/Yonghoon-DEM-DFT/bms-balancing")
LAUNCHER = BMS / "scripts" / "reil_c4e1_launch.py"
LAUNCHER_SHA256 = "2c70712381aec657f81c8e72c85e8c06e654364aefe9e38e5254ecfece9e4ebf"
REQUEST = "docs/REIL_C4E_E1_0B_APPROVAL_REQUEST_20261030.md"
PY = "/usr/bin/python3.11"
STEPS = {"identity": "03_identity", "fetch": "04_fetch", "run": "05_run"}
ALLOW_S = {"identity": 900.0, "fetch": 1800.0, "run": 12600.0}
MAX_CALLS = {"identity": 1, "fetch": 1, "run": 2}
START_WAIT_S = 60.0
TOTAL_S = 21600
RESERVE_S = 1800
EVIDENCE_NAME = re.compile(r"^reil_c4e1_20[0-9]{6}$")
SECTION = re.compile(r"^§[0-9]{2,3}$")
HEX40 = re.compile(r"[0-9a-f]{40}")
EPOCH_FORMAT = re.compile(rb"[0-9]{10}\n")
DATA_FILES = {"LFP_Data.xlsx": {"bytes": 10_841_377, "sha256": "fd50e09542be7adb2270963d65a6e7b5ccae1473a512f68462c2dd419d620ee1"},
              "util_LFP.py": {"bytes": 33_754, "sha256": "3c19e45ef8a64ce67cda1f623551e758d4c0f67086bbae02b978428d78de1c76"}}
RUN_FILES = ("AGGREGATE.json", "END_RECORD.json", "HEADER.json", "IDENTITY.json", "OPERATION.json", "RESOURCES.json", "ROWS.json",
             "RULE.json")
STAGE_TERMS = ("precheck_ok", "child_ok", "rc_0", "timeout_false", "postcheck_ok")
ABSENT = ("outer_error.json", "outer_start.json.tmp", "outer_end.json.tmp", "outer_rc.txt.tmp", "outer_error.json.tmp", "kill.json",
          "leftover_2.json")
K_START, K_END, K_BEGIN, K_SLICE, K_WATCH, K_OVERALL = ("REIL_E113_OUTER_START", "REIL_E113_OUTER_END", "REIL_E113_WATCH_BEGIN",
                                                        "REIL_E113_WATCH_SLICE", "REIL_E113_WATCH", "REIL_E113_OVERALL")


class Refusal(Exception):
    """의도된 거부 — 아무것도 쓰지 않고 반환 2."""


def utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def is_int(x) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)


def is_num(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool) and x == x and abs(x) != float("inf")


def null(d, k) -> bool:
    """키가 있고 값이 null — 키가 없으면 거짓 (C1)."""
    return isinstance(d, dict) and k in d and d[k] is None


def last_json(text: str):
    lines = [x for x in text.splitlines() if x.strip()]
    try:
        doc = json.loads(lines[-1]) if lines else None
    except ValueError:
        return None
    return doc if isinstance(doc, dict) else None


def numbers(ev: Path, name: str, part: str) -> list:
    pat = re.compile(rf"{re.escape(name)}\.watch_([1-9][0-9]*)\.{part}\.json")
    return sorted(int(m.group(1)) for m in (pat.fullmatch(x.name) for x in ev.iterdir()) if m)


def judge(ev: Path, step: str, section: str) -> dict:
    name = STEPS[step]
    items, inputs, cache = [], {}, {}

    def item(iid, ok, observed=None):
        items.append({"id": iid, "ok": bool(ok), "observed": observed})

    def read(rel):
        """파일마다 한 번 — 같은 버퍼를 다시 쓴다."""
        if rel in cache:
            return cache[rel]
        p, b = ev / rel, None
        try:
            if not p.is_symlink() and p.is_file():
                b = p.read_bytes()
        except OSError:
            b = None
        cache[rel] = b
        inputs[rel] = None if b is None else {"sha256": sha256(b), "bytes": len(b)}
        return b

    def jload(rel):
        b = read(rel)
        if b is None:
            return None
        try:
            doc = json.loads(b)
        except ValueError:
            return None
        return doc if isinstance(doc, dict) else None

    def sha_of(rel):
        b = read(rel)
        return None if b is None else sha256(b)

    def absent(rel):
        q = ev / rel
        return not q.exists() and not q.is_symlink()

    # 전체 기한
    ov = jload("00_overall.json")
    o = ov or {}
    ov_ok = (ov is not None and o.get("kind") == K_OVERALL and o.get("section") == section and is_int(o.get("T_a"))
             and is_int(o.get("T_end")) and o["T_end"] == o["T_a"] + TOTAL_S and is_int(o.get("R")) and o["R"] == RESERVE_S)
    item("overall.values", ov_ok, {k: o.get(k) for k in ("kind", "section", "T_a", "T_end", "R")})
    # 기산점
    lb = read(f"{name}.launch_epoch.txt")
    le = int(lb) if lb is not None and EPOCH_FORMAT.fullmatch(lb) else None
    item("launch.epoch", le is not None and ov_ok and o["T_a"] <= le, [None if lb is None else lb[:20].decode("ascii", "replace"), o.get("T_a")])
    # 시작 기록 (묘비면 거짓)
    start = jload(f"{name}.outer_start.json")
    s = start or {}
    start_sha = sha_of(f"{name}.outer_start.json")
    want_argv = [PY, "-I", str(LAUNCHER), step, "--evidence", str(ev), "--approval-section", section]
    item("outer.start_kind_step", s.get("kind") == K_START and s.get("step") == step and s.get("name") == name and s.get("section") == section,
         [s.get("kind"), s.get("step"), s.get("name"), s.get("section")])
    item("outer.start_argv", s.get("argv") == want_argv, s.get("argv"))
    item("outer.start_launcher", (s.get("launcher") or {}).get("sha256") == LAUNCHER_SHA256, (s.get("launcher") or {}).get("sha256"))
    item("outer.start_session_leader", is_int(s.get("pid")) and s.get("pid") == s.get("sid") == s.get("pgid"),
         [s.get("pid"), s.get("sid"), s.get("pgid")])
    item("outer.start_allow", s.get("allow_s") == ALLOW_S[step], s.get("allow_s"))
    ep, dl = s.get("epoch"), s.get("deadline_epoch")
    item("outer.start_deadline", is_num(ep) and is_num(dl) and dl == ep + ALLOW_S[step], [ep, dl])
    item("outer.start_window", is_num(ep) and le is not None and is_int(s.get("launch_epoch")) and s["launch_epoch"] == le
         and 0.0 <= ep - le <= START_WAIT_S, [s.get("launch_epoch"), le, None if not (is_num(ep) and le is not None) else ep - le])
    ov_sha = sha_of("00_overall.json")
    item("outer.start_budget", is_num(dl) and ov_ok and dl <= o["T_end"] - o["R"] and s.get("T_end") == o.get("T_end")
         and s.get("R") == o.get("R") and ov_sha is not None and s.get("overall_sha256") == ov_sha,
         [dl, o.get("T_end"), o.get("R"), s.get("overall_sha256"), ov_sha])
    # 끝 기록 · 반환
    rc = read(f"{name}.outer_rc.txt")
    item("outer.rc", rc == b"0\n", None if rc is None else rc[:20].hex())
    end = jload(f"{name}.outer_end.json")
    e = end or {}
    t_exit, t_snap = e.get("launcher_exit_epoch"), e.get("end_snapshot_epoch")
    item("outer.end", end is not None and e.get("kind") == K_END and e.get("step") == step and e.get("name") == name
         and start_sha is not None and e.get("start_sha256") == start_sha and is_int(e.get("rc")) and e["rc"] == 0
         and is_num(ep) and is_num(t_exit) and is_num(t_snap) and ep <= t_exit <= t_snap,
         {k: e.get(k) for k in ("kind", "rc", "start_sha256", "launcher_exit_epoch", "end_snapshot_epoch")})
    for k in ABSENT:
        item(f"outer.absent.{k}", absent(f"{name}.{k}"))
    for k in ("outer_stderr.txt", "wrapper_output.txt"):
        b = read(f"{name}.{k}")
        item(f"outer.empty.{k}", b == b"", None if b is None else len(b))
    so = read(f"{name}.outer_stdout.txt")
    summary = last_json(so.decode("utf-8", "replace")) if so is not None else None
    item("outer.stdout_summary", summary == {"step": step, "launched": True, "complete": True, "rc": 0, "timed_out": False, "errors": 0},
         summary)
    # 감시 사슬 — begin_1 … begin_n · slice_1 … slice_(n−1) · watch.json (published)
    begins, slices = numbers(ev, name, "begin"), numbers(ev, name, "slice")
    n = len(begins)
    item("watch.calls", 1 <= n <= MAX_CALLS[step] and begins == list(range(1, n + 1)) and slices == list(range(1, n)),
         {"begins": begins, "slices": slices, "max": MAX_CALLS[step]})
    prev, chain_ok, chain_obs = None, n >= 1, []
    for k in begins:
        bd = jload(f"{name}.watch_{k}.begin.json")
        okk = (bd is not None and bd.get("kind") == K_BEGIN and bd.get("step") == step and bd.get("k") == k and "prev_sha256" in bd
               and bd["prev_sha256"] == prev and is_num(bd.get("epoch")))
        if k == 1:
            okk = okk and null(bd, "prev_sha256") and le is not None and bd["epoch"] >= le
        if k < n:
            sd = jload(f"{name}.watch_{k}.slice.json") or {}
            okk = (okk and sd.get("kind") == K_SLICE and sd.get("k") == k and sd.get("state") == "continue"
                   and sd.get("begin_sha256") == sha_of(f"{name}.watch_{k}.begin.json") and start_sha is not None
                   and sd.get("start_sha256") == start_sha)
            prev = sha_of(f"{name}.watch_{k}.slice.json")
        chain_ok = chain_ok and bool(okk)
        chain_obs.append({"k": k, "ok": bool(okk)})
    item("watch.chain", chain_ok, chain_obs)
    wd = jload(f"{name}.watch.json")
    w = wd or {}
    t_obs, w_dl = w.get("observed_epoch"), w.get("deadline_epoch")
    last_begin = sha_of(f"{name}.watch_{n}.begin.json") if n >= 1 else None
    end_sha = sha_of(f"{name}.outer_end.json")
    item("watch.published", wd is not None and w.get("kind") == K_WATCH and w.get("step") == step and w.get("state") == "published"
         and w.get("k") == n and last_begin is not None and w.get("begin_sha256") == last_begin and start_sha is not None
         and w.get("start_sha256") == start_sha and end_sha is not None and w.get("end_sha256") == end_sha and is_int(w.get("rc"))
         and w["rc"] == 0 and is_num(t_obs) and is_num(w_dl) and is_num(dl) and w_dl == dl and is_num(t_snap) and t_snap <= t_obs <= dl,
         {k: w.get(k) for k in ("kind", "state", "k", "rc", "observed_epoch", "deadline_epoch")})
    tmps = sorted(x.name for x in ev.glob(f"{name}.watch*.tmp"))
    item("watch.no_tmp", tmps == [], tmps)
    # 잔류 관측
    left = jload(f"{name}.leftover_1.json")
    lf = left or {}
    item("leftover.1", left is not None and lf.get("alive_count") == 0 and lf.get("errors") == [] and is_int(lf.get("sid"))
         and lf["sid"] > 1 and lf["sid"] == s.get("sid") and null(lf, "sid_error"),
         [lf.get("alive_count"), len(lf.get("errors") or []), lf.get("sid"), lf.get("sid_error", "(키 없음)")])
    item("leftover.not_frozen", absent(f"frozen_{name}.json") and absent(f"frozen_{name}"))
    # launcher meta (F1 — v6 의 실제 필드)
    m = jload(f"{name}.meta.json")
    item("meta.present", m is not None)
    m = m or {}
    child = m.get("child") if isinstance(m.get("child"), dict) else {}
    group = child.get("group") if isinstance(child.get("group"), dict) else {}
    stage = m.get("stage") if isinstance(m.get("stage"), dict) else {}
    post = m.get("postcheck") if isinstance(m.get("postcheck"), dict) else {}
    records = m.get("records") if isinstance(m.get("records"), dict) else {}
    item("meta.identity", m.get("step") == step and m.get("name") == name and m.get("request") == REQUEST
         and m.get("approval_section") == section, [m.get("step"), m.get("name"), m.get("request"), m.get("approval_section")])
    item("meta.launcher", (m.get("launcher") or {}).get("sha256") == LAUNCHER_SHA256
         and (m.get("launcher") or {}).get("path") == str(LAUNCHER), m.get("launcher"))
    item("meta.stage", stage.get("complete") is True and all((stage.get("terms") or {}).get(t) is True for t in STAGE_TERMS), stage)
    item("meta.precheck_ok", m.get("precheck_ok") is True, m.get("precheck_ok"))
    item("meta.postcheck", post.get("ok") is True and post.get("problems") == [], post.get("problems"))
    item("meta.errors", m.get("errors") == [] and null(m, "first_error"), [m.get("errors"), m.get("first_error", "(키 없음)")])
    item("meta.child_started", child.get("started") is True and m.get("launched") is True, [child.get("started"), m.get("launched")])
    item("meta.child_rc", child.get("rc") == 0 and child.get("timed_out") is False, [child.get("rc"), child.get("timed_out")])
    item("meta.child_group_empty", group.get("status") == "empty", group.get("status"))
    item("meta.child_deadline", child.get("deadline_hit") is False, child.get("deadline_hit"))
    item("meta.child_errors", child.get("errors") == [], child.get("errors"))
    heads = [(records.get(k) or {}).get("out") for k in ("head_start", "head_end")]
    item("meta.head_unchanged", all(isinstance(h, str) and HEX40.fullmatch(h) for h in heads) and heads[0] == heads[1], heads)
    cr = m.get("child_result") if isinstance(m.get("child_result"), dict) else {}
    out = {"verdict": None, "step": step, "name": name}
    if step == "identity":
        item("identity.child_ok", cr.get("ok") is True, cr)
        item("identity.helper_output", read("03_identity.json") is not None)
    if step == "fetch":
        data = post.get("data") if isinstance(post.get("data"), dict) else {}
        item("fetch.data", all((data.get(k) or {}).get("ok") is True and (data.get(k) or {}).get("sha256") == v["sha256"]
                               and (data.get(k) or {}).get("bytes") == v["bytes"] for k, v in DATA_FILES.items()),
             {k: {kk: (data.get(k) or {}).get(kk) for kk in ("ok", "sha256", "bytes")} for k in DATA_FILES})
        item("fetch.child_ok", cr.get("ok") is True, cr)
    if step == "run":
        cs = read(f"{name}.stdout.log")
        doc = last_json(cs.decode("utf-8", "replace")) if cs is not None else None
        fin = (doc or {}).get("final") if isinstance((doc or {}).get("final"), dict) else {}
        result = {"ok": (doc or {}).get("ok"), "final.complete": fin.get("complete"), "final.E3a": fin.get("E3a"),
                  "final.c4a_gate": fin.get("c4a_gate"), "final.record_state": fin.get("record_state")}
        item("run.child_ok", cr.get("ok") is True and cr.get("final_complete") is True and cr.get("E3a") == "COMPLETE", cr)
        item("run.experimental_result", doc is not None and doc.get("ok") is True and fin.get("complete") is True
             and fin.get("E3a") == "COMPLETE" and fin.get("c4a_gate") is True, result)
        rd = ev / "run"
        got = sorted(str(x.relative_to(rd)) for x in rd.rglob("*") if x.is_file() or x.is_symlink()) \
            if rd.is_dir() and not rd.is_symlink() else None
        item("run.output_files", got == sorted(RUN_FILES), got)
        out["experimental_result"] = result
    validity = [i for i in items if not i["id"].startswith("run.experimental")]
    out["execution_validity"] = all(i["ok"] for i in validity)
    out["items"], out["inputs"] = items, inputs
    return out


def main(argv=None) -> int:
    a = list(sys.argv[1:] if argv is None else argv)
    me = Path(__file__)
    try:
        if len(a) != 3 or a[1] not in STEPS or not SECTION.match(a[2]):
            raise Refusal(f"인자 — <E> <{'|'.join(STEPS)}> <§NN>: {a}")
        ev = Path(a[0])
        if ev.parent != BMS / "evidence" or not EVIDENCE_NAME.match(ev.name) or ev.is_symlink() or not ev.is_dir():
            raise Refusal(f"증거 폴더 규칙 밖: {ev}")
        if me.is_symlink() or me.resolve() != (ev / "00_judge.py").resolve():
            raise Refusal(f"이 파일이 그 증거 폴더의 00_judge.py 가 아니다: {me}")
        outp = ev / f"{STEPS[a[1]]}.judge.json"
        if outp.exists() or outp.is_symlink():
            raise Refusal(f"이미 있다: {outp}")
    except Refusal as e:
        sys.stderr.write(f"거부: {e}\n")
        return 2
    try:
        res = judge(ev, a[1], a[2])
    except Exception as e:  # noqa: BLE001 — 판정 중 예외도 기록한다
        res = {"step": a[1], "name": STEPS[a[1]], "items": [{"id": "judge.exception", "ok": False,
                                                              "observed": f"{e.__class__.__name__}: {e}"[:500]}], "inputs": {}}
    failed = [i["id"] for i in res["items"] if not i["ok"]]
    res["verdict"] = "MATCH" if not failed else "STOP"
    res.update(kind="REIL_E113_JUDGE", utc=utc(), section=a[2], failed=failed,
               judge={"path": str(me.resolve()), "sha256": sha256(me.read_bytes()), "bytes": me.stat().st_size})
    with open(outp, "x", encoding="utf-8") as f:
        f.write(json.dumps(res, ensure_ascii=False, indent=1, sort_keys=True) + "\n")
    print(json.dumps({"written": str(outp), "verdict": res["verdict"], "checks": len(res["items"]), "failed": failed}, ensure_ascii=False))
    return 0 if res["verdict"] == "MATCH" else 1


if __name__ == "__main__":
    sys.exit(main())
