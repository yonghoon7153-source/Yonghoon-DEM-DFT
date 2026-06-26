# Cooperative Ion Conduction Enabled by Site Percolation in Random Substitutional Crystals — Ishikawa, Takae, Kurita (arXiv 2025 / PRL-class)

> slug `ishikawa2025_site_percolation_cooperative_ion_conduction` · DOI/arXiv `arXiv:2505.00362v2` (SI DOI `10.1103/9dxs-35z7` → published APS, PRL/PRX-class) · type `theory / classical MD (lattice-Coulomb)` · PDF `85999785-11._Cooperative…Site_Percolation….pdf` (= dup upload `34a1e3af-2505.00362v2.pdf`) · digested `2026-06-26` · status ✅
> **저자**: Rikuya Ishikawa¹, Kyohei Takae², Rei Kurita¹ — ¹Tokyo Metropolitan University (Dept. of Physics), ²Tottori University (Mechanical & Physical Engineering). 교신 Ishikawa / Kurita.
> **태그**: `[외부]` `theory` — argyrodite 논문 아님(rock-salt 모델계). **물성 4축 절대 비교 금지**: 우리 LPSCl 수치와 직접 대조 X. 보관 이유 = **우리 cascade dopant-blocking·dual-x·percolation 멘탈모델의 *이론 백본*** (개념/임계값 프레임 only).

---

## 0. 이 digest를 읽는 법 (가장 중요)
이 논문은 **"무질서 치환 결정(random substitutional crystal)에서 장거리 이온전도는 *국소 hop이 쉬운가*가 아니라, 운반이온이 점유하는 자리들이 *연결된 침투망(percolating network)을 이루는가*가 결정한다"** 는 한 가지 주장을 MD로 증명한다. 즉 **운반이온 농도 x가 site-percolation 임계 pc를 넘는 순간 σ가 급등**하고, 그 임계는 격자의 percolation 문턱(FCC ≈ 0.2)과 **수치적으로 일치**한다.

> 🔑 **우리에게 왜 중요한가**: 우리 cascade는 *random substitution*(dopant를 Li/anion 자리에 무작위 치환) 그 자체다. 이 논문이 주는 것은 **"dopant가 Li 자리를 *제거/차단*하면 운반망의 점유율이 pc 아래로 떨어질 때 σ가 붕괴한다"** 는 *임계(threshold) 개념틀*이다. 우리 tier2 `dopant_blocking_fraction`(dopant가 망에서 자리를 빼는 비율)·`migration_volume_fraction`(BVSE 병목 = 침투하는 저장벽 부피)·Nd σ-drop(0.52×)·dual-x(Sc2O3 0.75@x0.25 → 0.25@x0.0625)를 **percolation 언어로 *재해석***할 수 있게 한다.
>
> ⚠ **정직하게**: 이건 **프레임/임계 *개념*이지 우리 숫자와의 정량 일치가 아니다.** 모델계가 다르고(LiₓPb₁₋₂ₓBiₓTe rock-salt vs Li₆PS₅Cl argyrodite), 결합도 단순화(WCA+Coulomb만), 도판트-Li 차단 메커니즘도 우리와 화학이 다르다. **pc=0.2를 우리 LPSCl에 그대로 대입 금지.** 우리 sibling 분석(`hopping`/Nd 결론)은 Nd σ-drop이 *Ea 차단이 아니라 connectivity/prefactor 차단*임을 이미 보였고, 이 논문이 바로 그 "connectivity가 σ를 지배" 그림의 이론적 근거다.

## 1. 한 줄 요약
LiₓPb₁₋₂ₓBiₓTe rock-salt 무질서 결정의 MD에서 **σ는 x≈0.2를 넘는 순간 급등**하고, 이 문턱이 **FCC 양이온 부격자의 site-percolation 임계(≈0.2)와 일치** → 장거리 이온전도는 **운반이온이 만드는 침투 클러스터를 통한 *cooperative knock-on(연쇄 밀어내기)*** 으로 일어나며(단일이온 hop이 아님), 결정구조를 깨지 않고도 안정성↔전도성 trade-off를 푸는 **보편 설계원리 = "운반이온 농도를 pc 위로"** 를 제시.

