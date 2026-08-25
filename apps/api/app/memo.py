"""요청과 요청 사이에 남는 **메모리** 캐시.

`storage.py` 의 캐시는 디스크에 있고 *파싱* 을 아낀다.  이쪽은 프로세스 안에
있고 그 다음 두 가지를 아낀다.

* **압축 해제.**  `load_columns` 는 `.npz` 를 매번 새로 푼다.  프로파일 화면이
  사이클 20 개를 그리면 `_branch_profile` 이 40 번 불리고, 40 번 모두 같은
  아카이브를 다시 푼다 -- 200 사이클 · 49k 행 파일에서 재본 값이 요청당
  680 ms 이고 그중 370 ms 가 zlib 이었다.
* **knee 계산.**  `detect_knee` 는 기준 4종을 다 돌리고, DBW 가 들어오면서
  값이 두 배가 됐다 (400 사이클에서 130 ms).  대시보드는 이것을 셀마다 한 번씩
  부르므로 12 셀이면 4.5 초다.

둘 다 **입력이 같으면 답이 같은** 계산이라, 키에 입력을 그대로 넣으면 무효화할
일이 없다.  파일이 바뀌면 sha256 이 바뀌고, 사이클이 하나 늘면 용량 튜플이
바뀐다 -- 낡은 값을 꺼낼 키가 애초에 만들어지지 않는다.  "언제 지울까" 를
정하지 않아도 되는 대신, "무엇이 같음을 증명하는가" 를 키에 다 적어야 한다.
"""

from __future__ import annotations

import copy
from collections import OrderedDict
from collections.abc import Callable

import numpy as np

from wrdkit.knee import KneeAnalysis, detect_knee

from .settings import settings

# --------------------------------------------------------------------------
# 컬럼 (.npz 압축 해제)
# --------------------------------------------------------------------------
#: 한 항목이 예산 전체의 이만큼을 넘으면 아예 담지 않는다.  20 MB 짜리 `.wrd`
#: 하나가 예산을 다 먹고 자기도 곧 밀려나면, 캐시는 비용만 내고 아무도 못
#: 맞히는 상태가 된다.
_MAX_SHARE = 0.5


