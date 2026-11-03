# 50kg D1 (SE D50 1 µm) 압밀 곡선 — ps73 그림의 D1 판 (2026-11-02)

- **무엇**: 1저자 11-02 *"이 그림도 50Kg_D1 기준으로 만들면 좋을듯"* — ps73 발표 그림 (왼쪽 = 시간 축을 같이 쓰는 세 패널 두께 · 판 속도 · 압력 ·
  오른쪽 = 기공 3D 네 단계) 을 D1 침대 `kg50_d1_b50` (단분산 AM D6 · AM:SE = 85:15 wt% · SE D50 1 µm · 50 × 50 µm · 6.5 mAh/cm²) 로 만든다.
  왼쪽 열 = 이 폴더의 그림 · CSV · .ogs · 오른쪽 3D = 1저자가 웹앱에서 그린다 (이 폴더는 프레임 목록과 클러스터 명령만 · §3).
- **1저자 11-02 밤 (ps73 옛 그림과 대조)**: ① *"첫번째부터 예전처럼 particle packing 도 넣어야지"* — 정착 구간을 0 ms 부터 (투입 높이에서 내려오는 두께 · 시작 빨간 화살표 · 끊긴 y 축) ·
  ② *"관련해서 이어지게 다시 만들고 origin 으로도 맞게"* — 한 곡선 (원자 기준 하나) · Origin CSV · .ogs · ③ *"pressure 도 저 진동 안 생기게"* — 압력 슬라이드판 (ps73 README §5 선례) ·
  ⇒ ③ = 바로 만들었다 (§7) · ①② = D1 런 기계에서 원자 위치를 훑어야 한다 → 스크립트 · 명령 = §8 (CSV 가 오면 같은 생성기가 그린다 · 그 전에는 정착 구간을 그리지 않는다).
- **다시 만들기**: `python3 -I docs/50kg/report_y4/figs/d1_compaction/make_fig_d1_ms.py` (결정적 — 두 번 돌려 산출 14 개 sha256 같음) ·
  원자 기준 그림 = 같은 명령 + `--atomtop` (raw 폴더에 `kg50_d1_atomtop.csv` 가 있어야 한다 — 없으면 멈춘다) · 시험 `… --selftest` (90/90) ·
  클러스터 스크립트 시험 `python3 -I docs/50kg/report_y4/figs/d1_compaction/cluster/d1_atomtop_cluster.py --selftest` (9/9).
- **틀 (1저자 11-03 *"우측, 위측 테두리는 없애줘 그게 우리 표준이야"*)**: 그림 (PNG · SVG) 과 Origin `.ogs` 모두 위 · 오른쪽 축선 없음 · 끊긴 축 표시 = 왼쪽만 (`OPEN_FRAME` 기본 · `--closed-frame` = 옛 네 변) ·
  지금 커밋된 산출 = `--b3-contact --hi-span 45 --hi-frac 0.35` (원값판 · 원자 기준판 둘 다) · 덱 6장 판 = 같은 인자 + `--atomtop --figsize 3.5 3.85` · ⚠ `.ogs` 의 열린 틀 줄 (`layer.x2.showAxes = 0` 등) 은 Origin 에서 아직 확인 전.
- **본보기**: `docs/data/ps73_compaction_curve_20261006/` (README §5 · §7 · §8 · `make_fig_ms.py` · `make_fig_velocity_ms.py` · `atom_top_scan.py` · `docs/data/ps73_compaction_curve_20261006/early_ckpt/make_early_decks.py`) ·
  단계 고르기 = `docs/data/ps73_compaction_curve_20261006/stages_20261012/README.md` §6.  로그 읽기 = ps73 생성기와 같은 `scripts/compaction_curve.py`
  (thermo 블록 · run 마다 첫 줄 = 설정 줄 버림 · 단계 표지 · 판정 줄) · 앞 구간 곡선 채움 = ps73 `make_fig_ms.pchip` 그대로 (사본 없이 그 파일에서 읽는다).
