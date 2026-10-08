# ps73 감쇠 가지 실험 — DEMP-01 (준비 10-07 · WSL t0 1 회 FAIL = 우리 덱 결함 (§12) · 10-08 고침 · B = ibb 10 코어 제출 대기 · **B 미실행** · 예측은 런 전에 적었다)

- **무엇**: ps45 7:3 침대 (`dem_scripts/ps_sweep_6mah_20260914/in.ps_7_3_r45.liggghts` · 압밀 곡선 `docs/data/ps73_compaction_curve_20261006/README.md`) 를
  압축 중 마지막 체크포인트 (step 3,100,000) 에서 갈라, 압축 단계 전역 감쇠 (`fix damp all viscous 0.5`) 가 "300 MPa 도달" 의 정적 의미를 얼마나 바꾸는지 잰다.
- **왜 (DEMP-01 · P1 open)**: 1저자 ibb 실측 (10-07) — 압축 중 감쇠 저항 −0.5·Σv_z = **434.3 N = 목표 판 힘 750 N 의 57.9 %**
  (`docs/data/ps45_plane_load_20261007/ibb_damping_drag_20261007.txt`).  판이 멈추고 감쇠가 1e-5 로 내려가면 정적 망 압력은 **165.3 MPa** 이다.
  ⇒ 이 침대의 공극률 · 두께는 *"정적 300 MPa"* 가 아니라 *"저항이 하중 절반을 진 상태"* 의 값일 수 있다.
- **답하는 갈래 = (B) 서보 유지** (1저자 10-07: B 를 먼저 · A · C 는 플래그 뒤).  (B) 는 압축을 원 프로토콜 그대로 해서 멈춘 step 의 상태를 찍고
  (= A 의 판 고정 상태와 **같은 두께 · 공극률**), 그 다음 판 힘을 750 N 에 붙든 채 감쇠를 이완 값 (1e-5) 으로 내려 망이 300 MPa 를 혼자 질 때까지 둔다
  ⇒ **(B) 하나로 두 숫자가 나온다**: 원 프로토콜 공극률 (멈춘 step) 과 정적 300 MPa 공극률 (서보 유지 끝).
- 실행: **1저자 10-08 결정 = ibb 10 코어 (lmp_mpi · §6-ibb)**.  WSL 은 t0 1 회 (10-07 · lmp_serial 1 코어) 까지 — FAIL, 원인 = 우리 덱 (§12).
  이 컨테이너에는 LIGGGHTS 가 없어 **돌려 보지 못했다** — 문법은 LIGGGHTS-PUBLIC 3d5c00f 소스로 확인했고 (§8), WSL t0 1 회가 가드 정지 경로의 첫 print 전까지
  덱을 실제로 다 지나갔다 (§12).  고친 덱은 **새 SHA256SUMS 로 t0 를 다시** 통과해야 B 가 돈다 (run_branch.sh 기본 = t0 → B).

## 1. 출발점 (숫자마다 근거)

| 항목 | 값 | 근거 |
|---|---|---|
| 체크포인트 | ibb restart_compress_3100000.bin → WSL `~/ps73_branch_20261007/in/restart_compress_3100000.bin` · 80,807,696 B · sha256 `82234bea543ae369043f54d4379c6451cdab5a404213c0ecf0a698638bf4b3ee` | 1저자 10-07 (ibb · WSL 같은 값) |
| step · 원자 | 3,100,000 · 160,420 (원 런 이완 뒤 프레임 3,220,000 = 160,417 = AM 1,656 · SE 158,761 · 잃은 3 개의 종류는 미확인) | r8 로그 · ps45 union 표 (`docs/reviews/codex_ps45_porosity_evidence_20261001/inputs/ps45_lhs_20261001_1825/ps45_lhs_20261001_1825/union/ps45_union.tsv`) |
| 판 높이 | 0.111302 덱 m = 111.302 µm (바닥 z = 0) | 원 런 mesh_3100000.stl (`docs/data/ps73_compaction_curve_20261006/raw/ps73_curve_1.tgz`) |
| KE · 판 압력 | 1.695918e-05 J · 296.17 MPa (3,101,000: 296.35 · 3,105,000: 297.13) | r8 로그 (`raw/ps73_logs.tgz` · output_ps_7_3_r45_r8_220537.out) |
| 원 런 멈춤 | 3,125,000 (3,120,000 은 299.958 MPa = 목표 0.042 MPa 아래 · 3,125,000 은 300.95 MPa) · 두께 111.052 µm | 같은 로그의 판정 줄 · `docs/data/ps73_compaction_curve_20261006/curve/plate.csv` |
| 원 런 이완 | 100,000 step · 판 고정 · viscous 1e-5 → 끝 165.34 MPa · KE 최대 0.0764 J (3,127,000) · **원자 3 개 잃음** (160,420 → 160,417 · 3,128,000–3,130,000) | r8 로그 |
| 출발 형식 | r8 재개 덱 (compress_2650000 → 압축 끝 · 이완 완주 · 검증된 꼴) | 원 덱 9 개 중 r6–r8 이 compress 체크포인트 재개 (압밀 README §2) |

## 2. 갈래

| arm | 압축 (3,100,000 → 목표) | 멈춘 뒤 | 기본 실행 | 무엇에 답하나 |
|---|---|---|---|---|
| t0 | 한 덩어리 (5,000 step · 목표를 0 으로 둔다) | 이완 블록 200 · 서보 500 × 2 · 가드 경로 | ✅ 매번 먼저 (수 분) | 문법 · G1 · G3 · G2 판 메시 · 판 높이 공식 (T0_PZ · 멈춘 step 메시 덤프 대조) · 서보 부호 · 속도 상한 · 파일 |
| **B (주)** | 원 프로토콜 (판 0.01 · viscous 0.5 · 5000 step 마다 판정 0.30 덱 MPa) | **서보 750 N** · vel_max 0.01 (= press_speed) · kp 30 · viscous 1e-5 · 수렴 또는 1.5 M step | ✅ 기본 | DEMP-01 공극률 질문 — 멈춘 step = 원 프로토콜 값 · 끝 = 정적 300 MPa 값 |
| A | 원 프로토콜 | 판 고정 · viscous 1e-5 · 100,000 step (원 런 그대로) | `--arm A` | 재현 (멈춤 step · 이완 165 MPa) — 공극률은 B 의 멈춘 step 과 같다 (판 고정 = 두께 고정) |
| C1 | viscous **0.15** (저항 어림 17 %) · 판 · 판정 같음 | A 와 같은 이완 | `--arm C1` (A · B 완주 뒤만) | 저항이 작으면 같은 판정에서 얼마나 더 눌리나 |
| C2 | viscous **0.05** (저항 어림 6 %) · 판 · 판정 같음 | A 와 같은 이완 | `--arm C2` (A · B 완주 뒤만) | 같은 질문 · 더 깨끗한 시험 |

- **(B) 의 멈춘 step 까지는 (A) 와 같은 덱 줄**이다 (`make_branch_decks.py --selftest` 가 r8 부분열로 확인 · 같은 기계 · 같은 -np 면 비트까지 같을 것으로 본다 — 확인 안 함).
  (A) 는 그 뒤 판을 고정하므로 두께 · 공극률이 멈춘 순간 값에 머문다 ⇒ **A 의 공극률 = B 의 멈춘 step 공극률** — A 는 이완 압력 (165 MPa) 재현에만 필요하다.
- (B) 는 멈춘 step 과 서보 유지 끝 **두 상태 모두** 원자 · 접촉 · 판 메시 덤프를 같은 열로 남긴다 (`stop/` · `end/`) → 같은 도구 (parse_liggghts → plane_load_share · analyze_branch) 로 읽는다.

