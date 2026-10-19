#!/usr/bin/env bash
# =============================================================================
# run_nd_elf_nc_gabia.sh — Nd@Li (6 월 선별 구조의 9 월 새 PP 판 · 120 원자) ELF · NC 규약 · gabia GPU
#   구조 결정 D-2026-10-19-nd-q23-ppswap-structure · GPU 자리 결정 D-2026-10-19-gabia-nd-elf-coexist-or-pause-li3nd
#   runlog db/properties/nd_q3_bader_elf_runlog_2026_10_19.json
#
# 무엇
#   9 월 k331 SCF 입력 (kprobe.in · Bader 와 같은 기하 · sha256 고정) 의 셀 · 좌표 · k 를 그대로 두고 pseudo 만 NC 로 바꿔
#   SCF (GPU) → pp.x ELF (CPU 후처리) → 호스트 표와 같은 결합 중점 표본 (tools/figures/sample_elf_bonds.py).
#   NC 규약 = 호스트 modelc ELF (ONCV · ecut 80/320 · plot_num 8 · 같은 표본 도구):
#     Li P S Cl O = gabia 의 SG15 (LPSOCl ELF 가 쓴 /data/work/runs/lpsocl_elf/pseudo · md5 기록)
#     Nd = PseudoDojo Nd3+ f-in-core psp8 → UPF 변환본 (저장소 · sha256 고정 · 밀도 양에만 — oncv_regen_check.py docstring)
#   다른 점 (기록에 남긴다): smearing mv 0.01 · nosym · k 3 3 1 (kprobe 와 같다 · 호스트는 fixed · k444) — gap 은 scf.out
#   고유값으로 따로 잰다 (verbosity high).
#
# GPU 자리 (사용자 10-19 '일단 같이 돌려봐' · '안되면 잠깐 li3Nd stop하고 해도 되잖아')
#   ① 메모리 프로브 — CPU pw.x 1 랭크 · 'Estimated … RAM' 한 줄을 읽으면 바로 끝낸다 (검사 · run 아님 · 최대 PROBE_S 초)
#   ② need = 추정 × NEED_FACTOR + NEED_PLUS (MiB) · free = 총량 − 사용
#   ③ MODE=auto: GPU 계산 프로세스 0 → alone · free − need ≥ MARGIN_MIB → coexist (가드: 합계 > GUARD_MIB 면 **우리 pw.x 만**
#      죽이고 끝 11 — 그때는 MODE=pause 로 다시) · 아니면 GPU 위가 **Li₃Nd r2 하나뿐**일 때만 pause:
#        r2 를 다음 BFGS 줄 직후 EXIT 로 세움 (pause_relax_at_bfgs.sh --no_runner --out) → r2 판정 '사람이 세움 → restart' 확인 →
#        GPU 빔 × 2 → ELF SCF 혼자 → **성공·실패 상관없이** r2 를 restart_qe_relax.sh --run 으로 다시 건다 (tmux · BFGS 이력 승계)
#      r2 말고 다른 잡이 GPU 에 있으면 아무것도 세우지 않는다 (끝 5). 탄성 · UMA 는 건드리지 않는다.
#
# JOB=removal (2026-10-19 · 카드 db/properties/nd_anion_removal_estimand_2026_10_19.json · 결정 D-2026-10-19-nd-anion-removal ·
#   GPU 자리 D-2026-10-19-gabia-nd-removal-pause-li3nd): 같은 kprobe.in 에서 tools/electronic/nd_anion_removal.py --make_inputs 로
#   떼어낸 셀 8 개 (PAW 그대로 · pseudo_dir = PSEUDO_DIR) 를 만들고, 같은 프로브 · GPU 자리 결정 · r2 정지/재개 안에서
#   8 SCF 를 차례로 돌린다 (실패 점은 같은 입력으로 한 번 다시 · 두 번 실패면 멈추고 r2 재개) · ELF 후처리 (pp.x · 표본 · gap) 는 없다.
#
# 쓰는 법 (worktree 뿌리에서)
#   DRY_RUN=1 PY=<uma python> bash tools/electronic/run_nd_elf_nc_gabia.sh    # 점검 + 프로브 + 결정만 (CPU 검사 · GPU 계산 0)
#   tmux new -d -s ndelf "PY=<uma python> bash $PWD/tools/electronic/run_nd_elf_nc_gabia.sh"
#
# 종료: 0 끝 · 3 입력 (kprobe sha · UPF sha · SG15) · 4 프로브 실패 · 5 GPU 상태가 기대와 다름 (세우지 않음) · 6 r2 정지 실패 ·
#       7 ELF SCF 실패 · 8 pp.x 실패 · 9 표본 실패 · 10 이미 실행 중 · 11 공존 가드 발동 (우리 pw.x 만 죽임) ·
#       12 r2 재개를 못 걸었다 (⚠ 사람이 바로 본다 — r2 가 서 있다)
# ⛔ 못 하는 것: Li₃Nd 말고 다른 잡을 세우지 않는다 · 탄성을 재개하지 않는다 · 결합 해석 (그건 기록에서 사람이) ·
#    GPU 메모리를 정확히 모른다 (CPU 추정 × 계수 — 가드가 마지막 안전망) · 6 월 nd_ELF.cube 와 숫자를 대지 않는다 (다른 계산)
# =============================================================================
set -u; set +H
REPO=$(cd "$(dirname "$0")/../.." && pwd)
SCF_IN=${SCF_IN:-/data/work/runs/nd_ppswap_2026_09_16/kprobe_k331/kprobe.in}
SCF_IN_SHA=${SCF_IN_SHA:-adbd6f707af0c3b92209dad10fa08fa2ab8633b66a75d0947651dd4665f3f4e2}
ND_UPF=${ND_UPF:-$REPO/db/inputs/nd_q3_elf_nc_2026_10_19/pseudo/Nd3plus_f-in-core.dojo_psp8_conv.upf}
ND_UPF_SHA=${ND_UPF_SHA:-56b2e141cc9726c8b544bfd1fe87e5a2098ac8d8117e4f2c23b280da85d00654}
SG15_DIR=${SG15_DIR:-/data/work/runs/lpsocl_elf/pseudo}
JOB=${JOB:-elf}
case "$JOB" in elf) OUT_DEF=/data/work/runs/nd_q3_elf_2026_10_19 ;; removal) OUT_DEF=/data/work/runs/nd_anion_removal_2026_10_19 ;;
  *) echo "⛔ JOB '$JOB' 모름 (elf · removal)"; exit 3 ;; esac
