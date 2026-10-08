"""Read-only CSV reconciliation and evaluation of a pinned porosity function.
No DEM, MPM, jobs, deck generation or calibration is performed.
"""
from pathlib import Path
import ast, csv, hashlib, json, math
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
csvpath = ROOT/'source/docs/data/esse_calibration_2mAh_real_9.csv'
rows = list(csv.DictReader(csvpath.open(encoding='utf-8-sig')))
out = {'source_sha256': hashlib.sha256(csvpath.read_bytes()).hexdigest(), 'SE_rows': []}
for r in rows:
    if not r['seed'].startswith('SE_only'): continue
    sphere, union = float(r['eps_sphere_pct']), float(r['eps_union_pct'])
    vs, vu = 1-sphere/100, 1-union/100
    out['SE_rows'].append(dict(seed=r['seed'], sphere_pct=sphere, pair_union_pct=union,
        apparent_void_difference_pp=union-sphere, implied_overlap_pct=(vs-vu)/vs*100,
        reported_overlap_pct=float(r['overlap_pct']), solid_volume_sphere_per_box=vs,
        solid_volume_pair_union_per_box=vu, effective_density_ratio_for_same_mass=vs/vu))
    assert abs((vs-vu)/vs*100-float(r['overlap_pct'])) < 0.01

# Evaluate precisely the pinned production function body, avoiding unrelated imports.
source = ROOT/'source/scripts/dem_analysis_core.py'
tree = ast.parse(source.read_text(encoding='utf-8'))
node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name=='calc_porosity_dual')
ns = {'np':np}
exec(compile(ast.Module(body=[node], type_ignores=[]),str(source),'exec'),ns)
# Deliberately strong-overlap geometry, to disprove an EXACT-union identity.
# Three collinear equal balls; outer-ball intersection is inside the middle ball.
atoms = {i:{'radius':1.0,'x':x,'y':2.0,'z':2.0} for i,x in enumerate([1.5,2.0,2.5],1)}
contacts = [{'id1':i,'id2':j,'delta':2-abs(atoms[i]['x']-atoms[j]['x'])}
    for i,j in [(1,2),(2,3),(1,3)]]
result = ns['calc_porosity_dual'](atoms, contacts, 4.0, 4.0, 4.0)
lens = lambda d: math.pi*(4+d)*(2-d)**2/12
true_union = 3*4*math.pi/3-2*lens(0.5)
true_void = 100*(1-true_union/64)
diff = result['porosity_union']-true_void
assert abs(diff-100*lens(1.0)/64) < 1e-12
out['three_ball_definition_counterexample'] = dict(function_lines=[node.lineno,node.end_lineno],
    pair_union_porosity_pct=result['porosity_union'], exact_union_porosity_pct=true_void,
    overstatement_pp=diff, omitted_triple_intersection_volume=lens(1.0),
    limitation='Definition counterexample only; not an estimate of error in the two SE beds. Raw SE dumps are unavailable.')
out['composite_mass_porosity_formula'] = 'epsilon = 1 - (m_total/A/h) * sum(w_i/rho_i); h=z_top-z_bottom'
out['units_note'] = 'Porosity differences are percentage points, overlap percentages use sphere-sum solid volume as denominator.'
target = ROOT/'evidence/mv_anchor_porosity_result.json'
target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(out,ensure_ascii=False,indent=2))
