# R7 독립 검토 — 재생 증거·변이 감사·precision/Q3

대상: `521be85e74acef80feec45bd147dd339e25b8d0a`, `work/harness-r7-target/bms-balancing`.
요청문 `R7_REQUEST (1).md`와 저장소 정본을 먼저 읽었다. 이 검토는 수치 하네스의 검증 증거에 한정한다. MATLAB 원본 실행이나 private 입력을 독립 재현했다는 뜻이 아니다.

## 요약

현재 등록된 변이에 대한 **8/8·5/5 관측은 재현됐다**. 올바른 과거 baseline을 지정하면 적응판도 6/6 통과한다. precision/Q3 선택 회귀는 9개 통과했고, 그 축의 production 재개방 반례는 찾지 못했다.

새 확인 사항은 재생 명령의 기본 baseline 처리와 변이 감사의 종료 코드 두 건(P2)이다. 둘 다 현재 수정의 production 실패를 입증하는 것은 아니다. 단일 c6_01 시험의 주입 실행 보장도 약하지만, 적응판의 별도 양성 관측이 이를 보완하므로 묶음 증거 전체가 공허하다고 판정하지 않는다.

## 재현 방법 및 실행 범위

```bash
/home/yonghoon71/ddvenv/bin/python outputs/harness_r7_port_repros.py \
  --output outputs/harness_r7_port_results.json
```

스크립트는 SHA를 확인한 뒤 현재 소스의 별도 임시 사본에서만 변이한다. 임시 사본은 content snapshot을 git commit한 것이므로 사본 HEAD는 원래 HEAD와 다르며, 결과 JSON의 `source_head`가 리뷰 대상을 고정한다. shared target은 편집하지 않았다. 변이별 원문 pytest 출력과 적응판 probe 출력은 JSON에 저장돼 있다.

| 실행 | 실제 관측 | 해석 |
| --- | --- | --- |
| 적응판, `R6_OLD_OUT` 미지정 | rc 1, 5/6 닫힘 | inference probe가 잘못된 old baseline을 읽음 |
| 적응판, 올바른 `R6_OLD_OUT` 지정 | rc 0, 6/6 닫힘 | baseline을 갖춘 주장 재현 |
| 자체 변이 감사 | baseline 7 통과 → 8/8 CAUGHT → restored 7 통과, rc 0 | 각 mutant pytest는 rc 1; collection/setup 오류 아님 |
| 적응판 변이 감사 | baseline 6/6 → 5/5 CAUGHT → restored 6/6, rc 0 | 불일치 수치·소비 bytes·해시 축의 실제 실패 |
| 의도적으로 안 잡히는 후보를 준 감사 음성 대조 | `MISSED: 1`, **rc 0** | 감사 종료 코드 결함 |
| c6_01 주입을 끈 시험 음성 대조 | rc 0, 1 passed | 단일 회귀가 주입 발생을 강제하지 않음 |
| Q3 및 precision 선택 회귀 | rc 0, 9 passed | 기존 수정 유지 |

올바른 baseline은 `work/harness-r6-baseline-bfc-parent/bms-balancing/out`이었다. 실행 환경은 WSL Python 3.12의 기존 ddvenv 및 기존 pytest dependencies다. 표의 rc는 child 실행의 rc이며, 전체 재현 스크립트 rc 0은 그 기대 관측을 모두 확인했다는 뜻이다.

## P2-1 — 문서의 기본 적응판 명령이 과거 baseline을 현재 디렉터리로 착각한다

위치: `reviews/r6_repros/codex/replay_codex_r6_adapted.py:222`, `:227`.

상태·호출:

```bash
env -u R6_OLD_OUT python3 reviews/r6_repros/codex/replay_codex_r6_adapted.py --target .
```

`Path(os.environ.get("R6_OLD_OUT", ""))`는 env가 없을 때 `Path('.')`다. 현재 디렉터리는 존재하므로 `baseline.is_dir()`가 참이고, 의도한 derived-only 분기가 아니라 `--old .`로 full inference 검증을 부른다.

실제: 5/6, rc 1. `R6-04 inference`에 `assert old_m is not None` 실패가 기록된다. 같은 사본·같은 입력에서 `R6_OLD_OUT`을 올바른 과거 out으로 지정하면 6/6, rc 0이다. 따라서 기본 실행 실패를 R6-04 production 재개방으로 세면 안 된다.

최소 수정 조건: env 문자열이 비어 있는지 먼저 검사하고, full 재생에는 실제 baseline과 식별 정보를 명시적으로 요구할 것. baseline 없는 부분 재생을 지원한다면 의도적으로 derived-only를 선택하고 full 6/6과 구분할 것. 요청문에 baseline 설정 방법을 넣을 것.

