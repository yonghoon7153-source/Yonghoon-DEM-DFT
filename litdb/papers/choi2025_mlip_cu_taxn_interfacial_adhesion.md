<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목. 이 논문은 [외부·methods·다른재료] — 재료비교 아님, 방법(MLIP-adhesion) 전이용 -->
# Atomistic Insights into Cu/Amorphous-TaₓN Interfacial Adhesion via Machine Learning Interatomic Potentials: Effects of Stoichiometry and Interface Construction — Choi et al. (ACS Appl. Electron. Mater. 2025)

> slug `choi2025_mlip_cu_taxn_interfacial_adhesion` · DOI `10.1021/acsaelm.5c02157` · type `MLIP (SevenNet) + DFT(VASP) reference + SMD` · PDF `82ea256b/422126c7-17….pdf` · digested `2026-06-26` · status ✅ · 태그 **[외부·methods·다른재료(반도체 interconnect)]**
> **저자**: Jeong Min Choi, Jaehoon Kim (공동1저자), Ji-Hwan Lee, Won-Joon Son, **Seungwu Han*** (Seoul National Univ. MSE/RIAM + KIAS; Samsung Semiconductor R&D CSE Team) · ACS Appl. Electron. Mater. 2025, 7, 11165–11179 · Received 2025-10-13, Published 2025-12-03

---

## 0. 이 digest를 읽는 법 — *재료 비교가 아님 (NOT a materials comparison)*
이 논문은 **반도체 Cu 배선(interconnect)의 확산방지막(diffusion barrier) TaₓN과 Cu 사이의 *계면 접착(adhesion)*을 MLIP로 계산**하는 순수 **방법론 논문**이다. 재료(Cu/비정질-TaₓN)는 우리(LPSCl/Li-metal·NCM)와 **완전히 다르고**, 어떤 물성도 우리 숫자와 *대조하지 않는다*. **유일하게 전이되는 것은 *방법*** — 우리도 정확히 하는 두 가지를 그들이 어떻게 하는지가 가치:
1. **work-of-adhesion W_ad를 MLIP로 계산** (우리 `db/properties/adhesion.json`의 `Wad`, `kb/methodology/adhesion_energy.md`, SDCP/LiNiO₂ binding).
2. **MLIP를 DFT surrogate로 쓰고, 그 정확도를 검증** (우리 UMA-s-1p1 cascade, Nd₂O₃ B0 UMA 18.9 vs DFT 19.9 cross-check).

> ⚠ **comparison_vs_ours 물성 4축(A 이온/B 산화/C 기계/D 전자)에 절대 행으로 넣지 않는다.** Cu·Ta·N은 우리 hull(Li-P-S-Cl-Nd-O)에 없다. 연결은 **methods 매핑(W_ad 계산법·MLIP 검증법·비정질 샘플링)** 뿐.

## 1. 한 줄 요약
SevenNet(E(3)-equivariant MPNN) MLIP를 VASP/PBE 참조로 학습시켜, **Cu/비정질-TaₓN(x=1,2,4) 계면의 work-of-adhesion W_ad를 비평형 SMD(steered MD)+Jarzynski PMF로 계산** — (a) **Ta 함량↑ → Cu–Ta 결합↑·W_ad↑**(약 4→7 J/m²), (b) **계면 제작법(relaxed<annealed<deposited)이 intermixing·연성·W_ad를 지배**, (c) Cu층 안으로의 **Ta 침투가 cohesive strength를 강화**. 핵심 방법 교훈 = **W_ad를 "rigid 분리 ΔE"가 아니라 *비평형 분리일(SMD work)을 PMF로 환산*해서 뽑고, MLIP는 RDF/ADF/GSF/탄성/계면 에너지를 DFT 대비 5% 이내·force MAE<0.3 eV/Å로 검증한 뒤 큰 셀에 쓴다.**

