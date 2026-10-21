# Part 2 — registry · census · SV split (A round 2 · 10-21).  flake8: noqa


def cjunc_registry(sid, box_lo, vox, add_pts, add_phase, add_fid, add_kind, *, r_f_um, tol_ff_um, L_par_um, r_port_um,
                   s_min_um, gap_tol=2.0, tol_P_um=None, tol_sj_um=None, r_ptfe_um=PTFE_R_UM, r_sdcp_um=SDCP_R_UM):
    """② 탄소 접합 원장 — **기하만** (σ · 전류 없음).  문턱 = 식 고정 · 숫자 = S0 단계 1 (설계 §4-1 · R §2-1) — 기본값을 두지 않는다
    (r_f · tol_ff · L_par · r_port · s_min 필수).  tol_P · tol_sj 기본 = tol_ff (설계: 한 숫자).  → dict (지문 포함).
    s_min_um = 꺾임 자기 접합 거르기 문턱 (경로 호 길이 µm) — None = 미등록 (구조화 거부 `self_s_min_missing` · 정량 계획이 막는다 ·
    시험 모드는 거르지 않고 진행 · 표지 `off_s_min_missing` · 바닥은 늘 적용).
    ★ 10-21 (사전 리뷰 impl · 1저자 Q-A–Q-D): 조각 = 섬유 (끊긴 조각 = 서로 다른 섬유 규칙 · 닫힌 경로 이음매 = 연속) · 자기 접합 = 같은
    조각 중심선 쌍 (d ≤ D · 바닥 · 쌍마다 s 규칙) · 포트 = 옮기지 않음 (덮였으면 미실현) · SV 반사실 대조 = 다리 SV 면만 끊는 표지 ('sv_cut')."""
    sid = np.asarray(sid)
    if sid.ndim != 3:
        raise ValueError('② 탄소 접합: sid 는 3 차원 격자')
    vox = float(vox)
    lo = np.asarray(box_lo, np.float64).reshape(3)
    if not (math.isfinite(vox) and vox > 0.0 and np.isfinite(lo).all()):
        raise ValueError(f'② 탄소 접합: vox · 상자 원점 유한 (vox > 0) — {vox!r} {lo!r}')
    thr = {'r_f_um': r_f_um, 'tol_ff_um': tol_ff_um, 'L_par_um': L_par_um, 'r_port_um': r_port_um, 'gap_tol': gap_tol,
           'tol_P_um': tol_ff_um if tol_P_um is None else tol_P_um, 'tol_sj_um': tol_ff_um if tol_sj_um is None else tol_sj_um,
           'r_ptfe_um': r_ptfe_um, 'r_sdcp_um': r_sdcp_um}
    for k_, v_ in thr.items():
        if isinstance(v_, bool) or not isinstance(v_, (int, float, np.floating, np.integer)) or not math.isfinite(float(v_)) \
                or float(v_) < 0.0:
            raise ValueError(f'② 탄소 접합: 문턱 {k_} = {v_!r} — 유한한 0 이상 실수 (R §2-1 · 숫자 = S0 단계 1)')
    thr = {k_: float(v_) for k_, v_ in thr.items()}
    if thr['r_f_um'] <= 0.0 or thr['gap_tol'] <= 0.0:
        raise ValueError('② 탄소 접합: r_f · gap_tol > 0')
    if thr['L_par_um'] <= 0.0:
        raise ValueError('② 탄소 접합: L_par > 0 (길이 법칙 v0 의 분모 · 배율 = max(1, L_c/L_par))')
    if s_min_um is not None and (isinstance(s_min_um, bool) or not isinstance(s_min_um, (int, float, np.floating, np.integer))
                                 or not math.isfinite(float(s_min_um)) or float(s_min_um) < 0.0):
        raise ValueError(f'② 탄소 접합: s_min = {s_min_um!r} — None (미등록 · 정량 거부) 또는 유한한 0 이상 실수 '
                         f'(꺾임 자기 접합 경로 호 길이 µm · 숫자 = S0 단계 1 뒤 R §2-1)')
    thr['s_min_um'] = None if s_min_um is None else float(s_min_um)
    P, PH, F, K = _input_check(add_pts, add_phase, add_fid, add_kind)
    n = np.array(sid.shape, np.int64)
    rej = []
    vg_paths = _paths_of(P, PH, F, K, 2, rej, 'VGCF')
    nonpath = [f for f, _, kp in vg_paths if not kp]
    if nonpath:
        rej.append({'code': 'vgcf_nonpath_fid', 'n': len(nonpath), 'detail': nonpath[:8],
                    'why': 'VGCF fid 가 경로 (kind 1) 가 아니다 — 점 스탬프 VGCF 는 중심선이 없다 (설계 §4-2 · 거부)'})
    vg_paths_ok = _canonical_paths([(f, r, kp) for f, r, kp in vg_paths if kp], P, rej, 'VGCF')   # ★ 10-21 RCA-04 기하 정준 순서
    segs, pieces = _segments_of(vg_paths_ok, P, thr['gap_tol'])
    pos, piece_pos = _positions(pieces, segs, lo, vox, n, sid)
    flat = sid.reshape(-1)
    # 위치 정렬 (셀 → 멤버십 · 정준 순서) · 주 위치 (셀의 기본 dof) — 10-21: (셀, 조각, 번호) 만 (fid 라벨 없음 · RCA-04)
    live = np.flatnonzero(pos['live'])
    o = live[np.lexsort((pos['k'][live], pos['piece'][live], pos['lin'][live]))]
    primary = np.zeros(len(pos['lin']), bool)
    if len(o):
        fl = np.ones(len(o), bool); fl[1:] = pos['lin'][o][1:] != pos['lin'][o][:-1]
        primary[o[fl]] = True
    pos['primary'] = primary
    cell_lin, cell_cnt = (np.unique(pos['lin'][o], return_counts=True) if len(o) else
                          (np.zeros(0, np.int64), np.zeros(0, np.int64)))
    cell_ptr = np.r_[0, np.cumsum(cell_cnt)].astype(np.int64)
    cell_pos = o
    s3cells = np.flatnonzero(flat == 3)
    orphan = np.setdiff1d(s3cells, cell_lin, assume_unique=False)
    if len(orphan):
        rej.append({'code': 'vgcf_orphan_cells', 'n': int(len(orphan)),
                    'why': '멤버십 없는 VGCF 셀 (점 스탬프 · SDCP–VGCF 브리지 진단 팔 · 다른 입력) — 정량 거부'})
    n_extra = int(np.sum(pos['live'] & ~primary & (pos['alias'] < 0)))   # ★ 고리 이음매 별칭 = 목표 위치의 dof (새 dof 아님)

    def _cell_positions(lins):
        """셀 선형 번호들 → (질의 번호, 위치 번호) 쌍 (그 셀의 살아있는 위치 전부)."""
        j = np.searchsorted(cell_lin, lins)
        okj = (j < len(cell_lin))
        okj[okj] = cell_lin[j[okj]] == lins[okj]
        q = np.flatnonzero(okj)
        a0 = cell_ptr[j[q]]; cnt = cell_ptr[j[q] + 1] - a0
        qq = np.repeat(q, cnt)
        off = np.arange(len(qq)) - np.repeat(np.cumsum(cnt) - cnt, cnt)
        return qq, cell_pos[np.repeat(a0, cnt) + off]

    # ── distinct-fiber instances (J2a · J2c · ★ 10-21 Q-A: 조각이 다르면 — 같은 fid 의 끊긴 조각 포함) ──
    rf = thr['r_f_um']
    D = 2.0 * rf + thr['tol_ff_um']
    T_touch = 2.0 * rf
    inst = _distinct_instances(segs, D, T_touch)
    # ── 자기 접합 (★ 10-21 Q-B — 같은 조각 중심선 쌍 · 바닥 · 쌍마다 s 규칙) ──
    sp = _self_pairs(segs, D, thr['s_min_um'])
    selfinst = _self_instances(sp, segs, T_touch)
    cgroups = _pair_groups(sp['i'], sp['j'], segs, np.ones(len(sp['i']), bool))   # 후보 무리 (바닥 쌍) — census
    nD = len(inst['fi'])
    nSf = len(selfinst['fi'])
    # ── 면 표 ──
    stride = np.array([n[1] * n[2], n[2], 1], np.int64)
    rows_lin, rows_ax, rows_kind, rows_pa, rows_pb, rows_inst = [], [], [], [], [], []
    contact = []                                             # (lin_a, ax, oa, ob)
    owner_ties = 0
    for ax in range(3):
        sa = [slice(None)] * 3; sb = [slice(None)] * 3
        sa[ax] = slice(0, -1); sb[ax] = slice(1, None)
        g3 = sid[tuple(sa)] == 3; h3 = sid[tuple(sb)] == 3
        cand = g3 | h3
        if not cand.any():
            continue
        ii = np.nonzero(cand)
        la = np.ravel_multi_index(ii, tuple(n)).astype(np.int64)
        lb = la + stride[ax]
        fc = lo + (np.stack(ii, 1).astype(np.float64) + 0.5) * vox
        fc[:, ax] += 0.5 * vox                               # 면 중심
        qa, pa_all = _cell_positions(la)
        qb, pb_all = _cell_positions(lb)
        has_a = np.zeros(len(la), bool); has_a[qa] = True
        has_b = np.zeros(len(lb), bool); has_b[qb] = True
        # 축방향 쌍 (같은 fid · 조각 · 번호 차 1 · ★ 10-21 고리 조각 = 둘레 (첫 ↔ 끝) 도)
        vv = has_a & has_b
        axial_face = np.zeros(len(la), bool)
        if vv.any():
            # 면마다 a 위치 × b 위치 펼치기
            ca = np.bincount(qa, minlength=len(la)); cb = np.bincount(qb, minlength=len(la))
            sa_ = np.r_[0, np.cumsum(ca)]; sb_ = np.r_[0, np.cumsum(cb)]
            fv = np.flatnonzero(vv)
            na = ca[fv]; nb = cb[fv]
            rep = na * nb
            face_r = np.repeat(fv, rep)
            off = np.arange(len(face_r)) - np.repeat(np.cumsum(rep) - rep, rep)
            ia = off // np.repeat(nb, rep); ib = off % np.repeat(nb, rep)
            PA = pa_all[np.argsort(qa, kind='stable')][sa_[face_r] + ia]
            PB = pb_all[np.argsort(qb, kind='stable')][sb_[face_r] + ib]
            dkk = np.abs(pos['k'][PA] - pos['k'][PB])
            wrap = pos['ring'][PA] & (dkk == pos['piece_ng'][PA] - 1) & (pos['piece_ng'][PA] > 2)
            isax = (pos['fid'][PA] == pos['fid'][PB]) & (pos['piece'][PA] == pos['piece'][PB]) & ((dkk == 1) | wrap)
            if isax.any():
                axial_face[face_r[isax]] = True
                rows_lin.append(la[face_r[isax]]); rows_ax.append(np.full(int(isax.sum()), ax))
                rows_kind.append(np.full(int(isax.sum()), K_AXIAL)); rows_pa.append(PA[isax]); rows_pb.append(PB[isax])
                rows_inst.append(np.full(int(isax.sum()), -1))
        # 접촉 면 (VV · 축방향 쌍 없음) · VX 면 (한쪽만 멤버십)
        need_a = (has_a & ~axial_face)
        need_b = (has_b & ~axial_face)
        sel_a = np.isin(qa, np.flatnonzero(need_a)); sel_b = np.isin(qb, np.flatnonzero(need_b))
        oa, ta = _owner_select(qa[sel_a], pa_all[sel_a], fc, pos, segs, len(la))
        ob, tb = _owner_select(qb[sel_b], pb_all[sel_b], fc, pos, segs, len(la))
        owner_ties += ta + tb
        cf = np.flatnonzero(vv & ~axial_face)
        for i in cf:
            contact.append((int(la[i]), ax, int(oa[i]), int(ob[i]), fc[i]))
        vx = np.flatnonzero(has_a ^ has_b)                    # 한쪽만 멤버십 (VGCF ↔ 비탄소 · 고아 VGCF 셀) — 축방향일 수 없다
        if len(vx):
            rows_lin.append(la[vx]); rows_ax.append(np.full(len(vx), ax)); rows_kind.append(np.full(len(vx), K_VX))
            rows_pa.append(np.where(has_a[vx], oa[vx], -1)); rows_pb.append(np.where(has_b[vx], ob[vx], -1))
            rows_inst.append(np.full(len(vx), -1))
    # ── 접촉 면 분류 (★ 10-21 Q-A · Q-B): 다른 조각 = 접합 자리 절단 (서로 다른 섬유 instance 발자국) · 미등록 /
    #    같은 조각 = 연속 (바닥 밖 · s < s_min) 이면 옛 융합 · 아니면 자기 instance 발자국 = 절단 · 미등록 ──
    D_fp = D + math.sqrt(3.0) * 0.5 * vox
    by_pair = {}
    for k in range(nD):
        by_pair.setdefault((int(inst['piece_i'][k]), int(inst['piece_j'][k])), []).append(k)
    by_self = {}
    for q in range(nSf):
        by_self.setdefault(int(selfinst['piece_i'][q]), []).append(q)
    n_cut_site = 0
    n_unreg = 0
    multi_site = 0
    n_self_fused = 0
    self_face_n = np.zeros(nSf, np.int64)

    def _near(c, segset):
        return float(np.sqrt(np.min(pt_seg_d2(np.repeat(c[None], len(segset), 0), segs['P0'][segset], segs['P1'][segset])[0])))

    for (lin_a, ax, oa_, ob_, fcen) in contact:
        if oa_ < 0 or ob_ < 0:
            continue
        pa_, pb_ = int(pos['piece'][oa_]), int(pos['piece'][ob_])
        ca = lo + (np.array(np.unravel_index(lin_a, tuple(n)), np.float64) + 0.5) * vox
        cb_ = ca.copy(); cb_[ax] += vox
        if pa_ == pb_:
            s_f, d_f = _pos_pair_sd(oa_, ob_, pos, segs, lo, vox)
            if bool(np.asarray(_continuity(s_f, d_f, D, thr['s_min_um']))):
                rows_lin.append(np.array([lin_a])); rows_ax.append(np.array([ax])); rows_kind.append(np.array([K_SELF_FUSED]))
                rows_pa.append(np.array([oa_])); rows_pb.append(np.array([ob_])); rows_inst.append(np.array([-1]))
                n_self_fused += 1
                continue
            best, bestd = -1, math.inf
            for q in by_self.get(pa_, ()):
                Si, Sj = _footprint_segs(selfinst, q)
                for A_, B_ in ((Si, Sj), (Sj, Si)):
                    da = _near(ca, B_); db = _near(cb_, A_)
                    if da <= D_fp and db <= D_fp and da + db < bestd:
                        best, bestd = q, da + db
            if best >= 0:
                rows_lin.append(np.array([lin_a])); rows_ax.append(np.array([ax])); rows_kind.append(np.array([K_CUT_SELF]))
                rows_pa.append(np.array([oa_])); rows_pb.append(np.array([ob_])); rows_inst.append(np.array([nD + best]))
                self_face_n[best] += 1
            else:
                rows_lin.append(np.array([lin_a])); rows_ax.append(np.array([ax])); rows_kind.append(np.array([K_UNREG]))
                rows_pa.append(np.array([oa_])); rows_pb.append(np.array([ob_])); rows_inst.append(np.array([-1]))
                n_unreg += 1
            continue
        key = (min(pa_, pb_), max(pa_, pb_))
        best, bestd = -1, math.inf
        nmatch = 0
        for k in by_pair.get(key, ()):
            Si, Sj = _footprint_segs(inst, k)                # run 전체 (긴 접촉 = lumped 간선 · run 위 면이 남으면 우회)
            seg_of_fa = Si if int(inst['piece_i'][k]) == pa_ else Sj
            seg_of_fb = Sj if int(inst['piece_i'][k]) == pa_ else Si
            da = _near(ca, seg_of_fb)
            db = _near(cb_, seg_of_fa)
            if da <= D_fp and db <= D_fp:
                nmatch += 1
                if da + db < bestd:
                    best, bestd = k, da + db
        if best >= 0:
            multi_site += int(nmatch > 1)
            rows_lin.append(np.array([lin_a])); rows_ax.append(np.array([ax])); rows_kind.append(np.array([K_CUT_SITE]))
            rows_pa.append(np.array([oa_])); rows_pb.append(np.array([ob_])); rows_inst.append(np.array([best]))
            n_cut_site += 1
        else:
            rows_lin.append(np.array([lin_a])); rows_ax.append(np.array([ax])); rows_kind.append(np.array([K_UNREG]))
            rows_pa.append(np.array([oa_])); rows_pb.append(np.array([ob_])); rows_inst.append(np.array([-1]))
            n_unreg += 1
    # ── 같은 셀 비연속 재방문 (같은 조각 · 별칭 짝 아님 · 가지마다 따로 · 합치지 않음 · RCA-03) — census · 경로로만 쌍 ──
    jset = set(zip(sp['i'][sp['junc']].tolist(), sp['j'][sp['junc']].tolist()))
    rv, rv_s = [], []
    for c_i in range(len(cell_lin)):
        mem = cell_pos[cell_ptr[c_i]:cell_ptr[c_i + 1]]
        if len(mem) < 2:
            continue
        for x in range(len(mem)):
            for y in range(x + 1, len(mem)):
                p, q = int(mem[x]), int(mem[y])
                if pos['piece'][p] != pos['piece'][q] or int(pos['alias'][p]) == q or int(pos['alias'][q]) == p:
                    continue
                dk_ = abs(int(pos['k'][p]) - int(pos['k'][q]))
                if pos['ring'][p]:
                    dk_ = min(dk_, int(pos['piece_ng'][p]) - dk_)
                if dk_ < 2:
                    continue
                rv.append((p, q, int(cell_lin[c_i])))
                rv_s.append(_pos_pair_sd(p, q, pos, segs, lo, vox)[0])

    def _covered(p, q):
        return any((a, b) in jset or (b, a) in jset for a in range(int(pos['s0'][p]), int(pos['s1'][p]) + 1)
                   for b in range(int(pos['s0'][q]), int(pos['s1'][q]) + 1))

    path_only, path_broken = [], 0
    for (p, q, _l) in rv:
        if _covered(p, q):
            continue
        a0_, a1_ = sorted((p, q))
        if np.all(pos['live'][a0_:a1_ + 1]):
            path_only.append((p, q))                          # 경로 (같은 조각 살아있는 위치 사슬) 로만 이어진다
        else:
            path_broken += 1                                  # 사이에 덮인 위치 — 경로도 끊김 (SV · 다른 상 법칙만)
    # ── 자기 접합 census (후보 = 바닥 쌍 무리 · 남은 = 접합 instance · 거른 = 접합 쌍 없는 후보 무리) ──
    ncand = len(cgroups)
    cs = np.asarray([float(sp['s'][_group_cp(m, sp)]) for m in cgroups], np.float64)
    nfilt = int(sum(1 for m in cgroups if not sp['junc'][m].any()))
    if thr['s_min_um'] is None:
        self_filter = 'off_s_min_missing'
        rej.append({'code': 'self_s_min_missing', 'test': 'J8-self', 'n': int(ncand),
                    'why': 's_min (꺾임 자기 접합 거르기 · 경로 호 길이) 미등록 — 숫자 = S0 단계 1 의 분포를 본 뒤 등록 R §2-1 개정 · '
                           '기본값 없음 (시험 모드 = 거르지 않고 진행 · 바닥은 늘 적용)'})
    else:
        self_filter = 'applied'
    rv_s = np.asarray(rv_s, np.float64)
    rv_s = rv_s[np.isfinite(rv_s)]
    self_census = {'self_filter': self_filter, 'n_self_candidates': int(ncand), 'n_self_kept': int(nSf),
                   'n_self_filtered': int(nfilt), 'n_self_s_undefined': 0,
                   'n_self_fused_faces': int(n_self_fused), 'n_self_revisits_path_only': int(len(path_only)),
                   'n_self_revisits_path_broken': int(path_broken),
                   'self_s_um': ({'min': float(cs.min()), 'median': float(np.median(cs)), 'max': float(cs.max())}
                                 if len(cs) else None),
                   'n_revisit_pairs': int(len(rv)),
                   'n_revisit_cells': int(len({x[2] for x in rv})),
                   'n_revisit_fibres': int(len({int(pos['fid'][x[0]]) for x in rv})),
                   'revisit_s_um': ({'n': int(len(rv_s)), 'min': float(rv_s.min()), 'median': float(np.median(rv_s)),
                                     'max': float(rv_s.max())} if len(rv_s) else None)}
    # ── instance 합치기 (distinct + self) · 포트 ──
    allinst = _merge_instances(inst, selfinst)
    ports = _ports(allinst, pos, piece_pos, segs, lo, vox, n, flat, thr['r_port_um'])
    allinst.update(ports)
    nI = len(allinst['fi'])
    nrv = np.zeros(nI, np.int64)
    for (p, q, _l) in rv:
        for kq in range(nD, nI):
            A_, B_ = allinst['self_A'][kq], allinst['self_B'][kq]
            if (np.any(A_ == p) and np.any(B_ == q)) or (np.any(A_ == q) and np.any(B_ == p)):
                nrv[kq] += 1
    allinst['self_n_revisit'] = nrv
    allinst['self_n_face'] = np.r_[np.zeros(nD, np.int64), self_face_n].astype(np.int64)
    allinst['long'] = allinst['Lc'] > thr['L_par_um'] * (1.0 + CJUNC_LPAR_RTOL)   # 긴 접촉 표지 (집계 · 거부 아님) — 원장에서 한 번
    allinst['mult'] = np.asarray(junction_len_mult(allinst['Lc'], thr['L_par_um']), np.float64).reshape(nI)   # 길이 법칙 v0
    # ── 분산판 v0 (10-21 RCA-05 · Q3 (가)) — instance 마다 k = ceil(L_c/L_par) 간선 (k 1 = instance 그대로 = 옛 점 접합) ──
    sub, nsub = _subedges(allinst, pos, piece_pos, segs, lo, vox, n, flat, thr, T_touch)
    allinst['nsub'] = nsub
    allinst['sub_ptr'] = np.r_[0, np.cumsum(nsub)].astype(np.int64)
    #  경로로만 쌍은 접합 간선이 실제로 잇지 않은 것만 (실현 간선의 포트 짝이 그 두 위치면 이어졌다)
    if len(path_only):
        jp = {(int(a), int(b)) for a, b, ok in zip(sub['port_i'], sub['port_j'], sub['realized']) if ok}
        path_only = [(p, q) for (p, q) in path_only if (p, q) not in jp and (q, p) not in jp]
        self_census['n_self_revisits_path_only'] = int(len(path_only))
    # ── SDCP 근접 · PTFE 덮임 — instance 대표점 (옛 칸 · census) + 간선마다 (계획이 읽는 것) ──
    cp = allinst['cp']
    a_sdcp = np.zeros(nI, bool)
    sd = P[PH == 5]
    scp = sub['cp']
    nS = len(sub['inst'])
    s_a = np.zeros(nS, bool)
    if len(sd) and (nI or nS):
        from scipy.spatial import cKDTree
        tree = cKDTree(sd)
        if nI:
            dd, _ = tree.query(cp)
            a_sdcp = (dd - thr['r_sdcp_um']) <= thr['tol_sj_um']
        if nS:
            ds, _ = tree.query(scp)
            s_a = (ds - thr['r_sdcp_um']) <= thr['tol_sj_um']
    ptfe_cov = np.zeros(nI, bool)
    s_cov = np.zeros(nS, bool)
    pt_paths = _paths_of(P, PH, F, K, 4, rej, 'PTFE')
    psegs, _ = _segments_of(pt_paths, P, thr['gap_tol'])
    if len(psegs['P0']):
        lim = thr['r_ptfe_um'] + rf + thr['tol_P_um']
        for k in range(nI):
            d2, _, _ = pt_seg_d2(np.repeat(cp[k][None], len(psegs['P0']), 0), psegs['P0'], psegs['P1'])
            ptfe_cov[k] = math.sqrt(float(np.min(d2))) <= lim
        for e in range(nS):
            d2, _, _ = pt_seg_d2(np.repeat(scp[e][None], len(psegs['P0']), 0), psegs['P0'], psegs['P1'])
            s_cov[e] = math.sqrt(float(np.min(d2))) <= lim
    allinst['a_sdcp'] = a_sdcp
    allinst['ptfe_cov'] = ptfe_cov
    sub['a_sdcp'] = s_a
    sub['ptfe_cov'] = s_cov
    # ── 면 표 정렬 ──
    if rows_lin:
        ft = {'lin': np.concatenate(rows_lin).astype(np.int64), 'ax': np.concatenate(rows_ax).astype(np.int64),
              'kind': np.concatenate(rows_kind).astype(np.int64), 'pa': np.concatenate(rows_pa).astype(np.int64),
              'pb': np.concatenate(rows_pb).astype(np.int64), 'inst': np.concatenate(rows_inst).astype(np.int64)}
        oo = np.lexsort((ft['pb'], ft['pa'], ft['kind'], ft['ax'], ft['lin']))
        ft = {k_: v_[oo] for k_, v_ in ft.items()}
    else:
        z = np.zeros(0, np.int64)
        ft = {'lin': z, 'ax': z.copy(), 'kind': z.copy(), 'pa': z.copy(), 'pb': z.copy(), 'inst': z.copy()}
    ft['key'] = ft['lin'] * 3 + ft['ax']
    # ── SV 반사실 대조 표지 (★ 10-21 Q-D · 면 행마다 · 기하만) ──
    ft['sv_cut'], sv_census = _sv_split(sid, ft, pos, piece_pos, segs, n, lo, vox, D, thr['s_min_um'])
    # ── census ──
    census = _census(allinst, pos, ft, cell_lin, cell_ptr, cell_pos, sid, flat, owner_ties, multi_site, n_cut_site, n_unreg,
                     segs, len(vg_paths_ok), len(pieces), rf)
    census.update(_sdcp_bridging(sid, ft, pos, n))
    census.update(self_census)
    census.update(_sub_census(allinst, sub))
    census.update(sv_census)
    pc = np.asarray(segs['piece_closed'], np.int64)
    meets = 0
    for c_i in range(len(cell_lin)):
        mem = cell_pos[cell_ptr[c_i]:cell_ptr[c_i + 1]]
        fp_ = {}
        for p in mem:
            fp_.setdefault(int(pos['fid'][p]), set()).add(int(pos['piece'][p]))
        meets += int(any(len(v) >= 2 for v in fp_.values()))
    census.update({'n_instances_same_fid_pieces': int(np.sum((allinst['fi'] == allinst['fj']) & ~allinst['self'])),
                   'n_piece_cell_meets': int(meets), 'n_ring_pieces': int(np.sum(pc == 2)),
                   'n_closed_paths_joined': int(np.sum(pc == 1)), 'n_seam_alias': int(np.sum(pos['alias'] >= 0)),
                   'piece_rule': CJUNC_PIECE_RULE})
    reg = {'kind': 'cjunc_registry', 'version': CJUNC_MODEL_VERSION, 'schema': CJUNC_SCHEMA, 'vox': vox, 'lo': lo,
           'shape': tuple(int(x) for x in n), 'thresholds': thr,
           'rules': {'lc': CJUNC_LC_RULE, 'port': CJUNC_PORT_RULE, 'footprint': CJUNC_FOOTPRINT_RULE, 'self': CJUNC_SELF_RULE,
                     'owner': CJUNC_OWNER_RULE, 'eps_d2_um2': CJUNC_EPS_D2_UM2, 'lpar_rtol': CJUNC_LPAR_RTOL,
                     'len_law': CJUNC_LEN_LAW, 'self_lc': CJUNC_SELF_LC_RULE, 'self_s': CJUNC_SELF_S_RULE,
                     'dist': CJUNC_DIST_RULE, 'branch': CJUNC_BRANCH_RULE, 'order': CJUNC_ORDER_RULE, 'cp': CJUNC_CP_RULE,
                     'piece': CJUNC_PIECE_RULE, 'sv_cf': CJUNC_SV_CF_RULE},
           'positions': pos, 'segments': segs, 'instances': allinst, 'subedges': sub, 'faces': ft, 'cell_lin': cell_lin,
           'cell_ptr': cell_ptr, 'cell_pos': cell_pos, 'n_extra_dofs': n_extra,
           'self_revisit_pairs': np.asarray(path_only, np.int64).reshape(-1, 2), 'rejections': rej, 'census': census}
    reg['fp'] = {'sid': _grid_fp(sid), 'centreline': _fp(segs), 'membership': _fp(pos), 'registry': registry_fp(reg)}
    return reg


