<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목.
     깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md. 이 논문은 *물리 모델*이 아니라 *방법 TOOL* 이므로
     §7/§A/§B/§C 를 "경쟁자 아님 / 교차검증 도구" 프레임으로 재배치. -->
# TauFactor — voxel 미세구조에서 정상상태 확산(Laplace)을 풀어 tortuosity FACTOR τ 를 직접 계산하는 오픈소스 MATLAB 툴 — Cooper (SoftwareX 2016)

> slug `taufactor_tortuosity_factor_tomography_tool` · DOI `10.1016/j.softx.2016.09.002` · type `tool (voxel Laplace-solve, post-processing)` · PDF `Cooper_2016_SoftwareX_TauFactor_TortuosityFromTomography.pdf` · digested `2026-06-26` · status ✅
>
> ★ Paper #46 — **TOOL, not a physics competitor.** 분할된(segmented) voxel/단층촬영(tomography) 미세구조 위에서 **정상상태 확산방정식 ∇²C=0 을 직접 풀어** tortuosity **factor τ** (+ 부피분율 ε · 표면적 SA · triple-phase-boundary 밀도 TPB)를 산출하는 배터리/연료전지 미세구조 분석의 **사실상 표준 외부 툴**. ★ **핵심 매핑**: TauFactor 의 τ 정의 `D_eff = D·ε/τ` 는 **수학적으로 우리 τ_Laplace 와 같은 form** (= Minnmann 2021 JES Eq 4 = Bielefeld 2020 flux-PDE) 이지만, **연속체 voxel 상에서 풀므로 점접촉(SE-SE) Holm 구속저항이 없다** → 따라서 그것은 우리 **τ_Laplace,bulk** (기하/상한 tortuosity) 에 대응하며, 우리 **τ_Laplace,eff** (Holm constriction 포함) 에는 대응하지 **않는다**. 우리 τ_Laplace,bulk 의 **frame[4] 외부 교차검증 표준툴**이자, Huang2025 LBM-ETC 의 가벼운 voxel-transport cross-check 후보.

---

## 1. 한 줄 요약
TauFactor 는 단층촬영으로 얻어 **분할된 voxel 3D(또는 2D) 미세구조**를 입력받아, 전도상(conductive phase) 안에서 **정상상태 확산(라플라스) ∇²C=0 을 over-relaxed Jacobi 반복법으로 풀고**, 풀린 정상상태 flux 를 같은 크기·확산도·전위차의 *완전 치밀* 대조체적 flux 와 비교하여 **tortuosity factor τ ≡ ε·D/D_eff (Eq 1)** 를 산출하는 오픈소스 MATLAB GUI 툴이다. τ 외에 **부피분율 ε · 표면적 SA · TPB 밀도** 를 함께 주고, **representative volume analysis(RVA)** 로 RVE 충분성을 점검한다. **>10⁸ voxel 데이터셋을 단일 코어에서 수 시간** (10⁶ voxel <30 s) 에 처리 — 핵심 메시지는 "Bruggeman 같은 *상관식*에 의존하지 말고 미세구조에서 τ 를 **직접** 계산하라, 그리고 그 계산을 **일관되게**(remesh/resample 없이 voxel 을 직접 mesh 로) 하라". = 우리가 `voxel_conductivity.py` 로 이미 푸는 **τ_Laplace,bulk** 와 *같은 종류의 계산*을 하는 검증된 표준 외부 툴.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| **S.J. Cooper**(교신, Imperial College London), A. Bertei(ICL), P.R. Shearing(UCL), J.A. Kilner(ICL), N.P. Brandon(ICL) | **SoftwareX 5 (2016) 203–210** | **10.1016/j.softx.2016.09.002** | **소재-무관(material-agnostic) 툴**. 예시 = SOFC LSCF cathode (산화물). 우리 LPSCl/NCM 아님 — 어떤 분할 voxel 미세구조든 입력 가능. | **소프트웨어 publication / 방법 TOOL** (MATLAB app). 실험 아님·물리모델 아님. |

- 접수 2016-07-05, 개정 2016-09-15, 게재 2016-09-19. **CC BY 오픈액세스**.
- **코드/소프트웨어 버전 v1.10**, **FreeBSD 라이선스**, git 버전관리. 저장소 `github.com/ElsevierSoftwareX/SOFTX-D-16-00054`, 실행파일 `sourceforge.net/projects/taufactor`. **MATLAB 2015+ + Image Processing Toolbox** 필요. 지원 `sjc08@ic.ac.uk`.
- 지원: EPSRC Supergen Fuel Cells (EP/J016454/1, EP/M014045/1), Horizon 2020 Marie Skłodowska-Curie (654915). ⚠ 본 digest 는 **2016 SoftwareX 원논문(v1.10)** 기준 — 이후 Python 재구현 `TauFactor 2`(GPU, Cooper 그룹, 2023 JOSS)가 별도 존재하나 본 PDF 와 무관(필요 시 별도 digest).
- ★ **소재-무관 TOOL** 이므로 "소재 절대값 전이 금지" 같은 경고는 *입력 데이터*에 달리지 *툴 자체*엔 안 달림 — 즉 우리 LPSCl voxel 을 넣으면 *우리 소재의* τ 가 나온다(소재 swap 자동). 이것이 물리-모델 논문(halide·oxide)과의 결정적 차이.

## 3. 핵심 물성·수치 (이 논문이 주는 것 = 방법·성능·정의)
> ⚠ 이 논문은 *소재 물성 앵커*(porosity@P / σ / E_SE) 를 **주지 않는다** — 방법 TOOL 이므로. 주는 수치 = ① τ 정의식, ② 솔버 성능, ③ 예시 미세구조의 산출값, ④ voxel SA/TPB 추정 오차 한계.

