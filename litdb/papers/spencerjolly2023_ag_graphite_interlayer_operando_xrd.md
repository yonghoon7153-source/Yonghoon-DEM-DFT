<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목. COMPREHENSIVE / paper-level STANDALONE digest. -->
# Ag–흑연 복합 인터레이어(anodeless Li₆PS₅Cl)의 **구조 변화를 operando XRD 로** — 충전: Li 가 흑연에 **전기화학적으로** 들어간 뒤 Ag 와 **화학적으로** 합금화 (Li_xAg → LiAg → Li₉Ag₄ → Li₁₀Ag₃) · 방전은 역경로가 아니다 · Ag 는 CCD 를 올리지 않고 **CC 쪽 Li/Li–Ag 층을 균일하게** 만든다 (interface) — Spencer-Jolly · Agarwal · … · Grant · House · Bruce (*Joule* 7, 503 (2023))

> slug `spencerjolly2023_ag_graphite_interlayer_operando_xrd` · DOI `10.1016/j.joule.2023.02.001` · type `exp (operando PXRD — lab Cu Kα reflection + Diamond I12 synchrotron transmission; SEM/EDX morphology; Ag–graphite composite interlayer on anodeless Li6PS5Cl)` · PDF `0f713812-7._Structural_changes_in_the_silver-carbon_composite_anode_interlayer_of_solid-state_batteries.pdf` (13 pp) + SI1 `a4550f43-7._Sup1_….pdf` (그림 S1–S5) + SI2 `92b25727-7._Sup2_….pdf` (Joule 표준 보고 양식, 그림 없음) · digested `2026-09-23` · status ✅

> elements: Li, Ag, C, P, S, Cl
> methods: —

> ⚠⚠ **세 줄 경고 — 인용 전에 반드시.**
> ① **점착·박리·계면 역학은 재지 않았다.** 이 논문은 **구조(상)·형태·CCD** 논문이다 — 점착 트랙에는 "운전 중 계면이 *무엇으로* 바뀌는가" 의 원전으로만 쓴다.
> ② 탄소는 Samsung 원조(Lee 2020, 카본블랙)와 달리 **흑연**이다 (회절로 리튬화를 따라가기 위해). Ag·흑연 **입자 크기 미기재**.
> ③ 저율(30 µA cm⁻²)은 **상온**, 고율(2 · 2.5 · 4 mA cm⁻²)은 **60 °C** — "속도 효과" 에 온도가 섞여 있다. 적층압은 전 조건 **2 MPa**.

---

## 1. 한 줄 요약

**Ag–C 인터레이어가 anodeless 황화물 전지에서 어떻게 작동하는지를 operando PXRD + SEM/EDX 로 풀었다.**
충전 시 Li 는 먼저 **흑연에 전기화학적으로 삽입**되고(Ag 는 부피의 5.7 % 라 SE 와 직접 접촉이 거의 없다), 리튬화된 흑연(LiC_x)이 Ag 와 **화학적으로 반응**해 Li_xAg 고용체 → **LiAg → Li₉Ag₄ → Li₁₀Ag₃** 로 점점 Li-rich 합금이 된다. **LiC₆ 만이** LiAg 를 만들 만큼 화학퍼텐셜이 높다. 용량이 흑연+Ag 수용량을 넘으면 **Li 금속**이 인터레이어와 **집전체(CC) 사이**에 석출된다.
방전은 역경로가 아니다 — Li 가 결핍된 **Li₁₀₋ₓAg₃**, **LiAg 의 UPb 형 구조**처럼 충전에서 안 보이던 상을 지난다.
고율에서는 흑연 리튬화가 Ag 와의 화학 반응을 앞질러 Li-결핍 합금이 오래 남고 Li 금속이 더 많이 생긴다. **2.5 mA cm⁻² 이상에서는 흑연 단독이든 Ag–흑연이든 똑같이 덴드라이트로 단락**(2.0 에서는 안정) — **Ag 는 CCD 를 올리지 않는다**. Ag 의 실제 효과는 **CC 쪽 Li₁₀Ag₃ + Li 층을 균일하게 만들고 방전 때 층 안으로 되돌리는 것**이다.

## 2. 메타