- **입력 (리포 · 읽기만)**: 본 런 로그 `docs/data/kg50_d1_end_20261031/kg50_d1_b50_log.liggghts` (sha256 `6a90f706…` = 그 폴더 README §1) ·
  리포 덱 `docs/data/kg50_decks_20261027_v3_b50/kg50_d1_b50/input_kg50_d1_b50.liggghts` (`514afdb7…` · 로그 안 덱과 설정 14 개 같음) · 삽입 덱 `input_kg50_d1_b50_insert.liggghts` (`e5218b4d…`) ·
  끝 판 높이 기록 (mesh_end 122.596 µm · 그 README §2 · `docs/50kg/report_y4/draft2/data/D1/metrics_D1.json`) ·
  초안 2 압밀 곡선 `docs/50kg/report_y4/draft2/data/D1/curve_D1.csv` (대조 · 단계 표 ε_sphere 참고값).  dt · 판 속도 · 단위는 **로그 안 덱 글에서** 읽는다 (ps73 값을 쓰지 않는다).

## 1. 파일

| 파일 | 무엇 |
|---|---|
| `make_fig_d1_ms.py` | 생성기 (`--selftest` = 합성 시험 90 · §6 · `--atomtop` = 원자 기준 그림 요구) |
| `cluster/d1_atomtop_cluster.py` | D1 런 기계에서 돌리는 원자 기준 두께 준비 · 훑기 (표준 라이브러리만 · `--selftest` 9 · §8) |
| `origin/d1_ms_thickness_plate.csv` · `.ogs` | A Time (ms) · B Thickness (µm) · C Source — 판 위치 521 점 (메시 덤프 자리 5,000 step 마다 517 + 단계 모서리 4) |
| `origin/d1_ms_plate_velocity.csv` · `.ogs` | A Time (ms) · B Plate velocity (µm/s) · C Source — 계단 7 점 |
| `origin/d1_ms_pressure.csv` · `.ogs` | 압력 **원값판** — A Time (ms) · B Measured pressure (MPa) · C Source — 3,045 점 (0 ms 판 없음 0 MPa 하나 + thermo 원값 3,044) |
| `origin/d1_ms_pressure_slide.csv` · `.ogs` | 압력 **슬라이드판** — 3,044 점 (0 ms 1 + 판 정지까지 thermo 원값 2,943 + 이완 모식 100 · C Source 에 "모식" · §7) |
| `previews/d1_ms_compaction_3panel.png` · `.svg` | 세 패널 왼쪽 열 — 두께 (판 위치) · 판 속도 · 압력 원값 (ps73 서식 · 300 dpi · 4.3 × 7.2 in) |
| `previews/d1_ms_compaction_3panel_slide.png` · `.svg` | 같은 세 패널 — 압력만 슬라이드판 (§7) |
| `key_numbers_d1_ms.json` | 덱 설정 · 단계 경계 (step · ms) · 판 높이 · 잔차 · 압력 문턱 · 원자 수 · 대조 · 단계 프레임 · 클러스터 명령 · 압력 슬라이드판 (`pressure_slide`) · 원자 기준 (`atomtop` — 지금 `NOT_SUPPLIED`) |
| `stage_frames_d1.csv` | 오른쪽 3D 네 단계 → 가까운 atom 덤프 (§3) |
| (CSV 가 온 뒤) raw 폴더의 `kg50_d1_atomtop.csv` | D1 런 기계에서 받은 그대로 (§8) |
| (CSV 가 온 뒤) origin 폴더 d1_ms_thickness_atomtop (CSV · .ogs) · previews 폴더 d1_ms_compaction_3panel_atomtop · _atomtop_slide (PNG · SVG) | 원자 기준 한 곡선 (0 ms 부터 · 끊긴 y 축) — 압력 원값판 · 슬라이드판 두 장 (§8) |

- Origin: CSV 끌어 놓기 (Long Name = 1 줄 · Units = 2 줄 · 자료 3 줄부터) → 워크북을 앞에 두고 같은 이름 `.ogs` 를 Script Window 에 붙여 넣기 → BML 서식 (10 × 8 cm · Aptos 28 pt) ·
  단계 경계 점선 셋 (200.002 · 400.002 · 2685.002 ms) · x 눈금 500 ms · 색 = 두께 보라 · 판 속도 파랑 · 압력 빨강 · 목표 300 MPa 점선 없음 (1저자 슬라이드 서식 11-02).
  세 그래프를 세로로 쌓는 것 · 가로 단계 이름 · 빨간 화살표 = GUI (미리보기 배치 참고).
- 미리보기 글꼴 = Liberation Sans (이 기계에 Aptos 없음) — Origin 결과로 바꿔 끼운다.
- **한 그림 = 한 기준**: 판 기준 그림 (두께 = 판 위치) 과 원자 기준 그림 (두께 = 모든 원자의 max(z + r)) 을 섞지 않는다 (1저자 10-08 *"하나의 기준으로 해야지"*).

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

