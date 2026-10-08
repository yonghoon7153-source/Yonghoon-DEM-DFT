# ps73 네 시점 von Mises — 공동 색 범위 (1저자 10-08)

**무엇**: 1저자 요청 *"이걸 총 4등분으로 von mis 구한 다음에 공동 스케일로 그리면 좋을거 같아 · 처음 mesh 랑 닿았을 때, compression 중간,
3100000, 그리고 맨 마지막 꺼"* · *"각각에 대해서 잘 뽑아오고 contact 뽑으면 될듯"* · *"step 잘 선택하고"* · *"restart.bin step 별로 봐야"*.
같은 침대 (ps45 · PC:SC 7:3 · r45) 의 압축 중 세 시점과 이완 끝 하나에서 입자 von Mises 응력 (Love–Weber) 을 구해, 네 패널을 **같은 색 범위**로
그린다 — 압축 중에는 위가 더 눌리고 (감쇠 저항 · `DEMP-01`) 이완 뒤에는 고르게 되는 것을 보이는 그림 (`../snap_3100000_20261008/README.md` 단면 하중의 짝).

## 1. 시점과 체크포인트 — 이름이 아니라 계보로 고른다

| 시점 | 곡선에서 정한 step | 쓰는 것 | 판 압력 | 그 파일을 마지막으로 쓴 조각 | 최종 궤적 |
|---|---|---|---|---|---|
| (a) 판 첫 접촉 | 976,000 (판 압력이 0.01 MPa 를 처음 넘는 step · 0.09 MPa) | `restart_settling_1000000.bin` (첫 접촉 뒤 첫 체크포인트) | 0.449 MPa | r1 (원 런 · 0 → 1,470,002) — 1,000,000 을 지난 조각은 r1 뿐 (r4 는 200,001 → 209,000) | ✅ 0 → 1,450,000 = r1 |
| (b) 압축 중간 (300 의 절반) | 2,191,000 (150 MPa) | `restart_compress_2200000.bin` | 151.5 MPa | r6 (1,650,000 → 2,421,000) — r7 은 2,400,000 부터 | ✅ (1,650,000, 2,400,000] = r6 |
| (c) 정지 직전 | 3,100,000 | `restart_compress_3100000.bin` — 이미 뽑음 (`../snap_3100000_20261008/`) | 296.2 MPa | r8 | ✅ |
| (d) 이완 끝 | 3,225,000 (런 끝) | 체크포인트 없이 원 런 이완 단계 덤프 **3,220,000** (contact 덤프 10,000 step 마다 · 마지막) = ps45 망 배치 7:3 케이스 `260925_000559_082983` (원자 160,417 = 그 step thermo 줄) | 165.3 MPa | r8 | ✅ |

- 계보 = `../../ps73_compaction_curve_20261006/README.md` §2 (r1 → r3 → r6 → r7 → r8 만 잇고 r2 · r4 · r5 는 버림).
- **체크포인트 이름 함정**: 압축 중인데 1,650,000 까지는 `restart_settling_*` 다 — 원 덱이 PHASE 1 에서 건 `restart 50000 …/restart_settling_*.bin` 을
  압축 단계에서도 그대로 썼다 (r2–r5 덱도 같음).  r6 부터 `restart_compress_*`.  `restart_compress_1650000.bin` 은 r6 가 읽은 파일.
- ibb 목록 (1저자 10-08): `restart_settling_` 50,000 … 1,650,000 · `restart_compress_` 1,650,000 … 3,200,000 (50,000 마다) · `restart_after_settling`.
- 300 MPa 바로 그 순간 (3,125,000) 은 체크포인트가 없다 (50,000 마다 · 3,100,000 다음은 정지 뒤 3,150,000) → (c) = 3,100,000.
- r1 덱 ↔ t0 덱: r1 에는 삽입 fix (pts1–3 · pdd_mix) 가 남아 있고 중력은 PHASE 1 98.1 → PHASE 2–3 9.81 · 감쇠 0.5 — 압축 단계 설정은 t0 덱과 같다.
  r3 가 r1 체크포인트 (`settling_1450000`) 를 삽입 fix 없이 읽어 이어 돌렸다 (같은 방식).

## 2. 체크포인트 내용 검사 — 이름만 믿지 않는다 (`make_snap_decks.py --verify`)

