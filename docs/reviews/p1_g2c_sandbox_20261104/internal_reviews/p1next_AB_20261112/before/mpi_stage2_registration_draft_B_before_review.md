# G2c′ MPI 2 차 등록 — 같은 NP [왕복] · 랭크 경계 고스트 · 이력 지연 크기

> **초안 · 결과 0 건 · 1저자 비준 전 · 내부 반박 리뷰 전** — 2026-11-12 · 문서만 (실행 · 제출 · 리포 변경 없음).
> 트랙 = [DEM 우선] Ⓐ 언로딩 P1 · 자리 = 메모 `docs/reviews/p1_g2c_compare_definition_20261105.md` §5-4 · §7 Q7 (1저자 11-05 *"직렬 결과 + Codex 뒤 정함"* → 11-12 *"권고대로"*).
> 바꾸지 않는 것 = 메모 §2 정의 · §3 판정 식 · 허용폭 · §0-3 직렬 예측 · 11-04 덱 일곱 + BW (바이트) · 직렬 실행기 · 대조기 길 · 키트 · RJ 323957 기록.

| 이번에 닫는 것 | 닫지 않는 것 |
|---|---|
| ① 같은 NP [왕복] (다 · 라) 이 MPI (NP 2 · 4) 에서도 서나 ② 주기 restart 이력 지연 = 1 step 인가 (쓴 NP = 읽는 NP) ③ 스텝 끝 덤프 고스트 재계산 차이 (㉡) 가 랭크 경계 쌍에도 있나 · 몇 쌍 · 크기 | 쓴 NP ≠ 읽는 NP ([NP] · RJ 꼴 24 → 6) · NP 6 (QB1) · 상자 0.05 · 생산 침대 · 벽 이력 · RJ 323957 원인 단정 · 지연이 1 step 아닐 때 몇 step 인지 (QB2) |

## 0. 근거

| 무엇 | 값 | 출처 · 표지 |
|---|---|---|
| 직렬 (11-04 · 11-12) | ㉠ B shear = A(N−1) 3111/3111 · ㉡ C ↔ A 차이 = 주기 표지 334 쌍 전부 · 판정 다 · 라 PASS (11-12) | 메모 §1 · 노트 §7 · 받은 묶음 `…/scratchpad/intake/g2cp_run40000_return_20261112/x/run40000/compare_g2cp.json` (리포 반입 전) |
| RJ 323957 | 원 NP 24 (6×4×1) ↔ 재개 NP 6 (3×2×1) · 법선 실패 3295 쌍 = 전부 원 6×4 고스트 쌍 · 접선 실패 내부 쌍 360969/476046 (76 %) · 한 증분 모형 관측/예측 중앙 33 · R² 0.001 | `docs/reviews/dem_unloading_rj_g2c_cause_20261102/RESULT_20261102.md` · `ibb_result_20261102.json` |
| 직렬 아 (보고 · 11-12) | 지연이 정확히 1 step 인 침대에서도 한 증분 v(N)·dt 모형 기울기 0.0035 · R² 1.1e-4 · 중앙 상대 0.78 (모든 쌍) | 받은 JSON `reports.아` |
| ⇒ 측정 꼴 | 지연 크기 = 이력 열 직접 대조 (B ↔ A(N−1)) — 속도 모형 비로 step 수를 읽지 않는다 (11-02 의 "수십 배" = 보류 그대로 · 11-02 는 내부 고착 쌍이라 부분집합 다름 · 원인 단정 아님) | — |
| 같은 실행 파일 | ibb 생산 `lmp_mpi` md5 0c0daccc2a190d1cf219305bf5286d06 · sha256 ee2d7726… = RJ 323957 manifest `lmp_sha256` (6 행) = 11-12 직렬 1 프로세스 | `docs/reviews/codex_p1_g2c_diagnosis_20261027/run_manifest.user-relayed.txt` 6 행 · 받은 `lmp_identity.txt` |
| mpirun | RJ = conda 환경 myenv 의 mpirun · `--oversubscribe --bind-to none` · slurm_ntasks 6 | 같은 manifest 8 · 12 행 · 키트 `run_unload.sh` 37–39 행 |
| 관찰 | 11-12 덤프 12 = 11-04 덤프 바이트 같음 (실행 파일 · 기계 다름) → 1 프로세스 `lmp_mpi` = 직렬과 같은 결과 (이 침대) | 받은 JSON `predictions.가` (12/15 · 다른 3 = restart `.bin`) |

