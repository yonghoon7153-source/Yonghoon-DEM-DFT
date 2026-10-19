#!/usr/bin/env bash
# =============================================================================
# run_nd_bader_from_scf_gabia.sh — 이미 있는 PAW SCF 에서 AE Bader (자리별) 만 뽑는다 · gabia
#   Nd Q3 첫 칸 (결정 D-2026-10-19-nd-q23-ppswap-structure): 6 월 최종 Nd₂O₃@LPSCl1.6 (Nd@Li · 120 원자) 의
#   9 월 새 PP (frozen-4f) vc-relax 판 · 그 기하의 k 3 3 1 SCF (k-탐침 · kjpaw_psl 세트 · ecut 70/560) 를 읽기만 한다.
#
# 규약 = 기존 AE Bader 표 (bader_ae_modelc_LPSCl16.csv · run_lpsocl_bader_gabia.sh) 와 같다:
#   PAW kjpaw_psl · ecut 70/560 · pp.x plot_num=17 (AE **가전자** 밀도) · Henkelman bader · net = ZVAL − N_bader.
#   다른 점 (기록에 남긴다): occupations smearing (mv) · k 3 3 1 (호스트 표는 fixed · k444) — 절연체라 Bader 에 영향이 작다고 본다.
#   `bader -p all_atom` 은 안 쓴다 — 원자마다 격자 크기 파일을 120 개 쓴다 (전하 값은 같다 · ACF.dat 만 쓴다).
#
# 쓰는 법 (worktree 뿌리에서)
#   DRY_RUN=1 bash tools/electronic/run_nd_bader_from_scf_gabia.sh     # ① 점검만 (SCF 수렴 · save · 계보 · 실행파일 · MPI) — 계산 0
#   tmux new -d -s ndq3bader "bash $PWD/tools/electronic/run_nd_bader_from_scf_gabia.sh"
#
# 순서: ① 점검 — SCF 출력 수렴·JOB DONE · save (charge-density · data-file-schema) · 계보 (SCF 입력 셀·분율 좌표
#        = vc-relax 출력 'Begin final coordinates' 짝 · 셀 1e-4 Å · 좌표 1e-5) · pp.x · bader · libmpi (ldd)
#       ② pp.x plot_num=17 → nd_rho_ae.cube (SCF save 는 **읽기만** · filplot 은 OUT 에)
#       ③ bader nd_rho_ae.cube → ACF.dat
#       ④ 요약 — bader_summary_zval.py --zval_from_upf (UPF z_valence · 표와 다르면 멈춤) --sites (자리 분류 · 결과 전 거리)
#       ⑤ SHA256SUMS
# ⚠ CPU 후처리다 (pp.x · bader) — SCF·relax·nscf 실행이 아니다 (CLAUDE.md 'run 은 GPU' 대상 아님 · 결정 enforcement ③).
#   8 랭크 · OMP 1 · --mca btl self,vader · --allow-run-as-root (gabia root) · GPU 는 안 쓴다 (곁의 GPU pw.x 와 무관).
# 종료: 0 끝 · 3 SCF 미수렴/없음 · 4 계보 불일치 · 5 실행파일/MPI · 6 pp.x 실패 · 7 bader 실패 · 8 이미 실행 중 · 9 요약 실패
# ⛔ 못 하는 것: SCF 를 돌리지 않는다 (save 가 없으면 멈춘다) · ELF 는 안 한다 (NC 규약 · 새 SCF · GPU — 따로) ·
#    호스트와 자리별 비교는 못 한다 (호스트 표는 원소 평균뿐) · 자리 분류는 거리 하나 (bader_summary_zval.py docstring).
# =============================================================================
set -u; set +H
REPO=$(cd "$(dirname "$0")/../.." && pwd)
SCF_DIR=${SCF_DIR:-/data/work/runs/nd_ppswap_2026_09_16/kprobe_k331}
SCF_IN=${SCF_IN:-$SCF_DIR/kprobe.in}
SCF_OUT=${SCF_OUT:-$SCF_DIR/kprobe.out}
PREFIX=${PREFIX:-kprobe_k331}
OUTDIR=${OUTDIR:-$SCF_DIR/tmp_kprobe}
VCR_OUT=${VCR_OUT:-/data/work/runs/nd_ppswap_2026_09_16/lc_nd_doped_DFTrela/01_vcrelax.out}
OUT=${OUT:-/data/work/runs/nd_q3_bader_2026_10_19}
CPU=${CPU:-/data/apps/qe-7.4.1-cpu/bin}
BADER=${BADER:-/data/apps/bader/bader}
PY=${PY:-python3}
NP=${NP:-8}
mkdir -p "$OUT"
LOG=$OUT/run.log
say(){ echo "[$(date '+%F %T')] $*" | tee -a "$LOG"; }

