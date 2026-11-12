# G2c′ MPI 2 차 등록 — 같은 NP [왕복] · 랭크 경계 고스트 · 이력 지연 크기

> **초안 · 결과 0 건 · 1저자 비준 전 · Codex 설계 확인 전 · 내부 반박 리뷰 1 · 2 회차 반영 (11-12 · Codex 아님 · 1 회차 `docs/reviews/p1_g2c_sandbox_20261104/internal_reviews/p1next_AB_20261112/review1_AB.md` → `docs/reviews/p1_g2c_sandbox_20261104/internal_reviews/p1next_AB_20261112/disposition1_AB.md` · 2 회차 `docs/reviews/p1_g2c_sandbox_20261104/internal_reviews/p1next_AB_20261112/review2_AB.md` → `docs/reviews/p1_g2c_sandbox_20261104/internal_reviews/p1next_AB_20261112/disposition2_AB.md`)** — 2026-11-12 · 문서만 (실행 · 제출 · 리포 변경 없음).  고치기 전 판 = `mpi_stage2_registration_draft_B_before_review2.md` (sha256 앞 12 `cc3f6b4af2f7`) · 1 회차 전 판 = `mpi_stage2_registration_draft_B_before_review.md` (`e3a2d3481c83`).
> 트랙 = [DEM 우선] Ⓐ 언로딩 P1 · 자리 = 메모 `docs/reviews/p1_g2c_compare_definition_20261105.md` §5-4 · §7 Q7 (1저자 11-05 *"직렬 결과 + Codex 뒤 정함"* → 11-12 *"권고대로"*).
> 바꾸지 않는 것 = 메모 §2 정의 · §3 판정 식 · 허용폭 · §0-3 직렬 예측 · 11-04 덱 일곱 + BW (바이트) · 직렬 실행기 · 대조기 길 · 키트 · RJ 323957 기록.
> GO = 단계마다 1저자 (샌드박스 = 생산 침대 아님 · 11-12 직렬과 같은 꼴 · 코드 리뷰 = 내부 반박 리뷰 · Codex 아님 — 1저자 11-10) · 설계 = Codex 설계 확인 (초안 A 와 함께 · 비준 뒤 · 구현 전 · Codex 지금 남은 한 번 — 1저자 11-12) · 이 B 의 결과 = 초안 A 의 RJ 발사 GO 요청 (Codex · 리셋 약 11-15 뒤 · A 15-9 ⑧) 에 붙인다 — 샌드박스 GO (1저자) 와 RJ 발사 GO (Codex) 는 따로.
> 리포 경로 표지: 11-12 결과 = 대피 세션 커밋 L `bfd9b3bbd` (가린 사본 `docs/reviews/p1_g2c_sandbox_20261104/run_ibb_40000_20261112/` · 메모 §8) — 이 컨테이너 원격 추적 ref (`ef68eb7da`) 에 없음 = push 전 → 아래 그 경로 = **push 뒤 경로**.  덤프 · 로그 원본 = 리포 밖 (받은 묶음 sha256 3caf3e05… · 그 폴더 README 3 행).

| 이번에 닫는 것 | 닫지 않는 것 |
|---|---|
| ① 같은 NP [왕복] (다 · 라) 이 MPI (NP 2 · 4) 에서도 서나 ② 주기 restart 이력 지연 = 1 step 인가 (쓴 NP = 읽는 NP) ③ 스텝 끝 덤프 고스트 재계산 차이 (㉡) 가 랭크 경계 쌍에도 있나 · 몇 쌍 · 크기 | 쓴 NP ≠ 읽는 NP ([NP] · RJ 꼴 24 → 6) · NP 6 (QB1) · 상자 0.05 · 생산 침대 · 벽 이력 · RJ 323957 원인 단정 · 지연이 1 step 아닐 때 몇 step 인지 (QB2) |

## 0. 근거

| 무엇 | 값 | 출처 · 표지 |
|---|---|---|
| 직렬 (11-04 · 11-12) | ㉠ B shear = A(N−1) 3111/3111 · ㉡ C ↔ A 차이 = 주기 표지 334 쌍 전부 · 판정 다 · 라 PASS (11-12) | 메모 §1 · 노트 §7 · `docs/reviews/p1_g2c_sandbox_20261104/run_ibb_40000_20261112/compare_g2cp.json` `judgment` · 메모 §8 (push 뒤 경로) |
| RJ 323957 | 원 NP 24 (6×4×1) ↔ 재개 NP 6 (3×2×1) · 법선 실패 3295 쌍 = 전부 원 6×4 고스트 쌍 · 접선 실패 내부 쌍 360969/476046 (76 %) · 한 증분 모형 관측/예측 중앙 33 · R² 0.001 | `docs/reviews/dem_unloading_rj_g2c_cause_20261102/RESULT_20261102.md` · `ibb_result_20261102.json` |
| 직렬 아 (보고 · 11-12) | 지연이 정확히 1 step 인 침대에서도 한 증분 v(N)·dt 모형 기울기 0.0035 · R² 1.1e-4 · 중앙 상대 0.78 (모든 쌍) | 같은 JSON `reports.아` |
| ⇒ 측정 꼴 | 지연 크기 = 이력 열 직접 대조 (B ↔ A(N−1)) — 속도 모형 비로 step 수를 읽지 않는다 (11-02 의 "수십 배" = 보류 그대로 · 11-02 는 내부 고착 쌍이라 부분집합 다름 · 원인 단정 아님) | — |
| 같은 실행 파일 | ibb 생산 `lmp_mpi` md5 0c0daccc2a190d1cf219305bf5286d06 · sha256 ee2d7726… = RJ 323957 manifest `lmp_sha256` (6 행) = 11-12 직렬 1 프로세스 | `docs/reviews/codex_p1_g2c_diagnosis_20261027/run_manifest.user-relayed.txt` 6 행 · `docs/reviews/p1_g2c_sandbox_20261104/run_ibb_40000_20261112/lmp_identity.txt` 3 · 4 행 |
| mpirun | RJ = conda 환경 myenv 의 mpirun · `--oversubscribe --bind-to none` · slurm_ntasks 6 | 같은 manifest 8 · 12 행 · 키트 `run_unload.sh` 37–39 행 |
| 관찰 | 11-12 덤프 12 = 11-04 덤프 바이트 같음 (실행 파일 · 기계 다름) → 1 프로세스 `lmp_mpi` = 직렬과 같은 결과 (이 침대) | 같은 JSON `predictions.가` (12/15 · 다른 3 = restart `.bin`) · 메모 §8 225 행 |
| 11-12 로그 꼴 (받은 묶음 · 리포 밖) | 팔 아홉 모두 `Loop time … on 1 procs` (A · A2 두 줄 · 나머지 한 줄) · `1 by 1 by 1 MPI processor grid` 한 줄씩 · 치환된 `read_restart <경로>` = **로그 파일** (`-log <팔>/log.txt`) 에만 (BR `log.txt` 11 행 `read_restart ${RFILE}` · 12 행 치환) · 화면 (`<팔>/out.txt`) = `Reading restart file ...` 뿐 (BR `out.txt` 2 행 · 경로 없음 — 명령 메아리 = 로그 · 덱에 `echo` 없음 · 3d5c00f 소스 줄 [미확인]) | 받은 묶음 `<팔>/log.txt` · `<팔>/out.txt` (sha256 3caf3e05… 묶음 안) |

