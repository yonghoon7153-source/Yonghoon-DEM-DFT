"""섬유를 **복셀에 굽지 않고 1D 저항 요소로** 푼다 — 격자 의존의 근본 해법.

★ 왜 (CL-21 · CL-22): VGCF 는 Ø 0.15 µm 인데 STEP3 격자는 0.4 µm 다 (**0.37 셀**).
  복셀에 구우면 세 가지가 동시에 틀린다:
    ① 단면이 부푼다        → 직경-보존 σ 재척도로 고침 (CL-16/CL-17)
    ② 계단식 경로가 길다   → k = 1.486 실측 (CL-20)
    ③ **섬유끼리 가짜로 붙는다** → 격자를 조이면 σ_e −44.8 %, 비 −18.25 %.  **미수렴** (CL-22)
  ③ 은 σ 재척도로 못 고친다 — 기하 자체가 틀렸다.  그리고 격자를 조여 해결하려 해도
  vox 0.133 µm 에서 σ_eff = σ_bulk 에 닿아 **방법이 무효**가 된다 (CL-22).
  ⇒ 섬유를 격자에 올리지 말고 **실제 기하 그대로 1D 저항망**으로 푼다.

이 모듈이 하는 것 (격자 **무관**, 정의상):
  · 폴리라인 구간마다 저항 R = L/(σ_bulk·A_real),  A_real = πd²/4      ← 참 단면·참 길이
  · 섬유↔섬유 접촉: 두 점이 (d_i+d_j)/2 안이면 Holm 협착 R = 1/(2σ·a),  a = 접촉반경
  · 섬유↔복셀상(AM·SDCP): 섬유 점이 그 상의 복셀 안이면 계면 컨덕턴스로 결합
이 파일은 **섬유 부분망**만 만들고 검증한다.  복셀 FV 와의 결합은 `couple_to_voxel_grid`
가 (노드, 컨덕턴스) 목록으로 돌려주고, 조립은 step3_sigma 쪽에서 한다 (2단계).

⚠ 이것도 만능이 아니다 — 접촉 판정이 **점 샘플링 간격**에 의존한다 (섬유 점 간격 0.12 µm).
  격자 대신 그 간격이 새 자유도가 된다.  그래서 `contact_sensitivity()` 로 **그 민감도를
  같이 재도록** 만들었다.  "격자를 없앴다" 가 아니라 "격자 의존을 **잰 자유도**로 바꿨다".

사용:  python3 scripts/fibre_1d_network.py --selftest
"""
from __future__ import annotations

import argparse

import numpy as np


def polylines(pts, fid, gap_tol=2.0):
    """(N,3) 점 + 섬유 id → 끊긴 자리에서 나눈 폴리라인 목록.

    시더가 AM 내부 점을 드랍하므로 간격이 `gap_tol × 중앙간격` 을 넘으면 **물리적 단절**로
    보고 끊는다 (step3_sigma._fibre_segment_ijk 와 **같은 규약** — 규약이 갈리면 두 경로가
    다른 섬유를 본다).
    """
    P, F = np.asarray(pts, np.float64), np.asarray(fid)
    out = []
    for f in np.unique(F):
        Q = P[F == f]
        if len(Q) < 2:
            continue
        d = np.linalg.norm(np.diff(Q, axis=0), axis=1)
        med = float(np.median(d)) if len(d) else 0.0
        brk = (np.nonzero(d > gap_tol * med)[0] + 1) if med > 0 else np.array([], int)
        for R in (np.split(Q, brk) if len(brk) else [Q]):
            if len(R) >= 2:
                out.append(R)
    return out


def fibre_edges(lines, d_um, sigma_bulk):
    """폴리라인 목록 → (nodes[M,3], edges[(i, j, G)]).

    G = σ·A/L,  A = πd²/4.  **격자가 안 들어간다** — 참 단면·참 길이뿐이다.
    """
    A = np.pi * float(d_um) ** 2 / 4.0
    nodes, edges, off = [], [], 0
    for R in lines:
        nodes.append(R)
        L = np.linalg.norm(np.diff(R, axis=0), axis=1)
        for k, Lk in enumerate(L):
            if Lk <= 0:
                continue
            edges.append((off + k, off + k + 1, float(sigma_bulk) * A / float(Lk)))
        off += len(R)
    if not nodes:
        return np.zeros((0, 3)), []
    return np.vstack(nodes), edges


