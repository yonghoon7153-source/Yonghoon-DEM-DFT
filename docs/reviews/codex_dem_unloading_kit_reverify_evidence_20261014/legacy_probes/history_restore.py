"""Independent restoration counterexamples, source left unchanged."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / 'source/docs/data/ps45_unload_20261009'
sys.path.insert(0, str(KIT))
import ul_lib as L
import ul_reader as R
sys.path.insert(0, str(KIT / 'history_test'))
import read_history as H
P = L.load_params()
BED = R.B73
OUT = ROOT / 'evidence/history_restore_probe'
OUT.mkdir(exist_ok=True)
J = OUT / BED / 'RJ'

def write(p, text):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')

B = P['beds'][BED]
g1, g3 = B['g1'].split(), B['g3'].split()
resets = ''.join(f'Resetting {k} state of Fix {f} Style {s} from restart file info\n'
                 for f, s, ks in R.EXPECTED_RESETS for k in ks)
head = 'Step Atoms KinEng ul_erot ul_Ps pressMPa CPU\n'
scr = ('LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, git commit 3d5c00f)\n' + resets + head +
       f'{g1[0]} {g1[1]} {g1[2]} 1e-08 {g1[4]} {g1[4]} 0\n' +
       'Loop time of 0 on 6 procs for 0 steps\n' + head +
       f'{g1[0]} {g1[1]} {g1[2]} 1e-08 {g1[4]} {g1[4]} 0\n' +
       f'{g3[0]} {g3[1]} {g3[2]} 1e-08 {g3[4]} {g3[4]} 1\n' +
       'Loop time of 1 on 6 procs for 2000 steps\nUL_R_DONE\n')
write(J / 'R/screen.txt', scr)
write(J / 'UN/screen.txt', scr.replace('UL_R_DONE', 'UL_UNREAD_DONE'))
write(J / 'UN/run_check.txt', 'UNread screen.txt PASS rc=0 procs=6\n')
write(OUT / BED / 'in' / B['orig_log'], scr)
write(J / 'g0.json', json.dumps({'status': 'PASS', 'violations': []}))
acols = ['id', 'type', 'x', 'y', 'z', 'radius', 'vx', 'vy', 'vz']
atoms = [dict(zip(acols, [i, 3, i*.001, .002, .003, .0005, 1e-6, 0, 0])) for i in range(1, 4)]
ccols = [f'c_cpl[{i}]' for i in range(1, 27)]
contact = dict(zip(ccols, [.001,.01,.01,.0015,.01,.01,1,2,0,-.5,0,0,-.5,0,0,0,.01,0,0,0,0,1e-8,1e-5,.00125,.01,.01]))
for base in (OUT / BED / 'in', J / 'R/g2'):
    base.mkdir(parents=True, exist_ok=True)
    L.write_custom(str(base / 'atom_3200000.liggghts'), 3200000, acols, atoms)
    L.write_local(str(base / 'contact_3200000.liggghts'), 3200000, ccols, [contact])
    write(base / 'mesh_3200000.stl', 'solid fixture\nendsolid fixture\n')
hc = ['id', 'type'] + [f'f_history_zwall_bot[{i}]' for i in range(1, 5)]
hist = [dict(zip(hc, [1,1,2e-5,1e-6,0,0])), dict(zip(hc, [2,3,0,0,0,0]))]
zero = [dict(zip(hc, [i,3,0,0,0,0])) for i in (1, 2)]
for rel, rows in [('R/obs/pre_bot.dump',hist), ('R/obs/post_atom_3200000.dump',hist),
                  ('R/obs/end_pre_bot.dump',hist), ('UN/obs/un_pre_bot.dump',zero)]:
    p = J / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    L.write_custom(str(p), 3200000, hc, rows)
good = json.loads((ROOT / 'evidence/history_reread.json').read_text(encoding='utf-8'))
report = {}

def check(name, hv):
    p = OUT / (name + '_history.json')
    write(p, json.dumps(hv, ensure_ascii=False, indent=2))
    v = R.restore_verdict(str(OUT), BED, 'RJ', str(p), P)
    write(J / 'restore_verdict.json', json.dumps(v, ensure_ascii=False))
    write(OUT / BED / 'ul_base.in', 'variable ul_s2lim equal 1.0\n')
    v['followup_UB_gate'] = R.gate(str(OUT), BED, 'UB', P)
    report[name] = v
    write(OUT / (name + '_restore.json'), json.dumps(v, ensure_ascii=False, indent=2))
    return v

check('baseline', good)
# Re-evaluate genuine archived files, with SYN omitted from a separate copy.
actual = ROOT / 'evidence/history_actual/hist_20261014_094731'
no_syn = ROOT / 'evidence/history_no_syn'
for src in actual.rglob('*'):
    rel = src.relative_to(actual)
    if rel.parts[0] == 'SYN':
        continue
    dst = no_syn / rel
    if src.is_dir():
        dst.mkdir(parents=True, exist_ok=True)
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(src.read_bytes())
no_syn_v = H.evaluate(str(no_syn), H.load_params(str(KIT / 'history_test/history_params.json')))
check('actual_bundle_without_SYN', no_syn_v)
# UN observes the wrong ID set and only one zero row: cannot prove erasure.
L.write_custom(str(J / 'UN/obs/un_pre_bot.dump'), 3200000, hc, [dict(zip(hc, [999,3,0,0,0,0]))])
check('un_wrong_atom_ids', good)
L.write_custom(str(J / 'UN/obs/un_pre_bot.dump'), 3200000, hc, zero)
# A short PRE/POST dump has valid matching rows but declared count 20.
for rel in ('R/obs/pre_bot.dump', 'R/obs/post_atom_3200000.dump'):
    p = J / rel
    write(p, p.read_text().replace('ITEM: NUMBER OF ATOMS\n2\n', 'ITEM: NUMBER OF ATOMS\n20\n'))
    assert not L.read_dump(str(p), 'custom')['ok']
check('truncated_pre_post_declared_20_rows_2', good)
for rel in ('R/obs/pre_bot.dump', 'R/obs/post_atom_3200000.dump'):
    L.write_custom(str(J / rel), 3200000, hc, hist)
write(J / 'UN/screen.txt', 'ERROR: synthetic failure after a partial dump\n')
write(J / 'UN/run_check.txt', 'UNread screen.txt FAIL rc=1\n')
check('un_technical_failure_receipt', good)
assert all(v['status'] == 'RESTORED' and v['followup_UB_gate'][0] for v in report.values())
summary = {k: {'status':v['status'], 'history':v['checks']['history_test'],
               'pre_post':v['checks']['pre_post'], 'un_erasure':v['checks']['un_erasure'],
               'followup_UB_gate':v['followup_UB_gate']}
           for k, v in report.items()}
write(ROOT / 'evidence/history_restore_counterexamples.json', json.dumps(summary, ensure_ascii=False, indent=2))
print(json.dumps(summary, ensure_ascii=False, indent=2))
