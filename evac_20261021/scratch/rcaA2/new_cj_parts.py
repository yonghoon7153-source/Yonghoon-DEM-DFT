# New / replaced top-level items for scripts/carbon_junction.py (A round 2 · 10-21 pre-review impl fixes).
# Applied by patch_cj.py (replace top-level defs by name · insert new ones after anchors).  Not imported directly.
# flake8: noqa

CJUNC_MODEL_VERSION = 'r3-carbon-junction-port-v3'   # v3 (10-21 사전 리뷰 impl · Q-A 조각 = 섬유 · 고리 이음매 · Q-B 자기 = 중심선 근접 + 쌍 s · Q-C 옮김 없음 · Q-D SV 다리만 끊음)
CJUNC_SELF_LC_RULE = 'touch_len_max_junction_pairs_v2'   # 자기 접합 L_c — 같은 닿음 규칙 · 짝 = 그 instance 의 접합 쌍 (바닥 · s 규칙을 지난 쌍) 만
CJUNC_SELF_S_RULE = 'arc_at_closest_points_piece_cyclic_v2'   # s = 쌍의 최근접점 사이 조각 호 길이 (고리 = 짧은 쪽) · 쌍마다
CJUNC_PORT_RULE = 'nearest_cell_centre_any_liveness_within_rport_no_relocation_eps_band_tie_lex_ijk_branch_dist_v3'   # 10-21 Q-C
CJUNC_SELF_RULE = 'same_piece_centreline_pairs_d_le_D_floor_s_gt_D_and_halfpi_d_s_ge_s_min_v3'          # 10-21 Q-B
CJUNC_PIECE_RULE = 'piece_is_fibre_closed_path_seam_continuous_v1'           # 10-21 Q-A — 조각 = 섬유 · 닫힌 경로 이음매 = 연속
CJUNC_SV_CF_KIND = 'counterfactual_cut_sv_bridges_keep_self_v1'              # 10-21 Q-D — 반사실 대조 기록 종류 (옛 counterfactual_cut_sv_faces)
CJUNC_SV_CF_RULE = 'sdcp_component_owner_groups_same_piece_continuity_or_covered_through_cut_nonpassing_v1'

CJUNC_QUALIFIERS = (
    'R_j = 모형 내부 보정값 (재료값 아님 · 포트 = 셀 중심 · 직접 간선에 반셀 · 접근 몫 없음 → 그 몫이 R_j 에 묶인다)',
    'VGCF–VGCF 만 정량 — VGCF–AM · SDCP–VGCF · SDCP–AM 면 = 옛 융합 (SDCP–VGCF 접촉 저항 0 가정)',
    'instance = 중심선 기하 근접 (관통 포함 · MPM 은 섬유 접촉 역학을 풀지 않는다) · 중심선 위치 불확도 = MPM 점 간격',
    'R_j,0 는 모든 VV instance 에 같은 값 · 접합 총 G = max(1, L_c/L_par)/R_j,0 (길이 법칙 v0 — 선 접촉 협착 ∝ 길이의 1차 근사 · '
    '점 접합 L_c/L_par 개 병렬) · 분산판 v0: k = ceil(L_c/L_par) 간선 · 각 G/k · 닿음 구간 k 등분 점의 기하 포트 · 간선마다 PTFE 덮임 · '
    'SDCP 근접 (L_c ≤ L_par = 점 접합 하나) · L_c = 닿음 길이 (중심선 기하 근접) · 분산 간선 = 같은 R_j,0 의 균일 분포 근사 '
    '(접점 저항 분포 · 전달 길이 미검증) · k 가 바뀌는 L_c/L_par 정수 경계에서 σ 가 계단으로 뛴다 (이산화 오차 · 크기 ∝ h·r′/R_j)',
    '조각 = 섬유 — 같은 fid 의 끊긴 조각 (생산 끊기 규칙) 은 서로 다른 섬유와 같은 접합 규칙 (중심선 d ≤ D → R_j) · 닫힌 경로의 '
    '이음매 = 연속 · 자기 접합 = 같은 조각 중심선 쌍 d ≤ D 가 바닥 (s > D · s > (π/2)·d) 을 넘고 s ≥ s_min (s = 쌍의 경로 호 길이) — '
    's < s_min = 같은 가닥의 연속 (접합 아님 · 면 = 옛 융합) · 같은 셀 재방문 = 가지 (연속 구간) 마다 따로 (합치지 않는다 · RCA-03) · '
    's_min = 등록 문턱 (없으면 정량 거부)',
    '덮인 접점 (포트로 고른 셀이 SDCP · PTFE · 상자 밖) = 옮기지 않고 미실현 — 덮은 상의 법칙만 (SDCP = SV 융합 · S3 c · PTFE = '
    'face_alpha P0/P1 · 같은 접촉을 두 번 세지 않는다) · 접합 + PTFE centerline = 거부',
    'S3 c ∈ {0, 1} = 시나리오 끝 (재료 예측 아님 · c = 1 = 근접 접합 축약 끝 · 젖음 상한 아님)',
    'SV_local_dissipation = SV 면 + SDCP 셀 소산 몫 (국소 저항 민감도 진단) — 경로 지배 · 우회 크기 보증 아님 (RCA-06 · 옛 '
    'SV_DOMINANT 표지 철회) · 반사실 대조 (서로 다른 섬유 · 접합으로 갈린 가지를 잇는 SV 다리만 끊고 SDCP 를 지나는 섬유의 자기 '
    '연속은 남긴 판의 단자 G 비) = 선택 노브 · 문턱 = 등록',
)


def _self_floor(s_um, d_um, D):
    """같은 조각 중심선 쌍의 바닥 (★ 10-21 사전 리뷰 PRE-impl-02 · 1저자 Q-B) — s > D (곧은 가닥의 이웃 쌍은 s = d ≤ D) 그리고
    s > (π/2)·d (꺾임 모서리: 꼭짓각 θ 에서 s/d ≤ 1/sin(θ/2) — θ ≥ 79° 이면 ≤ π/2 · 반원 굽힘 s = (π/2)·d 가 경계).  바닥 밖 쌍 =
    어느 s_min 에서도 같은 가닥의 연속 (접합 후보 아님)."""
    s = np.asarray(s_um, np.float64)
    d = np.asarray(d_um, np.float64)
    return (s > float(D)) & (s > 0.5 * math.pi * d)


