"""Quick diff of an old-arm deck between the snapshot generator (unfixed) and the working-tree generator."""
import difflib
import importlib.util
import sys

OLD = '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/mxd2fix/snap_before/scripts/make_mixer_deck.py'
NEW = sys.argv[1]


def load(p, n):
    s = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


o, n = load(OLD, 'o'), load(NEW, 'n')
for arm in ('LC', 'E0', 'LA'):
    po, pn = o.plan(8000), n.plan(8000)
    to = o.deck(po, 60, 2, seed=32452843, arm=arm)
    tn = n.deck(pn, 60, 2, seed=32452843, arm=arm)
    d = [l for l in difflib.unified_diff(to.split('\n'), tn.split('\n'), lineterm='', n=0) if l[:1] in '+-' and l[:3] not in ('+++', '---')]
    print(arm, 'identical' if to == tn else f'{len(d)} diff lines', d[:6])
