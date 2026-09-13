# R13 α·β 검증 하네스 리뷰 — NO-GO

대상은 `bms-balancing/`이다. 이전 degradation-degeneracy 게이트나 COMSOL 검토의 판정을 이어 붙인 것이 아니다.

## 1. 판정과 검토 범위

**NO-GO — 현행 정본을 새 모델의 검증된 설계 근거로 승격할 수 없다.**

행별 입력 비교(C01)는 실제로 개선됐다. 그러나 이번에도 **두 산출물이 서로 같다는 것과, 각각이 올바른 과학 산출이라는 것을 혼동하는 자리**가 남았다. 잘못된 모집단을 두 번 적으면 승격 가능이고, reference receipt가 양쪽 모두 없으면 candidate의 필수 계약까지 사라진다. 감사 자료의 경우 빈 문자열을 막았지만 빈 객체는 여전히 감사로 인정한다.

아래 신규 항목은 **P1 4건, P2 5건**으로 묶었다. 모집단의 γ·matrix 변형은 하나의 P1에 합쳤다. 실행 관측, 보관 파일 관측, 정적 판단을 구분한다. 이미 신고한 미결을 새 발견으로 다시 세지 않았다. `ne_shape`는 신고된 Q6에 대한 추가 실측으로 별도 분리했다.

| 구분 | 확인한 대상 |
|---|---|
| 요청/리뷰 HEAD | `94add7b5d48ad5d19448d562a0909b15ce4dc056` |
| HEAD tree | `10541cf460c0fe4a7a93f8faa67268f420a7bf78` |
| 코드 정본 | `c7217c04f939889e88b915575fce6997005072aa` |
| 코드 차이 | 코드 정본→HEAD의 `*.py`, `*.sh` 차이 0개 |
| 첨부 요청문 | checkout의 `reviews/R13_REQUEST.md`와 SHA-256 동일: `1b352e3eb0abc18d2986329ce8269a4b770b14c269712e80b97edd57f3f42b34` |
| 작업트리 | 검토 후 `git status --short` 출력 없음. 대상 코드·정본 산출 수정 없음 |

보안 관련 import/bytecode/filter 우회 재현과 보관된 공격 재생은 실행하지 않았다. 해당 영역은 소스와 보관 증거의 읽기 전용 검토로 한정했다. 따라서 이 보고서는 전체 보안 경계 검증서나 236개 전수 통과 증명서가 아니다. 아래 과학 데이터 검사는 일반 합성 CSV/JSON과 정상 CLI 호출만 사용했다.

## 2. 직접 실행한 결과

| 검사 | 이번 기계에서 관측한 결과 |
|---|---|
| 선택 회귀 | **226 passed, 10 deselected in 117.63s** |
| MATLAB 보조 검사 | Octave 없음: 1~3단계 미실행. 4·5단계 각각 PASS, 전체 wrapper rc 0. MATLAB/Octave 실행 성공으로 해석하지 않음 |
| 현행 `out/` schema-only | **실제 자식 rc 2**, `promotion_eligible: false`; 요청문의 59·27·5·1과 일치 |
| 행별 identity 검사 | matrix/profile 순서 변경은 차이 없음; 첫 행 target 변경 감지; matrix 첫 reference 변경 감지 |
| 과학 schema/CLI 합성 검사 | 아래 실패 사례와 정상 대조군을 함께 실행. 각 사례의 stdout/stderr/입력 보존 |
| 보관 증거 수동 실행 없는 감사 | 보고서 5개 JSON 파싱, 보관 패키지 manifest **44/44** 해시 일치. 과거 실행 결과를 새로 실행한 것으로 세지 않음 |

환경: WSL2 Ubuntu, Python 3.12.3, NumPy 2.5.3, SciPy 1.18.1, pandas 3.0.5, pytest 9.1.1, openpyxl 3.1.5. 원자료·원본 MATLAB·문헌 OCP를 사용한 fitting은 실행하지 않았다. 외부에 설치돼 있던 의존성을 사용했고 대상에 설치/수정하지 않았다.

선택 회귀의 제외식은 다음과 같다. 이 10개를 통과·실패·환경상 불가로 바꾸어 세지 않는다.

```text
not d10_12 and not d10_13 and not d10_14 and not e11_09 and not e11_10
and not e11_17 and not e11_18 and not d8_07 and not d9_08 and not d7_05
```

