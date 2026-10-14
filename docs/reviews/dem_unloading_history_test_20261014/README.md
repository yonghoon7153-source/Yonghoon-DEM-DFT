# DEM 언로딩 키트 — 이력 시험 (H0–H5) 재실행 (ibb · 2026-10-14) — 결과 기록

- 키트 · 판정 규칙 (정본): `docs/data/ps45_unload_20261009/README.md` §1 (fixture · 단계 · 판정 · 명령) · 등록 `docs/reviews/dem_unloading_ps45_prereg_20261009.md` §13-7-4.
- 첫 실행 (10-13 · job 281180) = H0–H5 전부 TECH — 이력 시험 덱 결함 (pair/gran/local compute 둘) · 고침 `dc6d285a9` · 원장 `ULK-02` · 키트 README §1-5.
- 이 폴더 = 그 고침 뒤 **재실행** 의 1저자 반입본 그대로 (바이트 그대로 · 접속 정보 없음).
- ⛔ 이 결과는 본 R · 10:0 이완 연장 · U 의 GO 가 **아니다** (키트 README 머리 · 등록 §13-6 — 다음 = Codex 키트 재검토).

## 0. 파일

| 파일 | sha256 | 무엇 |
|---|---|---|
| `hist_20261014_094731.report.tgz` | `be0acbd7841d0922604eee8aa31524fcddbe179a8240f937b317432dbebb0ca0` | 러너가 만든 보고 묶음 (66,910 B · 파일 206 · 풀면 509,561 B · 맨 위 폴더 둘 = 런 폴더 hist_20261014_094731 · kit 사본의 SHA256SUMS) — ibb 화면의 sha256 과 같음 |
| `ulHist_283122.out` | `5d3115fe7ed3e7c9999415480cf873c2833bd472ea0158f1ff87d9be17816e7f` | SLURM 출력 (사전 점검 · 단계마다 rc · 판정 · 보낼 것 줄) |

반입 처리: 새 빈 폴더에 복사 → sha256 대조 → 멤버 목록 (절대 경로 · `..` · 링크 · 장치 0) → `tarfile` `filter='data'` 로 풀기 → JSON · 텍스트만 읽음 (묶음 안 어떤 것도 실행하지 않음).

## 1. 실행 조건 (묶음 안 run_manifest.txt · SLURM 출력)

| 항목 | 값 |
|---|---|
| job · 노드 · 시간 | 283122 · node01 · 2026-10-14 09:47:31 → 09:47:59 KST (sacct COMPLETED 00:00:30 · ExitCode 0:0 — 1저자 화면) |
| 리포 판 | `repo_head` = `f9edcc41674bfef2c72bcb803511050845008d09` · `repo_dirty_here` = 0 (이력 시험 폴더) |
| 키트 봉인 | kit 사본 SHA256SUMS sha256 `241277b20aaccb8d1ab73c79fb9e0758138a3bed64751add98f7849b44697bf6` = 리포 `history_test/SHA256SUMS` (`dc6d285a9` 새 봉인) |
| LMP | `/lustre/home/yonghoon/LIGGGHTS-PUBLIC/src/lmp_mpi` · sha256 `ee2d77261bac9e7fa4e9311c8709e74bf7583a13225a5bc35a791bef9be60a3f` = 등록 §11-1 ⓖ 빌드 (러너 사전 점검 ✓) · `ALLOW_OTHER_LMP` 0 |
| NP | 6 (H2 = 4) · `mpirun --oversubscribe --bind-to none` · SLURM ntasks 6 |
| 단계 rc (SLURM 출력) | P · C6 · C4 · Ebot · Cbot · Etop · Ctop · Enone · Cnone · SYN · PZ · CZ = 0 · BAD = 1 (기대값 — 잘못된 내부 ID) |

## 2. 판정 (읽는 쪽 `read_history.py` · 결과 전 고정 기준 = 키트 README §1-3)

