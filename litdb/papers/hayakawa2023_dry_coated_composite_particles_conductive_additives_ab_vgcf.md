<!-- digest 표준 양식 확장 (paper-level STANDALONE).  ★ = 이 묶음 (후보 표 3 순위 · N-81 · 코팅 활물질 · 정독 130) 에서 꼭 뽑으라고 한 항목.
     본 = jeong2024_operando_densification_chemomechanics_se_size_composite_cathode.md (절 번호 체계 · 머리 요약 상자 · 메타 줄 · 서지 표 · 그림 표 꼴).
     같은 그룹 · 같은 장치 이웃 = kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps.md · nakamura2020_dry_coating_ncm_li3ps4_core_shell.md (같은 Nara 건식 충격 블렌딩 · 같은 13,000 rpm · 5 min).
     두 필수 절 (§0-1 고른 의도 대조 · §8 자세한 분석) 은 같은 묶음 카드들과 같은 꼴.
     원문 = 출판본 (J. Power Sources 555 (2023) 232379 · 9 쪽 · PDF 쪽 n = 인쇄 쪽 n) + 보충 자료 2 쪽 (PDF 정보: 만든 프로그램 Microsoft Word · 만든 날 2026-11-12 → 출판사 SI 파일 (Word) 을 PDF 로 바꾼 사본으로 보인다 [카드 해석] · 쪽 = "SI p.n").
     값 표지: [인쇄] = 본문 · 표 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv 332 행 — 그림 6–10 은 순수 벡터라 픽셀이 아니라 PDF 경로 좌표 (표지 원 중심 · 곡선 꼭짓점 · 틀 눈금선 보정) 에서 읽었다 → 판독 오차는 선 굵기 수준 (≤ 0.3 pt ≈ 축 길이의 0.3 %)) ·
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 · [다른 카드] = 정본의 다른 카드에 적힌 값 (slug 병기) · [우리] = CLAUDE.md 출처 우리 값 · [미확인] = 본문 9 쪽 + SI 2 쪽 전수에 없음.
     원문 11 쪽은 글자 층 추출 + 쪽 렌더로 전부 읽었다.  DEM · MPM · FEM · 입자 계산 · 압밀 모델은 없다 — 실험만 (건식 코팅 · SEM/EDX · 순 조성 · EIS · 충방전 · CV). -->
# 건식 충격 블렌딩 (Nara · 13 000 rpm · 5 min) NCM523@Li₆PS₅Cl 코어–셸 복합 입자 + 도전재 — 아세틸렌 블랙 (일차 ≈35 nm) 은 SE 껍질 (100–1000 nm) 안으로 · VGCF (≈150 nm × ≈6 µm) 는 입자 밖으로 · 360 MPa 이온 차단 셀 EIS: 껍질만 (CP) σ_e 1.4 × 10⁻⁶ S cm⁻¹ = 막자 혼합 (SM) 2.8 × 10⁻⁵ 의 1/21 · σ_ion 3.2–4.6 × 10⁻⁵ S cm⁻¹ 유의차 없음 · CP-VGCF σ_e 최고 (5.0 × 10⁻⁴) 인데 율속 · CV 약함 ('층 σ_e ≠ AM 전자 공급') · CP-AB 2 C 방전 97.7 mAh g⁻¹ · 50 사이클 92.9 % — Hayakawa · Nakamura · Ohsaki · Watano (J. Power Sources 2023)

> slug `hayakawa2023_dry_coated_composite_particles_conductive_additives_ab_vgcf` · DOI `10.1016/j.jpowsour.2022.232379` · type `exp (건식 충격 블렌딩 dry process 코팅 · powder 코어–셸 복합 입자 · SEM/EDX morphology · UV–vis + TG–DTA 순 조성 · 이온 차단 셀 EIS impedance (360 MPa) · Li–In 반쪽셀 첫 사이클 · dQ/dV · 율속 · 50 사이클 · equivalent circuit Rs/Rct · CV — DEM · MPM · 모델 계산 없음)` · PDF `f403a22c-81._Design_of_active-materialsolid-electrolyte_composite_particles_with_conductive_additives_for_all-solid-state_lithium-ion_batteries.pdf` · SI `81f219c1-81._Sup_Design_of_active-materialsolid-electrolyte_composite_particles_with_conductive_additives_for_all-solid-state_lithium-ion_batteries.pdf` · digested `2026-11-16` · status ✅
>
> **원제**: *Design of active-material/solid-electrolyte composite particles with conductive additives for all-solid-state lithium-ion batteries* (p.1)
> **저자 · 소속 (p.1 · SI p.1 같음)**: Eiji Hayakawa · **Hideya Nakamura\*** · Shuji Ohsaki · Satoru Watano — Department of Chemical Engineering, **Osaka Metropolitan University**, Sakai, Osaka 599-8531, Japan (\* 교신 hideyanakamura@omu.ac.jp) · *J. Power Sources* **555** (2023) **232379** · 접수 2022-09-16 · 수정 2022-10-27 · 승인 2022-11-06 · 온라인 2022-11-17 (p.1) · 연구비 NEDO SOLiD-EV (JPNP18003) · 이해상충 없음 · 자료 = 요청 시 (p.8) · 키워드 (PDF 정보) *Dry coating · Conductive additives · Core-shell composite particle · All-solid-state battery*.
> **같은 그룹 · 같은 장치 이웃 (링크만)**: [`kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps`](kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps.md) (그 카드 ref 26 = 이 논문 · 같은 장치 · 13,000 rpm · 5 min · Li₃PS₄ · 무탄소) · [`nakamura2020_dry_coating_ncm_li3ps4_core_shell`](nakamura2020_dry_coating_ncm_li3ps4_core_shell.md) (이 논문 ref [15]) · [`kawaguchi2017_dry_coating_parametric_na2so4_model_se`](kawaguchi2017_dry_coating_parametric_na2so4_model_se.md) (ref [13] — 공정 조건 최적화의 근거) · [`kawaguchi2018_dry_coating_model_se_particle_powtec`](kawaguchi2018_dry_coating_model_se_particle_powtec.md) (ref [14]) · [`kissel2026_mechanofusion_derived_cathode_composite_microstructures_scalable`](kissel2026_mechanofusion_derived_cathode_composite_microstructures_scalable.md) (이 논문을 ref 63 으로 인용 · CB 를 껍질에 넣은 메카노퓨전) · [`frankenberg2025_milling_dry_processed_sulfide_cathode_microstructure`](frankenberg2025_milling_dry_processed_sulfide_cathode_microstructure.md) (ref 63) · [`kim2025_conductive_agent_se_coating_cathode`](kim2025_conductive_agent_se_coating_cathode.md) (같은 질문 · 반대 결론 — §7-3).
> **판독 원자료**: `litdb/figures/hayakawa2023_dry_coated_composite_particles_conductive_additives_ab_vgcf/digitized.csv` (332 행 — 그림 6a · 6b 표지 + 오차 막대 끝 · 그림 7a 곡선 끝 · 3.6 V 도달 용량 · 7b 봉우리 · 7c · 7d 표지 40 · 그림 8 나이키스트 표지 · 그림 9 CV 극값 · 그림 10 표지 200) · 그림 크롭 **43 장** (도구 12 중 다시 자름 9 + 캡션만 고침 1 · 손 크롭 31 = 그래픽 초록 1 · SI 그림 S1 1 · 패널 9 · 식 0 · 근거 문단 20) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: NCM523 (LiNbO₃ 1 wt% 선코팅 · 개수 중앙 4.3 µm) 에 Li₆PS₅Cl (개수 중앙 0.7 µm · 2.02 mS cm⁻¹) 을 **건식 충격 블렌딩 (Nara · 13,000 rpm · 5 min · 투입 10.0 g)** 으로 입힌 코어–셸 입자 (순 SE ≈16–17 wt%) 는 같은 SE 몫의 막자 혼합보다 **360 MPa 압분체 전자 전도도가 1/21** (1.36 × 10⁻⁶ vs 2.84 × 10⁻⁵ S cm⁻¹ [판독 그림 6b]) 이고 0.1 C 첫 방전이 **81.7 vs 137.0 mAh g⁻¹** [판독 그림 7a · 본문은 CP "ca. 87"] 로 떨어진다 — 비전도 SE 껍질이 AM–AM 전자 접촉을 막기 때문 (저자).  도전재를 코팅 전 예비 혼합에 넣으면 **아세틸렌 블랙 (AB) 은 껍질 안에 들어가** 용량 (142.3) · 율속 (2 C 방전 97.7 vs SM 63.9 [판독]) · 50 사이클 유지 (92.9 vs 32.2 % [인쇄] · SM 판독 29.9 %) 를 모두 살리지만 그 압분체 σ_e 는 **여전히 SM 의 0.22 배**이고, **VGCF 는 껍질에 못 들어가 입자 밖에 남아** σ_e 를 SM 의 **17.6 배 (5.0 × 10⁻⁴)** 로 올리면서도 율속 (2 C 30.7) · CV 전류가 가장 약하다 → 저자: 층 전체 σ_e 는 *"not an indicator of the ease of supplying electrons to AM particles"* (p.7).  이온 전도도는 네 시료 모두 3.2–4.6 × 10⁻⁵ S cm⁻¹ 로 유의차가 없다 (p.4 · N = 3 · SD 큼).  **기공 · 두께 · 밀도 · 압력별 측정 · 탈압 · 계산 모델은 없다.**

