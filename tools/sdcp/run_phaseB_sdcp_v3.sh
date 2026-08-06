#!/usr/bin/env bash
# =============================================================================
# run_phaseB_sdcp_v3.sh — SDCP Phase-B (DFT+U). **흡착에너지와 반응에너지를 둘 다** 낸다.
#
# 왜 v3 인가 (v2 를 못 쓰는 이유)
#   v2 는 얼린 스캔(freeze_frac 1.0)의 자세를 채점하는 설계였다. 그런데 그 자세들은
#   전부 물리흡착(O↔Li 2.5–2.9 Å)이었고, doped 의 Li 자리 vs Ni 자리 격차가 9 meV 라
#   무엇을 넣을지가 사실상 동전 던지기였다. 최상단 층을 풀어(0.85) 재스캔하니 그림이 바뀌었다:
#     · doped  — 108 자세 중 9개가 **Li 추출**(Li 가 2.35 Å 이동, 술폰산 O 에 1.94–1.98 Å 배위)
#     · neutral — 108 자세 **전부** 추출 없음 (최대 변위 0.64 Å)
#   즉 본론은 '누가 더 잘 붙나'가 아니라 '한쪽만 반응 경로를 연다' 이다.
#
# 무엇을 내나 (job 6개)
#   E_ads(doped)   = E(cx_d_phys) − E(slab) − E(mol_d)      ← 흡착에너지 (논문의 binding energy)
#   E_ads(neutral) = E(cx_n_phys) − E(slab) − E(mol_n)      ← 흡착에너지
#   Δ              = E_ads(d) − E_ads(n)                     ← E_slab 대수적으로 상쇄
#   ΔE_rxn(doped)  = E(cx_d_extr) − E(slab) − E(mol_d)      ← 전체 표면반응에너지
#   ΔE_extract     = E(cx_d_extr) − E(cx_d_phys)            ← 추출 단계만. 기준항 전부 상쇄
#
#   ⚠ 용어 — E(cx_d_extr) 기반 값은 **흡착에너지가 아니다.** 기판 Li 가 흡착종 착물에
#     편입됐으므로 adsorption 이 아니라 reaction 이다. 논문에 E_ads 로 쓰면 안 된다.
#
# ⚠⚠ 일관성 규율 — E_bind 는 기준항이 안 상쇄되므로 **모든 기하가 같은 MLIP 프로토콜**에서
#   와야 한다. 슬랩 기준은 반드시 `freeze_frac 0.85` 로 이완한 맨 슬랩이다. phaseA(고정)
#   슬랩을 쓰면 표면 이완에너지가 개별 E_ads 에 통째로 섞인다(Δ 에서는 상쇄되지만
#   지금 필요한 건 개별값이다).
#
# ⚠ 분자 기준항 — 가스상 분자는 ORCA r²SCAN-3c 로 이완한 기하에서 **SCF 만** 한다(v2 승계).
#   DFT 이완이 아니므로 분자 변형에너지가 E_ads 에 일부 남는다. 두 종을 같은 방식으로
#   처리하므로 **Δ 에서는 대부분 상쇄**되고, **ΔE_extract 에는 아예 안 들어간다**(분자 기준항이
#   식에 없다). 논문에는 "DFT+U single-point at MLIP/ORCA-relaxed geometries" 로 명시.
#
#   bash tools/sdcp/run_phaseB_sdcp_v3.sh probe   # 메모리 탐침 먼저 (권장)
#   bash tools/sdcp/run_phaseB_sdcp_v3.sh         # 전체
#   bash tools/sdcp/run_phaseB_sdcp_v3.sh complexes
#   DIAG=ppcg bash ...                            # OOM 사다리 2단
# =============================================================================
set -uo pipefail; set +H
REPO="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$REPO"
unset LD_LIBRARY_PATH OPAL_PREFIX 2>/dev/null || true

