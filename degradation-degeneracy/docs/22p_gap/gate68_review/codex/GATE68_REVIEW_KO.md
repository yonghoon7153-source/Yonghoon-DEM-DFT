# GATE68 — 독립 수신 검토

2026-09-24. 고정 HEAD `a1979cdf5b9f04234b6a441150e161bd4f0a3ced`.

## 판정

**부분 수용 / 종결 NO-GO. P2 잔여 1건: G68-T1.**

- G67-N1 및 G67-N2: 이번 경계 안에서 종결 수용.
- G67-T1-b: 수정된 고정 witness를 이번 실제 변이 대조에서 확인, 수용.
- G67-T1: 사용법 오류·수집 전용·상속 옵션 경계는 고쳐졌다. 그러나 call 단계를 실제로 수행했다는 증거 검사는 아직 불충분하다.

본실행은 승인하지 않는다. 상세 요청문 §0/§5도 본실행 GO를 요청하지 않으며, 별도 발송문의 “약 10시간 본실행 GO 요청”과 모순된다. 더 좁은 요청문 범위로 검토했다. P0-1/P0-4·등록부 격리 등 기존 미착수를 이번 새 결함으로 다시 세지는 않는다.

## 1. G68-T1 — JUnit 성공 testcase를 call 실행 증거로 오인 (P2)

위치: `degradation-degeneracy/tests/test_gate66_defensive.py:266`~`:318`, 특히 `:284`의 기본 passed 분기. 호출자 `:322`와 커밋된 G67-T1 회귀도 같은 소비자를 사용한다.

`_premise_outcomes()`는 JUnit testcase에 error/failure/skipped가 없으면 passed로 처리한다. `assert_premise_actually_ran()`는 rc 0·정확한 두 testcase 이름·이 상태만 보므로, **setup/teardown만 실행된 결과를 call PASS와 구분하지 못한다.**

### 실제 child 재현

| 실제 child 조건 | child rc | 실제 call | JUnit 소비 결과 |
|---|---:|---:|---|
| 정상 대조 | 0 | 2개 passed | ACCEPTED, 미측정 목록 [] |
| `--collect-only` | 0 | 0 | AssertionError로 REJECTED |
| **`--setup-only`** | **0** | **0** | **ACCEPTED, 미측정 목록 []** |

`--setup-only` 결과의 두 항목에는 setup/teardown만 있고 call 필드가 없다. JUnit에는 두 testcase가 실패/skip 자식 없이 기록됐다. 제품 코드를 수정하거나 subprocess 결과를 위조하지 않았다. 원본 `_premise_run()`의 명시 `env_extra`에 옵션을 전달했다. 이는 커밋된 `test_g67_11`이 사용법 오류/collect-only를 주입하는 것과 같은 검토 통로다. **상속 옵션 제거가 다시 뚫렸다는 주장이 아니다.**

추가로 JSON-report plugin 없이도 실제 커밋된 `test_g66_08_the_premise_test_does_not_fail_on_an_inherited_env({'PYTEST_ADDOPTS':'--setup-only'})`를 직접 호출했으며 정상 반환했다. 깨끗한 대조는 정상 반환, collect-only는 AssertionError였다. 따라서 별도 관측 plugin 때문에 생긴 수용이라고 볼 수 없다.

근거:

- `t1_setup_only/RESULTS.json`: 실제 argv/rc·JUnit 해석·독립 phase 관측.
- `t1_setup_only/setup_only.xml`, `setup_only.pytest.json`, stdout/stderr 원문.
- `final_checks/COMMITTED_ENTRY_RESULTS.json`: plugin 없는 커밋된 진입점의 직접 호출.
- `repro_gate68_t1.py`, `final_checks.py`: 재현 소스. 재실행은 새 출력/임시 경로를 준비한 독립 승인 범위에서만 수행할 것.

