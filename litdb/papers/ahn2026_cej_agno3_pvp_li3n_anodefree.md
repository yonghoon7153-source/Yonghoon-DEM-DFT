# Electrochemical precursor conversion for coupled control of Li nucleation and transport in anode-free all-solid-state batteries — Kim, Kang, Lee, Shin, **An**, Lee (Chem. Eng. J., 투고본 2026)

> slug `ahn2026_cej_agno3_pvp_li3n_anodefree` · DOI `n/a (미출판 투고본)` · type `exp + 연속체모델 + DFT` · source `Manuscript_CEJ.docx / Supplementary_Material_CEJ.docx / Highlights_CEJ.docx / Graphical_Abstract_CEJ.docx (2026-09-07 업로드)` · digested `2026-09-07` · status ✅
> **저자**: Dongseok Kim^a‡, Junhee Kang^a‡, Tae Young Lee^a‡, Hong Rim Shin^a, **Yonghoon An**^b, Jong-Won Lee^a,c\* (^a Hanyang Univ. MSE · ^b SK On Next Generation Battery R&D center · ^c Hanyang Univ. Battery Engineering) · 교신 jongwonlee@hanyang.ac.kr
> elements: Li, C, N, O, P, S, Cl, Ni, Co, Al, Ag
> methods: DFT, NEB, MLIP, XPS, Raman

---

## 🔴 배너 — 이건 외부 문헌이 아니라 **우리 원고다**

**통상의 "문헌 소환값" 규율이 적용되지 않는다.** Fig. 5c–e / Table S2 의 DFT 수치는
`db/properties/diffusion.json` · `db/properties/li3n_barrier_origin.csv` · `db/properties/li3n_barrier_fig_origin.csv`
에 있는 **우리 정본과 같은 계보**다. 그래서 §11 은 "그들 vs 우리" 비교가 아니라 **자기감사표**다.

### 감사 결과 요약 — 🔴 P0 2건 · 🟠 P1 4건 · 🟡 P2 6건 · ✅ 금지규율 위반 0건

| | 항목 | 어디 |
|---|---|---|
| 🔴 **P0-1** | **Fig. 5d 가 Li₃N 을 실선 연속 MEP 로 그리고, 캡션에서 "guide to the eye" 문장이 빠졌다.** 실제로 계산한 Li₃N 점은 **2개**뿐이고, 그 곡선은 kb 가 *폐기한* mirrored-spline NEB 모양에 진폭만 갈아끼운 것 — **확정(확정 status) 내부 결정을 어긴 상태로 제출됐다** | §11-A1 |
| 🔴 **P0-2** | **Methods §4.6 이 LiC₆ 를 "UMA-oc20 CI-NEB" 로만 기술하고 QE DFT 단일점 단계를 빠뜨렸다.** 그 경로만으로 나오는 우리 값은 **0.241 eV** 이지 0.290 이 아니다. 그 결과 Table S2 (QE 파라미터를 두 열에 병합) 와 §4.6 이 서로 다른 말을 한다 | §11-A2 |
| 🟠 P1-1 | 보고된 LiC₆ **0.290 eV 는 계산된 이미지가 아니라 스플라인 최대값**(xi=0.41). 실제 최고 계산점은 img3 = **0.2866 eV** | §11-A3 |
| 🟠 P1-2 | 우리 db 안에서 LiC₆ 값이 **0.287**(`diffusion.json`) vs **0.28968**(`li3n_barrier_origin.csv`) 로 갈라져 있다 | §11-A3 |
| 🟠 P1-3 | Fig. 3a 패널에 **0.1C**, Methods §4.5·Fig. 3e 캡션에는 **0.5C** | §11-B1 |
| 🟠 P1-4 | Abstract 는 "**18.8% higher** capacity retention", Conclusion 은 "**18.8 percentage points**" — 같은 수의 단위가 다르다 (실제로는 54.2−35.4 = %p) | §11-B2 |
| 🟡 P2-1..6 | 저자 byline 의 `~~` 잔재 + `b` 중복 · Eq.(2)→Fig. 3d 재현 불가(변환계수 미기재) · Fig. 2b/S6 배율 불일치 · Fig. S6 축라벨 "Ag" vs 본문 "AgNO₃" · Fig. 5e 그림 vs 본문 라벨(C–N vs pyrrolidone N) · 0.118/0.290 이 `canonical_registry.json` 미등록 | §11-C |

**✅ 금지규율 전수검사는 통과했다** — 특히 최우선 확인 항목이던 **"UMA 를 Li₃N 에 쓰지 말 것"(2026-06)** 은
**지켜졌다**: 원고의 Li₃N 0.118 eV 는 **Quantum ESPRESSO 두 점 구속이완**(DFT)이다. 상세는 §12.

---

## 0. 이 digest 를 읽는 법

- 이 논문은 **세 갈래**다: ① 실험(전구체 분산·전환·셀), ② 1D 전기화학–크리프 **연속체 모델**(Fig. 3),
  ③ **DFT** Li adatom 확산(Fig. 5c–e). 우리(계산) 기여는 ③ 이고, ②는 저자 측 별도 모델이다.
- **②와 ③은 서로 연결돼 있지 않다.** 크리프 모델에 Li₃N 이 안 들어가고, DFT 장벽이 모델 입력으로 안 쓰인다.
  Fig. 8 이 둘을 한 그림에서 묶지만 그건 **서술적 종합**이지 계산된 결합이 아니다 (§15).
- 그림에서만 읽은 값은 **`figure-read ≈`** 로 표시했다. 본문에 명시된 값과 구분된다.
- **실제로 본 그림 9장** (Fig. 2·3·4·5·6·7·8 · Fig. S6 · Fig. S8). **안 본 그림 15장** (Fig. 1 · S1–S5 · S7 · S9–S15 · GA). §9 에 표시.

---

## 1. 한 줄 요약

Ag 입자를 물리혼합하는 대신 **AgNO₃ 전구체 + PVP** 를 카본에 섞어 캐스팅하면, PVP 카보닐–Ag⁺ 배위가
건조 중 전구체 이동·결정화를 막아 **AgNO₃ 도메인이 53.4 → 7.82 nm 로 미세화**되고, 첫 충전 때 그 도메인이
**in-situ 전기화학 전환**되어 ① 고르게 퍼진 Ag–Li 합금 핵생성 자리와 ② **Li₃N 계면상**을 동시에 만든다 —
그 결과 NCA anode-free 풀셀이 **350 사이클**(대조군 Ag–C 는 174 사이클에서 단락) 간다.

---

## 2. 메타 / 동기

| 항목 | 내용 |
|---|---|
| 저널 | Chemical Engineering Journal (**투고본, DOI 없음**) |
| 계 | anode-free ASSB: **NCA ‖ LPSCl ‖ interlayer/SUS** |
| 계면층 3종 | `Ag–C` (물리혼합, 기준) · `AgNO₃–C` (전구체, PVP 없음) · `AgNO₃–C–PVP` (전구체 + PVP) |
| Ag 함량 | **25 wt%** 와 **15 wt%** (Ag + carbon black 합 기준) |
| 문제의식 | Ag–C 물리혼합은 슬러리 건조 중 Ag 가 표면에너지를 낮추려 **응집** → Ag-rich 국소 → Li flux 편중 → 계면 열화 |
| 해법 | 전구체를 **셀 작동 시점까지 남겨두고**(retained precursor) 전기화학적으로 전환 → 분산 제어 + 계면화학 제어를 **동시에** |

---

## 3. 핵심 수치 총정리

### 3.1 재료·구조
| 물성 | 값 | 어디 |
|---|---|---|
| AgNO₃ 도메인 지름 (PVP 없음) | **53.4 ± 58.6 nm** (SD > mean → 이봉분포) | Fig. S6 |
| AgNO₃ 도메인 지름 (PVP) | **7.82 ± 2.61 nm** | Fig. S6 |
| 원료 Ag 입자 D50 | 60 nm (US Research Nanomaterials) | Methods 4.1 |
| FT-IR C=O 스트레치 이동 | **1652.2 → 1617.5 cm⁻¹** (적색이동 = Ag⁺ 배위) | Fig. S5 |
| FT-IR C–N 이동 | 1285.3 → 1295.5 cm⁻¹ | Fig. S5 |
| Raman I_D/I_G | Ag–C **1.21** · AgNO₃–C **1.14** · AgNO₃–C–PVP **1.16** | Fig. 2d |
| PVP 첨가량 | AgNO₃ 중 Ag 질량 대비 **1 wt%** | Methods 4.1 |

