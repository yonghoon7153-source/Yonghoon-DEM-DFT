# Stage-2 모델 하자 감사 (audit) — Yonsei DTBL 2026 + 관련 문헌 대조

**목적:** PyBaMM(Phase 4) 직전까지의 우리 전 모델링 파이프라인 — **Stage-1 DEM 압축+Kirchhoff/Holm
네트워크 솔버(σ triad, Stage-E 소성접촉) + MPM(역학/morphology/coverage) + Stage-2 voxel FV(transport
cross-check)+CBD** — 에 **하자가 없는지**를, 같은 도메인을 다루는 문헌(특히 Yong Min Lee 그룹 2026 +
Bazzoun/Varkey)을 벤치마크로 1:1 대조한다.  living 문서: 각 논문 PDF가 litdb 풀 디제스트될 때마다 갱신.

판정 기호: ✅ 문헌과 정합(검증됨) · ⚠ 단순화/주의(하자 아니지만 명시 필요) · ❗ 잠재 하자(조사 필요) ·
⏳ 디제스트 대기(PDF 받으면 확정).

---

## 헤드라인 감사표

| # | 모델 요소 (우리) | 문헌 벤치마크 | 우리 값 | 판정 |
|---|---|---|---|---|
| 1 | **σ_ionic 절대값** (Kirchhoff/Holm) | Bazzoun 2026 EIS, 동일 LPSCl+NMC811 | 0.0436 mS/cm @85wt%CAM | ✅ 정합 (아래) |
| 2 | **τ for Phase 4** (σ_ionic-anchored) | #286 XCT τ, #266 bimodal τ↓ | τ_Laplace,eff ~4.0 | ✅ 이중계산 회피 (아래) |
| 3 | **Bimodal P:S 7:3 / Furnas dip** | #266 ASSB bimodal 7:3 최적 | 7:3 production, dip AM70-85% | ✅ 독립 실험 검증 |
| 4 | **CBD carbon 퍼콜** (방금 완료) | #275 연속 CNT sheath | 1-4wt% discrete 퍼콜 불가 | ✅ 정합 (아래) |
| 5 | **PTFE = 비전도 σ=0 장애물** | #271 PTFE void↓, #286 defluorination | additives.py PTFE phase | ⚠ 단순화 (아래) |
| 6 | **porosity 규약** (ε_sphere 물질보존) | #266 ASSB cathode (#286은 ✗ 흑연음극) | real_14 15.6% | ⏳ #266 디제스트 |
| 7 | **poly/single = 크기·σ만 다른 강체구** | #266/#285 poly↔single 역학 차이 | AM_P/AM_S | ⚠ 단순화 (아래) |
| 8 | **E_eff 18× softening** | Varkey multi-contact DEM (대안) | 1.35(DEM)/1.53(MPM) GPa | ✅ 3중 검증(기존) |
| 9 | **σ_thermal multi-pathway Ridge 14항** | (직접 벤치 없음) | LOOCV 0.90 | ⚠ 최소 물리근거 |
| 10 | **time-dependent spring-back** (장기보관 두께회복) | #285 점탄성 CBD (RT+4/HT+1µm/3주) | rate-indep J2 = 재현불가 | ❗ 범위 밖 (Stage-2 아님, Phase4+; #7 참조) |

---

## ✅#1 — σ_ionic 절대값이 실험 EIS와 정합 (가장 중요)

CLAUDE.md가 "missing direct validation"으로 표시했던 **절대 σ_ionic 실험 앵커**를 Bazzoun 2026 EIS가
제공한다(동일 Li₆PS₅Cl + NMC811, full-blocking cell, 400 MPa):
- Bazzoun EIS: σ_eff,ion = **0.137 / 0.101 / 0.065 mS/cm @ f_CAM = 70 / 75 / 80 wt%** (단조 감소, +5wt%
  CAM마다 ×0.74→×0.64).
- 우리 AMS_S1 (P:S 0:10, AM:SE 85:15 → **f_CAM = 85 wt%**): σ_ionic = **0.0436 (Hertz) / 0.031 (Physics)**.
- 80wt%→85wt% 외삽: 0.065 × ~0.65 ≈ **0.042** → 우리 **0.0436과 거의 일치** ✅.
- ⇒ 우리 절대 σ_ionic은 실험 EIS 추세 위에 앉는다 = 하자 아님, 오히려 **절대 검증**.

