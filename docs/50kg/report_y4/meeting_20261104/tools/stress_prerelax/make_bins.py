"""particles_<label>.csv → webtex/data/<label>_{NCM,SE}.bin (float32 x y z r v wall) + specs.json 한 줄씩."""
import csv, json, sys
from pathlib import Path
import numpy as np
csv_path, label, root, plate_mpa = sys.argv[1], sys.argv[2], Path(sys.argv[3]), float(sys.argv[4])
mode = sys.argv[5]                       # abs | norm
lo_am, hi_am, lo_se, hi_se = map(float, sys.argv[6:10])
dist = float(sys.argv[10]); ty = float(sys.argv[11]); W, H = int(sys.argv[12]), int(sys.argv[13])
rows = list(csv.DictReader(open(csv_path)))
specs = []
for name, ph, lo, hi, seg in (('NCM', 'AM', lo_am, hi_am, 16), ('SE', 'SE', lo_se, hi_se, 12)):
    sel = [r for r in rows if r['phase'] == ph and r['wall'] == '0']      # 1저자 11-03 '회색 빼고' = 판·바닥 접촉 입자 숨김 (16쪽 통계와 같은 제외)
    v = np.array([float(r['vm_MPa']) for r in sel]) / (plate_mpa if mode == 'norm' else 1.0)
    a = np.array([[float(r['x_um']), float(r['y_um']), float(r['z_um']), float(r['r_um']), vv, float(r['wall'])]
                  for r, vv in zip(sel, v)], dtype=np.float32)
    b = root / 'data' / f'{label}_{mode}_{name}.bin'; b.parent.mkdir(parents=True, exist_ok=True); a.tofile(b)
    zc = 0.5 * (float(np.min(a[:, 2] - a[:, 3])) + float(np.max(a[:, 2] + a[:, 3])))
    specs.append(dict(bin=f'data/{b.name}', out=str(root / 'out' / f'{label}_{mode}_{name}.png'), W=W, H=H, seg=seg,
                      lo=lo, hi=hi, cx=25.0, cy=25.0, cz=zc, dist=dist, ty=ty, n=int(len(a)),
                      frac_wall=float(a[:, 5].mean()), frac_over=float(np.mean((a[:, 5] < 0.5) & (a[:, 4] > hi)))))
(root / 'out').mkdir(exist_ok=True)
print(json.dumps(specs))
