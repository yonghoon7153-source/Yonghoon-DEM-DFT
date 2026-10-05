# LHS 구조 디스크립터 — 배포 v1.2 (2026-10-06 · 1저자 비준 10-06 · Codex 5차 조건부 인계 GO)

> 수영 님 ML 용 **구조 디스크립터 + 접촉 네트워크 수송 지표**.  DEM (LIGGGHTS) 으로 300 MPa 압밀한 복합 양극 침대의 설계 입력 → 구조 값 (v1.1 그대로) 에
> ⑤ F1 근접쌍 · ⑥ 힘 기반 파괴 · ⑦ 접촉 면적 (34 열) 과 **Hertz 접촉망의 수송 tortuosity factor T** (5 열 + 메타 4 열) 를 더한 표다.
> **v1.1 (`docs/data/lhs_release_20261001_v11/`) 의 열 · 값 · 순서는 한 칸도 바뀌지 않았다** (17,202 칸 대조 · 차이 0) — v1.1 README 의 §2–§5 규약은 그대로 살아 있고, 이 README 는 **더해진 것**과 **고쳐 읽을 것**을 적는다.
> 정본 (전체 열 251 · 253 · 내부 QC · τ 출처 부록 · 봉인 감사) = `docs/data/lhs_network194_11fcf91e8/handover_v12_20261006/` · 판정 = `docs/reviews/codex_review_rglr3_reverify_20261006.md`.

## 외부 검토 (Codex 5차 · 2026-10-06) — 먼저 읽을 것

- **판정: 고정 194 행 (아래 원천 CSV 두 개) 의 전사 · 수식 · 기록 정합 = PASS · ⑤⑥⑦ + Hertz 주 지표의 모델 내부 ML 기술자 인계 = 조건부 GO · Physics 값 = 기록 · 진단 부록으로 GO (기본 학습 열 HOLD) · 실험 절대값 타깃 · 실물 상대 순위 · COMSOL 물성 대입 = HOLD 유지 · 새 P1 없음.**
  조건 = §6 사용 설명 (이 README §3 · §4 · §5) 을 표와 함께 전달하고, Physics 를 자동 학습 입력으로 묵시적으로 선택하지 않는 것.  194 건 재계산은 요구하지 않았다.
- 검토가 직접 대조한 것: 옛 공통 36,600 칸 차이 0 · 새 ⑤⑥⑦ 34 열 × 194 행 · τ 원천 194 세트 해시 · F1 · 파괴 · 면적 항등식 산술 · `f_mc = q·L_gap/L_mc` · `T = φ_mc/f_mc` · `√T` 독립 재계산 · 봉인 감사 194 고유 ID · record hash.
- ⚠ 정본 폴더의 자동 검산기 `reread_v12.py` 의 PASS 는 **배포 관문이 아니다** (검산기 결함 `RGLR4-01` C4 공통 칸 차이 미반영 · `RGLR4-02` C8 ID 집합 미검사 — 수정 예정).  이 배포본은 그 검산기가 아니라 **Codex 독립 대조 + 배포 생성기의 내장 대조** (`scripts/lhs_release_build.py` — 배포 ⊆ 인계표 · 행 · 순서 · 값 · 열 사전 행) 로 확인했다.
- 원천 (Codex 수용 범위 · 이 파일을 바꾸거나 다른 계산 세대를 붙이면 수용을 자동 승계하지 않는다):

  | 원천 | 행 × 열 | sha256 |
  |---|---|---|
  | `lhs_handover_v12_20261006.csv` | 130 × 251 | `d1a05c6498f6959057bc6a20394a83acf9a3ff72bfec7149306539513352971a` |
  | `lhsx_handover_v12_20261006.csv` | 64 × 253 | `b17e39a8ef435e034f59c365e17481d82530b54f7adaabcd04c7b63ee88953ea` |

> **전달 문단 (판정문 §7 그대로)**:
> 이 자료는 고정 DEM 접촉망과 등록된 저항 규약에서 계산한 모델 기술자이다. 수송 tortuosity factor T(`tau2_ion_*`)는 φ_SE,mc/f_ion_*이며, `tau_ion_*`는 그 제곱근이다. `f_ion_*`는 판 간격 해를 질량보존 두께로 재척도한 값이지 재해석한 망 해가 아니다.
>
> 기본 분석 지표는 Hertz이다. Physics는 면적과 legacy 협착식이 함께 다른 모델 규약의 민감도 자료로 별도 보존하며, 기본 학습 열에 자동 포함하지 않는다. Physics의 T<1인 10행은 `MODEL_BELOW_CONTINUUM_BOUND`로 표시하고 값을 유지했다. 이는 원천과의 불일치가 아니라 연속체 전도상 하한과 정합하지 않는 모델 출력이다. T≥1 또는 상태 OK 역시 물리적 정확도 인증은 아니다.
>
> 비관통의 f=0과 T 빈칸(무한대)은 기술적 계산 실패의 빈칸과 다르므로 상태 열을 함께 읽어야 한다. 두 모드 모두 실험 절대값 타깃이나 실물 상대 순위의 검증값으로 사용하지 않는다. Physics 10행만 사후 삭제하여 남은 값의 물리적 타당성을 주장하지 않는다.