OUT=${OUT:-$OUT_DEF}
PSEUDO_DIR=${PSEUDO_DIR:-/data/work/pseudo}       # JOB=removal: PAW (kprobe.in 의 pseudo_dir 와 같다)
RM_TOOL=${RM_TOOL:-$REPO/tools/electronic/nd_anion_removal.py}
GPU_PW=${GPU_PW:-/data/apps/qe-7.4.1-gpu/bin/pw.x}
CPU_BIN=${CPU_BIN:-/data/apps/qe-7.4.1-cpu/bin}
MPIRUN_CPU=${MPIRUN_CPU:-/usr/bin/mpirun}
R2_DIR=${R2_DIR:-/data/work/runs/sei_control/li3nd_mp-976264_p333_r2}
R2_NSTEP=${R2_NSTEP:-200}
MODE=${MODE:-auto}
MARGIN_MIB=${MARGIN_MIB:-4096}; GUARD_MIB=${GUARD_MIB:-47500}
NEED_FACTOR=${NEED_FACTOR:-1.3}; NEED_PLUS=${NEED_PLUS:-1024}
PROBE_S=${PROBE_S:-300}; PROBE_MAXWAIT=${PROBE_MAXWAIT:-20}; POLL=${POLL:-30}; EMPTY_N=${EMPTY_N:-2}; EMPTY_MAX=${EMPTY_MAX:-3600}
PAUSE_TIMEOUT=${PAUSE_TIMEOUT:-14400}; PAUSE_POLL=${PAUSE_POLL:-20}
NVSMI=${NVSMI:-nvidia-smi}; TMUX_BIN=${TMUX_BIN:-tmux}
PAUSE_TOOL=${PAUSE_TOOL:-$REPO/tools/elastic/pause_relax_at_bfgs.sh}
RESTART_TOOL=${RESTART_TOOL:-$REPO/tools/sei/restart_qe_relax.sh}
SAMPLER=${SAMPLER:-$REPO/tools/figures/sample_elf_bonds.py}
PY=${PY:-python3}
NP_PP=${NP_PP:-8}
SKIP_LDD=${SKIP_LDD:-0}           # 시험용 — MPIRUN_GPU 를 직접 준다
GPU_ENV=()
# ── --selftest: 가짜 nvidia-smi · pw.x · pp.x · mpirun · 정지 도구 · Li₃Nd 드라이버 · tmux 로 전 경로 (QE·GPU 없이) ──
if [ "${1:-}" = --selftest ]; then
  T=$(mktemp -d); ok=0; bad=0; SELF=$(readlink -f "$0")
  ck(){ if [ "$2" = "$3" ]; then echo "  ⭕ $1"; ok=$((ok+1)); else echo "  ⛔ $1 — 얻음 '$2' · 기대 '$3'"; bad=$((bad+1)); fi; }
  mkdir -p "$T/bin" "$T/cpu" "$T/gpu" "$T/sg15" "$T/r2" "$T/other" "$T/hpcx/bin" "$T/hpcx/lib" "$T/lddbin"
  for e in Li P S Cl O; do echo "fake $e" > "$T/sg15/${e}_ONCV_PBE-1.2.upf"; done
  KP=$REPO/db/raw/nd_q3_bader_2026_10_19/scf_input_copy.in      # 9 월 kprobe.in 의 사본 (sha256 = 기록값)
  cat > "$T/bin/mpirun_cpu" <<'EOF'
#!/bin/bash
[ -n "${OPAL_PREFIX:-}" ] && { echo "OPAL_PREFIX 가 CPU mpirun 으로 샜다: $OPAL_PREFIX" >&2; exit 97; }
while [ $# -gt 0 ]; do case "$1" in --allow-run-as-root|--oversubscribe) shift ;; --bind-to|-np) shift 2 ;; --mca) shift 3 ;; *) break ;; esac; done
exec "$@"
EOF
  cat > "$T/bin/mpirun_gpu" <<'EOF'
#!/bin/bash
[ -n "${WANT_OPAL:-}" ] && [ "${OPAL_PREFIX:-}" != "$WANT_OPAL" ] && { echo "GPU mpirun 에 OPAL_PREFIX 가 없다" >&2; exit 96; }
while [ $# -gt 0 ]; do case "$1" in --allow-run-as-root|--oversubscribe) shift ;; --bind-to|-np) shift 2 ;; --mca) shift 3 ;; *) break ;; esac; done
exec "$@"
EOF
  cp "$T/bin/mpirun_gpu" "$T/hpcx/bin/mpirun"; : > "$T/hpcx/lib/libmpi.so.40"
  printf '#!/bin/bash\necho "\tlibmpi.so.40 => %s/hpcx/lib/libmpi.so.40 (0x0)"\n' "$T" > "$T/lddbin/ldd"
  cat > "$T/bin/ppcheck" <<'EOF'
#!/bin/bash
# QE 처럼 pseudo_dir (실행 폴더 기준) 에서 ATOMIC_SPECIES 의 파일을 찾는다 — 없으면 readpp 오류로 죽는다
f=$(printf '%s\n' "$@" | awk 'p{print; exit} /^-in$/{p=1}')
pd=$(grep -o "pseudo_dir='[^']*'" "$f" | cut -d"'" -f2)
for u in $(sed -n '/^ATOMIC_SPECIES/,/^$/p' "$f" | awk 'NF==3{print $3}'); do
  [ -f "$pd/$u" ] || { echo "     Error in routine readpp (1):"; echo "     file $pd/$u not found"; exit 1; }
done
EOF
  cat > "$T/cpu/pw.x" <<'EOF'
#!/bin/bash
"$(dirname "$0")/../bin/ppcheck" "$@" || exit 1
case "${PROBE_MODE:-ok}" in
  ok) echo "     PseudoPot. # 6 for Nd read from file:"; echo "     Estimated static dynamical RAM per process >       ${PROBE_GB_STATIC:-1.00} GB"
      [ "${PROBE_ONLY_STATIC:-0}" = 1 ] || { sleep 3; echo "     Estimated max dynamical RAM per process >       ${PROBE_GB:-9.50} GB"; }
      sleep 60 & echo $! >> "$NVSTATE/orphans"     # 고아 자식 하나 — 부모를 죽여도 남는다 (락 fd 를 물려받으면 락이 안 풀린다)
      exec sleep 60 ;;
  *)  echo "no estimate"; exec sleep 2 ;;
esac
EOF
  cat > "$T/cpu/pp.x" <<'EOF'
#!/bin/bash
f=$(grep -o "fileout='[^']*'" "$2" | cut -d"'" -f2)
{ echo "fake ELF"; echo "cube"; echo "    4    0.000000    0.000000    0.000000"
  echo "   10    1.000000    0.000000    0.000000"; echo "   10    0.000000    1.000000    0.000000"; echo "   10    0.000000    0.000000    1.000000"
  echo "   60    0.000000    1.000000    1.000000    1.000000"; echo "   16    0.000000    6.000000    1.000000    1.000000"
  echo "   17    0.000000    1.000000    6.000000    1.000000"; echo "    3    0.000000    6.000000    6.000000    1.000000"
  for i in $(seq 1 1000); do printf ' 0.50000'; [ $((i % 6)) = 0 ] && echo; done; echo; } > "$f"
EOF
  cat > "$T/gpu/pw.x" <<'EOF'
#!/bin/bash
"$(dirname "$0")/../bin/ppcheck" "$@" || exit 1
case "${SCF_MODE:-ok}" in
  fail) echo "     Error in routine c_bands (1):"; exit 1 ;;
  long) exec sleep 60 ;;
esac
sleep 1
cat <<'OUT'
     End of self-consistent calculation

          k = 0.0000 0.0000 0.0000 ( 24512 PWs)   bands (ev):

   -40.1000 -12.2000   1.5000   2.0000   4.6000   5.1000

     occupation numbers
     1.0000   1.0000   1.0000   1.0000   0.0000   0.0000

          k = 0.3333 0.0000 0.0000 ( 24498 PWs)   bands (ev):

   -40.0500 -12.1000   1.6000   2.1000   4.7000   5.2000

     occupation numbers
     1.0000   1.0000   1.0000   1.0000   0.0000   0.0000

     the Fermi energy is     3.1000 ev

!    total energy              =   -1234.56789012 Ry
     convergence has been achieved in  12 iterations
     PWSCF        :   1h 2m CPU      1h 3m WALL
   JOB DONE.
OUT
EOF
  cat > "$T/bin/nvsmi" <<'EOF'
#!/bin/bash
S=$NVSTATE
case "$*" in
  *memory.used*)  if [ -s "$S/used_seq" ]; then head -1 "$S/used_seq"; [ "$(wc -l < "$S/used_seq")" -gt 1 ] && sed -i 1d "$S/used_seq"; else cat "$S/used"; fi ;;
  *memory.total*) cat "$S/total" ;;
  *compute-apps*) cat "$S/pids" 2>/dev/null ;;
esac
EOF
  cat > "$T/bin/pause.sh" <<'EOF'
#!/bin/bash
echo "$*" > "$NVSTATE/pause_args"
[ "${PAUSE_RC:-0}" = 0 ] || { echo "[fake] ⛔ 정지 실패"; exit "$PAUSE_RC"; }
printf '\n     Program stopped by user request\nJOB DONE.\n' >> "$R2_DIR/00_control_relax.out"
kill "$(cat "$NVSTATE/r2pid")" 2>/dev/null; : > "$NVSTATE/pids"; echo "[fake] ✅ 세움"
EOF
  cat > "$T/bin/restart.sh" <<'EOF'
#!/bin/bash
if [ "$1" = --run ]; then echo "$*" >> "$NVSTATE/restart_ran"; echo "▶ $(basename "$4") mode=restart"; sleep 3; exit 0; fi
j=$(head -1 "$NVSTATE/judge"); [ "$(wc -l < "$NVSTATE/judge")" -gt 1 ] && sed -i 1d "$NVSTATE/judge"
echo "  $j $(basename "$1")"
EOF
  cat > "$T/bin/tmux" <<'EOF'