## 1. 무엇을 · 어디서

| 항목 | 값 |
|---|---|
| 기계 · 큐 | ibb · cpu-60 · 잡 둘 (`-n 2` · `-n 4` · `-N 1` · `-c 1`) |
| 실행 파일 | 위 생산 `lmp_mpi` (`$HOME/LIGGGHTS-PUBLIC/src/lmp_mpi`) · `-h` 확인 = 지금처럼 mpirun 없이 1 프로세스 |
| 침대 | 11-04 덱 일곱 + BW 바이트 그대로 (md5 = `run_40000/inputs.md5` = 11-12 `inputs.md5`) · N 40000 · 건식 N 200 |
| 팔 | 아홉 그대로 (A · A2 · B · B2 · C · BW · BR · CW · CR) — 모두 같은 NP · 같은 격자 |
| 격자 | wrapper 덱으로 명시 (§2 · QB1) |
| ⚠ 같은 침대의 뜻 | 같은 덱 · 같은 씨앗 · MPI 에서 삽입 · 궤적은 직렬 실현과 다를 수 있다 (insert/pack 의 랭크별 분배 = 믹서 `SELF-70` 선례 · 힘 합산 차례) → **모든 비교는 같은 NP 실행 안에서만** |

## 2. NP · 격자 (결과 전 고정)

| NP | 격자 (명시) | 하위영역 x · y (m) ↔ 고스트 절단 0.0045 = 2 r_max + skin [추정] | 랭크 경계 쌍 어림 (표지 0 / 표지 1) | 근거 | 지위 |
|---|---|---|---|---|---|
| 2 | 2 × 1 × 1 | 0.006 · 0.012 (한 번 교환) | 179 / 176 (같은 랭크 표지 1 = 158) | 지시 | 등록 |
| 4 | 2 × 2 × 1 | 0.006 · 0.006 | 328 / 334 | 지시 · 3:7 원 격자와 같은 꼴 (`docs/reviews/dem_unloading_ps45_precheck2_20261009/README.md` §2) | 등록 |
| 6 | 3 × 2 × 1 (= RJ) | **0.004** · 0.006 — x 가 절단보다 작다 → 여러 번 교환 · 3d5c00f 가 받는지 [미확인] | 457 / 334 | RJ manifest np 6 · slurm_ntasks 6 · 격자 3x2x1 (`ibb_result_20261102.json` `rj_screen_processor_grid`) · 키트 기본 NP 6 | QB1 (권고: 뺀다) |
| (기본) | 1 × 1 × NP = z 나눔 [추정 · LAMMPS 면적 최소 규칙 · 3d5c00f 줄 미확인] | — | NP 2 = 0 / 0 (경계 z 0.0195 = 침대 위) · NP 4 (1×1×4) = 145 / 18 | — | 쓰지 않음 |
| 참고 | 원 쓴 NP: 0:10 5 (5×1×1) · 3:7 4 (2×2×1) · 5:5 5 · 7:3 24 (6×4×1) · 10:0 11 | — | — | precheck2 README §2 | 후보 아님 |

- 어림 = 11-12 직렬 침대 (받은 A(N) 원자 · 쌍 덤프 · 쌍 3111 · 원자 1220 = AM_P 10 · AM_S 60 · SE 1150 · z + r 최대 0.0150 m) 를 고른 나눔으로 셈 — MPI 침대는 다른 실현이라 수는 달라진다 (판별력 기대치일 뿐).
- 절단 = `mat.inc` 2 행 skin 0.0005 + 2 × `fresh.inc` 7 행 r 2.0e-3 (산술 · LIGGGHTS 통신 절단 = 이웃 절단 가정 [추정]).

## 3. 결과 전 예측 (NP 2 · 4 각각 · 기준 = 메모 §0-3 · §0-2 그대로 + 아래)