def _distinct_keep(segs, i, j):
    """서로 다른 섬유 규칙의 선분 쌍 — ★ 10-21 (사전 리뷰 PRE-impl-01 · 1저자 Q-A) 조각이 다르면 (같은 fid 의 끊긴 조각 포함 · 조각 사이엔
    축방향 경로가 없다) 서로 다른 섬유와 같은 규칙 (d ≤ D → R_j · s 규칙 없음).  옛 = fid 가 다를 때만."""
    return segs['piece'][i] != segs['piece'][j]


def _ring_alias(cu, is_ring):
    """닫힌 경로 고리 조각 (★ 10-21 PRE-impl-06 · Q-A) 의 이음매 — 셀 열의 첫 · 끝 셀이 같으면 끝 위치를 첫 위치의 별칭 (한 dof) 으로 둔다
    (이음매 = 연속 · 옛: 첫 · 끝 위치 = 비연속 재방문 → s ≥ s_min 이면 R_j 접합 · 아니면 끊김)."""
    return bool(is_ring and len(cu) >= 2 and np.array_equal(cu[0], cu[-1]))


def _sv_cut_rows(info):
    """SV 반사실 대조가 끊을 SV 면 행 (★ 10-21 사전 리뷰 PRE-impl-04 · 1저자 Q-D · `CJUNC_SV_CF_RULE`) — SDCP 6-면 성분마다 그 성분에 SV 면으로
    닿는 VGCF 주인 위치를 무리 짓는다 (같은 조각 · 연속 (호 간격 = 같은 가닥) 또는 그 사이 위치가 전부 그 성분에 덮인 채 지남).  무리가 둘
    이상 = 다리 (서로 다른 섬유 · 접합으로 갈린 가지를 SV 가 잇는다) → 지나는 무리 (섬유가 그 성분을 지난다 = 자기 연속) 가 하나 이하면
    지나지 않는 무리의 행을 끊는다 · 지나는 무리가 둘 이상이면 못 가른다 (그대로 · 수 기록).  끊기만 = 부분 그래프 → 비 ≥ 1 (Rayleigh).
    info = {'comp': 성분 번호, 'group': 무리 번호, 'passing': 그 무리가 성분을 지나는가} (SV 행마다)."""
    comp, grp, pas = info['comp'], info['group'], info['passing']
    cut = np.zeros(len(comp), bool)
    for c in np.unique(comp):
        m = comp == c
        if len(np.unique(grp[m])) <= 1:
            continue
        if len(np.unique(grp[m & pas])) >= 2:
            continue
        cut |= m & ~pas
    return cut


def _closed_path(Q, kind_path):
    """닫힌 경로 (`CJUNC_PIECE_RULE`) — 경로 (kind 1) · 점 셋 이상 · 첫 점 = 끝 점 (좌표 비트 같음).  반올림으로 조금 떨어진 두 끝은 닫힌 것이
    아니다 (열린 경로의 두 끝이 만나는 접촉 = 같은 조각 쌍의 s 규칙)."""
    return bool(kind_path and len(Q) >= 3 and np.array_equal(Q[0], Q[-1]))


def _segments_of(paths, P, gap_tol):
    """경로 → 조각 (정준 방향) → 선분 표.  → dict(arrays) · 조각마다 (fid, 점 배열, kind_path).
    arc_a · arc_b = 선분 두 끝의 **조각 호 좌표** (꺾임 자기 접합 s) — 조각마다 그 조각의 저장 방향 (정준) 으로 연속 점 거리를 누적 ·
    점 역순 입력에서도 같은 비트.  선분 위 호 좌표 = arc_a + t·(arc_b − arc_a).
    ★ 10-21 (사전 리뷰 PRE-impl-01 · 1저자 Q-A) — 다른 조각 = 다른 섬유 (경로로 이어지지 않는다) → 호 좌표는 조각 안에서만 뜻이 있다
    (옛: fid 경로 전체 누적 · 조각 사이 간격 현 포함 = 끊긴 두 조각을 '같은 가닥의 연속' 으로 읽었다).
    ★ 닫힌 경로 (PRE-impl-06 · Q-A — 이음매 = 연속): 끊김이 있으면 마지막 조각 + 첫 조각을 이음매를 지나 한 조각으로 잇는다 (열린 조각 ·
    이음매는 조각 안 · 'piece_closed' 1) · 끊김이 없으면 고리 조각 하나 (`ring_L` = 고리 길이 > 0 · s = 고리 위 짧은 쪽 호 · 'piece_closed' 2 ·
    위치 첫 · 끝 = 이음매 = `_positions` 가 한 dof (별칭) 또는 축방향 이웃으로 잇는다).  끊김 판정은 원래 점열 그대로 (`fibre_pieces` — 생산
    스탬프와 같은 끊김 · 멤버십 셀 집합 불변).  조각마다 칸 (선분 표와 길이가 다름): piece_closed · piece_L."""
    sP0, sP1, sfid, spiece, sk, sa0, sa1, sring = [], [], [], [], [], [], [], []
    pieces = []
    pclosed, pL = [], []
    for f, r, kind_path in paths:
        Q = P[r]
        flip = bool(kind_path and _canon_flip(Q))
        Qc = Q[::-1] if flip else Q
        #  ★ 10-21 (RCA-04) — 조각 = 정준 방향 경로 (Qc) 의 순서 (옛: 입력 방향 순서 → 점 역순이 조각 번호 · 위치 순서를 바꿨다)
        ixs = fibre_pieces(Qc, gap_tol) if kind_path else [np.arange(len(Q))]
        closed = _closed_path(Qc, kind_path)
        ring_whole = bool(closed and len(ixs) == 1)
        joined = bool(closed and len(ixs) >= 2)
        if joined:                                           # 이음매를 지나 마지막 + 첫 조각을 잇는다 (Qc[−1] = Qc[0] — 점 하나 빼고)
            ixs = list(ixs[1:-1]) + [np.r_[ixs[-1], ixs[0][1:]].astype(np.int64)]
        for x_, ix in enumerate(ixs):
            R = Qc[ix]
            if kind_path and len(R) > 1 and _canon_flip(R):
                R = R[::-1]
            gp = len(pieces)
            pieces.append((f, R, kind_path))
            if len(R) == 1 or not kind_path:
                A = R; B = R                                  # 점 = 퇴화 선분 (경로 아닌 fid 도 점마다)
                a0 = np.zeros(len(R)); a1 = np.zeros(len(R))
                L_ring = 0.0
                Lp = 0.0
            else:
                A = R[:-1]; B = R[1:]
                cum = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(R, axis=0), axis=1))]
                a0 = cum[:-1]; a1 = cum[1:]
                Lp = float(cum[-1])
                L_ring = Lp if ring_whole else 0.0
            pclosed.append(2 if ring_whole else (1 if (joined and x_ == len(ixs) - 1) else 0))
            pL.append(Lp)
            sP0.append(A); sP1.append(B); sa0.append(a0); sa1.append(a1)
            sfid.append(np.full(len(A), f)); spiece.append(np.full(len(A), gp)); sk.append(np.arange(len(A)))
            sring.append(np.full(len(A), L_ring))
    if not pieces:
        z = np.zeros((0, 3))
        return {'P0': z, 'P1': z.copy(), 'fid': np.zeros(0, np.int64), 'piece': np.zeros(0, np.int64),
                'k': np.zeros(0, np.int64), 'arc_a': np.zeros(0), 'arc_b': np.zeros(0), 'ring_L': np.zeros(0),
                'piece_closed': np.zeros(0, np.int64), 'piece_L': np.zeros(0)}, pieces
    return {'P0': np.vstack(sP0), 'P1': np.vstack(sP1), 'fid': np.concatenate(sfid).astype(np.int64),
            'piece': np.concatenate(spiece).astype(np.int64), 'k': np.concatenate(sk).astype(np.int64),
            'arc_a': np.concatenate(sa0).astype(np.float64), 'arc_b': np.concatenate(sa1).astype(np.float64),
            'ring_L': np.concatenate(sring).astype(np.float64), 'piece_closed': np.asarray(pclosed, np.int64),
            'piece_L': np.asarray(pL, np.float64)}, pieces


