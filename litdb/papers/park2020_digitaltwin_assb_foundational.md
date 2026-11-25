# Park 2020 (Adv. Energy Mater. 10, 2001563) — Digital-Twin-Driven All-Solid-State Battery: 물리·전기화학 거동 규명 ★ DTBL 디지털트윈 계보의 시조(FOUNDATIONAL ROOT, 2020)

> slug `park2020_digitaltwin_assb_foundational` · DOI `10.1002/aenm.202001563` · type `FEM·digital-twin` · PDF `Park_2020_AdvEnergyMater_DigitalTwin_ASSB.pdf` · digested `2026-07-28` · status ✅
>
> ⓘ **정본 승격 2026-07-28** — 원본은 작업 브랜치 `claude/solid-state-cathode-improvement-hevry0` 의
> `docs/lit_park2020_digitaltwin_assb_foundational.md` 에서 논문 에이전트가 작성. 단일-서랍 규칙(CLAUDE.md)에 따라 이관.
>
> ⟦10-03 PDF 대조⟧ **원문 전수 대조 — 본문 10쪽 + SI 13쪽을 끝까지 읽음.**  대조 파일 = `litdb/inbox/tortuosity_20261003/`
> 의 `3. Digital twin#U2010driven all#U2010solid#U2010state battery … .pdf`(본문) · `3. Sup) Digital twin#U2010driven … .pdf`(SI).
> 그림 = `litdb/figures/park2020_digitaltwin_assb_foundational/` (fig_1–7 · fig_S1–S17 · tab_S1 · tab_S2) 그대로 사용.
> **쪽 표기:** 본문 p.n = 저널 "(n of 10)" = PDF 쪽.  SI p.n = SI PDF 쪽 — Fig S1 p.2 · S2–S3 p.3 · S4–S5 p.4 · S6–S7 p.5 ·
> **S8–S9 p.6** · S10–S11 p.7 · S12–S13 p.8 · S14–S15 p.9 · S16–S17 p.10 · **Table S1–S2 p.11** · Nomenclature p.12 · **Greek p.13**.
>
> | # | 이번 대조로 바뀐 것 (각 자리에 ⟦10-03 PDF 대조⟧ 표지 · 틀린 문장은 취소선+사유) | 자리 |
> |---|---|---|
> | ① | σ_eff 관계식·경계조건을 원문 그대로 전사.  Fig S9 경계조건 = **6면 모두 Dirichlet**(+x/+y/+z = 1 · −x/−y/−z = 0) — 카드의 "나머지 면 절연"·"Dirichlet jump" 는 원문에 없음 | §4 |
> | ② | ★ **tortuosity 정의 대조표 신설** — 관례 σ_eff = ε·σ/τ (τ 1제곱 · ε = 전도상 부피분율) 원문 확인.  τ 이름은 "tortuosity" 뿐("factor" 없음) · **τ 수치·산출법 미보고** | **§4-T** |
> | ③ | Fig 2a,b σ_eff 재판독 — 카드의 "log −4.5~−3 / −3~−4" 범위는 틀림.  **80 wt% 전자 실험점은 시뮬 밴드 밖(위)**, 이온 실험점은 60·70 wt% 에서 밴드 아랫변 | §4 |
> | ④ | Table S1: LPSCl 이온 σ 는 상수가 아니라 **−4.45×10⁻³·ε_s + 4.64×10⁻³ S cm⁻¹** (ε_s = AM 부피분율).  카드의 물리 근거("압력↓")·"NCM711 문헌값" 은 원문에 없음 | §4 · §8 · §9 |
> | ⑤ | 용량편차 수치 혼동 정정 — "≈12.5 vs ≈80 mAh/g" 와 "1C ≈11 vs >12.5 mAh/g" 는 **서로 다른 두 비교** | §7 · §9 |
> | ⑥ | 구조 생성 ③단계(겹치는 것은 *구형 NCM 객체*) · Fig S8 80/90 wt% 밴드 · Neumann(황화물)/Finsterbusch(산화물) · 소속 "조판 오류" · Fig 7 귀속 · 인용부호 문구 "핵심전극=구조분해…"(원문 없음) 정정 | §1 · §2 · §5 · §7 |
> | ⑦ | 원문에 없는 해석·계산에는 **[미확인] / (추론) / (우리 산술)** 표지.  새 절 §13 = 참고문헌 후속 조달 후보 | 전체 |




> elements: Li Nb O S

**인용:** Joonam Park, Kyu Tae Kim, Dae Yang Oh, Dahee Jin, Dohwan Kim, **Yoon Seok Jung\***, **Yong Min Lee\***,
"Digital Twin-Driven All-Solid-State Battery: Unraveling the Physical and Electrochemical Behaviors,"
*Advanced Energy Materials* **10** (2020) 2001563.  DOI **10.1002/aenm.202001563**.  Received 2020-05-08 ·
Revised 2020-06-19 · Published online 2020-07-26.  © 2020 WILEY-VCH.

**소속:** J. Park, D. Jin, D. Kim, Prof. Y. M. Lee — **DGIST** 에너지과학공학(yongmin.lee@dgist.ac.kr, 당시; 이후 연세
DTBL — ⟦10-03 PDF 대조⟧ 원문 밖 정보).  K. T. Kim, Dr. D. Y. Oh, Prof. Y. S. Jung — **한양대학교** 에너지공학(yoonsjung@hanyang.ac.kr).
⚠ 출판본 1쪽 본문 주소블록은 K.T.Kim/D.Y.Oh/Y.S.Jung을 한 곳에서 **"Yonsei University"**, 다른 곳에서 **"Hanyang
University"**로 동시에 표기~~(출판사 조판 오류).  SI·저자 정정란은 **Hanyang**이 정본 — 본 디제스트는 **Hanyang**으로 기록.~~
⟦10-03 PDF 대조⟧ 사유: "조판 오류"·"저자 정정란"은 원문 어디에도 근거가 없다.  본문 p.1 은 세 사람에게 **두 소속을 나란히**
적는다 — "Department of Chemical and Biomolecular Engineering, Yonsei University, Seoul 03722" **와** "Department of Energy
Engineering, Hanyang University, Seoul 04763".  SI p.1 은 Hanyang 만 적는다.  ⇒ **원문대로 이중 소속으로 기록**(어느 쪽이
정본인지 가를 근거 없음).  **J. Park 과 K. T. Kim 은 공동 1저자** (본문 p.9 Acknowledgements: *"J.P. and K.T.K. contributed
equally to this work."*).

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
  접촉수(contact-network-driven)가 지배 → **작은 NCM서 σ_e↑**가 표면상 반대로 보일 수 있음.  정밀 해석은 ~~§7-(σ_e방향)~~
  **§10-(2)** 에서 (⟦10-03 PDF 대조⟧ 절 번호 정정).
- ⟦10-03 PDF 대조⟧ **τ 관례 (이번 묶음의 목적):** 이 논문의 σ_eff 는 **σ_eff = ε·σ/τ** (τ 1제곱, ε = 전도상 부피분율)
  관례이고, 그 τ 는 우리 **T = φσ₀/σ_eff (= COMSOL τ_F = 웹앱 τ_Lap,eff²)** 와 같은 자리다.  단 원문은 τ 를 "tortuosity"
  라고만 부르고 **값도 산출법도 적지 않는다** → **§4-T**.

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
- ⟦10-03 PDF 대조⟧ **Bielefeld et al.**(ref 9, 위 bullet 에서 빠졌던 것): *"they studied the specific contact area and effective
  conduction with varying the amounts of binder"* (p.2) — 정본 카드 `bielefeld2020_effective_ionic_conductivity_binder` (같은 GeoDict
  EJ 솔버 · τ² 관례 → §4-T 의 대조 짝).
- **Shi et al.**(ref 10): 재료비·입경 함수로 cathode 이용률·용량손실 역산; **정밀 형상 미반영 + 전기화학 미시뮬**.
- ~~**Ito et al.**(ref 11): phase-field로 현실 계면 3D 전극 + 전압·SOC·과전압 수치화; **3D 디지털트윈에선 미시뮬**.~~
  ⟦10-03 PDF 대조⟧ 사유: 원문의 Ito 문장은 *"formed a 3D electrode structure with a realistic interface … on the basis of the
  phase-field method, and also numerically simulated the voltage and discharge capacity values"* (p.2) 이다 — Ito 는 **전압·방전
  용량**까지; "SOC·과전압"은 원문에서 **Park et al.(ref 12)** 의 서술이다 (다음 줄).  "3D 디지털트윈 위에서는 전기화학을 안 풀었다"
  는 Park(ref 12) 문장 바로 뒤의 *"Although …"* 문장이며, Ito 까지 걸리는지는 문장만으로 불분명하다.
- **Park et al.**(ref 12, 이 그룹 선행): SEM에서 실 전극 구조 복사 + 전기화학 변수(전압·SOC·유효전도도·접촉면적) 예측.
  ⟦10-03 PDF 대조⟧ 원문 한계 서술: *"the theoretical electrochemical simulation was not conducted on a 3D digital twin structure"* (p.2).
- ~~**Finsterbusch / Neumann et al.**(ref 13,14): oxide(LLZO 등) SE 전극을 SEM/X선 토모 3D 재구성 + 전기화학 시뮬.~~
  ⟦10-03 PDF 대조⟧ 사유: 두 논문은 SE 종류가 다르고 "LLZO" 는 이 논문에 없는 말이다.  원문(p.2):
  **Finsterbusch**(ref 13) = *"solid oxide electrolyte-based electrode structure fabricated by 3D reconstruction of SEM tomography
  images"* · **Neumann**(ref 14) = *"solid sulfide electrolyte-based electrode structure fabricated by 3D reconstruction of X-ray
  images"* → **Neumann 은 황화물** (우리 계와 같은 쪽).  Neumann 은 §7 의 "≈80 mAh g⁻¹ 편차" 비교 대상이기도 하다.

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
   ⟦10-03 PDF 대조⟧ 위 따옴표는 **한국어 의역**이다.  원문(p.2): *"Third, because the solid sulfide electrolyte is deformable
   during the pressing process, they are located at the interspace of the active materials with reflecting their sizes from the
   PSA result. Thus, sufficient percolation pathways for lithium ions are generated whilst creating minimal porosity; this is key
   to limiting the number of inactive voids."*
4. **NBR 고분자 바인더**를 모든 입자 사이에 추가.
- ⟦10-03 PDF 대조⟧ **random seed 정의**(p.2): *"A random seed is defined as an arbitrary number that assigns an initial location
  of the first object drawn."*  · 생성 속도 주장(p.2): *"our digital twin electrode can be easily and quickly generated using only a
  few design parameters"* (단층촬영 재구성과 대비).

### Experimental 실제 알고리즘(p8, GeoDict GrainGeo)
> "the **GrainGeo module in GeoDict 2020** was used and the formation process was as follows:" (p8 직접 인용)
- **0.5 µm edge cubic voxel**, random seed 1–5.
- ① PSA 데이터로 **uniform spherical NCM** 객체 생성(50×50×~39 µm 도메인).
- ② SEM 분석 기반 **polyhedral primary AM**을 ①의 구형 객체 위에 위치 → ①(구형) 제거(= 다면체 군집만 남김 = bumpy 형상).
- ~~③ PSA 기반 **spherical LPSCl 입자**를 다면체 NCM 구조와 겹치게 배치 → **겹친 AM 객체 부피는 유지하면서 LPSCl을 AM 간극에**.~~
  ⟦10-03 PDF 대조⟧ 사유: 겹치는 주체를 잘못 읽었다 — 원문에서 다면체 1차입자 구조와 겹치는 것은 **구형 NCM 객체**이고, LPSCl
  은 그렇게 겹친 AM 의 간극에 놓인다.  "부피 유지" 가 아니라 "**초기 random seed 유지**" 다.  원문(p.8): *"Next, the spherical NCM
  objects were overlapped with the structure of the polyhedral primary active materials, and the solid electrolyte particles,
  based on particle size analysis data (Figure S1), were located at the interspace of the overlapped active materials whilst
  maintaining the initial random seed number; then, a polymeric binder was added between all particles."*
  ⇒ ③ (정정) 구형 NCM 객체 ↔ 다면체 1차입자 구조 겹침(이차입자 형상) → PSA 기반 **구형 LPSCl** 을 그 간극에 배치 (seed 유지).
  (②에서 "기존 객체 제거" 뒤 ③에서 다시 "구형 NCM 객체"를 겹친다는 순서는 원문 그대로이며, 그 구형 객체가 ①의 것과 같은지는
  원문만으로 불분명 [미확인].)
