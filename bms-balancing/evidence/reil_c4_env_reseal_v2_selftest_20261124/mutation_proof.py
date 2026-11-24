"""변이 증명 v2 (2026-11-24 · 원장 §138 · v1 = ../reil_c4_env_reseal_selftest_20261124/mutation_proof.py 에 M13–M17 만 더함) — selftest.py 가 처음부터 다 통과했으므로 (CLAUDE.md 규율 2), 대조기의 검사 자리를 하나씩 일부러 끈 사본에서
selftest 를 돌려 그 자리를 겨냥한 사례가 실제로 FAIL 하는지 본다. 저장소는 읽기만 한다.

실행: 저장소 뿌리에서 `/usr/bin/python3.11 -I -B bms-balancing/evidence/reil_c4_env_reseal_v2_selftest_20261124/mutation_proof.py`.
TMPDIR 아래 임시 거울 트리 (대조기 · selftest 사본 + 10월 기록 · 봉인으로 가는 읽기용 심볼릭 링크) 에서만 돈다.
변이마다: 고친 줄이 정확히 한 번 바뀌었는지 · selftest rc 가 1 인지 · 기대한 사례가 FAIL 목록에 있는지. 하나라도 어긋나면 rc 1.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
TOOL_REL = "bms-balancing/scripts/reil_c4_env_reseal_check.py"
TEST_REL = "bms-balancing/evidence/reil_c4_env_reseal_v2_selftest_20261124/selftest.py"
LINKS = ("bms-balancing/evidence/reil_c4_env_20261013", "bms-balancing/reil_c6_rebuild_20261013")

#: (이름, 바꿀 원문, 바꿀 내용, 반드시 FAIL 해야 할 사례 머리)
MUTANTS = [
    ("M1 중복 경로 검사 끔", '        if row[0] in seen:\n', '        if False:\n', ["R4"]),
    ("M2 줄 끝 종류 무시 (줄 수만)", "    if o_ends != n_ends:\n", "    if len(o_ends) != len(n_ends):\n", ["R2"]),
    ("M3 wrapper 본문 결속 끔 (첫 줄만 봄)",
     "            if (record_hash(back), str(len(back))) != (old_row[1], old_row[2]):\n", "            if False:\n", ["R5", "R14b"]),
    ("M4 다른 dist-info 행 규칙 끔", '            if top.endswith(".dist-info") and top != own:\n', "            if False:\n", ["R8"]),
    ("M5 설치 바이트 대조 끔", "        elif got != (h, size):\n", "        elif False:\n", ["R11"]),
    ("M6 lock 바이트 대조 끔", '        same = e is not None and nd[n] == e\n',
     '        same = e is not None and (nd[n] == e or n == "REIL_C6.lock.txt")\n', ["S2", "S3", "S9"]),
    ("M7 ensurepip 구성원 차이 묵인",
     '                    rep["problems"].append(f"{name}: 구성원 {path} 가 옛 설치 RECORD 와 다름 (선언 밖)")\n',
     "                    pass\n", ["B2"]),
    ("M8 wheel sha256 무시 (크기만)", "for n in sorted(set(got) & set(want)) if got[n] != want[n]]",
     "for n in sorted(set(got) & set(want)) if got[n][0] != want[n][0]]", ["W2"]),
    ("M9 설명된 충돌의 디스크 대조 끔", "            if got != tuple(owner):\n", "            if False:\n", ["R18"]),
    ("M10 선언 행의 값 대조 끔", "        if want and (o[1], o[2]) == want[0] and (n[1], n[2]) == want[1]:\n", "        if want:\n", ["R10"]),
    ("M11 wrapper 를 같은 행이면 건너뜀", "        if n[0].startswith(prefix):", "        if n[0].startswith(prefix) and o != n:", ["R7"]),
    ("M12 pytest_t 의 ../../bin → target/bin 대응 끔", '    if kind == "target" and rel.startswith(WRAPPER_PREFIX["target"]):\n',
     "    if False:\n", ["R1"]),
    # v2 (검토 §137) — 새 검사 자리
    ("M13 배포판 식별 중복 거부 끔 (ENV18-C2)", "            if len(names) > 1:\n", "            if False:\n", ["R21", "R21b", "R21c"]),
    ("M14 실행 경로 관련 분류 끔 (채택 보류 표지)", "                ex = p.suffix in EXEC_SUFFIXES\n", "                ex = False\n", ["R23", "R23b"]),
    ("M15 seal 의 S9a 허용 확인 끔", '    if rr.get("allowed_only") is not True:\n', "    if False:\n", ["S12"]),
    ("M16 seal 의 보존 RECORD ↔ S9a sha 결속 끔", "    if want != got:\n", "    if False:\n", ["S11"]),
    ("M17 RECORD 밖 목록을 50 개로 자름 (v1 처럼)", '"unlisted": unlisted,', '"unlisted": unlisted[:50],', ["R22"]),
]
#: 1 차 (run1_*) 기록: M3 의 기대에 R14 를 적었으나 R14 는 RECORD↔바이트 검사로도 잡혀 M3 에서 FAIL 하지 않았다 — 시험 쪽 빈틈.
#: R14b 를 더하고 기대를 R14b 로 고쳤다 (대조기 코드는 그대로).


def mirror(root: Path, tool_text: str) -> Path:
    m = root / "repo"
    (m / TOOL_REL).parent.mkdir(parents=True)
    (m / TOOL_REL).write_text(tool_text, encoding="utf-8")
    (m / TEST_REL).parent.mkdir(parents=True)
    shutil.copyfile(REPO / TEST_REL, m / TEST_REL)
    for rel in LINKS:
        (m / rel).parent.mkdir(parents=True, exist_ok=True)
        os.symlink(REPO / rel, m / rel)
    return m


def main() -> int:
    src = (REPO / TOOL_REL).read_text(encoding="utf-8")
    bad = 0
    with tempfile.TemporaryDirectory(prefix="reseal_mut_") as tmp:
        for i, (name, old, new, must) in enumerate([("M0 변이 없음 (대조군)", "", "", [])] + MUTANTS):
            if old:
                n = src.count(old)
                if n != 1:
                    print(f"FAIL {name} — 바꿀 줄이 {n} 번 나온다 (정확히 1 이어야)")
                    bad += 1
                    continue
                text = src.replace(old, new)
            else:
                text = src
            m = mirror(Path(tmp) / f"m{i}", text)
            r = subprocess.run([sys.executable, "-I", "-B", str(m / TEST_REL)], cwd=str(m), capture_output=True, text=True, timeout=300)
            failed = [ln.split()[1] for ln in r.stdout.splitlines() if ln.startswith("FAIL ")]
            last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
            if not old:
                ok = r.returncode == 0 and not failed
            else:
                ok = r.returncode == 1 and all(x in failed for x in must)
            bad += not ok
            print(f"{'PASS' if ok else 'FAIL'} {name} — selftest rc {r.returncode} · {last} · FAIL 사례 {failed} · 기대 {must}")
    print(f"변이 증명: {len(MUTANTS) + 1 - bad} / {len(MUTANTS) + 1} 기대대로")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