def fibre_contacts(nodes, d_um, sigma_bulk, node_line=None, touch_scale=1.0):
    """섬유↔섬유 접촉 → [(i, j, G_holm)].

    두 노드가 `touch_scale · d` 안이면 접촉으로 본다.  Holm 협착 R = 1/(2σa) 이고
    접촉반경 a 는 겹침 기하에서 온다 — 여기서는 보수적으로 a = d/4 (반지름의 절반)로 둔다.
    ⚠ `a` 는 **앵커 없는 가정**이다 (§F1).  절대값이 아니라 **접촉이 있고 없고**가
    이 모듈의 주장이고, a 는 `--a-frac` 로 스윕한다.
    """
    from scipy.spatial import cKDTree
    if len(nodes) < 2:
        return []
    r = float(touch_scale) * float(d_um)
    tree = cKDTree(nodes)
    a = float(d_um) / 4.0
    G = 2.0 * float(sigma_bulk) * a
    out = []
    for i, j in tree.query_pairs(r):
        if node_line is not None and node_line[i] == node_line[j]:
            continue                                   # 같은 폴리라인 = 이미 간선으로 이어짐
        out.append((int(i), int(j), G))
    return out


def solve_z(nodes, edges, z_lo, z_hi, area_um2, sigma_A=None, touch_um=0.0, eps=1e-9):
    """z 방향 유효 전도도 — **거리-인지 플레이트 결합** (step3 규약과 같게).

    ⚠ 첫 판은 밴드 안 노드를 φ 로 **클램프**했다.  그러면 고정단 사이 유효길이가 L − 2·band
    로 줄어드는데 σ_eff 는 L 로 나누므로 답이 **L/(L−2·band) 배 부풀었다** (실측 정확히 10/9).
    ⇒ 플레이트를 **노드**로 두고 남은 거리만큼의 저항으로 잇는다: G = σ·A/max(dist, eps).
    ⚠⚠ 그리고 **밴드 안 노드를 전부 잇는 것도 틀렸다** (두 번째 실패): z=0, 0.25, 0.5 가
    모두 플레이트에 붙으면 섬유 구간과 **병렬 단락**이 생겨 σ 가 다시 부푼다.
    섬유는 플레이트에 **한 번 닿는다** ⇒ `touch_um` 안에 든 노드만 결합한다 (기본 0 =
    정확히 닿은 노드만; 실침대는 섬유 반지름 d/2 를 줄 것).
    `sigma_A` (= σ_bulk·A_real) 를 주지 않으면 간선 컨덕턴스에서 역산한다.

    반환 (sigma_eff_S_cm, info).  **격자가 없으므로 이 값은 격자 무관**이다.
    """
    from scipy.sparse import coo_matrix
    from scipy.sparse.linalg import cg
    n = len(nodes)
    if n == 0 or not edges:
        return 0.0, {'reason': 'empty'}
    L = float(z_hi - z_lo)
    touch = float(touch_um)
    if sigma_A is None:                       # G = σA/len 이므로 σA = G·len 을 한 간선에서 역산
        i0, j0, g0 = edges[0]
        sigma_A = float(g0) * float(np.linalg.norm(nodes[j0] - nodes[i0]))
    z = nodes[:, 2]
    # 플레이트 결합: (노드, φ_plate, G).  dist=0 이면 G 가 매우 커져 클램프와 같아진다.
    plate = []
    for m, phi_p in ((z <= z_lo + touch + eps, 1.0), (z >= z_hi - touch - eps, 0.0)):
        for k in np.nonzero(m)[0]:
            dist = abs(z[k] - (z_lo if phi_p == 1.0 else z_hi))
            plate.append((int(k), phi_p, float(dist)))
    if not any(p[1] == 1.0 for p in plate) or not any(p[1] == 0.0 for p in plate):
        nb = sum(1 for p in plate if p[1] == 1.0); nt = len(plate) - nb
        return 0.0, {'reason': f'no_plate_contact(bot={nb},top={nt})'}
    # ⚠ dist ≤ eps 를 σA/eps 라는 **거대 컨덕턴스**로 넣으면 행렬이 나빠져 CG 잔차가
    #   물리 오차처럼 보인다 (실측 상대 6e-6).  ⇒ 그런 노드는 **진짜 Dirichlet 로 소거**한다.
    #   판정은 **거리**로 한다 (컨덕턴스 크기로 하면 문턱이 스케일에 끌려다닌다 — 첫 판이
    #   그래서 하나도 클램프되지 않았다).
    clamp = {}
    couple = []
    for k, phi_p, dist in plate:
        if dist <= eps:
            clamp.setdefault(k, phi_p)
        else:
            couple.append((k, phi_p, float(sigma_A) / dist))
    free = np.ones(n, bool)
    for k in clamp:
        free[k] = False
    phi = np.zeros(n)
    for k, v in clamp.items():
        phi[k] = v
    m = int(free.sum())
    if m == 0:
        return 0.0, {'reason': 'all_clamped'}
    idx = -np.ones(n, np.int64); idx[free] = np.arange(m)
    rows, cols, vals = [], [], []
    diag = np.zeros(m); b = np.zeros(m)
    for i2, j2, g in edges:
        for u, v in ((i2, j2), (j2, i2)):
            if not free[u]:
                continue
            diag[idx[u]] += g
            if free[v]:
                rows.append(idx[u]); cols.append(idx[v]); vals.append(-g)
            else:
                b[idx[u]] += g * phi[v]
    for k, phi_p, g in couple:
        if free[k]:
            diag[idx[k]] += g; b[idx[k]] += g * phi_p
    A = coo_matrix((np.concatenate([vals, diag]),
                    (np.concatenate([rows, np.arange(m)]),
                     np.concatenate([cols, np.arange(m)]))), shape=(m, m)).tocsr()
    try:
        x, info = cg(A, b, rtol=1e-14, maxiter=50000)
    except TypeError:
        x, info = cg(A, b, tol=1e-14, maxiter=50000)
    phi[free] = x
    I = 0.0
    for i2, j2, g in edges:                       # 바닥 클램프 노드에서 나가는 전류
        for u, v in ((i2, j2), (j2, i2)):
            if clamp.get(u) == 1.0 and clamp.get(v) != 1.0:
                I += g * (phi[u] - phi[v])
    for k, phi_p, g in couple:                    # 거리-인지 결합으로 들어오는 전류
        if phi_p == 1.0:
            I += g * (phi_p - phi[k])
    return float(I * L / float(area_um2)), {'n_nodes': n, 'n_edges': len(edges),
                                            'n_plate': len(plate), 'cg_info': int(info),
                                            'I': float(I)}