## 2. 메타 / 동기
| 항목 | 내용 |
|---|---|
| 모델계 | **LiₓPb₁₋₂ₓBiₓTe** rock-salt RSIC (= random substitutional ionic crystal). AgInSnPbBiTe₅ 고엔트로피 rock-salt에서 유도(monovalent cation을 Li⁺로 치환). |
| 핵심 질문 | 메조스케일 운반이온 *공간배치/연결성* ↔ 거시 σ 의 관계 — "협동운동이 중요"는 알려졌으나 그 구조적 organization과 σ의 다리가 비어 있었음 |
| 방법 | **자체개발 고전 MD**(WCA 배제부피 + Coulomb, 외부 전기장 E 하). DFT/AIMD/KMC 아님. |
| 동기 | superionic conductor 설계의 근본 trade-off(안정성 vs σ): 과도핑은 구조 불안정·이온 과밀로 오히려 σ↓([13–15]). RSIC(고엔트로피류)는 configurational entropy로 안정 + element-specific 시너지 → trade-off 극복 후보 |
| 선행(자기) | 같은 그룹 AgInSnPbBiTe₅ MD([31,32]): In⁺이 자발적 Frenkel defect 형성→확산 촉진. 본 논문은 거기서 "carrier 연결성→σ" 다리를 놓음 |
| 운반이온 charge | 전하중성: n(Li⁺)=n(Bi³⁺) (Bi³⁺가 +charge 보상). x = Li 분율 |

## 3. 핵심 수치 (정량 총정리)
> ⚠ 모두 **환원단위(reduced units)** — σ₀=0.34 S/cm, E₀=6.61×10⁸ V/m, T₀=295 K, t₀=3.18 ps, P₀=4.71×10⁷ Pa 로 정규화. **우리 LPSCl 절대값과 직접 비교 금지.**

| 물성 | 값 | 조건/비고 |
|---|---|---|
| **site-percolation 임계 pc** | **≈ 0.2** | FCC 양이온 부격자 site-percolation([Stauffer-Aharony 38]). **이게 논문의 중심 수치.** |
| σ 급등 onset (x) | **x ≈ 0.2** | E-방향 무관(001/101/111 동일). x<0.2 σ≈0 |
| 최대 클러스터 길이 Lc | x=0.2부터 증가, **x≥0.25서 Lc=1**(완전침투) | Lc=1 = 시뮬박스 가로지름(침투). x=0.2서 큰 error bar = 간헐적 끊김 |
| σ(Li₁/₃Pb₁/₃Bi₁/₃Te, T=1.0=295K) | **6.8 × 10⁻³ S/cm** | = σ₀ 0.34 × 환원σ. **액체전해질급**이라 주장 |
| σ vs σ_NE(Nernst-Einstein) 격차 | **σ_NE가 ~2 orders 작음** | 단순확산(NE)으론 설명 불가 → **cooperative motion + 공간 비균질성**이 지배(핵심 증거) |
| cooperative event 정의 δ | **0.34**(=Li⁺ 이온지름) | min(\|Δrᵢ\|,\|Δrⱼ\|)≤δ 이면 두 이온 협동. **2–7개 연쇄 red-arrow** 관측(E≠0), E=0선 거의 없음 |
| Li⁺ 이온지름 d | 0.344 (Te⁻² d=4.42 Å 기준 정규화) | Pb²⁺ 0.538, Bi³⁺ 0.466, Te²⁻ 1.00 |
| 상호작용 ε | 295 k_B J | 일정 가정 |
| 시스템 크기 N | **24³ = 13824** 입자 | rock-salt, cation 무작위 배열 |
| 전기장 E | 2.1(주), 0.01P₀ 저압도 정성 동일 | E 방향 (001)/(101)/(111) |
| **Na⁺/Ag⁺ 치환** | pc 동일(x≈0.2)이나 σ **~1 order 작음**, K⁺/Ag⁺ 결정 x>0.2/0.33서 붕괴 | "pc는 보편, 절대 σ는 cation-anion 크기차 의존" |
| 무질서 처리 | **단일 무작위 배열**(cation type 랜덤 decorate), SQS/enumerate 아님 | N=13824라 단일 배열로 통계 충분 |

