"""Scratch — run readback CLI --table GM with --md on generated D2 decks (with deck_meta.json) and check the markdown."""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

W = sys.argv[1]
sys.path.insert(0, W + '/scripts')
import make_mixer_deck as g  # noqa: E402

spec = importlib.util.spec_from_file_location('_cdr', os.path.join(W, 'scripts', 'check_doc_refs.py'))
cdr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cdr)


def mk(gp, gs, d):
    p = g.plan(100000, cgf=151.4, stiffen_se=20.0, dens_gen='lab20261014')
    a = g.gm_arm({'AM_P': gp, 'AM_S': gs, 'SE': 1.0}, gamma_wall=g.gm_wall_from_ncm(0.3), bo_se=0.5, rho_uncoated_ncm=0.3)
    nm = g.register_arm('GMMD', a)
    try:
        rpm = g.resolve_rpm(p['R'])
        t = g.deck(p, rpm, 2, seed=32452843, arm=nm, hold_bo_pairwise=True)
        m = g.deck_meta(p, rpm, 2, 32452843, nm, t, argv=['x'], hold_bo_pairwise=True)
    finally:
        g.ARMS.pop(nm, None)
    os.makedirs(d)
    open(os.path.join(d, 'in.mixer'), 'w', encoding='utf-8').write(t)
    json.dump(m, open(os.path.join(d, 'deck_meta.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    return os.path.join(d, 'in.mixer')


with tempfile.TemporaryDirectory() as td:
    a, b = mk(0.3, 0.3, os.path.join(td, 'GMuu')), mk(1.0, 1.0, os.path.join(td, 'GMcc'))
    md = os.path.join(td, 'r.md')
    p = subprocess.run([sys.executable, '-B', os.path.join(W, 'scripts', 'mixer_deck_readback.py'), '--table', 'GM', a, b,
                        '--table', 'E', a, a, '--md', md], capture_output=True, text=True)
    txt = open(md, encoding='utf-8').read() if os.path.exists(md) else ''
    hits = [h for ln in txt.split('\n') for h in cdr._RE_SHA.findall(ln) if not h.isdigit()]
    print('rc', p.returncode, '(expected 1: the E table of a deck against itself must FAIL)')
    print('stderr tail', p.stderr.strip().splitlines()[-1:] if p.stderr.strip() else '-')
    print('md has GM table', '## 표 GM' in txt, '| AM_P–AM_P |' in txt, 'D2 덱' in txt, 'backtick hex hits', len(hits))
    print('\n'.join(l for l in txt.split('\n') if l.startswith('| `GM') or l.startswith('| AM_P–AM_P') or l.startswith('| SE–SE'))[:1500])
