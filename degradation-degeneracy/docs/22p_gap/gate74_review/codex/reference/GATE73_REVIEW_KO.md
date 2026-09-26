# Gate73 한정 재검토 — E3-R 종결 수용 / 조건부 한정 GO

2026-09-25. 이번 범위는 Gate72 잔여 P1인 원장 `evidence.out` 필수화와 멱등 반환 순서, 그 회귀 및 구조 시험의 리뷰 패키지 제외 수정이다. E1/E2/E4·E5·E6·E7·E8·E9·E10을 다시 설계하거나 과거 class 정리를 요구하지 않는다.

## 1. 요청 §3 답

| 질문 | 판정 |
| --- | --- |
| ① E3-R §4.5 ①②③ 종결 수용 | **예.** 필수 비공백 문자열·실행 자리 일치가 멱등 반환보다 앞서 확인되며, 누락/불일치 거부와 과거 기록 비재작성 조건을 충족한다. |
| ② 한정 실행 GO | **조건부 예.** 코드 `7a7945564e6a94803b4d3bc72e8202534189ccdb` / source_digest `c2ef1a811e70bb4c`를 유지하고, 사람이 실행 기계에서 생성·확인한 `grid_fit_v5` prospective 항목을 커밋한 최종 승인 HEAD 및 기존 E6/E9 조건에 한정한다. |

이번 범위에서 새 차단 P1/P2는 발견하지 않았다. 같은 보완안을 반복 제출하거나 E9를 다시 설계할 필요는 없다. **현재 prospective는 없으므로 지금 즉시 본 실행 가능 상태라는 뜻은 아니다.** 검토자가 계획 항목을 작성/커밋하거나 본 실행·복원·class 변경을 대행하지 않았다. 이 문서는 한정 리뷰 판정이지 이번 턴의 실행 승인을 확대하는 문서가 아니다.

## 2. 식별과 실제 변경

- 요청/발송 HEAD: `b0c0b9ca10743d83950c29322d30f581fecf884d`.
- 마지막 RUN_SCOPE 코드: `7a7945564e6a94803b4d3bc72e8202534189ccdb`.
- 57개 RUN_SCOPE 파일의 경로+원문 바이트를 독립 계산한 source_digest: `c2ef1a811e70bb4c`.
- 코드→요청 HEAD RUN_SCOPE diff: **0 bytes**.
- 요청 Git blob과 checkout 원문 일치: 6,735 bytes / SHA `032cb437f39dc0e8ad9c337db20ae49b92a71d0dfd2545698deda7cc01fe7a53`.
- 송신 전체 회귀 보고 HEAD `cfacfe6b44a27ee34af536cc84f29806d916f392`→요청 HEAD는 문서 3개만 변경됐다. 회귀 수치는 송신 측 실행 보고이며 수신자가 전체 suite를 재실행한 수치가 아니다.

RUN_SCOPE 수정은 `tools/preserve.py`의 `_assert_ledger_run_bound()` 추가와 attach 호출 순서 변경, 옛 선택적 분기 제거다. 원장 변경은 신고한 실물 검증 영수증 core SHA와 validator source_digest 두 값뿐이다. `paired_fixed5_v4`의 `out`은 여전히 없으며 과거 full_bundle 상태를 소급 변경하지 않았다. 상세 원문은 G72_TO_G73_SCOPE.diff와 LEDGER_AND_RECEIPT.diff에 있다.

## 3. 유한 종결 조건 대조

### ① 신규 승격에서 실행 자리 필수

`tools/preserve.py:7864`는 `ev.get("out")`을 읽고 :7865에서 비공백 문자열을 요구한다. 부재·null·빈/공백·숫자·리스트를 결속 성공으로 넘기지 않는다. :7870~7875에서 기존 posix 표현 규칙으로 정규화한 값과 영수증/묶음이 결속한 `bound_run`을 대조한다. 원장에 없는 out을 추측해 채우는 코드는 없다.

### ② 멱등 반환 전 확인 / 과거 기록 구분

