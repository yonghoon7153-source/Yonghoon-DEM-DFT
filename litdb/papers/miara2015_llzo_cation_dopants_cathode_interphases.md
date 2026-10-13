<!-- digest 표준 양식 (paper-level STANDALONE) · 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md
     2026-10-13 신설 (논문 에이전트). 1순위 목적 = 10-13 연구세미나 덱 5장 표 첫 행
     `Miara 2015 (via Anderson) | garnet oxide | one cation, 3 sites | n = 45 | mechanical axis: none` 검증 (§0S).
     그림 4장 + Table 1(이미지) + Table 2(수동 크롭) 를 실제로 보고 썼다. Fig. 3 · Fig. 4 는 픽셀로 다시 읽었다 (§16). -->

# First-Principles Studies on Cation Dopants and Electrolyte|Cathode Interphases for Lithium Garnets — Miara et al. (*Chem. Mater.* **2015**, 27, 4040–4047)

> slug `miara2015_llzo_cation_dopants_cathode_interphases` · DOI `10.1021/acs.chemmater.5b01023` · type `DFT 전용 (PBE·VASP 결함에너지 128 이온종 × Li·La·Zr 3 자리 + Li 개방 grand-potential pseudo-binary 계면 · 실험 0)` · PDF `litdb/inbox/Miara2015 ChemMater First-Principles Studies on Cation Dopants and Electrolyte Cathode Interphases for Lithium Garnets.pdf` (본문 8 pp · SHA256 `64fb9470…adc80` · 한양대 구독 다운로드 2026-10-13) · ⛔ **SI 미보유** (논문엔 `Table S1`–`S3` · `Figure S1` 이 있다 — 사용자 확인: 본문 PDF 만) · digested `2026-10-13` · status ✅ · 태그 **[외부]**

> elements: Li, La, Zr, O, Ta, Co, Mn, Fe, P, Al, Ga, Nb, In, Sn, Sb, Y, Ge, Si, Ca, Sr, Ba, Hf, Zn, Mg, W, Mo, Te, Rb, Ce, Sc, Bi, V, Cr, Ni, Nd
> methods: DFT, ESW

> **저자**: **Lincoln J. Miara\***† (Samsung Advanced Institute of Technology–USA, Cambridge MA) · William Davidson Richards‡ · Yan E. Wang‡ · **Gerbrand Ceder**‡ (‡MIT DMSE) · 교신 Lincoln.m@samsung.com
> Received 2015-03-18 · Revised 2015-04-30 · Published 2015-04-30 · 자금 **SAIT** · 계산자원 XSEDE (NSF ACI-1053575) + NERSC (DOE DE-AC02-05CH11231) · 이해상충 없음 선언
> **PDF 쪽 ↔ 인쇄 쪽**: PDF p.N = 인쇄 p.(4039+N). 이 digest 의 쪽 번호는 **인쇄 쪽**(p. 4040–4047)이다.
>
> **계보**: Miara 2013 *Chem. Mater.* 25, 3048 (Rb/Ta LLZO, 이 논문 ref 13) → **본 논문** → [Rich16] `papers/richards2016_interface_stability_pseudobinary.md` (같은 저자군, pseudo-binary 를 닫힌계·열린계·no-mixing 셋으로 체계화) → [Xiao19] `papers/xiao2019_cathode_coating_screening.md` (ref 35 로 인용) → [Xiao20Rev] `Fig. 4d` (ref 145 로 이 논문의 안정창 막대를 재수록) → [Anderson24] `papers/anderson2024_llzo_comprehensive_dopant_screening.md` (ref [12] 로 이 논문의 결함에너지를 `Fig. 3d` 에 옮겨 그리고 59종을 합성).
>
> ⚠⚠ **산화물 가넷(비-argyrodite)이다.** LLZO = Li₇La₃Zr₂O₁₂, LLTO = Li₅La₃Ta₂O₁₂. 우리는 황화물 argyrodite.
> **결함에너지·반응에너지·전압 숫자를 우리 계 숫자와 같은 표에 놓지 않는다** — 이식 가능한 것은 방법·논증 구조뿐이다 (`comparison_vs_ours.md` §J-60).
>
> **본 digest 에서 실제로 본 그림 (2026-10-13)**: `Fig. 1` `Fig. 2` (전체 + 확대 2곳) `Fig. 3` (+ 픽셀 판독) `Fig. 4` (+ 픽셀 판독) · `Table 1` (텍스트 레이어가 없는 **이미지 표**라 두 쪽으로 나눠 직접 판독) · `Table 2` (수동 크롭 확인) — **크롭 7장 중 6장**.
> 안 본 것: `Table 3` 이미지 (텍스트 레이어로 읽음 — 표는 PDF 텍스트가 정확하다) · 초록 TOC 그래픽 (번호 없음, p. 4040 쪽 렌더로만 봄 — `Fig. 3` 과 같은 LLZO|LCO 곡선).
> 대조용으로 **[Anderson24] `Fig. 3`** (`litdb/figures/anderson2024_llzo_comprehensive_dopant_screening/fig_3.png`) 도 보고 패널 d 를 픽셀로 다시 읽었다 (§11).
> 그림 위치에서 읽은 값은 **`figure-read ≈`**, 그림 안에 **인쇄된 숫자**를 옮긴 값은 **`Fig. 2 인쇄값`** 으로 구분한다.

---

## 0. 이 digest 를 읽는 법

이 논문은 **두 편이 한 PDF 에 붙어 있다.**

| 절 | 질문 | 방법 | 그림·표 |
|---|---|---|---|
| §2 도펀트 안정성 (p. 4041–4043) | 어떤 양이온이 LLZO 의 어느 자리(Li·La·Zr)에 들어가나 | PBE 결함에너지 (도핑 조성이 속한 hull 면의 화학퍼텐셜로 잼) · 2 eV 문턱 | `Fig. 1` `Fig. 2` `Table 1` `Table 2` |
| §3 계면 열역학 (p. 4043–4045) | LLZO·LLTO 가 LCO·LMO·LFP 양극과 전압에 따라 얼마나 반응하나 | Li 개방 grand potential + pseudo-binary 최소화 (eq 2–3) · 0–5 V | `Fig. 3` `Fig. 4` `Table 3` |

**이 digest 의 1순위 목적은 §0S** (세미나 표 첫 행 검증)다. 질문이 오면 §0S 의 쪽·그림·표 번호로 바로 답한다.
2순위는 §7 (우리 ESW · 계면 반응성 작업과의 관계)이고, 거기서 **"같은 이름, 다른 양"** 하나를 새로 잡았다 (§7c).

---

## 0S. ★★★ 세미나 표 검증 — 10-13 덱 5장 첫 행 `Miara 2015 (via Anderson) | garnet oxide | one cation, 3 sites | n = 45 | mechanical axis: none`

> ⛔ 이 절은 세미나 파일을 **고치지 않는다** (사용자가 고친다). 고칠 문장 위치만 7번에 적는다.

### 0S-1. 실제로 계산한 것 — 입력 수 (p. 4041 · `Table 1`)

- **본문 선언 (§2.1, p. 4041)**: *"we consider **128 possible dopant species** (Table 1), each of which can be placed at **three cation sites (Li, La, Zr)**. In addition, there are 3 lithium sites (24d, 96h, 48g) which must also be tested when a dopant is placed on the Li-site, leading to a total of **1152 structures** to be calculated."*
- **`Table 1` 캡션** "(128 total)" · 각주 "A total of 128 were used." (p. 4041)
- **species = 원소 × 산화수** — `Table 1` 은 원소마다 괄호에 산화수를 적는다 (예 `Mn(2,4)` = Mn²⁺·Mn⁴⁺ 두 종).
- **우리 셈 (`Table 1` 이미지 직접 판독)**: 산화수가 적힌 원소 **94** · 원소(산화수) 칸 **122** (2가지 22 원소 · 3가지 3 원소 Cl·Br·I · 1가지 69 원소). ⇒ **인쇄된 칸은 122 로 캡션의 128 보다 6 적다** (§10-2).
  - 산화수 칸이 없는 9 원소 (= 도펀트 아님): He Ne Ar Kr Xe Rn **O F U**.
  - **호스트 원소도 도펀트로 들어 있다** — `Li(1)` `La(3)` `Zr(4)` (다른 자리 antisite).
  - 94 원소 전체: H Li Be B C N Na Mg Al Si P S Cl K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Cs Ba Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Fr Ra Lr La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Ac Th Pa Np Pu Am Cm Bk Cf Es Fm Md No.
- **자리 조합**: 128 × 3 = **384 dopant(site)** (산술 — 본문에 이 수 자체는 없다).
  ⚠ **1152 = 128 × 9** 인데, 본문 규칙(Li 자리일 때만 하위자리 3개)대로 세면 128 × (3 + 1 + 1) = **640** 이다. 9 의 분해는 본문이 설명하지 않는다.
- **농도**: 8 f.u. conventional 초격자 (Li₅₆La₂₄Zr₁₆O₉₆, **192 원자**) 에 도펀트 **1 개** = 0.125 pfu. 농도 축은 없다 (한 농도).
- **결과가 실제로 지면에 나온 원소** (`Fig. 2`, p. 4043): 값이 인쇄된 원소 **73** + 판독 불가 2 (Np·Pu — §10-5). `Table 1` 에는 있지만 `Fig. 2` 가 **빈칸인 원소 16**: Re Os Po At Fr Ra Lr **Yb** Am Cm Bk Cf Es Fm Md No (+ 호스트 Li·La·Zr). 전 원소의 3 자리 값은 SI `Table S3` 에 있다고 한다 (미보유).
- **음이온 자리 치환: 0 건.** O 자리는 한 번도 바꾸지 않는다 (O·F 는 산화수 칸 없음). N·P·S·Cl·Br·I 는 **양의 산화수 양이온**으로만 Li/La/Zr 자리에 들어간다 (`Fig. 2`: Cl⁵⁺·S⁴⁺·P³⁺ 는 Zr 자리, Br³⁺ 는 Li 자리).
  ⇒ `kb/open_items.md` A1 할 일 4 *"45종의 음이온 자리 도핑이 있는지"* 의 답 = **없다.** 우리 "화합물 하나가 양이온·음이온 두 자리를 같이 채운다" 는 이 논문과 겹치지 않는다.

### 0S-2. '45' 의 근거 — **Miara 본문에 45 는 없다**

- **8 쪽 전문 텍스트 검색**: "45" 는 참고문헌 번호(ref 45 = Rettenwander 2014)와 서지 쪽수에만 나온다. **"45 종" · "추가 45" 에 해당하는 문장·표·그림이 없다.**
- **Miara 의 판정 기준** (§2.2, p. 4042): **E_defect < 2 eV**. 문턱 근거 = *"합성된 도펀트 중 계산 결함에너지가 가장 높은 것"* 을 고르는 실험 앵커 방식 — **Ce⁴⁺(La) 1.60 eV** 가 최고였고, *"to broaden our search"* **Te⁶⁺(Zr) = 2 eV** 로 넓혔다 (Te 는 LLZO 에 시도된 적 없고, 근거는 유사 가넷 Li₃₊ₓNd₃Te₂₋ₓSbₓO₁₂, ref 47).
- **Miara 의 집계는 전부 dopant(site) 조합 단위다** — *"dopants are allowed to be stable on multiple sites and in multiple oxidation states"* (p. 4042). 원소 수가 아니다.