## 4. Particle packing (정착) 구간 — 판 기준 그림에서 그리지 않은 이유

- **이유**: 정착 (PHASE 1) 에는 판이 없다 (정착 뒤 Z_MAX 로 판을 만든다) ⇒ 이 구간의 두께 = 침대 맨 위 = 원자 위치가 필요하다.  덱은 atom 덤프를 PHASE 3 부터만 쓰고
  (`dump dmp_atom` 이 PHASE 3 표지에서 정의됨) 삽입 직후 체크포인트도 없다 (덱 머리 ⑬).  로그에는 정착 중 운동에너지 열과 정착 끝 `Z_MAX (center)` 139.4457 µm 하나뿐인데,
  이것은 **중심** 높이 (윗면 max(z + r) 아님) 이고 판 위치와도 다른 기준이라 그리지 않는다.  ⇒ 판 기준 그림의 0–200 ms 두께 칸은 비어 있고 "Particle packing" 이름만 둔다 · 그 시작의 빨간 화살표도 안 그렸다 (가리킬 자료 없음).
- **1저자 11-02 밤 = 넣는다** → 그림 전체를 원자 기준 하나로 바꾼다 (판 기준 · 원자 기준을 한 그림에 섞지 않는다) → 방법 · 스크립트 · 명령 = §8.
- ⚠ **정정 (11-02 밤)**: 이 절의 앞 판 표에 적었던 삽입 재현 비용 *"≈ 2 시간 (추정 — D0.7-40 삽입 런 실측을 원자 수 · step 수로 비례)"* 은 다른 덱 비례 추정이었다.
  D1 원 삽입 런 화면 (`log_kg50_d1_b50_ins.out` · 끝 묶음 멤버 · sha256 `a83ee39e…`) 실측 = 투입 (step 1) 17.8 s · 1 → 1,000 step 178.5 s · **1 → 20,001 step 4,584 s (≈ 76 분)** — NP 1.
  ⇒ 1저자 11-02 밤 *"첫번째 넣은 거에서 10g 로 중력가속도 그림 그린 다음에 이으면 되잖아"* — §8 기본 = 재현 없음 (0–20 ms = 10 g 자유 낙하 모식) · 삽입 런 전체 재현 (≈ 76 분) 은 `--with-replay` 일 때만.

## 5. 한정어 (그림 · 캡션에 같이)

- x = **step × dt (축척 덱 시간)** — 실제 압착 시간이 아니다 (ps73 README §5).  축 이름은 1저자 슬라이드대로 `Time (ms)` (ps73 미리보기는 한정어를 축 이름에 둔 `Simulation time (ms)`) → 캡션에 한정어.
- 두께 (판 기준 그림) = **판 위치** (바닥 z = 0 → 판) · 덱으로 계산 (메시 덤프는 리포에 없다) — 끝에서 mesh_end 와 대조 (잔차 −0.27 nm) · 초안 2 곡선과 같은 식 (다른 코드) 대조 (§6).
  판이 침대에 닿는 848 ms 전에는 침대가 아니라 판 위치다 (그 사이 판 아래 빈 틈).
- 두께 (원자 기준 그림 · §8) = **모든 원자의 max(z + r)** — 판으로 거르지 않는다 ⇒ 판을 뚫고 나간 입자도 들어간다 (D1 끝 덤프 `atom_end_2785002` 훑기 · 11-02 이 컨테이너:
  맨 위 = SE 입자 · 중심 123.22 µm > 판 122.596 µm · 윗면 **123.72 µm**) · 0.001 → 450 ms 의 채운 점 (PCHIP) 은 측정이 아니다 (CSV Source 열).
- 압력 = 판이 받는 수직 힘 ÷ 면적 (thermo 1,000 step 간격 · run 마다 설정 줄 버림).  정지 뒤 하락 = 판 고정 이완 (목표 미달 아님) ·
  **원값판** (`d1_ms_pressure.*`) = 진동 그대로 (기록) · **슬라이드판** (`d1_ms_pressure_slide.*`) = 판 정지 뒤 모식 감쇠 (§7) — *"모식"* 은 이 README · CSV Source 열에만 적고 슬라이드에는 적지 않는다 (1저자 11-02 밤 · ps73 1저자 결정과 같다).
