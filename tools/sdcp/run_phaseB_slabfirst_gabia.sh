#!/usr/bin/env bash
# =============================================================================
# run_phaseB_slabfirst_gabia.sh — SDCP Phase-B 를 **슬랩부터** 다시 세운다.
#
# 왜 순서를 뒤집나
#   지난 판은 131원자 복합체를 FSM(tot_magnetization)+AFM+U 로 바로 때렸다.
#   FSM 은 전 셀 N↑−N↓ 만 묶을 뿐 **홀전자가 어디 앉을지는 못 정하면서**
#   Ni 부격자 이완과는 싸운다 — 그게 sloshing 의 원인이다 (전례: 슬랩이 scf-iter
#   148 에서 accuracy 1.6 Ry 로 정체). 그래서:
#
#     1단계  96원자 **슬랩만** 수렴 (싸다: 복합체의 ~1/3 비용)
#              → 나오는 것: Ni1/Ni2 수렴 모멘트 + 이 셀에서 먹히는 degauss/mixing
#     2단계  그 시드를 넣고 complex_neutral · complex_doped (+ 가스 2개)
#
#   ⚠ **슬랩 1회가 neutral·doped 양쪽에 다 쓰인다.** 두 복합체의 슬랩 부분은
#     완전히 같다 (Li24 Ni24 O48, 같은 셀, 슬랩 원자 전부 고정). 그래서 1단계는
#     한 번만 돌면 되고, 결과는 두 갈래에 그대로 간다.
#   ⚠ **"밀도 승계"는 QE 에서 불가능하다.** 슬랩 96 vs 복합체 130/131 — nat/ntyp 이
#     달라 charge density restart 가 안 된다. 넘어가는 건 **스칼라 시드값**뿐이다.
#
#   양쪽이 갈리는 지점은 딱 하나: tot_magnetization.
#     slab 0.0 · complex_neutral 0.0  → 그냥 뺀다 (AFM 자유이완)
#     complex_doped 1.0               → 물리 의도가 있다(홀전자 1개). 구속 대신
#                                       **자리를 직접 찍는다** (--seed_radical S:0.5).
#     이 계의 라디칼은 sulfonic acid 의 O–H 가 빠진 자리 = –SO3• 다
#     (neutral 은 O98–H 0.99 Å, doped 는 S–O 셋이 전부 1.48 Å 로 이미 비편재).
#     수렴 후 총 자화가 ~1 μB 인지 **반드시 검증**하고, 아니면 그때 FSM 을 되살린다.
#
#   cd ~/Yonghoon-DEM-DFT && git pull
#   tmux new -s pbslab -d 'bash tools/sdcp/run_phaseB_slabfirst_gabia.sh 2>&1 | \
#       tee -a /data/work/runs/sdcp_linio2_binding/pbslabfirst.log'
#
# ⚠ pw.x — GPU 에 UMA/다른 pw.x 가 없을 때만. 아래 가드가 먼저 확인한다.
# ⚠ CPU-빌드 QE 와 GPU-빌드 QE 는 **호스트 RAM 을 공유**한다 (2026-07-29 OOM 교훈:
#   20 rank × 1.4 GB + SDCP 26.7 GB > 62 GB → 커널이 SDCP 를 죽였다).
#   여기선 ELF/Bader 류 CPU 작업이 없는지도 같이 본다.
# =============================================================================
set -u; set +H
STAGE=${1:-all}          # all | slab | complexes
BASE=/data/work/runs/sdcp_linio2_binding
REPO=${REPO:-$HOME/Yonghoon-DEM-DFT}; [ -d "$REPO" ] || REPO=$HOME/work/Yonghoon-DEM-DFT
OUT=$BASE/phaseB_v7c_slabfirst
SCAN=$BASE/phaseA_v7c_tallvac
UMA_PY=$(ls /data/apps/miniforge3/envs/uma/bin/python3 2>/dev/null || which python3)
MAGJSON=$OUT/slab_mag.json
mkdir -p "$OUT"
ts(){ echo "[$(date +%m-%d\ %H:%M:%S)] $*"; }
_banner(){ ts "설정: stage=$STAGE · degauss=$DEGAUSS · mixing_ndim=$MIXNDIM · maxstep=$MAXSTEP · scf_must_converge=$SCF_MUST · tprnfor=$TPRNFOR"
           ts "      밀도승계 RESTART=$RESTART $([ "$RESTART" = 1 ] && echo '(켜짐 — 기본)' || echo '(꺼짐)')"; }

