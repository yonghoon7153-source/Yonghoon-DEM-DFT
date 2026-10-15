from pathlib import Path
import sys,json,hashlib,re
R=Path(__file__).resolve().parents[1];K=R/'source/docs/data/ps45_unload_20261009';sys.path.insert(0,str(K))
import make_unload_decks as g
P=g.ul_lib.load_params();rows=[]
for b,k in g.deck_names():
    path=K/'decks'/b/('in.'+k+'.liggghts');actual=path.read_bytes();expected=g.render(b,k,P=P).encode('utf8')
    rows.append({'bed':b,'deck':k,'bytes_equal':actual==expected,'sha256':hashlib.sha256(actual).hexdigest()})
out={'rendered_decks':rows,'all_equal':all(r['bytes_equal'] for r in rows),'physical':{a:g.physical(g.render('ps_7_3_r45',a,P=P)) for a in ['U_UB','UT','U_UVa','U_UVb','U_UT3','G_UVa','G_UVb']}}
assert out['all_equal'] and len(rows)==64
(R/'evidence/kit_byte_checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print('64/64 generated deck bytes equal pinned; physical table recorded')
