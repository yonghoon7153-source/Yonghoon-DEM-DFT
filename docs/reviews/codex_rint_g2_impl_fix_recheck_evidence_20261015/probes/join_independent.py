"""Independent join entrance, format and fail-closed consumer probes."""
from pathlib import Path
import contextlib
import copy
import gzip
import io
import json
import sys
import traceback
import warnings

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'source/scripts'))
import numpy as np
import rint_iface_join as J
import step3_sigma as S3
from lens_geometry import intersection_disc_area

TMP = ROOT / 'tmp/join_independent'
TMP.mkdir(parents=True, exist_ok=True)
result = {}
R = .001
exact = intersection_disc_area(R, R, .0005)
TM = {1: 'AM_P', 2: 'SE'}

def files(tag, *, distance=.0015, area=None, precision=6, edit=None, origin_x=.002):
    fmt = (lambda x: '%g' % x) if precision == 6 else (lambda x: '%.15e' % x)
    xyz = [[origin_x, .002, .002], [origin_x + distance, .002, .002]]
    delta = 2 * R - distance
    area = intersection_disc_area(R, R, delta) if area is None else area
    box = ['ITEM: BOX BOUNDS ff ff ff', '0 0.01', '0 0.01', '0 0.01']
    atom = ['ITEM: TIMESTEP', '100', 'ITEM: NUMBER OF ATOMS', '2'] + box + ['ITEM: ATOMS id type x y z radius']
    atom += [f'{i+1} 1 ' + ' '.join(fmt(v) for v in [*xyz[i], R]) for i in range(2)]
    tok = [*map(fmt, xyz[0]), *map(fmt, xyz[1]), '1', '2', '0'] + ['0'] * 12 + [fmt(area), fmt(delta)]
    contact = ['ITEM: TIMESTEP', '100', 'ITEM: NUMBER OF ENTRIES', '1'] + box + ['ITEM: ENTRIES ' + ' '.join(f'c_cpl[{i}]' for i in range(1, 24)), ' '.join(tok)]
    scaffold = [','.join(['1', *(f'{x:.12f}' for x in [*xyz[i], R])]) for i in range(2)]
    lines = [scaffold, atom, contact]
    if edit:
        edit(lines)
    paths = []
    for suffix, body in zip(('sc.csv', 'atom.dump', 'contact.dump'), lines):
        path = TMP / (tag + '_' + suffix)
        path.write_text('\n'.join(body) + '\n', encoding='utf-8')
        paths.append(path)
    return paths

def replace(lines, file_index, row, col, value, sep=' '):
    toks = lines[file_index][row].split(sep)
    toks[col] = value
    lines[file_index][row] = sep.join(toks)

def compact(join):
    return {k: join[k] for k in ('status', 'rejections', 'entrance', 'g_geo', 'g_frame', 'geom_reuse')}

def physical_schema(paths):
    out = {}
    for name, path, item in zip(('atom', 'contact'), paths[1:], ('ITEM: ATOMS', 'ITEM: ENTRIES')):
        lines = path.read_text(encoding='utf-8').splitlines()
        k = next(i for i, ln in enumerate(lines) if ln.startswith(item))
        header = lines[k][len(item):].split()
        rows = []
        for ln in lines[k+1:]:
            if ln.startswith('ITEM:'):
                break
            if ln.strip():
                rows.append(ln.split())
        out[name] = {'declared_count_line': lines[3], 'header_columns': len(header),
                     'duplicate_header_columns': sorted({s for s in header if header.count(s) > 1}),
                     'physical_nonempty_rows': len(rows), 'physical_row_widths': [len(row) for row in rows]}
    return out

def consume(join):
    plan = S3.am_iface_plan(ledger, {'AM_P|AM_P': .001}, join=join,
                          gap_law='cut', unreg_law='cut', ambiguous_arm='cut')
    out = {'plan_rejections': plan['rejections'], 'plan_join_status': plan['record']['iface_join']['status']}
    try:
        S3.iface_require_quantitative(plan, sid=sid, vox=.25)
        out['quantitative_guard'] = 'ACCEPT'
    except Exception as exc:
        out['quantitative_guard'] = type(exc).__name__ + ': ' + str(exc)
    return out

baseline_paths = files('baseline')
base = J.am_iface_join(*baseline_paths, type_map=TM)
c, r, t = (base['particles'][k] for k in ('c_um', 'r_um', 't'))
with contextlib.redirect_stdout(io.StringIO()):
    sid, pid = S3.rasterize(c, r, t, None, None, (0, 0, 0), (6, 4, 4), .25, bridge_um=.24)