### 3.2 셀 전기화학
| 물성 | Ag–C 25 | AgNO₃–C 25 | AgNO₃–C–PVP 25 | 어디 |
|---|---|---|---|---|
| η_nucleation | **10.1 mV** | **9.2 mV** | **7.2 mV** | Fig. 6f |
| Q_lithiation | **0.38** mAh cm⁻² | **0.68** | **0.58** | Fig. 6f |
| CCD @ 60 °C | 0.6 mA cm⁻² | 1.5 | **≥2.0**(시험 상한) | Fig. 6g |
| CCD @ 45 °C | 0.3 mA cm⁻² | 1.1 | **≥2.0**(시험 상한) | Fig. 6h |
| ΔP (operando) | **3.0 MPa** | **2.8** | **2.5** | Fig. 7b |
| 수명 @0.2C 45 °C | 174 cy 단락 (~75 cy 부터 CE 요동) | 125 cy 종료 | **350 cy 유지** | Fig. 7d |

### 3.3 15 wt% (저-Ag) 비교 — 이 논문의 진짜 주장
| | AgNO₃–C 15 | AgNO₃–C–PVP 15 |
|---|---|---|
| 300 cy 방전용량 | **64.1 mAh g⁻¹** | **102.2 mAh g⁻¹** |
| 300 cy 용량유지율 | **35.4 %** | **54.2 %** |
| 차이 | — | **+18.8 %p** (Abstract 은 "18.8%" 로 씀 → §11-B2) |

### 3.4 DFT (우리 기여)
| 물성 | 값 | 방법 | 어디 |
|---|---|---|---|
| Li adatom 흡착E, 최소점 | **−2.988 eV** | QE 구속이완 | Fig. 5c |
| Li adatom 흡착E, 안장영역 | **−2.870 eV** | QE 구속이완 | Fig. 5c |
| **Li₃N (001) 확산장벽** | **0.118 eV** | 두 점 구속이완 (DFT) | Fig. 5e, Table S2 |
| **LiC₆ (0001) 확산장벽** | **0.290 eV** | CI-NEB(UMA-oc20) **+ QE 단일점** ← §4.6 이 뒷단을 안 씀 | Fig. 5e, Table S2 |
| 감소율 | **≈59 %** (비율 2.46×) | | Results |

---

## 4. 재료 & 실험 방법

**계면층 제작 (4.1)** — 슬러리 캐스팅. Ag 입자(D50 60 nm) 또는 AgNO₃ + carbon black(DENKA BLACK)
을 NMP + **PVDF 바인더 5 wt%** 에 분산. AgNO₃ 계는 **Ag 분율 기준으로 환산**해 같은 Ag 함량을 맞춤.
PVP 는 AgNO₃ 속 Ag 질량 대비 1 wt%. 유성 원심 믹서(Thinky ARE-310) → **10 µm SUS 포일** 캐스팅 →
공기 60 °C 2 h → **진공 120 °C 12 h**.

**셀 (4.2)** — NCA(다결정) : LPSCl(POSCO JK Solid Solution) : CNF : PTFE = **85 : 15 : 3 : 1.5**,
탈수 자일렌, **건식 필름 공정**, NCA 로딩 **24.5 mg cm⁻²**. PEEK 몰드 내경 **13 mm**.
LPSCl 분말 **0.15 g → 50 MPa** 로 SE 층 성형 → 계면층/SUS 한쪽, 캐소드 시트 반대쪽 → 전체 **400 MPa** 가압.
운전 **스택압 20 MPa**. 반쪽셀은 Li 포일 ‖ LPSCl ‖ 계면층. 전부 Ar 글로브박스.

> 정합성 체크: Fig. 7a 인디케이터 **240 kg** / 13 mm 다이 면적 1.327 cm² → **≈17.7 MPa**.
> 본문 20 MPa 와 같은 자리수 ✓ (도식은 대표값으로 보인다).

**분석 (4.3)** — SEM-EDS(Verios G4UC) · XRD(D8 ADVANCE, Cu Kα 1.541 Å, **2° min⁻¹**) ·
Raman(DXR3xi) · XPS(PHI-GENESIS) · FT-IR(Nicolet iS50) · HAADF-STEM(JEM-2100F) · 단면 FIB(Helios).

**전기화학 (4.4)** — GITT: **1 mA cm⁻² 1 min 펄스 + 1 h 완화**. EIS: **7 MHz–10 mHz, 5 mV**, DRT 해석.
핵생성: 0.1C 로 **4.5 mAh cm⁻²** 까지. CCD: **5 mAh cm⁻² 예비증착** 후 0.1 mA cm⁻² 부터 **1 h 마다 +0.1**.
Operando 압력: 로드셀 분해능 **0.01 MPa**. 사이클: 45 °C, **2.5–4.25 V**, 초기 0.1C CC–CV(컷오프 = CC 전류의 50%),
이후 **0.2C**.

---

## 5. 결과 — 절별 상세

### 5.1 물리혼합의 한계 (Fig. 1)
슬러리 건조 중 Ag 응집 → 카본 매트릭스 안에 Ag-rich 영역. Ag–C 25 는 SEM/Ag 맵에서
**마이크로미터 스케일 Ag-rich 영역**이 뚜렷 (Fig. 1c). 필름 자체는 육안상 균일 (Fig. S2) —
즉 **거시적 균일 ≠ 미시적 균일**.

### 5.2 PVP 배위로 전구체 분산 (Fig. 2a,b · Fig. S5, S6)
- AgNO₃ 는 NMP 에 녹아 Ag⁺ 가 슬러리 전체에 고르게 퍼지지만, **용매 증발 중 이동·재결정**한다 →
  배위제가 필요. PVP 의 **카보닐 산소**가 Ag⁺ 와 배위 (FT-IR 1652.2 → 1617.5 cm⁻¹ 적색이동).
- SEM/EDS: AgNO₃–C 25 는 Ag-rich 국소, AgNO₃–C–PVP 25 는 균일 (Fig. 2a). 15 wt% 도 동일 (Fig. S4).
- HAADF-STEM: 큰 불규칙 밝은 도메인 → 미세·균일 도메인 (Fig. 2b).
  정량 **53.4 ± 58.6 → 7.82 ± 2.61 nm** (Fig. S6). 큰 편차는 저자도 "broad size distribution·severe
  agglomeration" 으로 명시.

### 5.3 as-fabricated 상태 = 전구체가 살아 있다 (Fig. 2c–e)
- **XRD**: Ag–C 25 = 금속 Ag 반사. AgNO₃ 계 2종 = **결정질 AgNO₃ 반사가 우세** → 제작 후에도
  AgNO₃ 가 대체로 미전환.
  ⚠ `figure-read`: AgNO₃ 계 패턴에도 **◆ 금속 Ag 마커가 ~38°/44°/64.5° 에 찍혀 있고, 44° ◆ 는
  최강 ▼(34.5°) 의 ~85% 높이**다 → 부분적 사전환원이 이미 있다 (§15).
- **Raman**: D/G 밴드 거의 동일, I_D/I_G 1.21 / 1.14 / 1.16 → **카본 골격은 안 변했다**(공정 대조군 확보).
- **N 1s XPS**: Ag–C 25 무신호. AgNO₃ 계는 고결합에너지 **nitrate** 성분. PVP 계만 **~400 eV** 추가
  성분 (본문: PVP 의 pyrrolidone N / 그림 라벨: "C-N bonding") → PVP 가 실제로 층에 들어갔다.

### 5.4 Ag 도메인 크기 → Li 증착 동역학 (Fig. 3, Fig. S8, Table S1) — 연속체 모델
1D 시간의존 **전기화학–크리프** 모델. 순서: **카본 리튬화 → Ag 보조 Li 핵생성·성장 → 증착 Li 의 확산 크리프**.
d_Ag = **10 / 50 / 100 nm** 를 각각 AgNO₃–C–PVP 25 / AgNO₃–C 25 / Ag–C 25 의 대표값으로 잡음.

- **핵생성 자리 인자** Γ_site = d_ref/d_Ag (d_ref = 100 nm) → **10 / 2 / 1**.
- **크리프**: Coble(입계) + Nabarro–Herring(격자) 병렬, Eq. (2). 확산도는 **E_a 0.35 eV** 아레니우스.
  D_pore = **25 / 45 / 50 nm** (d_Ag 10/50/100 에 대응, Table S1 에 "**Assumed**" 로 명시).
- 결과 (Fig. 3):
  - (a) 10 nm 가 초기 리튬화 이후 **분극 최소** — 인셋 4.4–5.0 mAh cm⁻² 확대에서 뚜렷.
  - (b) 핵생성률 최대 `figure-read ≈` **2.05 / 1.83 / 1.72** nmol s⁻¹ cm⁻² (10/50/100 nm).
  - (c) Li 핵 누적량 @5.8 mAh cm⁻² `figure-read ≈` **22.4 / 19.7 / 18.2** µmol cm⁻².
  - (d) **j_creep,eq = 0.39 / 0.10 / 0.08 mA cm⁻²** (10/50/100 nm) ← 본문 명시값, 그림과 일치.
  - (e) Q_res,Li/Q_charge 압력–온도 지도(10–30 MPa × 30–60 °C). 실험조건 별(20 MPa, 45 °C)에서
    10 nm 는 `figure-read ≈` **0 (노랑)**, 50/100 nm 는 `figure-read ≈` **0.6–0.85 (짙은 청)**.

