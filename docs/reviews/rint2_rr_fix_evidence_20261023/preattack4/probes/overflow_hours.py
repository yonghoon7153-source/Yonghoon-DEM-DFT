#!/usr/bin/env python3
"""Recompute design L173 '+24 팔 ≈ 86.7 – 104.9 h' from q9_time_budget.json (4040e4388) — and check the JSON's own multiplier."""
import json, sys
d = json.load(open(sys.argv[1]))
i = d['inputs']
f = i['solve_fraction']
mult = {k: 1 + f * (r - 1) for k, r in zip(('lo', 'hi'), i['iter_ratio'])}
print(json.dumps({'dbe_arm_s': i['dbe_arm_s'], 'multiplier_json': i['multiplier'], 'multiplier_recomputed': {k: round(v, 4) for k, v in mult.items()},
                  'overflow_24_arms_h': {k: round(24 * i['dbe_arm_s'] * i['multiplier'][k] / 3600, 2) for k in ('lo', 'hi')},
                  'json_overflow_note': d.get('overflow_note')}, ensure_ascii=False, indent=1))
