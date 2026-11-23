#!/usr/bin/env python3
"""매주 새 회차 반영 — 받기 → (새 회차가 있으면) 분석 → 테스트. git 은 건드리지 않는다.

    python lottery/weekly_update.py           # 종료 코드 0 = 새 회차 반영·테스트 통과, 3 = 새 회차 없음
    python lottery/weekly_update.py --force   # 새 회차가 없어도 분석·테스트를 돈다 (점검용)

종료 코드 0 이면 예약 작업이 lottery/data · lottery/results · lottery/RESULTS.md 를 커밋해
claude/lottery-site 에 push 하고, Cloudflare Pages 가 lotto.bmlwork.kr 을 다시 빌드한다.
새 회차가 없으면 받은 파일을 원래대로 되돌린다 (받은 시각만 바뀐 MANIFEST 로 빈 커밋을 만들지 않는다).
받기가 검증에 걸리면 종료 코드 1 — 가진 목록보다 회차가 줄었거나 옛 회차 값이 바뀐 응답도
여기 든다 (fetch_data.py 가 파일을 쓰기 전에 거부한다). 분석이나 테스트가 실패하면 2.
둘 다 커밋하지 말고 사람에게 알린다.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
MANIFEST = DATA / "raw" / "MANIFEST.json"


def _latest() -> dict[str, int]:
    files = json.loads(MANIFEST.read_text(encoding="utf-8"))["files"]
    return {name: f["latest_round"] for name, f in files.items()}


def _run(args: list[str], label: str) -> int:
    print(f"── {label}: {' '.join(args)}", flush=True)
    return subprocess.run([sys.executable, *args], cwd=ROOT).returncode


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--force", action="store_true", help="새 회차가 없어도 분석·테스트를 돈다")
    args = ap.parse_args()

    before = _latest()
    backup = Path(tempfile.mkdtemp(prefix="lottery-data-"))
    shutil.copytree(DATA, backup / "data")
    try:
        if _run(["fetch_data.py"], "받기") != 0:
            print("받기 실패 — 접속 실패, 원본 검증 실패, 또는 회차가 줄었거나 옛 회차가 바뀐 응답"
                  " (위 메시지). 사람이 확인한다.")
            return 1
        after = _latest()
        # fetch_data.py 가 회차가 줄거나 옛 회차가 바뀐 응답을 거부하므로 여기서 바뀌었다 = 늘었다 (A1·A2)
        new = {k: (before[k], after[k]) for k in after if after[k] != before[k]}
        if not new and not args.force:
            shutil.rmtree(DATA)
            shutil.copytree(backup / "data", DATA)  # 받은 시각만 바뀐 MANIFEST·CSV 를 되돌린다
            print(f"새 회차 없음 — 로또 {after['lotto645.json']}회 · 연금 {after['pension720.json']}회 그대로. 파일을 되돌렸다.")
            return 3
        if _run(["build_results.py"], "분석") != 0:
            return 2
        if _run(["-m", "pytest", "tests", "-q", "-p", "no:cacheprovider"], "테스트") != 0:
            return 2
        parts = [f"{'로또' if k == 'lotto645.json' else '연금'} {a}→{b}회" for k, (a, b) in new.items()]
        print("반영:", ", ".join(parts) if parts else "새 회차 없음 (--force)")
        return 0
    finally:
        shutil.rmtree(backup, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