합성 비교의 의미도 한정한다. 모집단 사례에서는 양쪽에 같은 잘못된 과학 구조를 주고 서로 다른 run ID를 사용했다. 이는 **candidate 독립 유효성 검사의 실패**이지, 올바른 완전 baseline과 다른 candidate의 행 차이를 숨겼다는 증명이 아니다. 실제 producer가 그 잘못된 모집단을 생성했다고도 주장하지 않는다. 합성 receipt·sidecar는 검사 계약용 자료이며 실제 과학 계산의 출처 증거가 아니다.

## 3. 신규 P1

### P1-1. C04/C05 — 정본 모집단의 개수는 확인하지만 구성원은 독립적으로 정하지 않는다

위치: [schema.py:332](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r13-target-wsl/bms-balancing/bms_balancing/schema.py:332), [schema.py:376](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r13-target-wsl/bms-balancing/bms_balancing/schema.py:376).

실행 증거: `r13_roster_schema_results/results.json`의 아래 세 case 모두 `schema_problems: []`, **rc 0, promotion true, blocker 전부 0**.

| case | 만드는 상태 | 정본 계약상 필요한 결과 |
|---|---|---|
| `profile_wrong_grid` | γ 21개를 0~0.4, 간격 0.02로; authority/requested/succeeded=21, missing=[] | 거부. 실제 producer는 0~0.5의 21점 |
| `matrix_self_declared_one_row_authority` | state 100에 GITT/Li/w=0 한 행; authority=requested=succeeded=1 | 거부. state 100의 독립 모집단은 32조합 |
| `matrix_wrong_member` | 32행이지만 한 Si 이름을 미등록 `Li2`로 | 거부. 개수뿐 아니라 선언된 Si 집합과 일치해야 함 |

근거: [verify.py:1457](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r13-target-wsl/bms-balancing/bms_balancing/verify.py:1457)의 matrix authority는 source×Si×weight를 독립 산출한다. [verify.py:1651](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r13-target-wsl/bms-balancing/bms_balancing/verify.py:1651)의 γ 격자는 model의 0~0.5 범위를 사용한다. 소비자는 이 집합들을 쓰지 않고 artifact의 count끼리만 대조한다.

회귀도 같은 맹점이다. `test_f09`의 정상 γ fixture는 0~1이고, `test_f10`은 authority=2의 두 행을 정상 full 모집단으로 취급한다. 정상 production 계약을 벗어난 예가 정상 대조군이다.

최소 종결 조건: state별 canonical 조합/γ 값을 공유 계약으로 정의하고 **각 candidate의 exact key set**을 검사한다. 위 세 case는 구조/모집단 사유로 거절하고 실제 21점·32조합 대조군은 통과해야 한다. 별도로 관측한 missing/partial 사례는 신고된 partial 수명 문제와 겹치므로 새 발견으로 더 세지 않았다.

### P1-2. C13/C16 — reference receipt가 양쪽 모두 없으면 candidate 계약도 검사하지 않는다

위치: [schema.py:412](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r13-target-wsl/bms-balancing/bms_balancing/schema.py:412), [check_u14.py:243](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r13-target-wsl/bms-balancing/scripts/check_u14.py:243).

직접 CLI 관측 (`r13_cli_contract_results_v3/results.json`):

| case | 실제 결과 |
|---|---|
| `candidate_reference_receipt_empty` — candidate만 `{}` | rc 2, inputs=1: **수정된 분기 작동** |
| `baseline_reference_receipt_empty` — baseline만 `{}` | rc 4, inputs_uncomparable=1: **수정된 분기 작동** |
| `both_reference_receipts_empty` — 양쪽 `{}` | **rc 0, promotion true**, inputs=0, inputs_uncomparable=0 |
| `reference_receipt_string_missing_locator` | half-cell path가 빠진 reference를 양쪽 JSON 문자열로 표현하면 **rc 0, promotion true** |

`check_degeneracy`는 reference가 truthy dict일 때만 검증한다. 빈 dict는 필수 key 검사에도 걸리지 않는다. 같은 불완전 reference가 dict이면 path 누락을 보고하지만 문자열이면 검증 자체를 생략한다. helper의 정규화가 schema 경로에 적용되지 않았다. 이어 비교 helper는 양쪽이 빈 경우 즉시 return한다.

