# ps45 다섯 조성 — 힘 · 응력 지표 (10-07 · 발표 그림 ① · ②)

- **무엇**: 1저자 10-07 발표 자료 — *"힘 관련 term … 이런식으로 plot"* → 고른 둘 (*"① · ② 정도면 좋을듯"* · ③ 균열 단계는 뺌).
  ① 상별 입자 응력 비 (Love–Weber) · ② 접촉 힘 몫 · 쌍별 평균 법선력.  PC:SC 0:10 · 3:7 · 5:5 · 7:3 · 10:0 (ps45 r4.5 · 6 mAh 침대 다섯).
- **원자료**: `raw/ps45_force_metrics.tgz` (1저자 WSL 10-06 망 배치 작업 폴더 `~/ps45_network_20261006` 의 `network_cases.tsv` + `work/results/<id>/full_metrics.json` 5 개 ·
  21,538 B · sha256 `0b3d7b2339eb05b558b437d3a9862981e386c0ac8a408f9cd1fa366ccf4ed5bb`).  실행 = 10-06 06:5x KST (파일 시각은 WSL UTC 10-05 21:5x) · 코드 `04756e749` ·
  케이스 ID = `../ps45_r45_network_20261006/` 과 같다.  ⚠ 접촉 분석 단계 코드 (analyze_contacts · dem_analysis_core · fracture_model) 는 `04756e749` → `0801d4ceb` 무변경 ⇒ 지금 코드의 값과 같다 (세대 2 가 바꾼 것은 망 단계뿐).
- **만든 것**: `make_force_figs.py` (값 = full_metrics 그대로 · 새 계산은 ② 힘 몫 = 쌍 묶음의 평균 법선력 × 접촉 수 ÷ 전체 뿐) → CSV 넷 (Origin 머리 세 줄: Long Name · Units · Comment) + `figs/` 미리보기 PNG 넷.
  다시 만들기: 묶음을 새 빈 폴더에 풀고 `python3 make_force_figs.py <푼 폴더> <출력 폴더>` (`--with-fracture` = ③ 도 — 발표에서는 뺌).

## ① 상별 입자 응력 비 (`stress_ratio_lw_all.csv` · `_nowall.csv`)

| PC:SC | 0:10 | 3:7 | 5:5 | 7:3 | 10:0 |
|---|---|---|---|---|---|
| PC | — | 1.336 | 1.603 | 1.508 | 2.288 |
| SC | 1.737 | 1.657 | 1.610 | 1.566 | — |
| SE | 0.979 | 0.986 | 0.990 | 0.994 | 0.997 |

- 정의 = 입자별 Love–Weber 응력 (접촉 힘 × 가지 벡터 ÷ 입자 부피) 의 von Mises 값을 상별 평균 ÷ 전체 입자 평균 (`dem_analysis_core.calc_love_weber_stress` · full_metrics `stress_ratio_<상>_lw`) — 입자 수는 SE 가 대부분이라 전체 평균 ≈ SE 평균.
- 벽 제외 (`_lw_nowall`) 거의 같다 — 벽 접촉 입자 PC 6–9 % · SC 2–3 % · SE 2 %.  다섯 케이스 `stress_lw_status` = OK · 일관성 검사 (7:3: 힘 분해 상대 3.1e-6 · 전체 비리얼 상대 1.5e-5 —
  전역 부호 · 척도 검사이지 상 배분의 증명 아님 · 코드 문구).
- ⚠ 각주 필수: **"모델 내부 비교 — 응력 기준틀 미인증"** (Codex 10-05 Q5 · 194 인계에서 LW 열 제외 · `RGLR-03` 뒤).  옛 열 `stress_ratio_<상>` (stress/atom 50/50 분할) 은 `LHS-29` (P1) 라 쓰지 않는다.

## ② 접촉 힘 (`contact_force_share.csv` · `contact_force_mean.csv`)

| PC:SC | 0:10 | 3:7 | 5:5 | 7:3 | 10:0 |
|---|---|---|---|---|---|
| 힘 몫 AM–AM (%) | 33.1 | 25.4 | 21.2 | 17.0 | 19.8 |
| 힘 몫 AM–SE (%) | 37.2 | 38.3 | 37.9 | 36.4 | 30.5 |
| 힘 몫 SE–SE (%) | 29.7 | 36.3 | 40.9 | 46.6 | 49.6 |
| 평균 법선력 SE–SE (µN) | 34.5 | 35.4 | 35.1 | 36.3 | 29.1 |
| 〃 PC–PC (µN) | — | 6,247 | 7,475 | 6,477 | 7,032 |
| 〃 SC–SC (µN) | 1,501 | 1,425 | 1,362 | 1,333 | — |

- 평균 법선력 = full_metrics `fn_<쌍>_mean` (`dem_analysis_core.calc_contact_force_distribution` · 덱 축척 환산 µN = F_deck × 1e6/scale) · 접촉 수 = `area_<쌍>_n`.
  AM–AM 접촉 = 전체 접촉의 0.39 % (7:3) – 1.6 % (0:10).
- ⚠ 각주 필수: **"접촉 힘 합의 몫 — 판 하중 분담 아님"** (판 반력 분율로 검증된 양이 아니다 · 하중 분담 두 규약은 CLAUDE.md f_AM 절).
- 해석 (모델 안 · 크기와 강성 효과를 떼지 않음 — 1저자에게 보고한 문장): 단단하고 큰 활물질끼리의 소수 접촉이 힘의 큰 몫 (힘 사슬) · PC 가 많을수록 활물질 접촉이 줄어 SE 망이 힘 경로의 중심 · 7:3 = AM–AM 몫 최소 · PC ≈ SC 응력 (가장 치밀한 조성과 같은 자리).
