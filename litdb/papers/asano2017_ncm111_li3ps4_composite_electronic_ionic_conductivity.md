<!-- digest 표준 양식 확장 (paper-level STANDALONE).  ★ = 사용자가 특히 원한 항목.  깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     τ 묶음 형식 기준 = tjaden2018_tortuosity_review_calculation_approaches.md · landesfeind2016_tortuosity_eis_electrodes_separators.md ·
     같은 날 앞 묶음 (kaiser2018_… · siroma2015_… · hlushkou2018_… 등 10 장).
     이 논문은 실험 (DC 분극 + AC 임피던스) 논문이다 — 시뮬레이션이 없다.  그래서 §4 '방법' 을 측정 사슬 (셀 → 저항 → 전도도 → "tortuosity") 로 쓴다.
     쪽 표기: 본문 = 인쇄 (학술지) 쪽.  PDF n 쪽 = 인쇄 p.A(3958 + n)  (PDF 1 = IOP 표지 · 인쇄 쪽 없음 / PDF 2 = A3960 … PDF 5 = A3963).
     식 번호는 원문에 없다 (번호 붙은 식 0 개).  표 = Table I · II, 그림 = Fig. 1–5 (원문 번호).  SI 파일 없음 — 본문도 SI 를 인용하지 않는다.
     값 표지: stated = 본문 · 캡션 · 표 원문 / 판독 = 그림에서 읽은 값 (≈ · 추세 전용, 정밀 인용 불가) / 파생 = 카드 작성자 계산 (식 명시). -->
# NMC111–Li₃PS₄ 유리 복합 양극의 전자 · 이온 전도도 — DC 분극 (이온 차단 / 전자 차단 대칭셀) vs AC 임피던스 (TLM 물방울) · NMC 48 / 55 / 62 vol% · SOC 0 → 50 % 에서 σ_e 26–45 배 · 식 없는 "tortuosity 4–6" — Asano (J. Electrochem. Soc. 2017)

> slug `asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity` · DOI `10.1149/2.1501714jes` · type `exp (DC 분극 · AC 임피던스 TLM — 이온 차단 · 전자 차단 대칭셀; 황화물 ASSB 복합 양극 σ_e · σ_ion · SOC 0/50 %)` · PDF `23. Electronic and Ionic Conductivities of LiNi13Mn13Co13O2-Li3PS4 Positive Composite Electrodes for All-Solid-State Lithium Batteries.pdf` · digested `2026-10-03` · status ✅
>
> ★ **정의 판정 (이 카드의 목적)** — 원문은 τ 에 **기호도 식도 주지 않는다**.  한 문단 (p.A3963) 에서 *"Effective ionic and electronic conductivities are theoretically described using volume ratio and tortuosity"* 라 쓰고
> 그 값을 *"in the range of 4 to 6"* 이라고만 적는다 (인용 [12] = Patel 2003).  원문 값만으로 후보 꼴을 다시 계산하면 **φ·σ₀/σ_eff (= 우리 `tau2` 꼴) 만 4–6 자릿수**를 낸다
> (√ 꼴 1.8–2.8 · MacMullin σ₀/σ_eff 6–20 · Bruggeman φ^−½ 1.4–1.6 — §3-5, 파생).  ⇒ **원문 낱말 "tortuosity" = tortuosity factor 꼴 (재구성 · 원문 식 없음)**.
> 단 정확한 입력은 재현되지 않는다: σ₀ 를 본문값 4×10⁻⁴ S/cm, φ_SE 를 1 − (NMC vol%) 로 두면 **4.2 / 5.8 / 6.9** (62 % 가 "6" 을 넘는다), Fig. 4a 의 순수 SE 점 (판독 ≈3.5×10⁻⁴) 을 쓰면 3.6 / 5.0 / 6.0.
> **기공률 · vol% 의 기준 (고체 / 전체) 이 원문에 없다** → 원문 값만으로 정해지는 것은 **f = σ_eff/σ₀** 이고, tau2 는 **상한** (φ_SE ≤ 1 − x) 으로만 정해진다.
>
> 형제 카드: `minnmann2021_jes_charge_transport_bottlenecks` (이 논문을 [27] 로 인용 — NCM622 + LPSCl 의 같은 측정 축) · `kaiser2018_ion_transport_limitations_assb_sulfide_electrodes` (황화물 유리 SE 복합 전극 τ_eff · TLM ↔ DC) ·
> `siroma2015_transmission_line_model_porous_electrode_impedance` (TLM 연결형 분류 — 이 논문의 AC 극한은 그 표 3 T형 open–open 꼴) · `sakuda2013_sulfide_mechanical_property` (= 이 논문 [13], 같은 그룹 · 같은 75Li₂S·25P₂S₅ 유리의 성형성 · 냉간 펠릿 σ) ·
> `tjaden2018_tortuosity_review_calculation_approaches` (명명 정본).  역링크: `hlushkou2018_void_space_ion_transport_assb_cathode` ([20]) · `cronau2022_wet_milling_particle_size_ionic_conductivity` ([22]).

---

## 0. 결론 먼저 (정의 판정 + 핵심 수치)

| 질문 | 답 | 근거 (쪽) |
|---|---|---|
| τ 를 쓰는가 · 어떤 양인가 | **낱말 "tortuosity" 만** — 기호 · 식 · 정규화 없음.  *"a parameter which accounts for nonuniformity of solid electrolytes in the composite [12]"*.  값 4–6 은 **tortuosity factor (τ²) 꼴로만 재현** (재구성) | p.A3963 · §3-5 |
| σ₀ 기준 | *"The SE exhibits Li⁺ conductivities of 4 × 10⁻⁴ S cm⁻¹ at 25°C"* — **측정 셀 · 압밀 · 밀도 미기재**.  Fig. 4a 의 NMC 0 vol% 점 = 판독 **≈3.5×10⁻⁴** (같은 그림의 표 값은 ≤3 % 로 재현되는데 이 점만 본문값과 ≈14 % 다르다).  같은 그룹 [13] 의 같은 유리 냉간 펠릿 (360 MPa) 은 3.1×10⁻⁴ (sakuda2013 카드) | p.A3960 · Fig. 4a (p.A3962) |
| φ (부피분율) 기준 | **"NMC volume ratios of 48%, 55% and 62%"** 뿐 — 고체 기준인지 전체 (기공 포함) 기준인지 · 환산 밀도 · 기공률 **모두 미기재**.  셀 치수 (48 vol%: L 0.032 / 0.034 cm, A 0.816 / 0.843 cm²) 는 있으나 시료 질량이 없어 밀도를 못 낸다 | p.A3960 · Fig. 2 캡션 (p.A3961) |
| 측정법 | **DC 분극** — 전자: 이온 차단 SS/시료/SS · 이온: 전자 차단 SS/Li-In/SE/시료/SE/Li-In/SS (SE 층 저항을 빼서) · 50 mV · 25 °C.  **AC 임피던스** — 이온 차단 SS/시료/SS 하나로 둘 다 (Siroma 2016 TLM 물방울: 고주파 끝 r_ion·r_e·L/(r_ion + r_e) · 저주파 끝 r_e·L) · 1 MHz–1 mHz · 10 mV | Fig. 1 (p.A3960) · p.A3961 · Fig. 3 |
| 두 측정법의 경계조건 | DC 이온 = **관통형 (conventional)** · AC = Siroma 2015 표 3 **T형 open–open** 극한 꼴 (단자 레일 = 전자) — 역시 관통형 부류.  **de Levie R/3 (τ_e 계열) 이 아니다** → 두 방법의 일치는 τ_e ↔ conventional 비교가 **아니다** | §4 · siroma2015 카드 |
| SOC 0 % 값 (Table I) | σ_ion,eff **5.0 / 3.1 / 2.2 ×10⁻⁵** (DC) · 5.0 / 2.6 / 2.0 ×10⁻⁵ (AC) · σ_e,eff **2.0 / 2.7 / 6.7 ×10⁻⁶** (DC) · 1.9 / 2.8 / 6.4 ×10⁻⁶ (AC) S cm⁻¹ — NMC 48 / 55 / 62 vol% | Table I (p.A3962) |
| DC ↔ AC 차 | 원문 *"at most 5% and 20%"* (전자 · 이온).  파생: 이온 0 / 19 / 10 % (AC 가 같거나 낮다) · 전자 5 / 4 / 4.5 % | p.A3961 · Table I |
| SOC 50 % (Table II, DC) | σ_e **5.2×10⁻⁵ / 9.3×10⁻⁵ / 3.0×10⁻⁴** (SOC 0 대비 **×26 / ×34 / ×45**, 파생) · σ_ion 5.2 / 3.0 / 2.1 ×10⁻⁵ (거의 불변 ×1.04 / ×0.97 / ×0.95) → σ_e ≥ σ_ion | Table II (p.A3962) |
| f = σ_eff/σ₀ (φ 불필요) | 0.125 / 0.078 / 0.055 (DC, σ₀ 4.0×10⁻⁴) · 0.145 / 0.090 / 0.064 (σ₀ 3.5×10⁻⁴) — 파생 | §3-5 |
| tau2 (상한, φ = 1 − x) | **4.2 / 5.8 / 6.9** (DC, σ₀ 4.0) · 3.6 / 5.0 / 6.0 (σ₀ 3.5) · AC 는 4.2 / 6.9 / 7.6 — 파생.  기공 p 를 넣으면 (1 − p) 배 | §3-5 |
| 퍼콜레이션 문턱 | **다루지 않는다** — 세 점 (48–62 %) 뿐.  σ_e 는 55 → 62 % 에서 ×2.5 로 가팔라지고 σ_ion 은 ÷1.6 → ÷1.4 로 완만 (붕괴 없음) — 파생 | Table I |
| 셀 성능 | 0.13 mA cm⁻²: 140–150 mAh g⁻¹ (stated, 조성 차 작음) · 1.3 mA cm⁻²: 판독 ≈92 / 70 / 67 — NMC 가 늘수록 감소 → 원문 *"ionic conductivity of the composite limits the rate performance"* | p.A3962 · Fig. 5 |
| 결정 4 뒤 §3-3 절대 대조점? | **아니오 (그대로는)** — 기공률 · vol% 기준 · SE 입경 미보고 · SE = **Li₃PS₄ 유리** (σ₀ 0.4 mS cm⁻¹) ≠ LPSCl.  쓰임: f (자기 순수 SE 기준) 추세점 · 실험 기준선 자체의 산포 증거 · 전자 σ 의 SOC 의존 (§8) | §8-1 |

