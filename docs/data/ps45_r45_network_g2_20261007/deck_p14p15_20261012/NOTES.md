# 2차년도 최종 덱 p14 · p15 막대그래프 갱신 (2026-10-12)

- **p15 σLi+** : Tabor · σ0 3.0 → **Hertz · σ0 1.5 mS cm−1** (주 값 · 보고 기준)
- **p14 Tortuosity** : Tabor → **Hertz** (주 값) — 변형 b = Hertz 막대 + Tabor ○ 표지 (둘 중 1저자 선택)
- p14 Coverage · p15 σe− : 새로 그리지 않음 (§6)

## 1. 자료 · 산술

원천 = `docs/data/ps45_r45_network_g2_20261007/network_cases.tsv` (세대 2 망 · 실행 `0801d4ceb` · 다섯 행 `ion_net_status` OK ·
`psi_placement_physics = multiply` · `ion_net_generation = g2` · 솔버 σ0 = 3.0) · 조성 = `P_S` 열.

- σLi+ (σ0 1.5) = `sigma_full_mScm_hertz` × 0.5 — 망 σ 는 σ0 에 정확히 비례 (같은 폴더 README §σ₀) · 다시 계산 없음
- 수송 tortuosity = `tau2_ion_hertz` · 변형 b 의 ○ = `tau2_ion_physics` — tau2 = φ_SE·σ0/σ_eff 라 σ0 가 약분된다
- `make_charts.py` 가 실행마다 검산: 아래 기대값 셋 일치 · 항등식 tau2 = `phi_se`·σ0/`sigma_full_*` 최대 상대차 2.8e-6 (Hertz) · 1.6e-6 (Tabor) —
  σ0 = 1.5 와 ×0.5 값을 넣어도 같음 · 질량 보존 틀 (`phi_se_mass_conserving` / `f_ion_*`) 차 0

## 2. 검증한 값

| PC:SC | 0:10 | 3:7 | 5:5 | 7:3 | 10:0 |
|---|---|---|---|---|---|
| `sigma_full_mScm_hertz` (σ0 3.0) | 0.117497 | 0.146029 | 0.162808 | 0.178588 | 0.167574 |
| **σLi+ Hertz · σ0 1.5 (새 p15)** | **0.0587** | **0.0730** | **0.0814** | **0.0893** | **0.0838** |
| (참고) σLi+ Tabor · σ0 1.5 | 0.1032 | 0.1304 | 0.1454 | 0.1618 | 0.1416 |
| **수송 tortuosity · Hertz (새 p14)** | **7.24** | **5.97** | **5.45** | **5.03** | **5.29** |
| 수송 tortuosity · Tabor (변형 b ○) | 4.12 | 3.35 | 3.05 | 2.78 | 3.13 |

## 3. 덱에서 바뀌는 값 (옛 막대 높이 = PDF 벡터 판독 `_inspect/deck_bar_values.json`)

| | 0:10 | 3:7 | 5:5 | 7:3 | 10:0 | 정체 |
|---|---|---|---|---|---|---|
| 옛 p15 σLi+ | 0.210 | 0.260 | 0.290 | 0.320 | 0.280 | `sigma_full_mScm_physics` (**Tabor** · σ0 3.0) 소수 2 자리 |
| 옛 p14 Tortuosity | 4.10 | 3.40 | 3.10 | 2.80 | 3.10 | `tau2_ion_physics` (Tabor) 소수 1 자리 (3:7 = 3.3457 → 3.35 → 3.4 이중 반올림) |

- p15 는 σ0 (3.0 → 1.5) 와 면적 규약 (Tabor → Hertz) **둘 다** 바뀐다 → 새 값 = 옛 값의 0.28–0.30 배.  p14 = 옛 값의 1.71–1.80 배.
- 순서는 그대로: σLi+ 최소 0:10 · 최대 7:3 / 수송 tortuosity 최대 0:10 · 최소 7:3.  5:5 ↔ 10:0 만 Tabor 와 뒤집힌다 (Hertz σ 0.0814 < 0.0838 · tortuosity 5.45 > 5.29).
- ⚠ 10:0 대비 7:3 = σ +6.6 % · tortuosity −4.9 % (Hertz) — 같은 폴더 README (10-12) 판정 = 시드 산포 안 · "7:3 최적" 확정 못 함.
  p14 *"7:3에서 최솟값"* · p15 *"7:3에서 최대"* 문장에 10-12 비준 한정어를 붙일지 = 1저자 · 그 문장의 숫자 (4.12 → 2.78 = Tabor) 도 Hertz 면 **7.24 → 5.03**.

## 4. 각주 문안 (권고)

- p15 σLi+: **σ0 = 1.5 mS cm−1 (LPSCl 펠릿 문헌 범위) · Hertz 접촉 면적 기준 (주 값) · Tabor = 접촉 면적 규약 민감도**
- p14 수송 tortuosity: **수송 tortuosity = φ_SE·σ0/σ_eff — σ0 와 무관** (변형 b 면 + *"막대 = Hertz (주 값) · ○ = Tabor (접촉 면적 규약 민감도)"*)
- (선택) τ 명명 규약의 정의 병기에는 *"제곱근 아님"* 이 붙는다 (CLAUDE.md τ 명명 규약)

## 5. 서식 (덱 판독 → 그대로 재현)