| 항목 | 값 |
|---|---|
| 저자 | **Dominic Spencer-Jolly**¹·³, **Varnika Agarwal**¹·³ (공동 1저자), Christopher Doerrer¹, Bingkun Hu¹, Shengming Zhang¹, Dominic L. R. Melvin¹, Hui Gao¹, Xiangwen Gao¹, Paul Adamson¹, Oxana V. Magdysyuk², **Patrick S. Grant**¹, **Robert A. House**¹, **Peter G. Bruce**¹·⁴\* (lead contact) |
| 소속 | ¹Univ. Oxford · ²Diamond Light Source |
| 서지 | *Joule* **7**, 503–514 (March 15, 2023) · DOI `10.1016/j.joule.2023.02.001` · **Open access CC BY** |
| 일정 | Received 2022-08-22 · Revised 2022-10-13 · Accepted 2023-01-31 · Published 2023-02-24 |
| 자금 | Faraday Institution FIRG026 · EPSRC EP/M009521/1 · Henry Royce Institute EP/R00661X/1, EP/S019367/1, EP/R010145/1 · Diamond 실험 mg26082 |
| 데이터 | Oxford Research Archive **DOI 10.5287/bodleian:kKBPZ282m** |
| 기여 | 분무 증착(Doerrer, Grant 감독) · 싱크로트론(Hu, Zhang, Magdysyuk) · operando PXRD(House) · 원고(Bruce, Spencer-Jolly, Agarwal) |
| 계보 | Samsung **Lee et al., *Nat. Energy* 5, 299 (2020)** (ref 32 — Ag–C 무과잉 Li 전지, 3.2 mA cm⁻² 에서 1,000 사이클 초과) 의 기전 해부. Liao 2025 (정본 `liao2025_interfacial_adhesion_li_plating_carbon_interlayer`) 가 이 논문을 ref 37 로 인용 |

## 3. 핵심 수치 ★

### 3.1 인터레이어 · 셀 제원

| 항목 | 값 | 출처 |
|---|---|---|
| 조성 (질량) | **Ag 나노입자 22.5 wt% · 흑연 67.5 wt% · PVdF 10 wt%** (Ag : 흑연 = 1 : 3 질량비, PVdF 비는 Lee 2020 과 동일) | Experimental |
| 조성 (부피) | **Ag 5.7 vol%** (Lee 2020 과 비슷) | p504 |
| 입자 크기 | **Ag · 흑연 모두 미기재** | — |
| 제조 | PVdF 용액(IPA 97 % + NMP 3 % 부피) 에 Ag+흑연 현탁 → 초음파 → **Ar 분무 증착**(자작 장치) → 110 °C 로 가열한 **스테인리스 CC** 위, **10 × 10 cm²** 시트 → 펀칭 → 70 °C 진공 건조 | Experimental |
| 인터레이어 두께 | **5 µm (± 1 µm)** | Experimental |
| **SE 와의 접합** | 인터레이어를 **Li₆PS₅Cl 분말(AMPCERA) 에 대고 400 MPa 단축 압착** → 한 면에 층이 붙은 SE 원판 | Experimental |
| 상대극 | Li 박 **50 µm** 압착 · 고율 셀은 **지름 5 mm Li** (상대극 공동화 기여를 줄이려고) | Experimental |
| **적층압 (운전)** | **2 MPa** (전 조건) · operando 셀은 원뿔 스프링 | Experimental |
| 온도 | 저율 **상온** · 고율 **60 °C** | Experimental |
| 흑연 삽입 용량 | **≈0.28 mAh cm⁻²** | Experimental |
| Ag 합금 최대 용량 | **≈0.60 mAh cm⁻²** | Experimental |
| 충전 용량 | 항상 위 둘을 **초과** (→ Li 금속 석출 보장) | p504 |

### 3.2 전기화학 수치

| 항목 | 값 | 출처 |
|---|---|---|
| 저율 operando | **30 µA cm⁻²** (상온) | p504, Fig. 1 · Fig. 3 |
| 1 구간 (계면상 형성) | 회절 변화 없이 전위가 **≈0.4 V** 까지 하강 = **황화물 전해질 환원** | p504 |
| LiC₁₂ 평탄부 | **≈105 mV** (25.5° 봉우리 출현) | p505 |
| 고율 operando | **2 · 4 mA cm⁻²** (60 °C, Diamond I12) | Fig. 4 |
| **CCD** | **2.0 mA cm⁻² 안정 · 2.5 mA cm⁻² 단락** — 흑연 단독 = Ag–흑연 (2.0 mAh cm⁻², 60 °C) | Fig. 5 · p507 |
| 4 mA cm⁻² | 단락 (본문 "≈0 V 로 급락") — 6 mAh cm⁻² 후 단면에서 **인터레이어/SE 계면에 Li 금속 핵생성 + Li–Ag 합금** | Fig. 4B · Fig. S3 |
| SEM/EDX 조건 | **0.1 mA cm⁻² · 2 mAh cm⁻² · 60 °C** | Fig. 6 · Fig. S4 |
| Samsung 원조 성능 (인용) | 1,000 사이클 초과 @ 3.2 mA cm⁻² | p503 (ref 32) |

### 3.3 회절 봉우리 (본문 명시, Cu Kα 환산 2θ)

| 상 | 2θ (°) | 비고 |
|---|---|---|
| 흑연 | **26.6** (논문 표기 "003") | 리튬화 시 저각 이동 |
| Ag | **38.3 · 44.1** | 저각 이동 = Li_xAg 고용체 |
| LiC₁₂ | **25.5** | ≈105 mV 평탄부 |
| Li₁₀Ag₃ | **27.4 · 39.1** | 방전 시 고각 이동 = Li₁₀₋ₓAg₃ |
| Li₉Ag₄ | **39.8** (셀 본체 봉우리와 겹침) | 2 mA cm⁻² 충전 |
| Li 금속 | ≈36.4 부근 (Fig. S2a, figure-read ≈) | 2 mAh cm⁻² 후에만 |

