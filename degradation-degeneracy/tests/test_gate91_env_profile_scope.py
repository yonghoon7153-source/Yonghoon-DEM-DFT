"""91차 — G90-N1 정정: 환경 프로필 C 의 origin 축은 **경로 검색** 범위다 (원장 §138 · 고정 표
`docs/22p_gap/PYBAMM_PIN_ROUND_SPEC.md` §13).

90차 검토 (원장 §137 · G90-N1 P2): `tools/env_profile.py::_origin` 은 `importlib.machinery.PathFinder.find_spec(module, paths)` 가
그 경로에서 찾은 파일만 RECORD 와 대조한다 — `sys.modules` 에 이미 로드된 객체 · 그 `__file__` / `__spec__.origin` · 다른
meta-path finder 의 선택은 보지 않는다. 그래서 그 수를 "실제 origin 확인" 으로 부를 수 없다. 이 파일은 정정된 이름 · 범위
선언 · 문구를 고정한다 (측정 · 비교 · 상태 결정은 90차 그대로 — 그 시험은 `tests/test_gate90_env_profile.py`).

node (고정 표 §13-5): s01 세 상태의 `not_measured` · s02 검토자 반례의 고정 (로드된 numpy ≠ 경로 검색 origin) · s03 요약 ·
docstring 문구. 합성 site 는 90차 시험의 fixture · helper 를 그대로 쓴다. assert 메시지는 결정적이다 (tmp 경로 · 측정값을
싣지 않는다 — 변이 증인으로 쓴다).
"""
from __future__ import annotations

import importlib
import inspect
import sys
from pathlib import Path

import pytest

from tests.test_gate90_env_profile import _lock_for, _set_directive, synth   # noqa: F401 — synth 는 fixture

#: 고정 표 §13-3 — 이 도구가 재지 않는 것 (세 상태 모두 같은 값).
LOADED_ORIGIN = ["loaded_module_origin"]
#: 고정 표 §13-3 — C1 경계 문장 (모듈 docstring 에 그대로).
C1_BOUNDARY = "C 일치 여부는 실행 gate 가 아니나, 측정 기능을 요구하는 회귀의 지원 환경에서는 측정 불가를 시험 실패로 본다"


def _ep():
    return importlib.import_module("tools.env_profile")


# ── s01 · 세 상태 모두 `not_measured` ─────────────────────────────────────────

def _match(ep, s, tmp_path):
    lock, _ = _lock_for(ep, s.paths, tmp_path / "c.lock.txt")
    return lock


def _mismatch(ep, s, tmp_path):
    _, text = _lock_for(ep, s.paths, tmp_path / "base.lock.txt")
    lock = tmp_path / "off.lock.txt"
    lock.write_bytes(_set_directive(text, "python", "0.0.0").encode("utf-8"))
    return lock


def _unmeasured(ep, s, tmp_path):
    return tmp_path / "absent.lock.txt"


STATES = {"MATCH": _match, "MISMATCH": _mismatch, "UNMEASURED": _unmeasured}


@pytest.mark.parametrize("state", sorted(STATES))
def test_s01_every_result_declares_loaded_origin_unmeasured(synth, tmp_path, state):
    ep = _ep()
    lock = STATES[state](ep, synth, tmp_path)
    r = ep.compare_lock(lock, paths=synth.paths)
    assert r["status"] == state, f"status {r['status']}"
    # 측정 칸이 아니라 도구 범위의 선언이다 — UNMEASURED 에서도 None 이 아니고, 빈 목록 ("모든 것을 쟀다") 도 아니다.
    assert r.get("not_measured") == LOADED_ORIGIN, f"not_measured {r.get('not_measured')!r}"


# ── s02 · 검토자 반례의 고정 — 로드된 module ≠ 경로 검색 origin ─────────────────

def test_s02_path_search_count_is_not_a_loaded_module_check(synth, tmp_path):
    """이미 로드된 객체가 다른 곳에서 왔어도 경로 검색은 RECORD 안의 파일을 찾아 수에 넣는다 (90차 검토의 정적 반례 그대로).

    이 프로세스의 `numpy` 는 실제 설치본이고 (합성 site 밖), 합성 경로의 경로 검색은 RECORD 가 있는 가짜 `numpy` 를 찾는다.
    도구는 그 가짜를 `path_origins_in_record` 에 센다 — 그러니 이 수는 "로드된 module 의 확인" 이 아니고, 결과는 그것을
    `not_measured` 로 스스로 밝힌다. 로드된 origin 을 재는 것은 별도 승인 범위다 (고정 표 §13-7).
    """
    import numpy

    ep = _ep()
    loaded = Path(numpy.__file__).resolve()
    assert synth.site.resolve() not in loaded.parents, "전제: 로드된 numpy 는 합성 site 밖이다"
    lock, _ = _lock_for(ep, synth.paths, tmp_path / "c.lock.txt")
    r = ep.compare_lock(lock, paths=synth.paths)
    assert r["status"] == "MATCH", f"status {r['status']}"
    assert r["counts"].get("path_origins_in_record") == 9, f"counts {sorted(r['counts'])}"
    assert r["unverifiable"].get("path_origins") == ["yaml"], f"unverifiable {sorted(r['unverifiable'])}"
    owners = ep.measure(paths=synth.paths)["path_origins"]["in_record"]
    assert owners.get("numpy") == "numpy", "경로 검색 origin 의 주인이 합성 numpy 가 아니다"
    assert r["not_measured"] == LOADED_ORIGIN, f"not_measured {r['not_measured']!r}"
    assert sys.modules["numpy"] is numpy, "대조가 numpy 를 다시 import 했다 (도구는 import 하지 않는다)"


# ── s03 · 문구 ──────────────────────────────────────────────────────────────

def test_s03_summary_and_docstrings_state_the_path_search_scope(synth, tmp_path):
    ep = _ep()
    lock, _ = _lock_for(ep, synth.paths, tmp_path / "c.lock.txt")
    text = ep._summary(ep.compare_lock(lock, paths=synth.paths))
    assert "origin 확인" not in text, "요약에 옛 문구 'origin 확인' 이 남아 있다"
    assert "경로 검색 origin 의 RECORD 소속 9 (로드된 module origin 미측정)" in text, "요약에 경로 검색 범위 문구가 없다"
    assert "확인 불가 — 경로 검색 origin: yaml" in text, "확인 불가 줄에 경로 검색 범위 문구가 없다"
    doc = " ".join(ep.__doc__.split())
    assert "실제 origin" not in doc, "모듈 docstring 에 '실제 origin' 이 남아 있다"
    assert "로드된 module origin 은 측정하지 않는다" in doc, "모듈 docstring 에 미측정 선언이 없다"
    assert C1_BOUNDARY in doc, "모듈 docstring 에 C1 경계 문장이 없다"
    odoc = " ".join(inspect.getdoc(ep._origin).split())
    assert "실제 origin" not in odoc and "PathFinder" in odoc, "_origin docstring 이 경로 검색 범위를 말하지 않는다"