#!/bin/bash
case "$1" in
  new) shift; while [ $# -gt 0 ]; do case "$1" in -d) shift ;; -s) S=$2; shift 2 ;; *) C=$1; shift ;; esac; done
       echo "$S" >> "$NVSTATE/tmux_sessions"; ( bash -c "$C" & ) ;;
  has-session) grep -qx "$3" "$NVSTATE/tmux_sessions" 2>/dev/null ;;
esac
EOF
  # 가짜 r2 pw.x — 명령줄에 '-in …' 이 남아야 한다 (러너가 /proc cmdline 에서 입력 이름을 읽는다) · TERM 이면 자식 sleep 도 끝낸다
  printf '#!/bin/bash\nsleep 300 & c=$!; trap "kill $c 2>/dev/null; exit 0" TERM INT; wait $c\n' > "$T/bin/r2_pw"; cp "$T/bin/r2_pw" "$T/bin/other_pw"
  chmod +x "$T"/bin/* "$T"/cpu/* "$T"/gpu/* "$T/hpcx/bin/mpirun" "$T/lddbin/ldd"
  printf "&CONTROL\n  calculation='relax'\n  prefix='li3nd'\n/\n" > "$T/r2/00_control_relax.in"; cp "$T/r2/00_control_relax.in" "$T/r2/00_control_relax.restart.in"
  RESTART_LINE="⏸ 사람이 세움(EXIT·max_seconds) → nstep 200 · restart (BFGS 이력 승계)"
  SCRATCH_LINE="⏸ 사람이 세움(EXIT·max_seconds) → nstep 200 · from_scratch (⚠ save 없음 — 처음부터)"
  r2_up(){ printf '     number of bfgs steps    =    5\n' > "$T/r2/00_control_relax.out"
           ( cd "$T/r2" && exec "$T/bin/r2_pw" -in 00_control_relax.restart.in ) > /dev/null 2>&1 & echo $! > "$1/r2pid"; echo $! >> "$1/pids"; }
  other_up(){ ( cd "$T/other" && exec "$T/bin/other_pw" -in x.in ) > /dev/null 2>&1 & echo $! >> "$1/pids"; echo $! > "$1/otherpid"; }
  down(){ for f in r2pid otherpid; do [ -f "$1/$f" ] && kill "$(cat "$1/$f")" 2>/dev/null; done; sleep 0.3; }
  alive(){ kill -0 "$(cat "$1/r2pid")" 2>/dev/null && echo yes || echo no; }
  run(){   # $1 = 이름 · 나머지 = 환경 → rc (로그 $T/out_$1/run.log)
    local n=$1; shift
    timeout 120 env SCF_IN="$KP" SG15_DIR="$T/sg15" OUT="$T/out_$n" GPU_PW="$T/gpu/pw.x" CPU_BIN="$T/cpu" MPIRUN_CPU="$T/bin/mpirun_cpu" \
      SKIP_LDD=1 MPIRUN_GPU="$T/bin/mpirun_gpu" R2_DIR="$T/r2" NVSMI="$T/bin/nvsmi" NVSTATE="$T/st_$n" TMUX_BIN="$T/bin/tmux" \
      PAUSE_TOOL="$T/bin/pause.sh" RESTART_TOOL="$T/bin/restart.sh" PY="$PY" PROBE_S=10 PROBE_MAXWAIT=6 POLL=1 EMPTY_N=2 EMPTY_MAX=15 PAUSE_TIMEOUT=10 \
      "$@" bash "$SELF" > "$T/out_$n.console" 2>&1
    local rc=$?; echo "$n $SECONDS" >> "$T/timing"; echo $rc
  }
  st(){ mkdir -p "$T/st_$1"; echo 49140 > "$T/st_$1/total"; echo "$2" > "$T/st_$1/used"; : > "$T/st_$1/pids"; printf '%s\n' "$RESTART_LINE" > "$T/st_$1/judge"; }
  has(){ [ -e "$1" ] && echo yes || echo no; }
  # 1 alone
  st a 500; rc=$(run a)
  ck "alone: rc 0" "$rc" 0
  ck "alone: 결정 alone" "$(grep -c '결정: alone' "$T/out_a/run.log")" 1
  ck "alone: Nd-S · Cl-Nd 행 (표본 도구 컷 보탬)" "$(grep -cE '^Nd_at_Li_newPP_NC,(Nd-S|Cl-Nd),' "$T/out_a/nd_elf_bonds.csv")" 2
  ck "alone: gap 줄 (E_F 3.1 · 점유 최고 2.1 · 빈 최저 4.6 → 2.5 eV)" "$(grep -c 'gap: E_F 3.1000 eV · 최고 점유 2.1000 · 최저 빈 4.6000 → 2.500 eV' "$T/out_a/run.log")" 1
  ck "alone: 정지 · 재개 안 함" "$(has "$T/st_a/pause_args"):$(has "$T/st_a/restart_ran")" "no:no"
  ck "alone: scf.in = k 3 3 1 0 0 0 · 셀 3 줄 · 원자 120 줄 (실물 kprobe 사본에서)" \
     "$(grep -A1 '^K_POINTS' "$T/out_a/scf.in" | tail -1 | tr -s ' ' | sed 's/^ //'):$(grep -A3 '^CELL_PARAMETERS' "$T/out_a/scf.in" | tail -3 | grep -cE '^ *-?[0-9]'):$(sed -n '/^ATOMIC_POSITIONS/,$p' "$T/out_a/scf.in" | grep -cE '^(Li|Nd|P|O|S|Cl) ')" \
     "3 3 1 0 0 0:3:120"
  ck "alone: run.log 끝 줄 = ■ 끝 (해시 전)" "$(tail -1 "$T/out_a/run.log" | grep -c '■ 끝 · 끝 코드 0')" 1
  ck "alone: SHA256SUMS 에 run.log · pseudo · probe" "$(grep -cE '  \./(run\.log|pseudo/Nd3plus_f-in-core\.dojo_psp8_conv\.upf|probe/probe\.out)$' "$T/out_a/SHA256SUMS")" 3
  # 2 coexist (r2 위 · 빔 11,890 · need 4.88 GB × 1.3 + 1024 = 7520 → 여유 4,370 ≥ 4,096)
  st b 37250; r2_up "$T/st_b"; rc=$(run b PROBE_GB=4.88)
  ck "coexist: rc 0 · 결정 coexist" "$rc:$(grep -c '결정: coexist' "$T/out_b/run.log")" "0:1"
  ck "coexist: r2 를 안 건드렸다 (살아 있음 · 정지 호출 없음)" "$(alive "$T/st_b"):$(has "$T/st_b/pause_args")" "yes:no"
  ck "프로브: static (1.00 GB) 다음에 오는 max (4.88 GB) 를 쓴다 → 추정 4997" "$(grep -c '추정 4997 →' "$T/out_b/run.log")" 1
  down "$T/st_b"
  # 3 pause (9.5 GB → need 13,670 > 빔)
  st c 37250; r2_up "$T/st_c"; rc=$(run c)
  ck "pause: rc 0 · 결정 pause" "$rc:$(grep -c '결정: pause' "$T/out_c/run.log")" "0:1"
  ck "pause: 정지 도구 인자 = --in restart.in --out .out --no_runner" "$(grep -c -- '--in 00_control_relax.restart.in --out 00_control_relax.out --no_runner' "$T/st_c/pause_args")" 1
  ck "pause: SCF 뒤 r2 재개 (--run --nstep 200 r2)" "$(grep -c -- "--run --nstep 200 $T/r2" "$T/st_c/restart_ran" 2>/dev/null)" 1
  ck "pause: 재개는 tmux 세션으로" "$(grep -c '^li3nd_r2_res_' "$T/st_c/tmux_sessions")" 1
  down "$T/st_c"
  # 4 다른 잡이 GPU 에 있고 자리가 모자라면 아무것도 안 세운다
  st d 37250; r2_up "$T/st_d"; other_up "$T/st_d"; rc=$(run d)
  ck "⛔음성: 다른 잡 + 자리 모자람 → rc 5" "$rc" 5
  ck "⛔음성: 그때 정지 · SCF 없음 · r2 살아 있음" "$(has "$T/st_d/pause_args"):$(has "$T/out_d/scf.out"):$(alive "$T/st_d")" "no:no:yes"
  down "$T/st_d"
  # 5 정지 도구 실패 → ELF 안 돌림 · 재개 안 부름
  st e 37250; r2_up "$T/st_e"; rc=$(run e PAUSE_RC=6)
  ck "⛔음성: 정지 실패 → rc 6 · SCF 없음 · 재개 없음" "$rc:$(has "$T/out_e/scf.out"):$(has "$T/st_e/restart_ran")" "6:no:no"
  down "$T/st_e"
  # 6 정지 뒤 SCF 실패 → 그래도 r2 재개
  st f 37250; r2_up "$T/st_f"; rc=$(run f SCF_MODE=fail)
  ck "⛔음성: 정지 뒤 SCF 실패 → rc 7 이고 r2 는 다시 건다" "$rc:$(grep -c -- '--run' "$T/st_f/restart_ran" 2>/dev/null)" "7:1"
  down "$T/st_f"
  # 7 공존 가드 — 합계가 문턱을 넘으면 우리 pw.x 만 죽인다
  st g 37250; printf '37250\n48000\n' > "$T/st_g/used_seq"; r2_up "$T/st_g"; rc=$(run g PROBE_GB=4.88 SCF_MODE=long)
  ck "⛔음성: 가드 발동 → rc 11 · r2 살아 있음 · 정지·재개 없음" "$rc:$(alive "$T/st_g"):$(has "$T/st_g/pause_args"):$(has "$T/st_g/restart_ran")" "11:yes:no:no"
  ck "⛔음성: 가드가 우리 가짜 pw.x 를 죽였다 (남은 프로세스 0)" "$(pgrep -fc -- "$T/gpu/pw.x" 2>/dev/null || true)" 0
  down "$T/st_g"
  # 7b max 줄이 없는 QE (static 만) — 조금 기다린 뒤 static 을 쓴다
  st g2 500; rc=$(run g2 PROBE_ONLY_STATIC=1 PROBE_GB_STATIC=2.00)
  ck "프로브: max 줄이 없으면 static 2.00 GB → 추정 2048 · rc 0" "$rc:$(grep -c '추정 2048 →' "$T/out_g2/run.log")" "0:1"
  # 8 프로브가 추정 줄을 안 찍으면 멈춘다
  st h 500; rc=$(run h PROBE_MODE=none)
  ck "⛔음성: 프로브 추정 없음 → rc 4 · SCF 없음" "$rc:$(has "$T/out_h/scf.out")" "4:no"
  # 9 입력 해시
  cp "$KP" "$T/kp_mod.in"; echo "! changed" >> "$T/kp_mod.in"; st i 500
  ck "⛔음성: kprobe 사본이 다르면 rc 3" "$(run i SCF_IN="$T/kp_mod.in")" 3
  ck "⛔음성: Nd UPF sha 가 다르면 rc 3" "$(run i ND_UPF_SHA=0000)" 3
  mkdir -p "$T/sg15b"; cp "$T"/sg15/*.upf "$T/sg15b/"; rm "$T/sg15b/Cl_ONCV_PBE-1.2.upf"
  ck "⛔음성: SG15 Cl 이 없으면 rc 3" "$(run i SG15_DIR="$T/sg15b")" 3
  # 10 DRY_RUN — pause 결정이 나도 r2 를 안 건드린다
  st j 37250; r2_up "$T/st_j"; rc=$(run j DRY_RUN=1)
  ck "DRY_RUN: rc 0 · 결정 pause 를 찍고 · 정지 없음 · SCF 없음 · r2 살아 있음" "$rc:$(grep -c '결정: pause' "$T/out_j/run.log"):$(has "$T/st_j/pause_args"):$(has "$T/out_j/scf.out"):$(alive "$T/st_j")" "0:1:no:no:yes"
  rc=$(run j)
  ck "DRY_RUN 뒤 본 실행은 프로브를 재사용한다" "$(grep -c '프로브 재사용' "$T/out_j/run.log")" 1
  down "$T/st_j"
  # 11 정지 뒤 판정이 restart 가 아니면 (save 없음) ELF 안 돌림
  st k 37250; printf '%s\n' "$SCRATCH_LINE" > "$T/st_k/judge"; r2_up "$T/st_k"; rc=$(run k)
  ck "⛔음성: 정지 뒤 from_scratch 판정 → rc 6 · SCF 없음 · 재개 없음" "$rc:$(has "$T/out_k/scf.out"):$(has "$T/st_k/restart_ran")" "6:no:no"
  down "$T/st_k"
  # 12 SCF 뒤 재개 판정이 restart 가 아니면 끝 코드 12 (ELF 는 끝)
  st l 37250; printf '%s\n%s\n' "$RESTART_LINE" "$SCRATCH_LINE" > "$T/st_l/judge"; r2_up "$T/st_l"; rc=$(run l)
  ck "⛔음성: 재개 판정 이상 → rc 12 · cube 있음 · 재개 안 걸음" "$rc:$(has "$T/out_l/nd_elf_nc.cube"):$(has "$T/st_l/restart_ran")" "12:yes:no"
  down "$T/st_l"
  # 13 GPU 런타임 격리 — ldd 로 읽은 hpcx OPAL_PREFIX 는 GPU mpirun 에만 · CPU pp.x mpirun 으로 새면 97
  st m 500; rc=$(run m SKIP_LDD=0 PATH="$T/lddbin:$PATH" WANT_OPAL="$T/hpcx")
  ck "GPU 환경 격리: rc 0 (GPU mpirun 에 OPAL_PREFIX 있음 · CPU mpirun 에 없음)" "$rc" 0
  # 14–17 JOB=removal — 떼어낸 셀 8 개 (가짜 PAW 폴더 · 같은 kprobe 사본) · PY 는 ase 가 있어야 한다 (gabia 는 uma python)
  mkdir -p "$T/paw"; for f in $(sed -n '/^ATOMIC_SPECIES/,/^$/p' "$KP" | awk 'NF==3{print $3}'); do echo fake > "$T/paw/$f"; done
  st r 500; rc=$(run r JOB=removal PSEUDO_DIR="$T/paw")
  ck "removal alone: rc 0 · scf.out 8 · MANIFEST" "$rc:$(ls "$T"/out_r/rm_*/scf.out 2>/dev/null | wc -l | tr -d ' '):$(has "$T/out_r/MANIFEST.json")" "0:8:yes"
  ck "removal: tot_charge (S +2 넷 · Cl +1 넷) · pseudo_dir = PAW 폴더 (여덟)" \
     "$(grep -l 'tot_charge=+2.0' "$T"/out_r/rm_S*/scf.in 2>/dev/null | wc -l | tr -d ' '):$(grep -l 'tot_charge=+1.0' "$T"/out_r/rm_Cl*/scf.in 2>/dev/null | wc -l | tr -d ' '):$(grep -l "pseudo_dir='$T/paw'" "$T"/out_r/rm_*/scf.in 2>/dev/null | wc -l | tr -d ' ')" "4:4:8"
  ck "removal: ELF 후처리 없음 (cube · 표본 없음)" "$(has "$T/out_r/nd_elf_nc.cube"):$(has "$T/out_r/nd_elf_bonds.csv")" "no:no"
  ck "removal: SHA256SUMS 에 rm_*/scf.out 여덟" "$(grep -c '/rm_.*/scf.out$' "$T/out_r/SHA256SUMS" 2>/dev/null)" 8
  st s 37250; r2_up "$T/st_s"; rc=$(run s JOB=removal PSEUDO_DIR="$T/paw")
  ck "removal pause: rc 0 · 정지 있음 · 재개 1 · scf.out 8" \
     "$rc:$(has "$T/st_s/pause_args"):$(grep -c -- '--run' "$T/st_s/restart_ran" 2>/dev/null):$(ls "$T"/out_s/rm_*/scf.out 2>/dev/null | wc -l | tr -d ' ')" "0:yes:1:8"
  down "$T/st_s"
  st u 37250; r2_up "$T/st_u"; rc=$(run u JOB=removal PSEUDO_DIR="$T/paw" SCF_MODE=fail)
  ck "⛔음성: removal 두 번 실패 → rc 7 · r2 재개 · '한 번 다시' 기록" \
     "$rc:$(grep -c -- '--run' "$T/st_u/restart_ran" 2>/dev/null):$(grep -c '같은 입력으로 한 번 다시' "$T/out_u/run.log" 2>/dev/null)" "7:1:1"
  down "$T/st_u"
  mkdir -p "$T/paw2"; cp "$T"/paw/* "$T/paw2/"; rm "$T/paw2/$(ls "$T/paw2" | head -1)"
  st w 500; ck "⛔음성: removal PAW 하나 없음 → rc 3" "$(run w JOB=removal PSEUDO_DIR="$T/paw2")" 3
  for x in $(pgrep -f -- "$T/bin/" 2>/dev/null); do kill -9 "$x" 2>/dev/null; done
  cat "$T"/st_*/orphans 2>/dev/null | xargs -r kill 2>/dev/null
  [ "${KEEP_T:-0}" = 1 ] && echo "  (시험 폴더 남김: $T)" || rm -rf "$T"
  echo "  selftest: ⭕ $ok · ⛔ $bad"; [ "$bad" = 0 ] && exit 0 || exit 1