## 4. DFT/계산 방법 ★ — (DFT 아님: 고전 MD)
- **code**: 자체개발 MD(self-developed). **DFT·AIMD·KMC·MLIP 전부 아님.**
- **퍼텐셜**: U_total = U_WCA(배제부피, Weeks-Chandler-Andersen, repulsive-only LJ) + U_q(Coulomb, −k qᵢqⱼ/rᵢⱼ). **다른 상호작용 전부 무시** — 이온전도 *1차 인자(배제부피+Coulomb)만* 격리하려는 의도적 미니멀 모델.
- **운동방정식**: mᵢ d²rᵢ/dt² = qᵢE + Σ −∇(U_WCA+U_q) (Eq.1). leap-frog, Δt=0.002.
- **Coulomb**: Ewald summation(α=0.6, real cutoff 6 d_Te, k-cutoff 11(2π/L), force RMS err <10⁻⁴). PBC.
- **앙상블/제어**: 초기 NPT 200(Andersen barostat + Nosé-Hoover) → 정상상태까지 300 대기 → Parrinello-Rahman stress + Nosé-Hoover T 고정, E 인가. thermostat τ=0.1, barostat τ=1.
- **T/P/E**: T=T₀=295K, P=P₀(또는 0.01P₀≈대기압, 정성 동일), E=2.1.
- **σ 계산**: σ=⟨J⟩/E (Eq.4), J=⟨Σ qᵢvᵢ/V⟩ (Eq.5). vᵢ는 Δt=10 윈도우 변위/시간(요동 억제). **E방향 성분만**(수직성분 σ≈0). NE σ는 D에서 별도 추정(비교용).
- **무질서 처리**: **단일 무작위 cation 배열**. SQS/enumerate/실험점유 decorate 전부 아님.
- **검증**: 선행 AgInSnPbBiTe₅([32])에서 같은 퍼텐셜이 종음속·융점 실험과 정성일치 → rock-salt telluride에 합리적.
- **특이/한계**: rock-salt telluride 추상모델. **재료별 정량예측 아님**(저자도 명시: 정량 필요시 DFT/MLIP로 확장이 "natural next step"). vibrational entropy·polarizability·공유결합성 전부 빠짐.

## 5. 결과 — 섹션별 상세

### 5.1 σ vs x — 급등 문턱 x≈0.2 (Fig.1, Sec.III)
- E=2.1 인가, σ(좌축) vs x. **x 작을 때 σ≈0 → x≈0.2 넘으며 *급격히* 증가**. E 방향(001/101/111) 무관(symbol square/triangle/diamond 겹침).
- **σ_NE(E=0, Nernst-Einstein, D 기반)** 도 단조증가하나 σ(Eq.4)보다 **약 2 orders 작음** → 🔑 "**단순확산이 아니라 cooperative motion + 공간 비균질성이 지배**"의 직접 정량증거.
- **σ 등방성**(E방향 무관)이 주목할 점: Li⁺ 입장서 (001)/(111)은 이웃이 anion, (101)은 cation — 국소 potential landscape가 다른데도 σ 동일 → **거시 구조인자(침투망)가 국소 결정환경을 압도**.

### 5.2 Lc — 최대 클러스터 길이 (Fig.1 우축)
- Lc = 시간평균 최대 Li 클러스터 길이, 박스 가로로 정규화(**Lc=1 = 침투**). **x=0.2부터 증가 시작 = percolation onset**, **x>0.25서 Lc≈1**(안정 침투망). x=0.2의 큰 error bar = 클러스터 간헐적 끊김. → σ급등과 Lc급등이 *같은 x*에서 = σ↔침투 강한 상관.

### 5.3 전도 경로 가시화 — knock-on (Fig.2)
- (a–c) Δr>3(시간 Δt=300) 큰 변위 Li⁺ 궤적, x=1/3, E 001/101/111. 색=개별 Li⁺. **궤적이 E방향 정렬 + 서로 크게 겹침 = 특정 전도 경로(pathway) 형성**. **결정구조 유지** → 🔑 **knock-on(연쇄 밀어내기)**: 한 Li⁺ 변위가 이웃을 연속 밀어 격자 골격 안 깨고 이동. 경로 간 간헐 전환(inter-pathway hopping)도 관측.
- (d) 도식: **single-ion hopping(파랑 단일화살) vs cooperative knock-on(빨강, rᵢ(t)→rⱼ(t)로 밀고 rⱼ가 다음으로)**.
- (e) Δr>0.7(≈1 격자 hop, Δt=1) 변위벡터 스냅샷, x=1/3, E=101. cooperative event(δ=0.34) = 빨강, single = 파랑. **2–7개 연쇄 빨강 화살** 흔함. E=0선 cooperative 거의 없음 → **knock-on은 전기장이 유도**.

