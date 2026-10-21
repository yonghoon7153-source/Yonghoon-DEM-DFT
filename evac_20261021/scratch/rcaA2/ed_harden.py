p = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1ea4b71aa06a03ee/scripts/test_carbon_junction.py'
s = open(p, encoding='utf-8').read()


def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80])
    s = s.replace(old, new)


# (1) KINK — KU s_min 없음: 자기 L_c = 접합 쌍 (바닥 쌍) 의 닿음만 (변이 M10 '두 쪽 선분 전부 짝' 을 가른다)
rep('''    chk('KINK KU (U 자 · 쌍 s 전부 < 20) s_min 20 — 자기 접합 0 · σ = 옛 경로 (면 셋 융합 · 1e-12)',
        rk is not None and int(np.sum(rk['instances']['self'])) == 0 and rel(Ik, I_of(solve_legacy(sidk, sig_e(), KU_N), KU_N)) < 1e-12,
        f'{Ik}')''',
    '''    chk('KINK KU (U 자 · 쌍 s 전부 < 20) s_min 20 — 자기 접합 0 · σ = 옛 경로 (면 셋 융합 · 1e-12)',
        rk is not None and int(np.sum(rk['instances']['self'])) == 0 and rel(Ik, I_of(solve_legacy(sidk, sig_e(), KU_N), KU_N)) < 1e-12,
        f'{Ik}')
    #  ★ 10-21 (변이 시험 다지기 · M10) — s_min 없음 (바닥 쌍 = 접합 쌍) · U 자기 접합 하나 · L_c = 그 쌍들의 닿음만: 다리 1 쪽 = z 0.9 (다리 2
    #    아래끝 (2.3, 1.5) 까지 1) … z* = 다리 1 맨 위 선분이 바닥을 지나는 짝 (다리 2 둘째 선분 · 위끝 (2.5 − 0.2/13, 4.5 − 3/13) 까지 1) —
    #    다리 2 첫 선분 짝은 바닥 밖 (s 1.46 < (π/2)·0.985) 인데 닿는다 (거리 0.985 ≤ 1) → 두 쪽 선분 전부를 짝으로 쓰면 z 4.5 까지 (L_c 3.6)
    rkn = _try(lambda: registry(sidk, PK, s_min_um=None), None)
    Ikn = (rkn or {}).get('instances') or {}
    qn = [q_ for q_ in range(len(Ikn.get('fi', []))) if Ikn['self'][q_]]
    ku_lc = (4.5 - 3.0 / 13.0) + math.sqrt(1.0 - (2.5 - 0.2 / 13.0 - 1.5) ** 2) - 0.9
    chk('KINK KU s_min 없음 — U 자기 접합 하나 · s = KU_S · L_c = 접합 쌍의 닿음만 = 손 값 %.9f (1e-9 · 두 쪽 선분 전부 짝 = 3.6)' % ku_lc,
        len(qn) == 1 and abs(float(Ikn['s'][qn[0]]) - KU_S) < 1e-9 and abs(float(Ikn['Lc'][qn[0]]) - ku_lc) < 1e-9,
        f"{qn} {None if len(qn) != 1 else (float(Ikn['s'][qn[0]]), float(Ikn['Lc'][qn[0]]))} ↔ {KU_S} · {ku_lc}")''')