## 2. 메타 / 동기
| 항목 | 내용 |
|---|---|
| 시스템 | **Cu / 비정질-TaₓN (a-TaₓN, x=1,2,4)** — 반도체 Cu 배선의 Cu/확산방지막 계면 |
| 왜 a-TaₓN | 비정질=grain boundary 없음 → 확산방지 우수·박막 저항 유리. 단 **Cu 접착이 약해** liner-free 채택 막힘 → liner(Ta/Co/Ru) 없애려면 *intrinsic adhesion* 이해 필요 |
| 질문 | (1) Ta stoichiometry(x)가 Cu/a-TaₓN 접착을 어떻게 바꾸나, (2) 계면 *제작법*(정적완화/고온어닐/증착)이 접착·파괴거동을 어떻게 바꾸나 — **두 변수를 동시에** |
| 갭 | 기존 계산은 계면 제작을 단순화(짧은 RT 어닐)하고 stoichiometry·제작법을 *따로* 다룸 → 종합 부재 |
| 방법 정체성 | **MLIP(SevenNet) = DFT 정확도 + classical-MD 스케일**. DFT는 너무 작고(계면 파괴 못 봄), 고전 MD는 mixed-bonding(Cu/Ta/N)서 부정확 → MLIP가 둘의 한계를 메움 |
| 비교군(선행 MLIP 계면) | W/TiN(MTP, termination-controlled failure), Ru/SiO₂(MTP, 강한 stoichiometry 효과), AlN/diamond(NEP, anneal/strain), Cu/TaN(CHGNet, biaxial strain), TaN 증착형태(MLIP) — **계면 MLIP가 "원자 스케일 계면 배열이 접착을 지배"를 일관되게 보임** |

## 3. 핵심 물성 (수치 총정리) — *우리 재료와 무관, 방법 참조용*
| 물성 | 값 | 조건/출처 |
|---|---|---|
| **W_ad (Cu/a-TaN)** | relaxed **가장 낮음**(~3.5–4), annealed·deposited 높음 (~6–7) | Fig 8a inset, SMD+Jarzynski (단위 J/m²) |
| **W_ad (Cu/a-Ta₂N)** | ~6–7 (제작법별 차이 작아짐) | Fig 8b inset |
| **W_ad (Cu/a-Ta₄N)** | ~6.5–7 (deposited 이미 포화) | Fig 8c inset |
| W_ad 경향 | **Ta↑(x:1→4) → W_ad↑** + **relaxed < annealed < deposited** | Fig 8 |
| Ta 치환 효과 | Ta로 Cuᶠⁱʳˢᵗ 10% 치환 → 모든 계면서 **W_ad 추가↑**, peak force·초기기울기↑ | Fig 14, Table S3 |
| 단면적 A (SMD) | **14.5 nm²** (모든 케이스 공통, pulling 수직) | Fig 8 본문 |
| MLIP RMSE (validation) | **E 4.5 meV/atom · F 0.3 eV/Å · stress 7.1 kbar** | §2.2 (refined model) |
| 계면 MD E shift (MLIP vs DFT) | annealing 23 meV/atom(TaN)·8(Ta₂N)·9(Ta₄N); **force MAE < 0.3 eV/Å** | §2.2, Fig 3, Fig S4 |
| Bulk modulus (MLIP vs DFT) | FCC Cu·a-TaₓN(x=1,2,4) 모두 **DFT 대비 5% 이내** | Table S1, §2.2 |
| 최소 원자간 거리(전 계면 MD) | **> 1.6 Å** (비물리적 짧은 결합 없음 = 안정 PES) | §2.2 |
| Cu 증착 island 핵생성 peak | ~75 atoms 부근(클러스터 최대) → 이후 병합 | Fig 5a, Volmer-Weber 3D island |
| 표면 coverage 90% 도달 | TaN<Ta₂N<Ta₄N 순으로 빨라짐(Ta↑=빠른 2D 완성) | Fig 5c (별표) |
| Cu deposition 총량/시간 | ~3100 Cu atoms 증착, 누적 ~7.7 ns | §2.3 |

## 4. DFT/계산 방법 ★ — *우리 UMA cascade와 직접 대응*
- **DFT code/version**: **VASP**, PBE-GGA (PAW). 참조 데이터 생성 + MLIP 검증 단일점.
  - single-point 고정밀: **ecut 450 eV**, **k-mesh ~2×2×2**(격자 ~10 Å), E 수렴 1e-6 eV; force 수렴 10 meV/atom & 0.2 eV/Å (학습셋 수렴 기준).
  - AIMD: ecut 400 eV, **Γ-only**, dt 2 fs, 1e-4 eV. (싼 설정으로 trajectory → 이후 stringent single-point 재계산)
