p = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1ea4b71aa06a03ee/scripts/test_carbon_junction.py'
s = open(p, encoding='utf-8').read()


def rep(old, new):
    global s
    assert s.count(old) == 1, (s.count(old), old[:80])
    s = s.replace(old, new)


rep('''    chk('RCA03 (가) 기록 — 자기 후보 1 · 거른 수 1 · 경로로만 이은 재방문 쌍 4 (합친 수 칸 없음 · 0)',
        cen.get('n_self_candidates') == 1 and cen.get('n_self_filtered') == 1 and cen.get('n_self_revisits_path_only') == 4
        and not cen.get('n_self_merged_revisits'), f'{ {k: cen.get(k) for k in ("n_self_candidates", "n_self_filtered", "n_self_revisits_path_only", "n_self_merged_revisits")} }')''',
    '''    #  ★ 10-21 (Q-B) — 후보 = 바닥 (s > D) 쌍 무리 (머리핀 + 모서리 · 수는 기하) → 남은 0 · 거른 수 = 후보 수 · 재방문 넷 = 경로로만
    chk('RCA03 (가) 기록 — 자기 후보 ≥ 1 · 남은 0 · 거른 수 = 후보 수 · 경로로만 이은 재방문 쌍 4 (합친 수 칸 없음 · 0)',
        (cen.get('n_self_candidates') or 0) >= 1 and cen.get('n_self_kept') == 0
        and cen.get('n_self_filtered') == cen.get('n_self_candidates') and cen.get('n_self_revisits_path_only') == 4
        and not cen.get('n_self_merged_revisits'), f'{ {k: cen.get(k) for k in ("n_self_candidates", "n_self_kept", "n_self_filtered", "n_self_revisits_path_only", "n_self_merged_revisits")} }')''')
rep('''    rj = 1e3
    qs = np.flatnonzero(rl['instances']['self']) if rl is not None else []
    pc = ((_pcells(rl, int(qs[0]), 'i'), _pcells(rl, int(qs[0]), 'j')) if len(qs) == 1 else None)''',
    '''    #       ★ 10-21 (Q-B · 쌍마다 s 규칙) — s_min 0.6 (모서리 쌍 s ≤ √2·D = 0.255 를 거른다 · s_min 0 이면 바닥 s > D (0.18) 만 걸러
    #       90° 모서리 다섯도 접합이 된다) · 머리핀 쌍 s = 2(0.44 − y) + 0.13 ≥ 0.6 → y ≤ 0.205 (닿음 L_c < L_par)
    rj = 1e3
    rl6 = _try(lambda: _rc_reg(sid, P, 0.6), None)
    qs = np.flatnonzero(rl6['instances']['self']) if rl6 is not None else []
    pc = ((_pcells(rl6, int(qs[0]), 'i'), _pcells(rl6, int(qs[0]), 'j')) if len(qs) == 1 else None)''')
rep('''    Ij = _try(lambda: I_of(solve(sid, sig_e(), RC_N, plan(rl, rj), vox=RC_H), RC_N, vox=RC_H))''',
    '''    Ij = _try(lambda: I_of(solve(sid, sig_e(), RC_N, plan(rl6, rj), vox=RC_H), RC_N, vox=RC_H))''')
rep('''    rsl = _try(lambda: _rc_reg(sids, Ps, 0.0, tol_sj_um=RC_TOL, r_sdcp_um=0.15), None)''',
    '''    rsl = _try(lambda: _rc_reg(sids, Ps, 0.6, tol_sj_um=RC_TOL, r_sdcp_um=0.15), None)''')