## 1. 한 줄 요약
**LiNbO₃ 코팅 NMC111 (≈5 µm) + 75Li₂S·25P₂S₅ 유리 (Li₃PS₄) SE** 복합 양극 세 조성 (NMC 48 / 55 / 62 vol%) 의 **전자 · 이온 유효 전도도**를 (i) 이온 차단 · 전자 차단 대칭셀의 **DC 분극**과 (ii) 이온 차단 셀 하나의 **AC 임피던스 (전송선 모델 물방울)** 로 재서
두 방법이 전자 ≤5 % · 이온 ≤20 % 안에서 일치함을 보이고, **충전 (SOC 50 %, Li₂/₃) 뒤 σ_e 가 26–45 배 올라 σ_ion 이상**이 된다는 것, 그리고 1.3 mA cm⁻² 에서 용량이 NMC 증가와 함께 떨어지므로 **율속은 이온 전도**라는 결론을 낸다.
"tortuosity 4–6" 은 식 없이 한 줄로 나온다.  우리에게는 **Minnmann 2021 과 같은 측정 축 (CAM 적재 ↔ σ_ion · σ_e) 의 두 번째 실험** — 단 재료 (유리 SE) · φ 장부 (기공 미보고) 가 달라 **f 로만 맞댈 수 있고**, 맞대 보면 고체 기준 같은 NMC 분율에서 f 가 **1.2–2.8 배** 갈린다 (실험 기준선 자체가 하나가 아니다) — 그리고 **전자 T 는 SOC 를 메타로 달아야 한다**는 실측 근거다.

## 2. 메타

| 저자 | 저널/년 | DOI | 재료계 | 연구유형 |
|---|---|---|---|---|
| **Takamasa Asano**, So Yubuchi, **Atsushi Sakuda**, Akitoshi Hayashi, **Masahiro Tatsumisago** (교신) — Department of Applied Chemistry, Graduate School of Engineering, **Osaka Prefecture University** (Sakai, Osaka) | **J. Electrochem. Soc. 164 (14) A3960–A3963 (2017)** | **10.1149/2.1501714jes** | AM **LiNi₁/₃Mn₁/₃Co₁/₃O₂ (NMC111)**, 평균 ≈5 µm, **LiNbO₃ 코팅** · SE **75Li₂S·25P₂S₅ (mol%) 유리 = Li₃PS₄ 유리** (자체 볼밀 합성 → 헵탄 + 디부틸에테르 습식 분쇄) · 도전재 · 바인더 없음 | **실험** (DC 분극 · AC 임피던스 · 셀 시험) — 시뮬레이션 없음 |

- 투고 2017-09-25 · 수정본 2017-12-11 · 출판 2017-12-30 (p.A3960).  © 2017 The Electrochemical Society — 오픈 액세스 표기 없음 (PDF 머리말에 권리 유보 문구).
- 원문 제목 (아래첨자 그대로): *Electronic and Ionic Conductivities of LiNi₁/₃Mn₁/₃Co₁/₃O₂-Li₃PS₄ Positive Composite Electrodes for All-Solid-State Lithium Batteries*.  인쇄 4 쪽 (A3960–A3963) · 참고문헌 13 편 · 그림 5 · 표 2.
- 같은 그룹 (Osaka Prefecture Univ. Hayashi · Tatsumisago) 의 [13] Sakuda 2013 (정본 카드 `sakuda2013_sulfide_mechanical_property`) 이 같은 유리의 상온 성형성 · 냉간 펠릿 σ 를 준다 — 이 논문은 낮은 tortuosity 의 이유로 그것을 든다 (p.A3963).
- 서론의 동기 (p.A3960): *"there have often been a trade-off relationship between rate performance and active material ratio … This is likely to be caused by insufficient ionic conducting pathways rather than electronic conducting pathways in the composite. However, the details of the rate limiting factor have been unclear."*

## 3. 핵심 수치 (★ 전부 원문 쪽 · 표지 병기)

### 3-1. 재료 · σ₀ · 조성 · 공정 (p.A3960–A3961)

| 항목 | 값 | 표지 | 비고 |
|---|---|---|---|
| SE 조성 | 75Li₂S·25P₂S₅ (mol%) **유리** | stated | 원문 다른 자리 표기 "Li₃PS₄ glass" · 결론 "Li₃PS₄ (SE)" |
| SE 합성 | Li₂S (Idemitsu Kosan, 99 %) + P₂S₅ (Aldrich, 99 %) · 유성 볼밀 Pulverisette 5 (Fritsch) · **210 rpm · 45 h** · ZrO₂ 용기 250 mL · ZrO₂ 볼 400 g (⌀ 4 mm) [4] | stated | — |
| SE 분쇄 | *"pulverizing the as-prepared SE in heptane and dibutyl ether using small zirconia balls (200 g, 2 mm in diameter)"* [5 = WO 특허] | stated | **분쇄 뒤 입경 미보고** (PSD 없음) |
| **σ₀ (순수 SE)** | **4 × 10⁻⁴ S cm⁻¹ @ 25 °C** | stated (1 유효숫자) | 측정 셀 · 펠릿 압력 · 밀도 · 분쇄 전/후 여부 **미기재** |
| σ₀ (Fig. 4a 의 NMC 0 vol% 점) | **≈3.5×10⁻⁴ S cm⁻¹** | 판독 (3.46) | DC 실선에 이어 그려져 있다 · 측정법 본문 미기재 |
| σ₀ 참고 (같은 그룹 [13], 다른 논문) | 냉간 360 MPa 펠릿 3.1×10⁻⁴ · 열간 프레스 3.4×10⁻⁴ S cm⁻¹ · 상대밀도 > 90 % @ > 350 MPa | sakuda2013 카드 (stated) | 같은 조성 · 다른 시료 — 이 논문의 σ₀ 가 아니다 |
| AM | NMC111 [6, 7] · **평균 ≈5 µm** · LiNbO₃ 코팅 *"to decrease the interfacial resistance between NMC and SE"* [9–11] | stated | 코팅 두께 · 방법 미기재 |
| AM 전자 σ (Fig. 4a 의 NMC 100 vol% 점) | **≈7.0×10⁻⁵ S cm⁻¹** (SOC 0) | 판독 (7.04) | 본문에 값 · 측정법 **없음** · 코팅 입자인지 미기재 |
| 혼합 | *"mild mixing using a ball milling at 150 rpm for 30 min"* · 250 mL · ZrO₂ 볼 25 g (⌀ 2 mm) | stated | — |
| 조성 | **NMC 48 · 55 · 62 vol%** | stated | 기준 (고체 / 전체) · 환산 밀도 · wt% **미기재** |
| 압밀 (이온 차단 셀) | 복합 시료 **360 MPa · 실온** 펠릿 → SS 두 판 사이 | stated | 전자 차단 5 층 펠릿의 압밀 조건 · **측정 중 하중 미기재** |
| 시료 치수 (48 vol%, Fig. 2) | 이온 차단 L **0.032 cm** · A **0.816 cm²** / 전자 차단 L **0.034 cm** · A **0.843 cm²** | stated | 질량 없음 → 밀도 · 기공률 계산 불가 |
| 측정 온도 | DC **25 °C** (p.A3961 · A3962) | stated | AC 온도 미기재 |

### 3-2. Table I — SOC 0 % (DC vs AC, p.A3962)

| NMC (vol%) | σ_e DC | σ_e AC | σ_ion DC | σ_ion AC | σ_ion/σ_e (DC, 파생) | DC↔AC 차 (파생) |
|---|---|---|---|---|---|---|
| 48 | 2.0×10⁻⁶ | 1.9×10⁻⁶ | **5.0×10⁻⁵** | 5.0×10⁻⁵ | 25 | e 5 % · ion 0 % |
| 55 | 2.7×10⁻⁶ | 2.8×10⁻⁶ | **3.1×10⁻⁵** | 2.6×10⁻⁵ | 11.5 | e 4 % · ion 19 % |
| 62 | 6.7×10⁻⁶ | 6.4×10⁻⁶ | **2.2×10⁻⁵** | 2.0×10⁻⁵ | 3.3 | e 4.5 % · ion 10 % |

- 단위 S cm⁻¹ (stated).  원문: *"Before charging, the electronic conductivity is lower than the ionic conductivities in each composite."* · *"The differences between the two techniques are at most 5% and 20% for electronic and ionic conductivities, respectively. The contact resistance between stainless-steel current collector and samples is negligible."* (p.A3961–A3962)
- 조성 의존 (파생): σ_e 48 → 55 → 62 % = ×1.35 → ×2.48 (전체 ×3.35) · σ_ion = ÷1.61 → ÷1.41 (전체 ÷2.27).
- 본문 서술값 대조: 48 % *"2.0 × 10⁻⁶ … and 5.0 × 10⁻⁵"* ✓ · 55 % *"2.7 × 10⁻⁶ … 3.1 × 10⁻⁵"* ✓ · 62 % *"6.7 × 10⁻⁶ … 2.2 × 10⁻⁵"* ✓ (DC) · 62 % AC *"6.4 × 10⁻⁶ … 2.0 × 10⁻⁵"* ✓ (p.A3961).

### 3-3. Table II — SOC 0 % vs SOC 50 % (DC, p.A3962)

| NMC (vol%) | σ_e SOC 0 | σ_e SOC 50 (Li₂/₃Ni₁/₃Mn₁/₃Co₁/₃O₂) | ×(50/0) 파생 | σ_ion SOC 0 | σ_ion SOC 50 | ×(50/0) 파생 | SOC 50 σ_e/σ_ion 파생 |
|---|---|---|---|---|---|---|---|
| 48 | 2.0×10⁻⁶ | **5.2×10⁻⁵** | **26** | 5.0×10⁻⁵ | 5.2×10⁻⁵ | 1.04 | **1.00** |
| 55 | 2.7×10⁻⁶ | **9.3×10⁻⁵** | **34** | 3.1×10⁻⁵ | 3.0×10⁻⁵ | 0.97 | 3.1 |
| 62 | 6.7×10⁻⁶ | **3.0×10⁻⁴** | **45** | 2.2×10⁻⁵ | 2.1×10⁻⁵ | 0.95 | 14 |

