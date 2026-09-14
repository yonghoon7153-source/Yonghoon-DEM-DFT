# R14 종결 확인 재현

대상은 `3aca0906dcf0e8690ab534f0bef3abf6a02cdb9a`의 bms-balancing이다. 원자료 fitting·COMSOL·동적 우회/변이는 실행하지 않는다. 원본 산출은 읽고, 일반 유효성 검사에 필요한 사본만 새 임시 디렉터리에 만든다.

다른 기계에서는 아래 target과 전달 묶음 경로를 바꾼다. 검토 환경은 WSL Ubuntu, Python3.12.3이며 필요한 프로젝트 의존성이 있는 기존 환경을 사용했다.

```bash
R14_TARGET=/mnt/c/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r14-close-3aca090-wsl/bms-balancing
R14_REVIEW=/mnt/c/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs
export PATH=/home/yonghoon71/ddvenv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
export PYTHONPATH=/mnt/c/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r2-pydeps
export PYTHONDONTWRITEBYTECODE=1
cd "$R14_TARGET"
python -m pytest tests/test_r14_codex.py -q -p no:cacheprovider
python -m pytest tests/test_r13_codex.py::test_g09_required_env_axes_are_checked_without_a_baseline tests/test_r13_codex.py::test_g29_a_baseline_without_env_is_uncomparable_not_a_contract_violation -q -p no:cacheprovider
```

관측은 각각7 passed(57.57s), 2 passed(1.87s). 286전수는 이번에 실행하지 않았다. JUnit 두 파일을 동봉한다.

```bash
python -B "$R14_REVIEW/r14_env_value_checks_f21cb648.py" "$R14_TARGET" "$R14_REVIEW/r14_env_values_3aca_repeat.json"
python -B "$R14_REVIEW/r14_close_checks.py" --target "$R14_TARGET" --output "$R14_REVIEW/r14_3aca_cli_repeat"
```

첫 스크립트 이름은 원래 f21 잔여 검토 당시의 이름이다. target 인자로 새 커밋을 전달했으며, 원래 다섯 대조군을 그대로 재사용한다. 정상 env.scipy0, 빈문자열/null/공백/탭줄바꿈2여야 한다. 파일의 원본·과학 본문은 불변이다. 출력 위치는 매번 새 이름으로 지정한다.

두 번째는 현행 schema0, legacy schema2(40·25·6·1), legacy 대조4(unknown17+1)를 기록한다. 자식 returncode와 stdout/stderr를 따로 보존한다.

보고서의 링크는 검토 PC의 절대 경로다. 다른 기계에서는 같은 commit의 대응 경로·줄을 사용한다. 포장 manifest는 바이트 무결성용이며 별도의 실행 인증서가 아니다.
