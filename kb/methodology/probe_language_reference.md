# Probe 언어 레퍼런스 — 각 계산이 무엇이고, 어떻게 구하고, 논문/figure에 어떻게 쓰는가

> 목적: 발표·논문·Q&A에서 각 probe를 **field 표준 언어**로 정확히 말하고 쓰기 위함.
> 각 항목: ① 무엇(정의) ② 어떻게 계산(workflow) ③ 논문 Methods 문장(영어) ④ Figure caption(영어) ⑤ in-text 표현 ⑥ 우리 값.
> 수치 출처는 `db/literature/argyrodite_dft_littable.csv` 참조.

---

## 1. DOS / PDOS (Density of States) — 전자구조

**① 무엇:** 에너지 구간당 전자 상태의 개수(states/eV). "전자가 어느 에너지에 얼마나 있는가"의 지도. E_F 아래=점유(가전자대 VB), 위=비점유(전도대 CB), 그 사이 빈 구간=band gap. **PDOS**는 이를 원자·궤도별로 분해(어느 원자/궤도가 어느 에너지에 기여하는지).

**② 어떻게 계산 (QE workflow):**
1. **SCF**: 바닥상태 자기일관 계산 → 전하밀도.
2. **NSCF**: 고정 밀도로 **더 조밀한 k-mesh**에서 고유값 계산 (DOS는 k-점이 많아야 매끄러움).
3. **dos.x**: 고유값을 smearing(Gaussian/MV, 예 0.005 eV)으로 broadening → DOS(E).
4. **projwfc.x**: 원자궤도에 투영 → PDOS(원소·궤도별).
5. E_F(또는 VBM) 기준으로 에너지축 정렬.

**③ Methods 문장 (영어):**
> "The electronic density of states (DOS) was evaluated from a non-self-consistent calculation on a denser Γ-centered **k**-mesh using the self-consistent charge density, with Gaussian broadening of 0.005 eV. Orbital-projected DOS (PDOS) was obtained by projecting the Kohn–Sham states onto atomic orbitals."

**④ Figure caption (영어):**
> "**Figure X.** Total and projected density of states (DOS/PDOS) of (a) Li₆PS₅Cl and (b) Li₅.₄PS₄.₄Cl₁.₆. The Fermi level is set to zero (dashed line); the band gap is shaded. Element-projected contributions are shown as filled curves."

**⑤ in-text 표현:**
> "The valence-band maximum (VBM) is dominated by S 3p / Cl 3p character, whereas the conduction-band minimum (CBM) comprises … . The computed band gap of 1.8 eV indicates electronically insulating behavior, consistent with low electronic leakage."

**⑥ 우리 값:** gap 1.76 (LPSCl) / 1.82 eV (LPSCl₁.₆); VBM = S 3p 우세.

---

## 2. Band gap — DOS에서 읽는 값

**① 무엇:** VBM(가전자대 꼭대기)과 CBM(전도대 바닥) 사이 에너지 간격. 전자전도의 1차 척도(클수록 절연성).

**② 계산:** DOS에서 점유/비점유 경계로 읽음(고유값 차 또는 DOS-threshold). ⚠ PBE는 gap을 ~1 eV 과소평가 → 정확값엔 hybrid(HSE06)/mBJ 필요.

**③ 표현:**
> "PBE systematically underestimates the gap; our value is therefore a lower bound, and the **comparison** between compositions (Δgap) is the robust quantity rather than the absolute value."

**⑥ 우리 1.76/1.82 vs 문헌 PBE 2.45, HSE06 3.30 (CSV C1) — method offset ~0.7 eV.**

---

## 3. EOS / BM3 (Equation of State) — V₀, B₀

**① 무엇:** 에너지를 부피의 함수로 본 곡선 E(V). 평형부피 V₀, **체적탄성률 B₀**(균일 압축에 대한 저항), B₀′(압력에 따른 B₀ 변화)를 줌.

**② 계산:** 셀 부피를 여러 배율(예 0.94–1.06)로 스케일 → 각 부피에서 셀 고정·원자 relax → E(V) 점들 → **3차 Birch–Murnaghan EOS** fit → V₀, B₀, B₀′.

**③ Methods 문장:**
> "The equation of state was determined by computing total energies at N scaled cell volumes (atoms relaxed at fixed cell) and fitting to a third-order Birch–Murnaghan EOS, yielding the equilibrium volume V₀, bulk modulus B₀, and its pressure derivative B₀′."

