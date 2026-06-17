# LPSCl (comp1) vs LPSCl1.6 (modelC) — 종합 비교 보고

작성 2026-06-17. 출처: db/properties/{electronic,elastic,li_transport,oxidation_stability,bonds,eos}.json,
kb/results/{lpscl_vs_lpscl16_v3_comparison, lpscl_structural_analysis_v3, paper_figure_plan_v3}.md,
db/literature/argyrodite_computational_littable.csv. (발표용 아닌 전수 보고용. 모든 값 0K DFT 수렴 구조 기준, 명시된 것 제외.)

- **comp1 = LPSCl** = Li₆PS₅Cl (F-43m, 4 f.u., 52원자, V₀ 1016.6 Å³) — 정렬·무공공
- **modelC = LPSCl1.6** = Li₅.₄PS₄.₄Cl₁.₆ (rhombo, 5 f.u., 62원자, V₀ 1216.4 Å³) — Cl-rich·Li공공·4d-Cl anti-site

---

## 한눈에 (마스터 요약)
| 축 | 물성 | comp1 | modelC | Δ/경향 | 방법 |
|---|---|---|---|---|---|
| 전자 | 밴드갭(eigenvalue) | 2.066 eV | 2.099 eV | +0.033 (불변) | DFT QE |
| 전자 | N(E_F) | 0 | 0 | 둘 다 절연체 | DFT |
| 전도 | σ_NE(300K) | 3.35 mS/cm | 13.96 mS/cm | **×4.2 ↑** | UMA-MLIP NE |
| 전도 | Ea | 0.253 eV | 0.224 eV | −11.7% | AIMD(600–1000K) |
| 전도 | D(600K) | 3.09e-6 | 7.90e-6 | ×2.56 | AIMD |
| 기계 | E (relaxed-ion) | 22.06 GPa | 27.66 GPa | **+25.4% ↑** | DFT 응력법 |
| 기계 | G / B | 8.13 / 25.51 | 10.61 / 23.40 | G+30%, B−8% | DFT VRH |
| 기계 | B₀(EOS) | 26.2 GPa | 21.7 GPa | −17% | BM3 |
| 산화 | OCV / ox onset(0Pa) | 1.72 / 2.14 V | 1.72 / 2.14 V | 동일(S-limited) | grand-potential |
| 산화 | constrained ESW(20GPa) | 1.66 V폭 | 3.30 V폭 | **modelc 2× 넓음** | constrained ESW |
| 계면 | vs LiCoO₂ ΔE_rxn | −0.3227 | −0.3308 eV/at | modelc 약간↑반응 | InterfacialReactivity |
| 결합 | ICOHP P–S | −5.944 | −6.000 eV | +0.9% (불변) | LOBSTER |
| 결합 | ICOHP Li–Cl | −1.855 | −2.103 eV | **+13.4%** | LOBSTER |
| 결합 | ICOHP Li–S | −1.592 | −1.717 eV | +7.9% | LOBSTER |
| ELF | P–S bridge | 0.946 | 0.944 | 불변(공유백본) | pp.x ELF |
| ELF | Li basin min | 0.072 | 0.065 | 약간↑이온성 | pp.x ELF |
| Bader | q(Li)/q(S) | +0.874/−1.52 | +0.882/−1.76 | S +15.7% 음전하 | Bader AE |

---

## 축별 상세 (헤드라인 + 표)

### 1) 구조/조성
| | comp1 | modelC | Δ |
|---|---|---|---|
| 식 | Li₆PS₅Cl | Li₅.₄PS₄.₄Cl₁.₆ | −0.6Li,+0.6Cl/−0.6S |
| V/f.u. | 254.2 Å³ | 243.3 Å³ | −4.3% |
| V/atom | 19.55 | 19.62 | +0.4%(골격 보존) |
| Li 공공/f.u. | 0 | 0.6 | +0.6 |
| 4d-Cl anti-site | 0% | 12.5%(1/8) | +12.5pp |
| Li 환경 종류 | 1 | 6 | 정렬→무질서 |
| d(Li–Cl) 4a/4d | 2.607 / — | 2.551 / **2.359** | 4d 초단·균일 |
| Cl 배위수 | 6.0±0 | 5.0±0.5 | 6→5 |
> **핵심: PS₄ 골격 보존, 음이온 sublattice에 disorder(4d anti-site Cl)·Li 공공만 도입.**

