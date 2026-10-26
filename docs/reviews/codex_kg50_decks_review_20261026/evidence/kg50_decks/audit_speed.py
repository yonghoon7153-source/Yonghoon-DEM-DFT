from pathlib import Path
import re,json,math
root=Path('../../snapshot/repo/docs/data/kg50_decks_20261026'); m=json.loads((root/'manifest.json').read_text(encoding='utf8')); out=[]
prod=(root/'kg50_d07_b40/input_kg50_d07_b40.liggghts').read_text(encoding='utf8')
for r in m['speed_tests']:
 c=r['case']; t=(root/'speed'/c/f'input_{c}.liggghts').read_text(encoding='utf8'); exe=[x for x in t.splitlines() if x.strip() and not x.lstrip().startswith('#')]
 v=re.findall(r'particletemplate/sphere (\d+)|particledistribution/discrete (\d+)|insert/pack seed (\d+)',t)
 s=[int(next(y for y in x if y)) for x in v]; base=[int(next(y for y in x if y)) for x in re.findall(r'particletemplate/sphere (\d+)|particledistribution/discrete (\d+)|insert/pack seed (\d+)',prod)]
 n=r['speed_test']['ntasks']; boxes=[(a,n//a,40/a,40/(n//a)) for a in range(1,n+1) if n%a==0]
 out.append(dict(case=c,seeds_equal=s==base,skin_line=[x for x in exe if x.startswith('neighbor ')],last_command=exe[-1],no_am_gate=not any('g_am_ins' in x for x in exe),total_gate=any('count(all)' in x for x in exe),no_full_settling='run 200000' not in t,best_min_subdomain_um=max(min(x[2],x[3]) for x in boxes),am_diameter_um=6))
print(json.dumps(out,indent=2)); Path('speed-independent.json').write_text(json.dumps(out,indent=2)+'\n')
