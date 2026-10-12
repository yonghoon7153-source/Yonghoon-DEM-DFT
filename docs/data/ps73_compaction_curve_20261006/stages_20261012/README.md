# ps_7_3_r45 발표 그림 — 네 단계 3D · porosity · SE von Mises (2026-10-12)

- 침대 = 이종기술 6 mAh/cm² P:S 7:3 r4.5 (`dem_scripts/ps_sweep_6mah_20260914/in.ps_7_3_r45.liggghts` · 웹앱 케이스 `260925_000559_082983`).
- 1저자 결정 (10-12): 단계 = Initial compression 405,000 · 50 MPa 1,665,000 · 300 MPa 3,125,000 (압축 끝) · After relaxation 3,225,000 (응력 = 3,220,000 · 접촉 덤프가 있는 마지막 step) ·
  SE 응력 = **Love–Weber** (접촉점 분할 · stress/atom 50/50 아님) · 3D = 그림만 + porosity 그래프 따로 · 시간–속도 = `../README.md` §8.
- 원자료 = ibb `~/dem_test/ps45/ps_7_3_r45` (find 명령 · 묶음 92,192,171 B · sha256 `25b8e849…` · 24 MB 조각 넷 합침) — 리포에 넣지 않음 · 영수증 = 이 폴더 `ps73_files.txt` (파일 6 sha256 · 시각) · `ps73_restart_list.txt` · `ps73_run_dir.txt`.
- 계산 = 리포 코드 import 만 (리포 쓰기 0) · 작업 폴더에서 `python3 -I -B` · 코드 = `code/` (작업 폴더 절대 경로 그대로 — 기록용) · 로그 = `logs/`.

> ★ **최종 판 = `aligned_ckpt/` (1저자 10-12)** — 3D · porosity · SE 응력을 **같은 step** (체크포인트 400,000 · 1,650,000 · 3,100,000 · 이완 3,220,000) 으로 맞췄다.
> **porosity = exact union** (1저자 10-12 *"exact union으로 해야지"* — LHS 배포 열 `porosity_union_exact_pct` 와 같은 양 · sphere-sum 은 기록 (JSON) 만) ·
> porosity **그래프는 덱에 넣지 않는다** (1저자 — *"thickness 있으니까"*) · 값 CSV 만 둔다.  아래 §1–§4 (405,000 · 1,665,000 · 3,125,000 · 3,225,000) = **첫 판 (이력)**.

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
- 압축 세 단계 = 접촉 덤프 없음 → **1저자 10-12: 10-08 AM 그림과 같은 방법** (`../../ps73_damping_branch_20261007/snap_moments_20261008/make_snap_decks.py` · 체크포인트에서 `run 0` · 접촉만 덤프) ·
  체크포인트 = **400,000** (0 MPa · `restart_settling_400000`) · **1,650,000** (47.1 MPa · `restart_settling_1650000` — `restart_compress_1650000` 은 이 파일의 심링크) · **3,100,000** (296.2 MPa · 10-08 스냅숏 그대로) — 3D · porosity 단계 (405,000 · 1,665,000 · 3,125,000) 와 5,000–25,000 step 다르다 (3,125,000 등은 체크포인트 없음) · ⬜ 단계 표기 = 1저자 · 명령 = 대화 (10-12) · ⬜ WSL 실행 → 그림.
- Origin 상자그림 입력 `t3_vm_se/ps73_se_vm_by_class_boxdata_origin.csv.gz` (Origin 에 넣을 때 `gunzip -k`) (네 열 = SE only · PC only · SC only · PC + SC · 벽 아닌 SE · MPa) = `code/t3_box_origin.py` (SE 별 CSV.gz 를 읽기만 · 개수 · 중앙값 = 요약표 검산).

## 3. 3D 기하 (`t1_geometry/`)

