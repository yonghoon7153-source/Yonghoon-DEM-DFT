"""Read-only seminar p11 evidence check; stdlib, no producer imports or simulations."""
from pathlib import Path
import csv
import hashlib
import io
import json
import math
import re
import sys
import tarfile

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
B = ROOT / 'source/docs/data/ps73_damping_branch_20261007/ibb_20261009/B_20261009_101443.report.tgz'
R8 = ROOT / 'baseline/ps73_logs.tgz'
if not R8.exists():
    R8 = WORKSPACE / 'dem_unloading_kit_reverify_20261014/source/docs/data/ps73_compaction_curve_20261006/raw/ps73_logs.tgz'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def text(tf, name):
    f = tf.extractfile(name)
    assert f is not None, name
    return f.read().decode('utf-8')

def thermo_rows(log, step):
    rows = []
    for line in log.splitlines():
        p = line.split()
        if len(p) == 5 and p[0] == str(step):
            try:
                r = dict(step=int(p[0]), atoms=int(p[1]), ke_J=float(p[2]),
                         cpu_s=float(p[3]), pressure_deck_MPa=float(p[4]))
            except ValueError:
                continue
            r['pressure_physical_MPa'] = 1000*r['pressure_deck_MPa']
            rows.append(r)
    return rows

def mesh_z(tf, member):
    z = [float(m.group(1)) for m in re.finditer(
        r'^\s*vertex\s+\S+\s+\S+\s+(\S+)\s*$', text(tf, member), re.M)]
    assert len(z) == 6 and max(z)-min(z) == 0
    return {'vertices': len(z), 'z_deck_m': z[0], 'physical_um': z[0]*1000}

with tarfile.open(B, 'r:gz') as tf:
    prefix = 'B_20261009_101443/'
    names = tf.getnames()
    summary = dict(line.split('=', 1) for line in text(tf, prefix+'branch_summary.txt').splitlines() if '=' in line)
    trace = list(csv.DictReader(io.StringIO(text(tf, prefix+'branch_trace.csv'))))
    analysis = json.loads(text(tf, prefix+'analysis_branch.json'))
    log = text(tf, prefix+'log.liggghts')
    stop_rows = thermo_rows(log, 3125000)
    end_rows = thermo_rows(log, 3735000)
    stop = next(r for r in stop_rows if r['cpu_s'] > 0)
    end = next(r for r in end_rows if r['cpu_s'] > 0)
    stop_mesh = mesh_z(tf, prefix+'stop/mesh_3125000.stl')
    end_mesh = mesh_z(tf, prefix+'end/mesh_3735000.stl')

with tarfile.open(R8, 'r:gz') as tf:
    member = 'home/yonghoon/dem_test/ps45/logs/output_ps_7_3_r45_r8_220537.out'
    original = next(r for r in thermo_rows(text(tf, member), 3225000) if r['cpu_s'] > 0)

s, e = analysis['states']
checks = {
    'B_archive_receipt_sha': sha(B) == '9cb7100b5ce1da6e32bc87975af2dfc25ca6ff81804b05fdf0424b58b12f5db1',
    'normal_stop_rounds_to_slide': round(stop['pressure_physical_MPa'],1) == 300.9,
    'normal_end_rounds_to_slide': round(end['pressure_physical_MPa'],1) == 299.3,
    'original_relax_rounds_to_slide': round(original['pressure_physical_MPa'],1) == 165.3,
    'stop_mesh_rounds_to_slide': round(stop_mesh['physical_um'],2) == 111.05,
    'end_mesh_rounds_to_slide': round(end_mesh['physical_um'],2) == 105.84,
    'atom_loss_13_in_thermo': stop['atoms']-end['atoms'] == 13,
    'trace_129_rows': len(trace) == 129,
    'trace_hold_122_rows': sum(r['phase']=='hold' for r in trace) == 122,
    'analysis_pressure_matches_trace': abs(analysis['stop_press_MPa']-1000*float(next(r['press_deckMPa'] for r in trace if r['phase']=='stop'))) < 1e-10,
    'analysis_eps_rounds_to_slide': round(s['eps_sphere_pct'],2)==14.95 and round(e['eps_sphere_pct'],2)==10.77,
    'analysis_drag_rounds_to_slide': round(100*s['drag_N']/750,1)==57.9,
    'no_atom_dumps_in_report': not any('/atom_' in n for n in names),
}
for state in (s, e):
    calc = 100*(1-state['solid_volume_deck']/(state['box_x_deck']*state['box_y_deck']*state['plate_z_deck']))
    checks[f"analysis_{state['state']}_eps_arithmetic"] = abs(calc-state['eps_sphere_pct']) < 1e-10

out = {
    'scope': 'Archive reads and independent arithmetic only; no simulation or producer import',
    'archives': [{'path':str(p.resolve()), 'sha256':sha(p), 'bytes':p.stat().st_size} for p in (B,R8)],
    'thermo': {'B_stop_all_same_step_rows':stop_rows, 'B_end_all_same_step_rows':end_rows,
               'selected_regular_stop':stop, 'selected_regular_end':end, 'original_relax':original},
    'mesh': {'stop':stop_mesh, 'end':end_mesh},
    'derived_from_saved_analyzer_output_not_raw_atoms': {
        'stop_eps_pct':s['eps_sphere_pct'], 'end_eps_pct':e['eps_sphere_pct'],
        'stop_drag_N':s['drag_N'], 'drag_share_target_pct':100*s['drag_N']/750,
        'sphere_volume_loss_um3':(s['solid_volume_deck']-e['solid_volume_deck'])*1e9,
        'thirteen_SE_spheres_um3':13*4*math.pi*.5**3/3,
        'phase_counts_stop':s['n_by_type'], 'phase_counts_end':e['n_by_type'],
    },
    'arithmetic': {
        'delta_h_um':end_mesh['physical_um']-stop_mesh['physical_um'],
        'delta_eps_pp':e['eps_sphere_pct']-s['eps_sphere_pct'],
        'relaxation_pressure_drop_fraction_pct':100*(1-original['pressure_physical_MPa']/stop['pressure_physical_MPa']),
        'physical_target_force_N_for_50um_square':300e6*(50e-6)**2,
    },
    'checks': checks, 'all_checks_pass':all(checks.values()),
    'limits': ['Atom dumps are absent: drag/porosity phase sums cannot be reconstructed from individual velocities/radii.',
               'Numerical self-consistency does not certify equilibrium, conservation, or experimental validity.',
               'The original relaxed pressure belongs to the original path, not the B servo path.'],
}
result_text = json.dumps(out, ensure_ascii=False, indent=2)
if sys.argv[1:2] == ['--out']:
    Path(sys.argv[2]).write_text(result_text+'\n', encoding='utf-8')
print(result_text)
assert all(checks.values()), checks