### 5.4 클러스터 percolation 직접 관찰 (Fig.3, Sec.III)
- Li⁺ 클러스터 = nearest-neighbor cation 자리 점유 Li끼리 한 클러스터. 3대 최대 클러스터 색(파/빨/초).
- **x=0.15**(Fig.3a): 작은 고립 클러스터만(tiny). **x=0.20**(Fig.3b): 클러스터가 *간헐적* 침투(가끔 끊김=non-percolating), 2·3위 클러스터도 큼 → **percolation onset 직전/경계**. 이 점이 σ 증가 onset과 일치. **x=0.25**(Fig.3c): 대부분 Li가 **단일 거대 클러스터로 시스템 가로지름 = 완전침투**.
- 시간진화: 미시적으론 Li가 클러스터 in/out 계속 출입하나, **거시적으론 침투 클러스터 구조 거의 불변**(통계적 정상).
- 🔑 **FCC site-percolation 임계 ≈ 0.2([38])와 정확히 일치** — rock-salt cation 자리 = FCC. "x≈0.2서 σ급등 = 그 자리가 FCC percolation 문턱 도달".

### 5.5 클러스터가 정말 전도하는가 (Fig.4)
- (a) x=0.2서 Δξ(E방향 평균변위, Δt=10) 시간추이: **최대클러스터 소속 Li(빨강·원) ≫ 그 외 클러스터(파랑·사각, 거의 0)**. → 🔑 **침투 클러스터 이온만 mobile**, 작은 클러스터 이온은 거의 안 움직임.
- (b) ⟨Δξ⟩ vs x: x<0.2 양쪽 ≈0; **x≥0.2서 최대클러스터 이온만 급증**, 작은 클러스터는 계속 ≈0. → **장거리 전도는 percolation 문턱 위 거대 클러스터가 전담**.

### 5.6 다른 cation 보편성 (Fig.5, Sec.III 말미)
- Li⁺→Na⁺/K⁺/Ag⁺(지름 0.461/0.624/0.520) 치환. **K⁺·Ag⁺ 결정은 E 인가 시 x>0.2/x>1/3서 붕괴**(구조 불안정), **Na⁺는 구조 유지**.
- σ(X=Ag,Na) vs x: **둘 다 x≈0.2서 σ 증가 시작(pc 동일)**, 단 σ **절대값 ~1 order 작고 상승 완만**. → **pc(0.2)는 cation 무관 보편, 절대 σ는 cation-anion 크기차에 의존**(작은 Li⁺가 가장 빠름).

### 5.7 Discussion — anion-cation 크기차 (Sec.IV)
- 본 모델은 site-percolation 문턱 = 전도 percolation 문턱 *일치*. **그러나 일반 rock-salt에선 불일치**: 다른 계는 **국소구조([49,50])·chemical short-range order([51])가 hop 장벽을 지배**, 전도경로는 *저장벽 영역*을 따라 생기고, **저장벽 영역이 침투할 때 고전도**(여기서 [49–51]=Ceder 그룹 disordered rock-salt cathode 계열).
- 본 계는 anion이 큰 Te²⁻(4.42 Å), 다른 계는 작은 O²⁻(2.80 Å) → **anion-cation 크기 mismatch가 전도경로 형성·유효 percolation 문턱을 다르게 함**. 정량은 future work.
- **σ 등방성 이유**: 침투 Li망이 결정 전역에 *균일* 형성 → 방향편향 없는 거시배치 → E 어느 방향이든 그 방향 전도. **소자 응용: 결정배향 제어 불필요**.

### 5.8 설계 함의 + trade-off (Sec.IV–V)
- σ(Li₁/₃...Te, 295K)=6.8×10⁻³ S/cm = 액체전해질급. **x↑하면 σ↑이나 융점↓(SI) = σ↔열안정 trade-off**.
- **🔑 설계원리**: "**운반이온 농도를 percolation 문턱(x≥0.2) 위로 올리되 열안정 한도 내에서**" → 고전도+화학안정 동시. Coulomb 지배라 **고엔트로피 등 다른 이온결정계로 확장 가능**.