### 3.4 ★ Li–Ag 합금화 순서 (저율 30 µA cm⁻², 상온)

**충전** (Fig. 1, 오른쪽 상 막대 figure-read ≈ 시간은 참고용)
1. **계면상 형성** — 회절 변화 없음, 전위 ≈0.4 V (SE 환원; 흑연 단독 음극에서도 보고된 현상).
2. **흑연 리튬화 + Ag 고용** — 흑연 봉우리 저각 이동(층간 팽창), Ag 봉우리도 저각 이동 → **Li_xAg 고용체**. 전압 곡선에 Ag 전기화학 합금화의 흔적 없음(Fig. S1) = Ag 는 **LiC_x 와의 화학 반응**으로만 Li 를 얻는다. 결과: 흑연 곡선이 **용량 방향으로 늘어난다**.
3. **≈105 mV 평탄부** — LiC₁₂ 출현, Ag 봉우리 계속 이동.
4. **LiC₆ 형성** → Li_xAg 고용체가 **LiAg** 로.
5. 더 높은 SOC → **LiAg → Li₉Ag₄ → Li₁₀Ag₃** (상 공존 구간이 길다).
6. **충전 말** — 회절에는 **Li₁₀Ag₃ + LiC₆ 만** 남는다. 그러나 통과 전하가 흑연+Ag 수용량을 넘으므로 **Li 금속**이 생긴다: PXRD 의 약한 Li 봉우리(Fig. S2a), SEM/EDX 에서 인터레이어와 CC 사이로 솟는 두 종류 입자 — Ag 있는 것(Li–Ag 합금) · Ag 검출 안 되는 것(Li 금속으로 명명) (Fig. S2b).

**화학 반응성 검증** (Fig. 2, 액체셀로 만든 LiC_x 를 Ag 나노입자와 6 : 1 질량비로 압착)
- **LiC₂₄ · LiC₁₈ · LiC₁₂ + Ag** → LiC_x 봉우리가 **고각(= Li 감소)** 으로 이동, Ag 봉우리는 저각(Li 고용).
- **LiC₆ + Ag** → **LiAg 생성** + LiC₆ 탈리튬화(LiC₁₂ 봉우리 출현).
- ⇒ **LiC₆ 만이 LiAg 를 만들 만큼 전위가 낮다** — 액체 전해질 흑연·Ag 부하곡선과 일치(refs 38–40).

**방전** (Fig. 3) — **충전의 역순이 아니다**
1. 처음엔 Li₁₀Ag₃ · LiC₆ 거의 불변; 이어 Li₁₀Ag₃ 봉우리(27.4 · 39.1°)가 고각 이동 = **Li₁₀₋ₓAg₃** (Li 결핍) — LiC₆ 는 그대로 ⇒ LiC₆ 에서 전기화학적으로 빠진 Li 를 **CC 쪽 Li · Li₁₀Ag₃ 가 즉시 화학적으로 보충**.
2. Li₁₀₋ₓAg₃ → **Li₉Ag₄**, LiC₆ → **LiC₁₂**, **LiAg** 출현.
3. LiC₁₂ → 흑연; LiAg 가 **CsCl 형 → UPb 형** 구조로 전이 (Li 결핍일 때 UPb 형이 더 안정 → 방전에서만 나타나는 이유로 해석, ref 41).
4. **방전 말: 흑연 + Ag 만**.

### 3.5 고율 (60 °C, Fig. 4)
- **2 mA cm⁻²** — 흑연 먼저 리튬화, **Ag 봉우리 초기 불변**(삽입이 화학 반응보다 빠름). LiC₆ 형성 후에야 Ag → LiAg → Li₁₀Ag₃, Li₉Ag₄ 흔적(39.8°). **Li 금속 형성**.
- **4 mA cm⁻²** — LiC_x (x > 6) 가 더 오래 지속, LiAg 흔적은 있으나 **Ag 가 충전 내내 잔존**. **단락** (Fig. 4B: figure-read ≈0.72 h 에서 전압 급변 + 요동; 이 digest 의 확대 판독으로는 ≈ −1.5 V → ≈ −0.6 V 로 튀고 이후 ≈ −1 V 부근 요동 — 캡션의 *"≈0 V 로 급락"* 보다는 작은 변화, §10-5).
- 저율 대비: 더 많은 **Li 금속**, Li-결핍 합금이 **더 높은 용량까지** 지속.

### 3.6 형태 (Fig. 6 · Fig. S4, CC 를 조심스럽게 떼어 인터레이어 윗면을 봄)