- ⚠ D1 이완 끝 156 MPa ↔ D2 280 · D3 291 MPa (D1 README §3 · `KG50-20` · `DEMP-01`) — 입도 효과로 읽지 않는다 · "After relaxation" 프레임은 300 MPa 상태가 아니다.
  슬라이드판의 매끈한 감쇠는 그림용 모식이라 이 비교의 근거가 아니다 (끝 값 156.15 MPa 만 계산값).
- 판 속도 = 실제 길이 / 시뮬레이션 시간 (ps73 §8) · 0 구간은 x 축선과 겹친다.
- 빨간 화살표 — 판 기준 그림 = 이완 구간 (판 고정 · 122.596 µm) 을 아래로 가리키는 하나 (정착 자료 없음) · 원자 기준 그림 = 정착 시작 (첫 자료 점) + 이완 둘 (§8) ·
  단계 이름 가로 (슬라이드 배치) · 목표 점선 없음 · "Particle packing" = 9 pt 가로 · 위 패널 테두리 위 (축 밖) · x = 0 ms 왼쪽 맞춤 · Stabilization · Relaxation 글 뒤 점선은 흰 바탕으로 가림.

## 6. 검사

- `--selftest` 90/90 (11-03 낙하판 · 합성 · 리포 자료 안 읽음 — 아래 내역은 82 판 기준 · 낙하판에서 8 개 추가 · 목록 = selftest 출력) · 82 판 = 앞 판 48 (덱 14 · 로그 11 · 판 궤적 · 끝 대조 · 두께 점 8 · 판 속도 1 · 압력 2 · 단계 표 4 · 명령 · CSV 3 · 초안 2 대조 5) +
  11-02 밤 34: 압력 슬라이드판 4 (R1 정지까지 원값 그대로 · 원값 목록 안 바뀜 · R2 식 · 1,000 step 간격 · 마지막 = 런 끝 · 출처 "모식" · R3 정지 줄 없음 거부 · R4 정지 → 끝이 1,000 배수 아님 거부) ·
  원자 기준 CSV 24 (A0 CSV 없음 = 거부 · A1 정상 합성 통과 · A2 머리 · A3 step 빠짐 · A4 TIMESTEP · A5 원자 수 머리 ≠ 줄 · A6 체크포인트 KE · A7 · A7b 재현 KE (1,000 · 20,000 step) · A8 덤프 원자 수 ≠ 본 로그 ·
  A9 파일 시각 거꾸로 · A10 반경 · A11 p99.9 · 중심 > 윗면 · A12 time_ms · A13 깨진 줄 · A14 삽입 줄 · A15 새 구간 (0.001 ms 부터 · 측정점 그대로 · 채움 440 · 시각 증가) · A16 런 폴더 sha256 ·
  A16b 메타 줄 겹침 · A17 · A17b 외톨이 규칙 · A18 클러스터가 읽은 원 로그 KE · A19 체크포인트 원자 수 ≠ run 0 로그 · A20 CSV 를 만든 스크립트 ≠ 리포 스크립트) · 끊긴 y 축 4 (B1 범위 · B2 · B2b 끊을 틈 없음 거부 · B3 그림이 그려진다 —
  이름 · 화살표 겹침 검사 통과) · 이음 2 (I1 클러스터 스크립트 `scan()` 이 가짜 런 · work 폴더에서 쓴 CSV 를 생성기가 읽고 검사 통과 · I2 sha256 다르면 ⑩).
- **시험 먼저**: 함수 자리만 둔 판에서 새 시험 27 개가 모두 FAIL (앞 48 은 PASS) → 구현 뒤 0 FAIL.  그 뒤 더한 7 개 (A7b · A18 · A19 · A20 · B2b · I1 · I2) 는 아래 변이 · 이음 시험으로 확인.  삽입 재현을 1,000 → 20,000 step 으로 늘린 뒤 (1저자 11-02 밤) 시험은 행을 step 으로 찾게 고쳐 계획 길이와 무관하다.
- 변이 17 (새 검사를 하나씩 끈 사본 · 같은 폴더 임시 파일 → 지움) = **모두 잡힘** — 정지 줄 · 1,000 배수 · τ · 런 KE · sha256 · 파일 시각 · 반경 · 삽입 줄 · 외톨이 규칙 · 끊을 틈 · 메타 겹침 ·
  CSV 없음 · 원 로그 KE · run 0 원자 수 · 덤프 원자 수 · 스크립트 sha256 · step 목록.  B2b 는 처음 판이 다른 이유로 통과해 (채운 점이 옛 매듭 값이라 시작보다 높았다) 곡선을 새 매듭으로 다시 만들게 고쳤다.
