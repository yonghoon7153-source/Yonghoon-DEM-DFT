# Electrochemical performance of bulk-type all-solid-state batteries using small-sized Li7P3S11 solid electrolyte prepared by liquid phase as the ionic conductor in the composite cathode — Calpa et al. (*Electrochim. Acta* **2019**, 296, 473–480) · 밀링 없이 만든 미립 SE (액상법 ≈500 nm) vs 볼밀 SE (>10 µm) · LiNbO₃-NCM111 79 wt% 복합양극

> slug `calpa2019_small_li7p3s11_liquid_phase_composite_cathode` · DOI `10.1016/j.electacta.2018.11.035` · type `exp (액상법 ≈500 nm vs 볼밀 >10 µm Li₇P₃S₁₁ · LiNbO₃-NCM111 : SE : VGCF = 79:19:2 · XRD/Raman/펠릿 EIS/SEM-EDX/반쪽셀 EIS · 시뮬 없음)` · PDF `e0348abf-7._Electrochemical_performance_of_bulk-type_all-solid-state_batteries_using_small-sized_Li7P3S11_solid_electrolyte_prepared_by_liquid_phase_as_the_ionic_conductor_in_the_composite_cathode.pdf` (본문 8 pp · SI 없음) · digested `2026-10-30` · status ✅

> topic: size_effect (SE 입도 효과)
> elements: Li, P, S, Ni, Co, Mn, Nb, O, C, In
> methods: XRD, Raman, EIS, SEM-EDX, galvanostatic cycling, equivalent circuit

<!-- 실독 기록 (2026-10-30, litdb-curator)
     본문 8 쪽 전부 읽었다 (pdftotext + 쪽 렌더).  본문에 보충자료 언급이 없다 (SI 없음으로 판단).
     크롭 11 장 = 그림 9 (Fig. 8 은 벡터 그림 — 쪽 렌더 영역으로 잘랐다) + 표 2 — 전부 열어 확인했다.
     판독 근거로 Fig. 3 의 저주파 절편은 500 dpi 로 따로 확대해 읽었다.
     표기 규약: 논문에 적힌 값 = stated · 그림에서만 읽은 값 = 판독 ≈ · 논문에 없는 계산 = 우리 산수.
     쪽 표기 = 저널 쪽 p. 473–480 (PDF 1–8).  pdftotext 는 µ 를 'm' 로 뽑는다 — 그림 눈금으로 단위 확인. -->

## 0. 이 digest 를 읽는 법 — 왜 지금 이 논문인가, 그리고 원문 판정

**계기 (2026-10-30)**: 50 kg 4차년도 DEM 보고 문헌 지도 `docs/50kg/report_y4/lit_se_size_map_20261030.md` §6 이 **7순위** 로 올렸다 —
*"밀링 손상 없는 미립화 — p5 교란 분리 단서 (p5 · p2)"*.  p5 의 교란이란 *"작은 SE 의 펠릿 σ 가 낮은 것은 입도 탓인가, 밀링 공정 탓인가"* 이다.  원문 판정:

| Q | 판정 (한 줄) | 근거 |
|---|---|---|
| **Q1 재료** | **LPSCl 이 아니다** — Li₇P₃S₁₁ 유리-세라믹 (Li₂S–P₂S₅ 계). CAM 도 **LiNbO₃ 코팅 NCM111** (입도 미보고). 분리막 80Li₂S·20P₂S₅ 유리 | p. 474 |
| **Q2 입도** | 액상법 (LP) **≈500 nm** · 볼밀 (BM) **>10 µm** — **둘 다 SEM 영상 인상** (PSD 측정 없음) | p. 475 · `Fig. 2` |
| **Q3 밀링 없이 작게 만들었나** | **그렇다** — LP = 아세토나이트릴 중 초음파 (60 °C · 30 min) → 180 °C 진공 건조 → **220 °C · 1 h**. BM = 510 rpm · 10 h → 같은 220 °C · 1 h. 크기는 *"초음파 해응집 + 용매의 계면활성 작용"* 에서 온다 (저자) | p. 474–475 |
| **Q4 그래도 σ 가 낮은가** | **그렇다, 1.9 배** — LP **1.0** · BM **1.9 mS cm⁻¹** (실온 펠릿). 저자는 입도가 아니라 **국소구조 (LP = P₂S₇⁴⁻ 주, BM = PS₄³⁻ 주)** 를 원인으로 본다. LP 에는 **Li₂S 불순물** 피크 (2θ 27°) 도 있다 | p. 475 · `Fig. 1` · `Fig. 3` |
| **Q5 복합체 (79 wt%)** | 첫 방전 **LP 154 · BM 46 mAh g⁻¹ (×3.35)** · 30 사이클 유지 **81 · 87 %** · 30 사이클 뒤 양극 계면 저항 **R2 67 · 25 Ω** | p. 477–478 · `Fig. 5` · `Table 1` |

⇒ **p5 판정**: 이 논문은 밀링 손상을 **없앴지만 교란을 없애지는 못했다** — 밀링 대신 **합성 경로 (국소구조 · Li₂S · 잔류 유기물 가능성)** 가 크기와 함께 바뀐다.
그래도 *"작은 SE 의 펠릿 σ 가 1.9 배 낮은데 복합체 첫 방전은 3.35 배 높다"* 는 **구조 이득이 물성 손해를 압도하는 사례** 다 (용량 ≠ σ_eff 라는 한정어와 함께).
덤으로 **우리 설계에 가장 가까운 조건** 이다 — AM **79 wt%** (우리 85) · SE **≈0.5 µm** (우리 D0.7) · 성형 **360 MPa** (우리 300).  다른 것은 재료 (LPS · NCM111).

