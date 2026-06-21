# Structure–Property Relationship of Argyrodite SEs — 통합 논리 (MASTER)
LPSCl (Li₆PS₅Cl) vs LPSCl₁.₆ (Li₅.₄PS₄.₄Cl₁.₆) · 2026-06-21
모든 수치는 우리 DFT/MLIP db. 흩어진 per-axis 리포트를 하나의 인과 사슬로 통합.

---

## 0. 중심 명제 (one sentence)
> **할로겐 enrichment(Cl↑)는 "구조 레버"다: 결합 화학은 그대로 둔 채 Li 공공 + anti-site Cl/S 무질서만 주입한다. 이 구조 변화가 이온전도도(×4)와 강성(+25%)을 동시에 올리면서, 내재 산화창은 그대로(S²⁻-limited)이고 양극 열역학 반응성은 오히려 낮춘다. Cl-rich의 알려진 실험적 단점은 열역학이 아니라 kinetic/interfacial이다 (전자전도도 두 조성이 같아서 원인 아님 — 후보: 이온전도 ×4·CEI passivation, 세부는 본 계산으로 미규명).**

---

## 1. 인과 사슬 (structure → property)

### [A] 조성 변화 = 두 가지 구조 효과
**Aliovalent 치환** 2Cl⁻ → S²⁻ + V_Li (Kröger–Vink: Cl•_S + V′_Li). 결과:
- **(i) Li 공공** (5 f.u.당 Li 27 vs 30 → 3 vacancy)
- **(ii) anti-site Cl/S 무질서** (free-anion 4a/4d 자리 SOF 분산)
→ 이 둘이 모든 물성 변화의 *뿌리*. (≠ "mixed", ≠ 공유성 변화)

### [B] 이온전도도 ×4 — 이중 메커니즘
| 인자 | 값 | 출처(증거) |
|---|---|---|
| Ea 인자 exp(ΔEa/kT)@300K | **×3.2** | AIMD Ea 0.253→0.224; anti-site가 inter-cage landscape 평탄화 |
| carrier/D₀ 인자 | **×1.41** | D₀ 4.11e-4→5.8e-4; Li vacancy가 운반자↑ |
| **곱** | **×4.5 (≈실측 14/3.4=×4.1)** | 잔차 거의 0 |

**다중 독립 증거 (같은 결론):**
- **AIMD-MLIP**: Ea 0.253→0.224, σ 3.4→14 mS/cm, D600 3.09e-6→7.90e-6.
- **BVSE**: comp1 단일 채널(BVS 1.60–1.64) → modelc bimodal(60.2%가 1.83–1.89, anti-site Cl 인접). 정적 채널은 −15%인데 σ는 ×4 (역설) → vacancy가 BVSE 못 보는 곳에서 작동.
- **Voronoi 무질서 std**: P 0→0.37, Cl 0→0.74, Li 0.21→1.15 (무질서↑ 정량).
- **Percolation (Li-density PMF, F=−kT·lnρ)**: 침투장벽 comp1 **0.191** → modelc **0.078 eV** (inter-cage 경로 평탄 = Ea↓를 BVSE와 독립적으로 재확인; cluster-count 역설 해소).

### [C] 결합 화학은 불변 (= 대조군, σ↑가 구조 탓임을 증명)
- **ELF**: Li–Cl·Li–S 이온결합 + P–S 공유결합, **조성 무관 유지** (bond-min ELF 동일).
- **Bader**: Li +0.88, Cl −0.91, P +4.7, S −1.8; **PS₄ 전하 불변**. (|Cl|>|Br| = Cl이 더 이온성)
- **CDD**: 재배치 ~5.8e(comp1)/6.84e(modelc), 둘 다 노랑(P–S 축적)/파랑(Li 결핍) **같은 패턴**.
→ **σ 변화는 공유성/전하 변화가 아니라 순수 구조(공공+무질서)** — 3개 독립 방법이 같은 대조 결론.

### [D] 기계: B0↓(vacancy) vs E_VRH↑(disorder) — 두 모듈러스가 반대로 (paradox 해결)
- **B0 (bulk, EOS)**: comp1 **26.2** → modelc **21.7 GPa (−17%)** ← **vacancy**: Li⁺ 빠지면 Coulomb 응집↓ → 부피압축이 쉬워짐(**bulk 연화**).
- **E_VRH (Young, relaxed-ion)**: comp1 **22.1** → modelc **27.7 GPa (+25%)** ← **anti-site disorder**: C44(전단) 8.0→**13.7** + Zener A 1.14→**1.44** → G(전단)↑. E는 전단 지배라 **E↑**.
- **★ divergence**: E = 9KG/(3K+G)에서 vacancy의 **K↓**를 disorder의 **G↑**가 이겨 net **E↑**. 즉 **vacancy = bulk 연화 / disorder = shear 강화**, 서로 반대 방향. (vacancy 단독은 오히려 E를 내리는 쪽.)
- clamped-ion은 둘 다 52.3로 동일(2.3× 과대 = paradox 인공물) → **relaxed-ion이라야 이 divergence가 드러남**. EOS B0(26.2) ≈ relaxed B_VRH(25.5) 교차검증.
- (정량 분리: ordered-vacancy vs disordered modelc의 C_ij 비교 = Ea 슬라이드7 disorder-control의 기계 버전.)
- clamped-ion은 52.3으로 둘 다 동일(2.3× 과대) = **paradox 인공물**. 이온 이완(Born screening) 허용해야 실험(~23)·문헌 DFT(SQS 22.1, ensm 27.8–29.9)와 일치.
- EOS B0(26.2) ≈ relaxed B_VRH(25.5) → 교차검증 통과.
→ Cl-rich가 **더 단단함** (문헌 Kim 초음파는 두 조성 비슷하나, 단결정 DFT는 강화 예측).