**④ Figure caption:** "Energy–volume curves with third-order Birch–Murnaghan fits (solid lines); extracted B₀ values are indicated."

**⑥ 우리 B₀ 26.23 / 21.71 GPa. (방법 원전: Birch 1947, CSV)**

---

## 4. Elastic constants Cij / VRH / Zener / Pugh — 기계물성

**① 무엇:** **Cij** = 탄성강성 텐서(변형↔응력). 입방정은 C11·C12·C44 독립. 다결정 평균으로 **영률 E**(당기기), **체적탄성률 B**(균일압축), **전단탄성률 G**(비틀기). **Zener A = 2C44/(C11−C12)** = 비등방성(1이면 등방). **Pugh B/G** = 연성(>1.75)/취성.

**② 계산:** 작은 유한변형(±ε)을 가해 응력 계산 → stress–strain 기울기에서 Cij. **relaxed-ion**(변형 하에 내부좌표 재완화) vs **clamped-ion**(원자 고정). 다결정 모듈러스는 **Voigt–Reuss–Hill(VRH) 평균**.

**③ Methods 문장:**
> "Elastic stiffness constants Cij were computed from the stress response to finite strains (±X%); the relaxed-ion tensor was obtained by re-relaxing internal coordinates at each strain. Polycrystalline moduli (E, B, G) were derived by Voigt–Reuss–Hill averaging, and the Zener anisotropy ratio A = 2C44/(C11−C12) was evaluated."

**④ Figure/table:** "Elastic constants Cij and derived VRH moduli (E, B, G), Pugh ratio B/G, and Zener anisotropy A."

**⑥ 우리 E_VRH(relaxed-ion) 22.06 / 27.66 GPa (+25%); 전단 주도(G +30%, C44 +72%); Zener 1.14 → 1.44.**

---

## 5. AIMD / MSD / Arrhenius — 이온전도 (Eₐ, D₀, D, σ)

**① 무엇:** 온도에서 원자 동역학을 직접 시뮬 → Li의 **평균제곱변위(MSD)** → 확산계수 D. 여러 온도의 D를 **Arrhenius식 D = D₀·exp(−Eₐ/k_BT)**로 fit → 활성화에너지 Eₐ(이동 장벽), prefactor D₀(carrier 밀도×시도빈도). σ는 Nernst–Einstein.

**② 계산:** NVT (A)IMD 또는 MLIP-MD를 여러 온도에서 → MSD(t) 장시간 기울기 = 6D → ln D vs 1/T 선형회귀 → Eₐ(기울기), D₀(절편).

**③ Methods 문장:**
> "Li-ion diffusivities were extracted from the long-time slope of the mean-squared displacement (MSD) in molecular-dynamics trajectories at several temperatures. Activation energies Eₐ and prefactors D₀ were obtained from Arrhenius fits, D = D₀ exp(−Eₐ/k_BT)."

**④ Figure caption:** "Arrhenius plot of log D versus 1000/T; lines are linear fits with the extracted Eₐ."

**⑥ 우리 Eₐ 0.253 / 0.224 eV (exp 0.25/0.22 매칭, CSV A2/A4); D(600K) 3.09e-6 / 7.90e-6 cm²/s (×2.5).**

---

## 6. COHP / ICOHP — 결합 세기

**① 무엇:** 두 원자 결합의 에너지별 기여. **COHP(E)**: 음수=결합(bonding), 양수=반결합(antibonding). **−ICOHP**(E_F까지 적분)= **결합 세기 지표**(더 큰 양수 = 더 강한 결합). eV/bond 단위.

**② 계산:** DFT 파동함수를 원자궤도 basis로 재투영(**LOBSTER**) → 원자쌍별 COHP → E_F까지 적분 = ICOHP.

**③ Methods 문장:**
> "Bond strengths were quantified by the crystal orbital Hamilton population (COHP) using LOBSTER. The integrated COHP up to the Fermi level (−ICOHP, eV per bond) was used as a measure of bond strength, where a larger −ICOHP denotes a stronger bond."

**④ Figure:** "−COHP curves for Li–Cl, Li–S, P–S bonds (bonding to the right); −ICOHP values are noted."

**⑥ 우리 −ICOHP Li–Cl 1.86 / 2.10 (+13%); P–S 거의 불변.**

