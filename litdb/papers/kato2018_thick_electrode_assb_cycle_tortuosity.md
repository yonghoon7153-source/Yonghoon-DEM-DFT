<!-- digest 표준 양식 확장 (paper-level STANDALONE).  ★ = 사용자가 특히 원한 항목.  깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     τ 묶음 형식 기준 = tjaden2018_tortuosity_review_calculation_approaches.md · landesfeind2016_tortuosity_eis_electrodes_separators.md ·
     taufactor_tortuosity_factor_tomography_tool.md + 같은 날 앞 묶음 (kaiser2018_… · hlushkou2018_… · froboese2019_… 를 열어 보고 같은 결로 썼다).
     이 논문은 실험 논문이다 (시뮬레이션 없음) — §4 '방법' 은 측정 · 적합 사슬 (반응대 모형 → 율속 자료 적합 → κ_eff → τ) 로 쓴다.
     쪽 표기: 본문 = 학술지 인쇄 쪽 p.607–613.  PDF n 쪽 = 인쇄 p.(606 + n)  (PDF 1 = p.607 … PDF 7 = p.613).
     SI = 별도 PDF 12 쪽 — 인쇄 쪽 번호가 없다 → "SI p.n" = SI PDF 쪽 (SI p.1 = 표지).
     식 · 표 · 그림 번호 = 원문 번호 (본문 eq 1–4 · Table 1–5 · Figure 1–4 / SI Eq S1–S5 · Table S1 · Figure S1–S7 · SI 참고문헌 34–36).
     수식 · 표 · 그림 쪽은 렌더해서 읽었다 (텍스트 추출은 τ→t, ε→1, κ→k 로 깨진다).
     값 표지: stated = 본문 · 캡션 · 표 원문 / 판독 = 그림에서 읽은 근사 (≈ · 추세 전용, 정밀 인용 불가) / 우리 산술 = 원문 숫자로 이 카드가 계산 (식 명시) / [미확인] = 원문에 없음. -->
# 600 µm 후막 전고체 전지의 율속 (용량–전류) 자료에서 이온 수송 tortuosity factor 를 뽑다 — Doyle–Newman ohmic-limit 반응대 식 (eq 4) · LiCoO₂ 양극 τ 2.47 (LGPS · Li₂S–P₂S₅ 유리 공유 가정) · 흑연 음극 τ 3.32 · 15.7 mAh cm⁻² — Kato (J. Phys. Chem. Lett. 2018)

> slug `kato2018_thick_electrode_assb_cycle_tortuosity` · DOI `10.1021/acs.jpclett.7b02880` · type `exp (율속 방전 자료 → Doyle–Newman ohmic-limit 반응대 식 (eq 4) 적합 → κ_eff · tortuosity factor τ; TLM-FSW 임피던스는 κ_eff 고정 정합 확인 — 후막 ASSB LiCoO₂/흑연, 시뮬레이션 없음)` · PDF `22. All-solid-state batteries with thick electrode configurations.pdf` · digested `2026-10-03` · status ✅
>
> SI = `22. Sup) All-solid-state batteries with thick electrode configurations.pdf` (12 쪽 — 표지 · §1 용량 적재 · 에너지밀도 (Fig S1–S2) · §2 실험법 (SE 3 종 합성 · XRD Fig S3–S5 · 전도도 측정 · 셀 제작 · 충방전 · 임피던스 · SEM) · §3 SEM (Fig S6) · §4 임피던스 해석 (Table S1 · Eq S1–S5) · §5 성능 추정 (Fig S7) · §6 추가 참고문헌 34–36).  본문 7 쪽 + SI 12 쪽 **전부 읽었다**.
>
> ★ **정의 판정 (이 카드의 목적)** — 이 논문의 τ 는 원문 낱말로 **"tortuosity factor"** (초록 p.607 · Eq 2 문장 p.609 · "Bruggeman tortuosity factor τ = ε^−0.5" p.611) 이고, 정의식은 **κ_eff = (ε/τ)·κ** (Eq 2, p.609) ⇒ **τ = ε·κ/κ_eff = 우리 `tau2`**.
> 제곱 기호 없이 τ 로 쓴다 — 보고값 2.47 · 3.32 를 **제곱하지 말 것** (이미 τ² 꼴).  √ 값 (우리 tau) · 기하 τ (τ_geo) 는 이 논문에 없다.
> 정규화 셋: **ε = 분말 배합의 공칭 SE 부피분율 0.57** (Table 2 — vol% 합 100 = 기공 0 의 고체 기준) · **κ (= σ₀) = 같은 SE 의 냉간 압분 펠릿** (420 MPa, 25 °C — SI p.6; LGPS 3.2 · 75Li₂S–25P₂S₅ 유리 0.28 · LiI 유리 1.2 mS cm⁻¹) · **q (용량밀도) = 치밀 조성값** (953 · 1298 C cm⁻³ — 기공 0 값과 같다, 우리 산술).
> 측정 경계조건 = **직류 관통형** — 반응대 앞면이 전극 안을 움직이는 sink 이고 이온만 옴 강하를 진다 = conventional τ 계열.  **τ_e (TLM) 가 아니다** — 임피던스 적합은 κ_eff 를 고정해 넣은 정합 확인이다.
>
> ★ **닫는 것 (메모 v2 §8-2 "EIS 와 독립인 사이클 기반 τ" · 닫는 항목 "절대 대조 교차")** — 답: **정의 교차는 선다 · 값 교차는 서지 않는다.**
> 같은 양 (tau2 · conventional · 펠릿 σ₀ ≡ 1 · Bruggeman 꼴 = COMSOL τ_F) 이라는 정의 쪽 근거는 깨끗하다.  값은 판정선 앵커가 못 된다: (i) 기공 미측정 + q 치밀 장부 → 상자 기준 환산 **τ × (1−p)²** (p = 0.10–0.20 이면 양극 2.00–1.58, 우리 산술)
> (ii) 재료 = LGPS · Li₂S–P₂S₅ 유리 + LiNbO₃ 코팅 LiCoO₂ 3–5 µm + 아세틸렌블랙 4.8 vol% (iii) 조성 하나 (ε 0.57) · 두 SE 의 τ 를 **같다고 놓고** 푼 값 (iv) 방법 내부 어긋남 ≈ 20–25 % (V–t 기울기 경로 ↔ eq 4 용량 경로, 우리 산술).
> 그리고 "사이클 기반" 은 원문과 다르다 — **율속 (방전 용량–전류) 기반**이다.  사이클 수 축 자료는 10 회 용량 유지 (Fig 1) 뿐이고 τ 추출에 쓰이지 않았다.
>
> 형제 카드: `kaiser2018_ion_transport_limitations_assb_sulfide_electrodes` (같은 Toyota–Marburg 계열 · 같은 해 · EIS 경로 · 공저자 Y. Kato) · `hlushkou2018_void_space_ion_transport_assb_cathode` (LiCoO₂ + LiI–Li₂S–P₂S₅ 유리 · 이 논문을 [21] 로 인용) ·
> `minnmann2021_jes_charge_transport_bottlenecks` (이 논문을 [33] 으로 인용 · EIS τ² 의 LPSCl 앵커) · `froboese2019_microstructure_ionic_conductivity_assb_electrode` (Eq 15 의 출처로 [36] 인용) · `park2019_electrode_design_methodology_assb_3d` ([35] 인용) ·
> `bielefeld2020_effective_ionic_conductivity_binder` (이 논문의 양극을 재구성해 σ 시뮬을 검증) · `deng2016_elastic_superionic_electrolytes_dft` (= 이 논문 SI 참고문헌 36 — τ_c1 = τ_c2 의 근거로 인용된 탄성 물성).

---

## 0. 결론 먼저 (정의 판정 + 핵심 수치)

| 질문 | 답 | 근거 (식 · 쪽) |
|---|---|---|
| τ 는 어떤 양인가 | **tortuosity factor τ = ε·κ/κ_eff = tau2**.  원문 낱말에 "factor" 가 있다 (같은 해 Kaiser "effective tortuosity" · Hlushkou "ionic conductivity-based tortuosity" 와 다르다).  제곱 표기 · √ 값 없음 | Eq 2 (p.609) · 초록 (p.607) · p.611 |
| 용량–전류 자료에서 τ 를 뽑는 식 | 반응대 (reaction zone) 모형의 ohmic limit: **V = U^θ − R_o i − (t/(q κ_eff)) i²** (eq 1) → 풀셀 (eq 3) → 컷오프 V_cutoff 에 닿는 용량 **C = t_d i = (1/i)·(1/(q_c κ_eff,cj) + 1/(q_a κ_eff,a))⁻¹·(U_c^θ − U_a^θ − V_cutoff − R_o i)** (eq 4) | p.609–610 |
| 적합 · 미지수 | 율속 자료 (L75–L600, 0.1–100 mA cm⁻²) 를 SE 계 (j = 1, 2) 마다 eq 4 에 맞춰 X_j = (1/(q_cκ_eff,cj) + 1/(q_aκ_eff,a))⁻¹ 두 개를 얻고, 미지수 셋 (κ_eff,c1 · κ_eff,c2 · κ_eff,a) 은 **τ_c1 = τ_c2 가정** (SEM 형태 유사) 으로 닫는다 | p.610 · Fig 3 · SI p.8 |
| 값 (stated) | κ_eff,c1 **0.73** · κ_eff,c2 **0.065** · κ_eff,a **0.21** mS cm⁻¹ · **τ_c1 (= τ_c2) 2.47** · **τ_a 3.32** | Table 5 (p.610) |
| 인쇄 식 ↔ 보고값 | **Eq 2 는 오식이 아니다** — 0.57×3.2/0.73 = 2.50 · 0.57×0.28/0.065 = 2.46 (보고 2.47 = 그 사이) · 0.57×1.2/0.21 = 3.26 (보고 3.32 = κ_eff,a 0.206 의 반올림).  차이 ≤ 2 % (우리 산술).  Minnmann 2021 Eq 4 같은 역수 오식은 없다 | §3-5 |
| 가정 (원문) | ① 이온 수송 지배 (σ_eff,c 0.3 · σ_eff,a 0.7 S cm⁻¹ ≫ κ) ② 고체 전해질 t_Li+ ≈ 1 → **농도 구배 없음** → **옴 효과 지배** (log C–log i 기울기 −1) — 액체의 한계 전류 (고갈) 기전이 아니다 (우리 해석) ③ 고확산 활물질 (반응대 앞면 모형 [18]) ④ U^θ · R_o 상수 ⑤ τ_c1 = τ_c2 | p.608 · p.610 · SI p.8 |
| 두께는 어디 들어가나 | **추출식에 직접 들어가지 않는다** — 높은 전류의 용량은 두께와 무관 (Fig 2c · Fig 3).  두께는 q = C/L 로만 들어가고, 쓰인 q 는 치밀값이다 | p.610 · Table 4 |
| σ₀ 기준 | **같은 SE 의 냉간 압분 펠릿** (알루미나 실린더 420 MPa · SS 집전 · 25 °C · Ar · 0.1 Hz–1 MHz).  LGPS 는 소결 펠릿 8.3 mS cm⁻¹ 도 쟀지만 냉간 값 3.2 를 "used for subsequent investigations".  측정 중 가압 유지 여부 [미확인] | SI p.4 · SI p.6 |
| ε · 기공 | ε = 0.57 = Table 2 의 공칭 부피분율 (wt% ÷ ρ 정규화, 기공 0).  기공률은 재지 않았다 — SEM 에서 SE 영역의 void · crack 을 정성 관찰 ("interference … increase in the tortuosity factor") | Table 2 (p.608) · p.610 · SI p.8 |
| 600 µm · 15.7 mAh cm⁻² | L600 = LCO 115.4 mg cm⁻², 이론 (양극 제한) **15.7** mAh cm⁻² (Table 3 · 초록; p.611–612 · SI p.2 는 15.8).  0.5 mA cm⁻² (≈ C/31) 에서 충전 > 95 % · 방전 **93 %** · 10 사이클 > 99 % · 6 mA cm⁻² 에서 **13.9 mAh cm⁻² (88 %)** · 25 °C · 운전압 50 MPa | p.607–608 · Table 3 · SI p.7 |
| 두 SE 비교 | 같은 형태라는 가정 아래 SE 전도도 비 (3.2/0.28 = 11.4) 가 거의 그대로 κ_eff 비 (11.2) 로 간다 — **형태 차를 시험한 것이 아니라 가정한 것**이다 | p.610 · SI p.8 |
| 우리 양 매핑 | **tau2 (conventional, 관통 DC)** — 우리 망 T 와 같은 꼴.  다른 것: φ 장부 (고체 기준 ε + 치밀 q → 상자 환산 (1−p)²) · 기준 상태 (냉간 펠릿 ≡ 1) | § τ 정의 대조 |
| 결정 4 뒤 절대 대조점? | **아니오** — 정의 사례 · EIS 와 독립인 DC 방법 사례 · **기준 상태 인자 실측 한 쌍** (LGPS 냉간 3.2 ↔ 소결 8.3 mS cm⁻¹ = 2.6 배) 으로 쓴다 | §8-0 |

