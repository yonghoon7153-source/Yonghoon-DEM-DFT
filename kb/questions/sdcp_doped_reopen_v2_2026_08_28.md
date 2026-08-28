---
title: "sdcp_doped 재개 설계 v2 — 회신 O 재승인 조건 7 을 실제로 채우는 카드"
date: 2026-08-28
updated: 2026-08-28
tags: [sdcp, estimand, reopen, polaron, stage0, design]
status: active
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-primary
---

# sdcp_doped 재개 설계 v2

> **이 카드가 재개 그 자체다.** 마감 문서(`db/properties/sdcp_doped_closed_2026_08_28.json`)는
> 옛 프로토콜(n=1 단량체·wave1)의 숫자 생산만 잠근다 — 잠금은 이 카드의 조건들이 채워지는
> 순간 풀리게 설계돼 있다 (planned_upgrade_triggers). v1 카드는 회신 O 로 P0 전면 반려됐고
> (`kb/questions/sdcp_doped_estimand_2026_08_28.md` — 기록 보존), 이 v2 는 그 반려 사유
> 여덟 개를 하나씩 구현한다.
>
> ⛔ **순서 규율**: 이 카드 §A–D 가 리뷰(회신 R)를 통과하기 전에는 Stage 0 기체상도
> 던지지 않는다. 통과 전 계산 = 아홉 번째 실패 후보.

## 왜 중요한가

1저자 결정(2026-08-28): doped 는 버리는 게 아니라 **제대로 다시 한다**. 여덟 번의 실패는
전부 "잘못된 화학종(n=1)에 잘못된 질문(단일 E_ads)" 이었다는 것이 리뷰 3연속(M·N·O)의
결론이므로, 재개는 화학종과 질문을 바꾸는 데서 시작한다. 원고에서 doped 가 맡을 몫 —
"자가도핑 바인더가 표면에 붙을 때 캐리어를 유지하는가" — 는 이 캠페인의 차별점이라
포기 대상이 아니다.

## A. 화학종 선언 (재승인 조건 ①)

**구성 규칙** (정확한 원자수·NELECT 는 빌더가 계산해 manifest 에 고정한다 — 손으로 안 적는다):

```
DPn/+m ≡ n-량체(반복단위 C₁₁H₁₆O₆S₂, 연결부마다 −H₂)에서
         술폰산기 m 개를 H-원자 제거(H⁺+e⁻)로 탈양성자화한 알짜중성 종
         → 백본 홀 m 개 · 남은 SO₃H 는 양성자화 유지 · counterion 없음(자기보상) · Q=0
```

| 라벨 | 종 | 도핑률 | 스핀 섹터 (기대) |
|---|---|---|---|
| S1 | DP3/+1 | 33 % | doublet (M=1) |
| S2 | DP4/+1 | 25 % | doublet (M=1) |
| S3a | DP6/+2 **A6** | 33 % | closed-shell singlet bipolaron (M=0) |
| S3b | DP6/+2 **A7a** | 33 % | triplet 2-polaron (M=2) |
| S3c | DP6/+2 **A7b** | 33 % | broken-symmetry open-shell singlet (M=0, 국소 반대부호) |
| N1–N3 | DP3/0 · DP4/0 · DP6/0 | 0 % | closed-shell singlet — S 시리즈의 n-matched 대조 |

- S1↔S2 가 **조성 bracket** (25–35 % 실측 범위의 양끝. DP5 는 자동 필수 아님 — 회신 O).
- S3a/b/c 는 **같은 조성·같은 NELECT** 의 스핀 섹터 셋 — polaron/bipolaron 을 선험적으로
  고르지 않는다. vertical(같은 기하) 비교 먼저, adiabatic(각자 이완) 비교는 분리 보고.
- 교차 크기 비교는 직접 총에너지 금지 — **동일 N 의 U_eff = E(+2)+E(0)−2E(+1)** 만 보조로.
- reservoir: 종 간 열역학 비교가 필요할 때만 H-원자 저장소를 ½E(H₂)로 선언해 쓴다.
  E_ads 자체(고정 종)에는 불필요.

