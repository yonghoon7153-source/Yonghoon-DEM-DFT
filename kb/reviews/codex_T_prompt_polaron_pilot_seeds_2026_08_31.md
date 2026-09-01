---
title: "리뷰 요청 T — 폴라론 pilot, phase S 착수 전 (seed 생성 완료)"
date: 2026-08-31
updated: 2026-08-31
tags: [review, codex, sdcp, polaron, orca, pilot, prereg]
status: 회신 수령 — `kb/reviews/codex_T_reply_polaron_pilot_2026_08_31.md`
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 리뷰 요청 T — 폴라론 pilot, **측정 직전**

회신 S(2026-08-31)가 32건 r²SCAN-3c adequacy pilot 을 조건부 GO 하고 착수 전 P0 5건을
봉인하라 했다. 봉인은 마쳤고(`db/properties/sdcp_polaron_pilot_prereg_2026_08_31.json`,
`D-2026-08-31-sdcp-polaron-Fbb` proposed), **seed 생성까지 끝냈다.**
다음이 phase S = **estimand 를 재는 단계**라 그 전에 묻는다.

⚠ **현재 구성은 사전등록에서 벗어나 있다** — 아래 Q1 이 그것이다.

## 0. 지금까지 실제로 한 것

| 단계 | 무엇 | 상태 |
|---|---|---|
| L | `D⁻`(charge −1, mult 1) · 중성 `P` SP + Pipek-Mezey 국재화 | ✅ 2잡 완료 |
| L2 | `.loc` 를 MORead, `NoIter` 로 **국재 궤도** MO 인구만 재출력 | ✅ 2잡 완료 |
| seeds | 목표 집합별 최다 국재 MO 선택 → phase S 입력 생성 | ✅ 15잡 생성 |
| **S** | **측정 (16 SP)** | ⛔ **여기서 멈춰 리뷰를 요청한다** |

부모: `dp6_gs0_neutral_final.xyz` (Stage A gs0, r2SCAN-3c Opt 완료,
E −10051.686813573808 Ha, SHA256 `036fbf55…f40ba`).
제거 H = 1-based **124** (산성 H 6개 중 사전 규칙으로 중간 위치).

## 1. 설계 (회신 S 계약 이행)

- **관측량**: `F_G = Σ_{i∈G}|m_i| / Σ_i|m_i|`, 세 집합 상호배타·완전, 합 = 1.
  Hirshfeld primary · Löwdin sensitivity, signed `M_G` 별도 보존.
  (v1 의 signed 분자 식은 폐기 — selftest 가 그 상쇄를 재현한다)
- **집합**: backbone(티오펜 고리 + **고리 C 에 직결된 에테르 O** + 고리 H) 44 /
  sulfonate(S + 3O + 산성H) 30 / other 126 = 200. hash `96b2334f097ab65f`.
  ⚠ 에테르 O 포함 여부가 estimand 를 움직이므로 분석기가 **포함·제외 두 값을 다 내고**
  class 가 갈리면 `BACKBONE_DEFINITION_DEPENDENT`.
- **seed 8종**(D•): A(제거된 SO₃) 1 + B(EDOT ring 별) 6 + default 1.
  positive control `P⁺`(charge +1, mult 2): B 6 + default 1.
- **제약은 seed 생성에만** — 최종 SCF 는 완전 비제약. 각 seed `NoAutoStart` +
  명시적 `MOInp`. 전 seed 에 `StabPerform`.
- **판정**: BACKBONE_SUPPORTED / SO3_CENTERED_WITHIN_MODEL / ENVIRONMENT_DEPENDENT /
  FUNCTIONAL_DEPENDENT / MODEL_NONDIAGNOSTIC / PARTITION_DEPENDENT /
  THRESHOLD_DEPENDENT / BACKBONE_DEFINITION_DEPENDENT.
  positive control 이 backbone 상태를 하나도 회수하지 못하면 **H-제거계를 해석하지 않는다.**

## 2. 실측이 드러낸 설계 결함 넷 (전부 측정 전에 잡았다)