- 결정성 · 바뀌지 않은 것: 산출 14 개를 두 번 돌려 sha256 같음 · 판 기준 원값판 (미리보기 PNG · SVG · CSV 3 · .ogs 3) · 단계 표 = 이 변경 전과 **바이트 같음** (git diff 없음).
- 원자 기준 갈래 건식 실행 (1 회 · 커밋 안 함): 합성 CSV (z 값 = 지어낸 것 · KE · 원자 수 = 실제 본 로그 · 원 삽입 화면 값) 를 `raw/` 에 두고 `--atomtop` →
  실제 로그 대조 통과 (체크포인트 10 · 덤프 48 의 KE · 원자 수 줄이 본 로그에 있음 · 클러스터 스크립트 step 계획 = 이 로그 · 덱 일정 · 스크립트 sha256 4 = 리포 로그 · 덱) · 그림 두 장 · CSV · .ogs · JSON 생성 →
  합성 CSV 와 산출을 지우고 다시 돌려 산출 sha256 이 건식 실행 전과 같음.  원자 기준 산출이 남았는데 CSV 가 없으면 생성기가 멈춘다 (낡은 그림 방지 · 확인함).
- 클러스터 스크립트: `--selftest` 9/9 (11-03 낙하판) · 실제 D1 덱 (리포) 로 덱 자르기 확인 (재현 덱 = 삽입 덱 처음 → `unfix ins_mix` 그대로 + 정착 블록 · `shell` · `restart` 줄 뺌 ·
  체크포인트 덱 = 본 덱 머리 + `read_restart` + 이웃 · 재료 · 접촉 · 벽 · 템플릿 · `run 0`) · 실제 끝 덤프 훑기 (`atom_end_2785002` · 168,452 · 깨진 줄 0 · 윗면 123.72 µm) ·
  원 삽입 화면 KE 읽기 (1 · 1,000 · 20,001 = 0.11946798 · 0.17034351 · 2.3894425) · 삽입 줄 읽기.
- pyflakes (생성기 · 클러스터 스크립트) 깨끗.  리포 모듈 (scripts · ps73 · cluster) 을 읽을 때 `__pycache__` 를 쓰지 않는다 (`sys.dont_write_bytecode`).
- 실제 로그: sha256 = D1 README · 로그 안 덱 = 리포 덱 (설정 14) · 판정 줄 457 = thermo · 마지막만 ≥ 0.3 · PHASE 4 표지 = 루프 탈출 · run 이 5,000 step 씩 빈틈없음 · step 엄격 증가.
- 초안 2 대조 (`make_fig_p2_aux.branches` 경로): `metrics_D1.json` compaction 11 값 같음 · `curve_D1.csv` 2,843 행 — 판 높이 최대 차 3.1e-8 µm · 압력 최대 차 5.7e-14 MPa.
  (같은 판 궤적 식을 다른 코드로 계산한 대조 — 판 위치의 독립 측정은 mesh_end 한 점뿐이다.)

## 7. 압력 슬라이드판 — 판 정지 뒤 진동 없이 (1저자 11-02 밤 · ps73 README §5 선례 그대로)

- 판 정지 (2,685,002 step = 2,685.002 ms · **300.58919 MPa**) 까지 = thermo 원값 (원값판과 같은 2,943 줄) · 그 뒤 = 모식 감쇠
  **p(s) = 156.15118 + (300.58919 − 156.15118) · exp(−(s − 2,685,002) / 15,000)** 을 1,000 step 마다 (2,686,002 … 2,785,002 · 100 점 · 마지막 = 런 끝).
- τ = 15,000 step (= 15 ms) = **그림용** (ps73 `make_fig.py` 값 · 자료에서 정한 값 아님) · **끝 값 156.15118 MPa 만 계산값** — 모식 곡선의 2,785,002 값은 156.335 MPa (0.18 MPa 위 · ps73 은 0.17 MPa 위).
- 대신한 원값 = 이완 101 줄: 첫 출력 2,686,000 199.68 MPa · 최저 2,689,000 111.98 · 최고 2,692,000 209.26 · 끝 156.15 MPa — 원값판 `d1_ms_pressure.csv` · `previews/d1_ms_compaction_3panel.*` 에 그대로 있다.
- 생성기 `slide_series` = ps73 `make_fig_ms.slide_series` 와 같은 식 · ps73 보다 엄격한 곳 하나: 마지막 압력 줄 = 런 끝 · 정지 → 끝 = 1,000 step 배수가 아니면 거부 (모식 마지막 점이 런 끝에 서야 끝 값과 같은 자리).
- Origin: `d1_ms_pressure_slide.csv` + `d1_ms_pressure_slide.ogs` (원값판과 같은 서식 · y 0–330 · 100 간격) · 실선 하나 (모식 구간도 같은 선 · 표지 없음).