> ⚠ Γ_site 가 **10×** 차이인데 핵생성률·핵량은 **1.2× 남짓**만 벌어진다 — 모델 안에서 다른 항이
> 강하게 상쇄한다는 뜻. 반면 **j_creep 은 4.8× 벌어진다** → 이 그림의 결론(“미세 도메인이 좋다”)을
> 실제로 떠받치는 건 핵생성이 아니라 **크리프 쪽**이다. 본문은 둘을 나란히 놓지만 기여도는 비대칭이다.

### 5.5 전환 후 Ag 분포가 유지된다 (Fig. 4)
초기 충전(0.1C) 후 단면 SEM + C/Ag 맵. 층 구조 **SE / 계면층 / Li / SUS**.
Ag–C 25 는 굵고 뭉친 Ag 도메인, AgNO₃–C 25 는 더 미세·광역, **AgNO₃–C–PVP 25 가 가장 균일**.
`figure-read`: 세 시료 모두 **Ag 신호가 석출된 Li 층 전체에 퍼져 있다** — 알려진 Ag 의 집전체 방향
이동(ref [5] Lee 2020)과 정합.

### 5.6 전환이 만드는 계면화학 (Fig. 5a,b)
- **XRD(충전 후)**: Ag–C 25 는 **잔류 금속 Ag + Ag–Li 합금** 공존 → 뭉친 Ag 는 합금화가 덜 됐다.
  AgNO₃ 계 2종은 **AgNO₃ 반사가 완전 소멸** + 뚜렷한 Ag–Li 합금.
  `figure-read` 상 지표: ▽ Li₉Ag₄ · ◇ Li₀.₉₈Ag₀.₀₂ · ◆ Ag.
- **N 1s XPS(충전 후)**: AgNO₃–C 25 = LiNO₃ / LiNO₂ / LiN_xO_y / Li₃N **혼재**(불완전·불균일 환원).
  AgNO₃–C–PVP 25 = **Li₃N 우세**, LiNO₃·LiNO₂ 미약 → 더 균일하고 깊은 환원.
- **방전 후에도 Li₃N 계면상이 유지**된다 (Fig. 5b 오른쪽).

### 5.7 DFT — Li₃N 이 왜 좋은가 (Fig. 5c–e) ★ 우리 기여
§7 에서 별도로 자세히.

### 5.8 반쪽셀 동역학 (Fig. 6a–f, Fig. S9–S13)
- **GITT** (Fig. 6a): AgNO₃ 계는 0 V(vs Li/Li⁺) 근처 **연장된 pre-plating 구간** — AgNO₃ 전환 +
  Ag–Li 합금화가 Li 도금 전에 추가로 일어난다.
- **펄스 내 분극** ΔE_t = E₀⁺ − E_τ (정의는 Fig. S9). Fig. 6b: Ag–C 25 가 가장 크고 요동
  (`figure-read ≈` 초기 스파이크 **1.19 V**, 평탄역 ~0.60 V), PVP 계가 가장 낮고 안정
  (`figure-read ≈` 후기 **0.10 V**).
- **EIS/DRT** (Fig. 6c,d): DRT 가 **R_SE**(τ~0.05 s) / **R_interface**(~0.4 s) / **R_CT,Li–Ag**(~3–5 s)
  세 봉우리 분리. `figure-read ≈` 봉우리 높이 —
  R_interface: 1.95 (Ag–C) / 1.6 (AgNO₃–C) / **1.1 (PVP)**;
  R_CT,Li–Ag: 6.3 / 5.85 / **4.0**.
  ⚠ Nyquist(Fig. 6c)는 세 곡선이 **−Z″ 축으로 오프셋**돼 있어 절대값 판독 불가 — 수치는 DRT 로만.
- **초기 증착 프로파일** (Fig. 6e,f): 정의는 Fig. S10. 값은 §3.2.
  Q_lithiation 이 AgNO₃ 계에서 큰 이유 = **전환에 Li 가 추가 소모**되기 때문.
  그럼에도 **η_nucleation 은 7.2 mV 로 최저** — 전환 비용을 치르고도 핵생성이 유리해졌다는 게 요점.
  15 wt% 에서도 같은 경향 (Fig. S11–S13).
- **CCD** (Fig. 6g,h): §3.2. ⚠ PVP 계는 두 온도 모두 **2.0 mA cm⁻² 에서 시험이 끝난다** —
  파괴점이 아니라 **시험 상한**이다. "≥2.0" 로 읽어야 맞다.

### 5.9 풀셀 (Fig. 7, Fig. S14, S15)
- **Operando 압력** (Fig. 7a,b): ΔP **3.0 → 2.8 → 2.5 MPa**. 더 균일한 Li 증착 = 국소 변형 감소.
  `figure-read`: Ag–C 의 ΔP 골이 **0 아래(~−0.5 MPa)** 까지 내려가고 PVP 는 ~0 에서 멈춘다 →
  진폭 차이 일부는 **비가역 baseline drift** 성분이다.
- **초기 프로파일** (Fig. 7c): AgNO₃ 계가 방전용량이 **더 낮다**(전환 Li 소모). `figure-read ≈`
  Ag–C 193 / AgNO₃–C 187 / PVP 190 mAh g⁻¹.
- **사이클** (Fig. 7d): §3.2. `figure-read ≈` PVP 25 는 350 cy 에서 **~92 mAh g⁻¹**.
- **15 wt%** (Fig. 7e,f): PVP 쪽이 초기 용량·분극 모두 유리하고 그 우위가 지속. §3.3.
  → **"총 Ag 량이 아니라 공간분포·전기화학적 접근성이 Ag 이용률을 지배한다"** 가 이 논문의 최종 주장.

### 5.10 종합 (Fig. 8)
① PVP–Ag⁺ 배위 → 미세·균일 AgNO₃ 도메인 → **균일 반응**
② 첫 충전 전환 → 분산된 Ag–Li 자리(핵생성 균질화) + **Li₃N 계면상**
③ 미세 Ag → 크리프로 Li 를 집전체 쪽으로 이송 → 계면 축적 억제
④ Li₃N 표면 확산장벽이 낮아 → Li adatom 이 **측면 재분배**되어 분산 Ag 자리로 감 → **촉진된 Li 수송**

---

## 6. 계산 ① — 전기화학–크리프 모델 (Methods 4.5, Table S1)

**설정**: 1D 시간의존. 양극 110 µm / SE 분리막 80 µm / **Ag–C 계면층 8 µm** / 집전체.
**0.5C, 45 °C, 20 MPa**, 면적용량 5.8 mAh cm⁻² 까지.

**Eq. (1)** Γ_site(d_Ag) = d_ref/d_Ag, d_ref = 100 nm.
근거: 고정 Ag 함량에서 도메인 수 ∝ d_Ag⁻³, 도메인당 표면적 ∝ d_Ag² → 총 표면적 ∝ d_Ag⁻¹.

**Eq. (2)** R_creep = 4 ε_p D_s,gb σ δ N_A /(k_B T L_int D_pore) + ε_p D_s,bulk σ N_A /(k_B T L_int)
(1항 = Coble 입계확산, 2항 = Nabarro–Herring 격자확산)

**Eq. (3)** Q_res,Li = max[0, Q_dep − j_creep,eq(P,T,d_Ag)·t_dep]

**Table S1 파라미터 전문**

| 파라미터 | 기호 | 값 | 단위 | 출처(원고 표기) |
|---|---|---|---|---|
| 스택압 | σ | 20 | MPa | Experimental |
| 온도 | T | 45 | °C | Experimental |
| 아보가드로 | N_A | 6.02×10²³ | mol⁻¹ | — |
| 볼츠만 | k_B | 1.38×10⁻²³ | J K⁻¹ | — |
| 패러데이 | F | 96485 | C mol⁻¹ | — |
| 충전용량 | Q_charge | 5.8 | mAh cm⁻² | Experimental |
| 리튬화 용량 | Q_lith,max | 0.1 | mAh cm⁻² | **Assumed** |
| 계면층 두께 | L_int | 8 | µm | Experimental |
| Ag 도메인 지름 | d_Ag | 10, 50, 100 | nm | Experimental |
| **유효 공극 크기** | **D_pore** | **25, 45, 50** | **nm** | **Assumed** |
| 계면층 공극률 | ε_p | 0.40 | — | Ref. 39 |
| 입계 Li 확산도 | D_s,gb | 3×10⁻¹² | m² s⁻¹ | Ref. 53, 54 |
| 벌크 Li 확산도 | D_s,bulk | 1×10⁻¹⁶ | m² s⁻¹ | Ref. 53, 54 |
| 입계 두께 | δ | 5 | Å | Ref. 53 |
| 크리프 활성화E | — | 0.35 | eV | Ref. 53 |

