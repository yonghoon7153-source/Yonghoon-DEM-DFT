# DEM1 포맷 — LIGGGHTS 캠페인 sh 도구 (1저자 정의 · 10-28)

- 1저자 10-28: *"이거가 DEM1이야 · DEM1으로 해줘라고 하면 이 형식대로 하면됨 · claude.md에 잘 적고 기록해놔"*.
- 정본 = `dem1_kit/DEM1_handoff.md` (일하는 방식 · 기계 · 포맷 정의 · 재개 엔진 · LIGGGHTS 사실 · 후막 6 케이스 상태 · 할 일 · 테스트 키트).  접속 주소 · 포트 네 자리만 가렸다 (원본 sha256 `8e8876acf963dcb045ef21d98b12cf2dccc1fd0385f9c25daabfd4815c12d18f`).
- 키트 = `dem1_kit/` (1저자 업로드 `dem1_kit.zip` sha256 `1d7734ab5bd58015724623f5fa1d27b06d1edb30fd68aea1b42ee542ca41cecf` 를 풀어 그대로 · 바꾼 것 = 인수인계 문서의 주소 가림 + 머리 한 줄).

| 파일 | 무엇 |
|---|---|
| `dem1_kit/tool/th_grid.sh` | 기준 구현 (후막 6 케이스 · md5 `337e840de647382ee3e01f4825afda70` = IBB `~/th_grid.sh`) |
| `dem1_kit/tool/th_grid_block.txt` | IBB 설치 블록 (md5 게이트 → gen 까지) |
| `dem1_kit/tool/make_block.sh` | 스크립트 → 블록 (느낌표 · 탭 · CR · 구분자 검사 + md5) |
| `dem1_kit/test/run_tests.sh` 외 | 납품 전 시험 (진짜 LIGGGHTS + Slurm 흉내 `slurm.py` · 샌드박스에서만) |

## 쓰는 법 (요지 · 자세한 것은 인수인계 문서)

1. 1저자가 **"DEM1 으로 해줘"** (또는 "DEM1 포맷으로" · "이런 sh 로") 라고 하면 `dem1_kit/tool/th_grid.sh` 구조 그대로 새 도구를 만든다 — 케이스 표 · 템플릿만 바꾸고 구조를 새로 짜지 않는다.
2. 납품 = 블록 하나 (`cat > ~/X.sh <<'X_EOF'` … + md5 게이트 · gen 까지) — `bash dem1_kit/tool/make_block.sh X.sh "bash ~/X.sh gen"` 로 검사해 만든다.  제출은 표 확인 뒤 `bash ~/X.sh start` 한 줄 따로.
3. 납품 전 `LMP=<lmp> bash dem1_kit/test/run_tests.sh all` (❌ 0) — 이 컨테이너 같은 샌드박스에서만 (`pkill -x lmp_mpi/mpirun` 을 쓴다 · IBB 에서 돌리지 않는다).
4. 물리 파라미터 · 원본 덱 · 러너 · restart · dump 는 바꾸지 않는다 (재개 덱 · 판 STL 은 새 파일).
5. 답 = 한국어 · 짧게 (인수인계 §1: 반말) · 수치 표 → 바뀐 점 · 주의 → 실행 줄.

## 이 리포의 등록 캠페인과의 경계

- 50kg 처럼 등록 순서 · 재개 도구 (`scripts/resume_ckpt.sh` · G0–G3) 가 정해진 캠페인은 DEM1 도구로 제출 · 재개하지 않는다 — DEM1 꼴의 **읽기 전용 watch** 만 붙인다.
- DEM1 도구의 수치 (예상 일수 · 처리량) 는 도구가 내는 운영 어림이다 — 판정 · 보고 수치가 아니다.
