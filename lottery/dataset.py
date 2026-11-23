"""로또 6/45 · 연금복권 720+ 원본 응답(JSON bytes) → 검증된 레코드.

원본은 fetch_data.py 가 동행복권에서 받아 data/raw/ 에 그대로 저장한 bytes 다.
여기서는 (1) 필요한 필드만 뽑아 이름을 붙이고 (2) 검증한다. 하나라도 어긋나면
DataError 로 멈춘다 (fail-closed) — 분석은 검증을 통과한 레코드만 본다.

검증 규칙은 2026-11-23 원본 프로파일링에서 실제로 성립함을 확인한 사실이다:
  - 로또: 1..N 회차 연속, 전부 토요일·7일 간격, 번호 6개 1..45 서로 다름·오름차순,
    보너스 1..45 이고 본번호와 겹치지 않음, 1회 = 10 23 29 33 37 40 + 16 (2002-12-07)
  - 게임당 가격: 5등 당첨금이 10,000원이면 2,000원(1~87회), 5,000원이면 1,000원(88회~)
  - 총판매액은 wholEpsdSumNtslAmt. (rlvtEpsdSumNtslAmt 는 261회부터 정확히 절반 =
    당첨금 재원 50%.) 판매액/가격 = 게임 수 로 계산한 5등 기대 당첨자 수와 실측이
    가격 구간별로 2% 안에서 맞는다 — 판매액 필드와 확률 공식을 동시에 검증한다.
  - 1등 자동/수동/반자동 구분은 262회부터 기록 (그 전은 0,0,0 → None 으로 둔다)
  - 연금: 1..N 회차 연속, 전부 목요일·7일 간격, 조 1..5, 1등·보너스 6자리 숫자 문자열
새로 받은 목록은 이에 더해 이미 가진 목록을 그대로 이어 가야 한다 (history_changes — fetch_data.py 가 적용).
"""
from __future__ import annotations

import datetime as dt
import json
from dataclasses import dataclass, fields
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW_DIR = ROOT / "data" / "raw"
N_COMB = comb(45, 6)  # 8,145,060 — 로또 1등 조합 수

# 본번호 6개 중 정확히 k개를 맞힐 확률 (보너스 무시) — 등수 기대값 검증에 쓴다
P_MATCH = {k: comb(6, k) * comb(39, 6 - k) / N_COMB for k in range(7)}
P_TIER5 = P_MATCH[3]  # 5등 = 정확히 3개 일치

SPLIT_FROM_ROUND = 262  # 1등 자동/수동/반자동 구분이 기록되기 시작한 회차
LOTTO_ANCHOR = {"round": 1, "date": dt.date(2002, 12, 7),
                "numbers": (10, 23, 29, 33, 37, 40), "bonus": 16}
PENSION_FIRST_DATE = dt.date(2020, 5, 7)  # 연금복권720+ 1회 추첨일


class DataError(ValueError):
    """원본이 검증 규칙을 어겼다. 메시지에 어긋난 항목을 모두 적는다."""


@dataclass(frozen=True)
class LottoDraw:
    round: int
    date: dt.date
    numbers: tuple[int, ...]  # 오름차순 6개
    bonus: int
    price: int  # 게임당 원: 2000 (1~87회) / 1000 (88회~)
    sales: int  # 총판매액(원)
    winners: tuple[int, ...]  # 1~5등 당첨 게임 수
    prize: tuple[int, ...]  # 1~5등 게임당 당첨금(원)
    first_auto: int | None  # 1등 중 자동 (262회 이전 None)
    first_manual: int | None  # 1등 중 수동
    first_semi: int | None  # 1등 중 반자동

    @property
    def games(self) -> float:
        return self.sales / self.price


@dataclass(frozen=True)
class PensionDraw:
    round: int
    date: dt.date
    group: int  # 1등 조 1..5
    number: str  # 1등 6자리
    bonus: str  # 보너스 6자리 (조 무관)


def _ymd(s: str) -> dt.date:
    s = str(s)
    if len(s) != 8 or not s.isdigit():
        raise DataError(f"날짜 형식이 YYYYMMDD 가 아님: {s!r}")
    return dt.date(int(s[:4]), int(s[4:6]), int(s[6:]))


