"""Integer model of output.cpp periodic scheduling; does not execute LIGGGHTS."""
from pathlib import Path
import re,json,math
HERE=Path(__file__).resolve().parent
p=HERE.parents[1]/'snapshot/repo/docs/data/kg50_decks_20261026/kg50_d07_b40/input_kg50_d07_b40.liggghts'
t=p.read_text(encoding='utf8'); command=[x.strip() for x in t.splitlines() if x.strip() and not x.lstrip().startswith('#')]
assert [int(x.split()[1]) for x in command if x.startswith('run ')]==[1,200000,1,200000,5000,100000]
assert not any(x.startswith(('write_dump ','dump_modify ')) for x in command)
atom=int(re.search(r'^dump dmp_atom all custom (\d+)',t,re.M).group(1)); contact=int(re.search(r'^dump dmp_contact all local (\d+)',t,re.M).group(1)); mesh=int(re.search(r'^dump dmp_mesh all mesh/stl (\d+)',t,re.M).group(1)); common=math.lcm(atom,contact,mesh)
rows=[]
for k in range(1010,1020):
 compression_end=1+200000+1+200000+5000*k; end=compression_end+100000; last=end//common*common
 rows.append(dict(k=k,compression_end=compression_end,final_step=end,atom_last=end//atom*atom,contact_last=end//contact*contact,mesh_last=end//mesh*mesh,common_last=last,saved_relaxation_steps=last-compression_end,gap_steps=end-last,old_atom_last=end//5000*5000,old_common_last=end//10000*10000))
(HERE/'terminal_cadence.json').write_text(json.dumps(dict(atom=atom,contact=contact,mesh=mesh,terminal_export=False,rows=rows),indent=2)+'\n')
for r in rows:print(r)

