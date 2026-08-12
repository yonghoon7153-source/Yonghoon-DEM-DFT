"""집계·병합 회귀 테스트 (solve 없음).

V100 실행에서 드러난 버그의 회귀 방지:
같은 --out에 --resume 없이 재실행하면
  - failed.csv 행이 중복 누적되고 (completed는 set으로 중복 제거)
  - curves.parquet에 같은 조건 행이 두 번 들어간다
→ 요약 수치가 어긋나고 downstream fitting이 같은 조건을 중복 계산한다.
"""

from __future__ import annotations

from pathlib import Path

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


# ---------------------------------------------------------------------------
# ★ 14차 발견 2 — source_digest 경로 정규화 + RUN_SCOPE 정합
# ---------------------------------------------------------------------------


def test_digest_path_key_is_posix_normalized():
    """★ 14차-2 — digest 경로 키는 OS 무관 POSIX 정규형이어야 한다.

    반례 (리뷰어 실측): 같은 Git blob 인데 경로 구분자 때문에 digest 가 갈린다 —
    POSIX `4fa3e2af0a2e8106` vs Windows `\\` 구분자 `7ac22c1055eae262`.
    `str(PureWindowsPath("src/io.py"))` 는 `"src\\io.py"` 라 Linux 에서도 RED 다.
    """
    from pathlib import PureWindowsPath

    from src.io import _digest_path_key

    assert _digest_path_key(PureWindowsPath("src/io.py")) == b"src/io.py"
    assert _digest_path_key("src/io.py") == b"src/io.py"


def test_source_digest_covers_full_run_scope(tmp_path):
    """★ 14차-2 — RUN_SCOPE 6개(src tools configs scripts run.sh requirements*.txt)
    전부가 digest 에 들어가야 한다.

    현재 기본값은 ("src","tools","configs") 3개뿐이라 `scripts/`·`run.sh`·
    `requirements*.txt` 를 바꿔도 digest 가 안 변한다 → 코드 identity 구멍.
    """
    from src.io import source_digest

    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "a.py").write_bytes(b"x = 1\n")
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "go.sh").write_bytes(b"echo hi\n")
    (tmp_path / "run.sh").write_bytes(b"#!/bin/sh\n")
    (tmp_path / "requirements.txt").write_bytes(b"numpy\n")

    d0 = source_digest(root=tmp_path)
    (tmp_path / "scripts" / "go.sh").write_bytes(b"echo bye\n")
    d1 = source_digest(root=tmp_path)
    assert d0 != d1, "scripts/ 변경이 digest 에 반영돼야 한다"

    (tmp_path / "run.sh").write_bytes(b"#!/bin/bash\n")
    d2 = source_digest(root=tmp_path)
    assert d1 != d2, "run.sh 변경이 digest 에 반영돼야 한다"

    (tmp_path / "requirements.txt").write_bytes(b"numpy\nscipy\n")
    d3 = source_digest(root=tmp_path)
    assert d2 != d3, "requirements*.txt 변경이 digest 에 반영돼야 한다"


def test_source_tree_has_no_crlf():
    """★ 14차-2 — RUN_SCOPE 텍스트 파일에 CRLF 가 0개여야 한다 (양성 검사).

    리뷰어 실측: 실제 Windows worktree 의 잔존 CRLF 만으로 digest 가
    `808f19ea5556d018` 으로 세 번째 갈래를 만들었다. `.gitattributes` 존재
    확인(test_compare.py)만으로는 이미 들어온 CRLF 를 못 잡는다.
    """
    root = Path(__file__).resolve().parent.parent
    bad = []
    targets = [root / d for d in ("src", "tools", "configs", "scripts")]
    files = [f for base in targets if base.exists()
             for f in sorted(base.rglob("*")) if f.is_file()]
    files += [f for f in [root / "run.sh"] if f.is_file()]
    files += sorted(root.glob("requirements*.txt"))
    for f in files:
        if "__pycache__" in f.parts or f.suffix in (".pyc", ".pyo"):
            continue
        if b"\r\n" in f.read_bytes():
            bad.append(str(f.relative_to(root)))
    assert bad == [], f"CRLF 파일 발견: {bad}"


