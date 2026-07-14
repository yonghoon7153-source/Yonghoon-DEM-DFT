# SDCP σ_e +33% — 논문용 서술 (mechanism + "작위적 값 아님" 방어) — 2026-07-14

대상 데이터: ⚖ 비교 (a7_p00 스캐폴드, 2mAh, 동일 세팅) — **A = SBE** (VGCF:PTFE = 3:1 wt%) vs
**B = DBE** (VGCF:PTFE:SDCP = 3:0.5:0.5).  σ_e 2.12→2.83 S/cm (+33.2%) · σ_ion 1.39e-4→1.44e-4
(+3.6%) · SDCP 손실분담 e 8.01% / ion 10.14% · 환산접점/AM 316→357 (+13.1%) · carbon cluster
1,447→4,698 (×3.2) · porosity 16.15→15.97% · thickness 51.01µm 동일 · econn 100/100 ·
R_geom 1.25e-5→1.21e-5 Ω·cm².

핵심 논지(리뷰어 프레임): **+33%는 모델에 "심어진" 값이 아니라, 같은 솔루션의 서로 다른 세
readout이 교차로 가리키는 구조적 결과** — (i) 병렬-기여 산수로는 불가능한 손실분담 8% vs +33%
(직렬 병목 해소 시그니처), (ii) 접점 +13%·클러스터 ×3.2·랜덤급 분산(D=1.14) — 브리지가 요구하는
기하 변화, (iii) 대안 가설(치밀화·퍼콜 개시·PTFE 해방)이 고정된 관측치들로 각각 배제.

---

## 1. Main-text 초안 (영문)

> Replacing half of the PTFE binder with SDCP at fixed total additive loading (SBE:
> VGCF/PTFE = 3/1 wt% → DBE: VGCF/PTFE/SDCP = 3/0.5/0.5 wt%) increases the through-plane
> electronic conductivity of the voxel-resolved electrode by 33% (2.12 → 2.83 S/cm) while
> leaving the ionic conductivity essentially unchanged (+3.6%).  Three independent readouts
> of the same numerical solution identify **interfacial bridging, not bulk parallel
> conduction,** as the dominant mechanism.
>
> First, the share of electronic Joule dissipation occurring inside the SDCP phase is only
> 8%.  A parallel-conductor picture — in which the conductivity gain tracks the added
> phase's own transport share — cannot yield a 33% gain from an 8% share.  Relief of
> series constrictions can: unblocking a narrow junction lowers the resistance of an entire
> percolation pathway, while the bridge itself, being highly conductive, dissipates little
> (dissipation is J²R-weighted and therefore systematically understates the role of
> low-resistance bridges).
>
> Second, the microstructure changes in exactly the way bridging requires.  The median
> number of carbon contact points per AM particle rises by 13% (316 → 357) and the number
> of distinct conductive clusters rises 3.2-fold (1,447 → 4,698), reflecting ~6×10⁴
> individually dispersed 0.3 µm SDCP particles (Fig. S3) whose spatial statistics are
> indistinguishable from a random field (index of dispersion 1.14 against 1.0 for complete
> spatial randomness after excluding AM-occupied volume; nearest-neighbour distance 1.16×
> the same-density random reference).  Uniformly random placement is the geometry that
> maximises the probability of a particle sitting in *any* given inter-fibre or fibre–AM
> gap.
>
> Third, the alternative explanations are excluded by observables held fixed across the
> pair: porosity (16.2 → 16.0%) and thickness (51.0 µm) are unchanged, ruling out
> densification; both electrodes are already fully collector-connected (100%), ruling out a
> percolation onset; and halving the insulating PTFE would relieve ionic and electronic
> transport alike, whereas the ionic network — which SDCP additionally serves, carrying 10%
> of the ionic dissipation — improves by only 3.6%.  The two cases are solved on the same
> voxel grid with identical numerics and material tables; only the recipe differs, so
> discretisation and solver biases cancel in the comparison.

### 1-K. 국문 대역 (검토용 — 본문은 위 영문 기준)

