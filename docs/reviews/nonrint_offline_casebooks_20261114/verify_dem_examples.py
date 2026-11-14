"""Hand-worked design examples only. No engine, repository import, or file access."""
from fractions import Fraction as Q
import json


def examples():
    rows = []

    def record(name, observed, expected, wrong_shortcut):
        if observed != expected:
            raise AssertionError((name, observed, expected))
        if wrong_shortcut == expected:
            raise AssertionError((name, 'shortcut does not distinguish this example'))
        rows.append(dict(id=name, observed=observed, expected=expected,
                         wrong_shortcut=wrong_shortcut))

    # Identical geometry does not erase particle ownership.
    contributions = [('p1', 0), ('p2', 0), ('p3', 0)]
    record('D01_ID', len({p for p, node in contributions if node == 0}), 3, 1)

    w, bi, bj, d = Q(1, 2), Q(1), Q(1), Q(5, 2)
    record('D02_TWO_BUDGETS', d <= 2*w+bi+bj, True, d <= 2*w+bi)
    # Equality belongs to the conservative graph, not a claim of positive weight.
    d = 2*w+bi+bj
    record('D03_EQUALITY', d <= 2*w+bi+bj, True, d < 2*w+bi+bj)

    # Rotation and deformation are point displacements; plate displacement is 0.
    record('D04_ROTATION', Q(2) > Q(1, 2)**2, True, Q(0) > Q(1, 2)**2)
    record('D05_DEFORMATION', Q(1, 2) > Q(1, 4), True, Q(0) > Q(1, 4))

    length, a, b = Q(10), Q(1, 10), Q(99, 10)
    raw = abs(b-a)
    periodic = min(raw, length-raw)
    record('D06_PERIODIC', periodic <= 2*w, True, raw <= 2*w)

    # Path graph 0--1--2--3; registered greedy order is not a chromatic proof.
    neighbors = {0: {1}, 1: {0, 2}, 2: {1, 3}, 3: {2}}
    def greedy(order):
        colors = {}
        for v in order:
            used = {colors[n] for n in neighbors[v] if n in colors}
            color = 0
            while color in used:
                color += 1
            colors[v] = color
        return len(set(colors.values()))
    record('D07_ORDER', [greedy([0, 1, 2, 3]), greedy([0, 3, 1, 2])], [2, 3], [2, 2])

    # A collision requires discard of the tentative P2G, not a new accepted mass.
    collision = len({p for p, color, node in [('p1', 0, 4), ('p2', 0, 4)]}) > 1
    record('D08_COLLISION', collision, True, False)
    # Three mutually adjacent vertices need three distinct colors, not two.
    record('D09_CAPACITY', 3 > 2, True, False)

    # Arbitrary byte units in this toy; not a measured memory coefficient.
    old, new, temporary, other, limit = 800, 900, 200, 100, 1500
    record('D10_PEAK', old+new+temporary+other > limit, True,
           max(old, new)+temporary+other > limit)

    # M32P corrected example: shared grid nodes do not force equal interpolants.
    v = [Q(0), Q(1), Q(2)]
    wa, wb = [Q(405, 1000), Q(590, 1000), Q(5, 1000)], [Q(180, 1000), Q(740, 1000), Q(80, 1000)]
    assert sum(wa) == sum(wb) == 1
    va, vb = sum(w*x for w, x in zip(wa, v)), sum(w*x for w, x in zip(wb, v))
    gap = Q(9, 10)-Q(6, 10)
    record('D11_INTERPOLATION', str(gap+vb-va), '3/5', str(gap))

    # Tangential impulses only, equal unit masses. This is NOT a contact solver.
    initial = [Q(0), Q(1), Q(-2)]
    jab, jbc = Q(1, 2), Q(-1)
    final = [initial[0]+jab, initial[1]-jab+jbc, initial[2]-jbc]
    work_ab_initial = jab*(initial[0]-initial[1])
    work_ab_final = jab*(final[0]-final[1])
    energy_initial = sum(x*x/2 for x in initial)
    energy_final = sum(x*x/2 for x in final)
    assert sum(initial) == sum(final) == -1
    assert energy_initial == Q(5, 2) and energy_final == Q(3, 4)
    record('D12_FINAL_SLIP', work_ab_final <= 0, False, work_ab_initial <= 0)
    return dict(scope='DESIGN_ARITHMETIC_ONLY', observations=rows,
                observations_count=len(rows), production_regressions=0,
                solver_runs=0, field_runs=0, real_inputs_read=0,
                implementation_qualification=False, overall='HOLD')


if __name__ == '__main__':
    print(json.dumps(examples(), ensure_ascii=True, indent=2))
