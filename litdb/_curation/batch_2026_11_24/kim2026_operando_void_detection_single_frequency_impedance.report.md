# 끝 보고 — kim2026_operando_void_detection_single_frequency_impedance (2026-11-24 · litdb-curator)

쓴 파일: `litdb/papers/kim2026_operando_void_detection_single_frequency_impedance.md` (≈510 줄 · 표 16 개 칸수 검사 0 건) · `litdb/figures/kim2026_operando_void_detection_single_frequency_impedance/` (PNG 19 장 + figures.json) · 이 보고 파일.
공유 파일 · git 은 안 건드렸다 (메인 체크포인트 커밋이 digest · 그림을 이미 담고 있다 — 이 보고 파일만 새로 생김). `litdb/figures/_sources.json` 은 추출 도구가 다시 썼다 (621편 색인 · 손으로 안 고침).
`build_index.py --check`: 이 slug 는 "어느 인덱스에도 없음 [dft]" · "comparison_vs_ours.md 미편입" 두 곳에만 뜬다 — (a) (b) 를 넣으면 풀린다.
웹앱 확인 (읽기만): `_paper_pis` → `['sakamoto']` · 원소 태그 Ag · Cl · La · Li · O · P · S · Ta · Zr · 그림 주석 19/19 키 파싱 · `methods: EIS, FEM, SEM` 은 METHOD_MAP 밖이라 용어 링크 0 (정상 — 선언이 있어 본문 토큰 스캔은 꺼진다).
talks 인입 대기열: 이 논문 없음 (grep) → 역링크 할 일 없음. `extract_figures.py --audit` · `--audit-src`: 이 편 지적 0.

## (a) INDEX.md 행

넣을 절: **`## ✅ Digest 완료 (paper-level)`** 표 맨 위 (새 행 먼저). `## 🧲 계면 점착 · 인터레이어 트랙` 은 머리말이 'G_c · 벌크 역학 실측 값' 절이라 이 논문 (점착 값 0) 과 안 맞는다 — 형제 lee2022 처럼 그 절에 모으려면 행 안의 '⛔ 점착 W · G_c 값 없음' 표시를 그대로 둔다.

```
| `papers/kim2026_operando_void_detection_single_frequency_impedance.md` **(본문 10 pp + SI 12 pp · 크롭 19장 (도구 18 중 다시 자름 1 — 그림 2 · 손 크롭 1 = 그림 3 (번호 공백 해소) · 자동 캡션 6개 인쇄 캡션으로 교정) 중 크롭 13장 실독 + 확대 렌더 9 · SI 그림 5장 (S1–S4 · S6) 은 쪽 렌더로만 · 표 1장 PDF 텍스트 · 2026-11-24)** | 🏷 **Jeff Sakamoto 공저** · **[외부·exp + 3-D 주파수 영역 임피던스 FEM (COMSOL)·Li₆PS₅Cl (comp1 조성) · Ta-LLZO+Ag 무음극 Li 박리 공극의 단일 주파수 조기 검출 · DFT 0 · ⛔ 점착 W · G_c 값 없음]** ✅ Younggyu Kim/Jonathan Gjerde/Hao Zheng (공동 1저자)/W. Beck Andrews/Daniel W. Liao/**Jeff Sakamoto\***/**Katsuyo Thornton\***/**Neil P. Dasgupta\*** (Univ. of Michigan · UC Santa Barbara · MUSIC EFRC), "**Operando Detection of Void Formation during Lithium Stripping in Solid-State Batteries Using Single-Frequency Impedance Analysis**" — ***ACS Electrochem.* 2, 384–393 (2026)**, DOI `10.1021/acselectrochem.5c00417`. Cu\|Li (in situ 2 mAh cm⁻²)\|SE\|Li · DC 0.4 + AC 0.1 mA cm⁻² · LPSCl 0.4 MPa / LLZO (Ag 100 nm) 5 MPa · +20 % 문턱: [LPSCl] −Im (10–60 Hz) ≈1.0 vs 분극 ≈1.42 · Re ≈1.45–1.48 mAh cm⁻² (판독) · 10² Hz 단일 주파수 1.245 vs 1.49 (판독) · [LLZO] −Im 0.17–0.47 vs 분극 0.93 (판독) · 5 MPa (RT · 60 °C) 대조에서 조기 상승 없음 · 박리 끝 ≈1.57 → ≈1.9 (판독) · Table S1 R-CPE 는 두 계면 · 0.283 cm² 로 읽어야 `Fig. S7` 재현 (카드 산술) · f_int 66.6 Hz (카드 산술) · **3-D 모델 결과 전부 = 1-D 활성 면적 식 Z_int/(1−φ) (카드 산술) — '다차원 모델 필요' · '공극 = 축전기 층' 을 그림이 받치지 않음** · Re 둔감 = 직렬 + SE 희석 (계면 몫 13 %, 카드 산술) · 가장 크게 자란 원호는 분석 창 10–10³ Hz 밖 (판독) · LLZO vs LPSCl 은 압력 · Ag 교란 · 조건마다 셀 1 개 | **Li 금속 박리 공극 · 접촉 상실의 operando 관측 (E 축 · 점착/공극 트랙 관측 대조 · DEM 경계 조건 압력 · 전류)** (exp, 외부) |
```

