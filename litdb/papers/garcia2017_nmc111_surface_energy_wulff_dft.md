<!-- digest 표준 양식 확장 (paper-level STANDALONE).  ★ = 사용자가 특히 원한 항목.
     깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · 형식 이웃 = faka2026_particle_size_consolidation_strain_lpscl.md · 같은 묶음 = johnson1971_… · begat2004_….
     원문 = 10 쪽 · SI 없음 · 쪽 표기 = 인쇄 쪽 (PDF n 쪽 = p.(8289 + n)).  그림은 300 ppi 래스터 (Fig 12 만 600 ppi 회색조) — 크롭 300 dpi = 원 해상도.
     값 표지: [인쇄] = 본문 · 표 · 그림 안 인쇄 숫자 / [판독] = 그림에서 읽은 값 (litdb/figures/<slug>/digitized.csv · 원 래스터 색 분리 + 직선 맞춤) /
     [우리 산술] = 원문 값 또는 다른 정본 카드 값으로 한 계산 / [추정] = 우리 해석 / [미확인] = 원문에 없음. -->
# Surface Structure, Morphology, and Stability of Li(Ni1/3Mn1/3Co1/3)O2 Cathode Material — NMC111 저지수면 7 종의 DFT 표면 에너지 (GGA+U 구조 → HSE06 단일점) · (104) 0.76 · (001) 0.89 · (110) 재구성 1.32 · (012) 1.97 · (100) 2.27 J/m² · O · Li 화학퍼텐셜에 따른 Wulff 평형 형상 (평형 형상에는 (104) · (012) · (001) 만) · 표면 Co³⁺ 중간 스핀 · (012) 의 산소 빈자리 생성이 더 쉽다 — Garcia · Bareño · Yan · Chen · Hauser · Croy · Iddir (J. Phys. Chem. C 2017)