def _distinct_instances(segs, D, T):
    """J2a · J2c — 서로 다른 섬유 (★ 10-21 Q-A: `_distinct_keep` = 조각이 다름 · 같은 fid 의 끊긴 조각 포함) 선분 쌍 중 최근접 ≤ D ·
    같은 조각 이웃 선분끼리 이어진 쌍 = instance 하나."""
    P0, P1 = segs['P0'], segs['P1']
    ns = len(P0)
    empty = {'fi': np.zeros(0, np.int64), 'fj': np.zeros(0, np.int64), 'self': np.zeros(0, bool), 'd0': np.zeros(0),
             'Lc': np.zeros(0), 'Ci': np.zeros((0, 3)), 'Cj': np.zeros((0, 3)), 'seg_i': [], 'seg_j': [],
             'piece_i': np.zeros(0, np.int64), 'piece_j': np.zeros(0, np.int64), 'si_min': np.zeros(0, np.int64),
             'sj_min': np.zeros(0, np.int64)}
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
    keep = np.asarray(_distinct_keep(segs, i, j), bool)
    i, j = i[keep], j[keep]
    if len(i) == 0:
        return empty
    sw = segs['piece'][i] > segs['piece'][j]                 # ★ 10-21 RCA-04 — 쌍 방향 = 정준 조각 순 (fid 라벨 아님)
    i, j = np.where(sw, j, i), np.where(sw, i, j)
    d, s, t, C1, C2 = seg_seg_closest(P0[i], P1[i], P0[j], P1[j])
    close = d <= D
    i, j, d, s, t, C1, C2 = i[close], j[close], d[close], s[close], t[close], C1[close], C2[close]
    if len(i) == 0:
        return empty
    uf = _UF()
    keyof = {}
    pi_, pj_ = segs['piece'], segs['piece']
    for x in range(len(i)):
        keyof[(int(pi_[i[x]]), int(segs['k'][i[x]]), int(pj_[j[x]]), int(segs['k'][j[x]]))] = x
    for x in range(len(i)):
        a0, ka, b0, kb = int(pi_[i[x]]), int(segs['k'][i[x]]), int(pj_[j[x]]), int(segs['k'][j[x]])
        for da in (-1, 0, 1):
            for db in (-1, 0, 1):
                y = keyof.get((a0, ka + da, b0, kb + db))
                if y is not None:
                    uf.union(x, y)
    groups = {}
    for x in range(len(i)):
        groups.setdefault(uf.find(x), []).append(x)
    out = {k: [] for k in ('fi', 'fj', 'd0', 'Ci', 'Cj', 'seg_i', 'seg_j', 'piece_i', 'piece_j', 'si_min', 'sj_min')}
    for g, mem in groups.items():
        mem = np.asarray(mem)
        #  ★ 10-21 (`CJUNC_CP_RULE` · RCA-04/05) — 접점 = 최근접 쌍들 중 거리² ε 띠 안 · 중점 사전식 최소 (나란한 접촉의 비유일 최근접점 ·
        #    쌍 목록 순서 · 선분 세분 무관) · d0 = 무리의 최소 거리 (옛 argmin 과 같은 값)
        dm2 = d[mem] * d[mem]
        bnd = mem[dm2 <= float(dm2.min()) + CJUNC_EPS_D2_UM2]
        mid = 0.5 * (C1[bnd] + C2[bnd])
        b = bnd[np.lexsort((j[bnd], i[bnd], mid[:, 2], mid[:, 1], mid[:, 0]))[0]]
        Si = np.unique(i[mem]); Sj = np.unique(j[mem])
        out['fi'].append(int(segs['fid'][i[b]])); out['fj'].append(int(segs['fid'][j[b]]))
        out['d0'].append(float(np.min(d[mem]))); out['Ci'].append(C1[b]); out['Cj'].append(C2[b])
        out['seg_i'].append(Si); out['seg_j'].append(Sj)
        out['piece_i'].append(int(segs['piece'][i[b]])); out['piece_j'].append(int(segs['piece'][j[b]]))
        out['si_min'].append(int(i[b])); out['sj_min'].append(int(j[b]))
    out['Lc'] = _touch_len_all(out['seg_i'], out['seg_j'], segs, T)
    #  ★ 10-21 (RCA-04) — instance 순서 = (정준 조각 i, 조각 j, 접점) — fid 라벨 아님
    o = np.lexsort((np.array([c[2] for c in out['Ci']]), np.array([c[1] for c in out['Ci']]),
                    np.array([c[0] for c in out['Ci']]), np.array(out['piece_j']), np.array(out['piece_i'])))
    res = {'fi': np.asarray(out['fi'], np.int64)[o], 'fj': np.asarray(out['fj'], np.int64)[o],
           'self': np.zeros(len(o), bool), 'd0': np.asarray(out['d0'])[o], 'Lc': np.asarray(out['Lc'])[o],
           'Ci': np.asarray(out['Ci']).reshape(-1, 3)[o], 'Cj': np.asarray(out['Cj']).reshape(-1, 3)[o],
           'seg_i': [out['seg_i'][x] for x in o], 'seg_j': [out['seg_j'][x] for x in o],
           'piece_i': np.asarray(out['piece_i'], np.int64)[o], 'piece_j': np.asarray(out['piece_j'], np.int64)[o],
           'si_min': np.asarray(out['si_min'], np.int64)[o], 'sj_min': np.asarray(out['sj_min'], np.int64)[o]}
    return res