| # | 비교 | 예측 = 맞음 기준 | 이유 (소스 · 덤프 행 순서 · 고스트) | 틀리면 |
|---|---|---|---|---|
| M-나 | B ↔ BW 쌍 · 원자 덤프 바이트 | 2/2 같음 · 보조: A ↔ A2 주기 파일 · A(N) ↔ A2(N) 덤프 · B ↔ B2 덤프 바이트 같음 | 같은 F · NP · 격자 → 같은 setup 길 · 역학에 들어가는 MPI 합산 없음 [추정] · 덤프 행 = 0 번 랭크부터 랭크 차례 + 랭크 안 차례 [미확인] | 그 NP 비트 · 바이트 예측 전부 거둠 · 멈춤 → 1저자 (메모 나 규칙) |
| M-다-값 · M-라-값 | BW → F′ → BR · CW → F′ → CR | 다른 쌍 0 · 다른 원자 0 · 집합 · TIMESTEP · 상자 같음 · 중복 0 | 첫 setup 뒤 상태를 F′ 가 담음 (메모 §0-1 끝) · `write_restart` = 랭크마다 그 랭크 이웃 목록 사본을 원자 배열로 (write_restart.cpp 171–185 · fix_contact_history.cpp 290–298) → 같은 격자 · 주인 → 같은 사본 [추정] | 판정 PASS 면 값 예측만 거둠 · 다른 쌍을 부류 (같은 랭크 · 랭크 경계 · 주기) 로 적음 |
| M-다-바이트 · M-라-바이트 | 같음 | 2/2 | F · F′ 둘 다 재이웃 · exchange 뒤에 쓰임 (주기 step = 재이웃 강제 neighbor.cpp 1359–1361 · 명령 = pbc · exchange · borders 뒤) · read_restart = 쓴 랭크 덩어리 차례대로 그 랭크로 (sort 0 0) [미확인] | 바이트 가설만 거둠 |
| M-다-판정 · M-라-판정 | 메모 §3 식 | PASS | — | FAIL = MPI 에서 G2c′ 를 이대로 못 씀 · 멈춤 · 초안 A ibb 보류 / NOT_COMPUTED = UNCONFIRMED |
| M-라-재현 (가) | C ↔ CW 바이트 | 2/2 | 같은 명령 파일 · 같은 길 (덤프는 `write_restart` 앞) | "CW = C" 거둠 |
| M-가 · M-라-재현 (나) | — | 해당 없음 | NP ≠ 1 · 실행 파일 ≠ 11-04 (메모 §0-3 판정 조건) | — |
| M-마-1 · M-바 · M-사 · M-예외① · ② | 메모 §0-3 · §0-3-1 그대로 | 메모 기준 그대로 | 둘 다 setup · 같은 NP · 명령 파일 = 동기한 H(N) | 메모 규칙 |
| M-마-2 | B shear = A(N−1) · C shear = A(N) (정확) | 다른 쌍 0 · 부류별 수 함께 | 주기 step 재이웃 강제 → 랭크마다 pre_exchange 가 힘 계산 전 사본을 원자 배열로 (fix_contact_history.cpp 305–424) = 직렬과 같은 길 · 덤프되는 사본 = 큰 tag 소유 원자 쪽 (compute_pair_gran_local.cpp 428 · 11-02 보고 §2-2) · 비주기 랭크 경계 쌍의 두 사본 = 비트로 반대 부호 [추정] | 결론 ② 없음 · 부류별 다른 쌍 · 최대 상대차 보고 → 지연 크기 = AH 팔 따로 등록 (QB2) |
| M-마-3 (직렬 꼴 · 판별력) | C ↔ A(N): 주기 표지 0 쌍 30 열 같음 | **틀림** (n_rb > 0 · 0 이면 해당 없음) | 랭크 경계 쌍은 표지 0 인데 스텝 끝 덤프의 고스트 v · ω = 힘 계산 전 통신 값 (verlet.cpp 293 · 299–330 · final_integrate 373 = 소유 원자만) — 주기 고스트와 같은 통신 [추정] | 맞으면 고스트 기전을 랭크 경계로 넓히지 않는다 · RJ 법선 3295 쌍 해석 보류 |
| M-마-3′ (MPI 꼴) | 같음 · 부류 = A(N) 원자 x 와 고른 나눔 | (a) 같은 랭크 · 표지 0 쌍: 30 열 다른 쌍 0 (torque = 같은 방향 행) (b) 모든 쌍: 힘 · 토크 밖 열 다른 쌍 0 (c) 랭크 경계 쌍 (주인 다름 · 표지 0 · 애매 빼고): 힘 다른 쌍 = 전부 (d) 표지 1 쌍: 힘 다른 쌍 = 전부 | step N = 재이웃 강제 → 주인 = x(N) · 경계 = lo + L·k/P [추정] · 애매 = \|x − 경계\| ≤ 1e-12 × L (따로 셈) | (a) · (b) ✗ = 고스트 밖 차이 → 결론 ③ 없음 · 멈춤 → 1저자 / (c) · (d) ✗ = 다른 쌍 몫 · 부류 보고 · "전부" 서술 거둠 |
| M-아 · M-연속 | 보고 | 함께: C 의 kit26 불일치 쌍 부류 ((a) 가 맞으면 ⊆ 고스트 쌍) · 부류별 힘 차 최대 · 중앙 상대 | — | — |