## (b) comparison_vs_ours.md

① **§E (환원 / 음극(Li 금속) 계면)** 표 맨 위에 한 행 (물성 4축 A–D 에는 넣지 않는다 — 같은 양이 없다):

```
| **🆕 (2026-11-24) Li₆PS₅Cl\|Li 박리 공극은 분극보다 먼저 −Im(Z) (계면 특성 주파수 ≈10² Hz) 에 보인다 — 0.4 MPa · RT · 0.4 mA cm⁻² · in situ Li 2 mAh cm⁻² 에서 −Im +20 % ≈1.0–1.25 vs 분극 ≈1.42–1.49 mAh cm⁻² (판독 · 조건마다 셀 1) · 5 MPa (RT · 60 °C) 에선 조기 상승 없음 · 박리 끝 ≈1.57 → ≈1.9** | **[Kim26Void]** `Fig. 4g` · `Fig. 6c` · `Fig. S9` (`papers/kim2026_operando_void_detection_single_frequency_impedance.md` §3d–3f · §7-1) | **해당 계산 없음** — 우리 §E 는 환원 열역학 (분해산물 · 창) 이고 이 행은 접촉 상실 (Li 크리프 · 빈자리 보충의 기계 · 수송 축). 점착 W 값은 점착 트랙 원장 위치만 (`docs/collab/wad_dem_interface_adhesion_report_2026_11_24.html` §2 · §7) | **—** (같은 양 없음 · 값 비교 금지 · 관측 대조로만) |
```

② **📑 Reference key** 표에 약칭 한 행 (`[Kim26Void]` 는 아직 없음 — grep 확인 · `[Kim26BiSEI]` · `[Kim26HTS]` 와 다름):

```
| **[Kim26Void]** ⭐ **Li₆PS₅Cl (comp1 조성) 무음극 Li 박리 공극의 operando 관측 — −Im(Z) (≈10² Hz) 가 DC 분극보다 먼저 · 0.4 vs 5 MPa 대조** · ⛔ **계산 = COMSOL 주파수 영역 전도 모델뿐 (DFT 0) — A–D 물성 4축 진입 금지 (§E 관측 행만)** · ⚠ **LLZO 셀은 Ag 100 nm · 5 MPa 로 교란 — SE 비교 금지** · 🔧 3-D 모델 결과는 1-D 면적 식으로 재현 (digest §10-① · 카드 산술) | Younggyu Kim · Jonathan Gjerde · Hao Zheng · W. Beck Andrews · Daniel W. Liao · Jeff Sakamoto · Katsuyo Thornton · Neil P. Dasgupta 2026 *ACS Electrochem.* 2, 384–393 | `papers/kim2026_operando_void_detection_single_frequency_impedance.md` ✅ | exp + FEM |
```