- 원문: *"While the ionic conductivities of the composites are nearly unchanged, the electronic conductivities of the composites drastically increases after the charging process because electronic conductivity of NMC increases with Li extraction [3]."* · *"At SOC 50%, the electronic conductivity is higher than or equal to ionic conductivity in each composite."* (p.A3962)
- ★ **배수가 조성에 따라 다르다 (×26 → ×45, 파생)**.  σ_e,eff = f_e·σ₀,NMC(SOC) 이고 f_e 가 기하 상수라면 이 비는 조성과 무관해야 한다 → **f_e 가 SOC 와 함께 바뀐다** (또는 펠릿 안 SOC 불균일) — 원문은 이 차이를 논하지 않는다 (§8-2 결정 14).
- SOC 50 % 의 NMC 단독 σ 는 원문에 **없다** → SOC 50 % 의 전자 f · tau2 는 이 논문만으로 못 만든다.

### 3-4. 그림 판독값 (추세 전용 · 정밀 인용 불가)

| 그림 (쪽) | 판독 | 비고 |
|---|---|---|
| Fig. 2a (p.A3961) | 이온 차단 셀 정상 전류 ≈2.6×10⁻⁶ A @ 50 mV (600 s) | 파생 기대값 L/(σA) → 0.05 V/19.6 kΩ = 2.55×10⁻⁶ A 와 맞다 |
| Fig. 2b (p.A3961) | 전자 차단 셀 정상 전류 ≈5.3–5.4×10⁻⁵ A @ 50 mV (300 s 까지 그림) | R_tot ≈ 920–940 Ω ↔ 복합체만 L/(σA) = 807 Ω → **SE 층 + 계면 ≈ 116–137 Ω = 전체의 13–14 %** 를 뺀 셈 (파생) |
| Fig. 3 (p.A3961) | 고주파 작은 반원 끝 ≈ 1×10³ · 큰 원호 꼭대기 Z'' ≈ −6.4×10³ @ Z' ≈ 1.2×10⁴ · 저주파 끝 (r_e·L 화살표) **≈1.97×10⁴** (축 표기 Ω cm²) | 축 단위 의심 → §10 |
| Fig. 4a (p.A3962) | NMC 0 vol% (순수 SE) **≈3.5×10⁻⁴** · NMC 100 vol% (순수 NMC, 전자) **≈7.0×10⁻⁵** S cm⁻¹ | 표 값 점 6 개를 ≤3 % 로 재현하는 같은 판독 (48 % σ_ion 4.97×10⁻⁵ · σ_e 1.95×10⁻⁶ · 55 % σ_e 2.72×10⁻⁶ · 62 % σ_e 6.48×10⁻⁶) |
| Fig. 4b (p.A3962) | Table II 와 같음 — 48 % 에서 두 선이 만난다 (σ_e = σ_ion = 5.2×10⁻⁵) | — |
| Fig. 5 (p.A3962) | 0.13 mA cm⁻²: **≈149 / 142 / 144** · 0.64: **≈119 / 105 / 104** · 1.3: **≈92 / 70 / 67** mAh g⁻¹ (NMC 48 / 55 / 62) | y 축 "Average cell capacity" — 무엇의 평균인지 (사이클 · 셀) 미기재 |

### 3-5. "tortuosity 4–6" 과 재구성 (파생 — 원문에 식 없음)

원문 (p.A3963): *"Effective ionic and electronic conductivities are theoretically described using volume ratio and tortuosity. The tortuosity is a parameter which accounts for nonuniformity of solid electrolytes in the composite.[12] The estimated tortuosity of the composites with 48, 55, and 62 vol. % of NMC was in the range of 4 to 6 in this study. As expected, these are larger than those using a liquid electrolyte, but they are rather small considering that they are tortuosity of room temperature molded bodies of an inorganic solid powder. This is due to the high formability of the sulfide solid electrolytes.[13]"*

후보 꼴 (Table I DC 이온값 · φ_SE = 1 − x, 기공 0 가정):

| 꼴 | σ₀ 4.0×10⁻⁴ (본문) | σ₀ 3.5×10⁻⁴ (Fig. 4a 판독) | σ₀ 3.1×10⁻⁴ (sakuda2013 냉간 펠릿) | "4 to 6" 과 |
|---|---|---|---|---|
| **φ·σ₀/σ_eff** (tortuosity factor 꼴 = `tau2`) | **4.16 / 5.81 / 6.91** | **3.60 / 5.02 / 5.98** | 3.22 / 4.50 / 5.35 | **자릿수 맞음** (σ₀ 선택에 따라 4–7 · 3.6–6.0) |
| √(φ·σ₀/σ_eff) (`tau`) | 2.04 / 2.41 / 2.63 | 1.90 / 2.24 / 2.44 | 1.80 / 2.12 / 2.31 | 안 맞음 |
| σ₀/σ_eff (N_M = 1/f) | 8.0 / 12.9 / 18.2 | 6.9 / 11.2 / 15.7 | 6.2 / 10.0 / 14.1 | 안 맞음 |
| Bruggeman φ^−½ | 1.39 / 1.49 / 1.62 | 〃 | 〃 | 안 맞음 |

- AC 이온값이면 φσ₀/σ_eff = 4.16 / 6.92 / 7.60 (σ₀ 4.0) · SOC 50 % DC 이온값이면 4.00 / 6.00 / 7.24 (σ₀ 4.0) · 3.46 / 5.19 / 6.26 (σ₀ 3.5).
- 기공 감도 (고체 기준 x · 기공 p → φ_SE = (1 − p)(1 − x), σ₀ 4.0, DC): p 0.10 → 3.74 / 5.23 / 6.22 · p 0.15 → 3.54 / 4.94 / 5.87 · p 0.20 → 3.33 / 4.65 / 5.53.
- ⇒ "4 to 6" 은 **φσ₀/σ_eff 꼴 + (σ₀ 가 4×10⁻⁴ 보다 약간 낮거나, 10–15 % 기공 보정)** 과 정합한다.  원문이 어느 쪽을 썼는지는 **[미확인]** — 식 · σ₀ · φ 어느 것도 원문에 없다.
- [12] Patel 2003 의 정의식은 원문에 옮겨져 있지 않고 정본 카드도 없다 [미확인].  (`landesfeind2016_…` 카드는 Patel 을 N_M = κ/κ_eff 와 구형 입자 Bruggeman 검증의 인용원으로 적는다.)
- 원문은 이 값을 **이온 (SE) 쪽**에만 쓴다 ("nonuniformity of solid electrolytes") — 전자 tortuosity 는 계산하지 않았다.

## 4. ★ 방법 — 셀 → 저항 → 전도도 사슬

### 4-1. DC 분극 (Fig. 1 · Fig. 2, p.A3960–A3961)

| 목표 | 셀 (Fig. 1) | 절차 | 표지 |
|---|---|---|---|
| 전자 σ | **SS/Sample/SS (이온 차단)** | 복합 시료를 360 MPa · 실온 펠릿 → SS 판 두 장 (집전체) · 50 mV · **600 s 뒤 전류** · 25 °C | stated |
| 이온 σ | **SS/Li-In/SE/Sample/SE/Li-In/SS (전자 차단)** — *"five layer pellets"* · *"The SE layers were used as electron blocking layers"* | 50 mV · **300 s 뒤 전류** · *"The ionic resistances of the composite electrodes were calculated by subtracting the resistances of SE layers from the total resistances of the electron-blocking cells."* | stated |

- 기기: potentio-galvanostat SI-1287 (Solartron Analytical) · *"Typical applied DC voltage used was 50 mV."*
- 전도도 = L/(R·A) 로 읽힌다 (L · A 는 Fig. 2 캡션에만 있다 — 식은 원문에 없음).  Fig. 2a 판독 전류가 L/(σA) 기대값과 맞는다 (§3-4).
- **빼는 SE 층 저항의 출처** (별도 측정인지 σ₀ × 두께 계산인지) · Li-In/SE 계면 저항 처리 · 5 층 펠릿 압밀 조건은 **미기재** [미확인].  원문 서론은 그 위험을 스스로 적는다: *"The DC technique possibly causes the resistance including interfacial resistance when non-negligible resistance exists at the interface between the electrode and the solid electrolyte (SE) or between the SE and composite sample layer."* (p.A3960) — AC 와의 일치 (≤20 %) 가 그 크기를 묶는 유일한 근거다.
- 경계조건: 이온은 Li-In 가역 전극 사이를 **관통** · 전자는 SE 층에 막힘 → **conventional (관통형) 이온 저항** = 우리 망의 두 띠 Dirichlet 와 같은 부류 (다른 그룹의 Kaiser 2018 Eq. 11 저주파 극한과 같은 배치 — `kaiser2018_…` 카드).

### 4-2. AC 임피던스 — TLM 물방울 (Fig. 3, p.A3961)

- 셀 = **이온 차단 SS/Sample/SS 하나** · SI-1260 (Solartron) · **1 MHz – 1 mHz · 10 mV**.
- 원문 (p.A3961): *"Two depressed semicircles are observed. Siroma et al. have reported that a teardrop shape of the low frequency region was attributed to the ionic and electronic resistance from a transmission line model.[2] The high and low frequency limit values of the teardrop shape correspond to r_ion·r_e·L/(r_ion + r_e) and r_e·L, respectively, where r_ion, r_e and L are the ionic resistance, the electronic resistance and the length of the composite."* (본문 인쇄는 괄호 없이 "r_ion r_e L/r_ion + r_e" — Fig. 3 의 분수 표기가 바른 꼴)
- 읽는 법 (우리 정리): 고주파에서는 계면 용량이 두 레일을 단락 → **두 레일 병렬** L/(σ_ion + σ_e) · 저주파에서는 SS 가 이온을 막아 **전자 레일만** L/σ_e.  두 끝으로 σ_e 를 먼저, 그다음 σ_ion 을 푼다.
- 연결형 (siroma2015 카드 표 3 기준): 단자가 **같은 레일 (전자) 의 양 끝**에 달리고 이온 레일은 양 끝이 열린 **T형 open–open** 과 같은 극한 꼴 — DC 극한 = L·z_A (단자 레일 전부) · 고주파 = 두 레일 병렬.  **de Levie 형 (Z/E형, 저주파 L·z_A/3 = τ_e 계열) 이 아니다.**  ⚠ 원문이 인용한 것은 **Siroma 2016** (J. Power Sources 316, 215 — 정본 카드 없음) 이고 2015 표와의 대응은 우리 판독이다.
- 적용 조건 (서론, p.A3960): *"This model is effective especially when the electronic resistance of the composites is larger than or comparable to the ionic resistance."* — SOC 0 % 에서는 성립 (σ_ion/σ_e 3.3–25), **SOC 50 % 에서는 σ_e ≥ σ_ion 이라 깨지는 방향**이다.  SOC 50 % 를 DC 로만 잰 이유를 원문은 적지 않는다 (이 조건과의 연결은 우리 읽기).
- 첫 (고주파) 작은 반원의 귀속은 원문에 없다.

