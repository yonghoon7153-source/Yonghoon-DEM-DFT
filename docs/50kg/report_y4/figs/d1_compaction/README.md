# 50kg D1 (SE D50 1 µm) 압밀 곡선 — ps73 그림의 D1 판 (2026-11-02)

- **무엇**: 1저자 11-02 *"이 그림도 50Kg_D1 기준으로 만들면 좋을듯"* — ps73 발표 그림 (왼쪽 = 시간 축을 같이 쓰는 세 패널 두께 · 판 속도 · 압력 ·
  오른쪽 = 기공 3D 네 단계) 을 D1 침대 `kg50_d1_b50` (단분산 AM D6 · AM:SE = 85:15 wt% · SE D50 1 µm · 50 × 50 µm · 6.5 mAh/cm²) 로 만든다.
  왼쪽 열 = 이 폴더의 그림 · CSV · .ogs · 오른쪽 3D = 1저자가 웹앱에서 그린다 (이 폴더는 프레임 목록과 클러스터 명령만 · §3).
- **다시 만들기**: `python3 -I docs/50kg/report_y4/figs/d1_compaction/make_fig_d1_ms.py` (결정적 — 두 번 돌려 산출 10 개 sha256 같음) ·
  시험 `… --selftest` (합성 로그 48/48).
- **본보기**: `docs/data/ps73_compaction_curve_20261006/` (README §5 · §7 · §8 · `make_fig_ms.py` · `make_fig_velocity_ms.py` · `atom_top_scan.py`) ·
  단계 고르기 = `docs/data/ps73_compaction_curve_20261006/stages_20261012/README.md` §6.  로그 읽기 = ps73 생성기와 같은 `scripts/compaction_curve.py`
  (thermo 블록 · run 마다 첫 줄 = 설정 줄 버림 · 단계 표지 · 판정 줄).
- **입력 (리포 · 읽기만)**: 본 런 로그 `docs/data/kg50_d1_end_20261031/kg50_d1_b50_log.liggghts` (sha256 `6a90f706…` = 그 폴더 README §1) ·
  리포 덱 `docs/data/kg50_decks_20261027_v3_b50/kg50_d1_b50/input_kg50_d1_b50.liggghts` (`514afdb7…` · 로그 안 덱과 설정 14 개 같음) ·
  끝 판 높이 기록 (mesh_end 122.596 µm · 그 README §2 · `docs/50kg/report_y4/draft2/data/D1/metrics_D1.json`) ·
  초안 2 압밀 곡선 `docs/50kg/report_y4/draft2/data/D1/curve_D1.csv` (대조 · 단계 표 ε_sphere 참고값).  dt · 판 속도 · 단위는 **로그 안 덱 글에서** 읽는다 (ps73 값을 쓰지 않는다).

## 1. 파일

| 파일 | 무엇 |
|---|---|
| `make_fig_d1_ms.py` | 생성기 (`--selftest` = 합성 로그 시험 48 · §6) |
| `origin/d1_ms_thickness_plate.csv` · `.ogs` | A Time (ms) · B Thickness (µm) · C Source — 판 위치 521 점 (메시 덤프 자리 5,000 step 마다 517 + 단계 모서리 4) |
| `origin/d1_ms_plate_velocity.csv` · `.ogs` | A Time (ms) · B Plate velocity (µm/s) · C Source — 계단 7 점 |
| `origin/d1_ms_pressure.csv` · `.ogs` | A Time (ms) · B Measured pressure (MPa) · C Source — 3,045 점 (0 ms 판 없음 0 MPa 하나 + thermo 원값 3,044) |
| `previews/d1_ms_compaction_3panel.png` · `.svg` | 세 패널 왼쪽 열 미리보기 (ps73 서식 · 300 dpi · 4.3 × 7.2 in) |
| `key_numbers_d1_ms.json` | 덱 설정 · 단계 경계 (step · ms) · 판 높이 · 잔차 · 압력 문턱 · 원자 수 · 대조 · 단계 프레임 · 클러스터 명령 · 정착 구간에 필요한 것 |
| `stage_frames_d1.csv` | 오른쪽 3D 네 단계 → 가까운 atom 덤프 (§3) |