| 우리 질문 (이 묶음) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ 복합 입자 · 조성 · 공정 | AM = **NCM523** (Sumitomo Metal Mining · LiNbO₃ **1 wt%** 선코팅 · 개수 중앙 **4.3 µm** · SEM = 일차 입자가 뭉친 다결정 2차 입자) · SE = **Li₆PS₅Cl** (Mitsui Mining & Smelting · 개수 중앙 **0.7 µm** · **2.02 mS cm⁻¹**) · AB = Denka Black Li-100 (일차 **≈35 nm**) · VGCF = Showa Denko (지름 **≈150 nm** · 길이 **c.a. 6 µm**) · 헵테인 초음파 예비 혼합 → 증발 → 393 K 감압 건조 → **10.0 g** 투입 → **13,000 rpm · 5 min** (Ar · 이슬점 < 193 K) · 순 조성 (표 1): SM **84.0 : 16.0** · CP **83.1 : 16.9** · CP-AB **81.4 : 15.8 : 2.79** · CP-VGCF **81.7 : 16.6 : 1.62** wt% | [인쇄] p.2 · p.4 · 표 1 |
| ② ★ 성형압 · 작동압 | 이온 차단 셀: 복합 입자 **80 mg · 360 MPa** (지름 · 시간 [미확인]) / 반쪽셀: SE **80 mg · 20 MPa** (10 mm 다이 · 수 초) → 복합 입자 **10 mg · 360 MPa · 5 min** → Li–In **90 MPa · 5 min** · 운전 적층압 · 체결 토크 [미확인] (SUS 막대 두 개) · **298 K** | [인쇄] p.2–3 |
| ③ ★ 기공 · 두께 · 밀도 | **없음** — 이온 · 전자 σ 를 *"thickness of the composite cathode, and electrode area"* 로 냈다면서 (p.3) **두께 값은 인쇄하지 않았다** · 진밀도 · 기공 · 겉보기 밀도 [미확인] | [인쇄] p.3 |
| ④ ★ σ_ion · σ_e (360 MPa 압분체 · EIS 두 반원 맞춤) | σ_ion (×10⁻⁵ S cm⁻¹ · 평균 ± SD · N = 3): SM **3.52 ± 1.42** · CP **3.21 ± 1.03** · CP-AB **3.78 ± 0.69** · CP-VGCF **4.61 ± 2.07** [판독 벡터] — "no significant difference" (p.4) / σ_e (S cm⁻¹): SM **2.84 × 10⁻⁵** · CP **1.36 × 10⁻⁶** · CP-AB **6.37 × 10⁻⁶** · CP-VGCF **5.02 × 10⁻⁴** [판독 벡터] — 본문 "CP-AB ≈5 × CP" · "CP-VGCF ≈18 × SM" (p.4–5) ↔ [카드 산술] 4.7 · 17.6 | [판독] 그림 6 · [인쇄] p.4–5 |
| ⑤ ★ 도전재 자리 (껍질 안 / 밖) | C 지도: CP-AB = 껍질 자리의 탄소 세기가 AM 심보다 높다 (흰 화살표) → AB 가 껍질 안 · CP-VGCF = 섬유가 입자 밖 (빨간 화살표) · 기전 (저자) = VGCF 지름 ≈150 nm > AB ≈35 nm · 길이 ≈6 µm > 껍질 두께 **100–1000 nm** → *"difficult to fold and incorporate"* · 투입 VGCF 를 2 배로 (2 → 4 wt%) 해도 순 VGCF/SE 질량비 **8.9 → 9.8 × 10⁻²** (SI 그림 S1) · 순 VGCF 최대 ≈1.6 wt% (SE 16 wt%) | [인쇄] p.4 · SI p.1–2 · 그림 4 · S1 |
| ⑥ 전기화학 (반쪽셀 · 0.1 C = 1/10 × 1.6 mA cm⁻²) | 첫 방전 SM **137.0** · CP **81.7** · CP-AB **142.3** · CP-VGCF **147.8** mAh g⁻¹ [판독 벡터 · 그림 7a] (본문 CP "ca. 87") · 첫 쿨롱 효율 **82.6 · 77.0 · 75.7 · 71.3 %** [인쇄 · 판독 재현 82.5 · 77.0 · 75.7 · 71.3] · 2 C 방전 **63.9 · 26.4 · 97.7 · 30.7** · 2 C 충전 **35.1 · 0.0 · 51.0 · 11.3** [판독] · 1.0 C 50 사이클 유지 **32.2 · 49.3 · 92.9 · 54.7 %** [인쇄] (SM 은 판독 29.9 % — §3-9) | [인쇄] p.6 · p.8 · [판독] 그림 7 · 10 |
| ⑦ EIS (SOC 50 %) · CV | 등가 회로 R–(R∥C) = Rs · (R∥C) = Rct · ((R + W)∥C) = R_NE · 그림 안 표: Rs SM **94.5** · CP **79.0** · CP-AB **70.5** · CP-VGCF **63.1** · Rct **49.9 · 79.5 · 40.4 · 32.6** (Ω — 단위는 축) · CV 0.05 mV s⁻¹: CP-AB 산화 봉우리 **0.53 mA @ 3.95 V** · CP-VGCF 는 봉우리 없이 **≈0.25 mA 평탄** (3.9–4.25 V) [판독] | [인쇄 그림 안] 그림 8 · [판독] 그림 9 |
| ⑧ 저자 해석 | ① CP 의 낮은 σ_e · 용량 = 껍질이 AM–AM 접촉을 막아 *"electrochemically inert AM particles"* (p.6) ② SM 의 높은 Rs = *"the coalescence of SE was not promoted because the compression stress was not uniformly acted upon by the non-uniform distribution of AM and SE particles"* (p.7 · **응력 측정 없음 · 가설**) ③ CP-VGCF 의 약한 CV = AM 으로의 전자 공급 부족 (p.7) ④ 코어–셸이 AM 부피 변화의 영향을 줄여 유지율 ↑ · SM 25 사이클 뒤 급락 = *"mechanical degradation [36]"* · *"peeling"* (p.8 · 측정 없음) | [인쇄] p.6–8 |
| ⑨ 계산 모델 · DEM | **없음** (본문 · SI 에 DEM · simulation · model 0 회 — 'model' 2 회는 참고문헌 제목) | 원문 낱말 셈 |

⛔ **한정어 (떼지 말 것)**: ① 재료 = **NCM523 + LiNbO₃ 1 wt%** · Li₆PS₅Cl (Mitsui · 0.7 µm · 2.02 mS cm⁻¹) — 우리 NCM811 · LPSCl 과 **CAM 이 다르다** ② σ 는 **360 MPa 로 누른 80 mg 압분체의 EIS 두 반원 맞춤** (이온 차단 셀) — 두께 · 지름 · 측정 때 압력 · 맞춤 회로 [미확인] · N = 3 (SD 큼: σ_ion 은 네 시료가 오차 막대 안에서 겹친다) ③ 같은 "SE 16–17 wt%" 라도 CP 류는 **순 (net)** 값이고 투입은 24–25 wt% — 표 1 셋은 SE 의 37–42 % (SI 의 VGCF 2 wt% 시료 46 %) 가 장치 벽에 붙어 빠졌다 [카드 산술 · AM 을 추적자로] ④ 반쪽셀 Rs 는 **분리막 (SE 80 mg) 을 포함** — Rs 차이를 양극 SE 합체로 읽은 것은 저자 해석이고, 같은 논문의 이온 차단 σ_ion 은 유의차가 없다 ⑤ 기공 · 두께 · 밀도 · 압력별 · 탈압 · 응력 · 손상의 측정이 **하나도 없다** ⑥ 0.1 C 첫 방전 CP 는 본문 "ca. 87" ↔ 그림 7a 81.7 · SM 유지율 본문 32.2 % ↔ 그림 10 29.9 % (§3-9).
⇒ **절대값 전이: 0 건.**  전이되는 것은 **방향과 크기 자릿수** (같은 순 조성에서 비전도 SE 껍질 → 압분체 σ_e ×1/21 · σ_ion 거의 그대로 · 껍질 안 탄소 (AB) 와 입자 사이 탄소 (VGCF) 의 역할이 다르다) 와 **관측량 구분** (층 σ_e ↔ AM 으로의 전자 공급) · **조성 보고 꼴** (투입 ↔ 순) 뿐이다.

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-81 의 '왜' 칸)

의도 원문: *"코팅 활물질 — '★ 코팅 입자의 전자 경로 문제 (Xs 0.3 붕괴) 를 도전재로 푸는 같은 그룹 후속' (kawaguchi2023) · '코팅 입자 + 도전재 (이 논문의 혼합 전도 껍질과 같은 질문)' (kissel2026) · 고강도 혼합 코팅 (frankenberg2025)"* (가리킨 카드 = kawaguchi2023 L288 · kissel2026 L508 · frankenberg2025 L363)

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| "코팅 입자의 전자 경로 문제" | **채움** | p.2 서론 *"although the composite particles can form a large AM-SE contact interface, the SE coating layer with electrical non-conductance can inhibit electron transfer to the AMs"* · 실측: σ_e CP **1.36 × 10⁻⁶** vs SM **2.84 × 10⁻⁵ S cm⁻¹** (×1/21 [판독 그림 6b · 360 MPa 압분체 · EIS]) · 첫 방전 CP 81.7 vs SM 137.0 mAh g⁻¹ [판독 그림 7a · 0.1 C · 298 K] · Rct CP 79.5 vs SM 49.9 Ω [인쇄 그림 8 · SOC 50 %] · 저자: *"suppressed contact between AM particles, resulting in the formation of electrochemically inert AM particles"* (p.6) |
| "(Xs 0.3 붕괴)" | **없음** | 이 논문은 SE 몫을 바꾸지 않았다 (순 SE 15.8–16.9 wt% 한 수준 · 표 1).  "Xs 0.3 붕괴" (1.8–11.0 mAh g⁻¹) 는 **kawaguchi2023 자신의 결과** (Li₃PS₄ · NCM111 · 껍질 5.6 wt% + 자유 SE) 다.  이 논문의 CP 는 붕괴가 아니라 **부분 손실** (첫 방전 SM 의 0.60 배 [카드 산술 81.7/137.0]) |
| "를 도전재로 푸는" | **일부** | **AB = 용량 · 율속 · 수명 · Rct 를 모두 푼다** (142.3 mAh g⁻¹ · 2 C 97.7 · 92.9 % · Rct 40.4 Ω) — 그러나 CP-AB 의 압분체 σ_e (6.37 × 10⁻⁶) 는 **SM 의 0.22 배로 남는다** (p.5 *"the formation of electron transfer paths using AB had smaller contribution for electrical conductivity than the contact inhibition of AMs by SE coating"*) · **VGCF = σ_e 는 SM 의 17.6 배로 올리지만 율속 (2 C 30.7) · CV · 수명 (54.7 %) 은 못 푼다** (p.6–8) ⇒ "도전재" 가 아니라 **"껍질 안에 들어가는 도전재"** 가 푼다 (저자 결론 p.8) |
| "같은 그룹 후속" | **일부 (같은 그룹 ✓ · '후속' ✗)** | 같은 그룹 ✓ (Osaka Metropolitan Univ. · 교신 Nakamura · Hayakawa · Ohsaki · Watano 가 kawaguchi2023 공저자) · 같은 Nara 장치 · 같은 13,000 rpm · 5 min ✓.  그러나 **이 논문이 먼저다**: 접수 2022-09-16 · 온라인 2022-11-17 (p.1) ↔ kawaguchi2023 온라인 2023-11-01 [다른 카드: kawaguchi2023 L15] · kawaguchi2023 가 이 논문을 ref 26 으로 **인용한다** → '후속' 이 아니라 **선행** (카드 문제 1) |
| "코팅 입자 + 도전재 (이 논문의 혼합 전도 껍질과 같은 질문)" | **채움** (낱말 한정) | CP-AB = SE 껍질 안에 AB 가 든 입자 = 이온 · 전자를 함께 나르는 껍질 (p.8 *"well-percolated electron/lithium-ion transfer paths to the AM particles"*) — 원문은 **"mixed conducting" 이라는 낱말을 쓰지 않는다** · 차이 [다른 카드 · kissel2026]: Kissel = Li₃InCl₆ (할라이드) + CB · 메카노퓨전 · TEM 껍질 ≈5 nm ↔ 이 논문 = Li₆PS₅Cl + AB · 충격 블렌딩 · 껍질 100–1000 nm |
| "고강도 혼합 코팅 (frankenberg2025)" | **일부** | 이 논문의 공정 = **건식 충격 블렌딩 (회전자 13,000 rpm · 순환관 · 5 min)** 코팅 — 회전자 지름 · 선속도 · 에너지 [미확인] · frankenberg2025 L363 은 [63] (이 논문) 과 [64] (Hayakawa 2022 *Adv. Powder Technol.* 33, 103705 = **고전단 혼합기** 건식 혼합 = 이 논문 ref [10]) 을 한 줄로 묶어 "고강도 혼합 코팅" 이라 적었다 — 혼합기 쪽은 [64] 의 내용이다 |

**가리킨 카드의 2 차 인용 대조** (카드 줄은 고치지 않는다 — 다른 점은 카드 문제로 보고):