| 집계 (원문) | 값 | 위치 |
|---|---|---|
| E_defect < 2 eV 인 조합 (전체) | **108** = Li 15 · La 27 · Zr 66 | `Table 2` (p. 4043) |
| 같은 것, V·Cr·Mn·Fe·Co·Ni 제외 (괄호) | **92** = 10 · 25 · 57 | `Table 2` |
| 그중 등원자가 (Li 수를 못 바꿔 입방상 안정화 못 함 → 제외 대상) | **37** | p. 4042 · `Table 2` (0 + 18 + 19) |
| 비등원자가 중 3d 원소 포함 | **25** | p. 4042 |
| 비등원자가 · V–Ni 6 원소 제외 = **저자 최종 후보** | **59** | p. 4042 · `Table 2` 괄호 (10 + 9 + 40) |

- **원소 단위로 다시 센 것 (우리, `Fig. 2` 선호 자리)**: E < 2 eV 원소 **57** (V = 2.000 은 경계라 제외 · 58 이면 포함).
- **45 를 주는 자연스러운 셈이 없다** — 시험한 것 (원소 단위는 전부 `Fig. 2` 기준): 값 있는 원소 73 · < 2 eV 원소 57 · 57 에서 [Anderson24] 기보고 30 을 뺌 = 29 (기보고 중 B·Si 는 2 eV 밖이라 28 개만 빠짐) · 73 에서 기보고 30 을 뺌 = 43 · 57 에서 Miara 서론의 기시도 14 원소를 뺌 = 44 (Si 는 2 eV 밖이라 13 개만 빠짐) · 59 (조합). **단위가 섞인 59(조합) − 14(원소) 만 45** 다 — 기시도 14 중 Sn⁴⁺·Hf⁴⁺·Ge⁴⁺(Zr)·Y³⁺(La) 는 등원자가라 59 에 들어 있지도 않으므로 **근거로 쓰면 안 된다**.
- **[Anderson24] 의 인용** (우리 digest §3a): *"ref [12] = Miara … 가 'LLZO 가 이론적으로 추가 45 종을 수용할 수 있다' 고 예측"* → **Miara 원문의 어떤 수와도 대응하지 않는다.** SI `Table S2` (2 eV 통과 목록)를 원소 단위로 다시 센 수일 가능성은 남지만 **SI 미보유로 확인 불가**. ⇒ **45 는 Anderson 의 수다.**
- 덧붙여 **[Anderson24] 의 '신규 30' 중 9 종은 Miara 의 2 eV 문턱 밖이다**: Na 2.340 · K 2.360 · P 3.550 · V 2.000 · Ag 2.750 · Cs 3.100 · Au 2.390 eV (`Fig. 2 인쇄값`) + 값 없음 Re·Yb. 그리고 신규로 분류된 **In·Sn 은 Miara 서론 (p. 4040) 이 이미 '시도된 도펀트' 로 꼽은 원소**다. ⇒ *"Anderson 의 신규 = Miara 예측 명단"* 도 그대로는 성립하지 않는다.

### 0S-3. 계산 설정 (§2.1 · §3.1, p. 4041–4044)

| 항목 | 값 | 원문 위치 |
|---|---|---|
| 코드 | **VASP** (ref 42) | p. 4042 |
| 범함수 | **PBE-GGA** — ⚠ ref 41 은 PBE0 하이브리드 논문 (*J. Chem. Phys.* 105, 9982) 이다. 본문 서술은 GGA 라 GGA 로 읽는다 (§10-6) | p. 4042 |
| PAW | PAW (ref 43, Blöchl) · 원자별 데이터셋 n/a | p. 4042 |
| **U 값** | **n/a — DFT+U 언급 0** (Fe·Co·Mn 도펀트와 LCO·LMO·LFP 양극을 계산하는데도) | — |
| 스핀 분극 | n/a (언급 0) | — |
| 컷오프 | **500 eV** | p. 4042 |
| k 점 | **밀도 ≥ 1000 / (단위셀 원자 수)** (k-points per reciprocal atom 식) — 192 원자 셀이면 ≥ 5.2 점 (산술). 실제 메시 n/a | p. 4042 |
| 초격자 | **8 f.u. conventional cell, Li₅₆La₂₄Zr₁₆O₉₆ = 192 원자** · 격자상수·이완 조건 n/a | p. 4041–4042 |
| 무질서 처리 | ICSD **422259** (Ia-3d) 에서 시작, 점유율 Li(1) 24d **0.417** · Li(2) 96h **0.479** 채택 → **Ewald 정전기 에너지**로 Li 배열 선별 (24d–96h 최근접 동시 점유 없음) → 정전기 최저 **100 배열을 DFT** → DFT 최저 **1 배열**을 바닥상태로. 도핑은 그 1 배열 위에서 | p. 4041–4042 |
| 결함에너지 정의 | **Eq. [1]** `E_defect = E_pure − E_doped + Σ Δn_i μ_i` (인쇄 그대로 — 부호 문제 §10-1). Δn_i = 도핑·전하보상으로 넣거나 뺀 i 원자 수 | p. 4041 |
| **기준 화학퍼텐셜** | **도핑 조성을 포함하는 다상 평형(hull 면)에서의 기울기** — *"the slope in the direction of element i in the phase diagram"*. 원소 기준(금속·O₂)도 고정 저장고도 아니다. pymatgen 으로 계산 (ref 37) | p. 4041 |
| 상평형도 | 각 도펀트마다 **Li–La–Zr–O–M 5원계의 모든 화합물** 계산: ICSD (ref 38) + **data-mined 치환 규칙으로 만든 가상 구조** (ref 39, Hautier 2011) | p. 4041 |
| **전하 보상** | **Li 양을 조절한다** — 빈자리는 에너지가 가장 높은 Li 자리에서 빼고, 침입 Li 는 가장 낮은 자리에 넣는다 (**정전기 에너지 기준**, ref 36 Ewald). 예 Al³⁺(Li) = Li 3 개 제거. 범위 Li₆.₂₅A₀.₁₂₅La₃Zr₂O₁₂ (6+ 가 Li 자리) ~ Li₇.₃₇₅La₃Zr₁.₈₇₅M₀.₁₂₅O₁₂ (1+ 가 Zr 자리) | p. 4041 |
| 엔트로피·온도 | **무시** — *"Determination of the exact entropic contribution … is beyond the scope"* | p. 4042 |
| AIMD · NEB · MLIP · 밴드갭 · DOS | **없음** (MD 는 문헌 인용 문맥에만, ref 13·54–56) | — |
| 계면 계산 | Li 개방 grand potential `φ_hull(c, μ_Li)` (eq 2) · pseudo-binary `Δφ(μ_Li)` (eq 3) · x ∈ [0, 1] · **0–5 V** (−5 eV < μ_Li < 0) · 상평형 Li–La–Zr–O · Li–La–Ta–O · 양극계 (ref 52 Ong 2008 방식) | p. 4043–4044 |

### 0S-4. 기계·탄성 물성 — **없다** ✓

본문 전문 텍스트 검색: elastic · modulus · mechanical · stiff · hardness · bulk modulus · shear · fracture · strain · stress · lattice parameter · volume → **0 건**.
다룬 축은 **결함에너지(용해 열역학)** 와 **계면 반응 열역학** 두 개뿐이다. ⇒ 표의 **`mechanical axis: none` 은 맞다.**

### 0S-5. 후반부 — 전해질|양극 계면 (§3–§4, p. 4043–4045)

근거 그림·표: `Fig. 3` · `Fig. 4` · `Table 3`.

- **무엇과 반응시켰나**: 전해질 **LLZO · LLTO** × 양극 **LiCoO₂ (LCO) · LiMnO₂ (LMO — 스피넬 LiMn₂O₄ 가 아니다) · LiFePO₄ (LFP)**. Li 저장고에 열린 grand potential 로, 두 조성을 x : (1 − x) 로 섞어 반응에너지가 가장 음인 x 를 찾고 (eq 3), 이를 **0–5 V 에서 반복**한다.
- **3 V 결과 (`Table 3`)**: 반응성 크기 **LFP > LMO > LCO**, 모든 양극에서 **LLZO > LLTO**.
  LLZO|LCO **−33.37** · LLZO|LMO **−108.9** · LLZO|LFP **−181.17** · LLTO|LCO **−10.54** · LLTO|LMO **−56.45** · LLTO|LFP **−124.41** meV/atom.
  기전: 전해질에서 **Li·O 가 빠져** 양극이 Li 을 얻고 산화 → **Li₂MO₃** (M = Co, Mn); LFP 는 P 가 **Li₃PO₄** 로, Fe 는 Fe₂O₃·LaFeO₃ 로.
- **전압 의존 (`Fig. 4`)**: 안정창 (figure-read ≈) **LLZO 0.47–3.39 V · LLTO 0.92–3.54 V** · LCO ≥ 1.93 · LMO ≥ 1.47 · LFP ≥ 2.26 V. 반응 구동력 극소는 **전부 3.17–3.44 V** — 가넷 창 위 끝 바로 아래 (*"The biggest driving force … at the edges of the intrinsic stability windows"*). 3.8 V 위에서는 평탄. < 2 V 에서 LLTO 는 양극과 Li₂O + 합금 (TaCo₃·TaMn₂) 을 만든다 (`Table S1`, 미보유).
- **결론**: (i) **LCO 가 가넷과 가장 덜 반응** (*"LCO is a good choice"*) · LFP 가 가장 반응 (Li₃PO₄ 가 보호층이 될 수도 — 단 철 산화물이 전자 경로를 안 만들 때). (ii) 실험의 엇갈림 (LLZO|LCO 계면 저항 큼 vs 없음) 을 **"상온에선 La·Zr·Co 가 못 움직이고, 고온 공소결에서 열역학 구동력대로 상호확산·분해"** 로 설명 — Co³⁺(Zr) 도핑 LLZO 가 La₂O₃ + Li₆Zr₂O₇ + Li₈CoO₆ 로 분해 (`Table S3`, 미보유) = Kim et al. (ref 57) 관측과 정합. (iii) 최종 문장: *"the electrolyte|cathode interphase is more sensitive to chemical decomposition at high sintering temperatures than it is to electrochemical decomposition during cycling."*
- **우리 작업과의 관계** (상세 §7):
  1. **안정창 = 우리 ESW 와 같은 구성** (Li 개방 grand potential 에서 그 상이 안정한 μ_Li 범위). 숫자는 계가 달라 비교 금지 — 우리 comp1 은 1.717–2.256 V (하한 1.717 = Li 교환 0 인 경계 · 라벨 규약 `HZ-esw-reduction-limit-label` CONDITIONAL).
  2. **eq 3 = 우리 `tools/oxidation/interface_reactivity_v2.py` 와 같은 Li 개방 pseudo-binary 지만 "혼합분만" 이다** — 반응물을 각자의 grand-potential hull 값으로 재므로 끝점이 0 이다. 우리 v2 는 `include_no_mixing_energy=True` 라 **전해질 자체 분해분이 들어간다** (pymatgen 원본에서 확인, §7c). ⇒ **같은 이름, 다른 양.** 숫자·곡선 모양을 맞대지 않는다.
  3. **출처 라벨**: Li 개방 혼합 반응식은 litdb 범위에서 **이 논문 (eq 3, 2015-04) 이 처음**이다 — [Rich16] 보다 앞서고, Kim 2026 SI eq 8 각주와 Nolan 2018 ref 69 가 이 논문을 원전으로 단다 (`comparison_vs_ours.md` §I).