fi

mkdir -p "$OUT"
LOG=$OUT/run.log
say(){ echo "[$(date '+%F %T')] $*" | tee -a "$LOG"; }
exec 9>"$OUT/.lock"; flock -n 9 || { say "⛔ 이미 실행 중 ($OUT/.lock)"; exit 10; }
# ⚠ 자식 프로세스에는 fd 9 를 닫아서 넘긴다 (… 9>&-) — 물려받은 자식이 남으면 락이 안 풀린다
#   (2026-10-19 selftest 실측: 프로브의 자식이 살아 남아 DRY_RUN 뒤 본 실행이 '이미 실행 중' 으로 멈췄다)
say "════ Nd $([ "$JOB" = removal ] && echo '떼어내기 SCF 8 (PAW 70/560)' || echo 'ELF (NC 80/320)') · HEAD $(git -C "$REPO" rev-parse --short HEAD 2>/dev/null) · MODE $MODE${DRY_RUN:+ · DRY_RUN} · OUT $OUT ════"

# ① 입력 ───────────────────────────────────────────────────────────────────
[ -s "$SCF_IN" ] || { say "⛔ kprobe 입력 없음 ($SCF_IN)"; exit 3; }
[ "$(sha256sum "$SCF_IN" | cut -c1-64)" = "$SCF_IN_SHA" ] || { say "⛔ kprobe 입력 sha256 ≠ Bader 계보 기록 ($SCF_IN_SHA) — 다른 기하다"; exit 3; }
if [ "$JOB" = removal ]; then
  PAWS=$(sed -n '/^ATOMIC_SPECIES/,/^$/p' "$SCF_IN" | awk 'NF==3{print $3}')
  [ "$(echo "$PAWS" | grep -c .)" = 6 ] || { say "⛔ kprobe 의 ATOMIC_SPECIES 가 여섯이 아니다"; exit 3; }
  for f in $PAWS; do [ -s "$PSEUDO_DIR/$f" ] || { say "⛔ PAW pseudo 없음 ($PSEUDO_DIR/$f)"; exit 3; }; done
  say "PAW pseudo ✓ $(for f in $PAWS; do printf '%s(%s) ' "$f" "$(md5sum "$PSEUDO_DIR/$f" | cut -c1-8)"; done)"
  "$PY" "$RM_TOOL" --make_inputs --out "$OUT" --lineage "$SCF_IN" --pseudo_dir "$PSEUDO_DIR" 2>&1 9>&- | tee -a "$LOG"
  [ "${PIPESTATUS[0]}" = 0 ] || { say "⛔ 떼어낸 입력 만들기 실패 (계보 sha · 줄 차이 검사)"; exit 3; }
  RM_DIRS=$(ls -d "$OUT"/rm_*/ 2>/dev/null | sed 's#/$##' | sort)
  [ "$(echo "$RM_DIRS" | grep -c .)" = 8 ] || { say "⛔ 떼어낸 입력이 8 개가 아니다 ($(echo "$RM_DIRS" | grep -c .))"; exit 3; }
  PROBE_IN=$(echo "$RM_DIRS" | head -1)/scf.in
  say "입력 ✓ $(echo "$RM_DIRS" | xargs -n1 basename | tr '\n' ' ')· 프로브 = $(basename "$(dirname "$PROBE_IN")")"
