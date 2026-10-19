# LHS214 S01 · S02 · S04 독립 재확인 묶음

먼저 `codex_review_lhs214s_fix_recheck_20261019.md`를 읽는다. 판정은 S01 지정 결함·S04 닫힘, S02 및 R03 전체 부분이다. 새 P1/P2 없음. 수치 인계 코드의 기존 HOLD 해제 가능 판단 유지, 새 214는 등록·봉인·실제 사전 점검·저자 승인 전 HOLD다.

## 핀과 구성

- 현재 `685c2bbdbbfee82898a9ec062bb9c2bc94612fc8`.
- 비교 `77d8fd44545c33cd10ab18fc250c7ad3023833ea`.
- ZIP은 같은 부모 아래 **두 형제 폴더**를 풀도록 구성했다. 폴더 이름을 유지한다.

```text
lhs214s_recheck_20261019/
  codex_review_lhs214s_fix_recheck_20261019.md
  README.md
  submitted/                  발송 요청서
  source/                     현재 핀의 manifest-listed 2,076 파일
  source_manifest.json         Git blob + SHA256
  probes/                     이번 독립 탐침
  evidence/                   원본 실패·통과 로그, JSON, 전체 HTML
  notes/                      세 독립 검토와 최종 교차검토
  tools/verify_and_package.py  무결성 검증·패키징 도구
lhs214rr_recheck_20261019/
  source/                     비교 핀의 manifest-listed 2,030 파일
  source_manifest.json
  evidence/receipt_fence_matrix.json
  evidence/receipt_fence_cases/  이전 114 입력
```

의존 라이브러리와 Python 실행 파일은 ZIP에 넣지 않는다. `tmp/`, pycache, 스냅샷 안의 manifest 밖 런타임 파일도 제외한다. `.git`은 없으며 checkout/fetch가 필요하지 않다. `evidence/source_integrity.json`은 양쪽 manifest의 실제 SHA256·Git blob 재검증 결과다. ZIP 내부 `PACKAGE_CONTENTS_SHA256.json`은 모든 패키지 입력의 hash를 기록하며 자기 자신은 제외한다. ZIP 전체 SHA256은 외부 `.receipt.json`에서 확인한다.

## 환경

실측 환경: Windows 11 build 26200, CPython 3.12.14, NumPy 2.5.3, SciPy 1.16.3, Flask 3.1.3, Jinja2 3.1.6, NetworkX 3.7, Requests 2.34.2, Matplotlib 3.11.2, Pillow 12.3.0, markdown-it-py 3.0.0, mdurl 0.1.2. 부속 의존성은 각 라이브러리 요구를 따른다.

실측 인터프리터:
`C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`.

탐침은 과거 작업의 형제 `deps/` 폴더를 import 경로에 더한다. 타 PC에서는 이 폴더를 복제할 필요 없이 **사용하는 인터프리터 환경에 필요한 라이브러리를 설치**하면 된다. 없는 형제 import 경로는 무시된다. 실제 사용 경로·버전은 `notes/package_dependencies.md`와 실행 metadata에 보존했다. OS/BLAS/라이브러리가 다르면 경계 원값은 달라질 수 있다. 같은 실패 수가 모든 환경에서 재현된다는 주장이 아니다.

## 격리 설정 — 모든 재실행 전에

ZIP을 풀어 `lhs214s_recheck_20261019`를 현재 폴더로 둔다. 재실행은 `evidence/`의 동명 산출물을 갱신하므로, 전달된 원본 증거를 보존하려면 **별도 복제본에서** 한다. 다음은 PowerShell 예시다. 프로덕션 ROOT·원자료 경로를 지정하지 않는다.

```powershell
$reviewRoot = (Get-Location).Path
$reviewTemp = Join-Path $reviewRoot 'tmp'
New-Item -ItemType Directory -Force -Path $reviewTemp | Out-Null
$env:TEMP = $reviewTemp
$env:TMP = $reviewTemp
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:OMP_NUM_THREADS = '1'
$env:OPENBLAS_NUM_THREADS = '1'
$env:MKL_NUM_THREADS = '1'
$env:NUMEXPR_NUM_THREADS = '1'
$env:WEBAPP_UPLOAD_FOLDER = Join-Path $reviewTemp 'uploads'
$env:WEBAPP_RESULTS_FOLDER = Join-Path $reviewTemp 'results'
$env:WEBAPP_ARCHIVE_FOLDER = Join-Path $reviewTemp 'archive'
$env:WEBAPP_MPM_LAB_FOLDER = Join-Path $reviewTemp 'mpm_lab'
$env:MPLCONFIGDIR = Join-Path $reviewTemp 'mpl'
$env:SUPABASE_URL = ''
$env:SUPABASE_KEY = ''
```

