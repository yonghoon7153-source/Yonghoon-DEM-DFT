<!-- digest 표준 양식 확장 (paper-level STANDALONE).  ★ = 사용자가 특히 원한 항목.
     깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · 형식 이웃 = faka2026_… · 같은 묶음 = johnson1971_… · begat2004_… · garcia2017_… · vanoss1988_… · fowkes1964_….
     원문 = 24 쪽 리뷰 (본문 18 쪽 + 참고문헌 336) · SI 없음 · 쪽 표기 = 인쇄 쪽 (PDF n 쪽 = p.(20 + n)).  그림은 PDF 안 200 ppi JPEG — 크롭 300 dpi (원 이상 정보 없음).
     값 표지: [인쇄] = 본문 · 표 · 그림 안 인쇄 숫자 / [판독] = 그림에서 읽은 값 (litdb/figures/<slug>/digitized.csv) / [우리 산술] / [추정] / [미확인] = 원문에 없음. -->
# Inverse gas chromatography applications: A review — 역기체크로마토그래피 (IGC): 분말을 칼럼에 채우고 탐침 증기 (n-알칸 · 극성 분자) 의 머무름으로 **분산 표면 에너지 γ_S^D** (Schultz · Dorris–Gray) · 특이 (산·염기) 자유에너지 ΔG^SP · van Oss γ⁺/γ⁻ · Gutmann K_A/K_B · **표면 에너지 불균일 (덮임률에 따른 분포)** · 응집 · 접착 일을 잰다 — 석영 γ_S^D 52.76 (Schultz) / 52.61 (Dorris–Gray) mJ/m² @5 % · 덮임률 따라 38–66 — Mohammadi-Jam · Waters (Adv. Colloid Interface Sci. 2014)

