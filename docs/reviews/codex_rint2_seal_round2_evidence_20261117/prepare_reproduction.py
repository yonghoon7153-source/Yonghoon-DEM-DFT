"""Prepare an offline, new-directory-only reproduction. Never runs review tests or an engine."""
import argparse, hashlib, json, os, shutil, subprocess, sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
PIN='64e4d213e8267bafaf3ae5af00a42996cefd3f33'
SEAL='c80d700bdd5915da82f77f839cb96ed4a5a6582e'
BUNDLE='input/extra/seal_candidate_v2_1/seal_form_G2_20261117.bundle'
SCRIPTS=['measurement_review/verify_measurements.py','measurement_review/verify_e4_baseline.py',
 'seal_form_review/scripts/audit_supplied_form.py','seal_form_review/scripts/audit_pin_boundary.py',
 'seal_form_review/scripts/probe_form_build.py','seal_form_review/scripts/probe_s0_gate.py','resume_review/review_resume.py']
SPARSE=['/scripts/','/docs/reviews/rint2_seal_20261120/','/docs/data/rint2_r_plan_20261120/',
 '/docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md','/docs/reviews/rint2_kgy_commands_20261020.md',
 '/docs/reviews/rint2_dev_probe_ledger_20261026.md','/docs/reviews/rint2_s0_store_probe_20261112/',
 '/docs/data/rint2_s0_sbe_20261116/','/docs/reviews/rint2_q14_finalpin_preparation_20261113/','/docs/reviews/claims.json']
ENV={k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_NO_LAZY_FETCH='1',GIT_OPTIONAL_LOCKS='0',GIT_TERMINAL_PROMPT='0',GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL=os.devnull)
def git(repo,*args):
    return subprocess.run(['git','-c','safe.directory='+str(repo).replace('\\','/'),'-c','protocol.allow=never',
      '-c','protocol.file.allow=always','-c','core.autocrlf=false','-C',str(repo),*args],env=ENV,capture_output=True,check=True).stdout
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--repo',required=True);ap.add_argument('--out',required=True)
    a=ap.parse_args();repo=Path(a.repo).resolve();out=Path(a.out).resolve()
    if out.exists():raise SystemExit('--out must not exist; choose a new directory.')
    if any(out==p or p in out.parents for p in (HERE,repo)):raise SystemExit('--out must be outside the evidence and source repository trees.')
    if not (HERE/BUNDLE).is_file():raise SystemExit('Attached bundle is missing.')
    for rel in SCRIPTS:
        if not (HERE/rel).is_file():raise SystemExit('Missing review script: '+rel)
    # Read only metadata and fixed historical objects from the supplied repository.
    for rev in (PIN,'6bf70fe4a','11a794674','b3481336c'):
        git(repo,'cat-file','-e',rev+'^{commit}')
    obj=Path(git(repo,'rev-parse','--git-path','objects').decode().strip())
    if not obj.is_absolute():obj=(repo/obj).resolve()
    out.mkdir(parents=True)
    shutil.copytree(HERE/'input',out/'input')
    # Preserve old evidence separately. Runnable directories initially contain only scripts.
    reference=out/'reference_evidence';reference.mkdir()
    for d in ('measurement_review','seal_form_review','resume_review'):
        for p in (HERE/d).rglob('*'):
            rel=p.relative_to(HERE/d)
            if any(x.startswith('work') or x in ('deps','baseline_1113','__pycache__') for x in rel.parts):continue
            if p.is_file() and p.suffix.lower() in ('.py','.md','.json','.txt'):
                dst=reference/d/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst)
    for p in HERE.iterdir():
        if p.is_file() and p.suffix.lower() in ('.json','.md','.py','.txt'):
            shutil.copy2(p,reference/p.name)
    for rel in SCRIPTS:
        p=out/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(HERE/rel,p)
    objects=out/'objects.git';objects.mkdir();git(objects,'init','--bare','-q')
    (objects/'objects/info/alternates').write_bytes((obj.as_posix()+'\n').encode('utf-8'))
    # The only fetch is from the attached local bundle into the new scratch bare repository.
    git(objects,'fetch','--no-tags','--no-write-fetch-head',str(out/BUNDLE),
        'refs/heads/seal-form-scratch:refs/heads/seal-form-scratch')
    assert git(objects,'rev-parse','refs/heads/seal-form-scratch').decode().strip()==SEAL
    candidate=out/'candidate_source';candidate.mkdir();git(candidate,'init','-q')
    (candidate/'.git/objects/info/alternates').write_bytes(((objects/'objects').as_posix()+'\n').encode('utf-8'))
    git(candidate,'config','core.sparseCheckout','true')
    (candidate/'.git/info/sparse-checkout').write_bytes(('\n'.join(SPARSE)+'\n').encode('utf-8'))
    git(candidate,'checkout','--detach','-q',SEAL)
    work=out/'seal_form_review/work';work.mkdir(parents=True)
    shutil.copytree(candidate/'scripts',work/'scripts')
    (out/'seal_form_review/logs').mkdir(exist_ok=True)
    identity={rel:{'source_sha256':sha(HERE/rel),'copy_sha256':sha(out/rel)} for rel in SCRIPTS}
    assert all(v['source_sha256']==v['copy_sha256'] for v in identity.values())
    result={'prepared_only':True,'source_repo_read_only':str(repo),'object_alternate_read_only':str(obj),
       'candidate':SEAL,'scripts_identity':identity,'python':sys.executable,
       'review_commands':[[sys.executable,'-I','-B','-X','utf8',str(out/r)] for r in SCRIPTS],
       'notes':['No tests or engine executed.','Global numpy/scipy must already be installed for this interpreter.',
                'Original logs preserved under reference_evidence; new tests write only in the new root.',
                'Keep source object store available; alternates are intentionally not a full repository archive.']}
    (out/'PREPARATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'prepared':str(out),'candidate':SEAL,'review_script_identity':'7/7 identical','tests_executed':0},ensure_ascii=False))
if __name__=='__main__':main()