| | 흑연 단독 | Ag–흑연 |
|---|---|---|
| 초기 | 균일 탄소 | 탄소 + 흩어진 Ag 뭉치 |
| **충전 (2 mAh cm⁻²)** | Li 금속이 **벌집(honeycomb) 모양으로 불균일** — 탄소 EDX 에 큰 검은 영역 (스케일 20 µm) | CC 쪽 층이 **균일**, Ag 신호가 면 전체에 고르게 = **Li₁₀Ag₃ + Li** 층 (단면: 인터레이어와 CC 사이에 Ag 함유 층, Fig. S4b) |
| **방전 후** | **Li 가 인터레이어 위에 남는다** | 대부분 Li₁₀Ag₃ 가 층 안으로 복귀, **거의 초기 상태**; 단 탄소-없는 검은 영역이 남은 Ag 영역보다 넓다 → Li 또는 Li-rich 합금 일부 잔존 |
| 단면 두께 (figure-read ≈, 스케일 2 µm) | 흑연층 → LiC₆, 위에 Li 층 | 흑연층 → LiC₆, 위에 Li/Ag 층 |

## 4. 방법 ★ (실험 — 시뮬레이션 없음)

### 4.1 시뮬레이션 — **없음** (DEM/MPM/FEM/DFT 0 건)
- **입자 처리 ★**: n/a. 실물은 흑연 입자(크기 미기재) + Ag 나노입자(크기 미기재) + PVdF 10 wt% 의 5 µm 분무층.

### 4.2 operando PXRD
- **저율 (30 µA cm⁻²)**: Rigaku SmartLab 3 kW, **Cu Kα, 반사** 배치. Rigaku 셀 — **Al 코팅 Be 창**을 **1 µm Cu 박(CC 겸 창 보호)** 이 덮고 그 위에 Ag–흑연 면을 누른다. 원뿔 스프링으로 적층압 (Fig. S5 모식).
- **고율 (2 · 4 mA cm⁻²)**: Diamond **I12 (JEEP)**, **투과**, X선 **56 keV**, 빔 **50 µm**, 자작 튜브 셀; 2θ 는 Cu Kα 환산.
- ex situ: Rigaku MiniFlex (N₂ 글러브박스, Cu Kα, 저배경 Si 홀더).
- 셀 봉우리·Li₆PS₅Cl 봉우리는 그림에 **빨간 눈금**으로 표시.

### 4.3 기준 LiC_x
코인셀(흑연 | Li, 1 M LiPF₆ EC/DMC 50 : 50) 을 10 mA g⁻¹ 로 충전 → 분해·DMC 세척·진공 건조 → PXRD 로 상 확인 → **LiC_x : Ag = 6 : 1 (질량)** 압착 → 분쇄 → PXRD.

### 4.4 SEM/EDX
Ar 글러브박스에서 해체, **스테인리스 CC 를 조심스럽게 제거**(ref 53 방법) → Gatan 기밀 이송 → Zeiss Merlin SEM · Oxford X-max 150 EDX · Aztec. Li 는 EDX 로 직접 못 보므로 **탄소 신호가 없는 검은 영역 = Li** 로 추론.

