# kg50_watch — 50kg SE 입도 비교 2케이스 읽기 전용 감시 (DEM1 포맷 · ibb · 10-28)

- 무엇: `docs/dem1/dem1_kit/tool/th_grid.sh` 의 `watch1` 을 그대로 옮겨 50kg 두 케이스 (`kg50_d07_b50` · `kg50_d2_b50`) 에 맞춘 **감시 전용** 도구.  제출 · 취소 · 재개는 하지 않는다 — 50kg 의 제출 · 재개는 `scripts/resume_ckpt.sh` (G0–G3) 몫이다 (`docs/dem1/README.md` "등록 캠페인과의 경계").
- 읽기 전용: sbatch · scancel · scontrol 없음 · 파일을 만들거나 바꾸지 않음 (임시 파일도 없음 · `~/.th_grid` 안 씀) · squeue 한 번 (실패하면 3초 간격 4번).

| 파일 | 무엇 |
|---|---|
| `kg50_watch.sh` | 도구 (md5 42ac91f7a4881eea7ae0a4365210c655) |
| `kg50_watch_block.txt` | ibb 설치 블록 — `cat > ~/kg50_watch.sh <<'KG50_WATCH_EOF'` … + 마지막 줄 md5 게이트 → watch 한 번 (md5 9afdf9c2a7ffd42c0c5e154dd734416d) |
| `test_kg50_watch.sh` | 납품 전 시험 (Slurm 흉내 `docs/dem1/dem1_kit/test/slurm.py` + 가짜 `~/dem_test` 나무 · LIGGGHTS 없음 · pkill 안 씀) |

## 쓰는 법

```bash
# 연구실 컴 WSL (리포 pull 뒤) — 주소 · 포트 = 1저자 (리포에 적지 않는다)
scp -P <포트> docs/dem1/kg50_watch/kg50_watch_block.txt <사용자>@<ibb 주소>:
# ibb
sed -i 's/\r$//' ~/kg50_watch_block.txt && bash ~/kg50_watch_block.txt     # md5 맞으면 ~/kg50_watch.sh 쓰고 watch 한 번
watch -n 60 bash ~/kg50_watch.sh watch
```

- 블록 다시 만들기 (도구를 고쳤을 때): `bash docs/dem1/dem1_kit/tool/make_block.sh docs/dem1/kg50_watch/kg50_watch.sh "bash ~/kg50_watch.sh watch"` (느낌표 · 탭 · CR · 구분자 검사 + md5).

## 표 (th_grid watch 와 같은 꼴 + 끝 열 resume)

머리 줄 = `내 코어 R <돌고 있는 내 잡 코어 합> / 60 (대기 <대기 잡 코어 합>)` (내 잡 전부 · 남의 캠페인 포함).

