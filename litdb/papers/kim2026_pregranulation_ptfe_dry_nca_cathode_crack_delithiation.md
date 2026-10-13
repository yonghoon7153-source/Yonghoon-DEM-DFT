<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     형식 이웃 = kim2023_mechanofusion_ncm811_lpscl_core_shell_intimate_contact.md · hippauf2019_dry_film_ptfe_sulfide_cathode_sheet.md · frankenberg2025_milling_dry_processed_sulfide_cathode_microstructure.md.
     쪽 표기 = 본문 "p.N" (PDF N 쪽 = 학술지 인쇄 쪽 N, 전 15 쪽) · SI "SI p.N" (받은 SI PDF N 쪽, 전 51 쪽 — p.1 제목 · 저자 / p.2–7 실험 · 계산 방법 /
     p.8–11 표 S1–S4 / p.12 Note S1 / p.13–49 그림 S1–S37 (한 쪽에 하나) / p.50–51 참고문헌).
     ⚠ 받은 SI 는 Word 에서 내보낸 PDF (문서 메타 작성자 "김태형" · 생성 2026-10-13) — 학술지 게시 SI 와 같은 판인지 [미확인].
     값 표지: [인쇄] = 본문 · 표 · 그림 안 숫자 · [판독] = 그림에서 읽은 값 (litdb/figures/<slug>/digitized.csv — 정밀도 · 보정 검산은 파일 머리, TREND 전용) ·
     [우리 산술] = 인쇄값으로 우리가 다시 한 계산 · [추정] = 우리 해석 · [미확인] = 본문 15 쪽 + SI 51 쪽 전수에 없음.
     크롭 51 장 (Scheme 1–2 · 그림 1–6 · SI 그림 M1 · S1–S37 · SI 표 S1–S4 · SI Note S1 식) 전부 렌더로 열람. -->

# PTFE 건식 후막 NCA 양극에서 **탄소를 넣기 전에 NCA + PTFE 만 먼저 과립화 (PGP — Thinky 2000 rpm × 2 min × 5 회, ≈2 mm 과립)** 하면 같은 혼합 · 반죽 · 캘린더링 뒤 PTFE 섬유가 가늘고 고르며 (< 20 vs 50–100 nm) 큰 NCA 2차 입자의 공정 균열이 줄었다 (SEM 정성) — 기공 쪽 수송 tortuosity 2.91 → 2.37 · R_ct 147 → 33.6 Ω cm² · 반쪽 셀 0.5C 100 사이클 86 % (CDE 는 ≈60 사이클부터 급락) · 전셀 0.5C 300 사이클 86.1 vs 80.9 % — "과립이 응력을 흡수" 는 측정되지 않았고 DFT (NCM622 대리) · CHGNet MD 의 "Li 균일 탈리 = 격자 연성 유지" 고리는 약하다 — Taehyeong Kim · Wonjin Oh … Dongsoo Lee · Junghyun Choi · Seho Sun (영남대 · 가천대 · 경북대 · 한양대, Chem. Eng. J. 2026)