1. 스냅숏 덱의 출발 step 검사 — 체크포인트의 step 이 기대와 다르면 `BRANCH_ABORT` 로 멈춘다 (t0 덱의 그 줄을 step 마다 바꾼 것).
2. setup thermo 줄의 KE · 원자 수 = 원 런 로그의 그 step 값 (상대 1e-6 — 재개 G1 과 같은 규칙).
   기준: 1,000,000 = **2.3504113e-07** · 160,420 (r1 로그 `output_ps_7_3_r45_181338.out` 4375 행) · 2,200,000 = **1.1878694e-05** · 160,420
   (r6 로그 `…_r6_198529.out` 3420 행) · 3,100,000 = 1.695918e-05 (r8 · 가지 실험 KE_REF).
3. 스냅숏 atom 덤프의 id · type · 위치 · 반경 · 속도 = 원 런 atom 덤프 (글자 그대로 · 같은 덤프 형식) — c_strs 는 합산 순서 (MPI ↔ 직렬) 로
   끝자리가 다를 수 있어 비교하지 않는다.

셋 중 하나라도 어긋나면 그 체크포인트는 그림에 쓰지 않는다.

## 3. 덱 (`make_snap_decks.py`)

t0 덱 (`../in.branch_t0_syntax.liggghts`) 의 첫 `run 0` 앞까지 (3,100,000 때 1저자가 쓴 awk 자름과 같다) 에서 두 줄만 바꾸고 (출발 step 검사 ·
`pz_branch`) 접촉 덤프 · `run 0` · `print "SNAP_DONE"` 을 붙인다.  판 높이 = 리포 메쉬 덤프 묶음 (`../../ps73_compaction_curve_20261006/raw/ps73_curve_1.tgz`)
의 그 step 값 — 1,000,000 = 0.132302 · 2,200,000 = 0.120302 (덱 단위).  `run 0` 은 입자를 움직이지 않는다 (접촉 힘 = 체크포인트의 위치 · 속도 ·
접선 이력에서 다시 계산).  시험 `--selftest` 16 — 3,100,000 덱 = 1저자가 돌린 덱 · 판 STL = 커밋본 바이트 · 다른 step 은 세 줄만 다름 · 거부 다섯 · 검사 넷.

## 4. 계산 · 그림 (`vm_moments.py`)

- σ_VM = 봉인 `dem_analysis_core.calc_love_weber_stress` (return_arrays) 의 `arrays_vm` 그대로 (입자 접촉력 기반 대칭 응력의 VM — 웹앱
  'AM 만 — 입자 응력 (LW)' 와 같은 정의) × scale / 1e6 → MPa.  읽기 전용 (`plane_load_share` 의 봉인 로더를 거친다).
- 벽 (바닥 · 판) 접촉 힘은 덤프에 없다 → 벽에 닿은 입자 (z − r < 0 · z + r > 판 높이) 는 회색 · 색 범위 · 평균에서 뺀다.
- `vm_moments.{png,svg}` — 위 = 판 압력 곡선 + 네 시점 표지 · 아래 = 네 패널 (AM 입자 옆모습 x–z · 정사영 · 깊이 순 · 실제 반경) · 색 = σ_VM
  (MPa · log) · **네 패널 같은 범위** (기본 = 네 시점 AM (벽 아님 · σ_VM > 0) 을 모은 p5–p95 · `--range minmax` · `--range fixed --vmin --vmax`).
- `vm_moments_ratio.{png,svg}` — 같은 그림 · 색 = σ_VM / ⟨σ_VM⟩ (그 시점 전 입자 평균) = 크기를 뺀 공간 분포만.
- `vm_profile.{png,svg}` · `vm_profile.csv` — 높이 (z / 판 높이 · 10 칸) 별 부피 가중 평균 σ_VM (AM · SE).
- `vm_moments.json` — 시점마다 LW 상태 · 입력 sha256 · 수 · 평균 · 위 1/3 ÷ 아래 1/3 · 색 범위.  LW 가 OK 아닌 시점이 있으면 그림 없이 rc 2.
- 시험 `--selftest` 10 — 합성 기둥 (손 계산 r (F_아래 + F_위) / V) · 벽 표지 · 위 ÷ 아래 · 공동 범위 = 모은 p5–p95 · 판 압력 = 곡선 CSV · 실패 경로.

