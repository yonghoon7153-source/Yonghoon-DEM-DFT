# 크기 이원 (bimodal) 분말의 탄소성 단축 압축 — EDEM-EEPA DEM (3D · GPU · 큰 입자 지름 50 µm + 작은 입자 12.5 µm (크기비 4 · 대조 = 크기비 1 단분산) · 작은 입자 부피 몫 Vf 0 · 0.1 · 0.3 · 0.5 · 물성은 모두 NCM111 (E 만 절반 71 GPa) · 접촉 소성비 λp 0 · 0.38 · 0.5 · 0.7 을 한 계산의 모든 접촉에 같게) · 400 MPa → 0.02 s 유지 → 제하 · S-S 곡선 · 압축 에너지 (Ee · Ep) · 공극 · 배위수 · 큰–큰 / 큰–작은 / 작은–작은 접촉 수 · 면적 + SI (JKR → EEPA f₀ 환산 · Δγ · x 민감도 · 배위수 시계열 · 힘–변위 곡선) · 실험 없음 — 矢野 Yano · 大崎 Ohsaki (교신) · 仲村 Nakamura · 綿野 Watano (Adv. Powder Technol. 2023)

> slug `yano2023_eepa_bimodal_size_plasticity_compression_dem` · DOI `10.1016/j.apt.2023.104245` · type `DEM (EDEM 2019 EEPA, 3D GPU, bimodal-size NCM-property spheres 50/12.5 um, uniaxial die compression 400 MPa + 0.02 s hold + unloading, compression-energy analysis; no experiment)` · PDF `4090b479-26._Compression_properties_of_bimodal_powders_with_different_plasticities_in_the_elastoplastic_powder_compression_process_A_numerical_analysis.pdf` (본문 10 쪽) + SI `798457d1-26._Sup_Compression_properties_of_bimodal_powders_with_different_plasticities_in_the_elastoplastic_powder_compression_process_A_numerical_analysis.pdf` (Supplementary Material 10 쪽) · digested `2026-11-12` · status ✅
> topic: contact_plasticity (EEPA λp · 크기 이원 압축 · 작은 입자 최적 비 · 접촉 종류 분해)
> elements: Li, Ni, Co, Mn, O (NCM111 물성만 빌린 계산 · 실험 없음)
> methods: DEM (EEPA, EDEM 2019, GPU), uniaxial die compaction + 0.02 s hold + unloading, compression energy analysis (Ee · Ep · FW), contact-type decomposition (C-C · C-F · F-F)
>
> **원제**: *Compression properties of bimodal powders with different plasticities in the elastoplastic powder compression process: A numerical analysis* [인쇄 p.1]
> **이웃 카드 (링크만)**: [`yano2024_eepa_binary_mixture_plasticity_compression_dem`](yano2024_eepa_binary_mixture_plasticity_compression_dem.md) (같은 그룹 짝 · 후보 N-25 — 이 논문을 [22] 로 인용 · '성분마다 소성이 다른' 이원 혼합은 그쪽) · [`yano2026_se_psd_width_ionic_tortuosity_dem`](yano2026_se_psd_width_ionic_tortuosity_dem.md) (같은 그룹 · 이 논문을 ref 48 로 f₀ 설정 근거로 인용 — f₀ 세 값이 이 논문 표 2 와 같은 수 · §0-1) · [`morrissey2013_eepa_elastoplastic_adhesion_dem_iron_ore_fines_thesis`](morrissey2013_eepa_elastoplastic_adhesion_dem_iron_ore_fines_thesis.md) (EEPA 원전) · [`thakur2014_eepa_adhesive_elastoplastic_dem`](thakur2014_eepa_adhesive_elastoplastic_dem.md) (EEPA 학술지 판 · 이 논문 ref [32]) · [`thorntonning1998_adhesive_elastoplastic_contact`](thorntonning1998_adhesive_elastoplastic_contact.md) (ref [30] — 인용만) · [`johnson1971_jkr_surface_energy_contact_elastic_solids`](johnson1971_jkr_surface_energy_contact_elastic_solids.md) (JKR · ref [27] — f₀ 환산의 바탕).
> **판독 원자료**: `litdb/figures/yano2023_eepa_bimodal_size_plasticity_compression_dem/digitized.csv` (301 행 — 벡터 경로 · 막대) · 크롭 **70 장** = 그림 18 (본문 11 · SI 7) · 표 4 (본문 2 · SI 2) · 식 28 (본문 24 · SI 4 · 번호마다 한 장) · 근거 문단 20 — `figures.json`.

<!-- 실독 기록 (2026-11-12)
     원문 = Advanced Powder Technology 34 (2023) 104245 · 본문 10 쪽 (PDF 1–10 = 논문 쪽 1–10) + Supplementary Material 10 쪽 (Word 출력 · 쪽 번호 1–10).
     PDF = Elsevier (Acrobat Distiller) · 텍스트 층 온전 → 쪽별 텍스트 전부 읽고, 식 28 개는 300 dpi 크롭 이미지에서 다시 읽음 (텍스트 층은 위첨자 · 분수 · 그리스 문자가 깨짐: λp → 'kp', Δγ → 'Dc', ζ_tm → 'ftm', μ → 'l').
     값 표지: [인쇄] = 본문 · 표 · 식 · 그림 안 글자 · [벡터 판독] = PDF 경로 좌표 (PyMuPDF get_drawings) — 축 = 눈금선 · 틀 모서리에 숫자 이름표를 맞춤 ·
     표지 = bbox 중심 · 곡선 = 선 꼭짓점 · 막대 = 채운 사각형 윗변 → digitized.csv 301 행 · [판독] = 래스터 (그림 4) 를 눈으로 읽은 것 ·
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 추론] = 이 카드의 해석 · [미확인] = 원문에 없음.
     크롭 70 장: 도구 (tools/litdb/extract_figures.py) 17 장은 전부 다시 자름 (그림 1 = 그림 2 와 두 단 합침 + 쪽 번호 · 캡션 빠짐 13 장 · 표 2 = 쪽 전체 · 표 S1 = 그림 S2 섞임 · 표 S2 = 위 본문 섞임) +
     도구가 못 낸 5 장 (그림 2 · 3 · 11 · S6 · 표 1) 손 크롭 · 식 28 장 · 근거 문단 20 장 (세 장은 두 단 · 두 쪽에 걸친 한 문단을 위아래로 이어 붙임) — 전부 열어 확인.
     중복 확인: 정본 litdb/papers/ 목록 (git ls-tree) · DOI '104245' · 'bimodal powders with different' · yano · ohsaki grep → 이 논문 카드 없음 (yano2024 L90 · L500 · yano2026 L425 가 인용만). -->

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 오사카 공립대 大崎 그룹이 EDEM 2019 의 **EEPA 접촉 법칙 (n 1.5)** 으로 NCM111 물성 (밀도 4.75 g/cm³ · ν 0.25 · E 는 계산 비용 때문에 **절반 71 GPa**) 의 구를 **크기 이원** (큰 50 µm + 작은 12.5 µm · 크기비 4 · 대조 크기비 1 = 단분산) 으로 섞어 (작은 입자 부피 몫 **Vf 0 · 0.1 · 0.3 · 0.5** · 전체 입자 부피 0.201 mm³ = Vf 0.5 에서 ≈ 10 만 개) 지름 0.9 mm 원통에서 위 펀치 25 mm/s 로 **400 MPa** 까지 누르고 **0.02 s 유지** 뒤 같은 속도로 뺐다.  접촉 소성비 λp (= 1 − k₁/k₂) 는 **0 · 0.38 (NCM 값) · 0.5 · 0.7 (Li₃PS₄ 값)** 을 한 계산의 **모든 접촉에 같은 값**으로 줬다 — 두 성분의 소성이 다른 계가 아니다 (그것은 짝 논문 yano2024).  결과: λp ↑ 와 작은 입자 ↑ 가 둘 다 치밀화 · Ep/Ee ↑ · 탄성 쪽 (λp 0 · 0.38) 은 **Vf 0.3 이 공극 최소**인데 λp 0.7 (과 그림상 0.5) 은 **Vf 0.5 가 최소** — 소성이 '작은 입자 최적 비' 를 옮긴다 · 작은 입자가 늘면 접촉 면적이 가장 큰 종류가 **큰–큰 → 큰–작은 → 작은–작은** 으로 바뀐다 (그림상 λp ≥ 0.38 에서만 — λp 0 은 Vf 0.1 에서 이미 큰–작은) · 실험 검증 없음 (*"In future work … X-ray computed tomography"*).

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 의도 '소성이 다른 이원 분말' 인가 | **아니다.**  '이원' = **크기 이원** · λp 는 계산마다 *"λp of all contacts between particles were set to same values in each condition"* (p.4) · 제목의 *"different plasticities"* = λp 를 바꾼 **여러 계산** · 성분마다 λp 가 다른 이원 혼합 (+ 이종 접촉 규칙 0.60) = 짝 논문 yano2024 (N-25) | [인쇄] p.4 · 표 2 |
| ② 0.619 · 0.642 · 0.38 | **0.38 = 있음** (NCM · ref [38] Cheng 2017 · *"λp of NCM and Li₃PS₄ … were 0.38 [38] and 0.7 [39]"*) · **0.619 · 0.642 · LPSCl = 없음** (본문 · 표 · SI 전수 문자열 0 건) · 이 논문의 SE 쪽 값 = **Li₃PS₄ 0.7** (ref [39] Baranowski 2016) · 0.5 = *"the median value of battery materials"* · ★ f₀ 세 값 (큰–큰 −1.05 × 10⁻⁵ · 큰–작은 −4.19 × 10⁻⁶ · 작은–작은 −2.62 × 10⁻⁶ N) = yano2026 표 3 의 NCM–NCM · NCM–LPSCl · LPSCl–LPSCl f₀ (−1.047 × 10⁻⁵ · −4.189 × 10⁻⁶ · −2.618 × 10⁻⁶) 와 **같은 수** = (8/3)π × 0.1 J/m² × R\* (R\* 12.5 · 5 · 3.125 µm = 지름 50 · 12.5 µm 쌍) [카드 산술] | [인쇄] p.4 · 표 2 · SI 식 (S4) |
| ③ **d** — 단단한 입자의 하중 몫 · 재밍 | **하중 몫 값은 없다** (입자 응력 · 힘 사슬 · 반력 분할 없음).  정성 문장 하나: *"The fine particles located in the interstitial voids of the coarse particles are not subjected to compressive forces because of the force chain formed by the coarse particles."* (p.8) · 대리 = 종류별 평균 배위수 (그림 9) · 큰–작은 접촉 수 · 면적 (그림 10 · 11) · ⚠ 두 크기가 **같은 재료 · 같은 λp** (강성 대비 0) — 우리 AM (단단) + SE (무름) 의 하중 분담과 다른 계 | [인쇄] p.8 · [벡터 판독] 그림 9–11 |
| ④ **e** — 점접촉 법칙 · 대안 · 맞춘 값 수 | **EEPA** 식 (1)–(24) 전부 + SI 의 JKR → f₀ 환산 식 (S1)–(S4) · **실험에 맞춘 값 0** (λp = 문헌 나노압입값 · 0.5 = '중앙값' · f₀ = 앞 연구 [28] 의 JKR γ 0.1 J/m² 를 0 겹침 힘으로 · x · Δγ = SI 민감도로 고정 · ζ_tm 0.67 = 문헌 2/3 · E 절반 = 계산 비용) · 큰 변형 범위 · 대안 법칙 비교 **없음** (Thornton–Ning [30] · Thornton–Cummins–Cleary [29] · He et al. [31] 인용만) | [인쇄] p.2–4 · SI §S2 · §S3 |
| ⑤ **b** — 뺄 때 되돌아옴 | **S-S 제하 (그림 5) · 펀치 힘–변위 (그림 S7) · Ee (그림 6)** — 회복 진변형률 (최대 → 1 MPa) 크기비 1: **0.123 · 0.103 · 0.103 · 0.098** (λp 0 · 0.38 · 0.5 · 0.7) · 크기비 4 · Vf 0.3: **0.100 · 0.086 · 0.085 · 0.094** (높이 +8.9 – +13.1 %) · ★ 크기비 4 에서 **0.02 s 유지 동안 펀치 위치는 그대로인데 힘이 6.2 · 12.5 · 15.7 · 25.9 % 떨어진다** (크기비 1 = ≤ 0.2 %) | [벡터 판독] 그림 5 · S7 · [카드 산술] |
| ⑥ **a · i** — 기공 | 순수 SE 없음 · 한 압력 (400 MPa) · 그림 7 공극 (중앙 0.8 원통 · **시점 미기재 — 뺀 뒤로 보인다** ⑩) **0.198–0.421** (§3c) · SI 그림 S3 (단분산 λp 0) = 충전 0.52 · **400 MPa 누른 채 0.222–0.245** · 뺀 뒤 0.366 | [벡터 판독] 그림 7 · S3 |
| ⑦ **k** — DEM 한계 (원문 문장) | *"In the EEPA model, the plastic deformation of the particles is expressed as an overlap between particles while maintaining their shape, whereas the cohesive force is considered a constant pull-off force."* (p.3) · *"Particle deformation was expressed as particle overlap, whereas the particle shape remained spherical."* · *"the contact area calculated using this method would be underestimated as the contact area increases, owing to particle deformation in the real particles."* (p.5) · 상수 점착 ↔ 크기 따라 다른 실제 점착 (SI p.2) — §4g | [인쇄] |
| ⑧ **l** — 소성이 왜 어려운가 · 우회 · 비용 | 원문 이유 = 탄소성 모델 연구 다수가 실제 분말의 **사례 연구**라 *"the parametric discussion of particle plasticity still needs to be solved"* · 미시 소성 거동 분석이 *"totally insufficient"* (p.2) · 우회 = **EEPA 접촉 강성비 (모양 불변 · 겹침)** · 비용 = **E 절반** · GPU · ≤ 10 만 입자 · 다이 18 d · Δt · 계산 시간 [미확인] | [인쇄] p.2–4 |
| ⑨ **g** — 2D ↔ 3D | **3D** (*"three-dimensional (3D) DEM simulation accelerated by graphical processing units"*, p.2) · 2D 언급 없음 | [인쇄] |
| ⑩ ★ 측정 시점 함정 | 그림 7–11 (공극 · 배위수 · 접촉 수 · 면적) 의 시점 (누른 채 / 뺀 뒤) 이 **적혀 있지 않은데, 뺀 뒤 구조로 보인다** [카드 추론 · 근거 다섯 — §3e]: 그림 10a λp 0 단분산의 접촉당 면적 **0.117 µm²** → 겹침 **1.49 nm** = EEPA 점착 평형 겹침 (f₀/k₁)^(2/3) = **1.51 nm** (누른 채라면 ≈ 145 µm² · Rumpf 어림) · 그림 8 Vf 0 λp 0 배위수 4.18 = SI S3 phase 3 (뺀 뒤) 4.16–4.25 ≠ phase 2 (누른 채) 8.94–9.30 · SI S6 누른 뒤 배위수 ≈ 8.0 ≠ 그림 8 Vf 0.3 4.54 · 5.88 · 그림 4 층 높이 ≈ 뺀 뒤 높이 → 저자의 *"Because the particles under elastic conditions cannot allow considerable overlap, the contact areas become small"* (p.8) 은 **뺀 뒤 상태**의 결과로 읽어야 한다 | [벡터 판독 · 카드 산술] |

⛔ **한정어 (떼지 말 것)**: ① 모든 입자 = **NCM111 물성 구** (E 만 계산 비용으로 절반 · SE 아님) — 큰 입자와 작은 입자는 **크기만** 다르다 ② λp 는 **모든 접촉 같음** (계산마다 하나) ③ 크기비 4 (50 / 12.5 µm) · *"Note that this study was not assumed to any specific experimental systems"* (p.4) ④ 점착 = 접촉 쌍별 **상수 f₀** (JKR γ 0.1 J/m² 의 0 겹침 힘) · Δγ 0 ⑤ 압력 한 점 (400 MPa) · 25 mm/s · 유지 0.02 s ⑥ **실험 검증 없음** ⑦ 그림 7–11 의 측정 시점 미기재 (§3e) ⑧ Δt · 전체 시간 · 시드 · 반복 수 · 벽 마찰 · 온도 [미확인].
⇒ **절대값 전이**: 하지 않는다 (공극 · 변형률 · 에너지 · 접촉 면적).  **전이 가능한 것** = (i) **접촉 소성이 크기 이원 충전의 최적 작은 입자 몫을 옮긴다** (탄성 Vf 0.3 → λp 0.7 에서 0.5) 는 방향 — 우리 AM_S : SE ≈ 4 : 1 과 같은 크기비 (ii) 크기 이원 + 접촉 소성에서 **종류별 배위수 · 접촉 수 · 면적 · 접촉당 면적** 으로 나눠 보는 꼴 (iii) **고정 위치 유지에서 작은 입자가 많은 층의 힘 완화** (6–26 % / 0.02 s) — 우리 `hold` (판 고정 → 이완) 와 같은 부류의 DEM 사례 (iv) **'누른 채 / 뺀 뒤' 표기 함정** (v) f₀ 를 **JKR 0 겹침 힘 −(8/3)πγR\*** 로 정하는 식 — yano2026 f₀ 의 뿌리.

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-26 의 '왜' 칸)

