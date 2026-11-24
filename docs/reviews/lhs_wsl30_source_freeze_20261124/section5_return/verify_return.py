"""Recheck the named author return and its frozen metadata without reading any simulation files."""
import argparse
from collections import Counter
import datetime as dt
import hashlib
import json
import math
from pathlib import Path
import re
import zipfile

HERE = Path(__file__).resolve().parent
ROSTER = HERE.parent / "roster.json"
ROSTER_SHA = "407d03aa2a2cd1ea2ff6c5e95de336af77de61d00cf19d35302c5c6bf3e01e81"
ZIP_SHA = "a48a5a9eca797a1a214df9782a0c1ee7010f22a63f36f829d9f89a1fa6f98e1a"
JSON_SHA = "8563b834e148219b7ae5746ad8149fb9beacd209c875659e4df4a4f8c0a35e24"
PIN = "a1828b86514f05483da5873ff74093aab3452546"


def check(ok, why):
    if not ok:
        raise ValueError(why)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def disposition(row, frozen):
    case = frozen["case"]
    check(row["case"] == case and row["run_segment"] == frozen["run_segment"] and
          row["harvest_step"] == frozen["harvest_step"], f"{case} identity")
    b = row["b7"]
    if b is None:
        check(row["pressure_check"] == "HOLD" and row["reason"], f"{case} source refusal")
        return "HOLD", None
    check(b["case"] == case and b["schema"] == "lhs_pressure_record/v1" and
          b["deck"] == frozen["deck"] and b["deck_sha256"] == frozen["deck_sha256"], f"{case} deck")
    check(re.fullmatch("[0-9a-f]{64}", row["canonical_sha256"]) and
          re.fullmatch("[0-9a-f]{64}", row["normalized_pressure_sequence_sha256"]) and
          row["normalized_pressure_sequence_sha256"].startswith(frozen["b7_lines_sha256_prefix12"]), f"{case} sequence")
    if b["status"] == "REFUSED":
        check(row["pressure_check"] == "HOLD" and b["why"], f"{case} B7 refusal")
        return "REFUSED", None
    check(b["log_sha256"] == row["canonical_sha256"] and b["log_file"] == frozen["canonical_log"] and
          b["n_press_lines"] == str(frozen["b7_line_count"]) and frozen["b7_line_count"] > 0 and
          str(b["lines_after_last"]).isdigit(), f"{case} log")
    target, last, max_mpa, target_deck, last_deck = [float(b[k]) for k in
        ("target_mpa", "last_press_mpa", "max_press_mpa", "target_press_deck", "last_press_deck")]
    check(all(map(math.isfinite, (target,last,max_mpa,target_deck,last_deck))) and
          last_deck*1000 == last and target_deck*1000 == target and max_mpa >= last, f"{case} units")
    # The log's literal Target is not exported. B7 allowed this much difference
    # from the deck; use the entire allowed interval as an independent sign check.
    tol = 1e-9 * max(abs(target_deck), 1.)
    if last_deck >= target_deck+tol:
        reached = True
    elif last_deck < target_deck-tol:
        reached = False
    else:
        raise ValueError(f"{case} reach sign cannot be checked from the exported fields")
    status = "OK" if reached else "NOT_REACHED"
    check(b["status"] == status and b["reached"] == str(reached), f"{case} stop")
    qualified = reached and abs(target-300.) <= 1e-6 and last >= target-1e-6
    check(row["pressure_check"] == ("OK" if qualified else "HOLD"), f"{case} qualification")
    if qualified:
        check(row["reason"] is None and b["why"] == "", f"{case} unexpected reason")
    return ("OK" if qualified else ("NOT_REACHED" if not reached else "HOLD")), last


def recheck(path):
    frozen_raw = ROSTER.read_bytes()
    check(digest(frozen_raw) == ROSTER_SHA, "roster checksum")
    roster = json.loads(frozen_raw)["roster"]
    check(digest(path.read_bytes()) == ZIP_SHA, "outer checksum")
    with zipfile.ZipFile(path) as archive:
        check(sorted(archive.namelist()) == ["SHA256SUMS","readback.json"] and archive.testzip() is None,
              "archive contents or CRC")
        data = archive.read("readback.json")
        check(digest(data) == JSON_SHA and archive.read("SHA256SUMS") == (JSON_SHA+"  readback.json\n").encode(),
              "internal checksum")
    report = json.loads(data)
    check(report["scope"] == "WSL30_ONLY_SECTION5_PRESSURE" and report["operator"] == "first_author" and
          report["approval_mode"] == "GO_LHS_WSL30_SECTION5_PRESSURE_ONCE" and report["release"] == PIN and
          report["roster_sha256"] == ROSTER_SHA and report["tau_read"] is False and
          report["release_authorized"] is False, "return scope")
    first, last = [dt.datetime.fromisoformat(report[k]) for k in ("read_started_utc","read_ended_utc")]
    check(first.utcoffset() == last.utcoffset() == dt.timedelta(0) and first <= last, "UTC interval")
    ids = [f"lhs00_{i}" for i in range(100,130)]
    check([r["case"] for r in roster] == [r["case"] for r in report["rows"]] == ids and report["planned"] == 30,
          "missing, duplicate, or reordered cases")
    outcomes = []
    for row, frozen in zip(report["rows"], roster, strict=True):
        status, mpa = disposition(row,frozen)
        outcomes.append((row["case"],status,mpa,row.get("reason") or (row["b7"] or {}).get("why") or ""))
    counts=Counter(s for _,s,_,_ in outcomes)
    check(report["ok"] == counts["OK"], "header count")
    return outcomes, {s:counts[s] for s in ("OK","NOT_REACHED","REFUSED","HOLD")}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("archive",type=Path)
    p.add_argument("--table",type=Path,help="local author-facing per-case table")
    args=p.parse_args()
    rows, counts=recheck(args.archive)
    print(json.dumps(counts), f"rows={len(rows)}")
    if args.table:
        lines=["# WSL30 §5 압력 자격 · 11-24 반환 재판독","",
               "각 행의 압력은 정본 가압 루프의 마지막 출력이다. 목표는 300 MPa이며 표시는 소수 여섯 자리로 반올림했다. 판정은 반환의 원 정밀도로 대조했다.","",
               "| 케이스 | 처분 | 마지막 압력 (MPa) | 보류 사유 |","|---|---|---:|---|"]
        for case,status,mpa,reason in rows:
            shown="—" if mpa is None else f"{mpa:.6f}"
            lines.append(f"| {case} | {status} | {shown} | {reason or '—'} |")
        doc=("\n".join(lines)+"\n").encode()
        if args.table.exists():
            check(args.table.read_bytes() == doc,"existing table differs")
        else:
            with args.table.open("xb") as stream:
                stream.write(doc)


if __name__=="__main__":
    main()