| 물성/수치 | 값 | 조건 | stated/derived | 비고 |
|---|---|---|---|---|
| **τ 정의 (Eq 1)** | **D_eff = D·ε/τ → τ = ε·D/D_eff** | 일반 (전류·열·물질 호환) | stated 핵심식 | τ=1 ⇔ 경로 직선(prismatic); **항상 τ≥1**(τ<1 이면 기하가 flow 를 *증폭* = 비물리) |
| 지배 PDE (sys 4) | **∇²C=0** in Ω; C=0 top; **∇C·n=0** on interface; C=1 bottom | 2-Dirichlet + reflective 계면 | stated | = 우리 voxel Laplace BC 와 동일 골격 |
| **솔버 성능** | 10⁶ voxel **<30 s**, 단일 i7 코어, ~**100 MB RAM** | iterative OR (over-relaxation) | stated | cf. 직접 행렬역(Rhazaoui) 동일 10⁶ voxel = **>2 h** (Xeon 8-core, 24 GB) → ★ **>240× 가속** |
| 반복수 절감 | **~3 orders of magnitude(약 1000×) 적은 반복** | OR vs Jacobi | stated | + checkerboard 벡터화로 추가 **≥4× 가속** |
| 처리 가능 크기 | **>10⁸ voxel** 단일 코어 수 시간 | 현대 tomography 규모 | stated/결론 | "고성능 컴퓨팅 불필요" 가 셀링포인트 |
| **예시 τ** (ThreePhase.tif, Fig 6 좌) | **τ = 2.26** (White 상, φ=37.5 %) | 90×100×80 voxel, **이방성 35×35×32.2 nm**, Dir 1 | stated 리포트 | percolation 99.8 %; 340 반복; 11 s |
| 예시 vol-frac (Fig 6 우) | Black 0.353 / Green 0.272 / White 0.375 | RVA 리포트 | stated | + SA Black 4.74·Green 5.19·White 7.65 µm⁻¹; TPB **30.2 µm⁻²** |
| **SA 과대추정** (Fig 7, "perfect tomography") | 단일구=단일voxel → SA **×~2**; 다voxel 구 → 최소 **×1.5**; sub-voxel 복잡구조 → *임의로 큰 과소* | voxel 면/모서리 직접사용(no Marching Cubes) | stated 경고 | ★ voxel SA/TPB 는 *근사*, 보정은 사용자 판단 |
| 이방성 보정 (Eq 8) | φ₁ = ½·(l₁l₂/l₃+l₃l₁/l₂+l₂l₃/l₁)⁻¹·(l₂l₃/l₁) | 비정육면체 voxel | stated | τ 는 dimensionless 라 *절대* voxel 크기는 무관, **이방성만** 보정 필요 |
| 검증 (Fig 8) | TauFactor τ = **Avizo XLab 와 일치** (8-method 비교) | LSCF SOFC cathode [22] | stated | 둘 다 *voxel 직접* 솔버라 일치(당연); 다른 method(거리맵·평균경로 등)는 크게 분산 |
| σ_ionic / σ_e / coverage / Z / E_SE / Heckel | **n/a** | — | n/a | **방법 TOOL** — 어떤 소재 물성도 자체 산출 안 함 (입력 voxel 의 τ·ε·SA·TPB 만) |

→ **이 논문이 주는 것** = ① τ 의 *조작적 정의*(우리와 동일 form), ② 그 τ 를 *voxel 직접·일관되게·빠르게* 푸는 검증된 솔버, ③ voxel-SA/TPB 의 정량 오차 한계.
→ **안 주는 것** = 우리 핵심 절대 앵커(porosity@P, σ_ion/e/thermal, coverage, Z, E_SE, Heckel) — 그건 *입력 미세구조*가 정하고 우리 솔버가 푼다. TauFactor 는 그 위에 *τ 한 숫자*(+ε·SA·TPB)만 얹는다.

## 4. 방법 — TauFactor 가 τ 를 어떻게 푸는가 ★
### (A) 입력 — 분할(segmented) voxel 미세구조
- **입력**: 단일 `*.tif` 스택(3D 또는 2D), 상(phase)이 이미 **분할**되어 있어야 함(최대 3상: black/white/green = 1/2/3, pore 포함). 8-bit integer array 로 변환. 다중 `*.tif` 선택 = **batch**(케이스별 순차 처리, 결과는 MATLAB workspace 의 분리 struct). **GUI 없이 스크립트에서 함수 직접 호출 가능**(매뉴얼에 입력변수 형식).
- **tomography 출처**: XCT(X-ray CT) 또는 FIB-SEM. grey-scale → **segmentation**(점증적으로 ML 기반) → 이진/3상 voxel.
- ★ **핵심 설계철학**: **voxel 을 직접 mesh 요소로 사용** — remesh/resample/surface-mesh **안 함**. 이유(저자 명시): meshing 은 효율은 좋으나 **smoothing·기하왜곡** 을 유발하고, 저자들의 이전 연구[22]가 "*명목상 동일한* 방법들 사이에 유의한 불일치"를 발견 → 그 비일관성을 없애려고 voxel-직접 채택. ⇒ **재현성/일관성**이 TauFactor 의 존재 이유.

### (B) 솔버 — 정상상태 Laplace 확산 ∇²C=0
- **물리 셋업** (sys 4, Eq 2–3):
  - 다공막 Ω 안에서 **∇²C=0** (정상상태, source 없음).
  - **상단(Top) C=0**, **하단(Bottom) C=1** = 2개 평행면에 **Dirichlet** 고정.
  - **계면(Interface, 비전도상 경계) ∇C·n=0** = **reflective(no-flux)** = 비전도상으로는 확산 안 감.
  - τ 추출: 다공 flux F_p = −A·D·(ε/τ)·ΔC/L (Eq 2) 를 *완전 치밀* 대조 flux F_cv = −A·D·ΔC/L (Eq 3) 로 나눠 → Eq 1 회복.
