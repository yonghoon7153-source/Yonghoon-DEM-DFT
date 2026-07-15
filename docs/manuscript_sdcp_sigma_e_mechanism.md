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

**지표 정의 (표 읽기 전에):**

> **Kirchhoff 저항망이란**: 전극을 0.4 µm 복셀로 잘게 나눈 뒤, 이웃한 전도 복셀 쌍마다 작은
> 저항(컨덕턴스 g = 두 복셀 σ의 조화평균 × 접촉면적/거리)을 연결해 **수백만 개의 저항으로 된
> 거대한 회로**로 취급하는 방법.  각 복셀(노드)에 "들어온 전류 = 나간 전류"라는 Kirchhoff
> 전류법칙(KCL)을 강제하면 연립방정식 ∇·(σ∇φ)=0이 되고, 아래(집전체 φ=1)/위(φ=0)에 전위를
> 걸어 풀면 복셀마다의 전위 φ와 면마다의 전류 g·Δφ가 나온다.  총 전류 I에서 σ_eff =
> I·L/(A·ΔV).  요약: **옴의 법칙 + 전하보존만으로 실제 기하(병목·우회로·막다른 길)를 그대로
> 반영해 푸는 정확해** — Bruggeman/EMT 같은 평균장 근사가 못 보는 constriction·토폴로지
> 효과가 전부 들어가며, 본 문서의 σ·손실분담·전류밀도 필드가 모두 이 해에서 나온다.

| 지표 | 뜻 |
|---|---|
| σ_e_eff / σ_ion_eff | 두께방향 **유효 전자/이온 전도도** — 0.4µm 복셀 Kirchhoff 저항망 해 (S/cm) |
| 손실분담 (dissipation share) | 전극의 총 저항 손실(열) 중 **그 재료 안에서 발생한 몫**(%) = 그 재료가 전극 전체 저항에서 차지하는 비중.  DBE 전자망 = VGCF 90 / SDCP 10 / AM 0.2.  ⚠ "전류를 얼마나 나르나"와는 다른 양 — 상세는 바로 아래 설명 블록 |
| BV 반응면 | STEP4에서 전자망과 이온망이 결합되는 **AM\|이온상(SE·SDCP) 인접 복셀면 수** = 충전 반응이 일어날 수 있는 계면 면적의 proxy (래스터에서 자연히 나옴 — coverage-native) |
| R_geom | 바닥 접점 **기하**가 만드는 계면저항 = L·(1/σ_bare − 1/σ_wetted).  측정 R_int − R_geom = 화학/열화 몫 (모델 출력이지 입력 아님) |
| carbon clusters | 서로 닿은 탄소(VGCF/SDCP)로 이뤄진 **독립 전도 클러스터 수** — 많을수록 분산된 전도 섬이 많다는 뜻 (연결성 자체는 econn이 담당) |
| 환산접점 중앙값 /AM | AM 표면 0.3µm 안에 있는 카본 점 수를 서브샘플 가중(전체/표시)으로 되돌린 값의 입자 중앙값 — "AM 하나가 탄소망에 몇 점으로 물렸나" |
| SDCP 분산 D / nn× | D = 2µm 셀 격자 점수의 분산/평균 (AM-점유 셀 제외, **완전 랜덤=1**, 클수록 응집).  nn× = SE→최근접 SDCP 거리 중앙값 ÷ 동밀도 랜덤 기대값 (≈1 = 랜덤급 균일 커버) |
| conductive_all nn_med | SE 매트릭스 임의 지점에서 **가장 가까운 전도상까지의 중앙값 거리** (µm) — 전자 "배달 거리" |
| porosity / thickness | MPM settled 공극률 / 압축면 두께 (SBE·DBE는 dilate-z 1.0711 공통 — base만 무확장이라 방향 참고) |
| STEP4 i/ī p95 · hot side | 입자별 충전 반응전류의 상대 분포(평균=1)의 95백분위(클수록 불균일) · 반응이 몰리는 면 — **부족한 운반자가 공급되는 쪽**으로 몰림 (σ_e<σ_ion이면 집전체쪽, σ_e≫σ_ion이면 분리막쪽) |