# ── 중복 실행 가드 ──────────────────────────────────────────────────────────
# ⚠⚠ **pgrep 로 세면 안 된다.** `pgrep -fc "[b]ash.*$SELF"` 는 자기 자신뿐 아니라
#   tmux 가 끼워 넣는 래퍼(`sh -c 'bash ... | tee ...'`)까지 센다 — 실측 count=4.
#   그래서 `-gt 1` 이 항상 참이 되어 **스크립트가 시작하자마자 죽었다** (2026-07-30,
#   tmux 세션이 목록에 아예 안 뜨는 걸로 발각). 대괄호 트릭도 이건 못 막는다.
#   flock 은 PID 를 안 세고 커널이 배타를 보장하므로 이 함정 자체가 없다.
LOCK=${LOCK:-/tmp/pbslabfirst.lock}
exec 9>"$LOCK" || { ts "⛔ 락 파일을 못 연다: $LOCK"; exit 1; }
if command -v flock >/dev/null 2>&1; then
  flock -n 9 || { ts "⛔ 이미 돈다 (flock $LOCK) — 중복 실행 중단"; exit 1; }
else
  ts "⚠ flock 없음 — 중복 실행 가드 없이 진행한다"
fi

# ── env ─────────────────────────────────────────────────────────────────────
HPCX=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi
export PATH=$HPCX/bin:$PATH
export LD_LIBRARY_PATH=$HPCX/lib:/data/apps/nvhpc/Linux_x86_64/24.11/compilers/lib:/usr/local/cuda-12.6/lib64:${LD_LIBRARY_PATH:-}
export OPAL_PREFIX=$HPCX OMP_NUM_THREADS=1 CUDA_VISIBLE_DEVICES=0
export OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
QE=/data/apps/qe-7.4.1-gpu/bin/pw.x
MPIRUN=$HPCX/bin/mpirun

# ── GPU/RAM 가드 ────────────────────────────────────────────────────────────
guard(){
  local used free_gb
  used=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits 2>/dev/null | head -1)
  ts "GPU 사용 ${used:-?} MiB"
  if [ "${used:-0}" -gt 4000 ]; then
    ts "⛔ GPU 에 이미 ${used} MiB 가 올라가 있다 (UMA? 다른 pw.x?) — 중단."
    nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv 2>/dev/null
    exit 1
  fi
  free_gb=$(free -g | awk '/^Mem:/{print $7}')
  ts "호스트 여유 RAM ${free_gb} GB"
  if [ "${free_gb:-0}" -lt 20 ]; then
    ts "⚠ 여유 RAM ${free_gb} GB — CPU-빌드 QE(ELF/Bader) 가 돌고 있는지 확인하라."
    pgrep -a -f "pw\.x|pp\.x|bader" | head -5
  fi
}