## 6. 메커니즘 종합 (논문의 논증 사슬)
1. **σ(Eq.4) ≫ σ_NE(2 orders)** → 전도 = 단순확산 아님 = cooperative.
2. **σ급등 onset = Lc급등 onset = x≈0.2** → σ↔침투 상관.
3. **Fig.3 클러스터가 x≈0.2서 percolate** + **FCC pc≈0.2 일치** → onset = site-percolation 문턱.
4. **Fig.4 침투클러스터 이온만 mobile** → 전도 = 침투망 전담.
5. **Fig.2 궤적 = knock-on 연쇄(δ=0.34, 2–7 chain), 격자 유지, E유도** → 침투망 위 cooperative knock-on이 운반 메커니즘.
6. **σ 등방(Fig.1) + Na/Ag도 pc=0.2(Fig.5)** → 거시 침투구조가 국소환경 압도, pc 보편.
→ **결론: 무질서 치환결정의 장거리 이온전도 = 운반이온 site-percolation으로 형성된 침투망 위의 cooperative knock-on. 임계 = 격자 site-percolation 문턱.**

## 7. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1 | σ(좌)·Lc(우) vs x. σ·Lc 둘 다 **x≈0.2 급등**, E방향 무관, Lc=1@x≥0.25 | **σ급등 = percolation onset**. 우리 dopant_blocking이 운반망 점유율을 pc 아래로 내리면 σ 붕괴 = 같은 그림의 *역방향* |
| 2 | (a–c) 큰변위 Li궤적(겹침=경로) (d) hop vs knock-on 도식 (e) 변위벡터(2–7 cooperative chain) | knock-on = **우리 inter-cage Li jump의 협동판**(li_transport H_R<1 = 협동운동 정량) |
| 3 | x=0.15(고립)/0.20(간헐침투=경계)/0.25(완전침투) 클러스터 스냅샷 | **percolation 문턱의 시각화**. 우리 dual-x(고x=차단↑ vs 저x=망보존)의 직관 그림 |
| 4 | (a) Δξ 시간추이 (b) ⟨Δξ⟩ vs x — **침투클러스터 이온만 mobile** | "mobile = 침투망 소속" → 우리 migration_volume_fraction(침투 저장벽 부피)이 mobile carrier 결정 |
| 5 | σ vs x for Ag/Na — pc=0.2 동일, σ ~1 order↓ | **pc는 보편, 절대 σ는 ion-size 의존** → 우리 LPSCl엔 pc *값* 직접이식 금지, *개념*만 |

## 8. Post-processing ★
- **무엇**: (1) **cluster analysis**(nearest-neighbor cation 점유 Li → connected component, 최대클러스터 Lc·percolation 판정), (2) **percolation 임계 비교**(FCC site pc≈0.2, Stauffer-Aharony), (3) **cooperative event 검출**(δ=0.34 cutoff로 knock-on chain 길이), (4) **σ(Green-Kubo류 current)** vs **σ_NE(D 기반)** 격차.
- **도구**: 자체 MD + 자체 후처리(특정 패키지 명시 없음). pymatgen/VESTA/LOBSTER 안 씀(=DFT 도구 무관).
- **수치화/플롯**: σ·Lc·⟨Δξ⟩ vs x 곡선, 클러스터 3D 스냅샷(색=크기순), 궤적/변위벡터 3D, cooperative chain 카운트.
- 우리 적용: **"운반이온 자리망의 connected-component 분석 + pc 비교"** = 우리도 BVSE 저장벽 자리/migration volume에 *site-percolation 분석*을 붙일 수 있는 방법론 힌트(현재 우리는 fraction proxy만, 실제 percolation 판정은 미실시).

## 9. 우리 DFT 대비 (comp1/modelc) → `../our_dft_baseline.md`
> ⚠ **이 논문은 우리 물성축(σ·Ea·ESW·gap·elastic 절대값)과 *직접 대조 불가*** — 모델계·단위·결합 전부 다름. 아래는 *개념/임계 프레임* 대응만. **수치 "일치/불일치" 칸 없음 — 의도적.**

