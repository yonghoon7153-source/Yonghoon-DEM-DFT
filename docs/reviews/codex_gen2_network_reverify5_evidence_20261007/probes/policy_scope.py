"""Read-only scope checks; never calls run_queue/cmd_run or any launcher."""
from pathlib import Path
import json,sys
R=Path(__file__).resolve().parents[1];sys.path[:0]=[str(R/'source/scripts')]
import run_network_194_parallel as rn
sets={n:rn.registered_id_set(n) for n in ('production194','pilot3')}
result={}
for name,s in sets.items():
    plan={'queue':[{'case':c,'cohort':h} for c,h in sorted(s['pairs'])]}
    result[name]=dict(n=len(s['pairs']),is_production=rn.production_plan(plan),flag_false=rn.production_observation_problem(dict(plan=plan,observe_imports=False)),flag_true=rn.production_observation_problem(dict(plan=plan,observe_imports=True)))
assert result['production194']['n']==194 and result['production194']['flag_false'] and not result['production194']['flag_true']
assert result['pilot3']['n']==3 and not result['pilot3']['is_production'] and not result['pilot3']['flag_false']
result['fork_census_pinned']=rn.fork_census(R/'source')
assert not result['fork_census_pinned']
(R/'evidence/policy_scope.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(result,ensure_ascii=False))
