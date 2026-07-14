# SDCP σ_e 메커니즘 — 최종판 (2026-07-15, CLOSED)

**본문 숫자 = 3.18mAh 실조성 쌍 (σ_e +45.4%)**.  a7_p00 쌍(+33.2%)은 독립 스캐폴드 재현성
보조.  전 지표 원장: `docs/sdcp_318_base_sbe_dbe_comparison.md`.  (구판의 a7-헤드라인 서술은
본 최종판으로 대체 — 2026-07-15.)

## 1. 결론 (논문 결론 문장 그대로)

같은 첨가제 총량(4 wt%)에서 절연 바인더 PTFE의 절반을 혼성전도 SDCP로 치환하면(SBE
70:27:3:1 → DBE 70:27:3:0.5:0.5) **전자 +45.4% · 이온 +5.6% · 반응계면 +18% · R_geom −32%
— 측정한 모든 수송·반응 축에서 이득이고 상쇄 축이 없다.**  메커니즘은 병렬 전도가 아니라
**계면 브리지(직렬 constriction 해소)**: 도로(VGCF 3 wt%, 연결률 100%)는 두 전극이 같고,
전도도를 깎는 것은 교차로(섬유-섬유·섬유-AM 접합부의 좁은 목)다.  랜덤-균일 분산(D = 1.13)된
0.3 µm SDCP 입자가 확률적으로 그 목에 앉아 고전도 브리지가 되면, 브리지 자신은 저항이 낮아
전체 줄(Joule) 저항 손실의 10%만 부담하면서도 그 목을 지나는 경로 전체의 전류를 풀어내
σ_e를 끌어올린다.  유일한 잠재 비용은 기계
축(바인더 반감)이며, 이는 transport 모델 밖 — manuscript의 SDCP 계면-앵커링(SAICAS/DFT)이
담당하는 주장.

## 2. 수치 원장

**3.18mAh 실조성 (본문)** — 동일 스캐폴드(AM 1271, 72.5 µm), 동일 세팅, V100 2026-07-14/15:

| 축 | base(무첨가) | SBE (3:1) | DBE (3:0.5:0.5) | SBE→DBE |
|---|---|---|---|---|
| σ_e_eff (S/cm) | 5.85e-4 | 1.975 | **2.871** | **+45.4%** |
| σ_ion_eff (S/cm) | 9.66e-4 | 2.034e-4 | 2.147e-4 | +5.6% |
| e-손실분담 SDCP (%) | — | 0 | **10.0** | 병렬 산수 불가 |
| ion-손실분담 SDCP (%) | — | 0 | 13.8 | |
| BV 반응면 (AM\|이온상) | 792,503 | 425,349 | **503,922** | **+18%** |
| R_geom (Ω·cm²) | 5.44e-2 | 1.37e-5 | 9.36e-6 | −32% |
| carbon clusters | 0 | 3,172 | 8,644 | ×2.7 |
| 환산접점 중앙값 /AM | — | 433 | 517 | +19.3% |
| SDCP 분산 D / nn× | — | — | **1.13 / ×1.13** | 랜덤급 균일 |
| conductive_all nn_med (µm) | — | 0.304 (×1.41) | 0.282 (×1.34) | 배달거리 단축 |
| porosity / thickness | 9.80% / 68.0µm* | 7.87% / 72.48µm | 7.39% / 72.48µm | (*base는 dilate-z 없음 — 방향 참고) |
| STEP4 i/ī p95 · hot side | 1.65 · 바닥 | 2.32 · 상단 | 2.48 · 상단 | base↔SBE = 지배축 반전 |

**a7_p00 재현 (보조)** — 다른 스캐폴드(2mAh, AM 995, 51.0 µm, porosity ~16%), 명목 3:1 vs
3:0.5:0.5: σ_e 2.12→2.83 (+33.2%) · SDCP e-분담 8.0% · σ_ion +3.6% · 접점 +13.1% ·
클러스터 ×3.2 · SDCP 분산 D 1.14/×1.16.  **같은 시그니처, 다른 침대** — 조밀한 실조성
침대(porosity ~7.5%)에서 증분이 커짐(브리지 기회 증가 방향).

## 3. 메커니즘 — 4축 논증 (작위성 방어의 골격)

