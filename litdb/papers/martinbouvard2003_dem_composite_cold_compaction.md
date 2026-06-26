# 연질+경질 분말 혼합물의 냉간 압밀을 DEM으로 — Martin & Bouvard (Acta Materialia 2003)

> slug `martinbouvard2003_dem_composite_cold_compaction` · DOI `10.1016/S1359-6454(02)00402-0` · type `DEM` · PDF `Martin_Bouvard_2003_ActaMater_DEM_cold_compaction_of_composite_powders.pdf` · digested `2026-06-23` · status ✅

## 1. 한 줄 요약
**연질(소성)+경질(탄성) 단분산 구 4000개를 주기 RVE에서 DEM으로 냉간 압밀**하여, 경질 입자가 압밀을
저지하는 두 메커니즘 — (i) 경질-경질 네트워크의 하중 분담(force network)과 (ii) "excluded volume"을
채우기 위한 연질 입자의 추가 변형 — 을 정량 분리한 **복합분말 압밀 DEM의 기초(foundational) 논문**.
우리의 AM(rigid)+SE(soft) 복합 양극과 정확히 같은 hard+soft 구도이지만, **소성을 입자 SHAPE-흐름이 아닌
Storåkers 소성-들여쓰기 CONTACT 법칙(δ-overlap 프록시)으로만** 다룬다는 점이 핵심 한계.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| C.L. Martin, D. Bouvard (Lab. GPM2, INPG–CNRS, Grenoble, France) | Acta Materialia **51** (2003) 373–386 | 10.1016/S1359-6454(02)00402-0 | **모델 소재** (특정 SE/CAM 아님): 연질 = 이상소성/경화 금속(E₁=120 GPa, "Al/Pb/Cu류"), 경질 = 강체급 탄성(E₂=10E₁) | DEM (3D, periodic, 4000 spheres) — 압밀 곡선·배위수·접촉력 분포·구속계수 |

> ⚠ 이 논문은 **금속분말 야금(MMC, metal-matrix composite) 맥락**의 일반 hard+soft 모델 논문이며 ASSB/LPSCl/NMC가 아니다. 우리에게 의미 있는 것은 **소재 절대값이 아니라 hard+soft 압밀의 메커니즘·구조 추세**(우리 AM+SE의 직접 기하 유비). 모든 절대값은 무차원화(Σ₁, K_h)되어 있어 그대로 전이 불가, 추세만.