- ④ **polymeric binder(NBR)** 추가 → composite 전극 완성.  ⟦10-03 PDF 대조⟧ 원문(p.8): *"Finally, the NCM primary active
  materials, the LPSCl solid electrolyte particles, and the NBR binder structures were combined to form a composite electrode
  structure."*
- **periodic function**으로 잘린 입자 부피를 반대편에 생성(작은 입자 substitution 없이 whole-particle 보존).

★ **분류(#18 taxonomy):** **top-down/reconstruction(측정 PSA·SEM에서 구조 재구성) × stochastic/rule-based placement
(확률·규칙 배치)** — #263(separator 확률 3D)과 같은 부류.  **process-physics-driven compaction이 아님**(압축 역학을 풀지
않음).  ⇒ ★ **시조 디지털트윈조차 "press를 시뮬"하지 않고, 규칙으로 입자를 놓는다.**

**신뢰성 주장(p2 우측 + Fig 1d):**
- **±2% 부피분율 오차** — 5개 seed 평균 부피분율이 목표값(Fig 1a 상단)에 ±2% 이내(Fig 1d).
  ⟦10-03 PDF 대조⟧ 원문(p.2): *"Each value is very close to the target values, depicted in the top region in Figure 1a, within a
  2% error range."* — %p(절대)인지 상대 % 인지는 미기술.  Fig 1d 판독: LPSCl 막대 60 wt% ≈47 · 70 wt% ≈34.5 (오차막대 ≈±1).
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
  ⟦10-03 PDF 대조⟧ Fig S1(SI p.2) 가로축 라벨은 두 재료 모두 **"Secondary Particle Size / µm"** — "이차입자" 표현은 원문 라벨
  그대로다.  판독: 피크 NCM ≈8.3 µm(≈10 %) · LPSCl ≈8.5 µm(≈12 %), 시작 ≈3–4 µm, 꼬리 NCM ≈26 µm · LPSCl ≈31 µm.  D50 은 원문에 없음.
- **NCM 1차입자 크기(Fig S2 SEM):** 565 nm ~ 1.55 µm(657 nm, 745 nm, 790 nm, 1.04/1.06 µm 등 표기).
  ⟦10-03 PDF 대조⟧ Fig S2 라벨 전수 = 1.04 µm · 565 nm · 790 nm · **721 nm** · 1.55 µm · 745 nm · 1.06 µm · 657 nm (8개; ×10.0k, 10 kV).
- LiNbO₃ 코팅 0.5 wt%(습식, lithium ethoxide + niobium ethoxide).  LPSCl: Li₂S+P₂S₅+LiCl 볼밀(600 rpm 10 h)+550°C 5 h 어닐.
- 전극 슬러리: dibromomethane 용매, doctor-blade, 60°C 진공건조.  전도도용 Ni-foil, 전기화학용 C-coated Al-foil.
- ⟦10-03 PDF 대조⟧ ★ **실험 전극은 세 조성뿐** — 원문(p.8): *"The weight ratios of NCM, LPSCl, and NBR were 60:38:2, 70:28:2, and
  80:18:2."*  ⇒ **NCM 90 wt% 는 시뮬 전용** (Fig 2a,b 에도 90 wt% 실험점 없음).
- ⟦10-03 PDF 대조⟧ **측정 조건 (원문 p.9, "Conductivity Measurements and Electrochemical Characterization"):**

  | 양 | 방법 (원문) | 조건 | 원문에 없는 것 [미확인] |
  |---|---|---|---|
  | σ_s,eff (전자, 실험) | *"four-probe Van der Pauw method under an applied pressure of 100 MPa"*[17] | Ni foil 위 슬러리 전극 (p.8) · 30 °C | 시편 형상(박리 여부)·측정 방향(면내/두께) |
  | σ_e,eff (이온, 실험) | *"AC impedance method using e⁻-blocking Li-In/LPSCl/electrode/LPSCl/Li-In symmetric cells"* | 진폭 14 mV · 10 mHz–7 MHz · Iviumstat · 30 °C | 대칭셀 성형압·등가회로/피팅법·두께 산정 |
  | 반쪽셀 (Fig S14 실험) | NCM/Li-In half cell, Li–In 대극 (Li₀.₅In:LPSCl = 80:20 wt%) | LPSCl 150 mg 을 100 MPa 로 펠릿화 → 전극·Li–In 을 양쪽에 놓고 **370 MPa** 로 최종 성형 · 30 °C | 운전 중 구속압 |

  *"All the measurements were conducted at 30 °C."* (p.9)
- ⟦10-03 PDF 대조⟧ **(우리 산술) Fig 1a 설계 vol% 의 합 = 88.0 / 80.2 / 71.7 / 63.7 %** (NCM 60/70/80/90 wt%) → 남는 **12.0 /
  19.8 / 28.3 / 36.3 %** 를 원문은 이름 붙이지 않는다 (공극으로 읽히나 [미확인]).  설계 vol% 를 NCM 4.44 g cm⁻³ 로 되짚으면 전극
  밀도 ≈2.60 / 2.56 / 2.50 / 2.44 g cm⁻³ = 원문 "2.5–2.6" 과 정합.  ⚠ NCM "particle porosity 32.7 %" 를 NCM 부피의 내부기공으로
  더하면 60 wt% 에서 합이 100 % 를 넘는다(35.1/0.673 + 47.7 + 5.2 ≈ 105 %) → 4.44 g cm⁻³ 와 32.7 % 의 관계(골격밀도인지 겉보기밀도
  인지)를 원문만으로 맞출 수 없다 [미확인].

---

## §3. ★ Dead particle 분석 — 물리적으로 고립된 입자 vs NCM wt% (Fig 1, Fig S6/S7)

**Dead particle = 주변 동종 재료에서 물리적으로 고립된 입자**(= 우리 dead-AM / f_AM^cc / ~~ionically-vulnerable AM~~, SE쪽은
SE-퍼콜레이션 실패).  부피분율%로 정량(seed 1–5).
⟦10-03 PDF 대조⟧ 사유(취소선): Park 의 NCM dead 는 **NCM–NCM(전자망)에서의 고립**이다 — 원문 *"physically isolated from the
surrounding identical materials"* (p.2).  우리 `*_vulnerable_pct`(AM 의 **SE 접촉** 0–1 개 = 이온 접근 위험)는 다른 망의 양이라
같은 칸에 둘 수 없다.  NCM dead ≈ 우리 AM 전자망 고립(f_AM^cc 의 여집합), LPSCl dead ≈ SE 망에서 떨어진 SE 덩어리.
- **판정 도구 (원문 p.9):** *"isolated particles of NCM and LPSCl were analyzed under activated flow boundary conditions using the
  function of Open and Closed Porosity in a PoroDict module in GeoDict 2020"* — 어느 면에 닿아야 'dead 아님'인지 등 연결 규칙은
  미기술 [미확인].
- **% 의 분모 (추론):** 원문은 분모를 적지 않는다.  그러나 NCM 90 wt% 의 LPSCl dead **19.82 %** 는 그 전극의 LPSCl 전체 부피분율
  **9.4 vol%**(Fig 1a)보다 크므로 "전극 부피 대비"일 수 없다 ⇒ **해당 상(相) 부피 대비 %** 로 읽어야 한다.
- ★ **dead ≠ 비관통:** Fig S10(SI p.7) = *"LPSCl structures without dead particles in NCM 90 wt%"* — dead 를 뺀 LPSCl 도 두께
  방향으로 이어지지 않아 σ_e,eff 를 *"could not be calculated due to disconnected percolation pathways"* (p.3).  ⇒ 이 논문의 'dead
  아님' 은 '관통(spanning)' 보다 **약한 조건**이다 — 우리 쪽 대응도 같은 구분이 필요하다 (`percolation_pct` 밴드 규칙 · 솔버 관통 ·
  `am_ionic_isolated_pct` = 경로 기준 고립 이 서로 다른 양이라는 J20-b·J20-p 구분과 같은 부류).
- 원문 개수 표현(p.2): *"In the case of NCM, there were only one or two dead particles in the NCM 60 wt% electrode (Figure S6)."*

### NCM(AM) dead particle (Fig S6)
| NCM wt% | seed1 | seed2 | seed3 | seed4 | seed5 | 경향 |
|---|---|---|---|---|---|---|
| 60 | 0.94% | 0.20% | 0.00% | 0.37% | 0.43% | 최대 ~0.94% |
| 70 | 0.00% | 0.05% | 0.00% | 0.00% | 0.17% | |
| 80 | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | |
| 90 | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0% |
→ **NCM dead particle은 NCM wt%↑ → 감소**(60wt%서 최대 ~1%, 90wt%서 0%).  이유: **NCM이 많을수록 stochastic
connectivity↑**(AM끼리 더 자주 닿음).  최대 부피분율 <1% → **전기화학 악영향 marginal**(~~p2 우측~~ ⟦10-03⟧ p.3).

### LPSCl(SE) dead particle (Fig S7) ★ 핵심
| NCM wt% | seed1 | seed2 | seed3 | seed4 | seed5 | 경향 |
|---|---|---|---|---|---|---|
| 60 | 0.00% | 0.02% | 0.00% | 0.00% | 0.00% | ~0% |
| 70 | 0.00% | 0.00% | 0.00% | 0.00% | 0.06% | <0.1% |
| 80 | 0.28% | 0.28% | 0.41% | 0.28% | 0.41% | ≤0.5% |
| 90 | **19.82%** | **7.65%** | **9.56%** | **6.16%** | **6.20%** | ★ 급증 6–20% |
→ **LPSCl dead particle은 NCM wt%↑(=LPSCl↓) → 증가**, 단 **NCM 80wt%까지 ≤0.5%**, **NCM 90wt%에서 ~6–20%로 급증**
(seed1 19.82% 최악, 나머지 6–10%).  이유: LPSCl이 적어 서로 고립.

⟦10-03 PDF 대조⟧ **Fig S6 · S7 (SI p.5) 의 40 칸 값을 그림 라벨과 하나씩 대조 — 위 두 표 전부 일치.**

### ★ 저자 결론(~~p2 우측~~ ⟦10-03 PDF 대조⟧ p.3, 직접 인용 가치)
> "these data indicate that the **compositional design range from NCM 60 to 80 wt%** (i.e., from LPSCl 38 to 18 wt%)
> **is appropriate** to achieve minimal dead particles within the all-solid-state electrode."

⇒ ★ **최적 설계창 = NCM 60–80 wt% (LPSCl 38–18 wt%)** — **dead particle 최소.**  NCM 90 wt%(LPSCl 8 wt%)는 LPSCl
고립 급증으로 부적합.

**= 우리 dead-AM/SE-퍼콜레이션과 1:1.** 우리 dead-AM warning(f_AM^cc<80%)·SE-no-perc(σ_ionic=0) degenerate 케이스가
이 NCM 90wt%(SE 8wt%) 코너에 정확히 대응.

---

## §4. ★ 유효 전자/이온 전도도 vs NCM wt% (Fig 2a,b + Table S1 + Fig S9/S10, Ohm's law)

