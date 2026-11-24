"""실행기 · 하네스 변이 증명 (2026-11-24 · 원장 §138) — selftest_runner.py 의 사례가 겨냥한 자리를 하나씩 끈 사본에서 실제로 FAIL 하는지 본다.

RM1 은 샌드박스 시험 1 차가 잡은 결함 (실행기를 import 할 때 저장소에 pyc 가 생겨 보호 경로가 더러워짐) 을 되살린다 — 고치기 전 상태의 재현이다.
RM6 은 1 차 개발 실행 (`dev1_mutation_proof_runner.*` · 8 / 9) 에서 살아남은 변이다 — T2 를 강화한 뒤 같은 변이가 잡히는지 본다. RM6b 는 선행 요구 전부를 끈다.
RM9 는 요청서 경로 대조 (자체 검토로 더함 · RED = `red_runner.*` 의 T15) 를 끈다.
실행: 저장소 뿌리에서 `/usr/bin/python3.11 -I -B bms-balancing/evidence/reil_c4_env_reseal_v2_selftest_20261124/mutation_proof_runner.py`.
TMPDIR 아래 임시 거울 트리 (실행기 · 하네스 · 대조기 사본 + 10월 기록으로 가는 읽기용 링크) 에서만 돈다. 저장소는 읽기만 한다.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
RUN_REL = "bms-balancing/scripts/reil_c4_env_reseal_run.py"
HAR_REL = "bms-balancing/scripts/reil_c4_env_reseal_harness.py"
CHK_REL = "bms-balancing/scripts/reil_c4_env_reseal_check.py"
TEST_REL = "bms-balancing/evidence/reil_c4_env_reseal_v2_selftest_20261124/selftest_runner.py"
OCT_REL = "bms-balancing/evidence/reil_c4_env_20261013"

#: (이름, 파일, [(바꿀 원문, 바꿀 내용)], 반드시 FAIL 해야 할 사례 머리)
MUTANTS = [
    ("RM1 -B 를 뺌 (하네스 argv · 실행기 확인) — 1 차 결함의 재현", None,
     [(HAR_REL, '    cmd = [cfg["py"], "-I", "-B", str(runner), mode]', '    cmd = [cfg["py"], "-I", str(runner), mode]'),
      (RUN_REL, " or not sys.flags.isolated or not sys.flags.dont_write_bytecode:", " or not sys.flags.isolated:")], ["T1a"]),
    ("RM2 자식 env 에서 CA 변수를 빼지 않음 (ENV18-N1)", None,
     [(RUN_REL, '        r_ca = sorted(k for k in base if k in CA_NAMES)\n', '        r_ca = []\n')], ["T1f"]),
    ("RM3 그룹이 아니라 본 자식만 끊음", None,
     [(RUN_REL, "                os.killpg(p.pid, sig)\n            except ProcessLookupError:\n                break\n            end = time.monotonic() + wait\n            gone = False",
       "                os.kill(p.pid, sig)\n            except ProcessLookupError:\n                break\n            end = time.monotonic() + wait\n            gone = False")], ["T7"]),
    ("RM4 S10 의 뒤 오류가 첫 원인 자리를 차지함 (followups 로 안 감)", None,
     [(RUN_REL, "        rec = {\"step\": \"S10\", \"reason\": f\"{type(exc).__name__}: {str(exc)[:300]}\", \"utc\": utc(), \"t_rel\": run.rel()}\n        if run.stopped is None:",
       "        rec = {\"step\": \"S10\", \"reason\": f\"{type(exc).__name__}: {str(exc)[:300]}\", \"utc\": utc(), \"t_rel\": run.rel()}\n        if True:")], ["T9"]),
    ("RM5 S10 의 5 s 미만 보호 끔 (index.lock 위험)", None,
     [(RUN_REL, "        if min(run.group_left(), run.total_left()) < 5.0:     # git", "        if False:     # git")], ["T12"]),
    ("RM6 precheck 선행 확인 중 존재 검사만 뺌 (1 차 개발 실행에서 살아남음 → T2 강화)", None,
     [(RUN_REL, "    if not pre_ret.is_file():\n        P.append(", "    if False:\n        P.append(")], ["T2"]),
    ("RM6b precheck 선행 요구 전부 끔", None,
     [(RUN_REL, "    if not pre_ret.is_file():\n        P.append(\"precheck 의 바깥 반환이 없다 — precheck 1 회 뒤에만 실행한다\")\n    else:\n",
       "    if False:\n        P.append(\"precheck 의 바깥 반환이 없다 — precheck 1 회 뒤에만 실행한다\")\n    elif False:\n")], ["T2"]),
    ("RM7 승인 블록의 실행기 · 하네스 · 대조기 sha 대조 끔", None,
     [(RUN_REL, "            if at_head(rel) != blk[key] or sha_file(plan[\"repo\"] / rel) != blk[key]:", "            if False:")], ["T4"]),
    ("RM9 승인 블록의 요청서 경로 대조 끔 (red_runner 의 T15 재현)", None,
     [(RUN_REL, "        if blk[\"request\"][\"path\"] != plan[\"request_rel\"]:", "        if False:")], ["T15"]),
    ("RM8 남은 자식 검사 끔", None,
     [(RUN_REL, "            if not timed_out:\n                survivors = self._kill_group(p, only_if_alive=True)",
       "            if False:\n                survivors = self._kill_group(p, only_if_alive=True)")], ["T8"]),
]


def mirror(root: Path, edits) -> Path:
    m = root / "repo"
    texts = {rel: (REPO / rel).read_text(encoding="utf-8") for rel in (RUN_REL, HAR_REL, CHK_REL)}
    for rel, old, new in edits:
        n = texts[rel].count(old)
        if n != 1:
            raise ValueError(f"{rel}: 바꿀 원문이 {n} 번 나온다 — {old[:60]!r}")
        texts[rel] = texts[rel].replace(old, new)
    for rel, t in texts.items():
        (m / rel).parent.mkdir(parents=True, exist_ok=True)
        (m / rel).write_text(t, encoding="utf-8")
    (m / TEST_REL).parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(REPO / TEST_REL, m / TEST_REL)
    (m / OCT_REL).parent.mkdir(parents=True, exist_ok=True)
    os.symlink(REPO / OCT_REL, m / OCT_REL)
    return m


def main() -> int:
    bad = 0
    with tempfile.TemporaryDirectory(prefix="runner_mut_") as tmp:
        for i, (name, _, edits, must) in enumerate([("RM0 변이 없음 (대조군)", None, [], [])] + MUTANTS):
            try:
                m = mirror(Path(tmp) / f"m{i}", edits)
            except ValueError as exc:
                print(f"FAIL {name} — {exc}")
                bad += 1
                continue
            env = dict(os.environ)
            env["TMPDIR"] = str(Path(tmp) / f"m{i}")
            r = subprocess.run([sys.executable, "-I", "-B", str(m / TEST_REL)], cwd=str(m), capture_output=True, text=True, timeout=900, env=env)
            failed = [ln.split()[1] for ln in r.stdout.splitlines() if ln.startswith("FAIL ")]
            last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
            ok = (r.returncode == 0 and not failed) if not edits else (r.returncode == 1 and all(x in failed for x in must))
            bad += not ok
            print(f"{'PASS' if ok else 'FAIL'} {name} — selftest_runner rc {r.returncode} · {last} · FAIL 사례 {failed} · 기대 {must}", flush=True)
    print(f"실행기 변이 증명: {len(MUTANTS) + 1 - bad} / {len(MUTANTS) + 1} 기대대로")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