### 0S-6. [Anderson24] digest 와의 대조 (상세 §11)

| # | Anderson digest 서술 | Miara 원문 / 우리 재판독 | 판정 |
|---|---|---|---|
| a | §3b (정정 전 113–116행) · §11 Figure set `3d` 행: *"Lu 는 `n/a` (ref [12] 에 값 없음)"* | [Anderson24] `Fig. 3d` x 라벨 순서는 `… Er, Tm, n/a, Lu, Bi` — **n/a 는 Yb 자리**다. Lu 는 값이 있다 (La figure-read ≈ 0.92 = Miara `Fig. 2 인쇄값` Lu³⁺(La) **0.930**) | 🔴 **Anderson digest §3b 오기** (§19.6 은 맞다: Yb n/a · Re 없음 → 57). 세미나 메모의 *"(Lu n/a · Yb 미포함)"* → **"(Yb n/a · Re 미포함)"**. Miara `Fig. 2` 도 Yb·Re 빈칸 = 정합 |
| b | §3a: *"계산 예측 45 종"* | Miara 본문에 없음 (0S-2) | 🔴 Anderson 의 수 |
| c | §3b·§19.4: 결함에너지 = Miara 인용값 3 점 | **최소값 57/57 이 Miara `Fig. 2` 와 일치** — \|Δ\| 중앙 **0.03** · 최대 **0.12 eV** (B — 마커 겹침) | ✅ 충실한 전사 |
| d | 산화수 첨자 (Fe3 V5 Cr3 Mn4 Co4 Ni2 Se4 Mo4 Ru4 Pd4 Sn4 Te4 Ce4 W4 Ir4 Pt4 Pb4) | 17 개 전부 Miara `Fig. 2` 선호 산화수와 같다 | ✅ |
| e | (digest 에 없음) | 🔴 **Al(La)**: [Anderson24] `Fig. 3d` figure-read ≈ **4.04 eV** ↔ Miara 본문 **3.16 eV** (p. 4042) — **0.88 eV 차**. 같은 Al 의 Li 1.32 ↔ 1.36 · Zr 1.84 ↔ 1.87 은 맞다 | 비선호 자리를 본문으로 대조할 수 있는 원소는 Al 하나 (+ Ce⁴⁺(La) 1.60 ↔ 1.56 ✓). 원인 (Miara `Table S3` 값이 본문과 다름 / Anderson 전사 오류) 확인 불가 |
| f | §4d: *"code/functional/셀 크기/U 값 이 논문에는 전혀 없음"* | Anderson 에 대해서는 맞다. 이제 Miara 원문으로 채운다 (0S-3) — **U 는 Miara 에도 없다** | ✅ 보강 |
| g | §3a: 신규 29(→30) 의 원천 = Miara 예측 | 신규 30 중 9 종이 Miara 2 eV 밖 · In·Sn 은 Miara 기준 '기시도' | ⚠ 원천 서술 약화 |

### 0S-7. 세미나 표 첫 행 권고 (사용자 결정 사항)

| 칸 | 지금 | 권고 | 근거 |
|---|---|---|---|
| **n** ('검토한 후보 수') | 45 | **128** | `Table 1` 캡션 "(128 total)" · §2.1 첫 문장 (p. 4041). 단위 = 도펀트 이온종 (원소 × 산화수), 각각 3 자리. 다른 행도 논문 자신이 인쇄한 수를 쓰므로 128 이 같은 결이다. 원소로 세고 싶으면 94 (우리 셈) · 구조로 세면 1,152 (같은 쪽). 384 (조합) 는 산술값이라 비권고 |
| **(via Anderson)** | 붙어 있음 | **n 을 128 로 바꾸면 뗀다** | host · varied · n · mechanical 네 칸이 전부 Miara 원문에서 직접 나온다. ⛔ **45 를 남기면 떼면 안 된다** — 45 는 Anderson 의 수다 |
| host | garnet oxide | ✓ 그대로 | 입방 LLZO (Ia-3d, ICSD 422259). LLTO 는 계면 절에만 |
| what is varied | one cation, 3 sites | ✓ 그대로 (풀어 쓰면 *"one ion species (element × oxidation state), three cation sites, Li-compensated"*) | §2.1. 전하 보상을 Li 로 하는 것은 우리와 같으므로 대비점이 아니다 |
| mechanical axis | none | ✓ 그대로 | 0S-4 |

- '(via Anderson)' 을 떼면 **표 안에서는** Anderson 인용이 필요 없어진다. 대본·디펜스에서 Anderson 을 말한다면 우상단 참고문헌의 `Adv. Energy Mater., 14, 2304025 (2024)` 는 남긴다 — 사용자 결정.
- **디펜스 메모에서 고칠 문장** (`kb/seminars/Research_Seminar_2026_10_13_cascade_defense_ko.md` — 내가 고치지 않았다 · 줄 번호는 커밋 `0ae806f` 기준이고 파일이 계속 바뀌므로 **인용 문구로 찾는다**):
  - 121행 *"Anderson 의 후보 풀 = 기존 실험 30 + Miara 예측 45"* — Anderson 의 서술이지 Miara 의 수가 아니다.
  - 127행 *"45 는 Miara 2015 가 DFT 결함에너지로 예측한 도펀트 수"* — 원문에 없다 (0S-2).
  - 133행 *"결론: LLZO 가 추가로 45 종을 받아들일 수 있다"* — 원문 결론 문장이 아니다. 원문은 *"Several novel dopants emerge such as subvalent Sc³⁺ and Mg²⁺ on the Zr-site"* (p. 4045).
  - 134행 *"Miara 가 실제로 계산한 원소는 더 많다 (Anderson Fig. 3d 에 … 57 종)"* → 원문 기준 **128 이온종 · 94 원소 (Table 1)**, 지면에 값이 나온 원소 73 (`Fig. 2`). 57 은 Anderson 의 59 중 Miara 값이 있는 수다.
  - 136행 *"(기존 보고 30 + Miara 예측에서 새로 29)"* — [Anderson24] digest §20.1 확정은 **신규 30 + 기보고 29**.
  - 133행 *"원문은 litdb 에 없다"* · 127행 *"Miara 원문은 litdb 에 아직 없습니다"* — 이제 있다.

---

## 1. 한 줄 요약

PBE 로 **128 개 양이온종 × LLZO 의 Li·La·Zr 세 자리** 결함에너지를 계산해 (`Fig. 2`), **2 eV 문턱 아래 dopant(site) 조합 108 개 · 비등원자가·비-(V–Ni) 59 개**를 추렸다 (`Table 2`). Al³⁺ 은 Li 자리 (1.36 eV) 가 맞고, Zn²⁺(Li) 1.32 · Mg²⁺(Zr) 1.22 · Sc³⁺(Zr) 등 새 후보를 냈다.
후반부에서는 Li 개방 pseudo-binary 로 **LLZO·LLTO × LCO·LMO·LFP** 의 반응 구동력을 0–5 V 에서 쟀고 (`Fig. 4`), 3 V 에서 **LFP (−181) > LMO (−109) > LCO (−33 meV/atom)** — *"LCO 가 가장 무난, 계면 문제는 사이클보다 고온 소결의 화학 분해"* 로 결론 낸다.

⚠ 단 이 "LCO 가 가장 안정" 은 **혼합분만 세는 축** (eq 3) 의 결론이다. LLZO 자체가 **3.39 V (figure-read) 위에서 산화 분해**되므로 LCO 작동 전위에서의 총 구동력은 다르다 — [Rich16] 은 같은 쌍을 LCO 전위에서 **−0.23 eV/atom (거의 전부 LLZO 자체 분해분)** 으로 낸다 (§7c · §10-9).

---

## 2. 메타 / 동기 / 질문

| 항목 | 내용 |
|---|---|
| 동기 ① 벌크 | 입방 LLZO (Ia-3d) 가 전도도 최고. 정방정 (I4₁/acd) 은 Li 가 8a(사면체)·16f·32g(팔면체)에 질서 배열해 상온 σ ~10⁻⁶ S/cm. Li 빈자리를 만드는 초원자가 도핑 (Al³⁺·Ga³⁺ → Li 자리, Ta⁵⁺·Nb⁵⁺ → Zr 자리) 이나 Li 를 7 pfu 위로 채우는 것으로 질서를 깬다 (Bernstein: Li₇₋₂ₓAₓLa₃Zr₂O₁₂ (A = Al³⁺, Ga³⁺) 에서 x = 0.2 를 넘으면 입방 · Ta⁵⁺ 는 Li₇₋ₓLa₃Zr₂₋ₓTaₓO₁₂ 에서 x ≥ 0.4 — 조성식은 인쇄 그대로) |
| 문헌 갭 ① | 기시도 도펀트 14 종 (Ta⁵⁺ Nb⁵⁺ Al³⁺ Ga³⁺ In³⁺ Sn⁴⁺ Sb⁵⁺ Y³⁺ Ge⁴⁺ Si⁴⁺ Ca²⁺ Sr²⁺ Ba²⁺ Hf⁴⁺, p. 4040) — **어느 자리에 들어가는지는 Al·Ga 말고는 미확정** |
| 동기 ② 계면 | 벌크가 좋아도 계면 저항이 크면 못 쓴다. LLZO\|LCO 에서 La·Zr·Co 상호확산으로 저항이 큰 보고 (ref 34·57) vs 저항 없음 보고 (ref 58·59) 가 엇갈린다 — **소결 때문인지 사이클 중 분해 때문인지 불명** |
| 던지는 질문 | (1) 가능한 모든 양이온의 **자리 선호와 결함에너지** (2) 가넷 전해질과 흔한 양극 셋의 **전압별 계면 분해 구동력** |
| 대상 | 도펀트: LLZO 만 · 계면: LLZO + LLTO (Li₅La₃Ta₂O₁₂) × LCO · LMO (LiMnO₂) · LFP |
| 연구 유형 | 순수 0 K DFT 열역학 · 실험 0 · 동역학 0 |

---

## 3. 핵심 수치 총정리 ★

### 3a. Al³⁺ 세 자리 — 방법 시연 (p. 4042 · `Fig. 1`)

| 자리 | 전하 보상 반응 (8 f.u. 셀) | 분해 산물 (인쇄) | E_defect |
|---|---|---|---|
| **Al³⁺(Li)** | Li₅₆La₂₄Zr₁₆O₉₆ + Al − 3Li → Li₅₃AlLa₂₄Zr₁₆O₉₆ | Li₅AlO₄ + 8 Li₆Zr₂O₇ + 12 La₂O₃ | **1.36 eV** |
| Al³⁺(La) | + Al − La → Li₅₆La₂₃AlZr₁₆O₉₆ | 0.6 Li₈ZrO₆ + Li₅AlO₄ + 7.7 Li₆Zr₂O₇ + 11.5 La₂O₃ | **3.16 eV** |
| Al³⁺(Zr) | + Al + Li − Zr → Li₅₇La₂₄Zr₁₅AlO₉₆ | 1.4 Li₈ZrO₆ + Li₅AlO₄ + 6.8 Li₆Zr₂O₇ + 12 La₂O₃ | **1.87 eV** |

