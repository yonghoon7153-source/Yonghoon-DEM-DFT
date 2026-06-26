# MPM after 25 years: theory, implementation, applications (리뷰) — de Vaucorbeil, Nguyen, Sinaie, Wu (Adv. Appl. Mech. 2020)

> slug `devaucorbeil2020_mpm_after_25_years_review` · DOI `10.1016/bs.aams.2019.11.001` · type `MPM 리뷰(review)` ·
> **OPEN ACCESS** · digested `2026-06-26` · status ✅ · WISHLIST Tier-4 #23
> ⚠ **출처 한정**: PDF 미제공 — 사용자가 붙여준 **Abstract + Introduction(§1.1–1.6) 전문 + 절 스니펫 + 참고문헌/cited-by**
> 기반 digest.  본문 §2–6(전체 수식·알고리즘 11개)은 미열람 → 방법 수식 디테일은 Stomakhin 2013
> (`papers/stomakhin2013_*`)·우리 코드로 보완.  변종 분류·contact·fracture·응용·코드·비교는 intro에서 stated.

## 1. 한 줄 요약
**MPM(Material Point Method)의 첫 종합 리뷰**(339 ref, ~2019까지) — Sulsky 1994 이래 25년의 이론·구현·응용을
한 그림으로 정리.  우리 MPM(`mpm3d_compaction.py`/`mpm2d_*`, Taichi MLS-MPM + von Mises J2)이 **속한 방법론
가족의 지도**이자, 우리 MPM의 정당화(왜 large-deformation 압밀에 MPM이 맞나)·변종 선택·contact/fracture 한계를
문헌으로 anchor.  저자의 오픈소스 코드 **Karamelo**가 **LAMMPS 구조 기반**(= 우리 LIGGGHTS/Taichi 환경과 동류).

## 2. 메타
| 저자 | 출처 | DOI | 유형 |
|---|---|---|---|
| A. de Vaucorbeil, V.P. Nguyen, S. Sinaie, J.Y. Wu (Deakin / Monash, Australia) | Advances in Applied Mechanics **53** (2020) 185–398 | 10.1016/bs.aams.2019.11.001 | 리뷰 (OPEN ACCESS) |

## 3. MPM 기본 개념 (intro stated)
- **Lagrangian 입자(material points) + 고정 Eulerian 배경격자** 하이브리드 (PIC/FLIP 계보; Sulsky 1994가 FLIP을
  고체역학으로 변형).  입자가 **전체 물리상태**(위치·질량·속도·부피·**변형구배 Fₚ**·Cauchy 응력 σₚ·온도·내부변수)를
  운반 → mass conservation 자동.  계산 cycle = **P2G(입자→격자) → grid update(운동량 약형 해) → G2P(격자→입자) →
  grid reset**.  격자 reset 덕분에 **mesh distortion 없음** = large-deformation의 강점 (FEM의 한계 극복).
- 분류: 운동량 약형을 푸는 **Galerkin meshfree**(EFG·RKPM·OTM 류)이되, shape function이 *고정격자 위 단순 다항식*
  이라 타 meshfree(비싼 rational cloud function)보다 구현 쉬움.  격자 안 고정이면 OTM과 유사.

## 4. ★ MPM 변종 (우리가 어디 속하나)
| 변종 | shape function | 핵심 | 우리 대비 |
|---|---|---|---|
| **standard MPM** (Sulsky 1995) | 선형 hat (C⁰) | 원조; **cell-crossing 불안정** | 미사용(C⁰ 노이즈) |
| **GIMP** (Bardenhagen-Kober 2004) | C¹ smooth (유한 입자영역) | cell-crossing 완화 | B-spline류와 동류 |
| **B-spline MPM (BSMPM)** | B-spline | 현재 인기; smooth | ★ **우리 MLS-MPM/B-spline 평활화와 동류** |
| **CPDI** (Sadeghirad 2011) | 사변형/사면체 입자영역 | 극단 인장서 numerical fracture 無 | 미사용(meshing 필요) |
| **TLMPM** (de Vaucorbeil 2020) | total-Lagrangian | 격자가 *초기*형상만 덮음→메모리↓ | 우리는 updated-Lagrangian(ULMPM) |
| **iMPM/MLS** (Sulsky-Gong 2016) | velocity만 MLS | 2차수렴(중간격자)·cell-crossing 제거 | ★ **우리 MLS-MPM이 이 계열** |
→ 우리 MPM = **MLS/B-spline 평활화 ULMPM** (Taichi 88-line MLS-MPM 계열) → intro의 BSMPM/iMPM 가지에 위치.

## 5. ★ Contact & Fracture (우리 MPM 한계의 문헌 근거)
- **Contact**: ★ **no-slip/no-penetration이 MPM에 *내재***(단일값 속도장 → 추가비용 0).  마찰·다물체 분리/슬라이딩은
  **Bardenhagen 다물체(multimaterial) 알고리즘**(2000/2001)이 표준(grain 수에 선형, 분리·슬라이딩·rolling 허용,
  매우 인기).  Nairn(2018)이 임의 마찰법칙(adhesion 포함)으로 일반화.  ⇒ **우리 scaffold MPM이 AM을 *frozen
  obstacle*(am_mask v=0)로 둔 것 = 이 자동 no-penetration contact의 가장 단순한 활용** (AM 표면서 SE가 못 뚫음).
  더 복잡한 마찰/분리 AM-SE contact이 필요하면 Bardenhagen 알고리즘이 경로(단, frame[5]: rigid 접촉망은 DEM 영역).