## 0. 바뀐 것 (v1.1 → v1.2)

| 무엇 | 왜 |
|---|---|
| **⑤ F1 근접쌍 6 열 · ⑥ 힘 기반 파괴 12 열 · ⑦ 접촉 면적 16 열 (= 34)** | J20-s 감사 (10-04 · 1저자 비준) 를 거친 묶음 — 정의 · 관문 · 한정어가 열 사전에 있다 (§2) |
| **Hertz 수송 tortuosity 5 열** (`f_ion_hertz` · `tau2_ion_hertz` · `tau_ion_hertz` · `ion_net_status_hertz` · `ion_net_status_reason_hertz`) **+ 메타 4 열** (`ion_sigma0_mScm` · `ion_sigma0_T_C` · `phi_basis` · `L_basis`) | 194 침대 접촉망 배치 (10-05 · `docs/data/lhs_network194_11fcf91e8/`) → Codex 5차 조건부 GO.  v1.1 §6 의 *"τ_Laplace (망 계산 단계 — 나중)"* 이 이 열이다 |
| **Physics 모드 = 별도 부록 파일** `*_physics.csv` (key + 5 + 메타 4) | Codex QV3 — 면적 + 협착 규약의 **결합** 민감도 자료 · 기본 학습 열 제외 (opt-in · 필요할 때만) |
| 원천 인계표 세대 | 10-01 (`d1ec42fba` 접촉 배치) → 10-06 v1.2 (같은 접촉 배치 + 망 배치 `11fcf91e8`).  **v1.1 의 89 · 88 열 값은 전부 같다** (Codex C4 24,440 + 12,160 칸 · 이 배포 17,202 칸 모두 차이 0) |
| 열 사전 문구 | v1.1 정오표 (`ERRATA_20261004.md`) 의 `tortuosity_SE_wall` 문장은 **인계표 사전에서 교체됐다** (*"수송 굴곡도는 망 단계의 tau2 = φ_SE·σ₀/σ_full …"*).  ⚠ 그 문장 끝의 *"이 표에 없음"* 은 v1.2 에서 **거짓**이다 — `tau2_ion_hertz` 열이 바로 그 양이다 (§4) |

v1 · v1.1 은 그대로 둔다.  이 배포는 **새 계산을 하지 않았다** — 정본 인계표에서 열을 고른 것뿐이다 (§9).

## 1. 파일

| 파일 | 행 × 열 | 내용 | sha256 |
|---|---|---|---|
| `lhs_release_20261006_v12.csv` | 130 × 132 | LHS 설계 130 침대 (bimodal 100 · mono AM_P 15 · mono AM_S 15) — v1.1 89 열 + 34 + 5 + 4 | `c1aeee346af5c598f109fa06ea260c8d965a727e02a9d42df38c63832608cad9` |
| `lhsx_release_20261006_v12.csv` | 64 × 131 | 확장 64 침대 (bimodal 48 · mono 16 · **전부 SE-rich**) — v1.1 88 열 + 34 + 5 + 4 | `548930c709015eef8ebc4f09b751d9e07afd3d839865b92d6cf985d0511ece0f` |
| `lhs_release_20261006_v12_physics.csv` | 130 × 10 | **부록 (opt-in)** — `case_id` + Physics 5 + 메타 4 | `be3cc51deabf13e13591dbd3839f7ee2565a320d22abb4cb26442ee11701f6e7` |
| `lhsx_release_20261006_v12_physics.csv` | 64 × 10 | 같은 부록 (64) | `f129eedc8b0688865888c44401253eb7d2b93ad4d89c7a235bc6f8cb8aeaac02` |
| `*_columns.tsv` (넷) | 열마다 한 줄 | 뜻 · 분모 · 주의 · 판정 근거 · 관문 — **정본 인계표 열 사전과 같은 줄** (이 README 와 다르면 **이 README 가 정정판** · `LREL-06` 규칙 그대로) | 150,749 · 150,622 · 19,980 · 19,980 B |

한 행 = 한 침대 (300 MPa 압밀 뒤 한 프레임).  `case_id` 가 키 · 행 순서 = v1.1 과 같다.  두 CSV 를 합쳐 쓸 때는 데이터셋 표지를 둔다 (v1.1 §3-8).

## 2. 더해진 열의 역할 (v1.1 §2 표에 잇는다)

