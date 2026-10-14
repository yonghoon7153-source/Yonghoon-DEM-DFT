"""Offline targeted review probes; source and supplied data remain untouched."""
from pathlib import Path
import copy
import gzip
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'source'
sys.path.insert(0, str(SRC / 'scripts'))
import numpy as np
import rint_iface_join as J
import step3_sigma as S3

OUT = ROOT / 'evidence' / 'join_adversarial.json'
TMP = ROOT / 'tmp' / 'join_adversarial'
TMP.mkdir(parents=True, exist_ok=True)
R14 = SRC / 'docs/data/real14_reference_20260928'
SC = SRC / 'docs/data/real14_am_scaffold.csv'
AT = R14 / 'atom_2060000.liggghts.gz'
CT = R14 / 'contact_2060000.liggghts.gz'
TM = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}

def load(p):
    with gzip.open(p, 'rt', encoding='utf-8') as f:
        return f.read().splitlines()

def save(lines, name):
    p = TMP / name
    p.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return p

def index(lines, prefix):
    return next(i for i, x in enumerate(lines) if x.startswith(prefix))

def report(join):
    return {'status': join['status'], 'rejections': join['rejections'],
            'g_geo': join['g_geo'], 'g_frame': join['g_frame'],
            'steps': join['steps']}

al, cl = load(AT), load(CT)
A = J.read_atom_dump_frame(AT)
types = dict(zip(A['ids'].tolist(), A['types'].tolist()))
row = next(i for i in range(index(cl, 'ITEM: ENTRIES') + 1, len(cl))
           if len(cl[i].split()) >= 23 and
           types[int(cl[i].split()[6])] in (1, 2) and types[int(cl[i].split()[7])] in (1, 2))
original_tokens = cl[row].split()
result = {'first_am_am_line': row + 1, 'first_am_am_tokens': original_tokens}
base = J.am_iface_join(SC, AT, CT, type_map=TM)
result['baseline'] = report(base)
print('baseline', base['status'], flush=True)
for tag, col, value in [('negative_area', 21, '-' + original_tokens[21]),
                         ('nan_area', 21, 'nan'),
                         ('nan_pos1_x', 0, 'nan'),
                         ('nan_delta', 22, 'nan')]:
    lines = cl.copy()
    tokens = lines[row].split()
    tokens[col] = value
    lines[row] = ' '.join(tokens)
    try:
        jn = J.am_iface_join(SC, AT, save(lines, tag + '.liggghts'), type_map=TM)
        result[tag] = report(jn)
        print(tag, jn['status'], [x['code'] for x in jn['rejections']], flush=True)
    except Exception as exc:
        result[tag] = {'exception': type(exc).__name__, 'message': str(exc)}
        print(tag, result[tag], flush=True)

# Triclinic-box tilt columns have different values while first two columns agree.
# A frame mismatch should reject even when the geometry currently sampled is unchanged.
aa, cc = al.copy(), cl.copy()
for lines, tilts in [(aa, ('0.001', '0', '0')), (cc, ('0.002', '0', '0'))]:
    i = index(lines, 'ITEM: BOX BOUNDS')
    flags = lines[i].split()[-3:]
    lines[i] = 'ITEM: BOX BOUNDS xy xz yz ' + ' '.join(flags)
    for k in range(3):
        lines[i + 1 + k] += ' ' + tilts[k]
jn = J.am_iface_join(SC, save(aa, 'tilt_atom.liggghts'), save(cc, 'tilt_contact.liggghts'), type_map=TM)
result['different_tilt_boxes'] = report(jn)
print('different_tilt_boxes', jn['status'], flush=True)

# The parser must not turn a nonintegral timestep into an apparently matching integer.
cc = cl.copy()
cc[index(cc, 'ITEM: TIMESTEP') + 1] = '2060000.9'
jn = J.am_iface_join(SC, AT, save(cc, 'fractional_step.liggghts'), type_map=TM)
result['fractional_step'] = report(jn)
print('fractional_step', jn['status'], jn['steps'], flush=True)

OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=True), encoding='utf-8')
print('evidence', OUT, flush=True)