### 2) 전자(밴드갭/DOS)
- gap 2.066 vs 2.099 eV (**+1.6%, 사실상 불변**). VBM=S 3p(91/92%), CBM=S/P/Li, **성분 동일**. 둘 다 **N(E_F)=0 clean 절연체.**
- ⚠️ 옛 modelC "defect band"는 **DOS-threshold 아티팩트** → eigenvalue로 보면 clean(2026-06-16 정정). 
- DOS-threshold 갭(1.76/1.82)은 구버전(USPP, ~0.3eV 과소).
> **Cl/공공이 벌크 전자구조를 안 바꿈 — 차이는 구조적이지 전자적이 아님.**

### 3) 이온전도
| | comp1 | modelC | Δ |
|---|---|---|---|
| Ea | 0.253 eV | 0.224 eV | −11.7% |
| D₀ | 4.11e-4 | 5.80e-4 | +41% |
| D(600/800/1000K) | 3.09/10.3/22.0 e-6 | 7.90/20.5/45.5 e-6 | ×2.0–2.6 |
| σ_NE(300K) | 3.35 | 13.96 mS/cm | ×4.2 |
> **이중 메커니즘: Ea↓(disorder가 장벽 낮춤, Schlem/Minafra) + D₀↑(공공·4d-Cl이 경로↑). 둘 다 문헌 정합.** ⚠️절대 σ는 UMA 3–5×과대→**비율(×4.2)·600–1000K 인용**, 300K 외삽은 불확실.

### 4) 산화안정성 (4개 축 — 한 숫자 아님)
1. **내재 onset(0Pa): 무승부** — OCV 1.72, ox 2.14 V (둘 다 S²⁻-limited, Cl 비활성).
2. **기계구속창(20GPa): modelC 승** — Cl 산물(bulky LiCl) 팽창(eps_RXN +0.023) → 구속이 산화 억제 → 창 1.66→**3.30 V**.
3. **계면 사이클(Zuo 2023): modelC 승** — Li 적게 방출(0.7 vs 1.75)·불활성 LiCl 2배 → R_int 성장 33%↓(8.9 vs 13.2).
4. **달력/열 노화(Wu 2026): modelC 패** — 90°C 유지 68%(comp1) vs 48–59% → O-도핑 동기.

