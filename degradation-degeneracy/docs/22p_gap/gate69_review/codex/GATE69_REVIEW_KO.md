# Gate 69 독립 검토 — G68-T1 및 한정 후속 대응 수용

2026-09-24 · Windows 수신 검토. **이번 후속 대응은 수용·종결 가능. 본실행 GO는 부여하지 않는다.** 검토 범위에서 새로운 차단 발견은 없다. 이는 저장소 전체의 무결함, 전체 과학 모델 정확성 또는 기존 미착수 게이트의 종결을 뜻하지 않는다.

## 1. 고정 대상과 실제 범위

| 항목 | 수신 측 확인 |
|---|---|
| 검토 HEAD | `e6ddcd1efb7df4be69849a4fd5b59c43cccff873` |
| 요청문 포함 커밋 | `afab6485e00f79ed78d43c4b4d51bca1903ae1b3` |
| 위 요청문 커밋 → 검토 HEAD의 degradation-degeneracy 차이 | 없음. 이후 커밋은 다른 프로젝트/웹 요약 변경 |
| 받은 GATE69_REQUEST.md ↔ 해당 Git blob | raw bytes 동일, SHA-256 `4b89b8f6f8595bbcab9ae4bef1dc50a9d7c1babaf3030360838b4e9d56b06ffd` |
| 직전 검토 HEAD | `a1979cdf5b9f04234b6a441150e161bd4f0a3ced` |
| RUN_SCOPE 마지막 커밋 | `743f65bead671bf353ce38027c2e8e457738ec08` |
| RUN_SCOPE diff / 후속 log | 모두 빈 출력 |
| source_digest 직접 계산 | `e9ee7475dea7de1d`, rc 0 |
| 플랫폼 | Windows, CPython 3.12.14, pytest 9.1.1 |
| 검토 시작/끝 Git status | 모두 clean |

받은 메시지에는 최종 전체 HEAD가 없었으므로 수신자가 브랜치를 fetch하고 요청문 바이트를 대조하여 위 대상으로 고정했다. 요청문 포함 SHA와 최신 SHA를 혼용하지 않았다. 근거: `IDENTITY.json`, `scope_diff.txt`, `scope_log.txt`, `source_digest.*`, `FINAL_PRESERVATION.json`.

검토 대상은 신규 phase witness, 실제 premise 실행/소비 경로, 새 13개 회귀, 등록 변이 1건, D1–D3 정정 및 리뷰 자료 재보존이다. 제품 소스는 수정하지 않았다. 변이는 별도 복사본에만 적용했다. COMSOL·실데이터·장시간 본실행·원격 쓰기/커밋/push는 하지 않았다.

## 2. 판정

| 항목 | 판정 | 직접 확인한 근거 |
|---|---|---|
| G68-T1: setup-only를 실행 완료로 읽음 | **종결 수용** | 원본 `_premise_run` → 원본 소비자에서 setup-only는 rc 0 / call 0 / AssertionError(G68-T1). 정상은 call 2 / 수용 |
| 정확 node ID·중복·오류·skip·교차 대조 | **요청 범위 수용** | 관련 41개 회귀, 수신 측 7개 기록 변형 거부, call-skipped의 미측정 반환/JUnit 불일치 회귀 |
| 새 call-phase 변이 | **수용** | baseline 5 PASS. mutant의 지정 3개만 call 단계 실패, 세 witness 모두 일치 |
| 기존 premise 변이 3개 | **회귀 유지 확인** | baseline 전부 rc 0, mutant 전부 rc 1, 정확 실패 집합·call 단계·witness 일치 |
| D1/D2/D3 정정 | **이번 종결 목적에서 수용** | 실행 코드 동일성과 문서 변경 구분, 본실행 GO 부인, 재실행≠바이트/역사 복원 명시 |
| 리뷰 자료 Git 바이트 복원 | **수용** | 66/67/68 각각 107/107·350/350·141/141. Git blob과 원본 ZIP/manifest 대조 |
| 전체 본실행 승인 | **이번 판정 대상 아님 / 승인하지 않음** | 기존 P0·등록부 격리·trusted launcher·F50b(b) 경계 유지 |

## 3. 실제 child 실행 검증

공통 진입점은 `tests/test_gate66_defensive.py:253`의 `_premise_run(python, env_extra, junit)`과 `:345`의 `assert_premise_actually_ran`이다. subprocess를 가짜로 교체하지 않았다.

| 조건 | child rc | call report 수 | 소비 결과 |
|---|---:|---:|---|
| clean | 0 | 2 | ACCEPTED, 미측정 목록 비어 있음 |
| PYTHONNOUSERSITE=1 | 0 | 2 | ACCEPTED, 미측정 목록 비어 있음 |
| 명시 PYTEST_ADDOPTS=--setup-only | 0 | 0 | REJECTED, G68-T1 call 부재 |
| 명시 --collect-only | 0 | 0 | REJECTED, G67-T1 node 집합 |
| 명시 존재하지 않는 옵션 | 4 | 0 | REJECTED, G67-T1 결과 파일 부재 |
| 부모에만 --setup-only 상속 | 0 | 2 | ACCEPTED. 자식 옵션 정리 경계 유지 |
| 외부 plugin 자동 로딩 비활성 | 0 | 2 | ACCEPTED. 저장소 내장 hook 경로로 동작 |

