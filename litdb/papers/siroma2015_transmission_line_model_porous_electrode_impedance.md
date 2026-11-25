<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목.
     깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · τ 묶음 형식 기준 = tjaden2018_… · taufactor_… · landesfeind2016_….
     이 논문은 측정도 시뮬레이션도 아닌 회로 수학 논문이다 (EIS 전송선 모델의 해석해 전집).  그래서 §4 = 식의 사슬 (원문 번호 그대로),
     §8 맨 앞 = "Minnmann 2021 TLM 식 [1] 의 원전" (이 카드를 연 이유), § τ 정의 대조 = 이 논문이 τ 를 정의하지 않는다는 것과
     그 해가 어느 τ 로 이어지는지의 매핑.
     쪽 표기 = 학술지 인쇄 쪽 (PDF n 쪽 = 인쇄 312 + n 쪽; 범위 313–322).  식 · 표 · 그림 번호 = 원문 번호.  SI 없음.
     수식 · 표는 원문 PDF 를 고배율로 렌더해 읽었다 (텍스트 추출은 β · α · √ · 분수선을 깨뜨린다).
     값 표지: stated = 본문 · 캡션 · 표 원문 / 판독 = 그림에서 읽은 값 (≈, 추세 전용) / 우리 유도 = 카드 작성자가 원문 식에서 끌어낸
     극한 · 관계 (원문에 그 문장은 없다) / 우리 재계산 = 원문 식 · 원문 매개변수로 다시 계산한 값 (방법 = "원문 대조 기록" 절). -->
# 다공 전극 전송선 모델 (TML/TLM) 임피던스 해석해 전집 — Z형 · T형 · E형 · 범용 연결 × 경계조건 변형 + TML-Y 변환 (★ Minnmann 2021 EIS-TLM 식 [1] 의 원전 · de Levie R/3 계열과 관통형의 위상 구분) — Siroma (Electrochim. Acta 2015)

> slug `siroma2015_transmission_line_model_porous_electrode_impedance` · DOI `10.1016/j.electacta.2015.02.065` · type `theory (analytic impedance solutions — EIS transmission-line model TLM · de Levie equivalent-circuit · Z/T/E/universal connections × boundary conditions · TML-Y transform)` · PDF `7. Mathematical solutions of comprehensive variations of a transmission-line model of the theoretical impedance of porous electrodes.pdf` · digested `2026-10-03` · status ✅
>
> inbox τ 문헌 묶음 #7 · 10 쪽 전부 읽음 (본문 + 부록 A + 참고문헌 25 편) · SI 없음 · 그림 크롭은 메인 몫 (§5 에 크롭 권고).
> ★ **이 카드의 결론 한 줄** — Minnmann 2021 식 [1] 은 이 논문 **표 3 (T형) "open–open" 행**이다.  T형 = 두 단자가 **같은 레일의 양 끝**
> (그림 5b) 인 **관통형**이고, 계면 (z_B) 이 용량성이면 DC 극한이 **단자 레일 저항 L·z_A 전부** (우리 유도) 라서 Minnmann 의 R_ion 은
> 우리 두 띠 Dirichlet 접촉망 (tau2) 과 **같은 경계조건 부류**다.  반대로 R/3 를 쓰는 de Levie · Landesfeind · Nguyen (τ_e) 계열은
> **표 2 (Z형) "open–open (z_C = 0)"** (= E형) 이고, 원문이 *"the most common in the literature [1–7]"* 라 부른다 (p.318).
> 이 논문은 **τ 를 정의하지 않는다** — 레일 비저항 z_A 하나에 레일 위 모든 직렬 저항을 뭉친다 (입계 용량은 레일 안에 둘 수 있다, p.315).
> 형제 카드: `minnmann2021_jes_charge_transport_bottlenecks` (식 [1] 사용처) · `landesfeind2016_tortuosity_eis_electrodes_separators` (TLM-Q · 1/3 규칙)
> · `nguyen2020_electrode_tortuosity_factor` (τ_e vs 관통 τ) · `tjaden2018_tortuosity_review_calculation_approaches` (명명 정본) · `bazzoun2026_dem_fem_rnm_ionic` ("Z-type TLM" 앵커).

---

## 0. 결론 먼저 (닫는 것 + 판정)

| # | 결론 | 근거 (인쇄 쪽 · 식) |
|---|---|---|
| ① | **Minnmann 식 [1] = 표 3 T형 "open–open"**.  항별 대응: 이 논문 (z_A, z_B, z_C) → Minnmann (z_el, z_int, z_ion).  두 식의 모양 (첫 항 L·z_A z_C/(z_A+z_C) · 둘째 항 2·z_A²·√z_B/(z_A+z_C)^(3/2) · (cosh β − 1)/sinh β) 이 글자 그대로 같다 | 표 3 (p.318) ↔ Minnmann 카드 §4.2 의 원문 전사 · Minnmann 원문 인용 *"see Table 3 in Ref. 32, condition 'open-open'"* (Minnmann 카드 참고문헌 표 [32] 기록 — 이 카드에서 Minnmann PDF 를 다시 보지는 않았다) |
| ② | **T형은 관통형**: 단자가 같은 레일 (z_A) 의 x = 0 과 x = L 에 달리고 다른 레일 (z_C) 은 양 끝이 열려 있다 (open–open).  z_B 가 용량성이면 **DC → L·z_A**, 고주파 → L·z_A z_C/(z_A+z_C) (= 두 레일 병렬) — 둘 다 **우리 유도** (원문에 극한 문장 없음, 수치로 확인) | 그림 5b (p.316) · 식 (14)–(16) (p.317) · 표 3 |
| ③ | **de Levie 형 = 표 2 Z형 "open–open (z_C = 0)" = √(z_A z_B) coth α** — *"the most common in the literature [1–7]"*.  z_C = 0 이면 Z형 ≡ E형 (§3.3).  저주파 실수부 → **L·z_A/3**; 전자 레일 저항이 유한하면 **L·(z_A + z_C)/3** (우리 유도) | p.318 (식 25–26 아래 문장 · §3.3) · 표 2 (p.317) · 표 4 (p.318) |
| ④ | **이 논문에 τ 는 없다**.  z_A = "다공 전극의 이온 비저항" (식 33 · p.319) 이고 3D object 단위 Ω cm = **기하 전극 단면 · 두께 L 기준** (표 1).  레일 위 직렬 저항은 전부 z_A 에 뭉치고, 원문은 z_A 안에 **입계 용량**을 둘 수 있게만 허용한다 (p.315).  σ₀ · φ · 미세구조는 없다 ⇒ **Minnmann R_ion 의 내용물은 Minnmann 의 하위회로 선택 (SI 식 S2: z_ion = 저항 하나) 이 정하고, 기준 상태는 TLM 밖 σ₀ (순수 SE 펠릿, τ² ≡ 1) 이 정한다** | p.315 · 표 1 (p.316) · p.319 |
| ⑤ | **원문 해 (표 2–4 · 식 27–32 · 45–47) 는 전부 맞다** — 세밀 이산 사다리 노드 해석과 상대오차 ≲ 4·10⁻¹⁰ (우리 재계산).  오식은 중간식 · 그림 쪽에 있다: **(A.4) 앞 부호 누락** · **그림 12 의 z_B 표지** (1 Ω cm 로 적혔는데 9 개 인쇄값 · 총 3.871 Ω 은 2 Ω cm 로만 재현) · 그림 2 캡션 분모 · §3.4 제목 · 식 33/35 대문자 · "C₁ ~ C₄" (§10) | "원문 대조 기록" 절 |

## 1. 한 줄 요약
1D 균질 전송선 (이온 레일 z_A · 분포 계면 z_B · 전자 레일 z_C) 을 외부 회로에 잇는 네 방식 (Z · T · E · 범용) 과 양 끝 경계 요소
(Z_P · Z_Q / Z_V–Z_Y) 의 모든 조합에 대한 임피던스 해석해를 표 하나로 모으고, 층 직렬 (다층 전극) 을 푸는 **TML-Y 변환**을 유도한
회로 수학 논문 — ASSB 복합 양극 EIS-TLM (Minnmann 2021 = T형 open–open) 의 공식 원전이자, **관통형 (T) 과 de Levie 형 (Z/E) 을
회로 위상으로 가르는 이름표**의 출처다.

## 2. 메타

| 저자 | 저널/년 | DOI | 소속 | 연구유형 |
|---|---|---|---|---|
| **Zyun Siroma\***, Naoko Fujiwara, Shin-ichi Yamazaki, Masafumi Asahi, Tsukasa Nagai, Tsutomu Ioroi | **Electrochimica Acta 160 (2015) 313–322** | **10.1016/j.electacta.2015.02.065** | Research Institute for Ubiquitous Energy Devices, AIST, Ikeda, Osaka (p.313) | theory — 해석해 + 가상 예 2 개 (실험 · 시뮬레이션 데이터 없음) |

- 이력 (p.313): Received 6 Aug 2014 · revised 17 Nov 2014 · accepted 7 Feb 2015 · online 9 Feb 2015.  Keywords: impedance · porous electrode ·
  transmission-line model · mathematical solution.  연구비 JSPS KAKENHI 25289363 (p.321).  "© 2015 Elsevier Ltd. All rights reserved." (p.313) — CC 표기 없음.
- 구성: 본문 9 쪽 + 부록 A (p.321–322) · 그림 12 · 표 4 · 식 (1)–(47) + (A.1)–(A.6) · 참고문헌 25.  **SI 없음.**
- 원문 약칭은 **TML** (transmission-line) 이다.  다른 카드들이 쓰는 TLM 과 같은 것.
- 저자 스스로: *"Although not all of the equations are original, a suitable equation can now be selected from among them depending on the
  situation."* (p.321) — 새로움은 **전집 · 경계조건 일반화 · TML-Y 변환**에 있다.

## 3. 핵심 수치 (이 논문이 주는 것 = 식 · 단위 · 가상 예)

### 3-1. 해의 목록 (값이 아니라 식)

