#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""단면 하중 몫 — 수평 단면을 지나는 수직 하중을 접촉 종류별로 나눈다 (읽기 전용 · 웹앱 결과 폴더).

    python3 scripts/plane_load_share.py --batch ~/ps45_network_20261006 --out ~/ps45_plane_load_20261007   (기록: docs/data/ps45_plane_load_20261007/)
    python3 scripts/plane_load_share.py --case <work/results/ID> --meta <work/uploads/ID/meta.json> --out <폴더>
    python3 scripts/plane_load_share.py --selftest

왜 (1저자 10-07 · 발표 5 쪽 힘 그래프): 접촉 힘 크기의 합은 같은 하중을 직렬로 놓인 접촉 수만큼 여러 번 센다 (real14: 합 = 단면 하중의 12.2 배)
  — 보존되는 양이 아니라서 '하중을 누가 지나' 로 읽을 수 없다.  단면을 지나는 하중은 힘 평형으로 높이마다 같다.

정의
  높이 z0 의 수평면이 입자를 **중심** 기준 위 (z ≥ z0) · 아래 (z < z0) 두 묶음으로 나눈다.  두 입자가 서로 다른 묶음인 접촉이 단면을 지난다.
  단면 하중 F(z0) = Σ (위쪽 입자가 그 접촉에서 받는 힘의 z 성분) — 접촉력 = 덤프 `fx·fy·fz` (id1 이 받는 힘 · 법선 + 접선 · id2 는 −f) ·
    그 열이 없으면 fn + ft.  압력 = F ÷ (box_x · box_y) × scale ÷ 1e6 MPa (덱 축척: σ_실제 = σ_덱 × scale).
  몫 = 접촉 종류 (쌍 PC–PC … · 묶음 AM–AM · AM–SE · SE–SE) 별 F 합 ÷ F.  법선 성분만의 몫도 참고로 낸다.
  위 묶음의 힘 평형 (준정적): F(z0) = 판 힘 + 위 묶음 무게 → 높이마다 같아야 한다 → 보존 검사 (유효 단면 하중 최대 ÷ 최소).
벽: 바닥 (z = 0 평면 — 덱 `zplane 0.0` 가정 · 덱은 읽지 않는다) · 판 (mesh_info.json plate_z) 접촉은 접촉 덤프에 없다 → 단면에 걸친 입자가
  벽에 닿으면 그 하중은 입자 몸을 지나 벽으로 가서 계산에서 빠진다 → 단면은 벽에서 2 × (가장 큰 반지름) 보다 먼 곳만 쓴다
  (벽에 닿은 입자의 몸은 벽에서 2r 안 — 그 밖의 단면에는 걸칠 수 없다).
상태: OK = 유효 단면 ≥ 3 · 보존 (최대 ÷ 최소 − 1 ≤ 2 %) · 입자 힘 평형 (중심이 유효 구간 안인 입자의 힘 가중 알짜 힘 ≤ 1 %) · 원자 id 누락 0 ·
  상자 = input_params.json.  어기면 CHECK (값은 내되 사유를 적는다) · 입력 결손 · 유효 단면 없음 = FAILED (값 없음).
출력 (--out): plane_load.json (전부 + 입력 sha256) · plane_load_cuts_<P_S>.csv (단면마다) · plane_load_summary.csv ·
  plane_load_share_slide.csv (Origin 머리 세 줄 — 가운데 단면 묶음 몫).
