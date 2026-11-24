"""REIL C4-ENV 실행기 — bms-balancing/docs/REIL_C4_ENV_APPROVAL_REQUEST_20261013.md §2 의 argv 를 순서대로 그대로 부른다.

승인: bms-balancing/docs/REIL_PREREQUISITES_STATUS_20261004.md §36 (사용자 2026-10-13 "권고대로").
실행: /usr/bin/python3.11 -I <이 파일>. 재시도 · 다른 경로 · 다른 interpreter · 추가 명령 없음 — 실패하면 첫 오류와 확보된 기록을 남기고 멈춘다.
보존 안전장치 (계산 아님): S1–S9 자식 env 에서 비밀 형태 변수를 뺀다 (이름만 기록) · 커밋 전 기록에 그 값이 들어갔는지 검사한다.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

REPO = Path("/home/user/Yonghoon-DEM-DFT")
SP = Path("/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/b881d255-9513-5adc-9b14-3c0be18d7ad6/scratchpad")
R = SP / "reil_c4env"
VENV = R / "venv"
V = str(VENV / "bin" / "python")
PY = "/usr/bin/python3.11"
C = "bms-balancing/evidence/reil_p0_20261006/01_venv_constraints.txt"
P0_LOG = "bms-balancing/evidence/reil_p0_20261006/01_venv_pip_install.stdout"
COMPARE = "bms-balancing/scripts/reil_c4_env_compare.py"
PROFILE_SCRIPT = "bms-balancing/scripts/reil_c6_profile.py"
BUNDLED = Path("/usr/lib/python3.11/ensurepip/_bundled")
E_REL = "bms-balancing/evidence/reil_c4_env_20261013"
NEW_REL = "bms-balancing/reil_c6_rebuild_20261013"
OLD_REL = "bms-balancing/reil_c6_rebuild_20261006"
E, NEW = REPO / E_REL, REPO / NEW_REL
REQUEST = "bms-balancing/docs/REIL_C4_ENV_APPROVAL_REQUEST_20261013.md"
REQUEST_SHA = "47af94d1eba4a8be885566aada162afbeb5fa8a792105dce19650b84cd76554d"
V2 = "bms-balancing/docs/REIL_C4_APPROVAL_REQUEST_v2_20261013.md"
V2_SHA = "22dcc8e5ef6430253f55834743e10808b0c3547c8fb560d0ad415dce77da8f87"
REQUEST_COMMIT = "98dec16a59497f1633e58ef449bf6747dd398eb8"
APPROVAL_COMMIT = "e5b7a254cfabc21047673d715bffc53b26350dd8"
TOTAL_S, DISK_LIMIT, FREE_MIN = 1800.0, 2_000_000_000, 4_000_000_000
SCI = ["numpy==2.4.6", "scipy==1.17.1", "pandas==3.0.5", "openpyxl==3.1.5", "matplotlib==3.11.2", "seaborn==0.13.2", "pymoo==0.6.2"]
TEST = ["pytest==9.1.1", "pluggy==1.6.0", "iniconfig==2.3.0", "pygments==2.21.0"]
PIP = ["--no-cache-dir", "--disable-pip-version-check"]
VERSION, BUILD = "3.11.17", ["main", "Oct  1 2026 15:41:07"]
EXPECT = {"version": VERSION, "build": BUILD, "implementation": "CPython", "system": "Linux", "machine": "x86_64", "libc": "glibc 2.39",
          "is_symlink": False, "size": 6644312, "sha256": "73bf4b06fad87996a59b3c0810eb127b91e84846d21e563862fb4acf74fbcb99"}
EXPECT_DEB = {"python3.11-minimal": "3.11.17-1+noble1", "libpython3.11-stdlib": "3.11.17-1+noble1", "python3.11-venv": "3.11.17-1+noble1"}
EXPECT_BUNDLED = {"pip-24.0-py3-none-any.whl": "ba0d021a166865d2265246961bec0152ff124de910c5cc39f1156ce3fa7c69dc",
                  "setuptools-79.0.1-py3-none-any.whl": "e147c0549f27767ba362f9da434eab9c5dc0045d5304feb602a0af001089fc51"}
PROTECTED_TREES = {
    "bms-balancing/reil_c6_20261005": "3ec46373da366265242e92df9c6e112e5ff100e0",
    "bms-balancing/reil_c6_rebuild_20261006": "b55f3a439e23bd41626d64bbb40b8221571f8690",
    "bms-balancing/evidence/reil_c6_n1_20261006": "fdd12a5f30dc52242e0553b6b616c463a264fe54",
    "bms-balancing/evidence/reil_p0_20261006": "82a74d69c3f3cad363d6f120fe0e88658af0a496",
    "bms-balancing/evidence/reil_c5_impl_20261006": "cfea813242c2d47f559a3807c5bab1bb63f3e183",
    "bms-balancing/evidence/reil_c5_pilot_20261006": "514e4dcd284f831a92e158ad4542136cc455f018",
    "bms-balancing/evidence/reil_c5_pilot_20261006_wrapper": "6238fff9ff7bc6a54747f28653eca4e3f1b20a2d",
}
PROTECTED_FILES = {
    PROFILE_SCRIPT: "408afc4bb5eb1069583b955e0eb6215bf48dd9259ad474c230549d1b3642df5d",
    "degradation-degeneracy/tools/env_profile.py": "83b0d8365d039d75050d087fe980ad7b64818686b699e5d06da1c0ad63148563",
    COMPARE: "eff94d3dfd4b3d31c7a19e440dfb968734dab1afb16b584c2fdee354100695e0",
    "bms-balancing/scripts/reil_c5_pilot.py": "73bee8dc412b39863afb64b70bc128cbecee2075a3a17914fc7288f353ef11a6",
    C: "db63333bdaf1835444a86187215ed7faf06897eb8a247c667ed167a5ee1dc772",
}
GUARDED = ["bms-balancing/scripts", "degradation-degeneracy/tools/env_profile.py", *PROTECTED_TREES]
SECRET_NAME = re.compile(r"TOKEN|SECRET|PASSW|ACCESS_KEY|CREDENTIAL|COOKIE|^GIT_CONFIG_", re.I)
STRIPPED = sorted(k for k in os.environ if SECRET_NAME.search(k))
SECRET_VALUES = {k: v for k, v in os.environ.items() if SECRET_NAME.search(k) and len(v) >= 8
                 and not k.endswith("_FILE") and not k.startswith("GIT_CONFIG_KEY_") and k != "GIT_CONFIG_COUNT"}
TRAILER = ("Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n"
           "Claude-Session: https://claude.ai/code/session_0157zrP6GFu6cJF5x8CwZaEm\n")
STATE = {"t0_utc": None, "t0_mono": None, "steps": [], "disk": [], "stopped": None, "finalizing": False}


def utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def rel() -> float:
    return round(time.monotonic() - STATE["t0_mono"], 3)


def sha_file(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def dump(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=1) + "\n", encoding="utf-8")


def git(*args, timeout=60, **kw):
    return subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True, timeout=timeout, **kw)


def log(msg: str) -> None:
    print(f"[{utc()} +{rel() if STATE['t0_mono'] else 0:.1f}s] {msg}", flush=True)


def disk(label: str) -> None:
    parts, total = {}, 0
    for p in (R, NEW, E):
        if p.exists():
            n = int(subprocess.run(["du", "-sb", str(p)], capture_output=True, text=True, timeout=60).stdout.split()[0])
            parts[str(p)] = n
            total += n
    obs = {"label": label, "utc": utc(), "t_rel": rel(), "du_sb_total": total, "du_sb_parts": parts,
           "free_bytes": shutil.disk_usage(str(REPO)).free}
    STATE["disk"].append(obs)
    log(f"disk {label}: {total} B")
    if total > DISK_LIMIT and not STATE["finalizing"]:
        stop(label, f"디스크 합계 {total} B > {DISK_LIMIT} B")


def run(sid: str, argv: list, extra: dict, allot: float, network: str) -> dict:
    remaining = TOTAL_S - (time.monotonic() - STATE["t0_mono"])
    if allot <= 0:
        stop(sid, "단계 배정 소진 — 이 단계를 시작하지 않음")
    if remaining <= 0:
        stop(sid, "전체 1,800 s 소진 — 이 단계를 시작하지 않음")
    timeout = min(allot, remaining)
    env = {k: v for k, v in os.environ.items() if not SECRET_NAME.search(k)}
    env.update(extra)
    meta = {"step": sid, "argv": argv, "cwd": str(REPO), "env_set": extra, "env_removed_names": STRIPPED, "network": network,
            "allot_s": allot, "timeout_s": round(timeout, 3), "start_utc": utc(), "start_rel": rel()}
    log(f"{sid} start (timeout {timeout:.0f}s)")
    t = time.monotonic()
    rc, timed_out = None, False
    with open(E / f"{sid}.stdout.log", "wb") as fo, open(E / f"{sid}.stderr.log", "wb") as fe:
        try:
            rc = subprocess.run(argv, cwd=str(REPO), env=env, stdout=fo, stderr=fe, timeout=timeout).returncode
        except subprocess.TimeoutExpired:
            timed_out = True
    meta.update({"end_utc": utc(), "end_rel": rel(), "elapsed_s": round(time.monotonic() - t, 3), "rc": rc, "timed_out": timed_out})
    dump(E / f"{sid}.meta.json", meta)
    STATE["steps"].append({k: meta[k] for k in ("step", "rc", "timed_out", "elapsed_s", "start_rel", "end_rel", "timeout_s")})
    log(f"{sid} end rc={rc} timed_out={timed_out} elapsed={meta['elapsed_s']}s")
    if timed_out:
        stop(sid, f"timeout {round(timeout, 3)} s")
    if rc != 0:
        stop(sid, f"rc {rc}")
    return meta


def approval_text() -> str:
    lines = (REPO / REQUEST).read_text(encoding="utf-8").splitlines()
    i = next(n for n, ln in enumerate(lines) if ln.startswith("## §6"))
    j = next(n for n, ln in enumerate(lines) if ln.startswith("## §7"))
    block = "\n".join(lines[i + 1:j]).strip()
    return (f"# C4-ENV 승인 원문 사본 (실행 기록용)\n\n"
            f"- 사용자 원문 (2026-10-13): \"권고대로\"\n"
            f"- 해석 기록: `bms-balancing/docs/REIL_PREREQUISITES_STATUS_20261004.md` §36 (커밋 `{APPROVAL_COMMIT}`) — "
            f"(A) C4-ENV 승인 (요청 §6) · (B) C4-0 범위 재확인 (v2 §8 · 효력은 새 봉인 검토 수용 뒤)\n"
            f"- 요청 문서: `{REQUEST}` · sha256 `{REQUEST_SHA}` (요청 커밋 `{REQUEST_COMMIT}`)\n"
            f"- C4 요청 v2: `{V2}` · sha256 `{V2_SHA}`\n"
            f"- t0: {STATE['t0_utc']} (monotonic 원점 · 각 meta 의 *_rel 은 이 원점에서 잰 초)\n\n"
            f"## 요청 §6 채택 문구 (요청 문서에서 그대로 옮김)\n\n{block}\n")


def precheck() -> tuple:
    """S0 의 읽기 전용 부분 — 만들거나 쓰지 않는다 (실행 전 점검에도 쓴다)."""
    t = time.monotonic()
    pre = {"t0_utc": STATE["t0_utc"], "problems": []}
    P = pre["problems"]
    pre["runner"] = {"sys_executable": sys.executable, "isolated": bool(sys.flags.isolated)}
    if os.path.realpath(sys.executable) != PY or not sys.flags.isolated:
        P.append({"runner_interpreter": pre["runner"]})
    pre["head"] = git("rev-parse", "HEAD").stdout.strip()
    for name, commit in (("request", REQUEST_COMMIT), ("approval", APPROVAL_COMMIT)):
        if git("merge-base", "--is-ancestor", commit, "HEAD").returncode != 0:
            P.append(f"{name} 커밋 {commit} 이 HEAD 의 조상이 아님")
    changed = git("diff", "--name-only", REQUEST_COMMIT, "HEAD", "--", *GUARDED).stdout.split()
    if changed:
        P.append({"요청 커밋 뒤 바뀐 보호 경로": changed})
    porcelain = git("status", "--porcelain=v1", "--untracked-files=all").stdout
    dirty = git("status", "--porcelain=v1", "--untracked-files=all", "--", *GUARDED).stdout
    if dirty.strip():
        P.append({"보호 경로 작업트리 변경": dirty.splitlines()})
    pre["porcelain_start_lines"] = len(porcelain.splitlines())
    pre["trees"] = {p: git("rev-parse", f"HEAD:{p}").stdout.strip() for p in PROTECTED_TREES}
    P += [{"tree": p, "want": w, "got": pre["trees"][p]} for p, w in PROTECTED_TREES.items() if pre["trees"][p] != w]
    pre["files"] = {p: sha_file(REPO / p) for p in PROTECTED_FILES}
    P += [{"file": p, "want": w, "got": pre["files"][p]} for p, w in PROTECTED_FILES.items() if pre["files"][p] != w]
    pre["documents"] = {REQUEST: sha_file(REPO / REQUEST), V2: sha_file(REPO / V2)}
    if pre["documents"] != {REQUEST: REQUEST_SHA, V2: V2_SHA}:
        P.append({"documents": pre["documents"]})
    interp = {"path": PY, "is_symlink": os.path.islink(PY), "size": os.path.getsize(PY), "sha256": sha_file(PY),
              "version": platform.python_version(), "build": list(platform.python_build()),
              "implementation": platform.python_implementation(), "system": platform.system(), "machine": platform.machine(),
              "libc": " ".join(platform.libc_ver()).strip(), "sys_version": sys.version}
    pre["interpreter"] = interp
    P += [{"interpreter": k, "want": w, "got": interp[k]} for k, w in EXPECT.items() if interp[k] != w]
    deb = {pkg: subprocess.run(["dpkg-query", "-W", "-f=${Version}", pkg], capture_output=True, text=True, timeout=10).stdout
           for pkg in EXPECT_DEB}
    pre["deb"] = deb
    P += [{"deb": k, "want": w, "got": deb[k]} for k, w in EXPECT_DEB.items() if deb[k] != w]
    pre["ensurepip_bundled"] = {p.name: sha_file(p) for p in sorted(BUNDLED.iterdir())}
    if pre["ensurepip_bundled"] != EXPECT_BUNDLED:
        P.append({"ensurepip_bundled": pre["ensurepip_bundled"]})
    pre["paths_exist"] = {str(p): p.exists() for p in (R, NEW, E)}
    P += [{"path_exists": k} for k, v in pre["paths_exist"].items() if v]
    pre["free_bytes"] = shutil.disk_usage(str(REPO)).free
    pre["df_B1"] = subprocess.run(["df", "-B1", str(REPO), str(SP)], capture_output=True, text=True, timeout=10).stdout
    if pre["free_bytes"] < FREE_MIN:
        P.append({"free_bytes": pre["free_bytes"]})
    pre["env_removed_names_for_children"] = STRIPPED
    pre["elapsed_s"] = round(time.monotonic() - t, 3)
    if pre["elapsed_s"] > 60:
        P.append("S0 60 s 초과")
    return pre, porcelain


def s0() -> None:
    t = time.monotonic()
    pre, porcelain = precheck()
    P = pre["problems"]
    if P:
        print(json.dumps(pre, ensure_ascii=False, indent=1))
        log("S0 사전 조건 실패 — 시작하지 않음 (기록 폴더를 만들지 않았다)")
        sys.exit(2)
    R.mkdir()
    (R / "tmp").mkdir()
    E.mkdir()
    (E / "00_porcelain_start.txt").write_text(porcelain, encoding="utf-8")
    shutil.copyfile(__file__, E / "00_runner.py")
    pre["runner_copy_sha256"] = sha_file(E / "00_runner.py")
    dump(E / "00_s0_precheck.json", pre)
    (E / "00_approval.md").write_text(approval_text(), encoding="utf-8")
    STATE["steps"].append({"step": "S0", "rc": 0, "timed_out": False, "elapsed_s": round(time.monotonic() - t, 3),
                           "start_rel": 0.0, "end_rel": rel(), "timeout_s": 60})
    log(f"S0 ok head={pre['head'][:12]} free={pre['free_bytes']}")


def secret_scan() -> list:
    hits = []
    for root in (E, NEW):
        if not root.exists():
            continue
        for p in sorted(root.rglob("*")):
            if p.is_file():
                b = p.read_bytes()
                hits += [{"file": str(p.relative_to(REPO)), "env_name": k} for k, v in SECRET_VALUES.items() if v.encode() in b]
    return hits


def finalize(stopped: bool) -> int:
    STATE["finalizing"] = True
    t = time.monotonic()
    rec = {"start_utc": utc(), "start_rel": rel(), "stopped": STATE["stopped"]}
    tt = R / "pytest_t"
    if tt.exists():
        out = E / "10_test_tool_records"
        out.mkdir()
        rows = {}
        for di in sorted(tt.glob("*.dist-info")):
            raw = (di / "RECORD").read_bytes()
            (out / f"{di.name}.RECORD").write_bytes(raw)
            text = (di / "RECORD").read_text(encoding="utf-8")
            rows[di.name] = {"record_raw_sha256": hashlib.sha256(raw).hexdigest(),
                             "record_text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()}
        rec["test_tool_records"] = rows
    (E / "10_porcelain_end.txt").write_text(git("status", "--porcelain=v1", "--untracked-files=all").stdout, encoding="utf-8")
    rec["head_end"] = git("rev-parse", "HEAD").stdout.strip()
    rec["protected_trees_end"] = {p: git("rev-parse", f"HEAD:{p}").stdout.strip() for p in PROTECTED_TREES}
    rec["protected_files_end"] = {p: sha_file(REPO / p) for p in PROTECTED_FILES}
    rec["protected_worktree_dirty_end"] = git("status", "--porcelain=v1", "--untracked-files=all", "--", *GUARDED).stdout.splitlines()
    problems = [p for p, w in PROTECTED_TREES.items() if rec["protected_trees_end"][p] != w]
    problems += [p for p, w in PROTECTED_FILES.items() if rec["protected_files_end"][p] != w]
    problems += rec["protected_worktree_dirty_end"]
    rec["protected_changed"] = problems
    disk("S10")
    if STATE["disk"][-1]["du_sb_total"] > DISK_LIMIT:
        problems.append(f"S10 디스크 합계 {STATE['disk'][-1]['du_sb_total']} B > {DISK_LIMIT} B")
    if time.monotonic() - STATE["t0_mono"] > TOTAL_S:
        problems.append(f"전체 {TOTAL_S} s 초과 (+{rel()} s)")
    rec["disk"] = STATE["disk"]
    rec["steps"] = STATE["steps"]
    rec["end_utc"], rec["end_rel"] = utc(), rel()
    rec["elapsed_s_records"] = round(time.monotonic() - t, 3)
    rec["note"] = "end_rel 은 커밋 직전 · 커밋 시각은 git 기록 · push 는 1,800 s 밖"
    dump(E / "10_end.json", rec)
    hits = secret_scan()
    if hits:
        print(json.dumps(hits, ensure_ascii=False, indent=1))
        log("비밀값 검사 실패 — 커밋하지 않고 멈춘다 (사람 확인 필요)")
        return 3
    paths = [x for x in (NEW_REL, E_REL) if (REPO / x).exists()]
    git("add", "-f", "--", *paths)
    staged = {}
    for ln in git("ls-files", "-s", "--", *paths).stdout.splitlines():
        meta, path = ln.split("\t", 1)
        staged[path] = meta.split()[1]
    files = sorted(staged)
    hashed = git("hash-object", "--stdin-paths", input="\n".join(files) + "\n").stdout.split()
    on_disk = sorted(str(p.relative_to(REPO)) for x in paths for p in (REPO / x).rglob("*") if p.is_file())
    mism = [f for f, h in zip(files, hashed) if staged[f] != h]
    if mism or files != on_disk:
        log(f"스테이지 대조 실패 — 커밋하지 않음 mism={mism[:5]} missing={sorted(set(on_disk) - set(files))[:5]}")
        return 4
    ok = not stopped and not problems
    steps = " · ".join(f"{s['step']} {s['elapsed_s']}s" for s in STATE["steps"])
    last_disk = STATE["disk"][-1]["du_sb_total"] if STATE["disk"] else None
    if ok:
        title = (f"REIL C4-ENV 실행 기록 (승인 §36 · S0–S10 · {rel():.1f} s · 디스크 {last_disk} B) — 새 봉인 {NEW_REL.split('/')[-1]}"
                 f" (검토 수용 전 · C4 환경 아님)")
    else:
        why = STATE["stopped"] or {"reason": f"보호 경로 변경 {problems[:3]}"}
        title = f"REIL C4-ENV 정지 기록 ({why.get('step', 'S10')} · {why['reason']}) — 정지 상태의 기록 · 채택 아님"
    body = (f"{title}\n\n- 단계: {steps}\n- t0 {STATE['t0_utc']} · 기록 끝 +{rel():.1f} s (1,800 s 한도 · push 는 한도 밖)\n"
            f"- 파일 {len(files)} 개 · 스테이지 blob = 디스크 바이트 (전수) · 비밀값 검사 0 건\n"
            f"- 자동 채택 없음 — old→new 차이표 · 새 MANIFEST 를 검토자에게 내고 멈춘다 (요청 §4)\n\n{TRAILER}")
    cp = git("commit", "-q", "-F", "-", input=body)
    log(f"commit rc={cp.returncode} {cp.stderr.strip()[:200]} — +{rel():.1f}s")
    return 0 if (ok and cp.returncode == 0) else 1


def stop(sid: str, reason: str):
    STATE["stopped"] = {"step": sid, "reason": reason, "utc": utc(), "t_rel": rel()}
    log(f"STOP {sid}: {reason}")
    if E.exists():
        dump(E / "STOP.json", STATE["stopped"])
        rc = finalize(stopped=True)
        log(f"정지 기록 마감 rc={rc}")
    sys.exit(1)


def main() -> int:
    STATE["t0_mono"], STATE["t0_utc"] = time.monotonic(), utc()
    s0()
    pipenv = {"TMPDIR": str(R / "tmp"), "PIP_CONFIG_FILE": "/dev/null"}
    tmpenv = {"TMPDIR": str(R / "tmp")}
    pyenv = {"TMPDIR": str(R / "tmp"), "PYTHONDONTWRITEBYTECODE": "1"}
    run("01_venv", [PY, "-I", "-m", "venv", str(VENV)], tmpenv, 120, "0")
    run("02_download_science", [V, "-I", "-m", "pip", "download", *PIP, "--only-binary=:all:", "--dest", str(R / "wheels"), "-c", C, *SCI],
        pipenv, 480, "PyPI")
    disk("S2")
    run("03_download_test", [V, "-I", "-m", "pip", "download", *PIP, "--only-binary=:all:", "--no-deps", "--dest", str(R / "wheels_test"),
                             *TEST], pipenv, 120, "PyPI")
    disk("S3")
    s4 = time.monotonic()
    run("04a_artifacts_science", [PY, "-I", COMPARE, "artifacts", "--wheels", str(R / "wheels"), "--expect-log", P0_LOG,
                                  "--out", f"{E_REL}/04_artifacts_science.json"], tmpenv, 30, "0")
    run("04b_artifacts_test", [PY, "-I", COMPARE, "artifacts", "--wheels", str(R / "wheels_test"), "--expect-dists", ",".join(TEST),
                               "--out", f"{E_REL}/04_artifacts_test.json"], tmpenv, max(0.0, 30 - (time.monotonic() - s4)), "0")
    run("05_install_science", [V, "-I", "-m", "pip", "install", *PIP, "--no-index", "--find-links", str(R / "wheels"), "-c", C, *SCI],
        pipenv, 300, "0")
    disk("S5")
    run("06_install_test", [V, "-I", "-m", "pip", "install", *PIP, "--no-index", "--find-links", str(R / "wheels_test"), "--no-deps",
                            "--target", str(R / "pytest_t"), *TEST], pipenv, 120, "0")
    disk("S6")
    run("07_emit", [V, PROFILE_SCRIPT, "emit", NEW_REL], pyenv, 180, "0")
    run("08_check", [V, PROFILE_SCRIPT, "check", NEW_REL], pyenv, 180, "0")
    if b"check OK" not in (E / "08_check.stdout.log").read_bytes():
        stop("08_check", "rc 0 이지만 'check OK' 출력 없음")
    disk("S8")
    run("09_compare", [PY, "-I", COMPARE, "compare", "--old", OLD_REL, "--new", NEW_REL, "--venv", str(VENV),
                       "--wheels", str(R / "wheels"), "--wheels", str(BUNDLED), "--python-version", VERSION,
                       "--python-build", "|".join(BUILD), "--records-out", f"{E_REL}/09_records",
                       "--out", f"{E_REL}/09_old_new_diff.json"], tmpenv, 120, "0")
    rc = finalize(stopped=False)
    log(f"DONE rc={rc}")
    return rc


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except BaseException as exc:          # 예상 밖 예외도 첫 오류로 남기고 멈춘다
        if STATE["t0_mono"] is not None and not STATE["finalizing"]:
            stop("runner", f"예외 {type(exc).__name__}: {str(exc)[:300]}")
        raise
