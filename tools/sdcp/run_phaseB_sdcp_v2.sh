#!/usr/bin/env bash
# =============================================================================
# run_phaseB_sdcp_v2.sh — SDCP Phase-B (DFT+U) on the **new** LiNiO2(104) slab
#
# 목적 (kb/projects/sdcp_phaseB_direction_2026_08_06.md)
#   E_ads(doped) · E_ads(neutral) 를 둘 다 내고, **판정은 Δ = 둘의 차**로 한다.
#   Δ 에서는 E_slab 과 k-오차가 상쇄되고 개별값은 안 된다 → 개별값은 조건 병기해서 논문에,
#   결론은 Δ 로.  UMA 기준: doped −0.258 / neutral −0.0879 → **Δ_UMA = −0.170 eV**
#
# 왜 새 러너인가 (옛 run_phaseB_slabfirst_gabia.sh 를 못 쓰는 이유)
#   · 옛 것은 **폐기된 깨진 슬랩**(sdcp_linio2_binding/phaseB_v7c_slabfirst)을 본다
#   · 파일명이 옛 규약이다 — 우리 Phase-A 는 **격자 인덱스가 붙는다**(..._r90_g22.xyz)
#   · neutral 을 chelation_r0 로 **고정**해 놨는데, 우리 스캔의 neutral 최저는 sulfonate_down 이다
#   힘들게 얻은 설정(c-shrink · AFM inplane · seed_radical S:0.5 · no_fsm · david_ndim 2 ·
#   단일-k · 밀도승계는 job 별로)은 **그대로 승계**한다.
#
# ⚠⚠ 최대 리스크 = **두 복합체의 AFM 상태 불일치**. 서로 다른 Ni 스핀 배열로 수렴하면
#   Δ 가 통째로 오염되는데, 며칠 태우고 나서 알면 최악이다. → `magcheck` 게이트를 넣었다.
#   초반 SCF 만 보고 두 job 의 absolute magnetization 이 어긋나면 **즉시 멈춘다**.
#
#   bash tools/sdcp/run_phaseB_sdcp_v2.sh            # 전체 (slab -> 복합체·분자)
#   bash tools/sdcp/run_phaseB_sdcp_v2.sh slab       # 1단계만
#   bash tools/sdcp/run_phaseB_sdcp_v2.sh complexes  # 2단계만
#   MAGTOL=2.0 bash ...                              # 자화 허용폭(μB) 조정
# =============================================================================
set -uo pipefail; set +H
REPO="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$REPO"
unset LD_LIBRARY_PATH OPAL_PREFIX 2>/dev/null || true

# ── 경로 (전부 sdcp_v2 계열. 옛 BASE 는 입력 분자만 빌려 쓴다) ────────────────
OUT=${OUT:-/data/work/runs/sdcp_v2/phaseB}
SCAN=${SCAN:-/data/work/runs/sdcp_v2/phaseA}
MOLDIR=${MOLDIR:-/data/work/runs/sdcp_linio2_binding/inputs/sdcp_v7c}
REFSCF=${REFSCF:-/data/work/runs/sdcp_linio2_binding/reference_dft_v2/scf_u62.in}
SLAB0=${SLAB0:-$REPO/db/structures/linio2_104_sym_1x4L4_relaxed.vasp}
MAGJSON="$OUT/slab_mag.json"

# ── 챔피언 자세 (2026-08-06 확정, phaseA_v7c_results.csv 전수 정렬) ──────────
#   ⚠ 각 종의 **실제 최저**를 쓴다. 둘 다 sulfonate_down 이고 회전만 다르다 —
#     즉 결합 부위는 같고 세기만 다르다는 것이 Phase-A 의 결과다.
CX_D=${CX_D:-doped_sulfonate_down_r90_g22}      # E_ads(UMA) = -0.258 eV
CX_N=${CX_N:-neutral_sulfonate_down_r180_g01}   # E_ads(UMA) = -0.0879 eV