def _positions(pieces, segs, lo, vox, n, sid):
    """조각 → 셀 열 (연속 중복 제거 · 정준 방향 번호) = 멤버십 위치.  생산 스탬프와 같은 원시 함수 (`segment_cells`) · 같은 셀.
    ★ 10-21 (Q-A · PRE-impl-06) — 고리 조각 (닫힌 경로 · 끊김 없음): 셀 열의 첫 · 끝 셀이 같으면 끝 위치 = 첫 위치의 별칭 ('alias' = 목표
    위치 · 조립기가 같은 dof · 비연속 재방문 아님) · 첫 · 끝 셀이 면으로 이웃이면 축방향 이웃 (면 표가 'ring' · 'piece_ng' 로 둘레를 잇는다)."""
    from fibre_segment_raster import segment_cells
    pf, pp, pk, plin, pijk, ps0, ps1, pal, prg, png = [], [], [], [], [], [], [], [], [], []
    seg_base = 0
    piece_pos = []
    npos = 0                                                 # 지금까지 위치 수 (조각마다 [시작, 끝) — 누적 · O(조각))
    ring_p = np.asarray(segs.get('piece_closed', np.zeros(len(pieces), np.int64)), np.int64) == 2
    for gp, (f, R, kind_path) in enumerate(pieces):
        nseg = 1 if (len(R) == 1 or not kind_path) else len(R) - 1
        if not kind_path:
            seg_base += len(R)
            piece_pos.append((npos, npos))
            continue
        if len(R) == 1:
            cells = np.floor((R - lo) / vox).astype(np.int64)
            sidx = np.zeros(1, np.int64)
        else:
            cl, si = [], []
            for i in range(len(R) - 1):
                c = segment_cells(R[i] - lo, R[i + 1] - lo, vox)
                cl.append(c); si.append(np.full(len(c), i))
            cells = np.vstack(cl).astype(np.int64); sidx = np.concatenate(si)
        new = np.ones(len(cells), bool)
        new[1:] = np.any(cells[1:] != cells[:-1], axis=1)
        grp = np.cumsum(new) - 1
        ng = int(grp[-1]) + 1
        cu = cells[new]
        s0 = np.full(ng, np.iinfo(np.int64).max); s1 = np.full(ng, -1)
        np.minimum.at(s0, grp, sidx); np.maximum.at(s1, grp, sidx)
        inb = ((cu >= 0) & (cu < n)).all(1)
        lin = np.full(ng, -1, np.int64)
        lin[inb] = np.ravel_multi_index(tuple(cu[inb].T), tuple(n))
        is_ring = bool(gp < len(ring_p) and ring_p[gp])
        al = np.full(ng, -1, np.int64)
        if _ring_alias(cu, is_ring):
            al[ng - 1] = npos                                 # 끝 위치 → 첫 위치 (전역 위치 번호)
        pf.append(np.full(ng, f)); pp.append(np.full(ng, gp)); pk.append(np.arange(ng)); plin.append(lin)
        pijk.append(cu); ps0.append(s0 + seg_base); ps1.append(s1 + seg_base)
        pal.append(al); prg.append(np.full(ng, is_ring)); png.append(np.full(ng, ng))
        piece_pos.append((npos, npos + ng))
        npos += ng
        seg_base += nseg
    if pf:
        pos = {'fid': np.concatenate(pf).astype(np.int64), 'piece': np.concatenate(pp).astype(np.int64),
               'k': np.concatenate(pk).astype(np.int64), 'lin': np.concatenate(plin).astype(np.int64),
               'ijk': np.vstack(pijk).astype(np.int64), 's0': np.concatenate(ps0).astype(np.int64),
               's1': np.concatenate(ps1).astype(np.int64), 'alias': np.concatenate(pal).astype(np.int64),
               'ring': np.concatenate(prg).astype(bool), 'piece_ng': np.concatenate(png).astype(np.int64)}
    else:
        z = np.zeros(0, np.int64)
        pos = {'fid': z, 'piece': z.copy(), 'k': z.copy(), 'lin': z.copy(), 'ijk': np.zeros((0, 3), np.int64),
               's0': z.copy(), 's1': z.copy(), 'alias': z.copy(), 'ring': np.zeros(0, bool), 'piece_ng': z.copy()}
    flat = np.asarray(sid).reshape(-1)
    pos['live'] = (pos['lin'] >= 0) & (flat[np.maximum(pos['lin'], 0)] == 3)
    return pos, piece_pos


def _continuity(s_um, d_um, D, s_min_um):
    """같은 조각 두 자리 (선분 쌍 · 면의 두 위치) 가 같은 가닥의 연속인가 — 바닥 (`_self_floor`) 밖이거나 s < s_min (등록 문턱 · 없으면
    바닥만).  아니면 접촉 (자기 접합 쌍 · 면 = 접합 자리 절단 또는 미등록)."""
    fl = np.asarray(_self_floor(s_um, d_um, D), bool)
    if s_min_um is None:
        return ~fl
    return ~fl | ~np.asarray(_self_is_junction(s_um, s_min_um), bool)