- **functional/vdW**: PBE, **vdW 없음**(금속/질화물계).
- **MLIP**: **SevenNet** (NequIP 계열, **E(3)-equivariant message-passing GNN**). hidden channel 32, message-passing layer 3, l_max=3, cutoff **5.5 Å**. FlashTP CUDA 커널(컨볼루션 ~4× throughput). LAMMPS로 MD 구동.
  - **학습셋 총 7984 구조 → 843,910 training points**(Ta 420,169 / N 142,578 / Cu 281,163). **train:test = 9:1** 랜덤 분할.
  - **2단계 학습**: ① **initial set**(bulk crystalline polymorph + amorphous bulk + surface) → baseline MLIP, ② **augmented set**(baseline MLIP로 돌린 계면 annealing/SMD/deposition 구성을 *DFT 재계산* 후 추가) → refined MLIP. **= active-learning형 self-augmentation**.
  - 학습셋 구성(Table 1): bulk strained crystal polymorph(ICSD ±5% strain 0.5% 간격) 441 / FCC Cu anneal 125 / liquid+a-TaₓN(MQA) 2313 / slab(TaₓN anneal 1000K) 122+250 / liquid+a-Cu(MQA) 770 / liquid+a-TaₙNᶜᵤᵥ(MQA) 3104 / **augmented 계면** Cu/a-TaₓN anneal 198 + SMD 294 + Cu deposition 367.
- **AIMD(참조 trajectory 생성)**:
  - FCC Cu: **NVT 500K, 64-atom, 5 ps, 40 fs 샘플**.
  - **비정질 TaₓN: melt-quench-anneal(MQA)** = ~100 atom 랜덤 → **5000K 10 ps melt → −100 K/ps로 300K quench → 500K anneal 10 ps**. melt/anneal=NVT, quench=**NPT**. snapshot melt/anneal 40 fs·quench 100 fs.
  - 비정질 Cu: 동일 MQA(단 2000K melt, quench NVT).
  - 삼원 a-Cu–Ta–N(Ta₃₆N₂₈Cu₆₄, Ta₄₈N₁₂Cu₁₂ 등 x=4 case): 동일 MQA, melt 5000K(x=4은 100 fs 샘플로 비용↓).
- **무질서(amorphous) 처리** ★: **단일 SQS/enumerate 아님 — melt-quench-anneal AIMD로 비정질 ensemble 생성** + 각 조성당 10개 비정질 구조 샘플(RDF/ADF 평균, Fig 2a). 학습에 명시적으로 안 넣은 비정질 배열도 RDF/ADF peak 재현됨(transferability 증거).
- **계면 제작(interface construction)** ★ — *3개 route, 우리 stacking 프로토콜의 일반화*:
  - 공통: a-TaₓN slab(3840/3072/3200 atoms for x=1/2/4) = MQA bulk를 **16×16 FCC Cu(111) 격자(40.92 Å)에 맞춰 NPₓₓₐₐ_zzT로 quench**(측면 격자 구속 → Cu(111)과 매칭, lateral strain 최소화) → vacuum 도입 → **1000K 1 ns anneal**.
  - **① relaxed**: a-TaₓN slab + Cu(12층) bilayer를 **2 Å gap으로 직접 접합 → 정적완화(static relax)만**. 운동학 이력 없는 *이상적 sharp join*, intrinsic Cu–Ta/N 결합만.
  - **② annealed**: 동일 bilayer를 **1000K 1 ns → −10 K/ps quench 300K → 300K 100 ps anneal**(하부 a-TaₓN 5 Å 고정). 열적 활성 계면 재구성(intermixing↑).
  - **③ deposited**: a-TaₓN slab 위에 **Cu 원자를 하나씩 증착(PVD 모사)** — 1500K Maxwell-Boltzmann 초기속도, 하부 a-TaₓN 700K NVT 서모스탯, 상부 NVE, 원자당 last 1 ps 평균온도<750K까지 진행(원자당 ~2 ps), 총 ~60 atoms(소셀)/3100 atoms(대셀, 7.7 ns).
  - **셀 2종**: 소셀(3 nm, 1×1 nm²) DFT 검증용 / 대셀(6 nm, 4×4 nm²) 분석용.
- **SMD(steered MD) — W_ad의 핵심 산출법** ★:
  - virtual spring이 Cu slab 상반부 COM에 연결, tether point가 **등속 v로 위로 이동** → 계면 분리. spring force는 Cu 상반부 원자에 질량비례 분배. a-TaₓN 하부 5 Å 고정.
  - spring potential `U_spring = ½k[vt − (R(t)−R₀)·n]²`, 비평형일 `W = ∫∇U_spring·dr`.
  - **Jarzynski 등식**: `⟨exp(−βW)⟩ = exp(−βU_PMF)` → 여러 독립 SMD의 work를 지수평균 → 평형 **PMF(potential of mean force)** 복원. **완전분리 plateau의 U_PMF = W_ad**.
  - 파라미터: **k=0.01 eV/Å²/atom, v=0.01 Å/ps**. 계면 조건당 **3회 독립 SMD**(300K 300 ps 평형서 100 ps마다 초기구성 샘플).