- 순위 **Li < Zr ≪ La** = MAS NMR (Al 이 Li 자리) · Rettenwander 2014 DFT (Li 24d > Li 96h > Zr 16a ≫ La 24c) 와 일치.
- 세 분해 반응식 모두 **원소 수지가 맞는다** (우리 검산). 그리고 **셋 다 산물에 LLZO 자신이 없다** (§10-4).

### 3b. 2 eV 문턱과 집계 (p. 4042–4043 · `Table 2`)

| 자리 | total | subvalent | isovalent | supervalent |
|---|---|---|---|---|
| Li(1+) | 15 (10) | 0 | 0 | 15 (10) |
| La(3+) | 27 (25) | 7 (7) | 18 (18) | 2 (2) |
| Zr(4+) | 66 (57) | 36 (30) | 19 (17) | 11 (10) |

괄호 = V·Cr·Mn·Fe·Co·Ni 제외 (각주는 "3d transition-metal dopants" 라고 쓰지만 본문은 이 여섯만 뺀다 — Sc·Ti·Cu·Zn 은 남는다). 합계 108 (92) · 등원자가 37 · 최종 59.

### 3c. `Fig. 2` 인쇄값 — 원소별 최저 자리·선호 산화수·E_defect (eV) ★

**Li 자리 (초록, 8)**: H¹⁺ 2.660 · Be²⁺ 1.020 · B³⁺ 2.210 · Al³⁺ 1.360 · Fe³⁺ 1.324 · Zn²⁺ 1.320 · Ga³⁺ 1.160 · Br³⁺ 3.080

**La 자리 (빨강, 22)**: Na¹⁺ 2.340 · K¹⁺ 2.360 · Rb¹⁺ 1.290 · Cs¹⁺ 3.100 · Ag¹⁺ 2.750 · Ca²⁺ 1.030 · Sr²⁺ 0.700 · Ba²⁺ 1.260 · Y³⁺ 0.490 · Bi³⁺ 0.700 · Pr³⁺ 0.220 · **Nd³⁺ 0.140** · Pm³⁺ 0.260 · Sm³⁺ 0.220 · Gd³⁺ 0.350 · Tb³⁺ 0.440 · Dy³⁺ 0.500 · Ho³⁺ 0.560 · Er³⁺ 0.660 · Tm³⁺ 0.740 · Lu³⁺ 0.930 · Ac³⁺ 0.010

**Zr 자리 (파랑, 42)**: C⁴⁺ 2.710 · Si⁴⁺ 2.350 · P³⁺ 3.550 · S⁴⁺ 2.640 · Cl⁵⁺ 2.750 · Mg²⁺ 1.220 · Sc³⁺ 0.760 · Ti⁴⁺ 0.430 · V⁵⁺ 2.000 · Cr³⁺ 1.050 · Mn⁴⁺ 0.530 · Co⁴⁺ 0.900 · Ni²⁺ 1.270 · Cu²⁺ 1.740 · Ge⁴⁺ 1.110 · As⁵⁺ 2.160 · Se⁴⁺ 1.240 · Nb⁵⁺ 0.920 · Mo⁴⁺ 0.130 · **Tc⁴⁺ −0.610** · Ru⁴⁺ 0.310 · Rh³⁺ 0.990 · Pd⁴⁺ 0.220 · Cd²⁺ 1.090 · In³⁺ 0.790 · Sn⁴⁺ 0.310 · Sb⁵⁺ 0.980 · Te⁴⁺ 1.440 · I⁵⁺ 0.980 · Hf⁴⁺ 0.110 · Ta⁵⁺ 0.940 · W⁴⁺ 1.270 · Ir⁴⁺ 0.390 · Pt⁴⁺ 0.270 · Au³⁺ 2.390 · Hg²⁺ 1.940 · Tl³⁺ 1.110 · Pb⁴⁺ 0.360 · Ce⁴⁺ 0.230 · Eu²⁺ 1.530 · Th⁴⁺ 1.050 · Pa⁵⁺ 0.860

**색 없음 (자리 판정 불가, 1)**: N³⁺ 3.950 (고에너지라 흰색) · **판독 불가 (2)**: Np "17.30" · Pu "13.38" (§10-5) · **빈칸 (16 + 호스트 3)**: Re Os Po At Fr Ra Lr Yb Am Cm Bk Cf Es Fm Md No · Li La Zr

- 합계 73 = 8 + 22 + 42 + 1. 선호 자리 값 < 2 eV 는 **57 원소**.
- 본문 단언 *"3d 전이금속 중 최저 자리가 Li 인 것은 Fe³⁺ 뿐"* (p. 4042) — `Fig. 2` 에서 Zn²⁺ 도 Li 자리인데, 저자는 Zn (d¹⁰) 을 전이금속으로 세지 않는다 (*"low-energy dopants that are not 3d transition metals … Zn²⁺(Li)"*, p. 4043). 정의를 알고 읽으면 일관된다.

### 3d. 본문이 이름을 댄 도펀트 (p. 4042–4045)

| 도펀트(자리) | E_defect | 본문 맥락 |
|---|---|---|
| Ce⁴⁺(La) | 1.60 | 합성된 것 중 최고 → 문턱 앵커 (Ce 의 선호 자리는 Zr 0.230) |
| Te⁶⁺(Zr) | 2.0 | 문턱으로 채택 (LLZO 에 Te 시도 없음) |
| **Zn²⁺(Li)** | **1.32** | *"Perhaps the most interesting"* — Al³⁺(Li) 1.36 보다 약간 낮음 · LISICON 등 SE 흔한 성분 |
| Mg²⁺(Li) · Sb⁵⁺(Zr) · W⁶⁺(Zr) · Mo⁶⁺(Zr) | < 2 (값 미인쇄) | 기타 초원자가 후보 |
| Rb¹⁺(La) | 1.29 | 저자 선행연구 — 입방상 안정 · 고전도 (Li > 7 pfu 경로) |
| **Mg²⁺(Zr)** | **1.22** | 미시도 아원자가 후보 (Sc³⁺(Zr) · Ca²⁺(Zr) · Ca²⁺(La) 와 함께) |
| Sn⁴⁺(Zr) | 0.31 | Li₇La₃Sn₂O₁₂ 가넷이 실재 → 완전 고용 예상 |
| 아원자가 군 (Li > 7 pfu 로) | 상대적으로 낮음 | Sc³⁺(Zr) · Ca²⁺(Zr) · Bi³⁺(Zr) · Mg²⁺(Zr) · Ca²⁺(La) · Sr²⁺(La) · Ba²⁺(La) — *"LLTO 에는 쓰였으나 LLZO 에는 아님"* |
| Zr 자리 아원자가 · 비-3d | 30 조합 < 2 eV | `Table 2` 36 (30) |
| Co³⁺(Zr) | (`Table S3`) | La₂O₃ + Li₆Zr₂O₇ + Li₈CoO₆ 로 분해 → LLZO\|LCO 공소결 상호확산 근거 |

- **제안 전략 (p. 4043)**: *"combine two dopants to achieve ∼6.5 Li pfu"* (공도핑 — 계산은 안 함) 또는 Li > 7 pfu 가넷 재탐색.

### 3e. 계면 — `Table 3` (3 V, Li 개방) 원문 + 우리 역산

| 전해질 (x) | 양극 (1 − x) | Δφ (meV/atom) | 산물 (인쇄) | 함의된 x (우리 역산, Li 제외 원자 기준) |
|---|---|---|---|---|
| 2.00 LLZO | 7.02 LCO | **−33.37** | La₂O₃ + 2.000 La₂Zr₂O₇ + 7.000 Li₂CoO₃ | **0.6175** (본문 0.618 ✓) |
| 2.01 LLZO | 7.05 LMO | **−108.9** | La₂O₃ + 2.008 La₂Zr₂O₇ + 7.033 Li₂MnO₃ | 0.618 |
| 1.48 LLZO | 3.47 LFP | **−181.17** | 3.457 Li₃PO₄ + Fe₂O₃ + 1.481 La₂Zr₂O₇ + 1.469 LaFeO₃ | 0.547 |
| 1.00 LLTO | 1.0 LCO | **−10.54** | Li₃TaO₄ + Li₂CoO₃ + La₃TaO₇ | 0.85 |
| 2.01 LLTO | 5.07 LMO | **−56.45** | La₃TaO₇ + 5.039 Li₂MnO₃ + 3.026 LaTaO₄ | 0.692 |
| 1.00 LLTO | 2.67 LFP | **−124.41** | LaPO₄ + 1.666 Li₃PO₄ + 1.334 Fe₂O₃ + 1.998 **[이름 누락]** | 0.515 |

- **마지막 행의 빠진 산물 = LaTaO₄** (우리 질량수지: 남는 La₂Ta₂O₈ = 2 LaTaO₄ → 계수 1.998 ✓). 인쇄 오류 (§10-7).
- **x 의 정의**: x 를 Li 를 뺀 원자 수 비로 읽어야 본문의 0.618 이 나온다 (2.00 × 17 / (2.00 × 17 + 7.02 × 3) = 0.6175). 전체 원자 비면 0.631, 화학식 비면 0.222. ⇒ pymatgen `GrandPotentialInterfacialReactivity` 와 **같은 정규화** (§7c). 에너지의 "per atom" 기준은 본문이 안 밝힌다 (같은 정규화면 Li 제외 원자당일 것 — 미확인).
- `Table 3` 캡션의 **"Maximum"** 은 3 V 에서 **x 에 대한 최대**다. 전압에 대한 최대가 아니다 — 전압 극소는 3.2–3.4 V 에 있고 더 깊다 (3f).

### 3f. 계면 — `Fig. 4` 픽셀 판독 (figure-read ≈, 판독법 §16)

| 쌍 | 3.0 V | `Table 3` | 극소 (eV/atom @ V) | 4.5 V 평탄 |
|---|---|---|---|---|
| LLZO\|LCO (굵은 파랑) | −0.034 | −0.0334 | **−0.054 @ 3.24** | −0.015 |
| LLZO\|LMO (굵은 빨강) | −0.109 | −0.1089 | **−0.116 @ 3.17** | −0.029 |
| LLZO\|LFP (굵은 초록) | −0.181 | −0.1812 | **−0.193 @ 3.21** | −0.111 |
| LLTO\|LCO (가는 파랑) | −0.011 | −0.0105 | **−0.026 @ 3.44** | −0.003 |
| LLTO\|LMO (가는 빨강) | −0.057 | −0.0565 | **−0.068 @ 3.27** | (겹침, 판독 안 함) |
| LLTO\|LFP (가는 초록) | −0.125 | −0.1244 | **−0.146 @ 3.29** | −0.075 |