| 카드 (줄) | 옮긴 값 · 표기 | 원문 | 판정 |
|---|---|---|---|
| `kawaguchi2023_…` L288 (ref 26) | 서지 *"E. Hayakawa, H. Nakamura, S. Ohsaki, S. Watano, Design of … lithium-ion batteries, J. Power Sources 555 (2023) 232379"* · *"★ 코팅 입자의 전자 경로 문제 (이 논문 Xs 0.3 붕괴) 를 도전재로 푸는 같은 그룹 후속"* | 서지 ✓ (p.1) · 내용 방향 ✓ · **'후속' ✗ (이 논문이 1 년 먼저)** · 도전재가 "푸는" 것은 AB 에 한정 (VGCF 는 율속 · 수명 못 품 · AB 도 압분체 σ_e 는 SM 아래) | **일부** |
| `kawaguchi2023_…` L287 (ref 25) | *"Hayakawa … Characterization of solid-electrolyte/active-material composite particles with different surface morphologies … Adv. Powder Technol. 33 (3) (2022) 103470"* | 이 논문 ref [16] = 같은 제목 · *Adv. Powder Technol.* 33 (2022) 103470 ✓ (호 "(3)" 은 이 논문 목록에 없음) | **채움** |
| `kissel2026_…` L508 (ref 63) | 서지 *"Hayakawa, E., Nakamura, H., Ohsaki, S. & Watano, S. Design of … J. Power Sources 555, 232379 (2023)"* · *"코팅 입자 + 도전재 (이 논문의 혼합 전도 껍질과 같은 질문)"* | 서지 ✓ · 질문 ✓ (AB 든 껍질) | **채움** |
| `frankenberg2025_…` L363 (refs 63 · 64) | *"E. Hayakawa, … J. Power Sources 2023, 555, 232379. · E. Hayakawa, … Adv. Powder Technol. 2022, 33, 103705."* · *"고강도 혼합 코팅 (오사카 그룹)"* | [63] 서지 ✓ · [64] = 이 논문 ref [10] *"Dry mixing of cathode composite powder for all-solid-state batteries using high shear mixer, Adv. Powder Tech. 33 (2022), 103705"* ✓ · 이 논문 자체는 고전단 혼합기가 아니라 충격 블렌딩 코팅 | **일부** (두 논문을 한 설명으로 묶음) |
| 후보 표 N-81 서지 | *"E. Hayakawa, H. Nakamura, S. Ohsaki, S. Watano, Design of … J. Power Sources 555 (2023) 232379"* | ✓ (DOI 10.1016/j.jpowsour.2022.232379 · 온라인 2022 · 권 2023) | **채움** |

⇒ **의도 대조 결과: 일부** — 코팅 입자의 전자 경로 문제 · 도전재 껍질 (AB) 은 **채움**; "Xs 0.3 붕괴" 는 **없음** (kawaguchi2023 자신의 결과); "도전재로 푼다" 는 **AB 에 한정** (VGCF 는 압분체 σ_e 만 올리고 율속 · 수명은 못 푼다 · AB 도 σ_e 는 SM 아래); "후속" 은 **시간 순서가 반대** (이 논문이 선행); "고강도 혼합" 은 이 논문이 아니라 짝 논문 [10] (= frankenberg [64]) 의 내용.

---

## 1. 한 줄 요약
같은 순 조성 (NCM523 : Li₆PS₅Cl ≈ 83 : 17 wt%) 에서 **막자 혼합 (SM)** 과 **건식 충격 블렌딩 코어–셸 (CP)** · **AB 를 넣은 코어–셸 (CP-AB)** · **VGCF 를 넣은 코어–셸 (CP-VGCF)** 넷을 견준다 — 입자 단면 SEM/EDX 로 도전재의 자리를, 360 MPa 압분체 EIS 로 σ_ion · σ_e 를, Li–In 반쪽셀로 첫 사이클 · dQ/dV · 율속 (0.1–2 C) · EIS · CV · 50 사이클을 본다.
비전도 SE 껍질은 AM–AM 전자 접촉을 막아 σ_e 를 1/21 로 떨어뜨리고, **껍질 두께보다 작은 AB 만 껍질 안에 들어가** AM 표면까지 전자를 나르며 (최고 율속 · 수명), 껍질보다 긴 VGCF 는 입자 사이에 머물러 층 σ_e 만 올린다.
저자 결론: *"AB is a more suitable material for improving the performance of ASSLIB with composite particles than VGCF"* (p.8).

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| E. Hayakawa · **H. Nakamura\*** · S. Ohsaki · S. Watano (Osaka Metropolitan Univ. 화공) | *J. Power Sources* 555 (2023) 232379 (온라인 2022-11-17) | 10.1016/j.jpowsour.2022.232379 | **Li₆PS₅Cl** (Mitsui · 개수 중앙 0.7 µm · 2.02 mS cm⁻¹) + **NCM523** (Sumitomo · LiNbO₃ 1 wt% · 개수 중앙 4.3 µm) + AB (Denka Li-100) / VGCF (Showa Denko) · Li–In 대극 | 실험 (건식 충격 블렌딩 코팅 · SEM/EDX · 순 조성 · 이온 차단 셀 EIS · 반쪽셀 전기화학 · CV) — 계산 없음 |

- **1저자 메모와의 대조**: 저자 넷 · 제목 · 학술지 · 권 555 · 논문 번호 232379 · 2023 · DOI — **같다** (PDF 첫 쪽 · 쪽 머리).  덧붙임 ① 온라인 출판은 **2022-11-17** (권 연도 2023) ② 교신 = Nakamura.
- **글의 꼴**: 서론 → 2 실험 (2.1 재료 · 2.2 코팅 · 2.3 분석 · 2.4 이온 차단 셀 σ · 2.5 반쪽셀) → 3.1 복합 입자 → 3.2 복합 양극 → 3.3 반쪽셀 → 4 결론 → 참고문헌 36.  그림 10 · 표 1 · **번호 식 0** (σ 계산식도 인쇄 안 됨) / SI: 본문 문단 1 · 그림 S1 (SEM · C 지도 + 표) · 그림 S2 (전형적 나이키스트 + 등가 회로) · 참고문헌 0.
- 그룹 맥락: 같은 장치 · 같은 조건을 Kawaguchi 2017 [13] (Na₂SO₄ 모델 물질로 공정 창) → Nakamura 2020 [15] (Li₃PS₄ 실제 코팅) → Hayakawa 2022 [16] (껍질 표면 형태) → **이 논문 (도전재)** → Kawaguchi 2023 (DOE · 이 논문을 인용) 으로 이어 썼다 · 고전단 혼합기 쪽은 Hayakawa 2022 [10] (*Adv. Powder Technol.* 33, 103705) · 흑연 음극 코팅은 Iwao 2022 [19].

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. ★ 재료 · 공정 · 조성 (p.2–4 · 표 1 · 그림 1 · 2 · `fig_1.png` · `fig_2.png` · `tab_1.png` · `txt_p2_materials_ncm523_lpscl_ab_vgcf.png` · `txt_p2_premix_dry_coating_13000rpm.png` · `txt_p2_net_mass_fraction_uvvis_tgdta.png` · `txt_p3_table1_se_wall_adhesion.png`)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| AM | LiNi₀.₅Co₀.₂Mn₀.₃O₂ (**NCM523**) · Sumitomo Metal Mining · **LiNbO₃ 1 wt%** 선코팅 · 개수 중앙 지름 **4.3 µm** · SEM (그림 1a) = 수백 nm 일차 입자가 뭉친 둥근 2차 입자 (다결정) | [인쇄] p.2 · [판독] 그림 1a (눈금 5 µm) |
| SE | Li₂S–P₂S₅–LiCl (**Li₆PS₅Cl** argyrodite) · Mitsui Mining & Smelting · 개수 중앙 **0.7 µm** · 이온 전도도 **2.02 mS cm⁻¹** (측정 조건 [미확인]) · SEM (그림 1b) = 모난 ≈0.2–1.5 µm 조각 + 잔 입자 | [인쇄] p.2 · [판독] 그림 1b (눈금 1 µm) |
| 도전재 | **AB** = Denka Black Li-100 (Denka) · 일차 입자 **≈35 nm** (p.4) · **VGCF** (Showa Denko) · 섬유 지름 **≈150 nm** · 길이 **c.a. 6 µm** (p.4) | [인쇄] p.2 · p.4 |
| 예비 혼합 | AM + SE (+ CA) 를 **헵테인** 속 초음파 균질기 (UH-50) 로 분산 → 증발기 (Smart Evaporator C1) 로 농축 → **−0.9 Pa (게이지) · 393 K** 감압 건조 · CA 는 초음파 중 투입 | [인쇄] p.2 |
| 코팅 장치 | **건식 충격 블렌딩 장치 (Nara Machinery)** — 냉각 재킷 챔버 · 날 달린 회전자 · 순환관 · 배출 밸브 · 회수 용기 · 백 필터 (그림 2) · **투입 10.0 g · 13,000 rpm · 5 min** · 조건은 [13,16] 에서 최적화 · Ar 글러브박스 (이슬점 **< 193 K**) · 회전자 지름 · 선속도 · 충격 에너지 · 온도 [미확인] | [인쇄] p.2 · 그림 2 |
| 비교 시료 SM | 막자 혼합 (mortar–pestle) · SE 몫을 다른 시료와 비슷하게 (84.0 : 16.0) · 혼합 시간 [미확인] | [인쇄] p.3 · 표 1 |
| 순 조성 측정 | 에탄올에 SE 녹임 → 13,000 rpm · 60 min 원심 → 노란 윗물 (SE) UV–vis **235 nm** 흡광 · 침전 (AM + CA) 333 K 건조 → TG–DTA 로 CA 몫 | [인쇄] p.2 |
| **표 1 (wt%)** | 투입 AM : SE : CA → 순 AM : SE : CA — **SM** – → **84.0 : 16.0 : –** · **CP** 75.5 : 24.5 : – → **83.1 : 16.9 : –** · **CP-AB** 74.0 : 24.0 : 2.0 → **81.4 : 15.8 : 2.79** · **CP-VGCF** 71.0 : 25.0 : 4.0 → **81.7 : 16.6 : 1.62** | [인쇄] 표 1 |
| SE 가 줄어든 까닭 | *"owing to the SE adhesion to the inner wall of the device"* (p.3) · VGCF 도 벽 부착 (SI p.1) | [인쇄] p.3 · SI p.1 |
| ★ 손실 크기 [카드 산술 · AM 을 추적자로 둠 (AM 은 벽에 안 붙는다는 가정 — 원문에 손실 질량 없음)] | 남은 SE = (순 SE/AM) ÷ (투입 SE/AM): CP **62.7 %** · CP-AB **59.8 %** · CP-VGCF **57.7 %** · SI 의 VGCF 2 wt% 시료 **54.4 %** / 남은 CA: AB **126.8 %** (> 100 % = AB 가 AM 보다 덜 잃었거나 측정 오차 — 원문 설명 없음) · VGCF **35.2 %** (4 wt% 투입) · **57.8 %** (2 wt% 투입) | [카드 산술] 표 1 · SI 표 |
| ★ 껍질 두께 어림 [카드 산술 · 가정: 모든 SE 가 고른 치밀 껍질 · AM = 지름 4.3 µm 구 · ρ_SE **1.64** (랩 표준 진밀도) · ρ_NCM523 **4.72** (다른 카드: `siroma2016_…` 원문의 가정 밀도)] | CP: V_SE/V_AM = (16.9/1.64)/(83.1/4.72) = **0.585** → 바깥 반지름 ×1.166 → 껍질 **≈0.36 µm** (CP-AB ≈0.34 · CP-VGCF ≈0.36 · ρ_SE 1.87 이면 CP ≈0.32 µm) — 원문 SEM 의 **100–1000 nm** 안 · SE 입자 지름 0.7 µm 의 ≈반 | [카드 산술] |
| 고체 부피비 [카드 산술 · 같은 가정] | SE/(AM+SE) = SM **0.354** · CP **0.369** · CP-AB **0.358** · CP-VGCF **0.369** (AM 0.63–0.65 · CA 무시) | [카드 산술] |
| AM 한 개당 SE 입자 수 [카드 산술 · 개수 중앙 지름끼리] | 껍질 부피 0.585 × (π/6)(4.3)³ = 24.4 µm³ ÷ (π/6)(0.7)³ = 0.180 µm³ → **≈136 개** | [카드 산술] |

