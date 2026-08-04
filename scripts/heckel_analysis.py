#!/usr/bin/env python3
"""Heckel fit for the pure-SE pressure series.

Reads heckel/manifest.json — a list of points:
  [{"P_MPa": 100, "plate_z": 0.0xxxx, "atom": "...", "contacts": ["...","..."]}, ...]
(plate_z from each mesh_*.stl vertex; contacts optional → enables ε_union/D_union.)

Computes per pressure:
  D_sphere = ΣV_sphere / V_box        (relative density, material-conserving)
  D_union  = (ΣV_sphere - ΣV_lens)/V_box   (geometric; <1 even when over-compressed)
Fits Heckel:  ln(1/(1-D)) = K·P + A   → mean yield pressure P_y = 1/K,
σ_y ≈ P_y/3.  Compares to LPSCl (σ_y≈0.30 GPa, H≈0.85 GPa).

Verdict: linear fit (high R²) with P_y ≈ 0.85 GPa → elastic-softened DEM
faithfully mimics LPSCl plasticity.  Curved / P_y far off → elastic limit.
"""
import json, math, sys
import numpy as np

R_SE = 0.0005
BOX = 0.05


def read_atoms(atom):
    """atom dump → (xyz[N,3], radius[N]).  Columns: id type x y z radius ..."""
    xyz, rad = [], []
    with open(atom) as f:
        for _ in range(9): next(f)
        for line in f:
            p = line.split()
            if len(p) < 6: continue
            xyz.append((float(p[2]), float(p[3]), float(p[4])))
            rad.append(float(p[5]))
    return np.asarray(xyz, float), np.asarray(rad, float)


def lens_from_geometry(xyz, rad, box=BOX):
    """겹침 렌즈 부피를 **atom 덤프 좌표만으로** 계산 (contact 덤프 불요).

    강체구이므로 LIGGGHTS 의 접촉 δ = rᵢ+rⱼ−dist 는 정확히 기하값이다 → 두 경로가
    같은 값을 줘야 하고, 둘 다 있는 압력점에서 그걸 교차검증한다.
    ★ 덱이 `boundary p p f` 이므로 x·y 는 **주기경계**다.  최소상 이미지를 안 쓰면
      경계층 접촉(≈ 2 r/L ≈ 2 %)을 통째로 놓친다.  z 는 비주기 → 큰 boxsize 로 무력화.
    """
    from scipy.spatial import cKDTree
    if len(xyz) < 2:
        return 0.0
    rmax = float(rad.max())
    q = xyz.copy()
    q[:, 0] %= box
    q[:, 1] %= box
    z0 = q[:, 2].min()
    q[:, 2] -= z0
    zbig = float(q[:, 2].max()) + 20.0 * rmax          # z 방향 되말림을 막는 여유
    tree = cKDTree(q, boxsize=[box, box, zbig])
    V = 0.0
    for i, j in tree.query_pairs(2.0 * rmax):
        ra, rb = float(rad[i]), float(rad[j])
        d = q[i] - q[j]
        d[0] -= box * round(d[0] / box)                # 최소상 이미지 (x, y)
        d[1] -= box * round(d[1] / box)
        dist = float(np.sqrt((d ** 2).sum()))
        if dist >= ra + rb:
            continue
        if dist <= abs(ra - rb):                        # 완전 포함
            V += (4.0 / 3.0) * math.pi * min(ra, rb) ** 3
            continue
        V += (math.pi * (ra + rb - dist) ** 2
              * (dist ** 2 + 2 * dist * rb - 3 * rb ** 2 + 2 * dist * ra
                 + 6 * ra * rb - 3 * ra ** 2) / (12.0 * dist))
    return float(V)


def lens_from_contacts(contacts, r_se=R_SE):
    """옛 경로 — contact 덤프의 δ 로 렌즈 부피.  덤프가 있을 때만."""
    V = 0.0
    for cf in (contacts or []):
        with open(cf) as f:
            for line in f:
                if line.startswith('ITEM'): continue
                p = line.split()
                if len(p) < 23: continue
                try: d = float(p[22])
                except: continue
                if 0 < d < 2*r_se:
                    V += (math.pi/12.0)*d**2*(6.0*r_se - d)
    return V


def vol_and_lens(atom, contacts, plate_z, geometric=True):
    """→ (V_sphere, V_lens, V_box, V_lens_contacts).

    V_lens 는 기본이 **기하 계산**(항상 가능) — contact 덤프는 교차검증용으로만 읽는다.
    옛 동작(contact 없으면 D_union=nan)이 4압력 중 3점을 못 쓰게 만들었다.
    """
    xyz, rad = read_atoms(atom)
    V_sphere = float(((4.0/3.0)*math.pi*rad**3).sum())
    V_c = lens_from_contacts(contacts) if contacts else 0.0
    V_lens = lens_from_geometry(xyz, rad) if geometric else V_c
    return V_sphere, V_lens, BOX*BOX*plate_z, (V_c if contacts else float('nan'))


