"""L214R-S02 증거 (둘째 축 근거) — 이 기계에서 실 생산자 사슬 (R01 경계 시험의 21 구 사슬) 로 잰다.  판정 아님 · 시험 · 생산 코드 바이트 그대로.
python3 -B s02_axis_analysis.py <리포 루트>
  ① I_bottom 은 상자와 무관 (bx · by 를 크게 바꿔도 비트 같음) · 생산자 q 재현 = fl(fl(I_bottom·T) / fl(bx·by)) 가 실 사슬 q 와 비트 같음
  ② box_x 는 건너뜀을 못 고친다 — E″a 출발 면적 (prev 건너뜀) 에서 bx 를 옮겨 (ULP · 다른 값) 실 사슬 box_y 걸음 → prev 여전히 건너뜀 + 같은 산술 재현 ±200 ULP
  ③ I_bottom 은 2^-53 격자 · 격자 칸 j 마다 닿는 경계 꼴 (next · eq · prev) = 3 칸 주기 (같은 산술 재현 · ±30 칸)
  ④ dlnG/dln(접촉 면적) → 면적 1 ULP 당 G 칸 · ±64 ULP 의 칸 수
  ⑤ 출발 면적 ±200 ULP (401 개) 마다 e0_search → 찾음 · 시도 수 · |k| 최대 · 찾은 면적의 I_bottom 칸 (j−j0) mod 3"""
import contextlib
import io
import math
import sys
import time
from pathlib import Path

root = Path(sys.argv[1]).resolve()
for p in (str(root / 'scripts'), str(root / 'webapp')):
    if p not in sys.path:
        sys.path.insert(0, p)
import test_l214r_r01_restored_full as T  # noqa: E402
import network_conductivity as nc  # noqa: E402
from test_lhs214_model_limit import chain_bed  # noqa: E402


def cert(area, bx, by):
    A, C, plate, _b = chain_bed(1.0, area=area)
    with contextlib.redirect_stdout(io.StringIO()):
        du = nc._run_all_networks(A, C, [1], [], {1: 'SE'}, 1, plate, bx, by, None, contact_mode='hertzian')
    return du['solve_certificate_full'], plate


def replica_hit(N, bx, tgt, span=8):
    byc = N / (bx * tgt)
    return any(N / (bx * T._ulp(byc, d)) == tgt for d in range(-span, span + 1))


t_all = time.perf_counter()
# ① 상자 무관 · 재현
c0, plate = cert(T.E_AREA, T.E_BX, T.E_BY['eq'])
Ib0 = c0['I_bottom']
same = []
for bx, by in ((T.E_BX, T.E_BY['next']), (T.E_BX, T.E_BY['prev']), (0.6, 0.9), (0.9, 0.6), (0.7, 0.7)):
    same.append(cert(T.E_AREA, bx, by)[0]['I_bottom'] == Ib0)
N0 = (Ib0 / c0['delta_V']) * plate
rep = []
by = T._ulp(T.E_BY['next'], -20)
for _ in range(41):
    rep.append(T._e_raw_q(nc, *chain_bed(1.0, area=T.E_AREA)[:3], T.E_BX, by) == N0 / (T.E_BX * by))
    by = T._ulp(by, 1)
print(f'① I_bottom {Ib0!r} — 상자 다섯 조합에서 비트 같음 {sum(same)}/{len(same)} · 생산자 산술 재현 (box_y 41 걸음) 실 사슬과 비트 같음 {sum(rep)}/{len(rep)}')

# ② box_x 로는 못 고친다 (E″a 출발 = prev 건너뜀)
aA = T.E2_START['a']
A, C, plate, _b = chain_bed(1.0, area=aA)
cA, _p = cert(aA, T.E_BX, T.E_BY['eq'])
NA = (cA['I_bottom'] / cA['delta_V']) * plate
rows = []
for lab, bx in [(f'{d:+d} ULP', T._ulp(T.E_BX, d)) for d in (-200, -50, -10, -1, 0, 1, 10, 50, 200)] + [('0.6', 0.6), ('0.9', 0.9)]:
    f, s, pr = T.find_boundary_inputs(nc, A, C, plate, bx, T.E_BY, recenter=True)
    ib_same = cert(aA, bx, f.get('eq', T.E_BY['eq']))[0]['I_bottom'] == cA['I_bottom']
    rows.append((lab, sorted(f), sorted(pr), ib_same))
