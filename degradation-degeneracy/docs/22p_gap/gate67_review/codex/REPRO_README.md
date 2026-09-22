# Gate67 재현·증거 읽기

대상은 `cdc49e91af15b2ef968753110cfae3bbe7ab5c2f`로 고정한다. 기존 사용자 checkout을 reset하지 말고 별도 checkout을 사용한다. 이 자료는 리뷰 결과이며 production 변경이나 과학 실행 승인문이 아니다.

## 요구 사항

Python 3.12 계열, 대상 저장소의 개발/시험 의존성과 `pytest`, `pytest-json-report`. 검토자는 Windows/Python 3.12.14를 사용했다. Linux native 전제는 Windows 보충 결과로 대체하지 않는다. venv·시험 sandbox·결과 파일을 만들므로 여유 공간이 필요하다. COMSOL·외부 계정·관리자 권한은 필요하지 않다.

`--repo`는 저장소 root가 아니라 **degradation-degeneracy/**를 가리킨다. `--out`은 아직 없는 새 디렉터리여야 한다. 아래의 `<...>`는 실제 경로로 치환한다. 원래 output 폴더를 재사용하거나 지우지 않는다.

```powershell
git -C <별도checkout> rev-parse HEAD
# 반드시 cdc49e91af15b2ef968753110cfae3bbe7ab5c2f

python .\repro_boundaries.py --repo <별도checkout>\degradation-degeneracy --out <새경로>\boundaries
python .\repro_premise_no_execution.py --repo <별도checkout>\degradation-degeneracy --out <새경로>\premise
```

Linux에서는 경로 구분자를 `/`로 쓴다. 스크립트에는 venv Python 경로의 Windows/POSIX 구분이 있다. Linux에서 같은 결과를 이 리뷰어가 이미 실측했다는 뜻은 아니다.

### 결과 해석

`repro_boundaries.py`의 `summary.json`:

- `namespace_explicit_off`: honest `entry=ACCEPTED`, **`forged_actual_entry=ACCEPTED`가 현 결함**. 최소 수정 뒤 기대값은 REJECTED.
- `namespace_explicit_on`: honest ACCEPTED, forged REJECTED. 대조군.
- `zip_package_remove_path`: complete ACCEPTED, **entry REJECTED가 현 결함**. 최소 수정 뒤 기대값은 ACCEPTED.
- `zip_package_plain`, `zip_module_remove_path`: entry ACCEPTED. 대조군.

namespace 위조는 reviewer가 `_observed_receipt` 반환을 복사/변경해 실제 검증 함수에 주는 fault injection이다. fresh helper/context 검사를 생략하지 않는다. 전체 coverage 위조나 process 권한 취득을 주장하지 않는다.

boundary 스크립트 끝에도 전제 시험의 탐색용 두 사례가 있다. 최종 T1 증거는 **`repro_premise_no_execution.py`**를 사용한다. 이것은 기존 두 parameter 자체를 바꾸지 않고 부모 env만 바꾼다.

`repro_premise_no_execution.py`의 `observations.json`:

- usage_error 두 사례: child rc4, stdout 빈 문자열인데 `committed_test_returned_normally=true`.
- collect_only 두 사례: JSON `total=0`, `call_phase_count=0`인데 같은 true.
- 수정 뒤에는 둘 다 PASS로 인정되지 않아야 한다. script 자체 rc0은 **관측 완료**일 뿐 product 통과 판정이 아니다.

## 기존 Gate66 반례 재실행

`repro_startup_gate66.py`는 이전 검토자의 스크립트를 바이트 그대로 복사한 것이다.

```powershell
python .\repro_startup_gate66.py --repo <별도checkout>\degradation-degeneracy --out <새경로>\old-startup --full-sandbox --case plain --case cwd_only_candidate --case cwd_on_pythonpath --case remove_loaded_path --case reorder_loaded_path
```

이번 고정 HEAD에서 다섯 경우 모두 complete/comparison/entry ACCEPTED였다.

## 시험과 변이

원래 명령은 대상 degradation-degeneracy에서 실행한다.

```text
python docs/22p_gap/mutation_replay.py --check-preimages
python docs/22p_gap/mutation_replay.py -k g66 --keep-sandbox
```

이번 Windows에서 후자는 conftest의 Linux mount 경계 때문에 scenario3/ran0이었다. 해당 실패 원자료도 포함했다.

보충 확인 전용:

```powershell
python .\partial_mutations.py --repo <별도checkout>\degradation-degeneracy --out <새경로>\partial-mutations
```

이는 실제 등록 old/new/EXPECT를 가져오되 `--noconftest`로 시험하는 reviewer 도구다. 공식 runner/coverage 파일로 위장하지 않는다. gate63의 fcntl import 때문에 F3 기대 시험 둘 중 하나를 제외한 한계가 있다. 기대 node 일치·실패 phase·witness를 각각 보고하므로 rc1만으로 kill이라고 판정하지 않는다.

`run_checks.py`, `audit_identity.py`, `finalize_package.py`는 검토 PC의 고정 디렉터리 배치를 기록한 도구다. 다른 PC에서 그대로 실행하는 범용 CLI가 아니다. 주요 반례 CLI 두 개와 보충 mutation CLI에는 `--repo/--out`이 있다. 기록된 command JSON을 다른 PC 경로에 맞춰 재현하되, 기존 증거를 덮어쓰지 않는다.

## 패키지 내용과 미포함

- `GATE67_REVIEW_KO.md`: 판정, 파일:줄, 최소 조건, 질문5개 답변, 실행 범위.
- `CLAUDE_REPLY.md`: 작성자에게 그대로 전달할 요약 회신.
- `TARGET_IDENTITY.json`, `FINAL_CHECK.json`: 검토 대상 식별/최종 불변 확인.
- `boundary-cases/`, `premise-no-execution/`: 새 반례 원자료.
- `old-startup/`: 원래 반례 재실행 원자료.
- `partial-mutations-final/`: 최종 보충 실행. 다른 partial-mutations 폴더는 앞선 환경 실패 기록.
- `.stdout.bin/.stderr.bin`, pytest XML/JSON: 출력 원자료. `.bin`은 원문 보존을 위한 확장자다. dedicated premise 스크립트의 두 출력 파일은 text=True 결과를 UTF-8 재직렬화한 것으로, 별도의 raw OS byte 캡처라고 하지 않는다.
- `registry-audit.json`: 현재 delta와 이전 삭제 감사 재사용 범위.
- `REVIEW_MANIFEST.json`: 포함 payload 경로·크기·SHA. 그 자체는 인증 서명이나 독립 실행 증명이 아니다.

별도 checkout/venv/pytest temp/전체 mutation sandbox/과학 results/COMSOL 파일은 포함하지 않는다. 역사적 삭제 파일 본문 전체를 이번에 다시 읽었다고 주장하지 않는다. 원자료의 로컬 절대경로는 reviewer 실행 문맥이며 수신 PC에 그 경로가 있다는 뜻이 아니다.

**수신 후** ZIP 전체 SHA를 별도 생성 영수증과 대조하고, manifest 정확집합·크기·SHA·CRC를 확인할 수 있다. 생성 측 검증은 수신 측 검증과 다르며 receipt의 recipient_verification은 null로 남긴다.