## 5. 명령 (1저자 · WSL — `<ibb 접속>` · `<포트>` 는 자리표시)

```bash
# ① ibb → WSL: 체크포인트 둘 + 원 런 atom 덤프 둘 (내용 검사용) — 약 200 MB
mkdir -p ~/ps73_snap_in && ssh -p <포트> <ibb 접속> 'cd ~/dem_test/ps45/ps_7_3_r45 && tar -cf - restart_ps_7_3_r45/restart_settling_1000000.bin restart_ps_7_3_r45/restart_compress_2200000.bin post_ps_7_3_r45/atom_1000000.liggghts post_ps_7_3_r45/atom_2200000.liggghts' | tar -xf - -C ~/ps73_snap_in && sha256sum ~/ps73_snap_in/restart_ps_7_3_r45/*.bin

# ② 코드 (이 커밋 이후) · 덱
cd ~/dem-audit && git fetch -q origin claude/stoic-knuth-NObVQ && git checkout -q --detach FETCH_HEAD && git log --oneline -1
PY=$(ls ~/Yonghoon-DEM-DFT/venv/bin/python ~/Yonghoon-DEM-DFT/.venv/bin/python3 2>/dev/null | head -1)
K=docs/data/ps73_damping_branch_20261007/snap_moments_20261008
$PY $K/make_snap_decks.py --selftest && $PY $K/make_snap_decks.py --steps 1000000 2200000 --out ~/ps73_snap_decks

# ③ 스냅숏 둘 (run 0 · 각 1 분 안팎) → 내용 검사 → 파서
for S in 1000000 2200000; do
  case $S in 1000000) CK=restart_settling_1000000.bin;; 2200000) CK=restart_compress_2200000.bin;; esac
  O=~/ps73_snap_$S && mkdir -p $O/post $O/snap $O/restart && cd $O
  stdbuf -oL ~/src/LIGGGHTS-PUBLIC/src/lmp_serial -in ~/ps73_snap_decks/in.snap_$S.liggghts -var ckpt ~/ps73_snap_in/restart_ps_7_3_r45/$CK -var out $O -var plate_stl ~/ps73_snap_decks/plate_snap_$S.stl > snap.log 2>&1; tail -1 snap.log
  cd ~/dem-audit && $PY $K/make_snap_decks.py --verify $S --log $O/snap.log --snap-atoms $O/post/atom_$S.liggghts --orig-atoms ~/ps73_snap_in/post_ps_7_3_r45/atom_$S.liggghts \
    && $PY scripts/parse_liggghts.py $O/post/atom_$S.liggghts $O/snap/contact_$S.liggghts $O/post/mesh_$S.stl -o $O/ana && echo '{"box_x": 0.05, "box_y": 0.05}' > $O/ana/input_params.json
done

# ④ 네 시점 그림 ((c) = 3,100,000 스냅숏 · (d) = ps45 망 배치 7:3 케이스)
$PY $K/vm_moments.py --selftest && $PY $K/vm_moments.py --meta ~/ps73_snap_3100000/ana_meta.json \
  --moment 1000000 ~/ps73_snap_1000000/ana --moment 2200000 ~/ps73_snap_2200000/ana --moment 3100000 ~/ps73_snap_3100000/ana \
  --moment 3220000 ~/ps45_network_20261006/work/results/260925_000559_082983 --out ~/ps73_vm_moments; echo "rc=$?"
tar -czf ~/ps73_vm_moments.tgz -C ~ ps73_vm_moments && sha256sum ~/ps73_vm_moments.tgz && cp ~/ps73_vm_moments.tgz /mnt/c/Users/Administrator/Downloads/
```

(d) 의 입력 sha256 은 ps45 단면 하중 분석과 같아야 한다 (`../../ps45_plane_load_20261007/ps45_v2/plane_load.json` 7:3 `inputs_sha256` —
atoms.csv `fd394a58…` · contacts.csv `d9685d03…`).

## 6. 결과 (1저자 WSL 10-08 · 묶음 `results_20261008/raw/ps73_vm_moments.tgz` sha256 `f01e491fa38f7b3c…` · 205,477 B)

