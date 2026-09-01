---
title: "리뷰 요청 V — 폴라론 S0 (회신 U P0 9건 이행)"
date: 2026-09-01
updated: 2026-09-02
tags: [review, codex, sdcp, polaron, orca, prompt]
status: 회신 수령 — 후속 W (P0 5건 이행)
kind: review-request
system: sdcp
confidence: high
verificationStatus: unverified
explored: false
authoredBy: agent
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 리뷰 요청 V — 폴라론 S0

> 이전 회신: 회신 U (NO-GO · P0 9건 · phase L 도 돌리지 말 것)
> **ORCA 는 여전히 한 잡도 돌리지 않았습니다. phase L 도 안 돌렸습니다.**

```
빌더      c3445652de9618bcbe46fcea31cddf800ec2b12aa3305b487278a06abfb49d10
커밋      35eb8a9f55fb77cce79c95683362a371f113df9d
S0 사전등록 60a58f657c26a1278a51e1914a7aafce815b3a2ca36e8074482a8ebfdc147731
부모 XYZ  b49076980623185cdde983dba64acc11a73021293b0886e263aee618a8de5085
selftest  195건 PASS   (회신 U 시점 152)
```

⚠ 지난번에 ZIP/MANIFEST 를 직접 대조하지 못하셨다고 하셨습니다. 이번에는 빌더 파일
하나가 전부이므로 위 SHA 로 대조하실 수 있습니다.

## P0 9건

### P0-1 `%loc` 계약 — 지적이 맞았습니다

`Randomize 0` 은 ORCA 의 키가 **아니었습니다**. 세 판 동안 그것을 쓰면서
"결정론 국재화를 걸었다" 고 적었고, 그 주장에 근거가 없었습니다.

- `Random 0` · `OCC true` · `VIRT false` · `T_CORE -3.0` 을 **전부 명시**합니다.
- R1(민감도)도 기본값에 맡기지 않고 `Random 1` 을 적습니다.
- ⛔음성시험: `Randomize` 가 되살아나면 실패합니다.

### P0-2 π 판정 — 회전불변으로 다시 만들었습니다

지적하신 대로 종전 식 `Σ n_k² p_k / Σ p_k` 는 대각 인구만 써서 **축 의존**입니다.
순수한 p_n̂ 궤도에 넣으면 `Σ n_k⁴` 가 나오고, 대각선 법선 (1,1,1)/√3 에서 **1/3** 로
무너집니다 — 주신 0.342·0.361·0.423… 이 정확히 그 값입니다.

- `%output Print[P_MOs] 1` 로 **MO 계수**를 받아, 같은 원자·같은 껍질의
  (c_x,c_y,c_z) 로 3×3 `P = Σ v vᵀ` 를 쌓고 `n̂ᵀPn̂ / tr P` 를 씁니다.
  회전 R 에서 v→Rv, n̂→Rn̂ 이라 **불변**이고 이상적 p_n̂ 에서 정확히 1 입니다.
- **계수가 없으면 통과를 주지 않습니다** (`pi_basis` 가 `mo_coefficients` 여야만 통과).
  대신 PSD 에 대한 Cauchy–Schwarz 로 `n̂ᵀPn̂ ≤ (Σ|n̂_k|√P_kk)²` 상한을 내고,
  상한이 문턱보다 작으면 **기각만** 합니다 (안전한 방향).
- 신설 시험: 링을 다섯 방향으로 기울여도 π=1.000 이고, **종전 식이 같은 자리에서
  0.335 로 무너지는 것**을 같은 시험 안에서 재현해 기록합니다.

### P0-3 spin parser — fixture 가 실물과 달랐습니다

콜론을 선택으로 바꿨고, fixture 를 **각 블록의 공식 형식**으로 고쳤습니다
(Loewdin 은 `0 C :`, Hirshfeld 는 콜론 없음). 종전 fixture 는 두 블록에 똑같이
콜론을 넣어, "Hirshfeld 를 한 번도 못 읽었다" 는 사실을 152건 통과 뒤에 숨겼습니다.