### 4-3. 충전 상태 (SOC 50 %) 측정 (p.A3961)
- *"Because the measurement needed a large amount of the composite electrode, the cell was constructed with thick composite electrode."* — 복합 펠릿 **80 mg** + SE 펠릿 **100 mg** 을 **360 MPa · 5 min** · In 상대극 → **93 mAh g⁻¹ (SOC 50 %, Li₂/₃Ni₁/₃Mn₁/₃Co₁/₃O₂)** 까지 0.13 mA cm⁻² 충전 (1470E, Solartron) → *"the composite pellets were removed from the batteries and the electronic and ionic conductivities were measured by the DC polarization technique"*.
- 빼낸 펠릿을 어떤 셀 (5 층 전자 차단 셀 재조립?) 에 어떻게 넣었는지 · 두께 펠릿 안 SOC 균일성은 **미기재** [미확인].
- 93 mAh g⁻¹ ↔ Li 1/3 추출 대응은 NMC 질량 기준 이론값 (≈92.6 mAh g⁻¹, 파생) 과 맞는다 → 비용량은 NMC 질량 기준으로 읽힌다.

### 4-4. 셀 용량 시험 (p.A3961)
- Li-In 상대극 · 이중층 펠릿 = 복합 양극 **15 mg** + SE **80 mg** · **360 MPa · 5 min** → SE 쪽에 In 박 + Li 박 **36 MPa · 2 min**.
- 0.13 · 0.64 · 1.3 mA cm⁻² · 차단 전압 **1.9–3.8 V vs Li-In (= 2.5–4.4 V vs Li⁺/Li)** · BTS-2004 (Nagano).  ⚠ 이 환산에 붙은 인용 번호는 [12] (목록상 Patel 2003, 다공 망 수치 모사) — 내용상 전위 환산의 출처로 맞지 않는다 (번호 착오 의심, 원문 그대로).
- **면적 · 두께 · 면적용량 · C-rate 미기재** → 같은 mA cm⁻² 가 조성마다 다른 비전류 (mA g⁻¹) 다 (복합체 질량 고정 15 mg → NMC 많을수록 NMC 질량↑ · 두께↓ — 둘 다 고-NMC 에 유리한 방향인데 관측은 반대, 우리 읽기).

### 4-5. 시뮬레이션 · 입자 처리
- **시뮬레이션 없음.**  입자 = 실물: NMC ≈5 µm (평균만, PSD 없음) · LiNbO₃ 코팅 · SE 분쇄 유리 (입경 미보고).
- 형상 소성은 실물에 들어 있다 — 원문은 낮은 tortuosity 를 **황화물 유리의 상온 성형성** [13] 으로 설명한다 (p.A3963).  이것은 우리 강체구 DEM 에 없는 **입자 형상 소성** (frame[1]/[2]) 이고 MPM J2 흐름이 그리는 쪽이다 — 단 이 논문 안에는 형태 증거 (SEM · 기공) 가 없다.

### 4-6. 기법 미니 용어집
- **DC 분극 (DC polarization)**: 일정 전압 (여기 50 mV) 을 걸고 정상 전류에서 저항을 읽는 법.  차단 전극으로 한 운반자만 흐르게 한다.
- **이온 차단 셀 (ion-blocking)**: SS/시료/SS — SS 는 전자만 통과 → DC 정상 전류 = 전자 전류.
- **전자 차단 셀 (electron-blocking)**: Li-In/SE/시료/SE/Li-In — SE 층이 전자를 막고 Li-In 이 Li⁺ 를 주고받는다 → DC 정상 전류 = 이온 전류 (SE 층 저항을 빼야 시료 값).
- **TLM (transmission line model)**: 이온 레일 r_ion · 전자 레일 r_e · 둘 사이 계면 소자의 사다리 회로.  여기서는 이온 차단 셀의 저주파 **물방울 (teardrop)** 모양의 두 끝으로 r_ion · r_e 를 뽑는다.
- **r_ion · r_e**: 원문 "ionic / electronic resistance" — 단위 길이 · 단위 면적당 저항 (Ω cm) 으로 읽힌다 (r·L = Ω cm²).  ⚠ 기호 r 은 반지름 · tortuosity 가 아니다.
- **SOC (state of charge)**: 여기서는 Li₂/₃ 조성 (93 mAh g⁻¹) 을 50 % 로 둔다.
- **T형 open–open / de Levie 형** (Siroma 2015 분류 — 이 논문은 쓰지 않는다): T형 = 단자가 한 레일의 양 끝 (관통) · de Levie = 이온이 한쪽 끝으로만 들어오고 분포 계면에서 소진 (저주파 R/3 → τ_e 계열).

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1** (p.A3960) | 측정법 · 셀 요약 표: DC 전자 = SS/Sample/SS (이온 차단) · DC 이온 = SS/Li-In/SE/Sample/SE/Li-In/SS (전자 차단) · AC 전자 + 이온 = SS/Sample/SS + 모식도 | **경계조건의 그림 증거** — DC 이온은 관통형 · AC 는 이온 차단 셀 (T형 꼴) |
| **2** (p.A3961) | 48 vol% DC 전류–시간 (반로그): (a) 이온 차단 (L 0.032 cm, A 0.816 cm²) σ_e = 2.0×10⁻⁶ · (b) 전자 차단 (L 0.034 cm, A 0.843 cm²) σ_ion = 5.0×10⁻⁵ | 수십 초 안에 정상 전류 (판독) · 캡션 "600 s" 인데 (b) 는 300 s 까지 그려짐 (본문 300 s) · SE 층 차감 몫 ≈13–14 % (파생) |
| **3** (p.A3961) | Nyquist (48 vol%, L 0.032 cm): 두 눌린 반원 · 물방울의 두 끝 화살표 r_ion r_e L/(r_ion + r_e) · r_e L · 삽입 σ_e 1.9×10⁻⁶ · σ_ion 5.0×10⁻⁵ | TLM 극한 두 개로 σ 두 개를 푸는 그림 — ⚠ 본문은 이 그림을 "62 vol%" 로 부른다 · x 축 표지 "Z''" · 축 단위 의심 (§10) |
| **4a** (p.A3962) | σ vs NMC vol% (SOC 0): 이온 (파랑) 0 % (순수 SE ≈3.5×10⁻⁴) → 62 % · 전자 (빨강) 48 % → 100 % (순수 NMC ≈7.0×10⁻⁵) · DC 실선 / AC 점선 | ★ **σ₀ 두 개 (SE · NMC) 가 그려진 유일한 자리** — 둘 다 본문 측정법 없음 |
| **4b** (p.A3962) | σ vs NMC vol% (SOC 50, DC): 전자 5.2×10⁻⁵ → 3.0×10⁻⁴ · 이온 5.2 → 2.1 ×10⁻⁵ · 48 % 에서 교차 | ★ 전자 σ 의 SOC 의존 (×26–45) — 우리 고정 σ_AM 의 한계 |
| **5** (p.A3962) | 평균 셀 용량 vs NMC vol% @ 0.13 · 0.64 · 1.3 mA cm⁻² | 고전류에서만 조성 의존 → 원문의 "이온 율속" 근거 · 면적용량 미기재 |
| Table I (p.A3962) | SOC 0 % σ_e · σ_ion, DC vs AC | ★ 핵심 데이터 (stated) |
| Table II (p.A3962) | SOC 0 vs 50 % σ_e · σ_ion (DC) | ★ 핵심 데이터 (stated) |

- 크롭 후보 (메인 순서대로 · 캡션 대조): **Table I** > **Table II** > **Fig. 4** (a+b) > **Fig. 1** > **Fig. 3** > **Fig. 5** > Fig. 2.

## 6. Post-processing ★
- **무엇**: DC 정상 전류 → R (전자 차단 셀은 SE 층 차감) → σ = L/(R·A) (식은 원문에 없음) · AC 물방울 두 끝 → r_e · r_ion → σ · 조성별 표 (Table I · II) · 반로그 σ vs vol% (Fig. 4) · 용량 vs vol% (Fig. 5) · "tortuosity" 는 식 없이 범위만 (p.A3963).
- **도구**: Solartron SI-1287 (DC) · SI-1260 (AC) · 1470E (충전) · Nagano BTS-2004 (셀 시험).  적합 소프트웨어 · 적합 회로 전체 · 오차막대 · 반복 수 **미기재**.
- **기공 회계 없음** — 밀도 · 기공률 · vol% 기준이 원문에 없다.  Kaiser 2018 (기공 0 고체 기준을 SI 표로 명시) · Minnmann 2021 (기공 14 % 로 φ 보정) 과 비교하면 **장부가 가장 얇다**.
- 수치 보고 정밀도: σ 는 2 유효숫자 · σ₀ 는 1 유효숫자 (4×10⁻⁴) — tau2 재구성의 불확도는 σ₀ 쪽이 지배한다 (§3-5).

## § τ 정의 대조 — 우리 규약 매핑

> 우리 규약 = CLAUDE.md ★★ τ 명명 규약 (1저자 비준 10-03).  'tortuosity factor' 는 τ² (`tau2`) 에만 쓴다.