> **[팔로우 랩: 가천대 최준현 교수 (건식 전극)]**
> slug `kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation` · DOI `10.1016/j.cej.2026.179740` · type `exp (PTFE 건식 후막 NCA 양극 · 조기 과립화 PGP · OM/SEM · BET · MCT · UTM 인장 · 180° 박리 · SAICAS · MIP · 대칭셀 EIS τ · 반쪽/전셀 · DRT · 나노압입 · 사후 SEM) + DFT (VASP PBE · NCM622 대리 · 탄성 텐서) + MD (CHGNet · 300 K); DEM · MPM · FEM 없음` · PDF `29688ace-3._Disrupting_the_crack-delithiation_feedback_loop_in_dry-processed_high-nickel_cathodes_through_early-stage_granule_engineering.pdf` · SI `48cae2e4-3._Sup_Disrupting_the_crack-delithiation_feedback_loop_in_dry-processed_high-nickel_cathodes_through_early-stage_granule_engineering.pdf` · digested `2026-10-13` · status ✅
>
> elements: Li, Ni, Co, Al, Mn, O, C, F, P
> methods: DFT, elastic, MD, MLIP, EIS, DRT, MIP, BET, nanoindentation
>
> **원제**: *Disrupting the crack-delithiation feedback loop in dry-processed high-nickel cathodes through early-stage granule engineering* (p.1)
> **저자 (p.1 · SI p.1, 인쇄 순서 그대로)**: Taehyeong Kim^a,1 · Wonjin Oh^a,1 · Seokjun Kim^a · Chanho Lee^b · Jinhyung Kim^b · Minseok Kim^b · Jungmin Lee^b · Yunhee Jang^a · Minkyu Kim^a · Patrick Joohyun Kim^c · Taeseup Song^d · Ungyu Paik^d · **Dongsoo Lee^b,\*** · **Junghyun Choi^b,\*** · **Seho Sun^a,\*** (\* 교신 · ¹ 동등 기여)
> **소속 (p.1 인쇄 그대로)**: a School of Chemical Engineering, Yeungnam University, 280 Daehak-ro, Gyeongsan, Gyeongbuk, 38541, Republic of Korea · b School of Chemical, Biological and Battery Engineering, Gachon University, 1342 Seongnam-daero, Sujeong-gu, Seongnam, 13120, Republic of Korea · c Department of Applied Chemistry, Kyungpook National University, Daegu, 41566, Republic of Korea · d Department of Energy Engineering, Hanyang University, Seoul, 04763, Republic of Korea
> **교신 전자우편 (p.1)**: dslee9117@gachon.ac.kr (D. Lee) · junghchoi@gachon.ac.kr (J. Choi) · seho.sun@yu.ac.kr (S. Sun)
> **팔로우 랩 표지 근거**: 인쇄 로마자 **"Junghyun Choi"** — 소속 b (가천대 화공 · 생명 · 배터리공학부) · **교신저자** (p.1 · SI p.1).  ⚠ 한글 이름은 PDF 어디에도 인쇄되지 않았다 — "Junghyun" 은 흔히 "정현" 의 로마자이므로 1저자가 말한 "최준현" 과 같은 분인지 [미확인] (같은 가천대 · 건식 전극 교신이라는 점은 PDF 로 확인됨).  같은 소속 교신 Dongsoo Lee 와 공동 교신, 1저자 둘은 영남대 (Seho Sun 교신).
> *Chemical Engineering Journal* **545** (2026) 179740 (15 쪽) · 접수 2026-04-30 · 수정 2026-07-12 · 승인 2026-07-20 · 온라인 2026-07-21 · 특집 *"Emerging Functional Materials"* (p.1) · 연구비 NRF RS-2024-00408156 · RS-2024-00449682 · 이해상충 없음 · 데이터 = *"The data that has been used is confidential."* (p.14) · 키워드 · 하이라이트 [미확인 — 인쇄 안 됨]
> **같은 축 카드 (링크만)**: [`hippauf2019_dry_film_ptfe_sulfide_cathode_sheet`](hippauf2019_dry_film_ptfe_sulfide_cathode_sheet.md) (PTFE 건식 막) · [`lee2025_dual_fibrous_ptfe_dry_electrode`](lee2025_dual_fibrous_ptfe_dry_electrode.md) (PTFE 섬유 · 로프 이중 계층) · [`matthews2024_ptfe_nanofibril_network`](matthews2024_ptfe_nanofibril_network.md) · [`lee2026_unveiling_ptfe_dry_electrode_digital_twin`](lee2026_unveiling_ptfe_dry_electrode_digital_twin.md) · [`koo2025_cnt_wrapped_sc_nca_dry_cathode`](koo2025_cnt_wrapped_sc_nca_dry_cathode.md) (건식 NCA) · [`kang2025_toughened_bimodal_nca_lzo`](kang2025_toughened_bimodal_nca_lzo.md) (쌍봉 NCA 균열) · [`landesfeind2016_tortuosity_eis_electrodes_separators`](landesfeind2016_tortuosity_eis_electrodes_separators.md) (이 논문 식 (1) 의 원형) · [`stallard2022_cathode_mechanical_properties_review`](stallard2022_cathode_mechanical_properties_review.md) (이 논문 ref 60).
> **판독 원자료**: `litdb/figures/kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation/digitized.csv` (69 행 — Fig 2h · 2j–k · 4c · 4d · 4g · 4i · 4j · 6b · 6c · SI S24–S26 · S36a) · 크롭 51 장 `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: NCA : Ketjen black : PTFE = 96 : 1.8 : 2.2 (wt) 의 PTFE 건식 후막 (10 mAh cm⁻² 목표 · 46–48 mg cm⁻² · 3.3–3.4 g cm⁻³ · 144 µm) 을 만들 때, 기존 공정 (CDP: 혼합 → 반죽 → 캘린더링) **앞에** NCA + PTFE 만 Thinky 유성 진공 혼합기로 2000 rpm × 2 min 을 5 번 돌리는 "조기 과립화 (PGP)" 를 넣으면 (SI p.2), 같은 뒤 공정을 거친 전극 (GIDE) 이 기존 전극 (CDE) 보다 PTFE 섬유가 가늘고 고르며, 큰 NCA 2차 입자의 공정 균열이 적고, 기공 쪽 이온 수송 · 전하전달 저항 · 율속 · 수명이 모두 낫다 — 저자는 이를 "섬유로 묶인 과립이 반죽 · 캘린더링 응력을 흡수 → 입자 균열 ↓ → Li 탈리 균일 → 격자 연성 유지 (DFT · MD) → 균열-탈리 되먹임 고리 차단" 으로 설명하지만, **응력 흡수는 한 번도 측정되지 않았고** (힘 · 응력 측정 0), GIDE 의 공극률이 더 높아 (0.333 vs 0.305) **덜 눌린 전극일 가능성**이 열려 있으며, DFT · MD 고리는 NCA 가 아닌 **NCM622** 모형 · 0.2 eV/Å 의 느슨한 수렴 · 단일 배치 · 부적절한 요동 공식 위에 서 있다 (§10).

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 공정 변수 (장치 · 속도 · 시간 · 에너지 · 온도) | PGP = **Thinky 유성 진공 혼합기 2000 rpm × 2 min, 5 회** (NCA + PTFE 만, 탄소 전) · 배치 **20 g** · CDE 의 혼합 · 반죽 · 캘린더 · 라미네이트 장치 · 시간 · 온도 · 롤 간격 · 압력 · 횟수 = **전부 [미확인]** · 에너지 n/a | [인쇄] SI p.2 · 본문 p.3 |
| ② 입자 · 크기 · 조성 | NCA **쌍봉: small 1–3 µm + large 8–10 µm** (섞는 비율 · 공급사 [미확인]) — 본문은 쌍봉을 한 번도 쓰지 않는다 · KB 1.8 · PTFE 2.2 wt% 한 조성 · PTFE 2차 입자 수백 µm (S1a [판독]) | [인쇄] SI p.2 |
| ③ 과립 · 전극 기계 | 과립 강도 C₁₀ **1.832 → 3.889 kgf mm⁻²** (×2.12) · 인장 연신 **7.4 → 23.6 %** (최대 응력 0.61 · 0.59 MPa) · toughness **36.6 → 121.2 kJ m⁻³** · 180° 박리 **0.175 → 0.191 N mm⁻¹** (그림; 본문 "0.91" 은 오기로 보임) · SAICAS +7–9 % [판독] · 나노압입 H 24.5/19.3 → 5.6/9.0 MPa (10 사이클) | [인쇄] Fig 1i · 2g · S16 · S17 · 표 S3 |
| ④ 기공 · 이온 수송 | 표면 기공 (SEM 면적) **8.9 → 13.6 %** · ε **0.305 → 0.333** (측정법 [미확인]) · MIP 피크 CDE 넓음 · GIDE ≈0.7 µm · 대칭셀 R_ion **18.03 → 13.44** (표 S2 단위 "Ω·cm²" — 식은 Ω 로 읽어야 재현) · 수송 tortuosity (논문 τ = ε·κ/κ_eff) **2.91 → 2.37** · N_M **9.54 → 7.02** (인쇄; 재계산 **7.11**) · R_ct **147 → 33.6 Ω cm²** · **σ_e 측정 없음** | [인쇄] Fig 2c–d · 2i–l · 4a · 표 S2 · Note S1 · [우리 산술] §3-4 |
| ⑤ 균열 · 사이클 | CDE 캘린더링 직후 큰 입자 균열 (Fig 2e) · 50/100 사이클 뒤 CDE 파편화 (Fig 5k · S34) · **균열 분율 정량 없음** · 반쪽 0.5C 100 사이클 **86 %** vs CDE ≈60 사이클 뒤 급락 (27.8 % @99 [판독]) · 전셀 0.5C 300 사이클 **86.1 vs 80.9 %** · 10 사이클 두께 +12.5 vs +8.3 % | [인쇄] p.6 · 8–10 · [판독] Fig 4d |
| ⑥ 시뮬레이션 | DEM · MPM · FEM **없음**.  DFT (VASP PBE 500 eV · NCM622 2×3×2 · 50 % 탈리 군집 vs 분산 · ±2 % 변형 탄성 텐서 → VRH · Pugh · A^U · Vickers) + CHGNet MD (300 K · NPT 50 ps + NVT 1 ns · 요동 탄성 · 시간평균 von Mises · Li MSD) | [인쇄] p.7–8 · 10–13 · SI p.4–7 |
| ⑦ 믹서 논문 V1 · V2 · V3 | **V2 (혼합 시간) 의 교락 경고 사례** — "기존 혼합의 rpm · 시간을 늘리면 과립 대신 손상만" 은 **데이터 없는 주장** · GIDE 는 기계 에너지가 더 들어갔다 · **첨가 순서** (AM + 바인더 먼저) 가 별도 축 · V3 (SE 함량) n/a | [인쇄] p.3 · [추정] §7-6 |

⛔ **한정어 (떼지 말 것)**: ① **액체 전해질 LIB** (반쪽 1.0 M LiPF₆ FEC/DMC 1:4 · 전셀 1.15 M LiPF₆ EC/EMC/DMC 2/4/4) — 황화물 SE 없음 ② NCA 쌍봉 (비율 미상) · 한 조성 (96 : 1.8 : 2.2) · 한 로딩 (10 mAh cm⁻²) ③ 반쪽 셀은 Li 박 200 µm 에서 매 사이클 ≈10 mAh cm⁻² 를 벗기고 입힌다 — CDE 반쪽 셀 "실패" 에 Li 음극 몫이 섞일 수 있음 (저자 인정, p.9) ④ DFT · MD 모형은 **NCM622** (SI p.4) ⑤ 셀 반복 수 · 오차 막대 · 대표 셀 선정 기준 [미확인] (그림마다 셀이 다른 흔적 — §10-9) ⑥ 원자료 비공개.

---

## 1. 한 줄 요약

PTFE 섬유화 건식 공정은 용매 없는 친환경 · 확장 가능한 양극 제조법이지만, 섬유화에 필요한 높은 기계 압력 (반죽 · 캘린더링) 이 양극 활물질 2차 입자를 깨뜨리고, 깨진 입자는 Li 를 고르지 않게 내보내 균열을 더 키운다는 "균열-탈리 되먹임" 을 저자는 문제로 세운다 (초록 · Scheme 1).  세라믹 성형에서 과립이 압축 응력을 나눠 결함을 줄이는 선례 (refs 42–47) 를 빌려, 탄소를 넣기 전에 NCA 와 PTFE 만 짧은 강한 전단 (Thinky 2000 rpm × 2 min × 5) 으로 섞어 PTFE 섬유가 NCA 를 감싼 ≈2 mm 과립을 먼저 만든다 (PGP, Scheme 2 · Fig 1).  그 뒤 기존과 같은 혼합 · 반죽 · 캘린더링을 거친 GIDE 는 CDE 보다 PTFE 가 막 (sheet) 대신 가는 섬유로 퍼지고 (Fig 2a–b · S12), 표면 기공이 덜 막히며 (Fig 2c–d), 큰 NCA 의 공정 균열이 적고 (Fig 2e–f), 인장 연신 · toughness · 박리 · SAICAS 값이 높고 (Fig 2g–h · S16–S19), 기공 크기 분포가 좁으며 (Fig 2i · S20) 대칭셀 이온 저항 · tortuosity · MacMullin 수가 낮다 (Fig 2j–l · 표 S2).  10 mAh cm⁻² 반쪽 셀에서 R_ct · DRT · 첫 용량 · 수명 · 율속이 모두 GIDE 쪽이 낫고 (Fig 4a–g), 흑연 전셀에서도 차이가 유지된다 (Fig 4h–j).  사후 분석은 사이클 뒤 CDE 의 표면 기공 소실 · 더 큰 두께 팽창 · 경도 · 모듈러스 감소 · 입자 파편화를 보인다 (Fig 5).  마지막으로 DFT (NCM622 대리 모형의 Li 공공 군집 vs 분산) 와 CHGNet MD 가 "군집 탈리 = 취성 · 고경도 · 높은 von Mises" 를 보인다고 해석해 되먹임 고리를 원자 수준에서 뒷받침하려 한다 (Fig 3 · 6).

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 (AM / 도전재 / 바인더 / 전해질) | 연구유형 |
|---|---|---|---|---|
| T. Kim¹ · W. Oh¹ · S. Kim · C. Lee · J. Kim · M. Kim · J. Lee · Y. Jang · M. Kim · P. J. Kim · T. Song · U. Paik · D. Lee\* · J. Choi\* · S. Sun\* (영남대 · 가천대 · 경북대 · 한양대) | *Chem. Eng. J.* 545 (2026) 179740 | 10.1016/j.cej.2026.179740 | NCA (LiNi₀.₈Co₀.₁₅Al₀.₀₅O₂, 쌍봉 1–3 + 8–10 µm) / Ketjen black / PTFE (Solvay) / 액체 LiPF₆ | 실험 (건식 전극 공정 · 미세구조 · 기계 · 전기화학) + DFT · MLIP-MD (보조 해석) |

- CRediT (p.13): T. Kim = 초고 · 실험 · 데이터 · 착상 / W. Oh = 초고 · 실험 · 착상 / D. Lee · J. Choi · S. Sun = 검토 · 초고 · **지도** · 착상 / C. Lee · J. Kim · T. Song · U. Paik = 방법 / M. Kim = 방법 · 데이터 / J. Lee · Y. Jang · M. Kim = 데이터 / S. Kim · P. J. Kim = 실험.
- 계산 담당 저자 · 계산 기관 [미확인] (CRediT 에 "software" · "computation" 항목 없음).
- 소속 b 의 저자 5 명 (C. Lee · J. Kim · M. Kim · J. Lee · D. Lee) 과 J. Choi = 가천대 [인쇄 p.1].

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 재료 · 조성 · 전극 · 셀 (SI p.2–4)

| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 활물질 | LiNi₀.₈Co₀.₁₅Al₀.₀₅O₂ (NCA) · **small 1–3 µm + large 8–10 µm** · 섞는 비율 · 공급사 · 단결정 여부 [미확인] | [인쇄] SI p.2 |
| 도전재 · 바인더 | Ketjen black (Nouryon) · PTFE (Solvay, 등급 [미확인]) | [인쇄] SI p.2 |
| 집전체 | 탄소 코팅 Al 박 (Al 15 µm + C 1 µm) | [인쇄] SI p.2 |
| 조성 · 배치 | **96 : 1.8 : 2.2** (AM : 도전재 : 바인더, wt) · 20 g 배치 | [인쇄] SI p.2 |
| 로딩 · 밀도 · 두께 | 10 mAh cm⁻² 목표 · **46–48 mg cm⁻²** (본문은 "48 mg cm⁻²", p.8) · 복합 밀도 **3.3–3.4 g cm⁻³** · 두께 **144 µm** (표 S2 · SI Fig S33) | [인쇄] SI p.2 · p.9 · p.45 · 본문 p.8 |
| [우리 산술] 정합 | 48 mg cm⁻² ÷ 144 µm = **3.33 g cm⁻³** (범위 안) · 46 mg cm⁻² 이면 3.19 (범위 밖) · AM = 0.96 × 48 = 46.1 mg cm⁻² (로딩 = 전극 전체라고 가정) → 0.5C 첫 방전 195 mAh g⁻¹ 면 9.0 mAh cm⁻² · "10 mAh cm⁻²" 은 ≈217 mAh g⁻¹ 를 가정한 명목값 | [우리 산술] |
| CDE 공정 | 혼합 → 반죽 → 캘린더링 (Scheme 1: + 라미네이트) — **조건 전부 [미확인]** (장치 · rpm · 시간 · 반죽 온도 · 롤 간격 · 선압 · 통과 횟수) · SI 는 *"Details … are listed in Scheme 1 and Scheme 2"* 라 하지만 두 개념도에 수치가 없다 | [인쇄] SI p.2 · p.2–3 |
| GIDE 공정 | **PGP: Thinky planetary vacuum mixer, 2000 rpm × 2 min, 5 회 반복** → 이후 CDE 와 같은 공정 | [인쇄] SI p.2 |
| 셀 | 지름 14 mm 펀칭 · 110 °C 진공 6 h · CR2032 · Ar 글러브박스 · PP 분리막 · 사이클러 CT4008Q | [인쇄] SI p.3 |
| 반쪽 셀 | Li 박 **200 µm** · **1.0 M LiPF₆ FEC/DMC 1:4** · CC 충전 / CC 방전 **3.0–4.3 V** | [인쇄] SI p.3 |
| 전셀 | 건식 흑연 음극 **11 mAh cm⁻² (N/P 1.1)** · **1.15 M LiPF₆ EC/EMC/DMC (2/4/4 vol%)** · CC-CV 충전 / CC 방전 **2.7–4.2 V** | [인쇄] SI p.3 · 본문 p.9 |
| 대칭셀 (R_ion) | NCA‖NCA 코인 대칭셀 (S21) · **전해질 · 차단 조건 · 충전 상태 [미확인]** · 표 S2 의 κ = 9.9 mS cm⁻¹ | [인쇄] SI p.3 · p.9 |
| EIS | **0.0001–100 kHz** (= 0.1 Hz–100 kHz) · ZIVE SP1 (WonATech) | [인쇄] SI p.4 |
| 분석 장비 | OM NX-10 · SEM Hitachi S-4800 · MCT-510 · BET 3-FLEX (N₂, −196 °C) · MIP AutoPore V · UTM Instron 3345 · SAICAS (EN-EX, DAIPLA WINTES) · 나노압입 G200 (Keysight) | [인쇄] SI p.2–3 |

### 3-2. ★ PGP 과립 (Fig 1 · SI S1–S10 · p.3–4)

- **두 모델 혼합물** (탄소 없이 NCA + PTFE 만): CDP = *"simply blended without significant shear input"* · PGP = 유성 원심 혼합기의 조절된 전단 [인쇄 p.3].  ⚠ 즉 Fig 1a–h 는 "전단 없음 vs 전단 있음" 비교다 — 순서 (sequence) 효과의 대조가 아니다 (§10-12).
- OM: CDP = 느슨한 응집 · PTFE 가 2차 입자 그대로 (Fig 1a · S1) / PGP = PTFE 가 섬유로 바뀜 · **≈2 mm 과립** (Fig 1b · S2 · S3) [인쇄 p.3].
- SEM: CDP = PTFE 구형 그대로 · NCA "1차 입자" 가 2차 입자 표면에 *"polar–polar interactions"* 로 붙은 채 혼합 뒤에도 남음 (S4) · PTFE 분산 나쁨 · 1차 입자 응집 (S5) / PGP = 나노 섬유가 NCA 1차 입자를 감싼 연결 망 (Fig 1d) · 개념도 Fig 1e (흩어진 비응집) · 1f (섬유 망) [인쇄 p.3].
  - ⚠ 저자가 "NCA primary particles" 라 부르는 입자는 그림상 **1–3 µm 의 각진 낱알** (S4b · S5 [판독]) — SI 의 small NCA 분획 (1–3 µm) 과 크기가 같다.  다결정 NCA 2차 입자 안의 수백 nm 1차 입자 (S4a 표면에 보이는 것) 와 다른 대상일 수 있다 [추정] · 본문은 쌍봉 분말이라는 사실을 쓰지 않는다.
- BET (Fig 1h): **0.4918 → 0.5549 m² g⁻¹** [인쇄 그림] = ×1.128 (+12.8 % [우리 산술]) — 섬유 망이 NCA 1차 입자 사이에 나노 통로를 만들었다는 해석 [인쇄 p.3].  N₂ 등온선 (Fig 1g) 의 0.45–0.95 P/P₀ 이력 고리는 **두 시료 모두** 있다 [판독] — 본문은 PGP 의 나노 기공 근거로만 씀.
- 탄소 혼합 뒤: PGP 의 섬유 형태 유지 (S6) · 탄소가 섬유 망에 들어가 **PCBD** (Primary particle – Conductive agent – Binder Domain) 단위 (S7) · PGP 분말의 비표면적이 계속 높다 (S8 · S9 — **면적 숫자는 없다**, 등온선 · 기공 분포만) [인쇄 p.4].  [판독] S8 흡착량 PGP 가 CDP 의 ≈2 배 안팎 (P/P₀ 0.6 에서 ≈9–10 vs ≈4 cm³ g⁻¹) · S9 PGP 는 3 · 5 nm 부근 피크, CDP 는 10–30 nm 기공 부피가 더 크다 (본문 미언급) · 기공 분포 계산법 (BJH/DFT) [미확인].
- **과립 강도** (MCT, S10 개략도 · Fig 1i): **C₁₀ 1.832 → 3.889 kgf mm⁻²** = ×2.12 (본문 "112 % higher", p.4) [인쇄]; [우리 산술] 17.97 → 38.14 MPa (×9.807).  C₁₀ 의 정의 (10 % 압축 강도로 보이나) · 시료 수 · 과립 크기 [미확인] · ⚠ 본문은 Fig 1i 를 *"post-mixing powders"* (탄소 혼합 뒤) 로 소개하고 축 이름은 "CDP granule · PGP granule" — Fig 1a–h (탄소 없음) 와 시료 상태가 다르다.
- 저자 해석 [인쇄 p.4]: 과립은 뒤 반죽에서 국소적으로 "파괴 · 변형" 할 만큼만 응집해 있어, 그 점진 파괴가 압축 응력을 재분배해 NCA 2차 입자의 응력 집중을 줄인다 — **측정 근거 없음 (가설)**.

### 3-3. ★ 전극 미세구조 · 기계 (Fig 2a–h · SI S11–S19 · p.4–6)

- 단면 SEM: CDE = PTFE 가 NCA 표면에 **막 (sheet)** 으로 붙거나 탄소와 뭉침 → 바인더 풍부 / 결핍 구역 (Fig 2a · S11a) / GIDE = 고르게 퍼진 섬유 · NCA 표면 뭉침 적음 (Fig 2b · S11b) [인쇄 p.4–6].  🔴 본문의 *"red region in Fig. 2a"* 는 인쇄 그림에 없다 ([판독] 빨간 화소 0).
- **섬유 굵기**: CDE **50–100 nm** · GIDE **< 20 nm** (S12) [인쇄 p.6] — 측정 개수 · 분포 [미확인].  저자: GIDE 의 차이는 섬유화 "양" 이 아니라 더 가늘고 고른 "질" (+ 과립 강도 112 %) [인쇄 p.6].
- **표면 기공** (윗면 SEM 의 빨간 칠 면적 비): CDE **8.9 %** (그림 8.896 %) · GIDE **13.6 %** (13.615 %) (Fig 2c–d · S13–S15) [인쇄] = ×1.53 [우리 산술] — 저자: 롤에 닿는 표면이 가장 큰 응력을 받아 기공이 막히는데 PGP 가 그 응력을 푼다 [인쇄 p.6].  문턱 · 소프트웨어 · 영상 수 [미확인].
- **공정 균열** (이온 밀링 단면, Fig 2e–f): CDE 2차 입자 안 균열 (빨간 점선 원) — *"already present after fabrication"* · GIDE 는 *"identical calendering pressures"* 에도 온전 [인쇄 p.6].  캘린더링 압력 값 [미확인] · 균열 입자 분율 [미확인].  [판독] 균열은 큰 (≈10 µm) 입자에서 보이고 작은 각진 입자에는 균열 흔적이 안 보인다 (정성).
- 저자의 구분 [인쇄 p.6]: 과립은 강체로 남는 것이 아니라 섬유 다리가 점진 변형 · 조절된 파괴로 응력을 흡수 · 재분배한다 — *"not from the fibril network confining individual secondary particles like a physical corset"* (p.7).
- **인장 (UTM, Fig 2g)**: CDE **7.4 % @ 최대 0.61 MPa** · GIDE **23.6 % @ 0.59 MPa** [인쇄 p.6]; toughness **36.6 → 121.2 kJ m⁻³** (S16) = ×3.31 (+231 %, 본문 "230 %") [인쇄 · 우리 산술].
- **180° 박리 (S17)**: 그림 (b) = CDE **0.175** · GIDE **0.191 N mm⁻¹** (10–40 mm 구간 평균) = +9.1 % [인쇄 그림 · 우리 산술].  🔴 본문 p.6 = *"GIDE exhibited a higher cohesion force of **0.91 N mm−1** … whereas the CDE showed … 0.175 N mm−1 (Fig. S17)"* — 그림의 0.191 을 0.91 로 잘못 옮긴 것으로 보인다 (본문대로면 ×5.2).  S17a 가로축 이름 "Strain (mm)" 도 변위의 오기.
- **SAICAS (S18 개략 · S19 프로파일 · Fig 2h 평균)**: 30 µm · 100 µm 깊이 수평력 F_h — GIDE 는 깊이마다 고른 F_h · CDE 는 일부 구간 F_h 낮음 [인쇄 p.6]; [판독] 평균 30 µm **0.343 → 0.366 N** (+6.8 %) · 100 µm **0.904 → 0.985 N** (+9.0 %) — Fig 2h 축이 0.30 · 0.80 에서 잘려 있어 차이가 크게 보인다 · S19 에 범례 없음 · 날 폭 · 속도 · N 을 폭으로 정규화했는지 [미확인].

### 3-4. ★ 기공 · 이온 수송 (Fig 2i–l · SI S20–S21 · 표 S2 · Note S1 · p.6–7)

- **MIP (Fig 2i)**: CDE = *"broad bimodal pore size distribution spanning 500–1500 nm"* · GIDE = *"sharp unimodal distribution centered at 700 nm"* [인쇄 p.6].  [판독] 그림의 표지 점선은 CDE **≈0.5 µm · ≈6 µm**, GIDE **≈0.65 µm** — CDE 의 두 번째 봉우리가 1.5 µm 가 아니라 ≈6 µm 에 있다 🔴.
- **누적 침투 (S20)**: GIDE 는 0.6–1 µm 에서 급증 · CDE 는 넓게 서서히 [인쇄 p.6]; [판독] 정규화 누적 **≈70 % (≈0.6 µm 아래) 는 두 곡선이 겹친다** — 차이는 큰 기공 쪽 ≈30 % 에만 있다 · 중앙 기공 ≈0.4 µm 는 둘이 같다.
- **대칭셀 Nyquist (Fig 2j–k · S21)**: "1/3 R_ion" 표지 → R_ion **CDE 18.06 Ω cm²** · **GIDE 13 Ω cm²** · 감소 **25.58 %** (본문 p.6) / 표 S2 = **18.03 · 13.44 "Ω·cm²"** [인쇄].  [우리 산술] 25.58 % = (18.06 − 13.44)/18.06 → 본문은 CDE 18.06 · GIDE 13.44 를 썼다 (표 S2 의 18.03 이면 25.46 %).
- **표 S2 (SI p.9)**: A **1.5386 cm²** (= 3.14 × 0.7² [우리 산술]) · L **144 µm** · ε **0.305 · 0.333** (칸 이름 "ε (%)" 인데 값은 분율) · κ **9.9 mS cm⁻¹**.
- **Note S1 (SI p.12)**: 식 (1) **τ = R_ion·A·k·ε / (2d)** · 식 (2) **N_m = τ / ε** — `landesfeind2016_tortuosity_eis_electrodes_separators` 카드의 Eq. 8 (N_M = τ/ε = R_Ion·A·κ/d, 단일 전극) 을 두 전극 대칭셀로 쓴 꼴 (d → 2d) [추정] · N_M 이 무차원이려면 R_Ion·A·κ/d 의 R_Ion 은 차원상 **Ω** (셀 저항) 이다 [우리 산술 — Ω × cm² × S cm⁻¹ / cm = 무차원].  식의 인용 출처는 SI 에 없다.
- **Fig 2l · 본문 p.6–7**: τ **2.906 → 2.369** (본문 2.91 · 2.37, "18.6 % reduction in lithium-ion transport path length") · N_M **9.537 → 7.018** (본문 9.54 · 7.02) [인쇄].
- **[우리 산술] 재현표**:

| | CDE | GIDE | 비고 |
|---|---|---|---|
| R_ion (표 S2 숫자) | 18.03 | 13.44 | 본문 18.06 · 13 |
| τ = R·A·κ·ε/(2d), R 을 **Ω (셀 저항)** 으로 | **2.909** | **2.367** (ε = 1/3 이면 2.369) | 인쇄 2.906 · 2.369 ✓ |
| 같은 식, R 을 **Ω·cm²** 로 읽고 A 를 빼면 | 1.890 | 1.538 | 인쇄와 안 맞음 |
| N_M = R·A·κ/(2d) = τ/ε (ε 무관) | **9.536** | **7.108** | 인쇄 9.537 ✓ · **7.018 ✗** |
| f = 1/N_M | 0.105 | 0.141 | 우리 규약 f = σ_eff/σ₀ |
| κ_eff = κ/N_M (mS cm⁻¹) | 1.04 | 1.39 | 기공 전해질 유효 전도도 |
| √(τ_GIDE/τ_CDE) | — | 0.903 | 경로 길이로 읽으면 −9.7 % |

  ⇒ 인쇄 τ 는 R_ion 을 **Ω** 으로 넣을 때만 나온다 — 표 S2 · 본문의 "Ω·cm²" 와 식 (1) 이 맞지 않는다 🔴.  면저항이라면 18.03 Ω × 1.5386 cm² = **27.7 Ω cm²** · 13.44 → **20.7 Ω cm²** [우리 산술].
  ⇒ GIDE 의 N_M **7.018 은 7.108 의 자리 바뀜**으로 보인다 (N_M = R·A·κ/2d 는 ε 를 안 쓰므로 ε 로는 설명 안 됨) 🔴.
  ⇒ Fig 2j–k 표지 간격 × 3 [판독] = **≈20.5 Ω (CDE) · ≈14.1 Ω (GIDE)** — x 축이 Ω 이므로 표 S2 의 숫자가 Ω 라는 해석과 같은 방향 · 표 S2 와는 −12 % · −5 % 차이.
  ⇒ "18.6 % 경로 길이 감소" 🔴 — 논문 τ 는 tortuosity factor (우리 명명 규약의 **수송 tortuosity = tau2**, 제곱근 아님) 이므로 길이 비로 읽으면 √ 비 **−9.7 %** [우리 산술].
  ⇒ **공극률 교락** 🔴: ε 0.305 → 0.333 만으로 Bruggeman (N_M = ε^−1.5) 이 주는 N_M 비 = (0.305/0.333)^−1.5 = **1.141** — 관측 N_M 비 9.536/7.108 = **1.342** 의 로그 몫 **≈45 %** [우리 산술 · Bruggeman 지수 가정, 실제 지수가 더 크면 몫도 커짐].  즉 수송 개선의 절반 가까이는 "더 다공한 (덜 눌린) 전극" 으로도 설명된다 — 저자는 논하지 않는다.
  ⇒ 같은 두께 (144 µm) · 같은 조성에서 ε 가 0.305 vs 0.333 이면 로딩이 (1 − 0.305)/(1 − 0.333) = **1.042 배** 다르다 (예: 48 vs 46 mg cm⁻²) [우리 산술] — 시료별 로딩 · ε 측정법 (MIP 침투 부피인지, 밀도 계산인지) [미확인].

### 3-5. ★ DFT (Fig 3 · SI M1 · S22–S23 · 표 S4 · p.7–8 · SI p.4–6)

- **모형**: SI = **LiNi₀.₆Co₀.₂Mn₀.₂O₂ (NCM622)** R3̅m — *"shares the same R3̅m crystal structure and analogous delithiation-induced mechanical behavior with NCA, while avoiding the computational complexity associated with the low-concentration Al substitution"* (SI p.4) [인쇄].  🔴 본문 · Fig 3 캡션은 *"high‑nickel layered oxide"* · *"R-3 m framework"* 로만 쓰고 NCM622 라는 말이 없다 (Fig 3a 범례에 Mn 이 보일 뿐).
- **설정 [인쇄 SI p.4–5]**: VASP · PAW · PBE · 평면파 500 eV · **ionic 수렴 0.2 eV/Å** (*"relatively relaxed"* — 0.03 eV/Å 은 진동만 하고 에너지 개선이 없었다) · 2×2×2 Monkhorst-Pack (어느 셀 기준인지 [미확인]) · 최적 격자 **a 4.9 · b 6.0 · c 10.6 Å** → **2×3×2 슈퍼셀 a 10.1 · b 19.2 · c 22.1 Å** · 50 % = 60 Li 제거 (pristine 480 원자 → 420) · VASPKIT 1.4.1 응력-변형 (−2…+2 %, 0.5 % 간격) · Spglib 대칭 · VRH 평균 · Pugh · 보편 비등방 지수 A^U · Vickers 경도 · Debye 온도 (**값 미보고**).  DFT+U · 스핀 분극 · 자기 배열 [미확인].
- **배치 셋 (SI M1 · Fig 3a)**: pristine (Li 가득) · **CDE-model** = Li 를 한 영역에서 몰아 뺀 군집 공공 ([판독] M1b 에서 Li 층 안에 렌즈 모양으로 빈 구역) · **GIDE-model** = 흩어진 공공.  *"Multiple candidate configurations were examined … representative structures that converged stably upon structural relaxation were selected"* — 모드마다 구조 **하나** (SI p.5).
- **결과 [인쇄]**:

| | pristine | CDE-model | GIDE-model | 출처 |
|---|---|---|---|---|
| B (GPa) | 128 | 135 | 156 | SI Fig S22a |
| E (GPa) | 141 | 208 | 203 | S22b |
| G (GPa) | 54 | 84 | 79 | S22c |
| B/G (Pugh) | **2.38** | **1.61** | **1.97** | Fig 3b · p.7–8 |
| A^U | 1.67 | 0.51 | 0.37 | Fig 3c · p.8 |
| Vickers Hv (GPa) | 4.40 | 12.10 | 8.56 | Fig 3d · p.8 |
| E max / min (GPa) | 214.9 / 59.9 | 296.8 / 135.7 | 253.1 / 140.7 | 표 S4 |
| G max / min (GPa) | 85.4 / 24.5 | 114.5 / 68.5 | 95.5 / 66.7 | 표 S4 |
| B max / min (GPa) | 256.1 / 76.5 | 252.0 / 66.9 | 314.4 / 77.5 | 표 S4 |
| 비 E · G · B (max/min) | 3.59 · 3.48 · 3.35 | **2.19** · 1.67 · 3.77 | **1.80** · 1.43 · **4.06** | S23 (= 표 S4 비 ✓ [우리 산술]) |
| [우리 산술] ν = (3B−2G)/(2(3B+G)) | 0.315 | 0.242 | 0.283 | S22 값 |

- 저자 해석 [인쇄 p.7–8]: Li 제거는 세 배치 모두 강성 ↑ · **B/G 1.75** 를 *"practical empirical guideline for relative comparison"* 으로 둘 때 CDE-model 만 아래 (취성 쪽) · GIDE 는 가장 등방 (A^U 0.37) · 경도 CDE ×≈3 (취성 + 고경도 = 균열에 불리) · GIDE ×≈2 (강도-인성 균형) → "균열 → 국소 과탈리 → 취성 · 경화 → 더 균열" 의 4 단계 사슬 (p.8) · CDE-model 은 *"bounding case rather than a unique structural assignment"* 라고 스스로 한정.
- [우리 산술] 'threefold' = 12.10/4.40 = **2.75** · 'twofold' = 8.56/4.40 = **1.95**.
- [우리 산술] **경도는 B · G 의 함수다**: Chen 계 경험식 Hv = 2(k²G)^0.585 − 3 (k = G/B — 논문에 식 인쇄 없음, SI 가 인용한 ref [8] 계열이라고 우리가 가정) 에 S22 값을 넣으면 **4.52 · 12.33 · 8.63 GPa** = 인쇄 4.40 · 12.10 · 8.56 과 ≤3 % 일치 → Pugh 비와 Vickers 경도는 **같은 두 숫자 (B, G) 의 두 표현**이지 독립 증거가 아니다.
- [우리 산술] 격자: 10.1/4.9 = **×2.06** · 19.2/6.0 = **×3.20** · 22.1/10.6 = **×2.08** — 2×3×2 확장의 정수배가 아니다 · 벌크 셀 부피 상한 a·b·c = 311.6 Å³ (원자 40 개 = 10 화학식 → ≤ 31.2 Å³/화학식) 은 같은 논문 MD 평형 부피 4071–4147 Å³ / 120 화학식 = **33.9–34.6 Å³/화학식** 보다 작다 → 벌크 격자상수 인쇄값이 슈퍼셀 · MD 와 맞지 않는다 🔴.
- ⚠ 본문은 E · G 의 max/min 비만 인용한다 — **B 비는 GIDE (4.06) > CDE (3.77)** · **pristine 이 E · G 비등방 최대 (3.59 · 3.48) · A^U 최대 (1.67)** 인데 '가장 연성' 이다 → "결정립 수준 방향 불균형 → 입계 균열" 논리를 pristine 에 그대로 쓰면 결론이 뒤집힌다 [추정].

### 3-6. 반쪽 셀 전기화학 (Fig 4a–g · SI S24–S26 · p.8–9)

- **EIS (Fig 4a)**: R_ct **CDE 147 · GIDE 33.6 Ω cm²** = −77 % (−77.1 % [우리 산술]) [인쇄 p.8] — 저자: 낮은 tortuosity · 균일 · *"higher electrical conductivity"* (🔴 σ_e 측정 없음) · 열린 활성 자리.  [판독] Nyquist 반원 지름 ≈220 vs ≈55 Ω (축 = Ω) — Ω cm² 환산 기준 [미확인].
- **DRT (Fig 4b)**: ~10⁵ Hz (벌크 전해질 · 접촉) GIDE 작음 · 10²–10⁴ Hz (R_ct) CDE 피크 큼 · 1–10² Hz CDE 넓음 (확산 · 굽은 기공) · < 1 Hz CDE 고체 확산 저항 큼 · *"GIDE exhibited suppressed peaks across all frequency ranges"* [인쇄 p.8].  [판독] R_ct 피크 γ ≈77 (≈1.3 kHz, CDE) vs ≈21 (≈8 kHz, GIDE) · **< 1 Hz 피크 높이는 둘 다 ≈57** (GIDE 는 ≈0.2 Hz 로 이동) 🔴 · DRT 곡선이 측정 창 (0.1 Hz–100 kHz) 밖까지 그려져 있다.
- **화성 (S24, 0.1C 충방전)**: [판독] 방전 **CDE ≈207 · GIDE ≈209 mAh g⁻¹** — 0.1C 에서는 거의 같다 · 화성 ICE [미확인].
- **첫 사이클 (Fig 4c, 0.2C 충전 / 0.5C 방전)**: ICE **96.3 → 97.0 %** · **185 → 195 mAh g⁻¹** (저자: *"variations in available active sites"*) · 과전압 GIDE 작음 [인쇄 p.8]; [판독] 방전 끝 186.3 · 195.4.  [추정] S24 의 0.1C 동등 + 0.5C 차이는 '활성 자리' 보다 **율속 (수송) 차이**를 가리킨다.
- **수명 (Fig 4d, 0.5C 방전 / 0.2C 충전)**: GIDE 100 사이클 **86 %** · CDE *"rapid capacity fading and eventual cell failure after approximately 60 cycles"* [인쇄 p.8]; [판독] GIDE **8.81 → 7.54 mAh cm⁻²** (85.6 %) · CDE **8.19 → 6.36 (60) → 3.11 (80) → 2.28 (99)** (27.8 %) — "실패" = 60 사이클부터 가속 감퇴.
- **dQ/dV (Fig 4e–f · S25–S26)**: H1→M · H2→H3 산화환원 피크 셋 · CDE 는 고전위 · 넓은 폭 (기계 응력 · 미세 균열에 따른 과전압) → 100 사이클에 피크 소실 · GIDE 좁게 유지 [인쇄 p.8–9].  [판독] S25 · S26 방전 끝 1st/10th/50th/100th = **170/166/145/47** (CDE) · **183/179/170/157** (GIDE) mAh g⁻¹ → 100th/1st = 27.5 · 86.1 % (Fig 4d 와 정합) · 그런데 Fig 4c '첫 사이클' 186 · 195 와 **7–8 % 다르다** 🔴 (다른 셀인지 [미확인]).
- **율속 (Fig 4g, 방전 0.2 → 0.5 → 1C → 복귀)**: GIDE **9.7 mAh cm⁻² (설계의 97 %) @0.2C · 1C 86 %** · CDE **92 % · 63 %** (본문 "6 3%" 조판) [인쇄 p.9]; [판독] GIDE 9.76 / 9.41 / 8.57 · CDE 9.18 / 8.74 / 6.31 mAh cm⁻² (0.2 / 0.5 / 1C) — "%" 는 설계 용량 10 mAh cm⁻² 대비 · 충전 율 [미확인] · 0.5C 값 (9.41) 이 Fig 4d 첫 점 (8.81) 보다 7 % 높다 (다른 셀 [추정]).

### 3-7. 전셀 (Fig 4h–j · p.9)

- NCA (10 mAh cm⁻²) ‖ 건식 흑연 (11 mAh cm⁻², N/P 1.1) · 2.7–4.2 V [인쇄 p.9 · SI p.3]; 첫 사이클 GIDE 가 약간 높다 (Fig 4h, [판독 정성]).
- **0.2C (Fig 4i)**: 200 사이클 **GIDE 86.3 % · CDE 84.8 %** [인쇄 p.9] ↔ 🔴 [판독] 그림 끝점 **≈89.5 % · ≈86.5 %** (보정 검산 = 같은 축의 Fig 4j 가 인쇄값과 0.1 %p 안).  기준 사이클이 다를 가능성 [추정].
- **0.5C (Fig 4j)**: 300 사이클 **GIDE 86.1 % · CDE 80.9 %** [인쇄 p.9] = [판독] 86.2 · 80.8 ✓.
- 저자: 흑연 음극의 완충 효과로 CDE 균열의 상대적 심각도가 줄어 전셀에서 CDE 가 더 오래 산다 · 반쪽 셀 CDE 의 짧은 수명에는 *"issues associated with lithium metal anodes"* 도 있을 수 있다 [인쇄 p.9].
- ⚠ 두 그림 모두 x 축이 ≈0–75 사이클을 좁게 압축 (break) 해 초기 하락 (100 → ≈95 %) 이 시각적으로 작게 보인다 [판독].

### 3-8. ★ 사후 분석 (Fig 5 · SI S27–S34 · 표 S3 · p.9–10)

- **DRT · Nyquist 300 사이클 뒤 (전셀, 충전 4.2 V · 방전 2.7 V, Fig 5a–b · S27–S28)**: CDE 의 R_ct · 이온 수송 저항이 더 크다 · < 1 Hz 확산 성분은 GIDE 가 더 뚜렷 (저자: CDE 는 균열이 새 표면 · 짧은 확산 경로를 만들어 겉보기 확산 제약이 작아진다) [인쇄 p.10].  🔴 [판독] S27 · S28 Nyquist 는 두 전극이 **거의 같다** (충전: 첫 반원 ≈10.0 vs ≈9.5 Ω · 둘째 반원 꼭지 ≈5.3 vs ≈5.7 Ω — 둘째 반원은 오히려 GIDE 가 큼) — "CDE 저항이 더 크다" 는 Nyquist 원자료에서 약하다.
- **나노압입 (전셀 · 10 사이클 전/후, Fig 5c–d · 표 S3)** [인쇄]:

| | 경도 H (MPa) | 탄성률 E (MPa) | 탄성 회복 (%) |
|---|---|---|---|
| CDE 사이클 전 | 24.5 | 774.65 | 25.2 |
| GIDE 사이클 전 | 19.3 | 327.13 | 38.4 |
| CDE 10 사이클 뒤 | 5.6 | 125.66 | 36.5 |
| GIDE 10 사이클 뒤 | 9.0 | 163.58 | 44.2 |

  [우리 산술] 감소 CDE H −77.1 % · E −83.8 % / GIDE H −53.4 % · E −50.0 % ✓ (본문 77 · 84 · 53 · 50 %) · 사이클 뒤 GIDE/CDE = H ×1.61 · E ×1.30 ✓ (본문 60 · 30 %) · 저자: 사이클 전 CDE 의 높은 E 는 바인더 뭉침 · 불균일 배열이 만든 국소 강성 부위 [인쇄 p.10].
  🔴 Fig 5c–d 가로축 **"Penetration Depth (nm)" 0–5** · 하중 ≈2.8 mN — H = P/A 로 A ≈ 2.8 mN / 24.5 MPa ≈ 114 µm², Berkovich 면적식 A ≈ 24.5 h² (우리가 가정) 이면 h ≈ **2.2 µm** [우리 산술] → 축 단위는 **µm** 여야 맞다.  깊이 2–4.5 µm 는 작은 NCA (1–3 µm) 크기급 = 다공 복합 전극의 겉보기 값 (입자 물성 아님).
  🔴 본문 *"consistent with … stress–strain curves (Fig. 2h)"* → 응력-변형은 Fig 2g (2h 는 SAICAS).
- **표면 기공 (Fig 5e–g · S29–S32)**: 전 **8.9 · 13.6 %** → 10 사이클 **2.935 · 6.355 %** (S29b · S30b 그림 안 숫자 — 캡션에 사이클 수 없음) → 100 사이클 **1.865 · 5.539 %** (Fig 5e–f) [인쇄 그림]; 본문 *"increase of approximately 197 %"* = 5.539/1.865 = ×2.97 [우리 산술] ✓.  셀 종류 (반쪽 · 전셀) [미확인] — 반쪽 CDE 는 ≈60 사이클 뒤 급락했으므로 100 사이클 CDE 시료가 어느 셀인지가 해석을 바꾼다.
- **두께 (Fig 5h–j · S33)**: 144 µm → 10 사이클 **CDE 162 µm (+12.5 %) · GIDE 156 µm (+8.33 %)** [인쇄]; 저자도 *"origin of this significant volumetric expansion … remains uncertain"* — 고니켈 후막 때문인지 건식 공정 때문인지 미해결 [인쇄 p.10] · CDE 는 더 부풀었는데도 표면 기공이 적다 → 균열 파편이 표면 기공을 막는다는 해석 [인쇄 p.10].
- **입자 단면 (Fig 5k–l = 50 사이클 · S34 = 100 사이클)**: CDE 2차 입자 균열이 넓게 퍼지고 일부는 알아볼 수 없을 만큼 파편화 · GIDE 거의 온전 [인쇄 p.10] — 🔴 50 vs 100 사이클 표기 불일치 · 균열 분율 정량 없음 · S34a 의 노랑/빨강 상자 구분 기준 [미확인].

### 3-9. ★ MD (Fig 6 · SI S35–S37 · p.10 · 12–13 · SI p.6–7)

- **설정 [인쇄 SI p.6–7]**: CHGNet (*"trained on the Materials Project relaxation trajectory dataset"*, 버전 [미확인]) · ASE · DFT 최적화 구조 셋 그대로 (pristine Li₁.₀ **480 원자** · CDE/GIDE Li₀.₅ **420 원자**) · **NPT 300 K · 0 GPa · 50 ps (Berendsen 압력조 τP = 1000 fs)** → **NVT 1 ns (Berendsen 열욕 τT = 200 fs)** · Δt 1 fs · 500 step (0.5 ps) 마다 위치 · 응력 기록 · 뒤 80 % 로 통계 · 블록 평균 표준오차 · z 검정 · 탄성 = **응력 요동식 Cαβ = (V/k_BT)⟨δσα δσβ⟩** → VRH · von Mises = 순간 응력 텐서 식 · Li 궤적 (unwrap · 최소 영상) · Li 밀도 지도 (2D 격자 · 가우스 σ = 1.5 격자).
- **결과 [인쇄 p.13]**: B/G **pristine 3.62 > GIDE 3.05 > CDE 2.56** (DFT 순서 유지; 절대값은 MD 가 모두 1.75 위 — 저자: 열 연화 · MLIP 의 부드러운 퍼텐셜 탓이라 문턱은 옮길 수 없고 순서만 의미) · **GIDE 가 CDE 보다 0.242 eV 안정 (p < 0.001)** · **시간평균 von Mises CDE 0.88 · GIDE 0.63 GPa (−28 %)** · **D_Li 1.73 × 10⁻⁷ vs 1.65 × 10⁻⁷ cm² s⁻¹ (비 0.95)** · Li 평균 변위 pristine **0.29 Å** · 탈리 둘 **≈2.5 Å** · CDE 최대 **8.3 Å** (공공 많은 영역에 몰림) · GIDE 는 셀 전체에 퍼진 변위 · Li 밀도 지도 CDE 불균일 / GIDE 고름 (Fig 6d–e).
- [판독] **Fig 6b MD 모듈러스** B **42.3 / 52.9 / 59.5** · G **11.2 / 20.5 / 19.2** · E **31.7 / 54.9 / 52.2 GPa** (pristine / CDE / GIDE) → DFT 의 **0.21–0.39 배** [우리 산술] — 본문은 *"systematically lower"* 로만 씀.
- [판독] 🔴 **Fig 6c pristine 시간평균 von Mises ≈1.94 GPa** — CDE (0.88) 의 2.2 배인데 본문에 없다.  "균일 = 낮은 내부 응력 = 균열 구동력 ↓" 논리를 그대로 쓰면 **완전히 균일한 pristine 이 가장 위험**하다는 모순.
- [판독] 🔴 **S35b**: 50 ps NPT 끝에서 셀 부피가 **아직 오른다** — pristine ≈4074 → 4147 Å³ (직선 증가) · CDE ≈4024 → 4071 · GIDE ≈4065 → 4078 Å³ — 캡션의 *"converging to"* 와 다르다 · S35c *"energy conservation"* 은 열욕이 걸린 NVT 에서 의미가 약하다.
- [판독] S37a: MSD **≈3 Å² @ 200 ps 지연** → rms ≈1.7 Å [우리 산술] — Li 자리 사이 한 번 이동 거리보다 짧다 (§10-17).
- [우리 산술] 0.242 eV / 420 원자 = **0.58 meV/원자**.
- 🔴 본문 *"GIDE is energetically more stable than CDE by 0.242 eV (p < 0.001) at 300 K (Fig. S36)"* — S36 은 탄성 상수 그림이다 (에너지 시계열은 S35c, 숫자 0.242 는 SI 어디에도 없음).

---

## 4. ★ 방법 — 측정 사슬 · 시뮬레이션 · 입자 처리

### 4-1. 측정 사슬
NCA (쌍봉) + PTFE → [GIDE 만] PGP (Thinky 2000 rpm × 2 min × 5) → OM · SEM · BET · MCT (Fig 1) → + Ketjen black 혼합 → SEM · BET (S6–S9) · MCT (Fig 1i) → 반죽 → 캘린더링 → 탄소 코팅 Al 위 막 (라미네이트, 조건 [미확인]) → (i) 단면 · 윗면 · 이온 밀링 SEM (Fig 2a–f · S11–S15) (ii) UTM 인장 · 180° 박리 · SAICAS (Fig 2g–h · S16–S19) (iii) MIP (Fig 2i · S20) (iv) NCA‖NCA 대칭셀 EIS → R_ion → τ · N_M (Fig 2j–l · 표 S2 · Note S1) → 반쪽 셀 (EIS · DRT · 화성 · 첫 사이클 · 100 사이클 · dQ/dV · 율속) · 흑연 전셀 (0.2C 200 · 0.5C 300 사이클) (Fig 4) → 사후 (DRT · 나노압입 · 표면 기공 · 두께 · 입자 단면) (Fig 5) → DFT (Fig 3) · MD (Fig 6) 해석.

### 4-2. 시뮬레이션 요약 (세부는 §3-5 · §3-9)
- **DFT**: VASP PBE · PAW · 500 eV · 0.2 eV/Å · 2×2×2 k · NCM622 2×3×2 (480/420 원자) · 50 % 탈리 군집 (CDE-model) vs 분산 (GIDE-model) · 각 1 구조 · VASPKIT 응력-변형 탄성 텐서 → VRH B · G · E · ν · Pugh · A^U · Vickers · Debye (미보고).
- **MD**: CHGNet · ASE · Berendsen NPT 50 ps → Berendsen NVT 1 ns · 300 K · 요동 탄성 · von Mises · MSD/D (Einstein) · Li 밀도 지도 · 블록 평균 · z 검정.
- **연속체 · 입자 스케일 모형**: 없음 (DEM · MPM · FEM · P2D 0).

### 4-3. ★ 입자 처리 (우리 축 언어로)
- **실험 쪽**: NCA = 강체처럼 깨지는 쌍봉 구 (큰 2차 입자 8–10 µm 는 다결정 · 작은 분획 1–3 µm 는 각진 낱알 [판독]) — **형상 소성 없음, 파괴만** · PTFE = 수백 µm 2차 입자 (S1a [판독]) → 전단으로 < 20–100 nm 섬유 · NCA 표면 막 (CDE) — **바인더가 형상을 바꾸는 유일한 상** · 과립 (≈2 mm) = AM + 섬유 결합 덩어리 → 뒤 공정에서 "점진 변형 · 조절된 파괴" (가설).
- **계산 쪽**: 입자 · 전극 스케일 없음.  원자 스케일 (≈1–2 nm 셀) 의 Li 공공 배치만 바꿔 "균열 → 국소 과탈리" 를 경계 사례로 근사.
- **우리 DEM 과의 대응** [추정]: 강체 구 · Hertz/hysteresis · Auerbach 파괴 판정 · 응집 (점착) — PTFE 섬유 · 바인더 막 · **결합 (bond) 된 과립** · 첨가 순서는 표현되지 않는다 (§7-2).

### 4-4. 기법 미니 용어집
- **PGP (pre-granulation process)**: 탄소 넣기 전 NCA + PTFE 만 전단 혼합해 섬유로 묶인 과립을 먼저 만드는 단계 (이 논문 이름).  **CDP / CDE**: 기존 건식 공정 / 그 전극.  **GIDE**: granule-induced dry electrode.
- **PCBD**: Primary particle – Conductive agent – Binder Domain — 1차 입자 · 탄소 · PTFE 섬유가 서브 µm 에서 묶인 단위 (이 논문 이름).
- **MCT C₁₀**: 미세 압축 시험기의 과립 압축 강도 (축 이름 그대로, kgf mm⁻²).
- **SAICAS**: 기울어진 날로 일정 깊이를 깎으며 수평력 F_h · 수직력 F_v 를 재는 박리 · 응집력 시험.
- **대칭셀 TLM**: 같은 전극 둘을 맞댄 셀의 Nyquist 45° 구간 실축 투영 = R_ion/3 → R_ion · τ · N_M.
- **N_M (MacMullin 수)**: κ/κ_eff = 1/f.  **논문 τ**: ε·N_M = ε·κ/κ_eff = **tortuosity factor (우리 tau2, 수송 tortuosity)**.
- **DRT**: 임피던스를 이완 시간 분포 γ(ln τ) 로 푼 것 — 피크 면적 ≈ 저항.
- **Pugh 비 B/G**: 금속에서 연성 (> 1.75) · 취성 (< 1.75) 경향을 가르던 경험 지표.  **A^U**: 보편 탄성 비등방 지수 (0 = 등방).
- **응력 요동식**: NVT 에서 탄성 상수 = Born 항 − (V/k_BT)⟨δσδσ⟩ + 운동 항 이 표준형 — 이 논문은 요동 항 하나를 C 로 씀 (§10-15).
- **CHGNet**: Materials Project 이완 궤적으로 학습한 범용 그래프 신경망 원자간 퍼텐셜.

---

## 5. Figure set ★ (크롭 51 장 = `litdb/figures/kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation/`)

| Fig | 내용 | 우리 활용 |
|---|---|---|
| Scheme 1 | 기존 건식 공정: 반죽 (A) + 막 · 캘린더링 (B) · 반죽 중 마찰로 CAM 응력 · PTFE 섬유 제어 어려움 · 표면 기공 막힘 · CAM 응력 누적 (그림 안 *"fraction force"* = friction 오기) | 공정 개념도 |
| Scheme 2 | (a) "약한 전단" 과립 형성 (호퍼 · 스크루 그림 = 실제 장치 (Thinky) 아님) · 과립 사진 · SEM · 세 특징 (과립 안 응력 완충 · 바인더 섬유화 개시 · CAM 과 CBD 망 미리 형성 — PGP 단계엔 탄소가 없는데 "CBD" 라 씀) (b) 응력 완충 망 (c) 잘 짜인 망 · 전극 | 개념도 (정성) |
| 1 | (a–b) OM CDP · PGP (c–d) SEM (e–f) 개념도 (g) N₂ 등온선 (h) BET 0.4918 · 0.5549 (i) C₁₀ 1.832 · 3.889 | ★ 과립 강도 = 혼합 상태 지표 후보 (§7-6) |
| 2 | (a–b) 단면 SEM (막 vs 섬유) (c–d) 윗면 표면 기공 8.896 · 13.615 % (e–f) 이온 밀링 단면 (균열) (g) 인장 (h) SAICAS (i) MIP (j–k) 대칭셀 Nyquist (l) τ · N_M (m) 개념도 | ★ 균열 · 바인더 형태 · 수송 원자료 |
| 3 | (a) NCM622 2×3×2 모형 셋 (b) Pugh (c) A^U (d) Vickers | DFT 결과 (약한 고리) |
| 4 | (a) 반쪽 Nyquist (b) DRT (c) 첫 사이클 (d) 0.5C 100 사이클 (e–f) dQ/dV (g) 율속 (h) 전셀 첫 사이클 (i) 0.2C 200 사이클 (j) 0.5C 300 사이클 | ★ 성능 · 판독 (digitized.csv) |
| 5 | (a–b) 300 사이클 DRT 충 · 방전 (c–d) 나노압입 (가로축 단위 의심) (e–f) 100 사이클 표면 기공 1.865 · 5.539 % (g) 표면 기공 변화 (h–i) 10 사이클 두께 162 · 156 µm (j) 두께 변화 12.5 · 8.33 % (k–l) 50 사이클 이온 밀링 단면 | ★ 사후 균열 · 팽창 |
| 6 | (a) Pugh DFT vs MD (b) 모듈러스 DFT vs MD (c) 시간평균 von Mises (pristine ≈1.94 [판독]) (d) Li 궤적 (e) Li 밀도 (f) 되먹임 고리 개념도 | MD (약한 고리) |
| SI M1 | NCM622 pristine · CDE-model (군집 공공) · GIDE-model (분산 공공) 원자 모형 | 모형 정체 확인 (NCA 아님) |
| SI S1 | 순수 PTFE 2차 입자 (저 · 중 · 고배율) — 수백 µm 덩어리 · ≈0.2–0.3 µm 막대 1차 입자 [판독] | PTFE 원료 형태 |
| SI S2 | PGP 초기의 NCA 2차 입자 + PTFE 복합 (섬유 다리 강조) | 과립 형성 |
| SI S3 | PGP 뒤 과립 사진 (눈금 1 mm) | "≈2 mm" 근거 |
| SI S4 | (a) 맨 NCA (b) CDP 혼합 뒤 NCA — 작은 낱알이 큰 입자 표면에 붙은 채 | "1차 입자" 정체 (§3-2) |
| SI S5 | CDP 과립의 NCA "1차 입자" 응집 (각진 1–3 µm) | 〃 |
| SI S6 | PGP 혼합 순서 뒤 분말 (섬유 강조) | 탄소 혼합 뒤 섬유 유지 |
| SI S7 | PGP 과립의 NCA + 탄소 + 섬유 망 (PCBD) | PCBD |
| SI S8 | 혼합 분말 N₂ 등온선 (CDP · PGP) | 면적 숫자 없음 |
| SI S9 | 혼합 분말 기공 분포 0–30 nm | 계산법 미기재 |
| SI S10 | 미세 압축 시험 개략도 | — |
| SI S11 | 저배율 단면 (CDE 막 · GIDE 섬유) | 바인더 형태 |
| SI S12 | 고배율 단면 — 섬유 굵기 (CDE 50–100 nm · GIDE < 20 nm) | ★ PTFE 섬유 지름 (CL-66 대조, §7-4) |
| SI S13 | 저배율 윗면 (300 µm) | 표면 |
| SI S14 · S15 | 칠하지 않은 윗면 원본 (CDE · GIDE) | 표면 기공 원본 |
| SI S16 | toughness 36.6 · 121.2 kJ m⁻³ | 기계 |
| SI S17 | 180° 박리 곡선 · 평균 0.175 · 0.191 N mm⁻¹ | 🔴 본문 0.91 오기 |
| SI S18 | SAICAS 개략도 | — |
| SI S19 | SAICAS 수평력-시간 (30 · 100 µm) — 범례 없음 | 기계 |
| SI S20 | 정규화 누적 침투 — 0.6 µm 아래 겹침 | 기공 |
| SI S21 | 대칭셀 구성 (Al 박 · 전극 · 전해질 · 분리막) | 측정 구성 |
| SI S22 | DFT 다결정 B · E · G (128/135/156 · 141/208/203 · 54/84/79) | DFT 원값 |
| SI S23 | DFT 비등방 비 (max/min) B · E · G | 〃 |
| SI S24 | 0.1C 화성 반쪽 셀 (≈207 vs ≈209 mAh g⁻¹ [판독]) | ★ 저율 동등 → 수송 차이 |
| SI S25 · S26 | CDE · GIDE 1 · 10 · 50 · 100 사이클 전압 곡선 | 사이클 판독 |
| SI S27 · S28 | 300 사이클 뒤 전셀 Nyquist (충전 · 방전) — 거의 같음 | 🔴 사후 EIS 차이 약함 |
| SI S29 · S30 | 윗면 (10 사이클) 원본 · 칠한 영상 2.935 · 6.355 % | 표면 기공 |
| SI S31 · S32 | 100 사이클 윗면 원본 | 〃 |
| SI S33 | 사이클 전 단면 (144 µm) | 두께 기준 |
| SI S34 | 100 사이클 입자 단면 (CDE 균열 상자 · GIDE 온전) | 균열 |
| SI S35 | MD 온도 · NPT 부피 (미수렴) · 총 에너지 | 🔴 평형 미확인 |
| SI S36 | MD C_ij 9 개 · VRH B · G · E | 요동 탄성 원값 |
| SI S37 | MD MSD · D_Li | 확산 |
| 표 S1 | PTFE vs PVDF 물성 (20.0 · 30.2 mN m⁻¹ · 0.5 · 2.45 GPa · 23 · 55 MPa) — 출처 없음 · "PDVF" 오식 | 바인더 물성 (주의) |
| 표 S2 | 대칭셀 R_ion · A · L · ε · κ | ★ τ 재현 원자료 |
| 표 S3 | 나노압입 H · E · 탄성 회복 | 기계 |
| 표 S4 | DFT 단결정 탄성 최대 · 최소 | DFT |
| Note S1 식 | τ = R_ion·A·k·ε/(2d) · N_m = τ/ε | 식 확인 |

## 6. Post-processing ★
- **무엇을**: SEM 면적 문턱 → 표면 기공 % · 섬유 굵기 (눈대중 범위) · BET · MCT 강도 · UTM 곡선 적분 → toughness · SAICAS F_h 평균 · MIP 미분 · 누적 · 대칭셀 Nyquist 그래프법 (R_ion/3) → τ · N_M · Nyquist · DRT · dQ/dV · 나노압입 (Oliver–Pharr 류로 보이나 [미확인]) · DFT 응력-변형 → 탄성 텐서 → VRH 파생량 · MD 요동 → C_ij · 순간 응력 → von Mises 평균 · MSD → D · 블록 평균 · z 검정.
- **안 한 것**: 균열 입자 분율 · 균열 길이 정량 · 섬유 지름 통계 · 표면 기공 영상 수 · 셀 반복 통계 · σ_e 측정 · 전극 밀도/ε 의 시료별 값 · 캘린더 압력 기록 · 과립 크기 분포 · 공정별 에너지 · DFT 배치 앙상블 · MD 크기 · 시간 수렴 시험.
- **우리 후처리 (이 카드)**: τ · N_M · f · κ_eff 재계산 (단위 판정) · 공극률 몫 Bruggeman 분해 · 로딩 정합 · Hv–(B,G) 재현 · 격자 · 부피 정합 · 나노압입 깊이 단위 검산 · 그림 판독 69 행 (보정 검산 포함 — digitized.csv 머리) · MD 응력 요동 잡음 바닥 추정 (§10-16).

---

## 7. ★ 우리 작업에 주는 것 (→ `our_dem_baseline.md` 는 정본 브랜치에서 자리표시 상태 — 우리 수치는 메인 리포 CLAUDE.md · 원장 `docs/reviews/claims.json` 의 해당 줄을 병기)

### 7-1. 비교표 — 같은 이름 · 다른 양 주의

| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 수송 tortuosity (논문 τ) | 기공 (액체) 상 **2.91 → 2.37** (ε 0.305 · 0.333) · f 0.105 → 0.141 [우리 산술] | SE 상 tau2 — ps45 Hertz 7.24–5.03 · Tabor 4.12–2.78 (메인 CLAUDE.md 10-13 줄) | **같은 정의 (φ·σ₀/σ_eff), 다른 상** — 액체 기공 vs 고체 SE.  수치 비교 금지 · 측정법 (대칭셀 TLM) 만 빌린다 |
| PTFE 섬유 지름 | **< 20 nm (GIDE) · 50–100 nm (CDE)** (S12, 범위 · 통계 없음) | `PTFE_D = 0.25 µm` (CL-66 — 로프 Ø 0.248 µm 에 앵커) | 이 논문 값은 섬유 계층의 **가는 쪽** — 우리 0.25 µm 는 로프 계층.  정정이 아니라 계층 하나가 더 있다는 자료점 |
| PTFE 형태 → 수송 | CDE = NCA 표면 **막** + 굵은 섬유 → R_ct 147 Ω cm² / GIDE = 가는 섬유 → 33.6 | STEP3 `ptfe_stamp = centerline` (CL-60 본문 규약) — 막은 복셀 아래 크기라 표현 안 됨 (CL-49: 부피 점유 효과 −25 % 뿐, 표면 차단은 복셀이 못 봄) | 바인더 **막 대 섬유** 가 표면 차단을 정한다는 정성 사례 하나 — 우리 복셀이 못 보는 축 |
| AM 공정 균열 | 캘린더링 직후 큰 2차 입자 균열 (SEM 정성) | DEM Auerbach 파괴 판정 (K_IC 0.3 = 소결 펠릿값, LHS-31) | 크기 의존 방향은 같다 [추정] — 정량 비교 불가 (균열 분율 없음) |
| AM 탄성 (DFT) | NCM622 pristine **E 141 · B 128 · G 54 GPa · ν 0.315** (PBE · 0.2 eV/Å) | DEM AM E 140 GPa — **출처 철회 상태** (CL-90) | 숫자는 가깝지만 **다른 조성 (622 vs 811) · 계산값 · 느슨한 수렴** → 앵커로 쓰지 않는다 · "DFT 참고 한 점" 까지만 |

### 7-2. DEM + MPM (압밀 · 힘 사슬 · 파괴)
- **이 논문의 핵심 주장은 DEM 이 시험할 수 있는 가설이다** — "결합 과립의 점진 변형이 캘린더링 응력을 재분배해 개별 2차 입자의 최대 접촉력을 낮춘다".  논문은 힘 · 응력을 **한 번도 재지 않았다** (사후 SEM 만).  frame[5] 상 힘 사슬 · 파괴 (Auerbach) 는 DEM 몫 — 같은 압축 변위에서 (a) 흩어진 혼합 vs (b) 결합 덩어리 (깨지는 bond) 의 **큰 입자 최대 접촉력 분포 · Auerbach 파괴 분율**을 비교하면 이 주장의 부호를 가를 수 있다 [추정].  ⚠ 우리 DEM 덱에 깨지는 결합 (bond) 모형이 있는지 [미확인] — 없으면 새로 들여야 한다.
- **공극률 교락이 먼저다** — GIDE ε 0.333 vs CDE 0.305 (§3-4): 덜 눌린 전극이면 입자 응력도 작고 수송도 좋다.  DEM 비교는 반드시 **같은 최종 밀도 (또는 같은 압력)** 두 조건으로 나눠야 '과립 효과' 와 '덜 눌림' 을 가른다 [추정].
- **쌍봉 크기 효과**: 균열이 큰 (≈10 µm) 입자에 보이고 작은 각진 입자에는 안 보인다 (정성) — 같은 응력에서 접촉력 ∝ R², Auerbach 임계력 ∝ R 이면 큰 입자가 먼저 깨진다는 우리 판정식의 방향과 같다 [추정].
- **MPM**: PTFE 섬유 · 막의 소성 · 파단은 우리 MPM 연속체에 상으로 없다 (SE J2 만) — 이 논문 축은 MPM 밖.

### 7-3. STEP3 복셀 · 접촉망 σ
- **σ_e 측정이 없다** — 본문은 R_ct 감소 원인에 *"higher electrical conductivity"* 를 넣지만 전자 전도도 · 전자 저항을 잰 데이터가 0 이다 🔴.  우리 접촉망 σ_e 와 대조할 숫자가 없다.
- **이온 쪽은 액체 기공 경로** — 우리 STEP3 의 pore-τ 출력과 같은 상이지만 우리 대상 (ASSB) 에서는 SE 상이 주 경로라 직접 대조 대상이 아니다.  다만 **"바인더 막이 AM 표면을 덮어 R_ct 를 ×4.4 키운다"** 는 정성 관찰은 우리 복셀이 원리적으로 못 보는 sub-voxel 표면 차단 (CL-49) 의 실험 쪽 그림이다.
- **대칭셀 단위 함정** (§3-4) — 우리 대칭셀 계획 (메인 `docs/symmetric_cell_ionic_plan_20261013.md`) 에서 R 을 Ω 와 Ω cm² 중 어느 쪽으로 기록할지, A 를 몇 번 곱하는지 결과 전에 못박아야 한다 (이 논문은 같은 숫자가 Ω cm² 로 표기되고 식은 Ω 로 계산).

### 7-4. 건식 PTFE 작업
- **조성 · 공정 기준점**: 96 : 1.8 : 2.2 (NCA : KB : PTFE) · 10 mAh cm⁻² · 46–48 mg cm⁻² · 3.3–3.4 g cm⁻³ · 144 µm · PGP 2000 rpm × 2 min × 5 (액체 LIB).
- **섬유 계층**: < 20 nm (GIDE) · 50–100 nm (CDE) — `lee2025_dual_fibrous_ptfe_dry_electrode` 의 섬유 + 로프 이중 계층과 같이 보면, 우리 `PTFE_D 0.25 µm` (CL-66) 는 로프 쪽 · 이 논문은 섬유 쪽.  CL-67 (씨더 끝점 거리 중앙 4.13 µm) 에 대응하는 섬유 길이는 이 논문에 없다.
- **표 S1 물성 (PTFE 20.0 mN m⁻¹ · 0.5 GPa · 23 MPa)** — 출처 인용 없음 → DEM 바인더 입력으로 옮기지 않는다 (원문 확인 안 된 값, 규율 ⑥).
- **"순서가 형태를 바꾼다"**: 같은 PTFE 양 · 같은 뒤 공정에서 첨가 순서 (AM + PTFE 먼저) 가 섬유 굵기 · 막 형성을 바꾼다는 보고 — 우리 STEP3 PTFE 스탬프는 형태 (막 · 섬유 · 굵기) 를 공정에서 받지 않고 고정 규약으로 넣는다 → 이 논문 같은 공정 대비를 모델로 재현할 길이 지금은 없다 (F 목록 후보).

### 7-5. AM 파괴 (Auerbach) · 사이클 균열 원장 (A10)
- **공정 균열이 초기 조건** — 저자 사슬의 출발점은 "캘린더링 직후 이미 깨진 입자" 다.  우리 사이클 접촉 원장 (`scripts/cycle_contact_ledger.py`, 메인 `docs/a10_cycle_chemomech_design.md`) 은 온전한 접촉에서 시작해 수축 · 개구로 파단을 센다.  **압밀 DEM 의 Auerbach 파괴 분율을 원장의 t = 0 상태로 넘기는 연결**이 비어 있다 [추정] — 이 논문은 그 연결이 수명을 가른다고 주장하는 실험 사례 (정량 없음).
- **반쪽 셀 수명 비교의 교락** — 10 mAh cm⁻² 를 Li 금속에서 매 사이클 벗기는 반쪽 셀의 CDE "60 사이클 실패" 에는 Li 음극 몫이 섞인다 (저자 인정).  우리 원장 검증 표적으로는 **전셀** 숫자 (0.5C 300 사이클 86.1 vs 80.9 %) 가 덜 오염돼 있다 — 차이 5.2 %p 로 반쪽 셀보다 훨씬 작다.
- **쌍봉** — 우리 Kang & Shin 쌍봉 앵커 (`kang2025_toughened_bimodal_nca_lzo`) 와 같이 쌍봉 NCA 지만 비율 미상 · 쌍봉 대 단봉 대조 없음 → 원장의 쌍봉 > 단봉 방향을 검증하는 데는 못 쓴다.
- **DFT 의 "탈리 → 취성" 고리** — 원장에 국소 SOC 불균일 → G_c (또는 파괴 문턱) 저하 항을 넣을 근거로는 약하다 (NCM622 · 0.2 eV/Å · 단일 배치 · Pugh 는 금속용 경험 지표 · 공정 균열은 완전 리튬화 상태에서 났는데 그때 B/G 2.38 "연성" — §10-13).

### 7-6. ★ 믹서 논문 계획 (메인 `docs/mixer_paper_pipeline_draft_20261013.md` V1 · V2 · V3) 과 이종기술 논지
- **V2 (혼합 시간 · 강도 고정) — 교락 경고 사례** — 저자는 *"increasing the RPM or duration of conventional mixing promotes uncontrolled fibrillation accompanied by particle damage rather than pre-organized granule formation"* (p.3) 이라 쓰지만 **그 대조 실험이 없다**.  GIDE = CDE 공정 + PGP 10 분 (2000 rpm) 이라 **기계 에너지가 더 들어갔다** — "순서 효과" 와 "에너지 · 시간 효과" 가 섞여 있다 🔴.  우리 V2 설계는 (a) 같은 총 시간 · 다른 순서 (b) 같은 순서 · 다른 시간 둘로 나눠야 이 혼동을 피한다 [추정].
- **V1 (코팅 상태) 의 사촌 축 = 첨가 순서** — 여기서 "코팅" 은 SE 가 아니라 **바인더가 먼저 AM 을 감싸는 상태**다.  같은 총 성분에서 무엇을 먼저 AM 에 붙이느냐가 최종 분포를 바꾼다는 정성 사례 (액체 LIB · PTFE) — 우리 논지 (SE 선코팅 → SE–SE 응집 ↓) 의 **직접 근거가 아니다** (다른 상 · 다른 기전 언어 = "응력 완충").
- **혼합 상태 측정 아이디어** (V2 실험 쪽): 과립 압축 강도 C₁₀ (MCT) · 혼합 분말 BET · 섬유화 전 분말 SEM 의 PTFE 형태 — 이 논문이 쓴 세 지표는 "섬유화 전 분말 EDS" 계획에 붙일 수 있는 보조 지표 [추정].
- **V3 (SE 함량)**: n/a (SE 없음 · PTFE 한 수준).
- **스케일**: 과립 ≈2 mm · PCBD = 서브 µm — 우리 믹서 DEM (탄소 미해상, 상자 ≈100 µm 급) 의 양 끝 밖 [추정].

### 7-7. DFT 트랙 (탄성 텐서 작업 흐름) 에 주는 교훈
- 같은 도구 (VASPKIT 응력-변형 · VRH) 를 쓰는 우리 탄성 계산의 **반면교사**: ① 힘 수렴 0.2 eV/Å 은 이완된-이온 탄성 상수에 큰 오차를 남길 수 있다 [추정] ② 배치 앙상블 없이 "안정 수렴한 대표 구조" 하나 ③ 경도 (Chen 식) 는 B · G 의 재표현 — 독립 지표로 세지 않는다 ④ 대리 조성 (NCA → NCM622) 은 본문 · 캡션에 적는다.
- MLIP-MD 탄성: 요동 항만으로 C 를 내면 Born 항이 빠져 값이 체계적으로 작다 [추정] — 이 논문 MD/DFT 비 0.21–0.39 와 같은 방향 (원인 미분리).

### 7-8. frame[4] · frame[5]
- **frame[5]**: 이 논문은 **실험 사슬 (공정 → 미세구조 → 전기화학)** 반쪽을 가졌고, 주장의 핵심인 **입자 · 과립 스케일 역학 (응력 재분배)** 반쪽이 비어 있다 — 원자 스케일 DFT/MD 로 그 빈칸을 메우려 했지만 스케일이 4–6 자릿수 다르다 (nm vs 2 mm 과립 · 10 µm 입자).  그 빈칸이 정확히 DEM (힘 사슬 · 파괴) 의 영역.
- **frame[4]**: 보정 · 교차검증 대상 수치 없음 (모형 없는 실험 논문).  "측정 = 실험 점 하나" 로만 쓴다.

---

## 8. ★★ 우리 연구에 주는 insight (번호마다: 논문이 보인 것 → 우리에게 뜻 → 할 일)

**8-1. "과립이 응력을 흡수한다" 는 측정되지 않은 DEM 질문이다.**
- 논문: 응력 완충을 사후 SEM (균열 적음) 으로만 주장 · 힘 · 응력 측정 0 · 공극률은 GIDE 가 더 높다 (0.333 vs 0.305).
- 뜻: 결합 덩어리 vs 흩어진 혼합의 최대 접촉력 · 파괴 분율 비교는 frame[5] 상 DEM 의 고유 몫 — 실험이 못 가른 "과립 효과 vs 덜 눌림" 을 같은 밀도 조건으로 가를 수 있다 [추정].
- 할 일: 우리 DEM 덱의 결합 (bond) 모형 유무 확인 → 있으면 같은 압축 변위 · 같은 최종 밀도 두 조건에서 큰 AM 의 접촉력 분포 비교를 후보 과제로 적는다 (1저자 판단).

**8-2. 수송 개선의 ≈45 % 는 공극률 차이만으로도 나온다 [우리 산술 · Bruggeman 가정].**
- 논문: N_M 9.54 → 7.11 (재계산) · ε 0.305 → 0.333.
- 뜻: "같은 캘린더링 압력" 이라도 결과 밀도가 다르면 미세구조 효과와 압밀 효과가 섞인다 — 우리 대칭셀 · 모델 비교도 **같은 ε** 에서 해야 형태 효과를 읽을 수 있다.
- 할 일: 우리 대칭셀 계획에서 시료별 ε (질량 · 두께) 를 같은 날 기록 항목으로 (이미 계획의 기공 측정과 묶을 수 있음).

**8-3. 공정 균열 → 사이클 균열 원장의 초기 조건.**
- 논문: 캘린더링 직후 균열이 수명 차이의 출발점이라고 주장 · 전셀 300 사이클 차이 5.2 %p.
- 뜻: 우리 A10 원장은 t = 0 균열 분율을 받지 않는다 — 압밀 DEM (Auerbach) → 원장 연결이 비어 있다.
- 할 일: `comparison_vs_ours_DEM.md` F 절 (우리가 아직 못 하는 것) 에 "공정 균열 초기 조건 · 결합 과립 · 첨가 순서" 줄 등재 제안 — 공유 파일이라 이 커밋에서는 손대지 않고 줄 문안만 따로 보고.

**8-4. 이 논문 숫자를 쓸 때의 함정 셋.**
- 박리 0.91 → 실제 그림 0.191 N mm⁻¹ · R_ion 단위 Ω cm² → 실제 Ω · N_M 7.02 → 재계산 7.11 · 0.2C 전셀 86.3/84.8 % → 그림 ≈89.5/≈86.5 % — 인용 시 그림 · 재계산값을 병기한다.

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Kim et al. (*Chem. Eng. J.* 2026) pre-granulated NCA with PTFE (2000 rpm, 2 min × 5, before carbon addition) in a 96:1.8:2.2 dry-processed cathode (10 mAh cm⁻²) and reported thinner PTFE fibrils (< 20 vs 50–100 nm), fewer calendering-induced cracks in large secondary particles (SEM, qualitative), a lower pore-phase tortuosity factor (2.91 → 2.37) and charge-transfer resistance (147 → 33.6 Ω cm²), and 86.1 vs 80.9 % full-cell retention after 300 cycles at 0.5C."
- 국문: *"건식 PTFE 양극에서 탄소 전에 NCA + PTFE 만 먼저 과립화하면 공정 균열이 줄고 수송이 좋아진다는 보고가 있다 (Kim 2026) — 단 응력 완충은 측정되지 않았고 과립화 전극이 더 다공 (ε 0.333 vs 0.305) 했다."*

## 10. 🔴 레드 플래그 — 원문 불일치 · 빠진 조건 · 해석 과장 (over-claim 방지)

1. **박리 강도 오기**: 본문 p.6 *"0.91 N mm−1"* ↔ SI Fig S17b **0.191** (CDE 0.175) — 본문대로면 ×5.2, 그림대로면 +9 %.
2. **R_ion 단위**: 표 S2 · 본문 *"Ω·cm²"* 인데 식 (1) 이 A 를 다시 곱해 τ 를 낸다 — 인쇄 τ 2.906 · 2.369 는 R 을 **Ω** 로 넣을 때만 재현 (§3-4) · Fig 2j–k 의 x 축도 Ω.
3. **R_ion 값 셋**: 본문 18.06 · 13 / 표 S2 18.03 · 13.44 / Fig 2j–k 표지 × 3 [판독] ≈20.5 · ≈14.1 Ω — 25.58 % 는 18.06 과 13.44 의 혼합.
4. **N_M(GIDE) = 7.02 (그림 7.018)** — 인쇄 R · A · κ · d 로 **7.108** (자리 바뀜으로 보임).
5. **"18.6 % 경로 길이 감소"** — tortuosity factor (tau2) 를 길이로 읽음 · 길이 비는 −9.7 %.
6. **ε 칸 "(%)" 에 분율 값** · 같은 두께 · 조성에서 ε 차이 = 로딩 4 % 차이 함의 · ε 측정법 미기재 · **공극률 교락** (N_M 개선의 ≈45 % 를 Bruggeman 이 설명).
7. **MIP**: 본문 "CDE 500–1500 nm bimodal" ↔ 그림 표지 ≈0.5 · ≈6 µm · 누적 곡선 70 % 겹침.
8. **전셀 0.2C 200 사이클**: 본문 86.3 · 84.8 % ↔ 그림 끝점 ≈89.5 · ≈86.5 % [판독, 같은 축 보정 검산 통과].
9. **셀이 그림마다 다른 흔적**: Fig 4c 첫 사이클 186 · 195 ↔ S25 · S26 1st 170 · 183 mAh g⁻¹ ↔ Fig 4d 첫 점 8.81 vs Fig 4g 0.5C 9.41 mAh cm⁻² — 반복 수 · 대표 셀 선정 [미확인] · 오차 막대 0.
10. **그림 참조 오류 다섯**: BET/등온선 Fig 1g ↔ 1h 뒤바뀜 · *"red region in Fig. 2a"* 없음 · 나노압입의 *"stress–strain curves (Fig. 2h)"* (= 2g) · 0.242 eV 의 *"(Fig. S36)"* (= 탄성 그림) · 되먹임 고리 서술의 *"(Fig. 3d)"* (= 경도 그림, 개념도는 6f).
11. **나노압입 축 단위**: Fig 5c–d *"Penetration Depth (nm)"* — 하중 2.8 mN · H 19–25 MPa 면 깊이 ≈2 µm 급 (§3-8).
12. **핵심 대조의 설계**: Fig 1 의 CDP 모델 혼합물 = 전단 거의 없음 vs PGP = 전단 — "순서" 가 아니라 "전단 유무" 대조 · 전극 단계도 GIDE 에 PGP 에너지가 추가 · *"increasing the RPM or duration … promotes uncontrolled fibrillation"* 은 데이터 없음.
13. **"격자 연성" 논리의 자기 모순**: 공정 균열은 완전 리튬화 (pristine, B/G 2.38 "연성") 상태에서 났다 · pristine 은 Pugh · 경도로는 가장 안전한데 비등방 (A^U · E · G max/min 최대) 과 MD von Mises (≈1.94 GPa, 최대) 로는 가장 위험 — 저자 지표끼리 서로 어긋나는데 본문은 pristine 쪽을 논하지 않는다 · 캘린더링 입계 균열은 격자 B/G 보다 입계 강도 문제 [추정].
14. **DFT 모형 · 설정**: NCA 대신 **NCM622** (본문 · 캡션 미기재) · 0.2 eV/Å · DFT+U · 스핀 [미확인] · 모드당 구조 하나 · 벌크 격자 (4.9 · 6.0 · 10.6 Å) 가 슈퍼셀 (×2.06 · ×3.20 · ×2.08) · MD 부피와 안 맞음 · Debye 온도 계산했다면서 값 없음.
15. **MD 탄성 식**: *"Cαβ = (V/k_BT)⟨δσα δσβ⟩"* 는 NVT 응력 요동 공식의 **요동 항 하나** (Born 항 · 운동 항 없음) · 인용은 Parrinello–Rahman *"Strain fluctuations"* (변형 요동, NσT) · **Berendsen 열욕 · 압력조는 정준 요동을 주지 않는다** → MD 모듈러스가 DFT 의 0.21–0.39 배인 원인을 *"열 연화 · MLIP"* 로 돌릴 수 없다 [추정].
16. **"내부 von Mises 응력"** — 순간 응력의 열 요동만으로도 시간평균 von Mises 가 생긴다: 그들 자신의 G_MD (11–21 GPa) 와 부피 (≈4100 Å³) 로 등방 근사하면 잡음 바닥 ≈**0.39–0.53 GPa** [우리 산술 · 차수 추정] — GIDE 0.63 은 바닥에 가깝고, pristine ≈1.94 [판독] 은 S35b 의 **미평형 부피 (50 ps 끝에도 증가)** 가 남긴 잔류 응력일 수 있다 [추정].
17. **D_Li**: MSD ≈3 Å² @ 200 ps (rms ≈1.7 Å) — 자리 간 이동 몇 번으로 낸 값이라 "비슷한 이동도 (비 0.95)" 의 통계 근거가 약하다 · 실험 확산계수 대조 없음.
18. **σ_e 주장에 데이터 없음**: R_ct 감소 원인에 *"higher electrical conductivity"* — 전자 전도도 측정 0.
19. **사후 EIS**: S27 · S28 원 Nyquist 가 거의 같은데 본문은 CDE 저항이 크다고 결론 · DRT 가 측정 창 밖까지 그려짐 · 반쪽 DRT 의 < 1 Hz 피크는 높이가 같은데 *"suppressed peaks across all frequency ranges"*.
20. **빠진 공정 조건**: CDE 혼합 · 반죽 · 캘린더 · 라미네이트 조건 전부 · 캘린더 압력 (*"identical"* 이라면서 값 없음) · NCA 크기 분획 비 · PTFE 등급 · 대칭셀 전해질 · 사후 시료가 반쪽/전셀 중 어느 것인지 · 50 vs 100 사이클 표기 (Fig 5k–l vs S34).
21. **과장**: 초록 *"Electron microscopy … validates the mechanism"* (결과는 보였지 기전 (응력 완충) 은 아님) · 결론 *"a regime where conventional dry electrodes fail"* (전셀 CDE 300 사이클 80.9 % 는 실패가 아님) · *"directly transferable to … twin-screw and high-shear granulation"* · *"additional process cost is minimal"* (시험 없음).
22. **표기 · 조판**: Scheme 1 *"fraction force"* · 표 S1 *"PDVF"* · 출처 없는 표 S1 물성값 · 표 S2 캡션 *"additive-incorporated electrodes"* (이 논문엔 첨가제 비교 없음 — 다른 원고 양식에서 옮겨온 듯 [추정]) · S17a *"Strain (mm)"* · S19 범례 없음 · 본문 *"6 3%"* · SI 재료 문장의 괄호 미닫힘 · MD 를 *"slabs configurations"* 라 부름 (실제는 주기 벌크) · 본문 *"each containing 60 vacancy sites"* (pristine 은 공공 0).
23. **데이터 비공개** (p.14) — 위 판독 · 재계산을 원자료로 확인할 길이 없다.

## 11. 다른 카드 정정 후보 (보고만 — 이 커밋에서 손대지 않음)
1. `lee2026_lpscl_coating_thickness_ncm811` 머리 (24 행): *"현재 litdb 전체에 `Taeseup Song` 등장 0회"* — 이미 낡았다: `kim2023_mechanofusion_ncm811_lpscl_core_shell_intimate_contact` (교신) · 이 카드 (공저) 에 Taeseup Song 이 있다.
2. (가드, 정정 아님) 정본에서 "Gachon" 이 나오는 기존 카드 셋 (`choi2026_elastomeric_li_metal_anode` · `jung2026_sio2_cosubstitution_mechanical_argyrodite` · `lee2026_eecfp_dnn_electrolyte_ce_lmb`) 에 **Junghyun Choi 는 없다** — 특히 `jung2026_…` 의 가천대 저자는 **Seung Ho Choi** (KETI 겸) 라 같은 "가천대 Choi" 로 묶어 팔로우 랩 표지를 붙이면 안 된다.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)

**같은 그룹 후보 (팔로우 랩 카드 후보 — "J. Choi" 가 Junghyun Choi 인지는 머리글자만이라 [미확인])**

| 번호 | 서지 (원문 목록 그대로) | 왜 · 카드 |
|---|---|---|
| 15 | J. Choi, S. Moon, D. Lee, S. Han, S. Yang, D.S. Jung, J. Joo, P.J. Kim, Dry electrode technology: a new processing paradigm for enhancing performance and sustainability in lithium-based batteries, Chem. Eng. J. 519 (2025) 165044. | 카드 없음 — 같은 교신 조합 (J. Choi · D. Lee · P.J. Kim) 의 건식 전극 리뷰로 보임 |
| 16 | J. Kim, K. Park, M. Kim, H. Lee, J. Choi, H.B. Park, H. Kim, J. Jang, Y.H. Kim, T. Song, 10 mAh cm− 2 cathode by roll-to-roll process for low cost and high energy density Li-ion batteries, Adv. Energy Mater. 14 (10) (2024) 2303455. | 카드 없음 — 같은 10 mAh cm⁻² 건식 양극 계열 |
| 17 | S. Han, E.-H. Noh, S. Chae, K. Kwon, J. Lee, J.-S. Woo, S. Park, J.W. Lee, P.J. Kim, T. Song, Mitigating PTFE decomposition in ultra thick dry-processed anodes for high energy density lithium-ion batteries, J. Energy Storage 96 (2024) 112693. | 카드 없음 — 건식 음극 PTFE 분해 |
| 20 | J. Lee, C.Y. Son, S. Han, S. Yang, P.J. Kim, D. Lee, J.W. Lee, W.-H. Ryu, J. Choi, Anode interface-stabilizing dry process employing a binary binder system for ultra-thick and durable battery electrode fabrication, Chem. Eng. J. 503 (2025) 158271. | 카드 없음 — 이원 바인더 건식 후막 |
| 22 | K.-E. Sung, I. Hwang, J. Choi, S.-K. Jung, J. Yoon, Enhanced adhesion in PTFE-based dry electrodes with hydrogen bonding co-binder integration for advanced lithium-ion batteries, Chem. Eng. J. 511 (2025) 161789. | 카드 없음 — PTFE 건식 접착 (같은 J. Choi 인지 [미확인]) |
| 23 | K. Kwon, J. Kim, S. Han, J. Lee, H. Lee, J. Kwon, J. Lee, J. Seo, P.J. Kim, T. Song, J. Choi, Low-resistance LiFePO4 thick film electrode processed with dry electrode technology for high-energy-density lithium-ion batteries, Small Sci. 4 (5) (2024) 2300302. | 카드 없음 — 건식 LFP 후막 |
| 50 | S. Han, W. Jeong, R. Kang, M. Kim, M. Jeong, H.-W. Lee, Y.-J. An, H.-J. Ji, M. Yoon, P.J. Kim, S. Sun, T. Song, D. Lee, W.-J. Kwak, J. Choi, Tailored electrolyte additive design for suppressing irreversibility in dry-processed anodes and enhancing electrochemical stability in full-cells, EES Batteries 1 (5) (2025) 1267–1278. | 카드 없음 — 같은 교신 셋 (S. Sun · D. Lee · J. Choi) |

**우리 축에 직접 닿는 것**

| 번호 | 서지 (원문 목록 그대로) | 왜 · 카드 |
|---|---|---|
| 27 | C. Meyer, M. Kosfeld, W. Haselrieder, A. Kwade, Process modeling of the electrode calendering of lithium-ion batteries regarding variation of cathode active materials and mass loadings, J. Energy Storage 18 (2018) 371–379. | 카드 없음 — 캘린더링 공정 모형 (DEM 압밀 대조) |
| 28 | R. Tao, B. Steinhoff, C.H. Sawicki, J. Sharma, K. Sardo, A. Bishtawi, T. Gibbs, J. Li, Unraveling the impact of the degree of dry mixing on dry-processed lithium-ion battery electrodes, J. Power Sources 580 (2023) 233379. | 카드 없음 — **건식 혼합 정도** = 믹서 V2 축의 선례 |
| 31 | B. Ludwig, J. Liu, I.M. Chen, Y. Liu, W. Shou, Y. Wang, H. Pan, Understanding interfacial-energy-driven dry powder mixing for solvent-free additive manufacturing of Li-ion battery electrodes, Adv. Mater. Interfaces 4 (21) (2017) 1700570. | 카드 없음 — 계면 에너지 구동 건식 혼합 (이종기술 논지 §2 의 표면 에너지 축) |
| 33 | A. Gyulai, W. Bauer, H. Ehrenberg, Dry electrode manufacturing in a calender: the role of powder premixing for electrode quality and electrochemical performance, ACS Appl. Energy Mater. 6 (10) (2023) 5122–5134. | 카드 없음 (`nam2026_dpe_microstructure_review` 가 인용) — 예비 혼합 → 캘린더 품질 |
| 36 | M. Prasad, S. Hein, T. Danner, A. Latz, Effect of a Heterogeneous Distribution of the Conductive Additives and Binder Domain on the Impedances of lithium-Ion Battery Electrodes, Electrochemical Society Meeting Abstracts 241, The Electrochemical Society, Inc, 2022. , (pp. 266–266). | 카드 없음 — CBD 불균일 → 임피던스 모형 |
| 43 | S. Cottrino, Y. Jorand, E. Maire, J. Adrien, Characterization by X-ray tomography of granulated alumina powder during in situ die compaction, Mater. Charact. 81 (2013) 111–123. | 카드 없음 — **과립 압밀의 단층 촬영** (DEM 과립 압밀 검증 표적 후보) |
| 46 | H. Abe, K. Sato, M. Naito, K. Nogi, T. Hotta, J.-i. Tatami, K. Komeya, Effects of granule compaction procedures on defect structure, fracture strength and thermal conductivity of AlN ceramics, Powder Technol. 159 (3) (2005) 155–160. | 카드 없음 — 과립 압밀 결함 |
| 48 | K.-J. Park, J.-Y. Hwang, H.-H. Ryu, F. Maglia, S.-J. Kim, P. Lamp, C.S. Yoon, Y.-K. Sun, Degradation mechanism of Ni-enriched NCA cathode for lithium batteries: are microcracks really critical? ACS Energy Lett. 4 (6) (2019) 1394–1400. | 카드 없음 — NCA 미세 균열 · 사이클 |
| 53 | X. He, X. Ding, R. Xu, Anisotropic mechanical properties of LiNixMnyCo1-x-yO2 cathodes for Li-ion batteries: a first-principles theoretical study, Acta Mater. 267 (2024) 119751. | 카드 없음 — NCM DFT 탄성 (이 논문 DFT 의 직접 인용) |
| 60 | J.C. Stallard, L. Wheatcroft, S.G. Booth, R. Boston, S.A. Corr, M.F. De Volder, B.J. Inkson, N.A. Fleck, Mechanical properties of cathode materials for lithium-ion batteries, Joule 6 (5) (2022) 984–1007. | 정본 카드 `stallard2022_cathode_mechanical_properties_review` |
| 63 | Y. Bi, J. Tao, Y. Wu, L. Li, Y. Xu, E. Hu, B. Wu, J. Hu, C. Wang, J.-G. Zhang, Reversible planar gliding and microcracking in a single-crystalline Ni-rich cathode, Science 370 (6522) (2020) 1313–1317. | 카드 없음 — 균열 · 상전이 결합 |
| 69 | B. Deng, P. Zhong, K. Jun, J. Riebesell, K. Han, C.J. Bartel, G. Ceder, CHGNet as a pretrained universal neural network potential for charge-informed atomistic modelling, Nature Machine Intelligence 5 (9) (2023) 1031–1041. | 카드 없음 — 이 논문 MD 퍼텐셜 원전 |
| 70 | M. Parrinello, A. Rahman, Strain fluctuations and elastic constants, J. Chem. Phys. 76 (5) (1982) 2662–2666. | 카드 없음 — §10-15 (변형 요동식 원전인데 응력 요동식의 근거로 인용됨) |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-13)
- 본문 15 쪽 · SI 51 쪽 텍스트 층 전수 (pdftotext) · 저자 · 소속 · 교신 · 날짜 · DOI · 특집 · 연구비 · 데이터 진술 = p.1 · p.13–14 · SI p.1 그대로 옮김 · SI 쪽 지도 (방법 p.2–7 · 표 p.8–11 · Note p.12 · 그림 p.13–49) 확인.
- 크롭 51 장 손 크롭: 본문 그림 = 래스터 원본 300 ppi (Scheme 1 · 그림 6 은 벡터 혼합) · SI 그림 = 래스터 원본 96–220 ppi 를 ≥200 dpi 로 · SI 표 · 식 = 벡터 300 dpi · 흰 여백만 자름 · 전부 렌더로 열람 (접촉 시트 포함).
- 판독 보정 검산: Fig 4j 끝점 86.2/80.8 (인쇄 86.1/80.9) · Fig 4c 끝점 186.3/195.4 (인쇄 185/195) · Fig 6b DFT 막대 ≤2 % (인쇄 S22) · Fig 6c CDE · GIDE 0.880/0.628 (인쇄 0.88/0.63) — 같은 보정으로 Fig 4i (≈89.5/≈86.5) · Fig 6c pristine (≈1.94) 을 읽음.
- 재계산: τ · N_M 식 (1)(2) 단위 판정 · Hv(B,G) · 표 S4 비 = S23 · 나노압입 감소율 · 표면 기공 비 · 두께 · 로딩 · 밀도 · 격자 배수 · MD 부피/화학식 · 0.242 eV/원자.
- 빨간 칠 확인: Fig 2a · 2b 크롭에서 빨간 화소 0 (본문 "red region in Fig. 2a" 없음).
- 정본 litdb 중복 확인: `git ls-tree` 로 `litdb/papers/` 429 장 전수 + 체크아웃 전 파일 DOI (179740) · 제목 낱말 (pre-granulation · granule-induced · crack-delithiation · GIDE) grep — 이 논문 카드 · 인용 없음.

## 🔗 관련 카드
- PTFE 건식 전극: `hippauf2019_dry_film_ptfe_sulfide_cathode_sheet` · `lee2025_dual_fibrous_ptfe_dry_electrode` · `matthews2024_ptfe_nanofibril_network` · `lee2026_unveiling_ptfe_dry_electrode_digital_twin` · `lee2025_corolling_dryprocess_lpscl_ptfe` · `kang2025_bollard_anchored_binder_dry_electrode` · `mun2025_dry_electrode_technology_assb_review` · `liu2025_dry_processing_high_energy_li_batteries_review` · `nam2026_dpe_microstructure_review`.
- 건식 혼합 · 공정 에너지: `frankenberg2025_milling_dry_processed_sulfide_cathode_microstructure` · `lee2024_shear_force_dry_process_cathode_coverage` · `sun2026_dem_extrusion_recirculation_dry_electrode` · `zhang2026_xct_dem_cathode_calendering_peel_calibration`.
- NCA · 균열 · 기계: `koo2025_cnt_wrapped_sc_nca_dry_cathode` · `kang2025_toughened_bimodal_nca_lzo` · `intergranular_cracking_nmc811_jmca2023` · `trevisanello2021_sc_pc_ncm_cracking_diffusion` · `lee2026_microcrack_tolerant_bilayer_cathode_chemomech_fastcharging` · `wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem` · `sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile` · `sharma2023_nmc_single_crystal_anisotropic_nanoindentation` · `stallard2022_cathode_mechanical_properties_review` · `dem_mechanical_stresses_ssb_electrode_cycling` · `bucci2017_chemomech_failure_assb_cycling_czm`.
- 대칭셀 tortuosity: `landesfeind2016_tortuosity_eis_electrodes_separators` · `malifarge2017_tortuosity_symmetric_cell_impedance_tlm` · `pouraghajan2018_tortuosity_polarization_interrupt_vs_blocking_electrolyte` · `morasch2018_binder_gradient_impedance_tortuosity` · `nguyen2020_electrode_tortuosity_factor`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