(참고 · 메인 판단: `comparison_vs_ours_DEM.md` 에 넣는다면 §I (계면 점착 · 인터레이어 트랙) 의 '관측 대조 — 압력 0.4 / 5 MPa · φ → Z 1-D 식' 한 줄이 맞는 자리.)

## (c) pdf_map.tsv

**필요 없다** — `extract_figures.py --inbox --only kim2026_operando` 가 본문 · SI 둘 다 자동 매칭 (1쪽 본문 66 %). 보험으로 넣는다면:

```
kim2026_operando_void_detection_single_frequency_impedance	kim2026_void_impedance
```

## (d) 추가로 먹일 논문 (8편 · 최근 것 먼저)

출처 = 이 논문 참고문헌 목록 (제목 · 저널 · 권 · 쪽 그대로). `litdb/papers` 본문 · inbox 파일명 grep 으로 **전부 '없음'** 확인 (2026-11-24 ≈12:00 시점 — 병렬 에이전트가 그 뒤 넣었을 수 있다). 전해질 종류는 6 번 (LLZO — 이 논문 p.385 에 적힘) 말고는 이 논문에서 확인 안 됨.

| # | 논문 | 왜 | litdb |
|---|---|---|---|
| 1 | Haslam, C. G. et al., "Evaluating Pressure-Dependent Discharge Behavior of Foil Versus In Situ Plated Lithium Metal Anodes in Solid-State Batteries", *Adv. Energy Mater.* 15, 2403614 (2025) — ref 53 · Jeff Sakamoto · Dasgupta · Janek 공저 | **방전 중 공극 × 압력 × Li 형태** (포일 vs in situ) 를 직접 잰다 · 이 논문이 '공극 깊이가 시간에 따라 바뀐다 (DRT)' 근거로 모델 한계에 인용 → DEM 공극 깊이 · 압력 경계 조건 | 없음 |
| 2 | Haslam, C. G. et al., "The Effect of Alloying Interlayers on Lithium Anode Morphology and Microstructure in 'Anode-Free' Solid-State Batteries", *ACS Energy Lett.* 10, 2285–2291 (2025) — ref 36 · Jeff Sakamoto 공저 | **무음극 · 합금 인터레이어의 젖음 · 점착** — 이 논문 LLZO 셀 Ag 100 nm 의 근거 ('wetting and adhesion') → W_ad 보고서 §7 Ag 친Li 의 실험 쪽 | 없음 |
| 3 | Lee, K.; Sakamoto, J., "Li Stripping Behavior of Anode-Free Solid-State Batteries Under Intermittent-Current Discharge Conditions", *Adv. Energy Mater.* 14, 2303571 (2024) — ref 38 · Jeff Sakamoto 공저 | **무음극 박리 · 전류 파형 (간헐 · 휴지)** 이 공극에 주는 효과 → DEM 전류 경계 조건 · 휴지 중 크리프 회복 | 없음 |
| 4 | Lewis, J. A. et al., "Accelerated Short Circuiting in Anode-Free Solid-State Batteries Driven by Local Lithium Depletion", *Adv. Energy Mater.* 13, 2204186 (2023) — ref 16 | **무음극 국부 Li 고갈** (이 논문 `Fig. S5b` 현상) → 단락까지의 경로 | 없음 |
| 5 | Eckhardt, J. K. et al., "Guidelines for Impedance Analysis of Parent Metal Anodes in Solid-State Batteries and the Role of Current Constriction at Interface Voids, Heterogeneities, and SEI", *Adv. Mater. Interfaces* 10, 2202354 (2023) — ref 40 · (짝: 같은 저자 *ACS Appl. Mater. Interfaces* 14, 42757 (2022) = ref 43 · '1-D 회로로는 안 된다' 주장의 원전) | **공극의 전류 수축이 스펙트럼 어디에 나타나나** — digest §10-② (고주파 원호 ≈3.4× 성장) 해석과 §10-① (3-D = 1-D 재현) 을 원전과 대조 | 없음 (리뷰 digest 인용만) |
| 6 | Singh, D. K. et al., "Origin of the Lithium Metal Anode Instability in Solid-State Batteries during Discharge", *Matter* 6, 1463–1483 (2023) — ref 28 | **방전 중 Li 금속 불안정의 기원** · 박리 중 GEIS 로 공극 해석 · **산화물 (LLZO)** | 없음 |
| 7 | Yan, H. et al., "How Does the Creep Stress Regulate Void Formation at the Lithium-Solid Electrolyte Interface during Stripping?", *Adv. Energy Mater.* 12, 2102283 (2022) — ref 18 | **압력 → Li 크리프 → 박리 공극 억제** — 이 논문 0.4 / 5 MPa 대조의 기전 쪽 → DEM / 연속체 압력 조건 | 없음 |
| 8 | Kasemchainan, J. et al., "Critical Stripping Current Leads to Dendrite Formation on Plating in Lithium Anode Solid Electrolyte Cells", *Nat. Mater.* 18, 1105–1111 (2019) — ref 17 | **임계 박리 전류** = 공극 생성의 전류 문턱 (이 논문은 0.4 mA cm⁻² 하나뿐) | 없음 (리뷰 digest 인용만) |

