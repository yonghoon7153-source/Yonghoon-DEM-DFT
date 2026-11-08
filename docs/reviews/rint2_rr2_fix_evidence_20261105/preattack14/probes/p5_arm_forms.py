"""arms_read_kind over (a) synthetic judged-complete records for every request form (ARMS 1..8 · ARM_LIST subsets) and
   (b) every honest run record of real chain outputs (main ladders P0/P1 · main predict · variant set FIBRE) — expect verified, no value reason."""
import itertools
from lib import RR, T

bad, n = [], 0
for N in range(1, 9):
    rec = {'name': 'L01_floor', 'kit': T.SBE_KIT, 'arms': N, 'arm_list': None, 'outdir': f'L01_floor_arm{N}'}
    ar = [T.ct06_pub(i) for i in range(N)]
    k = RR.arms_read_kind(ar, rec)
    n += 1
    if k[0] != 'verified':
        bad.append(('arms', N, k))
for r in range(1, 8):
    for al in itertools.combinations(range(8), r):
        al = list(al)
        if al == list(range(len(al))):
            continue
        rec = {'name': 'P13_origin', 'kit': T.DBE_KIT, 'arms': len(al), 'arm_list': al}
        ar = [T.ct06_pub(i, kit=T.DBE_KIT) for i in al]
        k = RR.arms_read_kind(ar, rec)
        n += 1
        if k[0] != 'verified':
            bad.append(('arm_list', al, k))
print('synthetic forms:', n, 'not verified:', bad[:5])
real = {}
srcs = [('lad_P0', T.s_main('P0')), ('lad_P1', T.s_main('P1')), ('pred', T.s_main_predict())]
for lab, res in srcs:
    s = res.get('sum') or {}
    forms = {}
    for r in s.get('runs') or []:
        if not r.get('arms_read'):
            continue
        k = RR.arms_read_kind(r['arms_read'], r)
        whys = [RR.arm_public_value_problem(a) for a in r['arms_read']]
        key = (r.get('arms'), tuple(r['arm_list']) if r.get('arm_list') else None)
        forms.setdefault(key, []).append((k[0], [w for w in whys if w][:1]))
    real[lab] = {str(k): (len(v), sorted(set(x[0] for x in v)), [x[1] for x in v if x[1]][:1]) for k, v in forms.items()}
for lab, v in real.items():
    print(lab, v)
