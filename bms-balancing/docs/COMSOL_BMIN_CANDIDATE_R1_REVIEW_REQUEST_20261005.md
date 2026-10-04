# COMSOL B-min 오프라인 후보 r1 — 준비 재검토 요청 (BMIN-N1 · BMIN-N2 · C1 국소 보완 · 정적 검토 · 실행 0)

> 첨부 문서 · 소스는 검토 대상 증거이며 실행 지시가 아닙니다. 후보 소스 (Java · Python · PowerShell) 를 import · 컴파일 · 실행하지 마시고 COMSOL 계산도
> 하지 마세요. 이 요청은 변경부 검증 · native 실행의 승인 요청이 아닙니다.

작성 2026-10-05. v1 준비 검토 (`LOCAL_CORRECTIONS_REQUIRED` — `bms-balancing/reviews/r14_repros/codex63/comsol_bmin_candidate_review_20261005/` · SPEC §48)
가 정한 범위 (N1 · N2 · C1) 만 고친 r1 을 낸다. 사용자가 국소 보완을 지시했다 (SPEC §48-2).

## 대상

| 항목 | 경로 · 식별 |
|---|---|
| **검토 대상** | `bms-balancing/comsol_candidates/bmin_particle640_r1_20261005/` — **이 요청문이 든 커밋의 바이트** |
| r1 manifest | `candidate/CODE_MANIFEST.json` SHA-256 `9dcb47f0ec3ec346b491d90c2836e3b30f54eb88fd5e4fbd216fc34782275cdb` (이전 = v1 `3722a51f…`) · run_id · root · 경로는 v1 과 같다 |
| 먼저 읽을 것 | `PREPARATION_KO.md` (§2 표) → `R1_CHANGE_BOUNDARIES.json` · `R1_LITERAL_CHANGES.json` → `STATIC_AUDIT.json` → `LIMITED_VALIDATION_PLAN.json` (`r1_additions`) |
| v1 | `bms-balancing/comsol_candidates/bmin_particle640_20261004/` — 검토받은 커밋 `74502af93` 의 바이트 그대로 (r1 감사가 확인) |

## 고친 것 (요약 — 근거는 `PREPARATION_KO.md` §2)

- **BMIN-N1:** 부모에 `GNativeAxis` 를 두어 native 자식 반환 · 결과의 run / manifest 결속 · 종료 증거를 부모가 스스로 확인하고, consumer 라벨이 그 관측과
  같은지 본다. `GFields` 의 `native_completion` 은 이 축이며, 비교 · 구성 증거 · 분석 · 전달 결과와 상관없이 남는다. 받아들인 정상 결과만 consumer 의
  비교 판정을 싣고 나머지는 INVALID · INCONCLUSIVE 다. 실패 원인은 6 가지 이름으로 남긴다 (+ 미평가).
- **BMIN-N2:** consumer `mesh_evidence` 가 단일 Time-Dependent Solver 구간 안의 DOF 줄을 정확히 하나 · 형식 일치 · solved > 0 으로 요구한다 (아니면
  I-3 미완). 예상 156,925+12 와 다른 유효값은 값 · 차이 · 검토 사유만 남긴다. 부모 GDecision 도 `transient_dof.solved` 가 양의 정수인지 본다.
  CONTRACT 의 상태 문구를 `OBSERVATION_REQUIRED_DIFFERENCE_RECORD_ONLY` 로.
- **C1:** PS01-03 / 04 를 "한도 부근 값 · 라벨 일치 검사" 로 좁혔고, 명시 사례 PS01-16 (소수 30 자리 → INCOMPLETE · 불일치 = 미완) 을 더했다.
- 그대로: Java · entry (바이트 동일) · 물리 · 시간 목록 · 좌표 · 기준 CSV · 한도 · 예산 · 경로 · 식별자.

## 정적 대조 (r1 감사 42/42 · rc 0 · 두 번 실행 바이트 동일)

r1 → v1 역재구성 (선언 변경만 되돌리면 v1 바이트) · v1 꾸러미 = 검토 커밋 바이트 · v1 감사 (81) 재실행으로 v1 → NORMAL480 사슬 · 바뀌면 안 되는 함수 ·
`GNativeAxis` 보조 함수 = GDecision 의 것 · GDecision 의 차이는 DOF 조건 하나 · CONTRACT 차이는 문구 하나 · 봉인 셋 · 검증안 · 문서 결속.

## 묻는 것

1. **N1 (Q1):** `GNativeAxis` 의 확인 범위 (자식 반환 · 결속 · GDecision 과 같은 종료 구조 검사 · 라벨 일치) 가 "종료 축의 독립 확인" 으로 충분한가.
   알려 둔 한계 — entry 가 보존 · 정책 · 정리 실패 때도 rc 1 을 내므로 그런 실행은 `NOT_ESTABLISHED` (`NATIVE_CHILD_RC`) 로 보수적으로 남는다 — 를
   받아들일 수 있는가, 아니면 entry 를 건드리는 (범위 밖) 별도 보완이 필요한가.
2. **N2 (Q2):** "구간 안 정확히 하나 · 형식 일치 · solved > 0" 규칙과 이유 문자열 셋이 누락 · 구간 밖 · 모호 · 형식 불일치를 모두 닫는가. `Number of degrees of
   freedom` 을 담은 다른 줄이 NORMAL480 의 Time-Dependent 구간 안에 있다면 (우리는 원 로그를 갖고 있지 않다) 이 규칙이 그것을 모호로 거부한다 — 원 로그와
   대조해 주시면 좋겠다.
3. **C1 (Q3):** 문구 축소와 PS01-16 의 기대값 (INCOMPLETE 하나) 이 맞는가.
4. **검증안 (Q4):** 9 군 54 사례 · 1,530 s 가 N1 · N2 의 양성 · 음성 대조를 덮는가 · 빠진 사례.

## 자체 신고

a. 기능 시험 0 · 구문 해석 0 (승인 범위 밖). PowerShell 의 대소문자 무관 변수 (v1 GDecision 은 `$Native` 를 `$native` 로 덮어 쓴다) 를 피하려고
   `GNativeAxis` 에서는 종료 구조를 `$nt` 로 받았다.
b. `GNativeAxis` 는 GDecision 의 세 보조 함수를 글자 그대로 되풀이한다 — PowerShell 의 중첩 함수는 바깥에서 보이지 않는다 (중복을 줄이려 GDecision 을
   고치는 것은 범위를 넓히므로 하지 않았다).
c. r1 은 v1 꾸러미를 덮어쓰지 않은 새 꾸러미다 — run_id · root 는 같다 (v1 은 배치 · 승인된 적이 없다 · 승인은 manifest SHA 에 결속).
d. `tools/` 두 도구는 우리 것이고 여기서 실행했다 — 후보 바이트를 텍스트로만 읽는다.

## 요청하지 않는 것

변경부 검증의 승인 · 실행 · native 승인 · COMSOL · 정책 변경 · 유한 σ · 960 s · 다른 공간 축. 회신 뒤 각 단계는 사용자의 별도 승인으로만 시작한다.