> **손실분담 자세히 — "전류 몫"과 왜 다른가 (풀어서)**
>
> ① 전류가 저항을 지나면 그 구간에서 전압이 떨어지고, 떨어진 만큼 에너지가 열로 바뀐다.
> 한 구간에서 나는 열 = (지나간 전류) × (그 구간에서 떨어진 전압) = I·ΔV = I²R.
>
> ② 우리 전극은 수백만 개 복셀 저항으로 된 회로다(위 Kirchhoff 블록).  솔버를 다 풀고 나면
> 복셀-면 하나하나에 대해 "전류가 얼마 지나갔고 전압이 얼마 떨어졌는지"를 알기 때문에,
> 복셀마다 열 I·ΔV를 계산할 수 있다.  이것을 재료별로 모아 합치고 전체로 나눈 %가
> 손실분담이다: "전극이 잃는 열의 90%는 VGCF 복셀 안에서, 10%는 SDCP 복셀 안에서 났다."
>
> ③ 이 숫자의 의미: **그 재료가 전극 전체 저항에서 차지하는 비중**이다.  전자가 집전체에서
> 분리막까지 가는 동안 겪는 "힘듦"의 90%가 VGCF 구간(섬유 내부 + 섬유끼리 건너는 목)에
> 있다는 뜻 — 그래서 병목 탐지기이자, 실제 충·방전 때 열이 나는 위치의 지도다.
>
> ④ **"전류를 얼마나 나르나"와 왜 다른가 — 숫자 예시 하나면 끝난다.**  저항 두 개가 직렬로
> 있다고 하자: R₁ = 9Ω, R₂ = 1Ω.  직렬이므로 **같은 전류가 둘 다 100% 통과**한다.  그런데
> 열은 I²R이라 R₁에서 90%, R₂에서 10%가 난다.  두 저항의 "전류 나르는 몫"은 완전히
> 같은데(100%씩), 손실분담은 9:1로 갈린다 — 손실분담 = 전류 × 저항이지, 전류가 아니다.
>
> ⑤ SDCP에 적용하면: SDCP는 σ = 150 S/cm로 이 전극에서 가장 저항이 낮은 재료다(④의 R₂
> 역할).  전류가 SDCP 복셀을 아무리 많이 지나가도, 그 복셀의 저항이 작으니 전압이 거의 안
> 떨어지고 열도 거의 안 난다.  따라서 **손실분담 10%는 "전류의 10%가 SDCP를 지난다"는 말이
> 아니라, 실제 전류 통행량보다 한참 작게 잡힌 하한**이다.
>
> ⑥ 이게 §3-① 논증의 핵심 산수다: SDCP가 그냥 "저항 비중 10%짜리 새 길 하나"를 병렬로 더
> 깔았을 뿐이라면 전체 개선도 ~10% 스케일이어야 한다.  실측은 +45.4% — SDCP가 자기 몸으로
> 저항을 부담해서가 아니라, **VGCF망의 비싼 접합부들을 값싼 다리로 이어 다른 구간(VGCF)의
> 저항 구조 자체를 바꿔놓았기 때문**이다.  손실분담이 작으면서 σ 이득이 큰 조합 = 브리지의
> 지문.


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

## 3. 메커니즘 — 4축 논증 (작위성 방어의 골격)

**① 손실분담 산수 (병렬-기여 기각)**: SDCP의 전자 줄손실 몫은 10.0%인데 σ_e는 +45.4% —
전도도 이득이 추가 상의 수송 몫을 따라가는 병렬-도체 그림으로는 불가능.  직렬 병목 해소는
가능: 목 하나를 뚫으면 경로 전체 저항이 내려가고, 브리지 자신은 σ=150 S/cm 저저항이라
J²R-가중 손실분담에는 작게 잡힌다(손실분담은 브리지 역할을 구조적으로 과소표시).
★ 스윕 독립 확인(2026-07-15): σ_SDCP를 1500→150→50→15 S/cm로 낮추면 분담이
1.7→10.0→16.3→19.6%로 **역행 증가**하면서 σ_e는 3.227→1.990으로 SBE 수준까지 수렴
(+63.4→+0.8%) — 병렬 도체라면 분담이 σ와 함께 0으로 가야 한다.  브리지가 저항일수록 자기
몫의 손실을 더 먹는 것 = 직렬-병목 토폴로지의 시그니처가 스윕 방향으로도 확인된다 (§8).

