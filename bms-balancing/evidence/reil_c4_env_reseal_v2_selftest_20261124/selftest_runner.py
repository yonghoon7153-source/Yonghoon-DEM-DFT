"""실행기 · 바깥 하네스 샌드박스 자체 시험 (2026-11-24 · 원장 §138) — 진짜 단계 (venv · pip · 내려받기 · 설치 · emit · check) 는 0.

임시 git 저장소 (샌드박스) 에 실행기 · 하네스 · 대조기 사본 + 가짜 요청서 · 원장 (승인 블록) 을 두고, 단계 argv 를 가짜 명령으로 바꾼 계획으로
하네스 → 실행기를 끝까지 돌린다. S0 의 읽기 대조 (interpreter · dpkg-query · dpkg -V · ensurepip 묶음 · 소스 sha · 여유 디스크) 는 진짜
시스템을 **읽기만** 한다. 자식 env 는 최소 env (PATH · HOME · LANG) + 가짜 시험 값뿐이다 — 진짜 환경 변수 값을 파일에 옮기지 않는다.
실행: 저장소 뿌리에서 `/usr/bin/python3.11 -I -B bms-balancing/evidence/reil_c4_env_reseal_v2_selftest_20261124/selftest_runner.py`.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
RUNNER = REPO / "bms-balancing/scripts/reil_c4_env_reseal_run.py"
HARNESS = REPO / "bms-balancing/scripts/reil_c4_env_reseal_harness.py"
CHECKER = REPO / "bms-balancing/scripts/reil_c4_env_reseal_check.py"
OCT_E = REPO / "bms-balancing/evidence/reil_c4_env_20261013"
PY = "/usr/bin/python3.11"
FAKE_TOKEN = "sandbox-fake-token-0123456789"
RESULTS = []


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


H = load(HARNESS, "harness_under_test")
PROD = load(RUNNER, "runner_template").production_plan()


def case(name: str, ok: bool, detail="") -> None:
    RESULTS.append((name, bool(ok)))
    print(f"{'PASS' if ok else 'FAIL'} {name}" + (f" — {detail}" if detail and not ok else ""), flush=True)


def sha(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def git(repo: Path, *a) -> str:
    return subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True, check=True).stdout.strip()


def leftover(marker: str) -> bool:
    return subprocess.run(["pgrep", "-f", marker], capture_output=True).returncode == 0


WRAPPER = '''import importlib.util, json, sys
from pathlib import Path
plan = json.loads(Path(__file__).with_name("plan.json").read_text(encoding="utf-8"))
for k in ("repo", "sp", "R", "outer"):
    plan[k] = Path(plan[k])
plan["groups"] = [(g[0], g[1], [tuple(c) for c in g[2]]) for g in plan["groups"]]
spec = importlib.util.spec_from_file_location("runner_copy", plan["repo"] / plan["runner_rel"])
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
sys.exit(m.main(sys.argv[1:], plan=plan))
'''


def sandbox(name: str, *, approval="ok", over=None, allot=None, total_s=180.0, s10_allot=60.0, hook=False, hold=False,
            env_drop=(), harness_limit=None, fake_runner=None) -> dict:
    root = Path(tempfile.mkdtemp(prefix=f"{name}_", dir=ROOT))
    repo, sp = root / "repo", root / "sp"
    repo.mkdir()
    sp.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    git(repo, "config", "user.email", "sandbox@example.invalid")
    git(repo, "config", "user.name", "sandbox")

    def put(rel, data: bytes):
        f = repo / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(data)

    put("bms-balancing/scripts/reil_c4_env_reseal_run.py", RUNNER.read_bytes())
    put("bms-balancing/scripts/reil_c4_env_reseal_harness.py", HARNESS.read_bytes())
    put("bms-balancing/scripts/reil_c4_env_reseal_check.py", CHECKER.read_bytes())
    put("bms-balancing/evidence/reil_c4_env_20261013/00_runner.py", (OCT_E / "00_runner.py").read_bytes())
    for sub in ("09_records", "10_test_tool_records"):          # 대조기 bundled 모드가 읽는 10월 원문 (읽기용 링크)
        os.symlink(OCT_E / sub, repo / "bms-balancing/evidence/reil_c4_env_20261013" / sub)
    put("bms-balancing/docs/REQ.md", b"# sandbox request\n")
    put("bms-balancing/docs/REQ_OLD.md", b"# sandbox superseded request (v1 \xec\x9e\x90\xeb\xa6\xac)\n")
    put("bms-balancing/docs/LEDGER.md", b"# sandbox ledger\n\n## \xc2\xa71 something\n")
    put("bms-balancing/protA/a.txt", b"protected tree\n")
    put("bms-balancing/protB.txt", b"protected file\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "request")
    req_commit = git(repo, "rev-parse", "HEAD")
    blk = {"kind": "C4ENV_RESEAL_EXECUTION", "decision": "APPROVED",
           "request": {"path": "bms-balancing/docs/REQ.md", "sha256": sha(repo / "bms-balancing/docs/REQ.md")},
           "request_commit": req_commit, "runner_sha256": sha(RUNNER), "harness_sha256": sha(HARNESS), "checker_sha256": sha(CHECKER),
           "user_text": "sandbox"}
    if approval == "bad_runner_sha":
        blk["runner_sha256"] = "0" * 64
    if approval == "wrong_request":              # 경로 · sha 는 서로 맞지만 승인된 요청서 (plan 의 request_rel) 가 아님
        blk["request"] = {"path": "bms-balancing/docs/REQ_OLD.md", "sha256": sha(repo / "bms-balancing/docs/REQ_OLD.md")}
    block = "\n```c4env-reseal-approval\n" + json.dumps(blk, ensure_ascii=False) + "\n```\n"
    if approval != "missing":
        with open(repo / "bms-balancing/docs/LEDGER.md", "a", encoding="utf-8") as f:
            f.write("\n## §2 승인\n" + block + (block if approval == "two" else ""))
        git(repo, "add", "-A")
        git(repo, "commit", "-q", "-m", "approval")
    if hook:
        h = repo / ".git/hooks/pre-commit"
        h.write_text("#!/bin/sh\nexit 1\n")
        h.chmod(0o755)
    cert = root / "cert.pem"
    cert.write_bytes(b"-----BEGIN CERTIFICATE-----\nsandbox\n-----END CERTIFICATE-----\n")
    environ = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": str(root), "LANG": "C.UTF-8",
               "PIP_CERT": str(cert), "PIP_INDEX_URL": "https://example.invalid/simple", "PIP_CONFIG_FILE": "/etc/should-be-replaced",
               "REQUESTS_CA_BUNDLE": "/x/requests.pem", "CURL_CA_BUNDLE": "/x/curl.pem", "SSL_CERT_FILE": "/x/ssl.pem",
               "SANDBOX_FAKE_TOKEN": FAKE_TOKEN, "https_proxy": "http://proxy.invalid:3128"}
    for k in env_drop:
        environ.pop(k, None)
    R, E_rel, N_rel = sp / "reil_env18", "bms-balancing/evidence/reil_c4_env_SANDBOX", "bms-balancing/reil_c6_rebuild_SANDBOX"
    c = [PY, "-I", "-c"]
    reasons = ["science/evil.pth"] if hold else []
    g = {
        "S1": [("01_venv", c + ["import os,sys; os.makedirs(sys.argv[1])", str(R / "venv")], {}, "0")],
        "S2": [("02_download_science", c + ["import os; print(sorted(os.environ))"], {"PIP_CONFIG_FILE": "/dev/null"}, "PyPI")],
        "S3": [("03_download_test", c + ["pass"], {"PIP_CONFIG_FILE": "/dev/null"}, "PyPI")],
        "S4": [("04a_wheels_science", c + ["pass"], {}, "0"), ("04b_wheels_test", c + ["pass"], {}, "0")],
        "S5": [("05_install_science", c + ["pass"], {"PIP_CONFIG_FILE": "/dev/null"}, "0")],
        "S6": [("06_install_test", c + ["pass"], {"PIP_CONFIG_FILE": "/dev/null"}, "0")],
        "S7": [("07_emit", c + ["import os,sys; os.makedirs(sys.argv[1]); open(sys.argv[1] + '/MANIFEST.json', 'w').write('{}\\n')", N_rel],
                {"PYTHONDONTWRITEBYTECODE": "1"}, "0")],
        "S8": [("08_check", c + ["print('check OK')"], {"PYTHONDONTWRITEBYTECODE": "1"}, "0")],
        "S9": [("09a_records", c + ["import json,os,sys; os.makedirs(sys.argv[1] + '/09_records'); "
                                    "json.dump({'allowed_only': True, 'adoption_hold': " + str(hold) + ", 'adoption_hold_reasons': "
                                    + json.dumps(reasons) + "}, open(sys.argv[1] + '/09a_records.json', 'w'))", E_rel], {}, "0"),
               ("09b_seal", c + ["import json,sys; json.dump({'allowed_only': True}, open(sys.argv[1] + '/09b_seal.json', 'w'))", E_rel], {}, "0")],
    }
    for sid, argv in (over or {}).items():
        for gname, kids in g.items():
            g[gname] = [(k[0], c + argv if k[0] == sid else k[1], k[2], k[3]) for k in kids]
    allots = {k: 10.0 for k in g}
    allots.update(allot or {})
    plan = dict(PROD)
    plan.update({
        "repo": str(repo), "sp": str(sp), "R": str(R), "outer": str(sp / "c4env18_outer"), "E_rel": E_rel, "N_rel": N_rel,
        "ledger_rel": "bms-balancing/docs/LEDGER.md", "request_rel": "bms-balancing/docs/REQ.md", "oct_runner_rel": "bms-balancing/evidence/reil_c4_env_20261013/00_runner.py",
        "guarded": ["bms-balancing/scripts"],
        "protected_trees": {"bms-balancing/protA": git(repo, "rev-parse", "HEAD:bms-balancing/protA")},
        "protected_files": {"bms-balancing/protB.txt": sha(repo / "bms-balancing/protB.txt")},
        "total_s": total_s, "s10_allot": s10_allot,
        "s0": {"allot": 60.0, "bundled": PROD["s0"]["bundled"][:-1] + [E_rel + "/00_bundled_check.json"]},
        "groups": [(k, allots[k], g[k]) for k in ("S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9")],
        "disk_after": ["S2", "S5", "S9"], "environ": environ,
    })
    (root / "plan.json").write_text(json.dumps(plan, ensure_ascii=False, default=str), encoding="utf-8")
    (root / "run_wrapper.py").write_text(fake_runner or WRAPPER, encoding="utf-8")
    cfg = {"repo": repo, "py": PY, "runner_rel": str(root / "run_wrapper.py"), "outer": sp / "c4env18_outer",
           "limits": {"precheck": 90.0, "run": harness_limit or 600.0}, "grace": 2.0}
    return {"root": root, "repo": repo, "sp": sp, "R": R, "E": repo / E_rel, "N": repo / N_rel, "cfg": cfg, "cert": cert,
            "head0": git(repo, "rev-parse", "HEAD")}


def harness(sb: dict, mode: str) -> int:
    devnull = open(os.devnull, "w")
    old = sys.stdout
    sys.stdout = devnull
    try:
        return H.main([mode], cfg=sb["cfg"])
    finally:
        sys.stdout = old
        devnull.close()


def jload(p: Path):
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None


def precheck_problems(sb) -> list:
    out = jload(sb["cfg"]["outer"] / "precheck" / "stdout.log") or {}
    return out.get("problems", ["<stdout 없음>"])


def t_happy():
    sb = sandbox("t1")
    rc_p = harness(sb, "precheck")
    probs = precheck_problems(sb)
    case("T1a precheck → rc 0 · 문제 0 · 실행기 쓰기 0 (기록 폴더 없음)", rc_p == 0 and probs == [] and not sb["E"].exists() and not sb["R"].exists(),
         str(probs)[:300])
    rc = harness(sb, "run")
    after = jload(sb["R"] / "11_after_commit.json") or {}
    end = jload(sb["E"] / "10_end.json") or {}
    outer = jload(sb["cfg"]["outer"] / "run" / "outer_return.json") or {}
    head = git(sb["repo"], "rev-parse", "HEAD")
    msg = git(sb["repo"], "log", "-1", "--format=%s")
    files = git(sb["repo"], "show", "--name-only", "--format=", "HEAD").splitlines()
    case("T1b run → rc 0 · 새 커밋 1 · 그 커밋에는 새 봉인 · 기록만", rc == 0 and head != sb["head0"] and "새 세대 실행 기록" in msg
         and files and all(f.startswith(("bms-balancing/reil_c6_rebuild_SANDBOX/", "bms-balancing/evidence/reil_c4_env_SANDBOX/")) for f in files),
         f"rc={rc} msg={msg} after={after.get('stopped')}")
    case("T1c 10_end.json = PRE_COMMIT · S10 PENDING (커밋 결과를 담지 않음 · ENV18-N2)",
         end.get("phase") == "PRE_COMMIT" and end.get("s10", {}).get("status") == "PENDING" and "commit" not in end)
    case("T1d 11_after_commit.json (커밋 밖) = 커밋 rc 0 · 새 커밋 · HEAD 일치 · S10 · 전체 · 디스크 한도 안 · ok",
         after.get("ok") is True and after["commit"]["rc"] == 0 and after["commit"]["head_after"] == head and after["s10"]["within"]
         and after["total"]["within"] and after["disk"]["within"] and not (sb["E"] / "11_after_commit.json").exists(), str(after)[:300])
    case("T1e 바깥 반환 outer_return.json = rc 0 · 상한 안 · stdout / stderr sha", outer.get("rc") == 0 and outer.get("killed_at_limit") is False
         and outer.get("stdout", {}).get("sha256") == sha(sb["cfg"]["outer"] / "run" / "stdout.log"))
    s2 = (sb["E"] / "02_download_science.stdout.log").read_text()
    meta = jload(sb["E"] / "02_download_science.meta.json") or {}
    bad = [n for n in ("REQUESTS_CA_BUNDLE", "CURL_CA_BUNDLE", "SSL_CERT_FILE", "PIP_INDEX_URL", "SANDBOX_FAKE_TOKEN") if f"'{n}'" in s2]
    case("T1f 자식 env — CA 변수 넷 · PIP_CERT 밖 PIP_* · 비밀 형태 이름 빠짐 · PIP_CERT · PIP_CONFIG_FILE=/dev/null 있음 (ENV18-N1)",
         not bad and "'PIP_CERT'" in s2 and "'PIP_CONFIG_FILE'" in s2 and meta.get("env", {}).get("removed_ca_names") == ["CURL_CA_BUNDLE", "REQUESTS_CA_BUNDLE", "SSL_CERT_FILE"]
         and meta["env"]["runner_set"].get("PIP_CONFIG_FILE") == "/dev/null" and "SANDBOX_FAKE_TOKEN" in meta["env"]["removed_secret_names"]
         and "PIP_INDEX_URL" in meta["env"]["removed_pip_names"], f"bad={bad} meta.env={meta.get('env')}")
    s0 = jload(sb["E"] / "00_s0_precheck.json") or {}
    case("T1g S0 기록 — PIP_CERT 파일의 크기 · sha (경로는 안 적음) · precheck 원문 사본 · 실행기 사본 · 10월 diff",
         s0.get("pip_cert", {}).get("sha256") == sha(sb["cert"]) and str(sb["cert"]) not in (sb["E"] / "00_s0_precheck.json").read_text()
         and (sb["E"] / "00_precheck_before_t0" / "outer_return.json").is_file() and sha(sb["E"] / "00_runner.py") == sha(RUNNER)
         and (sb["E"] / "00_runner_vs_oct.diff").stat().st_size > 1000)
    rc2 = harness(sb, "run")
    case("T14 같은 출력 폴더로 하네스 다시 → rc 2 (덮어쓰기 · 재시도 없음)", rc2 == 2)


def t_no_precheck():
    sb = sandbox("t2")
    rc = harness(sb, "run")
    # 1 차 개발 실행의 변이 RM6 이 살아남은 뒤 강화: rc 2 · 폴더 없음은 "충돌" 로도 나온다 → 거부 사유 · traceback 0 까지 본다
    out = (sb["cfg"]["outer"] / "run" / "stdout.log").read_text(encoding="utf-8")
    err = (sb["cfg"]["outer"] / "run" / "stderr.log").read_text(encoding="utf-8")
    case("T2 precheck 없이 run → rc 2 · 기록 폴더 · 작업 뿌리 만들지 않음 · 거부 사유를 stdout 에 · traceback 0",
         rc == 2 and not sb["E"].exists() and not sb["R"].exists() and "precheck 의 바깥 반환이 없다" in out and "Traceback" not in err,
         f"rc={rc} out={out[-200:]!r} err={err[-200:]!r}")


def t_approval(kind, label, needle):
    sb = sandbox(f"t_{kind}", approval=kind)
    rc = harness(sb, "precheck")
    probs = " ".join(map(str, precheck_problems(sb)))
    case(label, rc == 2 and needle in probs, probs[:300])


def t_no_cert():
    sb = sandbox("t6", env_drop=("PIP_CERT",))
    rc = harness(sb, "precheck")
    probs = " ".join(map(str, precheck_problems(sb)))
    case("T6 PIP_CERT 없음 → precheck rc 2 (유효 CA 미고정 · ENV18-N1)", rc == 2 and "PIP_CERT" in probs, probs[:200])


def run_full(sb) -> tuple[int, dict, dict]:
    harness(sb, "precheck")
    rc = harness(sb, "run")
    return rc, jload(sb["R"] / "11_after_commit.json") or {}, jload(sb["E"] / "STOP.json") or {}


def t_timeout_group():
    m = "31.4159"
    sb = sandbox("t7", over={"05_install_science": [f"import subprocess,time; subprocess.Popen(['sleep','{m}']); time.sleep(30)"]},
                 allot={"S5": 2.0})
    rc, after, stop = run_full(sb)
    meta = jload(sb["E"] / "05_install_science.meta.json") or {}
    case("T7 자식 timeout → 프로세스 그룹째 끊음 (손주 sleep 도) · 첫 원인 = S5 timeout · 정지 기록 커밋 · ok 아님",
         rc == 1 and stop.get("step") == "05_install_science" and "timeout" in stop.get("reason", "") and meta.get("timed_out") is True
         and not leftover(f"sleep {m}") and after.get("ok") is False and after["commit"]["rc"] == 0
         and "정지 기록" in git(sb["repo"], "log", "-1", "--format=%s"), f"rc={rc} stop={stop}")


def t_survivor():
    m = "27.1828"
    sb = sandbox("t8", over={"03_download_test": [f"import subprocess; subprocess.Popen(['sleep','{m}'])"]})
    rc, after, stop = run_full(sb)
    case("T8 rc 0 인데 같은 그룹에 남은 자식 → 끊고 멈춤 (첫 원인 = S3)", rc == 1 and stop.get("step") == "03_download_test"
         and "남은 자식" in stop.get("reason", "") and not leftover(f"sleep {m}"), f"stop={stop}")


def t_first_failure():
    sb = sandbox("t9", over={"04a_wheels_science": [f"open('bms-balancing/evidence/reil_c4_env_SANDBOX/leak.txt', 'w').write('{FAKE_TOKEN}')"],
                             "05_install_science": ["import sys; sys.exit(3)"]})
    rc, after, stop = run_full(sb)
    case("T9 첫 원인 보존 — S5 rc 3 뒤 S10 비밀값 검사 실패 → STOP.json 은 S5 그대로 · 뒤 오류는 followups · 커밋 안 함",
         rc == 1 and stop.get("step") == "05_install_science" and stop.get("reason") == "rc 3"
         and any("비밀값" in f.get("reason", "") for f in after.get("followups", [])) and after["commit"]["attempted"] is False
         and git(sb["repo"], "rev-parse", "HEAD") == sb["head0"], f"stop={stop} followups={after.get('followups')}")


def t_commit_hook():
    sb = sandbox("t9b", hook=True)
    rc, after, stop = run_full(sb)
    case("T9b 커밋 실패 (pre-commit hook) → 11_after_commit 에 rc 1 · 새 커밋 없음 · ok 아님 · 실행기 rc 1",
         rc == 1 and after["commit"]["attempted"] is True and after["commit"]["rc"] == 1 and after["commit"]["new_commit"] is False
         and after["ok"] is False, f"after={str(after)[:300]}")


def t_total():
    slow = ["import time; time.sleep(1.5)"]
    sb = sandbox("t10", total_s=6.0, s10_allot=60.0, over={k: slow for k in ("01_venv", "02_download_science", "03_download_test", "04a_wheels_science",
                                                                       "05_install_science")})
    rc, after, stop = run_full(sb)
    case("T10 전체 1,800 s 의 축소판 (6 s) 소진 → 자식을 시작하지 않거나 timeout · S10 은 5 s 미만이면 커밋 시작 안 함 · ok 아님",
         rc == 1 and bool(stop) and after.get("ok") is False and after["total"]["within"] is False, f"stop={stop} commit={after.get('commit')}")


def t_harness_kill():
    m = "41.4142"
    fake = f"import subprocess, time\nsubprocess.Popen(['sleep', '{m}'])\ntime.sleep(60)\n"
    sb = sandbox("t11", harness_limit=3.0, fake_runner=fake)
    rc = harness(sb, "run")
    outer = jload(sb["cfg"]["outer"] / "run" / "outer_return.json") or {}
    case("T11 바깥 하네스의 절대 상한 → 그룹째 끊음 · rc 124 · killed_at_limit · 손주 없음", rc == 124 and outer.get("killed_at_limit") is True
         and not leftover(f"sleep {m}") and outer.get("elapsed_s", 99) < 3.0 + 2.0 * 2 + 3.0, f"rc={rc} outer={outer}")


def t_s10_small():
    sb = sandbox("t12", s10_allot=1.0)
    rc, after, stop = run_full(sb)
    case("T12 S10 배정 1 s → git add · commit 을 시작하지 않음 (index.lock 위험 · 스테이지 0) · 기록은 작업트리에 · ok 아님",
         rc == 1 and after["commit"]["attempted"] is False and "5 s 미만" in after["commit"].get("skipped_reason", "")
         and sb["E"].exists() and git(sb["repo"], "rev-parse", "HEAD") == sb["head0"]
         and git(sb["repo"], "diff", "--cached", "--name-only") == "", f"after={str(after)[:300]}")


def t_hold():
    sb = sandbox("t13", hold=True)
    rc, after, stop = run_full(sb)
    end = jload(sb["E"] / "10_end.json") or {}
    case("T13 S9a 의 채택 보류 표지 → 10_end · 11_after_commit · 커밋 제목에 그대로 (자동 실패 아님 · 자동 채택 아님)",
         rc == 0 and (end.get("adoption_hold") or {}).get("hold") is True and (after.get("adoption_hold") or {}).get("hold") is True
         and "채택 보류" in git(sb["repo"], "log", "-1", "--format=%s"), f"rc={rc}")


if __name__ == "__main__":
    with tempfile.TemporaryDirectory(prefix="runner_selftest_") as root:
        ROOT = root
        print(f"runner {RUNNER.relative_to(REPO)} sha256 {sha(RUNNER)}")
        print(f"harness {HARNESS.relative_to(REPO)} sha256 {sha(HARNESS)}")
        print(f"checker {CHECKER.relative_to(REPO)} sha256 {sha(CHECKER)}")
        print(f"python {sys.version.split()[0]} · isolated {sys.flags.isolated} · dont_write_bytecode {sys.dont_write_bytecode}")
        tests = [t_happy, t_no_precheck,
                 lambda: t_approval("missing", "T3 승인 블록 없음 → precheck rc 2", "정확히 하나가 아님 (0)"),
                 lambda: t_approval("two", "T5 승인 블록 둘 → precheck rc 2", "정확히 하나가 아님 (2)"),
                 lambda: t_approval("bad_runner_sha", "T4 승인 블록의 실행기 sha 틀림 → precheck rc 2", "runner_sha256"),
                 lambda: t_approval("wrong_request", "T15 승인 블록이 다른 요청서 (경로 · sha 는 서로 맞음 · 예: v1) 를 가리킴 → precheck rc 2", "요청서 경로"),
                 t_no_cert, t_timeout_group, t_survivor, t_first_failure, t_commit_hook, t_total, t_harness_kill, t_s10_small, t_hold]
        for fn in tests:
            try:
                fn()
            except Exception as exc:
                case(f"{getattr(fn, '__name__', 'case')} 예외", False, f"{type(exc).__name__}: {exc}")
        n_ok = sum(ok for _, ok in RESULTS)
        print(f"{n_ok} / {len(RESULTS)} PASS")
        sys.exit(0 if n_ok == len(RESULTS) else 1)