---

## 1. 한 줄 요약

같은 Li₇P₃S₁₁ 상을 **액상법 (초음파 · 220 °C)** 으로 만들면 ≈500 nm, **볼밀** 로 만들면 >10 µm 가 되는데, 펠릿 σ 는 1.0 vs 1.9 mS cm⁻¹ 로 같은 자릿수다.
이를 LiNbO₃-NCM111 : SE : VGCF = 79:19:2 wt% 복합양극에 넣으면 **작은 SE 쪽이 NCM 사이로 고르게 퍼져 (SEM-EDX) 첫 방전 154 vs 46 mAh g⁻¹** 을 낸다.
대신 작은 SE 쪽은 30 사이클 뒤 **양극 계면 저항이 더 크고 (67 vs 25 Ω) 유지율이 낮다 (81 vs 87 %)** — 저자는 잔류 유기물과 넓은 계면을 의심한다.
고전압 (4.5 · 4.6 V vs Li) 에서도 ex-situ Raman 상 Li₇P₃S₁₁ 구조 변화가 없어, 계면 저항 성장 (145 → 318 Ω) 은 NCM 부피 변화 탓으로 돌린다.

## 2. 메타 / 동기 / 질문

| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| **Marcela Calpa**, **Nataly Carolina Rosero-Navarro\***, Akira Miura, Kiyoharu Tadanaga (Hokkaido University) | *Electrochim. Acta* **296**, 473–480 (2019) · 접수 2018-08-20 · 개정 10-18 · 수락 11-06 · 온라인 11-09 | 10.1016/j.electacta.2018.11.035 | **Li₇P₃S₁₁** (LP ≈500 nm · BM >10 µm) + **LiNbO₃ 코팅 LiNi₁/₃Co₁/₃Mn₁/₃O₂** + VGCF 2 wt% · 분리막 80Li₂S·20P₂S₅ 유리 · 대극 In | 실험 (XRD · Raman · 펠릿 EIS · SEM-EDX · 반쪽셀 사이클 · EIS 적합) — **시뮬 없음** |

- **동기 (p. 473–474)**: VGCF ≈2 wt% 면 전자 경로는 충분하지만 이온 경로에는 SE 가 **≈60 wt%** 나 필요하다 (ref 8). PLD 코팅은 효과적이나 양산이 어렵다 (ref 11). 대안 = **작은 SE 입자** (ref 12 Sakuda 2016) — 그러나 볼밀 분쇄는 에너지 · 시간이 많이 든다. 저자들의 액상법은 순간적으로 작은 고전도 Li₇P₃S₁₁ 을 만든다 (refs 13–14, 1 × 10⁻³ S cm⁻¹ at 22 °C, ESW 5 V 까지).
- **질문**: 액상법 소립 Li₇P₃S₁₁ 을 이온 전도체로 쓴 복합양극이 볼밀 대립 Li₇P₃S₁₁ 보다 나은가, 그리고 고전압에서 SE 가 안정한가.
- **자금 (p. 479)**: JST ALCA · SPRING. 이해관계 선언 없음 (본문에 절 없음).

## 3. 핵심 수치 총정리 ★

### 3a. 재료 · 합성

| 항목 | LP (액상법) | BM (볼밀) | 표기 · 출처 |
|---|---|---|---|
| 원료 | Li₂S (Mitsuwa 99.9 %) · P₂S₅ (Aldrich 99 %) | 같음 | stated · p. 474 |
| 공정 | 무수 아세토나이트릴 (Wako) 중 혼합 → **초음파 60 °C · 30 min · 28 kHz** (Shimadzu SUS-103) → **180 °C · 3 h 진공 건조** → **220 °C · 1 h** | ZrO₂ 포트 45 mL · ZrO₂ 볼 4 mm × 500 · **510 rpm · 10 h** (유성) → **220 °C · 1 h** (*"LP 와 같은 온도 — 비슷한 σ 를 얻으려고"*) | stated · p. 474 |
| 조성비 | Li₇P₃S₁₁ (본문에 Li₂S : P₂S₅ 몰비 미기재 — 화학양론 70 : 30 은 우리 환산) | 같음 | 우리 산수 |
| 입도 | **≈500 nm** (*"irregular particles"*) | **>10 µm** | stated · SEM · p. 475 · `Fig. 2` |
| 입도 근거 | SEM 한 장씩 — PSD · BET 없음. LP 영상은 0.3–0.8 µm 단위가 **목 (neck) 으로 이어진 망** 처럼 보이고 (판독), BM 영상은 ≈35–40 µm 덩어리 하나 (판독, 10 µm 눈금) | | 판독 ≈ · `Fig. 2a,b` |
| XRD | Li₇P₃S₁₁ 주상 (ICSD 157654) + **Li₂S 피크 2θ = 27°** | Li₇P₃S₁₁ 주상 | stated · p. 474 · `Fig. 1a` |
| Raman 분해 | 약 401 cm⁻¹ 넓은 띠 = 420 (PS₄³⁻) + 401 (P₂S₇⁴⁻) + 385 (P₂S₆⁴⁻) cm⁻¹ · **P₂S₇⁴⁻ 가 주** | 같은 세 띠 · **PS₄³⁻ 가 주** | stated · p. 474–475 · `Fig. 1b,c` |
| 저자 해석 | P₂S₆⁴⁻ 는 결정화 뒤 비정질상에 남는 것으로 가정 (refs 18–19) · 국소구조 차이는 반응 · 결정화 기구 차이 | | stated · p. 475 |

