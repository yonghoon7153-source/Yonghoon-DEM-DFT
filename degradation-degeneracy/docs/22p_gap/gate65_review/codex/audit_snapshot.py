from __future__ import annotations
import collections
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

OUT=Path(__file__).resolve().parent
REPO=OUT.parent.parent/'work/gate65-head'
DD=REPO/'degradation-degeneracy'
sys.path.insert(0,str(DD/'docs/22p_gap'))
import mutation_replay as mr

def git(*args):
    r=subprocess.run(['git',*args],cwd=REPO,capture_output=True,encoding='utf-8',errors='replace')
    return {'rc':r.returncode,'stdout':r.stdout,'stderr':r.stderr}

scope=['degradation-degeneracy/'+p for p in ['src','tools','configs','scripts','run.sh','requirements*.txt']]
files=['docs/22p_gap/mutation_replay.py','tests/test_gate63_defensive.py','tests/test_gate64_defensive.py',
       'tests/test_evidence_layer_58.py','tests/conftest.py','docs/22p_gap/GATE65_REQUEST.md',
       'docs/GATE64_WORKING_STATE.md','docs/08_REVIEW_RESPONSE.md']
recs=[json.loads(p.read_text(encoding='utf-8')) for p in (DD/'docs/22p_gap/_exec_class').glob('*.json')]
snap={'head':git('rev-parse','HEAD'), 'status':git('status','--porcelain'),
      'scientific_code':'743f65bead671bf353ce38027c2e8e457738ec08',
      'run_scope_log':git('log','--oneline','743f65bead671bf353ce38027c2e8e457738ec08..HEAD','--',*scope),
      'run_scope_diff':git('diff','743f65bead671bf353ce38027c2e8e457738ec08','HEAD','--',*scope),
      'files':{f:{'bytes':(DD/f).stat().st_size,'sha256':hashlib.sha256((DD/f).read_bytes()).hexdigest()} for f in files},
      'registry':{'root_json_count':len(recs),'by_evidence':dict(collections.Counter(r.get('evidence') for r in recs)),
                  'by_class':dict(collections.Counter(r.get('execution_class') for r in recs)),
                  'tracked_root_json':git('ls-files','degradation-degeneracy/docs/22p_gap/_exec_class/*.json')['stdout'].splitlines()},
      'mutation_counts':{'single':len(mr.MUTANTS),'multi':len(mr.MULTI),'expect':len(mr.EXPECT),'declared_masked':len(mr.DECLARED_MASKED)}}
(OUT/'FINAL_AUDIT.json').write_text(json.dumps(snap,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in snap.items() if k not in ('registry','files')},ensure_ascii=False,indent=2))
print('registry_count',len(recs))

# Recover the underlying collection error in binary mode, without changing policy/environment.
rlog=(OUT/'g64_replay.stdout.txt').read_text(encoding='utf-8')
sandbox=next(line[len('sandbox: '):] for line in rlog.splitlines() if line.startswith('sandbox: '))
argv=[sys.executable,'-m','pytest','tests/','-q','-k','a_child_with_user_site_disabled_matches_the_parent',
      '--collect-only','-p','no:randomly','--no-header']
r=subprocess.run(argv,cwd=sandbox,env=mr.replay_env(),capture_output=True,timeout=60)
(OUT/'collection_diagnostic.stdout.bin').write_bytes(r.stdout)
(OUT/'collection_diagnostic.stderr.bin').write_bytes(r.stderr)
encoding='cp949' if os.name=='nt' else 'utf-8'
report={'argv':argv,'cwd':sandbox,'rc':r.returncode,'decoding':encoding,
        'stdout':r.stdout.decode(encoding,errors='replace'),'stderr':r.stderr.decode(encoding,errors='replace')}
(OUT/'collection_diagnostic.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('collection_rc',r.returncode,report['stderr'][-2000:],report['stdout'][-2000:])
