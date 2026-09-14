# R10 evidence subreview — target `bd6ba4749a92f8d441b4d9176eb876bfc6cc287c`

범위: R9 P2-1~5, R7/R9 closure runner의 대상·패키지 결속, mutation 분류, `run_states.sh` sidecar와 `ne_shape` status 소비. 검토 대상은 수정하지 않았다. 모든 변이·dirty fixture는 임시 저장소에서 실행했다.

## 결론

증거 층만으로도 **NO-GO**다. 실행 가능한 새 반례는 P1 3건, P2 3건이다. 좁은 `classify()` 수정(rc 1+failed만 CAUGHT)은 맞지만, 그 판정을 감싸는 closure runner가 실패를 성공으로 만들 수 있다.

## E1 — P1 · `python -O`가 실패한 probe를 `closed:true`로 인증한다

자리:

- `reviews/r7_repros/replay_codex_r7.py:80-91`
- `reviews/r9_repros/replay_codex_r9.py:94-105`
- `reviews/r9_repros/replay_codex_r9.py:245-252`

positive closure, delegated pytest return code, 결과 조건이 전부 언어 `assert`다. 최적화 모드에서는 이 검사가 실행되지 않는다.

재현:

```bash
PYTHONOPTIMIZE=1 PYTEST_ADDOPTS=--definitely-invalid-option \
python reviews/r9_repros/replay_codex_r9.py \
  --target . --expected-head bd6ba4749a92f8d441b4d9176eb876bfc6cc287c \
  --probes P2-4
```

관측: delegated pytest는 `--definitely-invalid-option` usage error인데 러너는 rc 0, `dirty:false`, `package_digest_ok:true`, P2-4 `상태:"반례 소멸"`, `closed:true`를 냈다. JSON의 `summary` 자체가 usage error를 보여 준다.

최소 조건: 증거 판정에 `assert`를 쓰지 말고 명시적 조건 분기/예외를 사용한다. 시작 시 `sys.flags.optimize != 0`도 fail-closed하고, 각 subprocess의 실제 rc와 기대 fingerprint를 최종 `closed` 계산에 값으로 결속한다.

## E2 — P1 · `git status` 실패를 clean으로 바꾼다

자리:

- R7 `dirty_paths`: `reviews/r7_repros/replay_codex_r7.py:68-71`
- R9 `dirty_paths`: `reviews/r9_repros/replay_codex_r9.py:62-65`

두 함수 모두 stdout만 읽고 return code/stderr를 버린다.

재현은 `GIT_INDEX_FILE`을 디렉터리로 둔다. 같은 명령의 직접 `git status`는 rc 128 (`unable to map index file`)이지만 R9 P2-3 runner는 rc 0, `dirty:false`, `closed:true`였다.

최소 조건: `git status` rc가 0이 아니면 즉시 증거 오류. stdout/stderr와 실행한 Git 경로/version을 receipt에 남긴다. `subprocess.run(..., check=True)` 또는 같은 명시 분기가 필요하다.

## E3 — P1 · HEAD+porcelain은 실행한 bytes의 identity가 아니다

자리: E2의 `dirty_paths`와 두 runner의 HEAD/dirty preflight(R7 `:156-167`, R9 `:318-328`).

서로 독립인 두 재현을 했다.

1. 임시 fixture에서 `git update-index --assume-unchanged bms_balancing/verify.py` 후 그 tracked source에 marker를 추가했다. `git status --porcelain`은 빈 값, 수정 모듈은 실제 import·실행됐고 runner는 rc 0, `dirty:false`, `closed:true`였다.
2. 저장소 정책상 무시되는 `bms_balancing/__pycache__/verify.cpython-312.pyc`를 원본 source mtime/size와 맞춘 변조 bytecode로 만들었다. porcelain은 빈 값, 변조 bytecode marker가 실행됐고 runner는 다시 clean/closed를 기록했다.

이는 E2의 “status 오류”와 다르다. status가 정상 rc 0을 내도 실행 bytes가 commit tree와 다를 수 있다. `assume-unchanged`는 index 신뢰 경계, ignored pyc는 interpreter 신뢰 경계다.

최소 조건: evidence 실행은 expected commit에서 새로 materialize한 격리 snapshot에서 하고, 실행 대상 tracked file bytes를 tree blob과 대조한다. skip-worktree/assume-unchanged를 거부한다. 무시 파일이 import에 참여하지 못하도록 clean archive/temporary checkout과 격리된 pycache를 쓴다. 단순히 `git status` 검사를 하나 더 붙이는 것은 이 반례를 못 닫는다.

## E4 — P2 · P2-4의 “exact argv”는 비가역 문자열이며 회귀도 production binding을 안 돈다

자리:

- production binding: `scripts/run_states.sh:171-185`, 특히 `LAST_ARGV="$*"`
- 회귀: `tests/test_r9_codex.py:285-302`

현재 sidecar는 argv 배열이 아니라 `$*` 문자열이다. 다음 두 벡터는 서로 다르지만 같은 `cmd a b c`가 기록된다.

