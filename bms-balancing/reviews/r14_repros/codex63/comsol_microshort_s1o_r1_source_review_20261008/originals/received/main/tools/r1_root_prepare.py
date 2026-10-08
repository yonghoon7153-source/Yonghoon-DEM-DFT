"""New R1 static data/copy tool. Never imports or calls a candidate."""
from pathlib import Path
import hashlib, json, zipfile, shutil, difflib, datetime, time

OUT = Path(__file__).resolve().parents[1]
BASE = OUT.parent / 'microshort_s1o_20261007_133011'
def digest(raw): return hashlib.sha256(raw).hexdigest()
def save(name, obj):
    p=OUT/name; p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

review=Path('C:/Users/BML/Desktop/COMSOL_MICROSHORT_S1O_PREPARATION_REVIEW_20261007 (1).zip')
raw=review.read_bytes()
assert len(raw)==805653 and digest(raw)=='dee50be8d7dd1bcfd14323878deaeda1d31729f4f850cda5d6158bf64dfda46f'
selected=['REVIEW_KO.md','DECISION.json','NEXT_SCOPE_DRAFT_KO.md','notes/EXECUTION_REVIEW.md','notes/PHYSICS_REVIEW.md','notes/POLICY_REVIEW.md']
with zipfile.ZipFile(review) as z:
    names=z.namelist()
    assert len(names)==len(set(names))==len({n.lower() for n in names})
    assert z.testzip() is None
    for n in names:
        assert not n.startswith(('/','\\')) and '..' not in n.replace('\\','/').split('/') and ':' not in n
        assert (z.getinfo(n).external_attr>>16)&0o170000 !=0o120000
    for n in selected:
        p=OUT/'reference'/'review'/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(n))
save('INPUT_IDENTITY.json',{'review_zip':{'path':str(review),'bytes':len(raw),'sha256':digest(raw),'crc_checked':True},'base_zip':{'path':str(BASE/'COMSOL_MICROSHORT_S1O_OFFLINE_PREPARATION_20261007.zip'),'sha256':digest((BASE/'COMSOL_MICROSHORT_S1O_OFFLINE_PREPARATION_20261007.zip').read_bytes())},'directive':{'path':'reference/R1_DIRECTIVE_v2_KO.md','sha256':digest((OUT/'reference/R1_DIRECTIVE_v2_KO.md').read_bytes())},'candidate_executed':False})

for p in (BASE/'reference').rglob('*'):
    if p.is_file():
        q=OUT/'reference'/p.relative_to(BASE/'reference');q.parent.mkdir(parents=True,exist_ok=True)
        assert not q.exists();shutil.copyfile(p,q)

p=OUT/'candidate/variants/P0.java.inactive.txt'
old=p.read_bytes(); needle=b'|strict|requested tlist storage|eventout|'
assert old.count(needle)==1
new=old.replace(needle,b'|strict|accepted tsteps storage|eventout|')
p.write_bytes(new)
assert new.replace(b'|strict|accepted tsteps storage|eventout|',needle)==old
reference=(OUT/'reference/s0/candidate/MicroshortS1RestCandidate.java.inactive.txt').read_bytes()
diff=''.join(difflib.unified_diff(reference.decode().splitlines(True),new.decode().splitlines(True),fromfile='reference/s0/candidate/MicroshortS1RestCandidate.java.inactive.txt',tofile='candidate/variants/P0.java.inactive.txt'))
(OUT/'candidate/variants/P0.diff.txt').write_text(diff,encoding='utf-8',newline='')
save('notes/N4_STATIC_CHANGE.json',{'finding':'S1O-N4','before_sha256':digest(old),'after_sha256':digest(new),'line':439,'before':'requested tlist storage','after':'accepted tsteps storage','reverse_exact_bytes':True,'setting_unchanged':'tout=tsteps','functional_validation':'NOT_RUN','java_compile':0})
print(json.dumps({'kind':'R1_ROOT_STATIC_PREPARE','candidate_executed':False,'review_crc':'PASS','N4_reverse_equal':True,'copied_reference_files':sum(1 for p in (BASE/'reference').rglob('*') if p.is_file())}))
