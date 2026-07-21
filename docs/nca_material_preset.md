# A8 — NCA(Ni₀.₈₈) CAM 재료 프리셋: 물성 출처-교차검증 + 배선 결정 (2026-07-21)

랩 트렌드 소재 NCA를 파이프라인 옵션으로.  ★ 사용자 지시(2026-07-21): "물성값이면 확실하게 다른
문헌이랑도 비교하고 출처를 확실하게 하고 넣어" → **문헌 교차검증 에이전트 선행, 통과 값만 배선.**
검증 원자료: 로컬 PDF(`docs/literature_coverage/pdfs/Kang_2025_ACSAMI_*`) 정독 + WebSearch 독립문헌.

## ★ 헤드라인 발견 — E=175 GPa는 NCA 측정값이 아님

Kang&Shin 2025 본문 verbatim: *"The elastic moduli of NCA and LPSCl were **assumed** to be 175 and
22.1 GPa[42]"* — **assumed(가정)**, ref[42]=Koerver 2018 EES(10.1039/C8EE00907D)는 **팽창(부피변화)
논문**이지 모듈러스 측정 아님(umbrella 인용; E_NCA와 E_LPSCl을 한 ref에 걸어둠).  SI Table S4의
σ_e=1 S/m은 **무인용**, D=3e-14·c_max=48000은 [S1]=Yu 2023 JES **P2D 모델 테이블**(측정 아님).
→ **전체 파라미터가 모델-체인 상속값.**

## ★★ 140 vs 175 = 재료 차이가 아니라 출처-방법 artifact

| | 우리 NMC811 = 140 | Kang NCA = 175 |
|---|---|---|
| 정체 | **이차입자 나노인덴테이션** 앵커 (Xu 2017, fracture_model.py:20) | **치밀 결정-수준 FEM 가정** |
| 같은 급 비교 | 이차입자 NMC532 = 142.5±11.3 (Xu/de Vasconcelos/Zhao) | 치밀 펠릿 NMC111 199±12 (Cheng JECS 2017) · LCO 191 (Cheng JACS 2017) · NMC532 소결 177.5±19.5 |
| 조성 물리 | — | **MD/DFT: Ni↑ → E↓** (Haq&Lee 2025; Jahn-Teller) → NCA(Ni0.88)는 같은 미세구조 수준에서 NMC811 **이하**여야 |

⇒ 140 옆에 175를 그대로 배선하면 **가짜 25% 강성 대비**를 코드에 넣는 것.  둘은 서로 다른 미세구조
수준의 숫자다 (Joule 리뷰 envelope 80–200 GPa; 탈리튬 시 −50~60% 연화 별도).

## 물성별 verdict 표 (전 출처 명시)

| 물성 | Kang 사용값 | 그 출처 | 독립 문헌 | 스프레드 | **verdict** |
|---|---|---|---|---|---|
| **E(NCA)** | 175 "assumed" | Koerver 2018 (umbrella) | NCA-전용 측정 **부재**(진짜 gap).  프록시: 치밀 175–200 / 이차입자 130–155 (Cheng ×2, Stallard Joule 2022, Xu/Zhao) | 큼 | **배선 금지(재료값으로는)** — 프리셋 E=140 유지(이차입자 동급, Ni-트렌드상 ≤NMC811); 175는 "Kang-FEM 패리티" 명시 override로만 |
| **σ_e(NCA)** | 1 S/m (무인용) | — | **Amin/Chiang JES 2015**(소결 펠릿): 리튬화 **1e-4** → 충전끝 **1e-2 S/cm** (SOC 2자리 스윙); NMC333 대비 리튬화-상태 ~10³× 높음 = NCA가 실제로 고전도 계열 | 1e-4–1e-2 S/cm | **use-with-caveat**: 1 S/m = **충전-상태 상단**(Amin) — 프리셋 기본 0.01 S/cm + SOC-창 명시; 리튬화-상태 비교엔 1e-4 |
| **D_s(NCA)** | 3e-14 m²/s | Yu 2023 P2D | GITT max 1e-14 (SciRep 7:s41598-017-01657-9), 최적화 NCA 4.4e-15; 스프레드 1e-15–1e-14, 저SOC서 급락 | ~10× | **use-with-caveat**: fast-end(P2D 계보, 우리 NMC 기본과 동일값) — 비교용 OK |
| **ρ(NCA)** | (c_max 48000 → ~4.6 시사) | Yu 2023 | vendor true 4.45 (Sigma 760994·MSE); 결정학 유도 ~4.75 (R-3̄m 격자, 자체 유도 — 명시 Rietveld 인용 대기) | 4.45–4.75 | **use-with-caveat**: 결정-수준 4.75(우리 NMC 4.8 규약과 동급) 채택, vendor 4.45 병기 |
| **K_IC(NCA)** | (미사용; γ=1 J/m² 차용) | Boyce 2022(NMC 모델) | NCA-전용 **부재**.  층상산화물 서로게이트 0.1–0.5 MPa·m^½ (NMC ~0.1 EML; LMO 0.49→0.26 SoC-연화); Kang G_c=1 J/m²+E175 → K_IC≈0.42 정합 | 0.1–0.5 | **needs-lab**: Auerbach엔 서로게이트-밴드 태그로만, 배선 보류 |

E_LPSCl 22.1(Kang) = Bazzoun 22.1·우리 24와 정합 ✓ (교차확인 목적 달성).

## 배선 결정 (§F1)

**지금 배선 (검증 통과):**
- `mpm_webapp_payload.py --cam {nmc811,nca}`: nca → σ_e(AM) 기본 **0.010 S/cm 단일값**(S=P — NCA
  단결정/다결정 분리 데이터 부재 플래그; Amin 2015 충전-상단 태그, 리튬화 1e-4 캐비엇 meta 기록).
  사용자가 --sigma-am-s/-p 명시하면 그게 우선.
- D_s: step4 `--d-s` 기본 3e-14 그대로 = NCA와 동일값 (출처 태그만 doc).
- ρ: 코드 상수 4.8(porosity 폼) vs NCA 4.75 — 차이 1% 미만 = 폼 잔차(±2.3%p) 아래 → 유지 + 본 doc 기록.

**배선 안 함 (근거 부족/gap):**
- **E=175** — 위 artifact 판정.  DEM/fracture/MPM 전부 **140 유지**.  Kang-FEM 재현이 필요할 때만
  해당 도구의 E 인자에 175를 **명시적으로**(라벨과 함께) 넣는다.
- K_IC(NCA), NCA 단결정/다결정 σ_e 분리, σ_e 폼 σ_AM 재보정(corpus 필요 = WSL) — pending.

**남은 확인(수동):** Koerver 2018 원문(랩 접근)에 175가 실제로 등장하는지 — RSC 403으로 이 세션
미확인 (등장해도 '문헌-수집 값'이지 측정 아님이 유력).

## 한 줄 결론
NCA 프리셋의 정직한 형태 = **"σ_e/D/ρ는 SOC-창·계보 태그와 함께 채택, E는 140 유지(가짜 대비 차단),
K_IC는 gap 선언"** — 175를 그대로 넣었다면 §F1 위반이 될 뻔한 것을 교차검증이 막았다.