### P0-4 코어 배제 — 국재 MO 에너지를 쓰지 않습니다

- 국재화 **전** canonical `ORBITAL ENERGIES` 에서 `ε < T_CORE` 인 점유 궤도를 세어
  **index 창**을 만듭니다. 창이 앞쪽에 연속이 아니면 만들지 않습니다.
- 창을 못 만들면 **seed 를 만들지 않습니다** (종전엔 `ener=None` 이면 코어를 그냥 뽑았습니다).
- 두 번째 그물로 **AO 성격**(원소별 코어 껍질 — C 는 1s, S 는 1s/2s/2p)을 봅니다.
- phase L 입력에 `T_CORE`/`OCC true` 가 없으면 거부합니다.

### P0-5 사전등록 결박

- manifest 가 **S0 문서**를 가리키고 그 **해시를 봉인**합니다.
  `pilot_seeds`·`pilot_restart`·`pilot_analyze` 가 매번 대조합니다.
- 러너가 `$BUILDER` 의 sha256 을 manifest 의 `builder_sha256` 과 대조합니다.
- S0 사전등록을 **재발행**했습니다 (고친 것이 아니라 새 해시로 다시 봉인).
  `status_history` 에 순서가 남습니다. 이전 봉인도 `이전_봉인` 으로 보존합니다.

### P0-6 S0 전용 판정 — `ADEQUATE` 를 넣었습니다

최저 에너지 잡을 골라 `BACKBONE_SUPPORTED`/`SO3_CENTERED_WITHIN_MODEL` 을 내던
**폐기된 전체-pilot 경로를 삭제**했습니다. 이제:

- 게이트 0 + 계획된 positive control 전건 판정 + backbone 회수 + **게이트 통과 D•
  basin ≥ 2** → `ADEQUATE`
- basin 이 **1개면 막습니다** (사전등록 합격 조건 ②). 종전엔 안 막았습니다.
- `by_env` 에서 `lowest` 를 걷었습니다. 에너지는 `E_spread_eV` 로 자료만 남깁니다.

### P0-7 restart 재판정

`UNSTABLE_REJUDGED_STABLE` 이면 **에너지·스핀·class·군집 재료를 전부 재계산
출력에서** 읽고 `judged_from` 에 어느 잡인지 남깁니다. 주신 재현(원래 −100.01 /
restart −100.5 인데 결과가 −100.01)이 시험으로 들어가 있습니다.

### P0-8 basin 군집 — 네 겹 전부

- ⓐ 첫-job anchor greedy 폐기. 쌍 행렬 → **추이성 검사** → 동치관계면 연결성분.
  깨지면 `CLUSTER_AMBIGUOUS` 로 닫습니다. 이름 배치를 바꿔도 같은 수가 나옵니다.
- ⓑ `passed=False` 행은 군집 입력에서 뺍니다 (`excluded_gated` 로 보고).
- ⓒ 스핀 벡터를 `Σ|s_i|` 로 정규화하고, `ring_applicable=False` 인 해끼리는
  **링 축을 뺍니다**.
- ⓓ `d_spin = min(‖s_A−s_B‖₁, ‖s_A+s_B‖₁)`. 부분 반전은 정준화하지 않습니다.

### P0-9 `NO_VALUE`

게이트/결측 판정을 **positive control 앞으로** 옮겼습니다.
`MODEL_NONDIAGNOSTIC` 은 계획된 positive control 이 **전부 정상 판정됐는데도**
backbone 상태가 없을 때만 나옵니다.
⚠ 이 음성시험이 부수적으로 실제 버그를 하나 더 드러냈습니다 — `NOT_RUN` 잡에는
`_basin` 키가 없어 분석기가 **KeyError 로 통째로 죽었습니다**.

## 해제 순서

