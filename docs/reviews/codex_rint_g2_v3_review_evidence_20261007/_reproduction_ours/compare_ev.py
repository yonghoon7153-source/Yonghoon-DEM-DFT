"""Compare two evidence JSON files leaf by leaf.

Usage: python3 -I -B compare_ev.py <codex.json> <ours.json> [label]
Prints counts of identical leaves (numbers, strings, bools) and each difference
with the relative difference for numbers.
"""
import json
import sys


def flat(x, p=""):
    if isinstance(x, dict):
        for k, v in x.items():
            yield from flat(v, f"{p}.{k}" if p else k)
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from flat(v, f"{p}[{i}]")
    else:
        yield p, x


def main():
    a, b = (dict(flat(json.load(open(f, encoding="utf8")))) for f in sys.argv[1:3])
    label = sys.argv[3] if len(sys.argv) > 3 else ""
    keys = sorted(set(a) | set(b))
    only_a = [k for k in keys if k not in b]
    only_b = [k for k in keys if k not in a]
    common = [k for k in keys if k in a and k in b]
    num = [k for k in common if isinstance(a[k], (int, float)) and not isinstance(a[k], bool)]
    same_num = [k for k in num if a[k] == b[k] and type(a[k]) is type(b[k])]
    other = [k for k in common if k not in num]
    same_other = [k for k in other if a[k] == b[k]]
    print(f"[{label}] leaves: common {len(common)} · only codex {len(only_a)} · only ours {len(only_b)}")
    print(f"[{label}] numeric leaves {len(num)} · bit-identical {len(same_num)}")
    print(f"[{label}] non-numeric leaves {len(other)} · identical {len(same_other)}")
    for k in num:
        if k in same_num:
            continue
        x, y = a[k], b[k]
        rel = abs(y - x) / abs(x) if x not in (0, 0.0) else float("inf")
        print(f"  NUM  {k}: codex {x!r} -> ours {y!r}  rel {rel:.3g}")
    for k in other:
        if a[k] != b[k]:
            print(f"  OTHER {k}: codex {a[k]!r} -> ours {b[k]!r}")
    for k in only_a:
        print(f"  ONLY-CODEX {k}: {a[k]!r}")
    for k in only_b:
        print(f"  ONLY-OURS {k}: {b[k]!r}")


if __name__ == "__main__":
    main()