# ── 입력 생성 ───────────────────────────────────────────────────────────────
# ⚠ degauss 는 doped/neutral **양쪽 같은 값**이어야 한다. 다르면 E_bind 차분에
#   smearing 항이 상쇄되지 않아 verdict 가 오염된다.
# ⚠⚠ **degauss 를 0.02 로 좁힌 건 판단 착오였다 (2026-07-30 정정).**
#   scf_u62.in 에서 클론한 검증된 값은 **0.03** 인데 "좁을수록 정확"이라는 생각으로
#   0.02 로 낮췄다. 그런데 금속성 Ni 표면에서 좁은 스미어링은 E_F 근처 점유수를 매 반복
#   바꿔 **limit cycle** 을 만든다. 실측: 슬랩이 초반 0.024 자릿수/iter 로 5자릿수를
#   내려가다가 0.02 Ry 근처에서 감속(0.0012)하고 진동률 53% 로 갇혔다.
#   자화는 그동안 완전히 안정(abs mag 110.36±0.05, total −0.08)이라 **스핀 문제가 아니다.**
#   검증된 0.03 으로 되돌린다. doped/neutral 양쪽 같은 값이면 E_bind 차분에서 상쇄된다.
DEGAUSS=${DEGAUSS:-0.03}
MAXSTEP=${MAXSTEP:-300}
# 진동(limit cycle)에는 Broyden 이력을 **줄이는** 쪽이 듣는다 — 긴 이력이 진동을 고착시킨다.
MIXNDIM=${MIXNDIM:-8}
# per-site 자화를 매 반복 찍는다 — 미수렴으로 끝나도 시드를 건지기 위해 (필수)
REPORT=${REPORT:-1}
# ⚠⚠ **scf_must_converge 가 시드 수확을 막는다 (2026-08-02 실측).**
#   .true. 면 미수렴 시 QE 가 **그 자리에서 abort** 해서 최종 출력에 도달하지 못한다.
#   per-site 자화 블록은 그 최종 출력에 있으므로 report=1 을 켜도 안 나온다
#   (실제로 안 나왔다 — "시드도 못 건졌다"). 반대로 .false. 면 "convergence NOT achieved"
#   를 찍고도 **끝까지 진행해 자화 블록을 남긴다.**
#   → 시드 수확 런에서는 .false. 로 둔다. 가짜 수렴 위험은 없다:
#     우리는 이 런의 **에너지를 안 쓰고** 자화만 가져가며, plateau 는 이미 문서화돼 있다.
#   ⚠ 본 계산(복합체)에서는 .true. 를 유지한다 — 거기선 에너지가 결과다.
SCF_MUST=${SCF_MUST:-.true.}
# ⚠⚠ **plateau 수용 (2026-08-01).** 이 슬랩은 특정 값 근처에서 limit cycle 로 갇힌다.
#   degauss 0.05 판(옛 등록본) acc_end 6.2e-3 · degauss 0.03 판 5.0e-3 —
#   **넓혀도 안 잡히고, 우리 값이 이미 선례보다 낫다.** 즉 plateau 는 이 계의 정상 거동이다.
#   그리고 우리가 슬랩에서 원하는 건 에너지가 아니라 **Ni 시드**이고, verdict 에서는
#   슬랩이 통째로 상쇄된다. 그래서 미수렴이어도 시드가 멀쩡하면 2단계로 간다.
#   (db 에 이미 "Plateau convention" 선례가 있다 — sdcp_v7c_phaseB_energies.csv)
PLATEAU_OK=${PLATEAU_OK:-1}
# ⚠⚠ **힘 계산을 끈다 (2026-08-03 실측).** 슬랩이 SCF 30 iter 로 수렴한 뒤
#   `negative rho` 줄에서 멈춰 보였는데, 실은 죽은 게 아니라 **tprnfor 힘 항**을
#   35분+ 100% 로 돌고 있었다(elapsed 1h48m, JOB DONE 0). PAW+U 힘은 이 GPU 빌드에서
#   극단적으로 느리다. 우리 경로는 전부 단일점 scf 이고 E_bind = 총에너지 차분이라
#   **힘을 아무 데서도 안 쓴다** → 끄는 게 순이득. 130/131 원자면 손해가 더 크다.
TPRNFOR=${TPRNFOR:-.false.}
# ⚠⚠ **기본값이 1 이다 (2026-07-31 변경).** 이전 charge density 가 있으면 쓰는 게
#   언제나 이득인데, 기본을 0 으로 두었다가 두 번 연속 그냥 시작해서 각각 8시간을 버렸다.
#   원인은 tmux 가 **서버-클라이언트 구조**라는 것: `RESTART=1 tmux new -d '...'` 로는
#   변수가 새 세션 쉘에 안 넘어간다(tmux 서버의 환경을 쓴다). 넘기려면 따옴표 **안쪽**에
#   넣거나 `tmux new -e RESTART=1` 을 써야 한다 — 실수하기 너무 쉬운 구조다.
#   그래서 **기본을 켜 두고**, 정말 처음부터 돌고 싶을 때만 RESTART=0 을 준다.
#   밀도가 없는 job 은 run_one 이 알아서 건너뛰므로 켜 두어 손해 볼 일이 없다.
#   ⚠ restart_mode='restart' 가 아니라 startingpot='file' 이다 — 전자는 wfc 까지 이어받는
#     '중단 재개'라 disk_io='low' 와 충돌한다. 우리가 원하는 건 **밀도만** 승계.
RESTART=${RESTART:-1}
_banner