print(f'② E″a 출발 면적 {aA!r} (I_bottom {cA["I_bottom"]!r}) — bx 를 옮긴 실 사슬 box_y 걸음 (11 값):')
for lab, f, pr, ib in rows:
    print(f'     bx {lab:>9s} → 찾음 {f} · 건너뜀 {pr} · I_bottom 같음 {ib}')
rep_hits = sum(replica_hit(NA, T._ulp(T.E_BX, d), T.E_Q['prev']) for d in range(-200, 201))
print(f'   같은 산술 재현 bx ±200 ULP (401 값) 에서 prev 를 내는 box_y: {rep_hits} 개 (0 = box_x 축으로는 못 닿는다)')

# ③ 2^-53 격자 · 3 칸 주기
j0 = Ib0 * 2.0 ** 53
pat = []
for d in range(-30, 31):
    N = ((j0 + d) / 2.0 ** 53) * plate
    pat.append(''.join('1' if replica_hit(N, T.E_BX, T.E_Q[k]) else '0' for k in ('next', 'eq', 'prev')))
period3 = all(pat[i] == pat[i % 3] for i in range(len(pat)))
cls = {(-30 + i) % 3: pat[i] for i in range(3)}
print(f'③ I_bottom·2^53 = {j0!r} (정수 {j0 == int(j0)}) · 칸 j−j0 의 경계 꼴 (next·eq·prev) ±30 칸 3 칸 주기 {period3} · '
      f'(j−j0) mod 3 = 0 → {cls[0]} · 1 → {cls[1]} · 2 → {cls[2]}')

# ④ 면적 탄성
c1, _p = cert(T.E_AREA * (1 + 1e-6), T.E_BX, T.E_BY['eq'])
el = ((c1['I_bottom'] - Ib0) / Ib0) / 1e-6
per_ulp = el * Ib0 * (math.ulp(T.E_AREA) / T.E_AREA) / 2.0 ** -53
print(f'④ dlnG/dln(접촉 면적) = {el:.4f} · 면적 1 ULP 당 G {per_ulp:.4f} 칸 (= {1 / per_ulp:.1f} ULP 당 1 칸) · ±{T.E_AREA_ULP} ULP = ±{T.E_AREA_ULP * per_ulp:.2f} 칸')

# ⑤ 출발 면적 ±200 ULP 마다 e0_search
t = time.perf_counter()
res = []
for k0 in range(-200, 201):
    a0 = T._ulp(T.E_AREA, k0)
    r = T.e0_search(nc, a0, T.E_BX, T.E_BY)
    if r['probs']:
        res.append((k0, None, len(r['tried']), None))
        continue
    cf, _p = cert(r['area'], T.E_BX, r['bys']['eq'])
    jj = cf['I_bottom'] * 2.0 ** 53
    res.append((k0, r['k'], len(r['tried']), (int(jj) - int(j0)) % 3 if jj == int(jj) else 'not-grid'))
ok = [x for x in res if x[1] is not None]
skip_starts = [x for x in res if x[1] is not None and x[1] != 0]
print(f'⑤ 출발 면적 ±200 ULP ({len(res)} 개) → 찾음 {len(ok)}/{len(res)} · 출발 면적에서 바로 = {len(ok) - len(skip_starts)} · 둘째 축이 필요 = {len(skip_starts)} · '
      f'|k| 최대 {max(abs(x[1]) for x in ok)} · 시도 최대 {max(x[2] for x in ok)} · 찾은 면적의 (j−j0) mod 3 = {sorted({x[3] for x in ok}, key=str)} · '
      f'{time.perf_counter() - t:.1f} s')
hist = {}
for x in ok:
    hist[abs(x[1])] = hist.get(abs(x[1]), 0) + 1
print('   |k| 분포 ' + ' '.join(f'{k}:{v}' for k, v in sorted(hist.items())))
print(f'합계 {time.perf_counter() - t_all:.1f} s')
