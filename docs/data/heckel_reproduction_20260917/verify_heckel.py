"""업로드된 pure-SE atom 덤프에서 D_sphere·D_union 을 재계산해 CSV 와 대조한다.

⚠ 규약은 CSV 헤더가 정한 것을 그대로 쓴다 (새로 만들지 않는다):
   · 박스 단면 A = 0.05 × 0.05,  높이 h = plate_z_lu (바닥 z=0)
   · D_sphere = Σ(4/3 π r³) / (A·h)
   · D_union  = (Σ V_sphere − Σ V_lens) / (A·h),  **pair-only 차감** (원장 L1-05)
   · 겹침은 x·y **주기 최소상 이미지**, z 는 비주기
   · 같은 반지름 두 구의 렌즈 부피  V = π(2R−d)²(d+4R)/12
"""
import sys, math, numpy as np

def read_atoms(path):
    with open(path) as f:
        lines = f.readlines()
    n = int(lines[3])
    xlo, xhi = map(float, lines[5].split())
    ylo, yhi = map(float, lines[6].split())
    cols = lines[8].split()[2:]
    ix, iy, iz, ir = cols.index('x'), cols.index('y'), cols.index('z'), cols.index('radius')
    a = np.array([[float(p[ix]), float(p[iy]), float(p[iz]), float(p[ir])]
                  for p in (l.split() for l in lines[9:9 + n])])
    return a, (xhi - xlo), (yhi - ylo)

def lens_sum(xyz, r, Lx, Ly):
    """셀 리스트로 렌즈 부피 합.  같은 반지름 가정."""
    cut = 2.0 * r
    nx, ny = max(1, int(Lx / cut)), max(1, int(Ly / cut))
    cx = np.minimum((xyz[:, 0] / Lx * nx).astype(int), nx - 1)
    cy = np.minimum((xyz[:, 1] / Ly * ny).astype(int), ny - 1)
    cz = (xyz[:, 2] / cut).astype(int)
    from collections import defaultdict
    grid = defaultdict(list)
    for i, (a, b, c) in enumerate(zip(cx, cy, cz)):
        grid[(a, b, c)].append(i)
    tot = 0.0
    npair = 0
    for (a, b, c), idx in grid.items():
        near = []
        for da in (-1, 0, 1):
            for db in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    near += grid.get(((a + da) % nx, (b + db) % ny, c + dc), [])
        near = np.array(near)
        for i in idx:
            j = near[near > i]
            if not len(j):
                continue
            dx = xyz[j, 0] - xyz[i, 0]; dy = xyz[j, 1] - xyz[i, 1]; dz = xyz[j, 2] - xyz[i, 2]
            dx -= Lx * np.round(dx / Lx); dy -= Ly * np.round(dy / Ly)   # 주기 최소상
            d = np.sqrt(dx * dx + dy * dy + dz * dz)
            m = (d < cut) & (d > 0)
            if m.any():
                dd = d[m]
                tot += float(np.sum(math.pi * (cut - dd) ** 2 * (dd + 4 * r) / 12.0))
                npair += int(m.sum())
    return tot, npair

REF = {100: (1230000, 0.0119872, 0.6908, 0.7032),
       200: (1450000, 0.00973721, 0.8099, 0.8657),
       300: (1600000, 0.00823721, 0.8992, 1.0234),
       400: (1710000, 0.00713721, 0.9660, 1.1811)}

print(f'{"P":>4} {"N":>7} {"D_sph(계산)":>12} {"D_sph(CSV)":>11} {"Δ":>9} '
      f'{"D_uni(계산)":>12} {"D_uni(CSV)":>11} {"Δ":>9}  쌍')
for P, path in [(int(a.split("=")[0]), a.split("=")[1]) for a in sys.argv[1:]]:
    step, pz, d_uni_ref, d_sph_ref = REF[P]
    a, Lx, Ly = read_atoms(path)
    xyz, r = a[:, :3], float(a[0, 3])
    V_box = Lx * Ly * pz
    V_sph = len(a) * (4.0 / 3.0) * math.pi * r ** 3
    d_sph = V_sph / V_box
    V_lens, npair = lens_sum(xyz, r, Lx, Ly)
    d_uni = (V_sph - V_lens) / V_box
    print(f'{P:>4} {len(a):>7} {d_sph:>12.4f} {d_sph_ref:>11.4f} {d_sph-d_sph_ref:>+9.4f} '
          f'{d_uni:>12.4f} {d_uni_ref:>11.4f} {d_uni-d_uni_ref:>+9.4f}  {npair}')