- **Fracture** (3접근): **discontinuous**(명시적 균열, 다중속도장 = 절점복제, LEFM/cohesive-zone) vs
  **continuous**(damage 변수로 응력 degrade; strain-based + **particle erosion** = 항복입자 deviatoric 0, 질량 유지) vs
  **mixed**(Homel-Herbold 2017 CPDI: continuum damage + self-contact).  ★ 우리 MPM은 **fracture 미구현**(SE 균열 없음);
  yun2023(`papers/yun2023_*`)의 *SE 취성균열*은 이 continuous/cohesive 접근으로 넣어야 = frame[5] 공백.  우리 Auerbach는
  DEM(AM)쪽.

## 6. 응용·코드·비교 (intro stated)
- 응용: geotech(landslide·silo·pile·말뚝)·FSI·**image-based**(voxel→입자; foam 치밀화 Bardenhagen 2005, wood Nairn,
  **low-density snow Lee-Huang**, highly-filled composite) ·computer graphics(Disney Frozen/Big Hero 6/Zootopia; snow
  Stomakhin, sand, hair, lava)·sea-ice·avalanche·explosive.  ★ **image-based foam/composite 치밀화**(voxel→particle,
  다중 contact) = **우리 scaffold(real DEM dump→MPM) 접근의 직접 선례** (Bardenhagen 2005 "foam densification via
  numerical simulation").  Gritton 2017 = **Si anode chemo-mechanical MPM**(배터리 인접).
- 오픈소스 코드: **Karamelo**(저자, C++, LAMMPS 구조)·Uintah(BSAMR, 최고효율)·NairnMPM·CB-Geo·MPM3D(Tsinghua).
  → ★ Karamelo가 **LAMMPS 기반**이라는 점이 흥미: 우리 DEM=LIGGGHTS(=LAMMPS 파생), 우리 MPM=Taichi → 동일 생태.
- 비교: **MPM vs FEM**(large-def서 mesh distortion 없어 MPM 유리, Taylor impact서 MPM이 LS-DYNA FEM보다 빠름) ·
  **MPM vs SPH**(MPM이 더 빠르고 정확, neighbor search 없음·dt가 격자크기 기반) · **MPM vs DEM**(Coetzee/Gracia:
  "적절한 구성식이면 MPM이 DEM 정확도 재현 가능; DEM에서 유도한 구성식으로 MPM 대규모"; Dunatunga-Kamrin 2015
  granular 연속체).  ★ 이 **DEM↔MPM 비교 논의**가 우리 frame[4]/[5](DEM=transport/packing, MPM=mechanics)의
  방법론적 배경 — 저자도 "MPM은 DEM 구성식으로 대규모를, DEM은 정확도를" 분업 시사.
- ⚠ 한계(저자 명시): 수렴 비최적(1D서도 FEM 이하, *매우 고운 격자선 비수렴* — Sulsky-Gong 2016) · BC 부여 어려움 ·
  null-space 이슈 · 큰 메모리(ULMPM).

## 7. 우리 DEM+MPM 대비 (핵심)
- ★ **우리 MPM의 *정당화*와 *계보*를 한 편에**: large-deformation 압밀(SE void-fill·형상변화)에 MPM이 맞는 이유
  (mesh distortion 無)·우리 변종 위치(MLS/B-spline ULMPM)·우리 scaffold(AM frozen)가 MPM 내재 contact의 단순활용임을
  문헌으로 못박음.  Stomakhin 2013(원전 EP-MPM 알고리즘) + Sulsky 1994(MPM 자체) + 이 리뷰(가족 지도) = 우리 MPM
  인용 3종 세트.
- ★ **image-based 치밀화 선례**(Bardenhagen 2005 foam, voxel→particle, multi-contact) = 우리 `--am-scaffold`/`--se-dump`
  (real DEM dump→MPM 격자)의 방법론적 조상.  "image/structure → MPM 입자" 가 확립된 패턴임을 확인.
- ★ **SE 취성균열 = continuous-damage/cohesive MPM 으로 넣는 길**(Homel-Herbold mixed) — yun2023 frame[5] 공백의
  구현 경로(단 우리 J2는 ductile, SE 취성은 별도 damage 필요).
- **DEM↔MPM 분업**을 저자도 시사(MPM=DEM구성식 대규모, DEM=정확도) → 우리 frame[4]/[5] 방법론 배경 보강.
- ⚠ 한계 전사 금지: 리뷰라 LPSCl 물성·porosity·σ 없음(전부 n/a); 방법 수식은 §2–6 미열람이라 Stomakhin/우리 코드로 봐야.

## 8. 인용 가능 문장
- "MPM은 mesh distortion 없이 large deformation·contact·fracture를 다루는 meshfree Galerkin 법으로, 우리 SE 소성
  압밀(void-fill)에 적합하다 (de Vaucorbeil 2020 review)."
- "우리 MPM은 MLS/B-spline 평활화 updated-Lagrangian 변종이며, AM-freeze scaffold는 MPM에 내재한 no-penetration
  contact(Bardenhagen 다물체 계열)의 최소 활용이다."

## 9. 한계 (over-claim 방지)
- **intro 기반 digest** (PDF §2–6 미열람) → 방법 수식·수렴 수치는 미수록; 변종/contact/fracture/응용/코드/비교만 stated.
- 리뷰 = 1차 데이터 0 (porosity/σ/Heckel n/a).  우리에겐 *방법론 지도·정당화·계보*가 가치.
- 전체 PDF 확보 시 §2(일반 MPM)·§5(contact/locking/fluid)·§B(구성식 Johnson-Cook 등)를 추가 digest 권장.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