### 4.5 전기화학
Gamry 1010E · Biologic VMP3. anodeless 반쪽셀(Ag–흑연 | Li₆PS₅Cl | Li).

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1 | operando PXRD 충전 (30 µA cm⁻²): 2θ 19–29° · 35–45° 색지도 vs 시간(≈0–67 h), 전압 곡선(1.5 → 0 V), 오른쪽 **상 막대**(Li-흑연: Li_xC → LiC₂₄ → LiC₁₈ → LiC₁₂ → LiC₆ · Li-Ag: Ag → Li_xAg → LiAg → Li₉Ag₄ → Li₁₀Ag₃ · Li) — 분홍 = 계면상 형성, 파랑 = 삽입+화학 합금화+Li 석출 | ★ **운전 중 인터레이어의 실제 상 조성** — 점착 트랙의 "리튬화 계면(DFT 요청 P3)" 근거 |
| 2 | ex situ PXRD 20–40°: Ag · C · LiC₆/LiC₁₂/LiC₁₈/LiC₂₄ (+ Ag 혼합 전·후) — LiC₆ + Ag 에서만 **LiAg** 봉우리(≈28°, 빨간 원) | 화학 반응 경로의 직접 증거 (전기화학 아님) |
| 3 | operando PXRD 방전 (30 µA cm⁻², ≈0–35 h): Li₁₀₋ₓAg₃ · Li₉₋ₓAg₄ · LiAg(CsCl) · **LiAg(UPb)** · Ag, 흑연 역순, Li 막대는 ≈8.5 h 에 소진 (figure-read ≈) | 방전 비대칭 — 합금 상 이력 |
| 4 | 60 °C 고율 operando: **A) 2 mA cm⁻²** (0–3 h, 전압 figure-read ≈ −0.3 V) · **B) 4 mA cm⁻²** (0–0.9 h, ≈0.72 h 에 "Dendrite penetration") | 속도가 합금화 대 Li 석출의 몫을 바꾼다 |
| 5 | 60 °C 충전 곡선 (2.0 mAh cm⁻²): **A) Ag–흑연 2.5 mA cm⁻² → 덴드라이트** (≈1.5 mAh cm⁻² 이후 전압 요동) · **B) 흑연 2.0 안정** · **C) Ag–흑연 2.0 안정** | **Ag 는 CCD 를 올리지 않는다** |
| 6 | SEM + EDX(C 주황 · Ag 청록) 윗면: 흑연 A 초기 · **B 충전(벌집 Li, 20 µm)** · C 방전(Li 잔존) / Ag–흑연 D 초기 · **E 충전(균일 Ag = Li₁₀Ag₃ + Li)** · F 방전(거의 초기) | ★ **CC 쪽 석출층의 균일성** — CC/인터레이어 계면이 열리는 방식 |
| S1 | Ag 단독층 vs 흑연 단독층 충전 곡선 (30 µA cm⁻²): Ag 는 ≈0.1 V → 0 V 로 천천히, 흑연은 ≈0.22 mAh cm⁻² 에 0 V (figure-read ≈) | 복합층 곡선에 Ag 전기화학 흔적이 없다는 비교 기준 |
| S2 | a) Li 봉우리(≈36.4°): 초기 없음 / 2 mAh cm⁻² 후 있음 · b) SEM + Ag EDX — **Ag 신호 없는 어두운 석출물 = Li 금속** (노란 화살표) | Li 금속 동정 근거 (약하다) |
| S3 | 4 mA cm⁻² · 6 mAh cm⁻² · 60 °C 파괴 단면: **Li 금속 핵생성 + Li–Ag 합금이 인터레이어/SE 계면에** · C · S · Ag EDX | 고율에서는 석출 위치가 **SE 쪽으로** — Liao 에너지 수지의 수송 항 |
| S4 | 단면 SEM/EDX(Ag · C · S): Ag–흑연 초기/충전(층 위 **Li/Ag**, 흑연 → LiC₆) · 흑연 초기/충전(층 위 **Li**) | CC 쪽 석출층의 두께·연속성 |
| S5 | 반사 operando 셀 모식 (스테인리스 본체 · 클램프 · PTFE 절연 · 1 µm Cu · Al 코팅 Be 창 · 스프링) | 적층압 부가 방식 |

### 5.1 크롭 색인 — `litdb/figures/spencerjolly2023_ag_graphite_interlayer_operando_xrd/`

| 파일 | 대상 | 확인 |
|---|---|---|
| `fig_1.png` … `fig_6.png` | 본문 Fig. 1–6 (**본문 그림 6개 = 크롭 6장**) | 6장 전부 Read 로 봄 |
| `fig_S1.png` … `fig_S5.png` | SI1 Supplementary Fig. 1–5 (5장) | 5장 전부 Read 로 봄 |

추출기(캡션 앵커)가 처음 잘라낸 본문 크롭에는 **저널 머리 로고(Joule / CellPress)** 가, SI 크롭에는 **머리 띠 이미지**가 딸려 들어와 있어 **내장 그림 이미지 경계로 다시 잘랐다**(300 dpi, figures.json 에 `recrop` 표기). SI2 는 Joule 표준 보고 양식(체크리스트)이라 그림이 없다. 본문 서술과 어긋난 그림 = **Fig. 4B** (캡션 "≈0 V 로 급락" ↔ 그림의 전압 변화 폭, §10-5).

## 6. Post-processing ★

- **operando 색지도**: 2θ × 시간 강도 지도 + 같은 시간축 전압 곡선 + 상 존재 막대(정성). 봉우리 **이동 방향**(저각 = 격자 팽창 = Li 고용)과 **출현/소멸**로 상 순서를 판정. 정량 상분율(Rietveld 등)은 **없음**.
- **SEM/EDX**: 원소 지도로 Ag·C 분포, **C 신호 부재 = Li** 추론.
- 통계(셀 수·재현 횟수) **미기재**.

## 7. 우리 대비 — Ag–C 인터레이어 점착 트랙 (작업 브랜치 `docs/adhesion_agc_interlayer_20260923.md`) + DEM+MPM (→ `our_dem_baseline.md` 는 정본에 값 0 개 자리표시)

