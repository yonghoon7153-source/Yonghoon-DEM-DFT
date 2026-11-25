---
title: "회신 R — Stage 0 NO-GO: 재심사 조건 8 (U_eff 자료부재 · 기체상 retention 자명 · conditioning 오염)"
date: 2026-08-28
updated: 2026-08-28
tags: [review, codex, sdcp, reopen, stage0, verdict]
status: 접수 — 구현 중
confidence: high
verificationStatus: verified
verifiedAt: 2026-08-28
verifiedBy: codex
explored: false
authoredBy: human
effort: max
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 회신 R (2026-08-28) — 원문 보존

> 요청: `kb/reviews/codex_R_prompt_doped_reopen_v2_2026_08_28.md` · 대상: 재개 설계 v2 (커밋 4d74088 고정)
>
> **판정: Stage 0 NO-GO (v2 그대로 실행 금지) · 재개 방향 자체는 승인 · 재심사 조건 8.**
> 반영본: v3 카드 `kb/questions/sdcp_doped_reopen_v3_2026_08_28.md` + 빌더 manifest v2.

원문 그대로 (전사 수정 없음):

---

Stage 0: **NO-GO — 현재 v2 그대로는 계산 실행 금지.**
다만 재개 방향 자체는 승인한다. 아래 P0는 계산 결과로 보정할 수 없는 설계 결함이며, 이를 카드와 manifest에 반영하면 기체상 microstate 탐색으로 다시 GO 심사를 받을 수 있다.

## 먼저 — 묻지 않았지만 실행을 막는 P0 세 건

1. **`U_eff`를 계산할 자료가 없다.** 어느 n에도 E(0),E(+1),E(+2)가 모두 없다. 특히 DP6/+1이 누락됐다. 더구나 두 탈양성자화 위치 a,b가 비등가이면 U_eff(a,b) = E_+2(a,b) + E_0 − E_+1(a) − E_+1(b) 이며, 단순한 2E(+1)은 두 +1 상태가 등가일 때만 맞다. DP6/+1 위치별 잡을 추가하거나 `U_eff`를 v2에서 삭제해야 한다.

2. **기체상 `carrier_retention`은 현재 정의대로면 자명하다.** 기체상에서는 분자 조각이 전체 계다. 전 원자의 전하를 합하면 Q=0, 순스핀은 지정 다중도로 고정된다. 특히 closed-shell/BS singlet는 모두 순스핀 0이다. 따라서 Z5는 carrier retention을 측정하지 못한다. Stage 0 관측량은 `carrier_localization_profile`로 바꿔 백본·술포네이트 사이의 분포를 봐야 한다.

3. **conditioning에 realized 결과가 섞였다.** `backbone hole m`, `bipolaron`, `2-polaron`은 입력 화학종이 아니라 계산 후 판정할 결과다. 입력에는 `formal_oxidation_count=m`, RKS/UKS/BS ansatz와 seed만 기록하고, 실제 hole 위치와 polaron/bipolaron 판정은 `realized`로 내려야 한다.

## 1. 조건 ① 화학종 확정 — P0

빌더가 나중에 계산하는 것만으로는 확정이 아니다. 카드의 독립 기대값이 있어야 빌더 오류를 잡을 수 있고, 어느 SO₃H의 H를 제거했는지도 종 정의에 포함돼야 한다.
선형 n-mer의 기대식: C_{11n} H_{14n+2−m} O_{6n} S_{2n}, Q=0, N_e = 160n+2−m.

| 종 | 정확한 분자식 | 전전자 수 | ORCA 상태 |
|---|---|---:|---|
| S1 | C₃₃H₄₃O₁₈S₆ | 481 | multiplicity 2, Nα−Nβ=1 |
| S2 | C₄₄H₅₇O₂₄S₈ | 641 | multiplicity 2 |
| S3 | C₆₆H₈₄O₃₆S₁₂ | 960 | RKS singlet / UKS triplet / UKS-BS M_s=0 |
| N1 | C₃₃H₄₄O₁₈S₆ | 482 | singlet |
| N2 | C₄₄H₅₈O₂₄S₈ | 642 | singlet |
| N3 | C₆₆H₈₆O₃₆S₁₂ | 962 | singlet |
| 누락된 DP6/+1 | C₆₆H₈₅O₃₆S₁₂ | 961 | doublet |