- Origin: CSV 끌어 놓기 (Long Name = 1 줄 · Units = 2 줄 · 자료 3 줄부터) → 워크북을 앞에 두고 같은 이름 `.ogs` 를 Script Window 에 붙여 넣기 → BML 서식 (10 × 8 cm · Aptos 28 pt) ·
  단계 경계 점선 셋 (200.002 · 400.002 · 2685.002 ms) · x 눈금 500 ms · 색 = 두께 보라 · 판 속도 파랑 · 압력 빨강 · 목표 300 MPa 점선 없음 (1저자 슬라이드 서식 11-02).
  세 그래프를 세로로 쌓는 것 · 가로 단계 이름 · 빨간 화살표 = GUI (미리보기 배치 참고).
- 미리보기 글꼴 = Liberation Sans (이 기계에 Aptos 없음) — Origin 결과로 바꿔 끼운다.

## 2. 수치 (`key_numbers_d1_ms.json`)

| 항목 | 값 |
|---|---|
| 시간 축 | dt = 1e-6 s (로그 `variable dt equal 1.0e-6` = `timestep 1e-06`) ⇒ **1 step = 0.001 ms** · t = 0 = 삽입 전용 런 (NP 1) 의 step 0 (덱: 삽입 `run 1` → step 1) — 이 로그는 20,001 부터 (`read_restart restart_settling_20001.bin`) |
| 단위 (덱 머리 `Scale: r×1000, E×0.001, P×0.001` · `units si`) | 덱 1 m = 1000 µm · 압력 MPa = `pressMPa` × 1000 · 면적 0.0025 덱 m² = 상자 0.05 × 0.05 |
| 단계 (step → ms) | Particle packing (PHASE 1 SETTLING) 1 → 200,001 (0 → 200.001 ms) · 판 놓음 + Stabilization 200,002 → 400,002 · **Compression 400,002 → 2,685,002** (457 run × 5,000 step = 2,285,000 step = **2,285 ms**) · Relaxation 2,685,002 → 2,785,002 (100 ms) |
| 판 높이 (두께) | `PLATE HEIGHT` 145.4457 µm (= 정착 끝 맨 위 입자 **중심** 139.4457 + r_AM_P 3 + 여유 3 µm) → 등속 22.85 µm 하강 → 정지 · 끝 **122.595726 µm** (계산) ↔ mesh_end **122.596 µm** (6 유효숫자) ⇒ **잔차 −0.000274 µm** (반올림 반폭 ±0.0005 µm 안) |
| 판 속도 | `press_speed` 0.01 덱 m/s = **10 µm/s** (= 0.01 mm/s · ps73 과 같은 설정) · 400.002 → 2685.002 ms 만 |
| 압력 | 안정화 0 (201 줄 모두) · 처음 0 아님 = 848,000 (848 ms · 0.024 MPa · 판 140.966 µm = 판이 침대에 닿음) · ≥ 0.1 MPa 850,000 · ≥ 1 890,000 · ≥ 10 1,027,000 · **≥ 50 1,239,000 (50.20 MPa)** · ≥ 100 1,472,000 · ≥ 200 2,076,000 · ≥ 300 2,682,000 (thermo — 루프는 5,000 step 마다만 판정) |
| 정지 · 이완 · 끝 | 정지 2,685,002 = **300.58919 MPa** (판정 줄 = thermo) · 이완 첫 출력 2,686,000 199.68 MPa · 최저 2,689,000 111.98 MPa · 끝 2,785,002 **156.15118 MPa** |
| 원자 수 | 168,457 → 이완 2,687,000 168,456 · 2,688,000 168,455 · 2,689,000 168,452 (SE 5 개 소실 · D1 README §2) |

## 3. 오른쪽 3D 단계 → atom 덤프 (`stage_frames_d1.csv`)