## 3. 핵심 물성 (수치)
| 물성 | 값 | 조건 (P, 조성) | stated/digitized | 비고 |
|---|---|---|---|---|
| porosity / 상대밀도 | **초기 D₀ ≈ 0.637** (경질 유무 무관), 압밀 **D ≤ 0.95**까지 계산 | isostatic & close die | stated | 초기 D는 hard fraction에 "강하게 영향받지 않음"(0.637) |
| 배위수 Z (초기) | **≈ 6.2** (복합·균질 동일) | D₀≈0.637 | stated | RCP 단분산 구 일반값 6.2와 일치 |
| 배위수 Z (식) | Z = Z₀ + C[(D/D₀)^(1/3) − 1], **Z₀=7.3, C=15.5, D₀=0.64** | Mason 27 실험 피팅(eq 17) | stated | eq 18: Z=12D (Helle/Arzt). DEM이 eq 16–18 검증 |
| 구속계수 K_h (isostatic) | **≈ 1.3 (20 vol% hard) / 1.8 (40 vol%)** (DEM, μ=0.1, 1/m≈0.2–0.4) | D≈0.80–0.85 | stated/digitized | 실험(Table 1)과 정합: 1.3 / 1.7–2.0 |
| 구속계수 K_cd (close die) | **≈ 1.3 (20%) / 1.6 (40%)** | D≈0.80–0.85 | stated/digitized | K_cd ≤ K_h (close die가 추가 재배열) |
| N₂₂/N₁₁ (경질-경질/연질-연질 힘비) | **~3.5 (40%), ~2 (20%)** 마찰접촉; **~1.0–1.3** 무마찰 | vs Φ₂, frictionless vs μ=0.1 | digitized (Fig 6b) | Zavaliangos 결정격자 4.4(20%)/9.6(40%)보다 훨씬 작음 |
| N₁₂/N₁₁ (연질-경질/연질-연질) | **~1.0–1.27 (40%까지)** | vs Φ₂ | digitized (Fig 5/6a) | 마찰 영향 거의 없음(연-경 강성 = 연-연) |
| 연질 추가 들여쓰기 h | 연-경 접촉의 h가 균질 대비 **20–40 % 더 큼** | f₂=40% | stated | "excluded volume" 추가변형의 직접 신호 |
| σ_y / E / ν | 연질 E₁=**120 GPa**, ν₁=**0.34**; 경질 E₂=10E₁(=1200 GPa), ν₂/ν₁=1; Σ₂/Σ₁=**10⁴** | 모델 입력 | stated | Σ₁=연질 소성응력 파라미터(eq 1), 무차원 정규화 기준 |
| 경화지수 1/m | **0, 0.2, 0.4** (1/m=0 = 이상소성) | 파라미터 스윕 | stated | m=∞ 이상소성, m=1 선형경화; c(m): 0.5(선형)→1.45(이상소성) |
| 마찰 μ_pq | **0 또는 0.1** (Coulomb), 회전 **없음** | 3가지: 무마찰 / 연-연만 0.1 / 전부 0.1 | stated | 회전 무시 → 재배열 상한 추정 |
| Heckel P_y / knee | **n/a** (Heckel 분석 안 함; P/Σ₁ vs D 곡선 제시) | — | — | 우리 Heckel과 직접 대응 곡선 없음(무차원 P/Σ₁) |
| PSD (D10/D50/D90) | **n/a** (단분산 monosize, 연·경 같은 크기 → 크기효과 배제) | — | stated | "no size effect introduced" — Bouvard&Lange[2]가 크기비 담당 |

## 4. 시뮬레이션 방법 ★
- **code / version**: **in-house DEM** (LIGGGHTS/Rocky 아님). Cundall & Strack[22] explicit scheme. 방법 상세는 동저자 Martin–Bouvard–Shima [16](J. Mech. Phys. Solids)에 의존.
- **DEM 접촉법칙** ★ — **Storåkers 소성 들여쓰기 + Hertz 탄성 병렬, min으로 전환**:
  - 법선력 `N = −min(N_E, N_P)·n` (eq 5): 탄성 Hertz `N_E = E_pq·√r_pq·h^(3/2)` (eq 6)과 소성 `N_P` 중 **작은 쪽** 채택 (= 탄성으로 시작, 항복 후 소성 분기 — 우리 hooke/hysteresis와 같은 "탄성→소성 한계" 발상이나 식이 다름).
  - 소성 법선력 `N_P = π·Σ_pq·2^(1−1/m)·3^(1−1/m)·c(m)^(2+1/m)·r_pq^(1+1/m)·h^(1/m)` (eq 7, Storåkers et al.[18] 유사해; **무마찰 점탄소성 들여쓰기**, frictionless·obliquity 근사).
  - 접촉면적 `A = 2π·c(m)²·r_pq·h` (eq 8); **c(m)** = 면적↔들여쓰기 관계, Storåkers 표(0.5 선형경화 → 1.45 이상소성).
  - 변형률경화 소성칙 `σ_e = Σ_p·ε_e^(1/m)` (eq 1), m은 두 상 공통; 혼합접촉 `Σ_pq = (Σ_p^(−m)+Σ_q^(−m))^(−1/m)` (eq 4), `E_pq = (4/3)·[(1−ν_p²)/E_p + (1−ν_q²)/E_q]^(−1)` (eq 3), `r_pq = r_p·r_q/(r_p+r_q)` (eq 2).
  - **접선력**: sticking(상대접선변위 무시) **또는** gross sliding의 2상태. 슬라이딩 시 단순 Coulomb `T = −μ_pq·|N|·t` (eq 9). **회전 없음**(소성·고배위(6–10)가 회전을 억제한다는 논거; Redanz–Fleck[21]가 소성 시 회전기여 무시가능 확인).