def _rows(raw: bytes, path: tuple[str, ...]) -> list[dict]:
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as e:
        raise DataError(f"JSON 이 아님: {e}") from e
    node = obj
    for key in path:
        if not isinstance(node, dict) or key not in node:
            raise DataError(f"응답 구조에 {'.'.join(path)} 가 없음")
        node = node[key]
    if not isinstance(node, list) or not node:
        raise DataError(f"{'.'.join(path)} 가 비어 있거나 리스트가 아님")
    return node


def _check_calendar(rounds: list[int], dates: list[dt.date], weekday: int, label: str,
                    errors: list[str]) -> None:
    if rounds != list(range(1, len(rounds) + 1)):
        missing = sorted(set(range(1, max(rounds) + 1)) - set(rounds))
        errors.append(f"{label}: 회차가 1..N 연속이 아님 (빠짐 {missing[:10]}, 중복 "
                      f"{len(rounds) - len(set(rounds))})")
    bad_wd = [r for r, d in zip(rounds, dates) if d.weekday() != weekday]
    if bad_wd:
        errors.append(f"{label}: 추첨 요일이 다른 회차 {bad_wd[:10]}")
    bad_gap = [rounds[i] for i in range(1, len(dates)) if (dates[i] - dates[i - 1]).days != 7]
    if bad_gap:
        errors.append(f"{label}: 직전 회차와 7일 간격이 아닌 회차 {bad_gap[:10]}")


def parse_lotto(raw: bytes) -> list[LottoDraw]:
    rows = sorted(_rows(raw, ("data", "list")), key=lambda r: int(r["ltEpsd"]))
    errors: list[str] = []
    out: list[LottoDraw] = []
    for r in rows:
        rnd = int(r["ltEpsd"])
        nums = tuple(int(r[f"tm{k}WnNo"]) for k in range(1, 7))
        bonus = int(r["bnsWnNo"])
        if len(set(nums)) != 6 or not all(1 <= n <= 45 for n in nums):
            errors.append(f"로또 {rnd}회: 본번호가 1..45 서로 다른 6개가 아님 {nums}")
        if list(nums) != sorted(nums):
            errors.append(f"로또 {rnd}회: 본번호가 오름차순이 아님 {nums}")
        if not 1 <= bonus <= 45 or bonus in nums:
            errors.append(f"로또 {rnd}회: 보너스 {bonus} 가 범위 밖이거나 본번호와 겹침")
        tier5 = int(r["rnk5WnAmt"])
        price = {10000: 2000, 5000: 1000}.get(tier5)
        if price is None:
            errors.append(f"로또 {rnd}회: 5등 당첨금 {tier5} 로 게임 가격을 정할 수 없음")
            price = 1000
        winners = tuple(int(r[f"rnk{k}WnNope"]) for k in range(1, 6))
        split = (int(r["winType1"]), int(r["winType2"]), int(r["winType3"]))
        if rnd >= SPLIT_FROM_ROUND:
            if sum(split) != winners[0]:
                errors.append(f"로또 {rnd}회: 자동+수동+반자동 {split} 합이 1등 {winners[0]} 과 다름")
            auto, manual, semi = split
        else:
            if any(split):
                errors.append(f"로또 {rnd}회: {SPLIT_FROM_ROUND}회 이전인데 1등 구분 값이 있음 {split}")
            auto = manual = semi = None
        out.append(LottoDraw(
            round=rnd, date=_ymd(r["ltRflYmd"]), numbers=nums, bonus=bonus, price=price,
            sales=int(r["wholEpsdSumNtslAmt"]), winners=winners,
            prize=tuple(int(r[f"rnk{k}WnAmt"]) for k in range(1, 6)),
            first_auto=auto, first_manual=manual, first_semi=semi))

    _check_calendar([d.round for d in out], [d.date for d in out], 5, "로또", errors)
    if out and (out[0].round, out[0].date, out[0].numbers, out[0].bonus) != tuple(
            LOTTO_ANCHOR[k] for k in ("round", "date", "numbers", "bonus")):
        errors.append(f"로또 1회가 알려진 값과 다름: {out[0]}")
    prices = [d.price for d in out]
    switch = [d.round for d in out if d.price == 1000]
    if switch and prices != [2000] * (switch[0] - 1) + [1000] * (len(out) - switch[0] + 1):
        errors.append("로또: 게임 가격이 2000 → 1000 으로 한 번만 바뀌는 형태가 아님")
    # 판매액·확률 공식 동시 검증: 가격 구간별 5등 (실측 / 기대) 가 1 ± 2%
    for p in (2000, 1000):
        seg = [d for d in out if d.price == p]
        if seg:
            ratio = sum(d.winners[4] for d in seg) / sum(d.games * P_TIER5 for d in seg)
            if abs(ratio - 1) > 0.02:
                errors.append(f"로또: 가격 {p}원 구간 5등 실측/기대 = {ratio:.4f} (1±0.02 밖)")
    if errors:
        raise DataError("\n".join(errors))
    return out