> **재현성 감사**: Table S1 값으로 Eq. (2) 를 계산하면 Coble/NH = 4 D_gb δ /(D_bulk D_pore)
> ≈ **2.4×10³** → Coble 이 완전 지배. 따라서 R_creep ∝ 1/D_pore 이고 10 nm vs 100 nm 는
> D_pore 50/25 = **2.0×** 여야 한다. 그런데 Fig. 3d 는 0.39/0.082 = **4.8×** 다.
> 차이는 본문이 *"The resulting creep rate was converted to j_creep,eq"* 라고만 쓰고
> **변환식을 안 준 데서 온다** → **Fig. 3d 는 논문만 보고 재현할 수 없다** (🟡 P2-2).

---

## 7. 계산 ② — DFT Li adatom 확산 ★ (Methods 4.6, Table S2, Fig. 5c–e)

### 7.1 공통 전자구조 설정 (Table S2, 두 열 **병합 셀**)
| 항목 | 값 |
|---|---|
| 코드 | **Quantum ESPRESSO** [55] |
| 범함수 | **PBE** [56] (vdW 보정 없음) |
| 유사퍼텐셜 | **ultrasoft** [57] + **PAW** [58] (원소별 병기는 안 함 → §11-C) |
| 운동E 컷오프 | **60 Ry** |
| 전하밀도 컷오프 | **480 Ry** |
| k-mesh | **2 × 2 × 1 (Γ-centred)** |
| 스미어링 | **Marzari–Vanderbilt, 0.01 Ry** [59] |
| 수렴 (SCF / force) | **1×10⁻⁶ Ry / 1×10⁻³ Ry bohr⁻¹** |

> ⚠ 이 7행이 Table S2 에서 **gridSpan=2 로 두 열에 걸쳐 병합**돼 있다 (원본 XML 실측).
> 즉 표는 "**LiC₆ 도 같은 QE 설정으로 계산했다**" 고 말한다. 이게 §4.6 서술과 충돌한다 (§11-A2).

### 7.2 Li₃N (001)
- **α-Li₃N**, **N-노출 (001)** 종단, **3 × 3** 면내 초격자, **Li₂N 4면 + Li 3면**.
- 기판 **135 원자 + Li adatom 1**.
- 셀 **a = b = 10.95 Å, c = 28.545 Å, γ = 120°**, 진공 **≈15.7 Å**.
- **바닥 Li₂N/Li 이중층 2개 고정**.
- **방법 = 두 점 구속이완**: adatom 의 **면내(x,y) 좌표만 고정**(흡착최소 / 인접 안장영역),
  **z 와 자유 슬랩 원자는 이완**. 장벽 = 두 이완에너지 차.
  → **NEB 아님.** 우리 kb 가 이 계에서 NEB 4연속 실패를 기록했기 때문이다
  (`kb/methodology/li_adatom_neb_protocol.md`: 자유 슬랩 = 재구성 폭주, 동결 슬랩 = 초기-site 기억 편향).
- 결과: E_ads(최소) **−2.988**, E_ads(안장영역) **−2.870** → **ΔE = 0.118 eV**.

### 7.3 LiC₆ (0001)
- **stage-1 흑연 층간화합물**, **√3 × √3 R30°**, **2 × 2 × 2**, **graphene-terminated**.
- **108 원자 + Li adatom 1**, 진공 **15 Å**, **바닥 50 % 고정**.
- **방법 (§4.6 기재)**: **CI-NEB** [60] + **UMA-oc20 MLIP** [61] (ASE [62]), **7 images**,
  **IDPP** 초기보간 [63], **fmax 0.05 eV Å⁻¹**.
- 결과: **0.290 eV**.

### 7.4 결론 문장
"장벽이 LiC₆ (0001) **0.290 eV** → Li₃N (001) **0.118 eV** 로, **약 59 % 감소**" (비율 **2.46×**).
→ Li₃N 계면상이 **측면 Li adatom 재분배**의 동역학적 경로를 열어 준다.

### 7.5 ⚠ 이 절이 감추고 있는 것 (§11 에서 판정)
1. **두 표면의 장벽 정의가 다르다** — Li₃N = 2점 구속이완(안장을 *탐색*하지 않음),
   LiC₆ = CI-NEB(안장을 *수렴*시킴).
2. **두 표면의 에너지 출처가 다를 수 있다** — §4.6 대로면 LiC₆ 는 MLIP 에너지, Table S2 대로면 QE 에너지.
3. **Li₃N 의 "안장영역"은 이웃 자리로 가는 안장이 아니다** — kb C6 이 실측으로 남긴 미해소 항목.
   다만 원고는 *"saddle-region configuration"* 이라고만 써서 **서술은 방어 범위 안**이다.

---

## 8. 전체 논증 흐름

```
물리혼합 Ag–C → 건조 중 응집 (표면에너지 최소화)          [Fig. 1c, S2]
        ↓ 대안
AgNO₃ 를 NMP 에 용해 → 균일 Ag⁺ … 그러나 건조 중 재결정   [본문 §2]
        ↓ 그래서
PVP 카보닐–Ag⁺ 배위로 이동 봉쇄                          [FT-IR Fig. S5]
        ↓ 결과
AgNO₃ 도메인 53.4 → 7.82 nm                              [Fig. 2b, S6]
        ↓ 그런데 왜 작으면 좋은가? → 두 갈래로 답한다
   ┌─ (모델) 작을수록 핵생성 자리 ↑ + 크리프 수송 ↑ → 계면 Li 축적 ↓   [Fig. 3]
   └─ (전환) AgNO₃ → Ag–Li 자리 + Li₃N 계면상                        [Fig. 5a,b]
                    ↓ Li₃N 은 왜 좋은가?
              (DFT) 장벽 0.290 → 0.118 eV, 측면 재분배 용이           [Fig. 5c–e]
        ↓ 검증
반쪽셀: η_nuc 10.1→7.2 mV, R_int·R_CT ↓, CCD 0.3→≥2.0                [Fig. 6]
풀셀: ΔP 3.0→2.5 MPa, 174/125 → 350 cy                               [Fig. 7]
저-Ag 15 wt% 에서 격차 확대: 35.4 → 54.2 % (+18.8 %p)                [Fig. 7f]
        ↓
"총 Ag 량이 아니라 공간분포가 Ag 이용률을 지배" — 최종 주장           [Fig. 8]
```

---

## 9. Figure set ★

**👁 = 내가 실제로 이미지를 보고 쓴 것 (9장) · ○ = 캡션/본문만 (15장)**

