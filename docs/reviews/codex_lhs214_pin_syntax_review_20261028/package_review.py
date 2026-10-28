from pathlib import Path
import zipfile,hashlib,json,shutil
R=Path(__file__).resolve().parent
OUT=Path(r'C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/outputs/lhs214_pin_syntax_review_20261028').resolve()
assert OUT.is_relative_to(Path(r'C:/Users/Administrator/Documents/Codex').resolve())
OUT.mkdir(parents=True,exist_ok=True)
dirs=['input','wsl','repo','before','wslpin','trees','context','independent','canonical_boundary_complete_env','canonical_boundary_run','canonical_boundary_workspace_tmp']
files=['README.md','codex_review_lhs214_pin_syntax_20261028.md','intake.json','remote_manifest.json','remote_extra_manifest.json','cache_verified.json','data_cache_verified.json','b7_to_35_identity.json','registration_pin_identity.json','runner_independent.diff','probe_receipts.py','probe_launch_contract.py','run_canonical_complete_env.py','audit_delivery.py','final_integrity.py','package_review.py']
chosen={}
for folder in dirs:
 for p in (R/folder).rglob('*'):
  if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc':
   assert not p.is_symlink() and p.resolve().is_relative_to(R.resolve())
   chosen[p.relative_to(R).as_posix()]=p
for f in files:
 p=R/f;assert p.is_file(),p;chosen[f]=p
names=list(chosen);assert len(names)==len({s.casefold() for s in names})
sha=lambda b:hashlib.sha256(b).hexdigest()
manifest=''.join(f'{sha(p.read_bytes())}  {name}\n' for name,p in sorted(chosen.items()))
(R/'MANIFEST.sha256').write_text(manifest,encoding='utf8',newline='\n')
zipout=OUT/'codex_lhs214_pin_syntax_review_20261028.zip'
with zipfile.ZipFile(zipout,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for name,p in sorted(chosen.items()):z.write(p,name)
 z.writestr('MANIFEST.sha256',manifest)
with zipfile.ZipFile(zipout) as z:
 assert z.testzip() is None
 assert len(z.namelist())==len(chosen)+1
 for name,p in chosen.items():assert z.read(name)==p.read_bytes(),name
 for ln in z.read('MANIFEST.sha256').decode().splitlines():
  h,name=ln.split('  ',1);assert sha(z.read(name))==h
report=OUT/'codex_review_lhs214_pin_syntax_20261028.md';shutil.copyfile(R/report.name,report)
receipt={'zip':zipout.name,'bytes':zipout.stat().st_size,'sha256':sha(zipout.read_bytes()),'entries':len(chosen)+1,'manifest_files':len(chosen),'zip_readback_all_hashes_match':True,'report':report.name,'report_sha256':sha(report.read_bytes()),'scope':'Review and local reproduction evidence only. No actual batch launch GO.'}
(OUT/'delivery_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