이미 들어온 원전 (먹일 필요 없음 · digest 머리에 링크함): ref 19 `wang2019_li_se_interface_dynamics_stack_pressure_current_density` · ref 20 `lee2022_thin_insitu_li_void_rewetting_llzo` · ref 37 `sandoval2025_electro_chemo_mechanics_anode_free_ssb` · `seymour2021_void_suppression_interfacial_adhesion_vacancy_transport` · `masias2019_li_metal_elastic_plastic_creep_properties`. 순위 밖: Alsaç et al. *Chem. Rev.* 125, 2009 (2025) (ref 24 · 관측법 리뷰).

## (e) DEM-DFT 보고서에 쓸 거리

(쪽 = 본문 384–393 · SI S1–S12 · '봄' = 크롭 · 확대 렌더를 직접 읽음 · 판독 = figure-read · 카드 산술 = 인쇄값에 산술만)

| # | 쓸 곳 | 내용 | 근거 · 봤나 | 황화물/산화물 |
|---|---|---|---|---|
| 1 | DEM/연속체 — 압력 | 0.4 MPa 에서 공극 신호 있음 · 5 MPa (RT · 60 °C) 에서 없음 · 박리 끝 ≈1.57 → ≈1.9 mAh cm⁻² · 평탄 분극 0.030 → 0.0175 → 0.0055 V (판독) | `Fig. S9` · `Fig. S10` (S10–S11) · 봄 | **황화물** (LPSCl) |
| 2 | DEM/연속체 — 전류 · Li 두께 | DC 0.4 mA cm⁻² 하나 (전류 스윕 없음 · *"공극은 생기고 단락은 피하는 값"*) · 도금 0.05 mA cm⁻² · 5 MPa → 박리 0.4 MPa · Li 2 mAh cm⁻² ≈9.7 µm (카드 산술) | p.385–386 (텍스트) | 황화물 |
| 3 | 공극 개시의 관측 대조 | −Im +20 % ≈1.0 (10–60 Hz) · ≈1.05 (10² Hz) vs 분극 ≈1.42 mAh cm⁻² · 단일 주파수 셀 1.245 vs 1.49 (판독) · 문턱 30–60 % 에서도 순서 유지 | `Fig. 4g` (p.389) · `Fig. 6c` (p.390) · `Fig. S8` (S9) · 봄 (6c 확대) | 황화물 |
| 4 | DEM 기하 입력 | 1.2 mAh cm⁻² 박리 뒤 Li 층 ≈1.8 µm · 공극 폭 수 µm · 고갈 띠 ≈12 µm (판독) · 모델 기하 = 깊이 2 µm · 간격 5 µm · φ ≤0.89 | `Fig. S5` (S6) 봄 · p.387 · SI p.S8 (텍스트) · `Fig. 3a–c` 봄 | 황화물 |
| 5 | φ → 관측량 환산 (DEM 결과를 실험과 같은 잣대로) | Z(f, φ) = R_s + Z_SE + Z_int + Z_int/(1−φ) · Table S1 · A = 0.283 cm² — 이 논문 3-D 결과 (`Fig. 3d,e` · `Fig. 7b,c`) 를 판독 정밀도 안에서 재현 · −Im +20 % ⇔ φ ≈0.32 · Re ⇔ 0.87 (카드 산술) | `Table S1` (S7 텍스트) · `Fig. 7` (p.391) · `Fig. 3` (p.388) 봄 (확대) | 황화물 파라미터 |
| 6 | 접점 전류 집중 | 공극 옆 Li 기둥 ≈2× · 모서리 최대 ≈3× (판독 · 색막대 단위 'A/m³' 는 A/m² 오기) | `Fig. 2b` (p.388) · 봄 | 황화물 파라미터 |
| 7 | 접촉 상실의 길이 척도 | 실험 고주파 원호 ≈3.4× 성장 (`Fig. 1b`) 은 5 µm 격자 모델로 안 나온다 → 실제 접촉 상실 무늬가 훨씬 성기거나 거의 완전 (우리 추정 · 수축 면저항 ∝ ρ_SE × 접점 간격) → DEM 이 접점의 **공간 분포 (간격)** 까지 내야 하는 이유 | `Fig. 1b,c,d` (p.387) · 봄 (확대) | 황화물 |
| 8 | 계면 경계 조건 (공극 전) | R_int 4.47 Ω cm² (계면 하나) · α 0.561 · f_int 66.6 Hz · C_eff ≈5.3×10⁻⁴ F cm⁻² (카드 산술 · Brug) | `Table S1` (S7 텍스트) | 황화물 |
| 9 | W_ad 보고서 §7 (Li 친화성 · 점착과 공극) | 이 논문에 **점착 W · 접촉각 값 없음** · 바뀐 변수는 압력 · 온도뿐이라 W 효과는 이 자료로 말할 수 없다 → 쓸 꼴: *"박리 중 공극 개시는 압력 · 전류 · 온도에 크게 달린다 — W 는 그 위에 얹히는 계면 항이고, 둘을 가르려면 계면만 바꾼 대조가 필요"* · 점착 ↔ 빈자리 수송 계산 축은 seymour2021 | digest §12-③ · `Fig. S9` 봄 | 황화물 |
| 10 | W_ad §7 · Ag | Ag 100 nm 는 *"to improve interfacial wetting and adhesion"* (ref 36) 정성 근거로만 · LLZO 결과는 5 MPa · Ag 교란이라 SE 비교 금지 | p.386 (텍스트) · `Fig. 5` · `Fig. 6d–f` 봄 | **산화물** (LLZO+Ag) |