| Fig | 내용 | 우리 활용 |
|---|---|---|
| ○ 1a–d | 물리혼합 vs 전구체 개념도 · Ag 입자 SEM · Ag–C 25 표면 SEM+Ag맵 · 슬러리 공정도 | 문제설정 도식. **안 봄** — 응집 스케일 주장은 Fig. 1c 원본 확인 필요 |
| 👁 2a,b | AgNO₃–C 25 vs PVP 25 표면 SEM+Ag맵 / HAADF-STEM | ⚠ **(b) 두 패널 배율이 100 nm vs 20 nm 로 5× 다르다** — 시각비교는 like-for-like 아님. 정량은 Fig. S6 로만 |
| 👁 2c | XRD (as-fabricated) — ● C ◆ Ag ▼ AgNO₃ | ⚠ AgNO₃ 계에도 **◆ Ag 가 뚜렷**(44° ◆ ≈ 최강 ▼ 의 85%) → **부분 사전환원** 존재 |
| 👁 2d | Raman D/G, I_D/I_G 1.21/1.14/1.16 | 카본 골격 불변 = 좋은 공정 대조군. 우리도 도핑 전후 대조에 쓸 수 있는 값싼 게이트 |
| 👁 2e | N 1s XPS (as-fabricated) | nitrate 잔존 + PVP 의 ~400 eV. 그림 라벨은 "C-N bonding", 본문은 "pyrrolidone N" |
| 👁 3a–c | 모의 충전곡선 · 핵생성률 · Li 핵량 (10/50/100 nm) | ⚠ **패널 (a) 에 `0.1C` 라벨** — Methods §4.5·(e) 캡션은 0.5C (§11-B1). Γ_site 10× 인데 (b),(c) 는 1.2× 만 벌어짐 |
| 👁 3d | j_creep,eq = **0.39 / 0.10 / 0.08 mA cm⁻²** | 이 그림이 논문 결론을 실제로 떠받친다. ⚠ 축 라벨은 `j_creep`, 본문은 `j_creep,eq` |
| 👁 3e | Q_res,Li/Q_charge 압력–온도 지도 3장 | 실험조건(20 MPa,45 °C) 별표에서 10 nm 만 ≈0. **우리 스택압 규율(20 MPa)과 같은 창** |
| 👁 4a–c | 초기충전 후 단면 SEM + C/Ag 맵 | ⚠ **EDS 분해능(~µm) 이 8 vs 53 nm 를 못 가른다** — 이 그림이 뒷받침하는 건 µm 스케일 균일성뿐 (§15) |
| 👁 5a | 충전 후 XRD — ▽ Li₉Ag₄ ◇ Li₀.₉₈Ag₀.₀₂ ◆ Ag | Ag–C 만 금속 Ag 잔류 = 뭉친 Ag 의 합금화 미완. Ag–Li 상 동정 지표로 재사용 가능 |
| 👁 5b | N 1s XPS 충전 후/방전 후 | LiNO₃/LiNO₂/LiN_xO_y/Li₃N 분해. PVP 계 = Li₃N 우세 + **방전 후 유지** |
| 👁 5c | Li₃N (001) 흡착E: **−2.988 (Minimum) / −2.870 (Saddle)** + 원자모형 | ✅ **kb C4/C7 준수 확인** — `top`/`bridge` 라벨이 제거되고 `Minimum`/`Saddle` 로만 표기됨. `li3n_barrier_fig_origin.csv` (−2.9877/−2.8695) 와 반올림까지 일치 |
| 👁 5d | LiC₆ / Li₃N 확산 에너지 프로파일 | 🔴 **P0-1**: Li₃N 이 **실선 연속곡선**인데 계산점은 2개뿐. 캡션에서 "guide to the eye" 문장이 빠졌다. LiC₆ 우측 끝점이 `figure-read ≈ −0.02 eV` 로 0 아래 = 끝점 비대칭(0.0222) 이 그림에 노출돼 있다 |
| 👁 5e | 장벽 막대 **0.290 / 0.118 eV** | 우리 정본과 일치(단, 0.290 의 계보는 §11-A3) |
| 👁 6a,b | GITT + 펄스내 분극 ΔE_t | ΔE_t 정의(Fig. S9)가 깔끔 — 우리 반쪽셀 해석에 차용 가능 |
| 👁 6c,d | Nyquist + **DRT** (R_SE / R_interface / R_CT,Li–Ag) | ⚠ Nyquist 는 −Z″ 오프셋이라 절대값 판독 불가. **DRT 3-피크 분해**가 실질 정량 |
| 👁 6e,f | 초기증착 프로파일 + η_nuc / Q_lith 막대 | 값 전부 본문과 일치 ✅ |
| 👁 6g,h | CCD 60 °C / 45 °C | ⚠ PVP 는 **2.0 에서 시험 종료**(파괴 아님) → "≥2.0" |
| 👁 7a,b | Operando 압력 셋업 + ΔP **3.0/2.8/2.5 MPa** | 240 kg/13 mm ≈ 17.7 MPa 로 스택압 자체검증 가능. ΔP 골이 0 아래로 내려가는 baseline drift 주의 |
| 👁 7c,d | 25 wt% 초기 프로파일 + 350 cy 사이클 | Ag–C 의 CE 요동(~75 cy)이 단락 전조 — 우리 셀 판정에 쓸 지표 |
| 👁 7e,f | 15 wt% — **102.2 vs 64.1 mAh g⁻¹, 54.2 vs 35.4 %** | 논문의 진짜 주장(저-Ag 에서 격차 확대) |
| 👁 8 | 기전 종합 도식 | Li₃N 을 **SE/계면층 경계의 연속 박막**으로 그림 — XPS 는 그 *위치*를 증명하지 않는다 (추론) |
| ○ S1–S5 | 카본블랙 SEM · 필름 사진 2종 · 15 wt% SEM/Ag맵 · **FT-IR** | **안 봄**. FT-IR 수치(1652.2→1617.5)는 본문 명시값 |
| 👁 S6 | HAADF + 크기분포 **53.4±58.6 / 7.82±2.61 nm** | ⚠ 상단 히스토그램이 **명백히 이봉**(20–40 nm 에 23 counts, 145–185 nm 에 별도 무리)인데 **가우시안 fit 이 겹쳐져 있고 데이터를 전혀 안 맞춘다**. n ≈ 37 / 44. 축 라벨 "Ag diameter" vs 본문 "AgNO₃-domain" |
| ○ S7 | 15 wt% XRD | **안 봄** |
| 👁 S8 | 전기화학 모델 도식 | **Li₃N 이 없다** — 크리프 모델과 DFT 가 분리돼 있다는 직접 증거 (§15) |
| ○ S9, S10 | ΔE_t 정의 · Q_lith/η_nuc 정의 | **안 봄**. 정의는 본문 서술로 충분 |
| ○ S11–S13 | 15 wt% 증착 프로파일 · Nyquist · DRT | **안 봄** |
| ○ S14, S15 | 25/15 wt% 사이클 중 전압 프로파일 | **안 봄** |
| ○ GA | Graphical Abstract (이미지 1장, 본문 텍스트 없음) | **안 봄** |
| **Table S1** | 크리프 모델 파라미터 14행 | §6 에 전문 전사. **D_pore·Q_lith,max 가 "Assumed"** |
| **Table S2** | DFT 파라미터 (2열, 전자구조 7행은 **병합**) | §7.1 에 전문 전사. **병합이 §4.6 과 충돌** (§11-A2) |

---

## 10. Post-processing ★

| 무엇 | 도구 | 수치화·기록 방식 |
|---|---|---|
| **NEB (LiC₆)** | ASE `ase.mep.NEB` + **CI-NEB**, IDPP 초기보간, **UMA-oc20** (FAIRChem) | 7 images, fmax 0.05 eV Å⁻¹. 상대에너지 프로파일 → Fig. 5d 회색곡선 |
| **구속이완 (Li₃N)** | QE `pw.x` `relax`, adatom **xy 고정 / z 자유** | 두 점(min, saddle-region) 각각 BFGS 수렴 → 차이가 장벽. `db/properties/diffusion.json` `li3n_001_p0_2point_constrained_dft_2026-07-15` |
| **흡착에너지** | 위 두 이완의 총에너지 | Fig. 5c 막대. `db/properties/li3n_barrier_fig_origin.csv` `Eads_slab_abs` |
| **프로파일 곡선** | (원고엔 미기재) 스플라인 | `db/properties/li3n_barrier_origin.csv` 401행 Origin-ready. **`Li3N_guide_eV` 는 폐기된 mirrored-spline 모양 × 진폭 재조정** — 계산된 경로가 아니다 |
| **DRT** | Ciucci–Chen 베이지안 DRT [44] | γ(ln τ) vs τ, 3-피크 귀속 (R_SE/R_interface/R_CT) |
| **XPS 피팅** | (소프트 미기재) | N 1s 를 LiNO₃/LiNO₂/LiN_xO_y/Li₃N/nitrate/C–N 성분으로 분해 |
| **입도 분석** | "Quantitative image analysis" (도구 미기재) | HAADF 에서 도메인 지름 측정 → mean ± SD + 가우시안 fit |
| **XRD 상동정** | (소프트 미기재) | 마커 기반 (◆ Ag, ▼ AgNO₃, ● C, ▽ Li₉Ag₄, ◇ Li₀.₉₈Ag₀.₀₂) |
| **연속체 모델** | (코드 미기재) | 1D 시간의존, Eq. (1)–(3). **크리프율 → 전류밀도 변환식 미기재** |

---

## 11. 🔴 자기감사 — 원고 주장 vs 우리 정본

> 대조 대상: `db/properties/diffusion.json` · `db/properties/li3n_barrier_origin.csv` ·
> `db/properties/li3n_barrier_fig_origin.csv` · `db/properties/canonical_registry.json` ·
> `kb/methodology/li_adatom_neb_protocol.md` · `kb/syntheses/li3n_barrier_revision_defense_2026_08_12.md`

### 11-A. DFT 축 (우리 계보 — 여기가 핵심)

| # | 원고 주장 | 값 | 어디 | 우리 정본 | 판정 |
|---|---|---|---|---|---|
| 1 | Li₃N(001) 확산장벽 | **0.118 eV** | Fig. 5e, Table S2, Highlights | `diffusion.json` `li3n_001_p0_2point_constrained_dft_2026-07-15` **0.1182**; `li3n_barrier_origin.csv` `DFTpoint_eV` max **0.11820** | ✅ **일치** |
| 2 | E_ads 최소점 | **−2.988 eV** | Fig. 5c | `li3n_barrier_fig_origin.csv` `onN_min4` **−2.9877** (converged) | ✅ **일치** |
| 3 | E_ads 안장영역 | **−2.870 eV** | Fig. 5c | `li3n_barrier_fig_origin.csv` `bridge_saddle3` **−2.8695** (converged) | ✅ **일치** |
| 4 | 감소율 | **≈59 %** / 2.46× | Results | 방어카드 A-7 "**0.118 eV / ≈59 %, 비율 2.46×**" | ✅ **일치** (확정 결정 반영됨) |
| 5 | 진공 | **≈15.7 Å** | §4.6, Table S2 | 방어카드 A-2 "→ **15.7 Å**" | ✅ **일치** (수정 반영됨) |
| 6 | 자리 이름 미사용 | `Minimum`/`Saddle` | Fig. 5c,d | 방어카드 C-2 "**adsorption minimum / saddle configuration 으로**" | ✅ **일치** (C4·C7 노출 차단됨) |
| 7 | LiC₆(0001) 장벽 | **0.290 eV** | Fig. 5e, Table S2 | `li3n_barrier_origin.csv` `LiC6_DFT_eV` max **0.28968** | 🟠 **일치하나 계보 주의** → A3 |
| 8 | LiC₆ 방법 | "**CI-NEB + UMA-oc20**" (끝) | §4.6 | UMA-oc20 CI-NEB **단독** = **0.241 eV**; **DFT-SCF on UMA 기하** = 0.287/0.290 | 🔴 **불일치 = P0-2** → A2 |
| 9 | Fig. 5d Li₃N 곡선 | 실선 연속 프로파일 | Fig. 5d | `Li3N_guide_eV` = **폐기된 mirrored-spline × 진폭재조정**(편차 5e-7). 계산점 2개 | 🔴 **확정결정 위반 = P0-1** → A1 |

