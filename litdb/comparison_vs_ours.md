# 🔬 문헌 ↔ 우리 DFT — 차이 + 적용 인사이트

> 기준값: `our_dft_baseline.md`. 각 물성축마다 "문헌이 뭐라 하나 / 우리가 뭐라 하나 / 왜 다른가 / 어떻게 쓰나".

## A. 이온전도도 (Cl-rich가 빠르다 — 모두 일치)
- 문헌(다수 exp): Cl 증가(→Cl1.5–1.6) σ 2.5→7–10 mS/cm, Ea 0.34→0.22 eV (Adeli/Anie2019, Liu2022, Zuo2022, Nanolett2021).
- 우리: D(600K) 3.09→7.90e-6, Ea 0.253→0.224 — **방향·크기 정합.**
- 인사이트: 우리 AIMD가 실험 trend를 재현 → 신뢰. 단 절대 σ는 RT 외삽이라 실험과 직접 비교는 Arrhenius로.

## B. 산화안정성 — **4축으로 분리 (한 단어로 말하면 틀림)**
| 축 | 결론 | 근거 |
|---|---|---|
| ① intrinsic 0-pressure window | **무승부** (~2.1 V, S²⁻-limited) | 우리 ESW = Gil-González K_eff=0 (1.7–2.4) |
| ② 기계 구속 window | **Cl-rich 승** (구속 시 더 넓어짐) | Gil-González K_eff=20 + 우리 constrained_esw |
| ③ cathode 계면 cycling | **Cl-rich 승** (R_int↓, 성능↑) | Zuo (산물 양호) — 우리 stoichiometry 재현 |
| ④ calendar/thermal/moisture | **Cl-rich 패** | Wu2026 (90 ℃ retention L6 68%>L55 48%) |
- 우리 한계: ESW는 ①만 봄(S-limited 구조적). 실제 분해 *양*(Zuo CV 2×)·metastability(DSC/TGA)는 못 잡음 → 무질서 E_above_hull 계산이 보강책.
- 인사이트: deck에서 **"Cl-rich 산화안정성"을 축 명시 없이 말하지 말 것.** 핵심 결론 = "전도도 이득이 산화창 손해 없이(①–③ 중립~유리), 비용은 shelf-life(④)".

## C. 기계적 물성 (값이 functional·정의에 크게 의존)
- 문헌: Kaur2016(SQS) E=22.1/B=28.7/G=8.1; JPCC2025(D3) E=27.4/B=34.7/G=10.0/(B/G=3.46 연성); AcsMater2025 E 21.3→21.6 (Cl0→1.5 거의 불변).
- 우리: E_VRH 22.06→27.66, B0 26.23→21.71.
- **차이 원인**: relaxed-ion vs clamped-ion, PBE vs PBEsol/D3 → E/B 절대값 ±수 GPa. **비교 전 functional·ion-relax 조건 맞출 것.**
- 인사이트: B/G(Pugh) 연성 결론은 robust(문헌·우리 공통). 절대 modulus는 same-protocol(우리 cascade)에서만 비교.

## D. 전자구조 / band gap (방법 의존 — 절대 비교 금지)
- 문헌: Lu2025(PBE) 1.88; Ma2026(PBE) 2.10→2.62(In); batteries2026 PBE 2.45 / **HSE06 3.30**.
- 우리: 2.066(comp1)/2.098(modelc) PBE.
- **차이**: PBE 과소평가(HSE/exp ~3+ eV) + 무질서 배열·k-mesh ±0.2–0.3. → 1.88 vs 2.10은 model scatter, **σ_e와 무관**(In 0.52 eV↑가 σ_e 1.2×만 바꿈 = defect-controlled).
- 인사이트: gap은 "wide-gap insulator" 수준만. σ_e는 defect(neζ) 얘기로 (슬라이드 25 틀).

## E. 우리 계산이 문헌을 "검증"하는 지점 (강점으로 쓸 것)
- grand-potential 분해식 = Zuo Eq1/Eq2 재현 (③).
- 0-pressure ESW = Gil-González K_eff=0 재현 (①).
- AIMD Ea/D trend = exp 재현 (A).
- VBM=S 3p = HAXPES(Banik) 재현.

## F. 우리가 아직 못 하는 것 (정직 목록 → 향후)
- 기체상(SO₂/O₂) 포함 계면 분해 (Zuo의 R_int 메커니즘)
- 무질서 E_above_hull (DSC/TGA metastability)
- defect/σ_e 정량 (slide25 틀의 실제 계산)
- slab IP / absolute VBM (UPS 절대 기준)
