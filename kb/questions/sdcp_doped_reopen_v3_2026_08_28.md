---
title: "sdcp_doped 재개 설계 v3 — 회신 R 재심사 조건 8 반영 (Stage 0 재심사용)"
date: 2026-08-28
updated: 2026-08-28
tags: [sdcp, estimand, reopen, stage0, microstate, design]
status: active
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-primary
---

# sdcp_doped 재개 설계 v3

> v2 는 회신 R 로 **Stage 0 NO-GO** (재개 방향은 승인, 재심사 조건 8). 이 v3 가 그 여덟을
> 구현한다. 구현의 절반은 문서가 아니라 **빌더에 있다** — `tools/sdcp/build_v7c_trimer.py`
> manifest v2 (selftest 23건이 조건 1·2·3·4·7·8 의 기계 측 준수를 봉인).
>
> ⛔ **R2 (재심사) GO 전에는 Z1 도 실행하지 않는다.**

## 🔴 회신 R2 판정 (2026-08-28) — NO-GO → **최소수정 8 구현 완료, R3 대기**

원문: `kb/reviews/codex_R2_doped_reopen_v3_reply_2026_08_28.md`. 리뷰어가 커밋 b3ff72de 를
**직접 실행**해 산출물을 감사했다 — "23 PASS 는 문자열 selftest 이지 e2e 증명이 아니다."
빌더를 stage A/B 아키텍처로 재작성했다 (selftest 27건 · 음성 9종). 이 카드에서 바뀐 것:

- **종 명칭 정정 (조건 1)**: DPn_hm_Q0 = **neutral-H-deleted / internal-redox microstate**
  — Q=0 에서 H 핵+전자를 함께 제거한 종이므로 일반적 "탈양성자화" 가 아니다.
- **U_eff → U_PCET 개명 (조건 3·7)**: `U_PCET(a,b) = E[h2(a,b)] + E[h0] − E[h1(a)] − E[h1(b)]`
  — 균형 반응 h1(a)+h1(b)→h0+h2 의 에너지다. **핵 조성이 함께 변하므로 순수 Hubbard U/
  hole-pairing 이 아니다.** vertical 과 adiabatic 을 별도 표로, 혼합 금지. 순수 pairing 은
  동일 h2 조성 안의 sector 에너지차로 별도 판정.
- **매트릭스에 off-center hBC 추가 (Q2)** — dp6 pairs = CD·BE·AF·**BC**. reflection 9 class
  주장 철회 (조립 사슬은 B≢E·C≢D — label pair 15개가 맞다). **A,F 는 섹터 비교 전용**:
  U(AF)·거리 추세·부호 일반화 주장 금지, 필요 시 hA·hF 자동 승격.
- **h1 vertical 통일 (Q3)**: R⁰_k 마다 h0/h1(a)/h1(b)/h2(a,b) 네 leg 를 같은 좌표 프레임으로.
- **seed 바닥 (Q4)**: DP3/4 = 초기 4 + null K=2 ×2 (최소 8) · DP6 = 초기 8 + null ×4 (최소 16).
  변화 시 null counter 리셋 · 전 섹터 동일 geometry seed set · geometry/SCF seed 분리
  (`SEED_FLOOR` — manifest 에 선언) · --step 은 seed 아님.
- **ID 분리 (조건 8)**: `calculation_id` = conditioning 만의 불변 해시 (realized 유입 시 발급
  거부) / `realized_state_id` = analyzer 가 사후 발급.
- **analyzer (조건 5)**: `--analyze` 가 abort code 7종을 실제 emit — SCF_UNCONVERGED ·
  SECTOR_MISMATCH(HFTyp·⟨S²⟩) · SPIN_CONTAMINATION_UNREPORTED · NA_STATE_NOT_IDENTIFIED
  (BS 플립 실패) · STABILITY_UNSTABLE (opt 진행 차단). 음성 e2e 4종이 selftest 에 있다.
- ⚠ 남은 미구현 (정직 목록 — R3 에 명시): carrier_localization_profile 의 수식·class 경계·
  index-remap validator (조건 4 P1) · adaptive stopping 자동화 · Yamaguchi AP 산출.
  전부 "빌더가 못 하는 것" docstring 에 등재.


## 왜 중요한가

doped 재개의 첫 관문(Stage 0 기체상)이 설계 결함으로 막혀 있다. 회신 R 의 P0 들은
"계산 결과로 보정할 수 없는" 종류 — 던지기 전에만 고칠 수 있다. 이 카드가 통과해야
아홉 번째 실패 없이 첫 계산이 나간다.

## A. 화학종 — **카드의 독립 기대값** (조건 1)