`M=1`은 자기모멘트와 multiplicity 중 무엇인지 모호하므로 machine manifest에서는 금지해야 한다. `net_charge`, `multiplicity`, `n_alpha_minus_beta`, `wavefunction_class`를 따로 둬야 한다. VASP의 NELECT는 POTCAR valence와 연결되므로 `all_electron_count`와 `vasp_nelect + POTCAR hash`도 분리한다.
또한 `DP3/+1`은 알짜전하 +1로 오독되기 쉽다. machine ID는 `DP3_h1_Q0`처럼 바꾸는 편이 안전하다.
"counterion 없음"은 다음처럼 고치면 화학적으로 허용되는 이상화다: 외부 이동성 counterion은 포함하지 않고, m개의 tethered SO₃⁻가 formal backbone oxidation +m을 내부 보상하는 조건부 microstate. 살아남는 결론은 "이 특정 내부보상 microstate에서의 carrier localization"이다. 실제 재료 평균, 절대 흡착값, counterion을 넘는 순위는 살아남지 않는다.

## 2. S1/S2 bracket — P1, 도핑률 효과로 쓰면 P0

DP3/+1은 33.3%이지 35%가 아니다. 따라서 S1/S2는 25–35%의 양끝을 bracket하지 않고, 범위 안의 **25%와 33.3% sentinel point** 두 개다. 정확한 35% 정수 모델은 최소 DP20/+7이다.
DP3/+1↔DP4/+1은 사슬 길이와 hole fraction을 동시에 바꾼다 — 차이를 도핑률 효과로 귀속할 수 없다. 값싼 제한 설계: DP3/+1↔DP6/+2(같은 33.3% finite-size) · DP6/+1↔DP6/+2(같은 n 에서 hole-number) · 필요시 DP4/+1↔DP8/+2 · 정확 비교는 DP12/+3↔DP12/+4. DP12가 과하면 S1/S2를 유지하되 "도핑률 bracket"과 causal attribution을 모두 철회하면 된다.

## 3. S3 스핀 섹터 규약 — P0

한 상태에서 최적화한 기하를 공통 vertical 기하로 쓰면 그 상태를 구조적으로 편든다. conformer와 탈양성자화 위치쌍마다: ① 대응 N3 기하에서 지정 산성 H 두 개를 제거하되 추가 이완하지 않은 R⁰_kp 를 만든다 ② 동일 R⁰_kp 에서 S3a/RKS, S3b/UKS-triplet, S3c/UKS-BS 를 모두 계산 ③ state existence·stability 통과 상태만 각각 최적화 ④ 공통기하 vertical 표와 상태별 adiabatic 표 분리 ⑤ 필요시 각 상태 최적기하에서 경쟁 상태 교차 단일점.
S3a는 `RKS closed-shell candidate`, S3c는 `BS M_s=0 determinant, nominal OSS candidate`로 불러야 한다.
BS 의 ⟨S²⟩만 보고 raw E_BS 를 singlet 에너지로 쓰는 것은 불가. paired high-spin triplet 과 함께 raw energy, ⟨S²⟩, 국소 signed spin, UNO/UCO 를 기록하고 Yamaguchi AP 를 민감도 값으로 병기. 단 Yamaguchi 는 두 개의 유효 spin center 가 식별될 때만 — 여러 중심이면 `NA_SPIN_MODEL_NOT_IDENTIFIED`. 정밀 S–T gap 이 결론을 지배할 때만 spin-flip/multireference 를 다음 단계로.

## 4. carrier_retention 정의 — P0

Stage 0 과 slab 에서 서로 다른 두 관측량:
**Stage 0 `carrier_localization_profile`** — manifest 에서 원자 집합 고정(conjugated backbone / 각 tethered sulfonate / 나머지 side chain), 방법별로: 집합별 charge·signed spin · Σ|m_i| (BS 상쇄 전 국소스핀) · spin/charge centroid 와 participation ratio · BLA/quinoid order parameter · UNO occupation 기반 unpaired 지표. Löwdin·Hirshfeld 방향 일치는 강건성 진단이지 carrier 의 유일한 정의가 아니다.
**Slab `carrier_retention_change`** — Δq_M^A = q_M^A(complex) − q_M^A(isolated doped fragment; frozen adsorbed geometry). 같은 셀·Hamiltonian·분할법. Bader/DDEC 병기 + spin-density difference. 의미·atom-map·paired-reference 규약은 지금 고정, 구현은 Stage 0 뒤. Stage 0 결과를 slab retention 으로 부르는 것 금지.