- **이산화**: sys 4 를 cuboid voxel 격자에 remap → 각 voxel 의 농도 = **face-adjacent 이웃 전도 voxel 농도의 평균**(정육면체일 때). = 유한차분(FD) ≡ 면별 flux 질량보존. **6-이웃(north/south/east/west/up/down) 만**(대각선 무시).
- **경계 강제 = ghost-node 기법** (Fig 2, Eq 5–7): 경계 voxel 의 이웃수를 +1, 외부 인가농도를 ×2 → ghost-node ŷ 가 최종식에서 사라지면서 Dirichlet 면 농도를 정확히 강제. (Eq 7: e = (d+f+2·C_max)/4.)
- **반복법 = Over-Relaxation(OR)** : 직접 행렬역(비전도 노드 제외) *가능* 하나, 대신 **OR 반복**(Jacobi + 선형 외삽) 채택 → 반복수 ~1000× 절감, 메모리 거의 안 늘음. **checkerboard(RED/GREEN) 벡터화**로 한 반복 계산량 절반(MATLAB 벡터화 효율). 두 최적화 합쳐 **≥4× 추가 가속**.
- **이방성 보정** (Eq 8–10): voxel 이 비정육면체(l₁≠l₂≠l₃)면 방향별 가중 φ₁ 을 계산, 이웃맵 B_ani(Eq 9)·Jacobi 갱신(Eq 10)에 반영. ★ τ 는 dimensionless → **절대 voxel 크기는 무관**, **이방성만** 영향.
- **수렴** : 일괄(batch) 반복마다 **top·base 양면에서 τ 를 따로 계산**, 그 두 값의 *변화율 + 절대값 비교* 라는 **hybrid 기준**으로 수렴 판정(느린 수렴 + 대칭계 둘 다 대응).
- ★ **통계적 연속체도 OK**: 단일 확산입자에도 지배식 성립(random-walker 유도) → 물리적 연속체뿐 아니라 통계적 연속체로 해석 가능.

### (C) 산출(outputs) — τ 뿐 아니라 ε·SA·TPB·percolation·flux map
- **tortuosity factor τ** : 상별·방향별(Dir 1/2/3 = X/Y/Z). **percolation 안 되면(전도방향 미연결) 측정 불가**.
- **부피분율 ε** + 방향별 ε 변화 그래프.
- **표면적 SA** (µm⁻¹) : cuboid voxel **면(face)** 직접 사용(Marching Cubes 같은 smoothing **안 함**). 두 voxel 이 다른 상이면 면=interface. ★ 과대추정 경고(Fig 7).
- **TPB 밀도** (µm⁻²) : cuboid **모서리(edge)** 중 4-접촉 voxel 이 3종 다른 상이면 TPB. (외곽 면/모서리는 다음 layer 정보 없어 라벨 불가 → 첫 layer 제외·외곽은 0.5 가중으로 선형 scaling 보존.)
- **percolation fraction** : 전도방향 연결분율.
- **flux map** : 정상상태 농도장에서 voxel별 총 flux(+through-plane/in-plane 분리) → 정규화 `*.tif` 스택 export. ★ **bottleneck 시각화**(Fig 1 빨강 = 고-flux; 전류면 국소 열화/과열 진단 활용).
- **RVA(representative volume analysis)** : 4종(Fig 5; cuboid 등방 / L=const / A=const / base-from-bottom). ~5 % 증분으로 부피 키우며 metric 안정성 plot → RVE 충분성 점검(Tortuosity 10 step / Metrics 20 step).

### (D) "입자 처리"(이 논문엔 입자가 없음 — voxel 직접)
- ★ TauFactor 는 **입자(particle)를 모르는** 툴이다. 입력은 *이미 분할된 voxel 라벨장* 일 뿐 — 구/형상/소성/접촉법칙 개념 자체가 없음. 따라서 "rigid vs CONTACT-소성 vs SHAPE-소성" 축은 **TauFactor 에 부적용** — 그 정보는 *입력 미세구조를 만든 단계*(우리 경우 DEM+MPM)가 이미 결정해서 voxel 에 구워넣음. ⇒ TauFactor 는 *우리 DEM/MPM 의 하류(downstream) 후처리 솔버* 위치(우리 dump→voxel→τ).
- ⚠ 따라서 **TauFactor 의 τ 가 점접촉 constriction 을 담는가?** = **입력 voxel 해상도와 BC 가 결정**. voxel 이 점접촉을 sub-voxel 로 뭉개면(우리 SE 0.5 µm @ 1 µm grid 처럼) **그 구속이 사라진다** → 그래서 TauFactor τ ≈ **bulk/기하 tortuosity(상한)**, 우리 Holm 망 constriction 을 *대체 못 함*(§A 참조).

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1 | **워크플로** (좌→우): noisy grey tomography → segmented 2-phase → TauFactor 확산 시뮬(고-flux 빨강) | = 우리 DEM dump→voxel→τ 파이프라인의 하류 절반. flux map = bottleneck 가시화 |
| 2 | **ghost-node 2D 예시** + 각 voxel 총 scalar flow | Dirichlet 면 강제법(이웃수+1·인가농도×2). node f 는 flow↑, node c 는 무영향(막다른 가지) |
| 3 | **checkerboard 벡터화** 모식(3D→RED/GREEN 벡터) | OR+checkerboard = ≥4× 가속 구현 |
| 4 | **GUI 창** 3종(빈 화면 / 2D 2상 로드 / 3D 3상 로드); 상 라벨(black/white/green)·방향(1/2/3)·voxel 크기·RAM/시간 | 입력·옵션 UI; **voxel 크기 30.1×30.1×27.4 nm 이방성** 입력칸 |
| 5 | **RVA 3종** 모식(cuboid / L=const / A=const) | RVE 충분성 점검(우리 RVE box ≥7.5× 최대입자 와 같은 목적) |
| 6 | **리포트** 2종: (좌) τ 계산 리포트(농도장·초기·정상상태·flux + τ-vs-반복 곡선 + **τ=2.26**); (우) RVA metric 리포트(ε·SA·TPB) | ★ 산출 전체 스냅샷. τ 수렴거동·flux 분포·vol-frac 변화 한 장 |
| 7 | **voxel SA/TPB 오차** 3 시나리오("perfect tomography"): 1구=1voxel(SA ×2) / 다voxel 구(×1.5 최소) / sub-voxel 복잡(임의 과소) | ★ voxel SA/TPB 는 *근사* — 우리 coverage/면적 metric 도 voxel 화 시 같은 주의 |
| 8 | **8-method τ 비교**(LSCF cathode): TauFactor·Star-CCM+·**Avizo XLab**·Finite Volume·Random Walk·Mean Path·Pore Centroid·**Bruggeman** vs ε | ★ **TauFactor = Avizo XLab 일치**(둘 다 voxel 직접); 다른 method 는 크게 분산 → "method 마다 τ 다르다"는 *우리 τ_Dijkstra≠τ_Laplace,bulk≠τ_Laplace,eff* 분리의 외부 근거 |

