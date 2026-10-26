# 전달 묶음 — DEM 언로딩 정수 파싱 검토, 2026-10-24

먼저 `codex_review_unloading_ulpr_integer_20261024.md`를 읽으십시오.

- 판정: 정수 파싱 교정 수용. Q2·Q3 무결성 종결은 P2 두 건으로 HOLD.
- 대상: `01c1aaf5be8acdf7d1716f34cc86fc77d8e27362`
- 비교: `8347d32ea678c0174bd77d4c79cfbd7b0591e4a3`
- `repo/`: 제출 자료 및 원격 핀에서 바이트 검증한 시험 의존 파일. 전체 checkout이 아님.
- `baseline/`: 비교 기준의 관련 파일.
- `evidence/`: 이번 검토의 원자료. 제출된 저자 원자료는 `repo/docs/reviews/ulpr_resume_integer_evidence_20261024/`에 따로 보존.
- `MANIFEST.sha256`: 이 전달 ZIP 안 파일별 SHA-256. 자기 자신은 제외.

최소 재현 (새 출력 폴더):

```bash
python3 -B repro_boundary.py --repo ./repo --out ./rerun_boundary
```

Windows는 `python -X utf8 -B`를 사용하십시오. 스크립트는 실제 reader 함수와 arm CLI를 호출하지만, 입력은 합성 제어흐름 fixture입니다. LIGGGHTS·물리 시뮬레이션을 호출하지 않습니다.

`probe_independent.py`는 산술 오라클·정상 k=0/1/2/3·44개 CLI 사례를 다시 생성합니다. `diagnose_windows.py`는 Windows 하위 Python 인코딩만 UTF-8로 지정하는 별도 전수 자체시험입니다. 이 진단을 무수정 Linux 실행으로 세지 마십시오.

`intake.py`, `fetch_context.py`, `check_scope.py`, `final_integrity.py` 등은 이번 Windows 수집·검증 작업 기록입니다. 일부는 원래 경로 및 Windows 장경로 규약을 사용합니다. 집중 반례 재현에는 필요하지 않습니다.

원 소스·덱·Git 상태를 고치지 않았습니다. 실제 restart, 전체 155 lane의 독립 재실행 및 물리 실행 GO는 이 묶음이 증명하지 않습니다. 수치·변이·내부 검토 수를 합산하지 마십시오.
