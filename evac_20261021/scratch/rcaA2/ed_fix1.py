p = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1ea4b71aa06a03ee/scripts/test_carbon_junction.py'
s = open(p, encoding='utf-8').read()


def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80])
    s = s.replace(old, new)


rep('''        print(f"    GAP 생산 단위 {nm}: σ {None if r is None else r['sigma_eff']} S/cm · 옛 경로 (접합 끔) {rl['sigma_eff']} · 손 I {want:.9g}")
        chk(f'GAP 생산 단위 {nm} (h 0.15 · r_f 0.075 · tol_ff 0.03 · 틈 0.12 · s_min 0.3 · R_j 1e6) — instance 1 (조각 쌍) · '
            f'σ = 손 회로 (1e-12)',
            reg is not None and len(reg['instances']['fi']) == 1 and not bool(reg['instances']['self'][0]) and rel(I, want) < 1e-12,
            f'{I} ↔ {want}')''',
    '''        print(f"    GAP 생산 단위 {nm}: σ {None if r is None else r['sigma_eff']} S/cm · 옛 경로 (접합 끔) {rl['sigma_eff']} · 손 I {want:.9g}")
        #  허용 1e-9 — 생산 단위 대비 (축 g ≈ 1.2e3 ↔ 접합 g 1e-2 · 1e5 배) 에서 직접 풀이 반올림이 ~1e-11 상대 · 구조 차이 (축 면 하나
        #  더 · 덜) = ~1e-5 상대 → 1e-9 로도 판별
        chk(f'GAP 생산 단위 {nm} (h 0.15 · r_f 0.075 · tol_ff 0.03 · 틈 0.12 · s_min 0.3 · R_j 1e6) — instance 1 (조각 쌍) · '
            f'σ = 손 회로 (1e-9 · 대비 1e5)',
            reg is not None and len(reg['instances']['fi']) == 1 and not bool(reg['instances']['self'][0]) and rel(I, want) < 1e-9,
            f'{I} ↔ {want}')''')

rep('''    leg = None
    if rs is not None:
        Is = rs['instances']
        cand = [q for q in range(len(Is['fi'])) if Is['self'][q] and _pcells(rs, q, 'i') and _pcells(rs, q, 'j')
                and {_pcells(rs, q, 'i')[:2], _pcells(rs, q, 'j')[:2]} == {(1, 1), (2, 2)}]
        leg = cand[0] if len(cand) == 1 else None
    rec_s = _inst_rec(rs, leg) if leg is not None else None
    rec_d = _inst_rec(rd, 0) if (rd is not None and len(rd['instances']['fi']) == 1) else None
    chk('SELFD (ii) SFR 같은 fid (모서리 인접 다리 · 중심선 0.1414 < 2 r_f · 셀 면 공유 없음) — 다리 사이 자기 접합 하나 (옛 판 0) · '
        '기록 (L_c · 배율 · k · 분산 간선 포트 셀 · d0) = 둘로 나눈 서로 다른 섬유 instance (하나) 와 같음 (1e-12)',
        _rec_same(rec_s, rec_d), f'같은 fid {rec_s} · 나눔 {rec_d}')''',
    '''    leg = None
    if rs is not None:
        Is = rs['instances']
        cand = [q for q in range(len(Is['fi'])) if Is['self'][q]]
        leg = cand[0] if len(cand) == 1 else None
    rec_s = _inst_rec(rs, leg) if leg is not None else None
    rec_d = _inst_rec(rd, 0) if (rd is not None and len(rd['instances']['fi']) == 1) else None
    #  접점 = 최소 거리 0.1 (위 가로 (1.95, y, 3.5) 가 끝 다리 (2.05, 2.05, ·) 곁을 지나는 자리 · 셀 (1,2,3)) — 다리 둘 (0.1414) 보다 가깝다
    chk('SELFD (ii) SFR 같은 fid (모서리 인접 다리 · 중심선 0.1414 < 2 r_f · 다리 셀 면 공유 없음) — 자기 접합 하나 (옛 판 = 면 항목 셀 조각의 '
        '다른 기록) · 기록 (L_c · 배율 · k · 분산 간선 포트 셀 · d0) = 둘로 나눈 서로 다른 섬유 instance (하나) 와 같음 (1e-12)',
        _rec_same(rec_s, rec_d), f'같은 fid {rec_s} · 나눔 {rec_d}')''')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