## B. estimand (조건 ②·③)

**주 estimand** — `E_ads^ad = E_C(s*) − E_S(B₀) − E_M(m₀)`, s* = **사전 선언된 탐색**
(multistart 프로토콜)에서 발견된 최저 복합체 상태. "전역 최소" 라 부르지 않는다.
**주 관측량**: 연속 `carrier_retention` — 분자 조각의 스핀·전하 적분 (Löwdin + Hirshfeld/
Bader 병기, 방법 태그 필수. 단일 분할법 스칼라로 판정하지 않는다).

**보조 estimand** — `ΔE_loc^vert` 는 **두 국소화 상태가 bias 제거 후에도 반복 재현될 때만**
연다. 한쪽이 서지 않으면 `ΔE_loc = NA_STATE_NOT_IDENTIFIED` 로 끝낸다 — 정의역이 빌 수
있음을 코드가 말하게 한다.

**conditioning / realized 분리** (회신 O 스키마 그대로):

```
conditioning:  formula·DP·protonation·counterion·Q·NELECT·hole_count ·
               geometry_hash·pose·cell·fixed_or_relaxed · Hamiltonian/protocol ID ·
               spin-sector 또는 constraint ID · slab-topology target
realized:      M_tot · q_mol[method]·m_mol[method]·carrier_fraction[method] ·
               per-Ni signed moment vector + flip indices · occupation fingerprint
```

## C. 게이트 v2 (조건 ④ — G1–G4 전면 교체)

| | 내용 | v1 에서 바뀐 것 |
|---|---|---|
| G1' | **state-selection policy 동일** — 한 estimand 안에서 전부 자유 바닥상태이거나, 선언된 채널과 양립하는 대응 제약. LREAL 등 수치 설정도 기준·대상 동일(all-F) | "같은 NUPDOWN 값" 폐기 |
| G2' | **계별 기대 스핀 표** (§A 표) + 경쟁 다중도 스캔 + SCF stability | "M≈1 범용" 폐기 |
| G3' | **분할법 강건성** — Löwdin·Hirshfeld/IAO 가 같은 우세 방향일 때만 분류. 스칼라 문턱 없음 | "50 % 문턱" 폐기 |
| G4' | **per-Ni signed moment vector + flip indices** 로 basin 식별. ⚠ carrier 이동이 만든 국소 Ni 변화는 **답일 수 있다** — basin 오류와 분리 판정 | "총자화 분류" 폐기 |
| G5' | 판정바닥 분리: 자리대비 30 meV(문서화된 UMA 유래 — DFT 전용 바닥은 미해결, `sdcp_site_preference` 카드) ↔ carrier-gap ↔ 사슬수렴 문턱은 **각각 따로 선언** | 단일 30 meV 혼용 폐기 |
| G+ | 빠졌던 P0 게이트: 원자·전자 보존 반응식 · 동일 Hamiltonian · SCF/힘 수렴 · conformer ≥2 · vertical/adiabatic 구분 · state-existence 재현성 | 신설 |

## D. 결정 실험 — Stage 0 (기체상, 조건 ⑤. **회신 R 통과 후에만**)

방법: ORCA r²SCAN-3c (desktop WSL — n-시리즈와 동일 프로토콜) + 핵심 상태는
range-separated hybrid(ωB97X-D 급) 교차검사 (회신 O: self-interaction 민감성).

| 잡 | 내용 | 조건 |
|---|---|---|
| Z1 | S1 (DP3/+1) — SO₃-seed / backbone-seed **fresh-start multistart** × conformer 2 | G2'·G3' |
| Z2 | S2 (DP4/+1) — 동일 multistart | S1↔S2 로 도핑률 bracket |
| Z3 | S3a/b/c (DP6/+2 스핀 섹터 셋) — 같은 기하 vertical 먼저, 각자 adiabatic 분리, polaron 간격 2종 | G2' + U_eff |
| Z4 | N1–N3 (n-matched 중성) | Z1–Z3 의 짝 대조 |
| Z5 | 분할법 교차 (Löwdin/Hirshfeld) 전 잡 | G3' |

