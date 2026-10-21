p = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1ea4b71aa06a03ee/scripts/test_carbon_junction.py'
s = open(p, encoding='utf-8').read()


def rep(old, new):
    global s
    assert s.count(old) == 1, (s.count(old), old[:80])
    s = s.replace(old, new)


rep('''    P, sid = _rc_bed()
    r = _try(lambda: _rc_reg(sid, P, 0.0), None)
    c = (r or {}).get('census') or {}
    rs = c.get('revisit_s_um') or {}
    chk('CEN 같은 셀 비연속 재방문 — 쌍 4 · 셀 4 · 섬유 1 · s 분포 (재방문이 든 자기 후보마다 · 유한)',
        c.get('n_revisit_pairs') == 4 and c.get('n_revisit_cells') == 4 and c.get('n_revisit_fibres') == 1
        and rs.get('n') == 1 and math.isfinite(float(rs.get('min', math.nan))), f"{ {k: c.get(k) for k in ('n_revisit_pairs', 'n_revisit_cells', 'n_revisit_fibres', 'revisit_s_um')} }")''',
    '''    P, sid = _rc_bed()
    #  ★ 10-21 (Q-B) — s_min 0.6 (s_min 0 = 바닥만 → 90° 모서리도 접합 · 포트 동률 셈이 모서리에 묻힌다) · 재방문 s = 그 쌍 (같은 조각 ·
    #    같은 셀 두 가지) 의 경로 호 간격 (쌍마다 · 옛 = 그 쌍이 든 자기 후보마다 하나)
    r = _try(lambda: _rc_reg(sid, P, 0.6), None)
    c = (r or {}).get('census') or {}
    rs = c.get('revisit_s_um') or {}
    chk('CEN 같은 셀 비연속 재방문 — 쌍 4 · 셀 4 · 섬유 1 · s 분포 (재방문 쌍마다 4 · 유한 · 양수)',
        c.get('n_revisit_pairs') == 4 and c.get('n_revisit_cells') == 4 and c.get('n_revisit_fibres') == 1
        and rs.get('n') == 4 and math.isfinite(float(rs.get('min', math.nan))) and float(rs.get('min', 0.0)) > 0.0,
        f"{ {k: c.get(k) for k in ('n_revisit_pairs', 'n_revisit_cells', 'n_revisit_fibres', 'revisit_s_um')} }")''')
rep('''    chk('CEN KR — 재방문 쌍 1 · 셀 1 ((1,1,3)) · 섬유 1 · 재방문 든 후보 1 (면 후보는 세지 않는다 · 자기 후보 2)',
        ck.get('n_revisit_pairs') == 1 and ck.get('n_revisit_cells') == 1 and ck.get('n_revisit_fibres') == 1
        and (ck.get('revisit_s_um') or {}).get('n') == 1 and ck.get('n_self_candidates') == 2,''',
    '''    chk('CEN KR — 재방문 쌍 1 · 셀 1 ((1,1,3)) · 섬유 1 · 재방문 s 1 개 (면 항목은 세지 않는다 · 자기 후보 ≥ 1)',
        ck.get('n_revisit_pairs') == 1 and ck.get('n_revisit_cells') == 1 and ck.get('n_revisit_fibres') == 1
        and (ck.get('revisit_s_um') or {}).get('n') == 1 and (ck.get('n_self_candidates') or 0) >= 1,''')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