# (2) RING — 이음매가 다리 가운데인 닫힌 머리핀: 이음매를 지나는 접합 쌍 = 한 무리 (변이 M12 '쌍 무리 둘레 잇기 끔' = 둘)
rep('''    chk('RING 틈 하나 — σ = 손 회로 (연속 이음매 + 틈 R_j 간선 · 1e-12) · R_j = ∞ = 틈에서 열린 가닥 (1e-12)',
        rg is not None and rgi is not None and rel(I_of(rg, RING_N), wg) < 1e-12 and rel(I_of(rgi, RING_N), wgi) < 1e-12,
        f"{None if rg is None else I_of(rg, RING_N)} ↔ {wg} · {None if rgi is None else I_of(rgi, RING_N)} ↔ {wgi}")''',
    '''    chk('RING 틈 하나 — σ = 손 회로 (연속 이음매 + 틈 R_j 간선 · 1e-12) · R_j = ∞ = 틈에서 열린 가닥 (1e-12)',
        rg is not None and rgi is not None and rel(I_of(rg, RING_N), wg) < 1e-12 and rel(I_of(rgi, RING_N), wgi) < 1e-12,
        f"{None if rg is None else I_of(rg, RING_N)} ↔ {wg} · {None if rgi is None else I_of(rgi, RING_N)} ↔ {wgi}")
    #  ★ 10-21 (변이 시험 다지기 · M12) — 닫힌 머리핀 (다리 둘 0.8 · 닿음) 의 이음매 = 다리 1 가운데 (z 3.5): 다리 사이 접합 쌍은 이음매 앞 · 뒤
    #    선분 번호로 갈리지만 고리 둘레로 이웃 → 접촉 하나 = 자기 instance 하나 (둘레 잇기를 끄면 둘)
    RH = [(1.5, 1.5, 3.5), (1.5, 1.5, 6.5), (2.3, 1.5, 6.5), (2.3, 1.5, 0.5), (1.5, 1.5, 0.5), (1.5, 1.5, 3.5)]
    Ph = rows([RH])
    sidh, _ = bed(Ph, RING_N)
    regh = _try(lambda: registry(sidh, Ph, s_min_um=S_MIN), None)
    Ih_ = (regh or {}).get('instances') or {}
    nh = int(np.sum(Ih_['self'])) if regh is not None else -1
    chk('RING 닫힌 머리핀 (이음매 = 다리 가운데) — 고리 조각 1 · 다리 사이 자기 접합 = 하나 (이음매를 지나는 쌍 무리 · 고리 둘레 이웃)',
        regh is not None and regh['census'].get('n_ring_pieces') == 1 and nh == 1,
        f"{None if regh is None else regh['census'].get('n_ring_pieces')} · 자기 {nh}")''')

# (3) CEN — 재방문 두 가지 사이 위치가 덮이면 '경로로만' 아님 (경로 끊김) (변이 M27 '경로 끊김 검사 끔')
rep('''    t11 = _try(lambda: _solve_full(rows_exact([T4_A, T4_B]), T4_N), None)
    ct = (t11[1]['census'] if t11 is not None else {})''',
    '''    #  ★ 10-21 (사전 리뷰 PRE-impl-01 '경로로만 = 실제로 이어진 경로가 있을 때만' · 변이 시험 다지기 M27) — 같은 KR 에 SDCP 점이 두 가지
    #    사이 위치 (2,1,4) 를 덮으면 재방문 쌍은 경로로 안 이어진다 → 경로 끊김 1 · 경로로만 0 (접합 없음 · s_min 10)
    Pkb = cat_rows(rows(KR), rows([[(2.5, 1.5, 4.5)]], phase=5, kind=0, fid0=700))
    sidkb, _ = bed(Pkb, KR_N)
    rkb = _try(lambda: registry(sidkb, Pkb, s_min_um=10.0), None)
    ckb = (rkb or {}).get('census') or {}
    chk('CEN KR + SDCP 가 두 가지 사이 위치 (2,1,4) 를 덮음 — 재방문 쌍 1 · 경로 끊김 1 · 경로로만 0 (덮인 위치 = 경로 아님)',
        int(sidkb[2, 1, 4]) == 5 and ckb.get('n_revisit_pairs') == 1 and ckb.get('n_self_revisits_path_broken') == 1
        and ckb.get('n_self_revisits_path_only') == 0,
        f"{int(sidkb[2, 1, 4])} { {k: ckb.get(k) for k in ('n_revisit_pairs', 'n_self_revisits_path_broken', 'n_self_revisits_path_only')} }")
    t11 = _try(lambda: _solve_full(rows_exact([T4_A, T4_B]), T4_N), None)
    ct = (t11[1]['census'] if t11 is not None else {})''')

rep('''  FLOOR  (Q-B) 같은 조각 쌍의 바닥 = s > D · s > (π/2)·d — L 자 90° 모서리 = 어느 s_min (없음 · 0) 에서도 자기 후보 0 · 날카로운 V = 후보''',
    '''  FLOOR  (Q-B) 같은 조각 쌍의 바닥 = s > D · s > (π/2)·d — L 자 90° 모서리 = 어느 s_min (없음 · 0) 에서도 자기 후보 0 · 날카로운 V = 후보
  (변이 시험 다지기 · 10-21) KINK KU s_min 없음 L_c 손 값 (자기 L_c = 접합 쌍만) · RING 닫힌 머리핀 = 자기 하나 (쌍 무리 고리 둘레) ·
         CEN 재방문 사이 덮인 위치 = 경로 끊김 (경로로만 아님)''')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