> slug `garcia2017_nmc111_surface_energy_wulff_dft` · DOI `10.1021/acs.jpcc.7b00896` · type `DFT (VASP · spin-polarised GGA-PBE+U geometry → HSE06 single-point surface energies · slabs with Tasker dipole compensation · Wulff construction vs Δμ_O, μ_Li · O-vacancy energetics) + experiment (molten-salt single-crystal NMC111/532 synthesis · SEM morphology)` · PDF `72c25f8c-40._Surface_Structure_Morphology_and_Stability_of_LiNi13Mn13Co13O2_Cathode_Material.pdf` · digested `2026-10-13` · status ✅
>
> **서지 (원문 인쇄)**: Juan C. Garcia† · Javier Bareño‡ · Jianhua Yan§ · Guoying Chen§ · Andrew Hauser∥ · Jason R. Croy‡ · **Hakim Iddir\*†** — † Materials Science Division, Argonne National Laboratory · ‡ Chemical Sciences and Engineering Division, Argonne · § Energy Storage and Distributed Resources Division, Lawrence Berkeley National Laboratory · ∥ University of Wisconsin-Madison · *J. Phys. Chem. C* **2017**, 121, 8290−8299 · DOI 10.1021/acs.jpcc.7b00896 · Received 2017-01-27 · Revised 2017-03-17 · Published 2017-03-28 · "The authors declare no competing financial interest" [인쇄 p.8290 · 8298].
> ★ **이 카드가 맡는 일** — 이종기술 논지 (`docs/hetero_thesis.md`) §4 **D4 (NCM · LPSCl 의 DFT 표면 에너지 · 계면 분리일)** 의 NCM 쪽 앵커 (단 NMC111) · §2-3 의 판가름 비 γ_NCM/γ_SE 를 "청정 표면 DFT" 수준에서 어디에 놓는가.
> **판독 원자료**: `litdb/figures/garcia2017_nmc111_surface_energy_wulff_dft/digitized.csv` (15 행 — Fig 10 · 11 직선 맞춤 · 포락선 교차 · Fig 12 점).

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 화학량론 NMC111 의 저지수면 표면 에너지 (면당, 0 K · 진공 · 청정) 는 **(104) 0.76 < (001) 0.89 < (110)_A 1.32 < (012) 1.97 < (100) 2.27 J/m²** [인쇄 Table 1] 이고, 평형 형상에는 (104) · (012) · (001) 만 남으며, 산화성이 클수록 (012) 가 커지고 Li 화학퍼텐셜이 낮을수록 (001) 판상이 된다 [인쇄 p.8296–8297].
우리 논지에 대어 보면 [우리 산술 — §7-1]: 이 청정 표면 값을 정본 `pustorino2025_…` 카드의 LPSCl 면당 γ (0.10–0.37 J/m², PBE) 와 나누면 **γ_NCM/γ_SE ≈ 2–20 ≫ 0.31** — 청정 벽개 에너지 수준에서는 논지 §2-3 표의 "SE 가 AM 을 덮는" 줄이다.  ⇒ 논지 P1 (비코팅에서 SE–SE 응집이 남는다) 은 **청정 표면 DFT 로는 지지되지 않고**, 실제 분말 표면 (흡착층 · 잔류 리튬염 · 반응층) 의 유효 γ 로만 갈린다.

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ★ NCM 표면 에너지 값 | **(104) 0.76 · (001) 0.89 · (110)_A 1.32 · (110)_B Co/Ni/Mn 1.67/1.77/1.88 · (012) 1.97 · (100) 2.27 J/m²** (화학량론 · 면당 — 식 1 의 1/(2A)) | [인쇄] Table 1 p.8293 |
| 어떤 계산인가 | VASP · 스핀 분극 · PAW · **GGA-PBE+U** (U−J = Ni 5.96 · Co 5.00 · Mn 4.84 eV) 로 구조 최적화 → **HSE06 단일점** 으로 표면 에너지 · 500 eV · 진공 10 Å · 격자상수 = 벌크 고정 · 에너지 수렴 0.003 eV · 벌크 k 3×3×3 · TM 배열 √3 형 (≥ 3 배 a · b 초격자) · 엔트로피 · 부피 항 무시 | [인쇄] p.8291 · 8293 |
| ⚠ 어느 범함수의 값인가 | Table 1 이 GGA+U 인지 HSE06 인지 **표 · 캡션에 없다** — 방법 절은 "HSE06 단일점으로 그 수준의 표면 에너지" 라고만 | [미확인] |
| ★ 평형 형상 (Wulff) | 평형 형상에는 **(104) · (012) · (001) 만** · 화학량론 · 덜 산화성 → (104) 우세 · 매우 산화성 (Δμ_O → 0) → **(012) 우세** · (001) 은 거의 일정 비율 · μ_Li 낮으면 (001) **판상** | [인쇄] p.8296–8297 · Fig 10–11 |
| μ 의존 (Fig 10 · 11) | (012) 의 최저 에너지 1.10 (1 ML O, Δμ_O = 0) ~ 2.10 J/m² · (001) 0.12 (¼ ML Li, μ_Li = −4.5 eV) ~ 1.45 J/m² | [판독] Fig 10 · 11 |
| ⚠ 내부 불일치 | Fig 10 · 11 의 화학량론 (½ ML) 수평선 **2.10 · 1.45 J/m²** ↔ Table 1 **1.97 · 0.89** · 본문 "(104) … 0.79 J/m² (중간/고스핀 Co³⁺)" ↔ Table 1 0.76 | [판독] + [인쇄] |
| 실험 대조 | 용융염 (CsCl flux) 단결정 NMC532 · 111 — 산화성 조건 (LiNO₃, R = 2, 850 °C 8 h) 에서 노출면 **≈70 % 가 (012)** · Li₂CO₃, R = 4, 900 °C 12 h 결정 = 고 O · 저 Li 조건 계산 형상과 "excellent agreement" | [인쇄] p.8293 · 8296–8297 |
| 표면 화학 | (104) 표면 Co³⁺ = **중간 스핀** (2.3 µB, t₂g⁵e_g¹) — (104) 안정의 원인 · O 빈자리 생성 에너지 (104): Co 축 5.4 · Ni 축 2.2 · Mn 축 1.5 eV / (012): Co,Ni 적도 1.9 · Co,Mn 1.1 · Mn,Ni 0.6 eV · Li < ≈40 % (104) · < 60 % (012) 에서 O 방출 자발 | [인쇄] p.8294–8297 · Table 2 |
| NCM811 에 쓸 수 있나 | 원문은 111 (계산) · 111/532 (형상 실험) 만 — "as the relative Ni content increases, the effect of Li/Ni exchange and/or TM segregation may play an important role. Studies along these lines are currently in progress" | [인쇄] p.8297 · [미확인] 811 |

⛔ **한정어 (떼지 말 것)**: ① **NMC111** (811 아님) ② 0 K · 진공 · 청정 · 화학량론 (또는 μ 조건) — **흡착 · 잔류 리튬염 · 수분 없음** ③ 면당 값 (식 1 의 2A) — 벽개일 (두 면) 은 2 배 ④ 범함수 (Table 1) [미확인] · 슬랩 두께 · 슬랩 k 점 [미확인] ⑤ 표 ↔ 그림 값 불일치 (§10-1) ⑥ "표면 에너지" 는 **결합을 끊는 에너지**이지 입자 접촉의 분산 (반데르발스) 점착 에너지가 아니다 — 입자 점착의 W 로 바로 쓰지 않는다 (§7-2).

---

