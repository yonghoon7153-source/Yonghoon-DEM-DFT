"""Receipt section parser probes on temporary document copies, not source edits."""
from pathlib import Path
import json,os,re,sys,tempfile
R=Path(__file__).resolve().parents[1];S=R/'source';O=R/'evidence/receipt_fences';O.mkdir(exist_ok=True)
sys.path[:0]=list(map(str,[S/'scripts',R.parent/'lhs_coverage_review_20260930/deps',R.parent/'gen2_network_reverify3_20261007/deps']))
os.environ.update(PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
import supp20_input_receipt as sr
t=(S/sr.REG_DOC).read_text(encoding='utf8');fp=sr.NP.code_fp(sr.NP.code_hashes())
no_pending=re.sub(r'`code_fp_pending [0-9a-f]{64}`','(pending removed in probe)',t)
# No real section 3 remains in either case. The only ##3 text occurs in a fenced example.
no_active=re.sub(r'^## 3\.', '## 30.',no_pending,flags=re.M)
examples={
 'four_backtick_nested_example':f'\n````markdown\n```python\n## 3. Example only\n`code_fp {fp}`\n```\n````\n',
 'three_backtick_plain_example':f'\n```markdown\n## 3. Example only\n`code_fp {fp}`\n```\n',
}
out={}
for name,extra in examples.items():
    p=O/f'{name}.md';p.write_text(no_active+extra,encoding='utf8')
    rec=sr.receipt(reg_doc=str(p));body,why=sr._md_section(no_active+extra,3)
    out[name]={'rc':rec['rc'],'bad':[c['id'] for c in rec['checks'] if not c['ok']],'section':body,'section_problem':why,'read_code_fp':rec['registration']['values']['code_fp']}
(O/'results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(out,ensure_ascii=False,indent=2))