| 역할 | 열 | 130 · 64 | 빈칸 규칙 |
|---|---|---|---|
| **Y9 ⑦ 접촉 면적 (A_dem_geometric · µm²)** | `area_<쌍>_total` · `area_<쌍>_mean` (쌍 = AM_P_AM_P · AM_P_AM_S · AM_P_SE · AM_S_AM_S · AM_S_SE · AM전체_SE · SE_SE) · `am_am_total_area` · `am_am_mean_area` | 16 · 16 | total: 접촉 0 쌍 = **측정된 0** (두 상이 다 있을 때) · 설계에 없는 상의 칸 = 빈칸 (mono) / mean: 접촉 0 쌍 = **빈칸** (0 개의 평균은 정의되지 않는다).  130 에서 mean 빈칸 = AM_P–AM_P 18 (mono_AM_S 15 + 접촉 0 인 bimodal 3) · AM_S–AM_S 15 · AM_P–AM_S 30 / 64 = 14 · 8 · 16 |
| **Y10 ⑥ 힘 기반 파괴 (Auerbach · AM–AM 접촉만)** | `n_{intact,microcrack,multicrack,fragmentation,pulverization}_force_AM_AM` · `n_total_AM_AM_force` · `frac_{…}_force_pct` (5) · `fracture_index_force` | 12 · 12 | AM–AM 접촉 0 인 침대는 전부 빈칸 — 이 두 표에는 **없다** (`n_total_AM_AM_force` = `am_am_n_contacts` 194/194) |
| **Y11 ⑤ F1 근접쌍 (SE–SE)** | `se_se_cn_aug` · `se_se_cn_aug_std` · `se_se_cn_aug_n_extra` · `se_se_cn_aug_h_spread_sim` · `se_se_cn_eff_area` · `se_se_cn_eff_area_perc` | 6 · 6 | `_perc` 빈칸 ⟺ 비관통 (130 중 24 · 64 중 0) · 나머지 빈칸 0 |
| **Y12 수송 tortuosity (Hertz 접촉망 · 이온)** | `f_ion_hertz` · `tau2_ion_hertz` · `tau_ion_hertz` · `ion_net_status_hertz` · `ion_net_status_reason_hertz` | 5 · 5 | **상태 열이 정한다** (§3-1).  130: OK 106 · NOT_PERCOLATING 24 (f = 0.0 · T · √T 빈칸 = ∞) / 64: OK 64.  사유 열은 두 표 모두 전부 빈칸 (NOT_COMPUTED 가 없다) |
| **메타 (상수 · 특징 · 타깃 금지)** | `ion_sigma0_mScm` 3.0 · `ion_sigma0_T_C` 25.0 · `phi_basis` mass_conserving · `L_basis` L_mc | 4 · 4 | 194 행 모두 같은 값 — f · T 의 기준 상태를 표에 박아 둔 것 |

열 사전 (`*_columns.tsv`) 의 `source` = `webapp` (⑤⑥⑦ · 접촉 단계 재실행 `d1ec42fba`) · `tau_flux` (τ 묶음 · 망 배치 `11fcf91e8`) · `verdict` = ✅ 쓴다 / ✅ 쓴다(이름 주의) / ✅ 싣는다 (망 τ 묶음 · G6 — 두 모드 모두 물리 타깃 HOLD · 값은 싣는다 · ML 기술자 전용).

### 2-1. 정의 (열 사전 요지)