**방법(Fig S9, Ohm's law 정상상태):** 디지털트윈 구조에서 NCM(전자) / LPSCl(이온) 상을 각각 추출, ~~도메인 한 면 φ=1V·
반대면 φ=0(Dirichlet jump ΔV=1V), 나머지 면 절연~~:
⟦10-03 PDF 대조⟧ 사유(취소선): "나머지 면 절연" 은 본문·SI 어디에도 없다.  "jump" 는 경계조건이 아니라 **솔버 이름**(explicit jump,
EJ) 이다.  원문 경계조건은 바로 아래 원문 전사 참조 (Fig S9 는 6면 모두에 Dirichlet 값을 적는다).
```
j = (ε_s·σ_s / τ_s)·∇φ_s   [전자, NCM]      (Fig S9 식1)
j = (ε_e·σ_e / τ_e)·∇φ_e   [이온, LPSCl]    (Fig S9 식2)
σ_eff = (ε·σ_intrinsic)/τ   ← 부피분율 ε × intrinsic σ ÷ tortuosity τ      ⟦10-03⟧ 카드 요약식 — 원문에 독립 식으로는 없음 (아래)
```
⇒ ★ **σ_eff = intrinsic σ를 (부피분율/tortuosity)로 가중한 출력** — **from-scratch 접촉망 추론이 아님**(우리 Kirchhoff/
Holm과 정보론적 위상 다름; ~~§7~~ ⟦10-03⟧ **§10-(1)** cross-validation에서 강조).  GeoDict **ConductoDict + explicit jump(EJ) solver**(porous
구조에 적합)~~, σ는 Open/Closed porosity 제거 후 활성 입자에만~~.
⟦10-03 PDF 대조⟧ 사유(취소선): 원문에서 Open/Closed Porosity(PoroDict) 는 **dead(고립) 입자 판정에만** 쓰였다(p.9).  σ_eff 계산 전에
dead 입자를 지웠는지는 미기술 [미확인] — Fig S10 은 90 wt% LPSCl 을 "without dead particles" 로 *보여줄* 뿐이다.

> ⟦10-03 PDF 대조⟧ **원문 전사 — 식 번호 · 쪽:**
> - **Eq S1 · S2 (SI p.6, Fig S9 "Domain:")** — 그림 안 글자 그대로 (부호 없음 · j 아래첨자 없음):
>   `[1]  j = (ε_s σ_s / τ_s) ∇φ_s`  ("For Electron Density")  ·  `[2]  j = (ε_e σ_e / τ_e) ∇φ_e`  ("For Ion Density").
>   Fig S9 캡션(SI p.6): *"Domains with the governing equation and its boundary conditions for calculation of electron and ion
>   density (Ohm's law).[12]"*
> - **경계조건 (SI p.6, Fig S9)** — 두 정육면체 모두 **6면에 Dirichlet 값**: φ|₊ₓ = 1 · φ|₋ₓ = 0 · φ|₊ᵧ = 1 · φ|₋ᵧ = 0 ·
>   φ|₊z = 1 · φ|₋z = 0 (전자 φ_s, 이온 φ_e 같음).  본문(p.9): *"The boundary conditions were set up as ∆V = 1 V under the
>   Dirichlet condition that assigns the constant potential value on the plane."*
>   ⇒ 세 방향 해를 한 그림에 겹쳐 그린 것(방향별 계산)인지 문자 그대로 6면 동시인지, 그리고 **Fig 2 의 σ_eff 가 어느 방향(두께 z?
>   세 방향 평균?)인지 원문 미기술 [미확인]**.
> - **σ_eff 문장 (본문 p.9, "Calculation of Physical Properties from Digital Twin Structures"):** *"The effective conductivities
>   (σs,eff/σe,eff) were calculated by considering the volume fraction (εs/εe) and tortuosity (τs/τe) of conductive materials to
>   intrinsic electronic/ionic conductivity value (σs/σe) at 30 °C, and the magnitude of current density (j) was simulated on the
>   basis of the governing equation of Ohm's law which relates the electric/electrolyte potential (φs/φe) (Equation S1 and S2 in
>   Figure S9, Supporting Information)."*  이어서 *"The explicit jump (EJ) solver that has high advantages of solving the porous
>   structure was used for this simulation. All process implemented by using a ConductoDict module in GeoDict 2020 (Figure S9
>   and Table S1, Supporting Information).[11,15d,16]"*
> - **기호 (SI p.13, Nomenclature "Greek"):** ε_e *"volume fraction of electrolyte"* · ε_s *"volume fraction of active material"* ·
>   τ_e *"tortuosity of electrolyte"* · τ_s *"tortuosity of active material"* · σ_s *"electric conductivity of active material,
>   S cm⁻¹"* · σ_e *"ionic conductivity of electrolyte, S cm⁻¹"* · Superscripts *"eff = effective"*.  ε·τ 는 단위 없이 적힘.
> - **Fig 2 세로축 기호 (p.4):** "Log[σ_s,eff(e⁻) / S cm⁻¹]" · "Log[σ_e,eff(Li⁺) / S cm⁻¹]" — Eq S1·S2 의 σ_eff 가 곧 실험과 겹쳐 그린 양.
> - ⇒ 카드 요약식 `σ_eff = ε·σ/τ` 는 원문에 **독립된 식으로는 없다** — Eq S1·S2 의 계수(ε σ/τ)와 p.9 문장을 합쳐 읽은 것이며, 그 읽기는
>   원문과 정합한다.  **τ 가 무엇인지는 §4-T.**  (참고: 전기화학 모델 Eq S8·S9(SI p.8)는 **고유** σ_e·σ_s 만 쓰고 ε·τ 가 없다 —
>   구조분해 모델이기 때문이며, ε/τ 는 Fig S9 의 균질화 관계식에만 나온다.)

**Table S1 — intrinsic 전도도(입력값):**
| 재료 | 전자 σ (S/cm) | 이온 σ (S/cm) |
|---|---|---|
| NCM | **8.5×10⁻⁴** ^b | 0 |
| NBR | 0 | 0 |
| LPSCl | 0 | **−4.45×10⁻³·ε_s + 4.64×10⁻³** S cm⁻¹ ^a,b ~~(s = 4.64×10⁻³ S/cm)~~ |

⟦10-03 PDF 대조⟧ (SI p.11) 표 값은 원문과 일치.  취소한 괄호 "(s = 4.64×10⁻³ S/cm)" 는 원문에 없는 오독이다 — ε_s 는 SI p.13 의
*"volume fraction of active material"* 이다.  각주(원문): **a** *"Parameters set in cell design or by experiments"* · **b** *"Parameters
based on literature[18a-c]"*.  Table S2 는 같은 σ_s(^b)·σ_e(^a,b) 를 다시 적고 각주 b 를 *"[12, 16d, 18]"* 로 단다.

⚠ LPSCl 이온 σ는 ε_s(AM 부피분율) 의존 식 ~~— AM이 많을수록 LPSCl이 받는 압력↓로 σ_intrinsic↓을 반영한 보정식(문헌 기반,
ref 18a-c)~~.  NCM 전자 σ=8.5×10⁻⁴ S/cm는 ~~**NCM711 문헌값**~~(우리 σ_AM(e)=50 mS/cm 기준값과 다른 출처·낮음).
⟦10-03 PDF 대조⟧ 사유(취소선 두 곳):
- **물리 근거("압력↓")는 원문에 없다.**  원문은 이 직선식이 어떤 데이터에서 왔는지도 적지 않는다 — 각주가 **a,b 둘 다**(설계·실험
  설정 **및** 문헌)라는 것뿐 [미확인].  ⚠ 이 식이 **자기 복합전극 실측에 맞춘 것**이라면 Fig 2b 의 시뮬–실험 일치는 일부 **순환**
  이 된다 (고유 σ 에 이미 미세구조 벌점이 들어가 있을 수 있음) — 원문으로는 판정 불가.
- **"NCM711 문헌값" 은 원문에 없다.**  원문은 *"based on literature[18a-c]"* 라고만 적는다.  18a = Wang 2018, J. Power Sources 393, 75
  (정본 카드 `wang2018_lco_nmc_electronic_ionic_conductivity_vs_ni`) 는 **LCO·NMC333/532/622/811 만** 쟀고 NCM711 이 없으며, 그 카드의
  20 °C 본문값(NMC532 1.3×10⁻³ · NMC811 4.1×10⁻³ S cm⁻¹)에도 8.5×10⁻⁴ 는 없다 → 값의 출처 [미확인] (18b · 18c 미대조;
  18c Froboese 2019 는 고분자 모델계라는 것이 정본 카드 `ketter2025_resistor_network_models_predict_transport_properties` 의 기록).
- **(우리 산술) 조성별 LPSCl 고유 σ** — Fig 1a 설계 NCM vol% 를 ε_s 로 넣으면:

  | NCM wt% | ε_s (설계) | σ_LPSCl = −4.45×10⁻³ε_s + 4.64×10⁻³ |
  |---|---|---|
  | 60 | 0.351 | **3.08 mS cm⁻¹** |
  | 70 | 0.404 | **2.84** |
  | 80 | 0.450 | **2.64** |
  | 90 | 0.494 | **2.44** |
  | (ε_s → 0) | 0 | 4.64 (식의 절편 — 어떤 전극에도 해당 안 함) |

  ⚠ 시뮬이 설계 ε_s 를 썼는지 seed 별 실제 ε_s 를 썼는지 미기술 [미확인].  ⚠ **σ₀ 가 조성마다 다르다** — τ 를 되짚을 때 기준값이
  조성에 따라 바뀐다 (§4-T).  우연이지만 60–80 wt% 값(3.08–2.64)은 우리 σ_grain 3.0 mS cm⁻¹ 를 끼고 있다.

### ★ 결과(Fig 2a,b) — 시뮬 vs 실험, NCM wt% 함수
- **Fig 2a 유효 전자 σ(σ_eff,e):** **NCM wt%↑ → 증가**.  시뮬(빨강 영역 = seed 1–5 spread)이 ~~실험(빨강 ▲)을 잘 포괄~~.
  ~~log(σ_eff,e) ≈ −4.5 ~ −3 (S/cm) 범위~~, NCM 60→90wt%로 단조 상승.
- **Fig 2b 유효 이온 σ(σ_eff,ion):** **NCM wt%↑ → 감소**.  ~~시뮬(파랑 영역) ↔ 실험(파랑 ▼) 일치.  log(σ_eff,ion) ≈ −3 ~ −4
  (S/cm)~~, NCM 60→80wt%로 단조 하강.
- ⟦10-03 PDF 대조⟧ 사유(취소선): 범위가 틀렸고("−3" 까지 가는 점은 없다) "포괄/일치" 는 80 wt% 전자에서 성립하지 않는다.
  **재판독** = 그림 내장 래스터(2048×1117)에서 축·눈금 픽셀 보정 (두 패널 모두 1 dex = 146.2 px, −3 ↔ 위 테두리 · −6 ↔ 아래 테두리,
  로그 보조눈금으로 확인) → 판독 오차 ≈ ±0.02–0.03 dex.  밴드 = 5 seed 값의 범위 (p.3: *"five simulated values are depicted as
  colored areas"*).  **digitized = TREND 전용.**

  | NCM wt% | 전자 시뮬 밴드 log₁₀σ_s,eff (S cm⁻¹) | 전자 실험 (▲) | 위치 | 이온 시뮬 밴드 log₁₀σ_e,eff | 이온 실험 (▼) | 위치 |
  |---|---|---|---|---|---|---|
  | 60 | −4.96 ~ −4.20 (1.1–6.3 ×10⁻⁵) | −4.25 (5.6×10⁻⁵) | 밴드 안 · 윗변 근처 | −3.48 ~ −3.25 (3.3–5.6 ×10⁻⁴) | −3.48 (3.3×10⁻⁴ = 0.34 mS cm⁻¹) | **밴드 아랫변** |
  | 70 | −4.32 ~ −4.03 (4.8–9.3 ×10⁻⁵) | −4.07 (8.5×10⁻⁵) | 밴드 안 · 윗변 근처 | −4.00 ~ −3.65 (1.0–2.2 ×10⁻⁴) | −4.03 (9.3×10⁻⁵ = 0.093 mS cm⁻¹) | **아랫변(경계)** |
  | 80 | −4.12 ~ −3.95 (0.76–1.1 ×10⁻⁴) | **−3.80 (1.6×10⁻⁴)** | **밴드 밖(위) ≈ +0.15 dex (×1.4)** | −4.95 ~ −4.30 (1.1–5.0 ×10⁻⁵) | −4.51 (3.1×10⁻⁵ = 0.031 mS cm⁻¹) | 밴드 안 |
  | 90 | −3.93 ~ −3.87 (1.2–1.35 ×10⁻⁴) | 실험 없음 | — | **계산 불가** | 실험 없음 | — |

  ⇒ 원문 표현은 *"comparable to the real system"* (p.3) 이다.  판독상 **전자 실험은 시뮬 위쪽, 이온 실험은 시뮬 아래쪽**에 붙는다 —
  어느 쪽도 밴드 중앙이 아니다.  (원인은 원문이 논하지 않음: 측정 방향 차 Van der Pauw ↔ 시뮬 방향 [미확인] · 고유 σ 선택 등.)
- ★★ **NCM 90 wt%의 유효 이온 전도도는 계산 불가** — "**the effective ionic conductivity values of the NCM 90 wt%
  electrodes could not be calculated due to disconnected percolation pathways between LPSCl particles (Figure S10)**"
  (~~p2 우측~~ ⟦10-03 PDF 대조⟧ p.3 직접 인용).  Fig S10은 dead particle 제거 후에도 LPSCl 망이 끊긴 5개 seed를 보임 → **퍼콜레이션 실패**.
- **저자 종합:** "logical trends that the effective conductivity range depends on the amount of corresponding conductive
  materials" + "simulated conductivity range(색칠 면적)가 conductive material↓ 할수록 커진다(분산↑)".

⇒ ★ **방향 정리(audit #11 핵심):**
- **σ_eff,e ↑ with NCM wt%** ← **전자 전도재료(NCM) 부피분율↑** (intrinsic-σ-driven, 부피분율 지배).
- **σ_eff,ion ↓ with NCM wt%** ← **이온 전도재료(LPSCl) 부피분율↓** (intrinsic-σ-driven).
- **NCM 90 wt% σ_eff,ion = N/A** (LPSCl 퍼콜레이션 실패 = 우리 σ_ionic SE-no-perc degenerate).

**= 우리 σ_ionic 폼과 1:1**(SE↓→σ_ionic↓→퍼콜 임계 아래서 0).  **σ_e 방향은 ~~§7-(σ_e방향)~~ ⟦10-03⟧ §10-(2) 에서 우리 contact-network-driven과
대조** — 그들은 부피분율 지배(연속체 voxel), 우리는 입자수·접촉수 지배(이산 접촉망).

---

## §4-T. ★★ tortuosity 정의 대조표 — 이 논문의 τ 는 무엇인가 ⟦10-03 PDF 대조⟧

> 목적: 우리 τ 들(웹앱 τ_Lap,eff · τ_Lap,geom · τ_Dij · τ_Dij,all · 벽 τ · COMSOL τ_F · 인계 열 f/T/τ)과 이 논문의 τ 가
> **같은 양인지, 아니면 제곱·정규화가 다른지**를 원문으로 닫는다.  원문 근거는 전부 §4 의 원문 전사 (SI p.6 Eq S1·S2 ·
> 본문 p.9 · SI p.13 · SI p.11).

### (1) 원문이 말하는 것 / 말하지 않는 것

| 항목 | 원문 | 위치 | 판정 |
|---|---|---|---|
| 관계식 | j = (ε σ / τ) ∇φ — 전자(s)·이온(e) 각각 | SI p.6 Fig S9 Eq [1]·[2] | ✅ τ 는 **1제곱**으로 분모에 있다 (τ² 아님) |
| σ_eff 정의 | *"calculated by considering the volume fraction (εs/εe) and tortuosity (τs/τe) of conductive materials to intrinsic … conductivity value (σs/σe)"* | 본문 p.9 | ✅ ⇒ **σ_eff = ε·σ/τ** |
| ε | *"volume fraction of electrolyte"* · *"volume fraction of active material"* | SI p.13 | ✅ 전도상 부피분율.  분모 = 전극 전체(공극 포함)로 읽힘 — Fig 1a 설계 vol% 합이 88.0/80.2/71.7/63.7 % 로 100 미만 (추론) |
| τ 이름 | *"tortuosity of electrolyte"* · *"tortuosity of active material"* | SI p.13 | "tortuosity **factor**" 라는 말은 본문·SI **어디에도 없다** (전문 검색: "tortuos" = 본문 p.6 · 본문 p.9 · SI p.13(τ_e·τ_s 2회) 뿐; "factor" 는 "normal factor"(본문 p.9 · SI p.12) 뿐) |
| τ 값 | — | — | **보고 없음** (본문·SI·그림 전수) |
| τ 산출법 | — | — | **미기술 [미확인]** — EJ 해에서 역산한 양인지, GeoDict 가 따로 낸 τ 를 식에 넣은 것인지 원문이 말하지 않는다 |
| σ_eff 정규화 면적 | 명시 문장 없음 | — | **전체 단면**으로 읽는 것이 정합 (추론): ① 식에 ε 가 명시돼 있다 = 겉보기(superficial) 플럭스 관례 (상 단면 정규화라면 σ/τ 꼴이 된다) ② 시뮬 σ_eff 를 전극 전체로 잰 실험(Van der Pauw · 대칭셀 EIS)과 같은 축에 겹쳐 그렸다 (Fig 2a,b) |
| 방향 | Fig S9 = 6면 Dirichlet | SI p.6 | Fig 2 값이 어느 방향인지 미기술 [미확인] |
| 고유 σ (= 우리 σ₀) | NCM 8.5×10⁻⁴ S cm⁻¹ (상수) · LPSCl −4.45×10⁻³ε_s + 4.64×10⁻³ (조성 의존) | SI p.11 Table S1 | ⚠ 이온 쪽 σ₀ 가 조성마다 다르다 (3.08→2.44 mS cm⁻¹, §4) |
| 산문 속 tortuosity | *"…better deformation property for minimizing the tortuosity"* | 본문 p.6 | 정성적 '경로 굴곡' 의미 (정의 없음) |

★ **교차 근거 — 같은 GeoDict EJ 솔버를 쓴 Bielefeld 2020** (Park ref 9 · 정본 카드 `bielefeld2020_effective_ionic_conductivity_binder`
§2.2, 그 논문 Eq 3·11) 은 **같은 양을 τ² 로 적고 "tortuosity factor" 라 부르며, σ_eff 를 풀고 나서 역산한다**:
σ_eff,ion = (ε_SE/τ²)·σ_bulk,SE  →  τ² = ε_SE·σ_bulk,SE/σ_eff,ion (ε_SE = 전체 부피 대비, void 포함).
⇒ **Park 의 τ = Bielefeld 의 τ²** (기호만 다르고 같은 자리).  Park 도 같은 역산 경로였을 개연성은 높지만 Park 원문에는 근거가 없다 (추론).

### (2) 판정 — "이 전고체 논문은 σ_eff = ε·σ/τ (τ = tortuosity factor = 우리 T) 관례를 쓴다"

| 명제 | 판정 | 근거 |
|---|---|---|
| σ_eff = ε·σ/τ 관례를 쓴다 | ✅ **원문 확인** | SI p.6 Eq S1·S2 + 본문 p.9 |
| ε = 전도상 부피분율 | ✅ **원문 확인** | SI p.13 |
| σ_eff 는 전체 단면 정규화 | ◐ **추론** (명시 문장 없음) | 식에 ε 명시 + 실험과 직접 비교 |
| τ ≡ ε·σ₀/σ_eff (= 우리 T = COMSOL τ_F) | ✅ **식의 대수로 동일** | Eq S1·S2 가 성립하는 한 τ 는 정의상 그 값 |
| τ 를 "tortuosity factor" 라 부른다 | ✗ **원문에 없음** | 이름은 "tortuosity" 뿐 (SI p.13) — "factor" 라는 이름은 Bielefeld 2020 쪽 |
| τ 값 · 산출법 | ✗ **보고 없음 [미확인]** | — |

⇒ **최종:** *"관례 = σ_eff = ε·σ/τ 이고, 그 τ 는 우리 T(= τ_F) 자리다"* 는 **원문으로 선다**.  *"τ = tortuosity factor"* 라는 **이름**과
τ 의 **산출법**은 원문으로 닫히지 않는다 — 만약 GeoDict 가 따로 계산한 *기하* τ 를 식에 대입했다면 τ 는 여전히 식을 만족하지만, 그때
Fig 2 의 σ_eff 는 '해'가 아니라 '공식 대입값'이 된다.  **원문에 τ 수치는 하나도 없다.**

### (3) 대조표 — 원문 기호 · 정의식 · 이름 · 정규화 · 우리 어느 τ 와 같은 양인가 · 환산식

| 기호 (출처) | 정의식 | 이름 | 정규화 | 우리 대응 | 환산식 |
|---|---|---|---|---|---|
| **τ_e** (Park, SI p.6 Eq [2]) | σ_e,eff = ε_e·σ_e/τ_e ⇒ τ_e = ε_e·σ_e/σ_e,eff | *"tortuosity of electrolyte"* (SI p.13) | 전체 단면 (추론) · ε_e = LPSCl 부피분율 · σ_e = Table S1 식 (ε_s 의존) | **T = φσ₀/σ_eff** = **COMSOL τ_F** | τ_e = T = (τ_Lap,eff)² ; τ_Lap,eff = √τ_e — **σ₀ 를 같은 값으로 맞출 때만** (Park σ₀ = 3.08/2.84/2.64 mS cm⁻¹ @60/70/80 wt% ↔ 우리 σ_grain) |
| **τ_s** (Park, SI p.6 Eq [1]) | σ_s,eff = ε_s·σ_s/τ_s | *"tortuosity of active material"* | 같음 · ε_s = NCM 부피분율 · σ_s = 8.5×10⁻⁴ S cm⁻¹ | 전자망 T_AM = φ_AM·σ_AM/σ_e,eff — **우리 웹앱에 대응 열 없음 (n/a)** | τ_s = T_AM |
| τ² (Bielefeld 2020 Eq 3·11, 정본 카드) | σ_eff,ion = (ε_SE/τ²)·σ_bulk,SE | "tortuosity factor" | ε_SE = 전체 부피 대비 (void 포함) | T | τ²(Bielefeld) = τ_e(Park) = T |
| τ_F (COMSOL 5.6 Eq 6-6 — 메인 제공, 원문 아님) | f_e = ε_p/τ_F ; σ_eff = σ₀·f_e | tortuosity factor | — | T | τ_F = T ; Bruggeman 기본값 τ_F = ε_p^(−1/2) |
| **τ_Lap,eff** (웹앱 `webapp/app.py:2610`) | √(φ_SE·σ_grain/σ_full) | Laplace τ (협착 포함, "GB 포함") | σ_full = DEM 접촉망 Kirchhoff 해 · 전체 단면 | **√T** | τ_Lap,eff² = T = τ_e(Park) |
| τ_Lap,geom (웹앱 `webapp/app.py:2613`) | √(φ_SE·σ_grain/σ_bulk_net) | Laplace τ (협착 제외, "GB 제외") | σ_bulk_net = 같은 망, 협착 없는 가지 | √T_bulk | τ_Lap,geom² = T_bulk.  Park 의 복셀 해에는 입자간 접촉·계면 저항 항이 **언급되지 않는다** → 개념상 이 '협착 없는' 쪽에 더 가깝다 (추론) |
| τ_Dij · τ_Dij,all · 벽 τ (웹앱) | 최단경로 길이 / 직선 거리 | 기하 τ | — | Park 에 **대응 없음** (기하 τ 미보고) | 일반 환산식 없음 — "τ_F ≈ τ_geo²" 는 모세관(Carman) 모형 가정일 뿐 |
| 인계 열 계획 (메인 제공) | f = σ_eff/σ₀ · T = φ/f · τ = √T | — | 전체 단면 | — | Park 으로 쓰면 f = ε/τ_e · T = τ_e · τ = √τ_e |

⚠ **웹앱 라벨 점검 거리 (보고만 — 이 카드는 코드를 고치지 않는다):** 웹앱 표는 τ_Lap,eff 를 *"COMSOL input"* 이라 적는다
(`webapp/app.py:2050`·`2615` 표 머리).  COMSOL Eq 6-6 의 τ_F 는 **T** 이므로, τ_Lap,eff(= √T) 를 τ_F 칸에 그대로 넣으면 **제곱만큼**
어긋난다.  Park 식도 T 관례다.

### (4) τ 값 표 — **원문 보고 없음.**  아래는 **우리 역산** (원문 값 아님 · 수치로 옮기지 말 것 · TREND 전용)

계산 = τ = ε·σ₀/σ_eff (원문 Eq S1·S2 의 대수).  입력: ε = Fig 1a 설계 vol% (stated) · σ₀ = Table S1 (stated) · σ_eff = Fig 2a,b
판독 (digitized, ±0.03 dex) · 시뮬 범위 = 5 seed 밴드 양 끝.

| NCM wt% | ε_s | τ_s (시뮬 범위) | τ_s @실험 σ_eff | ε_e | σ₀,LPSCl (mS cm⁻¹) | τ_e (시뮬 범위) | τ_e @실험 σ_eff | √τ_e (시뮬) |
|---|---|---|---|---|---|---|---|---|
| 60 | 0.351 | 4.7–27 | 5.3 | 0.477 | 3.08 | 2.6–4.4 | 4.4 | 1.6–2.1 |
| 70 | 0.404 | 3.7–7.2 | 4.0 | 0.347 | 2.84 | 4.4–9.9 | 11 | 2.1–3.1 |
| 80 | 0.450 | 3.4–5.0 | 2.4 | 0.217 | 2.64 | 11–51 | 19 | 3.4–7.1 |
| 90 | 0.494 | 3.1–3.6 | 실험 없음 | 0.094 | 2.44 | 계산 불가 (퍼콜 끊김) | 실험 없음 | — |

- "@실험" 열 = 실험 σ_eff 에 **모델의** 고유 σ 를 대입한 가상의 값이다 — 원문은 이런 계산을 하지 않았다.
- 우리 관례로 다시 쓴 예 (σ₀ = 3.0 mS cm⁻¹ 고정, 같은 실험 이온 σ_eff): T = 4.3 / 11 / 21 · √T = 2.1 / 3.3 / 4.6 (60/70/80 wt%).
- Bruggeman 대조 (우리 산술): τ_F = ε^(−1/2) 이면 τ_s ≈ 1.7/1.6/1.5/1.4 · τ_e ≈ 1.4/1.7/2.1/3.3 → 역산 τ_e 는 60 wt% 에서 2–3배,
  80 wt% 에서 5–24배 크다.  (Bielefeld 카드의 *"Bruggeman 은 ASSB 양극에 그대로 쓰면 안 된다"* 와 같은 방향.)
- 읽을 점: τ_e 는 LPSCl 이 줄수록 급증(≈4 → ≈20), τ_s 는 NCM 이 늘수록 감소 — §4 의 '전도재료 부피분율 지배' 서사를 τ 로 다시
  적은 것.  60 wt% 전자 시뮬 범위가 넓은 것(τ_s 4.7–27)은 원문 서술 *"the simulated conductivity range … becomes larger as the
  corresponding conductive material decreases"* (p.3) 와 정합.

---

## §5. ★ Specific contact area vs NCM wt% (Fig 2 본문 + Fig S8)

**Specific contact area = NCM-LPSCl 접촉 비표면적(1/m, = 우리 ~~coverage /~~ A_AM-SE).**  GeoDict PoroDict로 Minkowski
measure(부피·표면·적분평균곡률) 통계분석 산출.
⟦10-03 PDF 대조⟧ 원문(p.9): *"…calculated using statistical analysis based on Minkowski measures (volume, surface, integral of mean,
integral of total curvature) through the PoroDict module"* — 네 번째 항 **integral of total curvature** 추가.  단위 m⁻¹ = 면적/부피이고
**분모 부피(전극 전체? NCM?)는 미기술 [미확인]**.  취소선 사유: 우리 **coverage 는 AM 표면 중 SE 가 덮은 비율(%)** 이라 같은 양이
아니다 — 대응은 **A_AM-SE / V**(우리 계면 면적 합 ÷ 상자 부피).  coverage 로 바꾸려면 AM 비표면적이 더 필요하다.

### 결과(Fig S8)
- **NCM wt%↑ → specific contact area 단조 감소**: ~**95,000 → ~35,000 1/m** (NCM 60→90wt%, max/min seed 밴드).
  ~~(60wt% ~78,000–97,000 / 80wt% ~55,000–62,000 / 90wt% ~30,000–40,000 1/m, w/dead vs w/o-dead 밴드.)~~
  ⟦10-03 PDF 대조⟧ 사유: 80·90 wt% 범위가 틀렸다.  **재판독** (Fig S8 래스터, 축 픽셀 보정 · ±0.5k · digitized):

  | NCM wt% | 최대 (w/ dead) | 최소 (w/ dead) | 최대 (w/o dead) | 최소 (w/o dead) |
  |---|---|---|---|---|
  | 60 | 97.4k | 77.8k | 96.6k | 76.8k |
  | 70 | ≈81k | 69.5k | ≈80k | 68.5k |
  | 80 | 58.1k | 54.4k | 57.3k | ≈54k |
  | 90 | 36.5k | 25.4k | ≈33k | 21.4k |

  (단위 m⁻¹.  범례 원문 = "Maximum / Mininum simulation value (w/o dead particles)" — "Mininum" 은 원문 오탈자.)
- ★ **dead particle 유무의 영향은 insignificant** — w/ dead(검정 점선)와 w/o dead(빨강 점선) 밴드가 거의 겹침(특히 NCM
  60–80wt%; 90wt%서만 살짝 벌어짐).  "the dead particle effect is insignificant in our electrode conditions"(~~p2 우측~~ ⟦10-03⟧ p.3).
- **물리 해석:** NCM↑ → LPSCl↓ → AM-SE 계면 면적↓ → **전기화학 반응 site↓**.  이것이 **NCM 80wt% rate 저하의 근본 원인**
  으로 이후 전기화학 절에서 반복 인용(~~§6, §8~~ ⟦10-03⟧ **§7** — Fig 3 specific capacity 감소 + Fig 6 과전압 증가의 구조적 뿌리).
- ⟦10-03 PDF 대조⟧ 원문 문장(p.3): *"That is, as NCM wt% increases from 60 to 90 wt%, a higher surface overpotential occurs even if
  both electrons and ions are in sufficient supply."*

⇒ **= 우리 coverage(Stage-E Hertz/Tabor) / A_AM-SE.**  "NCM↑ → contact area↓ → 반응site↓ → rate↓"는 우리 coverage→
전기화학 연결의 2020 원형.  (⟦10-03⟧ 단, 위 단위 주의 — 직접 수치 대응은 A_AM-SE/V 쪽.)

---

## §6. ★ Charge / current distribution — 전자 vs 이온 흐름 (Fig 2c–f + Fig S11/S12)

**방법:** 같은 Ohm's-law 시뮬 결과를 charge density(mA/cm²) colormap으로 3D 가시화.  ⚠ **전극에 도전탄소(conductive
carbon)를 넣지 않음** — "the electrodes did not contain conductive carbon materials to enhance the connectivity for the
NCM particles"(p3 우측).  즉 NCM 자체 전자전도로만.

### 결과(Fig 2c–f, charge density 0–100 mA/cm²)
- **Fig 2c(NCM 60wt%) vs 2d(NCM 80wt%) 전자밀도(NCM 상):** ★ **NCM 80wt%가 더 나은(높은·균일) 전자밀도** — AM이 많아
  연결 좋음.  "the NCM 80 wt% exhibits better electron density over the same domain than NCM 60 wt%."
  ⟦10-03 PDF 대조⟧ 원문 정확 문구(p.3): *"…than that of the NCM 60 wt% (Figure 2c,d)"* · 도전탄소 문장은 *"…to enhance the
  connectivity **of** the NCM particles"* (위 인용의 "for" 는 오기).
- **Fig 2e(NCM 60wt%) vs 2f(NCM 80wt%) 이온밀도(LPSCl 상):** ★ **NCM 60wt%가 훨씬 높은 이온밀도 + 더 넓은 공간영역에
  분포** — LPSCl 많아 연결 좋음.  "the NCM 60 wt% has a much higher ion density across more spatial regions."
- **종합(p3 우측):** NCM 80wt%(LPSCl 20wt%)는 이온경로가 **전자경로보다 더 국소화(localized)** → 이온이 병목.
  ⟦10-03 PDF 대조⟧ 원문은 **서로 다른 전극의 두 망**을 비교한다: *"Thus, as the content of LPSCl decreases to 20 wt% (NCM 80 wt%),
  its ionic pathways become more localized than the electronic pathways in the NCM 60 wt%."* (p.3 — "20 wt%" 는 원문 표기, 설계는
  LPSCl 18 wt% + NBR 2 wt%).