## 1. 한 줄 요약
NMC111 의 저지수면 7 종 (비극성 (104) · (100) · 극성 (001) · (012) · (110)) 을 쌍극자 없는 화학량론 슬랩으로 만들어 GGA+U 로 이완하고 HSE06 단일점으로 표면 에너지를 구했다.
(104) 가 가장 낮고 (0.76 J/m², 끊어지는 M–O 결합 하나), (100) 이 가장 높다 (2.27, 셋) — "끊어진 결합 수" 로 순위가 설명된다.
극성 (012) 는 O 피복 (Δμ_O), (001) 은 Li 피복 (μ_Li) 에 따라 에너지가 바뀌어 Wulff 형상이 합성 조건으로 바뀐다 — 산화성 소성은 (012) 가 지배하는 다면체, 낮은 μ_Li 는 (001) 판상 — 이것을 용융염 단결정 NMC532 · 111 의 SEM 형상과 맞췄다.
(104) 표면 Co³⁺ 는 중간 스핀이라 그 면을 안정화하고 (Co 의 표면 편석 동인), 산소 빈자리는 Mn 위에서 가장 쉽고 (Mn 용출 경로 후보), (012) 가 (104) 보다 쉽게 환원된다 (전해질 산화 반응성 ↑).

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| J. C. Garcia · J. Bareño · J. Yan · G. Chen · A. Hauser · J. R. Croy · **H. Iddir\*** (Argonne · LBNL · Wisconsin–Madison) | J. Phys. Chem. C **121** (2017) 8290–8299 | 10.1021/acs.jpcc.7b00896 | **Li(Ni1/3Mn1/3Co1/3)O₂ (NMC111)** 계산 · 실험 단결정 **NMC532 · NMC111** | DFT (표면 · Wulff · 빈자리) + 합성 · SEM |

| 원문 구조 | 쪽 | 내용 |
|---|---|---|
| Introduction | 8290–8291 | NMC 표면 불안정 · LCO/LNO 선행 (Kramer & Ceder: (104) · (001) · (012)) · NMC111 부피 100.6 Å³ (LCO 96.8 · LNO 102.3 사이) |
| 2. Methodology | 8291–8293 | 계산 조건 · TM 배열 (Fig 1) · (110) 재구성 (Fig 2–3) · (001) (Fig 4) · (012) (Fig 5) · 식 (1)–(2) · 용융염 합성 |
| 3.1 Surface energies and morphology | 8293–8295 | Table 1 · (104) (Fig 6) · (110)_A (Fig 7) · (012)/(100) (Fig 8) · Co 스핀 (Fig 9) |
| 3.2 Thermodynamic analysis of polar surfaces | 8295–8297 | Fig 10 ((012) vs Δμ_O) · Fig 11 ((001) vs μ_Li) · SEM 대조 |
| 3.3 Oxygen vacancy formation | 8297 | Table 2 · Fig 12 (vs Li 함량) |
| 4. Conclusions · References (39) | 8297–8299 | |

- 중복 확인 (2026-10-13): 정본 `litdb/papers/` 전수 목록에 garcia · nmc111 표면 파일 없음 · `git grep -i` "jp7b00896" · "Surface Structure, Morphology" 0 건 → 새 카드.

---

## 3. 핵심 수치 (★ 쪽 · 표지 병기)

### 3-1. 계산 조건 [인쇄 p.8291 · 8293]
| 항목 | 값 |
|---|---|
| 코드 · 기법 | VASP · 스핀 분극 DFT · PAW · GGA (PBE) |
| +U (Dudarev U−J) | Ni **5.96** · Co **5.00** · Mn **4.84** eV (ref 28 = Iddir & Benedek 2014) |
| 표면 에너지 단계 | DFT+U 기하 최적화 → **HSE06 단일점** ("to determine the surface energy at that level of theory") |
| 컷오프 · 수렴 | 500 eV · 이온 이완은 총에너지 차 ≤ 0.003 eV |
| 슬랩 | 주기 슬랩 · **진공 10 Å** · 격자상수 = 벌크 값 고정 · 극성면은 위층 전하 절반을 아래층으로 옮겨 쌍극자 상쇄 (Tasker type III → II) · 두께 [미확인] ("thicker slabs (>9 layer) should be used" 라는 서술만) · 슬랩 k 점 [미확인] |
| 벌크 | k 3×3×3 · TM 배열은 각 이온이 다른 TM 3 개씩 삼각으로 6 이웃 (고체 NMR ref 30 · 정전 기준 하위 30 배열 DFT 로 확인) · 벌크 Co³⁺ · Ni²⁺ · Mn⁴⁺ (자화 · Bader) |
| 표면 에너지 식 | (1) γ = (E_slab − E_bulk)/(2A) — 화학량론 · (2) γ = (1/2A)(E_slab − E_bulk + Σ Δ_i μ_i) — 비화학량론 · 엔트로피 · 부피 항 무시 |
| (110) 처리 | (110)_A = 반 피복 "missing-row" 재구성 (Fig 3c, Fig 3b 보다 0.44 eV 낮음) · (110)_B = TM 층을 한 칸 올린 확장 결함 (벌크 ΔE 0.02 eV) |
| (001) 처리 | ½ ML Li 종단 (선행 연구가 가장 유리) — μ_Li 에만 민감 |
| (012) 처리 | O 종단 · ½ ML O 이면 화학량론 · 자리 A (TM 2 + Li 1 배위) 점유가 안정 |

