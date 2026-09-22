# Gate65 방어층 리뷰 — 종결 불수용, 부분 수용

2026-09-22. 사용자 승인 범위: N1·N2·E2-R 대응, 정상 입력 거부 경로, 요청문 질문 검토. **본 실행 GO 심사가 아니다.** 과학 계산·COMSOL·BMS R17은 이번 범위 밖이다.

## 결론

**“접수 셋 전부 종결”은 수용하지 않는다.** 새로 확인한 것은 **P1 3건·P2 1건**이다. 두 P1은 수정하지 않은 실제 `_execution_receipt()` 진입점에서 재현했다. 추가 P1은 표준 namespace package를 실제로 import한 탐침 본문과 완전성 검사에서 재현했다. P2는 정상 venv에서 커밋된 회귀를 실행해 확인했다.

- N1 원래 사례(비활성 user site, 명시 import 없음)는 해결됐다. 그러나 “자동 import 비활성”을 “모듈 미로드”로 바꾸는 새 전제가 틀리다.
- N2 원래 ZIP package 사례는 해결됐다. 일반 파일·ZIP package·일반 customization의 ZIP 모듈 import 대조도 통과했다. 이를 모든 정상 origin의 지원으로 확대할 수는 없다.
- E2-R은 커밋된 음성 assertion 추가를 확인했다. **Linux 커널 실행은 이번 환경에서 확인하지 못했다.** 실제 lifecycle이 사용하는 token 탐침과 새 음성 대조군의 path 탐침이 서로 다른 함수라는 추가 검토 사항도 남는다.
- §0의 미착수 GO 전제와 이미 신고된 등록부 오염은 새 발견으로 세지 않았다. 이번 결과를 본 실행 승인으로 사용하지 않는다.

## 1. 고정한 정본과 실제 검증 범위

| 항목 | 관측 |
|---|---|
| fetch 후 고정 HEAD | `5e4cf1038f0f26a6a624d9984386cfd046657ac3` |
| 과학 코드 정본 | `743f65bead671bf353ce38027c2e8e457738ec08` |
| `source_digest()` 실측 | `e9ee7475dea7de1d` |
| 정본→HEAD RUN_SCOPE log / diff | 둘 다 rc 0, 빈 출력 |
| 리뷰 종료 시 대상 checkout 상태 | `git status --porcelain` 빈 출력 |
| Python / 플랫폼 | CPython 3.12.14 / Windows |

RUN_SCOPE 밖의 파일은 별도로 SHA-256을 고정했다. 전체 목록은 `FINAL_AUDIT.json`이다.

| 파일 | SHA-256 |
|---|---|
| `docs/22p_gap/mutation_replay.py` | `777ca1d6a1a4f993fac739ac04d75cbe0b23eb376e4bd908a74ab2fa591b984c` |
| `tests/test_gate63_defensive.py` | `101d08ef6a949ef9c4264b5199a2fd98f6af9672c56bc68e8292f8b9b146c679` |
| `tests/test_gate64_defensive.py` | `988c62cdc70ff4fdcb065572a8ed03a02d70784f2fcbc65a0a6577791195141d` |

첨부 GATE65 요청문보다 브랜치 요청문이 뒤다. 브랜치 문서에는 신고⑩/질문5가 추가돼 있어 같이 검토했다. 검토 중 HEAD를 움직이지 않았다.

### 직접 실행 결과

| 검사 | 결과·해석 |
|---|---|
| `mutation_replay.py --check-preimages` | **rc 0**, 133.594초. 지점 일치 검사이지 변이 실행 성공이 아니다 |
| Gate64 방어 회귀, user-site 활성 환경 | **9 passed, 1 deselected**. 커널 lock 1건 제외 |
| 같은 9건, 일반 user-site 비활성 venv | **1 failed, 8 passed, 1 deselected**. G65-T1 |
| 커널 lock 1건 별도 시도 | `ModuleNotFoundError: fcntl`. 커널 동작 미실행 |
| 원래 `mutation_replay.py -k g64 --keep-sandbox` | **rc 1, scenario 3, ran 0**. 세 항목 모두 collection rc 3 |
| collection 오류 독립 재확인 | conftest의 frozen seal 초기화가 `/proc/self/mountinfo` 부재로 `BoundaryUnknown` |
| 실제 `_execution_receipt()` 정상 입력 반례 | 완전성 검사 PASS 뒤 customization 대조에서 **2건 거부** |
| namespace package | 실제 startup 성공 후 history가 **failed**, 완전성 검사 거부 |

