"""REIL C4-ENV 새 세대 (CPython 3.11.18) 실행기 — 요청서 v2 (`bms-balancing/docs/REIL_C4_ENV_RESEAL_REQUEST_v2_20261124.md`) §2 의
argv 를 순서대로 그대로 부른다. 바깥 하네스 (`reil_c4_env_reseal_harness.py`) 만 이 파일을 부른다.

  /usr/bin/python3.11 -I -B bms-balancing/scripts/reil_c4_env_reseal_run.py precheck   읽기만 (쓰기 0 · 디렉터리 생성 0) · 결과 = stdout JSON
  /usr/bin/python3.11 -I -B bms-balancing/scripts/reil_c4_env_reseal_run.py run        S0–S10 1 회
  (-I · -B 둘 다 없으면 시작하지 않는다 — -B 는 저장소 안 pyc 쓰기를 막는다)

- 승인은 원장 (`REIL_PREREQUISITES_STATUS_20261004.md`) 안의 승인 블록 **하나** 에서 읽는다 (요청서 경로 · sha · 요청 커밋 · 이 파일 · 하네스 · 대조기의
  sha · 사용자 원문). 요청서 경로는 이 파일이 고정한다 (`request_rel` = 요청서 v2 — 다른 요청서를 그 sha 와 함께 넣으면 거부). 이 파일은 승인 값을 품지 않는다 — 자기 sha 를 품을 수 없기 때문이다 (C4-A v4 §4-2 의 승인 블록 선례).
- 재시도 · 다른 경로 · 다른 interpreter · 추가 명령 없음. 실패하면 **첫 원인** (`STOP.json` · 한 번만 씀) 과 확보한 기록을 남기고 멈춘다.
- 시간: 자식마다 timeout = min(단계 배정의 남은 몫, 전체의 남은 몫) · 넘으면 프로세스 그룹째 끊는다. 실행기 안의 순수 Python 작업 (해시 · du ·
  기록 쓰기) 은 도중에 끊지 못하고 **끝난 뒤** 초과를 잡는다 — 절대 반환은 바깥 하네스의 상한이 보장한다.
- 자식 env (검토 §137 ENV18-N1): 비밀 형태 이름 · `PIP_CERT` 밖의 `PIP_*` · `REQUESTS_CA_BUNDLE` · `CURL_CA_BUNDLE` · `SSL_CERT_FILE` ·
  `SSL_CERT_DIR` 를 뺀다 (이름만 기록). 실행기 자신의 env (git 포함) 는 정리하지 않는다 (10월과 같음 · 한계로 밝힘).
- S10 (ENV18-N2): `10_end.json` 은 커밋 **전** 기록 (PRE_COMMIT · S10 PENDING) 이다. 커밋 결과 · S10 끝 · 한도 판정은 커밋 **밖**
  `SP/reil_env18/11_after_commit.json` 에 쓴다. 못 얻은 값은 null 로 둔다.
"""
from __future__ import annotations

import datetime
import difflib
import hashlib
import json
import os
import platform
import re
import shutil
import signal
import subprocess
import sys
import time
import traceback
from pathlib import Path

SECRET_NAME = re.compile(r"TOKEN|SECRET|PASSW|ACCESS_KEY|CREDENTIAL|COOKIE|^GIT_CONFIG_", re.I)   # 10월 실행기 그대로
CA_NAMES = ("REQUESTS_CA_BUNDLE", "CURL_CA_BUNDLE", "SSL_CERT_FILE", "SSL_CERT_DIR")             # v2 · ENV18-N1
APPROVAL_FENCE = "```c4env-reseal-approval"
TRAILER = ("Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n"
           "Claude-Session: https://claude.ai/code/session_0157zrP6GFu6cJF5x8CwZaEm\n")


