# ═════════════════════════ RCA2 — 사전 리뷰 (구현 · 10-21) PRE-impl-01–06 · 09 · 1저자 Q-A–Q-D 권고대로 ═════════════════════════
#  반례 = 사전 리뷰 (impl) 탐침 (probe_gap_revisit · _prod · probe_closed_loop · probe_self_vs_distinct · probe_ptfe_monotone ·
#  probe_sdcp_relocate · probe_sv_cf · probe_k_boundary_prod · probe_mut_cf) 을 우리 시험으로 — 기대 = 손 회로 · 독립 셀 열.

def rows_pieces(pieces, fid=10, phase=2, kind=1):
    """한 fid 의 점열 조각들 (점 배열 그대로 · 순서대로 붙임) → (P, PH, F, K) — 끊긴 섬유 (조각 사이 틈 > gap_tol × 중앙 간격) 를 만든다."""
    P = np.vstack([np.asarray(p, np.float64).reshape(-1, 3) for p in pieces])
    n = len(P)
    return P, np.full(n, phase, np.int64), np.full(n, fid, np.int64), np.full(n, kind, np.int64)


def _cells_of_pts(pts, vox=H):
    """점열 → 셀 열 (연속 중복 제거) — 독립 도구 (생산 원시 함수 `segment_cells`)."""
    from fibre_segment_raster import segment_cells
    pts = np.asarray(pts, np.float64)
    cs = np.vstack([segment_cells(pts[i], pts[i + 1], vox) for i in range(len(pts) - 1)])
    keep = np.ones(len(cs), bool)
    keep[1:] = np.any(cs[1:] != cs[:-1], axis=1)
    return [tuple(int(v) for v in c) for c in cs[keep]]


def _graph_ref(cells_seq, n, extra=(), drop=(), g_ax=G_AX, g_pl=G_PL):
    """셀 열 손 회로 — 같은 셀 = 한 노드 (고리 이음매) · 연속 이웃 = 축 간선 g_ax · drop = 뺄 축 간선 (셀 쌍) · extra = (셀, 셀, g) ·
    판 = z 0 셀 (아래) · z n−1 셀 (위) 전부 g_pl (셀 중심이 판에서 h/2) → 아래 판 전류."""
    uniq = sorted(set(cells_seq))
    ix = {c: i for i, c in enumerate(uniq)}
    E = set()
    for a_, b_ in zip(cells_seq[:-1], cells_seq[1:]):
        if a_ != b_:
            E.add(tuple(sorted((ix[a_], ix[b_]))))
    for a_, b_ in drop:
        E.discard(tuple(sorted((ix[a_], ix[b_]))))
    edges = [(a_, b_, g_ax) for a_, b_ in sorted(E)] + [(ix[a_], ix[b_], g) for a_, b_, g in extra]
    bot = [(ix[c], g_pl) for c in uniq if c[2] == 0]
    top = [(ix[c], g_pl) for c in uniq if c[2] == n[2] - 1]
    return ref_I(len(uniq), edges, bot, top)


def _inst_rec(reg, q):
    """instance q 의 기록 — L_c · 배율 · k · 분산 간선 포트 셀 (정렬) · d0 (서로 다른 섬유 ↔ 같은 fid 대조 · fid 무관 보장)."""
    I = reg['instances']
    S = reg.get('subedges') or {}
    pos = reg['positions']
    cells = []
    for e in range(len(S.get('inst', []))):
        if int(S['inst'][e]) != q:
            continue
        a_, b_ = int(S['port_i'][e]), int(S['port_j'][e])
        cells.append((None if a_ < 0 else tuple(int(v) for v in pos['ijk'][a_]),
                      None if b_ < 0 else tuple(int(v) for v in pos['ijk'][b_])))
    return {'Lc': float(I['Lc'][q]), 'mult': float(I['mult'][q]), 'nsub': int(np.asarray(I.get('nsub', [-1] * (q + 1)))[q]),
            'cells': sorted(cells, key=str), 'd0': float(I['d0'][q])}


def _rec_same(a, b):
    return (a is not None and b is not None and abs(a['Lc'] - b['Lc']) <= 1e-12 * max(1.0, abs(b['Lc']))
            and abs(a['mult'] - b['mult']) <= 1e-12 * b['mult'] and a['nsub'] == b['nsub'] and a['cells'] == b['cells']
            and abs(a['d0'] - b['d0']) <= 1e-15)


GAP_N = (3, 3, 8)