## 8. 원자 기준 두께 — Particle packing 을 0 ms 부터 · 한 곡선 (D1 런 기계에서 한 번 · 약 10 분)

**0–20 ms (삽입) 구간 = 재현하지 않고 자유 낙하 모식으로 잇는다** (1저자 11-02 밤 *"첫번째 넣은 거에서 10g 로 중력가속도 그림 그린 다음에 이으면 되잖아"* · 76 분 재현 안 함):
- 측정은 삽입 런 끝 체크포인트 `restart_settling_20001.bin` (20.001 ms) 부터 — 그 윗면 h20 (측정) 에서 거꾸로 **h(t) = h20 + v0·(t20 − t) + ½·g·(t20² − t²)** 을 0 → 20 ms 1 ms 마다 (21 점) 그려 잇는다 —
  20.001 ms 에서 정확히 h20 (측정점과 맞닿는다).
- 상수 = 삽입 덱에서 읽는다 (생성기 `deck_free_fall`): **g = 98.1 m/s²** (`fix gravi all gravity 98.1` = 정착 중 10 g) · **v0 = 0.5 m/s** (`insert/pack … vel constant 0.0 0.0 -0.5`) · 덱 단위 (길이 ×1000 → 1 µm = 덱 1 mm · dt 1e-6 s) ·
  t20 = 20,001 step = 0.020001 s ⇒ **낙하 = (0.5 × 0.020001 + ½ × 98.1 × 0.020001²) × 1000 = 29.62 µm** ⇒ h(0) = h20 + 29.62 µm.
- **h(0) 대조 (자르지 않는다)**: 투입 영역 위끝 **322.7 µm** (`region reg_mix … 0.005 0.322700` — 입자 **중심** 이 놓이는 한계) 를 넘으면 생성기가 ⚠ 를 찍고 JSON `atomtop.free_fall.check` 에 적는다 ·
  윗면 (max(z + r)) 한계 = 위끝 + 최대 반경 3 µm = 325.7 µm 도 함께 적는다.  값은 그대로 그린다.
- **감쇠 무시 (`fix damp all viscous 1.0e-5` · F = −γ·v)**: m/γ = AM 55 s · SE (반경 0.5 µm) 0.086 s → 20 ms 동안 감쇠를 넣은 낙하 = AM 29.62 µm (차 0) · **SE 27.10 µm (모식보다 2.5 µm 덜)** —
  맨 위 입자가 SE 이면 실제 낙하가 모식보다 조금 작다 (어림 · JSON `damping_neglected`).  입자끼리 부딪힘도 넣지 않았다 (맨 위 = 구름 위쪽이 함께 떨어지는 동안만 맞는 그림).
- **모식 표기**: CSV Source 열 = `schematic free fall from insertion (모식 · not measured)` · 이 README · JSON 에만 — **그림에는 적지 않는다** (1저자).
- 삽입 런 전체 재현 (NP 1 · 1 → 20,000 step · 1,000 마다 덤프 21 장 · 원 화면 실측 4,584 s ≈ 76 분) 은 `prepare --with-replay` 로만 (그때는 0–20 ms 가 측정이고 모식이 없다 · CSV `#mode replay`).

**방법 = ps73 과 같은 갈래 · 같은 검사** (스크립트 `cluster/d1_atomtop_cluster.py` · 표준 라이브러리만 · 런 폴더는 읽기만 · 쓰기 = 새 work 폴더 · 있으면 거부):

