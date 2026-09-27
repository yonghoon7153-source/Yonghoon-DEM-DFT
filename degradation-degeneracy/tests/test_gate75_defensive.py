"""75차 회신 (원장 §104) — 잔여 세 경계를 **RED 먼저** 닫는다.

  G75-N1 (P1)  index 최종화 Python 호출의 실패가 archive 의 최종 rc 에 전파되지 않았다 — 승격·n_ok 뒤라
               옛 index 와 새 묶음이 어긋난 채 rc 0 · "git add artifacts" 안내로 끝났다 (리뷰어 S17).
               → 실패는 즉시 nonzero · 명시적 미완, 성공 안내 차단, 이미 승격된 상태는 숨기지 않는다.
  G75-N2 (P2)  `yaml.safe_load` 가 중복 mapping 키를 뒤 값으로 접어 preflight 가 rc 0 으로 받고 writer 가
               접힌 내용을 써 무관 항목을 잃는다 (I02·I03·I04). → 진입·동명 비교·병합이 **같은** 엄격 loader
               (중복 키 = 불명확 index) 를 쓰고, 첫 승격 전에 거부 · index 바이트 불변.
  G75-N3 (P2)  진단 전용 소비자(`_no_active_claim_evidence_problems`)가 `out` 의 존재만 봤다 — receipt·묶음이
               결속한 실행 자리와 대조하지 않았다 (D01: `results/OTHER_RUN` 이 통과). → 생산자와 **같은 함수**
               (`_assert_receipt_bound_to_bundle` · `_assert_ledger_run_bound`)로 대조한다.

이 파일은 패치 전 전부 RED 여야 한다 (처음부터 통과하면 fixture 감사).
"""
from __future__ import annotations

import copy
import hashlib
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tests import test_docs_lint as DL                          # noqa: E402
from tests.test_gate74_defensive import _FAKE, _archive_harness, _index, _seed   # noqa: E402


# ─────────────────────────────────────────────────────────────────────────────
# G75-N1 — index 최종화 실패는 archive 실패다
# ─────────────────────────────────────────────────────────────────────────────
_INDEX_MARKER = "_tmp = out.with_name("          # 최종 index heredoc 에만 있는 줄


def _python_wrapper(tmp_path: Path, mode: str) -> Path:
    """`PYTHON` 으로 끼우는 인터프리터 wrapper — 최종 index heredoc 에만 결함을 주입한다.

    mode = "rc17"     index 스크립트를 실행하지 않고 rc 17 (리뷰어 S17 그대로)
    mode = "replace"  index 스크립트의 `os.replace` 만 OSError 로 (리뷰어 W01 을 전체 프로그램 안에서)
    그 밖의 heredoc(검증·동명 비교)은 진짜 python 이 그대로 돈다.
    """
    real = sys.executable
    w = tmp_path / "bin" / "python-wrapper"
    w.parent.mkdir(parents=True, exist_ok=True)
    body = f'''#!/bin/bash
# stdin 의 스크립트를 잠시 파일로 받아 마커를 보고, 다시 stdin 으로 넘긴다 ("$PY" - args <<'PYEOF' 형태 유지 —
# `python -` 는 sys.path[0] 이 '' 라 cwd 의 src/·tools/ 를 찾는다; 파일로 실행하면 그것이 깨진다)
if [[ "$1" == "-" ]]; then
  tmp=$(mktemp)
  cat > "$tmp"
  if grep -q -F {_INDEX_MARKER!r} "$tmp"; then
    if [[ "{mode}" == "rc17" ]]; then rm -f "$tmp"; exit 17; fi
    {{ printf 'import os as _os0\\n_os0.replace = lambda *a, **k: (_ for _ in ()).throw(OSError("injected replace failure"))\\n'; cat "$tmp"; }} > "$tmp.mod"
    "{real}" "$@" < "$tmp.mod"; rc=$?; rm -f "$tmp" "$tmp.mod"; exit $rc
  fi
  "{real}" "$@" < "$tmp"; rc=$?; rm -f "$tmp"; exit $rc
fi
exec "{real}" "$@"
'''
    w.write_text(body, encoding="utf-8")
    w.chmod(w.stat().st_mode | stat.S_IEXEC)
    return w