@case('GAP')
def t_gap():
    """★ PRE-impl-01 (P1) · 1저자 Q-A — 같은 섬유의 끊긴 두 조각 (`fibre_pieces` 끊기 = 섬유 경로로 안 이어짐) = 서로 다른 섬유와 같은 규칙
    (중심선 거리 ≤ D → R_j 접합 · instance = 조각 쌍 · s 규칙 없음).  옛 판 (기반 a76f59d0d): 두 끝이 같은 셀 = 같은 fid 재방문 '경로로만'
    (경로가 없다 = 거짓 기록) → σ 0 (no_through_component) · 면 인접 = 옛 융합 (12.5 = 끊김 없는 섬유처럼).  기대 = 손 회로 (조각 사슬 +
    R_j 간선 하나) · s_min 무관 · census 칸 정정 · 생산 단위 (h 0.15 · r_f 0.075 · tol_ff 0.03 · 점 간격 0.05 · 틈 0.12 · 옛 판 = 0 ↔ 872.66)."""
    rj = 1e3
    for nm, ze, zs, ca, cb in (('같은 셀 (끝 z 3.15 · 3.85 · 셀 (1,1,3))', 3.15, 3.85, 3, 3),
                               ('면 인접 (끝 z 2.85 · 3.5 · 셀 (1,1,2)|(1,1,3))', 2.85, 3.5, 2, 3)):
        P = rows_pieces([densify([(1.5, 1.5, 0.5), (1.5, 1.5, ze)]), densify([(1.5, 1.5, zs), (1.5, 1.5, 7.5)])])
        sid, _ = bed(P, GAP_N)
        want = chain_I([G_PL] + [G_AX] * ca + [1e4 / rj] + [G_AX] * (7 - cb) + [G_PL])
        I_leg = I_of(solve_legacy(sid, sig_e(), GAP_N), GAP_N)
        okreg = oks = okinf = okc = True
        msg = []
        for smin in (S_MIN, 0.5):
            reg = _try(lambda smin=smin: registry(sid, P, s_min_um=smin), None)
            if reg is None:
                okreg = oks = okinf = okc = False
                continue
            I_, cen = reg['instances'], reg['census']
            okreg &= bool(cen.get('n_pieces') == 2 and len(I_['fi']) == 1 and not bool(I_['self'][0])
                          and int(I_['fi'][0]) == int(I_['fj'][0]) == 10 and int(I_['piece_i'][0]) != int(I_['piece_j'][0])
                          and bool(I_['realized'][0]) and (_pcells(reg, 0, 'i'), _pcells(reg, 0, 'j')) == ((1, 1, ca), (1, 1, cb)))
            r = _try(lambda reg=reg: solve(sid, sig_e(), GAP_N, plan(reg, rj)), None)
            I = I_of(r, GAP_N) if r is not None else math.nan
            oks &= rel(I, want) < 1e-12
            ri = _try(lambda reg=reg: solve(sid, sig_e(), GAP_N, plan(reg, math.inf, allow_rj_limits=True)), None)
            okinf &= bool(ri is not None and ri['sigma_eff'] == 0.0 and ri.get('reason') == 'no_through_component')
            okc &= bool(cen.get('n_instances_same_fid_pieces') == 1 and cen.get('n_self_revisits_path_only') == 0
                        and cen.get('n_revisit_pairs') == 0 and cen.get('n_piece_cell_meets') == (1 if ca == cb else 0))
            msg.append((smin, len(I_['fi']), I, None if ri is None else ri.get('reason'),
                        {k: cen.get(k) for k in ('n_pieces', 'n_instances_same_fid_pieces', 'n_self_revisits_path_only',
                                                 'n_revisit_pairs', 'n_piece_cell_meets')}))
        print(f'    GAP {nm}: 손 {want:.9g} · 옛 경로 (접합 끔) {I_leg:.9g} · {msg}')
        chk(f'GAP {nm} — 조각 2 · instance 1 (조각 쌍 · 같은 fid · 자기 아님 · 실현) · 포트 = (1,1,{ca}) · (1,1,{cb}) (s_min 3 · 0.5)', okreg,
            f'{msg}')
        chk(f'GAP {nm} — σ = 손 회로 (조각 사슬 + R_j 간선 하나 · 1e-12) · s_min 무관', oks, f'{msg}')
        chk(f'GAP {nm} — R_j = ∞ → 조각 사이 전류 0 (no_through_component · 조각은 접합으로만 이어진다)', okinf, f'{msg}')
        chk(f"GAP {nm} — census: 같은 fid 조각 쌍 instance 1 · 같은 셀 조각 만남 {1 if ca == cb else 0} · 같은 조각 재방문 0 · "
            f"'경로로만' 0 (옛 = 거짓 1)", okc, f'{msg}')
    VP, NPd, sv = 0.15, (3, 3, 8), 7853.98
    gax, gpl = sv * VP, sv * VP * VP / (0.5 * VP)
    sig = sig_e(s_vgcf=sv, s_am=0.0041)
    for nm, ze, zs, ca, cb in (('같은 셀 (끝 z 0.47 · 0.59)', 0.47, 0.59, 3, 3), ('면 인접 (끝 z 0.40 · 0.52)', 0.40, 0.52, 2, 3)):
        P = rows_pieces([densify([(0.225, 0.225, 0.075), (0.225, 0.225, ze)], 0.05),
                         densify([(0.225, 0.225, zs), (0.225, 0.225, 1.125)], 0.05)])
        sid, _ = bed(P, NPd, vox=VP)
        reg = _try(lambda: registry(sid, P, vox=VP, r_f_um=0.075, tol_ff_um=0.03, L_par_um=0.30, r_port_um=0.30, s_min_um=0.3), None)
        r = _try(lambda: solve(sid, sig, NPd, plan(reg, 1e6), vox=VP), None) if reg is not None else None
        want = chain_I([gpl] + [gax] * ca + [1e4 / 1e6] + [gax] * (7 - cb) + [gpl])
        I = I_of(r, NPd, vox=VP) if r is not None else math.nan
        rl = solve_legacy(sid, sig, NPd, vox=VP)
        print(f"    GAP 생산 단위 {nm}: σ {None if r is None else r['sigma_eff']} S/cm · 옛 경로 (접합 끔) {rl['sigma_eff']} · 손 I {want:.9g}")
        chk(f'GAP 생산 단위 {nm} (h 0.15 · r_f 0.075 · tol_ff 0.03 · 틈 0.12 · s_min 0.3 · R_j 1e6) — instance 1 (조각 쌍) · '
            f'σ = 손 회로 (1e-12)',
            reg is not None and len(reg['instances']['fi']) == 1 and not bool(reg['instances']['self'][0]) and rel(I, want) < 1e-12,
            f'{I} ↔ {want}')


RING_N = (5, 3, 8)
RING = [(1.5, 1.5, 4.2), (1.5, 1.5, 7.5), (3.5, 1.5, 7.5), (3.5, 1.5, 0.5), (1.5, 1.5, 0.5), (1.5, 1.5, 4.2)]


