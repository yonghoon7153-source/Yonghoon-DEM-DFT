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

## 인계 판정 (지금)

**↪ 갱신 09-28 밤 (J20-a)** — ⏸ **일괄 실행 보류**: ✅ 열을 묶음별로 코드 정의부터 감사한 뒤 실행 (① 접촉 위상 1차 감사 = J20-a).
**↪ 갱신 09-28 (J20)** — 1저자 비준 "채운 뒤 넘김": WSL 전 건 실행 → 인계표 재생성 (✅ 열 · 벽 τ · 열 사전) → README 와 함께 **배포**.
아래 "보류 유지" 는 J20 이전 (J9 · J2 · J3 시점) 서술이다 — 그 사유들은 J12–J19 로 닫혔다.

**보류 유지.**  사유 = J9 (97 건의 플래튼이 이른 시점) · J2 (분모 바닥 10 µm) · J3 (두께 측정값 부재).  J5 는 J9 로 대부분 설명됨.
다음 = ✅ 97 건 메시 재반입 (J12) → ✅ 수확기 수정 (J13) → ⛔ 재수확 72/130 (J14 — 가드 과잉 거부) → ✅ J14 비준 · 가드 교체
(덱 확인 + 벽 밖 기록) → ✅ 130 재수확 (J16) → ✅ Codex 판정 (J18, HND-01~06) → 비준 → 수확기 A · 생성기 B · τ 진단 C →
인계표 재생성 (명목 규약값 + 적격성 열 · 이탈 43 · 음수 18 HOLD) → lhsx 64 수확.
순서: J2 수정 → 인계표 재생성 → J3 (a) → 재수확 band 진단 (J3 (b) · J5) → J6 취급 비준 → 인계.
