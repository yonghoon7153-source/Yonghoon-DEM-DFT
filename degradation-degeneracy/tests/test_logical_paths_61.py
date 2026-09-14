"""61차 β (P0-2·P1-1) — **판정한 실물에 쓰는 것과 그 자리를 기록하는 것은 다른 값이다.**

리뷰어 반례 (정상 production 순서다, 공격이 아니다):

    manifest_input_exists_after_success: false
    manifest_fits_parquet_exists_after_success: false
    manifest_fits_parquet: /proc/self/fd/3/fits.parquet
    real_output_exists: true
    returned_out_exists_after_success: false
    real_lock_left_after_release: true

`[해석]` 60차 P0-4 는 "gate 뒤의 모든 쓰기를 판정한 handle 아래로" 를 세우면서
`out_dir` 자체를 `/proc/self/fd/N` 으로 **갈아 치웠다.** 그러면 그 아래의 모든
코드가 — 쓰는 코드뿐 아니라 **적는** 코드까지 — 그 경로를 본다. 그래서

  · `manifest.input` 에 staging 사본 경로가,
  · `manifest.fits_parquet` 과 반환 `out` 에 `/proc/self/fd/N/…` 이 봉인된다.

성공하면 capability 가 retire 되며 fd 가 닫히고 staging 도 지워지므로,
**성공한 artifact 가 존재하지 않는 경로를 provenance 로 들고 있다.**
`make_results.py` 는 그 `manifest.input` 을 재현 명령의 producer 경로로 실제
소비한다 — 기록이 재현 불가가 된다.

그리고 같은 갈아치우기가 수명 결함을 하나 더 만든다 (P1-1): commit 이 fd 를
닫은 **뒤에** 그 경로로 phase receipt 를 쓰고 lock 을 지우려 한다.
`release_run_lock()` 은 `OSError` 를 삼키므로 `.fit.lock` 이 실물에 남는다.

`[고침]` 값을 둘로 나눈다.

  · **write_root** — `staged_root(cap)`. **실제 writer 만** 이것을 받는다.
  · **logical_out / logical_in** — 기록·요약·phase receipt 가 적는 값.

그리고 순서를 고친다: 마지막 쓰기와 **lock 삭제가 끝난 뒤에** capability 를
소비한다. 그러면 "닫힌 handle 로 쓰기" 라는 물음 자체가 없어진다.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_fitting import _tiny_curves                           # noqa: E402


_OBJ_CFG = {"objectives": {}, "dqdv": {"window": 7, "polyorder": 2,
                                       "peak_weight": 1.0},
            "scaling": {"method": "reference_rmse"}}
_BOUNDS = {"init": [1.0, 0.0, 1.0, 0.0], "lb": [0.5, -1.0, 0.5, -1.0],
           "ub": [2.0, 1.0, 2.0, 1.0]}


@pytest.fixture
def fitted(tmp_path):
    """production `run_fit()` 을 한 번 완주시킨다 — 조각이 아니라 순서다."""
    import yaml

    import src.fitting as F

    in_dir = _tiny_curves(tmp_path / "in")
    out = tmp_path / "out"
    summary = F.run_fit(in_dir, out, _OBJ_CFG, {"a": {"w_pocv": 1.0}},
                        _BOUNDS, "expanded", 1, nproc=1)
    manifest = yaml.safe_load((out / "manifest.yaml").read_text(
        encoding="utf-8"))
    return {"in_dir": in_dir, "out": out, "summary": summary,
            "manifest": manifest}


# ── P0-2 ──────────────────────────────────────────────────────────────────
def test_the_sealed_input_path_exists_after_a_successful_fit(fitted):
    """★ P0-2 — 봉인된 입력 경로가 성공 뒤에 **존재해야** 한다.

    `make_results.py` 가 이 값을 재현 명령의 producer 경로로 소비한다. 성공하면
    지워지는 staging 사본을 적으면 그 명령은 처음부터 돌 수 없다.
    """
    got = fitted["manifest"].get("input")
    assert got, "manifest 에 input 이 없다"
    assert "/proc/self/fd/" not in got, (
        f"manifest.input 이 프로세스 지역 handle 경로다: {got} (61차 P0-2)")
    assert Path(got).exists(), (
        f"봉인된 입력 경로가 성공 뒤에 존재하지 않는다: {got} — 성공한 "
        "artifact 가 재현 불가한 provenance 를 들고 있다 (61차 P0-2)")


def test_the_sealed_output_path_exists_after_a_successful_fit(fitted):
    """★ P0-2 — 봉인된 출력 경로도 마찬가지다."""
    got = fitted["manifest"].get("fits_parquet")
    assert got, "manifest 에 fits_parquet 이 없다"
    assert "/proc/self/fd/" not in got, (
        f"manifest.fits_parquet 이 handle 경로다: {got} (61차 P0-2)")
    assert Path(got).exists(), (
        f"봉인된 출력 경로가 성공 뒤에 존재하지 않는다: {got} (61차 P0-2)")
    assert Path(got) == fitted["out"] / "fits.parquet"


def test_the_returned_summary_points_at_a_path_that_survives(fitted):
    """★ P1-1 — 반환값도 호출자가 실제로 열 수 있는 자리를 가리켜야 한다."""
    got = fitted["summary"]["out"]
    assert "/proc/self/fd/" not in got, f"반환 out 이 handle 경로다: {got}"
    assert Path(got).exists(), (
        f"반환된 out 이 성공 뒤에 존재하지 않는다: {got} (61차 P1-1)")


def test_no_durable_record_mentions_a_process_local_handle(fitted):
    """★ P0-2 — 굳은 기록 **어디에도** `/proc/self/fd` 가 없어야 한다.

    한 자리만 고치면 다음 자리가 또 새므로 **파일 전체**를 본다.
    """
    bad = []
    for p in sorted(fitted["out"].rglob("*")):
        if not p.is_file() or p.suffix not in (".yaml", ".json", ".csv"):
            continue
        try:
            body = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if "/proc/self/fd/" in body:
            bad.append(str(p.relative_to(fitted["out"])))
    assert not bad, (
        f"굳은 기록이 프로세스 지역 handle 경로를 담았다: {bad} (61차 P0-2)")


# ── P1-1 ──────────────────────────────────────────────────────────────────
def test_the_run_lock_is_gone_after_a_successful_fit(fitted):
    """★ P1-1 — 성공하면 `.fit.lock` 이 남지 않아야 한다.

    commit 이 fd 를 닫은 **뒤에** lock 을 지우려 하면 `release_run_lock()` 이
    `OSError` 를 삼키고 lock 이 실물에 남는다. 남은 lock 은 다음 실행을
    "이미 실행 중" 으로 오인하게 만든다.
    """
    left = fitted["out"] / ".fit.lock"
    assert not left.exists(), (
        "성공한 실행이 .fit.lock 을 남겼다 — capability 를 마지막 사용자보다 "
        "먼저 닫아 정리가 조용히 실패했다 (61차 P1-1)")


def test_the_phase_receipt_records_the_logical_place(tmp_path, monkeypatch):
    """★ P1-1 — phase receipt 의 `out` 도 지속 가능한 자리를 가리킨다.

    receipt 는 **재계산 없이 finalize** 하기 위한 근거다. 그 근거가 닫힌 fd
    경로면 finalize 는 아무것도 못 찾는다. smoke namespace 에는 claim 이 없어
    `_record_phase()` 가 일찍 돌아오므로, **그 함수가 무엇을 받는지**를 본다
    (claim 을 가짜로 세우면 그 아래 승인 축이 전부 가짜가 된다 — 시험이
    재는 것이 바뀐다).
    """
    import src.fitting as F

    seen = {}
    real = F._record_phase

    def _spy(claim, phase, summary, out_dir):
        seen[phase] = str(out_dir)
        return real(claim, phase, summary, out_dir)

    monkeypatch.setattr(F, "_record_phase", _spy)
    in_dir = _tiny_curves(tmp_path / "in")
    out = tmp_path / "out"
    F.run_fit(in_dir, out, _OBJ_CFG, {"a": {"w_pocv": 1.0}}, _BOUNDS,
              "expanded", 1, nproc=1)

    assert "fit" in seen, "`_record_phase` 가 안 불렸다"
    got = seen["fit"]
    assert "/proc/self/fd/" not in got, (
        f"phase receipt 가 handle 경로를 받았다: {got} (61차 P1-1)")
    assert Path(got) == out, f"receipt 가 논리 자리를 안 받았다: {got}"
    assert Path(got).exists()


def test_a_failed_lock_release_is_not_swallowed(tmp_path):
    """★ P1-1 의 둘째 층 — **자기 lock 을 못 지우면 소리를 낸다.**

    순서를 고쳐도 crash·권한·닫힌 handle 로 정리가 실패할 수는 있다. 그때
    `release_run_lock()` 이 조용히 넘어가면 남은 lock 이 다음 실행을 "이미
    실행 중" 으로 오인하게 만들고, **아무도 그 사실을 모른다**. 그것이 이번
    반례가 조용했던 이유다.

    ★ 62차 P1-1 — lock 이 token(dirfd+inode) 이 되면서 삭제는 `os.unlink(name,
      dir_fd=…)` 다. 그 자리를 막아 같은 성질을 잰다.
    """
    import os

    import src.io as io_mod

    d = tmp_path / "run"
    d.mkdir()
    tok = io_mod.acquire_run_lock(d, ".x.lock")
    real_unlink = os.unlink

    def _unlink(name, *a, **k):
        if str(name) == ".x.lock":
            raise OSError(1, "시험이 만든 정리 실패")
        return real_unlink(name, *a, **k)

    monkeypatch_target = io_mod.os
    saved = monkeypatch_target.unlink
    monkeypatch_target.unlink = _unlink
    try:
        with pytest.raises(OSError, match="시험이 만든"):
            io_mod.release_run_lock(tok)
    finally:
        monkeypatch_target.unlink = saved
    assert (d / ".x.lock").exists()


def test_releasing_a_missing_or_foreign_lock_is_loud_but_never_deletes(tmp_path):
    """★ 62차 P1-1 이 61차의 "없는 lock·남의 lock 은 조용히" 를 **뒤집었다.**

    리뷰어: own release 에서 missing/replaced 는 배타가 이미 깨졌다는 뜻이므로
    fail-closed 여야 한다. 남는 성질은 하나 — **남의 lock 은 절대 지우지
    않는다.** (경로만 받는 옛 release 는 `TypeError` — `test_run_lock_62.py`)
    """
    import os

    from src.io import acquire_run_lock, release_run_lock

    d = tmp_path / "run"
    d.mkdir()
    tok = acquire_run_lock(d, ".other.lock")
    os.unlink(d / ".other.lock")
    (d / ".other.lock").write_text("999999 x\n", encoding="utf-8")   # 남의 것
    with pytest.raises(RuntimeError, match="남의|inode"):
        release_run_lock(tok)
    assert (d / ".other.lock").exists(), "남의 lock 을 지웠다"