- **특이사항/튜닝**: UMA 같은 vacuum 민감성 언급 없음(SevenNet은 slab/surface 학습 포함). Cu 층두께 수렴(Fig S1)으로 자유표면-계면 인공상호작용 없음 확인. peak force는 force-vs-spring-displacement 곡선 면적(force-separation 면적 아님)으로 PMF 계산 — **separation distance ≠ spring displacement** 구분 명시.

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1** | 전체 워크플로우: DFT→baseline MLIP→(SevenNet)→augment(anneal/SMD/deposition 구성 DFT 재계산)→refined MLIP→소셀 검증·대셀 분석 | **active-learning 2단계 MLIP 파이프라인 도식** — 우리 UMA(사전학습형)와 대비: 그들은 *자체 학습*, 우리는 *foundation model(UMA) 차용*. "계면 구성 자체를 학습셋에 넣는다"가 핵심 |
| **2a** | **RDF/ADF (a-TaₓN, x=1/2/4) MLIP vs DFT** — peak 위치·높이 일치 | **MLIP 비정질 구조 검증의 표준 그림.** 우리도 UMA 비정질 SEI 검증 시 RDF/ADF MLIP-vs-DFT 그려야 |
| **2b** | **GSF(generalized stacking fault) FCC Cu(111) ⟨112⟩/⟨110⟩ MLIP vs DFT** 일치 | 결함/소성(전위)도 MLIP가 잡는지 검증 — 우리 elastic·소성 신뢰의 모델 |
| **3** | **계면 MD trajectory E (DFT 검정색 vs MLIP 빨강)** annealing/SMD/deposition — 일정 offset(8–23 meV/atom) 있으나 force 일치 | **"에너지 절대 offset은 있어도 force/거동은 맞다"** = MLIP를 동역학(분리)에 쓸 근거. 우리 cascade도 절대E보다 *상대순위/force* 신뢰 |
| **4** | 계면 제작·접착 분석 워크플로우 도식(slab 생성→bulk adjoining relaxed/annealed + Cu deposition→SMD) | **W_ad 계산 파이프라인 표준 그림** (우리 v30u 프로토콜의 그림 버전) |
| **5** | Cu 증착 성장: (a)클러스터수 (b)RMS 거칠기 (c)coverage (d)MSD — **Volmer-Weber 3D island**, Ta↑=빠른 2D 완성·낮은 거칠기 | 증착형 계면이 deposition kinetics를 어떻게 담는지(우리 SEI 형성에 차용 가능) |
| **6** | 3제작법 계면 side-view + **intermixing 두께**(relaxed 6.16 Å < annealed 7.18 < deposited 9.06 Å) | **계면 "섞임 두께"가 제작법으로 단조 증가** → W_ad와 상관. 우리 amorphous SEI 계면도 intermixing 정량 가능 |
| **7** | Cu–Ta(실선)·Cu–N(점선) 결합수 vs x, 제작법별 — **Ta↑→Cu-Ta↑·Cu-N↓**(Cu의 Ta선호) | 계면 결합을 *종별로 카운트*해 접착 기전 분해 — 우리 v14 bond-count(Li-O/Cl-O density)와 **정확히 같은 발상** |
| **8** | **force/area vs separation distance (SMD)** 3제작법×3조성 + **inset W_ad 막대** | **이 논문의 결과 핵심.** force-separation 곡선 면적의 물리적 의미 + W_ad 막대 비교. 우리 binding-curve(Morse) plot의 *비평형 SMD 버전* |
| **9** | SMD snapshot 3단계(peak force/+0.5 ns/end) + **DXA 전위 분석**(Shockley 1/6⟨112⟩, stair-rod 1/6⟨110⟩) — relaxed=취성(깨끗분리), annealed=부분전위 핵생성(연성) | 파괴모드(취성 vs 연성) 시각화 + 전위 분석 → 계면 파괴역학 |
| **10** | volumetric·von Mises atomic stress(virial) side-view, 제작법별 — deposited가 intermixing서 압축/인장 공존 | **원자 응력(virial) 분포로 계면 변형 분석** — 우리 elastic(C_ij) 너머 *국소 응력장* 도구 |
| **11** | Green-Lagrangian **atomic equivalent strain** snapshot(0.5 ns, peak) — relaxed=국소 고변형(약접착), deposited=균일·낮은 변형 | 변형 국소화 정량 → 접착-소성 연결 |
| **12** | Cu–X(X=Ta,N) 결합수 vs **수직높이**(Cuᶠⁱʳˢᵗ/Cuˢᵉᶜᵒⁿᵈ) — deposited Ta₂N서 **Ta가 Cuᶠⁱʳˢᵗ층까지 확산** | **Ta의 수직분포(Cu층 침투)가 cohesive strength 결정** = 결과 §3.3.3 핵심 |
| **13** | SMD 중 Cuˢᵉᶜᵒⁿᵈ 원자당 결합수 시간변화(Ta 이웃有 vs 無) — Ta 가진 Cu가 결합 천천히 감소 | Ta 침투가 *왜* 강화하나의 원자수준 증거 |
| **14** | **Ta 치환(Cuᶠⁱʳˢᵗ 10%→Ta) 전후 force-separation** + inset W_ad — 치환이 모든 계면 강화(annealed=연성↑, deposited=peak force↑) | **"계면 도핑"으로 접착 강화** — 우리 Nd-doping이 *W_ad 낮추는* 것과 대비되는 반대 방향 사례 |