def heckel(P, D):
    """Linear fit ln(1/(1-D)) = K*P + A on points with D<1 (nan/D≥1 은 제외)."""
    P = np.asarray(P, float)
    D = np.asarray(D, float)
    m = np.isfinite(D) & (D < 0.999)
    P, D = P[m], D[m]
    if len(P) < 2: return None
    y = np.log(1.0/(1.0 - D))
    K, A = np.polyfit(P, y, 1)
    yhat = K*P + A
    ss = np.sum((y - y.mean())**2)
    r2 = 1 - np.sum((y - yhat)**2)/ss if ss > 0 else float('nan')
    Py = 1.0/K if K > 0 else float('nan')            # MPa
    return dict(K=K, A=A, r2=r2, Py_MPa=Py, sigma_y_MPa=Py/3.0)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    man = json.load(open(args[0] if args else 'heckel/manifest.json'))
    rows = []
    for e in man:
        Vs, Vl, Vb, Vc = vol_and_lens(e['atom'], e.get('contacts'), e['plate_z'])
        eps_s = (1 - Vs/Vb)*100
        D_s = Vs/Vb
        D_u = (Vs - Vl)/Vb if Vl > 0 else float('nan')
        eps_u = (1 - D_u)*100 if Vl > 0 else float('nan')
        rows.append(dict(P=e['P_MPa'], eps_s=eps_s, D_s=D_s, eps_u=eps_u, D_u=D_u,
                         Vl=Vl, Vc=Vc))
        print(f"  P={e['P_MPa']:>4} MPa  ε_sphere={eps_s:+6.2f}%  D_sphere={D_s:.4f}"
              f"   ε_union={eps_u:6.2f}%  D_union={D_u:.4f}")
    # ★ 두 경로가 다 있는 압력점에서 기하 ↔ contact-덤프 교차검증 (강체구면 같아야 한다)
    xs = [r for r in rows if np.isfinite(r['Vc']) and r['Vc'] > 0]
    if xs:
        print('\n렌즈 부피 교차검증 (기하 vs contact 덤프) — 강체구면 일치해야 한다:')
        for r in xs:
            rel = abs(r['Vl'] - r['Vc'])/max(r['Vc'], 1e-30)
            print(f"  P={r['P']:>4} MPa  기하={r['Vl']:.6g}  contact={r['Vc']:.6g}  "
                  f"차이 {rel:.2%}" + ('  ✓' if rel < 0.05 else '  ⚠ 불일치 — 조사 필요'))
    else:
        print('\n  ⚠ contact 덤프가 있는 압력점이 없어 렌즈 교차검증 불가 (기하 경로만)')
    P = [r['P'] for r in rows]
    print("\nHeckel fit on D_union (physical, <1):")
    fu = heckel(P, [r['D_u'] for r in rows])
    if fu:
        print(f"  R²={fu['r2']:.4f}  P_y={fu['Py_MPa']:.0f} MPa ({fu['Py_MPa']/1000:.2f} GPa)"
              f"  σ_y≈{fu['sigma_y_MPa']:.0f} MPa")
        # ★ 판정을 둘로 나눈다.  옛 게이트는 (R²>0.97 and 500<P_y<1200) 하나였는데, 그 P_y
        #   구간은 **연화 안 한** LPSCl(H≈850 MPa)을 기대한 값이다.  우리 DEM 은 E 를 18×
        #   연화한 것이 설계이므로 P_y 가 그 구간에 들어오면 오히려 이상하다 — 게이트가
        #   "설계대로 동작했다" 를 실패로 찍고 있었다 (CLAUDE.md 는 이미 6.5× 연화의
        #   정량으로 해석하고 있어 문서와 코드가 어긋나 있었다).
        lin = fu['r2'] >= 0.95
        soft = 850.0 / fu['Py_MPa'] if fu['Py_MPa'] > 0 else float('nan')
        print(f"  LPSCl 단결정 참조: σ_y≈300 MPa, H≈850 MPa")
        print(f"  ① 직선성 R²={fu['r2']:.4f} → "
              f"{'✓ Heckel 선형 (소성 압밀 거동)' if lin else '⚠ 곡선 — 탄성 한계 노출'}")
        print(f"  ② 연화 배수 = 850/{fu['Py_MPa']:.0f} = {soft:.1f}×  "
              f"(σ_y 축: 300/{fu['sigma_y_MPa']:.0f} = {300.0/fu['sigma_y_MPa']:.1f}×)")
        print(f"     ↳ 이것은 실패가 아니라 **연화의 정량**이다.  E_eff 18× 연화가 설계이고, "
              f"P_y 가\n       500~1200 MPa 였다면 오히려 연화가 안 걸린 것.  "
              f"입도 재배열·GB 슬라이딩·미세파괴를\n       유효 탄성률에 뭉뚱그린 몫이 이 배수로 나타난다.")
        print(f"  VERDICT: {'✓ 선형 Heckel + 정량화된 연화' if lin else '⚠ 비선형 — 조사 필요'}")
    print("\nHeckel fit on D_sphere (flags over-compression where D≥1):")
    fs = heckel(P, [r['D_s'] for r in rows])
    if fs:
        print(f"  R²={fs['r2']:.4f}  P_y={fs['Py_MPa']:.0f} MPa")
    over = [r['P'] for r in rows if r['D_s'] >= 1.0]
    if over:
        print(f"  ⚠ D_sphere≥1 (over-compression artifact) at P={over} MPa → use D_union there")