exec 9>"$OUT/.lock"
flock -n 9 || { say "⛔ 이미 실행 중 ($OUT/.lock)"; exit 8; }
say "════ Nd AE Bader (기존 SCF 후처리) · HEAD $(git -C "$REPO" rev-parse --short HEAD 2>/dev/null) · OUT $OUT ════"

# ① 점검 ────────────────────────────────────────────────────────────────────
[ -s "$SCF_IN" ] && [ -s "$SCF_OUT" ] || { say "⛔ SCF 입력·출력 없음 ($SCF_IN · $SCF_OUT)"; exit 3; }
grep -aq "convergence has been achieved" "$SCF_OUT" && grep -aq "JOB DONE" "$SCF_OUT" \
  || { say "⛔ SCF 출력에 수렴 줄 · JOB DONE 이 없다 — $SCF_OUT"; exit 3; }
SAVE=$OUTDIR/$PREFIX.save
ls "$SAVE"/charge-density.* >/dev/null 2>&1 && [ -s "$SAVE/data-file-schema.xml" ] \
  || { say "⛔ save 없음 또는 불완전 ($SAVE — charge-density · data-file-schema.xml)"; exit 3; }
say "SCF ✓ $(grep -a '^!' "$SCF_OUT" | tail -1 | tr -s ' ') · 수렴 $(grep -ac 'convergence has been achieved' "$SCF_OUT") 회 · save ✓"

"$PY" - "$REPO" "$SCF_IN" "$VCR_OUT" "$OUT/lineage.json" <<'PY' 2>&1 | tee -a "$LOG"
import sys, json, hashlib
repo, scf_in, vcr_out, out = sys.argv[1:5]
sys.path.insert(0, f"{repo}/tools/comp1_v3"); sys.path.insert(0, f"{repo}/tools/electronic")
from build_lobster_paw_inputs import parse_final_cell, parse_final_positions
import bader_summary_zval as B
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
t = open(vcr_out, errors="replace").read()
cv, unit = parse_final_cell(t)
mode, block = parse_final_positions(t)
bad = []
if cv is None or block is None:
    bad.append("vc-relax 출력에 'Begin final coordinates' 짝 (셀 · 좌표) 이 없다")
else:
    cv = [[float(x) * (B.BOHR if unit == "bohr" else 1.0) for x in r] for r in cv]
    if unit not in ("angstrom", "bohr"):
        bad.append(f"vc-relax 셀 단위 {unit} 는 못 읽는다")
    sv = [l.split()[0] for l in block.strip().splitlines()]
    pv = [[float(x) for x in l.split()[1:4]] for l in block.strip().splitlines()]
    # 2026-10-19 gabia 실측: 9 월 vc-relax 출력의 최종 좌표는 **Å** 였다 (첫 판은 crystal 만 받아 Å 값을 분율로 읽고 멈췄다).
    #   Å · Bohr 는 같은 블록의 최종 셀로 분율로 바꿔 대조한다 — 옛 셀을 쓰지 않는다.
    m = mode.lower()
    if m.startswith("crystal"):
        fv = pv
    elif m.startswith("angstrom") or m.startswith("bohr"):
        sc = B.BOHR if m.startswith("bohr") else 1.0
        iv, _ = B._inv3(cv)
        fv = [[sum(r[c] * sc * iv[c][k] for c in range(3)) for k in range(3)] for r in pv]
    else:
        fv = pv
        bad.append(f"vc-relax 좌표 단위 {mode} 는 못 읽는다 (crystal · angstrom · bohr 만)")
    ss, cs, cells, _, _ = B.read_qe_input(scf_in)
    inv, _ = B._inv3(cells)
    fs = [[sum(r[c] * inv[c][k] for c in range(3)) for k in range(3)] for r in cs]
    dcell = max(abs(cv[i][j] - cells[i][j]) for i in range(3) for j in range(3))
    dfrac = max(abs((a - b + 0.5) % 1.0 - 0.5) for x, y in zip(fs, fv) for a, b in zip(x, y)) if len(fs) == len(fv) else 9.9
    if sv != ss:
        bad.append(f"원자 순서·종류가 다르다 (SCF {len(ss)} · vc-relax {len(sv)})")
    if dcell > 1e-4:
        bad.append(f"셀 차 {dcell:.2e} Å > 1e-4")
    if dfrac > 1e-5:
        bad.append(f"분율 좌표 차 {dfrac:.2e} > 1e-5")
rec = {"schema": "nd_bader_lineage/v1", "scf_in": scf_in, "scf_in_sha256": sha(scf_in), "vcrelax_out": vcr_out,
       "vcrelax_out_sha256": sha(vcr_out), "ok": not bad, "problems": bad}
if not bad:
    rec.update({"max_cell_diff_A": dcell, "max_frac_diff": dfrac, "nat": len(ss)})
