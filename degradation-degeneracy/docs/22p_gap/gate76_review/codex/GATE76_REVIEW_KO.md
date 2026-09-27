# Gate76 독립 검토 — 유한 목록 종결 수용

2026-09-27. **G75-N1·N2·N3 종결 수용. 74차 항목 1–6 및 75차 잔여에 대한 이번 검토를 종결한다. 새 실행 GO는 부여하지 않는다.**

이번 종결을 막는 잔여는 확인되지 않았다. 기존 Gabia 결과의 진단 전용 제한 수용을 유지한다. 추가 grid/fit 계산, 같은 전체 suite 반복, 영수증 재생성을 종결 조건으로 요구하지 않는다. 아래 기록 숫자 정정은 원문을 보존한 부가 기록으로 처리할 수 있으며 코드 보완 라운드를 다시 여는 조건이 아니다.

## 1. 고정 대상·수행 범위

| 항목 | 독립 확인 |
|---|---|
| 요청 HEAD | `b5e4eadea7794d157d961170247e49d2761bba26` |
| RUN_SCOPE 코드 | `23c361edbfc92fefcfbf0639b5ac40f61f7ebec7` |
| source digest | `1c67a748598baadb`, 58개 파일 |
| 코드→요청 HEAD | RUN_SCOPE diff 0 bytes |
| 비교 기준 | 75차 요청 HEAD `ef6689bbe296e545df57dc481e45ec98c2b9ea3b` |
| 검토 checkout | `C:/Users/Administrator/Documents/Codex/g76_20260927` |
| 보존 범위 | 위 checkout의 degradation-degeneracy tracked 2,868개 파일 전후 크기·SHA 및 clean 상태 |

고정 코드·원장·영수증·묶음·75차 패키지를 데이터로 읽었다. 독립 검사 **44개**는 검토자 코드로 허용 목록의 AST 판정 함수, 실제 index heredoc, shell의 index 호출 이후 반환 경계만 분리해 자기 fixture에서 수행했다. 제공된 모듈 전체, pytest, archive 프로그램 전체, restore, attach, receipt 생성기, 재채점/분석 프로그램, COMSOL/Java는 실행하지 않았다.

`src.io.source_digest` 호출만 독립 계산값으로 대체했다. index writer는 `names=[]`로 묶음 처리 루프를 비웠다. 실제 배포 환경의 전 과정 archive·승격을 수신자가 재현했다는 뜻은 아니다. 송신자의 전체 1,944 PASS·2 xfail/strict smoke/변이 replay는 보고된 현지 결과이며 이번 44개에 합산하지 않는다.

## 2. 세 항목 판정

| 항목 | 판정 | 이번 독립 근거 |
|---|---|---|
| N1 · index 최종화 오류 전파 | **종결 수용** | 실제 shell wrapper/footer에서 index rc17 → 부모 rc1, 성공 안내 없음, 이미 승격된 이름·미완 표시. 정상 대조군 rc0. 실제 writer의 write/replace 실패에서 기존 index 불변·tmp 제거. |
| N2 · 엄격 index 읽기 / merge 정책 | **종결 수용** | 동일 loader가 preflight·동명 비교·병합 세 reader에 연결됨. 9종 입력×3 reader=27건: 중복 키·merge·형식 오류 거부, 정상·비merge alias 대조군 수용. |
| N3 · 진단 소비자 out 결속 | **종결 수용** | 실제 소비자에 실물 typed receipt와 묶음을 연결. 다섯 다른 비공백 out·부재/빈값/공백/비문자열 거부, 정상 및 끝 `/` 수용. 12건에서 기존 생산자 out 판정과 일치. |

### N1 — 실패는 성공으로 반환되지 않는다

좌표: `scripts/archive_results.sh:302`, `:304`, `:413`, `:422`, `:431`, `:452`.