@case('RING')
def t_ring():
    """★ PRE-impl-06 · 1저자 Q-A — 닫힌 경로 (첫 점 = 끝 점 · 좌표 비트 같음) 의 이음매 = 연속 (접합도 끊김도 아님).  옛 판: 이음매 셀의 첫 ·
    끝 위치 = 같은 fid 재방문 (s = 고리 길이 18) → s ≥ s_min 이면 R_j 접합 (18.47 · −28 %) · s < s_min 이면 경로로만 (끊김 · 12.93 · −50 %).
    기대 = 손 연속 고리 회로 (= 옛 경로 25.641) · s_min 무관.  틈 하나 있는 고리 = 이음매를 지나 한 조각 (열린 가닥) + 틈 두 끝 사이 자기 접합
    (중심선 1.0 · s 17 · 손 회로 = 고리에서 틈 축 간선 하나를 R_j 간선으로)."""
    rj = 1e3
    pts = densify(RING)
    cells = _cells_of_pts(pts)
    want = _graph_ref(cells, RING_N)
    P = rows([RING])
    sid, _ = bed(P, RING_N)
    I_leg = I_of(solve_legacy(sid, sig_e(), RING_N), RING_N)
    for smin in (S_MIN, 100.0):
        reg = _try(lambda smin=smin: registry(sid, P, s_min_um=smin), None)
        r1 = _try(lambda reg=reg: solve(sid, sig_e(), RING_N, plan(reg, rj)), None) if reg is not None else None
        ri = _try(lambda reg=reg: solve(sid, sig_e(), RING_N, plan(reg, math.inf, allow_rj_limits=True)), None) if reg is not None else None
        I1 = I_of(r1, RING_N) if r1 is not None else math.nan
        Ii = I_of(ri, RING_N) if ri is not None else math.nan
        cen = (reg or {}).get('census') or {}
        chk(f'RING s_min {smin:g} — 이음매 = 연속: 자기 접합 0 · σ = 손 연속 고리 회로 (= 옛 경로 · 1e-12) · R_j = ∞ 도 같음',
            reg is not None and int(np.sum(reg['instances']['self'])) == 0 and rel(I1, want) < 1e-12 and rel(Ii, want) < 1e-12
            and rel(I_leg, want) < 1e-12,
            f"{None if reg is None else int(np.sum(reg['instances']['self']))} · {I1} · {Ii} ↔ {want} (옛 경로 {I_leg})")
        chk(f'RING s_min {smin:g} — census: 고리 조각 1 · 이음매 별칭 1 · 같은 조각 재방문 0 (첫 · 끝 위치 = 한 가지)',
            cen.get('n_ring_pieces') == 1 and cen.get('n_seam_alias') == 1 and cen.get('n_revisit_pairs') == 0,
            f"{ {k: cen.get(k) for k in ('n_ring_pieces', 'n_seam_alias', 'n_revisit_pairs', 'n_pieces')} }")
    m = ~((np.abs(pts[:, 0] - 3.5) < 1e-9) & (pts[:, 2] > 3.6) & (pts[:, 2] < 4.4))
    Pg = rows_pieces([pts[m]])
    sidg, _ = bed(Pg, RING_N)
    gapc = ((3, 1, 3), (3, 1, 4))
    wg = _graph_ref(cells, RING_N, drop=[gapc], extra=[(gapc[0], gapc[1], 1e4 / rj)])
    wgi = _graph_ref(cells, RING_N, drop=[gapc])
    regg = _try(lambda: registry(sidg, Pg, s_min_um=S_MIN), None)
    Ig = (regg or {}).get('instances') or {}
    cg = (regg or {}).get('census') or {}
    qs = [q for q in range(len(Ig.get('fi', []))) if Ig['self'][q]]
    rg = _try(lambda: solve(sidg, sig_e(), RING_N, plan(regg, rj)), None) if regg is not None else None
    rgi = _try(lambda: solve(sidg, sig_e(), RING_N, plan(regg, math.inf, allow_rj_limits=True)), None) if regg is not None else None
    chk('RING 틈 하나 (오른 다리 z 4.25 · 4.0 · 3.75 점 지움 · 틈 1.0) — 같은 sid · 이음매를 지나 한 조각 (조각 1 · 이음매 이음 1) · '
        '틈 두 끝 사이 자기 접합 하나 (포트 (3,1,3) · (3,1,4))',
        regg is not None and sidg.tobytes() == sid.tobytes() and cg.get('n_pieces') == 1 and cg.get('n_closed_paths_joined') == 1
        and len(qs) == 1 and {_pcells(regg, qs[0], 'i'), _pcells(regg, qs[0], 'j')} == set(gapc),
        f"{ {k: cg.get(k) for k in ('n_pieces', 'n_closed_paths_joined', 'n_ring_pieces')} } · 자기 {qs}")
    chk('RING 틈 하나 — σ = 손 회로 (연속 이음매 + 틈 R_j 간선 · 1e-12) · R_j = ∞ = 틈에서 열린 가닥 (1e-12)',
        rg is not None and rgi is not None and rel(I_of(rg, RING_N), wg) < 1e-12 and rel(I_of(rgi, RING_N), wgi) < 1e-12,
        f"{None if rg is None else I_of(rg, RING_N)} ↔ {wg} · {None if rgi is None else I_of(rgi, RING_N)} ↔ {wgi}")


SFR_N = (5, 8, 8)
SFR = [(1.95, 1.95, 0.5), (1.95, 1.95, 3.5), (1.95, 6.5, 3.5), (1.95, 6.5, 6.5), (2.05, 6.5, 6.5), (2.05, 6.5, 6.6), (3.5, 6.5, 6.6),
       (3.5, 2.05, 6.6), (2.05, 2.05, 6.6), (2.05, 2.05, 1.5)]


