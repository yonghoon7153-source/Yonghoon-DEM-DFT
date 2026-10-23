from pathlib import Path
import hashlib,json,subprocess,difflib,re
R=Path('/workspace/.cloud-setup/nonrint-20261024');D=R/'dem-gen2-amendment/deliverables';E=D/'docs/reviews/dem_gen2_ratified_amendment_evidence_20261024';O=R/'audit/dem-ratification';B='962caea2d1857b0e34fe724e38815661936b7183';get=lambda p:subprocess.check_output(['git','show',B+':'+p],cwd='/workspace/Yonghoon-DEM-DFT');sha=lambda b:hashlib.sha256(b).hexdigest();checks=[]
def check(n,v,detail=None):checks.append({'name':n,'pass':bool(v),'detail':detail})
prov=json.loads((E/'source-provenance.json').read_text())
for x in prov:
 b=get(x['source']);check('pinned original '+x['copy'],x['pin']==B and b==(E/x['copy']).read_bytes() and sha(b)==x['sha256'])
plan=(D/'docs/reviews/dem_protocol_gen2_plan_draft_20261014.md').read_text();before=(E/'plan-before-20261024.md').read_text();difference=''.join(difflib.unified_diff(before.splitlines(True),plan.splitlines(True),fromfile='a/docs/reviews/dem_protocol_gen2_plan_draft_20261014.md',tofile='b/docs/reviews/dem_protocol_gen2_plan_draft_20261014.md'));check('actual baseline-to-current diff exact',difference==(E/'plan-before-to-ratified.diff').read_text())
a=json.loads((E/'prior-arithmetic-results.json').read_text());section=plan.split('## 12. 2026-10-24 비준 개정',1)[1]
for label,value in [('A1 low',a['springback'][0]['porosity_change_pp']),('A1 high',a['springback'][1]['porosity_change_pp']),('A2 point boundary',a['zero_porosity_thickness_mm_density_1_64'])]:check(label+' existing exact rounding',f'{value:.10f}' in section,f'{value:.10f}')
for i,x in enumerate(a['density_measurement_interval_counterexamples'][1]['apparent_density_interval_g_cm3']):check('A2 interval bound '+str(i),f'{x:.10f}' in section,f'{x:.10f}')
for key in ['exact_single_probe_coverage','exact_single_probe_false_failure_probability','exact_three_independent_probes_any_false_failure_probability']:check('A3 true-SE '+key,f"{a['MC_one_sigma_acceptance'][key]:.10f}" in section)
check('A3 no deterministic one-sigma rule','결정적 정답 판정으로 쓰지 않는다' in section and '구체 표본 수·coverage 수치·반복 수·seed 값·허용 실패확률·합격 폭' in section and '미정' in section)
check('A4 exact existing five inputs',a['E_ladder_GPa']==[1.35,2.0,3.0,4.5,6.75] and 'E_SE={1.35, 2.0, 3.0, 4.5, 6.75} GPa' in section and '2/1.35=1.481481' in section)
check('A5 existing analytical witness',[(x['K_N_per_m'],x['gain']) for x in a['discrete_linear_servo'][-2:]]==[(1000000.0,2.0),(1100000.0,2.2)] and 'K=1.0×10⁶ N/m이면 a=2' in section and 'K=1.1×10⁶이면 a=2.2' in section)
check('A5 qualification without invented values',all(s in section for s in ['강성·응답 지연·포화·부호·제어주기','비수렴/불안정 음성','새 값을 선택하지 않는다','실제 서보/R-a 또는 T12 완료로 승격하지 않는다']))
check('prior replay exactly equal JSON',json.loads((E/'arithmetic-replay.json').read_text())==a)
r=json.loads((E/'arithmetic-replay-receipt.json').read_text());check('recorded replay rc0 and same source only',r['exit_code']==0 and r['equal_to_original_json'] is True and '-I' in r['command'])
t=json.loads((E/'t12-preserved-files.json').read_text());check('T12 eight original package files preserved',len(t)==8 and all((D/x['path']).read_bytes()==(R/'dem-gen2/deliverables'/x['path']).read_bytes() and sha((D/x['path']).read_bytes())==x['sha256'] for x in t))
check('T12 explicitly not run and no physical readiness','T12=NOT_RUN·physical_ready=false' in section)
check('same user ratification not requested again','기존 Q1–Q16은 재선택하지 않는다' in plan and '같은 비준을 다시 요청하지 않는다' in (D/'docs/reviews/codex_dem_protocol_gen2_ratified_update_20261024.md').read_text())
check('new fullgate remains pending','PENDING' in (E/'full_gate_receipt.json').read_text())
check('current amendment section unique and references consistent',len(re.findall(r'^## 12\.',plan,re.M))==1 and '현재 해석은 §12를 우선' in plan and '§11 A' not in plan)
check('historical status and approval context explicit','10-14 당시 지위' in plan and '비준은 완료' in plan)
res={'status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','base':B,'plan_sha256':sha(plan.encode()),'checks':checks,'failures':[x for x in checks if not x['pass']],'scope':'Independent document/numeric source comparison only; no repeated arithmetic/MC experiment or physical/fullgate execution.'};(O/'result.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in res.items() if k!='checks'},ensure_ascii=False,indent=2));print('checks',len(checks))