attach는 원장 lock 안에서 대상 leg/evidence/status를 읽은 다음 **:7941에서 필수 결속 함수를 호출**한다. `full_bundle` 분기는 :7942, 실제 멱등 반환은 :7945 이후다. 따라서 같은 receipt path/core SHA만으로 out 결손/모순을 덮는 기존 우회가 닫혔다. 다른 영수증을 가리키는 상태에서도 out이 없으면 identity 충돌보다 미결속이 먼저 나온다.

역사적 `paired_fixed5_v4`는 readable legacy 자료이며 현재 attach 성공의 양성 대조군이 아니다. 현재 실물 receipt의 reader/묶음 결속은 통과하지만, 원장 사본의 out 누락은 attach 단계에서 미결속으로 거부된다. 기존 결과 자체가 실패했다거나 과학 결과가 틀렸다는 판정은 하지 않는다.

### ③ 양성/부정 회귀와 불변

수신자는 실제 함수의 AST 본문과 필요한 reader/helper를 추출해 아래 16건을 확인했다. 프로젝트 모듈 전체는 import하지 않았고, lock/진입점 일부 협력 함수는 inert 대체, 쓰기 sink는 예외로 차단했다. 이 검사는 Linux 전체 attach·실제 lock·동시성 시험이 아니다.

| 원장 상태 | 일치 out | 다른 out | out 누락 |
| --- | --- | --- | --- |
| pending | 승격 쓰기 지점 도달 — **실제 쓰기 차단** | 거부 | 거부 |
| full_bundle + 같은 영수증 | 멱등 성공 | 거부 | 거부 |

추가로 빈 문자열·공백·정수·리스트를 두 상태 각각에 넣은 8건, 다른 영수증+out 누락(A06), 실제 역사적 원장 바이트 사본(A07)을 검사했다. 총 16건의 fixture 전후 바이트가 동일했다. 운영 원장 쓰기·복원·class 변경은 0회다.

실물 영수증 reader와 묶음 결속을 별도 양성 확인했고, payload index의 25개 구성원과 index를 포함한 26개 파일의 집합·크기·SHA가 receipt와 맞았다. 이는 재채점/복원 실행이 아니라 저장된 자료의 독립 대조다. 정확한 대체 함수 목록·소스 SHA·결과는 RECEIVER_CHECKS.json에 있다.

제출 회귀의 7개 test 함수와 4값 parameterization은 10 node에 대응한다. A00/A01은 기존 `test_g71_e3r_00`/`07b`가 맡고, 새 A03은 승격 뒤 멱등 양성, A04/A05는 승격 뒤 변조, A06은 검사 순서, A07은 실제 원장 사본에 대한 거부를 확인한다. 부정 시험은 `PreserveError` 및 원장 바이트 불변을 검사한다. 수신자는 이 제출 pytest를 다시 실행하지 않았다.

## 4. 변이와 구조 시험 수정의 해석

두 변이의 preimage가 현재 소스에 각각 정확히 1회 존재하고 selector가 해당 반례를 겨냥함을 확인했다. 재조준된 g71 변이는 실행 자리 비교를 꺼서 pending 불일치와 full_bundle 불일치를 겨냥한다. 새 g72 변이는 필수 타입/공백 검사를 끈다.

**새 g72의 5 node 실패 증거 일부는 잘못된 원장이 성공한 것이 아니라 뒤의 Path 변환에서 발생한 TypeError다.** 이 때문에 `PreserveError`를 요구한 시험이 실패한다. 이는 의도된 오류 계약을 검증하는 증거로 수용하되, 다섯 경우 전부 승격 우회를 재현했다는 뜻으로 확대하지 않는다. 원래 Gate72 우회 종결은 위 실제 함수 제어 검사와 A02/A04/A05 회귀 근거로 별도로 확인했다. 독립 mutation replay는 하지 않았다.

구조 시험의 새 제외 조건은 `docs/22p_gap/gate…` 아래 `_review/`를 포함한 경로다. 현재 checkout에서 제외된 비-test Python 증거 사본 112개와 나머지 검사 대상 48개를 독립 AST 대조했다. 새 제외 조건과 RUN_SCOPE 운영 경로의 교집합은 없고, 검사 대상의 raw sink 호출/직접 import 위반 및 파싱 오류는 없었다. 기존 `tools/preserve.py` 자체와 test 파일에 대한 제외는 새 변경이 아니다.

