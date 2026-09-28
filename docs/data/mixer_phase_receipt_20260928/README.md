# 믹서 재개-위상 영수증 (2026-09-28) — v2 ibb · v1 WSL · v0

## ★ v2 (ibb) — `receipt_v2_ibb.json` (09-28 오후) · LH 가 잇는 영수증

**1저자 ibb 원본을 한 바이트도 고치지 않고** 넣었다 (ibb → WSL scp → 업로드 · 1저자 WSL 사본 sha256 = 업로드 파일 sha256).

```
sha256  f2724c4afd5572f6f90579212274d7c8f6dc756cb99399f141f1822478702a17
크기    29,800 B
생성    ibb SLURM job 235118 (sbatch -n 1) · host node01 · sealed_at 2026-09-28T14:19:04.717690+09:00
```

| 양 | 값 | 비고 |
|---|---|---|
| `schema` · `passed` · `reasons` | `restart_phase_v2` · **true** · `[]` | 소비자 (`load_phase_receipt`) 는 v2 만 받는다 |
| `angle_error_deg` (최대) | **1.9219 × 10⁻⁵ °** | A 208 + B 81 = 289 step |
| `angle_bound_deg` | **0.0011651 °** | = 해상도 0.0011459 + 실측 오차 (합 — `HBR4-03`) |
| `pos_bound_m` | **3.165 × 10⁻⁷ m** | = (형상 잔차 5.137 × 10⁻⁸ + 출력 반올림 1.314 × 10⁻⁷) × √3 — 검사기가 부호거리에 더한다.  ⚠ 상별 규모 (Codex 5 차 HBR5-06): 겹침률 불확실성 100·u/r = AM_P 0.046 · AM_S 0.105 · **SE 0.418 %p** (1 % 문턱의 41.8 % — *"반경의 ≈ 0.03 %"* 는 AM 에만 맞다) · 회전각 항 별도 |
| `symmetric_gap_deg` | **3.8722 °** | 가장 가까운 다른 위상 후보 — 판별력 = 이것 ÷ 오차 ≈ 20 만 배 |
| `nfacet` · `dumps_n` A / B | 39 · 208 / 81 | |
| `motion_clock` | mover 셋 (Drum · Front · Back) 385,337 · 끝 9,452,094 | 소비자가 판정할 덱의 시계와 대조 |

| 봉인 | |
|---|---|
| LIGGGHTS | PUBLIC 3.8.0 · git `3d5c00f20519e6bb6eb6756f51f1ad36564e649d` · **2026-03-26-14:37:06 빌드** (WSL 판과 같은 소스 · 다른 빌드) |
| 바이너리 | `/lustre/home/yonghoon/LIGGGHTS-PUBLIC/src/lmp_mpi` · sha256 `ee2d77261bac9e7fa4e9311c8709e74bf7583a13225a5bc35a791bef9be60a3f` |
| 실행 | `launch_prefix` = `mpirun --oversubscribe --bind-to none -np 1` (병렬 mesh 덤프는 삼각형 순서가 바뀐다 — 사전등록 §2-5b) |
| `deck_source` | `…/runs/LH_s32452843/in.mixer` · `6d71bd50c00797b6…` (= 이 리포 생성기 산출 — 컨테이너 재생성 LH 3 덱 해시가 ibb 와 같다) |
| `motion_signature` | `87132d1e…` (= v1) |
| `tool_sha256` | `b1facac1…` = `scripts/mixer_restart_phase_test.py` @ `77919b860` |

★ **WSL v1 과 행 단위 비트 동일** — `rows` 208 행 (step · `error_deg` · `resid_m`) · `steps_checked_A/B` · 각 오차 · 잔차 · 대칭 간격 · 리셋 간격이
v1 (WSL `lmp_serial` 08-25 빌드 · LC 덱) 과 **전부 같다**.  빌드 · 실행 파일 · 덱 출처 (LC ↔ LH, 운동 서명 같음) 가 달라도 처방 회전의 **출력된** 궤적이
STL 출력 자릿수에서 같다는 실측이다.
⚠ 이것은 `-np 1` 끼리의 비교다 — **`-np 20` 런의 메시 운동이 같다는 증명이 아니다** (가정 그대로 · Codex 5 차 요청서 §S2).

소비자 대조 (컨테이너, 이 파일이 들어간 커밋의 코드): `load_phase_receipt(receipt_v2_ibb, deck_walls(LH_s32452843))` → **수용** (덱 문자열 유무 모두).
`run_dir` 을 주면 → **거부** *"발사 봉인 (launch_record.json) 이 없다"* — 설계대로다: 런에 잇는 것은 `launch_highbo.sh first` 가 봉인한 뒤이고,
그때 봉인의 바이너리 sha256 = `ee2d7726…` · SLURM 이면 `job_start.json` 까지 맞아야 한다 (사전등록 §2-5b).
⛔ **Codex 5 차 GO 전에는 이 영수증으로 발사 · 판정 결정을 하지 않는다.**  ⛔ 이것도 개별 런의 체크포인트 상태 확인이 **아니다** (아래 v1 절 그대로).

