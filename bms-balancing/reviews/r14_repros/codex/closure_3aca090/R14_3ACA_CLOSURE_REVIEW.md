# R14 종결 확인 — 3aca090

## 판정: GO (R14 범위)

**P2-1·P2-2·P2-3을 모두 종결로 인정한다. 이번 U18b 이관과 R14 수정 처리는 수용하며, 과학 재계산은 필요 없다.**

이 GO는 원래 R14 요청 §9의 범위에 한정한다. 전체 하네스의 보안·재현성 미결, BML 별건의 과학 타당성, COMSOL, 장시간 실행을 승인하는 판정이 아니다.

| 식별 | 확인값 |
|---|---|
| 대상 HEAD | `3aca0906dcf0e8690ab534f0bef3abf6a02cdb9a` |
| 대상 tree | `84a4bac041643fb4dd9b5885ffa57f3f83eaefd8` |
| 코드 정본 | `098728cbba0525edca8d16363c484f7caef6cd6a` |
| 코드 정본 이후 변경 | `WORKING_STATE.md`·`reviews/BML_R1_RESPONSE.md` 두 문서뿐 |
| 검토 방식 | 별도 detached 작업트리. 대상 코드·원본 산출·Git 이력 수정 없음 |

## 세 조건의 종결 근거

| 조건 | 판정 | 근거 |
|---|---|---|
| P2-1 중첩 OUT | 종결 유지 | f21의 구현과 H01 회귀가 그대로다. 이번 H01 세 대조군도 통과: 중첩 OUT clean, 외부 sibling dirty 및 실제 파일명 지목 |
| P2-2 필수 env 축·비공백 | **종결** | `schema.env_axes_missing()`에 판정을 모았으며 본문과 sidecar가 실제 같은 함수를 사용한다. 이전 공백 반례가 rc2로 바뀌고 정상 대조군은 rc0 |
| P2-3 재현 문맥 | 종결 유지 | full baseline과 HEAD 자기대조를 구분한 두 정정 문서가 f21과 바이트 동일. 코드 정본 이후 문서 두 건이라는 신고도 Git으로 확인 |

P2-2의 공통 규칙: [schema.py:76](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r14-close-3aca090-wsl/bms-balancing/bms_balancing/schema.py:76).

- degeneracy 본문은 같은 파일 193행에서 호출한다.
- [check_u14.py:374](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r14-close-3aca090-wsl/bms-balancing/scripts/check_u14.py:374)의 sidecar 검사는 schema-only 반환보다 먼저 호출한다.
- [test_h02:111](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r14-close-3aca090-wsl/bms-balancing/tests/test_r14_codex.py:111)은 네 종류 × 다섯 필수 축 × 다섯 빈값(빈 문자열·공백·탭/줄바꿈·NBSP·null), **100개 조합**을 실제 CLI로 검사한다. 이는 100개 별도 pytest 항목이라는 뜻이 아니라 네 매개변수화 시험 내부의 실행 조합이다.
- 정상 env, 키별 누락, python만 남김, env 전체 부재의 기존 대조도 유지한다. 현재 네 원본이 모두 존재하므로 파일 부재 skip에 기대지 않았다.

이번 잔여는 검사 하나를 다른 자리에 추가한 것이 아니라, 달랐던 두 판정 규칙을 공유하게 해 닫혔다. 버전 문자열의 모든 의미·형식이나 전체 실행 환경 재현성까지 보증한다는 뜻은 아니다.

## 직접 실행한 결과

| 검사 | 이번 기계의 실제 결과 |
|---|---|
| `tests/test_r14_codex.py` | **7 passed in 57.57s**, rc0 |
| R13 g09(본문 env)·g29(legacy 비대칭) | **2 passed in 1.87s**, rc0 |
| 이전 matrix 공백값 재현 5대조 | 정상0, 빈 문자열2, null2, 공백2, 탭/줄바꿈2. 사본만 변경, 원본 불변 |
| 현행 `out --schema-only` | rc0, 새13개. baseline_absent1 외 blocker0 |
| legacy archive `--schema-only` | rc2, schema40 / provenance_cols25 / content6 / provenance1 |
| 현행 대 legacy archive | rc4, numbers0, inputs_uncomparable17 / env_uncomparable1. promotion_eligible=false |

**관련 회귀 9개를 집중 실행했다. 사용자가 신고한 286개 전수 통과는 이번 기계에서 다시 실행하지 않았다.** 동적 우회·변이 재생 및 Octave도 실행하지 않았다. 이전 274개 선택 회귀 결과를 새 대상의 전수 결과로 옮겨 적지 않는다.

공백값 사본 검사는 schema-only 검사이고 전부 promotion_eligible=false다. 이 결과를 실제 승격 성공 또는 전체 파이프라인 실행으로 해석하지 않는다.

## 보존·범위 확인

- 원본1bb45b3·f21·현재의 `out/` tree가 모두 `1da2e9f5600dc5f91dd0a989188ef7b0ecb19437`로 같다.
- 실제 새 payload13 + sidecar13 + legacy26 = **52개 파일**, 바이트 차이0.
- f21 후속 리뷰 ZIP: 35,050 bytes, SHA `f1d39ff1d5fe1797b2d3de0932fb6febb62acc8b7b05bef38d4e08c66df0fef7`. 원본과 동일하며 23개 payload·manifest·추출 사본·CRC 확인.
- `R14_RESPONSE.md` §7은 이전 부분 판정과 이번 공백값 수정 범위를 구분해 보존한다.
- f21 이후에는 별건 BML 외부 문헌 입력 코드도 바뀌었다. 이번 R14 GO를 그 설계 전체나 BML 과학 결론에 대한 승인으로 확대하지 않는다. 098728c→대상 구간이 문서만이라는 신고와는 모순되지 않는다.

## 다음 작업과의 경계

`legacy_transition_approved`, 기록용 CLI 인자 정책, U18-05 묶음 commit 규칙, 조건6·8, openpyxl 환경 기록, r11 대체 증거는 신고된 별도 미결이다. 이들을 이번 R14의 새 차단 조건으로 다시 세지 않는다. 다음 라운드는 이미 수용한 일회성 이관을 되풀이 계산하기보다 해당 설계 과제를 명시적으로 선택해 진행하면 된다.

**최종: R14 GO. 세 P2 종결, U18b 이관 수용, 재계산 불필요. 전체 하네스·장시간 실행 GO는 별도.**