| 열 | 뜻 (th_grid 와 다른 점만 굵게) |
|---|---|
| case | `kg50_d07_b50` · `kg50_d2_b50` — 폴더 `~/dem_test/<C>` (resume_ckpt.sh 작업 사본 · 삽입 중엔 원 폴더) 또는 **`~/dem_test/<C>.ins1` 만** |
| job | 그 케이스 잡 = 이름 `C` 또는 `C_` 로 시작 (`C_ins` · `C_r<N>` · `C_r<N>t`) · **RUNNING 먼저 (번호 작은 것)** · **시험 잡 (`C_r<N>t`) 은 번호 뒤 `t`** |
| elapsed · left · np | squeue (np = 돌거나 대기 중인 잡 코어 · 없으면 최신 `run_C_r<N>.sh` 의 `#SBATCH -n`) |
| grid · phase · step · atoms · P_MPa | 로그에서: 돌고 있는 잡의 `~/dem_test/logs/output_<잡 이름>_<잡>.out` (없으면 `output_*_<잡>.out` · 그다음 잡 시작 뒤에 바뀐 `<폴더>/log.liggghts`) · 큐에 없으면 그 케이스의 가장 새 `output_C_*.out` · phase = 마지막 `====== (PHASE n · INSERT… · Simulation Finished` 줄 (덱 print 그대로) · P_MPa = 덱 thermo `pressMPa` (sim 값 · 덱 `target_press` 와 같은 단위 · CPU 0 인 run 첫 줄 제외) |
| plate_z · z/hs | 판 z = 이번 잡 mesh 덤프 (`post_C/mesh_<step>.stl`) 의 vertex z · **z/hs = 판 z ÷ (고체 두께 101.98 µm × 덱 길이 단위)** — 단위는 덱 `variable r_* equal <값>  # … r=<µm>` 줄 값 ÷ 주석 µm (세 줄이 같아야) = **1 µm = 0.001 → 0.10198** (화면 맨 아래 줄에 케이스마다 적음) · 101.98 = `docs/data/kg50_decks_20261027_v3_b50/README.md` §2 (덱 머리 ⑤) |
| kstep/h | 이번 잡 mesh 덤프 mtime (최근 1시간 · 모자라면 잡 시작부터) → 없으면 restart mtime → **그래도 없으면 로그 마지막 run 의 CPU 열 (그 run 의 경과 초 · 60 초 이상일 때)** — 긴 P1 (덤프 없음 · 체크포인트 50,000 step 마다) 에서도 값이 나오게 |
| ETA | P3 = 이번 잡 **P3 줄 안에서** 약 1시간 전 압력과 지금 압력의 기울기 (실제 step 간격으로 나눔) 로 덱 `target_press` 까지 선형 · P4 = **덱의 PHASE 4 print 글자 그대로인 줄** 다음 첫 thermo step + **덱 이완 run (100000)** − 지금 step · 그 밖 `-` |
| ckpt | `restart_C/` 의 가장 새 (mtime) 체크포인트 — `settling_N` · `compress_N` · `after_settling` · **`end`** |
| next | 대기 잡 (번호 작은 것 · 시험이면 `t`) — **50kg 은 다음 링크가 없으므로 '⚠다음링크없음' 경고 없음** |
| 상태 | `돌고있음 r4` · `시험 중 r56t` · `삽입 중` · `대기 <사유>` · `✅끝` · `시험 끝 · 본 제출 전` · `삽입 끝 · 재개 전` (`.ins1` 만 · 또는 원 폴더에서 마지막 step = 삽입 덱 run 합 23001) · `멈춤 (큐 없음)` · `폴더 없음` · `?큐조회실패` (squeue 4번 실패 — 멈춤으로 읽지 않음) · 덧붙임 `⚠로그없음` (돌고 있는 잡 로그가 없으면 옛 로그를 지금 것처럼 안 씀) · `⚠R2` (같은 케이스 RUNNING 둘) · `ERR<n>` · `FATAL` (덱 삽입 검사) |
| **resume** | `~/dem_test/resume_r*_*.md` 중 `## <C>` 절이 있는 **가장 최근 (mtime)** 보고의 판정 줄 — `✅본제출 <잡>` · `🧪시험만` · `⛔` · `-` (그 절이 있는 보고 없음).  보고 이름은 맨 아래 줄 |

- 덱에서 읽는 것 (작업 사본 덱 → 없으면 `.ins1` 덱): `target_press` · PHASE 4 print 글자 · 이완 run · r_* 줄 단위 · 삽입 덱 run 합.  덱 이름 규칙 (mesh · restart 이름 · thermo 열 · 표식) 은 시험의 "대조" 절이 리포 v3 덱 · 러너 · `scripts/resume_ckpt.sh` 와 맞는지 매번 확인한다 (바뀌면 시험 실패).
- 한계: 운영 어림이다 (판정 · 보고 수치 아님) · ETA 는 선형 · `dem_restart.py` 가 만드는 러너의 출력 이름은 리포에 없어 `output_<잡 이름>_<잡>.out` 을 먼저 보고 번호만으로 · log.liggghts 로 물러선다 (resume_ckpt.sh 는 시험 로그를 `logs/output_${C}_${SFX}t_$J.out` 로 읽는다) · 흉내에서만 시험했다 — ibb 실제 출력은 첫 실행에서 본다.

## 흉내 출력 (시험 장면 ① · 본런 P3 + `.ins1` 만)

