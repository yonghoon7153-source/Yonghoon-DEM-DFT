# Kim 2026 (Nature Communications, DOI 10.1038/s41467-026-73909-0) — 전하조작(charge-engineered) 셀룰로오스 나노피브릴 바인더로 PFAS-free 고로딩 양극

> slug `kim2026_charge_engineered_cnf_binder` · DOI `10.1038/s41467-026-73909-0` · type `experiment` · digested `2026-07-28` · status ✅
>
> ⓘ **정본 승격 2026-07-28** — 원본 `claude/stoic-knuth-NObVQ:docs/lit_kim2026_charge_engineered_cnf_binder.md`.
> 단일-서랍 규칙(CLAUDE.md)에 따라 이관 — 그전까지 DFT webapp 목록에 안 떴다.


**인용:** Sang-Woo Kim†, Nag-Young Kim†, Anseong Park, Jinho Ha, Cheol Bak, Yoojin Kim, Seong-Seok
Chae, Jung-Hui Kim, Sang-Cheol Nam, Chaoji Chen, **Yong Min Lee**, Jung-Il Choi, **Won Bo Lee\***,
**Sang-Young Lee\***, "Charge-engineered cellulose nanofibril binders for PFAS-free, high-loading
lithium battery positive electrodes", *Nature Communications* (2026),
DOI 10.1038/s41467-026-73909-0 (Article in Press / unedited). **Open Access (CC BY-NC-ND 4.0).**
접수 2025-09-09 / 게재확정 2026-05-22. †Sang-Woo Kim·Nag-Young Kim 동등기여.

**소속:** (1) Dept. of Energy & Chemical Engineering, **UNIST**(Ulsan 44919) — 제1저자 Sang-Woo Kim;
(2) Dept. of Chemical & Biomolecular Engineering, **연세대(Yonsei)**(Seoul 03772) — 교신 Sang-Young
Lee; (3) School of Chemical & Biological Engineering, **서울대(SNU)** — 교신 Won Bo Lee; (4) Dept. of
Battery Engineering, **연세대**; (5) Energy Materials Research Center, **POSCO Future M**(Sejong); (6)
School of Resource & Environmental Sciences, **우한대(Wuhan, China)** — Chaoji Chen; (7) School of
Mathematics & Computing(Computational Science & Engineering), **연세대**. 교신
wblee@snu.ac.kr; syleek@yonsei.ac.kr.

★★ **LEAD = Sang-Young Lee(연세대) + Won Bo Lee(서울대 — 분자모델/DFT) + UNIST(제1저자).** **Yong Min
Lee는 공저자**(연세대 Battery Eng.), DTBL 주도 논문이 아님 — #266/#285/#286(DTBL 핵심)보다 **협업·주변부**.

**소재계:** ★ **양극 활물질 = NCM811(LiNi₀.₈Co₀.₁Mn₀.₁O₂, LG Energy Solution) 액체전해질 LIB**. 바인더 =
**전하조작 셀룰로오스 나노피브릴 c-CNF**(목재 유래, 4급 암모늄 −N(CH₃)₃⁺ 양이온화)로 **PVDF 대체**. 도전재
= **carbon black Super C65(Imerys)** + 고로딩에선 **SWCNT(HCNT4, Cabot)**. 용매 = **에틸렌글리콜(EG, 비독성)**
— **NMP-free**. 전해질 1 M LiPF₆ EC/EMC 3:7(v/v) + 10 wt% FEC + 2 wt% VC(Enchem). 음극 = Li metal(100 µm,
Honjo) 또는 흑연(LG, 12.2 mg/cm²·porosity 31%). PE separator 20 µm.
★★ **우리 LPSCl sulfide ASSB가 아니다** — 분자스케일 바인더 화학 + 액체전해질 NCM811 LIB. 이 그룹의 **#282**
논문(`docs/literature_yonsei_dtbl_2026.md`) — **TIER-3(주변부 binder)** 갱신본.

**한 줄 핵심 변수:** **바인더 표면전하(b-CNF → a-CNF → c-CNF)** — bare CNF(중성·응집) → 알칼리 전처리로
음이온화 a-CNF → 4급 암모늄 그래프트로 **양이온 c-CNF(ζ ≈ +31.9 mV)**. 양전하가 (i) 슬러리에서 정전기
반발 → 분산 안정화, (ii) 건조 후 강한 수소결합 → 접착/구조 무결성. 비교군 = PVDF(중성, vdW 약결합).

**DB 동반 파일:** 이 논문은 **분자스케일 바인더 화학 + 액체전해질 NCM811 LIB** → `docs/data/*.csv`(densification
/porosity/σ 등) 수치 DB에 **추가하지 않음**. σ/porosity 절대앵커는 Bazzoun(LPSCl)·Varkey(halide)·Minnmann이
담당. DFT 보충데이터 16종(`scratchpad/si282_data/`) = **DFT 전하/ESP 데이터**(Gaussian cube `.cub`/`.txt`,
SCF density·정전기퍼텐셜; PVDF/b-CNF/c-CNF/TFSI/PF6/Cl 슬랩·이온 모델 — 본문 §4.4 참조). 대용량 trajectory는
파싱 불필요.

---

## ★ 한 문장 결론 — 이게 무엇이고 우리에게 (낮은) 관련성

**목재 유래 셀룰로오스 나노피브릴을 4급 암모늄으로 양이온화(c-CNF)하면, 슬러리에서 정전기 반발로 분산을
안정화하고 건조 후 강한 수소결합으로 접착·구조 무결성을 강화해, PFAS(PVDF)·NMP 없이도 초고로딩(113 mg/cm²)·
고밀도(3.65 g/cm³)·고면적용량(22.5 mAh/cm²) NCM811 양극을 만들 수 있다** — DFT(MEP/ESP·결합에너지)로 분자
근거를 세우고, 유변학·토모·EIS·full-cell로 검증.

**우리 프로젝트 관련성(낮음, TIER-3):** 이 논문은 **분자스케일 바인더 화학**(c-CNF 표면전하 엔지니어링) +
**액체전해질 LIB**다 — 우리 **LPSCl sulfide ASSB의 연속체/접촉망 DEM+MPM 압축·수송**과 소재·스케일·물리가
다르다. 접점은 **느슨한 맥락 3가지뿐**: (a) PFAS-free 바인더 = 우리 additives.py가 기하학적으로만 모델링하는
PTFE의 대안 맥락(우리는 바인더 화학을 모델링하지 않음); (b) 전하→분산 개념이 우리 CBD 분산균일도(E2)에 개념적
으로 인접하나 메커니즘이 다름(분자 표면전하 vs 기하 seeding); (c) 고로딩 양극 맥락. **셋 다 transport/압축/σ
앵커가 아니다** — 그건 Bazzoun/Varkey/Minnmann/#266이 담당. 관련성을 부풀리지 않는다.

