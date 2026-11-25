<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     형식 이웃 = kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation.md (같은 팔로우 랩, 같은 날) · kim2023_mechanofusion_ncm811_lpscl_core_shell_intimate_contact.md · kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps.md.
     쪽 표기 = 본문 "p.N" (= 학술지 인쇄 쪽 1944–1953; 받은 PDF 2–11 쪽.  PDF 1 쪽 = 쪽 번호 없는 표지 그림 홍보면) · SI "SI p.N" (= 받은 SI PDF N 쪽 = 인쇄 S-번호, 전 34 쪽 —
     p.1 제목 · 저자 / p.2–5 실험 · 계산 방법 (FEM 식 1–5) / p.6–7 Note S1–S2 / p.8–29 그림 S1–S22 (한 쪽에 하나) / p.30–32 표 S1–S3 / p.33–34 참고문헌).
     값 표지: [인쇄] = 본문 · 표 · 그림 안 숫자 · [판독] = 그림에서 읽은 값 (litdb/figures/<slug>/digitized.csv — 보정 검산은 파일 머리, TREND 전용) ·
     [우리 산술] = 인쇄값으로 우리가 다시 한 계산 · [추정] = 우리 해석 · [미확인] = 본문 10 쪽 + SI 34 쪽 전수에 없음 · [SI 미확보] = 본문이 인용하지만 받은 SI PDF 에 없음 (Video S1).
     ⚠ 본문 PDF 의 글꼴 대응 때문에 텍스트 추출에서 "~" 가 "B", "−" 가 빈칸, "µm" 가 "mm" 로 나온다 — 이 카드의 수치는 해당 줄을 300 dpi 로 렌더해 확인한 값이다 (원문 대조 기록).
     크롭 35 장 (표지 그림 · 그림 1–5 · SI 그림 S1–S22 · SI 표 S1–S3 · SI FEM 식 두 쪽 · Note S1–S2) 전부 렌더로 열람. -->

# PTFE 건식 후막 Si/흑연 음극 (96 : 1 : 3 · 2.1 g cm⁻³ · ≈63 µm · 13.5 mg cm⁻²) 을 SBR 프라이머 Cu 대신 **Li 6.5 µm 를 입힌 Cu 박 (Li/Cu)** 위에 라미네이트하면 박리는 비슷하게 남고 (≈3.45 vs ≈3.85 gf/mm [판독]) 계면 저항은 절반 (≈0.021 vs ≈0.046 [판독]) · Li 가 전해질 없이 고상 확산으로 음극 아래쪽을 미리 리튬화해 반쪽 셀 ICE 86.7 → 100.2 % · NCM811 전셀 ICE 74.8 → 93.3 % · 첫 방전 ≈4.5 → 5.63 mAh cm⁻² — 단 Li 공급은 비가역 손실의 1.42 배이고, 500 사이클 절대 감쇠는 두 셀이 거의 같다 (Li 재고 오프셋) · LFP 그림 5a 와 표 S1 의 숫자가 본문과 어긋난다 — Hyun-Wook Lee · Woojin Jeong · Seongsoo Park … Janghyuk Moon · Junghyun Choi · Won-Jin Kwak (UNIST · 가천대 · 중앙대 외, Energy Environ. Sci. 2026)