- `render3d.py` (웹앱 three.js 카메라 · 조명 · Phong 을 옮긴 z-버퍼) · 색 = 웹앱 `COL` (AM_P #222222 · AM_S #888888 · SE #f5e6a3) · 네 장 같은 카메라 · 같은 자르기 (첫 단계 상자 0–138.252 µm 기준) · 투명 배경 · 글자 없음 · `ps73_geom3d_4panel_preview.png` = 흰 바탕 미리보기.
- 한정어: SE 불투명 (웹앱은 0.85) · 판 안 그림 · 판을 뚫은 SE 11 개 그대로.

## 4. 새로 보인 것 (추정 · 미확인)

- 이완 시작 (3,125,000 → 3,130,000) 에 사라진 원자 3 개 = SE id 43757 · 51248 · 62089 — 3,125,000 에 **바닥 가까이** (중심 z 0.04–0.13 µm) 있었고 판 위 11 개와 다른 입자다 ⇒ `../README.md` §7-1 의 추정 *"판 위 입자가 튕겨 나갔다"* 와 맞지 않는다 (바닥 밑으로 빠진 것으로 보임 · 기전 미확인 · 그 문구는 1저자 판단 전까지 그대로 둔다) · `logs/aux_missing_atoms.json`.

## 5. 파일

`t1_geometry/` (단계별 PNG 4 · 미리보기) · `t2_porosity/` (CSV · Origin CSV · JSON · PNG · SVG) · `t3_vm_se/` (SE 별 CSV.gz 158,761 행 · JSON · 분류 요약 CSV · Origin CSV · 상자그림 입력 Origin CSV · 상자그림 PNG · SVG · 3D PNG 넷 · 범례 둘) · `code/` · `logs/` · `SHA256SUMS`.

## 6. 최종 판 — 같은 step 네 단계 (`aligned_ckpt/` · 10-12)

| 단계 | step | 판 압력 (MPa) | 판 높이 (µm) | **porosity exact union (%)** ± MC 1σ | SE (벽 아님) | SE σ_VM 중앙 (MPa) | 평균 | 중앙: SE 만 · PC 만 · SC 만 · PC + SC |
|---|---|---|---|---|---|---|---|---|
| Initial (before plate contact) | 400,000 | 0 | 138.302 | **31.81 ± 0.02** | 156,980 | 11.6 | 22.6 | 11.2 · 8.9 · 13.6 · 28.9 |
| 47 MPa (compression) | 1,650,000 | 47.1 | 125.802 | **25.09 ± 0.02** | 156,235 | 14.5 | 24.9 | 14.3 · 11.5 · 16.3 · 32.0 |
| 296 MPa (just before stop) | 3,100,000 | 296.2 | 111.302 | **16.68 ± 0.02** | 154,982 | 91.1 | 113.1 | 79.1 · 95.1 · 97.5 · 151.2 |
| After relaxation | 3,220,000 | 165.3 | 111.052 | **16.49 ± 0.02** | 155,033 | 91.7 | 113.1 | 80.2 · 95.4 · 98.6 · 150.5 |

- 입력: 400,000 · 1,650,000 · 3,100,000 = 1저자 WSL 스냅숏 (`../../ps73_damping_branch_20261007/snap_moments_20261008/make_snap_decks.py` · 체크포인트에서 `run 0`) 파서 출력 묶음 (`ps73_snap3.tgz` 165,473,075 B · sha256 `476df90c…` · 리포 밖) · 3,220,000 = 첫 판 T3 와 같은 파서 출력.
- 검사: 1,650,000 = 원 런 atom 덤프와 위치 · 속도 다른 원자 0 / 160,420 (`--verify`) · 400,000 = ibb 에 원 런 덤프가 없어 **원 런 로그 KE 대조** — r1 로그 (`../raw/ps73_logs.tgz` · `output_ps_7_3_r45_181338.out`) `400000 160420 2.8212798e-07` = 스냅숏 setup 줄 (글자 같음) · 1,650,000 KE 3.2731177e-06 도 r3 로그와 같음 · 3,100,000 = 10-08 스냅숏 · 판 높이 = `../curve/plate.csv` (네 단계 같음) · 3,220,000 union 16.4941 = 첫 판 재현.
- porosity = `code/t2b_union_ckpt.py` → `aligned_ckpt/ps73_ckpt_porosity_exact_union_origin.csv` (exact union 만 · Origin) · JSON (sphere-sum 은 기록만).
- 3D = `code/aligned_figs.py` → 첫 판 `t1_render.main` 그대로 (원자만 스냅숏 atoms.csv 에서) · 카메라 = 첫 단계 (400,000) 상자 · `aligned_ckpt/t1_geometry/`.
- SE 응력 = 첫 판 `t3_vm_se.compute` 그대로 (봉인 LW · 단계마다 ANA · step 만 바꿈) · LW 상태 네 단계 OK · **색 범위 = 네 단계 벽 아닌 SE (σ_VM > 0) 를 모은 p5–p95 = 1.17 … 205.5 MPa** (log · jet · 10-08 AM 그림과 같은 규칙) · `aligned_ckpt/t3_vm_se/` (SE 별 CSV.gz · 단계 × 분류 요약 CSV · Origin CSV · 3D 넷 × 두 판 (벽 칠함 · 벽 회색 — 투명 배경) · 공동 범례 · `ps73_se_vm3d_4panel_wallgrey_preview.png`).
- 한정어: MPa 절대값 = DEM (연화 SE) 모델 안 값 · 벽 SE 는 판 · 바닥 힘이 덤프에 없어 값이 불완전 (표 · 색 범위에서 뺌 · 3D 는 회색판 권장) · 단계 이름의 압력 = 판 압력 (입자 응력 평균 아님).
- 관찰 (원인 확인 전): 판이 닿기 **전** (400,000) 에도 SE σ_VM 이 아래로 갈수록 커진다 (중앙 11.6 MPa) — 정착 단계 중력 (덱 단위 · PHASE 1 98.1 → 2–3 9.81) 하중으로 보인다 · 47 MPa 단계 중앙 14.5 MPa 는 그보다 조금 크다.

### 6-1. 1저자 10-12 그림 고침 (`code/aligned_previews.py` · 재계산 없음 — SE 별 CSV.gz · 카메라 · porosity JSON 을 읽는다)

- *"저 회색 없애줘"* → 벽 SE (바닥 · 판에 닿은 SE) 는 **그리지 않는다** (칠하면 판 힘이 덤프에 없어 윗면이 거짓으로 낮게 보인다 · 그 아래 층이 보인다).
- *"log 말고 선형으로 범례"* · *"300 이상 다 같은색으로 한것처럼 잘 차이나는 mpa로"* → **선형 0–200 MPa** (기본 · 200 이상 = 맨 위 색) + 1저자 요청 **0–150 · 0–100** 판 — `ps73_se_vm3d_<step>_<단계>_nowall_linear_0_<상한>.png` (투명 · 글자 없음) · 범례 `ps73_se_vm3d_colorbar_linear_0_<상한>{,_bare}.png` · 미리보기 `…_4panel_nowall_linear_0_<상한>_preview.png`.
  근거: 벽 아닌 SE 분포 — 296 MPa · 이완 단계 p50 91–92 · p75 132–133 · p90 194–197 · p95 261–265 MPa · 처음 · 47 MPa 단계 p90 47–49 MPa.
- *"이건 porosity로 해줘야지"* → 3D 단계 이름 = porosity (exact union) — `t1_geometry/ps73_geom3d_4panel_porosity_preview.png` (글자는 그림 밖 아래).
- *"porosity는 porosity 그림으로 … webapp에서 기공 부분"* · *"3D로 … atom이라도 주던가 webapp에 먹이게"* → 웹앱 3D 보기 "기공 (빈 공간 · 격자 추정)" 으로 1저자가 그린다 — 입력 = WSL 스냅숏 `~/ps73_snap_<S>/post/atom_<S>.liggghts` + `mesh_<S>.stl` (atoms-only 케이스 · 메시를 같이 올려야 영역 윗면 = 판) · 이완 = 웹앱 케이스 `260925_000559_082983`.
  같은 규칙 (viewer3d.js `computeVoidVoxels` · 격자 보통) 으로 컨테이너에서 계산한 빈 칸 비율 = 31.8 · 25.1 · 16.7 · 16.5 % (exact union 과 0.1 %p 안 · 표시용) — 그 시도 (불투명 3D · 단면) 는 리포에 넣지 않았다.

### 6-2. AM 접촉 상대별 3D — 이완 단계 (1저자 10-13 · `code/aligned_class3d.py` · 재계산 없음)

- 1저자 *"저 중앙값 그림이 필요한게 아니고 ~사이에 응력값이던 3d geometry로 해서 각각의 차이를 보고싶은거야"* → 상자그림 (`t3_vm_se/ps73_se_vm_by_class.png` · 기록으로 남긴다) 대신
  이완 단계 (3,220,000) 의 SE 를 **접촉 상대 분류마다 따로** 3D 로 그린다 — None (AM 접촉 없음) · PC (PC 만) · SC (SC 만) · PC + SC (둘 다) · 분류 = SE 별 CSV.gz 의 `class` 열 (상자그림과 같다) ·
  카메라 = 네 단계 그림과 같다 · 벽 SE · AM 은 그리지 않는다 (§6-1 규칙).
- 색 = **선형 0–150 MPa** (1저자 *"150이 제일 좋은듯"* · 150 이상 = 맨 위 색) — `aligned_ckpt/t3_vm_se/ps73_se_vm3d_3220000_relaxed_class_{none,pc,sc,pcsc}_nowall_linear_0_150.png` (투명 · 글자 없음 ·
  1저자에게 네 장 전달 · 범례 없이 — 범례가 필요하면 네 단계 그림과 같은 `ps73_se_vm3d_colorbar_linear_0_150.png`) · 미리보기 `…_3220000_relaxed_class_4panel_nowall_linear_0_150_preview.png` ·
  기록 `…_3220000_relaxed_class_nowall_linear_0_150.json`.  처음 보인 0–200 MPa 판 = 같은 스크립트 `--vmax 200` (리포에는 0–150 만).

| 접촉 상대 (벽 아닌 SE) | 개수 | σ_VM p25 · p50 · p75 · p90 (MPa) | 150 MPa 이상 |
|---|---:|---|---:|
| None | 49694 | 58.1 · 80.2 · 104.1 · 127.2 | 3.0 % |
| PC | 44975 | 60.5 · 95.4 · 146.2 · 211.7 | 23.7 % |
| SC | 46738 | 68.0 · 98.6 · 139.6 · 190.7 | 20.8 % |
| PC + SC | 13626 | 83.6 · 150.5 · 272.1 · 439.5 | 50.1 % |

- 검산: 개수 합 155033 = §6 표의 이완 단계 SE (벽 아님) · 중앙값 넷 = §6 표 (80.2 · 95.4 · 98.6 · 150.5).
- 그림에서 보이는 것 (관찰): None 은 대부분 중간 색 · PC · SC 는 AM 둘레 껍질 모양에 150 이상 (맨 위 색) 이 섞인다 · PC + SC 는 절반이 150 이상.  MPa 절대값 = DEM (연화 SE) 모델 안 값 (§6 한정어).
