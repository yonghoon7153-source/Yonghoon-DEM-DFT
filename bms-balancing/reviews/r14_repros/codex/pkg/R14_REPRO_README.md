# R14 리뷰 재현 안내

대상: `1bb45b358db4850c73e185d5f851e35fbcff9ad6`의 `bms-balancing/`.
주 보고서: `HARNESS_R14_1BB45B35_CODEX_REVIEW.md`.

이 묶음은 정상 과학 데이터·메타데이터 검증과 보관 파일 읽기를 수행한다. 보안 실행 우회 재생, 변이, 원자료 fitting, COMSOL 실행은 포함하지 않는다. 대상 코드·원본 out은 변경하지 않는다. 검사에 쓰는 사본과 결과만 별도 위치에 만든다.

## 실행 환경과 경로

검토 환경은 WSL Ubuntu, Python3.12.3이다. 기존 가상환경과 pytest 보조 경로를 사용했다. 다른 기계는 같은 의존성 환경을 준비하고 다음 두 경로를 해당 checkout 및 이 묶음의 위치로 바꾼다. 기존 작업트리를 덮어쓰지 않는다.

```bash
R14_TARGET=/mnt/c/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r14-target-wsl/bms-balancing
R14_REVIEW=/mnt/c/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs
export PATH=/home/yonghoon71/ddvenv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
export PYTHONPATH=/mnt/c/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r2-pydeps
export PYTHONDONTWRITEBYTECODE=1
```

## 1. 정상 CLI 결과

매번 새로운 output 디렉터리를 지정한다. 스크립트는 대상 HEAD·clean 상태를 확인하고 각 자식의 rc/stdout/stderr/PROMOTION을 저장한다.

```bash
python -B "$R14_REVIEW/r14_run_checks.py" --target "$R14_TARGET" --output "$R14_REVIEW/r14_cli_repeat"
```

기대 관측: 현행 schema0, legacy schema2, 현행 대 legacy4, 현행 대 현재HEAD2(alias13), 현행 대 승격직전4. 후자의 old full SHA는 `42314198e0beee59834d394cdba2757183503b59`이다. `compare_states.py out`은 rc0.

## 2. 정상 출력 경로 분류

```bash
python -B "$R14_REVIEW/r14_nested_output_check.py" --target "$R14_TARGET" --output "$R14_REVIEW/r14_nested_repeat"
```

새 합성 Git 저장소 3개를 만든다. 얕은 out은 clean, 정상 중첩 out만 있는 경우에는 잘못된 dirty를 관찰한다. 출력 밖 sibling 대조군은 dirty여야 한다. 스크립트 rc0은 검사를 마쳤다는 뜻이며, 각 case의 expected/observed를 읽어야 한다. 결과 fixture를 기존 저장소에 만들지 않는다.

## 3. 환경 기록의 완전성

```bash
python -B "$R14_REVIEW/r14_env_schema_checks.py" --target "$R14_TARGET" --output "$R14_REVIEW/r14_env_repeat.json"
```

네 종류의 완전한 sidecar, python만 남긴 sidecar, env 전체 부재를 비교한다. 관측은 각각0/0/2. 과학 본문 bytes·원본 sidecar는 불변이고, schema-only이므로 모두 승격 자격은 false다. 일반 입력 유효성 검사이며 실제 승격 성공을 재현한 것이 아니다.

## 4. 옛/새 보관 자료 읽기

```bash
python -B "$R14_REVIEW/harness_r14_archive_audit.py" "$R14_TARGET"
```

대상 코드를 import하지 않고 AST의 literal schema, CSV/JSON, Git blob을 읽는다. 옛26/26 bytes 동일, 새13개 hash/명부/행 참조, 공통 숫자5184개 차이0이 확인값이다. 원자료에서 다시 계산한 증거가 아니다.

## 5. 선택 회귀

```bash
cd "$R14_TARGET"
python -m pytest tests/ -q -p no:cacheprovider -k 'not d10_12 and not d10_13 and not d10_14 and not e11_09 and not e11_10 and not e11_17 and not e11_18 and not d8_07 and not d9_08 and not d7_05'
```

실측: **267 passed, 10 deselected in242.46s**. 제외 항목을 통과·실패로 바꾸어 세지 않는다. 과거 재생 러너·변이 감사와 동시에 실행하지 않았다.

`matlab/tests/run_all.sh`는 이 기계에서 Octave가 없어1~3단계를 건너뛰고 Python4·5단계만 통과했다. wrapper rc0을 Octave/MATLAB 전수 통과로 해석하지 않는다.

## 보관 결과

- `r14_cli_checks/`: 자식 CLI 원문과 집계.
- `r14_nested_output_checks/results.json`: 정상 경로 세 case의 관측.
- `r14_env_schema_results.json`: 12개 환경 기록 대조의 명령·원문·불변 검사.
- `R14_selected_pytest.xml`: 선택 회귀 결과.
- `R14_VALIDATION_RESULTS.json`: 이번 검토의 요약. 독립 실행 인증서가 아니라 관측 결과를 정리한 기록이다.

보고서의 링크는 이 리뷰 PC의 절대 경로다. 다른 기계에서는 같은 대상 commit의 대응 파일·줄을 확인하면 된다.
