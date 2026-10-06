# C1 설계 요약 (TAU-13 · TAU-07/08 · L2-05 · 에이전트 10-06 저녁 · 리포 무수정) — 1저자 결정 대기
근거 = real_14 · case15 실덤프 + 같은 기하 FV 기준 (구 사슬 · SC/BCC/FCC 격자 · 무작위 충전) · 스크립트 designC1/
| # | 항목 | 판정 | 권고 |
|---|---|---|---|
| 1 | L2-05 전극 | 가상 전원/싱크 g_b (모든 간선 의존) → 정확 Dirichlet (B=1 · T=0 고정, spsolve ≤30k / CG rtol 1e-10 + ILU) | ✅ 세대 2 포함 · 배포값 변화 ≤1.5e-4 (194 행 5–6 째 자리) · 새 시험 test_network_dirichlet D1–D7 · 메타 ion_net_electrode='dirichlet_exact' |
| 2 | TAU-13 Hertz ψ 단독 (H1) | 모든 기하에서 과전도 +6…+50 % (원기둥 bulk 과전도가 드러남) | ⛔ 기각 |
| 3 | H1 + 구 조각 bulk (H12) | z≤10 개선 (±5 %) · z≈12 · s≳0.3 (LHSx 고밀) +20–28 % 과전도 | Hertz 기본 = H0 유지 (주 값 그대로) · H12 = 결합 팔 + 194 재실행에 `_h12` 민감도 열 (기본 학습 제외 · 행마다 [H0, H12] 괄호) · H1 단독 조합 거부 |
| 4 | 공유-코어 bulk | 간선별 bulk 의 원리적 한계 (T_CF = V_구/(V_막대·Σcos²θ): 원기둥 4/z · 구 조각 6/z) | 사전등록 (z 4–12 무작위 · AM 장애물 · 실침대 복셀 |f_망/f_FV−1| ≤ 10 % 통과 전 기본 불변) — 오늘 아님 |
| 5 | CF q>1.5 가드 | LHSx CF 29 행 solve_failed = 모형 과전도 오분류 (q = −0.222 + 0.233·φ·CN, R² 0.985) | ✅ 가드는 FULL 만 · CF/협착-only 는 값 유지 + 'model_over_conduction' 상태 (진단 열만) |
- 실침대 s=a/r (Hertz): real_14 중앙 0.27 (전력가중 0.22) · case15 전력가중 0.07 · 194: LHS s_A 0.20–0.45 · LHSx 0.42–0.46 · SE–SE CN LHS 중앙 4.7 · LHSx 6.9–11.2
- H12 효과: real_14 σ ×1.186 · case15 ×1.060 · 194 추정 LHS ×1.20 · LHSx ×1.21 (×1.03–1.37)
- ψ 곱셈 (비준분) 실크기: real_14 σ_P ×2.47 (T 15.1 → 6.1) · case15 ×1.24 · LHSx Physics T ×0.73–0.90 이하 → MODEL_BELOW_CONTINUUM_BOUND 10 행보다 늘어남
- 라벨: Hertz 협착 'maxwell_halfspace' 유지 · 새 메타 ion_net_electrode · ion_net_bulk ('cylinder_half_d') · 사전 문구 (Hertz 1세대 편향 z≤10 −12…−28 % · z≈12 ±5 % 상쇄 / Physics ψ곱 + 원기둥 = 과전도 쪽 / CF T_CF≈4/z 상한 아님)
- 고칠 시험: test_network_boundary_rule ① GOLD · ⑨ · test_constriction_power_share C1d (0.0916787 → 9/110) · (H12 팔) test_psi_default_switch ④⑤⑥ · test_tau_flux A4 · K1 · 계약 :889 · audit_transport_cap_equivalence ⑦f · ⑦n · ⑦j