| 항목 | 이 논문 | 우리 (트랙 문서 · 정본 카드) | 같은가 / 다른가 · 이유 |
|---|---|---|---|
| 계면 ① LPSCl ↔ Ag–C | 400 MPa 공압착 접합, 운전 중 SE 쪽 탄소는 **LiC₆**, Ag 는 Li–Ag 합금 | 트랙 §0 ① · DFT 요청: pristine vs 리튬화 계면 (P3) | ★ **이 논문이 P3 의 직접 근거** — 충전 상태의 SE 쪽 면은 흑연이 아니라 **LiC₆ + Li_xAg/LiAg…**. W_ad 를 pristine Ag‖LPSCl 만으로 내면 운전 조건을 대표 못 한다 |
| 계면 ② Ag–C ↔ VGCF | 흑연 호스트 (VGCF 아님) | 트랙 §0 ② | Ag 가 **탄소와 화학적으로 Li 를 주고받는** 관계(LiC_x + Ag → Li_xAg) — Ag↔탄소 계면은 운전 중 **반응 계면**이다. 트랙 §4 가설(흑연 위 Ag = 물리흡착 급)은 **pristine** 에 대한 것 |
| 🆕 계면 ③ 인터레이어 ↔ **CC** | 저·중율에서 **Li₁₀Ag₃ + Li 가 인터레이어와 CC 사이에** 석출 = 이 계면이 **열린다** | 트랙 문서에 **없음** | ★ **트랙에 세 번째 계면을 추가해야 한다** — Liao 2025 의 "약한 계면이 벌어진다" 기준과 합치면, CC 쪽 석출은 CC/인터레이어 계면이 **더 약할 때** 일어난다 |
| 탄소 종류 | **흑연** (입자 크기 미기재) | 트랙 §3 DEM 박리: "Ag 입자 + **카본블랙**" | 다름 — Samsung 원조(카본블랙)와 이 논문(흑연)의 차이. DEM 은 **탄소 형태(판상 흑연 vs 응집 카본블랙)** 를 변수로 둔다 |
| Ag 분율 | 5.7 vol% (22.5 wt%) | 미정 | DEM 설계 입력 후보 (Samsung 과 "비슷" 하다고 저자 명시) |
| 제조압 · 운전압 | **400 MPa 공압착 · 2 MPa 운전** | 트랙 §2: 구동압(수~수십 MPa)은 실접촉 면적으로 들어간다 | 점착을 정하는 것은 **제조압(400 MPa)** 이고 운전압은 2 MPa 로 낮다 — Liao(lamination 100–400 MPa, 운전 5 MPa)와 **같은 구도** |
| 점착 수치 | **없음** | DFT W_ad · DEM G_c(P) 계획 | 대조 표적은 Liao 2025 (탄소/LPSCl Γ) · Song 2025 (LPSCl 벌크 G_c) — 이 논문은 **어느 계면이 운전 중 무엇이 되는가**만 준다 |
| 자체 원고 | — | 정본 `ahn2026_cej_agno3_pvp_li3n_anodefree` (AgNO₃–C, 충전 후 XRD **Li₉Ag₄ · Li₀.₉₈Ag₀.₀₂ · Ag**) | 같은 Li–Ag 상 계열. 이 논문 저율 충전 말은 **Li₁₀Ag₃ + LiC₆** — 조건(속도·온도·Ag 형태)이 달라 **상 목록 차이를 결함으로 읽지 않는다** |
| frame[4]/[5] | 실험, 모델 없음 → 교차검증 상대 아님 | — | 가진 반쪽 = **상·형태·CCD**, 없는 반쪽 = **역학(점착·응력·부피변화 정량)** — 우리 트랙이 채우려는 반쪽 |

## 8. 적용 인사이트 (우리 연구에 어떻게)

### ① ★★★ **"어느 상태의 계면" 을 계산할지 정해 준다** — DFT 요청 P3 의 문헌 근거
충전된 Ag–C 인터레이어의 SE 쪽 면은 **LiC₆ + Li-rich Li–Ag 합금**이고, CC 쪽에는 **Li₁₀Ag₃ + Li 금속** 층이 생긴다. 방전 말에야 흑연 + Ag 로 돌아간다. ⇒ W_ad 계산 목록은 최소 **{Ag|LPSCl (pristine), LiC₆|LPSCl 또는 Li_xAg|LPSCl (충전), Li₁₀Ag₃/Li|CC(Cu/SUS)}** 로 잡는 것이 운전 조건을 대표한다. ⚠ 어느 합금 조성이 SE 와 실제로 닿는지는 이 논문이 **직접 보여주지 않는다**(Ag 는 5.7 vol% 라 SE 접촉이 적다고만 말한다).

### ② ★★★ **계면이 셋이다** — 인터레이어/CC 계면을 트랙에 넣는다
Li 가 CC 쪽에 쌓인다는 것은 **CC/인터레이어 계면이 운전 중 벌어진다**는 뜻이다. Liao 2025 는 이 위치가 **탄소/SE 계면 인성 ≳ ≈10 J m⁻²** 일 때 나타난다고 했고, 이 논문의 층은 **400 MPa 로 공압착**(Liao 에서 400 MPa = 41 J m⁻², 단 카본블랙+PVDF 14 %)이다 — **두 논문이 같은 구도로 맞물린다** (이 digest 의 종합, 점착은 이 논문에서 미측정). ⇒ DEM 박리는 **인터레이어/SE** 와 **인터레이어/CC** 를 둘 다 재야 석출 위치 논의에 쓸 수 있다.