## P2-2 — 변이 감사가 놓친 변이를 보고해도 성공 종료한다

위치: `reviews/r6_repros/codex_r6_mutation_audit.py:42`, `:48`–`:49`.

격리된 사본에서 변이 목록을 Q3 한 후보로 줄이고 치환 후 문자열을 원문과 같게 했다. 이는 현재 등록부에 그런 후보가 있다는 주장이 아니라, 감사기의 **안 잡힘 처리**를 시험하는 의도적인 음성 대조다. 원래 감사 실행·복원·집계·종료 흐름은 그대로 사용했다.

실제 원문:

```text
baseline: 0 7 passed, 45 deselected
MISSED | Q3 ... | c6_q3 | 1 passed, 51 deselected
restored: 0 7 passed, 45 deselected
MISSED: 1
```

프로세스 rc는 **0**이었다. 코드가 `bad`와 복원 후 rc를 출력만 하고 실패 종료하지 않기 때문이다. 따라서 이 명령을 종료 코드로 검사하는 실행자는 변이가 빠졌어도 성공으로 받을 수 있다. 현재 실제 8개 후보는 모두 실패시켰으므로 현재 8/8 관측을 취소하는 발견은 아니다.

최소 수정 조건: `bad != 0` 또는 복원 후 시험 실패면 비영 종료. 추가로 `rc != 0`만 CAUGHT로 인정하지 말고 collection/setup 실패와 선택한 시험의 assertion 실패를 구분하면 축별 증거의 의미가 강해진다. 이번 실제 8개 실행에는 collection/setup 실패가 없었다.

## 보조 관측 — 단일 회귀의 축과 묶음 증거를 구분해야 한다

### c6_01 주입이 사라져도 개별 시험은 통과

위치: `tests/test_r6_internal.py:1004`.

`assert {"attempt-A", "attempt-B"} & seen`은 두 결과가 모두 나왔음을 강제하지 않는다. 사본에서 `_hook_open`의 이벤트 발생만 꺼도 `-k c6_01`이 1 passed다. 따라서 "훅이 실제로 두 결과를 다 만들었다"는 주석보다 시험의 실행 보장이 약하다.

단, 적응판 `replay_codex_r6_adapted.py:57`, `:87`, `:117`은 `switched`/`published`를 명시적으로 검사한다. 실제 적응판 변이도 A/B 수치 불일치를 잡았다. 이 때문에 이 약점만으로 R6-01 수정 전체가 미검증이라고 할 수 없다. 최소 보강은 각 schedule에서 훅 실행 횟수·의도한 관측을 assert하고, 두 ID 모두 필요하다면 교집합 대신 포함 관계를 검사하는 것이다.

### 자체 감사 c6_04의 CAUGHT는 과거 데이터 소비가 아니라 정본 누락이다

해당 mutant는 canonical 파일을 제외하고 `_v2`를 yield한다. `load_degeneracy()`의 파일명 정규식(`scripts/compare_states.py:63`)이 그 `_v2` 이름을 처리하지 못해 `got["100"]`가 없어지고 `KeyError`로 시험이 실패했다. 정본 보존이라는 중요한 결과는 감시하지만, **이 한 mutant 출력**을 "옛 v2 값을 실제 소비했고 그 값 차이를 잡았다"고 설명하면 과장이다. 이 실행은 pytest rc 1이며 collection 오류는 아니다. 별도 inference/derived 재생은 올바른 baseline으로 통과했다.

## Q3 및 precision 결론

`FINDINGS.md:442`의 "옵션이 선언은 못 흡수하는 차이를 흡수한 셀이 있을 때만 partial(3)"는 현재 회귀와 맞는다. 동일 값은 conflict만 있어도 complete, `.125`와 `.126`을 느슨한 옵션이 흡수하는 경우는 partial이라는 조건을 검사했다.

선택한 `c6_q3` 및 `i6v_01/02/03/04/06/07`는 9 passed였다. 과거 `.2g` zero fixture도 다시 실행했으며 CSV 0 vs Python 0.049는 `model_mismatch=1`로 거부됐다. 이 범위에서 새로운 수치 통과 반례는 확인하지 못했다. 이전 1e308 helper stress는 실제 RMSE 경로 도달이 입증되지 않았으므로 재발견으로 포함하지 않았다.

## 담당 범위의 판정

R6-01/02/03의 적응 증거와 Q3/precision 수정은 이 범위에서 유지된다. 위 P2 두 건은 재현성·자동 검증 인터페이스 보강 조건이다. 이를 새로운 production 결함이나 전체 모델 근거의 단독 NO-GO 이유로 부풀리지 않는다. 전체 GO/NO-GO는 다른 담당의 실제 소비 경로·입력 snapshot 검토와 합쳐 판단해야 한다.