def production_plan() -> dict:
    repo = Path(__file__).resolve().parents[2]
    sp = Path("/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/b881d255-9513-5adc-9b14-3c0be18d7ad6/scratchpad")
    R = sp / "reil_env18"
    P = ["/usr/bin/python3.11", "-I", "-B"]
    K = "bms-balancing/scripts/reil_c4_env_reseal_check.py"
    V = str(R / "venv" / "bin" / "python")
    C = "bms-balancing/evidence/reil_p0_20261006/01_venv_constraints.txt"
    OE = "bms-balancing/evidence/reil_c4_env_20261013"
    E = "bms-balancing/evidence/reil_c4_env_20261124"
    N = "bms-balancing/reil_c6_rebuild_20261124"
    X = ["--no-cache-dir", "--disable-pip-version-check"]
    I = ["--index-url", "https://pypi.org/simple"]
    SCI = ["numpy==2.4.6", "scipy==1.17.1", "pandas==3.0.5", "openpyxl==3.1.5", "matplotlib==3.11.2", "seaborn==0.13.2", "pymoo==0.6.2"]
    TEST = ["pytest==9.1.1", "pluggy==1.6.0", "iniconfig==2.3.0", "pygments==2.21.0"]
    pip_env = {"PIP_CONFIG_FILE": "/dev/null"}
    py_env = {"PYTHONDONTWRITEBYTECODE": "1"}
    return {
        "repo": repo, "sp": sp, "R": R, "outer": sp / "c4env18_outer", "E_rel": E, "N_rel": N,
        "py": "/usr/bin/python3.11",
        "ledger_rel": "bms-balancing/docs/REIL_PREREQUISITES_STATUS_20261004.md",
        "request_rel": "bms-balancing/docs/REIL_C4_ENV_RESEAL_REQUEST_v2_20261124.md",
        "runner_rel": "bms-balancing/scripts/reil_c4_env_reseal_run.py",
        "harness_rel": "bms-balancing/scripts/reil_c4_env_reseal_harness.py",
        "checker_rel": K,
        "oct_runner_rel": OE + "/00_runner.py",
        "guarded": ["bms-balancing/scripts", "degradation-degeneracy/tools/env_profile.py"],
        "protected_trees": {
            "bms-balancing/reil_c6_rebuild_20261013": "f4384bb265ccd73ffc39cd4a43d7507014234bde",
            "bms-balancing/evidence/reil_c4_env_20261013": "df74b0e340c2c17fec440fa01c790d1c190fdc8e",
            "bms-balancing/evidence/reil_c4_env_20261013_outer_return": "3e6808af5c902d882f133fd8d910cd12be3a8291",
            "bms-balancing/evidence/reil_c4_env_compare_selftest_20261013": "e8dbb40efd11176c8a7f33201cbfa0eb8d5b1759",
            "bms-balancing/reil_c6_20261005": "3ec46373da366265242e92df9c6e112e5ff100e0",
            "bms-balancing/reil_c6_rebuild_20261006": "b55f3a439e23bd41626d64bbb40b8221571f8690",
            "bms-balancing/evidence/reil_p0_20261006": "82a74d69c3f3cad363d6f120fe0e88658af0a496",
            "bms-balancing/evidence/reil_c6_n1_20261006": "fdd12a5f30dc52242e0553b6b616c463a264fe54",
            "bms-balancing/evidence/reil_c5_impl_20261006": "cfea813242c2d47f559a3807c5bab1bb63f3e183",
            "bms-balancing/evidence/reil_c5_pilot_20261006": "514e4dcd284f831a92e158ad4542136cc455f018",
            "bms-balancing/evidence/reil_c5_pilot_20261006_wrapper": "6238fff9ff7bc6a54747f28653eca4e3f1b20a2d",
            "bms-balancing/evidence/reil_c4_env_reseal_pre_20261124": "1e759c6a5d0e38fb7c84f20fe7233f8b15276cc7",
            "bms-balancing/evidence/reil_c4_env_reseal_selftest_20261124": "6cedd7828d7a0949e70836efacb4b60f1aca3998",
        },
        "protected_files": {
            "bms-balancing/scripts/reil_c6_profile.py": "408afc4bb5eb1069583b955e0eb6215bf48dd9259ad474c230549d1b3642df5d",
            "degradation-degeneracy/tools/env_profile.py": "83b0d8365d039d75050d087fe980ad7b64818686b699e5d06da1c0ad63148563",
            "bms-balancing/scripts/reil_c4_env_compare.py": "eff94d3dfd4b3d31c7a19e440dfb968734dab1afb16b584c2fdee354100695e0",
            "bms-balancing/scripts/reil_c5_pilot.py": "73bee8dc412b39863afb64b70bc128cbecee2075a3a17914fc7288f353ef11a6",
            C: "db63333bdaf1835444a86187215ed7faf06897eb8a247c667ed167a5ee1dc772",
        },
        "interpreter": {"path": "/usr/bin/python3.11", "is_symlink": False, "size": 6644312,
                        "sha256": "ca969be9adfbddc0a593745da84da0348a4c2baf849daae18806a344708934c4",
                        "version": "3.11.18", "build": ["main", "Oct 26 2026 15:28:55"], "compiler": "GCC 13.3.0",
                        "implementation": "CPython", "system": "Linux", "machine": "x86_64", "libc": "glibc 2.39"},
        "deb": {"python3.11-minimal": "3.11.18-1+noble1", "libpython3.11-stdlib": "3.11.18-1+noble1", "python3.11-venv": "3.11.18-1+noble1"},
        "dpkg_verify": {"package": "python3.11-venv",
                        "stdout": "??5??????   /usr/lib/python3.11/ensurepip/_bundled/pip-24.0-py3-none-any.whl\n"},
        "source_sha": {"/usr/lib/python3.11/ensurepip/__init__.py": "0f4e3b95882c914577a9045e27ac88f78d9a0a931a409d3d0287df1cd49e945a",
                       "/usr/lib/python3.11/venv/__init__.py": "8671bc5810ee3e52a5ae7aa3b625764688cf12513b2f8e1b0b82aaec93f118a6"},
        "dpkg_query": ["dpkg-query", "-W", "-f=${Version}"], "dpkg_v": ["dpkg", "-V"],
        "total_s": 1800.0, "disk_limit": 2_000_000_000, "free_min": 4_000_000_000, "precheck_s": 60.0,
        "s0": {"allot": 60.0, "bundled": P + [K, "bundled", "--bundled", "/usr/lib/python3.11/ensurepip/_bundled",
                                              "--out", E + "/00_bundled_check.json"]},
        "groups": [   # (그룹 · 배정 s · 자식들 [id · argv · env 더함 · 네트워크]) — 요청서 v2 §2-2 표 그대로
            ("S1", 120.0, [("01_venv", ["/usr/bin/python3.11", "-I", "-m", "venv", str(R / "venv")], {}, "0")]),
            ("S2", 480.0, [("02_download_science", [V, "-I", "-m", "pip", "download", *X, *I, "--only-binary=:all:",
                                                    "--dest", str(R / "wheels"), "-c", C, *SCI], pip_env, "PyPI")]),
            ("S3", 120.0, [("03_download_test", [V, "-I", "-m", "pip", "download", *X, *I, "--only-binary=:all:", "--no-deps",
                                                 "--dest", str(R / "wheels_test"), *TEST], pip_env, "PyPI")]),
            ("S4", 30.0, [("04a_wheels_science", P + [K, "wheels", "--wheels", str(R / "wheels"), "--expect", OE + "/04_artifacts_science.json",
                                                      "--out", E + "/04a_wheels_science.json"], {}, "0"),
                          ("04b_wheels_test", P + [K, "wheels", "--wheels", str(R / "wheels_test"), "--expect", OE + "/04_artifacts_test.json",
                                                   "--out", E + "/04b_wheels_test.json"], {}, "0")]),
            ("S5", 300.0, [("05_install_science", [V, "-I", "-m", "pip", "install", *X, "--no-index", "--find-links", str(R / "wheels"),
                                                   "-c", C, *SCI], pip_env, "0")]),
            ("S6", 120.0, [("06_install_test", [V, "-I", "-m", "pip", "install", *X, "--no-index", "--find-links", str(R / "wheels_test"),
                                                "--no-deps", "--target", str(R / "pytest_t"), *TEST], pip_env, "0")]),
            ("S7", 180.0, [("07_emit", [V, "bms-balancing/scripts/reil_c6_profile.py", "emit", N], py_env, "0")]),
            ("S8", 180.0, [("08_check", [V, "bms-balancing/scripts/reil_c6_profile.py", "check", N], py_env, "0")]),
            ("S9", 120.0, [("09a_records", P + [K, "records", "--venv", str(R / "venv"), "--target", str(R / "pytest_t"),
                                                "--records-out", E + "/09_records", "--test-records-out", E + "/09_test_tool_records",
                                                "--out", E + "/09a_records.json"], {}, "0"),
                           ("09b_seal", P + [K, "seal", "--new", N, "--new-records", E + "/09_records",
                                             "--records-report", E + "/09a_records.json", "--out", E + "/09b_seal.json"], {}, "0")]),
        ],
        "disk_after": ["S2", "S3", "S5", "S6", "S8", "S9"],
        "s10_allot": 90.0,
        "check_ok_step": "08_check",
        "records_step": "09a_records",
        "environ": None,          # None = os.environ (시험에서만 바꾼다)
    }