**WSL v2 = `receipt_v2.json`** (`~/phase_v1` 재분석 · 1저자 원본 바이트 그대로 · sha256 `1c9e4e17897be21e…` · 29,733 B · 도구 `6f0aa198…` = `bc1a7cd83` 판 ·
바이너리 `4efca042…` (WSL `lmp_serial` 08-25) · 덱 출처 LC_s32452843 `72b52c17…`): **통과** — 각 오차 · 각 경계 · 위치 경계 · 잔차 · 대칭 간격 · 208 행 · 운동 시계가
**ibb v2 와 전부 같다**.  LH (ibb) 에는 이어지지 않는다 (소비자가 봉인 바이너리와 대조) — L · LC 측정 기록용.

---

## v1 (WSL) — `receipt_v1.json`

`receipt_v1.json` — **1저자 WSL 원본을 한 바이트도 고치지 않고** 넣었다.

```
sha256  520ee5d0135b0090dce2a541bdbb6808d79b25d398c90c4b3bdaf205e228e9e0
크기    29,231 B
원본    /home/yonghoon71/phase_v1/receipt_v1.json   (host DESKTOP-IK8J81H)
```

## 같은 폴더의 `receipt_v0_pre_hbr3.json` (1 차, 참고용)

09-28 00:0x 에 **HBR3 수정 전** 도구로 낸 1 차 실측 (`passed: true` · 오차 2.0015 × 10⁻⁵ °).
표본이 **3 step** 뿐이고 (20000 · 25000 · 30000) A/B 두 경로 대조 · 봉인 · `run_status` 가 없다.
그 자신의 note 도 범위를 좁게 적는다 — *"바이너리의 성질 … 어느 런의 벽 좌표가 아니다"*.
⛔ **수정 전 도구 산출이라 판정 경로에 쓰지 않는다.**  v1 이 그것을 대체한다.

## 무엇을 증명하나

09-26 WSL 크래시로 믹서 측정 10 런이 53–61 % 에서 끊겨 **체크포인트에서 이었다**.  드럼이 **39 각형**이라
재개가 **회전 위상**을 어긋나게 잡으면 가루가 만나는 면이 달라진다 — 캠페인이 조용히 오염된다.
이 영수증은 **처방된 회전(메시 운동 계약)이 재개를 건너 위상을 보존하는가**를 잰다.

| 양 | 값 | 비고 |
|---|---|---|
| `passed` · `reasons` | **true** · `[]` | |
| `angle_error_deg` (최대) | **1.9219 × 10⁻⁵ °** | A 208 + B 81 = 289 step 표본 |
| `angle_bound_deg` | **0.0011459 °** | = `angle_resolution_deg` — **STL 출력 자릿수 바닥**이지 측정 오차가 아니다 |
| 등록 상한 | 0.05 ° | 경계가 **43 배** 안쪽 |
| `symmetric_gap_deg` | **3.8722 °** | ★ 39면 대칭으로 같아지는 각을 뺀 **가장 가까운 다른 리셋 후보** |
| `reset_alternative_gap_deg` | 79.2047 ° | |
| `ab_max_vertex_diff_m` | **0.0** | ⚠ **증거로 쓰지 말 것** — 아래 정정 |
| `residual_max_m` | 5.1373 × 10⁻⁸ | |
| `nfacet` | **39** | |

★ **판별력은 경계가 아니라 이 비에 있다** — 측정 오차 1.92 × 10⁻⁵ ° 대 가장 가까운 다른 위상 3.8722 °
= 약 **20 만 배**.  위상이 모호하지 않게 특정된다.  경계 0.00115 ° 만 인용하면 이 사실이 안 보인다.

## ★ `SELF-56` 수정이 실제로 작동한 증거

```json
"run_status": { "A": {"exit":0,"complete":true,"completion_basis":"last_step","banner":false}, "B": {…같음} }
```
**배너가 없는데도** 마지막 thermo step(9,452,094)으로 완주를 판정했다.  이 빌드가 09-21 덱에서 배너를
안 찍는다는 것이 `SELF-56` 이고, `ba33a4939` 가 완주 정의를 `exit 0 ∧ (배너 ∨ 마지막 thermo step = 끝)`
으로 고쳤다.  `completion_basis` 가 **어느 근거로 판정했는지**를 남긴다.

## ⛔ 정정 (2026-09-28) — `ab_max_vertex_diff_m = 0.0` 은 증거가 아니다