의도 원문: *"d · e — 같은 저자의 '이원 압축 DEM' (소성이 다른 이원 분말) · N-25 와 짝"* · 가리킨 카드 = `yano2026_se_psd_width_ionic_tortuosity_dem` (L425 · 제목이 카드에서 잘림) · 지시서 ★ 목록 (접촉 모델 식 · λp · 되돌아옴 / 물성 · 혼합비 · 입자 수 · 다이 · 가압 · Δt · 연화 / 압력별 기공 (누른 채 · 뺀 뒤) / 쌍별 접촉 수 · 면적 · 하중 몫 / 패킹 지표 · Heckel / 실험 검증 · SI / N-25 · yano2026 대조 · 0.619 · 0.642 · 0.38 / 저자 한계 / 우리 숫자 옆에 놓을 값).

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| "같은 저자의 '이원 압축 DEM'" | **채움** | 저자 Yano · Ohsaki (교신) · Nakamura · Watano (yano2024 · yano2026 과 같은 그룹) · §2 (p.3–5) · EDEM 2019 · EEPA · **3D · GPU** · **크기 이원** 50 + 12.5 µm (크기비 4) · 대조 크기비 1 · Vf 0 · 0.1 · 0.3 · 0.5 · 위 펀치 25 mm/s → **400 MPa → 0.02 s 유지 → 25 mm/s 로 제하 → 안정 구조** (p.5) · 온도 언급 없음 [미확인] · 그림 7–11 시점 미기재 (뺀 뒤로 추정 — §3e) |
| "(소성이 다른 이원 분말)" | **없음 — 의도가 틀렸다** | λp 는 *"of all contacts between particles were set to same values in each condition"* (p.4) — 큰 입자 · 작은 입자 · 이종 접촉 모두 같은 λp · 제목의 *"bimodal powders with different plasticities"* = 크기 이원 분말을 λp 0 · 0.38 · 0.5 · 0.7 로 각각 계산 · 성분마다 λp 가 다른 이원 혼합 = yano2024 (N-25) |
| "d (단단한 입자의 하중 몫 · 재밍)" | **일부** | 하중 몫 · 힘 사슬 · 응력 분할 값 **없음** · 정성 문장 (p.8 force chain) · 종류별 배위수 (그림 9) · 큰–작은 접촉 수 · 면적 (그림 10 · 11) · 강성 대비 0 (같은 재료) |
| "e (점접촉 법칙 · 대안 · 맞춘 값 수)" | **일부** | EEPA 식 (1)–(24) · JKR → f₀ (S1)–(S4) · 맞춘 값 0 (§6-e) · 대안 법칙 비교 · 큰 변형 범위 **없음** |
| "N-25 와 짝" | **채움** | 같은 물성 묶음 (NCM111 · E 71 GPa 절반 · ν 0.25 · ρ 4.75 · 반발 0.25 · 정지 마찰 0.5 · 구름 마찰 0.01) · 같은 다이 (0.9 mm · 0.636 mm³) · 같은 f₀ (큰–큰 = 단분산 50 µm −1.05 × 10⁻⁵ N) · n 1.5 · x 1 · Δγ 0 · ζ_tm 0.67.  다른 점: 이 논문 = 크기 이원 · λp 모든 접촉 같음 (0 · 0.38 · 0.5 · 0.7) · **400 MPa** · EDEM **2019** · 실험 없음 / yano2024 = 단분산 · 성분 λp 0.38 · 0.70 + 이종 규칙 0.60 · **300 MPa** · EDEM 2023.0 · NCM–Na₂SO₄ 실험.  yano2024 가 이 논문을 [22] 로 인용 (*"単一材料で λp を上げた"* Ep/Ee 증가 — 그림 6b 와 맞다) |
| (★) DEM 접촉 모델 · 식 · λp 정의 · 값 · 근거 · 하중 뺄 때 곡선 | **채움** | 식 (4) 세 가지 (처녀 재하 k₁ · 제하/재하 k₂ · 점착 k_adh) — **제하 곡선이 모델에 있다** (그림 1 · p.3 가지 규칙) · λp = 1 − k₁/k₂ = 1 − E₁\*/E₂\* (식 7) · 값 = 표 2 · 근거 = 나노압입 문헌 [38] · [39] (λp 를 얻은 방법 [미확인]) |
| (★) 물성 · 혼합비 · 입자 수 · 다이 · 가압 · Δt · 연화 | **채움 (Δt 없음)** | 표 1 · 2 · p.4–5 (§3a) · 입자 수 = 카드 산술 (§3a) · Δt · 전체 시간 [미확인] · E 절반 = *"to reduce the simulation costs"* (공극 맞춤 아님) |
| (★) 압력별 상대밀도 · 기공 (누른 채 / 뺀 뒤) | **일부** | 압력 **한 점** (400 MPa) · 그림 7 (시점 미기재) · SI 그림 S3–S5 phase 1 (충전) · 2 (400 MPa 누른 채) · 3 (뺀 뒤) — 단분산만 · S-S 곡선 (변형률 축) · 층 평균 재구성 [카드 산술 · 가정 · §3e] |
| (★) 쌍별 접촉 수 · 면적 · 하중 몫 | **일부 (하중 몫 없음)** | 그림 9–11 · 종류별 접촉 수 · 접촉당 면적 = 카드 산술 (§3d) |
| (★) 패킹 지표 · 소성이 치밀화 · 접촉 면적을 바꾸는 방식 · Heckel | **일부** | 배위수 · 공극 · 접촉 면적 (그림 7–11) · Ep/Ee (그림 6) · **Heckel 없음** (카드 재구성 P_y = §3e · 인용 금지) |
| (★) 실험 검증 | **없음** | *"In future work, the microscopic properties will be experimentally investigated using X-ray computed tomography"* (p.9) |
| (★) SI 전부 | **채움** | 그림 S1–S7 · 표 S1 · S2 · 식 (S1)–(S4) (§3f) |
| (★) 0.619 · 0.642 · 0.38 | **0.38 = 있음 · 0.642 · 0.619 = 없음** | 위 ② |
| (★) 저자 한계 | **채움** | §4g |

**2 차 인용 대조 (카드 문제 — 고치지 않음)**:
- `yano2026_*` **L425** (참고문헌 48): *"T. Yano, S. Ohsaki, H. Nakamura, S. Watano, Compression properties of bimodal powders with different plasticities …, Adv. Powder Technol. 34 (2023) 104245 \| 같은 저자 이원 압축 DEM — 카드 없음"* — 서지는 원문과 같다 (제목 뒷부분 *"in the elastoplastic powder compression process: A numerical analysis"* 를 '…' 로 줄임) · '카드 없음' 은 이 카드로 낡았다 · '이원 압축' 은 **크기 이원** 이다.
- `yano2026_*` **L191** (*"f0 설정 \| Hertz–Mindlin + JKR 의 0 겹침 점착력에 맞춤 · 표면에너지 0.1 J/m² (refs 47–48)"*) — 이 논문 (ref 48) p.4 *"f₀ was set as the cohesive force at the overlap = 0 in the condition of the JKR surface energy … JKR surface energy of 0.1 J/m²"* · SI 식 (S1)–(S4) 와 **같다**.
- `yano2026_*` **L190** (표 3 f₀: NCM–NCM −1.047 × 10⁻⁵ · NCM–LPSCl −4.189 × 10⁻⁶ · LPSCl–LPSCl −2.618 × 10⁻⁶ N) — 이 논문 표 2 의 큰–큰 · 큰–작은 · 작은–작은 **−1.05 × 10⁻⁵ · −4.19 × 10⁻⁶ · −2.62 × 10⁻⁶ N** 과 같은 수 (유효숫자만 다름) · 식 (S4) 에 R\* 12.5 · 5 · 3.125 µm (지름 50 · 12.5 µm 쌍) 를 넣으면 정확히 1.0472 · 0.4189 · 0.2618 × 10⁻⁵ N [카드 산술] → yano2026 (NCM 65–113.5 µm · LPSCl 7.6–55.9 µm · 입자 ×10) 이 이 논문의 50 / 12.5 µm 값을 그대로 썼을 수 있다 [카드 추론].
- `yano2026_*` **L153** (§3g · f₀ 줄): *"f0 = 1.5πγR\* (γ 0.1 J/m²) 로 읽으면 R\* 22.2 · 8.9 · 5.6 µm (어느 반경을 썼는지 [미확인])"* — **원 식이 다르다**: 이 논문 (yano2026 의 ref 48) 식 (S4) **f₀ = −(8/3)πγR\*** → R\* = **12.5 · 5.0 · 3.125 µm** · '1.5π' 꼴은 이 논문 식 (8) **f_min = (3/2)πΔγR_a** (Δγ · 접촉 반경 R_a — f₀ 가 아님) 이다.  (같은 지적이 yano2024 카드 §0-1 에도 있다 — 이 논문이 직접 원전.)
- `yano2026_*` **L192** (*"λp 출처 \| NCM 0.38 (Cheng 2017 ref 49) · LPSCl 0.642 (Papakyriakou 2021 ref 50) · 이종 접촉 = 등가 소성비 0.619 (Yano 2024 ref 51)"*) — NCM 0.38 · Cheng 2017 = 이 논문 [38] 과 **같다** · 이 논문에는 0.642 · 0.619 · LPSCl 이 없다 (SE 쪽 = Li₃PS₄ 0.7).
- `yano2024_*` **L90 · L299 · L500** (*"[22] EEPA 단일 분말의 소성 · 입도 분포 영향 … Ep/Ee 증가 거동이 비슷 … 카드 없음 (후보 N-26 · PDF 받음)"*) — 서지 · 서술이 원문과 맞다 (단일 재료 · λp 를 올리면 Ep/Ee ↑ = 그림 6b) · '카드 없음' 은 낡았다.

⇒ **의도 대조 결과: 일부** — 같은 저자의 이원 압축 DEM (크기 이원 · EEPA · 400 MPa 가압 → 유지 → 제하) 은 **채움** · '소성이 다른 이원 분말' 은 **없음** (λp 는 계산마다 모든 접촉 같은 값 · 성분별 소성 차 = N-25 yano2024) · d (하중 몫) **일부** (정성 문장 하나 + 종류별 접촉 수 · 면적) · e **일부** (EEPA 식 전부 · 맞춘 값 0 · 대안 비교 없음) · 0.38 **있음** · 0.619 · 0.642 **없음**.

---

## 1. 한 줄 요약

EEPA 접촉 법칙 (n 1.5 · 상수 점착 f₀ = JKR γ 0.1 J/m² 의 0 겹침 힘) 의 NCM111 물성 구 (E 절반 71 GPa) 를 큰 50 µm · 작은 12.5 µm 의 크기 이원 (크기비 4 · 작은 입자 부피 몫 Vf 0–0.5) 과 크기비 1 대조로 3D DEM (EDEM 2019 · GPU) 에서 400 MPa 까지 단축 압축 → 0.02 s 유지 → 제하했고, 모든 접촉의 λp 를 0 · 0.38 · 0.5 · 0.7 로 바꿨다.  λp ↑ → 400 MPa 진변형률 −0.156 → −0.310 (크기비 1) · −0.262 → −0.330 (크기비 4 · Vf 0.3) · Ep/Ee 0.46 → 2.53 · 0.92 → 4.93 [벡터 판독] (작은 입자가 있으면 같은 λp 에서 Ep/Ee 가 크다 — 저자: 재배열이 세진다) · λp 0 에서도 Ep ≠ 0 (재배열).  공극 (중앙 0.8 원통): 탄성 쪽은 Vf 0.3 최소 (λp 0: 0.286 · Vf 0.5 0.324) · λp 0.7 은 Vf 0.5 최소 (0.198) — 저자 해석: 작은 입자의 두 효과 (빈틈 채움 ↔ 큰 입자 자리를 성긴 작은 입자 덩어리가 대신) 중 뒤의 것이 소성에서 약해진다 (덩어리가 소성으로 조밀).  배위수: 탄성은 ≈ 4.2 그대로 · 소성은 Vf 0.1 에서 최소 뒤 상승 (작은 입자 배위수가 소성에서 크게 오른다 · 큰 입자 사이 빈틈의 작은 입자는 큰 입자의 힘 사슬 때문에 눌리지 않는다).  접촉 면적: 작은 입자 ↑ → 총 · 작은–작은 ↑ · 큰–작은 은 Vf 0.1 → 0.3 에서 크게 늘고 0.3 → 0.5 에서 평평 (큰 입자 하나당 큰–작은 면적은 늘지만 큰 입자 수가 준다).  결론: *"it is important to determine the optimal addition ratio of fine particles based on the plastic deformability of the material"* (p.9).

## 2. 메타 / 동기 / 질문

| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| **Takeru Yano** · **Shuji Ohsaki\*** (교신 · shuji.ohsaki@omu.ac.jp) · Hideya Nakamura · Satoru Watano — Department of Chemical Engineering, Osaka Metropolitan University (Sakai, Osaka 599-8531) | **Advanced Powder Technology 34 (2023) 104245** · Original Research Paper · 접수 2023-06-16 · 수정 2023-10-05 · 승인 2023-10-14 · 온라인 2023-10-19 | 10.1016/j.apt.2023.104245 | **NCM111 (LiNi₁/₃Co₁/₃Mn₁/₃O₂) 물성의 가상 구** (*"The powder properties were assumed to be those of … (NCM) used in all-solid-state lithium-ion batteries"*) · λp 값만 NCM (0.38) · Li₃PS₄ (0.7) 문헌에서 | DEM (EDEM 2019 · EEPA · GPU) · 실험 없음 |

- **키워드 (p.1)**: Discrete element method · Elastoplastic compression · Two-component mixture · Packing structure · Contact area.
- **동기 (p.1–2)**: 분말 압축 = 충전 · 압축 · 제하 [6] · 배출 [7] · 이원 혼합의 최적 비가 고밀 충전을 준다 [8] · 점착이 공극을 바꾼다 [9] · 압축 중 재배열 [12] · 탄성 · 소성 변형 [13, 14] · 취성 파쇄 [15] 가 동시에 일어난다 [16] · 벌크 압축 특성 ↔ 성형체 특성 연구는 있으나 *"the analysis of microscopic behavior of plastic deformation is totally insufficient. The effects of cohesiveness and plasticity on powder compression still need to be clarified owing to the interactions among multiple factors."* (p.2) · JKR [27] · 같은 저자의 앞 연구 [28] (점착이 작은 입자 응집으로 접촉 수를 바꾼다) · Thornton–Ning [30] · He et al. [31] (Hertz + Thornton–Ning 로 형상 효과) · EEPA (Thakur [32]) · Zhang [33] (LIB 전극 압연 EEPA DEM ↔ 실험) 를 든 뒤 *"Most previous studies using the elasto-plastic models are case studies for individual actual powders, and the parametric discussion of particle plasticity still needs to be solved."* (p.2).
- **이원 크기의 근거**: *"Regarding the elastic powder with bimodal size distribution, both of experimental [34,35] and numerical study [28] reported that the volume mixing ratio of fine particles, which packed the powder bed most densely, was around 0.3."* (p.2) · 앞 연구 [28] 에서 작은 입자 효과가 크기비 4 에서 나타났다 (p.4).
- **질문**: 접촉 소성 (λp) 과 크기 이원 (Vf · 크기비) 이 ① S-S · 압축 에너지 ② 공극 · 배위수 · 접촉 면적 (접촉 종류별) 을 어떻게 바꾸나 · 작은 입자 최적 비가 소성에 따라 달라지나.
- **자금 (p.9)**: JSPS KAKENHI JP22KJ2617 · JP23H01748 · JPJSJRP20221606 · JST 大学フェローシップ創設事業 JPMJFS2138 · Hosokawa Powder Technology Foundation (20505) · 영문 교정 Editage.  이해상충 없음 진술 · 데이터 · 코드 공개 진술 없음 · SI = Appendix A.

---

## 3. 핵심 수치 총정리 ★

### 3a. 계산 조건 (표 1 · 표 2 · 표 S1 · S2 · p.4–5 · SI) [인쇄]

