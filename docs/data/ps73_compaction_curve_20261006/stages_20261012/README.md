# ps_7_3_r45 발표 그림 — 네 단계 3D · porosity · SE von Mises (2026-10-12)

- 침대 = 이종기술 6 mAh/cm² P:S 7:3 r4.5 (`dem_scripts/ps_sweep_6mah_20260914/in.ps_7_3_r45.liggghts` · 웹앱 케이스 `260925_000559_082983`).
- 1저자 결정 (10-12): 단계 = Initial compression 405,000 · 50 MPa 1,665,000 · 300 MPa 3,125,000 (압축 끝) · After relaxation 3,225,000 (응력 = 3,220,000 · 접촉 덤프가 있는 마지막 step) ·
  SE 응력 = **Love–Weber** (접촉점 분할 · stress/atom 50/50 아님) · 3D = 그림만 + porosity 그래프 따로 · 시간–속도 = `../README.md` §8.
- 원자료 = ibb `~/dem_test/ps45/ps_7_3_r45` (find 명령 · 묶음 92,192,171 B · sha256 `25b8e849…` · 24 MB 조각 넷 합침) — 리포에 넣지 않음 · 영수증 = 이 폴더 `ps73_files.txt` (파일 6 sha256 · 시각) · `ps73_restart_list.txt` · `ps73_run_dir.txt`.
- 계산 = 리포 코드 import 만 (리포 쓰기 0) · 작업 폴더에서 `python3 -I -B` · 코드 = `code/` (작업 폴더 절대 경로 그대로 — 기록용) · 로그 = `logs/`.

## 1. porosity (`t2_porosity/` · H = 그 step 판 높이 · A = 50 × 50 µm)

| 단계 | step | ms | H (µm) | 판 압력 (MPa) | ε_sphere (%) | ε_union (%) ± MC 1σ | 중심이 판 위 |
|---|---|---|---|---|---|---|---|
| Initial compression | 405,000 | 405 | 138.252 | 0.0 | 31.6854 | 31.7833 ± 0.0233 | 0 |
| 50 MPa | 1,665,000 | 1665 | 125.652 | 50.87 | 24.8350 | 24.9817 ± 0.0216 | 0 |
| 300 MPa | 3,125,000 | 3125 | 111.052 | 300.95 | 14.9531 | 16.5312 ± 0.0186 | 11 |
| After relaxation | 3,225,000 | 3225 | 111.052 | 165.34 | 14.9536 | 16.4945 ± 0.0186 | 11 |

- ε_sphere = `dem_analysis_core.calc_porosity` (구 부피 합 · 장부값) · ε_union = `dem_analysis_core.calc_porosity_union_exact` (MC 4e6 점 · 시드 = 케이스 이름 crc32 · `lhs_union_webapp.one` 과 같은 계산).
- **검사**: 3,220,000 에서 union 16.4941 ± 0.0186 · sphere 14.9536 · 두께 111.052 = ps45 요약표 (`docs/data/ps45_r45_union_20260929/r45_union_summary.tsv`) 와 같음 · 판 높이 = `../curve/plate.csv` = 판 메시 STL (비트 같음) · type 1/2/3 = AM_P 4.5 / AM_S 2.0 / SE 0.5 µm.
- 한정어: Initial (405 ms) 은 판이 침대에 닿기 전 — porosity 에 판 아래 빈 틈 6.2 µm 가 들어 있다 · 300 MPa 뒤 SE 11 개 중심이 판 위 (ε_sphere 는 그 부피를 다 세고 ε_union 은 판 아래만) · 시간 = 시뮬레이션 시간.

## 2. SE von Mises — 이완 3,220,000 (`t3_vm_se/` · Love–Weber · 벽 접촉 SE 3,728 개 제외 · MPa)

