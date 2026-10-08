"""Read-only dependency origins and AST checks; no candidate/harness imports."""
import sys,ast,types,json,hashlib,time,traceback,copy,builtins,os,csv,io,base64,math,decimal
from pathlib import Path
root=Path(__file__).resolve().parents[1]
parsed=[]
for p in (root/'harness').glob('*.py'):
 ast.parse(p.read_text(encoding='utf-8-sig'));parsed.append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
entries=[]
for name,module in sorted(sys.modules.copy().items()):
 if module is None:continue
 spec=getattr(module,'__spec__',None);origin=getattr(spec,'origin',None)
 file=getattr(module,'__file__',None)
 if file and Path(file).is_file():
  raw=Path(file).read_bytes();entries.append({'module':name,'origin':str(Path(file).resolve()),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
 else:entries.append({'module':name,'origin':origin,'file':None,'kind':'built-in/frozen/namespace/no-file'})
path=root/'DEPENDENCY_ORIGINS.json'
if path.exists():raise RuntimeError('NO_OVERWRITE')
path.write_text(json.dumps({'candidate_imports':0,'candidate_calls':0,'harness_imports':0,'module_origins':entries,'own_harness_AST':parsed},indent=2),encoding='utf-8')
print(json.dumps({'stdlib_origin_records':len(entries),'harness_AST_count':len(parsed),'candidate_calls':0}))