> slug `mohammadijam2014_inverse_gas_chromatography_review` · DOI `10.1016/j.cis.2014.07.002` · type `review (inverse gas chromatography: instrumentation, Schultz / Dorris–Gray dispersive surface energy, specific free energy, van Oss and Gutmann acid–base, surface-energy heterogeneity, applications to polymers, pharmaceuticals, minerals, nanomaterials) + new SEA data on quartz, talc, D-mannitol, acetate film` · PDF `dbaae954-41._Inverse_gas_chromatography_applications_A_review.pdf` · digested `2026-10-13` · status ✅
>
> **서지 (원문 인쇄)**: S. Mohammadi-Jam · K. E. Waters\* (Department of Mining and Materials Engineering, McGill University, Montreal) · *Advances in Colloid and Interface Science* **212** (2014) 21–44 · Available online 2014-07-15 · http://dx.doi.org/10.1016/j.cis.2014.07.002 [인쇄 p.21].  사사: NSERC CRD (SGS Canada · Shell Canada · Barrick Gold · COREM · Teck · Vale · CheMIQA & Xstrata) · CFI (SEA 장비) [인쇄 p.38].
> ★ **이 카드가 맡는 일** — 이종기술 논지 (`docs/hetero_thesis.md`) §2-8 *"측정: 코팅 전후 NCM · SE 분말의 유효 표면 에너지 (역기체크로마토그래피 IGC)"* 의 방법 카드 — **무엇을 재나 · 시료 조건 · 불확도 · 공기 민감 황화물에 쓸 수 있나**.
> **판독 원자료**: `litdb/figures/mohammadijam2014_inverse_gas_chromatography_review/digitized.csv` (22 행 — Fig 8 덮임률 분포 17 점 · Fig 4 · 6 · 9 검산).

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: IGC 는 분말을 **적시지 않고** (액체 접촉 없음) 건조 불활성 운반 기체 (He · Ar · N₂) 속에서 탐침 증기의 머무름 부피로 **γ_S^D (분산 성분)** 와 극성 탐침의 **특이 자유에너지 ΔG^SP** (→ γ⁺/γ⁻ · K_A/K_B) 를 재며, 값은 **덮임률에 강하게 의존** (석영 γ_S^D 0.5 % ≈ 66 → 50 % ≈ 38 mJ/m² [판독]) 하므로 덮임률을 명시해 비교해야 한다 [인쇄 · 판독].
우리 논지에 대어 보면: 판가름 비 γ_A/γ_S (§2-3) 를 **분산 성분 (γ^D) 끼리** 재는 표준 도구이고, 코팅 전후 NCM 의 표면이 SE 처럼 바뀌었는지 (§2-5 의 γ_A,유효 = γ_S) 를 같은 기계로 볼 수 있다.  황화물에 대한 예는 리뷰에 없다 — 운반 기체가 건조한 점은 유리, 극성 탐침과 황화물의 반응성 · 미분말 압력 강하는 미확인 위험 [추정].

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ★ 무엇을 재나 | 원측정 = **머무름 시간 t_R → 순 머무름 부피 V_N** (식 1) · 열역학 = ΔG°_ad (식 4) → **γ_S^D** (n-알칸 · 식 8 Schultz / 식 15–16 Dorris–Gray) · **ΔG^SP** (극성 탐침의 알칸선 위 수직 거리 · 식 5) · **γ_S⁺ · γ_S⁻** (van Oss 꼴 식 20, 단극성 탐침 디클로로메탄 · 에틸 아세테이트) · **K_A · K_B** (Gutmann 식 23–24) · **불균일 분포** (덮임률별 γ^D) · W_co · W_adh · 흡착 엔탈피 · 엔트로피 · 비표면적 (유한 농도) | [인쇄] p.23–27 |
| 측정 조건 두 가지 | **무한 희석** (탐침 극미량 · Henry 법칙 · 대칭 피크 · 고에너지 자리만 · 검출 감도 ≈ 10⁻⁹ mol) — γ^D · 산염기 · 불균일 / **유한 농도** — 흡착 등온선 · 비표면적 · 에너지 분포 | [인쇄] p.23–24 |
| ★ 수치 예 (SEA 신규 자료) | Table 1 (5 % 덮임, 30 °C): **석영 52.76 (Schultz) / 52.61 (Dorris–Gray) · 탈크 59.16 / 59.88 · D-만니톨 32.79 / 33.53 mJ/m²** · 석영 ΔG^SP: DCM 11.05 · EtOAc 13.96 kJ/mol (Schultz) · 11.35 · 12.53 (분극법) · K_A 0.2119 · K_B 0.2874 (양쪽성) | [인쇄] p.25–27 · Table 1 |
| ★ 불확도 | 방법 간 (Schultz ↔ Dorris–Gray) 차는 Table 1 에서 ≤ 2.3 % · 문헌상 Dorris–Gray > Schultz 이고 온도와 함께 비가 커진다 (Shi 등) · **덮임률 의존 (불균일) 이 훨씬 크다** — 석영 0.5–50 % 에서 ≈ 66 → 38 mJ/m² [판독] (본문은 "31 ~ ≈60" — §10-1) | [인쇄] p.26 · [판독] Fig 8 |
| 시료 조건 | "no special sample preparation" · 칼럼 = 곧은 유리관 (스테인리스 · 구리 · 테플론도) · 분말 · 섬유 · 필름 (필름 셀) · 석영 시료는 분쇄 체거름 53–75 · 106–150 µm · **미분말은 칼럼 압력 강하 · 칼럼 안 응집으로 어렵다** (마그네슘 스테아레이트) · 극성 탐침이 비정질 분말 속으로 확산할 수 있다 | [인쇄] p.22–23 · 30 |
| 수분 · 표면 상태 | 고에너지 광물은 물을 흡착해 측정이 어렵다 · CaCO₃ 는 가열 탈수로 표면 에너지 증가 (IGC 가 단분자층 이하 물 탈착까지 추적) · 건조 운반 기체가 전분을 완전 탈수 (습도 조절 없음) · 미분화 유당은 75 % RH 3 개월 저장 뒤 분산 · 특이 · 총 에너지 감소 · 적철석 350 °C 이상 열처리 뒤 재수화 불가 · NiO · 세리아 수화 · 열처리 영향 | [인쇄] p.31–32 · 37–38 |
| ★ 건식 코팅 · 기계 처리 | 이부프로펜을 나노실리카로 **건식 코팅** → γ^D 감소 · 에너지 자리 균일화 · 응집 감소 · 흐름성 개선 · **알루미늄 분말 건식 코팅 (실리카 · 티타니아 · 카본블랙)** · 실란 처리 → γ^D 감소 · 흐름성 개선 · **메카노퓨전 (MgSt) 이 Turbula 혼합보다 표면 에너지를 더 낮춤** · 미분화 → γ^D 증가 · 흑연 분쇄 → 고에너지 자리 증가 | [인쇄] p.31 · 35 · 38 |
| 코팅된 이원계 해석 | 실리카 코팅 약물: *"the interpretation of IGC results for studying a binary sample's dispersive surface energy was complicated … The dispersive surface energy derived from contributions of both components on the surface"* | [인쇄] p.30 |
| 접착 · 응집 일 | 살부타몰 설페이트–MgSt 의 W_adh < 살부타몰 응집 W_co (응집 조절제) — *"Determining interactions between non-symmetrical particles using AFM was found to be difficult due to their variable contact surfaces; therefore, IGC was used to calculate the thermodynamic work of cohesion/adhesion"* | [인쇄] p.31 |
| 황화물 · 배터리 소재 | 황화 광물 **pyrite (FeS₂) · lithopone (ZnS + BaSO₄)** 이 연마 충전재로 측정된 예 [239] · 공기 민감 황화물 · NCM · 배터리 전극 분말 예는 **없다** | [인쇄] p.31–32 · [미확인] |

⛔ **한정어 (떼지 말 것)**: ① 리뷰 — 대부분 문헌 소개 · 정량 자료는 저자들의 SEA 측정 (석영 · 탈크 · 만니톨 · 아세테이트 필름) 뿐 ② γ^D 는 **덮임률 · 온도 · 계산법 · 탐침 단면적 a 값** 에 따라 달라진다 — 덮임률 없는 단일 숫자는 비교 불가 ③ 특이 성분 (γ⁺/γ⁻ · K_A/K_B) 은 탐침 기준값 · 척도 (Gutmann AN/DN · van Oss 기준) 에 묶인 상대값 ④ 공기 · 수분 민감 황화물의 IGC 측정 예 없음 ⑤ 본문 · 그림 수치 불일치 하나 · 식 부호 표기 문제 하나 (§10).