# ── 작은 도구 ──────────────────────────────────────────────────────────────────

def utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def dump(path: Path, obj) -> None:
    if path.exists():
        raise FileExistsError(f"덮어쓰지 않는다: {path}")
    path.write_text(json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=1) + "\n", encoding="utf-8")


class Run:
    """한 번의 precheck 또는 run 의 상태. 시각은 monotonic 원점 기준 초."""

    def __init__(self, plan: dict, mode: str):
        self.plan, self.mode = plan, mode
        self.environ = dict(os.environ if plan.get("environ") is None else plan["environ"])
        self.t0 = time.monotonic()
        self.t0_utc = utc()
        self.steps, self.disk, self.followups = [], [], []
        self.stopped = None
        self.E = plan["repo"] / plan["E_rel"]
        self.N = plan["repo"] / plan["N_rel"]
        self.adoption_hold = None
        self.group = None                 # (이름, 배정, 시작 monotonic)

    def rel(self) -> float:
        return round(time.monotonic() - self.t0, 3)

    def log(self, msg: str) -> None:
        print(f"[{utc()} +{self.rel():.1f}s] {msg}", flush=True)

    def git(self, *args, timeout=60.0, **kw):
        return subprocess.run(["git", "-C", str(self.plan["repo"]), *args], capture_output=True, text=True, timeout=timeout, **kw)

    # ── 시간 ──
    def total_left(self) -> float:
        return self.plan["total_s"] - (time.monotonic() - self.t0)

    def group_left(self) -> float:
        name, allot, start = self.group
        return allot - (time.monotonic() - start)

    def check_budget(self, where: str) -> None:
        """순수 Python 작업 뒤의 사후 초과 탐지 — 도중에 끊지 못한다 (절대 반환은 하네스)."""
        if self.total_left() < 0:
            self.stop(where, f"전체 {self.plan['total_s']} s 초과 (사후 탐지 · +{self.rel()} s)")
        if self.group is not None and self.group_left() < 0:
            self.stop(where, f"단계 {self.group[0]} 배정 {self.group[1]} s 초과 (사후 탐지)")

    # ── 자식 ──
    def child_env(self, extra: dict) -> tuple[dict, dict]:
        base = self.environ
        r_secret = sorted(k for k in base if SECRET_NAME.search(k))
        r_pip = sorted(k for k in base if k.startswith("PIP_") and k != "PIP_CERT")
        r_ca = sorted(k for k in base if k in CA_NAMES)
        drop = set(r_secret) | set(r_pip) | set(r_ca)
        env = {k: v for k, v in base.items() if k not in drop}
        env.update(extra)
        return env, {"removed_secret_names": r_secret, "removed_pip_names": r_pip, "removed_ca_names": r_ca,
                     "names_passed": sorted(env), "runner_set": extra}

    def child(self, sid: str, argv: list, extra: dict, network: str) -> dict:
        timeout = min(self.group_left(), self.total_left())
        if timeout <= 0:
            self.stop(sid, "단계 또는 전체 배정 소진 — 이 자식을 시작하지 않음")
        env, env_rec = self.child_env({"TMPDIR": str(self.plan["R"] / "tmp"), **extra})
        meta = {"step": sid, "group": self.group[0], "argv": argv, "cwd": str(self.plan["repo"]), "env": env_rec, "network": network,
                "group_allot_s": self.group[1], "timeout_s": round(timeout, 3), "start_utc": utc(), "start_rel": self.rel()}
        self.log(f"{sid} start (timeout {timeout:.1f}s)")
        t = time.monotonic()
        with open(self.E / f"{sid}.stdout.log", "xb") as fo, open(self.E / f"{sid}.stderr.log", "xb") as fe:
            p = subprocess.Popen(argv, cwd=str(self.plan["repo"]), env=env, stdout=fo, stderr=fe, start_new_session=True)
            timed_out, survivors = False, False
            try:
                p.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                timed_out = True
                self._kill_group(p)
            if not timed_out:
                survivors = self._kill_group(p, only_if_alive=True)
        meta.update({"end_utc": utc(), "end_rel": self.rel(), "elapsed_s": round(time.monotonic() - t, 3), "rc": p.returncode,
                     "timed_out": timed_out, "group_survivors_killed": survivors})
        dump(self.E / f"{sid}.meta.json", meta)
        self.steps.append({k: meta[k] for k in ("step", "group", "rc", "timed_out", "elapsed_s", "start_rel", "end_rel", "timeout_s")})
        self.log(f"{sid} end rc={p.returncode} timed_out={timed_out} elapsed={meta['elapsed_s']}s")
        if timed_out:
            self.stop(sid, f"timeout {round(timeout, 3)} s (프로세스 그룹 종료)")
        if p.returncode != 0:
            self.stop(sid, f"rc {p.returncode}")
        if survivors:
            self.stop(sid, "rc 0 이지만 같은 프로세스 그룹에 남은 자식이 있어 끊었다")
        self.check_budget(sid)
        return meta

    @staticmethod
    def _kill_group(p, only_if_alive=False) -> bool:
        """자식의 프로세스 그룹 (start_new_session) 을 TERM → KILL 로 끊는다. 그룹에 아무도 없으면 False.
        only_if_alive=True 는 정상 종료 뒤 남은 그룹원만 잡는다. 기다리는 동안 p.poll() 로 본 자식을 거둬 좀비가 그룹을 붙잡지 않게 한다."""
        p.poll()
        try:
            os.killpg(p.pid, 0)
        except (ProcessLookupError, PermissionError):
            return False
        for sig, wait in ((signal.SIGTERM, 5.0), (signal.SIGKILL, 5.0)):
            try:
                os.killpg(p.pid, sig)
            except ProcessLookupError:
                break
            end = time.monotonic() + wait
            gone = False
            while time.monotonic() < end:
                p.poll()
                try:
                    os.killpg(p.pid, 0)
                except ProcessLookupError:
                    gone = True
                    break
                time.sleep(0.05)
            if gone:
                break
        if p.poll() is None:
            p.wait()
        return True

    # ── 디스크 ──
    def du(self) -> dict:
        parts, total = {}, 0
        for p in (self.plan["R"], self.N, self.E, self.plan["outer"]):
            if p.exists():
                out = subprocess.run(["du", "-sb", str(p)], capture_output=True, text=True, timeout=max(1.0, min(60.0, self.total_left())))
                n = int(out.stdout.split()[0])
                parts[str(p)] = n
                total += n
        return {"du_sb_total": total, "du_sb_parts": parts, "free_bytes": shutil.disk_usage(str(self.plan["repo"])).free}

    def disk_sample(self, label: str) -> None:
        obs = {"label": label, "utc": utc(), "t_rel": self.rel(), **self.du()}
        self.disk.append(obs)
        self.log(f"disk {label}: {obs['du_sb_total']} B")
        if obs["du_sb_total"] > self.plan["disk_limit"]:
            self.stop(label, f"디스크 합계 {obs['du_sb_total']} B > {self.plan['disk_limit']} B")
        self.check_budget(f"disk {label}")

    # ── 멈춤 (첫 원인은 한 번만) ──
    def stop(self, sid: str, reason: str):
        rec = {"step": sid, "reason": reason, "utc": utc(), "t_rel": self.rel()}
        if self.stopped is None:
            self.stopped = rec
            self.log(f"STOP {sid}: {reason}")
            if self.E.exists() and not (self.E / "STOP.json").exists():
                dump(self.E / "STOP.json", rec)
            raise Stopped(rec)
        self.followups.append(rec)          # 첫 원인을 덮지 않는다
        raise Stopped(rec)


