p = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1ea4b71aa06a03ee/scripts/test_ca_s0_census.py'
s = open(p, encoding='utf-8').read()


def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80])
    s = s.replace(old, new)


rep('''J_LC_PAR = 1.0 + 2.0 * math.sqrt(0.15 ** 2 - 0.12 ** 2)''',
    '''J_LC_PAR = 1.0 + 2.0 * math.sqrt(0.15 ** 2 - 0.12 ** 2)
#: ★ 10-21 (사전 리뷰 PRE-impl-02 · 1저자 Q-B) — 자기 접합 = 같은 조각 중심선 쌍 (d ≤ D) · 바닥 (s > D · s > (π/2)·d — 곧은 이웃 · 꺾임
#   모서리 아님) · S0 = s_min 없음 (바닥 쌍 전부) · L_c = 그 쌍들의 닿음 (중심선 · 셀 조각 아님).  U 자 (KU × 0.15 · 다리 1 x 1.5 · 다리 2
#   (2.5, 4.5) → (2.3, 1.5) 13 등분 · KU 단위 T = 2 r_f / 0.15 = 1 · D = 1.125): 다리 1 쪽 닿음 = z 0.9 (다리 2 아래끝 (2.3, 1.5) 까지 1) …
#   z* (다리 1 맨 위 선분이 바닥을 지나는 짝 = 다리 2 둘째 선분 · 그 위끝 (2.5 − 0.2/13, 4.5 − 3/13) 까지 1 · 첫 선분 짝은 s < (π/2)·d 라
#   바닥 밖) → L_c = 0.15 (z* − 0.9) · 다리 2 쪽 (둘째 선분부터 + 아래 가로 0.2) 은 더 짧다.  (옛 = 면 항목 셀 조각 0.45)
_J_X2 = 2.5 - 0.2 / 13.0
_J_Z2 = 4.5 - 3.0 / 13.0
J_KU_LC = J_H * (_J_Z2 + math.sqrt(1.0 - (_J_X2 - 1.5) ** 2) - 0.9)''')

rep('''    chk('R4 손계산 — U 자 섬유 (KU × 0.15) → 자기 후보 1 · s = 0.15 (4 + √9.04) = %.6f · 자기 L_c 0.45 · 배율 1.5 · '
        '거르지 않음 (s_min 미등록 · 거른 수 0)' % J_KU_S,
        len(sc) == 1 and close(sc[0].get('s_um'), J_KU_S, 1e-9) and close(sc[0].get('Lc_um'), 0.45, 1e-9)
        and close(sc[0].get('mult'), 1.5, 1e-9) and cen.get('n_self_candidates') == 1 and cen.get('n_self_filtered') == 0
        and cen.get('self_filter') == 'off_s_min_missing', str(sc))
    lc = jc.get('long_contacts') or []
    want_sum = J_LC_PAR / 0.30 + 1.5''',
    '''    chk('R4 손계산 — U 자 섬유 (KU × 0.15) → 자기 후보 1 · s = 0.15 (4 + √9.04) = %.6f · 자기 L_c = 중심선 닿음 %.9f (★ 10-21 · 옛 '
        '셀 조각 0.45) · 배율 L_c/0.30 · 거르지 않음 (s_min 미등록 · 거른 수 0)' % (J_KU_S, J_KU_LC),
        len(sc) == 1 and close(sc[0].get('s_um'), J_KU_S, 1e-9) and close(sc[0].get('Lc_um'), J_KU_LC, 1e-9)
        and close(sc[0].get('mult'), J_KU_LC / 0.30, 1e-9) and cen.get('n_self_candidates') == 1
        and cen.get('n_self_filtered') == 0 and cen.get('self_filter') == 'off_s_min_missing', str(sc))
    lc = jc.get('long_contacts') or []
    want_sum = J_LC_PAR / 0.30 + J_KU_LC / 0.30''')

