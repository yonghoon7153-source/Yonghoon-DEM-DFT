# R13 부분 리뷰 — 행별 입력 identity · 과학 재현성 메타데이터

대상: `94add7b5d48ad5d19448d562a0909b15ce4dc056`, 코드 정본 `c7217c04f939889e88b915575fce6997005072aa`.
담당: C01·C02·C03·C13·C16·C18·C33. `reviews/R13_REQUEST.md` 전문을 읽었다.

범위는 과학 산출의 구조·입력 identity 비교와 통상 producer/consumer 일관성이다. 보안 관련 주장은 정적으로만 읽었다. 실행 검사는 메모리 안의 합성 CSV/JSON 레코드에 한정했고, target·정본 산출·sidecar는 쓰지 않았다. 증거 runner와 기존 공격 스크립트는 실행하지 않았다. 아래 승격 경로에 관한 설명은 소스 흐름의 정적 함의이며, 승격 증명서를 발급하는 재현은 하지 않았다.

## 판정

이 범위에서도 요청문 §2의 반쪽 수정 패턴이 남아 있다. C01의 실제 행별 대조는 고쳐졌다. 그러나 C13/C16의 reference receipt 검증과 C33의 scale-audit 내용 검증은 끝나지 않았다. C18의 pandas 추가는 확인했지만, 필수 xlsx 엔진 버전이 환경 기록에서 빠진 것은 별도의 재현성 한계다.

| 항목 | 관찰 | 범위 내 결론 |
|---|---|---|
| C01 | 32행 matrix와 21행 profile의 순서 변경은 입력 차이 0; 첫 행의 target 입력 변경은 감지; matrix의 첫 reference 입력 변경도 감지 | 수정의 핵심 확인 |
| C02 | 같은 이름의 대응 산출에 대해 inode와 sidecar run_id를 검사함 (`check_u14.py:374`, `:384`) | byte-copy 차단 조건 정적 확인; 인증·독립 실행의 일반 증명으로 확대 해석하지 않음 |
| C03 | 세 필수 provenance 값에 `meta.get(k, _ABSENT) != want`를 적용 (`check_u14.py:353`) | 지워진 세 필드에 대한 분기 정적 확인 |
| C13 | `receipt_map(dict)`와 `receipt_map(JSON 문자열)`은 같음 | helper 수정 확인; reference schema 경로는 여전히 비대칭 (RI-01) |
| C16 | baseline에 reference가 있으면 새 산출의 누락은 문제, baseline만 없으면 대조 불가로 분리됨 | 두 쪽 모두 누락이면 검사가 사라지는 경우가 남음 (RI-01) |
| C18 | pandas의 버전 변경·누락 모두 `env_problems`가 보고 | pandas 수정 확인; openpyxl 기록 누락은 RI-03 |
| C33 | 빈 문자열은 거절하지만 빈 JSON 객체는 허용; audit 열은 여전히 수치 대조에서 제외 | 내용 보장은 미완 (RI-02) |

## RI-01 — P1: reference receipt를 candidate 자체의 필수 계약으로 검사하지 않는다 (C13/C16)

위치: [schema.py:417](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r13-target-wsl/bms-balancing/bms_balancing/schema.py:417), [check_u14.py:243](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r13-target-wsl/bms-balancing/scripts/check_u14.py:243).

`check_degeneracy`는 `ref_consumed_inputs`가 truthy이고 이미 dict일 때만 검증한다. 필수 키 검사는 `None`/빈 문자열만 누락으로 세므로 빈 dict는 통과한다. C16의 `_compare_roles` 수정도 첫 줄의 “양쪽 다 비면 return” 뒤에 있다. 따라서 reference가 없는 옛 baseline과 reference가 없는 candidate를 대조하면 새 산출의 계약 위반도, 입력 대조 불가도 기록되지 않는다. schema-only와 producer의 `check_degeneracy` 호출 역시 이 reference 누락을 검출하지 못한다.

직접 확인한 과학 schema 결과:

- 정상 degeneracy 레코드: 문제 `[]`.
- 그 레코드의 reference를 `{}`로 표현: 문제 `[]`.
- 양쪽 reference가 빈 레코드를 입력 비교: `(문제 [], 대조 불가 [])`.
- baseline reference가 정상이고 candidate만 비면: candidate 계약 위반 1건. 반대는 대조 불가 1건. 이 두 수정된 분기는 실제로 작동한다.
- reference의 half-cell locator가 빠진 dict: 문제 1건. 같은 reference를 JSON 문자열로 표현: 문제 `[]`. `receipt_map`의 정규화가 `check_degeneracy`에는 적용되지 않았다.

영향은 pristine reference를 먹었다는 증거가 없는 산출을 구조적으로 유효하다고 읽는 것이다. LAM/LLI는 target뿐 아니라 pristine 적합에도 의존하므로 “같은 입력의 재현” 결론을 뒷받침하지 못한다. 현재 `out/`의 degeneracy 4개는 모두 reference dict를 갖고 있음을 읽기 전용으로 확인했다. 따라서 현재 4개 baseline에 대해 candidate만 비우는 경우는 수정된 분기가 막는다. 미해결 범위는 baseline도 reference가 없는 지원 대상, schema-only, producer의 독립 구조 검사다.

