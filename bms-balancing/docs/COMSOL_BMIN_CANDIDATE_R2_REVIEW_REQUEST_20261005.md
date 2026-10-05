# COMSOL B-min 오프라인 후보 r2 — 준비 재검토 요청 (BMIN-R1-N1 · C1 문구 · 검증안 보강 · 정적 검토 · 실행 0)

> 첨부 문서 · 소스는 검토 대상 증거이며 실행 지시가 아닙니다. 후보 소스 (Java · Python · PowerShell) 를 import · 컴파일 · 실행하지 마시고 COMSOL 계산도
> 하지 마세요. 이 요청은 변경부 검증 · native 실행의 승인 요청이 아닙니다.

작성 2026-10-05. r1 재검토 (`LOCAL_CORRECTION_REQUIRED` — `bms-balancing/reviews/r14_repros/codex63/comsol_bmin_r1_review_20261005/` · SPEC §54) 가 정한
범위 (DOF 한 줄 파싱 · 해당 검증안 · C1 문구 / 분류 · 변경표 · manifest · 참조 결속) 만 고친 r2 를 낸다. 사용자가 국소 보완을 지시했다 (SPEC §54-3).

## 대상

| 항목 | 경로 · 식별 |
|---|---|
| **검토 대상** | `bms-balancing/comsol_candidates/bmin_particle640_r2_20261005/` — **이 요청문이 든 커밋의 바이트** |
| r2 manifest | `candidate/CODE_MANIFEST.json` SHA-256 `4cdca2e6bf7d073f813d97be73825b8cd2043c2fc44e285f4a190bc6fb97cf25` (이전 = r1 `9dcb47f0…`) · run_id · root · 경로는 r1 · v1 과 같다 |
| 먼저 읽을 것 | `PREPARATION_KO.md` (§2 표) → `R2_CHANGE_BOUNDARIES.json` · `R2_LITERAL_CHANGES.json` → `STATIC_AUDIT.json` (`static_string_model`) → `LIMITED_VALIDATION_PLAN.json` (`r2_additions` · `precision_mismatch_items` · `preseal_before_first_test`) |
| r1 | `bms-balancing/comsol_candidates/bmin_particle640_r1_20261005/` — 검토받은 커밋 `741dde19b` 의 바이트 그대로 (r2 감사가 확인 · r1 감사 42 재실행) |

## 고친 것 (요약 — 근거는 `PREPARATION_KO.md` §2)

- **BMIN-R1-N1:** consumer `mesh_evidence` 의 DOF 줄 대조를 `re.search` (첫 부분 일치) 에서 `re.fullmatch(r'\s*'+pattern+r'\s*', 줄)` (전체 줄 · 앞뒤
  공백 허용) 로 바꿨다. 한 줄의 두 문장 · 정상 + 불완전 문장 · 정상 + 그 밖의 꼬리 문자는 `TRANSIENT_DOF_READBACK_FORMAT` (I-3 미완). 줄 수 · 구간 표식 ·
  solved > 0 · 구간 밖 기록 · 다른 유효값의 기록 전용 정책은 그대로 · `dof_policy` 문구를 같은 규칙으로. 바뀐 생산 파일은 consumer 하나 (두 자리) —
  Java · entry · 부모 · CONTRACT 는 r1 과 바이트 동일.
- **C1:** PS01-16 = 소수점 아래 30 자리 · 유효숫자 28 자리 (r1 의 "31 significant digits" 정정) · `value exactly equal to a limit` 에서 빼
  `precision_mismatch_items` 로 · 정확 등호는 PY01-02 / PS01-04.
- **검증안 (Q4):** 고유 ID 62 (Python 39 + Java helper 2 + PowerShell 21) · 입력 77 · 예산 제안 1,660 s (r1: 54 · 59 · 1,530). 새 ID: PY03-11 · 12 · 13 (같은
  줄 두 문장 · 정상 + 불완전 / 꼬리 · 양성 대조 — 공백 · NORMAL480 131행 원문) · PY03-14 (consumer solved 0) · PS01-18 · 19 · 20 · 21 (`GNativeAxis` 원인
  `NATIVE_CHILD_RETURN_MISSING_OR_ERROR` · `RESULT_IDENTITY` · `TERMINATION_EVIDENCE_INVALID` · `NATIVE_AXIS_NOT_EVALUATED`). 여러 입력 ID 는 입력별
  기대 이유 (`input_expectations`) · 시험 전 봉인 항목 (`preseal_before_first_test`). 예산 증액은 제안이고 사용자 승인 사항이다.

