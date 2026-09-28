#!/usr/bin/env python3
"""lhs_contact_audit.py — LHS 접촉 덤프 **읽기 전용** 점검 (J20-a ⓐ · 1저자 비준 2026-09-28 밤 *"권고하는걸로 진행하자"*).

왜 — 인계표의 웹앱 CN · 접촉 수 열 (`dem_analysis_core.calc_se_se_cn` · `calc_am_isolation_risk` · `calc_am_am_cn` ·
`calc_interface_area`) 은 접촉 덤프의 **행을 거르지 않고** 행마다 두 입자에 +1 한다.  웹앱 파서는 파일 안 **모든 프레임을
이어 붙인다** (DESC-06 — 합성 2 프레임에서 SE-SE CN 정확히 2 배).  ⇒ 값을 뽑기 전에 입력이 "한 프레임 · 쌍마다 한 행 ·
접촉만" 인지 원자료에서 센다.  **인계 값은 만들지 않는다.**

케이스마다 (코호트 봉인 파일 — 수확과 같은 atom · contact · 같은 step mesh):
  ① 프레임 수 — 접촉 `ITEM: ENTRIES` · 원자 `ITEM: TIMESTEP`
  ② 마지막 프레임의 중복 무순서 쌍 · 자기쌍 · δ ≤ 0 행 · 주기 플래그 (`c_cpl[9]`) 행  (`lhs_descriptor_harvest.scan_contact_dump`)
  ③ ★ **기하 재계수** (1저자 09-28 밤: *"contact 파일에 flag 로 잘 되어 있으니 그걸로 판단해서 CN 확인하면 되지 않나"*) —
     원자 좌표로 x·y **최소 영상** (z 개방) 겹침 쌍을 다시 세어 (`lhs_perc_extract._pairs_within`) 덤프 쌍과 **쌍 단위로** 맞댄다:
     기하에만 · 덤프에만 있는 쌍 · 경계를 넘는 기하 쌍 ↔ 주기 플래그 행 (쌍마다) · 상별 CN (덤프 행 = 웹앱 방식 / 기하).
     접촉 판정 경계 (|d − (r_i + r_j)| ≤ 1e-6·(r_i + r_j)) 의 쌍은 출력 자릿수로 갈릴 수 있어 **따로** 센다.
  ④ 상별 바닥 벽 · 플래튼 접촉 입자 비율 (`lhs_descriptor_harvest.wall_touch_fractions` — J20-a ⓓ 새 열과 **같은 함수**).
     ⚠ 옆면 (x·y) 은 주기 경계라 ③ 이 검증하지만, 바닥 벽 · 플래튼 (z) 은 주기가 아니다 — 그 너머에 입자가 없어 CN 이 낮은 것은
     **정의상** 그렇다 (결함 아님).  ④ 는 그 몫을 가르는 설명 변수다.

출력: <out>/contact_audit.tsv (케이스당 한 행) · contact_audit.json (행 + 요약 + 실행 정보).
rc 0 = 전부 깨끗 · rc 3 = ①②③ 중 하나라도 어긋난 케이스가 있다 (보고용 — 거부는 배치 관문 `lhs_webapp_batch` 가 한다) ·
rc 2 = 입력 오류 (코호트 · 경로).

    python3 scripts/lhs_contact_audit.py --out ~/lhs_contact_audit_$(date +%Y%m%d)        # 코호트 전 건 (수 분)
    python3 scripts/lhs_contact_audit.py --case lhs00_000 --out /tmp/audit_one             # 한 건
    python3 scripts/lhs_contact_audit.py --selftest
"""
from __future__ import annotations

import argparse
import csv
import datetime
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

_SCR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCR))
import lhs_descriptor_harvest as H                      # noqa: E402  같은 읽기 · 같은 규칙 (규율 ①)
import lhs_harvest_batch as HB                          # noqa: E402  코호트 · 경로 치환 · 같은 step 메시
from lhs_perc_extract import BedRefusal, read_atom_dump, _pairs_within   # noqa: E402

