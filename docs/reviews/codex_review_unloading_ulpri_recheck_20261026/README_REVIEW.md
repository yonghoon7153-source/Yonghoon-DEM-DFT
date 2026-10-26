# ULPRI 재확인 전달 묶음 — 2026-10-26

먼저 `codex_review_unloading_ulpri_recheck_20261026.md`를 읽으십시오.

판정: ULPRI-01/02 닫힘. 새 P1/P2 없음. 표지 경계 수정의 GO이며 실제 언로딩 실행 승인이 아닙니다.

- `snapshot/`: 첨부 ZIP에서 받은 고정 핀 4c29705fa1c4의 자료. 파일 내용 무변경. 전체 리포 checkout은 아닙니다.
- `baseline/`: 원 반례를 재실행한 기준 01c1aaf5be8a의 kit 및 필요한 지원 스크립트 사본. 전체 리포가 아닙니다.
- `probe_independent.py`: 추가 Unicode 경계 208건. `--repo`, `--out` 필요. 출력 폴더는 새 경로.
- `probe_mutants.py`: 새 탐침이 가드 되돌림 4종을 잡는지 확인. 처음 전달된 실행 결과는 `evidence/mutants/`. 다시 돌릴 때 스크립트 출력 경로만 새 이름으로 지정하십시오.
- `repro_boundary.py`: 앞 판 여섯 입력의 동일 재현. `--repo baseline` / `--repo snapshot`으로 대조 가능.
- `evidence/a43/`: 작성자 portable 43건을 이번 환경에서 다시 실행한 결과.
- `evidence/matrix_v2/`: 독립 208건의 실제 CLI 결과, 원 입력, 입력 해시.
- `evidence/{old6,new6}/`: 기존 반례의 전후 결과.
- `evidence/mutants/`: 변이 사본, 결과, 입력 해시. 승인된 코드가 아닙니다.
- `evidence/utf8_selftest/`: Windows 자식 Python UTF-8 실행 옵션만 보정한 자체시험 346/346. 무수정 원 CLI 통과로 인용하지 마십시오.
- `diagnose_utf8.py`, `diagnose_deck_utf8.py`: 그 환경 진단을 재현하는 스크립트. 대상 생산 파일을 수정하지 않습니다.
- `receipt_audit.json`: 제출된 13개 kit 명령 및 공유 155 게이트의 원본 로그 감사. 이번 독립 재실행과 구별하십시오.
- `remote_*.json`, `scope.json`, `*.diff`: 원격 blob 대조와 범위 확인.
- `source_postcheck.json`: 시험 뒤 snapshot 524개 소스 바이트와 manifest 재확인.
- `MANIFEST.sha256`: 이 전달 묶음의 파일 해시. 자신은 제외.

모든 실행은 합성/판독 시험입니다. 물리 시뮬레이션은 실행하지 않았습니다. Python 3와 NumPy가 필요합니다.

Windows에서는 유효한 작업용 TEMP/TMP/TMPDIR을 정하고 자식 Python에도 `-X utf8`가 적용되어야 합니다. 초기 임시 경로/인코딩 실패 로그도 `evidence/`에 보존했습니다. 실패한 임시 fixture 트리와 Python bytecode는 포장하지 않았습니다. 성공 행렬 `matrix_v2`만 최종 증거입니다.

Linux에서 간단한 재현:

```bash
python3 -I -X utf8 -B probe_independent.py --repo snapshot --out /tmp/ulpri-new-208
python3 -I -X utf8 -B repro_boundary.py --repo baseline --out /tmp/ulpri-old-six
python3 -I -X utf8 -B repro_boundary.py --repo snapshot --out /tmp/ulpri-new-six
```

입력에 기재된 절대 경로는 실행 당시 경로이며 출처 기록으로 보존했습니다. 스크립트의 repo/out 인자로 새 경로를 지정할 수 있습니다. tmp 내용이나 물리 재시작 이진 파일은 필요하지 않습니다.