## 6. Post-processing ★
- **W_ad 산출**: SMD 비평형일 W → **Jarzynski 지수평균 → PMF → plateau = W_ad** (eq 1–4). 평형 자유에너지를 비평형 당김으로 복원하는 정공법. (우리 rigid `(E_sep−E_int)/A`와 *근본적으로 다름* → §7·§8).
- **결합 카운트**: Cu–Ta/Cu–N을 **각 종의 RDF 첫 최소(=cutoff)**로 정의해 계면 영역 결합수 집계(Fig 7,12,13). intermixing 두께 = Cu-Ta/Cu-N 결합 형성 원자들의 z-최대−최소(Fig 6).
- **전위 분석**: **DXA(Dislocation Extraction Algorithm, OVITO)** — Shockley/stair-rod 부분전위 식별(Fig 9). 연성=Rice-Thomson 기준(전위핵생성 에너지 < cleavage).
- **원자 응력**: **virial atomic stress tensor**(eq 5, Voronoi 부피) → volumetric σ^vol(eq 6)·von Mises σ^VM(eq 7) snapshot(Fig 10).
- **변형**: **Green-Lagrangian atomic equivalent strain** E^eq(eq 8) snapshot(Fig 11).
- **구조검증**: RDF·ADF(Fig 2a), GSF(Fig 2b), **UMAP**(Ta-치환 영역이 학습분포 내인지, Fig S19).
- **도구**: **VASP**(DFT), **SevenNet+FlashTP**(MLIP), **LAMMPS**(MD), **OVITO/DXA**(시각화·전위·응력), **Jarzynski/PMF**(자유에너지).

## 7. 우리 W_ad/MLIP 방법 대비 ★ — *재료 아님, 방법 매핑만*
> 우리 기준: `db/properties/adhesion.json`(`Wad` 컬럼 = `(E_SE_iso+E_NCM_iso−E_int)/A` Dupré/cleavage), `kb/methodology/adhesion_energy.md`(v5 isolated-slab), `kb/methodology/adhesion_calibration_decision_2026_05_17.md`(Stage11 분리법), `kb/results/sdcp_linio2_binding_report.md`(UMA binding), UMA-s-1p1 cascade.