else
[ -s "$ND_UPF" ] && [ "$(sha256sum "$ND_UPF" | cut -c1-64)" = "$ND_UPF_SHA" ] || { say "⛔ Nd UPF 없음 또는 sha256 ≠ $ND_UPF_SHA ($ND_UPF)"; exit 3; }
mkdir -p "$OUT/pseudo"
declare -A PPF
for e in Li P S Cl O; do
  c=$(ls "$SG15_DIR" 2>/dev/null | grep -iE "^${e}_ONCV_PBE.*\.upf$")
  [ "$(printf '%s\n' "$c" | grep -c .)" = 1 ] || { say "⛔ SG15 $e 가 하나가 아니다 ($SG15_DIR: ${c:-없음})"; exit 3; }
  PPF[$e]=$c; cp -p "$SG15_DIR/$c" "$OUT/pseudo/"
done
PPF[Nd]=$(basename "$ND_UPF"); cp -p "$ND_UPF" "$OUT/pseudo/"
say "pseudo ✓ $(for e in Li P S Cl O Nd; do printf '%s=%s(%s) ' "$e" "${PPF[$e]}" "$(md5sum "$OUT/pseudo/${PPF[$e]}" | cut -c1-8)"; done)"
"$PY" - "$SCF_IN" "$OUT/scf.in" "${PPF[Li]}" "${PPF[P]}" "${PPF[S]}" "${PPF[Cl]}" "${PPF[O]}" "${PPF[Nd]}" <<'PY' 2>&1 | tee -a "$LOG"
import re, sys
src, dst, li, p, s, cl, o, nd = sys.argv[1:9]
t = open(src).read()
def block(name, n):
    # ⚠ '^[ \t]*' 이지 '^\s*' 가 아니다 — \s 는 줄바꿈도 먹어서 앞 빈 줄에서 매치가 시작되고 블록이 한 줄 밀린다
    #   (2026-10-19 실물: k 줄 · 셀 셋째 줄 · 마지막 원자가 빠졌는데 가짜 QE 시험은 통과했다)
    m = re.search(rf"^[ \t]*{name}\b.*$", t, re.M | re.I)
    if not m:
        raise SystemExit(f"⛔ {name} 이 kprobe 입력에 없다")
    lines = t[m.start():].splitlines()
    head, body = lines[0], lines[1:1 + n]
    if not head.strip().upper().startswith(name) or len(body) != n or any(not l.strip() for l in body):
        raise SystemExit(f"⛔ {name} 블록이 머리 + {n} 줄이 아니다")
    return "\n".join([head] + body)
nat = int(re.search(r"\bnat\s*=\s*(\d+)", t).group(1))
species = re.findall(r"^\s*([A-Z][a-z]?)\s+[\d.]+\s+\S+\.(?:UPF|upf)\s*$", t, re.M)
if sorted(species) != sorted(["Li", "Nd", "P", "O", "S", "Cl"]):
    raise SystemExit(f"⛔ kprobe 종 {species} — Li Nd P O S Cl 이 아니다")
