"""Check unique label coverage across all search tiers for four fields."""
import importlib.util
import itertools
import json
from pathlib import Path
import sys

kernel_file, out = map(Path,sys.argv[1:])
spec = importlib.util.spec_from_file_location("kernel_for_coverage", kernel_file)
kernel = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kernel)
cases = []
for choices in (("open","normal"),("open","stick","positive","negative")):
    closed = choices[1:]
    all_modes = set(itertools.product(choices,repeat=6))
    for k in range(7):
        guess = [closed[i % len(closed)] if i < k else "open" for i in range(6)]
        first = {t for t in all_modes if sum(a!=b for a,b in zip(guess,t))<=2}
        for t in all_modes:
            if all(a==b or b=="open" for a,b in zip(guess,t)):
                first.add(t)
        last = list(kernel._remaining_four_body_faces(guess,choices))
        assert len(last)==len(set(last))
        assert not first.intersection(last) and first.union(last)==all_modes
        cases.append({"choices":len(choices),"warm_active":k,
                      "earlier":len(first),"last_tier":len(last),"total":len(all_modes)})
out.write_text(json.dumps(cases,indent=2)+"\n",encoding="utf-8")
print(len(cases),"label-set partition checks passed")
