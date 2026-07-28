# Positioning — 우리 DEM+MPM 파이프라인 vs GeoDict (상용) — "돈 내고 쓰는 GeoDict 이상"

**계기:** Yong Min Lee 그룹의 2026 논문들(#276 리뷰, #281 A3D, #284 SiOx, #286 porosity-gradient, #275 SWCNT)이
**전부 GeoDict**(Math2Market, 상용)로 미세구조→유효물성을 뽑는다.  이 패턴을 보고 — **우리 파이프라인은
GeoDict가 하는 일을 포함하면서 GeoDict가 구조적으로 못 하는 두 가지를 더 한다.**  논문 significance의 핵심.

## GeoDict이 하는 일 (그들이 돈 내고 쓰는 것)

GeoDict = **구조 → 유효물성 특성화 엔진**.  **주어진(given) 미세구조**가 입력:
- 입력 미세구조 출처: CAD/리소그래피(#281), 또는 토모그래피 XCT/FIB-SEM(#286/#284).  **GeoDict이 구조를
  만들지 않는다 — 측정하거나 설계해서 넣어줘야 한다.**
- voxel화 후 연속체 PDE를 격자에서 풂:
  - **ConductoDict**: ∇·(σ∇φ)=0 → 유효 σ_e/σ_ion
  - **DiffuDict**: 정상 Fick → 유효 D
  - **MatDict**: SSA·porosity
  - (FlowDict: Stokes → permeability 등)
- 출력: **그 구조의** 유효 수송물성.  구조 IN → 물성 OUT.

## 우리가 만든 것 (무료/오픈: LIGGGHTS scipy Taichi)

| 기능 | GeoDict | 우리 | 비고 |
|---|---|---|---|
| **미세구조 생성/예측** (압력·조성·입경·첨가제 → 구조) | ✗ (구조를 줘야 함) | ✅ **DEM+MPM 압축 시뮬** | ★ GeoDict 구조적으로 불가 |
| 연속체 유효 σ/D (voxel FV) | ✅ ConductoDict/DiffuDict | ✅ `voxel_conductivity.py` | 우리가 복제(무료); voxel≈σ_full 교차검증 |
| **granular 점접촉 constriction σ** (Holm/Kirchhoff) | ✗ (연속체라 놓침) | ✅ **DEM 접촉망 솔버** | ★ 연속체는 σ_contact-free 상한만 |
| 소성 morphology·void-fill·strain field | ✗ | ✅ **MPM** | |
| 입자 파괴 (Auerbach) | ✗ | ✅ | |
| σ triad (ionic+electronic+thermal) + Stage-E 소성접촉 + 문헌 σ_grain | 부분(σ만) | ✅ 전체 | |
| 예측 scaling law (design knobs → σ 직접) | ✗ | ✅ Phase 1 완료 | |

## ⇒ 우리 문제(공정→ASSB cathode 미세구조+수송 예측)에서 우리는 GeoDict의 **superset**

1. **구조를 예측한다** (GeoDict은 줘야 함) — **입력측**.  이게 가장 큰 차이: GeoDict 사용 논문들은 전부
   "이미 만든/측정한 구조"를 특성화할 뿐, **압력·조성에서 구조가 어떻게 나오는지 예측 못 한다.**  우리 DEM+MPM이
   그걸 한다.
2. **유효물성을 뽑는다** (GeoDict의 일) — voxel_conductivity로 복제(무료).
3. **연속체가 놓치는 접촉망 constriction σ를 잡는다** (frame[5]) — granular SE 점접촉의 진짜 σ_ionic은
   Kirchhoff/Holm 접촉망이 필요; GeoDict 연속체 FV는 **σ_contact-free 상한**만 줌(우리 voxel도 동일 한계 →
   그래서 생산 σ_ionic은 DEM).  우리는 **둘 다** 갖고 있어 그 차이(constriction overhead)까지 정량.

## ⚠ 정직하게 — GeoDict이 여전히 앞서는 것 (over-claim 금지)

- **성숙도·검증·견고성**: GeoDict 연속체 솔버는 상용으로 광범위 검증·복잡 형상 robust.  우리 voxel은 핵심을
  복제하고 우리 케이스서 교차검증(voxel≈σ_full)했지만 **범용 연속체 대체는 아님**.
- **모듈 폭**: FlowDict(permeability), 열·기계 등 다양한 물리 — 우리는 전지전극 특화.
- **워크플로 polish**: GUI·포맷·자동화.
- ⇒ "GeoDict보다 낫다"가 아니라 — **우리 특정 문제(granular 전지전극을 공정에서 예측+수송)에선 superset**;
  범용 연속체 특성화 도구로서는 GeoDict이 표준.  우리 voxel은 그 한 조각(ConductoDict/DiffuDict)을 무료로
  맞춘 것 + **그들에게 없는 예측·접촉망**을 더한 것.

## 논문 significance 한 문장

> "선행 연구들(#276/#281/#284/#286/#275)은 미세구조→유효물성을 상용 GeoDict로 **특성화**한다(구조는 측정/
> 설계로 주어져야 함).  본 연구는 (i) **공정(압력·조성)에서 미세구조를 예측**하는 DEM+MPM, (ii) 그 위의
> **연속체 유효물성**(voxel FV, GeoDict ConductoDict/DiffuDict에 상응), (iii) 연속체가 놓치는 **granular
> 점접촉 constriction σ**(Kirchhoff/Holm 접촉망)를 하나로 묶어, **주어진 구조의 특성화를 넘어 공정→구조→
> 수송을 예측**하는 오픈 파이프라인을 제공한다."

→ #281 frame[5](입력측 예측 vs 출력측 특성화) + #276(descriptive 리뷰 vs predictive 엔진)과 동일 논지의,
**가장 구체적·검증가능한 버전**(GeoDict이라는 명시적 비교 대상).

## ★★ 결정적 강화 — 이 분류는 "내가 만든 distinction"이 아니라 **필드(이 그룹)의 자기 taxonomy**

`docs/lit_choi2024_digital_twin_review_echem.md` (이용민 DTBL의 디지털트윈 방법론 총설, E.Chem 매거진 Vol16):
이 리뷰가 §"3D 디지털 트윈 구조체 형성 방법론"에서 **하향식(top-down / reconstruction)** vs **상향식(bottom-up
/ formation)** 두 범주를 **명시적으로 정의**한다.  ⇒ 위의 "GeoDict = 구조-given 특성화(top-down) ↔ 우리
DEM+MPM = 공정에서 구조-예측(bottom-up)"은 **내가 발명한 구분이 아니라 우리가 비교/이식하는 바로 그 그룹의
자기 방법론 리뷰가 NAMING한 필드 표준 taxonomy**다.
- 우리 DEM+MPM = **상향식(bottom-up / formation)** 범주에 정확히 속함.
- GeoDict 사용 논문(#266/#271/#281/#284/#286/#275) = **하향식(top-down / reconstruction)** 범주.
- 추가로 그 리뷰의 **DTP(digital twin prototype, design-side, 물리시스템 미연결) vs DTI(instance, 연결)**
  구분에서 우리 DEM+MPM = **DTP**(설계측 예측).
⇒ positioning이 **"우리가 만든 distinction" → "필드 taxonomy 안에서 우리 위치"**로 격상 = peer-review 최강.
한 문장에 추가: *"… 본 연구의 bottom-up/formation 접근(Choi et al., E.Chem 2024 분류)은 top-down/
reconstruction 도구(GeoDict 기반 선행연구)와 상보적이되, 공정→구조 예측 + 접촉망 constriction σ에서 그를 넘어선다."*

★★★ **peer-review 인용은 ACS EL 원본을 써라:** E.Chem 총설은 그룹의 peer-reviewed **Suhwan Kim, Hyobin Lee,
Jaejin Lim, Joonam Park, Yong Min Lee, "Digital Twin Battery Modeling and Simulations: A New Analysis and
Design Tool for Rechargeable Batteries," ACS Energy Lett. 2024, 9, 5225-5239, DOI 10.1021/acsenergylett.4c01931**
(Focus Review; **H. Lee·J. Lim 공동1저자** = 우리가 positioning 대상으로 삼는 #266/#271/#262 모델러들; 총설
Fig들이 "[Ref 127 재구성 ⓒ2024 ACS]")의 한국어 확장판.  ⚠ 디스크립터 정합: ACS EL 원본은 **electrode =
"percolation pathway"**, **"pore network" = separator** (총설이 pore-network를 electrode로 오기) → 라벨은
원본 기준.  풀 디제스트 `docs/lit_kim2024_digital_twin_acsenergyletters.md`.  ⇒ taxonomy의
출처는 **우리가 positioning 대상으로 삼는 바로 그 그룹의 peer-reviewed 자기 논문** = 최강 근거.  논문엔 ACS EL
원본을 인용.
★ 추가 결정타(원본/총설 §3): **bottom-up 정의가 "DEM·FVM 등이 활용되며, 입자 간 상호작용과 압축 하의 형상
변화를 모델링"이라고 DEM/FVM을 명시**하고, **그 bottom-up 예시가 LPSCl + NCM 70 wt%**(우리 정확한 소재계).
즉 그들 taxonomy가 **우리 도구(DEM+MPM)와 우리 시스템(LPSCl+NCM)을 bottom-up의 본보기로 직접 거명**.  우리는
그 bottom-up 안에서도 **"process-physics-driven" 최강 sub-type**(확률적 배치 #263가 아니라 압축역학 인과).
(단 그들 Fig 6c "압연 DEM 공정모델: 압축–spring-back–접촉/다공/굴곡"의 **spring-back은 우리 MPM 미구현 gap
#285** — 그 그림은 청사진이자 우리 future-work 근거.)

## ★★ 시조까지 거슬러 — 계보의 ROOT(2020)조차 GeoDict 규칙배치 (#22 Park 2020)

풀 디제스트 `docs/lit_park2020_digitaltwin_assb_foundational.md`.  **Park, …, Yoon Seok Jung, Yong Min Lee,
"Digital Twin-Driven All-Solid-State Battery," Adv. Energy Mater. 2020, 10, 2001563** — 이 디지털트윈-ASSB
계보의 **시조(2020)**, 우리 정확한 소재계(LiNbO₃-NCM711+LPSCl+NBR).  ★ 논문 Experimental이 **GrainGeo
(GeoDict 2020)로 입자 배치 + BatteryDict/ConductoDict/PoroDict로 물성**이라 명시 — 즉 **시조부터 GeoDict**.
구조 형성법 = "변형성 LPSCl을 입자 간극에 **규칙으로 배치**(reflecting PSA sizes → minimal porosity), NBR을
사이에 추가" = **press를 시뮬하지 않음**(top-down/reconstruction × 규칙배치, #263 bucket).  ⇒ 디지털트윈-ASSB
계보가 **시조(2020 Park) → 2023 Battery Energy → #271 → #266 → #281 → #286 → 2024 #18 taxonomy까지 전부
top-down/GeoDict 규칙배치**; 우리 DEM+MPM process-physics(압력·조성 → 구조 인과)는 **그 계보 전체의 ROOT를
능가하는 유일한 bottom-up**.  ★ Park의 *"deformable LPSCl → minimal porosity"* 규칙 = 우리 **MPM 소성
void-fill의 2020 언어 원형**(frame[5]): 그들은 **말로 규칙**, 우리는 **물리로 계산**.  ⇒ positioning 한 문장에
추가 가능: *"… 본 접근은 디지털트윈-ASSB 계보의 시조(Park 2020)부터 최신 리뷰(#18 2024)까지 일관된
GeoDict 규칙배치(top-down)와 달리, 공정 압축역학에서 구조를 인과적으로 예측하는 bottom-up이다."*

---
*정본 승격 2026-07-28 — 원본 `claude/solid-state-cathode-improvement-hevry0:docs/positioning_vs_geodict.md`*