---

## 1. 배경 / 동기 (Introduction, p.4–5)

- **PFAS 규제 강화 → PVDF 문제.** PVDF는 상용 전극 바인더의 지배종이나 (i) **불소화 조성(PFAS)** → 잔류·생물
  축적·독성 우려, (ii) **유독 용매 NMP** 의존, (iii) **기술적 한계** — 약한 vdW 상호작용·낮은 극성 →
  고로딩/고밀도에서 **계면접착 약함·응집(도전재 분산 불량)·박리·사이클 중 전기화학 열화**.
- 대안 바인더(합성 공중합체·알지네이트 등) 시도 있으나 **산업적 확장성 + 견고한 전기화학 성능**을 동시에 못
  주는 경우 多 — 바인더↔전극 성분 **분자수준 상호작용 이해 부족**이 원인.
- ★ **셀룰로오스 나노피브릴(CNF, 식물 유래)** — 재생가능·고종횡비·표면화학 조절가능·기계물성 우수. 그러나
  TEMPO 산화 CNF(TOCN)는 **수소결합 자리 과밀 → 취성 전극·이온수송 방해** → 진공여과·동결건조 같은 **비(非)
  슬러리 공정**에 의존(산업 슬러리 캐스팅과 비호환).
- **본 연구(명시):** **전하조작 CNF(c-CNF)** — 4급 암모늄(−N(CH₃)₃⁺)으로 기능화 → 슬러리에서 **정전기 반발로
  응집 억제·분산 안정화**, 건조 후 **NCM811·집전체와 강한 수소결합 → 접착·구조 강화**, 나노섬유 망이 **퍼콜
  네트워크 → 물리적 얽힘 기계보강 + 개방형 다공 → 전해질 침투·이온수송**. **NCM811 + 에틸렌글리콜(비독성
  용매) + R2R(roll-to-roll) 호환** → 고로딩(113 mg/cm²)·고밀도(3.65 g/cm³) 양극.

**약어:** CNF=cellulose nanofibril; b-CNF=bare(미개질); a-CNF=anionic(알칼리 전처리 알콕사이드);
c-CNF=charge-engineered(양이온 4급암모늄); AGU=anhydroglucose unit(셀룰로오스 반복단위); DS=degree of
substitution; CA=cationic agent; MEP=molecular electrostatic potential(=ESP); DFT=density functional
theory; DLVO=Derjaguin-Landau-Verwey-Overbeek 콜로이드 안정성 이론; 3ITT=three-interval thixotropy test;
t_Li+=Li⁺ transference number; DRT=distribution of relaxation times; CEI=cathode-electrolyte interphase;
BatPaC=Battery Performance and Cost 모델(Argonne).

---

## 2. 소재 & 제작 (Methods, p.27–34)

### 2.1 c-CNF 바인더 합성 (2단계 분자개질, Fig 2a)
- **원료:** CNF 현탁액(high-fines slurry, 고형분 3 wt%, University of Maine).
- **Step 1 — 음이온 중간체(a-CNF):** 1.0 wt% CNF를 **NaOH/urea(7:12 w/w)** 용액에 분산 → **4 °C 12 h 냉장**
  → −OH 부분 탈양성자화·**알콕사이드(−O⁻Na⁺) 생성** → 초음파(20 kHz, 800 W, 30 min). NaOH·urea가 수소결합
  donor/acceptor로 작용해 **섬유간 수소결합 교란 → 피브릴 부분 해체**.
- **Step 2 — 양이온화(c-CNF):** **(3-chloro-2-hydroxypropyl)trimethylammonium chloride(4급 암모늄 양이온제,
  CA)** 를 AGU 대비 정해진 몰비로 첨가 → **70 °C 8 h 교반** → c-CNF−Cl. 투석(5일, pH ~7.0) 정제.
- **음이온 교환:** c-CNF−Cl 0.2 g을 **2 M LiTFSI 수용액 20 mL**에 침지 70 °C 72 h → c-CNF−TFSI → 투석 →
  **동결건조(−120 °C 콘덴서, 3일)** → 최종 분말 바인더.

### 2.2 양이온화 최적화 (Fig 2e, Fig S1)
- CA:AGU 몰비를 ×12/×18/×24/**×30**/×36으로 스윕. **치환도 DS**(질소함량 N% 원소분석, DS = 162·N%/(14−151.5·N%))
  = **0.17 / 0.22 / 0.29 / 0.39 / 0.026**(×36에서 급락 — 과량 시 부반응/세척손실). **ζ-퍼텐셜** = 21.6/27.1/28.8/
  **31.9**/12.1 mV. ★ **CA:AGU = 30:1**이 콜로이드 안정성(ζ > +30 mV) + 반투명 균질 현탁액(Fig S2) → **최적**.
- c-CNF 나노피브릴 **평균 직경 ~38 nm**(HR-TEM, Fig 2e; b-CNF 불규칙 응집 → a-CNF 부분 해체 → c-CNF 균질 분산).

### 2.3 전극 제작 (Methods)
- **표준 c-CNF 양극:** 동결건조 c-CNF를 **EG**에 초음파 분산 → carbon black(Super C65) 첨가·vortex 10 min·
  bath sonication 30 s → NCM811 혼합. **NCM811 : carbon black : c-CNF = 97:2:1 (w/w/w)**. Al foil(20 µm)
  doctor blade → **120 °C roll-press + 120 °C 진공건조 12 h**. 펀칭 Ø10(0.79 cm²)/Ø14(1.54 cm²).
- **PVDF 대조군:** PVDF(280,000 g/mol, Solvay)를 NMP 용해 → NCM811·carbon black **96:2:2**.
- **고로딩 구성(Fig 7):** **NCM811 : SWCNT : c-CNF = 98.5:0.5:1 (w/w/w)** — **바인더 단 1 wt%**. 캐스팅·100 °C
  진공건조 12 h·roll-press → **밀도 3.65 g/cm³** 유지하며 **로딩 80/90/113 mg/cm²** 제작.
- **기본 로딩 = 40 mg/cm²**(별도 명시 없으면). 양극 두께 ~120 µm @40 mg/cm².