> 총 첨가제 로딩을 고정한 채 PTFE의 절반을 SDCP로 치환하면(SBE: VGCF/PTFE = 3/1 wt% →
> DBE: 3/0.5/0.5) 복셀-해상 전극의 두께방향 전자전도도가 33% 증가하고(2.12→2.83 S/cm)
> 이온전도도는 사실상 불변이다(+3.6%).  같은 수치해의 서로 다른 세 가지 readout이 지배
> 메커니즘을 **벌크 병렬전도가 아니라 계면 브리징**으로 지목한다.
>
> 첫째, SDCP 상 내부에서 발생하는 전자 줄(Joule) 손실은 전체의 8%뿐이다.  전도도 이득이
> 추가된 상의 수송 몫을 따라가는 병렬-도체 그림으로는 8% 몫에서 33% 이득이 나올 수 없다.
> 직렬 병목(constriction) 해소로는 가능하다: 좁은 접합부 하나를 뚫으면 그 퍼콜레이션 경로
> 전체의 저항이 내려가는 반면, 브리지 자신은 고전도라 손실이 거의 없다(손실분담은 J²R
> 가중이라 저저항 브리지의 역할을 구조적으로 과소표시한다).
>
> 둘째, 미세구조가 정확히 브리징이 요구하는 방향으로 변한다.  AM 입자당 카본 접점 중앙값이
> 13% 증가하고(316→357) 전도 클러스터 수가 3.2배(1,447→4,698) — 이는 개별 분산된 0.3 µm
> SDCP 입자 ~6×10⁴개(Fig. S3)를 반영하며, 그 공간 통계는 랜덤 필드와 구별 불가다
> (AM-점유 부피 제외 후 index of dispersion 1.14 vs 완전 랜덤 1.0; 최근접거리 = 동밀도
> 랜덤 기준의 1.16배).  균일-랜덤 배치는 "임의의 섬유-섬유·섬유-AM 틈"에 입자가 앉을
> 확률을 최대화하는 기하다.
>
> 셋째, 대안 설명들은 쌍에서 고정된 관측치로 배제된다: porosity(16.2→16.0%)·두께(51.0 µm)
> 불변 → 치밀화 배제; 두 전극 모두 이미 집전체 100% 연결 → 퍼콜레이션 개시 배제; 절연체
> PTFE의 반감이 지배 원인이라면 이온·전자 수송이 함께 좋아져야 하나, SDCP가 이온 손실의
> 10%를 새로 담당하는데도 이온망 개선은 +3.6%에 그침.  두 케이스는 동일 복셀 격자·동일
> 수치·동일 물성표로 풀렸고 레시피만 다르므로, 이산화·솔버 편향은 비교에서 소거된다.

## 2. Methods 초안 (영문)

> **Voxel resistor-network conductivity.**  The compacted MPM microstructure (AM spheres,
> plastically deformed SE continuum, and explicitly seeded additive material points) is
> rasterised onto a 0.4 µm voxel grid.  Each conducting voxel pair is joined by a
> harmonic-mean face conductance g = 2σᵃσᵇ/(σᵃ+σᵇ)·Δx, current collector and top plate are
> applied as per-column, distance-aware Dirichlet couplings, lateral boundaries are
> insulating, and ∇·(σ∇φ)=0 is solved by conjugate gradients (residual < 10⁻⁸; the assembly
> is verified against analytic laminate, single-column and percolation-cutoff solutions).
> The electronic and ionic networks are solved on the *same* grid with phase-wise
> conductivities (electronic: AM, VGCF, SDCP conduct; SE, PTFE insulate — ionic: SE, SDCP
> conduct; AM, VGCF, PTFE insulate).  Reported comparisons are between runs at identical
> grid, tables and boundary conditions, so they are **relative** statements about
> microstructure; absolute values inherit the voxel-scale contact resolution (0.4 µm was
> fixed against the experimental σ_ionic envelope, and sub-voxel constriction is not
> resolved).  Phase-wise dissipation shares are Σ g·(Δφ)² accumulated per phase.
> Additive dispersion is quantified on the as-seeded point clouds by (i) the index of
> dispersion of per-cell counts on a 2 µm lattice, with AM-occupied cells excluded so that
> complete spatial randomness in the accessible matrix reads 1.0, and (ii) the median
> nearest-additive distance from SE material points, normalised by the same-count Poisson
> reference (3·ln2/4πn)^⅓; both estimators are calibrated on synthetic random, clustered
> and fibre fields.