ledger = S3.am_iface_ledger(c, r, t, sid, sid, (0, 0, 0), .25,
                          delta_bound_um=base['g_geo']['delta_bound_um'], bridge_um=.24)
result['baseline'] = dict(compact(base), **consume(base), exact_area_sim2=exact)

def probe(tag, *, kwargs=None, edit=None, join_kwargs=None):
    paths = files(tag, edit=edit, **(kwargs or {}))
    try:
        with warnings.catch_warnings(record=True) as ws:
            warnings.simplefilter('always')
            j = J.am_iface_join(*paths, type_map=TM, **(join_kwargs or {}))
        out = dict(compact(j), warnings=[str(w.message) for w in ws], physical_schema=physical_schema(paths))
        out['particles_finite'] = {'c_um': bool(np.isfinite(j['particles']['c_um']).all()),
                                   'r_um': bool(np.isfinite(j['particles']['r_um']).all())}
        out['particle_r_um_repr'] = [repr(float(v)) for v in j['particles']['r_um']]
        try:
            out.update(consume(j))
        except Exception as exc:
            out['consumer_exception'] = type(exc).__name__ + ': ' + str(exc)
    except Exception as exc:
        out = {'exception': type(exc).__name__, 'message': str(exc)}
    result[tag] = out
    print(tag, out.get('status', out.get('exception')), [x['code'] for x in out.get('rejections', [])], flush=True)

# Original mutations retained. The 16-digit area mutation stays uniformly 16-digit.
for tag, kwargs in [('negative_area', {'area': -exact}), ('nan_area', {'area': np.nan}),
                    ('inf_area', {'area': np.inf}), ('uniform_16sig_baseline', {'precision': 16}),
                    ('uniform_16sig_area_plus_1ppm', {'precision': 16, 'area': exact * (1 + 1e-6)}),
                    ('uncertified_100', {'distance': 1e-9, 'area': 100}),
                    ('uncertified_true_area', {'distance': 1e-9})]:
    probe(tag, kwargs=kwargs)
for tag, fi, row, col, value, sep in [
    ('nan_position', 2, 9, 0, 'nan', ' '), ('nan_delta', 2, 9, 22, 'nan', ' '),
    ('scaffold_nan', 0, 1, 4, 'nan', ','), ('scaffold_inf', 0, 1, 4, 'inf', ','),
    ('scaffold_float64_radius_overflow', 0, 1, 4, '1e309', ','),
    ('scaffold_fixed_decimal_radius_overflow', 0, 1, 4, '1' + '0' * 309 + '.000000000000', ','),
    ('scaffold_fixed_decimal_negative_radius_overflow', 0, 1, 4, '-1' + '0' * 309 + '.000000000000', ','),
    ('scaffold_float64_position_overflow', 0, 1, 1, '1e309', ','),
    ('scaffold_radius_zero', 0, 1, 4, '0', ','),
    ('atom_radius_zero', 1, 10, 5, '0', ' '), ('atom_radius_negative', 1, 10, 5, '-0.001', ' '),
    ('atom_id_fraction', 1, 9, 0, '1.1', ' '), ('atom_type_fraction', 1, 9, 1, '1.1', ' '),
    ('contact_id_fraction', 2, 9, 6, '1.1', ' '), ('scaffold_type_fraction', 0, 1, 0, '1.1', ','),
    ('atom_id_int64_overflow', 1, 9, 0, '9223372036854775808', ' '),
    ('atom_trailing_zero', 1, 9, 2, '0.0020', ' '), ('contact_trailing_zero', 2, 9, 0, '0.0020', ' '),
    ('contact_plus_sign', 2, 9, 0, '+0.002', ' '), ('contact_decimal_exponent', 2, 9, 0, '2e-03', ' '),
    ('contact_pos_one_token_ulp', 2, 9, 0, '0.00200001', ' '),
    ('contact_pos_two_token_ulp', 2, 9, 0, '0.00200002', ' '),
    ('contact_negative_nonAM_area', 2, 9, 21, '-1', ' '),
]:
    if tag == 'contact_negative_nonAM_area':
        continue
    probe(tag, edit=lambda lines, fi=fi, row=row, col=col, value=value, sep=sep: replace(lines, fi, row, col, value, sep))

def tilt(lines):
    for fi, value in ((1, '.001'), (2, '.002')):
        lines[fi][4] = 'ITEM: BOX BOUNDS xy xz yz ff ff ff'
        lines[fi][5] += ' ' + value
        lines[fi][6] += ' 0'
        lines[fi][7] += ' 0'