⚠⚠ **`0.0` 을 "A/B 가 같다" 의 증거로 인용하지 말 것** (`HBR4-01`, Codex 4 차 2026-09-28): B 에는 좌표 유한성 검사가 없어 **B 좌표가 전부 NaN 이어도** `max(0.0, NaN)` 이 0.0 을 유지해 `passed=true` 가 난다.  실제 v1 이 NaN 이라는 뜻은 아니지만, **이 필드는 그 주장을 떠받치지 못한다**.

같은 판정문의 `HBR4-03` 은 **각 경계 0.00115 ° 도 완전한 오차 예산이 아니라고** 본다 — 생산자가 허용한 형상 잔차(≤ 1e-7 m)를 소비자가 버리기 때문이다 (합성 반례에서 실제 겹침 1.05568 % 를 0.95 % 로 계산해 PASS).
⇒ **이 영수증으로 LH 발사·판정 결정을 하지 않는다** (Codex 4 차 = HOLD).

## ⛔ 이 영수증이 증명하지 **않는** 것

영수증 자신이 못 박는다:

> `"개별 런의 체크포인트 상태 확인이 아니다"`

이것은 **바이너리 + 메시 운동 계약의 성질**이다 (처방 회전은 입자와 무관 → 같은 step 구조면 캠페인
메시와 같은 궤적).  ⇒ **측정 10 런 각각이 옳은 체크포인트에서 이어졌다는 증명이 아니다.**
그 구멍은 별건이고 미구현이다 — `docs/session_20260923_progress.md` ㉖ 의 남은 일 ④
"런별 체크포인트 상태 확인 도구 (Codex 3 차 Q1)".

## 봉인 (재생성 조건)

`"바이너리 · STL · 주기 · dt 가 바뀌면 다시 만든다"`

| | |
|---|---|
| LIGGGHTS | PUBLIC 3.8.0 · git `3d5c00f20519e6bb6eb6756f51f1ad36564e649d` · 2026-08-25-18:16:51 빌드 |
| 바이너리 | `/home/yonghoon71/src/LIGGGHTS-PUBLIC/src/lmp_serial` · sha256 `4efca042a1bbdafb4c68f64815ce7965b42f43588757527e91c7d82be07e038d` |
| 덱 A / B | `cd8fce2f…` / `19ea03e5…` |
| STL (A·B 동일) | Back `2e7b962d…` · Drum `fe821a8a…` · Front `443f9c3c…` |
| `deck_source` | `dem_scripts/mixer_20260921/runs/LC_s32452843/in.mixer` · `72b52c17…` |
| `motion_signature` | `87132d1e6803906c060952526674f8364e1375fcbc67b7dcc3436aaaced41e9f` |
| `tool_sha256` | `d846101419bacc8b1dfca274a246206e47296cdff9b6bd6c5208f8ff4c91cae7` |
| 운동 | `period` 0.799562 s · `dt` 7.055 × 10⁻⁷ · 축 x · 원점 (0,0,0) |
| step | `rotation_start_step` 385,337 · `run_total` 9,452,094 · `n1` 5,802,624 · `dump_every` 45,333 |
| `sealed_at` | 2026-09-28T01:44:32.737758+09:00 · host DESKTOP-IK8J81H |

## ⛔ 2026-09-28 낮 — 이 v1 영수증은 새 소비자 (v2) 가 **거부한다** (Codex 4 차 HBR4-01 · 02 · 03)

- 생산자 (`scripts/mixer_restart_phase_test.py`) 가 v2 로 바뀌었다: B 에도 유한성 · 형상 검사 · 봉인 목록과 덤프 해시 목록을 기대 집합과 **정확히** · 내보내는 수 전부 유한 ·
  운동 시계 · 회전 시작 · 위치 경계 `pos_bound_m` (형상 잔차 + 출력 반올림 → 거리) · 각 경계 = 실측 + 해상도 (합).
- 소비자 (`check_contact_validity.load_phase_receipt`) 는 `restart_phase_v2` 만 받는다 — 이 파일 (`restart_phase_v1`) 은 스키마에서 거부된다.
- ⇒ **WSL `~/phase_v1` 에서 고친 도구로 `analyze` 만 다시** 돌려 v2 를 만든다 (A/B LIGGGHTS 실행 · 봉인 · 덤프는 그대로 쓴다 — 재실행 불요):
  `python3 scripts/mixer_restart_phase_test.py analyze ~/phase_v1 --out docs/data/mixer_phase_receipt_20260928/receipt_v2.json`
- 이 v1 파일은 **측정 기록**으로 남긴다 (바이트 동일 · 지우지 않는다).  위의 `ab_max_vertex_diff_m = 0.0` 은 여전히 A/B 동일의 증거가 아니다 (HBR4-01).