```text
["cmd", "a b", "c"]
["cmd", "a", "b c"]
```

더구나 named 회귀는 `run()`을 호출하지 않고 `LAST_ARGV="python3 ..."`를 직접 넣은 뒤 `write_meta()`만 부른다. 임시 fixture에서 production 줄을 `LAST_ARGV="FORGED-BY-MUTANT"`로 바꿔도 `test_d9_10...`은 `1 passed`였다.

최소 조건: argv를 JSON 배열(경계 보존)로 만들어 sidecar에 넣고, 회귀는 실제 `run()`에 shim producer를 넘겨 산출·meta를 만든 뒤 그 배열을 대조한다. 위 결속 삭제 변이가 RED여야 한다.

## E5 — P2 · package digest 집행 삭제 변이가 P2-2 회귀를 통과한다

자리:

- digest: R7 `replay_codex_r7.py:55-65`, R9 `replay_codex_r9.py:50-59`
- R9의 P2-2 adapted 증거: `replay_codex_r9.py:210-231`; 실제 mismatch 대신 source에 문자열 두 개가 있는지만 본다.

임시 fixture에서 R7 `package_digest()`를 `return True, status`로 바꾸자 `test_d9_08...`이 `1 passed`였다. 그 뒤 checksum 목록의 MD 파일을 실제로 손상시켰다. 결과 JSON은 해당 파일을 `mismatch`라고 쓰면서도 `package_digest_ok:true`, `closed:true`, runner rc 0이었다.

현재 production 구현은 정상이다. 발견은 그 집행의 회귀 증거가 공허하다는 것이다.

최소 조건: test가 checksum 대상 byte를 실제로 바꾸고 runner rc 비영·probe 미실행을 확인한다. runner 자체와 checksum manifest도 대상 commit/tree identity에 포함한다.

## E6 — P2 · P2-5의 “wrapper가 status로 가른다”는 실행 경로가 없다

자리: `tests/test_r9_codex.py:305-315`, `reviews/r9_repros/replay_codex_r9.py:181-194,370-374`.

named 회귀와 adapted probe는 `ne_shape.main()`을 직접 부르고 meta/status와 문서 문구만 확인한다. production shell scripts에는 `ne_shape`의 rc 1/3 또는 meta `status`를 소비하는 wrapper가 0개다. 그럼에도 회귀는 `1 passed`이고 replay는 P2-5 closed로 기록한다.

`ne_shape.py` 자체의 typed producer 계약(complete=0, none=1, partial=3)과 canonical 보호는 확인됐다. 닫히지 않은 것은 요청문이 추가 주장한 **caller/wrapper 소비**다.

최소 조건: 실제 호출자를 추가해 typed status를 분기하고 그 production path를 회귀에서 실행하거나, wrapper가 없다는 범위로 주장을 축소한다. 문서 문자열 검사는 wrapper 증거가 아니다.

## R9 P2 조건별 판정

| 조건 | 판정 | 근거 |
|---|---|---|
| P2-1 probe 명부 | 닫힘 | 빈/오타/중복/혼합 unknown 거부와 요청 key 일치는 실제 코드 경로가 강제한다. |
| P2-2 target/dirtiness/package | **부분** | 정상 mismatch는 막지만 status error가 fail-open이고, HEAD+porcelain이 실행 bytes를 봉인하지 않으며 package 집행 회귀도 살아남는다. |
| P2-3 mutation rc 분류 | 좁은 조건은 닫힘 | `classify()`의 rc 1/2/3/4/5 구분은 맞다. 다만 closure runner 자체가 E1로 허위 성공 가능하다. |
| P2-4 sidecar roster/argv | **부분** | roster는 본문 snapshot에서 유도한다. argv는 `$*`로 경계를 잃고 production 결속 삭제 변이가 회귀를 통과한다. |
| P2-5 typed none/partial | **부분** | producer/meta/canonical 규칙은 닫혔다. 주장한 wrapper 소비는 존재하지도, 실행되지도 않는다. |

## dirty 개발 모드 질문

`--allow-dirty`를 개발용으로 유지할 수는 있으나, 같은 JSON에 `closed:true`와 rc 0을 내면 자동 소비자가 이를 증거로 오인한다. 최소한 `evidence_eligible:false`를 구조적으로 계산하고 evidence 출력/승격기는 이를 거부해야 한다. 더 단순한 안전 규칙은 dirty 실행은 결과를 진단용으로 출력하되 항상 비영 종료하는 것이다.

## 재현물

- `outputs/r10_evidence_repros.py`
- `outputs/r10_evidence_results.json`

전체 재생:

```bash
python outputs/r10_evidence_repros.py \
  --target work/harness-r10-target-wsl/bms-balancing --case all
```

최종 확인: 대상 HEAD는 `bd6ba4749a92f8d441b4d9176eb876bfc6cc287c`, 대상 `git status --short -- .`는 빈 값이다.