## 3. 덱 차이 (A 기준 · 전부 `deck_diffs.txt` · 생성기 `make_branch_decks.py`)

| 자리 | r8 | A | B | C1 · C2 |
|---|---|---|---|---|
| read_restart | restart_compress_2650000.bin | `${ckpt}` (3,100,000) | 같음 | 같음 |
| 판 STL · 출력 경로 | plate_ps_7_3_r45_r8.stl · post_ps_7_3_r45/ | `${plate_stl}` · `${out}/post/` (런마다 새 폴더) | 같음 | 같음 |
| shell mkdir -p | 있음 | 뺌 (run_branch.sh 가 만든다 — LIGGGHTS shell mkdir 는 -p 도 폴더로 만든다) | 같음 | 같음 |
| 압축 감쇠 `fix damp all viscous` | 0.5 | 0.5 | 0.5 | **0.15 · 0.05** |
| 압축 고리 (run 5000 · 판정 0.30) | 있음 | 같은 줄 + 덩어리마다 가드 · 기록 (run 사이 · 역학 불변) | 같음 | 같음 |
| 원자 덤프 · restart 간격 (압축) | 5,000 · 50,000 | 같음 | 같음 | 50,000 · 100,000 (출력만) |
| 멈춘 step 스냅숏 | 없음 | 원자 · 접촉 · 판 (`stop/` · run 0 = setup 만) + restart | 같음 | 같음 |
| 멈춘 뒤 | 판 고정 · 1e-5 · run 100000 · 접촉 10,000 | 같음 | **판 → 서보 (fix wall/gran 다시 만듦)** · 1e-5 · 서보 유지 고리 · 원자 50,000 · restart 100,000 | 같음 (접촉 50,000) |
| 끝 스냅숏 | 없음 (원 런 마지막 짝 = 3,220,000) | 원자 · 접촉 · 판 (`end/` · run 0) + restart + 요약 | 같음 | 같음 |
| 가드 정지 | 없음 | 원자 · 새어 나감 · KE · 덩어리 예산 → restart + 요약 · 멈춤 | 같음 + 서보 과도 | 같음 + 감쇠 전환 KE 창 (첫 8 덩어리 · §7) |
| run 뒤 읽는 값 (10-08) | — | 정의 바로 다음 줄에서 얼린다 (같은 step 의 값 · write_restart · run 0 뒤에도 그대로 · §12) | 같음 | 같음 |

- 역학이 바뀌는 줄은 **B 의 판 · 감쇠 전환**과 **C 의 압축 감쇠 값** 뿐이다.  나머지 표지 줄은 run 사이에서 읽고 적기만 한다.
- `run 0` (스냅숏) 은 setup 만 한다 — 같은 위치에서 이웃 목록 · 힘을 다시 계산할 뿐 적분하지 않는다 (덩어리 경계의 run 마다 원래도 setup 이 있다).

## 4. 사전 등록 예측 (2026-10-07 · 런 전)

**어림 모형** (모두 이 침대 · 이 덱 안): 판이 등속 0.01 로 내려가면 입자 속도가 바닥 0 → 판 0.01 로 대략 선형 (affine) 이고,
감쇠 저항 D = γΣv_z 가 침대 높이를 따라 **위에서 아래로 쌓여** 망 응력이 판 300 MPa → 바닥 ≈ 300 − 174 = 126 MPa 로 준다 (D/A = 434.3 N ÷ 0.0025 m² = 173.7 MPa 상당).
층 평균 망 응력 σ̄ = 300.95 − ⅔·173.7 ≈ **185 MPa**.  끝 압축의 기울기 dP/dh = 18.7 MPa/µm (3,050,000–3,120,000 · 저항 일정 가정) 를 층의 하중 곡선 기울기로 쓴다.
공극률 ε_sphere = 1 − 94.446/h (h µm · 고체 부피 236,116 µm³ = 원 런 7:3 프레임 φ_SE + φ_AM 0.85046 × 2500 µm² × 111.052 µm + 잃은 3 개를 SE 로 가정 — 영향 < 0.001 %p).

| # | 예측 (등록) | 허용 · 반증 | 근거 |
|---|---|---|---|
| **B1** | 멈춤 step = 3,125,000 · 두께 111.052 µm · ε_sphere 14.95 % · 판 압력 300.95 ± 0.5 MPa | 멈춤이 3,120,000 이면 "한 덩어리 안 재현" · 그 밖이면 **재현 실패** | r7 (9 코어) ↔ r8 (24 코어) 같은 체크포인트에서 20,000 step 뒤 판 압력 차 0.0056 MPa ≪ 여유 0.042 MPa |
| **B2** | 서보 유지 동안 판이 **내려간다** · 끝 두께 **104.9 µm** (Δh −6.1 µm) · ε_sphere **10.0 %** | 띠 103–107 µm (ε 8.3–11.7 %) · **판이 내려가지 않으면 (Δh ≥ 0) 모형 반증** | (300 − σ̄ 185) ÷ 18.7 = 6.1 µm |
| B3 | 수렴 (\|F/750−1\| ≤ 1 % · 덩어리당 판 이동 ≤ 5e-6 m · 4 연속) · 서보 유지 0.5–1.0 M step (점 0.74 M) | 1.5 M 안 미수렴이면 BUDGET_EXHAUSTED (값은 내되 한정어) | 6.1 µm ÷ vel_max (0.01 µm/1000 step) = 0.61 M + 접근 (kp 30 → τ ≈ 53,000 step) |
| B4 | 단면 하중 (`scripts/plane_load_share.py`): 멈춘 step = **아래로 갈수록 준다** — 가장 위 단면 250–300 · 가운데 150–200 · 가장 아래 110–160 MPa · 보존 검사 CHECK (최대 ÷ 최소 1.6–2.4) / 서보 끝 = 높이마다 300 ± 9 MPa (보존 OK · 무게 기울기 ≈ 2 %) | 멈춘 step 의 단면 하중이 높이에 따라 고르면 (최대 ÷ 최소 < 1.2) 저항 모형 반증 | 위 어림 (가운데 300 − 174 × ¾ ≈ 170) · 이완 프레임 가운데 167.1 MPa (ps45 단면 하중 README) |
| B5 | 서보 시작 뒤 풀림: KE 최대 0.02–0.15 J (첫 10,000 step) · 50,000 step 뒤 ≤ 1e-4 J · 원자 잃음 ≤ 10 · 새어 나감 증가 ≤ 20 | 가드 (§7) 가 멈추면 실패 기록 | 원 런 이완 (KE 0.0764 J · 원자 3) |
| A1 | 멈춤 · 두께 = B1 · 이완 끝 (3,225,000) 판 압력 **165.3 ± 8 MPa** (± 5 %) · 이완 첫 5,000 step 안 최저 ≈ 124 MPa · KE 최대 0.03–0.15 J · 원자 잃음 ≤ 10 | ± 5 % 밖이면 재현 실패 (MPI 분할 차 · 혼돈 — 재개 절차 G3 와 같은 폭) | 원 런 |
| C1 | 멈춤 ≈ 3,560,000 (3.45–3.75 M) · 두께 **106.7 µm** (105.0–108.5 · ε 11.5 % · 10.0–13.0) · 멈춘 step 감쇠 몫 15–20 % · 이완 끝 225–270 MPa | 순서 h_A > h_C1 가 깨지면 반증 | σ̄ = 300.95 − ⅔·52.1 = 266 → (266 − 185)/18.7 = 4.3 µm |
| C2 | 멈춤 ≈ 3,685,000 (3.55–3.85 M) · 두께 **105.5 µm** (104.0–107.0 · ε 10.5 % · 9.2–11.7) · 감쇠 몫 5–7 % · 이완 끝 255–295 MPa | 순서 h_A > h_C1 > h_C2 · \|h_C2 − h_B\| ≤ 1.5 µm 가 깨지면 반증 | σ̄ = 289 → 5.6 µm |
| C3 | 감쇠 전환 뒤 첫 덩어리 끝 KE: C1 ≈ 1e-4 J · C2 ≈ 4e-4 J (점 · 띠 ×0.3–3) 에서 덩어리마다 줄어 8 덩어리 뒤 affine 바닥 (≈ 2e-5 J) 근처 · 그 뒤 압축 KE ≤ 1.7e-3 J · 원자 잃음 ≤ 10 · 터짐 없음 | 가드가 멈추면 "0.15 / 0.05 에서 이 덱은 터진다" 가 결과다 | §9 시간 척도 어림 (SE · 침대 집단 모드가 여전히 과감쇠 — 풀림은 울림이 아니라 기어감) |

