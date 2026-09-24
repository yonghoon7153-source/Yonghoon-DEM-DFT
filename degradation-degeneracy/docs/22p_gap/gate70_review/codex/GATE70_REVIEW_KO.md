# Gate70 독립 검토 — 현재 본 실행 NO-GO, 유한 종결 조건 제시

2026-09-24 · 사용자 요청 Ultra 검토 · 제품 수정/본 실행 승인 아님.

## 1. 결론

**제출된 명령·대상·보존 계약으로는 본 실행 NO-GO다. 새 실행 결함은 G70-N1 [P1] 1건이다.** 기존 E3/E5의 미완을 새 발견 수에 더하지 않는다. F50b(E7)의 변경 방향과 국소 동작은 수용한다. E8의 69차 종결을 다시 열지 않는다.

끝없는 게이트를 요구하지 않는다. 현재 목적·배포 경계에서의 종결 목록은 이 문서 §5의 E1–E10으로 고정한다. E1/E2/E4는 사용자가 더 좁은 증거 주장에 동의하면 **미완인 채 조건부 실행의 한계**로 둘 수 있다. E6는 단순 문구로 대체할 수 없는 운영 간섭 위험이 있으나, 과거 등록부 전체 이관까지 끝내야만 새 계산을 할 수 있다는 뜻은 아니다. 새 실행의 권한 기록을 격리하거나 해당 권한 영역의 배타적 사용을 보장하는 제한 경로가 있다.

다음 회신은 이 목록과 실제 변경 영향에 한정한다. 새로운 목적/진입점/배포 조건이나 구체적 반례가 없다면 임의의 추가 보안 체계를 종결 조건으로 얹지 않는다. 조건이 닫힌 **최종 코드와 실행 명세를 확인한 뒤** GO 또는 명시적 조건부 GO를 판단한다. 이 회신 자체는 계산·복원·class 변경·승격 승인이 아니다.

## 2. 판정 대상과 증거 식별

| 항목 | 수신 측 확인 |
|---|---|
| 검토 HEAD | `8568f782db3acbf00d872ce5527147258c00bec7` |
| 코드 대상 | `f0dfaff3bea1e1caedcd7a34275e908284cc2d4f` |
| 직접 계산 source_digest | `5e660a8c73d5663a`, rc 0 |
| 코드 대상→HEAD RUN_SCOPE diff | 0 bytes |
| 수신 요청문↔해당 HEAD blob | 바이트 동일, SHA `fa0e8547f8eeb4242bafd56e1fad3875a0ade3f20f765f80574d4ba330bff311` |
| 직전 기준 이후 RUN_SCOPE 변경 | `src/io.py`의 대표 start 비교 tuple에서 `git_commit` 제거 및 주석 |
| 검토 작업트리 | `C:/Users/Administrator/Documents/Codex/g70_20260924` — 별도 detached worktree |
| 전후 보존 | DD 추적 파일 2,374개 크기/SHA 동일; Git 상태 clean; 등록부 top-level JSON tracked/disk 각각 367 |

근거: `IDENTITY.json`, `RUN_SCOPE_DIFF.txt`, `CODE_TO_HEAD_SCOPE.txt`, `source_digest.*`, `PRESERVATION_REVIEW.json`. 아래 코드 좌표는 고정 HEAD의 `degradation-degeneracy/` 기준이다. `source_excerpts/`에 원문 SHA와 행 번호를 포함한 발췌를 동봉했다.

주의: clean Git은 모든 파일시스템 쓰기 0을 뜻하지 않는다. 검사 중 생긴 빈 `_claims/` 디렉터리, 작업트리/검토 fixture 생성은 §8에 별도 기록한다.

## 3. 새 실행 차단 G70-N1 [P1] — all이 만든 인자를 하위 셸이 거부한다

### 원인과 영향

- `run.sh:526`, `:541`: all이 grid/fit 하위 argv에 `--may-open`을 추가한다.
- `run.sh:558–559`: 그 argv를 Python 모듈이 아니라 같은 셸 스크립트 `"$0"`에 전달한다.
- 셸 parser `run.sh:165–211`에는 해당 옵션이 없어 `:209`에서 `알 수 없는 인자: --may-open`, rc 1로 종료한다.
- 개별 grid/fit 분기는 Python 호출 때 해당 플래그를 이미 붙인다(`:374–375`, `:413–414`). 따라서 플래그의 소비 계층이 잘못됐다.