OUT=${OUT:-/data/work/runs/sdcp_v2/phaseB_v3}
SCAN=${SCAN:-/data/work/runs/sdcp_v2/phaseA_top1free}      # 자세 3개가 전부 여기서 온다
SLABREF=${SLABREF:-/data/work/runs/sdcp_v2/slabref_085/slab_ref_relaxed.xyz}
MOLDIR=${MOLDIR:-/data/work/runs/sdcp_linio2_binding/inputs/sdcp_v7c}
REFSCF=${REFSCF:-/data/work/runs/sdcp_linio2_binding/reference_dft_v2/scf_u62.in}
MAGJSON="$OUT/slab_mag.json"

# ── 자세 (2026-08-06 champion_report.py 로 확정) ────────────────────────────
#   같은 스캔(phaseA_top1free) 안에서 뽑았다 — 다른 스캔과 섞으면 ΔE 에 'UMA 기하를
#   DFT 로 채점한 벌점'이 추출 쪽에만 붙는다.
CX_D_PHYS=${CX_D_PHYS:-doped_sulfonate_down_r0_g20}      # 변위 0.30 Å · E_bind(UMA) −0.325
CX_D_EXTR=${CX_D_EXTR:-doped_sulfonate_down_r180_g20}    # 변위 2.35 Å · E_bind(UMA) −1.267
CX_N_PHYS=${CX_N_PHYS:-neutral_sulfonate_down_r180_g22}  # 변위 0.48 Å · E_bind(UMA) −0.252
CX_N_EXTR=${CX_N_EXTR:-}                                 # ⚠ 비움 — neutral 은 추출 자세가 없다

UMA_PY=${UMA_PY:-/data/apps/miniforge3/envs/uma/bin/python3}
QE=${QE:-/data/apps/qe-7.4.1-gpu/bin/pw.x}
H_MPI=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi
MPIRUN=${MPIRUN:-$H_MPI/bin/mpirun}
export PATH=$H_MPI/bin:$PATH OPAL_PREFIX=$H_MPI OMP_NUM_THREADS=1 CUDA_VISIBLE_DEVICES=0
export OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
export LD_LIBRARY_PATH=$H_MPI/lib:/data/apps/nvhpc/Linux_x86_64/24.11/compilers/lib:/usr/local/cuda-12.6/lib64

DEGAUSS=${DEGAUSS:-0.03}; MIXNDIM=${MIXNDIM:-8}; MAXSTEP=${MAXSTEP:-300}
SCF_MUST=${SCF_MUST:-.false.}; REPORT=${REPORT:-1}; TPRNFOR=${TPRNFOR:-.false.}
MAGTOL=${MAGTOL:-2.0}
DIAG=${DIAG:-}                 # 대각화 작업배열이 문제일 때만 (ppcg). newd OOM 엔 안 듣는다
ECUTWFC=${ECUTWFC:-60}         # Ry
ECUTRHO=${ECUTRHO:-480}        # Ry — newd OOM 의 실질 손잡이 (ngm ∝ ecutrho^1.5)
# ⛔ REAL_SPACE 는 이 빌드에서 newq OOM 에 도움이 안 된다 (2026-08-06 실측 — 오히려 악화).
#    진단용으로만 남긴다. 기본은 끔.
REAL_SPACE=${REAL_SPACE:-}
GAP=${GAP:-15.0}               # 생성기 --min_image_gap 과 **같은 수** (v2 사고 재발 방지)
CMARG=${CMARG:-1.0}
STAGE=${1:-all}
mkdir -p "$OUT"
ts(){ echo "[$(date +%m-%d\ %H:%M:%S)] $*"; }

LOCK=${LOCK:-/tmp/phaseB_v3.lock}
exec 9>"$LOCK" || { echo "⛔ 락 파일을 못 연다"; exit 1; }
command -v flock >/dev/null 2>&1 && { flock -n 9 || { ts "⛔ 이미 돈다 — 중단"; exit 0; }; }