**① 손실분담 산수 (병렬-기여 기각)**: SDCP의 전자 줄손실 몫은 10.0%인데 σ_e는 +45.4% —
전도도 이득이 추가 상의 수송 몫을 따라가는 병렬-도체 그림으로는 불가능.  직렬 병목 해소는
가능: 목 하나를 뚫으면 경로 전체 저항이 내려가고, 브리지 자신은 σ=150 S/cm 저저항이라
J²R-가중 손실분담에는 작게 잡힌다(손실분담은 브리지 역할을 구조적으로 과소표시).

**② 접점 기하·분산**: AM당 환산접점 +19.3%(433→517), 전도 클러스터 ×2.7(3,172→8,644) =
~13.7만 개 개별 분산 0.3 µm SDCP(Fig. S3).  공간 통계는 AM-배제 보정 후 완전 랜덤과 구별
불가(index of dispersion 1.13, 최근접거리 = 동밀도 포아송의 1.13×) — **균일-랜덤 배치는
"임의의 틈"에 입자가 앉을 확률을 최대화하는 기하**이고, 이 통계가 스캐폴드·조성이 다른
a7_p00(1.14/×1.16)에서 재현된다 = 파라미터가 아니라 형상(단독입자)의 귀결.

**③ 대안 배제 (고정 관측치)**: porosity(7.87→7.39%)·두께(72.48µm 동일) → 치밀화 아님;
둘 다 집전체 연결 100% → 퍼콜레이션 개시 아님; 절연 PTFE 반감이 주범이면 이온도 함께 커야
하나 이온망은 +5.6%(SDCP가 이온 손실 13.8%를 새로 담당하는데도) → PTFE-해방 기여는 부차.
**크기 논증**: 고립 개재물 유효매질(Maxwell-Garnett) 상한 3φ ≈ +3.9%(SDCP 1.39 vol%) ≪
실측 +45.4%(11.6×) — 부피 산수 기각, 위치가 만든 결과.  같은 입자가 전자망 +45%/이온망
+5.6%를 주는 비대칭 자체가 "σ 입력값이 아니라 네트워크 토폴로지가 결과를 결정"의 증명.

**④ 공간 증거 (σ-공동스케일 필드)**: 두 해의 색을 σ_eff 비율로 정렬(SBE ×0.69, DBE ×1.00★)
한 같은-색자 비교에서 — SBE는 전 영역 남색 연속 채널(병목이 경로 전체 전류를 누름), DBE는
SDCP 접합부 핫스팟이 점등되며 **네트워크 전체 레벨이 상승**.  병렬-도체였다면 기존 VGCF
패턴은 그대로이고 SDCP 위치만 밝아야 한다 — 관측은 반대.  (★비례 근사: |J| 자릿수 ∝ σ_eff,
동일 ΔV·유사 상위꼬리 가정 — 캡션 명시, SI에 자기-정규화판 병기.)

## 4. Main-text 최종 초안 (영문)

> Replacing half of the insulating PTFE binder with the mixed-conducting SDCP at fixed total
> additive loading (SBE: VGCF/PTFE = 3/1 wt% → DBE: 3/0.5/0.5) increases the through-plane
> electronic conductivity of the voxel-resolved electrode by 45.4% (1.975 → 2.871 S/cm),
> improves rather than sacrifices the ionic network (+5.6%), and enlarges the
> reaction-accessible interface by 18% (425,349 → 503,922 Butler-Volmer faces) — the usual
> conductive-additive trade-off (electrons gained at the cost of ions) does not appear,
> because an insulator is being replaced by a conductor of both carriers.  The same
> substitution on an independent scaffold and composition reproduces the effect (+33.2%),
> and four independent readouts of the same solutions identify **interfacial bridging, not
> bulk parallel conduction,** as the mechanism.
>
> First, the SDCP phase dissipates only 10% of the electronic Joule heat: a parallel-conductor
> picture cannot yield a 45% conductivity gain from a 10% transport share, whereas relief of
> series constrictions can — unblocking a junction lowers the resistance of an entire
> percolation pathway while the highly conductive bridge itself dissipates little.  Second,
> the microstructure moves exactly as bridging requires: carbon contact points per AM particle
> rise by 19% and the conductive-cluster count 2.7-fold, contributed by ~1.4×10⁵ individually
> dispersed 0.3 µm SDCP particles whose spatial statistics are indistinguishable from a random
> field (index of dispersion 1.13 after excluding AM-occupied volume; nearest-neighbour
> distance 1.13× the same-density Poisson reference) — random-uniform placement maximises the
> probability of occupying any given inter-fibre or fibre–AM gap.  Third, the alternatives are
> excluded by held-fixed observables (porosity and thickness unchanged; both electrodes fully
> collector-connected; the ionic response bounds the PTFE-removal contribution), and by
> magnitude: the dilute-inclusion effective-medium ceiling for 1.4 vol% of conductor is ≈+4%,
> an order below the observation.  Fourth, current-density fields rendered on a σ-joint colour
> scale show the spatial counterpart: at matched scale the SBE network runs uniformly dim,
> while DBE lights up at SDCP-bridged junctions and brightens as a whole — the direct
> signature of series-constriction relief.