수신 측은 원본 `run.sh`의 복사본에서 all의 dry argv를 얻고, **출력된 grid와 fit argv를 각각 실제 하위 parser에 넣었다. 둘 다 rc 1**이었다. Python grid/fit·precheck·claim·수치 계산은 호출하지 않았다. `ALL_CHILD_PARSER_RESULT.json`과 `grid_child_parser.*`/`fit_child_parser.*`에 실제 stdout/stderr/rc를 보존했다.

기존 `test_runner._dry_all`은 argv 출력 후 반환하는 경로만 검사한다(`tests/test_runner.py:61–73`, `run.sh:549–555`). strict smoke는 grid/fit 개별 모드를 사용한다. 그러므로 기존 dry/strict smoke 성공과 이 실패는 모순되지 않는다. 이 코드는 Gate57 이력부터 존재하며 **F50b가 만든 회귀로 분류하지 않는다.**

### 종결 조건

하위 셸 parser 경계까지 통과하는 RED→GREEN 회귀와 제한 수정, 또는 실제로 검토된 별도 단계 명령을 제시한다. 어느 대안을 택하든 planned leg/소유권 전달/finalize/archive 단계는 유지해야 한다. `RUN_SH_DRY`의 문자열 출력 성공만으로 닫지 않는다. 이 검토에서는 제품 수정을 하지 않았다.

## 4. 기존 항목의 실제 상태와 필요한 정정

### E3 — typed 보존 영수증 소비: 기존 미완 유지

CAS의 `execution-receipt/v1` 검사기는 이미 있다(`tools/preserve.py:2979`, `:3245`). 그러나 실제 lifecycle finalize는 다섯 bundle 선언 필드의 존재와 파일 수/바이트/index SHA를 사용한다(`:7464–7477`, `:7774–7780`, `:7955`). 기존 typed 검사기의 존재가 그 경로에 통합됐다는 증거는 아니다.

`_declared_index_members`는 잘못된 JSON/지원하지 않는 구조를 `None`으로 돌려주고, 호출부는 그때 구성원 집합 대조를 건너뛴다(`:7492–7523`). 원본 parser에 비JSON index를 넣은 소유 fixture에서 `None`을 확인했다. Linux mount 의존 전체 bundle 검증 우회를 재현했다고 주장하지 않는다.

실제 소비 경로가 versioned typed receipt를 읽어 leg/run/content 및 수행·실패·미수행 상태를 대조해야 한다. 알 수 없는 index 형식을 완전 coverage로 간주하지 말아야 한다. 현재 finalize가 `unvalidated/diagnostic`을 유지한다는 점은 옳으며, 이를 이미 검증/과학적 정본으로 자동 승격하는 결함이라고 과장하지 않는다. 실행 시 사용하지 않는 retention/restore 기능은 `unperformed`로 남겨야지 가짜 완료 증거를 요구하지 않는다.

### E5 — 내용·seal 체계는 구현됨, typed reader는 미완

요청문의 “미착수”는 부정확하다. 내용 identity·seal·capability·등록 lock·read-back·충돌 거부는 이미 존재한다. 남은 문제는 reader가 class enum과 content_id만 확인한다는 점이다(`tools/preserve.py:4950–4974`).

소유 fixture에서 다음 둘을 실제 `_read_exec_class_at`이 수용했다.

1. `content_id`와 `execution_class="canonical"` 두 키만 있는 레코드.
2. 위 키에 `sealed=[]`, `evidence=17`, `recorded_at=false`, 임의 추가 키가 있는 레코드.

`resolve_execution_class`는 `sealed`의 truthiness를 사용한다(`:5097–5111`). 따라서 modern/authorized legacy 레코드의 닫힌 typed variant와 seal 결속을 소비 지점까지 확정해야 한다. 복사/이동 후 같은 class인지 시험하는 것만으로는 충분하지 않다. 이번 probe는 reader까지며, 운영 등록부 위조나 실제 promotion 공격 성공을 주장하지 않는다. 과거 class 재분류/삭제는 별도 승인 사항이다.

### E6 — 결과 한정만으로는 부족, 과거 전체 migration은 필수 아님

약속한 `docs/22p_gap/registry_impact.md`는 검토 HEAD에 없다. 현재 테스트는 운영 등록부에 synthetic canonical을 만들 수 있다(`tests/test_compare.py:940–950`). session fixture는 시작 때 없었던 JSON 이름을 종료 시 모두 삭제한다(`tests/conftest.py:154–188`). 다른 실행이 그 사이 합법적으로 만든 기록도 소유권 구분 없이 삭제 대상이다.

