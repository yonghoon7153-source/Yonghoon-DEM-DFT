#!/usr/bin/env bash
# =============================================================================
# run_phaseB_refine_gabia.sh — DFT+U refine of SDCP LiNiO2 binding at the
# IMAGE-CLEAN UMA preferred poses (c40 tall-vacuum re-screen champions):
#   doped   = sulfonate_down_r90   (image-clean champion, -4.203 UMA)
#   neutral = chelation_r0         (neutral champion,       -2.673 UMA)
#
# WHY: the vertical protocol FORCED doped into the neutral pose -> biased ("약화").
# This scores each state in its OWN preferred, image-clean pose (the standard
# way). Verdict = E_bind(doped) - E_bind(neutral); SLAB CANCELS, so 2 complexes +
# 2 gas refs already give it (slab only for the absolute E_bind).
#
#   cd ~/Yonghoon-DEM-DFT && git pull   # (or checkout the 3 files)
#   tmux new -s pbrefine -d 'bash tools/sdcp/run_phaseB_refine_gabia.sh > \
#       /data/work/runs/sdcp_linio2_binding/pbrefine.log 2>&1'
# ⚠ pw.x -- run only when NO UMA/pw.x is on the GPU (VRAM). ~하루(복합체 2개가 heavy).
#
# OOM (2026-07-21): 48GB A6000에서 c40/c33/c31/c30/c29 전부 "cufftPlanMany failed"
# (scf#3에서 일회성 대형 할당이 천장 초과; vertical c25.334 자체가 47/48GB급이었음).
# c 축소만으론 부족 -> 큰 셀 3개를 Γ-only로 전환(gamma 트릭: real wfc, 1 k-point;
# wfc/Davidson 블록 ~4x 절감) + david_ndim 2 + C-LADDER(zmax+{8.5,7.5,6.5}A).
# 이미지 간격 6.5A 미만은 불허(UMA 아티팩트 영역) — 전부 실패 시 ecutrho 절충 논의.
# k 221->Γ: 절대값은 v2 vertical(221/c25.334)과 직접 비교 불가로 표기; verdict(차분)
# 는 4항 전부 동일 조건이라 견고.
# =============================================================================
set -u; set +H
BASE=/data/work/runs/sdcp_linio2_binding
REPO=${REPO:-$HOME/Yonghoon-DEM-DFT}; [ -d "$REPO" ] || REPO=$HOME/work/Yonghoon-DEM-DFT
OUT=$BASE/phaseB_v7c_refine
SCAN=$BASE/phaseA_v7c_tallvac
UMA_PY=$(ls /data/apps/miniforge3/envs/uma/bin/python3 2>/dev/null || which python3)
echo "REPO=$REPO  UMA_PY=$UMA_PY"
mkdir -p "$OUT"

# ---- qegpu env (vertical 러너와 동일) ----
HPCX=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi
export PATH=$HPCX/bin:$PATH
export LD_LIBRARY_PATH=$HPCX/lib:/data/apps/nvhpc/Linux_x86_64/24.11/compilers/lib:/usr/local/cuda-12.6/lib64:${LD_LIBRARY_PATH:-}
export OPAL_PREFIX=$HPCX OMP_NUM_THREADS=1 CUDA_VISIBLE_DEVICES=0
export OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
QE=/data/apps/qe-7.4.1-gpu/bin/pw.x
MPIRUN=$HPCX/bin/mpirun

# ---- pose zmax (이미지 간격 기준점) ----
ZMAX=$("$UMA_PY" - "$SCAN" <<'PYZ'
import sys
scan = sys.argv[1]; zmax = 0.0
for tag in ("complex_doped_sulfonate_down_r90", "complex_neutral_chelation_r0"):
    ls = open(f"{scan}/{tag}.xyz").read().split("\n")
    zs = [float(l.split()[3]) for l in ls[2:2 + int(ls[0])]]
    zmax = max(zmax, max(zs))
print(f"{zmax:.2f}")
PYZ
) || exit 1
echo "[cell] pose zmax=$ZMAX A (slab bottom z~0.07)"

gen_at_c() {  # $1 = c (A): shrunk slab vasp -> 5 inputs -> memory knob on big 3
  "$UMA_PY" - "$REPO/db/structures/sdcp_phaseB_slab_c40.vasp" "$OUT" "$1" <<'PYC' || return 1
import sys
vasp, out, c_new = sys.argv[1], sys.argv[2], float(sys.argv[3])
lines = open(vasp).read().splitlines()
assert "Cartesian" in lines[7], "expect Cartesian POSCAR"
lines[4] = f"      0.000000000000     0.000000000000    {c_new:.9f}"
open(f"{out}/slab_cshrink.vasp", "w").write("\n".join(lines) + "\n")
PYC
  "$UMA_PY" "$REPO/tools/sdcp/phaseB_v7c_dft_binding.py" \
    --slab "$OUT/slab_cshrink.vasp" \
    --complex_doped   "$SCAN/complex_doped_sulfonate_down_r90.xyz" \
    --complex_neutral "$SCAN/complex_neutral_chelation_r0.xyz" \
    --mol_doped   "$BASE/inputs/sdcp_v7c/sdcp_v7c_doped.xyz" \
    --mol_neutral "$BASE/inputs/sdcp_v7c/sdcp_v7c_neutral.xyz" \
    --ref_scf     "$BASE/reference_dft_v2/scf_u62.in" \
    --afm_mode inplane --mol_vacuum 8 --pseudo_dir /data/work/pseudo \
    --out "$OUT" > /dev/null || return 1
  for j in slab complex_doped complex_neutral; do
    grep -aq diago_david_ndim "$OUT/$j/scf.in" || \
      sed -i '/&ELECTRONS/a\    diago_david_ndim = 2' "$OUT/$j/scf.in"
  done
  # Γ-트릭 (2026-07-21): 221 k-mesh의 파동함수/Davidson 메모리(nks배 + complex계수)가
  # 진짜 살덩이 — Γ-only는 real-wfc라 그 블록을 ~4x 절감. verdict(차분)엔 영향 미미,
  # refine 세트 내부(복합체2+slab+mol) 전부 동일 샘플링이라 자기일관.
  "$UMA_PY" - "$OUT" <<'PYK'
import re, sys
out = sys.argv[1]
for j in ("slab", "complex_doped", "complex_neutral"):
    p = f"{out}/{j}/scf.in"; t = open(p).read()
    t2 = re.sub(r"K_POINTS automatic\n\s*[\d ]+\n", "K_POINTS gamma\n", t)
    open(p, "w").write(t2)
    assert "K_POINTS gamma" in t2, f"{j}: K_POINTS swap failed"
print("[mem] K_POINTS 221 -> gamma in slab/complex_doped/complex_neutral")
PYK
}