> **[팔로우 랩: 가천대 최준현 교수 (건식 전극)]**
> slug `lee2026_li_underlayer_primer_free_dry_prelithiated_thick_anode` · DOI `10.1039/d5ee05739f` · type `exp (PTFE binder dry process 건식 후막 Si/흑연 음극 · Li/Cu 밑층 = 프라이머 대체 + 고상 선리튬화 · 박리 · 계면 저항 · TOF-SIMS · XPS · XRD · CV · EIS/DRT impedance · 반쪽 셀 · LFP / NCM811 전셀 · TEM, 액체 전해질) + FEM (COMSOL 6.2 DFN multiphysics · Blender 적층 3D microstructure 50 µm) + MD (Materials Studio COMPASS 접착 에너지 · DMol3 원자 전하); DEM · MPM 없음` · PDF `b0e029b2-4._Integrated_one-step_dry_process_enabling_prelithiated_thick_electrodes_without_primer_coating_for_high_energy_density_and_initial_coulombic_efficiency.pdf` · SI `f13c3292-4._Sup_Integrated_one-step_dry_process_enabling_prelithiated_thick_electrodes_without_primer_coating_for_high_energy_density_and_initial_coulombic_efficiency.pdf` · digested `2026-10-13` · status ✅
>
> elements: Li, C, O, F, P, Si, Cu, Ni, Co, Mn, Fe
> methods: md, adhesion, dft
>
> **원제**: *Integrated one-step dry process enabling prelithiated thick electrodes without primer coating for high energy density and initial coulombic efficiency* (p.1944)
> **저자 (p.1944 · SI p.1, 인쇄 순서 그대로)**: Hyun-Wook Lee^†a · Woojin Jeong^†b,c · Seongsoo Park^†d · Ho-Jeong Ji^a · Ji-Su Woo^a · Juhyun Lee^b,e · Ye-Jin An^a · Yu-Chan Hwang^a · Dong-Ha Kim^a · Hongjun Chang^d · Minseok Kim^b · Mikang Jeong^b · Moonsu Yoon^b · Dongsoo Lee^b · Jongsoon Kim^f,g · Zheng-Long Xu^h · Taeseup Song^c,i · **Janghyuk Moon^\*d** · **Junghyun Choi^\*b** · **Won-Jin Kwak^\*a** (\* 교신 · † 공동 1저자 *"Co-first authors"*)
> **소속 (p.1944 인쇄 그대로)**: a School of Energy and Chemical Engineering, UNIST, Ulsan, 44919, Republic of Korea (wjkwak@unist.ac.kr) · b School of Chemical, Biological and Battery Engineering, Gachon University, Seongnam, 13120, Republic of Korea (junghchoi@gachon.ac.kr) · c Department of Energy Engineering, Hanyang University, Seoul 04763, Republic of Korea · d Department of Energy Systems Engineering, Chung-Ang University, Seoul, 06974, Republic of Korea (jhmoon84@cau.ac.kr) · e Department of Materials Science and Engineering, Pusan National University, Busan 46241, Republic of Korea · f Department of Energy Science, Sungkyunkwan University (SKKU), Suwon 16419, Republic of Korea · g SKKU Institute of Energy Science and Technology (SIEST), Sungkyunkwan University, Suwon 16419, Republic of Korea · h Department of Industrial and Systems Engineering, The Hong Kong Polytechnic University, Hung Hom, Hong Kong SAR, China · i Department of Battery Engineering, Hanyang University, Seoul, 04763, Republic of Korea (SI p.1 은 b 의 나라 이름을 *"Repubilc of Korea"* 로 오식)
> **교신 전자우편 (SI p.1)**: jhmoon84@cau.ac.kr (J.M.) · junghchoi@gachon.ac.kr (J.C.) · wjkwak@unist.ac.kr (W.-J.K.)
> **팔로우 랩 표지 근거**: 인쇄 로마자 **"Junghyun Choi"** — 소속 b (가천대 화공 · 생명 · 배터리공학부) · **교신저자 셋 중 하나** (p.1944 · SI p.1) · 표지 홍보면 (PDF p.1) 에 *"Showcasing collaborative research from the laboratories of Prof. Won-Jin Kwak (Ulsan National Institute of Science and Technology, Republic of Korea), Prof. Junghyun Choi (Gachon University, Republic of Korea), and Prof. Janghyuk Moon (Chung-Ang University, Republic of Korea)."* 로 세 연구실 중 하나로 인쇄 · 특허 출원 발명자 (p.1951).  ⚠ 한글 이름은 PDF 어디에도 인쇄되지 않았다 — "Junghyun" 은 흔히 "정현" 의 로마자이므로 1저자가 말한 "최준현" 과 같은 분인지 [미확인] (같은 가천대 · 건식 전극 교신이라는 점은 PDF 로 확인됨).  주도 연구실은 UNIST 곽원진 (Won-Jin Kwak — 1저자 Hyun-Wook Lee 소속 · 연구비 첫 줄 · 표지 그림 저작권자) 으로 보인다 [추정].  같은 소속 b 의 Dongsoo Lee 는 여기서는 교신이 아니다 (형제 카드 둘에서는 공동 교신).
> *Energy & Environmental Science* **19** (2026) 1944–1953 (10 쪽, PAPER) · *"Cite this: Energy Environ. Sci., 2026, 19, 1944"* · 접수 2025-09-27 · 승인 2026-01-14 · 게재 2026-01-21 · *"Licensed under CC-BY 4.0"* (p.1944) · 표지 홍보면 = Volume 19 Number 6, 24 March 2026, Pages 1767–2096 (PDF p.1) · 연구비 = W.-J. K.: Technology Innovation Program (20024252, MOTIE) / J. C.: NRF National R&D Program (RS-2024-00408156, MSIT) · UNIST Central Research Facilities (p.1951–1952) · **이해상충 = 특허 출원** *"Kwak, W.-J.; Woo, J.-S.; Choi, J.; Lee, J. 'Method of preparing a dry anode for lithium secondary battery and dry anode for lithium secondary battery' Korean Patent Application No. 10-2024-0058602, Filing Date: 05/22/2024"* (p.1951) · 데이터 = *"included as part of the supplementary information (SI)"* (p.1951) · 참고문헌 44 편 (본문) + 16 편 (SI).
> **같은 축 카드 (링크만)**: [`kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation`](kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation.md) (같은 팔로우 랩 · 건식 PTFE 양극) · [`gandla2026_layered_cathode_degradation_diagnostics_review`](gandla2026_layered_cathode_degradation_diagnostics_review.md) (같은 팔로우 랩 · 이 논문을 ref 128 로 인용) · [`nam2026_primer_layer_dry_electrode_collector`](nam2026_primer_layer_dry_electrode_collector.md) (건식 전극 프라이머 · 전극 수준 계면 저항) · [`jun2026_ppma_econductive_binder_si_lowpressure_assb`](jun2026_ppma_econductive_binder_si_lowpressure_assb.md) (ASSB Si 음극 Li 증착 선리튬화) · [`lee2026_unveiling_ptfe_dry_electrode_digital_twin`](lee2026_unveiling_ptfe_dry_electrode_digital_twin.md) · [`hippauf2019_dry_film_ptfe_sulfide_cathode_sheet`](hippauf2019_dry_film_ptfe_sulfide_cathode_sheet.md) · [`zhang2026_xct_dem_cathode_calendering_peel_calibration`](zhang2026_xct_dem_cathode_calendering_peel_calibration.md) (박리 보정 DEM) · [`liao2025_interfacial_adhesion_li_plating_carbon_interlayer`](liao2025_interfacial_adhesion_li_plating_carbon_interlayer.md) (계면 점착 축 I).
> **판독 원자료**: `litdb/figures/lee2026_li_underlayer_primer_free_dry_prelithiated_thick_anode/digitized.csv` (그림 2d · 2f · 3e · 4b–e · 4h–i · 5a–f · SI S2 · S12 · S13 · S18–S20) · 크롭 35 장 `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 건식 PTFE 후막 음극 (Si/C : 흑연 = 9 : 91 활물질 · 활물질 : Super-P : PTFE = 96 : 1 : 3 · 2.1 g cm⁻³) 을 지금까지처럼 SBR 로 미리 처리한 Cu (ThA) 대신 **Li 6.5 µm 가 붙은 Cu 10 µm 박 (MTI Korea BR0182)** 위에 라미네이트한 전극 (PrL-ThA) 은 (i) 박리 · 접힘에서 프라이머 없이도 붙어 있고 (ii) 계면 저항이 절반이며 (iii) Li 가 전해질 없이 고상 확산으로 음극 아래쪽을 미리 리튬화 · PTFE 와 반응해 LiF 가 많은 SEI 를 미리 만든 결과, 반쪽 셀 ICE 가 86.7 → 100.2 %, LFP 전셀 72.1 → 96.6 %, NCM811 전셀 74.8 → 93.3 % 로 오른다 — 그러나 이득의 대부분은 **Li 재고를 미리 채운 오프셋** 이다 (500 사이클 동안의 절대 감쇠는 두 셀이 거의 같다 [판독 · 우리 산술]), Li 공급량은 손실의 1.42 배로 "정밀 보상" 이라 부르기 어렵고, 전기화학 비교는 **프라이머 제거와 Li 추가를 동시에 바꾼 두 점** 이라 둘의 몫이 갈리지 않는다 (§10).

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 공정 변수 (장치 · 속도 · 시간 · 에너지 · 온도 · 압력) | 예비 혼합 = **Thinky ARE-310 유성 혼합기** (rpm · 시간 [미확인]) → **막자 + 막자사발 손 반죽** *"under shear force until a cohesive sheet formed"* (시간 · 온도 [미확인]) → 롤투롤 캘린더로 **≈85 µm** 자립 막 → SBR 처리 Cu 또는 Li/Cu 에 라미네이트 (압력 · 온도 · 롤 간격 [미확인]) · 전극 밀도 **2.1 g cm⁻³** · 에너지 n/a | [인쇄] SI p.2 |
| ② 입자 · 크기 · 조성 | Si/C 복합 (Hansol Chemical) : 인조 흑연 (G49, Shanshan) = **9 : 91** (wt) · 활물질 : Super-P (Imerys) : PTFE (F-106, DAIKIN) = **96 : 1 : 3** · 입경 · Si/C 안의 Si 함량 [미확인] | [인쇄] SI p.2 |
| ③ 접착 · 계면 | 박리 [판독] ThA **≈3.85** · PrL-ThA **≈3.45 gf/mm** (−10 %, 본문 *"Similar"*) · 시험 기하 · 폭 · 속도 [미확인] · MD 접착 에너지 SBR–PTFE **−0.89** · Li–PTFE **−1.39 eV** (면적 정규화 없음) · 계면 저항 [판독] 맨 Cu **0.0084** · ThA **0.046** · PrL-ThA **0.021** (축 표기 "ohm cm⁻²") · 측정 압력 [미확인] | [인쇄] p.1946–1947 · [판독] 그림 2d · 2f |
| ④ 이온 · 전자 수송 | **σ_ion · σ_e · tortuosity 측정 없음** · 공극률 미보고 → [우리 산술 · 가정 골격 밀도 2.21–2.25 g cm⁻³] 음극 공극률 **≈3–7 %** · 반쪽 셀 EIS (Ω, 면적 정규화 없음): 화성 전 R_ct **344.8 → 207.6** · 화성 뒤 R_SEI **77.3 → 27.8** · R_ct **90.5 → 30.8** | [인쇄] 표 S1 · [우리 산술] §3-1 |
| ⑤ 시뮬레이션 | **DEM · MPM 없음.**  FEM = COMSOL 6.2 DFN · Blender 4.3 로 Si · C 입자를 *"sequentially stacking"* 한 **50 µm** 3D 영역 (실제 전극 63–65 µm) · 입자 내부 + **접촉을 통한 입자간 고상 Fick 확산** (식 4) · BV (식 5) — **물성 · 입자 수 · 경계조건 · 모사 시간 전부 [미확인]** · MD = COMPASS 힘장 · 5 단위체 PTFE/SBR 사슬 · NPT 50 ps | [인쇄] SI p.3–5 |
| ⑥ 고상 선리튬화 깊이 | [판독] 전해질 없이 흑연 SOC **1.0 (바닥) → 0.36 (10 µm) → ≈0 (26 µm = 영역의 52 %)** — 본문 *"bottom region of the electrode (~52%)"* 의 뜻으로 추정 · 전해질 있으면 위끝 흑연 SOC **≈0.065** (본문 *"at least 6%"*) | [판독] 그림 3e · [인쇄] p.1947 |
| ⑦ 믹서 논문 V1 · V2 · V3 (메인 `docs/mixer_paper_pipeline_draft_20261013.md`) | **V1 (코팅 상태) · V3 (SE 함량) = n/a** (SE 없음 · 코팅 없음) · **V2 (혼합 시간) = 앵커 불가** — 혼합이 손 반죽이고 시간 · 에너지가 0 건 · 대신 "**한 공정이 두 처치를 함께 바꾼다**" (프라이머 제거 + Li 추가) 는 V1 설계의 교락 경고 사례 (§7-6) | [인쇄] SI p.2 · [추정] |

⛔ **한정어 (떼지 말 것)**: ① **액체 전해질 LIB** (1.15 M LiPF₆ EC/EMC/DEC 2/4/4 + VC 1 wt% + FEC 10 wt%; 전셀은 + LiPO₂F₂ 1 wt%) — 황화물 SE 없음 · ② **음극** 논문 (우리 ASSB 양극 축과 다른 전극) · ③ 한 조성 · 한 밀도 · **한 Li 두께 (6.5 µm, 상용 박 하나)** · ④ 셀 반복 수 · 오차 막대 · 대표 셀 선정 기준 [미확인] (그림 사이에 다른 셀로 보이는 흔적 — §10-1) · ⑤ FEM 은 물성값이 하나도 안 적힌 정성 모사 · ⑥ "에너지 밀도 476.7 Wh kg⁻¹" 은 **전극 수준** (집전체 · Li/Cu 박 · 분리막 · 전해질 질량 제외, Note S2).

---

## 1. 한 줄 요약

건식 공정은 용매 증발 없이 후막을 만드는 길이지만, 건식 후막 음극 (ThA) 에는 세 문제가 있다고 저자는 세운다 — (i) 막을 집전체에 붙이려면 **습식으로 바른 프라이머** 가 필요하고 그것이 전기 저항을 키우며, (ii) PTFE 가 PVDF 보다 높은 전위에서 환원 분해돼 초기 쿨롱 효율 (ICE) 을 깎고, (iii) 두꺼운 전극은 이온 이동이 제한돼 표면 쪽만 반응해 SEI 가 고르지 않다 (p.1945).  기존 선리튬화 (전기화학 · Li-arene 용액 · Li 금속 직접 접촉 · 용융 Li) 는 롤투롤 · 건식 · 정밀 제어를 동시에 못 맞춘다고 비교한 뒤 (그림 1a), **Li 가 입혀진 Cu 박 (Li/Cu)** 위에 건식 막을 바로 라미네이트하는 "한 단계" 공정을 제안한다 (그림 1b).  Li 층은 프라이머처럼 막을 붙잡고 (그림 2c–d), 프라이머보다 저항이 낮으며 (그림 2f), 전해질이 없어도 고상 확산으로 활물질을 리튬화하고 PTFE 와 반응해 LiF 가 많은 무기 SEI 를 뒷면까지 만든다 (그림 3 · SI S6–S9).  FEM 은 전해질 없이 아래 절반이 리튬화되고 전해질이 들어오면 전극 위끝까지 리튬화가 번진다고 보인다 (그림 3d–e · S10).  반쪽 셀에서 첫 사이클 비가역 손실 68.9 mAh g⁻¹ 이 사라지고 (ICE 100.2 %), 계면 저항 (R_ct · R_SEI) 이 1/1.7–1/3 로 줄며 (그림 4c–d · 표 S1), XPS 는 PrL-ThA SEI 의 F 몫이 더 크다고 본다 (그림 4f–i · S13).  LFP · NCM811 전셀에서 ICE · 첫 용량 · 에너지 밀도 · 율속이 모두 높고 (그림 5a–f), DRT 의 SEI 구간 저항이 작고 고르며 (그림 5g–h), 사이클 뒤 NCM811 표면의 암염상 전이도 적다고 해석한다 (그림 5i–j).

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 (활물질 / 도전재 / 바인더 / 전해질) | 연구유형 |
|---|---|---|---|---|
| H.-W. Lee† · W. Jeong† · S. Park† · H.-J. Ji · J.-S. Woo · J. Lee · Y.-J. An · Y.-C. Hwang · D.-H. Kim · H. Chang · M. Kim · M. Jeong · M. Yoon · D. Lee · J. Kim · Z.-L. Xu · T. Song · J. Moon\* · J. Choi\* · W.-J. Kwak\* (UNIST · 가천대 · 한양대 · 중앙대 · 부산대 · 성균관대 · 홍콩이공대) | *Energy Environ. Sci.* 19 (2026) 1944–1953 | 10.1039/d5ee05739f | 음극 Si/C (Hansol) + 인조 흑연 G49 (Shanshan) / Super-P / PTFE F-106 (DAIKIN) / 액체 LiPF₆ — 양극 NCM811 (90 : 5 : 5) · LFP (94.5 : 2.5 : 3) | 실험 (건식 전극 공정 · 계면 · 전기화학) + FEM (DFN) · MD (보조 해석) |

- 저자 기여 (p.1951, 인쇄 그대로 요약): H.-W. L. · W. J. · S. P. = 착상 · 실험 · 시각화 · 초고 · 검토 / H.-J. J. · J.-S. W. · Y.-J. A. = 실험 · 검토 / **S. P. · H. C. = 계산 모사** / J. L. · M. K. · M. J. · M. Y. · D. L. · J. K. · Z.-L. X. · T. S. = 분석 · 검토 / **J. M. · J. C. · W.-J. K. = 착상 · 연구비 · 검토 · 편집**.  ⚠ 저자 20 명 중 **Y.-C. Hwang · D.-H. Kim 두 사람은 기여 목록에 없다** [인쇄 대조].
- 계산 담당 = 중앙대 (Moon 연구실, 소속 d — S. Park · H. Chang) [인쇄 p.1951 · 소속 대조].
- 가천대 (소속 b) 저자 = W. Jeong · J. Lee · M. Kim · M. Jeong · M. Yoon · D. Lee · J. Choi (7 명) [인쇄 p.1944].

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 재료 · 공정 · 전극 · 셀 (SI p.2–3 · 표 S2)

| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 활물질 | Si/C 복합 (Hansol Chemical) + 인조 흑연 (G49, Shanshan) = **9 : 91** (wt) · Si/C 안의 Si 함량 · 입경 · 비표면적 [미확인] · 본문 · SI 가 "SiC composite" 라고도 쓰는데 탄화규소가 아니라 Si/C 를 뜻한다 [추정] | [인쇄] SI p.2 · p.4 |
| 도전재 · 바인더 | Super-P (Imerys) · PTFE (F-106, DAIKIN) | [인쇄] SI p.2 |
| 조성 | *"The Si/C composite, carbon black, and PTFE were premixed at a **96:1:3** weight ratio"* — 문장 그대로는 "Si/C" 이지만 바로 앞 문장의 Si/C + 흑연 혼합물을 뜻하는 것으로 읽힌다 [추정] | [인쇄] SI p.2 |
| 예비 혼합 | 유성 혼합기 **ARE-310 (THINKY)** *"to ensure uniform dispersion"* — rpm · 시간 · 배치 질량 [미확인] | [인쇄] SI p.2 |
| 섬유화 · 막 | *"manually kneaded with a mortar and pestle under shear force until a cohesive sheet formed"* → *"rolled to a target thickness of **~85 μm** using a roll-to-roll calendar"* → 자립 막 — 반죽 시간 · 온도 · 롤 간격 · 압력 · 통과 횟수 [미확인] | [인쇄] SI p.2 |
| 라미네이트 | ThA = *"SBR-pretreated copper current collectors"* (SBR 층 두께 · 조성 · 도포법 [미확인]; 단면 SEM 에서 안 보일 만큼 얇다, p.1946) · PrL-ThA = **Li/Cu 박 (Li 6.5 µm on Cu 10 µm, MTI Korea, BR0182)** · 라미네이트 압력 · 온도 [미확인] | [인쇄] SI p.2 · p.1946 |
| 전극 밀도 · 면적 | **2.1 g cm⁻³** (두 전극 같게 맞춤) · 전극 면적 **1.13 cm²** (= 지름 12 mm 원판 [우리 산술]) · 접힘 시험은 *"16 pi disks"* | [인쇄] SI p.2 · p.1946 |
| 음극 로딩 · 두께 (표 S2) | 활물질 로딩 **13.13 / 12.94 / 13.11 / 13.13** mg cm⁻² · 전체 로딩 **13.57 / 13.47 / 13.65 / 13.57** mg cm⁻² · 두께 **65 / 63 / 65 / 63 µm** (ThA‖LFP · PrL-ThA‖LFP · ThA‖NCM · PrL-ThA‖NCM) · 비용량 **428.27 mAh g⁻¹** | [인쇄] 표 S2 |
| [우리 산술] 밀도 · 공극률 | 13.57 / 65 µm = **2.09** · 13.47 / 63 = **2.14** · 13.65 / 65 = **2.10** · 13.57 / 63 = **2.15 g cm⁻³** (본문 2.1 과 맞음) · 골격 밀도를 흑연 2.26 · Si/C 1.8–2.2 · CB 1.9 · PTFE 2.2 로 가정하면 2.21–2.25 g cm⁻³ → **공극률 ≈3–7 %** — 액체 전해질 음극으로는 아주 치밀하다 · ⚠ SI 의 "≈85 µm" 막이 63–65 µm 로 줄어든 과정 (라미네이트 압밀) 은 서술 없음 | [우리 산술 · 가정 밀도] |
| [우리 산술] 면적 용량 · N/P | 음극 13.13 × 428.27 = **5.62 mAh cm⁻²** · NCM811 26.32 × 191.82 = **5.05** · LFP 30.84 × 163 = **5.03** → N/P **1.11–1.13** (인쇄 1.1 과 맞음) | [우리 산술] 표 S2 |
| 양극 | NCM811 : CB : binder = **90 : 5 : 5** · LFP : CB : binder = **94.5 : 2.5 : 3** · 활물질 로딩 26.3 / 26.32 (NCM) · 30.59 / 30.84 (LFP) mg cm⁻² · 전체 29.22 / 29.24 · 32.37 / 32.63 mg cm⁻² · 두께 **82 µm (NCM) · 131 µm (LFP)** (S16) · 비용량 191.82 · 163 mAh g⁻¹ · **양극 제조법 (습식/건식) · 바인더 종류 · 집전체 [미확인]** · [우리 산술 · 가정 밀도] 양극 밀도 3.56 · 2.47 g cm⁻³ → 공극률 ≈13 % (NCM) · ≈28 % (LFP) | [인쇄] SI p.2 · 표 S2 · S16 |
| 셀 | CR2032 (Wellcos) · 이슬점 **−80 °C 아래 드라이룸** · PE 분리막 19 mm · 반쪽 셀 상대극 Li 박 *"thickness 1.0 T"* (T = mm 로 읽힘 [추정]) · 전셀 음극 14 mm · 양극 12 mm · N/P **1.1** (용량 기준) | [인쇄] SI p.2 |
| 전해질 | 반쪽 셀 = **1.15 M LiPF₆ in EC/EMC/DEC (2:4:4, vol) + VC 1 wt% + FEC 10 wt%** (Enchem) · 전셀 = 같은 것 + **LiPO₂F₂ 1 wt%** | [인쇄] SI p.2 |
| 시험 조건 | 반쪽 셀: CC-CV, 화성 0.1 · 0.2 C 두 번 → 0.3 C · **0.01–1.5 V** (NEWARE MIHW-200-160CH-B) · CV 0.1 mV s⁻¹ (그림 4a 캡션은 **1.0–0.01 V**, SI 는 *"in the same voltage window"* = 0.01–1.5 V) · EIS **250 kHz–10 mHz, 5 mV** (VSP, Biologic) / 전셀: 화성 **0.05 · 0.1 C** → **0.2 C** · NCM **2.8–4.25 V** · LFP **2.5–4.0 V** · DRT = MATLAB 도구 (이름 [미확인]) · 상온 | [인쇄] SI p.2–3 · 그림 4 캡션 |
| 분석 장비 | FE-SEM SU8220 (Hitachi) · UTM Autograph AGS-X (SHIMADZU) · XRD D8 ADVANCE (2θ 10–90°, 50 min) · FIB SCIOS (FEI) → 수차 보정 TEM (모델 [미확인]) · TOF-SIMS 5 (ION TOF, Bi₃⁺ 25 keV) · 깊이 XPS K-alpha (*"with a 2 keV Al Kα X-ray source"* — Al Kα 광자는 1.49 keV 라 2 keV 는 식각 이온 에너지로 보인다 [추정]) · 식각 속도 [미확인] | [인쇄] SI p.3 |

### 3-2. ★ 접착 · 계면 저항 (그림 2 · SI S1–S2 · p.1946–1947)

- **층 구조**: ThA = Cu · 프라이머 · Si/G 세 층이지만 프라이머는 얇아 단면 SEM 에서 안 보인다 (S1, 표지 "~65 µm") · PrL-ThA = Cu · **Li (~6.5 µm)** · Si/G (그림 2a 사진 표지 "~63 µm" · 2b 단면) — *"the thickness of the composite layer in both electrodes is similar"* [인쇄 p.1946].  Li 두께는 *"precisely optimized to compensate for the first-cycle irreversible capacity loss … avoiding excess Li plating or dead Li formation, as detailed in Note S1"* [인쇄 p.1946] — 실제 값은 §3-6 (공급/손실 = 1.42).
- **접힘 시험** (그림 2c, 16 mm 원판 1 · 2 회): 두 전극 모두 막이 떨어지지 않음 (정성) [인쇄 p.1946].
- **박리 (그림 2d, 행정 10–50 mm)**: [판독] ThA 평균 **3.85 gf/mm** (3.65–4.06) · PrL-ThA **3.45 gf/mm** (3.01–3.80) = −10 % · [우리 산술] 0.0377 · 0.0339 N/mm.  본문: *"Similar values were recorded for both electrodes, confirming that Li provides comparable adhesive strength"* [인쇄 p.1947].  박리 각도 (90°/180°) · 시편 폭 · 속도 · 시편 수 [미확인] (SI p.3 은 장비 이름뿐).
- **흡착 에너지 (S2)**: Si · 흑연 · Cu 에 대한 Li 흡착이 모두 음수 = *"thermodynamic stability upon interaction with Li"* [인쇄 p.1947] · [판독] Li–Si **≈−0.11** · Li–Cu **≈−3.00** · Li–흑연 **≈−1.52 eV** · 계산법 (DFT? MD?) · 원자당/계당 정규화 [미확인].
- **접착 에너지 (그림 2e, MD)**: SBR–PTFE **−0.89 eV** · Li–PTFE **−1.39 eV** — *"The significantly lower adhesion energy of the Li–PTFE pair (−1.39 eV) indicates enhanced interfacial stability"* [인쇄 p.1947].  정의 E_adhesion = E_total − E_substrate − E_adsorbate (substrate = PTFE, adsorbate = SBR 또는 Li) [인쇄 SI p.4] · 접촉 면적 · 계 크기로 나눈 값이 아니다 → J m⁻² (W_ad) 로 옮길 수 없다 [우리 판단].
- **계면 저항 (그림 2f)**: *"measured under the same pressure, allowing the composite to contact the current collector without a primer"* (캡션) · [판독] **맨 Cu 0.0084 · ThA 0.046 · PrL-ThA 0.021** (축 이름 *"Resistance_interface (ohm cm⁻²)"* — 단위 표기는 Ω cm² 의 오기로 보임) · ThA/PrL = **2.14** (본문 *"more than twice lower"*) · PrL/맨 Cu = 2.6 → **Li 층은 맨 Cu 보다는 저항을 더한다** [판독 · 우리 산술] · 측정 압력 값 · 방법 (직류 2 단자? 4 단자? EIS?) · 시편 수 [미확인].

### 3-3. ★ SEI 균일성 · 고상 선리튬화 (그림 3 · SI S3–S10 · p.1947–1948)

- **전해질 없는 pristine ThA**: 앞 · 뒷면 모두 SiC⁻ 신호만 (TOF-SIMS S3) · XPS C–F₂ (PTFE) · C–C · C–O–C, LiF 없음 (S4) [인쇄 p.1947].
- **ThA 를 전해질에 24 h 담금**: 앞면 = SiC⁻ 위로 LiF₂⁻ · P⁻ (그림 3a 왼쪽) · XPS LiF (S5) / 뒷면 = 반응 산물 적음 (그림 3b 왼쪽 · S5 뒷면 C–F₂ 가 주) ⇒ *"mere electrolyte contact is insufficient to lithiate the entire thick electrode"* [인쇄 p.1947].
- **전해질 없는 pristine PrL-ThA**: XRD 흑연 피크가 낮은 각으로 이동 = 부분 리튬화 흑연 (S6) · 뒷면 TOF-SIMS 에서 LiSi⁻ 가 SiC⁻ 보다 큼 · LiF₂⁻ 높음 (S7) · XPS 뒷면 **685.4 eV LiF** (S8) ⇒ Li 가 전위를 낮춰 리튬화하고 PTFE 와 반응해 무기 SEI [인쇄 p.1947].
  - ⚠ S6 은 23–29° 만 보여 준다 (측정은 10–90°) — 잔류 금속 Li 가 남았는지 판단할 Li (110) 근처는 없다 [판독 · 추정].
- **PrL-ThA 를 전해질에 24 h**: 앞면 P · LiF₂⁻ 는 ThA 와 비슷 (그림 3a 오른쪽) · 뒷면 무기 SEI 가 잘 발달 (그림 3b 오른쪽) · XPS 앞 · 뒷면 모두 유기 탄산염 · Li₂CO₃ · LiF (**287 · 531.8 · 685.3 eV**, S9) [인쇄 p.1947] — S9 그림 표지는 531.8 근처를 "C=O" · "C-O" 로 적는다 (Li₂CO₃ 표지 없음) [판독].
- **해석** (그림 3c 개념도): 프라이머 전극은 표면만 반응 → 고르지 않은 SEI + 추가 Li 소모 / Li 밑층은 바닥에서 리튬화 → 순환 전에 전극 전체를 고르게 활성화 [인쇄 p.1947].
  - ⚠ TOF-SIMS 는 스퍼터 **0–300 s** (식각 속도 [미확인]) 로 **앞면 · 뒷면 표면 근처** 만 본다 — 63 µm 두께 방향의 분포를 잰 것이 아니다.  *"across the entire electrode depth"* 는 두 표면 + FEM 으로 이은 추론 [추정].
- **FEM (그림 3d–e · S10)**: 세 경우 — ThA + 전해질 · PrL-ThA (전해질 없음) · PrL-ThA + 전해질 [인쇄 p.1947].
  - ThA + 전해질 = 리튬화 없음 (Li 원천 없음) → ThA 위쪽 LiF 는 전해질과의 화학 반응만으로 생긴 것 [인쇄 p.1947].
  - PrL-ThA (전해질 없음): 고상 확산으로 바닥부터 리튬화 · [판독] 흑연 평균 SOC **0.99 (0 µm) · 0.87 (2) · 0.68 (5) · 0.36 (10) · 0.16 (15) · 0.025 (20) · ≈0 (26 µm)** · Si **0.10 (2 µm) → 0.04 (10) → ≈0.005 (20)** — 리튬화 영역 26/50 µm = **52 %** [우리 산술] ↔ 본문 *"facilitated LiF formation in the bottom region of the electrode (~52%)"* [인쇄 p.1947] (그 52 % 가 무엇의 몫인지 본문 정의 없음 — 높이 몫으로 읽힘 [추정]).
  - PrL-ThA + 전해질: Li⁺ 가 전해질을 통해 전 두께를 리튬화 · [판독] 흑연 **0.205 (2 µm) → 0.146 (10) → 0.101 (20) → 0.076 (30) → 0.064 (45 µm)** = 본문 *"SOC of at least 6%"* · Si **≈0.34 (8 µm) → 0.22 (15) → 0.17 (26) → 0.10 (33)** [판독 · 인쇄 p.1947].
  - S10: 평형 전위 위 **0.30 V** · 아래 **0.13 V** / 전해질 전위 위 **−0.27 V** · 아래 **−0.035 V** → *"provided sufficient overpotential … lithiation up to the electrode surface"* · 이 SOC 의 흑연 OCV **~0.3 V** < LiF 생성 전위 **0.4–0.6 V** → LiF 가 전극 표면 전체에서 생길 것 [인쇄 p.1947–1948].  [우리 산술, φ_s ≈ 0 (Cu 를 통해 Li 에 단락) 가정] η = φ_s − φ_l − U ≈ 0 + 0.27 − 0.30 = **−0.03 V (위)** · 0 + 0.035 − 0.13 = **−0.095 V (아래)** — 구동력은 아래가 더 크다 (SOC 가 위로 줄어드는 방향과 맞음).
  - ⚠ 물성 (D_s · D_l · σ_s · σ_l · i₀ · α · OCV 곡선) · 입자 수 · 크기 · Si : C 비 · Li 경계조건 · **모사 시간** · 메시 [전부 미확인] — 그림은 정성 지도로만 쓴다.

### 3-4. 반쪽 셀 전기화학 (그림 4 · SI S11–S15 · 표 S1 · p.1948–1950)

- **CV (그림 4a)**: ThA 첫 사이클 **≈0.7 V** 의 뚜렷한 환원 신호 (SEI) · PrL-ThA 는 같은 구간이 훨씬 약함 ⇒ SEI 가 전기화학적 분해가 아니라 Li 금속층이 시작한 화학 반응으로 생겼다는 해석 [인쇄 p.1948].
- **첫 사이클 (그림 4b, 1.5–0.01 V, 0.1 C)**: ThA **ICE 86.7 %** · *"Large Li loss 68.9 mAh g⁻¹"* (그림) = *"excess discharge capacity of 68.9 mAh g⁻¹ relative to its charge capacity, attributable to electrochemical decomposition of both the electrolyte and PTFE binder"* / PrL-ThA **ICE 100.2 %** · *"No Li loss"* [인쇄 p.1948 · 그림].  [판독] ThA 리튬화 **≈521** · 탈리튬화 **≈451** mAh g⁻¹ · 2nd 탈리튬화 **≈430** (= 표 S2 의 428.27 로 보임) / PrL-ThA 리튬화 **≈439** · 탈리튬화 **≈439** · 2nd **≈432**.
  - [우리 산술] PrL-ThA 첫 탈리튬화 (≈439) ≈ 첫 리튬화 (≈439) ⇒ Li 밑층이 미리 넣은 **가역 Li 는 ≈0** — 공급 1.34 mAh cm⁻² (≈102 mAh g⁻¹ 활물질) 중 손실 몫 (0.943 ≈ 72 mAh g⁻¹) 을 넘는 ≈0.40 mAh cm⁻² (≈30 mAh g⁻¹) 가 가역 용량으로 나타나지 않는다 → 추가 SEI · PTFE 탈불소에 쓰였거나 금속 Li 로 남아 비활성 [추정 — 논문은 정산하지 않음].
- **EIS (그림 4c–d · S11–S12 · 표 S1, Ω)**: 등가 회로 = 화성 전 R_s − [R_ct−W ∥ CPE] · 화성 뒤 R_s − [R_SEI ∥ CPE] − [R_ct−W ∥ CPE] (S11).

| | 화성 전 R_s | R_ct | R_total | 화성 뒤 R_s | R_SEI | R_ct | R_total |
|---|---|---|---|---|---|---|---|
| ThA | 1.5 | 344.8 | 346.3 | 2.2 | 77.3 | 90.5 | **202.1** |
| PrL-ThA | 1.5 | 207.6 | 209.1 | 1.6 | 27.8 | 30.8 | 60.2 |

  [인쇄 표 S1] — 본문: 화성 전 R_ct *"~40% lower"* ([우리 산술] −39.8 % ✓) · 화성 뒤 R_ct · R_SEI *"nearly three times lower"* (×2.94 · ×2.78 ✓) [인쇄 p.1949].  🔴 ThA 화성 뒤 **2.2 + 77.3 + 90.5 = 170.0 ≠ 202.1** (다른 세 행은 합이 맞음) [우리 산술] · 그림 4d 의 ThA 호는 **≈110 Ω** 에서 확산 꼬리로 넘어간다 [판독] (PrL-ThA 는 ≈45 Ω ↔ 표 60.2) · S12 막대 [판독] ThA 77.3 · 90.3 (표와 같음) · PrL-ThA **29.5 · 32.1** (표 27.8 · 30.8 보다 1.3–1.7 Ω 높게 그려짐).
- **50 사이클 (그림 4e)**: *"comparable discharge capacities over 50 cycles, likely owing to the continuous Li supply from the Li metal counter electrode"* [인쇄 p.1949] · [판독] 50 사이클 PrL-ThA **≈372** · ThA **≈334 mAh g⁻¹** (표지 겹침으로 ThA ±10) — 차이 ≈10 %.
- **XPS 깊이 (화성 뒤, 그림 4f–i · S13–S14)**:
  - 앞면: 두 전극 모두 LiF 가 주 · ThA F **33 %** (탄소 많은 SEI) · PrL-ThA F **60 %** (LiF 많은 무기 SEI) [인쇄 p.1949] · [판독 S13] t=0 F 33.5 · 62.2 % (최대 69.7 % @100 s).
  - 뒷면: LiF 가 주 (본문) · PrL-ThA 에서만 O 가 식각 깊이에 따라 증가 (그림 4i) · S14 CH₃O⁻ 가 PrL-ThA 뒷면에 고르게 → 혼합 유기–무기 SEI [인쇄 p.1949].  [판독] ThA 뒷면 C/O/F **45.5/21.3/30.5 (0 s) → 70.8/12.0/15.2 (1000 s)** · PrL-ThA **≈32/31.3/34.3 → 17.9/55.7/25.0**.
  - *"the atomic ratio of fluorine to oxygen on the back of PrL-ThA was ~1:1, compared with 3:2 in ThA (Fig. 4h and i), confirming a higher contribution of F-rich inorganic components"* [인쇄 p.1949] — 🔴 F:O 는 오히려 **ThA 가 높다** (1.43 vs 1.10 [판독]) · PrL 이 더 "F 가 많은" 것은 C 대비 F (깊이 1000 s 에서 F 25 vs 15 %) 로 읽어야 맞다 [우리 판단].
- **Si 입자 (S15, 0.3 C 20 사이클 뒤 단면)**: ThA 위쪽 Si 가 아래쪽보다 심하게 균열 (위에 반응 집중, refs 39–41) · PrL-ThA 는 위 · 아래 모두 덜 손상 → F 풍부 SEI 가 열화를 막는다 (refs 42–44) [인쇄 p.1950] — 정성 · 입자 수 · 통계 없음.

### 3-5. 전셀 (그림 5 · SI S16–S22 · 표 S2–S3 · p.1950–1951)

| 지표 | ThA | PrL-ThA | 표지 · 쪽 |
|---|---|---|---|
| LFP 첫 방전 · ICE | **3.46 mAh cm⁻² · 72.1 %** | **5.1 mAh cm⁻² · 96.6 %** | [인쇄] p.1950 · 그림 5a |
| LFP 개선 | — | **+1.64 mAh cm⁻² · +24.5 (%p)** | [인쇄] 그림 5a |
| LFP 197 사이클 유지 | **68.2 %** | **74.1 %** | [인쇄] p.1950–1951 (기준 사이클 [미확인]) |
| NCM811 첫 방전 · ICE | **≈4.50** ([우리 산술] 5.63 − 1.13) · **74.8 %** (그림) | **5.63 mAh cm⁻² · 93.3 %** | [인쇄] p.1951 · 그림 5c |
| NCM811 개선 | — | **+1.13 mAh cm⁻² · "20%"** | [인쇄] p.1951 (🔴 §10-2) |
| NCM811 500 사이클 | [판독] ≈4.55 → ≈2.74 | [판독] ≈5.67 → ≈3.83 mAh cm⁻² | 유지율 인쇄 없음 |
| 첫 사이클 에너지 밀도 (전극 수준) | LFP **246.0** · NCM **380.2 Wh kg⁻¹** | LFP **342.4** · NCM **476.7 Wh kg⁻¹** | [인쇄] 그림 5e |
| 에너지 밀도 개선 | — | NCM **+25.4 %** · LFP **+39.2 %** | [인쇄] p.1951 |
| 율속 0.5 → 5 mA cm⁻² (NCM) | [판독] ≈4.45 → ≈4.01 | [판독] ≈5.39 → ≈4.96 mAh cm⁻² | 그림 5f |

- 전극 물성은 같게 맞췄으므로 첫 방전 차이는 *"due solely to the prelithiation"* (표 S2 · S16) [인쇄 p.1950] — 🔴 단 ThA 는 SBR 프라이머가 있고 PrL-ThA 는 없다 → **프라이머 제거 (저항 ↓) 와 Li 추가 (재고 ↑) 가 함께 바뀐 비교** [우리 판단].
- *"The improvement shown by prelithiation is similar to or even higher than the theoretically calculated value (Fig. S17 and S18), owing to the synergistic effect of the structural stability of the active materials"* [인쇄 p.1951] — S17 계산: ThA 이상 ICE **85.4 %** = 100 − 110 × (100 − 86.7) (N/P 1.1 · 음극 ICE 86.7 %) ↔ 측정 72.1 (LFP) · 74.8 % (NCM) / PrL-ThA 계산 ≈99 (LFP, = LFP 반쪽 셀 ICE 99.4 %) · ≈89 % (NCM, = NCM811 반쪽 셀 ICE 88.8 %) ↔ 측정 96.6 · **93.3 %** [인쇄 S17 · S18].
  - [우리 산술] ThA 는 측정이 계산보다 **10.6–13.3 %p 낮고** (설명 없음), PrL-ThA‖NCM 은 측정이 계산 (양극 자체 한계) 보다 **4.3–4.5 %p 높다** — 양극 반쪽 셀의 측정 조건 (C-rate · 2.5–4.2 V) 과 전셀 (0.05 C · 2.8–4.25 V) 이 달라 "시너지" 없이도 생길 수 있는 차이 [추정].
- **유지 · 에너지 밀도 궤적** (S19 · S20): [판독] LFP PrL-ThA ≈342 → ≈236 · ThA ≈246 → ≈161 Wh kg⁻¹ (200 사이클) · NCM PrL-ThA ≈477 → ≈324 · ThA ≈380 → ≈231 Wh kg⁻¹ (500 사이클) — 🔴 S20 캡션은 "LFP" 인데 그림 범례는 "NCM full-cell".
  - ★ [우리 산술 · 판독] NCM 사이클 10 → 500 절대 감소 = PrL-ThA **1.40** · ThA **1.44 mAh cm⁻²** · 에너지 밀도 절대 감소 ≈153 · ≈149 Wh kg⁻¹ — **감쇠 기울기는 거의 같고 이득은 출발점 차이 (Li 재고)** 다.  본문의 *"highly stable cycle performance for up to 500 cycles"* (p.1945) 를 감쇠율 개선으로 읽으면 안 된다.  LFP 는 PrL-ThA 가 절대값으로 더 많이 잃는다 (사이클 10 → 197: 1.10 vs 0.78 mAh cm⁻²) [판독].
- **율속 (그림 5f)**: 0.5 · 1.0 · 1.5 · 2.5 · 5.0 mA cm⁻² × 3 사이클 — [우리 산술] 5 mA cm⁻² ≈ **0.9 C** (5.4 mAh cm⁻² 기준) → "고율" 은 ≈1 C 까지 · 0.5 → 5 mA cm⁻² 용량 유지 PrL-ThA **92 %** · ThA **90 %** [판독 · 우리 산술] — 차이의 대부분은 여기서도 오프셋.
- **SOC 별 XPS (S21)**: ThA 뒷면은 첫 충전 중 C–F₂ → LiF + LixPFyOz + LixPFy (*"severe incomplete decomposition of electrolyte"*) · PrL-ThA 는 처음부터 LiF 하나 [인쇄 p.1951 · 판독].
- **제자리 EIS + DRT (그림 5g–h · S22, 2.8 → 4.25 V, ΔV = 0.21 V)**: ThA 는 양 · 음극 R_SEI 를 포함한 계면 저항이 충전 중 크게 흔들림 · PrL-ThA 는 낮고 안정 [인쇄 p.1951] — 그림의 "large R_SEI" · "small R_SEI" 구간 = τ ≈ **10⁻³–3×10⁻² s** (분홍 · 초록 띠) [판독] · 전셀에서 그 τ 구간이 음극 SEI 라는 배정은 저자 해석 (3 전극 측정 · 대칭셀 없음).
- **TEM · FFT (그림 5i–j)**: 사이클 뒤 NCM811 — ThA 짝은 표면 거칠어짐 · 부분 암염상 · 흐트러진 FFT / PrL-ThA 짝은 층상 구조 유지 *"indicating that PrL-ThA protects the anode and suppresses cathode degradation"* [인쇄 p.1951] — 사이클 수 · 관찰 입자 수 [미확인].
- **문헌 비교 (그림 5k · 표 S3)**: This work Si/G‖NCM811 *"Roll-to-Roll"* ICE **93.3 %** · 양극 26.3 · 음극 13.13 mg cm⁻² · **500** 사이클 · **5.63 mAh cm⁻²** vs S9–S16 (ICE 73–89.21 % · 면적 용량 0.24–3.6 mAh cm⁻²) [인쇄 표 S3] — 비교군 대부분은 Si 함량이 높은 음극 (µ-Si · Si@SiO₂ · Si) · 이 논문 음극은 Si/C 가 활물질의 9 wt% (428 mAh g⁻¹ = 흑연 우세) → ICE 비교가 같은 조건이 아니다 [우리 판단] · S16 은 같은 그룹 논문 (D. Lee, W. Jeong … J. Choi, *Int. J. Ener. Res.* 2025).

### 3-6. ★ Li 재고 · 에너지 밀도 산술 (Note S1–S2 · S17–S18)

| 양 | 값 | 표지 |
|---|---|---|
| 음극 첫 사이클 비가역 손실 | **68.9 mAh g⁻¹ × 13.7 mg cm⁻² = 0.943 mAh cm⁻²** (13.7 은 표 S2 어느 칸과도 같지 않다 — 가장 가까운 전체 로딩 13.65) | [인쇄] Note S1 · [우리 산술] 0.944 ✓ |
| Li 공급 | **Q_Li = ρ_Li × h × C_th = 0.534 g cm⁻³ × 6.5 µm × 3860 mAh g⁻¹ = 1.34 mAh cm⁻²** | [인쇄] Note S1 · [우리 산술] 1.340 ✓ |
| 공급 / 손실 | **1.42** (초과 ≈0.40 mAh cm⁻² = 음극 가역 용량 5.62 의 ≈7 %) — 저자: *"sufficient to fully compensate the irreversible capacity loss while minimizing the risks associated with excessive prelithiation"* | [우리 산술] · [인쇄] Note S1 |
| Li 공급 전부가 흑연에 들어간다면 | 1.34 / 5.62 = **24 % SOC** 에 해당 (`jun2026_ppma_econductive_binder_si_lowpressure_assb` 의 ASSB Si 증착 Li 4.0 µm ≈23 % SOC 와 같은 크기) | [우리 산술] |
| NCM 전셀 첫 충전 | [판독] ThA **≈6.16** · PrL-ThA **≈6.06 mAh cm⁻²** = **≈234 · ≈230 mAh g⁻¹_NCM** (설계값 191.82 의 1.2 배 — 셀 4.25 V ≈ 양극 4.3 V 대 vs Li) | [판독] 그림 5c · [우리 산술] |
| 실제 첫 충전 기준 N/P | 음극 설계 가역 용량 5.62 ÷ 첫 충전 6.06 = **≈0.93** (< 1) — 그 위에 밑층의 초과 Li ≈0.40 이 더해지면 충전 끝에서 음극이 설계 용량보다 많은 Li 를 받아야 한다 → **Li 석출 위험** 을 논문은 확인하지 않았다 (사후 분석 · 3 전극 측정 없음) | [우리 산술 · 추정] |
| 에너지 밀도 식 (Note S2) | E = 중량 용량 × 공칭 전압 × 활물질 비 × m_양극 / (m_양극 + m_음극) — **전극 수준** · 공칭 전압 값 [미확인] | [인쇄] Note S2 |
| 공칭 전압 역산 (NCM) | 476.7 · 380.2 Wh kg⁻¹ ↔ 5.63 · 4.50 mAh cm⁻² → **3.625 · 3.622 V** (두 셀이 같음 → 식 해석 맞음) | [우리 산술] |
| 공칭 전압 역산 (LFP) | 본문 용량 5.1 · 3.46 으로는 **3.10 · 3.27 V** (갈림) · 그림 5a 곡선 끝 4.93 · 3.57 [판독] 으로는 **3.20 · 3.17 V** — 그림 5e 의 LFP 값은 5a 곡선과 맞고 본문 숫자와는 안 맞는다 | [우리 산술] 🔴 §10-1 |

### 3-7. 시뮬레이션 상세 (SI p.3–5)

- **MD (BIOVIA Materials Studio 2025)**: 패킹으로 복합 구조 생성 → COMPASS 힘장 *(Condensed-phase Optimized Molecular Potentials for Atomistic Simulation Studies)* 기하 최적화 (SI ref 1) → **NPT 50 ps** 예비 완화 · 25 °C · 1 bar · Nose–Hoover–Langevin 열욕 · Berendsen 압력조 · **1 fs** · vdW 차단 **1.85 nm** · Ewald · PTFE · SBR 사슬 **5 단위체** · 원자 전하 = DMol3 DFT (최대 힘 0.002 Ha Å⁻¹ · 에너지 1.0 × 10⁻⁵ Ha · SCF < 1.0 × 10⁻⁶ Ha · DNP 기저) [인쇄 SI p.3–4].
  - ⚠ COMPASS 는 분자 · 고분자용 비반응 힘장이다 — 금속 Li 의 금속 결합과 **Li–PTFE 탈불소 반응 (그들 XPS 가 보인 LiF 생성)** 을 담지 못한다 → "Li–PTFE 접착 에너지 −1.39 eV" 는 반응 전 물리 흡착 모형의 값 [추정].
- **FEM (COMSOL Multiphysics 6.2, DFN)**: Blender 4.3 으로 Si · C 입자를 *"sequentially stacking … within a 50 μm thick domain"* → COMSOL 메시로 가져옴 (SI refs 4–5) · 식 (1) 고체 옴 i_s = −σ_s∇φ_s · 식 (2) 전해질 수정 옴 (농도 항 포함) · 식 (3) 전해질 Fick + 이동 · 식 (4) **입자 안 · 접촉을 통한 입자 사이** 고상 Fick ∂c_s/∂t = ∇·(D_s∇c_s) · 식 (5) 일반화 BV [인쇄 SI p.4–5].
  - 🔴 식 (3) 의 이동 항 *"i_l t₊ / F"* 에 발산이 없다 (차원이 안 맞음) · 식 (5) 의 둘째 지수 *"exp(αFη/RT)"* 에 음의 부호가 없다 (인쇄 그대로면 BV 가 아니다) · "COSMOL" 오식 [인쇄 대조].

---

## 4. ★ 방법 — 측정 사슬 · 시뮬레이션 · 입자 처리

### 4-1. 측정 사슬
Si/C + 흑연 (9 : 91) + Super-P + PTFE (96 : 1 : 3) → Thinky ARE-310 예비 혼합 → 막자 손 반죽 (응집 막) → 롤 캘린더 ≈85 µm 자립 막 → [ThA] SBR 처리 Cu · [PrL-ThA] Li/Cu 박에 라미네이트 (2.1 g cm⁻³ · 63–65 µm) → (i) 단면 SEM · 접힘 · 박리 · 계면 저항 (그림 2) (ii) 전해질 0 / 24 h 담금 앞 · 뒷면 TOF-SIMS · XPS · XRD (그림 3 · S3–S9) (iii) FEM SOC · 전위 지도 (그림 3d–e · S10) (iv) 반쪽 셀 CV · 첫 사이클 · EIS (화성 전 · 뒤) · 50 사이클 · 화성 뒤 XPS 깊이 · TOF-SIMS · 20 사이클 뒤 Si 단면 (그림 4 · S11–S15) (v) LFP · NCM811 전셀 첫 사이클 · 200/500 사이클 · 에너지 밀도 · 율속 · SOC 별 XPS · 제자리 EIS-DRT · 사이클 뒤 NCM811 TEM (그림 5 · S16–S22) → 문헌 비교 (표 S3).

### 4-2. 시뮬레이션 요약 (세부 §3-7)
- **MD**: COMPASS · Materials Studio · 5 단위체 사슬 · NPT 50 ps · E_adh = E_total − E_substrate − E_adsorbate (계당 eV, 면적 정규화 없음).
- **FEM**: COMSOL DFN · Blender 적층 입자 50 µm · 접촉을 통한 입자간 고상 확산 포함 · 물성 · 시간 미기재.
- **입자 스케일 역학 · 접촉망 모형**: 없음 (DEM · MPM · 망 0).

### 4-3. ★ 입자 처리 (우리 축 언어로)
- **실험 쪽**: 흑연 판상 입자 (S15 단면에서 길쭉한 층) + Si/C 복합 입자 (S15 에서 ≈5–8 µm 둥근 단면 [판독]) + PTFE 섬유 (섬유 지름 · 형태 미보고) + Super-P 1 wt% · 2.1 g cm⁻³ 까지 압밀 — **형상 변화 · 섬유화 · 압밀 기전 관찰 없음** · Li 금속 (항복 강도가 아주 낮은 금속) 이 라미네이트 때 막 바닥으로 흘러 들어가 맞물렸을 가능성은 논의되지 않는다 [추정].
- **계산 쪽 (FEM)**: Blender 로 "차례로 쌓은" 둥근 덩어리 입자 (그림 3d 렌더 [판독]) — **강체 기하 · 압밀 없음 · 접촉은 메시로 붙어 있어 접촉 저항 항 없음** (우리 CL-81 의 CONTACT_FREE 가지와 같은 범주 [추정]) · PTFE · CB 상은 그림에 없다.
- **계산 쪽 (MD)**: 원자 스케일 판 · 사슬 — 입자 · 전극 스케일 없음.
- **우리 DEM 과의 대응** [추정]: 강체 구 + Hertz/hysteresis · 응집 · 파괴 판정 — 금속 Li 층 · 집전체 · 바인더 막 · 고상 확산은 표현되지 않는다 (§7-2).

### 4-4. 기법 미니 용어집
- **ThA / PrL-ThA**: thick film anode (SBR 프라이머 Cu 위) / prelithiated ThA (Li/Cu 위) — 이 논문 이름.
- **Li/Cu**: Li 6.5 µm 를 Cu 10 µm 에 붙인 상용 박 (MTI Korea BR0182).
- **프라이머 (primer)**: 건식 막이 집전체에 붙도록 집전체에 미리 바르는 얇은 접착 · 도전 층 (여기서는 SBR — 도전재 포함 여부 [미확인]).
- **ICE**: 첫 사이클 쿨롱 효율 = 첫 방전 / 첫 충전 (반쪽 셀 음극은 탈리튬화 / 리튬화).
- **N/P**: 음극 / 양극 면적 용량 비 (여기서는 설계 비용량 기준 1.1).
- **TOF-SIMS**: 이온 빔으로 표면을 깎으며 2차 이온 질량을 재는 분석 — 스퍼터 시간 = 깊이 (속도를 알아야 µm 로 바꿈).
- **DRT**: 임피던스를 이완 시간 분포 γ(ln τ) 로 푼 것 — 봉우리 면적 ≈ 저항 · τ 구간 배정은 해석.
- **DFN (Doyle–Fuller–Newman)**: 다공 전극 · 전해질 · 고체 확산 · BV 를 묶은 전기화학 연속체 모형 — 여기서는 입자를 직접 그린 3D 판.
- **COMPASS**: 분자 · 고분자용 2 세대 (class II) 힘장 — 반응 (결합 끊김) 없음.
- **Q_Li = ρ_Li h C_th**: Li 금속 두께 → 면적 용량 (1 µm ≈ 0.206 mAh cm⁻² [우리 산술]).

---

## 5. Figure set ★ (크롭 35 장 = `litdb/figures/lee2026_li_underlayer_primer_free_dry_prelithiated_thick_anode/`)

| Fig | 내용 | 우리 활용 |
|---|---|---|
| cover | 표지 홍보 그림 (롤 사이 PTFE 섬유 + 입자 막 · Li 층 · Cu) — 본문 인용 없음 | 개념도 |
| 1 | (a) 선행 선리튬화 넷의 R2R · 건식 · 정밀 제어 O/X (저자 판정) (b) Li/Cu 한 단계 공정 개념도 (연속 건식 혼합 그림 ≠ 실제 손 반죽) | 공정 개념 (정성) |
| 2 | (a) 롤투롤 전극 사진 (~63 µm) (b) 단면 SEM · Li ~6.5 µm (c) 접힘 (d) 박리 ≈3.85 · ≈3.45 gf/mm [판독] (e) MD 접착 −0.89 · −1.39 eV (f) 계면 저항 0.0084 · 0.046 · 0.021 [판독] ("ohm cm⁻²") | ★ 집전체 계면 · 점착 (§7-3 · I 절) |
| 3 | (a–b) 24 h 전해질 뒤 앞 · 뒷면 TOF-SIMS + 3D (c) 개념도 (d) FEM SOC 지도 (e) SOC–높이 (26 µm 까지 고상 리튬화 [판독]) | ★ 고상 확산 깊이 (§7-4) |
| 4 | (a) CV (b) 첫 사이클 86.7 · 100.2 % (c–d) EIS 화성 전 · 뒤 (e) 50 사이클 (f–g) 뒷면 F 1s 깊이 (h–i) 뒷면 C/O/F 원자비 | 반쪽 셀 · SEI 화학 |
| 5 | (a) LFP 전압 곡선 (🔴 끝점 ≠ 본문) (b) LFP 200 사이클 (c) NCM 전압 곡선 (d) NCM 500 사이클 (e) 에너지 밀도 (f) 율속 (g–h) 제자리 DRT (i–j) NCM811 TEM · FFT (k) 문헌 비교 버블 | ★ Li 재고 오프셋 (§8-2) |
| S1 | ThA 단면 (~65 µm, 프라이머 안 보임) | 두께 |
| S2 | Li–Si · Li–Cu · Li–흑연 흡착 에너지 ≈−0.11 · −3.00 · −1.52 eV [판독] | (주의: 계산법 미기재) |
| S3 | pristine ThA TOF-SIMS (SiC⁻ 만) | 대조 |
| S4 | pristine ThA XPS (C–F₂ · C–C · C–O–C) | 대조 |
| S5 | ThA 24 h 담금 XPS (앞면 LiF · 뒷면 C–F₂) | 후막 뒷면 미반응 |
| S6 | XRD 흑연 피크 이동 (23–29° 만) | 고상 리튬화 증거 |
| S7 | pristine PrL-ThA TOF-SIMS (뒷면 LiSi⁻ · LiF₂⁻ · CH₃O⁻) | 고상 리튬화 |
| S8 | pristine PrL-ThA XPS (뒷면 LiF 685.4 · C–O) | PTFE 탈불소 |
| S9 | PrL-ThA 24 h 담금 XPS | SEI 성분 |
| S10 | FEM 평형 전위 · 전해질 전위 · SOC (🔴 캡션 'overpotential' ↔ 색 막대 'Equilibrium potential') | 구동력 지도 |
| S11 | EIS 등가 회로 두 개 | 회로 |
| S12 | 화성 뒤 R_SEI · R_ct 막대 (PrL 막대가 표 S1 보다 1.3–1.7 Ω 높음) | — |
| S13 | 앞면 F 1s 깊이 · 원자비 (F 33 · 60 %) | SEI 화학 |
| S14 | 화성 뒤 TOF-SIMS 앞 · 뒷면 | SEI 분포 |
| S15 | 20 사이클 뒤 Si 입자 단면 (위 · 아래) | 정성 균열 |
| S16 | LFP 131 µm · NCM811 82 µm 단면 | 양극 두께 |
| S17 | Li 재고 도식 · 계산 ICE (85.4 · ≈99 · ≈89 %) | ★ Li 재고 정산 틀 (§7-5) |
| S18 | 양극 반쪽 셀 (LFP 99.4 · NCM811 88.8 %) | 양극 한계 |
| S19 | LFP 에너지 밀도 200 사이클 | 궤적 |
| S20 | NCM 에너지 밀도 500 사이클 (🔴 캡션 'LFP') | 궤적 |
| S21 | 전셀 첫 화성 SOC 별 뒷면 F 1s | SEI 형성 시점 |
| S22 | 제자리 EIS 원자료 (Nyquist 3D) | DRT 원자료 |
| Table S1 | EIS 맞춤 (🔴 ThA 화성 뒤 합 170.0 ≠ 202.1) | — |
| Table S2 | 로딩 · 두께 · 비용량 · N/P | ★ 밀도 · 공극률 · N/P 재계산 원자료 |
| Table S3 | 선리튬화 문헌 비교 | 문헌 지도 |
| SI 식 1–2 · 3–5 | FEM 지배식 (🔴 식 3 · 5 오식) | 식 확인 |
| Note S1 · S2 | Li 두께 산정 · 에너지 밀도 식 | 재계산 |

## 6. Post-processing ★
- **무엇을**: SEM 두께 · 박리 곡선 · 계면 저항 막대 · MD 에너지 차 · TOF-SIMS 깊이 곡선 + 3D 재구성 · XPS 봉우리 맞춤 (C 1s · O 1s · F 1s) + 식각 깊이 원자비 · XRD 피크 위치 · FEM SOC · 전위 지도와 높이 평균 · CV · 정전류 곡선 → ICE · EIS 등가 회로 맞춤 · DRT (MATLAB) · 사이클 · 율속 · 에너지 밀도 (Note S2) · Li 재고 도식 (S17) · TEM FFT.
- **안 한 것**: 공극률 · σ_e · σ_ion · tortuosity · 박리 시험 기하 · 계면 저항 측정법 · 셀 반복 통계 · 오차 막대 · Li 두께 변화 (단일 6.5 µm) · 잔류 금속 Li 정량 · Li 석출 사후 확인 · 3 전극 측정 · 2×2 대조 (프라이머 × Li) · FEM 물성 · 시간 · MD 면적 정규화.
- **우리 후처리 (이 카드)**: 그림 판독 ≈95 행 (보정 검산 포함 — digitized.csv 머리) · 밀도 · 공극률 (가정 밀도) · N/P · Li 공급/손실 · 실제 첫 충전 기준 N/P · 공칭 전압 역산 (Note S2) · 표 S1 합 검산 · 사이클 절대 감소 분해 · 과전압 부호 산술 (S10).

---

## 7. ★ 우리 작업에 주는 것 (→ `our_dem_baseline.md` 는 정본 브랜치에서 자리표시 상태 — 우리 수치는 메인 리포 CLAUDE.md · 원장 `docs/reviews/claims.json` 의 해당 줄을 병기)

### 7-1. 비교표 — 같은 이름 · 다른 양 주의

| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 집전체 계면 저항 | 그림 2f [판독] 맨 Cu **8.4** · SBR 프라이머 **46** · Li/Cu **21.5 mΩ cm²** (액체 셀 음극 · Cu · 측정법 · 압력 미기재) | R_int 앵커 (메인 `docs/data/rint_eis_anchors.csv` 의 `collector_bare_pristine` · `collector_coated_pristine` 행): 집전체 접촉 pristine bare Al **10–18.5** · carbon-coated **3.5–10 Ω cm²** (출처 = 혼합 문헌 조사, 황화물 단독값 없음) | **2–3 자릿수 차** — 같은 "계면 저항" 이름의 다른 양일 가능성 (측정법 · 집전체 · 셀이 다름 · 이 논문은 측정법 미기재) → 이 숫자를 우리 R_collector 앵커로 옮기지 않는다 |
| 같은 축 문헌 대조 | SBR 프라이머가 저항을 **올린다** (8.4 → 46 mΩ cm²) | `nam2026_primer_layer_dry_electrode_collector`: 도전성 (Super P/CNT) 프라이머가 **내린다** (32 → 15.9–20.4 mΩ cm², 전극 수준 멀티프로브) | 프라이머 **종류** 가 방향을 정한다 — "프라이머 = 저항 ↑" 는 일반화 불가 [추정] |
| 전극 공극률 | 미보고 · [우리 산술 · 가정 밀도] **≈3–7 %** (2.1 g cm⁻³ 음극) | ps45 다섯 조성 정확 union 공극률 16.5–20.6 % (`comparison_vs_ours_DEM.md` A 절 2026-10-13 줄 · ASSB 양극 DEM) | 다른 전극 · 다른 전해질 (액체는 공극이 이온 경로) — 비교하지 않는다 |
| PTFE 의 지위 | Li 와 닿으면 C–F₂ → LiF (S8 · S21) = **Li 를 먹는 반응 상** | STEP3 `ptfe_stamp = centerline` — 전자 · 이온 절연 불활성 상 (원장 `CL-60`) | 양극 전위 (3–4.3 V) 에서는 우리 가정이 무해 · **PTFE 건식 음극 (Si · 흑연 · ASSB 음극 복합체)** 에서는 Li 재고 항이 빠진다 |
| 고상 확산 경로 | FEM 식 (4): 입자 안 + **접촉을 통한 입자 사이** Fick 확산 (접촉 저항 없음) | STEP4 (메인 `scripts/step4_dyn.py` `RadialDiffusion`): 입자마다 **독립 구형 1D Fick** + BV — 그 코드의 휴지 메타가 스스로 *"inter-particle redistribution NOT modeled (v2.1 hook …)"* 라 적는다 · 접촉망은 AM–AM 접촉 면적을 갖지만 고상 확산 채널은 없음 | 우리에게 없는 경로 (§7-4) |
| 접착 · 박리 | 박리 ≈3.45–3.85 gf/mm [판독] (기하 미기재) · MD eV (면적 정규화 없음) | 계면 점착 축 I (W_ad ↔ G_c 분리 규약, `comparison_vs_ours_DEM.md` I 절) · DEM 응집 = JKR 계 CED | 어느 쪽도 W_ad · G_c 로 옮길 수 없다 — 정성 대조만 |

### 7-2. DEM + MPM (압밀 · 접착 · frame[5])
- **이 논문의 접착 주장은 기계 기전이 비어 있다** — "Li 가 프라이머를 대신한다" 를 박리 곡선 하나 (그림 2d) 와 MD 접착 에너지 (그림 2e) 로만 받친다.  Li 금속은 항복 강도가 아주 낮은 금속이라 라미네이트 압력에서 막 바닥의 요철로 **소성 유동해 맞물리는** 기전이 자연스러운 후보인데 논의되지 않는다 [추정].  frame[5] 상 "무른 금속이 다공 입자층 바닥으로 흘러 들어가는 부피 보존 흐름" 은 MPM (J2 소성) 의 몫이고 접촉 면적 → 박리 강도는 DEM (bond · 응집) 의 몫이다 — 지금 우리 MPM 에 Li 금속 상 · 집전체는 없다 [추정].
- **압밀 · 공극률**: 2.1 g cm⁻³ (공극률 ≈3–7 % [우리 산술 · 가정]) 은 강체 구 DEM 의 바닥 (~20 %, frame[1]/[2]) 보다 훨씬 치밀하다 — 흑연 판상 입자의 재배열 · 변형 · 섬유 PTFE 가 만드는 치밀화이므로 우리 강체 구 DEM 의 검증 표적으로 쓸 수 없다 (입자 형상 · 크기 정보도 없음).
- **frame[5]**: 이 논문은 **계면 화학 + 전기화학 (실험) + 연속체 FEM** 반쪽을 가졌고, 압밀 · 라미네이트 · 접착의 **역학** 반쪽과 AM–AM · CB 의 **접촉망** 반쪽이 비어 있다.  그 FEM 은 압밀하지 않은 Blender 적층 기하 위에서 돌았다.

### 7-3. STEP3 복셀 · 접촉망 σ · 집전체 계면 (Rint 트랙)
- **σ_e · σ_ion 측정 0** — 우리 접촉망 · 복셀 σ 와 대조할 숫자가 없다.
- **집전체 계면 항**: 우리 망 솔버는 세대 2 의 **정확 Dirichlet 전극** (판에 이상 접촉) 이고 STEP4 는 R_int = 0 (전극 내부) 이 기본이다 (메인 `docs/project_rint_fullcell_cycling.md` §0).  이 논문 그림 2f 는 "계면 항은 집전체 처리 (프라이머 · Li 층 · 맨 Cu) 로 ×5 범위에서 움직인다" 는 정성 자료점이다 — 크기는 우리 R_int 앵커와 2–3 자릿수 다르므로 (§7-1) **측정법 표지를 붙여 별도 칸** 으로만 기록할 후보 [추정].
- **복셀 규약**: 이 논문 FEM 의 붙은 메시 = 접촉 저항 없는 가지 (우리 CL-81 의 `CONTACT_FREE` 와 같은 범주) — 그 SOC 깊이 (§3-3) 는 접촉 저항을 넣으면 줄어드는 쪽의 상한 성격이다 [추정].

### 7-4. STEP4 · FEM — 고상 확산 · 반응 분포
- ★ **전해질 없는 선리튬화 = ASSB 의 일상 상황** — 액체 셀에서 "전해질 없이" 는 특수 조건이지만, 황화물 ASSB 에서는 활물질 사이 Li 이동이 전해질 대신 **고체 접촉** 을 지나는 것이 기본이다.  이 논문 FEM (그림 3e) 은 접촉을 통한 고상 확산만으로 바닥의 Li 원천에서 **26 µm (영역의 52 %)** 까지 흑연이 리튬화된다는 정성 그림을 준다 (모사 시간 · D_s 미기재).
  - 우리 접촉망은 이미 **AM–AM 접촉 면적** (Hertz · Tabor) 을 갖는다.  확산 협착도 전기 협착과 같은 꼴 (원판 접촉 반지름 a 에서 확산 전도도 ≈ 2·D·a) 이라 Holm 망을 그대로 "고상 Li 확산 망" 으로 옮길 수 있다 [추정] — STEP4 의 입자별 독립 구형 확산에는 그 경로가 없다.  ASSB Si 음극 선리튬화 (`jun2026_ppma_econductive_binder_si_lowpressure_assb` — Li 증착 4.0 µm ≈23 % SOC) 같은 문제에서 의미가 있다 (F 목록 후보).
- **Li 원천이 집전체 쪽에 있는 경계** — 우리 STEP4 는 반응 전선이 분리막 쪽에서 시작하는 일반 경우만 다룬다 · 바닥 Li 저장고 경계는 없다 (후막 반응 분포 카드 `kim2026_operando_neutron_thick_nmc811_interior_hotspot` 과 반대 방향의 경계조건).
- **Li 재고 정산 틀 (S17)**: N/P · 반쪽 셀 ICE 로 전셀 ICE 를 계산하는 틀이 측정과 **10–13 %p (ThA) · +4.5 %p (PrL‖NCM)** 어긋난다 — 우리 STEP4 풀셀 · R_int 트랙 (메인 `docs/step4_assb_window_review.md` · `docs/project_rint_fullcell_cycling.md`) 에서 반쪽 셀 값으로 전셀 Li 재고를 조립할 때 같은 크기의 틀 오차를 예상해야 한다 [추정].

### 7-5. 건식 PTFE 작업 · 팔로우 랩 공정 기준점
- **팔로우 랩 (가천대) 건식 음극 레시피 기준점**: 활물질 (Si/C 9 : 흑연 91) : Super-P : PTFE = 96 : 1 : 3 · Thinky ARE-310 예비 혼합 → 막자 반죽 → 롤 캘린더 ≈85 µm → 라미네이트 · 2.1 g cm⁻³ · 13.5 mg cm⁻² · 5.6 mAh cm⁻² (액체 LIB).  형제 카드 `kim2026_pregranulation_…` (같은 랩 · NCA 양극 96 : 1.8 : 2.2 · Thinky 2000 rpm × 2 min × 5) 와 같이 보면 **이 랩의 건식 막은 PTFE 2.2–3 wt% · 탄소 1–1.8 wt% · Thinky 예비 혼합 + 반죽** 이 공통 틀이다 [인쇄 대조].
- **PTFE 환원 분해** = 건식 음극의 Li 소모 원천 (p.1945 · ref 20 · 21) — ASSB 양극 (우리 PTFE 축) 에는 해당 없음, ASSB 음극에 PTFE 를 쓸 때는 Li 재고 항으로 넣어야 한다.
- **집전체 접착**: ASSB 건식 양극 막도 탄소 코팅 Al 위에 라미네이트한다 (형제 카드 `kim2026_pregranulation_…`: Al 15 µm + C 1 µm) — 우리 모델은 막 ↔ 집전체 접착 · 계면 저항을 다루지 않는다 (F 목록에 이미 R_int 트랙).

### 7-6. ★ 믹서 논문 계획 (메인 `docs/mixer_paper_pipeline_draft_20261013.md` V1 · V2 · V3) 과 이종기술 논지
- **V2 (혼합 시간) — 앵커 불가 · 보고 누락의 사례**: 혼합이 Thinky 예비 혼합 (조건 없음) + **막자 손 반죽** (*"until a cohesive sheet formed"*) 이라 시간 · 회전 · 에너지가 0 건이다.  우리 V2 실험 (같은 혼합기 · 시간 2–3 수준) 은 rpm · 시간 · 배치 질량 · 반죽 방식을 기록해야 이 논문과 같은 빈칸을 피한다.
- **V1 (코팅 상태) — 교락 경고 사례**: 이 논문의 핵심 비교는 "프라이머 있음 + Li 없음 (ThA)" ↔ "프라이머 없음 + Li 있음 (PrL-ThA)" 두 모서리뿐이다 (2×2 의 나머지 두 칸 = 맨 Cu 전기화학 · 프라이머 + Li 가 없다).  계면 저항 이득 (프라이머 제거) 과 재고 이득 (Li 추가) 이 섞여 있고, 그림 2f 의 맨 Cu 막대 (가장 낮은 저항) 는 전기화학으로 이어지지 않는다.  우리 V1 (같은 SE 총량 · 코팅 유무) 도 **코팅 공정이 함께 바꾸는 것** (추가 기계 에너지 · 시간 · 입자 손상 · 순 조성) 을 별도 칸으로 떼야 같은 함정을 피한다 [추정].
- **V3 (SE 함량)**: n/a.
- **이종기술 논지 (메인 `docs/hetero_thesis.md`)**: SE 가 없어 직접 근거가 아니다.  "한 공정 단계가 두 기능 (접착 + Li 원천) 을 한다" 는 서사 틀은 논지의 "선코팅 = 분산 + 경로" 와 모양이 같지만, 이 논문은 두 기능의 몫을 가르지 않았다 — 우리 논문은 그 분해를 DEM 으로 보이는 것이 몫이다 [추정].

### 7-7. frame[4] · frame[5]
- **frame[4]**: 모형 보정 · 교차검증 대상 없음 (FEM 물성 미기재 · MD 정규화 없음).  실험 점으로만 쓴다.
- **frame[5]**: §7-2 — 전기화학 · 계면 화학 쪽을 가진 논문 · 역학 (라미네이트 · 압밀 · 접착) 과 접촉망 (고상 확산 · 전자 망) 이 빈 반쪽.

---

## 8. ★★ 우리 연구에 주는 insight (번호마다: 논문이 보인 것 → 우리에게 뜻 → 할 일)

**8-1. 두 처치를 함께 바꾼 두 점 비교 — 2×2 가 없다.**
- 논문: ThA (SBR 프라이머 · Li 없음) ↔ PrL-ThA (프라이머 없음 · Li) 만 비교 · 맨 Cu 는 저항 막대 하나 (그림 2f) 뿐.
- 뜻: 계면 저항 이득과 Li 재고 이득이 섞여 ICE · 용량 · DRT · TEM 결과의 몫을 가를 수 없다.  우리 믹서 논문 V1 도 "코팅 유무" 가 함께 바꾸는 것 (에너지 · 시간 · 손상) 을 분리해야 한다.
- 할 일: V1 실험 · 모델 설계표에 "코팅 공정이 함께 바꾸는 변수" 칸을 두는 것을 1저자 검토 항목으로 제안 (믹서 파이프라인 초안 §6 과 같이 볼 것).

**8-2. 선리튬화 이득은 재고 오프셋 — 감쇠 기울기는 같다 [판독 · 우리 산술].**
- 논문: NCM 500 사이클 절대 감소 PrL-ThA 1.40 · ThA 1.44 mAh cm⁻² (사이클 10 → 500) · 에너지 밀도 ≈153 · ≈149 Wh kg⁻¹ · LFP 는 PrL 이 더 많이 잃음 · 율속 차이도 대부분 오프셋.
- 뜻: "더 안정한 SEI · 양극 보호" 서사와 달리 숫자는 **출발 재고 차이** 를 보인다.  우리 A10 사이클 원장 (메인 `docs/a10_cycle_chemomech_design.md`) · R_int 트랙에서 Li 재고 (ICE · 손실) 와 접촉 · 수송 열화는 **다른 항** 으로 둔다는 설계가 맞다는 외부 사례.
- 할 일: 없음 (설계 확인) — 이 카드의 수치를 인용할 때 "기울기 같음" 을 병기.

**8-3. 접촉을 통한 고상 Li 확산 — 우리 망이 줄 수 있는데 지금은 없는 채널.**
- 논문: FEM 이 전해질 없이 26 µm 까지 리튬화 (메시 접촉 · 접촉 저항 없음 · 물성 미기재).
- 뜻: ASSB 에서는 이것이 기본 경로다.  우리 DEM 접촉망의 AM–AM 접촉 면적을 Holm 꼴 확산 전도도로 바꾸면 "접촉 망 고상 확산" 을 계산할 수 있다 [추정].
- 할 일: `comparison_vs_ours_DEM.md` F 절 (우리가 아직 못 하는 것) 에 한 줄 등재 제안 (공유 파일이라 이 커밋에서는 손대지 않고 문안만 보고).

**8-4. 집전체 "계면 저항" 은 측정법마다 다른 양.**
- 논문: 8.4–46 mΩ cm² (측정법 미기재) · 같은 축 nam2026: 16–32 mΩ cm² (멀티프로브, 도전성 프라이머가 저항을 내림 — 방향 반대).
- 뜻: 우리 R_int 앵커 (`rint_eis_anchors.csv` 의 집전체 접촉 행 3.5–18.5 Ω cm², 혼합 문헌 조사) 와 섞으면 2–3 자릿수가 틀린다.
- 할 일: R_int 앵커 표 (메인 `docs/data/rint_eis_anchors.csv`) 에 넣는다면 측정법 칸을 필수로 — 지금은 넣지 않는다.

**8-5. 이 논문 숫자를 쓸 때의 함정 다섯.**
- LFP 그림 5a 곡선 끝 (≈3.57 · ≈4.93) ≠ 본문 · 화살표 (3.46 · 5.1 · 1.64) · NCM "20 %" = 18.5 %p · 표 S1 ThA 화성 뒤 합 170.0 ≠ 202.1 · F:O 논리 뒤집힘 · 전셀 첫 충전 기준 N/P ≈0.93 (Li 석출 미확인) — 인용 시 그림 · 재계산값을 병기한다.

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Lee et al. (*Energy Environ. Sci.* 2026) laminated a dry-processed PTFE Si/graphite anode (96:1:3, 2.1 g cm⁻³, ≈63 µm) onto a 6.5 µm Li-coated Cu foil instead of an SBR-primed Cu collector; the half-cell ICE rose from 86.7 to 100.2 % and the NCM811 full-cell ICE from 74.8 to 93.3 % (5.63 mAh cm⁻²), while the absolute capacity fade over 500 cycles was similar for both cells (read from their Fig. 5d), i.e. the gain is mainly a lithium-inventory offset."
- 국문: *"건식 후막 음극을 프라이머 Cu 대신 Li 를 입힌 Cu 에 붙이면 Li 가 고상 확산으로 음극을 미리 리튬화해 첫 사이클 손실을 지운다는 보고가 있다 (Lee 2026, 액체 LIB) — 단 Li 공급은 손실의 1.42 배였고 사이클 감쇠 기울기는 바뀌지 않았다 (그림 판독)."*

## 10. 🔴 레드 플래그 — 원문 불일치 · 빠진 조건 · 해석 과장 (over-claim 방지)

1. **LFP 그림 5a ↔ 본문 · 그림 5b**: 5a 곡선 끝 [판독] ThA **≈3.57** · PrL-ThA **≈4.93 mAh cm⁻²** (차 ≈1.36, PrL 곡선만으로 ICE ≈99 %) ↔ 본문 · 화살표 **3.46 · 5.1 · "1.64 mAh cm⁻² (24.5 %)"** · ICE 표지 96.6 % ↔ 5b 첫 점 [판독] **3.46 · 5.11** (본문과 같음) ⇒ 5a 곡선은 다른 셀로 보인다.  그림 5e 의 LFP 에너지 밀도 (246.0 · 342.4) 는 5a 곡선 용량으로만 같은 공칭 전압 (3.17–3.20 V) 이 나온다 [우리 산술 §3-6].  NCM (5c · 5d · 5e) 은 서로 맞는다.
2. **NCM ICE 개선 "20 %"**: 93.3 − 74.8 = **18.5 %p** (상대 +24.7 %) [우리 산술] · 그림 5c 의 "(20 %)" 는 1.13/5.63 (용량 몫) 인데 5a 의 "(24.5 %)" 는 ICE 차 (%p) — 같은 자리 괄호의 정의가 다르다 · 개요의 *"increasing by 20% the ICE of NCM811 full-cell"* (p.1944) 도 같은 숫자.
3. **표 S1**: ThA 화성 뒤 R_s + R_SEI + R_ct = **170.0 ≠ R_total 202.1** [우리 산술] · 그림 4d 호 끝 ≈110 Ω [판독] (PrL ≈45 ↔ 60.2) · S12 PrL 막대 29.5 · 32.1 ↔ 표 27.8 · 30.8.
4. **F:O 논리**: *"~1:1 (PrL) compared with 3:2 (ThA) … confirming a higher contribution of F-rich inorganic components"* — F:O 는 ThA 가 높다 (1.43 vs 1.10 [판독]) · *"On the back, LiF remained the primary component in both electrodes"* ↔ 그림 4f ThA 뒷면 0 분 = LixPFyOz 가 주 봉우리 [판독].
5. **XPS 배정 일관성**: ThA 의 "LiF" 봉우리 ≈686.2–686.4 eV (그림 4f · S13a) ↔ PrL-ThA LiF ≈685.0 eV (같은 그림 쌍) ↔ S21 LiF ≈684.5 eV [판독] · 같은 ≈689.3 eV 봉우리를 S4 는 "C-F₂", S8 은 "C-F₃" 로 표지 · 대전 보정 기준 [미확인] · 식각 속도 [미확인].
6. **Li 양의 "정밀 최적화"**: 공급 1.34 / 손실 0.943 = **1.42** (42 % 초과) [우리 산술] · Li 두께는 상용 박 하나 (6.5 µm) 로 변화 시험 없음 · 반쪽 셀 ICE 100.2 % = 초과분 ≈0.40 mAh cm⁻² 가 가역 용량으로 안 나타남 → 행방 (추가 SEI? 잔류 금속 Li?) 미정산 · S6 XRD 는 Li 피크 영역을 안 보여 줌 · Note S1 의 로딩 13.7 mg cm⁻² 는 표 S2 와 다름.
7. **실제 N/P · Li 석출**: N/P 1.1 은 설계 비용량 (428.27 = 2nd 탈리튬화 [판독] · 191.82 = 양극 반쪽 셀 첫 방전) 기준 · NCM 전셀 첫 충전 ≈6.06 mAh cm⁻² (≈230 mAh g⁻¹) [판독] → 실제 첫 충전 기준 N/P **≈0.93** [우리 산술] + 밑층 초과 Li → 충전 끝 Li 석출 가능성 [추정] — 사후 분석 · 3 전극 측정 없음.
8. **전셀 ICE > 양극 반쪽 셀 ICE** (93.3 > 88.8 %): *"synergistic effect of the structural stability of the active materials"* 로 설명 — 시험 없음 · 반쪽 셀 C-rate [미확인] · 차단 전압 차이로도 생길 수 있음 [추정] · ThA 의 계산 대비 −10.6 ~ −13.3 %p 는 설명 없음.
9. **설계 교락**: 프라이머 제거 + Li 추가를 함께 바꾼 두 점 (§8-1) · 맨 Cu 는 저항 막대만 · *"the difference in the initial discharge capacity … is due solely to the prelithiation"* (p.1950) 는 프라이머 차이를 무시한 서술.
10. **"500 사이클 안정"**: 절대 감쇠가 같다 (§3-5) · NCM 500 사이클 유지율 미인쇄 · LFP "197 사이클" 유지율의 기준 사이클 [미확인].
11. **박리 "similar"**: PrL-ThA ≈10 % 낮음 [판독] · 시험 기하 · 폭 · 속도 · 시편 수 [미확인] · 접힘 시험은 정성.
12. **그림 2f**: 축 단위 "ohm cm⁻²" · 측정법 · 압력 [미확인] · 맨 Cu 가 가장 낮다는 사실 (Li 층이 저항을 더함) 은 본문에 없음.
13. **MD 접착 에너지**: 계당 eV · 면적 · 사슬 수로 정규화 없음 · SBR (5 단위체 사슬) 과 Li 판의 크기가 다른 계를 비교 · COMPASS (비반응) 로 금속 Li · 탈불소 반응을 못 담음 [추정] · *"lower adhesion energy indicates enhanced interfacial stability"* 의 기준 불명 · S2 흡착 에너지 계산법 [미확인].
14. **TOF-SIMS "전극 깊이 전체"**: 스퍼터 0–300 s · 앞 · 뒷면 두 표면만 (§3-3) · 뒷면 측정을 위해 막을 Li/Cu 에서 어떻게 떼었는지 [미확인].
15. **FEM**: 물성 · 입자 수 · 크기 · Si : C 비 · Li 경계조건 · 모사 시간 · 메시 [전부 미확인] · 영역 50 µm ↔ 전극 63–65 µm · 압밀 안 한 Blender 적층 · 식 (3) 발산 누락 · 식 (5) 부호 누락 · S10 캡션 "overpotential" ↔ 그림 "Equilibrium potential" · "(~52%)" 정의 없음.
16. **"Fully dry · roll-to-roll"**: 막은 **막자 손 반죽** · 롤 공정은 캘린더 · 라미네이트 · 셀은 액체 전해질 · 그림 1b 의 연속 혼합 그림 ≠ 실제 · Video S1 [SI 미확보] · 그림 1a 에서 "Li 금속 직접 접촉" 을 세 항목 모두 X 로 그렸는데 이 논문 방법도 Li 금속 직접 접촉의 한 형태.
17. **빠진 공정 조건**: 예비 혼합 rpm · 시간 · 반죽 시간 · 캘린더 · 라미네이트 압력 · 온도 · SBR 프라이머 조성 · 두께 · ≈85 µm → 63–65 µm 감소 과정 · 양극 제조법 · 바인더 · 집전체 · 입경 · 공극률.
18. **문헌 비교 (표 S3 · 그림 5k)**: Si 함량이 높은 음극들과 흑연 우세 음극 (Si/C 9 wt%) 의 ICE 를 나란히 놓음 · "Roll-to-Roll" 을 선리튬화 전략 칸에 · S16 은 같은 그룹.
19. **양극 공극률**: NCM811 3.56 g cm⁻³ → ≈13 % [우리 산술 · 가정 밀도] — 액체 셀 양극으로 아주 치밀 · 설명 없음.
20. **표기 · 조판**: "Repubilc" (SI p.1) · "meterials" (p.1945) · "COSMOL" · "Mass Lading" · 그림 4d "foramtion" · S12 "trasnfer" · S20 캡션 LFP/NCM 혼동 · CV 범위 1.0 V (캡션) ↔ 1.5 V (SI 방법) · SI 참고문헌 번호 1–4 가 Note S1 의 인용 (과잉 선리튬화 위험 · Li 밀도) 에도 다시 쓰였는데 목록상 그 번호는 COMPASS 힘장 · MD 문헌 — 번호 재사용 의심 [추정] · 저자 기여 목록에 Y.-C. Hwang · D.-H. Kim 없음.

## 11. 다른 카드 정정 후보 (보고만 — 이 커밋에서 손대지 않음)
1. `gandla2026_layered_cathode_degradation_diagnostics_review` §12 ref 128 행: *"카드 없음 — 일단계 건식 후막"* → 이제 이 카드 (`lee2026_li_underlayer_primer_free_dry_prelithiated_thick_anode`) 가 있다 (링크 갱신 후보).
2. `kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation` §12 ref 17 행 (S. Han … *J. Energy Storage* 96 (2024) 112693): 그 카드의 저자 목록은 "T. Song" 에서 끝나는데 이 논문 ref 21 은 같은 논문을 *"… T. Song, W.-J. Kwak and J. Choi"* 로 인쇄한다 — 두 논문의 참고문헌 표기가 다르다 (원 논문 저자 목록 [미확인]; 같은 팔로우 랩 논문일 가능성 — 원문 확인 전까지 표지 판단 보류).
3. `nam2026_primer_layer_dry_electrode_collector` (정정 아님 · 교차 링크 후보): 이 논문 그림 2f 는 SBR 프라이머가 계면 저항을 올리는 반대 방향 사례 (8.4 → 46 mΩ cm² [판독]) — "프라이머 종류가 방향을 정한다" 한 줄을 붙일 수 있다.
4. `lee2026_lpscl_coating_thickness_ncm811` 머리의 *"현재 litdb 전체에 `Taeseup Song` 등장 0회"* — 형제 카드가 이미 지적한 낡은 문장 · 이 카드에도 Taeseup Song (소속 c · i) 이 있다.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)

**같은 그룹 후보 (팔로우 랩 카드 후보 — "J. Choi" 가 Junghyun Choi 인지는 머리글자만이라 [미확인])**

| 번호 | 서지 (원문 목록 그대로) | 왜 · 카드 |
|---|---|---|
| 21 | S. Han, E.-H. Noh, S. Chae, K. Kwon, J. Lee, J.-S. Woo, S. Park, J. W. Lee, P. J. Kim, T. Song, W.-J. Kwak and J. Choi, J. Energy Storage, 2024, 96, 112693. | 카드 없음 — 후막 건식 음극의 PTFE 분해 · FEC (이 논문 서론의 출발점) |
| SI 16 | D. Lee, W. Jeong, J. Lee, H. E. Yoo, S. Sun, C. Lee, J. Kim, Y. Kim, M. Yoon, P. J. Kim, U. Paik, J. W. Lee, T. Song, J. Choi, Int. J. Ener. Res. 2025, 1198001. | 카드 없음 — 같은 그룹 Si-G‖NCM811 (표 S3 비교군 S16) |

**우리 축에 직접 닿는 것**

| 번호 | 서지 (원문 목록 그대로) | 왜 · 카드 |
|---|---|---|
| 18 | N.-Y. Kim, J.-H. Kim, H. Koo, J. Oh, J.-H. Pang, K.-D. Kang, S.-S. Chae, J. Lim, K. W. Nam and S.-Y. Lee, ACS Energy Lett., 2024, 9, 5688–5703. | 카드 없음 — 프라이머가 저항을 키운다는 근거 (ref 18–19) |
| 19 | D. Burger, N. Keim, J. Shabbir, Y. Gao, M. Müller, W. Bauer, A. Hoffmann, P. Scharfer and W. Schabel, Energy Technol., 2024, 13, 2401668. | 카드 없음 — 〃 |
| 20 | Z. Wei, D. Kong, L. Quan, J. He, J. Liu, Z. Tang, S. Chen, Q. Cai, R. Zhang, H. Liu, K. Xu, L. Xing and W. Li, Joule, 2024, 8, 1350–1363. | 카드 없음 — PTFE 환원 전위 > PVDF (ASSB 음극 PTFE 의 Li 소모 근거 후보) |
| 22 | T. Lee, J. An, W. J. Chung, H. Kim, Y. Cho, H. Song, H. Lee, J. H. Kang and J. W. Choi, ACS Appl. Mater. Interfaces, 2024, 16, 8930–8938. | 카드 없음 — FEC 를 넣어도 흑연 ICE 87 % (refs 22–24) |
| 25 | T. Danner, M. Singh, S. Hein, J. Kaiser, H. Hahn and A. Latz, J. Power Sources, 2016, 334, 191–201. | 카드 없음 (`park2020_digitaltwin_assb_foundational` 이 인용) — 후막 농도 기울기 · 불균일 전류 |
| 27 | L. S. Kremer, T. Danner, S. Hein, A. Hoffmann, B. Prifling, V. Schmidt, A. Latz and M. Wohlfahrt-Mehrens, Batteries Supercaps, 2020, 3, 1172–1182. | 카드 없음 — 후막 미세구조 · 수송 모사 |
| 30 | J. Lee, D. Jin, J. Y. Kim, Y. Roh, H. Lee, S. H. Kang, J. Choi, T. Jo, Y. Lee and Y. M. Lee, Adv. Energy Mater., 2023, 13, 2300172. | 카드 없음 — 전해질 없이 Li 직접 접촉 고상 리튬화 (Yong Min Lee 그룹 · 우리 디지털 트윈 축) |
| 32 | C. Yang, H. Ma, R. Yuan, K. Wang, K. Liu, Y. Long, F. Xu, L. Li, H. Zhang, Y. Zhang, X. Li and H. Wu, Nat. Energy, 2023, 8, 703–713. | 카드 없음 — 전사 인쇄 선리튬화 (표 S3 의 S9) |
| 34 | W. Jin, G. Song, J. Yoo, S. Jung, T. Kim and J. Kim, ChemElectroChem, 2024, 11, e202400288. | 카드 없음 — 건식 음극에 프라이머가 필요하다는 근거 |
| 39 | X. Lu, M. Lagnoni, A. Bertei, S. Das, R. E. Owen, Q. Li, K. O'Regan, A. Wade, D. P. Finegan, E. Kendrick, M. Z. Bazant, D. J. L. Brett and P. R. Shearing, Nat. Commun., 2023, 14, 5127. | 카드 없음 — 후막 위쪽에 반응 집중 (S15 해석 근거) |
| 8 | X. Lu, S. R. Daemi, A. Bertei, M. D. R. Kok, K. B. O'Regan, L. Rasha, J. Park, G. Hinds, E. Kendrick, D. J. L. Brett and P. R. Shearing, Joule, 2020, 4, 2746–2768. | 카드 없음 (`he2026_dem_calendering_inhomogeneity_areal_density` 가 인용) — 후막 미세구조 설계 |
| SI 4 | J. Moon, T. D. Hoang, S. Soo Park, S. Park, D. Y. Rhee, J. Lee, S. A. Han, M.-S. Park and J. H. Kim, J. Ener. Chem., 2022, 71, 470–477. | 카드 없음 — 이 논문 FEM 의 기하 생성 · 메시 출처 (Moon 연구실) |
| SI 7 | J. Y. Kim, S. Jung, S. H. Kang, J. Park, M. J. Lee, D. Jin, D. O. Shin, Y. Lee and Y. M. Lee, Adv. Energy Mater., 2021, 12, 2103108. | 카드 없음 — 고상 확산 식 (4) 의 출처 (Yong Min Lee 그룹) · 권 12 / 2021 년 표기 그대로 |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-13)
- 본문 11 쪽 (표지 1 + 학술지 10) · SI 34 쪽 텍스트 층 전수 (pdftotext) · 저자 · 소속 · 교신 · 날짜 · DOI · 라이선스 · 연구비 · 특허 · 데이터 진술 · 저자 기여 = p.1944 · p.1951–1952 · SI p.1 그대로 옮김.
- 글꼴 대응 문제로 추출이 깨진 기호를 렌더로 확인: *"~6.5 µm"* (p.1946) · *"(−1.39 eV)"* · *"(~52%)"* (p.1947) · *"−0.27 V … −0.035 V"* · *"(~0.3 V)"* (p.1948).
- 크롭 35 장 손 크롭: 본문 그림 = 래스터 원본 300 ppi 영역 300 dpi · SI 그림 = 래스터 ≈220 ppi (S19 · S20 ≈257) 를 220 / 260 dpi · SI 표 · 식 · Note = 벡터 300 dpi · 흰 여백만 자름 · 전부 렌더로 열람 (접촉 시트 포함).
- 판독 보정 검산 (digitized.csv 머리): 그림 5b · 5d 첫 점 ↔ 본문 · 그림 5c 끝점 차 1.14 ↔ 1.13 · 그림 4b 손실 69.7 ↔ 68.9 · S12 ThA 막대 ↔ 표 S1 · 그림 4h–i F:O ↔ 본문 · S13 F ↔ 본문 · 그림 3e 위끝 ↔ "6 %".
- 재계산: 밀도 · 공극률 (가정 골격 밀도) · N/P · Li 공급 · 손실 · 실제 첫 충전 기준 N/P · Note S2 공칭 전압 역산 · 표 S1 합 · 사이클 절대 감소 · S10 과전압 부호.
- 정본 litdb 중복 확인: `git ls-tree` 로 `litdb/papers/` 432 장 전수 + DOI (d5ee05739f) · 제목 낱말 (prelithiat · primer-free · Li/Cu · PrL-ThA · Kwak) 을 `litdb/` 전체 grep — 이 논문 카드 없음 · `gandla2026_…` 의 참고문헌 행 하나만 인용.

## 🔗 관련 카드
- 같은 팔로우 랩: `kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation` · `gandla2026_layered_cathode_degradation_diagnostics_review`.
- 건식 전극 · 집전체 계면: `nam2026_primer_layer_dry_electrode_collector` · `nam2026_dpe_microstructure_review` · `lee2026_unveiling_ptfe_dry_electrode_digital_twin` · `hippauf2019_dry_film_ptfe_sulfide_cathode_sheet` · `lee2025_dual_fibrous_ptfe_dry_electrode` · `matthews2024_ptfe_nanofibril_network` · `kang2025_bollard_anchored_binder_dry_electrode` · `lee2025_corolling_dryprocess_lpscl_ptfe` · `mun2025_dry_electrode_technology_assb_review` · `liu2025_dry_processing_high_energy_li_batteries_review`.
- 음극 · 선리튬화: `jun2026_ppma_econductive_binder_si_lowpressure_assb` · `kim2026_electrolyte_interfacial_reactivity_alloying_anode_pulverization`.
- 점착 · 박리 · 계면: `liao2025_interfacial_adhesion_li_plating_carbon_interlayer` · `zhang2026_xct_dem_cathode_calendering_peel_calibration`.
- 후막 반응 분포 · 모사: `kim2026_operando_neutron_thick_nmc811_interior_hotspot` · `park2020_digitaltwin_assb_foundational` · `bazzoun2026_dem_fem_rnm_ionic`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