class ColumnCache:
    """가장 오래 안 쓴 것부터 버리는, **바이트로 상한을 둔** 캐시.

    항목 수로 상한을 두지 않는 이유는 `.wrd` 가 100 배까지 차이나기 때문이다.
    "4 개까지" 는 작은 파일에서는 너무 인색하고 큰 파일에서는 1 GB 다.
    """

    def __init__(self, budget_bytes: int) -> None:
        self.budget_bytes = budget_bytes
        self._entries: OrderedDict[tuple, dict[str, np.ndarray]] = OrderedDict()
        self._bytes = 0
        self.hits = 0
        self.misses = 0

    def get(self, key: tuple) -> dict[str, np.ndarray] | None:
        columns = self._entries.get(key)
        if columns is None:
            self.misses += 1
            return None
        self._entries.move_to_end(key)
        self.hits += 1
        return columns

    def put(self, key: tuple, columns: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
        """담아 두고, **읽기 전용으로 만든** 같은 배열을 돌려준다.

        딕셔너리를 그대로 나눠 주므로 호출자가 배열에 쓰면 다음 요청까지
        오염된다.  numpy 는 `writeable=False` 로 그 사고를 조용한 오답 대신
        그 자리의 `ValueError` 로 바꿔 준다.  wrdkit 은 읽기만 하므로
        (`seconds()` 도 `charge_mah()` 도 새 배열을 만든다) 이걸로 아무것도
        막히지 않고, 막힌다면 그 코드가 잘못된 것이다.
        """
        size = sum(int(array.nbytes) for array in columns.values())
        for array in columns.values():
            # 소유 여부를 보지 않는다.  numpy 는 쓰기를 **막는** 것은 뷰에도
            # 허용하고 (되돌리는 쪽만 소유를 요구한다), 파서가 큰 배열의 뷰를
            # 넘겨줄 수도 있는데 그때 뷰만 통과시키면 정작 오염될 수 있는
            # 것들이 다 빠진다.
            array.flags.writeable = False
        if size > self.budget_bytes * _MAX_SHARE:
            return columns
        self._entries.pop(key, None)
        self._entries[key] = columns
        self._bytes += size
        while self._bytes > self.budget_bytes and len(self._entries) > 1:
            _, evicted = self._entries.popitem(last=False)
            self._bytes -= sum(int(a.nbytes) for a in evicted.values())
        return columns

    def forget(self, run_id: int) -> None:
        """한 run 의 항목을 모두 버린다 (삭제·재파싱 뒤)."""
        for key in [k for k in self._entries if k[0] == run_id]:
            evicted = self._entries.pop(key)
            self._bytes -= sum(int(a.nbytes) for a in evicted.values())

    def clear(self) -> None:
        self._entries.clear()
        self._bytes = 0
        self.hits = self.misses = 0

    @property
    def used_bytes(self) -> int:
        return self._bytes


columns_cache = ColumnCache(settings.columns_cache_bytes)


def columns(run_id: int, sha256: str,
            load: Callable[[], dict[str, np.ndarray]]) -> dict[str, np.ndarray]:
    """이 run 의 컬럼.  없으면 `load()` 로 만들어 담는다.

    키에 sha256 이 들어가는 이유는 SQLite 가 행 id 를 재사용하기 때문이다.
    run 1 이 지워지고 다른 파일이 run 1 이 되면, id 만으로는 남의 셀의 컬럼을
    돌려주게 된다 -- `storage.load_columns` 가 디스크에서 막는 것과 같은 사고를
    메모리에서도 막는다.
    """
    key = (run_id, sha256)
    hit = columns_cache.get(key)
    if hit is not None:
        return hit
    return columns_cache.put(key, load())


# --------------------------------------------------------------------------
# knee
# --------------------------------------------------------------------------
#: knee 분석은 답이 작다 (기준 4종 · 각각 dict 하나).  값이 아니라 **키** 가
#: 크므로 -- 400 사이클이면 float 800 개 -- 항목 수를 넉넉히 두지 않는다.
KNEE_CACHE_SIZE = 128

_knee_entries: OrderedDict[tuple, KneeAnalysis] = OrderedDict()
_knee_stats = {"hits": 0, "misses": 0}


def knee_analysis(cycles, capacities, **options) -> KneeAnalysis:
    """`detect_knee` 와 같은 답을, 같은 입력이면 다시 계산하지 않고.

    키는 인자 전부다.  `detect_knee` 는 모듈 상수를 읽지 않고 인자만으로
    결정되므로 (DBW 격자·경계도 상수지만 코드가 바뀌면 프로세스가 다시 뜬다)
    이 키가 곧 답이다.

    돌려줄 때 깊은 복사를 하는 것은 `KneeAnalysis` 가 얼지 않은 데이터클래스라
    호출자가 한 글자만 고쳐도 그 뒤 모든 요청이 그 값을 받기 때문이다.
    복사는 수십 마이크로초, 계산은 100 밀리초가 넘는다.
    """
    key = (tuple(float(c) for c in cycles),
           tuple(float(q) for q in capacities),
           tuple(sorted(options.items())))
    hit = _knee_entries.get(key)
    if hit is not None:
        _knee_entries.move_to_end(key)
        _knee_stats["hits"] += 1
        return copy.deepcopy(hit)
    _knee_stats["misses"] += 1
    analysis = detect_knee(cycles, capacities, **options)
    _knee_entries[key] = analysis
    while len(_knee_entries) > KNEE_CACHE_SIZE:
        _knee_entries.popitem(last=False)
    return copy.deepcopy(analysis)


def knee_stats() -> dict[str, int]:
    return dict(_knee_stats, entries=len(_knee_entries))


def clear() -> None:
    """모두 버린다.  테스트가 서로의 캐시를 물려받지 않도록."""
    columns_cache.clear()
    _knee_entries.clear()
    _knee_stats["hits"] = _knee_stats["misses"] = 0
