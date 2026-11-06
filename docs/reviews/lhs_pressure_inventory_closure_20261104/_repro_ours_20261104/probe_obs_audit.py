"""OBS-AUDIT-01 only: exact block from received probe, synthetic roots only.
No LPI full suite, slow-input probe, actual research host or production roots.
"""
import importlib.util, json, pathlib, sys, tempfile
from unittest import mock
D=pathlib.Path(sys.argv[1]).resolve()
results=[]
def record(name,ok,**kw):
    row=dict(name=name,passed=bool(ok),**kw)
    results.append(row)
    if not ok: raise AssertionError(row)
# Unchanged inventory called directly, as in historical audit test 17.
spec=importlib.util.spec_from_file_location('original_tests',D/'test_pressure_inventory.py');t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t);m=t.load_module()
with tempfile.TemporaryDirectory(prefix='lpi-ancestor-') as tmp:
 shared=pathlib.Path(tmp)/'shared';root=shared/'local';root.mkdir(parents=True)
 for _,case in m.plan('wsl'):
  d=root/case;d.mkdir();(d/'log.liggghts').write_text('');(d/'log.txt').write_text('')
 base=m.inventory('wsl',{'local':root});record('ancestor_baseline',base['rc']==0,inventory_rc=base['rc'],roots=base['roots'])
 original=m.os.open; injections=[]
 def injected(path,flags,*args,**kwargs):
  if path=='shared':
   before=shared.stat();sibling=shared/'unrelated-sibling';sibling.mkdir();sibling.rmdir();after=shared.stat()
   injections.append({'before':m.stamp(before),'after':m.stamp(after)})
  return original(path,flags,*args,**kwargs)
 with mock.patch.object(m.os,'open',side_effect=injected):report=m.inventory('wsl',{'local':root})
 record('ancestor_sibling_create_remove',len(injections)==1 and report['rc']==2 and report['roots']=={'local':'CHANGED'},inventory_rc=report['rc'],roots=report['roots'],counted_cases=report['counted_cases'],injections=injections,historical_cause_proven=False)

print(json.dumps({'python':sys.version,'scope':'Exact external ancestor baseline/injection block only; synthetic directories','checks':results,'historical_cause_proven':False},indent=2))