## 1. 무엇을 · 어디서

| 항목 | 값 |
|---|---|
| 기계 · 큐 | ibb · cpu-60 · 잡 둘 (`-n 2` · `-n 4` · `-N 1` · `-c 1`) |
| 실행 파일 | 위 생산 `lmp_mpi` (`$HOME/LIGGGHTS-PUBLIC/src/lmp_mpi`) · `-h` 확인 = 지금처럼 mpirun 없이 1 프로세스 |
| 침대 | 11-04 덱 일곱 (`compare_g2cp.py` DECKS7) + BW 바이트 그대로 — md5: 일곱 = `run_40000/inputs.md5` 2–8 행 · BW = `run_ibb_40000_20261112/inputs.md5` 의 `BW.liggghts` 줄 (8 행 · = 샌드박스 `BW.liggghts` 70d395e8… · 11-04 기록엔 BW 없음) · 새 출력의 대조 = 파일 이름으로 (행 번호 아님 · §7 t50) · N 40000 · 건식 N 200 |
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

- 어림 = 11-12 직렬 침대 (받은 묶음 · 리포 밖 · A(N) 원자 · 쌍 덤프 · 쌍 3111 · 원자 1220 = AM_P 10 · AM_S 60 · SE 1150 · z + r 최대 0.0150 m) 를 고른 나눔으로 셈 — 내부 반박 리뷰 1 회차가 같은 덤프로 다시 셈 = 같음 (`docs/reviews/p1_g2c_sandbox_20261104/internal_reviews/p1next_AB_20261112/rb_count.py`) · MPI 침대는 다른 실현이라 수는 달라진다 (판별력 기대치일 뿐).
- **애매** = 쌍의 원자 하나라도 어느 랭크 경계 (lo + L·k/P) 에서 \|x − 경계\| ≤ 1e-12 × L — 그 쌍은 부류 (a) · (c) 에서 빼고 따로 센다 (11-12 직렬 침대 = 0 · 같은 산술).
- 절단 = `mat.inc` 2 행 skin 0.0005 + 2 × `fresh.inc` 7 행 r 2.0e-3 (산술 · LIGGGHTS 통신 절단 = 이웃 절단 가정 [추정]).

## 3. 결과 전 예측 (NP 2 · 4 각각 · 기준 = 메모 §0-3 · §0-2 그대로 + 아래)

