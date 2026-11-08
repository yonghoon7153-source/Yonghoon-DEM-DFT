"""Inputs that distinguish the surviving mutants (M14 · M18 · M47) — current code must reject them (test gap, not code bug)."""
import copy
from lib import RR, T, row
sc = T.scen('PA13', T.pa13_scen)
mm, l3, rr = (sc[k]['b']['sum'] for k in ('mm', 'l3', 'rr'))
X = 'p2_SBE_vgcf100_sph_fa_cj0_c0_a0.json'
def ed(s, fn):
    s = copy.deepcopy(s); fn(s); return s
rows = [
    ('M14 l3 copied_from True', 'l3', ed(l3, lambda s: s['runs'][0].update(copied_from=True))),
    ('M18 rr compared [same True] + det None', 'rr', ed(rr, lambda s: s['resume'].update(compared=[{'file': X, 'same': True}]))),
    ('M47 mm TL L03 + compared [5]', 'mm', ed(mm, lambda s: (s['stop'].update(code='TIME_LIMIT', run='L03_point'), s['resume'].update(compared=[5])))),
]
for nm, k, s in rows:
    print(f'{nm:42s}', row(T.pa13_folder(sc[k], 'p8_' + nm.split()[0]), s))
