# 실행 담당 Codex 발송 프롬프트 — S1 OPEN 연결부 좁은 정정 · 정적 재봉인 (OPEN-R1 · N1–N3) · 2026-10-10

> **사용자가 §0 의 채택 문구를 승인한 뒤에만 보낸다.** 승인 전에는 초안이다. 원장 `COMSOL_REBUILD_SPEC.md` §85.
> §0 문구는 검토 회신 (`REVIEW_KO.md` §2 · §5) 의 권고를 이 저장소가 승인문으로 옮긴 것이다 — 이번 회신에는 채택 문구 초안이 없었다. 예산 2,400 초는 이 저장소의 제안이다.
> 아래 `---` 사이가 붙여 넣을 본문이다. 같이 첨부: 준비본 검토 회신 zip (`COMSOL_MICROSHORT_S1_OPEN_CONNECTION_PREPARATION_REVIEW_20261010.zip` · 1,953,422 B · sha256 `f23d02b0…bdd15`).

---

첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.

## 0. 승인 범위 (사용자 채택 문구 — 승인 시 원문 그대로 붙인다)

> S1 OPEN 연결부 준비본 정적 검토 회신의 OPEN-R1-N1–N3 만 고치는 좁은 오프라인 정정과 정적 재봉인 (OPEN-R1) 한 건을 승인합니다. 대상은 준비본 (zip sha256 `32cbb6ee5b8885a645da762154dab38d8f67ef4c7f97b5b4bc9c2ecd5fdd6f5c` · CODE_MANIFEST sha256 `be19764204a4695c9058f565a69c5e09ea528124d4659e9d8f9d1c11fd6f749f`) 이고, 준비본 · 그 74 개 정적 기록 · 원 R1 21 구성원은 그대로 두고 새 폴더 **`C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/microshort_s1_open_connection_r1_20261010/`** 에서만 새 비활성 revision 을 만듭니다 — 이미 있으면 중지하고, 삭제 · 재사용 · 다른 이름으로의 자동 우회는 하지 않습니다. 고칠 것은 `resource_connection` 의 시간 원점 결속 (N1) 과 process counter 항목 검사 (N2), 그리고 검증안의 도달 조건 · 양성 대조 (N3) 뿐입니다. 기존 수치 예산 · reserve · 물리 · 허용치 · 원 수용 코드 (consumer / control / Parent · R1 21 구성원) 는 바꾸지 않습니다. 정적 확인 (구문 parse · 해시 · 텍스트 대조) 만 하고, 후보 / 받은 코드의 import · 함수 호출 · 기능 시험 · Java 컴파일 · JVM · COMSOL · OS 수집기 · approval / release / runtime / token 생성은 하지 않습니다. 시도 1 회 · 새 원점 상한 총 2,400 초 (정정 작성 1,200 · 정적 확인 300 · 검증안 갱신 · 재봉인 480 · 보존 · 전달 300 · 미완 정리 120) — 단계 사이 전용 없이, 넘으면 멈추고 미완으로 보고합니다. 제출 뒤 멈춥니다. 갱신 검증안의 실행 · 설치본 관측 · P0 native 는 각각 별도 승인입니다.

## 1. 고정 식별

| 대상 | 식별 |
|---|---|
| 정정 대상 준비본 | zip 1,929,576 B · sha256 `32cbb6ee…6f5c` · PACKAGE_MANIFEST sha256 `63c27d8783fd0c61111cd7c72f93b93a48fe6599ecd56f69680893dea87c7019` (79) · CODE_MANIFEST `be197642…f749f` (11 구성원) — 폴더 `…/outputs/microshort_s1_open_connection_candidate_20261009/` |
| 바꾸지 않는 기준 | R1 CODE_MANIFEST sha256 `4ce5c08dbde5153027819b5a651e3995ec82417b4429b9bb0f789082b440f5da` + 21 구성원 · 이전 수용 `LIMITED_VALIDATION_CLOSED_WITH_DOCUMENTED_SCOPE` |
| 검토 회신 | `COMSOL_MICROSHORT_S1_OPEN_CONNECTION_PREPARATION_REVIEW_20261010.zip` · 1,953,422 B · sha256 `f23d02b01b7a2ae96a2cfcf17009d73a2c47cddae7895c124aea6543b15bdd15` (특히 `REVIEW_KO.md` §2 · §5) |
| 새 폴더 (하나) | `C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/microshort_s1_open_connection_r1_20261010/` |

## 2. 고칠 것 — 회신 §2 그대로