SCHEMA = 'lhs_contact_audit/v1'
#: 접촉 판정 경계 — 덤프 좌표 자릿수로 δ ≈ 0 쌍은 어느 쪽으로도 갈릴 수 있다 (불일치로 세지 않고 따로 센다).
NEAR_REL = 1e-6
TSV_COLS = (
    'case', 'design_family', 'n_types', 'n_atoms', 'status', 'verdict', 'why',
    'contact_frames', 'atom_frames', 'rows_last', 'unique_pairs', 'dup_pairs', 'dup_rows', 'self_pairs',
    'delta_nonpos', 'delta_min', 'periodic_rows',
    'geom_pairs', 'geom_only', 'dump_only', 'mismatch_near_threshold',
    'geom_cross', 'flag_and_cross', 'flag_not_cross', 'cross_not_flag',
    'cn_se_se_dump', 'cn_se_se_geom', 'cn_am_se_dump', 'cn_am_se_geom', 'cn_am_am_dump', 'cn_am_am_geom',
    'wt_SE_floor', 'wt_SE_plate', 'wt_AM_P_floor', 'wt_AM_P_plate', 'wt_AM_S_floor', 'wt_AM_S_plate',
    'wt_AM_floor', 'wt_AM_plate',
)


def _cn(labels, idx_i, idx_j, ph_a, ph_b):
    """무순서 쌍 (i, j) 목록 → 상 ph_a 입자당 상 ph_b 이웃 수 평균 (ph_a 전 입자 · 접촉 0 포함 — 웹앱과 같은 분모)."""
    in_a = np.asarray([l in ph_a for l in labels])
    in_b = np.asarray([l in ph_b for l in labels])
    n_a = int(in_a.sum())
    if n_a == 0:
        return None
    cnt = np.zeros(len(labels), dtype=np.int64)
    m1 = in_a[idx_i] & in_b[idx_j]
    m2 = in_a[idx_j] & in_b[idx_i]
    np.add.at(cnt, idx_i[m1], 1)
    np.add.at(cnt, idx_j[m2], 1)
    return float(cnt[in_a].sum() / n_a)