현재 `out/`의 reference가 있는 네 degeneracy에 candidate만 누락시키는 경우가 다시 열렸다는 주장은 아니다. **legacy/missing-reference baseline을 지원하는 영역, schema-only, candidate 자체 유효성**이 미완이다. pristine 적합을 이용하는 LAM/LLI의 출처 근거를 무효화한다.

최소 종결 조건: candidate의 reference는 baseline 나이와 무관하게 한 번 정규화한 후 필수 역할·path·hash를 검사한다. 양쪽 누락도 candidate 계약 위반이어야 한다. C16의 현재 회귀는 schema가 빈 reference를 막지 않음을 fixture 조건으로 고정한다. 그 전제를 제거하고 schema 단독 검사와 CLI를 함께 시험해야 한다.

### P1-3. 보관 증거 — 미해결 범주가 있는데 `closed:true`와 “모든 case 닫힘”을 기록한다

이 항목은 **보관 JSON과 rc 파일을 직접 읽은 관측**이다. 공격 재생을 실행해 만든 결과가 아니다.

| 보관 보고서 | `반례 소멸` | 남은 상태 | 전체 `closed` / rc |
|---|---:|---|---|
| R7 | 5 | 전제 변경 1 | true / 0 |
| R10 | 20 | 전제 변경 1, 우리 코드 밖 1 | true / 0 |
| R11 | 32 | 전제 변경 2개 record, 환경상 불가 1 | true / 0 |

R10/R11의 `rc_reason`은 실제로 **“모든 case 가 닫혔다”**다. 요청문 §1/§5의 “전제 변경·환경상 불가는 닫힘으로 세지 않았다”와 기계용 결론이 다르다.

원인은 [R7 runner:263](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r13-target-wsl/bms-balancing/reviews/r7_repros/replay_codex_r7.py:263), [R10 runner:301](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r13-target-wsl/bms-balancing/reviews/r10_repros/replay_codex_r10.py:301), [R11 runner:420](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r13-target-wsl/bms-balancing/reviews/r11_repros/replay_codex_r11.py:420)의 집계 정책이다. C19의 evidence eligibility 검사 추가는 실제 수정이지만 이 의미 불일치를 닫지 않는다.

최소 종결 조건: 실행 유효성, 개별 조건 도달/판정, 적용 제외, 전체 종결을 별도 필드로 둔다. 미실행/전제 변경은 대체 증거 없는 상태에서 `closed:true`의 근거가 될 수 없다. rc 0을 “보고 작업 완료”로 정의하려면 `rc_reason`도 그 뜻이어야 하며 GO 소비자는 별도 완결 판정을 읽어야 한다.

### P1-4. C08 — 격리 재실행보다 의존성 import가 먼저다 [정적]

위치: [R7 runner:23](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r13-target-wsl/bms-balancing/reviews/r7_repros/replay_codex_r7.py:23). R9/R10/R11에도 같은 순서가 있다.

소스상 의존성 import 뒤에 재실행 조건을 검사한다. 따라서 “어떤 import보다 먼저 경계를 세웠다”는 주장에는 맞지 않는다. 또한 재실행 predicate는 요구된 격리 상태 전체가 아닌 일부 flag만 확인한다. `test_f13`은 `import evidence_gate` 앞에 문자열이 있는지만 읽으므로 초기 import 순서를 입증하지 않는다.

이는 **정적 미종결 판단**이다. 이번에 변조된 인증서나 실행 우회를 재현했다고 주장하지 않으며 재현 코드를 제공하지 않는다.

최소 종결 방향: 필요한 격리 상태로 시작한 launcher가 의존성을 읽도록 하고, 실행 entrypoint와 시험용 helper를 분리한다. 증거를 발행하는 entrypoint는 필요한 초기 상태 전체를 확인해야 한다. 소스 문자열의 존재 대신 초기화 순서/환경 계약을 검증해야 한다.

## 4. 신규 P2

### P2-1. C06 — 유한성 검사 전에 과학 값의 타입·모양 계약이 없다

[schema.py:388](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r13-target-wsl/bms-balancing/bms_balancing/schema.py:388)은 bool, 숫자로 파싱되지 않는 문자열, 빈 list/dict를 허용한다. `best_obj="not-computed"`, `best_p=[]`, `LLI_percent={}`는 schema=[]이며 반복 산출 비교가 승격 가능이다.