### 2-K. 국문 대역

> **복셀 저항망 전도도.**  압밀된 MPM 미세구조(AM 구, 소성변형 SE 연속체, 명시적으로 seed된
> 첨가제 재료점)를 0.4 µm 복셀 격자에 래스터화한다.  전도 복셀 쌍은 조화평균 면 컨덕턴스
> g = 2σᵃσᵇ/(σᵃ+σᵇ)·Δx로 잇고, 집전체·상부 플레이트는 컬럼별 거리-인지 Dirichlet 결합,
> 측면은 절연 경계로 두고 ∇·(σ∇φ)=0을 CG로 푼다(잔차 <10⁻⁸; 어셈블리는 적층/단일컬럼/퍼콜
> 차단 해석해로 검증).  전자망·이온망은 **같은 격자** 위에서 상별 전도도로 푼다(전자: AM·
> VGCF·SDCP 전도, SE·PTFE 절연 — 이온: SE·SDCP 전도, AM·VGCF·PTFE 절연).  보고되는 비교는
> 동일 격자·물성표·경계조건 런들 사이의 **상대** 진술이며, 절대값은 복셀-스케일 접촉 해상도
> 한계를 물려받는다(0.4 µm는 실험 σ_ionic envelope에 맞춰 고정; sub-voxel constriction은
> 미해상).  상별 손실분담은 Σ g·(Δφ)²를 상별로 누적한 값.  첨가제 분산은 as-seeded 점군에서
> (i) 2 µm 격자 셀별 점수의 index of dispersion(AM-점유 셀 제외 → 접근가능 매트릭스의 완전
> 랜덤 = 1.0), (ii) SE 재료점에서 최근접 첨가제까지의 중앙값 거리를 동수 포아송 기준
> (3·ln2/4πn)^⅓로 정규화한 비 — 두 추정자 모두 합성 랜덤/응집/섬유 필드로 보정.

## 3. Figure caption 초안 (⚖ 표/패널)

> **SDCP acts as an interfacial bridge, not a parallel conductor.**  Paired voxel solves of
> the SBE (VGCF/PTFE 3/1 wt%) and DBE (3/0.5/0.5 wt% with SDCP) electrodes on identical
> grids.  DBE gains +33% electronic conductivity while SDCP carries only 8% of the
> electronic dissipation; carbon–AM contact points rise 13% and conductive-cluster count
> 3.2-fold, while porosity, thickness and collector connectivity are unchanged and the
> ionic network improves by only 3.6% — together isolating series-constriction relief at
> fibre–fibre and fibre–AM junctions as the operative mechanism.

### 3-K. 국문 대역

> **SDCP는 병렬 도체가 아니라 계면 브리지로 작동한다.**  동일 격자에서 SBE(VGCF/PTFE
> 3/1 wt%)와 DBE(3/0.5/0.5, SDCP 포함) 전극을 짝지어 푼 복셀 해.  DBE는 전자전도도 +33%를
> 얻지만 SDCP가 담당하는 전자 손실은 8%뿐; 카본-AM 접점은 13%, 전도 클러스터 수는 3.2배
> 증가하는 반면 porosity·두께·집전체 연결률은 불변이고 이온망 개선은 +3.6%에 그침 —
> 종합하면 섬유-섬유·섬유-AM 접합부의 직렬 constriction 해소가 작동 메커니즘으로 격리된다.

## 4. "작위적 값이 아니다" — 리뷰어 방어 포인트 (국문, 순서대로 쓰기)

1. **결과가 입력 파라미터에 비례하지 않는다.**  같은 SDCP(같은 위치·같은 부피)가 전자망에는
   +33%, 이온망에는 +3.6%를 준다.  σ 테이블 값을 심어서 나오는 효과라면 두 망 모두 자기
   테이블 값에 비례해야 한다 — 실제로는 **네트워크 기하(어느 틈에 앉았나)가 결과를 결정**했다.
   같은 이유로 손실분담(8%)과 σ 이득(+33%)의 불일치도 병렬-기여 가설을 자체 기각한다.
