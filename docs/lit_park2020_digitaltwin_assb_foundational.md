# Park 2020 (Adv. Energy Mater. 10, 2001563) — Digital-Twin-Driven All-Solid-State Battery: 물리·전기화학 거동 규명 ★ DTBL 디지털트윈 계보의 시조(FOUNDATIONAL ROOT, 2020)

**인용:** Joonam Park, Kyu Tae Kim, Dae Yang Oh, Dahee Jin, Dohwan Kim, **Yoon Seok Jung\***, **Yong Min Lee\***,
"Digital Twin-Driven All-Solid-State Battery: Unraveling the Physical and Electrochemical Behaviors,"
*Advanced Energy Materials* **10** (2020) 2001563.  DOI **10.1002/aenm.202001563**.  Received 2020-05-08 ·
Revised 2020-06-19 · Published online 2020-07-26.  © 2020 WILEY-VCH.

**소속:** J. Park, D. Jin, D. Kim, Prof. Y. M. Lee — **DGIST** 에너지과학공학(yongmin.lee@dgist.ac.kr, 당시; 이후 연세
DTBL).  K. T. Kim, Dr. D. Y. Oh, Prof. Y. S. Jung — **한양대학교** 에너지공학(yoonsjung@hanyang.ac.kr).
⚠ 출판본 1쪽 본문 주소블록은 K.T.Kim/D.Y.Oh/Y.S.Jung을 한 곳에서 **"Yonsei University"**, 다른 곳에서 **"Hanyang
University"**로 동시에 표기(출판사 조판 오류).  SI·저자 정정란은 **Hanyang**이 정본 — 본 디제스트는 **Hanyang**으로 기록.

**소재계:** ★★★ **LiNbO₃-coated LiNi₀.₇₀Co₀.₁₅Mn₀.₁₅O₂(NCM711) + Li₆PS₅Cl(LPSCl) + NBR(nitrile butadiene
rubber) 바인더 = 우리 DEM+MPM corpus와 정확히 같은 SE·CAM 계열.**  (#266 NCWA·#271 NCM·Bazzoun NMC811과 함께 LPSCl
+Ni-rich 군; 이 논문이 그 중 가장 이른 2020 시조.)

**이 디제스트의 위상(WHY 특별한가):** 이 논문은 **Yong Min Lee 그룹 디지털트윈-ASSB 프로그램 전체의 발원지**다.
#18(Kim 2024 ACS EL, `lit_kim2024_digital_twin_acsenergyletters.md`)이 명명·체계화한 **top-down/reconstruction(구조
재구성) + 확률/규칙기반 입자배치** 방법론의 **첫 ASSB 적용**이며, #271(Hong 2026 LPSCl 양극)·#266(Oh 2026 bimodal)·
#281(Kim 2026 Li-O₂ Phase-4 결합)·#286(Yoo 2026 z-gradient)·2023 Battery Energy(SIC-SPE/LPSCl, "이른 시드")로
이어지는 GeoDict 라인의 **계보 뿌리(2020)**.  ⇒ positioning 관점에서: **창립 디지털트윈 논문조차 "압축을 시뮬레이션"하지
않고, 측정된 PSA/SEM에서 입자를 규칙기반 배치**해 구조를 만든다(아래 §2).  우리 DEM+MPM의 **공정-물리 bottom-up(압력·
조성에서 구조를 *계산*)**은 이 계보의 뿌리에 대한 상향식 진보 — frame[5]의 가장 깊은 positioning 근거.

DB 동반 후보: `docs/data/densification_porosity_db.csv`(직접 porosity 행 없음 — 이 논문은 압력 sweep 없는 "최소 porosity"
규칙배치라 Heckel 앵커 아님; 대신 §9 참고) · 새 `docs/data/park2020_sigma_vs_ncm.csv`(σ_e/σ_ionic vs NCM wt% 디지타이즈
trend, 후보).

---

## ★ 한 줄 결론 — 이건 우리 계보의 시조이자, "규칙기반 배치(structure-placed)"의 원형이다

2020년 시점에 "**디지털 트윈 ASSB**"라는 개념 자체를 처음 구현한 논문.  핵심 주장 3단:
1. **신뢰성 있는 3D 디지털트윈 전극을 빠르게 생성** — PSA(입도분석)+SEM에서 NCM 이차입자의 울퉁불퉁한 형상과 LPSCl을
   규칙기반으로 배치(GeoDict GrainGeo) → 목표 부피분율 대비 **±2% 오차**, random seed 1–5로 재현성 확보.
2. **실험 불가능한 시공간 분해 정보**(dead particle, specific contact area, charge distribution)를 추출 + Ohm's law
   정상상태 시뮬로 **유효 전자/이온 전도도**를 NCM 60/70/80/90 wt% 4조성에서 계산 → 실험과 대조.
3. **3D 디지털트윈 위에서 전기화학(mass transport + Butler–Volmer 계면반응)** 시뮬 → 전압·SOC·과전압·rate·시공간
   lithiation을 풀고 실험 방전과 대조.