## 6. Post-processing ★ (이 논문 *자체*가 post-processing 툴)
- **무엇**:
  - **tortuosity factor τ** = 정상상태 Laplace flux ÷ 치밀 대조 flux (Eq 1), 상별·방향별. **percolation 안 되면 측정 불가**.
  - **부피분율 ε** = voxel count. **표면적 SA**(µm⁻¹) = voxel face. **TPB 밀도**(µm⁻²) = voxel edge(3상 접촉).
  - **percolation fraction** = 전도방향 연결분율.
  - **flux map**(through/in-plane 분리, `*.tif` export) = bottleneck/열화 진단.
  - **RVA** = 4종 RVE 충분성 plot.
- **수치화·일관성 핵심**: voxel **직접** 솔버 → remesh/resample 의 자의성 제거 = "studies 간 비교가능성↑"가 **expected impact**(§3.2). 기존 method 들이 ① 고가 독점 SW 또는 ② black-box(상업적/학술적 비공개)라 비교불가 → **오픈소스 FreeBSD** 로 그 장벽 해소.
- **상관식(Bruggeman) 비판**: 저자 입장 = Bruggeman τ=ε^(−α) 같은 *상관식* 은 등방·단순기하 가정이라 복잡망에 부정확(Tjaden et al. 리뷰 인용) → **3D 이미지가 있으면 직접 계산하라**. ★ = 우리 σ_thermal "Bruggeman EMT R²<0 실패" + Bielefeld2020 "Bruggeman 4× 과소" 와 **같은 메시지**.

---

## 7. 우리 DEM+MPM 대비 (한눈에) → `our_dem_baseline.md`
> ⚠ TauFactor 는 *물리 모델 경쟁자*가 아니라 *τ 계산 TOOL* 이다. 따라서 비교는 "누가 SOTA"가 아니라 **"우리 어느 τ 출력에 대응하는가 + 우리가 그것을 넘어 무엇을 더 푸는가"**.