**① 인구 블록이 정준(canonical) 궤도의 것이었다.**
`LOEWDIN ORBITAL POPULATIONS PER MO` 는 출력 **5883줄**, 국재화는 **340994줄**.
MO 0 이 −88.757 Eh(S 1s 97%)인 것도 정준 코어다. 정준 궤도는 비편재라 "이 링에
걸린 MO" 를 거기서 고르는 것은 뜻이 없었다. 국재 궤도는 `<tag>.loc` 에 따로 있다.
⇒ **phase L2 신설**: `.loc` 를 MORead + `NoIter`. seed 입력도 `.gbw` 가 아니라
**`.loc`** 를 읽는다. (종전이면 국재 인구로 고른 인덱스를 정준 집합에 적용했다.)

**② 행 정규식이 실제 형식과 달랐다.** 실제는 `  2S   1s   97.0` — 인덱스와 원소가
**붙어 있다**(`36S`·`102S`). 종전 정규식은 공백을 요구해 한 행도 안 맞았다.

**③ Rotate 의 스핀 채널이 틀렸다 — 이게 제일 위험했다.**
`Rotate {from, to, angle, op_from, op_to}` 의 마지막 둘은 **스핀 채널**이다
(0 = 알파, 1 = 베타). 처음엔 `0,0`(알파)로 냈는데 그것은 **완전한 no-op** 이다:
`D•`(961전자 doublet)는 **알파 0..480 이 전부 점유**이고 베타가 0..479 다.
알파끼리 돌리면 둘 다 점유라 밀도가 안 변한다. 홀은 **베타**에 있으므로 목표
국재 MO 를 **베타의 첫 빈자리(480)** 로 보내야 한다 ⇒ 연산자 `1,1`.
⚠ 이대로 돌렸으면 **seed 8개가 전부 같은 기본 해로 수렴**하고, 우리는
*"방법이 backbone 상태를 회수하지 못한다"* → `MODEL_NONDIAGNOSTIC` 이라고
**잘못 결론**냈을 것이다. 입력 파일을 실제로 열어 보고 잡았다.
목표 인덱스도 "부모의 HOMO" 가 아니라 **S 계의 베타 첫 빈자리**로 명시 계산하게
고쳤다 (전자 하나 차이라 숫자는 우연히 같지만 뜻이 다르다).
`%scf` 도 여러 줄로 바꿨다 — `Rotate {...} end` 의 end 와 `%scf` 의 end 가 한 줄에
붙으면 모호하다.

**④ 고른 MO 가 HOMO 자체인 경우가 있다.** ring5 → mo **480** = HOMO(962/2−1).
그러면 `Rotate {480,480,90,0,0}` 이 되어 자기 자신과 회전이다. 그 경우 회전을
생략한다(홀이 이미 그 자리에 생긴다). job.json 에 사유를 남긴다.

## 3. seed 생성 실측

```
원자가 MO 319  (= 국재화 범위 162~480, 코어 0~161 자동 제외)
점유 481       (= 962/2)
D•  A_sulfonate mo=441 99.4% · ring0 237 98.6% · ring1 281 97.8% · ring2 326 97.4%
    ring3 372 97.1% · ring4 416 97.3% · ring5 480 98.6%(=HOMO, 회전없음) · default
P⁺  ring0 237 98.7% · ring1 281 97.8% · ring2 326 97.4% · ring3 364 97.3%
    ring4 416 97.6% · ring5 480 98.7%(=HOMO, 회전없음) · default
loc 결박 SHA256: a2b4ebd14ed8… (D⁻) · c245aaebf167… (중성)
```
ring MO 가 ~45 간격으로 늘어선 것이 반복단위 6개와 맞는다.

**부수 검증**: 97~99% 라는 값 자체가 "L2 가 `.loc` 를 실제로 읽었다" 는 증거다 —
정준 궤도를 읽었다면 비편재라 한 링에 97% 가 나올 수 없다.

## 4. 우리가 아는 한계 (숨기지 않는다)

