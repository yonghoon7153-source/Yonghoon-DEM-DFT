p = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1ea4b71aa06a03ee/scripts/test_carbon_junction.py'
s = open(p, encoding='utf-8').read()


def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80])
    s = s.replace(old, new)


rep('''    chk('RCA06 주 해 미수렴 → 반사실 비 없음 (status main_unconverged · 비 None · 표지 None · 해 unconverged True)',
        r_u is not None and r_u.get('unconverged') is True and cu.get('status') == 'main_unconverged'
        and cu.get('sv_counterfactual_ratio') is None and cu.get('flag') is None, f"{None if r_u is None else r_u.get('unconverged')} {cu}")''',
    '''    #  ★ 10-21 (Q-D) — 미수렴 기록의 종류도 원장 정본 상수 (반사실 = SV 다리만 끊음 · 옛 'counterfactual_cut_sv_faces' 문자열 고정 아님)
    chk('RCA06 주 해 미수렴 → 반사실 비 없음 (status main_unconverged · 비 None · 표지 None · 해 unconverged True · 종류 = CJUNC_SV_CF_KIND)',
        r_u is not None and r_u.get('unconverged') is True and cu.get('status') == 'main_unconverged'
        and cu.get('sv_counterfactual_ratio') is None and cu.get('flag') is None
        and cu.get('kind') == getattr(CJ, 'CJUNC_SV_CF_KIND', None), f"{None if r_u is None else r_u.get('unconverged')} {cu}")''')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
