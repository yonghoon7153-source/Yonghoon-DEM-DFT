#!/usr/bin/env python3
"""LHS · lhsx 침대의 porosity — 구 부피 합 (sphere) · 겹침 보정 (union) 을 **전부** 뽑는다 (읽기 전용).

  REPO=~/dem-web ~/Yonghoon-DEM-DFT/venv/bin/python3 lhs_union_webapp.py --cohort <코호트 TSV> --out x.tsv [--mc-n 4000000]
  python3 lhs_union_webapp.py --selftest

케이스마다 세 가지 union 을 낸다:
  ① 웹앱 그대로 — scripts/dem_analysis_core.calc_porosity (sphere) · calc_porosity_dual (쌍 렌즈 union · 겹침 %).
     원자 · 접촉 파싱도 웹앱 파서 (scripts/parse_liggghts).  ⚠ 쌍 렌즈만 뺀다 (세 입자 겹침을 되돌리지 않음 — 공극을 키우는 쪽)
     그리고 벽 밖 부피를 안 뺀다 (공극을 줄이는 쪽) ⇒ ① 은 상한이 **아니다** — 실측 194/194 건 ① < ③ (중앙 −0.64 %p · lhsx −0.75 %p ·
     docs/data/lhs_union_20260927/).  상한은 ② 다 (`SELF-72` · 09-30 정정 — 옛 판은 ① 을 "공극 상한" 이라 적었다).
  ② ① 에서 벽 밖 부피 (바닥 z < 0 · 플래튼 위) 를 뺀 값 (clipped).
  ③ **정확한 union** — 상자 안 [0,Lx)×[0,Ly)×[0,plate_z) 에 무작위 점 N 개를 뿌려 어느 구에도 안 든 비율 (x · y 주기).
     세 입자 이상 겹침까지 정확하다 (통계 오차만 — 열 `mc_void_se_pct`).  같은 점으로 SE 만 · AM 만 · 둘 다 덮인 부피도 낸다
     ⇒ φ 를 union 기준으로 나누는 규칙을 나중에 정해도 다시 돌릴 필요가 없다.
구 부피 합 쪽: φ_SE · φ_AM (sphere) · 쌍 렌즈 부피를 상 쌍 (SE–SE · AM–SE · AM–AM) 별 상자 대비 % 로.
검산: 접촉 덤프 delta 열 (c_cpl[23]) ↔ 원자 좌표로 잰 겹침 (1 % 넘으면 DELTA_MISMATCH — union 을 믿지 않는다) ·
      웹앱 sphere ↔ dual sphere · 쌍 렌즈 재계산 ↔ 웹앱 V_lens · ③ ≤ ② (쌍 렌즈는 상한 — 어기면 pair_upper_bound_ok False =
      접촉 덤프에 겹친 쌍이 빠졌다는 뜻.  ③ 은 원자만 쓰므로 그래도 유효).
플래튼 · 파일 = 수확기 규약 (lhs_harvest_batch.pick_mesh 같은 step 만 · plate_z_from_stl 평판 검사) · 한 프레임 파일만 받는다.
⛔ 아무 파일도 고치지 않는다 — 출력은 --out 하나.
"""
import argparse
import csv
import math
import os
import re
import sys
import time
import zlib
from pathlib import Path

import numpy as np

REPO = Path(os.environ.get('REPO') or Path(__file__).resolve().parents[1]).expanduser().resolve()
sys.path.insert(0, str(REPO / 'scripts'))

TYPE_MAP = {2: {1: 'AM', 2: 'SE'}, 3: {1: 'AM_P', 2: 'AM_S', 3: 'SE'}}
# 검산 ① 문턱: delta 열 ↔ 좌표 겹침 차 / r_min.  덤프 인쇄 정밀도 (%g · 6 자리) 로 생기는 차는 ~1e-3 이하 — 1 % 를 넘으면 열 · 시점 불일치
DELTA_TOL = 0.01
MC_CHUNK = 1_000_000
MAX_RADIUS_GROUPS = 24
PROFILE_BINS = 10          # z 방향 공극 분포 칸 (바닥 → 플래튼)


def _count(path, token):
    n = 0
    with open(path, 'r', encoding='utf-8', errors='replace') as fh:
        for ln in fh:
            if ln.startswith(token):
                n += 1
    return n