def _census(inst, pos, ft, cell_lin, cell_ptr, cell_pos, sid, flat, owner_ties, multi_site, n_cut_site, n_unreg, segs, nfib,
            npiece, rf):
    cnt = np.diff(cell_ptr)
    if len(cell_pos):                                        # ★ 고리 이음매 별칭 = 같은 위치 (교차 셀 수에서 뺀다)
        al = (pos['alias'][cell_pos] >= 0).astype(np.int64)
        cnt = cnt - np.add.reduceat(al, cell_ptr[:-1]) if len(cnt) else cnt
    nI = len(inst['fi'])
    real = inst['realized']
    rel = {'same_cell': 0, 'face': 0, 'edge': 0, 'corner': 0, 'apart': 0}
    for k in np.flatnonzero(real):
        d = np.abs(pos['ijk'][inst['port_i'][k]] - pos['ijk'][inst['port_j'][k]])
        s = int(d.sum()); mx = int(d.max())
        rel['same_cell' if s == 0 else ('face' if s == 1 and mx == 1 else
                                         ('edge' if s == 2 and mx == 1 else ('corner' if s == 3 and mx == 1 else 'apart')))] += 1
    reasons = {}
    for r_ in inst['reason'][~real]:
        reasons[str(r_)] = reasons.get(str(r_), 0) + 1
    vx_by = {}
    vx = ft['kind'] == K_VX
    if vx.any():
        n3 = np.array(sid.shape)
        stride = np.array([n3[1] * n3[2], n3[2], 1])
        la = ft['lin'][vx]; lb = la + stride[ft['ax'][vx]]
        other = np.where(ft['pa'][vx] >= 0, flat[lb], flat[la])
        for s_, c_ in zip(*np.unique(other, return_counts=True)):
            vx_by[_SID_NAME.get(int(s_), str(int(s_)))] = int(c_)
    gap = inst['d0'][~inst['self']] - 2.0 * rf
    lc = inst['Lc']
    dk = inst['self_dk_min'][inst['self'] & (inst['self_dk_min'] >= 0)]
    return {'n_vgcf_fibres': int(nfib), 'n_pieces': int(npiece), 'n_segments': int(len(segs['P0'])),
            'n_positions': int(len(pos['lin'])), 'n_live_positions': int(np.sum(pos['live'])),
            'n_cross_cells': int(np.sum(cnt >= 2)), 'n_kway_cells_ge3': int(np.sum(cnt >= 3)),
            'n_instances': int(nI), 'n_instances_distinct': int(np.sum(~inst['self'])),
            'n_instances_self': int(np.sum(inst['self'])), 'n_realized': int(np.sum(real)), 'n_unrealized_by_reason': reasons,
            'n_port_ties': int(np.sum(inst['tie_i']) + np.sum(inst['tie_j'])), 'n_port_displaced': int(np.sum(inst['port_displaced'])),
            'port_relation': rel, 'n_cut_site_faces': int(n_cut_site), 'n_unreg_faces': int(n_unreg),
            'n_cut_self_faces': int(np.sum(ft['kind'] == K_CUT_SELF)), 'n_vx_faces_by_sid': vx_by,
            'owner_tie_noncanonical': int(owner_ties), 'n_faces_multi_site': int(multi_site),
            'surface_gap_um': ({'min': float(gap.min()), 'median': float(np.median(gap)), 'max': float(gap.max())}
                               if len(gap) else None),
            'Lc_um': ({'min': float(lc.min()), 'median': float(np.median(lc)), 'p90': float(np.quantile(lc, 0.90)),
                       'p99': float(np.quantile(lc, 0.99)), 'max': float(lc.max())} if len(lc) else None),
            #  길이 법칙 v0 배율 (max(1, L_c/L_par)) — 합 · 최댓값 · 1 넘는 수 (긴 접촉이 σ 에 얼마나 들어가는가 · S0 용)
            'len_mult': ({'sum': float(np.sum(inst['mult'])), 'max': float(np.max(inst['mult'])),
                          'n_gt1': int(np.sum(inst['mult'] > 1.0))} if len(lc) else None),
            #  긴 접촉이 꺾임 (같은 조각 · 경로 간격 작음) 에서 생기는지 고리 · 머리핀 (간격 큼) 에서 생기는지 가르는 진단 (S0 용 · 판정 아님)
            'n_long_distinct': int(np.sum(inst['long'] & ~inst['self'])) if 'long' in inst else None,
            'n_long_self': int(np.sum(inst['long'] & inst['self'])) if 'long' in inst else None,
            'self_dk_min': ({'min': int(dk.min()), 'median': float(np.median(dk)), 'max': int(dk.max()),
                             'n_le_4': int(np.sum(dk <= 4))} if len(dk) else None)}