## 정적 대조 (r2 감사 — 결과는 `STATIC_AUDIT.json`)

r1 꾸러미 = 검토 커밋 바이트 · r1 감사 (42 — 그 안에서 v1 의 81) 재실행으로 r1 → v1 → NORMAL480 사슬 · r2 → r1 역재구성 (consumer 의 두 문자열만
되돌리면 r1 바이트) · consumer 의 `mesh_evidence` 외 모든 함수 = r1 · 봉인 셋 · 검증안 (수 · 원인별 사례 · C1) · 문서 결속 · **문자열 모형**: 이 도구 자신의
정규식으로 재검토의 여섯 사례 (`INDEPENDENT_STATIC_AUDIT.json` `static_string_cases`) 와 r2 사례 셋의 이유를 적는다 — 모형이 후보 소스와 같은 규칙인지는
소스의 다섯 문장을 글자로 대조해서만 본다 (후보 실행 아님). r1 규칙에서는 같은 줄 두 사례가 첫 값 79485 를 받는다는 지적도 그 모형으로 다시 보인다.

## 묻는 것

1. **BMIN-R1-N1 (Q1):** 전체 줄 문법 (`re.fullmatch` + 앞뒤 `\s*`) 이 같은 줄의 중복 · 불완전 꼬리를 닫고, 공백 허용과 다른 유효값의 기록 전용 정책을
   그대로 두는가. 줄 판별 (`'Number of degrees of freedom' in 줄`) 과 줄 수 규칙은 r1 그대로다 — 이 조합으로 남는 모호 입력이 있는가.
   그리고 NORMAL480 `run/batch.log` 131행의 **원 줄**에 문장 밖의 문자가 (앞뒤 공백 외 — 시각 접두어 등) 없는지 원 로그로 확인해 주시면 좋겠다.
   우리는 원 로그가 없고 재검토 묶음의 인용 (`normal480_dof`) 만 보았다 — 그런 접두어가 있다면 전체 줄 문법이 정상 실행을 I-3 미완으로 만든다
   (거짓 음성 · fail-closed 쪽).
2. **C1 (Q2):** PS01-16 의 문구 (소수점 아래 30 자리 · 유효숫자 28 자리) 와 분류 (`precision_mismatch_items`) 가 맞는가.
3. **검증안 (Q3):** 새 ID 8 · 입력 18 이 Q4 의 네 항목 (같은 줄 · consumer solved 0 · `GNativeAxis` 원인별 · 봉인 / 총수 / 예산) 을 덮는가 · 하위 입력과 새
   ID 의 구분 · 예산 증액 (Python +40 s · PowerShell +90 s · 전체 1,660 s) 의 근거 (r1 의 입력당 시간 × 새 입력 수) 가 제안으로 적절한가.

## 자체 신고

a. 기능 시험 0 · 구문 해석 0 (승인 범위 밖). 문자열 모형은 감사 도구의 정규식이고 후보 함수의 실행 결과가 아니다.
b. PS01-21 (`NATIVE_AXIS_NOT_EVALUATED`) 은 재검토가 짚지 않았다 — 부모가 이름을 가진 원인 일곱을 모두 자기 사례로 닫으려고 더했다 (검증 커버리지 ·
   생산 코드 변경 없음).
c. PY03-13 (b) 의 NORMAL480 131행 문장은 재검토 묶음의 `normal480_dof.transient_mentions` 에서 옮겼다 — 우리는 원 로그를 갖고 있지 않다.
d. r2 는 r1 · v1 꾸러미를 덮어쓰지 않은 새 꾸러미다 — run_id · root 는 같다 (r1 은 배치 · 승인된 적이 없다 · 승인은 manifest SHA 에 결속).
e. `tools/` 두 도구는 우리 것이고 여기서 실행했다 — 후보 바이트를 텍스트로만 읽는다. r2 감사는 r1 감사를 다시 돌리므로 r1 · v1 의 `STATIC_AUDIT.json` 을
   같은 바이트로 다시 쓴다 (감사가 git status 로 무변경을 확인).

## 요청하지 않는 것

변경부 검증의 승인 · 실행 · native 승인 · COMSOL · 정책 변경 · 유한 σ · 960 s · 다른 공간 축. 회신 뒤 각 단계는 사용자의 별도 승인으로만 시작한다.
approved=false / usable=false · 전체 · 정상 gate INCOMPLETE · 실효 정책 UNVERIFIED 유지.