클러스터의 atom 덤프 = 압축 시작 뒤 50,000 step 마다 (`dump dmp_atom … 50000` · 첫 장 450,000 · `undump` 없음 → 이완 2,700,000 · 2,750,000 까지) + `atom_end_2785002`.
메시 = 5,000 step 마다 (205,000 →) + `mesh_end_2785002.stl`.  **덱에서 읽은 일정** — 지금 남아 있는지는 미확인 (아래 명령의 `check` · `ls` 가 확인).
판 높이 = 덱 궤적 (§2) · 압력 · 원자 수 = 그 step 의 thermo.

| 단계 | 사건 (step · 압력) | 가장 가까운 덤프 (Δ step · 단계) | 그 덤프의 압력 · 판 높이 · 원자 | ε_sphere (초안 2) | 권고 |
|---|---|---|---|---|---|
| Initial compression | 압축 시작 400,002 · 0 MPa | `atom_450000` (+49,998 · 압축) | 0 MPa · 144.946 µm · 168,457 | 29.65 % | 이것 (판이 침대에 닿기 전 · ps73 "Initial (before plate contact)" 과 같은 꼴) |
| 50 MPa | 처음 ≥ 50 MPa 1,239,000 · 50.20 MPa | `atom_1250000` (+11,000 · 압축) | 53.11 MPa · 136.946 µm · 168,457 | 25.54 % | 이것 — 이름표는 실제 값 **53 MPa** 권고 (ps73 정렬판 "47 MPa") · 반대쪽 `atom_1200000` = 41.29 MPa |
| 300 MPa | 판 정지 2,685,002 · 300.59 MPa | `atom_2700000` (+14,998 · **이완**) | 154.70 MPa · 122.596 µm · 168,452 | 16.83 % | ⚠ 가장 가까운 덤프가 이완 단계 (판 고정 · 압력 155 MPa) — **`atom_2650000` 권고** (−35,002 · 압축 · **294.26 MPa** · 122.946 µm · 17.06 % · ps73 정렬판 "296 MPa (just before stop)" 과 같은 꼴) |
| After relaxation | 끝 2,785,002 · 156.15 MPa | `atom_end_2785002` (Δ 0) | 156.15 MPa · 122.596 µm · 168,452 | 16.83 % | 이것 (끝 묶음에 이미 있음 · sha256 `e55bb3f4…`) |

- **이완 동안 porosity 는 그대로**: 판이 2,685,002 부터 122.596 µm 에 고정 → `atom_2700000` 과 `atom_end` 는 판 높이 · 원자 수 (168,452 — 소실은 2,689,000 까지 끝남) 가 같아 ε_sphere 가 같다 (16.8250 %).
  그래서 "300 MPa" 칸에 `atom_2700000` 을 쓰면 "After relaxation" 과 같은 상자 porosity 를 보인다 (exact union 은 접촉 겹침이 달라 조금 다를 수 있다 — ps73: 3,125,000 16.53 % ↔ 이완 끝 16.49 %).
- ε_sphere 열 = 초안 2 `curve_D1.csv` 값 (구 부피 = 끝 덤프 168,452 개 기준 → 압축 중 프레임 (168,457 · SE 5 개 = 2.618 µm³ 더) 은 초안 2 값이 +0.0007–0.0009 %p 높다 · 표시 자리 아래) —
  **exact union 이 아니다** (웹앱이 자기 규칙으로 빈 칸을 센다 · 1저자 ps73 결정 = exact union).
- 정지 순간 덤프는 없다 (D1 README §3 · `K50Y4-01`).  체크포인트 `restart_compress_<200,000 배수>` · `restart_settling_400000` 에서 `run 0` 으로 정확한 step 을 뽑는 길도 있다 (ps73 정렬판 방식 · 이번에는 안 함).
- 웹앱 3D 기공 = 덤프 + **같은 step 메시** 를 함께 올린다 (atoms-only 케이스 · 메시가 있어야 영역 윗면 = 판 · `docs/data/ps73_compaction_curve_20261006/stages_20261012/README.md` §6-1).

