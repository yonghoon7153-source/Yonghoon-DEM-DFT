# ps45 r4.5 다섯 조성 — 접촉망 세대 2 재계산 (10-07 · 발표 = Tabor 수송 tortuosity · 이온 · 전자전도도)

- **왜**: 1저자 10-07 *"tabor로 구한 수송 tortuosity를 하자"* — 10-06 덱 8 장의 Tabor 선 (8.34–12.25) 은 세대 1 옛 ψ 나눗셈 결함 (`L2-01`) 의 값이라
  쓰지 않고, 같은 다섯 침대의 망 단계만 세대 2 코드로 다시 돌렸다.  세대 1 기록 = `../ps45_r45_network_20261006/` (같은 케이스 ID).
- **실행**: 1저자 WSL · 10-07 · `~/dem-audit` detached `origin/claude/stoic-knuth-NObVQ` = `0801d4ceb` (dirty 0) · `scripts/webapp_network_batch.py --from-tsv
  docs/data/ps45_r45_union_20260929/r45_union_summary.tsv --out ~/ps45_network_g2_0801d4ceb` · 5/5 done · published · 1,424 s · rc 0 · 격리 출력 (업로드 원본 읽기만 ·
  웹앱 케이스 페이지 무변경 — 웹앱 화면의 망 값은 세대 1 그대로).
- **원자료**: `raw/ps45_network_g2.tgz` (59,390 B · sha256 `076727a8f0f1e263349a9f50c4aca5afdb112b16c3b4193bc9f8c9573fcf608f` — `network_cases.tsv` · `.json` ·
  `status.json` · `logs/` · `solver_output/`) · 표 사본 `network_cases.tsv`.  다섯 행 `psi_placement_physics = multiply` (세대 2) · 이온 τ 상태 OK/OK.
- **그림 · CSV**: `make_tau2_figs.py` · `make_sigma_tabor_figs.py` (값 = 표 그대로 · 새 계산 없음) → `transport_tortuosity_g2.csv` · `sigma_tabor_g2.csv`
  (Origin 머리 세 줄) · `figs/` PNG 넷.

## 값

| PC:SC | 0:10 | 3:7 | 5:5 | 7:3 | 10:0 |
|---|---|---|---|---|---|
| 수송 tortuosity · Tabor (세대 2) | 4.1228 | 3.3457 | 3.0508 | **2.7759** | 3.1282 |
| 수송 tortuosity · Hertz (주 값) | 7.2433 | 5.9733 | 5.4495 | 5.0297 | 5.2864 |
| (세대 1 Tabor · 덱 8 장 — 쓰지 않음) | 12.2537 | 10.2240 | 9.2950 | 8.5058 | 8.3428 |
| σ_ion · Tabor (mS/cm) | 0.2064 | 0.2607 | 0.2908 | **0.3236** | 0.2832 |
| σ_e · Tabor (mS/cm) | 6.191 | 3.900 | 2.689 | 1.878 | 1.674 |

- 수송 tortuosity = tau2 = φ_SE·σ₀/σ_ion (**제곱근 아님** · τ 명명 규약) · σ₀ = 3.0 mS/cm (펠릿값).
- Hertz 는 세대 1 과 상대 −1.0e-6 ~ −1.2e-6 (전극 처리만 바뀜 — 세대 2 설계 기록 §3).  Tabor 는 다섯 조성 모두 < Hertz (0.55–0.59 배) — 세대 2 는 간선마다
  R_c(Tabor) ≤ R_c(Hertz) (면적 하한 = Hertz 원판 · ψ 곱셈 ≤ 1) 이고 bulk 저항이 같아 망 σ 는 Tabor ≥ Hertz (계산 전에 1저자에게 말한 예측과 같다).
- ⚠ 한정어 (그림 각주): Tabor = 면적 · 협착 규약의 민감도 (Codex 10-06 5 차 — 주 값은 Hertz) · Tabor 면적 계산의 열린 질문 (면적용 재구성 힘이 DEM 힘의 2.5–3.2 배 ·
  DEM 힘이면 σ_ion −11 % — 세대 2 설계 기록 §2 "세대 3 질문") · 세대 2 망 코드 = Codex 배포 관문 재검증 중 (수치 교정은 지지).
- ⚠ σ_e: 탄소 첨가제 없는 침대 (활물질 접촉만) · 활물질 입자 σ 입력 50 mS/cm (`network_conductivity.SIGMA_AM_ELECTRONIC` · 원장 `CL-92`: 측정 NCM811 4.1–5.2 mS/cm 의
  약 10 배) · 망 FULL (Stage E 파괴 보정 전) ⇒ 조성 사이 비교로만.
- 발표 문장 (1저자 4 쪽): *"7:3에서 이온 이동 저항도 가장 작음 (Tortuosity 4.12 → 2.78)"*.
