#!/usr/bin/env python3
"""반쪽전지를 **하나로 고정한** 데이터 루트를 만들고(`make`), 확인한다(`check`).

## 무엇을 가르려고 만드나

원통형 셀(#168 · #171)의 LAM/LLI 띠가 파우치보다 넓게 나왔다. 그런데 그
셀들은 반쪽전지를 **한 번만 재서** `prepare_cell.py` 가 같은 파일을 네 상태
이름으로 복사했다. 그러면 두 가지가 섞인다:

  (가) 셀이 실제로 다르다
  (나) 우리가 반쪽전지를 대체했다

`LLI = (c_lit_i − c_lit)/c_lit_i`, `c_lit = (a_PE + b_PE − b_NE)·c` 이므로
(나)는 **LLI 폭에 직접** 들어간다 (LAM_PE 도 마찬가지, LAM_NE 만 절연).
그래서 (나)를 **파우치에서 재현**해 본다 — 파우치는 상태마다 반쪽전지를
따로 쟀으므로, 그것을 일부러 pristine 하나로 고정해 다시 돌리면 (나)만
분리된다. 파우치 원본 대비 띠가 원통형만큼 벌어지면 원인은 (나)이고,
안 벌어지면 (가)가 남는다.

## 사용법

    # 만들기 — 파우치 루트에서 반쪽전지만 pristine 으로 고정한 사본
    python3 scripts/fixed_hc.py make \\
        --src "$BMS_DATA_ROOT" --out ~/dd/cells/pouch_fixedhc --pin pristine

    # 확인 — 어떤 루트가 정말 고정본인지 (이미 돈 실행에도 쓴다)
    python3 scripts/fixed_hc.py check --root ~/dd/cells/pouch_fixedhc
    python3 scripts/fixed_hc.py check --root "$BMS_DATA_ROOT"   # 원본은 "상태마다 다름"

`check` 는 **파일 해시로** 말한다. 실행 로그의 "반쪽전지 소스: 100=GITT ..."
는 소스 *종류*만 찍으므로 고정 여부를 알려주지 않는다 — 그 구멍을 메운다.
"""
from __future__ import annotations
import argparse, hashlib, shutil, sys
from pathlib import Path

#: 반쪽전지 소스별 파일 이름 규칙 (`bms_balancing/data.py` 와 같은 규약).
HC = {"GITT": "{state}.xlsx", "step_005C": "{state}_005C.xlsx"}


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def scan(root: Path) -> dict[str, dict[str, Path]]:
    """{소스: {상태: 경로}} — 실제로 있는 파일만."""
    found: dict[str, dict[str, Path]] = {}
    for src, pat in HC.items():
        d = root / "data" / "half_cell" / src
        if not d.is_dir():
            continue
        # 이름 꼬리표: GITT 는 "", step_005C 는 "_005C".
        # ⚠ 꼬리표가 "" 일 때 `st[:-0]` 은 `st[:0]` 이라 **빈 문자열**이 된다.
        #   첫 판이 그래서 네 상태를 전부 하나로 뭉갰고, 그러면 `check` 가
        #   "상태가 1 개뿐이라 판정불가" 를 내며 조용히 쓸모없어진다
        #   (2026-09-11, 아래 테스트가 잡았다). 그래서 빈 꼬리표는 **안 자른다.**
        tail = pat.format(state="")[:-len(".xlsx")]
        states = {}
        for f in sorted(d.glob("*.xlsx")):
            st = f.stem
            if tail:
                if not st.endswith(tail):
                    continue
                st = st[:-len(tail)]
            states[st] = f
        if states:
            found[src] = states
    return found


def cmd_check(a) -> int:
    root = Path(a.root).expanduser()
    found = scan(root)
    if not found:
        print(f"반쪽전지 디렉터리가 없다: {root}/data/half_cell/", file=sys.stderr)
        return 1

    verdicts = {}
    for src, states in found.items():
        print(f"\n[{src}]  {root}/data/half_cell/{src}")
        digests = {st: sha(p) for st, p in states.items()}
        for st, p in states.items():
            print(f"  {st:12} {digests[st][:16]}  {p.name}")
        uniq = set(digests.values())
        if len(states) < 2:
            v = "판정불가"
            print(f"  → 상태가 {len(states)} 개뿐이라 고정 여부를 말할 수 없다")
        elif len(uniq) == 1:
            v = "fixed"
            print(f"  → **고정됨** — {len(states)} 상태가 전부 같은 파일이다")
        else:
            v = "per-state"
            print(f"  → 상태마다 다름 — 서로 다른 파일 {len(uniq)} 개")
        verdicts[src] = v

    if a.expect:
        bad = {s: v for s, v in verdicts.items() if v != a.expect}
        if bad:
            print(f"\n기대 `{a.expect}` 와 다르다: {bad}", file=sys.stderr)
            return 2
        print(f"\n기대 `{a.expect}` 와 같다.")
    return 0


def cmd_make(a) -> int:
    src, out = Path(a.src).expanduser(), Path(a.out).expanduser()
    found = scan(src)
    if not found:
        print(f"원본에 반쪽전지가 없다: {src}", file=sys.stderr)
        return 1

    # 풀셀·문헌 곡선은 **그대로** 가져온다 — 이 실험이 건드리는 축은 반쪽전지뿐.
    for rel in ("data/full_cell", "data/literature"):
        s, d = src / rel, out / rel
        if not s.is_dir():
            print(f"원본에 없다: {s}", file=sys.stderr)
            return 1
        if d.exists():
            shutil.rmtree(d)
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(s, d)
        print(f"→ {d}  (원본 그대로)")

    for hsrc, states in found.items():
        if a.pin not in states:
            print(f"[{hsrc}] `{a.pin}` 이 없다 — 건너뛴다 "
                  f"(있는 것: {', '.join(sorted(states))})", file=sys.stderr)
            continue
        pin = states[a.pin]
        d = out / "data" / "half_cell" / hsrc
        d.mkdir(parents=True, exist_ok=True)
        for st, p in states.items():
            shutil.copyfile(pin, d / p.name)
        print(f"→ {d}  ({len(states)} 상태 전부 `{pin.name}` 하나로 — "
              f"sha {sha(pin)[:16]})")

    print("\n확인:")
    return cmd_check(argparse.Namespace(root=str(out), expect="fixed"))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("make", help="반쪽전지를 하나로 고정한 루트를 만든다")
    m.add_argument("--src", required=True, help="원본 BMS_DATA_ROOT")
    m.add_argument("--out", required=True, help="만들 루트")
    m.add_argument("--pin", default="pristine", help="어느 상태의 반쪽전지로 고정할지")
    m.set_defaults(fn=cmd_make)

    c = sub.add_parser("check", help="루트가 고정본인지 해시로 확인한다")
    c.add_argument("--root", required=True)
    c.add_argument("--expect", choices=("fixed", "per-state"),
                   help="기대와 다르면 exit 2")
    c.set_defaults(fn=cmd_check)

    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    raise SystemExit(main())
