#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""준비 — ① 입력 sha256 = 리포 영수증 ② 판 메시 STL 다섯 장 (리포 tgz → OUT/mesh) · 판 높이 = plate.csv 대조
③ type → 상 (덱 particletemplate) 을 덤프의 type 별 반경 분포로 확인.  실패 = rc 1 (값 없이 사유).

  cd OUT && python3 -I -B code/prepare.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

import numpy as np  # noqa: E402


def deck_types():
    """덱의 particletemplate/sphere 줄 → {atom_type: (템플릿 이름, 반경 변수, 반경 값)}."""
    text = C.DECK.read_text(encoding='utf-8')
    var = {}
    for m in re.finditer(r'^variable\s+(\w+)\s+equal\s+([0-9.eE+-]+)', text, re.M):
        var[m.group(1)] = float(m.group(2))
    out = {}
    for m in re.finditer(r'^fix\s+(pts\d)\s+all\s+particletemplate/sphere\s+\d+\s+atom_type\s+(\d+)\s+density\s+constant\s+(\S+)\s+'
                         r'radius\s+constant\s+\$\{(\w+)\}', text, re.M):
        out[int(m.group(2))] = {'template': m.group(1), 'density': float(m.group(3)), 'radius_var': m.group(4),
                                'radius_deck': var[m.group(4)]}
    comment = re.search(r'#\s*--- 3\. Material Properties \((.*?)\)', text)
    return out, (comment.group(1) if comment else None)


def main():
    rec = {'inputs': {}, 'mesh': {}, 'types': {}, 'problems': []}
    # ① 입력 sha256
    want = C.receipt_sha()
    for p in sorted(C.X.iterdir()):
        h = C.sha256(p)
        ok = want.get(p.name) == h
        rec['inputs'][p.name] = {'sha256': h, 'bytes': p.stat().st_size, 'receipt_match': ok}
        if not ok:
            rec['problems'].append(f'sha256 불일치 {p.name}')
    print('입력 sha256 = 영수증:', all(v['receipt_match'] for v in rec['inputs'].values()), f'({len(rec["inputs"])} 파일)')
    # ② 판 메시
    import lhs_descriptor_harvest as HV
    import parse_liggghts as PL
    steps = [s for _, _, s in C.STAGES] + [C.STRESS_STEP]
    shas = C.extract_meshes(steps)
    plate = C.plate_table()
    for s in sorted(steps):
        z_hv = HV.plate_z_from_stl(str(C.mesh_path(s)))          # 평판 검사 포함 (HND-06)
        z_pl, tris = PL.parse_mesh_stl(str(C.mesh_path(s)))
        z_csv = plate[s][0]
        ok = (z_hv == z_csv) and (z_pl == z_csv)
        rec['mesh'][s] = {'sha256': shas[s], 'plate_z_stl_deck': z_hv, 'plate_z_parser_deck': z_pl, 'plate_z_csv_deck': z_csv,
                          'thickness_um': plate[s][1], 'phase': plate[s][2], 'n_triangles': len(tris), 'equal': ok}
        if not ok:
            rec['problems'].append(f'판 높이 STL {z_hv!r} · 파서 {z_pl!r} ≠ plate.csv {z_csv!r} @ {s}')
        print(f'  mesh_{s}: STL {z_hv!r} · plate.csv {z_csv!r} · 같음 {ok} · 단계 {plate[s][2]}')
    # ③ type → 상
    dt, comment = deck_types()
    rec['deck_types'] = {str(k): v for k, v in dt.items()}
    rec['deck_material_comment'] = comment
    for s in sorted(steps):
        atoms, A, info = C.read_atoms(s)
        per = {}
        for t in sorted(set(A['type'].tolist())):
            r = A['r'][A['type'] == t]
            per[str(t)] = {'n': int(r.size), 'r_min_deck': float(r.min()), 'r_max_deck': float(r.max()),
                           'r_unique_deck': sorted({float('%.9g' % v) for v in r})}
            exp = dt.get(t)
            if exp is None or not np.all(r == exp['radius_deck']):
                rec['problems'].append(f'type {t} 반경 ≠ 덱 ({per[str(t)]["r_unique_deck"][:4]} ↔ {exp})')
        rec['types'][s] = {'n_atoms': info['n_header'], 'box_deck': info['box_deck'], 'boundary': info['boundary'],
                           'per_type': per}
        print(f'  atom_{s}: 원자 {info["n_header"]} · ' + ' · '.join(
            f'type {t} ({C.TYPE_MAP[int(t)]}) n {v["n"]} r {v["r_unique_deck"]}' for t, v in per.items()))
    rec['type_map'] = {str(k): v for k, v in C.TYPE_MAP.items()}
    rec['status'] = 'OK' if not rec['problems'] else 'FAILED'
    C.write_json(C.OUT / 'logs' / 'prepare.json', rec)
    print('상태', rec['status'], rec['problems'])
    return 0 if rec['status'] == 'OK' else 1


if __name__ == '__main__':
    sys.exit(main())
