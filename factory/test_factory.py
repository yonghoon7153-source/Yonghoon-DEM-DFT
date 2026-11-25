#!/usr/bin/env python3
"""test_factory.py — CI guard for the report-card pipeline.

Checks, for every system in SYSTEMS:
  1. the card builds without error,
  2. it validates against schema/report_card.schema.json (if jsonschema present),
  3. NO system-specific physics leaks into another system's card
     (audit round-2 BUG 4b regression guard).

  python3 factory/test_factory.py   # exit 0 = pass, 1 = fail
"""
import json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import assemble_report_card as A

# b2o3-specific VALIDATION RESULTS that must NEVER appear in another system's card.
# (Specific computed values/verdicts, not generic chemistry terms like "BS3" which
# legitimately appear in generic roadmap descriptions.)
B2O3_FINGERPRINTS = ["soft Li band", "18.51", "DYNAMICALLY STABLE (0 imaginary",
                     "free-S2-(low BE)", "+37.5 meV", "B0 +13%"]


def main():
    fails = []
    schema = json.loads((HERE / "schema" / "report_card.schema.json").read_text())
    try:
        import jsonschema
        V = jsonschema.Draft202012Validator(schema)
    except ImportError:
        V = None
        print("WARN: jsonschema not installed -> skipping schema validation")

    for sysid in A.SYSTEMS:
        try:
            card = A.build(sysid, stamp="TEST")
        except Exception as e:
            fails.append(f"{sysid}: build raised {type(e).__name__}: {e}")
            continue
        if V:
            errs = list(V.iter_errors(card))
            if errs:
                fails.append(f"{sysid}: {len(errs)} schema errors (first: {errs[0].message[:80]})")
        if sysid != "b2o3":
            blob = json.dumps(card, ensure_ascii=False)
            leaked = [fp for fp in B2O3_FINGERPRINTS if fp in blob]
            if leaked:
                fails.append(f"{sysid}: b2o3 physics leaked into card: {leaked}")
        print(f"  {sysid:8s} {card['overall']['completeness']}")

    if fails:
        print("\nFAIL:")
        for x in fails:
            print("  -", x)
        sys.exit(1)
    print("\nOK: all cards build + validate + no cross-system leakage")


if __name__ == "__main__":
    main()