### 3-2. ★ Table 1 — 화학량론 표면 에너지 (J/m², 면당) [인쇄 p.8293]
| 면 | 종단 | γ |
|---|---|---|
| (104) | Ni, Mn, Co, O | **0.76** |
| (001) | Ni, Mn, Co, O | **0.89** |
| (110)_A (표면 재구성) | Ni, Mn, Co, O | 1.32 |
| (110)_B (벌크 확장 결함) | Co, O · Ni, O · Mn, O | 1.67 · 1.77 · 1.88 |
| (012) | Ni, Mn, Co, O | **1.97** |
| (100) | Ni, Mn, Co, O | 2.27 |
- 순위 근거: (104) 는 M–O 결합 하나만 끊는 비극성 평탄면 · (100) 은 표면 TM 이 3 배위 (결합 셋 손실) — "more than double the energy of the other nonpolar, (104) surface" [인쇄 p.8293–8294].
- 비교 (원문 인용): LCO (104) 0.31 J/m² (중간/고스핀 Co³⁺) vs 1.0 (저스핀) — Qian 2012 (ref 21) · LNO 는 모든 면에서 LCO 보다 낮다 (ref 22) [인쇄 p.8291 · 8295].

### 3-3. ★ μ 의존 — Fig 10 ((012) vs Δμ_O) · Fig 11 ((001) vs μ_Li) [판독 — 직선 맞춤 rms ≤ 0.05 J/m²]
| 그림 · 피복 | 맞춘 직선 γ (J/m²) | 끝값 |
|---|---|---|
| Fig 10 · ½ ML O (화학량론) | 2.10 (수평) | ⚠ Table 1 은 1.97 |
| Fig 10 · ¼ ML O | 0.496·Δμ_O + 3.13 | 1.64 (Δμ_O = −3) |
| Fig 10 · ¾ ML O | −0.632·Δμ_O + 1.27 | 3.16 (−3) → 1.27 (0) |
| Fig 10 · 1 ML O | −1.120·Δμ_O + 1.10 | **1.10 (Δμ_O = 0)** |
| Fig 11 · ½ ML Li (화학량론) | 1.45 (수평) | ⚠ Table 1 은 0.89 |
| Fig 11 · ¼ ML Li | 0.502·μ_Li + 2.37 | **0.12 (μ_Li = −4.5)** |
| Fig 11 · ¾ ML Li | −0.622·μ_Li + 1.99 | 0–(−4.5) 범위에서 최저가 되지 않음 |
- [우리 산술 — 맞춘 직선의 교차] (012) 최저 포락선: Δμ_O < −2.06 → ¼ ML · −2.06 ~ −1.32 → ½ ML (2.10) · −1.32 ~ −0.35 → ¾ ML · > −0.35 → 1 ML (1.49 → 1.10).  (001): μ_Li < −1.83 eV → ¼ ML (판상 형상) · 그 위 → ½ ML.
- Fig 10 보조 축 [인쇄]: Δμ_O ↔ T (p_O₂ 0.2 atm: 0–2000 °C) · p_O₂ (T 850 °C: 10⁻¹⁶ – 10⁸ atm · T 900 °C: 10⁻¹⁴ – 10¹⁰ atm) · Δμ_O(T,P) = μ_O − ½μ_O₂.  Fig 11 x 축 = μ_Li(T,P) = μ°_Li − μ_Li-metal · 오른쪽 형상은 μ_Li ≈ −2.5 eV.
- 본문 (p.8296): 높은 T (0.2 atm 고정) · 높은 p_O₂ 가 (012) 피복 · 안정을 키운다 · (001) 은 ¼ ML Li 피복에서 우세 → 판상.

### 3-4. 표면 전자 구조 · 산소 빈자리 [인쇄 p.8294–8297]
- (104) 표면 Co: 자화 2.3 µB · t₂g⁵e_g¹ = **중간 스핀** · 표면 Co–O 축 2.01 Å · 적도 1.95 Å (벌크 1.99 Å) · 사각뿔 배위 — "intermediate spin Co³⁺ ions lower the (104) surface energy" (초록) · Co 의 (104) 편석 동인 (ref 10).
- (012) 표면 Co: 같은 5 배위인데 **저스핀** (자화 0) — 사각뿔이 표면과 ≈45° 로 기울어 결합 1.8 · 2.1 · 2.02 Å.
- 전 슬랩 이완 시 내부 팔면체 왜곡 (축 2.21 · 적도 1.96 Å) → 내부에 비물리적 중간 스핀 → **벌크 영역 고정 + 바깥 두 층만 이완** 으로 계산.
- Table 2 (O 빈자리 생성, eV): (104) Co 축 **5.4** · Ni 축 **2.2** · Mn 축 **1.5** / (012) Co,Ni 적도 **1.9** · Co,Mn **1.1** · Mn,Ni **0.6** — 빈자리는 Mn 위에서 가장 쉽다 (Mn 용출 경로 후보).
- Fig 12 [판독]: (104) 11 % Li −9.3 · 33 % −2.0 · 55 % +0.9 · 78 % +4.1 · 100 % +1.5 eV / (012) 33 % −6.0 · 55 % −1.0 · 78 % +0.6 · 100 % +0.5 eV · 0 교차 ≈45 % ((104)) · ≈63 % ((012)) — 본문 "below ∼40 % (104) · below 60 % (012)".

