# ULPRI 표지 경계 수정 증거 (2026-10-24)

대상 변경은 `01c1aaf5be8acdf7d1716f34cc86fc77d8e27362` 위의 RESUME 근접 표지와 manifest 줄 구분자 처리다. 외부 판정은 정수 파싱 교정을 수용하고 `ULPRI-01/02`의 무결성 종결을 HOLD로 남겼다. 이 폴더는 **로컬 수정·합성 검증**이며 외부 GO나 실제 연구 계산 결과가 아니다.

후보 자리: `<<sha:Reject ambiguous unloading resume markers and separators>>`. root가 고정 코드 후보의 전체 게이트·보호 범위·최종 원격 핀과 ZIP을 따로 기록한다. [요청서](../codex_dem_unloading_ulpri_recheck_request_20261024.md)와 [한정](NOTE.md)을 함께 읽는다.

## 작성자 실행

| 증거 | 실제 결과 | 읽는 방법 |
| --- | --- | --- |
| `author/tests-first.json`·로그·소스 | R40 처음 34개: 10 통과/24 실패 | 기존 production에 시험을 먼저 넣은 결과 |
| `author/tests-first-raw-marker.json`·로그·소스 | 선행 구분자 8개 추가: 1차 수정 34/42 | `_csv.splitlines()` 앞단을 검사하지 않은 수정의 한계 보존 |
| `author/r40-fixed.json`·로그 | 최종 42/42 | 실제 arm CLI와 입력 바이트 보존을 복합 단언 |
| `author/kit-suite/summary.json`·13개 로그 | **13명령 전부 rc 0·실패 줄 0**. reader **346/346** | reader의 R39 90개·R40 42개는 346에 포함되며 합산하지 않음 |
| `author/cli/baseline-result.json` | 같은 43개 중 26 통과/17 실패 | 외부 두 우회 유형이 기준 소비자에서 남는 시험 먼저 증거 |
| `author/cli/final-result.json` | **43/43**. 정상 9개와 k=0/1/2/3 관측은 기준과 정확히 같음 | 기존 정상과 음성 34개를 구분; 입력 CSV/manifest/state 바이트 불변 |
| `author/mutants/report.json` | **5/5 표적 변이 검출** | raw 표지 검사 삭제, CSV 선행 줄 정규화, 표지 오류의 인증 배제 무력화, manifest 구분자 검사 삭제, 키 선별을 먼저 하는 회귀 |
| `author/mutants/portable-check.json` | portable snapshot 구성으로 변이 한 종 재현 | 위 5종과 별개 여섯 번째 변이라고 더하지 않음 |
| `author/source-scope.json` | 생산 AST 변경 두 함수, 덱 64·history 16·params 불변 | 기존 `_i`·`_csv`·`_resume_integer`·`_state_vars` AST도 불변 |

kit suite는 고정 scratch source에서 실행했다. 이후 README의 옛 “이번 수정에서 소수 파싱을 닫지 않았다” 한 줄만 10-23 당시 기록임을 명확히 했다. `author/doc-only-delta.json`이 그 차이를 기록한다. reader·seal·활성 규칙·등록문서는 suite 뒤 바뀌지 않았다. 최종 파일 목록은 `author/source-freeze.json`이다.

## 재현 도구

- `author/probe_marker_cli.py --repo <source> --out <new-output>`: 외부 반례를 포함한 43개 실제 arm CLI. 기존 출력 디렉터리를 재사용하지 않는다.
- `author/run_marker_suite.py --repo <source> --out <new-output>`: 이전 정수 수정 증거의 run_suite.py에서 **같은 13개 명령 목록**을 읽는다. 그 고정 의존 파일이 필요하며, 실제 원본 로그·rc·작업 파일 SHA를 남긴다.
- `author/mutate_markers.py --repo <source> --out <new-output>`: kit와 params가 선언한 r8 archive만 임시로 복사한 뒤 명시한 다섯 변이를 하나씩 적용한다. Git checkout이나 `.git`은 복사하지 않는다. `--only <name>`으로 한 변이만 재현할 수 있다.
- `author/mutate_markers.original-v2.py`: 다섯 변이를 최초 실행한 역사 도구다. 당시에는 이미 축소된 scratch source를 복사했다. 일반 checkout에서 실행하려면 위 portable 도구를 사용한다. 변이 목록과 실행하는 R40은 두 도구가 같다.

모든 출력은 합성 원자료의 판독 결과다. 독립 재검토의 추가 CLI·변이와 root의 전체 게이트는 각각 별도 영수증이며, 작성자 사례 수와 더하지 않는다. 공용 155개 검사에 kit 13명령/reader 자체시험이 자동 연결되어 있지 않다.