- **3 V 판독 6 개가 `Table 3` 과 모두 1 meV/atom 안에서 일치** → `Table 3` = `Fig. 4` 의 3 V 단면, 판독 보정 검증됨.
- **안정창 막대 (점 중심)**: LLZO **0.47–3.39** · LLTO **0.92–3.54** · LCO **1.93→** · LMO **1.47→** · LFP **2.26→** V (화살표 = 5 V 너머). [Xiao20Rev] `Fig. 4d` 의 재수록 좌표 (0.43–3.41 · 0.88–3.57 · 1.89 · 1.44 · 2.21) 와 **≤ 0.05 V** 로 일치 — 그 그림이 이 그림의 재수록임을 원본으로 확인.
- 저전압: 0.1 V 에서 굵은 곡선 (LLZO) 도 0 이 아니다 (figure-read ≈ LCO −0.046 · LMO −0.019 · LFP −0.035) — 본문 *"The reaction energy is zero against LLZO"* 는 LLZO 창 (≥ 0.47 V) 안에서만 맞다 (§10-10).

### 3g. `Fig. 3` 꺾임점 (LLZO|LCO, 3 V · figure-read ≈)

| x (LLZO) | Δφ (eV/atom) | 산물 (그림 라벨) |
|---|---|---|
| **0.618 ★** | **−0.0334** | **La₂O₃ + La₂Zr₂O₇ + Li₂CoO₃** (최대 구동력) |
| 0.692 | −0.0297 | La₂O₃ + LiLaZrO₄ + Li₂CoO₃ |
| 0.789 | −0.0220 | La₂O₃ + Li₂ZrO₃ + Li₂CoO₃ |
| 0.918 | −0.0116 | La₂O₃ + Li₆Zr₂O₇ + Li₂CoO₃ |

LLZO 쪽에서 별 쪽으로 갈수록 Zr 상이 **Li₆Zr₂O₇ → Li₂ZrO₃ → LiLaZrO₄ → La₂Zr₂O₇** 로 Li 가 빠진다 — 가넷의 Li·O 가 양극 쪽 Li₂CoO₃ 로 넘어가는 그림이다. 끝점 (x = 0, 1) 은 정의상 0.

---

## 4. 계산 방법 ★ (§0S-3 표가 전부 — 여기는 템플릿 칸 대응)

- **code / version**: VASP (버전 n/a)
- **functional + vdW**: PBE-GGA · vdW 없음 (언급 0) · ⚠ ref 41 은 PBE0 논문 (§10-6)
- **pseudo / PAW**: PAW (데이터셋 n/a)
- **k-points / ecut / supercell / nat**: k 밀도 ≥ 1000/nat · **500 eV** · 8 f.u. conventional · **192 원자**
- **DFT+U**: **n/a** (언급 0)
- **AIMD / MLIP**: 없음
- **무질서 처리**: **정전기 (Ewald) 선별 100 배열 → DFT 최저 1 배열** · 도핑과 전하보상 자리도 정전기 순위로 1 개만 · 앙상블·SQS 없음 · 엔트로피 무시
- **특이사항**: 결함에너지의 μ 를 **도핑 조성이 속한 hull 면**에서 잰다 — "원소 기준 형성에너지" 가 아니라 **"경쟁상 대비 초과 에너지"** 에 가깝다. 상평형도에 data-mined **가상 화합물**이 들어간다 (예 Li₂CoO₃ — *"a predicted material … stable according to DFT"*).

---

## 5. 결과 — 절별 상세 (그림 실독 포함)

### 5.1 Al³⁺ 시연과 4원 단면 (`Fig. 1`, p. 4042)

`Fig. 1` 은 Li–La–Al–Zr–O 5원계의 **4원 단면** (꼭짓점 Li₂O · La₂O₃ · ZrO₂ · Li₅AlO₄) 이다. 번호 점 7 개: 1 Li₈ZrO₆ · 2 Li₆Zr₂O₇ · 3 Li₇La₃Zr₂O₁₂ · **4 Li₅₃AlLa₂₄Zr₁₆O₉₆ (초록 원 = Al(Li) 도핑 셀)** · 5 Li₂ZrO₃ · 6 LiLaZrO₄ · 7 La₂Zr₂O₇.
분홍 삼각형 = **La₂O₃ – Li₅AlO₄ – Li₆Zr₂O₇** = 4 번이 떨어지는 분해 면 (캡션 *"highlighted in green in the decomposition triangle"*, 1.36 eV).
- 실제로 보니: 점 색이 **파랑** (La₂O₃ · Li₅AlO₄ · 1 · 2) 과 **빨강** (Li₂O · ZrO₂ · 3 · 5 · 6 · 7) 으로 갈리는데 **캡션에 뜻이 없다**. 빨강 5·6 에도 tie line 이 모이므로 '빨강 = 불안정' 은 아니다 — 색으로 hull 안정성을 읽지 않는다.
- 우리가 가져갈 것: **"결함에너지 = 그 조성이 속한 면의 경쟁상 대비"** 를 한 장으로 보여 주는 문법.

### 5.2 주기율표 히트맵 (`Fig. 2`, p. 4043)

색 = 최저 에너지 자리 (초록 Li · 빨강 La · 파랑 Zr), **진할수록 낮은 에너지**, 칸 안에 선호 산화수와 E_defect (eV). 전사는 §3c.
- **자리 패턴**: 큰 저원자가 (알칼리·알칼리토·란타넘족 3+) → La 자리 · 작은 고원자가 (4d·5d 전이금속·p 블록 4+/5+) → Zr 자리 · 작은 2+/3+ 일부 (Be · Al · Ga · Zn · Fe) → Li 자리.
- **극단값**: Tc⁴⁺(Zr) **−0.610** (유일한 음수 = 도핑이 순수 LLZO + 경쟁상보다 낮다는 뜻) · Ac³⁺(La) 0.010 · Hf⁴⁺(Zr) 0.110 · Mo⁴⁺(Zr) 0.130 · Nd³⁺(La) 0.140 / 최고 N³⁺ 3.950 · P³⁺ 3.550 · Cs¹⁺ 3.100 · Br³⁺ 3.080.
- 실제로 보니: **Np·Pu 칸은 산화수 없이 이름 자리에 17.30 · 13.38** 이 찍히고 색은 짙은 파랑 (= 범례상 '낮은 에너지') 이다 — 범례와 모순 (§10-5). **Lu 는 란타넘족 줄 끝**에 놓였다 (`Table 1` 은 Lu 를 6주기 3족 본체에 둔다).

### 5.3 문턱과 집계 (p. 4042–4043, `Table 2`)

- 용해도는 *"결함에너지 vs Li 무질서 엔트로피 이득"* 의 경쟁인데 엔트로피를 못 구하므로, **합성 성공 사례의 최대 결함에너지**를 '합성 가능' 의 대리로 쓴다 — Ce⁴⁺(La) 1.60 → 넓혀서 2 eV.
- **등원자가 37 개를 따로 표시**: 녹기는 잘 녹겠지만 Li 함량을 안 바꿔 입방상 안정화에 못 쓴다. 3d 원소는 Li 음극에 환원될 수 있어 V–Ni 6 원소를 뺀다 (Fe³⁺ 이 실험상 입방상 안정화에 효과적이라는 점은 인정).
- ⇒ **59 dopant(site) 조합** (`Table 2` 괄호의 비등원자가 합).

### 5.4 새 후보 (p. 4043, 4045)

- 6–7 Li pfu 에서 전도도가 최고 → 초원자가가 필요. 흔한 넷 (Al³⁺(Li) · Ga³⁺(Li) · Ta⁵⁺(Zr) · Nb⁵⁺(Zr)) 밖에서 **Zn²⁺(Li) 1.32** 를 *"most interesting"* 으로, Mg²⁺(Li) · Sb⁵⁺(Zr) · W⁶⁺(Zr) · Mo⁶⁺(Zr) 를 덧붙인다.
- Li > 7 pfu 경로: Zr 자리 아원자가 비-3d **30 조합** · *"not tried before"* Mg²⁺(Zr) 1.22 · Sc³⁺(Zr) · Ca²⁺(Zr) · Ca²⁺(La).
- 결론 절 (p. 4045): *"Several novel dopants emerge such as subvalent Sc³⁺ and Mg²⁺ on the Zr-site."* 초록: *"Zn²⁺ and Mg²⁺ predicted to be stable on the Li- and Zr-sites, respectively."*

### 5.5 계면 방법 (§3.1, p. 4043–4044)

1. 계면은 벌크 상평형 열역학이 지배한다고 보고, **두 조성을 섞은 상평형도**를 본다 (계면에너지 무시).
2. Li 는 전극에서 들어오고 나가므로 **Li 개방**: `φ_hull(c, μ_Li) = min_{n_Li} [E_hull(c + n_Li) + n_Li μ_Li]` (eq 2).
3. `Δφ(μ_Li) = min_{x∈[0,1]} [φ_hull(x c_e + (1−x) c_c, μ_Li) − x φ_hull(c_e, μ_Li) − (1−x) φ_hull(c_c, μ_Li)]` (eq 3) — **반응물을 각자의 grand-potential hull 값으로 뺀다 → 혼합분만**.
4. 0–5 V vs Li (−5 < μ_Li < 0 eV) 에서 반복. 각 상의 **고유 안정창** = 그 상이 grand-potential 상평형에서 안정한 μ_Li 범위 (LGPS 선례 ref 53 과 같은 절차).

### 5.6 LLZO|LCO 시연 (`Fig. 3`, p. 4044)

3 V 에서 5원계 (Li–La–Zr–Co–O) grand potential 상평형 (`Figure S1`, 미보유) 위 tie line 을 그린 pseudo-binary. 꺾임점 표 §3g. 최대 구동력 **x = 0.618, −33.37 meV/atom → La₂O₃ + La₂Zr₂O₇ + Li₂CoO₃**.
- 실제로 보니: 왼쪽 (LCO 쪽) 은 x = 0 에서 별까지 **꺾임 없는 직선**, 오른쪽에 네모 3 개. 축 0.00 ~ −0.04 eV/atom.
- Li₂CoO₃ 는 **가상 화합물** (Li₂MnO₃ 구조 유사, DFT 로 안정) — 산물 목록에 실험 미확인상이 들어 있다.

### 5.7 전압 스캔과 안정창 (`Fig. 4` · `Table 3`, p. 4044–4045)

- 3 V 순위 (LFP > LMO > LCO · LLZO > LLTO) 가 **전해질 창 안에서 대체로 유지**된다.
- LLZO 가 저전압에서 더 안정 (하한 0.47 vs 0.92 V figure-read) · 두 가넷 모두 **3.8 V 까지 분해**.
- 구동력 극소가 **창 가장자리** (위 끝 근처 3.2–3.4 V) — 그 위 (3.8 V 이상) 는 전해질 분해 산물이 고정돼 **평탄**.
- 저전압 (양극 분해 영역) 에서는 양극 분해 산물 (금속 + Li₂O) 이 전해질과 공존. < 2 V 에서 LLTO 는 Li₂O + **TaCo₃ · TaMn₂** 합금 (`Table S1`).
- 실제로 보니: 0–0.4 V 에서 **모든 곡선이 −0.02 ~ −0.06 eV/atom** 로 0 이 아니다 (3f). 범례는 캡션에만 있고 그림 안에는 없다 (색·굵기 매핑은 캡션 [Legend] 문장).