### 3-5. 합성 실험 [인쇄 p.8293 · 8296–8297]
- 용융염: TM 질산염 + LiNO₃ 또는 Li₂CO₃ **10 % 과잉 (Li:M 1.1:1)** · CsCl flux (m.p. 645 °C) · R (flux/TM 몰비) 2 또는 4 · 알루미나 도가니 · 200 °C 5 h 건조 → 4 °C/min 로 850 또는 900 °C · 8 또는 12 h · 4 °C/min 냉각 · 탈이온수 세척 · 80 °C 진공 건조.
- Fig 10 SEM (100 nm 막대): NMC532 · LiNO₃ · R 2 · 공기 850 °C 8 h → **노출면 ≈70 % (012)**.
- Fig 11 SEM: NMC532 · Li₂CO₃ · R 4 · 900 °C 12 h (1 µm 막대) · 같은 조건 NMC111 (100 nm 막대) → 고 O · 저 Li 계산 형상과 일치.

---

## 4. ★ 방법 — 계산 사슬 · 입자 처리

### 4-1. 계산 사슬
벌크 NMC111 (R3̄m · TM 배열 확정) → 저지수면 슬랩 (화학량론 · 쌍극자 상쇄 재배열: (110) missing-row · (001) ½ ML Li · (012) ½ ML O) → GGA+U 이완 (바깥 두 층) → HSE06 단일점 → 식 (1) 표면 에너지 (Table 1) → 극성면의 피복 변화 + 식 (2) 로 Δμ_O · μ_Li 의존 (Fig 10 · 11) → Wulff 작도 (Cahn & Carter, ref 23) 로 평형 형상 → 단결정 SEM 과 대조 → 표면 O 빈자리 (Table 2 · Fig 12).

### 4-2. ★ 입자 처리 (DEM 판 "무질서 처리")
- **평형 결정 형상** (Wulff) = 각 면의 표면 에너지에 비례하는 거리에 면을 놓은 다면체 — 입자 크기 · 응집 · 2차입자 (다결정) 없음.  실험은 **단결정 1차입자** (≈100 nm–1 µm).
- 우리 쪽 대응: AM_S (단결정 NCM) 의 면 구성이 합성 조건으로 바뀐다는 근거 — 그러나 우리 DEM 은 구 (면 없음) · 다결정 AM_P 는 2차입자 표면 (1차입자 여러 면 혼합) [추정].

### 4-3. 기법 미니 용어집
- **표면 에너지 γ (DFT)**: 슬랩 − 벌크 에너지 차 ÷ 새 면 넓이 (두 면이면 2A).  0 K · 진공 · 결합 절단 에너지 — 실온 분말 표면의 "유효 표면 에너지" (IGC · 접촉각) 와 다른 양.
- **Tasker type I · II · III**: 이온 결정 면의 층 전하 · 쌍극자 분류 — III (층 전하 + 쌍극자) 은 재구성 없이 불안정.
- **화학퍼텐셜 Δμ_O · μ_Li**: 비화학량론 종단의 에너지를 합성 분위기 (T · p_O₂ · Li 활동도) 에 묶는 변수.
- **Wulff 작도**: 면별 γ 로 평형 형상을 만드는 기하 작도.
- **중간 스핀 (IS) Co³⁺**: t₂g⁵e_g¹ — 5 배위 표면에서 결정장 분리가 바뀌어 나타남.
- **O 빈자리 생성 에너지**: 표면 O 하나를 빼는 에너지 — 환원 · O 방출 · 전해질 산화 반응성의 지표.

---

## 5. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | (a) NMC111 R3̄m 벌크 · (b) TM 층 배열 (Ni · Mn · Co 삼각 배열) | TM 배열 규약 |
| 2 | (110) 슬랩 쌍극자 처리 (a 원 슬랩 · b TM 한 칸 이동 · c 위아래 전하 절반 이동) | 극성면 처리 — 우리 DFT (D4) 에서 같은 문제 |
| 3 | (110) 위층 (a 원 · b 줄 교대 빈자리 · c missing-row) | 재구성 |
| 4 | (001) 슬랩 (½ ML Li 위아래 · 대칭면) | (001) 종단 |
| 5 | (012) ½ ML O · 자리 A · B | O 피복 자리 |
| 6 | (104) 위 두 층 | 최저 에너지면 |
| 7 | (110)_A 재구성 — (104) 소면의 지그재그 | 재구성이 (104) 로 간다 |
| 8 | (012) 1 ML · ½ ML O · (100) 위 세 층 | |
| 9 | Co d 오비탈 PDOS (표면 IS · 벌크 LS) + 전자 배치 모식 | 표면 스핀 |
| 10 | ★ (012) γ vs Δμ_O (피복 4 종) + Wulff 형상 5 + T · p_O₂ 보조축 + NMC532 SEM (≈70 % (012)) | 합성 조건 → 면 구성 · ⚠ ½ ML 선 2.10 ↔ Table 1 1.97 |
| 11 | ★ (001) γ vs μ_Li (피복 3 종) + Wulff 형상 4 (판상 → 다면체) + NMC532 · 111 SEM | ⚠ ½ ML 선 1.45 ↔ Table 1 0.89 |
| 12 | O 빈자리 생성 에너지 vs Li 함량 ((104) · (012)) | 고 SOC 에서 O 방출 자발 |
| Table 1 | ★ 화학량론 표면 에너지 7 종 | D4 의 NCM 쪽 숫자 |
| Table 2 | O 빈자리 생성 에너지 (배위별) | 면 · 원소 의존 반응성 |

