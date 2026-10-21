p = '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaA2/impl/step3_sigma.py'
s = open(p, encoding='utf-8').read()


def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80])
    s = s.replace(old, new)


rep('''        if _cjp.get('sv_counterfactual') is not None:      # ★ 10-21 (Codex RCA-06 · Q4 (가)) — 선택 노브: SV 면 끊은 판의 단자 G 비 (진단)
            if unconv:                                     #   주 해가 미수렴 · 증서 실패 = 비를 내지 않는다 (분자 G 를 믿을 수 없다)
                out['cjunc']['sv_counterfactual'] = {'kind': 'counterfactual_cut_sv_faces', 'requested': True,''',
    '''        if _cjp.get('sv_counterfactual') is not None:      # ★ 10-21 (Codex RCA-06 · Q4 (가)) — 선택 노브: SV 다리 끊은 판의 단자 G 비 (진단)
            if unconv:                                     #   주 해가 미수렴 · 증서 실패 = 비를 내지 않는다 (분자 G 를 믿을 수 없다)
                #  ★ 10-21 (사전 리뷰 PRE-impl-04 · Q-D) — 기록 종류 = 원장 정본 상수 (반사실 = SV 다리만 끊음 · 옛 'SV 면 전부' 와 다른 양)
                out['cjunc']['sv_counterfactual'] = {'kind': _cjm.CJUNC_SV_CF_KIND, 'rule': _cjm.CJUNC_SV_CF_RULE, 'requested': True,''')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