닫힌꼴: 선형 n-량체 **C₁₁ₙH₁₄ₙ₊₂₋ₘO₆ₙS₂ₙ · Q=0 · Nₑ = 160n+2−m**.
빌더가 이 식과 다르게 산출하면 **빌더가 틀린 것** — `check_closed_form` 이 멈춘다
(실물 다이머 실검증 selftest 포함: DP3_h1 → C₃₃H₄₃O₁₈S₆ · 481e ✓).

| machine ID | 분자식 | 전전자 | wavefunction_class · multiplicity · Nα−Nβ |
|---|---|---:|---|
| DP3_h0_Q0 (N1) | C₃₃H₄₄O₁₈S₆ | 482 | RKS · 1 · 0 |
| DP4_h0_Q0 (N2) | C₄₄H₅₈O₂₄S₈ | 642 | RKS · 1 · 0 |
| DP6_h0_Q0 (N3) | C₆₆H₈₆O₃₆S₁₂ | 962 | RKS · 1 · 0 |
| DP3_h1_Q0 (S1) | C₃₃H₄₃O₁₈S₆ | 481 | UKS · 2 · 1 |
| DP4_h1_Q0 (S2) | C₄₄H₅₇O₂₄S₈ | 641 | UKS · 2 · 1 |
| **DP6_h1_Q0 (S4 — v2 누락분)** | C₆₆H₈₅O₃₆S₁₂ | 961 | UKS · 2 · 1 |
| DP6_h2_Q0 (S3) | C₆₆H₈₄O₃₆S₁₂ | 960 | RKS·1·0 / UKS·3·2 / UKS-BS·(orca 3)·Ms=0 |

- **removed-H 원자 ID 가 종 정의의 일부다** — manifest `removed_H_indices` (중성 프레임).
- `M=1` 표기 금지 — `net_charge / multiplicity / n_alpha_minus_beta / wavefunction_class`
  네 필드 분리 (빌더 구현). 기체상은 `all_electron_count`; VASP 단계에서만
  `vasp_nelect + POTCAR hash` 별도.
- counterion 이상화 (회신 R 문구 채택): **"외부 이동성 counterion 은 포함하지 않고,
  m 개의 tethered SO₃⁻ 가 formal backbone oxidation +m 을 내부 보상하는 조건부
  microstate."** 살아남는 결론은 **이 내부보상 stratum 에서의 carrier localization** 뿐 —
  실제 재료 평균·절대 흡착값·counterion 을 넘는 순위는 살아남지 않는다.

## B. conditioning / realized 분리 (조건 2 — P0-3)

conditioning 에는 **ansatz 만**: `formal_oxidation_count=m · wavefunction_class ·
multiplicity · n_alpha_minus_beta · removed_H_indices · localization_seed`.
⛔ "backbone hole" · "polaron" · "bipolaron" 은 conditioning 금지 — **realized 판정**이다
(빌더 selftest 가 manifest 에 그 단어가 없음을 검사). 섹터 명칭:
S3a = `RKS closed-shell candidate` · S3c = `BS M_s=0 determinant (nominal OSS candidate)`.

## C. U_PCET — 위치별 정의 + DP6_h1 추가 (조건 3 · R2 개명)

```
U_PCET(a,b) = E[h2(a,b)] + E[h0] − E[h1(a)] − E[h1(b)]     (균형 반응 h1(a)+h1(b) → h0+h2)
```

⛔ **순수 Hubbard U/hole-pairing 이 아니다** — 네 leg 의 핵 조성이 함께 변한다 (R2 조건 3).
disproportionation/PCET 에너지로만 부른다. vertical(전부 R⁰ 프레임)과 adiabatic(각 leg
자체 최소점)을 **별도 표**로, 혼합 금지. 순수 pairing 은 동일 h2 조성 안 sector 차로 별도.

2E(+1) 근사는 두 +1 위치가 등가일 때만 — 조립 사슬은 비틀림이 달라 **B≢E, C≢D** 로
취급한다. Stage 0 매트릭스: **DP6_h1 singles hB·hC·hD·hE** + **pairs hCD·hBE·hAF·hBC**
(hBC = off-center, R2 Q2 — 기존 singles 재사용). U_PCET 는 CD·BE·BC 세 쌍에서 위치별로.
**(A,F) 는 섹터 비교 전용** — U(AF)·거리 추세·부호 일반화 주장 금지, 대상이 최저상태/
교차검사에 들면 hA·hF 자동 승격. 부수 효과: DP6_h1↔DP6_h2 = 같은 n 의 hole-number 축.

## D. 관측량 (조건 4)