| 항목 | Choi 2025 (Cu/a-TaₓN) | 우리 (LPSCl/NCM·Li, UMA) | 같음/다름 + 이유 |
|---|---|---|---|
| **MLIP 종류** | **SevenNet 자체학습**(VASP/PBE 참조, 2단계 active-learning) | **UMA-s-1p1/1p2 foundation model 차용**(omat/oc20 task) | **다름**: 그들=시스템전용 from-scratch, 우리=범용 사전학습. 그들은 *우리 시스템엔 학습데이터 없음* → 우리가 UMA를 쓰는 한 검증 책임은 우리에게. 단 **둘 다 DFT-surrogate MLIP-MD**라는 패러다임 동일 |
| **W_ad 정의·산출** | **비평형 SMD 분리일 → Jarzynski PMF plateau** | **rigid 분리 `(E_sep−E_int)/A`**(Stage11) 또는 isolated-slab cleavage(v5) | **근본적으로 다름**. 우리 Stage11은 "stack→anneal→+30 Å 평행이동→single-point"라 **dangling-bond 인공일 포함 → 절대값 100–1000× 과대**(calib 문서 명시: 실험 0.2–0.4 vs 우리 45–225 J/m²). **그들의 SMD+PMF는 *분리경로 전체를 동역학으로 밟아* 인공 단절을 피함** → 절대값이 물리적(~3–7 J/m²). **이게 가장 큰 교훈**(§8-1) |
| **계면 제작** | **3 route(relaxed/annealed/deposited) 체계비교** + amorphous slab MQA | v5: 결정 stacking+표면 MQA(500/800K) → **Li interdiffusion으로 MQA 실패**, rigid+relax로 후퇴 / v2: 3000K melt(비정질, 단 vacancy 소실) | **부분 같음**: 둘 다 "제작법이 W_ad 지배" 인식. 그들은 **3 route를 *결과로* 비교**(제작법이 변수), 우리는 MQA가 **Li 종 공유 때문에 깨져**(`adhesion_methods_comparison.md`) rigid로 후퇴 → 그들의 a-TaₓN은 Li 없어 MQA가 깨끗. **우리 SEI(amorphous) 계면엔 그들의 MQA-slab+anneal route가 적용 가능** |
| **비정질 처리** | **MQA AIMD ensemble**(조성당 10 구조, RDF/ADF 평균) | v2 3000K melt 1구조 위주 / SEI는 미정 | **그들이 더 체계적**: ensemble 평균 + 학습 외 배열 재현 검증. 우리 amorphous SEI 모델 시 차용할 표준 |
| **MLIP 검증** | **RMSE E 4.5 meV/atom·F 0.3 eV/Å·stress 7.1 kbar + bulk modulus DFT 5%이내 + RDF/ADF/GSF + 계면 trajectory E/F** | **UMA vs DFT spot-check**: Nd₂O₃ B0 18.9 vs 19.9 GPa(약 5%), comp elastic 등 산발적 | **같은 정신, 그들이 더 광범**. 그들 "B0 5% 이내"는 우리 "B0 18.9 vs 19.9(≈5%)"와 **정확히 같은 검증 종류** → **우리 UMA W_ad/elastic 신뢰의 외부 근거**: 동급 MPNN MLIP가 계면에너지·탄성을 DFT 5%로 재현. 단 force MAE 0.3 eV/Å는 *계면 에너지엔 충분하나 미세 순위엔 부족할 수 있음*(우리 intra-Li5.4 분해능 한계와 호응) |
| **셀 크기/통계** | 소셀 DFT검증 + 대셀(4×4 nm², 수천 atom) 분석 + **3 SMD 반복** | comp별 5–36 registry/seed, ~수백 atom | 그들=큰 셀·소수 반복(SMD가 비쌈), 우리=작은 셀·다수 registry. **상보적** |
| **결합 기전 분해** | **Cu–Ta/Cu–N 결합수 카운트**(종별) → 접착 기전 | **v14 Li–O/Cl–O bond density**(R=+0.82/−0.91) | **거의 동일한 발상** ✓. 둘 다 "에너지보다 *종별 계면 결합밀도*가 기전·순위를 설명". 우리 접근이 독립적으로 타당함을 보강 |