### ③ ★★ **속도가 석출 위치를 SE 쪽으로 되돌린다** — 점착만으로는 안 된다
≥ 2.5 mA cm⁻² 에서는 흑연 삽입이 못 따라가 Li 가 **인터레이어/SE 계면**에 석출되고(Fig. S3) 덴드라이트가 SE 를 뚫는다 — **Ag 유무와 무관**. Liao 의 에너지 수지에서 수송 항(ρ_Li⁺)이 점착 항을 이기는 영역이다. ⇒ 점착 트랙의 결론을 "점착이 위치를 정한다" 로 쓰려면 **저·중율 한정**을 붙인다.

### ④ ★ **탄소 확산도가 CCD 를 정한다** (저자 예측) — 우리 VGCF 호스트의 의미
저자 결론: *"carbons with higher Li diffusivities will enable higher rates of dendrite-free charge."* 우리 트랙 ② 계면의 호스트가 **VGCF** 라면, 그 선택의 기계(점착) 측면과 별개로 **Li 확산도** 측면이 CCD 를 좌우한다는 점을 같이 적어야 한다. (값은 이 논문에 없다.)

### ⑤ ★ Ag 의 역할 재정의 — "덴드라이트 억제제" 가 아니라 "균일화·가역화 매개"
Ag 가 있으면 CC 쪽 층이 **균일한 Li₁₀Ag₃ + Li** 가 되고 방전 때 **층 안으로 복귀**한다(Fig. 6E→F). 흑연 단독은 **벌집형 불균일 Li** 가 남는다. ⇒ 점착 관점의 가설(검증 안 됨): 균일한 합금층이 **CC/인터레이어 계면을 고르게 벌리고 다시 닫는다** — DEM 에서 "Ag 분율 → 개구 균일도" 를 재 볼 수 있는 축.

## 9. 인용 가능 문장 (deck/paper 용)

- "In Ag–graphite anodeless interlayers on Li₆PS₅Cl, Li first intercalates electrochemically into graphite; lithiated graphite then reacts chemically with Ag to form increasingly Li-rich alloys (Li_xAg → LiAg → Li₉Ag₄ → Li₁₀Ag₃), and only LiC₆ is reducing enough to form LiAg (Spencer-Jolly et al., *Joule* 2023)."
- "Discharge is not the reverse of charge: Li-deficient Li₁₀₋ₓAg₃ and a UPb-type LiAg appear only on discharge."
- "Ag nanoparticles did not raise the critical current density — graphite-only and Ag–graphite layers both charged stably at 2.0 mA cm⁻² and failed at 2.5 mA cm⁻² (60 °C) — but they made the Li/Li₁₀Ag₃ layer between interlayer and current collector more homogeneous."

## 10. 주의 / 한계 (over-claim 방지) — 비판적으로

1. **점착·응력 미측정** — "합금은 부피변화가 커서 계면 변형·박리를 부른다"(서론, refs 23–25)는 **인용 서술**이고, 흑연 ≈10 % 부피변화도 일반 서술이다. Li–Ag 합금의 부피변화·응력은 이 논문에서 **정량되지 않았다**.
2. **입자 크기 미기재** (Ag · 흑연) — DEM 입력으로 옮길 수 없다. Ag 5.7 vol% 는 명시.
3. **온도 교란** — 저율(상온) vs 고율(60 °C). "고율에서 Li 금속이 더 많다" 는 속도와 온도의 **합성 효과**다.
4. **CCD 통계 부재** — 2.0 안정 / 2.5 단락은 대표 곡선 한 개씩(Fig. 5)으로 제시, 셀 수 미기재. "흑연 단독 = Ag–흑연" 은 **2.0 과 2.5 사이 해상도**에서의 동등이다.
5. **Fig. 4B 캡션과 그림의 어긋남(경미)** — 캡션은 *"sudden drop in cell potential to approximately 0 V"* 인데, 확대해 보면 전압이 ≈ −1.5 V 에서 ≈ −0.6 V 로 튄 뒤 ≈ −1 V 부근에서 요동한다(figure-read ≈). 단락 판정 자체는 Fig. S3 단면이 뒷받침한다.
6. **Li 금속 동정이 간접적** — Li 는 약한 산란체라 PXRD 봉우리가 작고(Fig. S2a), SEM/EDX 는 "Ag 가 검출 안 되는 입자 = Li" 로 명명한다(저자도 미량 Ag 가능성 인정).
7. **셀 차이** — 저율 operando 는 **1 µm Cu** CC + Be 창, SEM 셀은 **스테인리스** CC. CC/인터레이어 계면 거동을 비교할 때 CC 재질이 다르다.
8. **정량 상분율 없음** — 상 막대는 존재 구간의 정성 표시. 합금 상의 양·순서의 시간 경계는 그림 판독값이다.
9. **음극만** — 저자 스스로 *"these performances relate only to the anode"* (복합 양극을 갖춘 anodeless 전전지 아님).

## 11. 논증 흐름 (절별)