| 우리 양 | 이 논문의 대응 개념 | 관계 (framework only, NOT numeric match) |
|---|---|---|
| tier2 `dopant_blocking_fraction` (dopant가 Li 자리/경로를 차지하는 비율) | **운반망에서 자리를 *제거*하는 site dilution** | dopant blocking↑ = 운반 site 점유율 p↓. **p<pc면 σ 붕괴** 예측 → 우리 stability↔mobility trade-off의 *임계* 해석 |
| tier2 `migration_volume_fraction` (BVSE 병목 부피분율) | **침투하는 *저장벽 부피*(low-barrier percolating volume)** | Sec.IV: 실재계는 "저장벽 영역이 침투할 때 고전도". migration_volume = 그 침투부피의 우리 proxy |
| Nd σ300 0.52× / D 0.62× drop | **운반망 점유↓ → mobile carrier↓(prefactor/connectivity)** | li_transport: Nd drop = **D0 prefactor·n_Li(connectivity) 지배, Ea 불변(0.227≈0.224)**. = 이 논문 "σ는 connectivity가 지배, 국소 hop장벽 아님" 과 *정확히 같은 방향* (단 우리는 pc 미달까진 아님 — 아래 §10) |
| dual-x (Sc2O3 blocking 0.75@x0.25 → 0.25@x0.0625) | **저치환=p>pc(망보존) vs 과치환=p<pc(망차단)** | 저x서 blocking↓ = 운반망 손상 적음 = pc 위 유지; 고x서 blocking↑ = pc 아래로 밀 위험. **dual-x의 percolation 해석** |
| anion disorder(S²⁻/Cl⁻ 4a/4d) → "disorder→σ↑" | **무질서가 *침투경로를 연다*(open percolating paths)** | 부분적 일치: 본 논문은 *운반이온 자리* percolation; 우리 4a/4d disorder는 *anion sublattice* 무질서가 Li 경로를 등가화/개방. **다른 부격자지만 "disorder가 percolating path를 만든다"는 같은 정신** |
| H_R<1 (Haven, 협동운동) | **cooperative knock-on** (σ≫σ_NE) | li_transport.json "H_R≈0.3–0.7, concerted" = 이 논문 knock-on의 우리계 정량 흔적 |

## 10. 적용 인사이트 (우리 연구에 어떻게)
1. **우리 cascade = literal "random substitutional crystal"** → 이 논문이 *바로 그 계*의 전도이론. deck에서 우리 dopant-blocking 결과를 **"site-percolation 운반망에서 자리를 빼는 행위"** 로 프레이밍하면 *교과서적 이론 백본*이 생긴다(Stauffer-Aharony percolation).
2. **stability↔mobility trade-off에 *임계* 언어 부여**: "high-valence dopant가 Li 자리를 막아 σ↓"를 **"운반망 점유율을 pc로 밀어내림 → pc 근처서 σ가 *연속*이 아니라 *급격*히 떨어질 수 있음(percolation transition)"** 으로. → 우리 blocking_fraction이 *선형*이 아니라 *문턱형* 거동을 보일 가능성을 예측·검증 동기.
3. **Nd σ-drop 해석 강화 (sibling 결론과 교차)**: 우리 sibling 분석(li_transport.json)은 Nd drop이 **Ea 불변(0.227≈0.224) + D0 prefactor·connectivity 지배**임을 보였다. 이 논문이 **"σ는 국소 hop장벽이 아니라 망 connectivity가 지배"** 를 독립적으로 증명 → **우리 "prefactor/blocking 차단(Ea 차단 아님)" 해석의 이론적 근거**. *단* 우리 Nd는 아직 σ가 *급붕괴*가 아니라 *0.52×* 점진감소 = **pc 위(망 유지)에서의 점유율 *부분* 감소**로 봐야 정합(완전붕괴 아님).
4. **dual-x = percolation 위/아래 전환의 깨끗한 사례**: Sc2O3 x0.25(blocking 0.75)→x0.0625(blocking 0.25). 저x가 "pc 위 유지(vacancy가 망 보존)", 고x가 "pc로 접근(차단)". Fig.3(0.15/0.20/0.25)의 우리계 대응 후보 → **저치환이 σ를 살리는 이유 = 운반망을 pc 위에 두기 때문**.
5. **방법론 힌트**: 우리도 BVSE 저장벽 자리에 *connected-component/percolation 판정*을 붙이면 `migration_volume_fraction`(현재 부피 proxy)을 **실제 percolation 임계 분석**으로 격상 가능. 현재는 분율만 → 향후 "p>pc?" 직접 판정.