#### A1 🔴 **P0-1 — Fig. 5d 의 Li₃N 곡선이 "계산된 경로"처럼 보인다**

`kb/syntheses/li3n_barrier_revision_defense_2026_08_12.md` (status **확정**) 이 두 가지를 못 박았다:

> **확정 캡션**: "*(d) Calculated diffusion energy profiles and (e) corresponding diffusion barriers for
> Li adatom on the LiC₆ (0001) and Li₃N (001) surfaces. **Symbols in (d) denote DFT-calculated
> configurations and the lines are guides to the eye.***"

> **그림 지침**: "*5d 에서 이 곡선을 **계산된 경로처럼 그리면 안 된다.** 실선 금지, 점선 + 캡션에
> 'dashed line is a guide to the eye connecting the two computed configurations' 명시.*"

**제출본 상태 (실측)**:
- Fig. 5 캡션 = "*(d) calculated diffusion-energy profiles and (e) corresponding diffusion barriers…*"
  → **"Symbols … guides to the eye" 문장이 통째로 빠졌다.**
- Fig. 5d 의 Li₃N 곡선 = **파란 실선** (점선 아님).

**왜 위험한가**: 우리가 Li₃N 에서 계산한 것은 **점 2개**뿐이다. 그 곡선 모양은
`li3n_neb_fit_optimal.csv` 의 **폐기된 mirrored-spline NEB** 형상에 진폭만 0.1182 로
갈아끼운 것이다 (편차 5e-7 로 검산됨). 리뷰어가 "반응좌표 상 중간 이미지의 에너지는?" 하고
물으면 **답할 데이터가 없다.** 게다가 kb 는 min→TS 직선 경로가 **N 원자를 관통**해서
7점 보간 자체가 물리적으로 불가능하다는 것까지 실측해 뒀다(관통 가드 `CLEARANCE_A = 1.90`).

**조치**: 캡션에 확정된 두 문장을 복원하고, Li₃N 곡선을 **점선**으로 바꾼다. (LiC₆ 는 실측 7점이므로
실선이어도 되지만, 그 7점을 **심볼로 찍어 주는 것**이 캡션 문장과 짝이 맞는다.)

#### A2 🔴 **P0-2 — Methods §4.6 의 LiC₆ 서술이 반쪽이다**

원고 §4.6 원문:
> "*For LiC₆, … The Li-adatom diffusion pathway was **generated using the climbing-image nudged
> elastic band method** [60] **with the UMA-oc20 interatomic potential** [61] … maximum-force
> criterion of 0.05 eV Å⁻¹.*"

여기서 끝난다. **QE 단일점 단계가 없다.** 그런데:

| 경로 | 우리 값 |
|---|---|
| UMA-oc20 CI-NEB **단독** | **0.241 eV** (`li_adatom_neb_protocol.md` §OUTCOME 표) |
| **DFT-SCF on UMA 기하** (7 images) | **0.287 eV** (`diffusion.json`) / 스플라인 최대 **0.28968** |

즉 **§4.6 이 기술한 경로만으로는 0.290 이 안 나온다.** 반면 **Table S2 는 QE 파라미터 7행을
두 열에 병합**해 놓아 "LiC₆ 도 QE" 라고 말한다 — 방어카드도 그 병합을 의도한 방어수단으로 적어 뒀다
("*왜 한쪽만 NEB 인가 / 두 값이 비교 가능한가* → ᵃ 앞부분 + **표의 전자구조 행이 동일함**").

**⇒ 표는 맞고 Methods 가 틀렸다.** 방어카드 A-4 는 "*LiC₆(CI-NEB **+ DFT 단일점**) 문장 유지*"
를 요구했는데 **"+ DFT 단일점" 절반이 반영되지 않았다.**

**추가 노출**: Highlights 는 "*Li₃N lowers the Li-adatom diffusion barrier **from 0.290 to 0.118 eV**.*"
라고 아무 단서 없이 쓴다. §4.6 만 읽은 리뷰어에게 이건 **MLIP 값과 DFT 값을 뺀 것**으로 보인다.

**조치**: §4.6 에 한 문장 추가 —
*"Single-point DFT calculations were then performed on the resulting NEB image geometries using the
same plane-wave settings as for Li₃N (Table S2), and the reported LiC₆ barrier is obtained from those
DFT energies."* (방어카드 각주 ᵇ 문구를 회신이 아니라 **본문**으로 올리는 셈.)

#### A3 🟠 **P1-1 / P1-2 — 0.290 의 계보**

`li3n_barrier_origin.csv` 를 직접 검산한 결과:

| 항목 | 값 |
|---|---|
| 스플라인 최대 | **0.28968 eV @ xi = 0.4100** |
| 7 이미지 실계산점 | 0.0000 / 0.1684 / 0.2816 / **0.2866** / 0.2762 / 0.1594 / **−0.0222** |
| 실제 최고 계산점 | **img3 = 0.2866 eV** |

⇒ **보고된 0.290 은 계산된 이미지가 아니라 이미지 사이를 지나는 스플라인의 오버슛**이다.
그리고 `diffusion.json` 은 같은 계산을 **0.287** 로 적어 둔다 → **우리 db 안에서 값이 갈라져 있다**(P1-2).

**영향은 작다**: 0.2866 을 쓰면 감소율 58.8 %, 0.290 이면 59.3 % — 결론 문장이 안 바뀐다.
**그러나** A1 을 고쳐 "심볼 = 계산된 배치" 라고 캡션에 쓰는 순간, 막대(0.290)와 심볼 최대(0.2866)가
**서로 다른 수가 되어 그림 안에서 모순**이 된다. 두 P0/P1 은 **같이 고쳐야 한다.**

**조치 (택1)**: ① 보고값을 **0.287** 로 통일하고 `diffusion.json` 을 정본으로 삼는다(권장 — 계산점 기반),
또는 ② 0.290 을 유지하되 캡션/각주에 "spline maximum" 임을 명시. **①이 방어하기 훨씬 쉽다.**
어느 쪽이든 `li3n_barrier_origin.csv` 와 `diffusion.json` 의 값을 **하나로 맞춰야** 한다.

### 11-B. 실험·모델 축 (저자 측 데이터 — 우리 정본에 대응 항목 없음)

> 아래는 **우리 db 에 대조군이 없다**(전부 저자 측 실험/모델). 따라서 판정은 *일치/불일치* 가 아니라
> **내적 정합성**만 본다.

| # | 항목 | 판정 |
|---|---|---|
| B1 🟠 | **C-rate**: Fig. 3a 패널 라벨 `0.1C` vs Methods §4.5 "calculated at **0.5C**" vs Fig. 3 캡션 "(e) … **at 0.5C**" | 🟠 **내부 모순**. (a)–(d) 가 어느 rate 인지 확정 불가. 셋 중 하나를 고쳐야 함 |
| B2 🟠 | **18.8**: Abstract "18.8**%** higher capacity retention" vs Conclusion "18.8 **percentage points**" | 🟠 **단위 불일치**. 54.2 − 35.4 = 18.8 **%p** 가 맞다. Abstract 를 "%p" 또는 "18.8-percentage-point" 로 |
| — | 용량유지율 산술: 102.2 / 54.2 % → 초기 188.6; 64.1 / 35.4 % → 초기 181.1 mAh g⁻¹ | ✅ Fig. 7f `figure-read ≈` 190 / 185 와 정합 |
| — | 스택압: 240 kg / ⌀13 mm = 17.7 MPa vs 본문 20 MPa | ✅ 자릿수 정합 (도식은 대표값) |
| — | η_nuc·Q_lith·CCD·ΔP·사이클 수 전부 | ✅ 본문 ↔ Fig. 6f/6g/6h/7b/7d 그림값 **전수 일치** |

### 11-C. 🟡 P2 (경미 — 그러나 에디터/리뷰어가 잡는다)

