# LHS 인계 체크리스트 — 확보할 것 · 넘겨줄 것 (2026-09-29 · 1저자 요청 *"체크리스트 만들어서 확보할 거 · 넘겨줄 거로 나눠서"*)

정본은 `docs/reviews/lhs_handover_judgments_20260924.md` (J19 · J20 · J20-a · J20-b · J20-c) 이고, 이 파일은 **보기 쉬운 지도**다.  상태가 바뀌면 여기 표를 같이 고친다.

## 1. 한눈에 — 지금 어디까지 있나 (2026-09-29 밤)

저장된 파일 = `docs/data/lhs_handover_20260928.csv` (130 행 × 119 열) · **`docs/data/lhsx_handover_20260929.csv` (64 행 × 121 열 · 09-29 밤 생성)** + 각각의 열 사전 `*_columns.tsv`.
64 는 수확 (`docs/data/lhsx_descriptors_20260925/`) + union (`docs/data/lhs_union_20260927/lhsx64_union.tsv`) + 변환 설계 (`docs/data/lhsx_design_adapted_20260929.csv`) 로 같은 생성기에서 만들었다.

| 묶음 | 130 건 | 64 건 (lhsx) | 넘길까 |
|---|---|---|---|
| 설계 값 (입경 · 조성 · RVE · 하중 …) | ✅ 저장 | ✅ **변환됨** (`scripts/lhsx_design_adapter.py` · 130 전용 추정 열 10 은 없음 · lhsx 원래 값은 `lhsx_*` 열로 같이) | ✅ |
| **두께** `thickness_mass_conserving_um` (+ wall gap · envelope 는 내부) | ✅ 저장 | ✅ 저장 (25.0–44.7 µm) | ✅ |
| **porosity union** `porosity_union_exact_pct` + `se_rich` 표지 | ✅ 저장 | ✅ 저장 (5.43–9.43 % · se_rich 64/64) | ✅ **union 만** |
| φ_SE · φ_AM (구 부피 합 규약) | ✅ 저장 | ✅ 저장 (φ_SE 0.52–0.92) | ✅ 규약을 열 사전에 표기 |
| coverage (AM_P · AM_S · 전체 · 이름은 hertz 지만 A_dem_geometric) | ✅ 저장 (mono 30 은 P · S 둘 다 빈칸 · 값은 전체 열) | ✅ 저장 (mono 16 도 같음) | ✅ 이름 주의 표기 |
| τ (굴곡도) | 상태 열만 · 값은 보류 (`LHS-08` 14/130) | ⬜ | ⏸ 벽 기준 τ 판정 뒤 |
| **① 접촉 위상** — z_SE-SE mean·σ · z_AM-SE · AM_P/AM_S–SE CN · surface-weighted · z_AM-AM · 접촉 수 · 벽 접촉 비율 | ⬜ 계산 전 (감사 ✅ 적격) | ⬜ | ✅ **다음에 저장** |
| **② 퍼콜레이션** — percolation_pct · n_components · n_large · electronic_*_fraction · se_se_cn_*_perc | ⬜ 계산 전 (감사 ✅ 적격 · 비관통 24 건은 빈칸) | ⬜ | ✅ ① 다음 |
| ③ φ_SE(웹앱) · ④ 협착 저항 · σ_VM · ⑤ F1 근접쌍 · ⑥ Auerbach · ⑦ A_dem_geometric | 감사 전 | — | ⛔ 감사 끝나기 전엔 안 넘김 |
| 내부 전용 — sphere-sum porosity 4 종 · 두께 wall gap/envelope/pushback · 경계 QC · sha · 상태 열 | ✅ 저장 | ✅ 저장 (hold NEGATIVE_POROSITY 60 = 구 부피 합의 음수 · union 은 전부 양수) | ✗ 내부 표에만 |

⚠ **mono 케이스 (130 중 30 · 64 중 16)** — 2-type 덱은 AM 이 한 종류라 수확기가 상을 `AM` 으로만 라벨한다 (P · S 는 반지름으로 붙인 이름).  그래서 `coverage_AM_P` · `_AM_S` 가
**둘 다** `N_A_PHASE_ABSENT` (빈칸, 0 아님) 이고 값은 `coverage_AM_total_hertz_pct` 에 있다.  같은 이유로 `n_AM_P_measured` · `n_AM_S_measured` 가 둘 다 빈칸이라 **실측 AM 개수가 인계표에 안 실린다**
(수확 JSON `phase_counts.AM` 에는 있다) — 원장 `LHS-21` · 생성기에 `n_AM_measured` 열 추가 (반례 먼저 · 비준 ⓑ 와 함께).

## 2. 확보할 것 (할 일 · 순서대로)