1. **OPEN-R1-N1 (P1) · 시간 원점 결속** — `resource_connection.py.inactive.txt:69–86`: 전체 / native 원점과 clock 단위를 실행 시작 때 한 번 확정한 고정 context (샘플과 독립) 에 두고, 경과시간은 그 고정 값으로 계산한다.
   raw 에도 원점이 있으면 context 와 정확히 대조한다. 샘플 하나가 원점을 새로 정하거나 바꾸지 못하게 하고, 원점 부재 · 변경 · 다른 run / clock 기준은 명시 이유로 거부한다.
   상위 경계가 이를 보장한다고 할 거면 그 실제 호출 경로와 결속을 검증 대상에 넣는다 (주석으로 책임을 넘기지 않는다). 기존 수치 예산 · reserve 는 바꾸지 않는다.
2. **OPEN-R1-N2 (P2) · counter 항목 검사** — 같은 파일 49–58 · 96–104: 각 `process_counters` 항목의 타입 (dict) · 필수 키 · PID / creation 타입을 읽기 전에 검사하고, 전용 이유로 구조화된
   `STOP_REQUIRED` 를 돌려준다. `null` · scalar · 누락 키는 투영 단계의 실패로 기록하고 `assess_resources` 로 넘기지 않는다. 모든 예외를 PASS 나 정상 counter 로 바꾸는 수정은 안 된다.
3. **OPEN-R1-N3 (P2) · 검증안**:
   - C07-03: `assess_resources` 도달 요구를 없애고 "`project_owned_sample` 에서 `OS_QUERY_FAILURE` → `resource_decision` 이 `STOP_REQUIRED` · `assess_resources` 호출 0" 을 요구한다. 차단 코드를 약화해 뒤 함수에 억지로 도달시키지 않는다.
   - C04-03~05 의 양성 = C04-02 (non-null proof). C04-01 은 INCONCLUSIVE 분기 확인으로 따로 둔다.
   - C07-05 / 06 의 양성 = 같은 `advance_stop` 분기의 양성 (C07-04 의 같은 STOP_REQUESTED / 소유 · capability fixture 또는 별도로 명시한 양성). 판정 위치 (`transition.error` · `action` 등) 를 고정한다.
     강제 종료 *계획* 은 실제 강제 종료 관측이 아니다.
   - C08: property / equation / stored-grid 를 서로 다른 양성에 연결한다. C08-05 는 C08-04 의 stored-grid 양성을 기준으로 원 `checkShape` 의 `TIME_ORIGIN` 에 실제로 도달해야 한다 —
     하네스가 예외 문자열을 스스로 만들면 증거가 아니다.
4. **N1 / N2 사례 추가:** 같은 Job · 정상 counter 의 양성 / 원점만 이동한 음성 / 고정 원점 기준 실제 예산 초과 / 원점 부재 · 다른 clock 기준 / `[null]` · scalar · 키 누락 counter 의 음성 (`assess_resources` 호출 0).
5. **새 plan 과 manifest 로 봉인:** 확정 ID · 엔진 · 입력 · 기대 이유 · 반환 위치 · 필수 및 금지 도달 함수 · 양성 · 횟수 · 예산 · 실제 의존 함수와 예외 위치의 span · SHA · stub 경계.
   사례 수를 50 에 맞추지 않는다. 기존 R1 130 사례의 재실행은 요구하지 않는다.

## 3. 유지 · 하지 않는 것

- OPEN 4 그대로 · OS 수집기 미구현 그대로 · 기본 provider 의 OPEN 오류 차단 유지 · native argv / cwd · 승인 경로 null 유지. 몰래 완성하거나 true 로 채우지 않는다.
- `native_ready=false` · `approved=false` · `usable=false` · 전체 / 정상 gate INCOMPLETE. P0 실행 미승인 · 미세단락 효과 · K · 장시간 cohort 의 결과 주장 없음.

## 4. 회신 형식 · 전달

- `REPORT_KO.md` (N1–N3 · 고친 파일:줄 · 전 / 후 diff 요약) · 새 revision 전체 + 새 `CODE_MANIFEST.json` (준비본 대비 바뀐 파일 · sha256) · 갱신 검증안 (JSON + 설명) ·
  준비본 · R1 원본 불변 증거 (작업 전 / 후 sha) · 시간 기록 (새 monotonic 원점 · 단계 경계 · 상한 대비 · 마지막 쓰기 · 재읽기 뒤 snapshot 과 외부 반환의 범위 구분) ·
  `DECISION.json` (N1–N3 별 `fixed / partial / open` · 기능 검증 `NOT_RUN` · 실행 0 확인 · 정적 도구 사용은 따로 기록).
- ZIP 밖 기록 (영수증 · 포장 도구 반환 · 최종 확인 등) 은 모두 파일로 남기고 그 링크를 한 번에 알려 주세요.

---
