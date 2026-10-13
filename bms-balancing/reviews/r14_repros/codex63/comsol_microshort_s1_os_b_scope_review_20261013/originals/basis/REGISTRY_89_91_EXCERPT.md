# 원장 발췌

고정 ref c134f8b21ccd360715efbfbd0cad66068429341e · 원 파일 Git blob e224696c8ca37ce2894842878ea0eecbf6be1bf2 · 시작 원문 4503행. 발췌본이며 원 파일 전체 바이트가 아니다.

## 89. 93 사례 한정 검증 `_003` 결과 — 검토 회신 접수: `LIMITED_VALIDATION_ACCEPTED_WITH_DOCUMENTED_SCOPE` · P1 0 · 보존 구간 부속 정정 1 (2026-10-13 · 실행 0)

- **보존:** `reviews/r14_repros/codex63/comsol_microshort_s1_open_r1_003_review_20261013/`
  - 회신 zip 38,949 B · sha256 `879cff578dfa52a7dcf0c008cded5f42698bb3b2916570b9e4b5da0b31e10d17` (사용자 업로드 원파일과 바이트 동일).
  - `originals/` 17 · PACKAGE_MANIFEST 16 / 16 일치 · 비밀 0. 동봉 스크립트 (`review_intake.py` · `review_counts.py` · `package_review.py`) 는 실행하지 않았다.
  - 규칙 커밋 `dbcbc678` → 보존 커밋 `d02ea278` (blob 18 / 18 일치).
- **이 저장소에 없는 것:**
  - 실행 결과 zip `COMSOL_MICROSHORT_S1_OPEN_R1_VALIDATION_003_20261013.zip` (665,105 B · `6458419127231ce44203ddef9d10981954ae877fdbf990faab5d3649db172bb3`).
  - 보충 zip `COMSOL_MICROSHORT_S1_OPEN_R1_PYTHON_PREFLIGHT_20261013.zip` (53,751 B · `45bdff07b0db0d24f96766e6224807822ddae6278405a663924c4080edbb8fe8`).
  - ZIP 밖 영수증 · 포장 반환 · 최종 확인의 원파일 (회신 `USER_SIDECAR_RECONCILIATION.json` — 사용자가 붙여 넣은 전사로 대조 · 원바이트 미대조).
  - 포장 후 AFTER 원파일 (34,659 B · `b22417b5…57e4d`) 만 회신 안에 바이트로 들어 있다. 이 저장소에서도 sha 가 일치한다.
- **경위 (출처 구분):** 사용자가 §88 의 발송문과 재검토 zip 을 실행 Codex 에 보냈다. 이 저장소는 그 대화를 보지 못한다. 검토 회신이 연결을 확인한 것
  (보존된 승인 기록을 읽은 것 · 검토자가 대화 원본을 감사한 것은 아님): `_001` FIRST_ERROR (사전 관측 구간) → `_002` 새 Python 승인 · 중지 →
  `_003` "다시 ㄱ" 재개.
- **판정 (회신 `DECISION.json` · `REVIEW_KO.md`):** `LIMITED_VALIDATION_ACCEPTED_WITH_DOCUMENTED_SCOPE` · 기능 검증 수용 · 차단 발견 0 · 재시험 ·
  재포장 · 생산 수정 요구 0.
  - 93 사례: C01 7 · C02 6 · C03 5 · C04 5 · C05 7 · C06 8 · C07 6 · C08 6 (Java helper) · C09 43 → PASS 93 · FAIL 0 · 최종 NOT_RUN 0.
    Python 원시 `not_run=6` 은 Python 단계가 끝날 때 아직 돌지 않은 Java 6 이다 (Python 사례 누락 아님).
  - Python 대조 항목: 계획상 호출 횟수 기대 331 · 명시 금지 함수 횟수 136 (항목 수이지 총 호출 수가 아님) · 불일치 0. Java 원문 구간 12 바이트 일치 ·
    helper 24,285 B (`4664c984…a639`).
  - 식별: CODE_MANIFEST `feb12ef6…8ecc` (= §87 정정본) · 유효 검증안 `88a56e55…34e5` · CASE_RESULT_MAP `b220139a…a2cd`.
  - 엔진: Python 1 세션 · javac 1 · JVM 1 · 자식 rc 전부 0. Python 3.12.14 · 106,448 B · `10d845f5…79d1` (과거 107,312 B `b7a12c3a…` 는 이전
    기대값 — 엔진 교체를 같은 바이트로 처리하지 않았다). 기록된 실행 식별이지 검토자의 새 측정이 아니다.