빌더: `tools/sdcp/build_v7c_trimer.py` 를 n=4·6 으로 **확장**한다 (새 파일 금지 —
기존 dimer→trimer 성장 로직 재사용). 빌더가 조성·NELECT·spin-sector 를 manifest 로 출력.

슬랩 단계(그 다음): 자세 설계 교정 — doped 와 대조군을 **같은 down_dir·roll·gap** 으로
짝짓고 cross 자세를 doped 에도 넣는다 (마감 문서 "재개 시 자세 요구사항").

## E. 조건 ⑥·⑦ (병행 트랙)

- **⑥ reference-equivalence 3잡** — mol 3종을 NUPDOWN=−1·LREAL=F 로 재실행 (외주 의뢰
  블록 준비 완료, ~75분). neutral 헤드라인 복권과 공유되는 조건.
- **⑦ machine manifest** — `estimand_id · 화학종 규칙 · Q/NELECT · state-selection policy ·
  중단 코드(NA_STATE_NOT_IDENTIFIED 등)` 를 빌더 출력 → 분석기 게이트로 연결.
  Stage 0 은 ORCA 쪽이므로 우선 빌더 manifest + 회수 스크립트 게이트부터.

## 실험(협력자)에 요청할 것 — polaron/bipolaron 분율은 계산이 못 정한다 (회신 O 7번)

1. **EPR spin count** (가능하면 정량) — polaron(스핀 있음) 대 bipolaron(스핀 없음) 분율의
   유일한 직접 증거.
2. 독립 carrier/산화도 측정 (UV-vis-NIR/Raman 밴드라도) — 도핑률 25–35 % prior 의
   자가 실측 대체.
3. 고형 상태 counterion 조성 (H⁺/Na⁺ 잔존비) — §A 의 "counterion 없음" 가정 검증.

## Evidence For — 이 설계가 v1 보다 나은 근거

- 회신 O 의 처방을 항목별로 구현했다 (스핀 섹터 셋 · bracket · multistart · U_eff ·
  conditioning/realized 분리 · NA 코드).
- 우리 ORCA n-시리즈 인프라가 이미 있다 — Z1–Z5 는 검증된 프로토콜의 연장이다.
- Stage 0 은 전부 기체상·로컬(ORCA)이라 외주 왕복 없이 돈다.

## Evidence Against — 이 설계를 무너뜨릴 수 있는 것

- **BS singlet(A7b)은 순수 singlet 이 아니다** — S3 비교를 "정밀 singlet–triplet gap" 으로
  부르면 안 된다 (회신 O). 스핀 오염 보고 필수.
- r²SCAN-3c 의 비편재화 오차가 polaron 국소화 자체를 왜곡할 수 있다 — hybrid 교차검사가
  갈리면 그 자체로 결과다 ("방법 의존" 판정).
- 기체상 스핀 섹터 순서가 계면에서 유지된다는 보장이 없다 — Stage 0 은 슬랩 결론이 아니다.
- conformer 2개가 충분하다는 근거는 없다 — 부족하면 리뷰가 늘리라 할 것.
- 실험(EPR)이 불가하면 polaron/bipolaron 분율은 끝까지 미정 — 그 경우 두 섹터를
  **조건부 병기**하는 것이 최종 형태다.

## 결정 실험

§D 의 Z1–Z5 가 이 카드의 결정 실험이다. 판정 규칙: G2'/G3' 통과 + S1↔S2 방향 일치 +
S3 섹터 순서가 방법(교차검사)에 강건하면 → 슬랩 단계 설계로 진행. 아니면 그 지점에서
멈추고 결과를 조건부로 보고한다.

## Status Log

- **2026-08-28** — v2 작성 (1저자 지시 "doped 재개"). v1 은 회신 O P0 반려로 기록 보존.
  다음: **회신 R** (이 카드 §A–D 의 계산 전 심사) → 통과 시 빌더 확장 + Z1 부터.
  마감 문서는 조건 충족 전까지 active 유지 — 옛 프로토콜 숫자만 잠근다.