**Stage 0 = `carrier_localization_profile`** (⛔ 기체상 carrier_retention 은 자명 — 폐기):
manifest 의 `atom_sets_neutral_frame` (backbone / sulfonate_X / sidechain_rest —
빌더가 고정, 전 원자 1회 분할 selftest) 위에서 방법별로:
- 집합별 charge · signed spin · **Σ|mᵢ|** (BS 상쇄 전 국소스핀)
- spin/charge centroid + participation ratio
- backbone BLA / quinoid order parameter
- UNO occupation 기반 unpaired 지표
Löwdin·Hirshfeld 방향 일치는 **강건성 진단**이지 carrier 의 정의가 아니다 —
구조(BLA)·orbital(UNO) 진단과 함께 셋이 한 몸.

**Slab = `carrier_retention_change`** (지금 규약 고정, 구현은 Stage 0 뒤):
```
Δq_M^A = q_M^A(complex) − q_M^A(isolated doped fragment; frozen adsorbed geometry)
```
같은 셀·Hamiltonian·분할법 (Bader/DDEC + spin-density difference 병기). 분자 atom-map 은
빌더가 고정. ⛔ Stage 0 결과를 slab retention 으로 부르지 않는다.

## E. S3 스핀 섹터 규약 (조건 5)

conformer × 탈양성자화 위치쌍마다:
1. **R⁰ₖₚ = N3 최적 기하에서 지정 산성 H 2개 제거, 추가 이완 없음** — 어느 상태의
   기하도 아니라서 편들지 않는다 (v2 의 "같은 기하 vertical" 은 이 점이 미정의였다).
2. 같은 R⁰ₖₚ 에서 s(RKS)/t(UKS)/bs(UKS-BS) 전부 단일점 → **vertical 표**.
3. state existence + SCF stability 통과 상태만 각자 최적화 → **adiabatic 표** (분리 보고).
4. 필요시 각 상태 최적기하에서 경쟁 상태 교차 단일점.
5. BS: raw E · ⟨S²⟩ · 국소 signed spin · UNO/UCO 기록. **Yamaguchi AP 는 유효 spin
   center 2개가 식별될 때만** 민감도 값으로 병기 — 다중 중심이면
   `NA_SPIN_MODEL_NOT_IDENTIFIED` (중단 코드, 빌더 등재). raw E_BS 를 singlet 에너지로
   쓰지 않는다. 정밀 S–T gap 이 결론을 지배할 때만 spin-flip/MR 을 다음 단계로.
6. 결론을 지배하는 최소점은 **Hessian 또는 불안정모드 재최적화**로 최소성 확인
   (전 conformer full frequency 는 P2).

## F. 탐색 규칙 (조건 6) — pilot ≠ 수렴

**Batch-1 (pilot)**:

| | 종 | 패턴 | 섹터 |
|---|---|---|---|
| N1–N3 | DP3/4/6_h0 | — | RKS |
| S1 | DP3_h1 | **hB(middle) · hA(end)** | d |
| S2 | DP4_h1 | **hA(end) · hB(inner)** | d |
| S3 | DP6_h2 | **hCD · hBE · hAF(섹터전용) · hBC(off-center)** | s/t/bs (vertical→adiabatic) |
| S4 | DP6_h1 | **hB · hC · hD · hE** | d |

- 전 섹터 **동일 conformer·seed 예산** (차별 배정 금지).
- `seeded_separation`(빌더 기록)과 **realized spin-centroid separation** 분리 보고.
- **adaptive stopping**: conformer batch(K=2)를 추가해 ① 최저에너지 구조 ② 상태 순서
  ③ localization class 셋 다 불변이면 정지, 하나라도 바뀌면 반복. DP6_h2 의 9개
  symmetry class 는 pilot 3쌍의 결론이 위치쌍에 민감하면 확장한다 — 2쌍/3쌍이
  ensemble 을 대표한다고 주장하지 않는다.

## G. 방법 (조건 7) — 재현 가능하게 고정

- 주 방법: **ORCA r²SCAN-3c · Opt · TightSCF · serial · maxcore 6000** (n-시리즈 동일).
- 교차검사 (빌더 `HYBRID_SPEC` 그대로): **ωB97X-D3 / def2-TZVP / defgrid3 / TightSCF ·
  fresh-start (r²SCAN orbital 미승계, MORead 금지)** · 대상 = vertical 승자 + adiabatic
  승자 + 0.10 eV 이내 경쟁 상태 · hybrid 가 state identity/localization/순서를 바꾸면
  그 경쟁 상태만 hybrid 재최적화 · 두 방법이 갈리면 평균 없이 **`METHOD_DEPENDENT`**.
- `orca_version` 은 회수 시 .out 배너에서 채운다 (사전 기재 금지).

## H. microstate 스키마 (조건 8)