| # | 비교 | 예측 = 맞음 기준 | 이유 (소스 · 덤프 행 순서 · 고스트) | 틀리면 |
|---|---|---|---|---|
| M-나 | B ↔ BW 쌍 · 원자 덤프 바이트 | 2/2 같음 · 보조: A ↔ A2 주기 파일 · A(N) ↔ A2(N) 덤프 · B ↔ B2 덤프 바이트 같음 | 같은 F · NP · 격자 → 같은 setup 길 · 역학에 들어가는 MPI 합산 없음 [추정] · 덤프 행 = 0 번 랭크부터 랭크 차례 + 랭크 안 차례 [미확인] | 그 NP 비트 · 바이트 예측 전부 거둠 · 멈춤 → 1저자 (메모 나 규칙) |
| M-다-값 · M-라-값 | BW → F′ → BR · CW → F′ → CR | 다른 쌍 0 · 다른 원자 0 · 집합 · TIMESTEP · 상자 같음 · 중복 0 | 첫 setup 뒤 상태를 F′ 가 담음 (메모 §0-1 끝) · `write_restart` = 랭크마다 그 랭크 이웃 목록 사본을 원자 배열로 (write_restart.cpp 171–185 · fix_contact_history.cpp 290–298) → 같은 격자 · 주인 → 같은 사본 [추정] | 판정 PASS 면 값 예측만 거둠 · 다른 쌍을 부류 (같은 랭크 · 랭크 경계 · 주기 · 애매) 로 적음 · 결론 ① 없음 (§4) |
| M-다-바이트 · M-라-바이트 | 같음 | 2/2 | F · F′ 둘 다 재이웃 · exchange 뒤에 쓰임 (주기 step = 재이웃 강제 neighbor.cpp 1359–1361 · 명령 = pbc · exchange · borders 뒤) · read_restart = 쓴 랭크 덩어리 차례대로 그 랭크로 (sort 0 0) [미확인] | 바이트 가설만 거둠 |
| M-다-판정 · M-라-판정 | 메모 §3 식 | PASS | — | FAIL = MPI 에서 G2c′ 를 이대로 못 씀 · 멈춤 · 초안 A ibb 보류 / NOT_COMPUTED = UNCONFIRMED |
| M-라-재현 (가) | C ↔ CW 바이트 | 2/2 | 같은 명령 파일 · 같은 길 (덤프는 `write_restart` 앞) | "CW = C" 거둠 |
| M-가 · M-라-재현 (나) | — | 해당 없음 | NP ≠ 1 · 실행 파일 ≠ 11-04 (메모 §0-3 판정 조건) | — |
| M-마-1 · M-바 · M-사 · M-예외① · ② | 메모 §0-3 · §0-3-1 그대로 | 메모 기준 그대로 | 둘 다 setup · 같은 NP · 명령 파일 = 동기한 H(N) | 메모 규칙 |
| M-마-2 | B shear = A(N−1) · C shear = A(N) (정확) | 다른 쌍 0 · 부류별 수 함께 | 주기 step 재이웃 강제 → 랭크마다 pre_exchange 가 힘 계산 전 사본을 원자 배열로 (fix_contact_history.cpp 305–424) = 직렬과 같은 길 · 덤프되는 사본 = 큰 tag 소유 원자 쪽 (compute_pair_gran_local.cpp 428 · 11-02 보고 §2-2) · 비주기 랭크 경계 쌍의 두 사본 = 비트로 반대 부호 [추정] | 결론 ② 없음 · 부류별 다른 쌍 · 최대 상대차 보고 → 지연 크기 = AH 팔 따로 등록 (QB2) |
| M-마-3 (직렬 꼴 · 판별력) | C ↔ A(N): 주기 표지 0 쌍 30 열 같음 | **틀림** (n_rb > 0 · 0 이면 해당 없음) | 랭크 경계 쌍은 표지 0 인데 스텝 끝 덤프의 고스트 v · ω = 힘 계산 전 통신 값 (verlet.cpp 293 · 299–330 · final_integrate 373 = 소유 원자만) — 주기 고스트와 같은 통신 [추정] | 맞으면 고스트 기전을 랭크 경계로 넓히지 않는다 · RJ 법선 3295 쌍 해석 보류 |
| M-마-3′ (MPI 꼴 · 대조기 JSON 키 `마-3p`) | 같음 · 부류 = A(N) 원자 x 와 고른 나눔 | (a) 같은 랭크 · 표지 0 · 애매 아닌 쌍: 30 열 다른 쌍 0 (torque = 같은 방향 행) (b) 모든 쌍: 힘 · 토크 밖 열 다른 쌍 0 (c) 랭크 경계 쌍 (주인 다름 · 표지 0 · 애매 아닌 쌍): 힘 다른 쌍 = 전부 (d) 표지 1 쌍: 힘 다른 쌍 = 전부 · 애매 쌍 = (a) · (c) 밖 수만 ((b) · (d) 에는 그대로) | step N = 재이웃 강제 → 주인 = x(N) · 경계 = lo + L·k/P [추정] · 애매 폭 = §2 | (a) · (b) ✗ = 고스트 밖 차이 → 결론 ③ 없음 · 멈춤 → 1저자 / (c) · (d) ✗ = 다른 쌍 몫 · 부류 보고 · "전부" 서술 거둠 |
| M-아 · M-연속 | 보고 | 함께: C 의 kit26 불일치 쌍 부류 ((a) 가 맞으면 ⊆ 고스트 쌍) · 부류별 힘 차 최대 · 중앙 상대 | — | — |

- MPI 에서 **서지 않을** 것 (예측): 직렬 꼴 마-3 (위) · 가 · 라-재현 (나) (해당 없음) · MPI A(N) = 직렬 A(N) (관찰만 · 규칙 없음 · 다를 것 [추정]) · NP 2 ↔ NP 4 비교 (안 함) · 행 차례 = 직렬 차례 (바이트 비교는 같은 NP 안에서만).

## 4. 판정 규칙 · 결론 문 (결과 전 고정)

- 판정 다 · 라 = 메모 §3 식 그대로 (NP 마다 · PASS · FAIL · NOT_COMPUTED · 허용폭 그대로).
- n_rb (NP 마다) = 부류 (c) 쌍 수 (표지 0 · 주인 다름 · 애매 뺌).
- **결론 ①** "같은 NP [왕복] 이 MPI 에서도 선다 (이 침대 · NP 2 · 4)" ⇐ 두 NP 모두 판정 다 · 라 PASS ∧ M-다-값 · M-라-값 맞음.
- **결론 ②** "주기 restart 이력 지연 = 1 step (MPI · 쓴 NP = 읽는 NP · 이 침대)" ⇐ 두 NP 모두 M-마-2 맞음 ∧ n_rb > 0.
- **결론 ③** "스텝 끝 덤프 고스트 재계산 차이가 랭크 경계 쌍에도 있다" ⇐ 두 NP 모두 M-마-3 틀림 ∧ M-마-3′ (a)–(d) 맞음 ∧ n_rb > 0.
- **부분 결론 없음** — 결론마다 두 NP 모두 조건을 채울 때만 선다.  한 NP 라도 기술 실패 · 기록 문 · 완료 문 실패 · NOT_COMPUTED · FAIL · 조건 ✗ 이면 그 결론은 없다 (다른 NP 결과 = 보고 · "NP n 만" 결론 없음) · n_rb = 0 은 결론 ② · ③ 에만 걸린다 (① 은 n_rb 와 무관).
- **초안 A 의 선행 조건 = 결론 ① 그대로** — 판정 PASS 인데 M-값 틀림 = 선행 조건 아님 → 멈춤 → 1저자 (결과 전 · 11-12).
- **결론에 쓰는 출력 = §9 시도 셈** (2 회차 · 결과 전) — NP 마다 첫 내용 판정 시도 하나 · 두 NP 가 다른 작업 폴더에서 와도 됨 (B 구현 커밋 · `comparator_md5` · 실행 파일 md5 · 덱 md5 (일곱 + BW + wrapper 넷) 가 같을 때만) · 내용 판정이 난 NP 를 다시 돌려 결론을 세우지 않는다.
- 크기 보고 (판정 아님): 부류별 쌍 수 (같은 랭크 · 랭크 경계 · 표지 1 · 애매) · 랭크 경계 쌍 힘 차 최대 · 중앙 상대 · [연속] kit26 B · C 상태 · 수 · 팔별 초.
- **점검표** (결과 전 · 판독 = 칸을 두 OUT 의 대조기 JSON 키 그대로 옮김 · 해석 없음):