- **⑦ 면적** = LIGGGHTS 접촉 덤프의 `c_cpl[22]` = 두 구 **기하 교차 원판** 넓이 π(rδ − δ²/4) 의 쌍별 합 · 평균.  ⚠ 이름의 "area" 는 **Hertz 탄성 접촉 면적 πR\*δ 가 아니다** (같은 반경에서 ≈ 1.99 배 · `L1-04`) — `A_dem_geometric` 으로 부른다.  소성 보정 (physics) 면적은 넘기지 않는다 (v1.1 J20-m 과 같은 이유).  `am_am_total_area` = AM_P–AM_P + AM_P–AM_S + AM_S–AM_S · `area_AM전체_SE_total` = AM_P–SE + AM_S–SE.
- **⑥ 파괴** = AM–AM 접촉마다 마지막 프레임의 법선력 F 를 Auerbach 임계 P_c = A·K_IC²·R_min/E\* (A = 200) 와 비교해 다섯 단계 (F/P_c 배수 1 · 3 · 11 · 32) 로 분류한 **개수**와 **비율** · `fracture_index_force` = (파편화 + 분쇄) / 전체.  한정 (`LHS-31` · 열 사전 caveat 그대로): ① 마지막 프레임 힘 (압축 중 최대 아님 → 손상 **하한**) ② 벽 · 판 접촉 제외 (판에 닿은 AM_P 의 최대 하중이 빠진다) ③ R_min 선택 (R\* 이면 P_c 절반) ④ K_IC_P 0.3 MPa·m^½ = 소결 펠릿값 (정본 카드 xu2017 — 이차입자 0.102 의 3 배) · K_IC_S 1.0 은 측정 근거 없음 — P_c ∝ K_IC² ⑤ A 200 · 배수 원전 (Lawn Table 3.4) 의 정본 카드 없음 [미확인] ⑥ δ 기반 파괴 열 (이 표에 없음) 과 나란히 인용 금지.  ⇒ **단계 비율 · 지수는 이 모델 규약 안의 상대 지표**다.
- **⑤ F1 근접쌍** = 탄성 접촉 (덤프) 에 표면 틈 ≤ h 인 SE–SE 쌍을 더해 센 SE 배위수 `se_se_cn_aug` (= `se_se_cn` + 2·`se_se_cn_aug_n_extra`/`n_SE_measured`) 와 그 표준편차 · 더한 쌍 수 · h.  ⚠ **h = 10 nm 는 출처 없는 모델 상수** ("2 × h_film_min") — 감도 기술자로만 · SE–SE 만.  `se_se_cn_eff_area` = SE 표면 중 SE–SE 접촉 원판이 덮은 비율 = 2·`area_SE_SE_total`/(`n_SE_measured`·4πr_SE²) (SE 단분산) · `_perc` = 관통 SE 성분에 속한 SE 만.  범위: `se_se_cn_aug − se_se_cn` 130: 0.006–0.139 · 64: 0.036–0.109 / `se_se_cn_eff_area` 130: 0.019–0.417 · 64: 0.340–0.564.
- **수송 tortuosity (첫 출현에 늘 이렇게)**: **수송 tortuosity factor T (`tau2_ion_hertz`) = φ_SE,mc / f_ion_hertz · 제곱근 아님 = 문헌의 tortuosity factor (Tjaden κ = τ² · Landesfeind τ · COMSOL τ_F · TauFactor τ)**.  `f_ion_hertz` = σ_eff/σ₀ (무차원 · 문헌 ε/τ² · COMSOL f_e = 1/N_M) = 솔버 FULL 해의 σ 비 × L_gap/L_mc — **판 간격 해를 질량보존 두께 L_mc 로 재척도한 값이지 L_mc 에서 다시 푼 망 해가 아니다**.  `tau_ion_hertz` = √T (유도량 · Tjaden 식 3 flux τ · 웹앱 τ_Lap,eff) — Dijkstra 경로 길이비 (`tortuosity_SE_wall`) 의 뜻을 주지 않는다.  σ₀ = 3.0 mS/cm 펠릿값 (Cronau 2021 SI 그림 S2c µC-Li₆PS₅Cl 평탄 하단 · `CL-91`) 이지만 **f · T 는 무차원 σ 비로 계산해 σ₀ 수치에 무관**하다 — 다른 것은 기준 상태 (Minnmann 은 순수 SE 펠릿 τ² ≡ 1 · 우리는 간선 재료 σ₀ 기준).

## 3. 꼭 지킬 규약 (v1.1 §3 에 더한다)

**3-1. 상태 열을 반드시 같이 읽는다** (Codex QV2 — 상태 열을 버린 CSV 만 전달하지 않는다 · 숫자 열만 골라 `dropna`/0 채움 하는 학습 코드는 충분하지 않다).

| `ion_net_status_hertz` | f | T · √T | 뜻 | 이 배포 |
|---|---|---|---|---|
| `OK` | 값 | 값 | 기술 게이트 (G1–G6) 통과 — **모델의 물리적 정확도 인증이 아니다** | 130 중 106 · 64 중 64 |
| `NOT_PERCOLATING` | **0.0** | **빈칸** | 관통 SE 경로 없음 — f = 0 은 물리적 0 · T 빈칸은 **물리적 무한대의 저장 표현** (기술적 결측 · 0 과 다르다) · 이온적으로 죽은 전극으로 읽지 말 것 (`ionic_active_pct` 는 유한) · 문턱 근처 관통 여부는 상자 크기 (50 µm) 의 실현값 | 130 중 24 (= `percolation_pct` 0 · `tortuosity_SE_wall` 빈칸과 **같은 집합**) |
| `MODEL_BELOW_CONTINUUM_BOUND` | 값 | 값 (T < 1) | 모델 출력이 연속체 전도상 하한 (T ≥ 1 — 조건부 변분 상한) 과 정합하지 않음 · **값 유지 + 표지** · 물리값 인증으로 쓰지 않는다 | Hertz 0 · Physics 부록 10 (64 쪽) |
| `BAND_FALLBACK` | 빈칸 | 빈칸 | 솔버 경계 띠 규칙이 L0 가 아님 (등록된 과학적 HOLD) | 0 |
| `NOT_COMPUTED` | 빈칸 | 빈칸 | **기술적 실패** (입력 결손 · 무효 · 솔버 관문 · 온도 짝 · 관통 불일치) — 사유는 `ion_net_status_reason_hertz` (":" 앞이 코드) · 같은 빈칸이라도 무한대로 읽지 않는다 | 0 |

