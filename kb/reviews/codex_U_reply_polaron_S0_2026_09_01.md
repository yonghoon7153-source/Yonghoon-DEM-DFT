---
title: "회신 U — 폴라론 S0 (NO-GO · P0 9건 · phase L 도 돌리지 말 것)"
date: 2026-09-01
updated: 2026-09-01
tags: [review, codex, sdcp, polaron, orca, reply]
status: 회신 수령 — 이행 대기
kind: review-reply
system: sdcp
confidence: high
verificationStatus: verified
verifiedAt: 2026-09-01
verifiedBy: "회신 원문 (리뷰어가 실제로 빌더를 돌려 재현)"
explored: false
authoredBy: external
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 회신 U — 폴라론 S0

> 요청: `kb/reviews/codex_U_prompt_polaron_S0_2026_08_31.md`
> 판정: **NO-GO — 현재는 phase L 도 돌리면 안 된다.**

## 검증 범위 (리뷰어가 실제로 한 것)

커밋 `9bbf22de…` · 빌더 SHA `3faca7ce…` · 부모 XYZ SHA `b4907698…` 요청서와 일치 확인.
UTF-8 selftest 152건 PASS · 실제 `--polaron_pilot` 생성 정상(10파일 · L 2잡 · L2 2잡).
⚠ `sdcp_polaron_S0_inputs.zip` 자체는 첨부에 없어 ZIP/MANIFEST SHA 는 **직접 대조 못 함**.

## P0 9건

1. **`%loc` 계약이 틀림** — `build_v7c_trimer.py:3064` 가 `%loc Randomize 0` 을 쓰는데
   ORCA 6.1 공식 inline 키는 **`Random 0`** 이다. `OCC`·`VIRT`·`T_CORE` 생략으로
   "occupied valence 만 국재화" 를 보증 못 한다.
   → `Random 0 · OCC true · VIRT false · T_CORE <봉인값>` 명시. R1 도 기본값에 맡기지
   말고 `Random 1` 명시.
2. **π 판정식이 좌표축에 의존** — `pil_mo_character():3435` 의 `Σ n_k² p_k / Σ p_k` 는
   교차항과 AO 계수 부호를 잃어 실제 법선 투영이 아니다. **부모 구조 여섯 고리에
   이상적 `p_normal` 을 넣어도 점수가 0.529·0.423·0.666·0.342·0.510·0.361** 이라
   문턱 0.60 이면 **완전한 π 궤도도 5/6 이 탈락**한다. 축 정렬 합성 fixture 가 이
   결함을 숨겼다. → MO 계수 또는 p-subspace 밀도행렬로 `|n·c|²` 를 계산하는
   **회전불변** 판정 필요.
3. **실제 ORCA 출력을 spin parser 가 못 읽음** — `_spin_block():1043` 이 `0 C:` 처럼
   원소 뒤 콜론을 강제하는데 ORCA 6.1 Hirshfeld 출력은 `0 O  -0.333756  0.000000`
   으로 **콜론이 없다**. 실제 형식으로 재현하니 parser 가 `None` 을 반환했다.
   현재 fixture 는 인위적으로 `C:` 를 넣는다. → 콜론 선택사항 + 공식 형식을 e2e
   fixture 로.
4. **localized MO energy 로 core 를 거르는 것은 성립 안 함** — `pil_pick_seed_mo():3540`
   이 localized MO 에너지 < −3 Eh 를 core 로 보는데, ORCA 는 **localized MO 에 잘
   정의된 orbital energy 가 없다**고 명시한다. → localization **전** canonical window +
   명시적 `T_CORE` + AO 성격으로 봉인.
5. **생성물이 S0 사전등록을 안 가리킴** — S0 prereg 가 **옛 빌더**(`f58b8e5f…/d89acd…`)를
   봉인하는데 실제 빌더는 `9bbf22de…/3faca7…`. manifest 생성부(3188)는 S0 문서가 아니라
   **구판 전체-pilot prereg** 를 기록한다. 러너도 `BUILDER` SHA 를 manifest 와 대조 안 함.
6. **분석기가 S0 가 아니라 폐기한 전체-pilot 결론을 냄** — `pilot_analyze():4366` 이
   여전히 최저 에너지 잡을 골라 `BACKBONE_SUPPORTED`/`SO3_CENTERED_WITHIN_MODEL` 을
   낸다. **`ADEQUATE` 경로가 코드에 없다.** D• basin 이 하나여도 안 막는다.
   selftest 도 구판 verdict 를 정답으로 허용한다.
7. **restart 가 안정해를 재판정 안 함** — `4178` 이 restart 출력에서 안정성 문자열만
   보고 에너지·스핀·class·군집은 계속 **원래 불안정 출력**에서 읽는다. 재현:
   원래 −100.01 Eh · restart −100.5 Eh 인데 결과가 `UNSTABLE_REJUDGED_STABLE` 이면서
   에너지는 −100.01 그대로.
