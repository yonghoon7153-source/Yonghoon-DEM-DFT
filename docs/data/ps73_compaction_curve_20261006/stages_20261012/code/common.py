#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ps_7_3_r45 발표 그림 — 공통 (경로 · 단계 · 입력 sha256 · 판 높이 · 원자 읽기).

리포 (/home/user/Yonghoon-DEM-DFT) 는 **읽기만** 한다.  모든 출력은 OUT (이 파일의 부모 폴더) 아래.
실행 규칙: `python3 -I -B <script>` (cwd = OUT) — -I: 입력 덤프를 읽는 스크립트 (격리) · -B: 리포 모듈 import 때 __pycache__ 를 리포에 쓰지 않는다.
"""
import csv
import hashlib
import json
import os
import sys
import tarfile
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parents[1]
REPO = Path('/home/user/Yonghoon-DEM-DFT')
X = Path('/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/d26d1e75-209f-540f-83a8-c0e1957edc2f/scratchpad/'
         'ps73_in_1791811382/x/post_ps_7_3_r45')
SCRIPTS = REPO / 'scripts'
SNAP = REPO / 'docs' / 'data' / 'ps73_damping_branch_20261007' / 'snap_moments_20261008'
CURVE_DIR = REPO / 'docs' / 'data' / 'ps73_compaction_curve_20261006'
PLATE_CSV = CURVE_DIR / 'curve' / 'plate.csv'
MESH_TGZ = CURVE_DIR / 'raw' / 'ps73_curve_1.tgz'
RECEIPT = CURVE_DIR / 'stages_20261012' / 'ps73_files.txt'          # 1저자 ibb 묶음 영수증 (커밋 bef5bd5d7) — 입력 sha256 기준
DECK = REPO / 'dem_scripts' / 'ps_sweep_6mah_20260914' / 'in.ps_7_3_r45.liggghts'
UNION_TSV = REPO / 'docs' / 'data' / 'ps45_r45_union_20260929' / 'r45_union_summary.tsv'
PLANE_JSON = REPO / 'docs' / 'data' / 'ps45_plane_load_20261007' / 'ps45_v2' / 'plane_load.json'
VIEWER_JS = REPO / 'webapp' / 'static' / 'js' / 'viewer3d.js'

for p in (str(SCRIPTS), str(SNAP)):
    if p not in sys.path:
        sys.path.insert(0, p)
#  -I 는 사용자 site-packages 를 뺀다 — matplotlib 의 의존 (python-dateutil) 이 거기에만 있어 **맨 뒤에** 붙인다
#  (입력 폴더 · 작업 폴더는 sys.path 에 넣지 않는다 — -I 의 목적은 그대로).
import site as _site  # noqa: E402
_usp = _site.getusersitepackages()
if os.path.isdir(_usp) and _usp not in sys.path:
    sys.path.append(_usp)

#: 1저자 비준 단계 (보고 이름 · step).  기하 = 3,225,000 · 응력 = 3,220,000 (접촉 덤프가 거기만 있다).
STAGES = [
    ('initial', 'Initial compression', 405000),
    ('p50', '50 MPa', 1665000),
    ('p300', '300 MPa (end of compression)', 3125000),
    ('relaxed', 'After relaxation', 3225000),
]
STRESS_STEP = 3220000
CASE = 'ps_7_3_r45'                      # lhs_union_webapp --scan-root 의 케이스 이름 = MC 시드 crc32 의 입력 (r45_union_summary.tsv case 열)
WEBAPP_CASE = '260925_000559_082983'
SCALE = 1000.0                          # 덱 길이 × 1000 = µm (parse_liggghts · vm_moments scale · lhs_descriptor_harvest SIM_TO_UM)
STEP_MS = 1.0e-3                        # ms / step (Δt = 1e-6 s — make_fig_ms.STEP_MS)
TYPE_MAP = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}  # 덱 pts1 · pts2 · pts3 (atom_type 1 · 2 · 3) — prepare.py 가 반경 분포로 확인
SHORT = {'AM_P': 'PC', 'AM_S': 'SC', 'SE': 'SE'}


def atom_path(step):
    return X / f'atom_{step}.liggghts'


def contact_path(step):
    return X / f'contact_{step}.liggghts'


def mesh_path(step):
    return OUT / 'mesh' / f'mesh_{step}.stl'


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for b in iter(lambda: fh.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def receipt_sha():
    """영수증 (리포 커밋) 의 sha256 → {파일 이름: sha256}."""
    out = {}
    for ln in RECEIPT.read_text(encoding='utf-8').splitlines():
        parts = ln.split()
        if len(parts) == 2 and len(parts[0]) == 64:
            out[Path(parts[1]).name] = parts[0]
    return out


def plate_table():
    """curve/plate.csv → {step: (plate_z_deck, thickness_um, phase)}."""
    out = {}
    with open(PLATE_CSV, newline='', encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            out[int(r['step'])] = (float(r['plate_z_deck']), float(r['thickness_um']), int(r['phase']))
    return out


def extract_meshes(steps):
    """리포 tgz (읽기만) 에서 mesh_<step>.stl 을 OUT/mesh 로 — 멤버 이름을 확인하고 내용만 쓴다 (경로는 우리가 정한다)."""
    want = {f'post_ps_7_3_r45/mesh_{s}.stl': s for s in steps}
    got = {}
    with tarfile.open(MESH_TGZ, 'r:gz') as tf:
        for m in tf.getmembers():
            if m.name in want and m.isfile():
                data = tf.extractfile(m).read()
                dst = mesh_path(want[m.name])
                dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_bytes(data)
                got[want[m.name]] = hashlib.sha256(data).hexdigest()
    missing = sorted(set(steps) - set(got))
    if missing:
        raise SystemExit(f'⛔ 메시 tgz 에 없음: {missing}')
    return got


def read_atoms(step):
    """리포 웹앱 파서 (parse_liggghts.parse_atom_file) 로 원자 덤프 한 장 → (atoms dict, 배열 dict, 헤더 정보).

    atoms dict 꼴 = lhs_union_webapp.one() 과 같다 ({id: x · y · z · radius · type}).  배열은 id 정렬."""
    import parse_liggghts as PL
    path = atom_path(step)
    head = path.read_text(encoding='utf-8', errors='replace').splitlines()[:9]
    if head[0].strip() != 'ITEM: TIMESTEP' or int(head[1]) != step:
        raise SystemExit(f'⛔ {path.name}: TIMESTEP {head[1]!r} ≠ {step}')
    n_head = int(head[3])
    box = [tuple(float(v) for v in head[k].split()[:2]) for k in (5, 6, 7)]
    bc = head[4].replace('ITEM: BOX BOUNDS', '').split()
    ha, ra = PL.parse_atom_file(str(path))
    if len(ra) != n_head:
        raise SystemExit(f'⛔ {path.name}: 행 {len(ra)} ≠ 머리 원자 수 {n_head}')
    ia = {c: ha.index(c) for c in ('id', 'type', 'x', 'y', 'z', 'radius')}
    atoms = {}
    for v in ra:
        atoms[int(float(v[ia['id']]))] = {'x': float(v[ia['x']]), 'y': float(v[ia['y']]), 'z': float(v[ia['z']]),
                                          'radius': float(v[ia['radius']]), 'type': int(float(v[ia['type']]))}
    if len(atoms) != n_head:
        raise SystemExit(f'⛔ {path.name}: id 중복 ({n_head - len(atoms)})')
    ids = np.array(sorted(atoms), dtype=np.int64)
    arr = {'id': ids,
           'x': np.array([atoms[i]['x'] for i in ids]), 'y': np.array([atoms[i]['y'] for i in ids]),
           'z': np.array([atoms[i]['z'] for i in ids]), 'r': np.array([atoms[i]['radius'] for i in ids]),
           'type': np.array([atoms[i]['type'] for i in ids], dtype=np.int64)}
    info = {'timestep': step, 'n_header': n_head, 'box_deck': box, 'boundary': bc, 'columns': ha}
    return atoms, arr, info


def _jdefault(o):
    if hasattr(o, 'item'):                                    # numpy 스칼라
        return o.item()
    if hasattr(o, 'tolist'):
        return o.tolist()
    return str(o)


def write_json(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=1, default=_jdefault) + '\n', encoding='utf-8')


def write_origin_csv(path, head, units, rows, comments=None):
    """Origin 가져오기 꼴 — make_fig_ms.write_origin_csv 와 같다 (utf-8-sig · Long Name · Units · [Comment] · 자료)."""
    with open(path, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(head)
        w.writerow(units)
        if comments is not None:
            w.writerow(comments)
        w.writerows(rows)
