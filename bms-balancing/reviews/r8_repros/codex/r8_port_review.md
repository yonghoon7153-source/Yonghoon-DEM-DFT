# R8 독립 검토 — 재생·변이 증거·partial 판정

## 대상과 범위

- 정본 SHA: `a22da3380338f97b8eed2f600ffefad1e398c6c3`.
- 실행 checkout: `work/harness-r8-target-wsl/bms-balancing`. 원래 Windows linked worktree는 WSL Git이 absolute gitdir를 해석하지 못해, 같은 SHA의 WSL-native checkout으로 전환했다. 그 환경 문제는 발견으로 세지 않는다.
- `reviews/R8_REQUEST.md`를 전체 읽고, R6 원본/적응 변이 감사, R7 port 패키지와 회귀, precision Q3를 검토했다.
- 변이는 전부 별도 임시 사본에서 실행했다. 사본은 내용 snapshot을 별도 git commit했으므로 사본 HEAD와 원래 source SHA를 구분한다. 원래 target은 수정하지 않았다.
- MATLAB 원본·private xlsx의 독립 포팅 일치를 측정한 검토는 아니다. 전체 pytest 및 MATLAB run_all의 결과는 다른 담당과 합쳐야 한다.

재현물: `outputs/r8_port_repros.py`, 원문 출력: `outputs/r8_port_results.json`. 각 source 파일 SHA256 및 reviewer script SHA256도 JSON에 기록된다.

```bash
/home/yonghoon71/ddvenv/bin/python outputs/r8_port_repros.py \
  --output outputs/r8_port_results.json
```

## 요약 판정

R7-05의 baseline 기본값 오류와 R7-06의 실제 MISSED 종료 코드 오류는 **닫혔다**. baseline 없으면 rc 0이지만 JSON에 `부분`/5개 닫힘+1개 부분으로 명확히 구분하며 full 6/6이라고 하지 않는다. 올바른 baseline을 주면 full 6/6이다. 개별 no-op을 실제 시험으로 실행하면 이제 MISSED·rc 1이다.

현재 등록된 8개 자체 변이와 5개 적응판 변이는 모두 잡혔다. 그러나 “미실행도 CAUGHT”, “R7 probe가 자기 반례 assertion까지 갔다”, “c6_04가 이제 값으로 잡힌다”는 증거 경계에는 아래 보강이 필요하다. **새로운 production 수치 결함으로 세는 발견은 없으며**, 증거·재현성 P2와 이전 지적의 폐쇄 실패를 분리한다.

| 검사 | 실제 관측 | 판정 |
| --- | --- | --- |
| 선택 회귀 c6_01/c6_04/c6_q3/d7_05/d7_06 | `5 passed, 54 deselected`, rc 0 | 기존 기본동작 통과 |
| 적응판, baseline 미지정 | 5 닫힘 + 1 부분, `mode: 부분 …`, rc 0 | R7-05 폐쇄 |
| 적응판, 과거 baseline 지정 | 6 닫힘, `mode: full`, rc 0 | full 주장 재현 |
| 자체 등록 변이 | baseline 7 통과 → 8 CAUGHT → restored 7 통과, rc 0 | 관측 수 재현; c6_04는 아래 한정 |
| 적응판 등록 변이 | baseline 6 닫힘 → 5 CAUGHT → restored 6 닫힘, rc 0 | 각 숫자/해시 축에서 실제 실패 |
| 실제 선택 시험 + 무해한 주석 변이 | MISSED 1, rc 1 | R7-06 폐쇄 |
| 미존재 선택 시험 + 같은 주석 변이 | 52 deselected, CAUGHT, MISSED 0, rc 0 | 새 감사 false-success |
| c6_01 주입 전부 OFF | `AssertionError: {'attempt-A'}`, rc 1 | 이전 전체 OFF 지적 폐쇄 |
| c6_01 metadata 주입 두 축만 OFF | 1 passed, rc 0 | 개별 schedule 보장 불충분 |
| 요청문 그대로 R7 port controls 명령 | SHA guard AssertionError, rc 1 | 반례 본문 미실행 |