**우리 입장(frame[4]/[5]):**
- **같은 소재계(LPSCl+NCM711)·같은 조성축(AM:SE 60:38→90:8 = 우리 P:S/AM% sweep)** → **frame[4] 교차검증 표적**.
  단 그들 σ는 **intrinsic σ × 구조** 출력(from-scratch 접촉망 추론 아님) → **추세·자릿수만 비교, 점대점 절대 앵커 아님**
  (절대 σ 앵커는 Bazzoun/#271/Varkey/Minnmann/#266 유지).
- **NCM 60–80 wt% 최적창 + 90 wt% 이온-퍼콜레이션 실패 + dead-particle-vs-조성 + σ_e↑/σ_ionic↓-with-NCM** 4개 결론이
  **우리 AM:SE sweep·σ_ionic/σ_e 폼과 직접 1:1**.
- **"LPSCl은 변형성(deformable)이라 AM 간극에 위치 → 최소 porosity·충분한 Li⁺ 퍼콜레이션"** 규칙(아래 §2 3단계) =
  우리 **MPM 소성 void-fill을 *물리적으로 계산*하는 것의 2020 *언어적 진술***.  그들은 규칙으로 *놓고*, 우리는 압력에서
  *흐르게 한다*(frame[5]).
- **σ_e 방향(audit #11):** 이 논문은 **NCM wt%↑ → 유효 σ_e↑**(전자전도 재료=NCM이 늘어서) / **NCM wt%↑ → 유효 σ_ionic↓**
  (이온전도 재료=LPSCl이 줄어서) — **둘 다 "전도재료 부피분율"이 지배하는 intrinsic-σ-driven 방향**.  우리 σ_e는 입자수·
  접촉수(contact-network-driven)가 지배 → **작은 NCM서 σ_e↑**가 표면상 반대로 보일 수 있음.  정밀 해석은 §7-(σ_e방향)에서.

---

## §1. 동기 / 배경 (Introduction, p1–2)

**디지털 트윈의 계보.** 저자들은 디지털 트윈을 David Gelernter의 *Mirror Worlds*(1991)에서 출발, 2000년대 Michael Grieves가
제조공정에 도입 → 기계·열·유체 시뮬(자동차 충돌, 열교환기, 항공기 날개)에 광범위 검증된 기법으로 소개.  ★ 그러나 **전기화학
시스템의 디지털화는 아직 미달성** — 다차원의 복잡한 미분방정식 다수를 풀어야 하기 때문.  하드웨어·소프트웨어 발전으로 이제
가능해졌다는 것이 동기.

**리튬이온 배터리에서의 선례와 그 한계.** Newman 그룹의 연속체 모델이 복잡한 물리현상을 효과적으로 에뮬레이트했으나,
**pseudo-x dimension(x=2,3,4) 접근은 국소영역 문제를 시뮬할 수 없어 완전한 디지털트윈이 아니다**(p1 우측).  이 한계가 ASSB처럼
전극/셀 설계에서 국소 문제를 찾아야 하는 시스템에서 더 심각해짐 → **3D 구조-분해(structure-resolved) 디지털트윈**의 필요성.

**ASSB 동기.** 황화물 SE ASSB는 고에너지밀도·안전성의 유망 post-LIB.  Samsung이 argyrodite SE로 0.6 Ah 프로토타입 파우치
(>900 Wh/L, >1000 cycle @0.5C, 60°C) 보고 → 트윈 디지털화로 셀 성능 최적화·상용화 가속이 시급.

**선행 디지털트윈-ASSB 연구의 공백(p2 좌측, 직접 인용 가치).** 저자들이 정리한 7개 선행연구와 각 한계:
- **Bielefeld et al.**(ref 8): 연결입자 이용률(utilization)로 AM:SE 최적비 점검; **구·구 단순형상 + 전기화학 미시뮬**.
- **Shi et al.**(ref 10): 재료비·입경 함수로 cathode 이용률·용량손실 역산; **정밀 형상 미반영 + 전기화학 미시뮬**.
- **Ito et al.**(ref 11): phase-field로 현실 계면 3D 전극 + 전압·SOC·과전압 수치화; **3D 디지털트윈에선 미시뮬**.
- **Park et al.**(ref 12, 이 그룹 선행): SEM에서 실 전극 구조 복사 + 전기화학 변수(전압·SOC·유효전도도·접촉면적) 예측.
- **Finsterbusch / Neumann et al.**(ref 13,14): oxide(LLZO 등) SE 전극을 SEM/X선 토모 3D 재구성 + 전기화학 시뮬.

⇒ **남은 두 과제**: (i) 신뢰성 높은 디지털트윈 구조 제작, (ii) 시뮬↔실험의 낮은 편차.  이 논문이 둘 다 푼다고 주장 →
**"genuine digital twin model에 기반한 시뮬·실험 결과를 동시 보고한 첫 논문"**(p3, 저자 자평).

**이 논문의 3대 기여(p2 본문):**
1. 황화물 ASSB 전극(NCM711 이차입자 + LPSCl + NBR)의 **실제 제작공정**을 제안.
2. **디지털트윈 전극을 활용**해 셀 성능 직결 핵심물성을 분석하는 방법론 도입(specific value로 구조 검증).
3. 황화물 SE 디지털트윈-ASSB를 **셋업·전기화학 거동 예측**, 시뮬↔실험 대조로 신뢰성 확증.

---

## §2. ★ 디지털트윈 전극 구축 방법 — 규칙기반 배치(structure-placed), GeoDict GrainGeo (p2 + Experimental p8)

이 절이 positioning의 핵심.  **본문(p2)의 개념적 4단계 + Experimental(p8)의 실제 알고리즘**을 합쳐 기록.

### 본문 4단계(p2 우측, 개념)
1. **temporary globular(임시 구형) AM** 을 PSA 데이터를 반영해 3D 도메인에 그린다.
2. **polyhedral primary AM(다면체 1차입자)** — SEM에서 크기 확인 — 을 기존 구형 객체 위에 흩뿌려서 실 이차입자의 형상을
   모사(기존 구형 객체는 제거).  ⇒ **울퉁불퉁한 secondary-particle 형상을 다면체 1차입자 군집으로 재현**.
3. ★★ **"LPSCl은 가압 공정 중 변형성(deformable)이므로, PSA 크기를 반영해 AM 입자들의 간극(interspace)에 위치시킨다.
   따라서 최소 porosity를 만들면서 Li⁺ 퍼콜레이션 경로를 충분히 생성 — 이것이 비활성 void 수를 제한하는 핵심"**(p2 직접
   인용).  ⇒ **압축 물리 시뮬이 아니라, "변형성 SE는 빈틈을 채운다"는 규칙으로 SE를 배치**.
4. **NBR 고분자 바인더**를 모든 입자 사이에 추가.

### Experimental 실제 알고리즘(p8, GeoDict GrainGeo)
> "the **GrainGeo module in GeoDict 2020** was used and the formation process was as follows:" (p8 직접 인용)
- **0.5 µm edge cubic voxel**, random seed 1–5.
- ① PSA 데이터로 **uniform spherical NCM** 객체 생성(50×50×~39 µm 도메인).
- ② SEM 분석 기반 **polyhedral primary AM**을 ①의 구형 객체 위에 위치 → ①(구형) 제거(= 다면체 군집만 남김 = bumpy 형상).
- ③ PSA 기반 **spherical LPSCl 입자**를 다면체 NCM 구조와 겹치게 배치 → **겹친 AM 객체 부피는 유지하면서 LPSCl을 AM 간극에**.
- ④ **polymeric binder(NBR)** 추가 → composite 전극 완성.
- **periodic function**으로 잘린 입자 부피를 반대편에 생성(작은 입자 substitution 없이 whole-particle 보존).

★ **분류(#18 taxonomy):** **top-down/reconstruction(측정 PSA·SEM에서 구조 재구성) × stochastic/rule-based placement
(확률·규칙 배치)** — #263(separator 확률 3D)과 같은 부류.  **process-physics-driven compaction이 아님**(압축 역학을 풀지
않음).  ⇒ ★ **시조 디지털트윈조차 "press를 시뮬"하지 않고, 규칙으로 입자를 놓는다.**

**신뢰성 주장(p2 우측 + Fig 1d):**
- **±2% 부피분율 오차** — 5개 seed 평균 부피분율이 목표값(Fig 1a 상단)에 ±2% 이내(Fig 1d).
- random seed 1로 생성, seed 2–5(Fig S3)도 같은 조성이면 유사한 미세구조 특징 → 국소영역 해석의 한계를 극복하고 모델링·
  시뮬에서 발생하는 허용오차를 추정하기 위해 반복 필요.
- Fig 1b(3D)↔Fig 1c(2D 디지털 토모그래피)↔Fig S4(실 FESEM)로 morphology 대조 → 신뢰성 입증.

### 재료·셀 파라미터(Experimental, p8–9)
- **재료 밀도:** NCM 4.44 g/cm³(입자 porosity 32.7%), LPSCl 2.07, NBR 1.00 g/cm³.
- **전극설계 4조성(wt%):** NCM:LPSCl:NBR = **60:38:2 / 70:28:2 / 80:18:2 / 90:8:2**.  로딩 **10 mg/cm²**, 두께 **~39 µm**,
  전극밀도 **2.5–2.6 g/cm³**.
- **PSD(Fig S1):** NCM·LPSCl 둘 다 **secondary particle 피크 ~8–10 µm**, 꼬리 ~30 µm까지(거의 겹침; LPSCl가 약간 좁고
  높음).  ⚠ 이 논문은 LPSCl을 **이차입자 ~8 µm 크기 구**로 다룸 — 우리·Bazzoun·#266의 **D50 ~0.7–1.5 µm 작은 SE와 다름**
  (2020 시점 SE 입도 모델이 큼; 아래 §10 전이경계).
- **NCM 1차입자 크기(Fig S2 SEM):** 565 nm ~ 1.55 µm(657 nm, 745 nm, 790 nm, 1.04/1.06 µm 등 표기).
- LiNbO₃ 코팅 0.5 wt%(습식, lithium ethoxide + niobium ethoxide).  LPSCl: Li₂S+P₂S₅+LiCl 볼밀(600 rpm 10 h)+550°C 5 h 어닐.
- 전극 슬러리: dibromomethane 용매, doctor-blade, 60°C 진공건조.  전도도용 Ni-foil, 전기화학용 C-coated Al-foil.

---

## §3. ★ Dead particle 분석 — 물리적으로 고립된 입자 vs NCM wt% (Fig 1, Fig S6/S7)

**Dead particle = 주변 동종 재료에서 물리적으로 고립된 입자**(= 우리 dead-AM / f_AM^cc / ionically-vulnerable AM, SE쪽은
SE-퍼콜레이션 실패).  부피분율%로 정량(seed 1–5).

### NCM(AM) dead particle (Fig S6)
| NCM wt% | seed1 | seed2 | seed3 | seed4 | seed5 | 경향 |
|---|---|---|---|---|---|---|
| 60 | 0.94% | 0.20% | 0.00% | 0.37% | 0.43% | 최대 ~0.94% |
| 70 | 0.00% | 0.05% | 0.00% | 0.00% | 0.17% | |
| 80 | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | |
| 90 | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0% |
→ **NCM dead particle은 NCM wt%↑ → 감소**(60wt%서 최대 ~1%, 90wt%서 0%).  이유: **NCM이 많을수록 stochastic
connectivity↑**(AM끼리 더 자주 닿음).  최대 부피분율 <1% → **전기화학 악영향 marginal**(p2 우측).

### LPSCl(SE) dead particle (Fig S7) ★ 핵심
| NCM wt% | seed1 | seed2 | seed3 | seed4 | seed5 | 경향 |
|---|---|---|---|---|---|---|
| 60 | 0.00% | 0.02% | 0.00% | 0.00% | 0.00% | ~0% |
| 70 | 0.00% | 0.00% | 0.00% | 0.00% | 0.06% | <0.1% |
| 80 | 0.28% | 0.28% | 0.41% | 0.28% | 0.41% | ≤0.5% |
| 90 | **19.82%** | **7.65%** | **9.56%** | **6.16%** | **6.20%** | ★ 급증 6–20% |
→ **LPSCl dead particle은 NCM wt%↑(=LPSCl↓) → 증가**, 단 **NCM 80wt%까지 ≤0.5%**, **NCM 90wt%에서 ~6–20%로 급증**
(seed1 19.82% 최악, 나머지 6–10%).  이유: LPSCl이 적어 서로 고립.

### ★ 저자 결론(p2 우측, 직접 인용 가치)
> "these data indicate that the **compositional design range from NCM 60 to 80 wt%** (i.e., from LPSCl 38 to 18 wt%)
> **is appropriate** to achieve minimal dead particles within the all-solid-state electrode."

⇒ ★ **최적 설계창 = NCM 60–80 wt% (LPSCl 38–18 wt%)** — **dead particle 최소.**  NCM 90 wt%(LPSCl 8 wt%)는 LPSCl
고립 급증으로 부적합.

**= 우리 dead-AM/SE-퍼콜레이션과 1:1.** 우리 dead-AM warning(f_AM^cc<80%)·SE-no-perc(σ_ionic=0) degenerate 케이스가
이 NCM 90wt%(SE 8wt%) 코너에 정확히 대응.

---

## §4. ★ 유효 전자/이온 전도도 vs NCM wt% (Fig 2a,b + Table S1 + Fig S9/S10, Ohm's law)

**방법(Fig S9, Ohm's law 정상상태):** 디지털트윈 구조에서 NCM(전자) / LPSCl(이온) 상을 각각 추출, 도메인 한 면 φ=1V·
반대면 φ=0(Dirichlet jump ΔV=1V), 나머지 면 절연:
```
j = (ε_s·σ_s / τ_s)·∇φ_s   [전자, NCM]      (Fig S9 식1)
j = (ε_e·σ_e / τ_e)·∇φ_e   [이온, LPSCl]    (Fig S9 식2)
σ_eff = (ε·σ_intrinsic)/τ   ← 부피분율 ε × intrinsic σ ÷ tortuosity τ
```
⇒ ★ **σ_eff = intrinsic σ를 (부피분율/tortuosity)로 가중한 출력** — **from-scratch 접촉망 추론이 아님**(우리 Kirchhoff/
Holm과 정보론적 위상 다름; §7 cross-validation에서 강조).  GeoDict **ConductoDict + explicit jump(EJ) solver**(porous
구조에 적합), σ는 Open/Closed porosity 제거 후 활성 입자에만.

**Table S1 — intrinsic 전도도(입력값):**
| 재료 | 전자 σ (S/cm) | 이온 σ (S/cm) |
|---|---|---|
| NCM | **8.5×10⁻⁴** | 0 |
| NBR | 0 | 0 |
| LPSCl | 0 | **−4.45×10⁻³·ε_s + 4.64×10⁻³** (s = 4.64×10⁻³ S/cm) |
⚠ LPSCl 이온 σ는 ε_s(AM 부피분율) 의존 식 — AM이 많을수록 LPSCl이 받는 압력↓로 σ_intrinsic↓을 반영한 보정식(문헌 기반,
ref 18a-c).  NCM 전자 σ=8.5×10⁻⁴ S/cm는 **NCM711 문헌값**(우리 σ_AM(e)=50 mS/cm 기준값과 다른 출처·낮음).

### ★ 결과(Fig 2a,b) — 시뮬 vs 실험, NCM wt% 함수
- **Fig 2a 유효 전자 σ(σ_eff,e):** **NCM wt%↑ → 증가**.  시뮬(빨강 영역 = seed 1–5 spread)이 실험(빨강 ▲)을 잘 포괄.
  log(σ_eff,e) ≈ −4.5 ~ −3 (S/cm) 범위, NCM 60→90wt%로 단조 상승.
- **Fig 2b 유효 이온 σ(σ_eff,ion):** **NCM wt%↑ → 감소**.  시뮬(파랑 영역) ↔ 실험(파랑 ▼) 일치.  log(σ_eff,ion) ≈ −3 ~ −4
  (S/cm), NCM 60→80wt%로 단조 하강.
- ★★ **NCM 90 wt%의 유효 이온 전도도는 계산 불가** — "**the effective ionic conductivity values of the NCM 90 wt%
  electrodes could not be calculated due to disconnected percolation pathways between LPSCl particles (Figure S10)**"
  (p2 우측 직접 인용).  Fig S10은 dead particle 제거 후에도 LPSCl 망이 끊긴 5개 seed를 보임 → **퍼콜레이션 실패**.
- **저자 종합:** "logical trends that the effective conductivity range depends on the amount of corresponding conductive
  materials" + "simulated conductivity range(색칠 면적)가 conductive material↓ 할수록 커진다(분산↑)".

⇒ ★ **방향 정리(audit #11 핵심):**
- **σ_eff,e ↑ with NCM wt%** ← **전자 전도재료(NCM) 부피분율↑** (intrinsic-σ-driven, 부피분율 지배).
- **σ_eff,ion ↓ with NCM wt%** ← **이온 전도재료(LPSCl) 부피분율↓** (intrinsic-σ-driven).
- **NCM 90 wt% σ_eff,ion = N/A** (LPSCl 퍼콜레이션 실패 = 우리 σ_ionic SE-no-perc degenerate).

**= 우리 σ_ionic 폼과 1:1**(SE↓→σ_ionic↓→퍼콜 임계 아래서 0).  **σ_e 방향은 §7-(σ_e방향)에서 우리 contact-network-driven과
대조** — 그들은 부피분율 지배(연속체 voxel), 우리는 입자수·접촉수 지배(이산 접촉망).

---

## §5. ★ Specific contact area vs NCM wt% (Fig 2 본문 + Fig S8)

**Specific contact area = NCM-LPSCl 접촉 비표면적(1/m, = 우리 coverage / A_AM-SE).**  GeoDict PoroDict로 Minkowski
measure(부피·표면·적분평균곡률) 통계분석 산출.

### 결과(Fig S8)
- **NCM wt%↑ → specific contact area 단조 감소**: ~**95,000 → ~35,000 1/m** (NCM 60→90wt%, max/min seed 밴드).
  (60wt% ~78,000–97,000 / 80wt% ~55,000–62,000 / 90wt% ~30,000–40,000 1/m, w/dead vs w/o-dead 밴드.)
- ★ **dead particle 유무의 영향은 insignificant** — w/ dead(검정 점선)와 w/o dead(빨강 점선) 밴드가 거의 겹침(특히 NCM
  60–80wt%; 90wt%서만 살짝 벌어짐).  "the dead particle effect is insignificant in our electrode conditions"(p2 우측).
- **물리 해석:** NCM↑ → LPSCl↓ → AM-SE 계면 면적↓ → **전기화학 반응 site↓**.  이것이 **NCM 80wt% rate 저하의 근본 원인**
  으로 이후 전기화학 절에서 반복 인용(§6, §8 — Fig 3 specific capacity 감소 + Fig 6 과전압 증가의 구조적 뿌리).

⇒ **= 우리 coverage(Stage-E Hertz/Tabor) / A_AM-SE.**  "NCM↑ → contact area↓ → 반응site↓ → rate↓"는 우리 coverage→
전기화학 연결의 2020 원형.

---

## §6. ★ Charge / current distribution — 전자 vs 이온 흐름 (Fig 2c–f + Fig S11/S12)

**방법:** 같은 Ohm's-law 시뮬 결과를 charge density(mA/cm²) colormap으로 3D 가시화.  ⚠ **전극에 도전탄소(conductive
carbon)를 넣지 않음** — "the electrodes did not contain conductive carbon materials to enhance the connectivity for the
NCM particles"(p3 우측).  즉 NCM 자체 전자전도로만.

### 결과(Fig 2c–f, charge density 0–100 mA/cm²)
- **Fig 2c(NCM 60wt%) vs 2d(NCM 80wt%) 전자밀도(NCM 상):** ★ **NCM 80wt%가 더 나은(높은·균일) 전자밀도** — AM이 많아
  연결 좋음.  "the NCM 80 wt% exhibits better electron density over the same domain than NCM 60 wt%."
- **Fig 2e(NCM 60wt%) vs 2f(NCM 80wt%) 이온밀도(LPSCl 상):** ★ **NCM 60wt%가 훨씬 높은 이온밀도 + 더 넓은 공간영역에
  분포** — LPSCl 많아 연결 좋음.  "the NCM 60 wt% has a much higher ion density across more spatial regions."
- **종합(p3 우측):** NCM 80wt%(LPSCl 20wt%)는 이온경로가 **전자경로보다 더 국소화(localized)** → 이온이 병목.
- **Fig S11(20 mA/cm² 이상 영역만 추출):** (a) NCM 60wt% 전자밀도 / (b) NCM 80wt% 이온밀도 — 임계 전류밀도 이상 부피만
  refined volume으로 가시화.  **Fig S12(80 mA/cm² 이상, NCM 80wt% 이온):** 더 높은 임계서 이온경로가 **더 제한적·간신히
  연결**.  ⇒ "when the ionic current density in NCM 80 wt% is cut by over 80 mA/cm², the ionic pathway becomes more
  limited or only slightly connected."

⇒ **저자 결론:** "the blending ratios of NCM to LPSCl should be carefully designed to ensure favorable electronic and
ionic pathways."  intrinsic σ(전자=NCM·이온=LPSCl)에 따라 optimum 조성이 달라진다.

**= 우리 percolation·current-density-thresholded analysis와 동형.** 임계 전류밀도 이상 부피 추출 = 우리 backbone/병목 식별.

---

## §7. ★ 전기화학 시뮬레이션 — 3D 디지털트윈 위 mass transport + Butler–Volmer (Fig 3–6 + Fig S13–S17) ★ Phase-4 ANCESTOR

이 절이 우리 `docs/stage4_electrochem_research.md`(Phase-4 전기화학 결합)의 **가장 이른 조상**.

### 셀 구조 & 지배방정식(Fig S13, BatteryDict / GeoDict Design Battery)
> "the function of **Design Battery in a BatteryDict of GeoDict 2020** was used for the set-up of a digital twin cell"
> (p9 직접 인용)
- **stacked cell(Fig S13):** lithium metal(3 µm) | LPSCl separator(30 µm) | **NCM/LPSCl/NBR 전극** | aluminum(1.5 µm),
  직렬.  voxel 0.5 µm(전극), 0.01 µm급은 아님.  30°C, C-rate 0.1/0.5/1C.
- ★ **지배방정식(Fig S13, 직접 전사 — 우리 Phase-4 이식용):**
  ```
  Butler–Volmer 계면 전류밀도(식3):
     j_se = 2k·√(c_s·c_e·(c_max − c_s))·sinh[ (φ_s − φ_e − E_eq)·F/(2RT) ]
  계면 경계조건(식4,5):  J_s·n = j_se ,   J_e·n = j_se
  AM 질량보존(식6):       ∂c_s/∂t = ∇·(D_s·∇c_s)
  전해질 질량보존(식7):    ∂c_e/∂t = ∇·(D_e·∇c_e) − ∇·(t₊·J_e/F)
  전해질 전류(식8):        ∇·J_e = ∇·[ σ_e·(1−t₊)·(RT/F)·∇log c_e ] − ∇·(σ_e·∇φ_e)
  AM 전류(식9):           ∇·J_s = −∇·(σ_s·∇φ_s)
  비활성(pore·binder) 상: no-flux(절연); 셀 외곽 경계: no-flux.
  ```
- ★ **모델 파라미터(Table S2, 직접 전사):** D_s=3.0×10⁻¹⁵ m²/s, D_e=1.2×10⁻¹³ m²/s, k(BV rate)=1.0×10⁻⁷ A·m^2.5·mol^−1.5,
  σ_s=8.5×10⁻⁴ S/cm, σ_e=−4.45×10⁻³·ε_s+4.64×10⁻³ S/cm, c_s,max=47054 mol/m³, c_e=46276 mol/m³, **t₊=0.99**(LPSCl 단일이온
  근사), I_1C=2.625×10⁻⁹ A, T=303.15 K.  E_eq(SOC) = 6-가우시안 합 OCV 피팅(Table S2 식).
- ★ **단일이온 도체 가정(p5 우측):** "the inorganic solid electrolyte is a single-ion conductor with a transference
  number of approximately **0.99–1**" → LPSCl 내 농도구배 무시, **flux density**로 이온 이동 분석.  ⇒ 우리 LPSCl t₊≈1과 동일.

### Fig 3 — 전압-용량 프로파일(seed 1–5, 0.1/0.5/1C)
- **(a–c) NCM-기반 gravimetric capacity**(NCM 60/70/80wt%), **(d–f) electrode-기반 areal capacity**.  같은 C-rate서
  seed 변동은 미세(디지털트윈 신뢰성 재확인).
- ★ **검증(Fig S14):** 우리 시뮬 비용량이 여러 선행 실험 데이터(ref 15a-d, 다양한 조성·로딩)와 유사.  ★ **"우리 모델의 1C
  평균 용량편차 = ~11 mAh/g, 다른 디지털트윈 모델 기반 연구는 1C서 >12.5 mAh/g(특히 고율 ~80 mAh/g)"** → **더 정확**(p4
  우측).  이유: 더 정교한 미세구조 + 사전점검된 유효 전자/이온 전도도.  NCM 70wt% 전극/LPSCl/Li-In 셀을 같은 조건 실측 대조.
- ★ **specific capacity ↓ with NCM wt%**(Fig 3a–c): "considerable specific capacity reduction is observed as the NCM
  content increases from 60 to 80 wt%, **even at the lowest C-rate of 0.1C, as high as 20 mAh/g, equivalent to 15%**."
  ← **specific contact area↓**(Fig S8) 때문.  고율일수록 NCM 80wt% 용량비↓ 더 큼 = **낮은 contact area + 낮은 유효 이온
  전도도** 결합효과.
- **areal capacity(Fig 3d–f):** NCM 70·80wt%가 60wt%보다 0.1C서 약간 높은 areal capacity(절대 질량↑).  단 C-rate↑면 NCM
  고함량 전극 용량 급락 → "an electrode design with a higher NCM content is not effective under high C-rate conditions."

### Fig 4 — 시공간 lithiation(NCM 80wt%, 방전 마지막, 0.1/0.5/1C)
- **SOC ∝ AM 내 lithium 농도**(반비례).  **저율(0.1C):** 잘 분포된·균일한 lithiation; **중/고율(0.5/1C):** 불균일.
- **Fig 4a–c**(3.0V 종지) **vs 4d–f**(3.5V): NCM 70wt%가 80wt%보다 더 균일한 lithiation(Fig S15 보강).  ★ **In-depth 분석
  (Fig S16):** LPSCl separator에 가까운 NCM 입자가 더 많이 재리튬화 → "sufficient effective electronic conductivity"
  근거.  같은 전압(~3.5V)서도 저율선 우수한 lithiation 분포·밀도.  ⇒ **AM이 완벽히 리튬화/탈리튬화 안 됨** — SE 입자가
  이차입자 내부까지 침투 못해 농도 과전압↑.  해결책 제시: **나노렙 SE 사용 + AM 격자제어로 Li⁺ 확산성↑**.

### Fig 5 — 이온 flux(NCM 70 vs 80wt%, 방전 마지막, 0.1/1C)
- ★ LPSCl이 단일이온(t₊≈0.99–1)이라 농도구배 없음 → **flux density**로 분석.  중성전하 균형 → 전류밀도↑면 ion flux↑ 자연증가.
- ★ **"the ion flux from the 80 wt% electrode is higher and less uniform than 70 wt%"** ← NCM↑ → 더 높은 ion flux로
  몰림 + LPSCl↓ → **narrower·more complicated ion pathway** → **higher ohmic resistance in SE 망**(mass transport
  limitation).  ⇒ "new SE materials with higher intrinsic ionic conductivity and better deformation property for
  minimizing the tortuosity"가 필요(직접 인용 — ★ **"deformation property"가 SE 변형성=우리 MPM 소성 void-fill의 가치**).

### Fig 6 — surface overpotential(전기화학 반응 site, NCM 70 vs 80wt%, 방전 마지막, 0.1/1C)
- ★ **NCM 70wt%:** 저율 과전압 ≪ 고율.  **NCM 80wt%:** 저율 과전압이 이미 상당히 높음(고율과 비슷).  Fig S17(충전 후, 양수
  과전압)도 유사.
- ★ **저자 결론(p6 좌측, 직접 인용 가치):** "These significant surface overpotential values can be correlated to the
  **relatively low specific contact area** in comparison to the amount that required for the electrochemical reaction
  to proceed.  Thus, from the perspective of mass transport and electrochemical reaction rate kinetics, these analysis
  data visually demonstrate **why the rate capability of the 80 wt% electrode was poor**."  ⇒ **NCM 80wt% rate 저하 = 낮은
  contact area + 높은 과전압**.  해결: LiNbO₃/halide 코팅·도핑으로 계면 반응속도↑·부반응↓.

### Fig 7 — ASSB 설계 파라미터 맵(전망)
- electrolyte(입경·코팅두께·porosity·두께), Li metal(코팅·표면형상·두께), cathode(전극밀도·로딩·**component ratio
  20%/40%/60%/80%**·입경형상) — ★ **"Attempted in this work" = cathode component ratio(=우리 AM:SE sweep)**.  나머지는
  미래 디지털트윈 확장 축.

⇒ ★ **Phase-4 이식 레시피:** Fig S13 식3–9(BV+질량보존+전류) + Table S2 파라미터 + 단일이온(t₊≈1) flux 근사 + "핵심전극=
구조분해, 보조도메인=연속체" + "방전부터 검증, 동역학 파라미터 고정·구조변수만 변화"가 **우리 PyBaMM DFN(τ·σ 주입) Phase-4의
2020 원형**.  #281(Kim 2026 Li-O₂, COMSOL 1D)·#17(Song 2025, structure-resolved)이 이 라인의 후손.

---

## §8. SI 그림·표 총정리 (Fig S1–S17 + Table S1/S2)

| 항목 | 내용 | 우리 대응 |
|---|---|---|
| **Fig S1** | NCM·LPSCl PSD(이차입자, 둘 다 피크 ~8–10µm, 꼬리 ~30µm) | PSD 입력 — ⚠ LPSCl 8µm는 우리 0.7–1.5µm와 다름(2020 큰 SE) |
| **Fig S2** | NCM 이차입자 단면 FESEM(1차입자 565nm–1.55µm 표기) | 다면체 1차입자 형상 근거 |
| **Fig S3** | NCM 60/70/80/90wt% 디지털트윈, seed 2–5(4×4 그리드) | random-seed 재현성(우리 multi-seed) |
| **Fig S4** | (a) NCM 70wt% 디지털 토모 vs (b) 실 NCM 70wt% FESEM | 모델↔실측 morphology 대조 |
| **Fig S5** | NBR 3D 구조, NCM 60/70/80/90wt% × seed 1–5 | 바인더 분포(저함량이라도 고른 분포) |
| **Fig S6** | NCM dead particle %, 60/70/80/90wt% × seed1–5 (§3 표) | dead-AM vs 조성 |
| **Fig S7** | ★ LPSCl dead particle %, 90wt%서 6–20% 급증(§3 표) | SE-퍼콜레이션 실패 vs 조성 |
| **Fig S8** | ★ specific contact area vs NCM wt%(95k→35k 1/m), w/·w/o dead 거의 겹침 | coverage / A_AM-SE; dead 영향 무시 |
| **Fig S9** | 전자/이온 density 도메인+지배식(Ohm's law, j=εσ/τ·∇φ)+BC | σ_eff 시뮬 셋업(연속체 voxel) |
| **Fig S10** | ★ NCM 90wt% dead 제거 후에도 끊긴 LPSCl 망 5 seed | σ_ionic SE-no-perc 시각증거 |
| **Fig S11** | (a)NCM 60wt% 전자밀도 (b)NCM 80wt% 이온밀도, >20 mA/cm² 추출 | 임계 전류밀도 backbone |
| **Fig S12** | NCM 80wt% 이온밀도 >80 mA/cm²(더 제한적) | 고임계 병목 |
| **Fig S13** | ★ stacked cell(Li/LPSCl/전극/Al) + 전기화학 지배식3–9 | Phase-4 지배식 원형 |
| **Fig S14** | ★ 방전용량 시뮬 vs 실험(여러 ref 15) — 1C 편차 ~11 mAh/g | frame[4] 셀-수준 검증 |
| **Fig S15** | NCM 70wt% lithiation(0.1/0.5/1C 방전 마지막) | 시공간 lithiation |
| **Fig S16** | NCM 80wt% >80% lithiation 부분부피(separator 근접 NCM↑) | 두께방향 불균일 |
| **Fig S17** | NCM 70·80wt% 충전 후 과전압(양수, 0.1/1C) | 과전압-contact area 상관 |
| **Table S1** | ★ intrinsic σ: NCM 전자 8.5×10⁻⁴ / LPSCl 이온 4.64×10⁻³ S/cm | σ 입력값(intrinsic-driven 근거) |
| **Table S2** | ★ 모델 파라미터+OCV식(D_s/D_e/k/c_max/t₊=0.99/E_eq…) | Phase-4 파라미터 세트 |

---

## §9. 핵심 수치 한눈 요약 (검증·DB 후보)

- **조성표(wt% → vol%):** NCM:LPSCl:NBR = 60:38:2(35.1:47.7:5.2) / 70:28:2(40.4:34.7:5.1) / 80:18:2(45.0:21.7:5.0) /
  90:8:2(49.4:9.4:4.9).  ★ **NCM vol% = 35.1/40.4/45.0/49.4%** = 우리 AM vol% sweep 대역.  로딩 10 mg/cm², 두께 ~39 µm,
  전극밀도 2.5–2.6 g/cm³.
- **dead particle:** NCM <1%(60wt%서 max ~0.94%, 90wt% 0%); **LPSCl ≤0.5%(60–80wt%) → 90wt%서 6–20%**(stated, Fig S6/S7).
- **σ_eff,e:** NCM wt%↑ → 증가, log ~ −4.5→−3 S/cm(Fig 2a, 시뮬≈실험; 디지타이즈 TREND).
- **σ_eff,ion:** NCM wt%↑ → 감소, log ~ −3→−4 S/cm(Fig 2b); **NCM 90wt% = N/A(퍼콜 실패)**.
- **specific contact area:** ~95,000 → ~35,000 1/m(NCM 60→90wt%, Fig S8); dead 영향 무시.
- **specific capacity:** NCM 60→80wt%서 0.1C서도 ~20 mAh/g(~15%)↓; 1C 평균 용량편차 ~11 mAh/g(타 모델 >12.5).
- **intrinsic σ:** NCM 전자 8.5×10⁻⁴ S/cm, LPSCl 이온 4.64×10⁻³ S/cm(=4.64 mS/cm), t₊≈0.99.
- ⚠ **digitized-from-figure(TREND only):** σ_eff,e/σ_eff,ion 절대값(Fig 2a,b log 스케일)·contact area 밴드·전류밀도 맵.
  **stated-in-text:** dead particle %(Fig S6/S7 라벨)·조성표·intrinsic σ(Table S1/S2)·specific capacity Δ·1C 편차.
- ★ **DB 후보(직접 추가 안 함):** `park2020_sigma_vs_ncm.csv` — NCM 60/70/80/90wt% × {σ_eff,e, σ_eff,ion, contact_area,
  NCM_dead%, LPSCl_dead%}, 단 σ는 **intrinsic×구조 출력 + digitized → TREND·자릿수 reference**(절대 앵커 아님; densification_
  porosity_db.csv의 Heckel 앵커와 성격 다름 — 이 논문은 압력 sweep·porosity 직접보고 없음).

---

## §10. ★ 비교 vs 우리 DEM+MPM (frame[4]/[5]) — 시조와의 교차검증 + positioning

### (1) frame[4] 교차검증 — 같은 소재계·같은 조성축
| 축 | Park 2020 | 우리 DEM+MPM | 판정 |
|---|---|---|---|
| 소재 | LiNbO₃-NCM711 + LPSCl + NBR | **동일 SE·CAM 계열 ✓** | 같은 계 |
| 조성축 | NCM 60/70/80/90wt%(AM 35–49vol%) | AM:SE sweep(case_3d_collection) | **같은 축 ✓** |
| 구조생성 | GeoDict GrainGeo 규칙배치(top-down/reconstruct) | DEM packing+압축(bottom-up/predict) | ★ 우리가 상향식 |
| σ_eff 산출 | intrinsic σ × ε/τ (연속체 voxel, Ohm) | Kirchhoff/Holm 접촉망(from-scratch) | 위상 다름(§아래) |
| dead particle | NCM<1%·LPSCl 90wt%서 6–20% | dead-AM f_AM^cc·SE-no-perc | **1:1 ✓** |
| 최적 조성창 | **NCM 60–80wt%(LPSCl 38–18wt%)** | dead-AM warning·σ 코너 회피 | **1:1 ✓** |

★ **교차검증 결론 4건:**
1. **NCM 60–80wt% 최적창** ↔ 우리 dead-AM warning(f_AM^cc<80%)·degenerate 케이스 회피 구간.  **방향·코너 일치.**
2. **NCM 90wt% 이온-퍼콜레이션 실패(σ_eff,ion=N/A, Fig S10)** ↔ 우리 **σ_ionic SE-no-perc degenerate**(σ_ionic=0,
   예: 2mAh_real_16/8mAh_real_11).  **같은 물리 — SE 너무 적으면 LPSCl 망 끊김.**
3. **LPSCl dead particle vs 조성(90wt%서 6–20%)** ↔ 우리 SE-퍼콜레이션 취약 케이스의 조성 위치.
4. **σ_eff,ion ↓ with NCM wt%** ↔ 우리 σ_ionic 폼(φ_SE↓→σ_ionic↓, 퍼콜 임계 아래서 0).  **방향 일치.**

⚠ **절대값 비교 경계:** 그들 σ_eff는 **intrinsic σ(Table S1)를 ε/τ로 가중한 연속체 출력** — **우리 Kirchhoff(σ_grain·
접촉망 순추론)와 정보론적 위상이 다르다**.  그들은 "재료 부피분율·tortuosity"가 입력, 우리는 "접촉 반경·접촉수"가 출력.
⇒ **추세·자릿수 reference이지 점대점 절대 앵커 아님.**  절대 σ 앵커는 **Bazzoun(0.065–0.137)·#271(0.042–0.087)·Varkey·
Minnmann·#266** 유지.  (2023 Battery Energy LPSCl σ_eff 0.0428도 같은 "intrinsic×구조" 위상 — 같은 주의.)

### (2) ★ σ_e 방향 (audit #11) — intrinsic-driven vs contact-network-driven
- **Park 2020:** **NCM wt%↑ → σ_eff,e↑** (Fig 2a).  메커니즘 = **전자 전도재료(NCM) 부피분율↑** → ε_s↑ → σ_eff,e=ε_s·
  σ_s/τ_s↑.  **순수 부피분율 지배(intrinsic-σ-driven, 연속체 voxel).**  도전탄소 없음(NCM 자체전도).
- **우리:** σ_e는 **AM 입자수·AM-AM 접촉수**(contact-network-driven)가 지배 — Stage 22.5 폼 φ_AM⁴·√A_AM-AM.  같은 AM
  부피분율이라도 **작은 AM이 더 많은 접촉**을 만들어 σ_e↑(입경 효과).  ⇒ **표면상 "작은 NCM서 σ_e↑"가 Park의 "큰 부피분율서
  σ_e↑"와 직교** — 한쪽은 **부피분율 축**, 한쪽은 **입경/접촉수 축**.
- **#266과의 추가 대조:** #266은 σ_NCWA(큰 다결정) 13.7 ≫ σ_NCM(작은 단결정) 2.45 → **큰 입자서 σ_e↑**(intrinsic σ 자체가
  큰 입자서 큼) → **Park 방향과 일치(큰/많은 AM → σ_e↑)**, 우리 끝점 가정(σ_S-poly 10 > σ_P-single 5)과는 반대.
- ★ **audit #11 정리:** **Park 2020 = σ_e 방향이 "AM 부피분율↑ → σ_e↑"(intrinsic·연속체) 진영의 시조 증거.**  우리 σ_e가
  **부피분율(φ_AM⁴, Park과 같은 방향)** + **접촉수(√A, 입경의존)** 둘 다 가짐 → Park은 **부피분율 항의 방향을 확증**(φ_AM⁴이
  맞다), 단 입경 효과는 Park이 다루지 않음(고정 NCM711 이차입자).  ⇒ **우리 σ_e φ_AM⁴ 항 = Park과 동방향(검증), σ_S/σ_P
  끝점 순서는 #266과 재대조 필요(별도 audit 항목).**

### (3) frame[5] 분업 — "규칙배치 SE" vs "소성 흐름 SE" / 우리 우위·열위
★ **이 논문의 핵심 positioning 가치:** §2-3단계 **"LPSCl은 deformable → AM 간극에 배치 → 최소 porosity"는 우리 MPM이
*물리적으로 계산*하는 소성 void-fill의 2020 *언어적 규칙*.**  그들은 SE를 **규칙으로 빈틈에 *놓고*** porosity를 최소로 *가정*
한다; 우리는 **압력에서 SE가 *흘러* 빈틈을 채우게** 하고 porosity를 *계산*한다(MPM J2 소성, 우리 champion E_eff 1.53/σ_y
0.15, pure-SE 300→10–11%).  Fig 5에서 저자가 직접 **"better deformation property for minimizing the tortuosity"**가 필요한
새 SE라 적은 것 = **변형성(소성)이 transport에 중요**하다는 인식 → 우리 MPM이 그 변형성을 정량화.

**우리가 앞서는 점:**
- **공정→구조 *예측*** (그들 규칙배치/측정-재구성) — 압력·조성에서 구조를 *계산*(bottom-up).
- **접촉망 σ triad**: σ_ionic + **σ_e + σ_thermal**(그들 σ_eff,e + σ_eff,ion만, 열 없음; 연속체 ε/τ 가중).
- **Kirchhoff/Holm granular constriction** — 점접촉 구속저항(연속체 voxel ε/τ가 못 잡는 것).
- **MPM 소성 SHAPE morphology + void-fill flow**(그들 SE는 규칙배치 구·다면체, 형상변화 없음).
- **fracture(Auerbach/Holm), force chain, Stage-E 소성 접촉면적, scaling-law 압축**(LOOCV 0.975/0.953/0.90).
- **Furnas dip**(이산 패킹) — 그들 단일조성-스윕은 dip 명시 안 함(연속체).

**그들이 앞서는 점(우리가 흡수할 것):**
- ★ **전기화학(BV+질량보존) 3D 디지털트윈 결합** — 우리 Phase-4의 2020 원형(Fig S13 식3–9, Table S2).
- **셀-수준 실험검증**(Fig S14, 1C 편차 ~11 mAh/g; NCM 70wt% Li-In 셀 실측) — 우리 미세구조→셀전압 검증 부족분.
- **시공간 lithiation·ion flux·과전압 맵**(Fig 4–6) — 구조→전기화학 시공간 분해.

### (4) positioning / 계보 배치 (★ 본 디제스트의 결론)
- ★ **이 논문 = DTBL 디지털트윈-ASSB 계보의 ROOT(2020).**  #18(Kim 2024 ACS EL)이 명명한 **top-down/reconstruction +
  규칙기반 배치**의 **첫 ASSB 구현**.  계보: **Park 2020(ROOT) → 2023 Battery Energy(SIC-SPE/LPSCl 이른 시드) → #271(LPSCl
  양극 binder) → #266(bimodal) → #281(Li-O₂ Phase-4 결합) → #286(z-gradient) → #18(taxonomy 체계화)**.  모델러 계보:
  Joonam Park(2020 1저자) → Hyobin Lee·Jaejin Lim(2023+ 디지털트윈 모델러).