## 6. Post-processing ★
- **원문**: 자화 · Bader · PDOS 로 산화수 · 스핀 판정 · Wulff 작도 (도구 [미확인]) · SEM 형상 정성 대조 (노출면 ≈70 % 는 방법 미기술).
- **안 한 것**: 슬랩 두께 수렴 · 범함수 간 표면 에너지 비교 표 · 분산 (vdW) 보정 · 흡착 (H₂O · CO₂) 표면 · NCM811 · 면적 가중 평균 γ.
- **이 카드에서 한 것**: Fig 10 · 11 의 피복 직선을 원 래스터에서 색 분리해 맞춤 (rms ≤ 0.05 J/m²) · 포락선 교차 · Fig 12 점 판독 (`digitized.csv`) · LPSCl 값과의 비 (§7-1).

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 쪽 수치는 리포 출처를 병기)

### 7-1. ★ 논지 §2-3 의 비 γ_NCM/γ_SE 를 청정 표면 DFT 로 놓으면 [우리 산술 · 추정]
- NCM 쪽 (이 논문, NMC111 · 면당): 평형 형상 면 **0.76 ((104)) · 0.89–1.45 ((001), Table ↔ 그림) · 1.10–2.10 ((012), Δμ_O 따라)** J/m².
- SE 쪽 (정본 `pustorino2025_lpscl_bulk_surface_mechanical_electronic_li_filament` 카드): LPSCl 면당 γ = PS₄ 종결 0.10 · Li₂S-rich 0.37 J/m² (대칭 슬랩 · μ 조건값 · PBE · vdW 없음) · 같은 면 화학량론 벽개 (두 면) 0.47 J/m² → 면당 평균 ≈0.24 J/m².
- ⇒ **γ_NCM/γ_SE ≈ 0.76/0.37 = 2.1 … 2.27/0.10 = 23** (면당 평균끼리면 0.76/0.24 ≈ 3.2) — 논지 §2-3 문턱 **0.31 보다 7–70 배 크다**.  논지 표의 첫 줄 ("γ_A ≥ γ_S → SE 가 AM 을 덮는 방향") 에 해당한다.
- 같은 방향의 다른 근거: 정본 `lee2026_mechanical_halogen_argyrodite_drycoating` 카드 기록의 SE 슬랩 | LiNiO₂ (NCM 을 단순화) 계면 W_ad (MLIP · rigid single-point · 5 조성) **0.70–1.95 J/m²** ≥ LPSCl 화학량론 벽개 0.47 J/m² — 계산 수준에서 SE 는 SE 끼리보다 산화물 표면에 더 세게 붙는다 (⚠ 그 카드가 결합곡선 꼬리가 0 으로 안 가는 문제를 지적).
- ⚠ **이 결론은 청정 · 0 K · 결합 절단 수준의 이야기다** — 논지 P1 이 기대는 것은 **실제 분말 표면의 유효 (분산 위주) 점착** 이고, 그 비는 (i) NCM 의 잔류 Li₂CO₃ · LiOH · 흡착수 (ii) LPSCl 의 산화 · 가수분해 층 (iii) 거칠기 (johnson1971 카드 §7-4) 로 정해진다.  범함수도 다르다 (HSE06/GGA+U ↔ PBE).  ⇒ D4 에 주는 요구: **같은 범함수 · 같은 이완 규약 · 현실 종단 (흡착층 포함)** 으로 NCM · LPSCl 을 함께 계산하고, IGC · AFM (begat2004 카드) 의 실측 비와 대조.

### 7-2. 표면 에너지 (벽개) ≠ 입자 점착의 W — 왜 그대로 넣으면 안 되나 [추정]
- 우리 믹서 DEM 점착 (SJKR · CED) 이 표현하는 것은 입자 접촉의 분리일 W (johnson1971 카드 §7-1 대응식 CED = [9WE\*²/(4π²R\*)]^{1/3}).  같은 물질의 W = 2γ 는 **같은 결합을 다시 붙이는** 이상적 경우 (벽개 면을 정확히 다시 맞붙임) 에만 성립한다.
- 실제 분말 접촉은 서로 다른 방위 · 흡착층 · 돌기에서 만나 결합 대부분을 재형성하지 못한다 — 실온 산화물 분말의 유효 표면 에너지 (IGC 분산 성분) 가 DFT 벽개 에너지보다 훨씬 작게 나오는 이유 [추정 — 값은 IGC 카드 (같은 묶음) 에서 확인].
- ⇒ 이 논문 값으로 CED 를 정하면 W 가 과대 (수 J/m²) → 우리 parcel 규모 LC 의 W_eq (6×10⁻⁶ J/m², johnson1971 카드 §7-1) 와 비교할 대상이 아니다.  쓸 수 있는 것은 **면 사이 순위 · 조건 의존성** (예: (012) 가 많은 산화성 합성 입자가 더 "끈적" 할 가능성 [추정]).