**클러스터 명령** (D1 런 폴더 = 리포 기록상 `~/simulation/kg50_d1_b50` — `docs/data/kg50_decks_20261027_v3_b50/README.md` §3 · 다른 자리면 `cd` 줄만 고친다 —
첫 검사 (끝 묶음 sha256 둘) 가 맞지 않으면 아무것도 묶지 않고 멈춘다 · 런 폴더는 읽기만 · 결과는 홈 폴더 · 묶기 전 크기 ≈ 110 MB (atom 덤프 ≈ 22.5 MB × 5 · 추정)):

```bash
bash -s <<'EOF'
set -euo pipefail
cd "$HOME/simulation"   # D1 런 폴더 = $HOME/simulation/kg50_d1_b50 (리포 기록: docs/data/kg50_decks_20261027_v3_b50/README.md §3)
printf "%s  %s\n" e55bb3f44c138cf824837f9dd17775eaea5cc1148b28a8c1d4c07c57a3aec635 kg50_d1_b50/post_kg50_d1_b50/atom_end_2785002.liggghts ec99971a2e7f27e1baeedbdab72e6f3c2db52239cc318671142931d56592fe16 kg50_d1_b50/post_kg50_d1_b50/mesh_end_2785002.stl | sha256sum -c -   # 같은 런 (끝 묶음 기록)
check() { t=$(sed -n 2p "$1"); n=$(sed -n 4p "$1"); [ "$t" = "$2" ] && [ "$n" = "$3" ] || { echo "STOP $1: TIMESTEP $t atoms $n (expected $2 $3)"; exit 1; }; }
check kg50_d1_b50/post_kg50_d1_b50/atom_450000.liggghts 450000 168457
check kg50_d1_b50/post_kg50_d1_b50/atom_1250000.liggghts 1250000 168457
check kg50_d1_b50/post_kg50_d1_b50/atom_2650000.liggghts 2650000 168457
check kg50_d1_b50/post_kg50_d1_b50/atom_2700000.liggghts 2700000 168452
check kg50_d1_b50/post_kg50_d1_b50/atom_end_2785002.liggghts 2785002 168452
F="kg50_d1_b50/post_kg50_d1_b50/atom_450000.liggghts kg50_d1_b50/post_kg50_d1_b50/mesh_450000.stl kg50_d1_b50/post_kg50_d1_b50/atom_1250000.liggghts kg50_d1_b50/post_kg50_d1_b50/mesh_1250000.stl kg50_d1_b50/post_kg50_d1_b50/atom_2650000.liggghts kg50_d1_b50/post_kg50_d1_b50/mesh_2650000.stl kg50_d1_b50/post_kg50_d1_b50/atom_2700000.liggghts kg50_d1_b50/post_kg50_d1_b50/mesh_2700000.stl kg50_d1_b50/post_kg50_d1_b50/atom_end_2785002.liggghts kg50_d1_b50/post_kg50_d1_b50/mesh_end_2785002.stl"
ls -l $F
sha256sum $F > "$HOME/kg50_d1_stage_frames_20261102.sha256"
tar czf "$HOME/kg50_d1_stage_frames_20261102.tgz" $F
sha256sum "$HOME/kg50_d1_stage_frames_20261102.tgz" "$HOME/kg50_d1_stage_frames_20261102.sha256"
EOF
```

- 묶음 = 권고 넷 (450,000 · 1,250,000 · 2,650,000 · 끝) + 판 정지에 가장 가까운 2,700,000 (이완 · 비교용) — atom · 메시 짝 다섯.  가져오기 = 평소 방법 (주소 · 포트는 리포에 적지 않는다).
- 같은 명령 글 = `key_numbers_d1_ms.json` `cluster_tar.command` (생성기가 단계 표에서 만든다 · 원자 수 = 그 step 의 thermo).

## 4. Particle packing (정착) 구간 — 그리지 않은 이유 · 클러스터에서 필요한 것