| 칸 | JSON (NP 마다) | NP 2 | NP 4 |
|---|---|---|---|
| 앞 조건 | `run_gate.ok` · `deck_gate.ok` · `mpi_gate.ok` (§6 기록 문) = 참 | ☐ | ☐ |
| ① | `judgment.다.status` · `judgment.라.status` = PASS · `predictions.다-값.status` · `predictions.라-값.status` = 맞음 | ☐ | ☐ |
| ② | `predictions.마-2.status` = 맞음 · `mpi.n_rb` > 0 | ☐ | ☐ |
| ③ | `predictions.마-3.status` = 틀림 · `predictions.마-3p.status` = 맞음 ((a)–(d) 모두) · `mpi.n_rb` > 0 | ☐ | ☐ |

- 결론 = 앞 조건 ∧ 그 행이 두 NP 모두 ☑ 일 때만.

## 5. 실행기 변경 명세 (`run_g2cp.sh` · MPI 꼴 덧붙임)

| 자리 | 바뀜 |
|---|---|
| 꼴 고름 | `G2CP_NP` 없음 = 직렬 길 그대로 (코드 · 출력 · 기록 꼴 · 시험 41) · 있음 (빈 값 포함) = MPI 꼴 · 값 ∉ {2, 4} = rc 3 |
| 격자 표 (코드 상수 · 입력 아님) | NP 2 → `2 1 1` · NP 4 → `2 2 1` (QB1 이 6 을 넣으면 `3 2 1`) |
| mpirun | `G2CP_MPIRUN` (없으면 `command -v mpirun`) · 플래그 고정 `--oversubscribe --bind-to none` (RJ · 키트와 같음 · 입력 아님) |
| wrapper 덱 넷 (새 파일 · 샌드박스 폴더) | `MPA.liggghts` = `processors ${PX} ${PY} 1` + `include A.liggghts` · `MPA2` (A2) · `MPR` (R) · `MPBW` (BW) — 주석 · 빈 줄 빼고 두 줄 |
| 팔 명령 | `nice -n 19 timeout -k 30 <한도> "$MPIRUN" --oversubscribe --bind-to none -np "$NP" "$LMPABS" -log <팔>/log.txt -in <wrapper> -var PX <PX> -var PY <PY> <지금 인자 그대로>` · A → MPA · A2 → MPA2 · B · B2 · C · BR · CR → MPR · BW · CW → MPBW |
| 실행 전 멈춤 rc 3 (더함) | NP 꼴 · 집합 밖 · **MPI 꼴인데 `SLURM_JOB_ID` 없음 (MPI 꼴 = SLURM 잡 안에서만 · 남은 랭크는 잡 끝이 거둔다)** · mpirun 없음 · 실행 권한 없음 · `mpirun --version` rc ≠ 0 · `SLURM_NTASKS` = NP 아님 (재개 체크리스트 ④ 짝) · wrapper 넷 꼴 · (그대로) `-h` · 덱 일곱 md5 · BW 꼴 · git · OUT 자리 |
| 실행 중 멈춤 rc 4 (더함) | 로그 `Loop time of … on K procs` 의 K 가 모두 NP · 로그에 `  PX by PY by 1 MPI processor grid` 줄 정확히 하나 · 표와 같음 · (그대로) rc · ERROR (`ERROR on proc` 포함) · Loop time · 기대 출력 |
| 기록 (MPI 꼴만 덧붙임 · 이름마다 한 줄 = 메모 규칙 ⑩) | `lmp_identity.txt` 에 `np` · `procs_grid` · `mpirun_path` · `mpirun_realpath` · `mpirun_md5` · `mpirun_version` (첫 줄) · `mpirun_flags` · `slurm_job_id` · `slurm_ntasks` · `inputs.md5` = wrapper 가 `*.liggghts` 로 자동 (`run_g2cp.sh` 171 행) |
| 사람 멈춤 · 시간 한도 | 그대로 (직접 자식 timeout 에만 TERM) → timeout 이 mpirun 에 TERM → mpirun 이 랭크에 넘김 [미확인 · Open MPI] · 30 s 뒤 KILL · 남은 랭크 = 잡 끝 SLURM 이 거둠 [추정] · STOP 뒤 남은 랭크가 OUT 에 쓸 수 있음 [미확인] → 돌려받을 때 `find mpi2_40000 -newer mpi2_40000/STOP.txt -type f` (NP 4 는 `mpi4_40000`) 결과를 묶음에 (있으면 보고 · 판정은 완료 문 ⑪ 이 이미 막음) |

## 6. 대조기 변경 명세 (`compare_g2cp.py` · MPI 꼴)