- 24 행을 통째로 지우면 전도 가능한 하위집합만 남는다.  권장 = **분류 (관통 여부) + 관통 조건부 연속 회귀** 2 단계 (v1.1 §5-2 B 와 같은 틀) 또는 상태를 명시적으로 다루는 모델.
- 유한 양수 T 의 회귀에는 `log10(T)` 를 **후보** 변환으로 쓸 수 있다 (130 의 T 가 1.97–1868 로 세 자릿수 — 큰 값은 문턱 근처 전도가 작아 비가 커진 것이지 오류 · 이상치가 아니다 · 임의 상한으로 자르지 않는다).  변환 · 스케일러 · 튜닝은 **훈련 폴드 안에서** — 사후에 가장 잘 나온 변환을 고르라는 승인이 아니다.

**3-2. T · √T · f · φ 는 독립 정보가 아니다** — T 를 예측하면서 f 와 φ 를 함께 특성으로 넣으면 항등식 복원으로 성능이 부풀 수 있다 (모델 내부 기술자라는 지위도 이런 목표 누설을 허용하지 않는다).
- `tau_ion_hertz`² = `tau2_ion_hertz` (상대차 ≤ 2.2e-16 · 두 표 전 행).
- `tau2_ion_hertz` = φ_SE,mc / `f_ion_hertz` 의 φ_SE,mc 는 **망 기록 (웹앱) 의 장부값**이다.  이 표의 `phi_se_mass_conserving` 은 수확기의 장부값으로, 둘은 **같은 정의 · 다른 MC union 실현**이라 (J20-s ③ *"웹앱 = 인계표 · MC 잡음 안"*) `|T − phi_se_mass_conserving/f|/T` 가 130: ≤ 7.7e-4 · 64: ≤ 4.4e-4 다 (예 `lhs00_000`: 망 기록 φ 0.250049 · 표 0.250086).  **ML 에서는 항등식으로 취급할 것** (누설) — 다만 바이트 단위 항등식은 아니다.
- v1.1 §3-3 의 항등식 (ε + φ_SE + φ_AM = 1 · CN ↔ 개수 등) 은 그대로.  새 항등식: `se_se_cn_aug` = `se_se_cn` + 2·`se_se_cn_aug_n_extra`/`n_SE_measured` · 다섯 파괴 단계 개수 합 = `n_total_AM_AM_force` = `am_am_n_contacts` · `frac_*_force_pct` = 100·n/전체 (소수 둘째 자리 반올림 · 합 ≈ 100) · `fracture_index_force` = (파편화 + 분쇄)/전체 (넷째 자리) · `area_<쌍>_mean` × `area_<쌍>_n` = `area_<쌍>_total` · `area_AM전체_SE_total` = AM_P–SE + AM_S–SE · `am_am_total_area` = 세 AM 쌍 합 · `se_se_cn_eff_area` = 2·`area_SE_SE_total`/(`n_SE_measured`·4πr_SE²).  **한 묶음에서 하나만 독립 타깃으로 센다.**

**3-3. 총량 열은 정규화해서 쓴다** — `area_*_total` · `am_am_total_area` (µm²) · `n_*_force_AM_AM` · `n_total_AM_AM_force` · `se_se_cn_aug_n_extra` 는 두께 · 입자 수에 비례한다 (v1.1 §3-4 와 같은 규칙).

**3-4. 벽 효과** — `se_se_cn_aug` 도 CN 이라 바닥 · 플래튼에 닿은 입자 쪽 이웃이 없다 (정의상 · 결함 아님) → `wall_touch_frac_*` 와 함께 (v1.1 §3-5).  τ 쪽은 경계 띠 (입자 띠 · `ion_net_band_rule` L0 194/194) 끝의 단락이 T 를 **낮추는** 방향으로 작용할 수 있다 (크기 ≤ 4r_SE/L 규모 · 띠 분율은 정본 인계표 `ion_net_band_frac_hertz` 0.05–0.16).

**3-5. σ 의 basis (Codex QV5)** — `f_ion_hertz` × σ₀ (3.0 mS/cm) 는 **L_mc 재척도** σ 다.  웹앱 화면 · 10-06 보고 덱의 σ_ion 은 **판 간격 해** (= 정본 인계표 `f_ion_hertz_gap` × σ₀ · 이 배포에 없음) 라 같은 σ 행으로 무표지 혼용하면 안 된다 (Codex 중앙값: 판 간격 해 0.2273 · 1.4122 ↔ L_mc 재척도 0.2104 · 1.2553 mS/cm — 오류가 아니라 **다른 두 양**).  f · T 자체는 무차원이라 두 basis 가 그대로 전달된다 (`L_basis` = L_mc · `phi_basis` = mass_conserving).

**3-6. 적격성 HOLD (v1.1 §3-7) 는 그대로** — `physical_target_status` 130: OK 71 · HOLD 59 / 64: OK 2 · HOLD 62.  τ 열의 `OK` 와 **다른 열**이다 (τ `OK` = 기술 게이트 · 적격성 `OK` = 경계 이탈 · 음수 기공률 조건 없음) — 둘 다 물리 검증 완료가 아니다.

## 4. 이름과 뜻이 다른 곳 (v1.1 §4 에 더한다)