| 항목 | TauFactor | 우리 | 관계 |
|---|---|---|---|
| **무엇** | voxel 미세구조 → τ·ε·SA·TPB **계산 TOOL** | DEM(접촉망 σ 삼중항·percolation·coverage·fracture) + MPM(소성 morphology) **물리 엔진** | TOOL vs ENGINE — **하류 후처리**로 보완 관계 |
| **τ 솔버** | voxel **연속체** Laplace ∇²C=0 (OR-Jacobi), reflective 계면 | `voxel_conductivity.py` Laplace(연속체) **+** `network_conductivity.py` Holm 접촉망 | ★ 우리 voxel Laplace = TauFactor 와 **같은 종류** → **τ_Laplace,bulk 1:1 교차검증 대상** |
| **τ 종류** ★ | **점접촉 constriction 없는 기하/상한 τ** (= bulk) | **τ_Laplace,bulk**(constriction 無) + **τ_Laplace,eff**(Holm constriction 有) + **τ_Dijkstra**(geodesic 최단경로) | ★ TauFactor ↔ **우리 τ_Laplace,bulk** (≈Bielefeld2020 flux-PDE 상한). **τ_Laplace,eff·τ_Dijkstra 엔 대응 안 함** |
| **constriction** | **없음**(voxel 연속상; sub-voxel 점접촉 소실) | Holm 1/(2σ·r_c) + Stage-E 소성 접촉면적(Tabor+volume) | ★ **우리가 *더하는* 핵심** — TauFactor 가 비운 칸(Bielefeld2019 "future work: Greenwood" 자리) |
| **소재** | **소재-무관**(입력 voxel 의 τ) | LPSCl/NCM811 (우리 소재) | ★ 우리 voxel 넣으면 *우리 소재* τ → 절대전이 문제 자체가 없음 |
| **출력 채널** | τ·ε·SA·TPB (transport descriptor) | σ_ionic(LOOCV 0.975)·σ_e(0.953)·**σ_thermal**(0.90) 삼중항 + Z·coverage·force-chain·fracture | TauFactor 는 *τ 한 descriptor*; 우리는 *τ 를 입력으로 쓰는 σ 예측까지* |
| **공간장** | flux map(voxel별 flux) = bottleneck | MPM 응력·소성변형 공간장 / DEM lumped(공간 T장 無) | TauFactor flux map = *우리가 부분적으로 못 보던* 공간 flux bottleneck(Huang LBM 과 같은 역할) |
| **속도** | 10⁶ voxel <30 s, >10⁸ voxel 수 시간(단일코어) | σ 스케일링 폼 = 즉시 예측 / 망솔버 = 케이스당 solve | 둘 다 빠름; TauFactor 는 *검증용 1샷* |
| **성숙도** | 표준 툴·검증(Avizo 일치)·RVA·오픈소스 | 자체 파이프라인 | ★ **TauFactor = 우리 τ_Laplace,bulk 의 *표준-툴 도장*(frame[4])** |

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① ★ **우리 τ_Laplace,bulk 의 *표준 외부 툴* 교차검증 (frame[4]).** 우리 `voxel_conductivity.py` 의 Laplace-τ 는 *자체 구현* — TauFactor 는 *같은 계산의 검증된 표준 솔버*다. 우리 DEM dump 를 voxel 화 → TauFactor 에 넣어 τ 산출 → 우리 τ_Laplace,bulk 와 비교. 일치 → 우리 voxel-τ 구현 신뢰 보강(Avizo 가 TauFactor 를 검증했듯). **단 우리 τ_Laplace,eff·σ_ionic(constriction 포함)은 그 위에 *추가*되는 것** — TauFactor 가 그걸 검증하는 게 아니라 *bulk 하한(상한 τ)* 을 못박아 주는 것.
- ② ★ **Huang2025 LBM-ETC cross-check 의 가벼운 대안.** Huang2025 digest 에서 "우리 DEM dump 를 voxel 화 → LBM(또는 *더 가볍게 TauFactor τ만*)으로 ETC 독립 산출 → frame[4] 교차검증" 을 flag 했었다(§적용가능성-A). **TauFactor 가 바로 그 "더 가볍게 τ만" 경로** — full LBM(6×10⁵ iter) 없이 τ 만 빠르게 뽑아 우리 σ_thermal·κ 의 tortuosity 입력을 표준툴로 검증. (실제로 Huang2025 자신이 tortuosity 를 **TauFactor 로** 산출했다 → 우리도 같은 툴 쓰면 *Huang 과 같은 척도*로 직접 비교 가능.)
- ③ ★ **우리 `voxel_conductivity.py` 의 표준-툴 검증.** 우리 voxel 솔버(σ·τ)를 TauFactor 대비 *벤치마크* → "우리 voxel-Laplace 가 표준 TauFactor 와 일치(Avizo-급)" 라는 1-line 검증 문장 확보. ★ 단 voxel SA/TPB 는 *근사*(Fig 7: ×1.5–2 과대) → 우리 coverage/면적을 voxel 로 뽑을 땐 **TauFactor 의 same 한계**(Marching-Cubes 미적용) 가 적용됨을 인지(우리 coverage 는 *기하 KDTree*·Stage-E 라 더 정밀 — §B-D).
- ④ **RVA = 우리 RVE 충분성 점검의 표준화.** 우리 "RVE box ≥7.5× 최대입자" 는 *경험칙* — TauFactor RVA(metric-vs-volume plot)는 그걸 *정량 그래프*로 만든다. 우리 voxel 미세구조에 RVA 돌려 RVE 충분성을 *수치*로 보고(논문-grade rigor).
- ⑤ **method-다양성 경고의 외부 근거(Fig 8).** TauFactor 가 보인 "method 8종 τ 가 크게 분산, voxel-직접만 서로 일치" = 우리 **τ_Dijkstra(geodesic) ≠ τ_Laplace,bulk ≠ τ_Laplace,eff** 가 *다른 양*임을 못박는 외부 근거. 인용 시 "τ 는 정의·솔버 의존 — 같은 미세구조도 method 마다 다르다(Cooper 2016 Fig 8)" 로 우리 3종 τ 분리를 정당화.

## 9. 인용 가능 문장 (deck/paper용)
- "Tortuosity factors were cross-checked against TauFactor (Cooper et al., SoftwareX 2016), the standard open-source tool that solves steady-state diffusion (∇²C=0, τ = ε·D/D_eff) directly on the segmented voxel grid; because TauFactor treats the conductive phase as a continuum and carries no point-contact constriction, its τ corresponds to our *bulk* (geometric) Laplace tortuosity τ_Laplace,bulk — the upper-bound on which our Holm/Kirchhoff contact-network solver then imposes the SE–SE constriction to obtain the effective τ_Laplace,eff and σ_ionic."
- "TauFactor's own benchmark (its Fig 8) shows that nominally identical tortuosity definitions diverge widely across methods and only voxel-direct solvers (TauFactor ≡ Avizo XLab) agree — an external justification for our explicit separation of geodesic (τ_Dijkstra), bulk-Laplace (τ_Laplace,bulk) and constriction-resolved (τ_Laplace,eff) tortuosities."
- "Following the same TauFactor-based tortuosity workflow used by Huang et al. (2025) on an oxide DEM+LBM composite, we feed our LIGGGHTS-derived voxel microstructures to TauFactor as a lightweight (τ-only) cross-check of the thermal/ionic tortuosity entering our σ_thermal and σ_ionic forms, without the full Lattice-Boltzmann re-solve."

