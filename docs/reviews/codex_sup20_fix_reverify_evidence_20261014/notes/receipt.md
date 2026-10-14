# 보충 20 입력 영수증 — 독립 적대 검토

핀 `a9422d2e772f28417a6e0a5167aaab8d987bf27a`. 생산 소스 무변경, WSL/생산/수치 솔브 실행 없음.

재현: 작업 루트에서 `python -B run_checks.py receipt_extra` (run_checks가 격리 source를 cwd로 사용).

## 방법과 한정

- 제출 S7과 같은 형식으로 CPU·메모리·원자료 실재 검사 결과 등 환경 사전점검 객체만 합성했다. 실제 `preflight()`를 돌리지 않았으므로 WSL 사전점검 통과/발사 우회의 증거가 아니다.
- 실제 실행기 `build_plan`·`plan_input_digest`·`print_preflight`를 호출했다. receipt 전체 계산은 실제 반입 r3·r2 파일/설계/등록을 읽으며 대역 없음.
- 본 결과는 **출력된 로그로부터 무엇을 인증할 수 있는가**에 관한 반례다. TSV 지문이 로그에 아예 없다는 사실과 마지막 실패행이 없는 것을 성공으로 간주하는 판정은 환경 대역과 무관하다.
- 전체 상세 출력 `evidence/receipt_extra/*.json`, 생산자 로그 `*.log`, 14개 판정 사례 + 지문 비교 객체 = `summary.json`.

## 새 P2 후보 1 — dry-run 영수증에 실제 사용 TSV의 지문이 없다

위치:

- `scripts/supp20_input_receipt.py:174–180`: `_DRY_INPUT`에 case/ID/raw/missing만 존재.
- `:197–201`: E1이 그 네 개만 로컬 재계산·등록과 비교.
- `:214–217`: E6은 코호트 이름/개수만 비교하고 파일 내용 지문이나 위치를 비교하지 않음.
- `scripts/run_network_194_parallel.py:1219–1233`: 실제 `plan_input_digest`는 `cohort_tsv_sha256`를 계산함.
- `:1801–1802`: full log는 TSV 경로만 출력함.
- `:1815–1817`: 입력 지문 출력에서 **TSV 지문이 탈락**함.
- 등록 문서 §4는 grep 허용. 해당 필터는 TSV 경로가 있는 코호트 행까지 제거함.

반례:

1. 커밋된 `_cohort.tsv`의 `lhss_001` 행 `deck_sha256` 첫 자리만 바꾼 별도 TSV 생성. ID 집합·JSON raw 지문은 그대로.
2. 실제 `plan_for(cohort=별도TSV)` → `plan_input_digest` 호출.
3. 실제 `print_preflight`로 normal/wrong 로그 생성 후, 영수증 자체는 정상 반입 트리에서 `--dry-run-log`로 검사.

| 항목 | 결과 |
|---|---|
| 정상 TSV SHA | `69d3f913072288b1d6b8ca8a14e43b0bc8f80e8836a8f79a9b26b2d8ed6dcaf7` |
| 잘못된 TSV SHA | `8d5dcbd28061327f7c4f8c1a0b8915647c368236a78ced0c5ed7c3693100f1d4` |
| full log 판정 | **rc 0, 17칸 전부 PASS** |
| 등록 grep 로그 판정 | **rc 0, 16칸 전부 PASS** |
| 정상/잘못된 등록 grep 로그 | **바이트 동일** |
| 변경 TSV를 receipt의 `cohort` 인자로 직접 제공하는 양성 거부 대조 | **rc 1, B3/C2 실패** |

로그·출력: `wrong_tsv_full_log.*`, `wrong_tsv_registered_grep.*`, `wrong_tsv_local_positive_rejection.json`, `alternate_cohort.tsv`.

무너지는 결론은 **등록 TSV = 로컬 반입 TSV = dry-run이 실제 사용한 TSV**라는 세 번째 등호다. 로컬 기본 11칸 PASS나 SUP20-01/02 수정, 수치 봉인 32 동일성은 반증하지 않는다. worker의 원자료 SHA 검사/이후 배치 audit가 이 잘못된 입력을 통과시킨다는 주장도 아니다.

최소 해제:

- dry-run 증거에 실제 계획에서 계산한 `cohort_tsv_sha256` 포함 `INPUT_DIGEST_KEYS` 전부를 직렬화, receipt가 등록·로컬·실행 증거를 대조.
- 별도 파일의 TSV 내용만 변경 → 실패; 경로만 다르고 바이트 동일 → 수용(등록이 경로 동일까지 요구하지 않는 한).
- 허용된 grep 경로도 지문을 보존하거나, 불완전 텍스트 로그는 입력 일치 증서로 쓰지 않음.

## 새 P2 후보 2 — 실패 로그의 잘린 앞부분을 사전점검 성공으로 읽음

위치:

- `scripts/supp20_input_receipt.py:210–213`: STOP/✗의 **부재만** E5 PASS. 상태줄 존재, 생산자 완료 표지, 종료 코드, 관측 ON의 양성 필드 요구 없음.
- `:345–352`: 텍스트 파일을 읽고 `_dry_checks`만 호출. 완결성 검사 없음.
- `scripts/run_network_194_parallel.py:1709–1712`: 관측 OFF의 등록 생산 집합에 대한 실제 사유 생성.
- `:1816–1823`: 핵심 지문 먼저 출력, STOP는 마지막에 출력. 지문 행까지만 남아도 E1–E4는 모두 존재.

