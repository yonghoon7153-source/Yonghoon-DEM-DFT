# 194 망 배치 — 값 미리보기 (그림 · 요약 · 2026-10-05 밤)

- 1저자 요청 (10-05 밤): *"194개 관련해서 간단하게라도 plot"* · *"이 값들이 사용가능한지에 대해서도 codex에 물어봤으면"* — Codex 5차 요청서 §6 의 자료.
- 원천 = `docs/data/lhs_network194_11fcf91e8/merged/lhs/metrics_flat.csv` · `docs/data/lhs_network194_11fcf91e8/merged/lhsx/metrics_flat.csv` (커밋본) 만.  **새 계산 없음.**  `python3 plot_overview.py` 로 이 폴더의 다섯 파일을 다시 만든다.
- 파일: `net194_overview.png` · `.svg` (6 패널) · `net194_overview_data.csv` (케이스 194 행 · 그림 값) · `net194_value_summary.tsv` (코호트 × 양 · 두 모드 · 최소 · 중앙 · 최대 · 빈칸 수).

## 정의 (그림 아래 주석과 같다)

- φ = 질량보존 기준 부피분율 (`phi_se_mass_conserving` · `phi_am_mass_conserving`).
- f = σ_ratio · L_gap / L_mc (σ_ratio = 솔버 무차원 `sigma_full` · σ₀ = 3.0 mS/cm) — `scripts/tau_flux.py` 의 `ion_columns` 와 같은 식.
- **수송 tortuosity** = φ_SE / f (= φ_SE·σ₀/σ_ion · **제곱근 아님** = 문헌의 tortuosity factor · 키 `tau2_*`) — 표기는 1저자 10-05 밤 (*"τ² 이라 표현하지 말고 수송 tortuosity"*).
- Bruggeman a = ln f / ln φ_SE (수송 tortuosity = φ^(1−a)).
- 협착 전력 몫 = 접촉 협착의 ΣI²R / 전체 ΣI²R (같은 FULL 해).

## 한정

- **미리보기다** — `metrics_flat` 에 띠 규칙 (`boundary_rule`) 이 없어 τ 관문 G1 을 이 그림에선 안 걸렀다.  정본 = 고친 생성기로 만든 인계 v1.2 의 상태 칸 (OK · NOT_PERCOLATING · BAND_FALLBACK · MODEL_BELOW_CONTINUUM_BOUND).
- 용도 = ML 기술자 (이 모델 안의 상대 비교) · 실험 절대 대조 HOLD (10-01 최종 판정 · 1세대 협착식 · σ₀ = 펠릿값).
- 등록된 인계 범위 = ⑤⑥⑦ + 망 τ 묶음.  σ_e · σ_th · 협착 전력 몫은 **범위 밖** (194 metrics 에만 있다).

## 교차 검산 (이 폴더를 만들 때)

- 망 단계 SE 비관통 24 (LHS · 전부 φ_SE < 0.17) · AM 비관통 7 (LHSx · φ_AM 0.14–0.23) = 독립 퍼콜 감사 `docs/data/lhs_perc_audit_20261001/lhs_20261001_d1ec42fba/perc_audit.tsv` · `lhsx_20261001_d1ec42fba/perc_audit.tsv` 의 `se_perc_webapp_dump` · `am_perc_webapp_dump` 와 **같은 케이스 집합** (130 · 64 집합도 같다).
- 망 φ (`phi_se`) ↔ 장부 φ_mc·L_mc/L_gap 차 최대 2.2e-16 (194 전부).
- Hertz 수송 tortuosity < 1 = 0 건 · Bruggeman a 는 관통 170 건 모두 1.5 위 (1.84–4.82).
- Physics 모드: LHSx 10 건 (φ_SE 0.72–0.80) 의 수송 tortuosity 0.89–1.00 < 1 → 인계에서 G5 `MODEL_BELOW_CONTINUUM_BOUND` (값 유지 + 표지) 대상.