mass = {"Li": 6.941, "Nd": 144.242, "P": 30.974, "O": 15.999, "S": 32.065, "Cl": 35.453}
pp = {"Li": li, "P": p, "S": s, "Cl": cl, "O": o, "Nd": nd}
inp = f"""&CONTROL
  calculation='scf', prefix='nd_elf_nc', outdir='./tmp', pseudo_dir='./pseudo', verbosity='high'
/
&SYSTEM
  ibrav=0, nat={nat}, ntyp=6, ecutwfc=80.0, ecutrho=320.0,
  occupations='smearing', smearing='mv', degauss=0.01, nosym=.true.
/
&ELECTRONS
  conv_thr=1.0d-10, mixing_beta=0.3, electron_maxstep=200
/
ATOMIC_SPECIES
""" + "".join(f"  {e:2s} {mass[e]:9.3f}  {pp[e]}\n" for e in species) + "\n" + \
    block("K_POINTS", 1) + "\n\n" + block("CELL_PARAMETERS", 3) + "\n\n" + block("ATOMIC_POSITIONS", nat) + "\n"
kp = block("K_POINTS", 1).splitlines()[1].split()
cel = [l.split() for l in block("CELL_PARAMETERS", 3).splitlines()[1:]]
pos = [l.split() for l in block("ATOMIC_POSITIONS", nat).splitlines()[1:]]
if len(kp) != 6 or len(cel) != 3 or any(len(r) < 3 for r in cel) or len(pos) != nat or any(r[0] not in mass for r in pos):
    raise SystemExit(f"⛔ 옮긴 블록 검사 실패 (k {kp} · 셀 {len(cel)} 줄 · 원자 {len(pos)}/{nat})")
open(dst, "w").write(inp)
print(f"scf.in ✓ nat {nat} (원자 줄 {len(pos)}) · 종 {' '.join(species)} · k {' '.join(kp)} · 셀·좌표 = kprobe 그대로 · NC 80/320 · mv 0.01 · nosym")
PY
[ "${PIPESTATUS[0]}" = 0 ] && [ -s "$OUT/scf.in" ] || { say "⛔ scf.in 만들기 실패"; exit 3; }
PROBE_IN=$OUT/scf.in
fi

# ② 메모리 프로브 (CPU 검사 · run 아님) ──────────────────────────────────────
#   ⚠ QE 7.4 는 'Estimated static dynamical RAM' 다음 줄에 'Estimated max dynamical RAM' 을 찍는다 — **max 를 쓴다**
#     (2026-10-19 gabia 첫 프로브: 첫 'Estimated' 줄 = static 9.89 GB 를 읽었다 · 그날 결정 (pause) 은 같았다)
est_line(){ grep -a "Estimated max\|Estimated total" "$1" 2>/dev/null | head -1 | grep . || grep -a "Estimated" "$1" 2>/dev/null | head -1; }
est_mib(){ echo "$1" | awk '{for(i=1;i<=NF;i++) if($i ~ /^[0-9.]+$/ && ($(i+1)=="GB"||$(i+1)=="MB")) {printf "%d", ($(i+1)=="GB" ? $i*1024 : $i); exit}}'; }
EST_MIB=""
if [ -n "${PROBE_EST_MIB:-}" ]; then EST_MIB=$PROBE_EST_MIB; say "프로브 생략 — PROBE_EST_MIB=$EST_MIB 를 준 값으로 쓴다"
elif [ -f "$OUT/probe/scf.in.sha256" ] && [ "$(cat "$OUT/probe/scf.in.sha256")" = "$(sha256sum "$PROBE_IN" | cut -c1-64)" ] \
     && grep -aq "Estimated" "$OUT/probe/probe.out" 2>/dev/null; then
  L=$(est_line "$OUT/probe/probe.out"); EST_MIB=$(est_mib "$L")
  say "프로브 재사용 (같은 scf.in) — $(echo "$L" | tr -s ' ')"
else
  PD=$OUT/probe; rm -rf "$PD"; mkdir -p "$PD"
  # scf.in 의 pseudo_dir='./pseudo' 는 **실행 폴더** 기준이다 — 프로브는 probe/ 에서 도니 링크를 건다
  #   (2026-10-19 gabia 첫 DRY_RUN: 링크 없이 4 초 만에 MPI_ABORT · 가짜 pw.x 가 pseudo 를 안 읽어 시험이 못 잡았다)
  ln -s ../pseudo "$PD/pseudo"
  say "▶ 메모리 프로브 — CPU pw.x 1 랭크 · 검사용 (run 아님) · 'Estimated' 줄을 읽으면 바로 끝 (최대 ${PROBE_S} s)"
  ( cd "$PD" && OMP_NUM_THREADS=1 ESPRESSO_TMPDIR="$PD/tmp" exec "$MPIRUN_CPU" --allow-run-as-root --bind-to none --mca btl self,vader -np 1 \
      "$CPU_BIN/pw.x" -in "$PROBE_IN" > probe.out 2>&1 9>&- ) &
  PPID_PROBE=$!; t0=$(date +%s); tS=""
  while kill -0 "$PPID_PROBE" 2>/dev/null; do
    grep -aq "Estimated max\|Estimated total" "$PD/probe.out" 2>/dev/null && break
    if grep -aq "Estimated" "$PD/probe.out" 2>/dev/null; then   # static 만 보였다 — max 를 조금 기다린다
      [ -z "$tS" ] && tS=$(date +%s)
      [ $(( $(date +%s) - tS )) -ge "$PROBE_MAXWAIT" ] && break
    fi
    [ $(( $(date +%s) - t0 )) -gt "$PROBE_S" ] && break
    sleep 2
  done
  kill -TERM "$PPID_PROBE" 2>/dev/null; sleep 2; kill -KILL "$PPID_PROBE" 2>/dev/null; wait "$PPID_PROBE" 2>/dev/null
  for x in $(pgrep -f -- "-in $PROBE_IN" 2>/dev/null); do
    [ "$(readlink -f /proc/$x/cwd 2>/dev/null)" = "$(readlink -f "$PD")" ] && kill -KILL "$x" 2>/dev/null
  done
  rm -rf "$PD/tmp"
  L=$(est_line "$PD/probe.out"); EST_MIB=$(est_mib "$L")
  [ -n "$EST_MIB" ] || { say "⛔ 프로브가 'Estimated … RAM' 을 안 찍었다 — QE 오류 줄 (probe/probe.out):"
                         grep -a -A4 "Error in routine" "$PD/probe.out" | head -8 | tee -a "$LOG"; exit 4; }
  grep -aq "PseudoPot. # 6\|PseudoPot. #  6" "$PD/probe.out" && say "프로브: QE 7.4.1 이 pseudo 여섯을 읽었다 (Nd 변환 UPF 포함)"
  say "프로브 ✓ $(echo "$L" | tr -s ' ')"
  sha256sum "$PROBE_IN" | cut -c1-64 > "$PD/scf.in.sha256"
fi
NEED=$(awk -v e="$EST_MIB" -v f="$NEED_FACTOR" -v p="$NEED_PLUS" 'BEGIN{printf "%d", e*f+p}')

# ③ GPU 상태 · 결정 ──────────────────────────────────────────────────────────
gpu_used(){ "$NVSMI" --query-gpu=memory.used --format=csv,noheader,nounits 2>/dev/null | head -1 | tr -d ' '; }
gpu_total(){ "$NVSMI" --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | head -1 | tr -d ' '; }
gpu_pids(){ "$NVSMI" --query-compute-apps=pid --format=csv,noheader 2>/dev/null | tr -d ' ' | grep -E '^[0-9]+$'; }
R2_REAL=$(readlink -f "$R2_DIR" 2>/dev/null || echo "$R2_DIR")
TOT=$(gpu_total); USED=$(gpu_used)
[ -n "$TOT" ] && [ -n "$USED" ] || { say "⛔ nvidia-smi 를 못 읽었다"; exit 5; }
FREE=$((TOT - USED)); R2_PIDS=""; OTHER=""
for p in $(gpu_pids); do
  if [ "$(readlink -f /proc/$p/cwd 2>/dev/null)" = "$R2_REAL" ]; then R2_PIDS="$R2_PIDS $p"; else OTHER="$OTHER $p($(readlink -f /proc/$p/cwd 2>/dev/null || echo '?'))"; fi
