#!/usr/bin/env python3
"""G2c 샌드박스 대조 (읽기만) — 노트 docs/reviews/p1_g2c_source_check_20261104.md §6 의 예측을 셈한다.

사용: python3 -I compare.py OUT N  → OUT/compare.json + 화면 표
접촉 덤프 30 열 = pos 6 · id 3 (id1 id2 주기) · force 3 · force_normal 3 · force_tangential 3 · torque 3 ·
history 4 (deltaMax · shear x y z — 접촉 모델 구성 순서 = normal → tangential) · contactArea · delta · contactPoint 3.
쌍 열쇠 = (작은 id, 큰 id).  순서가 뒤집힌 줄은 pos 를 바꾸고 힘 · 접선 이력 부호를 뒤집는다 (torque 는 같은 순서 줄만).
"""
import json, math, sys, pathlib

GROUPS = {'pos': range(0, 6), 'force': range(9, 12), 'force_normal': range(12, 15),
          'force_tangential': range(15, 18), 'torque': range(18, 21), 'deltaMax': range(21, 22),
          'shear': range(22, 25), 'contactArea': range(25, 26), 'delta': range(26, 27),
          'contactPoint': range(27, 30)}
FLIP_NEG = list(range(9, 18)) + list(range(22, 25))


def read_local(p):
    lines = pathlib.Path(p).read_text().splitlines()
    i = lines.index('ITEM: NUMBER OF ENTRIES')
    n = int(lines[i + 1])
    j = next(k for k, l in enumerate(lines) if l.startswith('ITEM: ENTRIES'))
    rows = {}
    for l in lines[j + 1:j + 1 + n]:
        v = [float(t) for t in l.split()]
        if len(v) != 30:
            sys.exit('bad row width %d in %s' % (len(v), p))
        a, b = int(v[6]), int(v[7])
        flipped = a > b
        if flipped:
            v = v[3:6] + v[0:3] + v[6:]
            for c in FLIP_NEG:
                v[c] = -v[c]
        key = (min(a, b), max(a, b))
        if key in rows:
            sys.exit('duplicate pair %s in %s' % (key, p))
        rows[key] = (v, flipped)
    return rows


def read_atoms(p):
    lines = pathlib.Path(p).read_text().splitlines()
    j = next(k for k, l in enumerate(lines) if l.startswith('ITEM: ATOMS'))
    out = {}
    for l in lines[j + 1:]:
        t = l.split()
        if t:
            out[int(t[0])] = [float(x) for x in t[1:]]
    return out


def cmp_local(ra, rx):
    common = sorted(set(ra) & set(rx))
    res = {'n_ref': len(ra), 'n_x': len(rx), 'n_common': len(common),
           'only_ref': len(set(ra) - set(rx)), 'only_x': len(set(rx) - set(ra)),
           'orientation_differs': sum(1 for k in common if ra[k][1] != rx[k][1]), 'groups': {}}
    for g, cols in GROUPS.items():
        nd = 0; mabs = 0.0; mrel = 0.0; nconsidered = 0
        for k in common:
            va, fa = ra[k]; vx, fx = rx[k]
            if g == 'torque' and fa != fx:
                continue
            nconsidered += 1
            d = False
            for c in cols:
                a, b = va[c], vx[c]
                if a != b:
                    d = True
                    ad = abs(a - b); mabs = max(mabs, ad)
                    s = max(abs(a), abs(b))
                    if s > 0:
                        mrel = max(mrel, ad / s)
            nd += d
        res['groups'][g] = {'n_pairs': nconsidered, 'n_differ': nd, 'max_abs': mabs, 'max_rel': mrel}
    return res


def cmp_hist(ra, rx):
    """x 의 이력 (deltaMax · shear) ↔ ra 의 이력 — 정확히 같은 쌍 수."""
    common = sorted(set(ra) & set(rx))
    eq_dm = sum(1 for k in common if ra[k][0][21] == rx[k][0][21])
    eq_sh = sum(1 for k in common if all(ra[k][0][c] == rx[k][0][c] for c in range(22, 25)))
    return {'n_common': len(common), 'deltaMax_equal': eq_dm, 'shear_equal': eq_sh,
            'only_ref': len(set(ra) - set(rx)), 'only_x': len(set(rx) - set(ra))}


def cmp_atoms(aa, ax):
    common = sorted(set(aa) & set(ax))
    nd = sum(1 for i in common if aa[i] != ax[i])
    return {'n_ref': len(aa), 'n_x': len(ax), 'n_common': len(common), 'n_differ': nd}


