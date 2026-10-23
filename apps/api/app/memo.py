"""요청과 요청 사이에 남는 **메모리** 캐시.

`storage.py` 의 캐시는 디스크에 있고 *파싱* 을 아낀다.  이쪽은 프로세스 안에
있고 그 다음 두 가지를 아낀다.

* **압축 해제.**  `load_columns` 는 `.npz` 를 매번 새로 푼다.  프로파일 화면이
  사이클 20 개를 그리면 `_branch_profile` 이 40 번 불리고, 40 번 모두 같은
  아카이브를 다시 푼다 -- 200 사이클 · 49k 행 파일에서 재본 값이 요청당
  680 ms 이고 그중 370 ms 가 zlib 이었다.
* **knee 계산.**  `detect_knee` 는 기준 4종을 다 돌리고, DBW 가 들어오면서
  값이 두 배가 됐다 (400 사이클에서 130 ms).  대시보드는 이것을 셀마다 한 번씩
  부르므로 12 셀이면 4.5 초다.  knee 의 답은 **디스크에도** 남긴다 (`knee/`) —
  `bml` 이 pull 할 때마다 서버가 다시 뜨고, 그때마다 첫 화면이 모든 셀의 knee
  를 처음부터 다시 셌다 (ADR 0048).

둘 다 **입력이 같으면 답이 같은** 계산이라, 키에 입력을 그대로 넣으면 무효화할
일이 없다.  파일이 바뀌면 sha256 이 바뀌고, 사이클이 하나 늘면 용량 튜플이
바뀐다 -- 낡은 값을 꺼낼 키가 애초에 만들어지지 않는다.  "언제 지울까" 를
정하지 않아도 되는 대신, "무엇이 같음을 증명하는가" 를 키에 다 적어야 한다.
"""

from __future__ import annotations

import contextlib
import copy
import dataclasses
import hashlib
import json
import os
import threading
from collections import OrderedDict
from collections.abc import Callable
from pathlib import Path

import numpy as np

from wrdkit import knee as knee_module
from wrdkit.knee import KneeAnalysis, KneeResult, detect_knee

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
#: 메모리에 두는 답의 수.  키가 입력 그대로였을 때는 (400 사이클이면 float
#: 800 개) 128 개로 묶어야 했고, 그러면 셀이 128 개를 넘는 순간 대시보드가
#: 이름순으로 도는 LRU 를 **한 번도 못 맞혔다** -- 순서대로 훑으면 늘 가장 먼저
#: 들어온 것이 방금 밀려난 것이다.  키를 지문(sha256)으로 바꿔 넉넉히 둔다.
KNEE_CACHE_SIZE = 4096
#: 디스크에 남기는 답의 수 상한.  구동 중인 셀은 사이클이 늘 때마다 키가
#: 바뀌어 새 답이 생기므로, 지우지 않으면 끝없이 쌓인다.  넘으면 가장 오래 안
#: 쓴 것부터 지운다 -- 지워진 답은 한 번 다시 셀 뿐이다.
KNEE_DISK_LIMIT = 4000

_knee_entries: OrderedDict[str, KneeAnalysis] = OrderedDict()
_knee_stats = {"hits": 0, "disk": 0, "misses": 0}
_knee_lock = threading.Lock()
_knee_code: bytes | None = None


def _code_fingerprint() -> bytes:
    """`detect_knee` 의 코드와 numpy 판 — 이것이 바뀌면 디스크의 옛 답은 남의 답이다.

    메모리 캐시는 코드가 바뀌면 프로세스가 다시 떠서 저절로 비지만, 디스크는
    그렇지 않다.  "knee 를 고치면 이 상수도 올려라" 같은 규칙은 잊히므로 소스
    자체를 키에 넣는다.  `wrdkit.knee` 는 numpy 말고 아무것도 import 하지
    않는다 -- 그 파일 하나가 답을 정한다.
    """
    global _knee_code
    if _knee_code is None:
        digest = hashlib.sha256(Path(knee_module.__file__).read_bytes())
        digest.update(np.__version__.encode())
        _knee_code = digest.digest()
    return _knee_code


def _knee_key(cycles, capacities, options: dict) -> str:
    """입력 전부의 지문.  `detect_knee` 는 인자만으로 답이 정해지므로 이것이 곧 답이다.

    사이클과 용량은 float64 바이트로 넣는다 -- 예전 튜플 키와 같은 값을 보되,
    NaN 이 섞여도 같은 입력이면 같은 키가 된다 (튜플의 NaN 은 자기와도 달라서
    그런 입력은 한 번도 못 맞혔다).
    """
    digest = hashlib.sha256(_code_fingerprint())
    for values in (cycles, capacities):
        array = np.ascontiguousarray(values, dtype=np.float64)
        digest.update(len(array).to_bytes(8, "little"))
        digest.update(array.tobytes())
    digest.update(repr(tuple(sorted(options.items()))).encode())
    return digest.hexdigest()


def _plain(value):
    if isinstance(value, np.generic):
        return value.item()
    raise TypeError(f"{type(value).__name__} 는 JSON 으로 못 남깁니다")