UMA_PY=${UMA_PY:-/data/apps/miniforge3/envs/uma/bin/python3}
QE=${QE:-/data/apps/qe-7.4.1-gpu/bin/pw.x}
H_MPI=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi
MPIRUN=${MPIRUN:-$H_MPI/bin/mpirun}
export PATH=$H_MPI/bin:$PATH OPAL_PREFIX=$H_MPI OMP_NUM_THREADS=1 CUDA_VISIBLE_DEVICES=0
export OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
export LD_LIBRARY_PATH=$H_MPI/lib:/data/apps/nvhpc/Linux_x86_64/24.11/compilers/lib:/usr/local/cuda-12.6/lib64

DEGAUSS=${DEGAUSS:-0.03}; MIXNDIM=${MIXNDIM:-8}; MAXSTEP=${MAXSTEP:-300}
SCF_MUST=${SCF_MUST:-.false.}; REPORT=${REPORT:-1}; TPRNFOR=${TPRNFOR:-.false.}
MAGTOL=${MAGTOL:-2.0}          # 두 복합체의 absolute magnetization 허용 차이 (μB)
STAGE=${1:-all}
mkdir -p "$OUT"
ts(){ echo "[$(date +%m-%d\ %H:%M:%S)] $*"; }

# ⚠ 중복 실행 가드는 flock 만 — pgrep 은 tmux 래퍼까지 세서 자기 자신에 걸린다(실측 2회).
LOCK=${LOCK:-/tmp/phaseB_v2.lock}
exec 9>"$LOCK" || { echo "⛔ 락 파일을 못 연다"; exit 1; }
command -v flock >/dev/null 2>&1 && { flock -n 9 || { ts "⛔ 이미 돈다 — 중단"; exit 0; }; }

ts "═══ SDCP Phase-B v2 ═══"
ts "  슬랩   $SLAB0"
ts "  doped  $SCAN/complex_$CX_D.xyz"
ts "  neutral $SCAN/complex_$CX_N.xyz"
for f in "$SLAB0" "$SCAN/complex_$CX_D.xyz" "$SCAN/complex_$CX_N.xyz" \
         "$MOLDIR/sdcp_v7c_doped.xyz" "$MOLDIR/sdcp_v7c_neutral.xyz"; do
  [ -s "$f" ] || { ts "⛔ 없음: $f"; exit 1; }
done

# ── c 축소: 진공을 줄여 비용을 낮춘다 (옛 판정 기준 = 이미지 간격 6.5 Å) ─────
if [ ! -s "$OUT/slab_cshrink.vasp" ]; then
  ZMAX=$("$UMA_PY" - "$SCAN" "$CX_D" "$CX_N" <<'PYZ'
import sys
scan, zmax = sys.argv[1], 0.0
for tag in sys.argv[2:]:
    ls = open(f"{scan}/complex_{tag}.xyz").read().split("\n")
    zmax = max(zmax, max(float(l.split()[3]) for l in ls[2:2 + int(ls[0])]))
print(f"{zmax:.2f}")
PYZ
) || { ts "⛔ pose zmax 계산 실패"; exit 1; }
  C=$(awk -v z="$ZMAX" 'BEGIN{printf "%.3f", z + 6.5}')
  ts "pose zmax=$ZMAX Å → c=$C Å (이미지 간격 6.5 Å)"
  "$UMA_PY" - "$SLAB0" "$OUT/slab_cshrink.vasp" "$C" <<'PYC'
import sys
from ase.io import read, write
src, out, c_new = sys.argv[1], sys.argv[2], float(sys.argv[3])
at = read(src)
cell = at.cell.array.copy()
assert c_new > at.positions[:, 2].max() + 4.0, "c 가 슬랩보다 작다 — 중단"
cell[2] = [0.0, 0.0, c_new]
at.set_cell(cell); at.set_pbc(True)
write(out, at, format="vasp", direct=False)
print(f"c {cell[2][2]:.3f} Å · 슬랩 top {at.positions[:,2].max():.2f} Å")
PYC
fi