- MPI 에서 **서지 않을** 것 (예측): 직렬 꼴 마-3 (위) · 가 · 라-재현 (나) (해당 없음) · MPI A(N) = 직렬 A(N) (관찰만 · 규칙 없음 · 다를 것 [추정]) · NP 2 ↔ NP 4 비교 (안 함) · 행 차례 = 직렬 차례 (바이트 비교는 같은 NP 안에서만).

## 4. 판정 규칙 · 결론 문 (결과 전 고정)

- 판정 다 · 라 = 메모 §3 식 그대로 (NP 마다 · PASS · FAIL · NOT_COMPUTED · 허용폭 그대로).
- **결론 ①** "같은 NP [왕복] 이 MPI 에서도 선다 (이 침대 · NP 2 · 4)" ⇐ 두 NP 모두 판정 다 · 라 PASS ∧ M-다-값 · M-라-값 맞음.
- **결론 ②** "주기 restart 이력 지연 = 1 step (MPI · 쓴 NP = 읽는 NP · 이 침대)" ⇐ 두 NP 모두 M-마-2 맞음 ∧ n_rb > 0.
- **결론 ③** "스텝 끝 덤프 고스트 재계산 차이가 랭크 경계 쌍에도 있다" ⇐ 두 NP 모두 M-마-3 틀림 ∧ M-마-3′ (a)–(d) 맞음 ∧ n_rb > 0.
- 한 NP 가 기술 실패 · NOT_COMPUTED · n_rb = 0 이면 결론은 다른 NP 만 "NP n 만" 표지 · 두 NP 다면 결론 없음.
- 크기 보고 (판정 아님): 부류별 쌍 수 (같은 랭크 · 랭크 경계 · 표지 1 · 애매) · 랭크 경계 쌍 힘 차 최대 · 중앙 상대 · [연속] kit26 B · C 상태 · 수 · 팔별 초.

## 5. 실행기 변경 명세 (`run_g2cp.sh` · MPI 꼴 덧붙임)