빌더가 잡마다 발급 (`microstate_id`):
```
DP · formal_oxidation_count · removed_H_indices · external_counterion_inventory
· conformer_cluster · wavefunction_spin_sector · localization_seed
· realized_localization(사후) · pose(슬랩) · slab_basin(슬랩)
```
- 보고는 **microstate 별 값 + 관측 범위** 먼저. 정당한 자유에너지·prior 없이
  Boltzmann/"평균 SDCP" 서술 금지.
- SCF seed 도착 횟수 ≠ population · 최저 s* ≠ ensemble 평균 — 서술 금지 목록.
- **허용 문장 형식**: "이 [내부보상·DP·홀패턴·섹터] microstate 에서 …" — 조건 없는
  일반 문장은 만들지 않는다.

## Sentinel 정정 (회신 R 2번)

⛔ "S1/S2 = 25–35 % bracket" **철회**. 맞는 서술: **25 %(DP4_h1)와 33.3 %(DP3_h1)
sentinel point 두 개** — 사슬 길이와 hole fraction 이 함께 변해 **차이를 도핑률 효과로
귀속하지 않는다**. 분리 축은 DP3_h1↔DP6_h2(같은 33.3 % finite-size) ·
DP6_h1↔DP6_h2(같은 n, hole-number). 정확한 도핑률 대조(DP12)는 이번 범위 밖.

## Slab 진입 게이트 예약 (회신 R 6번 — Stage 0 뒤, slab 전 별도 승인)

- **DFT 전용 판정바닥**: UMA 30 meV 이식 금지. envelope = 수치수렴(cutoff·k·smearing·
  LREAL·vacuum) ⊕ magnetic basin ⊕ multistart/relaxation ⊕ method ⊕
  reference-equivalence — 각각 분리 측정. 동일 계산 반복은 replicate 아님 (CI 조작 금지).
  전 branch 부호 일치 + envelope 초과일 때만 판정, 아니면 NO_VERDICT.
- carrier boundary (분자/표면 경계) 규약 별도 승인.

## 실험 요청 — **paired requirement** (회신 R 7번 정정)

EPR 단독으로는 부족하다 — spin-silent bipolaron 총량을 못 준다.
**① 정량 EPR spin count ⊕ ② 독립 total carrier/산화도 측정** 이 **짝으로** 있어야
polaron/bipolaron 분율 추론 가능. ③ counterion 조성은 stratum 검증용 (별도).
둘 중 하나만 가능하면: 분율 추론 포기, 두 섹터 조건부 병기가 최종 형태.

## Evidence For

- 회신 R 의 여덟 조건이 각각 §A–H 에 1:1 매핑된다. 그중 1·2·3·4·7·8 은 빌더
  manifest v2 로 **기계가 강제**한다 (selftest 23건 — 닫힌꼴 실물 검증 · conditioning
  순수성 · atom_sets 완전분할 · 중단코드 · parity 가드 포함).
- 종 표의 전자수가 리뷰어의 독립 계산과 전 항목 일치 (481/641/960/961/962 등).

## Evidence Against — 남은 위험

- **conformer 대표성**: adaptive stopping 이 있어도 시작 batch 가 작다 — 정지 규칙이
  local trap 을 수렴으로 오판할 수 있다. 독립 torsion-seed batch 로만 완화된다.
- **BS 처리의 한계**: Yamaguchi 2-중심 조건이 실제로 성립 안 하면 (홀이 3+ 고리에
  퍼지면) S–T gap 은 이번 방법으로 못 정한다 — 그 경우가 오히려 물리적으로 그럴듯하다.
- **r²SCAN-3c SIE**: localization 질문 자체가 SIE 민감 — hybrid 와 갈리면
  METHOD_DEPENDENT 로 끝나는 시나리오가 실재한다 (그것도 결과다).
- DP6_h1 4잡 추가로 Stage 0 비용이 커졌다 (199원자 doublet ×4) — serial 데스크탑에서
  주 단위. 병렬화/우선순위는 GO 후 러너 설계에서.

## 결정 실험

§F Batch-1 (R2 GO 후에만). 판정: §E 규약의 vertical/adiabatic 표 + §D profile 이
방법 교차검사에 강건하면 slab 게이트 설계로 진행. METHOD_DEPENDENT / NA_* 가 나오면
그 지점에서 멈추고 조건부 보고.

## Status Log

- **2026-08-28** — v3 작성. 회신 R (NO-GO + 조건 8) 반영: U_eff 위치별 + DP6_h1 4잡 ·
  carrier_localization_profile 로 교체 · conditioning/realized 분리 · 닫힌꼴 독립
  기대값 + 빌더 실검증 · R⁰ state-neutral vertical 규약 · adaptive stopping ·
  ωB97X-D3 스펙 고정 · microstate_id 스키마 · sentinel 정정 · EPR paired requirement.
  빌더 manifest v2 구현 + selftest 23건 PASS. **다음: R2 재심사 발송 → GO 후 Z1.**