class Stopped(Exception):
    pass


# ── 승인 블록 · 사전 대조 ────────────────────────────────────────────────────────

def find_approval(text: str) -> tuple[dict | None, list]:
    lines = text.split("\n")
    starts = [i for i, ln in enumerate(lines) if ln.strip() == APPROVAL_FENCE]
    if len(starts) != 1:
        return None, [f"승인 블록이 정확히 하나가 아님 ({len(starts)})"]
    i = starts[0]
    ends = [k for k in range(i + 1, len(lines)) if lines[k].strip() == "```"]
    if not ends:
        return None, ["승인 블록이 닫히지 않음"]
    try:
        blk = json.loads("\n".join(lines[i + 1:ends[0]]))
    except json.JSONDecodeError as exc:
        return None, [f"승인 블록 JSON 오류: {exc}"]
    P = []
    if blk.get("kind") != "C4ENV_RESEAL_EXECUTION" or blk.get("decision") != "APPROVED":
        P.append("승인 블록의 kind · decision 이 C4ENV_RESEAL_EXECUTION · APPROVED 가 아님")
    for k in ("request", "request_commit", "runner_sha256", "harness_sha256", "checker_sha256", "user_text"):
        if not blk.get(k):
            P.append(f"승인 블록에 {k} 없음")
    if isinstance(blk.get("request"), dict) and not {"path", "sha256"} <= set(blk["request"]):
        P.append("승인 블록 request 에 path · sha256 없음")
    if blk.get("request_commit") and not re.fullmatch(r"[0-9a-f]{40}", str(blk["request_commit"])):
        P.append("승인 블록 request_commit 이 40 자 sha 가 아님")
    return blk, P


