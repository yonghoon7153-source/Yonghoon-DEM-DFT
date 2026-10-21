p = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1ea4b71aa06a03ee/scripts/test_carbon_junction.py'
s = open(p, encoding='utf-8').read()


def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80])
    s = s.replace(old, new)


rep('''  XC     (Q-B) 자기 교차 (닿음 0.8 · s 10.8 · L_c 1.2) — s ≥ s_min = R_j 간선 (손 회로) · s < s_min = 옛 융합 (= cjunc 끔) · 바닥 s > D ·''',
    '''  XC     (Q-B) 자기 교차 (닿음 0.8 · s 10.8 · L_c 1.2) — s ≥ s_min = R_j 간선 (손 회로) · s < s_min = 옛 융합 (= cjunc 끔) · 바닥 s > D ·
         s > (π/2)·d ·''')
rep('''  KBND   (05 · 한계 기록) k 경계 (90° → 89.99°) σ 뜀 크기 = 생산 단위 R_j 1e2 · 1e4 · 1e6 에서 −0.98 % · −2.1e-4 · −2.1e-6 (± 10 % · ∝ 1/R_j)
  MUT-RCA2 새 보장 변이 (조각 = fid 규칙 · 포트 옮김 · SV 전부 끊음 · 이음매 별칭 끔) 가 위 시험에 옳은 이유로 걸린다 · 변이 안 예외 = 하네스 실패''',
    '''  KBND   (05 · 한계 기록) k 경계 (90° → 89.99°) σ 뜀 크기 = 생산 단위 R_j 1e2 · 1e4 · 1e6 에서 −0.98 % · −2.1e-4 · −2.1e-6 (± 10 % · ∝ 1/R_j)
  MUT-RCA2 새 보장 변이 (조각 = fid 규칙 · 포트 옮김 · SV 전부 끊음 · 이음매 별칭 끔 · 바닥 = s > D 만) 가 위 시험에 옳은 이유로 걸린다 ·
         변이 안 예외 = 하네스 실패
  FLOOR  (Q-B) 같은 조각 쌍의 바닥 = s > D · s > (π/2)·d — L 자 90° 모서리 = 어느 s_min (없음 · 0) 에서도 자기 후보 0 · 날카로운 V = 후보
  MUT-RCA (09) 반사실 변이 = 생산 서명 (certify=) · 변이 안 예외 (`_try` 가 삼킨 것 포함) = 하네스 실패 (옳은 이유 아님)''')
rep('''    #  ★ 10-21 (Q-B) — s_min 0.6 (s_min 0 = 바닥만 → 90° 모서리도 접합 · 포트 동률 셈이 모서리에 묻힌다) · 재방문 s = 그 쌍 (같은 조각 ·
    #    같은 셀 두 가지) 의 경로 호 간격 (쌍마다 · 옛 = 그 쌍이 든 자기 후보마다 하나)''',
    '''    #  ★ 10-21 (Q-B) — s_min 0.6 (머리핀 접합 하나 · L_c < L_par · 90° 모서리는 바닥 (s > (π/2)·d) 이 거른다) · 재방문 s = 그 쌍 (같은
    #    조각 · 같은 셀 두 가지) 의 경로 호 간격 (쌍마다 · 옛 = 그 쌍이 든 자기 후보마다 하나)''')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
