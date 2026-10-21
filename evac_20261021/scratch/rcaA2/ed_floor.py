p = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1ea4b71aa06a03ee/scripts/test_carbon_junction.py'
s = open(p, encoding='utf-8').read()


def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80])
    s = s.replace(old, new)


rep('''    In = (rn or {}).get('instances') or {}
    sn = [float(In['s'][q_]) for q_ in range(len(In.get('fi', []))) if In['self'][q_]]
    D_ = 2.0 * RF + TOL
    chk('KINK s_min 없음 + 시험 모드 = 진행 · 거르기 안 함 표지 (self_filter = off_s_min_missing) · 교차 접합 (s 10.8) 이 그 안에 · '
        '바닥 = 모든 자기 접합 s > D (곧은 이웃 쌍 아님)',
        pt is not None and not pt['rejections'] and rn['census'].get('self_filter') == 'off_s_min_missing'
        and any(abs(x - XC_S) < 1e-9 for x in sn) and all(x > D_ for x in sn), f'{sn}')''',
    '''    In = (rn or {}).get('instances') or {}
    sn = [(float(In['s'][q_]), float(In['d0'][q_])) for q_ in range(len(In.get('fi', []))) if In['self'][q_]]
    D_ = 2.0 * RF + TOL
    chk('KINK s_min 없음 + 시험 모드 = 진행 · 거르기 안 함 표지 (self_filter = off_s_min_missing) · 교차 접합 (s 10.8) 이 그 안에 · '
        '바닥 = 모든 자기 접합 s > D · s > (π/2)·d0 (곧은 이웃 · 꺾임 모서리 아님)',
        pt is not None and not pt['rejections'] and rn['census'].get('self_filter') == 'off_s_min_missing'
        and any(abs(x - XC_S) < 1e-9 for x, _ in sn) and all(x > D_ and x > 0.5 * math.pi * d for x, d in sn), f'{sn}')''')

rep('''    #       ★ 10-21 (Q-B · 쌍마다 s 규칙) — s_min 0.6 (모서리 쌍 s ≤ √2·D = 0.255 를 거른다 · s_min 0 이면 바닥 s > D (0.18) 만 걸러
    #       90° 모서리 다섯도 접합이 된다) · 머리핀 쌍 s = 2(0.44 − y) + 0.13 ≥ 0.6 → y ≤ 0.205 (닿음 L_c < L_par)''',
    '''    #       ★ 10-21 (Q-B · 쌍마다 s 규칙) — s_min 0.6 · 머리핀 쌍 s = 2(0.44 − y) + 0.13 ≥ 0.6 → y ≤ 0.205 (닿음 L_c < L_par · 간선 하나) ·
    #       90° 모서리 쌍은 바닥 (s > D · s > (π/2)·d — 모서리 s ≤ √2·d) 이 어느 s_min 에서도 거른다''')

rep('''# ═════════════════════════ FP — 지문 재현 (RINT-23''',
    '''FL_N = (6, 3, 8)
FL_L = [[(1.5, 1.5, 0.5), (1.5, 1.5, 4.5), (4.5, 1.5, 4.5)]]            # 90° 모서리 하나
FL_V = [[(1.5, 1.5, 0.5), (1.5, 1.5, 6.5), (2.3, 1.5, 0.5)]]            # 날카로운 V (꼭짓각 7.6° · 두 팔이 D 안)


def _floor_case(poly, smin):
    P = rows(poly)
    sid, _ = bed(P, FL_N)
    reg = registry(sid, P, s_min_um=smin)
    I = reg['instances']
    return reg, [(float(I['s'][q]), float(I['d0'][q])) for q in range(len(I['fi'])) if I['self'][q]]


@case('FLOOR')
def t_self_floor():
    """★ 10-21 (사전 리뷰 PRE-impl-02 · 1저자 Q-B) — 같은 조각 쌍의 바닥 = s > D 그리고 s > (π/2)·d: 곧은 이웃 (s = d) · 꺾임 모서리
    (꼭짓각 θ ≥ 79° 이면 s/d ≤ 1/sin(θ/2) ≤ π/2) 는 어떤 s_min 에서도 접합 후보가 아니다 · 반원 굽힘 (s = (π/2)·d) 이 경계.
    s_min 없음 (S0 census) · s_min 0 에서도 L 자 = 후보 0 · V 자 (꼭짓각 7.6°) = 후보 ≥ 1 · 모든 자기 instance s > D · s > (π/2)·d0."""
    D_ = 2.0 * RF + TOL
    for nm, poly, smin, want0 in (('L 자 · s_min 없음', FL_L, None, True), ('L 자 · s_min 0', FL_L, 0.0, True),
                                 ('V 자 · s_min 없음', FL_V, None, False), ('V 자 · s_min 0', FL_V, 0.0, False)):
        out = _try(lambda poly=poly, smin=smin: _floor_case(poly, smin), None)
        reg, sv = out if out is not None else (None, [])
        c = (reg or {}).get('census') or {}
        if want0:
            ok = reg is not None and len(sv) == 0 and c.get('n_self_candidates') == 0
        else:
            ok = reg is not None and len(sv) >= 1 and all(s_ > D_ and s_ > 0.5 * math.pi * d_ for s_, d_ in sv)
        chk(f'FLOOR {nm} — ' + ('자기 후보 0 · instance 0 (90° 모서리 = 바닥 안)' if want0 else
                                '자기 instance ≥ 1 · 모두 s > D · s > (π/2)·d0'), ok, f'{sv} · 후보 {c.get("n_self_candidates")}')


# ═════════════════════════ FP — 지문 재현 (RINT-23''')

rep('''    def ring_ok():
        sid, _ = bed(rows([RING]), RING_N)
        I = _try(lambda: I_of(solve(sid, sig_e(), RING_N, plan(registry(sid, rows([RING])), rj)), RING_N))
        return rel(I, _graph_ref(_cells_of_pts(densify(RING)), RING_N)) < 1e-12
''',
    '''    def ring_ok():
        sid, _ = bed(rows([RING]), RING_N)
        I = _try(lambda: I_of(solve(sid, sig_e(), RING_N, plan(registry(sid, rows([RING])), rj)), RING_N))
        return rel(I, _graph_ref(_cells_of_pts(densify(RING)), RING_N)) < 1e-12

    def floor_ok():
        out = _try(lambda: _floor_case(FL_L, None), None)
        return out is not None and out[0]['census'].get('n_self_candidates') == 0 and not out[1]
''')

rep('''        ('고리 이음매 별칭 끔 → 이음매 첫 · 끝 위치가 따로 (고리가 끊긴다)', '_ring_alias', lambda cu, is_ring: False, ring_ok),
    )''',
    '''        ('고리 이음매 별칭 끔 → 이음매 첫 · 끝 위치가 따로 (고리가 끊긴다)', '_ring_alias', lambda cu, is_ring: False, ring_ok),
        ('바닥 = s > D 만 ((π/2)·d 없음) → L 자 90° 모서리가 자기 후보', '_self_floor', lambda s_, d_, D_: s_ > D_, floor_ok),
    )''')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
