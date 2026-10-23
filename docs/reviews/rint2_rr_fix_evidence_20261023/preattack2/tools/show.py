"""show.py <json> <prefix> [maxlen] — print entries whose key starts with prefix, compact."""
import json
import sys
d = json.load(open(sys.argv[1], encoding='utf-8'))
pre = sys.argv[2]
mx = int(sys.argv[3]) if len(sys.argv) > 3 else 700
for k, v in d.items():
    if k.startswith(pre):
        s = json.dumps(v, ensure_ascii=False, default=str)
        print(k, '=>', s[:mx])
        print()