| SE 가 닿은 AM | n | 평균 | 중앙 | p25 | p75 | p90 |
|---|---|---|---|---|---|---|
| 없음 (SE 만) | 49,694 | 82.2 | 80.2 | 58.1 | 104.1 | 127.2 |
| PC 만 | 44,975 | 121.1 | 95.4 | 60.5 | 146.2 | 211.7 |
| SC 만 | 46,738 | 112.5 | 98.6 | 68.0 | 139.6 | 190.7 |
| PC + SC | 13,626 | 201.1 | 150.5 | 83.6 | 272.1 | 439.5 |
| 전체 SE | 155,033 | 113.1 | 91.7 | 62.8 | 131.7 | 194.2 |

- 계산 = `docs/data/ps73_damping_branch_20261007/snap_moments_20261008/vm_moments.py` `moment()` 그대로 (봉인 `dem_analysis_core.calc_love_weber_stress` · return_arrays · `arrays_vm` 대칭부 VM) · 입력 = 리포 파서 `scripts/parse_liggghts.py` 출력 (atoms · contacts · mesh_info sha256 = 웹앱 케이스 · `ps45_plane_load_20261007` 7:3 과 같음).
- **LW 상태 OK**: force_decomp 3.1e-6 (≤ 1e-3) · branch/r 1.00072 (≤ 1.01) · virial 1.46e-5 (≤ 1e-2) · 접촉 없는 입자 1 · `snap_moments` README §6 (d) 값 재현 (AM 174 (115) · SE 113 · 위÷아래 0.97 · 1.05).
- 분류 = 같은 접촉 목록에서 SE 마다 n_SE · n_PC · n_SC (PC · SC 칸에도 SE 이웃은 있다).  표 · 상자그림 = 벽 아닌 SE 만 · 3D = 벽 SE 도 칠함 (판 힘이 덤프에 없어 윗면이 파랗다 → 벽 회색판 `_wallgrey` 같이 둠).
- 색 범위 (3D) = 벽 아닌 SE p5–p95 = 29.6 … 261 MPa (log · jet · `render3d.py`).
- 한정어: MPa 절대값 = DEM (연화 SE) 모델 안 값 — 분류 · 단계끼리 비교용 · 캡션 권고 *"Love–Weber particle von Mises stress (MPa) from the DEM contact forces (softened SE) — model-internal comparison."*
- 압축 세 단계 (405,000 · 1,665,000 · 3,125,000) = 접촉 덤프 없음 → 재시작 파일에서 짧게 다시 (settling_400000 · settling_1650000 · compress_3100000 — `ps73_restart_list.txt`) · ⬜ 명령.

## 3. 3D 기하 (`t1_geometry/`)

- `render3d.py` (웹앱 three.js 카메라 · 조명 · Phong 을 옮긴 z-버퍼) · 색 = 웹앱 `COL` (AM_P #222222 · AM_S #888888 · SE #f5e6a3) · 네 장 같은 카메라 · 같은 자르기 (첫 단계 상자 0–138.252 µm 기준) · 투명 배경 · 글자 없음 · `ps73_geom3d_4panel_preview.png` = 흰 바탕 미리보기.
- 한정어: SE 불투명 (웹앱은 0.85) · 판 안 그림 · 판을 뚫은 SE 11 개 그대로.

## 4. 새로 보인 것 (추정 · 미확인)

- 이완 시작 (3,125,000 → 3,130,000) 에 사라진 원자 3 개 = SE id 43757 · 51248 · 62089 — 3,125,000 에 **바닥 가까이** (중심 z 0.04–0.13 µm) 있었고 판 위 11 개와 다른 입자다 ⇒ `../README.md` §7-1 의 추정 *"판 위 입자가 튕겨 나갔다"* 와 맞지 않는다 (바닥 밑으로 빠진 것으로 보임 · 기전 미확인 · 그 문구는 1저자 판단 전까지 그대로 둔다) · `logs/aux_missing_atoms.json`.

## 5. 파일

`t1_geometry/` (단계별 PNG 4 · 미리보기) · `t2_porosity/` (CSV · Origin CSV · JSON · PNG · SVG) · `t3_vm_se/` (SE 별 CSV.gz 158,761 행 · JSON · 분류 요약 CSV · Origin CSV · 상자그림 PNG · SVG · 3D PNG 넷 · 범례 둘) · `code/` · `logs/` · `SHA256SUMS`.
