"""Package review evidence only; read-only target Git/files."""
import datetime,hashlib,json,pathlib,subprocess,zipfile
HERE=pathlib.Path(__file__).resolve().parent
WORK=HERE.parents[1];REPO=WORK/'work/gate66-head';SUB=REPO/'degradation-degeneracy'
HEAD='fa947cc9b17cdbeffbb39447c99159bc2c831e6e'
def git(*args):return subprocess.check_output(['git','-C',str(REPO),*args]).decode('utf-8').strip()
assert git('rev-parse','HEAD')==HEAD
status=git('status','--porcelain')
assert not status,status
scopes=['src','tools','configs','scripts','run.sh','requirements*.txt']
science_log=git('log','--oneline','743f65bead671bf353ce38027c2e8e457738ec08..HEAD','--',*['degradation-degeneracy/'+s for s in scopes])
assert not science_log,science_log
selected=['docs/22p_gap/GATE66_REQUEST.md','docs/08_REVIEW_RESPONSE.md','docs/GATE65_WORKING_STATE.md',
 'docs/22p_gap/mutation_replay.py','tests/test_gate65_defensive.py','tests/interpreter_fixture.py',
 'tests/test_gate64_defensive.py','tests/test_gate63_defensive.py','tests/receipt_fixture.py',
 'tests/conftest.py','src/io.py','src/fitting.py']
rows=[]
for rel in selected:
 data=(SUB/rel).read_bytes()
 rows.append(dict(path='degradation-degeneracy/'+rel,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),git_blob=git('rev-parse',HEAD+':degradation-degeneracy/'+rel)))
identity=dict(verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),head=HEAD,previous_review='5e4cf1038f0f26a6a624d9984386cfd046657ac3',
 scientific_reference='743f65bead671bf353ce38027c2e8e457738ec08',source_digest_observed='e9ee7475dea7de1d',
 source_digest_command_record='identity.json',source_digest_raw_stdout='identity.stdout.bin',
 final_status_porcelain=status,scientific_scope_log=science_log,reviewed_files=rows,
 target_changes_by_reviewer='none; sandbox copies only',registry_change_detection='read-only Git objects')
(HERE/'TARGET_IDENTITY.json').write_text(json.dumps(identity,ensure_ascii=False,indent=2),encoding='utf-8')
files=[]
for p in HERE.iterdir():
 if p.is_file() and p.name!='MANIFEST.json' and p.suffix in ('.py','.md','.json','.xml','.bin'):files.append(p)
for name in ('old-real-entry','startup_cases','startup_fullsandbox','partial_mutations'):
 for p in (HERE/name).rglob('*'):
  if p.is_file() and '__pycache__' not in p.parts and p.suffix in ('.py','.md','.json','.xml','.bin'):
   files.append(p)
files=sorted(set(files),key=lambda p:p.relative_to(HERE).as_posix())
manifest=[]
for p in files:
 data=p.read_bytes();manifest.append(dict(path=p.relative_to(HERE).as_posix(),bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
mp=HERE/'MANIFEST.json'
mp.write_text(json.dumps(dict(schema='review_payload_manifest_v1',files=manifest),ensure_ascii=False,indent=2),encoding='utf-8')
zpath=HERE.parent/'GATE66_REVIEW_20260922.zip'
assert not zpath.exists(),zpath
with zipfile.ZipFile(zpath,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in files+[mp]:z.write(p,p.relative_to(HERE).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert len(z.namelist())==len(set(z.namelist()))==len(files)+1
 assert len({n.casefold() for n in z.namelist()})==len(files)+1
 assert set(z.namelist())=={v['path'] for v in manifest}|{'MANIFEST.json'}
 assert z.testzip() is None
 for v in manifest:
  data=z.read(v['path']);assert len(data)==v['bytes'] and hashlib.sha256(data).hexdigest()==v['sha256']
receipt=dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),zip=str(zpath),bytes=zpath.stat().st_size,
 sha256=hashlib.sha256(zpath.read_bytes()).hexdigest(),payload_count=len(files),entries=len(files)+1,
 manifest_sha256=hashlib.sha256(mp.read_bytes()).hexdigest(),exact_set_size_sha_crc_verified=True,
 recipient_verification=None,scope='Gate66 review evidence; no production fixes or science runs')
(HERE.parent/'GATE66_REVIEW_20260922_RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=True,indent=2))