### 3-2. ★ 복합 입자의 형태 · 도전재 자리 (p.4 · SI p.1–2 · 그림 3 · 4 · S1 · `fig_3.png` · `fig_4.png` · `fig_4a/b/c.png` · `fig_S1.png` · `txt_p4_*` · `txt_si_p1_vgcf_doubling.png`)
- **그림 3 (입자 SEM + Ni · S 지도 · ×10.0k · 10 kV)**: SM = AM 과 SE 가 따로 놓임 (S 지도가 AM 둘레를 다 덮지 않음) · CP · CP-AB · CP-VGCF = Ni 와 S 지도가 겹침 → *"particles comprised composite particles with the AM particles covered with SE particles"* (p.4) · CP-VGCF 표면에 섬유가 보인다 [판독].
- **그림 4 (단면 SEM + C 지도 · ×15.0k)**: 흰 점선 = AM/SE 경계 · CP = 탄소 대비 없음 · **CP-AB = 껍질 자리 탄소가 AM 심보다 강함 (흰 화살표 5)** · **CP-VGCF = 섬유 · 탄소 덩이가 입자 밖 (SEM 빨간 화살표 4 · C 지도 빨간 3) · 껍질 쪽 흰 화살표 1** — *"the ABs were incorporated into the SE coating layer … the VGCFs in CP-VGCF were more likely to be placed outside the composite particles"* (p.4).  ⚠ 단면의 AM 은 속에 빈 곳 · 줄무늬가 보인다 (이온빔 단면 · 다결정) — 원문은 AM 내부 공극 · 균열을 다루지 않는다 [카드 해석].
- **기전 (저자 · p.4)**: VGCF 지름 ≈150 nm > AB ≈35 nm · VGCF 길이 c.a. 6 µm > 껍질 두께 100–1000 nm → *"it was difficult to fold and incorporate the VGCF into the SE coating layer compared to AB"* · 결론 p.8: *"AB was more effectively incorporated into the SE coating layer because the particle size of AB was smaller than that of the SE coating layer"*.
- **SI 그림 S1 (VGCF 2 vs 4 wt%)**: 투입 NCM : SE : CA = 74 : 24 : 2 → 순 **83.9 : 14.8 : 1.31** · 71 : 25 : 4 → 순 **81.7 : 16.6 : 1.62** · VGCF/SE 투입 **8.3 × 10⁻² → 1.6 × 10⁻¹** (2 배) · 순 **8.9 × 10⁻² → 9.8 × 10⁻²** (≈같음) — *"even if VGCF increased further, an increase in the VGCF fraction in the SE coating layer was not expected"* (SI p.1) · 본문 p.4: 순 VGCF 최대 ≈1.6 wt% (SE 16 wt% 일 때) → 그래서 표 1 의 넷을 견줬다.
- ⚠ **도전재 순 몫이 다르다**: AB 2.79 · VGCF 1.62 wt% (×1.7) — 두 도전재 비교는 같은 양의 비교가 아니다 (원문은 "lower CA fraction" 으로만 언급 · p.6).

### 3-3. ★ 복합 양극 σ_ion · σ_e (p.2–5 · 그림 5 · 6 · `fig_5.png` · `fig_6.png` · `fig_6a.png` · `fig_6b.png` · `txt_p2_ion_blocking_cell_360mpa.png` · `txt_p3_eis_two_semicircles_thickness_area.png` · `txt_p4_conductivity_order_5x.png` · `txt_p5_vgcf_18x_interparticle_paths.png`)
- **방법** [인쇄 p.2–3]: 이온 차단 셀 [16,23,24] = *"only a composite cathode with 80 mg of composite particles pressed at 360 MPa"* · SP-200 · 10 mV · **10 mHz–7 MHz · 298 K** · 나이키스트의 **두 반원을 맞춰** 전자 · 이온 저항 → *"thickness of the composite cathode, and electrode area"* 로 σ.  셀 지름 · 집전체 · 가압 시간 · 측정 때 압력 · 두께 값 · 맞춤 회로 [미확인] (같은 축 방법의 원전 = `siroma2016_…` [23] · `asano2017_…` [24] — 정본 카드 있음).
- **그림 5 (압분체 단면 SEM + C 지도)**: 밝은 회색 = AM · 어두운 회색 = SE (p.4) · CP 류 = SE 가 AM 둘레에 놓여 *"well-percolated lithium-ion transfer paths"* · CP-AB = AB 가 AM 둘레 (5c) · CP-VGCF = AM 가까이 VGCF 가 적다 (5d).  ⚠ 캡션은 (d) 를 "(c) CP-VGCF" 로 잘못 적었다 · 단면의 검은 공극은 정량하지 않았다 [카드 해석].
- **그림 6 판독 (벡터 경로 좌표 · digitized.csv fig6a · fig6b)**:

| 시료 | σ_ion (10⁻⁵ S cm⁻¹) 평균 [막대 끝] | σ_e (S cm⁻¹) 평균 [막대 끝] | σ_e/σ_ion [카드 산술] | f_ion = σ_ion/2.02 mS cm⁻¹ [카드 산술] |
|---|---|---|---|---|
| SM | **3.52** [2.10–4.95] | **2.84 × 10⁻⁵** [1.88–3.78 × 10⁻⁵] | 0.81 | 0.017 |
| CP | **3.21** [2.18–4.25] | **1.36 × 10⁻⁶** [1.23–1.47 × 10⁻⁶] | 0.042 | 0.016 |
| CP-AB | **3.78** [3.09–4.47] | **6.37 × 10⁻⁶** [3.08–9.63 × 10⁻⁶] | 0.17 | 0.019 |
| CP-VGCF | **4.61** [2.54–6.67] | **5.02 × 10⁻⁴** [3.33–6.66 × 10⁻⁴] | 10.9 | 0.023 |

  보정: (a) 선형 틀 아래 592.43 pt = 0 · 위 486.84 pt = 10 (1 단위 눈금) · (b) 로그 10⁻⁶ · 10⁻⁵ · 10⁻⁴ · 10⁻³ = 592.83 · 557.67 · 522.45 · 487.24 pt · 표지 중심 = 원 경로 테두리 상자 중심 · 오차 막대 = 캡의 수평선 y.  (b) 의 막대는 로그 축 위에서 위아래 같은 **선형** SD 다 (SM ±0.95 × 10⁻⁵ · CP-VGCF ±1.65 × 10⁻⁴).
- **비 (본문 ↔ 판독)**: CP-AB/CP **4.7** (본문 "approximately 5 times") · CP-VGCF/SM **17.6** (본문 "approximately 18 times") · **SM/CP 21.0** · CP-AB/SM **0.22** · CP-VGCF/CP **370** · σ_ion CP/SM **0.91** · CP-AB/SM 1.07 · CP-VGCF/SM 1.31 (모두 SD 안) [카드 산술].
- 저자 읽기 [인쇄 p.4–5]: σ_ion 은 *"no significant difference … because all samples had similar SE mass fractions"* · σ_e 순서 CP-VGCF > SM > CP-AB > CP · CP < SM = *"the contact between the AM particles was suppressed by the SE coating layer"* · CP-AB < SM = *"the formation of electron transfer paths using AB had smaller contribution for electrical conductivity than the contact inhibition of AMs by SE coating"* · CP-VGCF 최고 = *"electron transfer paths formed by the VGCFs in the interparticle space between the composite particles"*.

### 3-4. 반쪽셀 첫 사이클 · dQ/dV (p.3 · p.6 · 그림 7a · 7b · `fig_7.png` · `fig_7a.png` · `fig_7b.png` · `txt_p3_halfcell_20_360_90mpa.png` · `txt_p3_test_protocol_1c_cutoffs_cycles.png` · `txt_p6_cp_87_ce_side_reaction_3p6v.png`)
- **셀** [인쇄 p.3]: SE 80 mg 를 10 mm 다이에서 **20 MPa** 수 초 → 복합 입자 **10 mg** 넣고 **360 MPa 5 min** (2 층 펠릿) → Li–In 시트 **90 MPa 5 min** · 10 mm 펠릿 · SUS 막대 집전체 둘 · BTS-2004H · CC · **298 K** · 첫 3 사이클 **0.1 C (1C = 1.6 mA cm⁻²)** · 차단 **2.38/3.63 V vs Li–In (3.0/4.25 V vs Li/Li⁺)** · 율속 0.1 · 0.2 · 0.5 · 1.0 · 2.0 C (반대 반응은 0.1 C) · 율속 뒤 SOC 50 % EIS · 그 뒤 50 사이클 (방전 1.0 C · 충전 0.1 C) · 끝에 CV 0.05 mV s⁻¹ (3.0–4.25 V).
  [카드 산술]: AM 면 로딩 = 10 mg × 순 AM ÷ 0.785 cm² = **10.4–10.7 mg cm⁻²** → 1C ≈ **150–154 mA g⁻¹** (원문 g⁻¹ 기준 1C 값 [미확인]).
- **그림 7a 판독 (벡터 곡선 끝 · digitized.csv fig7a)**: 충전 끝 SM **166.1** · CP **106.1** · CP-AB **188.1** · CP-VGCF **207.2** / 방전 끝 **137.0 · 81.7 · 142.3 · 147.8 mAh g⁻¹** → 쿨롱 효율 **82.5 · 77.0 · 75.7 · 71.3 %** [카드 산술] ↔ 본문 **82.6 · 77.0 · 75.7 · 71.3 %** (p.6) ✓.  ⚠ 본문 *"The initial discharge capacity at 0.1 C of the cell prepared with CP (ca. 87 mAh g⁻¹)"* ↔ 그림 7a 방전 끝 **81.7** (효율 77.0 % 와 맞는 쪽은 81.7) · 그림 7c 0.1 C 방전 표지는 89.1 (다른 때 · p.6 의 주의) — §3-9.
- **충전 초기 3.6 V 도달 (그림 7a · 벡터)**: CP **0.36** · SM **0.79** · CP-AB **10.6** · CP-VGCF **15.8 mAh g⁻¹** [판독] ↔ 본문 *"those prepared with CAs … required a capacity of 10–15 mAh g⁻¹ to increase the potential to over 3.6 V"* · VGCF 쪽이 더 큼 ✓ — 저자: SE–CA 부반응 (CA 표면 산소 관능기 · 잘 이어진 전자망 [21,25–27]) · VGCF 는 1 차원 꼴이 전자 공급을 쉽게 해서 [26].  CP-AB 충전 곡선의 첫 점은 축 바닥 (2.0 V) 아래다 (경로 첫 점 1.61 V · 틀에 잘림 [판독] · 원문 언급 없음).
- **그림 7b (3 번째 사이클 dQ/dV · 그림 안 표)** [인쇄]: V_anodic / V_cathodic / ΔV — SM **3.781 / 3.710 / 0.071** · CP **3.796 / 3.722 / 0.074** · CP-AB **3.771 / 3.727 / 0.044** · CP-VGCF **3.774 / 3.710 / 0.064** V (ΔV = 두 값의 차 ✓ [카드 산술]) · 봉우리 높이 [판독 · 잡음 섞인 선의 극값]: 산화 SM 613 · CP 396 · CP-AB 616 · CP-VGCF 555 · 환원 −531 · −296 · −542 · −499 mAh g⁻¹ V⁻¹ · 벡터 극값 위치는 표의 전위와 셋째 자리까지 같다.
- 저자 읽기 [인쇄 p.6]: SM ≈ CP 분극 · CP-AB 분극 최소 · CP-VGCF 는 ΔV 가 CP-AB 보다 크고 봉우리가 낮고 넓다 → *"a more non-uniform electrical network of CP-VGCF"* · CP-AB 가 σ_e 는 SM 아래인데 용량은 SM 위 = *"increasing the area of AM-SE contact interface by the dry coating"*.

### 3-5. 율속 (p.6 · 그림 7c · 7d · `fig_7c.png` · `fig_7d.png`)
판독 (벡터 표지 중심 · mAh g⁻¹ · 0.1 / 0.2 / 0.5 / 1 / 2 C):

