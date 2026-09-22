"""Package review-owned evidence, never the target or synthetic test scratch trees."""
import datetime, hashlib, json, pathlib, subprocess, sys, zipfile
import xml.etree.ElementTree as ET
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[1]/'work/r17-response-7c8f61f9/bms-balancing'
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
def dump(name,d): (HERE/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
tracked=['bms_balancing/model.py','bms_balancing/schema.py','bms_balancing/cycles.py','bms_balancing/verify.py',
         'scripts/gc_partial.py','scripts/width_report.py','scripts/verify_run_receipt.py','scripts/check_u14.py',
         'tests/test_r17_codex.py','tests/test_chain_rule_contract.py','tests/test_widths.py',
         'reviews/R17_RESPONSE.md','reviews/BML_R1_RESPONSE.md','reviews/evidence_gate.py',
         'reviews/r11_repros/replay_codex_r11.py']
source={p:dict(sha256=sha((ROOT/p).read_bytes()),git_blob=git('rev-parse','HEAD:./'+p)) for p in tracked}
dump('REVIEW_IDENTITY.json',dict(target=git('rev-parse','HEAD'),out_tree=git('rev-parse','HEAD:./out'),
     status_after=git('status','--porcelain'),source=source,python=sys.version,
     scope='read-only target review; synthetic fixtures; no real-data refit; no COMSOL; no production edits',
     recipient_attachment_sha256=sha(pathlib.Path('C:/Users/Administrator/.codex/attachments/5e1fe2a5-9651-46a3-be82-99f982192942/붙여넣은 텍스트.txt').read_bytes())))
for name in ('targeted','full'):
    p=HERE/(name+'.xml')
    if not p.exists():continue
    tree=ET.parse(p); cases=tree.findall('.//testcase'); failures=[]
    for c in cases:
        f=c.find('failure');e=c.find('error')
        f=f if f is not None else e
        if f is not None:
            msg=''.join(f.itertext())
            tags=[]
            for needle,tag in [('fcntl','fcntl'),('WinError 2','missing-executable-or-file'),('TimeoutExpired','timeout'),('PermissionError','permission'),('test_count','count-contract')]:
                if needle in msg:tags.append(tag)
            failures.append(dict(test=c.get('classname')+'::'+c.get('name'),message=f.get('message'),tags=tags,trace=msg))
    dump(name+'_failures.json',dict(suites=[s.attrib for s in tree.findall('.//testsuite')],cases=len(cases),failed=len(failures),failures=failures))
if '--inspect-only' in sys.argv:
    print('Identity and JUnit summaries written.');sys.exit(0)
selected=sorted(p for p in HERE.iterdir() if p.is_file() and p.suffix in ('.py','.md','.json','.log','.xml') and p.name not in ('DELIVERY_RECEIPT.json','PACKAGE_MANIFEST.json'))
manifest={p.name:dict(bytes=p.stat().st_size,sha256=sha(p.read_bytes())) for p in selected}
dump('PACKAGE_MANIFEST.json',manifest)
zpath=HERE/'R17_FOLLOWUP_REVIEW_PACKAGE.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
    for p in selected+[HERE/'PACKAGE_MANIFEST.json']:z.write(p,p.name)
with zipfile.ZipFile(zpath) as z:
    assert len(z.namelist())==len(set(z.namelist()))==len(selected)+1
    assert z.testzip() is None
    for n,r in manifest.items():
        b=z.read(n);assert len(b)==r['bytes'] and sha(b)==r['sha256']
receipt=dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),path=zpath.name,bytes=zpath.stat().st_size,
             sha256=sha(zpath.read_bytes()),payload_count=len(selected),manifest_sha256=sha((HERE/'PACKAGE_MANIFEST.json').read_bytes()),
             scope='Reviewer code, reports and execution evidence; excludes source checkout, scratch fixtures, real data and COMSOL',
             recipient_verification=None)
dump('DELIVERY_RECEIPT.json',receipt);print(json.dumps(receipt,ensure_ascii=False))