## 10. 주의/한계 (over-claim 방지)
- ⚠ **방법 TOOL — 물리 앵커 없음.** porosity@P / σ / E_SE / coverage / Z / Heckel 어느 것도 자체 산출 안 함. 그 숫자는 *입력 미세구조*가 정함. TauFactor 는 그 위에 *τ·ε·SA·TPB* 만 얹음.
- ⚠ ★ **constriction 없음 = τ_Laplace,bulk(상한)만.** voxel 연속상에서 풀어 **점접촉(SE-SE) Holm 구속저항이 없다**. 우리 τ_Laplace,eff·σ_ionic(constriction 포함)을 **대체 못 함** — 오히려 그 *상한 하한값*을 줄 뿐. "TauFactor τ = 우리 σ_ionic-급 τ" 라 말하면 **틀림**.
- ⚠ **voxel SA/TPB 는 근사**(Fig 7): 1구=1voxel → SA ×~2, 다voxel 구 → 최소 ×1.5 과대, sub-voxel 복잡구조 → 임의로 큰 과소. Marching-Cubes 등 smoothing **안 함**(의도적 — 일관성 우선). 우리 coverage/면적 metric 을 voxel 로 뽑을 땐 같은 한계 적용 → 우리 *기하 KDTree·Stage-E* coverage 가 그 점에선 더 정밀.
- ⚠ **τ 는 voxel 해상도에 민감**(sub-voxel feature 소실 = constriction 소실). 우리 SE 0.5 µm 를 거친 grid(예 1 µm)로 voxel 화하면 SE-SE 목(throat)이 뭉개져 τ 가 *낮게(bulk 쪽으로)* 나옴 — 우리 mpm3d/voxel 파이프라인의 sub-cell SE under-resolution 주의와 같은 함정.
- ⚠ **percolation 안 되면 τ 측정 불가**(전도방향 미연결 = "inf"). 우리 dead-SE/dead-AM·degenerate-network 케이스와 같은 한계.
- ⚠ **예시 = SOFC LSCF cathode(산화물)** — 우리 LPSCl/NCM 아님. 단 *소재-무관 툴*이라 우리 voxel 넣으면 우리 소재 τ 가 나옴(절대전이 문제 없음 — 입력만 바꾸면 됨).
- ⚠ **버전 = 2016 SoftwareX v1.10**. 이후 `TauFactor 2`(Python/GPU, 2023 JOSS)는 별도 — 본 digest 는 원논문 범위.

---

## ★ 우리 DEM+MPM 대비 (comparison vs ours)

> 핵심 질문: TauFactor 의 **voxel-Laplace τ-factor** 는 우리 **세 가지 τ 출력**(τ_Dijkstra geodesic / τ_Laplace,bulk / τ_Laplace,eff) 중 *어느 것* 에 대응하는가? 그리고 그 대응이 *왜* bulk 이지 eff 가 아닌가?

### (1) 정의는 같다 — τ = ε·D/D_eff 는 우리 τ_Laplace 와 *수학적으로 동일한 form*
- TauFactor 정의(Eq 1): **D_eff = D·ε/τ ⟹ τ = ε·D/D_eff**. 확산도 D 를 전도도 σ 로, 농도 C 를 전위 φ 로 바꾸면 **정확히** 우리 τ_Laplace 정의 = Minnmann 2021 JES Eq 4 = **τ² = (σ_eff/σ_0)⁻¹·φ = σ_0·φ/σ_eff** 와 같은 form 이다.
  - ⚠ **τ vs τ² 표기 주의**: 다른 문헌(Minnmann)이 "tortuosity *factor* τ²" 라 부르는 양을 TauFactor 는 그냥 "tortuosity factor τ" 라 부른다 — 둘은 *같은 양*(= ε·D/D_eff = σ_0·φ/σ_eff). 즉 **TauFactor 의 τ ≡ Minnmann 의 τ²(=4.3) ≡ 우리 τ_Laplace²**. (Minnmann 의 선형 τ_ion=2.07 = √(이 값).) 인용 시 "TauFactor τ-factor (= τ²-정의, σ_0·φ/σ_eff)" 로 병기 — 우리 코드의 τ_Laplace 가 *제곱 전/후* 어느 쪽을 저장하는지와 일관되게 맞출 것.
- 솔버도 같은 종류: TauFactor = voxel Laplace ∇²C=0 (OR-Jacobi, reflective 계면) = **우리 `voxel_conductivity.py` 의 voxel-Laplace 와 같은 골격**. ⇒ **계산 자체가 1:1 교차검증 대상**.

### (2) 그러나 *어떤* τ 인가 — TauFactor = **τ_Laplace,bulk**(constriction 無), **τ_Laplace,eff 아님** ★
이게 이 digest 의 핵심 매핑이다.

| 우리 τ 출력 | 무엇 | TauFactor 대응? |
|---|---|---|
| **τ_Dijkstra** (geodesic 최단경로) | 순수 *경로길이* 우회도(l/l₀, Eq 3 류) | ❌ **대응 안 함** — TauFactor 는 경로길이 proxy 가 아니라 *확산 PDE* 를 푼다(저자가 Epstein[14] 인용해 "경로길이 ≠ tortuosity factor in complex networks" 라고 *명시 비판*) |
| **τ_Laplace,bulk** (Laplace, **constriction 無**) | voxel 연속상 확산 우회도 = *기하/상한* tortuosity | ✅ ★ **정확히 이것** (≈ Bielefeld2020 EJ-HEAT flux-PDE 상한) |
| **τ_Laplace,eff** (Laplace **+ Holm constriction**) | 점접촉 SE-SE 구속까지 포함한 *유효* tortuosity | ❌ **대응 안 함** — TauFactor 는 voxel 연속상이라 점접촉 constriction 이 *애초에 없다* |