def audit_case(atom_path, contact_path, n_types, mesh_path=None):
    """한 케이스 — 읽기만 한다.  반환 dict (TSV_COLS 키 + 세부)."""
    out = {}
    scan = H.scan_contact_dump(contact_path)
    out.update(contact_frames=scan['n_frames'], rows_last=scan['n_rows_last'], unique_pairs=scan['n_unique_pairs'],
               dup_pairs=scan['n_dup_pairs'], dup_rows=scan['n_dup_rows'], self_pairs=scan['n_self_pairs'],
               delta_nonpos=scan['n_delta_nonpos'], delta_min=scan['delta_min'], periodic_rows=scan['n_periodic_flag'])
    out['atom_frames'] = H.count_blocks(atom_path, 'ITEM: TIMESTEP')

    atoms, lo, hi, _bc = read_atom_dump(atom_path)
    ids = H._atom_ids(atom_path)
    labels, _tmap = H.phase_labels(atoms['type'], int(n_types))
    labels = [str(l) for l in labels]
    n = len(ids)
    out['n_atoms'] = n
    lx, ly = float(hi[0] - lo[0]), float(hi[1] - lo[1])
    xyz = np.column_stack([atoms['x'], atoms['y'], atoms['z']])
    r = atoms['radius']

    #  ③ 기하 재계수 — x·y 최소 영상 · z 개방 (수확의 퍼콜 그래프와 같은 함수)
    gp = _pairs_within(xyz, r, lx, ly, 0.0)
    gi, gj = (gp[:, 0].astype(np.int64), gp[:, 1].astype(np.int64)) if len(gp) else (np.empty(0, np.int64),) * 2
    pos = {int(a): k for k, a in enumerate(ids)}
    c1, c2, _ca, _hd, ex = H.read_contact_dump(contact_path, extra_cols=(H.COL_PERIODIC,))
    known = np.asarray([(int(a) in pos) and (int(b) in pos) for a, b in zip(c1, c2)], dtype=bool)
    out['orphan_rows'] = int((~known).sum())
    di = np.asarray([pos[int(a)] for a in c1[known]], dtype=np.int64)
    dj = np.asarray([pos[int(b)] for b in c2[known]], dtype=np.int64)
    flag = ex[H.COL_PERIODIC]
    flag = None if flag is None else flag[known]

    def key(i, j):
        return (min(int(i), int(j)), max(int(i), int(j)))

    gset = {key(a, b) for a, b in zip(gi, gj)}
    dset = {key(a, b) for a, b in zip(di, dj)}
    only_g, only_d = gset - dset, dset - gset

    def gap(k):
        a, b = k
        d = xyz[b] - xyz[a]
        d[0] -= lx * np.round(d[0] / lx)
        d[1] -= ly * np.round(d[1] / ly)
        return float(np.linalg.norm(d) - (r[a] + r[b])), float(r[a] + r[b])

    near = sum(1 for k in (only_g | only_d) if abs(gap(k)[0]) <= NEAR_REL * gap(k)[1])
    out.update(geom_pairs=len(gset), geom_only=len(only_g), dump_only=len(only_d), mismatch_near_threshold=int(near))

    def crosses(a, b):
        return abs(xyz[b, 0] - xyz[a, 0]) > lx / 2 or abs(xyz[b, 1] - xyz[a, 1]) > ly / 2

    gcross = {k for k in gset if crosses(*k)}
    out['geom_cross'] = len(gcross)
    if flag is not None:
        fset = {key(a, b) for a, b, f in zip(di, dj, flag) if f != 0.0}
        dcross = {k for k in dset if crosses(*k)}
        out.update(flag_and_cross=len(fset & dcross), flag_not_cross=len(fset - dcross), cross_not_flag=len(dcross - fset))
    else:
        out.update(flag_and_cross=None, flag_not_cross=None, cross_not_flag=None)

    AM = {'AM', 'AM_P', 'AM_S'}
    for nm, pa, pb in (('se_se', {'SE'}, {'SE'}), ('am_se', AM, {'SE'}), ('am_am', AM, AM)):
        out[f'cn_{nm}_dump'] = _cn(labels, di, dj, pa, pb)          # 덤프 **행** 기준 (중복 행 포함) = 웹앱 방식 (마지막 프레임)
        out[f'cn_{nm}_geom'] = _cn(labels, gi, gj, pa, pb)          # 기하 기준

    if mesh_path is not None:
        pz = H.plate_z_from_stl(str(mesh_path))
        wt = H.wall_touch_fractions(labels, atoms['z'], r, pz)
        for ph in ('SE', 'AM_P', 'AM_S', 'AM'):
            for side in ('floor', 'plate'):
                out[f'wt_{ph}_{side}'] = (wt.get(ph) or {}).get(side)
        out['plate_z_sim'] = pz

    bad = []
    if out['contact_frames'] != 1:
        bad.append(f"접촉 프레임 {out['contact_frames']}")
    if out['atom_frames'] != 1:
        bad.append(f"원자 프레임 {out['atom_frames']}")
    if out['dup_rows']:
        bad.append(f"중복 행 {out['dup_rows']}")
    if out['self_pairs']:
        bad.append(f"자기쌍 {out['self_pairs']}")
    if out['orphan_rows']:
        bad.append(f"고아 행 {out['orphan_rows']}")
    far = len(only_g) + len(only_d) - near
    if far:
        bad.append(f'기하≠덤프 쌍 {far} (기하에만 {len(only_g)} · 덤프에만 {len(only_d)} · 경계 {near})')
    if out['delta_nonpos']:
        bad.append(f"δ≤0 행 {out['delta_nonpos']}")
    if flag is not None and (out['flag_not_cross'] or out['cross_not_flag']):
        bad.append(f"주기 플래그≠경계 넘음 (플래그만 {out['flag_not_cross']} · 넘음만 {out['cross_not_flag']})")
    out['verdict'] = 'CLEAN' if not bad else 'FLAG'
    out['why'] = ' · '.join(bad)
    return out


def _write(out_dir: Path, rows, meta):
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / 'contact_audit.tsv').open('w', encoding='utf-8', newline='') as fh:
        w = csv.writer(fh, delimiter='\t')
        w.writerow(TSV_COLS)
        for r in rows:
            w.writerow(['' if r.get(c) is None else r.get(c) for c in TSV_COLS])
    (out_dir / 'contact_audit.json').write_text(
        json.dumps(dict(schema=SCHEMA, meta=meta, rows=rows), ensure_ascii=False, indent=1, default=str) + '\n',
        encoding='utf-8')


