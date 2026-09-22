"""Ordinary imports only; does not forge receipts, mutate production, or change OS policy."""
from __future__ import annotations
import argparse
import hashlib
import importlib
import json
import os
from pathlib import Path
import sys
import zipfile

p=argparse.ArgumentParser()
p.add_argument('--repo', type=Path, required=True)
p.add_argument('--out', type=Path, required=True)
a=p.parse_args()
a.repo=a.repo.resolve()
a.out=a.out.resolve()
a.out.mkdir(parents=True, exist_ok=False)
sys.path.insert(0, str(a.repo/'docs/22p_gap'))
import mutation_replay as mr
original_env=mr.replay_env
original_root=mr.ROOT
original_cwd=Path.cwd()
rows=[]

def case(name, content, *, disabled=False, relative=False, namespace=False, zip_member=False):
    d=a.out/name
    child=d/'child'
    parent=d/'parent'
    child.mkdir(parents=True)
    parent.mkdir()
    startup=child/'startup'
    startup.mkdir()
    if namespace:
        (startup/'sitecustomize').mkdir()
    elif zip_member:
        z=startup/'startup.zip'
        with zipfile.ZipFile(z,'w') as f:
            f.writestr('sitecustomize/__init__.py', content)
    else:
        (startup/'sitecustomize.py').write_text(content, encoding='utf-8')
    (startup/'usercustomize.py').write_text('# ordinary user customization\nVALUE = 42\n',encoding='utf-8')
    if relative:
        (parent/'startup').mkdir()
        (parent/'startup/sitecustomize.py').write_text('# different ordinary module in caller cwd\n',encoding='utf-8')
    env=dict(original_env())
    env['PYTHONPATH']='startup' if relative else str(z if zip_member else startup)
    if disabled:
        env['PYTHONNOUSERSITE']='1'
    mr.replay_env=lambda: dict(env)
    mr.ROOT=child
    os.chdir(parent if relative else original_cwd)
    rec={'case':name,'env':{k:env[k] for k in ('PYTHONPATH','PYTHONNOUSERSITE') if k in env},'parent_cwd':str(Path.cwd()),'probe_cwd':str(child)}
    try:
        full=mr._run_probe(f'_receipt_facts({mr._probe_names()!r}, [], {str(child)!r})',child,'review')
        got=full['startup']
        rec['startup']=got
        try:
            mr._assert_receipt_is_complete(full)
            rec['completeness']='PASS'
        except Exception as exc:
            rec['completeness']=f'{type(exc).__name__}: {exc}'
        rec['parent']=mr._parent_customization_view()
        try:
            mr._assert_customization_matches_parent({'startup':got})
            rec['comparison']='ACCEPTED'
        except Exception as exc:
            rec['comparison']='REJECTED'
            rec['error']=f'{type(exc).__name__}: {exc}'
    except Exception as exc:
        rec['error']=f'{type(exc).__name__}: {exc}'
    finally:
        os.chdir(original_cwd)
        mr.ROOT=original_root
        mr.replay_env=original_env
        importlib.invalidate_caches()
    (d/'observation.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2),encoding='utf-8')
    rows.append({'case':name,'startup_status':rec.get('startup',{}).get('status'),'completeness':rec.get('completeness'),
                 'history':rec.get('startup',{}).get('startup_history'),
                 'comparison':rec.get('comparison'),'error':rec.get('error')})

case('plain_control','# ordinary startup\n',disabled=True)
case('zip_control','# ordinary ZIP startup\n',disabled=True,zip_member=True)
case('disabled_but_explicit_import','import usercustomize\n',disabled=True)
case('normal_namespace_package','',disabled=True,namespace=True)
case('relative_pythonpath','# ordinary replay cwd startup\n',disabled=True,relative=True)
case('enabled_control','import site\n',disabled=False)
(a.out/'summary.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
for r in rows:
    h=r.pop('history',None)
    r['history_status']=h.get('status') if h else None
    r['history_reason']=h.get('reason') if h else None
    print(json.dumps(r,ensure_ascii=False))