@case('SELFD')
def t_self_vs_distinct():
    """★ PRE-impl-02 · 1저자 Q-B — 자기 접합 탐지 = 서로 다른 섬유와 같은 중심선 근접 (d ≤ D) · 같은 섬유 쌍만 덧붙여 s 규칙.
    (i) KW (다리 중심선 1.2 > D 1.1 · 면 인접 셀): 옛 판 = 같은 fid 만 자기 접합 1 (L_c 0 · σ +4.25 %) ↔ 다른 fid instance 0 →
        같은 fid 도 instance 0 · 다리 사이 면 = 미등록 (fid 무관) · σ 가 R_j 와 무관 (= 손 사슬)
    (ii) SFR (다리 중심선 0.1414 < 2 r_f · 모서리 인접 셀 · 면 없음): 옛 판 = 같은 fid 접합 0 ↔ 다른 fid instance 1 →
        같은 fid 도 그 접합 · 기록 = 둘로 나눈 서로 다른 섬유와 같음 (L_c · 배율 · k · 포트 셀 · d0)
    (iii) XC (교차 · 닿음 0.8) 같은 fid ↔ 둘로 나눔 — 기록 같음."""
    rj = 1e3
    PW = rows(KW)
    sidw, _ = bed(PW, KU_N)
    rw = _try(lambda: registry(sidw, PW, s_min_um=KW_SMIN), None)
    seqw = seq_cells(KW[0])
    w_chain = chain_ref(len(seqw))
    rc = _try(lambda: solve(sidw, sig_e(), KU_N, plan(rw, rj)), None) if rw is not None else None
    rinf = _try(lambda: solve(sidw, sig_e(), KU_N, plan(rw, math.inf, allow_rj_limits=True)), None) if rw is not None else None
    rf = _try(lambda: solve(sidw, sig_e(), KU_N, plan(rw, rj, unreg_law='fused')), None) if rw is not None else None
    I_leg = I_of(solve_legacy(sidw, sig_e(), KU_N), KU_N)
    ok_i = (rw is not None and rc is not None and rinf is not None and rf is not None and len(rw['instances']['fi']) == 0
            and np.float64(rc['sigma_eff']).tobytes() == np.float64(rinf['sigma_eff']).tobytes()
            and rel(I_of(rc, KU_N), w_chain) < 1e-12 and rel(I_of(rf, KU_N), I_leg) < 1e-12)
    chk('SELFD (i) KW 같은 fid — instance 0 · σ(R_j 1e3) = σ(R_j ∞) (비트 · 접합 효과 0 · 옛 판 +4.25 %) = 손 사슬 (cut · 1e-12) · '
        'fused 법칙 = 옛 경로 (1e-12)', ok_i,
        f"{None if rw is None else len(rw['instances']['fi'])} · {None if rc is None else I_of(rc, KU_N)} · "
        f"{None if rinf is None else I_of(rinf, KU_N)} ↔ {w_chain} · fused {None if rf is None else I_of(rf, KU_N)} ↔ {I_leg}")
    PWd = rows([KW[0][:2], KW[0][2:]])
    sidwd, _ = bed(PWd, KU_N)
    rwd = _try(lambda: registry(sidwd, PWd, s_min_um=KW_SMIN), None)
    fk_s = [_face_kinds(rw, (1, 1, z), (2, 1, z)) for z in (1, 2, 3)] if rw is not None else None
    fk_d = [_face_kinds(rwd, (1, 1, z), (2, 1, z)) for z in (1, 2, 3)] if rwd is not None else None
    chk('SELFD (i) KW 같은 fid ↔ 둘로 나눈 서로 다른 섬유 — 둘 다 instance 0 · 다리 사이 면 셋 (z 1 · 2 · 3) = 미등록 (분류 fid 무관)',
        rw is not None and rwd is not None and len(rwd['instances']['fi']) == 0 and fk_s == fk_d == [[CJ.K_UNREG]] * 3,
        f'같은 fid {fk_s} · 나눔 {fk_d}')
    Ps = rows([SFR])
    sids, _ = bed(Ps, SFR_N)
    rs = _try(lambda: registry(sids, Ps, s_min_um=S_MIN), None)
    Pd = rows([SFR[:4], SFR[6:]])
    sidd, _ = bed(Pd, SFR_N)
    rd = _try(lambda: registry(sidd, Pd, s_min_um=S_MIN), None)
    leg = None
    if rs is not None:
        Is = rs['instances']
        cand = [q for q in range(len(Is['fi'])) if Is['self'][q] and _pcells(rs, q, 'i') and _pcells(rs, q, 'j')
                and {_pcells(rs, q, 'i')[:2], _pcells(rs, q, 'j')[:2]} == {(1, 1), (2, 2)}]
        leg = cand[0] if len(cand) == 1 else None
    rec_s = _inst_rec(rs, leg) if leg is not None else None
    rec_d = _inst_rec(rd, 0) if (rd is not None and len(rd['instances']['fi']) == 1) else None
    chk('SELFD (ii) SFR 같은 fid (모서리 인접 다리 · 중심선 0.1414 < 2 r_f · 셀 면 공유 없음) — 다리 사이 자기 접합 하나 (옛 판 0) · '
        '기록 (L_c · 배율 · k · 분산 간선 포트 셀 · d0) = 둘로 나눈 서로 다른 섬유 instance (하나) 와 같음 (1e-12)',
        _rec_same(rec_s, rec_d), f'같은 fid {rec_s} · 나눔 {rec_d}')
    Px = rows(XC)
    sidx, _ = bed(Px, XC_N)
    rx = _try(lambda: registry(sidx, Px, s_min_um=5.0), None)
    Pxd = rows([XC_A, XC_B])
    sidxd, _ = bed(Pxd, XC_N)
    rxd = _try(lambda: registry(sidxd, Pxd, s_min_um=5.0), None)
    qx = [q for q in range(len(((rx or {}).get('instances') or {}).get('fi', []))) if rx['instances']['self'][q]]
    rec_x = _inst_rec(rx, qx[0]) if len(qx) == 1 else None
    rec_xd = _inst_rec(rxd, 0) if (rxd is not None and len(rxd['instances']['fi']) == 1) else None
    chk('SELFD (iii) XC 교차 같은 fid ↔ 둘로 나눔 — 기록 같음 (L_c 1.2 · 배율 1 · k 1 · 포트 (1,1,2)–(2,1,2) · d0 0.8)',
        _rec_same(rec_x, rec_xd) and rec_xd is not None and abs(rec_xd['Lc'] - XC_LC) < 1e-9 and abs(rec_xd['d0'] - 0.8) < 1e-12,
        f'같은 fid {rec_x} · 나눔 {rec_xd}')