### 3b. 순수 SE 펠릿

| 물성 | LP | BM | 조건 | 표기 · 출처 |
|---|---|---|---|---|
| σ (실온) | **1 × 10⁻³ S cm⁻¹** | **1.9 × 10⁻³ S cm⁻¹** | 분말 80 mg · ∅10 mm 폴리카보네이트 관 · **360 MPa** 실온 · SS 차단 · Solartron SI 1260 · 1 MHz–1 Hz · 30 mV · Z′ 절편 (선형 외삽) | stated · p. 474–475 |
| 스펙트럼 | 용량성 꼬리만 (SE–SS 계면) | 같음 | | stated · `Fig. 3` |
| 저주파 절편 | ≈115–117 Ω | ≈36–38 Ω | | 판독 ≈ (500 dpi) · `Fig. 3` |
| 저자 해석 | *"Young's moduli of about 20 GPa (ref 6) … room temperature pressure sintering, and therefore the resistance of pelletized sulfide solid electrolytes is not largely influenced by the particle size"* · BM 이 약간 높은 것은 PxSy 분포 차 | | | stated · p. 475 |

- ⚠ **우리 산수 — 절편 비와 σ 비가 맞지 않는다**: R_LP/R_BM ≈ **3.1–3.2** (판독) 인데 σ_BM/σ_LP = **1.9**. 같은 질량 (80 mg) · 같은 면적이면 σ ∝ L/R 이므로 **L_LP/L_BM ≈ 1.6–1.7** 이어야 한다 → LP 펠릿의 겉보기 밀도가 BM 의 **≈0.6 배** (A = 0.785 cm² 로 L ≈ σ·R·A: BM ≈0.054 cm · LP ≈0.090 cm). **두께 · 밀도는 논문에 없다** — 판독 의존 [추정].
  읽히는 방향: 작은 LP 분말이 360 MPa 에서 **덜 치밀** 하고, 그러면 1.0 mS cm⁻¹ 에는 기공 벌점이 들어 있어 *"국소구조 탓"* 의 몫이 그만큼 작을 수 있다.  (순수 SE 는 작을수록 덜 치밀할 수 있다는 `faka2026_particle_size_consolidation_strain_lpscl` 방향과 같다.)

### 3c. 복합양극 · 셀 (p. 474)

| 항목 | 값 | 표기 |
|---|---|---|
| 복합양극 | **LiNbO₃ 코팅 NCM111 : Li₇P₃S₁₁ : VGCF (Showa Denko) = 79 : 19 : 2 wt%** · *"simple mixture"* (혼합법 · 시간 미기재) | stated |
| CAM 입도 | **미기재** (refs 12 · 16 의 LiNbO₃ 코팅법 인용만) | — |
| 분리막 | 80Li₂S·20P₂S₅ (mol%) 유리 — 볼밀 510 rpm · 10 h · 80 mg | stated |
| 셀 | ∅10 mm 이층 펠릿 (복합양극 **10 mg** + 분리막 80 mg) **360 MPa 실온** → In 박 40 mg (0.1 mm) **240 MPa** 부착 · SS 봉 집전 · Ar 글러브박스 | stated |
| 사이클 | **정전류 0.13 mA cm⁻²** · 컷오프 **3.8 – 2 V** (vs Li–In; `Fig. 7` 범례 3.8 V = 4.4 V vs Li) · 실온 · Scribner 580 | stated · p. 474 · p. 477 |
| 셀 구속압 | **미기재** | — |
| 우리 산수 | NCM 면적 로딩 = 10 mg × 0.79 / 0.785 cm² = **10.06 mg cm⁻²** · LP 실현 용량 154 mAh g⁻¹ 기준 면적 용량 ≈1.55 mAh cm⁻² → 0.13 mA cm⁻² ≈ **C/12** | 우리 산수 |

### 3d. 전기화학 성능

| 항목 | LP (≈500 nm) | BM (>10 µm) | 표기 · 출처 |
|---|---|---|---|
| 첫 방전 | **154 mAh g⁻¹** | **46 mAh g⁻¹** | stated · p. 477 · `Fig. 5a` |
| 첫 충전 | ≈189 | ≈110 | 판독 ≈ · `Fig. 5a` |
| 첫 쿨롱효율 | ≈81 % (154/189) · 그림 첫 점 ≈80 % | ≈42 % · 그림 첫 점 ≈43 % | 판독 + 우리 산수 · `Fig. 5` |
| 쿨롱효율 99 % 넘는 시점 | 3 사이클 뒤 | 10 사이클 뒤 | stated · p. 477 |
| 30 사이클 유지 | **81 %** (30 사이클째 ≈124 mAh g⁻¹, 판독) | **87 %** (≈41, 판독) | stated · p. 477 · `Fig. 5b` |
| 방전 곡선 모양 | ≈3.1 V 중심의 긴 경사 → 150 mAh g⁻¹ 부근 급락 | **≈3.1 V 짧은 평탄 → ≈45 mAh g⁻¹ 에서 급락** | 판독 · `Fig. 5a` (§7b 해석) |
| 비 | 154 / 46 = **3.35** | | 우리 산수 |

### 3e. 셀 임피던스 (`Fig. 6` · `Table 1` — 단위 Ω, 본문 기준)

| 셀 | R1 (분리막, 1 MHz) | R2 (양극층, ≈1 kHz) | R3 (음극층, ≈1 Hz) |
|---|---|---|---|
| LP 충전 전 | 119.6 | — | — |
| LP 30 사이클 뒤 (충전 상태) | 119.6 | **67** | **46** |
| BM 충전 전 | 119.6 | — | — |
| BM 30 사이클 뒤 | 119.7 | **25** | **48** |

