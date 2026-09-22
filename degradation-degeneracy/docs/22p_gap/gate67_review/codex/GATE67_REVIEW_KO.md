# Gate67 적대적 재검토 — 부분 수용 / 종결 NO-GO

검토일: 2026-09-22. 사용자 승인 범위: XHigh 재검토. 과학 실행·COMSOL 실행·production 수정·등록부 복원/삭제/class 변경 없음.

## 1. 판정

**66차의 원래 파일 경로 반례와 PYTHONNOUSERSITE 반례는 닫혔다. 그러나 Gate67 수정 묶음 전체의 종결은 NO-GO다. 새 P1 2건, P2 1건을 실행으로 확인했다.**

1. **G67-N1 / P1 / 환경 영수증 결속:** user-site OFF에서 명시적으로 로드된 namespace를 영수증에서만 `<absent>`로 지워도 실제 검증 진입점이 받아들인다.
2. **G67-N2 / P1 / 정상 재생 가용성:** 표준 ZIP package가 자기 archive를 `sys.path`에서 제거하면 정상 영수증을 거부한다. ZIP 분기에는 여전히 사후 검색 경로 재탐색이 남아 있다.
3. **G67-T1 / P2 / 회귀 증거:** 새 전제 시험은 내부 pytest의 사용법 오류(rc 4) 또는 collection-only(실행 0건)를 통과시킨다. 관련 등록 변이의 witness에는 가변 traceback 꼬리도 섞여 있어 이 기계에서 EXPECT 문자열이 일치하지 않았다.

요청문 §6은 전체 GO를 요청하지 않았다. 따라서 위 판정은 **이번 수정·증거의 전부 종결 주장**에 대한 판정이다. 기존 P0-1·trusted launcher·typed receipt 소비·독립 replay·immutable bundle·등록부 격리 등 신고된 미착수를 새 발견으로 세지 않는다. 본 실행 승인도 아니다.

## 2. 고정 대상과 검토 방식

| 항목 | 관측 |
|---|---|
| 원격 | `https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT.git` |
| branch | `claude/14-gate-code-review-9qkx05` |
| fetch 후 고정한 HEAD | `cdc49e91af15b2ef968753110cfae3bbe7ab5c2f` |
| 직전 검토 SHA | `fa947cc9b17cdbeffbb39447c99159bc2c831e6e` |
| 요청문상 RUN_SCOPE 기준 | `743f65bead671bf353ce38027c2e8e457738ec08` |
| 직접 실행한 source_digest | `e9ee7475dea7de1d` |
| 위 RUN_SCOPE 기준 이후 src/tools/configs/scripts/run.sh/requirements 변경 이력 | 빈 출력 |
| 검토 플랫폼 | Windows / Python 3.12.14 |
| 대상 작업 트리 | 검사 시 clean. 최종 재확인은 `FINAL_CHECK.json` |

`TARGET_IDENTITY.json`에 요청문·원장·runner·시험·계약 관련 파일의 크기/SHA/git blob을 기록했다. `reviewed-code.diff`와 `registry-audit.json`을 함께 제공한다. 요청문에 있는 Linux 시험 숫자는 제출 측 보고이며 아래 독립 실행 결과와 구분한다.

반례는 reviewer 스크립트가 만든 별도 venv/전체 sandbox에서 실행했다. N1의 위조는 **영수증 reader 경계에 한 필드 변경본을 주입**한 검사다. 독립 provenance 인증을 뚫었다거나 전체 coverage artifact 위조/production 실행권 탈취까지 성공했다고 확대하지 않는다. N2는 정상 영수증을 그대로 사용한다. T1은 실제 subprocess와 커밋된 시험 함수의 두 원래 parameter를 사용하며 subprocess 결과를 가짜로 만들지 않았다.

## 3. 새 반례와 최소 종결 조건

### G67-N1 — 자동 import OFF가 이미 로드된 namespace의 부재 위조를 허용한다

**심각도 P1. 무효화 범위: customization 존재/종류의 영수증 결속.**