@case('QC')
def t_no_relocation():
    """★ PRE-impl-03 · 1저자 Q-C — 덮인 접점은 이웃 셀로 옮기지 않는다 (미실현 `covered_<sid>` · 덮은 상의 법칙만 = SDCP 는 SV 융합 한 번 ·
    같은 접촉을 두 번 세지 않는다) · 접합 + centerline PTFE = 거부 (옛 판: PTFE 피브릴이 포트 셀을 sid 7 로 덮으면 포트가 옆 셀로 옮겨
    σ 5.556 → 5.882 (+5.88 % · 절연체를 더해 σ 상승 = Rayleigh 위반) · SDCP 덮임 (DBE) = 옮긴 접합 + SV 융합 병렬 12.154 (+2.09 %))."""
    rj = 1e3
    P = cat_rows(rows(F2), rows([[(1.5, 1.5, 3.5)]], phase=5, kind=0, fid0=700))
    sid, _ = bed(P, F2_N)
    reg = _try(lambda: registry(sid, P, tol_sj_um=0.1, r_sdcp_um=0.5), None)
    gsv = 2.0 * SV * 250.0 / (SV + 250.0) * H
    E = [(0, 1, G_AX), (1, 2, G_AX), (2, 3, gsv), (3, 4, gsv)] + [(4 + i, 5 + i, G_AX) for i in range(4)]
    w_sv = ref_I(9, E, [(0, G_PL)], [(8, G_PL)])
    w_old = ref_I(9, E + [(2, 4, 1e4 / rj)], [(0, G_PL)], [(8, G_PL)])
    I_ = (reg or {}).get('instances') or {}
    S_ = (reg or {}).get('subedges') or {}
    chk('QC ① SDCP 가 접점 셀 (A 위끝 (1,1,3)) 을 덮음 — sid 5 · instance 1 · 미실현 (사유 covered_SDCP · instance · 간선) · 옮긴 포트 없음',
        reg is not None and int(sid[1, 1, 3]) == 5 and len(I_['fi']) == 1 and not bool(I_['realized'][0])
        and str(I_['reason'][0]) == 'covered_SDCP' and len(S_['inst']) == 1 and not bool(S_['realized'][0])
        and str(S_['reason'][0]) == 'covered_SDCP',
        f"{None if reg is None else (len(I_['fi']), list(I_['realized']), list(I_['reason']), list(S_.get('reason', [])))}")
    Ir = _try(lambda: I_of(solve(sid, sig_e(), F2_N, plan(reg, rj, ptfe_stamp='face_alpha')), F2_N))
    Ii = _try(lambda: I_of(solve(sid, sig_e(), F2_N, plan(reg, math.inf, allow_rj_limits=True, ptfe_stamp='face_alpha')), F2_N))
    print(f'    QC ① σ 접합 {Ir!r} · R_j ∞ {Ii!r} · 손 SV 만 {w_sv!r} · 옛 (옮긴 접합 + SV) {w_old!r}')
    chk('QC ① σ = SV 융합만 손 회로 (1e-12) = R_j ∞ (같은 접촉 한 번 · 옛 판 = 옮긴 접합 + SV 병렬 = +2.09 %)',
        rel(Ir, w_sv) < 1e-12 and rel(Ii, w_sv) < 1e-12, f'{Ir} · {Ii} ↔ {w_sv} (옛 {w_old})')
    P2 = rows(F2)
    sid2, _ = bed(P2, F2_N)
    reg2 = registry(sid2, P2)
    pl2 = plan(reg2, rj)
    pm = dict(pl2)
    pm['ptfe_stamp'] = 'centerline'
    pm['record'] = dict(pl2['record'], ptfe_stamp='centerline')
    pm['fp_rows'] = CJ.plan_rows_fp(pm)
    import ca_ext_cjunc as CW
    req = dict(R_j_ohm=1e6, len_law=CJ.CJUNC_LEN_LAW, unreg_law='cut', s_min_um=0.5, tol_ff_um=0.03)
    _CG_CALLS[0] = 0
    g = [('계획 centerline P0 (정량)', raises(lambda: plan(reg2, rj, ptfe_stamp='centerline', ptfe_jlaw='P0'))),
         ('계획 centerline P0 (시험 모드 · quantitative False)',
          raises(lambda: plan(reg2, rj, ptfe_stamp='centerline', ptfe_jlaw='P0', quantitative=False))),
         ('솔브 입구 — 계획 ptfe_stamp 만 centerline 으로 · 행 지문 다시 만듦', raises(lambda: solve(sid2, sig_e(), F2_N, pm))),
         ('protocol 기록 (ca_ext_cjunc.cjunc_protocol_record) centerline P0',
          raises(lambda: CW.cjunc_protocol_record(ptfe_stamp='centerline', ptfe_jlaw='P0', **req)))]
    cg = _CG_CALLS[0]
    for nm, okk in g:
        chk(f'QC ② 접합 + centerline = 거부 — {nm}', okk)
    pos_ok = _try(lambda: solve(sid2, sig_e(), F2_N, pl2)['sigma_eff'] > 0.0, False) is True
    fa_ok = _try(lambda: CW.cjunc_protocol_record(ptfe_stamp='face_alpha', ptfe_jlaw='P0', **req)['ptfe_stamp'] == 'face_alpha',
                 False) is True
    chk('QC ② 거부 경로 CG 0 · 양성 대조 (off 계획 풀림 · face_alpha protocol 받음)', cg == 0 and pos_ok and fa_ok,
        f'CG {cg} · off {pos_ok} · face_alpha {fa_ok}')