def _summary(rows):
    s = dict(n=len(rows), status={}, verdict={})
    for r in rows:
        s['status'][r['status']] = s['status'].get(r['status'], 0) + 1
        if r['status'] == 'OK':
            s['verdict'][r['verdict']] = s['verdict'].get(r['verdict'], 0) + 1
    ok = [r for r in rows if r['status'] == 'OK']
    for k in ('contact_frames', 'atom_frames', 'dup_rows', 'self_pairs', 'delta_nonpos', 'geom_only', 'dump_only',
              'mismatch_near_threshold', 'flag_not_cross', 'cross_not_flag', 'orphan_rows'):
        vals = [r.get(k) for r in ok if r.get(k) is not None]
        s[k] = dict(max=(max(vals) if vals else None), n_nonzero=sum(1 for v in vals if v and (k not in ('contact_frames', 'atom_frames') or v != 1)))
    s['n_periodic_rows_total'] = sum(int(r.get('periodic_rows') or 0) for r in ok)
    s['n_geom_cross_total'] = sum(int(r.get('geom_cross') or 0) for r in ok)
    return s


def run(args):
    cohort = Path(args.cohort)
    rows = HB.read_cohort(cohort)
    if not rows:
        print(f'⛔ 코호트가 0 행이다 — {cohort}', file=sys.stderr)
        return 2
    if args.case:
        want = set(args.case)
        rows = [r for r in rows if r['case'] in want]
        if len(rows) != len(want):
            print(f'⛔ 코호트에 없는 case: {sorted(want - {r["case"] for r in rows})}', file=sys.stderr)
            return 2
    out = []
    for k, row in enumerate(rows, 1):
        rec = dict(case=row['case'], design_family=row.get('design_family'), n_types=row.get('n_types'), status='OK',
                   verdict='', why='')
        atom = HB.remap(row['atom_file'], args.root_from, args.root_to)
        contact = HB.remap(row['contact_file'], args.root_from, args.root_to)
        try:
            for lab, p in (('atom', atom), ('contact', contact)):
                if not p.is_file():
                    raise BedRefusal(f'{lab} 파일 없음: {p}')
            mesh, pick, why = HB.pick_mesh(atom)
            rec['mesh_pick'] = pick
            rec.update(audit_case(str(atom), str(contact), int(row['n_types']), mesh))
            if mesh is None:
                rec['why'] = (rec['why'] + ' · ' if rec['why'] else '') + f'메시 없음 ({why}) — 벽 접촉 비율 없음'
        except (BedRefusal, OSError, ValueError, KeyError) as e:
            rec.update(status='INPUT_ERROR', verdict='', why=str(e))
        out.append(rec)
        print(f"  [{k}/{len(rows)}] {rec['case']}: {rec['status']} {rec.get('verdict', '')} {rec.get('why', '')}"[:220])
    s = _summary(out)
    meta = dict(generated=datetime.datetime.now().isoformat(timespec='seconds'), cohort=str(cohort),
                root_from=args.root_from, root_to=args.root_to, near_rel=NEAR_REL,
                code=_git_rev(), summary=s)
    _write(Path(args.out), out, meta)
    print(f"→ {args.out}/contact_audit.tsv · contact_audit.json\n  요약: {json.dumps(s, ensure_ascii=False)}")
    if s['status'].get('INPUT_ERROR'):
        return 2
    return 3 if s['verdict'].get('FLAG') else 0


def _git_rev():
    try:
        rev = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=str(_SCR), capture_output=True, text=True).stdout.strip()
        dirty = bool(subprocess.run(['git', 'status', '--porcelain', '--untracked-files=no'], cwd=str(_SCR),
                                    capture_output=True, text=True).stdout.strip())
        return dict(sha=rev or None, dirty=dirty)
    except OSError:
        return dict(sha=None, dirty=None)