| 자리 | 바뀜 |
|---|---|
| 꼴 고름 | `G2CP_NP` 없음 = 직렬 길 그대로 (코드 · 출력 · 기록 꼴 · 시험 41) · 있음 (빈 값 포함) = MPI 꼴 · 값 ∉ {2, 4} = rc 3 |
| 격자 표 (코드 상수 · 입력 아님) | NP 2 → `2 1 1` · NP 4 → `2 2 1` (QB1 이 6 을 넣으면 `3 2 1`) |
| mpirun | `G2CP_MPIRUN` (없으면 `command -v mpirun`) · 플래그 고정 `--oversubscribe --bind-to none` (RJ · 키트와 같음 · 입력 아님) |
| wrapper 덱 넷 (새 파일 · 샌드박스 폴더) | `MPA.liggghts` = `processors ${PX} ${PY} 1` + `include A.liggghts` · `MPA2` (A2) · `MPR` (R) · `MPBW` (BW) — 주석 · 빈 줄 빼고 두 줄 |
| 팔 명령 | `nice -n 19 timeout -k 30 <한도> "$MPIRUN" --oversubscribe --bind-to none -np "$NP" "$LMPABS" -log <팔>/log.txt -in <wrapper> -var PX <PX> -var PY <PY> <지금 인자 그대로>` · A → MPA · A2 → MPA2 · B · B2 · C · BR · CR → MPR · BW · CW → MPBW |
| 실행 전 멈춤 rc 3 (더함) | NP 꼴 · 집합 밖 · mpirun 없음 · 실행 권한 없음 · `mpirun --version` rc ≠ 0 · `SLURM_JOB_ID` 있으면 `SLURM_NTASKS` = NP (재개 체크리스트 ④ 짝) · wrapper 넷 꼴 · (그대로) `-h` · 덱 일곱 md5 · BW 꼴 · git · OUT 자리 |
| 실행 중 멈춤 rc 4 (더함) | 로그 `Loop time of … on K procs` 의 K 가 모두 NP · 로그에 `  PX by PY by 1 MPI processor grid` 줄 정확히 하나 · 표와 같음 · (그대로) rc · ERROR (`ERROR on proc` 포함) · Loop time · 기대 출력 |
| 기록 (MPI 꼴만 덧붙임 · 이름마다 한 줄 = 메모 규칙 ⑩) | `lmp_identity.txt` 에 `np` · `procs_grid` · `mpirun_path` · `mpirun_realpath` · `mpirun_md5` · `mpirun_version` (첫 줄) · `mpirun_flags` · `slurm_job_id` · `slurm_ntasks` (없으면 `없음`) · `inputs.md5` = wrapper 가 `*.liggghts` 로 자동 |
| 사람 멈춤 · 시간 한도 | 그대로 (직접 자식 timeout 에만 TERM) → timeout 이 mpirun 에 TERM → mpirun 이 랭크에 넘김 [미확인 · Open MPI] · 30 s 뒤 KILL · 남은 랭크 = 잡 끝 SLURM 이 거둠 [추정] |

## 6. 대조기 변경 명세 (`compare_g2cp.py` · MPI 꼴)

| 자리 | 바뀜 |
|---|---|
| 꼴 | `lmp_identity.txt` 에 `np` 줄 있음 = MPI 꼴 (값은 아래 기록 문이 본다 · `np 1` 도 집합 밖 = 막힘) · 없음 = 직렬 (지금 그대로 · 결과 칸 같음) |
| 기록 문 (MPI) | np ∈ 집합 · `procs_grid` = 표 · 팔 아홉 로그의 procs · 격자 줄 = 기록 — 아니면 예측 모두 계산 못 함 · 판정 NOT_COMPUTED + 기술 표지 (규칙 ⑪ 꼴) |
| 덱 문 | 여덟 + wrapper 넷 (md5 = 샌드박스 폴더) |
| 가 · 라-재현 (나) | 판정 조건에 NP = 1 더함 → MPI = 해당 없음 |
| 마-3 · 마-3′ | 직렬 꼴 계산 그대로 (MPI 예측 = 틀림 · n_rb = 0 이면 해당 없음) + 마-3′ 새로 (부류 = `A/post/atom_N` x · 고른 나눔 · 애매 따로) |
| 마-2 · 사 · 예외 · 다 · 라 | 계산 그대로 + 부류별 수 |
| 결론 ①–③ | 두 OUT 의 JSON 을 §4 규칙대로 읽는다 (새 묶음 도구 없음 · 규칙 = 기계적) |

## 7. 시험 먼저 (`test_g2cp.py` · 41 → 49 함수 · 가짜 lmp · 가짜 mpirun · LIGGGHTS · MPI · 네트워크 없이)