- 막대 색 0:10 → 10:0 = `#FDE724` `#B4DD2B` `#6BCD58` `#35B778` `#1E9C88` · 테두리 검정 0.34 pt · 막대 폭 = 간격의 50 % · x 범위 = 범주 ± 0.8 (Origin X 0.2–5.8)
- 축 왼쪽 · 아래만 0.68 pt · 바깥 틱 2.0 pt (y minor 1.0 pt · 주 눈금 사이 1 개) · 주 눈금 4 개 · 눈금 9.22 pt / 축 제목 11.25 pt (= Origin 28 : 34 의 비) · 그림 영역 119.5 × 119.6 pt
- 새 y 범위: σLi+ 0.04–0.10 · Hertz 4.5–7.5 · Hertz + Tabor 2–8 — 덱처럼 바닥이 0 이 아니다 (막대 높이 비 ≠ 값 비)
- **바꾼 두 곳**: ① 축 제목 *"Tortuosity"* → **"Transport tortuosity"** (τ 명명 규약 · 각주의 "수송 tortuosity" 와 같은 이름 — 덱 표기를 원하면 축 제목만 되돌림)
  ② x 눈금 **"5:7" = 덱 오타** (p14 Tortuosity · Coverage · p15 σLi+ · σe− 네 그림) → 새 그림은 "5:5" · 남겨 두는 Coverage · σe− 도 고칠 것
- 가장 빠른 길: 덱의 Origin 그래프에 새 CSV 의 B 열 (변형 b 는 B · C) 만 바꿔 넣고 y 범위만 조정.  Excel 로 열면 "3:7" 이 시각으로 바뀔 수 있다 — Origin 가져오기 때 A 열 = Text.
- 미리보기 글꼴 = Liberation Sans (Aptos 없음 · Arial 과 글자 폭 같음) · 한글 NanumGothic.  SVG = 슬라이드 크기 그대로 (100 % 로 붙이면 옛 그림과 같은 배율) · 글자는 글자로 둠.
- 범례 (변형 b) 는 그림 영역 밖 위 — 각주로 옮겨도 된다.

## 6. ⚠ 남겨 둔 두 그림 (1저자)

- **Coverage (p14 오른쪽)**: 이 TSV 에 coverage 열이 없어 자리표시만.  덱 막대 48.9 · 55.0 · 58.1 · 63.4 · 53.4 % = 세대 1 망 로그
  (`docs/data/ps45_r45_network_20261006/logs/*.stages.json`) 의 **Physics (Tabor 계열) 피복률** 을 AM 입자 수로 평균한 값 (48.86 · 55.00 · 58.10 · 63.36 · 53.38) 과 같다
  [관찰 · 산술].  같은 로그의 Hertz = 16.8 · 18.8 · 19.9 · 21.7 · 20.1 % → Tortuosity 를 Hertz 로 바꾸면 한 장 안에서 면적 규약이 갈린다 · 그대로 둘지 = 1저자
  (참고: LHS 인계는 10-01 J20-m 에서 Physics 피복률을 빼고 기하면적만 넘겼다).
- **σe− (p15 아래)**: 덱 그대로 = `electronic_sigma_full_mScm_physics` (Physics · σ_AM 50) 소수 1 자리 (6.2 · 3.9 · 2.7 · 1.9 · 1.7).  기준 = 외부 (Codex) 검토 중
  (`docs/reviews/codex_ps45_sigma_e_basis_request_20261012.md`) — 결정 뒤 따로 그린다.

## 7. 파일 (이 폴더)

| 파일 | 내용 |
|---|---|
| `p15_sigmaLi_hertz_s0_1p5.csv` · `.png` · `.svg` | σLi+ · Hertz · σ0 1.5 |
| `p14_tortuosity_hertz.csv` · `.png` · `.svg` | 수송 tortuosity · Hertz (변형 a) |
| `p14_tortuosity_hertz_tabor.csv` · `.png` · `.svg` | 수송 tortuosity · Hertz 막대 + Tabor ○ (변형 b) |
| `preview_p14a_hertz.png` · `preview_p14b_hertz_tabor.png` | p14 배치 그대로 (왼쪽 새 Tortuosity · 오른쪽 Coverage 자리표시 · 각주) |
| `preview_p15.png` | p15 배치 그대로 (위 새 σLi+ · 아래 σe− 자리표시 · 각주) |
| `make_charts.py` | 생성기 — `cd <이 폴더> && python3 make_charts.py` (TSV 읽기만 · 검산 실패면 멈춤) |
| `_inspect/` | 덱 판독 근거 (PDF 읽기만 · `python3 -I`): 막대 값 `deck_bar_values.json` (`read_bar_heights.py <덱 PDF>`) · 색 · 글꼴 · 선 `charts_dump.txt` (`charts_pdf.py <덱 PDF> <출력 폴더>`) · 축 · 틱 `axes_dump.txt` · 덱 원 그림 잘라낸 것 `deck_p14_tortuosity_300dpi.png` · `deck_p15_sigmaLi_300dpi.png` · 같은 배율 비교 `compare_deck_vs_new_300dpi.png` — 덱 PDF 자체는 리포에 넣지 않는다 |

CSV = 리포 Origin 규약 (1 줄 Long Name · 2 줄 Units · 자료 · utf-8-sig) · `Basis` 열 = 출처 글 (그리지 않음).  PNG 300 dpi.
