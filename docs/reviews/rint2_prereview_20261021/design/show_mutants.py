import json
import os
import sys

d = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe_registration_v3.json')))
for k, v in d['l_end_rule_mutants'].items():
    print(k, {kk: (round(vv, 6) if isinstance(vv, float) else vv) for kk, vv in v.items()})