**체크포인트 내용 검사 — 둘 다 ✓** (1저자 화면 10-08): 1,000,000 setup KE 2.3504113e-07 = 원 런 · 원자 160,420 · 위치 · 속도 다른 원자
**0 / 160,420** · 2,200,000 KE 1.1878694e-05 = 원 런 · **0 / 160,420**.  ibb 파일 날짜도 계보와 맞다 (settling_1000000 · atom_1000000 = 9-19 = r1 ·
compress_2200000 · atom_2200000 = 9-23 = r6).  (d) 입력 sha256 (atoms `fd394a58b91c…` · contacts `d9685d034219…`) = ps45 단면 하중 분석 7:3 입력과 같다.

| 시점 | 판 압력 | AM σ_VM 평균 (중앙값) MPa | AM 위 1/3 · 아래 1/3 | AM 위 ÷ 아래 | SE σ_VM 평균 · 위 ÷ 아래 | 벽 접촉 AM (제외) |
|---|---|---|---|---|---|---|
| (a) 판 첫 접촉 · 1.00 s | 0.45 MPa | 11.2 (12.5) | 5.4 · 16.1 | **0.34** | 19.9 · 0.34 | 17 / 1,656 |
| (b) 압축 중간 · 2.20 s | 152 MPa | 59.6 (38.7) | 110 · 22.6 | **4.87** | 54.7 · 2.53 | 41 |
| (c) 정지 직전 · 3.10 s | 296 MPa | 197 (121) | 259 · 141 | **1.84** | 113 · 1.43 | 56 |
| (d) 이완 끝 · 3.22 s | 165 MPa | 174 (115) | 169 · 174 | **0.97** | 113 · 1.05 | 54 |

평균 = 벽에 닿지 않은 입자의 부피 가중 · 위 / 아래 1/3 = 판 높이 기준.  공동 색 범위 = 네 시점 AM 을 모은 p5–p95 = **5.94 … 413 MPa** (log).

**읽기** (값 그대로 · 원인은 표지)
- (b) · (c) 압축 중에는 위가 더 눌린다 — AM 위 ÷ 아래 4.87 · 1.84.  (d) 이완 끝은 고르다 (0.97).  ⇒ 단면 하중 (`../snap_3100000_20261008/README.md` ·
  3,100,000 위 268 ↔ 아래 127 MPa · 이완 ≈ 165 고르게) 과 같은 방향이 **입자 응력에서도** 보인다.  원인 = 압축 단계 전역 감쇠 (`DEMP-01`) 로 본다 —
  (b) 의 기울기가 (c) 보다 큰 까닭은 확인 전 (관찰).
- (c) → (d): 판 압력은 296 → 165 MPa (−44 %) 인데 AM σ_VM 평균은 197 → 174 MPa (−12 %) — von Mises 는 세로 하중이 아니라 세로 · 가로 차이 (찌그러짐)
  라서 판 압력과 같이 줄지 않는다 (관찰 · 가로 응력 분해는 안 함).
- (a) 판 압력 0.45 MPa 인데 입자 σ_VM 이 수–수십 MPa 이고 **아래가 더 크다** (0.34).  ⚠ **축척 중력**: 덱은 길이를 1000 배로 키우고 응력을 1/1000 로
  줄였는데 중력 9.81 m/s² 와 밀도는 그대로다 → 침대 자기 무게가 만드는 응력이 실제보다 10⁶ 배 크다 (덱 ρ g H × 1000).  어림: 침대 겉보기 밀도 ≈ 3,260 kg/m³ (창 부피 몫 AM 0.655 · SE 0.345 · 고체 85 % 어림) ·
  높이 132 µm → 바닥 ≈ 4.2 MPa (세로).  ✅ 이완 끝 단면 하중이 위 165.6 → 아래 168.7 MPa 로 **3.1 MPa** 늘어나는 것이 같은 어림 (창 높이 93 µm →
  **2.98 MPa**) 과 맞는다.  (a) 의 σ_VM (AM 아래 16 · SE 아래 ≈ 28 MPa) 은 이 어림보다 크다 — 정착 단계 중력 98.1 (10 배 · r1 PHASE 1) 의 잔류 응력
  후보 (확인 전).  ⇒ 300 MPa 대에서는 중력 몫이 ≈ 2 % (3 / 165) 이지만 판 첫 접촉 같은 저압 상태에서는 중력이 응력을 지배한다.