## 1. 한 줄 요약
Toyota · 도쿄공대 (Kanno 그룹) 가 **LiNbO₃ 코팅 LiCoO₂ + 황화물 SE + 아세틸렌블랙** 양극 (두께 ≈ 75–600 µm) 과 **흑연 + LiI–Li₂S–P₂S₅ 유리** 음극으로 **600 µm 양극 · 15.7 mAh cm⁻²** 후막 전고체 전지를 상온에서 돌리고 (0.5 mA cm⁻² 방전 93 %),
양극 SE 를 **Li₁₀GeP₂S₁₂ (3.2 mS cm⁻¹) 와 75Li₂S–25P₂S₅ 유리 (0.28)** 로 바꿔 율속을 쟀다.  고체 전해질은 Li⁺ 운반율이 ≈ 1 이라 농도 구배가 없어 방전이 **옴 한계 (반응대 앞면 모형)** 로 기술되고, 그 해석식 (eq 4) 을 용량–전류 자료에 맞춰
**전극의 유효 이온전도도 κ_eff 와 tortuosity factor τ (= ε·κ/κ_eff)** 를 **임피던스 없이** 뽑았다 — 양극 2.47 (두 SE 공유 가정) · 음극 3.32 (흑연이 막자 혼합에서 변형 · 세로로 퍼짐).
같은 κ_eff 로 TLM-FSW 임피던스를 재현해 정합을 보이고, eq 4 로 "Bruggeman τ (ε^−0.5) 면 20 mA cm⁻² 에서 용량 ≈ 2 배" · "10 mS cm⁻¹ SE 면 15.8 mAh cm⁻² 를 30 mA cm⁻² 에서" 를 투영한다.
우리에게는 **tortuosity factor = tau2 = COMSOL τ_F 꼴의 원문 사례**, **펠릿 ≡ 1 기준 상태의 다섯째 원문 사례**, **기준 상태 인자 (냉간 ↔ 소결 2.6 배) 실측**이다 — 기공 미측정 · 재료 (LGPS/유리 · LCO · 탄소) · 조성 하나 때문에 우리 T 의 절대 대조점은 못 된다.

## 2. 메타

| 저자 | 저널/년 | DOI | 재료계 | 연구유형 |
|---|---|---|---|---|
| **Yuki Kato** (교신; Toyota Motor Europe NV/SA · Toyota Motor Corporation), Shinya Shiotani (Toyota Motor Corporation · Tokyo Tech), Keisuke Morita (Toyota Motor Corporation), Kota Suzuki · Masaaki Hirayama · **Ryoji Kanno** (Tokyo Institute of Technology, School of Materials and Chemical Technology) | **J. Phys. Chem. Lett. 9 (2018) 607–613** (Letter) | **10.1021/acs.jpclett.7b02880** | 양극: **LiNbO₃ 코팅 LiCoO₂** (Toda D5, 3–5 µm) + SE1 **Li₁₀GeP₂S₁₂** 또는 SE2 **75Li₂S–25P₂S₅ 유리** + **아세틸렌블랙** · 분리막 · 음극 SE3 **30LiI–70(0.75Li₂S–0.25P₂S₅) 유리** · 음극 AM **흑연** (Mitsubishi Chemical, ≈ 10 µm) — 바인더 없음 | **실험** (율속 · 사이클 · EIS · SEM) + 해석식 적합 (eq 4) + 등가회로 시뮬 (TLM-FSW) |

- 접수 2017-10-30 · 승인 2018-01-17 · 출판 2018-01-17 (p.607).  © 2018 American Chemical Society — 오픈 액세스 표기 없음.  저자 선언: 경쟁 이해 없음 (p.612).
- 사사 (p.612): SE 합성 · 셀 제작 지원 (Ms. Marta Cazorla Soult · Ms. Poonam Yadav).  연구비 기관 표기 없음.
- 같은 그룹 선행: 참고문헌 (8) Kato 2016 *Nat. Energy* (고출력 ASSB, 25 µm 박막 전극 > 50 mA cm⁻²) · (13) Kamaya 2011 *Nat. Mater.* (LGPS).
- 공저자 관계: 제1저자 Y. Kato 는 같은 해 Kaiser 2018 · Hlushkou 2018 (Marburg) 의 공저자다 — 이 논문은 EIS 가 아닌 **율속 경로**로 같은 물음 (ASSB 전극 τ) 에 답한다.

## 3. 핵심 수치 (★ 전부 원문 쪽 · 표지 병기)

### 3-1. SE 3 종 · σ₀ (Table 1, p.608 · SI §2.1–2.2)

| SE | 조성 · 상 | κ (= σ₀) | 조건 · 비고 | 표지 · 쪽 |
|---|---|---|---|---|
| **SE1** (양극) | Li₁₀GeP₂S₁₂ — 볼밀 370 rpm 40 h → 석영관 550 °C 8 h.  XRD 주상 LGPS (ICSD 248307) + **β-Li₃PS₄ 2차상** | **3.2 mS cm⁻¹** | **냉간 압분 펠릿 · 25 °C** — *"this value was used for subsequent investigations"* | stated · Table 1 · SI p.4 |
| SE1 (참고) | 같은 분말의 **소결 펠릿** | **8.3 mS cm⁻¹** | *"a comparable conductivity to literature values¹³ (i.e., 8.3 mS cm⁻¹) was obtained for the sintered pellet state"* · 문헌보다 약간 낮은 원인 = β-Li₃PS₄ 2차상 추정 | stated · SI p.4 |
| **SE2** (양극) | 75Li₂S–25P₂S₅ — 볼밀 370 rpm 40 h, XRD 비정질 | **0.28 mS cm⁻¹** | 같은 측정법 (아래) | stated · Table 1 · SI p.5 |
| **SE3** (분리막 · 음극) | 30LiI–70(0.75Li₂S–0.25P₂S₅) — 볼밀 370 rpm 40 h, XRD 비정질 | **1.2 mS cm⁻¹** | 흑연과의 안정성 때문에 분리막 · 음극에 사용 | stated · Table 1 · SI p.5–6 |
| 측정법 (셋 공통) | 알루미나 실린더에서 **420 MPa** 로 펠릿 → SS 집전 사이 → AC 임피던스 **25 °C · Ar** · **0.1 Hz – 1 MHz** · Solartron 1260 | — | **측정 중 가압 유지 여부 · 펠릿 두께 · 상대밀도 [미확인]** | stated · SI p.6 |
| 기준 상태 인자 (우리 산술) | LGPS 냉간 3.2 ↔ 소결 8.3 | **× 2.6** | 소결값을 σ₀ 로 쓰면 τ_c1 = 0.57 × 8.3/0.73 = **6.48** (보고 2.47 의 2.6 배) | 우리 산술 |
| 교차 (타 카드) | 75Li₂S–25P₂S₅ 유리: 냉간 0.31 @ 360 MPa ↔ 열간 0.34 mS cm⁻¹ (`sakuda2013_sulfide_mechanical_property` stated) | ≈ × 1.1 | 유리는 냉간 압분만으로 거의 치밀 — **결정 LGPS 와 기준 상태 인자가 다르다** (다른 논문 · 다른 배치의 값) | 타 카드 · 교차 산술 |

### 3-2. 복합체 조성 (Table 2, p.608) — ε 의 출처

| 물질 | 밀도 (g cm⁻³) | 양극층 wt% | 음극층 wt% | 양극층 vol% | 음극층 vol% |
|---|---|---|---|---|---|
| LiCoO₂ (LiNbO₃ 코팅) | 5.05 | 61 | — | 38.1 | — |
| 아세틸렌블랙 | 2.00 | 3 | — | 4.8 | — |
| 고체 전해질 | 2.00 | 36 | 54 | **57.1 (ε = 0.57)** | **57 (ε = 0.57)** |
| 흑연 | 2.27 | — | 46 | — | 43 |

- vol% = **wt%/ρ 를 정규화한 값**이다 (우리 산술: 양극 38.25 / 4.75 / 57.0 · 음극 57.13 / 42.87 — 표와 0.15 %p 안).  ⇒ **ε 는 기공 0 의 고체 기준**이다.  기공률 수치는 본문 · SI 어디에도 없다.
- SE 밀도는 세 SE 모두 2.00 으로 둔다 (표 값).  두 전극의 ε 가 우연히 같다 (0.57).

### 3-3. 전극 구성 (Table 3, p.609) — 두께는 치밀 명목값

| 구성 | 양극 두께 L_c (µm) | LCO 적재 (mg cm⁻²) | 음극 두께 L_a (µm) | 흑연 적재 (mg cm⁻²) | 용량 (양극 제한, mAh cm⁻²) | 137 mAh g⁻¹ × 적재 (우리 산술) | 치밀 두께 (우리 산술, µm) |
|---|---|---|---|---|---|---|---|
| L75 | ~75 | 14.5 | ~66 | 6.4 | 2.00 | 1.99 | 75.2 |
| L100 | ~100 | 19.3 | ~88 | 8.6 | 2.64 | 2.64 | 100.1 |
| L125 | ~125 | 24.1 | ~109 | 10.7 | 3.30 | 3.30 | 124.9 |
| L150 | ~150 | 28.9 | ~131 | 12.8 | 3.96 | 3.96 | 149.8 |
| L200 | ~200 | 38.6 | ~174 | 17.1 | 5.29 | 5.29 | 200.1 |
| L250 | ~250 | 48.2 | ~219 | 21.4 | 6.60 | 6.60 | 249.9 |
| L300 | ~300 | 57.7 | ~262 | 25.6 | 7.93 | 7.90 | 299.1 |
| **L600** | **~600** | **115.4** | **~524** | **51.3** | **15.7** | **15.81** | **598.3** |

- **치밀 두께** = 적재 ÷ 0.61 ÷ ρ_comp (ρ_comp = Σ vol% × ρ = 3.162 g cm⁻³, 기공 0).  양극 여덟 구성 모두 표의 두께와 0.3 % 안 · 음극도 같은 식 (ρ = 0.57 × 2.00 + 0.43 × 2.27) 으로 65.7 … 527.0 µm = 표와 1 % 안.  ⇒ **표의 두께는 기공 0 의 명목값과 같다**.  실측 두께 언급은 없다 [미확인] — 그런데 SEM 은 void · crack 을 보인다 (p.610).
- 용량 열은 137 mAh g⁻¹ (SI p.2 Fig S1 캡션) 와 L75 · L300 · L600 에서 0.3–0.7 % 어긋난다 (§10-1).
- 음극/양극 용량비 (L600, 우리 산술): 51.3 × 0.370 / 15.81 = **1.20**.  적층 명목 두께 (우리 산술) 600 + 100 + 524 ≈ **1.22 mm**.

### 3-4. 셀 매개변수 (Table 4, p.610)

| 기호 | 값 | 뜻 · 검산 (우리 산술) |
|---|---|---|
| q_c | **953 C cm⁻³** | 양극 용량밀도.  치밀 조성값 0.381 × 5.05 × 137 × 3.6 = **949** · Table 3 L300 의 C/L = 952 ⇒ **기공 0 값** |
| q_a | **1298 C cm⁻³** | 음극 용량밀도.  0.43 × 2.27 × 370 × 3.6 = **1300** ⇒ 기공 0 값 |
| U_c^θ | 4.1 V vs Li/Li⁺ | 충전 상태 양극 OCP (상수 가정) |
| U_a^θ | 0.1 V vs Li/Li⁺ | 음극 OCP (상수) |
| V_cutoff | 2.5 V | ΔU − V_cutoff = **1.5 V** 가 옴 강하 예산 |
| R_o | **8 Ω cm²** | "high frequency resistance" — **측정법 미기재** [미확인].  분리막 100 µm / 1.2 mS cm⁻¹ = 8.3 Ω cm² 와 같은 크기 · Fig 4a 고주파 절편 ≈ 3.8–4.5 Ω (판독, 1 cm²) 보다는 크고 반원 끝 ≈ 7 Ω (판독) 에 가깝다 |

### 3-5. ★ 이온 수송 결과 (Table 5, p.610) — 재계산 · 환산

| 양 | 보고값 | 재계산 · 환산 (우리 산술) |
|---|---|---|
| κ_eff,c1 (SE1 양극) | **0.73 mS cm⁻¹** | f = κ_eff/κ = 0.228 · τ 를 2.47 로 두면 0.738 |
| κ_eff,c2 (SE2 양극) | **0.065 mS cm⁻¹** | f = 0.232 · τ 2.47 이면 0.0646 |
| κ_eff,a (음극, SE3) | **0.21 mS cm⁻¹** | f = 0.175 · τ 3.32 이면 0.206 |
| **τ_c1 (= τ_c2)** | **2.47** | SE1 단독 2.50 · SE2 단독 2.46 → 평균 2.48.  κ_eff 비 0.73/0.065 = 11.23 ↔ κ 비 3.2/0.28 = 11.43 (−1.7 %) — **가정이 강제한 정합**이지 시험이 아니다 |
| **τ_a** | **3.32** | 0.57 × 1.2/0.21 = 3.26 (κ_eff,a 0.206 반올림 차) |
| √τ (= 우리 tau) | 보고 없음 | 1.57 (양극) · 1.82 (음극) |
| N_M = τ/ε = κ/κ_eff | 보고 없음 | 4.33 (양극) · 5.82 (음극) |
| Bruggeman τ_B = ε^−0.5 (원문 정의, p.611) | — | 0.57^−0.5 = 1.32 → **τ/τ_B = 1.86 (양극) · 2.51 (음극)** |
| 상자 기준 환산 (기공 p 미측정 — 가정 값) | — | ε_box = 0.57(1−p) · κ_eff,box = κ_eff/(1−p) · **τ_box = τ(1−p)²**: p 0.10 → 양극 2.00 · 음극 2.69 / p 0.15 → 1.78 · 2.40 / p 0.20 → 1.58 · 2.12 (ε 만 고치면 τ(1−p): 2.22–1.98) |
| X_j = (1/(q_cκ_eff,cj) + 1/(q_aκ_eff,a))⁻¹ | (Fig 3 적합값, 숫자 미기재) | Table 4 · 5 로 재구성: **X₁ = 0.196 · X₂ = 0.0505 C S cm⁻⁴** (X₁⁻¹ = 5.11 · X₂⁻¹ = 19.8 V s⁻¹ cm⁴ A⁻²) |