- ⚠ 예측의 크기 (6 µm · 10 % 등) 는 **어림** (선형 하중 곡선 · affine 속도 · 저항 일정) 이다 — 등록의 핵심은 **방향** (B · C 가 A 보다 얇다 · 순서 A > C1 > C2 ≳ B) 과 띠다.
- ⚠ 이 실험은 **한 침대 · 한 조성 · 체크포인트 하나**다.  다른 두께 · 조성으로 옮기는 것은 감쇠 몫 어림 N/300,000 (§9) 의 일이지 이 결과의 일이 아니다.
- ⚠ 결과를 본 뒤 띠를 옮기지 않는다 · 결과 뒤 해석이 필요하면 그 사실을 적는다.

## 5. 분석 계획 · 시간 어림

**정의** (`analyze_branch.py` 가 계산 · 표준 라이브러리만):
두께 = 판 메시 높이 (바닥 0) · ε_sphere = 1 − Σ(4/3)πr³ ÷ (0.05 × 0.05 × 판 높이) (웹앱 eps_sphere_web 과 같은 정의) ·
감쇠 저항 = −γΣv_z (그 상태에서 켜진 γ — 멈춘 step = 압축 감쇠 · 끝 = 1e-5) · 판 압력 = 요약 press_deckMPa × 1000.

| 읽을 것 | 자리 | 도구 |
|---|---|---|
| 멈춤 step · 두께 · 판 압력 · 서보 상태 | 런 폴더의 branch_summary.txt (key=value) | run_branch.sh 가 화면에 낸다 |
| 덩어리별 궤적 (step · 판 z · 압력 · 힘 · KE · 원자 · 새어 나감) | branch_trace.csv | 그대로 Origin |
| 두께 · ε_sphere · 감쇠 저항 (멈춤 · 끝) | stop/ · end/ 의 atom_<step> · mesh_<step> | `analyze_branch.py` → analysis_branch.json (run_branch.sh 가 자동) |
| 단면 하중 몫 (멈춤 · 끝) | stop/ · end/ 의 atom · contact · mesh | `scripts/parse_liggghts.py` → `scripts/plane_load_share.py` (§6 명령) |
| 압력–시간 · 두께–시간 | screen.out (thermo 1000 step) · post/ · post_hold/ mesh 덤프 (5,000 step) | `scripts/compaction_curve.py` 꼴 (필요하면) |

- 대조: B 멈춘 step ↔ 원 런 (두께 111.052 · 판 압력 300.95) · B 끝 ↔ B 멈춘 step (Δh · Δε · 단면 하중 고르기) · A 끝 ↔ 원 런 이완 (165.3 MPa) · C ↔ A · B (순서).
- ⚠ 공극률 관례: ε_sphere (구 부피 합) 만 쓴다 — union 과 섞지 않는다 (DEMP-01 질문은 같은 관례 안의 차이다).

**시간 어림** — ibb 실측 (원 로그 Loop time): 24 코어 24.6 step/s (r8) · 9 코어 14.9 (r7) · 4 코어 5.9 (r6) →
**ibb 10 코어 ≈ 16 step/s (어림 · r7 · r8 사이 로그 보간 15.7)** → t0 ≈ 10 분 · B ≈ 13 h (예산 끝 ≈ 27 h).
**WSL 직렬 실측 (10-07 t0 1 회 · lmp_serial 1 코어) ≈ 8.7 step/s** (run_branch.sh 속도 줄 — B 0.75 M ≈ 23.9 h).  어느 기계든 t0 가 5,000 step 덩어리로 재고 run_branch.sh 가 아래를 다시 계산해 보여 준다.

| arm | step | 15 step/s | 20 step/s | 25 step/s | 디스크 |
|---|---|---|---|---|---|
| t0 | 6,200 + setup 5 번 | 수 분 | 수 분 | 수 분 | 0.6 GB |
| **B** | 25,000 + 서보 ≈ 0.74 M (예산 끝 1.5 M) | 13.9 h (28 h) | 10.4 h (21 h) | 8.3 h (17 h) | ≈ 2 GB |
| A | 125,000 | 2.3 h | 1.7 h | 1.4 h | ≈ 4.5 GB (원 런 출력 간격) |
| C1 · C2 | ≈ 0.56 M · 0.69 M | 10 · 13 h | 8 · 10 h | 6 · 8 h | 각 ≈ 2 GB |

- ⚠ thermo 줄에서 같은 step 이 두 번 나오면 (run 경계 · 스냅숏의 run 0) **앞 줄 (정규 줄)** 만 쓴다 — setup 줄의 판 압력은 직전 step 합 + rank 0 의 setup 몫이다
  (직렬 2 배 · 10 rank 면 어림 1.1 배 · §8 · §12).  덱의 기록 값 (요약 · branch_trace.csv) 은 run 0 전에 얼린 값이라 이 영향이 없다.

## 6. WSL 실행 (1저자 · 10-07 t0 1 회까지 — 10-08 부터 B 는 §6-ibb)

