# R17 후속 3차 대응 — 독립 수신 재검토

2026-09-24. 고정 HEAD `a1979cdf5b9f04234b6a441150e161bd4f0a3ced`.

## 판정

**F3-01·F3-02·F3-03의 수정은 이번 재검토 범위에서 수용·종결한다.** 별도 권고였던 공통 receipt의 cycle 금지, instrument의 blob 전용, SLSQP 최종 후보의 상자 검사도 수용한다. 이번 범위에서 추가 코드 차단 결함은 발견하지 않았다.

이는 실데이터 정량 결과의 승인, package 독립 실행 인증, Windows 전체 회귀 PASS 또는 다른 GATE68의 GO가 아니다. 발송문에는 아래 동일성 문장 정정이 필요하지만, 실제 수정 코드의 동일성이 확인되므로 이 문서 정정을 이유로 세 코드 결함을 다시 열지는 않는다.

## 1. 대상과 변경 경계

- 원래 검토 대상: `e834b01e4066c5e78c06b6ed1f77878e5a27a481`.
- 대응 커밋: `fcb54da3`. 현재 고정 HEAD에서 해당 패키지와 GC/width/receipt 실행 파일의 추가 diff는 0이다.
- MSC 스크립트·시험 추가는 이번 종결 판정에 포함하지 않았다.
- 검토용 두 checkout은 같은 HEAD이며 최종 `git status --porcelain`이 모두 빈 출력이다. 제품 코드·원래 기록은 수정하지 않았다.

발송문과 대응문 머리의 다음 주장은 고정 HEAD에서는 정확하지 않다.

```text
git diff --stat fcb54da3 HEAD -- bms-balancing/bms_balancing bms-balancing/reviews
→ R17_FOLLOWUP3_RESPONSE.md 20 insertions
```

동일 경로의 `git diff --quiet`도 rc 1이다. 추가된 것은 재확인 블록 자체다. “해당 실행 코드 불변, 대응문에 발송 머리말 20줄 추가”로 좁히거나 재확인 당시의 정확한 커밋/working-tree 시점을 기록하면 된다. 이전 시점의 측정을 최종 HEAD의 rc 0으로 쓰지 않는다. 근거: `r17_response_delta.*`, `r17_unchanged_claim.json`, `r17_executable_unchanged.json`.

## 2. 지적별 재검산

| 지적 | 실제 확인 | 판정 |
|---|---|---|
| F3-01 — GC가 다른 바이트 또는 사라진 보존 대상을 무시 | 이전 재현기의 변경 바이트·보존 대상 부재 모두 rc 2, 파일과 index 전후 SHA 동일. 정상 대조군만 rc 0으로 자기 fixture의 오래된 payload 1개 삭제 | 종결 |
| F3-02 — starts/n_multistart를 독립 축으로 잘못 취급 | 동일 합성 원자료로 실제 `fit_cycles` 계산 starts 1/2를 만들고 CSV/sidecar 직렬화 후 CLI 비교. 양쪽 단독 검사와 두 별칭 축 비교 모두 rc 0 | 종결 |
| F3-03 — code=null/instrument=list를 찾아도 소비 중 crash | 두 경우 rc 3·구조화 `RUN_RECEIPT_VERIFY`·`verified=false`; 의존 검사는 null 및 `unperformed`로 남고 traceback 없음 | 종결 |

코드 근거:

- `bms-balancing/scripts/gc_partial.py:143` 이후: 삭제/보존 선택 전에 attempts 전체의 digest 형식·존재·SHA 검사.
- `bms-balancing/scripts/width_report.py:68`, `:366`: 별칭 집합을 한 의미 축으로 취급. 파일 내부 별칭·행 값 검사를 제거하지 않음.
- `bms-balancing/scripts/verify_run_receipt.py:167`, `:195`: 객체 형태를 확인한 뒤에만 의존 경로를 소비. 성공과 미수행을 구분.

추가 독립 대조:

- width 10건: 두 축 이름 각각에서 정상 비교 rc 0; 같은 축 값, 별칭 불일치, 행 `n_starts=999`, starts 외 seed까지 변경은 각각 rc 2.
- GC 4건: 보존 대상 바이트 변경, 삭제 후보 부재, malformed digest, 바이트 불일치 dry-run 모두 rc 2·전후 전체 fixture SHA 동일.
- 공통 receipt의 `cycle=999`: 정상 대조 rc 0, 반례 rc 2.
- instrument가 디렉터리 tree OID를 가리킴: rc 3. blob 전용 결정과 일치.
- 범위 밖 SLSQP 반환값을 명시적으로 주입: LAM_PE 결과 범위 약 ±16으로 유지, 이 fixture의 허용 범위 ±16.6667 안. 실제 SciPy가 범위 밖 해를 반환했다는 native 과학 반례가 아니다.

## 3. 실행 집계와 한계

| 검산 | 이번 수신 측 결과 |
|---|---|
| 이전 `repro_followup3.py --part fast` 원문 재사용 | 10 CLI 사례 + 별도 solver 반환 주입 1건, 기대와 일치 |
| 같은 재현기 `--part producer` | 합성 starts 1/2 생산·단독/비교 4 CLI 결과 일치 |
| 추가 width/GC 대조 | 10 + 4건 일치 |
| 커밋된 `test_r17_followup3.py`의 fu3_14~22 선택 | 12 passed, 14 deselected, 7.23초 |

이 수를 중복 제거한 전체 회귀 개수처럼 합산하지 않는다. `r17_repros/NEW_FAST_RESULTS.json`, `NEW_PRODUCER_RESULTS.json`, `r17_controls/RESULTS.json`, `r17_targeted.xml`에 명령·출력·식별을 남겼다.

Windows/Python 3.12.14/pytest 9.1.1에서 수행했다. 합성 producer의 실제 계산 함수·공개 직렬화·CLI consumer를 검증했으나, `fcntl`이 필요한 Linux 게시/locking 경로와 전체 suite는 재실행하지 않았다. 제출자가 보고한 Linux 523 passed/695.90초는 제출 측 기록이며 이번 수신 측 측정으로 바꾸지 않는다. 이전 47건 전체 재현기, full suite, 실데이터 A/B fitting도 이번에 다시 수행하지 않았다.

GC 정상 대조가 지운 것은 검토자가 새로 만든 fixture의 오래된 샘플 1개뿐이다. 생성 스크립트·삭제 전 SHA·삭제 후 보존 상태가 기록돼 재생성 가능하며 사용자 원자료 삭제는 없다. 나머지 GC 거부 사례는 파일과 index를 보존했다.

## 4. 회신 경계

F3-01/02/03 종결과 위 세 계약 결정을 기록하면 된다. 동시 게시/crash 중 GC 안전성, 모든 metadata schema의 완전성, 과학 결과 재승인, GATE68/COMSOL/장시간 실행으로 확대하지 않는다. 이번 리뷰는 구현 변경이나 다음 본실행 승인을 발행하지 않는다.