@pytest.mark.parametrize("mode", ["rc17", "replace"])
def test_g75_n1_an_index_finalisation_failure_makes_the_archive_fail_and_leaves_the_index_unchanged(tmp_path, mode):
    d, dest, run = _archive_harness(tmp_path)
    before = _seed(dest, _FAKE)
    r = run(extra={"PYTHON": str(_python_wrapper(tmp_path, mode))})
    assert r.returncode != 0, ("index 최종화가 실패했는데 archive 가 성공으로 끝났다 (G75-N1)\n" + r.stdout + r.stderr)
    assert (dest / "artifact_index.yaml").read_bytes() == before, "실패했는데 index 가 바뀌었다"
    assert "git add artifacts" not in r.stdout, "index 가 미완인데 commit 안내를 찍었다"
    assert (dest / "res").is_dir(), "묶음 승격은 이미 일어났다 — 그 사실을 지우거나 숨기지 않는다"
    out = r.stdout + r.stderr
    assert "index" in out and ("미완" in out or "실패" in out), out[-600:]


def test_g75_n1_control_a_healthy_run_still_succeeds_through_the_wrapper(tmp_path):
    """대조군 — wrapper 가 결함을 주입하지 않으면(rc17/replace 마커 없음) 정상 경로는 그대로 rc 0 이다."""
    d, dest, run = _archive_harness(tmp_path)
    _seed(dest, _FAKE)
    real = sys.executable
    w = tmp_path / "bin" / "python-passthrough"
    w.parent.mkdir(parents=True, exist_ok=True)
    w.write_text(f'#!/bin/bash\nexec "{real}" "$@"\n', encoding="utf-8")
    w.chmod(w.stat().st_mode | stat.S_IEXEC)
    r = run(extra={"PYTHON": str(w)})
    assert r.returncode == 0, r.stdout + r.stderr
    assert set(_index(dest)["runs"]) == set(_FAKE) | {"res"}


# ─────────────────────────────────────────────────────────────────────────────
# G75-N2 — 중복 YAML 키는 불명확한 index 다: 첫 승격 전 거부 · 바이트 불변
# ─────────────────────────────────────────────────────────────────────────────
_PRESERVED = "preserved: {artifact_kind: fit, payload_index_sha256: '" + "a" * 64 + "', source_commit: '" + "1" * 40 + "', run_dir: results/preserved, fits_sha256: '" + "f" * 64 + "', curves_sha256: '" + "c" * 64 + "'}"

_DUP_CASES = {
    "top-level runs twice (I02)":
        "_주의: seed\nsource_commit: null\nruns:\n  " + _PRESERVED + "\nruns: {}\n",
    "same run name twice (I03)":
        "_주의: seed\nsource_commit: null\nruns:\n  " + _PRESERVED + "\n  " + _PRESERVED.replace("a" * 64, "b" * 64) + "\n",
    "identity key twice in one entry (I04)":
        "_주의: seed\nsource_commit: null\nruns:\n  preserved:\n    artifact_kind: fit\n    payload_index_sha256: '" + "a" * 64 + "'\n    payload_index_sha256: '" + "b" * 64 + "'\n    source_commit: '" + "1" * 40 + "'\n    run_dir: results/preserved\n    fits_sha256: '" + "f" * 64 + "'\n    curves_sha256: '" + "c" * 64 + "'\n",
}


@pytest.mark.parametrize("label", list(_DUP_CASES))
def test_g75_n2_a_duplicate_mapping_key_in_the_index_stops_before_any_promotion(tmp_path, label):
    d, dest, run = _archive_harness(tmp_path)
    p = dest / "artifact_index.yaml"
    p.write_text(_DUP_CASES[label], encoding="utf-8")
    assert yaml.safe_load(_DUP_CASES[label]) is not None          # 느슨한 loader 는 접어서 받는다 — 그것이 결함
    before = p.read_bytes()
    r = run()
    assert r.returncode != 0, f"중복 키({label})를 가진 index 로 승격했다\n" + r.stdout + r.stderr
    assert p.read_bytes() == before
    assert not (dest / "res").exists(), "index 가 불명확한데 묶음을 승격했다"
    assert "중복" in (r.stdout + r.stderr)