SVY_N = (6, 3, 8)
SVY = [[(1.5, 1.5, 0.5), (1.5, 1.5, 7.5)], [(1.5, 2.5, 3.5), (4.5, 2.5, 3.5), (4.5, 2.5, 7.5)]]


@case('QD')
def t_sv_split():
    """★ PRE-impl-04 · 1저자 Q-D — SV 반사실 대조 = 서로 다른 섬유 (또는 접합으로 갈린 같은 섬유 가지) 사이 SV 우회만 끊는다 · 섬유 자기
    연속 (SDCP 가 덮은 섬유 셀을 지나는 같은 조각의 길) 은 남긴다 · 끊기만 (부분 그래프 → 비 ≥ 1 · Rayleigh).  옛 판 = SV 면 전부 끊음 →
    SDCP 를 지나는 섬유 하나도 비 ∞ · SV_DEPENDENT (판정 문장 늘 제한 · 정보 없음)."""
    rj = 1e3
    gsv = 2.0 * SV * 250.0 / (SV + 250.0) * H

    def cf(sid, P, n):
        reg = _try(lambda: registry(sid, P, tol_sj_um=0.1, r_sdcp_um=0.5), None)
        r = _try(lambda: solve(sid, sig_e(), n, plan(reg, rj, sv_counterfactual={'threshold': 2.0})), None) if reg is not None else None
        return reg, r, (((r or {}).get('cjunc') or {}).get('sv_counterfactual') or {})
    n1 = (3, 3, 8)
    P1 = cat_rows(rows([[(1.5, 1.5, 0.5), (1.5, 1.5, 7.5)]]), rows([[(1.5, 1.5, 3.5)]], phase=5, kind=0, fid0=700))
    sid1, _ = bed(P1, n1)
    reg1, r1, c1 = cf(sid1, P1, n1)
    w1 = chain_I([G_PL] + [G_AX] * 2 + [gsv, gsv] + [G_AX] * 3 + [G_PL])
    chk('QD ① 섬유 하나가 SDCP 셀 (1,1,3) 을 지남 (접합 0) — σ = 손 사슬 (SV 두 면 · 1e-12) · 반사실 비 = 1 정확 (자기 연속 남김 · '
        '옛 = ∞ · SV_DEPENDENT) · 끊은 SV 면 0 · 표지 없음',
        r1 is not None and int(sid1[1, 1, 3]) == 5 and rel(I_of(r1, n1), w1) < 1e-12 and c1.get('status') == 'computed'
        and c1.get('sv_counterfactual_ratio') == 1.0 and c1.get('n_sv_faces_cut') == 0 and c1.get('flag') is None,
        f"{None if r1 is None else I_of(r1, n1)} ↔ {w1} · {c1}")
    P2 = cat_rows(rows(F1), rows([[(1.5, 1.5, 1.5)]], phase=5, kind=0, fid0=700))
    sid2, _ = bed(P2, F1_N)
    reg2, r2, c2 = cf(sid2, P2, F1_N)
    w2 = chain_I([G_PL] + [gsv, gsv] + [G_AX] + [1e4 / rj] + [G_AX] * 7 + [G_PL])
    chk('QD ② F1 (접합 하나) + 접합에서 먼 SDCP (A 셀 (1,1,1) 덮음) — σ = 손 사슬 (1e-12) · 접합 실현 · 반사실 비 1 정확 · 표지 없음',
        r2 is not None and int(sid2[1, 1, 1]) == 5 and rel(I_of(r2, F1_N), w2) < 1e-12
        and bool(reg2['instances']['realized'][0]) and c2.get('sv_counterfactual_ratio') == 1.0 and c2.get('flag') is None,
        f"{None if r2 is None else I_of(r2, F1_N)} ↔ {w2} · {c2}")
    P3 = cat_rows(rows(SVY), rows([[(1.5, 1.5, 3.5)]], phase=5, kind=0, fid0=700))
    sid3, _ = bed(P3, SVY_N)
    reg3, r3, c3 = cf(sid3, P3, SVY_N)
    #  손 회로 — A0..A2 (1,1,0..2) = 0..2 · S (1,1,3) = 3 · A4..A7 (1,1,4..7) = 4..7 · B 셀 열 (1,2,3) (2,2,3) (3,2,3) (4,2,3) (4,2,4..7) = 8..15
    E3 = ([(0, 1, G_AX), (1, 2, G_AX), (2, 3, gsv), (3, 4, gsv), (4, 5, G_AX), (5, 6, G_AX), (6, 7, G_AX), (3, 8, gsv)]
          + [(8 + i, 9 + i, G_AX) for i in range(7)])
    bot, top = [(0, G_PL)], [(7, G_PL), (15, G_PL)]
    I_full = ref_I(16, E3, bot, top)
    I_cut = ref_I(16, [e for e in E3 if e[:2] != (3, 8)], bot, top)
    I3 = (reg3 or {}).get('instances') or {}
    chk('QD ③ SVY (A 가 SDCP 셀 (1,1,3) 을 지남 · B 가 그 셀에 닿음) — A–B 접점 = SDCP 덮임 (미실현 covered_SDCP) · σ = 손 회로 (1e-12)',
        r3 is not None and int(sid3[1, 1, 3]) == 5 and len(I3['fi']) == 1 and not bool(I3['realized'][0])
        and str(I3['reason'][0]) == 'covered_SDCP' and rel(I_of(r3, SVY_N), I_full) < 1e-12,
        f"{None if r3 is None else I_of(r3, SVY_N)} ↔ {I_full} · {None if reg3 is None else (list(I3['realized']), list(I3['reason']))}")
    chk('QD ③ SVY 반사실 = B 의 SV 면만 끊음 (A 자기 연속 남김) — 비 = 손 I_full/I_cut (1e-10 · 옛 = A 도 끊음) · 끊은 SV 면 1 · '
        '다리 놓는 SDCP 성분 1 · 못 가른 성분 0 · 문턱 2 → SV_DEPENDENT 여부 = 비 ≥ 2',
        c3.get('status') == 'computed' and rel(float(c3.get('sv_counterfactual_ratio') or math.nan), I_full / I_cut) < 1e-10
        and c3.get('n_sv_faces_cut') == 1 and c3.get('n_bridging_components') == 1 and c3.get('n_unsplit_bridging_components') == 0
        and c3.get('flag') == ('SV_DEPENDENT' if I_full / I_cut >= 2.0 else None),
        f'{c3} ↔ 손 비 {I_full / I_cut}')
    kd = c3.get('kind')
    nfields = ('n_sdcp_components_touching', 'n_bridging_components', 'n_sv_faces_cut', 'n_sv_faces_kept_self',
               'n_unsplit_bridging_components')
    chk('QD ④ 기록 꼴 — 종류 counterfactual… (옛 counterfactual_cut_sv_faces 아님 · 정의가 바뀌었다) · 수 칸 다섯 = 정수',
        isinstance(kd, str) and kd.startswith('counterfactual') and kd != 'counterfactual_cut_sv_faces'
        and all(type(c3.get(k)) is int for k in nfields), f'{kd} · {[(k, c3.get(k)) for k in nfields]}')


