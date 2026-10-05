# ps45 r4.5 다섯 조성 — 웹앱 케이스 페이지의 접촉 네트워크 값 (2026-10-05 밤 · 1저자 전사)

- 출처: 1저자가 WSL 웹앱 (`~/dem-web`) 케이스 페이지 다섯 개를 그대로 붙여 준 것 (10-05 밤) · 케이스 ID = `../ps45_r45_union_20260929/r45_union_summary.tsv`.
- 값의 세대: 업로드 때 (09-22 · 09-25) 웹앱 파이프라인이 계산한 망 솔버 값 — 페이지에 `tau2 handover status NOT_COMPUTED (missing_input)` ·
  띠 규칙 "기록 없음 (안 A 전 산출물)" · 전력 몫 "—" 가 보이는 것이 그 표지다.  ⬜ 지금 코드로 망 단계 재계산 (`stop_after='network'`) 뒤 대조.
- 열: σ_ion · σ_e = 망 솔버 FULL (Hertz = LIGGGHTS c_cpl[22] 기하 교차 원판 · Physics v1 = Tabor · 부피 · 기하 cap) · σ_e Stage E = 파괴 (Auerbach) 반영 ·
  κ = 열 (mS/cm 상당) · tau2 = φ_SE·σ₀/σ_ion (tortuosity factor · σ₀ = 3.0 mS/cm 펠릿값 · 1세대 협착) · AM–AM 접촉 수 · SE–SE 배위수 · 공극률 ε_sphere · 두께 (판 간격).
- 한정: 조성당 침대 1 개 (시드 반복 없음) · σ 는 접촉망 모델 값 (실험 앵커 아님) · Physics 는 소성 면적 보정 후처리.