| 연결 | 표 / 식 (쪽) | 경계조건 행 |
|---|---|---|
| Z형 | 표 2 (p.317) | P–Q · open–Q · open–open + 각각 z_C = 0 판 (6 행) |
| T형 | 표 3 (p.318) | P–Q · **P–P (symmetric)** · open–Q · **open–open** + 각각 z_C = 0 판 (8 행) |
| E형 | 표 4 (p.318) | P–Q · open–Q · open–open (3 행; z_C = 0 이면 표 2 와 같다, p.318) |
| 범용형 | 식 (27)–(32) (p.318) | Z_V · Z_W · Z_X · Z_Y 임의 |
| TML-Y (3 단자 → Y) | 식 (39)–(47) (p.321) | 오른쪽 끝 Z_X · Z_Y 임의 |

### 3-2. 단위 (표 1, p.316 · stated)

| 양 | 1D object | 3D object (단면 고려) |
|---|---|---|
| I | A | A cm⁻² |
| Z_total · Z_P · Z_Q · Z_V–Z_Y | Ω | Ω cm² |
| z_A · z_C | Ω cm⁻¹ | Ω cm |
| c (z_A · z_C 의) | F cm | F cm⁻¹ |
| z_B | Ω cm | Ω cm³ |
| c (z_B 의) | F cm⁻¹ | F cm⁻³ |

- 그림 4 캡션 (p.315) 도 1D 차원을 같게 적는다: z_A [Ω cm⁻¹] · z_B [Ω cm] · z_C [Ω cm⁻¹].
- 3D object 의 z_B 의 뜻 (p.316): 식 (7) S_A [cm⁻¹] = S [cm²]/V [cm³] (*"a kind of specific surface area"*) · 식 (8) z_B [Ω cm³] =
  R_A [Ω cm²]/S_A [cm⁻¹] (R_A = 실제 계면 단위 면적당 계면 임피던스) · 식 (9) c [F cm⁻³] = c_A [F cm⁻²] × S_A [cm⁻¹].
  ⚠ 원문의 **R_A 는 계면 임피던스**다 — 이 카드에서 레일 저항은 R_A 로 부르지 않고 **L·z_A** · **L·z_C** 로 적는다.

### 3-3. 가상 예의 매개변수 (stated) + 우리 재계산 ↔ 판독
**예 1 — 평판 전극 위 다공 전극 (Z형 open–Q, 그림 7–8, p.319)**: L = 100 µm · r_i = 100 Ω cm · r_e = 10 Ω cm · c_dl = 100 F cm⁻³ ·
r_ct = 1 Ω cm³ · C_dl = 100 µF cm⁻² · R_ct = 1 Ω cm² ~ ∞ (평판 쪽) · 주파수 1 mHz ~ 1 kHz (그림 8 캡션).

| 점 (그림 8) | 판독 | 우리 재계산 (표 2 open–Q + 식 33–36) |
|---|---|---|
| 1 kHz (네 곡선 공통) | ≈ (0.10, 0) Ω cm² | 0.0987 − 0.0078j |
| 1 Hz (네 곡선 공통) | ≈ (0.32, −0.25) | 0.316 − 0.241j (R_ct = 1: 0.319 − 0.250j) |
| 블로킹 (R_ct = ∞) 곡선이 −Z″ = 1.5 를 지나는 Z′ | ≈ 0.38–0.39 | 0.388 (0.1 Hz 근처) — 수직선 위치 ≈ L(r_i + r_e)/3 = **0.367** (우리 유도) |
| R_ct = 100 / 10 Ω cm² 곡선의 같은 점 | ≈ 0.40 / ≈ 0.6 | 0.409 / 0.596 |
| R_ct = 1 Ω cm² 호의 꼭대기 · Z′ = 1.5 에서 | ≈ −0.83 @ Z′ ≈ 1.1–1.2 · ≈ −0.75 | −0.834 @ Z′ 1.142 · −0.753 |

⇒ 그림 8 은 캡션 매개변수와 **완전히 맞는다**.  원문 해설: *"The results reflect the effect of the charge-transfer resistance on a flat
electrode."* (p.319).

**예 2 — 두 금속 기판 사이 혼합전도 펠릿 (범용형, 그림 9–10, p.319)**: L = 1 mm · r_i = 10 Ω cm · r_e = 10 Ω cm · c_dl = 100 F cm⁻³ ·
r_ct = 1 Ω cm³ · C_dl = 100 µF cm⁻² · R_contact = 1 Ω cm² · R_ct = 10 Ω cm² ~ ∞ · 1 mHz ~ 1 MHz (그림 10 캡션).  외부 요소는
Z_V = Z_X = 1/(jωC_dl + 1/R_ct) (식 37, 금속|이온 전도체) · Z_W = Z_Y = R_contact (식 38, 금속|전자 전도체).

| 점 (그림 10) | 판독 | 우리 재계산 (식 27–32) |
|---|---|---|
| 1 kHz (블로킹) | ≈ (1.93, −0.90) | 1.931 − 0.901j |
| 1 Hz (블로킹) | ≈ (2.55, −0.06) | 2.563 − 0.064j |
| 1 mHz: 블로킹 / 20 / 10 Ω cm² | ≈ 3.0 / ≈ 2.8 / ≈ 2.6 | 2.992 / 2.789 / 2.620 |
| 고주파 끝 (캡션 = 1 MHz) | ≈ (0.63, −0.47) 에서 곡선 시작 | 1 MHz = **0.500 − 0.003j** (실수축 · 두 레일 병렬 0.5); 판독 시작점은 우리 재계산의 ≈ 6 kHz |

⇒ 고주파 끝만 어긋난다 (그려진 곡선이 ≈ 6 kHz 에서 잘린 것으로 보임 — 판독 기반 · 저중요, §10).
- 우리 해석 (원문 해설 없음): 큰 호 = 기판 C_dl 이 열리며 R_contact 두 개 (2 Ω cm²) 가 직렬로 들어오는 과정 (R_contact·C_dl = 10⁻⁴ s →
  ≈ 1.6 kHz, 1 kHz 표시가 호 꼭대기 근처) · 작은 저주파 호 = 펠릿 내부 이온↔전자 교환이 c_dl 결합에서 r_ct 결합으로 바뀌는 과정
  (r_ct·c_dl = 100 s → ≈ 1.6 mHz).  블로킹 DC 2.992 = 2·R_contact + (전자 레일 관통 + r_ct 분로) 0.992 (우리 유도 · 재계산 일치).

### 3-4. 그림 12 — 3 층 직렬 예 (stated) vs 우리 재계산
층 (왼→오, 각 1 cm): (z_A, z_B, z_C) = (3 Ω cm⁻¹, **"1 Ω cm"**, 1 Ω cm⁻¹) · (2, "1", 1) · (1, "1", 1), Z형 open–open (단자 = 1 층 위 레일 왼끝 ·
3 층 아래 레일 오른끝), 1D object 단위.

| 단계 (그림 12 칸) | 인쇄값 (p.320) | 재계산 z_B = 1 Ω cm (표지대로) | 재계산 z_B = 2 Ω cm |
|---|---|---|---|
| ① 3 층 → Y: 위 / 아래 / 단자 쪽 | 2.164 / 0.462 / 0.500 Ω | 1.161 / 0.431 / 0.500 | **2.164 / 0.462 / 0.500** |
| ② 2 층 + ① → Y | 1.760 / 0.704 / 0.573 | 1.170 / 0.557 / 0.606 | **1.760 / 0.704 / 0.573** |
| ③ 1 층 + ② → Y | 2.081 / 0.724 (열린 가지) / 0.717 | 1.478 / 0.517 / 0.749 | **2.081 / 0.724 / 0.717** |
| 총합 | **3.871 Ω** (= 2.081 + 0.717 + 0.573 + 0.500, 캡션) | 3.334 (사다리 직접 3.3336) | 3.872 (사다리 직접 3.8718) |

⇒ **인쇄된 9 개 중간값과 총합은 모두 z_B = 2 Ω cm 로만 재현된다** — 그림의 "1 Ω cm" 표지가 틀린 것으로 판단 (§10).

### 3-5. 극한 — 우리 유도 (원문에 문장 없음 · 원문 식으로 수치 확인)

| 연결 (조건) | 고주파 (z_B → 0) | 저주파 · DC (z_B 용량성 → ∞) | 쓰는 곳 |
|---|---|---|---|
| T형 open–open (표 3) | L·z_A z_C/(z_A+z_C) (두 레일 병렬) | **L·z_A** (단자 레일 저항 전부 · z_B 무관 · 비균질이어도 ∫r dx) | **Minnmann 식 [1]** |
| T형 P–P (symmetric), Z_P 용량성 | 같음 | 같음 (L·z_A) | 블로킹 면 이중층을 넣은 판 |
| Z형 open–open (표 2) | L·z_A z_C/(z_A+z_C) | 실수부 → **L·(z_A + z_C)/3** · 허수부 → 1/(jωcL) | 전자 저항 유한한 de Levie |
| Z형 = E형 open–open (z_C = 0) | 0 | 실수부 → **L·z_A/3** | de Levie · Landesfeind Eq 12 · Nguyen Eq 5 (각 카드 기준) |
| E형 open–open (표 4) | 0 | 실수부 → L·(z_A + z_C)/3 | — |
| 비균질 Z형 (z_C = 0, 층마다 r · c 다름) | — | 실수부 → **∫₀ᴸ r(x)·(1 − C(x)/C_tot)² dx**, C(x) = ∫₀ˣ c dx′ (균일이면 L·z_A/3) | 결정 13 (§8-4) — 2 층 사다리로 확인 |

- β → 0 전개: (cosh β − 1)/sinh β ≈ β/2 (T형) · coth β ≈ 1/β + β/3 (Z/E형).  예: z_A = 2 · z_C = 0.5 · L = 1 이면 T형 DC 2.000 · Z/E형 LF 0.8333 ·
  z_C = 0 판 0.6667 · 고주파 0.40 으로 수렴 (우리 재계산).

## 4. ★ 방법 — 해석해의 사슬 (원문 식 번호 그대로)

### 4-1. 모델 (그림 4 · 식 1–9 · 표 1)
- *"The model consists of an 'upper line' and a 'bottom line' … For electrochemical systems, these represent the ionic current and electronic
  current, respectively."* (p.314) — **위 레일 z_A = 이온, 아래 레일 z_C = 전자** (원문 기본 배치).  I(x) = 위 레일 전류, I_T − I(x) = 아래 레일
  전류 (총전류 I_T 고정), E(x) = 두 레일 사이 전위차 (그림 4 캡션, p.315).