done
say "GPU 총 $TOT · 사용 $USED · 빔 $FREE MiB · 추정 $EST_MIB → need $NEED MiB (×$NEED_FACTOR + $NEED_PLUS) · r2 pw.x:${R2_PIDS:- 없음} · 다른 잡:${OTHER:- 없음}"
DEC=$MODE
if [ "$MODE" = auto ]; then
  if [ -z "$R2_PIDS$OTHER" ]; then DEC=alone
  elif [ $((FREE - NEED)) -ge "$MARGIN_MIB" ]; then DEC=coexist
  elif [ -n "$R2_PIDS" ] && [ -z "$OTHER" ]; then DEC=pause
  else say "⛔ 자리가 모자라고 GPU 에 r2 말고 다른 잡이 있다 — 아무것도 세우지 않는다"; exit 5; fi
fi
case "$DEC" in
  alone)   [ -z "$R2_PIDS$OTHER" ] || { say "⛔ MODE=alone 인데 GPU 에 계산 프로세스가 있다"; exit 5; } ;;
  coexist) [ $((FREE - NEED)) -ge "$MARGIN_MIB" ] || { say "⛔ MODE=coexist 인데 빔 $FREE − need $NEED < 여유 $MARGIN_MIB MiB"; exit 5; } ;;
  pause)   [ -n "$R2_PIDS" ] && [ -z "$OTHER" ] || { say "⛔ MODE=pause 는 GPU 위가 Li₃Nd r2 하나뿐일 때만 (r2:${R2_PIDS:- 없음} · 다른:${OTHER:- 없음})"; exit 5; } ;;
  *) say "⛔ MODE '$DEC' 모름 (auto · alone · coexist · pause)"; exit 5 ;;
esac
say "결정: $DEC$([ "$DEC" = pause ] && echo " — r2 를 다음 BFGS 줄 직후 EXIT 로 세우고 · ELF 혼자 · 끝나면 r2 restart")"
[ "${DRY_RUN:-0}" = 1 ] && { say "DRY_RUN — 여기서 끝 (GPU 계산 0 · r2 손대지 않음)"; exit 0; }

# GPU pw.x 런타임 — 추측하지 않고 ldd 로 묻는다 (tools/doping/run_force_check_scf.sh 와 같은 규칙)
if [ "$SKIP_LDD" != 1 ]; then
  out=$(ldd "$GPU_PW" 2>/dev/null); libmpi=$(echo "$out" | awk '/libmpi\.so/ {print $3; exit}')
  [ -n "$libmpi" ] && [ -f "$libmpi" ] || { say "⛔ GPU pw.x 의 libmpi 를 ldd 로 못 읽었다 — 시작하지 않는다"; exit 7; }
  mprefix=$(dirname "$(dirname "$libmpi")")
  extra=$(echo "$out" | awk '$3 ~ /^\// {print $3}' | xargs -r -n1 dirname | sort -u | tr '\n' ':' | sed 's/:$//')
  # ⚠ 전역 export 하지 않는다 — 뒤의 CPU pp.x 는 시스템 OpenMPI (/usr/bin/mpirun) 라 OPAL_PREFIX 가 hpcx 를 가리키면 깨진다
  GPU_ENV=(OPAL_PREFIX="$mprefix" PATH="$mprefix/bin:$PATH" LD_LIBRARY_PATH="$(dirname "$libmpi"):$extra:${LD_LIBRARY_PATH:-}"
           OMP_NUM_THREADS=1 CUDA_VISIBLE_DEVICES=0 OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1)
  MPIRUN_GPU=$mprefix/bin/mpirun
  [ -x "$MPIRUN_GPU" ] || { say "⛔ $MPIRUN_GPU 없음"; exit 7; }
  say "GPU 런타임 ✓ libmpi $libmpi → $MPIRUN_GPU · OMP 1"
fi

R2_PAUSED=0
resume_r2(){   # → 0 걸었다/필요 없음 · 1 못 걸었다
  local j; j=$(bash "$RESTART_TOOL" "$R2_DIR" 2>&1 9>&- | grep -a "$(basename "$R2_DIR")" | head -1)
  say "r2 판정: $(echo "$j" | tr -s ' ')"
  case "$j" in
    *"사람이 세움"*restart*) ;;
    *수렴*) say "r2 는 수렴 상태 — 다시 걸 것 없음"; return 0 ;;
    *) say "⛔ r2 가 '사람이 세움 → restart' 가 아니다 — 걸지 않는다 (사람이 본다)"; return 1 ;;
  esac
  local s=li3nd_r2_res_$(date +%m%d%H%M)
  "$TMUX_BIN" new -d -s "$s" "bash $RESTART_TOOL --run --nstep $R2_NSTEP $R2_DIR > $OUT/r2_resume.log 2>&1" 9>&- || { say "⛔ tmux 로 r2 재개를 못 띄웠다"; return 1; }
  sleep 5
  "$TMUX_BIN" has-session -t "$s" 2>/dev/null || grep -aq "▶" "$OUT/r2_resume.log" 2>/dev/null \
    || { say "⛔ r2 재개 세션 $s 가 바로 사라졌다 — $OUT/r2_resume.log"; return 1; }
  say "✅ r2 재개 — tmux $s (restart_qe_relax.sh --run --nstep $R2_NSTEP · GPU 여유를 스스로 기다린다) · 로그 $OUT/r2_resume.log"
  return 0
}
finish_fail(){   # $1 = 끝 코드 — pause 였으면 r2 부터 다시 건다
  local rc=$1
  if [ "$R2_PAUSED" = 1 ]; then resume_r2 || { say "⛔⛔ r2 재개 실패 — r2 가 서 있다 · 사람이 바로 본다"; exit 12; }; fi
  exit "$rc"
}