- 같은 정의 그림 셋: `results_20261008/vm_moments.png` (MPa · 공동 범위) · `vm_moments_ratio.png` (σ_VM / ⟨σ_VM⟩ — 분포만) · `vm_profile.png`
  (높이 10 칸 평균 · AM · SE).  SVG · 입자 CSV 넷은 묶음 안에만.

## 7. 웹앱 꼴 3D 그림 (`render3d.py` · 1저자 10-08 *"4개를 이 형식으로 줘"* · *"범례도"* · *"벽면 안칠하는거 없애주고 색깔 질감 webapp 에서 나오는거랑 똑같이"*)

- 입력 = 위 묶음의 입자 CSV (`vm_am_<step>.csv` · 위치 · 반경 · σ_VM) + `vm_moments.json` 의 공동 색 범위 — **WSL 재실행 없음**.
- 웹앱 (`webapp/static/js/viewer3d.js` · three.js 0.160) 을 식으로 옮김: 색 = `jetColor` (8 비트) · log 정규화 · three.js 색 관리 (sRGB → 선형 → sRGB) ·
  MeshPhong (specular 0x111111 · shininess 30) · 물리 기준 조명 (주변광 0.4 + 방향광 0.8 · 위치 (1, 1.5, 1) · 1/π) · 원근 50° ·
  카메라 = 상자 중심 + (1.2, 0.8, 1.2) × 최대 변 (THREE 좌표 = (x, z, y)) — 네 장 같은 카메라 (가장 높은 판 132.3 µm 기준 상자) · 같은 자르기.
- 벽 (바닥 · 판) 에 닿은 입자도 칠한다 (1저자 요청 · 웹앱 기본과 같다) — 그 입자는 벽 힘이 빠진 값 (그림 밖 한정어).
- 출력 `results_20261008/render3d/`: `vm3d_<step>.png` 넷 (투명 배경 · AM 만) · `vm3d_colorbar.png` (σ_VM MPa · log · 눈금 10 · 30 · 100 · 300 ·
  웹앱 jetColor 와 같은 색 = 조명 전 바탕색) · `vm3d_4panel.png` (흰 바탕 미리보기).
- 시험 `--selftest` 9 — jetColor 8 비트 · log · 선형 색 · 범례 가운데 (선형 = (lo + hi) / 2 · log = √(lo · hi)) · 벽도 칠함 · three.js r160 Phong 손 계산 ·
  sRGB 왕복 · z-버퍼 (앞 구가 이김 · 바깥 투명 · 순서 무관).
- **선형판** (1저자 10-08 *"이 von Mises 도 그냥 이등분"*): `--scale linear` → 색 = 0 … 413 MPa (아래 0 · 위 = 모은 p95) · 범례 눈금 셋 = 0 · 206 · 413
  (이등분) · `results_20261008/render3d_linear/` (넷 · 범례 · 숫자 없는 막대 · 미리보기).  log 판 범례 셋 = 5.94 · 49.5 (기하평균) · 413.
- **공통 위쪽 576 판** (1저자 10-08 *"0 576 을 공통 범례로 잡고 다 새로 그려줘"*): `--scale linear --top maxown` → 위쪽 = 시점마다 p95 중 최대 ((c) 576 MPa) · 범례 0 · 288 · 576 ·
  `results_20261008/render3d_linear576/`.  까닭: 모은 p95 (413) 는 낮은 시점 (a · b) 이 끌어내려 (c) 10.7 % · (d) 8.1 % 가 맨 위 색으로 잘렸다 → 576 에서 5.0 · 3.8 %.
  범위 밖 값 = 막대 끝 색 (진한 빨강 · 그늘에서 고동색) — 검은색 아님.
- 보고 한정어 (1저자 10-08 대화): 같은 모델 안 비교 (시점 · 높이) 는 그대로 · MPa 절대값 · AM ↔ SE 크기는 "DEM (연화 SE) 모델 안 값" ·
  (a) 의 값은 축척 중력이 지배.  캡션 권고: *"Love–Weber particle von Mises stress (MPa) from the DEM contact forces (softened SE) — same colour
  scale; model-internal comparison."*