### 4-K. 국문 대역

> 총 첨가제 로딩을 고정한 채 절연 PTFE의 절반을 혼성전도 SDCP로 치환하면(SBE 3/1 → DBE
> 3/0.5/0.5 wt%) 복셀-해상 전극의 두께방향 전자전도도가 45.4% 증가하고(1.975→2.871 S/cm),
> 이온망은 희생이 아니라 개선되며(+5.6%), 반응-접근 계면이 18% 커진다(BV 면 425,349→503,922)
> — 절연체를 양쪽 운반자의 전도체로 바꾼 것이라 통상의 도전재 트레이드오프(전자↑이온↓)가
> 나타나지 않는다.  독립 스캐폴드·조성에서 같은 치환이 효과를 재현하고(+33.2%), 같은 해의
> 네 가지 독립 readout이 메커니즘을 **벌크 병렬전도가 아닌 계면 브리징**으로 지목한다.
> (이하 ①손실분담 10% vs +45% ②접점 +19%·클러스터 ×2.7·랜덤 분산 D=1.13 ③대안 배제 +
> EMT 상한 +4% ≪ +45% ④σ-공동스케일 필드의 전체-레벨 상승 — §3과 동일.)

## 5. Methods 최종 초안 (영문, 국문 대역은 §2-K 구판과 동일 논리)

> **Voxel resistor-network conductivity.**  The compacted MPM microstructure (AM spheres,
> plastically deformed SE continuum, explicitly seeded additives) is rasterised onto a 0.4 µm
> grid; conducting voxel pairs are joined by harmonic-mean face conductances, collector and
> top plate enter as per-column distance-aware couplings, lateral boundaries are insulating,
> and ∇·(σ∇φ)=0 is solved by conjugate gradients (residual <10⁻⁸; assembly verified against
> analytic laminate, single-column and percolation-cutoff solutions).  Electronic (AM, VGCF,
> SDCP conduct) and ionic (SE, SDCP conduct) networks are solved on the same grid; PTFE is
> insulating on both — its volume resistivity exceeds 10¹⁸ Ω·cm (ASTM D257), i.e. σ_PTFE = 0
> is the discretisation of the literature value.  Reported pair-wise comparisons share grid,
> material tables and boundary conditions, so discretisation biases cancel; absolute values
> inherit the voxel-scale contact resolution (0.4 µm fixed against the experimental σ_ionic
> envelope; sub-voxel constrictions unresolved).  Phase-wise dissipation shares are Σg(Δφ)²
> per phase.  Additive dispersion is quantified by (i) the index of dispersion of per-cell
> counts on a 2 µm lattice with AM-occupied cells excluded (complete spatial randomness in
> the accessible matrix = 1.0), and (ii) the median nearest-additive distance from SE material
> points normalised by the same-count Poisson reference; both estimators are calibrated on
> synthetic random, clustered and fibre fields.

## 6. Figure 패키지 (조립만 남음)