최종 index 명령의 실패가 `index_ok=0`에 도달하고 최종 nonzero 조건에 포함된다. 실패 분기에는 이미 승격된 묶음 이름과 미완이 표시되며 commit 안내를 내보내지 않는다. 자동 rollback을 추가하지 않은 것도 합의한 범위에 맞는다.

검토자 `S17`은 archive 작업을 하지 않고 **실제 if/footer/최종 predicate**에 index 명령 rc17을 넣었다. 부모 rc1과 안내 차단을 확인했다. `W_replace_failure`, `W_partial_write_failure`에서는 **실제 index heredoc**의 자기 fixture I/O만 실패시켰다. 후자는 일부 tmp 바이트를 쓴 뒤 오류를 내므로, 쓰기 전 예외만 시험한 경우보다 cleanup 경로를 직접 확인한다. 둘 다 기존 index SHA 불변·tmp 부재였다.

“즉시 nonzero”는 오류 뒤 추가 수치/승격 단계로 진행하지 않고 최종 반환을 실패로 만드는 의미로 수용한다. 코드에는 오류 안내와 요약 footer가 남아 있으므로 해당 줄에서 곧바로 `exit`하는 구현이라고 쓰지 않는다.

수용 한계: write/replace 이전·도중 실패에서 확인한 index 불변을 **모든 비정상 종료**의 불변으로 확대하지 않는다. 소스 순서상 replace 뒤 `print`/`flush`도 있으므로, 그 뒤 오류까지 가정하면 rc만으로 교체 전후를 확정할 수 없다. 그 경우 파일 식별을 별도로 확인해야 한다. 이번에는 교체 후 출력 실패를 주입하지 않았고, 성공 위장 방지의 종결을 다시 여는 조건으로 삼지 않는다.

### N2 — 세 reader가 같은 규칙으로 거부한다

좌표: `tools/index_yaml.py:31`, `:41`, `:68`; `scripts/archive_results.sh:70`, `:227`, `:325`.

`_StrictLoader`는 각 mapping을 구성하기 전에 merge tag를 거부하고, 동일 mapping의 중복 키를 검사한다. `load_index_strict`가 최상위/runs/실행 이름/entry 형식도 확인한다. 세 reader 모두 이 함수를 호출한다. 병합 단계에서 다시 읽는 파일도 느슨한 parser로 돌아가지 않는다.

독립 27건은 top-level runs 중복, run 이름 중복, identity 키 중복, 값을 덮는 merge, 겹치는 값이 없는 merge, 잘못된 shape, 빈 파일, 정상 입력, merge 없는 YAML alias를 세 소비 경로 각각에 넣었다. 거부된 입력은 index 바이트 불변이었다. 병합 양성에서는 기존 runs의 파싱된 값이 보존됐다.

정책은 **YAML merge 기능을 허용하지 않는 것**이다. alias 전체 금지나, 인용된 일반 문자열 `"<<"`까지 무조건 금지한다고 확대하지 않는다. machine-written index에서 이 제한은 명시적이고 일관된다. raw 주석/공백까지 보존한다는 종전 문구도 “파싱된 값 보존”으로 정정됐다.

### N3 — 존재 확인이 실제 결속 확인으로 바뀌었다

좌표: `tests/test_docs_lint.py:2507`, `:2544`, `:2552`, `:2554`.

typed reader가 반환한 core를 재사용하고, `_repo_relative_or_refuse → _assert_receipt_bound_to_bundle → _assert_ledger_run_bound`를 호출한다. 마지막 함수만 이름으로 갖다 놓은 것이 아니라 receipt·실물 묶음으로부터 도출한 bound run을 전달한다.

`results/OTHER_RUN`, `results/grid_fit_v4`, `artifacts/grid_fit_v5`, 접미 이름, 하위 경로는 모두 out 결속 이유로 거부됐다. 부재/빈값/공백/정수/list도 거부됐다. 정상과 끝 `/`는 생산자와 소비자가 함께 받았다. fixture 원장 바이트는 모두 그대로다. attach 본체는 이전과 바이트 동일하며 이번 검토에서 호출하지 않았다.