- 일반해의 유도는 *"as described in the literature [16]"* (p.314) = Tröltzsch & Kanoun 2012.
```
dI/dx = −E / z_B                                                                    (1)
dE/dx = −z_A·I + z_C·(I_T − I)                                                      (2)
I = C₁ cosh(√((z_A+z_C)/z_B)·x) + C₂ sinh(√((z_A+z_C)/z_B)·x) + z_C·I_T/(z_A+z_C)    (3)
E = −C₂ √(z_B(z_A+z_C)) cosh(√((z_A+z_C)/z_B)·x) − C₁ √(z_B(z_A+z_C)) sinh(√((z_A+z_C)/z_B)·x)   (4)
Z_total = E_app / I_app                                                             (5)
z = 1/(jωc)    ← "double-layer capacitance for z_B, or grain-boundary capacitance for z_A or z_C"   (6)
S_A [cm⁻¹] = S [cm²] / V [cm³]                                                      (7)
z_B [Ω cm³] = R_A [Ω cm²] / S_A [cm⁻¹]                                              (8)
c [F cm⁻³] = c_A [F cm⁻²] × S_A [cm⁻¹]                                              (9)
```
- 표기 규약 (p.314–315): 무한소 원소 배열 (회색) 의 값 = 소문자 **z**, 배열 밖 거시 원소 = 대문자 **Z** ([Ω]).
- *"In our discussion, we implicitly assume that the sample is one-dimensional."* (p.315) — 3D 는 단면당 값 (표 1) 으로만 다룬다.
- 균질 가정 (p.313): *"if the material is macroscopically uniform and the values of the component elements … do not depend on the position,
  the material is considered to be a continuous medium"* → 해석해.  위치 의존이면 (예: DC 발전 중 R_ct 가 위치마다 다름) 해석해가
  *"difficult or impossible"* → 이산 사다리 (그림 1) 를 Y–Δ 변환 (그림 2–3) 으로 한 단씩 줄이는 재귀 [9][10].

### 4-2. 네 연결형과 경계조건 (그림 5 · 식 10–24)
- 네 단자 중 둘을 골라 외부 회로에 잇는 세 방식 = Z · T · E (그림 5a–c), 그리고 Z · T 를 포함하는 범용형 (그림 5d) (p.314).
  외부 요소 Z_P · Z_Q · Z_V–Z_Y 는 *"macroscopic elements with [Ω] dimension, put out of the arrays of infinitesimal elements"* (p.314).
  **"open" = 그 요소가 없음 (∞)** (그림 6, p.317).
- 외부 요소의 동기 (p.313–314): LIB 양극의 *기판–활물질층 사이 전자 (접촉) 저항* [18] + *기판–전해질 이중층* · PEFC 촉매층의
  *막|이오노머 이온 접촉저항* [19,20] + *최외층 패러데이 임피던스*.

| 연결 (그림 5) | 단자 | 외부 요소 | 경계조건 · 인가량 (원문 식) |
|---|---|---|---|
| **Z형** (a) | + = 위 레일 x = 0 · − = 아래 레일 x = L | Z_P (x = 0 두 레일 사이) · Z_Q (x = L 두 레일 사이) | (10) I(0) = I_T − E(0)/Z_P · (11) I(L) = E(L)/Z_Q · (12) I_app = I_T · (13) E_app = E(L) + ∫₀ᴸ z_A I(x) dx |
| **T형** (b) | + = 위 레일 x = 0 · − = **위 레일 x = L** | Z_P · Z_Q (같은 자리) | (14) I_T = I(0) + E(0)/Z_P = I(L) − E(L)/Z_Q · (15) I_app = I_T · (16) E_app = ∫₀ᴸ z_A I(x) dx |
| **E형** (c) | + = 위 레일 x = 0 · − = 아래 레일 x = 0 | Z_P (단자와 병렬 — 풀 때 빼고 나중에 병렬로 더함) · Z_Q | (17) I_T = 0 · (18) I(L) = E(L)/Z_Q · (19) I_app = I(0) · (20) E_app = E(0) |
| **범용형** (d) | + → Z_V → 위 x = 0 · + → Z_W → 아래 x = 0 · 위 x = L → Z_X → − · 아래 x = L → Z_Y → − | Z_V · Z_W · Z_X · Z_Y | (21) E(0) = −Z_V I(0) + Z_W (I_T − I(0)) · (22) E(L) = Z_X I(L) − Z_Y (I_T − I(L)) · (23) I_app = I_T · (24) E_app = Z_V I(0) + ∫₀ᴸ z_A I(x) dx + Z_X I(L) |

- *"The universal-type is equivalent to Z-type when Z_V and Z_Y are zero, and to T-type when Z_V and Z_X are zero."* (p.314) — 우리 확인:
  Z형 = (Z_W, Z_X) ← (Z_P, Z_Q) · T형 = (Z_W, Z_Y) ← (Z_P, Z_Q) 로 식 27 이 표 2 · 표 3 의 P–Q 행과 같다.  **E형은 범용형에 들지 않는다**
  (§3.4 제목 "which includes Z-type and E-type" 는 오식, §10).
- 그림 5 캡션: *"Note that the Z_P element of the E-type is less important since it is just a parallel connection with respect to the rest."*

### 4-3. 해 — 표 2 · 3 · 4 와 식 (25)–(32) (렌더 판독 · 전 행 수치 검산)
```
β ≡ √((z_A+z_C)/z_B)·L        (25)          α ≡ √(z_A/z_B)·L        (26)
```
- *"In these equations, the value of z_C is often set to be zero, since the electronic resistance in a porous electrode is apt to be
  negligible."* (p.318) · *"The 'open–open (z_C = 0)' condition in Table 2 is the most common in the literature [1–7], and the 'open–open'
  condition in Table 2 is identical to Eq. (12) in Ref. [16]."* (p.318)

**표 2 — Z형 (p.317)**
```
P–Q        Z = z_A z_C/(z_A+z_C)·L + √z_B/(z_A+z_C)^(3/2) ·
               [ (z_A²+z_C²) cosh β + 2 z_A z_C + (z_C²/Z_P + z_A²/Z_Q)·√(z_B(z_A+z_C)) sinh β ]
             / [ {1 + (1/(Z_P Z_Q))·z_B(z_A+z_C)} sinh β + (1/Z_P + 1/Z_Q)·√(z_B(z_A+z_C)) cosh β ]
open–Q     Z = z_A z_C/(z_A+z_C)·L + √z_B/(z_A+z_C)^(3/2) ·
               [ (z_A²+z_C²) cosh β + 2 z_A z_C + (1/Z_Q)·z_A²·√(z_B(z_A+z_C)) sinh β ]
             / [ sinh β + (1/Z_Q)·√(z_B(z_A+z_C)) cosh β ]
open–open  Z = z_A z_C/(z_A+z_C)·L + √z_B/(z_A+z_C)^(3/2) · [ (z_A²+z_C²) cosh β + 2 z_A z_C ] / sinh β
P–Q (z_C = 0)        Z = [ √(z_A z_B) cosh α + (1/Z_Q)·z_A z_B sinh α ]
                       / [ {1 + (1/(Z_P Z_Q))·z_A z_B} sinh α + (1/Z_P + 1/Z_Q)·√(z_A z_B) cosh α ]
open–Q (z_C = 0)     Z = [ √(z_A z_B) cosh α + (1/Z_Q)·z_A z_B sinh α ] / [ sinh α + (1/Z_Q)·√(z_A z_B) cosh α ]
open–open (z_C = 0)  Z = √(z_A z_B) cosh α / sinh α = √(z_A z_B) coth α        ← de Levie 형 ("most common [1–7]")
```
**표 3 — T형 (p.318)** — *"It is likely that a T-type connection will be used with a symmetric condition, i.e., Z_P and Z_Q are equal. Therefore,
a condition of 'P-P (symmetric)' was added to this table."* (p.318)
```
P–Q        Z = z_A z_C/(z_A+z_C)·L + z_A²√z_B/(z_A+z_C)^(3/2) ·
               [ 2(cosh β − 1) + (1/Z_P + 1/Z_Q)·√(z_B(z_A+z_C)) sinh β ]
             / [ {1 + (1/(Z_P Z_Q))·z_B(z_A+z_C)} sinh β + (1/Z_P + 1/Z_Q)·√(z_B(z_A+z_C)) cosh β ]
P–P (symmetric)
           Z = z_A z_C/(z_A+z_C)·L + 2·z_A²√z_B/(z_A+z_C)^(3/2) ·
               [ (cosh β − 1) + (1/Z_P)·√(z_B(z_A+z_C)) sinh β ]
             / [ {1 + (1/Z_P²)·z_B(z_A+z_C)} sinh β + (2/Z_P)·√(z_B(z_A+z_C)) cosh β ]
open–Q     Z = z_A z_C/(z_A+z_C)·L + z_A²√z_B/(z_A+z_C)^(3/2) ·
               [ 2(cosh β − 1) + (1/Z_Q)·√(z_B(z_A+z_C)) sinh β ] / [ sinh β + (1/Z_Q)·√(z_B(z_A+z_C)) cosh β ]
open–open  Z = z_A z_C/(z_A+z_C)·L + 2·z_A²√z_B/(z_A+z_C)^(3/2) · (cosh β − 1)/sinh β      ← ★ Minnmann 식 [1]
P–Q (z_C = 0)   Z = √(z_A z_B) · [ 2(cosh α − 1) + (1/Z_P + 1/Z_Q)·√(z_A z_B) sinh α ]
                  / [ {1 + (1/(Z_P Z_Q))·z_A z_B} sinh α + (1/Z_P + 1/Z_Q)·√(z_A z_B) cosh α ]
P–P (symmetric) (z_C = 0)
                Z = √(z_A z_B) · 2 · [ (cosh α − 1) + (1/Z_P)·√(z_A z_B) sinh α ]
                  / [ {1 + (1/Z_P²)·z_A z_B} sinh α + (2/Z_P)·√(z_A z_B) cosh α ]
open–Q (z_C = 0)     Z = √(z_A z_B) · [ 2(cosh α − 1) + (1/Z_Q)·√(z_A z_B) sinh α ] / [ sinh α + (1/Z_Q)·√(z_A z_B) cosh α ]
open–open (z_C = 0)  Z = 2√(z_A z_B) · (cosh α − 1)/sinh α
```
**표 4 — E형 (p.318)** — *"When z_C is set to be zero, there is no distinction between Z-type and E-type. Therefore, equations of z_C = 0 in
Table 2 can also be used for an E-type connection when z_C is zero."* (p.318)
```
P–Q        Z = [ √(z_B(z_A+z_C)) cosh β + (1/Z_Q)·z_B(z_A+z_C) sinh β ]
             / [ {1 + (1/(Z_P Z_Q))·z_B(z_A+z_C)} sinh β + (1/Z_P + 1/Z_Q)·√(z_B(z_A+z_C)) cosh β ]
open–Q     Z = [ √(z_B(z_A+z_C)) cosh β + (1/Z_Q)·z_B(z_A+z_C) sinh β ] / [ sinh β + (1/Z_Q)·√(z_B(z_A+z_C)) cosh β ]
open–open  Z = √(z_B(z_A+z_C)) cosh β / sinh β = √(z_B(z_A+z_C)) coth β
```
**범용형 (§3.4, p.318)**
```
Z = z_A z_C/(z_A+z_C)·L + √z_B/(z_A+z_C)^(3/2) · (A·cosh β + B·sinh β + C) / (D·cosh β + E·sinh β)          (27)
A = {Z_W(Z_X+Z_Y) + (Z_V+Z_W)Z_Y + Z_V Z_W + Z_X Z_Y}·z_A² + 2(Z_V Z_W + Z_X Z_Y)·z_A z_C
    + {Z_V(Z_X+Z_Y) + (Z_V+Z_W)Z_X + Z_V Z_W + Z_X Z_Y}·z_C²                                                   (28)
B = √(z_B(z_A+z_C)) · [ (Z_W+Z_Y)·z_A² + {Z_V Z_W (Z_X+Z_Y) + (Z_V+Z_W) Z_X Z_Y}·(z_A+z_C)/z_B + (Z_V+Z_X)·z_C² ]   (29)
C = −2·Z_W Z_Y·z_A² + 2·(Z_W Z_X + Z_V Z_Y)·z_A z_C − 2·Z_V Z_X·z_C²                                           (30)
D = (Z_V + Z_W + Z_X + Z_Y)·√(z_B(z_A+z_C))                                                                    (31)
E = z_B(z_A+z_C) + (Z_V+Z_W)(Z_X+Z_Y)                                                                          (32)
```