더 직접적인 사례는 `degeneracy_boolean_vs_numeric_baseline`: **정상 scalar `best_obj=1.0`에서 candidate만 `true`로 바꿔도 rc 0/promotion true**. [check_u14.py:282](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r13-target-wsl/bms-balancing/scripts/check_u14.py:282)의 float 비교가 둘을 같게 읽는다.

최소 조건: numeric 필드에서 bool/비수치 문자열 거부, parameter vector 길이 5, 통계 object 필수 key 검증. 그 다음에 유한성을 검사한다. `1e999`를 막은 수정 자체는 인정한다.

### P2-2. C33 — 감사 자료를 빈 객체로 바꾸어도 비교에서 보이지 않는다

[schema.py:60](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r13-target-wsl/bms-balancing/bms_balancing/schema.py:60)의 audit는 nonnumeric이고, [schema.py:68](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r13-target-wsl/bms-balancing/bms_balancing/schema.py:68)에서 여전히 비교 제외다.

`complete_audit_control`은 producer 모양의 3 metric·50 표본·scale/eps에 맞춘 양쪽 감사 자료로 rc 0이었다. **그 candidate의 audit 두 열만 `{}`로 바꾼 `candidate_audit_empty_object`도 rc 0/promotion true**였다. 표본·유한성·eps 영향에 대한 근거가 사라져도 차이를 기록하지 않는다. 빈 문자열 거부는 작동하지만 이것은 감사 내용 검증이 아니다.

최소 조건: audit JSON의 metric/필드/타입/산술/scale 결속을 검사하고 감사 내용 차이를 별도 보고한다. `MAY_BE_EMPTY ∩ ROW_SKIP == ∅`인지만 확인하는 f22로는 부족하다.

### P2-3. C32 — 반환형을 고친 helper에 도달하기 전에 CLI가 BOM JSON에서 죽는다

`bom_json_schema_only`: 정상 degeneracy JSON에 UTF-8 BOM을 붙이고 파일 checksum을 정확히 기록. 묶음 reader는 읽지만 [check_u14.py:331](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r13-target-wsl/bms-balancing/scripts/check_u14.py:331)에서 `JSONDecodeError`.

관측: **자식 rc 1, PROMOTION 없음**, stderr 마지막 줄은 `Unexpected UTF-8 BOM (decode using utf-8-sig)`. 스키마 오류의 구조화된 rc 2도, 문서상 rc 1인 숫자 불일치도 아니다. 실패를 성공으로 바꾸는 결함은 아니지만 자동 소비자가 실패 원인을 분류할 수 없다.

최소 조건: JSON bytes decoding/parse를 공유하고 BOM을 지원하거나 명시적 구조 오류로 반환한다. helper 직접 호출뿐 아니라 전체 CLI에서 결과 형식과 rc를 검증한다.

### P2-4. schema-only가 필수 환경 축 누락을 스키마 문제로 보지 않는다

`schema_only_missing_env_fields`: 정상 candidate의 sidecar env에서 Python만 남기고 NumPy/SciPy/pandas/platform 제거. **rc 0**, `blocked_by.schema=0`, `blocked_by.env=0`. promotion은 false이므로 이것을 승격 우회라고 세지 않는다.

[check_u14.py:347](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r13-target-wsl/bms-balancing/scripts/check_u14.py:347)는 env가 비어 있지 않은 dict인지만 보고, 필수 key 검사는 비교 모드에서만 한다. C18의 pandas 비교는 작동하지만 **완성된 묶음 스키마 검사**는 여전히 비대칭이다.

최소 조건: required env key의 존재/타입/비어 있지 않음은 모든 candidate에서 검사한다. old/new 값의 같음만 비교 모드에 둔다.

### P2-5. 증거의 예외 fingerprint와 개별 조건 명부가 충분히 구체적이지 않다 [정적 + 보관 관측]

[R10 runner:301](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r13-target-wsl/bms-balancing/reviews/r10_repros/replay_codex_r10.py:301)은 해당 shape case의 **모든 `오류`**를 전제 변경으로 바꾼다. 요청문의 “각각 fingerprint 봉인”을 이 코드가 집행하지 않는다. [R11 runner:339](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r13-target-wsl/bms-balancing/reviews/r11_repros/replay_codex_r11.py:339)은 구체적인 누락 의존성 대신 `FileNotFoundError` 접두어만 본다. 보관 결과의 설명도 문자열을 `[0]`으로 잘라 `"원"` 한 글자다.

