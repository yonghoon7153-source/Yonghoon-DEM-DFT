# Phase 1 — PVS 모드 감도, 첫 실측 (2026-09-03)

실행: `python3 phase1_pvs_jacobian.py` · 입력 `grid_curves_v4/curves.parquet`
(noise=0, 1023 조건) · 산출 `results/phase1/pvs.csv` (이 파일이 정본).

## 결과 요지

| 지점 | ∂PVS/∂(LLI, LAM_PE, LAM_NE) [Ah/V² per unit loss] | 부호 |
|---|---|---|
| pristine (0,0,0)+h | (+241.8, −192.0, −139.2) | + − − |
| 22p 근방 (0.16, 0.12, 0.12)+h | (−253.5, −21.6, −14.1) | − − − |

- **pristine 에서는 LLI 와 LAM_PE 가 반대 부호** — 세미나 p.8 의 P2D 단독
  스윕({LLI, LAM_PE} 둘 다 ↑)과 **다르다**.
- **22p 동작점 근방에서는 셋 다 같은 부호** — 거기서는 PVS 단독으로 어느
  방향도 안 갈린다.
- 부호 구조가 **동작점에 따라 뒤집힌다** = PVS 는 전역적으로 단조인 feature 가
  아니다. 세미나 p.8 이 보여준 단독 스윕 곡선도 실은 LLI 축에서 비단조였다
  (그쪽 도표에서도 LLI 곡선이 출렁인다 — figure-read).

## 세미나와 다른 점, 그리고 그대로 믿으면 안 되는 이유 (주의 3건)

1. **valley 정체성이 정의에 민감하다.** 수동 anchor 계산(첫 인접 valley,
   3.765 V)은 pristine PVS = −20.0 으로 세미나와 일치했는데, 스크립트의 정의
   (창 안 전역 최소, 3.859 V)는 −11.27 을 준다. 어느 valley 를 "Valley2" 로
   보느냐가 값과 감도를 바꾼다 — 세미나 p.15 discussion point 3 ("ICA 계산에
   따른 PVS 변화")이 정확히 이 문제다. 평활화 창(11/21/31)에는 둔감했다
   (−11.39/−11.27/−11.07).
2. **LLI 단독 스윕이 비단조다** (−11.3 → −3.9 → −11.0 → −63.6 → −44.6).
   곡선이 밀리면서 창 안에서 잡히는 peak/valley 의 정체가 바뀌는 것(feature
   tracking 실패)일 가능성이 높다 — 아직 검증하지 않았다. 검증 전에는 pristine
   gradient 의 LLI 부호(+)를 인용하지 말 것.
3. **LAM_PE ≥ 0.08 에서 NaN** — peak 이 [3.55, 3.72] 창을 벗어난다. 창을
   따라가게 만들면 다른 feature 를 재는 것이 되고, 고정하면 커버리지가 깎인다.
   PVS 류 feature 의 구조적 한계로 기록한다.

## 이 결과가 지금 말해도 되는 것 (방향성 관측 — 인용 금지 등급)

- 22p 동작점 근방에서 PVS 의 세 모드 감도가 동부호다 → **그 동작점에서 PVS
  는 LLI↔LAM_PE 를 가르는 방향을 주지 않는다** (질문 카드 H1 쪽 근거).
- PVS 값·감도가 valley 정의와 동작점에 강하게 의존한다 → 세미나 p.13 의
  permutation importance 에서 PVS 가 최하위권인 것과 정합적인 그림.

## 다음

1. LLI 비단조의 원인 분해 (peak/valley 좌표 열이 pvs.csv 에 있다 —
   v_peak/v_valley 가 스윕 중에 점프하는지 본다).
2. valley 정의 2종(인접 vs 전역)을 둘 다 계산해 감도 표를 재작성.
3. Phase 2 (SEV) 는 동역학 시뮬레이션 필요 — PyBaMM P2D 프로토콜 설계부터.