def checks(run: Run) -> tuple[dict, list, str]:
    """S0 와 precheck 가 같이 쓰는 읽기 전용 대조 — 만들거나 쓰지 않는다."""
    plan, P, info = run.plan, [], {}
    t = time.monotonic()
    info["runner"] = {"sys_executable": sys.executable, "isolated": bool(sys.flags.isolated),
                      "dont_write_bytecode": bool(sys.flags.dont_write_bytecode), "sha256": sha_file(__file__)}
    if os.path.realpath(sys.executable) != plan["py"] or not sys.flags.isolated or not sys.flags.dont_write_bytecode:
        P.append({"runner_interpreter": info["runner"]})
    head = run.git("rev-parse", "HEAD").stdout.strip()
    info["head"] = head
    ledger = run.git("show", f"HEAD:{plan['ledger_rel']}").stdout
    blk, bp = find_approval(ledger)
    P += bp
    info["approval"] = blk
    if blk and not bp:
        def at_head(rel):
            g = subprocess.run(["git", "-C", str(plan["repo"]), "show", f"HEAD:{rel}"], capture_output=True, timeout=60)
            return sha_bytes(g.stdout) if g.returncode == 0 else None
        if blk["request"]["path"] != plan["request_rel"]:      # 승인된 요청서가 이 실행기의 요청서인가 (다른 요청서 + 그 sha 로 바꿔 넣기 거부)
            P.append(f"승인 블록의 요청서 경로가 {plan['request_rel']} 가 아님 ({blk['request']['path']})")
        if at_head(blk["request"]["path"]) != blk["request"]["sha256"]:
            P.append("요청서 sha 가 승인 블록과 다름 (HEAD)")
        for key, rel in (("runner_sha256", plan["runner_rel"]), ("harness_sha256", plan["harness_rel"]), ("checker_sha256", plan["checker_rel"])):
            if at_head(rel) != blk[key] or sha_file(plan["repo"] / rel) != blk[key]:
                P.append(f"{rel} 의 sha 가 승인 블록 ({key}) 과 다름 (HEAD 또는 작업트리)")
        if sha_file(__file__) != blk["runner_sha256"]:
            P.append("지금 돌고 있는 실행기 파일의 sha 가 승인 블록과 다름")
        rc = blk["request_commit"]
        if run.git("merge-base", "--is-ancestor", rc, "HEAD").returncode != 0:
            P.append(f"요청 커밋 {rc} 이 HEAD 의 조상이 아님")
        intro = run.git("log", "--format=%H", f"-S{APPROVAL_FENCE}", "--", plan["ledger_rel"]).stdout.split()
        info["approval_commit"] = intro[0] if len(intro) == 1 else intro
        if len(intro) != 1:
            P.append(f"승인 블록을 넣은 커밋이 하나가 아님 ({intro})")
        elif run.git("merge-base", "--is-ancestor", rc, intro[0]).returncode != 0:
            P.append("승인 블록 커밋이 요청 커밋 뒤가 아님")
        changed = run.git("diff", "--name-only", rc, "HEAD", "--", *plan["guarded"], *plan["protected_trees"]).stdout.split()
        if changed:
            P.append({"요청 커밋 뒤 바뀐 보호 경로": changed})
    porcelain = run.git("status", "--porcelain=v1", "--untracked-files=all").stdout
    dirty = run.git("status", "--porcelain=v1", "--untracked-files=all", "--", *plan["guarded"], *plan["protected_trees"]).stdout
    if dirty.strip():
        P.append({"보호 경로 작업트리 변경": dirty.splitlines()})
    info["porcelain_lines"] = len(porcelain.splitlines())
    info["trees"] = {p: run.git("rev-parse", f"HEAD:{p}").stdout.strip() for p in plan["protected_trees"]}
    P += [{"tree": p, "want": w, "got": info["trees"][p]} for p, w in plan["protected_trees"].items() if info["trees"][p] != w]
    info["files"] = {p: (sha_file(plan["repo"] / p) if (plan["repo"] / p).is_file() else None) for p in plan["protected_files"]}
    P += [{"file": p, "want": w, "got": info["files"][p]} for p, w in plan["protected_files"].items() if info["files"][p] != w]
    exp = plan["interpreter"]
    interp = {"path": exp["path"], "is_symlink": os.path.islink(exp["path"]), "size": os.path.getsize(exp["path"]), "sha256": sha_file(exp["path"]),
              "version": platform.python_version(), "build": list(platform.python_build()), "compiler": platform.python_compiler(),
              "implementation": platform.python_implementation(), "system": platform.system(), "machine": platform.machine(),
              "libc": " ".join(platform.libc_ver()).strip()}
    info["interpreter"] = interp
    P += [{"interpreter": k, "want": w, "got": interp[k]} for k, w in exp.items() if interp[k] != w]
    deb = {k: subprocess.run(plan["dpkg_query"] + [k], capture_output=True, text=True, timeout=10).stdout for k in plan["deb"]}
    info["deb"] = deb
    P += [{"deb": k, "want": w, "got": deb[k]} for k, w in plan["deb"].items() if deb[k] != w]
    dv = subprocess.run(plan["dpkg_v"] + [plan["dpkg_verify"]["package"]], capture_output=True, text=True, timeout=30)
    info["dpkg_verify"] = {"stdout": dv.stdout, "rc": dv.returncode}
    if dv.stdout != plan["dpkg_verify"]["stdout"]:
        P.append({"dpkg_verify": dv.stdout})
    info["source_sha"] = {p: sha_file(p) for p in plan["source_sha"]}
    P += [{"source": p, "want": w, "got": info["source_sha"][p]} for p, w in plan["source_sha"].items() if info["source_sha"][p] != w]
    cert = run.environ.get("PIP_CERT")
    if not cert or not os.path.isfile(cert):
        P.append("PIP_CERT 가 없거나 파일이 아님 (유효 CA 가 고정되지 않는다 · ENV18-N1)")
        info["pip_cert"] = None
    else:
        info["pip_cert"] = {"size": os.path.getsize(cert), "sha256": sha_file(cert), "note": "경로는 적지 않는다"}
    info["env_names"] = {"ca_present": sorted(k for k in run.environ if k in CA_NAMES),
                         "pip_present": sorted(k for k in run.environ if k.startswith("PIP_")),
                         "secret_shaped_present": sorted(k for k in run.environ if SECRET_NAME.search(k)),
                         "proxy_present": sorted(k for k in run.environ if "proxy" in k.lower())}
    info["netrc_present"] = os.path.exists(os.path.expanduser("~/.netrc"))
    for p in (plan["R"], run.N, run.E):
        if p.exists():
            P.append({"path_exists": str(p)})
    info["free_bytes"] = shutil.disk_usage(str(plan["repo"])).free
    if info["free_bytes"] < plan["free_min"]:
        P.append({"free_bytes": info["free_bytes"]})
    info["elapsed_s"] = round(time.monotonic() - t, 3)
    limit = plan["precheck_s"] if run.mode == "precheck" else plan["s0"]["allot"]
    if info["elapsed_s"] > limit:
        P.append(f"사전 대조가 {limit} s 를 넘음 ({info['elapsed_s']} s)")
    return info, P, porcelain