- **왜 bulk 이고 eff 가 아닌가** = TauFactor 는 전도상을 **연속 매질(voxel 덩어리)** 로 다루고 계면을 reflective(∇C·n=0)로 처리 → 그 안에서 확산은 *기하 pore-throat* 의 좁아짐만 본다. 우리 DEM 의 **SE-SE 점접촉 수렴저항(Holm 1/(2σr_c))** — 두 구가 *작은 원판*으로만 닿아 그 목에서 전류가 쥐어짜이는 물리 — 는 voxel 연속상에 **존재하지 않는다**(접촉면이 voxel 로 메워져 연속 단면이 됨). ⇒ TauFactor τ 는 우리 *bulk* 솔버처럼 **constriction 을 누락한 상한 τ**.
- ★ **= Bielefeld 2020 flux-PDE 와 정확히 같은 위치**: 우리 comparison_vs_ours.md 가 Bielefeld2020 을 "SE 상을 연속 매질로 → SE-SE 점접촉 수렴저항을 안 풂 → σ_eff,ion = 강체-접촉 granular망의 **상한(upper bound)**, 우리 Kirchhoff/Holm σ 는 그 아래로 *constriction 만큼 깎임*" 이라 한 그 논리가 **TauFactor 에 그대로 적용**된다. TauFactor 와 Bielefeld2020 EJ-HEAT 는 *같은 voxel-flux-PDE 계열*(constriction-free 연속체 τ).
- **검증 정합**(Fig 8): TauFactor τ = Avizo XLab τ (둘 다 voxel-직접 연속체) 인데, *random walk·mean path·pore centroid* 등은 다른 값 → 이 분산 자체가 "**τ 는 method/정의 의존**(우리 3종 τ 가 다른 양)" 의 외부 증거.

### (3) 우리가 *더하는* 것 (TauFactor 가 비운 칸)
- ★ **constriction-resolved σ 삼중항**: TauFactor 는 *τ 한 descriptor* 까지. 우리는 그 τ(또는 우리 자체 bulk-τ) 위에 **Holm 점접촉 구속 + Stage-E 소성 접촉면적** 을 얹어 **σ_ionic·σ_e·σ_thermal** 을 *실제 전도도*로 푼다. = Bielefeld2019 가 "future work: Greenwood/Holm constriction" 으로 미룬 칸, Bazzoun2026 RNM 이 채운 칸, *우리도* 채우는 칸. TauFactor 는 그 칸을 **안 건드림**(애초 transport-descriptor 툴).
- **소성 morphology**: TauFactor 는 *입력* voxel 만 본다 — 그 voxel 을 *어떻게 만들지*(rigid DEM packing? MPM 소성 void-fill?)는 모름. 우리 MPM 이 만드는 *진짜 소성 형상변화*(SEM 일치)·void-fill flow 는 TauFactor 의 *상류*(우리가 더 잘 만든 미세구조를 TauFactor 에 먹임).
- **fracture·force-chain·Z·coverage**: 전부 우리 DEM 고유. TauFactor 는 τ·ε·SA·TPB·percolation·flux 까지.

---

## ★ 적용가능성 (applicability to our LIGGGHTS DEM + MPM model)

> 구체적으로: TauFactor 를 우리 모델에 *어떻게* 붙이나? 어떤 우리 출력에 대응하나? 무엇을 대체하고 무엇을 대체 못 하나?

- **(A) 우리 DEM dump → voxel → TauFactor τ (frame[4] 표준-툴 교차검증).**
  - **경로**: 우리 LIGGGHTS dump(예 `input_real_14`: atom 좌표 + 반경, 300 MPa 압밀 골격) → **voxel 화**(우리 `scripts/voxelize_microstructure.py` / `viz_mpm_continuum.py` / `extract_2d_microstructure.py` 가 이미 voxel/mesh 파이프라인 보유; 3D voxel union 으로 상 라벨 0=pore/1=AM/2=SE 부여) → `*.tif` 스택 export → **TauFactor**(GUI 또는 함수 직접호출) → 상별·방향별 **τ·ε·SA·TPB·percolation** 산출.
  - **무엇에 대응**: 산출된 τ = ★ **우리 τ_Laplace,bulk** (constriction 無). 우리 `voxel_conductivity.py` 의 bulk-Laplace τ 와 *직접 비교* → 일치하면 우리 voxel-τ 구현이 *표준 TauFactor 와 동급*(Avizo 가 TauFactor 를 검증한 방식의 mirror). ε = 우리 porosity 의 voxel-count cross-check.
  - **의미**: 우리 자체 voxel-Laplace solver 가 *검증된 표준*과 일치한다는 frame[4] 도장. **단 이건 우리 σ_ionic(constriction-resolved)을 검증하는 게 *아니라*, 그 *상한*(τ_Laplace,bulk)을 못박는 것** — 우리 σ_ionic 은 TauFactor τ *아래로* Holm 구속만큼 더 깎인 값이어야 *정상*(만약 우리 σ_ionic 이 TauFactor bulk-σ 보다 *높으면* 버그 신호).
- **(B) Huang2025 LBM-ETC 의 가벼운 τ-cross-check (내가 flag 한 그 자리).**
  - Huang2025 digest §적용가능성-A 에서 "우리 DEM dump 를 voxel 화 → LBM(또는 *더 가볍게 TauFactor τ만*)으로 ETC 독립 산출" 을 제안했다. **TauFactor 가 그 "더 가볍게 τ만" 경로**다 — full LBM 6×10⁵ iteration 없이 τ 만 빠르게(10⁶ voxel <30 s) 뽑아 우리 σ_thermal Ridge 의 `tortuosity_median`·`tortuosity_std` 입력을 *표준툴*로 검증.
  - ★ **결정적 이점**: Huang2025 *자신이* tortuosity 를 **TauFactor 로** 산출했다(그들 §6, ref 35). ⇒ 우리도 같은 툴 쓰면 *Huang 과 byte-동일 척도* 로 τ 직접 비교 가능 — "우리 LPSCl 양극 τ vs 그들 oxide 양극 τ" 를 *같은 정의*로(소재 차이만 남기고) 대조. (단 그들 위상별 τ 분리(pore↑→ETC↑, solid↑→ETC↓)를 우리 폼에 흡수하는 건 별개 작업 = Huang digest §8-③.)