| # | 할 일 | 누가 | 상태 |
|---|---|---|---|
| 1 | ② 감사 산출물 반입 — `~/lhs_perc_audit_20260929/perc_audit.tsv · .json` 보내기 → `docs/data/lhs_perc_audit_20260929/` 커밋 | 사용자 → 나 | ⬜ |
| 2 | **재수확 v3** (130 + 64 · 벽 τ · 벽 접촉 비율) — WSL 명령 = J20-c · **한 건 먼저** (`--case lhs00_000` · `--case lhsx_001`) | 사용자 (WSL) | ⬜ 비준 ⓐ |
| 3 | **웹앱 배치** (130 + 64) — ① ② 값이 여기서 나온다 (③~⑦ 도 계산되지만 저장은 감사 뒤) · 인계표 재생성 단계 [4] 는 돌리지 않는다 | 사용자 (WSL) | ⬜ 비준 ⓐ |
| 4 | 생성기 코드 — ① 만 저장하는 옵션 (`--webapp-groups contact`) · ~~64 설계 변환 어댑터~~ ✅ (09-29 밤 · 14/14) · 배포 프로필 (`--deliver`) — 반례 먼저 | 나 | ⬜ 비준 ⓑ ⓒ |
| 5 | 인계표 재생성 130 + 64 → 열 사전 (`*_columns.tsv`) → 커밋 · ① 열 설명을 열 사전에 그대로 | 나 | ⬜ (2 · 3 · 4 뒤) |
| 6 | 결정 셋 — `LHS-20` (top_reachable_pct · ionic_active_pct 넘길지) · ② 열 사전 문구 (J20-b ⓒ) · 배포 프로필 (§3) | 사용자 | ⬜ |
| 7 | ② 열 저장 (같은 배치 산출에서) → ③ φ_SE 감사 → ④ → ⑤ → ⑥ → ⑦ (묶음마다 감사 → 저장) | 나 | ⬜ 순서대로 |
| 8 | τ — 벽 기준 τ 새 열 판정 (`LHS-08`) → 넘길지 결정 | 나 → 사용자 | ⬜ |

## 3. 넘겨줄 것 (배포 묶음 · 제안 — ⬜ 비준 ⓒ)

| 파일 | 내용 |
|---|---|
| `lhs_handover_<날짜>.csv` (130) · `lhsx_handover_<날짜>.csv` (64) | 설계 + 두께 (mass-conserving) + porosity union + `se_rich` + φ_SE · φ_AM + coverage 3 + ① 접촉 위상 + ② 퍼콜레이션 (+ 뒤에 ③~⑦ 감사 끝나는 대로) |
| `*_columns.tsv` (열 사전) | 열마다 출처 · 판정 · 뜻 · 분모 · 주의 (벽 효과 · 파생 · 총량 · 빈칸 = N/A) |
| README | 규약 한 줄씩 — union 은 상한 규약 · 구 부피 합은 안 넘김 · τ 보류 · 64 는 SE-rich (SE/고체 0.51–0.85) |

**안 넘기는 것**: sphere-sum porosity 와 그 변형 4 종 (겹침 이중계상 · SE-rich 에서 음수) · 감사 전 묶음 ③~⑦ · τ 값 (판정 전) · 내부 QC · 상태 열.

## 4. 왜 porosity 는 union 만 넘기나 (1저자 09-29 *"union 정도만"*)

- 구 부피 합 (ε_sphere) 은 입자 겹침을 두 번 세어 SE 가 하중을 지는 침대에서 **음수**가 된다 — 130 중 음수 18 (HOLD) · se_rich 표지 21 · 64 중 음수 60.
- union (겹침을 뺀 정확한 부피) 은 194 건 **전부 양수** (`docs/data/lhs_union_20260927/`).
- 단 union 은 소성 압축에서 밀려난 재료를 고체로 안 세는 **상한 규약**이다 (CLAUDE.md E_SE 절 · ε_sphere 가 생산 규약) — 열 사전에 그대로 적고, 내부 표에는 둘 다 남긴다.

## 5. ① 접촉 위상 열 — 한 줄씩 (뜻은 생성기 `WA_DEFINE` · 상세 J20-a)

| 열 | 뜻 (쉽게) | 주의 |
|---|---|---|
| `se_se_cn` · `se_se_cn_std` | SE 한 알이 SE 몇 알과 닿아 있나 — 전 SE 평균과 산포 | 벽에 닿은 알은 그쪽 이웃이 없어 낮게 나온다 |
| `am_se_cn_mean` | AM 한 알이 SE 몇 알과 닿아 있나 — AM_P + AM_S 개수 평균 | 상별 값의 평균이라 **파생** |
| `AM_P_se_cn_*` · `AM_S_se_cn_*` | 위 값을 큰 AM · 작은 AM 따로 (mean · std · median · max) | 그 상이 없으면 빈칸 |
| `am_se_cn_surface_weighted` | AM 표면적으로 가중한 AM–SE 접촉 수 | 큰 AM 이 지배 → 벽 효과 큼 · **파생** |
| `am_am_cn` · `am_am_cn_std` · `am_am_n_contacts` | AM 한 알이 AM 몇 알과 닿아 있나 (P–S 교차 포함) · 총 AM–AM 접촉 수 | 접촉 수는 총량 |
| `area_<쌍>_n` | 쌍 종류별 접촉 **개수** (덤프 행 수) | 면적 아님 · 총량 → 입자당 · 부피당으로 나눠 쓸 것 |
| `wall_touch_frac_<상>_<floor\|plate>` | 상별로 바닥 · 플래튼에 닿은 알의 비율 | 위 벽 효과를 가르는 설명 변수 (재수확 v3) |

64 건은 SE-rich 라 `se_se_cn` 이 130 (중앙 4.75) 보다 높게 나온다 (J19 실측 9.6).
