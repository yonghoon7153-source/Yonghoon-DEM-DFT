#!/usr/bin/env python3
"""Retracted-value sweep for files OUTSIDE the repo (AVI work files).

  python3 -I ban_sweep_files.py FILE [FILE ...]      rc 1 if any banned pattern appears

Same registry and the same normalisation as the repo's `scripts/check_review_findings.py --ban-sweep`
(`docs/reviews/claims.json` → `quotation_ban` · `_ban_norm`: NBSP/thin spaces → space, JSON %/+ escapes,
trailing zeros of numbers trimmed, space before % removed).  The repo is only READ (json file);
nothing is imported from it or written there.  No banner / near-line exemption: a public video has none.
"""
import json
import os
import re
import sys

CLAIMS = os.environ.get("AVI_CLAIMS_JSON") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "reviews", "claims.json")
_WS = {" ": " ", " ": " ", " ": " ", " ": " "}


def norm(text):          # == check_review_findings._ban_norm (copied, not imported)
    for a, b in _WS.items():
        text = text.replace(a, b)
    text = text.replace("\\u0025", "%").replace("\\u002B", "+")
    text = re.sub(r"(\d)\.0+(?=\D|$)", r"\1", text)
    text = re.sub(r"(\.\d*?)0+(?=\D|$)", r"\1", text)
    text = re.sub(r"\s+%", "%", text)
    return text


def main(paths):
    bans = json.load(open(CLAIMS, encoding="utf-8")).get("quotation_ban") or []
    hits = 0
    for p in paths:
        try:
            lines = open(p, encoding="utf-8").read().split("\n")
        except (UnicodeDecodeError, OSError) as ex:
            print(f"SKIP {p}: {ex}")
            continue
        nl = [norm(x) for x in lines]
        for b in bans:
            pat = b.get("pattern")
            if not pat:
                continue
            npat = norm(pat)
            for i, (ln, nn) in enumerate(zip(lines, nl)):
                if pat in ln or npat in nn:
                    hits += 1
                    print(f"BAN {p}:{i + 1} — '{pat}' ({b.get('claim')})")
    print(f"ban sweep: {len(bans)} patterns · {len(paths)} files · hits {hits}")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