def _pos_arc_ranges(p, pos, segs, lo, vox):
    """위치 p 의 셀 조각 (그 셀 닫힌 상자로 자른 중심선) → (조각 끝점 X0 · X1, 호 구간 [lo, hi] 목록) · 고리 이음매 별칭이면 짝 위치의 조각도."""
    plist = [int(p)]
    a = int(pos['alias'][p])
    if a >= 0:
        plist.append(a)
    else:
        tgt = np.flatnonzero(pos['alias'] == int(p))
        plist += [int(t) for t in tgt]
    X0, X1, a0, a1 = _pos_portions(plist, pos, segs, lo, vox)
    return X0, X1, np.minimum(a0, a1), np.maximum(a0, a1)


def _arc_gap(rp, rq, L):
    """두 호 구간 묶음 (lo, hi 배열) 사이 최소 호 간격 — 고리 (L > 0) = 둘레 짧은 쪽."""
    lo_p, hi_p = rp
    lo_q, hi_q = rq
    if len(lo_p) == 0 or len(lo_q) == 0:
        return math.inf
    g = np.maximum(0.0, np.maximum(lo_p[:, None], lo_q[None, :]) - np.minimum(hi_p[:, None], hi_q[None, :]))
    if L > 0.0:
        span = np.maximum(hi_p[:, None], hi_q[None, :]) - np.minimum(lo_p[:, None], lo_q[None, :])
        g = np.minimum(g, np.maximum(0.0, L - span))
    return float(g.min())


def _pos_pair_sd(p, q, pos, segs, lo, vox):
    """같은 조각 두 위치의 (호 간격 s · 중심선 최소 거리 d) — 면 · 재방문 · SV 무리의 연속 판정 (`_continuity`) 입력."""
    Xp0, Xp1, lp, hp = _pos_arc_ranges(p, pos, segs, lo, vox)
    Xq0, Xq1, lq, hq = _pos_arc_ranges(q, pos, segs, lo, vox)
    L = float(segs['ring_L'][pos['s0'][p]]) if len(segs['ring_L']) else 0.0
    s = _arc_gap((lp, hp), (lq, hq), L)
    if len(Xp0) == 0 or len(Xq0) == 0:
        return s, math.inf
    ia = np.repeat(np.arange(len(Xp0)), len(Xq0))
    ib = np.tile(np.arange(len(Xq0)), len(Xp0))
    d, _, _, _, _ = seg_seg_closest(Xp0[ia], Xp1[ia], Xq0[ib], Xq1[ib])
    return s, float(d.min())


def _self_pairs(segs, D, s_min):
    """★ 10-21 (사전 리뷰 PRE-impl-02 · 1저자 Q-B · `CJUNC_SELF_RULE`) — 자기 접합 탐지 = 서로 다른 섬유와 같은 중심선 근접: 같은 조각 선분 쌍
    (i < j) 중 최근접 d ≤ D · 쌍마다 s = 최근접점 사이 조각 호 길이 (고리 = 짧은 쪽) · 바닥 (`_self_floor`) 을 넘는 쌍만 (후보 쌍) ·
    접합 쌍 = 후보 쌍 중 s ≥ s_min (s_min 없음 = 후보 쌍 전부 · 시험 모드 · S0 census).  셀 인접 (면 · 같은 셀) 은 쓰지 않는다 (옛: 셀
    인접 = 후보 · 중심선 거리 검사 없음 → 닿지 않는 다리에도 접합 · 닿는 모서리 인접 다리엔 접합 없음).  → dict(i, j, d, s, C1, C2, junc)."""
    P0, P1 = segs['P0'], segs['P1']
    ns = len(P0)
    empty = {'i': np.zeros(0, np.int64), 'j': np.zeros(0, np.int64), 'd': np.zeros(0), 's': np.zeros(0),
             'C1': np.zeros((0, 3)), 'C2': np.zeros((0, 3)), 'junc': np.zeros(0, bool)}
    if ns < 2:
        return empty
    from scipy.spatial import cKDTree
    mid = 0.5 * (P0 + P1)
    half = 0.5 * np.linalg.norm(P1 - P0, axis=1)
    rad = 2.0 * float(half.max()) + D
    pr = cKDTree(mid).query_pairs(rad, output_type='ndarray')
    if len(pr) == 0:
        return empty
    i, j = pr[:, 0], pr[:, 1]
    keep = segs['piece'][i] == segs['piece'][j]
    i, j = i[keep], j[keep]
    if len(i) == 0:
        return empty
    sw = i > j
    i, j = np.where(sw, j, i), np.where(sw, i, j)
    o = np.lexsort((j, i))
    i, j = i[o], j[o]
    d, sp_, tp_, C1, C2 = seg_seg_closest(P0[i], P1[i], P0[j], P1[j])
    close = d <= D
    i, j, d, sp_, tp_, C1, C2 = i[close], j[close], d[close], sp_[close], tp_[close], C1[close], C2[close]
    if len(i) == 0:
        return empty
    ai = segs['arc_a'][i] + sp_ * (segs['arc_b'][i] - segs['arc_a'][i])
    aj = segs['arc_a'][j] + tp_ * (segs['arc_b'][j] - segs['arc_a'][j])
    s = np.abs(aj - ai)
    L = segs['ring_L'][i]
    s = np.where(L > 0.0, np.minimum(s, L - s), s)
    fl = np.asarray(_self_floor(s, d, D), bool).reshape(len(s))
    if s_min is None:
        jn = np.ones(len(s), bool)
    else:
        jn = np.asarray(_self_is_junction(s, s_min), bool).reshape(len(s))
    m = fl
    return {'i': i[m], 'j': j[m], 'd': d[m], 's': s[m], 'C1': C1[m], 'C2': C2[m], 'junc': (fl & jn)[m]}


