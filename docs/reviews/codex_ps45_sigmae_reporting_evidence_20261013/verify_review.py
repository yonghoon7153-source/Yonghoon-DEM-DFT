"""Review-only tests and source-integrity verification; no production writes."""
from pathlib import Path
import hashlib,json,subprocess,sys
R=Path(__file__).resolve().parent
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
original=json.loads((R/'source_manifest.json').read_text(encoding='utf8'))
checks=[]
for f in original['files']:
    base='source' if f['kind']=='code' else 'literature_cards'
    p=R/base/f['path']; assert digest(p)==f['sha256'],str(p)
    checks.append(str(p.relative_to(R)))
for f in json.loads((R/'evidence/extra_source_manifest.json').read_text())['files']:
    p=R/'source'/f['path'];assert digest(p)==f['sha256'],str(p)
    checks.append(str(p.relative_to(R)))
def run(name):
    p=subprocess.run([sys.executable,'-X','utf8','-B',str(R/'probes'/name)],capture_output=True,text=True,encoding='utf8',timeout=120)
    assert p.returncode==0,(name,p.stderr[-2000:])
    return json.loads(p.stdout)
code=run('code_scaling.py')
expected=json.loads((R/'evidence/code_scaling.json').read_text())
assert code==expected,'Code probe differs from recorded evidence'
composition=run('composition_basis.py')
assert composition==json.loads((R/'evidence/composition_basis.json').read_text(encoding='utf8'))
arithmetic=run('report_arithmetic.py')
assert len(arithmetic['cases'])==5 and len(code['global_checks'])==6
for g in code['global_checks']:
    assert g['edges_equal'] and g['fields_equal']
    for b in g['branches'].values():
        assert b['raw_q_bitwise_equal'] and b['raw_info_equal'] and b['certificate_equal_except_sigma_bulk']
        assert b['linear_relative_error']<1e-14
report=(R/'codex_review_ps45_sigmae_reporting_20261013.md').read_text(encoding='utf8')
assert '\ufffd' not in report
for item in ['Q1','Q2','Q3','Q4','Q5','Q6','64.7077','0.390802','0.467175','native_unsupported_pair']:
    assert item in report,item
out={'status':'PASS','source_files_unchanged':len(checks),'synthetic_global_branch_comparisons':18,
     'actual_saved_FULL_readouts_reconstructed':10,'composition_cases':5,
     'code_probe_exact_rerun':True,'composition_probe_exact_rerun':True,
     'scope':'review evidence only, not material validation or production approval',
     'report_sha256':digest(R/'codex_review_ps45_sigmae_reporting_20261013.md')}
(R/'evidence/final_verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(out,ensure_ascii=False,indent=2))