def _box_xy(path):
    with open(path, 'r', encoding='utf-8', errors='replace') as fh:
        lines = fh.readlines()
    for i, ln in enumerate(lines):
        if ln.startswith('ITEM: BOX BOUNDS'):
            xs = [float(v) for v in lines[i + 1].split()[:2]]
            ys = [float(v) for v in lines[i + 2].split()[:2]]
            return xs[0], xs[1] - xs[0], ys[0], ys[1] - ys[0], ln.replace('ITEM: BOX BOUNDS', '').split()[-3:]
    raise ValueError(f'{path}: BOX BOUNDS 없음')


def _cap(r, h):
    h = np.clip(h, 0.0, 2.0 * r)
    return math.pi * h * h * (3.0 * r - h) / 3.0


def _lens(r1, r2, dl):
    """dem_analysis_core.calc_porosity_dual 과 같은 식 (벡터)."""
    dd = r1 + r2 - dl
    ok = (dl > 0) & (dd > 0)
    dds = np.where(ok, dd, 1.0)
    v = (np.pi * dl ** 2 / (12 * dds)) * (dds ** 2 + 2 * dds * (r1 + r2) - 3 * (r1 - r2) ** 2)
    return np.where(ok & (v > 0), v, 0.0)


def _query(tree, Q, r):
    try:
        d, _ = tree.query(Q, k=1, distance_upper_bound=r, workers=-1)
    except TypeError:                                   # scipy < 1.6
        d, _ = tree.query(Q, k=1, distance_upper_bound=r)
    return d < r


def coverage(X, R, isSE, x0, lx, y0, ly, Q):
    """점 Q (상자 좌표) 가 SE 구 · AM 구에 드는지 — x · y 주기, z 비주기.  반경별로 KD 트리를 따로 만든다."""
    from scipy.spatial import cKDTree
    rmax = float(R.max())
    zoff = max(0.0, -float((X[:, 2] - R).min()), -float(Q[:, 2].min())) + rmax
    BZ = float(max((X[:, 2] + R).max(), Q[:, 2].max())) + zoff + 4.0 * rmax + 1.0 * (lx + ly)   # z 는 사실상 비주기
    P = np.empty_like(X)
    P[:, 0] = np.mod(X[:, 0] - x0, lx)
    P[:, 1] = np.mod(X[:, 1] - y0, ly)
    P[:, 0] = np.where(P[:, 0] >= lx, 0.0, P[:, 0])
    P[:, 1] = np.where(P[:, 1] >= ly, 0.0, P[:, 1])
    P[:, 2] = X[:, 2] + zoff
    q = np.empty_like(Q)
    q[:, 0] = np.mod(Q[:, 0] - x0, lx)
    q[:, 1] = np.mod(Q[:, 1] - y0, ly)
    q[:, 0] = np.where(q[:, 0] >= lx, 0.0, q[:, 0])
    q[:, 1] = np.where(q[:, 1] >= ly, 0.0, q[:, 1])
    q[:, 2] = Q[:, 2] + zoff
    rk = np.array([float('%.9g' % r) for r in R])
    cov = {}
    for name, pm in (('SE', isSE), ('AM', ~isSE)):
        c = np.zeros(len(Q), dtype=bool)
        groups = np.unique(rk[pm]) if pm.any() else []
        if len(groups) > MAX_RADIUS_GROUPS:
            raise ValueError(f'{name} 반경 종류 {len(groups)} > {MAX_RADIUS_GROUPS} — 다분산은 이 방식으로 안 한다')
        for rg in groups:
            m = pm & (rk == rg)
            tree = cKDTree(P[m], boxsize=[lx, ly, BZ])
            c |= _query(tree, q, float(R[m].max()))
        cov[name] = c
    return cov['SE'], cov['AM']


