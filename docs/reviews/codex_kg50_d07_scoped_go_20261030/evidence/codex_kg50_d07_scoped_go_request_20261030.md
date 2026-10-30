# Codex 요청 — 50kg D0.7-50 정착 체크포인트 재개 본 제출 **한 건 범위** GO (10-30)

> **한 줄**: 재개 도구 전체 종결이 아니라, D0.7-50 **한 건** — 아래 재개 덱 · 시험 덱 · 러너 둘 · 체크포인트 · 도구 · 생성기 sha — 의 본 제출 (NP 56 · 정착 끝 step 200,001 에서 멈춤 · 등록 Q6) GO 를 묻는다.  1저자 10-30 Q12 *"권고대로해"* · 56 코어 본 제출 = Codex GO 뒤 (1저자 10-28).  리뷰 핀 = `09ae533d05f6f165c9754ff4edd42cd97c7c3c06` (원격 push 됨 · 리포 파일 = 그 blob) · 이 요청서 · `-T` 묶음 · 대조 증거 = 이 ZIP 에만 (커밋은 뒤에).

## 0. 이번에 닫는 것 / 닫지 않는 것

| 닫는 것 (이 한 건) | 닫지 않는 것 |
|---|---|
| 재개 덱 `input_kg50_d07_b50_r56.liggghts` (sha256 `8e129f42…`) 가 원 덱 `input_kg50_d07_b50.liggghts` 의 체크포인트 `restart_settling_20001.bin` (step 20001 · sha256 `aa833368…`) 이후와 같은 물리인가 | 재개 도구 일반 종결 (`KG50R-F01` · `F02` · 사전 공격 `PAI-01`–`09` 의 일반 판정) |
| 실제 `-T` (NP 56 · 2,000 step · ibb job 333858) 의 G0–G3 | 다른 침대 · W1 갈래 · Q5 판정 (`KG50R-F03`) · 정착 이후 단계의 물리 자격 · 결과 |
| 러너가 검사한 덱을 실행하는가 — 잡 안 해시 대조 · `LMP_IDENTITY` 줄 · 5 파일 영수증 | 본 잡 (`-T` 없는 호출) 의 실행 증거 — 아직 없음 |

## 1. 자료

| 무엇 | 값 |
|---|---|
| 도구 | `scripts/resume_ckpt.sh` sha256 `2dc7f693263708d7788ab721386182c6109a8f9278797ecc43f5165d6715f1e8` (핀 blob = ibb `~/dem_test/scripts/resume_ckpt.sh` · `-T` 보고 '도구 신원' 줄) |
| 생성기 | ibb `~/dem_test/dem_restart.py` sha256 `d6e590a18849d10c70dc831d5e8bebabf3a5163d502d5968db9688a70a29d7c8` (리포에 없음 · '도구 신원' 줄) |
| 원 덱 · 원 러너 | `docs/data/kg50_decks_20261027_v3_b50/kg50_d07_b50/` (핀 blob · ZIP `repo/`) |
| `-T` 묶음 | `kg50_d07_T_1030.tgz` 16,401 B · sha256 `5e5461c331cc8c060ac6fce22080142c614b09af07413ab5fe676456d2a2d549` (1저자 ibb · 멤버 41 · 경로 이탈 · 링크 0) — 보고 `resume_r56_1030_140521.md` · 시도 폴더 `attempt_r56_1030_140521_985018/` (18 파일) · 덱 r56 · r56t · 러너 r56 · r56t · 시험 출력 `output_kg50_d07_b50_r56t_333858.out` |
| 5 파일 영수증 | `main_inputs.sha256` (sha256 `29ff619a666f29131a9d582f27e555590316e8516dcf9d0a7d2af01715bde6fa`): 재개 덱 `8e129f42…` · 본 러너 `aad9ac22…` · 시험 덱 `94db4187…` · 시험 러너 `c00746e6…` · 체크포인트 `aa833368…` |
| 대조 증거 | ZIP `evidence/` — `diff_D07.txt` · `diff_D2.txt` · `transform_compare.json` · `compare_transform.py` |

## 2. 이 한 건의 대조

### 2-1 원 덱 ↔ 재개 덱
- `evidence/diff_D07.txt` (unified · n=0) = 40 줄 (뺀 25 · 넣은 15) — 머리 주석 · `create_box` 자리 → `read_restart restart_kg50_d07_b50/restart_settling_20001.bin` + 템플릿 · 분포 재선언 (`pts1` `pts2` `pts3` `pdd_mix` = 원 덱 줄 그대로) · 삽입 블록 삭제 · `shell mkdir` → `shell mkdir -p` · 첫 긴 run `run 200000` → `run 180000` · `write_restart` 공백.
- 첫 긴 run 고침 = 도구 출력 그대로: 생성기 잔여 179,999 → 180,000 (본 덱 그 run 끝 200,001 − 20,001 · 원 줄 157 · 다시 대조 통과 · `fixrun_r56.txt`).

### 2-2 D2 선례와 같은 변환인가
- D2-50 (`docs/data/kg50_resume_tests_20261027/d2_main_1028_0942/` 원 덱 ↔ r4 재개 덱) — 10-28 09:42 본 제출 → 10-29 끝 (1저자 화면 `Simulation Finished` · step 4,015,002 · ERROR 0).
- `compare_transform.py` 결과: 두 변환 모두 diff 40 줄 (뺀 25 · 넣은 15 = 원 덱 줄 7 + 새 줄 8) · 새 줄 8 = 케이스 이름 · 접미사 정규화 뒤 **같음** · 뺀 25 줄 = 숫자 가림 뒤 **같음** (`transform_compare.json`).

