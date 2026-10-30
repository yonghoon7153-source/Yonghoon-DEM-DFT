"""Independent G1/G3 check for the D0.7 -T: original insertion log vs test output, plus deck-echo check.

Usage: python3 -I g13_check.py <orig_log> <test_out> <deck> <deck_last_line> <out_json>
  orig_log       original run log (kg50_d07_b50.ins1/log.liggghts on ibb)
  test_out       -T test job output (logs/output_kg50_d07_b50_r56t_333858.out)
  deck           pinned original deck (docs/data/kg50_decks_20261027_v3_b50/kg50_d07_b50/input_kg50_d07_b50.liggghts)
  deck_last_line last deck line to check as executed before the checkpoint (157 = first long run)
Reads only; writes out_json.
"""
import hashlib, json, re, sys
from pathlib import Path

orig, test, deck, last, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5])
NUM = re.compile(r'^[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?$')


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def thermo_rows(lines):
    """All thermo rows: (line_no, header, row) — header = line whose first token is Step; rows = all-numeric, same width."""
    rows, hdr = [], None
    for i, ln in enumerate(lines, 1):
        t = ln.split()
        if t and t[0] == 'Step':
            hdr = t
            continue
        if hdr and t and len(t) == len(hdr) and all(NUM.match(x) for x in t):
            rows.append((i, hdr, t))
        elif hdr and t:
            hdr = None
    return rows


def pick(rows, step):
    res = []
    for i, h, t in rows:
        if int(float(t[0])) == step:
            d = dict(zip(h, t))
            res.append({'line': i, 'Atoms': d.get('Atoms'), 'KinEng': d.get('KinEng'), 'cols': h})
    return res


def rel(a, b):
    a, b = float(a), float(b)
    return abs(a - b) / max(abs(b), 1e-300)


ol = orig.read_text(encoding='utf-8', errors='replace').split('\n')
tl = test.read_text(encoding='utf-8', errors='replace').split('\n')
orow, trow = thermo_rows(ol), thermo_rows(tl)
res = {'orig': {'path': str(orig.name), 'sha256': sha(orig), 'bytes': orig.stat().st_size, 'lines': len(ol)},
       'test': {'path': str(test.name), 'sha256': sha(test), 'bytes': test.stat().st_size, 'lines': len(tl)},
       'deck': {'path': str(deck.name), 'sha256': sha(deck), 'checked_lines': f'1-{last}'}}
res['orig']['first_line'] = ol[0][:160] if ol else ''
res['orig']['n_thermo_rows'] = len(orow)
res['orig']['last_thermo_row'] = {'line': orow[-1][0], 'step': orow[-1][2][0]} if orow else None
res['orig']['n_ERROR_lines'] = sum(1 for x in ol if x.startswith('ERROR'))
res['orig']['phase_markers'] = [(i, x.strip()[:90]) for i, x in enumerate(ol, 1) if '======' in x][:40]
for step in (20001, 21000):
    res[f'orig_{step}'] = pick(orow, step)
    res[f'test_{step}'] = pick(trow, step)
g = {}
o1, t1 = res['orig_20001'], res['test_20001']
if o1 and t1:
    g['G1_test_setup_KE'] = t1[0]['KinEng']
    g['G1_orig_KE_rows'] = [r['KinEng'] for r in o1]
    g['G1_rel_vs_each_orig_row'] = [rel(t1[0]['KinEng'], r['KinEng']) for r in o1]
    g['G1_atoms_same'] = all(r['Atoms'] == t1[0]['Atoms'] for r in o1)
o3, t3 = res['orig_21000'], res['test_21000']
if o3 and t3:
    g['G3_test_KE'] = t3[0]['KinEng']
    g['G3_orig_KE'] = o3[0]['KinEng']
    g['G3_rel'] = rel(t3[0]['KinEng'], o3[0]['KinEng'])
    g['G3_atoms_same'] = t3[0]['Atoms'] == o3[0]['Atoms']
res['G'] = g

# deck echo: deck lines 1..last, '&' continuations joined the LAMMPS way, whitespace collapsed,
# must appear in order as echoed lines of the original log (substituted copies and output lines may sit between them).
dl = deck.read_text(encoding='utf-8').split('\n')[:last]
cmds, buf, start = [], '', None
for i, ln in enumerate(dl, 1):
    s = ln.rstrip()
    if start is None:
        start = i
    if s.endswith('&'):
        buf += s[:-1]
        continue
    buf += s
    j = ' '.join(buf.split())
    if j:
        cmds.append((start, j))
    buf, start = '', None
logn = [' '.join(x.split()) for x in ol]
pos, miss, first_hit = 0, [], None
for no, c in cmds:
    k = pos
    while k < len(logn) and logn[k] != c:
        k += 1
    if k < len(logn):
        if first_hit is None:
            first_hit = k + 1
        pos = k + 1
    else:
        miss.append((no, c[:120]))
res['deck_echo'] = {'deck_commands_checked': len(cmds), 'found_in_order': len(cmds) - len(miss),
                    'missing': miss[:20], 'first_hit_log_line': first_hit,
                    'last_hit_log_line': pos if len(cmds) > len(miss) else None}
out.write_text(json.dumps(res, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('orig', res['orig']['sha256'], res['orig']['bytes'], 'B · thermo rows', len(orow), '· last step', res['orig']['last_thermo_row'], '· ERROR', res['orig']['n_ERROR_lines'])
print('test', res['test']['sha256'])
print('G1', json.dumps(g.get('G1_test_setup_KE')), 'vs', g.get('G1_orig_KE_rows'), 'rel', g.get('G1_rel_vs_each_orig_row'), 'atoms same', g.get('G1_atoms_same'))
print('G3', g.get('G3_test_KE'), 'vs', g.get('G3_orig_KE'), 'rel', g.get('G3_rel'), 'atoms same', g.get('G3_atoms_same'))
print('deck echo', res['deck_echo']['found_in_order'], '/', res['deck_echo']['deck_commands_checked'], 'missing', len(miss))
for m in miss[:10]:
    print('  miss line', m[0], ':', m[1])