| 자리 | 바뀜 |
|---|---|
| 꼴 | `lmp_identity.txt` 에 `np` 줄 있음 = MPI 꼴 (값은 아래 기록 문이 본다 · `np 1` 도 집합 밖 = 막힘) · 없음 = 직렬 — **두 꼴 모두 팔 아홉 로그를 본다**: 직렬 = `Loop time … on 1 procs` 만 · `1 by 1 by 1 MPI processor grid` 줄 정확히 하나 (11-12 로그 아홉 = 그 꼴 → 직렬 결과 칸 무변경) · 어긋나면 예측 모두 계산 못 함 · 판정 NOT_COMPUTED + 기술 표지 (규칙 ⑪ 꼴) · JSON 새 칸 `comparator_md5` (이 대조기 파일 md5 — 옛 핀 `21bb09d8` 대조기는 MPI 출력을 직렬로 읽는다 → MPI 출력 판독 = B 구현 커밋 판만) |
| 기록 문 (MPI) | np ∈ 집합 · `procs_grid` = 표 · 팔 아홉 로그의 procs · 격자 줄 = 기록 — 아니면 예측 모두 계산 못 함 · 판정 NOT_COMPUTED + 기술 표지 (규칙 ⑪ 꼴) · 결과 = `mpi_gate.ok` |
| 덱 문 | 여덟 + wrapper 넷 (md5 = 샌드박스 폴더) |
| 가 · 라-재현 (나) | 판정 조건에 NP = 1 더함 → MPI = 해당 없음 |
| 마-3 · 마-3′ | 직렬 꼴 계산 그대로 (MPI 예측 = 틀림 · n_rb = 0 이면 해당 없음) + 마-3′ (키 `마-3p`) 새로 (부류 = `A/post/atom_N` x · 고른 나눔 · 애매 = (a) · (c) 밖 따로) · `mpi.n_rb` |
| 마-2 · 사 · 예외 · 다 · 라 | 계산 그대로 + 부류별 수 |
| 결론 ①–③ | §4 점검표 칸을 두 OUT 의 JSON 에서 그대로 옮긴다 (새 묶음 도구 없음 · 해석 없음 · 부분 결론 없음) |

## 7. 시험 먼저 (`test_g2cp.py` · 41 → 49 함수 · 가짜 lmp · 가짜 mpirun · LIGGGHTS · MPI · 네트워크 없이)

| 함수 | 보는 것 | 고치기 전 기대 |
|---|---|---|
| `t44_runner_mpi_calls` | 가짜 mpirun 이 받은 argv (플래그 · `-np N` · LMP · `-log` · `-in <wrapper>` · `-var PX/PY` · 지금 인자) · 팔 아홉 차례 · wrapper 대응 · nice 19 · `-h` = mpirun 없이 | 실패 (mpirun 안 불림) |
| `t45_runner_mpi_identity` | 새 키 아홉 · 이름마다 한 줄 · 직렬 꼴에 새 키 0 | 실패 |
| `t46_runner_mpi_preflight` | rc 3 · OUT 안 만듦 · 가짜 lmp 안 불림: NP 3 · 빈 값 · `2 ` · `SLURM_JOB_ID` 없음 (`G2CP_NP=2`) · mpirun 없음 · 권한 없음 · `--version` rc 1 · SLURM_NTASKS 4 ≠ NP 2 · wrapper 한 줄 더함 · wrapper 없음 | 실패 |
| `t47_runner_mpi_run_stops` | rc 4 · STOP: 로그 `on 1 procs` · 격자 줄 없음 · `1 by 2 by 1` · 격자 줄 둘 · mpirun rc 1 · (이름공간 안) 시간 한도의 TERM 이 가짜 mpirun → 가짜 lmp 까지 | 실패 |
| `t48_mpi_wrapper_shape` | wrapper 넷 꼴 · 11-04 덱 일곱 md5 · BW 그대로 | 실패 (파일 없음) |
| `t49_compare_mpi_mode` | 합성 MPI 침대 (지금 모형 + 격자 · 주인 · 랭크 경계 kind · 스텝 끝 덤프의 반 step 고스트 속도를 랭크 경계에도) → MPI 예측 다 맞음 · 음성: 랭크 경계 쌍 하나 같음 → (c) 틀림 · 같은 랭크 쌍 하나 다름 → (a) 틀림 · 직렬 꼴 마-3 = 틀림 · 격자 기록 없음 · 로그 격자 ≠ 기록 → 계산 못 함 · NOT_COMPUTED · 경계 위 원자 → 애매 수 · (a) · (c) 에서 빠짐 (경계 위 쌍이 (a) 를 깨지 않음) · NP ≠ 1 → 가 해당 없음 · 직렬 꼴 로그 문: `on 2 procs` · 격자 줄 없음 · 둘 → 계산 못 함 · `np` 줄만 지운 MPI 출력 → 직렬로 읽히지 않음 (계산 못 함) | 실패 |
| `t50_serial_unchanged` | 직렬 fixture · 가짜 lmp 직렬 실행의 argv · 기록 · 대조 JSON 칸이 고치기 전 판과 같음 — 빼는 것 (결과 전 목록): 시각 · 경로 · 새 칸 `comparator_md5` · `inputs.md5` 의 wrapper 넷 줄 (`MPA` · `MPA2` · `MPBW` · `MPR` `.liggghts` — 직렬 길에서도 `*.liggghts` glob 이 잡는다 · `run_g2cp.sh` 171 행) · 바뀐 세 파일 (`run_g2cp.sh` · `compare_g2cp.py` · `test_g2cp.py`) 의 `inputs.md5` 줄 · `inputs.md5` 대조 = 파일 이름으로 (행 번호 아님 — wrapper 가 끼면 `R.liggghts` · `probe.liggghts` 와 그 뒤 줄이 밀린다 · glob 정렬 = 로캘 의존 [추정]) | 통과 (회귀 기준) |
| `t51_mpi_registration_text` | 이 등록문 (비준 뒤 리포 자리) ↔ 실행기 · 대조기 상수 (집합 · 격자 표 · 플래그 · 애매 폭 · 결론 조건 · 점검표 JSON 키) — t30 꼴 | 실패 |

