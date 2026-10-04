#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LHS 감사 묶음 ④ (협착 저항 분율 · σ_VM) — 읽기 전용 검사기 (J20-s · 10-04).

인계 후보 열 둘의 **정의**를 실측으로 잰다.  값은 만들지 않는다 (인계표 · 웹앱 무변경).

  (A) σ_VM 열 (`stress_cv` · `stress_ratio_<상>` — `dem_analysis_core.calc_von_mises_stress`):
      입력 = LIGGGHTS `compute stress/atom` (`c_strs[1–3]`) ÷ 입자 부피 (`analyze_contacts.load_atoms_raw`).
      LIGGGHTS 공개 소스: 입자 접촉은 `pair_gran_base.h` 가 `ev_tally_xyz(i, j, …, delta)` 로 virial 을 내고
      (`delta` = 중심 − 중심) `Pair::ev_tally_xyz` 가 원자마다 **0.5 · delta ⊗ F** 를 준다 = **50/50 분할**.
      `fix wall/gran` 에는 virial 이 없다 → 벽 · 판 접촉은 입자 응력에 들어가지 않는다.
      ⇒ 크기가 다른 두 입자의 접촉에서 큰 입자의 응력은 작게 · 작은 입자는 크게 잡힌다.
      비교 기준 = 입자 평균 응력의 정의식 (Love–Weber · branch vector: 입자 중심 → 접촉점) σ_i = (1/V_i) Σ_c (x_c − x_i) ⊗ f_c.
      둘 다 같은 접촉 덤프 (`pair/gran/local` — 힘 · 접촉점) 에서 계산한다 (벽 접촉은 덤프에 없어 둘 다 빠진다 — 같은 조건).
      ① 재현: 접촉 덤프의 50/50 합이 `c_strs` 와 같은가 (부호 = −virial)
      ② 웹앱 정의 (대각 성분 VM · 상 평균 / 전체 평균 · CV) 를 두 규약에서 낸다

  (B) 협착 분율 (`bulk_resistance_fraction` — `network_conductivity.run_decomposition`):
      접촉 (간선) 마다 R_bulk/(R_bulk + R_c) 를 내고 **비가중 평균** (원장 `L2-08` — 이름표만 고쳤다).
      같은 망 해의 전력 (I²R) 가중 몫 Σ I²R_c / Σ I²R_total (관통 간선 · 가상 전극 제외) 과 맞댄다.
      입력 = `network_conductivity.py --dump-raw-dir` 의 `edges_<모드>_<채널>.csv` + 그 런의 결과 JSON.

  python3 scripts/lhs_stress_constriction_audit.py --selftest
  python3 scripts/lhs_stress_constriction_audit.py                       # (A) real_14 기준 상태 (리포 docs/data/real14_reference_20260928)
  python3 scripts/lhs_stress_constriction_audit.py --atoms A --contacts C --type-map 1:AM_P,2:AM_S,3:SE
  python3 scripts/lhs_stress_constriction_audit.py --network-dir OUT      # (B) OUT/raw/edges_*.csv + OUT/network_conductivity_<모드>.json
  # (B) 를 리포만으로 재현 (real_14):
  python3 scripts/lhs_stress_constriction_audit.py --prepare-network OUT   # OUT/atoms.csv · contacts.csv · mesh_info.json
  python3 scripts/network_conductivity.py OUT/atoms.csv OUT/contacts.csv -o OUT -t 1:AM_P,2:AM_S,3:SE -s 1000 --contact-mode both --dump-raw-dir OUT/raw
  python3 scripts/lhs_stress_constriction_audit.py --network-dir OUT
