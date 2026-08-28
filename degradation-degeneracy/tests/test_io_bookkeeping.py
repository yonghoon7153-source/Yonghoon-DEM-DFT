"""집계·병합 회귀 테스트 (solve 없음).

V100 실행에서 드러난 버그의 회귀 방지:
같은 --out에 --resume 없이 재실행하면
  - failed.csv 행이 중복 누적되고 (completed는 set으로 중복 제거)
  - curves.parquet에 같은 조건 행이 두 번 들어간다
→ 요약 수치가 어긋나고 downstream fitting이 같은 조건을 중복 계산한다.
"""

from __future__ import annotations

from pathlib import PurePosixPath, PureWindowsPath

import pandas as pd

from src.io import (append_failed, load_completed, load_failed, mark_completed,
                    merge_chunks, save_chunk)


def _frame(cond_id: str, v: float, n: int = 3) -> pd.DataFrame:
    return pd.DataFrame({"cond_id": [cond_id] * n,
                         "x_norm": [0.0, 0.5, 1.0][:n],
                         "v_full": [v] * n})


def test_load_failed_dedupes_by_cond_id(tmp_path):
    append_failed(tmp_path, "aaa", {"lli": 0.1}, "infeasible: PE")
    append_failed(tmp_path, "bbb", {"lli": 0.2}, "infeasible: PE")
    append_failed(tmp_path, "aaa", {"lli": 0.1}, "infeasible: PE")   # 재실행 중복
    assert len(pd.read_csv(tmp_path / "failed.csv")) == 3   # 행은 3
    assert load_failed(tmp_path) == {"aaa", "bbb"}          # 고유는 2


def test_load_failed_handles_commas_and_korean(tmp_path):
    append_failed(tmp_path, "ccc", {"lli": 0.1, "lam_pe": 0.2},
                  "infeasible: PE 초기농도 63522 > c_max 63104 (수용 불가 — PE-limited)")
    assert load_failed(tmp_path) == {"ccc"}


def test_bookkeeping_matches_after_rerun(tmp_path):
    """재실행 시 n_done - n_failed 가 실제 곡선 수와 일치해야 한다."""
    for _ in range(2):                       # 같은 디렉터리에 두 번 실행
        for cid in ("ok1", "ok2"):
            mark_completed(tmp_path, cid)
        append_failed(tmp_path, "bad1", {}, "infeasible")
        mark_completed(tmp_path, "bad1")

    n_done = len(load_completed(tmp_path))
    n_failed = len(load_failed(tmp_path))
    assert (n_done, n_failed) == (3, 1)
    assert n_done - n_failed == 2            # 버그 있던 버전은 1 (3 - 2)


def test_merge_chunks_keeps_newest_block(tmp_path):
    """같은 조건이 여러 청크에 있으면 최신 청크만 남는다."""
    save_chunk(_frame("c1", 1.0), tmp_path, 0)
    save_chunk(_frame("c2", 2.0), tmp_path, 1)
    save_chunk(_frame("c1", 9.0), tmp_path, 2)   # 재실행분 (최신)

    merge_chunks(tmp_path)
    df = pd.read_parquet(tmp_path / "curves.parquet")

    assert df.cond_id.nunique() == 2
    assert len(df) == 6                                   # 2조건 × 3점 (중복 제거)
    assert set(df.loc[df.cond_id == "c1", "v_full"]) == {9.0}   # 최신값 유지
    assert "_chunk" not in df.columns


def test_merge_chunks_empty(tmp_path):
    assert merge_chunks(tmp_path) is None


def test_chunk_filename_has_pid(tmp_path):
    """프로세스가 다르면 청크 파일명이 겹치지 않아야 한다 (동시 실행 시 덮어쓰기 방지)."""
    import os

    p = save_chunk(_frame("c1", 1.0), tmp_path, 0)
    assert p.name == f"chunk_00000_{os.getpid()}.parquet"


def test_merge_orders_by_mtime_not_name(tmp_path):
    """이름순이 아니라 생성순(mtime)으로 최신을 고른다.

    두 프로세스가 각자 chunk_idx를 세면 이름 정렬로는 시간 순서를 알 수 없다.
    """
    import os
    import time

    d = tmp_path / "chunks"
    d.mkdir(parents=True)
    old = d / "chunk_00009_111.parquet"      # 이름은 뒤, 시간은 앞
    new = d / "chunk_00000_222.parquet"      # 이름은 앞, 시간은 뒤
    _frame("c1", 1.0).to_parquet(old, index=False)
    time.sleep(0.01)
    _frame("c1", 9.0).to_parquet(new, index=False)
    os.utime(old, (1_000_000, 1_000_000))    # old를 확실히 과거로

    merge_chunks(tmp_path)
    df = pd.read_parquet(tmp_path / "curves.parquet")
    assert set(df.v_full) == {9.0}           # 나중에 만들어진 값이 이김


def test_run_lock_blocks_concurrent_run(tmp_path, monkeypatch):
    """살아있는 grid 실행이 있으면 두 번째 실행은 거부된다."""
    import pytest

    import src.io as io_mod

    (tmp_path / ".run.lock").write_text("4242 2026-01-01T00:00:00\n")
    monkeypatch.setattr(io_mod, "_pid_alive", lambda pid: pid == 4242)
    with pytest.raises(RuntimeError, match="이미 실행 중"):
        io_mod.acquire_run_lock(tmp_path)