| 항목 | 값 | 비고 |
|---|---|---|
| 코드 · 기계 | **EDEM 2019 (Altair)** · *"three-dimensional (3D) DEM simulation accelerated by graphical processing units"* · CPU · GPU 기종 · 코어 수 [미확인] | p.2 |
| 입자 | 큰 입자 지름 **50 µm** · 크기비 d_c/d_f **1 · 4** (→ 작은 입자 12.5 µm [카드 산술]) · 밀도 **4.75 g/cm³** · 총 입자 부피 **0.201 mm³** (본문 *"0.20 mm³, which is the volume of 100,000 particles at a size ratio of 4 and a volume mixing ratio of 0.5"*) · 작은 입자 부피 몫 Vf **0–0.5** (그림 = 0 · 0.1 · 0.3 · 0.5) · 푸아송비 **0.25** · 영률 **71 GPa** (*"only Young's modulus was halved to reduce the simulation costs"* — 절반 전 142 GPa [카드 산술] · 표의 값 = E₂ · EDEM 입력 E₁ = 식 (7) 로 계산) · 반발 계수 **0.25** · 정지 마찰 **0.5** · 구름 마찰 **0.01 (default)** · 운동 마찰 μ (식 17) 값 [미확인] | 표 1 · p.4 |
| 입자 수 [카드 산술 · V = 0.201 mm³] | Vf 0 (= 크기비 1 단분산): **3,071** · Vf 0.1: 큰 2,764 + 작은 19,655 = **22,419** · Vf 0.3: 2,150 + 58,964 = **61,114** · Vf 0.5: 1,536 + 98,274 = **99,809** · 작은 / 큰 개수비 = 64 Vf/(1 − Vf) (7.1 · 27.4 · 64) · 실제 입자 수는 원문에 없다 [미확인] — 같은 다이 · 같은 지름의 짝 논문 yano2024 단분산은 3,077 개 [그 카드 · 인쇄] (= 0.2014 mm³ → 0.201 은 반올림으로 보인다 · 0.2 % 차) | 본문 '≈ 10 만' ✓ |
| 다이 (그림 S1) | 평평한 위 · 아래 펀치 **0.45 mm** (반지름 — 면적 0.6362 mm² → 400 MPa = **254.5 N** [카드 산술]) · 원통 안지름 **0.9 mm** · 높이 **1.0 mm** · 부피 **0.636 mm³** · 다이 지름 = **18 d_c = 72 d_f** [카드 산술] | 표 1 · SI §S1 |
| 접촉 소성비 λp (*Contact Plasticity Ratio*) | **0 · 0.38 · 0.5 · 0.7** — 0 = *"perfect elastic material"* · 0.38 = NCM [38] · 0.7 = Li₃PS₄ [39] · 0.5 = *"the median value of battery materials"* · **모든 접촉에 같게** | 표 2 · p.4 |
| E₁ (EDEM 입력 · 하중) [카드 산술] | E₁ = (1 − λp) E₂ → **71 · 44.0 · 35.5 · 21.3 GPa** (같은 재료끼리 E₁\*/E₂\* = E₁/E₂) | 식 (7) |
| 끌림 (점착) | 일정 끌림 힘 f₀: 큰–큰 **−1.05 × 10⁻⁵ N** · 큰–작은 **−4.19 × 10⁻⁶** · 작은–작은 **−2.62 × 10⁻⁶** (*"f₀ was corresponding to JKR surface energy of 0.1 J/m² which was the critical value acting on the packing structure by particle cohesion as reported in [28]"*) · meso 표면에너지 Δγ **0 J/m²** | 표 2 · p.4 · SI 식 (S4) |
| 지수 · 접선 | Slope Exp (n) **1.5** · Tensile Exp (x) **1** · Tangential Stiff Multiplier ζ_tm **0.67** (*"2/3 is the ideal model for nonlinear elastic materials, as proposed by Di Renzo and Di Maio [36] and proved by Kruggel–Emden et al. [37]"*) | 표 2 · p.4 |
| 하중 이력 | 원통 안에 무작위 생성 → 중력 충전 → 안정 구조 → 위 펀치 **25 mm/s** 하강 → 위 펀치 압력 **400 MPa** → *"loaded with a pressure of 400 MPa for 0.02 s"* → 위 펀치 **25 mm/s** 상승 → *"The calculation was completed after obtaining a stable structure after release from the pressure."* | p.4–5 |
| 시간 | Δt · 전체 계산 시간 · 벽시계 시간 [미확인] · 그림 S6 시간 축 0.03–0.05 s · (짝 논문 yano2024 = Δt 2 × 10⁻⁹ s [그 카드 · 인쇄] — 이 논문 값으로 옮기지 않는다) | — |
| SI 비교 계산 (표 S1 · S2) | 단분산 50 µm · λp **0** · JKR 표면에너지 0.1 J/m² ↔ EEPA f₀ −1.05 × 10⁻⁵ N · 표 S1 ζ_tm **1** · 표 S2: Δγ **0 · 4 · 8 · 100 J/m²** · x **1 · 2.5** (그림 S5 는 1 · 2.5 · 5) · ζ_tm 0.667 | SI p.4 · p.6 |

### 3b. 거시 결과 — S-S · 힘–변위 · 에너지 (그림 5 · 6 · S7) [벡터 판독 · 비 = 카드 산술]

| λp | 0 | 0.38 | 0.5 | 0.7 |
|---|---|---|---|---|
| **크기비 1** — 최대 압력 (MPa) · 그때 진변형률 | 398.8 · −0.156 | 399.3 · −0.211 | 398.8 · −0.244 | 399.3 · −0.310 |
| 크기비 1 — 1 MPa 로 내려온 잔류 진변형률 · 회복 Δε · 높이 증가 e^Δε − 1 | −0.033 · 0.123 · 13.1 % | −0.108 · 0.103 · 10.8 % | −0.141 · 0.103 · 10.9 % | −0.212 · 0.098 · 10.3 % |
| **크기비 4 · Vf 0.3** — 최대 압력 · 진변형률 | 393.4 · −0.262 | 399.6 · −0.294 | 400.4 · −0.3125 | 399.6 · −0.330 |
| 크기비 4 — 잔류 · Δε · 높이 증가 | −0.162 · 0.100 · 10.5 % | −0.208 · 0.086 · 9.0 % | −0.228 · 0.085 · 8.9 % | −0.235 · 0.094 · 9.9 % |
| 그림 S7 위 펀치 최대 힘 (N) | 254.1 (1) · **248.7 (4 — 391 MPa)** | 254.1 · 253.7 | 254.1 · 254.1 | 254.4 · 253.9 |
| ★ 0.02 s 유지 끝 힘 (N · 펀치 위치 그대로) — 크기비 1 · 4 | 253.6 · **233.4 (−6.2 %)** | 254.1 · **222.0 (−12.5 %)** | 254.1 · **214.2 (−15.7 %)** | 254.0 · **188.2 (−25.9 %)** |
| 펀치가 힘 0.5 N 아래로 떨어지는 위치 − 최대 위치 (µm · 되튐) — 1 · 4 | 66.7 · 41.3 | 52.2 · 32.8 | 51.7 · 33.0 | 46.2 · 36.4 |
| 아래 (반대) 펀치 최대 힘 ÷ 위 펀치 최대 힘 — 1 · 4 | 0.62 · 0.84 | 0.69 · 0.78 | 0.69 · 0.78 | 0.69 · 0.72 |
| Ep · Ee (mJ · 그림 6a) — 크기비 1 | 1.8 · 4.01 | 4.0 · 3.40 | 4.9 · 3.40 | 6.9 · 2.77 |
| Ep · Ee (mJ) — 크기비 4 · Vf 0.3 | 2.2 · 2.49 | 3.9 · 1.85 | 4.9 · 1.66 | 6.9 · 1.42 |
| Ep/Ee (그림 6b) — 크기비 1 · 4 | 0.464 · 0.916 | 1.175 · 2.115 | 1.465 · 2.991 | 2.533 · 4.934 |
| 위 펀치 압축 일 W (그림 S7 하중 가지 넓이 · mJ) — 1 · 4 [카드 산술] | 7.78 · 5.22 | 10.03 · 7.05 | 11.03 · 8.58 | 13.37 · 10.65 |
| FW ≈ W − Ep − Ee (mJ · W 대비) — 1 · 4 [카드 산술] | 1.97 (25 %) · 0.53 (10 %) | 2.63 (26 %) · 1.30 (18 %) | 2.73 (25 %) · 2.02 (24 %) | 3.70 (28 %) · 2.33 (22 %) |

- **크기비 4 의 유지 중 힘 완화**: 펀치 위치가 고정된 채 (λp 0 은 처음 0.6 µm 내려간 뒤 고정) 힘이 수직으로 떨어진다 — 그림 5b 의 압력 수직 하강 (391 → 367 · 399 → 349 · 399 → 337 · 399 → 296 MPa) 과 같다 [벡터 판독].  본문은 *"loaded with a pressure of 400 MPa for 0.02 s"* 라 적었지만 그림은 **위치 유지**다 [카드 추론].  크기비 1 은 힘이 그대로 (≤ 0.2 %).
- **Ee 검산**: 그림 S7 제하 가지 넓이 = 크기비 1 · 4.08 · 3.62 · 3.47 · 3.06 · 크기비 4 · 2.62 · 1.92 · 1.74 · 1.43 mJ ↔ 그림 6a Ee 와 +1 – +11 % [카드 산술] — 그림 S7 이 에너지 해석의 원자료라는 SI §S5 와 맞다 (반대 펀치 곡선은 점선이라 FW · Ep 는 넓이 재계산을 하지 않았다 — 위 FW 는 그림 6a 의 Ep · Ee 를 뺀 값).
- 저자 서술: *"Both size ratios indicated that the strain and plastic deformation of the powder beds increased under high particle plasticity conditions. Under the elastic condition (λp = 0) of dc/df = 4, the S-S curve indicates a bending point at approximately 50 MPa. This was caused by a significant change in the packing structure at approximately 50 MPa (Fig. S6)."* · *"The effect of the particle plasticity was enhanced for dc/df = 1, whereas it was small for dc/df = 4. Hence, the strain of the powder beds increased because of the change in the packing structure caused by the rearrangement of particles and not by particle deformation."* (p.5) · *"Ep of λp = 0 did not indicate zero because a bulk powder exhibits a plastic deformation due to the particle rearrangement into interstitial voids, even for elastic powders."* · *"The addition of fine particles enabled densification with less energy."* (p.5).

### 3c. 미시 결과 — 공극 · 배위수 (그림 7 · 8 · 9 · 크기비 4 · Vf 0 = 단분산 50 µm) [벡터 판독]

| λp \\ Vf | 0 | 0.1 | 0.3 | 0.5 |
|---|---|---|---|---|
| **공극** (중앙 0.8 원통 · 그림 7) λp 0 | 0.421 | 0.390 | **0.286** | 0.324 |
| λp 0.38 | 0.379 | 0.309 | **0.237** | 0.252 |
| λp 0.5 | 0.351 | 0.301 | 0.233 | **0.217** |
| λp 0.7 | 0.300 | 0.240 | 0.214 | **0.198** |
| **평균 배위수** (수 평균 · 그림 8) λp 0 | 4.18 | 4.20 | 4.54 | 4.30 |
| λp 0.38 | 5.40 | 5.15 | 6.11 | 6.84 |
| λp 0.5 | 5.81 | 5.24 | 6.22 | 7.24 |
| λp 0.7 | 6.49 | 5.39 | 5.88 | 7.76 |
| **큰 입자 배위수** N_c,coarse (그림 9a) λp 0 · 0.38 · 0.5 · 0.7 | 4.29 · 5.37 · 6.07 · 6.60 | 13.37 · 17.98 · 19.67 · 19.88 | 29.49 · 40.26 · 41.24 · 39.87 | 30.35 · 50.43 · 53.07 · 56.71 |
| **작은 입자 배위수** N_c,fine (그림 9b) λp 0 · 0.38 · 0.5 · 0.7 | — | 2.87 · 3.24 · 3.32 · 3.33 | 3.61 · 4.86 · 4.99 · 4.70 | 3.91 · 6.20 · 6.55 · 7.02 |

- **최소 공극 Vf** (굵게): λp 0 · 0.38 = **0.3** · λp 0.5 · 0.7 = **0.5** [벡터 판독].  본문 p.7 *"This trend was observed under the conditions of λp = 0.38, while it was altered under high particle plasticity conditions (λp = 0.5 and 0.7)"* 와 맞고, p.9 *"in the case of hard materials, such as metals and minerals (λp = 0–0.5), Vf = 0.3 has the lowest void fraction"* 와는 λp 0.5 에서 어긋난다 (§3g-4).
- 본문의 *"The density of the powder beds when Vf was 0.4 and more became less than the density when Vf was 0.3"* (p.7) — 그림 7 에는 **Vf 0.4 점이 없다** (0 · 0.1 · 0.3 · 0.5 넷) — 앞 연구 [28] 의 서술로 읽힌다 [카드 추론].
- **수 평균 검산**: (N_c 큰 × N_c,coarse + N_c 작은 × N_c,fine) / N = 그림 8 과 **−1.7 – +1.9 %** (12 점) [카드 산술] → 그림 8 = 그림 9 의 수 평균 ✓ (*"the average coordination number was defined as the number average"*).  ⚠ Vf 0 에서 그림 9a (4.29 · 5.37 · 6.07 · 6.60) 와 그림 8 (4.18 · 5.40 · 5.81 · 6.49) 이 같은 단분산인데 −0.6 – +4.5 % 다르다 (§3g-6).
- *"As the number of fine particles increased, the coordination number of fine particles approached asymptotically 4.2. This value indicated the average coordination number of monosized particles in this simulation as shown in the Vf = 0 condition."* (p.8) — **탄성 (λp 0: 2.87 → 3.61 → 3.91) 에만** 맞는다 · 소성 λp 0.7 은 3.33 → 4.70 → **7.02** 로 4.2 를 넘어 단분산 소성 값 (6.49) 쪽으로 간다 [벡터 판독].

### 3d. 접촉 면적 · 큰–작은 접촉 (그림 10 · 11) + 종류별 접촉 수 [벡터 판독 · 카드 산술]

| λp · Vf | 총 (mm²) | 큰–큰 | 큰–작은 | 작은–작은 | 면적 몫 큰–큰 / 큰–작은 / 작은–작은 % |
|---|---|---|---|---|---|
| 0 · 0 | 0.00075 | (= 총) | — | — | 100 / – / – |
| 0 · 0.1 | 0.00185 | 0.00055 | 0.00108 | 0.00028 | 29 / **57** / 15 |
| 0 · 0.3 | 0.00668 | 0.00109 | 0.00368 | 0.00197 | 16 / **55** / 29 |
| 0 · 0.5 | 0.00608 | 0.00021 | 0.00224 | 0.00369 | 3 / 36 / **60** |
| 0.38 · 0 | 0.606 | (= 총) | — | — | 100 / – / – |
| 0.38 · 0.1 | 0.593 | 0.512 | 0.093 | 0.010 | **83** / 15 / 2 |
| 0.38 · 0.3 | 1.347 | 0.248 | 0.745 | 0.374 | 18 / **55** / 27 |
| 0.38 · 0.5 | 2.344 | 0.061 | 0.865 | 1.440 | 3 / 37 / **61** |
| 0.5 · 0 | 0.877 | 0.877 | — | — | 100 / – / – |
| 0.5 · 0.1 | 0.915 | 0.729 | 0.201 | 0.013 | **77** / 21 / 1 |
| 0.5 · 0.3 | 1.858 | 0.372 | 1.040 | 0.472 | 20 / **55** / 25 |
| 0.5 · 0.5 | 3.248 | 0.092 | 1.201 | 1.983 | 3 / 37 / **61** |
| 0.7 · 0 | 1.565 | (= 총) | — | — | 100 / – / – |
| 0.7 · 0.1 | 1.750 | 1.280 | 0.486 | 0.024 | **72** / 27 / 1 |
| 0.7 · 0.3 | 2.651 | 0.647 | 1.532 | 0.512 | 24 / **57** / 19 |
| 0.7 · 0.5 | 5.348 | 0.209 | 2.065 | 3.116 | 4 / 38 / **58** |

