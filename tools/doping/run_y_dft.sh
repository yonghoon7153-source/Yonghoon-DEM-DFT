#!/usr/bin/env bash
# run_y_dft.sh — Y 자리선호 DFT 대조: 기저 5상 + 타깃 2개를 **순차** 실행.
#
# 설계 이유
#   · **작은 상을 먼저** 돈다. pseudo·설정 문제라면 몇 분 만에 드러난다 —
#     100/108 원자를 몇 시간 돌리고 나서 알면 그 시간을 버린다.
#   · **순차**로 돈다. 동시에 띄우면 메모리가 예측 불가능하고, 어느 것이
#     터졌는지도 흐려진다.
#   · **장치는 바이너리로 고른다.** PWX 를 CPU 빌드로 주면 CPU, GPU 빌드로 주면
#     GPU 다. 별도 스위치를 두면 "GPU 빌드인데 CPU 모드" 같은 모순 조합이 생긴다.
#     ⚠ GPU 빌드를 쓸 때는 nvidia-smi 로 여유를 먼저 본다 (CLAUDE.md: pw.x ↔ UMA).
#
# ⛔ 이 스크립트가 못 하는 것
#   · 결과를 해석하지 않는다. 끝나면 dft_decomp_check.py --collect 를 돌려라.
#   · 수렴을 보장하지 않는다. relax 가 nstep 에서 끊기면 그 값은 바닥이 아니다
#     — --collect 가 마지막 총에너지를 쓰므로 **수렴 여부를 사람이 봐야 한다**.
#   · 중단된 계산을 이어받지 않는다. 지우고 다시 돌린다.
#
# 사용:
#   nohup bash tools/doping/run_y_dft.sh > /data/work/runs/y_dft/run.log 2>&1 &
#   NP=1 OMP_NUM_THREADS=8 PWX=~/apps/qe-7.4.1-gpu/bin/pw.x \
#       bash tools/doping/run_y_dft.sh                    # GPU 빌드
set -u
set +H

D="${D:-/data/work/runs/y_dft}"
NP="${NP:-$(( $(nproc) > 4 ? $(nproc) - 2 : 1 ))}"
PWX="${PWX:-pw.x}"

# ── 중복 실행 가드 (캠페인 관례) ──────────────────────────────────────────
#   ⛔ pgrep -fc 로 세면 **자기 자신을 두 번 센다**: $( ) 서브셸은 exec 전까지
#     부모 bash 와 같은 cmdline 을 갖는다. 실측으로 오탐 확인(2026-08-26).
#     flock 은 그런 함정이 없다 — 커널이 잠금을 관리한다.
LOCK="${LOCK:-/tmp/run_y_dft.lock}"
exec 9>"$LOCK" || { echo "⛔ 잠금 파일을 못 연다: $LOCK"; exit 1; }
if ! flock -n 9; then
  echo "⛔ 이미 돌고 있다 (잠금 $LOCK). 중복 실행 중단."
  exit 1
fi

command -v "$PWX" >/dev/null || { echo "⛔ $PWX 가 없다"; exit 1; }
# QE 가 CPU 빌드면 GPU 충돌 걱정이 없다 — 그 사실을 화면에 남긴다
IS_GPU=0
if command -v ldd >/dev/null && ldd "$(command -v "$PWX")" 2>/dev/null | grep -qi "libcud"; then
  IS_GPU=1
  QEKIND="GPU 빌드 ⚠ 다른 GPU 런과 VRAM 을 나눠 쓴다"
else
  QEKIND="CPU 빌드 ✅ GPU 를 안 건드린다"
fi

# ⛔ GPU 빌드에 랭크를 많이 주면 **랭크마다 GPU 컨텍스트를 잡아** 바로 OOM 이다.
#   QE 관례는 **GPU 1개당 MPI 랭크 1개** + OpenMP 로 코어를 쓴다.
#   이걸 모르고 CPU 때처럼 -np 12 를 주면 옆에서 도는 MD 까지 같이 죽는다.
if [ "$IS_GPU" = "1" ] && [ "$NP" -gt 1 ]; then
  NGPU=$(nvidia-smi --list-gpus 2>/dev/null | wc -l)
  if [ "$NP" -gt "${NGPU:-1}" ]; then
    echo "⛔ GPU 빌드인데 NP=$NP 다 (GPU ${NGPU:-1}개)."
    echo "   랭크마다 GPU 컨텍스트를 잡아 VRAM 이 터지고, **옆에서 도는 런까지 죽는다.**"
    echo "   → NP=${NGPU:-1} 로 두고 코어는 OMP_NUM_THREADS 로 쓴다:"
    echo "     NP=${NGPU:-1} OMP_NUM_THREADS=8 PWX=$PWX bash \$0"
    echo "   정말 여러 랭크로 돌리려면 ALLOW_MULTIRANK_GPU=1 를 준다."
    [ "${ALLOW_MULTIRANK_GPU:-0}" = "1" ] || exit 1
  fi
fi

# GPU 빌드면 시작 전 VRAM 여유를 남긴다 — 나중에 OOM 이 나면 이 줄이 근거가 된다
if [ "$IS_GPU" = "1" ]; then
  nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader \
    | awk -F, '{u=$1;t=$2;gsub(/[^0-9]/,"",u);gsub(/[^0-9]/,"",t);
        printf "VRAM : %s/%s MiB 사용 · 여유 %d MiB (시작 시점)\n",u,t,t-u}'