- ⟦10-03 PDF 대조⟧ ⚠ **(추론) 이 지도들의 전류밀도는 ΔV = 1 V 를 건 Ohm 해의 값이다** — p.9 가 전류밀도를 Eq S1·S2 + ΔV = 1 V
  경계조건으로 풀었다고 적고, Fig 2c–f 는 같은 σ_eff 계산의 시각화로 소개된다 (p.3 *"As estimated from the effective electronic
  conductivity values…"*).  ⇒ 20 · 80 mA cm⁻² 문턱(Fig S11·S12)은 **1 V 수송 프로브 기준의 상대 문턱**이지 운전 전류가 아니다
  (우리 웹앱의 "@1V 수송 프로브 ≠ @1C 운전" 프레임 구분과 같은 주의).  컬러바 0–100 mA cm⁻² (p.4 Fig 2).
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
  직렬.  voxel 0.5 µm(전극)~~, 0.01 µm급은 아님~~.  30°C, C-rate 0.1/0.5/1C.
  ⟦10-03 PDF 대조⟧ 사유(취소선): "0.01 µm" 는 원문에 없는 말이다.  "voxel 0.5 µm" 는 **구조 생성(GrainGeo)** 의 값(p.8)이고, 셀 전기화학
  모델의 이산화는 따로 적히지 않았다 [미확인].  원문 정확 문구(p.9): *"The function of Design Battery in a BatteryDict of GeoDict 2020
  was used for the set-up of a digital twin **stacked** cell with the composition lithium metal (3 µm)/LPSCl layer (30 µm)/all-solid-
  state electrode/aluminum (1.5 µm)."*  **푼 솔버**(p.9): *"All process proceeded by the Charge Battery (BESTmicro solver, Battery and
  Electrochemical Simulation Tool micro, Fraunhoher ITWM, Germany)"* — "Fraunhoher" 는 원문 오탈자(Fraunhofer).  각 셀은 *"driven at
  30 °C as a function of C-rate (0.1, 0.5, and 1C)"*.  Fig S13 의 축척 막대 = 15 µm.  셀 단면 크기(전기화학 도메인의 가로·세로)는
  미기술 [미확인].
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
  ⟦10-03 PDF 대조⟧ 식 3–9 를 SI p.8 Fig S13 그림 글자와 대조 — **일치** (원문 표기: [4] j⃗_s·n⃗ = j_se · [5] j⃗_e·n⃗ = j_se ·
  [7] ∂c_e/∂t = ∇(D_e∇c_e) − ∇(t₊j⃗_e/F) · [8] ∇j⃗_e = ∇[σ_e(1−t₊)(RT/F)∇log c_e] − ∇(σ_e∇φ_e) · [9] ∇j⃗_s = −∇(σ_s∇φ_s)).
  Fig S13 캡션의 인용 = [18f, 19] (Latz & Zausch 2011/2015 · Hein & Latz 2016 · Danner 2016 · Valoen & Reimers 2005 — 원문 표기).
  ★ τ 관점: 식 8·9 의 σ_e·σ_s 는 **고유값**(Table S2) 이고 ε·τ 가 없다 — 구조를 복셀로 푸는 모델이기 때문 (§4-T).
- ★ **모델 파라미터(Table S2, 직접 전사):** D_s=3.0×10⁻¹⁵ m²/s, D_e=1.2×10⁻¹³ m²/s, k(BV rate)=1.0×10⁻⁷ A·m^2.5·mol^−1.5,
  σ_s=8.5×10⁻⁴ S/cm, σ_e=−4.45×10⁻³·ε_s+4.64×10⁻³ S/cm, c_s,max=47054 mol/m³, c_e=46276 mol/m³, **t₊=0.99**(LPSCl 단일이온
  근사), I_1C=2.625×10⁻⁹ A, T=303.15 K.  E_eq(SOC) = 6-가우시안 합 OCV 피팅(Table S2 식).
  ⟦10-03 PDF 대조⟧ (SI p.11) 위 값 **전부 일치**.  각주: **a**(설계·실험 설정) = σ_e · I_1C · T · E_eq ; **b**(문헌 [12, 16d, 18]) =
  D_s · D_e · k · σ_s · σ_e · c_s,max · c_e · t₊ (σ_e 는 a,b).  E_eq 전문(원문 그대로, 단위·soc 정의역 표기 없음):
  `E_eq = 131.6exp(−((soc−15.94)/8.802)²) + 2.333exp(−((soc−33.8)/15.38)²) + 3.681exp(−((soc−58.6)/25.72)²)`
  `     + 2.063exp(−((soc−85.47)/15.52)²) + 1.351exp(−((soc−95.74)/9.27)²) + 0.7779exp(−((soc−100.12)/5.177)²)`
  ⚠ **(우리 산술) Phase-4 로 옮기기 전 주의:** soc = 100 → 3.01 V · 70 → 3.80 · 40 → 4.24 · 38 → 4.35 이지만 soc = 30 → 13.5 V ·
  20 → 108 V 로 **발산** (첫 항 131.6).  ⇒ 이 맞춤식의 유효 정의역은 대략 **soc ≳ 38** 이고, **soc = 100 이 ≈3.0 V(방전 끝)** 다.
  본문(p.5) 은 *"the SOC value of cell is inversely proportional to the lithium concentration in the active material"* 라 적으므로
  E_eq 의 "soc" 는 셀 SOC 와 **축 방향이 반대**(리튬화도에 가까움)로 읽힌다 [미확인].  I_1C 를 어느 면적·질량에서 냈는지도 미기술.
  ⟦10-03⟧ t₊ 원문(p.9): *"Herein, the lithium transference number (t+) was set as 0.99 because the LPSCl solid electrolyte is the
  single-ion conductor."*
- ★ **단일이온 도체 가정(p5 우측):** "the inorganic solid electrolyte is a single-ion conductor with a transference
  number of approximately **0.99–1**" → LPSCl 내 농도구배 무시, **flux density**로 이온 이동 분석.  ⇒ 우리 LPSCl t₊≈1과 동일.

### Fig 3 — 전압-용량 프로파일(seed 1–5, 0.1/0.5/1C)
- **(a–c) NCM-기반 gravimetric capacity**(NCM 60/70/80wt%), **(d–f) electrode-기반 areal capacity**.  같은 C-rate서
  seed 변동은 미세(디지털트윈 신뢰성 재확인).
- ★ **검증(Fig S14):** 우리 시뮬 비용량이 여러 선행 실험 데이터(ref 15a-d, 다양한 조성·로딩)와 유사.  ★ ~~**"우리 모델의 1C
  평균 용량편차 = ~11 mAh/g, 다른 디지털트윈 모델 기반 연구는 1C서 >12.5 mAh/g(특히 고율 ~80 mAh/g)"**~~ → **더 정확**(p4
  우측).  이유: 더 정교한 미세구조 + 사전점검된 유효 전자/이온 전도도.  NCM 70wt% 전극/LPSCl/Li-In 셀을 같은 조건 실측 대조.
  ⟦10-03 PDF 대조⟧ 사유(취소선): 원문의 **서로 다른 두 비교**를 한 문장으로 섞었고 따옴표 문장은 원문에 없다.  원문(p.4):

  | 비교 | 원문 | 숫자 |
  |---|---|---|
  | ① 우리 시뮬 ↔ **선행 실험[15]** 의 평균 편차, 그리고 **Neumann 2020[14]** 의 편차 | *"the average capacity deviation of our model was very low, ≈12.5 mA h g−1, whereas the latest study based on digital twin modeling and simulation reported much higher capacity deviation of around 80 mA h g−1, especially at high current densities.[14]"* | 우리 ≈12.5 · Neumann ≈80 mAh g⁻¹ |
  | ② **자기 실측** NCM 70 wt% 셀 ↔ 시뮬 (1C), 그리고 **나노 도전재를 쓴 다른 연구들** | *"…the simulated average capacity deviation at 1C was ≈11 mA h g−1 while the values of the other works based on the electrode having the nanosized conductive materials were more than 12.5 mA h g−1 at 1C (Figure S14)"* | 우리 ≈11 · 다른 연구 >12.5 mAh g⁻¹ |

  - 원문 p.4 는 선행 실험 비교를 *"(Figure S12, Supporting Information)"* 로 가리키는데, S12 는 이온밀도 그림이다 → **S14 의 오기로
    보인다** (원문 오류 표지).
  - **Fig S14 범례 (SI p.9, stated):** [In this work] NCM711:LPSCl:NBR = 70:28:2, 10 mg cm⁻² (○ 점선) · [15a] NCM622:Li₂S-P₂S₅:Super
    C65:NBR = 70:27.5:1:1.5, 3.77 mg cm⁻² · [15b] NCM622:LPSCl:Super C65:NBR = 83.1:14.2:1.3:1.4, 20 mg cm⁻² · [15c] NCM622:LPSCl:
    Super C65:NBR = 70:27.5:1:1.5, 15 mg cm⁻² · [15d] NCM622:LPSCl:Super C65:NBR = 68.1:29.2:1.3:1.4, 23 mg cm⁻² · 시뮬 막대 =
    NCM711 60:38:2 / 70:28:2 / 80:18:2 · *"Operating Temperature: 30 °C"*.
  - ⚠ **같은 계끼리의 비교는 [In this work] 한 줄뿐** — [15a–d] 는 **NCM622 + Super C65(도전탄소)** 전극인데 시뮬은 **NCM711 · 탄소
    없음**.  판독(≈, digitized): 1C 에서 자기 실측 ≈40, 시뮬 70 wt% 막대 ≈41–50 mAh g⁻¹ — 원문의 "≈11 mAh g⁻¹" 을 어떤 쌍의 평균으로
    셈했는지는 미기술 [미확인].
