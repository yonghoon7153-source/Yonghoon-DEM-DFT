# Diffusion Mechanism of Li Argyrodite Solid Electrolytes for Li-Ion Batteries and Prediction of Optimized Halogen Doping: The Effect of Li Vacancies, Halogens, and Halogen Disorder — de Klerk, Rosłoń & Wagemaker (Chem. Mater. 2016)

> slug `deklerk2016_diffusion_site_disorder_argyrodite` · DOI `10.1021/acs.chemmater.6b03630` · type `DFT-AIMD (순수 계산, 실험 0)` · PDF `82ea256b/f8e6711f-32._Diffussorder.pdf` (inbox #32, 본문 9 pp 7955–7963) + **SI 확보(2026-07-28, 인박스 #32 Sup = `82ea256b/428d530d-32._Sup_Disorder.pdf`, 6 pp: Tables S1–S3 전표(300/450/600 K σ·점프율·Ea) + Fig S1(PSe₆/Br 밀도)·S2(PSe₆/Br 점프그래프)·S3(4a-RDF))** · digested `2026-07-28` (동일자 SI 반영 갱신) · status ✅
> elements: Li, P, S, Se, Cl, Br, I
> methods: DFT, AIMD
> **저자**: Niek J. J. de Klerk, Irek Rosłoń, **Marnix Wagemaker*** — Department of Radiation Science and Technology, **TU Delft** (네덜란드). Chem. Mater. 2016, 28, 7955−7963. Received 2016-08-29 / Revised 09-29 / Published **2016-10-14**. **[외부]** (ADEM 네덜란드 + ERC FP7 307161 지원).

---

## 0. 이 digest를 읽는 법 (우리에게 왜 1순위인가)
이 논문은 argyrodite Li⁺ 전도의 **"halogen site disorder → inter-cage 활성화 → 거시 σ"** 서사의 **AIMD 원전(2016)** 이다 — Kraft 2017(실험 무질서 62→0 %)·Rao 2013/Rayavarapu 2012(실험)·[GG]/[Liu]/[Liang](후속 계산)·[Bai](리뷰)가 전부 이 논문을 무질서-메커니즘의 계산 근거로 소환한다. 우리 캠페인의 세 줄기가 이 논문에 정면으로 닿는다:
1. **무질서 decorate 방법론** — 그들이 AIMD 셀에 4a/4c S/X 무질서를 *어떻게* 넣었나 = 우리 **comp2 disorder ensemble**(라벨스왑 d-level·cfg0/1/2·anneal+relax)의 10년 전 원형. §4.2에 전 절차 복원.
2. **"무질서 75 %에서 σ 최고" 주장의 정확한 형태** — 인용 사슬에서 뭉개지기 쉬운 이 주장의 원문 조건(어느 조성·몇 K·무슨 지표·왜 100 %가 아닌가)을 §5.7에 고정. [Liu] digest의 재인용 판정 포함(§13).
3. **inter-cage = 율속** — 우리 `li_percolation` F*(0.191→0.078 eV)·BVSE 경로 위계·[Rao11]/[Dyre]/[Perc] 서사의 **jump-statistics 1차 계산 증거**.

> ⚠ **사이트 표기 주의 (이 논문 전체에 걸림)**: de Klerk는 free-anion 두 자리를 **4a("outside the cages") / 4c("inside the cages"=Li 48h 케이지 중심)** 로 부른다. Kraft 2017·[Liu]·우리 baseline 계열 표기로는 **de Klerk 4c ≡ 4d(cage-center, free-S²⁻ 기본 자리)**, 4a는 공통(F-43m 원점 선택 차이). 즉 이 논문의 "Cl 4c 점유 75 %" = 실험 문헌의 **"4d-자리 Cl 점유 75 %"**. 아래에서는 원문 표기(4a/4c)를 유지하되 필요 시 (=4d)로 병기.

## 1. 한 줄 요약
Li₇PS₆·Li₇PSe₆·Li₆PS₅Cl/Br/I 전 계열을 **VASP GGA AIMD(단위셀 52원자, 100 ps, 300/450/600 K)** 로 돌려 Li⁺ 점프를 **doublet(48h쌍 내)·intracage(케이지 내)·intercage(케이지 간, 율속)** 3종으로 분해 — (a) Cl/Br는 빠르고 I는 **intercage 점프 0**(모든 T)으로 느린 이유가 **halogen의 4a/4c 분포**임을 인공 배열(all-4a vs all-4c)로 입증하고, (b) Li vacancy와 halogen 치환 효과를 가상 조성(Li₆PS₆·Li₇PS₅Cl)으로 분리해 **둘 다 필요**함을 보이고, (c) Cl 주위 케이지엔 평균 **5 Li vs S 주위 7 Li**(빈 doublet 상존 → intercage 촉진)라는 국소 메커니즘을 RDF로 제시한 뒤, (d) **Li₆PS₅Cl의 최적 Cl 분포 = 4a:4c = 1:3(4c 점유 75 %)** 에서 limiting jump rate가 50:50 대비 **2×** → "합성으로 무질서를 조절하면 σ 2배" 예측, (e) 보너스로 **Li₅PS₄X₂**(할로겐-rich)가 Li₆PS₅Cl/Br급 σ + 공기/수분 안정 개선 후보라고 제안한, **halogen-disorder 엔지니어링의 계산 원전**.

## 2. 메타 / 동기
| 항목 | 내용 |
|---|---|
| 시스템 | HT phase(F-43m, No. 216, a≈10 Å) 고정: **Li₇PS₆·Li₇PSe₆·Li₆PS₅Cl·Li₆PS₅Br·Li₆PS₅I** + 가상 **Li₆PS₆·Li₇PS₅Cl** + 신규 **Li₅PS₄Cl₂/Br₂/I₂** + Li₆PS₅Cl 무질서 5분포 |
| 질문 | (1) 왜 Cl/Br는 10⁻³ S/cm급인데 I는 수 자릿수 낮나? (2) σ↑의 원인이 Li vacancy인가 halogen인가 disorder인가? (3) 무질서를 *어떻게* 조절하면 σ 최대인가? |
| 당시 알려진 것 | 실험 σ(Cl/Br ~10⁻³ ≫ I)·I는 4a만 점유(Rayavarapu ref 12)·**4c-Cl 점유↑ → σ↑ 실험**(Rao 2013 in-situ 중성자, ref 19)·NMR 다중 점프 과정(refs 18/23) — **미시 메커니즘은 미해명** |
| 방법 계보 | 저자들 직전 Na₃PS₄ 논문(ref 24, Chem. Mater. 2016)의 **site-visit jump-statistics** 방법을 Li argyrodite로 이식 |
| 시점 | **Kraft 2017보다 1년 앞** — 참조 실험 무질서 값은 Kraft가 아니라 **Rayavarapu 2012(ref 12)·Rao 2013(ref 19)·Kong/Deiseroth 2010(refs 4·15)** |

## 3. 핵심 물성 (수치 총정리)
> ⚠ **출처 규율**: 본문 명시 수치는 그대로, 그림 판독값은 **figure-read(≈)**. 조성·T별 점프율/σ/Ea 전체 표는 **SI Tables S1–S3에 있으나 이 PDF에 미포함** → n/a 표기. 전부 **소환값**(우리 db 절대값과 혼합 금지; 그들 AIMD σ·Ea는 GGA·단위셀·100 ps 조건값).

| 항목 | 값 | 조건/출처 |
|---|---|---|
| 점프 3종 거리 | **doublet 1.9 Å**(48h쌍 내) · **intracage 2.25 Å**(케이지 내 쌍간) · **intercage 가변**(케이지 연결) | 본문 §Results; 케이지 중심간 거리 **7.0 Å**(σ_J 환산용) |
| 케이지 구조 | 4c(=4d) 중심당 **48h 12개(6쌍)**; Li–Li쌍 거리 1.9 Å → **쌍당 1 Li**(≈50 % 점유) | 본문·ref 12 |
| σ (MD, 600 K) | σ_J(Cl·Br) **≈4–5 S/cm**, σ*(Cl·Br) **≈1–2 S/cm** | Fig 2 figure-read |
| σ (MD, 300 K) | σ_J(Cl·Br) **≈1 S/cm** (σ* ≈0.15–0.3) | Fig 2 figure-read; 임피던스 실측(~10⁻³)보다 **수 자릿수 높음**(단결정 상한 + GB 부재로 저자 해석) |
| Li₆PS₅I | **intercage 점프 0 — 300/450/600 K 전부** → 거시 확산 없음(도블릿 위주 국소 운동만) | 본문 §Conductivities·§Li₅PS₄X₂ |
| Li₇PS₆·Li₇PSe₆ | 300 K intercage 0; 450/600 K는 Cl/Br보다 낮은 σ | 본문·Fig 2 |
| σ 순위 (MD) | **Cl ≈ Br > PS₆ > PSe₆ ≫ I** — 실험 순위 재현(ref 12) | 본문 |
| correlation factor | **f = D*/D_J < 0.2** (Cl·Br, 전 온도) → back-and-forth 점프 다수 | 본문 (PS₆/PSe₆는 점프 수 부족으로 f 요동) |
| Ea (MD, ν₀=10¹³ s⁻¹ 가정) | **doublet·intracage 0.10–0.14 eV / intercage 0.20–0.25 eV** (Li₆PS₅Cl·Br) | 본문 (eq 2; 조성별 세부는 SI n/a) |
| Ea (문헌 대조) | NMR 단거리 0.08–0.09 / 장거리 **0.20(Br)·0.29(Cl)**; 임피던스 0.16–0.56(합성 의존); BV 단거리 0.10–0.20·intercage 0.30–0.35 | 본문 (refs 18·23·12·19) |
| 율속 판정 | **전 조성에서 intercage 점프율이 타 점프의 ≤1/5** → intercage가 거시 σ 지배 | 본문 |
| NMR 정합 | Li₆PS₅Cl ⁷Li NMR 점프율 **~1×10⁹ s⁻¹ @350 K**(ref 18); MD 300 K는 ~1자릿수 높으나(통계 부족) **450/600 K→350 K 외삽은 NMR과 정합** | 본문 |
| RDF (450 K, Li₆PS₅Cl) | 4c-**Cl 주위 Li ≈5개 / 4c-S 주위 ≈7개**(≤3.5 Å 적분; 4a도 동일 경향 Fig S3) → **Cl 근처 빈 doublet 상존** | Fig 6 + 본문; **5–7 분포가 6–6보다 안정**(전 온도·Cl/Br 공통) |
| 무질서 최적 (Fig 8, 450 K) | **4c-Cl 점유 75 %(4a:4c=1:3)** 에서 min(점프율) 최대 — **50:50 대비 limiting rate 2×** → "σ 2배" 예측 | 본문·Fig 8 |
| Fig 8 점프율 (450 K) | intercage: 0 %=**0** → 25 % ≈2×10¹⁰ → 50 % ≈3×10¹⁰ → 75 % ≈6×10¹⁰ → 100 % ≈1.3×10¹¹ s⁻¹ / doublet: ≈1×10¹² → 5×10¹¹ → 3×10¹¹ → ≈1×10¹¹ → **≈2×10⁹**(붕괴) / intracage ≈2–4×10¹¹ 거의 일정 | figure-read |
| Li₅PS₄X₂ | Cl₂·Br₂·I₂ 전부 거시 전도(**I₂도!** 단 300 K 제외); σ ≈ Li₆PS₅Cl/Br급 | Fig 9·본문 |
| 격자 효과 | Br 격자 +0.13 Å(vs Cl)·Se +0.48 Å(vs S) — **intercage 점프율엔 유의 영향 없음**(doublet/intracage만 변화) → 이온반경/부피는 거시 σ 비지배 | 본문 (ref 12·15) |

## 4. 방법 ★ (사용자 최우선 — 전 절차 복원)

### 4.1 AIMD 셋업
| 항목 | 값 |
|---|---|
| code | **VASP** (ref 25 Kresse/Hafner) |
| functional | **GGA**(ref 26 = **PBE**) — vdW 없음, DFT+U 없음 |
| basis/pseudo | **PAW-PBE** (ref 27 Blöchl) |
| ecut | **280 eV** (⚠ 낮음 — 현대 기준 soft; S/P 표준 400+ eV 대비 절감 셋업) |
| 셀 | **단위셀 1×1×1, a≈10 Å** — Li₆PS₅X = **52원자**(24 Li+4 P+20 S+4 X)·Li₇PS₆ 56·Li₅PS₄X₂ 48. **supercell 없음** |
| k-points | minimization **2×2×2** → MD **1×1×1**(Γ) |
| MD | **NVT, temperature scaling every 1000 steps**(=2 ps마다 velocity rescale; Langevin/Nosé 아님), **dt 2 fs**, **총 100 ps**, equilibration **2.5 ps** |
| 온도 | **300 / 450 / 600 K** (전 조성) |
| 초기구조 | 문헌 구조 사용(있으면; 없으면 최유사 구조) → minimization → MD |
| 오차 | 각 시뮬을 **10블록 분할** 후 표준편차(점프 과정 비상관 가정, 블록간 재평형 불필요 논리) |

### 4.2 무질서 decorate 방법론 ★★ (우리 comp2 ensemble의 원형 — 정밀 복원)
- **무질서 자유도**: 4 f.u. 단위셀의 free-anion 8자리(4a×4 + 4c×4)에 S 4개·X 4개 배치. **Fig 8 시리즈 = Cl의 4c 점유 5단계: 0/25/50/75/100 %** = 셀당 4c-Cl 0/1/2/3/4개(나머지 Cl은 4a; S는 보수적으로 반대 배치).
- **각 %당 배열 수 = 1개(단일 배열)**. 복수 배열·앙상블 평균 **없음**. 배열 선택 기준(랜덤/Ewald/enumerate) **일절 언급 없음**.
  - *우리 해석(원문 아님)*: 1×1×1 셀에서는 4c 부격자(FCC 4자리)에서 1개(C=4)·2개(C=6)·3개(C=4) 고르기가 **입방 대칭으로 사실상 등가**라 "분포 %만 정하면 anion 배열은 거의 유일" — 단일 배열이 우연히 정당화되는 셀 크기. **더 큰 셀에선 성립 안 함**(배열 다양성 발생) → 이 방법을 supercell로 확장하려면 우리처럼 config 앙상블 필수.
- **표준 Li₆PS₅Cl(Fig 2·3·4의 기본 시뮬) = 50:50 배열**(Fig 4b: 4c에 Cl 2 + S 2) — "currently prepared materials"(refs 12·19의 실험 ≈even 분포)를 모사. **Li₆PS₅I = all-4a**(실험 ref 12 그대로).
- **Li 배치**: 48h 24쌍에서 **쌍당 1 Li 제거**(쌍내 1.9 Å 동시점유가 에너지적 불리) → 24 Li. 쌍 안에서 어느 쪽 48h를 남기는지 기준 **미명시**. Li-vacancy는 조성으로 내재(Li₆ vs Li₇) — **명시적 공공 배치 규칙 없음**; 흥미롭게도 "Cl 케이지 5 Li / S 케이지 7 Li"의 불균등 분포는 **MD 중 자발 형성**(§5.6, 초기 배치 아님).
- **가상 조성 분리실험**: **Li₆PS₆**(=Li₇PS₆−1Li/f.u.: vacancy만, Cl 없음)·**Li₇PS₅Cl**(=Li₆PS₅Cl+1Li/f.u.: Cl만, vacancy 없음) — 변수 분리를 *조성 조작*으로 구현(우리 grand-canonical이 아니라 중성 위반을 감수한 인공 셀; 전하보상 처리 언급 없음 → 사실상 jellium 배경 가정으로 추정, **원문 미명시**).
- **Li₅PS₄X₂**: free-anion 8자리 전부 X(4a 4 + 4c 4 전부 halide), Li 20개.

### 4.3 점프 통계 → 물성 환산 (post-processing 수식 체계)
1. **site-visit 추적**: 각 Li가 방문하는 결정학 자리를 MD 내내 기록(방법 = ref 24 Na₃PS₄ 논문). **자리 반경 ≈0.9 Å**(이웃 자리 겹침 직전 최대).
2. **τ = J/(N·t)** (eq 1): J=점프 수, N=Li 수, t=시간 → 점프유형별 평균 점프율.
3. **ΔE_A = −kT·ln(τ/ν₀)** (eq 2, Vineyard ref 28): **ν₀ = 1×10¹³ s⁻¹ 가정** — Ea는 점프율의 로그 재표현(아레니우스 기울기 아님!).
4. **D_J = τ·a²/(2d)** (eq 3, Einstein–Smoluchowski, d=3): 점프율 확산계수. **σ_J용 a = 7.0 Å**(케이지 중심간 — "케이지 내 평균 위치=중심"이라 intercage 점프가 실질 변위라는 논리).
5. **D\*** = MSD tracer (eq 4).
6. **σ = ne²z²D/(k_BT)** (eq 5, **Nernst–Einstein**) → σ_J(점프율)·σ*(MSD) 두 벌. **Haven 보정 없음** — 대신 **f = D*/D_J**를 상관계수로 별도 보고(f<0.2 = back-and-forth 다수 = σ_J이 σ*보다 과대).

## 5. 결과 — 섹션별 상세

### 5.1 구조·점프 분류 (Fig 1)
HT F-43m: PS₄는 4b, free S는 4a+4c, Li는 4c를 둘러싼 48h(≈50 % 점유). 할로겐 치환 시 X는 4a 또는 4c만 차지(PS₄의 S는 불가침, ref 9). 48h 6쌍 = 케이지. MD 궤적에서 점프 3종 확인: **doublet(1.9 Å) → intracage(2.25 Å) → intercage(가변)**. **거시 확산엔 3종 모두 필요, 최저 점프율이 율속** — 이 프레임이 논문 전체의 렌즈.

### 5.2 조성별 σ (Fig 2)
5조성 아레니우스(σ_J·σ* 쌍). **Cl·Br 최고, PS₆·PSe₆ 중간, I는 거시 확산 0**(실험 순위 재현). MD σ ≫ 임피던스 실측: (a) PS₆/PSe₆는 실험이 LT phase라서, (b) Cl/Br는 **grain boundary가 실측을 지배**(수십 nm 전하수송, ref 18)라서 — MD는 결정 bulk **상한**. ⁷Li NMR(bulk 국소 점프)과는 동일 자릿수 → AIMD 검증. f<0.2 (Cl·Br): 점프의 8할이 왕복. **이온반경 무관론**: Br(+0.13 Å)·Se(+0.48 Å) 격자 팽창에도 intercage 점프율 유사 → "부피/Li"는 거시 σ 비지배(doublet/intracage만 민감) — Kraft 2017의 "무름/분극성" 서사와 *다른 축*으로 격자 크기를 기각한 선행 판정.

### 5.3 Li⁺ 밀도 시각화 (Fig 3, 450 K)
Li₇PS₆·Li₆PS₅Cl·Li₆PS₅I 밀도맵 — 전 조성 4c 둘레 케이지 4개 구조. **I: 48h쌍 고밀도만**(doublet, XRD·NMR과 정합) → 쌍간 경로 없음 = 국소 진동만. **PS₆: 케이지 내 국소화 강함**(큰 maxima). **Cl: maxima 작고 퍼짐** = 케이지 내 고속 순환 + 케이지 연결 시작. [GG]/[Liu]의 확률밀도 그림들의 원형.

### 5.4 점프 통계·Ea (Fig 4)
450 K 점프 그래프(선 굵기=점프율): PS₆=doublet+intracage 위주(intercage 소수), **Cl=3종 모두 + intercage 다수(빨강 망)**, I=doublet뿐. MD Ea(ν₀=10¹³): 단거리 0.10–0.14 / **intercage 0.20–0.25 eV** — NMR(0.08–0.09/0.20–0.29)·BV(0.10–0.20/0.30–0.35)와 정합, 임피던스(0.16–0.56)는 합성 의존 산포. **"intercage rate가 전 조성에서 ≥5× 낮음 → σ 올리려면 intercage부터"** — 설계 지침의 근거 문장.

### 5.5 vacancy vs halogen 분리 (Fig 5) — 가상 조성 실험
"Cl→S 치환의 σ↑가 단지 전하보상 Li-vacancy 때문인가?" 검증: **Li₆PS₆**(vacancy만)과 **Li₇PS₅Cl**(Cl만) 모두 케이지+intercage 연결이 나타나고 **rate-limiting intercage 점프율은 실제 Li₆PS₅Cl과 유사**(doublet/intracage는 서로 크게 다름). → **vacancy와 Cl 치환 둘 다 유의하게 작용, σ↑는 둘의 합작** — "vacancy가 전부"라는 단순론 기각. (우리 dual_mechanism 기록 — barrier와 prefactor/carrier 반반 — 과 같은 결의 2016년 판.)

### 5.6 국소 메커니즘: 5–7 Li 분포 (Fig 6) — 이 논문의 미시 화학 핵심
450 K Li₆PS₅Cl에서 4c-Cl vs 4c-S 주위 Li-RDF: 피크(≈2.5 Å) 위치·폭은 같으나 **Cl 주위 적분(≤3.5 Å) ≈5 Li vs S 주위 ≈7 Li**(4a도 동일 경향). 해석: **Cl⁻(−1)은 S²⁻(−2)보다 Li를 덜 묶음** → 전하보상 공공이 Cl 케이지에 몰림 → **Cl 근처엔 항상 빈 doublet** → intercage 점프의 착지 자리 상존 → 촉진. 전 온도·Cl/Br 공통으로 **5–7 분포 > 6–6 안정**. 부수 통찰: argyrodite 안정성 계산(ref 6)은 Li-배치(할로겐 유도)에 강민감할 것 — Li-배치 공간이 너무 커 본 논문 범위 밖 선언(→ 우리 enumeration/Ewald 접근이 채우는 자리).

### 5.7 ★ Halogen disorder — "75 % 최적"의 정확한 형태 (Fig 7·8)
- **동기**: vacancy로는 Cl vs I의 수 자릿수 차이를 설명 못 함. 실험(ref 12)은 I=4a만/Cl=4a+4c 분포, 실험(ref 19)은 4c-Cl↑→σ↑.
- **인공 배열 실험 (Fig 7, 450 K, Li₆PS₅Cl)**:
  - **all-4a**(I 모사): **intercage 점프 0** — 케이지들이 고립(Fig 7a: 초록+파랑만). Li₆PS₅I가 느린 이유 = 화학이 아니라 **자리 분포**.
  - **all-4c**: intercage 폭발적 증가(Fig 7b: 빨강 망)하나 **doublet 점프율 급락 → doublet이 새 율속** → intercage가 "국소 운동"으로 전락, σ 여전히 낮음.
  - → **무질서(4a+4c 동시 점유) 자체가 거시 확산의 필요조건**. 두 자리 치환이 서로 다른 점프 유형을 켠다: **4c-X → intercage↑ / 4a-X(=4c-S 유지) → doublet 유지**.
- **분포 스캔 (Fig 8, 450 K, 단일 배열/점)**: 4c-Cl 0/25/50/75/100 %에서 intercage 단조↑·doublet 단조↓·intracage 평탄 → **doublet과 intercage 곡선이 75 %와 100 % 사이에서 교차**. min(3종 점프율)의 최대 = **75 %**:
  - 75 %에서 min = intercage ≈6×10¹⁰ s⁻¹ vs 50 %에서 min = intercage ≈3×10¹⁰ → **"limiting jump rate 2×"** (원문: *"the highest Li-ion conductivity can be obtained when three-quarters of the 4c sites (and one-quarter of the 4a sites) are occupied by Cl ions... a limiting jump rate 2 times larger compared to when the Cl ions are evenly distributed"*).
  - 100 %는 min = doublet ≈2×10⁹ → 50:50보다도 **~15× 나쁨** — "무질서↑=σ↑ 단조"가 **아님**.
- **주장 형태 요약(재인용 검증용)**: ① 조성 = **Li₆PS₅Cl**(Cl 1.0; Br·I는 "최적 분포 다를 것" 명시 — Tables S1–S3 근거), ② 온도 = **450 K 단일점**, ③ 지표 = **min-jump-rate 극대화**(σ 직접 계산 아님; "σ 2배"는 σ_J∝intercage rate 논리의 예측), ④ 셀 = 단위셀·분포당 단일 배열·100 ps, ⑤ 실행 제안 = **열처리로 무질서 조절 가능**(ref 19) → "1:3 분포 합성 시 σ 2배" 전망.
- **성립 이유(원문 논리)**: 4c-Cl은 intercage를 켜지만 doublet을 끄는 **이율배반 레버** → 최적은 양 끝이 아닌 내부점. 3:1은 "intercage를 충분히 켜되 doublet이 아직 안 죽는" 지점 — 정량적 이유 설명은 없음(점프율 곡선의 교차가 사실상 전부).

### 5.8 Li₅PS₄X₂ — 할로겐-rich 제안 (Fig 9)
"무질서가 좋다면 할로겐을 더 넣어 4a·4c를 모두 X로": Li₅PS₄Cl₂/Br₂/I₂ AIMD → **전부 거시 전도**(Li₅PS₄I₂도 450/600 K에서 Cl₂/Br₂급 — Li₆PS₅I와 극명 대조), σ ≈ Li₆PS₅Cl/Br 동급. 역설 포인트: Li₆PS₅Cl에서 all-4a·all-4c는 나빴는데 **4a+4c 완전 점유(X₂)는 좋음** → "4a와 4c가 *둘 다* (같은 halide로라도) 점유되는 것"이 관건. I-rich 함의: Li₇₋ₓPS₆₋ₓIₓ에서 x>1이면 I가 4c로 밀려 들어감 → σ↑ 전략(ref 30 Pecher와 연결; [Rao2025]의 10년 전 예고). **안정성 보너스 추정**: free-S²⁻를 Cl⁻/Br⁻로 바꾸면 **산소·수분 안정 개선 "not unlikely"** — 정량 없음, 순수 추정( [Zhu20] 가수분해 지도·[Zuo]/[Liu] Cl-rich 서사의 씨앗 문장).

## 6. 메커니즘 종합 (Conclusions 재구성)
1. 할로겐 치환은 전하보상 Li-vacancy를 만들지만, **vacancy 양만큼이나 halogen "분포"가 중요** — 분포가 **vacancy 분포를 결정**(5–7 Li)하고, 그것이 국소 확산(빠름)을 거시 σ로 번역하는 스위치.
2. **4a·4c 각 자리의 치환이 서로 다른 점프 유형을 가속**(4c→intercage, 4a쪽 구성→doublet 유지) + 거시 확산은 3종 전부 필요 → **두 자리에 걸친 분포(=site disorder)가 고-σ의 필요조건**.
3. 처방 둘: (a) 분포 최적화(Li₆PS₅Cl 1:3 → σ 2×), (b) 할로겐 총량 증가(Li₅PS₄X₂ — σ 동급 + 공기/수분 안정 가능성).

## 7. 전체 논증 흐름
점프 3종 정의(Fig 1) → 5조성 σ·순위 재현+NMR 정합(Fig 2) → 밀도맵으로 I=doublet-only 시각화(Fig 3) → 점프통계·Ea로 intercage=율속 확정(Fig 4) → 가상 조성으로 vacancy/halogen 분리(Fig 5) → RDF 5–7 Li로 국소 메커니즘(Fig 6) → 인공 배열 all-4a/all-4c로 무질서=필요조건 입증(Fig 7) → 분포 스캔 최적 75 %(Fig 8) → 할로겐-rich 일반화(Fig 9) → "분포 조절 + 함량 증가" 처방으로 닫음.

## 8. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | HT Li₇PS₆ 구조(48h 노랑·4a 분홍·4c 빨강·PS₄) | 사이트 표기 매핑(4c=cage center) 기준 그림 |
| 2 | 5조성 σ_J·σ* 아레니우스(300–600 K) | MD σ=bulk 상한·GB 격차 논리의 원전; **σ_J vs σ*(f<0.2) 분리 보고** 양식 |
| 3 | Li 밀도맵 3조성(450 K) | I=doublet-only·Cl=퍼짐 — [GG]/[Liu] 확률밀도의 원형; 우리 li_density_cube 그림과 동종 |
| 4 | 점프 그래프(선굵기=rate) PS₆/Cl/I | **jump-network 시각화** — 우리 percolation 그림의 그래프 판; deck용 3종 점프 도식 |
| 5 | 가상 Li₆PS₆·Li₇PS₅Cl 점프 그래프 | **변수분리(vacancy vs halogen) 설계** — 우리 가상 조성 실험 템플릿 |
| 6 | Li-RDF: 4c-Cl vs 4c-S (450 K) | **5–7 Li 메커니즘** — 우리 site-분해 분석(어느 케이지에 공공이 모이나)으로 재현 가능 |
| 7 | all-4a vs all-4c 점프 그래프 | **무질서=필요조건의 결정적 실험** — 우리 comp2 ordered(d=0) frozen과 동일 물리 |
| 8 | **점프율 vs 4c-Cl 점유(0–100 %)** | **★ 75 % 최적의 원자료** — 우리 disorder ensemble의 d-level 스캔과 정면 대응 |
| 9 | Li₅PS₄X₂ 아레니우스 | 할로겐-rich(우리 modelc Cl1.6 계열) σ 동급의 최초 계산 근거 |
| S1–S3 (미보유) | PSe₆/Br 점프그래프·밀도·4a-RDF + **조성·T별 σ/점프율/Ea 전표** | ⚠ 정량 표는 SI에만 — 인용 시 "SI 미보유" 명시 |

## 9. Post-processing ★
- **site-visit jump statistics**(자리 반경 0.9 Å) → 점프유형별 τ → Ea(eq 2)·D_J(eq 3) — **NEB 없이 유한온도 점프율로 장벽 서열화**. 도구 자작(ref 24 방법).
- **MSD → D\*** + **f=D*/D_J** 상관 진단(Haven 대신).
- **σ_J**: intercage rate + a=7.0 Å(케이지 중심간) — "intercage만이 실변위" 가정의 명시적 구현.
- **Li 밀도맵·점프 그래프**(선굵기=rate) 시각화, **원소별 RDF**(Li around 4c-Cl/S).
- **10-블록 오차**: 시계열 블록 분할 표준편차.
> 우리 적용: (1) **min-of-three-rates 지표** — 우리 MD에서도 doublet/intracage/intercage를 분리 집계하면 "무엇이 율속인가"를 d-level별로 말할 수 있음(현재 우리는 총 MSD만). (2) **f=D*/D_J** — 우리 Haven 논의와 등가지만 점프율 기반이라 저렴. (3) 케이지 중심간 7.0 Å 환산은 우리 F*(PMF percolation) 지표와 상보 — 같은 "inter-cage 병목"을 각각 rate와 free-energy로 잼.

## 10. 우리 DFT 대비 (comp1/modelc/comp2) → `../our_dft_baseline.md`
> **방법 라벨**: 그들 = **진짜 AIMD**(VASP GGA, 힘=DFT). 우리 Ea·D = **MLIP-MD**(UMA-s-1p1 omat) — "둘 다 AIMD" 표현 금지. 그들 절대 σ·Ea = 소환값.

| 항목 | de Klerk 2016 (AIMD) | 우리 (MLIP-MD·DFT) | 판정 |
|---|---|---|---|
| **무질서 → σ↑ 방향** | all-4a=intercage 0 → 분포 걸치면 켜짐; 최적 75 % | comp1→modelc D(600 K) 3.09→7.90×10⁻⁶ cm²/s·Ea 0.253→0.224 eV; disorder_ensemble comp1 d=0.5 **Ea 0.177±0.027**(ordered frozen은 artifact 1.17); comp2 ordered champion **Ea 0.276 ≥ comp1** → disorder 런 진행 | **✓✓ 방향·물리 일치** — "ordered/한쪽-몰림 = frozen"을 우리 d=0 아티팩트와 comp2 ordered가 독립 재현 |
| **inter-cage = 율속** | intercage rate ≤1/5 · Ea 0.20–0.25 vs 단거리 0.10–0.14 | **li_percolation F\*** comp1 **0.191** → modelc **0.078 eV**(600 K Li-밀도 PMF, anti-site가 inter-cage 평탄화); BVSE 위계·[Rao11] 정합 | **✓✓ 정면 일치** — 그들 "intercage rate만 켜면 σ↑" = 우리 "F* 하락이 σ↑ 설명". 지표만 다름(rate vs PMF 문턱) |
| **5–7 Li (공공이 Cl 케이지로)** | RDF 적분 5 vs 7; 자발 형성 | 우리 site-분해 미실시(재현 후보) — modelc vacancy 서사(prefactor·carrier)와 정합적 | ○ 재현가치 높음: UMA 궤적에서 케이지별 Li 수 히스토그램이면 즉시 검증 |
| **무질서 decorate** | 분포 %당 **단일 배열**·선택기준 없음·단위셀 52원자·minimize 후 MD 100 ps | comp2 ensemble: 같은 52원자 단위셀이지만 **d-level(0/0.5/1.0)×cfg 3개**, Cl·Br↔free-S 라벨스왑 → **UMA anneal 700 K 20 ps + FIRE relax(fmax 0.03)** 후 NVT 600/800/1000 K 200 ps | **우리가 엄밀** — 특히 un-relaxed 스왑이 σ₃₀₀ ~70 mS/cm 아티팩트를 낸 우리 v1 사례(2026-07-27)는 "단일 배열+2.5 ps equil"의 위험을 실증. 단 그들은 힘이 DFT(정확)·우리는 MLIP(빠름·앙상블 가능) — 상보 |
| **온도·창 규율** | 300/450/600 K·100 ps·점프 수 부족 시 300 K 통계 취약(자인) | 600/800/1000 K 3점 아레니우스(400/500 제외)·**MSD 2–50 ps 고정창**·멀티시드 판정·절대 σ 인용 금지 | 우리 규율이 그들 약점(300 K 저통계·10-블록 가정)을 정확히 겨냥 |
| **σ 절대값** | σ_J(300 K)≈1 S/cm — 실측 대비 수 자릿수 과대(GB 부재·상한 해석) | UMA σ 3–5× 과대 인지 → 비율만 | ✓ 같은 캐비앳 계보 — "MD σ=bulk 상한" 문장 인용 가능 |
| **vacancy vs halogen 분리** | 가상 Li₆PS₆·Li₇PS₅Cl — 둘 다 필요 | 우리 dual_mechanism(장벽↓+prefactor/carrier↑ 합작) | **✓ 결론 동형** — 2016 AIMD가 우리 반반 서사의 선행 |
| **격자 크기 무관론** | Br/Se 팽창해도 intercage 불변 | Kraft(무름·prefactor)와 별개 축; 우리 EOS(modelc 수축)·comp2 진행 | △ 주의: de Klerk는 "크기 무관", Kraft는 "무름이 Ea·σ₀ 지배" — 둘은 모순 아님(크기≠강성) but 인용 시 축 구분 |
| **75 % 최적의 강건성** | 450 K·단일 배열·jump-rate 지표 | (우리 미검증) INDEX 계산값 #8(2024 MTP-MLIP, 대규모)은 **"σ 피크 = 4c-Cl 25 %"** 보고 — 원문과 상충 | **⚠ 방법 의존 플래그** — "최적 %" 숫자는 셀 크기·배열 수·지표(rate vs MSD)·MLIP에 민감. 안전 인용은 "중간 무질서에 최적 존재(양 끝 나쁨)"까지 |
| **할로겐-rich** | Li₅PS₄X₂ σ 동급 + 안정 추정 | modelc(Cl1.6) D 2.6×·[GG]/[Zuo]/[Liu] Cl-rich 계열 | ✓ 우리 modelc 노선의 최초 계산 선례(단 그들 X₂=완전치환, 우리 1.6) |

## 11. 적용 인사이트 (깊게)
1. **comp2 disorder ensemble의 문헌 정당화 + 차별화 논리 완성**: "왜 config 3개씩 돌리나?"의 답이 이 논문 — 원전은 **분포당 1배열·2.5 ps equil**로 75 %를 뽑았고, 2024 MLIP 재검(#8)은 25 %로 뒤집었다. 즉 **최적 %는 배열·통계 민감** → 우리 anneal+relax+멀티 config 설계가 정확히 그 빈틈을 메운다. 논문/deck 문장: "the optimal halogen distribution has been debated (75 % [de Klerk] vs 25 % [MTP-MLIP 2024]); our relaxed multi-config ensemble addresses the single-configuration ambiguity."
2. **F\*와 min-jump-rate는 같은 병목의 두 척도**: 그들 "min(doublet, intracage, intercage) 극대화" = 우리 "F* 최소화"와 동일 목적함수. 우리 li_percolation 그림에 de Klerk 점프 위계(0.10–0.14/0.20–0.25 eV)를 소환값 눈금으로 병기하면 서사가 잠긴다.
3. **5–7 Li 재현 = 저비용 고가치**: UMA 궤적에서 4d(=그들 4c) 중심별 ≤3.5 Å Li 적분 히스토그램만 뽑으면 "공공이 Cl 케이지로 몰린다"를 comp1/modelc/comp2에서 검증 가능 — vacancy-prefactor 서사의 미시 그림.
4. **doublet 붕괴 경고 = Cl-rich 상한의 물리**: all-4c에서 doublet이 죽어 σ가 꺾인다는 관찰은 "무질서·Cl은 다다익선"이 아님을 원전이 이미 못박은 것 — modelc(1.6)·comp2 d=1.0 해석 시 "어느 점프가 새 율속이 됐나"를 점검할 것.
5. **Li₅PS₄X₂·I-rich 예고**: [Rao2025]의 I-rich·[Son]의 물질군 교체 이전에, 2016년에 이미 "free-S²⁻를 halide로 바꿔 공기/수분 안정"을 추정으로 적어둠 — 우리 axis-④(대기) 서사의 최초 씨앗 인용처.

## 12. 인용 가능 문장 (deck/paper용)
- "de Klerk et al. (AIMD, 2016) showed that macroscopic diffusion in Li₆PS₅X requires all three jump types — doublet, intracage, and the rate-limiting intercage — and that halogen site disorder over 4a/4c is what switches the intercage jumps on: with all halides on 4a (as in Li₆PS₅I) no intercage jump occurs at any simulated temperature."
- "Their predicted optimum, 75 % of the cage-center (4c/4d) sites occupied by Cl (a 1:3 4a:4c distribution), maximizes the *minimum* jump rate at 450 K — twice that of the even distribution; note this is a single-configuration, single-cell, jump-rate-based prediction, and a 2024 large-scale MLIP study instead reports a 25 % optimum."
- "On average only five Li surround a 4c-Cl cage versus seven around a 4c-S cage: the charge-compensating vacancies condense next to the halide, so an empty 48h doublet is always available to receive an intercage jump — the microscopic origin of disorder-enhanced conduction."
- "Artificial compositions Li₆PS₆ (vacancies only) and Li₇PS₅Cl (Cl only) both reproduce the rate-limiting intercage jump rate of Li₆PS₅Cl — vacancies and halogen substitution are jointly, not singly, responsible."
- "Our percolation threshold F* (0.191→0.078 eV, comp1→modelc) is the free-energy analogue of de Klerk's min-jump-rate criterion: both measure the same inter-cage bottleneck that anion disorder flattens."

## 13. 주의/한계 (over-claim 방지) + 재인용 판정
- **75 % 주장의 조건 4중 축약 금지**: Li₆PS₅Cl 전용(Br/I 상이 명시)·450 K 단일점·jump-rate 지표(σ 직접 아님)·분포당 단일 배열. "argyrodite는 75 % 무질서가 최적" 일반화는 원문 초과.
- **[Liu] digest 재인용 판정 (요청 항목)**: liu2022 digest의 "Klerk … 75% 무질서 시 최고" — **핵심은 정확**(4d(=Klerk 4c) Cl 점유 75 %=1:3에서 limiting rate 최대). 단 ① 같은 행의 "무질서↔σ 양의 관계"는 **비단조**(0 %·100 % 모두 저전도, doublet↔intercage 교차)를 단조로 축약, ② Klerk 최적은 **Cl 1.0** 기준이라 Liu의 LPSCl₁.₅(61.7 %)에 그대로 씌우는 건 원문도 경고한 외삽. → liu2022 §14에 정정 각주 추가(2026-07-28).
- **후속 상충**: INDEX 계산값 #8(2024, MTP-MLIP 대규모·비-아레니우스)은 **σ 피크 = 4c 25 %** — 최적 위치는 방법 의존. 안전한 합의는 "양 끝(0/100 %)이 나쁘고 중간에 최적 존재"까지.
- **Excel 메모 오류 정정**: INDEX 계산값 #6의 "LPSCl Ea ~0.38 eV"는 **이 논문 값이 아님**(본문 MD Ea = 단거리 0.10–0.14/intercage 0.20–0.25 eV; 0.38은 Rao2011 임피던스 계열 값과 혼입 추정) → INDEX 행 교정함.
- **SI 미보유**: 조성·T별 점프율/σ/Ea 전표(Tables S1–S3)·Br/PSe₆ 그림(S1·S2)·4a-RDF(S3) 없음 — 본 digest의 σ·Fig 8 수치는 **figure-read(≈)**.
- **셋업 연대적 한계**: ecut 280 eV·Γ-only MD·velocity-rescale NVT·100 ps·단위셀 52원자·10-블록 오차(점프 비상관 가정) — 2016 기준 표준이나 현대 기준 soft. 절대 Ea·σ는 이 조건값으로만 소환.
- **Ea는 아레니우스 기울기가 아님**: eq 2(τ와 ν₀=10¹³ 가정의 로그 변환) — 우리·실험 아레니우스 Ea와 정의가 다름. 직접 등치 금지(방향·서열만).
- **가상 조성(Li₆PS₆·Li₇PS₅Cl)의 전하 처리 미명시** — 결과는 시사적, 정량 인용 비권장.
- **300 K 통계 취약 자인**: 점프 수 부족(I·PS₆·PSe₆ intercage 0; NMR 대비 1자릿수 편차) — 300 K 값 인용 금지, 450/600 K·외삽만.
- 안정성·기계·전자구조·ESW = **범위 밖**(n/a). Li₅PS₄X₂ 공기/수분 안정은 **추정 문장**("not unlikely")이지 계산 아님.

## 14. 기법 용어 미니사전
- **doublet jump**: 1.9 Å 떨어진 48h 자리쌍 내 왕복 점프. 가장 빠름·국소.
- **intracage jump**: 같은 케이지의 다른 48h쌍으로 점프(2.25 Å). 케이지 내 순환.
- **intercage jump**: 이웃 케이지로 점프(거리 가변, 중심간 7.0 Å). **전 조성에서 최저 rate = 거시 σ 율속**.
- **site-visit jump statistics**: MD 궤적에서 각 Li의 결정학 자리 방문 이력(자리 반경 ~0.9 Å)으로 점프를 세는 방법 — NEB 없이 유한온도 rate/장벽 서열.
- **σ_J vs σ\***: 점프율 기반(D_J=τa²/6, a=7.0 Å) vs MSD 기반(D*) Nernst–Einstein σ. **f=D*/D_J<1**이면 왕복 상관(σ_J 과대).
- **halogen(site) disorder**: X⁻와 free-S²⁻가 4a("케이지 밖")·4c(=4d, "케이지 중심") 두 자리에 섞여 앉는 것. Rietveld 점유율로 실측(Rayavarapu/Rao/Kraft), 열처리로 조절(ref 19).
- **5–7 Li distribution**: Cl 중심 케이지 평균 5 Li / S 중심 7 Li — 전하보상 공공이 할라이드 케이지에 응집, 빈 doublet이 intercage 착지점 제공.
- **velocity-rescale NVT**: 1000스텝(2 ps)마다 속도 재조정으로 온도 유지 — Langevin/Nosé보다 조악한 구식 서모스탯(동역학 교란 가능).
- **min-of-three-rates 최적화**: σ를 올리려면 3종 점프율의 최솟값을 키워야 한다는 설계 지표 — Fig 8의 75 % 최적이 이 지표의 산물.