따라서 이번 변경은 보관된 옛 preserve.py 사본을 운영 callsite로 세던 문제를 해소하는 범위로 수용한다. 이 경로 규칙을 OS 실행 금지나 미래 모든 동적 호출 탐지 보장으로 부르지 않는다. 첫 전체 회귀 실패와 그 뒤 재실행이라는 신고를 그대로 유지하며, 과거 패키지를 고쳐 통과시켰다는 증거는 없다.

## 5. 보존·증거 범위

- 저장소의 `f8ca8174-GATE72_REVIEW_20260925.zip`은 실제 SHA가 `9ae5356c96e26de3f2cc87ff521337e7c67b58e67951f1d8030bdc0a5df59d91`이며 수신자의 원본 ZIP과 바이트가 같다. 파일명 prefix를 SHA로 취급하지 않는다.
- Gate72 48 payload+manifest를 ZIP 및 펼친 자료와 대조했고 CRC/집합/크기/SHA가 맞았다.
- 현재 최상위 등록부 367개는 Gate72 checkout과 이름·크기·SHA가 같다. 삭제/이관하지 않았다.
- `grid_fit_v5` prospective 항목은 현재 원장에 없다.
- 1879 passed/2 xfailed·smoke·162/1·366 및 변이 실행 수치는 송신 보고다. 수신자의 16건 국소 확인과 합산하지 않는다.
- 검토 checkout의 tracked DD 2,552개는 최종 포장 전 재검사해 보존 여부를 별도로 기록한다. 원격 전체 파일/프로세스 검증으로 확대하지 않는다.

## 6. 조건부 GO의 정확한 경계

남은 것은 새 코드 결함 보완 라운드가 아니라 **기존 승인 절차의 실행 전 조건 충족**이다.

1. 사람이 실행할 기계에서 현행 코드/환경으로 계획 출력을 만들고 확인해 `grid_fit_v5` prospective 항목 및 cohort 연결을 커밋한다. `authorized_source_digest`는 **현재 `c2ef1a811e70bb4c`**여야 한다. 과거 문서의 dry 출력·구 source_digest·다른 기계 캐시 식별을 그대로 복사하지 않는다.
2. 실행 checkout은 그 계획을 담은 최종 승인 HEAD다. 코드 기준 `7a794556…`과 RUN_SCOPE diff 0, 시작 clean tree, config `configs/grid_fine.yaml`, OUT `results/grid_fit_v5`, 계획과 실제 환경/입력 식별 일치를 확인한다.
3. 기존 E6 배타 운영 창과 전후 등록부 snapshot을 유지한다. 실행 중 pytest/smoke/다른 publisher/커밋을 섞지 않는다. 367개 과거 기록 삭제·이관을 선행 조건으로 추가하지 않는다.
4. E9의 synthetic grid/fit 범위·정확 argv·`unset CANONICAL_RUN LEG`·archive→receipt→attach→사람의 역할 문구 순서를 유지한다. 실패 즉시 정지하고 동일 plan/token/source 및 재개 가능한 부분 산출을 확인한 경우에만 명시 `--resume` 최대 1회다. finalize/archive/receipt/attach 실패의 자동 재실행 승인으로 해석하지 않는다.
5. E1 producer 독립 결속 미검증, E2 디스크 source 자기 측정, E4 제한된 표본/독립 replay 한계와 E6 운영 전제를 결과에 남긴다. 새 g72 표본을 보고하더라도 전수 독립 검증으로 바꾸지 않는다. `inference_role`은 자동 승격하지 않으며 실셀 타당성·object-lock·power-loss·새 class 구현을 보증하지 않는다.

이 조건이 충족된 **합의된 synthetic grid/fit 한정 실행에 대한 리뷰 GO**다. 실행 결과 PASS를 미리 부여하지 않는다. 이번 리뷰에서는 plan_leg.py·run.sh·make_receipt.py·pytest/smoke/mutation replay·COMSOL/Java/분석 프로그램을 실행하지 않았고, prospective 작성/커밋·복원·class 변경도 하지 않았다.
