"""활성/비활성 user-site **인터프리터 fixture** (65차 G65-T1).

64차의 활성 대조군은 환경변수 하나(`PYTHONNOUSERSITE`)를 지우고 "이제 활성이다" 라고
가정했다. `pyvenv.cfg` 로 user site 가 꺼진 일반 venv 에서는 그 가정이 틀리고, 시험은
자기 전제를 만들지 못한 채 `assert child != "<absent>"` 에서 죽었다 (리뷰어 실측:
활성 인터프리터 9 passed · 일반 venv 1 failed).

여기서는 전제를 **만들고 잰다**: `python -m venv --without-pip` 로 인터프리터 둘을
만든다 — `--system-site-packages` 를 준 것은 `site.ENABLE_USER_SITE` 가 참(활성),
안 준 것은 거짓(비활성)이다 (CPython `site.venv()` 의 규칙). 만든 뒤 그 인터프리터를
실제로 띄워 값을 읽고, 기대와 다르면 fixture 가 전제를 못 만든 것이므로 **그 사실을
skip 이유에 그대로 적는다** — 조용히 다른 환경을 쓰지 않는다.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest


def measured_user_site(python: Path | str, cwd: Path | None = None) -> bool:
    """그 인터프리터가 **실제로** 보고하는 `site.ENABLE_USER_SITE`."""
    r = subprocess.run(
        [str(python), "-c", "import json, site; print(json.dumps(bool(site.ENABLE_USER_SITE)))"],
        cwd=cwd, capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, r.stderr[-500:]
    return bool(json.loads(r.stdout.strip().splitlines()[-1]))


def build_interpreter(tmp_path: Path, *, user_site: bool) -> Path:
    """user site 가 `user_site` 가 **되도록** venv 를 만든다 — 검증은 하지 않는다 (그것은
    `make_interpreter` 와 전제 시험의 일이다). venv 를 만들 수 없으면 `pytest.skip`."""
    name = "venv-user-site-on" if user_site else "venv-user-site-off"
    venv = tmp_path / name
    args = [sys.executable, "-m", "venv", "--without-pip"]
    if user_site:
        args.append("--system-site-packages")      # CPython site.venv(): 이것이 활성 조건이다
    r = subprocess.run([*args, str(venv)], capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        pytest.skip(f"venv 를 만들 수 없어 {name} 전제를 구성하지 못했다: {r.stderr[-300:]}")
    return venv / ("Scripts" if os.name == "nt" else "bin") / \
        ("python.exe" if os.name == "nt" else "python")


def make_interpreter(tmp_path: Path, *, user_site: bool) -> Path:
    """user site 가 `user_site` 인 인터프리터를 만들고 **실측으로 확인한** 뒤 그 실행 파일
    경로를 돌려준다.

    전제를 못 만들면 `pytest.skip` — 이유에 기대값·실측값을 담는다. 전제를 못 만든
    시험은 "그 환경에서는 원래 실패" 가 아니라 **미측정**이다.
    """
    python = build_interpreter(tmp_path, user_site=user_site)
    got = measured_user_site(python)
    if got != user_site:
        name = "venv-user-site-on" if user_site else "venv-user-site-off"
        pytest.skip(f"{name} 의 site.ENABLE_USER_SITE 실측이 {got} 다 (기대 {user_site}) — "
                    "이 기계에서는 이 전제를 구성할 수 없다 (G65-T1: 미측정으로 보고)")
    return python


def use_interpreter(monkeypatch, python: Path) -> None:
    """탐침·부모 문맥이 **둘 다** 이 인터프리터를 쓰게 한다 — `mutation_replay` 는
    `sys.executable` 을 호출 시점에 읽는다."""
    monkeypatch.setattr(sys, "executable", str(python))
    monkeypatch.delenv("PYTHONNOUSERSITE", raising=False)   # 조건은 venv 가 정한다