### 4-4. TML-Y 변환 (§4.2 · 그림 11–12 · 식 39–47, p.320–321)
- 동기: 다층 전극 = 매개변수가 다른 TML 의 직렬.  표 2–4 · 식 27 만으로는 못 푼다.  예외: **모든 층 z_C = 0 이면 Z형**은 오른쪽 층을
  open–open 으로 풀고 그 결과를 다음 층의 Q 로 넣어 open–Q 로 … 차례로 "unzip" 할 수 있다 (Warburg 판은 [21,22]).  그러나 *"for a T-type
  connection, or even for a Z-type connection when z_C element is not zero, this technique can not be used"* — 어느 층도 두 단자 원소로 볼 수
  없어서다 (p.320).
- 사다리는 Y–Δ 를 반복하면 결국 Y 하나가 된다 → *"a TML model inherently has an equivalent Y-circuit"* (p.321).  그림 11: 3 단자 = ② 위 레일
  왼끝 · ③ 아래 레일 왼끝 · ① 오른끝에서 Z_X (위) · Z_Y (아래) 가 만나는 점.
```
Z_T1~T2 (T3 open) = Z₁ + Z₂        (39)      Z_T2~T3 (T1 open) = Z₂ + Z₃        (40)      Z_T3~T1 (T2 open) = Z₃ + Z₁        (41)
Z₁ = ½Z_T1~T2(T3 open) − ½Z_T2~T3(T1 open) + ½Z_T3~T1(T2 open)                                                 (42)
Z₂ = ½Z_T2~T3(T1 open) − ½Z_T3~T1(T2 open) + ½Z_T1~T2(T3 open)                                                 (43)
Z₃ = ½Z_T3~T1(T2 open) − ½Z_T1~T2(T3 open) + ½Z_T2~T3(T1 open)                                                 (44)
```
  세 측정량은 *"universal-type, E-type, and universal-type problems, respectively"* (p.321) 이고, 결과는
```
Z₁ = z_A z_C/(z_A+z_C)·L + √z_B/(z_A+z_C)^(3/2) ·
     [ (Z_Y z_A − Z_X z_C)(z_A − z_C) cosh β + √((z_A+z_C)/z_B)·{Z_X Z_Y (z_A+z_C) − z_A z_B z_C} sinh β − (Z_Y z_A − Z_X z_C)(z_A − z_C) ]
   / [ √(z_B(z_A+z_C)) cosh β + (Z_X+Z_Y) sinh β ]                                                            (45)
Z₂ = [ (Z_X+Z_Y)·z_A·√(z_B/(z_A+z_C)) cosh β + z_A z_B sinh β − (Z_Y z_A − Z_X z_C)·√(z_B/(z_A+z_C)) ]
   / [ √(z_B(z_A+z_C)) cosh β + (Z_X+Z_Y) sinh β ]                                                            (46)
Z₃ = [ (Z_X+Z_Y)·z_C·√(z_B/(z_A+z_C)) cosh β + z_B z_C sinh β + (Z_Y z_A − Z_X z_C)·√(z_B/(z_A+z_C)) ]
   / [ √(z_B(z_A+z_C)) cosh β + (Z_X+Z_Y) sinh β ]                                                            (47)
```
- 쓰임 (p.321): 다층 구조로 연료전지 등의 활성을 높이려는 시도 [23–25] 의 임피던스 해석.  *"this is a very powerful technique that can be
  used to cope with any of the types of the problems shown in Fig. 5, if one does not mind complicated forms of Eqs. (45)–(47)."*
- 그림 12 예는 §3-4 (z_B 표지 문제 포함).

### 4-5. 부록 A — Z형 P–Q 의 유도 (p.321–322)
```
C₁ = z_A I_T/(z_A+z_C) + (1/Z_P)·√(z_B(z_A+z_C))·C₂                                                          (A.1)
C₁ cosh β + C₂ sinh β + z_C I_T/(z_A+z_C) = (1/Z_Q)·{ −C₂ √(z_B(z_A+z_C)) cosh β − C₁ √(z_B(z_A+z_C)) sinh β } (A.2)
C₁/I_T = z_A/(z_A+z_C) − [ (1/Z_P)·(z_A√z_B/√(z_A+z_C)) cosh β + (1/Z_P)·(√z_B z_C/√(z_A+z_C)) + (1/(Z_P Z_Q))·z_A z_B sinh β ] / Dₐ   (A.3)
C₂/I_T = [ (z_A/(z_A+z_C)) cosh β + (1/Z_Q)·(z_A√z_B/√(z_A+z_C)) sinh β + z_C/(z_A+z_C) ] / Dₐ    ← 인쇄 그대로 (부호 없음)   (A.4)
         Dₐ = {1 + (1/(Z_P Z_Q))·z_B(z_A+z_C)} sinh β + (1/Z_P + 1/Z_Q)·√(z_B(z_A+z_C)) cosh β   (Dₐ 는 카드 축약)
∫₀ᴸ I(x) dx = z_C I_T L/(z_A+z_C) + C₁ √(z_B/(z_A+z_C)) sinh β + C₂ √(z_B/(z_A+z_C)) (cosh β − 1)            (A.5)
Z_total = E_app/I_app = [E(L) + ∫₀ᴸ z_A I(x) dx]/I_T = [ −√(z_B(z_A+z_C))·(C₂ cosh β + C₁ sinh β) + ∫₀ᴸ z_A I(x) dx ] / I_T   (A.6)
```
- ⚠ **(A.4) 는 앞에 − 가 있어야 한다** (우리 재계산): (A.1)–(A.2) 를 직접 풀면 C₂/I_T = −[…]/Dₐ 이고, 인쇄 부호로 (A.6) 을 계산하면 표 2 P–Q 와
  다른 값이 나온다 (예: 0.946 + 0.019j 대신 −0.094 − 0.239j).  (A.3) · (A.5) · (A.6) 과 **표 2 의 최종식은 맞다** — 재유도할 때만 걸리는 오식.

### 4-6. 가정 목록 (원문 근거)

| 가정 | 원문 | 쪽 |
|---|---|---|
| 거시 균질 · 위치 무관 원소 | *"macroscopically uniform … do not depend on the position"* — 아니면 이산 사다리 / 층 TML-Y | p.313 · p.320–321 |
| 1D | *"we implicitly assume that the sample is one-dimensional"* | p.315 |
| 두 레일 + 분포 계면 | 위 = 이온, 아래 = 전자; z_A · z_B · z_C 는 임의 복소 원소 (식은 어떤 복소값에도 성립 — 우리 재계산) | p.314 · 표 1 |
| 전자 저항 | 일반해는 z_C 유지; *"often set to be zero"* | p.318 |
| 경계 조건 | 거시 외부 요소 Z_P · Z_Q · Z_V–Z_Y; "open" = 없음 | p.314 · 그림 5–6 |
| 이중층 · 전하이동 | z_B 일반; 용량은 식 (6), 단위 면적 → 단위 부피는 S_A (식 7–9); 예에서 z_B = 1/(jωc_dl + 1/r_ct) (식 34) | p.315–316 · p.319 |
| 레일 안 입계 | *"grain-boundary capacitance for z_A or z_C"* 허용 — 레일이 R∥C 를 품을 수 있다 | p.315 |
| CPE · 확산 | 예에는 없음 (이상 축전기 · R_ct 만).  Warburg 는 다층 재귀 문헌 [21,22] 언급뿐 | p.319 · p.320 |
| 정전류 | 총전류 I_T 고정 | 그림 4 캡션 p.315 |

### 4-7. 시뮬레이션 · 입자 처리
- **시뮬레이션 없음** (DEM · MPM · FEM · RNM 어느 것도 없다).  해석해 + 가상 예 두 개의 Nyquist 계산뿐.  계산 도구 이름 [미확인].
- **입자 처리 ★ = 해당 없음** — 연속 균질 매질.  입자 · 접촉 · 형상 · 입경 개념이 식에 없다.  "접촉 저항" 은 **끝면 외부 요소**로만 나온다
  (p.313–314 · 식 38).

### 4-8. 기법 미니 용어집