| 열 | 실제 뜻 |
|---|---|
| `area_*_total` · `area_*_mean` · `am_am_*_area` | **A_dem_geometric** — 기하 교차 원판 π(rδ − δ²/4) · Hertz 탄성 πR\*δ 가 아니다 (≈ 1.99 배) · 소성 보정 아님 |
| `se_se_cn_eff_area` | "eff_area" 지만 **면적 비율 (무차원)** — SE 표면 중 SE–SE 접촉 원판 몫 |
| `*_force_*` · `fracture_index_force` | 힘 기반 (Auerbach) **마지막 프레임** 분류 — 손상 **하한** · 모델 규약 상대 지표 (§2-1 ⑥ 한정 ①–⑥) |
| `tau2_ion_hertz` | **수송 tortuosity factor T = φ_SE,mc/f** — 제곱근 아님 · √ 값은 `tau_ion_hertz`.  `tortuosity_SE_wall` (기하 최단경로 / 쌍의 z 간격 · v1.1 §4) 과 **다른 양** — 둘의 최소 조성도 다를 수 있다.  ⚠ 열 사전 `tortuosity_SE_wall` 줄의 *"(… τ_Laplace,eff = √tau2 · 이 표에 없음 …)"* 은 v1.1 기준 문장이다 — **v1.2 에는 있다** (이 열) |
| `f_ion_hertz` | 판 간격 해의 σ 비를 L_mc 로 재척도한 **무차원 f** — 망을 L_mc 에서 다시 푼 해가 아니다 · COMSOL 에 넣는다면 Porous Electrode 보정 **User defined (fl)** 칸 (같은 틀 L_mc · φ_mc · 10-04 D1) · Tortuosity 칸은 tau2 꼴 — **어느 쪽도 GUI 방정식 확인 없이 대입하지 않는다** |
| `ion_net_status_hertz` = `OK` | 기술 게이트 통과 — 물리 정확도 인증 아님 (§3-1) |
| `ion_sigma0_mScm` 3.0 | 간선 재료 σ₀ = **펠릿값** (Cronau 2021 SI S2c 하단) · f · T 계산에는 약분돼 들어가지 않는다 — Holm 접촉 저항과의 부분 이중계상 (방향 T↑) 은 절대값 쪽 문제 |

## 5. Physics 부록 (`*_physics.csv` · 필요할 때만)

- 열 = `case_id` · `f_ion_physics` · `tau2_ion_physics` · `tau_ion_physics` · `ion_net_status_physics` · `ion_net_status_reason_physics` · 메타 4.  규약 (194 행 상수 · 정본 인계표 열): 면적 모드 `physics` · 협착식 `mikic_psi_divide` · ψ `legacy_divide` (Hertz 는 `hertz` · `maxwell_halfspace`).
- 상태: 130 = OK 106 · NOT_PERCOLATING 24 (Hertz 와 같은 24) / 64 = OK 54 · **`MODEL_BELOW_CONTINUUM_BOUND` 10** = `lhsx_048` · `050` · `051` · `053` · `054` · `060` · `061` · `062` · `063` · `064` (T 0.89–1.00 · 값 유지).  T 범위 130: 1.79–2127 · 64: 0.89–2.47 (Hertz 64: 1.25–2.56 · 같은 10 건의 Hertz 1.25–1.39).
- **쓰는 법 (Codex QV3 그대로)**: 기본 학습 열에 자동 포함하지 않는다 (opt-in).  Hertz 와 Physics 는 **면적 선택과 협착식이 함께 다르다** — 차이를 "소성 접촉 면적만의 민감도" 로 읽지 않는다 (인과 분해가 아니다).  T < 1 의 10 행만 걸러 나머지 Physics 를 기본 학습에 쓰지 않는다 (T ≥ 1 을 기준으로 조밀 조성 일부를 고르는 선택이 되고, 남은 행의 물리 타당성을 인증하지도 못한다).  "이 구세대 모델의 출력을 모사하는 surrogate" 를 **등록하고** 만들면 Physics 전체를 대상으로 쓸 수 있다 — 물리 성능 예측과 다른 과제다.
- T < 1 의 원인 (Codex 재계산): 같은 망의 접촉 저항 없는 해 (CONTACT_FREE) 가 이미 연속체 한계 위로 전도를 세고 (입자 내부 저항 = 원기둥 πr² · d/2 — 겹치지 않는 단순입방 3×3×N 격자도 T → 2/3) · Physics 는 면적과 협착식이 함께 다른 규약이라 그것이 드러난 것.  ⛔ *"큰 면적이 접촉 저항을 지운다"* (legacy ψ 는 s = a/r > 0.4 에서 R_c 가 커진다) · *"정의상 1 이 바닥"* (조건부 변분 상한) 이라고 쓰지 않는다.

## 6. 들어 있지 않은 것 (의도적으로)

