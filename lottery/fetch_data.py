#!/usr/bin/env python3
"""동행복권 공식 사이트에서 로또 6/45 · 연금복권 720+ 전 회차 결과를 받는다.

    python lottery/fetch_data.py            # 받기 → 검증 → data/raw/ 갱신 → CSV 재생성
    python lottery/fetch_data.py --offline  # 네트워크 없이 기존 raw 로 CSV 만 재생성

요청은 게임당 1번, 합계 2번이다. 범위/목록 API 가 한 번에 전 회차를 돌려준다.
회차별 상세 API 를 연달아 부르면 서버가 연결을 끊는다(2026-11-23 실측: 두 번째
연속 요청에서 connection reset) — 회차별 반복 호출은 하지 않는다.

받은 응답 bytes 는 그대로 data/raw/ 에 저장하고 MANIFEST.json 에 URL · 받은 시각(UTC) ·
sha256 · 크기 · 레코드 수를 적는다. 새 응답이 dataset.py 검증을 통과하지 못하면 기존
파일을 하나도 건드리지 않고 실패한다. 이미 가진 목록보다 회차가 줄었거나 옛 회차 값이 바뀐
응답도 같다 (dataset.history_changes) — 공식 정정이 맞다고 사람이 확인했을 때만
`--allow-history-change` 로 받는다. 주간 작업(weekly_update.py)은 이 플래그를 쓰지 않는다.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import sys
import urllib.request
from pathlib import Path

import dataset

BASE = "https://www.dhlottery.co.kr"
SOURCES = {  # raw 파일 이름 → (URL, Referer)
    "lotto645.json": (f"{BASE}/lt645/selectPstLt645Info.do?srchStrLtEpsd=1&srchEndLtEpsd=9999",
                      f"{BASE}/lt645/result"),
    "pension720.json": (f"{BASE}/pt720/selectPstPt720WnList.do", f"{BASE}/pt720/result"),
}
PARSERS = {"lotto645.json": dataset.parse_lotto, "pension720.json": dataset.parse_pension}
LABELS = {"lotto645.json": "로또", "pension720.json": "연금"}
HEADERS = {"User-Agent": "lottery-stats/1.0", "Accept": "application/json",
           "X-Requested-With": "XMLHttpRequest"}
DATA_DIR = dataset.ROOT / "data"


def _get(url: str, referer: str) -> bytes:
    req = urllib.request.Request(url, headers={**HEADERS, "Referer": referer})
    with urllib.request.urlopen(req, timeout=120) as r:
        ctype = r.headers.get("Content-Type", "")
        if r.status != 200 or "json" not in ctype:
            raise dataset.DataError(f"{url}: HTTP {r.status}, Content-Type {ctype!r}")
        return r.read()


def _atomic_write(path: Path, data: bytes) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(data)
    os.replace(tmp, path)


def write_csvs(lotto: list[dataset.LottoDraw], pension: list[dataset.PensionDraw],
               out_dir: Path = DATA_DIR) -> None:
    """엑셀에서 바로 열 수 있는 정리본. 정본은 raw JSON 이고 이건 파생물이다."""
    with open(out_dir / "lotto645.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["round", "date", "n1", "n2", "n3", "n4", "n5", "n6", "bonus",
                    "price_won", "sales_won", "games",
                    "winners_1", "winners_2", "winners_3", "winners_4", "winners_5",
                    "prize_1", "prize_2", "prize_3", "prize_4", "prize_5",
                    "first_auto", "first_manual", "first_semi"])
        for d in lotto:
            w.writerow([d.round, d.date.isoformat(), *d.numbers, d.bonus, d.price, d.sales,
                        round(d.games), *d.winners, *d.prize,
                        *("" if v is None else v for v in (d.first_auto, d.first_manual, d.first_semi))])
    with open(out_dir / "pension720.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["round", "date", "group", "number", "bonus",
                    *(f"d{i}" for i in range(1, 7)), *(f"b{i}" for i in range(1, 7))])
        for d in pension:
            w.writerow([d.round, d.date.isoformat(), d.group, d.number, d.bonus,
                        *d.number, *d.bonus])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--offline", action="store_true", help="네트워크 없이 기존 raw 로 CSV 만 재생성")
    ap.add_argument("--allow-history-change", action="store_true",
                    help="회차가 줄었거나 옛 회차 값이 바뀐 응답도 받는다 (공식 정정을 사람이 확인한 뒤에만)")
    args = ap.parse_args()
    raw_dir = dataset.RAW_DIR
    raw_dir.mkdir(parents=True, exist_ok=True)

    if not args.offline:
        fetched: dict[str, tuple[str, bytes, list]] = {}
        for name, (url, referer) in SOURCES.items():
            body = _get(url, referer)
            fetched[name] = (url, body, PARSERS[name](body))  # 검증 실패 시 여기서 중단
        if not args.allow_history_change:
            problems = [p for name, (_, _, recs) in fetched.items() if (raw_dir / name).exists()
                        for p in dataset.history_changes(PARSERS[name]((raw_dir / name).read_bytes()),
                                                         recs, LABELS[name])]
            if problems:
                raise dataset.DataError(
                    "받은 목록이 가진 기록을 그대로 이어 가지 않는다 — 아무 파일도 바꾸지 않았다. "
                    "공식 정정이 맞다고 확인했으면 --allow-history-change 로 다시 받는다.\n" + "\n".join(problems))
        now =dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
        manifest = {"source": "동행복권 dhlottery.co.kr (공식)", "fetched_at_utc": now, "files": {}}
        for name, (url, body, recs) in fetched.items():
            _atomic_write(raw_dir / name, body)
            manifest["files"][name] = {
                "url": url, "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body),
                "records": len(recs), "latest_round": recs[-1].round,
                "latest_date": recs[-1].date.isoformat()}
        _atomic_write(raw_dir / "MANIFEST.json",
                      (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode())

    lotto, pension = dataset.load_lotto(raw_dir), dataset.load_pension(raw_dir)
    write_csvs(lotto, pension)
    print(f"로또 6/45 {len(lotto)}회 ({lotto[0].date} ~ {lotto[-1].date}, 최신 {lotto[-1].round}회) | "
          f"연금복권720+ {len(pension)}회 ({pension[0].date} ~ {pension[-1].date})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