| 함수 | 보는 것 | 고치기 전 기대 |
|---|---|---|
| `t44_runner_mpi_calls` | 가짜 mpirun 이 받은 argv (플래그 · `-np N` · LMP · `-log` · `-in <wrapper>` · `-var PX/PY` · 지금 인자) · 팔 아홉 차례 · wrapper 대응 · nice 19 · `-h` = mpirun 없이 | 실패 (mpirun 안 불림) |
| `t45_runner_mpi_identity` | 새 키 아홉 · 이름마다 한 줄 · 직렬 꼴에 새 키 0 | 실패 |
| `t46_runner_mpi_preflight` | rc 3 · OUT 안 만듦 · 가짜 lmp 안 불림: NP 3 · 빈 값 · `2 ` · mpirun 없음 · 권한 없음 · `--version` rc 1 · SLURM_NTASKS 4 ≠ NP 2 · wrapper 한 줄 더함 · wrapper 없음 | 실패 |
| `t47_runner_mpi_run_stops` | rc 4 · STOP: 로그 `on 1 procs` · 격자 줄 없음 · `1 by 2 by 1` · 격자 줄 둘 · mpirun rc 1 · (이름공간 안) 시간 한도의 TERM 이 가짜 mpirun → 가짜 lmp 까지 | 실패 |
| `t48_mpi_wrapper_shape` | wrapper 넷 꼴 · 11-04 덱 일곱 md5 · BW 그대로 | 실패 (파일 없음) |
| `t49_compare_mpi_mode` | 합성 MPI 침대 (지금 모형 + 격자 · 주인 · 랭크 경계 kind · 스텝 끝 덤프의 반 step 고스트 속도를 랭크 경계에도) → MPI 예측 다 맞음 · 음성: 랭크 경계 쌍 하나 같음 → (c) 틀림 · 같은 랭크 쌍 하나 다름 → (a) 틀림 · 직렬 꼴 마-3 = 틀림 · 격자 기록 없음 · 로그 격자 ≠ 기록 → 계산 못 함 · NOT_COMPUTED · 경계 위 원자 → 애매 수 · NP ≠ 1 → 가 해당 없음 | 실패 |
| `t50_serial_unchanged` | 직렬 fixture · 가짜 lmp 직렬 실행의 argv · 기록 · 대조 JSON 칸이 고치기 전 판과 같음 (시각 · 경로 빼고) | 통과 (회귀 기준) |
| `t51_mpi_registration_text` | 이 등록문 (비준 뒤 리포 자리) ↔ 실행기 · 대조기 상수 (집합 · 격자 표 · 플래그 · 애매 폭 · 결론 조건) — t30 꼴 | 실패 |

- 가짜 mpirun (시험 안 · Python): 플래그를 정확히 `--oversubscribe --bind-to none -np N` 로만 받음 (다르면 rc 2) · argv 기록 · `FAKE_NP` 로 가짜 lmp 를 자식으로 · TERM · INT 를 자식에 넘김 · 모드 (mpifail · procs:K · nogrid · badgrid · twogrid).  가짜 lmp: `FAKE_NP` 있으면 로그에 `on N procs` · `  PX by PY by 1 MPI processor grid`.
- 신호 시험 = `unshare -pf --mount-proc --kill-child` 안 · kill = 직접 만든 자식 · pid > 1 · 자기 · 부모 아님 (`SELF-164` 규칙).
- 차례: 새 함수 먼저 (고치기 전 판 = 새 실패 · 옛 41 통과) → 구현 → 49/49 → 변이 (리포 밖 하네스 · 새 규칙마다) → 내부 반박 리뷰 → 게이트 → 커밋.

## 8. ibb 잡 꼴 (11-12 `job_dry.sh` · `job_40000.sh` 와 같은 환경 줄)

```bash
#!/bin/bash
#SBATCH --job-name=g2cp_mpi4
#SBATCH --output=logs/%x_%j.out
#SBATCH --partition=cpu
#SBATCH --qos=cpu-60
#SBATCH -N 1
#SBATCH -n 4
#SBATCH -c 1
#SBATCH --time=03:00:00
source ~/.bashrc
conda activate myenv
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
W=$HOME/g2cp_<날짜>                      # 작업 폴더 · repo/ = 핀 커밋 git archive (11-12 꼴 · PROVENANCE)
N=$1; OUT=$2                              # 건식 = 200 mpi4_dry200 · 샌드박스 = 40000 mpi4_40000
G2CP_NP=4 G2CP_MPIRUN="$(command -v mpirun)" LMP="$HOME/LIGGGHTS-PUBLIC/src/lmp_mpi" \
  bash "$W/repo/docs/reviews/p1_g2c_sandbox_20261104/run_g2cp.sh" "$N" "$W/$OUT"
echo "RUNNER_RC $?"
```