def _pair_groups(pi, pj, segs, sel):
    """같은 조각 쌍 무리 (union-find) — 이웃 선분 (k ± 1 · 고리 조각 = 둘레) 끼리 이어진 쌍 = 한 무리 (서로 다른 섬유 J2c 와 같은 꼴).
    sel = 쓸 쌍 마스크.  → 무리마다 쌍 번호 배열 (정준 순 = 무리 안 최소 (i, j))."""
    idx = np.flatnonzero(sel)
    if len(idx) == 0:
        return []
    piece, kk = segs['piece'], segs['k']
    nseg = np.bincount(piece, minlength=int(piece.max()) + 1 if len(piece) else 0)
    ring = segs['ring_L'] > 0.0
    keyof = {}
    for x in idx:
        keyof[(int(piece[pi[x]]), int(kk[pi[x]]), int(kk[pj[x]]))] = x
    uf = _UF()
    for x in idx:
        p_, ka, kb = int(piece[pi[x]]), int(kk[pi[x]]), int(kk[pj[x]])
        rg = bool(ring[pi[x]])
        n_ = int(nseg[p_])
        uf.find(x)
        for da in (-1, 0, 1):
            for db in (-1, 0, 1):
                a_, b_ = ka + da, kb + db
                if rg:
                    a_, b_ = a_ % n_, b_ % n_
                y = keyof.get((p_, a_, b_))
                if y is None:
                    y = keyof.get((p_, b_, a_))
                if y is not None:
                    uf.union(x, y)
    groups = {}
    for x in idx:
        groups.setdefault(uf.find(x), []).append(x)
    out = [np.asarray(sorted(m), np.int64) for m in groups.values()]
    out.sort(key=lambda m: (int(pi[m].min()), int(pj[m].min())))
    return out


def _group_cp(mem, sp):
    """쌍 무리의 접점 (`CJUNC_CP_RULE` — 서로 다른 섬유와 같은 규칙): 거리² ε 띠 안 · 중점 사전식 최소 · 그래도 같으면 (i, j)."""
    dm2 = sp['d'][mem] * sp['d'][mem]
    bnd = mem[dm2 <= float(dm2.min()) + CJUNC_EPS_D2_UM2]
    mid = 0.5 * (sp['C1'][bnd] + sp['C2'][bnd])
    return int(bnd[np.lexsort((sp['j'][bnd], sp['i'][bnd], mid[:, 2], mid[:, 1], mid[:, 0]))[0]])


def _touch_len_pairs(pi, pj, segs, T):
    """자기 접합 L_c (`CJUNC_SELF_LC_RULE`) — `_touch_len_all` 과 같은 닿음 규칙 · 짝 = 그 instance 의 접합 쌍만 (바닥 · s 규칙을 지난 쌍 ·
    같은 가닥의 연속 짝은 닿아도 넣지 않는다) · 쪽마다 선분별 구간 합집합 (안쪽 경계) 길이의 합 · 두 쪽의 최댓값."""
    best = 0.0
    for S, Q in ((pi, pj), (pj, pi)):
        su = np.unique(S); qu = np.unique(Q)
        si = np.searchsorted(su, S); qi = np.searchsorted(qu, Q)
        tot = _touch_runs_on(segs['P0'][su], segs['P1'][su], segs['P0'][qu], segs['P1'][qu], si, qi, T)[3]
        best = max(best, tot)
    return best


def _self_instances(sp, segs, T):
    """자기 접합 instance — 접합 쌍 무리마다 하나 (★ 10-21 Q-B).  접점 = `_group_cp` · d0 = 무리 최소 거리 · s = 접점 쌍의 s · L_c =
    `_touch_len_pairs` · 두 쪽 선분 = 무리의 i · j 선분 (발자국 · 분산판 · 포트 후보) · 쌍 목록 (분산판 짝 제한).  순서 = (조각, 접점)."""
    groups = _pair_groups(sp['i'], sp['j'], segs, sp['junc'])
    out = {k: [] for k in ('fi', 'fj', 'd0', 'Lc', 's', 'Ci', 'Cj', 'seg_i', 'seg_j', 'piece_i', 'piece_j', 'si_min', 'sj_min',
                           'pair_i', 'pair_j')}
    for mem in groups:
        b = _group_cp(mem, sp)
        pi_ = sp['i'][mem]; pj_ = sp['j'][mem]
        f = int(segs['fid'][sp['i'][b]]); p_ = int(segs['piece'][sp['i'][b]])
        out['fi'].append(f); out['fj'].append(f); out['piece_i'].append(p_); out['piece_j'].append(p_)
        out['d0'].append(float(np.min(sp['d'][mem]))); out['s'].append(float(sp['s'][b]))
        out['Ci'].append(sp['C1'][b].copy()); out['Cj'].append(sp['C2'][b].copy())
        out['seg_i'].append(np.unique(pi_)); out['seg_j'].append(np.unique(pj_))
        out['pair_i'].append(pi_.copy()); out['pair_j'].append(pj_.copy())
        out['si_min'].append(int(sp['i'][b])); out['sj_min'].append(int(sp['j'][b]))
        out['Lc'].append(_touch_len_pairs(pi_, pj_, segs, T))
    nq = len(out['fi'])
    if nq:
        C = np.asarray(out['Ci'], np.float64).reshape(-1, 3)
        o = np.lexsort((C[:, 2], C[:, 1], C[:, 0], np.asarray(out['piece_i'])))
    else:
        o = np.zeros(0, np.int64)
    res = {'fi': np.asarray(out['fi'], np.int64)[o], 'fj': np.asarray(out['fj'], np.int64)[o],
           'self': np.ones(nq, bool), 'd0': np.asarray(out['d0'], np.float64)[o], 'Lc': np.asarray(out['Lc'], np.float64)[o],
           's': np.asarray(out['s'], np.float64)[o], 'Ci': np.asarray(out['Ci'], np.float64).reshape(-1, 3)[o],
           'Cj': np.asarray(out['Cj'], np.float64).reshape(-1, 3)[o],
           'piece_i': np.asarray(out['piece_i'], np.int64)[o], 'piece_j': np.asarray(out['piece_j'], np.int64)[o],
           'si_min': np.asarray(out['si_min'], np.int64)[o], 'sj_min': np.asarray(out['sj_min'], np.int64)[o]}
    for k in ('seg_i', 'seg_j', 'pair_i', 'pair_j'):
        res[k] = [out[k][x] for x in o]
    return res