### 7-3. 단결정 AM_S · 코팅 공정에 주는 것
- 합성 분위기 (Δμ_O · μ_Li) 가 단결정 NCM 의 노출면 비율 ((104) ↔ (012) ↔ (001)) 을 바꾼다 [인쇄] → 같은 "단결정 NCM" 이라도 표면 에너지 · 반응성이 다르다 (예: O 빈자리 생성 (012) < (104)) [추정: 황화물 계면 반응도 면 의존일 수 있다].
- 건식 SE 선코팅 (논지 §2-5) 에서 SE 가 먼저 붙는 면이 (012) 쪽일지 [추정] — 이 논문은 SE 를 다루지 않는다.

### 7-4. 우리 DFT (D4) 계획에 주는 것
- 극성면 쌍극자 처리 (Tasker) · μ 의존 종단 · 벌크 영역 고정 (내부 팔면체 왜곡 → 비물리 스핀) · 슬랩 두께 (> 9 층 권고) — **NCM811 슬랩을 만들 때의 함정 목록**.
- Ni-rich 효과 (Li/Ni 자리바꿈 · TM 편석) 는 이 논문 밖 — 811 표면 에너지는 [미확인].
- 정본 `our_dft_baseline.md` 의 우리 LPSCl 계산 (PBE 계열) 과 범함수를 맞춰야 비가 뜻이 있다.

### 7-5. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 원자 척도 표면 에너지 · 형상 · 표면 반응성 (DFT) — 우리 쪽 D4 (DFT) 와 같은 층.
- **없는 것**: 입자 점착 · 분말 · 혼합 · 압밀 · 수송 · SE.  DEM · MPM 입력으로 직접 들어가지 않는다 (§7-2).

---

## 8. 적용 인사이트 (내 연구에 어떻게)
1. **D4 의 NCM 쪽 기준값** (NMC111 · 청정 · 면당): (104) 0.76 · (001) 0.89 · (012) 1.97 J/m² — 표 ↔ 그림 불일치 (§10-1) 를 같이 적는다.
2. **청정 표면 DFT 비 γ_NCM/γ_SE ≈ 2–20 ≫ 0.31** — 논지 P1 은 청정 표면으로는 서지 않는다.  P1 을 지키려면 "실제 표면 상태" 를 계산 · 측정해야 한다 (논지 §2-3 ⚠ 의 구체화).
3. **벽개 γ 를 DEM 점착 W 로 넣지 않는다** — 순위 · 조건 의존만 쓴다.
4. **합성 분위기 → 면 구성 → 표면 성질** — 단결정 AM_S 공급사 · 소성 조건 기록이 필요 (코팅 · 점착 실험 해석의 교란 변수).
5. **NCM811 은 [미확인]** — Ni-rich 표면 (Li/Ni 자리바꿈) 은 별도 문헌 · 계산 필요.

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "DFT (GGA+U geometries, HSE06 single points) gives stoichiometric NMC111 surface energies of 0.76 (104), 0.89 (001), 1.32 (reconstructed 110), 1.97 (012) and 2.27 J m⁻² (100); only (104), (012) and (001) appear in the equilibrium (Wulff) shapes (Garcia et al., J. Phys. Chem. C 2017)."
- "Oxidizing synthesis conditions stabilize the oxygen-covered (012) facet, which dominated (~70 %) the exposed surfaces of molten-salt NMC532 crystals."
- 국문: *"청정 표면 DFT 값 (NMC111 0.76–2.27 · LPSCl 0.10–0.37 J/m²) 의 비는 2–20 으로, 이종기술 논지의 SE–SE 응집 조건 (γ_NCM/γ_SE < 0.31) 과 정반대다 — 그 조건은 실제 분말 표면 상태에서만 판정할 수 있다 (우리 산술)."*