# ── S0 · 단계 · S10 ─────────────────────────────────────────────────────────────

def s0(run: Run) -> None:
    plan = run.plan
    run.group = ("S0", plan["s0"]["allot"], run.t0)
    info, P, porcelain = checks(run)
    pre = plan["outer"] / "precheck"
    pre_ret = pre / "outer_return.json"
    if not pre_ret.is_file():
        P.append("precheck 의 바깥 반환이 없다 — precheck 1 회 뒤에만 실행한다")
    else:
        r = json.loads(pre_ret.read_text(encoding="utf-8"))
        out = json.loads((pre / "stdout.log").read_text(encoding="utf-8")) if (pre / "stdout.log").is_file() else {}
        if r.get("rc") != 0 or out.get("problems") != [] or out.get("runner_sha256") != info["runner"]["sha256"]:
            P.append("precheck 가 rc 0 · 문제 0 · 같은 실행기 sha 로 끝나지 않았다")
    if P:
        print(json.dumps({"mode": "run", "stage": "S0", "problems": P, "info": info}, ensure_ascii=False, indent=1, default=str))
        run.log("S0 사전 조건 실패 — 시작하지 않음 (기록 폴더를 만들지 않았다)")
        sys.exit(2)
    plan["R"].mkdir()
    (plan["R"] / "tmp").mkdir()
    run.E.mkdir()
    (run.E / "00_porcelain_start.txt").write_text(porcelain, encoding="utf-8")
    shutil.copyfile(__file__, run.E / "00_runner.py")
    shutil.copyfile(plan["repo"] / plan["harness_rel"], run.E / "00_harness.py")
    oct_runner = (plan["repo"] / plan["oct_runner_rel"]).read_text(encoding="utf-8").splitlines(keepends=True)
    mine = Path(__file__).read_text(encoding="utf-8").splitlines(keepends=True)
    (run.E / "00_runner_vs_oct.diff").write_text("".join(difflib.unified_diff(oct_runner, mine, plan["oct_runner_rel"], plan["runner_rel"])),
                                                encoding="utf-8")
    shutil.copytree(pre, run.E / "00_precheck_before_t0")
    info["runner_copy_sha256"] = sha_file(run.E / "00_runner.py")
    info["t0_utc"] = run.t0_utc
    dump(run.E / "00_s0_precheck.json", info)
    blk = info["approval"]
    (run.E / "00_approval.json").write_text(json.dumps({"approval_block": blk, "approval_commit": info["approval_commit"], "t0_utc": run.t0_utc},
                                                       ensure_ascii=False, sort_keys=True, indent=1) + "\n", encoding="utf-8")
    run.steps.append({"step": "S0-checks", "group": "S0", "rc": 0, "timed_out": False, "elapsed_s": info["elapsed_s"], "start_rel": 0.0,
                      "end_rel": run.rel(), "timeout_s": plan["s0"]["allot"]})
    run.check_budget("S0")
    run.child("00_bundled_check", plan["s0"]["bundled"], {}, "0")
    run.log(f"S0 ok head={info['head'][:12]}")


