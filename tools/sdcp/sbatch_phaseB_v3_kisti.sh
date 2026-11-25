#!/bin/bash
#SBATCH -J sdcp_pb3
#SBATCH -p amd_a100nv_8
#SBATCH -N 1
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:4
#SBATCH --time=12:00:00
#SBATCH -o /scratch/x3430a02/kgy/sdcp_phaseB_v3/logs/pb3_%j.out
#SBATCH -e /scratch/x3430a02/kgy/sdcp_phaseB_v3/logs/pb3_%j.err
#SBATCH --comment qe
# =============================================================================
# sbatch_phaseB_v3_kisti.sh — Phase-B v3 (job 6개) 를 **한 job 을 4 GPU 로 쪼개** 돈다.
#
# 왜 KISTI 로 옮기나 (gabia 실측, 2026-08-06)
#   226원자 · 18.3×10.9×46.4 Å · 스핀분극 DFT+U 는 48 GB A6000 한 장에 안 들어간다.
#     ecutrho 480          → newd_gpu/newq_gpu 즉사
#     480 + real_space     → peak 33.8 GB, 같은 newq 에서 즉사 (실공간 테이블이 28 GB 선점)
#     ecutrho 400          → peak 45.6 GB, 여전히 SCF iteration 0 에서 즉사
#   ecutrho 를 더 내려도 안 된다 — 파동함수/Davidson 배열은 ecutwfc·nbnd 로 정해지지
#   ecutrho 와 무관하고, 그것만으로 30 GB 대다.
#
# ⚠⚠ 옛 chain 스크립트와의 결정적 차이
#   옛 판은 `run_stream <gpu>` 로 **job 2개를 GPU 2장에 하나씩** 돌렸다. 그건 처리량을
#   늘릴 뿐 **한 job 의 메모리는 그대로**다 — 지금 문제엔 아무 도움이 안 된다.
#   여기서는 `mpirun -np 4 ... -nk 1` 로 **평면파(G-벡터)를 4랭크에 분산**한다.
#   ngm 도 npw 도 랭크당 1/4 이 되므로 newq 의 qgm 배열이 GPU 한 장당 1/4 로 떨어진다.
#   그래서 job 은 **순차**로 돈다 — 우리 병목은 처리량이 아니라 메모리다.
#
# 준비 (gabia 에서 입력을 만들고 옮긴다)
#   gabia$ ECUTRHO=400 bash tools/sdcp/run_phaseB_sdcp_v3.sh slab   # 입력만 생성(즉사해도 무방)
#   gabia$ tar czf pb3_in.tgz -C /data/work/runs/sdcp_v2/phaseB_v3 \
#            slab complex_doped complex_doped_extr complex_neutral mol_doped mol_neutral \
#            --exclude=tmp --exclude='scf.out*'
#   → KISTI $WORK_BASE 에 풀고, 각 scf.in 의 pseudo_dir 를 $PSEUDO 로 치환한다(아래 fix_pseudo).
#
#   kisti$ bash tools/sdcp/submit_phaseB_v3_kisti.sh 2   # afterany 체인 2단
#
# ⚠ KISTI QOS — 동시 제출 4개 제한. scancel 직후 재제출 금지(카운터 지연).
# =============================================================================
set -u
WORK_BASE=${WORK_BASE:-/scratch/x3430a02/kgy/sdcp_phaseB_v3}
PW=${PW:-/scratch/x3430a02/kgy/apps/qe-gpu/bin/pw.x}
PSEUDO=${PSEUDO:-/scratch/x3430a02/kgy/manuscript_support/pseudo}
NP=${NP:-4}                       # MPI 랭크 = GPU 장수. 메모리가 이 수만큼 쪼개진다.
export OMP_NUM_THREADS=${OMP_NUM_THREADS:-8}