def knee_to_json(analysis: KneeAnalysis) -> str:
    """디스크에 남기는 모양.  pickle 이 아니라 JSON 인 이유는 읽어 보고 지울 수
    있어서다 -- 캐시는 사람이 들여다볼 수 있어야 의심할 수 있다."""
    return json.dumps(dataclasses.asdict(analysis), default=_plain,
                      ensure_ascii=False, sort_keys=True)


def knee_from_json(text: str) -> KneeAnalysis:
    data = json.loads(text)
    results = [KneeResult(**item) for item in data["results"]]
    primary = KneeResult(**data["primary"])
    # `detect_knee` 의 기준은 대개 `results` 안의 그 객체 자체다.  같은 값이면
    # 같은 객체로 되돌려 모양까지 맞춘다.
    primary = next((item for item in results if item == primary), primary)
    return KneeAnalysis(**{**data, "primary": primary, "results": results})


def _disk_path(key: str) -> Path:
    return settings.knee_dir / f"{key}.json"


def _disk_get(key: str) -> KneeAnalysis | None:
    path = _disk_path(key)
    try:
        analysis = knee_from_json(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError, KeyError):
        # 없거나, 반쯤 쓰였거나, 모양이 바뀐 옛 파일 -- 다시 세면 된다.
        return None
    # 프로세스마다 처음 한 번만 여기 온다 (그 뒤는 메모리가 답한다).  그때
    # 시각을 새로 찍어 두어야 오래된 것부터 지울 때 늘 쓰는 셀이 안 지워진다.
    with contextlib.suppress(OSError):
        os.utime(path)
    return analysis


def _disk_put(key: str, analysis: KneeAnalysis) -> None:
    try:
        text = knee_to_json(analysis)
    except (TypeError, ValueError):
        return
    directory = settings.knee_dir
    try:
        directory.mkdir(parents=True, exist_ok=True)
        temporary = directory / f".{key}.{os.getpid()}.{threading.get_ident()}.tmp"
        temporary.write_text(text, encoding="utf-8")
        # 바꿔치기는 원자적이다 -- 읽는 쪽은 옛 파일이나 새 파일만 본다.
        os.replace(temporary, _disk_path(key))
        _disk_prune(directory)
    except OSError:
        # 캐시를 못 남겨도 답은 맞다.  디스크가 꽉 찼다고 화면이 죽으면 안 된다.
        return


def _disk_prune(directory: Path) -> None:
    files = list(directory.glob("*.json"))
    if len(files) <= KNEE_DISK_LIMIT:
        return
    def mtime(path: Path) -> float:
        try:
            return path.stat().st_mtime
        except OSError:
            return 0.0
    # 상한의 90 % 까지 줄인다 -- 하나 넘을 때마다 하나씩 지우면 매번 디렉터리를 훑는다.
    for path in sorted(files, key=mtime)[:len(files) - int(KNEE_DISK_LIMIT * 0.9)]:
        with contextlib.suppress(OSError):
            path.unlink()


def knee_analysis(cycles, capacities, **options) -> KneeAnalysis:
    """`detect_knee` 와 같은 답을, 같은 입력이면 다시 계산하지 않고.

    메모리 → 디스크 → 계산 순서로 찾는다.  디스크의 답은 서버가 다시 떠도
    남는다 -- `bml` 은 pull 할 때마다 서버를 다시 띄우고, 그때마다 대시보드가
    모든 셀의 knee 를 처음부터 다시 셌다 (실측 합성 40 셀 · 셀당 400 사이클).

    돌려줄 때 깊은 복사를 하는 것은 `KneeAnalysis` 가 얼지 않은 데이터클래스라
    호출자가 한 글자만 고쳐도 그 뒤 모든 요청이 그 값을 받기 때문이다.
    복사는 수십 마이크로초, 계산은 100 밀리초가 넘는다.
    """
    key = _knee_key(cycles, capacities, options)
    with _knee_lock:
        hit = _knee_entries.get(key)
        if hit is not None:
            _knee_entries.move_to_end(key)
            _knee_stats["hits"] += 1
            return copy.deepcopy(hit)
    analysis = _disk_get(key)
    if analysis is not None:
        counter = "disk"
    else:
        counter = "misses"
        # 계산은 자물쇠 밖에서 -- 셀 하나를 세는 동안 다른 셀의 답을 꺼내는
        # 요청까지 기다리게 하지 않는다.  같은 셀을 둘이 동시에 세면 같은 답이
        # 두 번 나올 뿐이다.
        analysis = detect_knee(cycles, capacities, **options)
        _disk_put(key, analysis)
    with _knee_lock:
        _knee_stats[counter] += 1
        _knee_entries[key] = analysis
        _knee_entries.move_to_end(key)
        while len(_knee_entries) > KNEE_CACHE_SIZE:
            _knee_entries.popitem(last=False)
    return copy.deepcopy(analysis)


def knee_stats() -> dict[str, int]:
    with _knee_lock:
        return dict(_knee_stats, entries=len(_knee_entries))


def clear() -> None:
    """모두 버린다 -- 디스크의 knee 답까지.  테스트가 서로의 캐시를 물려받지 않도록."""
    columns_cache.clear()
    with _knee_lock:
        _knee_entries.clear()
        for name in _knee_stats:
            _knee_stats[name] = 0
    for path in settings.knee_dir.glob("*.json"):
        with contextlib.suppress(OSError):
            path.unlink()
