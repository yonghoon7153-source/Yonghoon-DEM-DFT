# 실행 담당 Codex 발송 프롬프트 — S1 OPEN-R1 변경부 한정 검증 (9 군 93 사례) · 2026-10-12

> **사용자가 §0 의 채택 문구를 승인한 뒤에만 보낸다.** 승인 전에는 초안이다. 원장 `COMSOL_REBUILD_SPEC.md` §87.
> §0 문구는 재검토 회신 (`REVIEW_KO.md` "남는 P2" · "다음 단계와 금지") 의 조건과 검증안의 명령 · 예산을 이 저장소가 승인문으로 옮긴 것이다 — 회신에는 채택 문구 초안이 없었다.
> 예산 1,350 초와 세션 수는 검증안의 원 제안 그대로다 (늘리지 않았다).
> 아래 `---` 사이가 붙여 넣을 본문이다. 같이 첨부: OPEN-R1 재검토 회신 zip (`COMSOL_MICROSHORT_S1_OPEN_CONNECTION_R1_REVIEW_20261011.zip` · 4,038,610 B · sha256 `4fcb4c32…432a`).

---

첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.

## 0. 승인 범위 (사용자 채택 문구 — 승인 시 원문 그대로 붙인다)

> S1 OPEN-R1 정정본 (zip sha256 `c9cf85b30f48fce0a8e747a8428b74b22a2d4c101498e2c0306720ed571fee0b` · CODE_MANIFEST sha256 `feb12ef6991141aab59fd2fbc0d5f0d138bdd735255aa7123274503ce80b8ecc` · 검증안 sha256 `6702a6be556f0f5b4512dd221c08f77d39111606f1d9f97511dd796f2d3d20c9`) 의 9 군 93 사례 변경부 한정 검증 한 건을 승인합니다. 먼저 재검토 회신의 두 메타데이터 정정 — ① 실행 순서: Python 1 세션에서 C01 → C02 → C03 → C04 → C05-01 · 02 · 03 · 07 · 04 · 05 · 06 → C06 → C07 → C09 (각 군의 나머지는 ID 순서), 그 뒤 javac 1 회와 Java helper 1 세션으로 C08-01~06 ② C03-04 · 05 의 양성 대조를 C03-02 로 (C03-02 는 그 분기의 양성, C03-03 은 C03-01 유지 · 입력과 기대값은 그대로) — 을 원 검증안보다 우선하는 봉인 부속서로 남기고 원 검증안 · 새 문서 · 고정 후보의 SHA 를 연결합니다. 이어서 새 하네스 · fixture · 실제 사용할 엔진 바이트 · 정확한 명령을 시험 전에 봉인한 뒤, 새 폴더 `C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/microshort_s1_open_connection_r1_20261010/proposed_changed_validation_001/` (이미 있으면 중지 · 삭제 · 재사용 · 다른 이름 우회 없음) 에서 위 순서대로 Python 87 사례 (1 세션) 와 Java helper 6 사례 (javac 1 회 + 1 세션) 만 실행합니다. 상한은 새 원점 총 1,350 초 (하네스 봉인 600 · Python 180 · javac 90 · Java helper 60 · 보존 · 전달 300 · 미완 정리 120) 이고 단계 사이 전용 · 자동 확대 · 세션 추가는 없습니다. 첫 예상 밖 실패나 시간 초과에서 멈추고 남은 모든 엔진 · ID 는 NOT_RUN 으로 남깁니다 — 수정 · 재시험 · 다른 shell · 기존 130 사례 재개는 하지 않습니다. 생산 코드 · 정정본 · 원 R1 · 준비본 · 기존 기록은 바꾸지 않습니다. javac / java 는 이 helper 에만 쓰고, COMSOL 모델 컴파일 · COMSOL / native 계산 · 설치본 관측 · OS 수집기 · Job · 정책 변경 · approval / release / runtime / token 생성은 승인하지 않습니다. 결과와 원문을 제출한 뒤 멈춥니다.

## 1. 고정 식별