9건은 **`--noconftest`**로 실행했다. 해당 파일의 선택된 시험은 저장소 conftest의 사용자 fixture를 요구하지 않는다. Linux 전용 seal bootstrap을 우회한 **한정 시험**이지 원래 전체 pytest 명령의 성공이 아니다. enabled/disabled 두 인터프리터를 구분했고 `10 passed`로 합산하지 않는다.

Windows의 자식 출력 cp949/부모 UTF-8 차이로 변이 실행 로그 수집에 `UnicodeDecodeError`도 발생했다. 원시 바이트로 collection 오류를 재수집해 위 mountinfo 원인을 확인했다. 이를 Linux 운영 코드 결함으로 세지 않았다. WSL 접근은 거부됐으며 설정 변경·권한 우회는 하지 않았다.

**전체 pytest, strict smoke, 변이 전수 재생, evidence_layer_58 전체, 실제 planned grid→fit는 이번에 완주/통과했다고 주장하지 않는다.** 요청문의 전체 pytest 칸도 여전히 `<대기: 실행 중>`이다.

## 2. 새 반례와 최소 종결 조건

아래 소스 줄은 위 고정 HEAD 기준이다. 재현기는 원본 Python 파일을 수정하지 않는다. 출력 폴더는 기존 자료를 덮지 않도록 새 경로를 요구한다.

### G65-N1a — P1 / 증거 가용성: 자동 import 비활성은 명시 import 부재가 아니다