역사적 `paired_fixed5_v4`에 out이 없다는 사실은 그대로다. 과거 기록을 읽는 것과 지금 attach 성공으로 올리는 것은 다르며, 이번 종결로 소급 out을 채우지 않는다.

## 3. 요청 §5에 대한 답

### ① N1·N2·N3 각각 종결인가?

**세 항목 모두 예.** merge 거부 정책 포함이다. 이번 유한 수정 범위에 추가 차단 항목을 만들지 않는다.

### ② 74차 1–6과 75차 잔여를 전부 닫으면 전체 종결인가?

**이 리뷰 묶음은 종결이다.** 75차에서 수용했던 1/2/4/6을 유지하고, 3의 N3와 5의 N1/N2가 닫혔다. 기존 Gabia 결과의 진단 전용 편입·보존 정리를 끝낸다는 뜻이다.

다음까지 의미하지는 않는다.

- 지난 승인 한도 밖 resume를 소급 승인하거나 실패 이력을 지우는 것.
- `no_active_claim` 결과를 active claim/투영으로 승격하는 것.
- E1/E2/E4의 명시적 한계, 미실측 WSL 고아 상태, 과학적 수렴·물리 타당성의 미검증 범위를 해소하는 것.
- 새 본 계산, 복원, class 변경, publisher 실행, COMSOL 실행을 승인하는 것.

새 과학 작업이 필요하면 목적·고정 코드·입력/출력·계획 항목·자원·resume/보존 조건을 사용자에게 별도로 승인받는다. **이번 종결 확인을 위해 새 과학 계산이나 전체 회귀 반복을 요구하지 않는다.**

### ③ 원장은 현행 영수증 한 쌍만 가리키는 것이 맞는가?

**맞다.** 실행 다리별 현재 validator를 가리키고, 이전 영수증은 history에 원문으로 남긴다. producer 식별은 바꾸지 않는다.

실제 배치는 다음과 같다. “세 세대 전부 history”라고 쓰면 현행 위치를 혼동하므로 아래로 정정한다.

| validator digest | 현재 위치·의미 |
|---|---|
| `c2ef1a811e70bb4c` | 74차 이전 기준 history, 두 다리 각각 원문 보존 |
| `27390883eb132941` | 75차 당시 기준 history, 두 다리 각각 원문 보존 |
| `cd2408354486c148` | 이번 중간 세대 history, 두 다리 각각 원문 보존 |
| `1c67a748598baadb` | 현행 `receipts/<leg>.validate.yaml`, 원장이 가리키는 두 파일 |

즉 **다리별 과거 3개+현행 1개, 두 다리 합계 8개**다. 현재 파일을 history에 중복 복사해야 한다는 요구는 아니다. 이전 각 원문을 해당 생성 커밋과 바이트 비교했고, 현행 core SHA를 재계산하여 원장과 대조했다. 원장 변화는 두 다리 각각 receipt core SHA·validator source digest뿐이다. validation/outputs와 producer는 불변이다.

## 4. 데이터·회귀 근거 감사