- 가짜 mpirun (시험 안 · Python): 플래그를 정확히 `--oversubscribe --bind-to none -np N` 로만 받음 (다르면 rc 2) · argv 기록 · `FAKE_NP` 로 가짜 lmp 를 자식으로 · TERM · INT 를 자식에 넘김 · 모드 (mpifail · procs:K · nogrid · badgrid · twogrid).  가짜 lmp: `FAKE_NP` 있으면 로그에 `on N procs` · `  PX by PY by 1 MPI processor grid` · 직렬 꼴도 `  1 by 1 by 1 MPI processor grid` 한 줄 (11-12 실제 로그 꼴 · 지금 가짜 lmp 엔 없음 — `test_g2cp.py` 1193 행 근처) — 대조기 직렬 로그 문 뒤에도 옛 41 이 통과하도록 가짜 lmp 를 먼저 실제 꼴로.
- 신호 시험 = `unshare -pf --mount-proc --kill-child` 안 · kill = 직접 만든 자식 · pid > 1 · 자기 · 부모 아님 (`SELF-164` 규칙).
- 차례: 새 함수 먼저 (고치기 전 판 = 새 실패 · 옛 41 통과) → 구현 → 49/49 → 변이 (리포 밖 하네스 · 새 규칙마다) → 내부 반박 리뷰 → 게이트 → 커밋.
- 초안 A 의 차등 시험은 새 파일 (`test_g2cp_kitdiff.py`) 이라 이 파일과 겹치지 않는다 · 이 대조기 고침 뒤 그 차등 시험을 다시 (직렬 판정 함수 무변경 = t50).

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
W="${SLURM_SUBMIT_DIR:?SLURM 밖}"          # 작업 폴더 = 제출 폴더 (~/g2cp_mpi_r1 · repo/ = 핀 커밋 git archive · PROVENANCE · 11-12 꼴)
[ -f "$W/repo/docs/reviews/p1_g2c_sandbox_20261104/run_g2cp.sh" ] || { echo "repo/ 없음: $W"; exit 3; }
N=$1; OUT=$2                              # 건식 = 200 mpi4_dry200 · 샌드박스 = 40000 mpi4_40000
G2CP_NP=4 G2CP_MPIRUN="$(command -v mpirun)" LMP="$HOME/LIGGGHTS-PUBLIC/src/lmp_mpi" \
  bash "$W/repo/docs/reviews/p1_g2c_sandbox_20261104/run_g2cp.sh" "$N" "$W/$OUT"