| 용어 | 뜻 (이 논문에서) |
|---|---|
| **TML** | transmission-line (전송선) 모델 = 다공 전극의 이온 · 전자 레일과 분포 계면의 사다리.  다른 카드의 TLM 과 같다 |
| **upper / bottom line** | 위 레일 (이온, z_A) / 아래 레일 (전자, z_C) |
| **z / Z** | 소문자 = 무한소 원소 (단위 길이 · 부피당), 대문자 = 배열 밖 거시 원소 [Ω] |
| **open** | 그 외부 요소가 없음 (∞) |
| **P–Q · open–Q · open–open · P–P (symmetric)** | 양 끝 외부 요소의 조합 (그림 6) — P–P = Z_P = Z_Q (T형 대칭) |
| **Z · T · E · universal** | 단자 배치: 다른 레일 · 반대 끝 (Z) / **같은 레일 · 반대 끝 (T)** / 다른 레일 · 같은 끝 (E) / 네 끝 모두 외부 요소로 (범용) |
| **β · α** | β = √((z_A+z_C)/z_B)·L (식 25), α = √(z_A/z_B)·L (식 26, z_C = 0) — 전송선의 무차원 길이 |
| **1D / 3D object** | 단면을 안 넣은 값 / 단면당 값 (표 1) |
| **S_A · R_A · c_A** | 비표면적 [cm⁻¹] · 실제 계면 단위 면적당 계면 임피던스 [Ω cm²] · 단위 면적당 용량 (식 7–9).  ⚠ R_A 는 레일 저항이 아니다 |
| **Y–Δ 변환** | 세 단자 Δ ↔ Y 등가 (그림 2; 출처 [10] = 위키백과 URL) |
| **TML-Y 변환** | 3 단자 TML (+ 오른끝 Z_X · Z_Y) ↔ Y (Z₁ · Z₂ · Z₃) — 식 (45)–(47) |
| **de Levie 형** | 표 2 open–open (z_C = 0) = √(z_A z_B) coth α.  이 이름은 원문 본문에 없다 (참고문헌 [1] De Levie 1963) |

## 5. Figure set ★ (크롭 권고 = ★ 표)

| 그림 / 표 (쪽) | 내용 | 우리가 참고할 점 |
|---|---|---|
| 그림 1 (p.314) | 이산 사다리 (R_i,n · R_e,n · C_dl,n · R_ct,n) | 위치 의존 매개변수의 일반형 — 해석해가 없을 때의 출발점 |
| 그림 2 (p.314) | Y–Δ 변환 (Δ: Z_P · Z_Q · Z_R ↔ Y: Z_J · Z_K · Z_L) | ⚠ 캡션 분모 인쇄 오식 (§10) |
| 그림 3 (p.315) | Y–Δ 를 반복해 사다리를 한 단씩 줄이는 절차 | 이산 사다리 재귀 |
| ★ 그림 4 (p.315) | 1D TML (길이 L · z_A · z_B · z_C · I(x) · I_T − I(x) · E(x)) | 기호 정의의 원천 |
| ★★ 그림 5 (p.316) | 네 연결: (a) Z (b) T (c) E (d) 범용 | **관통형 (T) ↔ de Levie 형 (Z/E) 위상 구분의 원천** |
| ★ 그림 6 (p.317) | Z · T · E 각각의 P–Q · open–Q · open–open | Minnmann "open–open" = T형 3 행째 |
| 그림 7 (p.319) | 전해질 \| 다공 전극 \| 평판 전극 — Z형 open–Q | 집전체 노출부 패러데이 반응을 Z_Q 로 |
| 그림 8 (p.319) | 그림 7 의 Nyquist (R_ct ∞ / 100 / 10 / 1 Ω cm²) | 우리 재계산과 전 특징 일치 (§3-3) · 블로킹 수직선 ≈ L(r_i + r_e)/3 |
| ★ 그림 9 (p.319) | 두 금속 기판 사이 혼합전도 펠릿 — 범용형 (이온 끝 R_ct∥C_dl · 전자 끝 R_contact) | **ASSB 복합 양극 대칭셀의 가장 가까운 원형** |
| ★ 그림 10 (p.319) | 그림 9 의 Nyquist (R_ct ∞ / 20 / 10) | 큰 호 · 작은 저주파 호 해석 (§3-3) · ⚠ 고주파 끝 (§10) |
| 그림 11 (p.320) | TML-Y 변환 (3 단자 TML ↔ Y) | 다층 · 구배 전극 (§8-7) |
| ★ 그림 12 (p.320) | 3 층 직렬 예 → 3.871 Ω | ⚠ z_B 표지 불일치 (§3-4 · §10) |
| ★ 표 1 (p.316) | 1D / 3D 단위 | Minnmann 단위 라벨 판정 근거 (§8-1 ⑧) |
| ★ 표 2 (p.317) | Z형 해 6 행 | open–open (z_C = 0) = de Levie |
| ★★ 표 3 (p.318) | T형 해 8 행 | **open–open = Minnmann 식 [1]** |
| ★ 표 4 (p.318) | E형 해 3 행 | z_C = 0 → 표 2 와 같음 |

## 6. Post-processing ★
- **무엇**: 해석해의 닫힌식 계산 → Nyquist (Z′ vs −Z″, 3D object 단위 Ω cm²) · 표지 주파수 점 (1 kHz · 1 Hz · 1 mHz) · R_ct 매개변수 곡선족.
  다층은 TML-Y 로 단계별 Y 값 (1D 단위 Ω) 을 적어 보인다 (그림 12).
- **도구**: 원문에 소프트웨어 이름 없음 [미확인].
- **기록 방식**: 매개변수는 전부 캡션에 (재현 가능 — 실제로 그림 8 · 10 은 재현됐다).  그림 12 는 중간값까지 인쇄해 검산 가능 (그래서 z_B 표지
  불일치가 드러났다).
- **우리 검산**: "원문 대조 기록" 절.

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 이 파일은 값 0 개 자리표시 — 비교는 판단 메모 v2 의 정의 · 코드 줄 기준)

| 항목 | 이 논문 | 우리 | 같음/다름 · 이유 |
|---|---|---|---|
| 역할 (frame[5]) | EIS 분포회로의 수학 = **실험 쪽 추출 사슬** (R_ion · R_el 을 스펙트럼에서 뽑는 식) | DEM 접촉망 σ (DC 관통) · MPM STEP3 복셀 σ (DC 관통) | 우리 모델의 경쟁자가 아니라 **우리 실험 앵커 (Minnmann · Bazzoun) 의 해석 도구**.  수송 절반만 · 기계 없음 |
| frame[4] | 어느 것에도 보정되지 않은 수학 | 각 모델을 실험에 따로 보정 | 이 카드에 "일치/불일치" 판정은 없다 — 식 · 정의의 대응만 |
| 이산화 | 1D 균질 연속 (레일 2 + 분포 계면); 비균질은 계단 사다리 · 층 TML-Y | 3D 접촉망 (SE 노드 + 간선) / 3D 복셀 FV | 차원 · 위상 다름.  **DC 관통 저항**은 둘 다 "끝면 등전위 사이 컨덕턴스" 같은 관측량 |
| 경계조건 | T형 open–open (관통) · Z/E형 (de Levie) · 외부 요소 일반 | 두 평행 띠 Dirichlet (메모 v2 §7: `network_conductivity.py:225–249` · 590–593) · 측면 주기 | **T형 DC 와 같은 부류** (이온 레일 끝 = 이상 접촉 Z_V = Z_X = 0, AM 레일 = 열림 Z_W = Z_Y = ∞).  Z/E형 대응은 없다 (τ_e 공백, 메모 v2 §7) |
| 레일 저항의 내용 | z_A 하나 (입계 R∥C 를 그 안에 둘 수 있음, p.315) | 간선 = 원기둥 bulk (σ₀ 3.0 펠릿값) + SE–SE Holm R_c = 1/(2σa) 직렬 (hertz 면적 = c_cpl[22] 교차 원판) = **모델 T** · CF 가지 = 협착 0 | 우리 레일은 내용이 **분해**돼 있고 TLM 은 **뭉친다**.  우리 FULL/CF ("모델 내부 협착비") 에 해당하는 TLM 양은 없다 — 실험 R_ion 은 FULL 쪽 관측량 |
| 레일 사이 계면 | z_B = R_A/S_A (균일 분포) | AM–SE 접촉 면적 — 이온 DC 망에는 안 들어감 (AM 비전도) | DC 관통엔 무관 · τ_e 형에서는 sink 가중 = 접촉 면적 분포 (LHS-25 의존) |
| 전자 레일 | z_C 유지 (0 은 관례) | 전자망 따로 (σ_e 채널) | 우리 이온 DC 는 전자 레일과 결합 안 함 = T형 DC 와 같다.  Z형 저주파는 R_el/3 이 섞인다 (우리 유도) |
| 외부 끝면 | 접촉저항 · 기판 패러데이 · 블로킹 이중층을 Z_P/Z_Q/Z_V–Z_Y 로 | 띠 등전위 = 이상 접촉 (띠 끝 단락 → T↓ ≤ 4r_SE/L, 메모 v2 결론 ⑥) | 우리는 끝면 접촉저항 0 · 이중층 없음 (DC 라 이중층은 무관) |
| 주파수 | 전 영역 | DC 하나 | 대응하는 것은 **DC 극한 하나뿐** |
| σ₀ | 없음 | 3.0 mS/cm (펠릿값, CL-91) — T 에서 약분 | 기준 상태는 σ₀ 선택에서만 생긴다 (결정 4, §8-2) |
| 다층 | TML-Y 로 층 직렬 (p.320–321) | graded-z (A7) · 층상 복합 양극 (Phase 5) | 응용 아이디어 (§8-7) |

- ⚠ 이 논문엔 재료 · 입자 · 압밀이 없어서 강체구 ↔ 소성 · halide ↔ LPSCl · 2D ↔ 3D 주의가 **직접 걸리지 않는다**.  걸리는 차이는
  **"1D 균질 연속" ↔ "3D 비균질 접촉망"** 하나다 — 그리고 그 차이가 바로 τ_e ≠ 관통 τ 를 만드는 자리다 (§8-4).

## § τ 정의 대조 — 우리 규약 매핑
> 우리 규약 (CLAUDE.md τ 명명 규약 · 1저자 비준 10-03): f = σ_eff/σ₀ · **tau2** = φσ₀/σ_eff = φ/f (= **tortuosity factor**) · tau = √tau2 ·
> τ_geo = 최단 경로/두께 · τ_e = electrode tortuosity factor (우리 없음).  'tortuosity factor' 는 tau2 에만 쓴다.