### 5) 기계물성 (★vacancy paradox 해결)
| | comp1 | modelC | Δ |
|---|---|---|---|
| C₁₁/C₁₂/C₄₄ | 37.7/20.4/7.98 | 37.0/16.8/**13.68** | C44 +71% |
| E (relaxed-ion) | 22.06 | 27.66 | **+25.4%** |
| G / B | 8.13 / 25.51 | 10.61 / 23.40 | G+30/B−8 |
| ν / Zener A | 0.356/1.14 | 0.303/1.44 | 이방성↑ |
| **clamped-ion E(참고)** | 52.31 | 52.30 | **0%(비물리)** |
> **clamped-ion은 PS₄ 고정이라 둘 다 52(차이 0)=paradox. relaxed-ion이 실험경향 복원(modelC +25%, Deng/Ong 22.1·Torii 27.4 일치).** 기구: 공공+4d-Cl이 soft Li-shear mode를 **미리 jam** → modelC가 더 단단. 운영온도(600K)선 둘 다 비슷(전도 이득에 기계 손해 0).

### 6) 결합 ICOHP
| bond | comp1 | modelC | Δ |
|---|---|---|---|
| P–S | −5.944 | −6.000 | +0.9%(불변) |
| Li–Cl(전체) | −1.855 | −2.103 | +13.4% |
| Li–Cl 4a/4d | −1.855 / — | −2.026 / **−2.836** | 4d 초강결합 |
| Li–S(전체) | −1.592 | −1.717 | +7.9% |
| Li–S(4d 자유S²⁻) | −2.566 | −2.516 | −2%(**불변 anchor**) |
> **모든 이온결합(Li–Cl/Li–S) 강화**(공공직관과 반대). P–S 백본 불변. ICOHP-거리 기울기는 modelC가 2–3× 완만(=soft, 열운동 쉬움 → 빠른 AIMD 설명). Wilkening 이온퍼텐셜이 ICOHP를 r=−1.00로 예측(3법 일치).

### 7) ELF / 8) Bader
- ELF P–S 0.946/0.944(불변 공유백본), Li basin 0.072/0.065(둘 다 강이온, modelC 약간 깊음).
- Bader: q(Li) +0.874/+0.882, q(S) −1.52/**−1.76**(modelC S 더 음전하 → Li–S 강화 주원인), q(Cl) −0.93/−0.92(불변), PS₄ 합 ≈ −2.8/−2.6(formal −3 보존). Li 이온성 = Cl 이웃당 +0.011 e 선형.
> **ELF·ICOHP·Bader·결합길이 4개 독립 probe 전부 일치: PS₄ 백본 불변 + modelC 이온결합 강화.**

---

## 그림/데이터 (표현용)
| Fig | 내용 | 데이터 |
|---|---|---|
| 1 (MAIN) | 4-panel COHP (P–S/S–S/Li–S/Li–Cl), 4d-Cl 2-peak | docs/figures/icohp/{comp1,modelc}_COHP_4panel.png |
| 2 | 구조 3-panel (Li–Cl 히스토·Voronoi·Li환경) | docs/figures/slide15_licl, slide16_voronoi |
| 3 | BVSE 채널 iso (9.84% vs 3.33%) | docs/figures/icohp/ |
| 4 | DOS/PDOS + bands (gap 2.066/2.099) | docs/figures/dos_compare_3.png, {comp1,modelc}_pdos_compact.csv |
| 5 (STAR) | vacancy paradox bar (clamped 52=52 → relaxed 22 vs 28) | elastic.json |
| 6 | AIMD Arrhenius (Ea 0.253/0.224) | docs/figures/slide09_arrhenius/arrhenius_fit_origin.csv |
| SI | ELF iso/slice, Cij eigenvalue, per-Cl ICOHP | docs/figures/icohp/ |

CSV: arrhenius_fit_origin, icohp_compare, icohp_summary_wide, {comp1,modelc}_pdos_compact, licl_distances_origin, ps_bondlengths_origin.

---

## 서사 (보고/논문 arc)
> **"Cl-rich LPSCl1.6는 벌크 전자구조(갭·궤도 동일)를 안 바꾸면서 전도 ~3×(고온)를 얻는다. 차이는 구조적 — 음이온 disorder(Li 공공+4d-Cl anti-site)가 동시에 (1)Li-hop 장벽↓(Ea −11.7%), (2)경로↑(D₀ +41%), (3)이온결합 강화(Li-음이온 +8–13%). 이 disorder가 soft Li-shear mode를 미리 jam → relaxed-ion Young's +25%. 기계 손해는 운영온도서 0. 산화는 내재창 동일(S-limited)이나 Cl 산물이 bulky→구속안정화(창 2×)·계면 R↓; 단 달력안정성은 손해(→O-도핑 동기). 결론: 음이온 치환으로 '속도 vs 안정성'을 튜닝."**

## 핵심 caveat (보고 시 명시)
1. **기계값은 전부 relaxed-ion** (clamped-ion 52는 비물리, 비교금지).
2. **σ 절대값은 UMA 3–5× 과대** → 비율·600–1000K만; 300K는 외삽 불확실.
3. **갭 절대값**은 USPP/PBE라 문헌(PAW) 대비 ~0.3eV 낮음 — 단 comp1↔modelC Δ는 유효.
4. constrained ESW는 leading-order(완전 Fitzhugh 재최소화 미완); 경향 robust.
5. Bader 개별 P/S σ 큼(basin shape) → **PS₄ 합으로 보고.**
6. modelC 옛 'defect band'='DOS-threshold 아티팩트'(정정됨).
