"""L13 world search — a smooth (monotone) SBE response whose first R_j,0 confirm fails (interpolation curvature > 2 %) and the second passes."""
import itertools
import math
import sys

sys.path.insert(0, '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-afe53be7bdb176c82/scripts')
import rint_r_chain as RR


def mk(f, C, Rc, beta):
    def S(R, i=0):
        if R == math.inf:
            return f
        if R == 0.0:
            return C
        return f + (C - f) / (1.0 + (R / Rc) ** beta)

    def fetch(role, key, arms):
        R = RR.rj_float(key)
        idx = list(range(arms)) if isinstance(arms, int) else list(arms)
        return [{'sigma': S(R) * 1e-3, 'state': 'positive'} for _ in idx]
    return fetch


hits = []
for f, C in ((0.5, 20.0), (0.3, 10.0), (1.0, 5.0)):
    for beta in (1.5, 2.0, 3.0, 4.0, 6.0):
        for le in [x / 8 for x in range(24, 64)]:
            Rc = 10 ** le
            lad = RR.Ladder(mk(f, C, Rc, beta), max_points=30, ratio_max='none')
            try:
                lad.run()
            except RR.Stop as e:
                continue
            cf = lad.st['confirms']
            if [c['ok'] for c in cf] == [False, True]:
                hits.append((f, C, beta, le, lad.st['n_runs'], cf))
for h in hits[:10]:
    print(h)
print(len(hits))