- **(C) 우리 `voxel_conductivity.py` 의 표준-툴 벤치마크.**
  - 우리 voxel σ·τ 솔버를 *동일 입력 voxel* 에서 TauFactor 와 나란히 → "우리 voxel-Laplace ≈ TauFactor(=Avizo급)" 1-line 검증. ★ 단 **SA/TPB 는 voxel 근사**(Fig 7 ×1.5–2) → 우리 coverage/접촉면적을 voxel 로 뽑을 땐 TauFactor 와 *같은 한계* 공유 → 우리 *기하 KDTree·Stage-E* coverage(rigid_geometric + plastic_deformed)가 그 점에선 *더 정밀*함을 명시(우리 coverage 우위 유지).
- **(D) RVA = RVE 충분성 정량화.** 우리 "RVE ≥7.5× 최대입자" 경험칙을 TauFactor RVA(metric-vs-volume plot)로 *수치 그래프* 화 → 논문-grade RVE 근거.
- **한계(무엇을 대체 못 하나)**:
  - ❌ **우리 constriction-resolved σ(σ_ionic/e/thermal)를 대체 못 함** — TauFactor 는 *bulk τ(상한)* 만. 우리 Holm/Stage-E constriction 이 *그 위에 추가*되는 핵심 물리 → TauFactor 는 그것을 *검증*도 *대체*도 안 함(상한만 제공).
  - ❌ **소성 morphology·void-fill·변형장 없음**(입력 voxel 만 봄 — 그건 우리 MPM 상류 책임).
  - ⚠ **voxel 해상도 의존**: 우리 작은 SE(0.5 µm) 를 거친 grid 로 voxel 화하면 SE-SE throat 소실 → τ 가 *더 bulk 쪽으로* 편향(우리 mpm3d sub-cell under-resolution 함정과 동일). 충분 해상도(또는 우리 접촉망 σ 가 정답) 필요.
  - **소재 k/σ swap** = 불필요(τ 는 dimensionless·소재무관) — *우리 미세구조*만 넣으면 됨. (σ_thermal·σ_ionic 절대값으로 환산할 땐 우리 소재 σ_grain 을 우리 솔버가 곱함.)

---

## ★ frame[4] 위치 — TOOL 이지 경쟁자 아님 (no "our SOTA" claim needed)

> 이 논문은 *물리 모델*(DEM/MPM/FEM)이 아니라 *방법 TOOL* 이다. 따라서 "우리가 왜 SOTA 인가" 식의 novelty 주장은 **부적절** — TauFactor 는 우리와 *경쟁*하지 않는다. 올바른 프레임 = **"TauFactor 가 우리 τ 를 *검증/교차검증* 하고, 우리 접촉망 constriction 이 그것을 *넘어선다*"**.

1. ★ **TauFactor = 우리 τ_Laplace,bulk 의 frame[4] 표준-툴 검증자.** 우리 DEM↔MPM↔실험 을 서로 교차검증하던 frame[4] 에, TauFactor 는 *τ-계산 축의 표준 도장* 을 추가한다. 우리 자체 voxel-Laplace τ 가 *검증된 표준(TauFactor, Avizo 가 이미 검증)* 과 일치하면 = 우리 τ_Laplace,bulk 신뢰 보강. **이건 우리를 *깎는* 게 아니라 우리 bulk-τ 한 다리를 *세워주는* 것.**

2. ★ **우리 constriction 물리가 TauFactor 를 *넘어서는* 지점이 정확히 우리 transport novelty 의 위치.** TauFactor(+Bielefeld2020 flux-PDE + Bielefeld2019 percolation)는 모두 **점접촉 구속을 안 푼다(bulk/상한)**. Bielefeld2019 가 "future work: Greenwood/Holm" 으로 미루고, Bazzoun2026 RNM 이 채운 **그 SE-SE constriction 칸을 우리도 Holm+Stage-E 로 채운다**. ⇒ "TauFactor τ_bulk → (Holm constriction) → 우리 τ_eff·σ_ionic" 의 *내림차순 사슬* 에서 우리는 *맨 아래 정밀단*. TauFactor 는 그 사슬의 *상한 끝* 을 표준화해 준다.

3. ★ **method-다양성 경고(Fig 8) = 우리 3종 τ 분리의 외부 정당화.** TauFactor 자신이 "τ 는 정의·솔버마다 다르다(8-method 분산, voxel-직접만 일치)" 를 보였다 → 우리가 **τ_Dijkstra(geodesic) / τ_Laplace,bulk / τ_Laplace,eff** 를 *별도 양*으로 구분 보고하는 게 옳다는 권위 있는 근거. (TauFactor 는 그중 *voxel-bulk-Laplace* 한 종류만 담당 — geodesic·constriction-eff 는 우리가 추가로 푼다.)

⇒ **결론**: TauFactor 는 *경쟁 물리 모델*이 아니라 **우리 τ_Laplace,bulk 의 검증된 표준 계산 TOOL + Huang2025-호환 τ cross-check 경로**다. 우리는 그것을 *frame[4] 외부 교차검증*으로 도입하되, **우리 핵심(접촉망 Holm/Stage-E constriction 으로 푸는 σ 삼중항)은 TauFactor 가 닿지 못하는 *그 아래 정밀단*** 에 있다. TauFactor 가 우리 bulk-τ 상한을 못박으면, 우리 constriction 이 그 상한을 *물리적으로 얼마나 깎는지* 가 곧 우리 transport 기여의 정량(frame[5] 분업: TauFactor=bulk-τ descriptor / 우리=constriction-resolved σ).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