- 등가회로 (`Fig. 6c`): (R1‖CP1) – (R2‖CP2) – (R3‖CP3) – W_o. 중간 · 저주파 반원 배정은 ref 22 (Sakuda 2010).
- 저자 해석 (p. 478): R2 는 공간전하층 (ref 23) 또는 원소 상호확산 반응 (ref 22) 기원 · LiNbO₃ 코팅의 틈 (ref 16). **LP 쪽 R2 가 큰 이유 = 액상 합성의 잔류 유기 착물 가능성 (ref 25) + 더 넓은 CAM–SE 계면** (추정, 측정 없음).

### 3f. 고전압 시험 (LP 셀 · `Fig. 7`–`9` · `Table 2`)

| 항목 | 값 | 표기 · 출처 |
|---|---|---|
| 순서 | 30 사이클 (3.8–2 V) → **3.9–2 V (4.5 V vs Li) 10 사이클** → **4–2 V (4.6 V vs Li) 10 사이클** · 0.13 mA cm⁻² | stated · p. 478 |
| 방전 용량 | 30번째 ≈122 · 40번째 ≈102 · 50번째 ≈90 mAh g⁻¹ | 판독 ≈ · `Fig. 7a` |
| 쿨롱효율 | ≈99 % 유지 · 용량은 계속 감소 | stated · `Fig. 7b` |
| R1 / R2 / R3 (3.9 V 뒤) | 119.7 / **145** / 57 Ω | stated · `Table 2` |
| R1 / R2 / R3 (4 V 뒤) | 119.7 / **318** / 63 Ω | stated · `Table 2` |
| ex-situ Raman (50 사이클 뒤 양극층, 900 점 평균) | 405 (P₂S₇⁴⁻) · 420 (PS₄³⁻) cm⁻¹ 두 주 피크 · P₂S₆⁴⁻ 추가 생성 없음 (*"scarce presence"*) | stated · p. 479 · `Fig. 9` |
| 결론 | Li₇P₃S₁₁ 은 고전압 충방전에서 구조 변화 없음 → 계면 저항 성장은 **NCM 부피 변화** 탓 (refs 26–28) | stated · p. 479 |

### 3g. 우리 산수 모음
- 크기 비 (SEM 인상) ≥ 20 (>10 µm / ≈0.5 µm) · σ 비 BM/LP = **1.9** · 첫 방전 비 LP/BM = **3.35** · R2 비 (30 사이클) LP/BM = 2.7.
- 펠릿 함의 두께 비 L_LP/L_BM ≈ 1.6–1.7 (절편 판독 + σ stated · 같은 80 mg 가정) — §3b.
- 복합양극 SE 함량 = **19 wt%** (AM 79 wt%) — 세 편 (Lin 70 · Tron 67 · 이 논문 79 wt%) 중 우리 85 wt% 에 가장 가깝다.
- NCM 로딩 10.06 mg cm⁻² · 전류 ≈C/12 (§3c).

---

## 4. 재료 & 방법 — 같은 축을 흉내 낼 때 필요한 조건 ★
- **SE 합성**: §3a 표 그대로. 두 경로 모두 마지막 열처리 **220 °C · 1 h** (같은 온도로 맞춘 것이 이 비교의 설계).
- **분석**: XRD Rigaku MiniFlex 600 · 10–40° · 0.01° 스텝 / Raman HORIBA XploRA PLUS · 532 nm · 17 mW · Gaussian–Lorentzian 분해 / SEM JIB-4600F (SEM-FIB) · 대기 차단 이송 용기 / EIS Solartron SI 1260.
- **펠릿 σ**: 80 mg · ∅10 mm · 360 MPa · 실온 · SS 차단 · 1 MHz–1 Hz · 30 mV · 실축 절편 (선형 적합).
- **셀**: 79:19:2 wt% 복합양극 10 mg + 80Li₂S·20P₂S₅ 80 mg (360 MPa) + In 40 mg (240 MPa) · SS 봉 · 0.13 mA cm⁻² · 3.8–2 V (vs Li–In) · 고전압 시험은 3.9 · 4.0 V 컷오프.
- **셀 EIS 조건 (진폭 · 주파수 범위)**: 미기재 — 그림에 1 MHz · 1 kHz · 1 Hz 표지만.
- **빠진 것**: CAM 입도 · 혼합법 · 셀 구속압 · 반복 셀 수 · 펠릿 두께 · 복합체 기공 · 복합체 유효 σ.

## 5. 결과 — 섹션별 상세 (그림 실독 포함)

### 5.1 두 SE 는 같은 상, 다른 국소구조 · 다른 크기 (`Fig. 1`, `Fig. 2`, `Fig. 3`)
XRD 는 둘 다 Li₇P₃S₁₁ (LP 에 Li₂S 피크 하나 더). Raman 넓은 띠를 세 성분으로 풀면 LP 는 P₂S₇⁴⁻, BM 은 PS₄³⁻ 가 많다.
SEM 은 LP ≈500 nm · BM >10 µm — *"10 배 넘게 작다"*. 펠릿 σ 는 1.0 vs 1.9 mS cm⁻¹ 로 *"comparable high ionic conductivity over 10⁻³ S cm⁻¹"*.
저자의 논리: 황화물은 영률이 ≈20 GPa 로 낮아 실온 가압 소결이 되므로 **펠릿 저항이 입도에 크게 좌우되지 않는다** — 그래서 σ 차는 국소구조 차.