| 패널 | 내용 | 캡션 | 에셋 |
|---|---|---|---|
| 메인-1 | σ-공동스케일 |J_e| 필드 SBE vs DBE (투명샷 2장) | §3-④ 영문 캡션 (★근사 명시) | 뷰어: ⚡필드+σ공동✓+이어짐✓+AM✓(종이-회색 고스트)+백본95% → 투명샷×2 (glow는 wiring 전용으로 분리, 2026-07-15) |
| 메인-2 | 전기 배선 도메인캡 SBE vs DBE (공동 스케일 298–673) | "SDCP acts as an interfacial bridge…" (구판 §3 caption 유지) | ⚖ wiring + 투명샷; 컬러바 버튼 |
| 보조 | Δ표 (σ/분담/접점/클러스터) + jrxn 지배축 반전(base↔SBE) | §2 표 | PNG 버튼(합성) |
| 공용 | 컬러바(જet γ1.6, 뷰어 1:1)·컴포넌트 범례·µm 스케일바 킷 | — | `sdcp_figure_assets.pptx` + `sdcp_scalebar_sigma_joint.pptx` (편집 가능 도형) |

## 7. 리뷰어 방어 (작위적 값 아님 — 8항)

1. **결과가 입력에 비례하지 않음**: 같은 SDCP(같은 위치·부피)가 전자 +45.4%/이온 +5.6% —
   σ 테이블을 심어 나오는 효과라면 두 망이 각자 테이블 값을 따라야 한다.  손실분담(10%) vs
   이득(+45%) 불일치가 병렬 가설을 자체 기각.
2. **크기 논증**: EMT(Maxwell-Garnett) 상한 3φ ≈ +3.9% ≪ +45.4% (11.6×) — 부피가 아니라
   위치(토폴로지)의 효과.
3. **동일-세팅 상대비교**: 같은 복셀·σ표·BC, 레시피만 다름 → 이산화 편향 소거.
4. **세 독립 readout + 공간 필드의 정합**: 스칼라(σ)·에너지 분해(분담)·기하 통계(접점/
   클러스터/분산)·공간 필드가 하나의 메커니즘으로만 동시 설명.
5. **재현성**: 독립 스캐폴드(a7_p00)에서 +33.2%·D 1.14 — 시그니처 동일.
6. **문헌 방향 정합**: 도전재의 σ_e↑/σ_ion 잠식(Kim 2024; Cho 2024; Bielefeld 2020)을 레시피
   반전 없이 재현; 전도성-바인더 계면-앵커링 클래스(Kang 2025 bollard; Han 2025 ICEP)와 일관.
7. **검증된 조작점 + 입력 provenance**: 0.4 µm = σ_ionic envelope 고정 검증값; 솔버 해석해
   셀프테스트; 분산 지표 CSR 보정.  σ표는 측정/문헌/가정 3분류로 공개 — PTFE=0은 데이터시트
   (>10¹⁸ Ω·cm)의 이산화 (⚠ Kang 2025 Fig 3c의 "PTFE 0.58 S/cm"은 **전극-수준 4-probe** 값 —
   재료 σ로 넣으면 카본망 이중계상, 오독 주의).
8. **정직 캐비엇 공개** (§8) — 숨긴 가정 없음.

## 8. 정직 캐비엇 / 잔여 (열린 것)

- **σ_SDCP(e)=150 S/cm 잠정** — 랩 펠릿/필름 측정으로 교체 예정 (`--sigma-sdcp`).
  robustness 스윕 {15/50/150} **미실행** — 실행 전 "weakly dependent" 주장 금지 (§F1).
- **σ-공동스케일 = 비례 근사★** — 캡션 명시 + SI 자기-정규화판.  glow = 렌더 장치(물리 아님).
- **기계 축은 범위 밖**: PTFE 반감의 접착 비용(binder_cap 0.645 "under")은 SDCP 계면-앵커링
  (E_bind 재계산 대기)이 담당하는 별도 주장.
- **i/ī p95 2.32→2.48**: "SDCP가 반응 불균일을 낮춘다"는 지지되지 않음 — 균일도 개선 주장 금지.
- 실험 앵커 훅: 대칭셀 SBE/DBE σ 비율(배영진 "얼추 비슷" — 수치 확보 시 §2에 추가),
  3.18mAh 실측 전극 두께(≈72.5µm 검증 → porosity 논란 종결).
- 조성 환산 규약: 카드 wt% = 최종 전극 전체 기준; 70:27:3:1(합101) ↔ 2.97/0.99,
  70:27:3:0.5:0.5 ↔ 2.97/0.495/0.495 (실현 조성 70.37/25.67 wt% 확인).