| 시료 | 방전 (그림 7c) | 충전 (그림 7d) | 2 C/0.1 C 방전 · 충전 [카드 산술] |
|---|---|---|---|
| SM | 134.5 · 127.8 · 116.9 · 102.7 · **63.9** | 133.5 · 129.4 · 117.9 · 96.2 · **35.1** | 47.5 % · 26.3 % |
| CP | 89.1 · 84.1 · 70.7 · 47.6 · **26.4** | 91.1 · 86.7 · 73.4 · 48.4 · **0.0** | 29.6 % · 0 % |
| CP-AB | 142.9 · 136.8 · 126.1 · 115.7 · **97.7** | 143.0 · 139.2 · 128.5 · 110.7 · **51.0** | 68.4 % · 35.7 % |
| CP-VGCF | 142.9 · 133.9 · 105.6 · 66.9 · **30.7** | 140.2 · 124.5 · 77.1 · 38.6 · **11.3** | 21.4 % · 8.1 % |

- 본문 [인쇄 p.6]: 낮은 율속에서는 CP 를 빼고 차이가 없다 · AB 가 2.0 C 방전 · 충전 용량을 크게 올림 → 최고 율속 · VGCF 는 0.1 C 용량만 올리고 *"did not contribute to the improvement of the discharge and charge capacity at higher C-rates"* · 그림 7c/7d 의 0.1 C 가 7a 와 조금 다른 것은 측정 때가 달라서 (원문).
- ⚠ 충전 쪽이 방전보다 율속이 훨씬 나쁘다 (2 C 충전 CP 0 · CP-VGCF 11.3 ↔ 방전 26.4 · 30.7 [판독]) — 원문은 이 비대칭을 다루지 않는다.

### 3-6. EIS (SOC 50 %) · 등가 회로 (p.6–7 · 그림 8 · SI 그림 S2 · `fig_8.png` · `fig_S2.png` · `txt_p6_eis_frequency_assignment.png` · `txt_p7_rs_se_coalescence_compression_stress.png`)
- **배정** [인쇄 p.6–7]: 고주파 (> 100 kHz) = 분리막 + 양극 층 SE 저항 **Rs** (첫째 + 둘째 저항 성분의 합) · 중주파 (100 kHz–100 Hz) = 양극 전하 이동 **Rct** [28,29] · 저주파 (100 Hz–0.2 Hz) = Li–In 음극 확산 **R_NE** · < 0.2 Hz 직선 = AM 속 확산 Warburg [30–33] · 등가 회로 = R – (R∥C) [Rs] – (R∥C) [Rct] – ((R + W_o)∥C) [R_NE] (그림 8 · S2).
- **그림 8 안 표** [인쇄]: Rs **94.5 · 79.0 · 70.5 · 63.1** · Rct **49.9 · 79.5 · 40.4 · 32.6** (SM · CP · CP-AB · CP-VGCF · 단위는 축의 Ω).  판독: 가장 왼쪽 표지 Z′ SM 80.6 · CP 69.8 · CP-AB 62.3 · CP-VGCF 63.1 Ω · ⚠ 그림 8 은 가로 1.0225 pt/Ω · 세로 0.878 pt/Ω 로 **등척이 아니다** (반원이 납작해 보인다) · 캡션의 "SM, **CA**, CP-AB" 는 CP 의 오기로 보인다.
- **SI 그림 S2 (전형적 나이키스트 · 어느 시료인지 [미확인])**: 100 kHz 화살표 Z′ ≈68 · 100 Hz ≈85 · 0.2 Hz ≈105 Ω [판독 · 화살표 위치].
- ★ **저자 해석 (p.7)**: Rs 차이는 분리막이 같은 공정이라 양극 SE 저항 차 → SM = *"the coalescence of SE was not promoted because the compression stress was not uniformly acted upon by the non-uniform distribution of AM and SE particles in the cathode"* · CP 류 = *"in a state of already promoted coalescence of SE by the dry coating process … the compression stress was uniform"* → 낮은 Rs.  **⚠ 응력 · 합체 · 접촉 면적의 측정은 없다** · 같은 논문의 이온 차단 σ_ion 은 SM 3.52 ↔ CP 3.21 (CP 가 오히려 낮음 · SD 안) 이라 Rs 해석과 **방향이 맞지 않는다** [카드 해석] · Rs 는 분리막을 포함 (같은 그룹 kawaguchi2023 카드도 같은 한정 [다른 카드]).
- Rct [인쇄 p.7]: CP > SM (비전도 껍질) · CP-AB · CP-VGCF < CP (도전재) · < SM (넓은 AM–SE 계면) · *"formation the large AM-SE contact interface and well-percolated electron transfer paths had a greater impact on Rct than the electrical conductivity in the cathode"*.  CP-VGCF 는 내부 저항이 가장 낮은데 율속이 나쁘다 → *"could not be explained by Rs and Rct"* → CV 로.

### 3-7. CV (p.7–8 · 그림 9 · `fig_9.png` · `txt_p7_conductivity_not_electron_supply.png`)
- 판독 (벡터 · 0.05 mV s⁻¹ · 3.0–4.25 V · 전류 mA (질량 정규화 아님)): CP-AB 산화 최대 **0.530 mA @ 3.946 V** · 환원 최소 **−0.392 mA @ 3.620 V** (봉우리 간격 0.33 V [카드 산술]) / CP-VGCF 산화 = 봉우리 없이 **0.244–0.248 mA** 평탄 (3.9–4.2 V) · 환원 최소 **−0.197 mA @ 3.620 V** [판독].
- 저자 [인쇄 p.7]: 같은 AM · SE 이고 CP-VGCF 의 Rct 가 더 낮으므로 약한 산화환원 전류 = AM 으로의 Li⁺ 또는 전자 공급 제한 · σ_ion 과 Li⁺ 경로는 둘이 같음 → 전자 쪽 · ★ *"these electrical conductivities describe the ease with which the electrical current can be made to flow through the entire cathode layer, and they are not an indicator of the ease of supplying electrons to AM particles"* · 그림 4 · 5 에서 CP-VGCF 는 AM 을 지나는 전자 경로가 적다.

### 3-8. 수명 (p.8 · 그림 10 · `fig_10.png` · `txt_p8_cycle_retention_volume_change.png`)
- 판독 (벡터 · 1.0 C 방전 · 표지 50 개씩 · 범례 표지 빼고): 첫 → 50 번째 SM **103.6 → 31.0** · CP **54.1 → 26.7** · CP-AB **118.0 → 109.6** · CP-VGCF **61.0 → 33.3 mAh g⁻¹** → 유지율 **29.9 · 49.3 · 92.9 · 54.7 %** [카드 산술] ↔ 본문 **32.2 · 49.3 · 92.9 · 54.7 %** (p.8) — SM 만 2.3 %p 다르다 (§3-9).  SM 은 25 번째 뒤 급락 (판독 80.2 → 35.6 · 25 → 45 사이클).
- 저자 [인쇄 p.8]: SM 급락 = *"mechanical degradation [36]"* · AM 부피 변화로 AM–AM · AM–SE 접촉 상태가 바뀌고 SM 은 친밀 계면이 어려워 *"peeling the contact interface"* · 코어–셸은 *"could mitigate the effect of the volume change of AMs owing to the intimate SE coating layer"* — **부피 변화 · 박리 · 손상의 측정은 없다** · 운전 적층압 [미확인].
- 그림 10 의 첫 1 C 값과 그림 7c 의 1 C 값이 다른 것 (SM 103.6 ↔ 102.7 · CP 54.1 ↔ 47.6 · CP-AB 118.0 ↔ 115.7 · CP-VGCF 61.0 ↔ 66.9 [판독]) 은 측정 때가 달라서 (원문 p.8).

### 3-9. ★ 저자가 적은 한계 · 원문 안 어긋남
**저자 한계 (원문)**: 순 VGCF 를 1.6 wt% 넘게 올릴 수 없었다 (p.4 · SI p.1) · CP-VGCF 의 율속은 Rs · Rct 로 설명되지 않는다 (p.7) · 측정 때가 달라 0.1 C · 1 C 값이 그림끼리 조금 다르다 (p.6 · p.8).  기공 · 압력 · 역학에 대한 한계 문장은 없다.
**원문 안 어긋남 (카드가 본 것 — 고치지 않고 적는다)**:
1. CP 첫 방전: 본문 "ca. 87 mAh g⁻¹" (p.6) ↔ 그림 7a 방전 끝 81.7 [판독 · 쿨롱 효율 77.0 % 와 맞는 값] · 그림 7c 0.1 C 89.1.
2. SM 50 사이클 유지율: 본문 32.2 % (p.8) ↔ 그림 10 첫 103.6 → 50 번째 31.0 = 29.9 % [판독] (다른 세 시료는 ±0.1 %p 안에서 재현).
3. 그림 5 캡션 "(c) CP-VGCF" (= (d)) · 그림 8 캡션 "SM, CA, CP-AB" (= CP) · 그림 3 · 4 의 "(c)CP-AB" 붙여 쓰기 등 표기.
4. Rs 해석 (SM 은 응력 불균일로 SE 합체 부족) ↔ 같은 논문 이온 차단 σ_ion (SM ≥ CP · 유의차 없음) — 방향이 맞지 않는다 (§3-6).
5. 시료 사이 순 도전재 몫이 다르다 (AB 2.79 ↔ VGCF 1.62 wt%) — "도전재 종류" 효과와 "도전재 양" 효과가 섞인다.
6. σ 계산에 쓴 두께 · 지름 값이 인쇄되지 않았다 (p.3) — σ 를 다시 낼 수 없다.
7. SI 문단 *"As shown Fig. S1"* (오탈) · SI 그림 S2 가 어느 시료인지 없음.

---

## 4. ★ 방법 — 측정 사슬 · 입자 처리 · 이 묶음의 네 질문

### 4-1. 측정 사슬
- **분말 → 입자**: 헵테인 초음파 예비 혼합 (CA 포함) → 건조 → 충격 블렌딩 코팅 → 순 조성 (UV–vis · TG–DTA) → 입자 SEM/EDX · 이온빔 단면 SEM/EDX.
- **입자 → 압분체**: 80 mg · 360 MPa → 이온 차단 셀 EIS (두 반원 맞춤 → σ_ion · σ_e) · 단면 SEM/EDX (그림 5).
- **입자 → 반쪽셀**: SE 20 MPa → 양극 360 MPa 5 min → Li–In 90 MPa 5 min → 0.1 C 3 사이클 → 율속 → EIS (SOC 50 %) → 50 사이클 → CV.  **세 종류 시편 (입자 · 80 mg 압분체 · 10 mg 반쪽셀 양극) 이 다르다.**

### 4-2. 입자 처리 ★
- 실험만이다 — 입자 계산 (DEM · MPM · FEM) 없음.  단면 SEM/EDX 는 2D 이고 정성 (탄소 세기 · 화살표) 뿐이다 (상 분율 · 피복률 · 껍질 두께 분포의 정량 없음).
- 껍질은 **SE 입자의 합체 (coalescence)** 로 생긴다고 쓴다 (p.7) — 껍질 SE 의 소성 변형 · 접합을 **암시**하지만 측정 · 모형은 없다.

### 4-3. ★ 이 묶음의 네 질문 (원문 문장과 위치)
1. **DEM (단단한 구 · 점접촉) 의 한계를 말한 문장** — **말 없음** (DEM · discrete · simulation 0 회).
2. **소성 · 큰 변형을 계산에 넣기 어려운 이유 · 우회 · 비용** — **말 없음**.  소성과 닿는 문장은 둘뿐: *"the composite particles were in a state of already promoted coalescence of SE by the dry coating process"* (p.7 · SE 합체) · *"it was difficult to fold and incorporate the VGCF into the SE coating layer"* (p.4 · 섬유를 껍질에 접어 넣기).  둘 다 측정 · 계산 없는 서술.
3. **2D / 3D** — 펠릿은 3D 실물 · 단면 SEM/EDX 는 2D 영상 · 2D → 3D 전이에 대한 말 **없음**.
4. **압력을 뺄 때의 거동** — **다루지 않았다**.  이온 차단 셀 · 반쪽셀이 측정 때 눌린 채인지 [미확인] · 탈압 · 스프링백 0 회.