def main():
    O = pathlib.Path(sys.argv[1]); N = int(sys.argv[2])
    A = read_local(O / 'A/post' / ('c_%d.txt' % N))
    Apre = read_local(O / 'A/post' / ('cpre_%d.txt' % (N - 1)))
    arms = {a: read_local(O / a / 'post' / ('c_%d.txt' % N)) for a in ('A2', 'B', 'B2', 'C')}
    atoms = {a: read_atoms(O / a / 'post' / ('atom_%d.txt' % N)) for a in ('A', 'A2', 'B', 'B2', 'C')}
    out = {'N': N, 'deltaMax_nonneg_A': all(v[0][21] >= 0 for v in A.values()),
           'contact_vs_A': {a: cmp_local(A, r) for a, r in arms.items()},
           'hist_vs_A_at_N': {a: cmp_hist(A, r) for a, r in arms.items()},
           'hist_vs_A_at_Nm1': {a: cmp_hist(Apre, r) for a, r in arms.items()},
           'atoms_vs_A': {a: cmp_atoms(atoms['A'], atoms[a]) for a in ('A2', 'B', 'B2', 'C')}}
    # B 쪽 세분: N-1 에도 있던 쌍 = 접선 이력이 A(N-1) 과 정확히 같은가 · N 에 새로 닿은 쌍 = 접선 이력 0 인가 ·
    # 법선력 다른 쌍 = A 에서 N 에 최대 겹침이 '커짐 말고' 바뀐 쌍 (인장 갈래 · 가드된 갱신) 인가
    Bx = arms['B']; sub = {}
    old_pairs = [k for k in Bx if k in Apre]; new_pairs = [k for k in Bx if k not in Apre]
    sub['old_pairs'] = len(old_pairs)
    sub['old_pairs_shear_eq_A_Nm1'] = sum(1 for k in old_pairs if all(Bx[k][0][c] == Apre[k][0][c] for c in range(22, 25)))
    sub['new_pairs'] = len(new_pairs)
    sub['new_pairs_shear_zero'] = sum(1 for k in new_pairs if all(Bx[k][0][c] == 0.0 for c in range(22, 25)))
    def guarded_change(k):
        if k not in Apre or k not in A:
            return False
        dmN, dmP, dl = A[k][0][21], Apre[k][0][21], A[k][0][26]
        return dmN != dmP and abs(dmN - dl) > 1e-9 * max(abs(dl), 1e-300)
    fnd = [k for k in Bx if k in A and any(A[k][0][c] != Bx[k][0][c] for c in range(12, 15))]
    sub['fn_differ'] = len(fnd)
    sub['fn_differ_guarded_change_in_A'] = sum(1 for k in fnd if guarded_change(k))
    sub['guarded_change_pairs_in_A'] = sum(1 for k in A if guarded_change(k))
    dmd = [k for k in Bx if k in A and A[k][0][21] != Bx[k][0][21]]
    sub['deltaMax_differ_vs_A_N'] = len(dmd)
    sub['deltaMax_differ_vs_A_N_guarded_change'] = sum(1 for k in dmd if guarded_change(k))
    out['B_detail'] = sub
    (O / 'compare.json').write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
    print('N', N, 'A pairs', len(A), 'A(N-1) pairs', len(Apre), 'deltaMax>=0', out['deltaMax_nonneg_A'])
    for a, r in out['contact_vs_A'].items():
        g = r['groups']
        print('%-3s common %d only_A %d only_x %d orient %d | ' % (a, r['n_common'], r['only_ref'], r['only_x'], r['orientation_differs'])
              + ' '.join('%s %d/%d' % (k, v['n_differ'], v['n_pairs']) for k, v in g.items()))
        print('     max_rel ' + ' '.join('%s %.2e' % (k, v['max_rel']) for k, v in g.items() if v['n_differ']))
    for lab in ('hist_vs_A_at_N', 'hist_vs_A_at_Nm1'):
        print(lab, ' '.join('%s dm %d/%d sh %d/%d' % (a, v['deltaMax_equal'], v['n_common'], v['shear_equal'], v['n_common'])
                            for a, v in out[lab].items()))
    print('B_detail', json.dumps(out['B_detail'], ensure_ascii=False))
    print('atoms', ' '.join('%s %d/%d differ' % (a, v['n_differ'], v['n_common']) for a, v in out['atoms_vs_A'].items()))


if __name__ == '__main__':
    main()
