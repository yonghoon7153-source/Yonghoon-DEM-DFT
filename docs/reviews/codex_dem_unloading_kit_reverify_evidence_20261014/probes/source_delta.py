"""Offline byte/provenance comparisons; no target source mutation."""
from pathlib import Path
import json, hashlib, difflib
R = Path(__file__).resolve().parents[1]
OLD = R/'comparison_base'
if not OLD.exists():
    OLD = R.parent/'dem_unloading_kit_review_20261014/source'
NEW = R/'source'
K = Path('docs/data/ps45_unload_20261009')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def scalar_diff(a,b,path=''):
    if isinstance(a,dict) and isinstance(b,dict):
        out=[]
        for k in sorted(a.keys()|b.keys()):
            out.extend(scalar_diff(a.get(k),b.get(k),path+'/'+k))
        return out
    return [] if a==b else [{'path':path,'old':a,'new':b}]
files=[]
for p in (NEW/K).rglob('*'):
    if not p.is_file() or '__pycache__' in p.parts: continue
    rel=p.relative_to(NEW); old=OLD/rel
    files.append({'path':str(rel).replace('\\','/'),'same':old.exists() and old.read_bytes()==p.read_bytes(),
                  'new_sha256':sha(p),'old_sha256':sha(old) if old.exists() else None})
Pold=json.loads((OLD/K/'unload_params.json').read_text(encoding='utf8'))
Pnew=json.loads((NEW/K/'unload_params.json').read_text(encoding='utf8'))
history=[f for f in files if '/history_test/in.' in f['path'] and f['old_sha256']]
manifest=json.loads((R/'source_manifest.json').read_text(encoding='utf8'))
entries=manifest['files'] if 'files' in manifest else manifest['entries']
if isinstance(entries,dict): entries=list(entries.values())
checked=[]
for e in entries:
    checked.append({'path':e['path'],'same':sha(NEW/e['path'])==e['sha256']})
out={'params_diff':scalar_diff(Pold,Pnew),'kit_files':files,'old_history_decks':history,
     'old_history_decks_all_equal':all(f['same'] for f in history),
     'source_files_checked':len(checked),'source_unchanged':all(f['same'] for f in checked),
     'source_changes':[f for f in checked if not f['same']]}
(R/'evidence/source_delta.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
diff=[]
for rel in [K/'ul_reader.py',K/'make_unload_decks.py',K/'run_unload.sh',K/'history_test/make_history_decks.py',
            Path('docs/reviews/dem_unloading_ps45_prereg_20261009.md')]:
    diff.extend(difflib.unified_diff((OLD/rel).read_text(encoding='utf8').splitlines(True),
        (NEW/rel).read_text(encoding='utf8').splitlines(True),fromfile='old/'+str(rel),tofile='new/'+str(rel)))
(R/'evidence/target_delta.diff').write_text(''.join(diff),encoding='utf8')
print(json.dumps({k:v for k,v in out.items() if k not in ('kit_files','old_history_decks')},ensure_ascii=False,indent=2))
