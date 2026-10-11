# 접촉망 세대 2 재검증 6 전달 묶음

판정문: `codex_review_gen2_network_reverify6_20261011.md`.

- 검토 핀: `a20fc1875951bead5fad4a4d387e77b4979b84c6`.
- 생산 코드·등록·원장 수정 없음. source는 Git blob으로 확인한 읽기용 사본.
- `source/`: 검토 및 재현에 필요한 핀별 493파일. `source_manifest.json`에 blob SHA-1·SHA-256.
- `submitted/`: 받은 WSL 묶음 원본과 추출본. 이전 탐침 재실행에 쓰는 이전 라운드 증거도 구분된 폴더에 보존.
- `probes/`, `run_checks.py`: 독립 재현. `r5_*`는 이전 원 탐침 그대로이며, 본문에 박힌 옛 source_sha는 탐침의 작성 이력이다. 실제 실행은 이번 `source/`를 import.
- `fixtures/`: 한 케이스 합성 감사용 픽스처. 실제 194 생산 아님.
- `evidence/`: 결과 JSON, 원 stdout/stderr, 원 명령 rc·시간. 초기 사본의 자료 결손 및 Windows 환경 실패도 보존. 성공 로그만 골라 포장하지 않음.
- `tmp/`: 로컬 실행 임시 산출물이며 ZIP에서 제외. 원자료는 source에, 판정 재현 입력은 evidence의 `.input.json`에 별도 보존.

핵심 반례: `python run_checks.py r6_s0b_cli`.

다른 PC에서 실행할 때 `run_checks.py`의 의존성 경로를 설치 환경에 맞춰야 한다. NumPy/SciPy/NetworkX/Flask/Matplotlib 등이 필요하다. source 수정은 금지한다. Windows에는 POSIX `os.wait4`가 없으므로 WSL 부모 실행기 전수 시험은 Linux/WSL에서 돌린다.

`r5_observation` 등 이미 출력이 있는 탐침은 `--output-name`에 새 이름을 준다. 본 묶음의 `r6_*` 파일은 리뷰 증거를 새로 출력하는 도구이며 생산 실행 명령이 아니다. 부록의 합성 `TEST_ONLY_NOT_GO.md`는 배포 관문 시험용 입력이지 발사 승인서가 아니다.

수치 솔버 재설계, 194 생산, DEM/MPM, S3는 이 검토에서 실행하지 않았다. 상세 한정과 Q1–Q9 답은 판정문이 정본이다.