echo "RUNNER_RC $?"
```

- `job_mpi2.sh` = 같음 · `-n 2` · `G2CP_NP=2` · 이름 `g2cp_mpi2`.  `-n` ↔ `-np` 짝 = 파일 안 · 실행기가 `SLURM_NTASKS` 대조.
- 작업 폴더 = `~/g2cp_mpi_r1` (새 시도 = `~/g2cp_mpi_r2` … · 11-12 `~/g2cp_20261112` 꼴 · `repo/` · `PROVENANCE.txt` · `logs/` 먼저) · 잡은 제출 폴더를 작업 폴더로 쓴다 (꺾쇠 자리표 없음 · REG 113 · 470 행 꼴).
- 제출 (작업 폴더에서): 건식 `sbatch job_mpi2.sh 200 mpi2_dry200` · `sbatch job_mpi4.sh 200 mpi4_dry200` (1저자 GO) → 건식 판독 (rc · 격자 줄 · procs · 대조기 = 판독 대상 아님) → 샌드박스 `sbatch job_mpi2.sh 40000 mpi2_40000` · `sbatch job_mpi4.sh 40000 mpi4_40000` (1저자 GO 따로).
- 돌려받기 = 11-12 와 같은 꼴 (출력 폴더 · 잡 로그 · PROVENANCE · §5 의 `find … -newer STOP.txt` (STOP 있을 때)) → `python3 -I repo/docs/reviews/p1_g2c_sandbox_20261104/compare_g2cp.py mpi2_40000 40000` · `… mpi4_40000 40000` (B 구현 커밋 판 · JSON `comparator_md5` 로 확인).
- 시간 어림: 11-12 직렬 A 29 s · A2 19 s · 재개 1–2 s (`docs/reviews/p1_g2c_sandbox_20261104/run_ibb_40000_20261112/rc.txt`) → NP 마다 2 분 안팎 [추정] · 대기 = cpu-60 차례.

## 9. 멈춤 규칙

- 실행기 rc 3 · 4 = 그 NP 만 멈춤 · 다시 돌리지 않고 보고 (새 빈 폴더 · 1저자 승인 뒤 · README_g2cp 끊김 규칙 · 재개 체크리스트 ⑥).
- 건식 = 판독 대상 아님 · 건식 실패 (rc ≠ 0 · 격자 줄 · procs · `processors` 문법) = 샌드박스 안 냄 → 보고.
- 판독 뒤: M-나 ✗ = 그 NP 비트 예측 전부 거둠 · 멈춤 → 1저자 · M-다 / 라 판정 FAIL = 결론 ① 없음 · 멈춤 · 초안 A ibb 보류 → 1저자 · 판정 PASS ∧ M-다-값 · M-라-값 틀림 = 결론 ① 없음 · 멈춤 → 1저자 (초안 A 선행 조건 아님 · §4) · M-마-3′ (a) · (b) ✗ = 멈춤 → 1저자 · 그 밖 ✗ = 그 서술만 거둠.
- 결론 = §4 점검표 그대로 (부분 결론 없음) · 한 NP 의 기술 실패 · NOT_COMPUTED = 그 결론 없음 → 그 NP 다시 = 새 빈 폴더 · 1저자 승인 (자동 없음 · 아래 시도 셈).
- **시도 셈 (2 회차 · 결과 전)**: 시도 = 작업 폴더 하나 (`~/g2cp_mpi_r1` · `~/g2cp_mpi_r2` …) 안의 그 NP 샌드박스 출력 (`mpi<NP>_40000`) · 건식 = 셈 밖 (판독 대상 아님 · 건식 다시 = 1저자).  다시 돌림 = 그 NP 의 마지막 시도가 기술 실패 (실행기 rc ≠ 0 · 앞 조건 `run_gate` · `deck_gate` · `mpi_gate` ✗) · NOT_COMPUTED 일 때만 · 새 빈 작업 폴더 · 1저자 승인 · **한도 = NP 마다 2 시도** (셋째 = 새 등록).  **내용 판정** (판정 PASS · FAIL · 예측 맞음 · 틀림) 이 난 NP 는 다시 돌리지 않는다 — FAIL · 값 틀림 · M-나 ✗ · M-마-3′ (a) · (b) ✗ = 멈춤 → 1저자 · 같은 등록으로 다시 돌려 결론 ① 을 세우지 않는다 (다시 = 새 등록).  결론 ①–③ 에 쓰는 출력 = NP 마다 첫 내용 판정 시도 하나 · 두 NP 가 다른 작업 폴더에서 와도 됨 — B 구현 커밋 · `comparator_md5` · 실행 파일 md5 · 덱 md5 (일곱 + BW + wrapper 넷) 가 같을 때만 (아니면 그 결론 없음 → 1저자).
- 자동 재실행 · 자동 다음 단계 없음 · 단계마다 1저자 GO (메모 §0-6 Q10 꼴).
- 하지 않는 것: RJ 323957 재실행 · 남은 침대 RJ · 허용폭 · 판정 식 · 키트 파일 · `lmp_auto` · 56 코어 (GO 전) · 11-04 덱 변경 · NP 6 · 교차 NP 팔 (QB1 · QB3 전).

## 10. 주장하지 않는 것

- NP 2 · 4 · 상자 0.012 결과를 RJ (쓴 NP 24 → 읽는 NP 6 · 상자 0.05) 나 키트 NP 6 에 그대로 옮기는 것.
- 쓴 NP ≠ 읽는 NP · NP 바뀜 차이 ([NP] 행).
- 직렬 침대와 같은 실현 · MPI 결정성 (이 실행 · 이 기계 · 같은 NP 밖).
- 벽 이력 (바닥 · 판) · `force_normal` 차이 = 법선 모델 힘.
- RJ 323957 접선 차이의 원인 단정 · 지연이 1 step 이 아닐 때 그 크기 (QB2).
- 고스트 기전의 몫 분해 (부류 · 수 · 크기만).
- 한 NP 만 선 결과를 결론으로 (§4 · 부분 결론 없음).

## 11. 보장 · 작은 반례 (구현 뒤 내부 반박 리뷰 · Codex 설계 확인이 깨 볼 것)

| 보장 | 깨 볼 작은 반례 |
|---|---|
| 팔 아홉 = 같은 NP · 같은 격자 | 한 팔만 wrapper 없이 (기본 격자) · `-np 4` + `processors 2 1 1` · SLURM_NTASKS 2 인데 `-np 4` · SLURM 밖 MPI 꼴 |
| 부류 = LAMMPS 주인 | 원자가 경계 위 (x = 0.006 → 애매 · (a) 를 깨지 않는가) · 경계 연산 차례 (0.012/2 ↔ 0.012 × 0.5) · A2 원자로 부류 (A2 의 N 재이웃 여부) |
| 바이트 예측 = 같은 NP 안 | 다른 NP 덤프끼리 바이트 비교가 끼어듦 · 행 차례가 랭크 차례가 아님 |
| 결론 ③ 의 판별력 | n_rb = 0 인데 마-3′ (c) "맞음" · 직렬 꼴 마-3 이 맞는데 결론 ③ |
| 부분 결론 없음 | NP 4 NOT_COMPUTED + NP 2 PASS → 결론 ① 이 서는가 (서면 안 됨 · 초안 A 선행 조건도 안 섬) · 판정 PASS ∧ M-값 틀림 → 선행 조건이 서는가 · n_rb = 0 이 결론 ① 을 막는가 (막으면 안 됨) |
| 직렬 길 그대로 | `G2CP_NP` 빈 값 · `1` · `02` · 공백 — 직렬로 새면 안 됨 (rc 3) |
| 꼴 판단 = 기록 + 로그 | MPI 출력에서 `np` 줄만 지움 → 직렬 로그 문 (`on 1 procs` · `1 by 1 by 1` 한 줄) 에서 막히는가 · 11-12 직렬 출력 = 결과 칸 무변경인가 |
| 시도 셈 (§9) | NP 4 시도 1 FAIL → 시도 2 PASS 를 결론에 씀 (안 됨) · NP 2 r1 PASS + NP 4 r2 PASS (r1 = 기술 실패 · 같은 구현 · 대조기 · 실행 파일 · 덱 md5) → 결론 ① 섬 · 대조기 md5 다른 두 시도 섞임 → 결론 없음 · 같은 NP 셋째 시도 (새 등록 없이) |
| t50 회귀 기준 | wrapper 넷이 놓인 폴더의 직렬 출력 `inputs.md5` 를 행 번호로 대조 (거짓 실패) · 빼는 목록에 없는 줄이 바뀜 (잡혀야) |

## 12. 1저자가 정할 것 (1저자 11-12 결정 반영 · 이번 고침이 바꾼 것만 다시 물음 — 이번엔 없음)

| 질문 | 내용 · 권고 | 1저자 11-12 | 이번 고침 (2 회차) | 지금 |
|---|---|---|---|---|
| QB1 | NP 집합 · 격자 · 권고 = NP 2 (2×1×1) · NP 4 (2×2×1) 만 · wrapper 로 명시 (기본 격자 = z 나눔 [추정] 이면 NP 2 랭크 경계 0) · NP 6 (RJ 격자) 은 이 상자에서 하위영역 0.004 < 절단 0.0045 [추정] = RJ 와 다른 통신 길이라 빼고 키트 RJ 의 G2c′ (초안 A) 가 NP 6 을 직접 본다 | 권고대로 [확인 표지 — 지시서의 정한 목록 (QA1 · QA2 · QA4 · QA6 · QA7 · QB4 · QB5) 에 없음 · 1저자 11-12 "P1 QA · QB = 고침이 권고를 안 바꾸면 권고대로" (세션 기록) 로 읽음] | 그대로 | 정함 (메인 확인) |
| QB2 | 지연이 1 step 이 아닐 때 쓸 AH 팔 (N−K … N 매 step 이력 덤프 · 같은 궤적) 을 지금 넣을지 · 권고 아니오 (아홉 팔로 먼저 · 결론 ② 가 안 서면 따로 등록) | 〃 | 그대로 | 정함 (메인 확인) |
| QB3 | 교차 NP 읽기 ([NP] · RJ 꼴) 를 보고 팔로 · 권고 이번 안 함 (같은 NP [왕복] 먼저 · 따로 등록) | 〃 | 그대로 | 정함 (메인 확인) |
| QB4 | 순서 · GO · 권고 = 시험 먼저 (실행기 · 대조기 MPI 꼴) → 내부 반박 리뷰 (독립 조수 · Codex 아님 표기) → 건식 NP 2 · 4 → 샌드박스 · 단계마다 1저자 GO (샌드박스 = 생산 침대 아님 · 11-12 직렬과 같은 GO 꼴) | 권고대로 | 차례 맨 앞에 **비준 → Codex 설계 확인 (A · B 함께 · 구현 전)** 을 끼움 = 1저자 11-12 Codex 계획 그대로 (권고 바뀜 아님) · 이 B 결과 = A 의 RJ 발사 GO 요청 (Codex · 리셋 뒤) 에 붙임 | 정함 |
| QB5 | 결론 집계 · 권고 = §4 그대로 — 결론마다 두 NP 모두 조건을 채울 때만 · 부분 결론 ("NP n 만") 없음 · n_rb > 0 은 ② · ③ 에만 · 초안 A 의 선행 조건 = 결론 ① 그대로 | 권고대로 | 보탬 = §9 시도 셈 (결론에 쓰는 출력 = NP 마다 첫 내용 판정 시도 · 한도 NP 마다 2 · 섞기 = 같은 구현 · 대조기 · 실행 파일 · 덱 md5 일 때만 · 내용 판정 난 NP 다시 안 돌림) — 권고 방향 그대로 (결과 뒤 옮길 길을 막는 쪽) | 정함 (보탬 = B 비준에 포함) |

- 순서 (QB4 + 1저자 11-12): 비준 (A 와 함께) → Codex 설계 확인 (A 15-13 · 이 §14) → 시험 먼저 (§7 · 새 함수 먼저 실패 확인) → 구현 → 49/49 · 변이 → 내부 반박 리뷰 → 게이트 → 커밋 → 건식 NP 2 · 4 (1저자 GO) → 샌드박스 NP 2 · 4 (1저자 GO 따로) → §4 점검표 → (리셋 뒤) A 의 Codex RJ 발사 GO 요청에 붙임.

## 13. [미확인] · [추정]

- [미확인] MPI 덤프 행 차례 (랭크 차례 + 랭크 안 차례) · read_restart 가 랭크 안 차례를 지킴 — 리포에 3d5c00f `dump.cpp` · `read_restart.cpp` 사본 없음.
- [미확인] wrapper 맨 앞 `processors` (atom_style 앞 · include 바깥) 를 3d5c00f 가 받는지 — 건식이 확인 (키트 R 덱은 read_restart 앞 `processors * * 1` 로 돎 = 선례).
- [미확인] NP 6 (하위영역 < 절단) 동작 · Open MPI 판 · TERM 전달 · KILL 뒤 랭크 (STOP 뒤 OUT 변화 = 보고 · §5) · insert/pack MPI 삽입 (수 · 겹침 · 오류).
- [추정] 기본 격자 = z 나눔 · 절단 0.0045 · 고른 나눔 경계식 · 비주기 랭크 경계 쌍 두 사본 = 비트로 반대 부호 · 같은 NP 결정성 · 랭크 경계 쌍 어림 수 (11-12 직렬 침대 · 받은 묶음).
- 인용 (이 세션 다시 안 읽음): 고스트 쌍 행 = 큰 tag 쪽 (compute_pair_gran_local.cpp 428) · 통신 = 힘 계산 전만 (verlet.cpp 299–330) — 11-02 보고 §2 · 메모 마-3 의 리포 기록.
- 11-12 숫자 = 커밋 L `bfd9b3bbd` 의 가린 사본 · 메모 §8 (push 뒤 경로 · 머리 표지) · 덤프 · 로그 = 받은 묶음 (리포 밖).
- [미확인] 명령 메아리가 로그 파일에만 찍히는 3d5c00f 소스 줄 (받은 11-12 화면 · 로그로 본 것 · §0) · `*.liggghts` glob 정렬 순서 (로캘 · §7 t50 은 이름 대조라 무관).

## 14. Codex 설계 확인 요청서용 — 이번에 닫는 것 / 닫지 않는 것 (B · 1저자 11-12 "지금 남은 한 번" · 초안 A 15-13 과 한 요청)

| 이번에 닫는 것 (설계 · 결과 0 건 · 구현 전) | 닫지 않는 것 |
|---|---|
| NP 집합 · 격자 (§2 · QB1) · 같은 침대의 뜻 = 같은 NP 실행 안 비교만 (§1) | 구현 (실행기 · 대조기 · 시험 = 이 확인 뒤) · MPI 실행 결과 (0 건) |
| 결과 전 예측 · 서지 않을 것 (§3) · 판정 · 결론 ①–③ · 점검표 · 부분 결론 없음 (§4) | NP 6 (QB1 · 키트 RJ 가 직접) · 교차 NP 읽기 (QB3) · 지연이 1 step 아닐 때 크기 (QB2 · AH 팔) |
| 시도 셈 · 한도 · 결론에 쓰는 시도 · 내용 판정 뒤 다시 안 돌림 (§9 · 2 회차) | 생산 침대 · 상자 0.05 · RJ 323957 원인 · 결론을 RJ · 키트 NP 6 에 옮기는 것 (§10) |
| 실행기 · 대조기 MPI 꼴 명세 (§5 · §6 · 직렬 길 무변경 · 로그 문 · `comparator_md5`) · 시험 먼저 목록 (§7 · 41 → 49 · t50 빼는 목록) · 잡 꼴 · 멈춤 (§8 · §9) | 초안 A 의 RJ 발사 GO (Codex · 리셋 뒤 · 이 B 결과 붙여 · A 15-9 ⑧) |
