# DEM 언로딩 — 재개 식별자 정수 파싱 외부 재검토

검토일: 2026-10-24 · 대상 가지: `codex/unloading-ulpr`

- 검토 핀: `01c1aaf5be8acdf7d1716f34cc86fc77d8e27362`
- 비교 기준: `8347d32ea678c0174bd77d4c79cfbd7b0591e4a3`
- 요청서: `docs/reviews/codex_dem_unloading_resume_integer_request_20261024.md`
- reader SHA-256: `7a395a549e8ad3eae820a9e575f094219ca7d47a4b9a07c5bc27623d7018af4b`
- 제출 ZIP SHA-256: `ca2925b6044b72a7c077058c0a3cfbd00595ccc01aaa75d86daa0111da73f393`
- 검토 방식: 고정 소스 읽기, 원자료 재계수, 실제 Python 함수·arm CLI 실행. LIGGGHTS·MPI·물리 시뮬레이션·실물 재개 없음. 생산 소스와 Git 상태 변경 없음.

## 1. 판정

**정수 반올림 결함의 교정은 수용한다. 그러나 요청서 Q2와 Q3의 넓은 “모호한 재개 증거가 섞이면 승인하지 않는다” 종결은 HOLD다. 새 P1은 없고, 그 주장에 직접 걸리는 P2 두 건을 재현했다.**

정확한 `RESUME` 표지가 붙은 k/step 및 상태 식별자에는 새 파서가 제대로 적용된다. 정상 k=0/1/2/3 모의 재개는 모두 `OK`, 주 값은 중단 없는 대조와 정확히 같다. 공용 숫자 파서·CSV 파서, 생산 덱 64개, history 16개, params의 변경도 발견하지 않았다.

남은 두 경로는 **정수 파서에 도달하기 전에 잘못된 기록이 다른 종류의 줄로 취급되어 사라지는 문제**다. 정상 인증 한 건 옆에 이런 기록을 추가하면, 오류 사유 없이 정상 인증을 유지하고 옛 행 5개를 분석에서 제외한 뒤 `primary_status=OK`, `rank_eligible=true`를 낸다. 입력 CSV 파일을 실제로 지우거나 고치지는 않는다.

두 반례 모두 비교 기준에서도 재현됐다. **이번 패치가 새로 만든 회귀가 아니며, 정상 생산 결과의 물리량이 틀렸다는 증거도 아니다.** 닫히지 않은 것은 재개 증거의 무결성 주장이다. 모든 악성 파일 문법을 방어하라는 요구로 확대하지 않는다. 아래의 RESUME 근접 표지와 요청서가 직접 지목한 Unicode 줄 구분자만 판정한다.

## 2. ULPRI-01 — RESUME 표지의 공백 변형이 정수 검사와 모호성 검사를 함께 우회

**심각도: P2 · 상태: 열림 · 영향: Q2, Q3의 재개 승인 무결성.**