gen(){   # $1 = "slab" | "complexes"
  local extra=()
  # ⚠⚠ **startingpot 을 여기서(전 job 공통으로) 붙이면 안 된다.** gen 은 5개 입력을
  #   한 번에 만드는데, 밀도가 있는 job 은 slab 뿐이고 complex_* / mol_* 은 없다.
  #   공통으로 붙이면 2단계에서 QE 가 '없는 파일을 읽어라'로 죽는다.
  #   → 승계는 **run_one 에서 그 job 의 tmp 를 직접 보고** 넣는다.
  [ -s "$MAGJSON" ] && extra+=(--mag_json "$MAGJSON")
  "$UMA_PY" "$REPO/tools/sdcp/phaseB_v7c_dft_binding.py" \
    --slab "$OUT/slab_cshrink.vasp" \
    --complex_doped   "$SCAN/complex_doped_sulfonate_down_r90.xyz" \
    --complex_neutral "$SCAN/complex_neutral_chelation_r0.xyz" \
    --mol_doped   "$BASE/inputs/sdcp_v7c/sdcp_v7c_doped.xyz" \
    --mol_neutral "$BASE/inputs/sdcp_v7c/sdcp_v7c_neutral.xyz" \
    --ref_scf     "$BASE/reference_dft_v2/scf_u62.in" \
    --afm_mode inplane --mol_vacuum 8 --pseudo_dir /data/work/pseudo \
    --no_fsm --degauss "$DEGAUSS" --scf_must_converge "$SCF_MUST" \
    --electron_maxstep "$MAXSTEP" --seed_radical S:0.5 --mixing_ndim "$MIXNDIM" \
    --report "$REPORT" --tprnfor "$TPRNFOR" \
    ${extra[@]+"${extra[@]}"} --out "$OUT" || return 1
  # OOM 대책은 refine 판과 동일: 단일-k + david_ndim 2
  for j in slab complex_doped complex_neutral; do
    grep -aq diago_david_ndim "$OUT/$j/scf.in" || \
      sed -i '/&ELECTRONS/a\    diago_david_ndim = 2' "$OUT/$j/scf.in"
    sed -i 's/^\s*2 2 1 0 0 0/  1 1 1 0 0 0/' "$OUT/$j/scf.in"
  done
}

# c 축소 슬랩 (refine 판의 c=6.5 Å 간격 판정을 그대로 승계)
if [ ! -s "$OUT/slab_cshrink.vasp" ]; then
  ZMAX=$("$UMA_PY" - "$SCAN" <<'PYZ'
import sys
scan = sys.argv[1]; zmax = 0.0
for tag in ("complex_doped_sulfonate_down_r90", "complex_neutral_chelation_r0"):
    ls = open(f"{scan}/{tag}.xyz").read().split("\n")
    zmax = max(zmax, max(float(l.split()[3]) for l in ls[2:2 + int(ls[0])]))
print(f"{zmax:.2f}")
PYZ
) || { ts "pose zmax 계산 실패"; exit 1; }
  C=$(awk -v z="$ZMAX" 'BEGIN{printf "%.3f", z + 6.5}')
  ts "pose zmax=$ZMAX Å → c=$C Å (이미지 간격 6.5 Å)"
  "$UMA_PY" - "$REPO/db/structures/sdcp_phaseB_slab_c40.vasp" "$OUT/slab_cshrink.vasp" "$C" <<'PYC'
import sys
vasp, out, c_new = sys.argv[1], sys.argv[2], float(sys.argv[3])
lines = open(vasp).read().splitlines()
assert "Cartesian" in lines[7], "expect Cartesian POSCAR"
lines[4] = f"      0.000000000000     0.000000000000    {c_new:.9f}"
open(out, "w").write("\n".join(lines) + "\n")
PYC
fi