σ_ion · σ_e · κ 절대값 (f · T 만 — σ₀ 곱은 §3-5 basis 를 붙여서) · 전자 · 열 τ · 협착 전력 몫 (Codex QV4 — **별도 amendment**) · 판 간격 틀 `f_ion_*_gap` · 경계 띠 분율 `ion_net_band_frac_*` · 규약 상수 열 (`ion_net_area_mode_*` 등 — 이 README §5 에 적음) · Love–Weber 입자 응력 (`stress_*_lw` — frame_unverified · 194 인계 제외) · 옛 σ_VM 열 (`LHS-33` · 인계표에도 없음) · 소성 보정 coverage · `path_hop_area_*` (`LHS-32`) · δ 기반 파괴 · 구 부피 합 기공률 · 내부 QC · τ 출처 부록 (`*_tau_provenance.tsv` · 정본 폴더).

## 7. 알려진 한계 (v1.1 §7 에 더한다)

- **1세대 협착식** — Hertz = 반공간 Maxwell R_c = 1/(2σa) (a/r_SE 0.30–0.44 에서 R_c 1.7–2.4 배 과대) · Physics = ψ 분모 + 접촉별 상한값 면적 + ψ < 1e-4 절벽.  ⇒ 두 모드 모두 **ML 기술자 전용 · 실험 절대 대조 금지** (게이트 G6 HOLD — 순수 SE 망 런 · S3 판정 전).  z 한 축 (Tjaden 식 21 τ_C 와 직접 비교 금지) · 입자 모양 · CBD 차단 없음.
- 가능한 문장 (Codex QV5): *"이 고정 접촉망 · 면적 · 협착 · 경계 규약에서 계산한 값은 조성 X 에 따라 Y 로 변했다"* — 실물의 순위 · 인과 효과 · 측정된 tortuosity · 미세구조 고유 상수로 바꾸어 쓰지 않는다.  σ₀ 의 약분은 공통 배율 하나를 지울 뿐 내부 저항 · 면적 · 경계 편향을 제거하지 않는다.
- 이 배포의 검산은 **커밋된 배치 증거 · τ 원천과의 대조**다 — 망을 다시 푼 것이 아니다.  원 194 건의 atoms/contacts 바이트 · 실행 바이너리 · 완료 압력은 검토 범위 밖 (판정문 §2).
- 정본 폴더의 `reread_v12.py` PASS 는 다음 납품본까지 인증하는 관문이 아니다 (`RGLR4-01` · `02` — 수정 전까지 배포는 Codex 독립 대조 + 생성기 내장 대조로).

## 8. AI 도구에 붙여 넣을 프롬프트 (v1.1 §8 에 9–12 를 더한 것)

```
너는 고체전지 복합 양극 DEM 시뮬레이션 데이터로 ML 을 하는 조수다.  데이터 = lhs_release_20261006_v12.csv (130 행) ·
lhsx_release_20261006_v12.csv (64 행, 전부 SE-rich — 분포가 달라 따로 보거나 데이터셋 표지를 둔다).  한 행 = 300 MPa 로
압밀한 전극 침대 하나.  열 뜻은 README §2 · §4 와 *_columns.tsv 에 있다 (README 가 정정판).  *_physics.csv 는 부록이다 —
요청받기 전에는 쓰지 마라.

규칙 1–8 = v1.1 README §8 그대로 (X = 설계 노브 5 · 상수 · ID · 적격성 표지는 X 아님 · 누설 금지 · 빈칸 = N/A ·
항등식 · 총량 정규화 · 이름 주의 · HOLD 구분 · 중첩 CV).
9) 상태 열을 반드시 같이 읽어라.  ion_net_status_hertz = NOT_PERCOLATING (130 중 24) 이면 f_ion_hertz = 0 은 물리적 0,
   tau2_ion_hertz · tau_ion_hertz 의 빈칸은 무한대의 저장 표현이다 — 0 이나 큰 값으로 채우지 말고, 관통 여부를 먼저 분류한 뒤
   관통 행에서만 T 를 회귀하라 (log10(T) 는 폴드 안에서 고르는 후보 변환이다 · 큰 T 는 이상치가 아니다).
10) tau2_ion_hertz = 수송 tortuosity factor T = φ_SE,mc / f_ion_hertz (제곱근 아님) · tau_ion_hertz = √T · 둘과 f · phi_se_mass_conserving 은
   항등식으로 묶여 있다 (MC 잡음 ≤ 0.08 %) — T 를 예측하면서 f · φ 를 특성으로 넣지 마라.  tortuosity_SE_wall (기하학적) 과 다른 양이다.
11) 새 열의 항등식: 파괴 다섯 단계 개수 합 = n_total_AM_AM_force = am_am_n_contacts · frac_*_force_pct = 100·n/전체 ·
   fracture_index_force = (파편화+분쇄)/전체 · area_<쌍>_mean × area_<쌍>_n = area_<쌍>_total · se_se_cn_aug = se_se_cn + 2·n_extra/n_SE_measured ·
   se_se_cn_eff_area = 2·area_SE_SE_total/(n_SE_measured·4πr_SE²).  한 묶음에서 하나만 타깃으로 세라.  면적 · 개수 열은 총량이다.
12) 전도도 절대값은 없다.  f · T 는 이 고정 접촉망 · 면적 · 협착 · 경계 규약 안의 모델 기술자다 — 실험값 · 실물 순위 · COMSOL 물성으로
   바꾸어 쓰지 마라.  Physics 부록을 쓰더라도 기본 학습 열에 섞지 말고, T < 1 인 10 행만 지우고 나머지의 타당성을 주장하지 마라.
```

