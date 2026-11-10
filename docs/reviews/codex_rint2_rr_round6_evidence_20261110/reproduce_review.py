"""Reproduce only static/local-memory audits. No siteq/host/project CLI runs."""
import json, subprocess, sys
from pathlib import Path

root=Path(__file__).resolve().parent
repo=root/'package/repo'
out=root/'independent_replay'
out.mkdir(exist_ok=True)
commands=[
    ('remote_blobs',[str(root/'verify_remote_blobs.py')],0),
    ('codekey_sources',[str(root/'verify_codekey_sources.py')],0),
    ('document_compare',[str(root/'rr6_document_closure/document_compare.py'),'--repo',str(repo),
      '--prior-verdict',str(repo/'docs/reviews/codex_review_rint2_rr_round5_20261109.md'),
      '--out',str(out/'document_comparison.json')],0),
    ('siteq_predicates',[str(root/'rr6_siteq_semantics/probe_siteq_predicates.py'),str(repo)],0),
    ('siteq_evidence',[str(root/'rr6_siteq_evidence/audit_siteq_evidence.py'),'--package',str(root/'package'),
      '--code-scripts',str(root/'codekey_sources/scripts'),'--out',str(out/'siteq_evidence.json')],1),
]
results=[]
for name,args,expected in commands:
    argv=[sys.executable,'-I','-X','utf8','-B']+args
    p=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
    (out/(name+'.stdout.txt')).write_bytes(p.stdout)
    (out/(name+'.stderr.txt')).write_bytes(p.stderr)
    results.append({'name':name,'argv':argv,'rc':p.returncode,'expected_rc':expected,'matched':p.returncode==expected})
(out/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps([{'name':x['name'],'rc':x['rc'],'expected_rc':x['expected_rc'],'matched':x['matched']} for x in results],indent=2))
raise SystemExit(0 if all(x['matched'] for x in results) else 1)