또한 R11 `publish:*`는 원래 3개 개별 case를 1개 record로 합친다. 그러므로 **35는 JSON record 수**, 개별 명부는 **37개**다. 보관 증거의 개별 해석은 32 소멸, root 전제 변경 1개, publication 그룹 중단으로 개별 판정 미완 3개(첫 matrix 단계 중단·후속 profile 2개 미실행), 환경상 불가 1개다. 후속 두 case도 전제가 바뀌었다고 추정해서는 안 된다. 35/35라는 식의 전수 조건 인증으로 확장할 수 없다.

최소 조건: 기대하는 leaf case 명부를 고정하고 그룹 중단 시에도 각 미실행 case를 남긴다. 예외의 종류/발생 지점/의존성 원인을 구조적으로 비교하고 예상 밖 실패는 오류로 남긴다. 위 상태 분류를 실행으로 바꿔치기하는 보안 재현은 하지 않았다.

## 5. 신고된 미결에 대한 추가 확인 — 새 발견 수에 포함하지 않음

### Q6의 `ne_shape`: 단순 재생성으로는 닫히지 않는다

현재 [ne_shape.py:166](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r13-target-wsl/bms-balancing/scripts/ne_shape.py:166)의 실제 CSV writer를 모든 선언 GITT state의 유한 합성 측정값, complete pairing으로 호출했다. solver는 실행하지 않았다.

새 파일의 묶음 검사에는 문제 없음(unit=0). 그런데 schema-only는 **rc 2, schema=27, provenance_cols=3, content=1, provenance=1**이었다. [check_u14.py:110](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r13-target-wsl/bms-balancing/scripts/check_u14.py:110)이 matrix 이외 CSV를 모두 profile로 읽는다. 새 shape writer의 19개 고유 열도 모르는 열이고 profile의 γ/적합 필드를 요구한다. sidecar 계약도 현재 U14와 맞지 않는다.

따라서 과거 shape만 낡은 것이 아니다. **shape 전용 kind·schema·state key·pairing/receipt·metadata 계약을 먼저 구현한 뒤 재생성**해야 한다. profile schema에 열 19개를 무작정 허용하는 것은 답이 아니다.

degeneracy 4개의 aggregate digest 불일치는 요청문 그대로 재확인했다. 옛 산출/sidecar를 소급 고쳐 깨끗한 실행인 것처럼 만들지 말고, 이전 규칙의 해석과 현행 계산을 분리하여 새로운 위치에 실제로 재실행해야 한다.

### 신고가 정직한 항목 및 추가 경계

C25/C34와 export 공통 snapshot·dataset manifest·run receipt·partial 수명·locator 무결성은 열린 것으로 유지한다. 새 반례로 세지 않았다. 그러나 이들이 열려 있다는 사실은 별도 GO 전제를 없애지 않는다.

추가 정적 한계: 필수 xlsx 엔진 openpyxl은 requirements에 있지만 env_signature/ENV_KEYS 어느 쪽에도 없다. 실제 버전 간 수치 변화는 측정하지 않았으므로 신규 수치 반례로 세지 않고 재현성 기록의 한계로 남긴다. C28의 none 회귀는 rc 1만 보아 정상 none과 오류를 구별하지 못한다. C31은 죽은 helper를 제거했지만 일부 임시 디렉터리의 정상 종료 cleanup은 여전히 보이지 않는다. 자세한 정적 근거는 분담 보고서에 있다.

## 6. C01~C35 조건별 판정

‘닫힘’은 **명시된 좁은 수정에 대한 판정**이며 하네스 전체 GO가 아니다. ‘정적’은 해당 경계를 동적으로 검증했다는 뜻이 아니다.

