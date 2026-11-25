# Zhao 2025 Small Methods Ce/O Co-Substitution — Critical Analysis

> **System**: Li₅.₄₊ₓP₁₋ₓCeₓS₄.₄₋₂ₓO₂ₓCl₁.₆ (x=0–0.05, optimal x=0.02)
> **Claim**: Ce⁴⁺ substitutes P⁵⁺ at 4b site, O²⁻ substitutes S²⁻ in PS₄ tetrahedra
> **Relevance**: Park (BML) raised this paper as challenge to our Nd→P infeasibility conclusion. This document refutes that challenge.

## TL;DR (Park 답변용 한 줄)

> Zhao 식은 'CeO₂ + Ce⁴⁺ + P-site' 3중 가정의 산물. Sulfide 환경 화학과 lanthanide ionic radius를 정직하게 따랐다면 **Li_{5.4-3x}Ce_xPS_{4.4-1.5x}O_{1.5x}Cl_{1.6}** 식이 됐을 것 — 즉 우리 Nd Track 1 식과 동일 구조. 결국 Zhao 합성물도 atomistically 보면 Ce가 Li 자리에 들어가있을 가능성이 매우 큼.

---

## 1. Ce⁴⁺ ≠ Nd³⁺ — 화학이 완전히 다름

| 항목 | Ce⁴⁺ (Zhao) | Nd³⁺ (우리) |
|---|---|---|
| Shannon r (CN=6) | **0.87 Å** | **0.983 Å** |
| P⁵⁺(0.38 Å) mismatch | 2.3× | **2.6×** |
| P⁵⁺ 치환 net charge | **−1 e** | **−2 e** |
| 보상 필요 Li⁺ | 1개 | **2개** |
| 4f 전자 | 4f⁰ (closed) | 4f³ (open shell) |

→ Ce⁴⁺는 PS₄ 중심에 들어가도 자기/궤도 disturbance 없음 (closed shell).
→ Nd³⁺의 4f³는 강한 국소 자기모멘트 + 이방성 결합.
→ "Ce가 됐으니 Nd도 된다"는 단순 외삽 불가.

---

## 2. Zhao 식의 charge balance — Ce⁴⁺ 가정에만 성립

식: $Li_{5.4+x}\ P_{1-x}\ Ce_x\ S_{4.4-2x}\ O_{2x}\ Cl_{1.6}$

### Case 1: Ce⁴⁺ 가정 (Zhao 본문 implicit)
| | Cation | Anion |
|---|---|---|
| Li(+1)×(5.4+x) | +5.4+x | |
| P(+5)×(1-x) | +5−5x | |
| Ce(+4)×x | +4x | |
| S(−2)×(4.4−2x) | | −8.8+4x |
| O(−2)×2x | | −4x |
| Cl(−1)×1.6 | | −1.6 |
| **Sum** | **+10.4** | **−10.4** ✓ |

### Case 2: Ce³⁺ 가정 (sulfide 환경 일반적)
| | Cation | Anion |
|---|---|---|
| Li(+1)×(5.4+x) | +5.4+x | |
| P(+5)×(1-x) | +5−5x | |
| Ce(+3)×x | +3x | |
| S(−2)×(4.4−2x) | | −8.8+4x |
| O(−2)×2x | | −4x |
| Cl(−1)×1.6 | | −1.6 |
| **Sum** | **+10.4 − x** | **−10.4** ✗ |

→ Ce³⁺이면 식 자체가 안 맞음. Zhao는 Ce⁴⁺을 implicitly 가정.
→ **그런데 Ce 3d XPS가 본문/SI 어디에도 없어** Ce 산화상태 직접 검증 부재.

---

## 3. 정직한 식 derivation — 4가지 시나리오

| Case | Precursor | Ce | Site | Li 변화 | O 변화 | "그럴듯함" |
|---|---|---|---|---|---|---|
| ① Zhao | CeO₂ | +4 | P | +x | +2x | 가정 3개 |
| ② | CeO₂ | +4 | Li | −4x | +2x | 가정 2개 |
| ③ | Ce₂O₃ | +3 | P | +2x | +1.5x | 가정 1개 |
| ④ | Ce₂O₃ | +3 | Li | **−3x** | +1.5x | **가장 합리** |

### Case ④ (정직한 식)
$$Li_{5.4-3x}\ Ce_x\ P\ S_{4.4-1.5x}\ O_{1.5x}\ Cl_{1.6}$$