| # | 항목 | 조치 |
|---|---|---|
| C1 | **저자 byline 파손**: 원본 XML 에 `Yonghoon An, ~~^b, ~~^b, Jong-Won Lee` — 리터럴 `~~` 2개 + `b` 상첨자 **중복**. 편집 잔재로 보이며 이름이 하나 빠졌을 가능성 | **제출 전 필수 수정.** 안용훈의 소속이 ^b(SK On)로 조판돼 있는 것도 의도인지 확인 |
| C2 | **Eq. (2) → Fig. 3d 재현 불가** — 크리프율→전류밀도 변환식 미기재. Table S1 값으로는 10 vs 100 nm 가 2.0× 여야 하는데 그림은 4.8× | SI 에 변환식 한 줄 추가 |
| C3 | **배율 불일치** — Fig. 2b (100 nm vs 20 nm), Fig. S6 HAADF (500 nm vs 50 nm) | 같은 배율 패널 추가 or 캡션에 명시 |
| C4 | **Fig. S6 축 라벨 "Ag diameter"** vs 본문/캡션 "**AgNO₃**-domain diameter" (as-fabricated 는 XRD 상 AgNO₃) | 축 라벨을 AgNO₃ 로 |
| C5 | **Fig. S6 가우시안 fit** 이 상단(이봉) 데이터를 전혀 안 맞춘다 | fit 제거 or 로그정규. 본문은 이미 "broad distribution" 으로 방어 중 |
| C6 | **`canonical_registry.json` 미등록** — 0.118 / 0.290 (또는 0.287) 이 42 entries 안에 없다. 등록된 건 MD Ea 계열뿐 | **투고본 headline 수치는 등록해야 한다** (CLAUDE.md 마감규율). `metric: li_adatom_barrier_eV`, `method_id: qe-pbe-uspp-paw__60-480Ry__2x2x1__MV0.01__2point-constrained` 로 2행 추가 권장 |
| C7 | §4.6 "ultrasoft [57] and PAW [58]" — **원소별 병기 안 됨** (방어카드 A-3 은 병기 요구; Li=USPP, N=USPP, C=PAW) | 한 문장으로 병기 |
| C8 | Fig. 3d 축 라벨 `j_creep` vs 본문 `j_creep,eq` · Fig. 2e 라벨 "C-N bonding" vs 본문 "pyrrolidone nitrogen" | 표기 통일 |

---

## 12. ✅ 금지규율 전수검사 (CLAUDE.md 데이터 규율)

| 규율 | 원고에 해당 문장이 있나 | 판정 |
|---|---|---|
| **⛔ UMA 를 Li₃N 에 사용 금지** (2026-06 결정론적 편향) ← **최우선 확인 항목** | **없다.** §4.6 은 Li₃N 을 **QE 구속이완**으로 명시하고, UMA-oc20 은 **LiC₆ 에만** 등장 | ✅ **통과**. kb 가 폐기한 UMA-Li₃N 값(0.054 / 0.237)은 원고에 **0회** 등장 |
| **⛔ MD σ 절대값 인용 금지 · 비율도 멀티시드만** | 원고에 MD·MSD·Nernst–Einstein·σ 계산이 **아예 없다** (`mS cm⁻¹`, `molecular dynamics` 전문검색 0회) | ✅ **해당 없음** |
| **⛔ `b2o3_vs_lpscl16_conductivity.csv` FORBIDDEN 문구** (`statistically equivalent transport` / `conductivity preserved` / `equivalent sigma` / 순위·기전 주장) | 전문검색 **0회**. B₂O₃ 자체가 이 논문과 무관 | ✅ **해당 없음** |
| **⛔ b2o3 UMA-MD 축 전체 인용 불가** (2026-08-25, 0.222 eV 포함) | 전문검색 **0회** | ✅ **해당 없음** |
| **⛔ Band gap 은 fixed-occupations nscf VBM/CBM 만** (DOS-threshold 판독 금지) | 원고에 band gap·DOS·전자구조 계산이 **없다** | ✅ **해당 없음** |
| **BVSE 정량·순위는 원본 주기셀 값만** | BVSE 없음 | ✅ **해당 없음** |
| 평균류 지표 창 일치(−8..0 eV) | 해당 계산 없음 | ✅ **해당 없음** |

> **요약**: 원고는 우리 **금지목록을 하나도 건드리지 않는다.** 이 논문의 계산은
> (i) QE 구속이완 DFT 2점, (ii) UMA-oc20 CI-NEB 경로 + (미기재) QE 단일점, (iii) 저자 측 연속체 모델
> 뿐이고, MD·전도도·밴드갭·BVSE·B₂O₃ 축을 전혀 쓰지 않는다.
> **위험은 "금지값 인용"이 아니라 "방법 귀속의 불완전"(§11-A1, A2) 에 있다.**

---

## 13. 적용 인사이트

1. **Li₃N 은 우리 SEI 축의 "빠른 측면수송" 후보로 확정 대역을 얻었다.**
   0.118 (우리 DFT) ↔ 0.133 (문헌 [41] Kim/Cui ACS Nano 2023, GPAW CatLearn ML-NEB) 이
   **같은 0.10–0.13 대역**에 있다. 우리 값이 문헌과 독립적으로 정합한다는 것은
   **§11-A1/A2 를 고치고 나면** 그대로 방어 자산이 된다.

2. **"무른 이온성 표면에서는 NEB 대신 구속 PES/2점"** 이라는 방법선택 규칙이 이 원고로 실전 검증됐다.
   Li₃N(NEB ✗ / 구속 ✓) vs LiC₆(NEB ✓ / PES ✗) 의 **재료-방법 궁합**은
   `kb/methodology/li_adatom_neb_protocol.md` 에 이미 있고, 앞으로 새 SEI 표면(Li₂O·LiF·Li₂CO₃)을
   칠 때 **먼저 이 표를 보고 방법을 고르면 된다.**

3. **DRT 3-피크 분해(R_SE / R_interface / R_CT)** 는 우리가 아직 안 쓰는 도구인데,
   Nyquist 반원이 겹칠 때 계면 vs 전하전달을 가르는 값싼 방법이다.
   우리 LPSCl 반쪽셀 해석에 그대로 이식 가능 (Ciucci–Chen 베이지안 DRT, ref [44]).

4. **스택압 20 MPa 창이 겹친다.** Fig. 3e 의 압력–온도 지도가 10–30 MPa × 30–60 °C 인데,
   우리 규율(스택압 20 MPa)과 같은 창이라 **우리 셀 조건에서 크리프가 지배적인지**를
   이 지도로 바로 읽을 수 있다.

---

## 14. 인용 가능 문장 (수정 후에만)

- ✅ "Li adatom 측면확산 장벽은 Li₃N(001)에서 **0.118 eV** 로, 리튬화 카본(LiC₆(0001))의
  **0.29 eV** 대비 절반 이하이며, 이는 같은 표면에 대해 보고된 문헌값 **0.133 eV** 와 정합한다."
- ✅ "Li₃N(001) 위 Li adatom 은 흡착최소(**−2.988 eV**)와 인접 안장영역(**−2.870 eV**)의
  두 독립 수렴 구속이완으로 평가했다."
- ⚠ **§11-A2 를 고치기 전까지 금지**: "장벽이 0.290 에서 0.118 eV 로 감소" 를 **방법 단서 없이**
  쓰는 것 (Highlights 현재 문구). 두 값의 방법이 다르다는 것을 같은 문단에 밝혀야 한다.
- ⚠ **§11-A1 을 고치기 전까지 금지**: Fig. 5d 를 "**계산된 Li₃N 확산 경로**" 라고 부르는 것.
  계산된 것은 **두 배치**이지 경로가 아니다.

---

## 15. 주의/한계 (over-claim 방지 — 비판적으로)