- 세 종류 합 ÷ 총 = 0.9–3.8 % 큼 [벡터 판독 합] · 축 범위: λp 0 패널 0–0.008 mm² · 0.38 패널 0–3 · 0.5 패널 0–4 · 0.7 패널 0–6 mm².  ⚠ **캡션은 (a) λp = 0 · (b) 0.38 · (c) 0.7 셋인데 그림은 네 패널 (c) 0.5 · (d) 0.7** · 본문도 *"(Fig. 10b–d)"* (p.8).
- ★ 초록 · 결론의 *"the largest contact type changed in the order of coarse–coarse, coarse–fine, and fine–fine"* 는 **λp ≥ 0.38** 에서만 맞다 — λp 0 은 Vf 0.1 에서 이미 큰–작은 이 가장 크다 (57 %) [벡터 판독 · 카드 산술].
- **큰 입자 하나당 큰–작은 접촉 수 (그림 11a)**: Vf 0.1 · 0.3 · 0.5 = λp 0: 10.31 · 27.43 · 29.78 · 0.38: 12.25 · 34.79 · 47.27 · 0.5: 13.10 · 35.05 · 49.25 · 0.7: 13.38 · 33.59 · 51.82 · 점선 **64** = *"the maximum geometric number of fine particles coordinated around one coarse particle was calculated as 64 by dividing the surface area of the coarse particles by the cross-sectional area of the fine particles"* (p.9 · 4π(25)²/π(6.25)² = 64 [카드 산술] — 덮개 효율 1 인 투영 면적 비라 실제 최대 접촉 수보다 크다 [카드 추론]).
- **큰 입자 하나당 큰–작은 면적 (그림 11b · mm²)**: λp 0 ≈ 0 (≤ 1 × 10⁻⁵ · 축 0–0.002 에서 판독 불가) · 0.38: 3 × 10⁻⁵ · 3.4 × 10⁻⁴ · 5.5 × 10⁻⁴ · 0.5: 8 × 10⁻⁵ · 4.8 × 10⁻⁴ · 7.8 × 10⁻⁴ · 0.7: 1.7 × 10⁻⁴ · 7.0 × 10⁻⁴ · 1.33 × 10⁻³.  × 큰 입자 수 (§3a) = 그림 10 의 큰–작은 면적과 1–11 % 안 [카드 산술] → **그림 10 은 층 전체 합**으로 보인다 (중앙 0.8 영역이면 약 절반이어야 한다) [카드 추론].  ⚠ 캡션은 *"in the condition of λp = 0.38"* 인데 그림은 λp 넷.
- **종류별 접촉 수 · 몫 · 접촉당 면적** [카드 산술 — 큰–작은 = N_큰 × 그림 11a · 큰–큰 = N_큰 × (그림 9a − 그림 11a)/2 · 작은–작은 = (N_작은 × 그림 9b − 큰–작은)/2]:

| λp · Vf | 큰–큰 / 큰–작은 / 작은–작은 접촉 수 | 수 몫 % | 접촉당 면적 µm² (큰–큰 / 큰–작은 / 작은–작은) |
|---|---|---|---|
| 0 · 0.1 / 0.3 / 0.5 | 4,223 / 28,501 / 13,987 · 2,211 / 58,974 / 76,833 · 434 / 45,733 / 169,130 | 9 / 61 / 30 · 2 / 43 / 56 · 0.2 / 21 / 79 | 0.13 / 0.038 / 0.020 · 0.49 / 0.062 / 0.026 · 0.48 / 0.049 / 0.022 |
| 0.38 · 0.1 / 0.3 / 0.5 | 7,915 / 33,856 / 14,953 · 5,883 / 74,784 / 106,003 · 2,425 / 72,590 / 268,302 | 14 / 60 / 26 · 3 / 40 / 57 · 0.7 / 21 / 78 | 64.7 / 2.7 / 0.7 · 42.1 / 10.0 / 3.5 · 25.1 / 11.9 / 5.4 |
| 0.5 · 0.1 / 0.3 / 0.5 | 9,080 / 36,198 / 14,502 · 6,653 / 75,345 / 109,590 · 2,932 / 75,631 / 284,212 | 15 / 61 / 24 · 3 / 39 / 57 · 0.8 / 21 / 78 | 80.3 / 5.6 / 0.9 · 55.9 / 13.8 / 4.3 · 31.4 / 15.9 / 7.0 |
| 0.7 · 0.1 / 0.3 / 0.5 | 8,981 / 36,979 / 14,227 · 6,750 / 72,208 / 102,516 · 3,752 / 79,574 / 305,360 | 15 / 61 / 24 · 4 / 40 / 57 · 1.0 / 20 / 79 | 143 / 13.1 / 1.7 · 95.9 / 21.2 / 5.0 · 55.8 / 25.9 / 10.2 |

- 읽기: 접촉 **수** 몫은 λp 와 거의 무관 (Vf 가 정한다 · Vf 0.5 에서 작은–작은 78–79 %) · 접촉 **면적** 은 λp 가 키운다 · 소성에서 큰–큰 접촉당 면적이 작은 입자가 늘수록 준다 (λp 0.7: 143 → 96 → 56 µm²) — 작은 입자가 하중 일부를 나눠 지는 것과 맞는 방향 [카드 추론 · 하중 값 없음].  λp 0 의 접촉당 면적은 **0.02–0.5 µm²** (겹침 ≈ nm) — §3e.

### 3e. ★ 측정 시점 · 층 평균 재구성 · Heckel [카드 산술 · 카드 추론 — 원문에 없는 수]

**(1) 그림 7–11 은 뺀 뒤 구조로 보인다 [카드 추론] — 근거 다섯 · 반대 근거 하나**
1. **접촉당 면적 = 점착 평형 겹침**: 그림 10a λp 0 단분산 총 0.00075 mm² ÷ 접촉 수 (3,071 × 4.18 / 2 = 6,424) = **0.117 µm²** → R_a² = 0.0372 µm² → 같은 구 (R 25 µm) 의 겹침 δn ≈ R_a²/R = **1.49 nm** ↔ 하중 없는 EEPA 처녀 가지의 힘 평형 f₀ + k₁δⁿ = 0 → δ = (|f₀|/k₁)^(2/3) · k₁ = (4/3)E\*√R\* (E\* = 71/(2 × 0.9375) = 37.87 GPa · R\* 12.5 µm → 1.785 × 10⁸ N/m^1.5) · |f₀| 1.047 × 10⁻⁵ N → **1.51 nm** (2 % 차).  큰–작은 · 작은–작은 도 같은 꼴 (R\* 5 · 3.125 µm → δ_eq 1.11 · 0.95 nm → 면적 0.035 · 0.019 µm² ↔ 관측 0.038–0.062 · 0.020–0.026).  누른 채라면: Rumpf 꼴 σ = (1 − ε) Z ⟨f⟩ / (π d²) 에 σ 400 MPa · 1 − ε 0.77 · Z 9.1 (SI 그림 S3 phase 2) → ⟨f⟩ ≈ 0.45 N → Hertz δ ≈ 1.85 µm → 접촉당 ≈ **145 µm²** (어림 · 단분산 · 등방 가정) — 그림 10a 의 **1,000 배**.
2. 그림 8 Vf 0 λp 0 배위수 **4.18** = SI 그림 S3 phase 3 (뺀 뒤) **4.16 · 4.25** ≠ phase 2 (400 MPa) **9.30 · 8.94**.
3. SI 그림 S6 (크기비 4 · λp 0 · 0.7) 의 가압 끝 배위수 ≈ **7.98 · 8.05** ≠ 그림 8 Vf 0.3 **4.54 · 5.88**.
4. SI 그림 S4 · S5 의 phase 3 (공극 0.300–0.305 · 배위수 6.57–6.80) ≈ 그림 7 · 8 Vf 0 λp 0.7 (0.300 · 6.49) (단 S4 · S5 의 λp 표기는 0 — §3g-7).
5. 그림 4 스냅숏 층 높이 [판독 — 다이 안지름 0.9 mm 기준 · ±3 %] **≈ 0.58 · 0.49 · 0.44 · 0.41 mm** (a–d) ≈ 그림 S7 에서 다시 만든 **뺀 뒤** 높이 (아래 (2)).
- 반대 근거: 그림 7 Vf 0 λp 0 공극 **0.421** ≠ SI S3 phase 3 (EEPA) **0.366** (같은 단분산 λp 0 · 표 S1 은 ζ_tm 1 · 시드 [미확인]).
- ⇒ 저자의 *"Because the particles under elastic conditions cannot allow considerable overlap, the contact areas become small. Thus, the influence of random packing is critical."* (p.8) 는 **뺀 뒤 점착 평형 상태의 결과**다 — 400 MPa 누른 채에는 탄성 접촉도 겹침이 크다 (Hertz 어림 δ/D ≈ 3.7 %).

**(2) 층 평균 공극 재구성 [카드 산술 · 가정 — 인용 금지 · 상대 경향만]**: 그림 S7 펀치 위치 x 와 그림 5 진변형률을 같은 힘에서 맞춰 x = b + h₀e^ε 로 b · h₀ 를 구하고 (크기비 1: b 0.112–0.115 mm · h₀ 0.582–0.594 mm · rms < 0.6 µm · 크기비 4 는 b 가 0.114–0.165 로 흔들려 0.114 로 고정) 고체 높이 V/A = 0.201/0.6362 = **0.316 mm** 로 나눴다.

| | λp 0 | 0.38 | 0.5 | 0.7 |
|---|---|---|---|---|
| 크기비 1 — 처음 · 400 MPa 누른 채 · 뺀 뒤 (펀치 힘 < 0.5 N) | 0.457 · 0.366 · 0.441 | 0.465 · 0.339 · 0.404 | 0.468 · 0.321 · 0.389 | 0.465 · 0.270 · 0.340 |
| 크기비 4 · Vf 0.3 (b 고정) — 처음 · 누른 채 · 뺀 뒤 | 0.356 · 0.163 · 0.246 | 0.363 · 0.146 · 0.215 | 0.366 · 0.134 · 0.206 | 0.364 · 0.116 · 0.198 |
| 그림 4 높이 [판독] → 층 평균 (뺀 뒤) | 0.455 (a · 크기비 1) · 0.282 (c · 크기비 4) | — | — | 0.355 (b) · 0.229 (d) |
| 그림 7 중앙 0.8 영역 (크기비 1 = Vf 0 · 크기비 4 = Vf 0.3) | 0.421 · 0.286 | 0.379 · 0.237 | 0.351 · 0.233 | 0.300 · 0.214 |

- 크기비 1 의 뺀 뒤 층 평균 (0.441 · 0.340) 과 그림 4 (0.455 · 0.355) 는 0.015 안 · 그림 7 (0.421 · 0.300) 보다 0.02–0.04 크다 (벽 쪽이 성기다 [카드 추론]) · 크기비 4 는 서로 0.03–0.08 어긋난다 (b 맞춤 불안정 · 그림 4 (c)(d) 의 Vf [미확인]).  SI 그림 S3 phase 2 (단분산 λp 0 · 중앙) 0.222–0.245 ↔ 위 누른 채 층 평균 0.366 — 0.12 차 (다른 계산 · 벽 영역 몫 · [미확인]).
- **Heckel (이 카드가 그린 것 · 원문 없음)**: 위 층 평균으로 ln(1/(1 − D)) 대 P 를 100–380 MPa 에서 직선 맞춤 → P_y = 1/K = 크기비 1: **2243 · 1582 · 1323 · 888 MPa** (R² ≥ 0.997) · 크기비 4: **1001 (R² 0.948) · 742 · 525 · 406 MPa** — λp 와 작은 입자가 P_y 를 낮춘다 (방향만) · ⛔ 연화 안 한 E 71 GPa · 다이 벽 마찰 · 층 평균 재구성이 다 들어간 **모델 지표 · 물성 아님 · 인용 금지**.

**(3) 규모 · 시간 [카드 산술]**: 변형률 속도 25 mm/s ÷ h₀ ≈ 0.58 mm ≈ **43 s⁻¹** · 관성수 I = ε̇ d √(ρ/P) ≈ 43 × 50 µm × √(4750/400 MPa) = **7 × 10⁻⁶** (≪ 10⁻³ · 준정적) · V/c_P = 0.025 / √(E₁/ρ) = 6.5 × 10⁻⁶ (λp 0) – 1.2 × 10⁻⁵ (λp 0.7) · Rayleigh 시간 (E 71 GPa · ν 0.25) 큰 입자 **35 ns** · 작은 입자 **8.8 ns** → Δt (원문 없음) 는 보통 그 10–30 % (1–3 ns) [가정] · 그림 S6 의 0.05 s 까지면 ≈ 2 × 10⁷ 단계 [카드 산술 · 가정].

### 3f. SI 결과 (그림 S2–S7) [벡터 판독]

| 그림 | 조건 | 값 |
|---|---|---|
| S2 | EEPA ↔ JKR 힘–겹침 (단분산 50 µm · λp 0 · 0–10 µm) | 두 곡선 거의 겹침 · 10 µm 에서 **5.65 N** (Hertz (4/3)E\*√R\* δ^1.5 = 5.645 N ✓ [카드 산술]) · *"The force curves in the EEPA model and JKR model were almost similar"* |
| S3 | JKR ↔ EEPA · phase 1 / 2 / 3 | 공극 JKR **0.516 / 0.222 / 0.366** · EEPA **0.521 / 0.245 / 0.366** · 배위수 JKR **4.17 / 9.30 / 4.16** · EEPA **4.16 / 8.94 / 4.25** · *"JKR and EEPA models indicated similar values in all phases, demonstrating the compatibility of the EEPA pull-off force as the JKR cohesive force"* |
| S4 | Δγ 0 · 4 · 8 · 100 J/m² (x 1) | 공극 phase 1 0.537 · 0.543 · 0.539 · 0.543 / phase 2 0.205 · 0.203 · 0.206 · **0.239** / phase 3 0.300 · 0.301 · 0.302 · 0.305 · 배위수 phase 1 4.20 · 4.20 · 4.21 · 4.22 / phase 2 8.97 · 8.93 · 8.98 · 8.89 / phase 3 6.70 · 6.75 · 6.57 · 6.80 |
| S5 | x 1 · 2.5 · 5 (Δγ 4) | 공극 phase 1 0.544 · 0.546 · 0.543 / phase 2 0.203 · 0.204 · 0.203 / phase 3 0.301 · 0.300 · 0.300 · 배위수 phase 1 4.20 · 4.24 · 4.24 / phase 2 8.93 · 8.91 · 9.03 / phase 3 6.75 · 6.69 · 6.76 |
| S6 | 크기비 4 · λp 0 · 0.7 (Vf [미확인]) · 시간 0.03–0.05 s | λp 0: 4.08 (0.030 s) → 4.29 (0.038) → **최소 4.16 (0.0405 s)** → 0.042–0.046 s 에 급등 → **7.99** · λp 0.7: 4.16 → 4.41 (0.040) → 0.042–0.048 s 에 오름 → **8.05** · *"In the elastic condition (λp = 0), the coordination number decreased around 0.04 s and rapidly increased. The rapid transition of the packing structure is considered to occur."* |
| S7 | 펀치 힘–변위 (위 = 실선 · 아래 = 점선) | §3b 표 |

- SI 판단 (p.6): *"In phase 2, the void fraction of Δγ = 100 J/m² was higher than other conditions. The void fraction of all conditions in Phase 3, however, indicated similar values. … x also exclusively affected the void fraction in Phase 2. Therefore, the cohesive parameters didn't have an impact on the packing structure in Phase 3."* — 그림 S5 phase 2 의 x 효과는 ≤ 0.001 로 보이지 않는다 [벡터 판독].
- phase 정의 (SI p.5): *"After forming a stable structure (phase 1), the powder bed was compressed at 400 MPa (phase 2). The pressure was released until the upper punch did not touch the powder bed (phase 3)."*

### 3g. 원문 안의 어긋남 · 미정의 (원문 비판 — §11 에 다시)

1. **공극 정의 문장** — *"The void fractions were defined as the volume ratio of the particles in the evaluation region to those in the evaluation region."* (p.5) — 글자 그대로는 1 (뜻 없음) · 겹침 이중 계산 처리 · 영역 위치 [미확인].
2. **측정 시점 미기재** (§3e) — 그림 7–11 · 그림 4 (*"after compression"*).
3. **유지 조건** — 본문 *"loaded with a pressure of 400 MPa for 0.02 s"* ↔ 그림 S7 · 5b 는 펀치 위치 고정 + 힘 완화 (크기비 4) [벡터 판독].
4. **λp 0.5 의 분류** — p.4 *"0.5 as the median value of battery materials"* · p.7 *"altered under high particle plasticity conditions (λp = 0.5 and 0.7)"* ↔ p.9 *"hard materials, such as metals and minerals (λp = 0–0.5), Vf = 0.3 has the lowest void fraction"* — 그림 7 의 λp 0.5 는 Vf 0.5 가 더 낮다 (0.217 < 0.233).
5. **캡션 오기** — 그림 10 캡션 패널 셋 (그림은 넷 · λp 0.5 패널 누락) · 그림 11 캡션 *"λp = 0.38"* (그림은 λp 넷).
6. 그림 8 ↔ 그림 9a 의 Vf 0 (단분산) 값이 −0.6 – +4.5 % 다르다 [벡터 판독].
7. **표 S2 ↔ 그림 S5 · S4** — 표 S2 Tensile Exp *"1, 2.5"* ↔ 그림 S5 *x 1 · 2.5 · 5* · 표 S2 Contact Plasticity Ratio *0* ↔ S4 · S5 phase 3 값이 본문 λp 0.7 단분산 (그림 7 · 8 Vf 0) 과 같고 S3 의 λp 0 phase 3 (0.366 · 4.2) 과 다르다 [카드 추론 — 실제 λp [미확인]].
8. **"number ratio … is 43"** (p.8) — 위첨자가 빠진 **4³** (= 큰 입자 하나 부피 = 작은 입자 64 개) 로 읽힌다 [카드 추론].
9. **식 (8) 부호 · 식 (11) m\*** — 식 (8) f_min = (3/2)πΔγR_a 에 음의 부호가 없다 (EEPA 원전은 끌림 −) · 식 (11) f_nd 의 제곱근 안에 m\* 가 없다 (식 (16) 은 √(k_t m\*)) [크롭 대조].
10. 기호표 (p.2) 의 μ = *"viscosity [Pas]"* ↔ 식 (17) 의 μ = 운동 마찰 계수 · Table 1 에 운동 마찰 값 없음.
11. 그림 S7 (b) λp 0 의 최대 힘 248.7 N = **391 MPa** (400 MPa 에 못 닿음) · 그림 5b λp 0 최대 393 MPa [벡터 판독].

