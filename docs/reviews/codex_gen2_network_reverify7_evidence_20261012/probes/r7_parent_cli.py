"""Reproduce all exact 25 registered mutations through actual parent/current CLI."""
from pathlib import Path
import contextlib,io,importlib.util,json,shutil,tempfile,copy
R=Path(__file__).resolve().parents[1];E=R/'evidence'
spec=importlib.util.spec_from_file_location('quality_exact',R/'probes/test_quality_probe.py')
q=importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):spec.loader.exec_module(q)
prior=json.loads((E/'r7_cli.json').read_text(encoding='utf8'))
T=Path(tempfile.mkdtemp(prefix='r7_parent_cli_',dir=R/'tmp'))
root=T/'consumer';shutil.copytree(prior['root'],root)
cases=[('positive',q.ns['base'])]
for group in ('V6','V6s'):cases.extend(q.ns[group].items())
rows=[]
normal=json.loads((E/'cli_positive.input.json').read_text(encoding='utf8'))
for name,doc in cases:
    record=copy.deepcopy(normal)
    record['reports']['case15_network']=doc['reports']['case15_network']
    record['timings']['case15_network']=doc['timings']['case15_network']
    record['checks']=[x for x in normal['checks'] if not x.get('id','').startswith('case15.')]+doc['checks']
    (root/'smoke_report.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8')
    row={'name':name}
    for label,mod in [('parent',q.parent),('current',q.current)]:
        output=E/f'cli25_{label}_{name}.json';cap=io.StringIO()
        with contextlib.redirect_stdout(cap):rc=mod.main(['--smoke-root',str(root),'--json',str(output)])
        d=json.loads(output.read_text(encoding='utf8'))
        assert len(d['meta'])==2,d['meta']
        row[label]={'rc':rc,'n_fail':d['n_fail'],'S0':d['meta'][0]['ok'],'S0b':d['meta'][1]['ok']}
        (E/f'cli25_{label}_{name}.log').write_text(cap.getvalue(),encoding='utf8')
    expected_parent=0 if name!='na_dup_row' else 1
    expected_current=0 if name=='positive' else 1
    for label,want in [('parent',expected_parent),('current',expected_current)]:
        assert row[label]==dict(rc=want,n_fail=want,S0=True,S0b=not bool(want)),row
    rows.append(row)
out={'root':str(root),'rows':rows,'all_expected':True,'mutants':len(rows)-1,
     'parent_accepts':sum(x['parent']['rc']==0 for x in rows[1:]),
     'current_accepts':sum(x['current']['rc']==0 for x in rows[1:])}
(E/'r7_parent_cli.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(out,ensure_ascii=False))