1. **🔴 두 표면의 장벽이 서로 다른 정의로 계산됐다.** Li₃N = 2점 구속이완(안장을 *가정*),
   LiC₆ = CI-NEB(안장을 *수렴*). 게다가 에너지 출처도 서술상 다르다(§11-A2).
   "59 % 감소" 는 **동일 프로토콜 비교가 아니다.** 방어카드가 준비한 논리("MLIP 기하 위 DFT
   단일점은 TS 를 매끄럽게 하므로 이 비율은 **보수적 하한**")는 옳지만, **그 문장이 원고 어디에도 없다.**
   `0.133` 도 원고·SI 전문에서 **0회** 등장한다 — 즉 정합성 방어 근거가 문서에 없다.

2. **🔴 계산된 안장점이 최근접 hop 의 안장점이 아니다** (kb C6, 미해소).
   min 에서 등가 자리까지는 2.107 Å 인데 계산된 TS 는 그 직선 위 **xi = 1.20**(도착지보다 0.43 Å 더 멀다).
   원고가 *"saddle-region configuration"* 이라고만 써서 **서술은 방어 범위 안**이지만,
   실제 2.107 Å hop 의 안장점(N–N 다리)은 **계산된 적이 없다**. 계산하면 0.118 보다 **낮아질 수 있고**,
   그러면 논문 주장은 오히려 **강해진다**.

3. **🟠 슬랩 두께 수렴 근거가 없다** (kb C2, 미해소·가장 약한 지점).
   우리 4층(135+1 원자) vs 문헌 6층. 그리고 우리 4층 슬랩에는 min4 보다 **0.085 eV 낮은
   2N-bridge pocket** 이 있어(kb C3), 엄밀한 escape barrier 를 적용하면 **0.2035 eV** 가 된다.
   **6층 243원자 2점 테스트 한 번이 C2·C3 를 동시에 닫는다** — 리비전까지 시간이 있으면 지금 걸어야 한다.

4. **🟠 진공 표면 ≠ 매몰 계면.** DFT 는 Li₃N(001)·LiC₆(0001) **자유표면**을 본다. 실제 셀에서
   Li₃N 은 LPSCl 과 카본/Ag 사이에 **매몰된 계면상**이고, Fig. 8 도 그렇게 그린다.
   매몰 계면의 측면 확산장벽은 진공 표면값과 다를 수 있다 — 원고는 이 근사를 언급하지 않는다.

5. **🟠 두 계산이 서로 연결돼 있지 않다.** 크리프 모델(Fig. 3)에 Li₃N 이 없고(Fig. S8 도식에도 없다),
   DFT 장벽(Fig. 5)이 모델 입력이 아니다. 제목의 "**coupled** control" 은 **서술적 종합**이지
   계산된 결합이 아니다. 리뷰어가 "그럼 Li₃N 이 j_creep 을 얼마나 바꾸나?" 물으면 답이 없다.

6. **🟠 Fig. 4 의 EDS 분해능이 주장 스케일에 못 미친다.** 8 nm vs 53 nm 도메인 차이를
   SEM-EDS(상호작용 부피 ~µm) 로 볼 수 없다. Fig. 4 가 실제로 보여 주는 것은
   **µm 스케일 Ag 균일성**이다. "전구체 분포가 전환 후에도 유지된다" 는 결론 자체는
   Fig. 2b/S6(STEM) 과 합쳐야 성립한다.

7. **🟡 as-fabricated 시료에 이미 금속 Ag 가 있다.** Fig. 2c 에서 AgNO₃ 계 패턴의 ◆(44°) 가
   최강 ▼ 의 ~85% 높이다. 본문은 "predominantly / largely unconverted" 로 넘어가는데,
   PVP 는 **Ag⁺ 환원제로도 알려져 있고 저자 스스로 ref [32]("Reducing ability … of PVP")를 인용**한다.
   **사전환원 분율이 두 시료에서 다르면** "PVP 가 도메인을 작게 했다" 와 "PVP 가 일부를 환원해
   Ag 씨앗을 만들었다" 가 섞인다 — 정량(예: XRD Rietveld 또는 Ag 3d XPS)이 있으면 훨씬 단단해진다.

8. **🟡 CCD 2.0 mA cm⁻² 는 측정된 임계값이 아니다** — 두 온도 모두 그 값에서 시험이 종료된다.
   "≥2.0" 로 써야 하고, 지금 본문("remains stable up to 2.0")은 정확하지만 독자가 CCD 값으로 오독하기 쉽다.

9. **🟡 Γ_site 의 근거가 얇다.** Eq. (1) 은 총 Ag 표면적 ∝ d_Ag⁻¹ 이라는 기하 논증만으로
   **핵생성률 스케일**을 정하는데, 실제 핵생성 자리 밀도는 표면적뿐 아니라 과전압·젖음성에 걸린다.
   그리고 Γ_site 10× 가 결과에서 1.2× 밖에 안 나온다(§5.4) — 이 인자가 결론을 지탱하지 않는다.
   결론을 지탱하는 건 **D_pore(Assumed) 를 통한 크리프**다.

10. **🟡 d_Ag = 100 nm 배정의 근거가 가장 약하다.** Ag–C 25 의 원료 D50 은 **60 nm** 이고
    Fig. 1c 는 **µm 스케일** 응집을 보여 준다. 100 nm 는 그 사이의 임의값이다
    (다만 더 크게 잡으면 Ag–C 가 더 불리해지므로 **보수적 선택**이긴 하다).

---

## 16. 기법 용어 미니사전

| 용어 | 뜻 | 이 논문에서 |
|---|---|---|
| **Anode-free (AF)** | 음극 활물질 없이 집전체에 Li 를 직접 도금 | 셀 구조 전체의 전제 |
| **Interlayer** | SE 와 집전체 사이 기능층 | Ag–C / AgNO₃–C / AgNO₃–C–PVP |
| **PVP** | poly(vinylpyrrolidone). 카보닐 O 가 금속이온과 배위 | Ag⁺ 배위 → 건조 중 이동 억제 |
| **CI-NEB** | climbing-image nudged elastic band. 이미지 사슬을 최소에너지경로로 이완시키고 최고점 이미지를 안장점으로 끌어올림 | LiC₆ 경로 생성 (7 images) |
| **구속이완 (constrained relaxation)** | 일부 자유도만 고정하고 나머지를 이완. 여기선 adatom **xy 고정 / z + 슬랩 자유** | Li₃N 장벽 (NEB 가 이 표면에서 실패해서 채택) |
| **IDPP** | image-dependent pair potential. NEB 초기 이미지를 직선보간 대신 쌍퍼텐셜로 만들어 겹침 방지 | LiC₆ NEB 초기화 |
| **UMA-oc20** | Meta FAIRChem 의 범용 MLIP. `oc20` = 표면 흡착종 태스크 | LiC₆ 경로 탐색. **Li₃N 에는 우리 규율상 사용 금지** |
| **Marzari–Vanderbilt smearing** | 금속계 점유수 스미어링. cold smearing 이라 엔트로피 외삽 오차가 작음 | 두 슬랩 공통, 0.01 Ry |
| **Coble creep** | 응력하 **입계확산**이 만드는 변형. 입경 d 에 대해 ∝ d⁻³ | Eq. (2) 1항, D_pore 로 스케일 |
| **Nabarro–Herring creep** | 응력하 **격자(벌크)확산** 변형. ∝ d⁻² | Eq. (2) 2항. 여기선 Coble 대비 ~10⁻³ 로 무시 가능 |
| **GITT** | 전류펄스 + 완화 반복으로 준평형 전압과 분극을 분리 | 1 mA cm⁻² 1 min + 1 h |
| **DRT** | 임피던스를 완화시간 τ 분포 γ(ln τ) 로 역변환. 겹친 반원을 분리 | R_SE / R_interface / R_CT,Li–Ag |
| **η_nucleation** | Li 핵생성 과전압. 증착곡선의 dip 깊이 | 10.1 → 7.2 mV |
| **CCD** | critical current density. 단락 없이 견디는 최대 전류밀도 | 계단식 증가 시험 |
| **HAADF-STEM** | 고각 환형 암시야 STEM. 대비 ∝ Z^~1.7 → 무거운 Ag 가 밝게 | AgNO₃ 도메인 크기 |
| **Stage-1 GIC / LiC₆** | 흑연 층간 모든 층에 Li 가 들어간 화합물. 리튬화 카본의 대표상 | DFT 비교 표면 |

---

## 17. 다음 액션 (우선순위)

| 순위 | 무엇 | 어디 |
|---|---|---|
| 1 | **Fig. 5d 캡션에 확정 문장 복원 + Li₃N 곡선 점선화** | §11-A1 |
| 2 | **§4.6 에 "QE 단일점" 한 문장 추가** (LiC₆ 0.290 의 출처 명시) | §11-A2 |
| 3 | **LiC₆ 값을 0.287 로 통일** + `diffusion.json` ↔ `li3n_barrier_origin.csv` 정합 | §11-A3 |
| 4 | **byline `~~` 잔재 제거** (제출 차단 요소) | §11-C1 |
| 5 | Fig. 3 의 **0.1C / 0.5C** 확정 · Abstract **"%p"** 수정 | §11-B1, B2 |
| 6 | `canonical_registry.json` 에 **0.118 / 0.287 등록** | §11-C6 |
| 7 | (리비전 대비) **6층 243원자 2점 테스트** — kb C2·C3 동시 해결 | §15-3 |

> 🔗 **관련 카드 (2026-11-16 한 줄 추가)**: [`kang2026_stress_regulated_li_plating_ag_c_cnf_hybrid_anode`](kang2026_stress_regulated_li_plating_ag_c_cnf_hybrid_anode.md) — 같은 랩 · 같은 장치 (PEEK Ø 13 mm · LPSCl 0.15 g · 하중 셀 분해능 0.01 MPa · 스택 20 MPa · 45 °C · 2.5–4.25 V): NCM811 ‖ Li ΔP 1.1 / 1.8 / 2.4 MPa · Ag–C/CNF ΔP 2.3 → 1.6 MPa — 이 카드의 ΔP 3.0 / 2.8 / 2.5 MPa 와는 양극 (NCA ↔ NCM811) · 인터레이어 · 공압착 압력 (400 ↔ 450 MPa) 이 달라 같은 표에 넣지 않는다.
