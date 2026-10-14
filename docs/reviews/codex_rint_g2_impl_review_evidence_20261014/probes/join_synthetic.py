"""Small actual-function join/plan precision and trust-boundary probes."""
from pathlib import Path
import contextlib
import copy
import io
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'source/scripts'))
import numpy as np
import rint_iface_join as J
import lhs_descriptor_harvest as H
import step3_sigma as S3
from lens_geometry import intersection_disc_area

TMP = ROOT / 'tmp/join_synthetic'
TMP.mkdir(parents=True, exist_ok=True)
RT = {'AM_P|AM_P': 0.001}
LAW = dict(gap_law='cut', unreg_law='cut', ambiguous_arm='cut')

def dataset(tag, *, distance=0.0015, area=None, badpos=None, baddelta=None, radius=0.001, different_tilt=False):
    c = np.array([[0.002, 0.002, 0.002], [0.002 + distance, 0.002, 0.002]])
    r = np.array([radius, radius])
    delta = radius * 2 - distance
    exact_area = intersection_disc_area(radius, radius, delta)
    area = exact_area if area is None else area
    fmt = lambda x: f'{float(x):.15e}'
    box = ['ITEM: BOX BOUNDS ff ff ff', '0 0.01', '0 0.01', '0 0.01']
    at = ['ITEM: TIMESTEP', '100', 'ITEM: NUMBER OF ATOMS', '2'] + box + ['ITEM: ATOMS id type x y z radius']
    at += [f'{i+1} 1 ' + ' '.join(fmt(v) for v in [*c[i], r[i]]) for i in range(2)]
    tokens = [*map(fmt, c[0]), *map(fmt, c[1]), '1', '2', '0'] + ['0'] * 12 + [fmt(area), fmt(delta)]
    if badpos is not None:
        tokens[0] = badpos
    if baddelta is not None:
        tokens[22] = baddelta
    ct = ['ITEM: TIMESTEP', '100', 'ITEM: NUMBER OF ENTRIES', '1'] + box + ['ITEM: ENTRIES ' + ' '.join(f'c_cpl[{i}]' for i in range(1, 24)), ' '.join(tokens)]
    if different_tilt:
        for lines, tilt in [(at, '0.001'), (ct, '0.002')]:
            lines[4] = 'ITEM: BOX BOUNDS xy xz yz ff ff ff'
            lines[5] += ' ' + tilt
            lines[6] += ' 0'
            lines[7] += ' 0'
    sc = [','.join(['1', *(f'{x:.12f}' for x in [*c[i], r[i]])]) for i in range(2)]
    files = []
    for suffix, lines in [('sc.csv', sc), ('atom.dump', at), ('contact.dump', ct)]:
        p = TMP / f'{tag}_{suffix}'
        p.write_text('\n'.join(lines) + '\n', encoding='utf-8')
        files.append(p)
    j = J.am_iface_join(*files, type_map={1: 'AM_P'})
    return j, exact_area

def compact(j):
    return {'status': j['status'], 'rejections': j['rejections'], 'g_geo': j['g_geo'], 'g_frame': j['g_frame']}

base, exact = dataset('baseline')
c, r, t = (base['particles'][k] for k in ('c_um', 'r_um', 't'))
with contextlib.redirect_stdout(io.StringIO()):
    sid, pid = S3.rasterize(c, r, t, None, None, (0, 0, 0), (6, 4, 4), 0.25, bridge_um=0.24)
L = S3.am_iface_ledger(c, r, t, sid, sid, (0, 0, 0), 0.25, delta_bound_um=base['g_geo']['delta_bound_um'], bridge_um=0.24)
result = {'baseline': compact(base), 'exact_area_sim2': exact}
for tag, kwargs in [('negative_area', {'area': -exact}), ('nan_area', {'area': np.nan}),
                    ('nan_position', {'badpos': 'nan'}), ('nan_delta', {'baddelta': 'nan'}),
                    ('16sig_area_plus_1ppm', {'area': exact * (1 + 1e-6)}),
                    ('different_tilt_boxes', {'different_tilt': True})]:
    j, _ = dataset(tag, **kwargs)
    p = S3.am_iface_plan(L, RT, join=j, **LAW)
    try:
        S3.iface_require_quantitative(p, sid=sid)
        accepted = True
    except Exception as exc:
        accepted = type(exc).__name__ + ': ' + str(exc)
    result[tag] = dict(compact(j), plan_join_status=p['record']['iface_join']['status'],
                       plan_rejections=p['rejections'], require_quantitative=accepted,
                       area_sim2=j['dem_am_am']['area_um2'].tolist()[0] / 1e6)
    print(tag, j['status'], 'plan', accepted, flush=True)
lo, hi, _, _ = H._area_enclosure([0.001], [0.001], [0.0005], sig=16)
E, uncert = H._producer_error_bound([0.001], [0.001], [0.0005])
result['16sig_enclosure'] = {'lo': lo.item(), 'hi': hi.item(), 'producer_E_using_wider_6sig_box': E.item(),
                            'mutated_area': exact * (1+1e-6),
                            'lower_mutated_token_end': exact * (1+1e-6)-5e-22,
                            'accepted_area_outside_16sig_even_with_6sig_E': bool(exact * (1+1e-6)-5e-22 > hi.item()+E.item())}

jn, exact_near = dataset('uncertified_near_concentric', distance=1e-9, area=100)
result['uncertified_near_concentric'] = dict(compact(jn), exact_area=exact_near, supplied_area=100)
print('uncertified_near_concentric', jn['status'], jn['g_geo']['n_area_uncertified'], flush=True)

# Document trust boundary rather than calling it cryptographic authentication:
# a public rehash can intentionally rewrite status, and inner identity is not rebuilt.
fake = copy.deepcopy(base)
fake['particles']['c_um'] += 100
fake['fp_join'] = S3.iface_join_fp(fake)
p = S3.am_iface_plan(L, RT, join=fake, **LAW)
result['rehashed_inconsistent_particles'] = {'join_particles_fp_actual': S3._iface_particles_fp(fake['particles']['c_um'], fake['particles']['r_um'], fake['particles']['t']),
                                            'join_particles_fp_declared': fake['fp_particles'],
                                            'plan_join_status': p['record']['iface_join']['status'], 'plan_rejections': p['rejections']}

out = ROOT / 'evidence/join_synthetic.json'
out.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=True), encoding='utf-8')
print(out, flush=True)