공식 pytest도 `--setup-only`는 fixture만 준비하고 테스트를 실행하지 않는다고 설명한다. runtest protocol은 이 옵션이 켜지면 call 단계를 생략하며 setup/call/teardown의 보고서를 구분한다. 이번 실제 관측과 일치한다. [pytest API Reference](https://docs.pytest.org/en/stable/reference/reference.html#pytest.hookspec.pytest_runtest_protocol).

### 영향과 최소 종결 조건

이 반례는 제출자가 실제로 실행한 깨끗한 회귀를 실패로 소급 분류하지 않는다. 실패는 **“시험 본문을 수행하지 않은 child를 실행 증거 소비자가 거부한다”는 계약과 종결 주장**에 있다.

최소 보완은 exact full node ID별 실제 call-phase report/marker를 검증하는 것이다. 정상 측정은 `when=call, outcome=passed`를 요구하고, setup/teardown 오류·skip/미측정·중복/누락을 별도로 구분해야 한다. `rc=0`, JUnit testcase 수, 요약의 passed 수 또는 특정 옵션 문자열 차단만으로 대체하지 않는다. 특정 외부 plugin을 필수화하라는 뜻은 아니며 내장 hook 기반의 작은 증거 기록도 가능하다.

회귀는 정상/명시 usage error/collect-only/setup-only 및 상속 옵션 제거 대조를 유지하고 실제 child와 같은 소비 경로를 사용해야 한다. 임의 예외나 서명 TypeError를 기대 거부로 세지 않는다.

## 2. 수용한 변경

### G67-N1

`mutation_replay.py:6112`의 `g != cand` 비교가 auto 여부보다 먼저 작동한다. 원래 `repro_boundaries.py`를 바이트 그대로 사용해 OFF/ON 명시 namespace의 정직한 영수증은 실제 entry까지 수용, absent 위조는 parent/entry에서 거부됨을 확인했다. completeness 단독은 여전히 구조 검사여서 이를 semantic 거부로 잘못 쓰지 않는다.

### G67-N2

`mutation_replay.py:6019`의 archive/member 직접 읽기는 사후 sys.path를 다시 찾지 않는다. ZIP package가 자기 경로를 제거한 경우와 경로 유지 package·단일 module 대조 모두 실제 entry까지 수용했다. 변경 바이트·member 소멸·지원하지 않는 origin 거부 회귀도 선택 suite에 포함됐다. startup 후 관측된 origin을 쓰는 경계이며 로드 순간 불변 바이트 증명으로 승격하지 않는다.

### T1-b 및 변이 대조

등록된 변이의 원래 old/new/selector/EXPECT를 가져와 독립 복사본에서 적용했다. 네 변이 모두 baseline rc 0, mutant rc 1이며 **정확한 예상 실패 집합·call 단계·고정 witness 일치**를 확인했다.

| 축 | 예상 실패 수 | 수신 결과 |
|---|---:|---|
| usercustomize-follows-the-startup-activation-g64 | 3 | 정확 집합/call/witness 일치 |
| the-premise-uses-a-controlled-env-g66 | 1 | 정확 집합/call/witness 일치 |
| zip-bytes-come-from-the-archive-member-g67 | 1 | 정확 집합/call/witness 일치 |
| the-premise-checks-the-child-actually-ran-g67 | 2 | 정확 집합/call/witness 일치 |

`gate_mutations/RESULTS.json`과 단계별 raw JSON/출력 참조. 이는 Windows에서 수행한 네 축의 독립 국소 대조다. 전체 공식 mutation replay의 증거 영수증/격리/native 커널 경로를 전수 통과했다고 쓰지 않는다. 기존 usage/collect 두 변이가 잡히는 사실과 setup-only 잔여는 양립한다.

## 3. 실행 범위와 환경 실패

- RUN_SCOPE 마지막 커밋 직접 확인: `743f65bead671bf353ce38027c2e8e457738ec08`.
- `source_digest()` 직접 재계산: `e9ee7475dea7de1d`.
- gate64~67 portable 선택 suite: **52 passed, 2 skipped, 1 deselected / 31.32초**, `--noconftest` 사용. skip 2개는 fcntl.flock 필요, deselected 1개는 kernel lock probe다. gate63/Linux native coverage를 포함하지 않는다.
- `--check-preimages`: rc 0. 지점 매칭 검사이지 mutant kill 결과가 아니다.
- 이전 경계 재현기의 원문을 사용한 namespace/ZIP 양성 5조건, absent 위조 2조건, 실제 usage/collect 거부를 확인했다.

실패 이력도 보존했다. 첫 portable suite는 6 failed/46 passed/2 skipped였고 자식 pytest의 기존 TEMP 디렉터리 접근권한 오류가 드러났다. 제품 코드를 바꾸지 않고 새 소유 TEMP로 격리해 위 52 passed 결과를 얻었다. 첫 경계 재현기는 깊은 checkout의 역사적 긴 파일명 복사 중 WinError 3로 중단됐다. 짧은 경로에 동일 HEAD의 별도 checkout을 두고 관련 소스 SHA 동일을 확인해 재현했다. 첫 source_digest 시도는 다른 venv의 yaml 부재로 실패했고, yaml이 이미 있는 gate venv에서 계산했다. 각각의 원출력과 명령/rc는 별도 파일로 남겼다.

제출 측 Linux 77 passed/1 xfailed, 전체 1789 passed/1 failed 등의 수치를 여기의 수신 검증 수로 바꾸지 않는다. 전체 41분 회귀, strict smoke, Linux fcntl·/proc/native locking, 약 10시간 본실행은 수행하지 않았다. COMSOL/JVM/Java·실데이터 fitting도 실행하지 않았다.

## 4. 문서 정정 — 새 코드 결함과 구분

1. `git diff --quiet a31be7a9 HEAD -- degradation-degeneracy`는 **rc 1**이다. 변경은 `GATE68_REQUEST.md` 머리의 20줄 추가이며, 그 파일을 제외하면 diff rc 0이다. “dd 한 바이트도 불변/rc 0”을 최종 HEAD에 적용하지 말고 “실행 코드 불변·요청문 머리 추가”로 정정한다.
2. 발송문은 본실행 GO 요청이라고 하지만 정본 요청은 두 번 명시적으로 부인한다. 이번 결과를 본실행 승인으로 해석하지 않도록 발송문도 정정한다.
3. “지운 고아 175건은 같은 회귀를 다시 돌리면 되돌릴 수 있다”는 표현은 바이트/역사 복원과 다르다. 재실행은 새 시각·ID·실행 이력의 기록을 만든다. 삭제 원자료나 당시 inventory 없이는 옛 175건을 독립 재구성했다고 할 수 없다. 이번 검토는 삭제/복원/class 변경을 하지 않았고 해당 과거 삭제의 종류·정당성을 추가 인증하지 않는다.

## 5. 요청문의 다섯 질문에 대한 답

1. 표준 ZIP 외 loader로 넓힐 필요는 이번 범위에서 없다. 명시된 지원 집합 밖은 사유와 함께 거부하면 된다. archive/member identity를 읽는 것과 원자적 로드 시점 결속은 별개다.
2. 관측된 loaded/kind/locations와 동일성을 비교하는 현재 namespace 수정으로 N1은 닫을 수 있다. 이름별 이력을 새로 만들지 않고 로드 시점 불변성까지 얻었다고 주장할 수는 없다.
3. 정책 skip을 제품 FAIL로 위조할 필요는 없다. 다만 전부 skip이면 해당 전제는 NOT_MEASURED라서 그 전제가 필요한 GO를 발행할 수 없다. 외부 회귀가 “skip 분류가 맞음”을 시험한 PASS와 child 전제의 실제 측정 PASS를 분리해야 한다.
4. 따옴표 heuristic은 현재 잘린 꼬리 재발을 잡는 국소 lint로 유지 가능하다. 모든 witness 안정성의 증명은 아니다. 실제 mutant의 정확 실패 집합/call/결정적 이유 대조를 우선한다. 결정적 repr 19건 때문에 범위를 무작정 넓힐 필요는 없다.
5. 먼저 읽기 전용 영향·의존성 지도와 판정 계약을 정리하고, 그 결과로 trusted launcher/P0-1/등록부 격리의 구현 범위를 함께 설계하는 편이 낫다. 관측 단계에서 삭제·복원·class 변경을 섞거나 기존 승인을 재사용하지 않는다.

## 다음 최소 범위

G68-T1의 call-phase 증거 소비와 그 회귀만 보완하고 문서 세 문장을 정정하는 후속안을 받으면 된다. N1/N2/T1-b를 새 설계로 다시 열 필요는 없다. 기존 P0·격리 미완과 본실행 보류를 유지한다. 이 검토문 자체는 수정/본실행 승인이 아니다.