# ──────────────────────────────────────────────────────────────────────────────
# 자기검사 — 반례를 합성 덤프로 심고 잡히는지 본다
# ──────────────────────────────────────────────────────────────────────────────
def _atoms(tmp, rows, lx=10.0, ly=10.0, lz=20.0, name='atom_100.liggghts', frames=1):
    """rows = (id, x, y, z, radius, type)"""
    p = os.path.join(tmp, name)
    with open(p, 'w') as fh:
        for f in range(frames):
            fh.write(f'ITEM: TIMESTEP\n{100 * (f + 1)}\nITEM: NUMBER OF ATOMS\n{len(rows)}\n')
            fh.write(f'ITEM: BOX BOUNDS pp pp ff\n0 {lx}\n0 {ly}\n0 {lz}\n')
            fh.write('ITEM: ATOMS id x y z radius type\n')
            for rr in rows:
                fh.write(' '.join(str(x) for x in rr) + '\n')
    return p


def _contacts(tmp, rows, name='contact_100.liggghts', frames=1):
    """rows = (id1, id2, periodic_flag, area, delta)"""
    p = os.path.join(tmp, name)
    hd = ['c_cpl[7]', 'c_cpl[8]', 'c_cpl[9]', 'c_cpl[22]', 'c_cpl[23]']
    with open(p, 'w') as fh:
        for f in range(frames):
            fh.write(f'ITEM: TIMESTEP\n{100 * (f + 1)}\nITEM: NUMBER OF ENTRIES\n{len(rows)}\n')
            fh.write('ITEM: BOX BOUNDS pp pp ff\n0 10\n0 10\n0 20\n')
            fh.write('ITEM: ENTRIES ' + ' '.join(hd) + '\n')
            for rr in rows:
                fh.write(' '.join(str(x) for x in rr) + '\n')
    return p