2. **동일-세팅 상대비교.**  두 케이스는 같은 복셀 크기·같은 σ표·같은 솔버·같은 경계조건으로
   풀렸고 레시피만 다르다.  이산화 편향과 sub-voxel 한계는 공통이라 비교에서 소거된다
   (절대값 주장 아님 — trust 문구에 명시).
3. **세 독립 readout의 정합.**  σ(전역 스칼라), 손실분담(에너지 분해), 접점/클러스터/분산
   (기하 통계)은 서로 다른 후처리인데 하나의 메커니즘(브리지)으로만 동시에 설명된다.
4. **대안 가설의 명시적 배제.**  치밀화(porosity·두께 불변), 퍼콜 개시(양쪽 100% 연결),
   PTFE-해방(이온 개선 부재)이 각각 관측치로 반증됨.
5. **방향의 외부 정합.**  도전재가 σ_e를 올리며 SE-도메인을 잠식해 σ_ion을 해치는 상반 효과는
   랩 실험(Kim 2024 carbon SE-domain occupation; Cho 2024 VGCF의 양면성)과 GeoDict 계열
   (Bielefeld 2020, binder 부피↑ → σ_ion 급감)에서 확립된 방향이고, 본 모델은 같은 방향을
   레시피 반전 없이 재현한다.  전도성-바인더 클래스의 계면-앵커링 개념(자가도핑 SDCP; 유사
   클래스 Kang 2025 bollard-anchored binder, Han 2025 ICEP)과도 일관.
6. **검증된 조작점.**  0.4 µm 복셀은 σ_ionic 실험 envelope에 맞춰 고정한 검증값이고, 솔버는
   해석해(적층/단일컬럼/퍼콜 차단) 셀프테스트를 통과하며, 분산 지표는 합성 랜덤/응집/섬유
   필드로 보정(CSR=1.0)되어 있다.
7. **남은 가정을 숨기지 않는다(정직 캐비엇).**  σ_SDCP(전자)=150 S/cm는 잠정 입력이며
   manuscript pellet 앵커(σ_e ×5.1)로 교체 예정.  단, +33%의 성립 조건은 "브리지가 그것이
   대체한 틈(진공/SE)보다 충분히 전도적"이라는 것뿐이므로 결론은 σ_SDCP 크기에 약하게만
   의존할 것으로 예상 — **robustness로 σ_SDCP ∈ {15, 50, 150} payload-only 스윕을 SI에 수록
   권고** (동일 raster 재솔브, GPU 수 분).  ⚠ 이 스윕은 아직 미실행 — 실행 전에는 본문에
   "weakly dependent"를 주장하지 말 것 (§F1).

## 5. 수치 원장 (그대로 인용)

| 축 | SBE (A) | DBE (B) | Δ |
|---|---|---|---|
| σ_e_eff (S/cm) | 2.12 | 2.83 | **+33.2%** |
| σ_ion_eff (S/cm) | 1.39e-4 | 1.44e-4 | +3.6% |
| e-손실분담 SDCP (%) | 0 | 8.01 | — |
| ion-손실분담 SDCP (%) | 0 | 10.14 | — |
| 환산접점 중앙값 /AM | 316 | 357 | +13.1% |
| carbon clusters | 1,447 | 4,698 | ×3.2 |
| porosity (%) | 16.15 | 15.97 | −1.1% |
| thickness (µm) | 51.01 | 51.01 | 0 |
| econn (%) | 100 | 100 | 0 |
| R_geom (Ω·cm²) | 1.25e-5 | 1.21e-5 | −3.2% |
| SDCP 분산 D / nn× (DBE) | — | 1.14 / 1.16 | 랜덤급 균일 |

조성 환산 규약: 카드 wt% = 최종 전극 전체 기준.  실험 70:27:3:1(합 101) ↔ 입력 2.97/0.99;
70:27:3:0.5:0.5 ↔ 2.97/0.495/0.495.  (a7_p00 계열은 3/1·3/0.5/0.5 명목 — 실제-조성판은
3.18mAh 스캐폴드 런으로 교체 예정.)