- **환산 (1−p)² 의 이유** (우리 유도): 적합이 정하는 것은 곱 q·κ_eff 다.  실제 전극이 기공 p 를 가지면 실제 q = q_치밀 (1−p) 이므로 실제 κ_eff = κ_eff,보고 /(1−p) 이고, 상자 기준 ε 는 0.57(1−p) 다 → τ_box = τ_보고 (1−p)².  두께를 실측한 Kaiser · Hlushkou 는 ε 만 고치면 되는 (1−p)¹ 부류다.
- Eq 4 재현 (우리 산술, Table 4 · 5 그대로): SE1 C(6 mA cm⁻²) = 47.4 C cm⁻² = **13.2 mAh cm⁻²** (본문 실측 13.9, −5 %) · C(10) log 1.44 · C(100) log 0.14 — Fig 3 빨간 선과 맞는다.  SE2 C(10) log 0.86 · C(100) log −0.45 — 파란 선과 맞는다.

### 3-6. 방전 · 사이클 수치 (Fig 1–2 · 본문)

| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| L600 충전 · 방전 (0.5 mA cm⁻², SE1) | 충전 **> 95 %** · 방전 **93 %** (이론 대비) — 방전 ≈ 14.6 mAh cm⁻² (우리 산술 0.93 × 15.7) | stated · p.607 |
| L600 사이클 (0.5 mA cm⁻², 10 회) | **> 99 %** 유지 · 충방전 효율 ≈ 100 % · 첫 사이클 효율 낮음 (음극/SE 계면 부동태 추정) · 과전압이 조금씩 증가 (양극–탄소 부반응 추정 [10,17]) | stated · p.607 · Fig 1 |
| L600 율속 (SE1, Fig 2b) | i < 6 mA cm⁻² 이론 용량에 가깝다 · **i = 6 → 13.9 mAh cm⁻² (88 %)** · i > 6 직선 방전 곡선 = 옴 한계 | stated · p.608 |
| 방전 곡선 기울기 (L600, SE1) | **−0.52 · −2.07 · −6.22** @ i = 6 · 12 · 20 mA cm⁻² (단위 미기재 — 그림 축으로 V h⁻¹) — 비 3.98 · 11.96 ↔ (i 비)² 4.0 · 11.1 | stated · p.609–610 |
| 두께 의존 (Fig 2c, i = 12 mA cm⁻²) | L100 은 > 80 % 방전 · 기울기는 두께와 무관 · SE 전도도에 강하게 의존 | stated · p.610 |
| SE 의존 (Fig 2d, L300, 12 mA cm⁻²) | SE1 ≈ 6.6 · SE2 ≈ 2.0 mAh cm⁻² (판독) — eq 4 재계산 6.37 · 1.64 (우리 산술) | 판독 · Fig 2d |
| 율속 범위 (Fig 3) | 0.1–100 mA cm⁻² · 높은 전류에서 두께 무관 · log C–log i **기울기 −1** = 옴 한계 전극 거동 | stated · p.610 |
| 0.5 mA cm⁻² 곡선 형태 (Fig 2a) | L300 = 흑연 단계 구조의 고원 · L600 = 매끈한 경사 (ΔV/ΔC 상수 @ ≈ 3.8 V) — 질량 수송 과전압으로 전극 깊이별 SOC 가 퍼진 결과로 해석 | stated · p.608 |
| C-rate 환산 (L600, 우리 산술) | 0.5 mA cm⁻² ≈ C/31 · 6 ≈ 0.38C · 12 ≈ 0.76C · 20 ≈ 1.3C · 100 ≈ 6.4C | 우리 산술 |

### 3-7. ★ 방법 내부 대조 — V–t 기울기 경로 ↔ eq 4 용량 경로 (우리 산술)

| 경로 | 무엇에서 | X⁻¹ = 1/(q_cκ_eff,c) + 1/(q_aκ_eff,a) (V s⁻¹ cm⁴ A⁻², SE1) |
|---|---|---|
| 본문 기울기 (eq 1/3 의 dV/dt = −X⁻¹ i²) | −0.52 / −2.07 / −6.22 V h⁻¹ @ 6 / 12 / 20 mA cm⁻² | **4.01 / 3.99 / 4.32** |
| Fig 2b 삽도 (기울기 vs i², 0–100 mA cm⁻²) | 직선 판독 | **≈ 4.2–4.5** (판독) |
| eq 4 적합 (Table 4 · 5 로 재구성) | Fig 3 율속 | **5.11** |

- 원문은 *"the slope shown in the inset of Figure 2b corresponds with the value of (1/(q_cκ_eff,c) + 1/(q_aκ_eff,a)) for the SE1 system"* (p.610) 이라고만 쓰고 삽도 기울기 숫자를 주지 않는다.  두 경로는 **≈ 15–25 %** 어긋난다 — Table 5 값은 실측 기울기를 0.66 / 2.65 / 7.35 V h⁻¹ 로 18–28 % 크게 예측한다.
- 해석 (우리 해석 — 원문에 없음): eq 4 는 방전 시작 전압을 U_c − U_a − R_o i (6 mA cm⁻² 에서 3.95 V) 로 두는데, 실측 곡선은 ≈ 3.75 V 에서 시작한다 (판독, Fig 2b — 시작 간격 ≈ 0.2 V @ 6 · 0.3 @ 12 · 0.4 @ 20 mA cm⁻²).  그 비옴 과전압 (전하전달 · 고체 확산) 을 용량 적합이 X⁻¹ 로 흡수하면 κ_eff 가 낮게 · **τ 가 높게** 나온다.  기울기 경로로 바꾸면 τ 는 ≈ 20 % 낮다 (양극 ≈ 2.0 · 음극 ≈ 2.7 — 분배 가정 τ_c1 = τ_c2 그대로).
- 보강 (우리 산술): Table S1 의 LCO 값 (d 5 µm · D 5×10⁻¹⁵ m² s⁻¹) 으로 τ_d = d²/D = 5000 s ≈ **1.4 h** — 적합 창의 방전 시간 0.2–2.3 h 와 같은 크기다.  "고확산 활물질" 전제 (p.608) 가 이 창에서 넉넉하지 않다 (원문도 큰 전류의 이탈을 입자 내 확산 탓으로 적는다, p.610).

### 3-8. 임피던스 (Fig 4 · SI §4 Table S1)

- 측정 (SI p.7): CCCV 충전 (0.5 mA cm⁻², 컷오프 0.005 mA cm⁻²) 으로 4.1 V → 25 °C · Ar · **10 mV · 0.1 mHz – 1 MHz** · VMP3 (Bio-Logic).  대상 = SE1 의 **L300 · L600**.
- 스펙트럼 (p.611, stated): 고주파 (10⁶–10¹ Hz) 작은 반원 · 중간 (≈ 10⁻³ Hz) ≈ 45° · 저주파 (≈ 10⁻⁴ Hz) 용량성 · **중저주파의 두께 의존** — 다공 전극의 확산 시간 상수가 활물질 입자 수준 이상이라는 해석.  0.1 mHz 끝점 −Z″ ≈ 117 Ω (L600) · ≈ 172 Ω (L300) (판독).
- 적합 (p.611 · SI p.9–10): Z = Z_elec,a + R_sep + Z_elec,c · TLM (Tröltzsch–Kanoun 해석해, Eq S1) · Z_i = 1/(Aκ_eff) · Z_e = 1/(Aσ_eff) (Eq S2) · Z_CT = Z_particle/(A·N) (Eq S3) · Z_particle = (R_CT ∥ CPE) + FSW 직렬 · FSW (Eq S4) · τ_d = d²/D (Eq S5).  **κ_eff 는 율속 값 (Table 5) 을 고정해 넣었고, 맞춘 것은 R_sep · R_CT · CPE · N 뿐**이다.

Table S1 (SI p.9, stated — 단위 원문 그대로):

| 셀 · 층 | L_elec (m) | A (m²) | σ_eff (S m⁻¹) | κ_eff (S m⁻¹) | CPE Q · n | R_ct (Ω) | d (m) | D (m² s⁻¹) | C_diff (F) | N (m⁻³) |
|---|---|---|---|---|---|---|---|---|---|---|
| L300 양극 | 3.00×10⁻⁴ | 10⁻⁴ | 30 | 0.073 | 5×10⁻⁶ · 0.85 | 42 | 5×10⁻⁶ | 5×10⁻¹⁵ | 10 | 1.0×10¹⁰ |
| L300 음극 | 2.62×10⁻⁴ | 10⁻⁴ | 70 | 0.021 | 5×10⁻³ · 1 | 0.10 | 5×10⁻⁵ | 5×10⁻¹¹ | 0.1 | 3.0×10⁹ |
| L600 양극 | 6.00×10⁻⁴ | 10⁻⁴ | 30 | 0.073 | 1×10⁻⁶ · 0.85 | 54 | 5×10⁻⁶ | 5×10⁻¹⁵ | 10 | 2.0×10¹⁰ |
| L600 음극 | 5.24×10⁻⁴ | 10⁻⁴ | 70 | 0.021 | 5×10⁻³ · 1 | 0.13 | 5×10⁻⁵ | 5×10⁻¹¹ | 0.1 | 3.1×10⁹ |

- 각주 (원문): a 율속 특성에서 · b DC 분극에서 · c SEM 추정 · d 참고문헌 31 (LCO 박막 D) · e 참고문헌 30 (흑연 D) · f 4.1 V 의 dQ/dV · g 참고문헌 23.  ⚠ σ_eff 에 a, κ_eff 에 b 가 붙어 있는데 SI 본문 (p.9–10) 은 반대로 적는다 (전자 = DC 분극 이온차단 셀 · 이온 = 율속) — 각주 뒤바뀜 (§10-1).
- 전자 전도도 (p.608, stated): σ_eff,c = **0.3 S cm⁻¹** (= 30 S m⁻¹) · σ_eff,a = **0.7 S cm⁻¹** — 이온 차단 셀 DC 분극 (측정법은 SI p.9–10).  σ_eff/κ_eff (우리 산술) = 411 (양극) · 3333 (음극) → 옴 한계 전제 (이온만 강하) 와 정합.
- R_sep 은 "refined" 라 했지만 **값이 표에 없다** [미확인].  N (부피당 요소 수, 적합값) 이 양극에서 L300 → L600 으로 **두 배** (1.0 → 2.0×10¹⁰ m⁻³) — 부피 밀도라면 두께와 무관해야 한다 (원문 설명 없음).
- 원문 판정: *"The good fit of the impedance data also confirms the accuracy of the effective conductivity or tortuosity factors obtained from the rate–capacity plots"* (p.611).  ⚠ Fig 4a 의 L600 저주파 부분은 적합선이 데이터 아래로 보이고 (판독, Z′ ≈ 40–60 Ω), SI p.10 은 ≈ 5×10⁻⁴ Hz 의 이탈을 입경 분포 탓으로 적는다.  자유 매개변수가 넷 (R_sep · R_CT · CPE · N) 이라 **κ_eff 의 독립 검정은 아니다**.

### 3-9. 투영 (Fig S7) · 에너지밀도 (Fig S2) · 적재 비교 (Fig S1)

| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| Fig S7 (i) "low tortuosity factor (τ = ε^−0.5)" — *"homogeneous mixing, no cracks or voids"* | SE1 에서 i = 20 mA cm⁻² 용량 **≈ 2 배** (stated).  우리 산술: X = 0.444 → C(20) = 29.7 ↔ 실측 적합 13.1 C cm⁻² = **× 2.27** | stated · p.611 · SI p.11 |
| Fig S7 (ii) "high ionic conductivity (κ = 10 mS cm⁻¹)" (양극 · 음극 둘 다) | 본문: *"the full capacity of the L600 configuration (15.8 mAh cm⁻²) can be discharged at 30 mA cm⁻²"* (p.611–612).  우리 산술 (eq 4 · τ 2.47/3.32): C(30) = **12.9 mAh cm⁻²** (R_o 8 유지) · 15.1 (R_o 를 10 mS cm⁻¹ 분리막 값 1 Ω cm² 로) — 15.8 전량은 **≈ 25–29 mA cm⁻²** 에서.  Fig S7 파란 선 판독 ≈ 50 C cm⁻² (≈ 14 mAh cm⁻²) @ 30 mA cm⁻² | stated · 우리 산술 · 판독 |
| 결론 문장 | 10 mS cm⁻¹ 초과 재료 [8,13,32,33] 는 **소결 · 열간압 상태**의 값 → *"materials exhibiting high conductivities in the compressed state are desirable"* | stated · p.612 |
| 에너지밀도 (Fig S2) | L600 **435 Wh L⁻¹ · 180 Wh kg⁻¹** — 20 µm Al (2.7 g cc⁻¹) · Cu (8.9 g cc⁻¹) 집전체를 **가정한 계산값** · L75 ≈ 245 Wh L⁻¹ · 117 Wh kg⁻¹ (판독) | stated · 판독 · SI p.3 |
| 적재 비교 (Fig S1) | L600 = 15.8 (LCO) · ≈ 19 (흑연) mAh cm⁻² — LCO/흑연 ASSB 보고값 중 최고.  다음 = Kato 2016 ≈ 7.7 (판독) | stated · 판독 · SI p.2 |