@case('KBND')
def t_k_boundary():
    """PRE-impl-05 (P3 · 한계 기록 · 고치지 않음) — 분산판 v0 간선 수 k = ceil(L_c/L_par) 의 경계 (깊은 교차 90° → 89.99° · k 1 → 2 · 배율 차
    1.5e-8) 에서 σ 가 뛴다 (반쪽 간선이 셀 경계로 가 사전식 최소 셀로 옮겨진다 — 크기 ∝ h·r′/R_j).  생산 단위 (h 0.15 · r_f 0.075 · L_par 0.30
    · σ_VGCF 7853.98) R_j 1e2 · 1e4 · 1e6 Ω 의 뜀 = 사전 리뷰 탐침 값 (−0.978 % · −2.10e-4 · −2.11e-6) ± 10 % 로 묶는다 · ∝ 1/R_j ·
    같은 sid.  ⚠ 이 시험은 맞는 값이 아니라 이산화 오차 크기의 기록이다 (바뀌면 알린다 · `carbon_junction._n_sub` 주석)."""
    VP, NK = 0.15, (9, 3, 10)
    want = {1e2: -0.009782110461166504, 1e4: -0.000209786930659428, 1e6: -2.1066342607012345e-06}

    def run(th, rj):
        t = math.radians(th)
        C = np.array([3.5, 1.5, 3.5]) * VP
        u = np.array([math.sin(t), 0.0, math.cos(t)])
        b0, b1 = C - 3.0 * VP * u, C + 3.0 * VP * u
        A = [(3.5 * VP, 1.5 * VP, 0.5 * VP), (3.5 * VP, 1.5 * VP, 5.5 * VP)]
        B = [tuple(b0), tuple(b1), (b1[0], 1.5 * VP, 9.5 * VP)]
        P = rows([A, B], step=0.05)
        sid, _ = bed(P, NK, vox=VP)
        reg = registry(sid, P, vox=VP, r_f_um=0.075, tol_ff_um=0.03, L_par_um=0.30, r_port_um=0.30, s_min_um=3.0)
        r = solve(sid, sig_e(s_vgcf=7853.98, s_am=0.0041), NK, plan(reg, rj), vox=VP)
        return int(np.asarray(reg['instances']['nsub'])[0]), float(r['sigma_eff']), sid.tobytes()
    jumps, ok = {}, True
    for rj in (1e2, 1e4, 1e6):
        k0, s0, h0 = _try(lambda rj=rj: run(90.0, rj), (None, math.nan, b''))
        k1, s1, h1 = _try(lambda rj=rj: run(89.99, rj), (None, math.nan, b''))
        j = s1 / s0 - 1.0 if s0 == s0 and s0 != 0.0 else math.nan
        jumps[rj] = (k0, k1, j)
        ok &= bool(k0 == 1 and k1 == 2 and h0 == h1 and h0 != b'' and abs(j - want[rj]) <= 0.1 * abs(want[rj]))
    chk('KBND k 경계 σ 뜀 (90° → 89.99° · k 1 → 2 · 같은 sid) = 사전 리뷰 값 ± 10 % (R_j 1e2 · 1e4 · 1e6 Ω · 생산 단위)', ok, f'{jumps}')
    r42 = jumps[1e4][2] / jumps[1e2][2] if jumps[1e2][2] else math.nan
    r64 = jumps[1e6][2] / jumps[1e4][2] if jumps[1e4][2] else math.nan
    chk('KBND 크기 ∝ 1/R_j (큰 R_j 에서) — 뜀(1e6)/뜀(1e4) ∈ [0.009, 0.011] · 뜀(1e4)/뜀(1e2) ∈ [0.015, 0.03]',
        0.009 <= r64 <= 0.011 and 0.015 <= r42 <= 0.03, f'{r64} · {r42}')