### 4-4. 기법 미니 용어집
| 용어 | 뜻 (이 논문 안에서) |
|---|---|
| 건식 충격 블렌딩 (dry impact-blending) | 날 달린 회전자가 고속 (13,000 rpm) 으로 돌며 분말을 순환관으로 돌려 반복 충돌시키는 건식 코팅 · 큰 핵 입자 (AM) 위에 작은 입자 (SE) 를 용매 · 결합제 없이 입힌다 (Nara) |
| 코어–셸 복합 입자 (CP) | AM 핵 + SE 껍질 (+ CA) 입자 · 이 논문에서는 "ordered mixture" 의 극단 (p.2) |
| 투입 ↔ 순 (initial ↔ net) 질량분율 | 장치에 넣은 비 ↔ 코팅 뒤 실제 입자 속 비 (SE 를 녹여 UV–vis · CA 는 TG–DTA) |
| 이온 차단 셀 EIS | 이온이 집전체로 못 넘어가는 셀에서 전자 · 이온 경로의 두 반원을 맞춰 σ_e · σ_ion 을 한 번에 (원전 [23] Siroma 2016 · [24] Asano 2017) |
| Rs · Rct · R_NE | 반쪽셀 EIS 의 고주파 (SE 저항 · 분리막 포함) · 중주파 (양극 전하 이동) · 저주파 (Li–In 음극) 저항 |
| 층 σ_e ↔ AM 전자 공급 | 판에서 판까지 층 전체에 전류가 흐르기 쉬운 정도 ↔ 각 AM 입자 표면까지 전자가 닿기 쉬운 정도 (저자 p.7 의 구분) |
| AB · VGCF | 아세틸렌 블랙 (일차 ≈35 nm 사슬 덩이 · 0 차원 꼴) · 기상 성장 탄소 섬유 (≈150 nm × ≈6 µm · 1 차원) |

---

## 5. Figure set ★
| 그림 | 보이는 것 | 우리가 쓸 것 |
|---|---|---|
| **그래픽 초록** (`fig_GA.png`) | 건식 코팅 장치 그림 + CA 없음 · VGCF · AB 세 입자의 전자 경로 그림 + 용량 · 율속 · 수명 ○ × 표 (× × × · ○ × × · ○ ○ ○) | 결론의 한 장 요약 (값 없음) |
| **그림 1** (`fig_1.png`) | 원료 SEM: (a) NCM523 다결정 2차 입자 (5 µm) · (b) Li₆PS₅Cl 조각 (1 µm) · (c) AB 사슬 덩이 · (d) VGCF 섬유 뭉치 | 원료 입자 꼴 — 우리 DEM 구 가정과 다른 모난 SE 조각 · 섬유 |
| **그림 2** (`fig_2.png`) | 건식 충격 블렌딩 장치 앞 · 옆 그림 (1 순환관 · 2 냉각 챔버 · 3 회전자 · 4 날 · 5 배출 밸브 · 6 회수 · 7 백 필터) | 공정 장치 (흐름 밖 · 믹서 Ⓒ 의 다른 장치 꼴) |
| **그림 3** (`fig_3.png`) | 입자 SEM + Ni · S 지도 (SM · CP · CP-AB · CP-VGCF) | 코팅 상태의 정성 판정 (Ni 와 S 의 겹침) |
| **그림 4** (`fig_4.png` · 패널 `fig_4a` · `4b` · `4c`) | 입자 단면 SEM + C 지도 · 흰/빨간 화살표 · AM/SE 경계 점선 | ★ 도전재가 껍질 안 (AB) / 밖 (VGCF) — 껍질 속 탄소 표현의 근거 그림 |
| **그림 5** (`fig_5.png`) | 압분체 단면 SEM + C 지도 (점선 = AM 윤곽) | 360 MPa 뒤 AM 둘레 SE · 탄소 자리 (정성) |
| **그림 6** (`fig_6.png` · `fig_6a` · `fig_6b`) | (a) σ_ion (선형) · (b) σ_e (로그) · 평균 ± SD (N = 3) | ★ 껍질의 σ_e 손실 ×1/21 · σ_ion 유의차 없음 — 결과 전 대조 항목 (§8) |
| **그림 7** (`fig_7.png` · `fig_7a`–`7d`) | (a) 첫 충방전 (0.1 C) · (b) 3 번째 dQ/dV + 봉우리 전위 표 · (c) 방전 율속 · (d) 충전 율속 | 첫 방전 · 효율 · 3.6 V 도달 용량 · 율속 판독 |
| **그림 8** (`fig_8.png`) | 나이키스트 + 등가 회로 + Rs · Rct 표 | 반쪽셀 저항 (Rs 는 분리막 포함 — 복합 σ_ion 대리로 쓰지 않는다) |
| **그림 9** (`fig_9.png`) | CV (CP-AB · CP-VGCF · 0.05 mV s⁻¹) | 'σ_e 높아도 전자 공급 약함' 의 근거 그림 |
| **그림 10** (`fig_10.png`) | 1.0 C 50 사이클 방전 용량 | 유지율 판독 (SM 은 본문과 2.3 %p 다름) |
| **표 1** (`tab_1.png`) | 투입 · 순 질량분율 | 순 조성 · SE 손실 [카드 산술] |
| **SI 그림 S1** (`fig_S1.png`) | (a) VGCF 2 · 4 wt% 입자 단면 SEM + C 지도 (3 µm) · (b) 투입 · 순 조성 · VGCF/SE 비 표 | 투입 2 배에도 껍질 VGCF 그대로 |
| **SI 그림 S2** (`fig_S2.png`) | 전형적 나이키스트 + 100 kHz · 100 Hz · 0.2 Hz 화살표 + 등가 회로 | 주파수 배정 |
| 근거 문단 20 (`txt_p*` · `txt_si_p1_*`) | 카드가 숫자 · 정의 · 단정의 근거로 인용한 문장 | 보고서 붙임 |

## 6. Post-processing ★
- **순 조성**: UV–vis (235 nm · SE 용해) + TG–DTA (CA) · 투입 ↔ 순 표 (표 1 · SI 표).
- **σ_ion · σ_e**: 이온 차단 셀 EIS 두 반원 맞춤 → 저항 → 두께 · 면적으로 σ (식 · 두께 미인쇄) · N = 3 평균 ± SD.
- **반쪽셀**: 첫 사이클 효율 · 3 번째 사이클 dQ/dV 봉우리 전위 (표) · 율속 · 등가 회로 맞춤 (Rs = 고주파 두 성분 합) · CV 모양 비교 · 50 사이클 유지율 (50 번째/첫).
- **영상**: SEM/EDX 지도 정성 판정 (Ni · S 겹침 · C 세기 · 화살표) — 정량 영상 분석 없음.
- **판독 (이 카드)**: 그림 6–10 은 벡터 → PDF 경로 좌표에서 직접 (표지 중심 · 곡선 꼭짓점 · 틀 눈금 보정) · digitized.csv 의 note 열에 보정 전부.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md 출처를 병기해 적는다)

### 7-1. 비교표 (모든 행에서 **재료 · 상태 · 측정법이 다르다**)
| 양 | 이 논문 | 우리 | 같은 / 다른 · 이유 |
|---|---|---|---|
| 무탄소 복합 양극 σ_e | 막자 혼합 SM **2.84 × 10⁻⁵ S cm⁻¹ = 0.028 mS cm⁻¹** (NCM523 + LiNbO₃ · 84 wt% · 360 MPa · EIS) | ps45 Hertz σ_e 인자 끔 **0.375–0.467 mS cm⁻¹** (σ_AM 4.1 mS cm⁻¹ · NCM811 · 무탄소 · DEM 접촉망) [우리 · CLAUDE.md 10-13] | 우리가 13–16 배 높다 — CAM (NCM523 + 절연 LiNbO₃ 코팅 ↔ NCM811 σ_AM 4.1) · 조성 · 측정 (AC ↔ 망 계산) 이 달라 **오차로 읽지 않는다** · [다른 카드] 무탄소 혼합 복합체 σ_e: `siroma2016_…` NCM523 (LiNbO₃) 70 vol% 0.178 · `strauss2018_…` NCM622 d50 4.0 µm (7 : 3 wt) 0.88 mS cm⁻¹ — 이 논문 SM 이 가장 낮은 쪽 |
| ★ 비전도 SE 껍질의 σ_e 손실 | CP/SM = **0.048 (×1/21)** · 같은 순 SE 16–17 wt% · CP 절대값 **1.4 × 10⁻³ mS cm⁻¹** | DEM 침대에 코어–셸 표현 없음 · 망 σ_e = AM–AM 접점망 [우리] | **우리에게 없는 상태** — 껍질이 AM–AM 접점을 없애면 우리 망 σ_e 도 무너질 것 (예측 · 미계산) · 같은 그룹 [다른 카드: `nakamura2020_…` Li₃PS₄ · DC σ_e −94 %] 와 같은 크기 (이 논문 −95 % [카드 산술]) · [다른 카드] `kissel2026_…` 무탄소 전부-코팅 80 : 20 : 0 = 0.034 mS cm⁻¹ (Li₃InCl₆ 껍질 ≈5 nm) — 이 논문 CP 의 ≈25 배 (껍질 두께 · SE · 측정 다름) |
| 복합 양극 σ_ion | 3.2–4.6 × 10⁻⁵ S cm⁻¹ = **0.032–0.046 mS cm⁻¹** · f = σ/2.02 mS cm⁻¹ = **0.016–0.023** (SE ≈35–37 vol% [카드 산술 · 랩 표준 1.64 · NCM523 4.72 가정]) | ps45 Hertz σ_ion (σ₀ 1.5) **0.0587–0.0893 mS cm⁻¹** [우리 · CLAUDE.md 10-13] · Bazzoun 2026 EIS 0.137 / 0.101 / 0.065 mS cm⁻¹ (CAM 70 / 75 / 80 wt% · 400 MPa) [우리 · CLAUDE.md] | 자릿수 같은 쪽 · CAM 이 많을수록 낮아지는 방향 (이 논문 84 wt% 0.032–0.046 < Bazzoun 80 wt% 0.065) — SE · CAM · σ₀ · 압력이 달라 **방향 · 자릿수만** |
| 코팅이 σ_ion 에 주는 효과 | CP/SM 0.91 · CP-AB 1.07 · CP-VGCF 1.31 (전부 SD 안 · "no significant difference") | 없음 (코어–셸 미표현) | [다른 카드] `nakamura2020_…` 은 같은 비교에서 DC σ_ion **+58 %** · `kim2024_optimal_cathode_composite_mechanical_mixing_se_coverage` 은 껍질 몫에 최적점 — 문헌끼리도 엇갈린다 (재료 · 측정 다름) |
| SE 입경 · AM 입경 | SE 개수 중앙 **0.7 µm** · NCM523 **4.3 µm** (≈1 : 6) | DEM 생산 r_SE 0.5 µm (지름 1.0) · real_14 크기 비 12 : 4 : 1 (AM_P : AM_S : SE) [우리 · CLAUDE.md] | 크기 자릿수는 우리 AM_S · SE 와 비슷 · 분포 · 꼴 (모난 SE · 다결정 AM) 다름 |
| 성형압 | 360 MPa (5 min · 반쪽셀 양극) · 80 mg 압분체 360 MPa | 300 MPa 압축 (DEM · MPM) [우리] | 비슷한 자릿수 · 압력별 자료 없음 |
| 탄소 있는 전극 σ_e | CP-VGCF **0.50 mS cm⁻¹** (VGCF 순 1.62 wt% · 입자 사이) | 랩 DC 분극 SBE **1.63** · DBE **4.68 mS cm⁻¹** (VGCF 든 SDCP 원고 전극 · 10-16 측정 · VGCF 몫은 이 카드에서 확인 안 함) [우리 · CLAUDE.md 10-19] | 3–9 배 차 — VGCF 양 · CAM · 측정 (EIS ↔ DC) 다름 · 대조 아님 |