| ID | 판정 | 근거 |
|---|---|---|
| C01 | 닫힘 | matrix/profile 행 재정렬 양성, 첫 행 target/ref 차이 감지 |
| C02 | 닫힘(해당 사본 축) | 대응 파일 inode/run_id 검사 및 선택 회귀 통과; 일반 독립 실행 인증은 미결 |
| C03 | 닫힘(필드 삭제 축) | 부재 sentinel로 세 필수 위험 필드 검사; 선택 회귀 통과 |
| C04 | 부분 | count/body 결속은 있으나 실제 γ 집합은 미검증: P1-1 |
| C05 | 부분 | combo count는 결속, state별 authority/구성원은 미검증: P1-1 |
| C06 | 부분 | 비유한 숫자 문자열 차단, numeric 타입/shape는 미검증: P2-1 |
| C07 | 정적 수정 확인 | 두 해시에 no-filters 적용; 우회 재생 미실행 |
| C08 | 안 닫힘(정적) | 최초 의존성 import가 격리 재실행 앞: P1-4 |
| C09 | 정적 수정 확인 | 해당 heredoc은 시작부터 격리 옵션; 모든 startup 경로 인증은 아님 |
| C10 | 정적 수정 확인 | LF 정책·보관 예외 순서 확인, 44개 보관 hash 일치; 새 Windows clone 시험은 안 함 |
| C11 | 닫힘(새 rc 분기) | baseline만 receipt 없음 rc4; schema-only 정상 rc0/비승격 직접 확인 |
| C12 | 닫힘(후보 stale 축) | stale_new blocker 및 선택 회귀 통과 |
| C13 | 부분 | receipt_map 정규화는 작동, reference schema는 문자열을 건너뜀: P1-2 |
| C14 | 부분 | 명부는 13개; shape kind/schema 미배선, 새 writer도 거부 |
| C15 | 부분 확인 | BMS_RUN_ID/묶음 검사 호출은 있음; 회귀는 호출 문자열 확인이라 경계 전체 입증은 아님 |
| C16 | 부분 | candidate-only 누락 rc2, baseline-only rc4; 양쪽 누락은 rc0: P1-2 |
| C17 | 닫힘(거부 기록 경로) | reader 거부의 pairing 기록 경로와 선택 회귀 확인; 실물 완주 미실행 |
| C18 | 닫힘(pandas 비교 축) | 변경/누락 직접 감지; schema-only 필수 env와 엔진 기록은 별도 한계 |
| C19 | 정적 수정 확인 | ineligible이면 rc3; 종결 집계 의미는 P1-3으로 미완 |
| C20 | 닫힘 | 수정된 namespace 숫자가 보관 기록과 일치 |
| C21 | 부분 | 주요 rc 계약 수정; incomparable의 rc 불변이라는 낡은 주석 잔존 |
| C22 | 닫힘 | 실측 schema59/provenance_cols27 분리, 사람용·JSON 일치 |
| C23 | 닫힘(목록 출력 축) | 실측 생략 개수 표시 및 공용 출력 helper 확인 |
| C24 | 닫힘 | 대상 보고서 5개 JSON 직접 파싱; rc 파일 분리 |
| C25 | 안 닫힘(신고) | before-evidence 둘의 full commit ID 부재 유지 |
| C26 | 닫힘(문서 숫자) | R7 5+1 기록 일치; 전체 closed 의미는 별도 P1-3 |
| C27 | 닫힘 | R11 manifest 13개 항목+manifest 자체=14개 파일 |
| C28 | 부분(정적) | none 회귀가 rc1만 보아 typed none 판정 사유를 증명 못 함 |
| C29 | 닫힘(종전 항진명제 축) | producer process run ID로 SHAPE_RESULT 구성; 전체 경계 검증은 아님 |
| C30 | 부분(정적) | 일부 child cache 분리 확인; 일반 snapshot 수명 불변식으로 확대 불가 |
| C31 | 부분(정적) | 죽은 helper 삭제; 남은 temp root 정상 cleanup 미완 |
| C32 | 부분 | helper tuple 수정, 실제 CLI BOM crash는 잔존: P2-3 |
| C33 | 부분 | 빈 문자열만 차단, `{}` 감사의 내용 소실은 여전: P2-2 |
| C34 | 안 닫힘(신고) | locator helper의 production 정보 소비자 없음 |
| C35 | 정적 수정 확인 | publication workspace가 target 밖 temp로 이동; signal 재현은 미실행 |

## 7. Q1~Q6 답변

**Q1. 반쪽 수정은 반복되는가?** 그렇다. C01의 행별화는 확인했지만 C04/C05는 count→구성원에서, C13/C16은 비교 helper→candidate 독립 schema에서, C14는 명부→kind/consumer에서, C32는 helper→CLI에서, C33는 빈 문자열→감사 내용에서 멈췄다. 특히 현재 fixture가 잘못된 full 모집단과 `{}` audit를 정상으로 인정하는 것은 공유 맹점의 직접 근거다.