과거 baseline은 `work/harness-r6-baseline-bfc-parent/bms-balancing/out`이다. raw JSON에 child별 명령·cwd·rc·stdout·stderr가 있다. 전체 재현 스크립트 rc 0은 예상한 정상/오류 관측을 모두 확인했다는 뜻이며, 모든 child가 성공했다는 뜻이 아니다.

## P2-E1 — 시험 0개 실행을 `CAUGHT`·성공 종료로 인증한다

위치: `reviews/r6_repros/codex_r6_mutation_audit.py:58`.

원인은 `ok = rc_m != 0`이다. pytest의 “선택된 시험 없음” rc 5도 assertion 실패와 같은 CAUGHT다.

재현은 임시 사본에서 현재 auditor의 `main()`과 `run()`을 그대로 사용하되 등록부 한 후보만 다음으로 구성한다.

```python
old = 'MODES = ("LAM_PE", "LAM_NE", "LLI")'
new = old + '  # harmless audit control'
MUTATIONS = [("semantic no-op fixture", "c6_DOES_NOT_EXIST",
              "scripts/compare_states.py", old, new)]
```

실제:

```text
baseline: 0 7 passed, 45 deselected
CAUGHT | semantic no-op fixture | c6_DOES_NOT_EXIST | 52 deselected
restored: 0 7 passed, 45 deselected
MISSED: 0
process rc=0
```

같은 선택자를 직접 실행한 pytest는 rc 5였다. 대조군으로 같은 무해한 변이의 선택자를 `c6_04`로 바꾸면 1 passed → MISSED 1 → auditor rc 1이다. 따라서 semantic-no-op 자체를 잘 잡는다는 주장이 아니라, **실행되지 않은 것을 잡혔다고 기록하는 감사 경계**의 실제 반례다.

현재 등록된 8개에 해당 오타가 있었다는 뜻은 아니다. 실제 8개 모두 pytest rc 1이었다. 이번 반례는 추후 이름 변경·오타·잘못된 selector를 감사가 스스로 구분하지 못함을 보인다.

최소 수정 조건: 선택된 node ID와 실행 개수(0보다 큼)를 확인하고, rc 2/3/4/5 등의 실행/수집 실패를 CAUGHT가 아닌 감사 오류로 분류하여 비영 종료한다. mutant가 겨냥한 시험의 assertion 실패를 확인하는 회귀를 붙인다.

## P2-E2 — 요청문의 R7 port 재생은 반례 assertion 전에 멈춘다

위치: `reviews/r7_repros/codex/harness_r7_port_repros.py:23`, `:163`, `:172`; 주장 위치 `reviews/R8_REQUEST.md:37`, `:48`, `:52`.

요청문 그대로 R8 checkout에서 실행:

```bash
python3 reviews/r7_repros/codex/harness_r7_port_repros.py --target . --case controls
```

실제 첫 실패:

```text
assert head["returncode"] == 0 and head["stdout"].strip() == REV, head
AssertionError: ... 'returncode': 0,
  'stdout': 'a22da3380338f97b8eed2f600ffefad1e398c6c3\n' ...
```

`REV`가 여전히 `521be85e74acef80feec45bd147dd339e25b8d0a`다. Git 자체는 성공했고 기대 SHA만 다르다. 따라서 이 명령의 rc 1을 “R7-05·06 반례 assertion이 실패했으므로 닫힘”으로 읽을 수 없다. 또한 `--case controls`는 `adapted_runs()`를 실행하지 않으므로 baseline 기본값을 측정하는 R7-05까지 담당하는 명령이 아니다.

이는 수정 코드가 틀렸다는 뜻은 아니다. 현행 API를 호출한 독립 대조와 d7_05/d7_06은 통과했고 R7-05/06은 닫힘으로 인정한다. 문제는 요청문·보관한 replay 설명과 **배포한 명령으로 얻는 증거**가 다르다는 점이다.