- **우리 Nd Track 1 식과 정확히 동일 구조**
- Lanthanide(0.87–0.98 Å) >> P⁵⁺(0.38 Å) → size-wise 절대 P 자리 못 들어감
- 자연스럽게 Li 자리 (Ce³⁺ 0.87 Å, Li⁺ 0.76 Å, ratio 1.14× — 무난)

→ Lanthanide 도핑은 본질적으로 Li-site 치환.

---

## 4. SI 데이터의 자기모순 (smoking guns)

### 🔴 4.1 Table S2 — O는 PS₄(16e) 아닌 free S(4d) 사이트
| Site | Wyckoff | Atom | Occ |
|---|---|---|---|
| PS₄ corner | **16e** | S1 | 1.0345 (S만, **O 없음**) |
| Free S²⁻ | **4d** | S2 | 0.9753 |
| Free S²⁻ | **4d** | **O1** | **0.0247** ← 여기 |

→ "O substitutes S in PS₄ tetrahedra" 본문 주장과 모순.
→ "P-O 결합 강화" 메커니즘 무너짐.

### 🔴 4.2 Figure S1 (XPS O 1s) — PS₃O³⁻ 피크 없음
| Peak | Position | Intensity | 의미 |
|---|---|---|---|
| Li-O-P | ~532 eV | dominant | O가 free site에서 framework bridge |
| P-O-P | ~530 eV | minor | pyrophosphate bridge (표면/축합) |
| ~~PS₃O³⁻~~ | (~531 eV expected) | **없음** | PS₄ 내부 O 치환 신호 0 |

→ Table S2의 "O@4d" 가설을 XPS로 직접 확인.

### 🔴 4.3 Figure S6 (Raman) — PS₄ chemistry 변화 없음
- PS₄³⁻ ν₁ ~420 cm⁻¹ peak 위치/형태 도핑 전후 거의 동일
- Peak splitting 없음, ~950 cm⁻¹ 새 P-O peak 없음
- → PS₄ tetrahedron 내부 O 치환의 분광학적 증거 부재

### 🔴 4.4 Ce 정련 occupancy 3.6× 과대
- Nominal x=0.02 → Ce = 0.02 atoms/f.u.
- Refined occ = 0.0720 → 3.6× 과대 검출
- 가능 해석: 국소 클러스터링 / Rietveld over-fit (Z=58 무거움) / 실제 함량 오차

### 🔴 4.5 LiCl 불순물 confounder
| | LiCl impurity | σ (mS/cm) |
|---|---|---|
| LPSC (x=0) | 6.024% | 6.82 |
| LPSC-0.02 | 3.237% | 7.13 |

→ LiCl 절연체. 6%→3% 감소만으로도 σ 향상 일부 설명 가능.
→ "Ce/O 효과"보다 batch quality 차이일 수 있음.

### 🔴 4.6 σ vs x 비단조성 + E_a anomaly
| x | 0 | 0.01 | 0.02 | 0.03 | 0.04 | 0.05 |
|---|---|---|---|---|---|---|
| σ (mS/cm) | 6.82 | **5.50**↓ | 7.13↑ | 6.32 | 5.97 | 5.27 |
| E_a (eV) | 0.293 | 0.284 | 0.266 | 0.293 | 0.27 | **0.188**!? |

→ x=0.01에서 19% 감소, x=0.02만 회복. 물리적으로 비합리.
→ x=0.05 E_a=0.188 anomaly. Batch noise 의심.

### 🔴 4.7 Table S3 — 자기 reference에 더 좋은 도핑 존재
- LPSC-Sn/O (same base): **8.7 mS/cm** > LPSC-Ce/O **7.13**
- Ce 도핑의 novelty 약함.

### 🔴 4.8 Li occupancy inconsistency
- LPSC Li1 (48h) Occ: 1.0080
- LPSC-0.02 Li1 (48h) Occ: 15.9853
- 같은 사이트 15.86× 차이 → normalization convention 불일치 또는 오류

### 🔴 4.9 EIS bulk vs GB 분리 안됨
- Single semicircle fitting → bulk Li 전도도와 grain boundary 분리 불가
- σ 향상 메커니즘이 bulk인지 GB인지 EIS만으로 결정 불가

---

## 5. 농도 비교 — x=0.20 (DFT) vs x=0.02 (Zhao 실험)

### 우리 결론이 dilute에도 적용되는 이유
1. **Per-defect cost 농도에 1차 둔감**: ΔE_form ~7 eV의 dominant 항은 size mismatch (Nd 0.98 vs P 0.38, 2.6×). Nd-Nd 상호작용은 ~1-2 eV 수준.
2. **Aliovalent doping은 dilute에서 더 불리**: Li interstitial 보상 효율 dilute에서 떨어짐. 우리 x=0.20은 lower bound.
3. **Boltzmann factor**: ΔE ~5-7 eV @ 298K → exp(-200) ≈ 0. 농도 무관 평형 점유 0%.
4. **ΔΔE 비교의 robustness**: Track 1, 2 모두 같은 x=0.20, 같은 settings → systematic error cancel.