def _sv_split(sid, ft, pos, piece_pos, segs, n, lo, vox, D, s_min):
    """★ 10-21 (사전 리뷰 PRE-impl-04 · 1저자 Q-D · `CJUNC_SV_CF_RULE`) — SV 반사실 대조가 끊을 SV 면 (면 행마다 'sv_cut') · census.
    SDCP 6-면 성분마다 SV 면 (VGCF 셀 ↔ 그 성분 SDCP 셀) 의 VGCF 주인 위치를 무리 짓는다: 같은 조각이고 (그 사이 위치가 전부 덮인 채
    그 성분 셀이다 — 섬유가 성분을 지난다 · 또는 두 위치가 같은 가닥의 연속 (`_continuity`)).  무리마다 '지남' = 덮인 채 지나는 이음이
    하나라도 있다.  끊을 행 = `_sv_cut_rows` (무리 둘 이상 = 다리 · 지나는 무리 하나 이하 → 지나지 않는 무리의 행).  → (행 마스크, census)."""
    nr = len(ft['lin'])
    cut = np.zeros(nr, bool)
    cen = {'n_sdcp_components_touching': 0, 'n_bridging_components': 0, 'n_sv_faces_cut_rows': 0,
           'n_sv_faces_kept_self': 0, 'n_unsplit_bridging_components': 0, 'sv_cf_rule': CJUNC_SV_CF_RULE}
    s5 = np.asarray(sid) == 5
    if not s5.any() or nr == 0:
        return cut, cen
    lab, _ = ndimage.label(s5)
    labf = lab.reshape(-1)
    flat = np.asarray(sid).reshape(-1)
    stride = np.array([n[1] * n[2], n[2], 1], np.int64)
    vx = np.flatnonzero(ft['kind'] == K_VX)
    la = ft['lin'][vx]; lb = la + stride[ft['ax'][vx]]
    a3 = ft['pa'][vx] >= 0
    lin5 = np.where(a3, lb, la)
    own = np.where(a3, ft['pa'][vx], ft['pb'][vx])
    m = (flat[lin5] == 5) & (own >= 0)
    rows = vx[m]
    if len(rows) == 0:
        return cut, cen
    comp = labf[lin5[m]].astype(np.int64)
    own = own[m].astype(np.int64)
    #  무리 — 같은 성분 · 같은 조각 주인 쌍마다 (사이 위치가 전부 덮인 채 그 성분 셀 = 지남 · 또는 연속)
    uf = _UF()
    passing_root = set()
    oc = sorted({(int(c), int(p)) for c, p in zip(comp, own)})
    by_c = {}
    for c, p in oc:
        by_c.setdefault(c, []).append(p)
        uf.find((c, p))
    for c, ps in by_c.items():
        for x in range(len(ps)):
            for y in range(x + 1, len(ps)):
                p, q = ps[x], ps[y]
                if pos['piece'][p] != pos['piece'][q]:
                    continue
                a0, a1 = piece_pos[int(pos['piece'][p])]
                kp, kq = int(pos['k'][p]), int(pos['k'][q])
                lo_k, hi_k = min(kp, kq), max(kp, kq)
                runs = [np.arange(a0 + lo_k + 1, a0 + hi_k)]
                if pos['ring'][p]:
                    ng = int(pos['piece_ng'][p])
                    runs.append(np.r_[np.arange(a0 + hi_k + 1, a0 + ng), np.arange(a0, a0 + lo_k)])
                through = False
                for btw in runs:
                    btw = btw[pos['alias'][btw] < 0] if len(btw) else btw
                    if len(btw) and np.all(~pos['live'][btw]) and np.all(pos['lin'][btw] >= 0) \
                            and np.all(labf[np.maximum(pos['lin'][btw], 0)] == c):
                        through = True
                if through:
                    uf.union((c, p), (c, q))
                    passing_root.add((c, p))
                    continue
                s_, d_ = _pos_pair_sd(p, q, pos, segs, lo, vox)
                if bool(np.asarray(_continuity(s_, d_, D, s_min))):
                    uf.union((c, p), (c, q))
    pas_root = {uf.find(x) for x in passing_root}
    roots = [uf.find((int(c), int(p))) for c, p in zip(comp, own)]
    gid = {}
    grp = np.asarray([gid.setdefault(r, len(gid)) for r in roots], np.int64)
    pas = np.asarray([r in pas_root for r in roots], bool)
    mask = np.asarray(_sv_cut_rows({'comp': comp, 'group': grp, 'passing': pas}), bool).reshape(len(rows))
    cut[rows[mask]] = True
    ncomp_touch = len(np.unique(comp))
    nbridge = nunsplit = kept_self = 0
    for c in np.unique(comp):
        mc = comp == c
        if len(np.unique(grp[mc])) < 2:
            continue
        nbridge += 1
        if len(np.unique(grp[mc & pas])) >= 2:
            nunsplit += 1
            continue
        kept_self += int(np.sum(mc & pas & ~mask))
    cen.update(n_sdcp_components_touching=int(ncomp_touch), n_bridging_components=int(nbridge),
               n_sv_faces_cut_rows=int(mask.sum()), n_sv_faces_kept_self=int(kept_self),
               n_unsplit_bridging_components=int(nunsplit))
    return cut, cen