| 갈래 | step | 무엇 | 맞춰 볼 값 (리포 기록 · 생성기 검사) |
|---|---|---|---|
| ① 체크포인트 `run 0` (NP 1) | 20,001 · 50,000 · 100,000 · 150,000 · 200,000 · 200,001 (`restart_after_settling`) · 250,000 · 300,000 · 350,000 · 400,000 | `in.ckpt_<step>` = 본 덱 머리 + `read_restart` (런 폴더 원본) + 이웃 · 재료 · 접촉 · 벽 · 템플릿 + 원자 덤프 (`id type x y z radius`) + `run 0` (움직이지 않음) | 본 로그 KE: 2.3894425 · 3.2480619 · 0.0073460391 · 0.00081993853 · 1.9866698e-05 · 1.9881675e-05 · 4.4168899e-07 · 3.8465837e-07 · 3.4737142e-07 · 3.1955678e-07 · 원자 168,457 |
| ② 원 atom 덤프 (읽기만) | 450,000 … 2,750,000 (50,000 마다 47) · `atom_end_2785002` | 그대로 훑기 | 머리 TIMESTEP = step · 원자 수 = 본 로그 그 step · 깨진 줄 0 · 파일 시각이 step 순서 |
| (`--with-replay` 일 때만) 삽입 재현 (NP 1 · ≈ 76 분) | 1 · 1,000 · … · 20,000 | `in.replay_0_20000` = 삽입 덱 처음 → `unfix ins_mix` 그대로 + 정착 블록 (`shell` · `restart` 줄 뺌) + 원자 덤프 + `run 20000` | 원 삽입 화면 KE (1,000 마다 21 개) · 삽입 줄 (168,457 개 · 질량 9.557438e-01) |

값 = 모든 원자의 **max(z + r)** (µm) · 열 = step · time_ms · ztop_um · source + 검사 열 (중심 최댓값 · 맨 위 입자 id · type · 반경 · p99.9 · 로그 원자 · KE · 파일 크기 · 시각) ·
끝 줄 = `#mode` (ckpt · replay) · `#insertion_orig` (원 삽입 줄) · `#sha256` (런 폴더 덱 둘 · 로그 둘) · `#script_sha256` (이 스크립트).

**1저자가 붙여 넣을 명령** (D1 런 기계 · 런 폴더 = 리포 기록상 `~/simulation/kg50_d1_b50` (`docs/data/kg50_decks_20261027_v3_b50/README.md` §3) — 다르면 `prepare --run <폴더>` ·
LIGGGHTS = 같은 §3 의 삽입 런 명령과 같은 `~/LIGGGHTS-PUBLIC/src/lmp_auto` — 다르면 `prepare --lmp <경로>` · 주소 · 포트는 적지 않는다):

```bash
# ⓪ 리포 파일 docs/50kg/report_y4/figs/d1_compaction/cluster/d1_atomtop_cluster.py 를 D1 런 기계 홈으로 가져간다 (평소 방법)
echo "8a9fe00fc86ba7b11d8d27d626bbebcf258d2aae1e64db1af8a8207998a57210  $HOME/d1_atomtop_cluster.py" | sha256sum -c -   # → OK (리포 파일과 같다)
python3 -I ~/d1_atomtop_cluster.py --selftest           # 끝 줄 = 9 PASS · 0 FAIL  (몇 초)
python3 -I ~/d1_atomtop_cluster.py prepare              # 런 폴더 확인 (sha256 4 · 체크포인트 10 · 덤프 48) → ~/kg50_d1_atomtop_20261102 에 덱 10 + run_atomtop.sh  (몇 초 · "삽입 재현 없음 (기본)")
cd ~/kg50_d1_atomtop_20261102 && setsid nohup bash run_atomtop.sh > run_atomtop.log 2>&1 < /dev/null &
tail -3 ~/kg50_d1_atomtop_20261102/run_atomtop.log      # 진행: ckpt <step> 시각 … → ≈ 10 분 뒤 KE_CHECK 10/10 같음 · ATOMTOP_DONE …/kg50_d1_atomtop.csv
sha256sum ~/kg50_d1_atomtop_20261102/kg50_d1_atomtop.csv
```

- 첫 대조가 `FAILED` 면: Windows 를 거치며 줄 끝이 CRLF 로 바뀐 경우가 흔하다 → `sed -i 's/\r$//' ~/d1_atomtop_cluster.py` 뒤 다시 대조 (그래도 다르면 다른 판 — 쓰지 않는다 ·
  CSV 끝 줄 `#script_sha256` 을 생성기가 리포 파일과 다시 대조한다 ⑪).