### 7-2. ★ "층 σ_e ≠ AM 전자 공급" 을 우리 수송 계산에 들일 때
- 원문의 구분 (p.7): 층 전체 σ_e 는 *"the ease with which the electrical current can be made to flow through the entire cathode layer"* 이고 *"not an indicator of the ease of supplying electrons to AM particles"*.  실증 = CP-VGCF (σ_e 최고 · CV · 율속 최약) ↔ CP-AB (σ_e 낮음 · CV · 율속 최강).
- 우리 망 σ_e 는 판에서 판까지 흐름 하나다 — **AM 입자마다 전자가 닿는가** 는 따로 재야 한다 (예: 판에 이어진 전자망에 붙은 AM 의 몫 · AM 입자별 전류).  우리 수송 계산에 VGCF 가 들어갈 때 (STEP3 · 탄소 망) 층 σ_e 가 올라도 AM 표면 전자 공급이 그만큼 늘었다고 읽지 않는다 [카드 해석 · 우리 쪽 적용].
- 탄소가 입자 사이에만 있으면 (VGCF) 층 σ_e 는 오르고 AM 접점은 그대로 막혀 있다 — 우리 복셀 STEP3 처럼 탄소 셀이 AM 셀에 맞닿으면 전자가 바로 들어가는 표현 (계면 막 없음) 은 이 구분을 지운다 [카드 해석].

### 7-3. 같은 질문 · 반대 결론 — `kim2025_conductive_agent_se_coating_cathode` 와
- [다른 카드 · kim2025 머리 요약]: SE 코팅에 CA 를 같이 넣으면 **0D Super P 는 코팅층에 응집 · 과잉 → 나쁨 · 1D VGCF 는 드물게 박힘 → 좋음 (CA 없는 SE@CAM 과 동등)** · CA 없는 SE@CAM 은 치밀 코팅 = 좋은 기준.
- 이 논문: **0D AB 가 좋음 · 1D VGCF 는 껍질에 못 들어가 율속 나쁨 · CA 없는 CP 는 가장 나쁨.**
- ⇒ "도전재 차원이 결과를 가른다" 는 같지만 **어느 차원이 좋은지는 공정 · 크기 · 양에 달렸다** [카드 해석] — 이 논문의 규칙은 "껍질 두께보다 작은 CA 가 껍질에 들어간다" (AB 35 nm < 껍질 100–1000 nm < VGCF 길이 6 µm).  두 논문의 재료 · 공정 · 측정이 달라 한 표에 넣지 않는다.

### 7-4. frame[5] — 어느 반쪽을 가졌나
- 이 논문 = **실험 (코팅 상태 · 압분체 σ · 전기화학)** 만 — 우리 분업의 **DEM 쪽 (접촉망 σ_e · σ_ion · 피복)** 에 대한 측정 쪽 짝이다.  MPM 쪽 (형상 변화 · 응력장) 은 "SE 합체 · 응력 불균일" 이라는 **가설 문장**뿐.
- 없는 반쪽: 압밀 과정 · 압력별 기공 · 응력 · AM 하중 분담 · 탈압 · 접촉 면적 정량.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문 재료 = NCM523 (LiNbO₃) + Li₆PS₅Cl (Mitsui) + AB / VGCF — **CAM 이 다르고 역학 측정이 없다**.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | 반면교사 둘 — ① **σ 를 두께로 냈는데 두께를 안 적었다** (p.3) → 우리 결과 전 대조 항목에는 두께 · 면적 · 측정 때 압력을 같은 칸에 등록 ② **투입 ≠ 순 조성** (SE 37–42 % 손실 [카드 산술]) → "같은 조성" 비교는 순 조성으로 등록 | 기공 · 진밀도 · 압력별 곡선 **없음** — 랩 표준 (10–13 % · 1.64) 과 나란히 놓을 숫자 없음 |
| **단계 1** (3D 메모리 · 장 수) | 크기 감각 하나: 코어–셸을 입자로 풀면 AM 한 개당 SE ≈136 개 (지름 0.7 µm · 껍질 ≈0.36 µm [카드 산술]) → 코팅 침대는 같은 AM 수에서 SE 입자 수가 크다 | 계산 없음 |
| **단계 2 · 3** (2D MPM · 접촉 표현 비교) | 없음 | — |
| **단계 4** (3D 순수 SE · σ_y 하나 맞춤) | 없음 (순수 SE 압분체 · 기공 · 항복 없음 · SE 2.02 mS cm⁻¹ 의 측정 조건 [미확인]) | — |
| **단계 5** (3D 복합 압밀) | ★ **출발 상태가 결과를 바꾼다는 실측 짝**: 같은 순 조성 · 같은 360 MPa 에서 출발 상태 (막자 혼합 ↔ 코어–셸) 만 달라 σ_e ×1/21 · σ_ion 유의차 없음 · Rs −16 % (분리막 포함) → 우리 3D 복합 압밀에 **코어–셸 출발 상태** (AM 둘레에 SE 를 미리 둔 침대) 를 넣을 때의 결과 전 대조 항목 (방향 · 자릿수) · 저자의 "응력 불균일 → SE 합체 부족" (p.7) 은 **검증 가능한 가설** (혼합 ↔ 코어–셸 침대의 SE 응력 분포 · SE–SE 접촉 면적) | 응력 · 기공 · 하중 분담 측정 없음 · 가설의 근거 없음 |
| **단계 6** (탈압 · 되돌아옴) | 없음 (탈압 0 회 · 측정 때 압력 [미확인]) | — |
| **단계 7** (형상 · 피복 · 수송) | ★★ ① 비전도 껍질 → 압분체 σ_e ×1/21 (AM–AM 전자 접점 소실) ② 껍질 안 탄소 (AB) → σ_e ×4.7 (CP 대비) 이지만 SM 의 0.22 · 껍질 밖 탄소 (VGCF) → ×370 (CP 대비) · SM 의 17.6 ③ **층 σ_e ↔ AM 전자 공급 구분** (p.7) → 우리 망에 AM 입자별 전자 접근성 지표 필요 (§7-2) ④ σ_ion f ≈0.016–0.023 (SE ≈36 vol% [카드 산술]) | 피복률 · 접촉 면적 정량 없음 · σ 의 두께 · 맞춤 회로 미기재 · N = 3 |
| **후보 D0** (지금 DEM) | 코팅 출발 상태를 D0 로 만들면 (AM 둘레 SE 입자 껍질) 망 σ_e 가 AM–AM 접점 소실로 무너지는지 — 결과 전 대조 = CP/SM **≈0.05** (이 논문) · **≈0.06** (`nakamura2020_…` −94 % [다른 카드]) · 탄소 없는 우리 망에 맞는 쪽은 CP (탄소 없음) | 재료 다름 (NCM523 + LiNbO₃) · DEM 에 껍질 합체 (SE 소성) 없음 |
| **후보 A′-0 · A · A′** (MPM 접촉 · 강체 AM · 입자별 속도장) | 없음 — 단, 껍질이 "합체" 된 연속 SE 라는 서술은 **SE 껍질을 한 연속체로 두는 MPM 표현** (A) 쪽 그림과 맞는다 [카드 해석] | 측정 없음 |
| **후보 B · C · C′ · M0** | 없음 | — |
| **U0–U6** | 없음 | — |
| **R1–R7** | **R2** (미끄럼 · 분리) — 사이클 중 AM–SE *"peeling"* (p.8 · 가설) · **R6** (SE 형상 변형) — 코팅 중 SE *"coalescence"* (p.7) · 그림 3 · 4 의 껍질 (SM 보다 매끈한 겉 · 정성 [카드 해석]) = 압밀 **전에** SE 가 이미 변형된 출발 상태 · **R7** (AM 파괴) — 단면 AM 속 빈 곳 (정성 · 원문 언급 없음) · SM 의 *"mechanical degradation"* (가설) | R1 · R3 · R4 · R5 없음 |
| **결과 전 대조 항목** | ① 같은 순 조성 (SE ≈16–17 wt%) 에서 코어–셸 (무탄소) ÷ 막자 혼합 **σ_e = 0.048** (360 MPa 압분체 · EIS · N = 3 · 판독) ② 같은 비교의 **σ_ion = 0.91 (유의차 없음)** ③ 껍질 안 탄소 (AB 2.79 wt%) 는 σ_e 를 SM 의 0.22 까지만 · 입자 사이 탄소 (VGCF 1.62 wt%) 는 17.6 배 — 그러나 율속 · CV 는 반대 — 맞추는 데 쓰지 않음 | 재료 · 압력 · 두께 · 측정법이 우리와 달라 절대값 대조 불가 |

- **재료 · 차원 · 조건 차이**: NCM523 + LiNbO₃ (우리 NCM811) · Li₆PS₅Cl 0.7 µm · 2.02 mS cm⁻¹ (우리 σ₀ 보고 1.5 · 풀이기 3.0) · 순 SE 16–17 wt% (≈36 vol% [카드 산술]) · AB / VGCF · 360 MPa · 298 K · 3D 실물 펠릿 · 2D 단면 영상 · 기공 · 두께 미보고.

## 9. 적용 인사이트 (행동)
1. **코어–셸 출발 상태의 결과 전 대조 항목 등록 (단계 5 · 7 · 믹서 Ⓒ)**: "같은 순 조성에서 비전도 SE 껍질 → 압분체 σ_e ×1/21 (Hayakawa 2023 · NCM523 · 360 MPa · EIS) · ×1/17 (Nakamura 2020 · Li₃PS₄ · DC −94 %)" 를 **방향 · 자릿수 항목**으로 — 우리 망 σ_e 가 코팅 침대에서 같은 쪽으로 무너지는지 본다 (값은 맞추는 데 쓰지 않는다).
2. **AM 전자 접근성 지표를 σ_e 옆에 (단계 7 · 흐름 밖: 접촉망 수송)**: 판–판 σ_e 와 별개로 "판에 이어진 전자망에 붙은 AM 의 몫 · AM 입자별 전류" 를 같이 보고 — 탄소 (VGCF) 를 넣어 층 σ_e 가 오를 때 특히.
3. **조성은 순 (net) 으로 (단계 0 · 믹서 등록)**: 건식 코팅은 SE 를 37–46 % · VGCF 를 42–65 % 잃는다 [카드 산술 · AM 추적자 · 표 1 + SI 표] — 코팅 침대의 SE 몫을 투입값으로 두지 않는다.
4. **탄소 자리 규칙 (흐름 밖: 첨가제 표현)**: 껍질 두께 (100–1000 nm) 보다 작은 CA (AB 35 nm) 는 껍질 안 · 긴 섬유 (VGCF 6 µm) 는 입자 사이 — 코팅 입자에 탄소를 그릴 때 이 기하 규칙을 결과 전에 적는다 (원문은 정성 SEM/EDX 근거뿐).
5. **Rs 는 복합 σ_ion 대리가 아니다**: 반쪽셀 Rs (분리막 포함) 의 차이 (94.5 ↔ 63.1 Ω) 와 이온 차단 σ_ion (유의차 없음) 이 엇갈린다 — 우리 σ_ion 교차검증에는 이온 차단 · 대칭 셀 σ 만 쓴다 (kawaguchi2023 카드와 같은 결론 [다른 카드]).

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "In dry-coated NCM523@Li₆PS₅Cl core–shell particles (net 16.9 wt% SE), the electronically insulating SE shell lowered the electronic conductivity of the 360-MPa composite to ≈1/21 of a mortar-mixed composite with the same SE fraction (1.4 × 10⁻⁶ vs 2.8 × 10⁻⁵ S cm⁻¹, read from Fig. 6b), while the ionic conductivity did not differ significantly (Hayakawa et al., *J. Power Sources* 555 (2023) 232379)."
- "Acetylene black (≈35 nm) was incorporated into the 100–1000-nm SE shell, whereas VGCF (≈150 nm × ≈6 µm) stayed outside the particles; the VGCF composite showed the highest layer electronic conductivity but the poorest rate and CV response, which the authors attribute to limited electron supply to the active-material particles (Hayakawa et al., 2023)."
- 국문 (한정어와 함께): *"같은 순 조성에서 비전도 SE 껍질은 360 MPa 압분체의 전자 전도도를 1/21 로 낮춘다 (Hayakawa 2023 · NCM523 · EIS · 판독) — 껍질 안에 든 AB 만 율속 · 수명을 살렸고, 입자 사이 VGCF 는 층 전도도만 올렸다 (층 σ_e ≠ AM 전자 공급)."*

