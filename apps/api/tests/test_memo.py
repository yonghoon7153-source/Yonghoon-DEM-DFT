"""메모리 캐시가 아끼는 것과, 아끼면 안 되는 것.

캐시의 위험은 느려지는 것이 아니라 **틀린 답이 빨리 나오는** 것이다.  그래서
여기 있는 테스트 대부분은 "빨라졌는가" 가 아니라 "같은 답인가" 를 본다.
"""

import numpy as np
import pytest

from app import memo, services, storage
from app.memo import ColumnCache
from wrdkit.knee import detect_knee


@pytest.fixture(autouse=True)
def _empty():
    memo.clear()
    yield
    memo.clear()


def _fading(n=60, break_at=40):
    cycles = list(range(1, n + 1))
    capacities, q = [], 2.0
    for i in range(n):
        q *= 0.999 if i < break_at else 0.99
        capacities.append(q)
    return cycles, capacities


# --------------------------------------------------------------------------
# knee
# --------------------------------------------------------------------------
def test_the_memo_answers_exactly_what_detect_knee_answers():
    """캐시는 답을 바꾸지 않는다 -- 두 번째 답도 첫 번째 답도."""
    cycles, capacities = _fading()
    direct = detect_knee(cycles, capacities, reference_cycle=3)

    first = memo.knee_analysis(cycles, capacities, reference_cycle=3)
    second = memo.knee_analysis(cycles, capacities, reference_cycle=3)

    assert memo.knee_stats()["hits"] == 1
    for got in (first, second):
        assert got.primary.method == direct.primary.method
        assert got.primary.cycle == direct.primary.cycle
        assert got.primary.detected == direct.primary.detected
        assert got.primary.reason == direct.primary.reason
        assert [r.method for r in got.results] == [r.method for r in direct.results]


def test_a_caller_that_edits_the_answer_cannot_edit_the_next_callers():
    """`KneeAnalysis` 는 얼지 않은 데이터클래스다.  꺼낼 때마다 복사한다."""
    cycles, capacities = _fading()
    first = memo.knee_analysis(cycles, capacities, reference_cycle=3)
    first.primary.reason = "손댔다"
    first.results.clear()

    second = memo.knee_analysis(cycles, capacities, reference_cycle=3)
    assert second.primary.reason != "손댔다"
    assert second.results


def test_one_more_cycle_is_a_different_question():
    """사이클이 늘면 키가 바뀐다 -- 무효화할 것이 없다."""
    cycles, capacities = _fading()
    memo.knee_analysis(cycles, capacities, reference_cycle=3)
    memo.knee_analysis(cycles + [61], capacities + [1.0], reference_cycle=3)
    assert memo.knee_stats() == {"hits": 0, "misses": 2, "entries": 2}


def test_different_options_are_different_questions():
    cycles, capacities = _fading()
    memo.knee_analysis(cycles, capacities, reference_cycle=3)
    memo.knee_analysis(cycles, capacities, reference_cycle=3, threshold_pct=90.0)
    assert memo.knee_stats()["misses"] == 2


def test_the_knee_table_stops_growing():
    for i in range(memo.KNEE_CACHE_SIZE + 5):
        memo.knee_analysis([1.0, 2.0, 3.0], [2.0, 1.9 - i * 1e-4, 1.8], reference_cycle=1)
    assert memo.knee_stats()["entries"] == memo.KNEE_CACHE_SIZE


# --------------------------------------------------------------------------
# 컬럼
# --------------------------------------------------------------------------
def _columns(rows=1000):
    return {"TIME": np.arange(rows, dtype=np.float64),
            "VOLTAGE": np.linspace(2.5, 4.2, rows)}


def test_columns_come_back_without_calling_the_loader_again():
    calls = []

    def load():
        calls.append(1)
        return _columns()

    memo.columns(1, "a" * 64, load)
    memo.columns(1, "a" * 64, load)
    assert len(calls) == 1


