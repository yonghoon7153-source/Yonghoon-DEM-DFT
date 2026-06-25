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