"""
import argparse
import csv
import hashlib
import json
import math
import os
import sys
import tempfile
from pathlib import Path

import numpy as np

SHORT = {'AM_P': 'PC', 'AM_S': 'SC', 'SE': 'SE'}
ORDER = {'PC': 0, 'SC': 1, 'SE': 2}
GROUPS = ('AM–AM', 'AM–SE', 'SE–SE')
PAIRS = ('PC–PC', 'PC–SC', 'SC–SC', 'PC–SE', 'SC–SE', 'SE–SE')
PS_ORDER = ['0:10', '3:7', '5:5', '7:3', '10:0']
N_CUTS = 21
CONSERVE_TOL = 0.02
BALANCE_TOL = 0.01
DEFAULT_BOX = 0.05


def parse_type_map(s):
    """'1:AM_P,2:AM_S,3:SE' → {1: 'AM_P', …}."""
    out = {}
    for tok in str(s or '').split(','):
        tok = tok.strip()
        if not tok:
            continue
        k, _, v = tok.partition(':')
        if not v.strip():
            raise ValueError(f'type map 항목 {tok!r} — "번호:이름" 이 아니다')
        out[int(k)] = v.strip()
    if not out:
        raise ValueError('빈 type map')
    return out


def pair_label(n1, n2):
    a, b = sorted([SHORT.get(n1, n1), SHORT.get(n2, n2)], key=lambda s: (ORDER.get(s, 9), s))
    return f'{a}–{b}'


def group_label(n1, n2):
    k = ('AM' in n1) + ('AM' in n2)
    if k == 2:
        return 'AM–AM'
    if k == 1 and 'SE' in (n1, n2):
        return 'AM–SE'
    if n1 == 'SE' and n2 == 'SE':
        return 'SE–SE'
    return 'other'


def compute(atoms, contacts, type_map, plate_z, box, scale, n_cuts=N_CUTS):
    """atoms = {'id','type','z','radius'} 배열 · contacts = {'id1','id2','f' (n,3) 전체 힘 (id1 이 받는 힘), 'fn' (n,3) 또는 None} ·
    plate_z 덱 · box = (box_x, box_y, 출처) · scale = 덱 축척.  반환 dict (status · why · cuts · mid · checks …)."""
    why = []
    ids = np.asarray(atoms['id'], dtype=np.int64)
    order = np.argsort(ids)
    ids = ids[order]
    if len(ids) and np.any(ids[1:] == ids[:-1]):
        return {'status': 'FAILED', 'why': ['원자 id 중복']}
    typ = np.asarray(atoms['type'], dtype=np.int64)[order]
    z = np.asarray(atoms['z'], dtype=float)[order]
    r = np.asarray(atoms['radius'], dtype=float)[order]
    if not (np.all(np.isfinite(z)) and np.all(np.isfinite(r)) and np.all(r > 0)):
        return {'status': 'FAILED', 'why': ['원자 z · 반경 비유한 또는 반경 ≤ 0']}
    unknown = sorted(set(typ.tolist()) - set(type_map))
    if unknown:
        return {'status': 'FAILED', 'why': [f'type map 에 없는 원자 형 {unknown}']}
    if not (np.isfinite(plate_z) and plate_z > 0):
        return {'status': 'FAILED', 'why': [f'plate_z {plate_z!r} 무효']}
    bx, by, box_src = box
    area = bx * by
    if box_src != 'input_params.json':
        why.append(f'상자 = {box_src} ({bx} × {by}) — 압력 값은 상자가 맞을 때만 (몫은 무관)')
    name = np.array([type_map[t] for t in typ.tolist()])

    i1 = np.searchsorted(ids, np.asarray(contacts['id1'], dtype=np.int64))
    i2 = np.searchsorted(ids, np.asarray(contacts['id2'], dtype=np.int64))
    ok1 = (i1 < len(ids)) & (ids[np.minimum(i1, len(ids) - 1)] == np.asarray(contacts['id1'], dtype=np.int64))
    ok2 = (i2 < len(ids)) & (ids[np.minimum(i2, len(ids) - 1)] == np.asarray(contacts['id2'], dtype=np.int64))
    ok = ok1 & ok2
    n_missing = int((~ok).sum())
    if n_missing:
        why.append(f'원자 id 없는 접촉 {n_missing} — 뺐다')
    f = np.asarray(contacts['f'], dtype=float)[ok]
    fn = None if contacts.get('fn') is None else np.asarray(contacts['fn'], dtype=float)[ok]
    i1, i2 = i1[ok], i2[ok]
    if not np.all(np.isfinite(f)):
        return {'status': 'FAILED', 'why': why + ['접촉 힘 비유한']}
    grp = np.array([group_label(name[a], name[b]) for a, b in zip(i1, i2)])
    pr = np.array([pair_label(name[a], name[b]) for a, b in zip(i1, i2)])
    z1, z2 = z[i1], z[i2]
    sgn = np.where(z1 > z2, 1.0, -1.0)                       # 위쪽 입자가 받는 힘 = id1 이 위면 f · 아니면 −f
    fz_up = sgn * f[:, 2]
    fnz_up = None if fn is None else sgn * fn[:, 2]
    lo_z, hi_z = np.minimum(z1, z2), np.maximum(z1, z2)

    r_max = float(r.max())
    lo, hi = 2.0 * r_max, plate_z - 2.0 * r_max
    conv = scale / 1e6 / area                                # 덱 힘 → 실제 MPa
    base = {'plate_z_deck': plate_z, 'plate_gap_um': plate_z * scale, 'scale': scale, 'box': [bx, by], 'box_source': box_src,
            'r_max_um': r_max * scale, 'window_um': [lo * scale, hi * scale], 'n_atoms': int(len(ids)),
            'n_contacts': int(len(f)), 'n_contacts_missing_atom': n_missing,
            'n_center_below_floor': int((z < 0).sum()), 'n_center_above_plate': int((z > plate_z).sum())}
    if not hi > lo:
        return dict(base, status='FAILED', why=why + [f'유효 단면 없음 — 판 간격 {plate_z * scale:.3f} µm ≤ 4 × 가장 큰 반지름 {r_max * scale:.3f} µm'])
    cuts = []
    for z0 in np.linspace(lo, hi, n_cuts):
        m = (lo_z < z0) & (hi_z >= z0)                         # 중심이 단면 위 (z = z0) 인 입자는 위 묶음 — 분할이 늘 정의된다
        F = float(fz_up[m].sum())
        row = {'z_um': float(z0 * scale), 'frac_of_gap': float(z0 / plate_z), 'n_cross': int(m.sum()), 'load_mpa': F * conv}
        row['share_group_pct'] = {g: (100.0 * float(fz_up[m & (grp == g)].sum()) / F if F > 0 else None) for g in GROUPS}
        row['share_pair_pct'] = {p: (100.0 * float(fz_up[m & (pr == p)].sum()) / F if F > 0 else None) for p in PAIRS}
        if fnz_up is not None:
            Fn = float(fnz_up[m].sum())
            row['share_group_normal_pct'] = {g: (100.0 * float(fnz_up[m & (grp == g)].sum()) / Fn if Fn > 0 else None) for g in GROUPS}
        cuts.append(row)
    loads = np.array([c['load_mpa'] for c in cuts])
    if np.any(loads <= 0):
        why.append('하중 ≤ 0 인 단면이 있다 (압축이 아니다)')
        cons = None
    else:
        cons = float(loads.max() / loads.min())
        if cons - 1.0 > CONSERVE_TOL:
            why.append(f'보존 검사 — 단면 하중 최대 ÷ 최소 = {cons:.4f} > 1 + {CONSERVE_TOL}')
    # 입자 힘 평형 (중심이 유효 구간 안 — 벽에 닿을 수 없는 입자)
    net = np.zeros((len(ids), 3)); mag = np.zeros(len(ids))
    fm = np.linalg.norm(f, axis=1)
    np.add.at(net, i1, f); np.add.at(net, i2, -f)
    np.add.at(mag, i1, fm); np.add.at(mag, i2, fm)
    inner = (z >= lo) & (z <= hi) & (mag > 0)
    bal = float(np.linalg.norm(net[inner], axis=1).sum() / mag[inner].sum()) if inner.any() else None
    if bal is None or bal > BALANCE_TOL:
        why.append(f'입자 힘 평형 — 힘 가중 알짜 힘 {bal} > {BALANCE_TOL}' if bal is not None else '입자 힘 평형 — 대상 입자 없음')
    mid = cuts[len(cuts) // 2]
    fnm = np.linalg.norm(fn, axis=1) if fn is not None else fm
    tot = float(fnm.sum())
    mag_share = {g: 100.0 * float(fnm[grp == g].sum()) / tot for g in GROUPS} if tot > 0 else None
    cnt_share = {g: 100.0 * float((grp == g).mean()) for g in GROUPS} if len(grp) else None
    mean_share = {g: float(np.mean([c['share_group_pct'][g] for c in cuts if c['share_group_pct'][g] is not None]))
                  if any(c['share_group_pct'][g] is not None for c in cuts) else None for g in GROUPS}
    rng = {g: [float(min(c['share_group_pct'][g] for c in cuts)), float(max(c['share_group_pct'][g] for c in cuts))]
           if all(c['share_group_pct'][g] is not None for c in cuts) else None for g in GROUPS}
    out = dict(base, cuts=cuts, mid=mid, conservation_max_over_min=cons, balance_residual=bal,
               magnitude_sum_over_mid_load=(tot / (mid['load_mpa'] / conv) if mid['load_mpa'] > 0 else None),
               share_group_mean_over_cuts_pct=mean_share, share_group_range_over_cuts_pct=rng,
               magnitude_share_group_pct=mag_share, contact_count_share_group_pct=cnt_share,
               n_other_group=int((grp == 'other').sum()))
    if (grp == 'other').any():
        why.append(f'AM · SE 밖 쌍 {int((grp == "other").sum())} — 몫 분모에는 들어 있다')
    hard = [w for w in why if not w.startswith('상자 =')] or [w for w in why if w.startswith('상자 =')]
    out['status'] = 'OK' if not why else 'CHECK'
    out['why'] = why if hard else []
    return out


# ── 파일 ────────────────────────────────────────────────────────────────────
def _sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for b in iter(lambda: fh.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def load_case(res_dir, meta_path, scale_cli=None):
    import pandas as pd
    res_dir, meta_path = Path(res_dir), Path(meta_path)
    inputs = {}
    for nm in ('atoms.csv', 'contacts.csv', 'mesh_info.json'):
        p = res_dir / nm
        if not p.is_file():
            raise FileNotFoundError(f'{p} 없음')
        inputs[nm] = _sha(p)
    meta = json.loads(meta_path.read_text(encoding='utf-8'))
    inputs['meta.json'] = _sha(meta_path)
    tmap = parse_type_map(meta.get('type_map_resolved') or meta.get('type_map'))
    scale = float(meta['scale']) if meta.get('scale') not in (None, '') else None
    if scale_cli is not None:
        if scale is not None and not math.isclose(scale, scale_cli):
            raise ValueError(f'scale 불일치 — meta {scale} ↔ 인자 {scale_cli}')
        scale = scale_cli
    if scale is None or not scale > 0:
        raise ValueError('scale 없음 (meta.json · --scale)')
    plate_z = float(json.loads((res_dir / 'mesh_info.json').read_text(encoding='utf-8'))['plate_z'])
    ip = res_dir / 'input_params.json'
    if ip.is_file():
        d = json.loads(ip.read_text(encoding='utf-8'))
        inputs['input_params.json'] = _sha(ip)
        if 'box_x' in d and 'box_y' in d:
            box = (float(d['box_x']), float(d['box_y']), 'input_params.json')
        else:
            box = (DEFAULT_BOX, DEFAULT_BOX, 'default (input_params.json 에 box 없음)')
    else:
        box = (DEFAULT_BOX, DEFAULT_BOX, 'default (input_params.json 없음)')
    a = pd.read_csv(res_dir / 'atoms.csv', low_memory=False)
    for c in ('id', 'type', 'z', 'radius'):
        if c not in a.columns:
            raise ValueError(f'atoms.csv 열 {c} 없음')
    atoms = {c: pd.to_numeric(a[c], errors='coerce').to_numpy() for c in ('id', 'type', 'z', 'radius')}
    if np.isnan(atoms['id']).any() or np.isnan(atoms['type']).any():
        raise ValueError('atoms.csv id · type 비유한')
    cdf = pd.read_csv(res_dir / 'contacts.csv', low_memory=False)
    col = lambda k: pd.to_numeric(cdf[k], errors='coerce').to_numpy(dtype=float)
    if not {'id1', 'id2'} <= set(cdf.columns):
        raise ValueError('contacts.csv id1 · id2 없음')
    fn = np.stack([col('fn_x'), col('fn_y'), col('fn_z')], 1) if {'fn_x', 'fn_y', 'fn_z'} <= set(cdf.columns) else None
    if {'fx', 'fy', 'fz'} <= set(cdf.columns):
        f, f_src = np.stack([col('fx'), col('fy'), col('fz')], 1), 'fx·fy·fz'
    elif fn is not None and {'ft_x', 'ft_y', 'ft_z'} <= set(cdf.columns):
        f, f_src = fn + np.stack([col('ft_x'), col('ft_y'), col('ft_z')], 1), 'fn + ft'
    else:
        raise ValueError('contacts.csv 힘 열 없음 (fx·fy·fz 또는 fn_* + ft_*)')
    contacts = {'id1': col('id1').astype(np.int64), 'id2': col('id2').astype(np.int64), 'f': f, 'fn': fn}
    return atoms, contacts, tmap, plate_z, box, scale, inputs, f_src


def run_one(res_dir, meta_path, scale_cli=None):
    atoms, contacts, tmap, plate_z, box, scale, inputs, f_src = load_case(res_dir, meta_path, scale_cli)
    out = compute(atoms, contacts, tmap, plate_z, box, scale)
    out.update(results_dir=str(res_dir), meta=str(meta_path), inputs_sha256=inputs, force_source=f_src,
               type_map={str(k): v for k, v in tmap.items()})
    return out


def write_origin(path, head, units, comments, rows):
    with open(path, 'w', encoding='utf-8', newline='') as fh:
        w = csv.writer(fh, lineterminator='\n')
        w.writerow(head); w.writerow(units); w.writerow(comments)
        w.writerows(rows)


def _fmt(v, nd=4):
    return '' if v is None else f'{v:.{nd}f}'


def write_outputs(results, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / 'plane_load.json').write_text(json.dumps(results, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    for lab, r in results['cases'].items():
        if r.get('status') == 'FAILED':
            continue
        tag = lab.replace(':', '_')
        write_origin(out_dir / f'plane_load_cuts_{tag}.csv',
                     ['z', 'z / gap', 'contacts crossing', 'load', 'AM–AM', 'AM–SE', 'SE–SE'] + list(PAIRS),
                     ['µm', '-', '-', 'MPa'] + ['%'] * (3 + len(PAIRS)),
                     ['단면 높이 (바닥 z = 0)', '판 간격의 비', '단면을 지나는 접촉 수', '단면 하중 ÷ 상자 면적 (실제 MPa)']
                     + ['단면 하중 몫 (전체 접촉력 z 성분)'] * (3 + len(PAIRS)),
                     [[_fmt(c['z_um'], 3), _fmt(c['frac_of_gap'], 4), c['n_cross'], _fmt(c['load_mpa'], 3)]
                      + [_fmt(c['share_group_pct'][g]) for g in GROUPS] + [_fmt(c['share_pair_pct'][p]) for p in PAIRS]
                      for c in r['cuts']])
    labs = [l for l in results['order'] if results['cases'][l].get('status') != 'FAILED']
    rows = []
    for l in labs:
        r = results['cases'][l]
        rows.append([l] + [_fmt(r['mid']['share_group_pct'][g]) for g in GROUPS]
                    + [_fmt(r['share_group_mean_over_cuts_pct'][g]) for g in GROUPS]
                    + [_fmt(r['magnitude_share_group_pct'][g]) for g in GROUPS]
                    + [_fmt(r['mid']['load_mpa'], 3), _fmt(r['conservation_max_over_min'], 5), _fmt(r['balance_residual'], 6), r['status']])
    write_origin(out_dir / 'plane_load_summary.csv',
                 ['PC:SC'] + [f'{g} (mid)' for g in GROUPS] + [f'{g} (mean)' for g in GROUPS] + [f'{g} (|F| sum)' for g in GROUPS]
                 + ['Load (mid)', 'Load max/min', 'Balance residual', 'Status'],
                 ['wt%'] + ['%'] * 9 + ['MPa', '-', '-', '-'],
                 ['조성'] + ['가운데 단면 하중 몫'] * 3 + ['유효 단면 평균 몫'] * 3 + ['비교: 접촉 법선력 크기 합의 몫 (옛 5 쪽 방식 · 보존량 아님)'] * 3
                 + ['가운데 단면 하중 (실제 MPa)', '유효 단면 하중 최대 ÷ 최소 (보존 검사)', '입자 힘 가중 알짜 힘 (평형 검사)', 'OK / CHECK'],
                 rows)
    write_origin(out_dir / 'plane_load_share_slide.csv', ['PC:SC'] + list(GROUPS), ['wt%'] + ['%'] * 3,
                 ['조성'] + ['가운데 수평 단면을 지나는 수직 하중의 몫 (힘 평형 — 보존량)'] * 3,
                 [[l] + [_fmt(results['cases'][l]['mid']['share_group_pct'][g]) for g in GROUPS] for l in labs])


def run_batch(batch, out_dir, scale_cli=None):
    batch = Path(batch)
    rows = list(csv.DictReader(open(batch / 'network_cases.tsv', encoding='utf-8'), delimiter='\t'))
    if not rows or not {'case_id', 'P_S'} <= set(rows[0]):
        raise ValueError('network_cases.tsv 에 case_id · P_S 열이 없다')
    cases, order = {}, []
    for row in sorted(rows, key=lambda q: (PS_ORDER.index(q['P_S']) if q['P_S'] in PS_ORDER else 99, q['P_S'])):
        lab, cid = row['P_S'], row['case_id']
        res = batch / 'work' / 'results' / cid
        meta = batch / 'work' / 'uploads' / cid / 'meta.json'
        try:
            r = run_one(res, meta, scale_cli)
        except Exception as e:                                # 케이스 하나의 입력 결손 = 그 케이스 FAILED (다른 케이스는 계속)
            r = {'status': 'FAILED', 'why': [f'{type(e).__name__}: {e}'], 'results_dir': str(res)}
        r['case_id'] = cid
        cases[lab] = r
        order.append(lab)
    results = {'tool': 'plane_load_share', 'definition': '수평 단면을 지나는 수직 하중 (전체 접촉력 z 성분 · 중심 기준 분할) 의 접촉 종류별 몫',
               'tolerances': {'conservation': CONSERVE_TOL, 'balance': BALANCE_TOL}, 'n_cuts': N_CUTS,
               'code_sha256': _sha(Path(__file__)), 'order': order, 'cases': cases}
    write_outputs(results, out_dir)
    return results


def print_report(results):
    print(f'{"PC:SC":6s} {"상태":6s} {"가운데 하중 MPa":>14s} {"보존 최대/최소":>14s} {"평형":>9s}   가운데 단면 몫 AM–AM · AM–SE · SE–SE   (|F| 합 몫)')
    for l in results['order']:
        r = results['cases'][l]
        if r.get('status') == 'FAILED':
            print(f'{l:6s} FAILED  {"; ".join(r.get("why", []))}')
            continue
        m = r['mid']['share_group_pct']; s = r['magnitude_share_group_pct']
        print(f'{l:6s} {r["status"]:6s} {r["mid"]["load_mpa"]:14.2f} {r["conservation_max_over_min"] or float("nan"):14.4f} '
              f'{r["balance_residual"]:9.2e}   ' + ' · '.join(_fmt(m[g], 1) for g in GROUPS) + '   (' + ' · '.join(_fmt(s[g], 1) for g in GROUPS) + ')')
        for w in r.get('why', []):
            print(f'         ⚠ {w}')


# ── 자체 시험 ───────────────────────────────────────────────────────────────
def _column(x_ids_start, zs, r, typ, F, fx_lat=0.0):
    """세로 기둥: 중심 zs (아래 → 위) · 이웃 접촉 (id1 = 아래) · 아래 입자가 받는 힘 = (fx_lat, 0, −F) (위 입자는 +F)."""
    ids = list(range(x_ids_start, x_ids_start + len(zs)))
    con = [(ids[k], ids[k + 1], (fx_lat, 0.0, -F)) for k in range(len(zs) - 1)]
    return ids, [typ] * len(zs), list(zs), [r] * len(zs), con


def _build(cols):
    ids, typ, z, rad, con = [], [], [], [], []
    for c in cols:
        ids += c[0]; typ += c[1]; z += c[2]; rad += c[3]; con += c[4]
    atoms = {'id': np.array(ids), 'type': np.array(typ), 'z': np.array(z), 'radius': np.array(rad)}
    contacts = {'id1': np.array([c[0] for c in con]), 'id2': np.array([c[1] for c in con]),
                'f': np.array([c[2] for c in con], dtype=float), 'fn': np.array([(0.0, 0.0, c[2][2]) for c in con], dtype=float)}
    return atoms, contacts


def _vcol(id0, typ, x, y, zs, r, F):
    """세로 기둥 (같은 반경 · 닿음) — parts [(id, 형, x, y, z, r)] · cons [(id1 = 아래, id2, 아래 입자가 받는 힘 (0, 0, −F), 접촉점 = 중점)]."""
    parts = [(id0 + k, typ, x, y, z, r) for k, z in enumerate(zs)]
    cons = [(id0 + k, id0 + k + 1, (0.0, 0.0, -F), (x, y, 0.5 * (zs[k] + zs[k + 1]))) for k in range(len(zs) - 1)]
    return parts, cons


def _lw_case(parts, cons):
    """parts [(id, 형, x, y, z, r)] · cons [(id1, id2, id1 이 받는 힘 (3), 접촉점 (3))] (법선 = 힘 · 접선 0) →
    (compute 용 배열 둘, 봉인 Love–Weber 용 atoms_raw · contacts_raw — analyze_contacts 로더와 같은 키)."""
    atoms = {'id': np.array([p[0] for p in parts]), 'type': np.array([p[1] for p in parts]),
             'z': np.array([p[4] for p in parts], dtype=float), 'radius': np.array([p[5] for p in parts], dtype=float)}
    f = np.array([c[2] for c in cons], dtype=float)
    contacts = {'id1': np.array([c[0] for c in cons]), 'id2': np.array([c[1] for c in cons]), 'f': f, 'fn': f.copy()}
    atoms_raw = {int(p[0]): {'type': int(p[1]), 'x': float(p[2]), 'y': float(p[3]), 'z': float(p[4]), 'radius': float(p[5])}
                 for p in parts}
    contacts_raw = []
    for c in cons:
        (fx, fy, fz), (cx, cy, cz) = c[2], c[3]
        contacts_raw.append({'id1': int(c[0]), 'id2': int(c[1]), 'fx': float(fx), 'fy': float(fy), 'fz': float(fz),
                             'fn_x': float(fx), 'fn_y': float(fy), 'fn_z': float(fz), 'ft_x': 0.0, 'ft_y': 0.0, 'ft_z': 0.0,
                             'cp_x': float(cx), 'cp_y': float(cy), 'cp_z': float(cz)})
    return atoms, contacts, atoms_raw, contacts_raw


def selftest():
    res = []

    def chk(name, cond):
        """cond = 참거짓 또는 인자 없는 함수 (함수면 여기서 부른다 — 예외 = 실패로 세고 이유를 적는다 · 시험 먼저 단계에서
        새 API 가 없을 때도 시험 전체가 끝까지 돈다)."""
        why = ''
        if callable(cond):
            try:
                cond = cond()
            except Exception as e:                            # noqa: BLE001 — 시험 실패로 센다
                cond, why = False, f'  — {type(e).__name__}: {str(e)[:120]}'
        res.append((name, bool(cond)))
        print(('  ✓ ' if cond else '  ✗ ') + name + why)

    def _try(fn):
        """공유 준비 계산 — 예외면 그 예외를 값으로 (그 값을 쓰는 시험이 실패로 센다)."""
        try:
            return fn()
        except Exception as e:                                # noqa: BLE001
            return e

    def _ok(x):
        if isinstance(x, Exception):
            raise x
        return x

    TM = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}
    box = (1.0, 1.0, 'input_params.json')
    # T1 직렬 기둥 (SE 10 개 · 하중 F) — 모든 단면 = F · 크기 합 = 9F
    a, c = _build([_column(1, [0.05 + 0.1 * k for k in range(10)], 0.05, 3, 2.0)])
    o = compute(a, c, TM, 1.0, box, 1.0)
    chk('T1 직렬 기둥: 상태 OK', o['status'] == 'OK')
    chk('T1 모든 단면 하중 = F (보존 1.0)', all(math.isclose(q['load_mpa'], 2.0 / 1e6) for q in o['cuts']) and math.isclose(o['conservation_max_over_min'], 1.0))
    chk('T1 SE–SE 몫 100 %', math.isclose(o['mid']['share_group_pct']['SE–SE'], 100.0))
    chk('T1 크기 합 ÷ 단면 하중 = 9 (직렬 접촉 수)', math.isclose(o['magnitude_sum_over_mid_load'], 9.0))
    # T2 평행 기둥 둘 — AM_P (F 3) · SE (F 1) → 단면 몫 75 / 25 · 크기 합 몫 12 / 21 (다르다)
    colA = _column(1, [0.1, 0.3, 0.5, 0.7, 0.9], 0.1, 1, 3.0)
    colB = _column(100, [0.05 + 0.1 * k for k in range(10)], 0.05, 3, 1.0)
    a, c = _build([colA, colB])
    o2 = compute(a, c, TM, 1.0, box, 1.0)
    chk('T2 평행 기둥: 단면 몫 AM–AM 75 % · SE–SE 25 %', math.isclose(o2['mid']['share_group_pct']['AM–AM'], 75.0) and math.isclose(o2['mid']['share_group_pct']['SE–SE'], 25.0))
    chk('T2b 단면이 입자 중심 (z = 0.5) 을 지나도 그 기둥 하중이 빠지지 않는다',
        any(math.isclose(q['z_um'], 0.5) for q in o2['cuts']) and all(math.isclose(q['load_mpa'], 4.0 / 1e6) for q in o2['cuts']))
    chk('T2 크기 합 몫 = 12/21 (단면 몫과 다르다)', math.isclose(o2['magnitude_share_group_pct']['AM–AM'], 100 * 12 / 21))
    chk('T2 쌍 몫 PC–PC 75 %', math.isclose(o2['mid']['share_pair_pct']['PC–PC'], 75.0))
    # T3 id 순서 바꿈 + 힘 부호 → 같은 결과
    c3 = {'id1': c['id2'], 'id2': c['id1'], 'f': -c['f'], 'fn': -c['fn']}
    o3 = compute(a, c3, TM, 1.0, box, 1.0)
    chk('T3 id1 ↔ id2 (힘 부호 반대) 불변', all(math.isclose(p['load_mpa'], q['load_mpa']) for p, q in zip(o2['cuts'], o3['cuts']))
        and math.isclose(o3['mid']['share_group_pct']['AM–AM'], 75.0))
    # T4 가로 힘 (접선) 은 단면 하중에 안 들어간다 · 법선 몫 따로
    a4, c4 = _build([_column(1, [0.1, 0.3, 0.5, 0.7, 0.9], 0.1, 1, 3.0, fx_lat=0.7), colB])
    o4 = compute(a4, c4, TM, 1.0, box, 1.0)
    chk('T4 가로 성분 무관 (AM–AM 75 %)', math.isclose(o4['mid']['share_group_pct']['AM–AM'], 75.0))
    chk('T4 법선 몫 계산됨', math.isclose(o4['mid']['share_group_normal_pct']['AM–AM'], 75.0))
    # T5 접촉 하나 빠짐 → 보존 · 평형 어긋남 → CHECK
    keep = np.ones(len(c['id1']), bool); keep[len(colA[4]) + 4] = False
    c5 = {k: (v[keep] if v is not None else None) for k, v in c.items()}
    o5 = compute(a, c5, TM, 1.0, box, 1.0)
    chk('T5 접촉 하나 빠짐 → CHECK (보존 · 평형 사유)', o5['status'] == 'CHECK' and any('보존' in w for w in o5['why']) and any('평형' in w for w in o5['why']))
    # T6 원자 없는 접촉 → CHECK · 그 접촉만 뺀다
    c6 = {k: (np.concatenate([v, v[:1]]) if v is not None else None) for k, v in c.items()}
    c6['id2'] = c6['id2'].copy(); c6['id2'][-1] = 99999
    o6 = compute(a, c6, TM, 1.0, box, 1.0)
    chk('T6 원자 없는 접촉 1 → 누락 1 · CHECK', o6['n_contacts_missing_atom'] == 1 and o6['status'] == 'CHECK')
    # T7 얇은 침대 (판 간격 ≤ 4 r_max) → FAILED
    o7 = compute(a, c, TM, 0.39, box, 1.0)
    chk('T7 얇은 침대 → FAILED (유효 단면 없음)', o7['status'] == 'FAILED' and '유효 단면 없음' in o7['why'][-1])
    # T8 무게 1 % (아래로 갈수록 하중 증가) → 허용 (OK)
    zs = [0.05 + 0.1 * k for k in range(10)]
    con = [(k + 1, k + 2, (0.0, 0.0, -(2.0 + 0.002 * (9 - k)))) for k in range(9)]
    a8 = {'id': np.arange(1, 11), 'type': np.full(10, 3), 'z': np.array(zs), 'radius': np.full(10, 0.05)}
    c8 = {'id1': np.array([q[0] for q in con]), 'id2': np.array([q[1] for q in con]), 'f': np.array([q[2] for q in con]), 'fn': None}
    o8 = compute(a8, c8, TM, 1.0, box, 1.0)
    chk('T8 무게 몫 1 % 안 → 보존 통과 (평형은 무게만큼 어긋남 → CHECK 사유는 평형만)',
        o8['conservation_max_over_min'] < 1.02 and not any('보존' in w for w in o8['why']))
    # T9 압력 환산 · type map · 쌍 이름
    o9 = compute(a, c, TM, 1.0, (0.5, 0.2, 'input_params.json'), 1000.0)
    chk('T9 압력 = F ÷ 면적 × scale ÷ 1e6', math.isclose(o9['mid']['load_mpa'], 4.0 / 0.1 * 1000.0 / 1e6))
    chk('T9 type map 해석 · 쌍 이름', parse_type_map('1:SE, 2:AM_P') == {1: 'SE', 2: 'AM_P'} and pair_label('SE', 'AM_P') == 'PC–SE'
        and pair_label('AM_S', 'AM_P') == 'PC–SC' and group_label('AM_S', 'SE') == 'AM–SE')
    try:
        parse_type_map('1AM_P')
        bad = False
    except ValueError:
        bad = True
    chk('T9 type map 형식 오류 거부', bad)
    chk('T9 상자 기본값 → CHECK 사유', compute(a, c, TM, 1.0, (0.05, 0.05, 'default (input_params.json 없음)'), 1.0)['status'] == 'CHECK')
    # T10 파일 · 배치 끝까지 (평행 기둥 · fx 없는 CSV = fn + ft 경로 · 한 케이스 입력 결손)
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        (td / 'network_cases.tsv').write_text('case_id\tP_S\nA1\t7:3\nB2\t3:7\n', encoding='utf-8')
        rd = td / 'work' / 'results' / 'A1'; up = td / 'work' / 'uploads' / 'A1'
        rd.mkdir(parents=True); up.mkdir(parents=True)
        with open(rd / 'atoms.csv', 'w', newline='') as fh:
            w = csv.writer(fh); w.writerow(['id', 'type', 'x', 'y', 'z', 'radius'])
            for i, t, zz, rr in zip(a['id'], a['type'], a['z'], a['radius']):
                w.writerow([int(i), int(t), 0.5, 0.5, zz, rr])
        with open(rd / 'contacts.csv', 'w', newline='') as fh:
            w = csv.writer(fh); w.writerow(['id1', 'id2', 'fn_x', 'fn_y', 'fn_z', 'ft_x', 'ft_y', 'ft_z', 'contact_area', 'delta'])
            for i1_, i2_, ff in zip(c['id1'], c['id2'], c['f']):
                w.writerow([int(i1_), int(i2_), 0.0, 0.0, ff[2], ff[0], ff[1], 0.0, 1e-3, 1e-3])
        (rd / 'mesh_info.json').write_text(json.dumps({'plate_z': 1.0}), encoding='utf-8')
        (rd / 'input_params.json').write_text(json.dumps({'box_x': 1.0, 'box_y': 1.0}), encoding='utf-8')
        (up / 'meta.json').write_text(json.dumps({'type_map_resolved': '1:AM_P,2:AM_S,3:SE', 'scale': 1}), encoding='utf-8')
        out = td / 'out'
        R = run_batch(td, out)
        ok_files = all((out / n).is_file() for n in ('plane_load.json', 'plane_load_summary.csv', 'plane_load_share_slide.csv', 'plane_load_cuts_7_3.csv'))
        chk('T10 배치: 파일 넷 · 순서 3:7 → 7:3', ok_files and R['order'] == ['3:7', '7:3'])
        chk('T10 fx 없는 CSV → fn + ft 경로 · 몫 75 %', R['cases']['7:3']['force_source'] == 'fn + ft'
            and math.isclose(R['cases']['7:3']['mid']['share_group_pct']['AM–AM'], 75.0))
        chk('T10 입력 결손 케이스 = FAILED (다른 케이스 계속)', R['cases']['3:7']['status'] == 'FAILED')
        lines = (out / 'plane_load_share_slide.csv').read_text(encoding='utf-8').splitlines()
        chk('T10 슬라이드 CSV 머리 세 줄 + 값 한 줄 (FAILED 제외)', len(lines) == 4 and lines[0].startswith('PC:SC') and lines[3].startswith('7:3,75.0000'))
        chk('T10 입력 sha256 기록', set(R['cases']['7:3']['inputs_sha256']) >= {'atoms.csv', 'contacts.csv', 'mesh_info.json', 'meta.json'})
        chk('T10 fx · 접촉점 열 없는 CSV → α NOT_COMPUTED (Love–Weber 사유) · 단면 하중 값은 그대로',
            lambda: R['cases']['7:3']['alpha']['status'].startswith('NOT_COMPUTED') and 'cp_x' in R['cases']['7:3']['alpha']['status']
            and R['cases']['7:3']['status'] == 'OK')

    # ══ Q1 (1저자 10-07) — 슬라이드 양 = Contribution to σ_zz = 21 단면 평균 Σ_k F_X ÷ Σ_k F (하중 가중) ═══════════════
    #  혼합 기둥 (AM_P r 0.1 셋 → SE r 0.05 넷 · 아래가 무겁다: AM–AM 4 · AM–SE 3 · SE–SE 2) · 판 1.0 · 창 [0.2, 0.8] ·
    #  21 단면 = 0.2 + 0.03 k → AM–AM 11 장 · AM–SE 5 · SE–SE 5 (중심 · 단면이 0.01 이상 떨어지게 골랐다 — 동률 없음).
    G3 = GROUPS
    M_parts = [(1, 1, 0.5, 0.5, 0.11, 0.1), (2, 1, 0.5, 0.5, 0.31, 0.1), (3, 1, 0.5, 0.5, 0.51, 0.1),
               (4, 3, 0.5, 0.5, 0.66, 0.05), (5, 3, 0.5, 0.5, 0.76, 0.05), (6, 3, 0.5, 0.5, 0.86, 0.05), (7, 3, 0.5, 0.5, 0.96, 0.05)]
    M_cons = [(1, 2, (0.0, 0.0, -4.0), (0.5, 0.5, 0.21)), (2, 3, (0.0, 0.0, -4.0), (0.5, 0.5, 0.41)),
              (3, 4, (0.0, 0.0, -3.0), (0.5, 0.5, 0.61)), (4, 5, (0.0, 0.0, -2.0), (0.5, 0.5, 0.71)),
              (5, 6, (0.0, 0.0, -2.0), (0.5, 0.5, 0.81)), (6, 7, (0.0, 0.0, -2.0), (0.5, 0.5, 0.91))]
    aM, cM, arM, crM = _lw_case(M_parts, M_cons)
    oM = compute(aM, cM, TM, 1.0, box, 1.0)
    exp_mean = {'AM–AM': 100 * 44 / 69, 'AM–SE': 100 * 15 / 69, 'SE–SE': 100 * 10 / 69}          # Σ_k F_X ÷ Σ_k F
    exp_int = {'AM–AM': 100 * 1.24 / 1.97, 'AM–SE': 100 * 0.45 / 1.97, 'SE–SE': 100 * 0.28 / 1.97}   # 창 잘린 적분 (연속 극한)
    chk('T11 혼합 기둥: 단면 분류 11 · 5 · 5 장 · 가운데 단면 = AM–AM 100 %',
        lambda: [sum(1 for q in oM['cuts'] if math.isclose(q['share_group_pct'][g], 100.0)) for g in G3] == [11, 5, 5]
        and math.isclose(oM['mid']['share_group_pct']['AM–AM'], 100.0))
    chk('T11 Contribution to σ_zz = Σ_k F_X ÷ Σ_k F = 44/69 · 15/69 · 10/69 (단면 몫 단순 평균 11/21 · 5/21 · 5/21 과 다르다)',
        lambda: all(math.isclose(oM['contribution_sigma_zz_pct'][g], exp_mean[g], rel_tol=1e-12) for g in G3)
        and not math.isclose(oM['contribution_sigma_zz_pct']['AM–AM'], 100 * 11 / 21, rel_tol=1e-3))
    chk('T11 σ_zz (21 단면 하중 평균) = 69/21 × 1e-6 MPa', lambda: math.isclose(oM['sigma_zz_planes_mean_mpa'], 69 / 21 * 1e-6, rel_tol=1e-12))
    chk('T11 연속 극한 (창 잘린 적분 Σ f_z^up × 창과 겹친 길이) = 1.24 · 0.45 · 0.28 ÷ 1.97 · σ_zz = 1.97 ÷ 0.6 × 1e-6',
        lambda: all(math.isclose(oM['contribution_sigma_zz_integral_pct'][g], exp_int[g], rel_tol=1e-12) for g in G3)
        and math.isclose(oM['sigma_zz_window_integral_mpa'], 1.97 / 0.6 * 1e-6, rel_tol=1e-12))
    exp_comment = 'Contribution to σ_zz — 21 수평 단면 평균 (= (1/V)Σ f_z l_z 의 접촉 유형별 몫 · 벽 근처 2 r_max 제외)'
    new_keys = ('contribution_sigma_zz_pct', 'sigma_zz_planes_mean_mpa', 'sigma_zz_window_integral_mpa',
                'contribution_sigma_zz_integral_pct', 'window_deck', 'alpha')

    def _write_m(d):
        o = dict(oM)
        o['alpha'] = stress_alpha(arM, crM, TM, oM, box, 1.0)
        R = {'tool': 'plane_load_share', 'n_cuts': N_CUTS, 'order': ['7:3'], 'cases': {'7:3': o}}
        write_outputs(R, d)
        return R
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        _try(lambda: _write_m(td / 'A'))
        sl = _try(lambda: list(csv.reader(open(td / 'A' / 'plane_load_share_slide.csv', encoding='utf-8'))))
        sm = _try(lambda: list(csv.reader(open(td / 'A' / 'plane_load_summary.csv', encoding='utf-8'))))
        chk('T11 슬라이드 머리: Long Name AM–AM · AM–SE · SE–SE contacts · 단위 % · 주석 = Contribution to σ_zz (21 수평 단면 평균)',
            lambda: _ok(sl)[0] == ['PC:SC', 'AM–AM contacts', 'AM–SE contacts', 'SE–SE contacts'] and _ok(sl)[1] == ['wt%', '%', '%', '%']
            and _ok(sl)[2] == ['조성'] + [exp_comment] * 3)
        chk('T11 슬라이드 값 = 21 단면 평균 63.7681 · 21.7391 · 14.4928 (가운데 단면 100 · 0 · 0 이 아니다)',
            lambda: _ok(sl)[3:] == [['7:3', '63.7681', '21.7391', '14.4928']])
        chk('T11 요약 (mean) 열 = 슬라이드 값 · (mid) 열 = 가운데 단면 그대로',
            lambda: (lambda h, row: [row[h.index(f'{g} (mean)')] for g in G3] == ['63.7681', '21.7391', '14.4928']
                     and [row[h.index(f'{g} (mid)')] for g in G3] == ['100.0000', '0.0000', '0.0000'])(_ok(sm)[0], _ok(sm)[3]))

        def _rw():
            rewrite_from_json(td / 'A' / 'plane_load.json', td / 'B')
            return {n: (td / 'A' / n).read_bytes() == (td / 'B' / n).read_bytes()
                    for n in ('plane_load_share_slide.csv', 'plane_load_summary.csv', 'plane_load_cuts_7_3.csv', 'stress_reduction_slide.csv')}
        same = _try(_rw)
        chk('T11 --rewrite (plane_load.json → CSV) = 처음 쓴 CSV 넷과 바이트 같다 (슬라이드 · 요약 · 단면 · α)',
            lambda: len(_ok(same)) == 4 and all(_ok(same).values()))

        def _old():
            d = json.loads((td / 'A' / 'plane_load.json').read_text(encoding='utf-8'))
            for k in new_keys:
                d['cases']['7:3'].pop(k)
            (td / 'C').mkdir()
            src = td / 'C' / 'plane_load.json'
            src.write_text(json.dumps(d, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
            h0 = _sha(src)
            rewrite_from_json(src, td / 'C')
            prov = json.loads((td / 'C' / 'plane_load_rewrite.json').read_text(encoding='utf-8'))
            return {'slide': (td / 'C' / 'plane_load_share_slide.csv').read_bytes() == (td / 'A' / 'plane_load_share_slide.csv').read_bytes(),
                    'kept': _sha(src) == h0, 'no_alpha': not (td / 'C' / 'stress_reduction_slide.csv').exists(),
                    'prov': prov.get('source_json_sha256') == h0 and prov.get('code_sha256') == _sha(Path(__file__))
                    and set(prov.get('written', {})) >= {'plane_load_share_slide.csv', 'plane_load_summary.csv', 'plane_load_cuts_7_3.csv'}}
        old = _try(_old)
        chk('T11 옛 형식 JSON (기여 키 · α 없음) 재작성 → 같은 슬라이드 (단면 기록에서 다시 계산)', lambda: _ok(old)['slide'])
        chk('T11 재작성은 원 JSON 을 안 건드린다 · α 없는 옛 JSON 이면 α 슬라이드를 안 쓴다', lambda: _ok(old)['kept'] and _ok(old)['no_alpha'])
        chk('T11 재작성 출처 기록 plane_load_rewrite.json (원 JSON sha256 · 코드 sha256 · 쓴 파일)', lambda: _ok(old)['prov'])

        def _refuse():
            base = json.loads((td / 'A' / 'plane_load.json').read_text(encoding='utf-8'))
            bad = []
            for mut in ('tamper', 'tool'):
                d = json.loads(json.dumps(base))
                if mut == 'tamper':
                    d['cases']['7:3']['contribution_sigma_zz_pct']['AM–AM'] += 1.0
                else:
                    d['tool'] = 'other'
                p = td / f'{mut}.json'
                p.write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')
                try:
                    rewrite_from_json(p, td / mut)
                    bad.append(mut)
                except ValueError:
                    pass
            return not bad
        chk('T11 재작성 거부: 저장된 기여 ≠ 단면에서 다시 계산 · 다른 도구의 JSON', _refuse)

    # ══ Q2 (1저자 10-07) — α = ⟨σ_zz⟩_상 ÷ ⟨σ_zz⟩_전체 (부피 가중 · 봉인 Love–Weber 입자 텐서 · 중심이 단면 창 안) ══════════
    #  평행 기둥 (T2 기하): AM_P r 0.1 (F 3) · SE r 0.05 (F 1) · 창 [0.2, 0.8] — 창 안 입자 = 접촉 둘 · |σ_zz| = 3F/(2πr²) (해석).
    pA, kA = _vcol(1, 1, 0.2, 0.5, [0.1, 0.3, 0.5, 0.7, 0.9], 0.1, 3.0)
    pB, kB = _vcol(100, 3, 0.7, 0.5, [0.05 + 0.1 * k for k in range(10)], 0.05, 1.0)
    aP, cP, arP, crP = _lw_case(pA + pB, kA + kB)
    oP = compute(aP, cP, TM, 1.0, box, 1.0)
    alP = _try(lambda: stress_alpha(arP, crP, TM, oP, box, 1.0))
    sA, sB = 3 * 3.0 / (2 * math.pi * 0.1 ** 2), 3 * 1.0 / (2 * math.pi * 0.05 ** 2)
    VA, VB = 4 / 3 * math.pi * 0.1 ** 3, 4 / 3 * math.pi * 0.05 ** 3
    s_all = (3 * VA * sA + 6 * VB * sB) / (3 * VA + 6 * VB)
    chk('T12 평행 기둥: α 상태 OK · 창 안 AM_P 3 · SE 6 (벽에 닿는 끝 입자 빠짐) · 창 안 벽 닿는 입자 0',
        lambda: _ok(alP)['status'] == 'OK' and _ok(alP)['n_window'] == {'AM_P': 3, 'SE': 6}
        and _ok(alP)['cross_check']['n_window_touching_wall'] == 0)
    chk('T12 봉인 Love–Weber 입자 σ_zz = −3F/(2πr²) (상 평균 · 압축 양수 · AM_P · SE)',
        lambda: math.isclose(_ok(alP)['mean_compressive_sigma_zz_mpa']['AM_P'], sA * 1e-6, rel_tol=1e-12)
        and math.isclose(_ok(alP)['mean_compressive_sigma_zz_mpa']['SE'], sB * 1e-6, rel_tol=1e-12))
    chk('T12 α AM_P = 0.9375 · α SE = 1.25 · α AM = α AM_P · α AM_S = null (상 없음 — 0 아님)',
        lambda: math.isclose(sA / s_all, 0.9375, rel_tol=1e-12) and math.isclose(_ok(alP)['alpha_zz']['AM_P'], 0.9375, rel_tol=1e-12)
        and math.isclose(_ok(alP)['alpha_zz']['SE'], 1.25, rel_tol=1e-12) and math.isclose(_ok(alP)['alpha_zz']['AM'], 0.9375, rel_tol=1e-12)
        and _ok(alP)['alpha_zz']['AM_S'] is None)
    chk('T12 닫힘 Σ (V_X/V_all) α_X = 1 · 수직 하중뿐 → α_p (평균 응력 tr σ/3) = α_zz',
        lambda: abs(_ok(alP)['closure_zz'] - 1) < 1e-12 and abs(_ok(alP)['closure_p'] - 1) < 1e-12
        and all(math.isclose(_ok(alP)['alpha_p'][k], _ok(alP)['alpha_zz'][k], rel_tol=1e-12) for k in ('AM_P', 'SE', 'AM')))
    chk('T12 교차 대조: LW 창 합 ÷ 21 단면 평균 = 1 (기둥이 창을 꼭 채운다) · 창 안 두 입자 1.7 · 가장자리 LW 0.7 = 적분 0.7 · 걸침 0',
        lambda: (lambda x: math.isclose(x['ratio_lw_over_planes'], 1.0, rel_tol=1e-12) and math.isclose(x['both_in_mpa'], 1.7 / 0.6 * 1e-6, rel_tol=1e-12)
                 and math.isclose(x['edge_lw_mpa'], 0.7 / 0.6 * 1e-6, rel_tol=1e-12)
                 and math.isclose(x['edge_integral_mpa'], 0.7 / 0.6 * 1e-6, rel_tol=1e-12) and x['span_integral_mpa'] == 0.0)(_ok(alP)['cross_check']))
    #  혼합 기둥 (창 경계가 가지를 자른다) — 손 계산 −T_zz: id 2 = 0.8 · id 3 = 0.7 (AM_P) · id 4 = 0.25 · id 5 = 0.2 (SE)
    alM = _try(lambda: stress_alpha(arM, crM, TM, oM, box, 1.0))
    m_all = (1.5 + 0.45) / (2 * VA + 2 * VB)
    chk('T12 혼합 기둥: α AM_P = (1.5 ÷ 2V_A) ÷ ⟨σ⟩ · α SE = (0.45 ÷ 2V_S) ÷ ⟨σ⟩ · 닫힘 1',
        lambda: math.isclose(_ok(alM)['alpha_zz']['AM_P'], 1.5 / (2 * VA) / m_all, rel_tol=1e-12)
        and math.isclose(_ok(alM)['alpha_zz']['SE'], 0.45 / (2 * VB) / m_all, rel_tol=1e-12) and abs(_ok(alM)['closure_zz'] - 1) < 1e-12)
    chk('T12 가장자리 분해: LW = 창 안 두 입자 1.45 + 가장자리 LW 0.5 · 적분 = 1.45 + 가장자리 0.52 + 걸침 0 · LW ÷ 21 단면 = 3.25 ÷ (69/21)',
        lambda: (lambda x: math.isclose(x['both_in_mpa'], 1.45 / 0.6 * 1e-6, rel_tol=1e-12) and math.isclose(x['edge_lw_mpa'], 0.5 / 0.6 * 1e-6, rel_tol=1e-12)
                 and math.isclose(x['edge_integral_mpa'], 0.52 / 0.6 * 1e-6, rel_tol=1e-12) and x['span_integral_mpa'] == 0.0
                 and math.isclose(x['lw_window_sigma_zz_mpa'], 1.95 / 0.6 * 1e-6, rel_tol=1e-12)
                 and math.isclose(x['ratio_lw_over_planes'], (1.95 / 0.6) / (69 / 21), rel_tol=1e-12)
                 and x['n_contacts'] == {'both_in': 3, 'edge': 2, 'span': 0}
                 and x['lw_identity_rel'] < 1e-12 and x['integral_identity_rel'] < 1e-12)(_ok(alM)['cross_check']))
    #  얇은 창 (판 0.5 · r_max 0.1 → 창 [0.2, 0.3] · H < 2 r_max = real14 꼴): AM_P 둘 (중심 0.15 · 0.33) 이 창 전체를 걸친다
    pT, kT = _vcol(10, 3, 0.7, 0.5, [0.1775, 0.2275, 0.2775, 0.3275], 0.025, 1.0)
    aT, cT, arT, crT = _lw_case([(1, 1, 0.2, 0.5, 0.15, 0.1), (2, 1, 0.2, 0.5, 0.33, 0.1)] + pT,
                                [(1, 2, (0.0, 0.0, -2.0), (0.2, 0.5, 0.24))] + kT)
    oT = compute(aT, cT, TM, 0.5, box, 1.0)
    alT = _try(lambda: stress_alpha(arT, crT, TM, oT, box, 1.0))
    chk('T12 얇은 창: AM_P 두 입자 모두 창 밖 → α AM_P · α AM = null (상은 있다) · α SE = 1 · 단면 기여 AM–AM 2/3',
        lambda: _ok(alT)['status'] == 'OK' and _ok(alT)['n_window'] == {'SE': 2} and _ok(alT)['alpha_zz']['AM_P'] is None
        and _ok(alT)['alpha_zz']['AM'] is None and math.isclose(_ok(alT)['alpha_zz']['SE'], 1.0, rel_tol=1e-12)
        and math.isclose(oT['contribution_sigma_zz_pct']['AM–AM'], 200 / 3, rel_tol=1e-12))
    chk('T12 창 전체를 걸친 접촉 (두 입자 모두 창 밖) = 적분에만 0.2 · LW 0.1 ↔ 적분 0.3 · LW ÷ 21 단면 = 1/3',
        lambda: (lambda x: math.isclose(x['span_integral_mpa'], 0.2 / 0.1 * 1e-6, rel_tol=1e-9) and x['n_contacts']['span'] == 1
                 and math.isclose(x['lw_window_sigma_zz_mpa'], 0.1 / 0.1 * 1e-6, rel_tol=1e-9)
                 and math.isclose(x['window_integral_sigma_zz_mpa'], 0.3 / 0.1 * 1e-6, rel_tol=1e-9)
                 and math.isclose(x['ratio_lw_over_planes'], 1 / 3, rel_tol=1e-9))(_ok(alT)['cross_check']))
    #  가로 쌍 (SE r 0.025 둘 · z 0.5 · 가로 압축 0.5 · 수직 하중 0) 을 평행 기둥에 더한다 — α_zz ≠ α_p
    hP = [(200, 3, 0.40, 0.2, 0.5, 0.025), (201, 3, 0.45, 0.2, 0.5, 0.025)]
    hK = [(200, 201, (-0.5, 0.0, 0.0), (0.425, 0.2, 0.5))]
    aH, cH, arH, crH = _lw_case(pA + pB + hP, kA + kB + hK)
    oH = compute(aH, cH, TM, 1.0, box, 1.0)
    alH = _try(lambda: stress_alpha(arH, crH, TM, oH, box, 1.0))
    VC = 4 / 3 * math.pi * 0.025 ** 3
    zz_all, zz_se = (1.8 + 0.6) / (3 * VA + 6 * VB + 2 * VC), 0.6 / (6 * VB + 2 * VC)            # −Σ T_zz ÷ Σ V
    p_all, p_se = (1.8 + 0.6 + 0.025) / (3 * VA + 6 * VB + 2 * VC), (0.6 + 0.025) / (6 * VB + 2 * VC)  # −Σ tr T ÷ Σ V
    chk('T12 가로 쌍: α_zz SE = ⟨σ_zz⟩ 비 · α_p SE = ⟨p⟩ 비 (서로 다르다) · 단면 기여는 그대로 75 %',
        lambda: math.isclose(_ok(alH)['alpha_zz']['SE'], zz_se / zz_all, rel_tol=1e-12) and math.isclose(_ok(alH)['alpha_p']['SE'], p_se / p_all, rel_tol=1e-12)
        and not math.isclose(_ok(alH)['alpha_zz']['SE'], _ok(alH)['alpha_p']['SE'], rel_tol=1e-3)
        and math.isclose(oH['contribution_sigma_zz_pct']['AM–AM'], 75.0, rel_tol=1e-12))
    aZ, cZ, arZ, crZ = _lw_case(hP, hK)
    oZ = compute(aZ, cZ, TM, 1.0, box, 1.0)
    alZ = _try(lambda: stress_alpha(arZ, crZ, TM, oZ, box, 1.0))
    chk('T12 수직 하중 0 → α_zz UNDEFINED (값 null · 0 으로 채우지 않음) · α_p SE = 1 · 단면 기여 null',
        lambda: _ok(alZ)['status'].startswith('UNDEFINED') and all(v is None for v in _ok(alZ)['alpha_zz'].values())
        and math.isclose(_ok(alZ)['alpha_p']['SE'], 1.0, rel_tol=1e-12) and oZ['contribution_sigma_zz_pct'] is None)
    alF = _try(lambda: stress_alpha(arP, [{k: v for k, v in q.items() if not k.startswith('cp_')} for q in crP], TM, oP, box, 1.0))
    chk('T12 접촉점 열 없음 → α NOT_COMPUTED (봉인 함수 사유 그대로) · α 값 없음',
        lambda: _ok(alF)['status'].startswith('NOT_COMPUTED') and 'cp_x' in _ok(alF)['status'] and _ok(alF).get('alpha_zz') is None)
    alA = _try(lambda: stress_alpha(arP, crP, {1: 'AM', 3: 'SE'}, compute(aP, cP, {1: 'AM', 3: 'SE'}, 1.0, box, 1.0), box, 1.0))
    chk('T12 mono 이름 (1:AM · 3:SE) → α AM = 0.9375 · α AM_P · AM_S = null · 닫힘 1',
        lambda: math.isclose(_ok(alA)['alpha_zz']['AM'], 0.9375, rel_tol=1e-12) and _ok(alA)['alpha_zz']['AM_P'] is None
        and _ok(alA)['alpha_zz']['AM_S'] is None and abs(_ok(alA)['closure_zz'] - 1) < 1e-12)

    # ══ T13 배치 파일 끝까지 (fx · 접촉점 열 → 봉인 로더 analyze_contacts → 봉인 Love–Weber → α 슬라이드) ═══════════════
    exp_al_comment = 'α = ⟨σ_zz⟩_phase / ⟨σ_zz⟩_all (부피 가중 · Love–Weber 입자 응력 · 단면 창 안 입자) — α < 1 = 평균보다 덜 눌림'
    pS, kS = _vcol(1, 3, 0.5, 0.5, [0.05 + 0.1 * k for k in range(10)], 0.05, 2.0)
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        (td / 'network_cases.tsv').write_text('case_id\tP_S\nP1\t7:3\nS1\t0:10\n', encoding='utf-8')
        for cid, parts, cons in (('P1', pA + pB, kA + kB), ('S1', pS, kS)):
            rd = td / 'work' / 'results' / cid
            up = td / 'work' / 'uploads' / cid
            rd.mkdir(parents=True)
            up.mkdir(parents=True)
            with open(rd / 'atoms.csv', 'w', newline='') as fh:
                w = csv.writer(fh)
                w.writerow(['id', 'type', 'x', 'y', 'z', 'radius'])
                w.writerows([list(p) for p in parts])
            with open(rd / 'contacts.csv', 'w', newline='') as fh:
                w = csv.writer(fh)
                w.writerow(['id1', 'id2', 'fx', 'fy', 'fz', 'fn_x', 'fn_y', 'fn_z', 'ft_x', 'ft_y', 'ft_z', 'contact_area', 'delta',
                            'cp_x', 'cp_y', 'cp_z'])
                w.writerows([[q[0], q[1], *q[2], *q[2], 0.0, 0.0, 0.0, 1e-3, 1e-3, *q[3]] for q in cons])
            (rd / 'mesh_info.json').write_text(json.dumps({'plate_z': 1.0}), encoding='utf-8')
            (rd / 'input_params.json').write_text(json.dumps({'box_x': 1.0, 'box_y': 1.0}), encoding='utf-8')
            (up / 'meta.json').write_text(json.dumps({'type_map_resolved': '1:AM_P,2:AM_S,3:SE', 'scale': 1}), encoding='utf-8')
        out = td / 'out'
        RB = _try(lambda: run_batch(td, out))
        al_lines = _try(lambda: (out / 'stress_reduction_slide.csv').read_text(encoding='utf-8').splitlines())
        smB = _try(lambda: list(csv.reader(open(out / 'plane_load_summary.csv', encoding='utf-8'))))
        chk('T13 배치 (fx · 접촉점 열 · 봉인 로더): 두 케이스 α 상태 OK', lambda: [_ok(RB)['cases'][l]['alpha']['status'] for l in ('0:10', '7:3')] == ['OK', 'OK'])
        chk('T13 stress_reduction_slide.csv 머리 세 줄 (PC:SC · α AM_P · α AM_S · α SE · α AM · 단위 - · 주석)',
            lambda: _ok(al_lines)[0] == 'PC:SC,α AM_P,α AM_S,α SE,α AM' and _ok(al_lines)[1] == 'wt%,-,-,-,-'
            and _ok(al_lines)[2] == '조성,' + ','.join([exp_al_comment] * 4))
        chk('T13 α 값 행: 0:10 = 없는 상 빈칸 · SE 1 / 7:3 = 0.9375 · 빈칸 · 1.25 · 0.9375',
            lambda: _ok(al_lines)[3:] == ['0:10,,,1.0000,', '7:3,0.9375,,1.2500,0.9375'])
        chk('T13 요약 α 열 · 닫힘 · LW ÷ 단면 · α 상태',
            lambda: (lambda h, r7: r7[h.index('α AM_P')] == '0.9375' and r7[h.index('α closure')] == '1.0000'
                     and r7[h.index('LW σzz / planes')] == '1.0000' and r7[h.index('α status')] == 'OK')(
                _ok(smB)[0], [q for q in _ok(smB) if q and q[0] == '7:3'][0]))
    n_ok = sum(1 for _, v in res if v)
    print(f'plane_load_share selftest {n_ok}/{len(res)}')
    return n_ok == len(res)


def main(argv=None):
    ap = argparse.ArgumentParser(description='단면 하중 몫 — 수평 단면을 지나는 수직 하중의 접촉 종류별 몫 (읽기 전용)')
    ap.add_argument('--batch', help='망 배치 폴더 (network_cases.tsv · work/results · work/uploads)')
    ap.add_argument('--case', help='결과 폴더 하나 (atoms.csv · contacts.csv · mesh_info.json · input_params.json)')
    ap.add_argument('--meta', help='--case 의 meta.json (type map · scale)')
    ap.add_argument('--label', default='case', help='--case 의 이름 (예: 7:3)')
    ap.add_argument('--scale', type=float, help='덱 축척 (meta.json 과 다르면 거부)')
    ap.add_argument('--out', help='출력 폴더')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return 0 if selftest() else 1
    if not a.out or not (a.batch or (a.case and a.meta)):
        ap.error('--out 과 (--batch 또는 --case + --meta) 가 필요하다')
    if a.batch:
        R = run_batch(a.batch, a.out, a.scale)
    else:
        r = run_one(a.case, a.meta, a.scale)
        R = {'tool': 'plane_load_share', 'tolerances': {'conservation': CONSERVE_TOL, 'balance': BALANCE_TOL}, 'n_cuts': N_CUTS,
             'code_sha256': _sha(Path(__file__)), 'order': [a.label], 'cases': {a.label: r}}
        write_outputs(R, a.out)
    print_report(R)
    bad = [l for l in R['order'] if R['cases'][l].get('status') != 'OK']
    print(f'→ {a.out} · 상태 OK {len(R["order"]) - len(bad)} / {len(R["order"])}' + (f' (OK 아님: {", ".join(bad)})' if bad else ''))
    return 0 if not bad else 2


if __name__ == '__main__':
    sys.exit(main())
