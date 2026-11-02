"""lw_frame.py — 한 contact 덤프 step 의 Love–Weber 입자 von Mises (덱 1–8장 · 16쪽 값과 같은 함수).

같은 함수: scripts/dem_analysis_core.calc_love_weber_stress (run_draft2_metrics 4d 와 같은 호출 · SIM_PA_TO_MPA 1e-3).
같은 파서: scripts/parse_liggghts.parse_atom_file · parse_contact_file → analyze_contacts.load_atoms_raw · load_contacts_raw.
벽 표지: z − r < 0 (바닥) 또는 z + r > 판 높이 (판) — 중앙값은 벽 접촉 입자 제외 (16쪽과 같은 규칙).

위치: contact 덤프의 두 입자 위치 (c_cpl[1–6]) = 그 step 의 정확한 위치 → x·y 를 상자 안으로 접어 같은 id 의 후보가 같은지 확인.
접촉 없는 입자 (응력 0) 만 atom 덤프 위치를 쓴다 (다른 step 이면 표지).  atom step ≠ contact step 이면 c_strs 를 넣지 않는다
(전역 virial 검사는 같은 step 일 때만 — 함수 규약).
"""
import argparse, csv, json, sys, hashlib
from pathlib import Path
import numpy as np

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / 'scripts'))
import parse_liggghts as PL          # noqa: E402
import analyze_contacts as AC        # noqa: E402
import dem_analysis_core as DAC      # noqa: E402

SIM_PA_TO_MPA = 1.0e-3
SCALE_UM = 1000.0                    # sim 길이 × 1000 = µm (run_draft2_metrics meta scale)
TYPE_LABEL = {1: 'AM', 3: 'SE'}


def dump_step(path):
    with open(path) as f:
        for line in f:
            if line.startswith('ITEM: TIMESTEP'):
                return int(next(f).split()[0])
    raise SystemExit(f'{path}: TIMESTEP 없음')


def box_bounds(path):
    with open(path) as f:
        for line in f:
            if line.startswith('ITEM: BOX BOUNDS'):
                return [tuple(map(float, next(f).split()[:2])) for _ in range(3)]
    raise SystemExit(f'{path}: BOX BOUNDS 없음')