# ④ (pause) r2 세우기 ──────────────────────────────────────────────────────
if [ "$DEC" = pause ]; then
  p=$(echo $R2_PIDS | awk '{print $1}')
  R2_IN=$(tr '\0' '\n' < /proc/$p/cmdline | awk 'f{print; exit} /^-(in|inp|input)$/{f=1}')
  R2_SRC=$(ls -1 "$R2_DIR"/*.in 2>/dev/null | head -1)          # restart_qe_relax.sh 와 같은 규칙: 첫 .in → .out
  R2_OUTB=$(basename "${R2_SRC%.in}.out")
  [ -n "$R2_IN" ] && [ -f "$R2_DIR/$R2_IN" ] && [ -f "$R2_DIR/$R2_OUTB" ] || { say "⛔ r2 입력·출력을 못 정했다 (in '$R2_IN' · out '$R2_OUTB')"; exit 6; }
  say "▶ r2 정지 — pw.x $p · in $R2_IN · out $R2_OUTB · 다음 BFGS 줄 직후 EXIT (최대 ${PAUSE_TIMEOUT} s)"
  bash "$PAUSE_TOOL" --in "$R2_IN" --out "$R2_OUTB" --no_runner --poll "$PAUSE_POLL" --timeout "$PAUSE_TIMEOUT" >> "$LOG" 2>&1 9>&-
  prc=$?
  tail -3 "$LOG" | sed 's/^/   /'
  [ "$prc" = 0 ] || { say "⛔ r2 정지 도구 끝 코드 $prc — ELF 를 안 돌린다 (r2 상태는 정지 도구 로그)"; exit 6; }
  R2_PAUSED=1
  j=$(bash "$RESTART_TOOL" "$R2_DIR" 2>&1 9>&- | grep -a "$(basename "$R2_DIR")" | head -1)
  case "$j" in
    *"사람이 세움"*restart*|*수렴*) say "r2 정지 확인: $(echo "$j" | tr -s ' ')" ;;
    *) say "⛔ 정지 뒤 r2 판정이 '사람이 세움 → restart' 가 아니다: $j — ELF 를 안 돌린다"; R2_PAUSED=0; exit 6 ;;
  esac
  n=0; t3=$(date +%s)
  while [ "$n" -lt "$EMPTY_N" ]; do
    [ $(( $(date +%s) - t3 )) -gt "$EMPTY_MAX" ] && { say "⛔ ${EMPTY_MAX} s 동안 GPU 가 안 비었다 — ELF 를 안 돌린다"; finish_fail 5; }
    if [ -z "$(gpu_pids)" ]; then n=$((n+1)); else n=0; fi
    [ "$n" -lt "$EMPTY_N" ] && sleep "$POLL"
  done
  say "GPU 빔 × $EMPTY_N — ELF SCF 혼자 간다"
fi

# ⑤ SCF (GPU) — ELF 는 OUT 하나 · removal 은 rm_* 여덟 ──────────────────────────
run_scf(){   # $1 = 폴더 → 0 수렴 · 7 실패 · 11 가드
  local d=$1 rc GP=""
  cd "$d" || return 7
  if grep -aq "JOB DONE" scf.out 2>/dev/null && grep -aq "convergence has been achieved" scf.out; then
    say "$(basename "$d"): scf.out 이 이미 끝나 있다 — 생략"; return 0
  fi
  [ -f scf.out ] && mv scf.out "scf.out.$(date +%m%d%H%M%S)"
  say "▶ SCF $(basename "$d") (GPU · $DEC)"
  env "${GPU_ENV[@]}" "$MPIRUN_GPU" --oversubscribe -np 1 "$GPU_PW" -nk 1 -in scf.in > scf.out 2>&1 9>&- &
  local MP=$!
  if [ "$DEC" = coexist ]; then
    ( while kill -0 "$MP" 2>/dev/null; do
        u=$(gpu_used)
        if [ -n "$u" ] && [ "$u" -gt "$GUARD_MIB" ]; then
          echo "[$(date '+%F %T')] ⛔ 가드 — GPU 합계 $u > $GUARD_MIB MiB · 우리 pw.x 만 죽인다" >> "$LOG"
          : > "$OUT/.guard_fired"
          for x in $(pgrep -f -- "-in scf.in" 2>/dev/null); do
            [ "$(readlink -f /proc/$x/cwd 2>/dev/null)" = "$(readlink -f "$d")" ] && kill -KILL "$x" 2>/dev/null
          done
          kill -KILL "$MP" 2>/dev/null; break
        fi
        sleep 10
      done ) 9>&- &
    GP=$!
  fi
  wait "$MP"; rc=$?
  [ -n "$GP" ] && { kill "$GP" 2>/dev/null; wait "$GP" 2>/dev/null; }
  if [ -e "$OUT/.guard_fired" ]; then rm -f "$OUT/.guard_fired"; say "⛔ 공존 가드 발동 — 우리 SCF 만 죽였다 · MODE=pause 로 다시"; return 11; fi
  if grep -aq "convergence has been achieved" scf.out && grep -aq "JOB DONE" scf.out; then
    say "SCF ✓ $(basename "$d") $(grep -a '^!' scf.out | tail -1 | tr -s ' ') · 반복 $(grep -a 'convergence has been achieved' scf.out | tail -1 | grep -oE '[0-9]+ iterations') · $(grep -a 'PWSCF.*WALL' scf.out | tail -1 | tr -s ' ')"
    return 0
  fi
  say "⛔ SCF $(basename "$d") rc=$rc · 수렴/JOB DONE 없음 — scf.out 끝:"; tail -5 scf.out | tee -a "$LOG"; return 7
}
if [ "$JOB" = removal ]; then
  for d in $RM_DIRS; do
    run_scf "$d"; r=$?
    [ "$r" = 11 ] && exit 11
    if [ "$r" != 0 ]; then say "↻ $(basename "$d") 같은 입력으로 한 번 다시"; run_scf "$d"; r=$?; [ "$r" = 11 ] && exit 11; fi
    [ "$r" = 0 ] || { say "⛔ $(basename "$d") 두 번 실패 — 남은 점을 멈춘다"; finish_fail 7; }
  done
  cd "$OUT" || finish_fail 7
else
  run_scf "$OUT"; r=$?
  [ "$r" = 11 ] && exit 11
  [ "$r" = 0 ] || finish_fail 7
fi
if [ "$R2_PAUSED" = 1 ]; then
  resume_r2 || { say "⛔⛔ r2 재개 실패 — r2 가 서 있다 · 사람이 바로 본다 (뒤 처리는 계속한다)"; R2_FAIL=1; }
  R2_PAUSED=0
fi

# ⑥ pp.x ELF (CPU 후처리 · 계산 아님) ────────────────────────────────────────
if [ "$JOB" = elf ]; then
if [ ! -s nd_elf_nc.cube ]; then
  cat > pp_elf.in <<EOF
&INPUTPP
  prefix='nd_elf_nc', outdir='./tmp', plot_num=8, filplot='./nd_elf_pl'
/
&PLOT
  iflag=3, output_format=6, fileout='nd_elf_nc.cube'
/
EOF
  say "▶ pp.x plot_num=8 (ELF · CPU ${NP_PP} 랭크 · save 읽기만)"
  OMP_NUM_THREADS=1 "$MPIRUN_CPU" --allow-run-as-root --bind-to none --mca btl self,vader -np "$NP_PP" "$CPU_BIN/pp.x" -in pp_elf.in > pp_elf.out 2>&1 9>&-
  rc=$?
  [ "$rc" = 0 ] && [ -s nd_elf_nc.cube ] || { say "⛔ pp.x rc=$rc 또는 cube 없음 — pp_elf.out"; exit 8; }
fi
say "pp.x ✓ nd_elf_nc.cube $(du -h nd_elf_nc.cube | cut -f1)"

# ⑦ 결합 중점 표본 (호스트 표와 같은 도구) · gap ────────────────────────────────
"$PY" "$SAMPLER" --cube nd_elf_nc.cube --system Nd_at_Li_newPP_NC --out nd_elf_bonds.csv 2>&1 9>&- | tee -a "$LOG"
[ "${PIPESTATUS[0]}" = 0 ] && [ -s nd_elf_bonds.csv ] || { say "⛔ 표본 실패"; exit 9; }
"$PY" - scf.out <<'PY' 2>&1 | tee -a "$LOG"
import re, sys
t = open(sys.argv[1], errors="replace").read()
ef = re.findall(r"the Fermi energy is\s+(-?[\d.]+)\s+ev", t)
blocks = re.findall(r"bands \(ev\):\s*\n(.*?)(?:\n\s*\n\s*(?:k =|occupation numbers|the Fermi))", t, re.S)
ev = [float(x) for b in blocks for x in re.findall(r"-?\d+\.\d+", b)]
if not ef or not ev:
    print("gap: 고유값 · E_F 를 못 읽었다"); sys.exit(0)
e = float(ef[-1]); vb = max(x for x in ev if x <= e); cb = min((x for x in ev if x > e), default=float("nan"))
print(f"gap: E_F {e:.4f} eV · 최고 점유 {vb:.4f} · 최저 빈 {cb:.4f} → {cb - vb:.3f} eV (k {len(blocks)} 블록 · smearing mv 0.01 Ry = 0.136 eV 와 비교)")
PY
fi

# ⑧ 기록 · 끝 줄 → 해시 ───────────────────────────────────────────────────────
git -C "$REPO" rev-parse HEAD > SOURCE_COMMIT 2>/dev/null || echo unknown > SOURCE_COMMIT
RC_END=0; [ -n "${R2_FAIL:-}" ] && RC_END=12
say "■ 끝 · 끝 코드 $RC_END$([ "$RC_END" = 12 ] && echo ' (계산은 끝 · ⛔ r2 재개 실패 — 사람이 바로 본다)') · 결정 $DEC"
find . -maxdepth 1 -type f ! -name '.lock' ! -name SHA256SUMS ! -name 'nd_elf_pl' ! -name '*.cube' -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS
[ "$JOB" = removal ] && find . -mindepth 2 -maxdepth 2 -path './rm_*' -type f \( -name scf.in -o -name scf.out \) -print0 | sort -z | xargs -0 sha256sum >> SHA256SUMS
[ -d pseudo ] && ( cd pseudo && sha256sum * ) | sed 's#  #  ./pseudo/#' >> SHA256SUMS
[ -f probe/probe.out ] && sha256sum probe/probe.out | sed 's#  probe/#  ./probe/#' >> SHA256SUMS
echo "SHA256SUMS $(wc -l < SHA256SUMS) 줄 (회수: $([ "$JOB" = removal ] && echo 'rm_*/scf.in · rm_*/scf.out · MANIFEST.json' || echo 'scf.in · scf.out · pp_elf.* · nd_elf_bonds.csv') · run.log · probe/probe.out · SOURCE_COMMIT)"
exit "$RC_END"