- ★ **specific capacity ↓ with NCM wt%**(Fig 3a–c): "considerable specific capacity reduction is observed as the NCM
  content increases from 60 to 80 wt%, **even at the lowest C-rate of 0.1C, as high as 20 mAh/g, equivalent to 15%**."
  ← **specific contact area↓**(Fig S8) 때문.  고율일수록 NCM 80wt% 용량비↓ 더 큼 = **낮은 contact area + 낮은 유효 이온
  전도도** 결합효과.
- **areal capacity(Fig 3d–f):** NCM 70·80wt%가 60wt%보다 0.1C서 약간 높은 areal capacity(절대 질량↑).  단 C-rate↑면 NCM
  고함량 전극 용량 급락 → "an electrode design with a higher NCM content is not effective under high C-rate conditions."

### Fig 4 — 시공간 lithiation(NCM 80wt%, 방전 마지막, 0.1/0.5/1C)
- ~~**SOC ∝ AM 내 lithium 농도**(반비례)~~.  **저율(0.1C):** 잘 분포된·균일한 lithiation; **중/고율(0.5/1C):** 불균일.
  ⟦10-03 PDF 대조⟧ 사유: "∝ … (반비례)" 는 자기모순 표기.  원문(p.5): *"this data indicates that the SOC value of cell is inversely
  proportional to the lithium concentration in the active material"* ⇒ **SOC ∝ 1/c_s** (반비례).  (Table S2 E_eq 의 "soc" 와 축이 반대로
  읽힌다는 점은 위 Table S2 주 참조.)
