"""Independent numeric-limits and guard-sensitivity checks; review-only mutants."""
from pathlib import Path
import argparse, contextlib, hashlib, io, json, math, re, sys, types, warnings
from run_review import ROOT,HERE,prep
ap=argparse.ArgumentParser();ap.add_argument('--source',default=str(ROOT/'source'));a=ap.parse_args()
SRC=Path(a.source).resolve();prep(SRC)
import rint_iface_join as J
import numpy as np
T=HERE/'tmp/known_limits';T.mkdir(parents=True,exist_ok=True)

def files(tag,huge=False):
    centers=[(.002,.002,.002),(.0035,.002,.002)]
    if huge: centers += [(1e160,.002,.002),(1e160,.002,.002)]
    box=['ITEM: BOX BOUNDS ff ff ff']+['0 3e+160' if huge else '0 0.01']*3
    at=['ITEM: TIMESTEP','100','ITEM: NUMBER OF ATOMS',str(len(centers))]+box+['ITEM: ATOMS id type x y z radius']
    at += [str(i+1)+' '+('1' if i<2 else '2')+' '+' '.join('%g'%v for v in (*c,.001)) for i,c in enumerate(centers)]
    vals=[*centers[0],*centers[1],1,2,0]+[0]*12+[math.pi*(.001**2-.0015**2/4),.0005]
    ct=['ITEM: TIMESTEP','100','ITEM: NUMBER OF ENTRIES','2' if huge else '1']+box+['ITEM: ENTRIES '+' '.join('c_cpl[%d]'%i for i in range(1,24))]
    ct+=[' '.join('%g'%v for v in vals)]
    if huge:
        vals=[*centers[2],*centers[3],3,4,0]+[0]*12+[0,.0005]
        ct+=[' '.join('%g'%v for v in vals)]
    sc=[','.join(['1',*(f'{v:.12f}' for v in (*c,.001))]) for c in centers[:2]]
    out=[]
    for suf,ls in zip(('sc.csv','atom.dump','contact.dump'),(sc,at,ct)):
        p=T/(tag+'_'+suf);p.write_bytes(('\n'.join(ls)+'\n').encode());out.append(p)
    return out

def run(mod,paths,**kw):
    try:
        with warnings.catch_warnings(record=True) as ws:
            j=mod.am_iface_join(*paths,type_map={1:'AM_P',2:'SE'},**kw)
        return {'status':j['status'],'codes':[q['code'] for q in j['rejections']],
                'r_um':j['particles']['r_um'].tolist(),'area_um2':j['dem_am_am']['area_um2'].tolist(),
                'n_derived_nonfinite':j['g_frame'].get('n_derived_nonfinite'),'delta_bound_um':j['g_geo'].get('delta_bound_um'),
                'warnings':[str(w.message) for w in ws]}
    except Exception as e:return {'exception':type(e).__name__+': '+str(e)}

src=(SRC/'scripts/rint_iface_join.py').read_text(encoding='utf8')
needle='np.isfinite(dist) & np.isfinite(wd) & np.isfinite(dd)'
assert src.count(needle)==1
mut=types.ModuleType('join_without_wd_guard');mut.__file__=str(SRC/'scripts/rint_iface_join.py')
exec(compile(src.replace(needle,'np.isfinite(dist) & np.isfinite(dd)'),mut.__file__,'exec'),mut.__dict__)
normal=files('normal');huge=files('wd_only',True)
out={'source':str(SRC),'normal':run(J,normal),'known_underflow':run(J,normal,sim_to_um=5e-324),
     'wd_only_current':run(J,huge),'wd_only_mutant':run(mut,huge),
     'numeric_oracle':{'distance_exact':0,'delta_true':.002,'delta_recorded':.0005,'delta_mismatch':.0015}}
# Verify test fixture portability independently, without touching test code.
p=T/'windows_default_text.txt'
with open(p,'w',encoding='utf8') as f:f.write('A\nB\n')
raw=p.read_bytes();encoded=raw.replace(b'\n',b'\r\n')
out['newline_fixture']={'default_bytes_hex':raw.hex(),'reencoded_hex':encoded.hex(),
                        'crcrlf_count':encoded.count(b'\r\r\n'),'platform':sys.platform}
(HERE/'evidence/known_limit_and_mutant.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(out,ensure_ascii=False,indent=2))