### Reviewer 대비 추가 계산 권장
- **Single-Nd in 240-atom (x=0.10)** dilute control × 2 (Track 1, 2)
- KISTI ~10일 추가, paper credibility 큰 향상

---

## 6. 종합 판정표

| Zhao 본문 주장 | SI 증거 | 판정 |
|---|---|---|
| Ce@P site (4b) | Table S2 occ 3.6× nominal | ⚠️ 정량 부정확 |
| O@PS₄ (16e) | Table S2 → 4d, Fig S1 PS₃O³⁻ 부재, Fig S6 Raman 변화 없음 | 🔴 **반박 가능** |
| Homogeneous Ce 분산 | Fig S3 SEM에 EDS 없음 | ⚠️ 미검증 |
| Bulk σ 향상 | Fig S5 single arc, GB 분리 없음 | ⚠️ 메커니즘 모호 |
| Ce 산화상태 | XPS Ce 3d 부재 | 🔴 **검증 부재** |
| LiCl 불순물 | Table S1/S2: 6.0% → 3.2% | 🔴 **σ confounder** |

---

## 7. 우리 paper 어드밴티지

| Zhao 약점 | 우리 답 |
|---|---|
| DFT 검증 0개 | DFT+U + ISPIN=2 + 500+ configs |
| Rietveld만으로 site 단정 | Track 1/2 ΔE_form 정량 비교 |
| O 위치 본문/SI 모순 (16e vs 4d) | 16e와 4d 모두 enumerate, 안정 site 결정 |
| Ce 산화상태 미검증 | Nd³⁺ explicit, Nd₂O₃ precursor 명확 |
| LiCl impurity confounder | DFT는 pure phase, 불순물 효과 없음 |
| x=0.02만 측정 | x=0.20 + (계획) x=0.10 농도 scaling |
| Bulk vs GB 분리 없음 | Single crystal supercell DFT |
| Charge balance Ce⁴⁺ 가정 의존 | Nd³⁺으로 식 엄밀 검증 |

---

## 8. Park 답변 template

> **"Zhao 2025 SI를 정밀 분석한 결과:**
> 1. **O 1s XPS (Fig S1)에 PS₃O³⁻ 피크가 없습니다** — 모든 O 신호는 Li-O-P 또는 P-O-P 다리에서 옴
> 2. **Raman (Fig S6)에서 PS₄ ν₁ peak (420 cm⁻¹)이 도핑 전후 동일** — peak shift/splitting 없음
> 3. **Rietveld Table S2도 O를 4d (free S 사이트)에 위치**
> 4. **Ce 3d XPS 부재** → Ce 산화상태 검증 안 됨
>
> 본문의 'PS₃O³⁻ 형성으로 P-O 결합 강화' 메커니즘은 SI 데이터로 뒷받침되지 않습니다.
> Ce 정련 occ가 nominal의 3.6배로 P-site 점유 정량성이 약하고, σ 향상은 LiCl 불순물 감소(6.0%→3.2%)로 부분 설명 가능합니다.
>
> 또한 Zhao 식은 'CeO₂ + Ce⁴⁺ + P-site' 3중 가정의 산물이며, sulfide 환경 화학과 lanthanide ionic radius를 정직하게 따랐다면 식 ④ Li_{5.4-3x}Ce_xPS_{4.4-1.5x}O_{1.5x}Cl_{1.6} (= 우리 Nd Track 1 식과 동일 구조)이 됐을 것입니다.
>
> 우리 Nd₂O₃ 연구는 (a) Nd³⁺(0.98 Å, charge -2)는 Ce⁴⁺(0.87 Å, -1)보다 mismatch가 크고, (b) DFT로 Track 1 (Nd→Li) vs Track 2 (Nd→P)를 정량 비교하며, (c) O 위치도 16e/4d 모두 enumerate해서 Zhao보다 더 엄밀한 atomistic 검증이 가능합니다."**

---

## 9. 결론

> Zhao 2025는 **우리 결론을 깬다기보다, 같은 lanthanide 화학을 P-site로 misinterpret한 사례**.
> 우리 DFT 결과는 Zhao의 CeS₂ 2차상 형성 + 비단조 σ trend + O@4d 위치와 **모두 consistent**.