8. **basin 수가 물리와 무관하게 바뀜** — `pil_basin_cluster():2949` 에 넷이 겹친다:
   ⓐ 첫 job anchor greedy 라 **job 이름 배치에 따라 basin 수가 1 또는 2**
   ⓑ gate 실패·불안정 행을 군집 입력에서 제외 안 함
   ⓒ backbone 몫 < 0.50 이면 링 판정을 면제하면서 군집엔 backbone 내부 정규화 `ring_p`
     를 계속 씀 — 작은 잡음이 basin 을 가름
   ⓓ **전역 α↔β 반전을 다른 상태로 셈** (collinear doublet 에선 같은 상태의 반대 M_S)
   → 통과 행만 사용 · `d_spin = min(‖s_A−s_B‖₁, ‖s_A+s_B‖₁)` 로 canonicalize ·
     spin vector 를 `Σ|s_i|` 로 정규화 · 비-backbone 해에는 `ring_p` 를 군집축에서 제외 ·
     complete-linkage 또는 비추이적 triple 이면 `CLUSTER_AMBIGUOUS` 로 닫기.
9. **미관측 positive control 을 방법 실패로 바꿈** — `4347` 이 blocks 보다 먼저 실행돼,
   Pcation 출력을 전부 없애면 `GATED_JOBS` 가 있는데도 `MODEL_NONDIAGNOSTIC` 이 나온다.
   → 실행 실패·결측은 반드시 **`NO_VALUE`**, 계획된 positive-control 이 **전부 정상
   판정됐는데** backbone 상태가 없을 때만 `MODEL_NONDIAGNOSTIC`.

## Q 답

- **Q2-① 최종 hit 미요구: 찬성** — 옮겨간 상태도 결과, `MOVED_FROM_SEED` 로 보존.
- **Q2-② backbone < 0.50 링 면제: 조건부** — Hirshfeld/Löwdin·strict/extended 모두에서
  robust 한 비-backbone 일 때만 `RING_NOT_APPLICABLE`. 분할·문턱 의존이면 면제가 아니라
  **`RING_ASSIGNMENT_UNRESOLVED`**.
- **Q2-③ 전역 스핀 반전 미흡수: 반대** — 같은 doublet 을 두 basin 으로 세어 `basin ≥2` 를
  **거짓 충족**할 수 있다.
- **Q3 1층 문턱 0.50: 단독 hard gate 반대** — seed MO 는 40% 부터 허용하면서 probe 는
  50% 를 요구해 내부 기준이 안 맞는다. 절대 0.50 은 회전 전부터 목표에 있던 spin 과
  실제 개입을 구분 못 한다. → D/P 각 하나의 `localized_no_rotation` NoIter control 을
  만들어 ⓐ 회전 후 목표 몫이 no-rotation 보다 증가 ⓑ 초기 spin vector 가 실제로 다름
  ⓒ 목표가 유일 최대 또는 봉인 margin 충족 을 확인. 0.50 은 보조 sanity gate 로 유지 가능.
- **Q4 군집 문턱: hard threshold 반대** — 정규화·부호 canonicalization·통과행 필터·
  명시적 linkage 를 먼저 고친 뒤 **같은 산출물을 0.5×/1×/2× 문턱으로 재분석**해 basin
  수·소속이 같을 때만 확정. 계산 추가 불필요.
- **Q5 probe UNO/UCO 면제: 찬성, 이유 문구 수정** — "NoIter 밀도에서 정의되지 않는다" 는
  과하다. 정확한 문구: *"UNO/UCO 는 계산·판정하지 않는다. NoIter probe 는 초기 개입
  확인만 하며 에너지와 최종 전자상태 해석에 쓰지 않는다."*
- **Q6 ε=1 선행: S0 기술시험 한정 찬성** — 단 ε=1 의 D⁻ 가 diffuse/unbound 라 실패하면
  방법 전체의 `MODEL_NONDIAGNOSTIC` 으로 부르면 안 되고
  **`S0_EPS1_ANION_REFERENCE_INADEQUATE`** 또는 `S0_EPS1_INCONCLUSIVE` 로 분리.
- **Q7 실행 승인: NO-GO.**

## 해제 순서 (회신 문구)

1. `%loc` 를 `Random 0 · OCC true · VIRT false · T_CORE 명시` 로 수정
2. S0 prereg·결정·빌더·입력 해시를 **새 manifest 에 결박**
3. π 판정과 공식 ORCA population parser 수정
4. S0 전용 verdict · restart 재판정 · 군집 수정
5. R0/R1 교차비교가 없으면 결과를 **`R0-conditional`** 로 제한
6. **작은 분자로 `%loc` 문법과 실제 suffix 확인**
7. 그 뒤 200원자 L 한 잡 → L2 한 잡 → seed 생성 → NoIter probe 한 잡 순으로 smoke

⚠ phase L 에는 `Rotate` 가 없으므로 **L 성공만으로 Rotate 까지 검증됐다고 쓰면 안 된다.**

## 우리 쪽 읽기 (2026-09-01)

이번 회신의 P0 아홉 중 **둘(#2 π 판정 · #3 spin parser)이 같은 유형**이다 —
**합성 fixture 가 실물과 달라서 결함을 숨겼다.** #2 는 축 정렬 fixture 라 회전
의존성이 안 보였고, #3 은 fixture 가 인위적으로 콜론을 넣어 실제 ORCA 출력을
못 읽는 것을 가렸다. selftest 152건이 전부 통과한 채로 그랬다.
⇒ 이 캠페인의 selftest 는 **실물 ORCA 출력 조각**을 fixture 로 써야 한다.