**② 접점 기하·분산**: AM당 환산접점 +19.3%(433→517), 전도 클러스터 ×2.7(3,172→8,644) =
~13.7만 개 개별 분산 0.3 µm SDCP(Fig. S3).  공간 통계는 AM-배제 보정 후 완전 랜덤과 구별
불가(index of dispersion 1.13, 최근접거리 = 동밀도 포아송의 1.13×) — **균일-랜덤 배치는
"임의의 틈"에 입자가 앉을 확률을 최대화하는 기하**이고, 이 통계가 스캐폴드·조성이 다른
a7_p00(1.14/×1.16)에서 재현된다 = 파라미터가 아니라 형상(단독입자)의 귀결.

**③ 대안 배제 — "혹시 다른 이유로 오른 것 아니냐"는 용의자 4명을 하나씩 심문**:

"σ_e가 +45.4% 올랐다"는 관측에 대해 브리지 말고도 떠올릴 수 있는 설명이 4개 있다.  각각을
우리 데이터가 어떻게 기각하는지:

- **용의자 1 — "전극이 더 눌려서(치밀해져서) 좋아졌다"**: 그렇다면 두 전극의 구조가 달라야
  한다.  실제로는 두께가 72.48 µm로 완전히 같고 공극률도 7.87 vs 7.39%로 사실상 같다.
  구조가 그대로인데 치밀화가 원인일 수는 없다.  → 기각.
- **용의자 2 — "SBE는 전자 길이 끊겨 있다가 DBE에서 처음 이어졌다" (퍼콜레이션 개시)**:
  그렇다면 SBE 쪽에 고립된 AM이 있어야 한다.  실제로는 **둘 다 AM의 100%가 이미 집전체에
  연결**돼 있다.  "안 이어짐 → 이어짐"의 전환이 아니라, 둘 다 이어진 상태에서 **길의 품질**만
  달라진 것.  → 기각.
- **용의자 3 — "절연체(PTFE)를 절반 뺐으니 당연히 좋아졌다"**: PTFE는 전자와 이온을 **똑같이**
  막는 절연체다.  그러니 PTFE 제거가 주원인이라면 전자망과 이온망이 **비슷한 비율로** 좋아져야
  한다.  실제는 전자 +45.4% vs 이온 +5.6% — 이온은 거의 안 움직였다.  심지어 이온 쪽은
  SDCP가 이온 저항의 13.8%를 새로 부담하며 "도와주고 있는데도" +5.6%에 그친다.  즉 PTFE
  제거로 얻을 수 있는 몫은 기껏 몇 % 수준이고, 전자 +45%의 주범이 될 수 없다.  → 기각
  (부차 요인으로만 인정).
- **용의자 4 — "전도체를 1.4 vol% 더 넣었으니 그만큼 좋아졌다" (부피 효과)**: "잘 섞인 전도체
  알갱이를 부피만큼 넣으면 전도도가 얼마나 오르나"에는 교과서 공식이 있다(유효매질 이론,
  Maxwell-Garnett): 알갱이들이 서로 고립돼 있다면 이득의 상한 ≈ 3 × 부피분율 = 3 × 1.3% ≈
  **+4%**.  실측은 **+45.4% — 부피 산수의 11.6배**.  "얼마나 넣었나"로는 설명이 안 되고,
  "**어디에 앉았나**"만이 남는다.  → 기각.