- **시간 (제출자 기록 · 검토자 대조):**

  | 단계 | 기록 | 한도 |
  |---|---:|---:|
  | 하네스 사전 봉인 | 499.0560668 s | 600 s |
  | Python 한 세션 (외부 stage) | 10.8930094 s | 180 s |
  | Java helper 컴파일 1 회 | 1.7277404 s | 90 s |
  | Java helper JVM 1 세션 | 0.5369169 s | 60 s |
  | 마지막 최종 확인 snapshot | 809.8249618 s | 전체 1,350 s |
  | 같은 최종 확인의 전달 경과 | 248.7441909 s | 300 s |

  회신 원문 (경계): "최종 809.8249618/1,350초 및 전달 248.7441909/300초는 확인 파일 쓰기·재읽기·해시 후, 도구 반환 전 snapshot으로 수용합니다.
  마지막 전사 저장/반환까지의 관측이라고 쓰지 않고 도구 wall time을 더하지 않습니다."
- **부속 정정 S1-003-P2-01 (원 봉인본 수정 없이 · 회신 원문 그대로 접수):**
  - 대상: 결과 묶음의 `REPORT_KO.md:14` · `RESULT_SUMMARY.json:108` · `ENGINE_PATH_APPROVAL_ADDENDUM.json:25-29` 의 `_001·_002 보존` 문구.
  - 회신 (`CLAUDE_REPLY_KO.md`): "`_003`의 114개 전후 보존에는 `_002` 선택 파일 33개가 포함됩니다. `_001 FIRST_ERROR`는 추가 사전 관측 ZIP에서
    원문과 당시 전후 보존을 확인했습니다. 그 구간은 10월 13일 02:04–02:07 KST이며 `_003` 전후 보존 증명이 아닙니다. `_001`이 이번 114개에서
    빠진 점은 미확인으로 남기고 현재 재측정으로 소급 보충하지 않습니다."
  - 상세 (`REVIEW_KO.md`): "`_002` 선택 기록은 `_003`의 114개 전후 대조에 포함된다. `_001 FIRST_ERROR.json`은 별도 사전 관측 ZIP에서 원문과
    당시 전후 기록을 확인했다. 그러나 `_003`의 114개에는 없으므로 `_003` 실행 전후 불변은 미확인이다. 변조됐다는 뜻은 아니며 현재 해시를 새로
    재어 과거 구간을 메우지 않는다."
  - `_001` 원문 식별: 1,448 B · `df14d1c1…0269` · 사전 관측 구간 2026-10-13T02:04:13.8117324+09:00 – 02:07:28.2691467+09:00. 기계 전체 보존은
    검증하지 않았다 (`whole_machine_preservation_verified=false`).
  - 이 정정은 기능 93 사례 수용을 막지 않는다. 이전 중지 · 실패 기록을 PASS 로 다시 쓰지 않는다.
- **확대하지 않는 것 (회신):**
  - 설치 COMSOL API 호환성 · OS 어댑터 · 실제 OS 소유 / 자원 / 중지 동작. Java 의 type / model / FeatureInfo / NumericalFeature 는 stub 이다.
  - C08-04 의 저장 시각 0 은 일관 초기화 직후의 증명이 아니다 (`POST_CONSISTENCY_PROOF_OPEN`).
  - C05 의 합성 proof provider 가 설치본 관측을 대신하지 않는다. C09 의 고정 문맥은 코드 계약이고 OS clock 진실성이 아니다.
  - microshort 물리 효과 · 설치본 t0 · 실효 계수 · native → Parent 생산 연결.
- **검토자 자체 도구 오류 1 (공개):** 첫 JSON 집계가 Java stdout 요약 footer 를 사례로 읽어 KeyError (chunk `ce990e`). 수신 시험 실패가 아니고,
  검토자 정적 대조만 다시 했다 (`REVIEW_ACTIVITY_NOTE.json`).
- **상태 유지:** OPEN 4 — ① 설치본 일관 초기화 직후 t0 · ② 생성식 ↔ 실제 설치 계수 · 변수 / API 결속 · ③ native 원시 증거 → 소비자 · Parent
  어댑터 · ④ 실제 OS 자원 · 소유 · 중지 어댑터. `native_ready / approved / usable = false` · 전체 / 정상 gate INCOMPLETE · 실효 정책 / 실제 코어
  UNVERIFIED. Parent manifest 세대 연결 · quadrature bound 등 하위 미완도 OPEN 지도 그대로다.
