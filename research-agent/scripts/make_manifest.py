#!/usr/bin/env python3
"""전달 매니페스트 생성·검증 — 사람이 세지 않는다.

v0.1.6 과 v0.1.8 에서 같은 실패가 났다: 회신문의 파일 목록과 실제로 도착한 파일이 달랐고,
두 번 다 "1:1 대조했다"고 적혀 있었다. 목록도 사람이 쓰고 대조도 사람이 하면 같은 순간에
두 번 실수해서 안 걸린다. ⇒ 목록을 **실제 파일에서 기계로** 뽑고, **받는 쪽이** 검증한다.

## kind — 파일이 어디까지 사는가
    code       repo 에 그대로 들어간다. 묶음에도 repo 에도 있어야 한다
    doc        repo 에 들어가는 문서 (`cowork/REPLY_*.md`). 위와 같다
    transient  **전달 전용.** repo 에는 이 이름으로 존재하지 않는다
               · `CHANGELOG_<ver>.md` — 규약상 받는 쪽이 `CHANGELOG.md` 에 splice 하고 버린다
               · `MANIFEST_<ver>.md`  — 전달 문서 자신

`transient` 가 없으면 **올바른 전달에서도 항상 MISSING 이 뜬다.** v0.1.10 이 그랬다.
늑대가 왔다고 매번 외치는 검사는 두세 판 안에 아무도 안 본다 — 그러면 진짜 유실이 묻힌다.
그래서 이건 편의 기능이 아니라 **도구가 살아남기 위한 조건**이다.

## 어디서 도는가
    --from <dir>   전달 묶음(평면 디렉터리)에서 basename 으로 대조. **복사하기 전에** 확인.
                   transient 까지 전부 검사한다. 이게 원래 쓰고 싶은 자리다.
    (없으면)       repo 기준. code·doc 만 검사하고 transient 는 건너뛴다(`skip`).

## 사용
    python scripts/make_manifest.py 0.1.11 <코드...> --doc <문서...> --transient <조각...>
    python scripts/make_manifest.py --verify MANIFEST_0.1.11.md --from .   # 묶음에서
    python scripts/make_manifest.py --verify MANIFEST_0.1.11.md            # 병합 후 repo 에서
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KINDS = ("code", "doc", "transient")
_ROW = re.compile(
    r"^\|\s*`([^`]+)`\s*\|\s*(code|doc|transient)\s*\|\s*([\d—]+)\s*\|\s*([\d—]+)\s*\|\s*`([0-9a-f—]+)`\s*\|$",
    re.M)


def _digest(p: Path) -> tuple[str, int, int]:
    data = p.read_bytes()
    lines = data.count(b"\n") + (0 if data.endswith(b"\n") or not data else 1)
    return hashlib.sha256(data).hexdigest()[:16], lines, len(data)


# --------------------------------------------------------------------------- build
def build(version: str, code: list[str], docs: list[str], transient: list[str]) -> str:
    self_name = f"MANIFEST_{version}.md"
    transient = list(dict.fromkeys([*transient, self_name]))   # 매니페스트 자신도 첨부물
    rows, missing = [], []
    for kind, group in (("code", code), ("doc", docs), ("transient", transient)):
        for rel in sorted(dict.fromkeys(group)):
            if rel == self_name:                               # 자기 참조 — 해시를 못 낸다
                rows.append((rel, kind, None, None, "—"))
                continue
            p = (ROOT / rel) if not Path(rel).is_absolute() else Path(rel)
            if not p.exists():
                missing.append(rel)
                continue
            sha, lines, size = _digest(p)
            rows.append((rel, kind, lines, size, sha))
    n = {k: sum(1 for r in rows if r[1] == k) for k in KINDS}
    out = [f"# 전달 매니페스트 — v{version}", "",
           f"**첨부 {len(rows)}개** (code {n['code']} · doc {n['doc']} · transient {n['transient']}).",
           "이 표의 줄 수와 실제 첨부 개수가 **같아야 한다** — 다르면 그 자체가 유실 신호다.", "",
           "```bash",
           f"python scripts/make_manifest.py --verify {self_name} --from .   # 묶음에서 (복사 전)",
           f"python scripts/make_manifest.py --verify {self_name}            # 병합 후 repo 에서",
           "```",
           "`MISSING`(파일 없음) / `MISMATCH`(내용 다름) 가 하나라도 나오면 **병합하지 말고 회신해 주십시오.**",
           "",
           "`transient` 는 **전달 전용**이라 repo 에 그 이름으로 남지 않는다 — `--from` 없이 돌리면",
           "`skip` 으로 건너뛴다. 매니페스트 자신은 자기 참조라 해시가 `—` 이고 존재만 확인한다.", "",
           "| 파일 | kind | 줄 | 바이트 | sha256[:16] |", "|---|---|---:|---:|---|"]
    out += [f"| `{r}` | {k} | {l if l is not None else '—'} | {s if s is not None else '—'} | `{h}` |"
            for r, k, l, s, h in rows]
    if missing:
        out += ["", "⛔ **보내는 쪽에서 찾지 못한 파일** (전달 전에 해결할 것):"]
        out += [f"- `{m}`" for m in missing]
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------- verify
def verify(manifest: Path, bundle: Path | None = None) -> int:
    rows = _ROW.findall(manifest.read_text(encoding="utf-8"))
    if not rows:
        print("매니페스트에서 파일 표를 찾지 못했다 (v0.1.11 이전 형식이면 kind 열이 다르다). "
              "make_manifest.py 를 먼저 갱신하십시오.", file=sys.stderr)
        return 2
    bad = skipped = 0
    for rel, kind, lines, size, sha in rows:
        if bundle is not None:
            p = bundle / Path(rel).name          # 묶음은 평면이라 basename 으로 찾는다
        elif kind == "transient":
            print(f"skip      [{kind}] {rel}  (전달 전용 — repo 에는 없는 것이 정상)")
            skipped += 1
            continue
        else:
            p = ROOT / rel
        if not p.exists():
            print(f"MISSING   [{kind}] {rel}")
            bad += 1
            continue
        if sha == "—":                            # 매니페스트 자신 — 존재만 본다
            print(f"ok(self)  [{kind}] {rel}")
            continue
        got_sha, got_lines, _ = _digest(p)
        if got_sha != sha:
            print(f"MISMATCH  [{kind}] {rel}  (기대 {sha} / 실제 {got_sha}, {lines}→{got_lines}줄)")
            bad += 1
        else:
            print(f"ok        [{kind}] {rel}")
    checked = len(rows) - skipped
    tail = "" if not bad else f"  ⛔ {bad}건 문제 — 병합하지 말 것"
    where = f"묶음 {bundle}" if bundle is not None else "repo"
    print(f"\n{checked - bad}/{checked} 일치 ({where})"
          + (f" · transient {skipped}건 건너뜀 — `--from <묶음>` 으로 돌리면 이것도 검사한다"
             if skipped else "") + tail)
    return 1 if bad else 0


# --------------------------------------------------------------------------- cli
def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    if argv[0] == "--verify":
        rest = argv[1:]
        bundle = None
        if "--from" in rest:
            i = rest.index("--from")
            bundle = Path(rest[i + 1])
            rest = rest[:i] + rest[i + 2:]
        if not rest:
            print("--verify 에 매니페스트 경로가 없다.", file=sys.stderr)
            return 2
        return verify(Path(rest[0]), bundle)
    version, groups, cur = argv[0], {"code": [], "doc": [], "transient": []}, "code"
    for a in argv[1:]:
        if a in ("--doc", "--transient"):
            cur = a[2:]
            continue
        groups[cur].append(a)
    print(build(version, groups["code"], groups["doc"], groups["transient"]), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