### 5.2 복합양극 단면 — 분포 (`Fig. 4`)
BM: NCM 덩어리와 **>20 µm SE 응집체** 가 따로 논다 (P · S 지도에 큰 밝은 섬, O · Mn 지도에 NCM 덩어리). *"SE 가 클수록 AM 함량이 높은 복합체에서 고르게 퍼뜨리기 어렵다."*
LP: SEM 영상만으로는 SE 를 못 가려내지만 EDX 상 **SE 가 NCM 입자 사이에** 있다 (P · S 신호가 잘게 흩어짐).

### 5.3 셀 성능 (`Fig. 5`)
첫 방전 LP 154 vs BM 46 mAh g⁻¹ — *"poor interfacial contact area … limited lithium ion-conductive pathways, which led to a deficient use of the active material"* (BM). 30 사이클 유지는 BM 이 오히려 높다 (87 vs 81 %).

### 5.4 계면 저항 (`Fig. 6`, `Table 1`)
분리막 저항 R1 ≈120 Ω 은 같고, 음극층 R3 (≈47 Ω) 도 같다 → 차이는 양극층. 30 사이클 뒤 **R2 = 67 (LP) vs 25 (BM) Ω** — 작은 SE 쪽이 계면 저항이 크다.

### 5.5 고전압 (`Fig. 7`–`9`, `Table 2`)
LP 셀을 4.5 · 4.6 V (vs Li) 까지 올리면 R2 가 145 → 318 Ω 으로 뛰고 용량이 준다. 양극층 Raman 은 P₂S₇⁴⁻ · PS₄³⁻ 그대로 (P₂S₆⁴⁻ 추가 생성 없음) → *"SE 는 안정, 저항 성장은 NCM 부피 변화"*.

### 5.6 결론 (p. 479–480, stated)
*"the particle size of the solid electrolyte largely influences the morphology of the composite cathode"* · *"the use of small-sized solid electrolytes is effective to obtain favorable lithium ion pathways in the composite cathode electrode"* · *"Li₇P₃S₁₁ is stable against charge-discharge measurements."*

## 6. 우선 질문 — 50 kg 4차년도 보고 쪽 (p1–p7) 기준 원문 대조

| 쪽 | 묻는 것 | 이 논문이 주는 것 | 못 주는 것 |
|---|---|---|---|
| p1 비교 틀 | 입도 · D_AM/D_SE | ≈0.5 vs >10 µm (SEM) — **우리 D0.7 에 가장 가까운 실측 SE** | PSD · CAM 입도 → λ 불가 |
| p2 공간 점유 · 압밀 | 기공 | (복합체 기공 없음) · 순수 SE 펠릿이 작은 쪽에서 덜 치밀할 가능성 [추정, §3b] | 복합체 기공 · 밀도 |
| p3 접촉 · 피복 | 분포 | SEM-EDX: LP = SE 가 NCM 사이 · BM = SE 응집체 >20 µm (정성) | 피복률 · 접촉 수 |
| p4 연결성 · 병목 | 이온 경로 | BM 방전 곡선의 *"짧은 평탄 → 급락"* = 도달 가능한 AM 몫이 제한된 모양 (우리 해석) | σ_eff · tortuosity |
| p5 구조 ↔ 물성 분리 | 펠릿 σ 손해 | **밀링 없이도 작은 SE 의 펠릿 σ 1.9 배 낮음** (합성 경로) · 그래도 복합체 첫 방전 3.35 배 | 같은 경로 · 다른 크기 대조군 · σ_eff |
| p6 두께 방향 | — | 없음 | — |
| p7 경향 · 다음 검증 | 방향 · 대가 | 작은 SE → 첫 방전 ×3.35 (79 wt% AM) · **대가: R2 ↑ (67 vs 25 Ω) · 유지 ↓ (81 vs 87 %)** | 율 · 다입도 · 반복 |

## 7. 우리 DEM+MPM 대비 ★ (근거 = 작업 브랜치 CLAUDE.md · `docs/50kg/report_y4/storyline_draft1.md` · `lit_se_size_map_20261030.md`)

### 7a. 항목별 대조

| 항목 | 이 논문 | 우리 (50 kg 4차년도 DEM) | 차이 / 이유 |
|---|---|---|---|
| SE 재료 | **Li₇P₃S₁₁ 유리-세라믹** (LP · BM) | LPSCl (DEM 유효 E 1.35 GPa · 물성 22 GPa) | 재료 다름 — 저자 인용 영률 ≈20 GPa (황화물 일반, ref 6) 는 우리 물성 22 GPa 와 같은 자릿수일 뿐, 값 이식 금지 |
| SE 입도 | ≈0.5 µm · >10 µm (SEM) | 0.7 · 1 · 2 · 3 µm 단분산 구 | LP 는 **D0.7 대역** · BM 은 D3 바깥 — 사이 입도 없음 (두 점 비교) |
| SE 형태 | LP = 목으로 이어진 불규칙 소립 망 · BM = 융합된 큰 덩어리 (판독) | 구 | 형상 · 응집 효과가 크기와 섞인다 (응집하면 이득이 준다 — `otani2025_dem_se_dispersion_aggregation_compression`) |
| CAM | LiNbO₃-NCM111 (입도 미보고) | NCM D6 µm | λ 불가 |
| 조성 | **79 : 19 : 2 wt%** (VGCF 포함) | **85 wt%** AM · 탄소 없음 | 세 편 중 우리에 가장 가깝다 |
| 압력 | 성형 360 MPa (In 240 MPa) · 구속압 미기재 | 300 MPa 목표 · 가압 상태 | 같은 자릿수 |
| 순수 SE σ | 1.0 (LP) · 1.9 (BM) mS cm⁻¹ | σ₀ = 입력 (보고에서는 f 로 나눔) | p5 펠릿 σ 비 목록에 **합성 경로형 1.9** 추가 (밀링형과 다른 부류로 표지) |
| 복합체 수송 | 측정 없음 (용량 · EIS 만) | f · 수송 tortuosity (tau2) · 연결성 · 협착 몫 | 우리 망 지표의 실험 짝이 이 논문에는 없다 |
| 분포 영상 | SEM-EDX 정성 | 단면 · 피복 지도 (기하 캡) | 같은 질문 (작은 SE 가 AM 사이로 들어가나) 의 정성판 · 정량판 |