def _merge_instances(inst, selfinst):
    """distinct + self instance 표 (distinct 먼저 · 자기 instance 번호 = distinct 수 + 자기 번호).  자기 접합의 접점 (Ci · Cj) = 그 무리
    접점 쌍 (옛 칸 self_xa · self_xb = 같은 값 · 분산판 k 1 이 읽는다) · 두 쪽 위치 · 재방문 · 면 수는 호출자가 채운다."""
    nI = len(inst['fi']); nS = len(selfinst['fi'])
    out = {'fi': np.r_[inst['fi'], selfinst['fi']].astype(np.int64), 'fj': np.r_[inst['fj'], selfinst['fj']].astype(np.int64),
           'self': np.r_[np.zeros(nI, bool), np.ones(nS, bool)],
           'd0': np.r_[inst['d0'], selfinst['d0']].astype(np.float64),
           'Lc': np.r_[inst['Lc'], selfinst['Lc']].astype(np.float64),
           's': np.r_[np.full(nI, np.nan), selfinst['s']].astype(np.float64),          # 자기 접합 경로 호 길이 (distinct = NaN)
           'Ci': np.r_[inst['Ci'], selfinst['Ci']].reshape(-1, 3), 'Cj': np.r_[inst['Cj'], selfinst['Cj']].reshape(-1, 3),
           'piece_i': np.r_[inst['piece_i'], selfinst['piece_i']].astype(np.int64),
           'piece_j': np.r_[inst['piece_j'], selfinst['piece_j']].astype(np.int64),
           'si_min': np.r_[inst['si_min'], selfinst['si_min']].astype(np.int64),
           'sj_min': np.r_[inst['sj_min'], selfinst['sj_min']].astype(np.int64)}
    out['self_xa'] = np.r_[np.full((nI, 3), np.nan), selfinst['Ci']].reshape(-1, 3)
    out['self_xb'] = np.r_[np.full((nI, 3), np.nan), selfinst['Cj']].reshape(-1, 3)
    out['seg_i'] = list(inst['seg_i']) + list(selfinst['seg_i'])
    out['seg_j'] = list(inst['seg_j']) + list(selfinst['seg_j'])
    out['pair_i'] = [np.zeros(0, np.int64)] * nI + list(selfinst['pair_i'])
    out['pair_j'] = [np.zeros(0, np.int64)] * nI + list(selfinst['pair_j'])
    return out


def _piece_cand(piece, pos, piece_pos):
    """조각의 포트 후보 = 그 조각의 위치 **전부** (★ 10-21 사전 리뷰 PRE-impl-03 · 1저자 Q-C — 덮인 위치도 · 고른 뒤 `_port_take` 가 살았는지
    본다 · 옛: 살아있는 위치만 → 접점 셀이 덮이면 r_port 안 이웃 셀로 옮겨 붙었다)."""
    a0, a1 = piece_pos[piece]
    return np.arange(a0, a1)


def _side_cand(S, piece, pos, piece_pos):
    """자기 접합 한 쪽의 포트 후보 = 그 조각의 위치 중 선분 범위 [s0, s1] 가 그 쪽 선분 (접합 쌍의 그 쪽) 과 겹치는 것 (살았든 덮였든 —
    다른 쪽 가닥의 셀을 고르지 않는다)."""
    a0, a1 = piece_pos[piece]
    c = np.arange(a0, a1)
    S = np.asarray(S, np.int64)
    if len(c) == 0 or len(S) == 0:
        return c[:0]
    lo_ = np.searchsorted(S, pos['s0'][c], 'left')
    hi_ = np.searchsorted(S, pos['s1'][c], 'right')
    return c[hi_ > lo_]


def _port_take(C, cand, pos, segs, lo, vox, flat, r_port):
    """★ 10-21 (사전 리뷰 PRE-impl-03 · 1저자 Q-C · `CJUNC_PORT_RULE`) — 포트 = 후보 위치 (살았든 덮였든) 중 `_port_pick` 규칙 하나 · 고른
    위치가 덮였으면 (다른 상 · 상자 밖) **옮기지 않고** 미실현 (사유 covered_<상> · out_of_box) — 덮은 상의 법칙만 남는다 (SDCP = SV
    융합 · S3 c · PTFE face_alpha = P0/P1 · 같은 접촉을 두 번 세지 않는다).  r_port 안 후보 없음 = no_port_in_rport.
    → (위치 | −1, 동률, 셀 중심 거리, 사유)."""
    p, tie, dist = _port_pick(C, cand, pos, segs, lo, vox, r_port)
    if p < 0:
        return -1, False, math.inf, 'no_port_in_rport'
    if not pos['live'][p]:
        lin = int(pos['lin'][p])
        why = 'out_of_box' if lin < 0 else f'covered_{_SID_NAME.get(int(flat[lin]), str(int(flat[lin])))}'
        return -1, bool(tie), float(dist), why
    return int(p), bool(tie), float(dist), ''


def _ports(allinst, pos, piece_pos, segs, lo, vox, n, flat, r_port):
    """J3 · J4 — instance 접점 → 포트 (`_port_take` · 방향 무관 기하 정준 규칙 · 10-21 RCA-04 · ★ Q-C 옮김 없음).  서로 다른 섬유 = 그 조각의
    위치 중 r_port 안 · 자기 접합 = 그 쪽 위치 (`_side_cand`) 중 r_port 안 — 같은 규칙 (fid 무관).  자기 접합 k 차 (self_dk_min) = 두 포트
    위치 번호 차 (고리 = 둘레 짧은 쪽 · 미실현 = −1)."""
    nI = len(allinst['fi'])
    port_i = np.full(nI, -1, np.int64); port_j = np.full(nI, -1, np.int64)
    reason = np.array([''] * nI, dtype=object)
    tie_i = np.zeros(nI, bool); tie_j = np.zeros(nI, bool)
    disp = np.zeros(nI, bool); sdist = np.full(nI, np.nan)
    cp = np.zeros((nI, 3))
    dk = np.full(nI, -1, np.int64)
    side_A, side_B = [], []
    for k in range(nI):
        Ci, Cj = allinst['Ci'][k], allinst['Cj'][k]
        cp[k] = 0.5 * (Ci + Cj)
        if allinst['self'][k]:
            ci = _side_cand(allinst['seg_i'][k], int(allinst['piece_i'][k]), pos, piece_pos)
            cj = _side_cand(allinst['seg_j'][k], int(allinst['piece_j'][k]), pos, piece_pos)
        else:
            ci = _piece_cand(int(allinst['piece_i'][k]), pos, piece_pos)
            cj = _piece_cand(int(allinst['piece_j'][k]), pos, piece_pos)
        side_A.append(np.asarray(ci, np.int64)); side_B.append(np.asarray(cj, np.int64))
        pi_, ti, di, wi = _port_take(Ci, ci, pos, segs, lo, vox, flat, r_port)
        pj_, tj, dj, wj = _port_take(Cj, cj, pos, segs, lo, vox, flat, r_port)
        port_i[k], port_j[k] = pi_, pj_
        tie_i[k], tie_j[k] = ti, tj
        if pi_ < 0 or pj_ < 0:
            reason[k] = wi or wj
            continue
        sdist[k] = max(di, dj)
        ni = np.floor((Ci - lo) / vox).astype(np.int64); nj = np.floor((Cj - lo) / vox).astype(np.int64)
        disp[k] = bool(np.any(pos['ijk'][pi_] != ni) or np.any(pos['ijk'][pj_] != nj))
        if allinst['self'][k]:
            d_ = abs(int(pos['k'][pj_]) - int(pos['k'][pi_]))
            if pos['ring'][pi_]:
                d_ = min(d_, int(pos['piece_ng'][pi_]) - d_)
            dk[k] = d_
    return {'port_i': port_i, 'port_j': port_j, 'realized': (port_i >= 0) & (port_j >= 0), 'reason': reason,
            'tie_i': tie_i, 'tie_j': tie_j, 'port_displaced': disp, 'port_search_um': sdist, 'cp': cp,
            'long': np.zeros(nI, bool), 'self_dk_min': dk, 'self_A': side_A, 'self_B': side_B}


