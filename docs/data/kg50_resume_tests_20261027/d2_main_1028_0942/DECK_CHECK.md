# D2 본 런 (ibb job 328599) 재개 덱 대조 — 10-28 밤 (메인 · 읽기만 · KG50R-02 · 03 · 05 꼴 확인)

- 받은 묶음 `received_d2_resume_1028.tgz` (7,150 B · sha256 `b0d376a6ffa97f81d2e9feb41aa8c53010915e0e19c483247503f7b9a6474635` · 1저자 10-28 밤 ibb `~/dem_test` 에서 tar · 10 파일) · 보고 원본 = 상위 폴더 `resume_r4_1028_0942.md` (sha256 `d0d9f3f02ff4b5b4fc4f9f0236ea2ced830e2b14e3d3b3dd1718954b616e97dc`).
- ibb 원 덱 `input_kg50_d2_b50.liggghts` sha256 = 리포 v3 덱 (`docs/data/kg50_decks_20261027_v3_b50/kg50_d2_b50/`) 과 같음 (앞 16 자 `f8ac9932a6cb4a0b`).
- 논리 명령 단위 대조 (주석 · `&` 이음 처리 · 공백 정규화 · 이 세션의 일회성 스크립트): 원 덱 129 · 재개 덱 123 명령 · 재개 덱 첫 긴 run = `run 180000` (옵션 없음 · 한 줄) · **그 뒤 명령 = 원 덱 정착 run (`run 200000`) 뒤 명령과 차이 0 줄** · 재개 덱 앞부분에서 원 덱에 없는 명령 = 셋뿐 (`read_restart restart_kg50_d2_b50/restart_settling_20001.bin` · `shell mkdir -p post_kg50_d2_b50` · `shell mkdir -p restart_kg50_d2_b50`) · 옵션 붙은 run 0 · label = `loop_press` 하나.
- ⇒ D2 는 KG50R-02 (첫 run 옵션) · 03 (끼어든 물리 명령 · 변수 · label) · 05 (계속 줄 run) 꼴이 아니다 (이 덱 한정 · 앞부분 상태 재현의 전수 증명은 아님 — 고친 도구의 전체 대조로 다시 본다).  KG50R-01 (압축 위상) · 04 (옛 시험) 도 해당 없음 (settling 재개 · 새 시험 328597).
- 관찰: `shell mkdir -p` — LIGGGHTS `shell mkdir` 는 인자마다 폴더를 만들어 `-p` 라는 폴더가 생길 수 있다 (DEM1 기록 · 물리 무관 · 확인 전).
