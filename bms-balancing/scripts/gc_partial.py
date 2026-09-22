#!/usr/bin/env python3
"""부분 산출의 **보관 정책** — `partial/<종류>/<attempt-id>/` 를 (종류, 산출)마다 최근 N 개만 남긴다.

    python3 scripts/gc_partial.py --root out --keep 5            # 기본 **dry-run** — 무엇을 지울지만 말한다
    python3 scripts/gc_partial.py --root out --keep 5 --apply    # 실제로 지운다

조건 8 축 ④ 의 마지막 조각이다. attempt-id 를 정본으로 골랐으므로 (`verify.publish_target` 의 설명)
시도가 쌓인다 — 쌓이는 것을 받아들인 대신 **줄이는 규칙**을 둔다.

세 가지를 지킨다:

  ① **기본이 dry-run 이다.** 지우는 도구의 기본값이 "지운다" 이면 사고를 되돌릴 수 없다.
  ② **canonical 을 절대 안 건드린다.** 이 도구는 `<root>/partial/` 아래만 본다 — 과학 산출은 그 밖이다.
  ③ **모르면 안 지운다.** index 에 없는 디렉터리를 만나면 rc 2 로 멈춘다. 지우고 나서 "몰랐다" 는
     되돌릴 수 없다 (fail-closed — 이 저장소의 "부재는 안전값이 아니다" 와 같은 결).

종료 코드: 0 정상(dry-run 포함) · 2 입력 문제 또는 **index 와 디스크가 어긋남**.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from bms_balancing.verify import PARTIAL_INDEX      # noqa: E402


def load_index(root: pathlib.Path) -> dict:
    p = root / PARTIAL_INDEX
    try:
        doc = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise SystemExit(f"! partial index 를 못 읽었다 ({p}): {e} — 모르는 상태에서 지우지 않는다")
    if not isinstance(doc, dict) or not isinstance(doc.get("attempts"), list):
        raise SystemExit(f"! partial index 의 모양이 아니다 ({p})")
    return doc


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", required=True, type=pathlib.Path, help="산출 디렉터리 (그 아래 `partial/` 을 본다)")
    ap.add_argument("--keep", type=int, default=5, help="(종류, 산출)마다 남길 최근 시도 수 (기본 5)")
    ap.add_argument("--apply", action="store_true", help="실제로 지운다 (기본은 dry-run)")
    a = ap.parse_args(argv)
    if a.keep < 1:
        print("! --keep 은 1 이상이다 — 0 은 전부 지우라는 뜻이고 그것은 이 도구의 일이 아니다", file=sys.stderr)
        return 2

    root = a.root / "partial"
    if not root.is_dir():
        print(f"부분 산출이 없다 ({root}) — 할 일 없음")
        return 0
    idx = load_index(root)

    # ③ index 와 디스크를 먼저 댄다 — 모르는 디렉터리가 있으면 **아무것도 지우지 않는다**
    known = {(e["kind"], e["attempt"]) for e in idx["attempts"]}
    on_disk = {(k.name, att.name) for k in root.iterdir() if k.is_dir()
               for att in k.iterdir() if att.is_dir()}
    unknown = sorted(on_disk - known)
    if unknown:
        print(f"! index 에 없는 시도 디렉터리 {len(unknown)} 개 — 지우지 않는다 (모르는 것을 지우고 나서 "
              f"'몰랐다' 는 되돌릴 수 없다):", file=sys.stderr)
        for k, att in unknown[:20]:
            print(f"    {k}/{att}", file=sys.stderr)
        return 2

    # (종류, 산출)마다 index 순서(=기록 순서)의 뒤쪽 keep 개를 남긴다
    groups: dict = {}
    for e in idx["attempts"]:
        groups.setdefault((e["kind"], e["artifact"]), []).append(e)
    doomed = [e for g in groups.values() for e in g[:-a.keep]]

    # ⚠ Codex R17 P1-01: 전 판은 보관을 **(종류, 산출)** 로 정하고 삭제는 **(종류, 시도) 디렉터리** 로 했다 —
    #   두 모델이었다. 한 시도 A 가 matrix_100 과 matrix_200 을 내고 다른 시도 B 가 matrix_100 을 다시 내면,
    #   `--keep 1` 은 100 의 A 만 버려야 하는데 `matrix/A/` 를 통째로 지워 **200 의 유일한 최신 결과**까지
    #   없앴다 (rc 0 으로). 이제 삭제 단위를 **index 항목 하나 = 파일 하나** 로 내리고, 시도 디렉터리는
    #   retained 항목이 **하나도** 참조하지 않을 때만 정리한다. index 도 같은 항목 단위로 줄인다 — 한 모델이다.
    doomed_ids = {id(e) for e in doomed}
    retained = [e for e in idx["attempts"] if id(e) not in doomed_ids]
    retained_attempts = {(e["kind"], e["attempt"]) for e in retained}

    if not doomed:
        print(f"남길 {a.keep} 개 안이다 — 지울 것 없음 (시도 {len(idx['attempts'])} · 묶음 {len(groups)})")
        return 0

    # ③ 의 연장: index 의 `path` 가 partial 밖을 가리키면 **아무것도 지우지 않는다** (모르는 것은 안 지운다)
    root_r = root.resolve()
    targets = []
    for e in doomed:
        f = (root / str(e.get("path") or "")).resolve()
        if not str(e.get("path") or "") or not f.is_relative_to(root_r):
            print(f"! index 항목의 path 가 partial 밖이거나 비었다 ({e.get('path')!r}) — 지우지 않는다", file=sys.stderr)
            return 2
        targets.append((e, f))

    verb = "지웠다" if a.apply else "**지우지 않았다** (dry-run — 실제로 지우려면 `--apply`)"
    print(f"{'지울' if not a.apply else '지운'} 부분 산출 {len(doomed)} / 전체 {len(idx['attempts'])} "
          f"((종류, 산출)마다 최근 {a.keep} 개는 남긴다 · 삭제 단위는 **파일**이고 시도 디렉터리는 "
          f"retained 산출이 참조하지 않을 때만 정리한다)")
    for e, f in targets:
        print(f"  - {e['kind']}/{e['attempt']}/{e['artifact']}  [{e['status']}]  {e['sha256'][:12]}")
    if not a.apply:
        print(f"  → {verb}")
        return 0

    for e, f in targets:
        if f.is_file():
            f.unlink()
        att = root / e["kind"] / e["attempt"]
        if (e["kind"], e["attempt"]) not in retained_attempts and att.is_dir():
            shutil.rmtree(att)                       # 이 시도의 산출이 전부 버려졌을 때만
        parent = root / e["kind"]
        if parent.is_dir() and not any(parent.iterdir()):
            parent.rmdir()
    idx["attempts"] = retained
    (root / PARTIAL_INDEX).write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"  → {verb}. index 도 같은 항목 단위로 정리했다 (남은 부분 산출 {len(idx['attempts'])})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