def _touch_runs(S0, S1, Q0, Q1, T):
    """선분 열 S (순서 = 정준 경로 순서) 의 선분마다 선분 집합 Q 까지 중심선 거리 ≤ T 인 구간 합집합 (안쪽 경계) → (선분 번호 · ua · ub ·
    길이 합).  `_touch_len_all` · `_touch_len_pairs` 의 한 쪽과 같은 원시 (`_touch_intervals`) · 같은 합집합 · 같은 합산 순서 — 그 길이 =
    L_c 의 그 쪽 값 (비트).  짝 = S × Q 전부 (서로 다른 섬유)."""
    ns, nq = len(S0), len(Q0)
    if ns == 0 or nq == 0:
        z = np.zeros(0)
        return np.zeros(0, np.int64), z, z.copy(), 0.0
    return _touch_runs_on(S0, S1, Q0, Q1, np.repeat(np.arange(ns), nq), np.tile(np.arange(nq), ns), T)


def _touch_runs_on(S0, S1, Q0, Q1, si, qi, T):
    """`_touch_runs` 의 몸체 — 짝 (si, qi) 를 준다 (★ 10-21 Q-B 자기 접합 = 그 instance 의 접합 쌍만 · 서로 다른 섬유 = S × Q 전부)."""
    z = np.zeros(0)
    si = np.asarray(si, np.int64); qi = np.asarray(qi, np.int64)
    if len(si) == 0:
        return np.zeros(0, np.int64), z, z.copy(), 0.0
    _, us, _, _, _ = seg_seg_closest(S0[si], S1[si], Q0[qi], Q1[qi])
    ua, ub = _touch_intervals(S0[si], S1[si], Q0[qi], Q1[qi], T, us)
    ok = np.isfinite(ua)
    if not ok.any():
        return np.zeros(0, np.int64), z, z.copy(), 0.0
    si, ua, ub = si[ok], ua[ok], ub[ok]
    o = np.lexsort((ua, si))
    si, ua, ub = si[o], ua[o], ub[o]
    seglen = np.linalg.norm(S1 - S0, axis=1)
    rs, ra, rb = [], [], []
    tot = 0.0
    start, n = 0, len(si)
    while start < n:                                         # 선분마다 구간 합집합 (`_touch_len_sets` 와 같은 고리)
        end = start
        while end < n and si[end] == si[start]:
            end += 1
        cur_a, cur_b = ua[start], ub[start]
        acc = 0.0
        for x in range(start + 1, end):
            if ua[x] <= cur_b:
                cur_b = max(cur_b, ub[x])
            else:
                acc += cur_b - cur_a
                rs.append(si[start]); ra.append(cur_a); rb.append(cur_b)
                cur_a, cur_b = ua[x], ub[x]
        acc += cur_b - cur_a
        rs.append(si[start]); ra.append(cur_a); rb.append(cur_b)
        tot += acc * seglen[si[start]]
        start = end
    return np.asarray(rs, np.int64), np.asarray(ra, np.float64), np.asarray(rb, np.float64), float(tot)


def _divide_runs(rs, ra, rb, S0, S1, k):
    """닿음 구간 (정준 경로 순서) 을 길이로 k 등분한 칸의 가운데 점 k 개 — 칸 j 의 점 = 누적 길이 (j + ½)·L/k (L = 구간 길이 합)."""
    return _divide_runs_idx(rs, ra, rb, S0, S1, k)[0]


def _divide_runs_idx(rs, ra, rb, S0, S1, k):
    """`_divide_runs` + 점마다 그 점이 놓인 선분 번호 (S 안 번호 · 자기 접합 분산판의 짝 제한)."""
    seglen = np.linalg.norm(S1 - S0, axis=1)
    lens = (rb - ra) * seglen[rs]
    cum = np.r_[0.0, np.cumsum(lens)]
    L = float(cum[-1])
    out = np.zeros((k, 3))
    sidx = np.zeros(k, np.int64)
    for j in range(k):
        t = (j + 0.5) * L / k
        m = min(max(int(np.searchsorted(cum, t, side='right')) - 1, 0), len(lens) - 1)
        while m < len(lens) - 1 and lens[m] <= 0.0:          # 길이 0 구간 (접선 한 점) 은 건너뛴다
            m += 1
        f = 0.0 if lens[m] <= 0.0 else min(max((t - cum[m]) / lens[m], 0.0), 1.0)
        u = ra[m] + f * (rb[m] - ra[m])
        s = rs[m]
        out[j] = S0[s] + u * (S1[s] - S0[s])
        sidx[j] = int(s)
    return out, sidx


def _n_sub(Lc, L_par):
    """간선 수 k = ceil(L_c/L_par) — L_c ≤ L_par·(1 + `CJUNC_LPAR_RTOL`) = 1 (점 접합 · 긴 접촉 표지와 같은 문턱) · 정수 경계도 같은 1e-9 띠
    (L_c/L_par = 2 + 몇 ulp 가 3 이 되지 않게).
    ⚠ 10-21 (사전 리뷰 PRE-impl-05 · 한계 기록 · 고치지 않음): k 는 계단이라 L_c/L_par 가 정수 경계를 넘으면 (깊은 교차 90° → 89.99° ·
      배율 차 1.5e-8) 간선 자리가 바뀌어 σ 가 뛴다 — 반쪽 간선이 셀 경계 (±L_c/4 = ±h/2) 로 가 사전식 최소 셀로 옮겨진다 · 크기 ∝ h·r′/R_j
      (생산 단위 R_j 1e2 · 1e4 · 1e6 Ω 에서 −0.98 % · −2.1e-4 · −2.1e-6 — 시험 KBND 가 묶는다).  분산판 v0 = 계단 근사 (이산화 오차) ·
      origin · 순서 대조에서 이 뜀이 잡음으로 섞일 수 있다 (한정어) · 경계 연속 배치는 v1 후보."""
    r = float(Lc) / float(L_par)
    if not (r > 1.0 + CJUNC_LPAR_RTOL):
        return 1
    return max(2, int(math.ceil(r - CJUNC_LPAR_RTOL)))