## 5. Z1–Z5 과부족 — P0

conformer=2·거리 2종은 pilot 최소치이지 수렴 규칙이 아니다. 필수: DP3/+1 end/middle 패턴 · DP4/+1 end/inner · DP6/+2 짧은·중간·긴 위치쌍 + symmetry-distinct (이상적 reflection 만으로도 15쌍·9 class) · seeded vs realized spin-centroid separation 별도 기록 · 전 스핀 섹터 동일 conformer·seed 예산 · adaptive stopping rule (새 batch 에 저에너지 구조·상태순서·localization 결론이 안 바뀔 때 정지).
"ωB97X-D급"은 재현 불가 — functional·basis·dispersion·grid·SCF·ORCA 버전, decision set, r²SCAN orbital 미승계 fresh-start, 갈리면 `METHOD_DEPENDENT`(평균 금지)를 계산 전에 지정.
U_eff 유지하려면 DP6/+1 위치별 추가, 아니면 삭제. 힘 수렴만으로 adiabatic minimum 이라 부르지 않는다 — 결론 지배 최소점은 Hessian/불안정모드 재최적화 확인 (전 conformer full frequency 는 P2).

## 6. G5′의 30 meV — P1

동의 — Stage 0 blocker 아님. 단 **slab 진입 전 필수 게이트**: 수치수렴(cutoff·k·smearing·LREAL·vacuum) / magnetic basin / multistart·relaxation / method / reference-equivalence 를 분리한 envelope. 동일 계산 반복은 replicate 가 아니다 — 억지 CI 금지. 전 branch 부호 일치 + envelope 초과일 때만 판정, 아니면 NO_VERDICT.

## 7. 남은 ensemble→microstate 오류 — P0

v2 에도 남아 있다: 탈양성자화 위치 class (DP3 end/middle 등) · DP6/+2 의 9 symmetry class · conformer·spin state 분기 · counterion stratum · 표면의 pose·coverage·basin. SCF seed 도착 횟수는 물리적 population 이 아니고, 최저 s* 도 유한온도 ensemble 평균이 아니다.
최소 machine ID: microstate_id = (DP, formal_hole_count, removed_H_indices, external_counterion_inventory, conformer_cluster, wavefunction/spin_sector, localization_seed, realized_localization, pose, slab_basin). microstate 별 값 + 관측 범위로 보고. 정당한 자유에너지·prior 없이 Boltzmann/"평균 SDCP" 금지.
EPR 은 unpaired spin 만 직접 센다 — spin-silent bipolaron 총량은 단독으로 못 준다. **정량 EPR + 독립 total carrier/oxidation 측정을 paired requirement 로** 묶어야 분율 추론 가능.

## 실행 재심사 조건 (여덟 전부 반영 전 Z1 도 금지)

1. 정확한 분자식·전자수·Q·multiplicity·wavefunction class·removed-H atom ID 고정
2. `backbone hole/bipolaron`을 conditioning 에서 제거
3. DP6/+1 추가 및 위치별 U_eff 정의, 또는 U_eff 삭제
4. Stage 0 `carrier_localization_profile`과 slab `carrier_retention_change` 분리
5. state-neutral vertical geometry 와 BS/HS/AP 규약 고정
6. adaptive conformer·deprotonation-pattern·polaron-separation 탐색 규칙
7. 정확한 range-separated hybrid method 와 decision set
8. 모든 결과가 conditional microstate 결과임을 스키마와 허용문장에 고정

이 여덟을 반영하면 **기체상 microstate/method mapping 으로는 GO 가능**. 평균 재료 판정·slab 실행 승인 아님 — slab 전에는 carrier boundary 와 DFT 전용 판정바닥 별도 승인.