- ★ **positioning 한 줄:** **시조 디지털트윈 논문조차 "press를 시뮬"하지 않고, 측정 PSA/SEM에서 입자를 규칙기반 배치**해
  구조를 만든다(GeoDict GrainGeo).  ⇒ 우리 DEM+MPM의 **공정-물리 bottom-up(압력·조성 → 구조 *계산*)**은 이 계보의 **뿌리에
  대한 상향식 진보** — `positioning_vs_geodict.md`의 "GeoDict=구조-given / 우리=공정→구조 예측"을 **2020 발원 사례**로 소급
  적용.  (단 positioning_vs_geodict.md 본체는 유저가 직접 fold — 여기선 근거만 제공.)

### (5) ⚠ 전이 경계 / honest limits
- **σ_eff는 intrinsic σ × ε/τ 연속체 출력**(from-scratch 아님) → **추세·자릿수 reference, 점대점 절대 앵커 아님**(§10-(1)).
- **LPSCl 이차입자 ~8 µm**(Fig S1)로 모델 — 우리·Bazzoun·#266의 **D50 0.7–1.5 µm 작은 SE와 다름**(2020 시점 SE 입도 큼) →
  **specific contact area·dead-SE 절대값은 SE 입도에 민감 → 우리 작은-SE 케이스와 절대 비교 신중**(추세만).