```bash
# 0) 체크포인트 복사는 끝났다 (10-07 · sha256 82234bea… 양쪽 확인).  다시 할 때의 꼴만 남긴다 (주소 · 포트는 적지 않는다):
#    scp -P <포트> <ibb 접속>:~/dem_test/ps45/ps_7_3_r45/restart_ps_7_3_r45/restart_compress_3100000.bin ~/ps73_branch_20261007/in/
#    (선택 · G2 원자 대조) 같은 자리의 post_ps_7_3_r45/atom_3100000.liggghts 도 ~/ps73_branch_20261007/in/ 로 받으면 t0 가 원자까지 대조한다
# B 전용 작업 트리 (10-07 밤 고침 · SELF-76) — ~/dem-audit 는 재검증 · 194 체크아웃에 쓰이므로 도는 B 와 분리한다.  커밋마다 새 폴더 · 이미 있는 폴더는 다시 체크아웃하지 않는다
cd ~/dem-audit && git fetch -q origin claude/stoic-knuth-NObVQ && W=~/ps73_branch_src_$(git rev-parse --short FETCH_HEAD) && { [ -d "$W" ] || git worktree add -q --detach "$W" FETCH_HEAD; } && cd "$W" && git log --oneline -1
pgrep -af "lmp_|liggghts" || echo "실행 중인 LIGGGHTS 없음"
sha256sum ~/ps73_branch_20261007/in/restart_compress_3100000.bin      # 82234bea543ae369043f54d4379c6451cdab5a404213c0ecf0a698638bf4b3ee
python3 -I docs/data/ps73_damping_branch_20261007/make_branch_decks.py --check     # 덱 = 생성 결과 · SHA256SUMS

# 1) 0 단계 문법 시험만 (수 분) — LMP 는 ~/lhs_local/lhs00_110/run_lhs00_110.sh 의 mpirun 줄에서 읽는다 (다르면 LMP=… 를 앞에)
#    그 러너가 mpirun 앞에 conda · module 환경을 켠다면 같은 것을 먼저 켠다 (못 찾으면 run_branch.sh 가 그 줄을 보여 주고 멈춘다)
bash docs/data/ps73_damping_branch_20261007/run_branch.sh --t0-only

# 2) t0 PASS 를 본 뒤 본 실행 = t0 + (B) (반나절 ~ 하루) — 창을 닫아도 돈다
nohup bash docs/data/ps73_damping_branch_20261007/run_branch.sh > ~/ps73_branch_20261007/run_B_$(date +%m%d_%H%M).log 2>&1 &

# 1′ · 2′) ★ 1저자 WSL (DESKTOP-IK8J81H) 은 위 1) · 2) 대신 이것 (10-07 밤 · `SELF-97`) — 이 기계는 MPI 경로가 멈춘다
#     (lmp_auto 직접 실행 · mpirun -np 1 둘 다 CPU 0 · 로그 0 바이트 — dem_scripts/mixer_20260921/run_all.sh 머리 주석 · 09-21 실측 · 10-07 밤 재현).
#     run_branch.sh 는 고치지 않는다 (kit SHA256SUMS = 이 실험의 신원 — 바꾸면 통과한 t0 와 덱 묶음 지문이 갈린다) → mpirun 자리에
#     인자 (--oversubscribe · --bind-to X · -np N) 를 버리고 stdbuf 로 lmp_serial 을 바로 실행하는 대리 스크립트를 준다.  t0 PASS 면 B 로 자동.
mkdir -p ~/bin && cat > ~/bin/nompi <<'EOF'
#!/bin/bash
a=(); while [ $# -gt 0 ]; do case "$1" in --oversubscribe) shift;; --bind-to|-np) shift 2;; *) a+=("$1"); shift;; esac; done
exec stdbuf -oL -eL "${a[@]}"
EOF
chmod +x ~/bin/nompi
MPIRUN=~/bin/nompi NP=1 LMP=~/src/LIGGGHTS-PUBLIC/src/lmp_serial nohup bash docs/data/ps73_damping_branch_20261007/run_branch.sh > ~/ps73_branch_20261007/run_tB_$(date +%m%d_%H%M).log 2>&1 &
#     정지는 PID 로만 (pkill -f 금지 · mixer run_all.sh 규약) · 1 코어라 t0 (6,200 step) ≈ 1 h · B (≈ 0.77 M step) ≈ 4–6 일 (ibb 코어당 1.0–1.7 step/s 로 어림 —
#     실측 = screen.out thermo 1,000 step 간격 · run_branch.sh 의 "속도:" 줄은 t0 가 끝난 뒤에 찍힌다)
#     ⚠ 정정 10-08: 실측 = t0 12 분 50 초 · 직렬 ≈ 8.7 step/s (속도 줄) → B ≈ 24 h — 위 "t0 ≈ 1 h · B 4–6 일" 어림은 틀렸다 (ibb 코어당 속도로 어림했는데
#     WSL 한 코어가 더 빨랐다 · §12).  이 기계의 t0 1 회는 덱 결함으로 FAIL 했고 (§12) · B 는 1저자 10-08 결정으로 ibb (§6-ibb).
# 진행 보기 (B_<시각>/ 폴더만 — 끝에 / 를 붙여 .tgz 를 빼고, 마지막 / 는 지운다)
R=$(ls -d ~/ps73_branch_20261007/B_*/ | tail -1); R=${R%/}; tail -3 $R/branch_trace.csv; grep -E "BRANCH_|Hold [0-9]+:" $R/screen.out | tail -4

# 3) B 끝나면 단면 하중 (멈춘 step · 서보 끝)
cd "$(ls -dt ~/ps73_branch_src_* | head -1)"         # B 를 띄운 작업 트리 (가장 최근 것 · scripts/ 가 여기 있다 · 새 창이면 $W 가 없다)
PY=$(ls ~/Yonghoon-DEM-DFT/venv/bin/python ~/Yonghoon-DEM-DFT/.venv/bin/python3 2>/dev/null | head -1)
R=$(ls -d ~/ps73_branch_20261007/B_*/ | tail -1); R=${R%/}
for st in stop end; do S=$(grep "^${st}_step=" $R/branch_summary.txt | tail -1 | cut -d= -f2); \
  $PY scripts/parse_liggghts.py $R/$st/atom_$S.liggghts $R/$st/contact_$S.liggghts $R/$st/mesh_$S.stl -o $R/ana_$st && \
  echo '{"box_x": 0.05, "box_y": 0.05}' > $R/ana_$st/input_params.json; done
echo '{"type_map_resolved": "1:AM_P,2:AM_S,3:SE", "scale": 1000}' > $R/ana_meta.json
for st in stop end; do $PY scripts/plane_load_share.py --case $R/ana_$st --meta $R/ana_meta.json --label B_$st --out $R/plane_$st; done
tar -czf $R.plane.tgz -C $(dirname $R) $(basename $R)/plane_stop $(basename $R)/plane_end && sha256sum $R.plane.tgz

# 4) (선택 · 1저자 결정 뒤) A → C1 → C2 — C 는 A 와 B 가 끝까지 돈 기록이 있어야 run_branch.sh 가 돌린다
# nohup bash docs/data/ps73_damping_branch_20261007/run_branch.sh --skip-t0 --arm A --arm C1 --arm C2 > ~/ps73_branch_20261007/run_AC_$(date +%m%d_%H%M).log 2>&1 &
```

**보낼 것**: run_branch.sh 가 런마다 만드는 `<arm>_<시각>.report.tgz` (요약 · 궤적 · manifest · 화면 · 로그 · 판 메시 · analysis_branch.json — 덤프 · restart 는 WSL 에 둔다) 와
sha256 · (B) 는 `B_<시각>.plane.tgz` 도.  t0 가 FAIL 이면 t0 의 report.tgz 만 보내고 멈춘다 (arm 을 돌리지 않는다 · 덱을 손으로 고치지 않는다).

## 6-ibb. ibb 실행 (1저자 10-08 — *"10 코어로"* · WSL 대신 · Q1 (가) *"아 이게 낫겠다"* = 제출하고 기다린다)

- 러너 = `run_branch_ibb.sbatch` (이 폴더 · 덱 묶음 SHA256SUMS 안) → run_branch.sh 기본 (**t0 → PASS 면 B**) 을 **NP 10 · lmp_mpi**
  (`/lustre/home/yonghoon/LIGGGHTS-PUBLIC/src/lmp_mpi`) · conda myenv (ibb 원 런 러너 · 믹서 러너와 같은 꼴) 로 부른다.
  `#SBATCH -n 10` ↔ run_branch.sh 의 `mpirun --oversubscribe --bind-to none -np 10` 짝 — 래퍼가 SLURM_NTASKS = 10 을 대조하고, t0 가 'Loop time … on 10 procs' 를 본다.
- 작업 폴더 = `~/ps73_branch_20261007_ibb` (새 폴더 · WSL 런과 섞지 않는다) · 체크포인트 = 원본을 **cp 로 사본** (옮기거나 고치지 않는다 · `cp -n` = 있으면 덮지 않는다).
- ⚠ **QOS cpu-60 이 지금 LHS 보충 런으로 60/60** 이다 — 제출하면 **PD 로 기다리다 10 코어가 비면 저절로 시작**한다 (정상 · squeue 이유 칸 QOSMaxCpuPerUserLimit 류).
  **아무 job 도 끄지 않는다** (1저자 10-08 Q1 (가)).  우리 job 을 꺼야 할 때만 그 번호 하나만 끈다 (⑥).
- 시간 어림 (§5): 시작 뒤 t0 ≈ 10 분 → B ≈ 13 h (예산 끝 ≈ 27 h) · 한도 3 일.  등록 예측 (§4) 은 그대로다 — 기계 (WSL → ibb · 1 → 10 rank) 만 바뀌었고 띠는 옮기지 않는다.