원본 fixture 본문에서 decorator만 제거하고 ROOT만 소유 scratch로 바꾼 재현에서, snapshot 뒤 추가한 canonical sentinel은 teardown 후 사라졌고 기존 sentinel은 남았다. **운영 등록부 파일은 이 probe로 수정하지 않았다.** archive/report가 같은 권한 기록을 소비하므로 이는 계산 후 증거·승격 경로의 실제 간섭 위험이다. “실행 중 커밋 안 함”만으로 막히지 않는다.

새 실행의 유한 대안은 다음 중 하나다.

- 모든 관련 테스트/자식 진입점의 권한 쓰기를 분리한 전용 fixture 영역으로 격리하고 운영 영역 불변을 검증한다.
- 전용 실행 checkout/권한 영역에서 테스트·cleanup·동기화·다른 writer가 겹치지 않는 운영 창을 확정하고, 시작/종료 및 새 class delta의 소유·바이트를 보존한다. smoke/후속 검증의 권한 목적지도 명시한다.

이 조건으로 새 실행의 안전성을 확보하면 과거 등록부 전체 정리·복원·class 변경은 별도 작업으로 남길 수 있다. 현재 367개 기록의 문구를 읽는 것만으로 “실제 과학 실행의 canonical 367개”라고 확인할 수는 없다.

### E1/E2/E4 — 한정 수용 가능하지만 닫힌 것은 아님

**E1의 수정 위치부터 정정해야 한다.** 원래 Gate49 조건은 `row_projection.py`의 projection/restart 두 압축 payload와 leg/producer/manifest 결속이다. `archive_bundle.py`의 fit 보관 묶음만 수정해서는 같은 조건을 닫지 못한다. 동일 압축해제 내용의 gzip 재압축은 내용 identity와 운송 바이트 identity를 구분해야 한다. 무조건 거부 회귀로 정의하지 않는다.

E2의 현재 source_digest는 실행 코드의 디스크 자기 측정이다. 예전 decoy selector 반례 종결은 독립 launcher attestation 구현과 다르다. E4의 checker는 보고서 바이트/선언/판정을 재검산하지 변이 시나리오 자체를 독립 재생하지 않는다. 표본 재생은 선택·seed·분모·미수행 범위를 가진 **표본 주장**만 닫는다.

계약에 선언된 단일 principal/local ext4·협조적 배포 경계를 가정하면, 이 셋의 부재만으로 grid/fit 수치가 틀린다는 경로는 입증되지 않았다. 그 경계는 실제 실행 환경에서 다시 확인해야 하며 이번 수신 Windows 관측으로 입증된 것이 아니다. 더 좁은 실행 목적에서는 이 셋을 한계로 남길 수 있다. 이는 기존의 무제한 독립 GO 주장을 줄이는 사용자 결정이며, 미구현 항목을 구현 완료로 바꾸거나 기존 승격 gate를 우회하는 허가가 아니다.

## 5. 닫힌 종료 조건 표

| ID | 현재 판정/분류 | 이번 목적에서 필요한 종결 증거 |
|---|---|---|
| E1 | 미완; 한정 실행에서 결과·출처 보증 한계 허용 | 강한 producer 주장을 사용할 경우 실제 projection/restart 소비 경로의 typed manifest·압축해제 hash·producer receipt. 사용하지 않으면 미검증 범위를 명시하고 해당 주장 제외. |
| E2 | 미완; 독립 실행 코드 보증 한계 허용 | 독립 launcher 주장을 사용할 경우 실제 시작/import bytes 및 소비 receipt. 그렇지 않으면 자기 측정임을 명시. |
| E3 | 기존 실행/보존 계약 차단 유지 | 선택한 lifecycle 완료/승격 경로의 typed receipt 소비, 실제 상태·bundle 식별 결속, 지원하지 않는 index의 fail-closed, 정상/부정/부분 경로 회귀. |
| E4 | 미완; 독립 변이 replay 보증 한계 허용 | 미재생 또는 명시적 표본 범위로 한정. 전수 독립 replay 완료라 표시하지 않음. |
| E5 | 부분 구현; class 소비 계약 차단 유지 | typed modern/legacy variant, content/seal 결속, 실제 writer→reader→promotion 경로 회귀. 과거 class 임의 재작성 금지. |
| E6 | 새 실행의 운영 전제; 전체 과거 이관과 분리 | 읽기 전용 영향 지도 + 새 실행 권한 영역의 격리/배타 사용 및 전후·delta 보존. 단순 한계 라벨만으로 대체 불가. |
| E7 | F50b 제한 수용 | 현재 비교 규칙 유지; 최종 source/검증 식별에서 통합 회귀 확인. `git_dirty` 제거 불요. |
| E8 | 69차 한정 종결 유지 | 관련 코드·계약 변경이 없다면 반복 심사하지 않음. |
| E9 | 실행 명세 미완 + G70-N1 | 정확한 argv/config/입력/출력/leg/cohort/run_spec·새 prospective 승인·archive/검증 순서·실패 처리. all 결함 해결 또는 검토된 별도 명령 경로. |
| E10 | 최종 통합/환경 증거 미완 | 실제 대상 Linux/의존성/파일시스템에서 최종 식별의 전체 회귀와 작은 전 과정 smoke; 기존 positive-control 공백 해소. 본 10시간 계산 선행은 요구하지 않음. |