소스: `docs/data/ps45_unload_20261009/ul_reader.py:169`, `:324`, `:327`.
[고정 핀의 read_run](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/01c1aaf5be8acdf7d1716f34cc86fc77d8e27362/docs/data/ps45_unload_20261009/ul_reader.py#L315), [인증 함수](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/01c1aaf5be8acdf7d1716f34cc86fc77d8e27362/docs/data/ps45_unload_20261009/ul_reader.py#L143).

현재 분기에는 정확한 문자열 동등성이 두 번 있다.

```python
index = _resume_integer if r['event'] == 'RESUME' else _i
# ...
if e['event'] != 'RESUME':
    continue
```

따라서 event 셀의 `RESUME ` 또는 `RESUME\u00a0`는 R39의 엄격한 정수 검사 대상이 아니다. k=`1.49`도 공용 `_i`로 1이 된다. 뒤의 인증 검사에서는 아예 RESUME가 아닌 사건으로 건너뛴다. `_csv`의 열 개수는 맞으므로 CSV 구조 오류도 발생하지 않는다.

### 실제 함수·CLI 반례

생산 덱의 제어 흐름을 이용한 합성 UT fixture를 만들고, 정상 인증 `(k=1, step=3310000)` 및 상태 파일을 유지했다. 실패했던 앞 시도의 k=2 이후 관측이 있어 정상 재개 시 분석에서 제외할 옛 행은 5개다. 여기에 정상 RESUME를 복사하되 k만 `1.49`로 바꾼 행을 추가했다.

| 추가 행의 event 셀 | k 셀 | resume_auth | 제외한 옛 행 | primary_status | rho_pct | rank_eligible |
| --- | ---: | --- | ---: | --- | ---: | --- |
| 없음 — 정상 대조 | — | `(1, 3310000)` | 5 | OK | 0.20260778734286913 | true |
| `RESUME` | 1.49 | 없음 | 0 | UNIDENTIFIED | null | false |
| `RESUME ` — 끝 ASCII 공백 | 1.49 | `(1, 3310000)` | 5 | OK | 0.20260778734286913 | true |
| `RESUME\u00a0` — 끝 NBSP | 1.49 | `(1, 3310000)` | 5 | OK | 0.20260778734286913 | true |
| 잘못된 행을 제거한 대조 | — | `(1, 3310000)` | 5 | OK | 0.20260778734286913 | true |

모든 행은 실제 `ul_reader.py arm` 진입점의 결과다. 반례의 `read_run.problems=[]`이고 입력 세 CSV의 SHA-256은 실행 전후 같다. 정상 대조와 literal `RESUME` 음성 대조를 함께 통과하므로, 실패 원인은 fixture가 아니라 **사건 표지 인식 단계**로 좁혀진다.

### 최소 해결

1. events의 event 셀을 숫자 변환 전에 검사한다. 특히 `RESUME`의 앞뒤 공백·비ASCII 공백 변형을 **정상 RESUME로 정규화해 수용하지 말고**, 잘못된 재개 표지로 오류 처리한다.
2. 그 오류가 있으면 다른 정상 RESUME만 남겨 인증하지 않는다. `resume_auth=[]`, 옛 행 제외 0, 주 값 UNIDENTIFIED/null을 유지한다.
3. 위 두 표지 변형을 실제 arm CLI 회귀로 추가하고, 정상 대조·CSV 바이트 불변도 함께 검사한다.

사건명 전체 허용목록을 도입할 수도 있지만 이번 최소 해제에 모든 관측 필드의 문법 개편이 필요한 것은 아니다. 임의의 `UNKNOWN` 사건 자체를 새 결함으로 세지는 않았다.

해결 증거: 현재 핀에는 없음. `evidence/boundary/result.json`의 `trailing_space_event`, `nbsp_event` 및 해당 원본 CSV·arm_verdict가 실패 증거다.

## 3. ULPRI-02 — 다른 문자열 뒤의 Unicode 줄 구분자가 잘못된 resume_from을 숨김

**심각도: P2 · 상태: 열림 · 영향: Q2의 manifest Unicode 줄 구분 거부, Q3의 승인 없음 보장.**

소스: `docs/data/ps45_unload_20261009/ul_reader.py:152–164`.
[고정 핀](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/01c1aaf5be8acdf7d1716f34cc86fc77d8e27362/docs/data/ps45_unload_20261009/ul_reader.py#L149).

`split('\n')`로 Unicode 줄 구분자를 정상 개행으로 정규화하지 않는 선택은 맞다. 그러나 그 뒤에는 현재 줄이 `resume_from=`으로 시작하는 경우만 검사한다. Unicode 줄 구분자가 **그 키 뒤**에 있거나 줄 맨 앞에 있는 기존 시험은 거부하지만, 키 앞에 다른 문자열이 있으면 줄 전체를 무관한 기록으로 버린다.

정상 manifest에 다음 바이트를 한 줄 추가했다. 아래 `\u2028`은 문자 여섯 개가 아니라 실제 U+2028 한 글자다.

```text
note=old\u2028resume_from=3310000.49\n
```

결과:

```text
resume_auth = [(1, 3310000)]
problems = []
n_superseded_rows = 5
primary_status = OK
rho_pct = 0.20260778734286913
rank_eligible = true
CSV SHA-256 = 실행 전후 동일
```

Q2는 manifest의 잘못된 `resume_from=`과 Unicode 줄 구분자가 승인 증거에서 사라지는지를 직접 묻는다. 이 반례에는 둘 다 들어 있고, 인증 경계와 동일한 step의 소수 변형이 사라진다. 따라서 “Unicode 줄 구분 우회가 닫혔다”는 설명은 현재 시험에 포함된 위치들에 한정해야 한다.

### 최소 해결

manifest의 줄을 키별로 버리기 **전에** 금지된 Unicode 줄 구분자를 검사하여 오류를 남긴다. U+2028을 LF로 바꾼 뒤 정상 줄처럼 읽는 처방은 피한다. 현재 허용하는 LF·CRLF·CR은 유지하고, U+0085/U+2028/U+2029 등 금지할 구분자는 명시한다. 정상 표지와 잘못된 표지가 공존해도 정상 것만 골라 인증하지 않는다.

회귀는 구분자가 키 뒤·맨 앞에 있는 경우뿐 아니라, 위처럼 **다른 텍스트와 잘못된 키 사이**에 있는 경우를 포함해야 한다. 실제 CLI에서 인증 없음·행 제외 0·UNIDENTIFIED/null·CSV 불변을 검사한다.

해결 증거: 현재 핀에는 없음. `evidence/boundary/unicode_embedded_manifest/`와 `result.json`에 입력 바이트와 실제 출력 보존.

## 4. 요청서 Q1–Q5 답

| 질문 | 판정 | 근거와 한계 |
| --- | --- | --- |
| Q1 정확한 정수 파싱 | **닫힘 — 표지가 정확히 인식된 경로** | Decimal은 원문을 받아 정수성을 확인한다. 앞의 float 검사는 유한성/범위 검사이며 정수값 대조에 반올림 결과를 쓰지 않는다. Fraction 독립 산술 오라클 514/514, resident R39 90/90. `9007199254740993`은 정확히 유지하고 `9007199254740992.0000000001`은 거부한다. |
| Q2 중복·모호 기록 공존 | **부분** | 같은 상태 식별자 중복, literal RESUME의 소수·비ASCII 숫자, 기존 위치의 잘못된 manifest·CSV 열 구조 결손은 거부한다. 그러나 ULPRI-01/02의 표지 인식 앞단에서 다른 정상 인증을 유지한다. |
| Q3 실제 arm 및 정상 재개 | **부분** | 정확한 RESUME 표지의 잘못된 경계는 실제 CLI에서 UNIDENTIFIED/null, CSV 불변. 정상 k=0/1/2/3 수치도 유지. 모든 모호 표지에 대한 보장은 두 반례 때문에 닫히지 않는다. |
| Q4 변경 범위·봉인 | **닫힘 — 이 핀의 바이트 비교 범위** | 94 kit 파일 중 변경 5개 + 밖의 사전등록 1개. `_i`/`_csv` AST 동일. 덱 64개는 두 핀 사이 불변이고 현재 생성 결과와도 바이트 동일. history 16개·params 불변. kit 봉인 76개·활성 24규칙·history 봉인 15개·증거 manifest 310개 불일치 0. |
| Q5 숫자·증거 지위 | **숫자 일치, 포괄적 거부 문구는 수정 필요** | 작성자 13개 로그의 통과·실패 줄을 다시 셌고 JSON과 일치. 내부 독립 150개 사례도 모두 pass 기록. 전체 gate 로그 155개 lane 및 receipt 해시 일치. 실제 물리 실행이라고 쓰지는 않는다. 다만 NOTE의 “잘못된 runner 표지/모호 RESUME 공존은 승인하지 않는다”는 현재 반례를 제외하는 범위 표기가 필요하다. |

Q1 보충: 숫자값이 정확한 0인 `0e1000000000`은 0으로 수용된다. 반면 `3e-1000000000`은 0으로 반올림해 수용되지 않고 거부된다. 따라서 “큰 지수 문자열은 모두 거부”라고 적기보다 “비유한/넘침·정수가 아닌 값은 거부, 안전하게 표현된 정확한 정수값은 보존”이라고 쓰는 편이 실제 계약과 맞는다. 음수 부호가 있는 `-0`은 문법상 거부된다. 이 둘을 새 차단 결함으로 세지 않았다.

정상 모의 재개의 값:

| k | 재개 step | 결과 | rho_pct | 중단 없는 대조와 비교 |
| ---: | ---: | --- | ---: | --- |
| 0 | 3230000 | RM_STOP / OK | 0.20260778734286913 | 정확히 같음 |
| 1 | 3310000 | RM_STOP / OK | 0.20260778734286913 | 정확히 같음 |
| 2 | 3360000 | RM_STOP / OK | 0.20260778734286913 | 정확히 같음 |
| 3 | 3410000 | RM_STOP / OK | 0.20260778734286913 | 정확히 같음 |

여기의 `rho_pct`는 독립 실행에서 다시 얻은 **합성 관측 입력의 판독값**이다. 실물 언로딩의 되튐률 측정이나 물리 동등성 증명으로 인용하면 안 된다. k=0/1의 모든 행이 중단 없는 실행과 동일하다는 주장도 하지 않는다.

## 5. 실행·원자료 검증을 구분한 증거 장부

| 증거 | 이번 검토에서 한 일 | 결과 |
| --- | --- | --- |
| 제출 파일 신원 | ZIP 426 manifest 항목 재계산, 리포 파일 407개를 원격 핀 Git blob과 대조 | 불일치 0; ZIP 경로 이탈·중복·심볼릭 링크 없음 |
| 현재/기준 소스 | 원격 두 핀의 kit·등록문서를 고정 다운로드, 변경 범위 재계산 | 6파일 범위, reader SHA·diff SHA 일치 |
| 정수 산술 | Decimal을 기대값 계산에 재사용하지 않고 Fraction으로 500개 생성 사례 + 14개 경계값 계산 | 514/514 |
| 좁은 실제 CLI | 44개 탐침 중 사전에 수용/거부를 정한 35개 + 탐색 9개 | 정해진 35개 모두 기대대로; 탐색에서 위 두 유형 분리 |
| 집중 반례 | 현재·기준 각각 정상/음성/변형/복구 6개를 실제 arm CLI로 실행 | ULPRI-01/02는 양쪽 핀에서 재현; CSV 불변 |
| R39 | 현재 함수를 직접 실행 | 90/90 |
| reader 전체 자체시험 | 소스 불변, Windows 하위 Python 프로세스에 UTF-8 모드만 추가하여 실행 | 기준 214/214, 현재 304/304 |
| 작성자 변이 11개 | 제공된 변이 도구를 핀 코드에 다시 실행 | 모두 검출, 예외 0, 실패 수 22·12·5·2·7·1·4·2·6·3·3 재현 |
| 작성자 13개 kit 명령 | 제출된 원래 로그의 ✓/✗ 및 rc를 재계수 | 기록상 모두 rc 0·FAIL 0, README/NOTE 집계와 일치 |
| 내부 독립 150개·별도 변이 2개 | 원래 JSON의 사례·실패 목록과 로그를 대조 | 기록과 일치; 이번 11개 변이 재실행에 더하지 않음 |
| 전체 저장소 gate | 로그의 155 lane 재계수, receipt의 로그 SHA 대조, before/after 신원 비교 | 기록상 155/0·rc 0; 이번 환경에서 전체 gate를 새로 돌린 결과는 아님 |

전체 gate 로그 SHA-256: `f27982bb9f2497c32dcea0a3e50130c6dea2dac16492d1fde3b32750bd8656c3`. receipt의 candidate는 `652d43704034f24d2f4a024092b36ce0ddf558fe`다. 835항의 before/after 신원표는 같고, 그중 이번에 확보한 파일 100항의 바이트와도 일치했다. 나머지 저장소 전체 파일을 모두 재다운로드해 다시 실행했다고 주장하지 않는다.

Windows에서 원래 kit 명령을 그대로 실행한 초기 로그에는 외부 fixture 누락, 하위 `python -I`의 cp949 출력 인코딩, Bash 실행 불가가 섞였다. 의존 fixture는 고정 핀에서 확보했고, reader는 **하위 인터프리터에 `-X utf8`만 추가한 별도 진단**으로 214/304 전수를 통과했다. 이 결과를 무수정 Linux CLI 13/13 재현으로 적지 않는다. 덱 생성 바이트 비교·실제 arm CLI·새 반례에는 생산 소스 패치가 없다. Bash 기반 runner 전수 및 실제 DEM restart는 이번 검토의 독립 실행 증거가 아니다.

증거 수는 합산하지 않는다. 514개 산술 표본, resident 90개 단언, 기존 304개 자체시험, 44개 CLI 탐침, 11개 제공 변이는 서로 중복되는 보증 범위를 가진다.

## 6. 우리 트리에서 재현

증거 ZIP을 풀면 `repo/`에 핀의 필요한 파일과 검증된 의존 fixture, `baseline/`에 비교 기준이 들어 있다. 전체 Git 저장소는 아니다. 새 출력 경로를 지정한다. 이 스크립트는 합성 파일만 쓰고 물리 실행을 하지 않는다.

```bash
# 외부 검토에서 새로 작성한 집중 반례 — 먼저 이것만 재실행하면 된다.
python3 -B repro_boundary.py --repo ./repo --out ./rerun_boundary

# 같은 두 경로가 기준판에도 있었는지 확인
python3 -B repro_boundary.py --repo ./baseline --out ./rerun_boundary_baseline

# 별도 산술 오라클·정상 k=0/1/2/3·44 CLI 탐침
python3 -B probe_independent.py
```

Windows는 위 명령의 `python3 -B` 대신 `python -X utf8 -B`를 사용한다. 임시 디렉터리는 해당 환경에서 허용된 경로로 설정한다. 집중 반례 스크립트는 폴더 위치를 인자로 받으므로 원래 checkout에서도 `--repo <고정 핀 경로>`로 실행할 수 있다.

핵심 산출:

- `evidence/boundary/result.json` 및 여섯 사례별 `cli.log`, 원본 CSV/manifest, `arm_verdict.json`
- `evidence/boundary_baseline/result.json`
- `evidence/independent/integer_oracle.json`, `positive.json`, `cli_cases.json`
- `evidence/windows_diagnostic/results.json` — UTF-8 인터프리터 적응을 명시한 전수 자체시험
- `evidence/mutations_replayed/results.json`
- `evidence/scope_and_counts.json`, `intake.json`, `zip_pin_checks.json`, `source_manifest.json`

`arm` 명령은 UNIDENTIFIED일 때도 rc=0일 수 있다. 이 CLI는 판정 JSON을 생성하는 진입점이며, 이번 판정은 rc 대신 `resume_auth`, `primary_status`, `rho_pct`, `rank_eligible`와 입력 바이트를 읽었다. rc=0을 물리 실행 허가로 해석하지 않았다. 이후의 실제 생산 launch gate까지 통과한다고 주장하지도 않는다.

## 7. 최소 종결 조건

1. ULPRI-01의 변형된 RESUME 표지를 오류로 남기고, 다른 정상 표지만으로 승인하지 않는 arm 회귀 추가.
2. ULPRI-02의 Unicode 줄 구분자를 키 선별 전에 거부하는 회귀 추가. 기존 LF/CRLF/CR 및 정상 k=0/1/2/3 유지.
3. 두 반례에서 인증 없음·옛 행 제외 0·UNIDENTIFIED/null·rank 불가·입력 CSV 불변을 함께 재현.
4. 기존 R39·reader 및 봉인 재확인. 기존 코드에서 숫자만 정수로 만드는 우회 수정이나 표지 공백을 조용히 정상화하는 수리는 피할 것.
5. README/NOTE는 정상 표지의 정수성 교정과 기록 구조의 보증 범위를 구분할 것. 실물 런의 신규 승인으로 확장하지 말 것.

이 두 앞단 경계를 고치기 위해 물리값·덱·등록 판정선을 바꾸거나 실물 시뮬레이션을 다시 돌릴 필요는 없다. 현재 숫자 파서의 교정은 유지하는 것이 맞다.

**최종: 정수 파싱 교정 수용 / Q2·Q3 무결성 종결 HOLD.**
