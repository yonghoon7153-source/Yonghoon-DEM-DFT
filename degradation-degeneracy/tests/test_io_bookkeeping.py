"""집계·병합 회귀 테스트 (solve 없음).

V100 실행에서 드러난 버그의 회귀 방지:
같은 --out에 --resume 없이 재실행하면
  - failed.csv 행이 중복 누적되고 (completed는 set으로 중복 제거)
  - curves.parquet에 같은 조건 행이 두 번 들어간다
→ 요약 수치가 어긋나고 downstream fitting이 같은 조건을 중복 계산한다.
"""

from __future__ import annotations

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
