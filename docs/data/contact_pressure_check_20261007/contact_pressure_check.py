#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""웹앱 3D 'Stress Concentration' 의 양 (입자별 최대 접촉 압력 = |Fn| / 덤프 접촉 면적) 이 하중을 따라가는지 — real14 커밋 원자료로 확인 (10-07).

    python3 docs/data/contact_pressure_check_20261007/contact_pressure_check.py [atom.gz contact.gz] > real14_contact_pressure.txt

입력 기본값 = docs/data/real14_reference_20260928/ 의 atom_2060000 · contact_2060000 (hooke/hysteresis 덱 · scale 1000).
웹앱과 같은 정의: p = |force_normal| / contactArea × scale / 1e6 (MPa) · 입자별 최대 (scripts/viewer3d_data.py stress_max).
부호 = force_normal · (pos1 − pos2) / |pos1 − pos2| (> 0 밀어냄 = 압축 · < 0 당김 = 접착) — 주기 경계 너머 접촉 (거리 > 1.5 (r1 + r2)) 은 부호를 셀 수 없어 뺀다.
"""
import gzip
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
REF = ROOT / 'docs/data/real14_reference_20260928'
atom_p = Path(sys.argv[1]) if len(sys.argv) > 2 else REF / 'atom_2060000.liggghts.gz'
cont_p = Path(sys.argv[2]) if len(sys.argv) > 2 else REF / 'contact_2060000.liggghts.gz'
SCALE = 1000.0
NAME = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}


def body(path, head):
    with gzip.open(path, 'rt') as f:
        lines = f.read().split('\n')
    i = next(k for k, l in enumerate(lines) if l.startswith(head))
    return [l for l in lines[i + 1:] if l.strip()]


types, rad, zpos = {}, {}, {}
for l in body(atom_p, 'ITEM: ATOMS'):
    v = l.split()
    a = int(v[0]); types[a] = int(v[1]); zpos[a] = float(v[4]); rad[a] = float(v[5])
rows = np.array([[float(x) for x in l.split()] for l in body(cont_p, 'ITEM: ENTRIES')])
# c_cpl: 1–3 pos1 · 4–6 pos2 · 7 id1 · 8 id2 · 9 periodic · 10–12 force · 13–15 force_normal · 16–18 force_tangential · 19–21 torque · 22 contactArea · 23 delta · 24–26 contactPoint
id1, id2 = rows[:, 6].astype(int), rows[:, 7].astype(int)
fn_vec = rows[:, 12:15]
fn = np.linalg.norm(fn_vec, axis=1)
area = rows[:, 21]
pair = np.array(['-'.join(sorted([NAME[types[a]], NAME[types[b]]])) for a, b in zip(id1, id2)])
d12 = rows[:, 0:3] - rows[:, 3:6]
dist = np.linalg.norm(d12, axis=1)
rsum = np.array([rad[a] + rad[b] for a, b in zip(id1, id2)])
wrapped = dist > 1.5 * rsum
sgn = np.einsum('ij,ij->i', fn_vec, d12 / np.where(dist > 0, dist, 1)[:, None])
ok = (area > 0) & (fn > 0)
p = np.where(ok, fn / np.where(area > 0, area, 1) * SCALE / 1e6, np.nan)
comp = ok & ~wrapped & (sgn > 0)
pull = ok & ~wrapped & (sgn < 0)

print(f'# 원자료: {atom_p.relative_to(ROOT) if atom_p.is_relative_to(ROOT) else atom_p} · {cont_p.relative_to(ROOT) if cont_p.is_relative_to(ROOT) else cont_p}')
print(f'접촉 {len(fn)} · 면적 > 0 · 힘 > 0 = {int(ok.sum())} · 주기 경계 너머 (거리 > 1.5(r1+r2)) {int(wrapped.sum())} (periodic 열 1 = {int((rows[:, 8] != 0).sum())}) · 압축 {int(comp.sum())} · 당김 {int(pull.sum())}')
print()
print('## 1. 압축 접촉: 힘은 크게 달라도 압력은 거의 같은 천장 (쌍 유형별)')
print('| 쌍 | n | |Fn| p5–p95 폭 | p (MPa) p5 · p50 · p95 · p99 | p5–p95 폭 | 기울기 d log p / d log |Fn| |')
print('|---|---|---|---|---|---|')
for pt in sorted(set(pair)):
    m = comp & (pair == pt)
    if m.sum() < 20:
        continue
    lf, lp = np.log10(fn[m]), np.log10(p[m])
    q = lambda a, x: float(np.percentile(a, x))
    print(f'| {pt} | {int(m.sum())} | {10 ** (q(lf, 95) - q(lf, 5)):.1f} 배 | {q(p[m], 5):.1f} · {q(p[m], 50):.1f} · {q(p[m], 95):.1f} · {q(p[m], 99):.1f} | '
          f'{10 ** (q(lp, 95) - q(lp, 5)):.2f} 배 | {np.polyfit(lf, lp, 1)[0]:+.3f} |')
print()
print('## 2. 당김 (접착) 접촉')
print('| 쌍 | 당김 몫 (주기 너머 제외) | 당김 p 중앙값 (MPa) |')
print('|---|---|---|')
for pt in sorted(set(pair)):
    m = ok & ~wrapped & (pair == pt)
    if m.sum() < 20:
        continue
    mm = m & (sgn < 0)
    print(f'| {pt} | {100 * mm.sum() / m.sum():.2f} % | {np.median(p[mm]) if mm.any() else float("nan"):.1f} |')
print()
print('## 3. p 가 가장 큰 접촉 8 개')
print('| p (MPa) | 쌍 | 부호 | δ / (r1 + r2) | 거리 / (r1 + r2) |')
print('|---|---|---|---|---|')
for k in np.argsort(np.nan_to_num(p, nan=-1))[::-1][:8]:
    print(f'| {p[k]:.1f} | {pair[k]} | {"당김" if sgn[k] < 0 else "압축"} | {rows[k, 22] / rsum[k]:.2e} | {dist[k] / rsum[k]:.6f} |')
print()
print('## 4. 입자별 최대 (웹앱 보기의 양) — 색 범위 = 전체 입자 p5–p95 (log)')
ids = np.array(sorted(types)); idx = {a: k for k, a in enumerate(ids)}
pmax_all = np.zeros(len(ids)); pmax_cmp = np.zeros(len(ids)); arg_pull = np.zeros(len(ids), bool)
for k in np.nonzero(ok)[0]:
    for a in (id1[k], id2[k]):
        j = idx[a]
        if p[k] > pmax_all[j]:
            pmax_all[j] = p[k]; arg_pull[j] = bool(pull[k])
        if comp[k] and p[k] > pmax_cmp[j]:
            pmax_cmp[j] = p[k]
t = np.array([types[a] for a in ids])
v = pmax_all[pmax_all > 0]
lo, med, hi = (float(np.percentile(v, x)) for x in (5, 50, 95))
print(f'전체 입자 (최대 p > 0) {len(v)} · p5 {lo:.1f} · 중앙값 {med:.1f} · p95 {hi:.1f} MPa (웹앱 색 범위 규칙)')
for tt in (1, 2, 3):
    m = (t == tt) & (pmax_all > 0)
    print(f'- {NAME[tt]}: 입자 {int(m.sum())} · 색 범위 위 (> p95) {100 * np.mean(pmax_all[m] > hi):.1f} % · 아래 (< p5) {100 * np.mean(pmax_all[m] < lo):.1f} % · '
          f'최대가 당김 접촉에서 온 입자 {100 * np.mean(arg_pull[m]):.1f} % · 최대 ≥ 1e4 MPa {int((pmax_all[m] >= 1e4).sum())} (압축만 세면 {int((pmax_cmp[m] >= 1e4).sum())})')
