import json, glob, sys
for f in sorted(glob.glob('se_*.json')):
    try: m = json.load(open(f))
    except Exception: print(f'   {f:22} (읽기 실패)'); continue
    print(f"   {f:22} eps {m.get('porosity_settled_pct')}%  t {m.get('thickness_um')}um  "
          f"sig {m.get('final_stress_GPa')}  [g{m.get('n_grid')} sub{m.get('sub')} "
          f"to{m.get('compact_to_pct')}]")
