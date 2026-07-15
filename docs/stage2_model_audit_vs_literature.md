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
| 1 | **σ_ionic 절대값** (Kirchhoff/Holm) | Bazzoun + **#271** EIS, 동일 LPSCl+NCM | DEM ~0.04–0.18 mS/cm | ✅✅ 다점 검증 (envelope 0.04–0.14) |
| 2 | **τ for Phase 4** (σ_ionic-anchored) | #286 XCT τ, #266 bimodal τ↓ | τ_Laplace,eff ~4.0 | ✅ 이중계산 회피 (아래) |
| 3 | **Bimodal P:S 7:3 / Furnas dip** | **#266** ASSB bimodal (정확값) | a9_50 dip min p06 (6:4) | ✅✅ **정량 1:1** (dip모양·opt·σpeak·endpoint) |
| 4 | **CBD carbon 퍼콜** (방금 완료) | #275 연속 CNT sheath | 1-4wt% discrete 퍼콜 불가 | ✅ 정합 (아래) |
| 5 | **PTFE = 비전도 σ=0 장애물** | **#271** PTFE void−6.4%p·팽창1.74 (정량) | additives.py PTFE phase | ⚠ 양(+)기계역할 누락 → MPM --coh (E3) |
| 6 | **porosity 물리값** (MPM 소성) | **#266** He pycnometry 8.83% @CAM7:3 | MPM 10.44% @p06 | ✅ like-for-like (~1.5%p; DEM rigid는 floor offset) |
| 7 | **poly/single = 크기·σ만 다른 강체구** | #266/#285 poly↔single 역학 차이 | AM_P/AM_S | ⚠ 단순화 (아래) |
| 8 | **E_eff 18× softening** | Varkey multi-contact DEM (대안) | 1.35(DEM)/1.53(MPM) GPa | ✅ 3중 검증(기존) |
| 9 | **σ_thermal multi-pathway Ridge 14항** | (직접 벤치 없음) | LOOCV 0.90 | ⚠ 최소 물리근거 |
| 10 | **time-dependent spring-back** (장기보관 두께회복) | #285 점탄성 CBD (RT+4/HT+1µm/3주) | rate-indep J2 = 재현불가 | ❗ 범위 밖 (Stage-2 아님, Phase4+; #7 참조) |
| 11 | **σ_e 조성방향** (single vs poly 누가 전도↑) | **#266** σ_NCWA(poly)13.7≫σ_NCM(single)2.45 | 우리 σ_e: single-rich↑ (반대) | ⚠ 재료(σ_AM endpoint)-의존 → 재검토 (아래) |

---

## ✅#1 — σ_ionic 절대값이 실험 EIS와 정합 (가장 중요)

CLAUDE.md가 "missing direct validation"으로 표시했던 **절대 σ_ionic 실험 앵커**를 Bazzoun 2026 EIS가
제공한다(동일 Li₆PS₅Cl + NMC811, full-blocking cell, 400 MPa):
- Bazzoun EIS: σ_eff,ion = **0.137 / 0.101 / 0.065 mS/cm @ f_CAM = 70 / 75 / 80 wt%** (단조 감소, +5wt%
  CAM마다 ×0.74→×0.64).
- 우리 AMS_S1 (P:S 0:10, AM:SE 85:15 → **f_CAM = 85 wt%**): σ_ionic = **0.0436 (Hertz) / 0.031 (Physics)**.
- 80wt%→85wt% 외삽: 0.065 × ~0.65 ≈ **0.042** → 우리 **0.0436과 거의 일치** ✅.
- ⇒ 우리 절대 σ_ionic은 실험 EIS 추세 위에 앉는다 = 하자 아님, 오히려 **절대 검증**.