### 2.4 셀 조립 (Methods)
- **코인(2032):** c-CNF 또는 PVDF 양극 ‖ Li metal(100 µm), PE separator(20 µm, Toray-Tonen), Ar 글러브박스.
  표준 pouch(2×2 cm²) NCM811 ‖ Li metal, **N/P = 2.5**, dry room(dew point −60 °C), 공칭 0.033 Ah.
- 전해질 100 µL/coin·150 µL/pouch(E/C = 4.5 mL/Ah).
- **흑연‖NCM811 full-cell**(추가 사이클 검증), **면적용량 매칭 pouch**(PVDF 3 unit cell vs c-CNF 1 unit cell,
  총 ~0.44 Ah).

### 2.5 분석 (Methods)
- **구조/물성:** HR-TEM(ARM300, JEOL; ImageJ 직경분포), FE-SEM(SU-8100)+EDS, FT-IR(400–4000 cm⁻¹),
  CHNS 원소분석, XRD(Cu Kα), **인장시험**(필름 toughness/flexibility), ζ-퍼텐셜(Nano ZS, dilute 10 ppm
  in EG/NMP), **유변학(MCR 302, Anton Paar)**, **micro-CT(SKYSCAN 1273, voxel 5.0 µm — 슬러리 미세구조)**,
  **LSCM(FV1000, 표면 균질도)**, **FE-EPMA(JXA-8530F — 탄소 분포 매핑)**, FIB(cycled NCM811 단면), **XPS
  (ESCALAB 250XI, depth profile Ar⁺)**, ToF-SIMS, RM2610(HIOKI — bulk/계면 전기저항), peel-test(180° 접착),
  ⁷Li MAS NMR(600 MHz, 20 kHz), through-thickness Raman(E_g/A_1g — DOD 분포).
- **전기화학:** galvanostatic(3.0–4.3 V, 1C=200 mA/g), EIS(1 MHz–0.01 Hz, 14.1 mV), **t_Li+(Bruce-Vincent-
  Evans)**, GITT(0.5C 펄스+60 min 휴지), LSV(OCV→5.5 V), DRT, 대칭 blocking cell(R_ion).
- **DFT(§2.6 아래 §4.4):** **VASP, GGA-PBE, PAW, Γ-point, plane-wave cutoff 450 eV, EDIFF 1e−6 eV, σ=0.05.**
  진공 환경에서 바인더 상호작용 에너지 평가(보충데이터 1–2, 10–12). **MD**(Al₂O₃ 슬랩 결합에너지) 별도.

---

## 3. 핵심 메커니즘 — c-CNF가 PVDF를 이기는 4가지 축

**(1) 분산(슬러리): 정전기 반발 + 나노섬유 망.** c-CNF의 −N(CH₃)₃⁺ 양전하 → **DLVO 정전기 반발로 입자 응집
억제·콜로이드 안정화**. b/a/c-CNF·PVDF의 ζ = −12/−21/**+31.9**/−8 mV(c-CNF만 강한 양전하). 건조 후 나노섬유가
**수소결합으로 퍼콜 네트워크** → 높은 점도·항복응력 → **용매증발 중 수직 상분리(Peclet) 억제**(아래 §4.2).

**(2) 접착(건조 후): 강한 수소결합.** PVDF는 vdW 약결합 → 활물질·집전체와 약한 친화 → 박리. c-CNF는 NCM811·
Al과 **강한 수소결합** → 접착·구조 무결성. DFT: c-CNF −OH···−OH 결합에너지 **−0.64 eV** ≈ PVDF −F···H− **−0.07
eV**의 거의 한 자릿수↑. MD(Al₂O₃ 슬랩): c-CNF(N(CH₃)₃⁺···Al₂O₃) **−1193.8 kJ/mol** ≫ PVDF(F···Al₂O₃) **−530.26
kJ/mol**. → peel 접착 **157.3 N/m vs PVDF 14.2 N/m**(Fig S20, ~11×).

**(3) 이온수송(전해질 상호작용): 양전하가 PF6⁻를 잡고 Li⁺를 풀어준다.** c-CNF의 4급 암모늄이 액체전해질
**PF6⁻와 정전기 상호작용** → Li⁺를 음이온에서 해리·이동성↑. ⁷Li NMR downfield shift(−0.338 vs PVDF −0.471 ppm),
**t_Li+ = 0.83 vs PVDF 0.54**(필름, Fig S29). → 토르투오시티↓·MacMullin↓·침투깊이↑(아래 §4.3).

**(4) 고로딩 구조 무결성: 항복응력·calendering 내성.** 나노섬유 망의 높은 점도·항복응력 → 두꺼운 슬러리 안정
(h_max 2.73 mm vs PVDF 1.35 mm) + calendering 시 균일 응력 → **113 mg/cm²·3.65 g/cm³에서도 균열·박리 없음**.

⇒ 우리 식으로: **분자 표면전하(양이온)가 (분산↑ + 접착↑ + Li⁺ 이동↑ + 구조 무결성↑)을 동시 달성** — 모두
**바인더 화학**이 주체. 우리 모델은 이 화학을 다루지 않으며(우리 PTFE는 기하/부피/전자블로킹만), 따라서
**개념(전하→분산)만 멀리서 인접**, 수치·메커니즘 차용 없음.

---

## 4. 섹션별 결과 — 모든 수치 (Results, p.7–26)

### 4.0 헤드라인 수치 (Abstract + §"High-mass-loading", Fig 7)
| 지표 | c-CNF | PVDF(대조) |
|---|---|---|
| **Mass loading** | **113 mg/cm²**(최대) | 실용 한계 ~50 mg/cm²(균열·박리 @3.35 g/cm³) |
| **전극 밀도** | **3.65 g/cm³** | 3.35 g/cm³ |
| **면적용량** | **22.5 mAh/cm²** @113 mg/cm² | 실용 한계 ~8 mAh/cm² |
| **체적 에너지밀도** | **1781.5 Wh/L** | (경쟁) |
| **중량 에너지밀도** | **431.8 Wh/kg** @113 mg/cm² | — |
| **바인더 함량** | **1 wt%**(고로딩) / 1 wt%(표준) | 2 wt% |
- ★ **고로딩 + 고밀도 동시 달성**은 드물다 — 22.5 mAh/cm²(113 mg/cm²)에서 면적용량 **선형 스케일**(@0.05C ≈
  1.13 mA/cm²). 두께 80/90/113 mg/cm² → **225/260/320 µm**(Fig S39, 모두 균질·무균열).

