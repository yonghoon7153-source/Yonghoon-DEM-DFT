# Slide 2 (Literature summary) — 개정 (2026-06-21)

문헌 20+편(실험) + 18편(계산) 종합 → 대표값(±범위) + 출처. 구조: 조성별 **문헌 / BML(본 연구)** 2행.
BML/DFT(파란값)은 우리 db와 일치 — 유지. 문헌 행만 아래로 교체.

## 개정 표

### LPSCl (Li₆PS₅Cl)
| 열 | 문헌 (literature) | BML (본 연구) |
|---|---|---|
| σ 실험 (mS/cm) | **2.9 ± 0.9** (1.5–4.9; Adeli 2.5, ACS EL 2.4, Nanolett 3.3, Kim 3.5) | 2.95 ± 0.25 |
| σ DFT (mS/cm) | 0.4–2.3 (방법의존: AIMD 0.43, MTP 2.3) | **3.4** |
| Ea 실험 (eV) | **0.34 ± 0.04** (0.26–0.38; Kraft 0.25*, Adeli 0.34) | — |
| Ea DFT (eV) | 0.33 ± 0.05 (AIMD 0.325–0.38) | **0.253** |
| Oxidative (V) | onset ~1.95 (CV) / grand-pot ESW **1.74–2.01** | — |
| Mechanical (GPa) | **E 21.3** (Kim ultrasonic; G 8.45, B 14.8) ※7.6에서 수정 | 9.7 / DFT **22.06** (relaxed E) |
| Band gap (eV) | PBE **1.88–2.45** / mBJ 3.11 / HSE 3.30 | **2.066** |

### Halogen-rich LPSCl (Li₅.₅PS₄.₅Cl₁.₅ / **Li₅.₄PS₄.₄Cl₁.₆**)
| 열 | 문헌 | BML (본 연구) |
|---|---|---|
| σ 실험 (mS/cm) | **8.7 ± 1.5** (6–11; **Li₅.₄Cl₁.₆ = 10.8** Nanolett'21; Adeli 9.4, Kim 9.9) | 7.5 ± 0.6 |
| σ DFT (mS/cm) | 14.55 (AIMD, S2405829721005894) | **14** |
| Ea 실험 (eV) | **0.27 ± 0.03** (0.24–0.32) ※0.254에서 보정 | 0.29 ± 0.01 |
| Ea DFT (eV) | 0.23 (AIMD) | **0.224** |
| Oxidative (V) | onset ~1.9 (LPSCl보다 낮음, 분해전류↑; AdvFM'22, Anie'22) | onset 2.85 / max 3.5 |
| Mechanical (GPa) | **E 21.6** (Kim ultrasonic; G 7.61, B 14.3) / AFM 16–18 | 17.5 ± 0.5 / DFT **27.66** |
| Band gap (eV) | ~1.84–2.1 (PBE) | **2.099** |

## ★ 꼭 고칠 것 (현재 → 개정)
1. **LPSCl Mechanical 7.6 → E 21.3 GPa** (Kim 2025 ultrasonic). 7.6은 E가 아니라 G(8.45)에 가까운 잘못된 값.
   - 두 조성 mech를 **Kim ultrasonic E로 통일**: LPSCl 21.3 / Cl-rich 21.6 (같은 측정법 = 공정).
2. **Halogen-rich Ea 실험 0.254 → 0.27 ± 0.03** (문헌 평균).
3. **σ 실험에 우리 정확 조성 표시**: Li₅.₄PS₄.₄Cl₁.₆ 실측 **10.8 mS/cm** (Nanolett 2021) — 8.65보다 이게 우리 조성과 직결.
4. **Band gap 각주**: PBE는 과소 → mBJ 3.11 / HSE06 3.30 (실제 gap). 우리 PBE 2.07 vs 문헌 PBE 2.45 차이는 QE-USPP vs VASP-PAW (method spread 2.1–2.45 내).

## 주의/해석 포인트 (발표 시)
- **기계: 실험(Kim) vs 우리 DFT 불일치 주목** — Kim ultrasonic E는 LPSCl 21.3 ≈ Cl-rich 21.6 (**거의 동일**)인데, 우리 relaxed-ion DFT는 22.06 → 27.66 (**+25%**). 즉 *단결정 DFT는 Cl-rich 강화를 예측하나 pellet ultrasonic 실험은 차이 작음* → "단결정 vs 다결정/포로시티" 차이로 설명 (정직하게 언급).
- Ea*: Kraft NMR 0.25는 short-range, EIS는 0.33–0.38 (long-range = 측정 표준).
- σ DFT(문헌)는 disorder 모델에 따라 0.4~30으로 출렁 → 우리 AIMD 3.4/14가 실험(2.9/8.7)과 잘 맞는 게 강점.

## 핵심 출처
- 기계 실험: Kim *ACS Mater.Lett.* 2025 (10.1021/acsmaterialslett.4c02029) — LPSCl/Cl-rich 둘 다.
- σ Cl-rich: Adeli *Angew.* 2019; **Li₅.₄Cl₁.₆ Nanolett 2021** (10.1021/acs.nanolett.1c01344).
- gap: Batteries 2026 (PBE 2.45/HSE 3.30); Physica B 2023 (mBJ 3.11).
- 기계 DFT 비교: Deng *JES* 2016 (E 22.1); Torii/jpcc 2025 (E 27.4).