## 10. 주의/한계 (over-claim 방지 · 원문 비판)
1. ★ **표 ↔ 그림 불일치**: Fig 10 의 (012) ½ ML (화학량론) 수평선 **2.10 J/m²** ↔ Table 1 **1.97** (+7 %) · Fig 11 의 (001) ½ ML 수평선 **1.45 J/m²** ↔ Table 1 **0.89** (+63 %) [판독 — 원 래스터 색 분리 · rms 0.002] · 본문 (104) "0.79 J/m² (high/intermediate spin)" ↔ Table 1 0.76.  범함수 (GGA+U ↔ HSE06) 나 이완 규약이 다를 가능성 [추정] — 원문은 어느 값이 어느 수준인지 밝히지 않는다 [미확인].  Wulff 형상 (Fig 10–11) 이 어느 (001) 값을 썼는지도 [미확인].
2. **슬랩 두께 · 슬랩 k 점 · Wulff 도구 [미확인]** — 그리고 저자 스스로 "thicker slabs (>9 layer) should be used" 라며 벌크 영역을 고정했다 (전 이완은 내부에 비물리 스핀).
3. **NMC111 만 계산** — 형상 실험은 532 · 111.  Ni-rich (811) 는 "in progress".
4. **엔트로피 · 부피 항 무시 · vdW 보정 없음** — 고온 (850–900 °C) 합성 형상과의 비교는 정성.
5. **"≈70 % (012)" 의 산출법 미기술** — SEM 한 장의 정성 판단으로 보인다 [추정].
6. **O 빈자리 · Li 함량 곡선 (Fig 12)** 은 점 4–5 개 + 맞춘 곡선 · "spontaneous below ∼40 %" 는 곡선 교차 (판독 ≈45 %) 보다 낮게 적혀 있다.
7. **전이 한계**: 0 K · 진공 · 청정 표면 — 액체 전해질 · 황화물 SE · 흡착층 없는 조건.  반응성 결론 ((012) 가 전해질 산화에 더 반응적) 은 액체 전해질 맥락의 추론이다.

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| 19 | Kramer, D.; Ceder, G. Tailoring the Morphology of LiCoO2: A First Principles Study. Chem. Mater. 2009, 21, 3799−3809. | 층상 산화물 표면 에너지 · Wulff 방법의 원형 |
| 21 | Qian, D.; Hinuma, Y.; Chen, H.; Du, L.-S.; Carroll, K. J.; Ceder, G.; Grey, C. P.; Meng, Y. S. Electronic Spin Transition in Nanosize Stoichiometric Lithium Cobalt Oxide. J. Am. Chem. Soc. 2012, 134, 6096−6099. | LCO (104) 0.31 vs 1.0 J/m² (스핀) |
| 22 | Kim, Y.; Lee, H.; Kang, S. First-Principles and Experimental Investigation of the Morphology of Layer-Structured LiNiO2 and LiCoO2. J. Mater. Chem. 2012, 22, 12874−12881. | Ni-rich 끝 (LNO) 표면 에너지 — 811 쪽 근거 |
| 28 | Iddir, H.; Benedek, R. First-Principles Analysis of Phase Stability in Layered−Layered Composite Cathodes for Lithium-Ion Batteries. Chem. Mater. 2014, 26, 2407−2413. | U 값 출처 |
| 31 | Tasker, P. W. The Stability of Ionic Crystal Surfaces. J. Phys. C: Solid State Phys. 1979, 12, 4977. | 극성면 분류 |
| 37 | Maram, P. S.; Costa, G. C. C.; Navrotsky, A. Experimental Confirmation of Low Surface Energy in LiCoO2 and Implications for Lithium Battery Electrodes. Angew. Chem., Int. Ed. 2013, 52, 12139−12142. | ★ 표면 에너지 **실측** (열량) — DFT 값과의 다리 |
| 38 | Vallverdu, G.; Minvielle, M.; Andreu, N.; Gonbeau, D.; Baraille, I. First Principle Study of the Surface Reactivity of Layered Lithium Oxides LiMO2 (M = Ni, Mn, Co). Surf. Sci. 2016, 649, 46−55. | 표면 반응성 (흡착) |
| 10 | Yan, P.; Zheng, J.; … Ni and Co Segregations on Selective Surface Facets and Rational Design of Layered Lithium Transition-Metal Oxide Cathodes. Adv. Energy Mater. 2016, 6, 1502455. | 면 선택 편석 실측 |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-13)
- 10 쪽 전부 쪽 이미지로 읽고 `pdftotext` 로 인용 대조 · DOI 는 매 쪽 하단 인쇄 (10.1021/acs.jpcc.7b00896).
- Fig 10 · 11 은 PDF 원 래스터 (300 ppi, pdfimages) 에서 틀 · 눈금을 검출하고 색으로 네 피복 직선을 분리해 맞췄다 (rms 0.002–0.052 J/m²) — 표 ↔ 그림 불일치는 이 판독에서 나왔다.
- 크롭 14 장 = Fig 1–12 (자동 추출, 원 해상도 300 dpi — 캡션은 figures.json) + Table 1–2 (손 크롭) · Fig 6 은 옆 단 글자가 섞여 손으로 다시 잘랐다.
- 정본 litdb 중복 확인: 파일 목록 + DOI · 제목 낱말 `git grep` 0 건.

## 🔗 관련 카드
- LPSCl 표면 · 벽개: `pustorino2025_lpscl_bulk_surface_mechanical_electronic_li_filament`.
- SE|NCM 계면 W_ad (계산) · AFM: `lee2026_mechanical_halogen_argyrodite_drycoating`.
- 같은 묶음 (점착 · 표면 에너지 측정): `johnson1971_jkr_surface_energy_contact_elastic_solids` · `begat2004_cohesive_adhesive_balance_afm_colloid_probe`.
- NCM 기계 물성: `sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile` · `xu2017_nmc532_nanoindentation_modulus_hardness_toughness`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
