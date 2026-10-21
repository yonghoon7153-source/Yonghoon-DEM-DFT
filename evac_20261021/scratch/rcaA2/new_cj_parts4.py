# Part 4 — assembler (A round 2 · 10-21).  flake8: noqa


class CjuncAssembler:
    """`solve_sigma_z` 가 셀 dof 로 만든 면 (couple) · 판 결합을 받아 멤버십 dof · 접합 간선 · 절단 · 축약 · 실제 그래프 가지치기를
    한 계를 만든다 (J1 · J3 · J5 · J6 · J7 · J9 · J11 · J12 · E1 · E3 · E6)."""

    def __init__(self, plan, sid, cond, idx, n_cells, sig, vox):
        self.plan = plan
        self.reg = reg = plan['registry']
        self.sid = sid
        self.flat = np.asarray(sid).reshape(-1)
        self.sigf = np.asarray(sig, np.float64).reshape(-1)
        self.vox = float(vox)
        self.cells_lin = np.flatnonzero(np.asarray(cond).reshape(-1))
        self.n_cells = int(n_cells)
        pos = reg['positions']
        live = pos['live'].copy()
        if live.any() and not np.asarray(cond).reshape(-1)[pos['lin'][live]].all():
            raise ValueError('cjunc: 멤버십 셀이 이 채널에서 도체가 아니다 (σ_VGCF > 0 이어야 · 조용한 무효 금지)')
        alias = np.asarray(pos.get('alias', np.full(len(pos['lin']), -1)), np.int64)
        self.pos_dof = np.full(len(pos['lin']), -1, np.int64)
        prim = pos['primary']
        self.pos_dof[prim] = np.asarray(idx).reshape(-1)[pos['lin'][prim]]
        extra = np.flatnonzero(live & ~prim & (alias < 0))
        self.pos_dof[extra] = self.n_cells + np.arange(len(extra))
        al = np.flatnonzero(live & (alias >= 0))              # ★ 10-21 (Q-A) 고리 이음매 별칭 = 목표 위치의 dof (이음매 = 연속)
        self.pos_dof[al] = self.pos_dof[alias[al]]
        self.n_total = self.n_cells + len(extra)
        ft = reg['faces']
        self.ft = ft
        self.tkey = ft['key']
        self.E = []                                          # (u, v, g, cat, sa, sb, sida, sidb, 간선 행, 반사실 끊음)
        self.tomb = {'cut_site': 0, 'cut_self': 0, 'unreg_cut': 0}
        self.n_unreg_fused = 0
        self.n_self_fused = 0

    def add_faces(self, axis, a2, b2, g):
        if axis is None:
            raise ValueError('cjunc: 주기 면 (axis None) — 정량 거부 (입구에서 막혀야 한다)')
        a2 = np.asarray(a2, np.int64); b2 = np.asarray(b2, np.int64); g = np.asarray(g, np.float64)
        la = self.cells_lin[a2]; lb = self.cells_lin[b2]
        key = la * 3 + axis
        lo_ = np.searchsorted(self.tkey, key, 'left'); hi_ = np.searchsorted(self.tkey, key, 'right')
        hit = hi_ > lo_
        pt = ~hit
        if pt.any():
            self._emit(a2[pt], b2[pt], g[pt], np.full(int(pt.sum()), _CAT['other_bulk']), la[pt], lb[pt])
        if not hit.any():
            return
        fh = np.flatnonzero(hit)
        nr = (hi_ - lo_)[fh]
        fi = np.repeat(fh, nr)
        row = np.repeat(lo_[fh], nr) + (np.arange(len(fi)) - np.repeat(np.cumsum(nr) - nr, nr))
        kind = self.ft['kind'][row]
        pa = self.ft['pa'][row]; pb = self.ft['pb'][row]
        svc = np.asarray(self.ft.get('sv_cut', np.zeros(len(self.ft['kind']), bool)), bool)[row]
        m = kind == K_AXIAL
        if m.any():
            self._emit(self.pos_dof[pa[m]], self.pos_dof[pb[m]], g[fi[m]], np.full(int(m.sum()), _CAT['vv_axial']),
                       la[fi[m]], lb[fi[m]])
        m = kind == K_VX
        if m.any():
            u = np.where(pa[m] >= 0, self.pos_dof[np.maximum(pa[m], 0)], a2[fi[m]])
            v = np.where(pb[m] >= 0, self.pos_dof[np.maximum(pb[m], 0)], b2[fi[m]])
            sa_, sb_ = self.flat[la[fi[m]]], self.flat[lb[fi[m]]]
            pair = np.minimum(sa_, sb_) * 10 + np.maximum(sa_, sb_)
            cat = np.where(np.isin(pair, (13, 23)), _CAT['va_face'], np.where(pair == 35, _CAT['sv_face'], _CAT['vx_other']))
            self._emit(u, v, g[fi[m]], cat, la[fi[m]], lb[fi[m]], cf=svc[m] & (cat == _CAT['sv_face']))
        m = kind == K_UNREG
        if m.any():
            if self.plan['unreg_law'] == 'fused':
                self._emit(self.pos_dof[pa[m]], self.pos_dof[pb[m]], g[fi[m]], np.full(int(m.sum()), _CAT['vv_unreg_fused']),
                           la[fi[m]], lb[fi[m]])
                self.n_unreg_fused += int(m.sum())
            else:
                self.tomb['unreg_cut'] += int(m.sum())
        m = kind == K_SELF_FUSED
        if m.any():                                          # 같은 가닥의 연속 (바닥 밖 · s < s_min) — 옛 복셀 융합 그대로 (접합 아님)
            self._emit(self.pos_dof[pa[m]], self.pos_dof[pb[m]], g[fi[m]], np.full(int(m.sum()), _CAT['vv_self_fused']),
                       la[fi[m]], lb[fi[m]])
            self.n_self_fused += int(m.sum())
        self.tomb['cut_site'] += int(np.sum(kind == K_CUT_SITE))
        self.tomb['cut_self'] += int(np.sum(kind == K_CUT_SELF))

    def _emit(self, u, v, g, cat, la, lb, cf=None):
        u = np.asarray(u, np.int64)
        cfa = np.zeros(len(u), bool) if cf is None else np.asarray(cf, bool).reshape(len(u))
        self.E.append((u, np.asarray(v, np.int64), np.asarray(g, np.float64), np.asarray(cat, np.int64), self.sigf[la],
                       self.sigf[lb], self.flat[la], self.flat[lb], np.full(len(u), -1, np.int64), cfa))

    def _plate_owner(self, A, top):
        """판 결합 셀이 VGCF (멤버십) 이면 판 쪽 면 중심에 최근접 멤버십 dof (J9) — 아니면 그대로."""
        A = np.asarray(A, np.int64)
        if len(A) == 0:
            return A
        reg = self.reg
        pos = reg['positions']
        lin = self.cells_lin[A]
        j = np.searchsorted(reg['cell_lin'], lin)
        okj = j < len(reg['cell_lin'])
        okj[okj] = reg['cell_lin'][j[okj]] == lin[okj]
        if not okj.any():
            return A
        q = np.flatnonzero(okj)
        a0 = reg['cell_ptr'][j[q]]; cnt = reg['cell_ptr'][j[q] + 1] - a0
        qq = np.repeat(q, cnt)
        off = np.arange(len(qq)) - np.repeat(np.cumsum(cnt) - cnt, cnt)
        pp = reg['cell_pos'][np.repeat(a0, cnt) + off]
        ijk = np.stack(np.unravel_index(lin, reg['shape']), 1).astype(np.float64)
        X = reg['lo'] + (ijk + 0.5) * self.vox
        X[:, 2] += (0.5 if top else -0.5) * self.vox
        own, _ = _owner_select(qq, pp, X, pos, reg['segments'], len(A))
        out = A.copy()
        sel = own >= 0
        out[sel] = self.pos_dof[own[sel]]
        return out

    def build(self, Ab, gb, At, gt, cb=None, ct=None):
        """주 계 — 멤버십 dof · 분산 접합 간선 · 축약 · 절단 · 실제 그래프 가지치기 · 관통 · 단락 (J11).  반사실 대조가 같은 판 입력을
        다시 쓰도록 보관한다 (`sv_counterfactual`)."""
        self._plate_in = (Ab, gb, At, gt, cb, ct)
        out, st = self._assemble(Ab, gb, At, gt, cb, ct, counterfactual=False)
        self.junction_edge_sub = st['e']
        self.junction_edge_inst = np.asarray(self.reg['subedges']['inst'], np.int64)[st['e']]
        self.n_contracted = st['n_contracted']
        self.stats = st['stats']
        self.n_sv_edges = st['n_sv_edges']
        if 'reason' not in out:
            self.sys = st['sys']
            self._jidx = st['jidx']
            self._jsub = st['jsub']
        return out

    def _assemble(self, Ab, gb, At, gt, cb=None, ct=None, counterfactual=False):
        """계 조립 (부작용 없음) — counterfactual = 반사실 대조 판 (원장이 'sv_cut' 로 표지한 SV 다리 면 간선을 뺀다 · ★ 10-21 Q-D ·
        옛 = SV 면 부류 전부).  → (솔버 입력 | 사유, 상태)."""
        plan, reg = self.plan, self.reg
        sub = reg['subedges']
        #  분산 접합 간선 (간선마다 한 행 · 10-21 RCA-05) · 축약 — 주 계의 간선 목록 (self.E) 은 바꾸지 않는다 (지역 사본)
        mode = plan['mode']
        pu = self.pos_dof[np.maximum(sub['port_i'], 0)]; pv = self.pos_dof[np.maximum(sub['port_j'], 0)]
        e = np.flatnonzero(mode == MODE_EDGE)
        Elist = list(self.E)
        if len(e):
            gj = plan['g_code'][e]
            Elist.append((pu[e], pv[e], gj, np.full(len(e), _CAT['vv_junction']), np.full(len(e), np.nan),
                          np.full(len(e), np.nan), np.full(len(e), 3), np.full(len(e), 3), e.astype(np.int64),
                          np.zeros(len(e), bool)))
        rep = np.arange(self.n_total)
        #  ★ 10-21 (RCA-03) — 재방문 가지는 합치지 않는다 (옛: s < s_min 재방문 = 두 위치 한 노드 · 비연속 가닥 단락).
        #  접합 축약 (R_j′ = 0 · J6) — 단락 판정 (J11) 대상은 이 무리뿐
        con = np.flatnonzero(mode == MODE_CONTRACT)
        uf = _UF()
        for k in con:
            uf.union(int(rep[pu[k]]), int(rep[pv[k]]))
        members = {}
        for x in list(uf.p):
            members.setdefault(uf.find(x), []).append(x)
        if members:
            jr = np.arange(self.n_total)
            for r_, ms in members.items():
                jr[np.asarray(ms)] = r_
            rep = jr[rep]
        n_contracted = int(len(con))
        Ab2 = rep[self._plate_owner(Ab, False)] if Ab is not None else np.zeros(0, np.int64)
        At2 = rep[self._plate_owner(At, True)] if At is not None else np.zeros(0, np.int64)
        gb = np.asarray(gb if gb is not None else [], np.float64); gt = np.asarray(gt if gt is not None else [], np.float64)
        U = np.concatenate([x[0] for x in Elist]) if Elist else np.zeros(0, np.int64)
        V = np.concatenate([x[1] for x in Elist]) if Elist else np.zeros(0, np.int64)
        G = np.concatenate([x[2] for x in Elist]) if Elist else np.zeros(0)
        CAT = np.concatenate([x[3] for x in Elist]) if Elist else np.zeros(0, np.int64)
        SA = np.concatenate([x[4] for x in Elist]) if Elist else np.zeros(0)
        SB = np.concatenate([x[5] for x in Elist]) if Elist else np.zeros(0)
        IA = np.concatenate([x[6] for x in Elist]) if Elist else np.zeros(0, np.int64)
        IB = np.concatenate([x[7] for x in Elist]) if Elist else np.zeros(0, np.int64)
        TG = np.concatenate([x[8] for x in Elist]) if Elist else np.zeros(0, np.int64)
        CF = np.concatenate([x[9] for x in Elist]) if Elist else np.zeros(0, bool)
        U = rep[U]; V = rep[V]
        keep = (U != V) & (G > 0.0)
        n_sv_edges = int(np.sum(keep & (CAT == _CAT['sv_face'])))
        n_cf_edges = int(np.sum(keep & CF))
        if counterfactual:
            keep &= ~CF
        U, V, G, CAT, SA, SB, IA, IB, TG = (U[keep], V[keep], G[keep], CAT[keep], SA[keep], SB[keep], IA[keep], IB[keep],
                                            TG[keep])
        # 단락 (J11) — 축약 무리가 두 판에 다 닿음
        short = False
        big = [r_ for r_, ms in members.items() if len(ms) >= 2]
        if big:
            bs = set(Ab2.tolist()); ts = set(At2.tolist())
            short = any((r_ in bs and r_ in ts) for r_ in big)
        # 실제 그래프 연결 성분 (J7 · J12 · E3)
        from scipy.sparse.csgraph import connected_components
        n = self.n_total
        A = sparse.coo_matrix((np.ones(len(U), np.int8), (U, V)), shape=(n, n))
        ncomp, lab = connected_components(A, directed=False)
        is_rep = rep == np.arange(n)
        bot_c = np.zeros(ncomp, bool); top_c = np.zeros(ncomp, bool)
        bot_c[lab[Ab2]] = True; top_c[lab[At2]] = True
        kept_c = bot_c | top_c
        thr_c = bot_c & top_c
        kept = kept_c[lab] & is_rep
        n_kept = int(kept.sum())
        n_through = int((thr_c[lab] & is_rep).sum())
        n_path_only = int(len(np.asarray(reg.get('self_revisit_pairs', np.zeros((0, 2)))).reshape(-1, 2)))
        stats = {'n_extra_dofs': int(self.n_total - self.n_cells), 'n_contracted': n_contracted,
                 'n_floating_dropped': int((is_rep & ~kept).sum()), 'n_through_dof': n_through,
                 'n_plate_reachable_dof': n_kept, 'short': bool(short), 'tombstones': dict(self.tomb),
                 'n_unreg_fused': int(self.n_unreg_fused), 'n_junction_edges': int(np.sum(TG >= 0)),
                 'n_self_fused_faces': int(self.n_self_fused), 'n_self_revisits_path_only': n_path_only}
        st = {'e': e, 'n_contracted': n_contracted, 'stats': stats, 'n_sv_edges': n_sv_edges, 'n_cf_edges': n_cf_edges}
        if short:
            return {'reason': 'cjunc_electrode_short'}, st
        if n_kept == 0:
            return {'reason': 'all_floating_dropped'}, st
        if n_through == 0:
            return {'reason': 'no_through_component'}, st
        new = -np.ones(n, np.int64)
        new[kept] = np.arange(n_kept)
        ek = kept[U] & kept[V]
        U, V, G, CAT, SA, SB, IA, IB, TG = U[ek], V[ek], G[ek], CAT[ek], SA[ek], SB[ek], IA[ek], IB[ek], TG[ek]
        jidx = np.flatnonzero(TG >= 0)
        st['jidx'] = jidx
        st['jsub'] = TG[jidx]
        u, v = new[U], new[V]
        bk = kept[Ab2]; tk = kept[At2]
        Abn, gbn = new[Ab2[bk]], gb[bk]
        Atn, gtn = new[At2[tk]], gt[tk]
        cbn = tuple(np.asarray(x)[bk] for x in cb) if cb is not None else None
        ctn = tuple(np.asarray(x)[tk] for x in ct) if ct is not None else None
        diag = np.zeros(n_kept)
        np.add.at(diag, u, G); np.add.at(diag, v, G)
        np.add.at(diag, Abn, gbn); np.add.at(diag, Atn, gtn)
        b = np.zeros(n_kept)
        np.add.at(b, Abn, gbn)
        L = sparse.coo_matrix((np.concatenate([-G, -G, diag]), (np.concatenate([u, v, np.arange(n_kept)]),
                                                                  np.concatenate([v, u, np.arange(n_kept)]))),
                              shape=(n_kept, n_kept)).tocsr()
        st['sys'] = {'u': u, 'v': v, 'G': G, 'CAT': CAT, 'SA': SA, 'SB': SB, 'IA': IA, 'IB': IB, 'Ab': Abn, 'gb': gbn,
                     'At': Atn, 'gt': gtn, 'n': n_kept}
        return {'L': L, 'b': b, 'Ab': Abn, 'gb': gbn, 'At': Atn, 'gt': gtn, 'cb': cbn, 'ct': ctn, 'n_dof': n_kept}, st

    def record(self, phi):
        """원장을 읽는 소산 분담 · 접합 전류 (E1 · E2 · E4′) — 같은 단위 (코드) 로만 합친다.  접합 전류 = instance 마다 그 간선 합.
        ★ 10-21 (RCA-06) — 옛 `sv_dominant` (지배성 표지) 철회 → `sv_local_dissipation` (국소 소산 몫 진단 · 지배성 보증 아님)."""
        s = self.sys
        u, v, G, CAT = s['u'], s['v'], s['G'], s['CAT']
        dphi = phi[u] - phi[v]
        P = G * dphi * dphi
        Pb = s['gb'] * (phi[s['Ab']] - 1.0) ** 2
        Pt = s['gt'] * (phi[s['At']]) ** 2
        Ptot = float(P.sum() + Pb.sum() + Pt.sum())
        share = {k: 0.0 for k in _CAT}
        share['sdcp_cell'] = 0.0
        share['plate'] = float(Pb.sum() + Pt.sum())
        sv = CAT == _CAT['sv_face']
        share['sv_face'] = float(P[sv].sum())
        rest = ~sv
        ia5 = (s['IA'] == 5) & rest; ib5 = (s['IB'] == 5) & rest
        with np.errstate(invalid='ignore', divide='ignore'):
            fa = np.where(ia5, s['SB'] / (s['SA'] + s['SB']), 0.0)        # a 쪽 (SDCP) 반셀 몫 = σb/(σa+σb)
            fb = np.where(ib5, s['SA'] / (s['SA'] + s['SB']), 0.0)
        fa = np.nan_to_num(fa); fb = np.nan_to_num(fb)
        ps = P * (fa + fb)
        share['sdcp_cell'] = float(ps[rest].sum())
        for k, c in _CAT.items():
            if k == 'sv_face':
                continue
            m = CAT == c
            share[k] = float((P[m] * (1.0 - fa[m] - fb[m])).sum())
        tot = sum(share.values())
        frac = {k: (x / Ptot if Ptot > 0 else 0.0) for k, x in share.items()}
        nI = len(self.reg['instances']['fi'])
        jI = np.full(nI, np.nan)                             # instance 마다 접합 전류 (그 간선 합 · 간선 없는 instance = NaN)
        if len(self._jidx):
            qi = np.asarray(self.reg['subedges']['inst'], np.int64)[self._jsub]
            acc = np.zeros(nI)
            np.add.at(acc, qi, G[self._jidx] * dphi[self._jidx])
            has = np.zeros(nI, bool); has[qi] = True
            jI[has] = acc[has]
        I_bot = float(np.sum(s['gb'] * (1.0 - phi[s['Ab']])))
        sv_I = float(np.sum(np.abs(G[sv] * dphi[sv]))) / I_bot if I_bot > 0 else None
        sld = {'kind': 'diagnostic_local_dissipation', 'sv_share': float(frac['sv_face'] + frac['sdcp_cell']),
               'vv_junction_share': float(frac['vv_junction']),
               'meaning': 'SV 면 + SDCP 셀 소산 몫 = 국소 저항 민감도 — 경로 지배 · 우회 크기 보증 아님 (RCA-06 · 반사실 대조 = 선택 노브)'}
        return {'P_total_code': Ptot, 'P_sum_check_code': float(tot), 'dissipation_share': frac,
                'sv_local_dissipation': sld,
                'sv_face_abs_current_over_I': sv_I, 'junction_current_code': jI, 'I_bot_code': I_bot}

    def sv_counterfactual(self, solve, I_full, request, certify=None):
        """반사실 대조 (10-21 Codex RCA-06 · 1저자 Q4 (가) · 선택 노브) — 같은 침대 · 같은 R_j · 같은 판 입력에서 ★ 10-21 (사전 리뷰
        PRE-impl-04 · 1저자 Q-D) **SV 다리만** 끊은 계의 단자 전류 I_cut → `sv_counterfactual_ratio` = I_full / I_cut (≥ 1 · Rayleigh —
        끊기만 = 부분 그래프).  다리 = 서로 다른 섬유 · 접합으로 갈린 가지를 잇는 SDCP 성분의 SV 면 (원장 'sv_cut' · `_sv_split`) ·
        SDCP 를 지나는 섬유의 자기 연속은 남긴다 (옛: SV 면 전부 → SDCP 를 지나는 섬유 하나도 비 ∞ · 정보 없음).  문턱 (request) 이 있을
        때만 비교 표지 `SV_DEPENDENT` (비 ≥ 문턱) — 문턱 기본값 없음 (등록이 채운다).
        비 inf (`no_through_without_sv`) = **위상** 에서만 — 다리 SV 면을 끊은 조립 그래프에 관통 성분이 없을 때 (가지치기 사유).  관통 성분이
        있는데 푼 I_cut ≤ 0 · 비유한 = 수치 실패 (`nonpositive_cut_current` · 비 없음 — 양의 컨덕턴스 그래프의 관통 전류는 해석적으로 > 0).
        certify = 수렴 증서 (주 해와 같은 함수 · `step3_sigma` 가 CONV_CERT 일 때 넘긴다) — (L, b, φ, info, 잔차, Ab, gb, At, gt) → dict ·
        증서 실패 = 미수렴 (비 · 표지 없음 · 주 해 증서만 보고 분모를 믿지 않는다 · 10-21 사전 공격 리뷰)."""
        thr = request.get('threshold') if isinstance(request, dict) else None
        Ab, gb, At, gt, cb, ct = self._plate_in
        out, st = self._assemble(Ab, gb, At, gt, cb, ct, counterfactual=True)
        cen = self.reg.get('census') or {}
        rec = {'kind': CJUNC_SV_CF_KIND, 'rule': CJUNC_SV_CF_RULE, 'requested': True, 'threshold': thr,
               'n_sv_faces_cut': int(st['n_cf_edges']),
               'n_sdcp_components_touching': int(cen.get('n_sdcp_components_touching', 0)),
               'n_bridging_components': int(cen.get('n_bridging_components', 0)),
               'n_sv_faces_kept_self': int(cen.get('n_sv_faces_kept_self', 0)),
               'n_unsplit_bridging_components': int(cen.get('n_unsplit_bridging_components', 0)),
               'G_full_code': float(I_full), 'G_cut_code': None,
               'sv_counterfactual_ratio': None, 'flag': None, 'cg_info': None, 'resid': None, 'conv_cert': None}
        if not (math.isfinite(float(I_full)) and float(I_full) > 0.0):
            rec.update(status='nonpositive_full_current')       # 주 해 단자 전류 ≤ 0 · 비유한 — 비의 분자를 믿을 수 없다 (풀지 않는다)
        elif out.get('reason'):
            if out['reason'] in ('no_through_component', 'all_floating_dropped'):
                rec.update(status='no_through_without_sv', G_cut_code=0.0, sv_counterfactual_ratio=math.inf)
            else:
                rec.update(status=str(out['reason']))
        else:
            phi_c, info = solve(out['L'], out['b'])
            resid = float(np.linalg.norm(out['L'] @ phi_c - out['b']) / max(np.linalg.norm(out['b']), 1e-30))
            I_c = float(np.sum(out['gb'] * (1.0 - phi_c[out['Ab']])))
            rec.update(cg_info=int(info) if info else 0, resid=resid, G_cut_code=I_c)
            cert = None
            if certify is not None:
                cert = certify(out['L'], out['b'], phi_c, info, resid, out['Ab'], out['gb'], out['At'], out['gt'])
                rec['conv_cert'] = cert
            if bool(info) or not np.isfinite(resid) or resid > 1e-6 or (cert is not None and not cert.get('ok')):
                rec.update(status='unconverged')
            elif math.isfinite(I_c) and I_c > 0.0:
                rec.update(status='computed', sv_counterfactual_ratio=float(I_full / I_c))
            else:
                rec.update(status='nonpositive_cut_current')       # 관통 성분이 있는데 I_cut ≤ 0 — 수치 실패 (위상 서술 아님)
        r_ = rec['sv_counterfactual_ratio']
        if thr is not None and r_ is not None and r_ >= thr:
            rec['flag'] = 'SV_DEPENDENT'
        return rec
