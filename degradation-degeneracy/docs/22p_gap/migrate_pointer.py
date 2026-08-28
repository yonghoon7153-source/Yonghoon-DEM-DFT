#!/usr/bin/env python3
"""이미 커밋된 cohort pointer 를 46차 계약으로 **한 번** 옮긴다.

46차 #9 에서 pointer 의 닫힌 key 집합이 바뀌었고(`cohort_id` echo 제거) 원장
봉인 authority 에 producer pin 의 불변 부분과 사용 정책이 들어왔다. 그래서
이미 커밋된 `CURRENT` 는 (a) key 집합이 다르고 (b) 봉인 값이 다르다 — 둘 다
reader 가 fail-closed 로 거부한다.

`schema` 문자열은 **올리지 않는다.** 그것은 `generation_id()` 의 preimage 에
들어가므로 올리면 이미 굳은 generation 의 이름이 전부 바뀐다.

이 스크립트가 **하지 않는 것**을 먼저 적는다:

  · `generation_id` 를 바꾸지 않는다        (바이트 계보는 그대로다)
  · `files` 를 바꾸지 않는다                 (실물과 대조한 뒤에만 쓴다)
  · generation directory 를 만들지도 지우지도 않는다
  · 원장을 고치지 않는다

하는 일은 하나다: **같은 generation 을 가리키는 pointer 를 새 schema 로 다시
쓴다.** 새 봉인 값은 살아 있는 원장 record 에서 그 자리에서 계산한다.

이것이 pointer 소실(→ terminal fail-closed) 과 다른 이유: 계보가 끊기지
않는다. 옛 pointer 를 읽어 그것이 가리키는 generation 을 그대로 이어받는다.
읽을 옛 pointer 가 없으면 이 스크립트는 아무것도 하지 않는다.

사용::

    python3 docs/22p_gap/migrate_pointer.py docs/22p_gap/proj_g2
    python3 docs/22p_gap/migrate_pointer.py docs/22p_gap/proj_g2 --dry-run
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent



def _rp():
    spec = importlib.util.spec_from_file_location(
        "_rp_migrate", HERE / "row_projection.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def migrate(out: pathlib.Path, dry_run: bool = False) -> int:
    rp = _rp()
    moved = 0
    for name in ("CURRENT", ".PENDING"):
        p = out / name
        if not p.is_file():
            continue
        rec = json.loads(p.read_text(encoding="utf-8"))
        want = rp._PENDING_KEYS if name == ".PENDING" else rp._CURRENT_KEYS
        if rec.get("schema") != rp.CURRENT_SCHEMA:
            print(f"✗ {name}: 옮길 수 있는 schema 가 아니다: {rec.get('schema')!r}")
            return 1
        if set(rec) == want:
            print(f"{name}: 이미 46차 key 집합이다 — 건드리지 않는다")
            continue
        if set(rec) - want != {"cohort_id"}:
            print(f"✗ {name}: 46차 이전 pointer 로 보이지 않는다 — "
                  f"여분 {sorted(set(rec) - want)} · 모자람 {sorted(want - set(rec))}")
            return 1
        gid = rec["generation_id"]
        gdir = out / "gen" / gid
        # 실물과 대조한다 — pointer 만 고치고 실물을 안 보면 옛 거짓말을 새
        # schema 로 옮겨 적는 것이 된다.
        got = {n: rp._sha(b) for n, b in rp._generation_entries(gdir, out).items()}
        if got != rec["files"]:
            print(f"✗ {name}: generation {gid[:16]} 실물이 pointer 와 다르다 — "
                  "옮기지 않는다")
            return 1
        if rp.generation_id(rec["files"]) != gid:
            print(f"✗ {name}: generation_id 가 files 와 다르다 — 옮기지 않는다")
            return 1
        seal = rp._ledger_seal(rp._ledger_cohort(out))
        new = {"schema": rp.CURRENT_SCHEMA, "generation_id": gid,
               "files": rec["files"], "ledger_seal": seal}
        if name == ".PENDING":
            new["roster_digest"] = rec["roster_digest"]
            new["base_generation"] = rec["base_generation"]
        body = json.dumps(new, sort_keys=True, ensure_ascii=False,
                          separators=(",", ":")) + "\n"
        print(f"{name}: key 집합을 46차 계약으로 옮긴다 (schema {rec['schema']} "
              f"그대로) · generation {gid[:16]} 유지 · seal {seal[:16]}")
        if not dry_run:
            p.write_text(body, encoding="utf-8")
        moved += 1
    if not moved:
        print("옮길 pointer 가 없다")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("out", help="cohort 출력 디렉터리")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    return migrate(pathlib.Path(a.out), a.dry_run)


if __name__ == "__main__":
    sys.exit(main())
