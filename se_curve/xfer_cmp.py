import json, glob
import numpy as np
# real_14 정본 곡선 (φ_SE_local, wallP GPa) — scripts/am_load_balance_jam.REAL14_SE_CURVE
R14 = np.array([[0.5356,0.0000],[0.5593,0.0001],[0.5785,0.0004],[0.5956,0.0117],
                [0.6174,0.0388],[0.6707,0.1157],[0.7184,0.1582],[0.7617,0.1850],
                [0.8106,0.1979],[0.8588,0.2376],[0.9131,0.2771]])
V_AM, V_SE, A = 159978.3, 83088.8, 2500.0        # kit_ps_7_3 (AM+SE 스캐폴드)
rows = []
for f in sorted(glob.glob('xfer_ps73_e*.json')):
    try: m = json.load(open(f))
    except Exception: continue
    h, s = m.get('thickness_um'), m.get('final_stress_GPa')
    if h is None or s is None: continue
    phi = V_SE / (A*float(h) - V_AM)
    ref = float(np.interp(phi, R14[:,0], R14[:,1]))
    d = (float(s)/ref - 1)*100 if ref > 1e-6 else float('nan')
    rows.append((phi, float(h), float(s), ref, d))
if not rows:
    print('   (아직 json 없음)'); raise SystemExit
print(f'   {"φ_SE":>7}{"t(µm)":>9}{"σ_ps73":>9}{"σ_r14":>9}{"Δ%":>8}')
for phi,h,s,ref,d in sorted(rows):
    flag = '' if abs(d) <= 10 else (' ★>25%' if abs(d) > 25 else ' ~밴드')
    print(f'   {phi:7.4f}{h:9.2f}{s:9.4f}{ref:9.4f}{d:+8.1f}{flag}')
ds = [abs(d) for *_ , d in rows if d == d]
if ds:
    med = float(np.median(ds))
    v = '전이 성립 (곡선 하나로 전 코퍼스)' if med <= 10 else \
        ('베드별 곡선 필요 (다압력 비용 3배)' if med > 25 else '밴드로 보고')
    print(f'   → median |Δ| = {med:.1f} %  ⇒  {v}   [{len(rows)}/5]')