### 4.1 c-CNF 합성·특성 (Fig 2)
- **HR-TEM(Fig 2b–e):** b-CNF 불규칙 응집 → a-CNF 부분 해체 → c-CNF **균질 분산, 평균직경 38 nm**.
- **FT-IR(Fig 2f–h, S3):** a-CNF에서 **C−O 신축(950–1050 cm⁻¹)** 출현(알콕사이드) + c-CNF **4급 암모늄 peak
  1477 cm⁻¹** → 양이온화 성공. O−H 신축(3800–3000 cm⁻¹) **광폭화** → 표면개질로 섬유간 수소결합 약화.
- **수소결합 디콘볼루션(Fig S4–S5):** O6−H···O3′ **분자간** 수소결합(peak 1) 비율이 b-CNF **32% → c-CNF 26%**
  (분자간 상호작용 교란·응집 감소). O2−H···O6 **분자내**(peak 3) 23→34% 증가.
- **XRD(Fig 2i):** native 셀룰로오스 Iβ → c-CNF **결정성↓ + (200)→(020) 변환**(격자 재배열).
- **기계물성(Fig 2j–k):** c-CNF 필름 **toughness 16.3 MJ/m³**(b/a-CNF 능가) + 고유연성(종이접기 origami 학
  반복 접힘에도 무결). → 용매증발·roll-press 응력 견딤.
- **LSV(Fig S7):** c-CNF 필름 전압안정창 ≈ PVDF(양극 작동전위 내 전기화학 안정, 5.5 V까지).