반례:

1. 실제 `production_observation_problem({plan: 실제20계획, observe_imports: False})`가 반환한 거부 사유를 pf.stop에 담음.
2. 실제 `print_preflight` 전체 출력 → receipt **rc 1, E5 실패**.
3. 동일 로그를 입력 지문 뒤/마지막 경고·STOP 앞에서 자른 prefix → receipt **rc 0, 17칸 전부 PASS**.
4. 정상 로그에서 전이 의존·지연 import·fork 세 상태줄을 모두 삭제해도 **rc 0, 17칸 전부 PASS**.

로그·출력: `observation_off_full_log.*`, `observation_off_truncated_before_stop.*`, `missing_three_prerequisite_lines.*`.

이는 체크아웃과 실행기의 관측 OFF 거부 기능이 깨졌다는 뜻이 아니다. **중단 사유가 기록 끝에서 탈락한 불완전 증거를 도구가 성공 증거로 읽는다**는 뜻이다. 실제 완전 로그에는 STOP가 있으므로 등록 grep 자체는 이를 보존하며, 완전한 grep 출력은 거부한다. 수동 fast16+real4·저자 승인까지 인증한다고 도구가 주장하지는 않는 점도 유지한다.

최소 해제:

- 동일 실행에서 생성한 구조화된 완료 영수증: 스키마·고유 실행 신원·complete·return code·stop 목록·정확한 등록 집합·`observe_imports=true`·전이/지연/fork 판정 및 전체 입력 지문 필수.
- 텍스트를 유지하면 적어도 필수 상태줄 각각 존재/유일성, 명시적 관측 ON, 마지막 완료/종료 상태를 요구하고 누락을 REFUSED로 분류. 실행 종료 자체를 확인하지 않는 마커만으로 인증 범위를 확대하지 않음.
- 정상 full/허용 필터본 통과, 끝 절단·필수 상태줄 삭제·OFF·다른 실행 로그 혼합 실패. `--dry-run-log` 없는 기본 실행은 container 범위로만 유지 가능.

## 추가 관찰 — 새 P1로 올리지 않을 신뢰 경계

실제 함수에서 다음도 재현했으나, 현재 도구의 제한된 부분증거 범위 및 후속 관문 때문에 독립 생산 결함으로 단정하지 않는다.

- E2는 dry-run git short를 파싱해 놓고 비교하지 않는다(:202–205). 다른 `b429c3c1d`를 출력해도 rc0. F5/H1은 두 manifest의 SHA가 서로 같은지만 보며 현재/승인 핀과 같음은 검사하지 않는다. **code_fp 동일 ≠ 실행기/인계기 동일**이므로 발사핀 대조를 수동으로 남기거나 위 구조화 증거에 expected fullSHA·도구 SHA를 포함할 것.
- G(194)에는 F6에 해당하는 HANDOVER 지문 대조가 없음(:247–250의 `dg is not None` 조건). 194만 인계 지문 전부0으로 바꾸면 rc0, 보충에서 같은 변조는 F6로 rc1. 현재 문서가 G6까지 보장한다고 쓰지는 않았으므로 범위 확장 권고. 194 자체 등록/관문을 면제하면 안 됨.
- manifest의 계획 TSV 경로를 별도 변경 TSV로 바꾸고 기존 input_digest를 그대로 둬도 receipt rc0. F3은 로컬 정상 digest와 manifest의 **기록값**만 비교하며 계획 경로의 현 파일을 재계산하지 않는다. 실행기 audit는 :2633–2635에서 계획의 지문을 재계산하므로 이 receipt가 audit를 대신하지 않는다는 점을 분명히 해야 함.
- H1의 다른 폴더는 '신규 빈 ROOT' 자체를 증명하지 않는다. 실행기 cmd_run이 실제 발사 시 비어 있음/기존 manifest를 검사하므로 도구 이름을 확대 해석하지 않을 것. 복사된 manifest 두 개를 읽었다고 두 신규 실행이 일어났다는 증거가 되지 않는다.
- JSON 동시 편집이나 태그 일관 위조를 독립 실행 증거로 잡아내야 한다는 보안 요구를 추가한 것이 아님. 새 P2 둘은 이미 계획한 텍스트 증거 경로에서의 비동일 입력과 불완전 로그 수용이다.

## Q3 권고

현재 container rc0는 커밋 r3 반입·설계·등록·수치 코드의 대조 증거로 충분하며, 실제 WSL 입력/원자료 존재/실행 환경 인증은 아니다. 요청된 수정 검토 닫힘과 **운영 발사 GO**를 구분해야 한다.

이번 두 증거 구멍을 닫은 다음, 승인된 최종 발사 핀의 WSL dry-run 영수증·fast16+real4·관측 ON·새 ROOT 둘 등 등록 요건을 **실제 발사 전에** 확보하고 저자 별도 발사 승인을 받는 순서가 안전하다. '조건부 기술 수용 → WSL 사전점검 → 발사 승인'은 가능하지만, '현재 container rc0 = 발사 준비 전체 GO'는 불가하다. 이 검토만으로 생산 실행을 허가하거나 요구하지 않는다.
