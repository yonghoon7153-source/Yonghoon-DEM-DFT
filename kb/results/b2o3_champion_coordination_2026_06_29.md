# B₂O₃-doped LPSCl 챔피언 구조의 국소 배위: 삼각 BS₃ + free-S + phosphate P–O

**날짜** 2026-06-29 · **구조** `db/structures/b2o3_relaxV0.cif` (DFT V₀ 고정셀 relax, QE PBE)
**조성** Li₅₈P₈S₄₁Cl₁₆**B₂O₃** (128 atoms = modelc Li₅.₄PS₄.₄Cl₁.₆ 2×10f.u. + B₂O₃)

> **한 줄 결론.** B₂O₃-doped argyrodite의 DFT 챔피언 구조에서 **B³⁺는 삼각평면 BS₃**(4번째 S는 비가교 free-S²⁻로 방출)를 이루고, **O²⁻는 P corner에 들어가 phosphate-like P–O(1.55 Å)** 를 형성한다(PS₄₋ₓOₓ). **B–O 결합은 없다.** 이는 thioborate glass ¹¹B NMR·결정질 Li₃BS₃·oxysulfide ³¹P NMR 문헌과 **완전 정합**하며, 우리 DB의 기존 "BS₄/BS₃O-rich" 예측을 **정정**한다.

---

## 1. 구조 출처

- UMA-s-1p1 B₂O₃-doping 챔피언(Ewald joint pre-rank → UMA relax) → DFT BM-EOS(96–104% 등방 부피 스케일, 셀 고정 이온 relax) → **BM3 V₀ = 2436.33 Å³, B₀ = 24.5 GPa** (vs undoped modelc DFT 21.7 GPa, +13%).
- V₀(2436.33 Å³)로 셀 등방 스케일 + 이온만 relax (`calculation='relax'`, vc-relax 아님 → argyrodite 입방 골격 보존). **bfgs 수렴**, Final E = −2621.7554 Ry.
- 셀: a=6.997, b=6.984, c=70.387 Å, α=60.08°, β=60.15°, γ=59.99° (= modelc 2×c).
- **전하수지**: 2 B³⁺@P⁵⁺ = −4 acceptor → **+4 Li**(기존 0.6 vac/fu 채움)로 보상; 3 O²⁻@S²⁻ = isovalent.

---

## 2. 국소 배위 — DFT 구조 실측 (minimum-image 거리)

### 2.1 B = 삼각 BS₃ + 비가교 free-S
| B | 결합 S (≈1.8 Å) | 4번째 S | 4번째 S의 최근접 양이온 |
|---|---|---|---|
| **B1** | S8 1.82, S4 1.82, S17 1.83 | S13 **3.72 Å** | P3=4.66, B2=10.85 → **어느 P corner도 아님 = free-S** |
| **B2** | S9 1.80, S18 1.84, S5 1.85 | S14 **3.95 Å** | B1=4.52, P4=9.92 → **free-S** |

→ B는 **S 3개와만 결합(BS₃, 삼각평면)**, 4번째 잠재 corner는 **비가교 S²⁻**(3.7–4.0 Å, 어느 사면체에도 안 속함).

### 2.2 P = 정상 사면체, O는 P corner에 (phosphate)
| P | corner 4개 | unit |
|---|---|---|
| P1,P2,P4,P5,P6,P8 | 4×S @ 2.05–2.08 Å | PS₄ (정상) |
| **P3** | **O2 1.55, O1 1.56**, S3 2.05, S12 2.10 | **PS₂O₂** |
| **P7** | **O3 1.56**, S38 2.05, S24 2.06, S29 2.08 | **PS₃O** |

→ **모든 P 4배위 정상**(긴 P–S 결합 없음, 5th 이웃 4.2 Å+). **O 3개 전부 P corner**(P3 2개 + P7 1개), **P–O = 1.55 Å = phosphate-like**. **B 근처 O 없음**(최근접 B–O 6.8–25.7 Å).

---

## 3. 문헌 검증 — 세 축 모두 정합

### 3.1 B = 삼각 BS₃ (Li-rich thioborate의 본질)
- **결정질 Li₃BS₃·LiSrBS₃ = "orthothioborates with trigonal planar boron coordination"** — Li 과잉 결정에서 B 삼각평면 BS₃ (직접 결정 선례).
- **Li₂S–B₂S₃ glass ¹¹B NMR**: Li₂S 증가 시 **4배위 분율 N₄ = 35% → 5% 감소**; 0.65Li₂S에서 **~80% BS₃**; 순수 B₂S₃ = **전부 BS₃**.
- **★ thioborate anti-anomaly**: oxide borate는 알칼리 첨가 시 BO₃→BO₄(4배위↑)이지만, **thioborate는 알칼리 첨가 시 BS₄→BS₃(3배위↑)**. → 극-Li-rich인 우리계는 **BS₃가 정답.** (Sakai 1994의 BS₄ Raman은 *저-Li* 조성; DB가 이를 일반화한 것이 오류였음.)

### 3.2 free-S = 비가교 S (documented)
- thioborate NMR: "BS₃/₂ triangles **with or without nonbridging sulfur atoms**" → 삼각 BS₃ 옆 비가교 S = 우리 S13·S14. **coordination motif로 알려짐.**