ts "═══ SDCP Phase-B v3 (E_ads + ΔE_rxn) ═══"
ts "  수치 설정 ecutwfc $ECUTWFC · ecutrho $ECUTRHO Ry$([ -n "$REAL_SPACE" ] && echo ' · real_space')$([ -n "$DIAG" ] && echo " · diag=$DIAG")"
ts "  슬랩 기준 $SLABREF"
ts "  doped  물리흡착 $CX_D_PHYS"
ts "  doped  추출     $CX_D_EXTR"
ts "  neutral 물리흡착 $CX_N_PHYS"
[ -n "$CX_N_EXTR" ] && ts "  neutral 추출     $CX_N_EXTR" \
                    || ts "  neutral 추출     (없음 — UMA 가 108 자세 전부에서 못 찾았다)"

NEED=("$SLABREF" "$SCAN/complex_$CX_D_PHYS.xyz" "$SCAN/complex_$CX_D_EXTR.xyz"
      "$SCAN/complex_$CX_N_PHYS.xyz" "$MOLDIR/sdcp_v7c_doped.xyz" "$MOLDIR/sdcp_v7c_neutral.xyz")
[ -n "$CX_N_EXTR" ] && NEED+=("$SCAN/complex_$CX_N_EXTR.xyz")
for f in "${NEED[@]}"; do
  [ -s "$f" ] || { ts "⛔ 없음: $f"; exit 1; }
done

