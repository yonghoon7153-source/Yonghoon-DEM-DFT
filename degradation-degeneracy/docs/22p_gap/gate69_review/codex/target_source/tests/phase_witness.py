"""pytest plugin — **어느 node 가 어느 단계(setup · call · teardown)를 어떤 결말로 지났는가** 를 한 줄씩 적는다.

★ 68차 G68-T1 — JUnit XML 은 testcase 에 error/failure/skipped 자식이 없으면 "passed" 로 읽힌다.
  그런데 `--setup-only` child 는 fixture 만 준비하고 **call 단계를 생략**하면서도 testcase 를 자식 없이
  적는다 (pytest `pytest_runtest_protocol` 의 문서화된 동작). 그래서 rc 0 · 정확한 두 testcase · 자식
  없음 — 셋 다 맞는데 시험 본문은 한 줄도 안 돈 child 가 전제 회귀에 **ACCEPTED** 였다 (리뷰어 실측).

  이 plugin 은 pytest **내장 hook** (`pytest_runtest_logreport`) 만 쓴다 — 외부 plugin 을 요구하지 않는다.
  보고서가 나올 때마다 **즉시 append** 하므로 child 가 도중에 죽어도 그때까지의 단계는 남는다.

  소비자는 `tests/test_gate66_defensive.py::assert_premise_actually_ran` — exact full node id 마다
  `when=call` 기록이 **정확히 하나** 있고 그 결말이 passed(측정) / skipped(미측정) 인지를 본다.
  setup/teardown 만 있는 node 는 "돌지 않았다" 다.

사용: `python -m pytest ... -p tests.phase_witness --phase-witness=<파일>` (child 는 cwd=REPO 에서 뜬다 —
`tests/` 는 package 라 `tests.phase_witness` 로 import 된다).
"""
from __future__ import annotations

import json
import os


def pytest_addoption(parser):
    parser.addoption("--phase-witness", default=None, metavar="PATH",
                     help="runtest 단계 기록을 JSON Lines 로 append 할 파일 (G68-T1)")


def pytest_configure(config):
    path = config.getoption("--phase-witness")
    if path:
        # 이전 실행의 찌꺼기를 지운다 — 같은 경로를 두 번 쓰면 첫 실행의 call 이 남아 두 번째의 부재를 가린다.
        with open(path, "w", encoding="utf-8"):
            pass


def pytest_runtest_logreport(report):
    path = _path()
    if not path:
        return
    rec = {"nodeid": report.nodeid, "when": report.when, "outcome": report.outcome}
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        fh.flush()
        os.fsync(fh.fileno())


_PATH = None


def pytest_sessionstart(session):
    global _PATH
    _PATH = session.config.getoption("--phase-witness")


def _path():
    return _PATH