fi
# ⛔ OpenMP 를 안 묶으면 mpirun 랭크마다 스레드를 다 잡아 코어를 초과 구독한다
export OMP_NUM_THREADS="${OMP_NUM_THREADS:-1}"

# ⛔ **mpirun 을 무조건 쓰면 안 된다.** QE 가 serial 빌드면 mpirun -np N 이
#   같은 계산을 N 번 통째로 돌리며 같은 파일에 동시에 쓴다 — 조용히 깨지거나
#   즉시 죽는다. 빌드가 MPI 를 쓰는지 **확인하고** 정한다 (2026-08-26 kgy 실측).
HAS_MPI=0
if command -v ldd >/dev/null && ldd "$(command -v "$PWX")" 2>/dev/null \
   | grep -qiE "libmpi|libmpich|libopenmpi"; then HAS_MPI=1; fi
if [ "$HAS_MPI" = "1" ] && command -v mpirun >/dev/null && [ "$NP" -gt 1 ]; then
  LAUNCH="mpirun -np $NP"
  MPIKIND="MPI 빌드 · mpirun -np $NP"
else
  LAUNCH=""
  if [ "$NP" -gt 1 ]; then
    if [ "$HAS_MPI" = "0" ]; then
      MPIKIND="⚠ **serial 빌드다** — NP=$NP 를 무시하고 단일 프로세스로 돈다"
    else
      MPIKIND="⚠ mpirun 이 PATH 에 없다 — 단일 프로세스로 돈다"
    fi
    MPIKIND="$MPIKIND (코어는 OMP_NUM_THREADS 로 쓸 것)"
  else
    MPIKIND="단일 프로세스 (NP=1)"
  fi
fi
echo "════════ $(date '+%F %T') Y DFT 대조 ════════"
echo "pw.x : $(command -v "$PWX")"
echo "NP   : $NP   (OMP_NUM_THREADS=$OMP_NUM_THREADS)"
echo "빌드 : $QEKIND"
echo "병렬 : $MPIKIND"
# ⛔ **바이너리 선택이 곧 장치 선택이다.** GPU 빌드인데 CUDA_VISIBLE_DEVICES 를
#   비우면 pw.x 가 장치를 못 찾아 죽거나 조용히 이상하게 돈다. 초판이 그랬다.
if [ "$IS_GPU" = "1" ]; then
  echo "장치 : GPU (GPU 빌드를 골랐으므로) — 옆 런과 VRAM 을 나눠 쓴다"
else
  export CUDA_VISIBLE_DEVICES=""
  echo "장치 : CPU (CUDA_VISIBLE_DEVICES 비움) — 옆의 GPU 런을 건드리지 않는다"
fi

cd "$D" || { echo "⛔ $D 없음"; exit 1; }

# ★ 작은 상 먼저, 큰 타깃 나중 — 실패를 싸게 발견한다
ORDER="LiCl Li2S LiYS2 Li3PO4 Li3PS4 sc_Li_24g_perm00 sc_P_4b_perm03"

for name in $ORDER; do
  IN="in/${name}.in"
  OUT="${name}.out"
  [ -f "$IN" ] || { echo "  ⛔ $IN 없음 — 건너뜀"; continue; }
  if grep -aq "JOB DONE" "$OUT" 2>/dev/null; then
    echo "  · $name 이미 끝남 (JOB DONE) — 건너뜀"
    continue
  fi
  NAT=$(grep -a "nat" "$IN" | head -1 | grep -oE '[0-9]+')
  echo ""
  echo "──▶ $name  (nat ${NAT:-?})  $(date '+%T')"
  T0=$(date +%s)
  $LAUNCH "$PWX" -in "$IN" > "$OUT" 2>&1
  RC=$?
  T1=$(date +%s)
  DT=$(( T1 - T0 ))

  if grep -aq "JOB DONE" "$OUT"; then
    E=$(grep -a "^!" "$OUT" | tail -1 | awk '{print $5}')
    # relax 가 수렴했나 — 안 했으면 마지막 에너지는 바닥이 아니다
    if grep -aq "End of BFGS Geometry Optimization" "$OUT"; then
      CONV="✅ BFGS 수렴"
    elif grep -aq "End of self-consistent calculation" "$OUT" \
         && ! grep -aq "bfgs" "$OUT"; then
      CONV="· scf (기하는 UMA 가 정한 것)"
    elif grep -aq "bfgs" "$OUT"; then
      CONV="⚠ **BFGS 미수렴** — 이 에너지는 바닥이 아니다"
    else
      CONV="⚠ 수렴 표시를 못 찾았다 — 출력을 직접 볼 것"
    fi
    printf "    끝  %5ds  E = %s Ry   %s\n" "$DT" "${E:-?}" "$CONV"
  else
    echo "    ⛔ 실패 (rc=$RC, ${DT}s). 마지막 줄:"
    tail -5 "$OUT" | sed 's/^/       /'
    echo "    ⛔ **여기서 멈춘다** — 뒤 계산을 돌려봤자 --collect 가 거부한다."
    exit 2
  fi
done

echo ""
echo "════════ 전부 끝 $(date '+%F %T') ════════"
echo "다음: python3 tools/doping/dft_decomp_check.py --collect --out $D"