수정 방향: candidate의 reference를 먼저 한 번 정규화하고, 빈 값·타입·역할·locator·hash 형식을 항상 검사한다. baseline의 스키마 연식은 candidate 검증을 생략할 이유가 아니다. 비교 helper의 양쪽 빈 값 분기도 candidate 누락을 먼저 처리해야 한다. 기존 `test_f08`은 schema가 먼저 막지 않음을 오히려 fixture 조건으로 고정한다 (`tests/test_r12_selfreview.py:271`); schema 자체 검사도 회귀에 포함해야 한다.

## RI-02 — P2: scale audit는 아직 “빈 문자열이 아닌 칸”에 머문다 (C33)

위치: [schema.py:253](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r13-target-wsl/bms-balancing/bms_balancing/schema.py:253), [schema.py:69](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r13-target-wsl/bms-balancing/bms_balancing/schema.py:69).

C33는 `MAY_BE_EMPTY`만 비웠다. 두 audit 열은 숫자 파싱 대상도 아니고, JSON/필수 metric 검증도 없으며, 계속 `ROW_SKIP`에 포함된다. 정상 32행 합성 matrix에서 첫 target audit를 빈 문자열로 두면 거절하지만, 빈 JSON 객체로 두면 `check_rows`가 문제 `[]`를 반환했다. audit record가 하나도 없는 경우를 필수 셀 존재로 처리하는 것이다.

이 audit는 장식용 주석이 아니다. `model.py:434`부터 표본 수·유한성·예외·raw 평균·eps 영향·동치 flag를 만들며, `FINDINGS.md:982`는 그 조건으로 포팅과 원본 설명식의 동치 범위를 한정한다. audit 내용이 빠져도 같은 과학 근거를 갖췄다고 읽으면 그 범위 주장을 검증할 수 없다. audit 내용의 변화도 현 비교기에서는 보고되지 않는다는 것은 `ROW_SKIP`와 `check_u14.py:434`의 흐름으로 확인했다.

fixture도 같은 맹점을 유지한다. `tests/test_review_findings.py:2747`의 공용 `matrix_row`는 두 audit의 기본값이 모두 `"{}"`이다. 새 `test_f22`는 두 상수 집합의 교집합만 검사하므로 이 fixture를 거절하지 않는다. 요청문 §6의 “fixture가 실제 invariant를 만족하게 고쳐졌다”는 설명을 audit 내용까지 확대할 수 없다.

수정 방향: audit JSON의 세 metric과 필수 필드, 개수 산술, 행의 scale/표본수와의 일관성을 검증하고, 감사 내용의 차이를 별도로 비교·보고한다. 비동치 실행을 무조건 숨기는 것이 아니라 실제 기록을 보존하면서 그 실행으로 주장할 수 있는 과학 범위를 명시해야 한다.

## RI-03 — P2, 정적 재현성 메타데이터 누락: openpyxl 버전이 기록·비교되지 않는다 (C18 인접)

위치: [provenance.py:53](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r13-target-wsl/bms-balancing/scripts/provenance.py:53), [schema.py:46](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r13-target-wsl/bms-balancing/bms_balancing/schema.py:46), [requirements.txt:7](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r13-target-wsl/bms-balancing/requirements.txt:7).

이 저장소는 openpyxl을 “pandas가 xlsx를 읽는 데 반드시 필요한 엔진”으로 명시하고, `openpyxl>=3.1`로 설치 범위를 열어 둔다. half/full-cell와 문헌 Gr 입력이 `pd.read_excel`을 통과하지만, `env_signature`와 `ENV_KEYS` 어느 쪽에도 openpyxl이 없다. 따라서 현재 산출만으로 그 필수 파싱 구성요소의 버전을 복원하거나 비교할 수 없다.

이는 C18의 pandas 추가가 실패했다는 뜻은 아니다. pandas 변경·누락 보고는 합성 환경 레코드로 확인했다. `test_f20`은 “현재 기록하는 key가 비교 목록에 포함되는가”만 보므로, 기록 자체에서 빠진 이 의존성은 검사하지 못한다. 여기서는 서로 다른 openpyxl 버전이 실제 수치를 바꾼다고 주장하거나 재현하지 않았다. 확인한 결함은 필수 파싱 환경의 기록 누락이다. 실제 사용한 xlsx 엔진과 그 버전을 공통 signature에 포함하고 비교하면 된다.

## Q5에 대한 범위 내 답

역할별 locator 변경을 정보로 보고하는 것은 bytes를 identity로 두는 R6 F1/F4와 충돌하지 않는다. C01의 동일 행 key·역할별로 old/new path를 표시하되 hash가 같으면 입력 identity 차이로 세지 않으면 된다. 현재 `receipt_paths`는 정보를 얻는 helper일 뿐 production 소비자가 연결된 상태는 아니다. C34를 닫지 않은 요청문의 판단이 맞다.

## 검증 기록

- 환경: WSL Ubuntu, `/home/yonghoon71/ddvenv/bin/python -B`, Python 3.12.3.
- 실행: `outputs/r13_receipt_identity_checks.py`에 read-only target 경로를 인자로 전달. 최종 exit code **0**. 추가 패키지는 이 stdlib/schema 검사에 필요하지 않았다.
- [검사 소스](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/r13_receipt_identity_checks.py), [실측 결과 JSON](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/r13_receipt_identity_results.json).
- 이 검사는 실제 fitting 숫자·원자료·MATLAB 동치를 검증하지 않는다. 전체 회귀와 다른 축의 결과는 총괄 리뷰에 합산한다.