```bash
# ibb 에 로그인한 셸에서 (접속 · 포트는 적지 않는다).  ⚠ 아래 줄에는 꺾쇠 자리표시가 없다 — 그대로 붙여 넣는다 (10-02 dev-bo 첫 발사 줄이 꺾쇠를 리다이렉트로 읽어 발사 0)
# ① 리포 사본 (믹서 때와 같은 ~/Yonghoon-DEM-DFT · 경로가 다르면 그 경로) → 이 커밋의 새 작업 트리 (커밋마다 새 폴더 · 이미 있으면 다시 체크아웃하지 않는다)
cd ~/Yonghoon-DEM-DFT && git fetch -q origin claude/stoic-knuth-NObVQ && W=$HOME/ps73_branch_src_$(git rev-parse --short FETCH_HEAD) && { [ -d "$W" ] || git worktree add -q --detach "$W" FETCH_HEAD; } && cd "$W" && git log --oneline -1
K=$W/docs/data/ps73_damping_branch_20261007
conda activate myenv && python3 -I $K/make_branch_decks.py --check      # "✓ check: … SHA256SUMS 일치 (10 파일 · ibb 래퍼 포함)" 가 아니면 멈춘다
# ② 작업 폴더 · 체크포인트 사본 (원본은 읽기만)
R=$HOME/ps73_branch_20261007_ibb && mkdir -p $R/in $R/logs
cp -n ~/dem_test/ps45/ps_7_3_r45/restart_ps_7_3_r45/restart_compress_3100000.bin $R/in/
cp -n ~/dem_test/ps45/ps_7_3_r45/post_ps_7_3_r45/atom_3100000.liggghts $R/in/ || echo "atom_3100000 없음 — t0 의 G2 원자 대조만 빠진다"
sha256sum $R/in/restart_compress_3100000.bin        # 82234bea543ae369043f54d4379c6451cdab5a404213c0ecf0a698638bf4b3ee
# ③ 제출 전 사전 점검 (로그인 노드 · 런 없음 · job 과 같은 환경 · 같은 경로) — 끝 줄 "✓ 사전 점검만 — 통과" 를 본 뒤 ④
bash $K/run_branch_ibb.sbatch $K
# ④ 제출 — 작업 폴더에서 (출력 logs/ 는 제출 폴더 기준) · 기본 = t0 → PASS 면 B
cd $R && JOB=$(sbatch --parsable $K/run_branch_ibb.sbatch $K) && echo "job $JOB"
# ⑤ 기다림 · 진행 — 처음엔 PD 가 정상 (cpu-60 이 차 있다) · 10 코어가 비면 R 로 바뀐다 · 다른 job 은 그대로 둔다
squeue -u $USER
R=$HOME/ps73_branch_20261007_ibb; L=$(ls -t $R/logs/ps73B_*.out 2>/dev/null | head -1); if [ -n "$L" ]; then tail -5 "$L"; else echo "아직 시작 전 (PD)"; fi
B=$(ls -d $R/B_*/ 2>/dev/null | tail -1); B=${B%/}; [ -n "$B" ] && tail -3 $B/branch_trace.csv && grep -E "BRANCH_|Hold [0-9]+:" $B/screen.out | tail -4
# ⑥ 우리 job 만 끌 때 (필요할 때만): scancel $JOB — 새 창이면 squeue -u $USER -n ps73B 로 JOBID 를 보고 그 번호 하나만
```

```bash
# ⑦ B 끝나면 단면 하중 (멈춘 step · 서보 끝) — ibb 에서 (작업 트리의 scripts/ · myenv · 새 창이어도 되게 R · W 를 다시 잡는다)
R=$HOME/ps73_branch_20261007_ibb; W=$(ls -dt $HOME/ps73_branch_src_* | head -1); cd $W && conda activate myenv
B=$(ls -d $R/B_*/ | tail -1); B=${B%/}
for st in stop end; do S=$(grep "^${st}_step=" $B/branch_summary.txt | tail -1 | cut -d= -f2); \
  python3 scripts/parse_liggghts.py $B/$st/atom_$S.liggghts $B/$st/contact_$S.liggghts $B/$st/mesh_$S.stl -o $B/ana_$st && \
  echo '{"box_x": 0.05, "box_y": 0.05}' > $B/ana_$st/input_params.json; done
echo '{"type_map_resolved": "1:AM_P,2:AM_S,3:SE", "scale": 1000}' > $B/ana_meta.json
for st in stop end; do python3 scripts/plane_load_share.py --case $B/ana_$st --meta $B/ana_meta.json --label B_$st --out $B/plane_$st; done
tar -czf $B.plane.tgz -C $R $(basename $B)/plane_stop $(basename $B)/plane_end && sha256sum $B.plane.tgz
# 보낼 것 = $R 의 t0_<시각>.report.tgz · B_<시각>.report.tgz · B_<시각>.plane.tgz + sha256 (WSL 로 가져오는 꼴 · 주소 · 포트는 적지 않는다):
#   mkdir -p ~/ps73_branch_20261007/from_ibb && scp -P <포트> <ibb 접속>:~/ps73_branch_20261007_ibb/*.tgz ~/ps73_branch_20261007/from_ibb/
```

- t0 가 FAIL 이면 job 은 B 를 돌리지 않고 끝난다 (rc 2) — t0 의 report.tgz 와 `logs/ps73B_<JOBID>.out` 만 보낸다 (덱을 손으로 고치지 않는다).

## 7. 가드 (덩어리마다 · run 사이에서만 읽는다 · 걸리면 restart + 요약을 남기고 멈춘다 — 이어 돌리지 않는다)

| 가드 | 문턱 | 왜 |
|---|---|---|
| 원자 잃음 | 시작 원자 − 50 아래 | LIGGGHTS 기본 `thermo_modify lost ignore` — 잃어도 멈추지 않는다 (원 런 이완에서 3 개) |
| 새어 나감 | 중심이 바닥 (z < 0) 아래 + 판 위인 원자 수가 가지 시작보다 100 넘게 늘면 | 1저자 10-07 · real14 는 정지 상태에서 이미 122 개 (시작 값을 기준으로 뺀다) |
| KE (압축) | 1.7e-3 J (= 3,100,000 KE 의 100 배) 초과 · 또는 앞 덩어리의 10 배 초과이면서 1.7e-4 J 초과 | 압축 KE 는 affine 운동 ≈ 1.5e-5 J (질량 0.904 kg · v_p 0.01) 가 바닥 — 원 로그 1.63–1.86e-5 |
| KE (C 의 감쇠 전환 창) | C1 · C2 만: 첫 8 덩어리 (40,000 step) 는 0.1 J 상한만 · 그 뒤 위 규칙 | ⚠ 1저자 지시 (10 배 규칙) 에서 **바꾼 점**: γ 0.5 → 0.05 로 내리면 저항이 받치던 늦음이 과감쇠로 풀려 침대 집단 모드 속도가 처음 (γ0−γ1)/γ1 = 9 배 더해진다 → 첫 덩어리 끝 KE ≈ 1.5e-3 × e^(−5000/4050) ≈ 4e-4 J = 앞 덩어리의 ≈ 26 배 (어림 · C1 은 ≈ 7 배) — 터짐이 아닌데 10 배 규칙이 멈춘다.  0.1 J = 원 런 이완 풀림 최대 (0.0764 J) 위 |
| KE (서보 유지) | 첫 10 덩어리 = 1.0 J (원 런 이완 최대 0.0764 J 의 13 배) · 그 뒤 1e-2 J · 10 배 뜀은 1e-3 J 위에서만 | 감쇠를 내리면 저항이 받치던 응력 기울기가 풀려 KE 가 4,500 배 뛴다 (원 런 실측 · 정상) — 10 배 규칙을 처음부터 쓰면 바로 멈춘다 |
| 서보 과도 | 판 힘 > 1,500 N | 제어 발산 |
| 덩어리 예산 | 압축 40 (A · B) · 400 (C) 덩어리 · 서보 300 덩어리 (1.5 M step) | 끝없이 돌지 않게 — 서보 예산 끝은 가드가 아니라 BUDGET_EXHAUSTED (값은 낸다) |