- **재료 파라미터**: 연질 E₁=120 GPa, ν₁=0.34, Σ₁=정규화기준. 경질 E₂/E₁=10(주), ν₂/ν₁=1, Σ₂/Σ₁=10⁴(경질-경질 접촉이 **압밀 내내 탄성** 유지하도록 큰 값). E₂/E₁=100도 시험 → 거시응력 **<3 % 변화** ("경질상 탄성변형은 압밀에 무시할 기여").
- **bond/binder 모델**: 없음 (순수 hard+soft 2상; 바인더·소결목 없음).
- **MPM/continuum**: 없음 (순수 DEM). 단 §3–5에서 해석모델(Arzt/Helle eq 17–18 배위수, Storåkers eq 9 stress) 과 **DEM을 대조**해 해석식의 타당범위를 검증.
- **전달 솔버**: **없음** (이 논문은 순수 **역학** 논문 — σ_ionic/e/thermal 전혀 없음). frame[5] 기준 **MPM/역학 쪽 절반만 다루고 transport 절반은 부재**.
- **입자 처리** ★ (DEM판 "무질서 처리"):
  - **구만** (sphere only). "압밀 진행 시 접촉부에서 소성흐름으로 운반된 물질은 무시 → 입자는 접촉부에서 **단순 절단(truncated)된 구**로 취급" (명시적 가정). → **진짜 SHAPE 소성 흐름 아님**; bulge·재돌출 없는 **CONTACT 소성**(δ-overlap h가 소성 프록시).
  - **mono-PSD** (연·경 동일 크기 → 크기비 효과 의도적 배제). 크기비는 Bouvard&Lange[2] 별도 논문 담당.
  - **rigid 위치 + 소성 CONTACT** (Storåkers 들여쓰기). 인접 접촉 간 비간섭 가정 → **상대밀도 D ≤ 0.95**에서만 유효(접촉 impingement 무시 한계). 본문도 "기하·역학 제약상 0.85–0.90 이전만 엄밀 유효" 명시.
- **도메인/RVE / servo / seeds / 압력범위**: **주기 입방 RVE**, **4000 입자**. 거시변형률 텐서를 셀에 부과 `Δx_i = ε̇_ij·x_j·Δt` (eq 13), 변형률율 ε̇=10⁻⁴ s⁻¹. **nominal density upscaling**(질량 증폭)으로 Δt를 10⁻³ s급으로 키워 가속 — 평형 근접 체크 포함. 시간스텝 eq 10(Cundall) — 소성접촉 k(eq 11) vs 경질-경질 탄성접촉 k_22=E₂₂√(r₂₂h₂₂)(eq 12) 중 결정. f₂=10/20/30/40 vol% 각각 초기 무작위 패킹 준비(균질 샘플에서 연질을 경질로 무작위 치환 후 "한 접촉만 소성" 조건으로 재배열).
- **특이사항/튜닝**: (1) **경질상 강성은 거의 무관**(E₂/E₁ 10↔100에서 <3 %) → hard=강체 근사 정당. (2) 회전 무시 = 재배열 **상한** 추정(실제 회전 가능 시 더 무름). (3) **Φ₂ = f₂·D** (eq 15) = 압밀 진행에 따라 변하는 "compact 전체부피 대비 경질 부피분율" — 가로축으로 사용(Φ₂는 D와 함께 증가).

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1 | 두 구 p,q 접촉 기하 모식(Σ_p,E_p,ν_p / Σ_q,E_q,ν_q, overlap h, r_p/r_q) | Storåkers 소성접촉의 h-정의 = 우리 δ-overlap 대응 그림 |
| 2 | (a) f₂=30% 초기 패킹(D=0.64) (b) 0.90 압밀 후 — **경질=흰색, 연질=회색** | 우리 AM(rigid)+SE(soft) RVE 시각화와 1:1. 압밀 후에도 구형 유지(=SHAPE-흐름 부재 가시 증거) |
| 3 | Z vs D (f₂=0/10/20/30/40%, μ=0.1) + eq17(Arzt) + eq18(Helle) 비교 | **Z는 경질분율에 거의 무관**(균질곡선과 동일). 우리 coordination Z 검증: 재배열이 Z를 eq17 위로 올림 |
| 4 | Z_pq/f_q vs D — eq16(모든 Z_pq/f_q가 마스터곡선 Z로 collapse) 검증 | **Z_22/f_2만 마스터에서 약간 이탈**(경질이 서로 덜 들여쓰기 — excluded volume). 우리 AM-AM 접촉도 동일 예상 |
| 5 | N₁₂/N₁₁, N₂₂/N₁₁ vs D (**무마찰**, 20·40%) | 무마찰 시 힘비 ~1 부근, 뚜렷한 추세 없음 → 재배열 자유 시 하중 균등 |
| 6 | (a) N₁₂/N₁₁ vs Φ₂ (b) N₂₂/N₁₁ vs Φ₂ — 마찰 2조건(연-연만 0.1 / 전부 0.1) | ★ **핵심**: 경질-경질 마찰 도입 시 N₂₂/N₁₁ → ~3.5(40%). 우리 AM-AM 마찰·force-chain 직접 유비 |
| 7 | P/Σ₁ vs D (이상소성 연질, f₂=0/10/20/30/40%, μ=0.1) | 경질 ↑ → 같은 D 도달에 더 큰 P 필요. 우리 "stiffer/more-rigid → higher floor"의 force-network판 |
| 8 | K_h vs Φ₂ (isostatic, 마찰 2조건) + Storåkers[9] 모델(점선) | **K_h가 N₂₂/N₁₁ 추세를 그대로 복제** → 구속계수 상승 ⊃ force-network 효과. 우리 composite porosity 관계식에 hard-network 항 시사 |
| 9 | K_h vs Φ₂ (1/m=0/0.2/0.4) + 실험(Table 1) | **경화지수 1/m이 K_h에 큰 영향** = 연질의 추가변형(2번째 메커니즘) 신호. 1/m 0.2–0.4가 실험 정합 |
| 10 | K_cd vs Φ₂ (close die, 1/m=0/0.2/0.4) + 실험(Table 2) | K_cd ≈ 압밀 내내 일정(<40%); K_h는 증가 → close die가 추가 재배열 |
| 11 | σ₁₁/σ₃₃ (close die, 횡/축응력비) vs D (f₂=0–40%) | 초기 감소 후 증가, 경질분율 영향 작음. 우리 close-die 응력 이방성 참고 |