- Gate75 원본 ZIP: 903,605 bytes / SHA `4a1ad8a2a7374cbc24467ca5cc24e39f9d31d9fb1845a7cc131414bbdf44cf7c`. 로컬 이전 생성본과 동일, 70 payload+manifest의 집합/크기/SHA/CRC 및 해제 사본 70개도 일치.
- `grid_fit_v5`: 29개, 27,313,017 bytes. `paired_fixed5_v4`: 26개, 23,863,555 bytes. index↔실물 집합·각 SHA·영수증 요약/restore map 대조 완료. 검토자가 복원·재채점한 것은 아니다.
- index·묶음·class 등록부·publisher·g18 projection·CLAIM_STATUS·`tools/preserve.py`·receipt 생성기 자체는 75차 HEAD 대비 불변.
- 현행 v5 core: `ae614af28efc8f9e8315198d348b935cf0f32c6f1ab83885ba58e38cc4e83a5b`. v4 현행 core의 정확 값 및 각 세대 원문 SHA는 `DATA_AUDIT.json`에 수록.
- 현행 `grid_fit_v5` stamp의 `validator_tree_dirty=true`, `paired_fixed5_v4=false`를 그대로 읽었다. 송신자가 설명한 순차 생성 맥락과 이전 stamp 동일성은 구분한다. 이를 수신자가 clean 동시 실행을 직접 관측했다고 쓰지 않는다.
- N1 wrapper가 `python -`로 stdin을 재전달하는 정정, marker에 한정된 오류 주입, 성공 대조군, 승격된 이름/tmp/index SHA assertion을 소스에서 확인했다. 첫 거짓 RED 및 최초 전체 1 failed는 §105에 남아 있다. 이를 최종 성공으로 덮지 않는다.
- 변이 4개의 preimage/변이/선택 시험/EXPECT를 정적으로 읽었다. merge 변이는 거부 자체가 없어지는 것이 아니라 **명시적 merge 오류 사유**가 없어지는 것을 검출한다는 기록이 맞다. 4개 모두 과학 의미의 독립 강건성 증명이라는 뜻은 아니다. 변이 replay는 재실행하지 않았다.
- `5b10a79f`의 리뷰 사본 claim 관할 제외 변경은 RUN_SCOPE 밖이다. 고정 HEAD에서 새 소문자 gate 접두사로 제외되는 현재 md는 모두 `gateNN_review/` 아래 증거 사본이다. 다만 구현은 정확한 디렉터리 정규식이 아니라 접두사이므로, 미래의 임의 `gate…` 운영 문서를 같은 경로에 두고 검사된 것으로 간주하면 안 된다. 현행 운영 문서 누락을 관측했다는 뜻은 아니다.

## 5. 비차단 기록 정정

1. 발송문 등록부 `367=367`은 고정 HEAD 실물 **369=369**로 정정한다. 요청문 §2는 이미 369다. 367은 과거 기준 수이며 현행 검토 실패가 아니다.
2. 영수증 세대 위치는 위 표대로 **history 3세대+현행**으로 구분한다. 요청문 §3의 “전부 history” 표현을 그대로 재사용하지 않는다.
3. 첫 RED “19 node · 11 failed/7 passed”는 산술상 18개다. 이번 제출 소스로 최종 22개 구성은 확인되지만, 그 첫 실행의 누락 상태를 추정해 채우지 않는다. 당시 원본 요약이 있으면 분모/빠진 상태만 부가 정정하고, 없으면 미확인으로 남긴다. 이를 맞추기 위한 재시험은 요구하지 않는다.

이 세 기록 사항은 **N1/N2/N3 코드 종결의 선행 조건이 아니다.** 원래 문서/영수증/실패를 보존한 회신 기록으로 충분하다.

## 6. 제출물과 한계

`DECISION.json`은 유한 범위 종결과 새 실행 승인 없음의 기계 판독 기록이다. `DECISION_PROBES.json`은 44개 사례·추출 함수 좌표/식별·adapter·결과, `DATA_AUDIT.json`은 실물 식별/세대 대조, `PRESERVATION_AFTER.json`은 검토 checkout 보존을 기록한다.

검토자 자신의 읽기 도구 실행 과정에서 기본 Git Schannel의 lazy fetch가 한 번 실패해 동일 read-only diff를 OpenSSL 설정으로 다시 읽었다. 대상 프로그램 실패나 회귀 재실행이 아니며 자료는 `REVIEWER_CHECK_HISTORY.md`에 구분했다. 제공된 원격 전체 회귀 로그나 실행 환경을 독립 재현한 검토가 아니다.

**결론: 수용·종결. 현재 결과와 한계는 보존하고 이번 리뷰를 끝낸다. 새로운 실행 권한은 발생하지 않는다.**