`tests/phase_witness.py:29`는 시작 시 대상 파일을 비우고, `:37`은 실제 `pytest_runtest_logreport`마다 nodeid/when/outcome을 append·flush·fsync한다. `--rootdir`와 예상 full node ID를 고정하고, `test_gate66_defensive.py:297` 및 `:345`에서 call 존재/단일성/결말과 JUnit을 함께 소비한다. 따라서 이전처럼 JUnit의 자식 없는 testcase를 실제 call 실행으로 대신하지 않는다.

추가 수신 데이터 검사는 정상 child가 실제로 만든 파일에 **call 제거, call 복제, setup 실패, teardown 실패, 다른 파일 node, 알 수 없는 call outcome, 빈 단계 목록**을 각각 적용했다. 같은 소비자는 7개 모두 AssertionError로 거부했다. 이는 실제로 setup/teardown 오류가 발생한 새 child를 돌렸다는 뜻이 아니라, 실제 정상 산출을 변형한 소비자 검사다. 해당 원문/수치는 `boundaries/REAL_CHILD_RESULTS.json`, `boundaries/RECIPIENT_RECORD_CASES.json` 및 곁의 XML/JSONL/stdout/stderr에 있다.

### 신뢰 경계에 대한 답

이번 수정의 주장 범위는 타당하다. **정상 pytest 자식이 옵션·환경 탓에 test body를 수행하지 않은 경우를 구분하는 실행 관측**이다. 자식이 작성하는 JSONL과 JUnit은 악의적인 자식에 맞서는 독립 보안 증명이 아니다. 임의 hook/plugin이 허위 report를 만들거나 파일을 조작하는 공격까지 닫았다고 해석하지 않는다. pytest의 call report는 call 단계의 존재/결말을 말하며, 모든 assertion·모든 branch가 실행됐다는 coverage 증명도 아니다.

이 범위를 지키는 한 새로운 권한 서명·보안 샌드박스 설계를 이번 G68-T1 종결 조건에 추가할 필요는 없다. skipped는 측정 성공이 아니며 기존 미측정 반환/보고 구분을 유지해야 한다.

## 4. 회귀와 변이 독립 대조

수신 명령은 `review_checks.py`, `remaining_premise_mutations.py`와 각 JSON argv에 보존했다. 새 소유 TEMP를 사용하고 `--noconftest`로 프로젝트의 frozen-coordinate bootstrap/등록부 정리 hook을 실행하지 않았다. 이 실행 조건을 제출자의 Linux 전체 회귀와 같다고 쓰지 않는다.

- `test_gate66_defensive.py`, `test_gate67_defensive.py`, `test_gate68_defensive.py`: **41 passed**, pytest 출력 26.78초, rc 0. 새 gate68의 13개가 포함된다. `targeted.pytest.json`/XML/원시 stdout 보존.
- 등록부의 전체 `--check-preimages`: **rc 0**, 수신 프로세스 관측 134.781초. pytest 전수 재생이 아니라 변이 위치 검사다.
- premise 등록 변이 4개를 원본과 분리한 복사본에서 실제 pytest로 대조했다.

| 등록 변이 | baseline | mutant | 정확한 실패 |
|---|---|---|---|
| the-fixture-measures-its-premise-g65 | 2 PASS | 1 FAIL·1 PASS | 활성 전제 `[True]` 1개 |
| the-premise-uses-a-controlled-env-g66 | 2 PASS | 1 FAIL·1 PASS | g66_08[nousersite] 1개 |
| the-premise-checks-the-child-actually-ran-g67 | 2 PASS | 2 FAIL | g67_11[usage_error/collect_only] 2개 |
| the-premise-checks-the-call-phase-g68 | 5 PASS | 3 FAIL·2 PASS | g68_01, g68_03[setup_only], g68_04 |

모든 mutant에서 예상 실패 집합이 정확하고 실패가 setup/collection 오류가 아닌 call 단계이며, 등록 witness가 해당 call longrepr에 있다. 새 G68-T1의 witness는 세 노드 모두 `Failed: DID NOT RAISE AssertionError`이다. 예상한 mutant rc 1을 제품 실패나 정상 회귀 실패로 합산하지 않는다.

이는 Windows에서의 **독립 국소 대조**다. 공식 `mutation_replay.py -k premise` 인증 체인이나 Linux native locking/`/proc` 경로를 실행한 것으로 대체하지 않는다. 원본 mutation 위치 바이트는 네 사례 모두 불변이다.

## 5. 문서 정정과 원자료 보존