이 네 앱 저장 경로를 지정해야 소스 폴더 안에 빈 런타임 디렉터리가 생기는 일을 막을 수 있다.

## 핵심 재현

아래 `python`은 위 의존성이 있는 인터프리터를 뜻한다. 전체 DEM·새 214가 아니라 작은 합성망·문서·Flask 라우트 검사다.

```powershell
python -X utf8 -B tools/verify_and_package.py audit
python -X utf8 -B probes/root_checks.py metadata
python -X utf8 -B probes/root_checks.py receipt old
python -X utf8 -B probes/root_checks.py receipt new
python -X utf8 -B probes/s01_parser_audit.py all
python -X utf8 -B probes/s01_parser_audit.py selftest
python -X utf8 -B probes/s02_run.py old
python -X utf8 -B probes/s02_run.py new
python -X utf8 -B probes/s02_boundary.py
python -X utf8 -B probes/s04_run.py matrix_source probes/s04_matrix.py source
python -X utf8 -B probes/s04_run.py matrix_baseline probes/s04_matrix.py baseline
python -X utf8 -B probes/s04_run.py null_test source/webapp/test_single_null_metrics.py
python -X utf8 -B probes/s04_run.py submitted_baseline probes/s04_submitted_baseline.py
python -X utf8 -B probes/s04_run.py types_source probes/s04_types.py source
python -X utf8 -B probes/s04_run.py types_baseline probes/s04_types.py baseline
python -X utf8 -B probes/s04_compare.py
python -X utf8 -B probes/s04_run.py reg_web09 source/webapp/test_web09_accepted_refresh.py
python -X utf8 -B probes/s04_run.py reg_l214r03 source/webapp/test_l214r03_display.py
python -X utf8 -B probes/s04_run.py reg_labels source/webapp/test_closed_param_labels.py
python -X utf8 -B probes/s04_run.py reg_tau_final probes/s04_tau_adapter.py
python -X utf8 -B probes/root_checks.py regression
```

각 wrapper가 자식 프로세스의 rc와 로그를 저장한다. wrapper 자신의 rc만으로 성공 여부를 판단하지 않는다. 특히 아래 실패는 지워서는 안 된다.

- 이전 R01 23/26 및 현재 R01 23/29: 이 Windows의 실제 실패.
- 이전 null 시험 2/6 및 이전 페이지 matrix HTTP500 16건: 수정 전 반례.
- 실제 등록 receipt: 현재도 D1 하나로 rc1인 것이 맞음.
- S01 새 빈 제목 12 잘못 수용·2 잘못 거부: 자체시험 118/118과 별개로 남는 결함.

`s02_boundary.py`의 32/32는 원본 실패 검출과 진단 기하·정책 변이를 포함한 독립 단언이며 제출 원본 30/30이 아니다. tau 회귀 46/46은 `.git` 없는 스냅샷에서 검증된 4 TSV를 공급하는 어댑터를 거쳤다. 처음 환경 실패 로그도 함께 보존했다.

## 대표 증거

| 물음 | 파일 |
|---|---|
| 봉인 32·등록·diff | `evidence/root_metadata.json`, `root_code_diff.json`, `root_receipt_new.json` |
| 빈 `##` 반례 | `evidence/s01_new_cases/h2_empty.md`, `s01_receipt_h2_empty.json`, `s01_heading_boundary_cases.json` |
| 114문서·19,200울타리 | `evidence/s01_replay_114.json`, `s01_new_fence_matrix.json` |
| 실제 Windows 실패 | `evidence/s02_new_full.log`, `s02_new_full.json` |
| 인접 입력에서 target skip | `evidence/s02_boundary.json`의 `adjacent_skip`, `scan_1025`, `exact_hits` |
| null 수정·정상값 불변 | `evidence/s04_comparison.json`, `s04_matrix_source.json`, 전체 HTML 응답 |
| S05 및 타입 범위 | `evidence/s04_types_source.json`, `s04_types_baseline.json` |
| FULL/CF·provenance | `evidence/root_regressions.json`와 두 로그 |

추가 설계·수치 변경 또는 원장 상태 수정은 이 묶음에 없다. 보고서의 최소 해결은 권고 목록이며 구현이 아니다.