- `job_mpi2.sh` = 같음 · `-n 2` · `G2CP_NP=2` · 이름 `g2cp_mpi2`.  `-n` ↔ `-np` 짝 = 파일 안 · 실행기가 `SLURM_NTASKS` 대조.
- 제출 (작업 폴더에서 · `logs/` 먼저): 건식 `sbatch job_mpi2.sh 200 mpi2_dry200` · `sbatch job_mpi4.sh 200 mpi4_dry200` (1저자 GO) → 건식 판독 (rc · 격자 줄 · procs · 대조기 = 판독 대상 아님) → 샌드박스 `sbatch job_mpi2.sh 40000 mpi2_40000` · `sbatch job_mpi4.sh 40000 mpi4_40000` (1저자 GO 따로).
- 돌려받기 = 11-12 와 같은 꼴 (출력 폴더 · 잡 로그 · PROVENANCE) → `python3 -I compare_g2cp.py <OUT> 40000` (핀 사본).
- 시간 어림: 11-12 직렬 A 29 s · A2 19 s · 재개 1–2 s (받은 `rc.txt`) → NP 마다 2 분 안팎 [추정] · 대기 = cpu-60 차례.

## 9. 멈춤 규칙

- 실행기 rc 3 · 4 = 그 NP 만 멈춤 · 다시 돌리지 않고 보고 (새 빈 폴더 · 1저자 승인 뒤 · README_g2cp 끊김 규칙 · 재개 체크리스트 ⑥).
- 건식 = 판독 대상 아님 · 건식 실패 (rc ≠ 0 · 격자 줄 · procs · `processors` 문법) = 샌드박스 안 냄 → 보고.
- 판독 뒤: M-나 ✗ = 그 NP 비트 예측 전부 거둠 · 멈춤 → 1저자 · M-다 / 라 판정 FAIL = 결론 ① 없음 · 멈춤 · 초안 A ibb 보류 → 1저자 · M-마-3′ (a) · (b) ✗ = 멈춤 → 1저자 · 그 밖 ✗ = 그 서술만 거둠.
- 자동 재실행 · 자동 다음 단계 없음 · 단계마다 1저자 GO (메모 §0-6 Q10 꼴).
- 하지 않는 것: RJ 323957 재실행 · 남은 침대 RJ · 허용폭 · 판정 식 · 키트 파일 · `lmp_auto` · 56 코어 (GO 전) · 11-04 덱 변경 · NP 6 · 교차 NP 팔 (QB1 · QB3 전).

## 10. 주장하지 않는 것

- NP 2 · 4 · 상자 0.012 결과를 RJ (쓴 NP 24 → 읽는 NP 6 · 상자 0.05) 나 키트 NP 6 에 그대로 옮기는 것.
- 쓴 NP ≠ 읽는 NP · NP 바뀜 차이 ([NP] 행).
- 직렬 침대와 같은 실현 · MPI 결정성 (이 실행 · 이 기계 · 같은 NP 밖).
- 벽 이력 (바닥 · 판) · `force_normal` 차이 = 법선 모델 힘.
- RJ 323957 접선 차이의 원인 단정 · 지연이 1 step 이 아닐 때 그 크기 (QB2).
- 고스트 기전의 몫 분해 (부류 · 수 · 크기만).

## 11. 보장 · 작은 반례 (내부 반박 리뷰가 깨 볼 것)