**(a) 이 논문의 양 → 우리 다섯 양**

| 이 논문 (쪽) | 정의 · 정규화 | 우리 양 (키) | 판정 |
|---|---|---|---|
| τ (어떤 꼴이든) | **없음** — 본문에 "tortuosity" · "porosity" 낱말이 한 번도 없다 (텍스트 검색) | — | 이 논문은 τ 를 정의하지 않는다 |
| z_A = r_i (식 33, p.318–319) | *"ionic … resistivity … in the porous electrode"* (p.319) · 3D object 단위 Ω cm = **기하 전극 단면 · 두께 L 기준** (표 1) | σ_eff = 1/z_A → **f = 1/(z_A·σ₀)** (`f_ion_<mode>` 의 재료) | σ₀ · φ 는 이 논문에 없다 — 사용자 몫 |
| T형 open–open 의 DC 극한 L·z_A (우리 유도, 표 3) | 관통 · 단자 레일 저항 전부 · z_B 무관 | → Minnmann 식 2 σ_eff = L/(R·A) → 식 4 (보고 꼴) τ² = φσ₀/σ_eff = **tortuosity factor** → **tau2** (`tau2_ion_<mode>`) | **BC 부류 같음** · σ₀ (기준 상태) 다름 |
| Z형 · E형 open–open (z_C = 0) 의 저주파 실수부 L·z_A/3 (우리 유도, 표 2 · 4) | 편측 진입 + 분포 sink (de Levie) | → Landesfeind Eq 12–13 · Nguyen Eq 2 · 5 (각 카드) → **τ_e** (electrode tortuosity factor) | **우리 없음 (—)** — tau2 와 한정어 없이 비교 금지 |
| z_B = R_A/S_A (식 8) · c = c_A·S_A (식 9) | 단위 부피당 계면 임피던스 · 용량 | (아날로그) AM–SE 접촉 면적 / 부피 | tau2 무관 · τ_e 의 sink 가중 |
| z_C = r_e (식 35) | 전자 비저항 | 전자 채널 (`_el_` 꼬리표, 결정 14) | T형 이온 셀 DC 엔 무관 · Z형 LF 엔 R_el/3 로 섞임 |
| 외부 요소 Z_P · Z_Q · Z_V–Z_Y | 끝면 경계 요소 [Ω] | 우리 띠 Dirichlet = 이상 접촉 · AM 레일 열림 | 우리 BC = T형 open–open 의 DC |
| τ_geo · tau (√) | 없음 | `tau_geo_SE_dij` · `tau_ion_<mode>` | 대응 없음 |

- **σ₀ 기준**: 이 논문 = **없음** (회로 수학).  그 해로 τ 를 만드는 쪽이 정한다 — Minnmann = **순수 SE 펠릿 EIS 1.6 mS/cm @25 °C, τ² ≡ 1**
  (Minnmann 카드 · SI §3) · 우리 = 간선 재료 σ₀ 3.0 mS/cm (펠릿값, CL-91) — 우리 T 에서는 약분, 실험 T 에서는 정비례 (메모 v2 §3-1).
- **정규화 길이 · 면적**: TML 의 L = 전류 방향 시료 길이 (그림 4) = 전극 두께 · 3D object = **기하 단면당** (표 1) ↔ Minnmann σ = L/(R·A) (A = 전극
  기하 면적) ↔ 우리 σ_ratio = G·T/A_box (전체 단면, nguyen 카드 대조표) — **같은 관례**.  우리 쪽의 L 기준 선택 (판 간격 ↔ 질량보존 두께,
  결정 1) 은 이 논문이 답하지 않는다.

**(b) J 절 한 줄** — Siroma 2015 는 τ 기호가 없다: 레일 비저항 z_A (Ω cm, 기하 단면 기준) 와 연결형만 준다.  **T형 open–open DC (L·z_A) → Minnmann
τ² = tau2 부류 (관통 conventional)** · **Z/E형 (z_C = 0) 저주파 L·z_A/3 → τ_e 부류 (우리 없음)** · σ₀ 없음 (사용자 몫 — Minnmann 은 순수 SE 펠릿
1.6 mS/cm, τ² ≡ 1).

## 8. 적용 인사이트 (내 연구에 어떻게)

### 8-1. Minnmann 2021 TLM 식 [1] 의 원전 — 이 카드를 연 이유

| 물음 | 답 | 근거 |
|---|---|---|
| ① Z · T · E · 범용 연결의 정의 | 단자 배치로 정의: Z = 다른 레일 · 반대 끝 · **T = 같은 레일 · 반대 끝** · E = 다른 레일 · 같은 끝 · 범용 = 네 끝에 Z_V–Z_Y (Z_V = Z_Y = 0 → Z형 · Z_V = Z_X = 0 → T형) | 그림 5 · p.314 · §4-2 |
| ② 일반해 | (3)–(4) + 경계조건 (10)–(24) → 표 2–4 · (27)–(32) · TML-Y (45)–(47).  전 행 수치 검산 통과 | §4-3 · 원문 대조 기록 |
| ③ Minnmann 이 쓴 변형 | **표 3 T형 "open–open"** — 대응 (z_A, z_B, z_C) → (z_el, z_int, z_ion).  Minnmann 의 하위회로 (카드 §4.2): z_ion = r_ion (S2) · z_el = z_el,bulk + R-CPE (S3–S4) · z_int = CPE (비패러데이, S5) · 외부 끝면은 TLM 밖 직렬 (분리층 · In/InLi 계면 따로 뺌) | 표 3 · Minnmann 카드 §4.2 |
| ④ 레일 역할의 비대칭 | T형 해의 앞계수 **z_A² 는 단자가 달린 레일의 것**이다.  원문 기본 배치는 z_A = 이온 (p.314).  Minnmann 인쇄 식 [1] 은 앞계수가 **z_el²** → 단자 레일 = 전자 = **이온 차단 (SS) 셀** 의 식이다.  이온 측정 (전자 차단 In/InLi 셀) 에는 z_el ↔ z_ion 을 바꾼 꼴 (앞계수 z_ion²) 이 맞고 그 DC 극한은 L·z_ion = R_ion — Minnmann 카드 §4.2 의 "역할 교환" 메모와 같은 결론.  Minnmann 카드의 판독 (이온 차단 스펙트럼 저주파 끝 ≈ 107 Ω = R_el) 도 T형 DC = 단자 레일 저항과 맞는다 | 표 3 · p.314 · Minnmann 카드 §4.2 · 그림 판독표 |
| ⑤ 저주파 극한 | T형 open–open: **DC = L·z_A** (R/3 아님) · 고주파 = L·z_A z_C/(z_A+z_C).  de Levie (Z/E형, z_C = 0): **L·z_A/3** · z_C ≠ 0 이면 **L·(z_A + z_C)/3** — 전부 우리 유도 (원문은 극한을 쓰지 않는다) | §3-5 |
| ⑥ 가정 | 균질 · 1D · 위치 무관 원소 · 두 레일 + 분포 계면 · 외부 요소 = 끝면 경계 · z_C 일반 (0 은 관례) · z_B = 1/(jωc_dl + 1/r_ct) 예 (CPE · 확산 없음) · 정전류 | §4-6 |
| ⑦ Minnmann 이 뺀 것 | **P–P (symmetric) 행** (블로킹 면 이중층을 Z_P = Z_Q 로) 을 쓰지 않고 open–open 을 썼다.  DC (L·z_A) · 고주파 극한은 두 행이 같으므로 **R_ion · R_el 값에는 영향 없음**; 중간 주파수 모양 적합에만 영향 (우리 유도) | 표 3 · p.318 |
| ⑧ 단위 라벨 판정 (Minnmann 카드 §17 #16) | Minnmann 은 R = L·r (S6–S7, Ω) → σ = L/(R·A) 로 쓰므로 **1D object 관례**다 — 그 관례의 일관된 단위는 z_el · z_ion · r [Ω m⁻¹] · z_int [Ω m] (표 1).  Minnmann 인쇄 라벨 (z [Ω m] · z_int [Ω m⁻¹]) 은 지수가 거꾸로이고 3D 관례 (z_int 는 Ω m³) 와도 안 맞는다 → 카드 판단 ("라벨 오기, 계산 무영향") 이 표 1 로 확정 | 표 1 (p.316) · 그림 4 캡션 |
| ⑨ 끝면 요소를 따로 빼도 되나 | 다른 레일의 양 끝이 열려 있으면 (Z_W = Z_Y = ∞) 범용형 = **T형 open–open + Z_V + Z_X 직렬** (우리 확인) → Minnmann 의 "분리층 · In/InLi 계면을 따로 빼기" 는 이 조건에서 정확하다 | 식 27 (우리 수치 확인) |

### 8-2. 결정 4 — Minnmann 의 R_ion 이 무엇을 포함하나 (기준 상태)

| 성분 | R_ion 에 들어가나 | 이유 |
|---|---|---|
| SE 결정립 (bulk) | **들어간다** | 이온 레일 직렬 저항 |
| SE–SE 입계 | **들어간다 (분리 안 됨)** | 이 논문은 레일 안 입계 용량을 허용하지만 (p.315) Minnmann 은 z_ion = 저항 하나 (S2) — 입계 호를 따로 두지 않았다 |
| SE–SE 접촉 협착 | **들어간다** | 레일 직렬 (TLM 에 접촉 원소 없음 — "접촉 저항" 은 끝면 외부 요소로만, p.313–314 · 식 38) |
| 경로 기하 (굽음 · 좁아진 단면 · SE 부피분율) | **들어간다** | Minnmann 식 4 (보고 꼴) 가 φ 를 따로 곱해 빼고 남는 것이 τ² 로 해석된다 |
| CAM\|SE 계면 | 안 들어간다 | z_int (CPE) = 레일 사이 원소, DC 전류 0 |
| 끝면 (분리층 · In/InLi 계면) | 안 들어간다 | open–open TLM 밖 직렬 (§8-1 ⑨) |
| NCM 의 Li⁺ 전도 | 안 들어간다 | CAM 은 이온 레일에 없다 (계면 비패러데이) |
| 정규화 | 두께 L (TML 분포 길이 = 측정 기하 두께) × 기하 단면 A | 표 1 · 그림 4 · Minnmann 식 2 |
| 기준 상태 | **TLM 밖** — σ₀ 선택 (순수 SE 펠릿 1.6 mS/cm, τ² ≡ 1) | 이 논문에 σ₀ 없음 |

- ⇒ Minnmann τ² 의 펠릿 정규화는 **펠릿 자신의 입계 · 접촉 · 기공을 단위 경로당 같은 만큼만** 지운다 — 복합체가 펠릿보다 접촉이 많으면 그
  초과분은 τ² 에 남는다 (같은 레일에 뭉쳐 있으므로 TLM 으로는 못 가른다).
- **우리 쪽 짝**: 간선 σ₀ 3.0 (펠릿값) 위에 Holm 을 더한 모델 T 를 **순수 SE 망 T_pure,ours 로 나누는 것**이 Minnmann 의 펠릿 정규화 (τ² ≡ 1) 와
  같은 조작이다.  ⇒ **결정 4 권고 (순수 SE 게이트 · 원 T 와 정규화 T 둘 다 보고) 유지 — 바꾸지 않는다.**  이 논문이 더하는 것은 *왜* 그것이
  유일한 길인지다: Minnmann 의 이온 레일엔 입계 원소가 없어 **스펙트럼 분해로는 기준을 맞출 수 없다**.

### 8-3. 판단 메모 v2 §3-2 (기준 상태 — 방향)
- 이 논문은 기준 상태에 **중립**이다 (σ₀ · φ 가 없다).  §3-2 의 "Minnmann 기준 = 순수 SE 펠릿 τ² ≡ 1 · 우리 기준 = 간선 펠릿값 + Holm (부분 이중계상
  → T↑) · 맞추면 × 0.5–0.7" 의 **방향은 그대로**다.  이 논문이 확정하는 것은 하나: Minnmann 의 R_ion 이 펠릿과 **같은 뭉침 규칙** (레일 저항 하나)
  으로 정의돼 있어 "펠릿 = 1" 정규화가 **같은 종류의 양끼리의 비**라는 것.