rep('''    chk('R8 같은 셀 비연속 재방문 (판정문 RCA-03 고리) — 쌍 4 · 셀 4 · 섬유 1 · s 분포 (재방문 든 자기 후보 1 · 유한) · 원장 census 와 '
        '보고 블록 같은 값',
        cen.get('n_revisit_pairs') == 4 and cen.get('n_revisit_cells') == 4 and cen.get('n_revisit_fibres') == 1
        and rv.get('n_pairs') == 4 and rv.get('n_cells') == 4 and rv.get('n_fibres') == 1
        and (rv.get('s_um') or {}).get('n') == 1 and math.isfinite(float((rv.get('s_um') or {}).get('min', math.nan))),''',
    '''    #  ★ 10-21 (Q-B) — 재방문 s = 그 쌍 (같은 조각 · 같은 셀 두 가지) 의 경로 호 간격 (쌍마다 4 · 옛 = 재방문 든 자기 후보마다 1)
    chk('R8 같은 셀 비연속 재방문 (판정문 RCA-03 고리) — 쌍 4 · 셀 4 · 섬유 1 · s 분포 (쌍마다 4 · 유한 · 양수) · 원장 census 와 '
        '보고 블록 같은 값',
        cen.get('n_revisit_pairs') == 4 and cen.get('n_revisit_cells') == 4 and cen.get('n_revisit_fibres') == 1
        and rv.get('n_pairs') == 4 and rv.get('n_cells') == 4 and rv.get('n_fibres') == 1
        and (rv.get('s_um') or {}).get('n') == 4 and math.isfinite(float((rv.get('s_um') or {}).get('min', math.nan)))
        and float((rv.get('s_um') or {}).get('min', 0.0)) > 0.0,''')

rep('''    sub = jc.get('subedges') or {}
    chk('R8 긴 접촉 · 분산 간선 — 긴 instance 1 (L_c %.4f · k 7) · 간선 9 (자기 1 + 7 + T1-11 꼴 1) · 긴 접촉 간선 7' % RV_LC,
        jc.get('n_long') == 1 and sub.get('n') == 9 and sub.get('n_long') == 7 and cen.get('n_subedges') == 9, str(sub))''',
    '''    sub = jc.get('subedges') or {}
    zq = np.load(os.path.join(out, 's0_junctions_kit_RV.npz')) if os.path.exists(os.path.join(out, 's0_junctions_kit_RV.npz')) else None
    #  ★ 10-21 (Q-B) — 자기 후보 (머리핀) 의 L_c = 중심선 닿음 (S0 = s_min 없음 · 바닥 쌍 전부 — 옛 셀 조각보다 길다 · k 는 원장 값) →
    #    간선 수 = Σ k (나란한 쌍 7 + T1-11 꼴 1 + 자기 k_s) · 긴 접촉 = 나란한 쌍 + (자기 L_c > L_par 이면 자기)
    ks = int(np.asarray(zq['nsub'])[np.asarray(zq['is_self'], bool)].sum()) if zq is not None else -1
    n_self = int(np.sum(np.asarray(zq['is_self'], bool))) if zq is not None else -1
    ls = int(np.sum(np.asarray(zq['long'], bool) & np.asarray(zq['is_self'], bool))) if zq is not None else -1
    chk('R8 긴 접촉 · 분산 간선 — 나란한 쌍 긴 instance (L_c %.4f · k 7) · 자기 후보 1 (k_s ≥ 1) · 간선 = 7 + 1 + k_s · 긴 접촉 간선 = '
        '7 + (자기가 길면 k_s)' % RV_LC,
        n_self == 1 and ks >= 1 and jc.get('n_long') == 1 + ls and sub.get('n') == 8 + ks
        and sub.get('n_long') == 7 + (ks if ls else 0) and cen.get('n_subedges') == 8 + ks, f'{sub} · 자기 {n_self} k {ks} 긴 {ls}')''')

rep('''    chk('R8 npz — 간선별 배열 (instance 번호 · PTFE 덮임 · SDCP 근접 · 실현) · S0-2 σ · 전류 · 소산 칸 없음',
        z is not None and {'sub_inst', 'sub_ptfe_cov', 'sub_a_sdcp', 'sub_realized'} <= set(z.files)
        and int(np.sum(z['sub_ptfe_cov'])) == 1 and len(z['sub_inst']) == 9''',
    '''    chk('R8 npz — 간선별 배열 (instance 번호 · PTFE 덮임 · SDCP 근접 · 실현) · S0-2 σ · 전류 · 소산 칸 없음',
        z is not None and {'sub_inst', 'sub_ptfe_cov', 'sub_a_sdcp', 'sub_realized'} <= set(z.files)
        and int(np.sum(z['sub_ptfe_cov'])) == 1 and len(z['sub_inst']) == 8 + ks''')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
