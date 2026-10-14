from pathlib import Path
import urllib.request,json,hashlib
R=Path(__file__).resolve().parent; M=R/'upstream_manifest.json';m=json.loads(M.read_text());up=m['pin']
for p in ['mesh_mover_linear.cpp','tracking_mesh.h','tracking_mesh_I.h','domain.cpp']:
    try:
        with urllib.request.urlopen('https://raw.githubusercontent.com/CFDEMproject/LIGGGHTS-PUBLIC/'+up+'/src/'+p,timeout=40) as r:b=r.read()
        (R/'upstream'/p).write_bytes(b)
        m['files']=[x for x in m['files'] if x['path']!=p]+[{'path':p,'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}]
        print(p,len(b))
    except Exception as e:print(p,type(e).__name__,str(e))
M.write_text(json.dumps(m,indent=2),encoding='utf8')