### 3.3 O = P corner phosphate (oxysulfide의 정설)
- O-doped Li₃PS₄ / LGPS / Li₆PS₅Cl **³¹P NMR: "S in PS₄³⁻ partially replaced by O"** → O가 PS₄ corner 치환 → **P–O(phosphate)** 형성. 우리 PS₂O₂·PS₃O와 정확히 일치. (O-doped argyrodite는 air/전기화학 안정성↑ 선례 존재.)

---

## 4. DB 정정

| 항목 | 기존 DB (`b2o3_doping_chemistry.md`) | 정정 (본 문서, DFT+문헌) |
|---|---|---|
| B 배위 | "**BS₄ tetrahedral** (Sakai), B prefers sp³" | **삼각 BS₃** (Li-rich → N₄↓, Li₃BS₃ 결정) |
| O motif | "**BS₃O-rich**, B가 O 끌어당김 (HSAB)" | **O-on-P (phosphate PS₄₋ₓOₓ)**, B–O 없음 |
| 근거 | Sakai BS₄ + HSAB 직관 (B 사면체 가정) | DFT 챔피언 + thioborate anti-anomaly + oxysulfide NMR |

> UMA가 "bo4(O-on-B) 근소우세(17/20)"라 했던 것은 **UMA의 B 화학 부정확**(DB 경고)에서 온 artifact 가능성. DFT·문헌은 둘 다 **O-on-P** 지지.

---

## 5. 왜 이런 배치인가 — 설득 논리 (paper/리뷰어용)

**축: "thioborate는 oxide와 반대로 Li가 많을수록 B가 삼각이 된다."**

1. **B³⁺ → 삼각 BS₃**: oxide borate anomaly의 정반대(알칼리↑ → BS₃↑, N₄ 35→5%). 극-Li-rich argyrodite → BS₃. [¹¹B NMR, Li₃BS₃]
2. **4번째 corner S 방출 = 비가교 free-S²⁻**: 작은 삼각 B가 4-corner(P) 자리를 못 채워 생기는 **본질적 coordination defect**. O 배치와 무관(B–O여도 B는 BS₂O로 1 S 방출). [thioborate NMR]
3. **O²⁻ → 더 강한 phosphate P–O(1.55 Å)**: B는 삼각으로 만족해 O 불필요 + free-S는 어차피 생김 → O는 phosphate corner 선호. [oxysulfide ³¹P NMR]
4. **검증 가능**: ¹¹B(삼각 BS₃ 시그널, δ·CQ)·³¹P(PS₄₋ₓOₓ 시그널) NMR로 **testable prediction**.

**한 문장 요약**: *"B³⁺ 도핑은 Li-rich argyrodite에서 삼각 BS₃ + 비가교 S²⁻를 형성하고, O²⁻는 phosphate corner(P–O)로 가 PS₄₋ₓOₓ를 이룬다 — thioborate anti-anomaly + oxysulfide 화학으로 설명되는, NMR-검증 가능한 구조."*

---

## 6. 전자구조 (진행 중)
- DFT NSCF gap(occupations='fixed', smearing 무) = **1.97 eV** (VBM 2.472 / CBM 4.439 eV). PBE band-structure 범위.
- PDOS(projwfc) 진행 중 → **비가교 S²⁻·B–S·P–O가 gap(1.97 eV) 근처에 주는 상태** 확인 예정 (coordination defect의 전자구조 흔적).

---

## 7. 정직한 한계
- 구조는 **UMA 챔피언 1개 + 고정셀 DFT local relax**. BS₃ 자체는 문헌 정합이나, BS₄/BS₃O 대안 motif의 **명시적 DFT 에너지 비교**(각 config 따로 구성·relax)는 미수행 — "BS₃가 *유일* ground state"가 아니라 "**Li-rich에서 BS₃가 문헌상 dominant이고 우리 챔피언과 일치**"까지가 현재 주장 범위.
- bo4 vs distributed(O-motif)는 UMA상 ~1–3 meV/atom near-degenerate(≪ Li-ordering 1162 meV)였음 — 절대 O-motif 선호는 약함, 글로벌 챔피언 배열이 distributed로 결정.

---

## 8. 참고문헌
- ¹¹B NMR, B₂S₃–Li₂S–LiI thioborate glass (N₄ 35→5%): J. Non-Cryst. Solids — https://www.sciencedirect.com/science/article/abs/pii/002230939190772X
- Li₃BS₃·LiSrBS₃, trigonal planar B orthothioborate — https://www.researchgate.net/publication/250552815
- Li₂S–B₂S₃ glass neutron diffraction (Sakai 1994) — https://www.sciencedirect.com/science/article/abs/pii/0022309394900345
- Oxysulfide solid electrolytes (O in sulfides 리뷰) — https://www.sciencedirect.com/science/article/abs/pii/S2405829725006671
- O-doped Li₆PS₅Cl argyrodite (안정성↑) — https://www.sciencedirect.com/science/article/abs/pii/S0167273823002023
- (DB 내부) `kb/methodology/b2o3_doping_chemistry.md`, `db/structures/b2o3_relaxV0.cif`, `db/properties/b2o3_eos_dft_result.json`