def one(atom_path, contact_path, mesh_path, n_types, mc_n, seed, margin_d=2.0):
    import dem_analysis_core as WEB
    import lhs_descriptor_harvest as HV
    import parse_liggghts as PL
    nf_a, nf_c = _count(atom_path, 'ITEM: TIMESTEP'), _count(contact_path, 'ITEM: ENTRIES')
    if nf_a != 1 or nf_c != 1:        # 웹앱 파서는 프레임을 이어 붙인다 (DESC-06) — 한 프레임 파일만 받는다
        raise ValueError(f'프레임 수 atom {nf_a} · contact {nf_c} (1 이어야)')
    plate_z = HV.plate_z_from_stl(str(mesh_path))
    x0, lx, y0, ly, bc = _box_xy(atom_path)
    if abs(lx - ly) > 1e-12:
        raise ValueError(f'상자가 정사각형이 아니다 lx {lx} ly {ly} (웹앱 V_box = box_xy²·plate_z)')
    ha, ra = PL.parse_atom_file(str(atom_path))
    ia = {c: ha.index(c) for c in ('id', 'x', 'y', 'z', 'radius', 'type')}
    atoms = {}
    for v in ra:
        atoms[int(float(v[ia['id']]))] = {'x': float(v[ia['x']]), 'y': float(v[ia['y']]), 'z': float(v[ia['z']]),
                                          'radius': float(v[ia['radius']]), 'type': int(float(v[ia['type']]))}
    del ra
    hc, rc = PL.parse_contact_file(str(contact_path))
    i1, i2, idl = hc.index('id1'), hc.index('id2'), hc.index('delta')
    contacts = [{'id1': int(float(v[i1])), 'id2': int(float(v[i2])), 'delta': float(v[idl])} for v in rc]
    del rc

    eps_web = float(WEB.calc_porosity(atoms, plate_z, box_xy=lx))
    dual = WEB.calc_porosity_dual(atoms, contacts, plate_z, box_xy=lx)
    V_box = float(dual['V_box_sim'])
    V_sum = float(dual['V_sphere_sum_sim'])
    V_lens_web = float(dual['V_lens_total_sim'])

    ids = np.fromiter(atoms.keys(), dtype=np.int64)
    ids_s = np.sort(ids)
    X = np.array([[atoms[k]['x'], atoms[k]['y'], atoms[k]['z']] for k in ids_s])
    R = np.array([atoms[k]['radius'] for k in ids_s])
    T = np.array([atoms[k]['type'] for k in ids_s])
    tmap = TYPE_MAP[n_types]
    bad_t = sorted(set(int(t) for t in np.unique(T)) - set(tmap))
    if bad_t:
        raise ValueError(f'선언 밖 type {bad_t}')
    isSE = np.array([tmap[int(t)] == 'SE' for t in T])
    c1 = np.array([c['id1'] for c in contacts], dtype=np.int64)
    c2 = np.array([c['id2'] for c in contacts], dtype=np.int64)
    dl = np.array([c['delta'] for c in contacts], dtype=np.float64)
    del contacts
    j1 = np.clip(np.searchsorted(ids_s, c1), 0, len(ids_s) - 1)
    j2 = np.clip(np.searchsorted(ids_s, c2), 0, len(ids_s) - 1)
    ok = (ids_s[j1] == c1) & (ids_s[j2] == c2)
    n_missing = int((~ok).sum())
    j1, j2, dl = j1[ok], j2[ok], dl[ok]
    d = X[j1] - X[j2]
    d[:, 0] -= lx * np.round(d[:, 0] / lx)
    d[:, 1] -= ly * np.round(d[:, 1] / ly)
    r1, r2 = R[j1], R[j2]
    rel = np.abs(dl - (r1 + r2 - np.sqrt((d * d).sum(1)))) / np.minimum(r1, r2)
    lens = _lens(r1, r2, dl)
    s1, s2 = isSE[j1], isSE[j2]
    kinds = {'SE_SE': s1 & s2, 'AM_SE': s1 ^ s2, 'AM_AM': ~s1 & ~s2}
    V_lens = float(lens.sum())
    V_SE = float((4.0 / 3.0 * np.pi * R[isSE] ** 3).sum())
    V_AM = float((4.0 / 3.0 * np.pi * R[~isSE] ** 3).sum())

    z = X[:, 2]
    lo_m, hi_m = (z - R) < 0, (z + R) > plate_z
    cap_lo = np.where(lo_m, _cap(R, R - z), 0.0)
    cap_hi = np.where(hi_m, _cap(R, z + R - plate_z), 0.0)
    V_out = float(cap_lo.sum() + cap_hi.sum())

    rec = dict(
        n_atoms=len(ids_s), n_SE=int(isSE.sum()), n_AM=int((~isSE).sum()), n_contacts=int(len(dl) + n_missing),
        n_contact_id_missing=n_missing, bc='/'.join(bc),
        thickness_um=plate_z * 1e3, lx_um=lx * 1e3, se_of_solid_vol=V_SE / V_sum,
        # ── sphere (웹앱 주 값) ──
        eps_sphere_web=eps_web, eps_sphere_dual=float(dual['porosity_spheresum']),
        phi_se_sphere=V_SE / V_box, phi_am_sphere=V_AM / V_box,
        # ── ① 쌍 렌즈 union (웹앱) ──
        eps_union_web=float(dual['porosity_union']), overlap_fraction_pct_web=float(dual['overlap_fraction_pct']),
        lens_over_Vbox_pct=100.0 * V_lens_web / V_box,
        lens_SE_SE_over_Vbox_pct=100.0 * float(lens[kinds['SE_SE']].sum()) / V_box,
        lens_AM_SE_over_Vbox_pct=100.0 * float(lens[kinds['AM_SE']].sum()) / V_box,
        lens_AM_AM_over_Vbox_pct=100.0 * float(lens[kinds['AM_AM']].sum()) / V_box,
        # ── ② 벽 밖 부피 · clipped ──
        out_floor_over_Vbox_pct=100.0 * float(cap_lo.sum()) / V_box,
        out_plate_over_Vbox_pct=100.0 * float(cap_hi.sum()) / V_box,
        out_SE_over_Vbox_pct=100.0 * float((cap_lo + cap_hi)[isSE].sum()) / V_box,
        out_AM_over_Vbox_pct=100.0 * float((cap_lo + cap_hi)[~isSE].sum()) / V_box,
        eps_sphere_clipped=100.0 * (1.0 - (V_sum - V_out) / V_box),
        eps_union_pair_clipped=100.0 * (1.0 - (V_sum - V_out - V_lens_web) / V_box),
    )
    for k, m in kinds.items():
        mm = m & (dl > 0)
        rec[f'n_{k}'] = int(m.sum())
        rec[f'delta_over_dmin_{k}_mean'] = float(np.mean(dl[mm] / (2 * np.minimum(r1[mm], r2[mm])))) if mm.any() else None
    rec['cn_SE_SE'] = 2.0 * rec['n_SE_SE'] / max(rec['n_SE'], 1)
    # ── 검산 ──
    rec['delta_col_vs_geom_max_rel'] = float(rel.max()) if rel.size else None
    rec['n_delta_nonpos'] = int((dl <= 0).sum())
    rec['lens_recomputed_rel_diff'] = abs(V_lens - V_lens_web) / max(V_lens_web, 1e-300)
    rec['sphere_web_minus_dual'] = eps_web - float(dual['porosity_spheresum'])
    # ── ③ 정확한 union (몬테카를로, 상자 안) ──
    if mc_n > 0:
        rng = np.random.default_rng(seed)
        nSE = nAM = nBoth = nVoid = 0
        done = 0
        #  ★ 벽 근처는 성기게 쌓인다 (벽 효과) — 얇은 침대에서는 그 몫이 커서 벌크 공극률을 부풀린다.
        #    바닥 · 플래튼에서 margin_d × d_SE 를 뺀 **내부** 공극률과 z 칸 분포를 같은 점으로 낸다.
        d_ref = 2.0 * float(np.median(R[isSE] if isSE.any() else R))
        mz = margin_d * d_ref
        nInt = nIntVoid = 0
        zb = np.zeros(PROFILE_BINS)
        zv = np.zeros(PROFILE_BINS)
        while done < mc_n:
            m = min(MC_CHUNK, mc_n - done)
            Q = rng.random((m, 3)) * np.array([lx, ly, plate_z]) + np.array([x0, y0, 0.0])
            cs, ca = coverage(X, R, isSE, x0, lx, y0, ly, Q)
            nSE += int((cs & ~ca).sum())
            nAM += int((ca & ~cs).sum())
            nBoth += int((cs & ca).sum())
            void = ~cs & ~ca
            nVoid += int(void.sum())
            zq = Q[:, 2]
            inside = (zq >= mz) & (zq <= plate_z - mz)
            nInt += int(inside.sum())
            nIntVoid += int((void & inside).sum())
            bi = np.minimum((zq / plate_z * PROFILE_BINS).astype(int), PROFILE_BINS - 1)
            zb += np.bincount(bi, minlength=PROFILE_BINS)
            zv += np.bincount(bi, weights=void.astype(float), minlength=PROFILE_BINS)
            done += m
        p = nVoid / mc_n
        rec.update(mc_n=mc_n, mc_seed=seed,
                   mc_void_pct=100.0 * p, mc_void_se_pct=100.0 * math.sqrt(p * (1 - p) / mc_n),
                   mc_SE_only_pct=100.0 * nSE / mc_n, mc_AM_only_pct=100.0 * nAM / mc_n, mc_both_pct=100.0 * nBoth / mc_n)
        pin = (nIntVoid / nInt) if nInt else None
        rec.update(mc_interior_margin_um=mz * 1e3, mc_interior_n=nInt,
                   mc_void_interior_pct=(100.0 * pin) if pin is not None else None,
                   mc_void_interior_se_pct=(100.0 * math.sqrt(pin * (1 - pin) / nInt)) if pin is not None else None,
                   mc_void_profile_pct=';'.join(f'{100.0 * v / b:.3f}' if b else 'nan' for v, b in zip(zv, zb)))
        rec['pair_minus_mc_void_pct'] = rec['eps_union_pair_clipped'] - rec['mc_void_pct']
        # 쌍 렌즈 union 은 정확 union 의 상한이다 (Bonferroni) — 4σ 넘게 아래면 접촉 덤프에서 겹친 쌍이 빠진 것 (합성 시험에서 실측)
        rec['pair_upper_bound_ok'] = bool(rec['pair_minus_mc_void_pct'] >= -4.0 * rec['mc_void_se_pct'])
    return rec