JOBS=(mol_doped mol_neutral slab complex_doped complex_doped_extr complex_neutral)
NJOB=${#JOBS[@]}

mkdir -p "$WORK_BASE/logs"; cd "$WORK_BASE" || exit 1
[ -f ALL_DONE ] && { echo "ALL_DONE — 할 일 없음"; exit 0; }
echo "===== Phase-B v3  job=$SLURM_JOB_ID  np=$NP  $(date) ====="

# pseudo_dir 를 KISTI 경로로 (gabia 경로가 그대로 오면 즉사한다)
fix_pseudo () {
  local f=$1
  grep -aq "pseudo_dir" "$f" || return 0
  sed -i "s|pseudo_dir *= *'.*'|pseudo_dir      = '$PSEUDO'|" "$f"
}

run_one () {
  local j=$1 d="$WORK_BASE/$1"
  [ -s "$d/scf.in" ] || { echo "[$j] scf.in 없음 — 입력을 먼저 옮길 것"; return 1; }
  if grep -aq "JOB DONE" "$d/scf.out" 2>/dev/null; then echo "[$j] 이미 완료 — 건너뜀"; return 0; fi
  fix_pseudo "$d/scf.in"
  # ⚠ 중간에 끊긴 런은 tmp 를 지우고 처음부터. 격자·랭크 수가 바뀌면 밀도를 못 이어받는다.
  [ -f "$d/scf.out" ] && { echo "[$j] 이전 런 미완 — tmp 정리 후 재실행"; rm -rf "$d/tmp" "$d/scf.out"; }
  echo "[$j] START  $(date)  (np=$NP, 평면파 분산)"
  ( cd "$d" && mpirun -np "$NP" "$PW" -nk 1 -in scf.in > scf.out 2>&1 )
  if grep -aqiE "cufftPlanMany|cuMemAlloc|out.?of.?memory|CUDA_ERROR_OUT_OF_MEMORY" "$d/scf.out"; then
    echo "[$j] ⛔ OOM — np 를 더 키울 것 (NP=8 + --gres=gpu:8). 터진 자리:"
    grep -a "File:\|Function:" "$d/scf.out" | tail -2
    return 2
  fi
  grep -aq "JOB DONE" "$d/scf.out" && echo "[$j] DONE  $(date)" || echo "[$j] 미완(벽시계/에러)  $(date)"
}

for j in "${JOBS[@]}"; do
  run_one "$j"; rc=$?
  [ "$rc" = 2 ] && { echo "OOM 으로 중단 — 자원을 늘려 재제출"; exit 2; }
done

n=$(grep -l "JOB DONE" "$WORK_BASE"/*/scf.out 2>/dev/null | wc -l)
echo "===== segment 끝: $n/$NJOB 완료  $(date) ====="
[ "$n" -eq "$NJOB" ] || exit 0

touch "$WORK_BASE/ALL_DONE"
echo "===== 전부 완료 — 결산 ====="
python3 - "$WORK_BASE" <<'PYS'
import os, re, sys
out = sys.argv[1]
def E(j):
    p = os.path.join(out, j, "scf.out")
    if not os.path.isfile(p): return None
    m = re.findall(r"^!\s+total energy\s+=\s+(-?[\d.]+)", open(p, errors="ignore").read(), re.M)
    return float(m[-1]) * 13.605693 if m else None
J = ("slab", "complex_doped", "complex_doped_extr", "complex_neutral", "mol_doped", "mol_neutral")
e = {j: E(j) for j in J}
for j in J:
    print(f"  {j:22s} {'—' if e[j] is None else f'{e[j]:.4f} eV'}")
def ads(cx, mol):
    return None if None in (e[cx], e["slab"], e[mol]) else e[cx] - e["slab"] - e[mol]
ad, an = ads("complex_doped", "mol_doped"), ads("complex_neutral", "mol_neutral")
rx = ads("complex_doped_extr", "mol_doped")
print()
if ad is not None: print(f"  E_ads(doped, 물리흡착)   = {ad:+.4f} eV   ← 흡착에너지")
if an is not None: print(f"  E_ads(neutral, 물리흡착) = {an:+.4f} eV   ← 흡착에너지")
if None not in (ad, an):
    print(f"  Δ = E_ads(d) − E_ads(n)  = {ad-an:+.4f} eV   (UMA −0.073)")
    print("     ⚠ Δ 는 프로토콜 의존적이다 — 결론을 여기 걸지 말 것")
if rx is not None: print(f"\n  ΔE_rxn(doped)            = {rx:+.4f} eV   ← **반응**에너지 (흡착에너지 아님)")
if None not in (e["complex_doped_extr"], e["complex_doped"]):
    dx = e["complex_doped_extr"] - e["complex_doped"]
    print(f"  ★ ΔE_extract(doped)      = {dx:+.4f} eV   (UMA −0.942)")
    print("     기준항이 전부 상쇄되는 값 — 이 캠페인에서 제일 믿을 만하다.")
    print("     " + ("→ DFT+U 에서도 추출 유리 = **Li 스캐빈징 열화 기구 실재**" if dx < 0 else
                     "→ DFT+U 에서는 추출 불리 = UMA 가 Ni³⁺→Ni⁴⁺ 산화 대가를 안 문 것"))
    print("     ⚠ 열역학이지 속도론이 아니다 — 장벽은 NEB 이 있어야 말한다")
print("\n  ⚠ 6개 job 이 전부 같은 ecutrho 여야 위 차이값이 성립한다.")
print("     gabia OOM 때문에 480 → 400 Ry 로 내렸다면 그 사실을 논문 방법론에 명시할 것.")
PYS
