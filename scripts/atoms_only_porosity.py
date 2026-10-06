#!/usr/bin/env python3
"""atom 덤프 + 판 메시만 올린 케이스 (접촉 덤프 없음 · 웹앱 atoms-only 모드) 의 공극률 · 두께 (2026-10-07).

  python3 scripts/atoms_only_porosity.py <결과 폴더> [--scale 1000] [--atom-dump atom_*.liggghts …]

접촉이 필요 없는 정의만 — 접촉 분석 (`dem_analysis_core.run_full_analysis`) 이 부르는 **같은 함수**를 같은 원자 · 판 · 상자로 부른다 (새 식 없음):
  ε_sphere  = calc_porosity              (구 부피 합 · 생산 규약 · L_x·L_y·판 간격)              → porosity · porosity_spheresum
  ε_union   = calc_porosity_union_exact  (몬테카를로 정확 union · 벽 밖 제외 · x·y 주기 · 같은 씨앗) → porosity_union_exact_pct …
  두께      = get_plate_z × scale        (mesh_info.json 판 = 판 간격)                            → thickness_um · plate_z_source
  원자      = analyze_contacts.load_atoms_raw (접촉 분석과 같은 읽기 → 같은 dict → 같은 MC 씨앗)
접촉이 있어야 하는 값 (쌍 렌즈 union · 겹침 비율 · 질량 보존 두께 · 퍼콜레이션 · CN · …) 은 내지 않는다.

판 메시가 없으면 **계산하지 않는다** (판 간격을 모른다 — 최고 입자 중심으로 판을 짐작하는 접촉 분석의 대체 규칙은 덜 다져진 프레임에서
두께를 크게 틀린다).  판이 입자 윗면 최댓값 (max z + r) 보다 위에 떠 있으면 (덜 다져진 프레임 · 판 간격에 빈 머리 공간) 같은 두 함수를
판 대신 그 윗면으로 한 번 더 불러 `porosity_bedtop_*` 로 따로 적는다 (판 간격 값을 바꾸지 않는다).

상자: input_params.json (input deck) → 그 상자.  deck 이 없고 atom 덤프의 BOX BOUNDS 가 x·y 주기 (pp) 면 그 상자를 input_params.json 에
`box_source = 'atom dump BOX BOUNDS'` 로 적고 쓴다 (3D 뷰어 /3d-data 도 같은 상자를 읽는다 — 기본 50 µm 로 틀리게 재지 않게).
deck 상자 ≠ 덤프 상자면 계산하지 않는다 (어느 쪽이 맞는지 모른다).  둘 다 없으면 기본 0.05 (접촉 분석과 같은 기본값 · 표지).

결과 = full_metrics.json 에 합친다 (원자적 쓰기 · 있던 키는 그대로).  계산을 못 하면 `porosity_status = 'not_computed: 사유'` 만 적고
rc 0 (판정이 적힌 정상 결과) — 읽기 · 쓰기 실패만 rc 1.
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import dem_analysis_core as C          # noqa: E402

BOX_FROM_DUMP = 'atom dump BOX BOUNDS'
BOX_REL_TOL = 1e-6


def _write_json(path, obj):
    """원자적 쓰기 — 같은 폴더 temp → os.replace (반쪽 파일을 남기지 않는다)"""
    tmp = path + '.atoms_only_porosity.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2, default=float)
    os.replace(tmp, path)


def dump_box(atom_files):
    """parse_liggghts 가 고르는 그 파일 (find_last_file) 의 BOX BOUNDS → (lx, ly, x·y 주기 여부) · 못 읽으면 None"""
    if not atom_files:
        return None
    try:
        import parse_liggghts as PL
        import lhs_union_webapp as LU
        path = PL.find_last_file(list(atom_files))
        _x0, lx, _y0, ly, flags = LU._box_xy(path)
    except Exception:                                            # noqa: BLE001 — 머리가 없는 파일 · 잘린 파일
        return None
    per = len(flags) >= 2 and all(str(f).startswith('p') for f in flags[:2])
    return float(lx), float(ly), per, ' '.join(flags), os.path.basename(path)


def resolve_box(results_dir, atom_files):
    """→ (box_x, box_y, source, problem) — sim 단위.  problem 이 있으면 계산하지 않는다."""
    ip_path = os.path.join(results_dir, 'input_params.json')
    ip = {}
    if os.path.exists(ip_path):
        try:
            with open(ip_path, encoding='utf-8') as f:
                ip = json.load(f) or {}
        except (OSError, ValueError):
            ip = {}
    db = dump_box(atom_files)
    has_deck_box = isinstance(ip.get('box_x'), (int, float)) and isinstance(ip.get('box_y'), (int, float))
    if has_deck_box:
        bx, by = C._get_box_xy(results_dir)
        src = ip.get('box_source') or 'input_params.json'
        if db and src == 'input_params.json':
            lx, ly = db[0], db[1]
            if abs(lx - bx) > BOX_REL_TOL * max(lx, bx) or abs(ly - by) > BOX_REL_TOL * max(ly, by):
                return bx, by, src, (f'box_mismatch — input deck 상자 {bx:g} × {by:g} ≠ atom 덤프 BOX BOUNDS {lx:g} × {ly:g} (sim) '
                                     f'({db[4]}) · 어느 쪽이 맞는지 모른다')
        return bx, by, src, None
    if db:
        lx, ly, per, flags, name = db
        if not per:
            return lx, ly, BOX_FROM_DUMP, (f'not_periodic — atom 덤프 BOX BOUNDS 경계 "{flags}" ({name}) 가 x·y 주기 (pp) 가 아니다 · '
                                           '정확 union · ε_sphere 상자 규약 (x·y 주기) 밖')
        ip.update({'box_x': round(lx, 9), 'box_y': round(ly, 9), 'box_source': BOX_FROM_DUMP})
        _write_json(ip_path, ip)
        bx, by = C._get_box_xy(results_dir)
        return bx, by, BOX_FROM_DUMP, None
    bx, by = C._get_box_xy(results_dir)
    return bx, by, 'default 0.05 (input deck · atom 덤프 상자 없음 — 접촉 분석과 같은 기본값)', None


def compute(results_dir, scale=1000.0, atom_files=None):
    """→ full_metrics 에 합칠 키 dict (porosity_status 는 늘 있다)"""
    out = {'porosity_source': 'atoms_only'}
    mesh = os.path.join(results_dir, 'mesh_info.json')
    if not os.path.exists(mesh):
        out['porosity_status'] = ('not_computed: 판 메시 없음 — atom 덤프만으로는 판 간격 (두께) 을 모른다 · '
                                  '판 메시 (mesh_*.stl) 를 같이 올리면 공극률 · 두께를 낸다')
        return out
    import analyze_contacts as AC
    atoms, _df = AC.load_atoms_raw(os.path.join(results_dir, 'atoms.csv'))
    if not atoms:
        out['porosity_status'] = 'not_computed: atoms.csv 에 원자가 없다'
        return out
    plate_z, pz_src = C.get_plate_z(results_dir, atoms, scale)
    if pz_src != 'mesh' or not (plate_z and plate_z > 0):
        out['porosity_status'] = f'not_computed: 판 z 를 판 메시에서 못 읽었다 (plate_z={plate_z!r} · {pz_src})'
        return out
    bx, by, bsrc, problem = resolve_box(results_dir, atom_files)
    out.update({'porosity_box_x_um': round(bx * scale, 6), 'porosity_box_y_um': round(by * scale, 6), 'porosity_box_source': bsrc})
    if problem:
        out['porosity_status'] = 'not_computed: ' + problem
        return out
    eps = C.calc_porosity(atoms, plate_z, bx, by)
    ue = C.calc_porosity_union_exact(atoms, plate_z, bx, by)
    out.update({'porosity': eps, 'porosity_spheresum': eps, 'thickness_um': plate_z * scale, 'plate_z_source': pz_src,
                'n_atoms_porosity': len(atoms)})
    out.update({k: ue.get(k) for k in ('porosity_union_exact_pct', 'porosity_union_exact_se_pct', 'union_exact_mc_n',
                                        'union_exact_mc_seed', 'union_exact_status', 'wall_overhang_over_Vbox_pct')})
    top = max(a['z'] + a['radius'] for a in atoms.values())
    out['bed_top_um'] = top * scale
    out['headspace_um'] = (plate_z - top) * scale
    if top < plate_z:
        eps_t = C.calc_porosity(atoms, top, bx, by)
        ue_t = C.calc_porosity_union_exact(atoms, top, bx, by)
        out.update({'porosity_bedtop_spheresum': eps_t, 'porosity_bedtop_union_exact_pct': ue_t.get('porosity_union_exact_pct'),
                    'porosity_bedtop_union_exact_se_pct': ue_t.get('porosity_union_exact_se_pct'),
                    'porosity_bedtop_status': 'OK' if ue_t.get('union_exact_status') == 'OK' else f"ε_union: {ue_t.get('union_exact_status')}"})
    else:
        out['porosity_bedtop_status'] = ('not_applicable: 판이 입자 윗면 최댓값 (max z + r) 보다 위에 있지 않다 — 판 간격에 빈 머리 공간 없음 '
                                         '(판 값만 쓴다)')
    out['porosity_status'] = 'OK'
    return out


def merge_into_full_metrics(results_dir, keys):
    p = os.path.join(results_dir, 'full_metrics.json')
    fm = {}
    if os.path.exists(p):
        with open(p, encoding='utf-8') as f:
            fm = json.load(f) or {}
    fm.update(keys)
    _write_json(p, fm)
    return fm


def main(argv=None):
    ap = argparse.ArgumentParser(description='atoms-only (접촉 덤프 없음) 케이스의 공극률 · 두께 — 접촉 분석과 같은 함수')
    ap.add_argument('results_dir')
    ap.add_argument('--scale', type=float, default=1000.0)
    ap.add_argument('--atom-dump', nargs='*', default=[], help='parse 단계에 들어간 atom_*.liggghts (상자 = BOX BOUNDS · 마지막 파일)')
    a = ap.parse_args(argv)
    try:
        keys = compute(a.results_dir, a.scale, a.atom_dump)
    except Exception as e:                                       # noqa: BLE001 — 계산 자체의 실패는 사유로 남긴다
        keys = {'porosity_source': 'atoms_only', 'porosity_status': f'failed: {type(e).__name__}: {e}'}
    merge_into_full_metrics(a.results_dir, keys)
    st = keys.get('porosity_status')
    if st == 'OK':
        print(f"  Porosity (atoms only): ε_sphere {keys['porosity']:.3f} % · ε_union 정확 {keys.get('porosity_union_exact_pct')} % · "
              f"두께 (판 간격) {keys['thickness_um']:.3f} µm · 상자 {keys['porosity_box_x_um']} × {keys['porosity_box_y_um']} µm "
              f"({keys['porosity_box_source']})")
        if keys.get('porosity_bedtop_spheresum') is not None:
            print(f"  입자 윗면 기준 (빈 머리 공간 {keys['headspace_um']:.3f} µm 제외): ε_sphere {keys['porosity_bedtop_spheresum']:.3f} % · "
                  f"ε_union 정확 {keys.get('porosity_bedtop_union_exact_pct')} %")
    else:
        print(f'  Porosity (atoms only): {st}')
    return 1 if str(st).startswith('failed') else 0


if __name__ == '__main__':
    sys.exit(main())