gen(){
  local extra=()
  # ⚠ startingpot 을 여기(전 job 공통)에 붙이면 안 된다 — 밀도가 있는 job 은 slab 뿐이라
  #   복합체·분자가 '없는 파일을 읽어라'로 죽는다. 승계는 run_one 이 job 별로 판단한다.
  [ -s "$MAGJSON" ] && extra+=(--mag_json "$MAGJSON")
  "$UMA_PY" "$REPO/tools/sdcp/phaseB_v7c_dft_binding.py" \
    --slab "$OUT/slab_cshrink.vasp" \
    --complex_doped   "$SCAN/complex_$CX_D.xyz" \
    --complex_neutral "$SCAN/complex_$CX_N.xyz" \
    --mol_doped   "$MOLDIR/sdcp_v7c_doped.xyz" \
    --mol_neutral "$MOLDIR/sdcp_v7c_neutral.xyz" \
    --ref_scf     "$REFSCF" \
    --afm_mode inplane --mol_vacuum 8 --pseudo_dir /data/work/pseudo \
    --no_fsm --degauss "$DEGAUSS" --scf_must_converge "$SCF_MUST" \
    --electron_maxstep "$MAXSTEP" --seed_radical S:0.5 --mixing_ndim "$MIXNDIM" \
    --report "$REPORT" --tprnfor "$TPRNFOR" \
    ${extra[@]+"${extra[@]}"} --out "$OUT" || return 1
  # OOM 대책 (옛 러너와 동일): 단일-k + david_ndim 2
  for j in slab complex_doped complex_neutral; do
    [ -s "$OUT/$j/scf.in" ] || continue
    grep -aq diago_david_ndim "$OUT/$j/scf.in" || \
      sed -i '/&ELECTRONS/a\    diago_david_ndim = 2' "$OUT/$j/scf.in"
    sed -i 's/^\s*[0-9] [0-9] [0-9] 0 0 0/  1 1 1 0 0 0/' "$OUT/$j/scf.in"
  done
}

