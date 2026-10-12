#!/usr/bin/env python3
"""보조 — 3,125,000 → 3,225,000 사이 빠진 원자 3 개 (id · 상 · 3,125,000 위치) 와 판 위 중심 입자 id 대조 (기록용)."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402
import numpy as np  # noqa: E402

pt = C.plate_table()
_, A3125, _ = C.read_atoms(3125000)
_, A3220, _ = C.read_atoms(3220000)
_, A3225, _ = C.read_atoms(3225000)
miss = np.setdiff1d(A3125['id'], A3225['id'])
idx = np.searchsorted(A3125['id'], miss)
H = pt[3125000][0]
out = {'missing_ids_3125000_to_3225000': miss.tolist(),
       'missing_phase': [C.TYPE_MAP[int(t)] for t in A3125['type'][idx]],
       'missing_z_minus_plate_um_at_3125000': [float((z - H) * C.SCALE) for z in A3125['z'][idx]],
       'missing_z_um_at_3125000': [float(z * C.SCALE) for z in A3125['z'][idx]],
       'missing_bottom_z_minus_r_um_at_3125000': [float((z - r) * C.SCALE) for z, r in zip(A3125['z'][idx], A3125['r'][idx])],
       'n_center_below_0p25r_by_step': {str(s): int((A['z'] < 0.25 * A['r']).sum()) for s, A in ((3125000, A3125), (3220000, A3220), (3225000, A3225))},
       'ids_3220000_equal_3225000': bool(np.array_equal(A3220['id'], A3225['id']))}
above = {s: set(A['id'][A['z'] > pt[s][0]].tolist()) for s, A in ((3125000, A3125), (3220000, A3220), (3225000, A3225))}
out['above_plate_ids'] = {str(s): sorted(v) for s, v in above.items()}
out['missing_were_above_plate_at_3125000'] = [int(i) in above[3125000] for i in miss]
C.write_json(C.OUT / 'logs' / 'aux_missing_atoms.json', out)
print(json.dumps(out, ensure_ascii=False))
