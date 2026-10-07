"""접선력을 넣으면 힘 기여도가 얼마나 바뀌나 — real14 커밋 덤프 (법선 |Fn| · 접선 |Ft| · 합 |Fn+Ft|)."""
import gzip, sys
import numpy as np
atom_p, cont_p = sys.argv[1], sys.argv[2]
def body(path, head):
    with gzip.open(path, 'rt') as f:
        lines = f.read().split('\n')
    i = next(k for k, l in enumerate(lines) if l.startswith(head))
    return [l for l in lines[i + 1:] if l.strip()]
types = {}
for l in body(atom_p, 'ITEM: ATOMS'):
    v = l.split(); types[int(v[0])] = int(v[1])
rows = np.array([[float(x) for x in l.split()] for l in body(cont_p, 'ITEM: ENTRIES')])
NAME = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}
id1, id2 = rows[:, 6].astype(int), rows[:, 7].astype(int)
fnv, ftv = rows[:, 12:15], rows[:, 15:18]
fn, ft, ftot = np.linalg.norm(fnv, axis=1), np.linalg.norm(ftv, axis=1), np.linalg.norm(fnv + ftv, axis=1)
grp = []
for a, b in zip(id1, id2):
    ta, tb = NAME[types[a]], NAME[types[b]]
    am = ('AM' in ta) + ('AM' in tb)
    grp.append({2: 'AM–AM', 1: 'AM–SE', 0: 'SE–SE'}[am])
grp = np.array(grp)
MU = 0.5
print(f'접촉 {len(fn)} · μ = {MU} (덱 coefficientFriction 전 쌍 0.5)')
print('| 묶음 | 접촉 수 | |Ft|/|Fn| 중앙값 | Σ|Ft|/Σ|Fn| | 쿨롱 한계 (|Ft| ≥ 0.99 μ|Fn|) 몫 | 기여도: 법선만 | 합력 |Fn+Ft| | 차 |')
print('|---|---|---|---|---|---|---|---|')
tn, tt = fn.sum(), ftot.sum()
for g in ('AM–AM', 'AM–SE', 'SE–SE'):
    m = grp == g
    r = ft[m] / np.where(fn[m] > 0, fn[m], np.nan)
    print(f'| {g} | {m.sum()} | {np.nanmedian(r):.3f} | {ft[m].sum() / fn[m].sum():.3f} | {100 * np.nanmean(r >= 0.99 * MU):.1f} % | '
          f'{100 * fn[m].sum() / tn:.2f} % | {100 * ftot[m].sum() / tt:.2f} % | {100 * ftot[m].sum() / tt - 100 * fn[m].sum() / tn:+.2f} %p |')
print(f'전체 Σ|Ft|/Σ|Fn| = {ft.sum() / fn.sum():.3f} · Σ|Fn+Ft|/Σ|Fn| = {tt / tn:.3f}')