---

## 7. ELF (Electron Localization Function) — 결합 성격 시각화

**① 무엇:** 전자 국재화 정도(0~1). **1≈완전 국재(공유결합·lone pair), 0.5≈자유전자, 낮음≈이온결합**(전자를 양도). 결합의 공유/이온 성격을 그림으로.

**② 계산:** 전하밀도+kinetic-energy density에서 ELF 계산(pp.x) → 등가면/단면 plot.

**③ Methods 문장:**
> "The electron localization function (ELF) was computed to visualize bonding character (ELF → 1: localized, covalent or lone-pair; → 0: delocalized/ionic)."

**④ Figure caption:** "ELF iso-surfaces/slices. P–S bridges show ELF ≈ 0.95 (covalent backbone); Li basins < 0.1 (Li⁺ has donated its electron — ionic)."

**⑥ 우리 P–S 0.946/0.944; Li basin <0.1 양쪽.**

---

## 8. BVSE (Bond-Valence Site Energy) — Li 경로 스크리닝

**① 무엇:** Li⁺가 격자 내 각 위치에서 갖는 (경험적) 근사 에너지 지형 → 이동 경로·병목 추정. **빠른 스크리닝용**(DFT 아님).

**② 계산:** bond-valence 모델로 3D 격자에 Li 시험전하 site-energy map → 등에너지면/percolation 분석.

**③ 표현 + ⚠주의:**
> "Bond-valence site-energy (BVSE) maps were used to screen Li-ion migration pathways and bottlenecks. BVSE is an empirical, computationally inexpensive approximation; quantitative barriers require DFT-NEB."

**⑥ 우리 BVSE bimodal: LPSCl 단봉 vs LPSCl₁.₆ 39.8/60.2% 분리 (slide17).**

---

## 9. Bader charge — 원자별 전하

**① 무엇:** 전하밀도를 "Bader 분지"(밀도 최소가 경계)로 나눠 각 원자에 귀속된 전자수 → **실제 이온성**(형식전하 대비). Li⁺가 +1에 가까우면 거의 완전 이온.

**② 계산:** 전하밀도(cube; QE pp.x plot_num=0 valence 또는 21 all-electron) → Bader 분해(Henkelman bader) → 원자별 전하(ACF.dat).

**③ Methods 문장:**
> "Atomic charges were obtained from a Bader analysis of the (all-electron) charge density (Henkelman algorithm)."

**④ 표현:** "Bader charges (Li +0.87, P +1.3, S −1.x, Cl −0.7) confirm the predominantly ionic Li and the anionic framework."

**⑥ (계산 중 — Nd 도핑 V0) + 비교: Torii Li +0.87 (CSV 7).**

---

## 10. Voronoi 부피 분석 — 무질서 지표

**① 무엇:** 각 원자 주변 Voronoi 다면체의 부피 = 국소 자유부피. **부피의 표준편차** = 국소환경 불균일도(=무질서) 정량.

**② 계산:** relaxed 구조에서 PBC 고려해 각 원자의 Voronoi cell 부피 → 원소별 평균·표준편차.

**③ Methods 문장:**
> "Local free volume was characterized by Voronoi tessellation of the relaxed structures; the standard deviation of per-atom Voronoi volumes quantifies the degree of local structural disorder."

**④ Figure/table:** "Per-species Voronoi-volume standard deviations (Å³)."

**⑥ 우리 Li std ×5.5 (0.21→1.15); S −40% (3.41→2.05); P 거의 0.**

---

## 부록: figure set 구성 관례 (학회/논문)

- **DOS/PDOS**: 보통 좌(stoichiometric)·우(doped/Cl-rich) 2-panel, E−E_F 축, gap 음영, 원소별 채움곡선 + total 검정선. 핵심 1줄 caption.
- **Arrhenius**: log D vs 1000/T, 점=데이터·선=fit, Eₐ를 그림 안에 표기.
- **EOS**: E–V 점 + BM3 곡선, B₀ 표기.
- **ELF/Bader/spin density**: VESTA 등가면/단면, 동일 isovalue·시점으로 좌우 비교, color bar 명시.
- **공통 원칙**: ① 같은 축·scale로 두 시스템 나란히 ② E_F=0 정렬 ③ caption에 "무엇을·어떤 조건으로" 한 줄 ④ 본문은 "VBM character / 정량 차이 / 메커니즘" 순.