| 보장 | 깨 볼 작은 반례 |
|---|---|
| 팔 아홉 = 같은 NP · 같은 격자 | 한 팔만 wrapper 없이 (기본 격자) · `-np 4` + `processors 2 1 1` · SLURM_NTASKS 2 인데 `-np 4` |
| 부류 = LAMMPS 주인 | 원자가 경계 위 (x = 0.006) · 경계 연산 차례 (0.012/2 ↔ 0.012 × 0.5) · A2 원자로 부류 (A2 의 N 재이웃 여부) |
| 바이트 예측 = 같은 NP 안 | 다른 NP 덤프끼리 바이트 비교가 끼어듦 · 행 차례가 랭크 차례가 아님 |
| 결론 ③ 의 판별력 | n_rb = 0 인데 마-3′ (c) "맞음" · 직렬 꼴 마-3 이 맞는데 결론 ③ |
| 직렬 길 그대로 | `G2CP_NP` 빈 값 · `1` · `02` · 공백 — 직렬로 새면 안 됨 (rc 3) |
| 꼴 판단 = 기록 | MPI 출력에서 `np` 줄만 지우면 직렬 규칙으로 읽힘 — 막이 후보 = 직렬 꼴에도 팔 로그 `on 1 procs` 확인 (넣을지 = 리뷰 · 11-12 로그로 직렬 결과 칸 무변경 확인 뒤) |

## 12. 1저자가 정할 것

- [Ⓐ 언로딩] **QB1** — NP 집합 · 격자.  권고: NP 2 (2×1×1) · NP 4 (2×2×1) 만 · wrapper 로 명시 (기본 격자 = z 나눔 [추정] 이면 NP 2 랭크 경계 0) · NP 6 (RJ 격자) 은 이 상자에서 하위영역 0.004 < 절단 0.0045 [추정] = RJ 와 다른 통신 길이라 빼고, 키트 RJ 의 G2c′ (초안 A) 가 NP 6 을 직접 본다.
- **QB2** — 지연이 1 step 이 아닐 때 쓸 AH 팔 (N−K … N 매 step 이력 덤프 · 같은 궤적) 을 지금 넣을지.  권고: 아니오 (아홉 팔로 먼저 · 결론 ② 가 안 서면 따로 등록).
- **QB3** — 교차 NP 읽기 ([NP] · RJ 꼴) 를 보고 팔로.  권고: 이번 안 함 (같은 NP [왕복] 먼저 · 따로 등록).
- **QB4** — 순서.  권고: 시험 먼저 (실행기 · 대조기 MPI 꼴) → 내부 반박 리뷰 (독립 조수 · Codex 아님 표기) → 건식 NP 2 · 4 → 샌드박스 · 단계마다 1저자 GO.
- **QB5** — 결론 집계.  권고: §4 그대로 (두 NP 모두 맞아야 결론 · 한 NP 실패면 "NP n 만").

## 13. [미확인] · [추정]

- [미확인] MPI 덤프 행 차례 (랭크 차례 + 랭크 안 차례) · read_restart 가 랭크 안 차례를 지킴 — 리포에 3d5c00f `dump.cpp` · `read_restart.cpp` 사본 없음.
- [미확인] wrapper 맨 앞 `processors` (atom_style 앞 · include 바깥) 를 3d5c00f 가 받는지 — 건식이 확인 (키트 R 덱은 read_restart 앞 `processors * * 1` 로 돎 = 선례).
- [미확인] NP 6 (하위영역 < 절단) 동작 · Open MPI 판 · TERM 전달 · KILL 뒤 랭크 · insert/pack MPI 삽입 (수 · 겹침 · 오류).
- [추정] 기본 격자 = z 나눔 · 절단 0.0045 · 고른 나눔 경계식 · 비주기 랭크 경계 쌍 두 사본 = 비트로 반대 부호 · 같은 NP 결정성 · 랭크 경계 쌍 어림 수 (11-12 직렬 침대 · 받은 자료).
- 인용 (이 세션 다시 안 읽음): 고스트 쌍 행 = 큰 tag 쪽 (compute_pair_gran_local.cpp 428) · 통신 = 힘 계산 전만 (verlet.cpp 299–330) — 11-02 보고 §2 · 메모 마-3 의 리포 기록.
- 11-12 숫자 = 받은 묶음 (scratchpad · 리포 반입 전 · 메모 §8 빈칸).