## 8. LIGGGHTS 문법 근거 (LIGGGHTS-PUBLIC 3d5c00f20519 — ibb · WSL 소스 트리 HEAD 와 같다 · `docs/data/liggghts_add_pair_pin.json`)

원 소스를 raw 로 받아 읽었다 (컨테이너 · 10-07).  줄 번호는 그 커밋 기준.
- 서보 = 메시 모듈 (doc/mesh_module_servo.txt · src/mesh_module_stress_servo.cpp): `target_val` → sp = −값 (173 행) · 오차 = sp − F·axis · 판 속도 = −vel_max·kp·오차/|sp| (502–512) ·
  \|v\| ≤ vel_max (551–563) · move/mesh 와 함께 못 쓴다 (doc · 289 행 nMove 검사) · wall/gran 이 있어야 한다 (293) · vel_max < skin/(2dt) = 1000 (367).
  ⇒ axis 0 0 −1 · target_val +750: 판이 받는 위 방향 힘 F < 750 N 이면 −z 로 내려가고 넘으면 올라간다.  kp 는 무차원 — 오차 1/kp (3.3 %) 넘으면 vel_max.
- 전역 벡터: stress 모듈 9 (힘 3 · 토크 3 · 기준점 3 · src/mesh_module_stress.cpp 432–440 · 헤더 112) + servo 3 (질량중심 · 657) → f_plate_servo[3] = z 힘 · [12] = 판 z ·
  모듈 순서 = 스타일 문자열 순서 (src/fix_mesh_surface.cpp 254–272 · 530–543 — stress 의 MPI 합이 servo 보다 먼저) · 판이 받는 힘 = 입자 힘의 음 (stress 288 행).
- 키워드: FixMesh → stress (모르는 키워드에서 멈춤 · 오류 아님) → servo · 남으면 오류 (fix_mesh_surface 316) — 서보 줄은 file · type · scale · com · ctrlPV · axis · target_val · vel_max · kp 순서.
- 판 바꾸기 순서: 메시에 dump 가 남아 있거나 fix wall/gran 이 남아 있으면 unfix 가 오류 (fix_mesh_surface.cpp 437–451 — "need to unfix fix wall/gran first, then mesh") · move/mesh 가 남아 있어도 오류 (fix_mesh.cpp 447–470)
  ⇒ 덱 순서 = unfix move_press (멈춤) → undump dmp_mesh → unfix zwall_top → unfix top_mesh → 새 판 STL → fix plate_servo → fix zwall_top.  unfix 때 그 메시의 이웃 목록 · 접촉 이력도 지운다 (같은 자리).
- restart: 메시는 restart 자료로 만든다 · 판 STL 은 있기만 하면 된다 (fix_mesh.cpp 405–443 · r8 로그 "INFO: mesh file … data will be taken from restart file") ·
  run 마다 setup 에서 원 위치를 다시 잡는다 (multi_node_mesh_I.h refreshOwned · fix_move_mesh setup · servo setup_pre_force) → 덩어리로 나눈 run 이 이어진다 (원 런 C5 직선 검사와 같은 까닭).
- 덱 언어: `$` 는 따옴표 안에서 줄 읽을 때 치환되지 않고 if · print 가 스스로 치환한다 (src/input.cpp 435–538 · 702–774 · 1010–1023) · if 조건 = 숫자 · 비교 · 논리 · 괄호뿐 (variable.cpp evaluate_boolean 3684–3855) ·
  equal · string 다시 정의 가능 (variable.cpp 305 · 382) · `region ID delete` (domain.cpp 1351) · `count(group,region)` (variable.cpp 2905) · `quit` (input.cpp 1110) ·
  `dump_modify first yes` = 만든 뒤 첫 setup 에서 쓴다 (dump.cpp 526 · output.cpp 229–235) · run 마다 init 에서 모든 시간 의존 compute 에 현재 step 을 건다 (modify.cpp 277 → setup 덤프의 c_strs 유효) ·
  thermo `ke` 를 run 사이에 읽으려면 그 step 에 thermo 가 나와야 한다 (thermo.cpp 972–985 — run 의 마지막 step 은 늘 나온다) · lost 기본 ignore (thermo.cpp 123) · shell mkdir 는 -p 를 폴더로 만든다 (input.cpp 1126–1131).
- ★ **run 사이 읽기 (10-08 · t0 1 회 FAIL 뒤 소스로 확인 · 그때 놓친 것)**: `write_restart` = lmp->init() (write_restart.cpp 171) → Modify::init 이 모든 compute 의 invoked 를 −1 로
  (modify.cpp 271–277) → 다음 run 전까지 thermo `ke` 를 읽으면 ERROR (thermo.cpp 972–985 — 978 = t0 1 회의 ERROR 줄).  위 줄 ("run 의 마지막 step 은 늘 나온다") 은
  run 바로 뒤에만 맞다.  `run 0` 은 메시 응력 합을 지우지 않는다 (지우는 곳 = step 안 pre_force · mesh_module_stress.cpp 249–258) — 그 위에 fix wall/gran setup 이
  이 rank 의 접촉 힘을 더하고 (fix_wall_gran.cpp 681–687 · verlet.cpp Verlet::setup) compute_vector 는 그 합을 돌려준다 (432–437) · run 사이 f_ 읽기에는 시점 검사가 없다
  (variable.cpp 1184 — run 중일 때만) ⇒ **run 0 뒤 f_판[3] = 직전 step 의 MPI 합 + 이 rank 의 몫** (직렬 2 배 — t0 1 회 끝 스냅숏 setup 줄 0.37551816 = 정규 줄 0.1877583 × 2.0000083 ·
  r8 24 rank 이완 setup 줄 0.30893332 = 정규 0.30095234 × 1.0265).  재개 절차 (`docs/resume_ckpt_procedure_20260927.md`) 의 *"setup 줄의 메시 압력은 기준이 못 된다"* 의
  소스 쪽 설명으로 본다 (추정 — 여러 rank 의 몫은 덤프로 재지 않았다 · read_restart 직후 0 은 새 fix 의 f_total_old_ = 0 과 맞는다).
  ⇒ 덱은 run 뒤 읽는 값을 정의 바로 다음 줄에서 얼리고 (생성기 selftest ⑭b) · 기록 값은 run 0 전에 얻는다 · ⑭a 가 덱의 모든 경로 (jump · if) 에서 이 셋 (write_restart 뒤 ke ·
  run 0 뒤 판 힘 · 없는 fix) 을 읽는 곳을 찾는다.

## 9. 왜 0.5 였나 (기록 없음 · 1저자 기억: 낮추면 터짐) · 저항 규모 · 시간 척도 (어림)

- **기록 없음**: 압축 감쇠 0.5 는 리포 수입 커밋 (660600a44) 이전 덱부터 있었고 근거 기록이 없다.  1저자 기억 (10-07): *"감쇠를 낮추면 런이 터졌다"*.  C 갈래가 그 기억을 이 침대에서 재 본다 (가드가 막는다).
- **저항 규모 어림**: affine 이면 D = γΣv_z ≈ γ·N·v_p/2 → 몫 = D/(σ_목표·A) = 0.5 × N × 0.01 / 2 / 750 ≈ **N/300,000** (상자 0.05², 판 속도 0.01) —
  ps45 7:3 N 160,420 → 53 % (실측 57.9 %) · real14 N 3.3 만 → 11 %.  γ 에 비례: 0.15 → 17 % · 0.05 → 6 % (실측 비례 환산).