## 4. ★ 방법 — 율속 자료를 τ 로 바꾸는 사슬

### 4-1. 반응대 모형 · ohmic limit (eq 1–3, p.609 · 렌더로 확인)

| 식 | 원문 | 뜻 · 비고 |
|---|---|---|
| eq 1 | V = U^θ − R_o i − (t/(q κ_eff)) i² | 반쪽 전지의 옴 한계 전압.  U^θ = 충전 상태 OCP · R_o = 고주파 저항 · q = 복합 전극 용량밀도 · κ_eff = 복합 전극 유효 이온전도도 · t = 시간.  (t/(qκ_eff)) i² = [(ti/q)·(1/κ_eff)] × i — **ti/q = 반응대 앞면의 위치, i/q = 그 속도** [18] |
| eq 2 | **κ_eff = (ε/τ)·κ** | *"Incorporation of the volume fraction of the electrolyte ε and the tortuosity factor τ gives the effective conductivity of the composite electrode"* — **τ 정의** |
| eq 3 | V = U_c^θ − U_a^θ − R_o i − (1/(q_cκ_eff,c) + 1/(q_aκ_eff,a)) i² × t | 풀셀 (양극 · 음극 직렬).  방전 곡선 기울기 ∝ i² (원문 p.609 마지막 문장) |

- 물리 그림 (p.608–610): 고체 전해질은 Li⁺ 운반율 ≈ 1 → **농도 구배 없음** → 전극 안 리튬 수송은 옴 강하가 지배.  반응은 분리막 쪽부터 앞면 (reaction zone front) 으로 진행하고, 이온은 이미 반응한 두께 x = it/q 를 지나며 i·x/κ_eff 의 강하를 진다.  전자 쪽은 σ_eff ≫ κ_eff 라 강하 무시.
- 원전: Newman 그룹의 반응대 모형 [18] (*"valid for a system based on highly diffusive active materials"*, p.608) · 용량–율속 해석 [19].  **eq 1–4 의 유도는 SI 에 없다** — 본문 서술과 참고문헌에 위임.

### 4-2. eq 4 적합 → κ_eff → τ (p.610)

| 단계 | 내용 | 쪽 |
|---|---|---|
| ① 컷오프 용량식 | **C = t_d i = (1/i)·(1/(q_cκ_eff,cj) + 1/(q_aκ_eff,a))⁻¹·(U_c^θ − U_a^θ − V_cutoff − R_o i)** (eq 4) · t_d = V_cutoff 도달 시간 · j = 1 (SE1) · 2 (SE2) | p.610 |
| ② 저전류 극한 | i ≪ (U_c − U_a − V_cutoff)/R_o 이면 C ∝ 1/i — 그래서 **작은 전류 + 두꺼운 전극**이 입자 내 확산 영향을 줄이는 데 유리 | p.610 |
| ③ 적합 | Fig 3 (log C vs log i, L75–L600) 에 SE 계마다 eq 4 → X_j 추정.  큰 전류의 이탈 = 입자 내 확산 효과 | p.610 · Fig 3 |
| ④ 분배 | **τ_c1 = τ_c2** (SEM 형태 유사, Fig S6) → κ_eff,c1/κ_eff,c2 = κ₁/κ₂ → X₁ · X₂ 두 식으로 κ_eff,c1 · κ_eff,a 를 닫는다 (κ_eff,a 는 두 셀 공통 — 음극은 늘 SE3) | p.610 · SI p.8 |
| ⑤ τ | Eq 2 → τ = εκ/κ_eff (ε = 0.57 두 전극 모두) → Table 5 | p.610 |
| 원문 평 | *"although estimation of the tortuosity tends to be challenging due to the complex battery reactions taking place²⁰⁻²², a simplified electrochemical treatment … due to the absence of a concentration gradient allows this value to be determined relatively easily"* | p.610 |

- **τ_c1 = τ_c2 의 근거 (SI p.8)**: ① SEM 단면에서 SE1 · SE2 양극의 입자 분포 차이 없음 ② 큰 SE 입자가 τ 를 바꿀 수 있어 분말을 체로 거름 ③ *"thiophosphates exhibit similar elastic properties³⁶ and can be easily deformed by cold pressing, the electrode morphology would be comparable especially at high SE volumic fractions"*.
  - ⚠ [36] = Deng 2016 (정본 카드 `deng2016_elastic_superionic_electrolytes_dft`: LGPS E = 21.7 GPa · DFT 결정) 이고, 유리 75Li₂S–25P₂S₅ 는 Sakuda 카드 E = 24 GPa (실험) — 탄성은 비슷하다.  그러나 **σ₀ 를 냉간 펠릿으로 잡았기 때문에 "같은 τ" 가 성립한다** — 소결 · 열간 값으로 잡으면 같은 자료가 τ_c1 6.48 ↔ τ_c2 2.98 (Sakuda 0.34 교차 · 우리 산술, × 2.2) 을 준다 (§8-2 결정 4).

### 4-3. 임피던스 TLM (SI Eq S1–S5, SI p.9–10)

| 식 | 원문 | 뜻 · 비고 |
|---|---|---|
| Eq S1 | Z_elec = L_elec/((1/Z_i) + (1/Z_e)) × (1 + [2 + ((Z_e/Z_i) + (Z_e/Z_e))·cosh(L_elec√((Z_i+Z_e)/Z_CT))] / [L_elec√((Z_i+Z_e)/Z_CT)·sinh(L_elec√((Z_i+Z_e)/Z_CT))]) | 이온 · 전자 두 레일 TLM 의 해석해 [26].  ⚠ 인쇄본 분자 "(Z_e/Z_i) + (Z_e/Z_e)" — 일반 TLM 해 (두 레일) 는 (Z_i/Z_e + Z_e/Z_i) 다 (§10-1) |
| Eq S2 | Z_e = 1/(A·σ_eff) · Z_i = 1/(A·κ_eff) | 단위 길이당 레일 임피던스 |
| Eq S3 | Z_CT = Z_particle/(A·N) | N = 단위 부피당 요소 수 (값을 모르므로 적합) |
| Eq S4 | Z_FSW = (τ_d/C_diff)·(jωτ_d)^−0.5·coth(jωτ_d)^−0.5 | finite-space Warburg.  ⚠ 표준형은 coth[(jωτ_d)^+0.5] (§10-1) · **τ_d = 시간 상수 — tortuosity 아님 (기호 충돌)** |
| Eq S5 | τ_d = d²/D | d = 입경 (SEM) · D = 문헌값 |

- 경계조건: 분리막 R_sep 를 사이에 두고 음극 · 양극 TLM 직렬 (Fig 4d) — 전극마다 이온은 분리막 쪽 · 전자는 집전체 쪽 레일.  Z_particle = (R_CT ∥ CPE) + FSW 직렬의 병렬 묶음 (Fig 4e).

### 4-4. SE 합성 · 셀 제작 · 압력 이력 (SI §2, p.4–7)

| 단계 | 내용 | 쪽 |
|---|---|---|
| SE 합성 | SE1: Li₂S (99.98 %) · P₂S₅ (98 %) · GeS₂ (99.9 %) → ZrO₂ 볼 (⌀ 10 mm) 370 rpm 40 h → 550 °C 8 h.  SE2 · SE3: 같은 볼밀 (열처리 없음) | SI p.4–5 |
| 체거름 | 큰 SE 입자를 **5 µm 니켈 체**로 제거 (SE 입도 분포 미보고) | SI p.6 |
| 양극 혼합 | LiNbO₃ 코팅 LiCoO₂ (D5, Toda, **3–5 µm**) + SE1 또는 SE2 + 아세틸렌블랙 → **볼텍스 믹서 5 분** | SI p.6–7 |
| 음극 혼합 | 흑연 (≈ 10 µm, 구형) + SE3 → **마노 막자** (전단 → 흑연 변형) | SI p.7 · SI p.8 |
| 압밀 | 양극층 · 분리막 · 음극층 분말을 알루미나 실린더에서 함께 **500 MPa** | SI p.7 |
| 집전 · 운전압 | SS 집전체 10 MPa 로 접합 → SS 하우징 나사로 **50 MPa** [35] · 셀 지름 11.28 mm (1 cm²) | SI p.7 |
| 비교 | σ₀ 펠릿 420 MPa ↔ 복합체 500 MPa ↔ 운전 50 MPa — **압밀 이력이 셋 다 다르다** | SI p.6–7 |

### 4-5. 측정 프로토콜 (SI p.7)
- 충방전: 0.5 mA cm⁻² · 2.5–4.1 V.  율속: 4.1 V 까지 CC (0.5 mA cm⁻²) + CV (컷오프 0.005 mA cm⁻²) 충전 → 방전 전류를 바꿔 2.5 V 컷오프.  **모든 전기화학 시험 25 °C · Ar**.
- SEM: Ar 이온 밀링 단면 (E-3500, Hitachi) → JSM-6610A (JEOL).  **사이클 전** 전극 (SI p.8).

### 4-6. 시뮬레이션 · 입자 처리
- **입자 기반 시뮬레이션 없음** (DEM · MPM · FEM 아님).  모형은 1D 해석식 (eq 1–4) 과 등가회로 (TLM-FSW) 뿐 — 입자 처리 항목은 해당 없음.
- 입경 정보 (원문): LiCoO₂ 3–5 µm (SI p.6) · SE ≤ 5 µm 체 통과 (분포 없음) · 흑연 ≈ 10 µm 구형 (SI p.7) · 아세틸렌블랙 입경 없음.  ⇒ r_SE/r_AM ≲ 1 (우리 산술 — 우리 코퍼스 중앙 0.13 과 다른 영역).
- 형상 정보 (정성): LCO = 각진 경질 세라믹, 잘 분산 · 흑연 = 막자 전단으로 **변형되어 세로로 퍼짐** → 음극 τ ↑ 로 해석 (p.610 · Fig S6).  = 입자 **형상** 변화가 τ 를 올린다는 정성 증거 (강체구 DEM 이 못 그리는 쪽).

