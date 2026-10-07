"""Literal-only inactive Java variant writer. No Java/API/import/test execution."""
import pathlib,json,re,hashlib,difflib
R=pathlib.Path(__file__).resolve().parent
source=R/'reference/s0/candidate/MicroshortS1RestCandidate.java.inactive.txt'
raw=source.read_bytes();text=raw.decode('utf-8')
assert hashlib.sha256(raw).hexdigest()=='a90d1e66db796f6b8077fa1d158620d1ec548265a1508b698e35da8ef6e3492c'
policy=json.loads((R/'contracts/POLICY_VARIANTS.json').read_bytes())
out=R/'candidate/variants';out.mkdir(exist_ok=False)
oldcap=re.search(r'static final String MAXSTEP_S1="([^"]+)";',text).group(1)
oldreq=re.search(r'(m.study\("std1"\).feature\("time"\).set\("tlist",")([^"]+)("\);)',text).group(2)
records=[]
for v in policy['variants']:
    patches=[('T_END_SECONDS=3600.0;','T_END_SECONDS=120.0;'),('SIGMA_S1_S_M=1.7e-7;','SIGMA_S1_S_M=1.7e-6;'),
      ('static final String MAXSTEP_S1="'+oldcap+'";','static final String MAXSTEP_S1="'+v['maxstepexpressionbdf']+'";'),
      ('.set("tout","tlist");','.set("tout","'+v['tout']+'");'),
      ('.set("tlist","'+oldreq+'");','.set("tlist","'+' '.join(policy['request_vectors'][v['request_vector']]['tokens_s'])+'");'),
      ('INACTIVE_S1_PROPOSAL=uniform concentration rest 0..3600 s; one sigma per future approved run','INACTIVE_S1_PROPOSAL='+v['variant_id']+' uniform concentration rest 0..120 s; one sigma per future approved run')]
    current=text;applied=[]
    for before,after in patches:
        assert current.count(before)==1,(v['variant_id'],before[:60])
        if before!=after:
            current=current.replace(before,after,1);applied.append(dict(before=before,after=after))
    reverse=current
    for patch in reversed(applied):
        assert reverse.count(patch['after'])==1
        reverse=reverse.replace(patch['after'],patch['before'],1)
    assert reverse.encode('utf-8')==raw
    assert '.runAll(' not in current and 'denyS0Execution();' in current
    p=out/(v['variant_id']+'.java.inactive.txt');p.write_bytes(current.encode('utf-8'))
    diff=''.join(difflib.unified_diff(text.splitlines(True),current.splitlines(True),fromfile='S0_inactive',tofile=p.name))
    (out/(v['variant_id']+'.diff.txt')).write_text(diff,encoding='utf-8',newline='')
    records.append(dict(variant=v['variant_id'],path=str(p.relative_to(R)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),reverse_whole_bytes_equal=True,patches=applied))
(R/'VARIANT_STATIC_RESULT.json').write_text(json.dumps(dict(kind='INACTIVE_LITERAL_VARIANTS_NO_FUNCTIONAL_TEST',source_sha256=hashlib.sha256(raw).hexdigest(),variants=records,compile=0,JVM=0,COMSOL=0),indent=2),encoding='utf-8')
print(json.dumps(dict(variants=4,reverse_whole_bytes_equal=True,received_or_candidate_execution=0)))