def plate_z(stl):
    zs = [float(l.split()[3]) for l in open(stl) if l.strip().startswith('vertex')]
    if not zs or max(zs) - min(zs) > 1e-12 * max(1.0, abs(max(zs))):
        raise SystemExit(f'{stl}: 평평한 판이 아님 (z {min(zs) if zs else None} … {max(zs) if zs else None})')
    return zs[0]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--atom', required=True); ap.add_argument('--contact', required=True)
    ap.add_argument('--mesh', required=True); ap.add_argument('--out', required=True)
    ap.add_argument('--label', required=True); ap.add_argument('--plate-mpa', type=float, default=None,
                    help='그 step 의 판 압력 (로그 thermo) — 기록만')
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)

    s_atom, s_con = dump_step(a.atom), dump_step(a.contact)
    (xlo, xhi), (ylo, yhi), _ = box_bounds(a.atom)
    Lx, Ly = xhi - xlo, yhi - ylo
    pz = plate_z(a.mesh)

    ah, arows = PL.parse_atom_file(a.atom)
    ch, crows = PL.parse_contact_file(a.contact)
    A = {h: k for k, h in enumerate(ah)}
    C = {h: k for k, h in enumerate(ch)}
    for need in ('id', 'type', 'x', 'y', 'z', 'radius'):
        assert need in A, f'atom 열 {need} 없음'
    for need in ('p1_x', 'p1_y', 'p1_z', 'p2_x', 'p2_y', 'p2_z', 'id1', 'id2', 'fx', 'cp_x'):
        assert need in C, f'contact 열 {need} 없음'

    # 같은 step 이면 c_strs 도 (virial 검사) · 아니면 뺀다
    same = (s_atom == s_con)
    keep = ['id', 'type', 'x', 'y', 'z', 'radius'] + ([c for c in ('c_strs[1]', 'c_strs[2]', 'c_strs[3]') if c in A] if same else [])

    # contact 위치 → 상자 안으로 접기 (x·y 주기) · 같은 id 후보 일치 확인
    def wrap(v, lo, L):
        w = (v - lo) % L + lo
        return w
    pos = {}
    maxdev = 0.0
    for r in crows:
        for idk, px, py, pzk in (('id1', 'p1_x', 'p1_y', 'p1_z'), ('id2', 'p2_x', 'p2_y', 'p2_z')):
            i = int(float(r[C[idk]]))
            p = (wrap(float(r[C[px]]), xlo, Lx), wrap(float(r[C[py]]), ylo, Ly), float(r[C[pzk]]))
            if i in pos:
                q = pos[i]
                d = max(min(abs(p[0] - q[0]), Lx - abs(p[0] - q[0])), min(abs(p[1] - q[1]), Ly - abs(p[1] - q[1])), abs(p[2] - q[2]))
                maxdev = max(maxdev, d)
            else:
                pos[i] = p
    n_from_contact = 0
    with open(out / 'atoms.csv', 'w', newline='') as f:
        w = csv.writer(f); w.writerow(keep)
        for r in arows:
            row = [r[A[k]] for k in keep]
            i = int(float(r[A['id']]))
            if i in pos and not same:
                row[2], row[3], row[4] = (repr(v) for v in pos[i]); n_from_contact += 1
            w.writerow(row)
    with open(out / 'contacts.csv', 'w', newline='') as f:
        w = csv.writer(f); w.writerow(ch); w.writerows(crows)

    atoms_raw, _ = AC.load_atoms_raw(str(out / 'atoms.csv'))
    contacts_raw, _ = AC.load_contacts_raw(str(out / 'contacts.csv'))
    (out / 'atoms.csv').unlink(); (out / 'contacts.csv').unlink()          # 중간 CSV (덤프 그대로 옮긴 것) — 디스크 아끼기
    type_map = {t: TYPE_LABEL[t] for t in sorted({v['type'] for v in atoms_raw.values()})}
    lw = DAC.calc_love_weber_stress(atoms_raw, contacts_raw, type_map, pz, box_x=Lx, box_y=Ly,
                                    plate_z_source='mesh', return_arrays=True)
    if lw['status'] != 'OK':
        raise SystemExit(f'LW 상태 {lw["status"]}')
    vm = dict(zip(lw['ids'], np.asarray(lw['arrays_vm'], float) * SIM_PA_TO_MPA))
    # P_ref = ⟨σzz⟩ 상자 평균 (압축 양수) = −Σ V_i σ_i,zz / (Lx · Ly · 판 높이) — 웹앱 viewer3d_data._p_ref_block 과 같은 정의 (힘 평형 확인용)
    T = np.asarray(lw['tensor'], float)
    rad = np.array([atoms_raw[i]['radius'] for i in lw['ids']], float)
    p_ref = float(-np.sum((4.0 / 3.0) * np.pi * rad ** 3 * T[:, 2, 2]) / (Lx * Ly * pz) * SIM_PA_TO_MPA)
    H = pz * SCALE_UM
    ncon = {}
    for c in contacts_raw:
        ncon[c['id1']] = ncon.get(c['id1'], 0) + 1; ncon[c['id2']] = ncon.get(c['id2'], 0) + 1
    rows = []
    for i, at in sorted(atoms_raw.items()):
        z, r = at['z'] * SCALE_UM, at['radius'] * SCALE_UM
        rows.append(dict(id=i, type=at['type'], phase=type_map[at['type']], x_um=at['x'] * SCALE_UM, y_um=at['y'] * SCALE_UM,
                         z_um=z, r_um=r, vm_MPa=float(vm[i]), wall=int(z - r < 0.0 or z + r > H), n_contacts=ncon.get(i, 0)))
    with open(out / f'particles_{a.label}.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

    summ = dict(label=a.label, step_atom=s_atom, step_contact=s_con, same_step=same, plate_mpa_log=a.plate_mpa,
                plate_z_um=H, box_um=[Lx * SCALE_UM, Ly * SCALE_UM], n_particles=len(rows), n_contacts=len(contacts_raw),
                pos_from_contact=n_from_contact, pos_candidate_maxdev_um=maxdev * SCALE_UM,
                lw_status=lw['status'], lw_vm_cv=lw['vm_cv'], virial=lw['checks'].get('virial_status'), p_ref_MPa=p_ref,
                files={k: dict(path=v, sha256=sha(v)) for k, v in (('atom', a.atom), ('contact', a.contact), ('mesh', a.mesh))})
    for ph in ('AM', 'SE'):
        v = np.array([r['vm_MPa'] for r in rows if r['phase'] == ph and not r['wall']])
        summ[ph] = dict(n=int(v.size), n_wall=int(sum(1 for r in rows if r['phase'] == ph and r['wall'])),
                        median=float(np.median(v)), p10=float(np.percentile(v, 10)), p90=float(np.percentile(v, 90)),
                        p99=float(np.percentile(v, 99)), max=float(v.max()))
        if a.plate_mpa:
            summ[ph]['median_over_P'] = summ[ph]['median'] / a.plate_mpa
    (out / f'summary_{a.label}.json').write_text(json.dumps(summ, ensure_ascii=False, indent=1))
    print(json.dumps({k: summ[k] for k in ('label', 'step_atom', 'step_contact', 'plate_mpa_log', 'n_particles', 'n_contacts',
                                         'pos_from_contact', 'pos_candidate_maxdev_um', 'lw_status', 'virial', 'p_ref_MPa', 'AM', 'SE')},
                     ensure_ascii=False))


if __name__ == '__main__':
    main()