- **시간 척도 (어림 · 덱 E · ν · 밀도 · hooke 식 characteristicVelocity 2.0 으로 계산 · 접촉 감쇠 e = 0.3 은 그대로)**:

| 양 | γ 0.5 | γ 0.15 | γ 0.05 | γ 1e-5 | 견줄 시간 |
|---|---|---|---|---|---|
| SE 입자 τ = m/γ (m 1.05e-6 kg) | 2.1 µs | 7.0 µs | 21 µs | 0.10 s | SE–SE hooke 접촉 주기 ≈ 193 µs (dt 1e-6 s → 193 step) |
| AM_S 입자 τ (1.61e-4 kg) | 0.32 ms | 1.1 ms | 3.2 ms | 16 s | AM_S–AM_S 접촉 주기 ≈ 173 µs |
| AM_P 입자 τ (1.83e-3 kg) | 3.7 ms | 12 ms | 37 ms | 183 s | — |
| 침대 집단 모드 감쇠비 ζ = γN/(2√(KM)) | 42 | 12.7 | 4.2 | 8.5e-4 | K = M(2π/T)² = 9.9e5 N/m (원 런 이완 링잉 주기 T ≈ 6,000 step · M 0.904 kg) |
| 집단 모드 과감쇠 이완 시간 γN/K | 81,000 step | 24,000 step | 8,100 step | (과감쇠 아님 — 원 런은 6,000 step 주기로 울렸다) | 판이 0.01 µm 를 1,000 step 에 간다 |

  ⇒ SE 는 세 γ 모두 입자 수준 과감쇠 · AM 은 원래부터 감쇠가 아니라 접촉이 잡는다 · 침대 집단 모드는 0.05 까지도 과감쇠 (ζ 4.2) 이고 1e-5 에서만 울린다.
  그래서 C 의 압축 중 터짐 위험은 낮다고 본다 (어림 · 확인은 C 런).  반대로 **0.5 에서는 집단 이완 시간이 81,000 step** 이라 침대가 판을 따라오지 못하고 저항이 하중을 진다 — 이것이 DEMP-01 이다.
  감쇠를 1e-5 로 갑자기 내리는 순간 (원 런 이완 · B 서보 시작) 그 늦음이 풀려 KE 가 뛰고 원자가 몇 개 빠진다 (원 런 실측).

## 10. 확인 안 된 점 (t0 · B 런이 닫을 것)

1. **이 컨테이너에서 한 번도 돌지 않았다** — 덱 문법은 소스 대조 · 생성기 selftest (따옴표 · 변수 · label · if 꼴 · r8 부분열 · ⑭ run 사이 읽기) 까지.  WSL 바이너리가 3d5c00f 와 다르면 (배너로 본다) 서보 동작이 다를 수 있다.
   ✅ 10-07 WSL t0 1 회 (§12) 가 가드 정지 경로의 첫 print 전까지 덱을 실제로 다 지나갔다 (서보 줄 · 판 바꾸기 · 스냅숏 덤프 · restart · jump 포함) — 그 결함 (run 사이 읽기) 은
   소스로 확인 · 고쳤고, 고친 줄 (같은 이름 즉시 치환 — 이미 지나간 `comp_n` · `hold_n` 줄과 같은 꼴 · 부호 있는 판 힘 br_Fz_E) 은 t0 2 회가 확인한다.
2. 서보 전환 때 **판–입자 접촉 이력이 새로 시작**한다 (fix wall/gran 을 다시 만들므로 · 접선 · hysteresis) — 판에 닿은 첫 층의 접선 힘이 0 에서 다시 쌓인다.  하중 방향 (법선 · 적재 중) 은 같은 값이다.
3. kp 30 (τ ≈ 53,000 step) 은 어림 — 판 하중 기울기 4.7e4 N/m (끝 압축) · 원 런 링잉 감쇠 ζ_eff ≈ 0.08 로 안정 한계 τ > 5,800 step 을 셈.  재하 강성이 3 배면 τ ≈ 18,000 step (여유 3 배).
4. 서보 수렴 판정의 5e-6 m (5,000 step 당) 은 남은 두께 오차 ≈ 0.05 µm 에 해당한다 (B2 띠 4 µm 의 1/80).
5. A · C 의 이완 · 끝 스냅숏 (top_mesh) 블록은 t0 에서 200 step 짧게만 지나간다 · C 의 감쇠 값 줄은 숫자만 다르다.
6. 판 높이 기록 (압축 중) 은 덱 공식 (0.111302 − 0.01·dt·Δstep) 이다 — 원 런 C5 (압축 메시가 한 직선) · t0 G2 (mesh_3100000.stl 바이트 대조) · T0_PZ (3,105,000 = 0.111252) ·
   run_branch.sh 의 멈춘 step 대조 (공식 ↔ stop 메시 덤프 6 자리 · t0 는 다르면 FAIL · arm 은 경고) 가 받친다 · 서보 판 높이는 f_plate_servo[12] · 두께 결과는 메시 기준 (analyze_branch.py).
   ⚠ 초판 덱은 가지 시작 step 을 `equal step` 로 두어 공식이 늘 0.111302 를 냈다 (equal 은 쓸 때마다 다시 계산된다) — 커밋 전 자기 검토로 잡아 즉시 치환으로 얼렸고,
   생성기 selftest ⑦b (얼려야 하는 변수 lint) 와 위 메시 대조가 같은 부류를 막는다.
7. 서보 유지가 끝나면 그 상태에서 판을 고정한 이완은 하지 않는다 (등록 밖) — 필요하면 restart_end 에서 따로 등록한다.
8. 서보 유지 중간에 멈추면 이어 돌리는 덱은 아직 없다 — restart_hold_* (100,000 step 마다) 를 남기니, 필요하면 재개 절차 (`docs/resume_ckpt_procedure_20260927.md`) 에 맞춰 따로 만든다.
9. **ibb (lmp_mpi · 10 rank) 은 이 덱의 첫 실행이다** (10-08) — 배너 3.8.0 · 3d5c00f · 'Loop time … on 10 procs' 를 t0 가 본다.  MPI 분할이 원 런 (r8 24 rank) 과 달라 압축 궤적이
   갈라질 수 있다 — B1 의 멈춤 재현 띠 (r7 9 rank ↔ r8 24 rank 같은 체크포인트 20,000 step 뒤 판 압력 차 0.0056 MPa ≪ 여유 0.042) 가 받친다 · 띠는 옮기지 않는다.

## 11. 파일

`make_branch_decks.py` (생성기 · `--check` · `--selftest`) · in.branch_t0_syntax · in.branch_A · in.branch_B · in.branch_C1 · in.branch_C2 (.liggghts) · `plate_branch3100000.stl` (판 STL · 자료는 restart 에서) ·
`run_branch.sh` (러너 · WSL · ibb · `--preflight-only`) · `run_branch_ibb.sbatch` (ibb 제출 래퍼 · 10-08) · `analyze_branch.py` (읽기 전용 분석 · `--selftest`) · `deck_diffs.txt` · `SHA256SUMS` (위 열 개) ·
`t0_run1_20261007/in.branch_t0_syntax.liggghts` (10-07 WSL t0 1 회에 돈 덱 그대로 · sha256 `c0130fd0…` · selftest ⑭c 가 그 결함 자리를 다시 잡는다 · 묶음 SHA256SUMS 밖).

## 12. 실행 기록

### 12-1. t0 1 회 — WSL · 10-07 23:36:49 → 23:49:39 KST · **FAIL (원인 = 우리 덱 · 서보는 설계대로 움직였다)**