## 11. 인용 가능 문장 (deck/paper용) — *framework 한정*
- "Following Ishikawa et al. (site-percolation in random substitutional crystals), our doping cascade is a *random substitutional crystal*; tier-2 `dopant_blocking_fraction` is the **site-dilution of the Li percolation network**, and `migration_volume_fraction` (BVSE bottleneck volume) is the **percolating low-barrier volume**."
- "The σ-drop on high-valence substitution is consistent with the percolation picture: long-range conduction is controlled by **network connectivity, not the local hop barrier** — matching our AIMD finding that the Nd σ-drop is prefactor/connectivity-limited with **Ea unchanged**."
- "Our dual-x result (Sc₂O₃ blocking 0.75 at x=0.25 → 0.25 at x=0.0625) is naturally read as **keeping the Li network above vs pushing it toward the percolation threshold**."
- ⚠ 금지: "우리 LPSCl pc=0.2", "Nd가 pc 아래로 떨어져 σ 붕괴"(우리 drop은 0.52×=부분, 붕괴 아님), 어떤 환원단위 σ도 우리 mS/cm와 등치.

## 12. 주의/한계 (over-claim 방지) — **이 논문 비판 + 우리 인용 가드레일**
- **모델계가 우리와 다르다**: LiₓPb₁₋₂ₓBiₓTe rock-salt(큰 Te²⁻ anion) vs Li₆PS₅Cl argyrodite(PS₄ 골격+S²⁻/Cl⁻). **pc *값* 0.2를 우리계에 이식 금지** — 저자 스스로 "다른 계는 pc가 site-percolation과 불일치, 국소구조·CSRO가 장벽 지배"(Sec.IV).
- **퍼텐셜이 극단 미니멀**: WCA+Coulomb만. 공유결합성(P–S)·polarizability·진동엔트로피·실제 Li 환경 전부 빠짐 → **정량예측 아님**(저자: DFT/MLIP 확장이 next step). 우리 AIMD(MLIP)가 오히려 *더* 재료충실.
- **단위가 환원단위**: σ 6.8 mS/cm도 σ₀=0.34 S/cm 정규화 산물 — **우리 mS/cm와 같은 척도 아님.**
- **무질서 = 단일 무작위 배열**(SQS/enumerate 아님). 우리 cascade decorate와 처리방식 다름(우리는 다중 cfg·DFT relax).
- **우리 blocking은 화학적, 이 논문 dilution은 기하적**: 우리 dopant는 *전하보상 vacancy·결합변화·BVSE 장벽변화*를 동반(화학); 이 논문은 *자리 점유 제거*(순수 기하). "dopant_blocking = site dilution"은 *비유*이지 동일물리 아님.
- **Nd drop ≠ percolation 붕괴**: 우리 0.52×는 *완만 감소*(망 유지 하 점유율↓). 이 논문의 *급등/급붕괴*(transition)와 등치하면 over-claim. 우리 데이터는 아직 "pc 위에서의 connectivity 점진감소" 단계.
- **인용 태깅 필수**: 항상 `[외부·theory·framework only]`. argyrodite 4축 비교표에 *절대* 안 넣음(개념 행만).

## 13. 기법 용어 미니사전
- **Site percolation**: 격자 자리를 확률 p로 점유 → p가 임계 pc 넘으면 *전역 연결 클러스터*(침투망) 출현. 전도/투과의 문턱.
- **pc (FCC ≈ 0.20)**: FCC 부격자 site-percolation 임계점유율(Stauffer-Aharony 표준값). rock-salt cation 자리 = FCC.
- **Cooperative knock-on**: 한 이온 변위가 이웃을 연쇄로 밀어내는 협동운동(단일이온 hop 대비). σ≫σ_NE의 원인.
- **RSIC (random substitutional ionic crystal)**: 이온종이 자리에 무작위 치환된 이온결정(고엔트로피류). = 우리 cascade의 일반명.
- **σ_NE (Nernst-Einstein)**: σ_NE = n z²e²D/(k_BT), 무상관(uncorrelated) hop 가정. 협동운동이면 실제 σ가 더 큼(H_R<1) — 여기선 반대로 σ≫σ_NE라 cooperative 증명.
- **WCA potential**: Weeks-Chandler-Andersen, LJ의 repulsive-only(배제부피만). attractive 제거.
- **Lc**: 최대 Li 클러스터 길이(박스 정규화). Lc=1 = 침투.
- **knock-on chain (δ=0.34)**: 변위 cutoff δ 이내 협동 이온 연쇄(2–7개 관측).