run_one(){   # $1 = job dir
  local j=$1
  [ -s "$OUT/$j/scf.in" ] || { ts "⛔ $OUT/$j/scf.in 없음"; return 1; }
  if grep -aq "convergence has been achieved" "$OUT/$j/scf.out" 2>/dev/null; then
    ts "✓ $j 이미 수렴 — 건너뜀"; return 0; fi
  # 밀도 승계는 **이 job 자신의** charge-density 가 있을 때만 (U-ramp / 재시작)
  if ls "$OUT/$j"/tmp/*.save/charge-density* >/dev/null 2>&1; then
    grep -aq "startingpot" "$OUT/$j/scf.in" || \
      sed -i "/&ELECTRONS/a\    startingpot     = 'file'" "$OUT/$j/scf.in"
    ts "↻ $j 밀도 승계 (startingpot='file')"
  fi
  # ⚠ 이전 scf.out 을 덮어쓰면 accuracy 궤적이 사라진다 — 진단이 그걸 먹고 산다.
  [ -s "$OUT/$j/scf.out" ] && mv "$OUT/$j/scf.out" "$OUT/$j/scf.out.$(date +%m%d_%H%M)"
  ts "▶ $j 시작"
  ( cd "$OUT/$j" && $MPIRUN -np 1 --oversubscribe "$QE" -nk 1 -in scf.in > scf.out 2>&1 )
  if grep -aq "convergence has been achieved" "$OUT/$j/scf.out"; then
    ts "✓ $j 수렴 — $(grep -a '!.*total energy' "$OUT/$j/scf.out" | tail -1)"
  else
    ts "✗ $j 미수렴 — 진단:"
    "$UMA_PY" "$REPO/tools/sdcp/scf_convergence_doctor.py" \
        --scf_out "$OUT/$j/scf.out" --scf_in "$OUT/$j/scf.in" 2>&1 | tail -20
    return 1
  fi
}

# ── ★ AFM 게이트 — Δ 를 지키는 장치. 며칠 태우기 전에 여기서 걸린다 ──────────
magcheck(){
  local a b
  a=$(grep -a "absolute magnetization" "$OUT/complex_doped/scf.out"   2>/dev/null | tail -1 | awk '{print $4}')
  b=$(grep -a "absolute magnetization" "$OUT/complex_neutral/scf.out" 2>/dev/null | tail -1 | awk '{print $4}')
  [ -n "$a" ] && [ -n "$b" ] || { ts "· 자화 비교 보류 (아직 출력 없음)"; return 0; }
  local d; d=$(awk -v x="$a" -v y="$b" 'BEGIN{printf "%.2f", (x>y?x-y:y-x)}')
  ts "자화 대조: doped $a μB · neutral $b μB · 차 $d (허용 $MAGTOL)"
  awk -v d="$d" -v t="$MAGTOL" 'BEGIN{exit !(d<=t)}' && { ts "  ✅ 같은 AFM 배열로 수렴"; return 0; }
  ts "  ⛔⛔ **두 복합체가 다른 자기 상태다 — Δ 가 오염된다.** 여기서 멈춘다."
  ts "     처방: --mag_json 시드를 다시 뽑거나(1단계), U-ramp 를 명시적으로 걸어라."
  ts "     ⚠ 이 상태로 끝까지 돌려서 나온 Δ 는 **쓰면 안 된다.**"
  return 1
}

# ── 1단계: 슬랩 (E_ads 개별값에 필요. Δ 에는 상쇄되지만 논문 수치라 낸다) ────
if [ "$STAGE" = all ] || [ "$STAGE" = slab ]; then
  ts "═══ 1단계: 슬랩 (E_ads 개별값용 · AFM 시드 생성) ═══"
  gen || { ts "⛔ 입력 생성 실패"; exit 1; }
  run_one slab || ts "⚠ 슬랩 미수렴 — 시드만 뽑아 진행을 시도한다"
  "$UMA_PY" "$REPO/tools/sdcp/slab_mag_from_scfout.py" \
      --scf_out "$OUT/slab/scf.out" --scf_in "$OUT/slab/scf.in" --out "$MAGJSON" \
    && ts "✓ AFM 시드 → $MAGJSON" \
    || ts "⚠ 시드 추출 실패 — 복합체는 관례 ±0.3 으로 간다(NO_SEED 상당)"
fi

# ── 2단계: 복합체 2 + 분자 2 ────────────────────────────────────────────────
if [ "$STAGE" = all ] || [ "$STAGE" = complexes ]; then
  ts "═══ 2단계: 복합체 2 + 가스상 분자 2 ═══"
  gen || { ts "⛔ 입력 재생성 실패"; exit 1; }
  for j in complex_doped complex_neutral mol_doped mol_neutral; do
    run_one "$j" || ts "⚠ $j 실패 — 나머지는 계속 간다"
    case "$j" in complex_neutral) magcheck || exit 1 ;; esac
  done
fi

# ── 결산 ────────────────────────────────────────────────────────────────────
ts "═══ 결산 ═══"
"$UMA_PY" - "$OUT" <<'PYS'
import os, re, sys
out = sys.argv[1]
def E(j):
    p = os.path.join(out, j, "scf.out")
    if not os.path.isfile(p): return None
    m = re.findall(r"^!\s+total energy\s+=\s+(-?[\d.]+)", open(p, errors="ignore").read(), re.M)
    return float(m[-1]) * 13.605693 if m else None      # Ry -> eV
e = {j: E(j) for j in ("slab", "complex_doped", "complex_neutral", "mol_doped", "mol_neutral")}
for k, v in e.items():
    print(f"  {k:16s} {'—' if v is None else f'{v:.4f} eV'}")
def ads(cx, mol):
    if None in (e[cx], e["slab"], e[mol]): return None
    return e[cx] - e["slab"] - e[mol]
ad, an = ads("complex_doped", "mol_doped"), ads("complex_neutral", "mol_neutral")
if ad is not None: print(f"\n  E_ads(doped)   = {ad:+.4f} eV")
if an is not None: print(f"  E_ads(neutral) = {an:+.4f} eV")
if None not in (e["complex_doped"], e["complex_neutral"], e["mol_doped"], e["mol_neutral"]):
    d = (e["complex_doped"] - e["complex_neutral"]) - (e["mol_doped"] - e["mol_neutral"])
    print(f"\n  ★ Δ = E_ads(d) − E_ads(n) = {d:+.4f} eV   (UMA 기준 −0.170 eV)")
    print("     ⚠ Δ 는 E_slab 과 k-오차가 상쇄되어 ★★★ · 개별 E_ads 는 Γ-only 와 구속이"
          " 그대로 실려 ★☆☆ — 논문에는 조건 병기해서 싣고 결론은 Δ 로 낸다.")
    if abs(d) < 0.026:
        print("     ⛔ |Δ| 가 열잡음(kT≈26 meV) 수준이다 — UMA 자세 선택 자체를 못 믿는다는 뜻.")
PYS
ts "═══ 끝 ═══"