def groups(run: Run) -> None:
    plan = run.plan
    for name, allot, children in plan["groups"]:
        run.group = (name, allot, time.monotonic())
        for sid, argv, extra, net in children:
            run.child(sid, argv, extra, net)
            if sid == plan["check_ok_step"] and b"check OK" not in (run.E / f"{sid}.stdout.log").read_bytes():
                run.stop(sid, "rc 0 이지만 'check OK' 출력 없음")
            if sid == plan["records_step"]:
                rr = json.loads((run.E / "09a_records.json").read_text(encoding="utf-8"))
                run.adoption_hold = {"hold": bool(rr.get("adoption_hold")), "reasons": rr.get("adoption_hold_reasons", [])}
        if name in plan["disk_after"]:
            run.disk_sample(name)


def secret_scan(run: Run) -> list:
    vals = {k: v for k, v in run.environ.items() if SECRET_NAME.search(k) and len(v) >= 8 and not k.endswith("_FILE")
            and not k.startswith("GIT_CONFIG_KEY_") and k != "GIT_CONFIG_COUNT"}
    hits = []
    for root in (run.E, run.N):
        if root.exists():
            for p in sorted(root.rglob("*")):
                if p.is_file():
                    b = p.read_bytes()
                    hits += [{"file": str(p.relative_to(run.plan["repo"])), "env_name": k} for k, v in vals.items() if v.encode() in b]
    return hits


def s10(run: Run, stopped: bool) -> int:
    """커밋 전 기록 → 비밀값 검사 → 스테이지 대조 → 커밋 → (커밋 밖) 11_after_commit.json. 커밋 전 기록은 S10 결과를 담지 않는다."""
    plan = run.plan
    run.group = ("S10", plan["s10_allot"], time.monotonic())
    s10_start = run.rel()
    after = {"kind": "C4ENV_RESEAL_AFTER_COMMIT", "stopped": run.stopped, "followups": run.followups,
             "commit": {"attempted": False, "argv": None, "rc": None, "timed_out": None, "stderr_tail": None, "head_after": None,
                        "new_commit": None},
             "s10": {"start_rel": s10_start, "end_rel": None, "elapsed_s": None, "allot_s": plan["s10_allot"], "within": None},
             "total": {"end_rel": None, "limit_s": plan["total_s"], "within": None},
             "disk": {"after_commit": None, "limit": plan["disk_limit"], "within": None},
             "files": {"10_end_json_sha256": None, "staged": None}, "adoption_hold": run.adoption_hold, "ok": False}
    head_before = None
    try:
        head_before = run.git("rev-parse", "HEAD", timeout=max(1.0, run.group_left())).stdout.strip()
        protected_end = {p: run.git("rev-parse", f"HEAD:{p}", timeout=max(1.0, run.group_left())).stdout.strip() for p in plan["protected_trees"]}
        problems = [p for p, w in plan["protected_trees"].items() if protected_end[p] != w]
        problems += [p for p, w in plan["protected_files"].items() if not (plan["repo"] / p).is_file() or sha_file(plan["repo"] / p) != w]
        porcelain_end = run.git("status", "--porcelain=v1", "--untracked-files=all", timeout=max(1.0, run.group_left())).stdout
        try:
            run.disk_sample("S10-pre-commit")
        except Stopped:
            pass                                   # 첫 원인은 이미 기록됐다 · 커밋 전 기록은 그대로 쓴다
        (run.E / "10_porcelain_end.txt").write_text(porcelain_end, encoding="utf-8")
        end = {"phase": "PRE_COMMIT", "s10": {"status": "PENDING", "start_rel": s10_start,
                                              "note": "이 파일은 커밋 전에 쓴다 — 커밋 결과 · S10 끝 · 한도 판정은 커밋 밖 11_after_commit.json"},
               "t0_utc": run.t0_utc, "written_rel": run.rel(), "stopped": run.stopped, "followups": run.followups, "steps": run.steps,
               "disk": run.disk, "protected_trees_end": protected_end, "protected_changed": problems, "adoption_hold": run.adoption_hold,
               "head_before_commit": head_before}
        dump(run.E / "10_end.json", end)
        after["files"]["10_end_json_sha256"] = sha_file(run.E / "10_end.json")
        hits = secret_scan(run)
        if hits:
            after["secret_scan_hits"] = hits
            raise RuntimeError("비밀값 검사 실패 — 커밋하지 않는다")
        paths = [x for x in (plan["N_rel"], plan["E_rel"]) if (plan["repo"] / x).exists()]
        if min(run.group_left(), run.total_left()) < 5.0:     # git 을 도중에 죽이면 index.lock 이 남을 수 있다 — 시작하지 않는다
            after["commit"]["skipped_reason"] = "S10 또는 전체 배정이 5 s 미만 남음 — git add · commit 을 시작하지 않음 (기록은 작업트리에 남는다)"
            raise RuntimeError(after["commit"]["skipped_reason"])
        add = run.git("add", "-f", "--", *paths, timeout=max(5.0, min(run.group_left(), run.total_left())))
        if add.returncode != 0:
            raise RuntimeError(f"git add rc {add.returncode}")
        staged = {}
        for ln in run.git("ls-files", "-s", "--", *paths, timeout=max(1.0, run.group_left())).stdout.splitlines():
            meta, path = ln.split("\t", 1)
            staged[path] = meta.split()[1]
        files = sorted(staged)
        hashed = run.git("hash-object", "--no-filters", "--stdin-paths", input="\n".join(files) + "\n",
                         timeout=max(1.0, run.group_left())).stdout.split()
        on_disk = sorted(str(p.relative_to(plan["repo"])) for x in paths for p in (plan["repo"] / x).rglob("*") if p.is_file())
        if [staged[f] for f in files] != hashed or files != on_disk:
            raise RuntimeError("스테이지 blob ↔ 디스크 바이트 대조 실패")
        after["files"]["staged"] = len(files)
        ok_so_far = not stopped and not problems and not run.followups
        hold = " · ⚠ 채택 보류 표지 (RECORD 밖 실행 경로 관련 파일)" if (run.adoption_hold or {}).get("hold") else ""
        if ok_so_far:
            title = f"REIL C4-ENV 새 세대 실행 기록 (S0–S9 · 자동 채택 없음 · 검토 대기){hold} — 새 봉인 {plan['N_rel'].split('/')[-1]}"
        else:
            why = run.stopped or {"step": "S10", "reason": f"보호 경로 변경 {problems[:3]}"}
            title = f"REIL C4-ENV 정지 기록 ({why['step']} · {why['reason']}) — 정지 상태의 기록 · 채택 아님{hold}"
        steps_s = " · ".join(f"{s['step']} {s['elapsed_s']}s" for s in run.steps)
        body = (f"{title}\n\n- 단계: {steps_s}\n"
                f"- t0 {run.t0_utc} · 커밋 전 기록 +{end['written_rel']} s · S10 결과 · 한도 판정은 커밋 밖 11_after_commit.json\n"
                f"- 파일 {len(files)} · 스테이지 blob = 디스크 바이트 (전수) · 비밀값 검사 0 건\n\n{TRAILER}")
        argv = ["git", "-C", str(plan["repo"]), "commit", "-q", "-F", "-"]
        tmo = min(run.group_left(), run.total_left())
        if tmo < 5.0:
            after["commit"]["skipped_reason"] = "S10 또는 전체 배정이 5 s 미만 남음 — commit 을 시작하지 않음 (스테이지는 됨)"
            raise RuntimeError(after["commit"]["skipped_reason"])
        after["commit"].update({"attempted": True, "argv": argv[3:]})
        try:
            cp = subprocess.run(argv, input=body, capture_output=True, text=True, timeout=tmo)
            after["commit"].update({"rc": cp.returncode, "timed_out": False, "stderr_tail": cp.stderr[-400:]})
        except subprocess.TimeoutExpired:
            after["commit"].update({"rc": None, "timed_out": True,
                                    "index_lock_present": (plan["repo"] / ".git" / "index.lock").exists()})
        head_after = run.git("rev-parse", "HEAD", timeout=30).stdout.strip()
        after["commit"]["head_after"] = head_after or None
        after["commit"]["new_commit"] = bool(head_after and head_after != head_before)
        after["protected_changed"] = problems
    except Stopped:
        pass
    except Exception as exc:                     # 첫 원인을 덮지 않고 따로 남긴다
        rec = {"step": "S10", "reason": f"{type(exc).__name__}: {str(exc)[:300]}", "utc": utc(), "t_rel": run.rel()}
        if run.stopped is None:
            run.stopped = rec
            if run.E.exists() and not (run.E / "STOP.json").exists():
                dump(run.E / "STOP.json", rec)
        else:
            run.followups.append(rec)
        after["stopped"], after["followups"] = run.stopped, run.followups
    end_rel = run.rel()
    after["s10"].update({"end_rel": end_rel, "elapsed_s": round(end_rel - s10_start, 3)})
    after["s10"]["within"] = after["s10"]["elapsed_s"] <= plan["s10_allot"]
    after["total"].update({"end_rel": end_rel, "within": end_rel <= plan["total_s"]})
    try:
        d = run.du()
        after["disk"].update({"after_commit": d["du_sb_total"], "within": d["du_sb_total"] <= plan["disk_limit"]})
    except Exception as exc:
        after["disk"]["error"] = f"{type(exc).__name__}: {exc}"
    after["ok"] = bool(not run.stopped and not run.followups and after["commit"]["rc"] == 0 and after["commit"]["new_commit"]
                       and after["s10"]["within"] and after["total"]["within"] and after["disk"]["within"] and not after.get("protected_changed"))
    out = plan["R"] / "11_after_commit.json"
    if plan["R"].exists():
        dump(out, after)
    run.log(f"S10 done ok={after['ok']} commit_rc={after['commit']['rc']} +{end_rel}s")
    return 0 if after["ok"] else 1