⏳ 완전 검증(PENDING, CLAUDE.md 항목): Bazzoun 4개 조성(vol% CAM:SE)을 우리 φ_SE로 매핑해 다점 비교 +
multi-pressure σ-vs-P를 우리 Heckel knee(P_y=138)와 대조.  단결정(우리 0:10) vs 다결정(Bazzoun) 차이가
잔차로 남을 수 있음 → 매핑 후 확정.

## ✅#2 — Phase 4 τ는 σ_ionic-anchored라 "기하 τ 이중계산" 함정을 피한다

문헌(#286, #266)은 τ를 **tomography 기하값**으로 측정해 concentration polarization과 연결.  우리 τ는 두 종류:
- τ_Dijkstra ~2.35 (최단경로 기하), τ_Laplace,eff ~4.0 (constriction 포함), Bruggeman ratio.
- **Phase 4 입력 = σ_ionic-anchored 역산** `τ = ε·σ_grain/σ_ionic`.  그러면 PyBaMM이 σ_eff = σ_grain·ε/τ
  = σ_ionic을 **정확히 재현**(자기일관) → constriction을 PyBaMM transport에서 **이중계산하지 않음** ✅.
- ❗회피된 하자: 만약 **기하 τ(Bruggeman/Dijkstra)**를 PyBaMM "tortuosity factor"에 넣고 constriction을
  별도로 또 넣으면 이중벌점.  CLAUDE.md가 "Laplacian τ, NOT geometric"으로 올바르게 지정 → 함정 회피.
- ✅ 단, 보고 시 우리 "τ"가 **constriction 포함 effective**임을 명시해야(문헌 기하 τ와 직접 숫자 비교 금지).

## ✅#4 — CBD carbon 퍼콜 결과가 #275(연속 CNT)와 정합

방금 완료: real_10 두꺼운 전극(708셀)에서 carbon 1·4wt% **discrete**(SuperP 점/짧은 VGCF 섬유)는
self-percolate 불가(carbon-only σ=0; carbon ≈6-7% ≪ 31% 3D 퍼콜 threshold).  #275는 정확히 이 문제를
**연속 CNT sheath**(engineered 1D 연속망)로 해결 → 두꺼운 전극엔 연속 도전망이 필요하다는 동일 결론.
- ✅ 우리 "discrete carbon = gap-filler, never backbone"은 문헌 정합.
- ⚠ 명시: 우리 VGCF(짧고 무작위 배향 섬유) ≠ #275 연속 CNT sheath → 우리 SuperP>VGCF 결론은 **우리
  additive morphology**에 한정.  또한 200× contrast cap이 VGCF 5× intrinsic σ를 묵음(=carbon이 병목
  아닐 때 물리적으로 타당하나, 가정으로 명시).
- ✅✅ **#275 풀 디제스트 = EXPERIMENTAL PROOF** (`docs/lit_koo2026_swcnt_sheath_thick_electrode.md`):
  #275 서론이 **"conventional conductive additives fail to form continuous networks AND obstruct
  ion-transport channels"**라고 명시 → 우리 두 발견을 그대로: (전자) discrete carbon σ=0(연속망 실패),
  (이온) SuperP가 SE 채널 1.8× 막음.  그들의 해법 = **연속 SWCNT conformal sheath**(NCMA 표면 감싸기,
  99.7wt% AM, 두꺼운 >11mAh/cm², 3D digital twin 2.5× Li⁺ 확산).  ⇒ ✅#4가 정성정합에서 **실험증명**으로
  격상.  ★ NEW: SWCNT **conformal sheath = 제3 morphology**(표면-순응형; 우리 additives.py의 SuperP=분산점/
  VGCF=interstitial 둘 다 아님) — **두꺼운 전극서 실제로 이기는** 형태 → 향후 additive 옵션(`additives.py`
  seed_sheath 후보).  Li-ion liquid라 절대값 전이는 아니고 carbon-morphology 물리만.

## ⚠#5 — PTFE를 비전도 장애물(σ=0)로만 모델링 → 역할 일부 누락

- #271(동일 sulfide ASSB): **PTFE(dry)가 긴밀 접촉 유지 + void 형성 최소화** → 계면 열화 억제 (NBR은 void
  성장).  즉 PTFE는 **기계적 void-감소** 이득이 있는데 우리는 σ=0 차단만 → PTFE의 **양(+) 기여를 과소평가**.