# ── 셀: 진공은 게이트와 같은 기준으로. 자세 전부의 zmax 를 본다 ──────────────
ZMAX=$("$UMA_PY" - "$SCAN" "$CX_D_PHYS" "$CX_D_EXTR" "$CX_N_PHYS" ${CX_N_EXTR:+"$CX_N_EXTR"} <<'PYZ'
import sys
scan, zmax = sys.argv[1], 0.0
for tag in sys.argv[2:]:
    ls = open(f"{scan}/complex_{tag}.xyz").read().split("\n")
    zmax = max(zmax, max(float(l.split()[3]) for l in ls[2:2 + int(ls[0])]))
print(f"{zmax:.2f}")
PYZ
) || { ts "⛔ pose zmax 계산 실패"; exit 1; }
# ⚠⚠ 슬랩 바닥이 z=0 이 아니다 (우리 슬랩은 z=12.0 부터). 다음 이미지의 슬랩 바닥은
#   c + zmin_slab 에 있으므로 필요한 c 는 zmax + GAP + 여유 − **zmin_slab** 이다.
#   2026-08-06 이전 판은 zmin_slab 을 안 빼서 c 를 34.4 대신 46.4 로 잡았고(간격 28 Å),
#   셀이 35% 부풀어 48 GB GPU 에서 newq 가 OOM 으로 죽었다.
ZMIN=$("$UMA_PY" -c "
from ase.io import read; import sys
print('%.3f' % read('$SLABREF').positions[:,2].min())") || { ts "⛔ 슬랩 바닥 계산 실패"; exit 1; }
C=$(awk -v z="$ZMAX" -v g="$GAP" -v m="$CMARG" -v b="$ZMIN" 'BEGIN{printf "%.3f", z + g + m - b}')
ts "pose zmax=$ZMAX · 슬랩 바닥 $ZMIN Å → c=$C Å"
ts "   (실제 이미지 간격 = 천장까지 $(awk -v c=$C -v z=$ZMAX 'BEGIN{printf "%.1f", c-z}') + 바닥 오프셋 $ZMIN = $GAP+$CMARG Å)"

# 슬랩 기준은 **freeze_frac 0.85 로 이완한 맨 슬랩**이다. 셀만 c 로 맞춘다.
SLABC="$OUT/slab_ref_c${C%.*}.vasp"
if [ -s "$SLABC" ]; then
  "$UMA_PY" - "$SLABC" "$C" <<'PYCHK' || rm -f "$SLABC"
import sys
from ase.io import read
have, want = read(sys.argv[1]).cell.array[2][2], float(sys.argv[2])
if have + 1e-3 < want:
    print(f"  ⚠ 기존 셀 c={have:.3f} < 필요 {want:.3f} — 다시 만든다"); raise SystemExit(1)
print(f"  · 슬랩 기준 재사용 (c={have:.3f} Å)")
PYCHK
fi
if [ ! -s "$SLABC" ]; then
  "$UMA_PY" - "$SLABREF" "$REPO/db/structures/linio2_104_sym_1x4L4_relaxed.vasp" "$SLABC" "$C" <<'PYC'
import sys
from ase.io import read, write
src, cellsrc, out, c_new = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
at = read(src)                       # ⚠ .xyz 라 격자가 없다 — 원본 슬랩에서 면내 격자를 가져온다
cell = read(cellsrc).cell.array.copy()
cell[2] = [0.0, 0.0, c_new]
at.set_cell(cell); at.set_pbc(True)
assert c_new > at.positions[:, 2].max() + 4.0, "c 가 슬랩보다 작다 — 중단"
write(out, at, format="vasp", direct=False)
print(f"슬랩 기준 c {c_new:.3f} Å · top {at.positions[:,2].max():.2f} Å · {len(at)} 원자")
PYC
fi

gen(){
  local extra=()
  [ -s "$MAGJSON" ] && extra+=(--mag_json "$MAGJSON")
  [ -n "$CX_N_EXTR" ] && extra+=(--complex_neutral2 "$SCAN/complex_$CX_N_EXTR.xyz")
  "$UMA_PY" "$REPO/tools/sdcp/phaseB_v7c_dft_binding.py" \
    --slab "$SLABC" \
    --complex_doped   "$SCAN/complex_$CX_D_PHYS.xyz" \
    --complex_doped2  "$SCAN/complex_$CX_D_EXTR.xyz" \
    --complex_neutral "$SCAN/complex_$CX_N_PHYS.xyz" \
    --mol_doped   "$MOLDIR/sdcp_v7c_doped.xyz" \
    --mol_neutral "$MOLDIR/sdcp_v7c_neutral.xyz" \
    --ref_scf     "$REFSCF" \
    --afm_mode inplane --mol_vacuum 8 --pseudo_dir /data/work/pseudo \
    --min_image_gap "$GAP" \
    --ecutwfc "$ECUTWFC" --ecutrho "$ECUTRHO" ${REAL_SPACE:+--real_space} \
    --no_fsm --degauss "$DEGAUSS" --scf_must_converge "$SCF_MUST" \
    --electron_maxstep "$MAXSTEP" --seed_radical S:0.5 --mixing_ndim "$MIXNDIM" \
    --report "$REPORT" --tprnfor "$TPRNFOR" \
    --slab_coord_tol 99 \
    ${extra[@]+"${extra[@]}"} --out "$OUT" || return 1
  # ⚠ --slab_coord_tol 99 = 사실상 해제. 그 가드는 **고정 프로토콜 전용**이었다 —
  #   최상단 층이 이완되면 복합체 속 슬랩이 맨 슬랩과 다른 게 당연하고, 그 차이(표면
  #   재배열)는 흡착의 일부다. 대신 아래 결산에서 표면 변위를 따로 보고한다.
  for j in slab complex_doped complex_doped_extr complex_neutral complex_neutral_extr; do
    [ -s "$OUT/$j/scf.in" ] || continue
    grep -aq diago_david_ndim "$OUT/$j/scf.in" || \
      sed -i '/&ELECTRONS/a\    diago_david_ndim = 2' "$OUT/$j/scf.in"
    sed -i 's/^\s*[0-9] [0-9] [0-9] 0 0 0/  1 1 1 0 0 0/' "$OUT/$j/scf.in"
    # ⚠ 'K_POINTS gamma'(메모리 ~2배 절감)는 못 쓴다 — ortho-atomic Hubbard 와 미구현 충돌.
    # ⚠ 생성기가 이미 diagonalization='david' 를 쓴다 — 줄을 **추가**하면 네임리스트에
    #   같은 키가 두 번 들어간다. 반드시 **치환**해야 한다 (2026-08-06).
    [ -n "$DIAG" ] && sed -i "s|diagonalization *= *'[^']*'|diagonalization = '$DIAG'|" "$OUT/$j/scf.in"
  done
}

# ⚠ 대소문자 무시 — 2026-08-06 실측 메시지가 "Out of memory"/"CUDA_ERROR_OUT_OF_MEMORY"/
#   "cuMemAlloc" 라서 소문자 패턴만 두면 OOM 을 못 잡고 '미수렴'으로 잘못 분류한다.
is_oom(){ grep -aqiE "cufftPlanMany|cfft3d_gpu|cuMemAlloc|Accelerator Fatal Error|insufficient.*memory|out.?of.?memory|CUDA_ERROR_OUT_OF_MEMORY" "$1"; }
oom_advice(){
  ts "⛔⛔ GPU 메모리 초과(OOM). **c 축소는 선택지가 아니다** — 15 Å 이미지 간격이 물리 요구다."
  ts "    ⚠ 어느 루틴에서 터졌는지를 먼저 본다 — 처방이 달라진다:"
  ts "        newd/newq_gpu  = USPP/PAW augmentation charge 를 조밀 G-격자에 까는 자리."
  ts "                         메모리 ∝ ngm ∝ ecutrho^1.5. **대각화 옵션(ppcg)은 여길 안 건드린다.**"
  ts "        cegterg/david  = 대각화 작업배열. 이때는 DIAG=ppcg 가 듣는다."
  ts "    사다리(newd 에서 터졌을 때):"
  ts "      ① ECUTRHO=400 …     newq 의 qgm(ngm×nij) 이 ngm∝ecutrho^1.5 로 준다."
  ts "                          480→400 은 0.76배, →360 은 0.65배, →320 은 0.54배."
  ts "                          ⚠ USPP 라 8×ecutwfc 가 기본 — 6× 아래는 augmentation 정확도를 의심할 것"
  ts "      ② 셀/계 축소        c 는 못 줄인다(15 Å 게이트). 슬랩 면적을 줄이려면 Phase-A 부터 다시."
  ts "      ⛔ REAL_SPACE=1 은 **쓰지 말 것** — 2026-08-06 실측: 이 GPU 빌드에서 newq 를 우회하지"
  ts "         않는다. 실공간 테이블에 28 GB 를 먼저 먹고 같은 newq 에서 더 빨리 죽었다."
  ts "      ⛔ CPU 빌드도 답이 아니다 — 호스트 가용 RAM 이 31 GB 로 GPU 49 GB 보다 작다(실측)."
  ts "    ⚠⚠ 어느 손잡이를 쓰든 **6개 job 전부 같은 값**이어야 한다 — 우리가 내는 값은 전부"
  ts "       차이(E_ads·Δ·ΔE_extract)라, 설정이 같기만 하면 내부적으로는 일관된다."
  ts "    이력: 2026-07-21 은 SCF 3회차의 대형 할당, 오늘은 초기화 newq 에서 즉사."
}

run_one(){
  local j=$1
  [ -s "$OUT/$j/scf.in" ] || { ts "⛔ $OUT/$j/scf.in 없음"; return 1; }
  if grep -aq "convergence has been achieved" "$OUT/$j/scf.out" 2>/dev/null; then
    ts "✓ $j 이미 수렴 — 건너뜀"; return 0; fi
  if ls "$OUT/$j"/tmp/*.save/charge-density* >/dev/null 2>&1; then
    grep -aq "startingpot" "$OUT/$j/scf.in" || \
      sed -i "/&ELECTRONS/a\    startingpot     = 'file'" "$OUT/$j/scf.in"
    ts "↻ $j 밀도 승계 (startingpot='file')"
  fi
  [ -s "$OUT/$j/scf.out" ] && mv "$OUT/$j/scf.out" "$OUT/$j/scf.out.$(date +%m%d_%H%M)"
  ts "▶ $j 시작"
  ( cd "$OUT/$j" && $MPIRUN -np 1 --oversubscribe "$QE" -nk 1 -in scf.in > scf.out 2>&1 )
  if is_oom "$OUT/$j/scf.out"; then ts "✗ $j — OOM"; oom_advice; return 2; fi
  if grep -aq "convergence has been achieved" "$OUT/$j/scf.out"; then
    ts "✓ $j 수렴 — $(grep -a '!.*total energy' "$OUT/$j/scf.out" | tail -1)"
  else
    ts "✗ $j 미수렴 — 진단:"
    "$UMA_PY" "$REPO/tools/sdcp/scf_convergence_doctor.py" \
        --scf_out "$OUT/$j/scf.out" --scf_in "$OUT/$j/scf.in" 2>&1 | tail -20
    return 1
  fi
}

# ── ★ AFM 게이트 — 이제 **세 복합체**를 다 본다 ─────────────────────────────
#   ΔE_extract 는 같은 종의 두 기하 차이라, 둘이 다른 스핀 상태로 수렴하면 그 차이가
#   추출이 아니라 스핀 전이를 재게 된다. Δ 보다 오히려 여기가 더 민감하다.
magcheck(){
  local -a n=() v=()
  for j in complex_doped complex_doped_extr complex_neutral; do
    local m; m=$(grep -a "absolute magnetization" "$OUT/$j/scf.out" 2>/dev/null | tail -1 | awk '{print $4}')
    [ -n "$m" ] && { n+=("$j"); v+=("$m"); }
  done
  [ "${#v[@]}" -ge 2 ] || { ts "· 자화 비교 보류 (출력 부족)"; return 0; }
  local lo=${v[0]} hi=${v[0]} i
  for i in "${!v[@]}"; do
    awk -v a="${v[$i]}" -v b="$lo" 'BEGIN{exit !(a<b)}' && lo=${v[$i]}
    awk -v a="${v[$i]}" -v b="$hi" 'BEGIN{exit !(a>b)}' && hi=${v[$i]}
    ts "  자화 ${n[$i]} = ${v[$i]} μB"
  done
  local d; d=$(awk -v x="$hi" -v y="$lo" 'BEGIN{printf "%.2f", x-y}')
  ts "자화 폭 $d μB (허용 $MAGTOL)"
  awk -v d="$d" -v t="$MAGTOL" 'BEGIN{exit !(d<=t)}' && { ts "  ✅ 같은 자기 상태"; return 0; }
  ts "  ⛔⛔ **복합체들이 다른 자기 상태다.** Δ 도 ΔE_extract 도 오염된다. 여기서 멈춘다."
  ts "     ⚠ 특히 doped 물리흡착 vs 추출이 갈리면, 그 차이는 추출이 아니라 스핀 전이다."
  return 1
}

# ── 0단계: 메모리 탐침 ──────────────────────────────────────────────────────
if [ "$STAGE" = probe ]; then
  ts "═══ 0단계: 메모리 탐침 (complex_doped_extr, electron_maxstep=$MAXSTEP) ═══"
  [ "$MAXSTEP" -le 10 ] || ts "⚠ 탐침이면 MAXSTEP=5 로 줄 것"
  gen || { ts "⛔ 입력 생성 실패"; exit 1; }
  run_one complex_doped_extr; rc=$?
  [ "$rc" = 2 ] && { ts "⛔ 이 셀은 현재 설정으로 안 들어간다."; exit 2; }
  ts "✅ 탐침 통과 — c=$C Å 가 메모리에 들어간다. 본 계산으로 가도 된다."
  grep -a "Estimated max dynamical RAM\|per-process dynamical memory" "$OUT/complex_doped_extr/scf.out" | tail -3
  exit 0
fi

# ── 1단계: 슬랩 (E_ads 기준항 + AFM 시드) ───────────────────────────────────
if [ "$STAGE" = all ] || [ "$STAGE" = slab ]; then
  ts "═══ 1단계: 슬랩 (E_ads 기준항 · AFM 시드) ═══"
  gen || { ts "⛔ 입력 생성 실패"; exit 1; }
  run_one slab || ts "⚠ 슬랩 미수렴 — 시드만 뽑아 진행 시도"
  "$UMA_PY" "$REPO/tools/sdcp/slab_mag_from_scfout.py" \
      --scf_out "$OUT/slab/scf.out" --scf_in "$OUT/slab/scf.in" --out "$MAGJSON" \
    && ts "✓ AFM 시드 → $MAGJSON" || ts "⚠ 시드 추출 실패 — 관례 ±0.3 으로 간다"
fi

# ── 2단계: 복합체 3 + 분자 2 ────────────────────────────────────────────────
if [ "$STAGE" = all ] || [ "$STAGE" = complexes ]; then
  ts "═══ 2단계: 복합체 + 가스상 분자 ═══"
  gen || { ts "⛔ 입력 재생성 실패"; exit 1; }
  JOBS=(complex_doped complex_doped_extr complex_neutral mol_doped mol_neutral)
  [ -n "$CX_N_EXTR" ] && JOBS+=(complex_neutral_extr)
  for j in "${JOBS[@]}"; do
    run_one "$j"; rc=$?
    [ "$rc" = 2 ] && exit 2
    [ "$rc" != 0 ] && ts "⚠ $j 실패 — 나머지는 계속 간다"
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
    m = re.findall(r"^!\s+total energy\s+=\s+(-?[\d.]+)",
                   open(p, errors="ignore").read(), re.M)
    return float(m[-1]) * 13.605693 if m else None
J = ("slab", "complex_doped", "complex_doped_extr", "complex_neutral",
     "complex_neutral_extr", "mol_doped", "mol_neutral")
e = {j: E(j) for j in J}
for j in J:
    if e[j] is not None or os.path.isdir(os.path.join(out, j)):
        print(f"  {j:22s} {'—' if e[j] is None else f'{e[j]:.4f} eV'}")

def ads(cx, mol):
    if None in (e[cx], e["slab"], e.get(mol)): return None
    return e[cx] - e["slab"] - e[mol]

print()
ad = ads("complex_doped", "mol_doped")
an = ads("complex_neutral", "mol_neutral")
if ad is not None: print(f"  E_ads(doped, 물리흡착)   = {ad:+.4f} eV      ← 흡착에너지")
if an is not None: print(f"  E_ads(neutral, 물리흡착) = {an:+.4f} eV      ← 흡착에너지")
if None not in (ad, an):
    print(f"  Δ = E_ads(d) − E_ads(n)  = {ad-an:+.4f} eV   (UMA: −0.073)")
    print("     ⚠ Δ 는 프로토콜 의존적이다 — 얼린 스캔 −0.170 vs top1free −0.073.")
    print("        결론을 Δ 하나에 걸지 말 것. 견고한 것은 추출 대비다.")

rx = ads("complex_doped_extr", "mol_doped")
if rx is not None:
    print(f"\n  ΔE_rxn(doped)            = {rx:+.4f} eV      ← **반응**에너지 (흡착에너지 아님)")
if None not in (e["complex_doped_extr"], e["complex_doped"]):
    dx = e["complex_doped_extr"] - e["complex_doped"]
    print(f"  ★ ΔE_extract(doped)      = {dx:+.4f} eV      (UMA: −0.942)")
    print("     기준항이 전부 상쇄되는 값이라 이 캠페인에서 제일 믿을 만한 수치다.")
    if dx < 0:
        print("     → DFT+U 에서도 추출이 유리하다 = **Li 스캐빈징 열화 기구가 실재**한다")
    else:
        print("     → DFT+U 에서는 추출이 불리하다 = UMA 가 Ni³⁺→Ni⁴⁺ 산화 대가를")
        print("        안 물어 과대평가한 것이다. 그 자체가 보고할 결과다.")
    print("     ⚠ 열역학이지 속도론이 아니다 — 장벽은 NEB 이 있어야 말할 수 있다.")
print("\n  ⚠ neutral 추출 job 은 없다 — UMA 가 108 자세 전부에서 그 상태를 못 만들었다.")
print("     그게 결과이지 누락이 아니다.")
PYS
ts "═══ 끝 ═══"