- **Fig 4a–c**(3.0V 종지) **vs 4d–f**(3.5V): NCM 70wt%가 80wt%보다 더 균일한 lithiation(Fig S15 보강).
  ⟦10-03 PDF 대조⟧ 정확히는 **Fig 4 는 NCM 80 wt% 한 전극뿐** (캡션 p.6: *"Lithiation at the last moment of discharge for a cell in the
  charged state at a) 0.1C, b) 0.5C, and c) 1C at 3.0 V and at d) 0.1C, e) 0.5C, and f) 1C at 3.5 V."*) — 70 vs 80 wt% 비교는 본문 문장 +
  Fig S15(SI p.9, NCM 70 wt%) 로 한다.  Fig S16(SI p.10) 라벨 = "NCM 80 wt%", "Partial Volume over 80% Lithiation".  ★ **In-depth 분석
  (Fig S16):** LPSCl separator에 가까운 NCM 입자가 더 많이 재리튬화 → "sufficient effective electronic conductivity"
  근거.  같은 전압(~3.5V)서도 저율선 우수한 lithiation 분포·밀도.  ⇒ **AM이 완벽히 리튬화/탈리튬화 안 됨** — SE 입자가
  이차입자 내부까지 침투 못해 농도 과전압↑.  해결책 제시: **나노렙 SE 사용 + AM 격자제어로 Li⁺ 확산성↑**.
  ⟦10-03 PDF 대조⟧ "나노렙" = 오타 — 원문(p.5): *"…the use of nanolevel solid electrolyte for filling in pore and the lattice control of
  active materials for higher lithium-ion diffusivity"* · 원인 문장: *"…because the solid electrolyte particles are not infiltrated to the
  interstice of secondary particles"*.

### Fig 5 — 이온 flux(NCM 70 vs 80wt%, 방전 마지막, 0.1/1C)
- ★ LPSCl이 단일이온(t₊≈0.99–1)이라 농도구배 없음 → **flux density**로 분석.  중성전하 균형 → 전류밀도↑면 ion flux↑ 자연증가.
- ★ **"the ion flux from the 80 wt% electrode is higher and less uniform than 70 wt%"** ← NCM↑ → 더 높은 ion flux로
  몰림 + LPSCl↓ → **narrower·more complicated ion pathway** → **higher ohmic resistance in SE 망**(mass transport
  limitation).  ⇒ "new SE materials with higher intrinsic ionic conductivity and better deformation property for
  minimizing the tortuosity"가 필요(직접 인용 — ★ **"deformation property"가 SE 변형성=우리 MPM 소성 void-fill의 가치**).
  ⟦10-03 PDF 대조⟧ 원문 정확 문구(p.5–6): *"It is remarkable to note that the ion flux simulated from the 80 wt% electrode is higher and
  less uniform than that from the 70 wt% electrode."* · *"That is why the new solid electrolyte materials, which have higher intrinsic ionic
  conductivity and better deformation property for minimizing the tortuosity, have been extensively investigated."* (p.6) — 본문 산문에서
  "tortuosity" 가 나오는 **유일한** 자리이며 정의 없이 정성적으로 쓰였다 (정의 쪽은 §4-T).

### Fig 6 — surface overpotential(전기화학 반응 site, NCM 70 vs 80wt%, 방전 마지막, 0.1/1C)
- ★ **NCM 70wt%:** 저율 과전압 ≪ 고율.  **NCM 80wt%:** 저율 과전압이 이미 상당히 높음(고율과 비슷).  Fig S17(충전 후, 양수
  과전압)도 유사.
- ★ **저자 결론(p6 좌측, 직접 인용 가치):** "These significant surface overpotential values can be correlated to the
  **relatively low specific contact area** in comparison to the amount that required for the electrochemical reaction
  to proceed.  Thus, from the perspective of mass transport and electrochemical reaction rate kinetics, these analysis
  data visually demonstrate **why the rate capability of the 80 wt% electrode was poor**."  ⇒ **NCM 80wt% rate 저하 = 낮은
  contact area + 높은 과전압**.  해결: LiNbO₃/halide 코팅·도핑으로 계면 반응속도↑·부반응↓.
  ⟦10-03 PDF 대조⟧ 위 인용은 축약 — 원문 정확 문구(p.6): *"…in comparison to the amount that **is** required for the electrochemical reaction
  to proceed. Thus, from the perspective of mass transport and electrochemical reaction rate kinetics, **these data** visually demonstrate why
  the rate capability of the 80 wt% electrode was poor **in comparison to the other electrodes (Figure 3)**."*  해결책 원문: *"This issue
  has been solved by coating or doping specific materials (LiNbO3, lithium halide, etc.) on electrode materials…"*

### Fig 7 — ASSB 설계 파라미터 맵(전망)
- electrolyte(입경·~~코팅두께·~~porosity·두께), Li metal(코팅·표면형상·두께), cathode(전극밀도·로딩·**component ratio
  20%/40%/60%/80%**·입경형상) — ★ **"Attempted in this work" = cathode component ratio(=우리 AM:SE sweep)**.  나머지는
  미래 디지털트윈 확장 축.
  ⟦10-03 PDF 대조⟧ 사유(취소선): 그림(p.8)의 화살표를 따라가면 **"Particle Coating Thickness" 는 Cathode 쪽**이다.  원문 라벨 전수 —
  **Cathode**: Particle Size & Shape · Particle Coating Thickness · Electrode Density · Electrode Loading Level · Electrode Component
  Ratio / **Electrolyte**: Electrolyte Porosity & Thickness · Particle Size & Shape / **Li Metal**: Coating Material · Surface Morphology ·
  Thickness.  "component ratio" 는 막대 **두 개**(초록 80 % + 노랑 20 % · 초록 60 % + 노랑 40 %) 로 그려져 있고 그 아래에
  "Attempted in this work" 가 붙는다.  캡션: *"Design parameters for an all-solid-state battery with a solid sulfide electrolyte and
  lithium metal electrode."*