@case('MUT-RCA2')
def t_mut_rca2():
    """새 보장의 판별력 (10-21 · PRE-impl 01 · 03 · 04 · 06) — 모듈 훅을 바꿔 끼운 변이가 위 시험 (손 회로) 에 옳은 이유로 걸려야 한다 ·
    변이 전 통과 (예외 없이) · 변이 뒤 같은 검사 실패 · 변이 안 예외 (`_try` 가 삼킨 것 포함) = 하네스 실패 (PRE-impl-09 규칙)."""
    rj = 1e3

    @contextlib.contextmanager
    def patched(name, fn):
        if not hasattr(CJ, name):
            raise AttributeError(f'변이 훅 {name} 없음')
        old = getattr(CJ, name)
        setattr(CJ, name, fn)
        try:
            yield
        finally:
            setattr(CJ, name, old)

    def gap_ok():
        P = rows_pieces([densify([(1.5, 1.5, 0.5), (1.5, 1.5, 3.15)]), densify([(1.5, 1.5, 3.85), (1.5, 1.5, 7.5)])])
        sid, _ = bed(P, GAP_N)
        I = _try(lambda: I_of(solve(sid, sig_e(), GAP_N, plan(registry(sid, P), rj)), GAP_N))
        return rel(I, chain_I([G_PL] + [G_AX] * 3 + [1e4 / rj] + [G_AX] * 4 + [G_PL])) < 1e-12

    def qc_ok():
        P = cat_rows(rows(F2), rows([[(1.5, 1.5, 3.5)]], phase=5, kind=0, fid0=700))
        sid, _ = bed(P, F2_N)
        gsv = 2.0 * SV * 250.0 / (SV + 250.0) * H
        E = [(0, 1, G_AX), (1, 2, G_AX), (2, 3, gsv), (3, 4, gsv)] + [(4 + i, 5 + i, G_AX) for i in range(4)]
        I = _try(lambda: I_of(solve(sid, sig_e(), F2_N, plan(registry(sid, P, tol_sj_um=0.1, r_sdcp_um=0.5), rj,
                                                            ptfe_stamp='face_alpha')), F2_N))
        return rel(I, ref_I(9, E, [(0, G_PL)], [(8, G_PL)])) < 1e-12

    def qd_ok():
        n1 = (3, 3, 8)
        P = cat_rows(rows([[(1.5, 1.5, 0.5), (1.5, 1.5, 7.5)]]), rows([[(1.5, 1.5, 3.5)]], phase=5, kind=0, fid0=700))
        sid, _ = bed(P, n1)
        r = _try(lambda: solve(sid, sig_e(), n1, plan(registry(sid, P, tol_sj_um=0.1, r_sdcp_um=0.5), rj,
                                                    sv_counterfactual={'threshold': None})), None)
        return (((r or {}).get('cjunc') or {}).get('sv_counterfactual') or {}).get('sv_counterfactual_ratio') == 1.0

    def ring_ok():
        sid, _ = bed(rows([RING]), RING_N)
        I = _try(lambda: I_of(solve(sid, sig_e(), RING_N, plan(registry(sid, rows([RING])), rj)), RING_N))
        return rel(I, _graph_ref(_cells_of_pts(densify(RING)), RING_N)) < 1e-12

    def live_only(piece, pos, piece_pos):
        a0, a1 = piece_pos[piece]
        c = np.arange(a0, a1)
        return c[pos['live'][c]]
    cases = (
        ('조각 = fid 규칙 (옛 · 같은 fid 조각 쌍을 서로 다른 섬유 규칙에서 뺌) → GAP 같은 셀 σ 0', '_distinct_keep',
         lambda segs, i, j: segs['fid'][i] != segs['fid'][j], gap_ok),
        ('포트 = 살아 있는 위치만 (옛 · 덮이면 r_port 안 이웃 셀로 옮김) → QC ① 옮긴 접합 + SV 병렬', '_piece_cand', live_only, qc_ok),
        ('반사실 = SV 면 전부 끊음 (옛) → QD ① SDCP 를 지나는 섬유 하나도 비 ∞', '_sv_cut_rows',
         lambda info: np.ones(len(info['comp']), bool), qd_ok),
        ('고리 이음매 별칭 끔 → 이음매 첫 · 끝 위치가 따로 (고리가 끊긴다)', '_ring_alias', lambda cu, is_ring: False, ring_ok),
    )
    for nm, name, fn, check in cases:
        _TRY_EXC[0] = 0
        b = bool(check())
        e0 = _TRY_EXC[0]
        c, why = None, ''
        try:
            with patched(name, fn):
                _TRY_EXC[0] = 0
                c = not bool(check())
                if _TRY_EXC[0]:
                    c, why = None, f'변이 안 예외 {_TRY_EXC[0]} 건 = 하네스 실패'
        except Exception as e:                              # noqa: BLE001 — 훅 없음 (고치기 전) · 변이 예외 = 하네스 실패
            c, why = None, f'{type(e).__name__}: {e}'
        if why:
            print(f'    MUT-RCA2 {nm}: {why}')
        chk(f'MUT-RCA2 {nm} (훅 `{name}` · 변이 전 통과 · 변이 실패 · 예외 없음)', b and e0 == 0 and c is True,
            f'base {b} (예외 {e0}) caught {c} {why}')