---

## 1. 한 줄 요약
IGC 는 일반 기체크로마토그래피의 역할을 뒤집어, **시험할 고체를 고정상으로 칼럼에 채우고** 성질을 아는 탐침 증기를 흘려 그 머무름으로 고체 표면의 열역학을 잰다 (1941 Martin · Synge → 1960 년대 Kiselev 명명 → 1970 년대 고분자 → 현재 의약 · 광물 · 나노 재료).
무한 희석에서 n-알칸 동족열의 RT ln V_N 직선 기울기로 분산 성분 γ_S^D (Schultz: a√γ_L^D 축 · Dorris–Gray: CH₂ 당 증분), 극성 탐침이 그 직선에서 벗어난 거리로 특이 자유에너지 ΔG^SP 를 얻고, 이것을 Gutmann (AN · DN) 또는 van Oss (γ⁺ · γ⁻) 틀로 산 · 염기 성질로 바꾼다.  탐침량을 늘리면 덮임률별 표면 에너지 분포 (불균일) 와 흡착 등온선 · 비표면적이 나온다.
저자들은 자신의 SEA (Surface Energy Analyser) 자료로 석영 · 탈크 · 만니톨의 두 방법 비교, 석영 불균일 분포, Gutmann 도표를 예시하고, 고분자 · 의약 (밀링 · 미분화 · 건식 코팅 · 메카노퓨전 · 저장 습도) · 광물 (실리카 · 점토 · 제올라이트) · 계면활성제 · 나노 탄소 · 필름 · 금속 산화물 · 알루미늄 분말 응용을 정리한다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| S. Mohammadi-Jam · **K. E. Waters\*** (McGill University, Mining and Materials Engineering) | Adv. Colloid Interface Sci. **212** (2014) 21–44 | 10.1016/j.cis.2014.07.002 | 리뷰 + SEA 자료 (석영 · 탈크 · D-만니톨 · 아세테이트 필름) | 리뷰 (방법 · 응용) |

| 원문 구조 | 쪽 | 내용 |
|---|---|---|
| 1. Introduction | 22 | 역사 · 측정 가능한 양 |
| 2.1 Instrumentation and methods | 22–24 | 장치 (Fig 1) · GC ↔ IGC (Fig 2) · 펄스 ↔ 전면 · 검출기 (TCD · FID) · 무한 희석 ↔ 유한 농도 |
| 2.2 Theory (2.2.1 분산 · 2.2.2 특이 · 2.2.3 산염기) | 24–27 | 식 (1)–(24) · Fig 3–9 · Table 1 |
| 3. Applications (고분자 · 의약 · 광물 (실리카 · 점토 · 제올라이트) · 계면활성제 · 나노 재료 · 평면 재료 · 기타) | 27–38 | Table 2–5 · Fig 10–11 |
| 4. Conclusions · References (336) | 38–44 | |

- 중복 확인 (2026-10-13): 정본 `litdb/papers/` 전수 목록에 IGC 카드 없음 · `git grep -i` "Inverse gas chromatography applications" · DOI 0 건 → 새 카드.

---

## 3. 핵심 식 · 수치 (★ 원문 그대로 — 크롭 `eq_*.png`)

### 3-1. 식 [인쇄 p.24–27]
| 식 | 원문 | 뜻 |
|---|---|---|
| (1) | V_N = j·F_c·(t_R − t₀) — j = James–Martin 압축성 보정 · F_c = 운반 기체 유량 | 순 머무름 부피 |
| (2) · (3) | V_g⁰ = (V_N/m_S)·(273.15/T) = (j/m_S)·F_c·(t_R − t₀)·273.15/T | 비 머무름 부피 (ml g⁻¹, 0 °C) |
| (4) | ΔG°_ad = ΔG°_de = R·T·ln V_N + C (⚠ 인쇄 그대로 — §10-2) | 표준 몰 흡착 자유에너지 |
| (5) | ΔG°_ad = ΔG_ad^D + ΔG_ad^SP | 분산 + 특이 |
| (6) · (7) | −ΔG°_ad = N_A·a·W_adh · **W_adh = 2√(γ_S^D·γ_L^D)** (Fowkes) | 탐침 단면적 a 의 접착 |
| (8) | **R·T·ln V_N = 2·N_A·a·√(γ_S^D)·√(γ_L^D) + C** — RT ln V_N vs a√γ_L^D 의 n-알칸 직선 기울기 → γ_S^D | ★ Schultz |
| (9)–(13) | ΔG_ad^CH2 = −R·T·ln[V_N(C_{n+1}H_{2n+4})/V_N(C_nH_{2n+2})] · W_CH2 = 2√(γ_S^D·γ_CH2) · −ΔG_CH2 = N_A·a_CH2·W_CH2 · γ_S^D = (1/4γ_CH2)·(−ΔG_CH2/(N·a_CH2))² | ★ Dorris–Gray (CH₂ 당 증분) |
| (14) | γ_CH2 = 35.6 + 0.058·(293 − T) (mJ/m²) | CH₂ 표면 에너지 |
| (15) · (16) | γ_S^D = [R·T·ln(V_N^{n+1}/V_N^n)]²/(4·N²·a_CH2²·γ_CH2) = slope²/(4·N²·a_CH2²·γ_CH2) (RT ln V_N vs 탄소 수 기울기) | |
| (17) · (18) | R·T·ln V_N + C = C′·P_DP·P_DS · P_D = [(n² − 1)/(n² + 2)]·(M/ρ) | 분극법 (변형 분극) |
| (19) | γ^D_DG/γ^D_Schultz = (a_{n+1}√γ_{n+1} − a_n√γ_n)²/(γ_CH2·a_CH2²) (Shi 등) | 두 방법의 비 |
| (20) · (21) | −ΔG = 2·N_A·a·(√(γ_S⁺γ_L⁻) + √(γ_S⁻γ_L⁺)) · γ_S^SP = 2√(γ_S⁺γ_S⁻) — 단극성 산 (CH₂Cl₂) · 염기 (에틸 아세테이트) 탐침 둘로 | ★ van Oss 꼴 (vanoss1988 카드) |
| (22)–(24) | −ΔH = AN·DN/100 · −ΔG = K_A·DN + K_B·AN · −ΔG/AN = K_A·(DN/AN) + K_B | ★ Gutmann (K_A 산 · K_B 염기) |

