# Iodide-substituted halide-rich lithium argyrodite solid electrolytes with improved performance for all-solid-state batteries — Rao et al. (J. Mater. Chem. C 2025)

> slug `rao2025_iodide_argyrodite` · DOI `10.1039/d5tc00529a` · type `DFT + AIMD (계산 전용, 실험 없음)` · PDF `82ea256b/dc0452f3-19._Iodideeries_.pdf` (= INDEX PDF #13 `fdf6b91a (d5tc00529a)`, ⬜→✅) · digested `2026-06-26` · status ✅
> **저자**: Adwitiya Rao, Jacob Rempel, Ming Jiang, Parvin Adeli, Chae-Ho Yim, Mohamed Houache, Yaser Abu-Lebdeh, **Chandra Veer Singh** (교신) · J. Mater. Chem. C, 2025, **13**, 10733–10739
> **소속**: Univ. of Toronto (MSE + Mech. Eng., Singh group) + Anhui Univ. (Hefei) + Univ. of Waterloo + **NRC Canada** (Abu-Lebdeh). **외부 그룹 (≠ 우리 한양/Jong-Won Lee/Y.M.Lee/Cho/Cha/Kang)**

---

## 0. 이 digest를 읽는 법 (그리고 stray/dup 검증)
**검증 통과 — 중복 아님**: 파일명 "19._Iodide…eries"는 잘렸지만 1쪽 정독 결과 **정확히 on-topic**: argyrodite 황화물 SE에 **요오드(I)를 Cl-rich 모체에 치환한 Cl–I 혼합 할라이드** 계산 연구. DOI `d5tc00529a`는 **INDEX 보유 PDF #13(`fdf6b91a`, ⬜ 미digest)과 동일** → 이 digest가 그 ⬜를 ✅로 전환(재업로드 upload-id만 다름). **기존 digest 어느 것과도 다름** — 우리 litdb의 다른 Br/I 언급(Li2025 CuBr₂=Br 도핑·exp / INDEX exp#13 "I-rich mechanical alloying" RSC 2026=별개 논문 / INDEX DFT#11 Physica B 2023 Li₆PS₅I optical)과 모두 별개 논문.

이 논문은 **"잘 연구된 Cl–Br 혼합 할라이드-rich argyrodite 대신, *덜 탐구된* Cl–I 혼합을 쓰면 어떻게 되나? Cl–Br과 정면 비교하면?"** 를 *순수 계산*(DFT + AIMD, 실험 0)으로 푼다. 핵심 결론 3개:
1. **상안정성(phase stability)**: I 첨가가 E_hull을 *낮춰* Cl–I가 Cl–Br보다 **열역학적으로 더 안정** (가장 안정 = Li₅.₅PS₄.₅ClI₀.₅, E_hull 18 meV/atom). 이유는 역설적 — Li–I 결합이 Li–Cl·Li–Br보다 *약한데도*(formation energy LiCl −2.03 > LiBr −1.83 > LiI −1.39 eV/atom) **저에너지 분해상(LiX) + 큰 I⁻의 음이온 정전반발 완화**가 안정화.
2. **전극 호환성(electrode compatibility)**: 계면 반응에너지 ΔE_D가 모든 cathode(LiCoO₂/LiFePO₄/S)에서 **I-치환이 약간 더 우호적** — LiI(I₂)의 낮은 formation energy 덕에 분해산물 에너지가 낮음. 특히 **S 양극과는 Cl–I argyrodite가 최적**(어떤 비호환 반응도 없음).
3. **이온전도**: **Cl–I와 Cl–Br은 동일 X/Cl 비율이면 σ가 거의 같다**(둘 다 total halogen 1.5서 ~10 mS/cm). I/Cl 비율 최적 = **0.75:0.75 → σ=23.5 mS/cm**(Li₅.₅PS₄.₅Cl₀.₇₅I₀.₇₅), 이는 **Li Voronoi 다면체 부피 최대 = 가장 넓은 이동 채널** 때문. 단 I↑ 더 넣으면(>0.75) 5-배위 다면체가 4-배위로 회귀하며 σ 다시 감소.

> ⚠ **이 논문은 실험이 전혀 없다** — σ·E_hull·ΔE_D·gap 전부 DFT/AIMD 계산값. 전압(V), 계면저항(Ω), capacity(mAh/g) 같은 **셀 측정값은 0**. (우리 비교 시 "실험 EIS vs 우리 AIMD"가 아니라 "**그들 AIMD vs 우리 AIMD**"라 오히려 직접적.)
> ⚠ **명명**: 일반식 = **Li₆₋ₓPS₅₋ₓCl₁.₅₋ₓIₓ**(0<x<0.5, total halogen ≤1.5) 및 **Li₅.₅PS₄.₅Cl₁.₅₋ₓIₓ**(total halogen 고정 1.5, I/Cl 비율 스캔, x=0–1.5). 핵심 조성: **Li₅.₅PS₄.₅ClI₀.₅**(E_hull 최저)·**Li₅.₅PS₄.₅Cl₀.₇₅I₀.₇₅**(σ 최대).

## 1. 한 줄 요약
Cl-rich argyrodite에 **I를 치환(Cl→I, 4a 자리)** 하면 Cl–Br 대비 **상안정성↑(E_hull↓, LiI 저에너지 분해상)·전극 호환성↑(LiI/I₂ 낮은 형성E)** 가 생기고, **이온전도는 Cl–Br과 사실상 동급**(같은 X/Cl 비율이면)이며 **I/Cl=0.75:0.75서 σ=23.5 mS/cm**(Li Voronoi 부피 최대=넓은 채널)로 정점을 찍지만, **밴드갭은 Cl–Br보다 *좁아*(2.19 vs 2.32 eV, 둘 다 PBE 과소)** — I의 큰 polarizable p-band가 VBM을 올리기 때문. 즉 **I의 이로움 = 상안정·계면·전도 채널이지, 전자절연이나 산화창이 아니다.**

## 2. 메타 / 동기
| 항목 | 내용 |
|---|---|
| 비교축 | **Cl–I vs Cl–Br** 혼합 할라이드-rich argyrodite (같은 halide 총량·비율서 head-to-head) |
| 일반식 | **Li₆₋ₓPS₅₋ₓCl₁.₅₋ₓIₓ** + total-halogen-고정 **Li₅.₅PS₄.₅Cl₁.₅₋ₓIₓ** |
| 핵심 조성 | Li₅.₅PS₄.₅ClI₀.₅ (E_hull 최저 18 meV), Li₅.₅PS₄.₅Cl₀.₇₅I₀.₇₅ (σ 최대 23.5 mS/cm) |
| 양극(계면 검증) | LiCoO₂·Li₀.₅CoO₂·LiFePO₄·FePO₄·S·Li₂S (lithiated/delithiated 모두) |
| 질문 | 잘 연구된 Cl–Br 대신 **덜 탐구된 Cl–I**가 (a) 상안정성, (b) 전극 호환성, (c) σ 에서 어떤가 |
| 동기 | 단일 I 치환(Li₆PS₅I σ 0.31 mS/cm로 *나쁨*, LiX 2차상)·순수 결정상 합성난 → **Cl-rich에 소량 I**가 현실적. 선행 Cl–Br(Li₅.₅PS₄.₃ClBr₀.₇ 24 mS/cm)·Cl–I 실험 제한적 |
| 선행 | Yu(Li₅.₅PS₄.₅Br₁.₅ 4.35 mS/cm)·Zhang(Li₅.₅PS₄.₅I₁.₅ 0.31 mS/cm)·Adeli(Li₆PS₅Cl 2.5/Li₅.₇₅PS₄.₇₅Cl₁.₂₅ 4.2 mS/cm)·Li et al.(Li₅.₅PS₄.₅Cl₁.₅₋ₓBrₓ chemical space) |

## 3. 핵심 물성 (수치 총정리) — **전부 계산값**
| 물성 | 값 | 조건 | 출처/비고 |
|---|---|---|---|
| **σ (RT, AIMD 외삽)** Li₆PS₅Cl | **1.33 mS/cm** | 300 K, Arrhenius 외삽 | Fig 3a,b (총 halogen 1.0) |
| σ Li₅.₇₅PS₄.₇₅Cl₁.₂₅ | **4.69 mS/cm** | 300 K | Fig 3 (halogen 1.25) |
| σ **Li₅.₅PS₄.₅Cl₁.₅** | **18.86 mS/cm** | 300 K | Fig 3 (halogen 1.5, 순수 Cl 기준) |
| σ Li₅.₅PS₄.₅ClBr₀.₅ | **~10 mS/cm 대** | 300 K | Fig 3a (Cl–Br) |
| σ Li₅.₅PS₄.₅ClI₀.₅ | **~10 mS/cm 대** (ClBr₀.₅와 동급) | 300 K | Fig 3a — **Cl–I ≈ Cl–Br (같은 비율)** |
| σ **Li₅.₅PS₄.₅Cl₀.₇₅I₀.₇₅** | **23.5 mS/cm** ← **최대** | 300 K | Fig 4a (I/Cl=0.75:0.75, 등량) |
| σ Li₅.₅PS₄.₅I₁.₅ (I만, total 1.5) | **4.3 mS/cm** | 300 K | Fig 4g — I 과다서 σ↓ (5→4배위 회귀) |
| σ Li₅.₄PS₄.₄Cl₁.₄I₀.₂ (혼합 검증) | **15.79 mS/cm** (계산) ↔ 실험 17 (Li et al.) | 300 K | 본문 — AIMD가 실험 잘 재현 |
| **Ea (활성화에너지)** | **최소 0.18 eV @ 등량 I/Cl** | Arrhenius fit (600–1000 K) | Fig 4c — I 증가서 Ea↑ 후 등량서 최소 |
| **E_hull** Li₆PS₅Cl (순수 Cl) | **24 meV/atom** (문헌 21) | DFT convex hull, rigorous enumeration | Fig 1b — Cl 기준 |
| E_hull Li₅.₅PS₄.₅Cl₁.₅ | **28 meV/atom** | DFT | Cl 추가가 E_hull *증가*(반발↑) |
| E_hull **Li₅.₅PS₄.₅ClI₀.₅** | **18 meV/atom** ← **최저(가장 안정)** | DFT | **I 첨가가 E_hull 감소** |
| 안정 임계 | **E_hull < 36–40 meV/atom** | (entropic 안정화 한계, ICSD 통계) | 본문 |
| **밴드갭** Li₅.₅PS₄.₅ClBr₀.₅ | **2.19 eV** (PBE/GGA) | DFT band structure | Fig 1c — **Cl–Br** |
| 밴드갭 **Li₅.₅PS₄.₅ClI₀.₅** | **2.32 eV** (PBE/GGA) | DFT band structure | Fig 1d — **Cl–I**, 본문 "larger bandgap is desirable" |
| **Bader 전하** Q_Cl (Li₅.₅PS₄.₅Cl₁.₅) | **−0.898 \|e\|** (−0.0232 \|e\|/Å³) | Bader, total halogen 1.5 | Table 1 |
| Q_Cl / Q_Br (ClBr₀.₅) | −0.897 / **−0.889 \|e\|** | Bader | Table 1 |
| Q_Cl / **Q_I** (ClI₀.₅) | −0.897 / **−0.857 \|e\|** (−0.0163 \|e\|/Å³) ← **최저 전하밀도** | Bader | Table 1 — **I가 전하밀도 가장 낮음 = 정전반발 가장 작음** |
| **Li Voronoi 다면체 부피** (등량 Cl–I) | **9.39 Å³** ← 최대 | Voronoi, 600 K | Fig 4b — I/Cl 등량서 채널 최대 |
| 자리 선호 (site preference) Br | 4a > 4d, **ΔE 0.14 eV/atom** | DFT enumeration | 본문 — Br은 4a 약선호 |
| 자리 선호 **I** | 4a > 4d, **ΔE 0.35 eV/atom** ← 더 강한 4a 선호 | DFT enumeration | 본문 — **I는 큰 이온반경 때문에 4a 강선호** |
| formation energy LiX (MP) | LiCl **−2.03** > LiBr **−1.83** > LiI **−1.39** eV/atom | Materials Project | 본문 — Li–I 결합이 가장 약함 |

### LiX(분해상) 정보 — interphase 맥락
| 상 | 이 논문 언급 | 우리 sei_products.json gap (MP) | 역할 |
|---|---|---|---|
| LiCl | E_f −2.03 eV/atom (가장 안정) | **6.65** eV (insulator) | 분해/계면 inert 산물 |
| LiBr | E_f −1.83 eV/atom | (우리 db 없음; [Li25] DFT 5.07) | 분해상 |
| **LiI** | E_f −1.39 eV/atom (가장 *덜* 안정) + **LiFePO₄와 LiI / FePO₄와 I₂ 형성**(둘 다 낮은 형성E) → 계면 우호 | **(우리 db 없음)** — 문헌 광학 gap **~6.0 eV** (LiI rock-salt 절연체, NaCl형) | I-bearing argyrodite의 계면 분해산물 |
> ⚠ **이 논문은 LiI의 밴드갭을 직접 계산하지 않음** — LiI를 *낮은 형성에너지의 계면 우호 산물*로만 다룸. LiI gap ~6.0 eV는 *문헌 일반값*(우리가 맥락 보강용으로 명시; 논문 수치 아님 → "n/a in paper"). 즉 LiI도 wide-gap 절연 패밀리(LiCl 6.65/LiBr ~5–6/LiI ~6)에 들어가나 **이 논문이 그 절연성을 주장하진 않음**(I의 셀링포인트는 상안정·계면, 전자절연 아님).

## 4. DFT/계산 방법 ★
- **code / version**: **VASP** (Vienna Ab Initio Simulation Package)
- **functional**: **PBE (GGA)** — vdW(D3) **명시 없음**(미사용 추정)
- **pseudo / PAW**: **PAW(projector augmented-wave)**
- **k-points**: 구조최적화 **Monkhorst–Pack 4×4×4**; **AIMD = single Γ-point**
- **ecut**: **520 eV** (energy cutoff)
- **supercell / nat**: **1×1×1 argyrodite**(격자 ~10 Å), "moderate system size for AIMD". (Li₆PS₅Cl 단위포 = 52 atom 급)
- **DFT+U**: **없음** (TM-free 황화물 — U 불필요)
- **AIMD**: **NVT 앙상블**, **single Γ-point**, **시간스텝 2 fs**, **총 110 ps**(첫 10 ps 평형화 후 100 ps로 MSD), **온도 600/700/800/900/1000 K**(100 K 간격 5점) → Arrhenius로 300 K 외삽. D = MSD/(2NdΔt) (eqn 1), σ = Nq²D/(VkT) Nernst–Einstein (eqn 2)
- **MLIP**: 없음 (순수 AIMD)
- **무질서 처리 ★**: **rigorous enumeration (pymatgen)** — Li는 48h 자리 점유율 0.5를 enumeration+Coulomb(Ewald) 에너지로 iterative 제거; **할라이드 치환은 4d 자리에서만**(4a/4d S²⁻/Cl⁻ antisite disorder는 *의도적으로 회피* "to keep computational costs reasonable, 4a/4d antisite disorder between Cl⁻ and S²⁻ have been avoided"); 최소에너지 구조를 DFT로 최적화 후 AIMD. **단일배열 decorate(SQS 아님)** — Li et al. 무질서 entropy 논의는 본 연구 범위 밖이라 명시.
- **특이사항**: ① 4a/4d disorder 회피 = **단순화**(저자 자인); 실험 Cl은 4a/4c 점유라 본 연구는 4a만 고려한 ICSD 기준. ② σ는 **고온 AIMD(600–1000 K) Arrhenius 외삽** — 본문 자인 "high-T 외삽이 변동 유발 가능". ③ 계면 = pseudo-binary grand-potential phase diagram(ΔE_D, eqn 3, pymatgen·MP 에너지).

> **우리 대비**: code(VASP)·functional(PBE)·PAW·AIMD-MSD→Arrhenius·grand-potential 계면 ΔE = **우리 파이프라인과 거의 동일 노선**. 차이: (a) **우리는 무질서 ensemble(disorder_ensemble)·MLIP(UMA) surrogate**도 쓰는데 이들은 단일 enumerate-DFT-AIMD; (b) **k**: 우리 comp1 k444 / modelc k663 정적, AIMD는 양쪽 Γ급 → 정합; (c) **ecut 520 = 우리와 동급**; (d) 둘 다 **4a/4d disorder 단순화**(우리도 modelc 단일배열, SQS 아님 — Liu2022·우리와 같은 철학).

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1a** | Li₆PS₅Cl 기준구조(ICSD, 48h 점유 0.5 조정) 모식 | 우리 comp1 구조와 동일 출발점 |
| **1b** | 모든 할라이드 치환 조성의 **E_hull + formation energy** 막대(Cl₁.₅/ClBr₀.₅/Cl₁.₀/Cl/ClI₀.₅/I₀.₅) | **I가 E_hull↓(18 meV 최저)·Cl 추가는 E_hull↑** — 상안정성 핵심 그림 |
| **1c** | **Li₅.₅PS₄.₅ClBr₀.₅ 밴드구조, gap=2.19 eV** | Cl–Br gap 기준(PBE) |
| **1d** | **Li₅.₅PS₄.₅ClI₀.₅ 밴드구조, gap=2.32 eV** | **Cl–I gap이 Cl–Br보다 큼**(PBE) — 단 둘 다 과소·"wide-gap insulator"만 |
| **2** | cathode(Li₂S/S/FePO₄/LiFePO₄/Li₀.₅CoO₂/LiCoO₂) × argyrodite **계면 반응E 히트맵** | **계면 호환성 = I 우호(LiI/I₂ 저형성E); LiCoO₂ 반응E 높음(부적합)·S 양극 우수** |
| **3a** | **σ vs total halogen 분율**(Cl/Cl–Br/Cl–I 색분류) | **같은 비율이면 Cl–I≈Cl–Br σ** — head-to-head 동급 |
| **3b** | **log D vs 1000/T**(Arrhenius, 600–1000 K, 조성별) | AIMD 외삽 방식 = 우리와 동일 |
| **3c** | Li₅.₅PS₄.₅ClBr₀.₅ Li 주위 **음이온 RDF**(Li–S/Li–Cl/Li–Br) | Br 주위 Li 강한 clustering(Li–Br 상호작용↑) |
| **3d** | Li₅.₅PS₄.₅ClI₀.₅ Li 주위 **음이온 RDF**(Li–S/Li–Cl/Li–I) | **I 주위 Li clustering 큼**(I↑면 확산 둔화 요인) — 단 등량서 채널 부피로 상쇄 |
| **4a** | **σ vs I/Cl 비율**(Li₅.₅PS₄.₅Cl₁.₅₋ₓIₓ) — **0.75:0.75서 23.5 mS/cm 정점** | **I/Cl 등량이 σ 최적**(화산형) |
| **4b** | **평균 Li Voronoi 다면체 부피 vs I/Cl** — 등량서 9.39 Å³ 최대 | **σ↑ = 채널 부피↑** 직접 상관(우리 cage/migration-volume과 같은 물리) |
| **4c** | log D vs 1000/T (I/Cl별) + **Ea 최소 0.18 eV @ 등량** | I 증가→Ea↑ 후 등량 최소 |
| **4d** | **확대된 Li 다면체 모식**(Li–S/S/Cl/I 배위) | 5-배위 다면체 = 큰 부피=빠른 전도 |
| **4e,f,g** | Li 다면체 부피 **분포 히스토그램**(Cl₁.₅ / Cl₀.₇₅I₀.₇₅ / I₁.₅) | **5-배위 다면체(빨간 점선)**가 σ에 가장 기여; I 과다(I₁.₅)서 4-배위 회귀 → 부피↓→σ↓ |
> Fig S1 = Li₅.₅PS₄.₅Cl₁.₅ 밴드구조(ESI); S2 = 다른 조성 다면체 분포(ESI); Tables S2–S4 = 계면 반응E 상세(ESI).

## 6. Post-processing ★
- **무엇**: ① **convex hull / E_hull + formation energy** (상안정성) · ② **band structure**(gap·전자절연) · ③ **Bader charge**(음이온 전하·전하밀도 → 정전반발) · ④ **grand-potential 계면 반응에너지 ΔE_D**(eqn 3, electrode 호환성) · ⑤ **AIMD MSD→D→σ(Nernst–Einstein)+Arrhenius Ea** · ⑥ **Voronoi 다면체 부피 분석**(이동 채널·배위수) · ⑦ **음이온 RDF**(Li clustering).
- **도구**: **pymatgen**(enumeration·E_hull·grand-potential·ΔE_D·MP 에너지) · **VASP**(DFT·AIMD) · Voronoi(Li 다면체) · MP(common cathode 에너지).
- **수치화·플롯·기록 방식**: σ=Arrhenius 300 K 외삽(mS/cm); E_hull/E_f=meV/atom; gap=eV; Bader=\|e\| 및 \|e\|/Å³; Voronoi=Å³ + 배위수 분포 히스토그램; ΔE_D=히트맵(meV/atom); RDF=average number of Li atoms vs distance.

> **우리 적용**: **Voronoi 다면체 부피 vs σ** 상관(Fig 4a,b)이 우리 cascade `migration_volume_fraction`(BVSE bottleneck 부피)·cage descriptor와 *같은 물리*. **5-배위 vs 4-배위 다면체 분포 → σ** 논리가 우리 inter-cage 서사의 정량 보강. **Bader 전하밀도(Q/Å³)로 음이온 정전반발 → 안정성**은 우리 ICOHP/oxophilicity와 다른 도구로 같은 결론.

## 7. 우리 DFT 대비 (comp1 / modelc) → `../our_dft_baseline.md`
| 항목 | 이 논문 (Cl–I / Cl–Br) | 우리 (comp1 / modelc) | 일치 / 차이 + 이유 |
|---|---|---|---|
| **σ(AIMD) Cl-rich 빠름** | Li₆PS₅Cl 1.33 → Li₅.₅PS₄.₅Cl₁.₅ **18.86 mS/cm**(300 K); 등량 Cl–I/Cl–Br ~10대; **Cl₀.₇₅I₀.₇₅ 23.5** | D(600K) 3.09→**7.90e-6** cm²/s, Ea 0.253→**0.224** | **✓✓ trend 일치** (halide↑·무질서↑→σ↑). **둘 다 AIMD-Arrhenius**라 방법 직접 비교 가능. 단 그들 절대 σ(18.86)는 우리 RT 외삽과 같은 *고온 외삽 과대* 주의(우리 UMA σ 3–5× 과대와 같은 결) |
| **Ea↓ (halide-rich/등량)** | 최소 **0.18 eV** @ I/Cl 등량 | comp1 0.253 → modelc **0.224 eV** | **✓ 같은 방향**(halide-rich·무질서서 Ea↓). 그들 0.18 < 우리 0.224 = 조성·자리·등량 I/Cl 차이 |
| **이온전도 기전 = 넓은 이동 채널** | Li **Voronoi 다면체 부피 9.39 Å³** 최대 = 넓은 채널 = 낮은 Ea | 우리 inter-cage·BVSE `migration_volume_fraction`·cage descriptor | **✓✓ 동일 물리** — "채널 부피↑→σ↑"는 우리 cascade 중심 멘탈모델. 그들 5-배위 다면체 = 우리 percolating bottleneck 부피 |
| **밴드갭 (PBE)** | Cl–Br **2.19** / Cl–I **2.32 eV** | comp1 **2.066** / modelc **2.098** (PBE) | △ **"wide-gap insulator" 수준만 정렬** — 같은 PBE 과소 영역. **🔑 우리계와 가장 직접 비교 가능**(둘 다 PBE·argyrodite). 그들 2.19/2.32 > 우리 2.07/2.10 = 4a/4d 처리·k·조성차(그들 total halogen 1.5 vs 우리 1.0/1.6). **절대 gap 직접비교 금지**(HSE 보정 전, He19 §) |
| **VBM character / 산화 onset** | 명시 안 함; **I는 큰 polarizable p-band → gap 변화** (VBM↑ 추정) | comp1/modelc VBM = **S 3p**, onset **2.256 V**(LiS4 제외)/2.14(포함) **S²⁻-limited** | **🔑 핵심: I는 산화 onset을 옮기지 *않을* 가능성** — 우리/Banik2022 = onset은 **S²⁻→S⁰가 율속**(halide 무관). 이 논문도 **산화 onset(V)을 전혀 계산/주장 안 함**(상안정 E_hull·계면 ΔE_D만). §8·§10 참조 |
| **상안정성 (E_hull)** | Cl 추가 E_hull↑(28); **I 추가 E_hull↓(18 meV)** = Cl–I가 Cl–Br보다 안정 | 우리 **E_above_hull 미계산**(0K closed hull만) | ✗ **우리 못 봄** → 그들이 채움. **🔑 우리 H목록 "무질서 E_hull metastability" gap을 *I 방향*으로 메우는 외부 DFT**. 단 그들도 4a/4d disorder 회피·single-config E_hull |
| **전극 계면 호환성 ΔE_D** | I-치환이 LiCoO₂/LiFePO₄/S 모두서 약간 우호(LiI/I₂ 저형성E); **S 양극 최적** | 우리 **interface_reactivity / grand-potential ΔE_D**(vs LiCoO₂) | **✓ 같은 방법(pymatgen grand-potential ΔE_D)** — 우리 도구와 동일 알고리즘. 우리는 vs LiCoO₂ comp1/modelc dE≈−0.32(noise), 그들은 *halide 종류*로 ΔE_D 비교. **I=저에너지 LiX 산물로 ΔE_D↓**는 우리가 LiCl 산물 보는 것의 I 버전 |
| **Bader 음이온 전하** | Q_Cl −0.898 / Q_Br −0.889 / **Q_I −0.857 \|e\|**(전하밀도 최저) | comp1 Bader Q_Cl ≈ **−0.914 \|e\|** | **✓ 정합**(우리 Q_Cl −0.914 ≈ 그들 −0.898). **I가 전하밀도 가장 낮음**(−0.0163 \|e\|/Å³) = 큰 이온이라 전하 분산 → 정전반발↓→안정화. 우리 Cl Bader와 같은 줄 |
| **무질서 처리** | enumerate→lowest-Ewald→DFT(단일배열), 4a/4d disorder 회피 | modelc 단일배열(SQS 아님), 4a/4d 단순화 | **✓✓ 동일 철학** (Liu2022·우리와 같은 enumerate 단일배열) |

## 8. 산화/환원 창에서 I의 위치 — **정직한 분석 (over-claim 방지)**
**질문**: I⁻는 Cl⁻보다 *쉽게 산화*된다(I⁻/I₂ 표준전위 낮음·큰 polarizable p-band). 그럼 I-bearing argyrodite는 **산화 onset이 낮아지나?** 우리 2.14 V S²⁻-limited 그림이 무너지나?

**답 — 아니다 (이 논문 + 우리 + Banik2022 종합)**:
1. **이 논문은 산화 onset(V)을 계산하지도, 주장하지도 않는다.** I의 장점은 전부 (a) **E_hull 상안정**, (b) **계면 ΔE_D 호환**(LiI/I₂ 저형성E), (c) **σ 채널**. **전압창(ESW)·산화 onset은 본 논문 스코프 밖.** → "I가 산화창을 좁힌다"를 이 논문으로 인용 **불가**.
2. **우리/Banik2022 = onset은 S²⁻이 pin** — argyrodite 첫 산화는 **S²⁻→S⁰(폴리설파이드)** 가 율속이라 **halide 종류와 무관**하게 onset 동일(우리 comp1=modelc 2.256 V; Banik "substitutions 거의 영향 없음, anion(S) sublattice가 oxidative stability 결정"). I를 넣어도 **첫 산화는 여전히 S²⁻**일 것 → onset 거의 불변 예상.
3. **단 미묘함(정직)**: I⁻/I₂ 산화는 S²⁻/S⁰보다 *더 낮은* 전위서 일어날 *수* 있다 — 만약 I가 충분하면 **I⁻ 산화가 새 limiting reaction**이 되어 onset을 *낮출* 가능성이 이론상 있다(우리 B2O3가 limiting reaction을 2.317 V로 *올린* 것의 반대 방향). **그러나 이 논문은 그 계산을 안 했고**, 소량 I(x≤0.5)면 S²⁻가 여전히 다수라 S-limited 유지가 더 가능성 높음. → **"I가 onset을 낮춘다"는 *가설*로만, 우리 grand-potential로 직접 확인 필요**(향후: I 포함 chemsys ESW). 현재로선 **"I는 conductivity·interphase·phase-stability 레버이지 oxidation-onset 레버라는 증거는 없음"** 이 정직한 진술.
4. **밴드갭은 오히려 I-bearing이 더 큼**(2.32 > 2.19 eV, Cl–I > Cl–Br) — 단 이건 PBE·VBM character 미분석이라 "전자절연 우수"로 못 읽음(gap≠산화창; Banik/우리: VBM은 S 3p가 지배, I p가 VBM 위로 올라오면 *오히려* 산화 쉬워질 수도 → gap 크다고 산화 안정 아님). **gap 절대비교·"I가 절연 우수" 금지.**

> **결론(산화축)**: I의 셀링포인트 = **상안정·계면·전도**. **산화 onset은 (이 논문도 안 다루고) S²⁻-limited라 거의 불변 예상** — "I-rich = 산화 더 안정/불안정"을 이 논문으로 주장하면 틀림. Cl-rich oxidation처럼 **반드시 축 명명**(B① intrinsic onset은 S-pinned·halide 무관 / I 효과는 *다른 축*).

## 9. Cl/Br/I 할라이드-도핑 그림에서 I의 자리 (우리 cascade 맥락) ★
> 우리 anion-site cascade: **O→S(16e)** / **F→Cl(4d)** / **Cl→ (comp1 1.0 → modelc 1.6)** / F–I dual-anion 선례(JPCC 2023, `10.1021/acs.jpcc.3c00962`, Li₆PS₅I). 이제 **I→4a**가 이 그림에 추가됨.

| 할라이드 | 이온반경 (Å) | polarizability(softness) | 선호 자리 | σ 효과 | 산화 onset | 전자절연(LiX gap) |
|---|---|---|---|---|---|---|
| **Cl⁻** | **1.81** | 낮음(hard) | **4a/4d 모두**(S²⁻와 크기 유사→4a swap) | 기준(Cl-rich σ↑·disorder↑) | S-limited(불변) | LiCl **6.65** eV (우리 db) |
| **Br⁻** | **1.96** | 중간 | **4d 우선**(4a strain), 이 논문 site ΔE 0.14 eV/atom | Cl–Br σ↑(등량 Cl/Br=σ 최적, exp 24 mS/cm) | S-limited(불변) | LiBr **5.07** eV ([Li25] DFT) |
| **I⁻** | **~2.20** | **높음(soft, 가장 polarizable)** | **4a 강선호**(이 논문 site ΔE **0.35 eV/atom** = Br보다 큼; "only 4a, not 4d") | **Cl–I ≈ Cl–Br**(등량); I/Cl=0.75:0.75서 **23.5 mS/cm 최대**(채널 부피); I 과다서 σ↓ | **S-limited 예상(불변)** — 이 논문 미계산 | LiI **~6.0 eV**(문헌; 논문 미계산) |

**I의 메커니즘 (이 논문이 보인 것)**:
1. **자리(site)**: I⁻는 **너무 커서(2.20 Å) 4a만 점유**(4d는 S²⁻ 16e와 antisite 시 강왜곡 불리). Br(1.96)이 4a 약선호(0.14)인데 **I(2.20)는 4a 강선호(0.35 eV/atom)**. → 이 논문 자체가 본문에서 명시: "both Br and I atoms preferred 4a sites over 4d... 0.14(Br)/0.35(I) eV/atom... due to the larger ionic radius of Br⁻/I⁻ compared to S²⁻/Cl⁻". (cf. 우리 mechanism note: Cl은 4a swap으로 *표면 노출*·Br은 4d bulk; 이 논문은 4a를 더 본질적 선호로 봄 — **4d disorder 회피 모델**이라 우리 표면-segregation 그림과는 결이 다름, §10 주의.)
2. **polarizability/softness**: I⁻ = 가장 polarizable(soft) → **Bader 전하밀도 가장 낮음**(−0.0163 \|e\|/Å³, Q_I −0.857) → **음이온 정전반발 완화 → E_hull↓(상안정)**. 동시에 I 주위 **Li clustering 큼**(Fig 3d, Li–I 상호작용) → I 과다면 확산 둔화(σ↓).
3. **이동 채널(conductivity)**: I 치환이 격자팽창 → **Li Voronoi 다면체 부피↑(9.39 Å³ @등량)** → 넓은 채널 → Ea↓(0.18 eV)·σ↑(23.5). 단 I/Cl>0.75면 5-배위→4-배위 회귀로 부피↓·σ↓ (화산형).
4. **LiI interphase**: I-bearing argyrodite의 계면 분해산물 = **LiI(LiFePO₄와)·I₂(FePO₄와)** — 둘 다 저형성E → ΔE_D↓(계면 우호). **LiI는 wide-gap 절연체(~6 eV)** 이지만 **이 논문이 그 절연성을 주장하진 않음**(우리 sei halide-gap 시리즈 LiCl 6.65/LiBr 5.07/LiI ~6에 *맥락상* 추가되나, LiI gap은 논문 수치 아님 → "n/a in paper").

**Li2025(Br) 대비 I의 위치**:
- **Li2025 = exp + Br을 Cu와 함께 도핑**(CuBr₂, σ 10.3·gap 1.82→2.41·CCD 1.9·대기안정), Br→4a/4d 무질서로 σ↑ + **wide-gap LiBr(5.07) 절연계면 주장**.
- **Rao2025 = 순수 DFT, I 단독 치환**(Cl–I), σ는 Cl–Br과 동급이나 **I만의 추가 가치 = 상안정 E_hull↓ + 계면 ΔE_D↓**(Br엔 없는 분석). **gap은 I-bearing이 더 큼**(2.32 vs Cl–Br 2.19)이나 절연성 주장 안 함.
- **Cl/Br/I trend 종합**: 이온반경·polarizability **Cl<Br<I**; σ는 **등량 비율이면 셋 다 ~10–24 mS/cm 동급**(halide 종류보다 *총량·비율·무질서·채널부피*가 지배); **산화 onset은 셋 다 S²⁻-limited라 거의 불변**(halide 무관, Banik/우리); 차별화는 **I=상안정+계면(이 논문)·Br=대기안정+절연계면(Li2025 via Cu–S)·Cl=표면 segregation+계면 양호(Zuo/Cha)**.

## 10. 인용 가능 문장 (deck/paper용)
- "Rao et al. (JMCC 2025, DFT+AIMD) show Cl–I argyrodites match Cl–Br in ionic conductivity at equal halide ratios (~10–24 mS/cm) while being *more phase-stable* (E_hull 18 vs 28 meV/atom) — iodide's value is phase stability and electrode compatibility, not conductivity per se."
- "Their AIMD reproduces the same halide-rich σ↑/Ea↓ trend as our comp1→modelc (Ea 0.18 eV at equimolar I/Cl vs our 0.224 eV; both AIMD-Arrhenius), driven by the same physics — enlarged Li Voronoi polyhedron volume (9.39 Å³) = wider migration channels."
- "Iodide is the most polarizable halide (Bader Q_I −0.857 \|e\|, lowest charge density) and prefers the 4a site most strongly (site-preference ΔE 0.35 eV/atom vs Br 0.14) — its softness relaxes anionic electrostatic repulsion, lowering E_hull."
- "Crucially, Rao et al. compute *no* oxidation onset — consistent with Banik 2022 and our grand-potential, the S²⁻ sublattice pins oxidation; iodide is expected to leave the intrinsic onset essentially unchanged, acting on conductivity/interphase/phase-stability instead."

## 11. 주의 / 한계 (over-claim 방지 — **비판적**)
- ⚠ **실험 0** — σ·E_hull·ΔE_D·gap 전부 계산. 셀 V·R_int·capacity 없음. "I가 실제로 성능 좋다"를 이 논문으로 주장 금지(예측만).
- ⚠ **4a/4d antisite disorder 의도적 회피** — 저자 자인 "to keep computational costs reasonable". 실험 Cl/Br/I는 4a/4c 점유·disorder가 σ의 핵심인데(우리 modelc·Liu2022 무질서 61.7%) 이를 단순화 → **σ·E_hull 절대값이 disorder를 과소반영**할 수 있음. 우리 표면-segregation(Cl 4a swap 표면 노출·Br 4d bulk) 그림과 **자리 해석이 다름**(이 논문은 4a를 본질 선호로, disorder 무시).
- ⚠ **σ 고온 AIMD(600–1000 K) 외삽** — 저자 자인 "high-T 외삽이 변동 유발". 절대 σ(18.86 mS/cm for Cl₁.₅)는 일부 실험(9.4–10.8)보다 높음 → 우리 UMA σ 3–5× 과대와 같은 *외삽 과대* 주의. **Ea·비율만 신뢰, 절대 σ는 ±**.
- ⚠ **밴드갭 PBE 절대값 비교 금지** — Cl–Br 2.19 / Cl–I 2.32는 PBE(과소, HSE 보정 전). **gap 크다고 "I 전자절연/산화안정 우수" 금지**(VBM character 미분석; I p-band가 VBM 위로 오면 *오히려* 산화 쉬울 수도). "wide-gap insulator" 수준만.
- ⚠ **LiI 밴드갭은 논문에 없음** — 우리가 맥락상 ~6 eV(문헌)로 보강했으나 **이 논문 수치 아님**(n/a in paper). "Rao가 LiI 절연계면 보였다" = 틀림(LiI는 *저형성E 계면산물*로만 다룸, 절연성 주장 X).
- ⚠ **산화 onset 미계산** — I의 ESW·산화 onset 효과는 이 논문이 *전혀* 안 다룸. "I-rich oxidation 안정/불안정"을 이 논문으로 인용 불가. (우리 가설: S-limited라 불변; 확인은 향후 I-chemsys grand-potential.)
- ⚠ **단일 I 치환(Li₆PS₅I)은 σ 나쁨**(0.31 mS/cm, LiX 2차상) — I는 *소량 Cl-rich 공치환*에서만 유효. Cl-rich LiCl 용해한계(Zuo·우리 modelc Cl1.6 주의)에 더해 **I도 과다면 σ↓(I₁.₅서 4.3) + LiX 2차상**.
- ⚠ **계면 ΔE_D = pseudo-binary grand-potential(0 K)** — 우리 interface_reactivity와 같은 한계(기체상·kinetics·passivation 못 봄). "I가 계면 우호"는 *thermo ΔE_D*만.
- **외부 그룹** (Toronto/Anhui/Waterloo/NRC Canada) — 우리 그룹 아님. **INDEX [우리 그룹] 태그 금지** → **[외부]**.

## 12. 기법 용어 미니사전
- **E_hull (energy above hull)**: convex hull(가장 안정 상조합) 위 에너지. 낮을수록 안정; <36–40 meV/atom면 entropic 안정화로 합성가능(ICSD 통계).
- **grand-potential 계면 반응E (ΔE_D)**: 전해질+양극을 chemical potential 공간서 분해시킬 때 에너지(eqn 3). 음수 클수록 분해(비호환), 0 근처면 호환. = 우리 interface_reactivity 동일 도구.
- **Bader 전하밀도 (\|e\|/Å³)**: Bader 전하를 부피로 나눔. 큰 이온(I)일수록 전하 분산→밀도↓→정전반발↓.
- **Voronoi 다면체 부피**: Li 주위 배위 다면체 부피. 클수록 넓은 이동 채널→낮은 Ea→높은 σ. = 우리 cage/migration-volume descriptor.
- **5-배위 vs 4-배위 다면체**: Li 배위수. **5-배위(큰 부피)가 σ에 가장 기여**; I 과다면 4-배위로 회귀→부피↓→σ↓(화산형).
- **site preference ΔE (eV/atom)**: 할라이드가 4a vs 4d 점유 시 에너지차. 큼=강선호. Br 0.14 / **I 0.35**(I는 커서 4a 강선호).
- **polarizability/softness**: 전자구름이 잘 변형되는 정도. I⁻가 가장 soft(polarizable) → 전하 분산·약결합·격자팽창.
- **Nernst–Einstein σ**: σ=Nq²D/(VkT) (eqn 2). AIMD D를 σ로 환산(상관효과 무시 = Haven 1 가정 → 우리 H_R<1 보정과 다름).