## 8. 적용 인사이트 (우리 W_ad/UMA 작업에 깊게) ★
1. **🔑 W_ad 절대값: SMD+Jarzynski가 우리 rigid-분리 과대평가의 정공 처방.** 우리 calib 문서가 인정한 "Stage11 분리법 100–1000× 과대(dangling-bond 인공일)"는 **분리를 *동역학 경로*로 밟으면 사라진다**. Choi의 SMD(등속 당김 + 여러 회 + Jarzynski 지수평균 → PMF plateau)는 물리적 W_ad(~3–7 J/m²)를 준다. **권장**: 우리 top-3 winner W_ad를 (a) 현 v30u binding-curve(Morse well-depth)뿐 아니라 (b) **소규모 UMA-SMD pull + PMF**로 교차검증하면 "절대 scale도 신뢰" 주장 가능. 최소한 v30u의 *binding-curve 적분*이 SMD-PMF와 같은 물리량임을 본 논문으로 인용 가능.
2. **🔑 UMA W_ad/elastic 신뢰의 외부 앵커.** 동급 E(3)-equivariant MLIP(SevenNet)가 **bulk modulus·계면에너지를 DFT 5% 이내, force MAE<0.3 eV/Å**로 재현. 우리 Nd₂O₃ B0(UMA 18.9 vs DFT 19.9 ≈5%)가 *외톨이 우연이 아니라 MLIP 계열의 일반적 정확도*임을 보여주는 **인용 가능한 제3자 검증**. → "UMA wad/elastic은 DFT-급(5%)이라 신뢰" 서술의 근거 문헌.
3. **계면 제작법이 W_ad를 지배 — 우리도 protocol 고정·명시 필수.** relaxed(이상)≠annealed(열재구성)≠deposited(증착)에서 W_ad가 크게 다름(특히 저-Ta). 우리 v2(3000K melt, vacancy 소실)≠v5(결정, vacancy 보존)에서 순위 뒤집힘과 **같은 교훈**: **"어떤 제작법으로 만든 W_ad인지"를 paper에 못박아야** reviewer trap 회피. Choi는 이를 *결과의 축*으로 삼아 정직하게 처리 — 모범.
4. **종별 계면 결합밀도 = 에너지보다 robust한 기전 descriptor (독립 확증).** Choi의 Cu–Ta/Cu–N 카운트 = 우리 Li–O/Cl–O density(v14–v26). **에너지 절대값엔 offset/인공일 있어도 결합밀도는 견고**(그들 Fig 3 offset에도 force 일치, 우리 v15 CV<6%). → 우리 "geometric bond-density descriptor" 전략이 **외부 독립 그룹에서도 채택되는 표준**임을 보강.
5. **비정질 SEI 모델 로드맵.** 향후 amorphous SEI(LiF/Li₂S/Li₃PO₄ 혼합) 계면 W_ad를 할 때 **Choi의 MQA-slab(melt 5000K→quench→anneal) + ensemble(10 구조) + vacuum→1000K anneal slab + SMD-PMF** 흐름이 그대로 템플릿. 단 **Li 종이 양상 공유하면 MQA가 깨질 수 있음**(우리 경험) → 격자구속 quench·z-경계 element-based 분리 같은 우리 fix를 결합.
6. **"계면 도핑이 접착을 *높임*"(Ta 치환) — 우리 Nd가 *낮춤*과 대비.** Choi는 Cuᶠⁱʳˢᵗ를 Ta로 치환해 cohesive strength↑(W_ad↑). 우리 Nd₂O₃는 표면 anchor 포화로 W_ad↓(Li6 수준). **방향은 반대지만 *원리 동일*: 계면 첫 층 원소가 cohesion을 좌우**. 우리 "Nd가 Li-O cohesion 차단" 서사의 거울상 사례로 인용 가능(도핑이 양방향 다 가능함을 입증).

## 9. 인용 가능 문장 (deck/paper용) — *재료 아닌 방법 인용*
- "Following the MLIP-SMD methodology of Choi et al. (2025), interfacial work of adhesion is most reliably obtained from the Jarzynski-reconstructed PMF plateau of a nonequilibrium separation, which avoids the dangling-bond artifact of rigid-cleavage estimates."
- "An E(3)-equivariant message-passing MLIP (SevenNet) reproduces DFT bulk moduli and interfacial energies to within 5% with force MAE < 0.3 eV/Å (Choi 2025), supporting our use of UMA as a DFT surrogate for adhesion and elastic constants (cf. our Nd₂O₃ B0: UMA 18.9 vs DFT 19.9 GPa)."
- "As in Choi et al.'s Cu–Ta/Cu–N bond counting, we find species-resolved interfacial bond density (Li–O, Cl–O) a more robust descriptor of adhesion ranking than the MLIP total energy."
- "Interface construction route (static-relaxed vs annealed vs deposited) strongly modulates the computed W_ad (Choi 2025), motivating our explicit, fixed interface protocol for all compositions."