E9의 실행 명세에 **기존 Gate63 §0의 적용성 표**를 한 번 붙인다. 대상은 immutable publication, 필요한 class/삭제 절차, 비-grid 진입점, retention/power-loss, publisher principal, truth_provenance다. 각 항목을 `이번에 사용/완료 근거`, `범위 제외`, `명시적으로 보증하지 않음`으로 나눈다. 쓰지 않는 sweep/baseline 경로, 주장하지 않는 object-lock/전원손실 보증을 모두 구현하라는 새로운 차단 목록이 아니다. 사용하는 경로가 요구하는 조건은 한계 라벨로 우회할 수 없다.

과학 목적도 `기존 synthetic grid/fit 재실행`인지 `Stage3 primary 비교`인지 고정해야 한다. 후자면 이미 계약에 있는 paired/fixed bank/primary–secondary 조건이 적용된다. 통상 재실행에 새 셀 집단·새 C-rate 자료를 갑자기 실행 전제로 추가하지 않는다. 프로그램의 `execution_class`, 보존 상태, validator 상태, 과학적 inference_role은 서로 다른 축이다.

### E9에서 당장 빠진 구체 사항

- 문자 그대로 `./run.sh`는 `--mode 필수`, rc 1이다. 단순 축약 표기였더라도 완전한 명령이 필요하다.
- 기본 OUT은 timestamp 경로이며 요청한 `results/grid_fit_v4/`가 아니다. “정본 config”라는 말로 실제 config/protocol을 대신할 수 없다.
- 현재 planned index는 8개 과거 executed 기록이고, 새 `grid_fit_v4` prospective 항목/활성 cohort의 새 leg가 없다. 이 사실은 ledger·검사 코드의 정적 대조다. 수신 Windows에서 Linux precheck 완주를 주장하지 않는다.
- all 체인은 grid→fit→finalize→score→report이고 archive를 부르지 않는다. finalize 출력도 별도 bundle 단계 전 `preservation_pending`이라고 명시한다. 한 프로세스로 합칠 필요는 없으나 별도 명령/receipt/상태 전이를 적어야 한다.
- E3/E5/run.sh가 바뀌면 RUN_SCOPE도 바뀐다. 미래 수정 완료를 현재 `f0dfaff3`에 소급 적용하지 말고 최종 commit/source_digest와 증거를 제출한다.

### E10의 알려진 실패 한 건

제출한 `1 failed / 1804 passed / 2 xfailed`, rc 1과 strict smoke rc 0은 서로 다른 결과다. full suite를 전부 통과했다고 적을 수 없다.

`test_a_smoke_run_cannot_be_promoted_to_a_canonical_report`는 smoke 거부 뒤 ambient `results/grid_fit_v4`의 양성 경로를 확인한다(`tests/test_docs_lint.py:9192–9222`). 폴더 부재는 smoke 승격이 성공했다는 반례가 아니지만 **정상 승격 양성 근거의 공백**이다. 적법한 증거를 갖춘 격리된 정상 fixture/환경에서 양성 경로와 음성 대조를 확인해 닫는다. skip 또는 가짜 class 레코드로 녹색을 만들지 않는다.

