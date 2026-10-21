p = '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaA2/impl/ca_ext_cjunc.py'
s = open(p, encoding='utf-8').read()


def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80])
    s = s.replace(old, new)


rep('''★ Z3 (10-20) — face_alpha (S1) + cjunc (S2) 한 런 = 받는다 (설계 §3 · §4 조합 규칙 · 등록 R §10 꼴 · B6 통합 때의 임시 거부를 뺐다) ·
  P1 (덮인 접합 절단) = face_alpha 에서만 · centerline + P1 · off + P1 = 거부 그대로.''',
    '''★ Z3 (10-20) — face_alpha (S1) + cjunc (S2) 한 런 = 받는다 (설계 §3 · §4 조합 규칙 · 등록 R §10 꼴 · B6 통합 때의 임시 거부를 뺐다) ·
  P1 (덮인 접합 절단) = face_alpha 에서만 · off + P1 = 거부 그대로.
★ 10-21 (사전 리뷰 PRE-impl-03 · 1저자 Q-C) — 접합 + ptfe_stamp centerline = 거부 (P0 도 · protocol 정본 · 검증기 `cjunc_block_problem` 이 같은
  함수로 다시 만든다): centerline 은 VGCF 셀을 sid 7 로 덮어 옛 판은 덮인 접점의 포트를 옆 셀로 옮겨 절연체를 더해 σ 가 올랐다 (Rayleigh
  위반) · 원장은 이제 덮인 접점을 옮기지 않지만 PTFE 법칙 (P0 · P1) 은 face_alpha 표현에서만 정의된다 · payload · 러너의 거부 코드 = 그 쪽 몫.''')

rep('''    """`ca_ext.cjunc.protocol` — 물리 칸 (p3ca id 에 들어간다).  선언 값 여섯 + 이 코드의 상수 (모델 판 · 규칙 판 · 고정 문턱).
    정량 (R_j 유한 > 0 · s_min 등록 · tol_ff 유한 ≥ 0) 또는 ★ Z3 극한 런 (`rj_limit` — `rj_limit_value`) · ptfe_stamp = off · centerline ·
    face_alpha (Z3 — 조합 받음) · P1 = face_alpha 에서만 (centerline 은 이미 VGCF 셀을 sid 7 로 자른다 · off 는 PTFE 표현이 없다)."""''',
    '''    """`ca_ext.cjunc.protocol` — 물리 칸 (p3ca id 에 들어간다).  선언 값 여섯 + 이 코드의 상수 (모델 판 · 규칙 판 · 고정 문턱).
    정량 (R_j 유한 > 0 · s_min 등록 · tol_ff 유한 ≥ 0) 또는 ★ Z3 극한 런 (`rj_limit` — `rj_limit_value`) · ptfe_stamp = off · face_alpha
    (Z3 — 조합 받음 · ★ 10-21 Q-C centerline = 거부) · P1 = face_alpha 에서만 (off 는 PTFE 표현이 없다)."""''')

rep('''    if ptfe_stamp not in ('off', 'centerline', 'face_alpha'):
        raise ValueError(f'ptfe_stamp = {ptfe_stamp!r} — 접합 (S2) 은 off · centerline · face_alpha 에서만 (capsule = 예약값)')
    if ptfe_jlaw == 'P1' and ptfe_stamp != 'face_alpha':
        raise ValueError(f'PTFE–접합 법칙 P1 (덮인 접합 절단) 은 face_alpha 에서만 ({ptfe_stamp} — centerline 은 이미 VGCF 셀을 sid 7 로 '
                         f'자른다 · off 는 PTFE 표현이 없다 · 설계 §4-1)')''',
    '''    if ptfe_stamp not in ('off', 'face_alpha'):
        raise ValueError(f'ptfe_stamp = {ptfe_stamp!r} — 접합 (S2) 은 off · face_alpha 에서만 (★ 10-21 사전 리뷰 PRE-impl-03 · 1저자 Q-C: '
                         f'centerline = 거부 — VGCF 셀을 sid 7 로 덮어 옛 판은 덮인 접점의 포트를 옆 셀로 옮겨 절연체를 더해 σ 가 올랐다 · '
                         f'capsule = 예약값)')
    if ptfe_jlaw == 'P1' and ptfe_stamp != 'face_alpha':
        raise ValueError(f'PTFE–접합 법칙 P1 (덮인 접합 절단) 은 face_alpha 에서만 ({ptfe_stamp} — off 는 PTFE 표현이 없다 · 설계 §4-1)')''')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