위치: [`mutation_replay.py:5990–5996`](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/cdc49e91af15b2ef968753110cfae3bbe7ab5c2f/degradation-degeneracy/docs/22p_gap/mutation_replay.py#L5990). 회귀의 빠진 축: [`test_gate66_defensive.py:167`](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/cdc49e91af15b2ef968753110cfae3bbe7ab5c2f/degradation-degeneracy/tests/test_gate66_defensive.py#L167)의 `on` fixture.

만드는 상태:

```text
startup/
  sitecustomize.py    # 내용: import usercustomize
  usercustomize/     # 빈 디렉터리. __init__.py 없음
```

표준 venv로 user-site를 OFF로 만들고 이 startup을 PYTHONPATH에 둔다. 실제 child와 문맥 probe 모두 `user_site=false`, `usercustomize.loaded=true`, `origin=null`, namespace locations 1개를 관측한다. 정직한 영수증은 namespace identity를 가진다. 이력의 file-backed `modules`에는 namespace 이름이 없다.

그 영수증을 복사해 **`startup.customization.usercustomize` 한 곳만 `<absent>`로 변경**한다. 다른 이력·digest·context는 바꾸지 않는다.

재현:

```powershell
python .\repro_boundaries.py --repo <고정checkout>\degradation-degeneracy --out <새결과경로>
```

실측:

| 동일 fixture의 조건 | 정상 영수증 | 한 필드만 위조한 영수증 |
|---|---|---|
| user-site OFF, 명시 namespace import | complete/parent/entry 모두 ACCEPTED | **complete/parent/실제 `_execution_receipt()` 모두 ACCEPTED** |
| user-site ON, 명시 namespace import | 모두 ACCEPTED | parent/entry REJECTED |

`_execution_receipt()` 확인에서는 `_observed_receipt` 반환만 위조본으로 바꿨고, fresh `_replay_context()`와 completeness/parent 검사는 실제 코드를 그대로 실행했다. 이는 reader 경계의 거부 조건을 검사하는 단위 적대 실험이다.

원인: `loaded_file=False`인 namespace에서 `elif auto and cand != '<absent>'`가 마지막 방어다. OFF이면 `auto=False`이므로 **parent가 namespace를 관측했어도** child의 `<absent>`가 통과한다. 새 회귀는 ON만 보므로 이 조합을 실행하지 않는다. “부모가 올렸다고 잰 것을 child가 absent라 하면 거부”라는 §2-2 설명은 현재 코드의 일반 규칙이 아니다.

**최소 종결 조건 N1:** 실제 loaded/kind/locations와 child 표현의 일치를 자동 import 정책과 무관하게 강제한다. OFF+명시 namespace의 `<absent>` 위조는 거부하고 정상 namespace는 수용해야 한다. OFF+실제 미로드의 정당한 `<absent>`도 계속 수용한다. ON/OFF × 명시 import/미로드 × 파일/namespace 대조를 분리한다. 모든 OFF를 거부하거나 namespace를 전부 금지하는 것으로 닫지 않는다.

근거: `boundary-cases/namespace_explicit_off/{context,receipt,forged,observation}.json`, ON 대조군, `boundary-cases/summary.json`.

### G67-N2 — 표준 ZIP package에서 사후 경로 재탐색이 정상 실행을 다시 거부한다

**심각도 P1. 무효화 범위: 정상 startup을 지원한다는 재생/증거 생성 계약. fail-open이나 실행권 탈취가 아니라 false rejection이다.**

위치: [`mutation_replay.py:5934–5941`](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/cdc49e91af15b2ef968753110cfae3bbe7ab5c2f/degradation-degeneracy/docs/22p_gap/mutation_replay.py#L5934).

PYTHONPATH에 표준 ZIP 하나를 놓고 `sitecustomize/__init__.py`에 다음만 넣는다.

```python
import os, sys
_arc = os.path.dirname(os.path.dirname(__file__))
sys.path[:] = [p for p in sys.path
              if os.path.normcase(os.path.normpath(p))
              != os.path.normcase(os.path.normpath(_arc))]
```

원본/archive/module을 지우지 않는다. 커스텀 loader도 없다. Python 표준 ZIP package가 정상 로드된 뒤 검색 경로에서 자기 archive만 빼는 상태다.

위 `repro_boundaries.py`가 세 대조를 함께 실행한다.

| ZIP fixture | native 로드 | complete | parent 및 실제 entry |
|---|---|---|---|
| package, 경로 유지 | 성공 | ACCEPTED | ACCEPTED |
| 단일 module, 경로 제거 | 성공 | ACCEPTED | ACCEPTED |
| **package, 경로 제거** | **성공** | **ACCEPTED** | **REJECTED / `_ReplayError`** |

오류는 “파일이 아니고 loader가 바이트를 못 준다. 지원하지 않는 loader”다. 하지만 origin은 정상 `archive.zip/sitecustomize/__init__.py`이며 child는 그 바이트를 읽어 영수증을 만들었다.

원인: 파일이 아닌 origin에는 여전히 `PathFinder.find_spec(name, [dirname(origin)] + final_search_path)`를 사용한다. package의 `dirname(origin)`은 archive root가 아니라 `archive.zip/sitecustomize`다. 그 안에서 다시 top-level 이름 `sitecustomize`를 찾으면 올바른 package가 아니고, archive root는 이미 final path에서 빠졌다. 일반 파일 분기를 고친 것이 ZIP package 분기의 실행 위치까지 고친 것은 아니다. 코드 주석의 “search_path는 진단용”과도 어긋난다.

표준 ZIP loader는 module과 package를 지원하며 archive/prefix/get_data 정보를 제공한다. 따라서 “모든 ZIP은 미지원”으로 환원할 문제가 아니다. [Python 3.12 zipimport 문서](https://docs.python.org/3.12/library/zipimport.html).

**최소 종결 조건 N2:** 지원하는 표준 loader의 실제 archive/prefix/member identity를 읽기 경로로 결속하고 **post-startup sys.path에서 fullname을 다시 찾는 데 의존하지 않는다.** origin 일치·바이트 재확인·읽기 실패 거부는 유지한다. plain file/package/ZIP module/ZIP package의 경로 제거·재정렬 정상 대조와 변조/읽기 불가 음성 대조를 분리한다. 임의 loader를 parent에서 무조건 실행하거나 child digest를 그대로 정답으로 삼지 않는다.

근거: `boundary-cases/zip_package_remove_path/{context,receipt,observation}.json` 및 같은 이름 ZIP, 나머지 두 ZIP 대조군.

### G67-T1 — 시험이 실행되지 않아도 새 전제 회귀는 초록이다

**심각도 P2. 무효화 범위: G66-T1 회귀의 실행 증거. 실제 interpreter fixture 수정 전체가 잘못됐다는 판정은 아니다.**

위치: [`test_gate66_defensive.py:240–261`](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/cdc49e91af15b2ef968753110cfae3bbe7ab5c2f/degradation-degeneracy/tests/test_gate66_defensive.py#L240).

`_premise_run`은 전체 env를 물려받는다. 외부 `PYTEST_ADDOPTS`만 바꾼 뒤 **커밋된 두 parameter `{}`, `{'PYTHONNOUSERSITE':'1'}`를 그대로** 실제 시험 함수에 전달했다.

```powershell
python .\repro_premise_no_execution.py --repo <고정checkout>\degradation-degeneracy --out <새결과경로>
```

| 상속 PYTEST_ADDOPTS | 실제 내부 subprocess | 커밋된 바깥 회귀 결과 |
|---|---|---|
| `--g67-option-does-not-exist` | rc 4, stdout 비어 있음, stderr usage error | 두 parameter 모두 정상 반환 |
| `--collect-only --json-report ...` | rc 0, 두 node 수집, JSON `total=0`, **call phase 0개** | 두 parameter 모두 정상 반환 |

pytest rc 4는 사용법 오류다. PYTEST_ADDOPTS가 CLI에 옵션을 추가하는 것은 pytest의 정상 동작이다. [Exit codes](https://docs.pytest.org/en/stable/reference/exit-codes.html), [PYTEST_ADDOPTS](https://docs.pytest.org/en/stable/reference/reference.html#envvar-PYTEST_ADDOPTS).

원인: 실제 assertion은 `"failed" not in stdout.lower()` 하나다. rc/stderr/정확 node 집합/call 실행 여부를 보지 않는다. **rc 0 검사만 추가해도 collection-only 반례는 남는다.** 이 재현은 실제 subprocess이고 CompletedProcess를 가짜로 돌려주지 않는다. 단독 재현기는 test 함수 호출 전 같은 child 명령의 stdout/stderr도 별도로 기록한다. JSON report는 해당 바깥 함수 호출이 재실행한 child의 결과다.

**최소 종결 조건 T1-a:** 통제된 child pytest 옵션/환경과 machine-readable 결과를 사용한다. 기대한 True/False 두 node가 실제 call에서 통과했음을 검사한다. 정책상 skip은 미측정으로 별도 보고하고, usage/setup/collection 오류·예상 node 누락·실행 0건은 PASS가 아니어야 한다. 누락 activation option 변이는 같은 축의 call failure로 계속 검출해야 한다.

#### 연관된 witness 보완 조건 — 실패 자체와 그 이유의 일치를 분리할 것

등록 변이 `the-premise-uses-a-controlled-env-g66`를 그대로 적용한 보충 실행은 baseline 2 passed → mutant 1 failed/1 passed였고 **EXPECT의 실패 node 집합과 call 실패는 일치**했다. 그러나 [`mutation_replay.py:5145`](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/cdc49e91af15b2ef968753110cfae3bbe7ab5c2f/degradation-degeneracy/docs/22p_gap/mutation_replay.py#L5145)의 witness에는 `stdout[-600:]`에서 우연히 잘린 `도 기대와 다르면 그때는`이 포함된다. 이 기계의 traceback 꼬리는 다른 위치에서 시작해 `call_witness_matches=false`였다.

**최소 종결 조건 T1-b:** 의미가 고정된 오류 코드/메시지를 witness로 삼고 경로·시간·traceback 절단 위치와 분리한다. 실패 집합·call phase·오류 이유는 모두 유지하며 witness를 아무 예외로 완화하지 않는다. 이번 관측을 “변이가 안 물었다” 또는 “변이가 정상적으로 전수 인증됐다” 어느 쪽으로도 바꿔 쓰지 않는다.

근거: `premise-no-execution/observations.json`, 네 stdout/stderr와 두 pytest JSON. witness는 `partial-mutations-final/the-premise-uses-a-controlled-env-g66.json` 및 mutant pytest JSON.

## 4. 66차 조건별 판정

| 항목 | 이번 판정 | 근거 |
|---|---|---|
| G66-N1 A: 읽지 않은 cwd 파일 | 원래 반례 닫힘 | 기존 재현기 그대로 full sandbox, 정상 영수증 entry ACCEPTED |
| G66-N1 B: 로드 후 자기 경로 제거 | 일반 파일 반례 닫힘 / 일반화 부분 | 기존 파일 반례 ACCEPTED. 새 ZIP package N2는 REJECTED |
| G66-N1 C: 사후 후보 재정렬 | 원래 반례 닫힘 | 기존 reorder_loaded_path entry ACCEPTED |
| altered bytes / file absent 거부 | 지정 회귀 수용 | 대상 회귀 및 loaded-origin 변이에서 검출. namespace OFF로 일반화 불가 |
| namespace absent 거부 | 부분 | ON 대조는 거부, OFF+명시 import N1은 수용 |
| G66-T1 PYTHONNOUSERSITE | 원래 반례 닫힘 / 증거 회귀 부분 | 직접 전제 시험 2 passed. 새 wrapper는 T1 false green |
| context 중복 측정 | 닫힘 | 지정 회귀 통과, registered 변이에서 기대 call failure/witness 일치 |
| G66-R1 삭제 사실과 원인 정정 | 사실관계 정정 수용 | 현재 delta 추가 1·삭제 0·기존 변경 0. 과거 삭제의 설명과 git tree 식별 일치 |
| R1 과거 authority 소비·복원·격리 | 미완 유지 | 이번 자료/정정만으로 역사적 소비 여부나 복원 정책을 확정할 수 없음 |
| Linux native 검증 | 제출 측 주장 / 독립 미측정 | Windows fcntl/proc 제약. 가짜 kernel로 바꿔 통과시키지 않음 |

## 5. 이번 기계의 실행 출력

| 명령/범위 | 실제 결과 | 인정 범위 |
|---|---|---|
| 직접 source_digest | `e9ee7475dea7de1d` | RUN_SCOPE identity |
| 기존 Gate66 재현기 5종 `--full-sandbox` | plain/cwd-only/cwd-on-path/remove/reorder **5종 모두 complete·comparison·entry ACCEPTED** | 원래 경로 반례 종결 |
| gate66/65/64 지정 시험, `--noconftest`, kernel_lock_probe_control_actually 제외 | **35 passed, 2 skipped, 1 deselected, 21.46s** | Windows에서 실행한 지정 축. Linux suite 대체 아님 |
| PYTHONNOUSERSITE=1, 직접 premise 시험 | **2 passed, 15 deselected, 0.55s** | 실제 on/off 전제 시험 |
| runner `--check-preimages` | rc 0, 모든 변이 지점 정확히 1회 | preimage 존재. kill 증거 아님 |
| 원래 conftest 포함 collection | rc 3, `/proc/self/mountinfo` 경계 식별 실패 | Linux 전제 미충족, 시험 실행 실패 |
| 원래 runner `-k g66 --keep-sandbox` | **rc 1, scenario 3, ran 0**. 세 항목 collection rc 3 | kill/coverage 0건. stderr의 Windows 디코딩 오류도 보존 |
| 별도 registered 변이 보충 실행 9종 | 아래 상세 | 공식 replay/coverage 인증 아님 |

보충 변이는 fresh full sandbox에서 원래 등록 old/new·selector·EXPECT를 사용하되 `--noconftest`로 실행했다. Linux kernel을 대체하지 않았다.

- 8종에서 baseline이 통과하고 mutant의 **정확 실패 node 집합과 call phase**가 일치했다.
- 그중 7종은 witness도 일치했다. 나머지 1종은 위 T1-b다.
- 9번째 `parent-customization-uses-the-path-finder-g63`는 이 환경에서 receipt_62 대조 한 건만 수집 가능했고 baseline/mutant 둘 다 passed였다. fcntl을 import하는 gate63 package 대조를 실행하지 못했으므로 이 축의 전체 EXPECT를 검증하지 못했다. 이를 새로운 product 결함이나 kill로 세지 않는다.

최종 수치는 `partial-mutations-final/summary.json` 기준이다. 앞선 시도에는 gate63의 fcntl 수집 실패, pytest 기존 temp root 접근 실패, 길어진 temp 경로의 생성 실패가 있었다. 이를 고친 **reviewer 실행 환경**은 짧은 새 temp root뿐이다. 원자료는 `partial-mutations`, `partial-mutations-portable`, `partial-mutations-isolated`에 보존했고, setup 오류를 mutant kill로 세지 않았다. production 코드를 고쳐 결과를 만든 것이 아니다.

전체 pytest·strict smoke·Linux native 3종은 이 기계에서 완주하지 않았다. 요청문의 `1772 passed · 1 failed · 1 skipped · 2 xfailed`, smoke rc 0, token 3 passed는 **제출 측 실측 보고**로 남긴다. 없는 results/ 산출물과 로컬 cache 재봉인에 대한 설명은 여기서 독립 재현하지 않았다. 위 Windows 실패를 그 제출 환경의 코드 실패로 바꿔 세지도 않는다. 전체 pytest 도중 HEAD 이동이 있었다는 신고도 유지한다.

## 6. 질문 다섯 개에 대한 답

### Q1. helper가 origin을 주고 parent가 바이트를 읽으면 충분한가?

**정직한 동일-startup helper를 신뢰한다는 제한 안에서 일관성을 비교하는 것과, 실제 실행 코드의 독립적 출처 인증은 다르다.** 후자를 닫았다고 할 수 없다. 그 경계는 이미 신고됐으므로 새 발견으로 다시 세지 않는다.

게다가 현재 probe는 startup 완료 후 `sys.modules`의 `__file__`/`__spec__.origin`을 읽는다. **로드 순간의 불변 기록**은 아니다. Python도 module과 spec 속성 사이에 자동 동기화가 없고 런타임 수정이 가능함을 설명한다. 따라서 주석/문서의 “로드 시점 origin”을 “startup 후 관측한 module origin”으로 좁혀야 한다. [ModuleSpec 문서](https://docs.python.org/3.12/library/importlib.html#importlib.machinery.ModuleSpec).

이를 보완하려고 사후 sys.path에서 후보를 다시 고르는 것은 원래 N1 문제로 되돌아간다. 더 강한 주장은 trusted launcher/immutable input bundle 등 별도 신뢰 경계 설계와 실제 로드 증거가 필요하다. 이번 범위에서는 선언 경계를 유지하되 **그 안에서도 모순인 N1을 먼저 거부**해야 한다.

### Q2. ZIP spec.origin == 측정 origin 조건이면 충분한가?

**아니다.** 일치 조건은 다른 대상을 잘못 읽지 않기 위한 조건이지, 원래 loader/member를 다시 찾을 수 있다는 보장이 아니다. N2가 표준 ZIP package로 반증한다. archive/prefix/member 및 지원 loader 종류를 정확히 다루고 사후 검색 경로 의존을 제거해야 한다. 원래 바이트 비교는 유지한다.

### Q3. auto를 유지할 것인가?

**부재 위조를 거부하는 근거로는 auto를 쓰면 안 된다.** 자동 import OFF와 이미 명시적으로 로드됐다는 사실은 양립한다. measured loaded/kind/locations와 영수증을 먼저 비교하고 file history의 모순도 별도로 검사한다. namespace에 대한 이름별 이력을 추가하는 방향은 가능하지만, 현재의 이름 없는 unfiled 집계만으로 namespace 부재를 입증할 수 없다.

### Q4. 환경변수를 더 통제해야 하는가?

PYTHONNOUSERSITE 통제는 원래 문제를 해결했다. 그러나 **시험 launcher 경계에는 PYTEST_ADDOPTS 등 별도의 입력**이 있다. 허용 pytest 옵션·plugin/config 로딩 정책을 명시하고, 환경 통제와 별개로 실제 expected call 결과를 검사해야 한다. env 이름을 하나씩 계속 삭제하는 것만으로 T1은 닫히지 않는다. 통제 불가 정책 skip도 PASS와 별도다.

### Q5. R1 영향 확인을 격리 계약 승인까지 미룰 것인가?

**읽기 전용 영향 확인을 먼저 하고, 복원/삭제/class 변경/격리 migration을 별도로 승인받는 순서가 맞다.** 과거 권한 소비 여부를 조사하는 것과 authority를 바꾸는 것은 같은 행위가 아니다.

이번 직접 확인: tracked registry 366→367, 추가 1(`eb9aabdd…`), 삭제 0, surviving JSON 변경 0. 과거 175개 삭제 경로와 이전/현재 git tree blob 식별도 재대조했다. 삭제 JSON의 sealed/class/evidence 통계는 앞선 독립 검토 원자료를 재사용했으며 이번에 175개 본문을 모두 재독한 것으로 쓰지 않는다. `registry-audit.json`에 범위를 나눴다.

현재 `read_execution_class`/`resolve_execution_class`의 code path를 확인하는 것만으로 “그 175개가 과거에 authority로 소비되지 않았다”는 역사적 부정을 증명할 수 없다. 각 ID의 생성·삭제 이력, 연결 산출물/영수증/승격·원장 참조와 당시 소비 가능한 경로를 읽기 전용으로 대조하고, 자료 부재는 미확인으로 남겨야 한다. 그 뒤 test namespace 격리·tombstone·복원 중 정책을 결정한다. **이번 리뷰는 복원이나 class 변경을 승인하지 않는다.**

## 7. 다음 라운드의 최소 수용 조건

1. N1: user-site OFF+명시 namespace의 한 필드 `<absent>` 위조 거부, 정상 namespace/정상 미로드 대조 수용.
2. N2: 표준 ZIP package의 archive 경로 제거·재정렬 후에도 정상 영수증 수용. 변조된 bytes/다른 origin/읽기 불가 거부 유지.
3. T1-a: rc 4 및 collection-only를 PASS로 만들지 않기. 정확 두 premise node의 실제 call 증거, skip 미측정 구분, activation-option 변이 유지.
4. T1-b: 가변 stdout 꼬리가 아닌 고정 이유 witness. 정확 실패 집합·단계·이유를 유지한 재생 출력.
5. 위 코드/시험의 고정 full SHA에서 Linux native 검증과 runner 재생 원자료 제출. 이 기계의 `--noconftest` 보충 결과를 공식 coverage로 대체하지 않기.

등록부 영향 확인은 별도 읽기 전용 과제로 진행 가능하다. 등록부 격리·F50b의 RUN_SCOPE 변경·error_code 매트릭스 등의 기존 우선순위/승인 경계는 유지한다. 알려진 독립 GO 전제를 새 반례 수에 더하지 않는다.

**최종: 부분 수용 / 종결 NO-GO. 핵심은 새 검사가 없다는 것이 아니라, 이미 측정한 사실을 실제 판정과 실행 증거에 끝까지 연결하지 않았다는 것이다.**