- ⚠ 순수 SE σ₀ 는 TML 이 아니라 SS 블로킹 전극 펠릿 측정에서 왔다 (Minnmann 카드 · SI Fig S6) — 추출법은 다르지만 둘 다 "SE 경로의 총 이온 저항 ×
  L/A" 라는 같은 뭉침 양이다.

### 8-4. 결정 13 — τ_e 계열 EIS-TLM 의 가정이 우리 접촉망 관통 BC 와 어디서 다른가

| 가정 | τ_e 계열 (Z/E형 open–open, z_C ≈ 0 — Landesfeind · Nguyen eSCM) | Minnmann (T형 open–open) | 우리 접촉망 (두 띠 Dirichlet) |
|---|---|---|---|
| 단자 | 이온은 x = 0 에서만 들어오고 전자는 x = L 집전체 (Z) / 둘 다 x = 0 (E) | 같은 레일 양 끝 (관통) | 같은 SE 망의 양 끝 띠 (관통) |
| DC 전류 | 0 (z_B 용량성 → 차단) — 정보는 저주파 실축 절편 | 단자 레일 전부 | 관통 G_full |
| 저주파 / DC 저항 | 실수부 L·z_A/3 · z_C ≠ 0 이면 L(z_A + z_C)/3 | L·z_A | 1/G |
| 균질 가정 | **1/3 은 균일 r(x) · 균일 c(x) 의 산물** — 비균질이면 ∫ r (1 − C/C_tot)² dx | DC 는 비균질이어도 ∫ r dx (직렬 합) | 3D 망 그대로 (균질 가정 없음) |
| 계면 면적 | sink 가중 ∝ S_A (식 8–9) → **AM–SE 접촉 면적 분포 의존** | DC 무관 | 이온 DC 무관 |
| 전자 레일 | z_C ≠ 0 이면 R_el/3 이 섞인다 | DC 무관 (전자 레일 양 끝 열림) | 무관 (AM 비전도) |
| 방향성 | **방향 의존** — 2 층 (r 3 : 1, c 같음) 이면 저항층이 입구 쪽 0.917 ↔ 반대 0.417 (같은 Σ rL/3 = 0.667) | **방향 맹** (가역성) | 방향 맹 |
| dead-end | sink 를 품어 기여 (균질 적합이 겉보기 z_A 로 흡수) | DC 기여 0 | 기여 0 (관통 성분만) |

- **핵심**: 균질 TML 에서는 T형 DC 와 Z형 적합이 **같은 z_A** 를 준다.  τ_e ≠ 관통 τ 는 매질이 **균질 1D TML 가정을 벗어날 때만** 생긴다 — dead-end ·
  S_A 분포 · z 구배 · 전자 레일.  ⇒ Minnmann τ² 와 우리 tau2 는 **BC 부류가 같고**, 다른 것은 기준 상태 (σ₀) · 협착 모델 · 미세구조다.  Bazzoun ·
  Landesfeind · Nguyen 의 τ_e 는 **부류가 다르다**.
- **"R_ion = 3·R_eff" 의 조건** (메모 v2 §7 최소안 · Nguyen Eq 5): 균일 r · 균일 c · z_C = 0 일 때만 정확 (우리 유도 · 사다리 확인).  2 층 3 : 1 예에서
  3·R_eff = 2.75 또는 1.25 (참 ΣrL = 2.0) → **±37.5 %** (우리 계산).
- ⇒ **결정 13 권고 유지 — 바꾸지 않는다.**  메모 v2 의 진단 셋 (FULL 장 flux dead-end · z 단면별 SE 컨덕턴스 · AM–SE 면적 분포) 이 정확히 위 표의
  세 줄 (dead-end · 균질 가정 · 계면 면적) 에 대응한다.  **넷째 진단을 덧붙일 것**: 전자 레일 저항 (저 CAM 에서 R_el/3 항 — Minnmann τ_el² 120 @25 vol%
  가 그 조성이 있음을 보인다).

### 8-5. 결정 5 (COMSOL/EIS 표기) — "EIS 입력" 은 연결형을 함께 적어야 한다
- 같은 "EIS-TLM τ" 가 **T형이면 관통 tortuosity factor (tau2 부류)**, **Z/E형 (de Levie) 이면 τ_e 부류**다.  ⇒ TAU-01 정정 (√T 에서 "COMSOL/EIS input"
  삭제) 을 지지하고, 앞으로 tau2 에 "EIS" 표지를 달 때는 **"T형 (관통) EIS-TLM 과 같은 부류"** 처럼 연결형을 명시한다.  권고 변경 없음 (한정어 추가).

### 8-6. 결정 14 (전자 · 열 T)
- Minnmann 의 전자 레일은 z_el,bulk + NCM–NCM 접촉 R-CPE (S3–S4) 이고 R_el = L(r_el,bulk + r_el,int) (S6) — **접촉 저항이 R_el 안에 있다**.
  이온 차단 SS 셀은 T형이고 DC = R_el (관통).  ⇒ "전자 T 는 GB · 접촉 인자를 T 에 흡수한다고 명시" (결정 14) 와 같은 뭉침 규칙.  권고 변경 없음.

### 8-7. TML-Y 를 쓰는 길 (아이디어 · 미검증)
- z 단면별 SE 망 컨덕턴스 (결정 13 진단) + 층별 AM–SE 면적 (c(z) = c_A·S_A(z)) + 층별 전자 컨덕턴스 → 층별 (z_A, z_B, z_C) → **TML-Y 직렬로 Z형
  (τ_e 형) 스펙트럼과 T형 DC 를 같은 층 데이터에서** 계산.  메모 v2 §7 최소안 (3D 희소 솔브) 의 반해석 대안.
- ⚠ 조건: 층마다 1D 균질 근사 → 층 두께 ≫ 입자 지름 필요 (메모 v2 §7 ②: 침대 두께 ÷ 최대 AM 지름 중앙 4.7) · sink 가중 = 접촉 면적 → LHS-25 가 먼저.

### 8-8. Bazzoun "Z-type TLM" 표기 읽기
- 이 논문의 정의에서 "Z형" = 다른 레일 · 반대 끝 = de Levie 계 (τ_e 계열).  Bazzoun 카드의 "full-blocking 대칭셀 Z-type TLM (R_ion / R_elec / CPE)" 가
  이 정의를 따른 것이라면 Bazzoun 의 R_ion 은 **τ_e 계열 적합값**이고 저주파 오프셋에는 R_elec/3 도 섞인다 (우리 유도).  nguyen 카드 ⑤ 의 판독과 같은
  결론에 **위상 근거**를 더한다 — 확정은 Bazzoun 원문 (회로도 · 인용) 대조 뒤.

## 9. 인용 가능 문장 (deck/paper용)
- "Minnmann et al. (2021) extracted R_ion and R_el with the T-type 'open–open' transmission-line solution of Siroma et al. (2015, Table 3), in which
  both terminals sit on the same rail; for a purely capacitive interface its low-frequency limit is the full through-resistance of that rail
  [limit derived by us from the published solution], i.e., the same through-plane boundary class as a two-plate Dirichlet network simulation."
- "The de Levie limit R_ion/3 belongs to the Z-type (equivalently E-type, for negligible electronic resistance) 'open–open' solution, which Siroma et
  al. (2015) note is the most common form in the literature; with a finite electronic-rail resistance the low-frequency real-axis offset becomes
  (R_ion + R_el)/3 [our derivation]."
- "In the transmission-line formalism each rail is a single homogenized per-length impedance, so the fitted rail resistance lumps bulk,
  grain-boundary and contact contributions unless a sub-circuit is placed inside the rail."

## 10. 주의/한계 (over-claim 방지)
- **회로 수학이다** — 실험 · 미세구조 · 재료가 없다.  우리 수치와의 "일치/불일치" 근거로 쓰지 않는다.  쓰는 자리는 **정의 · 경계조건 · 극한**뿐이다.
- **극한 (L·z_A/3 · L·z_A · L·(z_A + z_C)/3 · 비균질 식) 은 원문 문장이 아니다** — 우리가 원문 식에서 끌어내고 수치로 확인한 것이다.  인용 시 "derived from
  Siroma 2015 Table N" 로 적는다.