⇒ ★ **Phase-4 이식 레시피:** Fig S13 식3–9(BV+질량보존+전류) + Table S2 파라미터 + 단일이온(t₊≈1) flux 근사 ~~+ "핵심전극=
구조분해, 보조도메인=연속체" + "방전부터 검증, 동역학 파라미터 고정·구조변수만 변화"~~가 **우리 PyBaMM DFN(τ·σ 주입) Phase-4의
2020 원형**.  #281(Kim 2026 Li-O₂, COMSOL 1D)·#17(Song 2025, structure-resolved)이 이 라인의 후손.
⟦10-03 PDF 대조⟧ 사유(취소선): 따옴표 두 문구는 **이 논문(본문·SI)에 없다** — 다른 카드의 표현이 섞인 것으로 보인다.  이 논문의
셀은 Li 금속·LPSCl 층·전극·Al 을 **모두 한 복셀 셀**로 놓는다(Fig S13).  ★ τ 주입 주의: DFN 에 이 논문 관례의 τ 를 넣을 때는
**σ_eff = σ·ε/τ (τ = T)** 인지 Bruggeman 지수형(σ·ε^b)인지 먼저 맞춘다 — 환산은 §4-T (3).  ⚠ E_eq 맞춤식의 유효 정의역(soc ≳ 38)
과 soc 축 방향도 위 Table S2 주 참조.

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
| **Fig S8** | ★ specific contact area vs NCM wt%(95k→35k 1/m), w/·w/o dead 거의 겹침.  ⟦10-03⟧ SI p.6 · 재판독 밴드 60 77.8–97.4k · 80 54.4–58.1k · 90 25.4–36.5k (§5) | coverage / A_AM-SE; dead 영향 무시.  ⟦10-03⟧ 단위상 직접 대응은 A_AM-SE/V (§5) |
| **Fig S9** | 전자/이온 density 도메인+지배식(Ohm's law, j=εσ/τ·∇φ)+BC.  ⟦10-03⟧ SI p.6 · Eq [1] j=(ε_sσ_s/τ_s)∇φ_s · [2] j=(ε_eσ_e/τ_e)∇φ_e · BC = 6면 Dirichlet (+x/+y/+z=1, −x/−y/−z=0) · 캡션 인용 [12] | σ_eff 시뮬 셋업(연속체 voxel) · ★ τ 관례의 원문 근거 (§4-T) |
| **Fig S10** | ★ NCM 90wt% dead 제거 후에도 끊긴 LPSCl 망 5 seed | σ_ionic SE-no-perc 시각증거 |
| **Fig S11** | (a)NCM 60wt% 전자밀도 (b)NCM 80wt% 이온밀도, >20 mA/cm² 추출 | 임계 전류밀도 backbone |
| **Fig S12** | NCM 80wt% 이온밀도 >80 mA/cm²(더 제한적) | 고임계 병목 |
| **Fig S13** | ★ stacked cell(Li/LPSCl/전극/Al) + 전기화학 지배식3–9 | Phase-4 지배식 원형 |
| **Fig S14** | ★ 방전용량 시뮬 vs 실험(여러 ref 15) — 1C 편차 ~11 mAh/g.  ⟦10-03⟧ SI p.9 · [15a–d] = **NCM622 + Super C65** 전극(탄소 있음) · 같은 계 실측은 [In this work] NCM711 70:28:2 한 줄 · "≈11"(자기 실측, 1C) 과 "≈12.5"(선행 실험) 은 다른 비교 (§7) | frame[4] 셀-수준 검증 (like-for-like 는 한 줄뿐) |
| **Fig S15** | NCM 70wt% lithiation(0.1/0.5/1C 방전 마지막) | 시공간 lithiation |
| **Fig S16** | NCM 80wt% >80% lithiation 부분부피(separator 근접 NCM↑) | 두께방향 불균일 |
| **Fig S17** | NCM 70·80wt% 충전 후 과전압(양수, 0.1/1C) | 과전압-contact area 상관 |
| **Table S1** | ★ intrinsic σ: NCM 전자 8.5×10⁻⁴ / LPSCl 이온 ~~4.64×10⁻³ S/cm~~ ⟦10-03⟧ **−4.45×10⁻³·ε_s + 4.64×10⁻³ S cm⁻¹** (SI p.11; 4.64 는 ε_s→0 절편일 뿐 — 60–90 wt% 에서 3.08→2.44 mS cm⁻¹) | σ 입력값(intrinsic-driven 근거) · τ 역산의 σ₀ (조성 의존) |
| **Table S2** | ★ 모델 파라미터+OCV식(D_s/D_e/k/c_max/t₊=0.99/E_eq…).  ⟦10-03⟧ SI p.11 · 값 전부 원문 일치 · E_eq 맞춤식은 soc ≲ 35 에서 발산 (§7 주) | Phase-4 파라미터 세트 |
| ⟦10-03⟧ **Nomenclature** | SI p.12(로마자) · **p.13(그리스: ε_e·ε_s = 부피분율, τ_e·τ_s = "tortuosity", η, φ_s·φ_e, σ_s·σ_e)** · 위첨자 eff = effective | ★ τ·ε 정의의 유일한 원문 자리 (§4-T) |

---

## §9. 핵심 수치 한눈 요약 (검증·DB 후보)

- **조성표(wt% → vol%):** NCM:LPSCl:NBR = 60:38:2(35.1:47.7:5.2) / 70:28:2(40.4:34.7:5.1) / 80:18:2(45.0:21.7:5.0) /
  90:8:2(49.4:9.4:4.9).  ★ **NCM vol% = 35.1/40.4/45.0/49.4%** = 우리 AM vol% sweep 대역.  로딩 10 mg/cm², 두께 ~39 µm,
  전극밀도 2.5–2.6 g/cm³.
- **dead particle:** NCM <1%(60wt%서 max ~0.94%, 90wt% 0%); **LPSCl ≤0.5%(60–80wt%) → 90wt%서 6–20%**(stated, Fig S6/S7).
- **σ_eff,e:** NCM wt%↑ → 증가, ~~log ~ −4.5→−3 S/cm~~(Fig 2a, ~~시뮬≈실험~~; 디지타이즈 TREND).
  ⟦10-03 PDF 대조⟧ 재판독: 시뮬 −4.96~−4.20 (60) → −3.93~−3.87 (90) · 실험 −4.25 / −4.07 / **−3.80** (60/70/80; 80 wt% 는 시뮬 밴드 밖·위).
- **σ_eff,ion:** NCM wt%↑ → 감소, ~~log ~ −3→−4 S/cm~~(Fig 2b); **NCM 90wt% = N/A(퍼콜 실패)**.
  ⟦10-03 PDF 대조⟧ 재판독: 시뮬 −3.48~−3.25 (60) → −4.95~−4.30 (80) · 실험 −3.48 / −4.03 / −4.51 = **0.34 / 0.093 / 0.031 mS cm⁻¹** (60/70/80, 30 °C).
- **specific contact area:** ~95,000 → ~35,000 1/m(NCM 60→90wt%, Fig S8); dead 영향 무시.
  ⟦10-03⟧ 밴드 재판독 (w/ dead): 60 77.8–97.4k · 70 69.5–≈81k · 80 54.4–58.1k · 90 25.4–36.5k m⁻¹ (§5 표).
- **specific capacity:** NCM 60→80wt%서 0.1C서도 ~20 mAh/g(~15%)↓; ~~1C 평균 용량편차 ~11 mAh/g(타 모델 >12.5)~~.
  ⟦10-03⟧ 정정: 선행 실험 대비 평균 편차 **≈12.5** (Neumann[14] ≈80) · 자기 실측 NCM 70 wt% 셀 1C 편차 **≈11** (나노 도전재 쓴 다른 연구 >12.5) — 두 비교 (§7).
- **intrinsic σ:** NCM 전자 8.5×10⁻⁴ S/cm, LPSCl 이온 ~~4.64×10⁻³ S/cm(=4.64 mS/cm)~~, t₊≈0.99.
  ⟦10-03⟧ LPSCl 이온 = **−4.45×10⁻³·ε_s + 4.64×10⁻³ S cm⁻¹** → 3.08 / 2.84 / 2.64 / 2.44 mS cm⁻¹ (60/70/80/90 wt%, 우리 산술).
- ⟦10-03⟧ **τ:** 원문 보고 **없음**.  관례 = σ_eff = ε·σ/τ (τ = 우리 T).  역산값(우리 산술, 원문 값 아님 · TREND 전용)은 §4-T (4).
- ⟦10-03⟧ **실험 조건:** 전자 = Van der Pauw 4-probe, 100 MPa 가압 하 · 이온 = e⁻-차단 Li-In/LPSCl/전극/LPSCl/Li-In 대칭셀 EIS (14 mV,
  10 mHz–7 MHz) · 모두 30 °C · **실험 전극 = 60/70/80 wt% 셋뿐** (90 wt% 시뮬 전용).
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
접촉망 순추론)와 정보론적 위상이 다르다**.  ~~그들은 "재료 부피분율·tortuosity"가 입력,~~ 우리는 "접촉 반경·접촉수"가 출력.
⇒ **추세·자릿수 reference이지 점대점 절대 앵커 아님.**  절대 σ 앵커는 **Bazzoun(0.065–0.137)·#271(0.042–0.087)·Varkey·
Minnmann·#266** 유지.  (2023 Battery Energy LPSCl σ_eff 0.0428도 같은 "intrinsic×구조" 위상 — 같은 주의.)
⟦10-03 PDF 대조⟧ 사유(취소선): **τ 는 입력이 아니다.**  입력은 **복셀 구조 + 고유 σ (Table S1)** 이고, τ 는 σ_eff·ε 와 묶여 정의되는
양(σ_eff = ε·σ/τ)이다 — 원문은 τ 를 따로 적지도 입력표에 넣지도 않는다 (§4-T).  보강 세 가지:
- **CONTACT_FREE 위치 (추론):** 이 논문의 σ_eff 계산에는 입자간 접촉·계면 저항 항이 **언급되지 않는다**(Table S1 = 고유 σ 만,
  p.9 = Ohm 법칙 + EJ 솔버).  ⇒ 우리 STEP3 복셀 FV 와 같은 부류 — 접촉망이 스스로 `CONTACT_FREE` 라 부르는 가지 위 (CLAUDE.md
  CL-81).  같은 GeoDict 를 쓴 Bielefeld 2020 은 AM/SE 계면 저항 40 Ω·cm² 를 **명시해 넣었다**(정본 카드 §2.2) — Park 은 그것도 없다.
  단 Park 은 LPSCl 고유 σ 자체를 ε_s 따라 깎는다(3.08→2.64 mS cm⁻¹, 60→80 wt%) — 이 식의 출처가 실측 맞춤이면 일부 순환 [미확인].
- **실험 이온 σ_eff 의 자릿수 (digitized, 30 °C):** 60/70/80 wt% ≈ **0.34 / 0.093 / 0.031 mS cm⁻¹** ↔ Bazzoun(정본 카드, stated,
  400 MPa) 70/75/80 wt% = 0.137 / 0.101 / 0.065.  70 wt% 에서 Park/Bazzoun ≈ 0.68, 80 wt% 에서 ≈ 0.48 — **같은 자릿수**.  ⚠ 같은
  비교가 아니다: NCM711 ↔ NMC811 · LPSCl PSD 피크 ≈8.5 µm(Fig S1) ↔ Bazzoun 의 SE · 슬러리+NBR ↔ 건식 PTFE+CNF · 대칭셀 성형압
  미기술 ↔ 400 MPa · 30 °C.
- **τ 로 다시 보면 (우리 산술, §4-T (4)):** 실험 이온 σ_eff 를 우리 관례(σ₀ = 3.0 mS cm⁻¹)로 바꾸면 T ≈ 4.3 / 11 / 21 (60/70/80 wt%)
  · √T ≈ 2.1 / 3.3 / 4.6 — 웹앱 τ_Lap,eff 와 같은 자리의 숫자다 (같은 침대가 아니므로 비교는 자릿수까지).

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
- ⟦10-03 PDF 대조⟧ **τ 수치 없음 · τ 산출법 미기술** — 이 논문을 "τ 값의 문헌 앵커"로 쓸 수 없다.  쓸 수 있는 것은 **관례**(σ_eff = ε·σ/τ)
  뿐이고, 숫자가 필요하면 Fig 2 판독값에서 되짚어야 한다(§4-T (4), 원문 값 아님 · TREND 전용).