---

## 4. ★ 방법

### 4a. DEM 지배식 · 접촉 (§2.1 · 식 1–21 · 크롭 `eq_01` … `eq_21`) [인쇄 — 크롭 이미지에서 다시 읽음]

- (1) m dv/dt = ΣF + mg · (2) I dω/dt = ΣM — Newton 제2법칙 (병진 · 회전).
- (3) f_n = (f_hys + f_nd) u — 법선 힘 = EEPA 이력 힘 + 감쇠 · u 법선 단위 벡터.
- (4) **EEPA 이력 법선 힘 (세 가지)**:
  - f_hys = f₀ + k₁δnⁿ  — if k₂(δnⁿ − δpⁿ) ≥ k₁δnⁿ (처녀 재하)
  - f_hys = f₀ + k₂(δnⁿ − δpⁿ) — if k₁δnⁿ > k₂(δnⁿ − δpⁿ) > −k_adh δn^x (제하 · 재하)
  - f_hys = f₀ − k_adh δn^x — if −k_adh δn^x ≥ k₂(δnⁿ − δpⁿ) (점착)
  - 가지 규칙 (p.3): *"When the overlap was greater than the maximum overlap at a point, a virgin loading equation was applied (the first condition in Eq. (4)). In the case of separation behavior or an overlap smaller than the maximum overlap at that point, the equation of plastic deformation is applied (the second condition in Eq. (4)). When the contact force is less than the minimum force f_min during separation, the cohesive force equation is applied (third condition in Eq. (4))."*
- (5) δp = λp^(1/n) δn — 소성 겹침 (n = 1.5 → 잔류 겹침비 λp^(2/3) = 0.525 · 0.630 · 0.788 [카드 산술]).
- (6) k_adh = (f_min − f₀)/δ_min^x — 점착 가지 강성.
- (7) **λp = 1 − k₁/k₂ = 1 − [(4/3)E₁\*√R\*] / [(4/3)E₂\*√R\*] = 1 − E₁\*/E₂\*** — *"Contact plasticity λp is defined in Eq. (7) using k₁, k₂, the equivalent Young's modulus E, and the equivalent radius R."*
- (8) f_min = (3/2)πΔγR_a [부호 없음 — 인쇄 그대로] · (9) R_a = √(R_i² − (R_i − δ_i)²) = √(R_j² − (R_j − δn + δ_i)²) · (10) δ_i = (δn² − 2R_jδn) / (2(δn − R_i − R_j)).
- (11) f_nd = −2√(5/6) β √(k_nd) v_n^rel [m\* 없음 — 인쇄 그대로] · (12) β = ln e / √(ln²e + π²) · (13) k_nd = 2E\*√(R\*δn).
- (14) F_t = f_t + f_td (f_t ≤ μs f_hys) · f_ct (f_t > μs f_hys) — Coulomb · (15) f_t = f_t(n−1) + Δf_t · (16) f_td = −2√(5/6) β √(k_t m\*) v_t^rel · (17) f_ct = μ · abs(f_hys + k_adh δnⁿ − f₀) (점착 지수가 x 가 아닌 n — yano2024 식 (19) · 원전과 같은 꼴).
- (18) k_t = 8G\*√(R\*δn) · (19) E\* = 2G\*(1 + ν) · (20) Δf_t = k_t δ_t · (21) k_t = ζ_tm (8G\*√(R\*δn)) — *"The tangential stiffness coefficient ζ_tm is the normal and tangential stiffness ratio and is 2/3 to 1 in a real elastic body."*

### 4b. f₀ 설정 — JKR 의 0 겹침 점착 (SI §S2 · 식 S1–S4 · 크롭 `eq_S01` … `eq_S04`)

- (S1) F_JKR = −4√(πγE\*) a^(3/2) + (4E\*/(3R\*)) a³ · (S2) δn = a²/R\* − √(4πγa/E\*) · (S3) a = (4πγR\*²/E\*)^(1/3) (δn = 0 의 양의 해 — *"only one suitable answer for the square root of the contact radius constantly exists"*) · **(S4) f₀ = −(8/3)πγR\*** (E\* 와 무관).
- 검산 [카드 산술]: γ 0.1 J/m² · R\* 12.5 · 5 · 3.125 µm → **1.047 × 10⁻⁵ · 4.19 × 10⁻⁶ · 2.62 × 10⁻⁶ N** (표 2 ✓) · (S1) 에 (S3) 를 넣으면 −8πγR\* + (16/3)πγR\* = −(8/3)πγR\* ✓.
- 동기 (SI p.2): *"Particle cohesion is considered a constant value called the pull-off force in the Edinburgh elasto-plastic adhesive (EEPA) model. In contrast, cohesive force is according to particle sizes in actual particles; for instance, the Johnson-Kendall-Roberts (JKR) model … In this study, the pull-off force calculated based on JKR theory was applied."* — 접촉 쌍 (크기) 별로 f₀ 를 다르게 넣어 EEPA 의 상수 점착을 보완.
- 같은 결과 확인: SI 그림 S2 (힘 곡선) · S3 (세 phase 공극 · 배위수) 에서 JKR ≈ EEPA.

### 4c. 평가 방법 (§2.3 · 식 22–24 · 그림 2 · 3 · p.5)

- **S-S**: 진변형률 (22) ε_strain = ln(h/h₀) (*"h₀ and h are the powder bed heights before and after compression"*) · 압력 = 위 펀치 압력.
- **압축 에너지 (그림 3)**: 위 펀치 힘–변위 곡선 아래 = 총 압축 에너지 · 위 · 아래 펀치 곡선 사이 (회색) = 마찰 손실 FW (*"The pressure loss during pressure transmission from the operated punch to the counter punch is caused by the frictional loss of the powder"*) · 제하 곡선 아래 (초록) = 탄성 에너지 Ee · 총 − Ee − FW (빨강) = 소성 에너지 Ep · Ep/Ee = 분말의 소성 지표 (캡핑 예측 [40]).
- **미시**: 공극 · 배위수 · 접촉 수 · 접촉 면적 — *"The evaluation volume was set as a cylinder with 0.8 times the diameter and height of the powder bed."* · 배위수 = 영역 안 입자당 접촉 수 · 접촉 면적 = 겹침 교차원 (23) S_a = πR_a² · (24) R_a² = R_i(δn² − 2R_jδn)/(δn − R_i − R_j) − {(δn² − 2R_jδn)/(2(δn − R_i − R_j))}² · 접촉 면적 합의 영역 [미확인 — 층 전체로 보인다 §3d].

### 4d. 실험

없음 — 미래 과제로 X 선 CT (p.9).  모든 검증 = SI 의 JKR ↔ EEPA 모델 간 비교뿐.

### 4e. 입자 처리 ★ (우리 '무질서 처리' 칸)

- **형상**: 전부 **구** · 크기 두 개 (50 · 12.5 µm) · 입도 분포 폭 없음.
- **두 크기의 차이**: **크기 하나** — 밀도 · E · ν · 마찰 · 반발 · λp 모두 같음 · 점착 f₀ 만 쌍의 R\* 로 달라짐 (JKR 0 겹침 힘).
- **소성**: EEPA **접촉 소성** (하중 · 제하 강성비 → 잔류 겹침) — 입자 **형상 소성 (유동) 아님** · 항복 캡 없음 · E₂ 고정이라 λp ↑ = 하중 강성 k₁ ↓ (1 − λp 배) 가 같이 따라온다 (§7c).
- **점착**: 쌍별 상수 f₀ · Δγ 0 · 벽 점착 언급 없음 [미확인].
- **강성**: NCM E 의 **절반 (71 GPa)** — *"It was essential that constant Young's modulus was applied as the aim of this study was the investigation of the effect of λp. From this, only Young's modulus was halved to reduce the simulation costs."* (p.4).
- **파괴**: 없음 (서론에만 *"brittle fracture"*).
- **혼합 · 충전**: *"The particles were generated randomly and packed into a cylindrical cell under gravity."* (p.4).

### 4f. 계산 규모 · 비용

입자 3,071 (단분산) – 99,809 (Vf 0.5) [카드 산술] · 다이 지름 18 d_c · 층 높이 ≈ 0.58 mm (≈ 12 d_c) [카드 산술 · 가정] · GPU (EDEM 2019) · Δt · 전체 시간 · 벽시계 시간 · 시드 수 · 반복 [미확인].  비용 절감 수단 = E 절반 (명시) · 작은 영역 (다이 0.9 mm).

### 4g. ★ 네 항목 — DEM 한계 · 소성이 어려운 이유와 우회 · 2D/3D · 탈압

**(i) DEM (단단한 구 · 점접촉) 의 한계 — 원문 문장**
- p.3 (§2.1): *"In the EEPA model, the plastic deformation of the particles is expressed as an overlap between particles while maintaining their shape, whereas the cohesive force is considered a constant pull-off force."* (`txt_p03_eepa_overlap_keeps_sphere_constant_pulloff`)
- p.5 (§2.3): *"A soft-sphere model was applied to the contact method in the DEM simulations. Particle deformation was expressed as particle overlap, whereas the particle shape remained spherical. The contact area in this model was geometrically calculated."* · *"Note that the contact area calculated using this method would be underestimated as the contact area increases, owing to particle deformation in the real particles."* (`txt_p05_eval_region_void_cn_soft_sphere_geometric_area` · `txt_p05_contact_area_underestimated`)
- SI p.2 (§S2): *"Particle cohesion is considered a constant value called the pull-off force in the Edinburgh elasto-plastic adhesive (EEPA) model. In contrast, cohesive force is according to particle sizes in actual particles"* (`txt_si_p02_eepa_constant_vs_size_dependent_cohesion`)
- p.4: *"Note that this study was not assumed to any specific experimental systems. In the present study, an ideal system was utilized to investigate the effect of particle plasticity and size distributions on the powder compression process."*

**(ii) 소성 · 큰 변형을 계산에 넣기 어려운 이유와 이 논문의 우회 · 비용**
- 이유 (원문): *"the analysis of microscopic behavior of plastic deformation is totally insufficient. The effects of cohesiveness and plasticity on powder compression still need to be clarified owing to the interactions among multiple factors."* · *"Most previous studies using the elasto-plastic models are case studies for individual actual powders, and the parametric discussion of particle plasticity still needs to be solved."* (p.2 · `txt_p02_case_studies_parametric_plasticity_unsolved`).
- 우회: ① 입자 소성 → **EEPA 접촉 강성비 λp** (겹침 · 모양 불변) ② 크기별 점착 → JKR 0 겹침 힘으로 쌍별 f₀ ③ 비용 → **E 절반** · GPU · 0.9 mm 다이.  맞춘 값 0 · 검증 = 모델 간 (JKR ↔ EEPA) 뿐.
- 비용 (§4f) · 벽시계 [미확인].

**(iii) 2D / 3D**: **3D** (*"three-dimensional (3D) DEM simulation accelerated by graphical processing units"*, p.2 · `txt_p02_3d_gpu_edem2019_vf03_densest`) · 2D 언급 · 2D → 3D 전이에 대한 말 **없음**.

**(iv) 압력을 뺄 때**: **다뤘다** — *"decompressed by moving up the upper punch at 25 mm/s. The calculation was completed after obtaining a stable structure after release from the pressure."* (p.5 · `txt_p05_25mms_400mpa_hold_0p02s_release`) · SI phase 3 = *"The pressure was released until the upper punch did not touch the powder bed"* (`txt_si_p05_three_phases_release_until_no_contact`) · S-S 제하 (그림 5) · 힘–변위 (그림 S7) · Ee · Ep/Ee (그림 6) · 뺀 뒤 구조 (그림 7–11 · 추정) · 다이 벽 이형 · 배출 없음.

---

## 5. 결과 — 절별 상세 (그림 실독)

### 5.1 Fig. 1 — EEPA 힘–겹침 곡선 (λp 0 · 0.38 · 0.7 · E₂ 고정)
- λp 0 (실선) = 처녀 재하 = 제하 · 0.38 (파선) · 0.7 (쇄선) = 재하가 낮아지고 (k₁ = (1 − λp)k₂) 제하가 가팔라 일찍 0 에 닿는다.  최대 겹침 **0.534 µm** 에서 힘 **0.0696 · 0.0432 · 0.0209 N** (비 1 : 0.620 : 0.300 = 1 − λp ✓) · 제하 힘 0 겹침 **0.283 · 0.422 µm** (÷ 0.534 = 0.530 · 0.790 ↔ λp^(2/3) 0.525 · 0.788) [벡터 판독].  λp 0 의 최대 힘 = Hertz (4/3)E\*√R\* δ^1.5 (E 71 GPa · ν 0.25 · R\* 12.5 µm = 지름 50 µm 쌍) = 0.0697 N [카드 산술] — 표 1 조건 그대로.  끌림 바닥 (f₀ ≈ −10⁻⁵ N) 은 축의 0.03 % 라 판독 불가.

### 5.2 Fig. 2 — 접촉 면적 모식 (R_i · R_j · R_a · δn · δ_i · 렌즈 기하)

### 5.3 Fig. 3 — 압축 에너지 해석 모식 (위 펀치 압축 · 아래 펀치 압축 · 위 펀치 제하 · FW · Ep · Ee)

### 5.4 Fig. 4 — 스냅숏 (a) 크기비 1 · λp 0 (b) 1 · 0.7 (c) 4 · 0 (d) 4 · 0.7 (큰 = 회색 · 작은 = 보라)
- *"The height of the powder bed decreases with increasing particle plasticity. The powder bed heights under the added fine particle condition were lower than those of the monosized powder under all λp conditions."* (p.5) · 층 높이 ≈ 0.58 · 0.49 · 0.44 · 0.41 mm [판독] · (c)(d) 의 Vf [미확인 — 0.3 으로 보인다] · 시점 = 뺀 뒤로 보인다 (§3e).

### 5.5 Fig. 5 — S-S 곡선 (a) 크기비 1 (b) 크기비 4 · Vf 0.3 → §3b
- (b) λp 0 의 **≈ 50 MPa 꺾임** = 충전 구조의 급변 (그림 S6) · 유지 구간 수직 하강 (b) · 제하 뒤 0 응력 수평선.

### 5.6 Fig. 6 — (a) Ee 대 Ep (b) Ep/Ee 대 λp → §3b
- *"Under elastic conditions, Ep/Ee exhibited similar values for different size ratios. Under high particle plasticity conditions, the difference in Ep/Ee between size ratios 1 and 4 increased. … When the plasticity increased under the condition of dc/df = 4, the deformation of coarse particles promoted the rearrangement of fine particles into interstitial voids."* (p.6) — ⚠ 그림 6b 의 λp 0 값은 0.46 ↔ 0.92 로 2 배 차 ('similar' 는 다른 λp 대비 상대적 표현).

### 5.7 Fig. 7 — 공극 대 Vf → §3c
- 두 효과: *"First, the density of the powder beds increased as the fine particles rolled into the interstitial voids of the coarse particles. Second, the coarse solid particles were substituted with fine particle agglomerates by the presence of many fine particles."* · *"The fine particle agglomerates had a dense structure owing to plastic deformation under the high plastic conditions. The densification effect was enhanced under the plastic conditions because the second effect became small."* (p.7).

### 5.8 Fig. 8 — 평균 배위수 대 Vf → §3c
- *"did not change substantially when fine particles were added under elastic conditions, as reported in [41]"* · 소성 = *"downward convex"* (Vf 0.1 최소).

### 5.9 Fig. 9 — 큰 · 작은 입자 배위수 → §3c
- *"Whereas the particle plasticity significantly affected the variation in N_c,coarse, the effect of the particle plasticity on N_c,fine was small. The fine particles located in the interstitial voids of the coarse particles are not subjected to compressive forces because of the force chain formed by the coarse particles."* (p.8) · *"As the number of fine particles increased, compressive forces were applied not only to the coarse particles but also to the fine particles."*

### 5.10 Fig. 10 — 접촉 면적 (총 · 큰–큰 · 큰–작은 · 작은–작은) → §3d