| 행 | 결과 | 결과 전 기대 | 세부 (판정 JSON) |
|---|---|---|---|
| H0 문법 · 기술 | **PASS** | PASS | rc · 배너 · Loop time procs = NP · 덤프 · reset 로그 |
| H1 같은 NP round-trip | **PASS** | PASS | primitive · mesh · pair PASS · sentinel 바닥 4 · 판 4 · 쌍 5 · 같은 값 중복 0 |
| H2 NP 바꿈 (6 → 4) | **PASS** | PASS | 같음 |
| H3 바닥 (primitive) 소거 | **PASS** | PASS | 소거 전 관측 PASS · PRE 전부 0 · POST 다시 참 · sentinel 4 / 4 소거 · 양성 대조 PASS |
| H4 판 (mesh) 소거 | **PASS** | PASS | 소거 전 관측 PASS · POST 다시 참 · sentinel 4 / 4 · 대조 PASS |
| H5 결손 · 0 뿐 분류 | **PASS** | PASS | 잘못된 ID → TECH · 0 뿐 → INCONCLUSIVE |
| 정보 ⓐ run 끝 자동 restart | 없음 (`auto_end_of_run_restart` false · 자동 restart step = 1500 만) | 미리 정하지 않음 | 본 키트 10:0 연장 덱은 이미 끝에서 명시 write_restart · 러너가 파일 확인 (README §1-3 ⓐ) — 바꿀 것 없음 |
| 정보 ⓑ 총힘 출력 시점 | PASS (접촉 없는 Z 입자 fz = −m g) | PASS | S3 함수 입력 = 덤프 f = 중력까지 더한 총힘 (등록 §13-7-1 C1) 가정과 같음 |
| SYN 문법 미리 지나가기 | PASS | PASS · 판 접촉 4 → 3 | rc 0 · 표지 · read_restart 뒤 dt · Ps 부호 · 판 접촉 W0 4 → W1 3 · 들어 올림 mesh z · 판 z 식 · 끝 restart 씀 |
| 정보 ⓓ 판 접촉 법선력 부호 | **−1** (한 부호 · 압축 상태에서 입자가 받는 fn_z 음수) | −1 (추정 · 미확인이던 것) | = 표 `unload_params.json` `plate_fn_compressive_sign` −1 — 표 바꿀 것 없음 |
| 읽는 쪽 rc | 0 | 0 | 0 = H0–H5 전부 기대대로 |

## 3. 내 대조 (컨테이너 · LIGGGHTS 없음)

- 같은 읽는 쪽 (`docs/data/ps45_unload_20261009/history_test/read_history.py` · 이 리포 판) 으로 풀린 런 폴더를 다시 판독 = rc 0 · 판정 JSON 이 묶음 안 판정 JSON 과 **같음** (`run_dir` 경로 키만 다름).
- 본 키트 복원 판정이 이 파일을 읽는 식 (`ul_reader.py` 의 이력 시험 칸 — exit_code 0 · H0–H5 status PASS · 부호 = 표) 을 이 판정 JSON 에 그대로 적용 = **통과** (부호 −1 = 표 −1).
  ⇒ 본 실행 7:3 `RJ` 에서 `HIST_VERDICT` 로 이 판정 파일 (ibb 런 폴더 안 history_verdict.json) 을 넘기면 복원 판정의 이력 시험 칸이 통과로 들어간다 (키트 README §3 ③ — ibb 의 이 런 폴더는 지우지 않는다).

## 4. 이 결과가 말하는 것 · 말하지 않는 것

- 말하는 것: 고친 이력 시험 덱이 등록 빌드에서 돈다 (`ULK-02` claimed_fixed 근거) · 복원 관문의 관측자 (primitive 바닥 · mesh 판 `wall/gran/local` · 입자쌍) 가 알려진 이력을 그대로 읽고, 지워진 이력과 가른다 (CX2 §5 의 판별력 증거) · ⓑ · ⓓ 가 키트 표 · 가정과 같다.
- SYN 이 실제 바이너리에서 지나간 문법 (SYN 덱 판독): read_restart 뒤 dt · `erotate/sphere` · `fix ave/time` 출력을 run 사이에 읽기 (f_u_av 를 run 뒤 변수로) · `region … delete` 뒤 다시 정의 · `fix move/mesh` 한 번 정의 → run → `unfix` · `wall/gran/local id force_normal` local 덤프 (고정 주기) · `mesh/stl` 덤프 · 명시 `write_restart`.
- 말하지 않는 것: 본 키트 덱 64 의 실제 바이너리 실행 (0 건 — 첫 실행은 GO 뒤 7:3 Ut0 문법 런) · SYN 이 지나가지 않은 문법 (맨 바깥 `include` + `jump SELF` 이어 돌림 경로 · 변수 주기 덤프 `dump_modify … every v_` · `fix move/mesh` 를 단마다 여러 번 다시 정의) · 생산 침대 S0 의 이력 복원 (본 R 의 몫).