### 3-2. 수치 [인쇄 · 판독]
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 검출 감도 | ≈ 10⁻⁹ mol (무한 희석에 적합) | [인쇄] p.23 |
| 운반 기체 | 헬륨 · 아르곤 · 질소 (고순도 불활성) | [인쇄] p.22 |
| 검출기 | TCD (범용 · 물 검출) · FID (탄화수소 고감도 · 물 검출 불가) · 직렬 사용 예 | [인쇄] p.23 |
| Table 1 (30 °C · 5 % 덮임) | 석영 (53–75 µm) **52.76 / 52.61** · 탈크 (53–75 µm) **59.16 / 59.88** · D-만니톨 **32.79 / 33.53** mJ/m² (Schultz / Dorris–Gray) | [인쇄] p.26 |
| 크로마토그램 (Fig 3) | 석영 (106–150 µm) n-옥탄 크로마토그램 — 덮임률 n/n_m 0.0378 · 0.4716 · 0.7846 · 주입량이 클수록 Henry 법칙 · 대칭에서 벗어남 | [인쇄] p.24 |
| Schultz 도표 (Fig 4) | 석영 Schultz 도표 (헥산–데칸 알칸선 · 극성: 에탄올 · 에틸 아세테이트 · 아세토니트릴 · 아세톤 · DCM) — 판독 기울기로 γ_S^D ≈ **52.4** mJ/m² [우리 산술] (인쇄 52.76) | [판독] |
| ΔG^SP (석영 53–75 µm) | DCM **11.05** · 에틸 아세테이트 **13.96** kJ/mol (Schultz) · **11.35** · **12.53** kJ/mol (분극법) | [인쇄] p.25 · 26 |
| Dorris–Gray 도표 (Fig 6) | 탄소 수 6–10 — 판독 −ΔG_CH2 ≈ 3.13 kJ/mol → a_CH2 = 6 Å² (우리 가정 — 원문에 값 없음) 으로 γ_S^D ≈ 53.4 [우리 산술] (인쇄 52.61) | [판독] |
| ★ Fig 8 (석영 불균일, C6–C10, 0.5–50 %) | 0.6 % **66.5** · 1 % 62.2 · 2 % 57.9 · 5 % 52.2 · 10 % 48.0 · 20 % 43.7 · 30 % 41.2 · 40 % 39.3 · 50 % **38.0** mJ/m² | [판독] (본문 "31 ~ ≈60" — §10-1) |
| Gutmann 도표 (Fig 9, 석영) | K_A **0.2119** · K_B **0.2874** — "amphoteric" | [인쇄] p.27 |
| 물 접착일 (Fig 10) | 물과의 W_adh (방연석 · 석영) · 친수도 vs 덮임률 (0.05–0.38) — 둘 다 덮임률과 함께 감소 · 석영이 방연석보다 높다 · 부유 선광 회수율과 상관 (Ali 등 [243]) · ⚠ 캡션 (찬 기호 = W_adh · 빈 기호 = 친수도) 과 범례 · 축 색 (파란 계열 = 오른쪽 친수도 축) 이 어긋나 계열–축 대응이 모호 → **값 판독 안 함** | [인쇄 캡션] · [판독 — 추세만] |
| 필름 셀 (Fig 11) | 아세테이트 시트 γ^D (필름 셀, Schultz) ≈ 33 → 26 mJ/m² (덮임 0.015–0.22) [판독] | — |

---

## 4. ★ 방법 — 측정 사슬 · 입자 처리