## 6. Post-processing ★
- **무엇**:
  - **배위수 Z 분해** Z, Z₁₁, Z₁₂, Z₂₂ + 정규화 Z_pq/f_q(eq 16 collapse 검증) + Arzt eq17 / Helle eq18 해석식 대조.
  - **접촉력 분포** N₁₁(연-연), N₁₂(연-경), N₂₂(경-경) 평균 + 비율 N₁₂/N₁₁, N₂₂/N₁₁(force-network 정량).
  - **거시응력** σ_ij = (1/V)Σ_c[(r_p+r_q−h)·N·n_i·n_j + (r_p+r_q−h)·T·t_i·t_j] (eq 14) — 접촉력·접촉텐서 합.
  - **구속계수** K_h(isostatic) = 복합압력/균질압력 @동일 D; K_cd(close die) = 복합 축응력/균질 축응력. **D≈0.80–0.85에서 평가**(모델 유효구간).
  - **추가변형 신호**: 연-경 접촉의 평균 들여쓰기 h를 균질과 비교(40%서 +20–40 %).
- **도구**: 자체 DEM 후처리(별도 OVITO/pymatgen 등 언급 없음). Fig 2 시각화는 자체 렌더.
- **수치화·플롯·기록 방식**: 모든 응력 **Σ₁(연질 소성응력 파라미터)로 정규화**, Φ₂(=f₂·D) 또는 D를 가로축. K_h/K_cd를 실험 Table 1/2(Turner-Ashby, Kim, Sridhar-Fleck, Lange, Martin)와 **D≈0.80–0.85에서 직접 수치 대조** → 1/m=0.2–0.4, μ=0.1에서 정합.

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`
| 항목 | 이 논문 | 우리 | 차이 / 이유 (rigid·plastic / 2D·3D / contact·shape / mean-field·continuum) |
|---|---|---|---|
| hard+soft 구도 | 경질(탄성, E₂=10E₁) + 연질(소성) | AM(rigid, 140 GPa) + SE(soft) | **개념적으로 동일** ✓ — 우리 AM=그들 경질, 우리 SE=그들 연질. 우리 기하 유비의 정전(canonical) |
| **소성 종류** ★ | **CONTACT 소성** (Storåkers 들여쓰기, 절단된 구, h=프록시) — **SHAPE-흐름 없음** | DEM=CONTACT(hooke/hyst, δ 프록시) / **MPM=진짜 SHAPE 소성**(부피보존 흐름) | 우리 DEM과 **같은 한계**(구만, 형상불변). 우리 MPM이 채우는 그 절반을 이 논문도 **못 함** → frame[5] 외부 확증 |
| 차원 | **3D** (4000 구, 주기) | DEM 3D / MPM 2D·3D | **3D 동일** ✓ (Varkey·우리 2D MPM과 달리 절대 스케일 차원문제 없음 — 단 소재가 모델금속이라 절대값 전이는 별개) |
| 전달(σ) | **없음** (순수 역학) | σ_ionic/e/thermal 삼중항 + Kirchhoff/Holm | 우리 transport 절반 완전 우위. 이 논문은 frame[5] **역학 절반만** |
| 압밀 메커니즘 분리 | **(1) hard force-network(N₂₂/N₁₁, K_h↑) + (2) soft 추가변형(1/m 효과)** 정량 분리 | 우리는 porosity·overlap·packing으로 통합 측정 | 그들의 **2-메커니즘 분해**가 우리 composite porosity 관계식 설계에 직접 시사(hard-network 항 + soft-hardening 항) |
| 경질 강성 영향 | E₂/E₁ 10↔100 → <3 % | 우리 AM=140 GPa rigid 가정 | **정량적 정당화 제공**: hard=강체 근사 OK. 우리 "AM load-shielding" 논거의 외부 근거 |
| K_h 절대값 | 1.3(20%)/1.8(40%) — 무차원, 모델금속 | 우리는 K_h 미산출(porosity@P 직접) | K_h는 **무차원 비**라 소재무관 추세지표 — 우리도 composite/pure 압력비로 뽑아 대조 가능(미실시) |
| Heckel | **없음**(P/Σ₁ vs D만) | 우리 DEM Heckel R²=0.965, P_y=138 | 직접 Heckel 대조 불가(무차원·금속) — 단 P/Σ₁ vs D 곡선 형태는 비교 가능 |
| 회전 | **무시**(상한 추정) | 우리 DEM 회전 포함(LIGGGHTS) | 우리가 더 현실적. 단 그들은 고배위(6–10)서 회전기여 작다고 논증 |
| 데이터 형태 | digitized(Fig 6–11) + 모델금속 | — | 절대값 전이 금지, **추세·메커니즘만** |

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① **우리 hard+soft = AM+SE 유비의 "정전(canonical) 문헌"**: 이 논문이 **경질(=AM)+연질(=SE) 압밀 DEM의 원형**이고, 우리 AM(rigid)+SE(soft) 양극이 정확히 같은 구도. **압밀 저지의 두 메커니즘 — (1) 경질 force-network 하중분담(N₂₂/N₁₁↑, K_h↑) + (2) 연질의 excluded-volume 추가변형(1/m·하드닝 의존)** — 을 우리 composite porosity **관계식의 두 항으로** 직접 채택 가능. 우리 CLAUDE.md "AM load-shielding"(rigid AM skeleton이 300 MPa를 지지, SE는 가볍게 하중)은 곧 그들의 **mechanism (1)** 의 우리판이고, 우리 MPM void-fill flow는 그들의 **mechanism (2)** 의 진짜-소성판이다.
- ② **경질 강성 무관(<3 %) = 우리 AM=140 GPa rigid 가정의 외부 정당화**: E₂/E₁를 10→100 올려도 거시응력 <3 % → "경질상 탄성변형은 압밀에 무시할 기여". 우리가 AM을 강체로 두고 SE만 연화(E_eff 1.35)하는 비대칭 처리가 **물리적으로 옳다**는 독립 근거. (우리 CLAUDE.md 1.75 % composite overlap ↔ 12 % pure-SE overlap = AM-shielding 정량과 같은 결론.)
- ③ **그들도 SHAPE-소성을 못 한다 = frame[5] 분업의 외부 확증**: 2003년 기초 DEM부터 2026 Varkey/Bazzoun까지, **모든 DEM이 "구만·절단된 구·δ 프록시"** 로 멈추고 진짜 형상흐름은 안 한다(이 논문은 "운반된 물질 무시 = 절단 구"를 **명시적으로** 가정). 우리 MPM(진짜 J2 흐름, SEM morphology)이 채우는 그 절반은 **DEM 계열의 구조적 공백**이지 우리만의 누락이 아니다. → frame[5](DEM=transport·packing / MPM=mechanics·morphology) 분업이 23년에 걸친 DEM 문헌의 일관된 한계로 재확인됨.

## 9. 인용 가능 문장 (deck/paper용)
- "The foundational DEM treatment of soft+hard powder co-compaction (Martin & Bouvard 2003) resolves two retarding mechanisms — a load-bearing hard-particle force network (N₂₂/N₁₁ rising to ~3.5 at 40 vol% hard with friction) and the extra indentation forced on the soft phase to fill the excluded volume around rigid inclusions (20–40 % larger soft–hard indentation at 40 vol%) — which map directly onto our AM(rigid)+SE(soft) cathode: AM load-shielding and SE void-filling, respectively."
- "Even this canonical DEM keeps particles as truncated spheres (plastic CONTACT, no shape flow), establishing that true plastic morphology is a structural gap of DEM across two decades — exactly the half our MPM supplies (frame [5])."
- "The macroscopic stress is insensitive (<3 %) to the hard-phase modulus over E₂/E₁ = 10→100, justifying a rigid-AM approximation in composite cathode DEM."

## 10. 주의/한계 (over-claim 방지)
- **소재가 ASSB 아님**: 일반 금속분말 야금(MMC) 모델 — LPSCl/NMC가 아니고 연질=E₁=120 GPa 금속. **모든 절대값 무차원(Σ₁ 정규화)** 이라 우리 LPSCl(E_eff 1.35 / real 24)·NMC로 **절대 porosity·압력 직접 전이 금지**. 가져올 것은 **메커니즘·구조 추세·무차원 비(K_h, N₂₂/N₁₁, Z)** 뿐.
- **CONTACT 소성만** (Storåkers 들여쓰기) — 입자는 "접촉부에서 절단된 구"로 **명시적 가정**, 소성흐름으로 운반된 물질 **무시**. → 진짜 SHAPE 변화·bulge·void-fill 흐름 없음. 우리 MPM과 직접 비교 시 "이 논문은 우리 DEM과 같은 쪽(CONTACT 프록시), 우리 MPM(SHAPE-흐름)은 다룸"을 명시.
- **상대밀도 D ≤ 0.95(엄밀히는 0.85–0.90)** 까지만 유효 — 인접 접촉 비간섭·구절단 기하 가정 붕괴. 고밀도(우리 90 %+ 압밀)에는 외삽 주의. **~20 % porosity 강체-구 floor** 논의와 정합(소성흐름 없이는 못 넘음).
- **회전 무시** = 재배열 **상한** 추정 → 실제(회전 가능)는 더 무름. 우리 LIGGGHTS(회전 포함)와 절대 비교 시 그들이 약간 빡빡한 쪽.
- **monosize**(연·경 같은 크기, 크기효과 의도적 배제) → 우리 12:4:1 bimodal Furnas packing·dip은 **이 논문 범위 밖**(크기비는 Bouvard&Lange[2] 별도). 우리 dip을 이 논문으로 뒷받침 불가.
- **digitized 값**(Fig 5–11의 N비·K_h·K_cd·σ비)은 추세 ±만, stated 텍스트값(Z₀=7.3, C=15.5, D₀=0.64, K_h≈1.3/1.8, E₂/E₁=10, 1/m=0/0.2/0.4)과 구분.
- **전달(σ) 전무**: frame[5] 기준 **역학 절반만** — 이 논문으로 우리 σ_ionic/e/thermal 어느 것도 검증·보강 불가(Bazzoun이 그 역할).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
