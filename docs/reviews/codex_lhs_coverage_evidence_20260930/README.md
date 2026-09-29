# LHS 피복률 병합 전 리뷰 — 재현 증거

판정문: `docs/reviews/codex_lhs_coverage_verdict_20260930.md`.
고정 요청서/패치 스냅샷: `2e57dff90e7eebead7a446478f97e2c414176c28`.
대상: `da4670594` 위에 제출된 `0001–0007` 패치를 순서대로 적용한 소스.
패치 대상 8파일은 사용자 핀과 기준 커밋에서 바이트가 같았다. 패치·원본·적용본 해시는 `source_manifest.json`에 있다. 이후 HEAD는 사용하지 않았다.

## 포함 범위

- 네 `audit*.py`: 리뷰 작성자가 만든 합성 입력과 실제 함수/CLI 호출. 시뮬레이션이나 원격 계산은 하지 않는다.
- `*_results.json`, `harvest_comparison.json`: 위 호출의 결과.
- `.log`, `selftests.json`: 제출 코드의 selftest 독립 실행 및 명시된 플랫폼 통제 실행.
- `fixtures/`, `pipeline_fixtures/`, `cli_fixtures/`: 합성 입력/출력. 실 130/64 코퍼스가 아니다.
- ZIP의 `lhs_coverage_review_20260930/{baseline,candidate}`: 패치 대상 8파일만 포함. **완전한 실행 저장소가 아니다.**
- ZIP의 `submitted_bundle/`: 고정 핀에서 가져온 패치와 제출자의 로그. 제출자의 `gate.log`는 독립 실행 결과가 아니다.
- `PACKAGE_SHA256SUMS.json`: ZIP 안 각 파일의 해시. ZIP 자체 해시는 ZIP 옆 JSON에 있다.

## 재현 환경

실행 환경: Windows, Python 3.12.14, NumPy 2.3.5, pandas 3.0.1, SciPy 1.16.3, NetworkX 3.7, Flask 3.1.3.
다른 플랫폼의 마지막 부동소수 자리·줄바꿈·symlink 권한 차이는 별도 통제가 필요하다.

1. 생산 checkout이 아닌 **별도 전체 소스 사본**을 준비하고, 위 기준 + 포함 패치 7개를 적용한다. 또는 고정 핀의 전체 소스 사본에 적용한다(대상 8파일 동일 검증됨). 현재 브랜치 끝에 적용하지 않는다.
2. ZIP을 새 증거 디렉터리에 풀고 필요한 의존성이 있는 Python 환경에서 다음을 실행한다. `LHS_REVIEW_REPO`는 전체 후보 저장소, `LHS_REVIEW_BASELINE`은 ZIP에 포함된 baseline 디렉터리를 가리킨다.

```bash
export LHS_REVIEW_REPO=/absolute/path/to/isolated/full/candidate
export LHS_REVIEW_BASELINE=/absolute/path/to/unpacked/lhs_coverage_review_20260930/baseline
export PYTHONUTF8=1
export PYTHONDONTWRITEBYTECODE=1
python3 lhs_coverage_evidence_20260930/audit.py
python3 lhs_coverage_evidence_20260930/audit_pipeline.py
python3 lhs_coverage_evidence_20260930/audit_harvest.py
python3 lhs_coverage_evidence_20260930/audit_cli.py
```

PowerShell에서는 `export` 대신 `$env:LHS_REVIEW_REPO='C:/...'`와 같은 환경변수 문법을 쓴다. 스크립트는 증거 디렉터리 아래 자신이 생성한 fixture와 결과를 다시 쓴다. 원본 증거 보존이 필요하면 **압축 해제 사본에서** 실행한다. 전체 selftest를 다시 돌리려면 `run_selftests.py`를 사용한다. 전체 `check_all.sh`는 이 리뷰에서 독립 재실행하지 않았다.

## 해석과 한계

- `audit.py`: 실제 v2/수확기 함수. 무효 분모·고립 NaN이 `0.0/ok`로 나오는 두 반례와 정상 고립 입자의 실제 0인 양성 대조를 함께 둔다. 분모 붕괴와 반올림 경계 반례는 깊은 겹침의 경계 시험이며 코퍼스 발생률을 뜻하지 않는다.
- `wall_outside_numerator`는 좌표/접촉 기하가 일치하는 입력이다. `wall_invalid_exclusion`은 제외 산술을 보여 주는 직접 면적 장부 입력이며, 그 좌표와 면적을 실제 접촉 침대로 해석하지 않는다.
- `audit_pipeline.py`: 실제 orchestration 함수와 파일 정리/검증. standard/bimodal의 계산 subprocess만 대역으로 바꿔 오래된 v2 키가 지워지는지 본다. atoms-only 재현은 subprocess 자체가 없다. 원격 DB 설정은 비운다. 배치 selftest의 symlink만 byte copy로 바꾼 통제는 **배포 환경 symlink의 검증이 아니다.**
- `audit_harvest.py`: baseline/candidate를 같은 입력에 호출. fixture의 텍스트 쓰기만 LF로 통제한다. τ median 핀 실패는 두 코드가 같은 1 ULP 차이를 보여 패치 수치 회귀로 세지 않았다.
- `audit_cli.py`: 실제 CPU coverage CLI를 실행한다. nested archive skip과 손상 JSON의 rc=0은 기존 CLI 경로이지 이번 신규 결함으로 세지 않는다.
- AST 우회는 제공된 두 일반 import 문장의 검출 실패다. 현행 수확기가 실제로 그 우회를 사용한다는 주장은 아니다.
- 스크립트는 모든 연구 결론을 자동으로 판정하는 회귀 게이트가 아니라 **반례 생성·측정 증거**다. 패치 수정 후 기대 출력으로 바뀌었는지는 판정문의 해제 조건과 대조해야 한다.

원형 selftest: plastic 27/27, coverage 13/13, provenance 198/198, dataset 113/113. 수확기 137/139 → LF 통제 138/139(남은 τ 1 ULP); 배치 원형은 Windows symlink 권한 오류 → copy 통제 29/29. “전체 초록”으로 요약하지 않는다.