### 4-1. 측정 사슬 (원문 §2)
분말 (또는 섬유 · 필름) 을 칼럼 (곧은 유리관) 에 충전 → 운반 기체 (He 등) 일정 유량 · 칼럼 온도 일정 → 탐침 (n-알칸 C6–C10 · 극성: DCM · 에틸 아세테이트 · 아세톤 · 아세토니트릴 · 에탄올) 을 펄스로 주입 (빠른 평형) 또는 전면 (느린 평형) → 검출 (FID · TCD) → t_R · t₀ → V_N (식 1) → 덮임률 (주입량) 별로 반복 → Schultz / Dorris–Gray 로 γ_S^D, 알칸선 거리로 ΔG^SP → K_A · K_B (Gutmann) 또는 γ⁺ · γ⁻ (van Oss) → 덮임률별 분포 (불균일 지도).

### 4-2. ★ 입자 처리
- **분말층 전체의 평균 표면** — 입자 하나하나가 아니라 칼럼 속 모든 표면 자리가 탐침과 평형.  무한 희석에서는 **가장 센 자리** 가 먼저 (그래서 저덮임 γ^D 가 크다), 덮임률을 올리면 약한 자리까지.
- **접촉 기하 없음** — 탐침 분자와 표면의 상호작용 에너지 → 표면 에너지 (면적당) — 입자–입자 떼는 힘 (AFM, begat2004 카드) 과 달리 곡률 · 거칠기 · 접촉 면적이 직접 들어가지 않는다 (리뷰가 AFM 대신 IGC 를 쓴 이유로 드는 점, p.31).
- 이원계 (코팅된 분말) 는 두 성분의 표면 기여가 섞인 값 — "availability and surface energy heterogeneity" 에 달림 (p.30).

### 4-3. 기법 미니 용어집
- **무한 희석 (zero coverage)**: 탐침 극미량 · 탐침–탐침 상호작용 없음 · Henry 직선 등온선 · 대칭 피크.
- **유한 농도**: 많은 탐침 · 모든 자리 · 등온선 · 비표면적 · 에너지 분포.
- **알칸선 (alkane line)**: n-알칸 동족열의 RT ln V_N 직선 — 기울기 = 분산 상호작용.
- **ΔG^SP**: 극성 탐침이 알칸선에서 벗어난 거리 = 특이 (산 · 염기) 흡착 자유에너지.
- **Gutmann AN · DN**: 탐침의 받개 · 주개 수 → 고체의 K_A (산) · K_B (염기).
- **표면 에너지 불균일 (heterogeneity)**: γ^D (또는 ΔG^SP) vs 덮임률 곡선.
- **SEA**: Surface Measurement Systems 사의 상용 IGC (Surface Energy Analyser) — 이 리뷰의 신규 자료 장비.

---

## 5. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | IGC 장치 모식 (운반 기체원 · 질량 유량 제어기 · 탐침 저장조 · 유로 전환 · 오븐 속 시료 칼럼 · FID · 처리기) | 측정 구성 — 글로브박스 충전 칼럼이 들어갈 자리 [추정] |
| 2 | GC (긴 코일 칼럼 · 혼합물 분리) ↔ IGC (짧은 충전 칼럼 · 한 탐침 피크) | 개념 |
| 3 | 석영 n-옥탄 크로마토그램 — 덮임률 0.04 · 0.47 · 0.78 · 큰 주입일수록 비대칭 | 무한 희석 판정 |
| 4 | ★ 석영 Schultz 도표 — 알칸선 + 극성 탐침 5 종 | γ_S^D · ΔG^SP 읽는 법 |
| 5 | Schultz 법 ΔG^SP 개념도 | |
| 6 | 석영 Dorris–Gray 도표 (탄소 수) | 방법 비교 |
| 7 | 분극법 ΔG^SP 개념도 (P_D 축) | |
| 8 | ★ 석영 γ^D 불균일 분포 (0.5–50 %) — 66 → 38 mJ/m² [판독] | 덮임률 명시의 근거 |
| 9 | 석영 Gutmann 도표 (ΔG/AN vs DN/AN) — K_A 0.2119 · K_B 0.2874 | 산 · 염기 |
| 10 | 물–방연석 · 물–석영 W_adh · 친수도 vs 덮임률 (재수록 — 출처 번호 §10-6) | 덮임률별 접착일 |
| 11 | 아세테이트 시트 γ^D (필름 셀) vs 덮임률 | 평면 시료 |
| Table 1 | Schultz ↔ Dorris–Gray (석영 · 탈크 · D-만니톨) | ★ 방법 차 크기 |
| Table 2 | 고분자 · 공중합체 · 블렌드 — IGC 로 잰 물성 목록 (두 쪽) | 목록 |
| Table 3 | 의약 물질 — γ^D · ΔG^SP · K_A/K_B · W_co · W_adh · 불균일 … | 분말 응용 목록 |
| Table 4 · Table 5 | 점토 · 계면활성제 | 목록 |
| 식 크롭 | `eq_01_05_retention_free_energy.png` · `eq_05_08_free_energy_fowkes.png` · `eq_09_15_dorris_gray.png` · `eq_16_19_polarization_comparison.png` · `eq_20_24_vanoss_gutmann.png` | 식 원문 |