### 5.8 토론 — 실험 엇갈림의 해소 (p. 4045)

- **LCO 추천 · LFP 비추천** (Fe 산화 · P → Li₃PO₄). LiMPO₄ (M = Ni · Cr · V) 도 같은 패턴 (값 미제시).
- Li₃PO₄ 가 보호층일 가능성 — 조건 *"iron oxides do not create percolating electronic pathways"*.
- LLZO\|LCO: 상온에서 La·Zr·Co 는 크고 고전하라 못 움직인다 → **고온 공소결**에서만 열역학대로 분해 (Co³⁺(Zr) LLZO 분해 = Kim et al. 관측) · **저온 PLD** 는 안정 사이클 (준안정 계면, 또는 분해층이 장벽).
- 소결 중 O·Li 손실은 *"beyond the scope"*.

---

## 6. 논증 종합

1. **도펀트**: 결함에너지 (경쟁상 대비) → 자리 선호 → 문턱 (합성 사례 앵커) → 등원자가 제외 (Li 함량 불변) → 3d 제외 (환원 위험) → 59 조합. **"녹는가"** 만 판정하고 **"입방상이 얼마나 되는가"·"전도도가 얼마인가"** 는 계산하지 않는다 (엔트로피·동역학 없음).
2. **계면**: 혼합 구동력만 세면 LCO 가 가장 무난 → 실험의 저항 문제는 **사이클이 아니라 소결 (고온 화학 분해)** 탓이라는 해석.
3. 두 절을 잇는 고리 = **Co³⁺(Zr) 결함 계산** (§2 방법) 이 LLZO\|LCO 소결 분해 (§3 질문) 의 근거로 재사용된다.

---

## 7. 우리 DFT 와의 대조 ★★ (`../our_dft_baseline.md` · `kb/methodology/doping_substitution_algorithm.md` · `tools/oxidation/interface_reactivity_v2.py`)

### 7a. 항목별

| 항목 | Miara 2015 | 우리 | 같다 / 다르다 · 이유 |
|---|---|---|---|
| 계 | 산화물 가넷 LLZO (+ LLTO) | 황화물 argyrodite (comp1 · modelc · LPSOCl) | **다르다** — 숫자 이식 금지 |
| 코드 · 범함수 | VASP · PBE · PAW · 500 eV | QE (pw.x) · PBE (`our_dft_baseline.md`) | 범함수 계열 같음 · 코드·의사퍼텐셜 다름 |
| 도펀트 에너지 | PBE 결함에너지, hull 면 μ 기준, 128 종 × 3 자리 | cascade UMA 스크리닝 · `screen_de_per_atom` **절대값 인용 금지** (2026-08-19 판정, `kb/methodology/cascade_design_contract_2026_08_28.md` §2) | **우리에게 이 양과 같은 검증된 DFT 결함에너지가 없다** — 이 논문을 "우리도 같은 양을 쟀다" 로 인용하면 틀린다 |
| 도핑 단위 | **이온종 하나** (원소 × 산화수) · 음이온 자리 0 | **전구체 화합물 하나** (양이온·음이온을 화학식 비로) | **진짜 차이** (세미나 novelty 의 근거와 같은 방향) |
| 전하 보상 | Li 빈자리 / 침입 (정전기 순위로 자리 선택) | Li 빈자리 / 침입 · 형식전하 총수지 0 이 아니면 생성 거부 (`db/properties/cascade_s1_contract_amendment_2026_09_12.json` ②) | **같다** — 대비점 아님 |
| 무질서 | Ewald 100 → DFT 최저 1 배열, 도핑은 그 위 단일 배치 | 도펀트별 배치 앙상블 (`kb/methodology/dopant_screening_funnel_2026_06_13.md`) | 방법 차이 — 단일 배열이면 자리 순위가 배열 의존일 수 있다 |
| 문턱 | **2 eV — 합성 성공 사례의 최대값 (1.60) 에 앵커 후 확장** | cascade 게이트 (보고량 카드 기준) | **빌릴 만한 방법** — 문턱을 실험 앵커로 정하고 그 근거를 한 문장으로 남긴다 |
| 안정창 | Li 개방 grand potential · LLZO 0.47–3.39 V (figure-read) | 같은 구성 · comp1 1.717–2.256 V (`esw_lis4excluded.json` · 하한 라벨 규약 `HZ-esw-reduction-limit-label`) | **구성 같음 · 계 다름** — 숫자 비교 금지. 우리 산화 onset 은 S-제한 (축 ①) |
| 계면 반응 | **혼합분만** (eq 3, 끝점 0) | v2 열린계 = `include_no_mixing_energy=True` (**SE 자체 분해분 포함**, 끝점 ≠ 0) | 🔴 **같은 이름, 다른 양** (7c) |
| 기계 | 없음 | 탄성 (EOS · 탄성상수) 계산 있음 | 우리 쪽만 있음 — 단 세미나 메모대로 *기계 축 자체는 새로움이 아니다* ([Jung26LGPS] 가 ML G·G/K 로 거름) |

### 7b. Nd 를 볼 때 (CEI 트랙 — 1저자는 실험 쪽)

`Fig. 2` 인쇄값 **Nd³⁺(La) 0.140 eV** (등원자가 · 란타넘족 중 최저 근처). **가넷 La 자리 값이다** — 우리 argyrodite·NdP₅O₁₄ 계면 판단에 **이식하지 않는다**. 인용한다면 *"in garnet LLZO, Nd³⁺ is predicted to prefer the La site (Miara 2015)"* 수준까지만.

### 7c. 🔴 "같은 이름, 다른 양" — Δφ(eq 3) vs 우리 `interface_reactivity_v2.py` (2026-10-13 pymatgen 원본 대조)

pymatgen `GrandPotentialInterfacialReactivity.__init__` (master 소스, `src/pymatgen/analysis/interface_reactions.py`):
- `include_no_mixing_energy=False` → `self.e1 = self.pd.get_hull_energy(self.comp1)` — 반응물을 **grand-potential hull 값**으로 → 끝점 0 → **Miara eq 3 과 같은 양** (혼합분만).
- `include_no_mixing_energy=True` → `self.e1 = self._get_grand_potential(self.c1)` — 반응물을 **Li 를 고정한 원래 조성의 grand potential** 로 → 반응물 자체의 Li 교환·분해 에너지 (no-mixing) 가 반응에너지에 들어간다.
- 정규화: 두 경우 모두 **저장고 원소 (Li) 를 뺀 원자 수**로 나눈다 → Miara `Table 3` 계수로 역산한 x (0.6175) 와 같은 규약.
- ⇒ 우리 v2 (`include_no_mixing_energy=True`) 의 열린계 값은 **Miara Δφ 가 아니다**. 우리 v2 docstring 이 2026-09-16 에 잡은 *"끝점 값이 0 이 아니다 — 순수상의 grand-potential 자체 분해 에너지"* 가 바로 이 차이다.
- **같은 그룹 두 편의 LLZO\|LCO 가 엇갈리는 이유도 이것이다**: Miara (혼합분, 3 V) **−0.033** eV/atom → *"LCO 가 가장 무난"* · [Rich16] (no-mixing 포함, LCO 전위) **−0.23 / −0.23** (no-mixing / 전체 — 거의 전부 LLZO 자체 분해분) → LLZO 에 LCO 가 가장 나쁜 축. **모순이 아니라 축이 다르다.** "LCO 와 안정하다" 류 문장은 **어느 축인지 이름을 댄다** (우리 'Cl-rich 산화안정성' 규율과 같은 원리).
- ⚠ 우리 v2 docstring 은 방법 출처를 *"Richards/Ong 2016"* 으로 적는데 [Rich16] 저자에 Ong 은 없다 — 라벨 오기 (도구는 안 고쳤다, `comparison_vs_ours.md` §I 에 기록).

---

## 8. Post-processing ★

- **무엇**: (i) 정전기 (Ewald) 에너지 순위 — Li 배열 100 개 선별 · 전하보상 자리 선택 (ii) **convex hull + 면 화학퍼텐셜** (pymatgen) — 결함에너지의 μ (iii) **grand potential 상평형도** (Li 개방) — 고유 안정창 (iv) **pseudo-binary tie line 최소화** (eq 3) — 계면 반응에너지·산물 (v) 0–5 V 스캔.
- **도구**: VASP · pymatgen (ref 37) · ICSD · data-mined 치환 (ref 39). LOBSTER · Bader · DOS · NEB **없음**.
- **수치화·기록**: 결함에너지는 eV / 8 f.u. 셀 (= 도펀트 1 개당) 로 **주기율표 히트맵** (`Fig. 2`) + 조합 수 표 (`Table 2`) + 목록·전 자리 값은 SI (`Table S2`·`S3`). 계면은 pseudo-binary 곡선 (`Fig. 3`) · Δφ(V) 곡선 + 안정창 막대 (`Fig. 4`) · 3 V 표 (`Table 3`) · 타 전압 표 (`Table S1`).
- **그림 양식**: `Fig. 2` 는 칸마다 (자리 색 · 산화수 · 값) 세 정보를 넣은 주기율표 — [Anderson24] `Fig. 1`·`Fig. 4` 도 같은 문법을 쓴다.

---