## 9. 출처 · 재현 (새 계산 없음 — 정본 인계표의 열 부분집합)

- 정본 인계표 v1.2 (1저자 WSL 10-06 02:11 KST · `docs/data/lhs_network194_11fcf91e8/handover_v12_20261006/wsl_run_20261006.md` 에 명령 · 출력 그대로): 접촉 단계 `d1ec42fba` + 망 배치 `11fcf91e8` (194/194 · 봉인 감사 SEALED_LEGACY 194) → 생성기 `scripts/lhs_design_dataset.py --export-handover … --webapp-groups contact,percolation,f1,fracture,area,tau --tau-results …`.
- 배포 표 = 인계표의 열 부분집합 (`scripts/lhs_release_build.py` — 만들 때 대조 내장 · 열 목록 = v1.1 배포 열 사전 첫 열 + `--add`):
  ```
  H=docs/data/lhs_network194_11fcf91e8/handover_v12_20261006
  A567="--add am_am_mean_area --add am_am_total_area --add area_AM_P_AM_P_mean --add area_AM_P_AM_P_total --add area_AM_P_AM_S_mean --add area_AM_P_AM_S_total \
        --add area_AM_P_SE_mean --add area_AM_P_SE_total --add area_AM_S_AM_S_mean --add area_AM_S_AM_S_total --add area_AM_S_SE_mean --add area_AM_S_SE_total \
        --add area_AM전체_SE_mean --add area_AM전체_SE_total --add area_SE_SE_mean --add area_SE_SE_total \
        --add frac_fragmentation_force_pct --add frac_intact_force_pct --add frac_microcrack_force_pct --add frac_multicrack_force_pct --add frac_pulverization_force_pct \
        --add fracture_index_force --add n_fragmentation_force_AM_AM --add n_intact_force_AM_AM --add n_microcrack_force_AM_AM --add n_multicrack_force_AM_AM \
        --add n_pulverization_force_AM_AM --add n_total_AM_AM_force --add se_se_cn_aug --add se_se_cn_aug_h_spread_sim --add se_se_cn_aug_n_extra --add se_se_cn_aug_std \
        --add se_se_cn_eff_area --add se_se_cn_eff_area_perc"
  AH="--add f_ion_hertz --add tau2_ion_hertz --add tau_ion_hertz --add ion_net_status_hertz --add ion_net_status_reason_hertz"
  AM="--add ion_sigma0_mScm --add ion_sigma0_T_C --add phi_basis --add L_basis"
  python3 scripts/lhs_release_build.py --handover $H/lhs_handover_v12_20261006.csv --columns-from docs/data/lhs_release_20261001_v11/lhs_release_20261001_v11_columns.tsv \
      $A567 $AH $AM --out docs/data/lhs_release_20261006_v12/lhs_release_20261006_v12
  # 64 는 --handover $H/lhsx_handover_v12_20261006.csv · --columns-from …/lhsx_release_20261001_v11_columns.tsv · --out …/lhsx_release_20261006_v12
  # 부록 = --columns-from <case_id 한 줄짜리 열 사전> --add f_ion_physics --add tau2_ion_physics --add tau_ion_physics --add ion_net_status_physics --add ion_net_status_reason_physics $AM
  ```
  네 표 모두 `✓ 대조 통과` (배포 ⊆ 인계표 · 행 · 순서 · 값 · 열 사전 행) · v1.1 CSV 와 칸 단위 대조 = 130 × 89 + 64 × 88 = **17,202 칸 차이 0**.
- 원자료: 수확 `docs/data/{lhs,lhsx}_descriptors_cov_1e09f661d/` · 웹앱 접촉 단계 `docs/data/{lhs,lhsx}_webapp_contact_d1ec42fba/` · union `docs/data/lhs_union_20260927/` · 퍼콜 감사 `docs/data/lhs_perc_audit_20261001/` · 망 배치 `docs/data/lhs_network194_11fcf91e8/` (τ 원천 `net194_tau_sources_20261006.tar.gz` · 봉인 감사 `seal_audit.tsv` · 실행 등록 `docs/reviews/lhs_network_batch_registration_20261005.md`).
- 판정: J20-s (⑤⑥⑦ · 10-04) · Codex RINT G1 · RGL · RGLR · RGLR2 · RGLR3 · 5차 (`docs/reviews/codex_review_rglr3_reverify_20261006.md`) · τ 명명 규약 (CLAUDE.md ★★ τ 블록 · `docs/reviews/tau_conventions_judgment_v2_20261003.md`).