def test_lock_ignores_unrelated_process(tmp_path, monkeypatch):
    """PID는 살아있지만 grid가 아닌 프로세스(재사용된 PID)면 잠금을 회수한다."""
    import src.io as io_mod

    (tmp_path / ".run.lock").write_text("4242 2026-01-01T00:00:00\n")
    monkeypatch.setattr(io_mod, "_pid_alive", lambda pid: False)
    io_mod.acquire_run_lock(tmp_path)        # 예외 없이 통과
    io_mod.release_run_lock(tmp_path)


def test_stale_lock_is_reclaimed(tmp_path):
    """죽은 프로세스가 남긴 lock은 자동 정리된다."""
    from src.io import acquire_run_lock

    (tmp_path / ".run.lock").write_text("999999 2026-01-01T00:00:00\n")
    acquire_run_lock(tmp_path)               # 예외 없이 통과해야 함
    assert (tmp_path / ".run.lock").exists()


# ─────────────────────────────────────────────────────────────────────────────
# ★ 14차 발견 2 — source_digest 의 OS 의존성
#
# 리뷰어 실측: **같은 Git blob** 인데 digest 가 세 가지로 갈렸다.
#   POSIX (V100)                      4fa3e2af0a2e8106
#   경로 구분자만 `\` 인 경우          7ac22c1055eae262
#   CRLF 가 남은 실제 Windows worktree 808f19ea5556d018
# `source_digest` 는 `str(f.relative_to(root))` 를 해시하므로 경로 구분자가
# 그대로 들어가고, 정렬도 OS 문자열 순서다. code identity 가 OS 마다 달라지면
# "같은 코드로 만든 행" 이라는 판정 자체가 성립하지 않는다.
# ─────────────────────────────────────────────────────────────────────────────


def test_digest_path_key_is_posix_on_every_os():
    """digest 경로 키는 OS 무관 POSIX 정규형이어야 한다."""
    from src.io import _digest_path_key

    assert _digest_path_key(PureWindowsPath("src/io.py")) == b"src/io.py"
    assert _digest_path_key(PurePosixPath("src/io.py")) == b"src/io.py"
    assert (_digest_path_key(PureWindowsPath("configs/sub/base.yaml"))
            == b"configs/sub/base.yaml")


def test_digest_order_is_posix_order_not_os_path_order():
    """정렬 키도 같아야 한다 — `sorted(rglob())` 는 `Path` 비교다.

    `Path` 비교는 구분자에는 안 흔들리지만(부분 tuple 비교) **Windows 에서는
    각 부분을 소문자로 접어서** 비교한다. 그래서 대소문자가 섞인 파일 집합은
    OS 별로 순서가 뒤집힌다 (실측: Windows `apple.py, Zebra.py` /
    POSIX `Zebra.py, apple.py`). 순서가 바뀌면 내용이 같아도 digest 가 갈린다.
    """
    from src.io import _digest_path_key

    win = [PureWindowsPath("src/Zebra.py"), PureWindowsPath("src/apple.py")]
    assert sorted(win) == [PureWindowsPath("src/apple.py"),
                           PureWindowsPath("src/Zebra.py")]   # 소문자 접기
    assert sorted(_digest_path_key(p) for p in win) == [b"src/Zebra.py",
                                                        b"src/apple.py"]


def test_digest_files_sorts_by_posix_key(tmp_path):
    """수집 순서는 POSIX 바이트 키 기준으로 고정한다 (`Path` 비교가 아니라)."""
    from src.io import _digest_files

    (tmp_path / "src").mkdir(parents=True)
    (tmp_path / "src" / "Zebra.py").write_text("z\n")
    (tmp_path / "src" / "apple.py").write_text("a\n")

    keys = [k for k, _ in _digest_files(tmp_path, scope=("src/",))]
    assert keys == [b"src/Zebra.py", b"src/apple.py"]


def test_digest_scope_matches_run_scope():
    """digest 범위 == `RUN_SCOPE` (git dirty 판정 범위와 같아야 한다).

    실제 기본값은 `dirs=("src","tools","configs")` 뿐이었다 — `scripts/`·
    `run.sh`·`requirements*.txt` 를 고쳐도 code identity 가 안 바뀐다.
    smoke·실행 스크립트·의존성 핀이 바뀐 채 같은 서명이 찍히면, 그 서명은
    "이 결과를 만든 코드" 를 가리키지 못한다.
    """
    from src.io import RUN_SCOPE, _digest_files

    keys = {k.decode() for k, _ in _digest_files()}
    for entry in RUN_SCOPE:
        if entry.endswith("/"):
            assert any(k.startswith(entry) for k in keys), entry
        else:
            assert entry in keys, entry


def test_digest_sources_have_no_crlf():
    """digest 대상 파일에 CRLF 가 남아 있으면 안 된다.

    `.gitattributes` 의 `eol=lf` 는 정책일 뿐이고, worktree 바이트를 세지 않으면
    지켜졌는지 모른다 (리뷰어의 세 번째 digest 가 바로 이 경우다).
    """
    from src.io import _digest_files

    bad = [k.decode() for k, f in _digest_files() if b"\r\n" in f.read_bytes()]
    assert bad == []