1. **서론** — anodeless 는 불균일 석출·덴드라이트가 과제. 얇은 합금층(Mg·Al·Ge·In·Si·Sb·Sn·Au·Ag)은 부피변화로 계면 변형·박리 문제; 흑연은 ≈10 % 부피변화로 작다. Samsung(Lee) 의 Ag–탄소층이 뛰어난 성능 → **작동 중 구조 변화**를 밝히는 것이 목적.
2. **저율 충전 (Fig. 1, S1, S2)** — 계면상 → 흑연 삽입 + Ag 화학 합금화 → LiC₁₂ → LiC₆ + LiAg → Li₉Ag₄ → Li₁₀Ag₃ + Li 금속.
3. **LiC_x–Ag 반응성 (Fig. 2)** — 화학 경로 확인, LiC₆ 만 LiAg 형성.
4. **저율 방전 (Fig. 3)** — 역경로 아님, Li₁₀₋ₓAg₃ · UPb-LiAg.
5. **고율 충전 (Fig. 4, 5, S3)** — 삽입이 화학 반응을 앞지름, Li 금속 증가; 2.5 mA cm⁻² 이상 단락, 흑연 단독과 같은 CCD ⇒ **덴드라이트 저항은 흑연 삽입 속도가 정한다** → 확산도 높은 탄소 제안.
6. **Ag 의 이점 (Fig. 6, S4)** — CC 쪽 Li₁₀Ag₃ + Li 층 균일화 · 방전 시 복귀.
7. **결론** — 위를 요약, 탄소 기반 인터레이어 설계 일반으로 확장.

## 12. 용어 미니 사전

| 용어 | 뜻 |
|---|---|
| **anodeless (anode-free)** | Li 금속 없이 조립, 첫 충전에서 CC 쪽에 Li 를 만든다 |
| **operando PXRD** | 전지를 돌리는 **도중에** 분말 X선 회절을 연속 측정 |
| **LiC_x (x = 24, 18, 12, 6)** | 흑연 층간 화합물의 단계(stage) — x 가 작을수록 Li-rich, LiC₆ 가 완전 리튬화 |
| **Li_xAg 고용체 → LiAg (β) → Li₉Ag₄ (γ) → Li₁₀Ag₃** | Li 함량이 늘수록 나타나는 Li–Ag 상 (이 논문의 관측 순서) |
| **CsCl 형 vs UPb 형 LiAg** | 같은 조성의 두 구조 — Li 결핍일 때 UPb 형이 안정 (방전에서만 관측) |
| **CCD** | 덴드라이트 단락 없이 충전할 수 있는 최대 전류밀도 |
| **화학적 vs 전기화학적 합금화** | 외부 회로 전자 이동 없이 LiC_x 가 Ag 에 Li 를 넘겨주는 반응 vs 전극 전위로 직접 일어나는 합금화 |

## 13. 🧮 파생 · 판독 원장 (`derived(ours)` / figure-read)

- **용량 대비 충전량**: 흑연 0.28 + Ag 0.60 = **0.88 mAh cm⁻²** 가 층의 최대 저장량(본문 두 값의 합, 이 digest 산술) — 모든 충전(2 mAh cm⁻² 등)이 이를 넘어 **≥ 1.1 mAh cm⁻² 는 Li 금속**으로 가야 한다 (Ag 가 전부 Li₁₀Ag₃ 에 도달했다고 가정할 때).
- **Fig. 1 상 막대 (figure-read ≈, 총 ≈67 h)**: Li_xC ≈0–10 h · LiC₂₄ ≈9–12 · LiC₁₈ ≈10–15 · LiC₁₂ ≈12–43 · LiC₆ ≈15–67 / Ag ≈0–8 · Li_xAg ≈8–37 · LiAg ≈18–44 · Li₉Ag₄ ≈22–58 · Li₁₀Ag₃ ≈22–67 / **Li ≈22–67 h**.
- **Fig. 3 상 막대 (figure-read ≈, 총 ≈35 h)**: Li ≈0–8.5 h 소진 · Li₁₀₋ₓAg₃ ≈0–23 · Li₉₋ₓAg₄ ≈12–31 · LiAg(CsCl) ≈23–32 · LiAg(UPb) ≈27–35 · Ag ≈29.5–35 / LiC₆ ≈0–25 · LiC₁₂ ≈12–25 · … · Li_xC₆ ≈26–35.
- **Fig. 5 (figure-read ≈)**: 흑연 단독 2.0 mA cm⁻² 는 ≈0.3 mAh cm⁻² 에서 0 V 아래 평탄 (≈흑연 용량 0.28 과 정합), Ag–흑연 2.0 은 ≈0.25 mAh cm⁻² — **고율에서 Ag 의 용량 연장이 사라진다**는 본문 서술과 정합.
- **Fig. S1 (figure-read ≈)**: 30 µA cm⁻² 에서 흑연 단독은 ≈0.22 mAh cm⁻² 에 0 V, Ag 단독은 ≈0.1 V 에서 0 V 로 2 mAh cm⁻² 에 걸쳐 완만.
