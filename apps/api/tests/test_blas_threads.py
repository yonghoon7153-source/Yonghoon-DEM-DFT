"""서버의 BLAS 는 스레드 하나로 뜬다 (ADR 0048 보완 1).

이 값은 numpy 가 처음 import 되기 전에만 먹힌다 -- 테스트 프로세스는 이미 numpy 를
읽었으므로, 새 파이썬을 띄워 서버가 import 하는 순서 그대로 본다.
"""

import os
import subprocess
import sys
from pathlib import Path

API = Path(__file__).resolve().parents[1]
REPO = API.parents[1]


def _after_import(extra_env: dict[str, str]) -> str:
    env = {k: v for k, v in os.environ.items()
           if k not in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS")}
    env.update(extra_env)
    env["PYTHONPATH"] = os.pathsep.join([str(API), str(REPO / "packages/wrdkit/src")])
    code = ("import app, numpy, os; "
            "print(os.environ['OPENBLAS_NUM_THREADS'], os.environ['OMP_NUM_THREADS'])")
    return subprocess.run([sys.executable, "-c", code], env=env, cwd=API,
                          capture_output=True, text=True, check=True).stdout.strip()


def test_the_server_package_pins_blas_to_one_thread_before_numpy():
    assert _after_import({}) == "1 1"


def test_a_value_given_from_outside_wins():
    assert _after_import({"OPENBLAS_NUM_THREADS": "4"}) == "4 1"