## 6. ★ 실조성 재현 — 3.18mAh 스캐폴드 (2026-07-15, V100 런) = 본문 헤드라인 숫자

manuscript 조성 그대로(70:27:3:1 ↔ 70:27:3:0.5:0.5; 실현 AM 70.37/SE 25.67 wt%)를 실제
3.18mAh DEM 스캐폴드(AM 1271, 두께 72.5µm) 위에서 재실행 — **§1의 메커니즘 시그니처가 전부
재현되고 크기는 더 큼**.  a7_p00 쌍(+33%)은 재현성/보조, **본문 숫자는 이 쌍(+45%)**.

| 축 | base(무첨가) | SBE (3:1) | DBE (3:0.5:0.5) | SBE→DBE |
|---|---|---|---|---|
| σ_e_eff (S/cm) | 5.85e-4 | 1.975 | **2.871** | **+45.4%** |
| σ_ion_eff (S/cm) | 9.66e-4 | 2.034e-4 | 2.147e-4 | +5.6% |
| e-손실분담 SDCP (%) | — | 0 | **10.0** | (병렬 산수로 +45% 불가) |
| ion-손실분담 SDCP (%) | — | 0 | 13.8 | |
| R_geom (Ω·cm²) | 5.44e-2 | 1.37e-5 | 9.36e-6 | −32% |
| carbon clusters | 0 | 3,172 | 8,644 | ×2.7 |
| STEP4 BV faces (AM\|이온상 반응면) | 792,503 | 425,349 | **503,922** | +18% (SDCP 반응-접근 계면) |
| STEP4 i/ī p95 | 1.65 (바닥-hot) | 2.32 (상단-hot) | 2.48 (상단-hot) | 지배축 반전은 base↔SBE |
| porosity (%) | 9.80 | 7.87 | 7.39 | (DBE 첨가제 부피 +0.57vol%) |
| SDCP 분산 D / nn× | — | — | **1.13 / 1.13** | a7의 1.14/1.16과 재현 일치 |
| conductive_all nn_med (µm) | — | 0.304 (×1.41) | 0.282 (×1.34) | 배달거리 단축 |

- **EMT 크기 논증 (a7보다 더 강함)**: SDCP 1.385 vol%(고체) ≈ 1.28 vol%(전극) → Maxwell-Garnett
  고립 개재물 상한 3φ ≈ **+3.9% ≪ 실측 +45.4% (11.6×)** — 부피 산수 기각, 위치(브리지) 지배.
- **재현성 축**: SDCP 분산 D(1.14→1.13)·nn×(1.16→1.13)이 다른 스캐폴드·조성에서 거의 동일 =
  "랜덤-균일 나노분산" 서사가 seeding 파라미터가 아니라 형상(0.3µm 단독입자)의 귀결임을 지지.
- **증분 크기의 스캐폴드 의존(+33→+45%)**: 같은 부호·같은 시그니처, 더 조밀한 실조성 침대
  (porosity ~7.5% vs 16%)에서 브리지 이득이 커짐 — 접점 밀도가 높을수록 병목 해소 기회가 많다는
  방향으로 일관 (정량 분해는 후속).
- ★ **부수 발견 — 첨가제의 반응계면 상쇄와 SDCP의 부분 복원**: base→SBE에서 BV 반응면이
  792,503→425,349(−46%) — VGCF/PTFE가 AM 표면을 점유하며 AM|SE 반응계면을 잘라먹는 대가
  (전자 +3,400×의 숨은 비용).  DBE는 SDCP의 AM|SDCP 면이 반응면으로 복귀해 +18%(425k→504k)
  회복 — "SDCP = 혼성전도 배달부"가 반응-접근성 축에서도 정량 확인됨 (base는 dilate-z 유무가
  달라 SBE↔DBE 비교가 엄밀; base 값은 방향 참고).  base↔SBE의 **반응 hot-side 반전**(바닥→상단,
  전자지배→이온지배)은 §STEP4 대비쌍으로 별도 그림.