### 2-3 체크포인트 앞 (준비 구간) 의 위험 문법 — 원 덱 실측

| 꼴 (출처) | 덱 전체 | 체크포인트 (165 행) 앞 |
|---|---|---|
| 이름 자리 `${…}` (사전 공격 R1) | 0 | 0 |
| `run … every` (R2) | 0 | 0 |
| CR · NBSP · 탭 (R3) | 0 · 0 · 0 | 0 |
| 명령 쪽 비 ASCII (R3) | 0 (주석에만) | 0 |
| `print … file/append` (R4) | 16 | 0 (182 행부터 = 판 생성 단계) |
| `jump` · `label` · `clear` (R5) | 1 (224 행) | 0 |
| `neigh_modify exclude` · `run upto` | 0 | 0 |
| `&` 줄잇기 · `if` | 36 · 4 | 28 · 3 (삽입 수 관문 — D2 와 같은 꼴) |

### 2-4 `-T` 결과 (보고 그대로)

| 관문 | 결과 |
|---|---|
| 정적 대조 | 통과 (문제 0) · 남은 step 같음 끝 200,001 · 첫 긴 run 뒤 명령 64 같음 · 그 자리 치환 4 곳 같은 상수 · 재개 지점 상태 본 48 · 재개 46 (재개 덱이 `region reg_box` · `reg_mix` 재선언 안 함) · 헬퍼 러너 엄격 대조 통과 (#SBATCH 6 · 환경 줄 6 · cd 실제 경로 `/lustre/home/yonghoon/dem_test/kg50_d07_b50`) |
| G0 | COMPLETED · ExitCode 0:0 · 끝 step 22,001 = 기대 · 마지막 thermo 줄 정상 · `Loop time … for 2000 steps` · 상태 조회 실패 1 번 뒤 끝 상태 얻음 · **잡 안 덱 신원 관문 통과** |
| G1 | step 20,001 · 원자 488,291 · KinEng 2.2522724 = 원 로그 |
| G2 | 체크포인트 step 덤프 없음 → G1 KE 일치로 대신 (도구 규칙) |
| G3 | step 21,000 KinEng 2.3879436 = 원 로그 (5 % 안 · 실제 같음) |
| 분해 | `processors * * 1` → 8 × 7 × 1 (1저자 watch) |

### 2-5 검사한 덱 = 실행한 덱
- 시험 로그 `LMP_IDENTITY` 줄: `lmp_mpi=/home/yonghoon/LIGGGHTS-PUBLIC/src/lmp_mpi sha256=ee2d7726…` · `deck=…/input_kg50_d07_b50_r56t.liggghts sha256=94db4187…` · `checkpoint=…/restart_settling_20001.bin sha256=aa833368…` = 영수증 셋째 줄 · 체크포인트 · lmp_mpi = 기록만.
- 본 제출은 도구가 새 시험부터 다시 돌고 G0–G3 · 큐 · sha256 를 다시 본 뒤 낸다 (보고 끝 줄).

## 3. 남은 도구 한계가 이 한 건에 주는 영향

| 항목 | 이 한 건 |
|---|---|
| `PAI-01` (P1 · 판 메시 file 이름 허용이 작업 폴더 밖 STL 도 받음) | 해당 없음 — `deckcheck_r56.txt` 의 '판 메시 파일만 다름' 0 줄 (1저자 ibb 확인) · 판 STL 은 덱 안 상대 이름 · 체크포인트 뒤 생성 |
| `PAI-02` (P2 · 본 명령 ↔ `-T` 영수증 미결합) | 손 확인 — 본 호출의 새 `main_inputs.sha256` sha256 = `29ff619a…` 인지 시험 잡이 끝나기 전에 대조 · 다르면 `scancel` |
| `PAI-03`–`09` (P3) | 증거 신원 · 격리 · ABA · 기록 빈칸 · 인자 검사 · 시험 고정물 — 정해진 명령 · 외부 쓰기 없음 · D0.7 삽입 덱 ↔ 본 덱 1–166 행 같음 |
| F02 안 닫힌 것 (본 잡 결과 미판독 · `-T` 모드 영수증 재확인 없음) | 본 잡 진행 = 1저자 watch · 정착 끝에서 멈춤 (등록 Q6) |
| `shell mkdir -p` (생성기 변환) | LIGGGHTS `shell mkdir` 은 인자를 폴더 이름으로 → `-p` 폴더 하나 · D2 선례와 같음 · 물리 무관 |

## 4. 질문
- **Q1** §2-1 · §2-2 로 재개 덱이 원 덱 체크포인트 이후와 같은 물리인가.
- **Q2** §2-4 · §2-5 로 "검사한 덱 = 실행할 덱" 이 이 한 건에서 성립하는가.
- **Q3** §3 의 남은 한계가 이 한 건의 본 제출에 영향을 주는가 (손 확인 둘이 충분한가).
- **Q4** GO 면 §5 명령 그대로 본 제출해도 되는가.

## 5. 본 제출 명령 (`-T` 보고 끝 줄 그대로)
`bash /home/yonghoon/dem_test/scripts/resume_ckpt.sh -n 56 -s ins1 -r /home/yonghoon/dem_test -x r56 -t 2000 -A 2dc7f693263708d7788ab721386182c6109a8f9278797ecc43f5165d6715f1e8 -H d6e590a18849d10c70dc831d5e8bebabf3a5163d502d5968db9688a70a29d7c8 kg50_d07_b50`
