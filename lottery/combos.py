"""로또 6/45 조합 지표 — 전수 열거(8,145,060개)로 '정확한' 기대 분포를 만든다.

흔히 '패턴'이라 부르는 지표(총합·홀짝·고저·연번·AC값·구간·끝수)는 추첨기가 아니라
조합의 개수에서 나온다. 예: 총합 100~175 구간에 당첨이 몰리는 건 조합이 거기 몰려
있기 때문이다. 그래서 관측 분포를 '모든 조합의 분포'와 비교해야 의미가 있다.

모든 함수는 (k, 6) 오름차순 정수 배열을 받는다 — 전수 열거, 실제 당첨번호, 사용자가
고른 한 줄에 같은 코드를 쓴다. 사이트(JS)의 지표 계산은 이 정의를 그대로 옮긴 것이다.
"""
from __future__ import annotations

import itertools
from functools import lru_cache

import numpy as np

N_COMB = 8_145_060
_PAIRS = [(i, j) for i in range(6) for j in range(i + 1, 6)]

FEATURES = {  # 이름 → (한국어 라벨, 설명)
    "sum": ("총합", "6개 번호의 합 (21~255)"),
    "odd": ("홀수 개수", "6개 중 홀수 개수"),
    "low": ("저번호 개수", "1~22 에 속한 개수 (23~45 는 고번호)"),
    "consec": ("연번 쌍", "연속된 두 수(예: 17·18) 쌍의 개수"),
    "ac": ("AC값", "서로 다른 차이값 개수 − 5 (0~10, 클수록 흩어짐)"),
    "decades": ("구간 수", "1~9·10번대·20번대·30번대·40번대 중 몇 구간에 걸쳤나"),
    "birthday": ("31 이하 개수", "1~31 에 속한 개수 (생일·날짜로 고를 수 있는 번호)"),
    "last_digits": ("끝수 종류", "일의 자리 숫자가 몇 종류인가"),
}


@lru_cache(maxsize=1)
def all_combos() -> np.ndarray:
    """8,145,060 × 6 int8, 사전순. 약 1초."""
    flat = np.fromiter(itertools.chain.from_iterable(itertools.combinations(range(1, 46), 6)),
                       dtype=np.int8, count=N_COMB * 6)
    out = flat.reshape(-1, 6)
    out.setflags(write=False)
    return out


def features(c: np.ndarray) -> dict[str, np.ndarray]:
    c = np.asarray(c)
    if c.ndim != 2 or c.shape[1] != 6:
        raise ValueError(f"(k, 6) 배열이어야 함: {c.shape}")
    c16 = c.astype(np.int16)
    diffs = np.abs(c16[:, [j for _, j in _PAIRS]] - c16[:, [i for i, _ in _PAIRS]])
    diffs.sort(axis=1)
    ac = (np.diff(diffs, axis=1) != 0).sum(axis=1) + 1 - 5
    dec = np.minimum(c16 // 10, 4)  # 1~9→0, 10~19→1, ..., 40~45→4
    dec_n = np.zeros(len(c16), dtype=np.int16)
    for k in range(5):
        dec_n += (dec == k).any(axis=1)
    last = c16 % 10
    last_n = np.zeros(len(c16), dtype=np.int16)
    for k in range(10):
        last_n += (last == k).any(axis=1)
    return {
        "sum": c16.sum(axis=1),
        "odd": (c16 % 2 == 1).sum(axis=1),
        "low": (c16 <= 22).sum(axis=1),
        "consec": (np.diff(c16, axis=1) == 1).sum(axis=1),
        "ac": ac,
        "decades": dec_n,
        "birthday": (c16 <= 31).sum(axis=1),
        "last_digits": last_n,
    }


@lru_cache(maxsize=1)
def exact_distributions() -> dict[str, dict[int, float]]:
    """지표별 정확한 확률분포 {값: 확률} — 무작위 추첨이면 당첨번호가 따라야 할 분포."""
    out = {}
    for name, v in features(all_combos()).items():
        vals, cnt = np.unique(v, return_counts=True)
        out[name] = {int(a): float(b) / N_COMB for a, b in zip(vals, cnt)}
    return out


def rank_of(combo: tuple[int, ...]) -> int:
    """사전순 순위 (0 부터). 전수 배열 인덱스와 같다 — 테스트로 고정."""
    from math import comb
    c = sorted(combo)
    r, prev = 0, 0
    for pos, x in enumerate(c):
        for y in range(prev + 1, x):
            r += comb(45 - y, 5 - pos)
        prev = x
    return r