def _subedges(allinst, pos, piece_pos, segs, lo, vox, n, flat, thr, T):
    """분산판 v0 (`CJUNC_DIST_RULE`) — instance 마다 k 간선.  k = 1 = instance 그대로 (포트 · 접점 · 사유 · 동률 = 옛 점 접합 · 비트 같음).
    k > 1 = 정의 쪽 (닿음 길이가 긴 가닥 · 1e-9 상대 안 동률 = i 쪽) 의 닿음 구간을 k 등분한 칸 가운데 점 X · 맞은편 최근접점 Y (ε 띠 ·
    사전식) · 포트 = `_port_take` (서로 다른 섬유 = 그 조각 / 자기 접합 = 그 쪽 위치 · 둘 다 r_port 안 · 덮였으면 미실현) · 간선 접점 =
    (X_i + X_j)/2.  ★ 10-21 (Q-B) 자기 접합 = 닿음 · 맞은편 = 그 instance 의 접합 쌍만 (같은 가닥의 연속 짝은 쓰지 않는다).
    PTFE 덮임 · SDCP 근접은 호출자가 간선 접점에서 잰다.  → (간선 표 dict, instance 마다 k)."""
    nI = len(allinst['fi'])
    L_par, r_port = thr['L_par_um'], thr['r_port_um']
    rec = {k_: [] for k_ in ('inst', 'j', 'k', 'side', 'port_i', 'port_j', 'cp', 'X_i', 'X_j', 'realized', 'reason', 'tie_i',
                              'tie_j', 'port_search_um')}
    nsub = np.ones(nI, np.int64)

    def add(q, j, kq, side, pi_, pj_, xi, xj, cp_, ok, why, ti, tj, sd):
        for k_, v_ in (('inst', q), ('j', j), ('k', kq), ('side', side), ('port_i', pi_), ('port_j', pj_), ('cp', cp_),
                       ('X_i', xi), ('X_j', xj), ('realized', ok), ('reason', why), ('tie_i', ti), ('tie_j', tj),
                       ('port_search_um', sd)):
            rec[k_].append(v_)
    for q in range(nI):
        kq = _n_sub(allinst['Lc'][q], L_par)
        nsub[q] = kq
        isself = bool(allinst['self'][q])
        if kq == 1:                                          # 점 접합 — instance 그대로 (옛 점 접합과 비트 같음)
            add(q, 0, 1, -1, int(allinst['port_i'][q]), int(allinst['port_j'][q]), np.asarray(allinst['Ci'][q], np.float64).copy(),
                np.asarray(allinst['Cj'][q], np.float64).copy(), allinst['cp'][q].copy(), bool(allinst['realized'][q]),
                str(allinst['reason'][q]), bool(allinst['tie_i'][q]), bool(allinst['tie_j'][q]),
                float(allinst['port_search_um'][q]))
            continue
        Si, Sj = np.asarray(allinst['seg_i'][q], np.int64), np.asarray(allinst['seg_j'][q], np.int64)
        I0, I1 = segs['P0'][Si], segs['P1'][Si]
        J0, J1 = segs['P0'][Sj], segs['P1'][Sj]
        if isself:
            pa = np.searchsorted(Si, np.asarray(allinst['pair_i'][q], np.int64))
            pb = np.searchsorted(Sj, np.asarray(allinst['pair_j'][q], np.int64))
            rI = _touch_runs_on(I0, I1, J0, J1, pa, pb, T)
            rJ = _touch_runs_on(J0, J1, I0, I1, pb, pa, T)
        else:
            rI = _touch_runs(I0, I1, J0, J1, T)
            rJ = _touch_runs(J0, J1, I0, I1, T)
        ci = np.asarray(allinst['self_A'][q], np.int64)
        cj_ = np.asarray(allinst['self_B'][q], np.int64)
        side = 1 if rJ[3] > rI[3] * (1.0 + CJUNC_LPAR_RTOL) else 0
        if side == 0:
            Xd, Xs = _divide_runs_idx(rI[0], rI[1], rI[2], I0, I1, kq)
        else:
            Xd, Xs = _divide_runs_idx(rJ[0], rJ[1], rJ[2], J0, J1, kq)
        for j in range(kq):
            if side == 0:
                xi = Xd[j]
                if isself:
                    m_ = pb[pa == Xs[j]]
                    xj = _nearest_on(xi, J0[m_], J1[m_])
                else:
                    xj = _nearest_on(xi, J0, J1)
            else:
                xj = Xd[j]
                if isself:
                    m_ = pa[pb == Xs[j]]
                    xi = _nearest_on(xj, I0[m_], I1[m_])
                else:
                    xi = _nearest_on(xj, I0, I1)
            pi_, ti, di, wi = _port_take(xi, ci, pos, segs, lo, vox, flat, r_port)
            pj_, tj, dj, wj = _port_take(xj, cj_, pos, segs, lo, vox, flat, r_port)
            ok = pi_ >= 0 and pj_ >= 0
            why = '' if ok else (wi or wj)
            add(q, j, kq, side, pi_, pj_, xi.copy(), xj.copy(), 0.5 * (xi + xj), ok, why, ti, tj,
                (max(di, dj) if ok else np.nan))
    nS = len(rec['inst'])
    reason = np.empty(nS, dtype=object)
    for x, w in enumerate(rec['reason']):
        reason[x] = w
    sub = {'inst': np.asarray(rec['inst'], np.int64), 'j': np.asarray(rec['j'], np.int64), 'k': np.asarray(rec['k'], np.int64),
           'side': np.asarray(rec['side'], np.int64), 'port_i': np.asarray(rec['port_i'], np.int64),
           'port_j': np.asarray(rec['port_j'], np.int64), 'cp': np.asarray(rec['cp'], np.float64).reshape(-1, 3),
           'X_i': np.asarray(rec['X_i'], np.float64).reshape(-1, 3), 'X_j': np.asarray(rec['X_j'], np.float64).reshape(-1, 3),
           'realized': np.asarray(rec['realized'], bool).reshape(nS), 'reason': reason,
           'tie_i': np.asarray(rec['tie_i'], bool).reshape(nS), 'tie_j': np.asarray(rec['tie_j'], bool).reshape(nS),
           'port_search_um': np.asarray(rec['port_search_um'], np.float64).reshape(nS),
           'a_sdcp': np.zeros(nS, bool), 'ptfe_cov': np.zeros(nS, bool)}
    return sub, nsub