## (f) 그림 크롭 요약

- **19 장** = 본문 그림 7 + Scheme 1 · SI 그림 10 (S1–S10) · SI 표 1 (Table S1). 도구 18 + **손 크롭 1 (`Fig. 3`)** — 오른쪽 단 `Fig. 3` 캡션이 왼쪽 단 `Fig. 2` 캡션과 한 블록으로 합쳐져 번호 공백으로 떴다 → 래스터 xref 238 경계로 잘라 `manual_crop` 사유 기록 · `missing_labels` f3 에 `resolved`.
- **다시 자름 1 (`Fig. 2`)** — 도구 크롭이 쪽 폭 띠라 `Fig. 3` 윗부분이 섞여 있었다 → 왼쪽 단 래스터만 (`recrop` 사유 기록).
- **자동 캡션 6 개 교정** (`Fig. 1` · `Fig. 2` · `Fig. 5` · `Fig. 6` · `Fig. 7` · `Fig. S10` — 본문 글 · 식 (2) 조각 · 'REFERENCES' 가 섞였다) → 인쇄 캡션으로 · 옛 문자열은 `caption_original_auto`.
- 실독: 크롭 13 장 Read (`Fig. 1`–`Fig. 7` · `Scheme 1` · `Fig. S5` · `S7` · `S8` · `S9` · `S10`) + 확대 렌더 9 장 · SI 쪽 렌더로만 5 장 (`Fig. S1`–`S4` · `S6`) · `Table S1` 은 PDF 텍스트. figures.json `viewed` · `viewed_how` 에 같은 구분을 적었다. 놓친 그림 없음 · `--audit` · `--audit-src` 지적 0.
- **scratchpad 대조 (코디네이터 지시)**: 내가 읽은 글자층 (`scratchpad/kim2026/main.txt` · `si.txt`) 은 PDF 에서 새로 뽑은 것과 md5 가 같다 (1c6c5ab7796f · 1229dec85aeb · 제목 · 저자 · 384–393 · S1–S12 확인) — 덮어써지지 않았다. 확대 렌더 12 장도 다시 렌더해 대조: 10 장 바이트 동일 · `f6_ad` · `f6_cf` 는 픽셀 차 최대 1 (렌더 반올림 · 같은 그림 · 수정 시각도 내 렌더 시각 그대로). digest 숫자는 처음부터 PDF 쪽 렌더 (Read) 로 대조했다. 이후 임시 파일은 `scratchpad/kim2026_operando_void_detection_single_frequency_impedance/` 에만.

