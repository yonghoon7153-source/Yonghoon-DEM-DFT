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
DEGAUSS=${DEGAUSS:-0.02}
gen(){   # $1 = "slab" | "complexes"
  local extra=()
  [ -s "$MAGJSON" ] && extra+=(--mag_json "$MAGJSON")
  "$UMA_PY" "$REPO/tools/sdcp/phaseB_v7c_dft_binding.py" \
    --slab "$OUT/slab_cshrink.vasp" \
    --complex_doped   "$SCAN/complex_doped_sulfonate_down_r90.xyz" \
    --complex_neutral "$SCAN/complex_neutral_chelation_r0.xyz" \
    --mol_doped   "$BASE/inputs/sdcp_v7c/sdcp_v7c_doped.xyz" \
    --mol_neutral "$BASE/inputs/sdcp_v7c/sdcp_v7c_neutral.xyz" \
    --ref_scf     "$BASE/reference_dft_v2/scf_u62.in" \
    --afm_mode inplane --mol_vacuum 8 --pseudo_dir /data/work/pseudo \
    --no_fsm --degauss "$DEGAUSS" --scf_must_converge .true. \
    --electron_maxstep 300 --seed_radical S:0.5 \
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
  guard
  ts "▶ $j 시작 (-nk $nk)"
  ( cd "$OUT/$j" && $MPIRUN -np 1 --oversubscribe "$QE" -nk "$nk" -in scf.in > scf.out 2>&1 )
  if grep -aq "convergence has been achieved" "$OUT/$j/scf.out"; then
    ts "✓ $j 수렴 — $(grep -a '!.*total energy' "$OUT/$j/scf.out" | tail -1)"
  else
    ts "✗ $j 미수렴 — 마지막 accuracy:"
    grep -a "estimated scf accuracy" "$OUT/$j/scf.out" | tail -3
    return 1
  fi
}

# ── 1단계: 슬랩 ─────────────────────────────────────────────────────────────
if [ "$STAGE" = all ] || [ "$STAGE" = slab ]; then
  ts "═══ 1단계: 96원자 슬랩 (neutral·doped 공용) ═══"
  gen slab || { ts "입력 생성 실패"; exit 1; }
  run_one slab 1 || { ts "슬랩이 안 수렴했다 — 여기서 멈춘다. 복합체로 가면 안 된다."; exit 1; }
  "$UMA_PY" "$REPO/tools/sdcp/slab_mag_from_scfout.py" \
      --scf_out "$OUT/slab/scf.out" --scf_in "$OUT/slab/scf.in" --out "$MAGJSON" || exit 1
fi

# ── 2단계: 복합체 + 가스 ────────────────────────────────────────────────────
if [ "$STAGE" = all ] || [ "$STAGE" = complexes ]; then
  [ -s "$MAGJSON" ] || { ts "⛔ $MAGJSON 이 없다 — 1단계를 먼저 돌려라"; exit 1; }
  ts "═══ 2단계: 시드 승계 후 복합체 ($(cat "$MAGJSON" | tr -d '\n ')) ═══"
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