run_one() {
  local d=$OUT/$1
  grep -aq "JOB DONE" "$d/scf.out" 2>/dev/null && { echo "[$1] done — skip"; return; }
  echo "[$(date +%H:%M:%S)] pw.x $1 (nat $(grep -a 'nat' "$d/scf.in"|head -1|grep -ao '[0-9]*'))"
  cd "$d" && "$MPIRUN" -np 1 "$QE" -npool 1 -in scf.in > scf.out 2>&1
  grep -aq "JOB DONE" "$d/scf.out" && echo "[$1] OK  E=$(grep -a '^!' "$d/scf.out"|tail -1|awk '{print $(NF-1)}')" \
    || echo "[$1] plateau/미수렴/에러 (ladder 판정 아래)"
}

# ---- C-LADDER: complex_doped가 살아남는 최대 c를 찾고 그 c로 전체 진행 ----
ok=0
for GAP in 8.5 7.5 6.5; do
  C=$("$UMA_PY" -c "import math; print(math.ceil($ZMAX + $GAP))")
  echo "══ [ladder] c=${C}A 시도 (image gap ~${GAP}A, david_ndim 2) ══"
  gen_at_c "$C" || { echo "입력생성 실패 (scf_u62.in / 자세 xyz 경로 확인)"; exit 1; }
  rm -f "$OUT/complex_doped/scf.out" "$OUT/complex_neutral/scf.out" "$OUT/slab/scf.out"
  run_one complex_doped
  if grep -aqE "cufftPlanMany|cfft3d_gpu|[Ii]nsufficient.*memory|out of memory" "$OUT/complex_doped/scf.out"; then
    echo "[ladder] c=$C OOM — 한 단계 축소해서 재시도"; continue
  elif grep -aq "Error in routine" "$OUT/complex_doped/scf.out"; then
    echo "[ladder] c=$C 비-OOM 에러 — 중단, tail:"; tail -20 "$OUT/complex_doped/scf.out"; exit 1
  fi
  ok=1; echo "[ladder] c=$C 통과 — 이 셀로 나머지 진행"; break
done
[ "$ok" = 1 ] || { echo "!! Γ-only로도 gap 6.5A(c≈29)까지 전부 OOM — ecutrho 절충 논의 필요 (에스컬레이션)"; exit 1; }
# 복합체 먼저 (verdict 핵심) -> gas(이미 done, skip) -> slab (절대값용)
for j in complex_neutral mol_doped mol_neutral slab; do run_one "$j"; done

# ---- harvest + verdict (slab-free) ----
echo ""; echo "===== VERDICT ====="
python3 - <<PYH
import re
Ry=13.605693
def E(p):
    try:
        t=open(f"$OUT/{p}/scf.out").read()
        m=re.findall(r"^!\s+total energy\s+=\s+(-\d+\.\d+)",t,re.M) or re.findall(r"total energy\s+=\s+(-\d+\.\d+)",t)
        return float(m[-1]) if m else None
    except FileNotFoundError: return None
e={k:E(k) for k in ["slab","complex_doped","complex_neutral","mol_doped","mol_neutral"]}
print("harvest (Ry):", {k:(round(v,5) if v else None) for k,v in e.items()})
need=["complex_doped","complex_neutral","mol_doped","mol_neutral"]
if all(e[k] is not None for k in need):
    d=(e["complex_doped"]-e["mol_doped"]-e["complex_neutral"]+e["mol_neutral"])*Ry
    print(f"VERDICT  Delta = E_bind(doped,sulfonate) - E_bind(neutral,chelation) = {d:+.3f} eV")
    print(f"  => {'도핑이 결합 강화 (UMA 방향 DFT 확정)' if d<0 else '도핑이 결합 약화'}")
    if e["slab"] is not None:
        ebd=(e["complex_doped"]-e["slab"]-e["mol_doped"])*Ry
        ebn=(e["complex_neutral"]-e["slab"]-e["mol_neutral"])*Ry
        print(f"  절대값: E_bind(doped,sulfonate)={ebd:+.3f} | E_bind(neutral,chelation)={ebn:+.3f} eV")
else:
    print("복합체/가스 일부 미완 — 붙여주면 verdict 계산")
PYH
echo ">> refine DONE (verdict 위)"