- **압력 sweep 없음** — 단일 "최소 porosity" 규칙배치라 **Heckel/다압력 앵커 아님**(Bazzoun·Varkey·우리 DEM이 담당).
  porosity 값 자체를 직접 보고하지 않음(전극밀도 2.5–2.6 g/cm³·입자 porosity 32.7%만).
- **NBR(wet 공정 바인더)** = 우리 모델 없음(process-specific).  바인더 부피분율 5vol% 고정.
- **시간(cycling) 화학-기계 열화 없음** — 단일 스냅샷(우리·전 디지털트윈 공통 GAP).
- **σ_e 방향**은 **부피분율 축**(Park)이라 우리 **입경/접촉수 축**과 직교 — 같은 데이터로 우리 입경 효과는 검증 못함(§10-(2)).
- **도전탄소 미포함**(NCM 자체전도만) — 우리 CBD(Super P/VGCF) 케이스와 다름.

---

## §11. 미니 용어집 (이 논문 맥락)

- **digital twin (DT):** 실물의 가상 복제 — 실 형상·물리현상을 디지털 공간으로 전이.  여기선 ASSB 전극의 3D voxel 모델.
- **GrainGeo / BatteryDict / ConductoDict / PoroDict (GeoDict 2020 모듈):** GrainGeo=입자 구조 생성(규칙배치),
  ConductoDict=∇·(σ∇φ)=0 voxel FV 유효전도도, PoroDict=Minkowski measure 구조통계(specific contact area), BatteryDict
  "Design Battery"=stacked 셀 전기화학.  ★ ConductoDict EJ(explicit jump) solver = porous 구조용.