**결정타 — 같은 입자, 두 개의 다른 답**: 동일한 SDCP 입자들(같은 위치, 같은 양)이 전자망에는
+45.4%를, 이온망에는 +5.6%를 줬다.  만약 효과가 "재료의 σ 입력값을 넣어서" 나오는 것이라면
두 네트워크 모두 자기 입력값에 비례해 좋아져야 한다.  같은 입자가 두 망에서 전혀 다른 효과를
낸다는 사실 자체가, 결과를 결정하는 것이 입력값이 아니라 **그 입자가 각 네트워크의 어느
자리에 앉았는가(토폴로지)**라는 증명이다 — 전자망에서는 병목(접합부) 자리에 앉았고, 이온망
에서는 SE가 이미 연속상이라 앉을 병목 자체가 드물었던 것.

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

- **σ_SDCP(e) 의존성 — 스윕 실행 완료 (2026-07-15, V100 재압밀 침대 = 원장 침대 byte-재현:
  porosity 7.386/두께 72.484/점수 67,901,280 동일, σ_e 2.874 = 원장 2.871 +0.1% CG 잔차)**:
  σ_SDCP {15 / 50 / 150 / 1500 S/cm} → σ_e {1.990 / 2.485 / 2.874 / 3.227 S/cm} = SBE(1.975)
  대비 **{+0.8 / +25.8 / +45.5 / +63.4%}**, SDCP 손실분담 {19.6 / 16.3 / 10.0 / 1.7%}.
  ⇒ **전자 이득의 크기는 σ_SDCP에 강하게 의존 — "weakly dependent" 주장 기각** (§F1 정직 기록).
  단: (i) 가장 비관적인 15 S/cm에서도 **손해 없음**(SBE와 동급, +0.8%); (ii) 분담이 σ_SDCP↓에서
  10→20%로 **역행 증가** = 직렬-병목(브리지) 시그니처의 독립 확인(§3-①; 병렬이면 분담↓); (iii)
  이온 +5.6% · 반응면 +18% · R_geom −32% · 접점/클러스터/분산 축은 σ_SDCP(e)와 무관 — 불변;
  (iv) 1500 점 = 천장 해석: 분담 1.7% ≈ 무손실 브리지 → **σ_e 기하 천장 ≥ 3.23 S/cm(+63%)**
  = 브리지 "배치"의 기하 가치이고, σ_SDCP는 그 실현률을 정한다(150에서 천장의 ~70% 실현,
  천장≈3.23 근사) — 곡선은 15–150 급상승 → 150–1500 감속의 전형적 포화형.
  성립-조건 정정: 브리지 이득의 크기는 "틈보다 잘 통하느냐"(15도 충족)가 아니라 **VGCF 우회로
  대비 경쟁력**이 결정 — 15 S/cm는 우회로와 동급이 되는 지점.  **랩 펠릿/필름 σ_SDCP 측정이
  전자 헤드라인의 크기를 직접 결정** → 논문은 단일 +45.4%가 아니라 σ_e(σ_SDCP) 3점 곡선
  (+최악에서도 무손해)으로 제시 권고.
- **σ-공동스케일 = 비례 근사★** — 캡션 명시 + SI 자기-정규화판.  glow = 렌더 장치(물리 아님).
- **기계 축은 범위 밖**: PTFE 반감의 접착 비용(binder_cap 0.645 "under")은 SDCP 계면-앵커링
  (E_bind 재계산 대기)이 담당하는 별도 주장.
- **i/ī p95 2.32→2.48**: "SDCP가 반응 불균일을 낮춘다"는 지지되지 않음 — 균일도 개선 주장 금지.
- 실험 앵커 훅: 대칭셀 SBE/DBE σ 비율(배영진 "얼추 비슷" — 수치 확보 시 §2에 추가),
  3.18mAh 실측 전극 두께(≈72.5µm 검증 → porosity 논란 종결).
- 조성 환산 규약: 카드 wt% = 최종 전극 전체 기준; 70:27:3:1(합101) ↔ 2.97/0.99,
  70:27:3:0.5:0.5 ↔ 2.97/0.495/0.495 (실현 조성 70.37/25.67 wt% 확인).