✅✅ **2번째 절대 앵커 = #271 (Hong 2026, 동일 LPSCl+NCM, digital-twin)** — `docs/data/hong2026_sigma_ionic.csv`:
LPSCl 양극 EIS σ_ionic = **Pwd 0.087 / S-Pwd 0.079 / PTFE 0.064 / NBR 0.042 mS/cm** (350 MPa).  우리 DEM
production 범위(**~0.04–0.18**) 안에 정확히 들어가고, Bazzoun(0.065–0.137)과 합쳐 **LPSCl+NCM σ_ionic
엔벨로프 ≈ 0.04–0.14**를 형성 → **우리 DEM 출력이 그 안에 앉는다.**  조성추세도 정합(coverage/φ_SE↓→σ↓:
Pwd LPSCl-coverage 35%/σ 0.087 → NBR 26%/σ 0.042).  bulk LPSCl **1.87** mS/cm도 (Bazzoun pellet 1.02,
Cronau single-crystal 3.0) 사이 = GB-incl 다결정 범위로 일관.  ⇒ **audit #1: 1점 외삽(Bazzoun) → 2독립
EIS 데이터셋이 둘러싸는 다점 검증.**
⏳ 잔여(point-to-point): 압력 차(Hong 350 / Bazzoun 400 / 우리 300 MPa) + Hong vol% 미제공 → 엔벨로프
정합이지 1:1은 아님; 압력·vol%→φ_SE 매핑하면 점대점 확정.  하지만 **절대값 검증은 사실상 닫힘**(envelope).

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
- ✅⚠ **#19 (Kim 2025, Battery Energy) = SAME-SYSTEM(LPSCl+NCM) 실험 — ✅#4 두 축으로 정밀화** (`docs/lit_kim2025_conductive_agent_se_coating_assb.md`):
  CA를 **SE-coating-on-CAM**에 혼입.  σ_e SE@CAM 3.3e-2 → **SE-SP 1.0e-5(3자릿수 붕괴, Super-P-rich 코팅이 CAM
  표면 차단)** → SE-VGCF 1.4e-2(회복); σ_ion **SE-SP 0.9 < SE@ 1.3 < VGCF 1.6 (×1e-4)**, ASA SP가 절반(0.51).
  ⇒ **VGCF(1D) > Super P(0D) 실험**.
  - **(이온축) ✅ 강화**: SuperP가 이온 더 막음 = 우리 voxel(SuperP 0.0168 < VGCF 0.0298) **방향을 같은 LPSCl
    시스템 실험으로 직접 확인**(#275는 NCMA/liquid 전이 필요했지만 #19는 직접).  단 directional ordering(절대 1.8× 아님).
  - **(전자축) ⚠ regime 차이**: 실험 VGCF>SuperP(**SE-coating**), 우리 voxel SuperP>VGCF(**bulk gap-filler** 1wt%,
    density가 dead-AM mop-up).  **carbon 위치가 "density"의 부호를 뒤집음**(bulk=이득 / coating=차단).  우리
    SuperP>VGCF는 **bulk-gap-filler corner 한정 맞음**; 성능 가르는 SE-coating regime은 VGCF 승.
  - **❗ 모델-setup gap (E4)**: `additives.py`가 carbon을 **bulk 간극에만** seed → SE-coating-on-CAM의 Super-P-rich
    차단(σ_e 3자릿수 붕괴)을 **표현 못 함** → 향후 `se_coating_interface` carbon 옵션이 fix.  #19+#275(같은 그룹)
    = ASSB서 1D/연속 carbon이 0D/discrete를 이김(same-system + general 둘 다).

## ⚠#5 — PTFE를 비전도 장애물(σ=0)로만 모델링 → 양(+)의 기계 역할 누락 (#271로 정량)

- ❗ **#271(동일 LPSCl ASSB, 풀 디제스트) — PTFE의 양(+) 기계 역할이 ASSB에서 실재·지배적**:
  PTFE(dry, confined fibril) → **pore-vol 28.7→22.3 vol% (−6.4%p, void 억제)**, 부피팽창 1.74 < Pwd 1.88,
  접착 2×, retention 94.6%(최고).  순 σ_ionic 0.064 = Pwd의 74%(차단−치밀화 상쇄 후).  우리는 **σ=0 차단(음)만**
  모델 → **void 억제·치밀화(양)를 빠뜨림** → PTFE-case porosity **과대예측** + σ_ionic **과소예측** 위험.
  ⇒ defluorination(#285/#286, 액체 LIB-only, ASSB 무관)과 **다른 새 축**: "PTFE 기계적 void-억제 미모델".
  **구현 lever:** MPM에 PTFE를 **cohesion 상**으로(`--coh` PTFE 항) → void-억제·치밀화 재현; 검증 앵커 = #271
  pore-vol(28.7→22.3)·팽창(1.74).
- NBR(wet, 광범위 coverage → void 성장, σ 0.042 최저, rock-salt 17-22nm)은 **wet 공정 특화 → 우리 dry-side
  모델 무관**(전이 안 함).
- 판정: transport-only Stage 2에선 σ=0 단순화가 **σ_ionic 엔벨로프엔 여전히 정합**(#271 PTFE 0.064도 우리 범위
  안) → **Stage-2 하자 아님**.  단 PTFE-case **porosity·치밀화 정밀도**를 위해 MPM --coh PTFE 항이 개선 lever
  (E3).  Phase 4 degradation에선 PTFE void-억제가 retention을 가르므로 필수.

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

## ✅ #266/#271 디제스트 완료 — 정량 검증 닫힘 + σ_e caveat (2026-06-25)

- **#3 (bimodal) ✅✅ 정량 1:1** — `docs/a9_50_ps_sweep_vs_bimodal266.md` §CLOSED + `docs/data/oh2026_bimodal_sigma_porosity.csv`.
  우리 a9_50 DEM sweep이 #266 실험 Furnas dip을 **dip모양·최적위치(p06 6:4↔CAM7:3)·σ_ion peak(0.0506↔0.055)·
  endpoint rebound** 전부 1:1 재현 (frame[4]).
- **#6 (porosity) ✅ like-for-like** — #266 He pycnometry **8.83%** @CAM7:3 ↔ 우리 **MPM 10.44%** @p06 (~1.5%p).
  DEM rigid 12.70%는 rigid floor로 위(소성흐름 없음) → **물리값=MPM, dip모양=DEM** (frame[5] 깨끗).
- **#1 (σ_ionic 절대값) ✅✅** — Bazzoun + #271 + #266 = 3 독립 LPSCl+NCM EIS가 우리 DEM(~0.04–0.18)을
  감싸는 엔벨로프 ~0.03–0.14 형성.
- **★ Tier-1 Cronau 2021 (σ_grain 출처) — 값 OK / 라벨 3중 오류** (`docs/lit_cronau2021_stack_pressure_ionic_conductivity.md`):
  우리 σ_grain=3.0 mS/cm "**Cronau 2022 Li6PS5Cl single-crystal**"은 **(i) 연도 2022→2021, (ii) 소재 Cl→실제 Br
  (그 논문은 Li6PS5Cl 미측정; Li6PS5Br만), (iii) "single-crystal" 거짓 — 전부 GB-포함 pellet σ**.  실제 최댓값은
  µC-Li6PS5Br **2.40 mS/cm**(550℃ anneal, 392MPa-fab).  ⇒ **값 3.0은 방어가능**(2.4 plateau + 타 LPSCl 1–6 문헌
  blend, well-sintered 상단) but **라벨 정정 필요**(연도·Br·GB-pellet; NOT single-crystal).  Cronau(r_SE) 서브-µm
  sigmoid도 **반경법칙 아님**(논문은 σ-vs-radius 미플롯) — 실제는 **결정성(sintering) class 효과**(µC→GB gap→σ↓)
  → 방향만 맞고 breakpoint(0.5/0.3/0.1/0.03µm)는 **경험적 외삽** → "particle-size decay"를 **"crystallinity/
  grain-contact 효율 인자"로 재명명** 권고(값·LOOCV +0.0043 유지).  ★ 보너스: **fabrication(300MPa) vs
  stack(40–70MPa) 압력 분리** + inter-lab **10× 분산**(Ohno/Zeier round-robin) = 우리 envelope 허용폭 + E_eff
  softening + Heckel P_y=138 + σ-vs-P ~400MPa saturation을 **"압력이 grain contact를 닫아 σ 포화"** 서사로 통합.
- **★ #22 Park 2020 (FOUNDATIONAL ROOT) ✅ frame[4] 4건** (`docs/lit_park2020_digitaltwin_assb_foundational.md`):
  계보 시조(2020) — 우리 정확한 소재계(LiNbO₃-NCM711+LPSCl+NBR) + 조성축(NCM 60–90wt%).  ① 최적창 NCM
  60–80wt%(dead LPSCl ≤0.5%→90wt%서 6–20%) ↔ 우리 dead-AM 회피대; ② **NCM 90wt% σ_eff,ion=계산불가
  (LPSCl 퍼콜 단절, Fig S10) ↔ 우리 σ_ionic SE-no-perc degenerate(2mAh_real_16, 8mAh_real_11) 1:1**;
  ③ dead-SE 6–20% ↔ 우리 SE-퍼콜 취약 corner; ④ σ_eff,ion↓ with NCM ↔ 우리 form.  ⚠ σ_eff=intrinsic×ε/τ
  연속체(voxel-FV) **출력**(접촉망 아님) → 추세·자릿수만, 절대앵커는 Bazzoun/#271/#266 유지.  ★ positioning:
  **시조 논문조차 GeoDict 규칙배치**(GrainGeo+BatteryDict; press 미시뮬) → 우리 process-physics가 계보 ROOT 능가.
- **#5 (PTFE) — #271로 정량** (void −6.4%p) + **E3 lever 보강(#264)**: SBR 가교도 modulus↑→무결성 = 같은
  결론(PTFE/SBR 수렴).  #264 힌트: `--coh`는 **비단조(과가교 X14 agglomeration→하락) cap 곡선** + binder
  modulus(MPa)는 SE E_eff(1.53 GPa)와 **별개 항**(3–4 자릿수 차).
- **⚠ #11 σ_e 조성방향 (새 caveat, #266이 잡음)**: #266 σ_e는 **poly(NCWA 13.7) ≫ single(NCM 2.45)** →
  CAM10:0(poly) 4.09 > CAM0:10(single) 0.95.  우리 a9_50 σ_e는 **반대**(P↑→감소; single-rich가 높음 —
  접촉망 조밀 + endpoint 가정 σ_S-single 10 > σ_P-poly 5).  **포로시티·σ_ion·fracture는 깨끗이 1:1인데
  σ_e만 방향 반대.**  원인 = σ_AM endpoint **재료-의존**(#266 NCWA는 W-doped 고전도 poly; 우리 Trevisanello
  NCM811 가정은 single이 높음).  → **하자라기보다 재료-특이 가정**이지만, CLAUDE.md σ_e endpoint(σ_S=10/
  σ_P=5)가 #266 재료엔 sign-flip → **σ_e form 재검토 대상**(Phase 3 predictor 전, 조성-σ_e 방향을 재료별로
  분리하거나 σ_AM을 입력으로).  porosity/σ_ion 검증과 **분리해서** 관리.
  ★ #22 Park 2020: **σ_eff,e↑ with NCM wt%** = 부피분율 지배 → 우리 **φ_AM⁴ 항 방향 확증**(부피축); Park은
  입경/σ_S/σ_P endpoint 축은 안 다룸(NCM711 고정).
  ★★ **#11 VERDICT — σ_S/σ_P "Trevisanello" 출처 = MIS-ATTRIBUTION 확정** (Tier-1 Trevisanello 2021 digest +
  코드 grep, 2026-06-25; `docs/lit_trevisanello2021_sc_pc_ncm_cracking_diffusion.md`): Trevisanello 2021은
  **단·다결정 NCM의 bulk 전자전도도 σ_e를 측정한 적이 없다** — Li⁺ 화학확산(cm²/s)·BET 활성표면적·R_ct(液체셀)
  만 측정.  우리 σ_S=10/σ_P=5 mS/cm + "Trevisanello" 인용은 **값·출처 둘 다 오배선**(코드
  `generate_comparison_plots.py:5712-13` 주석은 S=poly/P=single로 **라벨 혼동**까지).  게다가 그 논문 유일한
  단·다결정 비율(기하표면적 **SC 0.84 > PC 0.17 m²/g**)은 오히려 "single이 높음" 가정과 **반대**.  ⇒ #11은
  "재료-의존 caveat"가 아니라 **확정 mis-attribution + 미검증 sign 가정**.  #266(W-doped NCWA poly 13.7≫single
  2.45)은 Trevisanello와 **모순 아님**(그 논문이 σ_e에 침묵) → σ_AM은 **재료·도핑-특이**가 맞다.
  ★ **권고 (Phase 3 전; 코드변경은 사용자 승인 후)**: (1) σ_S/σ_P를 **재료-특이 INPUT**으로(LOCKED single>poly
  sign 제거); (2) 전자 endpoint의 Trevisanello 인용 수정/제거 + S/P 라벨 혼동 정리; (3) NCM(r)=1/(1+(r/2)^1.5)는
  **방향만 Trevisanello 지지**(큰 poly 동역학 불리, PSD median ~2µm로 r0=2 검증), 형태·β=1.5는 **우리
  corpus-fit** → "Trevisanello β=1.5" 표기를 "Trevisanello spirit + corpus-fit"으로 재표기, 전자-GB가 아니라
  확산/dead-AM 채널로 옮길지 검토.  ⚠ liquid-vs-ASSB: 그 논문 "crack=이득(액체 침투→표면적↑·R_ct↓)"은 ASSB서
  **부호 반대**(고체 SE는 crack 못 메움 → 접촉손실=손해) → 우리 fracture/Auerbach 채널이 이미 **고체 부호
  (crack=손해)**로 옳음(대조 교차검증).  SC=무결정립=우리 작은 AM_S(F/P_c<1, #285) phenotype 일치.

**최종 결론 (논문 13편 디제스트 후):** Stage-2 transport 모델 **명백한 하자(❗) 없음** — σ_ionic 절대값(3 EIS
앵커 envelope), bimodal dip(#266 1:1), CBD 퍼콜(#275 실험증명), PTFE σ=0(#271 정량, E3 lever), E_eff
softening(#266 E_SE 22 = 3중 확인) 모두 독립 문헌과 정합/검증.  남은 것: (a) **σ_e endpoint mis-attribution 수정
+ σ_AM 재료-input화**(⚠#11 **CONFIRMED** — Trevisanello엔 단·다결정 σ_e 없음; Phase 3 전, 코드변경 사용자승인),
(b) 단순화/범위밖 명시(점탄성 spring-back #10, poly/single 역학 #7; **scaffold MPM SE-poor over-compression
regime限** = DEM 영역, 별도 기록), (c) enhancement
(Phase5 graded-z #286, pore-τ #286/#281 DiffuDict, MPM --coh PTFE/SBR E3, dispersion CoV E2).  ⇒ **Stage-2
무결성 OK + 정량 검증 닫힘**; σ_e 방향만 Phase 3 전 점검.

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