- **이유**: 정착 (PHASE 1) 에는 판이 없다 (정착 뒤 Z_MAX 로 판을 만든다) ⇒ 이 구간의 두께 = 침대 맨 위 = 원자 위치가 필요하다.  덱은 atom 덤프를 PHASE 3 부터만 쓰고
  (`dump dmp_atom` 이 PHASE 3 표지에서 정의됨) 삽입 직후 체크포인트도 없다 (덱 머리 ⑬).  로그에는 정착 중 운동에너지 열과 정착 끝 `Z_MAX (center)` 139.4457 µm 하나뿐인데,
  이것은 **중심** 높이 (윗면 max(z + r) 아님) 이고 판 위치와도 다른 기준이라 그리지 않는다.  ⇒ 그림의 0–200 ms 두께 칸은 비어 있고 "Particle packing" 이름만 둔다 · 그 시작의 빨간 화살표도 안 그렸다 (가리킬 자료 없음).
- **ps73 은 어떻게 그렸나** (그 README §7): ① 투입 재현 — 원 덱 처음 → 정착 블록을 원 런과 같은 코어 수 (2) 로 다시 돌려 1 · 1,000 step 원자 덤프 (1,000 step KE = 원 로그) ·
  ② 체크포인트 `run 0` — `restart_settling_<50,000 … 400,000>` · `restart_after_settling` (200,001) 을 열어 원자만 덤프 (setup KE · 원자 수 = 원 로그) ·
  ③ 원 atom 덤프 (5,000 step 마다 565 장 · `atom_top_scan.py` 로 클러스터에서 훑기) → **모든 원자의 max(z + r)** · 100 ms 튀어 오른 입자 하나 점은 뺌 ·
  0–405 ms 측정점 사이 = PCHIP 곡선 채움 (측정 아님 · Source 열) · 보고용 단조 포락선판 따로.
- **D1 에 필요한 것** (D1 런 폴더 · 이름 = 덱의 `restart 50000 restart_kg50_d1_b50/restart_settling_*.bin` · 존재는 미확인):

| 무엇 | 파일 · 방법 | 맞춰 볼 로그 값 (step · 원자 · KE) |
|---|---|---|
| 정착 체크포인트 → `run 0` + atom 덤프 (`id type x y z radius`) | `restart_kg50_d1_b50/restart_settling_20001.bin` (삽입 런이 씀) · `restart_settling_50000.bin` · `_100000` · `_150000` · `_200000` · `restart_after_settling.bin` | 20,001 · 168,457 · 2.3894425 / 50,000 · 3.2480619 / 100,000 · 0.0073460391 / 150,000 · 0.00081993853 / 200,000 · 1.9866698e-05 / 200,001 · 1.9881675e-05 |
| 0 ms 점 · 낙하 (1 → 20,001 step) | 삽입 전용 덱 `input_kg50_d1_b50_insert.liggghts` 를 **NP 1** (원 삽입 런과 같음) 로 다시 + atom 덤프 (예: 1 · 1,000 · … · 20,001) | 삽입 세 줄 (INSERTED · AM · SE) · KE = `log_kg50_d1_b50_ins.out` (끝 묶음 안 · 리포 밖) · 비용 ≈ 2 시간 (추정 — D0.7-40 삽입 런 실측 4 h 40 m (`docs/data/kg50_decks_20261027_v3_b50/README.md` §2) 를 원자 수 · step 수로 비례) |
| (그림 전체를 원자 기준으로 바꿀 때) 안정화 체크포인트 | `restart_settling_250000` · `_300000` · `_350000` · `_400000` (`restart 50000` 이 PHASE 3 의 `restart 200000 …restart_compress_*` 전까지 살아 있어 이 이름일 것 · 미확인) | 4.4168899e-07 · 3.8465837e-07 · 3.4737142e-07 · 3.1955678e-07 |
| (같은 경우) 압축 · 이완 원자 기준 두께 | atom 덤프 47 장 (`atom_450000` … `atom_2750000`) + `atom_end` → 클러스터에서 ps73 `atom_top_scan.py` 꼴로 훑어 CSV 만 받는다 (덤프 ≈ 1.1 GB 는 두고) | 덤프 머리 TIMESTEP · 원자 수 = thermo |

