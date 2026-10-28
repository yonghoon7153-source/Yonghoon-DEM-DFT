# dem1_kit — DEM1 포맷 인수인계 키트

| 파일 | 뭐 |
|---|---|
| `DEM1_handoff.md` | **새 대화에 통째로 붙여넣는 인수인계 프롬프트** (규칙·포맷·현재 상태·할 일) |
| `tool/th_grid.sh` | DEM1 기준 구현 (후막 6케이스, md5 337e840de647382ee3e01f4825afda70 = IBB `~/th_grid.sh`) |
| `tool/th_grid_block.txt` | IBB 설치 블록 (md5 게이트 → gen 까지) |
| `tool/make_block.sh` | 수정한 스크립트로 블록 다시 만들기 (`!`·탭·CR·구분자 검사 + md5) |
| `test/run_tests.sh` | 납품 전 테스트 (진짜 LIGGGHTS + Slurm 흉내) — `all` / `insert` / 개별 |
| `test/kit_lib.sh` | 테스트 공용 함수 (목업 홈·데몬·검사) |
| `test/slurm.py` | Slurm 흉내 (sbatch·squeue·scancel·scontrol·sacct + 의존·보류·QoS·시간제한 데몬) |
| `test/mkdeck_th.py` | gen 덱을 테스트용으로 축소 |
| `test/lmp_wrap.sh` | ERROR / 조용한 실패 주입용 lmp_mpi 래퍼 |
| `test/build_liggghts.sh` + `Makefile.novtk` | 테스트용 LIGGGHTS-PUBLIC 빌드 (VTK 없이) |

**순서**: `DEM1_handoff.md` 읽기 → (LIGGGHTS 없으면) `bash test/build_liggghts.sh` → 도구 수정 → `LMP=… bash test/run_tests.sh all` (❌ 0) → `bash tool/make_block.sh …` → 블록을 사용자에게 (파일로 주면 scp → `sed -i 's/\r$//' ~/X_block.txt && bash ~/X_block.txt`).

⚠ 테스트는 샌드박스에서만 (`pkill -x lmp_mpi/mpirun` 사용). IBB 에서 돌리지 말 것.
