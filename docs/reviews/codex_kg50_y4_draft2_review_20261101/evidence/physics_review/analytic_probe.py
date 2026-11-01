import json, math
from pathlib import Path

out = Path(__file__).resolve().parent
N = [168457, 22353, 7666]
drop = [144.43801, 20.44751, 9.25654]
rows = []
for name, n, dp in zip(['D1', 'D2', 'D3'], N, drop):
    affine = n * 1e-3
    alpha = math.sqrt(dp / (2 * affine))
    rows.append(dict(bed=name, N=n, drop_MPa=dp,
                     affine_drag_reference_MPa=affine,
                     ratio=dp/affine,
                     homogeneous_affine_elastic_drop_MPa=(2/3)*affine,
                     spring_counterexample_alpha=alpha,
                     spring_counterexample_k_top_over_bottom=alpha/(1-alpha),
                     reconstructed_drop_MPa=2*affine*alpha**2))

# SI-like deck to reported-pressure conversion used in submitted files.
# Registered R5 is unsigned; exact total drag uses the signed sum.
v = [-0.01, 0.01]
gamma = 0.5
signed = -gamma*sum(v)
absolute = gamma*sum(map(abs, v))

result = dict(
    kind='read-only algebra; no DEM or transport solve', rows=rows,
    unsigned_counterexample=dict(vz=v, gamma=gamma,
                                  signed_drag_N=signed,
                                  absolute_sum_N=absolute),
    sphere_loss=dict(number=5, r_um=0.5, volume_um3=5*(4/3)*math.pi*0.5**3,
                     porosity_percentage_point_change=100*5*(4/3)*math.pi*0.5**3/(50*50*122.596)),
    preregistration_note='182.4/24.2/8.32 MPa are drag-force equivalents, not preregistered relaxation-drop predictions.'
)
(out/'analytic_probe.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps(result, indent=2, ensure_ascii=False))