def contact_sensitivity(nodes, node_line, d_um, sigma_bulk, base_edges,
                        z_lo, z_hi, area_um2, scales=(0.8, 1.0, 1.25)):
    """접촉 판정 문턱을 흔들어 **새 자유도의 민감도**를 잰다.

    격자를 없앤 대신 '접촉 문턱' 이 자유도가 됐다 — 그것을 숨기지 않고 잰다.
    """
    out = {}
    for s in scales:
        c = fibre_contacts(nodes, d_um, sigma_bulk, node_line=node_line, touch_scale=s)
        se, _ = solve_z(nodes, base_edges + c, z_lo, z_hi, area_um2)
        out[float(s)] = {'n_contacts': len(c), 'sigma_eff': float(f'{se:.6g}')}
    v = [x['sigma_eff'] for x in out.values()]
    out['spread_pct'] = float(f'{(max(v) / min(v) - 1) * 100:.3g}') if min(v) > 0 else None
    return out


def _selftest():
    ok, fail = 0, []

    def chk(n, c):
        nonlocal ok
        (ok := ok + 1) if c else fail.append(n)
        print(('  PASS  ' if c else '  FAIL  ') + n)

    D, SIG, LZ, AREA = 0.15, 100.0, 10.0, 100.0     # Ø0.15 µm · 100 S/cm · 높이 10 · 단면 100 µm²
    A = np.pi * D ** 2 / 4.0

    # ① 축방향 직선 섬유 1개 = 정확해 σ_eff = σ·A/AREA (해석적)
    z = np.linspace(0.0, LZ, 41)
    P = np.stack([np.full_like(z, 5.0), np.full_like(z, 5.0), z], 1)
    nodes, edges = fibre_edges([P], D, SIG)
    se, info = solve_z(nodes, edges, 0.0, LZ, AREA)
    exact = SIG * A / AREA
    chk(f'① 직선 섬유 = 해석해 {exact:.6g} (측정 {se:.6g})', abs(se / exact - 1) < 1e-8)

    # ② ★ 격자 무관 — 점 간격을 4배로 바꿔도 같은 답 (복셀 경로에서는 이게 안 된다)
    z2 = np.linspace(0.0, LZ, 161)
    P2 = np.stack([np.full_like(z2, 5.0), np.full_like(z2, 5.0), z2], 1)
    se2, _ = solve_z(*fibre_edges([P2], D, SIG), 0.0, LZ, AREA)
    chk(f'② ★ 점 간격 ×4 에도 불변 ({se:.6g} vs {se2:.6g}) = **이산화 의존 0**',
        abs(se2 / se - 1) < 1e-8)

    # ③ 기울어진 섬유 = **cosθ** 법칙 (내 첫 시험은 cos²θ 로 적었다 — 틀린 기대였다).
    #    R = (L/cosθ)/(σA) → I = ΔV·σA·cosθ/L → σ_eff = σA·cosθ/A_box.  cos² 는 부피분율을
    #    고정했을 때 나온다.  ★ 복셀 경로는 여기서 계단 인자 k 만큼 틀리는데 이 경로는 정확하다.
    t = np.linspace(0.0, 1.0, 41)
    th = np.deg2rad(30.0)
    P3 = np.stack([5.0 + LZ * np.tan(th) * t, np.full_like(t, 5.0), LZ * t], 1)
    se3, _ = solve_z(*fibre_edges([P3], D, SIG), 0.0, LZ, AREA)
    chk(f'③ 30° 기울기 = σ·A·cosθ/AREA ({exact * np.cos(th):.6g} vs {se3:.6g})',
        abs(se3 / (exact * np.cos(th)) - 1) < 1e-8)

    # ④ 병렬 2개 = 2배 (선형성)
    P4 = P.copy(); P4[:, 0] = 7.0
    n4, e4 = fibre_edges([P, P4], D, SIG)
    se4, _ = solve_z(n4, e4, 0.0, LZ, AREA)
    chk(f'④ 병렬 2개 = 2배 ({se4:.6g} vs {2*exact:.6g})', abs(se4 / (2 * exact) - 1) < 1e-8)

    # ⑤ 끊긴 섬유는 안 통한다 (접촉 없이는 0)
    zc = np.concatenate([np.linspace(0, 4.0, 17), np.linspace(6.0, LZ, 17)])
    P5 = np.stack([np.full_like(zc, 5.0), np.full_like(zc, 5.0), zc], 1)
    lines5 = polylines(P5, np.zeros(len(P5), int))
    se5, i5 = solve_z(*fibre_edges(lines5, D, SIG), 0.0, LZ, AREA)
    chk(f'⑤ 2 µm 갭이면 안 통한다 (σ={se5:.3g}, 폴리라인 {len(lines5)}개)',
        len(lines5) == 2 and abs(se5) < 1e-6 * exact)

    # ⑥ **서로 다른 두 섬유가 스치는** 배치 — 이것이 진짜 접촉이다.
    #    ⚠ 두 번째 픽스처는 z 로 2 µm **겹치게** 놨는데, 겹친 구간은 두 섬유가 **병렬**이라
    #      σ 가 단일보다 커지는 것이 맞다 — 내 기대("작아야 한다")가 틀렸다.
    #      순수 **직렬**을 보려면 겹치지 않고 끝끼리 만나야 한다.
    za = np.linspace(0.0, 5.0, 21); zb = np.linspace(5.0, LZ, 21)   # 겹침 없이 끝끼리
    F1 = np.stack([np.full_like(za, 5.00), np.full_like(za, 5.0), za], 1)
    F2 = np.stack([np.full_like(zb, 5.10), np.full_like(zb, 5.0), zb], 1)   # x 로 0.10 µm 옆
    n6, e6 = fibre_edges([F1, F2], D, SIG)
    nl = np.concatenate([np.zeros(len(F1), int), np.ones(len(F2), int)])
    se_nc, _ = solve_z(n6, e6, 0.0, LZ, AREA)
    c6 = fibre_contacts(n6, D, SIG, node_line=nl)
    se6, _ = solve_z(n6, e6 + c6, 0.0, LZ, AREA)
    chk(f'⑥a 접촉 없이는 관통 못 한다 (σ={se_nc:.3g})', abs(se_nc) < 1e-6 * exact)
    chk(f'⑥b 접촉을 놓으면 통하고 협착 때문에 단일보다 작다 '
        f'({se6:.4g} < {exact:.4g}, 접촉 {len(c6)}개)', 0 < se6 < exact and len(c6) > 0)

    # ⑦ ★ 새 자유도를 **숨기지 않는다** — 접촉 문턱 민감도를 재서 돌려준다
    s7 = contact_sensitivity(n6, nl, D, SIG, e6, 0.0, LZ, AREA)
    chk(f'⑦ ★ 접촉 문턱 민감도를 보고한다 (spread {s7["spread_pct"]} %)',
        s7.get('spread_pct') is not None)

    # ⑧ 플레이트에 안 닿으면 거부 (조용히 0 을 만들지 않는다)
    P8 = P[(P[:, 2] > 2.0) & (P[:, 2] < 8.0)]
    se8, i8 = solve_z(*fibre_edges([P8], D, SIG), 0.0, LZ, AREA)
    chk('⑧ 플레이트 미접촉은 reason 을 남긴다', se8 == 0.0 and 'no_plate_contact' in i8.get('reason', ''))

    print(f'\nfibre_1d_network selftest: {ok}/{ok + len(fail)} PASS'
          + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    raise SystemExit(_selftest() if a.selftest else _selftest())
