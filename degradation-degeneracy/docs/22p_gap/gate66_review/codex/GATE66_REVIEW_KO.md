# Gate66 독립 수신 리뷰 — 부분 수용 / NO-GO

2026-09-22. 범위는 Gate65 접수 4건과 E2-R 후속의 종결 검토다. 본 실행 승인을 요청한 것으로 해석하지 않았다. 생산 코드를 수정하거나 과학 실행·등록부 정리를 하지 않았다.

## 1. 결론

**이번 보완을 전부 종결로 수용할 수 없다. 새 P1 1건, P2 2건이다.**

기존 명시 import·상대 경로·namespace 반례를 고친 것은 확인했다. 그러나 **startup 뒤에 다시 찾을 수 있는 후보를 startup 때 실제로 로드한 모듈과 동일시**하는 다음 등식이 남았다. 정상 CPython에서도 실제 진입점이 완전한 영수증을 거부한다.

추가 P2는 (1) 활성 fixture의 새 전제 시험이 외부 `PYTHONNOUSERSITE=1`에 의존하는 것, (2) 이전 리뷰 HEAD부터 이번 HEAD까지의 sealed 등록부 175건 삭제가 “기존 기록 무변경” 설명에서 빠진 것이다. 등록부 격리 미착수 자체를 새 발견으로 다시 센 것이 아니다.

| 식별 | 고정값 / 관측 |
|---|---|
| 검토 HEAD | `fa947cc9b17cdbeffbb39447c99159bc2c831e6e` |
| 직전 리뷰 HEAD | `5e4cf1038f0f26a6a624d9984386cfd046657ac3` |
| RUN_SCOPE 정본 | `743f65bead671bf353ce38027c2e8e457738ec08` |
| 직접 계산한 source_digest | `e9ee7475dea7de1d` — 일치 |
| 정본→HEAD RUN_SCOPE log | 빈 출력 |
| 환경 | Windows / CPython 3.12.14 |
| 대상 작업트리 | 분리된 detached checkout, 종료 시 clean 확인 |

이하 코드 위치는 전부 위 HEAD의 `degradation-degeneracy/` 기준이다. 재현기는 별도 리뷰 디렉터리에 있고 원본 대신 새 sandbox/출력 디렉터리만 쓴다.

## 2. G66-N1 — P1 / 정상 환경의 증거 생성 거부

**하나의 원인에 서로 다른 반례 3개다. 세 건으로 부풀려 세지 않는다.**