- **균질 1D** 가 전제다.  실제 ASSB 복합 양극 (입경비 · z 구배 · dead-end · 판 근처 층) 에서는 적합된 z_A 가 "겉보기" 값이 된다 — Z형에서 특히.
- Minnmann 에 관한 서술 (S2–S7 · 셀 배치 · 판독 107 Ω · "Table 3 … open-open" 인용) 은 **Minnmann 카드 (10-03 PDF 대조판) 기록**에서 가져왔다 — 이 카드
  작성 중 Minnmann PDF 는 다시 보지 않았다 (인박스에 없음).  Landesfeind Eq 12–13 · Nguyen Eq 2 · 5 · Bazzoun "Z-type" 도 각 카드 기준.

**원문 오식 · 내부 불일치 (우리 확인)**

| # | 자리 (쪽) | 인쇄 | 맞는 것 | 근거 |
|---|---|---|---|---|
| 1 | 그림 12 (p.320) | 세 층 z_B = "1 Ω cm" | 인쇄된 9 중간값 + 총 3.871 Ω 은 **z_B = 2 Ω cm** 로만 재현 (1 Ω cm 이면 총 3.334 Ω) | §3-4 (TML-Y 식 · 사다리 직접 둘 다) |
| 2 | 식 (A.4) (p.321) | C₂/I_T = +[…]/Dₐ | **−**[…]/Dₐ | (A.1)–(A.2) 직접 풀이 · (A.6) → 표 2 P–Q 재현 (§4-5) |
| 3 | 그림 2 캡션 (p.314) | Z_J = Z_Q·Z_R/(Z_P·Z_Q·Z_R) 등 (분모가 곱 — 텍스트 층도 같은 글리프) | 분모 = **Z_P + Z_Q + Z_R** (표준 Δ→Y) | 인쇄 꼴은 차원이 Ω⁻¹ |
| 4 | §3.4 제목 (p.318) | "Universal-type, which includes Z-type and E-type" | **Z형 · T형** (§2.2 본문 p.314 · 그림 5 캡션과 같게) | 식 27 환원 (우리 확인) |
| 5 | 식 (33) · (35) (p.318–319) | Z_A = r_i · Z_C = r_e (대문자) | 소문자 z_A · z_C (원문 규약 p.314–315; 식 37 아래 *"z_A ~ z_C are the same as … Eqs. (33)–(35)"*) | 표기 규약 |
| 6 | §3.1 (p.318) | "the integral constants C₁ ~ C₄ in Eqs. (3) and (4)" | 식 (3)–(4) 엔 C₁ · C₂ 뿐 | — |
| 7 | 그림 10 (p.319) | 곡선이 ≈ (0.63, −0.47) Ω cm² 에서 시작 (판독), 캡션 1 MHz | 우리 재계산 1 MHz = 0.500 − 0.003j (시작점 ≈ 6 kHz) | 판독 기반 · 저중요 |
| 8 | 참고문헌 [20] (p.322) | "Park, Y.-W. Choi, …" | 제1저자 이름 머리글자 누락 | — |

- 원문 **해 자체** (표 2–4 · 식 27–32 · 45–47) 에는 오식이 **없다** (§0 ⑤).

**메모 v2 정정 후보** (`docs/reviews/tau_conventions_judgment_v2_20261003.md`)

| # | 메모 자리 | 현재 문장 | 원문 근거 | 제안 |
|---|---|---|---|---|
| A | §1 τ_e 행 · Minnmann 칸 / §7 마지막 행 | "관통형에 가깝다 [판독 — nguyen 카드 ⑤]" / "Minnmann (… → 관통형) [판독]" | Minnmann 식 [1] = 표 3 T형 open–open (p.318) · T형 = 같은 레일 양 끝 (그림 5b, p.316) · DC = 단자 레일 저항 (우리 유도) | **[판독] 해제 → "관통형 (T형 open–open)"** — 한정어: 이온 셀은 z_A = z_ion 판 (§8-1 ④) |
| B | §8-1 #7 "왜 필요한가" | "Minnmann 의 R_ion 이 무엇을 포함하는지 (입계 · 접촉) 확인" | 이 원문은 미세구조를 다루지 않는다 — 레일 = 균질 저항 하나 · 레일 안 입계 용량 허용 (p.315) · "접촉 저항" 은 끝면 외부 요소로만 (p.313–314 · p.319 식 38) | **"구조적 답만 가능"** 으로: 내용물은 Minnmann SI 식 S2 (z_ion = 저항 하나) 가 정한다 → 입계 · 접촉 · bulk 가 한 덩어리 (§8-2) |
| C (보강) | §7 최소안 "R_ion = 3·R_eff (Nguyen Eq 5)" | AM 등전위 가정 명시됨 | 표 2 open–open 의 저주파 전개 (우리 유도) | 정정 아님 — "균일 r · 균일 c · z_C = 0 에서만 정확; z_C ≠ 0 이면 (R_ion + R_el)/3, 비균질이면 ∫ r (1 − C/C_tot)² dx (2 층 예 ±37.5 %)" 한정어 추가 후보 |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것)
- **렌더**: 10 쪽 전부 2 배 렌더 + 표 2 · 3 · 4 · 식 (27)–(32) · (45)–(47) · (A.1)–(A.6) · 그림 2 캡션 · 그림 8 · 10 · 12 는 4–7 배 고배율로 읽었다.
  (A.4) 앞 부호는 7 배로 다시 봤다 (부호 없음).  그림 2 캡션은 텍스트 층에서도 분모 구분자가 곱셈과 같은 글리프다.
- **검산 1 — 해 전 행**: 표 2 (6 행) · 표 3 (8 행) · 표 4 (3 행) · 식 (27)–(32) · (45)–(47) 을 판독한 그대로 코드로 옮겨, 같은 매개변수 (임의 복소수
  z_A · z_B · z_C · Z_P · Z_Q · Z_V–Z_Y · L) 의 **세밀 이산 사다리** (구간 800 · 1600, 끝 반가중 분로, Richardson) 노드 해석과 대조 → 전 행 상대오차
  ≲ 4·10⁻¹⁰.  (TML-Y 는 사다리로 (39)–(41) 의 세 개방 측정을 만든 뒤 (42)–(44) 로 Z₁–Z₃ 를 구해 (45)–(47) 과 대조.)
- **검산 2 — 부록**: (A.1)–(A.2) 직접 풀이와 (A.3) 일치 · (A.4) 는 부호 반대 · 부호를 고치면 (A.5)–(A.6) 이 표 2 P–Q 를 재현 (두 매개변수 묶음).
- **검산 3 — 환원**: 범용형 → Z형 (Z_V = Z_Y = 0) · T형 (Z_V = Z_X = 0) 일치 · Z_W = Z_Y → ∞ 이면 T형 open–open + Z_V + Z_X.
- **검산 4 — 그림 12**: 표지대로 z_B = 1 → 3.334 Ω (TML-Y 사슬 · 사다리 직접 같음) · z_B = 2 → 9 인쇄값 전부와 총 3.8718 Ω.
- **검산 5 — 그림 8 · 10**: 캡션 매개변수로 재계산 → 표지 점 · 곡선 특징 비교 (§3-3).  그림 10 고주파 끝만 어긋남.
- **검산 6 — 극한 · 비균질 식**: T형 DC · 고주파, Z/E형 저주파 (z_C 유무) 를 원문 식으로 수치 확인 · ∫ r (1 − C/C_tot)² dx 를 2 층 사다리 (네 경우) 로 확인
  (모두 5 자리 일치).
- **텍스트 검색**: 본문에 "tortuosity" · "porosity" · "limit" · "low frequency" 0 회 · "Warburg" 1 회 (p.320) · "grain-boundary" 1 회 (p.315).
- **중복 확인 (10-03)**: 정본 `litdb/papers/` 파일 목록 (355 개) 에 이 slug 없음 · DOI `git grep` 0 건 · "siroma" 는 다른 문서의 **인용**으로만 나온다
  (카드: minnmann2021 · ketter2025 · interfacial_impedance · bielefeld2019 · bong2023 + INDEX · comparison_vs_ours — 이 중 bielefeld2019 · bong2023 은
  다른 Siroma 논문 (복합 전극 측정) 의 인용).

## 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)

| 원문 번호 · 서지 (p.322) | 왜 |
|---|---|
| [1] R. De Levie, Electrochim. Acta 8 (1963) 751. | TML 원전 · open–open (z_C = 0) coth 형과 R/3 계보의 출발 |
| [4] A. Lasia, J. Electroanal. Chem. 397 (1995) 27. | landesfeind 카드가 TLM-Q 해석해 출처로 "Lasia [36]" 를 적는다 — 같은 논문인지 [미확인] |
| [12] J. Bisquert, G. Garcia-Belmonte, F. Fabregat-Santiago, A. Compte, Electrochem. Commun. 1 (1999) 429. | 일반 경계조건 TLM (Bisquert 계) — 반사 · 투과 끝면 |
| [13] J. Bisquert, Phys. Chem. Chem. Phys. 2 (2000) 4185. | 같은 계열 |
| [16] U. Tröltzsch, O. Kanoun, Electrochim. Acta 75 (2012) 347. | 이 논문 일반해의 유도 출처 (p.314) · 표 2 open–open = 그 Eq. (12) (p.318) |
| [18] T. Nakamura, S. Okano, N. Yaguma, Y. Morinaga, H. Takahara, Y. Yamada, J. Power Sources 244 (2013) 532. | LIB 양극 기판–활물질층 접촉저항 (외부 요소의 동기) |
| [21] V. Freger, Electrochem. Commun. 7 (2005) 957. · [22] J.-P. Diard, N. Glandut, C. Montella, J.-Y. Sanchez, J. Electroanal. Chem. 578 (2005) 247. | 다층 (z_C = 0) Z형 재귀 (Warburg) — graded-z 전극 EIS |
| [24] Z. Siroma, K. Yasuda, Electrochemistry 79 (2011) 326. | 저자 선행 [내용 미확인] |
| (목록 밖 — Minnmann 참고문헌 [26] 서지 그대로) Z. Siroma, T. Sato, T. Takeuchi, R. Nagai, A. Ota, and T. Ioroi, J. Power Sources, 316, 215 (2016). | T형을 복합 전극에 적용 · σ_e 분리 측정 ("Siroma 법" — bong2023 카드 [32] 와 같은 논문).  정본 카드 없음 · 이 카드에서 원문 미확인 |

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
