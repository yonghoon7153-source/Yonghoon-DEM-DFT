# LHS 인계표 — 판단 누적 (2026-09-24 ~)

> 인계표 `docs/data/lhs_handover_20260919.csv` (생성기 `scripts/lhs_design_dataset.py`, 커밋 `a5e181384`) 는
> **배포 보류**다 — 수영 님께 나가지 않는다.  앞서 파일로 보낸 것은 검토용이지 인계가 아니고, 저자 비준 뒤에 넘긴다.
> 이 파일은 그 비준을 위한 **판단 목록**이다.  판단이 생길 때마다 아래에 **더한다** (지우지 않고, 뒤집히면 표시한다).
> 각 판단에 근거 (실측) · 처방 · 비준 필요 여부를 단다.

## J1. porosity 는 ε_union 이 아니라 ε_sphere — 인계표에서는 **기록 전용** (동의)

- 근거: CLAUDE.md 의 porosity 규약 (ε_sphere = 물질 보존, ε_union 은 교차점검 · 상한) · 2026-08-12 정정 (*"모든 porosity 는
  ε_sphere 로 통일"*).  인계표 열은 `porosity_sphere_pct_RECORD_ONLY` 이고 회귀 타깃은 φ_SE · φ_AM 둘이다 — porosity 는
  ε = 1 − φ_SE − φ_AM 로 유도하고 그 항등식을 1e-9 로 검사한다 (DESC-07).
- 처방: 없음.  단 **J2 가 그 φ 두 개의 분모를 틀리게 잡고 있다.**

## J2. ⛔ φ · porosity 의 분모가 **바닥 벽이 아니라 덤프 상자 바닥**에서 잰 높이다 — 원장 `LHS-10` (새로 등재)

- 근거 (인계 CSV 130 행):
  - `scripts/lhs_descriptor_harvest.py` 의 `volumes_and_phi` 는 `H = plate_z − box_lo[2]` 를 쓴다 (`box_lo` = 덤프 `BOX BOUNDS`).
    같은 계열 덱 (`dem_scripts/ps_sweep_6mah_20260914/in.ps_7_3_r45.liggghts`) 은 상자를 `region reg_box block … -0.01 1.0`
    로, 바닥 벽을 `wall/gran … zplane 0.0` 으로 둔다 ⇒ 상자 바닥 −10 µm, 입자는 z ≥ 0 에만 있다.
  - `V_box_sim / rve²` 가 **130/130 에서 정확히 plate_z + 10.000 µm** 다.
  - φ 편향 인자 plate_z / (plate_z + 10 µm) = **0.757 (`lhs00_126`) – 0.875 (`lhs00_002`)**.  얇은 침대일수록 크다
    ⇒ 상수 배율이 아니라 **설계 축과 얽힌 편향**이라 회귀가 흡수하지 못한다.
  - porosity (기록 전용) 중앙 **47.2 %** → 벽 기준 **37.5 %** (q25 27.1 · q75 40.4).
  - DESC-07 항등식은 셋이 같은 분모를 쓰므로 **통과한다** — 자기일관은 옳음의 증명이 아니다 (규율 ⑤ 의 친척).
- 처방: 수확기가 바닥을 **덱의 벽 (`zplane`)** 에서 읽고 산출물에 `z_floor` 로 남긴다 → 인계표 재생성.
  ΣV 가 그대로라 기존 열만으로도 **정확한** 사후 보정이 된다 (φ′ = φ · (plate_z + 10 µm) / plate_z) — 이것은 확인용이고,
  정본 수정은 수확기다.
- 비준 필요: 수정 방식 (권고 = 수확기 수정 + 재생성).  ⚠ 인계 보류 사유에 이것이 **더해진다** — 회귀 타깃 자체가 틀렸다.
- ↪ 처방은 **J8 에서 다듬었다** — 덱에서 벽을 읽는 대신 웹앱 규약 (`V_box = L² · plate_z`) 에 맞춘다.

## J3. 두께 = **① plate_z − z_floor** (J2 수정 뒤) — ② 는 φ 까지 함께 옮길 때만 (앞선 메모의 "② 가 맞다" 에 부분 반대)

- 원칙 (메모에 동의): 두께와 porosity 는 **한 정의**에서 같이 나와야 한다 (ε = 1 − ΣV / (A·H)).
- 그런데 지금 인계표의 φ · porosity 는 **플래튼 기준**이다 (J2) ⇒ 그것과 자기일관인 두께는 ② (고체 z 범위) 가 아니라
  **① plate_z − z_floor** 다 (벽이 z = 0 이므로 곧 plate_z × 1e3 µm).  ② 를 **두께에만** 쓰면 바로 그 원칙이 깨진다.
- ① 과 ② 의 차이 = 플래튼이 고체 위에 뜬 틈 (plate_z − z_hi) + 바닥 틈 (z_lo − z_floor).  크기는 **아직 못 잰다** —
  band 진단이 산출물 최상위에 없다 (`LHS-08` · `LHS-09`).
- 처방: (a) J2 수정과 함께 `thickness_plate_um` (= plate_z − z_floor) 을 **φ 와 같은 정의의 측정값**으로 내보낸다.
  (b) 재수확에서 band 진단 (z_lo · z_hi · plate_above_solid) 을 최상위로 올려 틈을 잰다.  (c) 틈이 무시할 만하면 ① 유지,
  크면 **φ · porosity · 두께를 함께** ② 로 옮긴다 (harvest_v2).  한쪽만 옮기지 않는다.
- `thickness_est_um` 은 이름 그대로 두고 "두께 측정값" 으로 부르지 않는다 (메모에 동의).
- 비준 필요: (a) 를 지금 측정값으로 넣을지.

## J4. "plate_z 대 추정치 31 % 차이 = 바닥 기준 문제" — 원인이 아니다

- 근거: plate_z 는 벽 (z = 0) 에서 잰 값이라 바닥 문제를 타지 않는다 (바닥 문제는 V_box 쪽 — J2).  추정식 `thickness_of` 는
  porosity 를 **18.3 % 로 고정**하는데, 그 값은 6 mAh 침대 **한 개**에서 보정했다 (plate_z 116.8 µm · 고체 높이 96.2 µm
  ⇒ 17.6 %).  LHS 침대의 벽 기준 porosity 는 중앙 37.5 % 라 추정이 얇게 나온다.  |오차| 중앙 31.28 % · 최대 76.78 % 를
  재현했고, 벽 기준 porosity 가 plate_z 와 +0.51 로 같이 움직여 두꺼운 쪽에서 더 벌어진다.
- 처방: 추정식은 설계 점검용 그대로 둔다 (측정으로 쓰지 않는다).  "바닥 기준 문제" 라는 진단은 J2 (V_box) 로 옮겨 적는다.

## J5. ⚠ 벽 기준으로 고쳐도 porosity 가 높다 (중앙 37.5 %) — 설명되지 않았다, 인계 전 해소 필요

- 근거: 같은 300 MPa · E_SE 1.35 GPa 인데 6 mAh 보정 침대 17.6 % · real_14 15.6 %.  LHS 는 면용량 2 mAh · RVE 50 µm ·
  두께 31–70 µm (130 행 전부 압력 300 · E_SE 1.35 · RVE 50 · 면용량 2 고정).  상관: plate_z +0.51 · am_pct +0.30.
- 후보: 플래튼 뜸 (① − ② — z_hi 가 있어야 잰다) · 얇은 침대에서 벽 근처 성긴 층의 몫 · 덤프 시점 (RELAXATION 뒤 플래튼 위치).
- 처방: 재수확 band 진단 (z_hi) 로 첫 후보부터 판별.  판별 전에는 인계표 φ · porosity 를 **절대값**으로 넘기지 않는다.
- ↪ **대부분 J9 로 설명됨** (같은 step 메시 33 건 중앙 11.0 % · 이른 메시 97 건 중앙 38.5 % — 겹치지 않는다).

## J6. 벽 기준 porosity 가 **음수**인 4 건 — 겹침 과다 (ε_sphere 규약의 퇴화 케이스)

- `lhs00_118` −2.0 % · `lhs00_100` −1.18 · `lhs00_121` −0.65 · `lhs00_106` −0.09 (J2 보정 뒤).  ΣV 가 상자를 넘는 조밀
  침대에서 ε_sphere 가 음수가 되는 겹침 artifact 다 — CLAUDE.md 는 이런 케이스를 코퍼스에 섞으면 추세가 깨진다고 적는다.
- 처방: 인계표에 표시 열 (`eps_sphere_negative`) 을 두고, 회귀에서의 취급 (제외 / ε_union 병기) 을 비준받는다.

## J7. lhsx 확장 64 건은 **J2 수정 뒤에** 수확한다

- 근거: ibb 워치 (09-24 02:29) — lhsx 62/64 완주, 2 건 진행 중.  같은 수확기로 돌리면 같은 편향이 들어간다.
- 처방: J2 수정 → 수확기 selftest 에 바닥 검사 (덱 `zplane` ↔ 산출물 `z_floor`) 추가 → lhsx 수확.

## J8. 왜 웹앱 코드로 130 건을 안 돌렸나 · 무엇이 문제였나 (사용자 질문 09-24)

- **웹앱 코드는 바닥이 맞다**: `scripts/dem_analysis_core.py` 는 `V_box = box_xy · box_xy · plate_z` (줄 42 · 66) — 벽 z = 0 부터
  잰다.  10 µm 문제는 **새 수확기에만** 있다.
- **그래도 웹앱 코드를 그대로 못 쓴 이유 = `DESC-01`** (Codex 판정 09-13 HOLD, `docs/reviews/codex_verdict_lhs_descriptors_20260913.md`):
  `dem_analysis_core.py:941` 이 τ 가 없으면 `return None` 하고 `analyze_contacts.py:430` 의 `if eff_cond:` 가드가 **기하량 φ
  두 개까지 버린다**.  LHS 는 τ 가 130 중 14 에서만 나온다 (`LHS-08`) ⇒ 웹앱으로 돌렸으면 **116 건의 구조 타깃이 비고**, 비는
  쪽이 하필 연결이 약한 침대라 결측이 물리와 상관된다.  그래서 τ 와 무관하게 φ 를 항상 내는 수확기를 따로 만들었다.
- **무엇이 잘못됐나**: 수확기가 φ 의 분모 높이를 웹앱 규약에서 **가져오지 않고** 덤프 `BOX BOUNDS` 에서 다시 뽑았다 (덱 상자가
  벽보다 10 µm 아래서 시작).  자기일관 검사 (DESC-07) 는 같은 분모라 통과했고, **같은 침대에서 수확기 φ ↔ 웹앱 φ 를 맞대는
  검사가 한 번도 없었다** — 그 하나면 바로 잡혔다.  규율 ① (리포에 있는 것부터) 을 덤프 읽기에는 지켰는데 **정의**에는 안 지켰다.
- 처방 (J2 를 다듬음): 수확기의 H 를 웹앱 규약 (`plate_z`, 벽 z = 0) 에 맞추고, **같은 침대 픽스처에서 수확기 φ · porosity =
  웹앱 φ · porosity** 를 selftest 로 강제한다 (먼저 빨간불 확인 — 규율 ②).  덱의 `zplane` 은 그 가정 (벽 = 0) 의 점검으로만 쓴다.
- 남는 것: 웹앱 규약으로도 porosity 중앙 37.5 % — **J5 는 수확기 버그와 별개**로 열려 있다.

## J9. ⛔ 플래튼 위치를 **원자 덤프보다 이른 메시**에서 읽었다 — J5 의 주원인 · 원장 `LHS-11` (새로 등재)

- 근거 (`docs/data/lhs_descriptors_20260919/_batch_summary.json` + 인계 CSV): `lhs_harvest_batch.pick_mesh` 는 같은 step 의
  메시가 없으면 원자 step 이하의 최신 메시를 쓴다 (`latest_le`) — **130 중 97 건**.  step 차이 중앙 150만 · 최대 290.5만.
  LHS 런은 290만 step 에서도 압축 중이다 (ibb 워치 09-24) ⇒ 이른 메시의 플래튼은 **아직 내려오는 중**인 위치다.
- 벽 기준 porosity: 같은 step 메시 (`exact`) 33 건 중앙 **11.0 %** (−2.0 … 27.1) · 이른 메시 97 건 중앙 **38.5 %**
  (32.8 … 52.9) — 두 집단이 **겹치지 않는다**.  메시 step 과의 상관 **−0.95**.  음수 4 건 (J6) 은 전부 `exact` 쪽.
- ⇒ J5 의 높은 porosity 는 대부분 이것이다.  앞선 메모의 *"낮은 쪽은 맞고 높은 쪽이 벌어진다"* 도 이것 — 벌어진 쪽이 이른 메시다.
- 영향: 97 건의 φ · porosity · plate_z 두께가 모두 틀렸다.  얼마나 틀렸는지는 그 step 의 플래튼 위치가 있어야 잰다.
- 처방: (a) 원자 step 과 같은 step 의 메시를 원본 (WSL `lhs_local` · ibb) 에서 찾는다 — 있으면 재수확.  (b) 없으면 플래튼 위치를
  로그 (thermo) 에서 읽거나 고체 윗면 (②) 으로 대체하고 **라벨을 단다**.  (c) `pick_mesh` 의 `latest_le` 를 거부로 바꾸거나 step
  차이 한도를 둔다 — 조용한 대체가 사고의 원인이다.  (d) `scripts/lhs_phi_crosscheck.py` 를 WSL 에서 돌려 130 건의 바닥 틈과
  **플래튼 − 고체 윗면** (`plate_gap`) 을 실측으로 확인한다.
- 비준 필요: (a)–(c).

## J10. 교차검사 실측 (WSL, 실제 130 덤프, 09-24) — LHS-10 · LHS-11 확인, 세 번째 차이 없음 → 두께 · φ 정의 권고

`scripts/lhs_phi_crosscheck.py` (두 코드의 함수를 같은 덤프에 호출, 인터프리터 `~/Yonghoon-DEM-DFT/venv`):
- 131 행 = FLOOR_ONLY **130** · OTHER 0 · ERROR 0 · MISSING 1 (코호트 131 번째 행, 원본 없음).
- 바닥 틈 130/130 **정확히 0.01** (10 µm) · 최대 |잔차| **5.5e-14 %p** ⇒ 두 코드의 차이는 바닥 하나로 **전부** 설명된다.
- porosity 중앙 — 수확기 47.28 % · **웹앱 37.54 %** · φ 배율 0.7571–0.8746 (J2 의 CSV 추정과 일치).
- 플래튼 − 고체 윗면: `exact` 33 건 **−1.2 … −0.3 µm** (중앙 −0.53 — 윗면 알이 플래튼에 살짝 눌림 = 정상) ·
  `latest_le` 97 건 **+8.1 … +27.4 µm** (중앙 +16.2 — 플래튼이 침대 위에 떠 있다 = 압축 중 위치) ⇒ **LHS-11 을 덤프에서 직접 확인**.

권고 (J3 확정 — 비준 필요): **두께 · φ · porosity 를 모두 ② (고체 윗면 − 벽) 한 정의로** 낸다 (harvest_v2).
- 이유 ① 130 건 전부 원자 덤프만으로 나온다 — 메시 시점에 기대지 않으므로 LHS-11 의 뿌리가 없어진다.
- 이유 ② 플래튼이 현재 위치인 33 건에서 ① 과 ② 가 0.3–1.2 µm (두께의 약 1 %) 안에서 일치한다 — 웹앱 규약 (①) 과의 차이를 수로 밝힐 수 있다.
- 이유 ③ 두께와 porosity 가 한 정의에서 나온다 (메모의 원칙).  ⚠ 고체 윗면 = 가장 높은 알 하나의 윗면 (τ 밴드와 같은 `solid_zrange`) —
  튀어나온 알 하나에 좌우될 수 있으니 재생성 때 상위 분위 (예: 99.9 %) 와의 차이를 함께 적는다.
- 이 권고가 J2 의 "웹앱 규약 (plate_z) 에 맞춘다" 를 **대체**한다 — 플래튼 시점이 틀린 97 건에서는 웹앱 규약도 틀리기 때문이다.

## J11. ↩ J10 정정 — **웹앱 방식 (같은 시점 플래튼 · 벽 z = 0) 이 1순위**, ② 는 검산용 (사용자 지적 09-24)

- 사용자: *"그냥 기존 webapp 때처럼 하면 안 되는 이유"* · *"mesh 를 99 이렇게 sort 하지 말고"*.  둘 다 맞다.
- 덱 (`lhs00_000`): `dump dmp_mesh all mesh/stl 5000 post_…/mesh_*.stl` · undump 없음 ⇒ 원본에는 메시가 **끝까지 5000 step 마다** 있어야 한다.
  그런데 WSL `lhs_local` 에는 `mesh_985000 · 990000 · 995000` **세 장뿐**이다 = "마지막 3 장" 을 **문자열 정렬**로 고르면 나오는 결과
  (`mesh_995000` > `mesh_2425000`).  `exact` 33 건은 메시 덤프가 100만 step 뒤에 시작해 이름이 전부 7 자리라 문자열 정렬이 우연히 맞았다 (추정).
- 수확기 `pick_mesh` 는 step 을 정수로 비교한다 — 정렬 결함은 **옮기는 단계** (리포 밖) 에 있다.  리포 안 두 곳 (`recompute_porosity_dual.py` ·
  `make_heckel_manifest.py`) 은 키 정렬이다.
- ⇒ 처방: 97 건의 **원자 덤프와 같은 step 의 메시**를 원본 (ibb) 에서 숫자 순서로 다시 가져온다 → 130 건 전부 웹앱 규약 (①) · 수확기는 바닥 (LHS-10) 만
  고친다 → 기존 코퍼스와 같은 규약.  ② (고체 윗면) 는 검산 (`exact` 33 건 −1.2…−0.3 µm) 으로만 쓴다.  원본에 없는 케이스만 ② 로 대체 + 라벨.
- 대기: ibb 원본에 `mesh_<원자 step>.stl` 이 있는지 (사용자 확인 중).

## J12. 같은 step 메시 재반입 뒤 교차검사 (WSL 130 덤프, 09-24) — LHS-11 해소 · 남은 결함은 LHS-10 하나

- 재반입: 코호트 원자 step 과 같은 `mesh_<step>.stl` 을 ibb 원본 (`/home/yonghoon/dem_test/lhs/<case>/post_<case>/`) 에서 숫자 그대로
  (`--files-from` 목록 · rsync).  원본에는 메시가 끝까지 있었다 (예: `lhs00_034` 672 장).
- `lhs_phi_crosscheck.py` 재실행: FLOOR_ONLY 130 · OTHER 0 · MISSING 1 · 바닥 틈 0.01 · 잔차 5.5e-14 %p ·
  **플래튼 − 고체 윗면 = exact 130/130, −1.21 … −0.27 µm (중앙 −0.52)** — 전부 정상 눌림.
- **웹앱 규약 porosity 중앙 9.89 %** (수확기 30.65 %) · φ 배율 0.7416–0.8246 ⇒ J5 (높은 porosity) 는 전부 LHS-11 이었다.
- 남은 것 = **LHS-10 (바닥 10 µm) 하나**.  처방: 수확기 H = plate_z − z_floor, z_floor = 벽 0 (웹앱 규약) + 입자가 벽 아래에 없는지
  (min(z − r) ≥ −허용) 거부 검사 + 교차검사 selftest 로 두 코드 일치 강제 → 130 재수확 + lhsx 64 수확 (메시는 원자 step 과 같은
  것만, `latest_le` 는 거부) → 인계표 재생성 → J6 (음수 porosity) 건수를 새 값으로 다시 센다.

## J13. ✅ 수확기 수정 (사용자 비준 09-24 "비준이야") — 재현 먼저, 세 곳

- `lhs_descriptor_harvest.volumes_and_phi`: 분모 H = plate_z − `Z_FLOOR` (벽 0, 웹앱 규약) · 입자가 벽 아래 (z − r < −½·r_max) 면 거부 ·
  산출에 `z_floor_sim` · `solid_bot_sim` 추가.  selftest ⑭ (상자 바닥 −1 인 덤프에서 H = 5 · porosity = 웹앱 식 · 벽 아래 입자 거부) —
  수정 전 **3 건 빨간불** 확인 뒤 초록.
- `lhs_harvest_batch.pick_mesh`: `latest_le` 폐지 — 같은 step 메시가 없으면 거부 (`none` → `NO_MESH`).  수정 전 빨간불 확인.
- `lhs_phi_crosscheck`: 두 코드가 **SAME** 이어야 통과 (수정 전 3 건 빨간불).
- 다음: WSL 에서 130 재수확 → 교차검사 SAME 130 확인 → 인계표 재생성 → LHS-10 · LHS-11 claimed_fixed → J6 (음수 porosity) 재집계.

## J14. ⛔ 재수확 72/130 — 거부 58 건은 J13 가드 (½·r_max) 가 **연속 분포의 한가운데**를 자른 것 → 가드를 "덱 확인 + 기록" 으로 (✅ 비준 09-24 · 구현) — 원장 `LHS-12`

- 실측 (WSL, `0424795d6`, 09-24):
  - 교차검사: SAME 72 · ERROR 58 · MISSING 1.  SAME 72 은 바닥 틈 0 · φ 배율 1.0000 · 최대 |잔차| 5.6e-14 %p ·
    porosity 중앙 8.28 % (양쪽 같음) · 플래튼 − 고체 윗면 −1.05…−0.27 µm.  ERROR 58 = 수확기 가드가 던진 거부.
  - 수확: 72/130.  58 건 전부 같은 사유 — *"입자가 벽 아래: min(z − r) = −0.8…−5.4 µm"*.
    58 = bimodal 31/100 · mono_AM_S 15/15 · mono_AM_P 12/15.
- 판단 (설계 CSV 반지름과 대조):
  - 깊이 d = −min(z − r) 는 **가장 큰 입자 반지름을 따라간다** — corr(log d, log r_max) **0.877** vs log r_SE 0.242.
    d/r_max = 0.50–0.97 (아래 2 건 제외) ⇒ 가장 깊은 입자는 **제일 큰 AM** 이고 중심은 벽 **위** =
    바닥 벽과의 **깊은 겹침**이지 벽을 뚫고 샌 것이 아니다.
  - d/r_max 가 문턱 0.5 바로 위에 몰려 있다 — 0.5–0.6 **24** · 0.6–0.7 15 · 0.7–0.8 9 · 0.8–0.9 5 · 0.9–1.0 3 · ≥ 1 2
    = 연속 분포를 문턱에서 자른 꼬리 모양.  ⇒ ½·r_max 는 정상과 결함을 가르는 선이 아니다 (J13 에서 근거 없이 고른 값).
  - 거부하면 설계 축과 얽힌 편향이다 — 거부된 bimodal 은 AM_P 가 작고 (지름 중앙 7 vs 11 µm) · AM 이 많고
    (85 vs 80 wt%) · P 비중이 높다 (0.8 vs 0.4).  mono 는 27/30 이 빠진다.
  - 웹앱은 이 58 건을 경고 없이 계산한다 (구 부피 전부 · 벽 0 기준) ⇒ 새로 깨진 것이 아니라 **새로 보인 것**.
  - ⚠ 예외 4 건 — `lhs00_056` · `079` · `107` · `110`: d 가 **정확히 같은 1.98008 µm**, 넷 다 r_AM_S = 1.0 µm.
    107 · 110 (mono_AM_S, r_max 1.0) 은 d > r_max ⇒ 어떤 입자의 **중심이 벽 아래 0.98 µm** = 사실상 벽을 뚫었다.
    독립 런 넷에서 같은 값인 것은 우연일 수 없다 — **원인 미상**, 덤프로 확인 필요.
  - ⚠ 남는 문제 — ε_sphere 규약 (웹앱) 은 벽과 겹친 구 부피를 고체로 센다.  AM 이 반지름의 50–90 % 를 겹치면
    그 몫이 작지 않을 수 있는데 **아직 재지 않았다**.  생산 덱도 같은 벽이므로 웹앱 코퍼스 전체의 규약 비용이다.
- 권고 (✅ **비준 09-24** — 사용자 *"ㅇㅇ 비준해줘"*):
  1. 입자 깊이로 벽 위치를 **추정**하던 가드를 없애고, 벽 위치를 **덱에서 직접** 확인한다 — 코호트 `deck` (sha 봉인) 의
     `wall/gran … zplane Z` 를 읽어 Z ≠ 0 이면 거부.  J11 의 원래 뜻 (*"덱의 zplane 은 가정 (벽 = 0) 의 점검으로만"*) 그대로.
     벽의 재질 type 도 기록한다 (깊은 겹침의 원인 후보).
  2. 벽 아래 입자는 **거부하지 않고 기록**한다 — 케이스마다 가장 깊은 입자 (상 · r · z) · 겹침/r · **중심이 벽 아래인 입자 수** ·
     벽 아래 구 부피 / ΣV · 플래튼 쪽도 같은 셈.
  3. 수확기 = 웹앱, 130 건 (교차검사 SAME 130).  제외 여부는 수확기가 아니라 **인계표 단계에서 저자가** 이 기록을 보고 정한다
     (특히 위 4 건).
- 보강 (사용자 09-24 *"밑에 박힌 양도 살릴 수 있는 방법이 있나, 예외로 안 두고?"*): 웹앱 식은 구 부피를 **통째로** 더하므로
  박힌 부피를 버리지 않는다 — 달라지는 것은 그 물질이 **어디로 갔다고 보느냐**뿐이다.
  - (가) 주 값 = 웹앱 그대로 — 박힌 물질이 틀 안 빈틈을 메웠다고 본다 (두께 plate_z, porosity 조금 낮음).
  - (나) 되돌려 놓기 — 박힌 부피를 벽 안으로 되돌려 얇은 층으로 쌓는다: H′ = plate_z + V_out / (L_x·L_y) ·
    porosity′ = 1 − ΣV / (L_x·L_y·H′).  물질도 빈틈도 그대로, 두께만 는다.  플래튼 쪽도 같이.
  - 둘의 차이 = 벽에 박힌 효과의 크기.  **130 건 전부 두 값** — 예외 없음.  4 건의 관통 입자 (r = 1 µm) 는 고체의
    0.005–0.007 % (설계 추정 부피 기준) 라 어느 쪽 값에도 영향이 없다.
- 구현 (재현 먼저 — 세 selftest 빨간불 확인 뒤 초록: 수확기 12 · 배치 4 · 교차검사 4):
  - `lhs_descriptor_harvest.check_deck_floor`: 덱의 `fix … wall/gran … primitive type N zplane Z` 를 읽어 가장 낮은 Z = 0 인지 본다
    (주석 무시 · `&` 이어 읽기 · 변수·벽 없음·0 아님 → 거부).  CLI 는 `--deck` 필수.  산출물 `deck_floor` · `raw.deck` (sha).
  - `volumes_and_phi`: ½·r_max 가드 **삭제** · `wall_record` = 바닥/플래튼 각각 벽 밖 부피 (구 cap π h²(3r − h)/3) · 비율 ·
    닿은 입자 수 · 중심이 벽 밖인 입자 수 (상별) · 통째로 벽 밖인 수 · 가장 깊은 입자 (상 · r · z · 겹침/r) + `pushback` (나).
    산출물에 `z_floor_sim` · `H_sim` · `solid_bot_sim` · `solid_top_sim` 도 올린다 (J13 판은 함수 안에만 있고 산출물에 안 나갔다).
  - `lhs_harvest_batch.run_one`: 코호트 `deck` 를 넘긴다 · 덱이 없으면 `MISSING_RAW` · `--verify-sha` 는 덱 sha 도 대조.
  - `lhs_phi_crosscheck`: 벽 밖 기록 칸 + 요약 (벽 밖 부피 분포 · 관통 입자 케이스 · (나) − (가) porosity · 두께 증가).
  - 수확기 docstring 의 `\*` (Python 3.12 SyntaxWarning, WSL 실행에서 보임) 정리.

## J15. 웹앱 porosity 코드 점검 (사용자 09-24 *"webapp 코드는 완성형인지 봐봐"*) — 식은 완성형, 입력 검사는 비어 있다 · 원장 `SELF-47` · `SELF-48` · `SELF-49`

- 식: `dem_analysis_core.calc_porosity` · `calc_porosity_dual` — ε = 1 − ΣV / (box_x² · plate_z), 두께 = plate_z × scale.
  코퍼스 전체가 이 식 하나를 쓴다 ⇒ 기준으로 삼기에 맞다.
- 구멍 — 입력을 검사 없이 믿는다:
  1. 메시와 원자 덤프의 step 을 맞춰 보지 않는다 — 올라온 메시 중 번호가 가장 큰 것을 쓴다 (`scripts/parse_liggghts.py:314`).
     이른 메시가 섞이면 LHS-11 과 똑같이 틀린다.  뷰어는 압축 전 plate_z 를 알고 **화면에서만** 피한다 (`webapp/app.py:7921`) —
     porosity 계산은 안 피한다.  → `SELF-47` (P1)
  2. 재계산 도구는 플래튼이 고체보다 **낮을 때만** 잡는다 (`scripts/recompute_porosity_dual.py:226`) — 자기 docstring 이 경고하는
     "압축 전 플래튼" (= **높을 때**) 은 통과한다.  → `SELF-48` (P2)
  3. 메시가 없으면 플래튼 = 가장 높은 입자 **중심** (`scripts/dem_analysis_core.py:125`) → 맨 윗줄 반쪽이 상자 밖 → porosity 가 낮다
     (`plate_z_source = estimated_center` 로 라벨은 남는다).
  4. 바닥은 항상 0 (덱 확인 없음).  5. 벽과 겹친 부피를 따로 세지 않는다 — ε_union 도 입자끼리 렌즈만 뺀다
     (`scripts/dem_analysis_core.py:69`).  6. 음수 porosity 경고 없음 — 25 % 초과만 경고 (`scripts/analyze_contacts.py:509`).
  7. 상자 가로만 읽어 정사각형 가정 (`scripts/dem_analysis_core.py:1060`).  → 3–7 묶어 `SELF-49` (P3)
- LHS 쪽: 1 은 수확기가 같은 step 메시만 받아 막혀 있다 (J13) · 4 · 5 는 J14 · 6 은 J6 재집계 · 2 · 3 · 7 은 LHS 와 무관.
- 코퍼스 쪽: 1 · 2 때문에 이른 메시로 계산된 웹앱 케이스가 섞였을 수 있다 (`1mAh_100_*` 가 plate_z 버그로 이미 제외된 전례).
  권고 = 읽기 전용 전수 점검 — 케이스마다 플래튼 − 고체 윗면이 + 몇 µm 이상이면 의심.  **미실행** (저자 결정 대기).
- 확인: 플래튼 STL 은 평판이다 (`docs/data/heckel_reproduction_20260917/mesh/mesh_1230000.stl` — 꼭짓점 6 개의 z 가 모두 같다) ⇒
  파서의 "꼭짓점 평균" 과 재계산 도구의 "최댓값" 정의 차이는 이 덱 계열에서 0.
- Codex 리뷰 — 권고대로 **재수확 뒤** 실측을 붙여 보낸다 (사용자 09-24 *"ㅇㅇ 비준해줘"*).  물을 것: (가) · (나) 중 주 값 ·
  두께 정의 · 덱 `zplane` 확인의 충분성 · 4 건 같은 깊이의 기전 · 위 구멍 중 코퍼스를 위해 고칠 것.  인계표는 그때까지 보류.

## J16. ✅ 재수확 130/130 (09-24, `4ee1038c3`) — LHS-10 · 11 · 12 닫힘 · 새로 보인 것 둘: 바닥 벽 재질 SE (`LHS-14`) · 음수 porosity 18 건 (`LHS-15`)

- 실측 (`docs/data/lhs_descriptors_20260924/`): 수확 130/130 · 메시 exact 130 · 봉인 sha (atom · contact · deck) 130 · 덱 바닥 z = 0 130 ·
  교차검사 SAME 130 (잔차 5.6e-14 %p) · 플래튼 − 고체 윗면 −1.21 … −0.27 µm.
- 옛 판 (09-19) 대비: porosity −15.8 … −48.6 %p (중앙 −36.3) · φ_SE ×1.21–2.01 (중앙 1.73) ⇒ 09-19 판으로 만든 인계표 값은 전부 틀렸다
  (배포 보류가 맞았다).
- (가) porosity: 중앙 9.89 % · p90 21.9 · 최대 27.1 · 최소 −2.43.  (나): 중앙 10.56.  (나) − (가): 중앙 0.61 %p · 최대 2.53 (mono_AM_P) ·
  두께 증가 중앙 0.23 µm · 최대 1.07 µm.  벽 밖 부피는 거의 다 **바닥 쪽** (ΣV 대비 중앙 0.60 % · 최대 4.39 % vs 플래튼 0.08 % · 0.21 %).
- ★ 바닥 벽 재질 = SE (`LHS-14`): 덱은 `primitive type 3` (bimodal) · `type 2` (mono) — 생산 real_4 는 `type 1` (AM_P).  AM 이 무른 바닥에
  깊게 박히는 까닭이고 J14 의 "깊이 ∝ 최대 AM 반지름" 과 맞는다.  의도 (분리막 SE 층 표현 등) 인지 **저자 확인 필요**.
- 관통은 4 건만의 일이 아니다 — 중심이 바닥 아래인 입자가 있는 케이스 42 (AM_S 618 · SE 62 · AM 2) · 통째로 바닥 아래 15 케이스
  (최대 21 개, 대부분 SE) · 통째로 플래튼 위 3 케이스 (SE).  겹침/반지름 **1.98** 자리는 9 케이스 (r 1 µm 7 · 0.5 µm 2) — 반지름에 비례하는
  같은 자리다 (`LHS-13`).  부피 몫은 작다.
- ★ J6 재집계 (`LHS-15`): (가) 음수 18 건 (−2.43 … −0.09 %) · (나) 16 건 ⇒ 벽이 아니라 **입자끼리** 겹침 과다.  생산 코퍼스는 음수
  ε_sphere 케이스를 코퍼스 밖에 둬 왔다.  인계표 취급 (표지만 · 회귀 타깃에서 빼기 · ε_union 병기) 은 **저자 결정**.
- 다음: Codex 리뷰 패키지 — 질문 = (가) · (나) 주 값 · 두께 정의 · 덱 `zplane` 확인 충분성 · 바닥 SE 재질의 뜻 · 1.98 자리 기전 ·
  음수 porosity 취급 · 웹앱 구멍.  덱 발췌 (플래튼 메시 type · 물성 블록) 가 필요하다.

## J17. 바닥 벽 SE 는 **의도**다 (사용자 09-24) → `LHS-14` wontfix · (가) · (나) 의 뜻이 분명해진다

- 사용자: *"우리 양극 가압할 때 밑에 SE 있고 SUS 넣는 쪽을 넣는데, 그건 AM 물성이어도 돼서 그렇게 한 거였어"* — 바닥 = SE 분리막 층,
  플래튼 = SUS 플런저 (AM 물성으로 충분).  덱 확인: 플래튼 메시 `type 1` (AM) · 바닥 `primitive type 3` (bimodal) · `type 2` (mono) = SE.
- ⇒ 바닥에 박힌 부피는 결함이 아니라 **AM 이 분리막 SE 를 누르고 들어간 것**이다 (실제 가압에서도 일어나는 일, 크기는 연화 E 에 좌우).
  바닥 쪽 박힘 (ΣV 의 0.60 %) 이 플래튼 쪽 (0.08 %) 보다 훨씬 큰 까닭도 이것 (무른 바닥 · 단단한 플래튼).
- 해석 (가설 — Codex 리뷰 Q1):
  - (가) = **LHS 고유 값** — 분리막 위에서 누른 침대 그대로 (주 값).
  - (나) ≈ **바닥이 단단했다면** — 박힌 부피를 되돌려 두께에 더한 값.  생산 덱 (바닥 AM) 코퍼스와 나란히 볼 때 쓰는 값.
- 생산 코퍼스와의 계통 차이 (바닥 재질) 는 인계표 README 에 적는다.
- Codex 요청서: `docs/reviews/codex_request_lhs_porosity_thickness_20260924.md`.

## J18. Codex 판정 (09-25, `docs/reviews/codex_verdict_lhs_porosity_thickness_20260924.md`) — 전부 수용 · 원장 `HND-01` ~ `HND-06` · (나) 가설 철회 · 인계표 = "명목 규약값 + 적격성 열"

- 결론: 인계표를 **"물리적 전극 구조의 ML 타깃"** 으로 외부 배포하는 것은 HOLD — 130 행을 버리라는 뜻이 아니다.  주 두께 = 같은 프레임의 플래튼 − 바닥
  간격 (ACCEPT, 한정) · (가) 는 **명목 구 부피 / 틀 간격 부피** 의 장부값으로 이름 붙여 보존 · (나) ≈ hard-bottom 은 REJECT · 관통 "기록만" REJECT ·
  음수 처리 REVISE (원값 보존 + 타깃별 적격성) · 웹앱/코퍼스 REVISE (provenance 감사) · coverage · τ 도 경계에 걸림 (REVISE).
- 내가 검증한 것 (09-25):
  - `HND-03` 산술 재현 — LIGGGHTS hooke kn 식 · Y* 1,468,923.8 · q 3 · φf 0.01 → r 1 µm z −0.980075994 (JSON −0.980076) · r 0.5 µm −0.490018998
    (JSON −0.490019).  q · φf 는 생산 덱 m6 (`coefficientMaxElasticStiffness`) · m8 (`coefficientPlasticityDepth`) 의 **AM–SE 칸**에 실재 (Codex 가 적은 "57 행" 은 m6
    만이고 φf 는 67 행 m8).  ⇒ 9 건의 입자는 바닥 평면 **아래쪽에 점착으로 매달려** 있다 (윗면이 평면 위 0.02·r).  LHS 덱의 m6 · m8 이 같은지는 사용자 grep 대기.
  - `HND-04` — `HANDOVER_EXTRA` 에 wall_record · deck_floor · 적격성 열이 없고 기본 수확 디렉터리가 20260919 인 것 실물 확인.  φ · porosity 상태를 수확기가 무조건
    OK 로 두는 것도 확인.
  - `HND-02` · `HND-05` · `HND-06` 은 코드 읽기로 확인 (min(z) · 쌍 렌즈 · z 평균).
- 철회: J17 의 *"(나) ≈ 바닥이 단단했다면"* — (나) 의 공극 부피는 (다) 와 같고 (가) 보다 W 만큼 크다; 벽 재질 변경의 편향 방향은 모른다.  (나) 는
  `*_pushback_equiv` 산술 지표로만 남긴다.  `LHS-14` 의 "의도된 설계" 는 유지하되 표현은 *"SE 접촉물성을 쓴 평면 바닥 proxy"* 까지.
- ★ 새로 보인 것 — τ 의 아래 밴드 (LHS-08): 110/130 이 `ELECTRODE_BAND_EMPTY` 인데 **전부 아래 밴드가 빈 것**이고, 그 밴드는 min(z − r) = 벽 아래로 새어
  나간 입자가 정한다 (lhs00_000: z_lo −1.905 µm, 밴드 [−1.905, −0.905] 에 SE 없음, SE 최저면 −0.658).  벽 (z = 0) 기준 밴드로 재진단하면 달라질 수 있다 —
  규약 변경은 재측정 뒤 (LHS-08 그대로), 진단 열만 먼저.
- 실행 계획 (**비준 대기** — 코드 변경 없음, 문서 · 원장만 커밋):
  A. 수확기: `overlap_over_r` → `outside_cap_depth_over_r` · 상별 cap 부피 (AM/SE × floor/plate) · (다) clipped 값 · 상태 분리 (중심 통과 · 완전 이탈 · 정상 겹침) ·
     STL 평판 검사 (`plate_planarity_span`) · `check_deck_floor` 문법 제한 (unfix · 재정의 = 마지막 활성 · group=all · 그 밖은 "검증 불가").  전부 빨간불 먼저.
  B. 인계 생성기: 기본 = 20260924 · Codex 권고 열 (명목 alias · pushback_equiv · clipped · 외피 · 경계 QC · `calculation_status` / `physical_target_status` /
     `hold_reason_codes` / `phi_sum_gt_one` · 규약 ID · 4 종 sha) · 음수 18 · 이탈 43 케이스로 end-to-end 회귀 · 130 행 원값 보존.
  C. τ: 벽 기준 양쪽 밴드 **진단 열** (보고 τ 규약은 불변).
  D. 결정 (저자): ① 이탈 43 케이스의 물리 타깃 = `HOLD_BOUNDARY` (Codex 권고) ② 음수 18 = 원값 + `physical_target_status=HOLD_NEGATIVE` ③ 인계표의 이름 =
     "DEM 명목 규약 데이터셋" (실제 공극률 예측기라 소개하지 않음) ④ 기존 코퍼스 provenance 감사 (Q6) 는 별도 트랙.
  E. ✅ 기전 확인 (사용자 grep 09-25): LHS 덱 m6 · m7 · m8 = 생산 덱과 동일 (AM–SE q 3.0 · φf 0.01 · kc 2.0e5) → HND-03 **재현됨 (조건부)**.
     9 건의 마지막 프레임 (관통 시점) 은 ibb 에 있으면 나중에.
- ✅ 비준 (09-25 "ㅇㅇ ㄱ ㄱ") · 구현 (재현 먼저 — 수확기 20 · 생성기 3 빨간불 → 전부 초록):
  - A 수확기: `plate_stl_info` + 평판 검사 (`PLATE_SPAN_TOL` 1e-7 sim, HND-06) · `check_deck_floor` = fix/unfix 생명주기 · 같은 id 재정의 = 교체 ·
    group=all 요구 · 흐름 제어 (label/jump/if/next) 뒤의 벽 정의/삭제와 include/read_restart/python 은 "검증 불가" 거부 (HND-02; 생산 덱 real_4 는
    벽 83 행 · `label loop_press` 180 행이라 통과) · `_wall_side` = 부호 있는 거리 → `outside_cap_depth_over_r` + `contact_overlap_over_r` (HND-03) ·
    상별 cap 부피 · `clipped` (다) · `boundary` = `calculation_status` / `physical_target_status` / `hold_reason_codes` (BOUNDARY_CENTER_OUT ·
    NEGATIVE_POROSITY) / `phi_sum_gt_one` · `handover_qc` 평면 (두께 µm · 명목 alias · pushback_equiv · clipped · 외피 · 부피 감사 · 경계 QC ·
    적격성 · 규약 ID `harvest_v2_20260925/spheresum_nominal_gap/wall_z0/exact_step_mesh` · `boundary_model_id` · sha 넷).
  - C τ 진단: `band_detail.wall_n_bot / wall_n_top / wall_n_span_components` (벽 z = 0 · 플래튼 기준) — 보고 τ · 규약 문자열 불변.
  - B 생성기: `DEFAULT_HARVEST_DIR` = 20260924 · `HANDOVER_EXTRA` 에 위 QC · 적격성 · τ 진단 · 프로비넌스 열 46 개 · 음수 케이스 (lhs00_005 실측값)
    end-to-end 회귀 (원값 보존 + HOLD 열).
  - ⚠ 09-24 스냅샷 JSON 에는 `handover_qc` 가 없다 (옛 코드 산출) ⇒ **WSL 재수확 v2** (`docs/data/lhs_descriptors_20260925/`) 뒤 인계표 재생성.

## J19. lhsx 음수 porosity = 겹침 이중계상 (확정) · 194 건 union 실측 · 인계표 porosity 규약 제안 (**비준 09-28 · 구현**) · 순수 SE 판정 시험 등록 (09-27)

- 원인 (확정): lhsx 는 SE/고체 **0.51–0.85** (pdd_SE 0.306–0.699 — 130 은 0.11–0.51).  SE 가 하중을 지며 SE–SE 겹침 (δ/d 0.107 · 배위수 9.6 — 130 은 0.079 · 4.75)
  이 구 부피 합에서 두 번 세어진다.  수확 · 덱 결함 아님: sha 64/64 · 같은 step 메시 64/64 · 웹앱 `calc_porosity` 직접 호출 교차검사 SAME 64 (4.6e-14 %p).
  130 의 음수 18 중 17 도 같은 영역 (SE/고체 0.5–0.6) · 두 세트가 겹치는 SE/고체 0.5–0.6 에서 중앙 −1.34 vs −1.21 % (한 곡선).
- union 실측 (`docs/data/lhs_union_20260927/`, `scripts/lhs_union_webapp.py`): **194 건 전부 양수** · 정확한 union 중앙 130 **13.60 %** · lhsx **6.55 %** ·
  웹앱 쌍 렌즈 + 벽 밖 제거 ≈ 정확 (차 중앙 0.004 %p) · 이 도구가 원본에서 다시 잰 sphere · 두께 · SE/고체 가 수확 JSON 과 1e-13 까지 같다.
- 사용자 지적 (09-27): 복합체가 순수 SE 보다 치밀한 것은 이원 충전 물리다 → 내 *"SE 영역에서 DEM 이 과압축"* 표현은 근거 부족으로 **철회**.
  남은 몫 (희석 추정보다 1–3 %p 더 치밀) 은 판정 시험 `docs/reviews/pure_se_union_prereg_20260927.md` 가 가른다.
- 새로 보인 것: 같은 SE/고체에서 **SE 가 클수록 SE–SE 가 상대적으로 더 깊이 겹친다** (δ/d 편상관 +0.79 lhsx · +0.32 130) — 판정 시험 Q3.
- 실험 앵커 정정: *"Minnmann 순수 SE 10 %"* 는 보정 표적이다 (`SELF-52`) — 실측 띠 8–19 % (Ohno 2020 6 연구실 13.3 ± 5.3 % 등).
- 제안 (**비준 대기 · 코드 변경 없음**): 인계표에 ① 정확한 union 을 **전 행** 물리 porosity 열로 (ε_sphere 는 J1 대로 기록 열 — 행마다 골라 쓰지 않는다:
  오차는 음수 전부터 연속이고 전환점에 계단이 생긴다) ② **질량 보존 두께** = 두께 × (1 − ε_sphere)/(1 − ε_union) 열 (비 중앙 1.043 · 1.118 — DEM 에서 겹친 부피는
  사라지므로 union 과 DEM 간격을 둘 다 실제 값으로 받을 수 없다) ③ φ_SE · φ_AM 의 union 판 — AM–SE 겹침 배분은 저자 결정 (MC 로 SE 만 · AM 만 · 둘 다 부피를
  이미 쟀다) ④ `NEGATIVE_POROSITY` 는 *"구 부피 합 규약 퇴화"* 표지로 남기고 물리 타깃 적격성은 union 기준으로 — 판정 시험 결과를 보고 확정.

- ✅ **비준 (1저자 09-28)** — 제안 ① (union 을 전 행 물리 porosity 열로 · ε_sphere 는 기록 열 그대로) · ② (질량 보존 두께) + SE-rich 표지.
  ③ (φ union 판) · ④ (적격성 union 기준) 는 **비준 범위 밖** — 안 했다.  구현 = `scripts/lhs_design_dataset.py` (셀프테스트 ⑱ · 옛 코드에서 실패 재현 뒤) ·
  기본 수확을 `lhs_descriptors_20260925` 로 (0924 판엔 `handover_qc` 가 없어 HND-04 열이 빈칸이었다 — J18 의 *"재수확 v2 뒤 인계표 재생성"*).
  재생성 인계표 = `docs/data/lhs_handover_20260928.csv` — ⛔ **배포 보류는 그대로** (아래 인계 판정).  SE-rich 문턱 0.50 = 도구 선택 (⬜ 저자 확인).
  ★ 재생성 인계표 (130 행 × **119 열** = 0919 판 63 + HND-04 49 + J19 7) 는 0919 판과 **공통 열 값이 다르다** — 0919 판은 바닥을 덤프 상자에서 잰 옛 수확 (LHS-10 · 11) 이고
  이 판은 재수확 v2 (`lhs_descriptors_20260925` = 0924 와 공통 값 Δ 0) 다: ε_sphere 중앙 **47.28 → 9.89 %** (−2.43 … 27.07 · 음수 0 → **18**) · union 중앙 **13.60 %** (6.07 … 28.81) ·
  질량 보존 두께 / 벽 간격 중앙 **1.043** (1.015 … 1.114) · SE-rich 21 행.  = J2 · J18 이 요구한 *"재수확 v2 뒤 인계표 재생성"* 그것이다.

## J20. ✅ 파라미터 채우기 (웹앱 파이프라인 그대로) · 벽 기준 τ 새 열 · 배포 (**비준 09-28 · 코드 구현 — WSL 실행 대기**)

- 요청 (1저자 09-28): 전수 판정 (`docs/param_audit_report_20260919.md` §2) 의 ✅ 파라미터 — 접촉 위상 (z_SE-SE · z_AM-SE · AM_P-SE CN ·
  surface-weighted · z_AM-AM · 접촉 수) · 퍼콜 (SE 성분 · top↔bottom · f_SE^sep · AM 퍼콜 · f_AM^cc) · 협착 분율 · CV(σ_VM) · σ_VM 비 ·
  F1 근접쌍 · Auerbach force-based · A_dem_geometric 면적 · 피복 — 를 인계표에 **채운 뒤** 수영 님께 넘긴다.
- 비준 (09-28, 네 권고 전부): ① **벽 기준 τ 새 열** (옛 τ 열은 그대로 보류) ② **채운 뒤 넘김** (README 와 함께) ③ SE-rich 문턱 **0.50 유지**
  (J19 의 ⬜ 닫힘) ④ **✅ 만 이번에** — 🔧 Physics 피복 (DESC-03 · L1-01 · L1-02 를 함께 고쳐야 한다 · DESC-10) 은 10/2 보고 뒤.
- 경로 — 새로 구현하지 않는다 (규율 ①): 웹앱 `run_pipeline` 을 **그대로** 부르는 배치 `scripts/lhs_webapp_batch.py` (그림 · 자동 DB 만 뺀다 —
  `run_pipeline(figures=False, auto_db=False)` · `webapp/test_pipeline_provenance.py` T9: 계산 단계 순서 동일) + 코퍼스와 같은
  `export_master_csv.row_for` ⇒ **열 이름 = case_master**.  DESC-01 (τ 가 없으면 φ 둘을 버린다) 은 φ 에만 걸리고 φ 는 수확기 값이 정본이다.
- 같은 프레임 (fail-closed): 네 파일 (atom · contact · 같은 step mesh · deck) sha = 수확 JSON · type_map 덱 판독 = 수확 JSON · 스테이징 청소 ·
  인계표 생성 때 **웹앱 porosity − 수확 porosity ≤ 0.05 %p** (같은 식이라 같은 프레임이면 ~1e-13, 다른 프레임이면 수 %p — LHS-11).
- 벽 τ (`lhs_descriptor_harvest.py`, 규약 `harvest_v3/wall_z0_plate/rSEmax/no_fallback/same_component`): 밴드만 바닥 벽 (z = 0) · 플래튼이고
  표본 규칙 · seed 는 옛 τ 와 **같은 함수** (`_tau_sample`).  selftest ⑰ — 벽 아래 AM 이 옛 밴드를 비우는 침대에서 새 τ = 1 (곧은 기둥) · 진짜 미관통은
  NOT_PERCOLATING · 두 밴드가 같은 침대에서 두 τ 동일 · **옛 τ 는 옮기기 전 값 그대로** (무작위 900 SE 2.0612290410739833 · 사슬 1.0198039027185568).
  ↪ 10-01: 고정값 (다른 기계에서 적은 수) 과의 비교는 **4 ULP 안** (`_ulp_close`) — WSL numpy 2.5.2 · Codex Windows 2.3.5 에서 median 이 1 ULP 달라
  이 회귀가 실패했다 (계산 결함 아님 · 환경).  반례 ⑰u 먼저 (1 ULP 이웃 수용 · 100 ULP 거부 · None/NaN 거부) · 같은 실행 안의 같은 계산끼리 (벽 τ = 옛 τ) 는 그대로 비트 동일.
  진단 (0925 수확): 벽 밴드를 잇는 SE 성분이 있는 침대 **106/130** (옛 규약 τ OK 는 14).
- 인계표 생성기 (`lhs_design_dataset.py --export-handover … --webapp DIR`): ✅ 열만 (🔶 σ · fallback · 웹앱 τ · MPM · Stage E · 🔧 Physics 제외) ·
  이름 충돌 (`phi_se` · `phi_am` · `plate_z_source`) 은 **수확 열이 정본** · 행마다 `wa_status` (done · partial · failed · REFUSED — 아니면 웹앱 열 빈칸) ·
  배치가 시도하지 않은 설계행이 있으면 거부 · 수확 세대 혼합 (벽 τ 일부만) 거부 · **열 사전** `<출력>_columns.tsv` (출처 · 판정 · 뜻 · 주의 —
  이름 주의 35 열은 A_dem_geometric · δ-based 파괴 열은 "force-based 와 나란히 인용 금지").  selftest ⑲a–n (78/78) · 옛 인자로는 09-28 인계표와 **바이트 동일**.
- 실행 (WSL): `ONE=lhs00_000 bash scripts/run_lhs_fill_wsl.sh` (한 건 — 실제로 도는지 · 한 건 시간) → `bash scripts/run_lhs_fill_wsl.sh` (전 건 ·
  재개 안전) → `~/lhs_fill_<날짜>.tar.gz` 를 받아 커밋 · 인계 README 작성 · 배포.
- ⚠ 남는 한정: ① `physical_target_status` HOLD 59 · 음수 ε_sphere 18 은 그대로 (J18 · J19) ② 🔧 Physics 피복 · σ_e · κ 는 이번 인계에 없다
  ③ 웹앱 열의 뜻은 **코퍼스와 같은 계산**이라는 것이지 추가 검증이 아니다 — 09-19 판정의 한정어 (이름 주의 · force/δ) 가 그대로 따라간다.

## J20-a. ⏸ 일괄 실행 보류 — ✅ 열을 **묶음별로 코드 정의부터** 감사 (1저자 09-28 밤)

- 지시: *"아직 다 일괄적으로 뽑지 말고 하나하나 코드 확실하게 수정/갱신한 다음에 하려 했어 — 지금 같은 porosity, union 같은 경우가 생길 수 있으니까"*
  · *"z_SE-SE mean, z_AM-SE 요런 식으로 좀 보고"*.  ⇒ J20 의 WSL 실행 순서 (`run_lhs_fill_wsl.sh` 전 건) 는 **감사가 끝날 때까지 보류**.
- ⚠ 09-19 전수 판정의 ✅ `SAFE` 는 *"Hertz/Physics cap 선택과 무관 (Δ = 0 %)"* 이라는 **좁은 검사**였다 — 분모 · 접촉 기준 · 벽 · 프레임 같은
  **정의**를 감사한 것이 아니다 (J20 한정 ③ 과 같은 말).
- 묶음 순서: ① 접촉 위상 → ② 퍼콜레이션 → ③ φ_SE → ④ 협착 저항 분율 · σ_VM → ⑤ F1 근접쌍 → ⑥ Auerbach 힘 기반 → ⑦ A_dem_geometric.

### ① 접촉 위상 — 1차 감사 (코드 읽기 + 합성 프로브 · 실데이터 미확인)

| 열 (UI 이름) | 코드 | 정의 |
|---|---|---|
| `se_se_cn` · `_std` (z_SE-SE mean · σ) | `dem_analysis_core.py:232-279` | SE **전 입자**의 SE 이웃 수 평균 (접촉 0 · 벽에 닿은 입자 포함) · 모집단 std |
| `am_se_cn_mean` (z_AM-SE) | `:710-742` | AM **전 입자** (P + S) 의 SE 접촉 수 평균 = **개수 가중** |
| `AM_P_se_cn_*` · `AM_S_se_cn_*` | `:749-764` | 상별 mean · std · median · max · 상이 없으면 키 없음 (= N/A, 0 아님) |
| `am_se_cn_surface_weighted` | `:766-778` | Σ r²·CN / Σ r² (AM 전 입자) |
| `am_am_cn` · `_std` · `am_am_n_contacts` | `:347-375` | AM 전 입자의 AM 이웃 수 (P–S 교차 포함) · 접촉 수 = Σ/2 |
| `area_<쌍>_n` | `:131-167` | 쌍 종류별 접촉 **행 수** |

공통: 접촉 = LIGGGHTS `pair/gran/local` 덤프 (`c_cpl`) 의 행 — 벽 · 플래튼 접촉은 없다 · 주기 경계 쌍은 `c_cpl[9]` 플래그 열이 있다 (포함 여부는 실데이터로 확인).
**코드는 행을 거르지 않는다** — 행마다 두 입자에 +1.

1. ⚠ **DESC-06 이 CN 에 직접 걸린다.**  웹앱 파서 (`parse_liggghts.parse_contact_file`) 는 파일 안 **모든 프레임을 이어 붙인다** (수확기는 마지막 블록만).
   합성 2 프레임 파일 → SE-SE CN **1.333 → 2.667 (정확히 2 배)** (스크래치 프로브).  배치는 수확과 같은 파일 (sha) 을 쓰지만 **파일 안 프레임 수는 검사하지 않는다**.
   ⬜ 130 접촉 덤프의 `ITEM: ENTRIES` 블록 수 실측.
2. ⬜ 한 프레임 안 **중복 쌍** (같은 id 쌍 두 번) · **δ ≤ 0 행** · periodic 플래그 분포 — 코드가 거르지 않으므로 있으면 CN 이 부푼다.  실데이터 확인.
3. **벽 효과 — 결함이 아니라 정의 주의 (porosity/union 과 같은 부류).**  벽 · 플래튼에 닿은 입자는 그쪽에 이웃이 없어 CN 이 낮다.  설계 d/T (설계 두께 추정 기준):
   SE 0.02–0.07 · AM_S 0.02–0.17 · **AM_P 0.10–0.52 (중앙 0.25)** — AM_P 는 두께가 입자 2–10 개라 `AM_P_se_cn` · 표면 가중 CN (r² 가중이라 AM_P 지배) 이
   **두께에 따라 체계적으로** 움직인다.  전극 전체 평균이라는 정의로는 맞지만, ML 이 두께 효과와 섞지 않으려면 벽 몫을 가를 열이 필요하다
   (제안: 상별 벽 · 플래튼 접촉 입자 분율, 또는 벽 인접 입자를 뺀 CN — 저자 결정).
4. **항등식 (DESC-07 과 같은 부류).**  `am_se_cn_mean` = (N_P·CN_P + N_S·CN_S)/(N_P + N_S) 는 정의상 정확 · 표면 가중은 상별 반경이 한 값이면
   (N_P r_P² CN_P + N_S r_S² CN_S)/(N_P r_P² + N_S r_S²) 로 정확 ⇒ AM–SE CN 네 열 중 **독립은 둘** (+ N · r).  인계 사전에 **"파생"** 으로 표시.
5. **접촉 수는 총량이다** (RVE 50 µm 고정 · 설계 두께 29–52 µm · 조성에 따라 입자 수가 다르다) — 특징으로 쓰려면 입자당 · 부피당으로 나눈다.
   `area_<쌍>_n` 은 **개수**인데 열 사전이 A_dem_geometric (면적) 주의를 붙인다 → 문구 수정 대상.
6. `A_binding_*_n_contacts` 는 Physics 모듈 (`coverage_physics_vs_hertzian.py:401-417` · 열린 P1 DESC-03 · L1-01 · L1-02) 이 센 수 — `area_*_n` 과
   같은 접촉 집합인지 한 건으로 대조 (다르면 거르는 행이 있다는 뜻).
7. (묶음 ⑤ 로 넘김) `se_se_cn_aug` (F1) 의 근접쌍 격자는 **x·y 주기 경계를 감지 않는다** (`:297-337`) — 경계 너머 근접쌍을 놓친다.

- 제안 (⬜ 비준 대기): ⓐ WSL **읽기 전용** 점검 — 130 접촉 덤프의 프레임 수 · 중복 쌍 · δ ≤ 0 · periodic 플래그 · 상별 벽 접촉 분율 (인계 값은 만들지 않는다)
  ⓑ 배치 관문 — 프레임 ≠ 1 · 중복 쌍이면 거부 (반례 셀프테스트 먼저) ⓒ 열 사전 정의 문구 (분모 · 벽 포함 · 파생 · 총량 · `area_*_n` = 개수)
  ⓓ 벽 분리 열 추가 여부 = 저자 결정.

### ① 비준 · 구현 (1저자 09-28 밤 *"권고하는걸로 진행하자"* · ⓓ = **상별 벽 접촉 비율**)

- 1저자 제안 반영 (09-28 밤): *"벽 넘어가도 … contact 파일에 flag 로 잘 되어 있으니까 그걸로 판단해서 CN 확인하면 되지 않나"* —
  옆면 (x·y) 은 주기 경계라 경계를 넘는 접촉은 `c_cpl[9]` 플래그와 함께 덤프에 있다 ⇒ 원자 좌표로 **최소영상 재계수**해 덤프 쌍과
  **쌍 단위로** 맞대면 CN 이 독립 검증된다 (플래그 의미까지).  ⚠ 바닥 벽 · 플래튼 (z) 은 주기가 아니라 그 너머 이웃이 없다 — 벽 효과는 ⓓ.
- ⓐ `scripts/lhs_contact_audit.py` (읽기 전용 · 인계 값 없음): 프레임 수 (접촉 · 원자) · 중복 무순서 쌍 · 자기쌍 · δ ≤ 0 · 주기 플래그 ·
  **기하 재계수** (기하에만 · 덤프에만 · 경계를 넘는 쌍 ↔ 플래그 행, 쌍마다 · 판정 경계 |d − Σr| ≤ 1e-6·Σr 는 따로) · 상별 CN
  (덤프 행 = 웹앱 방식 / 기하) · 상별 벽 접촉 비율.  selftest 14/14 — 반례 여섯 (다중 프레임 · 중복 · 주기 누락 · δ≤0 · 플래그 뒤바뀜 ·
  원자 다중 프레임) + 웹앱 경로 CN 2 배 실증.  rc 0 깨끗 · 3 어긋남 · 2 입력 오류.
- ⓑ `lhs_webapp_batch.stage_case` 관문: atom · contact **프레임 ≠ 1** · contact **중복 행 · 자기쌍** → REFUSED (실행 없음) ·
  점검 결과 (`contact_scan` · `atom_frames`) 를 status.json 에 남김 (δ ≤ 0 은 기록만).  **반례 시험 먼저** — ⑧–⑪ 이 옛 코드에서
  실패하는 것을 확인한 뒤 고쳤다 (추가 전 14/14 → 수정 전 14/18 → 수정 후 18/18).
- ⓒ 열 사전 (`lhs_design_dataset.wa_define`): CN = 전 입자 평균 · 벽 효과 주의 · **파생** (z_AM-SE · 표면 가중) · 접촉 **개수 = 총량**
  (`area_*_n` 의 면적 주의 제거) · Physics 모듈 접촉 수는 "같은 집합인지 대조 전".  09-19 판정 근거는 괄호로 남긴다.
- ⓓ 수확 v3 `wall_touch` (`lhs_descriptor_harvest.wall_touch_fractions` · 규칙 `WALL_TOUCH_RULE` = z − r ≤ 0 · z + r ≥ plate_z ·
  SE · AM_P · AM_S · 합친 AM) → 인계표 새 열 `wall_touch_frac_<상>_<floor|plate>` (없는 상 빈칸 · 수확 세대 혼합 거부).  벽 인접 입자를
  뺀 CN 은 택하지 않았다 — AM_P 가 두께 2–10 개인 침대에서 남는 입자가 거의 없어 정의가 흔들린다.
  수확은 새 키만 늘었다 (`wall_touch` · `contact_scan` · `n_atom_frames`) — status 키 · 옛 값 그대로 (selftest ⑱).
- ⬜ WSL 실행 (읽기 전용): `python3 scripts/lhs_contact_audit.py --selftest` → `--case lhs00_000 --out /tmp/audit_one` (한 건 시간) →
  `--out ~/lhs_contact_audit_<날짜>` (전 건) → `contact_audit.tsv` · `.json` 을 받아 판정 → ② 퍼콜레이션 묶음.
  ⚠ **실행 위치 (09-29 첫 시도 실패로 확인)**: WSL `~/Yonghoon-DEM-DFT` 는 **`claude/evac-2026-09-28`** 체크아웃
  (= `friendly-meitner-lldvar` 계열) 이라 이 브랜치의 스크립트가 없다 — 내 명령 블록이 브랜치를 주석으로만 적고 막지 않아
  `git pull` 이 *divergent* 로 멈춘 뒤 (**아무것도 합치지 않음**) 파이썬 세 줄이 "파일 없음" 으로 떨어졌다 (쓴 것 없음).
  ⇒ 그 체크아웃은 건드리지 않고 **분리 워크트리** `git worktree add --detach ~/dem-audit origin/claude/sdcp-dem-manuscript-si-pqwtv8`
  에서 돌린다 (인터프리터 `~/Yonghoon-DEM-DFT/venv/bin/python` — `cKDTree` 에 scipy 필요 · 조건 = `merge-base --is-ancestor 3e20d250f`
  + selftest 통과일 때만 본 실행).

### ① WSL 실측 v1 (09-29 · `~/dem-audit` 워크트리 `3e20d250f` · 131 행 · 한 건 3.0 s · 전 건 수 분) — 원자료는 깨끗 · **FLAG 113 은 감사기 v1 의 폭**

| 검사 | 130 건 결과 |
|---|---|
| 접촉 · 원자 프레임 수 | **전부 1** (DESC-06 의 CN 배가 경로는 이 코호트에서 실현되지 않는다 — 관문은 그대로 둔다) |
| 중복 행 · 자기쌍 · 고아 행 · δ ≤ 0 | **전부 0** |
| 경계를 넘는 접촉 ↔ 플래그 | 넘는데 플래그 0 = **0** (130/130) — 넘는 쌍 682,234 (기하) vs 플래그 행 691,370 |
| `perc` (131 번째) | INPUT_ERROR (원본 없음 · J10 과 같음) → rc 2 |
| **기하 ≠ 덤프 쌍** | **113 건 FLAG** — 케이스당 (경계 제외) 0 쌍 17 · 1–10 쌍 77 · 11–50 쌍 24 · 51–200 쌍 11 · 1,034 쌍 1 (`lhs00_023`) · 대부분 "덤프에만" |
| **플래그만 (경계 안 넘음)** | `lhs00_029` **4,065 행** · `lhs00_098` **5,024 행** — 나머지 128 건 0 |

- ⛔ **감사기 v1 결함 (원장 `SELF-63`)**: 판정 경계 폭 `1e-6·Σr` (= 0.01 nm) 은 덤프 자릿수보다 **좁다** — WSL 실측 `atom_2020000` 토큰
  `0.0304637 0.0148603 0.0042173 0.005` = LIGGGHTS `%g` **6 유효숫자** → x·y 마지막 자리 0.1 nm (반폭 0.05 nm/좌표) · z (< 10 µm) 0.01 nm.
  재계산 거리 오차 최대 ≈ 0.17 nm 이므로 겹침 < 0.2 nm 인 쌍은 어느 쪽으로도 갈린다.  LIGGGHTS 는 전 정밀도로 판정하므로 **틀린 쪽은
  재계산이고 웹앱 CN (덤프 행 기준) 이 옳다**.  ⚠ 이것은 가설이었고 **비준 없이 CLEAN 으로 바꾸지 않았다** — v2 가 쌍마다 판별한다.
- **`c_cpl[9]` 의 뜻 (LIGGGHTS-PUBLIC master 원문 09-29 열람)**: `compute_pair_gran_local.cpp` add_pair — `tag[i] · tag[j]` 다음 값은
  두 입자가 다 local 이면 0, 아니면 `is_periodic_ghost(i) || is_periodic_ghost(j)`; `domain_I.h` `is_periodic_ghost` = 고스트 (i ≥ nlocal)
  이고 어느 **주기** 축에서 `x < boxlo + cutneighmax` 또는 `x > boxhi − cutneighmax` 이면 1.  ⇒ 직렬 런은 고스트 = 주기 영상뿐이라
  플래그 = 경계 넘음 (128/130 실측 정합).  **MPI 런은 내부 분할면 너머의 고스트 (상자 안) 도 주기면 띠 (cutneighmax = 2 r_max + skin
  = 2·5 + 2 = 12 µm — 50 µm 상자의 24 %/면) 안이면 1** ⇒ `029` · `098` 의 "플래그만" 행 = 분할면을 걸친 쌍 중 고스트가 띠 안인 것
  (가설 — ibb 로그가 로컬에 없어 격자는 덤프에서 추정한다).  ⚠ ibb/WSL 빌드 (3.8) 와 master 의 동일성은 미확인.
  인계 값에는 **무영향** — 리포에서 `periodic_flag` 를 쓰는 소비자가 없다 (`parse_liggghts` 가 이름만 붙인다 · grep 0).  원장 `LHS-16`.
- 실물 실증 (합성 · 이 세션): 6 만 입자 · 75,208 접촉 쌍을 정밀 좌표로 만들고 `%g` 로 써서 v2 에 넣으면 **반올림으로 갈린 쌍 정확히 2** ·
  δ 불일치 최대 1.39e-7 ≤ 폭 1.57e-7 → CLEAN · 1.7 s.  = 실물에서 본 "덤프에만" 이 이 기전으로 나오는 것을 재현.

### ① 감사기 v2 (09-29 비준 *"비준이고 너가 자기리뷰를 받아봐봐"* · 반례 먼저 · 자기리뷰 반영) — `lhs_contact_audit/v2`

- **반올림 폭** B 를 쌍마다 **토큰에서** 계산한다: S = 원자 덤프 전체의 최대 유효숫자 (문자열로 셈 · `%g` 가 끝 0 을 지우므로 토큰 자신의
  자릿수를 쓰면 `0.005` 가 5e-4 = 10⁵ 배 헐거워진다 — false-green 함정) · 반폭 h = 0.5·10^(지수 − S + 1) · 위치 폭 = 분리 벡터 방향 투영
  (Σ|u_k|(h_ik + h_jk))/|u| + 반지름 반폭.  판별: ① 덤프에만 g + δ ≤ B + h_δ ② 기하에만 o ≤ B ③ 양쪽 |δ − o| ≤ B + h_δ (**새 검사** —
  v1 은 양쪽 쌍의 δ 를 대조하지 않았다).  폭 밖 = far → FLAG · 폭 안 = rounding (불일치 아님) · 예시 5 쌍을 JSON 에 남긴다.
- **플래그만** 쌍: 덱 `neighbor` skin 으로 띠 = 2 r_max + skin (덱 없으면 fail-closed FLAG) · id2 (= 고스트 후보 — 이웃 루프의 i 는 항상
  local) 가 주기 축 띠 안인 수 · 전부가 균일 분할면을 걸치는 **최소** 격자 (x·y ≤ 8 · z ≤ 64) → 둘 다 성립해야 "설명됨" (CLEAN + note).
  ⚠ 설명됨은 "결함 아님 · 인계 무영향" 이지 MPI 실행의 증명이 아니다 — ibb 로그 `MPI processor grid` 줄이 있으면 그것이 정본.
- 반례 먼저 (옛 코드 = NameError/KeyError 로 실패 → 구현 → 24/24): ⑫ 반올림 폭 안 → rounding · ⑬ 폭 밖 덤프에만 · ⑬b 폭 밖 기하에만 ·
  ⑭ δ 불일치 · ⑭b 일치 · ⑮ 고스트 설명됨 (1x1x2) · ⑮b 띠 밖 → FLAG · ⑮c 덱 없음 → FLAG · ⑮d 플래그 0 → None.  v1 픽스처의 δ 는
  기하와 안 맞았는데 (임의값) ③ 이 잡아서 고쳤다.
- **자기리뷰 (서브에이전트 · 적대 · 09-29 · 12 항) 반영** — P1 ① 분할면 걸침에 허용오차가 없어 `%g` 토큰이 분할면 위에 떨어진 원자 하나가 전 격자를 죽였다
  (합성 2×2×16 실측 · 무작위 플래그 설명률은 τ 로 안 바뀜) → τ = 반폭 합 + skin/2 (소유권 지연) · P1 ② NaN δ 가 CLEAN → 비유한 값 행 · `~(δ > 0)` ·
  P2 ③ 유효숫자 바닥 6 (관측 최대는 하한) · ④ 원자 step = 접촉 step · ⑤ MPI 설명의 정박 — `processors` 줄을 격자 제약으로 · **충분성** (격자가 플래그를
  예측하는 쌍에 플래그가 빠지면 FLAG) · 이름 `mpi_grid_min` (분해의 증명 아님 · 실행 기록 없음을 note 에) · ⑥ `run()` 이 RAW_OK 외 행을 SKIPPED ·
  봉인 sha256 대조 · rc 3 (FLAG) > 2 · ⑦ 같은 step 메시 없음 = NO_MESH (CLEAN 아님) · ⑧ 플래그 · δ 열 없음 = FLAG · ⑨ `neighbor` 마지막 줄 ·
  ⑪ newton off 규칙 (플래그 행 id1 > id2) · 상자 플래그 pp pp ff · NUMBER OF ENTRIES = 읽은 행 · ⑫ orphan_rows 열 · bound_max 전 쌍.
  반례 ⑯–㉒b 먼저 → 34/34.  리뷰가 짚은 사실 하나를 옮겨 둔다: 기본 분할 `1 by 1 by N` 의 첫 분할면은 z = −0.01 + 1.01/N 이라 **N ≤ 25 면 침대
  (27–40 µm) 위**다 ⇒ `029`·`098` 의 수천 행은 rank ≥ 26 이거나 명시 `processors` 줄을 뜻한다 — 덱의 processors 줄 (감사기가 적는다) 로 가른다.
- ✅ **WSL v2 실측 (09-29 · 1저자 · HEAD `acab799c4` · rc 0)** — 130/130 **CLEAN** · SKIPPED 1 (`perc`).  요약: 프레임 1 · 중복 0 · 자기쌍 0 · 고아 0 ·
  δ≤0 0 · 비유한 0 · **far 0 · δ 불일치 0** · 반올림 쌍 있음 114 건 (최대 1,090 · `lhs00_023`) · 유효숫자 관측 6 (전 건) · 폭 최대 1.83e-7 mm ·
  경계 넘는데 플래그 0 = 0 · newton off 규칙 위반 0 · **플래그만 2 건 = `029` 4,065 · `098` 5,024 — 둘 다 설명됨** (id2 띠 안 100 % · 최소 설명 격자
  **1x1x24 · 1x1x30** · 예측 누락 0 · 띠 0.011 / 0.013).  ⇒ v1 의 FLAG 113 은 전부 감사기 폭이었다 (`SELF-63` 검증) · `LHS-16` 가설 정합 (실행 기록은 없음).
  ⬜ `contact_audit.json` 반입 → `docs/data/lhs_contact_audit_20260929/` (sha 기록).

### ① 판정 — 접촉 위상 묶음은 인계 적격 (코드 정의 감사 + 실물 130 건 검증)

| 열 | 판정 | 근거 · 한정어 |
|---|---|---|
| `se_se_cn_mean` (z_SE-SE) · `am_se_cn_*` (z_AM-SE) · `AM_P/AM_S_se_cn_*` · `am_am_cn_*` (z_AM-AM) | ✅ | 덤프 = 한 프레임 · 쌍마다 한 행 · 접촉만 · 기하와 반올림 안에서 일치 (130/130) · 분모 = 상의 **전 입자** (접촉 0 · 벽 접촉 포함 — 열 사전) |
| 표면 가중 CN · `am_se_cn_mean` (수 가중) | ✅ (파생) | 상별 CN 의 대수 함수 — 열 사전에 파생으로 표기 |
| 접촉 개수 (`area_*_n`) | ✅ (총량) | RVE 50 µm 고정 · 두께 29–52 µm ⇒ 크기에 비례 — 열 사전 |
| `wall_touch_frac_<상>_<floor\|plate>` (ⓓ 새 열) | ✅ | 벽 효과의 설명 변수 (z 는 주기가 아니라 CN 이 낮은 것은 정의상) |
| `c_cpl[9]` 플래그 | — | 인계 열 아님 · 소비자 없음 · `LHS-16` |

⛔ 이 판정은 **① 묶음의 열**에 한한다 — ② 퍼콜레이션 이후 묶음은 각자 감사한다.  일괄 실행 (`run_lhs_fill_wsl.sh`) 은 여전히 보류.

## J20-b. ② 퍼콜레이션 묶음 — 1차 감사 → ✅ WSL 실측 130/130 CLEAN (09-29) → **② 판정 = 명목 정의 그대로 인계 적격** (규칙 ⓑ · ⓒ 열 사전 문구 · ⓓ `LHS-20` = 비준 대기)

대상 열 (09-19 census ✅): `percolation_pct` · `n_components` · `n_large_components` (SE 이온 · `dem_analysis_core.calc_percolation`) ·
`electronic_active_fraction` · `electronic_percolating_fraction` (AM 전자 · `network_conductivity.build_network` + `run_decomposition` 의 성분 셈) ·
`se_se_cn_perc` · `se_se_cn_n_perc` · `se_se_cn_eff_area_perc` (`calc_se_se_cn` — 관통 SE 부분집합).  (+ 🔶 `top_reachable_pct` · `ionic_active_pct` — F4.)

### ② 정의 (코드 그대로 — `dem_analysis_core.py:380–460` · `network_conductivity.py:179–249` · `active_fractions` (옛 `run_decomposition:1101–1120` 에서 추출))

| 항목 | SE (이온 · `calc_percolation`) | AM (전자 · `build_network`) |
|---|---|---|
| 그래프 | 접촉 덤프 **행마다** 양끝이 SE 면 간선 (면적 · δ 로 거르지 않음) · **모든 SE 가 노드** (외톨이 = 크기 1 성분) | AM_P + AM_S **한 상** · 양끝 AM · `ca > 0 or δ > 0` 인 행만 (① 실측 δ > 0 전 행이라 실효 없음) · 성분 셈 `G_active` 는 **간선 있는 노드만** (외톨이는 active/percolating 에서 빠짐) |
| 바닥 밴드 L0 | z_i ≤ 2·r_i — **바닥 벽 = z 0 을 암묵 가정** (확인 없음) | 같음 |
| 위 밴드 L0 | z_i ≥ plate_z − 2·r_i — plate_z = `mesh_info.json` (STL 꼭짓점 z 평균 · 평판 검사 없음 `HND-06`) · 없으면 최고 입자 중심 | 같음 |
| ★ 폴백 | 어느 한쪽 밴드가 **3 개 미만**이면 **두 밴드를 함께** L1 (z ≤ 0.15·plate_z · z ≥ 0.85·plate_z) 로 → 여전히 3 미만이면 L2 (관측 SE z-범위의 15/85 %) — **어느 단계가 쓰였는지 산출물에 없다** | 같은 규칙 (관측 범위 = AM) · `n_boundary_overlap` 은 재지만 **어느 채널 것도 full_metrics 에 안 올라간다** (`pipeline_service.NET_MERGE_KEYS` 에 경계 키 없음 · 이온 것은 `network_conductivity.json` 에만 · 전자 것은 어디에도 없다 — 자기리뷰 #9 정정) |
| 관통 | 성분이 두 밴드에 다 닿음 → `percolation_pct` = 관통 SE / 전 SE · `top_reachable_pct` = 위 밴드 닿는 성분의 SE / 전 SE (**위 밴드에 앉은 외톨이 포함**) | `percolating_fraction` = 관통 AM / 전 AM · `active_fraction` = 바닥 닿는 성분의 AM / 전 AM |
| 그 밖 | `n_components` = 성분 수 (**외톨이 포함**) · `n_large_components` = 크기 ≥ **10** 성분 수 (코드 안 상수 · 출처 없음) · `se_se_cn_*_perc` = 관통 SE 만의 CN · 면적 CN (관통 0 이면 **키 자체가 없음** → 빈칸) | — |

### 발견 (원장 `LHS-17` ~ `LHS-20`)

- **F1 (P2 · `LHS-17`) 조용한 경계 폴백.**  L1 · L2 가 발동하면 같은 열 이름이 **다른 정의**로 채워지는데 기록이 없다 (`calc_percolation` 과
  `build_network` 가 같은 코드).  LHS 규모: SE 밴드 = 2·r_SE = **1–2 µm** (d_SE 1.0/1.5/2.0) · AM 밴드 = 2·r_i (AM_S 1–5 · AM_P 5–15 µm).
  빈도는 실측 전 **미상** — SE 가 적은 설계점 (am_pct 95 · mono_AM_P) 과 AM_S 만 있는 얇은 밴드에서 가능.  ⇒ 검사기가 케이스마다 단계 · L0 인원을 센다.
- **F2 (P3 · `LHS-18`) bottom∩top 겹침 인공물.**  두께 < 4·r 이면 한 입자가 두 밴드에 동시에 들고 그 성분은 **통째로 관통**이 된다 (간선 0 인 외톨이
  셋만으로 `percolation_pct` = 100 — 합성 재현 selftest ④ · 생산 실사고 P600 부류).  LHS 는 **기하상 0 건** (벽 간극 두께 − 4·r_AM,max 최소 **+1.47 µm** ·
  `lhs00_075` · SE 는 r ≤ 1 이라 불가) — 실측으로 확인만.  겹침 수가 full_metrics 에 안 올라가는 것 (이온은 network JSON 에만 · 전자는 어디에도 없음) 은 그대로 등재.
- **F3 (P3 · `LHS-19`) 열의 뜻이 이름과 다르다 (열 사전 대상).**  `n_components` 는 외톨이 SE 를 성분으로 센다 — 단절 침대는 SE 의 **최대 49 %** 가
  무접촉 (`LHS-06`) 이라 이 열은 사실상 **외톨이 수**다 · `n_large_components` 의 10 은 출처 없는 관례 · `top_reachable_pct` 는 위 밴드의 외톨이도 센다
  (합성: 관통 11/15 인데 top_reach 13/15) · `se_se_cn_*_perc` 는 비관통이면 빈칸 (= N/A · `DESC-05` 부류) · RVE 50 µm 고정이라 성분 수는 두께에 비례 (총량).
- **F4 (P3 · `LHS-20`) census 오분류.**  09-19 census 가 `top_reachable_pct` · `ionic_active_pct` 를 `COND_cov` (*"coverage 문턱 기반 → Hertz 채널 종속"*) 로
  적었는데 둘 다 **SE 그래프 양**이다 (coverage 무관 — `calc_ionic_active_am` 은 AM–SE **접촉 유무**와 top-reachable SE 만 본다).  방향은 보수적 (인계에서 빠짐).
  생성 규칙을 리포에서 찾지 못했다 (census 생성 스크립트 없음).  승격 여부 = **저자 결정**.
- **F5 (정보) 바닥 z = 0 암묵.**  웹앱은 덱을 보지 않는다.  수확기 `check_deck_floor` 가 130/130 에서 z = 0 을 확인했고 (J16), 검사기가 케이스마다 재확인한다 (덱 없으면 fail-closed FLAG).
- **F6 (정보) 수확기 AM perc 와 웹앱 전자 관통은 다른 정의다.**  수확기 `lhs_perc_extract.percolation` = 고체 외피 (min(z−r) · max(z+r)) 기준 슬래브 t = r_AM,max ·
  **표면** 기준 · **기하** 접촉 (d ≤ Σr) · 폴백 없음 ↔ 웹앱 = 벽/플래튼 기준 2·r_i **중심** · **덤프** 접촉 · 폴백 있음.  작은 AM_S 에는 수확기 밴드가 훨씬 넓다
  (r_max 7.5 vs r_S 0.5 µm).  09-15 생산 팔 `ionic_percolates` (25/127 False) 는 **솔버 결과** (`ionic_status` OK vs SOLVE_NONE) 이고 그 그래프는
  `ca > 0 or δ > 0` 행만 · 간선 있는 노드만 (`G_active`) 이라 `calc_percolation` (거르지 않음 · 외톨이 포함) 과 **LHS 에서만** 일치한다 (① 실측 δ > 0 전 행 ·
  겹침 0 일 때) — 그 밖에 plate_z 시점 (LHS-11 이전 메시) 이 다를 수 있다 (자기리뷰 #9 한정어).
  ⇒ 검사기가 **접촉 원천 {덤프 · 기하} × 경계 규칙 {웹앱 · 수확기}** 2×2 로 불일치를 귀속한다 (밴드 · 접촉 · 둘 다).
- **F7 (정보 · τ 묶음으로 이월) 상자 크기.**  ~~배치는 `input_params.json` 을 만들지 않아 웹앱이 0.05 기본을 쓴다~~ — **틀린 서술이었다** (자기리뷰 #9 · `SELF-64`):
  배치가 덱을 `input_<case>.liggghts` 로 잇고 `run_pipeline` 이 `input*.liggghts` 를 `parse_liggghts` 에 넘겨 `parse_input_script` 가 `region reg_box block 0.0 0.05 …`
  에서 box_x/box_y 를 읽어 `input_params.json` 을 **쓴다** (`webapp/app.py:3184` · `parse_liggghts.py:335–340`).  ⇒ 웹앱 상자 = 덱 상자 (0.05 · RVE 50 µm 130/130).
  검사기의 `box_is_lhs_rve` 는 덤프 상자와 0.05 의 **대조**일 뿐이다.  ② 값은 무영향 (간선 거리 가중만) · τ (`LHS-08`) 에서 다시 본다.
- **F8 (정보) 독립 재현 경로.**  SE 가 단분산이면 웹앱 L0 밴드 (z ≤ 2r · 중심) 와 수확기 벽 밴드 (`tortuosity_se` — z − r ≤ 0 + r_max · 표면) 는 **같은 집합**이다
  ⇒ 수확기 `wall_n_span_components > 0` 이 웹앱 `percolation_pct > 0` 의 독립 재현 (접촉 원천만 다름).  검사기가 케이스마다 같은 집합인지 단언한다 (다르면 재현 오류 FLAG).

### 검사기 `scripts/lhs_perc_audit.py` (읽기 전용 · 인계 값은 만들지 않는다 · selftest 23 건)

- 케이스마다: 프레임 · 고아 행 · 덱 바닥 · plate_z (수확과 같은 정의) → SE/AM **경계 단계 L0/L1/L2 · L0 인원 · 쓰인 인원 · 겹침** → 성분 통계
  (관통 · top_reach · 성분 · 외톨이 · ≥10 · 최대) → **재현 ↔ 정본 대조** (웹앱 `calc_percolation` 값 · 밴드 집합 · `calc_se_se_cn` 관통 키 · `build_network`
  밴드 집합 · 간선 수 · 겹침 · `network_conductivity.active_fractions` (run_decomposition 이 쓰는 함수 그대로 — 복사본 아님) · 수확기 `percolation` 슬래브 인원 · perc) —
  하나라도 다르면 FLAG (내 판독을 정본이 검증) · 중복 행 · 자기쌍 (`scan_contact_dump` — ① 과 같은 함수) · 선언 수 ↔ 읽은 행 · 메시 sha256 기록 →
  2×2 귀속 (SE · AM) → legacy 09-15 대조.  FLAG = 폴백 발동 · 겹침 · 재현 불일치 · 덱/프레임/고아 (그 케이스의 열 정의가 명목과 다르다는 뜻 · 원자료 결함 아님).
- 반례 먼저 (selftest): L1 ② · L2 ③ · 겹침 인공물 ④ · ≥10 문턱 ⑤ · 귀속 band ⑥ · contact ⑦ · 비관통 키 없음 ⑧ · 덱 바닥 ⑨ · 다분산 ⑩ · 프레임/고아 ⑪ ·
  **변이 ⑫ (재현 폭만 3.0 으로 바꾸면 정본과 어긋나 FLAG)** · CLI ⑭ · 2-type ⑮ · 정본 `run_decomposition`/`tortuosity_se` 와 분율·성분 일치 ①f·①g.
- ⚠ 시간 (자기리뷰 실측 · 합성 150,006 입자 / 441,500 행): AM 주 침대 12.2 s · 1.3 GB (`build_network` 5.3 s) · SE 주 침대 6.9 s · 0.8 GB ⇒ 130 건 ≲ 30 분
  (실물 덤프는 열이 26 개라 읽기가 더 무겁다 — +0.5–1 GB 예상).

### 자기리뷰 (적대 서브에이전트 · 09-29) — 9 항 전부 반영 (반례 먼저 · selftest 23 → 32)

| # | 판정 | 반례 | 반영 |
|---|---|---|---|
| 1 | P2 | 중복 행 · 자기쌍 행이 CLEAN — `calc_se_se_cn` 은 행마다 세서 `se_se_cn_perc` 1.818 → 2.0 / 2.364 로 부풀고, ① 감사는 같은 파일을 FLAG (모순) | `scan_contact_dump` (① 과 같은 함수) → FLAG ⑯ |
| 2 | P2 | 토큰 수가 다른 원자 행을 모든 파서가 조용히 버린다 — `NUMBER OF ATOMS` 와 대조하지 않았다 | 선언 수 ↔ 읽은 행 (atom · contact) ⑰ |
| 3 | P2 | 전자 분율을 **복사본** (`_electronic_fractions`) 과 대조했다 — 정본 `run_decomposition` 이 바뀌어도 초록 | 셈을 `network_conductivity.active_fractions` 로 **추출** (동작 중립 · NC selftest 29/29) · 감사기가 그 함수를 부른다 ⑱ (정본을 바꾸면 FLAG) |
| 4 | P2 | `_xcheck` 가 정본 둘만 같으면 'agree' — 기하 지지 없는 덤프 행 하나로 웹앱 관통이 서도 'agree' | 네 칸 전부 같을 때만 'agree' · 그 밖은 `prod_agree:` / `prod_differ:` + 축 · 웹앱 값이 접촉 원천에 기대면 note ⑲ |
| 5 | P2 | 감사된 케이스 0 (전부 SKIPPED) 이 rc 0 "전부 CLEAN" | rc 2 ⑳ |
| 6 | P3 | AM 자기쌍이 "재현 오류" 로 읽힌다 | #1 + 불일치 문구에 원인 명시 |
| 7 | P3 | legacy `TRUE`/`1` 이 조용히 미대조 · `case_id` 열 없으면 산출물 없이 중단 | true/false/1/0 · 모르는 값 거부 · rc 2 ㉑ |
| 8 | P3 | rc 3 이 INPUT_ERROR (rc 2) 를 가린다 | ① 과 같은 규약으로 **명시** (docstring) — 요약 `status` 에 수는 항상 남는다 |
| 9 | P3 | 문서 서술 셋이 코드와 다르다 — "이온 겹침만 병합" (둘 다 안 됨) · F7 "input_params.json 부재" (배치가 덱을 넘겨 **만든다**) · F6 "같은 규칙" (솔버 결과 · LHS 에서만 일치) · 분율 4 자리 반올림 · 줄 번호 | 본 절 정정 · `SELF-64` |
| 의심 | — | 메시 sha 미봉인 · 예상 밖 예외에 산출물 없음 · `np.mod` 경계 | 메시 sha 를 행에 기록 ㉒ · 예외 → INPUT_ERROR 행 + 기록 ㉓ · `np.mod` 는 수확기 함수 (INPUT_ERROR 쪽 · false-green 아님 — 그대로) |


### 권고 (비준 요청) — 순서: WSL 실측 → 판정 → 열 사전 → ③ φ_SE

- ⓐ WSL 130 건 실행 (읽기 전용 · `~/dem-audit` 워크트리 · 이 커밋 이후):
  ```
  cd ~/dem-audit && git fetch origin claude/sdcp-dem-manuscript-si-pqwtv8 && git checkout --detach origin/claude/sdcp-dem-manuscript-si-pqwtv8 && git log -1 --oneline
  ~/Yonghoon-DEM-DFT/venv/bin/python scripts/lhs_perc_audit.py --selftest
  ~/Yonghoon-DEM-DFT/venv/bin/python scripts/lhs_perc_audit.py --case lhs00_000 --out ~/lhs_perc_audit_one          # 한 건 (시간)
  ~/Yonghoon-DEM-DFT/venv/bin/python scripts/lhs_perc_audit.py --out ~/lhs_perc_audit_$(date +%Y%m%d)              # 전 건 · rc 0/3 둘 다 정상 종료
  ```
  받을 것: `perc_audit.tsv` · `perc_audit.json` (+ 화면 요약 줄).
- ⓑ 판정 규칙 (미리 적는다): 폴백 0 건 · 겹침 0 건 · 재현 전부 일치 ⇒ ② 열은 **명목 정의 그대로** = 인계 적격 (열 사전 한정어 F3 만).  폴백 n > 0 ⇒ 인계표에
  단계 열 (`perc_band_level_se` · `perc_band_level_am`) + 발동 케이스 표지 (값은 웹앱 규약 그대로 — 생산 코퍼스와 같은 정의) · 저자 결정.  겹침 n > 0 ⇒ 그 케이스의
  전자 열 HOLD 표지.  2×2 불일치는 판정에 안 쓰고 **기록** (수확기 AM perc 는 인계 열이 아니다).
- ⓒ 열 사전 문구 (F3) — 판정 뒤 생성기 `column_dictionary` 에 반영.  ⓓ census 오분류 (F4) — 저자 결정.
- ⛔ 값 산출 (`run_lhs_fill_wsl.sh` 전 건) 은 여전히 보류.

### ② WSL 실측 (09-29 · 1저자 · `~/dem-audit` 워크트리 `c0c2d4f44` · selftest 32/32 · 131 행 · 전 건 309.7 s · 한 건 1.4–5.9 s) — **130/130 CLEAN · rc 0**

산출물 (저자 기계): `~/lhs_perc_audit_20260929/perc_audit.tsv · perc_audit.json` · 한 건 `~/lhs_perc_audit_one/` (⬜ 반입 → `docs/data/lhs_perc_audit_20260929/`).

| 검사 | 130 건 결과 |
|---|---|
| 상태 · 판정 | OK 130 · SKIPPED 1 (`perc` · 원본 없음 · ① 과 같음) · **CLEAN 130 · FLAG 0** |
| 프레임 ≠ 1 · 중복 행 · 자기쌍 · 고아 행 · 선언 수 불일치 · 덱 바닥 | 전부 0 (FLAG 0 이 곧 그 뜻) · 덱 바닥 z = **0.0** 130/130 (`floor_z_deck`) |
| **경계 밴드 단계 (F1 · `LHS-17`)** | SE **L0 130/130** · AM **L0 130/130** — 폴백 L1 · L2 **0 건** (⇒ 이 코호트에서는 조용한 정의 변경이 실현되지 않았다) |
| **bottom∩top 겹침 (F2 · `LHS-18`)** | SE 0 · AM 0 · 수확기 슬래브 0 — 기하 예측 (최소 여유 +1.47 µm) 그대로 |
| 재현 ↔ 정본 (`calc_percolation` · `calc_se_se_cn` · `build_network` + `active_fractions` · 수확기 `percolation` · `tortuosity_se` 벽 밴드) | **130/130 일치** (`replica_ok_all` true) |
| 2×2 SE (접촉 원천 × 경계 규칙) | `agree` 130 |
| 2×2 AM | `agree` 128 · **`prod_differ:band` 2** (`lhs00_107` · `lhs00_110`) — 웹앱 밴드 (중심 z ≤ 2r) 는 관통, 수확기 슬래브 (표면 ≤ r_AM,max) 는 비관통 · 접촉 원천 (덤프/기하) 은 무관 = 밴드 규칙에만 귀속 |
| 덤프 ↔ 기하 접촉 차 (① 의 반올림 부류) | SE 기하에만 ≤ 7 · 덤프에만 ≤ 17 · AM 기하에만 ≤ 46 · 덤프에만 ≤ 1,032 (케이스 최대) — 관통 판정을 바꾼 케이스 **0** (`contact` 귀속 0) |
| SE 관통 (`percolation_pct` > 0) | **106/130** · 비관통 24 (0.0 %): `001 012 018 023 026 030 037 041 053 062 074 075 079 082 083 087 093 105 107 108 111 112 126 128` — 09-19 수확 진단 106/130 과 같은 집합 |
| AM 관통 (`electronic_percolating_fraction` > 0) | **130/130** (예: `000` 0.99703 · `009` 0.83178 · `107` 0.99992) |
| 수확기 AM `percolation` | 128/130 (위 107 · 110 만 비관통) |
| legacy 09-15 `ionic_percolates` (= 솔버 결과) | 대조 127 · 일치 126 · **불일치 1 = `lhs00_009`** (웹앱 밴드 규칙 SE 관통 99.993 % vs 솔버 False) = 원장 `LHS-04` 의 바로 그 케이스 (솔버 전극 규칙 · P1 open) · legacy 행 없음 3 (`034` `089` `098`) |
| 단분산 SE · 상자 | 다분산 0 (SE r 한 종류 ⇒ 웹앱 L0 밴드 = 수확기 벽 밴드 · `se_wall_band_equal`) · ⚠ 화면 요약의 `box_default_cases: 0` 은 감사기의 **낡은 키** (`box_is_webapp_default` 는 어느 행에도 없다 · 행 값 `box_is_lhs_rve` 는 옳다 · 원장 `SELF-65` · 같은 커밋에서 반례 ⑭e 먼저 → `box_not_lhs_rve_cases`) — 상자 판정은 TSV 열로 반입 뒤 확인 (설계상 130/130 RVE 50 µm) |

- 실행 순서 (ⓐ 명령 그대로): selftest 32 ✓ → 한 건 `lhs00_000: OK CLEAN SE L0 92.5356 · AM L0 0.99703 · 5.89 s` → 전 건.  코드 = `c0c2d4f44` (자기리뷰 반영판) — 실측이 곧 ⓐ 의 비준이다.
- ⚠ 이 실측은 **정의가 이 코호트에서 어떻게 실현됐는가** 를 말한다 — `LHS-17` (폴백 미기록) · `LHS-18` (겹침 인공물 · 경계 키 미병합) 의 **코드 결함은 그대로 open** 이다 (생산 코퍼스 · 다른 침대에서는 발동할 수 있다).  실측 0 건은 원장 note 에 적었다.

### ② 판정 — 퍼콜레이션 묶음은 **명목 정의 그대로 인계 적격** (규칙 ⓑ 적용: 폴백 0 건 · 겹침 0 건 · 재현 130/130 일치)

| 열 | 판정 | 근거 · 열 사전 한정어 (F3 · `LHS-19`) |
|---|---|---|
| `percolation_pct` (SE 이온 · `calc_percolation`) | ✅ | 밴드 L0 130/130 (중심 z ≤ 2r_i · z ≥ plate_z − 2r_i · 바닥 z = 0 암묵 = 덱 바닥 0.0 과 같다) · 관통 성분에 든 SE / 전 SE (분모에 외톨이 포함) · **밴드 규칙 관통 ≠ 솔버 관통** — `lhs00_009` 는 이 열 99.99 인데 σ_ion 열은 SOLVE_NONE (N/A) 이 된다 (`LHS-04`) |
| `n_components` | ✅ (뜻 한정) | **외톨이 SE (간선 0) 도 성분 1 로 센다** — 단절 침대에서는 사실상 외톨이 수 (`LHS-06` 무접촉 최대 49 %) · RVE 50 µm 고정이라 두께에 비례하는 총량 |
| `n_large_components` | ✅ (뜻 한정) | 문턱 ≥ 10 입자 = 출처 없는 코드 상수 — 열 사전에 그대로 명시 (값은 바꾸지 않는다) |
| `electronic_active_fraction` · `electronic_percolating_fraction` (AM 전자 · `build_network` + `active_fractions`) | ✅ | AM_P + AM_S 한 상 · 밴드 L0 130/130 · 분자 = **간선 있는 노드** 만 (바닥 밴드에 앉은 외톨이 AM 은 active 에서 빠진다 — `G_active` 규약) · 분모 = 전 AM · 130/130 관통 |
| `se_se_cn_perc` · `se_se_cn_n_perc` · `se_se_cn_eff_area_perc` (`calc_se_se_cn`) | ✅ (N/A 24 건) | 관통 SE 부분집합 위의 CN · **비관통 24 건은 키 자체가 없다 → 인계표 빈칸 = N/A** (0 이 아니다 · `DESC-05` 부류 — 생성기가 빈칸을 0 으로 채우지 않는지 ③ 전에 확인) |
| `top_reachable_pct` · `ionic_active_pct` (🔶 census `COND_cov` · F4 · `LHS-20`) | ⬜ 저자 결정 | 둘 다 SE 그래프 양 (coverage 값을 읽지 않는다) — ✅ 로 승격하면 `top_reachable_pct` 는 **위 밴드에 앉은 외톨이도 센다** 한정어가 붙는다 · 그대로 두면 인계에서 빠진다 (보수적) |
| `perc_band_level_se` · `perc_band_level_am` (ⓑ 의 조건부 새 열) | — 불요 | 폴백 0 건이라 만들지 않는다 (규칙 ⓑ 그대로) |
| 수확기 AM `percolation` (설계 CSV 진단 열) | — 인계 열 아님 | `107` · `110` 의 밴드 불일치는 **기록만** (ⓑ: 2×2 불일치는 판정에 안 쓴다) |

- ⓒ **열 사전 문구 초안** (비준 뒤 생성기 `lhs_design_dataset.column_dictionary` 에 반영 — 생산 생성기 코드 변경이라 **비준 대기**):
  - `percolation_pct`: *"SE 그래프 (접촉 덤프 행 · 양끝 SE) 에서 바닥 밴드 (z ≤ 2r · 바닥 z=0) 와 플래튼 밴드 (z ≥ plate_z − 2r) 를 잇는 성분에 든 SE 의 % (분모 = 전 SE · 외톨이 포함).  밴드 규칙 관통이며 솔버 (전극 규칙) 관통과 다를 수 있다 (`lhs00_009`).  LHS 130 건 전부 기본 밴드 (L0) · 폴백 없음."*
  - `n_components`: *"SE 접촉 그래프의 연결 성분 수 — 간선 0 인 외톨이 SE 도 성분 1.  RVE 50 µm 고정 총량."*
  - `n_large_components`: *"입자 ≥ 10 인 성분 수 (문턱 10 = 코드 상수 · 문헌 출처 없음)."*
  - `electronic_active_fraction` / `electronic_percolating_fraction`: *"AM (AM_P + AM_S 한 상) 접촉 그래프에서 바닥 밴드에 닿는 성분 / 두 밴드를 잇는 성분에 든 AM 의 분율 (분자 = 간선 있는 노드만 · 분모 = 전 AM).  밴드 = 웹앱 L0."*
  - `se_se_cn_perc` · `se_se_cn_n_perc` · `se_se_cn_eff_area_perc`: *"관통 SE 부분집합 위의 SE–SE CN (수 · 면적 가중).  비관통 케이스 (24/130) 는 정의되지 않아 **빈칸 = N/A** (0 아님)."*
  - (승격 시) `top_reachable_pct`: *"플래튼 밴드에 닿는 성분에 든 SE % — 밴드에 앉은 외톨이 SE 도 센다."*
- 원장: `LHS-17` · `LHS-18` open 유지 (코드 결함 · 실측 0 건 note) · `LHS-19` 실측 note · `LHS-20` 저자 결정 · `LHS-04` 에 ② 대조 note · `SELF-64` claimed_fixed (`c0c2d4f44`) · `SELF-65` 신규 (요약 낡은 키 · 반례 먼저).
- ⛔ 값 산출 (`run_lhs_fill_wsl.sh` 전 건) 은 **여전히 보류** — 이 판정은 ② 묶음 열에 한한다.  다음 = ③ φ_SE (코드 정의부터).

## J20-c. ① 접촉 위상 **값 산출** — 130 + 64 · 열마다 설명하며 저장 (1저자 09-29 밤 지시 · ⬜ 비준 항목 셋)

지시: *"z_SE-SE mean·σ · z_AM-SE · AM_P-SE CN · surface-weighted · z_AM-AM · contact count — 이 부분 관련해서 130, 64 관련해서 하나하나 설명하면서 저장해가자"* ·
*"porosity 는 보낼 때 union 정도만"* · ③ φ_SE 감사는 그 뒤 (② 판정 뒤 바로 ③ 으로 가지 않는다).

- **지금 저장된 것** (`docs/data/lhs_handover_20260928.csv` · 130 행 × 119 열): 설계 32 열 · 수확 측정 = φ_SE · φ_AM (구 부피 합) · coverage Hertz P/S/total (= A_dem_geometric) ·
  porosity **5 규약** (sphere RECORD_ONLY · nominal gap · clipped · pushback · union exact / pair-clipped / SE) · 두께 **3 규약** (wall gap · envelope · mass-conserving) + pushback 등가 ·
  τ 는 상태 열만 (값은 `LHS-08` 로 보류) · 경계 QC · sha.  **① CN · ② 퍼콜레이션 열은 아직 없다** (웹앱 배치 미실행).
  **64 (lhsx)** 는 수확 (`lhsx_descriptors_20260925` · v2) 과 union (`lhs_union_20260927/lhsx64_union.tsv`) 만 있고 인계표가 없다 — 설계 CSV 스키마가 130 과 다르다
  (`id · pdd_SE · w_AM_P · w_AM_S · rP_um …` ↔ `case_id · am_pct · d_am_p_um …`) ⇒ 생성기용 **설계 어댑터**가 필요하다 (⬜).
- **① 열 (인계 이름 = 코퍼스 이름 · 뜻 = 생성기 `WA_DEFINE` · 상세 = J20-a ① 정의표)**:
  `se_se_cn` · `se_se_cn_std` (z_SE-SE mean · σ — SE 전 입자 · 접촉 0 · 벽 입자 포함 · 모집단 σ) · `am_se_cn_mean` (z_AM-SE — AM 전 입자 개수 가중 · **파생**) ·
  `AM_P_se_cn_{mean,std,median,max}` · `AM_S_se_cn_{…}` (상별 · 상 없으면 빈칸 = N/A) · `am_se_cn_surface_weighted` (Σ r²·CN / Σ r² · AM_P 지배 · **파생**) ·
  `am_am_cn` · `am_am_cn_std` (z_AM-AM · P–S 교차 포함) · `am_am_n_contacts` · `area_<쌍>_n` (접촉 **개수** = 덤프 행 수 · 총량 · 면적 아님) · ⓓ `wall_touch_frac_<상>_<floor|plate>` (수확 v3).
  130 실측 (① 감사): 프레임 1 · 중복 0 · 자기쌍 0 · δ ≤ 0 0 ⇒ 정의 그대로 셈이 선다.  64 는 SE-rich (SE/고체 0.51–0.85) 라 z_SE-SE 가 130 (중앙 4.75) 보다 높게 나온다 (J19 실측 9.6).
- **계획 (⬜ 비준 ⓐ–ⓒ)**: ⓐ WSL 산출 = 재수확 v3 (130 + 64 · wall_touch · 벽 τ) → 웹앱 배치 (130 + 64) → tgz 송부 (아래 · **인계표 재생성 [4] 는 돌리지 않는다**) ·
  ⓑ 생성기 `--webapp-groups contact` (① 열만 저장 · 반례 먼저) + lhsx 설계 어댑터 (id → case_id · rP_um → r_AM_P_um … · 검산 = 수확 입자 수 ↔ n_*_est) — 코드 · 비준 뒤 ·
  ⓒ **배포 프로필** (저자 제안 "union 정도만"): porosity = `porosity_union_exact_pct` (+ `se_rich`) · 두께 = `thickness_mass_conserving_um` · 내부 표는 전부 유지 — 근거: 구 부피 합은 겹침 이중계상으로
  SE-rich 에서 음수 (130 중 18 · 64 중 60) · union 은 194 건 전부 양수 · 단 union 은 소성 압축의 고체를 과소계상하는 상한 규약 (CLAUDE.md E_SE 절) — 열 사전에 그대로 적는다 · ⬜ 저자 결정.
  그 뒤 ② 열 같은 방식 → ③ φ_SE 감사.
- WSL 명령 (한 건 먼저 · `--case lhs00_000` · `--case lhsx_001` · 64 배치가 안 서면 보고):
  ```
  cd ~/dem-audit && git fetch origin claude/sdcp-dem-manuscript-si-pqwtv8 && git checkout --detach origin/claude/sdcp-dem-manuscript-si-pqwtv8 && git log -1 --oneline
  P=~/Yonghoon-DEM-DFT/venv/bin/python; D=$(date +%Y%m%d)
  $P scripts/lhs_harvest_batch.py --verify-sha --out-dir docs/data/lhs_descriptors_$D --summary docs/data/lhs_descriptors_$D/_batch_summary.json
  $P scripts/lhs_webapp_batch.py --harvest-dir docs/data/lhs_descriptors_$D --work ~/lhs_webapp_work --out-dir docs/data/lhs_webapp_$D
  $P scripts/lhs_harvest_batch.py --verify-sha --cohort docs/data/lhsx_descriptors_20260925/_cohort.tsv --out-dir docs/data/lhsx_descriptors_$D --summary docs/data/lhsx_descriptors_$D/_batch_summary.json
  $P scripts/lhs_webapp_batch.py --cohort docs/data/lhsx_descriptors_20260925/_cohort.tsv --harvest-dir docs/data/lhsx_descriptors_$D --work ~/lhsx_webapp_work --out-dir docs/data/lhsx_webapp_$D
  tar czf ~/lhs_fill_$D.tar.gz docs/data/lhs_descriptors_$D docs/data/lhs_webapp_$D docs/data/lhsx_descriptors_$D docs/data/lhsx_webapp_$D
  ```
  ⚠ **09-29 밤**: 위 첫 줄의 브랜치 `claude/sdcp-dem-manuscript-si-pqwtv8` 는 **낡았다** — 연장 세션이 stoic-knuth 로 병합됐다 (`docs/handoff_merge_to_stoic_knuth_20260929.md`) ⇒
  `origin/claude/stoic-knuth-NObVQ` 를 쓴다.  두 배치 스크립트 모두 `--case` (여러 번) 가 있다 (한 건 먼저).

## J20-d. 64 (lhsx) 인계표 생성 — 저장된 열까지 130 과 같은 생성기로 (1저자 09-29 밤 *"64 도 진행하자"* · ✅ 실행)

- 설계 변환 `scripts/lhsx_design_adapter.py` (selftest 14/14 · 반례 6): 질량분율 (`w_AM_P · w_AM_S · pdd_SE` · 합 1 ± 2e-6 = 6 자리 반올림) → `am_pct = 100·(1 − pdd_SE)` ·
  `ps_frac = w_AM_P/(w_AM_P + w_AM_S)` · mono 는 **P 열 = 일반 AM 자리** (`lhs_ext_materialize` 머리말 · R14) · 입자 수는 `lhs_ext_design.n_spheres` 로 상별 재계산해 CSV 값과 왕복 대조
  (허용 = 반지름 4 자리 반올림 몫 3·n·5e-5/r + 1 — 실측 lhsx_001 SE 56118 vs 56120) · 압력 300 · E_SE 1.35 · 상자 50 은 템플릿 덱 상속 (`render()` 는 반지름 · 가중 · volfrac · seed · 이름만 치환 ·
  상자는 union `lx_um` 64/64 = 50 확인).  130 전용 추정 열 10 (loading · thickness_est · phi_*_est · se_percolation_est · sv_inv · rve_min/recommended · thick_over · finite_size_flag) 은
  하중 기반 규약이 없어 **넣지 않았다** (사유는 스크립트 `OMITTED`) — lhsx 원래 값은 `lhsx_*` 12 열로 같이 싣는다.
- 산출 `docs/data/lhsx_handover_20260929.csv` **64 행 × 121 열** + `_columns.tsv` — 생성기 계약 전부 통과 (DESC-07 항등식 · union 짝 = 같은 프레임 · 두께 · 입자 수 · union (0, 100)):
  porosity union exact **5.43–9.43 %** (중앙 6.55) · 두께 mass-conserving 25.0–44.7 µm (wall gap 22.5–41.3) · φ_SE 0.52–0.92 · SE/고체 0.51–0.85 → `se_rich` 64/64 ·
  구 부피 합 porosity −8.40 … +1.52 % (음수 60 · `hold_reason_codes` NEGATIVE_POROSITY 60 · BOUNDARY_CENTER_OUT 11) — J19 그대로 (규약의 음수이지 결함 아님) · coverage 는 mono 16 건의 없는 상이 빈칸 (N_A_PHASE_ABSENT 32 칸).
  kind = bimodal 48 · mono_AM_P 8 · mono_AM_S 8.
- 130 과의 열 차이: 64 에만 `lhsx_*` 12 · 130 에만 추정 열 10.  ① ② 열은 둘 다 아직 없다 (웹앱 배치 뒤 · J20-c).
- 체크리스트 `docs/lhs_handover_checklist_20260929.md` §1 갱신.

## J20-e. φ_SE · φ_AM — **넘기는 두께와 같은 장부로** (J19 ③ 재검토 · 09-29 밤 · 1저자 *"φSE 코드 문제 다시 · 뜻"* · ⬜ 저자 결정)

- **코드 정의**: 수확기 `volumes_and_phi` (`lhs_descriptor_harvest.py:444–507`) — φ_i = Σ(4/3)πr³ (상 i 전부) ÷ (L² × (plate_z − 벽 0)).  겹친 부피를 두 번 세고 벽 밖 cap 도 센다 ·
  코드 자신이 *"장부값 — 틀 안 점유율이 아니다"* 라고 적는다 (`:494`) — **계산 결함은 아니다**.  웹앱 ③ φ_SE (`network_conductivity.py:1120–1123`) 도 같은 구 부피 합 식.
  DEM 구는 크기가 안 변하므로 분자 = 레시피 부피 (상수) ⇒ 이 φ 는 **레시피 부피 ÷ DEM 판 간격** 이고, 새로 잰 것은 판 간격 하나다.
- **결함 = 장부 섞임**: 인계는 porosity = union exact (J19 ①) · 두께 = 질량 보존 H_mc = H (1 − ε_s)/(1 − ε_u) (J19 ②) 로 **M 장부** (겹친 재료가 두께를 늘린다고 보고 재료를 보존) 인데,
  φ 는 **S 장부** (두께 H · ε_sphere — 겹친 재료가 빈틈을 메운다고 봄) 다 ⇒ φ_SE + φ_AM + ε_union − 1 = 130 중앙 +3.77 %p (1.15–10.17) · 64 중앙 +10.91 %p (6.80–14.22) ·
  φ 합 > 1 이 130 중 18 · 64 중 60.
- **J19 ③ 의 "union 판 φ" (09-29 저녁 체크리스트 §6 의 ★ (가)) 도 짝이 안 맞는다 — 철회**: union MC 점유율은 **G 장부** (두께 H 인 DEM 상자 안) 라 union 과는 닫히지만 넘기는 두께 H_mc 와
  섞으면 적재량 (φ × 두께) 이 레시피와 어긋난다 — AM 130 중앙 +3.2 % (최대 +10.7 %) · 64 중앙 +11.2 % (6.4–14.8 %) · SE −6.9 % · −4.8 % (인계표 · union TSV 에서 계산).
- **권고 (라) 질량 보존 φ**: φ_i = V_i / (L² · H_mc) = φ_i(구) × H / H_mc — union 과 닫힘 잔차 0 (194/194) · 적재량 = 레시피 · SE/고체 = `se_of_solid_vol` (≤ 3e-16 · `se_rich` 와 같은 값) ·
  겹침 배분 규칙 불요 · 새 측정 불요.  범위 130 φ_SE 0.079–0.474 · φ_AM 0.422–0.715 · 64 φ_SE 0.476–0.798 · φ_AM 0.143–0.449.
  한정어 (열 사전): M 장부는 union 을 공극률로 받는 **상한 규약**의 짝이다 (소성 압축에서 밀려난 재료를 빈틈이 아니라 두께로 보낸다 — 실제는 S 와 M 사이).
- 구현 (비준 뒤 · 반례 먼저): 생성기 열 둘 · 검사 셋 (닫힘 1e-9 · φ_i × H_mc × L² = 구 부피 합 · SE/고체 = `se_of_solid_vol`) · 구 부피 합 φ 와 (가)~(다) MC 부피는 내부 표.
- 체크리스트 §1 · §6 갱신 (같은 커밋).
- ✅ **결정 · 구현 (1저자 09-29 밤 *"φ 는 (라) 에 해당하는 것만 뽑으면"*)** — 생성기 `phi_se_mass_conserving` · `phi_am_mass_conserving` (selftest ⑱m–r · ⑱l2 — 옛 코드 84/90
  (새 6 실패) → 90/90) · 런타임 관문 닫힘 1e-9 · 재생성 `docs/data/lhs_handover_20260929.csv` (130 × 121 · 새 파일 · 열 사전 첫 생성) · `lhsx_handover_20260929.csv`
  (64 × 123 · 제자리) — **옛 열 칸 변경 0** · 닫힘 최대 3.3e-16 (130) · 2.2e-16 (64) · 새 계산 없음 (저장된 세 열의 곱).
- ⚠ **같은 날의 방향 정정** — J20-c ⓐ 는 ① 을 얻으려고 웹앱 파이프라인 **전체**를 돌리는 계획이었다 (한 건 575.6 s · 743.4 s → 194 건 ≈ 34 h · ③~⑦ 까지 계산).
  1저자 *"왜 전체에 대해서 뽑고 있는 거야"* · *"단독적으로 하나씩 돌려서 표를 채워나갈 거야"* ⇒ 묶음마다 **그 묶음을 내는 단계만** 돌린다 (① = 접촉 분석 단계) —
  09-28 밤 *"일괄적으로 뽑지 말고"* 와 같은 뜻.  한 건 시험 (lhs00_000 · lhsx_001 · 둘 다 `partial` = 선택 단계 실패 · 필수 단계 성공) 의 산출은 대조 기준으로 쓴다.
- ✅ **① 전용 실행 모드 (09-29 밤 · 1저자 *"ㅇㅇ 단독적으로 하나씩"* · 반례 먼저)** — 웹앱 `run_pipeline(stop_after='contact')` 는 접촉 분석 단계 (`analyze_contacts[_bimodal].py`) 가 성공하면 멈춘다 (T10: 멈추기 전 명령 = 전체 실행의 앞부분 · 인자까지 같다 · 다른 값 ValueError · 접촉 실패는 failed · 옛 코드 182/188 → 188/188) · 배치 `lhs_webapp_batch.py --stop-after contact` (산출 폴더에 모드를 새기고 다른 모드와 섞으면 rc 2 · ⑫ ⑬) · 생성기 `--webapp-groups contact` (접촉 단계 산출 열만 · 접촉만 돈 배치를 묶음 없이 부르면 거부 · ⑲q–u · 90/95 → 95/95).
  ⚠ ① 사전 (WA_DEFINE) 중 넷은 접촉 단계 산출이 **아니다** — `A_binding_AM_SE_n_contacts` · `A_binding_total_n_contacts` (피복 단계 `coverage_physics_vs_hertzian.py`) · `n_am_am_contacts_total` · `_excluded` (`run_network_fracture_aware.py`) ⇒ 이 묶음에서 뺐다 (필요하면 그 단계 묶음에서).
  ✅ **WSL 한 건 대조 통과 (09-29 밤 · 1저자 · `~/dem-audit` @ `e833a498d`)**: `lhs00_000` · `lhsx_001` 둘 다 ① 22 열 **값 다름 0** (전체 실행 `$O/wa*` ↔ 접촉만 `$O/c*` · 문자열 비교) · porosity 같음 (11.8828 · 0.1797 % — 같은 프레임 관문 값) · 시간 **29.3 s** (전체 575.6 s) · **92.4 s** (743.4 s) · 상태 done 2/2.  ⬜ 전 건 = 수확 v3 130 + 64 → 접촉만 배치 130 + 64.

## J20-f. mono (2-type) 덱 — 배치 type_map 관문이 **이름 규약 차이**로 30 + 16 건을 거부 (09-30 · 1저자 비준 · 원장 `SELF-66`)

- **WSL 전 건 실측 (1저자 · `~/dem-audit` @ `4b42179ec`)**: 수확 v3 130/130 OK (`docs/data/lhs_descriptors_20260929/`) → 접촉만 배치 **done 100 · REFUSED 30** = `lhs00_100–129` 전부 (mono 덱 전부) ·
  사유 `type_map 덱 판독 1:AM_S,2:SE ≠ 수확 JSON {'1': 'AM', '2': 'SE'}` (AM_P 인 것도 같은 꼴) · 한 건 0.0–1.4 s (실행 전 거부 · 잘못 채운 값 0).  lhsx 는 mono 16 건 (`lhsx_003 · 005 · 012 … 060 · 062`) 이 같은 관문에 걸린다.
- **원인 = 두 코드의 이름 규약**: 수확기는 AM 이 한 상인 침대를 `'AM'` 으로 적는다 (`lhs_perc_extract.TYPE_MAP[2]` — 상별 P/S 칸 N/A 규약) · 웹앱 덱 판독은 같은 입자를
  **반지름**으로 부른다 (`type_map_resolve.py:134` — 덱이 `r_AM` 하나만 선언하면 r > 4 µm (sim 0.004) → AM_P, 아니면 AM_S · "기존 동작 보존").  배치 관문 (`resolve_mode`) 은 글자 그대로 비교했다.
- **수정 (반례 먼저 · selftest ⑭–⑭f · 옛 코드 26/28 (⑭ · ⑭b 실패) → 28/28)**: `fold_single_am` — **두 쪽 다 2-type 이고 수확 쪽이 정확히 {AM, SE}** 일 때만 덱 판독의 AM_P/AM_S 를 AM 으로 접어 비교.
  음성 대조 유지: SE 번호 뒤바뀜 · SE 없는 두 AM · 수확 2-type ↔ 덱 3-type · 3-type 이름 다름 (④) → 전부 거부.  웹앱에는 **덱 판독 map 그대로** 넘긴다 (업로드 입구와 같은 입력) ·
  접은 사실은 status.json `type_map_fold` · meta `type_map_notes` 에 남는다.
- **① 총량 열은 이름과 무관**: 웹앱의 AM 집합 = "이름에 AM" (`dem_analysis_core.py:180 · 714 · 816 · 1054`) ⇒ `se_se_cn*` · `am_se_cn_mean` · `am_se_cn_surface_weighted` · `am_am_cn*` · `am_am_n_contacts` 는
  AM_S 로 부르든 AM_P 로 부르든 같다.
- ⚠ **상별 ① 열은 이름을 따라간다 (정정 — 같은 날 첫 보고에서 *"① 에는 상별 열이 없다"* 고 잘못 말했다)**: ① 묶음 (`wa_group_contact`) 에는 `AM_P_se_cn_{mean,std,median,max}` ·
  `AM_S_se_cn_{…}` · `area_<쌍>_n` 이 있다 ⇒ mono 의 값은 **반지름 이름** 칸에 들어간다.  설계 상 (ps_frac) 과 반지름 이름이 **다른** mono:
  **130 = 5 건** `lhs00_118` (설계 AM_P · r 3.0 µm) · `121` (4.0) · `124` (3.0) · `125` (3.5) · `126` (2.5) — WSL 거부 줄의 덱 판독 이름과 **정확히 일치** ·
  **64 = 4 건 (예측)** `lhsx_003` (3.17) · `017` (2.80) · `048` (2.72) · `062` (3.80) — 실행 뒤 status.json `type_map` 으로 확인.  나머지 mono (130 의 25 · 64 의 12) 는 이름이 설계와 같다.
- ⬜ **저자 결정 (인계표 재생성 전 — 실행은 막지 않는다)**: mono 의 상별 ① 열을 어떻게 싣나.
  (A) **권고** = 인계표의 기존 규약 그대로 — mono 는 상별 P/S 칸 **빈칸 (N/A)** · 총량 열이 값을 싣는다 (수확기 coverage 상별 열이 mono 30 + 16 건에서 이미 이렇다 · 이름 충돌이 원천적으로 없다 ·
  잃는 것 = mono 의 상별 std · median · max 셋 — ① 에 그 총량 열이 없다 · mean 만 총량 `am_se_cn_mean` 과 같은 값 (같은 입자 집합의 `np.mean` · `dem_analysis_core.py:737–761`)).
  (B) 설계 상 이름으로 옮겨 싣기 (예: 설계 AM_P 인데 웹앱 AM_S → `AM_P_*` 로) — 정보는 다 남지만 같은 표 안에서 coverage 상별 (N/A) 과 규약이 갈린다.
  공통: 웹앱이 붙인 이름을 열 하나로 남긴다 (`status.json` `type_map`).
- ⚠ 뒤 묶음 (② 이후) 에서 AM_P/AM_S **이름이 물리에 쓰이는지** (예: 상별 σ_AM) 는 그 묶음을 돌리기 전에 코드로 확인한다 — 묶음마다 따로 돌리므로 ① 의 선택이 뒤 묶음을 묶지 않는다.
- WSL 다시 돌리기: 같은 두 배치 명령 · 같은 `--out-dir` — done · partial 은 건너뛰어 **REFUSED 만** 돈다 (`KEEP_STATUS`).
- ✅ **결정 (1저자 09-30 *"권고대로"*) = (A)** — mono 의 상별 웹앱 열 (AM_P/AM_S 이름이 든 열) 은 빈칸 · 총량 열이 값을 싣는다 · 구현 = J20-g.

## J20-g. 인계표에는 **1저자와 함수 단위로 같이 확인한 웹앱 열만** (09-30 · 1저자 비준 *"권고대로"* — *"하나하나씩 쳐내가자"*)

- 규칙: 09-19 census ✅ 는 **필요조건**일 뿐이다 — 인계표 생성기 (`lhs_design_dataset.py`) 가 `WA_REVIEWED` (열 패턴 · 검토 기록) 에 든 열만 싣는다 (`build_handover(wa_reviewed_only=True)` 기본 · CLI 는 항상 이 경로 · False 는 옛 기제 시험 전용).
  함수 검토가 하나 끝날 때마다 패턴을 더한다 — 지금 = `area_(.+)_n` (`calc_interface_area` · 09-30 검토 · 수정 불요).  열 사전 뜻에 검토 기록을 붙인다.
- J20-f (A) 구현: 수확 JSON `n_types` = 2 인 침대는 상별 웹앱 열을 빈칸으로 (보고 `wa_mono_phase_blanked`) · `n_types` 가 없는데 상별 열을 실어야 하면 **거부** (반지름 이름을 그대로 싣지 않는다) · 열 사전에 mono 규약 문구.  ⚠ **09-30 저녁 (B) 로 개정 (J20-k · 7b · `06b24cdd0`)** — 이 줄은 09-30 오전 판 기록이다 · 지금 생성기는 설계 상 칸에 채우고 보고 키도 `wa_mono_design_filled` · `wa_mono_renamed_cases` · `wa_mono_absent_blanked` 로 바뀌었다.
- 시험 먼저: ⑳a–f (옛 코드 96/101 — 새 5 실패 · ⑳c 는 bimodal 이라 원래 통과) → 101/101.  옛 기제 시험 ⑲f · ⑲j · ⑲q 는 `wa_reviewed_only=False` 로 census · 묶음 선별을 계속 시험한다 · 픽스처 `_hq` 에 `n_types` 3.
- 함수 검토 순서 (체크리스트 §5): 계면 개수 ✅ → SE–SE CN → AM–AM CN → AM 고립 · 나머지 분석은 그 묶음 차례에.
- ✅ **적용 (09-30)**: WSL 배치 130/130 · 64/64 done (원자료 `docs/data/lhs_webapp_contact_20260929/` README) → `lhs_handover_20260930.csv` 130×133 · `lhsx_handover_20260930.csv` 64×135 — 새 열 12 (`area_<쌍>_n` 7 · `wa_status` · `wa_failed_stages` · QC 3) · 뺀 census ✅ 접촉 열 15 · mono 상별 칸 빈칸 60 · 32 · 같은 프레임 |Δporosity| ≤ 2.5e-10 %p · 옛 칸 변경 0 · QC coverage |Δ| ≤ 1.4e-14.  수확은 v2 (20260925) 로 불렀다 (v3 새 열 = 벽 τ · 벽 접촉은 같이 확인 전 · 기존 값 v2 = v3).
  ⚠ **새 발견 (검토 때 못 짚음)**: `calc_interface_area` 는 접촉이 0 인 쌍의 키를 만들지 않는다 → bimodal 에서 그 쌍 칸이 **빈칸** (130: `area_AM_P_AM_P_n` 3 건 · 64: 6 건 — AM_P 가 3–16 알인 침대) · 뜻은 **측정된 0** 이지 N/A 가 아니다 → J20-h.

## J20-h. 접촉 0 인 쌍 = 0 (09-30 · 1저자 비준 *"bimodal 에서 빠진 쌍을 0 으로 채우게 · 시험 먼저 — 이렇게 하자"*)

- 규칙 (생성기 `WA_PAIR_COUNT` · `PAIR_ZERO_NOTE`): 웹앱 행이 있고 (done · partial) · 쌍 개수 열 `area_<A>_<B>_n` 이고 · 값이 빠졌고 · 두 상이 수확 `phase_counts` 에 **있으면** `0` · mono 상별 칸은 J20-f (A) 빈칸 그대로 · 상이 없으면 빈칸 (N/A) · `phase_counts` 가 없으면 **거부** · 배치가 거부한 행 (REFUSED) 은 채우지 않는다 · 열 사전 뜻에 규약 문구.
- 시험 먼저: ⑳g–l (옛 코드 103/107 — ⑳g · j · k · l 실패 · ⑳h · i 는 원래 통과하는 방어 경우) → **107/107**.
- 적용: `lhs_handover_20260930.csv` · `lhsx_handover_20260930.csv` 재생성 — 바뀐 칸 = **정확히 3 · 6** (`area_AM_P_AM_P_n` `''` → `0` · 130: `lhs00_016` · `048` · `092` · 64: `lhsx_008` · `021` · `028` · `040` · `044` · `056`) · 열 목록 그대로.

## J20-i. 접촉 ① 둘째 함수 — SE–SE CN 두 열 (09-30 · 1저자 비준 *"비준하고"*)

- 검토 (`calc_se_se_cn` · `scripts/dem_analysis_core.py:232–344` → `scripts/analyze_contacts.py:376–377`): SE 한 알마다 SE 와의 접촉 수를 세고 SE **전 입자**로
  평균 (`se_se_cn` · 접촉 0 · 벽 · 플래튼에 닿은 입자 포함) · 모집단 표준편차 (`se_se_cn_std` · `np.std`) · 접촉 = 계면 개수 (J20-g) 와 같은 덤프 행 집합
  (원자 프레임에 없는 id 의 행은 버림 · 벽 접촉은 없다) ⇒ **코드 수정 불요**.
- 대조 (09-30 · 컨테이너 · 커밋된 배치 원자료): 평균 = 2 × `area_SE_SE_n` / SE 입자 수 (수확 `phase_counts`) — **130/130 · 64/64 차이 0** (최대 상대차 0).
  값: 130 = 0.680–9.174 (중앙 4.746) · 64 = 6.892–11.147 (중앙 9.619 — SE-rich 설계) · mono 포함 전 행 (SE–SE 는 상별 열이 아니다 · J20-f (A) 무관).
- 같은 함수의 나머지 출력 8 열은 **싣지 않는다** (census ✅ 여도): `se_se_cn_perc` · `se_se_cn_n_perc` · `se_se_cn_eff_area_perc` (② 퍼콜레이션 차례) ·
  `se_se_cn_eff_area` (⑦ 접촉 면적 정의 — L1-04) · `se_se_cn_aug` · `_aug_std` · `_aug_n_extra` · `_aug_h_spread_sim` (⑤ F1 근접쌍 차례).
- ⚠ 미리 본 결함 `LHS-22` (⑤ 차례에 수정): F1 근접쌍 격자 탐색 (`dem_analysis_core.py:297–342`) 이 주기 영상을 보지 않아 x · y 경계 너머의 근접쌍을 못 센다 —
  탄성 접촉 `cn` 은 경계 너머를 포함하므로 `mean_aug` 는 두 규칙이 섞인 값.  인계 열 아님.
- 구현 (시험 먼저): 생성기 `WA_REVIEWED` 에 `se_se_cn(_std)?` · 관문 — 표에 함께 실린 `se_se_cn` 과 `area_SE_SE_n` 이 `se_se_cn = 2 × area_SE_SE_n / N_SE` 를
  (상대 `WA_CN_IDENTITY_TOL` 1e-9 안) 만족하지 않거나 수확 `phase_counts` 가 없으면 **거부** · REFUSED 행은 웹앱 값을 싣지 않으므로 보지 않는다 · 보고 `wa_cn_identity_checked`.
  시험 ⑳m–r (+ ⑳a · ⑳d 개정 · 픽스처 `se_se_cn` 을 항등식에 맞춤): 옛 코드 107/113 (⑳d · m · n · o · p · r 실패 · ⑳q 는 관문 성질) → **113/113**.
- 적용: 두 표 재생성 — `lhs_handover_20260930.csv` 130×135 · `lhsx_handover_20260930.csv` 64×137 (새 열 2 = `area_SE_SE_n` 바로 뒤 · 옛 칸 변경 0 ·
  새 칸 = 배치 `metrics_flat` 원값 260/260 · 128/128 · 빈칸 0) · 항등식 확인 130 · 64 행 · 열 사전 2 행.
- 주의 (열 사전 그대로 · `CAVEAT_WALL`): 벽 · 플래튼에 닿은 SE 는 그쪽 이웃이 없어 CN 이 낮다 → 얇은 침대일수록 체계적으로 낮다 — 같이 볼 `wall_touch_frac_*` 는
  수확기 item 4 (벽 닿음 규칙) 병합 뒤 싣는다.

## J20-j. 접촉 ① 셋째 함수 — AM–AM CN 세 열 (09-30 · 1저자 *"6번 진행하자 코드 부탁해"*)

- 검토 (`calc_am_am_cn` · `scripts/dem_analysis_core.py:347–375` → `scripts/analyze_contacts.py:452–458`): 두 원자가 모두 AM 종류 (AM_P · AM_S · mono 는 AM)
  인 접촉 행마다 두 입자에 +1 → AM **전 입자** 평균 (`am_am_cn` · P–S 교차 포함 · 접촉 0 인 AM 포함) · 모집단 표준편차 (`am_am_cn_std`) ·
  `am_am_n_contacts` = Σ/2 (AM–AM 접촉 총수) ⇒ **코드 수정 불요**.  (AM 이 없으면 `total_area` 키가 빠지는 비대칭이 있으나 `analyze_contacts` 가
  `n_am > 0` 일 때만 쓰고 LHS 는 전부 AM 이 있다 — 무영향.)
- 대조 (09-30 · 커밋된 배치 원자료): `am_am_n_contacts` = AM–AM 쌍 개수 합 (`area_AM_P_AM_P_n` + `area_AM_P_AM_S_n` + `area_AM_S_AM_S_n` · 없는 쌍 = 0) ·
  `am_am_cn` = 2 × `am_am_n_contacts` / AM 입자 수 (수확 `phase_counts`) — **130/130 · 64/64 차이 0**.  값: 130 = 1.719–6.633 (중앙 5.148) ·
  64 = 0.438–3.970 (중앙 1.934 — SE-rich 라 AM 끼리 덜 닿는다).
- mono: 세 열 모두 상별 열이 아니다 (소문자 `am_` · J20-f (A) 무관) ⇒ **J20-f (A) 로 비운 mono 의 AM–AM 개수가 `am_am_n_contacts` 로 돌아온다** (130 의 30 · 64 의 16 행).
- 싣지 않는 것: `am_am_mean_area` · `am_am_total_area` (접촉 면적 — ⑦ A_dem_geometric · L1-04 차례).
- 구현 (시험 먼저): 생성기 `WA_REVIEWED` 에 `am_am_(cn(_std)?|n_contacts)` · 관문 둘 — ① `am_am_n_contacts` = 웹앱 원 행의 AM–AM 쌍 개수 합
  (`WA_AM_AM_PAIR`) ② `am_am_cn` = 2 × `am_am_n_contacts` / N_AM (상대 1e-9) — 어긋나거나 `phase_counts` 가 없으면 거부 · REFUSED 행은 보지 않는다 ·
  보고 `wa_am_identity_checked`.  시험 ⑳s–x (+ ⑳a · ⑳d 개정 · 픽스처 AM–AM 값을 항등식에 맞춤 · ⑳g 기대값 12 → 17 · ⑳i 는 AM_P 0 침대에 AM_P 쌍이 남던
  앞뒤 안 맞는 재료를 고침): 옛 코드 112/119 (⑳d · s · t · u · v · w · x 실패) → **119/119**.
- 적용: 두 표 재생성 — `lhs_handover_20260930.csv` 130×138 · `lhsx_handover_20260930.csv` 64×140 (새 열 3 · 옛 칸 변경 0 · 새 칸 = 배치 원값 390/390 · 192/192 ·
  빈칸 0) · 항등식 확인 130 · 64 행 · 열 사전 3 행.
- 주의 (열 사전 그대로): CN = 벽 효과 (`CAVEAT_WALL` — 큰 AM_P 는 두께 대비 커서 SE 보다 크다) · `am_am_n_contacts` = 총량 (`CAVEAT_COUNT`).

## J20-k. mono 상별 칸 채우기 (J20-f 개정 → (B)) + 전체 AM–SE 분포 열 (C) · AM–SE CN · 고립 비율 싣는 시점 (09-30 · 1저자)

- 1저자: *"인계할때는 중복되더라도 잘 채워서 보내야될듯"* · *"잃는게 있음 돌리는게 낫지 않아? 너가 권고하는대로 해"* · *"고립은 coverage 관련해서 닫히면 진행하자"*.
- 배경 (7번 검토 · `calc_am_isolation_risk` · `dem_analysis_core.py:710–780` → `analyze_contacts.py:435–444` · 코드 수정 불요): 대조 전부 차이 0 —
  상별 평균 × 상 입자 수 = `area_<상>_SE_n` 130/130 · 64/64 (웹앱 입자 수 = 수확 230/230 · 112/112) · 전체 평균 × AM 수 = `area_AM전체_SE_n` ·
  표면 가중 = 설계 반경 단일 반경 항등식 (최대 상대차 2.4e-12) · `am_vulnerable_pct` = 상별 개수 가중 · median/max/std 모양 정상.
  잃는 것 = J20-f (A) 에서 적은 대로 **mono 30 + 16 침대의 AM–SE 분포 (std · median · max)** — 전체 열이 없다 (함수는 전체 std 를 계산하나 `analyze_contacts` 가 안 내보냄 · median/max 전체는 계산 안 함).
- **(C) 채택**: 웹앱이 전체 분포 `am_se_cn_std` · `am_se_cn_median` · `am_se_cn_max` 를 내보내게 고친다 (시험 먼저) → 5번 coverage 배치
  (`--stop-after coverage` = 접촉 단계 포함) 에서 값이 생긴다 (추가 실행 없음) · census (09-19) 에 없는 새 키라 싣는 때 열 사전 · 판정 기록을 같이 단다.
- **(B) 채택 (J20-f (A) 개정)**: mono 침대는 **설계 상 칸**에 단일 AM 값을 채운다 (P 만 → `AM_P_*` · S 만 → `AM_S_*` · 웹앱 반지름 이름이 설계와 다른 9 건 = 130 의 5 · 64 의 4 도
  설계 이름 칸으로) · 설계에 없는 상의 칸은 빈칸 (N/A — 그 상이 없다 · 0 아님) · **모든 상별 열에 같은 규칙** (계면 개수 AM_x 쌍 · AM–SE CN 상별 통계 ·
  `n_AM_*_measured` (`LHS-21` 해소) · 수확기 coverage 상별) · 열 사전 표지 "mono: 설계 상 칸 = 단일 AM 값 (전체 열과 중복)".
- 7번 분할: **7a** 웹앱 분포 내보내기 (코드 · 지금) · **7b** 생성기 (B) (지금 · 재실행 불요 · 이미 실린 mono 쌍 개수부터) · **7c** AM–SE CN 10 열 + 고립 비율 3 열 +
  분포 3 열을 표에 (coverage 가 닫힌 뒤 · 관문 = 위 항등식들).
- 고립 비율 census 오분류 = 원장 `LHS-23`.
- ✅ **7a 구현 (09-30 · 시험 먼저)**: `calc_am_isolation_risk` (`dem_analysis_core.py:736–746`) 가 전체 `am_se_cn_median` (float · np.median) · `am_se_cn_max` (int) 를 더 내고,
  `analyze_contacts.py:435–444` 가 전체 `am_se_cn_std` · `_median` · `_max` 를 full_metrics 에 싣는다 (추가만 · 옛 키 · 옛 값 그대로 · 상별 통계와 같은 counts · 같은 함수).
  새 시험 `scripts/analyze_contacts.py --selftest` (12 항 · 등재): 3 상 (AM_P 3 · AM_S 4 · SE 접촉 수 3,0,1 / 2,2,5,0 · AM–AM 행 · SE 사슬은 안 센다) + mono (AM 4 · 0,1,4,2) 작은 침대를
  **웹앱과 같은 CLI** (`analyze_contacts_bimodal.py` · `analyze_contacts.py`) 로 돌려 손계산과 대조 — 옛 코드 6/12 (새 키 셋 없음) → 12/12 · 항등식 (전체 평균 × 7 = `area_AM전체_SE_n` 13 ·
  상별 평균 × N = 4 · 9) · mono 전체 분포 = `AM_S_*` 와 같다 (짝수 개 중앙값 1.5 = 가운데 둘의 평균 · 7b 근거).  값은 5번 coverage 배치 (접촉 단계 포함) 재실행 뒤 생긴다 — 커밋된 09-29/30 배치
  원자료에는 없다 (인계표 무변경 · 7c 에서 census 확장 기록과 함께 싣는다).
- ✅ **7b 구현 (09-30 · 1저자 *"4‴ 안보고 7b로 가도 되는거면 그러자"* · 시험 먼저)** — 생성기 `lhs_design_dataset.py` 의 (B) 규칙:
  - **판별**: 설계 `block` (`mono_AM_P` → AM_P · `mono_AM_S` → AM_S) 이 설계 상을 정한다 (`_mono_design_phase`).  설계 block 과 수확 모양 (`n_types` 2 ·
    `phase_counts` = AM 하나 · coverage 상별 둘 다 `N_A_PHASE_ABSENT` · `coverage_AM_only` = `coverage_AM_total`) 이 어긋나거나 둘 중 하나를 모르면 **거부**
    (조용히 (A) 로 돌아가면 한 표에 두 규약이 섞인다 — 반례 ⑯d3–d10 8 건).
  - **수확기 열**: 설계 상 칸 ← 수확 `AM` (coverage 상별 ← 전체 · `n_AM_*_measured` ← `phase_counts.AM` (**`LHS-21` 해소**) · `cov_*_n_valid` ← `counts.AM` ·
    v3 `wall_touch` 상별 ← `AM`) · 설계에 없는 상의 칸은 빈칸 (status `N_A_PHASE_ABSENT` 그대로 · 0 아님).
  - **웹앱 열**: 웹앱이 단일 AM 에 붙인 반지름 이름을 접촉 열에서 읽어 (두 이름 다 값이면 거부) 설계 이름 칸으로 옮긴다 (`_phase_swap` — `area_AM_S_AM_S_n` →
    `area_AM_P_AM_P_n` 처럼 토큰 전부) · 새 열 `wa_mono_phase_name_webapp` 에 웹앱 이름을 남긴다 (설계와 다르면 = 옮긴 행) · J20-h 접촉 0 쌍은 설계 상으로 판단 ·
    QC `qc_wa_cov_<설계 상>_minus_harvest_pct` = 웹앱 `coverage_<웹앱 이름>_mean` − 수확 전체.
  - **열 사전**: 상별 열 전부 (수확 coverage · `_status` · `n_AM_*_measured` · `cov_*_n_valid` · 벽 접촉 · 웹앱 쌍 · QC) 에 표지 *"mono: 설계 상 칸 = 단일 AM 값 (전체 열과 중복 · J20-k (B))"* ·
    총량 · 설계 열에는 없음.
  - **시험 먼저**: ⑯d–d10 · ⑳b · ⑳f · ⑳h 개정 + ⑳y–af 새로 — 옛 코드 117/137 (20 건 실패 = 전부 (B) 시험) → 137/137.  ⚠ 구현 중 잡은 것: QC 블록의 기존 변수 `wp`
    (웹앱 porosity) 가 새 변수를 덮어 QC 가 비었다 → `wname` 으로 분리 (⑳aa 가 잡았다).
  - **인계표 재생성** (같은 명령 · 재실행 없음): `lhs_handover_20260930.csv` 130×**139** · `lhsx_handover_20260930.csv` 64×**141** (새 열 1 = `wa_mono_phase_name_webapp`) ·
    **바뀐 옛 칸 = mono 행의 상별 칸만 240 · 128 (bimodal 0)** · 이름 옮김 **5 · 4 건** (130: `118 · 121 · 124 · 125 · 126` · 64: `lhsx_003 · 017 · 048 · 062` — 09-30 §0 예측과 같다) ·
    설계 상 칸 ↔ 원천 (수확 전체 · `phase_counts.AM` · `counts.AM` · 웹앱 반지름 이름 값) 대조 **46/46 행 차이 0** · QC 웹앱 피복 − 수확 전체 = 0 (|Δ| ≤ 1.4e-14) ·
    옛 (A) 판은 `912ceea3b` 이력으로 남는다.

- ✅ **7c 구현 (10-01 · 1저자 비준 *"ㄱㄱ 하자"* · 시험 먼저)** — AM–SE CN 10 열 + 고립 비율 3 열 + 전체 분포 3 열 (7a) 을 인계표에:
  - **원천**: 웹앱 = 5번 배치 `docs/data/{lhs,lhsx}_webapp_coverage_1e09f661d/` (`--stop-after coverage` = 접촉 단계 포함 · 생성기 `WA_STAGE_GROUPS` 로
    contact 묶음 수용 · 묶음 제한 없이 부르면 여전히 거부) · 수확 = v2 그대로 (`…_descriptors_20260925` — v3 로 바꾸면 벽 τ · 벽 접촉 열이 켜진다 = τ 차례).
  - **판정 바꿔 싣기** (`WA_VERDICT_OVERRIDE` · 열 사전에 옛 판정 병기): 고립 비율 3 = census 🔶 COND_cov → ✅ (오분류 · `LHS-23` — SE 접촉 0–1 개인
    AM 비율 · 접촉 개수만 센다) · 7a 새 키 3 = census 밖 → **배치 머리에 있을 때만** ✅ (옛 배치의 빈칸이 측정된 N/A 로 읽히지 않게).
  - **관문 (fail-closed · 같은 counts 에서 나온 값인가)**: G1 상별 평균 × 상 입자 수 = `area_<상>_SE_n` · G2 전체 평균 × AM 수 = `area_AM전체_SE_n` ·
    G3 고립 비율 × N / 100 = 정수 개수 · 전체 = 상별 합 · G4 max = 상별 max 최댓값 · G5 median (mono = 상 값 · bimodal = 상별 사이 — 합집합 중앙값
    성질, 무작위 20 만 쌍 위반 0) · G6 합동 std · G7 표면 가중 = Σ N r² μ / Σ N r² (설계 반경 · 실측 최대 상대차 2.4e-12 · 3.5e-13) + 상 있음/없음 ·
    **실데이터 130/130 · 64/64 통과**.
  - **시험 먼저**: 새 ㉑a–w 23 건 + 픽스처 일관화 (`_wa3` 의 AM_*_se_cn_mean 이 쌍 개수와 모순이었다 — 새 관문이 바로 잡았다) · ⑳a · b · d · y 기대 갱신 —
    옛 코드 134/160 (26 실패) → 160/160.  웹앱 (J20-l): 고립 비율 영문 라벨 · 쉬운 설명 · 툴팁 · 피팅 보고서의 "coverage 낮아 / 살짝 덮여" 설명을
    "SE 접촉 0–1 개" 로 (`webapp/test_am_isolation_labels.py` 옛 0/7 → 7/7) · ⚠ 웹앱 케이스 화면은 AM–SE CN **평균**만 보인다 (std · median · max 행 없음 — 보고).
  - **인계표** `docs/data/lhs_handover_20261001.csv` 130×**155** · `lhsx_handover_20261001.csv` 64×**157** (+16) · **옛 칸 변경 0** (이름 기준 대조) ·
    상별 열 채움 115/130 · 56/64 (bimodal + 설계 상 mono) · 전체 열 130/130 · 64/64 · 재생성 바이트 동일 · 0930 판은 이력.

## J20-l. 닫힌 열은 웹앱에도 같은 정의로 (09-30 밤 · 1저자 — *"지금 해당 닫힌 parameter 들도 잘 webapp 에 반영됐는지 확인하고 앞으로 하나 완성되면 webapp 수정하고 그런식으로 가자"*)

- **규칙 (운영)**: 인계표에 싣기로 닫은 열 (함수 검토 · 정의 · 한정어 확정) 은 그 **같은 정의 · 이름 · 한정어** 가 웹앱 (케이스 페이지 · 그룹 비교 · 보고서 · CSV · 도움말) 에도
  보이도록 고친다 — 열 하나가 닫힐 때마다 웹앱 수정을 같은 묶음에서 한다 (보고 → 설명 → 비준 → 실행 · 시험 먼저).
- **첫 감사 대상 (09-30 밤)**: coverage 를 **hertz (DEM 기하 교차 원판 `c_cpl[22]` — 이름만 hertz · L1-04) · physics (legacy Tabor · 부피 · 기하 cap) · physics v2 (미검증 후보 · `LHSC-10`)** 로
  나눠 보이기 + 이미 닫힌 여섯 — porosity union (인계 = `porosity_union_exact_pct` · MC 정확 union) · 두께 (`thickness_mass_conserving_um`) ·
  φ_SE · φ_AM ((라) `phi_*_mass_conserving`) · 계면 개수 (`area_<쌍>_n` · J20-g · h) · SE–SE CN (J20-i) · AM–AM CN (J20-j).
- 감사 결과 · 수정안은 판정 기록을 이 절에 덧붙인다 (⬜ 보고 → 비준).
- ✅ **비준 09-30 밤 (1저자)**: 순서 = HBR10-01 · 03 → **웹앱 ① (표시만)** → ② (값 · 경로) → ③ (정확 union · v2 후보) · (가) 두 공극률을 나란히 (ε_sphere 생산 규약 + ε_union · 강등 없음) ·
  (나) v2 는 ③ 에서 "후보 · 미검증" 표지로 (등급 · ML 제외).
- ✅ **웹앱 ① (09-30 밤 · 시험 먼저 — `webapp/test_closed_param_labels.py` 옛 코드 4 PASS · 47 FAIL → 55/55)** — 계산 불변 · 이름 · 한정어만:
  네트워크 표 열 머리 **Hertz 계열 (LIGGGHTS c_cpl[22] 기하 교차 원판)** · **Physics 계열 v1 (Tabor · 부피 · 기하 cap)** (절 머리 셋 포함) ·
  공극률 두 줄 **ε_sphere (구 부피 합 · 생산 규약)** + **ε_union 쌍 렌즈 (벽 밖 미제거)** · 두께 = **판 간격** + 배지에 `plate_z_source` (판 메시 / ⚠ 최고 입자 중심 추정) ·
  φ_SE = 구 부피 합 ÷ 판 간격 · **AM–AM CN std 행** (J20-j 세 열 중 화면에 없던 것) · coverage 툴팁 = 입자별 `min(100, 100·ΣA(AM–SE)/(4πr² − ΣA(AM–AM)))` 평균 (두 열 = 분자 면적만 다름) ·
  면적 툴팁 = c_cpl[22] (옛 "Hertz 접촉역학 기반" 삭제) · SE–SE · AM–AM CN = 입자–입자 덤프만 (벽 안 셈) · 모집단 σ ·
  접촉 요약 · 배위수 탭 = 탭 문맥 툴팁 (옛 판은 접촉 요약 AM–AM 행에 **파괴 severe % 툴팁**을 붙였다) · 라벨 → 툴팁 역맵 전수 (SELF-51 개명 때 끊긴 σ_ionic SE 크기 인자 행 복구) ·
  그룹 비교 열 툴팁 12 · MD 보고서 · 그룹 보고서 · AI 분석 표 · 인용 철회 둘 (coverage 툴팁의 "Minnmann 2021 40–65 %" — 인용 뿌리 감사 E7 · MI-5) · σ_grain "grain interior" → 펠릿 (SELF-51).
  ⚠ **감사 중 정정** — 웹앱 ε_union 은 **공극 상한이 아니다**: 벽 밖 부피를 안 빼서 `docs/data/lhs_union_20260927/` 194/194 건에서 정확 union 보다 낮다
  (중앙 −0.64 %p · 범위 −3.43 … −0.19 · lhsx −0.75 %p · 벽 밖까지 빼면 차 중앙 0.001 %p).  `lhs_union_webapp.py` docstring 의 "① = 공극 상한" 도 틀렸다 → `SELF-72`.
- ✅ **웹앱 ②-a (09-30 밤 · 파이프라인 값 — 시험 먼저 `webapp/test_closed_param_values.py` 옛 코드 12/28 → 28/28 · 합성 침대 다섯을 웹앱과 같은 CLI 로)**:
  (a) `full_metrics.json` 의 numpy 값이 `default=str` 로 문자열 (`am_am_n_contacts` '412') 이던 것 → 쓰기 `metrics_json.json_default` (int · bool · float) ·
  읽기 `metric_number` 로 옛 케이스의 숫자 문자열도 숫자 (그룹 선택기 · 그룹 그림 · **예측기** — 예측기 자동 타깃은 빠진 값을 0 으로 채워 옛 케이스가 가짜 0 이 될 뻔했다) ·
  (b) 두 상이 침대에 다 있는데 접촉 0 인 쌍 = **측정된 0** (`area_<쌍>_n` 0 · `_total` 0 · `_mean` 없음 · 접촉 요약 행 · 평균 '—') · 상이 없으면 쌍 없음 (J20-h 와 같은 규칙) ·
  (c) τ 가 없어도 `phi_se` · `phi_am` (σ_Bruggeman 두 행만 τ 조건 · 원장 `DESC-01`) · (d) 분석기가 `porosity_union` · `overlap_fraction_pct` · `porosity_spheresum` 을
  **직접** 저장 — 재분석 경로 (batch_rerun_physics · archive_reanalyze · stop_after contact/coverage) 에서도 남는다 ·
  (h) 비정사각 상자 = x · y (`calc_porosity(_dual)` · `recompute_porosity_dual.compute_dual`) — 코퍼스 163/163 정사각형이라 값 영향 0.
  ⚠ **(d) 보고 정정** — 착수 전 보고의 *"2e 는 다른 판 · 상자 규칙이라 처방 뒤 화면 ε_union 이 조금 바뀔 수 있다"* 는 **틀렸다**: 2e 는 원 공극률에 고정해
  ε_u = ε_s + 겹침 · (1 − ε_s) 로 쓰므로 판 · 상자 규칙이 최종값에 들어가지 않는다 → 분석기 값 = 2e 값 (시험 D2 · 1e-9) · 기존 케이스 값 변화 0.
  웹앱: 접촉 요약 툴팁 (0 행 · '—' · N/A · 옛 케이스는 재분석해야 0 행) · φ_SE 툴팁 (τ 없어도 나온다) · 파이프라인 변경이라 WSL 5번 봉인 (1e09f661d) 이후 세대.
- ✅ **웹앱 ②-b (10-01 · 표시 · 경로 — 시험 먼저 `webapp/test_closed_param_groupview.py` 옛 코드 3 PASS · 13 FAIL → 38/38 · 값 · 점수 계산 불변)**:
  (e) 그룹 비교 표의 열 정의 · '낮을수록 좋음' 집합을 모듈 수준 `GROUP_DISPLAY_KEYS` · `GROUP_LOWER_BETTER` · `_group_best_marks` 로 옮기고 **표 열 이름과 같은 철자**를 시험이 강제 —
  porosity union · overlap · SE–SE CN std · **AM–AM CN std (새 열 · J20-j)** 를 넣음 · ⚠ 감사 중 새로 잡은 것: 옛 집합의 `'Vulnerable'` 이 표 열 `'AM Vulnerable'` 과 철자가 달라
  AM Vulnerable 이 **거꾸로 (높을수록 좋음) 강조**되고 있었다 · 표에 없는 이름 (τ std · GB Density · SE Cluster) 제거 ·
  (f) 등급 엔진 `_grade_axis` 가 `source_key` · `fallback_note` 를 낸다 — physics 키가 없어 Hertz 계열 (c_cpl[22]) 대체 키로 채우면 *'⚠ Hertz 계열 대체 … 문턱은 physics 기준'* ,
  physics → physics 대체 (B3 없음) 는 *'⚠ 대체'* 로 · basis (툴팁 · 보고서) 앞에도 · 등급 표 라벨 옆 `⚠대체` · 3D 뷰어 피복 범례가 `viewer3d_data.coverage_map_column` 으로
  읽은 열을 표시 (physics 열 없으면 *'⚠ Hertz 계열 대체'*) · (g) 그룹 그림 `porosity_union` · `overlap_fraction_pct` 등록 (옛: `[SKIP] Unknown`) — 값이 없는 (재분석 전) 케이스는
  0 으로 그리지 않고 빠진다 · 모든 그림 체크박스 값 ⊆ 그림 목록을 시험이 강제 (누락은 이 둘뿐이었다).
- ✅ **웹앱 ③ (10-01 · 시험 먼저 `webapp/test_closed_param_exact_union.py` 옛 코드 3 PASS · 15 FAIL (W5 는 조인 뒤 실패 쪽) → 36/36)** — 분석 단계 (analyze_contacts → `dem_analysis_core.run_full_analysis`) 가
  ε_sphere 와 **같은 판 · 같은 상자**로 `calc_porosity_union_exact` 를 돌린다 = 상자 [0,Lx)×[0,Ly)×[0,판) 무작위 점 (기본 4×10⁶ · env `DEM_UNION_MC_N` · 0 = 끔) ·
  x · y 주기 · 세 입자 겹침까지 정확 · 벽 밖 부피 제외 — **인계표와 같은 계산** (`lhs_union_webapp.coverage` 를 그대로 import · 복제 없음) · 3.3 만 입자 침대 ≈ 10 s.
  full_metrics 새 키: `porosity_union_exact_pct` · `_se_pct` (1σ) · `union_exact_mc_n` · `_mc_seed` · `union_exact_status` · `wall_overhang_over_Vbox_pct` ·
  `porosity_union_pair_clipped_pct` · `union_pair_upper_bound_ok` (쌍 렌즈 + 벽 밖 제거 ≥ 정확 − 4σ — 어기면 접촉 덤프에 겹친 쌍이 빠진 것) · `se_of_solid_vol` ·
  `thickness_mass_conserving_um` = 판 간격 × (1 − ε_sphere)/(1 − ε_exact) · `phi_{se,am}_mass_conserving` = (1 − ε_exact) × 부피 몫 (J20-e (라) · 닫힘 = 1).
  해석해 시험: 겹친 두 구 · 바닥을 뚫은 구 · 주기 경계 · 같은 자리 세 구 (쌍 렌즈가 틀리는 곳) · 비정사각 상자 — 4σ 안.  분석기에 있으므로 재분석 경로에서도 남는다.
  웹앱: 케이스 배지 (정확 union ± 1σ · 두께 질량 보존) · 망 요약 행 넷 · 그룹 표 열 넷 (정확 union · 질량 보존 두께 = 낮을수록 좋음) · 그룹 그림 · MD 보고서 · 쉬운 설명 · AI 표 정의 ·
  **physics v2 = 후보 · 미검증** (`inject_physics_v2_rows` — 망 요약 끝에 표지 붙은 절 · Physics 열에만) · 예측기 자동 타깃에서 `*_physics_v2` 제외 (`_fm_auto_target_ok` ·
  ⚠ 감사 중 발견: v2 가 이미 자동 타깃 후보였고, 자동 타깃은 빠진 값을 0 으로 채운다 = 원장 `PRED-01` 열림) · 등급 축엔 원래 v2 없음 (시험 V7).
  ⚠ 파이프라인 (분석기) 변경 = 5번 봉인 (1e09f661d) 이후 세대 · 옛 케이스는 재분석해야 값이 생긴다 (그 전엔 배지 · 행 · 열이 비고, 그림은 점을 안 찍는다).

## J20-m. coverage 인계 열 = 기하면적만 — physics v1 · v2 제외 (10-01 · 1저자 *"그래 그럼 그렇게 하자"* · 원장 `LHS-25` · `LHS-26` · `SELF-74`)

- **계기**: 5번 배치 (봉인 `1e09f661d` · WSL tar sha256 e7d649f5… · LHS 130 + lhsx 64) 보고에서 내가 v2 빈칸 18 침대를 *"이웃 AM 과 아주 깊이 겹친 경우 ·
  오류가 아니라 설계대로의 동작"* 으로 설명했다 → 1저자 *"이런 경우가 세상에 어딨어"* → 원자료 대조로 **그 설명이 틀렸다** (`SELF-74` — 같은 문구가
  `coverage_physics_vs_hertzian.py` 의 LHSC-01 주석에도 있었다 · 정정).  이어서 *"머신러닝 디스크립터로 줄 수 있는 값인가"*.
- **대조 — 같은 입자 · 같은 접촉을 두 면적으로** (5번 배치 원자료 · 수확기 JSON + 웹앱 `metrics_flat.csv`):

  | | 기하면적 (LIGGGHTS c_cpl[22] · 인계표 `coverage_*_hertz_pct`) | physics v2 (후보) | physics v1 (legacy) |
  |---|---|---|---|
  | 분모 (4πr² − ΣA(AM–AM)) ≤ 0 인 AM | **0 / 1,320,178** (194 침대) | **18 침대 · 73 AM** (LHS 70 / 17 침대 · lhsx 3 / 1) — 첫 사례 = 전부 bimodal 침대의 AM_S (r 0.5 µm 15 · 0.68 µm 1 · 1 µm 2) | 분모의 AM–AM 이 기하면적이라 안 무너짐 |
  | 100 % 로 잘린 AM | **0** | **22.41 %** (LHS) · **97.04 %** (lhsx) | AM 단위 산출 없음 |
  | 침대 평균 ≥ 99 % | 0 | LHS 29/113 · lhsx 62/63 (lhsx AM_P 55/55 = 100.000 상수열) | LHS 29/130 · lhsx 62/64 |
  | 값 범위 (전체) | LHS 2.44–50.01 % · lhsx 37.93–61.43 % | — | LHS 5.92–100 · lhsx 96.58–100 |
  | cap 충돌률 (÷ 접촉 · ok 침대) | — | LHS 중앙 0.048 (0.018–0.623) · lhsx 0.018 (0.015–0.045) | — |

- **원인 (둘이 같은 뿌리)**: physics 는 접촉마다 추정한 소성 면적 (Tabor F/H · SE 경도 0.85 GPa — 기하 원판의 약 3 배) 을 **표면 한도 없이** 더한다 —
  접촉 조각끼리 겹치는 부분을 빼는 규칙이 없다.  AM–SE 쪽 → 100 % 포화 (클립이 가림) · v2 의 AM–AM 쪽 (SE 경도 · `L1-03` · 접촉 하나가 작은 쪽 표면의
  절반 2πr² 까지) → 분모 ≤ 0 (빈칸).  legacy 부피 cap 은 194 침대 어디서도 안 잡는다 (`DESC-03` 과 정합).  포화 문턱: Hertz 전체 ≥ 36.8 % 인 LHS 침대는
  전부 v1 ≥ 99 % · lhsx 는 Hertz 최소 37.9 % 라 코호트 전체가 문턱 위.  v1 포화 29 침대 = AM 70–75 wt% (φ_SE 중앙 0.51 · 나머지 101 침대 0.26).
  ⇒ 기하면적으로는 세상에 없는 경우 (면적 합 > 입자 표면) 가 0 건이고, 그것을 만드는 것은 physics 면적 식이다.
- **결정 (1저자 비준)**:
  1. LHS · lhsx 인계 coverage = **기하면적 열만** (`coverage_AM_{P,S,total}_hertz_pct` + 수확기 벽 제외 proxy) — 지금 인계표 그대로 (변경 0 · 시험 K4 가 physics 열 부재를 강제).
     physics v1 · v2 · rough 는 인계하지 않는다.
  2. physics 는 망 전도도 · 등급 · 웹앱에서 **바꾸지 않는다**.  ⚠ 그쪽 쓰임새는 **이 결정이 닫지 않는다** — σ_ionic T1 이 cov_Hertz 를 쓰는 근거
     (CLAUDE.md 기록 · Spearman 0.697 vs 0.476) 는 **코드 함수 검토 전**이다 (1저자 10-01 *"이걸로 닫지 말고 아직 · 저거에 대해서 코드를 아직 안 뜯어봤으니까"*) ·
     등급 physics 피복 축의 판별력도 코퍼스로 확인 안 함 → `LHS-25` 열림 항목.
  3. 웹앱 표지 (J20-l · 시험 먼저 `webapp/test_coverage_handover_scope.py` 옛 코드 3 PASS · 13 FAIL → 16/16): 케이스 피복 툴팁 셋 (AM_P · AM_S · AM) 에 포화 · 인계 제외 한정어 ·
     ③ 이후 낡은 문장 (*"v2 후보 연산자는 … 아직 표시하지 않는다"*) 정정 · v2 절 머리 + v2 행 툴팁 셋 (분모 무효 · 포화 · 같은 원인) · 쉬운 설명 두 줄 (포화) ·
     rough 쉬운 설명의 *"가장 믿을 만한"* 철회 (①에서 METRIC_TIPS 쪽만 철회됐던 잔재 · 인용 뿌리 감사 E7 · MI-5 계열) · 코드 주석 정정 (`SELF-74`).  계산 · 값 변경 0.
- **합리성 검사** (1저자 *"coverage 로 나온 값들이 다 합리적인 값인지 확인해봐"* · 서브에이전트 · 읽기 전용 · 보고서 `docs/reviews/lhs_coverage_reasonableness_20261001.md` ·
  내 독립 계산 네 수치와 일치): **계산 결함 신호 0** — 0–100 밖 · NaN · 개수 항등식 · 순서 (7 순서 × 3 칸 × 2 코호트) 위반 0 · 수확기 ↔ 웹앱 Hertz 최대 1.42e-14 %p ·
  mono 상 누출 0 · 잔차 z > 4 인 LHS 8 침대 전부 설계로 설명 (SE 5 wt% 얕은 겹침 2 · d_S 1 µm AM_S 무리 6 — 같은 침대 AM_S 피복을 모형에 넣으면 6 곳 모두 사라짐).
  분류: 기하면적 · 벽 제외 ✅ · legacy v1 🟡 (LHS 상단 22–25 % 판별 없음 · lhsx 사실상 불가) · rough 🟡 + ⚠ (`LHS-26`) · v2 🔴.
- **인계 한정어** (열 사전 · 인계 README 에 붙일 것 — 다음 인계표 재생성 때): ① 기하 교차 원판 (Hertz 탄성 아님 · L1-04 — 열 사전에 이미 있음) ② SE-rich 과압축 영역
  (ε_sphere < 0: lhsx 60/64 · LHS 18/130) 의 절대값 ③ AM 90–95 wt% 침대의 SE 바닥 몰림 (**추정** — 바닥 접촉 AM 피복 / 내부 1.4–6.3 배 · SE 바닥 · 플래튼 접촉 수 비와 ρ +0.81 ·
  원자 z 분포는 직접 안 봄) ④ porosity 와 공선 (LHS ρ −0.985) · AM wt% 와 ρ −0.94 ⑤ AM_P 소표본 (n_P ≤ 10: LHS 12 · lhsx 9 침대 — `n_AM_P_measured` · `cov_AM_P_n_valid` 는 표에 있음)
  ⑥ 옛 코퍼스와 섞을 때 치밀도 보정 필요 (같은 SE/고체 0.3–0.5 에서 LHS 가 25–47 % 높음 — 더 치밀 · 생산 조성 근처 21.0 % 는 옛 18–22 % 와 같다).
- `LHSC-10` 의 5번 보고 요구 중 무효 분모율 (AM 0.0059 % · 0.0022 %) · 제외율 (침대 17/130 · 1/64) · 클립 · cap 충돌률 = 위 표 · 보고서 §1-2 · §4.
  근접 접선 수는 산출물에 없다 (원 덤프에서 세야 함).
- ✅ **5번 원자료 커밋 (10-01 · 1저자 *"ㄱㄱ 하자"*)**: `docs/data/{lhs,lhsx}_{descriptors_cov,webapp_coverage}_1e09f661d/` (200 파일 · tar sha256 e7d649f5… · README) ·
  옛 기준선 대조 보고서 `docs/reviews/lhs_coverage_batch5_comparison_20261001.md` · 합리성 검사 스크립트 `docs/reviews/lhs_coverage_reasonableness_20261001/`
  (리포 원자료만으로 보고서 바이트 동일 재현) · 대조 보고서의 🔴 `dirty` 193/194 = 피복 단계가 추적 파일 요약 CSV 를 덮어쓴 것 (코드 변경 아님 · `LHS-27`).
  ⇒ 다음 = **7c** (AM–SE 배위수 · 고립 비율 · 분포 — 이 폴더의 웹앱 열).

## J20-n. ② 퍼콜레이션 · 벽 τ (Dijkstra) 인계 (10-01 · 1저자 *"퍼콜레이션은 그렇게 가고"* · *"dijkstra tortuosity 벽을 확실하게 닫고 값을 추출해두자 · laplace는 차근차근"* · 시험 먼저)

- **② 퍼콜레이션 7 열** (`--webapp-groups contact,percolation` · 접촉 분석 단계 산출 — 09-29 contact 배치 · 5번 배치 둘 다 130/130 값):
  `percolation_pct` · `top_reachable_pct` · `n_components` · `n_large_components` · `ionic_active_pct` · `se_se_cn_perc` · `se_se_cn_n_perc`.
  - **판정 바꿔 싣기** `LHS-20`: `top_reachable_pct` · `ionic_active_pct` = census 🔶 COND_cov → ✅ (SE 그래프 양 · coverage 를 읽지 않는다 · 옛 판정 열 사전 병기).
  - **안 싣는 것**: `electronic_active_fraction` (census ✅ 지만 **망 단계** 산출 — 접촉 · coverage 배치에 값이 없어 빈칸 = 측정된 N/A 로 읽힌다) ·
    `se_se_cn_eff_area_perc` (면적 · ⑦ 차례).
  - **열 사전 F3 한정어** (`LHS-19`): `n_components` 외톨이 포함 (단절 침대는 사실상 외톨이 수) · `n_large_components` 문턱 10 = 출처 없는 코드 상수 ·
    `percolation_pct` = 밴드 규칙의 그래프 관통 (솔버 전류 관통과 다른 정의 · 0.0 = 진짜 미퍼콜) · `top_reachable_pct` · `ionic_active_pct` 는 위 밴드의 외톨이도 센다 ·
    `se_se_cn_*perc` 비관통 = 빈칸 (N/A) · 경계 폴백 `LHS-17` · 겹침 `LHS-18` 은 CAVEAT 로.
  - **관문** (fail-closed · 실측 **130/130 · 64/64**): P1 관통 일관 — `percolation_pct > 0` ⟺ `_perc` 두 열에 값 ⟺ 수확기 벽 밴드 관통
    (`tau_detail.band_detail.wall_n_span_components > 0` · J20-b F8 독립 재현) · P2 범위 · 순서 (비율 ∈ [0, 100] · 성분 수 정수 · `n_large ≤ n_components` ·
    `top_reachable ≥ percolation`) · P3 관통 SE 개수 `se_se_cn_n_perc` = `percolation_pct × N_SE / 100` (실측 최대 차 1.5e-11).
  - ⚠ lhsx 64 는 J20-b 감사기 (`lhs_perc_audit.py` · 폴백 · 겹침 · 재현) 를 **돌리지 않았다** — 관문 P1 (수확기 독립 재현) 64/64 로 대신 · WSL 에서 한 번 돌리면 닫힌다 (몇 분).
- **벽 τ** (`tortuosity_SE_wall` · `_median` · `_status` · `tau_wall_n_*` · `tau_wall_convention`) — 원천 = **수확 v3** (5번 `docs/data/{lhs,lhsx}_descriptors_cov_1e09f661d/`) ·
  v2 → v3 로 바꿔도 **옛 칸 변경 0** (130 · 64) · 함께 켜지는 벽 접촉 비율 8 열 (J20-a ⓓ) 도 싣는다.
  - **함수 검토** (`lhs_descriptor_harvest.tortuosity_se` → `_tau_sample`): SE 그래프 (원자 좌표 기하 접촉 d ≤ r_i + r_j · x·y 주기 — 덤프 접촉과 같은 집합 J20-a) ·
    벽 밴드 (바닥 z − r ≤ 0 + r_SE,max · 플래튼 z + r ≥ plate_z − r_SE,max) · 두 밴드를 **같은 성분 안에서** 잇는 쌍 전부 중 무작위 200 쌍 (seed 42) ·
    Dijkstra 최단경로 (가중 = 중심 거리) / 두 끝 중심 |Δz| · [1, 20) 절단 평균 · 중앙값 · 상태 OK · NOT_PERCOLATING (잇는 성분 0) · NO_VALID_SAMPLED_PAIR ·
    ELECTRODE_BAND_EMPTY · N_A_PHASE_ABSENT.  수정 불요.
  - **실측**: 130 = OK 106 · NOT_PERCOLATING 24 · τ 1.292 / 1.494 / 4.151 (최소 / 중앙 / 최대) · 절단 0 · 64 = OK 64 · τ 1.262 / 1.365 / 1.600 ·
    `percolation_pct > 0` ⟺ τ OK **130/130 · 64/64**.
  - **관문**: T1 관통 성분 수 (정수 · OK ⟹ > 0 · NOT_PERCOLATING ⟹ 0 · 수확 벽 밴드 진단과 같아야) · T2 값 · 표본 (OK ⟹ 평균 · 중앙값 ∈ [1, 20) ·
    0 < n_valid ≤ n_sampled ≤ 200 · 0 ≤ n_truncated < n_valid) · T3 (② 와 함께 실리면 NOT_PERCOLATING ⟺ percolation_pct 0) · 관문 상수 = 수확기 상수 (selftest ㉓d).
  - **열 사전**: ⚠ **기하 최단경로 τ — 수송 τ 가 아니다** (협착 · 단면 병목을 보지 않아 1 근처) · COMSOL/EIS 입력 τ 는 τ_Laplace,eff = √(φ_SE·σ_grain/σ_full)
    (망 단계 · 이 표에 없음 — 1저자 *"laplace는 차근차근"*) · 비관통 = 빈칸 (N/A).
  - **벽 접촉 비율 문구 정정**: 옛 문구 "z − r ≤ 0 · z + r ≥ plate_z" (접선 포함) 는 수확기 `WALL_TOUCH_RULE` (겹침 깊이 > 0 · 접선 제외) 와 달랐다 → 같은 규칙으로.
- **시험 먼저**: 생성기 ㉒a–q (②) · ㉓a–l (τ) + ⑲s · ⑳d 갱신 — 옛 코드 (7c 판 `8c18a7558`) 161/189 → 189/189 (τ 구현만 뺀 판 178/189).
  웹앱 (J20-l): `webapp/test_percolation_labels.py` — SE Cluster 수 · Ionic Active AM 영문 라벨 · 툴팁 넷 (외톨이 · 문턱 10 · 밴드 규칙 ≠ 솔버 · top_reachable ≥
  percolation (옛 문장은 부등호가 거꾸로) · coverage 무관) · ⚠ 웹앱은 벽 τ 를 계산 · 표시하지 않는다 (웹앱 τ = `calc_tortuosity` 밴드 규약 · `DESC-02` 열림 — 보고).
- **인계표** (같은 날 판 덮어씀 · 7c 판은 `8c18a7558` 이력): `docs/data/lhs_handover_20261001.csv` 130×**177** · `lhsx_handover_20261001.csv` 64×**179** (+22 = ② 7 + 벽 τ 7 + 벽 접촉 8) · **옛 칸 변경 0** · 관문 G1–G7 · P1–P3 · τ T1–T3 **130/130 · 64/64** · 재생성 바이트 동일 · 명령 = `--harvest docs/data/{lhs,lhsx}_descriptors_cov_1e09f661d --webapp docs/data/{lhs,lhsx}_webapp_coverage_1e09f661d --webapp-groups contact,percolation` (+ union · lhsx `--design docs/data/lhsx_design_adapted_20260929.csv`).
- ⬜ 남은 것: τ_Laplace (망 단계 배치 · 1저자 *"차근차근"*) · lhsx perc 감사기 1 회 · 배포 보류 해제 (1저자) · ③ 이후 묶음 (σ_VM · F1 · Auerbach · A_dem_geometric).

## J20-o. ✅ 배포 보류 해제 · 배포 v1 (10-01 · 1저자 *"해제하고 최소 단위로 나가고 프롬프트에 관련해서 잘 작성해주고"*)

- **배포 묶음** `docs/data/lhs_release_20261001/` — `lhs_release_20261001.csv` 130×74 · `lhsx_release_20261001.csv` 64×73 (설계 입력 16–17 + 측정 디스크립터 57) ·
  열 사전 (정본 인계표 사전의 같은 줄) · `README.md` (규약 · 이름 주의 · 안 넣은 것 · 한계 · **AI 도구에 붙여 넣을 프롬프트**).  값은 정본 인계표
  `lhs_handover_20261001.csv` 의 **열 부분집합** (한 글자도 안 바꿈) · 안 넣은 것 = 체크리스트 §3 그대로 (구 부피 합 porosity 계열 · 내부 QC · 상태 열 · 감사 전 ③–⑦).
- **고립 위험 ↔ 고립 구분** (1저자 10-01 *"내가 알고 있는 고립은 저 얘기"* · *"'고립 위험' 이렇게 나누면 좋을거 같고"*): `*_vulnerable_pct` = SE 접촉 0–1 개 = **고립 위험** ·
  경로 기준 **고립** (이온이 못 가는 AM) = `100 − ionic_active_pct` (SE 무접촉 + 닿은 SE 가 분리막 쪽으로 안 이어짐).  예 `lhs00_083`: 위험 0.1 % · 고립 89 % ·
  130 의 비관통 24 침대 고립 61–97 % (중앙 89) vs 위험 0–95 % (중앙 4).  열 사전 · README 문구 정정 (값 변화 없음).
- ✅ **v1.1 비준 10-01** (1저자 *"비준이야"* · 구현 = **J20-p**) — 제안 원문: ① 경로 기준 고립 열 `am_ionic_isolated_pct = 100 − ionic_active_pct` (재실행 없음 · 항등식) ② 그 분해 (SE 무접촉 · 경로 단절 · 상별)
  = 웹앱 `calc_ionic_active_am` 의 `dead_pct` · `no_se_pct` 내보내기 + 접촉 단계 배치 재실행 ③ 비관통 24 침대의 연속 디스크립터 — 수확 v3
  `tau_detail.band_detail.largest_comp_z_span_frac` (가장 큰 SE 덩어리가 두께를 얼마나 가로지르나 · 비관통 0.10–0.90 중앙 0.37 · 관통 0.88–0.99) ·
  `largest_comp_frac` (재실행 없음 · 함수 검토 필요).  τ 는 빈칸 유지 (두 단계 모델 권고 — README §7).

## J20-p. v1.1 ①②③ 구현 (10-01 · 1저자 *"비준이야"* · *"우선 이거 해결하자"* · 시험 먼저)

- **① 경로 기준 고립** `am_ionic_isolated_pct` = 100 − `ionic_active_pct` — 생성기 **유도** (재실행 없음 · 활성 열이 실리면 늘 실린다) · 웹앱 v1.1 도
  같은 이름 · 같은 식으로 내보낸다 (배치에 있으면 같아야 — D1).  새 관문 **D3** = 활성 비율 × N_AM / 100 = 정수 개수 (분해 키가 없는 5번 배치에서도 — ①의 원천).
  실측 130: 관통 106 = 0–52.7 % (중앙 0) · 비관통 24 = **61.4–96.9 %** (중앙 89.3) · 64: 0–0.13 % · **고립 위험 (접촉 0–1 개) 보다 20 %p 넘게 큰 침대 24**
  (예 `lhs00_018` 위험 0.09 % ↔ 경로 고립 85.4 % · `lhs00_083` 0.1 % ↔ 89 %) — 두 "고립" 을 가르는 이유가 이 표에서 보인다.
- **② 분해** (단절 = SE 는 닿았지만 닿은 SE 가 위 밴드로 안 이어짐 · 무접촉 = SE 접촉 0 · 상별 셋) — 웹앱 `calc_ionic_active_am` 이 계산하고 버리던 값 +
  상별 단절 · 무접촉 계산 추가 → `analyze_contacts` 가 `ionic_dead_pct` · `ionic_no_se_pct` · `{AM_P,AM_S}_ionic_{active,dead,no_se}_pct` · `am_ionic_isolated_pct`
  를 내보낸다 · 케이스 표 새 세 줄 (경로 기준 고립 · 단절 · 무접촉).  **시험 먼저** `analyze_contacts --selftest` 12/16 → **18/18** (⑬–⑱ · 웹앱과 같은 CLI 로
  3 상 · mono 작은 침대 · 손 계산 · 고립 위험 5/7 ≠ 경로 고립 4/7 인 픽스처).  생성기: census 밖 새 키 = **배치 머리에 있을 때만** (5번 배치엔 없음 → 열 없음 ·
  빈칸이 측정된 N/A 로 읽히지 않게) · 관문 **D1** 합 100 · **D2** 상별 합 100 · **D3** 정수 개수 · **D4** 상별 개수 합 = 전체 · **D5** 무접촉 ≤ 고립 위험 (7c 와
  같은 접촉 집합 — SE 접촉 0 ⊂ 0–1 개) · 상 있음/없음 · mono 는 설계 상 칸.  ⬜ **WSL 접촉 단계 배치 재실행** (130 + 64 · 새 디렉터리) → 원천 교체 → 옛 칸 대조.
- **③ 가장 큰 SE 덩어리** — 수확 v3 `tau_detail.band_detail` (벽 τ 와 같은 SE 그래프) · 함수 검토 `lhs_descriptor_harvest.tortuosity_se:1293–1322`:
  가장 큰 = **SE 수** 기준 성분 (가장 멀리 뻗은 성분이 아닐 수 있다) · 폭 = 성분 SE 의 max(z + r) − min(z − r) · ⚠ **원값의 분모 = 전 입자 (AM 포함) z 범위**
  — 바닥 아래로 샌 입자 · 벽과 겹친 입자 (z_lo 최저 −5.4 µm) 에 끌려 벽 간격보다 **3–20 %** 크다 (130 중앙 7 % · 64 중앙 6 %) → 침대마다 다르게 작아진다.
  ⇒ 1저자 질문 (한정어로 싣나 · 수확기 재실행하나) 의 **셋째 길**: 수확 JSON 에 z_lo · z_hi · plate_z · 바닥이 기록돼 있어 **벽 간격 기준으로 정확 환산**
  (= 원값 × 전 입자 z 범위 / 벽 간격 · 재실행 없음).  열 `se_largest_comp_frac` · ★ `se_largest_comp_wall_span_frac` (인계) · `se_largest_comp_env_span_frac`
  (원값 · 내부 참고) · 관문 **C1** SE 수 = phase_counts · 비율 × N_SE = 정수 · **C2** 원값 ∈ (0, 1] (성분 ⊂ 전 입자) · **C3** 플래튼 = `plate_z_sim` · 바닥 =
  `z_floor_sim` · 수확 세대 혼합 거부.  실측 130 비관통 24: SE 비율 **0.002–0.91** (중앙 0.026) · 벽 폭 **0.11–0.96** (중앙 0.39) · 관통 106: 0.43–1.0 · 1.01–1.05 ·
  64 (전부 관통): 0.999–1.0 · 1.02–1.06 (표면이 벽 · 플래튼과 겹쳐 1 을 넘는다).
- **웹앱 (J20-l)**: 케이스 표 · 옛 세대 보정 (부모 = 100 − 활성 · 분해 두 줄은 — · 0 으로 안 채움) · 영문 라벨 · 역방향 맵 · 툴팁 (고립 위험과 다른 양) ·
  그룹 비교 세 열 (낮을수록 좋음 · 옛 세대는 로드 때 100 − 활성) · MD 보고서 · 쉬운 설명 · 표 재구성기 — `webapp/test_ionic_isolation_labels.py` **0/13 → 13/13**
  (게이트 배선) · ⚠ 웹앱은 ③ 을 표시하지 않는다 (수확기 산출 · 웹앱이 계산하지 않는 값 — 보고).
- **인계표** (같은 날 판 덮어씀 · 이전 판 = `8b84ba476`): `lhs_handover_20261001.csv` 130×**181** · `lhsx_handover_20261001.csv` 64×**183** (+4 = ① 1 + ③ 3) ·
  **옛 칸 변경 0** (열 순서 유지) · 관문 D (① 원천) · C **130/130 · 64/64**.  생성기 시험 189/207 → **207/207** (㉔a–r · 픽스처 정합 1 건: ㉒ q2 활성 45 % × 11
  = 4.95 개 → 5/11 · 새 D3 가 잡는 모양).
- ✅ **배포 v1.1** = J20-q (10-01 · 배포 v1 `docs/data/lhs_release_20261001/` 은 그대로).
- ✅ **Codex 최종 리뷰 (10-01)** = 고정 v1.1 계산값 전달 **GO** · 물리 타깃 인증 **HOLD** · 새 P1 없음 → J20-r (README = ML 인계본).

## J20-q. 배포 v1.1 (10-01 · 1저자 *"ㄱㄱ"* = 권고 넷 그대로 · 접촉 단계 재실행 반입)

- **원천 교체**: 웹앱 접촉 단계 재실행 `docs/data/{lhs,lhsx}_webapp_contact_d1ec42fba/` (1저자 WSL · 130 + 64 done · 묶음 sha256 `2662f152…5eba55`) — 5번 배치
  (`1e09f661d`) 대비 공통 열 차이는 셋뿐이고 전부 알려진 코드 변경: F1 근접쌍 세 열 (`LHS-22` — 130 중 125 · 64 중 64 · `se_se_cn_aug` 중앙 +0.041 % · 최대 +0.144 % /
  64 +0.023 % · +0.039 % · 줄어든 침대 0) · `phi_se`/`phi_am` 13 건 (`DESC-01` — 옛 판 빈칸) · `area_AM_P_AM_P_{total,n}` 3 + 6 건 (접촉 0 쌍을 0 으로 · J20-h 웹앱 쪽).
  ⚠ 출처 표지 dirty = 작업 트리 추적 파일 변경 — 사유 확인 중 (`LHS-27` 요약 CSV 유력).  같은 날 같은 트리에서 옛 `d8663fe05` 실행이 돌다 섞인 일은 `SELF-76` (그 산출은 반입 안 함).
- **인계표 재생성** (같은 명령 · `--webapp` 만 교체): 130×181 → **189** · 64×183 → **191** = ② 분해 8 열 (`ionic_dead_pct` · `ionic_no_se_pct` · 상별 6) ·
  **옛 칸 변경 0** · 열 순서 그대로 · 관문 D1–D5 · C1–C3 130/130 · 64/64.  생성기 열 사전 문구만 보강: `boundary_state` · `physical_target_status` ·
  `hold_reason_codes` 의 뜻 (값 목록뿐이던 것 — 배포에 싣기 위해) · 생성기 시험 207/207.
- **배포 v1.1** `docs/data/lhs_release_20261001_v11/` — 130×**89** · 64×**88** = v1 열 (값 · 순서 그대로) + 15 열: 이온 경로 고립 9 (① ②) · SE 덩어리 2 (③) ·
  `thickness_wall_gap_um` (측정 두께 — v1 은 유도값인 질량 보존 두께뿐) · ★ **적격성 표지 3** (`physical_target_status` · `hold_reason_codes` · `boundary_state`).
  - ★ **v1 결함 정정**: 정본 인계표의 HOLD 표지가 v1 배포에서 빠졌다 — 130 HOLD 59 (BOUNDARY_CENTER_OUT 41 · NEGATIVE_POROSITY 16 · 둘 다 2) · 64 HOLD 62
    (NEGATIVE 51 · 둘 다 9 · BOUNDARY 2) 가 표지 없이 나갔고 README 에 언급이 없었다 (대조 조사 · 내가 다시 셈).  v1.1 = 표지를 싣고 거르기는 쓰는 쪽에 맡긴다 (권고 (가)).
  - README 정정 (대조 조사 · 내가 다시 확인): 상수 열 (130: `rve_um` · `pressure_MPa` · `e_se_gpa` · `loading_mAh_cm2` / 64: + `se_rich` · `n_large_components` ·
    `ionic_dead_pct`) 을 특징 후보로 적었던 것 · "생성기가 전부 1e-9 로 검사" 과장 (`coverage_AM_total` 가중평균은 관문 밖) · 옛 291 코퍼스와 섞지 말 것 (`DESC-08`) ·
    두 두께 (질량 보존 / 벽 간격 = 130 1.015–1.114 · 64 1.074–1.153).
  - **배포 = 인계표 열 부분집합** 도구 `scripts/lhs_release_build.py` (만들 때 대조 내장 · 시험 8/8 · v1 을 바이트 그대로 재현) — "배포를 만든 도구가 리포에 없다" (`HND-04` 조사) 정정.
- **퍼콜 감사 반입** `docs/data/lhs_perc_audit_20261001/` (네 묶음 · README) — 130 · 64 모두 `d1ec42fba` CLEAN · 130 은 09-29 판과 공통 열 차이 0 · lhsx 동률 = 옛 FLAG 다섯 건 그대로.
- ✅ 원장 갱신 (다음 커밋 · `c981d77f0` 기준): DESC/HND 14 건 대조 반영 (claimed_fixed · 범위 표기 · 웹앱 잔여 `DESC-02W` · `DESC-04W` 신설) · `REL-01` (배포 v1 표지 누락 — v1.1 정정) · `SELF-75` claimed_fixed.
- ⬜ **Codex 최종 리뷰** — 요청서 `docs/reviews/codex_lhs_release_final_request_20261001.md` (대조 원문 `…_reconcile_20261001.md`) · 발송 = 1저자 · 통과하면 같은 코드로 ps45 (사양 5 조성) 를 돌린다 (1저자 10-01 밤).
  웹앱: 이 묶음은 계산 · 정의를 바꾸지 않는다 (열 사전 문구와 배포 묶음만) — 해당 화면 없음 (J20-l 보고).

## J20-r. Codex 최종 리뷰 반입 · README = ML 인계본 (10-01 · 1저자 *"보내도 된데 · README 만으로 머신러닝 적용할 수 있게"*)

- 판정 (`docs/reviews/codex_lhs_release_final_verdict_20261001.md` · 증거 `docs/reviews/codex_lhs_release_final_evidence_20261001/` · 묶음 sha256 `b89f50be…`):
  **고정 v1.1 DEM 계산값 전달 GO · 실제 전극 물리 타깃 인증 HOLD 유지** · 새 P1 없음 · P2 다섯 · P3 하나 (원장 `LREL-01`~`06` — 판정문 표기 LHSREL-0x · ID 형식 5 자 제한).
  Codex 재생성 인계표 = 커밋본과 **바이트 동일** (130 `4df9c1f5…` · 64 `769cb269…`) · 194 행 전수 대조 · 항등식 산술 · 적격성 재계산 일치.
- 원장 (판정문 §6 그대로): verified = DESC-01 · 02 · 05 · 09 · HND-01 · 02 · 04 · 05 · 06 · REL-01 (각 범위 표기) · 부분 = DESC-04 · 07 (claimed_fixed 유지 + 메모) · open 유지 = DESC-03 · 06 (최종 join raw SHA 변이 잔여 추가) · 08 · HND-03.
- README 개정 (CSV · 열 사전 바이트 그대로 — Codex 승인 sha 유지): 외부 검토 절 · 인계 문단 (§8) · 열 역할표 (두 CSV 전 열 · 빠진 열 0) · 항등식 재검산 (최대 오차 1.5e-11) ·
  HOLD 문안 (§4) · H_mc/φ_mc = 등가 장부량 (§5) · τ 분모 = 쌍 z 간격 · 이온 고립 = 경계 띠 그래프 지표 (`LREL-05`) · 질량 % 분모 · 상수 분리 · MC 오차 · 15:1 = 경험적 주의 (`LREL-06`) · ML 적용 안내 (판정문 §7).
- 용어 (1저자 10-01): `tortuosity_SE_wall` = **Tortuosity (기하학적)** · `coverage_*_hertz_pct` = **Coverage (DEM)** — 열 이름은 그대로 · 덱 v3 도 같은 용어.
- 다음: `LREL-05` · `06` claimed_fixed (이 커밋 sha) · 관문 보강 (`LREL-01`~`04` — 반례 먼저) · 열 사전 문구 (다음 생성).


## J20-s. ③ 마감 · ④–⑦ 1차 감사 — 코드 정의 + real_14 실측 (10-04 서브 세션 · 1저자 *"권고에 맞게 진행 · 순서 꼬이지 않게 너가 잘 컨트롤해"* · ⬜ 비준 대기)

- 배경: 망 배치 (τ · 협착 분율) 는 이 감사 → 수정 → 리뷰 → 봉인 **뒤** (1저자 10-04 *"아직 network 까지 갈 수 없는 거 아니야"*).  ⑤ · ⑥ · ⑦ · ④b 는
  **접촉 단계** 열이라 10-01 재실행 (`docs/data/lhs_webapp_contact_d1ec42fba/` · 130) 에 값이 이미 있다 · ④a (`bulk_resistance_fraction`) 만 망 단계.
- 검사기 `scripts/lhs_stress_constriction_audit.py` (읽기 전용 · selftest 9/9 — 크기 다른 두 구 손풀이 · 같은 크기 사슬 · 주기 최소영상 · 웹앱 상 비 · L2-08 반례 ·
  다중 프레임 거부) · 실측 = real_14 기준 상태 (리포 덤프 `docs/data/real14_reference_20260928/`) · 결과 `docs/data/lhs_audit_bundle4_20261004/real14_audit.json`
  (리포만으로 재현 — 같은 값 · LHS 침대가 아니라 같은 물리 · 같은 덤프 형식의 침대 한 건 = **크기 확인용**).

| 묶음 | 열 | 코드 | 판정 | 핵심 |
|---|---|---|---|---|
| ③ φ_SE | `phi_se_mass_conserving` · `phi_am_mass_conserving` · `thickness_mass_conserving_um` · `porosity_union_exact_pct` · `_se_pct` | 웹앱 ③ (10-01) ↔ 수확기 | ✅ **마감** | 웹앱 (d1ec42fba · MC n 4,000,000 · 케이스별 seed) ↔ 인계표 (수확기) 130/130 — union Δ 중앙 0.015 · p90 0.035 · 최대 0.075 %p · φ_SE ≤ 1.7e-4 · φ_AM ≤ 6.7e-4 · L_mc ≤ 0.031 µm = **두 MC 독립 추출의 잡음** (SE √2 × 0.015 %p) · 정본은 인계표 (수확기 열 · J20-e) 그대로 |
| ④a 협착 분율 | `bulk_resistance_fraction` (+ `_physics`) | `network_conductivity.py` `run_decomposition` (`bulk_frac` · L2-08 주석) | ⚠ **이름 · 정의** | 간선마다 R_bulk/(R_bulk+R_c) 의 **비가중 평균** (전류 없는 간선 · 비관통 덩어리 포함) — 거시 전력 몫이 아니다 (`L2-08` = 이름표만 고침).  real_14 이온: 보고 1−bf **0.766** ↔ I²R 가중 **0.786** (hertz) · 0.782 ↔ **0.828** (physics) · 열 physics 0.704 ↔ **0.544** — 잘 관통된 침대에서도 2–16 %p, 문턱 근처 침대는 미측정.  웹앱 주석 *"σ_ionic moves while σ_bulk stays fixed"* (app.py:2672) = 이유 틀림 (모드에 따라 **접촉 면적 → R_c** 가 바뀐다) |
| ④b σ_VM | `stress_cv` · `stress_ratio_{AM_P,AM_S,SE}` (+ `stress_z_layer_cv`) | `dem_analysis_core.calc_von_mises_stress` ← `analyze_contacts.load_atoms_raw` (`c_strs` ÷ 4/3πr³) | ⛔ **규약 결함** (원장 `LHS-29`) | LIGGGHTS `stress/atom` 의 입자 접촉 몫 = **0.5 · (x_i − x_j) ⊗ F** 를 두 입자에 똑같이 (공개 소스 `pair_gran_base.h` `ev_tally_xyz(…, delta)` · `pair.cpp` `Pair::ev_tally_xyz` 의 0.5) — 재현 중앙 비 **1.000000** · 크기가 다른 쌍에서 큰 입자 응력 과소 · 작은 입자 과대 (손풀이: r 6 : 1 에서 0.575 배 · 7.21 배).  real_14: `stress_ratio_AM_P` **0.884** (웹앱) ↔ **3.217** (Love–Weber · 입자 중심 → 접촉점) — **대소가 뒤집힌다** · AM_S 1.085 ↔ 2.343 · SE 0.999 ↔ 0.980 · `stress_cv` **213 → 133 %**.  벽 · 판 접촉은 virial 0 (`fix wall/gran` 에 virial 없음 · 바닥에 닿은 입자 AM_P 7 · AM_S 52 · SE 2237) · 대각 성분만 (덤프 `c_strs[1–3]`).  소비자 = 웹앱 케이스 표 σ_*/σ_mean 행 · 그룹 비교 · **등급 축 "기계적 안정성" (`grade_engine.py` stress_cv)** · 탐색 적합 (v35 · screening — 생산 폼 아님) |
| ⑤ F1 | `se_se_cn_aug` · `_std` · `_n_extra` · `_h_spread_sim` | `calc_se_se_cn` F1 (`dem_analysis_core.py` · LHS-22 주기 수정 뒤) | ✅ **조건부** | 탄성 CN + 표면 틈 ≤ h 인 SE–SE 쌍 · h = 10 nm 물리 (`H_SPREAD_REAL_M` · 확대 배율 반영 = DESC-03 의 혼용 없음) — **10 nm 는 출처 없는 모델 상수** ("2 × h_film_min") → 감도 기술자 한정어 · SE–SE 만 · 반올림 쌍 (접촉 감사 v2 의 114 쌍 / 130 침대) 이 탄성 CN 과 겹쳐 셀 수 있음 (무시 가능 수준) |
| ⑥ Auerbach | `fracture_index_force` · `frac_<단계>_force_pct` (+ `n_*`) | `calc_fracture_stages` · `fracture_model.fracture_classify_force_sim` | ✅ **조건부** (원장 `LHS-31`) | AM–AM 만 · F/P_c (P_c = A K_IC² R_min / E*) 의 배수 1 · 3 · 11 · 32 로 단계.  힘 환산 F/scale 은 덱 E/1000 과 정합.  한정: ① **마지막 프레임 힘** (압축 중 최대 아님 → 손상 **하한**) ② 벽 · 판 접촉 제외 (판에 닿은 AM_P 의 최대 하중 빠짐) ③ R_min 선택 (R* 이면 P_c 절반) ④ **K_IC_P 0.3 = 소결 펠릿값** (정본 카드 `xu2017` — 이차입자 0.102 의 3 배) · K_IC_S 1.0 측정 근거 없음 (카드 판정 ⚠) — P_c ∝ K_IC² 라 이차입자값이면 P_c 1/8.6 ⑤ A 200 · 배수 원전 (Lawn Table 3.4) 카드 없음 [미확인] ⑥ δ 판과 나란히 인용 금지 (09-19 그대로) |
| ⑦ A_dem_geometric | `area_<쌍>_mean` · `_total` · `_n` · `se_se_cn_eff_area` (`_perc`) | `analyze_contacts` · `calc_se_se_cn` · `c_cpl[22]` | ✅ **조건부** | `c_cpl[22]` = 두 구 **교차원 넓이의 정확식** (공개 소스 `compute_pair_gran_local.cpp:558` — 반지름이 달라도 정확) · 작은 δ 에서 Hertz πR*δ 의 ≈ 2 배 (이름 주의 그대로 · L1-04) · `_total` · `_n` = 총량 (입자당 · 부피당으로 나눠 쓰기) · coverage 는 J20-m 으로 이미 인계 · ⛔ `path_hop_area_*` = 덩어리마다 고른 경로 30 개 (best · mean · worst 10) 의 평균 = **선별 표본 통계** → 인계 제외 (원장 `LHS-32`) |

- 비준 대기 (권고):
  - **④a**: 옛 열은 이름표 *"접촉별 R_bulk/R_total 비가중 평균 (전력 몫 아님 · L2-08)"* + 새 열 **`constriction_power_share_ion_hertz`** (같은 FULL 해의 Σ I²R_c / Σ I²R_total · 관통 간선 · 가상 전극 제외) 를 망 단계에서 같이 계산 · hertz 먼저 (v2 결정 3) · 봉인 모듈 수정 = S3 재봉인과 같은 묶음 · 웹앱 주석 정정 (`LHS-30`).
  - **④b**: (가) **접촉 덤프로 Love–Weber 입자 응력**을 새로 계산 (전 텐서 — 대각만 아님 · 벽 접촉 입자 표지 열) → 새 열 `stress_cv_lw` · `stress_ratio_<상>_lw` · 옛 열은 *"LIGGGHTS stress/atom 50/50 분할"* 이름표로 남김 · 웹앱 표 · 그룹 비교 같은 묶음 · **등급 축 전환은 바뀌는 등급값 보고 뒤** (②b TAU-03 과 같은 절차).  (나) 인계 제외만.  → **(가) 권고** — 접촉 단계라 재실행이 싸다 (건당 16–37 s).
  - **⑤ · ⑥ · ⑦**: 위 한정어로 인계 (열 사전 문구 · 생성기 묶음 추가 · 새 계산 없음 — d1ec42fba 값) · `path_hop_area_*` 제외.
  - **순서**: ④a · ④b 수정 (시험 먼저 · 웹앱 같은 묶음) → Codex **한 번** (④ 수정 + 망 경로 + `stop_after='network'`) → 접촉 단계 재실행 (④b 새 열) + 망 배치 (④a · τ) — 설계만 보내고 다시 고치는 왕복을 줄인다 (coverage 는 5 회 왕복).


## 인계 판정 (지금)

**↪ 갱신 09-28 밤 (J20-a)** — ⏸ **일괄 실행 보류**: ✅ 열을 묶음별로 코드 정의부터 감사한 뒤 실행 (① 접촉 위상 1차 감사 = J20-a).
**↪ 갱신 09-28 (J20)** — 1저자 비준 "채운 뒤 넘김": WSL 전 건 실행 → 인계표 재생성 (✅ 열 · 벽 τ · 열 사전) → README 와 함께 **배포**.
아래 "보류 유지" 는 J20 이전 (J9 · J2 · J3 시점) 서술이다 — 그 사유들은 J12–J19 로 닫혔다.

**보류 유지.**  사유 = J9 (97 건의 플래튼이 이른 시점) · J2 (분모 바닥 10 µm) · J3 (두께 측정값 부재).  J5 는 J9 로 대부분 설명됨.
다음 = ✅ 97 건 메시 재반입 (J12) → ✅ 수확기 수정 (J13) → ⛔ 재수확 72/130 (J14 — 가드 과잉 거부) → ✅ J14 비준 · 가드 교체
(덱 확인 + 벽 밖 기록) → ✅ 130 재수확 (J16) → ✅ Codex 판정 (J18, HND-01~06) → 비준 → 수확기 A · 생성기 B · τ 진단 C →
인계표 재생성 (명목 규약값 + 적격성 열 · 이탈 43 · 음수 18 HOLD) → lhsx 64 수확.
순서: J2 수정 → 인계표 재생성 → J3 (a) → 재수확 band 진단 (J3 (b) · J5) → J6 취급 비준 → 인계.