- **dead particle:** 동종 재료 망에서 물리적으로 고립된 입자(전기화학 비활성).  = 우리 dead-AM / SE-no-perc.
- **specific contact area (1/m):** 단위부피당 NCM-LPSCl 접촉면적 = 반응 site 밀도 = 우리 coverage / A_AM-SE.
- **effective conductivity σ_eff = ε·σ_intrinsic/τ:** 부피분율·tortuosity로 가중한 거시 전도도(연속체).  ⚠ 우리 Kirchhoff
  접촉망 σ와 위상 다름.
- **transference number t₊ ≈ 0.99–1:** LPSCl 단일이온 도체 → 전해질 농도구배 무시, flux density로 이온 이동 분석.
- **Butler–Volmer (식3):** 계면 전류밀도 j_se = 2k√(c_s·c_e·(c_max−c_s))·sinh[(φ_s−φ_e−E_eq)F/2RT].
- **random seed:** 입자배치 난수 — seed 1–5로 미세구조 변동·허용오차 추정(우리 multi-seed).
- **top-down/reconstruction vs bottom-up/formation(#18 taxonomy):** 측정구조 재구성(이 논문·GeoDict 라인) vs 설계파라미터→
  공정모델 생성(우리 DEM+MPM).  이 논문 = top-down/reconstruction + 규칙배치.

---

## §12. ⇒ 우리 작업에 꽂히는 인사이트 (2–3 sharpest)

1. ★★★ **계보 ROOT 확보 + positioning 소급:** 이 논문이 **DTBL 디지털트윈-ASSB의 2020 발원지**이고, **창립 논문조차 압축을
   시뮬하지 않고 규칙배치(GeoDict GrainGeo)**한다는 것이 우리 **공정-물리 bottom-up**의 상향식 우위를 **계보 뿌리까지** 정당화.
   "변형성 LPSCl을 빈틈에 *놓는다*"는 규칙 = 우리 MPM이 *흐르게 *계산*하는 것의 언어적 원형(frame[5]).  Fig 5의 "better
   deformation property" 인용이 SE 소성=transport 중요성의 저자 자인.
2. ★★ **frame[4] 교차검증 4건(같은 소재계·같은 조성축):** NCM 60–80wt% 최적창 / 90wt% 이온-퍼콜 실패(σ=N/A) / LPSCl
   dead 6–20%@90wt% / σ_eff,ion↓-with-NCM — 모두 우리 dead-AM·SE-no-perc·σ_ionic 폼과 1:1 방향.  단 **σ는 intrinsic×구조
   출력 → 추세·자릿수만**(절대 앵커는 Bazzoun/#271).
3. ★★ **σ_e 방향(audit #11) 부분 확증:** Park **NCM wt%↑→σ_eff,e↑**는 **부피분율 지배(φ_AM⁴ 동방향)** → 우리 σ_e φ_AM⁴
   항의 방향을 검증.  단 우리 **입경/접촉수 축**(작은 AM→σ_e↑)은 Park이 안 다룸 → 직교; σ_S/σ_P 끝점 순서는 #266(큰 입자
   σ_e↑)과 재대조 필요(별도 항목).
4. ★ **Phase-4 원형(stage4_electrochem_research.md):** Fig S13 식3–9 + Table S2(BV+질량보존+t₊≈1 flux + OCV 6-가우시안) +
   "핵심전극 구조분해·보조 연속체·방전부터 검증" = 우리 PyBaMM DFN 결합의 2020 레시피.  #281/#17이 후손.