def parse_pension(raw: bytes) -> list[PensionDraw]:
    rows = sorted(_rows(raw, ("data", "result")), key=lambda r: int(r["psltEpsd"]))
    errors: list[str] = []
    out: list[PensionDraw] = []
    for r in rows:
        rnd = int(r["psltEpsd"])
        grp = str(r["wnBndNo"])
        num, bns = str(r["wnRnkVl"]), str(r["bnsRnkVl"])
        if grp not in {"1", "2", "3", "4", "5"}:
            errors.append(f"연금 {rnd}회: 조 {grp!r} 가 1..5 가 아님")
        for label, v in (("1등", num), ("보너스", bns)):
            if len(v) != 6 or not v.isdigit():
                errors.append(f"연금 {rnd}회: {label} 번호 {v!r} 가 6자리 숫자가 아님")
        out.append(PensionDraw(round=rnd, date=_ymd(r["psltRflYmd"]),
                               group=int(grp) if grp.isdigit() else 0, number=num, bonus=bns))
    _check_calendar([d.round for d in out], [d.date for d in out], 3, "연금", errors)
    if out and out[0].date != PENSION_FIRST_DATE:
        errors.append(f"연금 1회 추첨일 {out[0].date} 가 {PENSION_FIRST_DATE} 이 아님")
    if errors:
        raise DataError("\n".join(errors))
    return out


def history_changes(old: list, new: list, label: str) -> list[str]:
    """새 목록이 옛 목록을 그대로 이어 가는지. 회차가 줄었거나 옛 회차 값이 바뀌었으면 그 내용을 돌려준다.

    끝이 잘린 목록(캐시·장애)이나 과거 값이 바뀐 목록은 위의 형식 검증을 통과하지만, 그대로 받으면
    분석과 배포가 그 값을 쓴다 (자체 리뷰 A1·A2). 두 목록 모두 1..N 연속으로 검증된 뒤라 i 번째 = i+1 회.
    """
    problems = []
    if new[-1].round < old[-1].round:
        problems.append(f"{label}: 최신 회차가 {old[-1].round}회 → {new[-1].round}회로 줄었다 (잘린 목록)")
    changed = [(o, n) for o, n in zip(old, new) if o != n]
    for o, n in changed[:10]:
        diff = ", ".join(f"{f.name} {getattr(o, f.name)} → {getattr(n, f.name)}"
                         for f in fields(o) if getattr(o, f.name) != getattr(n, f.name))
        problems.append(f"{label} {o.round}회가 바뀌었다: {diff}")
    if len(changed) > 10:
        problems.append(f"{label}: 그 밖에 {len(changed) - 10}개 회차가 더 바뀌었다")
    return problems


def load_lotto(raw_dir: Path = RAW_DIR) -> list[LottoDraw]:
    return parse_lotto((raw_dir / "lotto645.json").read_bytes())


def load_pension(raw_dir: Path = RAW_DIR) -> list[PensionDraw]:
    return parse_pension((raw_dir / "pension720.json").read_bytes())