### 7b. 50 kg 4차년도 보고 쪽 대응 (문헌 지도에 넣을 문장 후보)
- **p5 (주 자리)**: 지도 §6 의 *"밀링 손상 없는 미립화 — p5 교란 분리 단서"* 는 **절반만 맞다**. 밀링 손상은 없지만 **합성 경로 · 국소구조 · Li₂S 불순물 · (아마) 펠릿 밀도** 가 크기와 함께 바뀌어, 작은 SE 의 펠릿 σ 가 여전히 **1.9 배** 낮다. ⇒ 덱 각주 문장 후보: *"밀링을 피한 미립 SE (액상법, Li₇P₃S₁₁) 에서도 펠릿 σ 는 0.5 배 수준이었다 — 펠릿 σ 의 입도 의존은 공정 · 국소구조와 분리되지 않는다 (Calpa 2019)"*. 그리고 *"복합체 (79 wt%) 첫 방전은 3.35 배 높았다 — 구조 이득이 펠릿 σ 손해보다 컸던 사례 (단 용량 ≠ σ_eff)"*.
- **p4 (연결성)**: BM 셀의 방전 곡선은 **분극이 크게 다르지 않은 채 (평탄 ≈3.1 V, LP 와 비슷) 용량만 46 에서 끊긴다** (판독). 이것은 *"이온 망과 이어진 AM 만 일하고 나머지는 경로가 없다"* 는 모양과 맞는다 — 우리 `calc_ionic_active_am` 이 내는 **"SE 관통망과 경로 없는 AM" 몫** 의 실험 쪽 서명 후보. ⚠ 낱말: *"활성 AM"* · *"SE 이용률"* 금지 (`KG50B-01`) — *"연결성 기준"* 으로만. ⚠ 우리 해석이고 저자 주장은 *"limited lithium ion-conductive pathways … deficient use of the active material"* 까지다.
- **p3**: EDX 지도 = *"작은 SE 가 NCM 사이로 들어간다"* 의 정성 근거. 우리 피복 지도와 같은 양이라고 하지 않는다.
- **p2**: 순수 SE 펠릿의 밀도 함의는 [추정] — 덱에는 쓰지 않고, *"순수 SE 는 작을수록 덜 치밀할 수 있다 (faka2026)"* 의 보조 단서로만.
- **p7 (문헌 방향 열)**: "작은 SE → 첫 방전 ↑ (×3.35, 79 wt%)" + **"대가: 양극 계면 저항 ↑ · 유지 ↓"** — 문헌 지도 §2 의 반례 · 단서 줄에 *"작은 SE 는 계면이 넓어 계면 열화도 크다"* 를 더할 수 있다 (저자 추정 기반).
- **p1**: *"우리 D0.7 대역의 실측 복합양극은 이 논문 (LPS) 이 가장 가깝고, LPSCl 로는 세 편 중 없다"* — 문헌 공백 한정어.

### 7c. 문헌 지도 속 위치
- 지도 §1 표에 넣을 행 (안): `calpa2019_small_li7p3s11_liquid_phase_composite_cathode` | Li₇P₃S₁₁ (LPSCl 아님) 액상법 ≈0.5 µm vs 볼밀 >10 µm (SEM) | LiNbO₃-NCM111 (입도 미보고) · 79:19:2 wt% | 펠릿 σ 1.0 vs 1.9 mS/cm (360 MPa) · Raman 국소구조 차 · SEM-EDX 분포 · 첫 방전 154 vs 46 mAh/g · 30 사이클 81 vs 87 % · R2 67 vs 25 Ω | 분포 · 연결성 (AM 경로 유무) | 용량 · 계면 화학 · 펠릿 σ.
- §2 빈도: T1 (SEM ✓ · PSD ✗) · T2 (✓) · T3 (✗) · T4 (SEM-EDX ✓) · T5 (정성) · T6–T8 (✗) · T9 (곡선 모양 단서) · T10 (✓) · T11 (✗) · T14 (Raman 국소구조 ✓ — 밀링 아님).
- **교차 카드 주의**: 정본 `du2022_lmro_lpscl_reversible_redox_assb` §3g 가 옮긴 Du 2022 의 `Table S1` 행 *"LiNi₁/₃Co₁/₃Mn₁/₃O₂ | Li₇P₃S₁₁ | 2.6–4.4 | 154 | 580 | 87 (0.1C 30) | Calpa 2019"* 은 **원문과 짝이 어긋난다** — 154 mAh g⁻¹ 은 LP 셀, **87 % 는 BM 셀 (46 mAh g⁻¹) 의 유지율** 이고 LP 셀은 **81 %**. 전류도 0.13 mA cm⁻² 로 C-율 표기가 원문에 없다. (그 카드는 Du 의 표를 충실히 옮겼을 뿐 — 원 표의 인용 오류.)