- **다음 (사용자 결정):** 네 OPEN 중 먼저 닫을 항목의 **설치본 관측 및 연결 구현 범위 · 검증안**을 따로 고정하는 제안 (초안 작성 여부 · 어느 항목부터).
  이 회신은 그 구현 · 설치본 관측 · P0 · COMSOL / native 실행의 승인이 아니다. 회신 지시대로 실제 계산 없이 멈춘다.

## 90. 다음 OPEN 해소 범위 — 제안 초안 작성 승인 (2026-10-13 · 사용자 "3번도 권고대로" · 문서만 · 계산 0)

- **물음 (§89 보고):** "COMSOL: 남은 OPEN 4개 중 어느 것을 먼저 닫을지 범위 제안 초안을 쓸지 정해 주세요. 계산 없이 문서만 씁니다. 저는 쓰기를
  권합니다. 네 항목 사이의 의존 관계를 먼저 정리하고, 첫 항목을 골라 제안하는 방식입니다."
- **사용자 (2026-10-13):** "3번도 권고대로" → 초안 작성 승인 (문서 · 계산 0).
- 초안은 검토 Codex 의 범위 검토를 거친다. 실행 승인 여부는 그 뒤 사용자가 정한다.
- 이 절은 구현 · 설치본 관측 · P0 · COMSOL / native 실행 승인이 아니다. OPEN 4 · `native_ready=false` 는 그대로다.

## 91. 다음 OPEN 해소 범위 — 제안 초안 (검토 발송 대기 · 2026-10-13 · 문서만 · 실행 0 · 네트워크 0)

- **두 문서:**
  - 검토 요청문 `docs/COMSOL_MICROSHORT_S1_OPEN_NEXT_SCOPE_PROPOSAL_20261013.md` (sha256 `a7e376074cd97195e63098ccd25a921e678538ba0c6e880eaba1934dadd3b5ef`).
  - 실행 발송문 초안 v1 `docs/COMSOL_MICROSHORT_S1_OS_B_SEND_20261013.md` (sha256 `2181ddf1faca7b416eac709ebc7bc6f217f5c1522b7fa46089240b603a04c095` · §0 채택 문구 초안 · 승인 전에는 초안).
- **네 OPEN 의 의존 (문서 근거):**
  - 준비본 별도 허용 초안 A–E — A 는 `_003` 으로 수용 · 다음이 B.
  - S0 범위안 §5 "이 항목 미정이면 native 승인 불가" (RAM/commit 감시 · 소유 Job 종료).
  - C → mapping 봉인 → D (한 P0 runAll 안에서 ① ② ③ 관측).
  - E 는 collector · mapping 고정과 inert 검증 수용 뒤.
  - ③ provider 는 ① ② 없이 지나지 못한다 (`UnavailableInstalledProof`).
- **제안:** 첫 항목은 ④ OS 자원 · 소유 · 중지를 B 단계부터 한다.
  - B 의 범위: 공식 근거 대응 · 비활성 provider 후보 · 변경부 검증안 작성만 · 새 원점 3,600 초 · 새 폴더 1.
  - 프로세스 · Job 생성과 OS API 호출 시험은 0 이다.
  - 이유: COMSOL 없이 끝까지 닫히는 유일한 OPEN · native 승인 문턱 · 다른 OPEN 에 기대지 않음 · A–E 순서.
  - REIL C4-N2 · N3 와 같은 표본기 결함 유형을 검증안 규칙에 넣었다.
- **사용자 · 검토자가 고를 것:**
  - 근거 문서: (a) 실행 PC 의 공식 URL 열람 또는 (b) 이 저장소가 사본 묶음을 받아 첨부 — 권장 (b). (b) 의 fetch 는 아직 하지 않았다.
  - 검토 질문 Q1–Q7 (Q5: C 에도 §5 조건이 걸리는가 · Q6: D 가 곧 P0 인가 포함).
- **다음:** 사용자가 검토 요청문 + 실행 발송문 초안을 검토 담당 Codex 에 보낸다 → 회신 반영 v2 → §0 채택 (사용자) → (b) 면 문서 묶음 작성 → 실행 담당 Codex 발송.
  이 절은 B 착수 · 설치본 관측 · OS 시험 · COMSOL / native 실행의 승인이 아니다.