| 원문 기호 (쪽) | 원문 정의식 | 원문 이름 | 정규화 (어느 부피 · 어느 단면 · 어느 σ₀) | 우리 다섯 양 중 | 환산 · 비고 |
|---|---|---|---|---|---|
| σ_ion (DC, Table I · II) | (식 없음) 전자 차단 셀 R_tot − R_SE층 → L/(R·A) 로 읽힘 | ionic conductivity | 시료 기하 단면 (A 0.843 cm², 48 %) · 두께 L · 관통 | σ_eff (망 `sigma_full` 의 차원값) | **관통형 (conventional)** — 우리 망과 같은 경계조건 부류 |
| σ_ion (AC, Table I) | 물방울 고주파 끝 r_ion r_e L/(r_ion + r_e) + 저주파 끝 r_e L 로 풂 | ionic conductivity | 이온 차단 셀 · 전 두께 레일 | σ_eff (관통형 부류) | Siroma 2015 표 3 T형 open–open 극한 꼴 (우리 판독) — **τ_e 계열 (de Levie R/3) 아님** |
| σ_e (DC · AC) | 이온 차단 셀 DC 정상 전류 / 물방울 저주파 끝 r_e L | electronic conductivity | 관통 · NMC 레일 | 전자 σ_eff (우리 `_el_`) | SOC 의존 ×26–45 (Table II) |
| σ_eff/σ₀ | 없음 | — | — | **f** (`f_ion_<mode>`) | 파생: 0.125 / 0.078 / 0.055 (DC, σ₀ 4.0×10⁻⁴) — **φ 없이 원문 값만으로 정해지는 유일한 무차원 양** |
| **"tortuosity"** (p.A3963) | **없음** — *"described using volume ratio and tortuosity"* | tortuosity (기호 없음 · "factor" 없음) | 원문 미기재 (부피 · σ₀ · 단면 모두) | **tau2 꼴 (재구성)** (`tau2_ion_<mode>`) | 값 4–6 은 φσ₀/σ_eff 꼴로만 재현 (§3-5) · ⚠ 정확한 σ₀ · φ 입력 [미확인] |
| (√ 값) | 보고 없음 | — | — | **tau** (`tau_ion_<mode>`) — 파생만 | 1.8–2.8 (σ₀ 선택 · DC/AC 에 따라) |
| volume ratio (p.A3960) | "NMC volume ratios of 48%, 55% and 62%" | volume ratio | **고체 / 전체 기준 미기재** | ≈ 1 − φ_SE (고체 기준이면) | φ_SE ≤ 1 − x → tau2 는 **상한** |
| σ₀ (p.A3960) | 4 × 10⁻⁴ S cm⁻¹ @ 25 °C | Li⁺ conductivity of the SE | 순수 SE (펠릿 · 압력 · 밀도 미기재) · Fig. 4a 0 % 점 ≈3.5×10⁻⁴ (판독) | 우리 `ion_sigma0_mScm` 자리 | **순수 SE ≡ 기준** 관례로 읽힌다 (Fig. 4a 가 0 % 끝점에 그린다) |
| τ_geo | 없음 | — | — | **τ_geo** — 해당 없음 | — |
| τ_e | 없음 | — | — | **τ_e** — 해당 없음 | AC 법은 T형 꼴이라 τ_e 를 주지 않는다 |
| r_ion · r_e (p.A3961) | TLM 레일 저항 | ionic / electronic resistance | 단위 길이 (Ω cm) | — | **기호 충돌 주의**: r 은 반지름 · 저항률 꼴 — 키 · 표로 옮길 때 꼬리표 |

**σ₀ 기준**: 순수 75Li₂S·25P₂S₅ 유리 — 본문값 **4×10⁻⁴ S cm⁻¹ @ 25 °C** (1 유효숫자 · 측정 셀 · 압밀 · 밀도 미기재) ↔ 같은 논문 Fig. 4a 의 0 % 점 **≈3.5×10⁻⁴** (판독) ↔ 같은 그룹 같은 조성 냉간 펠릿 (360 MPa) **3.1×10⁻⁴** (sakuda2013 카드, 다른 시료).
세 값의 폭 (×1.3) 이 같은 원자료의 tau2 를 그대로 ×1.3 움직인다.  우리 망 σ₀ 3.0 mS cm⁻¹ (LPSCl 펠릿값, `CL-91`) 는 망 안에서 약분되지만 (메모 v2 §3-1), 실험 tau2 는 **가정한 σ₀ 에 정비례**한다.

**환산 사슬 (한 줄로)**:
```
f          = σ_eff/σ₀                                  (원문 값만으로 정해짐 — φ 불필요)
tau2       = φ_SE·σ₀/σ_eff = φ_SE/f   ;  φ_SE ≤ 1 − x  →  tau2(1 − x) 는 상한   (기공 · vol% 기준 미보고)
"tortuosity 4–6" (원문) ≈ tau2 꼴 (재구성)  — √ 꼴 · N_M 꼴 · Bruggeman 은 자릿수가 안 맞음
σ₀ 짝 = 순수 SE (본문 4×10⁻⁴ ↔ 그림 ≈3.5×10⁻⁴)  →  tau2 ∝ σ₀
DC 이온 = 관통 (conventional) ;  AC = T형 open–open 꼴 (관통 부류)  — 둘 다 τ_e 아님
```