### 7d. frame [4]/[5] 판정
- **frame [5]**: 이 논문은 **실험 (전기화학 · 정성 영상)** 만 갖고 미세구조 → 수송 사슬은 말로만 잇는다. 우리 DEM 이 줄 수 있는 것 = 같은 조성 (≈80–85 wt%) · 같은 크기 대비 (0.7 µm vs 3 µm) 에서 **AM 이 이온 망에 이어지는 몫 · f · 협착 몫** — 이 논문의 *"deficient use of the active material"* 를 숫자로 만드는 쪽. SE 형상 (목으로 이어진 소립 망 · 융합 덩어리) 은 우리 구 DEM 에 없다.
- **frame [4]**: 값 이식 금지 (Li₇P₃S₁₁ ≠ LPSCl · NCM111 ≠ NCM811 · 두 점 · 반복 없음). 쓸 수 있는 것 = **방향 (작은 SE → 이득) + 펠릿 σ 비의 문헌 범위 (합성 경로형)**.
- 이전 가능성 경계: 재료가 다르므로 **"같은 재료에서 밀링 없는 미립화"** 의 증거로는 쓸 수 없다. *"같은 상을 다른 경로로 작게 만들면"* 의 증거다.

---

## 8. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | (a) XRD — LP · BM · ICSD 157654 · LP 의 Li₂S 피크 (*) · (b,c) Raman 분해 (PS₄³⁻ · P₂S₇⁴⁻ · P₂S₆⁴⁻) | 크기와 함께 바뀌는 국소구조 = p5 교란의 실체 |
| 2 | (a) LP SEM (1 µm 눈금, ≈500 nm 불규칙 소립 · 목 연결) · (b) BM SEM (10 µm 눈금, 큰 덩어리) | ★ 입도 근거의 전부 (PSD 없음) — 우리 D0.7 대역 실물 예 |
| 3 | 펠릿 Nyquist — LP (보라 원) · BM (파랑 사각), 용량성 꼬리 | σ 1.0 vs 1.9 의 원자료 · 절편 비 ≈3.1 (§3b 밀도 함의) |
| 4 | 복합양극 단면 SEM + EDX (O · P · Mn · S) — (a) BM · (b) LP (5 µm 눈금) | ★ 작은 SE 가 NCM 사이로 들어가는 정성 그림 (p3) |
| 5 | (a) 첫 충방전 (0.13 mA cm⁻², mAh g⁻¹_NCM) · (b) 30 사이클 방전 용량 + 쿨롱효율 | ★ 154 vs 46 · BM 곡선의 *"평탄 → 급락"* 모양 (p4 연결성 서명 후보) |
| 6 | Nyquist (충전 전 · 30 사이클 뒤) — (a) LP · (b) BM · (c) 등가회로 (R1‖CP1)(R2‖CP2)(R3‖CP3)W_o | 양극 계면 저항 R2 — 작은 SE 의 대가 |
| 7 | (a) 30 · 40 · 50 번째 방전 (3.8 · 3.9 · 4.0 V 컷오프) · (b) 31–50 사이클 용량 · 쿨롱효율 | 고전압 열화 (우리 범위 밖) |
| 8 | 40 · 50 번째 충전 뒤 Nyquist (3.9 · 4.0 V) — R2 145 · 318 Ω | 같은 |
| 9 | 양극층 Raman 분해 — (a) as-prepared · (b) 50 사이클 뒤 (4 V) | SE 안정성 근거 (§10-7) |
| Table 1 | R1 · R2 · R3 (LP · BM × 충전 전 · 30 사이클 뒤) | ★ R2 67 vs 25 Ω |
| Table 2 | R1 · R2 · R3 (LP, 3.9 · 4 V 컷오프 뒤) | R2 145 · 318 Ω |

## 9. Post-processing ★
- **XRD**: 상 동정만 (ICSD 대조) · 정량 없음.
- **Raman**: Gaussian–Lorentzian 세 성분 분해 (420 · 401 · 385 cm⁻¹) → 주 성분 판정 (면적비 수치 미기재) · 사이클 뒤 900 점 평균 스펙트럼 분해.
- **펠릿 σ**: Nyquist 실축 절편 (선형 적합) → σ (두께 미기재).
- **셀 EIS**: 등가회로 적합 (`Fig. 6c`) → R1 · R2 · R3 표 (`Table 1`–`2`) · 반원 정점 주파수 (1 MHz · 1 kHz · 1 Hz) 로 층 배정.
- **성능**: mAh g⁻¹_NCM · 쿨롱효율 % · 30 사이클 유지 % · 반복 셀 수 미기재 (오차 막대 없음).

## 10. 비판 / 주의 / 한계 ★ (over-claim 방지)