- ⚠ **하나의 기준**: 정착 구간을 원자 기준으로 넣으면 그림 전체 두께를 원자 기준으로 바꿔야 한다 (1저자 10-08 *"하나의 기준으로 해야지"* — 판 기준 · 원자 기준을 한 그림에 섞지 않는다).
  그때 압축 구간은 50,000 step 간격 (ps73 은 5,000) 이라 점이 성기다 · 판이 닿기 (848 ms) 전에는 원자 기준 두께가 거의 평평할 것으로 본다 (ps73 관찰 · D1 은 미확인).

## 5. 한정어 (그림 · 캡션에 같이)

- x = **step × dt (축척 덱 시간)** — 실제 압착 시간이 아니다 (ps73 README §5).  축 이름은 1저자 슬라이드대로 `Time (ms)` (ps73 미리보기는 한정어를 축 이름에 둔 `Simulation time (ms)`) → 캡션에 한정어.
- 두께 = **판 위치** (바닥 z = 0 → 판) · 덱으로 계산 (메시 덤프는 리포에 없다) — 끝에서 mesh_end 와 대조 (잔차 −0.27 nm) · 초안 2 곡선과 같은 식 (다른 코드) 대조 (§6).
  판이 침대에 닿는 848 ms 전에는 침대가 아니라 판 위치다 (그 사이 판 아래 빈 틈).
- 압력 = 판이 받는 수직 힘 ÷ 면적 (thermo 1,000 step 간격 · run 마다 설정 줄 버림).  정지 뒤 하락 = 판 고정 이완 (목표 미달 아님) · 진동은 기록 그대로 (ps73 의 이완 모식 슬라이드판은 만들지 않았다 — 필요하면 "모식" 표지로 따로).
- ⚠ D1 이완 끝 156 MPa ↔ D2 280 · D3 291 MPa (D1 README §3 · `KG50-20` · `DEMP-01`) — 입도 효과로 읽지 않는다 · "After relaxation" 프레임은 300 MPa 상태가 아니다.
- 판 속도 = 실제 길이 / 시뮬레이션 시간 (ps73 §8) · 0 구간은 x 축선과 겹친다.
- 빨간 화살표 = 이완 구간 (판 고정 · 122.596 µm) 을 아래로 가리키는 하나 · 정착 시작 화살표는 자료가 없어 뺐다 (§4) · 단계 이름 가로 (슬라이드 배치) · 목표 점선 없음.

## 6. 검사

- `--selftest` 48/48 (합성 로그 · 덱 14 · 로그 11 · 판 궤적 · 끝 대조 · 두께 점 8 · 판 속도 1 · 압력 2 · 단계 표 4 · 명령 · CSV 3 · 초안 2 대조 5) —
  그중 반례 (거부해야 하는 입력) 를 담은 시험 34 (덱 12 · 로그 10 · 판 5 · 압력 1 · 단계 1 · 명령 1 · 대조 4: 판정 줄 ≠ thermo · 목표 둘 · 압력 열 없음 · NaN ·
  루프 탈출 규칙 · read_restart step · PHASE 4 표지 · run 길이 · 판 높이 관계 · timestep · 옆으로 움직이는 판 · mesh_end 1 nm 어긋남 · …) — 모두 거부.
  변이 14 (검사를 끄거나 계산을 하나씩 바꾼 사본) = 모두 잡힘 (selftest rc 1).  시험이 생성기 결함 하나를 먼저 잡았다 — 초안 2 대조의 `max(0.0, nan) = 0.0` (NaN 이 조용히 통과) → 줄마다 유한 검사로 고침.
- 실제 로그: sha256 = D1 README · 로그 안 덱 = 리포 덱 (설정 14) · 판정 줄 457 = thermo · 마지막만 ≥ 0.3 · PHASE 4 표지 = 루프 탈출 · run 이 5,000 step 씩 빈틈없음 · step 엄격 증가.
- 초안 2 대조 (`make_fig_p2_aux.branches` 경로): `metrics_D1.json` compaction 11 값 같음 · `curve_D1.csv` 2,843 행 — 판 높이 최대 차 3.1e-8 µm · 압력 최대 차 5.7e-14 MPa.
  (같은 판 궤적 식을 다른 코드로 계산한 대조 — 판 위치의 독립 측정은 mesh_end 한 점뿐이다.)
