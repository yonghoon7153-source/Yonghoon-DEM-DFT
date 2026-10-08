# ps73 압축 중 스냅숏 — step 3,100,000 의 단면 하중 (1저자 WSL 10-08)

**무엇**: 압축 중 마지막 체크포인트 `restart_compress_3100000.bin` (sha256 `82234bea…` · 가지 실험 출발점과 같은 파일) 을 읽고,
**시간을 진행하지 않은 채** (`run 0`) atom · contact 덤프만 쓴 것이다.  같은 침대 (ps45 · PC:SC 7:3 · r45) 의 이완 끝 상태와
단면 하중을 비교하려고 만들었다 — "판 압력 300 MPa" 순간의 침대 안 하중이 고르지 않다는 것을 보이는 증거 (원장 `DEMP-01`).
1저자 요청 10-08 *"300MPa 딱 도달했을때의 그 atom contact 에서의 상황을 보여달래"*.

## 만든 법 (1저자 WSL · `SNAP_DONE`)

1. 가지 실험 t0 덱 (`../in.branch_t0_syntax.liggghts`) 에서 첫 `run 0` 앞까지만 잘라 (`awk '/^run 0/{exit} {print}'`) 접촉 덤프를 붙였다:
   `dump dmp_contact_snap all local 5000 ${out}/snap/contact_*.liggghts` (c_cpl[1]…c_cpl[26]) · `dump_modify dmp_contact_snap first yes` · `run 0` ·
   `print "SNAP_DONE"`.
2. `lmp_serial -in in.snap.liggghts -var ckpt …/restart_compress_3100000.bin -var out $O -var plate_stl $O/plate_branch3100000.stl`
   → 1저자 WSL `~/ps73_snap_3100000/post/atom_3100000.liggghts` (21,416,859 B) · `~/ps73_snap_3100000/post/mesh_3100000.stl` ·
   `~/ps73_snap_3100000/snap/contact_3100000.liggghts` (148,856,647 B · 접촉 559,470) — 리포 밖 (크기 때문에 반입 안 함).
3. 웹앱 파서로 읽기 → `scripts/plane_load_share.py --case <ana> --meta <ana_meta.json> --label snap_3100000 --out <plane>`
   (도구 code sha256 `a1d95cb9…` · 입력 sha256 은 `plane/plane_load.json` 의 `inputs_sha256`).
4. 결과 묶음 = `raw/ps73_snap_3100000_plane.tgz` (sha256 `312a66f3…` · 9,093 B) — `plane/` 다섯 파일은 그 묶음과 바이트가 같다 (반입 때 sha256 대조).

`run 0` 은 입자를 움직이지 않는다 — 접촉 힘은 체크포인트의 위치 · 속도 · 접선 이력에서 다시 계산한 값이다.  전역 감쇠 (`fix damp all viscous`) 는
접촉 힘이 아니라서 덤프에 없다.

## 결과 — 단면 하중 (판 간격 111.30 µm · 창 9.0–102.3 µm · 21 단면 중 다섯)

| 높이 (µm) | 3,100,000 (압축 중 · 판 압력 296.2 MPa) | 이완 끝 (ps45 7:3 · 판 압력 165.3 MPa) |
|---|---|---|
| 102.3 (위) | **268.2** | 165.6 (102.1) |
| 79.0 | 212.4 | 166.4 (78.8) |
| 55.7 (가운데) | 168.9 | 167.1 (55.5) |
| 32.3 | 140.3 | 167.9 (32.3) |
| 9.0 (아래) | **127.2** | 168.7 |
| 단면 최대 ÷ 최소 | **2.108** (보존 검사 `CHECK` — 정적 평형이 아니라서 기대대로) | 1.019 (`OK`) |
| 21 단면 평균 σ_zz | 179.7 MPa | 167.1 MPa |

판 압력 = ps73 압축 곡선 (`../../ps73_compaction_curve_20261006/curve/pressure.csv`) 의 같은 step 값.  이완 끝 열 = `../../ps45_plane_load_20261007/ps45_v2/plane_load.json`
(7:3 · 판 간격 111.05 µm — 판이 3,125,000 에서 멈춰 0.25 µm 더 내려간 뒤) · 괄호 = 그 단면 높이.

**읽기**: 압축 중에는 판이 민 힘이 아래로 갈수록 줄어든다 (위 268 → 아래 127 MPa).  덱의 `fix damp all viscous 0.5` 가 움직이는 입자마다
속도에 비례하는 저항 (F = −γv) 을 걸어, 판 힘의 일부를 층마다 가져가기 때문이다 (`DEMP-01` · ps45 7:3 실측 감쇠 저항 = 판 힘의 57.9 %).
판이 멈추고 감쇠를 내리면 속도가 0 이 되어 하중이 높이마다 같아진다 (≈165 MPa).

## 몫 · α 는 거의 같다 (상대 지표는 이 오염에 둔감)

| | 3,100,000 | 이완 끝 (7:3) |
|---|---|---|
| Contribution to σ_zz — AM–AM · AM–SE · SE–SE (%) | 51.7 · 36.6 · 11.6 | 48.5 · 39.1 · 12.4 |
| α (σ_zz) — AM_P · AM_S · SE · AM | 1.367 · 1.072 · 0.471 · 1.279 | 1.336 · 1.086 · 0.505 · 1.261 |
| LW 창 합 ÷ 21 단면 평균 | 0.997 | 1.0006 |

⇒ 압축 중 스냅숏의 **절대 하중 · 응력** (MPa · µN) 은 쓰지 않는다 (높이마다 2.1 배 차).  몫 · α (비) 는 ±3 %p · ±0.03 안이다.

## 기록 그대로 둔 것

- `n_center_above_plate` = 10 (판 높이 0.111302 위에 중심이 있는 입자 · 이완 끝 7:3 은 11) — 해석하지 않았다.
- 판 STL = `../plate_branch3100000.stl` (덱 변수 `pz_branch` 0.111302 와 같은 높이 · 메쉬 덤프 `mesh_3100000.stl` 기준).

## 정지 구간 판 압력 그림

`ps73_stop_zoom.{png,svg}` — `make_stop_zoom.py <pressure.csv> <출력 폴더>` (값 = 압축 곡선 CSV 그대로).
3,125,000 (판 정지 · 300.95 MPa) → 1,000 step 뒤 204.6 MPa → 이완 끝 165.3 MPa.  시간 = step × 1e-6 s.