- ⟦10-03 PDF 대조⟧ **방향 불일치 가능성 [미확인]** — 시뮬 경계조건은 6면 Dirichlet 로만 그려져 있어 Fig 2 의 σ_eff 방향을 모른다.
  실험 전자 σ 는 Van der Pauw(4-probe) 로, 이온 σ 는 두께 방향 대칭셀 EIS 로 쟀다 — 원문은 두 측정의 방향 차와 시뮬 방향의 대응을
  논하지 않는다.  80 wt% 전자 실험점이 시뮬 밴드 위로 벗어난 것(§4)의 원인 후보지만 판정 불가.
- ⟦10-03 PDF 대조⟧ **σ_LPSCl(ε_s) 의 출처 [미확인]** — 각주 a,b(설계·실험 설정 + 문헌[18a–c]) 뿐.  자기 복합전극 실측에 맞춘 식이라면
  Fig 2b 의 일치는 일부 순환이고, 그 경우 τ_e 역산값에는 기준 σ₀ 쪽 미세구조 벌점이 섞인다.

---

## §11. 미니 용어집 (이 논문 맥락)

- **digital twin (DT):** 실물의 가상 복제 — 실 형상·물리현상을 디지털 공간으로 전이.  여기선 ASSB 전극의 3D voxel 모델.
- **GrainGeo / BatteryDict / ConductoDict / PoroDict (GeoDict 2020 모듈):** GrainGeo=입자 구조 생성(규칙배치),
  ConductoDict=∇·(σ∇φ)=0 voxel ~~FV~~ 유효전도도, PoroDict=Minkowski measure 구조통계(specific contact area), BatteryDict
  "Design Battery"=stacked 셀 전기화학.  ★ ConductoDict EJ(explicit jump) solver = porous 구조용.
  ⟦10-03 PDF 대조⟧ "FV(유한체적)" 는 원문 표현이 아니다 — 원문은 *"The explicit jump (EJ) solver that has high advantages of solving the
  porous structure"* 라고만 한다 (이산화 방식 미기술).  BatteryDict "Design Battery" 는 **셀 셋업**이고, 전기화학을 **푼** 것은 *"Charge
  Battery (BESTmicro solver, … Fraunhoher ITWM)"* 이다 (p.9).  PoroDict 는 specific contact area 외에 **dead 판정**(Open and Closed
  Porosity, "activated flow boundary conditions")에도 쓰였다.
- **dead particle:** 동종 재료 망에서 물리적으로 고립된 입자(전기화학 비활성).  = 우리 dead-AM / SE-no-perc.
- **specific contact area (1/m):** 단위부피당 NCM-LPSCl 접촉면적 = 반응 site 밀도 = 우리 coverage / A_AM-SE.
  ⟦10-03 PDF 대조⟧ 분모 부피는 원문 미기술 · 산출 = PoroDict Minkowski measures (volume · surface · integral of mean · integral of total
  curvature).  우리 coverage(%) 와는 단위가 달라 직접 대응은 A_AM-SE/V 쪽 (§5).
- **effective conductivity σ_eff = ε·σ_intrinsic/τ:** 부피분율·tortuosity로 가중한 거시 전도도(연속체).  ⚠ 우리 Kirchhoff
  접촉망 σ와 위상 다름.
- ⟦10-03 PDF 대조⟧ **tortuosity τ_e · τ_s (이 논문):** SI p.13 의 *"tortuosity of electrolyte / active material"* — 단위 없음, 값·산출법
  미보고.  Eq S1·S2(SI p.6) 에서 **1제곱**으로 분모에 있다 ⇒ τ = ε·σ₀/σ_eff = **우리 T** = COMSOL τ_F = Bielefeld 2020 의 τ² =
  (웹앱 τ_Lap,eff)².  "factor" 라는 이름은 이 논문에 없다.  자세히 §4-T.
- ⟦10-03 PDF 대조⟧ **겉보기(superficial) 정규화:** 전류·전도도를 **전체 단면**으로 나누는 관례 — 그래서 식에 ε 가 붙는다.  상(相) 단면
  으로 나누면 σ/τ 꼴(ε 없음)이 된다.  이 논문은 명시하지 않지만 식 꼴과 실험 비교가 전자를 가리킨다 (추론).
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
4. ★ **Phase-4 원형(stage4_electrochem_research.md):** Fig S13 식3–9 + Table S2(BV+질량보존+t₊≈1 flux + OCV 6-가우시안)~~ +
   "핵심전극 구조분해·보조 연속체·방전부터 검증"~~ = 우리 PyBaMM DFN 결합의 2020 레시피.  #281/#17이 후손.
   ⟦10-03 PDF 대조⟧ 취소선 문구는 이 논문에 없다(§7 주).  E_eq 맞춤식 정의역(soc ≳ 38)·soc 축 방향을 확인한 뒤에 옮길 것.
5. ⟦10-03 PDF 대조⟧ ★★ **τ 관례는 원문으로 닫혔고, τ 숫자는 원문에 없다.**  이 논문의 σ_eff = ε·σ/τ (SI p.6 Eq S1·S2) 의 τ 는
   **1제곱** 자리 = 우리 **T** = COMSOL τ_F = Bielefeld 2020 의 τ² = (웹앱 τ_Lap,eff)².  ⇒ 같은 GeoDict 계열 두 논문이 **같은 양을
   τ 와 τ² 로 다르게 적는다** — 문헌 τ 를 우리 표에 옮길 때는 **기호가 아니라 식의 꼴(ε 와 τ 의 지수, 정규화 면적)** 로 맞춰야 한다.
   그리고 웹앱의 "COMSOL input = τ_Lap,eff" 라벨은 COMSOL τ_F(= T) 와 제곱만큼 어긋날 수 있다 — 메인 점검 거리 (§4-T (3)).

---

## §13. 참고문헌 — 우리가 더 볼 것 ⟦10-03 PDF 대조⟧

서지는 본문 p.9–10 참고문헌 목록 **그대로**.  "이유" 는 **이 논문이 그 문헌을 어디에 인용했는지**만 근거로 적는다 (그 문헌의 내용은
원문을 안 봤으므로 쓰지 않는다 — 규율 ⑥).  정본 카드 유무 = `litdb/papers/` 파일 내용 grep (10-03).

| 순위 | 서지 (원문 그대로) | Park 2020 이 인용한 자리 | 왜 보나 (한 줄) | 정본 카드 |
|---|---|---|---|---|
| 1 | [12] a) J. Park, D. Kim, W. A. Appiah, J. Song, K. T. Bae, K. T. Lee, J. Oh, J. Y. Kim, Y.-G. Lee, M.-H. Ryou, Y. M. Lee, Energy Storage Mater. 2019, 19, 124; b) J. Park, J. Y. Kim, D. O. Shin, J. Oh, J. Kim, M. J. Lee, Y.-G. Lee, M.-H. Ryou, Y. M. Lee, Chem. Eng. J. 2020, 391, 123528. | **Fig S9 캡션**(ε σ/τ Ohm 식·경계조건) · Table S2 각주 b · 본문 p.2 (유효전도도·접촉면적 예측) | ★ τ 의 **정의·산출법·수치**가 있을 가장 유력한 곳 — 이 논문이 비운 칸을 채울 1순위 | 없음 |
| 2 | [11] Y. Ito, S. Yamakawa, A. Hayashi, M. Tatsumisago, J. Mater. Chem. A 2017, 5, 10658. | σ_eff 계산 문장 끝 **[11,15d,16]** · 본문 p.2 (phase-field 3D 전극) | σ_eff 계산 절차의 인용 출처 — 그 3D 전극 계산에서 τ 를 어떻게 정의했는지 확인 | 없음 |
| 2 | [15] d) Y. J. Nam, K. H. Park, D. Y. Oh, W. H. An, Y. S. Jung, J. Mater. Chem. A 2018, 6, 14867. | σ_eff 계산 문장 끝 **[11,15d,16]** · Fig S14 데이터 [15d] | Fig S14 범례상 NCM622 + LPSCl + Super C65 + NBR 시트 전극(23 mg cm⁻²) — σ_eff 절차의 인용 출처이자 비교 데이터 | 없음 |
| 3 | [18] b) S.-K. Jung, H. Gwon, S.-S. Lee, H. Kim, J. C. Lee, J. G. Chung, S. Y. Park, Y. Aihara, D. Im, J. Mater. Chem. A 2019, 7, 22967; c) L. Froboese, J. F. v. d. Sichel, T. Loellhoeffel, L. Helmers, A. Kwade, J. Electrochem. Soc. 2019, 166, A318 | **Table S1 각주 b** ("literature[18a-c]") | NCM 8.5×10⁻⁴ 와 **ε_s 의존 LPSCl σ 식**의 출처 확인 — 그 σ 가 '고유'인지 이미 '유효'인지(이중계상 여부)가 τ 역산을 좌우 | 없음 (18c 는 `famprikis2019_fundamentals_inorganic_sse` 가 조달 1순위로 추천 · `ketter2025_…` 에 내용 요약) |
| 4 | [14] A. Neumann, S. Randau, K. Becker-Steinberger, T. Danner, S. Hein, Z. Ning, J. Marrow, F. H. Richter, J. Janek, A. Latz, ACS Appl. Mater. Interfaces 2020, 12, 9277. | 본문 p.2 (황화물 X-선 재구성 + 전기화학) · p.4 (≈80 mAh g⁻¹ 편차 비교 대상) | **황화물** 재구성 전극의 두 번째 데이터 — 같은 BEST 계열에서 σ_eff/τ 관례 대조 | 없음 (다른 카드에 언급만) |
| 5 | [19] c) T. Danner, M. Singh, S. Hein, J. Kaiser, H. Hahn, A. Latz, J. Power Sources 2016, 334, 191. | **Fig S13** 지배식 인용 [18f, 19] | 이 논문 셀 모델(BEST 계열) 수송식의 출처 — Phase-4 이식 시 ε·τ 처리 확인 | 없음 |
| 5 | [16] d) X. Li, L. Jin, D. Song, H. Zhang, X. Shi, Z. Wang, L. Zhang, L. Zhu, J. Energy Chem. 2020, 40, 39 | Table S2 각주 b [12, 16d, 18] · σ_eff 절차 [11,15d,16] | D_s·D_e·k 등 전기화학 파라미터 출처 — Phase-4 파라미터 근거 | 없음 |
| 6 | [15] c) D. Y. Oh, Y. J. Nam, K. H. Park, S. H. Jung, K. T. Kim, A. R. Ha, Y. S. Jung, Adv. Energy Mater. 2019, 9, 1802927 | p.8 슬러리 공정 *"as described in a previous report by the authors.[15c]"* · 재료밀도 [15c,16] · Fig S14 [15c] | 실험 전극 제작 공정(NBR·dibromomethane)의 원 기술 — 습식 시트 공정 맥락 | 없음 |
| 7 | [17] a) L. J. Pauw, Philips Tech. Rev. 1958, 20, 220 | 전자 σ_eff 측정법 | 이 측정이 어느 방향의 전도도를 주는지 확인 — §10-(5) 방향 불일치 판단용 | 없음 |
| — | [8] A. Bielefeld, D. A. Weber, J. Janek, J. Phys. Chem. C 2019, 123, 1626. | 본문 p.2 | 이미 있음 | `bielefeld2019_microstructural_modeling_composite_cathode` |
| — | [9] A. Bielefeld, D. A. Weber, J. Janek, ACS Appl. Mater. Interfaces 2020, 12, 12821. | 본문 p.2 | 이미 있음 — **§4-T 의 τ² 대조 짝** | `bielefeld2020_effective_ionic_conductivity_binder` |
| — | [10] T. Shi, Q. Tu, Y. Tian, Y. Xiao, L. J. Miara, O. Kononova, G. Ceder, Adv. Energy Mater. 2020, 10, 1902881. | 본문 p.2 | 이미 있음 | `shi2019_high_am_loading_particle_size_assb` |
| — | [18] a) S. Wang, M. Yan, Y. Li, C. Vinado, J. Yang, J. Power Sources 2018, 393, 75 | Table S1 각주 b | 이미 있음 — NCM711 없음, 8.5×10⁻⁴ 출처 아님 (§4) | `wang2018_lco_nmc_electronic_ionic_conductivity_vs_ni` |