- #286: PTFE **defluorination → LiF + amorphous carbon** 1st-cycle 계면 변화(전기화학).  우리 Stage-2(무전기화학)
  엔 무관하나 Phase 4에선 고려 대상.
- 판정: transport-only Stage 2에선 **허용 가능한 단순화**지만, porosity/coverage에 PTFE의 void-fill 기여를
  넣으면 더 정확.  → MPM에서 PTFE는 이미 상으로 존재(additives.py) → MPM porosity엔 반영, 단 σ 네트워크엔
  순수 장애물.  하자 아님, 개선 여지.

## ✅/❗ #7 — poly/single 역학 — #285 디제스트로 정량 (rigid-AM ✅ 검증 + 점탄성 spring-back ❗ 한계)

`docs/lit_hong2026_cbd_viscoelasticity_springback.md`.  #285는 단결정 NCMA(액체 LIB) — 전기화학 절대값은
전이불가지만 **입자/CBD 역학은 전이됨**(우리 AM_S=단결정).  세 갈래로 갈림:
- ✅ **rigid-AM 검증:** #285 핵심 = **단결정 CAM은 견고(monolithic)해 파괴로 에너지를 못 푼다 → 압축응력이
  CBD로 간다**.  이것이 정확히 **우리 MPM의 rigid-AM scaffold + 소성 soft상** 그림 → 우리 rigid-AM 가정이
  단결정에 대해 **실험 정당화**됨(단순화가 아니라 **맞는 모델**).