def test_g75_n2_the_strict_loader_is_one_function_shared_by_every_index_reader():
    """진입·동명 비교·병합이 **같은** 해석 규칙을 써야 한다 — 세 곳이 따로 읽으면 그 사이가 구멍이다."""
    src = (REPO / "scripts" / "archive_results.sh").read_text(encoding="utf-8")
    assert src.count("load_index_strict(") >= 3, "index 를 읽는 세 자리가 같은 엄격 loader 를 쓰지 않는다"
    assert "yaml.safe_load(open(idx" not in src and "yaml.safe_load(out.read_text" not in src \
        and "yaml.safe_load(open(p" not in src, "느슨한 safe_load 로 index 를 읽는 자리가 남아 있다"
    from tools.index_yaml import load_index_strict, DuplicateKeyError

    with pytest.raises(DuplicateKeyError):
        load_index_strict(_DUP_CASES["top-level runs twice (I02)"])
    ok = load_index_strict("_주의: x\nsource_commit: null\nruns:\n  " + _PRESERVED + "\n")
    assert list(ok["runs"]) == ["preserved"]


# ─────────────────────────────────────────────────────────────────────────────
# G75-N3 — 진단 전용 소비자의 out 결속 = 생산자와 같은 규칙
# ─────────────────────────────────────────────────────────────────────────────
def _live():
    return DL._live_contract()


def _leg(reg, lid):
    return next(e for e in reg["legs"] if e["leg_id"] == lid)


def test_g75_n3_00_the_live_diagnostic_leg_is_bound_to_its_receipt_and_bundle_run():
    reg, *_ = _live()
    assert DL._no_active_claim_evidence_problems(reg) == []


@pytest.mark.parametrize("bad_out", ["results/OTHER_RUN", "results/grid_fit_v4", "artifacts/grid_fit_v5",
                                     "results/grid_fit_v5x", "results/grid_fit_v5/sub"])
def test_g75_n3_01_a_different_nonempty_out_is_refused_by_the_consumer(bad_out):
    """리뷰어 D01 — receipt·묶음·hash 는 그대로 두고 원장의 `out` 한 값만 바꾼다."""
    reg, *_ = _live()
    _leg(reg, "grid_fit_v5")["evidence"]["out"] = bad_out
    bad = DL._no_active_claim_evidence_problems(reg)
    assert any("grid_fit_v5" in b and "out" in b for b in bad), bad


def test_g75_n3_01b_what_the_producer_accepts_the_consumer_accepts_too():
    """같은 함수이므로 producer 의 정규화(끝 `/`)는 소비자도 받는다 — 소비자가 더 엄격하거나 느슨하면 그것이 다음 반례다."""
    reg, *_ = _live()
    _leg(reg, "grid_fit_v5")["evidence"]["out"] = "results/grid_fit_v5/"
    assert DL._no_active_claim_evidence_problems(reg) == []


@pytest.mark.parametrize("value", [None, "", "   ", 17, ["results/grid_fit_v5"]])
def test_g75_n3_02_an_absent_or_untyped_out_is_refused_with_its_own_reason(value):
    reg, *_ = _live()
    ev = _leg(reg, "grid_fit_v5")["evidence"]
    if value is None:
        del ev["out"]
    else:
        ev["out"] = value
    bad = DL._no_active_claim_evidence_problems(reg)
    assert any("grid_fit_v5" in b and "out" in b for b in bad), bad


def test_g75_n3_03_the_consumer_reuses_the_producer_binding_functions():
    """재구현이 아니라 재사용 — `_assert_receipt_bound_to_bundle` 과 `_assert_ledger_run_bound` 를 부른다."""
    import inspect

    src = inspect.getsource(DL._no_active_claim_evidence_problems)
    assert "_assert_receipt_bound_to_bundle" in src and "_assert_ledger_run_bound" in src, src