최종 RUN_SCOPE 변경 뒤 실제 실행 환경에서 필요한 회귀를 수행한다. 문서만 변경되어 코드·테스트·의존성·계약이 동일한 경우는 바이트 동일 근거로 기존 실행 증거를 재사용할 수 있으며, 문서 commit마다 40분 시험·과거 영수증 갱신을 무조건 반복하라는 뜻이 아니다.

## 6. 여섯 질문에 대한 답

| 질문 | 답 |
|---|---|
| Q1: E1–E8 전부 닫히면 f0dfaff3에 GO인가? | **아니오.** E9/E10과 기존 §0의 적용성 처리가 빠졌다. 미래 변경의 대상은 최종 수정 commit이다. 위 유한 목록을 충족한 동일 목적의 최종본을 재검토하면 GO 판단 가능하다. |
| Q2: E3/E5/E7만 차단, E1/E2/E4/E6는 결과 한정인가? | **부분 동의.** E1/E2/E4는 주장 축소에 따라 가능. E6는 권한 기록 간섭을 막는 실행별 운영 조건이 필요하다. 과거 전면 migration까지 요구하지 않는다. |
| Q3: E3/E5/E7 종결 후 조건부 GO 가능한가? | **그 셋만으로는 아니오.** E6 운영 전제, E9 실행 경로/명세, E10 증거를 더 닫으면 E1/E2/E4를 명시한 한정 실행 GO 경로가 있다. 현재 GO는 아니다. |
| Q4: F50b를 다음 본 실행 코드에 묶는가? | **동의.** start와 실행중 코드 판정 기준을 맞추는 국소 변경이다. source_digest 변화와 과거 producer/현재 validator 구분을 유지한다. |
| Q5: “자체 검증층 통과, N/M 미닫힘”이면 충분한가? | **아니오.** 실제 통과/실패/미수행과 미닫힌 ID·영향을 적어야 한다. `N/M`은 보조 요약만 가능하다. |
| Q6: git_dirty를 빼는가? | **유지한다.** 현재 git_info는 RUN_SCOPE 기준이다. 범위 밖 문서 수정도 무조건 dirty가 된다는 요청문 전제가 틀렸다. source_digest와 tracked/untracked 상태는 서로 다른 보조 증거다. |

라벨 예시 — 완료 후 실제 관측만 채운다:

> 실행 허용 범위: [합의된 synthetic grid/fit 목적, 승인 ID]. 코드/입력/실행 식별: […]. 현지 검증: [명령·rc·실패/skip/xfail]. E1: projection producer 독립 결속 미검증. E2: 실행 source 자기 측정, 독립 launcher attestation 미구현. E4: 변이 보고서 일관성 검사와 독립 replay 범위 […]. E6: 이번 실행 권한 영역의 격리/배타 사용 근거 […], 과거 이관은 별건. execution_class/보존/validation/inference_role: 각각 실제 값 […]. archive/복원/retention: 수행·실패·미수행 […]. 이 한계는 더 강한 독립 provenance·외부 셀 타당성·미시험 내구성의 보증이 아니다.

사용자가 정한 2라운드 예산은 존중한다. 그 뒤 사용자가 검토 GO 없이 실행을 선택하면 “사용자 결정, 검토 GO 없음”을 유지한다. 기한 경과가 GO를 자동 발행하지는 않는다.

## 7. F50b·영수증 대조와 수신 검증 범위

F50b의 실제 비교 AST 두 문장을 그대로 실행했다. 같은 값과 commit만 다른 두 대조는 허용하고, source/dirty true/dirty null/env/input/recipe 변경은 거부했다. 예전 tuple로만 역변경한 대조는 commit-only를 거부했다. **전체 validate_provenance 또는 원래 F50b pytest의 통과라고 확대하지 않는다.** 원래 test_compare 모듈 수집은 matplotlib 부재로 중지됐다.

원본 dirty-scope 두 함수 본문을 소유 Git fixture에서 그대로 실행해 모두 통과했다. 별도 `test_io_bookkeeping` 5개는 `--noconftest`와 소유 temp에서 pytest **5 passed / 실제 rc 0**이다. 첫 시도는 다섯 call이 통과했지만 pytest 전역 temp 정리 PermissionError로 실제 rc 1이었다. 두 결과를 보존했고 내부 JSON의 exitcode 0으로 외부 실패를 덮지 않았다.