probe('different_tilt', edit=tilt)
for tag, fi, row, value in [('step_fraction', 2, 1, '100.1'), ('count_fraction', 2, 3, '1.1'),
                           ('step_extra_token', 2, 1, '100 0.9'), ('count_extra_token', 2, 3, '1 garbage'),
                           ('box_reversed', 2, 5, '0.01 0'), ('box_extra_token', 2, 5, '0 0.01 0'),
                           ('box_trailing_zero', 2, 5, '0 0.010')]:
    probe(tag, edit=lambda ls, fi=fi, row=row, value=value: ls[fi].__setitem__(row, value))

probe('malformed_extra_contact_row', edit=lambda ls: ls[2].append('0.002 0.002 nan malformed'))
probe('malformed_extra_atom_row', edit=lambda ls: ls[1].append('3 1 nan'))
probe('malformed_numeric_contact_row_inside_block', edit=lambda ls: ls[2].insert(9, ls[2][9] + ' 0'))
probe('malformed_numeric_atom_row_inside_block', edit=lambda ls: ls[1].insert(9, ls[1][9] + ' 0'))
probe('wellshaped_duplicate_contact_control', edit=lambda ls: ls[2].insert(9, ls[2][9]))
probe('wellshaped_duplicate_atom_control', edit=lambda ls: ls[1].insert(9, ls[1][9]))
def duplicate_header(lines):
    lines[1][8] += ' radius'
    lines[1][9] += ' nan'
    lines[1][10] += ' nan'
probe('duplicate_radius_column', edit=duplicate_header)

# Preserve the original 1e-9 separation while translating x to zero so %g does
# not collapse the two x tokens. The 100 sim^2 attack itself is unchanged.
probe('uncertified_100_translated', kwargs={'distance': 1e-9, 'area': 100, 'origin_x': 0.0})
probe('uncertified_true_translated', kwargs={'distance': 1e-9, 'origin_x': 0.0})

# Distinguish join false PASS from downstream finite-input defenses: no solver.
paths = files('overflow_ledger', edit=lambda ls: replace(ls, 0, 1, 4, '1' + '0' * 309 + '.000000000000', ','))
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    overflow_join = J.am_iface_join(*paths, type_map=TM)
try:
    S3.am_iface_ledger(*(overflow_join['particles'][k] for k in ('c_um', 'r_um', 't')),
                      sid, sid, (0, 0, 0), .25, delta_bound_um=overflow_join['g_geo']['delta_bound_um'], bridge_um=.24)
    result['overflow_matching_ledger'] = {'status': 'ACCEPT'}
except Exception as exc:
    result['overflow_matching_ledger'] = {'exception': type(exc).__name__, 'message': str(exc)}

def other_step(lines):
    lines[2][1] = '101'
for tag, reuse in [('d19_undeclared', None), ('d19_declared', {'atom_step': 100, 'contact_step': 101, 'reason': 'same geometry synthetic positive'}),
                   ('d19_wrong_declaration', {'atom_step': 100, 'contact_step': 102})]:
    probe(tag, edit=other_step, join_kwargs={'geom_reuse': reuse})
probe('d19_unneeded', join_kwargs={'geom_reuse': {'atom_step': 100, 'contact_step': 100}})

# Enumerate canonical six-digit area tokens near an exact finite test geometry.
result['area_token_sweep'] = []
for area in np.arange(137442, 137449, dtype=float) * 1e-11:
    paths = files('area_' + ('%g' % area), area=area)
    j = J.am_iface_join(*paths, type_map=TM)
    result['area_token_sweep'].append({'area_token': '%g' % area, 'status': j['status'],
                                       'codes': [x['code'] for x in j['rejections']]})

# Real normal second bed, including out-of-scope negative AM-SE area count.
D = ROOT / 'source/docs/data/case15_corner_20261001'
j = J.am_iface_join(D/'case15_am_scaffold.csv', D/'atom_v4_1710000.liggghts.gz',
                   D/'contact_v4_1710000.liggghts.gz', type_map=TM)
result['case15'] = compact(j)
aa = J.read_atom_dump_frame(D/'atom_v4_1710000.liggghts.gz')
cc = J.read_contact_dump_frame(D/'contact_v4_1710000.liggghts.gz')
type_by_id = dict(zip(aa['ids'].tolist(), aa['types'].tolist()))
result['case15_negative_area_rows'] = [
    {'zero_based_row': int(k), 'ids': [int(cc['id1'][k]), int(cc['id2'][k])],
     'types': [TM[type_by_id[int(cc['id1'][k])]], TM[type_by_id[int(cc['id2'][k])]]],
     'area_sim2': float(cc['area'][k])}
    for k in np.flatnonzero(cc['area'] < 0)]
print('case15', j['status'], j['g_geo']['n_dem_am_am'], j['g_geo']['n_area_negative_not_am_am'], flush=True)
(ROOT/'evidence/join_independent.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