### 5.11 Fig. 11 — 큰 입자 하나당 큰–작은 접촉 수 · 면적 → §3d
- *"The contact area per coarse particle increased in the Vf range from 0.3 to 0.5. In particular, the reduction in the change of the C-F contact area inside the compact was due to a decrease in the number of coarse particles introduced."* (p.9).

### 5.12 SI 그림 S1–S7 → §3a · §3f

### 5.13 결론 (p.9, 3 항)
1. Ep/Ee 가 λp 에 따라 증가 · 작은 입자 추가도 Ep/Ee 증가.
2. *"In contrast to that for the elastic model, the void fraction at Vf = 0.5 was smaller than that at Vf = 0.3 for the high plastic condition (λp = 0.7). The plasticity of the particles enhanced the effects of fine particle addition."*
3. *"As the number of fine particles increased, the contact type with the largest proportion of the total contact area changed in the order of C–C, C-F, and F-F contacts."* (λp ≥ 0.38 에서 — §3d).
- *"It is important to determine the optimal addition ratio of fine particles based on the plastic deformability of the material. In future work, the microscopic properties will be experimentally investigated using X-ray computed tomography."* (`txt_p09_conclusions_future_xray_ct`).

---

## 6. 우선 질문 — 원문 대조

### d. 단단한 입자의 하중 몫 · 재밍
- **직접 값 없음.**  힘 · 응력 분할 · 힘 사슬 지도 · 펀치 반력의 종류별 몫을 내지 않았다.  있는 것 = 정성 문장 (큰 입자 힘 사슬 → 빈틈의 작은 입자는 안 눌림, p.8) + 종류별 배위수 · 접촉 수 · 면적 (§3c · §3d).
- 대리 지표 하나 [카드 산술]: 소성에서 큰–큰 접촉당 면적이 Vf 0.1 → 0.5 로 143 → 56 µm² (λp 0.7) 로 준다 — 작은 입자가 많을수록 큰 입자 접촉이 덜 눌린다는 방향 (뺀 뒤 잔류 겹침이라 하중 그 자체 아님).
- ⚠ 두 크기가 **같은 재료** — 단단한 골격 (AM) 이 무른 상 (SE) 을 감싸 하중을 지는 우리 R1 (강성비 6–7 배 + 크기비) 과 다르다.  크기만으로 생기는 '큰 입자 힘 사슬' 은 우리 계에도 겹쳐 있을 효과의 한 성분 [카드 추론].

### e. 점접촉 법칙 · 대안 · 맞춘 값 수
- 법칙 = **EEPA** (Thakur [32] · EDEM 내장) — 비선형 (n 1.5) · 항복 캡 · 경도 없음 · 다접촉 보정 없음.
- **맞춘 값 0**: λp = 나노압입 문헌 ([38] NCM · [39] Li₃PS₄ · *"E₂ and λp were obtained from reported data measured using the nanoindentation method"* — 계산법 [미확인]) · 0.5 = 중앙값 · f₀ = JKR γ 0.1 J/m² (앞 연구 [28] 의 '충전 구조에 작용하는 임계값') · x · Δγ = SI 민감도 (*"did not have a significant impact"*) · ζ_tm = 문헌 2/3 · 마찰 = 표 1 값 (보정 언급 없음) · E = 절반.
- 큰 변형 범위: 다루지 않음 · 대표 겹침 (뺀 뒤 잔류) δn/D ≈ 1.9 · 2.5 · 4.0 % (λp 0.38 · 0.5 · 0.7 단분산 · 접촉당 면적 73 · 98 · 157 µm² → R_a² ≈ Rδn [카드 산술]) · 누른 채 Hertz 어림 δ/D ≈ 3.7 % (λp 0) — 작은 겹침 영역.
- 대안 비교: 없음 — Thornton–Ning [30] (정본 카드 있음) · Thornton–Cummins–Cleary [29] · He et al. [31] (Hertz + Thornton–Ning · 다구 형상) 인용만.

### b. 압력을 뺄 때 되돌아오는 양과 잰 방법
- 방법: 위 펀치 압력 ↔ ln(h/h₀) (그림 5) · 위 · 아래 펀치 힘–변위 (그림 S7) · 제하 곡선 아래 넓이 = Ee (그림 6) · 펀치가 층에서 떨어질 때까지 (SI phase 3).
- 값 (§3b): Δε 0.085–0.123 (높이 +8.9 – +13.1 %) · 크기비 1 은 λp ↑ 에 Δε 가 0.123 → 0.098 로 줄고 · 크기비 4 는 0.085–0.100 · 펀치 되튐 33–67 µm.  유지 중 힘 완화 (크기비 4) 6–26 %.
- ⚠ 단분산 λp 0 (SI S3) 은 400 MPa 공극 0.245 → 뺀 뒤 0.366 (중앙 영역) — 탄성 겹침이 다 돌아온 상태 [벡터 판독].

### a · i. 기공
- 순수 SE: 없음 · 모든 값은 **NCM 물성 구** (λp 0.7 도 SE 아님).
- §3c (그림 7 · 시점 = 뺀 뒤로 추정) · §3e (층 평균 재구성 · 인용 금지) · §3f (SI phase 별).

### k · l · g → §4g.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 본 세션 지시서 · CLAUDE.md 출처를 병기해 적는다)

### 7a. 비교표

| 항목 | 이 논문 | 우리 | 같음 / 다름 · 이유 |
|---|---|---|---|
| 재료 | NCM111 물성 구 한 종 (크기 둘) · λp 만 NCM · Li₃PS₄ 문헌값 | NCM811 + Li₆PS₅Cl (+ 첨가제) | 다른 재료 · '작은 입자' 는 SE 아님 |
| 크기 | 큰 50 · 작은 12.5 µm (크기비 **4**) · Vf 0–0.5 | AM 이봉 (대 · 소) + SE — 실크기 12 : 4 : 1 (CLAUDE.md) | ★ 크기비 4 = 우리 **AM_S : SE ≈ 4 : 1** 쌍과 같은 비 · 단 강성 · 밀도 대비 없음 |
| DEM 코드 · 접촉 | EDEM 2019 · **EEPA (비선형 n 1.5)** · λp 모든 접촉 같음 · 쌍별 f₀ (JKR) | LIGGGHTS · `hooke/hysteresis` (선형 이력) | 같은 층 (접촉 강성비 이력 · 형상 불변) · 꼴 다름 |
| 강성 | E₂ 71 GPa (계산비 절반) · 하중 E₁ 21.3–71 GPa | SE E_eff **1.35 GPa** (벌크 ≈ 24 → **18 배 연화** · 공극에 맞춤) | 동기 다름: 이 논문 = 계산비 · 우리 = 기공 · 재배열 대리 · 이 논문의 가장 무른 하중 강성도 우리 SE E_eff 의 ≈ 16 배 |
| 소성 표현 | λp (k₂/k₁) — 잔류 겹침 · 항복 없음 | DEM = 연화 + 이력 · Stage-E 면적 보정 / MPM = J2 (E 1.53 · σ_y 0.30 GPa · ν 0.49) 형상 소성 | 이 논문 = 우리 DEM 과 같은 층 · MPM 형상 소성 · 공극 채움 유동 없음 |
| 압력 · 이력 | **400 MPa** · 25 mm/s · 위치 고정 0.02 s 유지 → 제하 | 300 MPa 목표 · 판 고정 이완 · 판 속도 0.01 mm/s (CLAUDE.md 10-12) · 언로딩 팔 = 준비 중 (DEM 우선 Ⓐ) | ★ 이 논문의 '유지 중 힘 완화' 가 우리 `hold` 이완과 같은 부류 (§12 ②) |
| 공극 (400 MPa) | 뺀 뒤 (추정) 중앙 0.198–0.421 · SI 단분산 λp 0 누른 채 0.222–0.245 | 랩 표준 순수 SE 10–13 % (≈ 300 MPa) · 복합 real_14 DEM 15.6 % (CLAUDE.md) | **같은 축 아님** (재료 · 크기 · 시점 · 정의 다름) — 방향만: 연화 안 한 구 DEM 은 400 MPa 에서도 성기다 (frame [2]) |
| 되돌아옴 | Δε 0.085–0.123 · 유지 완화 6–26 % (크기비 4) | 우리 DEM · MPM 언로딩 값 = 아직 없음 | 단계 6 · R4 규모 감각 (값 인용 금지) |
| 접촉 면적 | 겹침 교차원 πR_a² · 종류별 · 뺀 뒤 (추정) | Stage-E Hertz / Physics (Tabor) 피복 | 기하 (Hertz 꼴) 면적 · Tabor · 소성 면적 아님 · 시점 다름 |
| Heckel | 없음 (카드 재구성 P_y 406–2243 MPa · 인용 금지) | DEM 순수 SE P_y **138 MPa** (σ_y_eff 46 MPa) | 비교 불가 (재료 · 연화 · 재구성) |
| 차원 | 3D | 3D (DEM · MPM) | 같음 |

### 7b. ★ 랩 기준과 나란히 (판정 없이 · **랩 표준과 다른 문헌 값 = 다른 재료 · 다른 상태**)

| 우리 랩 기준 (고정) | 이 논문에서 나란히 놓을 수 있는 값 | 왜 같은 축이 아닌가 |
|---|---|---|
| 순수 SE (LPSCl) 기공률 **10–13 %** (≈ 300 MPa) | 없음.  단분산 λp 0 (SI S3) 400 MPa 누른 채 **22.2–24.5 %** · 뺀 뒤 36.6 % · 그림 7 단분산 (뺀 뒤 추정) λp 0.7 **30.0 %** · 크기 이원 최저 19.8 % (λp 0.7 · Vf 0.5) | 모두 **NCM 물성 (E 71 GPa) 구** · 400 MPa · 중앙 0.8 영역 · 대부분 뺀 뒤 → 랩 표준과 다른 문헌 값 |
| LPSCl 진밀도 **1.64 g/cm³** | 없음 (입자 밀도 4.75 g/cm³ = NCM111 값 하나) | — |

### 7c. ★ 18 배 연화와 견줄 자리 (frame [2])
- 이 논문은 **연화하지 않고 (계산비로 E 절반만)** 400 MPa 누른 채 단분산 공극 0.22–0.25 (SI S3) · 뺀 뒤 0.30–0.42 — frame [2] 의 *"연화 안 한 강체구 + 접촉 소성만으로는 ~20 % 아래로 못 간다"* 와 같은 방향의 외부 사례 하나 (⚠ 재료 · 크기 · 시점 [추정] — 크기 인용 금지).  크기 이원 + λp 0.7 의 뺀 뒤 0.198 이 가장 낮다.
- ★ **함정 (yano2024 과 같다)**: E₂ 고정에서 λp 0 → 0.7 은 하중 강성 k₁ 을 **3.3 배** 낮춘다 (E₁ 71 → 21.3 GPa) — 그림 5 의 '소성이 클수록 더 눌린다' (크기비 1 최대 변형률 −0.156 → −0.310) 에는 **잔류 겹침 (소성) 과 하중 연화가 섞여 있다** [카드 추론].  우리 18 배 연화도 '눌림' 을 키우는 손잡이 → 문헌 탄소성 DEM 의 '소성 효과' 를 읽을 때 E₁ · E₂ 중 무엇을 고정했는지 먼저 본다.
- 크기비 4 에서는 λp 효과가 작다 (−0.262 → −0.330) — 저자: 변형률 증가의 주인은 **재배열** (p.5).

### 7d. frame [3] / [4] / [5]
- **frame [3] (Furnas dip)**: ★ 이 논문의 크기 이원 최적 Vf 가 **접촉 소성으로 0.3 → 0.5 로 옮겨진다** (뺀 뒤 · 중앙 · 크기비 4) — 우리 기록의 *"소성 흐름이 충전 dip 을 일부 지운다"* (2D MPM · CORRECTION 2) 와 **같은 방향의 DEM 쪽 외부 사례** (기전은 다르다: 이쪽은 접촉 강성비 + 하중 연화 · 형상 유동 아님) [카드 추론].
- **frame [4]**: 실험에 맞추지 않았고 실험 대조도 없다 → 교차 확인 재료가 아니다 (모델 간 JKR ↔ EEPA 일치뿐).
- **frame [5]**: 이 논문은 **충전 · 접촉망 (DEM 몫)** 의 크기 이원 지표를 주고 형상 소성 (MPM 몫) · 수송 (σ) 은 없다 — 큰–작은 접촉 면적 (그림 10 · 11) 이 AM–SE 계면 (피복) 쪽으로 넘어갈 다리이지만 σ 계산은 없다.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나