| 항목 | 값 | 근거 |
|---|---|---|
| 실행 | 1저자 WSL · lmp_serial 1 코어 · mpirun 자리 대리 `~/bin/nompi` (§6 1′ · 2′ · `SELF-97`) · 작업 트리 ~/ps73_branch_src_aa7ec7fe9 · 덱 묶음 = 커밋 928a40caa 의 SHA256SUMS (t0 덱 sha256 `c0130fd0a5019ca9…` — 사본 `t0_run1_20261007/`) | 1저자 화면 (조정자 전달 10-08) · `docs/session_20260923_progress.md` 10-07 밤 줄 |
| 지나간 곳 | G1 (출발 KE 1.695918e-05 = r8) → 압축 한 덩어리 → 멈춤 스냅숏 → 이완 200 → 끝 스냅숏 (top_mesh) → 서보 전환 → 서보 500 × 2 (BUDGET_EXHAUSTED) → 끝 스냅숏 (서보) → 요약 (`BRANCH_DONE` 찍힘) → … → 가드 정지 경로 첫 print 에서 ERROR | 화면 끝 줄 |
| ERROR | `Compute used in variable thermo keyword between runs is not current (../thermo.cpp:978)` — 가드 정지 print 의 g_ke (살아 있는 `equal ke`) 를 **write_restart 뒤** 읽었다 · write_restart = lmp->init() → compute invoked 초기화 (§8) | 화면 · 소스 · selftest ⑭c 가 그 덱에서 이 자리를 다시 잡는다 |
| 같은 부류 둘째 (오류 없이 지나갔을 자리 · 추정) | T0_SERVO 가 판 힘을 **run 0 뒤** f_plate_servo[3] 로 새로 읽었다 → 직전 합 + setup 몫 (직렬 ≈ 2 × 469 ≈ 939 N) → 'F < 750' 판정이 틀어져 FAIL 로 찍혔을 것 (report 확인 전) | 끝 스냅숏 setup 줄 판 압력 0.37551816 = 정규 줄 0.1877583 × 2.0000083 (화면) · §8 · ⑭c |
| 서보 | **설계대로**: 서보 1,000 step 동안 판 0.111252 → 0.11124201 (Δ 9.99e-6 덱 m = 0.00999 µm ≈ vel_max 0.01 µm / 1,000 step · 포화) · F 469.4 N < 750 N → 아직 내려가는 중 · 힘 부호 + (위) | 화면 `BRANCH_HOLD_DONE` · `BRANCH_END_STATE` · branch_trace.csv 줄 |
| 관찰 (판정 아님 · t0 는 문법 시험) | 3,105,000 에서 판을 멈추고 감쇠를 1e-5 로 내린 뒤 1,200 step (이완 200 + 서보 1,000) 의 3,106,200 판 압력 **187.8 MPa** (469.4 N) ↔ r8 원 로그 3,105,000 (감쇠 0.5 · 판 이동 중) **297.1 MPa** · KE 0.0717 J · 원자 160,420 (잃음 0) · 새어 나감 0.  원 런 이완 (3,125,000 에서 멈춤) 의 1,000 · 2,000 step 뒤 판 압력 204.6 · 151.5 MPa · KE 0.061 · 0.076 J 와 같은 빠른 낙하 (출발 step · 판이 달라 비교는 아니다) | 화면 · r8 로그 (`docs/data/ps73_compaction_curve_20261006/raw/ps73_logs.tgz` · output_ps_7_3_r45_r8_220537.out 3015 · 3042–3044 행) |
| 속도 | 직렬 ≈ **8.7 step/s** (run_branch.sh 속도 줄: B 0.75 M ≈ 23.9 h · 예산 끝 48.5 h · A 4.0 h · C1 17.8 h · C2 21.9 h) — §6 1′ · 2′ 의 "B 4–6 일" 어림은 틀렸다 | 화면 (조정자 전달) |
| 보고 묶음 | t0_20261007_233649.report.tgz · sha256 `9e3a24fc47014efc39f7843974728a45493b2c71c877334cc6d1cc61207c59d0` — 1저자 업로드 예정 (**아직 받지 않음** · 받으면 T0_SERVO 줄 · run_manifest 의 deck_sha256 = `c0130fd0…` 를 대조한다) | — |

### 12-2. 고친 것 (10-08 · 이 README 와 같은 커밋 · 시험 먼저 — 규율 ②)

- **덱**: 덩어리마다 읽는 값 (g_step · g_atoms · g_ke · g_F · g_pz · current_press · t0_n · t0_ke0 · 새 g_Fz) 을 정의 바로 다음 줄에서 같은 이름의 즉시 치환으로 얼린다 ·
  T0_SERVO 는 끝 스냅숏이 run 0 전에 얼린 부호 있는 판 힘 (br_Fz_E) 을 쓴다 · 가지 시작의 g_step · g_atoms 는 얼린 br_step0 · br_n0v 에서.
- **검사** (생성기 selftest — 고치기 전 덱에서 먼저 실패를 봤다): ⑭a 덱의 모든 경로 (jump · if 포함 · 경로마다 상태를 따로) 에서 write_restart 뒤 ke · run 0 뒤 판 힘 · 없는 fix 를
  읽는 곳 — **고치기 전 t0 6 곳 (4 줄: T0_SERVO print · if · 가드 정지 print 둘) · A · B · C1 · C2 0 곳** · ⑭b 살아 있는 equal 정의 다음 줄 = 얼림 (고치기 전 다섯 덱 모두 위반) ·
  ⑭0 합성 덱 17 + ⑭b 2 (검사기 자신) · ⑭c t0 1 회 덱 사본에서 ERROR 자리 (g_ke) 와 T0_SERVO 자리 (t0_Fs) 를 다시 잡는다 · ⑭d `$` 꼴 · ⑮ ibb 래퍼 ↔ 러너 짝 → 고친 뒤 selftest 전부 통과.
- ⇒ **arm 덱 (A · B · C1 · C2) 은 1 회 키트에서도 이 결함에 걸리지 않았다** (⑭a 0 곳 — arm 의 가드 정지는 늘 run 바로 뒤에서 온다).  고친 arm 덱의 차이 = run 사이 variable 줄 · 주석뿐
  (fix · run · dump · restart · 서보 줄 0 줄) → 역학 · 기록 값 같음 (같은 step 의 값을 15 자리로 박는다 · `deck_diffs.txt`).
- **러너**: kit 사본에 래퍼 · t0 가 MPI 프로세스 수를 본다 ('Loop time … on N procs' 의 N = NP — `SELF-97` 의 둘째 항목) · `--preflight-only` · run_manifest 에 SLURM job ·
  모의 시험 9/9 (정상 · 'on 1 procs' 반례 → t0 FAIL · 래퍼 SLURM 밖 = 사전 점검만 · 안 = t0 → B · NTASKS 반례 · 인자 없음 · kit 목록 반례 ·
  `--help` 는 kit 사본을 만들지 않는다 — LIGGGHTS 대신 출력만 흉내 내는 가짜 실행 파일 · 컨테이너).
- ⚠ **덱 묶음 SHA256SUMS 가 바뀌었다** → t0 를 새 묶음으로 **다시** 통과해야 B 가 돈다 (`--skip-t0` 는 같은 묶음의 PASS 만 받는다 · 1 회는 FAIL 이라 어차피 없다).

### 12-3. 1저자 결정 (10-08)

- B 는 **ibb 10 코어** (lmp_mpi) — WSL 아님 (*"10 코어로"*).  t0 도 같은 job 에서 먼저 (§6-ibb).
- Q1 (가) *"아 이게 낫겠다"* = **제출하고 기다린다** — QOS cpu-60 이 LHS 보충 런으로 60/60 이어도 그 job 들을 끄지 않는다 · PD 로 대기 · 시작은 저절로.