"""
import argparse
import csv
import gzip
import json
import math
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(ROOT, 'docs', 'data', 'real14_reference_20260928')
REF_ATOMS = os.path.join(REF, 'atom_2060000.liggghts.gz')
REF_CONTACTS = os.path.join(REF, 'contact_2060000.liggghts.gz')
REF_TYPES = '1:AM_P,2:AM_S,3:SE'          # input_real_14.liggghts: atom_type 1 = r_AM_P · 2 = r_AM_S · 3 = r_SE
CHANNELS = (('ionic', 'bulk_resistance_fraction'), ('electronic', 'electronic_bulk_frac'), ('thermal', 'thermal_bulk_frac'))


# ── 덤프 읽기 (마지막 블록 · 프레임 둘 이상이면 거부 — DESC-06) ─────────────────────
def _open(path):
    return gzip.open(path, 'rt') if path.endswith('.gz') else open(path)


def read_dump(path, item):
    """item = 'ATOMS' · 'ENTRIES' → (열 이름, 배열, 상자 [[lo, hi]] × 3).  블록이 둘 이상이면 ValueError."""
    with _open(path) as fh:
        lines = fh.read().splitlines()
    heads = [k for k, l in enumerate(lines) if l.startswith('ITEM: ' + item)]
    if len(heads) != 1:
        raise ValueError(f'{os.path.basename(path)}: ITEM: {item} 블록 {len(heads)} 개 — 한 프레임만 받는다 (DESC-06)')
    k = heads[0]
    cols = lines[k].split()[2:]
    box = []
    for j, l in enumerate(lines[:k]):
        if l.startswith('ITEM: BOX BOUNDS'):
            box = [[float(v) for v in lines[j + 1 + d].split()[:2]] for d in range(3)]
    rows = [l.split() for l in lines[k + 1:] if l.strip() and not l.startswith('ITEM')]
    data = np.array(rows, dtype=float) if rows else np.zeros((0, len(cols)))
    return cols, data, box


# ── (A) 입자 응력 두 규약 ─────────────────────────────────────────────────────────
def per_particle_virials(pos, i1, i2, F, cp, box_len):
    """접촉 목록 → 원자별 virial 대각 (xx, yy, zz) 두 규약.
    sym  = 0.5 · (x_i − x_j) ⊗ F_i  (두 원자 같은 값 — LIGGGHTS stress/atom 의 입자 접촉 몫)
    brch = (x_c − x_i) ⊗ F_i  ·  (x_c − x_j) ⊗ (−F_i)  (Love–Weber)
    box_len = (Lx, Ly, None) — 주기 축만 최소영상."""
    n = len(pos)

    def mi(d):
        d = d.copy()
        for ax in (0, 1):
            L = box_len[ax]
            if L:
                d[:, ax] -= L * np.round(d[:, ax] / L)
        return d
    dl = mi(pos[i1] - pos[i2])
    sym = np.zeros((n, 3))
    np.add.at(sym, i1, 0.5 * dl * F)
    np.add.at(sym, i2, 0.5 * dl * F)
    brch = np.zeros((n, 3))
    np.add.at(brch, i1, mi(cp - pos[i1]) * F)
    np.add.at(brch, i2, mi(cp - pos[i2]) * (-F))
    return sym, brch


def webapp_stress_summary(stress, typ, type_names):
    """`calc_von_mises_stress` 와 같은 정의 — 대각 성분 VM · CV (%) · 상 평균 / 전체 평균."""
    sxx, syy, szz = stress[:, 0], stress[:, 1], stress[:, 2]
    vm = np.sqrt(np.maximum(sxx ** 2 + syy ** 2 + szz ** 2 - sxx * syy - syy * szz - sxx * szz, 0.0))
    mean = float(vm.mean())
    out = {'stress_cv': float(vm.std() / mean * 100) if mean > 0 else 0.0}
    for t, nm in type_names.items():
        m = typ == t
        if m.any():
            out[f'stress_ratio_{nm}'] = float(vm[m].mean() / mean) if mean > 0 else 0.0
    return out


def audit_stress(atoms_path, contacts_path, type_map):
    ac, ad, box = read_dump(atoms_path, 'ATOMS')
    cc, cd, _ = read_dump(contacts_path, 'ENTRIES')
    ix = {c: k for k, c in enumerate(ac)}
    need = ['id', 'type', 'x', 'y', 'z', 'radius', 'c_strs[1]', 'c_strs[2]', 'c_strs[3]']
    miss = [c for c in need if c not in ix]
    if miss:
        raise ValueError(f'원자 덤프에 열 없음: {miss}')
    if len(cc) < 26:
        raise ValueError('접촉 덤프 열 < 26 (pos id force force_normal force_tangential torque contactArea delta contactPoint)')
    ids = ad[:, ix['id']].astype(int)
    row = {a: k for k, a in enumerate(ids)}
    typ = ad[:, ix['type']].astype(int)
    pos = ad[:, [ix['x'], ix['y'], ix['z']]]
    rad = ad[:, ix['radius']]
    vol = 4.0 / 3.0 * np.pi * rad ** 3
    cstr = ad[:, [ix['c_strs[1]'], ix['c_strs[2]'], ix['c_strs[3]']]]
    i1 = np.array([row[int(a)] for a in cd[:, 6]])
    i2 = np.array([row[int(a)] for a in cd[:, 7]])
    F, cp = cd[:, 9:12], cd[:, 23:26]
    Lx = box[0][1] - box[0][0] if box else None
    Ly = box[1][1] - box[1][0] if box else None
    sym, brch = per_particle_virials(pos, i1, i2, F, cp, (Lx, Ly, None))
    nz = np.abs(cstr).sum(1) > 0
    with np.errstate(divide='ignore', invalid='ignore'):
        rep = np.where(np.abs(cstr[nz]) > 0, -sym[nz] / cstr[nz], np.nan)
    deg = np.bincount(np.r_[i1, i2], minlength=len(ids))
    out = {
        'n_atoms': int(len(ids)), 'n_contacts': int(len(cd)),
        'n_by_type': {type_map.get(int(t), str(t)): int((typ == t).sum()) for t in sorted(set(typ.tolist()))},
        'repro_median_ratio_xx_yy_zz': [round(float(v), 6) for v in np.nanmedian(rep, 0)],
        'n_atoms_no_contact': int((deg == 0).sum()),
        'total_virial_sym_over_branch': [round(float(v), 6) for v in (sym.sum(0) / brch.sum(0))],
        'webapp_50_50': webapp_stress_summary(cstr / vol[:, None], typ, type_map),
        'love_weber_branch': webapp_stress_summary(-brch / vol[:, None], typ, type_map),
        'n_floor_touching': {type_map.get(int(t), str(t)): int((((pos[:, 2] - rad) < 1e-4) & (typ == t)).sum())
                             for t in sorted(set(typ.tolist()))},
    }
    return out


# ── (B) 협착 분율: 비가중 평균 vs 전력 가중 ─────────────────────────────────────────
def constriction_shares(edge_rows):
    """간선 기록 [{I, R_bulk, R_constr, R_total}] → (비가중 평균 R_c/R_total, Σ I²R_c / Σ I²R_total)."""
    rc = np.array([float(r['R_constr']) for r in edge_rows])
    rt = np.array([float(r['R_total']) for r in edge_rows])
    I = np.array([float(r['I']) for r in edge_rows])
    ok = rt > 0
    uw = float(np.mean(rc[ok] / rt[ok])) if ok.any() else float('nan')
    P = float(np.sum(I[ok] ** 2 * rt[ok]))
    w = float(np.sum(I[ok] ** 2 * rc[ok]) / P) if P > 0 else float('nan')
    return uw, w


def audit_network(net_dir):
    out = {}
    for mode in ('hertzian', 'physics'):
        jp = os.path.join(net_dir, f'network_conductivity_{mode}.json')
        res = json.load(open(jp)) if os.path.exists(jp) else {}
        for ch, key in CHANNELS:
            ep = os.path.join(net_dir, 'raw', f'edges_{mode}_{ch}.csv')
            if not os.path.exists(ep):
                continue
            rows = list(csv.DictReader(open(ep)))
            uw, w = constriction_shares(rows)
            bf = res.get(key)
            out[f'{mode}/{ch}'] = {'reported_1_minus_bulk_frac_all_edges': None if bf is None else round(1 - bf, 4),
                                   'unweighted_perc_edges': round(uw, 4), 'power_weighted_I2R': round(w, 4),
                                   'n_perc_edges': len(rows)}
    return out


REF_MESH = os.path.join(REF, 'mesh_2060000.stl')


def prepare_network_inputs(atoms_path, contacts_path, mesh_path, out_dir):
    """덤프 (.gz 가능) → 망 CLI 입력 (atoms.csv · contacts.csv · mesh_info.json) — 웹앱과 같은 파서 (`parse_liggghts`)."""
    import tempfile
    sys.path.insert(0, os.path.join(ROOT, 'scripts'))
    import pandas as pd
    import parse_liggghts as PL
    os.makedirs(out_dir, exist_ok=True)

    def _plain(path):                       # 파서는 평문만 읽는다 → .gz 는 임시 파일로
        if not path.endswith('.gz'):
            return path, None
        fd, tmp = tempfile.mkstemp(suffix='.liggghts')
        with os.fdopen(fd, 'w') as fh, gzip.open(path, 'rt') as src:
            fh.write(src.read())
        return tmp, tmp
    a_path, a_tmp = _plain(atoms_path)
    c_path, c_tmp = _plain(contacts_path)
    try:
        h, rows = PL.parse_atom_file(a_path)
        pd.DataFrame(rows, columns=h).to_csv(os.path.join(out_dir, 'atoms.csv'), index=False)
        h, rows = PL.parse_contact_file(c_path)
        pd.DataFrame(rows, columns=h).to_csv(os.path.join(out_dir, 'contacts.csv'), index=False)
    finally:
        for t in (a_tmp, c_tmp):
            if t:
                os.unlink(t)
    pz, _tri = PL.parse_mesh_stl(mesh_path)
    with open(os.path.join(out_dir, 'mesh_info.json'), 'w') as fh:
        json.dump({'plate_z': pz}, fh)
    return pz


# ── 셀프테스트 (반례 먼저 — 정의를 손으로 푼 값과 맞댄다) ──────────────────────────────
def selftest():
    ok = 0
    fails = []

    def chk(name, cond, detail=''):
        nonlocal ok
        print(('  PASS  ' if cond else '  FAIL  ') + name + ('' if cond else f'  ({detail})'))
        if cond:
            ok += 1
        else:
            fails.append(name)

    # S1 크기가 다른 두 구 (r_i = 6 · r_j = 1 · 겹침 δ = 0.1) · 힘 F (i 를 밀어내는 방향 = +x)
    ri, rj, dlt, Fm = 6.0, 1.0, 0.1, 2.0
    d = ri + rj - dlt
    pos = np.array([[d, 0.0, 0.0], [0.0, 0.0, 0.0]])          # i 가 +x 쪽
    cp = np.array([[d - (ri - dlt / 2), 0.0, 0.0]])            # 접촉점 = 교차면 근사 (i 에서 ri − δ/2)
    F = np.array([[Fm, 0.0, 0.0]])
    sym, brch = per_particle_virials(pos, np.array([0]), np.array([1]), F, cp, (None, None, None))
    chk('S1a 50/50: 두 원자 virial xx = 0.5·d·F 로 같다 (크기 무관)',
        abs(sym[0, 0] - 0.5 * d * Fm) < 1e-12 and abs(sym[1, 0] - 0.5 * d * Fm) < 1e-12, sym[:, 0])
    chk('S1b branch: 큰 입자 = (ri − δ/2)·F · 작은 입자 = (rj − δ/2)·F (부호 −)',
        abs(-brch[0, 0] - (ri - dlt / 2) * Fm) < 1e-12 and abs(-brch[1, 0] - (rj - dlt / 2) * Fm) < 1e-12, brch[:, 0])
    chk('S1c 총 virial 은 두 규약이 같다 (부호만 반대)', abs(sym.sum(0)[0] + brch.sum(0)[0]) < 1e-12, (sym.sum(0), brch.sum(0)))
    chk('S1d 50/50 ÷ branch = d / (2(r − δ/2)) — 큰 입자 0.575 배 · 작은 입자 7.21 배',
        abs(sym[0, 0] / -brch[0, 0] - d / (2 * (ri - dlt / 2))) < 1e-12 and abs(sym[1, 0] / -brch[1, 0] - d / (2 * (rj - dlt / 2))) < 1e-12)

    # S2 같은 크기 사슬 (r = 1 · 세 구 · 양 끝에서 같은 힘) — 두 규약이 같은 입자 응력을 낸다 (크기 효과 없음)
    r, dl2 = 1.0, 0.02
    p3 = np.array([[0.0, 0, 0], [2 - dl2, 0, 0], [2 * (2 - dl2), 0, 0]])
    i1, i2 = np.array([1, 2]), np.array([0, 1])
    F3 = np.array([[Fm, 0, 0], [Fm, 0, 0]])                    # 1 이 0 에서 +x 로 밀림 · 2 가 1 에서 +x 로 밀림
    cp3 = np.array([[1 - dl2 / 2, 0, 0], [3 - 1.5 * dl2, 0, 0]])
    s3, b3 = per_particle_virials(p3, i1, i2, F3, cp3, (None, None, None))
    chk('S2 같은 크기: 가운데 입자는 두 규약 응력이 같다', abs(s3[1, 0] + b3[1, 0]) < 1e-12, (s3[1, 0], b3[1, 0]))

    # S3 주기 경계 너머 접촉 — 최소영상으로 delta 가 짧은 쪽
    L = 10.0
    pp = np.array([[0.4, 5, 5], [9.6, 5, 5]])                  # 실제 거리 0.8 (경계 너머)
    s4, _ = per_particle_virials(pp, np.array([0]), np.array([1]), np.array([[1.0, 0, 0]]), np.array([[0.0, 5, 5]]), (L, L, None))
    chk('S3 주기 최소영상 — 0.5·0.8·1 = 0.4 (상자 길이 9.2 가 아님)', abs(s4[0, 0] - 0.4) < 1e-12, s4[0, 0])

    # S4 웹앱 정의 재현 — 한 상이 다른 상보다 두 배 VM 이면 비 = 2·N/(N_a + 2 N_b) …
    st = np.array([[1.0, 0, 0], [1.0, 0, 0], [2.0, 0, 0]])
    sm = webapp_stress_summary(st, np.array([3, 3, 1]), {1: 'AM_P', 3: 'SE'})
    chk('S4 상 비 = 상 평균 / 전체 평균 (AM_P 2/(4/3) = 1.5 · SE 0.75)',
        abs(sm['stress_ratio_AM_P'] - 1.5) < 1e-12 and abs(sm['stress_ratio_SE'] - 0.75) < 1e-12, sm)

    # S5 L2-08 반례 그대로 — 병렬 두 경로 × 직렬 두 간선 · R_bulk = 1 · A 경로 R_c = 9 · B 경로 R_c = 0 · 전압 1
    #     A: 간선 R = 10 둘 직렬 → I = 1/20 · B: R = 1 둘 → I = 1/2
    rows = [{'I': 1 / 20, 'R_bulk': 1, 'R_constr': 9, 'R_total': 10}] * 2 + [{'I': 1 / 2, 'R_bulk': 1, 'R_constr': 0, 'R_total': 1}] * 2
    uw, w = constriction_shares(rows)
    chk('S5 L2-08 반례: 비가중 협착 몫 45 % · 전력 가중 8.1818 %',
        abs(uw - 0.45) < 1e-12 and abs(w - 0.0818181818) < 1e-9, (uw, w))

    # S6 프레임 둘 이상 = 거부 (DESC-06)
    import tempfile
    with tempfile.NamedTemporaryFile('w', suffix='.liggghts', delete=False) as fh:
        fh.write('ITEM: TIMESTEP\n0\nITEM: ATOMS id type\n1 1\nITEM: TIMESTEP\n1\nITEM: ATOMS id type\n1 1\n')
        two = fh.name
    try:
        read_dump(two, 'ATOMS')
        refused = False
    except ValueError:
        refused = True
    os.unlink(two)
    chk('S6 원자 덤프에 프레임 둘 = 거부 (DESC-06)', refused)

    print(f'\n{ok} PASS · {len(fails)} FAIL')
    return 0 if not fails else 1


def main():
    ap = argparse.ArgumentParser(description='LHS 감사 묶음 ④ — σ_VM 규약 · 협착 분율 정의 (읽기 전용)')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--atoms', default=REF_ATOMS)
    ap.add_argument('--contacts', default=REF_CONTACTS)
    ap.add_argument('--type-map', default=REF_TYPES)
    ap.add_argument('--network-dir', default=None, help='network_conductivity.py -o OUT --dump-raw-dir OUT/raw 의 OUT')
    ap.add_argument('--json', default=None, help='결과 JSON 저장 경로')
    ap.add_argument('--mesh', default=REF_MESH, help='판 메시 (plate_z) — --prepare-network 용')
    ap.add_argument('--prepare-network', default=None, metavar='OUT', help='망 CLI 입력을 OUT 에 쓰고 끝낸다')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.prepare_network:
        pz = prepare_network_inputs(a.atoms, a.contacts, a.mesh, a.prepare_network)
        print(f'망 입력 → {a.prepare_network} (plate_z {pz})')
        return 0
    tm = {int(k): v.strip() for k, v in (p.split(':') for p in a.type_map.split(','))}
    out = {'stress': audit_stress(a.atoms, a.contacts, tm)}
    if a.network_dir:
        out['constriction'] = audit_network(a.network_dir)
    print(json.dumps(out, ensure_ascii=False, indent=1))
    if a.json:
        with open(a.json, 'w', encoding='utf-8') as fh:
            json.dump(out, fh, ensure_ascii=False, indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