최소 수정 조건: 원본 R7 pinned probe는 보존하고, R8용 명시적 adapter/closure runner를 제공한다. 대상 검증 뒤 실제 case에 도달했음을 기록하고 baseline와 audit control을 별도로 실행한다. “실행 불가”, “반례 미재현”, “positive closure 성립”을 분리해 결과와 요청문을 갱신한다.

## 폐쇄 실패 E3 — c6_04는 여전히 `KeyError`로 잡힌다

위치: `reviews/r6_repros/codex_r6_mutation_audit.py:36`–`:38`, `scripts/compare_states.py:69`, `tests/test_r6_internal.py:1144`; 주장 `reviews/R8_REQUEST.md:70`–`:71`.

현재 등록부를 그대로 돌려 얻은 c6_04 실패:

```text
> assert got["100"]["file"] == "degeneracy_100_Li.json" ...
E KeyError: '100'
1 failed, 51 deselected
```

mutant가 최고 `_vN`을 고르기는 하지만 `yield f`는 여전히 `_v2` 파일명이다. `f.rename(...) if False else f`는 이름을 바꾸지 않는다. downstream 정규식 `degeneracy_(.+)_([A-Za-z]+)$`은 `_v2`를 처리하지 않아 state 100 자체가 사라진다. `222.0`을 소비해 `111.0`과 달라서 실패하는 경로에 도달하지 않는다.

이것은 R7에서 이미 한정했던 증거 약점이므로 **새 production 발견으로 재계수하지 않는다**. 다만 R8의 “고쳐 값으로 잡힌다”는 폐쇄 주장은 현재 출력과 다르다. canonical 보존 변화는 감시하지만 과거 수치를 실제 소비한 변이 증거는 아니다.

최소 수정 조건: 과거 선택과 이름 해석을 함께 복원하는 multi-site mutant 또는 동등한 fixture로 정상 parser까지 도달시키고, stale 값 `222`(정상 `111`)를 실제로 관측한 후 수치 assertion이 독립적으로 실패하게 한다. matrix 축도 현대 schema/meta 거부에 가리지 않도록 적합한 legacy/valid fixture를 사용한다. 실패 원문을 보관한다.

## 보조 P2-E4 — c6_01의 개별 주입 카운터는 읽기 카운터다

위치: `tests/test_r6_internal.py:964`–`:966`, `:1017`, `:1028`.

R8은 전체 주입 OFF를 확실히 잡는다. 그러나 다음처럼 **metadata 경계 주입만** 끄면 여전히 1 passed다.

```python
if n["v"] == k and not target_name.endswith(".meta.json"):
    on_k()
```

이는 target source를 바꾼 production 반례가 아니라 시험 fixture에 대한 음성 대조다. `fired["v"]`는 callback이 아니라 읽기 수여서 `>= k`가 통과한다. data 경계의 다른 schedule들이 B/B와 미완을 제공해 metadata schedule의 무실행을 가린다.

최소 보강 조건: callback에서 별도의 publication count/flag를 세고 각 schedule에서 이를 assert한다. 다른 schedule의 합집합과 별도로 각 지점에서 실제 게시된 ID/예상 관측을 남긴다.

적응판은 `switched`/`published`를 명시적으로 검사하며 현재 등록 변이도 실제로 잡는다. 이 단일 시험 약점으로 R6-01 production 수정 전체를 재개방하거나 모든 경쟁순서 증거가 공허하다고 판정하지 않는다.

## 종합에 넘길 결론

R7-05/06 기본 수정과 Q3 정책은 유지되며 현재 등록 변이의 개수는 재현된다. E1/E2는 새 증거 도구·명령 경계, E3는 이전 지적의 폐쇄 실패, E4는 보조 시험 강도 한계다. 이 담당 범위에서 새 P1 수치 오류는 확인하지 못했다. 전체 GO/NO-GO는 실제 소비 경로·입력 snapshot 담당의 결과와 합치되, “모든 evidence claim까지 닫혔다”는 판정은 위 최소 조건 충족 전에는 뒷받침되지 않는다.
