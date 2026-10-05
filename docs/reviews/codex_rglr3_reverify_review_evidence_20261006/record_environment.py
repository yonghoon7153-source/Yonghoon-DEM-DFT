"""Record environment and cross-check evidence, without editing source or production."""
import sys,json,hashlib,platform,importlib
from pathlib import Path
R=Path(__file__).resolve().parent;W=R.parent;S=R/'source'
sys.path[:0]=[str(W/'lhs_coverage_review_20260930/deps'),str(W/'audit_review_evidence_20260909/pydeps'),str(S/'scripts'),str(S/'webapp')]
import tau_flux as TF,app
env=dict(platform=platform.platform(),python=sys.version,executable=sys.executable,modules={})
for n in ('numpy','scipy','pandas','flask'):
 m=importlib.import_module(n);env['modules'][n]=getattr(m,'__version__','see installed metadata')
(R/'environment.json').write_text(json.dumps(env,ensure_ascii=False,indent=2),encoding='utf8')
net=json.loads((R/'evidence/network_adversarial.json').read_text(encoding='utf8'))
rb=next(r for r in net if r['name']=='rollback_destination_failure')
rd=R/rb['path'];fm=json.loads((rd/'full_metrics.json').read_text(encoding='utf8'))
raw=TF.tau2_from_metrics(fm)[0];prob=app._network_generation_guard(str(rd),fm);guarded=TF.tau2_from_metrics(fm)[0]
assert raw==15.0710327185347 and guarded is None and prob
summary=dict(network_cases=len(net),all_cases_without_harness_error=not any(r.get('harness_error') for r in net),
 positive_statuses={r['name']:r['status'] for r in net[:3]},general_bad_statuses={r['name']:r['status'] for r in net if r['name'].startswith('general_')},
 rollback=dict(failure_kind=rb['attempt']['failure_kind'],kept=rb['attempt']['previous_generation_kept'],active=rb['status_view']['active_status'],
              raw_grade_tau2=raw,guarded_grade_tau2=guarded,tau_status=rb['tau']['ion_net_status_hertz'],problem=prob))
(R/'evidence/closure_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(summary,ensure_ascii=False,indent=2));print(json.dumps(env,ensure_ascii=False,indent=2))