(우리 계획 = 단단한 AM (NCM) + 무른 SE (LPSCl) 복합 양극을 ≈ 300 MPa 로 누르고 압력을 빼는 과정을 한 모델로.  랩 기준 (순수 SE 기공률 10–13 % · LPSCl 진밀도 1.64 g/cm³) 은 고정 · 판정하지 않는다.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 재료 · 차원 · 조건 차이 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ **반례 두 개**: ① 시점 (누른 채 / 뺀 뒤) 을 안 적어 그림 7–11 을 어느 상태로 읽을지 카드가 추론해야 했다 (§3e) ② 공극 정의 문장이 글자 그대로는 뜻이 없다 + 영역 (중앙 0.8 원통) 값과 층 평균 재구성이 0.02–0.12 다르다 → 우리 등록에 **연산자 · 영역 · 시점 · 겹침 처리 · 밀도 기준**을 같이 적을 근거 | 값은 NCM 물성 모델계 — 판정 기준 값으로 쓰지 않는다 |
| **단계 1** (입자별 속도장 3D 메모리 · 장 수) | 규모 감각만: 크기비 4 · Vf 0.5 에서 작은 입자 **98,274 개 = 큰 입자의 64 배** (부피당) · 다이 18 d_c — 작은 상 (SE) 을 입자별로 풀면 장 수가 작은 입자 수로 정해진다 | DEM · 메모리 수치 없음 |
| **단계 2** (2D MPM 코드 · 단위 시험) | 없음 | — |
| **단계 3** (2D 접촉 표현만 바꿔 누르는 힘 비교) | 보고 꼴: **같은 침대 · 같은 조성에서 접촉 법칙 매개변수 (λp) 만 바꿔** S-S 의 재하 · 유지 · 제하 · 잔류를 따로 · Ee · Ep · FW 를 같이 — 크기비 1 은 최대 변형률이 2 배 (−0.156 → −0.310) · 크기비 4 는 1.26 배 → '접촉 표현의 영향은 충전 구조 (크기 이원) 에 따라 크기가 다르다' 는 예 | 2D 아님 · MPM 아님 · λp 가 하중 강성도 바꿈 |
| **단계 4** (3D 순수 SE 붓고 눌러 항복 세기 하나를 실험 기공에 맞춤) | 출발 상태: 원통 안 **무작위 생성 → 중력 충전 → 안정 구조** · 점착 f₀ (JKR γ 0.1 J/m²) 가 충전을 정한다 (앞 연구 [28]) · 충전 공극 (SI S3 · 단분산) **0.52** · 크기비 4 · Vf 0.3 의 처음 층 평균 ≈ 0.36 [카드 산술 · 가정] — 우리도 출발 충전율을 결과 전에 적는 이유 | 순수 SE 없음 · 항복 세기 없음 |
| **단계 5** (3D 복합 AM + SE 압축) | ★ **크기 이원 + 접촉 소성의 조성 경향** (크기비 4 = 우리 AM_S : SE): 최적 작은 입자 몫이 소성으로 0.3 → 0.5 · 작은 입자 배위수는 탄성에서 단분산 값 (4.2) 쪽 · 소성에서 넘어선다 · 접촉 수 몫은 Vf 가 · 면적은 λp 가 정한다 · 큰 입자 힘 사슬이 빈틈의 작은 입자를 막는다 (정성) — **결과 전 대조 항목** 후보 | 우리 복합은 AM · SE 강성 · 밀도 대비 (6–7 배 · 2.9 배) · 실제 소성 SE · SE 가 '작은 입자' 이면서 무른 상 → 이 논문 경향이 그대로 성립한다고 가정하지 않는다 |
| **단계 6** (압력 빼고 되돌아옴) | ★ **관측량**: 최대 · 잔류 ln(h/h₀) · Ee (제하 곡선 아래) · Ep · FW (두 펀치 힘 차) · Ep/Ee · 펀치 되튐 · ★ **위치 유지 중 힘 완화 (작은 입자 있을 때 6–26 % / 0.02 s · λp ↑ 일수록 큼 · 단분산 ≈ 0)** — 유지 구간을 따로 보고할 근거 · 규모 감각: Δε 0.085–0.123 · 단분산 λp 0 중앙 공극 0.245 → 0.366 | 재료 · 크기 다름 · 배출 · 다이 이형 · 벽 점착 없음 · 다른 정본 카드의 실제 SE 값 (miss2026) 과 같은 축 아님 |
| **단계 7** (눌린 구조의 형상 · 피복 · 수송) | 큰 입자 하나당 **큰–작은 접촉 수 · 면적** (= AM 하나당 SE 접촉 · 피복의 크기 이원 꼴) · 투영 면적 상한 64 (4(d_c/d_f)²) · 큰–작은 면적이 Vf 0.3 → 0.5 에서 평평해지는 이유 (큰 입자 수 감소 ↔ 하나당 면적 증가) | 수송 계산 없음 · 면적 = 기하 교차원 · 뺀 뒤 (추정) |
| **후보 D0** (지금 DEM: 구 · 탄성-이력 · 무른 E) | 같은 층의 외부 사례: 비선형 EEPA · **연화 없음 (E 절반)** → 400 MPa 단분산 누른 채 0.22–0.25 · 저자 스스로 *"the contact area … would be underestimated as the contact area increases"* · **λp ↑ = 하중 연화 동반** (§7c) · ★ 문헌 DEM 의 접촉 면적 · 배위수가 **뺀 뒤 값일 수 있다** (§3e) | 우리 연화 18 배 · 선형 이력 · 재료 다름 |
| **후보 A′-0** (MPM 판 · 벽 · AM 자리에만 접촉 규칙) | 벽 마찰의 크기 감각: 아래 / 위 펀치 최대 힘 비 **0.62–0.69 (단분산) · 0.72–0.84 (크기비 4)** · FW ≈ 압축 일의 25–28 % (단분산) [카드 산술] — 18 d 다이에서 판 · 벽 규칙이 내야 할 관측량 (두 판 힘 차) | MPM 아님 · 벽 마찰 값 [미확인] |
| **후보 A** (MPM: AM 강체 + SE 한 속도장) | 없음 | — |
| **후보 A′** (MPM: 입자별 속도장 · 다물체 마찰) | 없음 | — |
| **후보 B** (입자별 FE + 접촉) | 없음 (저자가 형상 유지 · 기하 면적 과소를 한계로 듦 — B 가 채울 칸) | — |
| **후보 C** (큰 변형 접촉 DEM — MDR 류) | 없음 · EEPA 는 큰 변형 법칙 아님 · 대표 겹침 δn/D 1.9–4.0 % (뺀 뒤) · ≈ 3.7 % (누른 채 어림) [카드 산술] | — |
| **후보 C′** (항복 캡 탄소성 접촉 DEM — Thornton–Ning · 다접촉) | Thornton–Ning [30] · He et al. [31] (Hertz + Thornton–Ning) 을 인용만 · EEPA 의 '소성 손잡이' = 강성비 → 하중 연화가 함께 (C′ 의 항복 캡과 다른 손잡이) · 크기별 점착 = JKR 0 겹침 f₀ (식 S4) | 항복 캡 · 다접촉 보정 없음 |
| **후보 M0** (균질화 압밀 — 캡 소성 · Heckel) | 벌크 서술자 Ep/Ee (0.46–2.53 단분산 · 0.92–4.93 크기비 4) · 압축 일 5.2–13.4 mJ · Heckel 원문 없음 (카드 재구성 P_y = §3e · 인용 금지) | 한 압력 · 압밀 곡선은 S-S 뿐 |
| **U0** (접촉 끈 것과 같은지) | 없음 | — |
| **U1** (입자 하나 압축 · 해상도) | 없음 (그림 1 = 두 입자 접촉 법칙 곡선 — U3 쪽) | — |
| **U2** (경사면 마찰) | 없음 · 정지 마찰 0.5 · 구름 0.01 (default) · 운동 마찰 값 [미확인] | — |
| **U3** (단단한 구를 소성 블록에 눌렀다 떼기) | ★ DEM 접촉 법칙 쪽 기준선: 그림 1 = **지름 50 µm NCM 물성 쌍** (Hertz 검산 ✓) 의 재하 · 제하 · 잔류 — 잔류 겹침비 **λp^(2/3)** (0.38 → 0.530 · 0.7 → 0.790 · 이론 0.525 · 0.788) · λp 를 나노압입에서 얻은 방법 [미확인] → 압입 깊이비 ↔ EEPA λp 대응 규칙을 결과 전에 정할 자리 | MPM U3 의 수치 표적 아님 |
| **U4** (판 분리) | SI phase 3 = *"released until the upper punch did not touch the powder bed"* · 그림 S7 의 힘 0.5 N 아래 = 분리 (되튐 33–67 µm) · 벽 점착 언급 없음 | 판 분리 조건 (0 힘 · 벽 점착) 의 실험 대조 없음 |
| **U5** (비슷한 강성 입자 충돌 · 다물체) | 반발 0.25 · 감쇠식 (11)–(13) · (16) · ζ_tm 0.67 (2/3 근거 [36, 37]) · 같은 재료 큰 · 작은 입자 충돌 — 입력 꼴 | 충돌 시험 없음 |
| **U6** (작은 조밀 충전 해상도 수렴) | 없음 (시드 · 반복 · 해상도 보고 없음) · 자기 일관 검산 하나: 그림 9 의 수 평균 = 그림 8 (±1.9 %) [카드 산술] | — |
| **R1** (AM 이 움직이고 하중을 나눠 짐) | 두 크기 다 움직임 · 큰 입자 힘 사슬 ↔ 빈틈의 작은 입자 (정성) · 큰–큰 접촉당 면적이 작은 입자 ↑ 에 준다 (대리) | 강성 대비 0 · 하중 값 없음 |
| **R2** (미끄럼 · 분리) | Coulomb (μs 0.5) · 구름 0.01 · 점착 가지 (쌍별 f₀ · Δγ 0) · SI: Δγ 100 J/m² 는 누른 채 공극을 0.205 → 0.239 로 올리지만 뺀 뒤는 같다 | 벽 점착 · 벽 마찰 [미확인] |
| **R3** (SE 입자 경계 기억) | 접촉마다 δp 이력 (EEPA) — 입자 경계 · 형상 기억 없음 | — |
| **R4** (탈압 · 되돌아옴) | **있음** — S-S 제하 · 유지 완화 · 힘–변위 · Ee · Ep/Ee · SI phase 3 | 값 전이 금지 |
| **R5** (맞추는 값은 모델마다 하나) | 이 논문 DEM 은 **0 맞춤** (λp 문헌 · f₀ 앞 연구 · E 절반) · 실험 대조도 없다 | — |
| **R6** (SE 입자 형상 변형) | 없음 — *"the particle shape remained spherical"* | 저자 명시 |
| **R7** (AM 파괴) | 없음 — 서론의 *"brittle fracture [15]"* 만 | — |
| **결과 전 대조 항목** | 우리 DEM 에 **같은 재료 · 크기비 4 대조 팔**을 둔다면 결과 전에 적어 둘 기대 (이 논문 경향): 탄성 쪽 최적 Vf ≈ 0.3 · 소성 (λp 0.7) 쪽 0.5 · 작은 입자 배위수 → 단분산 값 (탄성) · 큰–작은 면적이 Vf 0.3 → 0.5 에서 평평 · 유지 중 힘 완화가 작은 입자 · 소성에 따라 커짐 | 실제 AM–SE 복합의 기대값 아님 |

---

## 9. Figure set ★ (크롭 70 장 — `litdb/figures/yano2023_eepa_bimodal_size_plasticity_compression_dem/`)

| 그림 · 표 | 내용 | 파일 | 우리 활용 |
|---|---|---|---|
| Fig. 1 | EEPA 힘–겹침 곡선 (λp 0 · 0.38 · 0.7 · E₂ 고정) | `fig_1.png` (다시 자름 — 도구는 그림 2 와 합침) | U3 · 잔류 겹침비 λp^(2/3) |
| Fig. 2 | 접촉 면적 모식 (R_a · δ_i · 렌즈) | `fig_2.png` (손 크롭) | 식 (9)–(10) · (23)–(24) |
| Fig. 3 | 압축 에너지 해석 모식 (FW · Ep · Ee) | `fig_3.png` (손 크롭) | 단계 6 관측량 정의 |
| Fig. 4 | 스냅숏 (a)–(d) · 큰 = 회색 · 작은 = 보라 | `fig_4.png` (캡션 넣어 다시) | 층 높이 [판독] · 시점 추정 |
| Fig. 5 | S-S (a) 크기비 1 (b) 크기비 4 · Vf 0.3 | `fig_5.png` (캡션 넣어 다시) | 최대 · 잔류 · 유지 하강 |
| Fig. 6 | (a) Ee 대 Ep (b) Ep/Ee 대 λp | `fig_6.png` (캡션 넣어 다시) | 에너지 분해 |
| Fig. 7 | 공극 대 Vf (λp 넷) | `fig_7.png` (캡션 넣어 다시) | ★ 최적 Vf 이동 |
| Fig. 8 | 평균 배위수 대 Vf | `fig_8.png` (캡션 넣어 다시) | 수 평균 · 탄성 4.2 |
| Fig. 9 | (a) 큰 (b) 작은 입자 배위수 | `fig_9.png` (캡션 넣어 다시) | 종류별 배위수 |
| Fig. 10 | 접촉 면적 (총 · 큰–큰 · 큰–작은 · 작은–작은) · 네 패널 | `fig_10.png` (캡션 넣어 다시) | 면적 몫 순서 · 캡션 오기 |
| Fig. 11 | (a) 큰 입자당 큰–작은 접촉 수 (최대 64 점선) (b) 면적 | `fig_11.png` (손 크롭 — 도구가 놓침) | AM 하나당 SE 접촉 꼴 |
| 표 1 | 입자 · 기하 설정 | `tab_1.png` (손 크롭) | 입력 |
| 표 2 | EEPA 매개변수 (쌍별 f₀ · λp · 지수 · ζ_tm) | `tab_2.png` (다시 자름 — 도구는 쪽 전체) | f₀ = yano2026 값의 원전 |
| Fig. S1 | 압축 도구 3D 기하 (0.9 mm · 1 mm · 0.636 mm³) | `fig_S1.png` (캡션 넣어 다시) | 다이 규모 |
| 표 S1 | JKR ↔ EEPA 비교 조건 | `tab_S1.png` (다시 자름 — 그림 S2 섞임) | ζ_tm 1 · λp 0 |
| Fig. S2 | EEPA ↔ JKR 힘 곡선 | `fig_S2.png` (다시 자름) | f₀ 환산 확인 |
| Fig. S3 | JKR ↔ EEPA 공극 · 배위수 (phase 1–3) | `fig_S3.png` (캡션 넣어 다시) | ★ 누른 채 ↔ 뺀 뒤 |
| 표 S2 | Δγ · x 시험 조건 | `tab_S2.png` (다시 자름 — 위 본문 섞임) | 표 ↔ 그림 어긋남 |
| Fig. S4 | Δγ 0 · 4 · 8 · 100 의 공극 · 배위수 | `fig_S4.png` (캡션 넣어 다시) | 점착 민감도 |
| Fig. S5 | x 1 · 2.5 · 5 의 공극 · 배위수 | `fig_S5.png` (캡션 넣어 다시) | 점착 지수 민감도 |
| Fig. S6 | 배위수 시계열 (λp 0 · 0.7) | `fig_S6.png` (손 크롭 — 도구 '그래픽 없음') | 50 MPa 꺾임 · 누른 뒤 8.0 |
| Fig. S7 | 위 · 아래 펀치 힘–변위 (a) 1 (b) 4 · Vf 0.3 | `fig_S7.png` (캡션 넣어 다시) | ★ 유지 완화 · 되튐 · 벽 마찰 |
| 식 (1)–(24) · (S1)–(S4) | 번호마다 한 장 | `eq_01_translational_motion.png` … `eq_24_contact_radius_squared.png` · `eq_S01_jkr_contact_force.png` … `eq_S04_f0_from_jkr_zero_overlap.png` | 보고서 DEM 절 (EEPA · 감쇠 · 접선 · JKR f₀ · 진변형률 · 접촉 면적) |
| 근거 문단 20 | 카드가 숫자 · 정의 · 단정의 근거로 인용한 문단 | `txt_p01_…` … `txt_si_p05_…` (아래) | — |

근거 문단 크롭 (파일 이름의 p = PDF 쪽 = 논문 쪽 · si = SI 쪽): `txt_p01_abstract_eepa_bimodal_lambda_p_vf_contact_order` (초록) · `txt_p02_case_studies_parametric_plasticity_unsolved` (p.2 ★ 소성 매개변수 논의 부족) · `txt_p02_3d_gpu_edem2019_vf03_densest` (p.2 ★ 3D · GPU) · `txt_p03_eepa_overlap_keeps_sphere_constant_pulloff` (p.3 ★ DEM 한계) · `txt_p03_virgin_unloading_adhesion_branch_rules` (p.3 가지 규칙) · `txt_p04_ncm_props_e_halved_bimodal_50um_0p20mm3` (p.4 · 두 단을 이어 붙임 — 물성 · E 절반 · 크기 · 입자 수) · `txt_p04_x_dgamma_no_impact_f0_jkr_0p1` (p.4 f₀) · `txt_p04_e2_measured_e1_input_lambda_p_same_all_contacts` (p.4 ★ 의도 — 모든 접촉 같은 λp) · `txt_p05_25mms_400mpa_hold_0p02s_release` (p.4–5 · 두 쪽을 이어 붙임) · `txt_p05_eval_region_void_cn_soft_sphere_geometric_area` (p.5 · 두 단을 이어 붙임 ★) · `txt_p05_contact_area_underestimated` (p.5 ★) · `txt_p05_ss_bending_50mpa_rearrangement_not_deformation` · `txt_p05_ep_nonzero_elastic_rearrangement_less_energy` (p.5) · `txt_p07_void_vf05_lowest_two_effects_dense_agglomerates` (p.7) · `txt_p08_cn_number_ratio_fine_4p2_force_chain` (p.8 ★ 힘 사슬) · `txt_p08_elastic_contact_area_minimal_cf_trend` (p.8 ★ 시점 함정) · `txt_p09_hard_vf03_plastic_vf05_optimal_ratio` (p.9) · `txt_p09_conclusions_future_xray_ct` (p.9) · `txt_si_p02_eepa_constant_vs_size_dependent_cohesion` (SI p.2 ★) · `txt_si_p05_three_phases_release_until_no_contact` (SI p.5 phase 정의).

## 10. Post-processing ★
- **원문**: S-S (위 펀치 압력 vs ln(h/h₀)) · F–D 넓이로 FW · Ee · Ep · 중앙 0.8 원통의 공극 · 배위수 · 접촉 수 · 교차원 면적 합 (식 23–24) · 큰 입자당 큰–작은 접촉 수 · 면적 · 오차 막대 · 반복 · 시드 [미확인].
- **이 카드**: 그림 1 · 5–11 · S2–S7 벡터 경로 · 막대 판독 (`digitized.csv` 301 행) · 유지 중 힘 완화 · 되튐 · 반대 펀치 비 · 압축 일 · FW 차감 · Ee 재계산 · 입자 수 · 수 평균 배위수 검산 · 종류별 접촉 수 · 접촉당 면적 · 점착 평형 겹침 · Rumpf 어림 · 층 평균 공극 재구성 · Heckel 재구성 · f₀ 검산 · Hertz 검산 · 관성수 · Rayleigh 시간 (§3).

## 11. 비판 / 주의 / 한계 ★ (over-claim 방지)

1. **'두 성분의 소성이 다르다' 가 아니다** — λp 는 계산마다 모든 접촉 같은 값.  제목 · 키워드 (*"Two-component mixture"*) 의 '두 성분' = 크기 둘.
2. **모든 입자 = NCM111 물성 구** (E 절반) — '작은 입자' 를 SE 로 읽지 않는다.
3. **측정 시점 미기재** (§3e) — 그림 7–11 은 뺀 뒤로 보인다 · 저자의 '탄성 접촉 면적이 작은 이유' 해석은 그 상태에서만 맞다.
4. **소성 손잡이 = 연화 손잡이** — E₂ 고정이라 λp ↑ 가 하중 강성을 (1 − λp) 배로 낮춘다 (그림 1 로 확인) · '소성이 클수록 더 치밀' 의 몫을 잔류 겹침과 하중 연화로 나누지 않았다 [카드 추론].
5. **'유지' 의 뜻** — 본문은 400 MPa 로 0.02 s 유지라 적었지만 그림은 위치 유지 + 힘 완화 (크기비 4) · 그림 5b λp 0 은 400 MPa 에 못 닿았다 (391–393 MPa).
6. **λp 0.5 의 분류 모순 · 캡션 오기 · 공극 정의 문장 · 4³ 위첨자 · 식 (8) 부호 · 식 (11) m\* · 기호표 μ** (§3g) — 글자 그대로 인용하지 않는다.
7. **주장의 범위** — '가장 큰 접촉 면적 종류의 순서 C–C → C–F → F–F' 는 λp ≥ 0.38 에서만 · '작은 입자 배위수 → 4.2' 는 탄성에서만 · 'Vf 0.4 이상이 0.3 보다 성기다' 는 그림에 0.4 점이 없다.
8. **실험 검증 없음 · 0 맞춤** — 결과는 모델 내부 경향이다 (frame [4] 의 교차 확인 재료 아님).
9. **소계 · 벽 효과** — 다이 18 d_c · 중앙 0.8 영역 · 층 평균과 0.02–0.12 차 [카드 산술 · 가정] · 아래 / 위 펀치 힘 비 0.62–0.84.
10. **SI 의 표 ↔ 그림 어긋남** — 표 S2 (λp 0 · x 1, 2.5) ↔ 그림 S5 (x 1, 2.5, 5) · phase 3 값이 λp 0.7 꼴 (§3g-7).
11. 한 압력 · 한 속도 · 한 유지 시간 · 시드 · 반복 · Δt [미확인] · 데이터 · 코드 공개 진술 없음.

## 12. 적용 인사이트
- ① **'누른 채 / 뺀 뒤' 표기 점검표** (단계 0 · 결과 전 대조): 문헌 DEM 의 접촉 면적 · 배위수를 우리 Stage-E 피복 · 배위수와 견줄 때, 접촉당 면적이 **점착 평형 겹침 (|f₀|/k₁)^(2/3)** 크기면 뺀 뒤 값이다 — 이 논문 λp 0 은 1.49 nm ↔ 1.51 nm [카드 산술].
- ② **유지 이완** (단계 6 · R4 · 흐름 안): 위치를 고정한 0.02 s 동안 작은 입자가 있는 층은 힘이 6–26 % 빠지고 단분산은 거의 안 빠진다 — 우리 `hold` (판 고정 → 침대 이완 · `settled_over_target`) 해석에 같은 부류의 외부 DEM 사례 (작은 입자 재배열 · 접촉 소성 이완) [카드 추론] · 유지 구간을 따로 보고하는 꼴.
- ③ **f₀ = −(8/3)πγR\*** (JKR 0 겹침 · 식 S4): 상수 점착 EEPA 에 크기별 점착을 넣는 규칙 — 우리 믹서 · 응집 축 (흐름 밖: 믹싱 · 점착 매개변수) 에서 쌍별 점착 크기를 정할 때 · yano2026 f₀ 값의 원전.
- ④ **최적 작은 입자 몫은 강체 기하만으로 정해지지 않는다** (흐름 밖: 입도 설계 · Furnas dip): 크기비 4 에서 접촉 소성이 최적 Vf 를 0.3 → 0.5 로 옮긴다 — 우리 SE 몫 최적 (dip) 을 '강체 기하 (de Larrard)' 로만 정할 때의 한정어 근거.
- ⑤ **'소성 = 연화' 함정** — yano2024 과 같다: 문헌 탄소성 DEM 의 '소성 효과' 를 우리 18 배 연화와 견주기 전에 고정한 강성 (E₁ · E₂) 을 확인.

## 13. 인용 가능 문장 (deck/paper 용 — 표지 그대로)
- *"In an EDEM–EEPA study of bimodal (50/12.5 µm) spheres with NCM properties and halved Young's modulus, compressed to 400 MPa, the void fraction was lowest at a fine-particle volume fraction of 0.3 for elastic contacts (λp = 0, 0.38) but at 0.5 for λp = 0.7 — contact plasticity shifted the optimal fine fraction [Yano et al., Adv. Powder Technol. 34 (2023) 104245]."* (⚠ 측정 시점 미기재 — 뺀 뒤로 추정)
- *"In the EEPA model, the plastic deformation of the particles is expressed as an overlap between particles while maintaining their shape, whereas the cohesive force is considered a constant pull-off force (Yano et al. 2023, p. 3)."*
- *"The contact area calculated geometrically from soft-sphere overlaps would be underestimated as the contact area increases, owing to particle deformation in real particles (Yano et al. 2023, p. 5)."*
- 국문: *"크기 이원 EEPA DEM 에서 위치를 고정한 0.02 s 유지 동안 작은 입자가 있는 층의 펀치 힘은 6–26 % 빠지고 단분산은 거의 안 빠진다 (Yano 2023 그림 S7 · 벡터 판독)."* [벡터 판독 표지 유지]
- ⛔ 인용 금지: 공극 · 변형률 · 접촉 면적 값을 LPSCl · NCM 복합의 값으로 쓰는 문장 · *"소성이 다른 두 성분 (NCM–SE) 의 혼합 압축"* (이 논문은 크기 이원 · 모든 접촉 같은 λp) · 카드 재구성 Heckel P_y · 층 평균 공극.

## 14. 기법 용어 미니사전
- **EEPA (Edinburgh Elasto-Plastic Adhesion)**: 처녀 재하 k₁ · 제하/재하 k₂ 로 잔류 겹침 δp 를 남기는 DEM 접촉 법칙 + 점착 가지 · 입자 모양 불변.
- **접촉 소성비 λp (Contact Plasticity Ratio · 원문 'particle plasticity')**: 1 − k₁/k₂ = 1 − E₁\*/E₂\* · 0 = 완전 탄성.
- **E₁ · E₂**: 하중 · 제하 강성에 해당하는 영률 · EDEM 입력 = E₁ · 측정 영률 = E₂.
- **f₀ (Constant pull-off force)**: 겹침과 무관한 상수 끌림 힘 · 이 논문 = JKR 0 겹침 힘 −(8/3)πγR\*.
- **Δγ (Meso-surface energy · contact effective surface adhesion energy)** · **x (Tensile Exp)** · **n (Slope Exp)** · **ζ_tm (Tangential Stiff Multiplier)**.
- **Vf**: 작은 입자 부피 몫 (volume mixing ratio of fine particles) · **d_c/d_f**: 크기비.
- **C-C · C-F · F-F**: 큰–큰 · 큰–작은 · 작은–작은 접촉.
- **S-S curve**: 위 펀치 압력 vs ln(h/h₀) · **F-D curve**: 펀치 힘 vs 위 펀치 변위.
- **Ee · Ep · FW**: 탄성 회복 에너지 · 소성 변형 에너지 · 마찰 일 (두 펀치 힘 차) · Ep/Ee = 분말 소성 지표 [40].
- **phase 1 · 2 · 3 (SI)**: 충전 · 400 MPa 압축 · 위 펀치가 층에서 떨어질 때까지 제하.
- **soft-sphere model**: 변형을 겹침으로 나타내는 DEM.

## 15. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로)

| 번호 | 서지 (원문 목록) | 왜 · 정본 카드 |
|---|---|---|
| 5 | A. Sakuda, A. Hayashi, M. Tatsumisago, Sulfide solid electrolyte with favorable mechanical property for all-solid-state lithium battery, Sci. Rep. 3 (2013) 2–6 | 정본 `sakuda2013_sulfide_mechanical_property` |
| 17 | C.L. Martin, D. Bouvard, S. Shima, Study of particle rearrangement during powder compaction by the Discrete Element Method, 51 (2003) 667–693 | 재배열 DEM — 학술지 이름 없음 [인쇄 그대로] · 카드 없음 (정본 `martinbouvard2003_dem_composite_cold_compaction` 은 다른 논문) |
| 27 | K.K. and A.D.R. Kenneth Langstreth Johnson, Surface energy and the contact of elastic solids, Proc. Roy. Soc. London. A. 324 (1971) 301–313 | 정본 `johnson1971_jkr_surface_energy_contact_elastic_solids` (저자 표기 깨짐 [인쇄 그대로]) |
| 28 | T. Yano, S. Ohsaki, H. Nakamura, S. Watano, Numerical study on compression processes of cohesive bimodal particles and their packing structure, Adv. Powder Technol. (2021), https://doi.org/10.1016/j.apt.2021.02.040 | ★ 이 논문의 설정 · γ 0.1 J/m² '임계값' · 탄성 이원 최적 Vf 0.3 의 출처 (권 · 쪽 없음 [인쇄 그대로]) — 카드 없음 |
| 29 | C. Thornton, S.J. Cummins, P.W. Cleary, On elastic-plastic normal contact force models, with and without adhesion, Powder Technol. 315 (2017) 339–346 | e — 탄소성 법선 접촉 모델 비교 — 카드 없음 |
| 30 | C. Thornton, Z. Ning, A theoretical model for the stick/bounce behaviour of adhesive, elastic- plastic spheres, Powder Technol. 99 (1998) 154–162 | 정본 `thorntonning1998_adhesive_elastoplastic_contact` |
| 31 | Y. He, T.J. Evans, Y.S. Shen, A.B. Yu, R.Y. Yang, Discrete modelling of the compaction of non-spherical particles using a multi-sphere approach, Miner. Eng. 117 (2018) 108–116 | e · R6 — Hertz + Thornton–Ning · 비구형 압축 — 카드 없음 |
| 32 | S.C. Thakur, J.P. Morrissey, J. Sun, J.F. Chen, J.Y. Ooi, Micromechanical analysis of cohesive granular materials using the discrete element method with an adhesive elasto-plastic contact model, Granul. Matter 16 (2014) 383–400 | 정본 `thakur2014_eepa_adhesive_elastoplastic_dem` (원전 학위논문 = `morrissey2013_*`) |
| 33 | J. Zhang, H. Huang, J. Sun, Investigation on mechanical and microstructural evolution of lithium-ion battery electrode during the calendering process, Powder Technol. 409 (2022), https://doi.org/10.1016/j.powtec.2022.117828 117828 | e · h — LIB 전극 EEPA DEM ↔ 실험 — 카드 없음 (`zhang2026_xct_dem_cathode_calendering_peel_calibration` 은 다른 논문) |
| 34 · 35 | R.M. German, Prediction of packing and sintering density for bimodal powder mixtures, Adv. Powder Metall. 3 (1992) 1–15 · A.E.R. Westman, H.R. Hugill, the Packing of Particles, J. Am. Ceram. Soc. 13 (1930) 767–779 | 이원 충전 최적 Vf ≈ 0.3 (실험) — 카드 없음 (정본 `mcgeary1961_bimodal_sphere_packing` 은 같은 축 다른 논문) |
| 36 · 37 | A. Di Renzo, F. Paolo Di Maio, An improved integral non-linear model for the contact of particles in distinct element simulations, Chem. Eng. Sci. 60 (2005) 1303–1312 · H. Kruggel-Emden, S. Wirtz, V. Scherer, A study on tangential force laws applicable to the discrete element method (DEM) for materials with viscoelastic or plastic behavior, Chem. Eng. Sci. 63 (2008) 1523–1541 | ζ_tm 2/3 근거 — 카드 없음 |
| 38 | E.J. Cheng, K. Hong, N.J. Taylor, H. Choe, J. Wolfenstine, J. Sakamoto, Mechanical and physical properties of LiNi0.33Mn0.33Co0.33O2 (NMC), J. Eur. Ceram. Soc. 37 (2017) 3213–3217 | ★ NCM λp 0.38 · E₂ 출처 (yano2024 · yano2026 과 같음) — 카드 없음 |
| 39 | L.L. Baranowski, C.M. Heveran, V.L. Ferguson, C.R. Stoldt, Multi-Scale Mechanical Behavior of the Li3PS4 Solid-Phase Electrolyte, ACS Appl. Mater. Interfaces 8 (2016) 29573–29579 | ★ Li₃PS₄ λp 0.7 출처 — 카드 없음 |
| 40 | H. Nakamura, Y. Sugino, T. Iwasaki, S. Watano, Development of a novel tablet machine for a tiny amount of powder and evaluation of capping tendency, Chem Pharm Bull (Tokyo). 59 (2011) 1518–1522 | Ep/Ee (캡핑) — 카드 없음 |
| 41 | M. Suzuki, T. Oshima, Estimation of the co-ordination number in a two-component mixture of cohesive spheres, Powder Technol. 36 (1983) 181–188 | d — 이원 혼합 배위수 추정 (탄성 배위수가 작은 입자 추가에 안 변함의 근거) — 카드 없음 |

## [미확인] 목록
- 그림 7–11 · 그림 4 의 측정 시점 (누른 채 / 뺀 뒤) — 카드는 뺀 뒤로 추정 (§3e) · 공극의 겹침 처리 · 중앙 영역의 높이 위치.
- Δt · 전체 계산 시간 · 벽시계 시간 · CPU · GPU 기종 · 시드 · 반복 수.
- 운동 마찰 μ · 벽 마찰 · 벽 점착 · 온도.
- 그림 4 (c)(d) · 그림 S6 의 Vf (0.3 으로 보인다).
- SI 그림 S4 · S5 의 실제 λp (표 S2 는 0 · 값은 0.7 꼴) · 그림 S5 의 x = 5 조건이 표에 없는 이유.
- 나노압입 문헌 ([38] · [39]) 에서 λp 를 얻은 방법.
- 그림 7 Vf 0 λp 0 (0.421) ↔ SI S3 phase 3 (0.366) 차의 원인 (ζ_tm 1 ↔ 0.67 · 시드 · 영역).
- 접촉 면적 합 (그림 10) 의 영역 — 층 전체로 보인다 (§3d).

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)
- 서지: PDF 첫 쪽 *"Advanced Powder Technology 34 (2023) 104245"* · DOI *10.1016/j.apt.2023.104245* · 저자 *"Takeru Yano, Shuji Ohsaki ⇑, Hideya Nakamura, Satoru Watano"* · 교신 *shuji.ohsaki@omu.ac.jp* · 접수 · 수정 · 승인 · 온라인 날짜 — 후보 표 · 지시서 서지와 **같다** (후보 표는 제목을 '…' 로 줄임).
- 식 24 + SI 4 를 크롭에서 다시 읽고 §4a · §4b 에 옮김 · 식 (S4) 를 (S1) · (S3) 에서 다시 유도해 확인 · 표 2 f₀ 세 값 검산.
- 표 1 · 2 · S1 · S2 = 텍스트 층 + 크롭 대조 (표 2 의 f₀ 음의 부호는 크롭에서 확인 — 텍스트 층은 기호가 깨짐).
- 벡터 판독 자기 일관: 그림 9 → 그림 8 수 평균 (±1.9 %) · 그림 11b × 큰 입자 수 = 그림 10 큰–작은 (1–11 %) · 그림 10 세 종류 합 ↔ 총 (0.9–3.8 %) · 그림 S7 Ee ↔ 그림 6a (+1 – +11 %) · 그림 S7 (b) 유지 하강 ↔ 그림 5b 수직 하강 (같은 압력) · 그림 1 Hertz 검산 (0.0697 N) · 그림 S2 Hertz 검산 (5.645 N) · 그림 6a 비 ↔ 그림 6b (±3 %).
- '0.619' · '0.642' · 'LPSCl' · 'Li6PS5Cl' 문자열 = 본문 · SI 0 건 · '0.38' · '0.7' · 'Li3PS4' = p.4.
- 중복 확인: 정본 `litdb/papers/` 목록 · DOI · '104245' · 'bimodal powders with different' grep — 이 논문 카드 없음 (`yano2024_*` L90 · L500 · `yano2026_*` L425 가 인용만).