**판정**:
1. 원문의 이온 σ 두 개 (DC · AC) 는 **둘 다 관통형 부류**다 → 우리 tau2 와 같은 경계조건 꼴로 환산할 수 있다.  다른 것은 φ 장부 (미보고) 와 σ₀ 기준 상태 (순수 SE ≡ 1, 값 자체가 흔들림) 두 가지다.
2. "tortuosity 4–6" 은 **식이 없는 보고값**이다 — tau2 꼴이라는 판정은 재구성 (자릿수) 이고, 원문 숫자를 우리 표에 옮길 때는 "원문 낱말 tortuosity · 식 없음 · tau2 꼴로 재구성" 을 함께 적는다.  우리 쪽에서 다시 계산한 값 (f · tau2 상한) 을 쓰는 것이 낫다.
3. 이름이 아니라 식으로 판정한다는 원칙 (결정 15) 의 극단 사례 — **식이 아예 없으면 수치 재구성만 남는다** → 실험 앵커 메타에 "정의 재구성 여부" 를 다는 것을 제안 (§8-2).
4. COMSOL 칸으로 옮길 수 있는 양은 우리가 다시 계산한 tau2 (τ_F 꼴, 결정 5) 이고, 짝 σ₀ 는 이 논문의 순수 SE 값이다 — 단 φ 미보고라 상한으로만.

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md` (⚠ 이 브랜치에서는 값 자리표시 상태 — 우리 수치는 메모 v2 `docs/reviews/tau_conventions_judgment_v2_20261003.md` 의 유도값으로 적는다)

| 항목 | 이 논문 | 우리 | 같음 / 다름 · 이유 |
|---|---|---|---|
| 역할 (frame[5]) | 수송 절반의 **실험** — 이온 · 전자 σ_eff (조성 · SOC) + 셀 율 특성.  기계 · 형상 · 기공 · 입경 없음 | DEM 접촉망 T (이온 · conventional) · 전자 망 σ_e · STEP3 복셀 σ (CONTACT_FREE 가지) | 이 논문은 수송 쪽만 가진다 — 압밀 물리 (기공 · 형상) 는 비어 있다 |
| frame[4] | 실험 — 원칙적으로 독립 보정 앵커 후보 | 각 모델을 실험에 따로 보정 | ⛔ 재료 (유리 SE) · 기공 · 입경 미상이라 **이 값으로 우리 모델을 맞추지 않는다** |
| SE | **Li₃PS₄ 유리** (75Li₂S·25P₂S₅), σ₀ 4×10⁻⁴ S cm⁻¹ (0.4 mS cm⁻¹) · 상온 성형성 높음 [13] | LPSCl argyrodite (결정), 망 σ₀ 3.0 mS cm⁻¹ (펠릿값, `CL-91`) | **다른 재료 · 다른 상 · σ₀ 7.5 배 차** — 압밀성 (접촉 형성) 이 다를 수 있다 (원문은 그것을 낮은 τ 의 이유로 든다) |
| AM | **NMC111** ≈5 µm · LiNbO₃ 코팅 · 순수 NMC 전자 σ ≈7×10⁻⁵ S cm⁻¹ (SOC 0, 판독) | NMC811 (bimodal), 강체구 · σ_AM 입력 50 mS cm⁻¹ (모델 기준값, `CL-92`) · SOC 의존 없음 | 다름 — 전자 σ 는 조성 · SOC 로 자릿수가 바뀐다 (×26–45, Table II) |
| 입경비 | SE 입경 **미보고** (분쇄 유리) · NMC 평균만 | r_SE/r_AM 중앙 ≈ 0.13 (메모 v2 §3-3) | **대조 불가** |
| 기공 · φ 기준 | **미보고** · vol% 기준 미기재 | ε_sphere 명시 (예: 53 vol% 띠 중앙 15.8 %) · φ = 상자 기준 구합 | φ 축 위치가 (1 − p) 만큼 안 정해진다 |
| 압밀 · 측정 | 360 MPa 실온 (이온 차단 셀) · 측정 하중 · 5 층 셀 압밀 미기재 · 25 °C | 300 MPa 계열 냉간 압밀 · 최대 압밀 기하 (판 고정 완화) 의 망 | 압밀 범위 비슷 · springback 처리 비교 불가 |
| 두께 | 시료 0.032–0.034 cm (320–340 µm, 48 %) | 침대 L 15–184 µm (메모 v2 §7) | 이 논문 시료가 더 두껍다 — 띠 끝 효과 · 균질 가정 둘 다 유리 |
| τ 정의 | 식 없는 "tortuosity" (tau2 꼴 재구성) · 원 σ 는 관통형 | T = φ·σ₀/σ_full (`tau2`) | **같은 꼴로 환산 가능** — φ 미보고 · σ₀ 흔들림 |
| 값 (판정 없이) | tau2 상한 (φ = 1 − x, σ₀ 4.0) 4.2 @ φ ≤ 0.52 · 5.8 @ ≤ 0.45 · 6.9 @ ≤ 0.38 / 기공 10–17 % 를 빌리면 ≈3.5–3.7 @ ≈0.43–0.47 · ≈4.8–5.2 @ ≈0.37–0.41 · ≈5.7–6.2 @ ≈0.32–0.34 (파생 · 가정) | T_H 중앙 3.20 @ 0.444 띠 (2.36–4.87) · 5.40 @ 0.330 띠 (3.89–18.6) — 1세대 협착식 · 기준 상태 미보정 (메모 v2 §3-3) | **비율을 내지 않는다** — φ (가정) · σ₀ 기준 · 재료가 다르다.  ⛔ "일치 · 정합" 낱말 금지 (결정 4 게이트 전) |
| Bruggeman 배수 | tau2/φ^−½ = 3.0 / 3.9 / 4.3 (상한, 파생) | H 중앙 3.40 (IQR 2.54–6.71) · P 5.42 (메모 v2 §3-5) | 축은 같다 — 값 대조는 위와 같은 이유로 하지 않는다 |
| 방법 | DC 관통 + AC T형 (둘 다 관통 부류) | 관통 하나 (τ_e 없음) | 대응 부류 같음 |

- **방법 artifact 와 실제 차이의 구분**: 이 표의 어느 행도 "모델 오차 배수" 를 주지 않는다.  ① 강체구 DEM (겹침 = 형상 소성 대리) vs 실물 유리 SE 의 상온 성형 ② 재료 이전 (Li₃PS₄ 유리 ≠ LPSCl · NMC111 ≠ NMC811) ③ φ 장부 (미보고 vs 상자 기준 구합) ④ σ₀ 기준 (순수 SE 펠릿 ≡ 1 — 값 흔들림 · 우리는 간선 재료값 + Holm, 미정규화) ⑤ 판독 vs stated — 다섯이 겹친다.
- 우리 T 를 기준 상태로 맞추면 (메모 v2 §3-2 외삽 T_pure,ours ≈ 1.4–2.0, hertz) 5.40 → ≈2.7–3.9 로 내려간다 — 그래도 판정 대상이 아니다 (게이트 전).
- **frame[5]** — 이 논문이 가진 반쪽 = 실험 수송 (이온 · 전자 · SOC).  없는 반쪽 = 미세구조 (입경 · 기공 · 상 분포) · 기계 (압밀 · 형상 변화).  원문이 낮은 τ 의 이유로 든 **유리 SE 의 성형성** [13] 은 MPM (J2 형상 흐름) 이 그리는 절반이고, 우리 DEM 은 그것을 연화 E_eff (1.35 GPa) 의 겹침으로만 대리한다 — 이 논문만으로는 그 연결을 정량할 수 없다.

## 8. 적용 인사이트 (내 연구에 어떻게) — 이 묶음이 닫으려는 것

### 8-1. NCM111–Li₃PS₄ CAM 적재 ↔ 수송 스윕 — 같은 실험 축의 두 번째 점

| 물음 | 이 논문 (쪽) | 판정 |
|---|---|---|
| 측정법 | **DC 분극** (이온 차단 → σ_e · 전자 차단 + SE 층 차감 → σ_ion, 50 mV, 25 °C) + **AC 임피던스** (이온 차단 셀, TLM 물방울 두 끝) (Fig. 1 · p.A3961) | **차단 전극 DC + EIS-TLM** — Minnmann 과 같은 측정 축.  둘 다 관통형 부류 |
| 조성별 σ_ion,eff | 5.0 / 3.1 / 2.2 ×10⁻⁵ (DC) · 5.0 / 2.6 / 2.0 ×10⁻⁵ (AC) S cm⁻¹ (Table I) | stated |
| 조성별 σ_e,eff | SOC 0: 2.0 / 2.7 / 6.7 ×10⁻⁶ · SOC 50: 5.2×10⁻⁵ / 9.3×10⁻⁵ / 3.0×10⁻⁴ (Table I · II) | stated |
| 기공률 | **미보고** — 시료 L · A 는 있으나 질량 · 밀도 없음 (Fig. 2) | φ 를 원문 값만으로 못 정한다 |
| 성형 / 측정 압력 | 성형 360 MPa 실온 (이온 차단 셀) · 측정 하중 · 5 층 셀 조건 **미기재** (p.A3961) | springback 이력 비교 불가 |
| 온도 | DC 25 °C · σ₀ 25 °C (p.A3960–A3962) | — |
| 순수 Li₃PS₄ σ₀ | **4×10⁻⁴ S cm⁻¹** (본문, 조건 미기재) · ≈3.5×10⁻⁴ (Fig. 4a 판독) | 값 자체가 ≈14 % 흔들린다 |
| **tau2 = φσ₀/σ_eff 를 원문 값만으로?** | f 는 **예** (0.125 / 0.078 / 0.055) · tau2 는 **상한만** (φ_SE ≤ 1 − x → 4.2 / 5.8 / 6.9).  빠진 것 = ① 기공률 ② vol% 의 기준 (고체 / 전체) ③ σ₀ 의 측정 조건 (어느 값이 순수 SE 기준인가) ④ "tortuosity" 의 식 | 원문 "4–6" 은 재구성 정합 (§3-5) |
| 퍼콜레이션 문턱 | 원문 미논의 · 세 점 (48–62 %).  σ_e 는 55 → 62 % 에서 가팔라짐 (×2.5) · 62 % 에서도 f_e ≈ 0.095 (판독 σ₀ 기준) · σ_ion 붕괴 없음 | 문턱을 정할 수 없다 |
| 원문이 τ 를 쓰는가 | "tortuosity" 낱말만 · 식 없음 · 값 4–6 · [12] Patel 2003 인용 (p.A3963) | tau2 꼴 (재구성) |

**두 실험 맞대기 — Asano ↔ Minnmann (SI Table S2 · 정본 카드 `minnmann2021_…` 의 표; 파생 · 추세 전용)**

같은 φ_SE 축에 놓을 수 없으므로 (Asano 기공 미보고), **f (각자 순수 SE 기준)** 를 **고체 기준 NMC 분율 x_s** 위에서 맞댄다.  Minnmann x_s = φ_NCM/(φ_NCM + φ_SE) (표기 vol% 25/61 · 33/53 · 42/44 · 53/33 · 61/25 → 0.291 · 0.384 · 0.488 · 0.616 · 0.709).  ⚠ Asano 의 vol% 를 고체 기준으로 **가정**한다 (원문 미기재).

| x_s (고체 기준 NMC) | Asano f_ion (DC; σ₀ 4.0 / 3.5 ×10⁻⁴) | Minnmann f_ion (σ₀ 1.6 mS cm⁻¹, ln 보간) | 비 Asano/Minnmann | Asano f_el (σ₀ 판독 7.0×10⁻⁵) | Minnmann f_el (σ₀ 1.0×10⁻² S cm⁻¹, ln 보간) | 비 |
|---|---|---|---|---|---|---|
| 0.48 | 0.125 / 0.145 | 0.108 (42 vol% 점 x_s 0.488 의 0.104 근방) | **1.16 / 1.34** | 0.028 | 0.052 | 0.55 |
| 0.55 | 0.078 / 0.090 | 0.049 | **1.59 / 1.84** | 0.038 | 0.078 | 0.49 |
| 0.62 | 0.055 / 0.064 | 0.020 (53 vol% 점 x_s 0.616 의 0.0216 근방) | **2.81 / 3.25** | 0.095 | 0.112 | 0.85 |

- 같은 고체 기준 (기공 무시 · 둘 다 φ_SE = 1 − x_s) 의 tau2: Asano 4.16 / 5.81 / 6.91 ↔ Minnmann 4.93 (x_s 0.488) · 17.8 (x_s 0.616) → **x_s ≈ 0.48–0.49 에서 비 0.84 · ≈ 0.62 에서 0.39** (파생).
- **명목 vol% 그대로 (기준이 섞인 비교)** 면 Asano 62 % 의 f (0.055) 가 Minnmann 61 vol% 의 f (0.0019) 의 **29 배**다 — φ 장부 하나가 비를 ×1.2–2.8 ↔ ×29 로 흔든다.
- 판정: **측정 축은 같고 재료 축이 다르다** (유리 Li₃PS₄ σ₀ 0.4 mS cm⁻¹ · 분쇄 입경 미보고 · NMC111 코팅 5 µm ↔ LPSCl 1.6 mS cm⁻¹ · D50 3.45 / D90 20 µm · NCM622 3 µm).  두 실험은 **x_s ≈ 0.48 에서 f 가 ≈ 1.2 배로 가깝고**, 고-CAM (x_s ≈ 0.62) 으로 갈수록 **Asano 가 2.8 배 높은 f** 를 유지한다 (Minnmann 의 이온 붕괴는 x_s 0.616 → 0.709 구간 — Asano 의 시험 범위 바깥 입구).
  원인 후보 (검정 안 됨): SE 입경 (Minnmann 자신도 fine SE 로 61 vol% τ² 130 → 33.8) · 유리 SE 의 성형성 [13] · NMC 크기 · 코팅.  ⇒ **"실험 기준선" 자체가 같은 축에서 수 배 갈린다** — 메모 v2 결론 ④ ("SE 적은 쪽 = 다른 미세구조의 비교") 의 실험 쪽 증거이고, 우리 vs Minnmann 의 T_H/T_M 0.35–0.10 (53 · 61 vol% 띠) 을 "모델 오차" 로 읽지 말아야 할 이유가 하나 더 생긴다.
- 전자: 절대 σ_e 는 Minnmann 이 **167–287 배** 높지만 (σ₀,NMC 비 ≈142 배 — NCM622 1.0×10⁻² ↔ NMC111 ≈7×10⁻⁵ 판독), 각자 순수 AM 기준 f_el 은 **0.5–0.85 배**로 같은 자릿수다 → 전자 f 는 AM 화학을 정규화해 준다 — **단 SOC 가 같을 때만** (§3-3: ×26–45).

### 8-2. 결정별 인사이트 (메모 v2 §0-2 결정 번호)
- ① **결정 4 (순수 SE 기준 상태)** — 권고 **불변**.  보강 둘:
  (a) **한 논문 안에서도 σ₀ 가 흔들린다**: 본문 4×10⁻⁴ (조건 미기재) ↔ Fig. 4a 0 % 점 ≈3.5×10⁻⁴ (판독) ↔ 같은 그룹 같은 유리 냉간 펠릿 3.1×10⁻⁴ (sakuda2013 카드) → 같은 원자료의 tau2 가 ×1.3 움직인다.  4ⓓ (기준 시료의 압밀 · 측정 상태 메타) 에 **"σ₀ 출처 = 본문값 / 그림값 / 다른 논문"** 칸을 더한다.
  (b) **실험 기준선이 하나가 아니다**: 같은 측정 축의 두 실험이 고체 기준 같은 NMC 분율에서 f 1.2–2.8 배 (명목 vol% 기준이면 29 배) 갈린다 → 절대 대조는 게이트 (순수 SE 정규화) 뒤에도 **재료 · 입경 · φ 장부가 같은 실험**과만 한다는 판단이 강해진다.  4ⓑ (ε 장부) 에 **"vol% 의 기준 (고체 / 전체) 명시 여부"** 를 판정선 앞 필수 칸으로.
- ② **결정 14 (전자 T 의 정의)** — 권고 **불변** (오히려 "또는 f 만" 쪽을 지지).  근거: 복합체 σ_e 가 SOC 0 → 50 % 에서 **×26 / ×34 / ×45 (조성 의존)** — 단일 σ₀ 스케일링이면 비가 같아야 하므로 **f_e 자체가 상태 의존**이다 (또는 SOC 불균일 · 원문 미논의).  게다가 원문은 SOC 50 % 의 NMC 단독 σ₀ 를 주지 않는다 (SOC 0 의 순수 NMC 점 ≈7×10⁻⁵ 도 측정법 미기재 · 판독뿐).
  ⇒ 전자 T 를 싣는다면 σ₀ 메타에 **AM 상태 (SOC / 리튬화도)** 를 필수로 달고, 우리 모델 σ_e (σ_AM 50 mS cm⁻¹ 고정, `CL-92`) 는 **단일 상태 대리값**이라고 적는다.  인계 기본값은 f_el 만 (T_el 은 σ₀ 상태가 정해진 뒤).
- ③ **결정 13 (τ_e)** — 권고 **불변** ("부호 불정" 유지).  이 논문의 DC (전자 차단 · 관통) 와 AC (이온 차단 · T형 꼴 · 고주파 병렬 극한) 는 **둘 다 관통형 부류**라 0–19 % 일치는 τ_e ↔ conventional 비교가 **아니다** — Kaiser 2018 의 TLM (de Levie 계열) 과 같은 사례로 세지 않는다.  한정어 보강: EIS 값에 연결형 (T형 / Z·E형) 을 병기 (부록 결정 5 한정어와 같은 방향).
- ④ **결정 15 · 5 (이름 · COMSOL)** — 권고 **불변**.  "tortuosity" (factor 없음 · 기호 없음 · 식 없음) 가 tau2 꼴 값을 단 또 하나의 사례 → 식으로 판정하는 원칙 재확인.  식이 없을 때는 수치 재구성만 남으므로 실험 앵커 메타에 **"정의 재구성 (식 없음)"** 표지를 제안.

### 8-3. 그 밖의 적용
- **DC 전자 차단 셀의 차감 몫**: 48 vol% 에서 SE 층 + 계면 ≈ 전체 저항의 13–14 % (Fig. 2b 판독 · 파생).  이온 σ 가 높을수록 (SE 많을수록) 이 몫이 커져 차감 오차가 결과를 더 흔든다 — 실험 앵커를 고를 때 "SE 층 저항을 어떻게 뺐는가" 를 확인 항목으로.
- **율속 판정의 논리**: 1.3 mA cm⁻² 용량 서열 (48 > 55 ≳ 62 %) 은 SOC 0 의 σ_e 서열 (48 < 55 < 62) 과 **반대** → 방전 끝 (SOC 0 쪽) 의 전자 율속 가설은 이 데이터와 맞지 않고, 원문의 이온 율속 해석과 정합한다 (우리 읽기).  남는 교란 = 조성마다 다른 비전류 · 두께 (면적용량 미기재, §4-4).
- **STEP4 · 열화 쪽**: 전자 σ 의 SOC 의존 (×26–45) 은 우리 STEP4 의 고정 σ_AM 가정이 놓치는 축이다 — STEP4-v2 의 전자 옴강하가 이온보다 자릿수 작다는 실측 분해 (CLAUDE.md 07-21 기록) 는 σ_AM 이 높은 쪽 가정에서 나온 것이므로, 저-SOC (방전 끝) 에서 전자 몫이 커질 수 있다는 한정어 후보.
- **σ_ion 은 SOC 50 % 에서 거의 불변** (×0.95–1.04) — 한 번 충전 (NMC111, 50 %) 으로는 SE 망 이온 경로가 눈에 띄게 손상되지 않았다는 점 데이터.  사이클 열화 (A10 접촉 원장) 의 기준선으로는 1 회 · 1 상태뿐이라 약하다.

## 9. 인용 가능 문장 (deck/paper용)
- "Asano et al. measured the effective electronic and ionic conductivities of LiNbO₃-coated LiNi₁/₃Mn₁/₃Co₁/₃O₂–Li₃PS₄-glass composites (48–62 vol% NMC) with ion-/electron-blocking DC polarization and with the transmission-line analysis of a single ion-blocking cell; the two techniques agreed within 5 % (electronic) and 20 % (ionic) (J. Electrochem. Soc. 164 (2017) A3960)."
- "Upon charging to SOC 50 % (Li₂/₃Ni₁/₃Mn₁/₃Co₁/₃O₂), the electronic conductivity of the composites rose from 2.0–6.7 × 10⁻⁶ to 5.2 × 10⁻⁵–3.0 × 10⁻⁴ S cm⁻¹, while the ionic conductivity stayed at 2.1–5.2 × 10⁻⁵ S cm⁻¹."
- "The paper reports a 'tortuosity' of 4–6 without stating its definition; only the tortuosity-factor form φ·σ₀/σ_eff reproduces this order of magnitude from the reported conductivities, and because neither porosity nor the basis of the volume ratio is given, φ·σ₀/σ_eff can be bounded from above only."
- "Because the electronic conductivity of the composite changed by a composition-dependent factor of 26–45 between SOC 0 and 50 %, an electronic tortuosity factor is meaningful only together with the state of charge of its reference conductivity."

## 10. 주의/한계 (over-claim 방지)
- ⚠ **재료 전이**: SE = **Li₃PS₄ 유리** (0.4 mS cm⁻¹, 상온 성형성 높음) ≠ 우리 LPSCl argyrodite · AM = **NMC111 (LiNbO₃ 코팅)** ≠ NMC811.  수치를 우리 계로 옮기지 않는다.
- ⚠ **기공 · vol% 기준 · SE 입경 미보고** — tau2 는 상한으로만 · φ_SE 축 위치는 (1 − p) 만큼 불확정 · 입경비 축에 놓을 수 없다.
- ⚠ **"tortuosity 4–6" 은 식 · σ₀ · φ 가 없는 값**이다 — 재구성으로 tau2 꼴이라는 판정까지만.  σ₀ 4×10⁻⁴ · φ = 1 − x 로는 62 % 가 6.9 로 "6" 을 넘는다 (원문 입력은 [미확인]).  이 숫자를 정밀값으로 인용하지 않는다.
- ⚠ **σ₀ 흔들림**: 본문 4×10⁻⁴ (1 유효숫자 · 조건 미기재) ↔ Fig. 4a 0 % 점 ≈3.5×10⁻⁴ (판독; 같은 그림 표 값은 ≤3 % 재현) — ≈14 % 차.
- ⚠ **Fig. 4a 의 두 끝점 (순수 SE · 순수 NMC) 은 본문에 측정법 · 값이 없다** — 판독값을 σ₀ 로 쓸 때는 표지 필수.
- ⚠ **원문 내부 불일치** (그대로 두고 표지만):
  - Fig. 2 의 조성 — 본문 *"with 45 vol. % of NMC"* (p.A3961) ↔ 캡션 "48 vol. %" (조성표에 45 % 없음 → 본문 오기로 보임).
  - Fig. 3 의 조성 — 본문 *"Figure 3 shows a Nyquist plot of the composite with 62 vol. % of NMC"* · 62 % 값 6.4×10⁻⁶ · 2.0×10⁻⁵ 를 그 그림에서 푼 것처럼 씀 (p.A3961) ↔ 캡션 "NMC: 48 vol. %, L 0.032 cm" · 삽입값 1.9×10⁻⁶ · 5.0×10⁻⁵ = Table I 의 48 % AC 값.  ⇒ 그림은 48 % · 본문 서술은 62 % 를 섞었다.
  - Fig. 3 축 — x 축 표지가 "Z'' / Ω cm²" (실수부여야 함).  저주파 끝 판독 ≈1.97×10⁴ 를 표기대로 Ω cm² 로 읽으면 σ_e = L/(r_e L) ≈ 1.6×10⁻⁶, **Ω 로 읽고 Fig. 2a 의 A 0.816 cm² 를 쓰면 ≈2.0×10⁻⁶** — 삽입값 1.9×10⁻⁶ 은 후자에 가깝다 → 축 단위 표기 의심 (판독 기반 · 원문 미언급).
  - Fig. 2 캡션 *"under a constant voltage of 50 mV for 600 s"* ↔ 본문 이온 300 s · (b) 그림 300 s 까지.
  - 초록 "(a) electron-blocking cells and (b) ion-blocking cells" ↔ Fig. 2 (a) 이온 차단 · (b) 전자 차단 (순서 반대).
  - p.A3961 의 Li-In ↔ Li⁺/Li 전위 환산에 [12] (Patel 2003) — 내용상 맞지 않는 인용 번호.
  - 서론의 Siroma 2016 재료 표기 "LiNi0.5Mn0.2Co0.3O2" (p.A3960) — Siroma 2016 원문 미대조 (그대로 옮김).
  - 오탈자: "potentio-galvanoostat" (p.A3961) · "This results suggest" (p.A3962).
- ⚠ **율속 결론의 범위**: 세 조성 · 한 SOC (50 %) 의 σ 값 · 면적용량 미기재.  결론의 설계 규칙 *"The composite with the almost the same ionic conductivity as electronic conductivity will show the highest rate performance"* (p.A3963) 은 **검정되지 않았다** — σ_ion = σ_e 인 48 % 가 시험한 가장 낮은 NMC 분율이라, "균형점이 최적" 과 "σ_ion 이 클수록 좋다" 를 이 데이터로 가를 수 없다 (더 낮은 NMC 조성이 없다).  초록 자신도 *"seemed to be associated"* 로 썼다.
- ⚠ SOC 50 % 측정의 셀 재조립 · 펠릿 안 SOC 균일성 · AC 측정 온도 · 반복 수 · 오차막대 · 적합 회로 전체 **미기재**.
- ⚠ 시뮬레이션 없음 — DEM · MPM 어느 쪽의 검증도 아니다 (frame[4]: 실험 쪽 앵커 후보일 뿐, 이 계에서는 연결 조건 미충족).

### 10-1. 메모 v2 정정 후보 (`docs/reviews/tau_conventions_judgment_v2_20261003.md`)
1. **§8-2 의 [27] 행** — *"NCM111–Li₃PS₄ CAM 적재 ↔ 수송 스윕 — 같은 실험 축의 두 번째 점 | §3-3"*.
   원문으로는 **측정 축만 같다** (차단 전극 DC + EIS-TLM · CAM vol% 스윕 · 360 MPa — Fig. 1 p.A3960 · p.A3961).  **§3-3 의 φ_SE 띠에는 가정 없이 놓을 수 없다**: 기공률 미보고 · vol% 기준 미기재 (p.A3960) · SE 입경 미보고 · SE = Li₃PS₄ 유리 σ₀ 4×10⁻⁴ (p.A3960) · 세 점 (48–62 %).
   → 닫는 항목을 *"결정 4 (실험 기준선의 산포 — 고체 기준 f 1.2–2.8 배 · σ₀ 한 논문 안 ×1.14) · 결정 14 (전자 σ 의 SOC 의존 ×26–45, Table II p.A3962)"* 로 바꾸고, §3-3 에는 **f 추세점 (고체 기준 가정)** 으로만 두는 것을 제안.
2. (보강 · 정정 아님) **결론 ④ · §3-8** — "SE 적은 쪽 = 다른 미세구조의 비교" 에 실험끼리의 산포를 근거로 더할 수 있다: 같은 측정 축의 두 실험이 고체 기준 x_s ≈ 0.62 에서 f 2.8 배 (명목 vol% 기준 29 배) 갈린다 (Table I p.A3962 ↔ Minnmann SI Table S2, 파생).
3. (보강) **§3-1 비대칭 문단** ("실험 T 는 가정한 σ₀ 에 정비례") 에 한 논문 안의 σ₀ 흔들림 사례: 본문 4×10⁻⁴ (p.A3960) ↔ Fig. 4a ≈3.5×10⁻⁴ (판독, p.A3962).
4. (보강) **§1 명명 표**에 이 논문 열을 더할 수 있다: "tortuosity" — 기호 · 식 없음 (p.A3963) · 값은 tau2 꼴로만 재현 (재구성).

### 10-2. 이 논문을 인용하는 카드 — 원문과 대조
| 카드 | 그 카드의 서술 | 이 원문 | 판정 |
|---|---|---|---|
| `minnmann2021_jes_charge_transport_bottlenecks` (참고문헌 표 [27]) | *"NCM111–Li₃PS₄ 의 CAM 적재 ↔ 수송 스윕 (49 vol% 최적, p.7) — 같은 실험 축의 두 번째 점"* | 조성은 **48 · 55 · 62 vol%** 뿐 · **"optimum" 낱말 없음**.  48 % 가 SOC 50 % 에서 σ_ion = σ_e (Table II) 이고 1.3 mA cm⁻² 에서 용량 최고 (Fig. 5) · 결론의 설계 규칙 (σ_ion ≈ σ_e → 최고 율 특성, p.A3963) — 그러나 48 % 는 시험 범위의 **끝점** | **"49 vol%" 는 원문에 없다**.  Minnmann 원문 p.7 의 문장은 이 환경에 PDF 가 없어 대조 못 함 — 가능성: Minnmann 42 vol% (기공 포함) 의 고체 기준 환산 48.8 % ≈ 49 % (우리 산술 · 미확인).  "최적" 은 내부 최적이 아니라 시험 범위 끝점의 최고값이다 |
| `cronau2022_wet_milling_particle_size_ionic_conductivity` (참고문헌 표 [22]–[24]) | Cronau p.2 `[20,22–24]` *"불활성 용매 + 1–3 mm 볼 LWM 이 입경 감소에 성공"* | SE 를 *"heptane and dibutyl ether"* + ZrO₂ 볼 200 g (⌀ 2 mm) 로 분쇄 (p.A3960, [5] = WO 특허) — **분쇄 뒤 입경 · PSD 를 보고하지 않는다** | 절차 (불활성 용매 + 2 mm 볼) 는 맞다 · **"입경 감소 성공" 은 이 원문의 수치로 뒷받침되지 않는다** (Cronau 의 인용 문장 쪽 문제 — 카드 전사는 Cronau 그대로) |
| `hlushkou2018_void_space_ion_transport_assb_cathode` (참고문헌 표 [20]) | *"황화물 복합양극 조성 스윕 — 메모 v2 §8-2 의 같은 실험 축 두 번째 점"* · 서지 문자열 | 서지 (제목 · 권 · 쪽 A3960–A3963) ✓ · 조성 스윕 ✓ | "같은 실험 축 두 번째 점" 은 §10-1 의 1 과 같은 한정이 필요 (측정 축만 같음) |

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)

| 서지 (원문 목록 그대로) | 왜 | 정본 카드 |
|---|---|---|
| 2. Z. Siroma, T. Sato, T. Takeuchi, R. Nagai, A. Ota, and T. Ioroi, J. Power Sources, 316, 215 (2016). | AC 법 (이온 차단 셀 물방울 TLM) 의 원전 — 연결형 (T형 판독) · 고주파/저주파 극한의 유도 · 적용 조건 (r_e ≳ r_ion) 확인.  ⚠ `siroma2015_…` (Electrochim. Acta 160, 313) 과 **다른 논문** | 없음 |
| 12. K. K. Patel, J. M. Paulsen, and J. Desilvestro, J. Power Sources, 122, 144 (2003). | 원문 "tortuosity" 의 유일한 인용원 — τ 정의 (τ/ε 인지 τ²/ε 인지) 로 재구성 판정을 닫는다 | 없음 (`landesfeind2016_…` 가 [2] 로 서지만 보유) |
| 13. A. Sakuda, A. Hayashi, and M. Tatsumisago, Sci. Rep., 3, 2261 (2013). | 낮은 τ 의 이유로 든 "high formability" · 같은 유리의 냉간 펠릿 σ (3.1×10⁻⁴ @ 360 MPa) | ✅ `sakuda2013_sulfide_mechanical_property` |
| 3. M. Shibuya, T. Nishina, T. Matsue, and I. Uchida, J. Electrochem. Soc., 143, 3157 (1996). | "electronic conductivity of NMC increases with lithium extraction" 의 인용원 — 전자 σ₀ 의 SOC 의존 원값 (재료가 NMC 인지 원문 목록만으로는 미확인) | 없음 |
| 11. A. Sakuda, T. Takeuchi, and H. Kobayashi, Solid State Ionics, 285, 112 (2016). | SE 미립자 · AM 위 SE 코팅이 이온 경로를 개선한다는 근거 (p.A3963) — 입경비 가설의 같은 그룹 쪽 자료 | 없음 |
| 5. K. Sugiura and M. Ohashi, WO patent WO2013/073035. | SE 습식 분쇄 (헵탄 + 디부틸에테르) 절차 — 입경 결과가 있는지 | 없음 |
| 9. N. Ohta, K. Takada, L. Zhang, R. Ma, M. Osada, and T. Sasaki, Adv. Mater., 18, 2226 (2006). · 10. N. Ohta, K. Takada, I. Sakaguchi, L. Zhang, R. Ma, K. Fukuda, M. Osada, and T. Sasaki, Electrochem. Commun., 9, 1486 (2007). | LiNbO₃ 코팅 — 코팅이 전자 접촉 (NMC–NMC) 에 주는 저항 (전자 f 해석) | 없음 (다른 카드들이 Ohta 를 인용) |
| 4. A. Hayashi, S. Hama, H. Morimoto, M. Tatsumisago, and T. Minami, J. Am. Ceram. Soc., 84, 477 (2001). | 75Li₂S·25P₂S₅ 유리 기계적 밀링 합성 | 없음 |
| 8. H. Kitaura, A. Hayashi, K. Tadanaga, and M. Tatsumisago, Electrochim. Acta, 55, 8821 (2010). | 같은 그룹의 NMC 복합 양극 기준 | 없음 |
| 1. K. Takada, Acta Mater., 61, 759 (2013). · 6. T. Ohzuku and Y. Makimura, Chem. Lett., 30, 642 (2001). · 7. N. Yabuuchi and T. Ohzuku, J. Power Sources, 119, 171 (2003). | 서론 일반 · NMC111 재료 | 없음 |

- 정본 카드 유무 = `litdb/papers/` 파일 목록 + 서지 낱말 grep 으로 확인 (2026-10-03).

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것)
- 본문 4 쪽 (A3960–A3963) + IOP 표지를 전부 렌더로 읽었다 (Table I · II · Fig. 1–5 · 참고문헌 13).  SI 없음 · 본문의 SI 인용 없음.
- Fig. 4a 를 확대 판독해 표 값 점 6 개를 ≤3 % 로 재현한 뒤 두 끝점 (순수 SE ≈3.46×10⁻⁴ · 순수 NMC ≈7.04×10⁻⁵) 을 읽었다.
- Fig. 2a 판독 전류 (≈2.6×10⁻⁶ A) 가 L/(σA) = 2.55×10⁻⁶ A 와 맞는다 → 전도도 = L/(R·A) 로 읽음.  Fig. 2b 로 SE 층 차감 몫 13–14 % (파생).
- "tortuosity 4–6" 의 후보 꼴 넷을 σ₀ 세 값 · DC/AC · SOC 0/50 으로 다시 계산했다 (§3-5).
- Minnmann 비교의 수 (f · x_s · ln 보간) 는 정본 카드 `minnmann2021_…` 의 SI Table S2 전사값으로 계산했다 — Minnmann 원문은 이 카드에서 다시 보지 않았다.
- 본문 어디에도 없는 것: 기공률 · 밀도 · 시료 질량 (전도도 셀) · vol% 기준 · SE 입경 · σ₀ 측정 조건 · 측정 중 하중 · AC 온도 · 반복 수 · 오차막대 · 적합 회로 · "tortuosity" 의 식 · 면적용량 · C-rate.

## 이 논문을 인용하는 corpus 카드
- `minnmann2021_jes_charge_transport_bottlenecks` — [27] (같은 측정 축 · "49 vol% 최적" 서술은 원문과 어긋남, §10-2).
- `hlushkou2018_void_space_ion_transport_assb_cathode` — [20] (조성 스윕 · 메모 v2 §8-2 표현).
- `cronau2022_wet_milling_particle_size_ionic_conductivity` — [22] (습식 분쇄 절차 — 입경 결과는 이 원문에 없음, §10-2).

## Q&A 로그
- (아직 없음)
