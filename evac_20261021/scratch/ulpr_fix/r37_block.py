        def ut_mix(lad=LAD, **kw):
            """7:3 UT (기준 궤적 _mk_arm → _resume_mix) → (팔 판정, 선택, UVa 관문, read_run) · 만들기 · 판독 예외 = 그 예외 (시험 먼저 · 예외도 실패)."""
            try:
                shutil.rmtree(os.path.join(root, B73, 'UT'), ignore_errors=True)
                d = _mk_arm(root, B73, 'UT', {'W': 10000, 'dt': 5e-7, 'steps': _ladder(lad[0], lad[1]), 'summary': lad[3], 'events': list(lad[2])}, P)
                if kw:
                    _resume_mix(d, P, **kw)
                return arm_verdict(d, B73, 'UT', P, root=root), selection_state(root, P), gate(root, B73, 'UVa', P), read_run(d, P)
            except Exception as ex:  # noqa: BLE001
                return ex

        def ks(rr):
            return [x['k'] for x in rr['steps']]

        def k_windows(rr, k):
            return [x['w'] for x in rr['windows'] if x['k'] == k]

        def holds(r, pred):
            return not isinstance(r, Exception) and bool(pred(*r))

        def unid2(u, s, g, rr):   # 같은 꼴 fresh 판정 — 확인 단 2 없음 · 주 값 · 하한 · 점 추정 없음 · 선택 UNRESOLVED · UVa 거부
            return (u['primary_status'] == 'UNIDENTIFIED' and u['rho_pct'] is None and any('확인 단 2 없음' in w for w in u['why'])
                    and ks(rr) == [0, 1, 2, 3] and s['stage'] == 'SELECTION_UNRESOLVED' and not g[0])

        def okp(u, s, g, rr, sup):
            return (u['primary_status'] == 'OK' and abs(u['rho_pct'] - 0.2026077873428664) < 1e-12 and g[0] and ks(rr) == [0, 1, 2, 3, 4]
                    and rr['n_superseded_rows'] == sup)

        def show(r):
            if isinstance(r, Exception):
                return f'{type(r).__name__}: {r}'
            u, s, g, rr = r
            return (f'primary={u["primary_status"]} rho={u["rho_pct"]} lb={u["lower_bound_pct"]} traj={u["trajectory_status"]} k={ks(rr)} '
                    f'sup={rr["n_superseded_rows"]} ev={[(e["event"], e["k"]) for e in rr["events"]]} gate={g[0]} why={u["why"][:2]} pr={rr["problems"][:2]}')
        a0, a1, a3 = ut_mix(), ut_mix(kr=3, new_nw=2, resumed=False), ut_mix(kr=3, new_nw=2, end='GUARD', resumed=False)
        chk('R37 대조: 7:3 UT 한 시도 끝까지 (교차 k 2 · 확인 k 3 · 4 · R_M) = OK ρ 0.2026… · UVa 허용 · 같은 꼴 fresh 가 단 k 4 창 둘 뒤 TIMEOUT · GUARD = '
            'UNIDENTIFIED (확인 단 2 없음) · UVa 거부',
            lambda: holds(a0, lambda *r: okp(*r, 0)) and holds(a1, unid2) and holds(a3, unid2) and a3[0]['trajectory_status'] == 'GUARD',
            f'{show(a0)} | {show(a1)} | {show(a3)}')
        for kw, what, extra in (({'new_nw': 2}, '새 시도가 단 k 4 창 둘 뒤 TIMEOUT (옛 판 = OK ρ 0.2026… · UVa 허용)', lambda u, rr: k_windows(rr, 4) == [1, 2]),
                                ({'new_nw': 2, 'end': 'GUARD'}, '새 시도가 단 k 4 창 둘 뒤 GUARD (요약 GUARD · 옛 판 = OK · UVa 허용)',
                                 lambda u, rr: u['trajectory_status'] == 'GUARD' and k_windows(rr, 4) == [1, 2]),
                                ({'new_nw': 0}, '새 시도가 단 k 4 로 이동 중 TIMEOUT (새 창 없음 · 옛 판 = 옛 창 넷 · 단 줄 그대로 OK)', lambda u, rr: k_windows(rr, 4) == []),
                                ({'new_nw': 4}, '새 시도가 옛 시도와 같은 창 수 (넷) 뒤 단 줄 전 TIMEOUT (단 줄 ↔ 창 수 · 마지막 창 step 이 옛 · 새 둘 다와 같다)',
                                 lambda u, rr: k_windows(rr, 4) == [1, 2, 3, 4])):
            r = ut_mix(kr=3, old_nw=4, old_line=True, old_ev=True, **kw)
            chk(f'R37 ULPR-01 옛 시도 = 단 k 4 창 넷 · 단 줄 · RM 사건 뒤 요약 전 끊김 → RESUME (k 3 · s_r) → {what} → 옛 단 줄 · 창 · 사건을 쓰지 않는다 = 같은 꼴 fresh 판정 '
                '(UNIDENTIFIED · 확인 단 2 없음 · 단 k [0–3] · RM 사건 없음 · 남긴 줄 5) · UVa 거부',
                lambda r=r, extra=extra: holds(r, lambda u, s, g, rr: unid2(u, s, g, rr) and extra(u, rr) and rr['n_superseded_rows'] == 5
                                               and not any(e['event'] == 'RM' for e in rr['events'])), show(r))
        b1 = ut_mix(NOC, kr=2, new_nw=2, resumed=False)
        chk('R37 대조: 교차 전 단 (k 3) 창 둘 뒤 TIMEOUT (fresh) = LOWER_BOUND 0.225119763714296 % (k 2 = 0.25 µm) · 단 k [0–2]',
            lambda: holds(b1, lambda u, s, g, rr: u['primary_status'] == 'LOWER_BOUND' and abs(u['lower_bound_pct'] - 100 * 0.25 / h0um) < 1e-12
                          and ks(rr) == [0, 1, 2]), show(b1))
        for nn, what in ((2, '창 둘 (옛 판 = 옛 단 줄로 하한 0.27014371645715524 %)'),
                         (4, '옛 시도와 같은 창 넷 (사건 없는 단 — 단 줄이 어느 시도 것인지 기록으로 가를 수 없다)'),
                         (0, '이동 중 끝 (새 창 · 사건 없음 — 경계 뒤 줄이 어느 시도 것인지 기록으로 가를 수 없다)')):
            r = ut_mix(NOC, kr=2, old_nw=4, old_line=True, new_nw=nn)
            chk(f'R37 ULPR-01 교차 전 단 — 옛 시도 = 단 k 3 창 넷 · 단 줄 (사건 없는 단) 뒤 끊김 → RESUME (k 2) → 새 시도 {what} → 그 단 줄을 쓰지 않는다 = '
                'fresh 하한 그대로 (LOWER_BOUND 0.225119763714296 % · 단 k [0–2] · 남긴 줄 5)',
                lambda r=r: holds(r, lambda u, s, g, rr: u['primary_status'] == 'LOWER_BOUND' and not isinstance(b1, Exception)
                                  and u['lower_bound_pct'] == b1[0]['lower_bound_pct'] and ks(rr) == [0, 1, 2] and rr['n_superseded_rows'] == 5), show(r))
        pa = ut_mix(kr=1, new_nw=4, new_line=True, new_ev=True, rest=True)
        pb = ut_mix(kr=1, old_nw=2, new_nw=4, new_line=True, new_ev=True, rest=True)
        chk('R37 양성 대조: 옛 시도가 경계 뒤 아무것도 안 씀 (이동 중 끊김) · 옛 시도 창 둘만 (단 줄 · 사건 없음) → 새 시도가 단 k 2 부터 끝까지 → 주 값 OK (ρ 0.2026…) · '
            '남긴 줄 0 · 2 · UVa 허용',
            lambda: holds(pa, lambda *r: okp(*r, 0)) and holds(pb, lambda *r: okp(*r, 2)), f'{show(pa)} | {show(pb)}')
        pc = ut_mix(kr=3, old_nw=4, new_nw=4, new_line=True, new_ev=True, rest=True)
        chk('R37 양성 대조: 옛 시도 = 단 k 4 창 넷 (단 줄 전 · 다섯째 창 중 끊김) → 새 시도 = 창 넷 · 단 줄 · RM 사건 · 요약 (단 줄 ↔ 창이 옛 · 새 둘 다와 맞는다 — '
            'RESUME 뒤 새 시도 RM 사건 (그 단 끝 사건 · 같은 k · step) = 새 시도 단 줄) → 주 값 OK · 남긴 줄 4 · UVa 허용',
            lambda: holds(pc, lambda *r: okp(*r, 4)), show(pc))
        pd_, pd_f = ut_mix(NOC, kr=1, new_nw=4, new_line=True, new_state=True), ut_mix(NOC, kr=1, new_nw=4, new_line=True, new_state=True, resumed=False)
        chk('R37 양성 대조: 사건 없는 단 — 옛 시도 이동 중 끊김 → 새 시도가 단 k 2 를 끝내고 단 끝 restart · 상태 파일 (state_unload_<그 단 끝>) 뒤 k 3 이동 중 끝 '
            '(상태 파일 = 새 시도가 그 단 줄을 썼다) → 단 줄 그대로 · fresh 와 같은 하한 (k 2) · 남긴 줄 0',
            lambda: holds(pd_, lambda u, s, g, rr: holds(pd_f, lambda u2, s2, g2, rr2: u['primary_status'] == u2['primary_status'] == 'LOWER_BOUND'
                                                         and u['lower_bound_pct'] == u2['lower_bound_pct'] and ks(rr) == ks(rr2) == [0, 1, 2])
                          and rr['n_superseded_rows'] == 0), f'{show(pd_)} | {show(pd_f)}')
        pe, pe_f = ut_mix(NOC, kr=1, new_nw=4, new_line=True), ut_mix(NOC, kr=1, new_nw=4, resumed=False)
        chk('R37 시도 미확정 = 쓰지 않는다 (보수): 같은 꼴에서 단 끝 상태 파일 · 사건 · 경계 뒤 다른 단 · 창 역행이 없다 (단 줄 → restart 사이 끊김 — 옛 · 새 어느 시도 '
            '줄인지 기록으로 가를 수 없다) → 경계 뒤 줄 (창 넷 · 단 줄) 을 쓰지 않는다 = 단 k 2 단 줄이 없는 fresh 와 같은 하한 (k 1) · 남긴 줄 5',
            lambda: holds(pe, lambda u, s, g, rr: holds(pe_f, lambda u2, s2, g2, rr2: u['primary_status'] == u2['primary_status'] == 'LOWER_BOUND'
                                                        and u['lower_bound_pct'] == u2['lower_bound_pct'] and ks(rr) == ks(rr2) == [0, 1])
                          and rr['n_superseded_rows'] == 5), f'{show(pe)} | {show(pe_f)}')
        bad = ut_mix(kr=3, old_ev=True, new_nw=4, new_line=True, new_ev=True, rest=True)
        chk('R37 ULPR-01 모순: RESUME 앞에 경계 뒤 옛 사건 (RM) 이 있는데 옛 시도 창이 없다 (창 역행 없음) · 새 시도 기록은 있다 → 버리지 · 고르지 않고 주 값 미식별 '
            '(사유 ULPR-01) · UVa 거부',
            lambda: holds(bad, lambda u, s, g, rr: u['primary_status'] != 'OK' and u['rho_pct'] is None and any('ULPR-01' in w for w in u['why']) and not g[0]),
            show(bad))

        def gap_case():
            r = ut_mix(kr=1, old_nw=2, new_nw=4, new_line=True, new_ev=True, rest=True)
            if isinstance(r, Exception):
                return r
            d = r[3]['dir']
            try:
                _edit_rows(os.path.join(d, 'ul_windows.csv'), lambda rows: rows.remove([x for x in rows if x['k'] == '3' and x['w'] == '2'][-1]))
                return arm_verdict(d, B73, 'UT', P, root=root), selection_state(root, P), gate(root, B73, 'UVa', P), read_run(d, P)
            except Exception as ex:  # noqa: BLE001
                return ex
        gv = gap_case()
        chk('R37 ULPR-01 경계 뒤 단 줄 ↔ 그 단 창 기록 (n_windows · w 1 … n · 마지막 창 step) — 새 시도 단 k 3 의 창 w 2 줄 빠짐 → 시도 섞임 · 결손 = 주 값 미식별 '
            '(사유 ULPR-01) · UVa 거부',
            lambda: holds(gv, lambda u, s, g, rr: u['primary_status'] != 'OK' and any('ULPR-01' in w for w in u['why']) and not g[0]), show(gv))

        def sep_case():
            try:
                shutil.rmtree(os.path.join(root, B73, 'UB'), ignore_errors=True)
                st = _ladder(LAD[0], LAD[1]) + [{'lift_um': 0.4, 'P': 0.3, 'steady': True, 'nw': 4, 'kind': 'B', 'phase': 2, 'modeB': 1, 'n_move': 0},
                                                {'lift_um': 0.45, 'P': 0.2, 'steady': True, 'nw': 4, 'kind': 'B', 'phase': 2, 'modeB': 1, 'n_move': 0}]
                d = _mk_arm(root, B73, 'UB', {'W': 5000, 'dt': 1e-6, 'steps': st, 'summary': 'DONE', 'events': list(LAD[2])}, P)
                _resume_mix(d, P, kr=4, old_nw=2, old_events=[('SEPARATED', 2)], new_nw=4, new_line=True)
                return arm_verdict(d, B73, 'UB', P, root=root), read_run(d, P)
            except Exception as ex:  # noqa: BLE001
                return ex
        sv = sep_case()
        chk('R37 양성 대조: 분리 단 — 옛 시도 = 단 k 5 창 둘 + SEPARATED (창 사건 · 단 줄 없음) → RESUME (k 4) → 새 시도 = 창 넷 · 단 줄 (분리 없이 유지 끝) 뒤 k 6 이동 중 끝 '
            '→ 새 단 줄 그대로 (옛 창 둘 · SEPARATED 만 버림) · UB 주 값 OK',
            lambda: (not isinstance(sv, Exception) and sv[0]['primary_status'] == 'OK' and abs(sv[0]['rho_pct'] - 0.2026077873428664) < 1e-12
                     and ks(sv[1]) == [0, 1, 2, 3, 4, 5] and sv[1]['n_superseded_rows'] == 2 and not any(e['event'] == 'SEPARATED' for e in sv[1]['events'])),
            (f'{type(sv).__name__}: {sv}' if isinstance(sv, Exception) else
             f'{sv[0]["primary_status"]} k={ks(sv[1])} sup={sv[1]["n_superseded_rows"]} pr={sv[1]["problems"][:2]} why={sv[0]["why"][:2]}'))