**Q2. schema-only만 rc 0인 설계는 가능한가?** 가능하다. 승격을 묻지 않는 명시적 진단 모드이며, 실제 정상 대조군에서 rc0/비승격/baseline_absent=1을 확인했다. 승격 소비자는 rc만 보지 말고 비교 모드·promotion_eligible·완전 명부를 함께 확인해야 한다. 단, “schema 통과” 자체가 정직하려면 P1-2/P2-1/P2-4의 후보 독립 검사가 필요하다.

**Q3. execv 재실행과 main 가드는 충분한가?** 현재 위치/조건으로는 부족하다. 앱 의존성을 읽기 전에 필요한 격리 상태로 시작하고, helper와 executable bootstrap을 분리해야 한다. 이번 답은 정적 판단이며 보안 우회 재현으로 입증한 결과가 아니다.

**Q4. 배제목록 방향이 맞는가?** 현재 `ARTIFACT_SUFFIXES={.csv,.json}`은 여전히 확장자 허용목록이다. 새 확장자의 실제 producer는 이번에 확인하지 않았으므로 새 실행 반례로 세지 않는다. 명시적인 artifact-kind 등록부/manifest가 종류·필수 파일·스키마를 함께 정하고 미등록 산출을 조용히 생략하지 않는 방향이 낫다. sidecar 존재만으로 모집단을 정하지 않은 결정은 맞다.

**Q5. locator 정보 소비가 path-neutral identity와 충돌하는가?** 충돌하지 않는다. 동일 행 key/역할의 hash 비교와 별도로 old/new path 변화를 정보로 표시하면 된다. 같은 bytes의 위치 변화는 identity 불일치로 세지 않는다. C34를 열린 상태로 신고한 것은 맞다.

**Q6. 재생성인가, schema 확대인가?** 종류별로 다르다. shape는 **전용 schema/consumer/metadata 배선을 먼저 고치고 재생성**해야 한다. degeneracy digest 불일치는 이전 규칙/실제 소비 입력을 검토한 뒤 새 provenance를 가진 실행으로 분리해야 한다. 어느 쪽도 검사 조건을 느슨하게 하거나 과거 sidecar를 소급 보수하여 통과시키면 안 된다.

## 8. GO를 위한 최소 조건

1. 각 candidate의 γ/조합 exact membership을 producer와 공유된 state별 계약으로 검증. P1-1 세 case 거부, 정상 격자/명부 통과.
2. candidate reference receipt를 baseline과 독립적으로 정규화·검증. 양쪽 누락/불완전 문자열 거부, legacy baseline-only는 정직한 비승격.
3. 과학 JSON의 field별 타입·shape, scale audit 내용·결속, 필수 env 축을 독립 검증. bool=1과 빈 감사 자료를 같은 과학 근거로 세지 않기.
4. BOM/파싱 실패를 일관된 구조화된 CLI 결과로 반환. helper와 production CLI 모두 회귀로 고정.
5. 증거의 실행 유효성/도달/개별 결과/전체 종결을 분리. 전제 변경·미실행이 종결로 집계되지 않고 정확한 개별 명부를 보존.
6. 증거 실행의 초기화 경계를 재설계하고 별도 적절한 환경에서 검증. 이 보고서의 정적 검토를 동적 인증으로 대체하지 않기.
7. shape 전용 계약을 배선한 다음 actual producer→wrapper→U14를 완주. 기존 provenance-incomplete `out/`는 보존하고 별도 출력에 실제 재실행.
8. 신고된 공통 snapshot/dataset manifest/run receipt/partial 수명/locator 무결성 등 기존 GO 전제의 닫힘 또는 적용 범위에 대한 명시적 판단. 이번 신규 발견만 고쳤다고 전체 GO로 바꾸지 않기.

**최종: NO-GO.** 226개 회귀의 성공은 해당 시험 범위의 성공이다. 반대로 위 신규 과학 schema/CLI 관측은 회귀가 초록이어도 candidate와 증거의 의미가 충분히 보장되지 않음을 보여 준다.

## 9. 재현 자료

동봉한 `R13_REPRO_README.md`에 실행 순서와 환경을 적었다. 과학 기능 검사 스크립트 세 개, 보관 파일 읽기 전용 감사 스크립트, 합성 입력과 stdout/stderr/JSON을 포함한다. 대상 수정이나 과거 보안 공격 재생 없이 이 보고서의 실행 관측을 확인할 수 있다. `r13_cli_contract_results_v3/`가 강화된 audit 정상 대조군의 입력까지 별도 보존한 최종 CLI 결과다.