1. **재료가 LPSCl 이 아니다** — Li₇P₃S₁₁ 유리-세라믹 (+ LiNbO₃-NCM111 · 80Li₂S·20P₂S₅ 분리막). 우리 LPSCl/NCM811 로 수치 이식 불가, 방향만.
2. **입도는 SEM 한 장씩의 인상** — PSD · BET · 반복 영상 없음. LP 는 목으로 이어진 소립 망 (판독) 이라 *"500 nm 입자"* 가 실제로는 더 큰 응집 단위일 수 있다.
3. **크기와 합성 경로가 함께 바뀐다** — 국소구조 (P₂S₇⁴⁻ 주 vs PS₄³⁻ 주) · Li₂S 불순물 (LP) · 잔류 유기물 가능성 (저자 언급). *"작은 SE 가 좋다"* 가 아니라 *"이 액상법 SE 가 이 볼밀 SE 보다 좋았다"* 가 원문이 받치는 문장.
4. **펠릿 σ 와 절편의 불일치** (§3b): 절편 비 ≈3.1 vs σ 비 1.9 → 두께 · 밀도가 달랐을 것 [추정]. σ 차의 원인을 *"국소구조"* 로만 돌리기 어렵다. 두께 · 밀도 미보고.
5. **복합체 수송을 재지 않았다** — 기공 · σ_eff · tortuosity 없음. *"이온 경로가 좋아졌다"* 는 EDX 정성 + 용량에서의 추론.
6. **반복 · 오차 없음** — 셀 한 개씩 · 30 사이클. 첫 쿨롱효율 (LP ≈81 · BM ≈42 %, 판독) 의 큰 차이도 해석 없이 지나간다.
7. **Raman 적합의 일관성**: 분말 LP (`Fig. 1b`) 에는 P₂S₆⁴⁻ 성분이 뚜렷이 적합되는데 복합체 as-prepared (`Fig. 9a`) 에서는 0 으로 적합된다 (우리 판독). *"P₂S₆⁴⁻ 추가 생성 없음"* 결론이 적합 선택에 기대고 있다.
8. **본문 그림 참조 오기**: LP 복합체 SEM 을 *"(Fig. 4a)"* 로 적는다 (캡션상 LP = 4b).
9. **CAM 입도 · 혼합법 · 셀 구속압 · 셀 EIS 조건 미기재** → λ · 압력 축에 못 올린다.
10. **R2 해석은 추정** — 잔류 유기물 · 넓은 계면 둘 다 측정 없음 (XPS · 잔류 탄소 분석 없음).
11. **인용 연쇄 주의**: Du 2022 `Table S1` 의 Calpa 행 (154 · 87 %) 은 두 셀의 값을 섞었다 (§7c).

## 11. 적용 인사이트
- ① **p5 의 펠릿 σ 비를 "밀링형" 과 "경로형" 으로 나눠 적자**: LIN 3.28 · CRO 1.45 … (밀링) 와 CALPA 1.9 (액상법 vs 볼밀) 는 다른 기전이다. 손익분기선 2.217 의 *"현실 범위"* 를 말할 때 둘을 섞지 않는다.
- ② **D0.7 대역 실측 앵커의 공백**: 우리 D0.7 에 크기로 가장 가까운 복합양극 실측이 LPS · NCM111 계 (이 논문) 다 — LPSCl 로는 세 편 (Lin · Calpa · Tron) 안에 없다. 덱에서 *"D0.7 은 문헌 실측이 드문 대역"* 이라는 한정어 근거.
- ③ **연결성 서명**: *"분극은 비슷한데 용량이 끊긴다"* 는 곡선 모양은 우리 연결성 지표 (SE 관통망과 경로 없는 AM) 로 설명 가능한 종류 — 다음 3D 전기화학 (p7 ②) 에서 같은 모양이 나오는지 볼 대조 그림 후보.
- ④ **미립화의 대가**: 계면이 넓어지면 계면 저항 · 열화도 커질 수 있다 (R2 67 vs 25 Ω) — 우리 보고의 *"관측된 경향"* 표에 *"계산 / 모형 한계"* 칸으로 (DEM 은 계면 화학을 모른다).

## 12. 인용 가능 문장 (영문 초안)
- *"Li₇P₃S₁₁ synthesized by a liquid-phase route (≈500 nm, SEM) gave a lower pellet conductivity than ball-milled Li₇P₃S₁₁ (>10 µm; 1.0 vs 1.9 mS cm⁻¹ at room temperature), yet as the ionic conductor in LiNbO₃-coated NCM111 composite cathodes (79:19:2 wt%) it delivered a 3.35-fold higher first discharge capacity (154 vs 46 mAh g⁻¹) [Calpa 2019]."*
- *"The smaller electrolyte also produced a larger positive-electrode interfacial resistance after 30 cycles (67 vs 25 Ω) and a lower capacity retention (81 vs 87 %) [Calpa 2019, Table 1]."*
- ⚠ *"without milling damage"* 로 소개하지 말 것 — 합성 경로가 다르다고 함께 적는다.

## 13. 기법 용어 미니사전
- **액상법 (liquid-phase synthesis)**: 원료를 유기 용매 (여기선 아세토나이트릴) 에 섞어 반응 · 건조 · 저온 열처리하는 합성. 볼밀 없이 작은 입자를 얻지만 잔류 유기물 · 불순물 상이 남을 수 있다.
- **Li₇P₃S₁₁ (70Li₂S·30P₂S₅ 유리-세라믹)**: 결정상 Li₇P₃S₁₁ 은 PS₄³⁻ 와 P₂S₇⁴⁻ 단위로 이뤄지고, 비정질 쪽에 P₂S₆⁴⁻ 가 남기도 한다.
- **PS₄³⁻ / P₂S₇⁴⁻ / P₂S₆⁴⁻**: 오르토 · 피로 · 하이포 티오인산 단위 (Raman ≈420 · 401 · 385 cm⁻¹).
- **LiNbO₃ 코팅**: NCM 과 황화물 SE 사이의 계면 반응 · 공간전하층을 줄이는 산화물 완충층.
- **R1 / R2 / R3**: 이 논문의 셀 EIS 배정 — 분리막 (고주파) / 양극층 계면 (≈1 kHz) / 음극층 (≈1 Hz).
- **CP**: 원문의 상수위상요소 표기 (CPE 와 같은 것).
- **W_o**: 개방 경계 Warburg (유한 확산) 요소.
- **0.13 mA cm⁻² ≈ C/12**: 이 카드의 우리 환산 (원문은 C-율을 적지 않는다).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