## 6. Post-processing ★
- **원문**: 머무름 → V_N → 직선 맞춤 (Schultz · Dorris–Gray · 분극) → 덮임률별 반복 → 분포 · Gutmann 직선 · van Oss 두 탐침.
- **안 한 것 (리뷰가 적지 않음)**: 반복 측정 산포 · 칼럼 충전 밀도 · 시료 질량 · 사전 처리 온도 · 시간 (SEA 자료의 조건 상세 [미확인]).
- **이 카드에서 한 것**: Fig 8 점 17 개 판독 · Fig 4 · 6 · 9 기울기로 인쇄 숫자 검산 (`digitized.csv`).

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 쪽 수치는 리포 출처를 병기)

### 7-1. ★ 논지 §2-8 측정 설계 — IGC 로 무엇을 정할 수 있나 [추정]
| 논지의 양 | IGC 로 | 비고 |
|---|---|---|
| γ_A/γ_S 의 **분산 부분** (γ_NCM^D/γ_SE^D) | ★ 직접 — 같은 기계 · 같은 덮임률 · 같은 온도로 두 분말 | 기하평균 결합 규칙이 성립하는 성분 (fowkes1964 · vanoss1988 카드) |
| AM–SE 극성 교차항 | γ⁺ · γ⁻ (식 20) 로 W_AS^AB = 2(√(γ_A⁺γ_S⁻) + √(γ_A⁻γ_S⁺)) 계산 | 탐침 기준값에 묶인 상대 척도 · 탐침–황화물 반응성 [미확인] |
| 코팅 효과 (§2-5: γ_A,유효 → γ_S) | 코팅 전 · 후 NCM γ^D · 불균일 분포 비교 — 리뷰의 실리카 코팅 약물 · 알루미늄 건식 코팅 예와 같은 문법 | 이원계는 두 성분 기여가 섞인다 (p.30) — 피복률이 높을수록 SE 쪽에 가까워질 것 [추정] |
| W_co · W_adh | W = 2√(γ_i^Dγ_j^D) + 극성항 → JKR 대응식 CED_ij (`johnson1971_jkr_surface_energy_contact_elastic_solids` §7-1) | 접촉 기하 · 곡률은 IGC 밖 — CAB (AFM, `begat2004_cohesive_adhesive_balance_afm_colloid_probe`) 와 상보 |

### 7-2. ★ 공기 · 수분 민감 황화물 (LPSCl) 에 쓸 수 있나 [추정 — 리뷰에 직접 예 없음]
- **유리한 점**: 측정 매질이 **건조 고순도 불활성 기체** (He · Ar · N₂) 이고 액체 접촉이 없다 (리뷰 p.22 · 23).  리뷰의 "건조 운반 기체가 전분을 완전 탈수" 는 우리에게는 오히려 조건 통제 (드라이룸 분말 상태 유지) 다.  황화 광물 (FeS₂ · ZnS) 측정 선례가 있다 [인쇄 p.31–32].
- **위험**: ① **극성 탐침의 반응** — 황화물 SE 는 수분과 반응해 H₂S 를 내고, 극성 유기 탐침 (에탄올 · 아세톤 · 아세토니트릴 · 에틸 아세테이트 · DCM) 과의 반응성은 이 리뷰 밖 [미확인] → n-알칸 (γ^D) 부터, 극성 탐침은 별도 안정성 시험 뒤. ② **칼럼 충전 · 이송** — 글로브박스에서 칼럼을 채우고 밀봉해 옮겨야 한다 (리뷰에 절차 없음). ③ **미분말 압력 강하 · 칼럼 속 응집** — 리뷰가 MgSt 에서 지적 (p.30) · LPSCl ≈ 1 µm [추정 위험]. ④ **사전 처리 온도** — 물 제거용 가열이 황화물 · NCM 표면 (잔류 리튬염) 을 바꿀 수 있다 (적철석 350 °C · NiO · 세리아 사례가 표면 재구성을 보임, p.37–38).
- NCM 쪽: 금속 산화물 (적철석 · NiO · ZnO · 세리아 · Cr₂O₃) 측정 선례 — 수화 · 열처리 이력이 γ^D · 불균일을 크게 바꾼다 (p.37–38) → **NCM 시료의 저장 · 건조 이력 기록이 필수**.

### 7-3. 값의 자리 — 정본 카드 값과 대조 [우리 산술 · 추정]
- 석영 γ_S^D ≈ 52 mJ/m² (5 %) · 38–66 (분포) — Fowkes 1964 의 산화물 분말 (π_e 기반, 탈기) 80–150 mJ/m² 보다 낮다 (`fowkes1964_attractive_forces_interfaces_dispersion` §7-2) — 측정법 · 표면 상태 (공기 중 분말 ↔ 탈기) 차이로 보인다 [추정].  ⇒ NCM · LPSCl 의 비는 **같은 IGC 조건**에서만 뜻이 있다.
- 우리 덱 parcel 규모 W (6×10⁻⁶ J/m², johnson1971 카드) 는 실입자 W 가 아니다 — IGC 값을 덱에 넣으려면 CG 규칙 결정 (논지 §2-6 · 브리핑 §1-4) 이 먼저다.

### 7-4. 혼합 공정 해석에 주는 것
- 메카노퓨전이 표면 에너지를 Turbula 혼합보다 크게 낮추고 흐름성 · 분산성이 좋아졌다 (MgSt–유당, p.31) · 나노실리카 건식 코팅이 γ^D 와 응집을 낮춘다 — **건식 코팅 → 표면 에너지 변화 → 응집 감소** 사슬의 의약 분말 실례 (우리 논지 §2-5 와 같은 방향의 사례이나, 그 기전은 "코팅 물질 표면이 되는 것" 이고 SE 선코팅과 소재가 다르다).