## 🔗 관련 카드
- 같은 그룹 · 같은 모델 줄기: `yano2024_eepa_binary_mixture_plasticity_compression_dem` (짝 · 성분마다 λp 가 다른 이원 혼합 + 이종 접촉 규칙 0.60 · 이 논문을 [22] 로 인용) · `yano2026_se_psd_width_ionic_tortuosity_dem` (이 논문을 ref 48 로 f₀ 설정 근거로 인용 — f₀ 세 값이 이 논문 표 2 와 같은 수 · §0-1) · `nakamura2020_dry_coating_ncm_li3ps4_core_shell` · `kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps`.
- EEPA 원전 · 학술지 판 · 소성 접촉 원전: `morrissey2013_eepa_elastoplastic_adhesion_dem_iron_ore_fines_thesis` · `thakur2014_eepa_adhesive_elastoplastic_dem` · `thorntonning1998_adhesive_elastoplastic_contact` (ref [30]) · `johnson1971_jkr_surface_energy_contact_elastic_solids` (ref [27] · f₀ 환산의 바탕).
- 단단 + 무른 / 크기 이원 압밀 DEM · 충전 (정본): `martinbouvard2003_dem_composite_cold_compaction` · `bouvard2000_hard_soft_powder_densification` · `mcgeary1961_bimodal_sphere_packing` (이원 충전 dip 의 실험 원전) · `otani2025_dem_se_dispersion_aggregation_compression` · `so2022_dem_compaction_coated_particles_assb`.
- 같은 300–400 MPa 급 가압 → 제하 의 큰 겹침 DEM (후보 C · 단일 재료): `zunker2025_dem_large_deformation_compaction`.
- λp 의 재료 쪽: `papakyriakou2021_mechanical_behavior_inorganic_li_solid_electrolytes_nanoindentation` (yano2026 의 LPSCl 0.642) · `sakuda2013_sulfide_mechanical_property` (ref [5]).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