### D1–D3

1. D1: 과거 `a31be7a9 → a1979cdf`의 dd 차이는 요청문 머리 20줄이다. 요청문 제외 diff는 비어 있다. 수정된 문장은 과거 rc 0을 취소하고 **실행 코드 불변·요청문 변경**으로 좁혔다. 이번 `afab648… → e6ddcd1…` dd diff도 별도로 측정해 비어 있음을 확인했다.
2. D2: 정본 요청문 머리/§0와 원장 §87–88에 **본실행 GO 요청이 아님**이 명시돼 있다. 저장소 밖의 과거 발송문을 수정·없앴다고 주장하지 않는다. 이번 리뷰 역시 실행 승인문이 아니다.
3. D3: GATE68_REQUEST §2-4는 재실행이 새 시각·ID·이력을 만들 뿐 삭제된 175개 바이트/역사를 복원하지 않는다고 정정했다. 과거 삭제의 정당성이나 원자료 복원까지 이번 리뷰가 인증하지 않는다.

근거: `DOCUMENT_IDENTITIES.json`, D1 diff 원문, 고정 HEAD의 `docs/GATE68_WORKING_STATE.md`, `docs/08_REVIEW_RESPONSE.md:7634`/`:7658` 및 요청문.

### Git blob ↔ 원본 ZIP

현재 작업 파일만 해시하지 않았다. 각 manifest와 payload를 **`git show <고정 HEAD>:<path>`로 직접 읽어** 비교하고, 저장된 원본 ZIP의 manifest·payload·CRC와 다시 맞췄다.

| 리뷰 묶음 | 현재 Git blob SHA 일치 | 보존 규칙 직전 커밋의 불일치 | 원본 ZIP |
|---|---:|---:|---|
| Gate 66 | 107/107 | 82/107 | 136,864 bytes · SHA `aa2cde592d28c4cfd0654e1f968dc3ad66fca452388ded5acc4cc62978c0a0ec` |
| Gate 67 | 350/350 | 174/350 | 533,373 bytes · SHA `3ab027349935843f8a2404a87b988b3e7264fa0a9d3266f2e3f20a757bd10220` |
| Gate 68 | 141/141 | 64/141 | 301,502 bytes · SHA `6679445165c2fba82b1dacf5b3dd24228d23bbce512306e6248d8e5fd7f096eb` |

ZIP별 정확 집합, 크기, SHA, CRC, 이름 중복/대소문자 충돌/경로 이탈/링크 검사를 통과했다. manifest 자체도 Git blob과 ZIP에서 raw 동일하다. `.gitattributes` 규칙 커밋 `90c766f` 뒤에 Gate 68/67/66 재추가 커밋이 순서대로 있다. 수신 측이 확인한 것은 **현재 커밋의 보존 복구와 원본 ZIP 대조**다. 과거 잘못 저장된 Git commit이 소급 변경됐다는 뜻은 아니다.

근거: `GIT_BLOB_MANIFEST_CHECKS.json`, `ARCHIVE_SET_AND_SIZE_CHECKS.json`, `attributes_before_readdition.txt`.

### 현재 등록부

고정 HEAD의 `_exec_class`는 tracked 367·디스크 JSON 367이며, 파일별 Git blob 대조 불일치 0이다. 직전 a1979cdf 대비 등록부 diff도 없다. 검토 종료 Git status는 clean이다. 원격 서버의 전체 디스크·과거 세션·모든 프로세스의 변경 부재까지 측정한 결과는 아니다.

## 6. 남겨 둔 한계와 다음 조치

- 제출자의 `1803 passed / 1 failed / 2 xfailed`, strict smoke, 41분 전체 회귀는 **이번 수신자가 재실행한 수치가 아니다**. 전체 회귀를 PASS로 바꾸지 않는다.
- 보고된 docs-lint 실패는 unchanged `test_docs_lint.py:9222`가 clone에 없는 `results/grid_fit_v4`에 의존한다는 코드 설명과 정합적이다. 이번에는 그 전체 시험/실데이터를 다시 실행하거나 근본 원인을 별도 종결하지 않았다. 정상적인 전체 실행 승인에 필요한 근거와 이번 한정 종결을 구분한다.
- G67-N1/N2/T1-b의 수용은 유지하며 새 설계를 요구하지 않는다. P0-1/P0-4, 등록부 격리/trusted launcher 및 F50b(b)는 기존 상태 그대로다.
- **다음으로 필요한 것은 이 수용을 원장에 기록하는 일이다. G68-T1을 위해 같은 수정·동일 suite를 다시 돌릴 요구는 없다.** 본실행이나 미착수 과제는 별도 범위·검증·사용자 승인으로 다룬다.

최종 판정: **G68-T1 종결 수용 / D1–D3 정정 수용 / 리뷰 원자료 보존 복구 수용. Gate 69의 이번 한정 후속 검토 종료. 본실행 GO 없음.**