### 4-7. 기법 미니 용어집
- **반응대 (reaction zone) 모형**: 활물질 확산이 빠르면 반응이 좁은 앞면에 몰려 분리막 쪽에서 집전체 쪽으로 진행한다고 보는 모형 (Newman 그룹 [18]).  이온은 반응이 끝난 두께만큼 전해질상을 지나며 옴 강하를 진다.
- **ohmic limit (옴 한계)**: 농도 분극 없이 전해질상 저항만으로 과전압이 정해지는 극한.  용량 ∝ 1/i (log–log 기울기 −1).  액체 전해질의 **한계 전류 (농도 고갈)** 와 다른 기전 — 고체 SE 는 t_Li+ ≈ 1 이라 고갈이 없다.
- **율속 (rate capability) 자료**: 같은 충전 뒤 방전 전류를 바꿔 얻는 용량–전류 곡선.  이 논문의 τ 는 사이클 수가 아니라 이 자료에서 나온다.
- **tortuosity factor τ (이 논문)**: κ_eff = (ε/τ)κ 의 τ = 우리 tau2.  Bruggeman 은 τ = ε^−0.5 (κ_eff = ε^1.5 κ).
- **TLM (전송선 모형)**: 이온 레일 · 전자 레일 · 그 사이 계면 소자의 사다리 회로.  여기서는 κ_eff 를 고정한 정합 확인 도구.
- **FSW (finite-space Warburg)**: 유한 공간 (반사 경계) 확산 임피던스 — 활물질 입자 내 Li 확산.  τ_d = d²/D.
- **DC 분극 (이온 차단 셀)**: 이온이 못 지나는 전극으로 막고 직류 전압을 걸어 전자 전도도만 재는 법 (σ_eff 0.3 · 0.7 S cm⁻¹).
- **냉간 압분 펠릿 ↔ 소결 펠릿**: 같은 분말을 상온 가압만 한 시료 (입계 · 접촉 · 기공 포함) ↔ 열처리로 치밀화한 시료.  LGPS 3.2 ↔ 8.3 mS cm⁻¹.

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| GA (p.607) | 600 µm 셀 사진 + 굽은 이온 경로 모식 (빨간 화살표) | 논문 요지 |
| **1** (p.608) | (a) 셀 모식 — 양극 L_c (LCO + SE1/SE2) · 분리막 L_s ≈ 100 µm (SE3) · 음극 L_a (흑연 + SE3) · (b)(c) L100/L300/L600 충방전 (0.5 mA cm⁻², SE1) · L600 10 사이클 (삽도 1st→10th) | ⚠ **그림 안 패널 표지 (b)(c) 가 캡션 · 본문과 뒤바뀌어 있다** (§10-1) · 15.7 mAh cm⁻² 의 근거 그림 |
| **2** (p.609) | (a) L600 · L300 충방전 vs 비용량 + 미분 (ΔV/ΔC) · (b) L600 방전 i = 6 · 12 · 20 mA cm⁻² + 삽도 (기울기 vs i², 0–100 mA cm⁻²) · (c) i = 12 에서 L100 · L200 · L300 · L600 · (d) L300 에서 SE1 vs SE2 | ★ 옴 한계의 세 증거 (기울기 ∝ i² · 두께 무관 · SE 전도도 의존) · 삽도 기울기 ↔ Table 5 의 15–25 % 어긋남 (§3-7) |
| **3** (p.610) | log C vs log i, L75–L600, SE1 (○) · SE2 (■) + eq 4 적합 (빨강 · 파랑) | ★★ **τ 추출의 원자료** — 높은 전류에서 두께 무관 · 기울기 −1 |
| **4** (p.611) | 4.1 V 임피던스: (a) Nyquist (L300 ▲ · L600 ○ + 적합, 고주파 삽도) · (b)(c) Bode · (d)(e) TLM 등가회로 (Z_elec,a · R_sep · Z_elec,c · Z_CT = Z_particle/A · (R_CT∥CPE)+FSW) | κ_eff 고정 정합 — 독립 검정 아님 · TLM 경계조건 그림 (τ_e 계열의 틀) |
| SI Fig S1 (SI p.2) | LCO/흑연 ASSB 용량 적재 문헌 비교 막대 (137 · 370 mAh g⁻¹ 로 계산) | 15.8 의 근거 (Table 3 의 15.7 과 다름) |
| SI Fig S2 (SI p.3) | 에너지밀도 · 비에너지 vs L_c | 계산값 (집전체 가정) |
| SI Fig S3–S5 (SI p.4–6) | SE1 XRD (LGPS + β-Li₃PS₄ ▼) · SE2 · SE3 비정질 | SE1 의 2차상 = 소결 8.3 이 문헌보다 낮은 이유 |
| **SI Fig S6** (SI p.8) | 단면 SEM: (a) SE1 양극 (b) SE2 양극 (c) SE3 + 흑연 음극 (눈금 10 µm) | **τ_c1 = τ_c2 가정의 유일한 근거** · 흑연 변형 · SE 영역 crack (정성) |
| **SI Fig S7** (SI p.11) | eq 4 투영: (i) Bruggeman τ (ii) κ = 10 mS cm⁻¹ — 실측 율속 위에 겹침 | "×2" · "15.8 @ 30" 의 근거 — 후자는 eq 4 재계산과 어긋남 (§3-9) |
| SI Table S1 (SI p.9) | TLM-FSW 매개변수 (L300 · L600) | 각주 a/b 뒤바뀜 · N 의 두께 비례 (§3-8) |

- **크롭 후보 (메인 순서대로 · 캡션 대조)**: **Fig 3** > **Table 4 + Table 5** (p.610) > **Fig 2** > **Table 2 + Table 3** (p.608–609) > **Fig 1** (패널 표지 주의) > **SI Fig S7** > **SI Fig S6** > Fig 4 > SI Table S1.

## 6. Post-processing ★
- **무엇**: 율속 곡선 (전류별 방전) → 컷오프 용량 C(i) → log–log 그림 (Fig 3) → eq 4 비선형 적합 (SE 계별 X_j) → τ_c1 = τ_c2 로 분배 → Eq 2 로 τ.  보조: 방전 곡선 기울기 vs i² (Fig 2b 삽도) · TLM-FSW 등가회로 시뮬 (κ_eff 고정 · R_sep · R_CT · CPE · N 적합) · eq 4 투영 (Fig S7).
- **도구**: 원문에 적합 소프트웨어 · 오차 처리 · 반복 셀 수 **미기재** [미확인].  Fig 2b 삽도의 오차막대 정의도 없다.
- **수치화 · 플롯**: 용량을 **C cm⁻² (쿨롱)** 으로 그린다 (Fig 3 · Fig S7 — mAh cm⁻² × 3.6).  적합한 X_j 숫자 · 적합 범위 (어느 전류부터) 는 적혀 있지 않다 → Table 5 가 유일한 수치 출력.
- **기공 회계 없음**: ε (Table 2) · q (Table 4) · 두께 (Table 3) 셋 다 기공 0 의 명목값이다.  void · crack 효과는 정의상 τ 안에 들어간다 (원문도 그렇게 해석, p.610).

## § τ 정의 대조 — 우리 규약 매핑

> 우리 규약 = 메인 리포 CLAUDE.md ★★ τ 명명 규약 (1저자 비준 10-03).  'tortuosity factor' 는 τ² (`tau2`) 에만 쓴다.

| 원문 기호 (쪽) | 원문 정의식 | 원문 이름 | 정규화 (어느 부피 · 어느 단면 · 어느 σ₀) | 우리 다섯 양 중 | 환산 · 비고 |
|---|---|---|---|---|---|
| **κ** (Table 1, p.608 · SI p.4–6) | 펠릿 임피던스 | ionic conductivity (of the solid electrolyte) | **냉간 압분 펠릿** 420 MPa · 25 °C (LGPS 3.2 · 유리 0.28 · LiI 유리 1.2 mS cm⁻¹) | **σ₀** | 우리 망 σ₀ = 3.0 (LPSCl 펠릿값, `CL-91`) — 숫자가 비슷한 것은 우연 (다른 재료) |
| **κ_eff** (eq 1–4, Table 5) | eq 4 적합의 곱 q·κ_eff ÷ q_치밀 | effective ionic conductivity of the composite electrode | 전극 단면 · **치밀 명목 두께 (q 치밀값)** = "치밀 등가" σ_eff | σ_eff (망 `sigma_full` 의 차원값) | 상자 기준 = κ_eff/(1−p) (p 미측정) |
| κ_eff/κ (Eq 2 의 ε/τ, 이름 없음) | ε/τ | — | 위 둘의 비 | **f** (`f_ion_<mode>`) | 0.228 (SE1) · 0.232 (SE2) · 0.175 (음극) (우리 산술) · 상자 기준 f/(1−p) |
| **τ** (Eq 2, p.609) | **ε·κ/κ_eff** | **"tortuosity factor"** (초록 · p.609 · p.611) | **ε = 공칭 고체 기준 SE 분율 0.57** (기공 0) · **σ₀ = 냉간 펠릿** · **q 치밀** | **tau2** (`tau2_ion_<mode>`) — conventional (관통 DC) | ⚠ 상자 기준 τ_box = τ(1−p)² · 기준 상태 = 냉간 펠릿 ≡ 1 → 우리 T 와 맞대려면 결정 4 의 ÷ T_pure,ours · 제곱하지 말 것 |
| "Bruggeman tortuosity factor" (p.611 · SI p.11) | **τ = ε^−0.5** | — | ε 0.57 → 1.32 | T_B = φ^−½ (Landesfeind α 0.5 관례 = T 지수) | = COMSOL Bruggeman τ_F = ε_p^(−1/2) (메모 v2 §1, COMSOL p.377) · f 로는 ε^1.5 |
| (√τ) | 보고 없음 | — | — | **tau** (`tau_ion_<mode>`) — 파생만 | 1.57 · 1.82 (우리 산술) |
| (τ_geo) | 없음 | — | — | **τ_geo** — 해당 없음 | "voids and cracks … interference of ion transfer" (p.610) 는 정성 |
| (τ_e) | 없음 — TLM 은 κ_eff 고정 | — | — | **τ_e** — 해당 없음 | 임피던스 경로로 τ 를 따로 뽑지 않았다 |
| **τ_d** (SI Eq S4–S5) | d²/D | characteristic diffusion time constant | — | **기호 충돌** — tortuosity 아님 | LCO 5000 s · 흑연 50 s (Table S1 값, 우리 산술) |
| ε (Eq 2 · Table 2) | wt% ÷ ρ 정규화 | volume fraction of the electrolyte | 기공 0 · 아세틸렌블랙 4.8 vol% 를 고체에 포함 | ≈ φ_SE — 단 우리 φ = 상자 기준 구합 (기공 포함 분모) → ε ≥ φ_true | 액체 문헌의 ε (= 기공 = 전해질) 와 "전해질상 분율" 이라는 뜻은 같고 기공을 세지 않는다 |
| N_M | 보고 없음 | — | — | 1/f | τ/ε = 4.33 · 5.82 (우리 산술) |

**σ₀ 기준**: 같은 SE 분말의 **냉간 압분 펠릿** (420 MPa · 25 °C · 측정 중 가압 미기재) — 순수 SE 펠릿을 τ ≡ 1 에 두는 관례 (Minnmann · Kaiser · Hlushkou · Froboese 와 같은 부류).
복합체는 500 MPa 압밀 · 50 MPa 운전이라 **펠릿과 압밀 이력이 다르다**.  같은 LGPS 의 소결 펠릿 (8.3) 을 σ₀ 로 쓰면 τ 가 2.6 배 커진다 — 기준 상태가 수치를 정한다는 실측 한 쌍.

**환산 사슬 (한 줄로)**:
```
f        = κ_eff/κ              = ε/τ                          (Eq 2)   — 0.228 (SE1) · 0.232 (SE2) · 0.175 (음극)
τ        = ε·κ/κ_eff            ↔ tau2 (꼴) — ε 고체 기준 · κ 냉간 펠릿 · κ_eff 는 치밀 q 와의 곱에서 나온 '치밀 등가'
상자 기준 (기공 p, 미측정):     ε_box = ε(1−p) ;  κ_eff,box = κ_eff/(1−p) ;  τ_box = τ·(1−p)²
τ/τ_pellet = 1 (냉간 펠릿)      ↔ 우리 T ÷ T_pure,ours (결정 4) 와 맞대야 같은 기준
Bruggeman: τ = ε^−0.5  ⇔  κ_eff = ε^1.5 κ   (p.611) = COMSOL τ_F = ε_p^(−1/2)
N_M = τ/ε = κ/κ_eff = 4.33 (양극) · 5.82 (음극)
```