| 대상 | 식별 |
|---|---|
| 정정본 | zip 4,011,062 B · sha256 `c9cf85b3…ee0b` · PACKAGE_MANIFEST sha256 `045bcfc47bdd5571ba045df5b60f700b07292775239af8f2de03f1d2205a7392` (117) · CODE_MANIFEST `feb12ef6…8ecc` (14) · resource source sha256 `f45e6531383d03daa2e968437c6188be0229c144c6956647b0b0f81fae795816` — 폴더 `…/outputs/microshort_s1_open_connection_r1_20261010/` |
| 원 검증안 (그대로 둠) | `LIMITED_VALIDATION_PLAN.json` · 178,519 B · sha256 `6702a6be…20c9` · 9 군 93 사례 (C01 7 · C02 6 · C03 5 · C04 5 · C05 7 · C06 8 · C07 6 · C08 6 · C09 43) · Python 87 · Java helper 6 |
| 재검토 회신 | `COMSOL_MICROSHORT_S1_OPEN_CONNECTION_R1_REVIEW_20261011.zip` · 4,038,610 B · sha256 `4fcb4c3216fa4bc8c38277d68682fb2b24e732a4c9e512896dca0ca7571e432a` (판정 `STATIC_CORRECTIONS_ACCEPTED_WITH_PLAN_METADATA_CONDITIONS`) |
| 새 폴더 (하나) | `…/outputs/microshort_s1_open_connection_r1_20261010/proposed_changed_validation_001/` — 정정본 폴더의 기존 파일은 바꾸지 않는다 |
| 명령 (검증안 `commands` 그대로 · 각 1 회) | Python: `…/codex-primary-runtime/dependencies/python/python.exe -I -S -B -X utf8 …/proposed_changed_validation_001/run_python.py` (180 s) · javac: COMSOL 동봉 JRE `javac.exe -proc:none -d …/classes …/OpenReadbackHarness.java` (90 s) · Java helper: 같은 JRE `java.exe -cp …/classes OpenReadbackHarness` (60 s) |

## 2. 순서 · 양성 (재검토 회신 조건 그대로)

- **Python 1 세션:** C01 → C02 → C03 → C04 → C05-01 / 02 / 03 / 07 / 04 / 05 / 06 → C06 → C07 → C09. 각 군의 나머지는 ID 순서.
- **그 뒤에만:** javac 1 회 → Java helper 1 세션 C08-01~06. 앞 단계가 정상으로 끝나지 않으면 javac 도 실행하지 않는다.
- **C03 양성:** C03-04 · 05 → C03-02 · C03-02 는 그 분기의 양성 · C03-03 → C03-01. 입력 · 기대 이유 · 사례 수는 그대로.
- 부속서는 원 검증안보다 우선한다고 명시하고, 원 계획 SHA (`6702a6be…`) · 부속서 SHA · 고정 후보 SHA 를 함께 봉인한다. 옛 봉인본은 고치거나 지우지 않는다.

## 3. 봉인 · 중지 · 기록

- 시험 전에 하네스 · fixture · 정확한 명령 · 실제 사용할 엔진 (python.exe · javac.exe · java.exe) 의 바이트를 봉인한다. 검증안의 엔진 식별은 과거 관측 pin 이므로, 실제 바이트와의 일치 여부를 함께 기록한다.
  엔진을 바꾸거나 설치 · fallback 하지 않는다.
- 첫 **예상 밖** 실패나 시간 초과에서 멈추고 남은 엔진 · ID 를 NOT_RUN 으로 남긴다. 선언된 예외를 정확히 포착하는 음성 사례는 예상 밖 실패가 아니다. 하네스가 기대 예외 문자열을 스스로 만들어 내면 증거가 아니다.
- 사례마다 ID · 엔진 · 입력 식별 · 기대 / 관측 이유 · 반환 위치 · 필수 / 금지 도달 함수 · 양성 연결 · raw stdout / stderr / rc 를 남긴다. 같은 사례 안의 복수 호출을 별도 사례로 세지 않는다.

## 4. 유지

통과해도 OPEN 4 (설치본 t0 · 설치본 계수 · raw native 증거 어댑터 · OS 자원 / 소유 / 중지 어댑터) 는 닫히지 않는다. `native_ready / approved / usable = false` · native argv / cwd / 승인 경로 null ·
전체 / 정상 gate INCOMPLETE · 실효 정책 / 실제 코어 UNVERIFIED 유지. 설치본 관측 · P0 · S1-P · K · 장시간 cohort · 미세단락 효과 결과는 이 승인에 들어 있지 않다.

## 5. 회신 형식 · 전달

- `RESULT_KO.md` · 사례별 결과표 (93 행 · PASS / FAIL / NOT_RUN) · raw 출력 · 봉인 기록 (부속서 · 하네스 · fixture · 엔진 · 명령) · 원본 불변 증거 (전 / 후 sha) ·
  시간 기록 (새 monotonic 원점 · 단계 경계 · 상한 대비 · 마지막 쓰기 · 재읽기 뒤 snapshot 과 외부 반환의 범위 구분 · 도구 wall time 미합산) · `DECISION.json`.
- ZIP 밖 기록 (영수증 · 포장 도구 반환 · 최종 확인 등) 은 모두 파일로 남기고 그 링크를 한 번에 알려 주세요.

---