### 7-5. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 분말 표면 에너지 (분산 · 특이 · 분포) 측정 — 쌍별 점착 입력 (D2) 의 실험 앵커 후보 · 코팅 전후 비교 도구.
- **없는 것**: 입자 접촉 역학 · 혼합 · 압밀 · 수송.  배터리 소재 측정 예.

---

## 8. 적용 인사이트 (내 연구에 어떻게)
1. **판가름 비의 분산 부분은 IGC 로 직접** — NCM · LPSCl 의 γ^D 를 같은 덮임률 · 온도에서 (Schultz · Dorris–Gray 둘 다 보고).
2. **덮임률을 늘 적는다** — 석영만 해도 0.5–50 % 에서 66 → 38 mJ/m².  "γ_A/γ_S" 는 분포 대 분포로 비교.
3. **황화물은 n-알칸부터** — 극성 탐침 반응성 · 칼럼 충전 (글로브박스) · 미분말 압력 강하를 먼저 시험.
4. **코팅 전후** — 실리카 코팅 · 메카노퓨전 사례처럼 코팅 NCM 의 γ^D · 분포가 SE 쪽으로 움직이는지가 §2-5 의 직접 검증 (이원계 해석 주의).
5. **IGC ↔ AFM CAB 상보** — IGC = 면적당 에너지 (기하 없음) · AFM = 같은 탐침의 힘 비 (기하 약분) — 둘이 같은 방향을 주면 판가름이 단단해진다.

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Inverse gas chromatography determines the dispersive surface energy γ_S^D of powders from the retention of n-alkane probes at infinite dilution (Schultz or Dorris–Gray methods) and their specific (acid–base) interactions from polar probes, without wetting the solid (Mohammadi-Jam & Waters, Adv. Colloid Interface Sci. 2014)."
- "For quartz (53–75 µm) the two methods gave 52.76 and 52.61 mJ m⁻² at 5 % surface coverage, whereas γ_S^D varied from about 66 to 38 mJ m⁻² between 0.5 % and 50 % coverage (read from their Fig. 8), so reported values must specify coverage."
- 국문: *"IGC 는 분말을 적시지 않고 건조 불활성 기체 속에서 분산 표면 에너지를 잰다 — 석영도 덮임률 0.5–50 % 에서 66 → 38 mJ/m² 로 바뀌므로 NCM · 황화물 SE 의 비는 같은 덮임률에서만 비교한다."*