def test_a_new_file_under_a_reused_run_id_is_not_the_old_file():
    """SQLite 는 행 id 를 재사용한다.  sha256 이 키에 들어가는 이유다."""
    first = memo.columns(7, "a" * 64, lambda: {"V": np.zeros(3)})
    second = memo.columns(7, "b" * 64, lambda: {"V": np.ones(3)})
    assert first["V"].tolist() == [0, 0, 0]
    assert second["V"].tolist() == [1, 1, 1]


def test_cached_arrays_refuse_to_be_written():
    """조용한 오염 대신 그 자리에서 터지게."""
    columns = memo.columns(1, "a" * 64, _columns)
    with pytest.raises(ValueError):
        columns["VOLTAGE"][0] = 99.0


def test_forget_releases_a_runs_arrays():
    memo.columns(1, "a" * 64, _columns)
    memo.columns(2, "b" * 64, _columns)
    used = memo.columns_cache.used_bytes
    memo.columns_cache.forget(1)
    assert memo.columns_cache.used_bytes < used
    assert memo.columns_cache.get((1, "a" * 64)) is None
    assert memo.columns_cache.get((2, "b" * 64)) is not None


def test_the_budget_is_bytes_not_entries():
    """`.wrd` 는 100 배까지 차이난다.  '4 개까지' 는 상한이 아니다."""
    one = _columns(1000)
    size = sum(a.nbytes for a in one.values())
    cache = ColumnCache(budget_bytes=size * 2)

    for i in range(6):
        cache.put((i, "x"), _columns(1000))

    assert cache.used_bytes <= size * 2
    assert cache.get((0, "x")) is None       # 가장 오래된 것부터
    assert cache.get((5, "x")) is not None   # 마지막 것은 남는다


def test_an_entry_bigger_than_the_budget_is_served_but_not_stored():
    """혼자 예산을 다 먹고 곧 밀려날 항목은 남들을 쫓아낼 자격이 없다."""
    cache = ColumnCache(budget_bytes=1024)
    columns = cache.put((1, "x"), _columns(1000))
    assert columns["TIME"][0] == 0          # 답은 그대로 돌려준다
    assert cache.get((1, "x")) is None      # 담기지는 않았다
    assert cache.used_bytes == 0


def test_a_zero_budget_turns_the_cache_off():
    cache = ColumnCache(budget_bytes=0)
    cache.put((1, "x"), _columns(10))
    assert cache.get((1, "x")) is None


# --------------------------------------------------------------------------
# 경계 — 지운 run 은 메모리에서도 사라진다
# --------------------------------------------------------------------------
def test_dropping_a_runs_cache_drops_the_memory_copy_too(client, sample_id,
                                                         wrd_bytes):
    run = client.post("/api/runs/upload", params={"sample_id": sample_id},
                      files={"file": ("c.wrd", wrd_bytes,
                                      "application/octet-stream")}).json()
    client.get(f"/api/samples/{sample_id}/profile", params={"cycles": "3"})
    assert memo.columns_cache.used_bytes > 0

    storage.drop_run_cache(run["id"])
    assert memo.columns_cache.used_bytes == 0


def test_a_profile_of_many_cycles_unpacks_the_archive_once(client, sample_id,
                                                           wrd_bytes,
                                                           monkeypatch):
    """사이클 하나에 브랜치 둘 -- 예전에는 그때마다 `.npz` 를 다시 풀었다."""
    client.post("/api/runs/upload", params={"sample_id": sample_id},
                files={"file": ("c.wrd", wrd_bytes, "application/octet-stream")})
    memo.clear()

    reads = []
    original = storage.load_columns

    def counted(run_id, expect_sha256=None):
        reads.append(run_id)
        return original(run_id, expect_sha256=expect_sha256)

    monkeypatch.setattr(services.storage, "load_columns", counted)
    response = client.get(f"/api/samples/{sample_id}/profile",
                          params={"cycles": "1-6"})
    assert response.status_code == 200
    assert len(response.json()["series"]) > 2
    assert len(reads) == 1
