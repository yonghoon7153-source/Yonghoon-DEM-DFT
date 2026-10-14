"""Package only this review and the current retained probe cases. No Git changes."""
from pathlib import Path
import hashlib, json, zipfile, tarfile, io
R=Path(__file__).resolve().parent
E=R/'evidence'
PIN='a30fe150e21f66aea2f1c360593e1cd781689b14'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
reader=json.loads((E/'reader_recheck.json').read_text(encoding='utf8'))
runner=json.loads((E/'runner_recheck.json').read_text(encoding='utf8'))
case_roots=[Path(reader['fixture_root']),Path(runner['run_dir'])]
cases=[]
for root in case_roots:
    root=root.resolve()
    assert root.is_relative_to(E.resolve()), root
    cases.extend(p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
case_manifest=[{'path':str(p.relative_to(R)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':sha(p)}
               for p in sorted(cases)]
case_archive=E/'_cases_20261014.tgz'
with tarfile.open(case_archive,'w:gz') as tf:
    data=json.dumps(case_manifest,ensure_ascii=False,indent=2).encode('utf8')
    info=tarfile.TarInfo('CASES_MANIFEST.json');info.size=len(data);info.mode=0o644
    tf.addfile(info,io.BytesIO(data))
    for p in sorted(cases):
        tf.add(p,arcname=str(p.relative_to(R)).replace('\\','/'),recursive=False)
with tarfile.open(case_archive,'r:gz') as tf:
    for m in tf:
        assert m.isfile() and not m.name.startswith('/') and '..' not in Path(m.name).parts
files=[]
for directory in ('source','upstream','submitted','notes','probes','legacy_probes'):
    files.extend(p for p in (R/directory).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
files.extend(p for p in E.iterdir() if p.is_file())
for name in ('codex_review_dem_unloading_kit_reverify_20261014.md','source_manifest.json',
             'upstream_manifest.json','run_baselines.py','run_legacy_probes.py','package_review.py'):
    files.append(R/name)
files=sorted(set(files))
old=R.parent/'dem_unloading_kit_review_20261014/source'
comparison=[p for p in (old/'docs/data/ps45_unload_20261009').rglob('*')
            if p.is_file() and '__pycache__' not in p.parts]
comparison.append(old/'docs/reviews/dem_unloading_ps45_prereg_20261009.md')
manifest={'review_pin':PIN,'native_simulation_executed':False,'target_code_modified':False,
          'case_files':len(cases),'files':[{'path':str(p.relative_to(R)).replace('\\','/'),
              'bytes':p.stat().st_size,'sha256':sha(p)} for p in files]}
manifest['files'].extend({'path':'comparison_base/'+str(p.relative_to(old)).replace('\\','/'),
                         'bytes':p.stat().st_size,'sha256':sha(p)} for p in comparison)
dest=R.parent/'codex_dem_unloading_kit_reverify_a30fe150e_20261014.zip'
assert not dest.exists(), 'Do not silently overwrite an existing delivered package'
with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    z.writestr('PACKAGE_MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2))
    for p in files: z.write(p,str(p.relative_to(R)).replace('\\','/'))
    for p in comparison: z.write(p,'comparison_base/'+str(p.relative_to(old)).replace('\\','/'))
with zipfile.ZipFile(dest) as z:
    assert z.testzip() is None
    for e in manifest['files']:
        assert hashlib.sha256(z.read(e['path'])).hexdigest()==e['sha256'],e['path']
receipt={'pin':PIN,'zip':str(dest),'bytes':dest.stat().st_size,'sha256':sha(dest),
         'entries':len(manifest['files'])+1,'case_files':len(cases),'case_archive_sha256':sha(case_archive),
         'report_sha256':sha(R/'codex_review_dem_unloading_kit_reverify_20261014.md')}
dest.with_suffix('.receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
