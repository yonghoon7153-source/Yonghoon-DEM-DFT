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

## 6. 결과

⬜ 반입 대기 (1저자 WSL 실행 뒤).