- **돌려받을 것** = `kg50_d1_atomtop.csv` 하나 (58 줄 + 메타 · 수십 KB) 와 그 sha256 → 이 폴더 아래 `raw` 폴더에 `kg50_d1_atomtop.csv` 이름 그대로 넣고
  `python3 -I docs/50kg/report_y4/figs/d1_compaction/make_fig_d1_ms.py --atomtop` → 검사 ①–⑫ (step 계획 · TIMESTEP · 원자 수 · 파일 시각 · 반경 · KE 상대 1e-6 · 삽입 줄 · 런 폴더 sha256 · 만든 스크립트 sha256 · #mode) 가
  하나라도 어긋나면 그리지 않고 멈춘다 → 통과하면 원자 기준 그림 두 장 (압력 원값판 · 슬라이드판) · CSV · .ogs · JSON `atomtop` (측정 · 채움 · 모식 수 · 자유 낙하 식 · h(0) 대조 · 무시한 감쇠 ·
  끊긴 자리에 가려진 측정점 · 외톨이 후보 · 맨 위가 판에 닿은 첫 덤프 · 판 위 중심 덤프 수 · 원자 수 변화 · KE 대조).
- `prepare` 가 거부하면 (런 폴더 파일 없음 · sha256 다름) 아무것도 만들지 않는다 → 그 줄을 보내 주면 된다.  체크포인트 KE 가 갈리면 `KE_CHECK` 줄에 표시되고 생성기가 거부한다.
- 쓰는 곳 = `~/kg50_d1_atomtop_20261102` 만 (덱 10 · 러너 · 로그 · 덤프 10 장 ≈ 0.1 GB 추정 · CSV) · 런 폴더 = `read_restart` · 덤프 읽기만.
- 시간 (추정): 체크포인트 10 × `run 0` (읽기 + 이웃 목록 · 각 수십 초 · 합 ≈ 5 분) + 훑기 58 장 (원 덤프 48 × ≈ 22.5 MB + 체크포인트 덤프 10 ≈ 1.2 GB 읽기 · 1–3 분) ≈ **10 분**.

**그림 꼴** (CSV 가 오면 · 합성 자료로 배치만 미리 확인 — 값은 아직 없다):
- 두께 패널 = **끊긴 y 축** — 아래 범위 = 판 놓은 뒤 모든 점 (+ 위쪽 단계 이름 자리 10 µm · 5 µm 단위 · 판 기준 그림과 같은 115–155 µm 예상) · 위 범위 = 시작 h(0) 을 담는 20 µm
  (같은 µm/높이 축척) · 끊긴 자리 = 흰 띠 + 양쪽 빗금.
- 빨간 화살표 둘 — 정착 시작 = 첫 점 (0 ms · 모식 h(0)) 을 위 오른쪽에서 · 이완 = 이완 구간 가운데의 원자 기준 값을 위에서 · 단계 이름 높이 = 이름 폭 안의 곡선 최댓값 위 · "Particle packing" = 위 패널 테두리 위.
- 20 → 450 ms = 측정점 (체크포인트 · 첫 원 덤프) 사이 PCHIP 채움 (측정 아님 · ps73 과 같다) · CSV Source 열에 표시.
- ⚠ 끊긴 자리 (아래 위끝 ~ 위 아래끝) 에 든 측정점은 보이지 않는다 (예: 20.001 · 50 ms 체크포인트가 그 사이면) → JSON `atomtop.hidden_in_break` 에 적는다 · 위 범위를 넓히려면 `HI_SPAN_UM` (1저자 결정).
- ⚠ 외톨이 (튀어 오른 입자 하나 — 윗면 − p99.9 ≥ 20 µm) 는 **빼지 않는다** — JSON 에 후보로만 적는다 · 빼라고 하면 ps73 규칙 그대로 (`atomtop_series(drop=…)` · 외톨이일 때만).
- Origin: 원자 기준 두께 CSV + .ogs (origin 폴더 · `d1_ms_thickness_atomtop` 이름 · y = 아래 범위 아래끝 … 위 범위 위끝) · **끊기 = GUI 한 번** (.ogs 머리 주석에 From · To 값 — LabTalk 끊기 속성은 확인하지 않아 스크립트에 넣지 않았다).

- **1저자에게 준 명령 (11-03)**: 같은 스크립트 (sha256 `8a9fe00f…`) 를 파일 이름 `d1_atomtop_ff.py` 로 받아 `prepare --work ~/kg50_d1_atomtop_ff` (예전 재현판으로 만든 `~/kg50_d1_atomtop_20261102` 와 겹치지 않게) · 돌려받을 것은 같다 (`kg50_d1_atomtop.csv` + sha256).