run_one(){   # $1 = job dir name, $2 = -nk pools
  local j=$1 nk=${2:-1}
  [ -s "$OUT/$j/scf.in" ] || { ts "⛔ $OUT/$j/scf.in 없음"; return 1; }
  if grep -aq "convergence has been achieved" "$OUT/$j/scf.out" 2>/dev/null; then
    ts "✓ $j 이미 수렴 — 건너뜀"; return 0
  fi
  # ── 밀도 승계: **이 job 자신의** charge-density 가 있을 때만 주입 ─────
  if [ "$RESTART" = 1 ]; then
    if ls "$OUT/$j"/tmp/*.save/charge-density* >/dev/null 2>&1; then
      grep -aq "startingpot" "$OUT/$j/scf.in" || \
        sed -i "/&ELECTRONS/a\    startingpot     = 'file'" "$OUT/$j/scf.in"
      ts "↻ $j 밀도 승계 (startingpot='file', maxstep $MAXSTEP)"
    else
      ts "· $j 이전 밀도 없음 — 처음부터 (정상: 이 job 은 처음 도는 것)"
    fi
  fi
  guard
  # ⚠ 이전 scf.out 을 덮어쓰면 **accuracy 궤적이 사라진다.** 진단(doctor)이 그걸 먹고 산다.
  [ -s "$OUT/$j/scf.out" ] && mv "$OUT/$j/scf.out" "$OUT/$j/scf.out.$(date +%m%d_%H%M)"
  ts "▶ $j 시작 (-nk $nk)"
  ( cd "$OUT/$j" && $MPIRUN -np 1 --oversubscribe "$QE" -nk "$nk" -in scf.in > scf.out 2>&1 )
  if grep -aq "convergence has been achieved" "$OUT/$j/scf.out"; then
    ts "✓ $j 수렴 — $(grep -a '!.*total energy' "$OUT/$j/scf.out" | tail -1)"
  else
    ts "✗ $j 미수렴 — 진단:"
    "$UMA_PY" "$REPO/tools/sdcp/scf_convergence_doctor.py" \
        --scf_out "$OUT/$j/scf.out" --scf_in "$OUT/$j/scf.in" 2>&1 | tail -22
    return 1
  fi
}

# ── 1단계: 슬랩 ─────────────────────────────────────────────────────────────
if [ "$STAGE" = all ] || [ "$STAGE" = slab ]; then
  ts "═══ 1단계: 96원자 슬랩 (neutral·doped 공용) ═══"
  gen slab || { ts "입력 생성 실패"; exit 1; }
  if ! run_one slab 1; then
    if [ "$PLATEAU_OK" = 1 ] && grep -aq "Magnetic moment per site" "$OUT/slab/scf.out"; then
      ts "⚠ 슬랩 미수렴(plateau) — 그러나 per-site 자화가 있으므로 **시드만 뽑아 진행**한다."
      ts "   acc_end: $(grep -a 'estimated scf accuracy' "$OUT/slab/scf.out" | tail -1)"
      ts "   ⚠ 이 슬랩 **에너지**는 plateau 값이다 — 절대 E_bind 인용 시 오차막대 필수."
    else
      ts "슬랩이 안 수렴했고 **시드도 못 건졌다** — 여기서 멈춘다."
      ts "   → per-site 자화 블록이 없다. scf_must_converge=.true. 면 QE 가 미수렴 시"
      ts "     abort 해서 최종 출력에 도달하지 못한다. 시드 수확은 이렇게:"
      ts "     SCF_MUST=.false. MAXSTEP=30 bash tools/sdcp/run_phaseB_slabfirst_gabia.sh slab"
      exit 1
    fi
  fi
  "$UMA_PY" "$REPO/tools/sdcp/slab_mag_from_scfout.py" \
      --scf_out "$OUT/slab/scf.out" --scf_in "$OUT/slab/scf.in" --out "$MAGJSON" || exit 1
fi

# ── 2단계: 복합체 + 가스 ────────────────────────────────────────────────────
if [ "$STAGE" = all ] || [ "$STAGE" = complexes ]; then
  # ⚠ 시드는 **결과가 아니라 초기 추측**이다. 관례값 ±0.3 도 이미 합리적 범위고,
  #   슬랩에서 absolute magnetization 이 110.94 μB 로 안정(상대폭 0.05%)인 것으로
  #   "AFM 이 유지된다"는 확인은 이미 끝났다. per-site 블록 확보가 계속 비싸지면
  #   **시드 없이 진행하는 게 합리적**이다 — 1단계의 진짜 소득(레시피 검증:
  #   degauss 0.03 · ndim 8 · 밀도승계 → 5e-3, plateau 가 정상)은 이미 챙겼다.
  #   NO_SEED=1 로 그 판단을 명시적으로 내린다.
  if [ ! -s "$MAGJSON" ]; then
    if [ "${NO_SEED:-0}" = 1 ]; then
      ts "⚠ 시드 없이 진행한다 (NO_SEED=1) — starting_magnetization 은 관례 ±0.3."
      ts "   1단계에서 얻은 것: degauss $DEGAUSS · mixing_ndim $MIXNDIM · plateau 규약."
    else
      ts "⛔ $MAGJSON 이 없다 — 1단계를 먼저 돌리거나, 시드를 포기하려면 NO_SEED=1."
      exit 1
    fi
  fi
  ts "═══ 2단계: 복합체 ($([ -s "$MAGJSON" ] && cat "$MAGJSON" | tr -d '\n ' || echo '시드 없음 — 관례 ±0.3')) ═══"
  gen complexes || { ts "입력 재생성 실패"; exit 1; }
  for j in mol_neutral mol_doped complex_neutral complex_doped; do
    run_one "$j" 1 || ts "⚠ $j 실패 — 나머지는 계속 간다"
  done

  # ── doped 검증: 홀전자가 실제로 분자(–SO3)에 앉았나 ──────────────────────
  # ⚠ FSM 을 뺐으므로 **총 자화가 저절로 1 μB 근처로 갔는지**가 판정 기준이다.
  #   0 이면 라디칼이 슬랩으로 새거나 닫힌껍질로 떨어진 것 — 그때만 FSM 을 되살린다.
  if [ -s "$OUT/complex_doped/scf.out" ]; then
    TM=$(grep -a "total magnetization" "$OUT/complex_doped/scf.out" | tail -1)
    ts "doped 총 자화: $TM"
    ts "  → ~1.0 이면 OK. 0 에 가까우면 --seed_radical 을 키우거나 FSM(tot_magnetization=1.0) 복귀."
    "$UMA_PY" - "$OUT/complex_doped/scf.out" "$OUT/complex_doped/scf.in" <<'PYS'
import re, sys
out, inp = sys.argv[1], sys.argv[2]
txt = open(out, errors="ignore").read()
sp = []
L = open(inp, errors="ignore").read().splitlines()
i = next(k for k, l in enumerate(L) if l.strip().startswith("ATOMIC_POSITIONS"))
for l in L[i+1:]:
    t = l.split()
    if len(t) < 4 or not re.match(r"^[A-Za-z][A-Za-z0-9]{0,2}$", t[0]): break
    sp.append(t[0])
st = [m.start() for m in re.finditer(r"Magnetic moment per site", txt)]
if not st: raise SystemExit("site 자화 블록 없음")
blk = txt[st[-1]:st[-1] + 200*140]
rows = [(int(m.group(1)), float(m.group(2)))
        for m in re.finditer(r"atom\s+(\d+)\s.*?magn=\s*(-?\d+\.\d+)", blk, re.I)]
rows.sort(key=lambda r: -abs(r[1]))
print("  |magn| 상위 8 자리 (홀전자 위치 확인):")
for idx, mv in rows[:8]:
    s = sp[idx-1] if idx-1 < len(sp) else "?"
    print(f"    atom {idx:4d}  {s:4s}  {mv:+.3f}")
mol = sum(mv for idx, mv in rows if idx-1 < len(sp) and sp[idx-1] in ("C","H","S")
          or (idx-1 < len(sp) and sp[idx-1] == "O" and idx > 96))
print(f"  분자 쪽(C/H/S + 슬랩 뒤 O) 자화 합 {mol:+.3f} μB "
      "— 1 근처면 라디칼이 분자에 있다.")
PYS
  fi
fi
ts "끝. 다음: E_bind = E(complex) − E_slab − E_mol 을 README_harvest.txt 대로."
