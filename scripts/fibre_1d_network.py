"""섬유를 **복셀에 굽지 않고 1D 저항 요소로** 푼다.

⚠⚠ **격위 강등 2026-08-13 (CL-23 → hold, Codex CDX-06/07/08)** — 이 파일은 한때 스스로를
  "격자 의존의 근본 해법" 이라고 적었다.  **철회한다.**  적대 리뷰가 낸 반례 셋이 전부
  재현됐고 (지금은 selftest ⑨⑪⑫ 로 상주), 자유도는 없어진 게 아니라 **옮겨졌다**:
    · 접촉 판정 문턱 `touch_scale`  · Holm 접촉반경 `a_frac` (앵커 없음 §F1)
    · 분포 접촉(나란한 섬유)에 점접촉 Holm 을 쓰는 것 자체가 미해결
  ⇒ 지금 이 모듈이 주장할 수 있는 **한 문장**:
      "순서가 정해진 접촉 없는 고정 폴리라인의 축방향 edge conductance 는
       기존 edge 의 단순 세분에 불변이고 직선 해석해와 일치한다."
  실침대 절대 σ · SBE/DBE 비 · "복셀 경로 대체" 에는 **인용 금지**.

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
이 파일은 **섬유 부분망**만 만들고 검증한다.
⚠ 복셀 FV 와의 결합(`couple_to_voxel_grid`)은 **아직 없다** — 설명에만 있고 정의도 호출도
  없다 (Codex CDX-08 이 지적, 확인함).  그것이 생기기 전까지 이 모듈은 실침대 σ_e 를
  낼 수 없다.

⚠ 접촉 판정은 2026-08-13 에 **선분↔선분 기하**로 옮겨 점 샘플링 의존을 없앴다 (selftest
  ⑪⑫).  그래도 남는 자유도는 `touch_scale`(접촉 문턱)과 `a_frac`(Holm 반경)이고, 둘 다
  앵커가 없다 (§F1).  `contact_sensitivity()` 가 전자를, `--a-frac` 이 후자를 스윕한다.
  "격자를 없앴다" 가 아니라 "격자 의존을 **잰 자유도**로 바꿨다".

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


def _seg_seg_dist(p1, q1, p2, q2):
    """두 **선분** 사이 최단거리와 각 선분 위의 매개변수 (s, t).  표준 Ericson 알고리즘."""
    d1, d2, r = q1 - p1, q2 - p2, p1 - p2
    a, e, f = float(d1 @ d1), float(d2 @ d2), float(d2 @ r)
    if a <= 1e-30 and e <= 1e-30:
        return float(np.linalg.norm(r)), 0.0, 0.0
    if a <= 1e-30:
        s, t = 0.0, min(max(f / e, 0.0), 1.0)
    else:
        c = float(d1 @ r)
        if e <= 1e-30:
            t, s = 0.0, min(max(-c / a, 0.0), 1.0)
        else:
            b = float(d1 @ d2)
            den = a * e - b * b
            s = min(max((b * f - c * e) / den, 0.0), 1.0) if den > 1e-30 else 0.0
            t = (b * s + f) / e
            if t < 0.0:
                t, s = 0.0, min(max(-c / a, 0.0), 1.0)
            elif t > 1.0:
                t, s = 1.0, min(max((b - c) / a, 0.0), 1.0)
    w = (p1 + s * d1) - (p2 + t * d2)
    return float(np.linalg.norm(w)), float(s), float(t)


def fibre_contacts(nodes, edges, d_um, sigma_bulk, node_line=None, touch_scale=1.0,
                   a_frac=0.25, return_meta=False):
    """섬유↔섬유 접촉 → [(i, j, G_holm)].  **선분↔선분 기하**로 판정한다.

    ⚠⚠ 2026-08-13 전면 재작성 (Codex CDX-06, 반례 3개를 직접 재현하고 고쳤다).
    첫 판은 cKDTree 로 **노드 쌍**을 봤고, 그래서 같은 물리를 표현점 수에 따라 다르게 셌다:
      · 직교로 교차하는 두 선분 — 교차점을 노드로 넣으면 접촉 1, 안 넣으면 **0**
      · 나란한 두 선분을 41 → 161 점으로 재표현 — 접촉 41 → **481** (11.7배 병렬 단락)
    ⇒ 판정을 **선분**(간선) 단위로 옮긴다.  곡선을 세분해도 곡선 위의 점 집합은 그대로이므로
      선분-선분 최단거리는 **재표현에 불변**이다.

    그리고 접촉하는 선분쌍을 **접촉 패치**로 묶어 패치당 Holm 하나만 낸다 (같은 물리 접촉을
    여러 병렬 간선으로 중복 적용하지 않는다).  패치는 같은 선쌍 안에서 단일연결로 묶는다.

    Holm 협착 R = 1/(2σa), a = `a_frac`·d (기본 0.25 = 반지름의 절반).
    ⚠ `a_frac` 는 **앵커 없는 가정**이다 (§F1) — `--a-frac` 로 스윕할 것.
    ⚠⚠ Holm 은 **점접촉** 모델이다.  나란히 스치는 두 섬유처럼 접촉이 **선(분포)** 이면
      이 모델은 물리적으로 맞지 않는다 — 패치 길이 `len_um` 를 함께 돌려주니 그것이
      d 보다 훨씬 크면 결과를 쓰지 말 것 (분포 접촉 모델은 미구현).
    """
    from scipy.spatial import cKDTree
    if len(nodes) < 2 or not edges:
        return ([], []) if return_meta else []
    P = np.asarray(nodes, float)
    seg = [(int(e[0]), int(e[1])) for e in edges]
    if not seg:
        return ([], []) if return_meta else []
    mid = np.array([(P[i] + P[j]) / 2.0 for i, j in seg])
    half = np.array([float(np.linalg.norm(P[j] - P[i])) / 2.0 for i, j in seg])
    thr = float(touch_scale) * float(d_um)
    tree = cKDTree(mid)
    # 중점 거리 ≤ thr + 두 반길이 → 후보.  최대 반길이로 한 번에 조회하고 뒤에서 정확히 거른다.
    pairs = tree.query_pairs(thr + 2.0 * float(half.max()))
    hit = {}                                          # (line_a, line_b) → [(segA, segB, dist)]
    for u, v in pairs:
        ia, ja = seg[u]
        ib, jb = seg[v]
        if node_line is not None:
            la, lb = int(node_line[ia]), int(node_line[ib])
            if la == lb:
                continue                              # 같은 폴리라인 = 이미 간선으로 이어짐
        else:
            la, lb = u, v
        if {ia, ja} & {ib, jb}:
            continue                                  # 노드를 공유 = 같은 사슬
        dist, s_, t_ = _seg_seg_dist(P[ia], P[ja], P[ib], P[jb])
        if dist <= thr:
            hit.setdefault((min(la, lb), max(la, lb)), []).append((u, v, dist, s_, t_))
    a = float(a_frac) * float(d_um)
    G = 2.0 * float(sigma_bulk) * a
    out, meta = [], []
    for (_la, _lb), lst in sorted(hit.items()):
        # 같은 선쌍 안에서 **인접한 접촉 선분들**을 하나의 패치로 묶는다 (단일연결).
        segs_a = sorted({u for u, _v, _d, _s, _t in lst})
        parent = {s: s for s in segs_a}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for x, y in zip(segs_a, segs_a[1:]):
            if y - x == 1:                            # 같은 선 위에서 연속한 선분 = 같은 패치
                parent[find(y)] = find(x)
        patch = {}
        for rec in lst:
            patch.setdefault(find(rec[0]), []).append(rec)
        for members in patch.values():
            u, v, _d, s_, t_ = min(members, key=lambda r: r[2])   # 가장 가까운 선분쌍
            # ⚠ 대표 노드는 **접촉점에 가까운 쪽**이어야 한다.  첫 판은 무조건 선분의 앞
            #   노드를 썼는데, 그러면 접촉이 그 선분을 **건너뛰는 지름길**이 되어 σ 가
            #   오히려 커졌다 (⑥b 가 0.0177 > 해석해 0.0176715 로 잡아냈다).
            ia = seg[u][0] if s_ <= 0.5 else seg[u][1]
            ib = seg[v][0] if t_ <= 0.5 else seg[v][1]
            ln = sum(float(np.linalg.norm(P[seg[m][1]] - P[seg[m][0]]))
                     for m in {r[0] for r in members})
            out.append((int(ia), int(ib), G))
            meta.append({'len_um': float(f'{ln:.6g}'), 'n_seg_pairs': len(members),
                         'distributed': bool(ln > 3.0 * float(d_um))})
    return (out, meta) if return_meta else out


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
    # ── 섬유 소속(연결성분) — 플레이트 탭을 **섬유당 하나**로 줄이는 데 쓴다 ──────────────
    #   ⚠⚠ 2026-08-13 (Codex CDX-07): 밴드 안 노드를 **전부** 물리면 같은 섬유가 플레이트에
    #     여러 번 닿아 병렬 단락이 생기고, 같은 직선을 41 → 161 점으로 재표현하면 σ 가
    #     +0.63 % 움직인다 (재현).  섬유는 플레이트에 **한 번** 닿는다.
    comp = np.arange(n)
    for _ in range(2):                                # 두 번이면 이 크기에서 수렴한다
        for e in edges:
            i2, j2 = int(e[0]), int(e[1])
            r_ = min(comp[i2], comp[j2])
            comp[i2] = comp[j2] = r_
        for k in range(n):
            comp[k] = comp[comp[k]]
    # 플레이트 결합: (노드, φ_plate, G).  dist=0 이면 G 가 매우 커져 클램프와 같아진다.
    plate, best = [], {}
    for m, phi_p in ((z <= z_lo + touch + eps, 1.0), (z >= z_hi - touch - eps, 0.0)):
        for k in np.nonzero(m)[0]:
            dist = abs(z[k] - (z_lo if phi_p == 1.0 else z_hi))
            key = (int(comp[k]), phi_p)               # 섬유 × 플레이트 → 가장 가까운 노드 하나
            if key not in best or dist < best[key][1]:
                best[key] = (int(k), float(dist))
    for (_c, phi_p), (k, dist) in best.items():
        plate.append((k, phi_p, dist))
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
    # ⚠⚠ 2026-08-13 (Codex CDX-07): 첫 판은 여기서 `all_clamped` 로 **0 을 반환**했다.
    #   그런데 두 플레이트에 정확히 닿는 2-노드 섬유는 자유노드가 없을 뿐 전류는 정의된다
    #   (I = G·Δφ).  실측: 반환 0.0 vs 정확해 0.01767146 — 완전한 오답이었다.
    #   ⇒ 자유노드가 없으면 **선형계를 건너뛰고** 클램프-클램프 간선의 전류를 바로 센다.
    info_extra = {}
    if m == 0:
        idx = -np.ones(n, np.int64)
        x, info = np.zeros(0), 0
        info_extra['note'] = 'all_clamped — 클램프-클램프 간선 전류로 직접 계산'
    else:
        idx = -np.ones(n, np.int64); idx[free] = np.arange(m)
    rows, cols, vals = [], [], []
    diag = np.zeros(m); b = np.zeros(m)
    for e in edges:
        i2, j2, g = int(e[0]), int(e[1]), float(e[2])
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
    if m:
        A = coo_matrix((np.concatenate([vals, diag]),
                        (np.concatenate([rows, np.arange(m)]),
                         np.concatenate([cols, np.arange(m)]))), shape=(m, m)).tocsr()
        try:
            x, info = cg(A, b, rtol=1e-14, maxiter=50000)
        except TypeError:
            x, info = cg(A, b, tol=1e-14, maxiter=50000)
        phi[free] = x
    I = 0.0
    for e in edges:                               # 바닥 클램프 노드에서 나가는 전류
        i2, j2, g = int(e[0]), int(e[1]), float(e[2])
        for u, v in ((i2, j2), (j2, i2)):
            if clamp.get(u) == 1.0 and clamp.get(v) != 1.0:
                I += g * (phi[u] - phi[v])
    for k, phi_p, g in couple:                    # 거리-인지 결합으로 들어오는 전류
        if phi_p == 1.0:
            I += g * (phi_p - phi[k])
    return float(I * L / float(area_um2)), dict(
        {'n_nodes': n, 'n_edges': len(edges), 'n_plate': len(plate),
         'n_free': m, 'cg_info': int(info), 'I': float(I)}, **info_extra)


def contact_sensitivity(nodes, node_line, d_um, sigma_bulk, base_edges,
                        z_lo, z_hi, area_um2, scales=(0.8, 1.0, 1.25), a_frac=0.25):
    """접촉 판정 문턱을 흔들어 **새 자유도의 민감도**를 잰다.

    격자를 없앤 대신 '접촉 문턱' 이 자유도가 됐다 — 그것을 숨기지 않고 잰다.
    """
    out = {}
    for s in scales:
        c = fibre_contacts(nodes, base_edges, d_um, sigma_bulk, node_line=node_line,
                           touch_scale=s, a_frac=a_frac)
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
    c6 = fibre_contacts(n6, e6, D, SIG, node_line=nl)
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

    # ══ 2026-08-13 Codex 적대 리뷰 반례 (CDX-06/07/08) ══════════════════════════════
    #   전부 **먼저 실패를 재현하고** 고쳤다.  옛 코드의 실측 오답을 주석에 남긴다.

    # ⑨ 2-노드 섬유가 두 플레이트에 정확히 닿는다 — 옛 코드는 `all_clamped` 로 **0.0** 반환
    n9, e9 = fibre_edges([np.array([[5., 5., 0.], [5., 5., LZ]])], D, SIG)
    se9, i9 = solve_z(n9, e9, 0.0, LZ, AREA)
    chk(f'⑨ 2-노드 전관통 = 해석해 {exact:.6g} (옛 코드 0.0, 지금 {se9:.6g})',
        abs(se9 / exact - 1) < 1e-10)

    # ⑩ 플레이트 탭은 섬유당 하나 — 밴드를 두껍게 줘도 재표현에 불변이어야 한다
    #    (옛 코드: 41 → 161 점 재표현에 σ 가 +0.629 % 움직였다)
    def _band(npts):
        zz = np.linspace(0.0, LZ, npts)
        Q = np.stack([np.full_like(zz, 5.0), np.full_like(zz, 5.0), zz], 1)
        return solve_z(*fibre_edges([Q], D, SIG), 0.0, LZ, AREA, touch_um=D / 2)[0]
    b41, b161 = _band(41), _band(161)
    chk(f'⑩ 두꺼운 밴드(touch=d/2)에서도 재표현 불변 ({b41:.8g} vs {b161:.8g})',
        abs(b161 / b41 - 1) < 1e-10)

    # ⑪ 직교 교차 두 선분 — 교차점을 노드로 **안** 넣어도 접촉을 찾아야 한다
    #    (옛 노드-쌍 판정: 안 넣으면 0, 넣으면 1)
    xa = np.array([[4.5, 5., 5.], [5.5, 5., 5.]])
    xb = np.array([[5., 4.5, 5.], [5., 5.5, 5.]])
    nx, ex = fibre_edges([xa, xb], D, SIG)
    nlx = np.array([0, 0, 1, 1])
    xa2 = np.array([[4.5, 5., 5.], [5., 5., 5.], [5.5, 5., 5.]])
    xb2 = np.array([[5., 4.5, 5.], [5., 5., 5.], [5., 5.5, 5.]])
    nx2, ex2 = fibre_edges([xa2, xb2], D, SIG)
    nlx2 = np.array([0, 0, 0, 1, 1, 1])
    c_coarse = fibre_contacts(nx, ex, D, SIG, node_line=nlx)
    c_fine = fibre_contacts(nx2, ex2, D, SIG, node_line=nlx2)
    chk(f'⑪ 직교 교차 = 표현점 수에 불변 (성긴 {len(c_coarse)} · 촘촘 {len(c_fine)}; '
        f'옛 코드 0 vs 1)', len(c_coarse) == len(c_fine) == 1)

    # ⑫ 나란한 두 선분 — 재표현해도 접촉 **패치 수**가 같아야 한다 (옛 코드 41 → 481)
    def _par(npts):
        zz = np.linspace(0.0, LZ, npts)
        Pa = np.stack([np.full_like(zz, 5.0), np.full_like(zz, 5.0), zz], 1)
        Pb = np.stack([np.full_like(zz, 5.1), np.full_like(zz, 5.0), zz], 1)
        nn, ee = fibre_edges([Pa, Pb], D, SIG)
        nll = np.r_[np.zeros(npts, int), np.ones(npts, int)]
        return fibre_contacts(nn, ee, D, SIG, node_line=nll, return_meta=True)
    (p41, m41), (p161, m161) = _par(41), _par(161)
    chk(f'⑫ 나란한 두 섬유 = 재표현 불변 ({len(p41)} vs {len(p161)}; 옛 코드 41 vs 481)',
        len(p41) == len(p161) == 1)
    chk(f'⑫b 분포 접촉임을 **라벨한다** (패치 길이 {m41[0]["len_um"]} µm ≫ d={D})',
        m41[0]['distributed'] and m161[0]['distributed'])

    # ⑬ a_frac 은 실제로 결과를 바꾼다 (docstring 에만 있고 CLI 에 없었다 — CDX-08)
    ca = fibre_contacts(n6, e6, D, SIG, node_line=nl, a_frac=0.25)
    cb = fibre_contacts(n6, e6, D, SIG, node_line=nl, a_frac=0.50)
    sa = solve_z(n6, e6 + ca, 0.0, LZ, AREA)[0]
    sb = solve_z(n6, e6 + cb, 0.0, LZ, AREA)[0]
    chk(f'⑬ a_frac 0.25 → 0.50 이 σ 를 바꾼다 ({sa:.4g} → {sb:.4g})', sb > sa > 0)

    print(f'\nfibre_1d_network selftest: {ok}/{ok + len(fail)} PASS'
          + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--a-frac', type=float, default=0.25,
                    help='Holm 접촉반경 a = a_frac·d (앵커 없는 가정 §F1 — 스윕용)')
    a = ap.parse_args()
    raise SystemExit(_selftest() if a.selftest else _selftest())