## 10. 주의/한계 (over-claim 방지 · 원문 비판)
1. ★ **본문 ↔ 그림 불일치**: 본문 (p.26) *"ranging from 31 mJ m⁻² to approximately 60 mJ m⁻²"* ↔ Fig 8 판독 **38.0–66.5 mJ/m²** (원 래스터 눈금 보정, ±0.2) — 5 % 점 52.2 는 Table 1 (52.76) 과 맞으므로 그림 쪽이 일관 [판독 + 우리 산술].
2. **식 (4) 부호 표기**: "ΔG°_ad = ΔG°_de = R·T·ln V_N + C" — 식 (6) (−ΔG°_ad = N_A a W_adh > 0) · 식 (8) (RT ln V_N = 2N_A a√… + C) 와 맞으려면 ΔG°_ad = −RT ln V_N + C (그리고 ΔG°_de = −ΔG°_ad) 여야 한다 [추정 — 표기 문제 · 결과식 (8) 은 맞다].
3. **a (탐침 단면적) · a_CH2 값이 리뷰에 없다** — Schultz 값은 a 선택에 민감하다 [추정] · Dorris–Gray 검산에 우리는 6 Å² 를 가정했다.
4. **SEA 자료 조건 미기재** — 시료 질량 · 칼럼 크기 · 유량 · 사전 처리 · 반복 수 [미확인] · Table 1 의 온도 30 °C 는 본문 문장에서만.
5. **Dorris–Gray ↔ Schultz 의 우열** 은 인용 문헌끼리 엇갈린다 (Shi: DG 가 더 크고 온도와 함께 비 증가 · "DG 가 더 정확" · 차이 없음) — 이 리뷰의 Table 1 은 ≤ 2.3 % 차.
6. **Fig 10 출처 번호 불일치** — 캡션은 "[233] … Reproduced with permission" ([233] = Keller & Luner, 탄산칼슘) 인데 본문 (p.32) 은 방연석 · 석영 부유 선광 자료를 Ali 등 [243] 으로 든다 — 캡션 번호 오기로 보인다 [추정] · 축 판독은 추세 전용.
7. **배터리 · 공기 민감 황화물 예 없음** — §7-2 는 전부 우리 추정.

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유)
| 번호 | 서지 (원문 목록 그대로 — 텍스트층) | 왜 |
|---|---|---|
| 49 | Jallo LJ, Chen Y, Bowen J, Etzler F, Dave R. Prediction of inter-particle adhesion force from surface energy and surface roughness. J Adhes Sci Technol 2011;25:367–84. | ★ IGC 표면 에너지 + 거칠기 → 입자 간 접착력 |
| 81 | Schultz J, Lavielle L, Martin C. The role of the interface in carbon fibre-epoxy composites. J Adhes 1987;23:45–60. | Schultz 법 원전 |
| 82 | Schultz J, Lavielle L. Interfacial properties of carbon fiber-epoxy matrix composites. Inverse gas chromatography characterisation of polymers and other materials, ACS Symposium Ser. vol. 391: ACS Publications; 1989. p. 185–202. | Schultz 법 |
| 87 | Dorris GM, Gray DG. Adsorption of n-alkanes at zero surface coverage on cellulose paper and wood fibers. J Colloid Interface Sci 1980;77:353–62. | Dorris–Gray 법 원전 |
| 89 | Gamble JF, Leane M, Olusanmi D, Tobyn M, Šupuk E, Khoo J, et al. Surface energy analysis as a tool to probe the surface energy characteristics of micronized materials—A comparison with inverse gas chromatography. Int J Pharm 2011;422:238–44. | 미분화 · 단극성 탐침 |
| 92 | Gamble JF, Davé RN, Kiang S, Leane MM, Tobyn M, Wang SS. Investigating the applicability of inverse gas chromatography to binary powdered systems: an application of surface heterogeneity profiles to understanding preferential probe–surface interactions. Int J Pharm 2013;445:39–46. | ★ 코팅 (이원계) 분말 해석 |
| 189 | Tay T, Das S, Stewart P. Magnesium stearate increases salbutamol sulphate dispersion: what is the mechanism? Int J Pharm 2010;383:62–9. | IGC W_adh · W_co |
| 194 | Das SC, Stewart PJ. Characterising surface energy of pharmaceutical powders by inverse gas chromatography at finite dilution. J Pharm Pharmacol 2012;64:1337–48. | ★ 메카노퓨전 · 75 % RH · 분포 |
| 205 | Zhou QT, Denman JA, Gengenbach T, Das S, Qu L, Zhang H, et al. Characterization of the surface properties of a model pharmaceutical fine powder modified with a pharmaceutical lubricant to improve flow via a mechanical dry coating approach. J Pharm Sci 2011;100:3421–30. | ★ 기계적 건식 코팅 → 표면 · 흐름 |
| 239 | Voelkel A, Strzemiecka B. Characterization of fillers used in abrasive articles by means of inverse gas chromatography and principal component analysis. Int J Adhes Adhes 2007;27:188–94. | 황화 광물 (FeS₂ · ZnS) 선례 |
| 243 | Ali S, Heng J, Nikolaev A, Waters K. Introducing inverse gas chromatography as a method of determining the surface heterogeneity of minerals for flotation. Powder Technol 2013;249:373–7. | Fig 10 의 본문 출처 (캡션은 [233] — §10-6) |
| 334 | Chen Y, Jallo L, Quintanilla MA, Dave R. Characterization of particle and bulk level cohesion reduction of surface modified fine aluminum powders. Colloids Surf A Physicochem Eng Asp 2010;361:66–80. | ★ 건식 코팅 → 응집 감소 (입자 · 벌크) |
| 335 | Jallo LJ, Schoenitz M, Dreizin EL, Dave RN, Johnson CE. The effect of surface modification of aluminum powder on its flowability, combustion and reactivity. Powder Technol 2010;204:63–70. | 건식 코팅 (실리카 · 티타니아 · 카본블랙) |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-13)
- 24 쪽 텍스트층 전부와 그림 · 표 · 식 쪽 이미지 (300 dpi 크롭) 를 읽었다 · DOI = p.21 인쇄.
- 식 (1)–(24) 는 크롭 이미지로 확인 (텍스트층의 근호 · 위첨자 깨짐) · Fig 8 은 PDF 원 래스터 (200 ppi) 에서 눈금 보정 판독.
- 크롭 23 장 = Fig 1–11 · Table 1 · 2 (두 쪽) · 3 · 4 · 5 · 식 영역 5 — 전부 손 크롭 (자동 추출은 Fig 4 · 7 · 11 누락 · Fig 6 · 7 을 한 장으로 · 표를 쪽 전체로 잡음).  표 2 · 3 은 220 dpi (쪽 폭 표).
- 참고문헌 행은 텍스트층에서 옮겼다 (쪽 이미지 대조는 하지 않음).
- 정본 litdb 중복 확인: 파일 목록 + 제목 · DOI `git grep` 0 건.

## 🔗 관련 카드
- 같은 묶음: `fowkes1964_attractive_forces_interfaces_dispersion` (식 7 의 원전) · `vanoss1988_lifshitz_vdw_acid_base_interfacial` (식 20–21 의 원전) · `begat2004_cohesive_adhesive_balance_afm_colloid_probe` (AFM CAB) · `johnson1971_jkr_surface_energy_contact_elastic_solids` · `garcia2017_nmc111_surface_energy_wulff_dft`.
- 건식 혼합 · 코팅: `hare2026_dem_pept_dry_mixing_nmc622_eirich` · `lee2026_mechanical_halogen_argyrodite_drycoating`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