**판정**:
1. 이 논문의 τ 는 **우리 tau2 와 같은 꼴 · 같은 관통 (DC) 경계조건 부류**다.  sink 가 집전체 쪽 띠가 아니라 **전극 안을 움직이는 반응 앞면**이라는 점이 다르다 (반응한 두께만 관통).
2. **원문 이름 "tortuosity factor" 가 Tjaden 규약 (tortuosity factor = τ²) 과 맞는다** — Minnmann 2021 과 함께 "factor" 낱말과 tau2 꼴이 일치하는 실험 원문이다 (Kaiser · Hlushkou · Froboese 는 "factor" 없음).  기호는 다르다: 같은 양을 Minnmann 은 **τ²**, 이 논문은 **τ** 로 적는다 — 기호로 제곱 여부를 판정하지 말 것.
3. Eq 2 = COMSOL f_e = ε_p/τ_F 꼴이고 Bruggeman 식도 COMSOL 과 같다 → 이 τ 숫자가 들어갈 자리는 τ_F 칸이고, **σ₀ 짝은 냉간 펠릿 κ · ε 짝은 고체 기준 0.57 · 두께 짝은 치밀 명목값**이다 — 셋 중 하나만 바꿔도 같은 κ_eff 가 재현되지 않는다 (결정 5).
4. τ_e 는 이 논문에 없다 (임피던스는 κ_eff 고정).

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md` (⚠ 이 브랜치에서는 값 자리표시 상태 — 우리 수치는 메모 v2 `docs/reviews/tau_conventions_judgment_v2_20261003.md` 의 유도값으로 적는다)

| 항목 | 이 논문 | 우리 | 같음 / 다름 · 이유 |
|---|---|---|---|
| 역할 (frame[5]) | 수송 절반의 **실험** (κ_eff · τ · 율속 · 10 사이클) — 기공 · 입도 분포 · 접촉 면적 · 역학 수치 없음 | DEM 접촉망 T (conventional) · STEP3 복셀 T (CONTACT_FREE 가지) · MPM 형상 | 이 논문은 수송 쪽만 가진다.  압밀 물리 (기공 · 형상) 는 SEM 정성뿐 |
| frame[4] | 실험 — 원칙적으로 독립 보정 앵커 후보 | 각 모델을 실험에 따로 보정 | ⛔ 재료 · 탄소 · 기공 미측정 · 조성 하나라 **이 값으로 우리 모델을 맞추지 않는다** |
| SE | LGPS (결정, 소결 단계 · β-Li₃PS₄ 2차상) 3.2 / 75Li₂S–25P₂S₅ 유리 0.28 / 음극 LiI 유리 1.2 mS cm⁻¹ (냉간 펠릿) | LPSCl argyrodite, 망 σ₀ 3.0 (펠릿값) | 다른 재료.  유리 · 결정의 냉간 ↔ 치밀 인자가 다르다 (§3-1) |
| AM | LiNbO₃ 코팅 LiCoO₂ 3–5 µm (단일 입경 · 각진 입자) | NMC811 bimodal (강체구, E 140 GPa) | 다름 |
| 탄소 | 아세틸렌블랙 4.8 vol% | DEM 망에 탄소 없음 | 다름 — 우리 T 는 탄소 차단이 없어 **과소** 방향 |
| 입경비 | SE ≤ 5 µm 체 · LCO 3–5 µm → r_SE/r_AM ≲ 1 | 중앙 ≈ 0.13 (메모 v2 §3-3) | 다른 미세구조 영역 (메모 결론 ④ 와 같은 교란) |
| 기공 | 미측정 · ε · q · 두께 모두 기공 0 명목 | ε_sphere 명시 (φ 0.613 띠 중앙 4.7 % · 0.536 띠 6.1 % — 메모 v2 §3-3) | 장부 차 **(1−p)²** |
| 압밀 · 측정 상태 | 500 MPa 3 층 동시 → 운전 · 측정 50 MPa (하우징) | 300 MPa 계열 · 최대 압밀 기하 (판 고정 완화) | 비슷한 범위.  실험은 되튐 뒤 50 MPa 하 |
| τ 정의 | τ = εκ/κ_eff (Eq 2) "tortuosity factor" | T = φσ₀/σ_full (`tau2`) | **같은 꼴** — φ 장부 · 기준 상태가 다름 |
| 경계조건 | DC 관통 · 반응 앞면 sink (옴 한계) | 두 띠 Dirichlet 관통 | 같은 부류 (conventional) · sink 위치 다름 |
| 값 (판정 없이) | τ_c 2.47 @ ε 0.57 (고체) · 상자 환산 2.00–1.58 @ φ 0.51–0.46 (p 0.10–0.20 가정) · τ_a 3.32 | T_H 중앙 2.65 @ φ 0.613 띠 · 2.73 @ 0.536 · 3.20 @ 0.444 (1세대 협착식 · 기준 상태 미보정 · 위 두 띠는 과압축 영역) | **비율을 내지 않는다** — φ 장부 · 재료 · 탄소 · 기준 상태가 다 다르다 |
| Bruggeman 배수 | 1.86 (양극) · 2.51 (음극) (고체 기준 ε, 우리 산술) | H 중앙 3.40 (IQR 2.54–6.71) (메모 v2 §3-5) | 축은 같다 (T ÷ φ^−½) — 값 대조는 위와 같은 이유로 하지 않는다 |
| 전자 쪽 | σ_eff 0.3 (양극, AB 3 wt%) · 0.7 S cm⁻¹ (흑연 음극) — DC 분극 | σ_e Stage 22.5 (형태식) · STEP3 σ_e (VGCF) | 옴 한계 전제 (σ_e/κ_eff 411 · 3333) 는 우리 STEP4 실측 "2C 옴강하 전자 0.01–0.03 mV ↔ 이온 84–90 mV" (CLAUDE.md 07-21) 와 같은 방향 — 후막 율속은 이온망이 정한다 |
| 형상 | 흑연이 막자 전단으로 변형 · 세로 확산 → τ_a ↑ (정성) | DEM = 강체구 (형상 불변) · MPM = SE 소성 (AM 고정) | AM 형상 변화가 τ 를 올리는 경로는 우리 두 모델 모두에 없다 |

- **방법 artifact 와 실제 차이의 구분**: 이 표의 어느 행도 "모델 오차 배수" 를 주지 않는다.  ① 강체구 DEM vs 실물 (유리 SE 의 흐름 · 흑연 변형) ② 재료 이전 (LGPS/유리 ≠ LPSCl · LCO ≠ NMC811) ③ 탄소 유무 ④ φ 장부 (고체 기준 ε + 치밀 q vs 상자 기준 구합) ⑤ 실험 쪽 방법 불확도 (≈ 20–25 %, §3-7) — 다섯이 겹친다.
- **frame[5]** — 이 논문이 가진 반쪽 = 실험 수송 (κ_eff · τ · 율속).  없는 반쪽 = 미세구조 수치 (기공 · PSD · 접촉 면적) · 역학.  우리 DEM 이 그 반쪽을 줄 수 있지만 재료가 달라 연결이 끊긴다.

## 8. 적용 인사이트 (내 연구에 어떻게) — 이 묶음이 닫으려는 것

### 8-0. ★ 닫는 것: **EIS 와 독립인 사이클 기반 τ** (메모 v2 §8-2 · 닫는 항목 "절대 대조 교차")

| 물음 | 이 논문 (쪽) | 판정 |
|---|---|---|
| 용량–전류 자료에서 τ 를 뽑는 식 | eq 1 (반쪽 전지 옴 한계) → eq 3 (풀셀) → **eq 4** (컷오프 용량) → Eq 2 (τ = εκ/κ_eff) (p.609–610) | 닫힘 — 식 · 단위 재현 (§3-5 · C 단위 C cm⁻²) |
| 가정 — 이온 수송 지배 | σ_eff ≫ κ_eff (0.3 · 0.7 S cm⁻¹ vs 0.73 · 0.21 mS cm⁻¹) · 직선 방전 곡선 · 기울기 ∝ i² (p.608–610) | 성립 (자료와 정합) |
| 가정 — 한계 전류 | **한계 전류가 아니다** — t_Li+ ≈ 1 → 농도 구배 없음 → **옴 한계** (C ∝ 1/i, 기울기 −1) (p.610) | "한계 전류" 로 읽지 말 것 — 이 논문의 기전은 옴 한계다 (우리 해석) |
| 가정 — 두께 | 추출식에 두께가 없다 (높은 전류 용량은 두께 무관) · q = C/L 로만 들어가고 **q = 치밀값** (Table 4) | 두께는 정확히 몰라도 되지만 **기공은 (1−p)² 로 들어온다** |
| 가정 — SE σ₀ | 냉간 압분 펠릿 (420 MPa · 25 °C · SI p.6) | 펠릿 ≡ 1 관례 |
| 가정 — 두 SE 공유 τ | τ_c1 = τ_c2 (SEM 유사 · 탄성 유사 · 체거름, SI p.8) | **풀이 조건** — 시험된 것이 아니다 |
| 값 | τ_c 2.47 · τ_a 3.32 · κ_eff 0.73 / 0.065 / 0.21 mS cm⁻¹ (Table 5) | stated · Eq 2 로 ≤ 2 % 재현 |
| 두 SE 비교 | SE1 (3.2) 양극 X₁⁻¹ 5.11 ↔ SE2 (0.28) 19.8 V s⁻¹ cm⁴ A⁻² (우리 산술) · L300 @ 12 mA cm⁻² 용량 ≈ 6.6 ↔ ≈ 2.0 mAh cm⁻² (판독) | SE 전도도가 율속을 정한다 (두께 아님) |
| 600 µm · 15.7 mAh cm⁻² | 치밀 명목 두께 · 이론 (양극 제한) 용량 (137 mAh g⁻¹) · 실측 방전 93 % @ 0.5 mA cm⁻² · 88 % @ 6 · 25 °C · 50 MPa (p.607–608 · SI p.2 · p.7) | 초록의 "15.7 achieved" 는 **이론 적재**다 — 실측 방전은 ≈ 14.6 (우리 산술) |
| τ 인가 τ² 인가 | **τ² 꼴 (tortuosity factor)** — 원문은 τ 로 적는다 | **tau2** |
| ε 정규화 | 한다 — ε = 0.57 공칭 고체 기준 (기공 0) | φ 장부 다름 |
| σ₀ 기준 | 순수 SE **냉간 펠릿** (치밀 · 결정립 값 아님) | 기준 상태 = Minnmann 과 같은 부류 · 우리와 다름 (결정 4) |
| EIS 와 독립인가 | 추출 사슬은 **율속 (DC)** 만 쓴다 · 단 R_o (고주파 저항, 8 Ω cm²) 는 측정법 미기재 [미확인] — 임피던스 고주파 값이면 완전 독립은 아니다 · EIS (Fig 4) 는 κ_eff 고정 정합 확인 (p.611 · SI p.9–10) | **대체로 독립** — R_o 출처만 남는다 |
| "사이클 기반" 인가 | 아니다 — **율속 (방전 용량–전류) 기반**.  사이클 자료는 10 회 유지 (Fig 1) 뿐 | 메모 v2 정정 후보 (§10-3) |
| **우리 T 와 절대 대조할 수 있는 조건** | ① 같은 양: tau2 conventional ✓ ② φ 장부: 기공 p 실측 (또는 두께 실측) → τ(1−p)² 환산 ✗ (없음) ③ 기준 상태: 우리 T ÷ T_pure,ours (순수 SE 게이트) — 보류 (결정 4 런 전) ④ 같은 계: LGPS/유리 + LCO 3–5 µm (r_SE/r_AM ≲ 1) + AB ✗ ⑤ 방법 띠 ± 20–25 % (§3-7) 를 판정선에 반영 ⑥ 압밀 상태: 500 → 50 MPa 되튐 ↔ 우리 최대 압밀 기하 | **② · ④ 가 막는다 → 값 교차 불가 · 정의 교차만** |

### 8-1. 두 실험 경로 맞대기 (Kato 율속 DC ↔ Minnmann EIS τ², SI Table S2 — 메모 v2 §3-3 값 · ln 보간 · 우리 산술 · 추세 전용)

| Kato 점 · φ 장부 | φ | Kato τ | Minnmann T (보간) | Kato ÷ Minnmann | 우리 T_H 띠 중앙 (보간 · 1세대 · 미정규화) |
|---|---|---|---|---|---|
| 공칭 그대로 (고체 기준 ε) | 0.570 | 2.47 | 2.84 | 0.87 | 2.69 |
| p = 0.10 · (1−p)² | 0.513 | 2.00 | 3.47 | 0.58 | 2.84 |
| p = 0.14 (Minnmann 평균 기공을 빌림) · (1−p)² | 0.490 | 1.83 | 3.71 | 0.49 | 2.95 |
| p = 0.14 · (1−p)¹ (ε 만 고침) | 0.490 | 2.12 | 3.71 | 0.57 | 2.95 |
| p = 0.20 · (1−p)² | 0.456 | 1.58 | 4.11 | 0.38 | 3.13 |
| 음극 (흑연 + LiI 유리) 공칭 | 0.570 | 3.32 | 2.84 | 1.17 | 2.69 |

- **기공 가정 하나가 비를 0.87 ↔ 0.38 로 흔든다.**  Minnmann 의 φ 는 기공 14 % 를 넣은 상자 기준이라 첫 행은 장부가 섞인 비교다 — 같은 장부 (아래 행들) 에서 Kato 양극은 Minnmann 보다 **≈ 1.7–2.6 배 낮다**.
  재료 (LGPS/유리 + LCO ↔ LPSCl + NCM622) · 입경비 (둘 다 ≈ 1 근처 — 우리 0.13 과 다른 영역) · 탄소 (AB ↔ 없음) · 방법 (DC 반응 앞면 ↔ EIS 관통) 이 한꺼번에 다르므로 이 비를 **"방법 차"** 로 읽지 않는다.
- 우리 열은 판정 없이 둔다 — 위 두 띠 (φ ≥ 0.54) 는 메모 v2 의 과압축 영역이고 기준 상태 보정 (× 0.5–0.7 추정) 전이다.  "일치 · 정합" 낱말 금지 (결정 4).
- Y. Kato 가 함께한 두 실험 경로 (Kaiser EIS · 이 논문 율속) 도 재료 (LTO + LPSI 유리 · LCO + LGPS) 가 달라 같은 축의 반복 측정이 아니다.

### 8-2. 결정별 인사이트 (메모 v2 §0-2 결정 번호)
- ① **결정 4 (순수 SE 게이트 · σ₀ 기준 상태)** — 이 논문은 **펠릿 ≡ 1 관례의 다섯째 원문 사례**이고, τ 를 보고한 같은 논문 안에서 **같은 SE 의 냉간 ↔ 소결 값 한 쌍 (LGPS 3.2 ↔ 8.3, × 2.6)** 을 준다 (SI p.4).  같은 자료가 σ₀ 에 따라 τ_c1 2.47 ↔ 6.48 이 된다.
  더 깊은 함의: 원문의 τ_c1 = τ_c2 (두 SE 공유) 는 **펠릿 정규화 안에서만 서는 문장**이다 — 유리는 냉간 ≈ 치밀 (Sakuda 카드 0.31 ↔ 0.34) 이라 치밀 정규화로 바꾸면 같은 자료가 τ_c1 6.48 ↔ τ_c2 2.98 (× 2.2, 교차 산술) 로 갈린다.
  ⇒ "같은 미세구조 = 같은 τ" 는 기준 상태를 정해야 뜻이 생긴다.  우리 T (펠릿 σ₀ 위 SE–SE Holm) 를 실험 τ 와 맞대려면 순수 SE 망 정규화가 유일한 같은 기준이라는 판단이 **강해진다**.  **권고 불변.**
  보강 제안: 사전등록 ⓑ ε 장부 옆에 **두께 · q 장부** (치밀 명목 / 실측) 를 두고 환산 지수를 적는다 — Kaiser · Hlushkou (두께 실측) = (1−p)¹ · Kato (q 치밀) = (1−p)².  ⓓ 압밀 · 측정 상태 열에 Kato = 펠릿 420 MPa ↔ 복합체 500 MPa → 50 MPa.
- ② **결정 5 (이름 · COMSOL 표기)** — 원문이 **"tortuosity factor"** 를 Eq 2 κ_eff = (ε/τ)κ 에 붙이고 Bruggeman 을 **τ = ε^−0.5** 로 적는다 — COMSOL f_e = ε_p/τ_F · Bruggeman τ_F = ε_p^(−1/2) (메모 v2 §1) 와 **기호 · 꼴이 같다** → COMSOL τ_F 칸 = tau2 판단을 지지한다.  **권고 불변.**
  한정어 보강: τ_F 숫자는 **σ₀ 짝 (냉간 펠릿) · ε 짝 (고체 기준 / 상자 기준) · 두께 짝 (치밀 명목 / 실측)** 셋과 함께 넘긴다 — 이 논문 값을 상자 기준 ε 와 짝지으면 COMSOL 이 κ_eff 를 (1−p)² 만큼 틀리게 재현한다.
- ③ **결정 13 (τ_e)** — 이 논문의 τ 는 **DC 관통 (반응 앞면)** 부류이고 임피던스 TLM 은 κ_eff 를 고정한 채 R_CT · CPE · N · R_sep 만 맞췄다 → **τ_e 를 따로 재지 않았다**.  τ_e ↔ conventional 비교 자료로 쓸 수 없다.  **권고 불변** ("부호 불정" 유지).
  보강: 실험 τ 의 **방법 내부 불확도** 하나 — 같은 셀의 V–t 기울기 경로와 eq 4 용량 경로가 X⁻¹ 를 4.0–4.3 ↔ 5.11 로 준다 (≈ 20–25 %, §3-7).  결정 4 의 판정선을 등록할 때 실험 쪽 띠로 넣는다.
- ④ **결정 15 (키 이름)** — Y. Kato 가 저자로 들어간 같은 해 세 논문이 같은 양 (ε·σ₀/σ_eff) 을 "tortuosity factor τ" (이 논문) · "effective tortuosity τ_eff" (Kaiser) · "ionic conductivity-based tortuosity τ_cond" (Hlushkou) 로 불렀고, Minnmann 2021 은 같은 양을 "tortuosity factor τ²" 로 적는다 → 이름 · 기호가 아니라 **식으로 판정**한다는 원칙의 사례가 늘었다.  **권고 불변.**
- ⑤ **결정 11 (CF · 협착 비)** — 해당 없음.  원문의 "voids and cracks … interference" (p.610) 는 정성이고 경로 · 협착 분리 수치가 없다.
- ⑥ (선택 · STEP4 해석해 기준선) — eq 4 는 **옴 한계의 율속 상한을 닫힌 꼴로** 준다: C(i) = X·(ΔU − R_o i)/i, X = q·κ_eff (반쪽 전지면 음극 항 없음).  우리 STEP4 (BV + 입자 확산) 가 같은 κ_eff 에서 이 값 아래에 있는지 보는 **패리티 검산**으로 쓸 수 있다.  ⚠ 전제 (좁은 반응 앞면 · 상수 OCV · 비옴 과전압 0) 가 이 논문 자료에서도 ≈ 0.2–0.4 V 어긋난다 (§3-7) — 상한으로만.

## 9. 인용 가능 문장 (deck/paper용)
- "Kato et al. extracted an electrode tortuosity factor τ from rate–capacity data of thick all-solid-state cells using the ohmic-limit (reaction-zone) model, defining κ_eff = (ε/τ)κ with ε the nominal, porosity-free volume fraction of the solid electrolyte and κ the conductivity of a cold-pressed electrolyte pellet (J. Phys. Chem. Lett. 9 (2018) 607)."
- "For LiNbO₃-coated LiCoO₂ cathodes (ε = 0.57) the reported τ was 2.47 — obtained under the assumption that the Li₁₀GeP₂S₁₂ and 75Li₂S–25P₂S₅-glass cathodes share the same tortuosity factor — and 3.32 for the graphite anode."
- "Because the volumetric capacities used in the fit correspond to fully dense electrodes and the porosity was not measured, converting these values to a total-volume basis requires a factor (1 − p)², which is unknown; they constrain the definition of τ but cannot serve as an absolute benchmark."
- "The same Li₁₀GeP₂S₁₂ powder showed 3.2 mS cm⁻¹ as a cold-pressed pellet and 8.3 mS cm⁻¹ when sintered; the choice of reference conductivity alone changes the extracted τ by a factor of 2.6."

## 10. 주의/한계 (over-claim 방지)
- ⚠ **재료 전이**: SE = **LGPS · 75Li₂S–25P₂S₅ 유리 · LiI–Li₂S–P₂S₅ 유리** ≠ 우리 LPSCl · AM = **LiCoO₂ 3–5 µm** ≠ NMC811 bimodal · **아세틸렌블랙 4.8 vol%** (우리 DEM 망에 없음).  수치를 우리 계로 옮기지 않는다.
- ⚠ **기공 미측정 · φ 장부** — ε · q · 두께가 모두 기공 0 명목값이다.  상자 기준 환산은 τ(1−p)² 인데 p 를 모른다 (p 0.10–0.20 이면 양극 2.00–1.58).  "τ 2.47" 을 기공 포함 φ 의 곡선 위에 그대로 놓지 말 것.
- ⚠ **τ_c1 = τ_c2 는 가정** — 두 SE 의 κ_eff 비가 κ 비와 맞는 것 (11.2 ↔ 11.4) 은 가정이 강제한 결과다.  "두 SE 의 형태가 같음을 보였다" 로 인용하지 말 것.
- ⚠ **방법 내부 어긋남 ≈ 20–25 %** — 기울기 경로 (X⁻¹ 4.0–4.3) ↔ 용량 경로 (5.11).  비옴 과전압을 τ 가 흡수했을 수 있다 (우리 해석).  적합 범위 · 오차 · 반복 셀 수 미기재.
- ⚠ **"고확산 활물질" 전제** — Table S1 값으로 τ_d(LCO) ≈ 1.4 h 는 적합 창의 방전 시간 (0.2–2.3 h) 과 같은 크기 (우리 산술).
- ⚠ **σ₀ 기준 상태** — 냉간 펠릿 (420 MPa · 측정 중 가압 미기재) ≠ 복합체 (500 MPa → 50 MPa).  LGPS 는 소결로 2.6 배.
- ⚠ **"15.7 mAh cm⁻² achieved" (초록)** 는 이론 적재다 — 실측 방전은 93 % (≈ 14.6, 우리 산술) · 6 mA cm⁻² 에서 13.9.
- ⚠ **R_o 출처 미기재** — "EIS 와 독립" 은 R_o 가 임피던스 고주파 값이 아닐 때만 엄밀하다.
- ⚠ **임피던스 "good fit"** 은 κ_eff 의 독립 검정이 아니다 (자유 매개변수 넷 · L600 저주파 이탈 판독).
- ⚠ **Fig S7 투영 (×2 · 15.8 @ 30)** 은 eq 4 계산이지 측정이 아니다 — 후자는 eq 4 재계산과 어긋난다 (아래 10-1 ⑨).
- ⚠ 시뮬레이션 없음 — DEM · MPM 어느 쪽의 검증도 아니다 (frame[4]: 실험 앵커 후보일 뿐, 이 계에서는 연결 조건 미충족).

### 10-1. 원문 오식 · 불일치 (그대로 두고 표지만)
1. **Figure 1 패널 표지** (p.608): 그림 안 위쪽 패널 (L100/L300/L600 충방전) 이 "(c)", 아래쪽 (L600 10 사이클) 이 "(b)" 로 찍혀 있다 — 캡션 · 본문은 1b = 충방전 · 1c = 사이클.  표지 뒤바뀜.
2. **15.7 ↔ 15.8 mAh cm⁻²**: 초록 (p.607) · Table 3 (p.609) = 15.7 / 본문 p.611–612 · SI p.2 = 15.8.  137 mAh g⁻¹ × 115.4 mg cm⁻² = 15.81 (우리 산술).  Table 3 용량 열은 L75 (2.00 ↔ 1.99) · L300 (7.93 ↔ 7.90) · L600 (15.7 ↔ 15.81) 에서도 0.3–0.7 % 어긋난다.
3. **Table S1 각주 a/b** (SI p.9): σ_eff 에 a (*"Obtained from rate-capacity characteristics"*) · κ_eff 에 b (*"Obtained by DC polarization"*) — SI 본문 (p.9–10) 은 전자 = DC 분극 · 이온 = 율속.  각주 뒤바뀜.
4. **Eq S1 분자** (SI p.9): "(Z_e/Z_i) + (Z_e/Z_e)" — 두 번째 항이 1 이 된다.  일반 두 레일 TLM 해는 (Z_i/Z_e + Z_e/Z_i).  원문 계산에 무엇을 썼는지 [미확인].
5. **Eq S4** (SI p.10): "coth(jωτ_d)^−0.5" — 표준 finite-space Warburg 는 coth[(jωτ_d)^+0.5].  인쇄 의심.
6. **SI p.10** *"The simulated result is shown in Figure S7"* — 임피던스 시뮬은 본문 Fig 4 이고 Fig S7 은 율속 투영이다.  교차 참조 오류.
7. **기울기 ↔ Table 5** (p.609–610): 본문 기울기 −0.52 / −2.07 / −6.22 V h⁻¹ 와 삽도 (≈ 4.2–4.5 V s⁻¹ cm⁴ A⁻², 판독) 는 X⁻¹ ≈ 4.0–4.5 를, Table 4 · 5 는 5.11 을 준다 — "corresponds" 는 15–25 % 안에서만 (§3-7).  기울기 단위는 본문에 없다 (그림 축으로 V h⁻¹).
8. **Table 5 반올림**: κ_eff,c1 0.73 → τ 2.50 (보고 2.47) · κ_eff,a 0.21 → 3.26 (보고 3.32, 0.206 의 반올림) — ≤ 2 %.
9. **"15.8 mAh cm⁻² at 30 mA cm⁻² with 10 mS cm⁻¹"** (p.611–612): eq 4 재계산 (τ 2.47 · 3.32 · κ 10 mS cm⁻¹ 양 전극) = 12.9 mAh cm⁻² (R_o 8) · 15.1 (R_o 1) @ 30 mA cm⁻² · 15.8 전량은 ≈ 25–29 mA cm⁻² · Fig S7 (ii) 판독 ≈ 14 mAh cm⁻² — 원문 수치보다 4–18 % 낮다 (R_o 처리 미기재).
10. **R_o 8 Ω cm²** (Table 4) ↔ Fig 4a 고주파 절편 ≈ 3.8 (L600) · 4.5 Ω (L300) (판독, 1 cm²) — 출처 미기재.
11. **N 의 두께 비례** (Table S1): "단위 부피당" 요소 수가 양극에서 L300 → L600 으로 1.0 → 2.0×10¹⁰ m⁻³.  **음극 d = 5×10⁻⁵ m (50 µm)** ("SEM 추정") ↔ 원료 흑연 ≈ 10 µm (SI p.7) — 설명 없음.
12. 인용 번호 의심: SI p.6 *"good electrochemical stability against graphite.¹⁶"* — (16) 은 Ohta 2007 (LiNbO₃ 코팅 LiCoO₂) 이고 흑연 음극 논문은 (15) Takada 2003 이다 [추정 — 원문 의도 미확인].
13. 사소: "R_0" (p.609 본문) ↔ "R_o" (eq 1) · "coordination of the reaction zone front" (p.609, = coordinate) · "respecitively" (SI p.10) · Fig S7 축 "curent" · 참고문헌 (23) "Electrochim. Electrochim. Acta" · (19) 제목 "Capacity ± Rate" (= Capacity–Rate 의 조판 깨짐).

### 10-2. 이 논문을 인용하는 정본 카드 넷 — 서술 대조 (그 카드는 고치지 않는다)
| 카드 (참고문헌 번호) | 그 카드의 서술 (요지) | 원문 대조 | 판정 |
|---|---|---|---|
| `froboese2019_…` ([36]) | "Eq 15 의 두 번째 출처 — 메모 v2 §8-2 의 Minnmann [33] (사이클 기반 τ) 과 같은 논문 → 황화물 ASSB τ 의 연결 고리" | Kato Eq 2 κ_eff = (ε/τ)κ (p.609) = Froboese Eq 15 꼴 ✓ · Froboese 원문 *"An analytical method to determine the tortuosity τ is given by Equation 15 [32,36]"* ✓ · 같은 논문 ✓ | **일치** — 단 "사이클 기반" 은 "율속 기반" (메모 쪽 낱말을 옮긴 것) |
| `hlushkou2018_…` ([21]) | "같은 계열 (Toyota) ASSB 후막 전극의 tortuosity — Bielefeld 2020 카드가 'void 를 빼고 τ² 를 계산' 했다고 적은 출처 → 이 논문 τ_cond 의 ε 장부와 같은 관례인지 확인" | Toyota ✓ (Kato · Shiotani · Morita) · 후막 τ ✓ · **void 제외 ✓** — ε 0.57 = Table 2 (합 100, p.608).  Hlushkou 원문은 [19–21] 을 "ASSB 복합 전극 이온 수송 자료가 드물다" 의 예로 든다 | **일치**.  열린 물음의 답: ε 는 같은 공칭 고체 기준 부류 (Hlushkou 쪽 ε 는 원문 미기재 — 그 카드 역산 0.62) · **두께 장부는 다르다** — Hlushkou 는 d 실측 (208 µm) → (1−p)¹ · Kato 는 q 치밀 → (1−p)² |
| `minnmann2021_…` ([33]) | "사이클 데이터 적합으로 유효전도도·tortuosity 를 얻는 EIS 와 독립인 방법 (p.2) — [6] 카드는 Kato 의 void 제외 ε 관례를 지적" | 유효전도도 · τ ✓ · **"사이클 데이터" ✗ → 율속 (용량–전류) 자료** ("capacity-current data", p.607 · "rate capability tests", p.610) · EIS 와 독립 ✓ (R_o 출처만 미기재) · void 제외 ✓ | **부분 일치** — "사이클" 낱말.  Minnmann 원문 p.2 의 낱말은 이 묶음에 PDF 가 없어 대조 못 했다 [미확인] |
| `park2019_…` ([35]) | "ASSB P2D 구성 인용 [33–35]" | Park 원문 (p.125): *"the specific contact area, and effective electric and ionic conductivities from the 3D structural model are used for building the electrochemical model for ASSBs [33–35]"*.  Kato 에는 **P2D (COMSOL) 모형도 비접촉면적도 없다** — 유효 전자 (DC 분극) · 이온 (율속) 전도도를 반응대 해석식 · TLM 입력으로 쓴 선례다 | **부분 일치** — "P2D 구성" 은 넓은 꼬리표.  정확히는 "ASSB 전기화학 모형에 유효 전도도를 넣은 선례 (반응대 · TLM)" |
| (참고) `bielefeld2020_…` | "Kato 실측 0.73 mS/cm, τ² = 2.47" · "solid vol% 38.1/57.1/4.8" · "void 미보고 → 15 % 가정" · "Kato 는 void 를 빼고 τ² 를 계산" | 수치 · 조성 ✓ (Table 2 · 5) · void 미보고 ✓ | 일치.  우리 산술 한 줄 — 같은 장부 (void 15 %) 로 옮기면 Kato 는 κ_eff 0.86 · τ 1.79 → 그 카드의 재구성 0.68 · 2.29 와의 "0.68 vs 0.73" 은 **장부가 섞인 비교**다 (같은 장부면 시뮬 σ −21 % · τ +28 %).  그 카드의 "ρ_AM/SE 40 Ω·cm² (Braun 2018, Kato EIS 추정)" 은 이 논문 Table S1 R_ct (42 · 54 Ω — Eq S3 의 단위 요소 저항, 면저항 아님) 와 연결된다는 근거가 이 논문에 없다 [미확인] |

### 10-3. 메모 v2 정정 후보 (`docs/reviews/tau_conventions_judgment_v2_20261003.md` · 부록 `…_addendum_lit10_20261003.md`)
1. **§8-2 [33] 행** — *"EIS 와 독립인 사이클 기반 τ | 절대 대조 교차"*.
   → *"**율속 (방전 용량–전류) 기반** τ — Doyle–Newman 옴 한계 반응대 식 (eq 1–4, p.609–610) · EIS 는 κ_eff 고정 정합 확인뿐 (p.611 · SI p.9–10) · R_o (고주파 저항) 출처 미기재 (Table 4, p.610)"* | 닫는 항목 → *"**정의 교차만** (tau2 · 냉간 펠릿 σ₀ · Bruggeman = COMSOL τ_F 꼴) — 값 교차 불가 (기공 미측정 + q 치밀 → 상자 환산 (1−p)² · LGPS/유리 + LCO + AB · 조성 하나 · 방법 내부 20–25 %)"*.
2. **부록 §0 ② · §1 결정 4 ⓓ** — 펠릿 ≡ 1 목록 "Minnmann · Kaiser · Hlushkou · Froboese" 에 **Kato** (냉간 펠릿 420 MPa · 25 °C, SI p.6 ↔ 복합체 500 MPa · 운전 50 MPa, SI p.7) 를 더한다.  그리고 **기준 상태 인자 실측 한 쌍** (LGPS 냉간 3.2 ↔ 소결 8.3 mS cm⁻¹, SI p.4 → τ × 2.6) 을 결정 4 의 근거로.
3. **부록 §1 결정 4 ⓑ (ε 장부)** — 장부에 **두께 · q 기준**을 더한다: 두께 실측 (Kaiser p.178 · Hlushkou) = 상자 환산 (1−p)¹ ↔ q 치밀 명목 (Kato Table 3–4) = (1−p)².
4. **§1 명명 표** (보강) — Kato 열: "tortuosity factor" τ (초록 p.607 · Eq 2 p.609) = T · "Bruggeman tortuosity factor τ = ε^−0.5" (p.611) = COMSOL Bruggeman τ_F 와 같은 꼴 · τ_d (SI Eq S5) = 시간 상수 (기호 충돌).
5. **§3-5 Bruggeman 배수 문헌 칸** (보강) — ASSB 실험 (율속 경로): **1.86 (양극) · 2.51 (음극)** — 고체 기준 ε 0.57 · q 치밀 · 우리 산술.
6. **§3-8 ③ springback** (보강) — Kato 율속 자료는 500 MPa 압밀 뒤 50 MPa 하우징 하에서 잰 것 (SI p.7) 이고 두께는 치밀 명목값이다 → 되튐 · 기공은 q 의 치밀 장부 오차로 흡수되어 상자 기준 τ 를 **낮추는** 쪽 (실제 두께 ↑ → q_true ↓ → κ_eff,true ↑).

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)

| 서지 (원문 목록 그대로) | 왜 | 정본 카드 |
|---|---|---|
| (18) Doyle, M.; Newman, J. Modeling the Performance of Rechargeable Lithium-Based Cells: Design Correlations for Limiting Cases. J. Power Sources 1995, 54, 46−51. | 반응대 모형 · 옴 한계 (eq 1) 의 원전 | 없음 |
| (19) Doyle, M.; Newman, J. Analysis of Capacity ± Rate Data for Lithium Batteries Using Simplified Models of the Discharge Process. J. Appl. Electrochem. 1997, 27, 846−856. | 용량–율속 해석 (eq 4 꼴 · 기울기 −1) 의 원전 — 이 논문 τ 추출의 방법 근거 | 없음 |
| (29) Siroma, Z.; Sato, T.; Takeuchi, T.; Nagai, R.; Ota, A.; Ioroi, T. AC impedance analysis of ionic and electronic conductivities in electrode mixture layers for an all-solid-state lithium-ion battery. J. Power Sources 2016, 316, 215−223. | 황화물 ASSB 전극 혼합층의 임피던스 이온 · 전자 전도도 — EIS 경로의 같은 축 (Kaiser [13] 과 같은 논문) | 없음 (`siroma2015_…` 는 다른 논문) |
| (28) Malifarge, S.; Delobel, B.; Delacourt, C. Determination of Tortuosity Using Impedance Spectra Analysis of Symmetric Cell. J. Electrochem. Soc. 2017, 164, E3329−E3334. | 대칭셀 임피던스 τ (메모 v2 §8-2) | 같은 묶음 `malifarge2017_tortuosity_symmetric_cell_impedance_tlm` (10-03 작성 · 미커밋) |
| (26) Tröltzsch, U.; Kanoun, O. Generalization of Transmission Line Models for Deriving the Impedance of Diffusion and Porous Media. Electrochim. Acta 2012, 75, 347−356. | Eq S1 의 원전 — 인쇄 분자 (Z_e/Z_e) 대조용 | 없음 |
| (27) Ogihara, N.; Itou, Y.; Sasaki, T.; Takeuchi, Y. Impedance Spectroscopy Characterization of Porous Electrodes under Different Electrode Thickness Using a Symmetric Cell for High-Performance Lithium-Ion Batteries. J. Phys. Chem. C 2015, 119, 4612−4619. | 두께 변화 대칭셀 TLM (Kaiser [16] 과 같은 논문) | 없음 |
| (8) Kato, Y.; Hori, S.; Saito, T.; Suzuki, K.; Hirayama, M.; Mitsui, A.; Yonemura, M.; Iba, H.; Kanno, R. High-power All-solid-state Batteries using Sulfide Superionic Conductors. Nat. Energy 2016, 1, 16030. | 같은 그룹 박막 (25 µm) 고출력 · Fig S1 의 다음 높은 적재 | 없음 |
| (13) Kamaya, N.; Homma, K.; Yamakawa, Y.; Hirayama, M.; Kanno, R.; Yonemura, M.; Kamiyama, T.; Kato, Y.; Hama, S.; Kawamoto, K.; Mitsui, A. A Lithium Superionic Conductor. Nat. Mater. 2011, 10, 682−686. | LGPS 원전 — 소결 8.3 이 비교한 문헌값 | 없음 |
| (33) Seino, Y.; Ota, T.; Takada, K.; Hayashi, A.; Tatsumisago, M. A Sulphide Lithium Super Ion Conductor is Superior to Liquid Ion Conductors for Use in Rechargeable Batteries. Energy Environ. Sci. 2014, 7, 627−631. | > 10 mS cm⁻¹ 은 치밀화 (열간) 상태라는 원문 논거의 출처 — 기준 상태 (결정 4) | 없음 |
| (10) Zhang, W.; Leichtweiß, T.; Culver, S. P.; Koerver, R.; Das, D.; Weber, D. A.; Zeier, W. G.; Janek, J. The Detrimental Effects of Carbon Additives in Li10GeP2S12-Based Solid-State Batteries. ACS Appl. Mater. Interfaces 2017, 9, 35888−35896. | 사이클 과전압 증가의 원인 후보 (탄소–LGPS 부반응) | 없음 |
| (20) Fongy, C.; Jouanneau, S.; Guyomard, D.; Badot, J. C.; Lestriez, B. Electronic and Ionic Wirings Versus the Insertion Reaction Contributions to the Polarization in LiFePO4 Composite Electrodes. J. Electrochem. Soc. 2010, 157, A1347−A1353. | 액체 전극에서 τ 추정이 어려운 이유로 든 문헌 (20–22 중 하나) | 없음 |
| (31) Xia, H.; Lu, L.; Ceder, G. Li Diffusion in LiCoO2 Thin Films Prepared by Pulsed Laser Deposition. J. Power Sources 2006, 159, 1422−1427. | Table S1 의 LCO D (τ_d ≈ 1.4 h 산술의 입력) | 없음 |
| (36) Deng, Z.; Wang, Z.; Chu, I-H.; Luo, J.; Ong, S. P. Elastic Properties of Alkali Superionic Conductor Electrolytes from First Principles Calculations. J. Electrochem. Soc. 2016, 163, A67–A74. | τ_c1 = τ_c2 의 근거로 인용 (SI p.8) | ✅ `deng2016_elastic_superionic_electrolytes_dft` |
| (35) Kato, Y.; Kawamoto, K.; Kanno, R.; Hirayama, M. Discharge Performance of All-Solid-State Battery Using a Lithium Superionic Conductor Li10GeP2S12. Electrochemistry 2012, 80, 749–751. | 50 MPa 하우징 셀의 출처 | 없음 |

- 정본 카드 유무 = `litdb/papers/` 파일 목록 + 낱말 grep 으로 확인 (2026-10-03).

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것)
- 본문 7 쪽 · SI 12 쪽 전부 렌더로 읽었다 (eq 1–4 · Table 1–5 · Figure 1–4 · SI Eq S1–S5 · Table S1 · Fig S1–S7).  eq 1–2 · Table S1 · Eq S1 분자 · Eq S4 · Fig 1 패널 · Fig 2b 삽도 · Fig 3 · Fig S7 은 확대 렌더로 다시 봤다.
- Table 2 vol% = wt%/ρ 정규화 (기공 0) 재현 · Table 3 두께 = 치밀 두께 재현 (8 구성) · q_c · q_a = 치밀 조성값 재현 · Table 5 τ = Eq 2 재현 (≤ 2 %) · eq 4 로 Fig 3 적합선 · 6 mA cm⁻² 용량 재현 (−5 %).
- Fig S7 곡선은 화소 색 판독으로 읽었다 (축 보정 = 데이터 점 L600 ≈ 57 C cm⁻² @ 1 mA cm⁻² 로 확인).
- 본문 · SI 어디에도 없는 것: 기공률 수치 · 두께 실측 여부 · SE 입도 분포 · 펠릿 측정 중 가압 · R_o 측정법 · R_sep 값 · 적합 범위 · 오차 · 반복 셀 수 · X_j 수치.
- 인용 문장 대조: Froboese · Hlushkou · Park 2019 원문 PDF 의 해당 문장을 읽었다 (§10-2).  Minnmann 2021 원문은 이 묶음에 PDF 가 없어 카드 서술만 대조했다.

## 🔗 이 논문을 인용하는 corpus 카드
- `froboese2019_microstructure_ionic_conductivity_assb_electrode` — [36] (Eq 15 의 출처).
- `hlushkou2018_void_space_ion_transport_assb_cathode` — [21] (ASSB 이온 수송 자료가 드물다는 서론 인용).
- `minnmann2021_jes_charge_transport_bottlenecks` — [33] (EIS 와 독립인 유효전도도 · tortuosity 경로).
- `park2019_electrode_design_methodology_assb_3d` — [35] (유효 전도도를 ASSB 전기화학 모형에 넣는 선례 [33–35]).
- `bielefeld2020_effective_ionic_conductivity_binder` — 이 논문의 양극 (LCO + LGPS + AB) 을 재구성해 σ 시뮬을 검증 (Kato 0.73 mS cm⁻¹ · τ 2.47).

## 🗨️ Q&A 로그
- (아직 없음)