def main(argv=None, plan=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv not in (["precheck"], ["run"]):
        print(__doc__, file=sys.stderr)
        return 2
    plan = plan or production_plan()
    run = Run(plan, argv[0])
    if argv[0] == "precheck":
        info, P, _ = checks(run)
        print(json.dumps({"mode": "precheck", "problems": P, "info": info, "runner_sha256": info["runner"]["sha256"],
                          "t0_utc": run.t0_utc}, ensure_ascii=False, indent=1, default=str))
        return 0 if not P else 2
    stopped = False
    try:
        s0(run)
        groups(run)
    except Stopped:
        stopped = True
    except SystemExit:
        raise
    except BaseException as exc:                 # 예상 밖 예외도 첫 원인으로 남기고 멈춘다 (기록 폴더 전이면 stderr 의 traceback 이 유일한 원문)
        stopped = True
        traceback.print_exc()
        rec = {"step": "runner", "reason": f"예외 {type(exc).__name__}: {str(exc)[:300]}", "utc": utc(), "t_rel": run.rel()}
        if run.stopped is None:
            run.stopped = rec
            if run.E.exists() and not (run.E / "STOP.json").exists():
                dump(run.E / "STOP.json", rec)
        else:
            run.followups.append(rec)
    if not run.E.exists():
        return 2
    return s10(run, stopped)


if __name__ == "__main__":
    sys.exit(main())