## (g) Jeff Sakamoto

**있음 — 교신 저자** (UC Santa Barbara Materials + MUSIC DOE EFRC, Michigan · 교신 셋 = Jeff Sakamoto · Katsuyo Thornton · Neil P. Dasgupta). digest 저자 줄에 'Jeff Sakamoto' 로 적었고 webapp `_paper_pis` 가 `['sakamoto']` 를 돌려준다 (확인). INDEX 행 둘째 칸 맨 앞에 `🏷 **Jeff Sakamoto 공저** · ` 를 넣어 두었다 (위 (a)).

## 메인에 알릴 것 — 사용자 설명용 요점

- **실제로 본 그림**: 크롭 13 장 + 확대 9 장 (위 (f)). **안 본 것**: `Fig. S1`–`S4` · `S6` 크롭 PNG (쪽 렌더로만) · `Table S1` 이미지.
- **본문과 어긋난 그림 · 표기** (digest §10-⑦): 7 % 자료 인용 'Figures S1 and S2' → 실제 `Fig. S2`·`S3` · SI 'Figure S3' (두께 근거) → 실제 `Fig. S5` · `Fig. 2b` 색막대 'A/m³' (→ A/m²) · `Fig. 6` 캡션 '300 %' ↔ 축 비 ≈4× · `Fig. 6f` 본문 'LLZO Re 가 +30 % 초과에서 실패' ↔ 그림은 20 % 한 점뿐 · `Fig. 7b` 범례 없음 · `Fig. 7c` 주파수 단위 없음 · 최대 면적비 0.89 ↔ 맞닿음 한계 0.907 · 측정 시간 'ms' (서론) ↔ '≈1 s' (결과) · `Fig. 1b` 세로 선 · `Fig. 1c` 점선 · `Fig. 5g` × 표지의 뜻이 캡션에 없음 · LPSCl Nyquist 에서 가장 크게 자란 원호가 분석 창 밖인데 본문은 '계면 임피던스 증가' 로 뭉뚱그림.
- **가장 날카로운 셋**: ① 3-D COMSOL 결과 전부가 Table S1 + 1-D 활성 면적 식 Z_int/(1−φ) 로 판독 정밀도 안에서 재현된다 (카드 산술 · COMSOL 재실행 아님) → '다차원 모델 필요' · '공극이 축전기 층' 은 이 기하에서 근거가 없고, DEM 의 φ 를 실험 관측량으로 바꾸는 식으로 그대로 쓸 수 있다. ② Re(Z) 둔감 = 직렬 126 Ω + SE 84.3 Ω 희석 (계면 몫 13 %) — 두꺼운 펠릿 셀 구조 탓이 크고 얇은 SE 막 셀에서는 순위가 바뀔 수 있다. ③ [LPSCl] 0.4 → 5 MPa 로 조기 신호가 사라진다 — 같은 계면에서 압력만으로 공극 관측이 갈린다는 점이 W_ad 보고서 §7 의 '점착과 공극' 문장의 한계 (W 효과는 이 자료로 말 못 함) 를 정한다.
