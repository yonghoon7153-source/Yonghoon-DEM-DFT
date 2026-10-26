# KG50 독립 검토 전달 묶음

먼저 codex_review_kg50_decks_20261026.md 를 읽으세요.
판정: 현재 속도시험/본런 경로 HOLD. P1 2건 + P2 4건 + P3 2건.

snapshot/ 은 사용자 입력 ZIP에서 추출한 원본입니다. evidence/intake.json의 51개 파일 SHA256을 전달 직전 다시 대조했습니다. 생산 파일은 수정하지 않았습니다.
원격에 아직 없는 커밋/트리 신원은 사용자 진술로 기록했습니다. source를 바꾸거나 최신 가지로 갈아 끼우지 않았습니다.

evidence/에는 실제 실행한 CPU 생성/산술 검사, 합성 로그 의미 탐침, 공식 LIGGGHTS 고정 버전 소스와 원문 링크가 있습니다.
물리 DEM/MPI/WSL/SLURM 실행은 0회입니다.
evidence/kg50_restart/probe_resume_gates.py는 준비된 Bash harness지만 실행되지 않았습니다. 성공한 조건 검증은 probe_source_semantics.py입니다.

보고서 §11의 명령은 이 폴더에서 실행합니다. 생성기 selftest는 임시 폴더에 덱을 만듭니다.
MANIFEST.sha256는 자기 자신을 제외한 모든 전달 파일의 체크섬입니다.
PACKAGING.json은 원본 보존 검사 및 파일 수를 기록합니다.

