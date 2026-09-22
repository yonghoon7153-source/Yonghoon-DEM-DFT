"""Read-only git object accounting; never changes registry entries."""
import collections,hashlib,json,pathlib,subprocess
HERE=pathlib.Path(__file__).resolve().parent
REPO=HERE.parents[1]/'work/gate66-head'
OLD='5e4cf1038f0f26a6a624d9984386cfd046657ac3'
NEW='fa947cc9b17cdbeffbb39447c99159bc2c831e6e'
PREFIX='degradation-degeneracy/docs/22p_gap/_exec_class/'
def git(*args):return subprocess.check_output(['git','-C',str(REPO),*args])
def inventory(ref):
 paths=git('ls-tree','--name-only',ref,PREFIX).decode().splitlines()
 return {p:json.loads(git('show',ref+':'+p)) for p in paths if p.endswith('.json')}
old,new=inventory(OLD),inventory(NEW)
deleted=sorted(set(old)-set(new));added=sorted(set(new)-set(old))
rows=[]
for p in deleted:
 data=git('show',OLD+':'+p)
 rows.append(dict(path=p,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),record=old[p]))
report=dict(old=OLD,new=NEW,old_count=len(old),new_count=len(new),deleted_count=len(deleted),added_count=len(added),
 changed_survivors=[p for p in old.keys() & new.keys() if old[p]!=new[p]],
 deleted_sealed=dict(collections.Counter(str(old[p].get('sealed')) for p in deleted)),
 deleted_class=dict(collections.Counter(old[p].get('execution_class') for p in deleted)),
 deleted_evidence=dict(collections.Counter(old[p].get('evidence') for p in deleted)),
 deletion_commits=git('log','--format=%H %s','--diff-filter=D',OLD+'..'+NEW,'--',PREFIX).decode('utf-8'),
 deleted=rows,added=added)
(HERE/'registry-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('deleted','added')},ensure_ascii=True,indent=2))