open(out, "w").write(json.dumps(rec, ensure_ascii=False, indent=1) + "\n")
print(f"  계보 {'✓' if not bad else '✗'} — SCF 입력 = vc-relax 최종 짝" + ("" if not bad else " · " + " · ".join(bad))
      + (f" (셀 {dcell:.1e} Å · 좌표 {dfrac:.1e} · {len(ss)} 원자)" if not bad else ""))
sys.exit(0 if not bad else 1)
PY
[ "${PIPESTATUS[0]}" = 0 ] || { say "⛔ 계보 불일치 — 시작 안 함 ($OUT/lineage.json)"; exit 4; }

[ -x "$CPU/pp.x" ] || { say "⛔ pp.x 없음 ($CPU)"; exit 5; }
[ -x "$BADER" ] || { say "⛔ bader 없음 ($BADER)"; exit 5; }
LIBMPI=$(ldd "$CPU/pp.x" 2>/dev/null | awk '/libmpi\.so/{print $3; exit}')
case "$LIBMPI" in
  /lib/x86_64-linux-gnu/*|/usr/lib/x86_64-linux-gnu/*) MPIRUN=${MPIRUN:-/usr/bin/mpirun} ;;
  "") say "⛔ pp.x 에 libmpi 가 안 보인다 (ldd) — 직렬 빌드면 NP=1 · MPIRUN= 로 다시"; [ "${NP}" = 1 ] || exit 5; MPIRUN="" ;;
  *) MPIRUN=${MPIRUN:-$(dirname "$(dirname "$LIBMPI")")/bin/mpirun} ;;
esac
[ -z "$MPIRUN" ] || [ -x "$MPIRUN" ] || { say "⛔ mpirun 없음 ($MPIRUN · libmpi $LIBMPI)"; exit 5; }
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
say "실행파일 ✓ pp.x · bader · libmpi ${LIBMPI:-없음} → ${MPIRUN:-직렬} · np $NP · OMP 1"
[ "${DRY_RUN:-0}" = 1 ] && { say "DRY_RUN — 여기서 끝 (계산 0)"; exit 0; }

# ② pp.x plot_num=17 ────────────────────────────────────────────────────────
cd "$OUT" || exit 6
if [ ! -s nd_rho_ae.cube ]; then
  cat > pp_ae.in <<EOF
&INPUTPP
  prefix='$PREFIX', outdir='$OUTDIR', plot_num=17, filplot='./nd_ae'
/
&PLOT
  iflag=3, output_format=6, fileout='nd_rho_ae.cube'
/
EOF
  say "▶ pp.x plot_num=17 (AE 가전자 · save 읽기만)"
  if [ -n "$MPIRUN" ]; then
    "$MPIRUN" --allow-run-as-root --bind-to none --mca btl self,vader -np "$NP" "$CPU/pp.x" -in pp_ae.in > pp_ae.out 2>&1
  else
    "$CPU/pp.x" -in pp_ae.in > pp_ae.out 2>&1
  fi
  rc=$?
  [ "$rc" = 0 ] && [ -s nd_rho_ae.cube ] || { say "⛔ pp.x rc=$rc 또는 cube 없음 — pp_ae.out"; exit 6; }
fi
say "pp.x ✓ nd_rho_ae.cube $(du -h nd_rho_ae.cube | cut -f1)"

# ③ bader ───────────────────────────────────────────────────────────────────
if [ ! -s ACF.dat ]; then
  say "▶ bader (ACF.dat · -p all_atom 안 씀)"
  "$BADER" nd_rho_ae.cube > bader_run.out 2>&1
  rc=$?
  [ "$rc" = 0 ] && [ -s ACF.dat ] || { say "⛔ bader rc=$rc 또는 ACF.dat 없음 — bader_run.out"; exit 7; }
fi
say "bader ✓ $(grep -a 'NUMBER OF ELECTRONS' ACF.dat | tr -s ' ')"

# ④ 요약 ────────────────────────────────────────────────────────────────────
cp -f "$SCF_IN" scf_input_copy.in
"$PY" "$REPO/tools/electronic/bader_summary_zval.py" --acf ACF.dat --struct "$SCF_IN" --zval_from_upf \
  --sites nd_bader_sites.csv --out nd_bader_summary.json 2>&1 | tee -a "$LOG"
[ "${PIPESTATUS[0]}" = 0 ] || { say "⛔ 요약 실패"; exit 9; }

# ⑤ 끝 줄 → 해시 ─────────────────────────────────────────────────────────────
git -C "$REPO" rev-parse HEAD > SOURCE_COMMIT 2>/dev/null || echo unknown > SOURCE_COMMIT
say "■ 끝 · 끝 코드 0"
find . -type f ! -name '.lock' ! -name SHA256SUMS ! -name 'nd_ae' -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS
echo "SHA256SUMS $(wc -l < SHA256SUMS) 줄 (회수: ACF.dat · nd_bader_summary.json · nd_bader_sites.csv · lineage.json · pp_ae.* · bader_run.out · run.log · SOURCE_COMMIT — cube 는 gabia 에 둔다)"
exit 0
