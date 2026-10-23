#!/usr/bin/env python3
"""Independent arithmetic/source audit; reads repo/request, writes only --out."""
import argparse, ast, hashlib, json, math, re, subprocess, sys
from pathlib import Path
from fractions import Fraction

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True, type=Path)
    ap.add_argument('--request', required=True, type=Path)
    ap.add_argument('--out', required=True, type=Path)
    args = ap.parse_args()
    repo = args.repo.resolve()
    def git(*xs):
        return subprocess.check_output(['git', '-C', str(repo), *xs])
    pin='7799a2ff64ba462b42ce05edd3e63b7c2854d557'
    old='9dc235c38f6347c1d94febc598b1d93ee2ffef68'
    new='aaa275e2081ce43a6892c7dde40ea4d8f82576de'
    planpath='docs/reviews/dem_protocol_gen2_plan_draft_20261014.md'
    plan=(repo/planpath).read_text()
    checks=[]
    def check(name, condition, **details):
        checks.append(dict(name=name, pass_=bool(condition), **details))
        if not condition:
            raise AssertionError(name)
    recovery=[100*(1-(1-.115)/(1+r)-.115) for r in [.016,.07]]
    check('recovery_porosity', all(abs(a-b)<1e-7 for a,b in zip(recovery,[1.3937008,5.7897196])), delta_percentage_points=recovery)
    boundary=.1/(1.64*math.pi*.5**2)*10
    rho_min=.0999/(math.pi*.5**2*.078)
    rho_max=.1001/(math.pi*.5**2*.076)
    check('density_threshold', abs(boundary-.7763656)<1e-7 and rho_min<1.64<rho_max, boundary_mm=boundary, interval_g_cm3=[rho_min,rho_max], diameter_exact_mm=10)
    exact_true=sum(Fraction(math.comb(100,k),2**100) for k in range(45,56))
    estimated=sum(Fraction(math.comb(100,k),2**100) for k in range(46,55))
    any_fail=1-exact_true**3
    check('MC_true_SE_A3', abs(float(exact_true)-.72874698)<1e-8 and abs(float(any_fail)-.6130)<5e-5, coverage=float(exact_true), at_least_one_failure_three_independent=float(any_fail))
    check('MC_actual_plugin_SE', float(estimated)<float(exact_true), coverage=float(estimated), failure=1-float(estimated), accepted_binomial_counts=list(range(46,55)), reported_se_at_zero_count=0, rare_p_001_zero_count_probability=.99**100)
    ratios=[b/a for a,b in zip([1.35,2,3,4.5],[2,3,4.5,6.75])]
    check('E_ladder_not_exact_geometric', ratios[0]!=ratios[1] and ratios[1:]==[1.5]*3, ratios=ratios)
    alphas=[K*30*.01*.005/750 for K in [1e6,1.1e6]]
    check('control_dimensions_and_counterexample', alphas==[2,2.2], a=alphas, eigenvalues=[1-a for a in alphas], units='K=N/deck_m, vmax=deck_m/deck_s, period=deck_s, F=deck_N')
    # Positive thickness recovery alone does not fix geometric union-density ordering.
    sphere_before=.9; sphere_after=.9/1.02
    union_before=.85; union_after=.89/1.02
    check('X4_union_density_order_not_universal', sphere_after<sphere_before and union_after>union_before, h_ratio=1.02, conserved_sphere_volume=.9, sphere_D=[sphere_before,sphere_after], union_D=[union_before,union_after], description='kinematic admissibility counterexample only, not a demonstrated LIGGGHTS trajectory')
    overlap=math.pi*1**2*(6*1-1)/12
    box=3*2*2
    check('two_spheres_analytic', abs(100*overlap/box-10.9083078)<1e-7, radius=1, center_distance=1, box=[3,2,2], centers=[[1,1,1],[2,1,1]], delta_percentage_points=100*overlap/box, boundary='nonperiodic for this analytic witness')
    one=100*(4/3*math.pi*4.5**3)/(50*50*111.052)
    equal_count_replacement=100*(4/3*math.pi*(4.5**3-.5**3))/(50*50*111.052)
    check('mass_conservation_counterexample', abs(one-.1374864)<1e-7, one_AM_loss_pp=one, fifty_AM_loss_pp=50*one, one_AM_replaced_by_SE_equal_count_pp=equal_count_replacement)
    # A regular sampler can miss an oscillation completely.
    samples=[750+20*math.sin(2*math.pi*n) for n in range(21)]
    check('sample_aliasing', max(abs(x-750) for x in samples)<1e-10, sampled_max_error_N=max(abs(x-750) for x in samples), continuous_max_error_N=20, fractional_max=20/750, period_deck_s=.005)
    check('rotation_and_residual_cancellation', .5*.4*1**2>0 and sum([10,-10])==0, Ktrans=0, Krot=.2, net_force=0, sum_force_norms=20)
    check('parameter_identifiability', abs(2**.8*.25**.4-1)<1e-15, E_multiplier=2, V_multiplier=.25, stiffness_multiplier=2**.8*.25**.4)
    source_paths=[
      'docs/handoff_codex_nonrint_20261023.md', planpath,
      'docs/reviews/findings.json','docs/reviews/claims.json',
      'docs/reviews/codex_review_model_validation_20261008.md',
      'docs/reviews/codex_model_validation_review_evidence_20261008/_README_reproduction.md',
      'docs/reviews/codex_model_validation_review_evidence_20261008/probes/mv_pressure_arithmetic.py',
      'docs/data/ps73_damping_branch_20261007/README.md',
      'docs/data/ps73_damping_branch_20261007/in.branch_B.liggghts',
      'docs/data/ps73_damping_branch_20261007/make_branch_decks.py',
      'docs/reviews/dem_unloading_ps45_prereg_20261009.md',
      'docs/data/ps45_unload_20261009/README.md',
      'docs/data/ps45_unload_20261009/unload_params.json',
      'docs/reviews/codex_review_dem_unloading_kit_20261014.md',
      'docs/reviews/dem_unloading_kit_fix_plan_20261014.md',
      'docs/dem_governing_equations_background_20261011.md',
      'docs/dem_governing_equations_report_20261009.md',
      'dem_scripts/ps_sweep_6mah_20260914/in.ps_7_3_r45.liggghts',
      'scripts/make_heckel_inputs.py','docs/data/heckel_pure_se_dem.csv',
      'docs/esse_calibration_2mAh_real_9.md','docs/data/esse_calibration_2mAh_real_9.csv']
    sources=[]
    for p in source_paths:
        data=(repo/p).read_bytes(); baseline=git('show',f'{pin}:{p}')
        sources.append(dict(path=p,sha256=hashlib.sha256(data).hexdigest(),same_as_pin=data==baseline))
    check('sources_22_pin_identity', len(sources)==22 and all(s['same_as_pin'] for s in sources), count=len(sources))
    tree=ast.parse((repo/'scripts/run_network_194_parallel.py').read_text())
    files=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CODE_FILES' for t in n.targets))
    different=[p for p in files if (repo/p).read_bytes()!=git('show',f'{pin}:{p}')]
    check('sealed_32_pin_identity',len(files)==32 and not different, count=len(files), different=different)
    section=plan.split('## 10.')[1].split('## 11.')[0]
    slugs=[]
    for line in section.splitlines():
        if line.startswith('| `'):
            slugs+=re.findall(r'`([A-Za-z0-9_]+)`',line.split('|')[1])
    slugs=sorted(set(slugs)); lit=[]
    for slug in slugs:
        p=f'litdb/papers/{slug}.md'
        a,b=git('show',f'{old}:{p}'),git('show',f'{new}:{p}')
        lit.append(dict(path=p,same=a==b,old_sha256=hashlib.sha256(a).hexdigest(),new_sha256=hashlib.sha256(b).hexdigest()))
    changed=[x['path'] for x in lit if not x['same']]
    check('literature_45_44_identity',len(lit)==45 and changed==['litdb/papers/sakuda2013_sulfide_mechanical_property.md'],count=len(lit),changed=changed)
    findings=json.loads((repo/'docs/reviews/findings.json').read_text())['findings']
    ids={f'MV-{x:02}' for x in range(1,10)}|{'DEMP-01','DEMP-02'}
    status={x['id']:x['status'] for x in findings if x['id'] in ids}
    check('eleven_findings_remain_open',len(status)==11 and set(status.values())=={'open'},status=status)
    out=dict(schema='independent_dem_gen2_preattack_v1',repo_head=git('rev-parse','HEAD').decode().strip(),python=sys.version,request_sha256=hashlib.sha256(args.request.read_bytes()).hexdigest(),checks=checks,source_files=sources,literature=lit,limitations=['No author CLAIM_AUDIT, probe, verification results or explanations read.','No DEM, LIGGGHTS, GPU, scheduler or external action.','No existing whole-repo gates repeated.','Analytic counterexamples do not establish magnitude in real beds.'])
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(checks=len(checks),passed=sum(x['pass_'] for x in checks),out=str(args.out)),ensure_ascii=False))
if __name__=='__main__': main()