위치: [mutation_replay.py:5720](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/fa947cc9b17cdbeffbb39447c99159bc2c831e6e/degradation-degeneracy/docs/22p_gap/mutation_replay.py#L5720), 같은 파일 5821–5826, 5875–5900. `_replay_context()`는 `python -c` 본문에서 **초기화 완료 후** `sys.path`를 얻고, 부모는 그 목록에서 새 `PathFinder.find_spec()`를 한다. 판정은 이 후보에 대해 미로드 또는 byte 불일치를 거부한다.

### 반례 A — startup을 한 줄도 실행하지 않은 cwd 파일

만드는 상태:

1. runner의 `_make_sandbox()`로 실제 전체 subtree 복사본을 만든다.
2. 복사본 cwd에 주석만 있는 `sitecustomize.py`를 둔다.
3. `PYTHONPATH`에는 다른 빈 디렉터리만, `PYTHONNOUSERSITE=1`을 준다. 시스템 sitecustomize가 없는 이번 인터프리터를 쓴다.
4. 수정하지 않은 `_observed_receipt()` → 완전성 검사 → `_execution_receipt()`를 호출한다.

관측:

```text
native python -c: sitecustomize loaded=False, origin=None
receipt complete=True; customization.sitecustomize='<absent>'
parent candidate='4ae1adf1c1ad16cb'
_execution_receipt(): REJECTED
"startup 이 자동 import 하는 후보가 있는데 child=<absent>"
```

이 CPython에서는 `site` 초기화 시점에는 없었던 `-c`의 `sys.path[0] == ''`가 본문 실행 때 추가된다. 부모는 그 뒤 cwd에서 발견한 파일을 “startup이 읽었어야 하는 파일”로 소급한다. 같은 파일의 cwd를 **명시적으로 PYTHONPATH에 넣은 대조군**에서는 실제 startup import가 되고 ACCEPTED였다. 파일·sys.modules·digest를 위조하지 않았다.

시점 구분은 직접 측정과 CPython 3.12.14의 [초기화 코드](https://github.com/python/cpython/blob/v3.12.14/Python/pylifecycle.c#L1130), [본문 실행 전 path0 추가](https://github.com/python/cpython/blob/v3.12.14/Modules/main.c#L545)로 교차 확인했다. 최종 sys.path 설명만으로 초기 import 검색 경로를 역산하면 안 된다.

### 반례 B — 실제 로드한 startup이 자기 검색 경로만 정리

PYTHONPATH의 `startup/sitecustomize.py`:

```python
import os, sys
_here = os.path.dirname(__file__)
sys.path[:] = [p for p in sys.path if os.path.abspath(p) != _here]
```

파일은 남아 있고 읽을 수 있으며 `sys.modules`도 그대로다. 실제 전체 subtree sandbox에서도:

```text
native: loaded=True; origin=.../startup/sitecustomize.py
receipt complete=True
child='714392a77b46c917'; parent='<absent>'
_execution_receipt(): REJECTED
```

Python은 sitecustomize를 검색 경로 등을 조정하는 사용자화 지점으로 제공한다. 이 반례는 부모/자식 탐침 출력 변조가 아니라 정상 경로 정리다. [Python site 문서](https://docs.python.org/3.12/library/site.html#sitecustomize)

### 반례 C — 다른 후보를 앞으로 넣기

startup이 다른 디렉터리를 `sys.path.insert(0, ...)`로 추가하고 그곳에 별도의 sitecustomize.py가 있으면, 이미 로드한 원래 모듈과 부모가 새로 발견한 후보가 달라진다. 축소 sandbox에서 child `cc383292e18ff589` / parent `3d4c0e115a180f72`, 완전성 통과 후 실제 진입점 거부를 관측했다. C는 전체 복사 sandbox 재실행까지는 하지 않았고 A/B는 했다.

### 재현 명령과 최소 종결 조건

아래는 **리뷰 패키지의** `repro_startup.py`다. `--out`은 존재하지 않는 새 경로여야 한다. 시스템 sitecustomize가 있으면 A가 가려질 수 있으므로 native_control을 먼저 확인한다. 이 환경 제한을 숨기지 않는다.

```powershell
python repro_startup.py --repo '<HEAD checkout>/degradation-degeneracy' --out '<new output>' --full-sandbox --case plain --case cwd_only_candidate --case cwd_on_pythonpath --case remove_loaded_path
```

원자료: `startup_fullsandbox/*/observation.json`, `receipt.json`; 보조 C와 namespace/explicit 대조군은 `startup_cases/`.

기대 결과는 네 상태 모두 정상 receipt 수용이며 실제는 ACCEPTED / REJECTED / ACCEPTED / REJECTED였다.

최소 수정 방향: **로드 시점의 origin/loader·검색 문맥과, 로드 후 resolver 후보를 별도 자료로 다룬다.** 현재 신고된 보조 인터프리터 신뢰 경계 안에서도 이 구분은 필요하다. 실제 origin의 바이트는 부모가 대조하되 이름만 있는 이력과 최종 후보의 조합을 import 증명으로 쓰지 않는다. A/B/C가 수용되고 기존 changed-bytes·위조 absent·origin 없는 ModuleType 거부가 유지되는 회귀가 필요하다. `auto`를 무조건 끄거나 parent mismatch를 통째로 허용하는 수정은 아니다.

추가 정적 관측: ctx 생략 경로에서 5875의 `_parent_customization_view(None)`가 문맥을 재고, 5876이 또 `_replay_context()`를 부른다. “한 번 측정한 하나의 문맥” 구현도 아니다. 이것은 별도 finding으로 세지 않았지만 수정 시 하나의 측정 객체를 재사용하는 편이 맞다. 횟수의 런타임 계측은 하지 않았다.

## 3. G66-T1 — P2 / 시험 전제의 환경 의존 잔여

위치: [interpreter_fixture.py:24](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/fa947cc9b17cdbeffbb39447c99159bc2c831e6e/degradation-degeneracy/tests/interpreter_fixture.py#L24), 같은 파일 37–45·55–69; [test_gate65_defensive.py:95](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/fa947cc9b17cdbeffbb39447c99159bc2c831e6e/degradation-degeneracy/tests/test_gate65_defensive.py#L95).

새 `make_interpreter()`는 실제값이 다르면 skip한다. 하지만 변이를 잡기 위해 만든 `test_the_interpreter_fixture_measures_its_own_premise`는 그 함수를 우회하여 `build_interpreter()` 후 곧바로 `assert ... is True`를 한다. 생성/측정 subprocess는 외부 환경을 그대로 물려받는다. `PYTHONNOUSERSITE`를 지우는 `use_interpreter()`는 이 전제 시험에 호출되지 않는다.

재현: 같은 코드·같은 실행 파일에서 다음 테스트의 자식 환경에만 `PYTHONNOUSERSITE=1`을 둔다.

```text
PYTHONNOUSERSITE=1 python -m pytest tests/test_gate65_defensive.py
  --noconftest -q -p no:cacheprovider
  -k the_interpreter_fixture_measures_its_own_premise

1 failed, 1 passed, 15 deselected
[True]: AssertionError: assert False is True
```

위 환경 변수 표기는 POSIX식이다. Windows 실측은 리뷰 `run_checks.py premise_env_disabled`가 `subprocess.run(env=...)`로 해당 변수만 추가했다. 원자료 `premise_env_disabled.json`, `.stdout.bin`, `premise-env-disabled.xml`. 같은 변수 없는 선택 회귀에서는 해당 True/False 둘 다 통과했다.

이는 생산 승인 우회가 아니라 **환경의 비활성을 fixture 구현 실패로 오판하는 시험 결함**이다. 이번 고정 환경에서 on/off가 성공한 증거를 무효화하지는 않지만 “전제를 못 만들면 skip”이라는 전체 설명은 여전히 맞지 않는다. PYTHONNOUSERSITE가 user site를 비활성화하는 것은 명시된 동작이다. [Python site.ENABLE_USER_SITE](https://docs.python.org/3.12/library/site.html#site.ENABLE_USER_SITE)

최소 조건: fixture 생성과 측정의 환경을 명시적으로 통일하고, 외부 환경 변수에 의한 off와 fixture의 `--system-site-packages` 누락을 구별한다. `PYTHONNOUSERSITE` 유무 양쪽에서 일관된 결과를 보여야 한다. 정상 구성도 무조건 skip하거나 현재 T1 변이를 skip으로 숨기면 안 된다. 관리자 보안 정책으로 전제를 만들 수 없는 경우는 별도의 미측정 사유로 남긴다.

## 4. G66-R1 — P2 / “기존 기록 무변경” 설명의 누락

위치: [GATE66_REQUEST.md:217](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/fa947cc9b17cdbeffbb39447c99159bc2c831e6e/degradation-degeneracy/docs/22p_gap/GATE66_REQUEST.md#L217), 같은 문서 42·239–240, `docs/GATE65_WORKING_STATE.md:141`.

**git 객체를 직접 읽은 전후 대조:**

| 항목 | 관측 |
|---|---:|
| 직전 리뷰 SHA의 tracked root JSON | 541 |
| 이번 고정 HEAD | 366 |
| 기존 파일 삭제 | 175 |
| 새 파일 추가 / 살아남은 JSON 내용 변경 | 0 / 0 |
| 삭제된 레코드 | 모두 `sealed: true`, `execution_class: canonical` |
| evidence 문구별 분포 | fixture 87 / leg=L grid 88 |

삭제는 `d60f25391f9e7a08c210ef559efa0d58589171be` 한 커밋에 있다. 커밋 제목은 BMS R17 대응이며, Gate66 수정 주체가 직접 삭제했는지·의도했는지·별도 승인이 있었는지는 이 자료로 확정하지 않는다. 제목이 다른 작업이라는 사실은 대상 HEAD의 삭제를 없애지 않는다.

```text
git diff --name-status --diff-filter=D 5e4cf1038f0f26a6a624d9984386cfd046657ac3 fa947cc9b17cdbeffbb39447c99159bc2c831e6e -- degradation-degeneracy/docs/22p_gap/_exec_class
git show --format= --numstat d60f25391f9e7a08c210ef559efa0d58589171be -- degradation-degeneracy/docs/22p_gap/_exec_class
```

전체 175건의 경로·이전 바이트 SHA·JSON은 `registry-audit.json`에 저장했다. 재현기는 `audit_registry.py`다.

“이번 새 시험에서 생긴 미추적 175건이 정상 종료 때 사라졌다”는 현지 관측과, **이전 커밋에 이미 있던 tracked 175건이 사라진 것**은 별개다. 후자를 전자만으로 설명할 수 없다. 알려진 등록부 오염을 다시 finding으로 센 것이 아니라, 라운드 간 보존 범위 설명이 불완전하다는 finding이다.

최소 조건: 541→366의 기준 SHA와 삭제 커밋/파일 명부/알려진 처리 근거를 대응 원장에 추가하고 “무변경”의 시간 범위를 한정한다. 권한/소급 변경 정책은 승인된 방식으로 결정할 사항이며, 리뷰어가 삭제본을 자동 복원하거나 class를 바꾸라고 승인하지 않는다. 이미 승인된 정리였다면 그 근거를 제시하면 된다. 단순 수치 수정만으로 authority 전후 영향까지 입증한 것으로 쓰지 않는다.

## 5. 직접 실행한 증거와 미실행

| 검사 | 이 PC 관측 | 해석 |
|---|---|---|
| source_digest | 일치 | 과학 identity 재계산 |
| Gate65+64 선택 시험 | **24 passed, 2 skipped, 1 deselected**, rc0 | `--noconftest`; Linux 의존 kernel 시험은 skip/제외 |
| 기존 Gate65 실제 진입 재현기 | explicit/relative 모두 ACCEPTED | 이 실행의 base interpreter는 user-site 활성; 비활성 증거는 새 on/off 회귀에서 확인 |
| 새 startup 대조 7개 | 4 ACCEPTED / 3 REJECTED; 완전성 모두 통과 | 3개 거부가 G66-N1 |
| 실제 전체 subtree 복사 반례/대조 4개 | 2 ACCEPTED / 2 REJECTED | 축소 sandbox만의 현상이 아님 |
| `--check-preimages` | rc0 | 위치 일치 검사. 변이 실행 증명이 아님 |
| 원래 conftest를 둔 수집 | rc3 | `/proc/self/mountinfo` 부재 → frozen seal bootstrap `BoundaryUnknown` |
| 원래 `mutation_replay.py -k g65 --keep-sandbox` | rc1, **scenario5 / ran0** | 모두 collection rc3. 추가로 Windows 출력 decoding 오류 로그도 남음. 변이가 죽었다고 세지 않음 |
| 별도 `--noconftest` 보조 변이 4개 | 등록된 실패 node 집합·call 단계·witness **4/4 일치** | N1a/N1b/N2b/T1, 원래 runner coverage 인증 아님 |
| E2-R 보조 변이 | 정적 검사 2개 의도대로 실패 / native 검사 1개 skip | Linux native 종결 미확인 |
| PYTHONNOUSERSITE=1 전제 시험 | 1 failed / 1 passed | G66-T1 |
| registry git 객체 대조 | sealed 기존175 삭제 | G66-R1 |

보조 변이는 `partial_mutations.py`가 등록부의 old/new를 새 전체 복사 sandbox에 기계적으로 적용해 실행했다. 생산 파일은 바꾸지 않았다. 각 `partial_mutations/*.json`에 command, cwd, 단계, 등록 EXPECT, 실제 실패, witness 일치가 있다. E2-R의 전체 EXPECT 일치는 **false**이며 이를 숨기지 않았다.

**전체 pytest, strict smoke, 원래 Linux replay, Linux flock, 실제 planned grid→fit은 여기서 완료했다고 주장하지 않는다.** 제출자의 `1759 passed / 3 failed / 1 skipped / 2 xfailed` 및 smoke rc0는 제출자 측 주장이다. 이미 collection이 Linux 전제로 막힌 환경에서 전체 명령을 반복 실행해 같은 실패를 늘리지 않았다. WSL 접근도 E_ACCESSDENIED였다. 커널 검사를 모의 함수로 바꾸어 native 성공을 만들지 않았다.

## 6. 접수 항목별 판정

| 접수 | 이번 판정 | 근거 |
|---|---|---|
| G65-N1a 명시 import | **원 반례 닫힘 / 관련 구조는 부분** | 비활성+명시 import 정상·changed bytes 거부 회귀 통과, 등록 변이 call 실패 재현. 최종 후보=로드 origin 문제는 G66-N1로 남음 |
| G65-N1b 상대 cwd | **원 반례 닫힘 / 관련 구조는 부분** | 실제 entry의 상대 경로 수용. 같은 cwd여도 startup 시점과 최종 시점의 path가 달라 새 반례 발생 |
| G65-N2b namespace | **원 반례 닫힘** | 실제 namespace 상태 수용, 다른 위치·origin 없음·ZIP/읽기 실패 대조 및 변이 확인. 모든 loader 지원이나 전체 실행 dependency 봉인 주장이 아님 |
| G65-T1 fixture | **부분** | 이 고정 환경에서 on/off 성공. 외부 PYTHONNOUSERSITE=1에서는 새 전제 시험이 실패 |
| E2-R | **구조 수정 수용 / 독립 native 확인 보류** | 공유 predicate+같은 token 음성+상수True 회귀가 요청 방향과 일치. 이 PC에서는 kernel 호출 미실행 |

## 7. 요청문 질문에 대한 답

요청문 실제 번호는 **1·2·3·4·6·7**이다.

**Q1 조건·후보·이력:** 현재 조합은 부족하다. 이력의 이름과 최종 경로의 후보는 같은 사건의 origin이 아니다. `-X importtime -v` 대 `sys.modules` 중 하나를 고르면 해결되는 문제가 아니라, 시점·실제 origin·부모 byte 대조를 연결해야 한다. 보조 프로세스가 같은 startup 신뢰 경계라는 기존 신고를 새 발견으로 세지 않았다. A는 startup 코드 자체가 실행되지 않아도 터진다.

**Q2 built-in/frozen:** 증거를 구성할 수 없는 loader를 **명시적 미지원으로 거부**하는 정책은 수용 가능하다. 이 PC에서 표준 sitecustomize/usercustomize의 builtin/frozen 정상 사례를 만들거나 실행한 것은 아니다. 따라서 모든 배포판/embedded Python에서 그런 경우가 없다고 보증하지 않는다. 필요 시 별도의 interpreter image/code identity 계약으로 확장할 문제이지 `<absent>`로 접을 이유는 없다.

**Q3 namespace:** 코드 없는 package 객체의 **origin 종류/검색 위치 식별** 목적에는 현재 규칙이 맞고 디렉터리 전체 목록을 즉시 요구하지 않는다. 그러나 “namespace이므로 하위 파일도 실행에 영향이 없다”는 확대는 불가하다. 실제 가져온 child module의 bytes·선택된 loader/검색 순서는 별도 실행 증거의 대상이다. 빈 namespace와 다른 검색 위치의 직접 대조는 통과했다. 전체 하위 dependency 봉인을 종결 판정한 것이 아니다.

**Q4 T1 고정 환경:** 한 환경에서 native on/off 두 경우를 실제 실행하는 것은 요구한 최소 증거가 된다. 이번 Windows에서도 둘 다 확인했다. 다만 그것과 환경에 독립적인 fixture는 다른 주장이고 G66-T1이 후자를 반박한다. skip을 PASS로 세지 말고, 제어 가능한 환경 변수를 먼저 고정한 뒤 fixture 자체 변이가 실패하도록 유지해야 한다.

**Q6 F50b:** **(b) 다음 RUN_SCOPE 변경에 묶되, 그때까지 같은 commit에서 resume한다는 운영 제약을 명시**하는 쪽을 권고한다. 지금 여기서 science 산출물 재생성을 승인하지 않는다. 단순히 `git_commit` 한 항목 삭제가 정답이라고 확정하지도 않는다.

소스상 `src/fitting.py:1223–1252`는 resume마다 새 attempt provenance를 만들고 대표 start는 최초 시도로 보존한다. `src/io.py:1671–1685`는 최신 attempt 전체 문서의 일치와 최초 start의 공통 불변항 비교를 따로 한다. `실행중_코드불변`은 **한 attempt 안의 변화**, `start_파일_일치`는 **attempt 사이의 호환성**이라 의미가 같지 않다. 변경 시 doc-only 다른 commit의 정상 resume은 허용할지 계약으로 정하고, 최초/최신 commit 기록·attempt 전체 대조는 유지해야 한다. source/input/env/recipe 변경 거부와 doc-only 대조를 각각 회귀로 고정하라. 이번 검토에서는 제출자의 2회 smoke를 독립 재실행하지 않았다. 이 이미 신고된 문제를 새 finding으로 세지 않았다.

**Q7 E2-R:** lifecycle 중간의 lock을 풀어 시험을 위험하게 만들 필요는 없다. 공유 `_flock_reports_held`와 같은 live token에서 True→False→True를 확인하는 격리된 kernel 대조, 해당 wrapper 상수True 변이가 이를 깨는 회귀면 좁은 결함에 적절하다. 코드 구조는 수용한다. Linux 원래 실행 출력의 독립 확인은 여전히 필요하며 이번 정적 변이 2건 성공으로 native 미측정을 바꾸지 않는다.

## 8. 최소 재심 조건

1. **N1:** 최종 resolver 후보와 startup 로드 origin을 분리. 전체 sandbox A/B 정상 수용과 원래 위조/changed-byte 거부를 동시에 재현. C도 회귀에 포함.
2. **T1:** 외부 PYTHONNOUSERSITE 유무에서 fixture의 전제 구성/측정/skip 계약을 일치시키고, 활성 옵션 제거 변이는 여전히 call 실패여야 함.
3. **R1:** 이전 리뷰 SHA→이번 HEAD의 기존 sealed175 삭제를 원장에 명시하고 처리 근거/승인·권한 영향의 확인 범위를 구분. 삭제/복원을 자동 수행하지 않음.
4. **환경 증거:** 수정된 고정 HEAD에서 Linux native token 음성·상수True 대조 및 원래 g64/g65 replay의 명령/출력을 제공. 전체 pytest의 기존 환경 실패는 해결/미완 분류를 유지하고 성공으로 재표기하지 않음.

§0의 producer 결속·trusted launcher·보존 영수증 소비·독립 replay·immutable bundle·등록부 격리 미착수는 별도의 기존 전제다. 이번 NO-GO를 그 목록의 재확인만으로 내린 것이 아니다. **본 실행 승인 없음.**