- **국재화가 무작위 seed 로 돈다** (`Localizations seeded randomly ... on`).
  재실행하면 MO 순서가 달라진다. 결정론을 만드는 키워드를 확인하지 못했으므로
  **실현된 `.loc` 의 SHA256 에 결박**하고, seed 가 "이 국재화에 조건부" 임을 각
  job 에 기록했다. **Q2 에서 묻는다.**
- **잡 수가 16 이지 32 가 아니다** — 환경이 ε=1 하나뿐이다. **Q1.**
- seed 가 97~99% 로 국재됐다는 것이 **SCF 가 그 basin 으로 수렴한다는 뜻은 아니다.** **Q4.**
- 아직 phase S 를 **한 잡도 돌리지 않았다.**

## 5. 묻는 것

**Q1 (제일 중요).** 사전등록은 **환경 2개 × 32 SP** 였는데 지금은 **ε=1 만 · 16 SP** 다.
dry-polymer ε 값에 litdb 근거를 아직 확보하지 못해, 근거 없는 값을 넣으면 우리
사전등록을 우리가 어기는 것이라 도구가 `--eps_why` 없이는 거부하게 만들었다.
⇒ ε=1 만으로 **adequacy 판정**(positive control 이 backbone 을 회수하는가 · 의도한
basin 이 잡히는가)을 먼저 하는 것이 허용되나? 아니면 ε 근거를 먼저 확보하고
32건을 한 번에 돌려야 하나? 전자라면 그 결과로 말할 수 있는 것의 상한은?

**Q2.** 무작위 국재화에 대한 우리 대응 — **결정론을 포기하고 실현된 `.loc` 해시에
결박**한 것 — 이 충분한가? 재현 가능성을 해시 결박으로 대체하는 것이 이 estimand 에서
받아들여지나, 아니면 결정론적 국재화(또는 seed 를 다른 방식으로 준비)가 필수인가?

**Q3.** backbone 정의에 **EDOT 3,4-에테르 O 를 포함**한 선택. 그 O 는 고리 C 에 직결돼
π 에 전자를 밀어넣으므로 폴라론 밀도를 갖는다고 봤다(빼면 F_bb 가 체계적으로 과소평가).
sp³ `-CH2CH2-` 다리는 other 로 뒀다. 이 분할이 맞나? 두 정의를 다 보고하고 갈리면
`BACKBONE_DEFINITION_DEPENDENT` 로 닫는 것으로 충분한가?

**Q4.** seed 가 목표 집합에 97~99% 국재됐다는 것과, **비제약 SCF 가 그 basin 으로
수렴한다**는 것 사이의 간극. 우리는 `StabPerform` + 수렴 후 F 측정으로만 본다.
seed 가 의도한 basin 을 실제로 회수했는지 판정하는 **추가 기준**이 필요한가
(예: 수렴 후 F 가 seed 집합과 일치하는지, 또는 여러 seed 가 같은 해로 무너지는지)?

**Q5-0.** ③ 의 연산자 판단이 맞나 — `D•`(알파 481 · 베타 480)에서 목표 집합에
스핀을 놓으려면 **베타의 첫 빈자리로 보내는 것**이 맞는가? 알파 쪽에 손대야 하는
경우가 있나? 그리고 `Rotate` 90° 가 두 궤도를 **교환**한다는 우리 이해가 맞는지.

**Q5.** `ring5` 처럼 **고른 MO 가 HOMO 자체**일 때 회전을 생략한 것. 이 경우 seed 가
"준비된" 것이 맞나, 아니면 그 링에 대해서는 seed 가 사실상 **default 와 같아져**
독립 seed 로 세면 안 되나? (D•/P⁺ 둘 다 ring5 가 그렇다.)

**Q6.** `D⁻` 기준이 **`L_dminus` 와 같은 계산**이다(seed 생성원 겸 same-nuclei 기준).
이 이중 역할이 문제인가? 별도 잡으로 분리해야 하나?

**Q7.** `P⁺` 의 ring3 국재 MO 가 **364**, `D•` 는 **372** 로 다르다. 두 계의 국재화가
조금 다르게 수렴한 것인데, positive control 로서 문제가 되나?

**Q8.** phase S 착수 **GO/NO-GO**. 막는 것이 남았으면 무엇인가.