- ⑤ 결과에 `realization_scope = R0-conditional` 을 박았습니다 (R0/R1 교차비교 전).
- ⑥ 러너에 **`loccheck`** 단계를 넣었습니다 — H₂O 하나로 `%loc` 구문·`.loc` suffix·
  두 인쇄 블록을 30초에 확인합니다. 200원자 잡은 `%loc` 이 무시돼도 정상 종료하기
  때문에 없는 키를 세 판 동안 못 봤습니다. **이것이 통과해야 phase L 입니다.**

## Q 답 반영

- **Q5**: 면제 사유 문구를 주신 대로 고쳤습니다 — *"UNO/UCO 는 계산·판정하지 않는다.
  NoIter probe 는 초기 개입 확인만 하며 에너지와 최종 전자상태 해석에 쓰지 않는다."*
  근거가 *정의 불가* 가 아니라 **쓰지 않음**이라는 지적을 그대로 받았습니다.

## 우리가 아직 **안** 한 것 (숨기지 않습니다)

1. **실물 ORCA 확인이 0 입니다.** `Random 0`·`T_CORE`·`Print[P_MOs]` 가 실제로
   먹는지, `.loc` suffix 가 맞는지 확인하지 않았습니다. `loccheck` 가 그것을 하려고
   있는 것이지, 한 것이 아닙니다.
2. **Q3 (1층 문턱 0.50)**: `localized_no_rotation` NoIter control 을 아직 안 만들었습니다.
   0.50 은 보조 sanity gate 로 두었고, 주신 ⓐⓑⓒ 세 조건은 미구현입니다.
3. **Q2-②** `RING_ASSIGNMENT_UNRESOLVED`: 분할·문턱 의존일 때 면제 대신 이 판정어를
   내는 경로를 아직 안 넣었습니다 (현재는 `applicable=False` 하나입니다).
4. **Q6** `S0_EPS1_ANION_REFERENCE_INADEQUATE` 판정어 미구현.
5. **R0/R1 교차비교** 자체를 안 돌렸습니다 (돌릴 승인이 없습니다).

## 여쭙는 것

**Q1.** P0-2 의 회전불변 판정이 맞습니까? 같은 원자·같은 껍질의 p 만 vvᵀ 로 쌓고
겹침 행렬을 쓰지 않았습니다 — 껍질 **안**에서는 정확하고 원자 간·껍질 간 교차
겹침만 무시합니다. 이 근사가 "이 p 뭉치가 법선을 향하는가" 에 충분합니까?

**Q2.** 계수가 없을 때 Cauchy–Schwarz 상한으로 **기각만** 하는 처리가 적절합니까?
상한은 엄밀하므로 안전한 방향이라고 봅니다만, 아예 판정을 안 하는 편이 낫습니까?

**Q3.** P0-4 의 **canonical index 창**이 성립합니까? `T_CORE` 국재화가 코어를
제자리에 두므로 국재 인쇄의 앞쪽 index 가 곧 코어라고 가정했습니다. 이 가정이
ORCA 에서 보장됩니까, 아니면 AO 성격만 남기고 창을 버려야 합니까?

**Q4.** P0-8ⓐ 의 **추이성 검사 → `CLUSTER_AMBIGUOUS`** 가 주신 "complete-linkage
또는 비추이적 triple 이면 닫기" 를 만족합니까? 저희는 동치성이 성립할 때만 세고,
아니면 수를 내지 않습니다.

**Q5.** 위 "안 한 것" 5건 중 **phase L 하나를 돌리기 전에 반드시 닫아야 하는 것**이
있습니까? 저희는 ①(loccheck 실행)만 선행이고 나머지는 phase S 전이라고 봅니다.

**Q6.** 미구현 4건(Q3 control · RING_ASSIGNMENT_UNRESOLVED · S0_EPS1_* · R0/R1)의
순서를 정해 주시면 그대로 하겠습니다.

파일은 수정하지 않으셔도 됩니다 — **GO/NO-GO 와 P0/P1** 판정만 주십시오.