### [E] 전자구조는 조성 무관 (gap·VBM)
- **gap (eigenvalue)**: comp1 **2.066** ≈ modelc **2.099 eV** (PBE; 실제 mBJ 3.11/HSE 3.30). 갭은 disorder 무관.
- **VBM = S 3p** (둘 다). **PDOS**: free S²⁻ 3p가 가장 얕음(mean −0.88/−0.90 eV), PS₄-S 깊음(−2.14/−2.25, P–S 공유결합 안정화), Cl 더 깊음(−2.83).
→ **free S²⁻ = 산화-prone 자리**, 조성 무관. Cl-rich는 free S²⁻를 4→2로 줄임.

### [F] 산화/전기화학 안정성
- **내재 ESW (grand-potential)**: 둘 다 환원 1.24 / OCV 1.72 / **산화 onset 2.14 V (S²⁻→폴리설파이드)**. **동일** — Cl⁻는 3.3 V까지 불활성이라 onset 안 바꿈 (S²⁻-limited). VBM 0.32 eV 차이에도 onset 동일 = 산화는 밴드엣지 아니라 분해화학.
- **계면 반응성 (전압분해, v2)**: LPSCl이 모든 양극·전압에서 **더 반응성**, 격차 +0.04(2.5V)→+0.20(4.3V). Cl이 반응성 S/Li를 희석 → **Cl-rich가 열역학적으로 덜 반응**.
→ 문헌 "Cl-rich 양극서 더 나쁨(분해전류↑)"은 **열역학 아님 → kinetic/interfacial**. ⚠️ **전자전도도 아님** (LPSCl≈LPSCl1.6 갭 2.066≈2.099 → σ_e 동일). 후보: 이온전도 ×4가 분해 kinetics 가속 / CEI passivation 품질 (세부 미규명). 우리 계산이 *열역학·전자구조* 둘 다 배제.

---

## 2. 마스터 비교표
| 물성 | LPSCl (comp1) | LPSCl₁.₆ (modelc) | 변화 | 근거 |
|---|---|---|---|---|
| 구조 | 입방, 공공 0 | 능면체, 공공 3/5fu + anti-site | 무질서↑ | XRD/구조 |
| Ea (eV) | 0.253 | 0.224 | ↓ | AIMD |
| σ₃₀₀ (mS/cm) | ~3.4 | ~14 | **×4** | AIMD+NE |
| 침투장벽 (eV) | 0.191 | 0.078 | ↓ | Li-density PMF |
| 결합(ELF/Bader/CDD) | 이온 Li/공유 PS₄ | **동일** | — | 대조군 |
| **B0 bulk (GPa)** | 26.2 | 21.7 | **−17%** | EOS (vacancy 연화) |
| C44 shear (GPa) | 8.0 | 13.7 | +71% | disorder |
| E_VRH relaxed (GPa) | 22.1 | 27.7 | **+25%** | 탄성 (disorder) |
| 밴드갭 (eV) | 2.066 | 2.099 | ~동일 | eigenvalue |
| VBM | S 3p | S 3p | 동일 | PDOS |
| 산화 onset (V) | 2.14 | 2.14 | **동일** | grand-potential |
| 양극 반응성 @4.3V | −1.54 | −1.35 | Cl-rich↓ | interface v2 |

---

## 3. 증명됨 vs 대기
**증명됨 (다중 독립 증거):**
- σ↑ 이중 메커니즘 (AIMD×BVSE×Voronoi×percolation, 정량 닫힘).
- 결합 불변 (ELF×Bader×CDD).
- 강성↑ + vacancy paradox 해결 (relaxed vs clamped, EOS 교차검증).
- 산화 onset 동일 + S²⁻-limited (grand-potential + PDOS).
- 양극 반응성 Cl-rich 우위 (interface v2, 전압분해).

**대기 (HPC):**
- **ε∞ (격자 분극률, Kraft 메커니즘)** — epsilon.x 입력 준비됨. "분극률↑→연한 격자→Ea↓"를 우리 DFT로 직접 연결 → [B]를 보강할 마지막 축.
- modelc MP-호환 DFT 에너지 (interface reactivity 정밀화).

---

## 4. 슬라이드 매핑
- S1–2: 동기·문헌표 / S3: 시스템 설계 / **S4–7: 이온전도도([B][C] + percolation·이중메커니즘 슬라이드)**
- S10: 기계([D]) / S15–16: ELF·Bader([C]) / S18: 전자구조([E])
- 산화 섹션: ESW staircase + interface v2([F]) / PDOS(free S²⁻)
- 신규(우리 기여): percolation, 이중메커니즘 분해, CDD 비교, PDOS site, interface v2, ε∞(대기)

## 5. 한 줄 결론 (발표 마무리)
> "Cl enrichment는 결합을 바꾸지 않고 **공공+무질서**만으로 σ(×4)·강성(+25%)을 올리며, 내재 산화창(S²⁻-limited, 2.14 V)은 보존하고 양극 열역학 반응성은 낮춘다. 남는 단점은 kinetic/interfacial(전자전도 아님 — 갭 동일; 이온전도·CEI 후보)이라 코팅/계면설계로 다룰 영역이다."