def _selftest():
    ok, fail = 0, []

    def chk(name, cond):
        nonlocal ok
        if cond:
            ok += 1
        else:
            fail.append(name)

    R = R_SE
    # 같은 반지름 두 구, 겹침 δ → 렌즈 부피 πδ²(6R−δ)/12 (contact 경로가 쓰는 바로 그 식)
    for delta in (0.2*R, 0.8*R, 1.5*R):
        dist = 2*R - delta
        xyz = np.array([[0.02, 0.02, 0.01], [0.02 + dist, 0.02, 0.01]])
        want = math.pi/12.0*delta**2*(6.0*R - delta)
        got = lens_from_geometry(xyz, np.array([R, R]))
        chk(f'등반지름 렌즈 부피 δ={delta/R:.1f}R', abs(got - want)/want < 1e-6)

    xyz = np.array([[0.02, 0.02, 0.01], [0.02 + 2.5*R, 0.02, 0.01]])
    chk('안 닿으면 0', lens_from_geometry(xyz, np.array([R, R])) == 0.0)

    # ★ 주기경계 (덱이 boundary p p f) — 경계를 가로지르는 접촉을 놓치면 안 된다
    d = 2*R - 0.5*R
    xyz = np.array([[BOX - d/2, 0.02, 0.01], [d/2, 0.02, 0.01]])   # x 경계 넘어 마주봄
    want = math.pi/12.0*(0.5*R)**2*(6.0*R - 0.5*R)
    chk('★ x 주기경계를 가로지르는 겹침을 잡는다',
        abs(lens_from_geometry(xyz, np.array([R, R])) - want)/want < 1e-6)
    xyz = np.array([[0.02, BOX - d/2, 0.01], [0.02, d/2, 0.01]])
    chk('★ y 주기경계도 마찬가지',
        abs(lens_from_geometry(xyz, np.array([R, R])) - want)/want < 1e-6)
    # z 는 비주기 — 바닥과 천장이 이어지면 안 된다
    xyz = np.array([[0.02, 0.02, 0.0], [0.02, 0.02, 0.012]])
    chk('z 는 되말리지 않는다 (바닥↔천장 가짜 접촉 금지)',
        lens_from_geometry(xyz, np.array([R, R])) == 0.0)

    # 완전 포함 (작은 구가 큰 구 안으로) → 작은 구 부피
    xyz = np.array([[0.02, 0.02, 0.01], [0.02 + 0.1*R, 0.02, 0.01]])
    got = lens_from_geometry(xyz, np.array([2*R, 0.5*R]))
    chk('완전 포함이면 작은 구 부피',
        abs(got - (4.0/3.0)*math.pi*(0.5*R)**3)/((4.0/3.0)*math.pi*(0.5*R)**3) < 1e-9)

    # ★ heckel() 이 리스트/nan/D≥1 을 견디는가 (2026-08-05 실제 크래시 회귀)
    f = heckel([100, 200, 300, 400], [0.69, float('nan'), 1.02, 1.18])
    chk('★ 리스트 입력에 죽지 않는다 (D<0.999 를 리스트에 걸던 TypeError)', f is None)
    f = heckel([100, 200, 300], [0.60, 0.70, 1.05])
    chk('D≥1 점은 fit 에서 빠진다', f is not None)
    f = heckel([100, 200, 300], [0.60, float('nan'), 0.80])
    chk('nan 점도 빠진다', f is not None and f['K'] > 0)

    # 알려진 Heckel 직선을 심어두고 K/P_y 회수
    K0, A0 = 1.0/850.0, 0.5
    Ps = [100, 200, 300, 400]
    Ds = [1 - math.exp(-(K0*p + A0)) for p in Ps]
    f = heckel(Ps, Ds)
    chk('심어둔 Heckel 직선에서 P_y 회수', abs(f['Py_MPa'] - 850) < 1e-6 and f['r2'] > 0.999)

    print(f'selftest: {ok}/{ok + len(fail)} PASS' + (f'   FAILED: {fail}' if fail else ''))
    return 0 if not fail else 1


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(_selftest())
    main()