### 4.2 슬러리 유변학·분산 (Fig 3, Fig S9–S13)
- **모델 현탁액 ζ(Fig 3e, S8):** PVDF/b-CNF/a-CNF/**c-CNF** = −8/−12/−21/**+31.9 mV**(=Fig S8 −8/−12/−20.7/+31).
- **육안 분산(Fig S9):** carbon black + 바인더 모델 슬러리 — PVDF/b/a-CNF는 탄소 응집덩어리, **c-CNF만 균질
  검은 분산**.
- **유변학(Fig 3f, S11):** 고형분 76 wt% 슬러리(97:2:1 / 96:2:2). 둘 다 shear-thinning이나 **c-CNF가 뚜렷한
  비뉴턴 + thixotropy**. 진동 shear stress sweep G′/G″ 교차점(=항복응력) **c-CNF 120 Pa ≫ PVDF 0.2 Pa**
  (잘 발달한 점탄성 구조).
- **h_max(Fig S12):** 최대 안정 코팅높이 **c-CNF 2.73 mm ≈ 2× PVDF 1.35 mm**(h_max = τ_y/ρg).
- **3ITT(Fig 3g, S38):** c-CNF 거의 완전한 점도 회복(전단 후) vs PVDF 회복 불량.
- **micro-CT(Fig 3h):** PVDF 슬러리 국소 응집 vs c-CNF **균질·연속 입자 분포**.
- **캐스팅 형상유지(Fig 3i,j):** 2×2 cm² 몰드 — c-CNF 1분 후 **~92% 두께 유지** vs PVDF **~50%**(슬럼프).
- ★ **수직분리 물리(Peclet):** Pe = U/D₀·h. PVDF는 약 vdW·저점도 → **Pe ≫ 1 → 가벼운 바인더·도전재 상향
  이동 → 수직 불균일**. c-CNF 나노섬유 망 → 점도·항복응력↑ → 대류 억제 → **유효 Pe↓ → 균질**. Darcy(U=−k/μ·∇P)
  로도 점성저항↑ 확인. → **고로딩에서도 두께방향 조성 균일·무균열**.

### 4.3 전극 구조 균질성·전기/이온 수송 (Fig 4, Fig S14–S30)
- **BS-SEM/FE-EPMA 탄소분포(Fig 4c–h, S13):** PVDF 전극 **도전재·바인더 불균일 응집**(C Area% 최대 16) vs
  **c-CNF 균질**(최대 7.0 — 응집덩어리 없음).
- **표면에너지/접착일(Fowkes, 본문 Fig 4i + Table S1):** 접촉각(H₂O/DIM): PVDF 95.05°/60.60°, c-CNF
  53.01°/49.94°. γ_total **PVDF 29.79 → c-CNF 53.45 mN/m**(γᵖ 1.63 → 19.13 — 양이온화로 극성성분↑).
  **접착일(work of adhesion):**
  | 쌍 | PVDF | c-CNF |
  |---|---|---|
  | binder↔binder(cohesion) | 59.58 | **106.9** |
  | binder↔활물질(NCM811) | 78.40 | **107.1** |
  | binder↔도전재(carbon) | 77.56 | **103.6** |
  | binder↔집전체(Al) | 68.77 | **88.53** |
  ★ PVDF는 cohesion(59.58) < 활물질접착(78.40) → **불균형 → 바인더 자기응집·상분리**. c-CNF는 **세 접착일이
  cohesion(106.9)과 균형**(107.1/103.6) → **균질 분산·구조 안정**.
- **LSCM 표면 균질도(Fig S16):** 40 mg/cm²에서 PVDF 표면 비균일(±32 µm 편차) vs c-CNF 최소 변동(calendering
  내성).
- **접착 검증(Fig 4k, S19–S21):** peel 평균접착 **c-CNF 157.3 vs PVDF 14.2 N/m**(Fig S20); SAICAS 접착강도
  c-CNF ~750 vs PVDF ~540 N/m(Fig S21); 180° peel에서 **PVDF 박리·c-CNF 무박리**(Fig S19). 전해질 침지+초음파
  후에도 c-CNF 구조유지(Fig S22).
- **XPS depth profile(Fig 4j, S17):** c-CNF 전극 Ni peak 표면 854.9 → bulk 853.9 eV **이동**(4급 암모늄이
  Ni−O 격자 산소와 상호작용 → 국소 전자환경 변조). PVDF는 ~854.1 eV 변화 거의 없음(약 계면상호작용).
- ★ **전극 전기전도도(Fig 4k middle):** **c-CNF 0.23 S/cm > PVDF 0.16 S/cm**(연속 전자전도망). (주: 전극
  복합체의 거시 전도도이지 바인더 자체가 아님 — c-CNF 균질분산이 도전망을 더 연속화.)
- **유효 비표면적(GA 모델, Fig 4k right):** **c-CNF 16.19×10⁵ m⁻¹ ≫ PVDF 0.2591×10⁵ m⁻¹**(개방·상호연결망 →
  전해질 접근성↑; PVDF는 건조 시 응집·치밀화).
- **전해질 젖음(Fig 4l left, S23):** 접촉각 **c-CNF 12.80° < PVDF 27.80°**(양이온 표면화학 → 전해질 친화).
  ★ **porosity는 유사**(c-CNF 30.9% vs PVDF 29.7%) — 차이는 다공도가 아니라 **표면화학·분산**에서 옴.
- ★ **토르투오시티·MacMullin·침투깊이(Fig 4l, S24–S26):**
  | 지표 | c-CNF | PVDF | 식 |
  |---|---|---|---|
  | **토르투오시티 τ** | **~3.6** | ~6.8 | τ = R_ion·A·k·ε / 2d (EIS 대칭셀) |
  | **MacMullin N_M** | **~11.5** | ~23 | N_M = K_bulk/K_eff = τ/ε |
  | **침투깊이 L_d** | 더 깊음(@0.1C ~0.066 m) | (~0.034) | L_d = ε/τ · D₀C₀F/((1−t_Li+)I) |
  → c-CNF가 **이온경로 덜 우회 + Li⁺ 더 깊이 침투**(고전류·고로딩에서 유리).
- **EIS R_ion vs 로딩(Fig 5e, S30):** 20 mg/cm²에선 c-CNF≈PVDF, **30→40 mg/cm² 고로딩에서 c-CNF R_ion 뚜렷
  낮음**(고로딩일수록 차이↑). DRT(Fig 5f): c-CNF가 **전하전달저항·확산분극 모두 낮음**.

### 4.4 ★ DFT/MD 분자 모델링 (Fig 3b–d, Fig 5a–c, Fig S18, S28; 보충데이터 1–16)
우리 프로젝트의 (먼) 방법 관심사 — **DFT 전하/ESP 분석**.
- **방법:** **VASP, GGA-PBE, PAW, Γ-point, cutoff 450 eV, EDIFF 1e−6, σ=0.05**(진공). 분석 = **MEP(=ESP) 맵**
  (전자밀도 SCF에서) + **결합/자유에너지**. 보충 cube/txt 파일이 **Gaussian-cube 포맷 SCF density·ESP**:
  - 보충데이터 1(.cub): **PVDF** "Electron density from Total SCF Density"(원자 20).
  - 보충데이터 2(.txt): **1cCNF** "Electrostatic potential from Total SCF Density"(원자 43, O/C/H).
  - 보충데이터 10/11/12: **TFSI⁻**(원자 15, N·S·O·C·F) / **PF6⁻**(P 중심 6F) / **Cl⁻**(단원자) ESP.
  - 보충데이터 3–9, 13–16: 추가 SCF/ESP grid(대용량 — 본문 RDF/MD 부속).
- ★ **결과 1 — 분산(Fig 3b–d):** c-CNF의 **4급 암모늄 주위 강한 양전하 분포**(MEP) → PVDF보다 강한 정전기
  상호작용. **−OH···−OH 수소결합 −0.64 eV ≈ 10× PVDF −F···H− −0.07 eV.**
- ★ **결과 2 — 집전체 접착(MD, Fig S18):** Al₂O₃(집전체 native 산화막) 슬랩 위 결합에너지 ΔE: PVDF **−530.26**,
  CNF(6 repeat) −1060.87, **1 c-CNF(1 양이온기) −1204.8**, 2 c-CNF −1193.79 kJ/mol → c-CNF ≫ PVDF.
- ★ **결과 3 — 음이온 교환/Li⁺ 해리(Fig 5a–c, S28):** 4급 암모늄−음이온 쌍(Cl⁻/PF6⁻/TFSI⁻) 모델.
  - **MEP 평균값:** Cl⁻ −0.26, PF6⁻ −0.12, **TFSI⁻ −0.025**, c-CNF⁺ +0.29 Ha/e — TFSI⁻이 가장 약한(0에 가까운)
    음전위 → 큰 분자부피(점유부피 **TFSI 1268~2277 bohr³** vs PF6 735 vs Cl 332)에 저전위가 고르게 퍼짐 →
    **c-CNF에서 가장 쉽게 이탈** → 액체전해질 PF6⁻와 효율적 교환.
  - **이온교환 자유에너지 Δ(ΔG⁰)(Fig 5d, S28d):** **TFSI⁻ −46.7 kJ/mol**(PF6⁻로 자발 치환), Cl⁻ −3.9.
    → c-CNF−TFSI 설계 정당화(TFSI가 PF6⁻로 쉽게 교환되어 Li⁺ 이동 촉진).
- **검증:** FT-IR P−F peak 840 → 836 cm⁻¹(c-CNF 전극, PF6⁻와 정전기 상호작용); PF6⁻ RDF peak r=4.1 Å·높은 CN
  (c-CNF) vs 4.3 Å·낮은 CN(PVDF); **t_Li+ 0.83 vs 0.54**; ⁷Li NMR −0.338 vs −0.471 ppm(downfield = Li 염 해리
  촉진).

### 4.5 전기화학 성능 (Fig 6, Fig S31–S36)
- **PDE 전기화학 모델(Fig 5g–i, S31):** 실측 파라미터(τ·OCV·저항)로 다공전극 PDE(질량/전하보존, BV) — **GA로
  100회 파라미터 추정 → 확률밀도**. c-CNF가 **전 SOC에서 두께 전체 Li⁺ 농도↑**(전해질 접근성), 겉보기 Li⁺
  확산계수 최빈값↑.
- **율속(Fig 6a, S32–S33):** 120 µm·40 mg/cm² ‖ Li metal — c-CNF **면적용량 8 mAh/cm²·비용량 200 mAh/g_NCM811
  @0.1C**(NCM811 이론용량 근접). 0.2→1.0C에서 **고전류·고로딩일수록 c-CNF 우위 뚜렷**.
- **사이클(Fig 6b, S34):** c-CNF 용량유지↑(Li metal 교체 시 c-CNF 회복 → 열화는 Li metal 탓). 흑연‖NCM811
  full-cell **300사이클 후 ~88% 유지 > PVDF ~80%**(Fig S42).
- **post-mortem(Fig 6c–f, S35–S36):** Through-thickness Raman E_g/A_1g — PVDF는 **두께방향 산화환원 불균일**
  (표면집중 리튬화), c-CNF는 **거의 일정**(균질 DOD). F 1s XPS CEI(Li_xPO_yF_z 686.7 eV) c-CNF↓(부반응 억제),
  ToF-SIMS 부산물↓. cycled NCM811 — **PVDF 심한 균열**(불균일 산화환원·국소 전류밀도 → 응력집중) vs **c-CNF
  균열 억제·결정성 유지**(Fig S36 HR-TEM/FFT).
- **고로딩(Fig 7):** 98.5:0.5:1(SWCNT)로 80/90/113 mg/cm² — 3.65 g/cm³ 유지·무균열, 면적용량 22.5 mAh/cm²
  까지 선형. SWCNT는 c-CNF가 **noncovalent π–π로 균질 분산**(Fig S37, Raman D/G upshift).
- **셀설계/비용(Fig 7g–i, S41):** 동일 0.44 Ah pouch — PVDF 3 unit cell(80 mg/cm²) vs **c-CNF 1 unit cell
  (240 mg/cm² double-stack)** → **셀 두께 −51%·무게 −27%**(비활성부품↓). BatPaC(72 Ah, 흑연‖NCM811):
  면적용량↑ → 제조에너지 −22.3%·셀비용 −5.8%.

---

## 5. 그림 한 장씩 — 무엇을 보이고 (우리는 거의 안 씀)

### 본문 Figures
- **Fig 1:** 개념도(a) + 고로딩 전극/성능 요약(b) — PFAS-free c-CNF 전략·113 mg/cm²·3.65 g/cm³.
- **Fig 2:** c-CNF 합성·특성 — (a) 2단계 분자개질, (b–e) HR-TEM(38 nm), (f–h) FT-IR(1477 cm⁻¹·O−H), (i) XRD,
  (j) toughness 16.3 MJ/m³, (k) origami 유연성.
- **Fig 3:** ★ DFT+유변학 — (a) Peclet/DLVO 모식, **(b) c-CNF MEP 맵**(양전하), **(c,d) 수소결합 −0.64 vs
  −0.07 eV**, (e) ζ −8/−12/−21/+31.9, (f) G′/G″ 항복응력 120 vs 0.2 Pa, (g) 3ITT, (h) micro-CT, (i,j) 캐스팅
  형상유지 92 vs 50%.
- **Fig 4:** 전극 구조 — (a,b) PVDF 불균일/c-CNF 균질 모식, (c–h) BS-SEM/EPMA 탄소분포, **(i) 접착일(Fowkes)**,
  (j) XPS Ni depth, **(k) 전도도 0.23/0.16·비표면적 16.19/0.2591×10⁵**, **(l) 토르투오시티 ~3.6/6.8·MacMullin
  11.5/23·접촉각 12.8/27.8°**.
- **Fig 5:** ★ 이온수송 분자기전 — **(a) 4급암모늄−PF6⁻ 모식**, (b) FT-IR P−F 840→836, (c) PF6⁻ RDF, (d) ⁷Li
  NMR, (e) R_ion vs 로딩, (f) DRT, (g–i) PDE 모델·Li⁺ 농도·확산계수 PDF.
- **Fig 6:** 전기화학 — (a) 율속, (b) 사이클, (c,d) through-thickness Raman E_g/A_1g(c-CNF 균질 DOD), (e)
  ToF-SIMS CEI, (f) cycled NCM811 균열(PVDF) vs 무균열(c-CNF), (g) pouch 이론용량 근접.
- **Fig 7:** 고로딩·셀설계 — (a) 로딩 vs 면적용량, (b–e) 80/90/113 mg/cm² 무균열·선형용량, (f) 에너지밀도 vs
  면적용량(밀도 3.0/3.35/3.65), (g,h) 셀 두께 −51%·무게 −27%, (i) BatPaC 비용.

### SI 주요(스킴): S1 DS/ζ, S2 현탁액 사진, S3–S5 FT-IR/수소결합(32→26%), S6 필름 SEM, S7 LSV, S8 ζ(+31),
S9 모델슬러리 분산, S11 유변, S12 h_max 2.73/1.35, S13 EPMA C, S14–S15 접촉각/표면에너지, S16 LSCM,
S17 XPS survey, **S18 MD Al₂O₃ 결합(−1204.8/−530.26)**, S19–S21 접착(157.3/14.2), S22 침지 무결성,
S23 전해질 접촉각, **S24 토르투오시티 6.8/3.6**, **S25 MacMullin 23/11.5**, S26 침투깊이, S27 GITT,
**S28 음이온 MEP/부피/ΔG(TFSI −0.025/2277/−46.7)**, S29 t_Li+ 0.54/0.53/0.63/**0.83**, S30 EIS vs 로딩,
S31 PDE workflow, S32–S33 율속곡선, S34 사이클(n=3), S35 F1s CEI, S36 cycled NCM811 HR-TEM, S37 SWCNT
π–π, S38 SWCNT 슬러리 유변, S39 단면 225/260/320 µm, S40 로딩별 사이클, S41 셀설계/비용, S42 흑연 full
300cyc 88/80%.

---

## 6. 기술 미니용어집 (우리 맥락)

- **c-CNF(charge-engineered CNF):** 4급 암모늄(−N(CH₃)₃⁺)으로 양이온화한 셀룰로오스 나노피브릴 바인더(직경
  ~38 nm). 양전하 → 분산(정전기 반발) + 접착(수소결합). 우리엔 직접 대응 없음(우리는 PTFE를 기하로만 모델).
- **DS(degree of substitution) / ζ-퍼텐셜:** DS = AGU당 양이온 치환 정도(N% 원소분석); ζ = 콜로이드 표면전하
  지표. CA:AGU 30:1에서 DS 0.39·ζ +31.9 mV 최적. 우리 morphology엔 표면전하 축 없음.
- **MEP/ESP(molecular electrostatic potential):** DFT 전자밀도에서 계산한 분자 정전기퍼텐셜 맵(전자풍부=red,
  결핍=blue). c-CNF 양전하·음이온 이탈성 평가. = 우리가 안 하는 분자스케일 DFT(우리 DFT-DEM은 입자스케일).
- **work of adhesion(Fowkes/OWRK):** 접촉각(극성+비극성 액)으로 표면에너지를 분산γᵈ·극성γᵖ로 분해 →
  두 상 부착일 W_adh. c-CNF는 활물질·도전재·집전체·자기 접착일이 균형(~107/104/89/107) → 균질·접착. 우리
  `--coh`(SE 부착)와 같은 "계면 부착" 물리축이나 **그들은 바인더-전극 접착, 우리는 SE-SE/SE-AM**.
- **t_Li+(transference number, Bruce-Vincent-Evans):** 전류 중 Li⁺ 기여분율. c-CNF 0.83 > PVDF 0.54(양이온이
  PF6⁻ 잡고 Li⁺ 풀어줌). 우리 ASSB는 단일이온(SE) 전도체 → t_Li+≈1 자명, 직접 대응 없음.
- **토르투오시티 τ / MacMullin N_M:** 이온경로 우회도(τ = R_ion·A·k·ε/2d) / N_M = τ/ε = K_bulk/K_eff.
  c-CNF τ~3.6·N_M~11.5 < PVDF 6.8/23. ★ **우리 σ_ionic의 C(τ) 항과 같은 변수**지만 **그들은 액체전해질
  pore τ**(전해질이 채운 다공경로), **우리는 SE 입자 접촉망 τ**(고체) — 물리·정규화 다름 → 폼/수치 차용 금지.
- **Peclet 수 Pe = U·h/D₀:** 슬러리 건조 시 대류(상향)/확산 경쟁 → Pe≫1이면 가벼운 바인더 상향분리. c-CNF
  망이 점도↑→Pe↓→균질. 우리는 건조 슬러리 동역학을 모델 안 함(압축만).
- **CEI / E_g/A_1g Raman:** cathode-electrolyte interphase(부산물); E_g/A_1g 강도비 = Ni-rich 층상 리튬화도
  지표(두께방향 산화환원 균질도). 우리 ASSB transport엔 CEI/산화환원 축 없음.
- **PFAS / PVDF:** per/polyfluoroalkyl substance(불소화 잔류물질); PVDF = 대표 불소 바인더. c-CNF가 PFAS-free
  대체. → 우리 `additives.py`의 **PTFE(역시 불소계, PFAS)** 와 같은 "불소 바인더" 범주 — 단 우리는 PTFE를
  **기하 피브릴**(nucleate_frac으로 carbon에 co-locate)로만 모델, 화학·PFAS는 안 다룸.

---

## ★ 7. 비교 vs 우리 DEM+MPM — 짧고 정직하게 (TIER-3 / 주변부)

⚠ **대전제:** 이 논문은 **분자스케일 바인더 화학(c-CNF 표면전하 엔지니어링) + 액체전해질 NCM811 LIB**다.
우리 모델은 **LPSCl sulfide ASSB의 연속체/접촉망 DEM+MPM 압축 + 수송(Kirchhoff/Holm σ triad)**다. **소재
(셀룰로오스 바인더·NCM811·액체전해질 ≠ LPSCl SE·NMC811·무전해질), 스케일(분자 DFT ≠ 입자 DEM/연속체 MPM),
물리(바인더 화학·전해질-매개 Li⁺ ≠ 고체 접촉전도)** 가 전부 다르다. **Yong Min Lee는 공저자(주도 아님)** →
DTBL 핵심 #266/#285/#286과 달리 협업·주변부. **수치 σ/porosity 앵커가 절대 아니다** — 그건 Bazzoun(LPSCl)·
Varkey(halide)·Minnmann(LPSCl cold-press)·#266이 담당한다. **관련성을 부풀리지 않는다.**

### 접점은 맥락 3가지뿐 (모두 모델 영향 없음)

**(a) PFAS-free 바인더 = 우리 PTFE의 대안 맥락 (맥락만).**
- 그들: **c-CNF가 PVDF(PFAS·불소계)를 대체** — 환경·접착·분산 이점.
- 우리: `scripts/additives.py`가 **PTFE 피브릴**(역시 PFAS·불소계)을 **기하학적으로만** 모델(nucleate_frac=0.6
  으로 carbon에 co-locate, 부피·전자블로킹). **바인더 화학·PFAS·접착일을 모델하지 않는다.**
- 판정: **순수 맥락**. "우리가 모델하는 PTFE도 PFAS이고, 산업계는 c-CNF 같은 PFAS-free 바인더로 가는 중"이라는
  배경 인지일 뿐. **우리 모델에 c-CNF/바인더화학을 넣을 계획 없음**(우리는 transport/압축, 바인더 화학 아님).

**(b) 전하→분산 개념 = 우리 CBD 분산균일도(E2)에 개념적 인접 (메커니즘은 다름).**
- 그들: **분자 표면전하(4급 암모늄 양이온)** → DLVO 정전기 반발 → 도전재/활물질 균일분산(ζ +31.9, micro-CT·
  EPMA 균질). 분산 정량 = ζ·유변학·EPMA 탄소맵·토르투오시티.
- 우리(`docs/cbd_morphology_roadmap.md` E2): CBD 분산을 **기하 seeding**(SuperP distributed vs VGCF concentrated,
  PTFE surface_frac/nucleate_frac)으로 모델 — 분산 균일도를 **morphology 좌표·근접도**로 본다.
- 판정: **개념적으로만 인접**(둘 다 "분산이 좋으면 균질 수송망"). 그러나 **메커니즘이 완전히 다르다** — 그들은
  **분자 표면전하/콜로이드**, 우리는 **기하 입자 배치**. 그들의 ζ·DLVO·Peclet은 **슬러리 건조 동역학**(우리가
  모델 안 하는 단계)에 산다. ⇒ **수치·폼·메커니즘 전이 없음**. 굳이 멀리서 얻을 것은 "분산 균일도를 단일
  수치로 정량(EPMA 탄소 Area% 공간분포)" 한다는 **측정 프레임**뿐인데, 이는 이미 #284(Oh 2026, SSRM)가 더
  직접적으로 제공한다(#284가 이온/전자 trade-off·분산정량의 주 공급원, 이 논문 아님).
- ★ 명확화: **이 논문은 #284와 달리 우리 CBD ion/electron trade-off의 독립확증이 아니다.** #284는 "탄소↑→전자
  ↑·이온↓ 중간최적"을 보여 우리 SuperP-vs-VGCF와 같은 긴장을 확증했지만, 이 논문은 **바인더(c-CNF vs PVDF)
  교체**이지 도전재 trade-off가 아니다 — c-CNF는 분산↑·접착↑·t_Li+↑·전도↑를 **동시에** 개선(trade-off가 아니라
  all-win). 우리 CBD 작업과 직접 대응하는 긴장이 없다.

**(c) 고로딩 양극 맥락 (배경만).**
- 그들: 113 mg/cm²·3.65 g/cm³·22.5 mAh/cm² 초고로딩 양극(액체 LIB).
- 우리: 고로딩 thick electrode 압축·수송이 관심사이나 **ASSB(고체)** — 그들의 액체전해질 고로딩 한계(Peclet
  수직분리·전해질 침투)는 **우리 ASSB에 없는 문제**(전해질이 없음; 우리는 SE-network σ가 지배).
- 판정: **배경 인지만**. 고로딩이 중요하다는 공통 동기일 뿐, **압축/σ 메커니즘 전이 없음**.

### 우리 우위 / frame[5] (간단)
- 그들: **분자 DFT(MEP/결합에너지) + 액체전해질 LIB 실험 + 다공전극 PDE(전해질-매개)**. 강력하지만 **입자스케일
  압축역학 없음·explicit 접촉 σ triad 없음·소성 morphology 없음·압력→미세구조→σ 예측 없음**(우리 DEM+MPM 영역).
- 우리: **압력→미세구조→σ(ionic/e/thermal) 예측 + MPM 소성 void-fill + voxel FV + fracture**. 그들의 분자 DFT는
  우리 입자스케일 모델과 **스케일이 달라 상보조차 아님**(우리 DFT-DEM은 입자접촉, 그들 DFT는 분자결합).
- ⇒ **이 논문은 우리 파이프라인의 입력단도 출력단도 아니다.** 순수 문헌 맥락(PFAS-free 바인더 동향 + 분산
  개념의 먼 인접). **모델 하자/검증/앵커 어느 것도 아님.**

### 비교 요약표
| 축 | Kim 2026 (#282, c-CNF/NCM811·액체) | 우리 (LPSCl ASSB, DEM+MPM) | 판정 |
|---|---|---|---|
| 소재·스케일 | 셀룰로오스 바인더(분자 DFT) + 액체 LIB | LPSCl SE+NMC811 입자 접촉망 | ⚠ 전부 다름 — 전이불가 |
| PFAS-free 바인더 | c-CNF가 PVDF 대체 | PTFE(PFAS)를 기하로만 모델 | 맥락만(우리 PTFE도 PFAS 배경) |
| 분산 | 분자 표면전하(ζ+31.9, DLVO) | 기하 seeding(SuperP/VGCF/PTFE) | 개념 인접·메커니즘 다름·수치 전이 無 |
| 이온/전자 trade-off | **없음**(c-CNF all-win) | SuperP 전자 vs VGCF 이온 | ✗ 대응 안 됨(#284가 그 역할) |
| 토르투오시티 τ | 액체 pore τ(3.6/6.8) | 고체 SE 접촉망 τ(C(τ) 항) | 변수명만 같음·물리 다름·차용 금지 |
| 고로딩 | 113 mg/cm² 액체 양극 | thick ASSB 압축·σ | 배경 동기만 |
| DFT | 분자 MEP/결합에너지(VASP) | 입자스케일 DFT-DEM | 스케일 달라 상보 아님 |
| 수치 앵커 | ✗ (분자·액체) | Bazzoun/Varkey/Minnmann/#266 | **앵커 아님** |

---

## ★ 8. 우리 작업에 넣을 인사이트 — 정직하게 거의 없음

1) **모델 영향 0 — 순수 문헌 맥락 강화.** 이 논문은 우리 DEM+MPM transport/압축 어디에도 꽂히지 않는다(분자
   바인더 화학 + 액체 LIB). 가치는 **"PFAS-free 바인더 동향(우리가 기하로 모델하는 PTFE의 대안)" + "전하→분산
   이라는 개념이 우리 CBD 분산(E2)에 멀리서 인접"** 이라는 **배경 인지**뿐. **수치·폼·메커니즘 전이 없음.**

2) **#284와 혼동 금지 — 이건 trade-off 확증이 아니다.** CBD ion/electron trade-off 독립확증 + 분산정량법
   (SSRM/W_adh) + balance-point 개념은 **#284(Oh 2026)** 가 공급한다. 이 논문(#282)은 **바인더 교체(c-CNF vs
   PVDF)** 로 분산·접착·t_Li+·전도를 **동시 개선**(trade-off 아님)이라 우리 SuperP-vs-VGCF 긴장과 대응 안 됨.

3) **DFT 스케일 구분 명확화(상보 아님).** 그들 DFT = **분자 MEP/결합에너지(VASP, 바인더-음이온/Al₂O₃)**.
   우리 DFT-DEM = **입자스케일**. 둘은 스케일이 달라 cross-validation도 division-of-labor도 아니다 — 단지
   "둘 다 DFT를 쓴다"는 표면적 공통점. 우리 transport DFT 앵커(σ_grain Cronau 등)와 무관.

### 보너스 실행 항목
- **#282 인덱스 갱신**(아래 완료): web-abstract → 검증 수치(c-CNF ζ+31.9·DS0.39·직경38nm; 로딩 113 mg/cm²·
  밀도 3.65 g/cm³·면적용량 22.5 mAh/cm²·1781.5 Wh/L·431.8 Wh/kg; t_Li+ 0.83 vs 0.54; τ 3.6 vs 6.8; W_adh
  107.1/103.6 vs 78.40/77.56; 결합 −0.64 vs −0.07 eV·Al₂O₃ −1204.8 vs −530.26 kJ/mol; 흑연 full 300cyc
  88/80%; DFT=VASP-PBE MEP/ESP)로 교체. **TIER-3 유지.**
- ⚠ **역할 구분(혼동 금지):**
  - **#282(이 논문, c-CNF/NCM811·액체):** **PFAS-free 바인더 맥락 + 전하→분산 개념 인접**. 분산정량법·trade-off
    확증·수치앵커 **아님**. 모델 영향 0.
  - **#284(Oh, SiOx/흑연·액체):** CBD ion/electron **trade-off 독립확증 + 분산정량(SSRM/W_adh) + balance point**.
  - **#285(Hong, 단결정 NCMA·액체):** rigid-AM 검증 + 점탄성 spring-back 미구현 한계.
  - **#286(Yoo, 흑연·액체):** Phase 5 z-구배 + 토모 정량(τ/PNM) + 전기화학시뮬 workflow.
  - **σ/porosity 절대앵커는 Bazzoun(LPSCl)·Varkey(halide)·Minnmann이 담당.**
- DFT 보충데이터(`scratchpad/si282_data/`)는 **분자 DFT 전하/ESP**(Gaussian cube) — 우리 입자스케일과 무관 →
  파싱·DB화 불필요(노트만 유지).