자리: [mutation_replay.py:5668–5673](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/5e4cf1038f0f26a6a624d9984386cfd046657ac3/degradation-degeneracy/docs/22p_gap/mutation_replay.py#L5668).

만드는 상태:

1. 기본 venv처럼 `site.ENABLE_USER_SITE == False`인 인터프리터를 사용한다.
2. 정상 `sitecustomize.py`에는 `import usercustomize` 한 줄을 둔다.
3. 같은 디렉터리의 `usercustomize.py`는 `VALUE = 42`뿐이다. 그 디렉터리를 절대 PYTHONPATH로 준다.
4. 원래 ROOT·원래 `replay_env()`·원래 `_execution_receipt()`를 그대로 호출한다.

실측 (`real_entry_cases/observations.json`):

```text
receipt_complete: true
enabled: false
child.usercustomize: 1cfeb13a2258c8d8
parent.usercustomize: <absent>
entry_result: REJECTED (_ReplayError)
```

startup history도 성공했고 파일은 읽을 수 있다. receipt 위조·sys.modules 삭제·해시 세탁은 없다. 단지 Python의 일반 import다. 공식 `site` 설명도 ENABLE_USER_SITE 조건을 **site가 수행하는 자동 import 시도**에 적용한다. 다른 모듈의 명시 import 금지로 설명하지 않는다. [Python site 문서](https://docs.python.org/3.12/library/site.html#usercustomize).

원인: 부모는 boolean이 false면 origin 확인 전에 무조건 `<absent>`를 넣는다. “찾을 수 있음≠자동 실행됨”을 고치며 “자동 실행 안 함=실제로 로드 안 됨”이라는 다른 등식을 만들었다.

최소 종결: 비활성+미로드, 비활성+정상 명시 로드, 활성+자동 로드 세 상태를 구분한다. 각각 일치하는 바이트는 수용하고 바뀐 바이트는 거부하는 회귀를 둔다. 조건을 모르는 경우의 fail-closed는 유지한다. 단순히 usercustomize 대조를 없애거나 child가 준 digest를 정답으로 사용하면 종결이 아니다.

### G65-N1b — P1 / 증거 가용성: 상대 PYTHONPATH를 부모 cwd로 다시 해석한다

자리: [mutation_replay.py:5578](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/5e4cf1038f0f26a6a624d9984386cfd046657ac3/degradation-degeneracy/docs/22p_gap/mutation_replay.py#L5578), [5654–5656](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/5e4cf1038f0f26a6a624d9984386cfd046657ac3/degradation-degeneracy/docs/22p_gap/mutation_replay.py#L5654).

상태: 호출 디렉터리에만 `startup/sitecustomize.py`(주석 한 줄)를 두고 `PYTHONPATH=startup`으로 실행한다. replay 탐침의 cwd는 실제 저장소 ROOT다. 저장소의 `startup/`에는 그 모듈이 없다.

실측 (원래 ROOT와 실제 `_execution_receipt()`, `real_entry_cases/observations.json`):

```text
receipt_complete: true
child.sitecustomize: <absent>
parent.sitecustomize: 2e252a13409dfd33
entry_result: REJECTED (_ReplayError)
```

별도 격리 fixture에서는 양쪽 cwd에 서로 다른 정상 파일을 두어, 두 digest가 달라지는 경우도 재현했다 (`import_full_cases/relative_pythonpath`). 어느 경우도 읽기 실패나 추가 프로세스 생성 실패가 아니다.

원인: child는 `cwd=...`로 실행하지만 부모는 원시 상대 PYTHONPATH와 **부모 자신의 sys.path**를 PathFinder에 넘긴다. 같은 executable/env 문자열만으로 경로 해석 문맥이 같아지지 않는다.

추가로 **호출 cwd를 지시대로 실제 ROOT에 둔 경우도 재현했다.** upstream runner가 만든 실제 sandbox를 읽기 전용으로 재사용하고 ROOT 밖 customization을 상대 PYTHONPATH로 지정했다. `_observed_receipt`는 sandbox cwd에서 미로드, 부모는 ROOT 상대 파일 digest를 기대해 실제 `_execution_receipt()`가 거부했다 (`real_entry_sandbox_cases/observations.json`, `relative_from_repo_with_real_sandbox`). 보조 user-site 탐침도 sandbox가 아니라 ROOT를 쓴다. 따라서 단순히 “저장소 안에서 실행하라”로는 닫히지 않는다. 이 확인에서 SANDBOX 변수는 runner의 이미 생성된 복사본으로 지정했으며 ROOT·생산 함수·replay_env는 수정하지 않았다.

최소 종결: cwd·argv·env·정규화된 검색 경로를 하나의 replay 문맥으로 고정해 탐침·재생·부모 대조가 공유한다. 단순 `resolve()`를 호출자 cwd에서 하는 수정은 안 된다. 상대/절대 PYTHONPATH, 다른 호출 cwd, sandbox 유무의 대조군을 둔다. 부모 pytest가 추가한 sys.path를 child 검색 경로라고 가정하지 않는다.

### G65-N2b — P1 / 증거 상태 모델: 정상 namespace customization을 모순으로 오분류

자리: [mutation_replay.py:5229](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/5e4cf1038f0f26a6a624d9984386cfd046657ac3/degradation-degeneracy/docs/22p_gap/mutation_replay.py#L5229), [5346–5350](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/5e4cf1038f0f26a6a624d9984386cfd046657ac3/degradation-degeneracy/docs/22p_gap/mutation_replay.py#L5346).

상태: PYTHONPATH 아래에 빈 `sitecustomize/` 디렉터리만 둔다. `__init__.py`는 없다. Python은 정상 namespace package로 import하며 `__file__`은 None이다.

실측 (`namespace_case_corrected/observation.json`):

```text
startup.status: measured
startup.startup_history.status: failed
reason: 손자는 sitecustomize 을 올렸다는데 customization 은 <absent> 다 — 어긋난 증거
_assert_receipt_is_complete: _ReplayError
```

최초 원래 frame 호출에서는 위 진단의 em dash 출력이 Windows cp949에서 먼저 실패했다. **원인을 분리한 재현은 JSON 직렬화만 `ensure_ascii=True`로 바꿨다.** `_ENV_PROBE_BODY`, 실제 import, history 규칙, 완전성 검사 코드는 원본 그대로다. 이것은 원래 frame 경로의 native 성공을 주장하는 시험이 아니다.

원인: `__file__` 부재를 `<absent>`에 접고, 성공한 import 기록과 `<absent>` 조합을 무조건 모순으로 본다. 뒤에는 namespace를 정상 unfiled로 다루는 분기가 있고 부모 함수 주석도 namespace 지원을 명시하지만, 앞의 모순 검사에서 먼저 막힌다. 기존 ZIP 결함의 재발이 아니라 **다른 정상 origin 종류의 기존 결함을 새로 확인한 것**이다.

최소 종결: 실제 미로드 / 로드된 namespace·builtin·frozen / 읽을 수 있는 파일·ZIP / 읽기 실패를 구분한다. namespace identity는 그 종류와 검색 위치 등 필요한 구조에 결속한다. “모든 origin 없는 모듈을 정상으로 통과”시키는 수정은 금지한다. 표준 빈 namespace, 일반 파일, ZIP, 읽기 실패 네 축이 각각 자기 이유로 검사되어야 한다.

### G65-T1 — P2 / 회귀 신뢰도: 활성 대조군이 활성을 만들지 않는다

자리: [test_gate64_defensive.py:105–127](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/5e4cf1038f0f26a6a624d9984386cfd046657ac3/degradation-degeneracy/tests/test_gate64_defensive.py#L105).

`test_an_enabled_user_site_still_compares_the_bytes`는 환경변수 하나를 지우지만 `pyvenv.cfg`로 비활성화된 user site는 켜지지 않는다. 동일 소스에서:

```text
user-site 활성 인터프리터: 9 passed, 1 deselected
일반 비활성 venv:         1 failed, 8 passed, 1 deselected
실패: line 122, assert child != '<absent>'
```

N1의 생산 코드 검사가 실패한 것이 아니라 **시험이 자기 전제를 구성하지 못한 것**이다. 이 파일이 venv 관련 수정의 대조군이므로 “그 환경에서는 원래 실패”로 종결할 수 없다.

최소 종결: 활성/비활성 interpreter fixture를 명시적으로 구성하고 실제 ENABLE_USER_SITE를 확인한 뒤 양쪽을 실행한다. 활성 환경을 만들 수 없으면 정확히 skip/미측정으로 보고하되, CI의 적어도 한 고정 환경에서는 활성 및 바이트 변경 거부가 실제로 돈다는 증거를 남긴다. 활성 확인 assertion 자체를 지우는 수정은 안 된다.

## 3. E2-R 판정과 추가 검증 제안

새 path 탐침은 없는 파일을 False로 처리하지 않는다. `os.open()` 실패는 전파되고, 시험은 release로 사라진 경로를 확인한 뒤 새 파일을 만들고 flock을 시도한다. 따라서 **“열 수 없음=안 잡힘”이라는 바로 그 오판은 소스에서 확인되지 않는다.** 새 path 함수가 상수 True라면 마지막 False assertion은 실패해야 한다.

그러나 실제 planned lifecycle의 관측(기존 시험 479·487줄)은 `_kernel_lock_held(tok)`이고, 새 음성은 별도 `_kernel_lock_held_at(path)`다. token 함수는 계속 True 쪽에서만 불린다. 등록된 E2-R 변이도 token helper를 망가뜨리는 것이 아니라 **시험의 False assertion을 바꾸고 다른 AST 시험으로 검출**하는 것이다.

따라서 “커밋된 음성 assertion 없음”이라는 좁은 지적은 수정됐지만, 실제 사용하는 token predicate까지 양방향으로 검증됐다는 결론은 보류한다. 같은 살아 있는 token/inode에서 `flock(tok.fd, LOCK_UN)` 후 token 탐침의 False를 확인하거나, 두 wrapper가 공유하는 단일 fd 판정 함수에 양방향 시험을 둬야 한다.

`repro_e2_linux_NOT_RUN.py`에 정상 token 양방향 대조와 token helper 상수 True 변이 후 두 커밋된 대조군을 실행하는 후속 스크립트를 제공했다. **이 스크립트는 이번 Windows에서 미실행이며 새 확정 발견 수에 포함하지 않았다.** 실제 kernel lock 대신 mock·Windows 잠금으로 치환하지 않았다.

## 4. 요청문 질문에 대한 답

### Q1 / ⑨ — 추가 프로세스와 실행 문맥

같은 실행파일·env만으로 충분하지 않다(G65-N1b). 또한 ENABLE_USER_SITE는 로드 이력의 완전한 대용물이 아니다(G65-N1a). 추가 interpreter 자체를 못 띄우면 거부한다는 정책은 fail-closed로 정당할 수 있지만, 이번 두 반례는 **추가 interpreter도 성공한 정상 환경**이다. 신고⑨로 흡수할 수 없다.

부모의 `-s/-S`를 child에 자동 상속하지 않는 것은 실제 argv를 그 방식으로 계약했다면 그 자체로 오류가 아니다. 대신 부모 sys.path를 child 것처럼 쓰지 말아야 한다. 모든 flag 조합을 이번에 전수 실행했다고 주장하지 않는다.

### Q2 — loader 범위

`get_data`는 모든 loader의 필수 기능이 아니다. `ResourceReader/get_resource_reader`도 별도 optional interface다. 둘의 부재를 같은 말로 쓰지 않는다. bytes를 제공하지 않는 loader를 **명시적인 미지원 상태**로 거부하는 정책은 합리적일 수 있다. 임의 loader를 전부 수용하는 것이 최소 수정 조건은 아니다. 다만 Python 표준 namespace처럼 코드가 없을 뿐인 경우와 bytes 읽기 실패는 구분해야 한다. [Python importlib 문서](https://docs.python.org/3.12/library/importlib.html#importlib.abc.ResourceLoader).

### Q3 — 음성 대조

위 §3과 같다. 경로 탐침에 진짜 음성을 추가했으나 token 탐침의 음성 및 native 실행 확인은 남았다.

### Q4 — 증인 문맥 의존을 기계로 줄이는 방법

이번 고정 문구는 이전 특정 digest 문제를 줄였다. 다만 `except _ReplayError` 전체를 같은 AssertionError로 바꾸면 **다른 원인의 _ReplayError까지 N1 증인으로 보일 수 있다.** 이번에 그 오분류의 새 실행 반례를 확정한 것은 아니므로 새 finding으로 세지 않는다.

권고: 사람이 읽는 설명과 별개로 고정 `error_code`·검사 단계·관련 필드를 내보내고 정확한 실패 원인에 assertion을 건다. EXPECT는 traceback 전체보다 구조화된 실패 ID/단계를 사용한다. 정당한 cwd·임시 경로·활성/비활성 interpreter 문맥을 바꿔도 동일 변이가 동일 실패 ID를 내는 matrix를 둔다. 정규식으로 경로·숫자 문자열을 지우는 것만으로 의미 동일성을 보장하지 않는다. 이번 upstream 변이 재생 성공은 미확인이다.

### Q5 / ⑩ — 등록부 오염은 경로와 의미를 함께 격리

첨부본의 191/366을 현재 관측치로 옮겨 적지 않았다. 고정 HEAD의 **tracked root JSON은 541개**다. evidence 문자열별 직접 집계는:

- `_complete_artifact` 합성 기록: **261개**
- `leg=L phase=grid class=canonical` 완료 기록: **264개**
- re-key/legacy 설명 기록: **16개**

문자열 분류는 provenance 검증이 아니다. 264개를 실제 과학 실행이라고 확인한 것이 아니며, 반대로 541개 전부가 `_complete_artifact`라고 말하지 않는다. 이 누적 문제 자체는 이미 신고돼 새 발견으로 세지 않는다.

권고는 **둘 다**, 단 운영 authority와 테스트 authority를 구분해서 적용한다.

1. 모든 회귀/자식 프로세스가 사용할 임시 원장·등록부를 실행 전 주입하고, production 등록부 전후 불변을 확인한다. 세션 끝에 지우는 conftest(155–191줄)만으로는 중단·동시 실행을 격리하지 못한다.
2. 운영 등록부에는 시험 synthetic 산출물을 canonical 권한으로 유입시키지 않는다. 단 **격리된 시험 등록부의 canonical positive fixture까지 일괄 smoke로 바꾸면**, 실제 canonical 경로 시험을 잃는다. 테스트 안에서는 필요한 class 의미를 유지하되 운영 reader가 그 authority를 소비하지 못하게 한다.
3. `local/`로 옮기는 것만으로 충분하지 않다. production reader가 그 경로를 읽는지, class/authority가 승격 권한을 주는지 함께 고정해야 한다. gitignore는 신뢰 경계가 아니다.
4. 기존 기록은 근거 목록을 고정하고 append-only supersession/revocation/새 registry epoch 등 **reader가 실제 반영하는** 무효화 절차로 정리한다. JSON 삭제 또는 기존 sealed 내용을 소급 고치는 작업은 이번에 하지 않았다. 기존 class/삭제 계약 변경은 별도 승인 대상이다.

## 5. 재현 명령

리뷰 파일을 임의 디렉터리에 두고 `REPO`를 고정 HEAD의 `degradation-degeneracy` 절대 경로로 지정한다. 아래 출력 폴더는 매번 새 이름으로 바꾼다. 원본 저장소는 수정하지 않는다.

```powershell
# 일반 venv: include-system-site-packages=false. 재현 자체는 표준 라이브러리만 사용.
python -m venv gate65-normal-venv
gate65-normal-venv\Scripts\python.exe repro_real_entry.py --repo "<REPO>" --out "<새 출력 폴더>"
# 기대: 두 receipt_complete=true, 두 entry_result=REJECTED → 현재 결함 재현.

python repro_namespace.py --repo "<REPO>" --out "<다른 새 출력 폴더>"
# 기대: namespace의 startup_history=failed, completeness=_ReplayError.

# pytest가 설치된 일반 비활성 venv에서 실행. Linux/Windows 모두 같은 전제 문제를 검사.
python -m pytest "<REPO>/tests/test_gate64_defensive.py" --noconftest -p no:cacheprovider -q `
  -k "not kernel_lock_probe_control_actually" --basetemp "<새 임시 폴더>"
# 이 리뷰 Windows 실측: 1 failed, 8 passed, 1 deselected.
```

Linux 후속: `python repro_e2_linux_NOT_RUN.py --repo "<REPO>"`. 이 명령의 예상 영향은 시험용 임시 lock 파일과 메모리 내 helper 대체뿐이다. **결과를 받기 전에는 통과/변이 생존 숫자를 채우지 않는다.**

`run_checks.py`는 이 PC의 리뷰 환경에 묶인 실행 기록 도우미이고, portable 재현기는 위 `repro_*.py`다. `verify_observations.py`는 저장된 관측의 자기 정합성 검사이며 upstream 독립 replay가 아니다.

초기 진단에서 namespace 출력 경로를 상대 경로로 준 잘못된 1회(`namespace_case/`)와 json-report plugin이 없는 venv에 report 인자를 준 실패(`disabled_missing_report_plugin.*`)도 보존했다. **둘은 발견의 근거에서 제외**했다. 유효 근거는 `namespace_case_corrected/` 및 최종 `target_disabled_venv.*`다.

## 6. 최소 재심 조건

1. 비활성+명시 import 정상 receipt를 수용하고 bytes 변경은 거부한다(G65-N1a).
2. 실제 replay 문맥으로 상대 경로·검색 순서를 고정하고 다른 cwd에서도 정상 receipt를 수용한다(G65-N1b).
3. 표준 namespace를 미로드/읽기 실패와 구분하며 파일·ZIP·읽기 실패 대조를 유지한다(G65-N2b).
4. 활성/비활성 interpreter 회귀 전제를 명시적으로 만들고 두 환경 결과를 제출한다(G65-T1).
5. Linux에서 원래 커널 대조와 g64 3개 replay를 실행한다. token/path 탐침의 음성 결속을 별도로 확인하고, 전체 pytest 미완 숫자를 완주 증거로 바꾸지 않는다.

**최종: 이번 방어층의 전부 종결에는 NO-GO(부분 수용). 본 실행 GO는 별도이며 승인하지 않았다.** 원본 코드·원장·registry·원자료의 수정, push, 장시간 계산은 하지 않았다.