```
══ 50kg SE 입도 2케이스 · 10-28 01:33:00 · 내 코어 R 9 / 60 (대기 28) ══
case         job      elapsed    left       np  grid   phase     step     atoms   P_MPa   plate_z   z/hs  kstep/h ETA    ckpt              next     상태                       resume
kg50_d07_b50 -        -          -          -   1x1x1  P1-settle 23001    488291  -       -         -     -       -      settling_20001    -        삽입 끝 · 재개 전          -
kg50_d2_b50  410001   3:00:00    4-20:59:59 4   2x2x1  P3-comp   640002   22353   0.2000  0.177600  1.74  60      2h     compress_600000   -        돌고있음 r4                ✅본제출 410001
(job 뒤 t = 시험 잡 · next = 대기 잡 (50kg 은 다음 링크 없음) · step: 이번 잡 mesh 덤프·로그 중 앞선 값 · P_MPa: 덱 thermo pressMPa (sim 값 · 덱 target_press 와 같은 단위) · z/hs: 판 z / 고체 두께 101.98 µm (덱 길이)
 kstep/h: 이번 잡 mesh 덤프 mtime (없으면 restart · 그것도 모자라면 로그 CPU 열) · ETA: P3 = 이번 잡 P3 의 최근 1시간 압력 기울기로 목표까지 선형 · P4 = 이완 남은 step)
(kg50_d07_b50 덱 값: 목표 0.30 · 이완 run 100000 · 1 µm = 0.001 덱 길이 (r_* 줄 3개) → 고체 두께 0.10198 · 덱 ~/dem_test/kg50_d07_b50.ins1/input_kg50_d07_b50.liggghts · resume ← 없음)
(kg50_d2_b50 덱 값: 목표 0.30 · 이완 run 100000 · 1 µm = 0.001 덱 길이 (r_* 줄 3개) → 고체 두께 0.10198 · 덱 ~/dem_test/kg50_d2_b50/input_kg50_d2_b50.liggghts · resume ← resume_r4_1028_0942.md)
```

(값은 흉내 고정물 — 실제 런 수치가 아니다.)

## 시험

```bash
bash docs/dem1/kg50_watch/test_kg50_watch.sh                       # 이 기계 awk
AWKBIN=/usr/bin/gawk LC_ALL=C.UTF-8 bash docs/dem1/kg50_watch/test_kg50_watch.sh   # ibb 꼴 (gawk 가 있을 때)
```

- 10-28 결과: ✅ 165 · ❌ 0 — mawk (POSIX) · gawk 5.2.1 (POSIX) · gawk 5.2.1 (C.UTF-8) 세 판 다.
- 장면: ① 본런 P3 (압력 기울기 ETA · mesh mtime kstep/h · 잡 시작 전 옛 mesh 안 셈 · 이름 비슷한 남의 잡 `kg50_d2_b40_r4` 안 셈 · 머리만 있는 더 새 보고 건너뜀) + `.ins1` 만 ② 보류 대기 + 시험 끝 (흉내 잡 COMPLETED) ③ 시험 돌고있음 (`t`) + ERROR 줄 + 본런 로그 지워짐 (mesh 로만 step · 판 z · kstep/h) + ⛔ 보고 ④ P4 이완 ETA + 끝 (✅끝 · ckpt end) ⑤ squeue 실패 ⑥ 삽입 중 (원 폴더) + 삽입 끝 · 옮기기 전 ⑦ QoS 대기 + 같은 케이스 RUNNING 둘 (⚠R2) ⑧ 삽입 FATAL + 폴더 없음.
- 장면마다: 읽기 전용 (홈 아래 파일 목록 · 크기 · mtime · 흉내 큐 잡 목록이 전후 같음) · stdin 을 열린 빈 FIFO 로 막아도 끝까지 돎 (빈 파일 이름으로 stdin 을 읽는 awk/grep 이 없다) · resume 열이 화면 폭 (한글 · 이모지 = 2칸) 으로 맞음.
- 대조 · 형식 · 붙여넣기: 리포 v3 덱 · 러너 · `scripts/resume_ckpt.sh` 의 이름 · 줄 · 판정 줄 · 느낌표 · 탭 · CR 0 · 첫 6줄 사용법 · `main "$@"; exit $?` · make_block 결과 = 이 폴더 블록 · 대화형 붙여넣기 왕복 · 1글자 깨짐 → 게이트가 막음 · CRLF → sed 로 복구.
- 가짜 로그는 ibb LIGGGHTS 꼴 (머리 `    Step    Atoms         KinEng …` · `Loop time of … finish time …` · `docs/data/mixer_highbo_devu_prelim_20261006/exact_runs/` 의 실제 로그와 같은 폭) 로 만든다.