## 9. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | Li–La–Al–Zr–O 5원계의 4원 단면 (꼭짓점 Li₂O · La₂O₃ · ZrO₂ · Li₅AlO₄) + 번호 화합물 7 개 · Al(Li) 도핑 셀 (초록 4번) 이 떨어지는 분해 삼각형 La₂O₃–Li₅AlO₄–Li₆Zr₂O₇ (분홍) · 1.36 eV. 점 색 (파랑/빨강) 의 뜻은 캡션에 없다 | "결함에너지 = 그 조성이 속한 hull 면의 경쟁상 대비" 를 한 장으로 설명하는 문법 — 우리 치환에너지 기준 μ 설명 그림의 견본. 색을 hull 안정성으로 읽지 않는다 |
| 2 | 주기율표 히트맵: 원소별 최저 자리 (초록 Li · 빨강 La · 파랑 Zr) · 선호 산화수 · E_defect (eV) — 값 있는 원소 73 · 판독 불가 2 (Np 17.30 · Pu 13.38) · 빈칸 16 (Re Os Po At Fr Ra Lr Yb Am–No) | [Anderson24] `Fig. 3d` 의 원천 (최소값 57/57 일치, 차이 ≤ 0.12 eV). 세미나 '입력 수' 질문의 그림 근거. 우리 도펀트 풀을 (자리 · 산화수 · 에너지) 한 장으로 그릴 때의 양식 견본. Nd³⁺(La) 0.140 은 가넷 값 — 이식 금지 |
| 3 | LLZO–LCO pseudo-binary @ 3 V (Li 개방): x(LLZO) 0–1 vs Δφ · 꺾임점 4 개 · 최대 구동력 ★ x = 0.618, figure-read ≈ −0.0334 eV/atom → La₂O₃ + La₂Zr₂O₇ + Li₂CoO₃ | 우리 `interface_reactivity_v2` 의 kink 그림과 같은 문법. ⚠ x = Li 제외 원자 기준 · 에너지 = 혼합분만 (끝점 0) → 우리 v2 열린계 값 (no-mixing 포함) 과 다른 양 |
| 4 | Δφ(V) 0–5 V: 굵은 선 LLZO · 가는 선 LLTO × 파랑 LCO · 빨강 LMO · 초록 LFP + 아래 고유 안정창 막대 (figure-read LLZO 0.47–3.39 · LLTO 0.92–3.54 · LCO ≥ 1.93 · LMO ≥ 1.47 · LFP ≥ 2.26 V). 극소는 전부 3.17–3.44 V | 우리 ESW (grand potential) · 계면 반응성 전압 스캔과 같은 축 구성. 3 V 판독 6 개 = `Table 3` (≤ 1 meV/atom). [Xiao20Rev] `Fig. 4d` 막대의 원본. ⚠ 혼합분만이라 창 밖에서 평탄 — 우리 v2 곡선과 모양 비교 금지 |
| Table 1 | 계산한 도펀트 원소·산화수 (캡션 "128 total") — 인쇄된 칸은 원소 94 · 원소(산화수) 122 · 이미지 표 | 세미나 표 n 의 정본 (128). ⚠ 6+ 종이 하나도 없다 (본문은 Te⁶⁺ · W⁶⁺ · Mo⁶⁺ 를 쓴다) |
| Table 2 | E_defect < 2 eV 인 dopant(site) 조합 수: Li 15 (10) · La 27 (25) · Zr 66 (57) — 괄호 = V–Ni 제외 · 아/등/초원자가 분해 | 세미나 '45' 검증의 1차 근거 — 원문 집계는 전부 조합 단위 (108 · 92 · 59). 자동 크롭이 '영역 없음' 으로 빠뜨려 수동 크롭 (`figures.json` `manual_crop`) |
| Table 3 | 3 V 에서 6 쌍 (LLZO · LLTO × LCO · LMO · LFP) 의 최대 Δφ (meV/atom) 와 산물·계수 | 소환값 — 혼합분 · 3 V · Li 개방. LLTO–LFP 행 마지막 산물 이름 누락 (질량수지로 LaTaO₄) |

---

## 10. 비판 — 이 논문의 약한 곳 ★

1. **Eq. [1] 의 인쇄 부호가 보고값의 해석과 맞지 않는다.** `E_pure − E_doped + Σ Δn_i μ_i` 는 Δn_i 를 '넣은 원자 +' 로 읽으면 통상식 (`E_doped − E_pure − Σ Δn_i μ_i`) 의 정확히 −1 배이고, '뺀 원자 +' 로 읽으면 에너지 항과 μ 항의 부호가 서로 어긋나 열역학적으로 말이 안 되는 식이 된다. 그런데 본문은 **"낮을수록 유리"** (Al(Li) 1.36 이 최적 · 진할수록 낮은 에너지 · 2 eV 이하 통과) 로 쓴다 → **통상식으로 읽는다** (인쇄 부호는 오기로 본다).
2. **`Table 1` 의 인쇄 칸 122 ≠ 캡션 128.** 그리고 본문이 쓰는 **6+ 종 (Te⁶⁺(Zr) 2 eV 문턱 · W⁶⁺(Zr) · Mo⁶⁺(Zr) · "A = 6+ dopant on Li site")** 이 `Table 1` 에 **하나도 없다**. 빠진 6 이 6+ 종일 가능성 — S · Se · Te · Cr · Mo · W 의 6+ 라면 정확히 6 이다 (**우리 가설**, SI 없이 확인 불가).
3. **1152 구조의 셈이 본문 규칙과 안 맞는다** (128 × 9 vs 규칙대로 128 × 5 = 640).
4. **LLZO 자신이 그들의 0 K hull 꼭짓점이 아닌 것으로 보인다 (우리 추론).** Al 세 자리와 Co³⁺(Zr) 의 인쇄된 분해 산물 4 건이 **전부 LLZO 를 빼고** La₂O₃ · Li₆Zr₂O₇ · Li₈ZrO₆ 쪽으로 간다. 도핑 셀은 LLZO 8 f.u. 에서 192 원자 중 2–4 개만 다르므로 (도펀트 1 + 보상 Li), LLZO 가 hull 꼭짓점이면 그 조성이 속한 면에 LLZO 가 들어가야 한다 (순수 LLZO = 1.5 La₂O₃ + 0.2 Li₈ZrO₆ + 0.9 Li₆Zr₂O₇ 로 같은 면에 들어간다 — 우리 질량수지). 본문은 **LLZO 의 E_hull 도, 안정창 계산에서 그것을 어떻게 다뤘는지도 밝히지 않는다** ([Zhu15] 는 준안정 SE 를 hull 로 내렸다고 명시). Eq. [1] 의 순수 셀 항이 그 몫을 상쇄하므로 결함에너지 순위에는 큰 영향이 없겠지만, **Tc⁴⁺ 의 −0.61 eV** 같은 음수가 나오는 배경일 수 있다.
5. **`Fig. 2` 의 Np·Pu 칸** — 산화수 없이 이름 자리에 17.30 · 13.38, 색은 짙은 파랑 (범례상 '낮은 에너지'). 판독 불가 칸으로 둔다. 그리고 `Table 1` 에 있는 **16 원소 (Re · Os · Yb · Fr · Ra · Po · At · Lr · Am–No)** 는 지면에 결과가 없다 — 실패인지 생략인지 설명 없음.
6. **ref 41 오인용** — 본문은 "PBE GGA" 라고 쓰는데 ref 41 은 PBE0 하이브리드의 근거 논문 (*J. Chem. Phys.* 105, 9982, 저자명도 'Emzerhof' 오기). 또 Rb¹⁺(La) 결과를 *"we have previously shown … ³"* 로 ref 3 (Xu 2012 PRB) 에 다는데 저자 자신의 Rb 논문은 ref 13 이다.
7. **`Table 3` LLTO\|LFP 행의 마지막 산물 이름 누락** (`+ 1.998` 로 끝남 — 질량수지로 LaTaO₄).
8. **DFT+U · 스핀 언급 0.** Fe · Co · Mn 도펀트와 LCO · LMO · LFP 양극을 계산하면서 U 를 안 밝힌다. 계면 반응에너지는 전이금속 산화환원이 핵심이라 이 공백이 크다.
9. **"LCO 가 가장 안정" 은 혼합분 축의 결론이다** (§7c). LLZO 창 위 끝 (3.39 V figure-read) 이 LCO 작동 전위보다 낮아서, 그 전위에서는 LLZO 자체 산화가 지배한다 — [Rich16] 이 같은 쌍을 −0.23 eV/atom 으로 낸 이유. 저자도 *"both garnets are decomposed by 3.8 V"* 라고는 적지만 결론 문장에 축을 달지 않는다.
10. **저전압 서술과 그림의 작은 불일치** — *"The reaction energy is zero against LLZO"* 인데 `Fig. 4` 에서 0.4 V 아래 LLZO 곡선은 −0.02 ~ −0.05 eV/atom (figure-read). LLZO 창 안에서만 맞는 문장이다.
11. **원자가 라벨 오기** — 토론 (p. 4045) *"promising **subvalent** dopants … such as Zn²⁺(Li), and Mg²⁺(Li)"* — Li⁺ 자리의 2+ 는 **초원자가**다.
12. **'3d 제외' 가 두 정의로 쓰인다** — `Table 2` 각주 "3d transition-metal dopants" vs 본문 "V, Cr, Mn, Fe, Co, Ni". 비등원자가 중 "25 개가 3d 포함" 인데 실제로 빠진 것은 71 − 59 = 12 개 (Sc · Ti · Cu · Zn 은 남김). 모순은 아니지만 숫자를 옮길 때 헷갈린다.
13. **엔트로피·온도·농도 없음** — 한 농도 (0.125 pfu) · 한 배열 · 0 K. "합성 가능" 판정은 문턱 하나에 기대고, 그 문턱은 합성 사례 앵커 (1.60) 에서 '넓혀' 정한 판단값이다. **결함에너지 크기가 입방상 비율을 예측하지 못한다**는 것은 [Anderson24] 가 실험으로 보였다 (ρ ≈ 0, Anderson digest §19.4).
14. **"소결이 문제" 결론은 계산된 것이 아니다** — 온도 효과를 안 계산했다. 0 K 구동력이 작다는 것 + "상온에선 이온이 안 움직인다" 는 동역학 논증의 조합이다.
15. **SI 미보유** — `Table S1` (타 전압 산물) · `Table S2` (2 eV 통과 목록 — '45' 의 유일한 후보 출처) · `Table S3` (전 자리 값 · Co³⁺(Zr) 분해) · `Figure S1` 의 주장은 검증하지 못했다.

---

## 11. [Anderson24] `Fig. 3d` 대조 — 상세 (§0S-6 의 근거)

**무엇을 했나**: [Anderson24] `Fig. 3` 크롭 (2118 × 1573) 의 패널 d 를 자리별로 다시 읽어 (판독법 §16) Miara `Fig. 2 인쇄값` 과 맞댔다.

- **x 라벨 순서** (패널 d, La 블록): Na K Ca Rb Sr Y Ag Cs Ba Pr Nd Sm Gd Tb Dy Ho Er Tm **n/a** Lu Bi — 패널 a·b 의 같은 자리는 **Yb**. Zr 블록에는 패널 a·b 의 `*Re` 가 없다. ⇒ 값이 있는 도펀트 = 59 − Yb − Re = **57**.
- **최소값 대조 (57 종)**: \|Δ\| 중앙 **0.03 eV** · 최대 **0.12 eV** (B −0.12 · Er −0.10 · Ho −0.09 · Zn −0.06 · Mo +0.06 — 전부 마커가 겹친 칸) · 평균 Δ −0.027 (판독 보정 1–2 px 치우침).
- **자리 판정이 엇갈려 보인 3 건** — Fe (Li ↔ Zr) · Ca (La ↔ Zr) · Tm (La ↔ Zr): 세 칸 모두 두 마커가 같은 높이에 겹쳐 하나가 가려졌다. 값은 Fe 1.32 / Ca 1.03 / Tm 0.73 ↔ Miara 1.324 / 1.030 / 0.740 으로 맞는다 → **실제 불일치 아님 (동률)**.
- **Al 세 자리 (본문으로 비선호 자리까지 대조 가능한 유일한 원소)**:

| 자리 | Miara 본문 (p. 4042) | [Anderson24] `Fig. 3d` figure-read ≈ | 차 |
|---|---|---|---|
| Li | 1.36 | 1.32 | −0.04 |
| Zr | 1.87 | 1.84 | −0.03 |
| **La** | **3.16** | **4.04** | **+0.88** 🔴 |

  La 자리 원은 다른 마커와 겹치지 않아 판독 신뢰도가 높다. 원인 후보: (i) Miara SI `Table S3` 의 Al(La) 가 본문 3.16 과 다르다 (ii) Anderson 의 전사 오류. **SI 없이 확정 불가.** 순위 (Li < Zr < La) 는 같다.
- 그 밖에 본문 인쇄값으로 대조된 비선호 자리: Ce⁴⁺(La) 1.60 ↔ Anderson 1.56 ✓.
- **산화수 첨자 17 개** 모두 Miara 선호 산화수와 같다 — Anderson 은 `Fig. 2` 의 선호 산화수 값을 옮겼다.