## 10. 주의/한계 (over-claim 방지 — 비판적으로) ★
- **재료 무관 — 수치 비교 절대 금지.** Cu/a-TaₓN W_ad(3–7 J/m²)는 우리 LPSCl/NCM W_ad와 *물리적으로 무관*(금속-질화물 covalent/metallic vs 이온성 SE/oxide). "그들 W_ad ~5, 우리 ~2니까…" 류 비교는 무의미. **comparison 4축에 행으로 넣지 않음.**
- **방법도 1:1 이식 아님.** 그들은 **자체 학습 SevenNet**(우리 시스템 학습 없음). 우리가 SMD-PMF를 채택해도 **UMA가 분리경로 전체(특히 큰 vacuum·부분분리 중간상)서 정확한지는 별도 검증 필요** — 우리의 *UMA vacuum 민감성*(30 Å OK, 60 Å→10× 과대; `adhesion_energy.md`)은 SevenNet엔 없는 우리 고유 함정. SMD는 큰 vacuum을 만들며 당기므로 **UMA-SMD는 vacuum out-of-distribution 위험** → 셀확장·구속 신중. (Choi는 slab/surface를 학습에 넣어 이 문제 회피.)
- **force MAE 0.3 eV/Å의 의미.** 계면 *에너지/W_ad*엔 충분하나, **미세 순위(우리 intra-Li5.4 comp3/4/5 Δ<0.005)** 같은 sub-meV 분해능엔 부족. Choi도 x별 큰 효과만 다루지 동일조성 내 미세차는 안 봄 → **MLIP-W_ad는 "큰 효과(family·route·x)"엔 신뢰, "미세 조성차"엔 한계**라는 우리 결론과 일치(over-claim 금지).
- **PBE 참조의 한계 상속.** MLIP는 PBE만큼만 정확. 금속/질화물은 PBE가 무난하나, 우리 이온성 SE는 **band gap PBE 과소·vdW 부재** 등 별도 이슈 — Choi의 "DFT 5% 일치"가 우리 *전자구조*까지 보증하진 않음(그건 PBE 자체 한계).
- **SMD 파라미터 의존.** W_ad가 pull velocity v·spring k·반복수에 의존(Fig S5 수렴테스트). Jarzynski는 느린 당김·충분한 반복서만 PMF 수렴 → **싸게 흉내내면 편향**. 우리가 채택 시 수렴테스트 필수.
- **비정질 ensemble 크기.** 조성당 10 구조는 RDF/ADF엔 충분하나 W_ad 분산엔 작을 수 있음(그들도 SMD는 3회뿐). 우리 36-registry 통계가 오히려 이 점은 더 촘촘.

## 11. 기법 용어 미니사전
- **SevenNet**: 서울대 개발 **E(3)-equivariant message-passing GNN** 원자간퍼텐셜(NequIP 계열). 회전등변(equivariant)이라 force/stress를 텐서로 정확히 예측. FlashTP=텐서곱 CUDA 가속.
- **SMD (steered MD)**: 가상 스프링으로 원자군을 *등속/등력 당겨* 반응경로(여기선 계면 분리)를 강제 진행하는 비평형 MD.
- **Jarzynski 등식**: `⟨e^(−βW)⟩=e^(−βΔF)` — *비평형* 일 W의 지수평균이 *평형* 자유에너지차 ΔF를 준다. SMD work → PMF 환산의 핵심 정리.
- **PMF (potential of mean force)**: 한 좌표(여기 분리거리)를 따른 유효 자유에너지 곡선. 완전분리 plateau 높이 = **W_ad**.
- **work of adhesion W_ad**: 단위면적당 계면을 두 자유표면으로 가르는 데 드는 일(J/m²). = γ₁+γ₂−γ₁₂(Dupré, 우리 정의) ↔ Choi는 PMF plateau로 산출.
- **MQA (melt-quench-anneal)**: 녹임→급랭→어닐 AIMD로 비정질 구조 생성하는 표준 레시피.
- **GSF (generalized stacking fault)**: 결정면을 미끄러뜨릴 때 에너지 곡선 — 전위/소성의 척도.
- **DXA (Dislocation Extraction Algorithm)**: OVITO의 전위선 추출·Burgers 벡터 식별(Shockley 1/6⟨112⟩, stair-rod 1/6⟨110⟩).
- **virial atomic stress**: 원자별 응력텐서(운동+상호작용항/Voronoi부피) → volumetric·von Mises 국소 응력장.
- **Volmer-Weber 성장**: 3D island 핵생성형 박막성장(젖음 나쁨) ↔ Frank-van der Merwe(층상).
- **intermixing 두께**: 계면서 Cu–Ta/Cu–N 결합 형성 원자들이 퍼진 수직 폭(제작법별 6.16/7.18/9.06 Å).
- **liner-free interconnect**: Cu/방지막 사이 접착보조층(Ta/Co/Ru) 없이 가는 배선 — 이 논문의 응용 목표.