def scan_rows(root, n_types, family):
    """코호트 TSV 없이 런 폴더를 훑는다 — <root>/<case>/post*/ 에서 atom · contact · mesh 가 **같은 step** 으로 다 있는
    가장 늦은 step 을 고른다 (없으면 그 케이스는 MISSING 으로 남긴다)."""
    rows = []
    for cd in sorted(p for p in Path(root).iterdir() if p.is_dir()):
        best = None
        for post in sorted(cd.glob('post*')):
            if not post.is_dir():
                continue
            for ap_ in post.glob('atom_*.liggghts'):
                mm = re.fullmatch(r'atom_(\d+)\.liggghts', ap_.name)
                if not mm:
                    continue
                st = int(mm.group(1))
                cp = post / f'contact_{st}.liggghts'
                if cp.is_file() and (post / f'mesh_{st}.stl').is_file() and (best is None or st > best[0]):
                    best = (st, ap_, cp)
        rows.append(dict(case=cd.name, atom_file=str(best[1]) if best else str(cd / 'post_MISSING' / 'atom_0.liggghts'),
                         contact_file=str(best[2]) if best else str(cd / 'post_MISSING' / 'contact_0.liggghts'),
                         n_types=str(n_types), design_family=family))
    return rows


def run(a):
    import lhs_harvest_batch as HB
    rows = scan_rows(a.scan_root, a.n_types, a.family) if a.scan_root else HB.read_cohort(Path(a.cohort))
    if not rows:
        raise SystemExit('코호트 0 행 — 경로 · 형식 확인')
    out, t0 = [], time.time()
    for k, row in enumerate(rows, 1):
        case = row['case']
        if a.case and case not in a.case:
            continue
        rec = {'case': case, 'design_family': row.get('design_family'), 'n_types': row.get('n_types')}
        atom = HB.remap(row['atom_file'], a.root_from, a.root_to)
        contact = HB.remap(row['contact_file'], a.root_from, a.root_to)
        mesh, how, note = HB.pick_mesh(atom)
        if not atom.is_file() or not contact.is_file() or mesh is None or how != 'exact':
            rec.update(status='MISSING', note=f'atom {atom.is_file()} contact {contact.is_file()} mesh {how} {note}')
        else:
            try:
                rec.update(one(atom, contact, mesh, int(row['n_types']), a.mc_n, zlib.crc32(case.encode()), a.margin_d))
                bad = (rec.get('delta_col_vs_geom_max_rel') or 0.0) > DELTA_TOL or rec.get('n_contact_id_missing')
                rec['status'] = 'DELTA_MISMATCH' if bad else 'OK'
            except Exception as e:                                  # noqa: BLE001
                rec.update(status='ERROR', note=f'{type(e).__name__}: {e}'[:200])
        out.append(rec)
        nan = float('nan')
        print(f"[{k}/{len(rows)}] {case} {rec['status']}  sphere {rec.get('eps_sphere_web', nan):6.2f}  "
              f"union(쌍) {rec.get('eps_union_web', nan):6.2f}  union(정확) {rec.get('mc_void_pct', nan):6.2f}  "
              f"({time.time() - t0:.0f}s)", flush=True)
    keys = []
    for r in out:
        for kk in r:
            if kk not in keys:
                keys.append(kk)
    with open(a.out, 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=keys, delimiter='\t')
        w.writeheader()
        w.writerows(out)
    ok = [r for r in out if r['status'] == 'OK']
    print(f'→ {a.out}  OK {len(ok)} / {len(out)}')
    if ok:
        def med(key):
            v = sorted(r[key] for r in ok if r.get(key) is not None)
            return v[len(v) // 2] if v else float('nan')
        print(f"중앙: sphere {med('eps_sphere_web'):.2f} % · union 쌍 {med('eps_union_web'):.2f} % · 쌍 clipped "
              f"{med('eps_union_pair_clipped'):.2f} % · union 정확 {med('mc_void_pct'):.2f} % · 겹침/상자 {med('lens_over_Vbox_pct'):.2f} %")
        mx = [r['delta_col_vs_geom_max_rel'] for r in ok if r.get('delta_col_vs_geom_max_rel') is not None]
        print(f"검산: delta 열 ↔ 좌표 최대 {max(mx) if mx else float('nan'):.2e} · sphere 웹앱↔dual 최대 "
              f"{max(abs(r['sphere_web_minus_dual']) for r in ok):.1e} %p · 정확 union 음수 {sum(1 for r in ok if r.get('mc_void_pct', 0) < 0)} · "
              f"쌍 clipped < 정확 (상한 위반) {sum(1 for r in ok if r.get('pair_minus_mc_void_pct', 0) < -4 * r.get('mc_void_se_pct', 0))}")
    return 0 if len(ok) == len(out) else 1


def selftest():
    """합성 침대 셋 — 손계산 · 전수 대조로 확인한다."""
    import tempfile
    fails = []

    def chk(name, cond):
        print(('  ✓ ' if cond else '  ✗ ') + name)
        if not cond:
            fails.append(name)

    # (1) coverage() 를 전수 거리 계산과 대조 — 주기 x·y, 세 입자 겹침 포함 조밀 침대
    rng = np.random.default_rng(7)
    lx = ly = 0.02
    n = 1500
    X = np.c_[rng.random(n) * lx - 0.003, rng.random(n) * ly + 0.001, rng.random(n) * 0.012 - 0.001]
    R = np.where(rng.random(n) < 0.8, 0.001, 0.0025)
    isSE = R < 0.002
    Q = np.c_[rng.random(40000) * lx - 0.003, rng.random(40000) * ly + 0.001, rng.random(40000) * 0.01]
    cs, ca = coverage(X, R, isSE, -0.003, lx, 0.001, ly, Q)
    bs = np.zeros(len(Q), bool)
    ba = np.zeros(len(Q), bool)
    for i in range(n):
        dq = Q - X[i]
        dq[:, 0] -= lx * np.round(dq[:, 0] / lx)
        dq[:, 1] -= ly * np.round(dq[:, 1] / ly)
        inside = (dq * dq).sum(1) < R[i] ** 2
        if isSE[i]:
            bs |= inside
        else:
            ba |= inside
    chk('coverage() = 전수 거리 계산 (SE · AM 가림 40,000 점 전부 일치 · 주기 x·y)', np.array_equal(cs, bs) and np.array_equal(ca, ba))

    # (2) 두 구가 겹친 침대: 쌍 렌즈 union = 정확 union (세 입자 겹침 없음) — 몬테카를로가 4σ 안
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)

        def write_case(name, atoms, pairs, plate_z, swap=False):
            post = td / name / 'post'
            post.mkdir(parents=True)
            with open(post / 'atom_100.liggghts', 'w') as f:
                f.write(f'ITEM: TIMESTEP\n100\nITEM: NUMBER OF ATOMS\n{len(atoms)}\nITEM: BOX BOUNDS pp pp ff\n0 0.01\n0 0.01\n-0.01 0.05\n'
                        'ITEM: ATOMS id type x y z radius\n')
                for a in atoms:
                    f.write(' '.join(str(v) for v in a) + '\n')
            with open(post / 'contact_100.liggghts', 'w') as f:
                f.write(f'ITEM: TIMESTEP\n100\nITEM: NUMBER OF ENTRIES\n{len(pairs)}\nITEM: BOX BOUNDS pp pp ff\n0 0.01\n0 0.01\n-0.01 0.05\n'
                        'ITEM: ENTRIES ' + ' '.join(f'c_cpl[{i}]' for i in range(1, 27)) + '\n')
                for i1, i2, dd in pairs:
                    v = [0.0] * 26
                    v[6], v[7], v[21], v[22] = i1, i2, 1e-7, dd
                    if swap:
                        v[21], v[22] = v[22], v[21]
                    f.write(' '.join(str(x) for x in v) + '\n')
            with open(post / 'mesh_100.stl', 'w') as f:
                f.write('solid p\n')
                for tri in (((0, 0), (0.01, 0), (0.01, 0.01)), ((0, 0), (0.01, 0.01), (0, 0.01))):
                    f.write('facet normal 0 0 1\nouter loop\n' + ''.join(f'vertex {x} {y} {plate_z}\n' for x, y in tri) + 'endloop\nendfacet\n')
                f.write('endsolid p\n')
            return post

        # 두 SE (r 1 µm) — 하나는 주기 경계를 넘어 다른 하나와 겹친다 · AM (r 2.5 µm) 하나는 바닥 밑으로 0.5 µm
        atoms = [(1, 3, 0.0095, 0.005, 0.003, 0.001), (2, 3, 0.0008, 0.005, 0.003, 0.001), (3, 1, 0.005, 0.005, 0.002, 0.0025)]
        dlt = 0.001 + 0.001 - 0.0013
        post = write_case('two', atoms, [(1, 2, dlt)], 0.006)
        r = one(post / 'atom_100.liggghts', post / 'contact_100.liggghts', post / 'mesh_100.stl', 3, 3_000_000, 11)
        vb = 0.01 * 0.01 * 0.006
        lens = math.pi * dlt ** 2 * (6 * 0.001 - dlt) / 12
        vs = 2 * 4 / 3 * math.pi * 0.001 ** 3 + 4 / 3 * math.pi * 0.0025 ** 3
        cap = math.pi * 0.0005 ** 2 * (3 * 0.0025 - 0.0005) / 3
        want_sphere = 100 * (1 - vs / vb)
        want_union_clip = 100 * (1 - (vs - lens - cap) / vb)
        chk(f'sphere = 손계산 ({r["eps_sphere_web"]:.6f} vs {want_sphere:.6f})', abs(r['eps_sphere_web'] - want_sphere) < 1e-9)
        chk(f'쌍 렌즈 clipped = 손계산 ({r["eps_union_pair_clipped"]:.6f} vs {want_union_clip:.6f})', abs(r['eps_union_pair_clipped'] - want_union_clip) < 1e-9)
        chk(f'정확 union (MC) = 손계산 4σ 안 ({r["mc_void_pct"]:.4f} ± {r["mc_void_se_pct"]:.4f} vs {want_union_clip:.4f})',
            abs(r['mc_void_pct'] - want_union_clip) < 4 * r['mc_void_se_pct'])
        chk('delta 열 ↔ 좌표 (주기 경계 넘는 쌍) 일치', r['delta_col_vs_geom_max_rel'] < 1e-9)
        chk('벽 밖 부피 = AM 캡 손계산', abs(r['out_floor_over_Vbox_pct'] - 100 * cap / vb) < 1e-9 and r['out_AM_over_Vbox_pct'] > 0)
        chk('SE–SE 렌즈 몫 = 전부', abs(r['lens_SE_SE_over_Vbox_pct'] - 100 * lens / vb) < 1e-9 and r['lens_AM_SE_over_Vbox_pct'] == 0)
        prof = [float(v) for v in r['mc_void_profile_pct'].split(';')]
        chk(f'z 분포: 맨 위 칸 (z > 5.4 µm, 고체 없음) = 100 % · 칸 평균 ≈ 전체 ({sum(prof) / len(prof):.3f} vs {r["mc_void_pct"]:.3f})',
            len(prof) == PROFILE_BINS and abs(prof[-1] - 100.0) < 1e-9 and abs(sum(prof) / len(prof) - r['mc_void_pct']) < 0.2)
        chk('내부 공극률: 여백 2 d_SE (4 µm) × 2 > 두께 6 µm → 없음 (None)', r['mc_void_interior_pct'] is None)
        r1 = one(post / 'atom_100.liggghts', post / 'contact_100.liggghts', post / 'mesh_100.stl', 3, 500_000, 11, margin_d=0.5)
        chk(f'내부 공극률: 여백 0.5 d_SE → 값 있음 ({r1["mc_void_interior_pct"]:.3f} %)',
            r1['mc_void_interior_pct'] is not None and 0.0 < r1['mc_void_interior_pct'] < 100.0 and r1['mc_interior_n'] > 0)
        # --scan-root: 늦은 step 중 atom · contact · mesh 가 다 있는 것을 고른다
        import shutil as _sh
        sr = td / 'scan'
        (sr / 'pse_x' / 'post_pse_x').mkdir(parents=True)
        for fn in ('atom_100.liggghts', 'contact_100.liggghts', 'mesh_100.stl'):
            _sh.copy(post / fn, sr / 'pse_x' / 'post_pse_x' / fn)
        _sh.copy(post / 'atom_100.liggghts', sr / 'pse_x' / 'post_pse_x' / 'atom_200.liggghts')   # contact · mesh 없는 늦은 step
        rows = scan_rows(sr, 3, 'pure_SE')
        chk('--scan-root: atom · contact · mesh 가 다 있는 step (100) 을 고른다',
            len(rows) == 1 and rows[0]['atom_file'].endswith('atom_100.liggghts') and rows[0]['design_family'] == 'pure_SE')

        # (3) 세 SE 가 한 점에서 겹친다 — 쌍 렌즈 union 은 공극을 **크게** (상한), 정확 union 이 그보다 작아야
        c = 0.005
        tri = [(1, 3, c - 0.0006, c, 0.003, 0.001), (2, 3, c + 0.0006, c, 0.003, 0.001), (3, 3, c, c + 0.0006, 0.003, 0.001)]
        pairs = []
        for (ia, _, xa, ya, za, ra_), (ib, _, xb, yb, zb, rb_) in ((tri[0], tri[1]), (tri[0], tri[2]), (tri[1], tri[2])):
            pairs.append((ia, ib, ra_ + rb_ - math.dist((xa, ya, za), (xb, yb, zb))))
        post = write_case('tri', tri, pairs, 0.006)
        r3 = one(post / 'atom_100.liggghts', post / 'contact_100.liggghts', post / 'mesh_100.stl', 3, 3_000_000, 5)
        chk(f'세 입자 겹침: 쌍 렌즈 clipped {r3["eps_union_pair_clipped"]:.4f} > 정확 {r3["mc_void_pct"]:.4f} (상한)',
            r3['pair_minus_mc_void_pct'] > 4 * r3['mc_void_se_pct'])

        # (4) 열이 어긋난 접촉 덤프 · 두 프레임 원자 덤프 — 거부
        post = write_case('swap', atoms, [(1, 2, dlt)], 0.006, swap=True)
        r4 = one(post / 'atom_100.liggghts', post / 'contact_100.liggghts', post / 'mesh_100.stl', 3, 0, 1)
        chk('delta 자리에 area 가 든 덤프 → 검산 ① 이 잡는다 (> 1 %)', r4['delta_col_vs_geom_max_rel'] > DELTA_TOL)
        post = write_case('two_frames', atoms, [(1, 2, dlt)], 0.006)
        txt = (post / 'atom_100.liggghts').read_text()
        (post / 'atom_100.liggghts').write_text(txt + txt)
        try:
            one(post / 'atom_100.liggghts', post / 'contact_100.liggghts', post / 'mesh_100.stl', 3, 0, 1)
            chk('두 프레임 원자 덤프 거부', False)
        except ValueError:
            chk('두 프레임 원자 덤프 거부', True)
    print(f'selftest {"PASS" if not fails else "FAIL"} ({len(fails)} 실패)')
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser(description='LHS · lhsx porosity — sphere · union 전부 (읽기 전용)')
    ap.add_argument('--cohort')
    ap.add_argument('--root-from', default='')
    ap.add_argument('--root-to', default='')
    ap.add_argument('--case', action='append', default=[])
    ap.add_argument('--out')
    ap.add_argument('--mc-n', type=int, default=4_000_000, help='정확 union 의 무작위 점 수 (0 = 끔).  4e6 이면 통계 오차 ≈ 0.01 %%p')
    ap.add_argument('--margin-d', type=float, default=2.0, help='내부 공극률: 바닥 · 플래튼에서 뺄 두께 (SE 지름 배수)')
    ap.add_argument('--scan-root', help='코호트 대신 <root>/<case>/post*/ 를 훑는다 (예: 순수 SE 판정 시험 런)')
    ap.add_argument('--n-types', type=int, default=2, help='--scan-root 일 때 덱의 type 수 (순수 SE 덱 = 2)')
    ap.add_argument('--family', default='pure_SE', help='--scan-root 일 때 design_family 라벨')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.cohort or a.scan_root) or not a.out:
        ap.error('--cohort (또는 --scan-root) 와 --out 이 필요하다')
    return run(a)


if __name__ == '__main__':
    sys.exit(main())