> ✍ **Anderson digest 정정 (2026-10-13 · 원문 보존 · 취소선 + 주석)**: ① §3b 의 *"Lu 는 `n/a`"* → **"Yb 는 `n/a`, Re 는 패널에 없음; Lu 는 값 있음 (La ≈ 0.92)"** + Al(La) 불일치 한 줄 ② §11 Figure set `3d` 행의 같은 문구 ③ §3a *"계산 예측 45종"* 줄에 *"Miara 본문에는 45 가 없다"* 주석. §19.6 의 서술은 원래 맞았다.

---

## 12. 적용 인사이트 ★

1. **세미나 표**: n = **128** 로 바꾸면 행 전체가 Miara 원문에서 직접 나오고 '(via Anderson)' 을 뗄 수 있다. 45 는 원문에 없는 수다 — 남기면 출처가 Anderson 이다.
2. **계면 반응성 보고량에 축 이름을 단다**: "혼합분만 (eq 3 · pymatgen `include_no_mixing_energy=False`)" 인지 "자체 분해 포함 (우리 v2)" 인지. 같은 LLZO\|LCO 가 −0.033 (Miara) 과 −0.23 eV/atom ([Rich16]) 으로 갈리는 것은 이 한 칸 때문이다. 우리 계면 결과를 문헌과 나란히 놓을 때 이 칸을 먼저 맞춘다.
3. **문턱을 실험 앵커로 정하고 근거를 한 문장으로 남기는 방식** (합성된 최대 1.60 eV → 2 eV) 과 **등원자가 제외 (Li 함량이 안 바뀌면 목적에 못 쓴다)** 는 우리 cascade 게이트 카드에 그대로 빌릴 수 있는 '보고량 → 판정 기준' 연결이다. 단 [Anderson24] 가 보였듯 결함에너지 **크기**는 실험 결과를 순위 매기지 못한다 → **게이트로만, 순위로는 쓰지 않는다**.
4. 음이온 자리 치환이 0 건 → 우리 "화합물 하나가 양이온·음이온 두 자리를 같이 채운다" 는 이 계보와 겹치지 않는다 (open_items A1 할 일 4).

---

## 13. 인용 가능 문장 (영문 초안 · 랩 표기 *Chem. Mater.*, 27, 4040 (2015).)

- "Defect energies were computed with PBE for 128 dopant species, each placed on the Li, La, and Zr sites of cubic Li₇La₃Zr₂O₁₂ (1,152 structures), and 108 dopant–site combinations fell below a 2 eV cutoff."
- "The 2 eV cutoff was anchored on the highest computed defect energy among dopants already synthesized in LLZO (Ce⁴⁺ on La, 1.60 eV) and then widened."
- "Charge balance was maintained by removing or adding Li according to an electrostatic criterion."
- "The interfacial reaction energy of Miara et al. counts only the mixing contribution — each side is referenced to its own grand-potential hull — so it vanishes inside both stability windows and is not comparable to reaction energies that include the electrolyte's own decomposition."

---

## 14. 주의 / 한계 (인용 규율)

- ⛔ **45 를 Miara 의 수로 인용하지 않는다** — 원문에 없다. 쓰려면 *"Anderson et al. (2024), citing Miara et al."* 로.
- ⛔ **Al(La) 값은 본문 3.16 eV 가 정본** — [Anderson24] `Fig. 3d` 의 ≈ 4.04 를 인용하지 않는다.
- ⛔ Np · Pu 칸 값 (17.30 · 13.38) 인용 금지.
- ⛔ 가넷 결함에너지·반응에너지·전압을 우리 argyrodite 값과 같은 표에 놓지 않는다 (A–D 4축 진입 금지).
- ⚠ `Table 1` 을 인용하면 **"128 (캡션) · 인쇄 칸 122"** 를 같이 안다. 세미나에는 128 을 쓴다 (논문 자신의 수).
- ⚠ **LMO = LiMnO₂** (스피넬 아님). Xiao 2020 리뷰 표의 LiMn₂O₄ 값과 섞지 않는다.
- ⚠ `Table 3` 의 "최대" = 3 V 에서 x 에 대한 최대. 전압 최대 (3.2–3.4 V) 는 figure-read 로만 있다.
- ⚠ LLZO 안정창은 출처마다 다르다 — Miara `Fig. 4` 0.47–3.39 (figure-read) · [Zhu15] 0.05–2.91 · [Rich16] 0.06–3.11 V. **어느 그림·어느 ref 인지 늘 붙인다.**
- ⚠ "LCO 가 가넷과 안정" 은 **혼합분 · 3 V 축**에서만.

---

## 15. 기법 용어 미니사전

- **결함에너지 (defect energy)**: 도펀트를 넣고 전하를 맞춘 셀이 "순수 셀 + 넣고 뺀 원자의 화학퍼텐셜" 보다 얼마나 높은가. 여기서는 μ 를 **도핑 조성이 속한 hull 면**에서 재므로, '그 조성의 경쟁상 묶음보다 얼마나 높은가' 에 가깝다. 낮을수록 잘 녹는다.
- **hull 면의 화학퍼텐셜**: 볼록 껍질 (convex hull) 의 한 면은 평면이고, 그 평면의 원소 방향 기울기가 그 상 묶음과 평형인 μ_i 다. 면이 바뀌면 μ 도 바뀐다.
- **등원자가 / 아원자가 / 초원자가 (iso- / sub- / supervalent)**: 도펀트 전하가 호스트 자리 전하와 같음 / 낮음 / 높음. LLZO 에서 초원자가 → Li 빈자리 (Li < 7 pfu), 아원자가 → Li 침입 (Li > 7 pfu). 등원자가는 Li 수를 안 바꾼다.
- **pfu (per formula unit)**: 화학식 Li₇La₃Zr₂O₁₂ 하나당 개수. 6.5 Li pfu 근처가 전도도 최고라는 것이 실험 관찰.
- **24d / 96h / 48g**: 입방 가넷 Li 자리의 Wyckoff 기호 — 24d 사면체 · 96h 팔면체 (48g 는 그 중심). SOF = 자리 점유율.
- **Ewald (정전기) 선별**: 점전하 정전기 에너지만으로 수많은 Li 배열을 순위 매겨 DFT 할 후보를 줄이는 값싼 사전 필터.
- **grand potential φ · μ_Li ↔ 전압**: Li 를 저장고와 주고받게 한 열역학 퍼텐셜. μ_Li = μ_Li(Li 금속) − eV 이므로 0 V ↔ μ_Li = 0, 5 V ↔ −5 eV.
- **고유 안정창 (intrinsic stability window)**: 그 상이 grand potential 상평형도에서 안정한 μ_Li (전압) 범위. 우리 ESW 와 같은 구성.
- **pseudo-binary · tie line · kink**: 두 조성 (전해질 · 전극) 을 잇는 선 위에서 섞음 비 x 를 바꿔 가며 hull 에너지를 본 1차원 단면. 꺾임점 (kink) 마다 산물 묶음이 바뀐다.
- **no-mixing energy**: 섞지 않아도 각 상이 그 μ_Li 에서 스스로 분해하며 내는 에너지. eq 3 은 이것을 빼고 (혼합분만), 우리 v2 는 넣는다.
- **data-mined 치환 (Hautier 2011)**: 알려진 구조의 이온을 통계적으로 그럴듯한 이온으로 바꿔 가상 화합물을 만들어 상평형도에 넣는 방법 — Li₂CoO₃ 같은 미확인상이 산물로 나올 수 있다.
- **4원 단면 (quaternary section)**: 5원계 조성 공간을 산화물 꼭짓점 넷으로 자른 단면 (`Fig. 1`).

---

## 16. 재현 기록 — 숫자를 어떻게 읽었나

- **그림 추출**: `python3 tools/litdb/extract_figures.py --slug miara2015_llzo_cation_dopants_cathode_interphases --pdf "litdb/inbox/Miara2015 ChemMater First-Principles Studies on Cation Dopants and Electrolyte Cathode Interphases for Lithium Garnets.pdf" --clean` → 6 장. **`Table 2` 는 '영역 없음' 으로 빠졌고** (텍스트만 있는 표라 기하 검증에 걸림) 손으로 잘랐다 — p. 4043 왼쪽 단, 캡션 위 377.0 pt ~ 아래 괘선 477.5 pt (`figures.json` `t2.manual_crop` · `missing_labels[t2].resolved`).
- **모든 그림은 PDF 안에 래스터로 박혀 있다** (벡터 아님): `Fig. 1` 566×553 · `Fig. 2` 1945×1069 · `Fig. 3` 662×711 · `Fig. 4` 666×606 px · **`Table 1` 도 이미지** (8400×2495). `Table 2`·`Table 3` 만 텍스트 레이어.
- **`Table 1` 계수**: 크롭을 좌우 두 쪽으로 나눠 직접 읽고 칸을 셌다 (94 원소 · 122 칸).
- **`Fig. 2`**: 크롭 전체 + 확대 2 곳 (악티늄족 줄 · p 블록) 을 직접 읽어 73 원소를 전사했다 (§3c).
- **`Fig. 4` 픽셀 판독**: PDF 내장 래스터 (xref 276, 666×606) 를 원 해상도로 뽑았다. x: 눈금 라벨 중심 0 V = 156 · 1 V = 256 · 3 V = 456 · 4 V = 556 · 5 V = 656 px (100 px/V). y: 0.00 = 78.5 px · −0.30 = 465.0 px. 막대 끝점 = 막대 행 ±12 px 안에서 세로 두께 ≥ 7 px 인 열 묶음의 중앙. 곡선 = 색 마스크 + 세로 런 두께 (≥ 4 px = 굵은 선 = LLZO). **검산: 3 V 6 개 ↔ `Table 3` 모두 ≤ 1 meV/atom.**
- **`Fig. 3` 픽셀 판독**: 내장 래스터 (xref 248) · 틀 x 151.5–635.5 px = 0–1 · y 25.5–598.5 px = 0.00 ~ −0.04. 네모 = 침식 후 연결성분 중심 · 별 = 빨강 성분 중심. **검산: 별 x 0.618 · −0.0334 = 본문 0.618 · `Table 3` −33.37.**
- **[Anderson24] `Fig. 3d`**: litdb 크롭 `fig_3.png` (2118×1573) · 격자선 0 eV = y 1486 · 5 eV = y 1252 · 블록 경계 x 135 / 305.5 / 1007 / 2077 · 슬롯 배정과 색 분류는 `tools/litdb/anderson2024_fig_verify.py` 의 `FIG3CD_LABELS` · `_site_class` 를 그대로 썼다 (자리별 중앙 y). Al 칸은 연결성분 중심으로 한 번 더 읽어 같은 값 (La 4.05 · Zr 1.84 · Li 1.32).
- 판독 스크립트는 일회성 대조라 repo 에 넣지 않았다 — 위 매개변수로 다시 낼 수 있다.
- **pymatgen 의미 확인**: `src/pymatgen/analysis/interface_reactions.py` (master) 의 `GrandPotentialInterfacialReactivity.__init__` · `_get_grand_potential` 을 원문으로 읽었다 (§7c).