갱신된 `paired_fixed5_v4` 영수증의 validator는 새 digest이고, 과거 producer digest `d50295f980ccaa81` 및 `historical_validated/diagnostic`은 유지됐다. commit/dirty/time 등의 stamp 변화는 재현 core와 구분한다. 과거 bytes를 지금 검증했다는 뜻이지 새 코드로 생산했다는 뜻은 아니다. 요청자가 보고한 34/34는 이번 수신 측 직접 복원 결과가 아니다. `make_receipt.py`는 실제 복원/검증을 수반하므로 이번 리뷰에서 실행하지 않았다.

| 수신 측 직접 확인 | 결과/한계 |
|---|---|
| 요청문·commit·digest·RUN_SCOPE diff | 확인 |
| all→하위 parser | grid/fit 각각 rc 1, 미지원 옵션 재현; 계산 0 |
| F50b 비교 branch | 8사례 + 예전 tuple 역변경 대조; 전체 validator 아님 |
| 원본 dirty-scope 함수 | 2개 소유 fixture에서 통과; 원래 전체 모듈 수집 아님 |
| io bookkeeping pytest | 5 passed, 두 번째 소유 temp 시도 rc 0; 첫 정리 오류 보존 |
| E5 reader | 두 malformed record 수용 재현; promotion 미실행 |
| E3 index parser | unsupported index → None; 전체 Linux bundle verifier 미실행 |
| E6 session cleanup | 소유 fixture의 새 canonical 기록 삭제 재현 |
| 전체 pytest / strict smoke / mutation replay | 이번 수신 환경에서 미실행; 요청자 보고와 구분 |
| 본 grid/fit·COMSOL·보관 복원·class migration | 0회 |

## 8. 환경 한계·검토 부수효과·보존

수신 환경은 Windows/Python 3.12.14와 Git Bash이다. Linux mount/lock/backend/40분 전체 suite 또는 본 fit을 검증한 환경이 아니다. WSL 목록 조회는 E_ACCESSDENIED였고 우회/승격하지 않았다. 관련 수집 오류(matplotlib 부재), pytest temp 정리 오류, agent 최초 Bash PATH 오류를 제품 수치 실패로 세지 않는다.

부검토자가 읽기 전용이라고 주석된 `precheck_leg_run`을 호출했으나 `_lifecycle_root`가 mount 검사 전에 디렉터리를 만든다. 그래서 **원본 검토 worktree의 `docs/22p_gap/_claims/` 빈 폴더 하나가 생성됐다.** 이후 Windows에서 `/proc/self/mountinfo`를 확인할 수 없어 `BoundaryUnknown`으로 중지했다. claim/token/ledger/class 파일은 생성/수정하지 않았고, 폴더는 임의 삭제하지 않고 남겼다. 후속 planned-leg 호출도 의존성 문제로 완주하지 못했으므로 missing-leg 런타임 거부를 실측했다고 쓰지 않았다.

추적 파일 2,374개 전후 동일과 등록부 367개 관측은 `PRESERVATION_REVIEW.json`에 있다. 전체 OS 쓰기·모든 프로세스·원격 현지 파일을 검사했다는 뜻은 아니다. 검토용 소유 scratch의 cleanup 재현은 새 sentinel 한 개를 삭제했으며 그 입력 바이트는 fixture에 남아 복구 가능하다. 제품 코드 수정, 기존 산출물 삭제/복원, class 변경, commit/push, 외부 발송은 하지 않았다.

동봉 스크립트는 실행 지시가 아니라 검토 증거다. 특히 `agents/preservation_class/probe.py`에는 위 실패한 precheck 호출이 남아 있으므로 원래 checkout에서 무심코 재실행하지 않는다.

## 9. 다음 회신에서 받을 최소 묶음

1. G70-N1 수정 또는 대체 명령의 하위 parser/연결 회귀.
2. E3/E5 실제 소비 경로 보완과 정상·부정·부분 상태 증거.
3. E6 실행별 격리/배타 운영 및 읽기 전용 영향 지도.
4. E9 정확 명령·prospective spec·archive 순서·과학 목적/기존 조건 적용성 표.
5. 최종 식별에 결속된 E10 회귀/작은 pipeline 증거와 남은 실패의 처리.
6. E1/E2/E4를 구현할지, 구체적으로 주장 범위를 좁힐지 사용자 결정.

E8·과거 종결 항목·독립 launcher 미구현 같은 사실을 다시 “새 P0”로 세지 않는다. 새 본 계산을 먼저 돌려야 이 검토를 통과한다는 요구도 하지 않는다.