def selftest():
    fails = []

    def chk(name, ok):
        print(('  ✓ ' if ok else '  ✗ ') + name)
        if not ok:
            fails.append(name)

    #  침대: 반경 1 · 상자 10×10×20 (xy 주기).  1–2 는 x 경계를 넘어 접촉 (x = 0.5 · 9.7 → 최소영상 거리 0.8 < 2),
    #  2–3 은 안쪽 접촉 (거리 1.9) · 4 는 외톨이 · 5 는 플래튼 (z 20) 에 닿는다 · 1 · 2 · 3 은 바닥 (z − r ≤ 0) 에 닿는다.
    #  type 1 = AM_P · 2 = AM_S · 3 = SE
    A = [(1, 0.5, 5.0, 0.9, 1.0, 3), (2, 9.7, 5.0, 0.9, 1.0, 3), (3, 7.8, 5.0, 0.9, 1.0, 1),
         (4, 5.0, 1.5, 10.0, 1.0, 2), (5, 5.0, 8.5, 19.5, 1.0, 3)]
    clean = [(1, 2, 1, 0.1, 0.2), (2, 3, 0, 0.1, 0.1)]
    with tempfile.TemporaryDirectory() as td:
        stl = H._stl(td, z=20.0)
        a1 = _atoms(td, A)
        r = audit_case(a1, _contacts(td, clean), 3, stl)
        chk('① 깨끗한 침대 → CLEAN (프레임 1 · 중복 0 · 기하 = 덤프 · 플래그 = 경계 넘음)', r['verdict'] == 'CLEAN' and r['why'] == '')
        chk('①b 경계를 넘는 기하 쌍 1 = 플래그 행 1 (쌍 단위로 일치)',
            r['geom_cross'] == 1 and r['flag_and_cross'] == 1 and r['flag_not_cross'] == 0 and r['cross_not_flag'] == 0)
        chk('①c CN: SE-SE 덤프 = 기하 = 2/3 (SE 3 개 · 1–2 쌍 하나 · 외톨이 5 포함 분모)',
            abs(r['cn_se_se_dump'] - 2 / 3) < 1e-12 and abs(r['cn_se_se_geom'] - 2 / 3) < 1e-12)
        chk('①d 벽 접촉 비율: SE 바닥 2/3 · 플래튼 1/3 · AM_P 바닥 1 · AM_S 0 · AM (합친) 바닥 1/2',
            abs(r['wt_SE_floor'] - 2 / 3) < 1e-12 and abs(r['wt_SE_plate'] - 1 / 3) < 1e-12
            and r['wt_AM_P_floor'] == 1.0 and r['wt_AM_S_floor'] == 0.0 and abs(r['wt_AM_floor'] - 0.5) < 1e-12)

        r2 = audit_case(a1, _contacts(td, clean, name='contact_2f.liggghts', frames=2), 3, stl)
        chk('② ★ 접촉 프레임 2 개 → FLAG (웹앱 파서는 이어 붙여 CN 이 2 배가 된다)',
            r2['verdict'] == 'FLAG' and r2['contact_frames'] == 2 and '접촉 프레임 2' in r2['why'])

        r3 = audit_case(a1, _contacts(td, clean + [(2, 1, 1, 0.1, 0.2)], name='contact_dup.liggghts'), 3, stl)
        chk('③ ★ 같은 쌍이 두 행 (순서 뒤집힘) → FLAG · 덤프 행 CN > 기하 CN',
            r3['verdict'] == 'FLAG' and r3['dup_rows'] == 1 and r3['cn_se_se_dump'] > r3['cn_se_se_geom'])

        r4 = audit_case(a1, _contacts(td, [(2, 3, 0, 0.1, 0.1)], name='contact_noper.liggghts'), 3, stl)
        chk('④ ★ 경계를 넘는 접촉이 덤프에 없다 → 기하에만 1 · FLAG · 덤프 CN < 기하 CN',
            r4['verdict'] == 'FLAG' and r4['geom_only'] == 1 and r4['cn_se_se_dump'] < r4['cn_se_se_geom'])

        r5 = audit_case(a1, _contacts(td, clean + [(4, 5, 0, 0.0, -0.3)], name='contact_neg.liggghts'), 3, stl)
        chk('⑤ ★ 떨어진 쌍 (δ ≤ 0) 이 행으로 있다 → 덤프에만 1 · δ≤0 1 · FLAG',
            r5['verdict'] == 'FLAG' and r5['dump_only'] == 1 and r5['delta_nonpos'] == 1)

        r6 = audit_case(a1, _contacts(td, [(1, 2, 0, 0.1, 0.2), (2, 3, 1, 0.1, 0.1)], name='contact_badflag.liggghts'), 3, stl)
        chk('⑥ ★ 플래그가 뒤바뀐 덤프 (넘는 쌍 0 · 안쪽 쌍 1) → 플래그만 1 · 넘음만 1 · FLAG',
            r6['verdict'] == 'FLAG' and r6['flag_not_cross'] == 1 and r6['cross_not_flag'] == 1)

        a2 = _atoms(td, A, name='atom_2f.liggghts', frames=2)
        r7 = audit_case(a2, _contacts(td, clean, name='contact_c7.liggghts'), 3, stl)
        chk('⑦ 원자 프레임 2 개 → FLAG (웹앱 atoms.csv 에 id 가 두 번)', r7['verdict'] == 'FLAG' and r7['atom_frames'] == 2)

        #  ⑧ 접촉 판정 경계 쌍 (δ ≈ 0, 출력 자릿수로 갈림) 은 불일치로 세지 않는다
        B = [(1, 3.0, 5.0, 5.0, 1.0, 3), (2, 5.0 + 1e-9, 5.0, 5.0, 1.0, 3)]
        a3 = _atoms(td, B, name='atom_near.liggghts')
        r8 = audit_case(a3, _contacts(td, [(1, 2, 0, 0.0, 1e-9)], name='contact_near.liggghts'), 3, stl)
        chk('⑧ 접촉 판정 경계 쌍 (|d − Σr| ≤ 1e-6·Σr) 은 경계로 따로 센다 · CLEAN',
            r8['mismatch_near_threshold'] == 1 and r8['verdict'] == 'CLEAN')

        #  ⑨ 2-type (mono) 침대 — AM 한 상
        C = [(1, 2.0, 5.0, 0.9, 1.0, 1), (2, 3.8, 5.0, 0.9, 1.0, 2)]
        a4 = _atoms(td, C, name='atom_mono.liggghts')
        r9 = audit_case(a4, _contacts(td, [(1, 2, 0, 0.1, 0.2)], name='contact_mono.liggghts'), 2, stl)
        chk('⑨ 2-type 침대: AM–SE CN 1 · AM_P · AM_S 벽 비율은 빈칸 (N/A · 0 아님)',
            r9['verdict'] == 'CLEAN' and r9['cn_am_se_geom'] == 1.0 and r9['wt_AM_P_floor'] is None and r9['wt_AM_floor'] == 1.0)

        #  ⑩ 웹앱 경로 실증 — 같은 2 프레임 파일을 웹앱 파서로 읽으면 CN 이 정확히 2 배 (감사가 잡는 이유)
        import parse_liggghts as PL
        import dem_analysis_core as C_
        c2f = os.path.join(td, 'contact_2f.liggghts')
        hd, rows = PL.parse_contact_file(c2f)
        cons = [dict(id1=int(float(x[hd.index('id1')])), id2=int(float(x[hd.index('id2')])),
                     contact_area=float(x[hd.index('contact_area')]), delta=float(x[hd.index('delta')])) for x in rows]
        at = {k: dict(id=k, type=t, x=x, y=y, z=z, radius=rad) for (k, x, y, z, rad, t) in A}
        cn2 = C_.calc_se_se_cn(at, cons, [3])['mean']
        chk('⑩ 웹앱 경로 (parse_liggghts → calc_se_se_cn) 는 2 프레임 파일에서 SE-SE CN = 2 × 기하 (4/3 vs 2/3)',
            abs(cn2 - 2 * (2 / 3)) < 1e-12)

        #  ⑪ CLI 한 건 — 코호트 TSV · 산출 파일 · rc
        post = Path(td) / 'cohort' / 'c1' / 'post'
        post.mkdir(parents=True)
        import shutil
        shutil.copy(a1, post / 'atom_100.liggghts')
        shutil.copy(os.path.join(td, 'contact_100.liggghts'), post / 'contact_100.liggghts')
        shutil.copy(stl, post / 'mesh_100.stl')
        tsv = Path(td) / 'cohort.tsv'
        tsv.write_text('# 합성 코호트\ncase\tn_types\tdesign_family\tatom_file\tcontact_file\n'
                       f'c1\t3\tlhs\t{post / "atom_100.liggghts"}\t{post / "contact_100.liggghts"}\n', encoding='utf-8')
        od = Path(td) / 'out'
        rc = main(['--cohort', str(tsv), '--out', str(od)])
        js = json.loads((od / 'contact_audit.json').read_text(encoding='utf-8'))
        chk('⑪ CLI: rc 0 · TSV · JSON (schema · 요약 · 코드 sha 칸)',
            rc == 0 and (od / 'contact_audit.tsv').is_file() and js['schema'] == SCHEMA
            and js['meta']['summary']['verdict'].get('CLEAN') == 1 and 'code' in js['meta'])

    print()
    if fails:
        print(f'✗ {len(fails)} 건 실패')
        return 1
    print('✓ 전부 통과 — 감사기가 반례 (다중 프레임 · 중복 · 주기 누락 · δ≤0 · 플래그 어긋남) 를 잡는다.  '
          '⚠ 실제 130 덤프가 깨끗하다는 뜻은 아니다 (WSL 실행 결과를 볼 것)')
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description='LHS 접촉 덤프 읽기 전용 점검 (J20-a ⓐ) — 프레임 수 · 중복 쌍 · δ≤0 · '
                                             '주기 플래그 ↔ 기하 재계수 · 상별 벽 접촉 비율.  인계 값은 만들지 않는다')
    ap.add_argument('--cohort', default=str(HB.COHORT), help='코호트 TSV (기본: 봉인 area_s2_cohort.tsv)')
    ap.add_argument('--case', action='append', default=[], help='이 case 만 (여러 번 줄 수 있다)')
    ap.add_argument('--root-from', default='', help='코호트 경로 접두사 (치환 전)')
    ap.add_argument('--root-to', default='', help='실제 경로 접두사로 치환')
    ap.add_argument('--out', help='산출 폴더 (contact_audit.tsv · contact_audit.json)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.out:
        ap.error('--out 이 필요하다')
    return run(a)


if __name__ == '__main__':
    sys.exit(main())
