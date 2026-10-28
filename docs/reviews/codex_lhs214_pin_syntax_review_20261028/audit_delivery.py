from pathlib import Path
import sys,json,hashlib,re,datetime
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'repo/scripts'))
import run_network_194_parallel as N
import supp20_input_receipt as S
W=R/'wsl/lhs_preflight_35f032737_1028_173239';O=R/'independent'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
for ln in (W/'receipts_sha256.txt').read_text().splitlines():
 expected,old=ln.split(None,1);p=W/Path(old.strip()).name;checks.append({'file':p.name,'sha256':sha(p),'match':sha(p)==expected})
assert all(x['match'] for x in checks)
supp=S.receipt(preflight_receipt=str(O/'netsupp20_relocated.json'),approved_sha='35f0327377a4213774010a090df4d224e50d29e1')
assert supp['rc']==0,supp
(O/'supp20_reverified.json').write_text(json.dumps(supp,ensure_ascii=False,indent=2),encoding='utf8')
hand=json.loads(next(x.split('INPUT_DIGEST_JSON ',1)[1] for x in (W/'handcheck_194_lines.txt').read_text(encoding='utf8').splitlines() if 'INPUT_DIGEST_JSON ' in x))
pr=json.loads((O/'receipt_probe.json').read_text(encoding='utf8'))
dv=pr['normal']['production194']['recomputed']['input_digest'];assert hand==dv
base=R/'repo/docs/reviews/lhs_network_batch_registration_20261007_g2.md'
regtext=base.read_text(encoding='utf8');expected={
 'n':194,'missing_raw_sha':[],'ids_sha256':'a04282d7275bd8f92b0afb4ac8b045f72f3867ccebbb7813b530b3901fd7b3bf',
 'raw_sha256_table_sha256':'da7c93f9a0887145ff171e381c8608cb79779d96aea5a595a25677dc361ef784',
 'cohort_tsv_sha256':{'lhs':'32f00daa8394188d1e72531fd7fda1a8b47a9c279be76311ae7f2afa024b2809','lhsx':'0b85e8589917c9a3936ce29e9f36326993985ddd113ef32353a4ff96d981cb45'}}
assert hand==expected
for v in [expected['ids_sha256'],expected['raw_sha256_table_sha256'],*expected['cohort_tsv_sha256'].values(),N.code_fp(N.code_hashes())]:assert v in regtext,v
hashes=N.code_hashes();fp=N.code_fp(hashes)
inventory={p.relative_to(W).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p)} for p in W.iterdir() if p.is_file()}
env=(W/'env.txt').read_text(encoding='utf8').splitlines();same_env=env[0].split()[1:]==env[1].split()[1:]
summaries={fn:(W/fn).read_text(encoding='utf8').splitlines()[-1] for fn in ['fast16.log','real4.log','reread_selftest.log','runner_selftest.log','receipt_selftest.log']}
gate=json.loads((R/'repo/docs/reviews/lhs214_pin_syntax_fix_evidence_20261024/full_gate_receipt.json').read_text(encoding='utf8'))
out={'date':datetime.datetime.now().astimezone().isoformat(),'files':inventory,'receipt_hashes':checks,'env_normal_isolated_same':same_env,'sup20_checks':len(supp['checks']),'sup20_rc':supp['rc'],'production194_checks':len(pr['normal']['production194']['checks']),'handcheck_numbers_equal_registration_and_recomputed_plan':True,'manual_signoff_present':False,'separate_selftest_shell_exit_code_records_present':False,'sealed32':hashes,'code_fp':fp,'submitted_selftest_last_lines':summaries,'full_gate_historical_keys':list(gate)}
(O/'delivery_audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in out.items() if k not in ('files','sealed32')},ensure_ascii=False,indent=2))