## 11. 주의/한계 (over-claim 방지)
**원문이 스스로 적은 한계**: §3-9 첫 줄.
**카드가 본 한계**
1. **기공 · 두께 · 밀도 · 압력별 · 탈압 측정 없음** — σ 계산의 두께도 미인쇄.
2. **N = 3 · SD 큼** — σ_ion 네 값은 오차 막대가 서로 겹친다 ("no significant difference" 는 저자 판단 · 검정 방법 없음).
3. **CA 순 몫이 다르다** (AB 2.79 ↔ VGCF 1.62 wt%) — 종류 효과와 양 효과가 섞인다.
4. **Rs 해석 (응력 불균일 · SE 합체) 은 측정 없는 가설** · 같은 논문 σ_ion 과 방향이 안 맞는다 · Rs 는 분리막 포함.
5. **원문 안 어긋남 둘** (CP 첫 방전 87 ↔ 81.7 · SM 유지율 32.2 ↔ 29.9 %).
6. **재료**: NCM523 + LiNbO₃ (우리 NCM811) · SE 2.02 mS cm⁻¹ 측정 조건 미기재 · AM 다결정.
7. **영상은 정성** — 껍질 두께 · 피복률 · 탄소 분포의 정량 없음.
8. **인과 주장** ("코어–셸이 부피 변화 영향을 줄인다" · "기계적 열화") 은 손상 · 부피 측정 없이 연결된 것.
9. **운전 적층압 · 측정 때 압력 [미확인]** — 압력 의존 대조 불가.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| [16] | E. Hayakawa, H. Nakamura, S. Ohsaki, S. Watano, Characterization of solid-electrolyte/active-material composite particles with different surface morphologies for all-solid-state batteries, Adv. Powder Technol. 33 (2022), 103470, https://doi.org/10.1016/j.apt.2022.103470. | ★ 이 논문 공정 조건의 근거 [13,16] · 껍질 표면 형태 (불연속 ↔ 연속) 별 성능 — 카드 없음 (kawaguchi2023 이 인용만) |
| [10] | E. Hayakawa, H. Nakamura, S. Ohsaki, S. Watano, Dry mixing of cathode composite powder for all-solid-state batteries using high shear mixer, Adv. Powder Tech. 33 (2022), 103705, https://doi.org/10.1016/j.apt.2022.103705. | 고전단 혼합기 건식 혼합 (frankenberg2025 [64] · wolf2026 ref 15) — 후보 표 N-87 · 카드 없음 |
| [19] | M. Iwao, R. Sakurai, H. Nakamura, E. Hayakawa, S. Ohsaki, S. Watano, Solid electrolyte/graphite composite particle for an all-solid-state lithium-ion battery, Adv. Powder Technol. 33 (2022), 103633, https://doi.org/10.1016/j.apt.2022.103633. | 양극 AM 보다 *"more brittle"* 한 흑연에도 *"by controlling the preparation conditions"* 같은 건식 코팅을 적용 (p.2 · 코팅 중 핵 손상 = R7 쪽 관심) · 카드 없음 |
| [36] | T. Shi, Y.-Q. Zhang, Q. Tu, Y. Wang, M.C. Scott, G. Ceder, Characterization of mechanical degradation in an all-solid-state battery cathode, J. Mater. Chem. 8 (2020) 17399–17404, https://doi.org/10.1039/D0TA06985J. | SM 급락의 "mechanical degradation" 근거 — 후보 표 N-101 · 카드 없음 (gandla2026 · li2026 이 인용만) · 원문 목록은 학술지를 "J. Mater. Chem. 8 (2020)" 로 적었다 (후보 표 N-101 서지는 "Journal of Materials Chemistry A 8, no. 34") |
| [27] | W. Zhang, T. Leichtweiß, S.P. Culver, R. Koerver, D. Das, D.A. Weber, W.G. Zeier, J. Janek, The detrimental effects of carbon additives in Li10GeP2S12-based solid-state batteries, ACS Appl. Mater. Interfaces 9 (2017) 35888–35896. | CA–SE 부반응 (3.6 V 전 10–15 mAh g⁻¹) — 카드 없음 (kato2018 이 인용만) |
| [26] | K. Yoon, J.-J. Kim, W.M. Seong, M.H. Lee, K. Kang, Investigation on the interface between Li10GeP2S12 electrolyte and carbon conductive agents in all-solid-state lithium battery, Sci. Rep. 8 (2018) 8066. | VGCF 1 차원 꼴의 전자 공급 · 부반응 — 카드 없음 |
| [13] · [14] · [15] · [23] · [24] · [7] · [11] · [17] | Kawaguchi 2017 · Kawaguchi 2018 · Nakamura 2020 · Siroma 2016 · Asano 2017 · Nam 2018 · Sakuda 2011 · Pfeffer 2001 | 정본 카드 있음 (`kawaguchi2017_…` · `kawaguchi2018_…` · `nakamura2020_…` · `siroma2016_…` · `asano2017_…` · `nam2018_…` · `sakuda2011_…` · `pfeffer2001_…`) |

## 13. [미확인] 목록 (본문 9 쪽 + SI 2 쪽 전수에 없음)
1. 이온 차단 셀의 지름 · 가압 시간 · 압분체 두께 · 측정 때 압력 · 맞춤 등가 회로 · σ 계산식.
2. 진밀도 (NCM523 · Li₆PS₅Cl · AB · VGCF) · 기공 · 겉보기 밀도.
3. 반쪽셀 운전 적층압 · 체결 토크 · 양극 층 두께.
4. 충격 블렌딩 장치 모델명 · 회전자 지름 · 선속도 · 충격 에너지 · 공정 온도.
5. SE 2.02 mS cm⁻¹ 의 측정 조건 (압력 · 온도).
6. 막자 혼합 시간 · 방법 세부.
7. 껍질 두께 분포 · 피복률 정량 (본문은 범위 100–1000 nm 만).
8. "no significant difference" 의 통계 검정 방법.
9. SI 그림 S2 의 시료.
10. 손실 질량 (벽 부착) 의 직접 측정 — 카드의 손실률은 AM 추적자 가정의 산술.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-16)
- 본문 9 쪽 + SI 2 쪽을 글자 층 추출 + 쪽 렌더로 읽음.  서지 = 본문 첫 쪽 (제목 · 저자 넷 · 소속 · DOI · 접수 · 수정 · 승인 · 온라인 날짜) · 쪽 머리 (권 555 · 232379) · p.8 (CRediT · 이해상충 · 자료 · NEDO SOLiD-EV JPNP18003).  SI 첫 쪽 = 같은 제목 · 저자.  원문 낱말 셈: DEM · discrete · simulation 0 · plastic · deform · elastic · porosity · unload · stack · torque 0 · stress 2 (p.7 Rs 해석) · coalescence 2 (p.7).
- 그림 크롭 **43 장** = 도구 12 (그림 1–10 · SI 그림 S2 · 표 1 — **다시 자름 9**: 그림 2 · 8 · 9 · 10 여백 고르지 않음 · 그림 4 · 6 · 7 쪽 폭 · SI 그림 S2 가로축 이름 잘림 · 표 1 이 쪽 머리글과 본문 두 단을 먹음 · 캡션만 고친 것 1 = 그림 3) + 손 크롭 31 (그래픽 초록 1 · SI 그림 S1 1 = 도구가 'Fig. S1(a)' 꼴 캡션을 못 잡음 · 패널 9 = 4a–c · 6a–b · 7a–d · 식 0 = 원문에 번호 식 없음 · 근거 문단 20).  본 뒤 다시 렌더한 것 = txt_p2_shell (위 줄 조각) · fig_S1 (오른쪽 흰 띠).  43 장 전부 Read 로 열어 확인.  `figures.json` 의 `recrop` · `manual_crop` · `note_manual` · `viewed_how`.
- 판독: digitized.csv 332 행 — 그림 6–10 은 벡터라 PDF 경로 좌표에서 직접 (보정 = 틀의 눈금선).  재현 확인: 그림 6b 비 4.7 · 17.6 ↔ 본문 "≈5" · "≈18" · 그림 7a 효율 82.5 · 77.0 · 75.7 · 71.3 ↔ 본문 82.6 · 77.0 · 75.7 · 71.3 · 그림 7b 극값 전위 ↔ 그림 안 표 (셋째 자리까지) · 그림 10 유지율 셋 ±0.1 %p (SM 만 2.3 %p 다름) · 그림 7a 3.6 V 도달 10.6 · 15.8 ↔ 본문 "10–15".
- 2 차 인용 대조: kawaguchi2023 (L287 · L288 · L301) · kissel2026 (L508) · frankenberg2025 (L363) — 고치지 않았다 (카드 문제 = 정독 출력 batch_130 의 "카드 문제" 절).
- 정본 litdb 중복 확인: `git ls-tree` 로 `litdb/papers/` 전수 + DOI (jpowsour.2022.232379 · 232379) · 제목 낱말 ("composite particles with conductive") · 저자 (Hayakawa) grep — 이 논문 카드 없음 (인용만: kawaguchi2023 · kissel2026 · frankenberg2025) · 같은 그룹 카드 = `nakamura2020_…` · `kawaguchi2017_…` · `kawaguchi2018_…` · `kawaguchi2023_…` (2026-11-16).

## 🔗 관련 카드
- 같은 그룹 · 같은 장치 (Nara 건식 충격 블렌딩 · 13,000 rpm · 5 min): `kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps` (이 논문을 ref 26 으로 인용 · 무탄소 Li₃PS₄ · Xs · P · Ts DOE) · `nakamura2020_dry_coating_ncm_li3ps4_core_shell` (ref [15] · σ_e −94 %) · `kawaguchi2017_dry_coating_parametric_na2so4_model_se` (ref [13]) · `kawaguchi2018_dry_coating_model_se_particle_powtec` (ref [14]).
- 코팅 + 도전재 · 껍질 전도: `kissel2026_mechanofusion_derived_cathode_composite_microstructures_scalable` (CB 든 Li₃InCl₆ 껍질) · `kim2025_conductive_agent_se_coating_cathode` (같은 질문 · 반대 결론 · §7-3) · `lee2026_lpscl_coating_thickness_ncm811` (껍질 두께 ↔ σ_e) · `kim2024_optimal_cathode_composite_mechanical_mixing_se_coverage` (껍질 몫 최적) · `kim2023_mechanofusion_ncm811_lpscl_core_shell_intimate_contact`.
- 무탄소 복합 양극 σ_e (전자 접점망): `strauss2018_cam_particle_size_inactive_ncm622_electronic_percolation` · `siroma2016_ac_impedance_tlm_electron_electron_connection_effective_conductivity_assb` (ref [23] · 이온 차단 셀 방법) · `asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity` (ref [24]).
- 건식 공정 · 혼합: `frankenberg2025_milling_dry_processed_sulfide_cathode_microstructure` (ref 63) · `wolf2026_extruder_vs_batch_mixing_core_shell_dry_sulfide_cathode` · `nam2018_dry_vs_slurry_mixed_electrode_binder_coverage_premixing_pouch` (ref [7]) · `pfeffer2001_dry_particle_coating_engineered_particulates` (ref [17]) · `sakuda2011_pld_sulfide_se_coated_licoo2_composite_cathode` (ref [11] · PLD 코팅).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