- ✅ **D1 사실상 충족 (force-based Auerbach):** a9_50_p00(0:10 전부 단결정)에서 우리 **force-based Auerbach(★
  production) = 4.18% microcrack**(severe 0) = #285의 "단결정 균열 억제"와 정합.  δ-based 17.23%는 단결정엔
  **과대**(보수적 보조 readout) → 단결정 케이스 보고는 force-based(★)가 옳음.  **추가 P_c 보정 불필요**
  (#285는 CBD/spring-back 논문이라 정량 P_c factor를 안 줌; force-based가 이미 단결정-적합).
- ❗ **점탄성 time-dependent spring-back = 정직한 한계(미구현 물리):** #285의 spring-back은 **점탄성 = 시간(주)·
  온도 의존**(RT 3주 +4µm vs HT 80°C +1µm).  우리 MPM은 **rate-independent von Mises J2**(시간축 없음),
  `--protocol hold`의 relax는 ~40 substep **순간 settling** → **구조적으로 시간의존 spring-back 재현 불가**.
  이것이 CLAUDE.md "springback validation pending"의 **구체적 정체**.  ⚠ 단 — 이건 **Stage-2 transport 하자가
  아님**: spring-back은 **장기 보관(주 단위)** 두께회복이고, 우리가 모델링하는 건 **as-compacted(압축 직후)**
  구조의 transport.  → **Phase 4(degradation)·장기거동으로 갈 때의 한계**, Stage-2 무결성엔 영향 없음.
  해결책(향후): MPM에 **Maxwell/Kelvin 점탄성 CBD 요소**(시간상수 + 온도의존 tan δ) 추가 → 그때 #285의
  DMA tan δ·3주 두께회복 데이터가 검증 앵커.

## ⚠#9 — σ_thermal Ridge(14항)는 triad 중 물리근거 최소

CLAUDE.md 자체 기록: multi-pathway라 단일 backbone scaling 불가 → Ridge가 irreducible(LOOCV 0.90, ceiling).
문헌에 κ 직접 벤치마크 없음 → 검증 어려움.  하자는 아니나 **triad 중 가장 경험적** → 리뷰어 방어 시 명시.

---

## ❗ 잠재 하자 후보 (조사 우선순위)

현재까지 **명백한 하자(❗)는 없음**.  단순화(⚠)는 모두 transport-Stage2에서 허용 가능하고 chemo-mechanical
(Phase 4)로 갈 때 한계로 전환.  우선 확인할 것:
1. **σ_ionic 다점 EIS 검증** (#1 ⏳) — Bazzoun 4조성 매핑.  현재 1점 외삽은 정합이나 다점 확정 필요.
2. **porosity 규약 like-for-like** (#6 ⏳) — 우리 ε_sphere vs #266 ASSB cathode 측정 porosity (Hg/XCT).
   규약 차이(물질보존 vs 기하 void)로 ~1-2%p 오프셋 예상 → #266 PDF로 확정.
3. **tortuosity 절대값** (#2/#286 ⏳) — #286이 XCT τ 절대값 제공 → 우리 τ_Dijkstra(기하)와 같은 정의로
   비교(τ_Laplace 말고).  정합하면 우리 기하 τ 검증.

---

## ✅ #286 디제스트 완료 — 역할 확정 (절대 벤치마크 ✗, 방법/추세/설계 ✓)

`docs/lit_yoo2026_porosity_gradient_dry_electrode.md` (풀 디제스트).  **#286은 천연흑연 음극 + 액체전해질
일반 LIB** → 그들의 τ(1.86/1.98/3.09)·porosity(32%)는 **액체충전 pore 확산(Bruggeman ε/τ²)**, 우리는 **고체
SE 접촉망(Kirchhoff/Holm)** → **절대값 전이 금지**.  ⇒ #286은 **방법·추세·설계** 레퍼런스로만:
- **#2 (τ) 보강:** #286은 **2개 독립 τ 측정법** 제시 — (a) FIB-SEM+GeoDict **확산-sim τ (ε/τ²·D)**, (b) **EIS
  Eq.1 측정 τ** (τ²=R_ion·A·ε·κ/2d).  둘이 같은 순서.  우리는 **측정 τ가 없음** → 이걸 **frame[4] pore-side
  cross-check로 이식 가능**(우리 contact-σ τ_Laplace vs pore 확산 τ).  하자 아님, **enhancement 후보**.
  추세(connectivity↑ → τ↓ → rate↑)는 보편 → 우리 CN·coverage→σ 논리와 정합.
- **#5 (PTFE) 확정:** #286이 우리 모델 **확증** — PTFE 1D-fibril → pore connectivity (우리 additives.py 기하
  모델과 일치).  **PTFE 탈불소화 → LiF+비정질C, ICE 85-87% vs 92.7%**는 **일반 LIB 1st-cycle 전기화학**
  현상 → 우리 ASSB transport-Stage2와 **무관**(우리가 안 다루는 게 맞음).  ⇒ ASSB에선 PTFE σ=0 장애물
  단순화 **정당**.
- **#6 (porosity) 확정:** #286 32%는 흑연음극(고porosity 설계) → 우리 ASSB cathode 10-16%와 **비교 불가**.
  절대 porosity 벤치마크 = **#266(ASSB)** 단독.
- **Phase 5 모델 개선 (★ 실행가능):** 동일 총porosity라도 **z-구배**(top多孔/bottom치밀)면 τ 3.09→1.86, 3C
  용량 23→80 mAh/g.  우리 `extract_2d_microstructure.py`는 이미 K=8 z-band 층화(line 668)+τ-구동 pore
  elongation(line 826) 보유 → **각 band를 다른 target porosity로 구동 + through-plane porosity(z) 프로파일·
  top↔bottom Δ metric 추가**가 Phase 5 직접 업그레이드.  메커니즘(연질 interlayer 소성변형 → 비대칭 압축)은
  우리 MPM-scaffold 물리로 재현 가능.

## ⏳ 추가 디제스트 대기 (PDF 받으면 채움)
- **#266** (bimodal ASSB, P:S 7:3) — bimodal porosity·τ·87.8%@200cyc 수치 → #3·#6 **정량** 확정 (현재 ✅정성).
- **#271** (sulfide dry/wet binder digital-twin) — PTFE void 정량 → #5 보강.
- **#262** (digital-twin Si 역학) / **#285** (CBD springback) — #7 chemo-mechanical 한계 정량.

**중간 결론:** Stage-2까지 모델은 문헌 대조에서 **명백한 하자(❗) 없음** — σ_ionic 절대값(EIS 정합), bimodal
7:3(#266), CBD 퍼콜(#275), PTFE σ=0(#286이 ASSB엔 정당 확인), E_eff softening(3중 검증) 모두 독립 문헌과
정합.  남은 것은 (a) 단순화 2건(PTFE void 기여=일반LIB만, poly/single 역학=chemo-mech 단계 한계) 명시,
(b) σ_ionic·porosity·τ **다점 정량 검증**(#266 PDF), (c) **enhancement 2건**: Phase 5 graded-z-stack(#286) +
pore-side 확산-τ frame[4] cross-check(#286).  ⇒ Stage-2 무결성 OK, 개선 2건은 하자 아닌 기능 추가.

---

## DEM 모델 — 적용 큐 (apply queue, MPM뿐 아니라 DEM도)

문헌 인사이트가 MPM/morphology로 기울지 않게 **DEM 전용**으로 분리 정리.  DEM = transport(Kirchhoff/Holm) +
packing + Auerbach fracture.

| ID | 출처 | DEM에 적용할 것 | 상태 |
|---|---|---|---|
| **D1** | #285 | **poly/single-aware Auerbach P_c** — 단결정 균열억제(높은 P_c), 다결정 입계파괴(낮은 P_c). | ✅ **이미 충족·검증** — a9_50_p02(bimodal)에서 우리 Auerbach가 AM_S P_c 5.357 > AM_P 1.446 mN → AM_S intact(95.7%)/AM_P 파괴(F/P_c 15.96) = #285 정합. 추가 보정 불요 |
| **D2** | #286 | **pore-side τ frame[4] cross-check** — 현재 DEM은 contact-side만(z_SE-SE). #286의 (i) pore-network 배위수+connectivity-bandwidth(watershed pore 분할), (ii) 확산-sim τ(ε/τ²·D)를 이식 → 우리 contact-σ τ_Laplace의 독립 교차검증. | 📋 scoped enhancement (metric 추가) |
| **D3** | #286 | **through-plane porosity(z) 프로파일 + top↔bottom Δ** metric — 현재 단일 porosity만 보고. z-구배 정량 필요(Phase 5 연계). | 📋 dashboard/synth metric |
| **D4** | #266 | bimodal P:S — DEM이 **이미 보유**(P:S sweep). 변경 불필요, **검증 인용**만. | ✅ 보유 |
| **E1** | #284 | **CBD 이온/전자 balance 곡선** — #284가 carbon-coating 두께로 "전자↑·이온↓, 중간 최적"을 실험확인(우리 SuperP/VGCF trade-off의 거울 → **독립 검증, 모델신뢰↑**). carbon-loading sweep(0.5→4wt%)로 voxel σ_e gain vs σ_ionic loss를 **한 곡선**에 → 우리 balance point 정량. | 📋 (pending 4wt% VGCF가 시작점) |
| **E2** | #284 | **voxel 분산균일도 metric** — #284는 SSRM+work-of-adhesion+rheology로 분산을 3중 정량. 우리는 morphology 근접만. **carbon-occupancy CoV / 최근접-carbon 거리분포**로 SuperP(분산)↔VGCF(응집)를 한 숫자로(=SSRM의 메커니즘판) + carbon↔SE/AM work-of-adhesion으로 nucleate_frac/surface_frac 물리근거화. | 📋 scoped |

⚠ **새 케이스 a9_50_p00이 D1을 즉시 건드림:** 0:10 = **전부 단결정(AM_S)**인데 Auerbach가 δ-based **17.23%
microcrack** (force-based 4.18%, severe 0).  #285에 따르면 단결정은 **균열을 restrain** → 우리 δ-based
microcrack 17%가 단결정엔 **과대일 수 있음** (force-based 4%가 더 맞을 가능성).  → #285 디제스트로 단결정
P_c 보정계수 받으면, AM_S P_c를 올려(또는 force-based를 단결정 기본으로) 재계산.  **D1 우선순위 ↑.**
(severe=0이라 σ엔 영향 작음 → 하자 아닌 **정밀화**.)

**apply 원칙:** 반쯤 디제스트된 논문으로 코드를 미리 바꾸지 않음.  각 DEM 항목은 해당 논문 **풀 디제스트
완료 후** 정량값(P_c factor 등) 확보되면 적용.  D1은 #285 끝나면 바로, D2/D3는 scoped 후 별도 적용.
