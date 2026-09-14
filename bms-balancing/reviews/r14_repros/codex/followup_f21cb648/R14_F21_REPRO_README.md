# R14 f21cb648 후속 검토 재현

이 묶음은 정상 출력 경로·환경 메타데이터 유효성 검사와 보관 자료 읽기를 수행한다. 실제 fitting, COMSOL, 동적 우회·변이 재생은 포함하지 않는다. 원본 코드는 바꾸지 않으며, 사본과 결과만 별도 디렉터리에 만든다.

실행 환경: WSL Ubuntu, Python 3.12.3. 대상 HEAD는 `f21cb6480fc27857c7aac67e823cae62b1443830`이다. 아래 경로는 검토 PC 기준이며 다른 PC에서는 대응 checkout과 전달 묶음 위치로 바꾼다. 각 결과 경로는 새 이름을 사용한다.

```bash
R14_TARGET=/mnt/c/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r14-response-f21cb648-wsl/bms-balancing
R14_REVIEW=/mnt/c/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs
export PATH=/home/yonghoon71/ddvenv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
export PYTHONPATH=/mnt/c/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r2-pydeps
export PYTHONDONTWRITEBYTECODE=1
```

## CLI 대조

```bash
python -B "$R14_REVIEW/r14_followup_checks.py" --target "$R14_TARGET" --output "$R14_REVIEW/r14_f21_cli_repeat"
```

현행 schema0 / legacy schema2 / legacy 대조4 / HEAD 자기대조2(alias13) / full 승격 직전 대조4. 자식의 returncode와 원문을 별도로 기록한다.

## 이전 두 재현의 수정 확인

```bash
python -B "$R14_REVIEW/r14_nested_output_check.py" --target "$R14_TARGET" --output "$R14_REVIEW/r14_f21_nested_repeat"
python -B "$R14_REVIEW/r14_env_schema_checks.py" --target "$R14_TARGET" --output "$R14_REVIEW/r14_f21_env_repeat.json"
```

중첩 OUT만 있으면 clean, OUT 밖 sibling은 dirty이며 실제 파일명을 지목한다. 네 종류 sidecar의 완전 env / python-only / env 부재는 0 / 2 / 2다.

## 남은 공백 값 조건

```bash
python -B "$R14_REVIEW/r14_env_value_checks_f21cb648.py" "$R14_TARGET" "$R14_REVIEW/r14_f21_env_values_repeat.json"
```

matrix의 `env.scipy`만 사본에서 바꾼다. 정상 문자열0, 빈 문자열2, null2, 공백만0, 탭·줄바꿈만0을 관측했다. 마지막 둘의 기대값은 rc2다. 이 스크립트의 종료0은 기록 완료이며 모든 case가 옳다는 뜻이 아니다. `promotion_eligible`는 전부 false다. 원본과 과학 본문은 바뀌지 않는다.

## 선택 회귀

```bash
cd "$R14_TARGET"
python -m pytest tests/ -q -p no:cacheprovider -k 'not d10_12 and not d10_13 and not d10_14 and not e11_09 and not e11_10 and not e11_17 and not e11_18 and not d8_07 and not d9_08 and not d7_05'
```

실측 274 passed, 10 deselected, 296.40s, rc0. JUnit은 `R14_F21_selected_pytest.xml`이다. 동적 우회 재생 및 Octave 미실행을 전수 확인으로 바꾸어 적지 않는다.

보관 감사 스크립트 `r14_response_preservation_audit.py`의 인자는 차례대로 대상 bms-balancing 경로, 원래 R14_REQUEST.md 첨부 경로, 이전 HARNESS_R14_1BB45B35_REVIEW_PACKAGE.zip 경로다. 대상 저장소에 보존된 대응 원본들을 인자로 사용할 수도 있다. 이전 out Git blob과 현재52개 파일을 읽어 비교한다.

이 묶음의 manifest는 포장 무결성 기록이며 독립 실행 인증서가 아니다. 보고서 링크는 검토 PC의 절대 경로다.