rep('''    #  (바) 다른 셀 자기 접근 (KU) · c = 1 — SDCP 두 점이 분산 간선 둘의 접점 옆 → 둘 다 축약 (면 셋 절단 그대로)
    sdk = rows([[(1.9, 0.5, 1.75)], [(1.9, 0.5, 3.25)]], phase=5, kind=0, fid0=700)
    Pk = cat_rows(rows(KU), sdk)
    sidk, _ = bed(Pk, KU_N)
    seqk = seq_cells(KU[0])
    ixk = {c: seqk.index(c) for c in seqk}
    rk = _try(lambda: registry(sidk, Pk, s_min_um=KU_S - 0.5, tol_sj_um=0.6, r_sdcp_um=0.5), None)
    rkc = _try(lambda: solve(sidk, sig_e(), KU_N, plan(rk, 1e3, sdcp_mod={'c': 1.0})), None)
    I_k = chain_ref(len(seqk), merge=[(ixk[(1, 1, 1)], ixk[(2, 1, 1)]), (ixk[(1, 1, 3)], ixk[(2, 1, 3)])])
    chk('RCA03 (바) 다른 셀 자기 접근 (U 자) · c = 1 — 분산 간선 둘 다 근접 → 둘 다 축약 · 면 셋 절단 (손 회로 1e-12)',
        rkc is not None and (rkc.get('cjunc') or {}).get('n_contracted') == 2 and rel(I_of(rkc, KU_N), I_k) < 1e-12,
        f"{None if rkc is None else ((rkc.get('cjunc') or {}).get('n_contracted'), I_of(rkc, KU_N))} ↔ {I_k}")
    rki = _try(lambda: solve(sidk, sig_e(), KU_N, plan(rk, math.inf, allow_rj_limits=True)), None)
    chk('RCA03 (바) 다른 셀 자기 접근 · R_j = ∞ → 면 셋 절단 · 간선 없음 → 사슬 그대로 (1e-12)',
        rki is not None and rel(I_of(rki, KU_N), chain_ref(len(seqk))) < 1e-12)''',
    '''    #  (바) 다른 셀 자기 접근 · c = 1 — ★ 10-21 (Q-B) 꼴 = XC (교차 접점 (1.9,1.5,2.5) · 옛 KU 는 쌍마다 s 규칙에서 경계 꼴) · SDCP 점 하나가
    #       (0,1,2) (다리 1 셀 (1,1,2) 옆 빈 셀 = 매달린 셀 · 다른 VGCF 셀과 면을 안 나눈다) · 근접 (중심 ↔ 간선 접점 1.4 − r 0.5 ≤ tol 1.0) →
    #       교차 자기 접합 축약 · 면 (1,1,2)|(2,1,2) 절단 그대로 (손 회로 = 그 두 노드 합침)
    sdk = rows([[(0.5, 1.5, 2.5)]], phase=5, kind=0, fid0=700)
    Pk = cat_rows(rows(XC), sdk)
    sidk, _ = bed(Pk, XC_N)
    seqk = seq_cells(XC[0])
    ixk = {c: seqk.index(c) for c in seqk}
    rk = _try(lambda: registry(sidk, Pk, s_min_um=5.0, tol_sj_um=1.0, r_sdcp_um=0.5), None)
    rkc = _try(lambda: solve(sidk, sig_e(), XC_N, plan(rk, 1e3, sdcp_mod={'c': 1.0})), None)
    I_k = chain_ref(len(seqk), merge=[(ixk[(1, 1, 2)], ixk[(2, 1, 2)])])
    chk('RCA03 (바) 다른 셀 자기 접근 (교차) · c = 1 — 근접 자기 접합 축약 1 · 면 절단 (손 회로 1e-12)',
        rkc is not None and (rkc.get('cjunc') or {}).get('n_contracted') == 1 and rel(I_of(rkc, XC_N), I_k) < 1e-12,
        f"{None if rkc is None else ((rkc.get('cjunc') or {}).get('n_contracted'), I_of(rkc, XC_N))} ↔ {I_k}")
    rki = _try(lambda: solve(sidk, sig_e(), XC_N, plan(rk, math.inf, allow_rj_limits=True)), None)
    chk('RCA03 (바) 다른 셀 자기 접근 · R_j = ∞ → 면 절단 · 간선 없음 → 사슬 그대로 (1e-12)',
        rki is not None and rel(I_of(rki, XC_N), chain_ref(len(seqk))) < 1e-12)''')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