def test_run_scope_matcher_shared_with_digest():
    """★ 14차 2차 발견 5 — digest 범위와 dirty 범위가 같은 matcher 를 써야 한다.

    digest 는 `requirements*.txt` 를 glob 으로 전부 읽는데 `RUN_SCOPE` 는
    `requirements.txt`·`requirements-gpu.txt` 두 이름만 exact match 한다.
    미래의 `requirements-dev.txt` 는 digest 에는 들어가고 dirty 판정에는 안
    들어가 "RUN_SCOPE 와 1:1" 설명이 깨진다. 현재 tracked 파일에는 영향 없다.
    """
    from src.io import in_run_scope

    for p in ("src/io.py", "tools/x.py", "configs/base.yaml", "scripts/go.sh",
              "run.sh", "requirements.txt", "requirements-gpu.txt",
              "requirements-dev.txt"):
        assert in_run_scope(p), p
    for p in ("docs/RESULTS.md", "wiki/x.md", "kit_a/run.py",
              "src_extra/x.py", "requirements.md", "my-requirements.txt"):
        assert not in_run_scope(p), p


def test_untracked_requirements_counts_as_critical(tmp_path):
    """★ 14차 2차 발견 5 — root 의 untracked/ignored requirements 파일도
    critical 이어야 한다. digest 가 읽는 파일이 dirty 판정 밖이면, 그 파일을
    새로 만든 채 실행해도 clean 으로 승인된다."""
    import subprocess

    from src.io import git_info

    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "a.py").write_text("x = 1\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(tmp_path), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "-c", "user.email=t@t",
                    "-c", "user.name=t", "commit", "-qm", "init"], check=True)
    assert git_info(tmp_path)["git_dirty"] is False

    (tmp_path / "requirements-dev.txt").write_text("pytest\n", encoding="utf-8")
    info = git_info(tmp_path)
    assert info["git_dirty"] is True, info
    assert any("requirements-dev.txt" in c for c in info["git_untracked_critical"])


def test_scope_exclusion_helper_is_shared():
    """★ 14차 3차 발견 3 — 제외 규칙도 digest 와 dirty 가 공유해야 한다.

    dirty 쪽 `_SKIP` 은 `.pyc` 를 **이름 중간**에 포함해도 제외했고, digest 는
    suffix 만 제외한다. 그래서 `configs/model.pyconfig` 같은 파일이 digest 파일
    집합에는 들어가고 dirty 판정에서는 빠질 수 있다 (현재 HEAD 에는 없다).
    """
    from src.io import is_scope_excluded

    # 캐시·바이트코드는 양쪽에서 제외
    for p in ("src/__pycache__/io.cpython-311.pyc", "src/io.pyc", "src/io.pyo",
              "tools/.ipynb_checkpoints/x.ipynb"):
        assert is_scope_excluded(p), p
    # 이름 중간에 `.pyc`/`.ipynb_checkpoints` 가 있는 실제 입력은 제외하지 않는다
    for p in ("configs/model.pyconfig", "src/pycache_helper.py",
              "tools/pyc_writer.py", "configs/ipynb_checkpoints_note.yaml"):
        assert not is_scope_excluded(p), p


def test_tracked_dirty_is_conservative_for_excluded_paths(tmp_path):
    """★ 14차 4차 발견 3 — tracked 변경은 제외 규칙을 **적용하지 않는다** (의도).

    digest 는 캐시·바이트코드를 제외하지만, tracked 파일이 바뀐 사실 자체는
    막는 쪽이 안전하다 (false-clean 이 아니라 false-dirty). 저장소 규칙상
    validator 는 느슨하게 만들지 않으므로 이 비대칭을 **고정**한다 —
    "digest 와 dirty 가 같은 제외 규칙"이라는 서술 대신 "untracked/ignored 와
    digest 가 제외 규칙을 공유한다"가 정확하다.
    """
    import subprocess

    from src.io import git_info, source_digest

    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    d = tmp_path / "src" / ".ipynb_checkpoints"
    d.mkdir(parents=True)
    (d / "note.py").write_text("x = 1\n", encoding="utf-8")
    (tmp_path / "src" / "a.py").write_text("y = 1\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(tmp_path), "add", "-A", "-f"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "-c", "user.email=t@t",
                    "-c", "user.name=t", "commit", "-qm", "init"], check=True)

    d0 = source_digest(root=tmp_path)
    assert git_info(tmp_path)["git_dirty"] is False

    (d / "note.py").write_text("x = 2\n", encoding="utf-8")
    assert source_digest(root=tmp_path) == d0, \
        "제외 경로는 digest 에 들어가면 안 된다"
    assert git_info(tmp_path)["git_dirty"] is True, \
        "tracked 변경은 제외 경로라도 dirty 로 센다 (보수적, 의도)"
