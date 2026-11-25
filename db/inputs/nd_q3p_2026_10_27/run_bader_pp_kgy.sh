#!/usr/bin/env bash
# run_bader_pp_kgy.sh — Nd Q3′ Bader 후처리 (kgy): 끝난 Bader SCF (R/bader/<모델>) 의 save 를 **읽기만** 해서
#   pp.x plot_num 17 (AE 가전자) → bader → bader_summary_zval.py (--roles 원래 역할 · --zval_from_upf · --sites).
#   카드 nd_q3p_same_cell_card_2026_10_27 §2 · §4 · 결정 D-2026-10-27-nd-q3p-same-cell (proposed 면 결과는 잠정).
#   규약 = Q3 (tools/electronic/run_nd_bader_from_scf_gabia.sh) 와 같다: kjpaw_psl · 70/560 · plot_num 17 · Henkelman bader ·
#   net = ZVAL − N_bader · `-p all_atom` 은 안 쓴다 (ACF.dat 만).
# ⚠ 후처리다 — SCF 를 돌리지 않는다. pp.x 는 GPU 빌드 bin 의 것을 MPI 1 랭크로 (환경은 tools/sei/qe_env.sh 의 ldd 경로).
#   곁에 GPU pw.x 가 돌 수 있어서 시작 전 VRAM 여유를 본다 (PP_MIN_FREE_MIB · 모자라면 시작하지 않는다).
# Env: W (worktree · 필수) · R (/home/kgy/work/runs/nd_q3p_1027) · BIN (/home/kgy/apps/qe-7.4.1-gpu/bin) ·
#      BADER (없으면 PATH → ~/apps/bader/bader → ~/bin/bader) · MODELS ("MLi_04 MP_07") · PY (python3) ·
#      PP_MIN_FREE_MIB (6000) · DRY_RUN (0) · MPIRUN (주면 qe_env.sh 대신 그대로 — 시험용)
# Exit: 0 끝 · 2 거부 (worktree · 입력이 저장소 판과 다름 · 이미 실행 중) · 3 SCF 미완료 · save 없음 ·
#       5 실행파일 · MPI · VRAM · 6 pp.x 실패 · 7 bader 실패 · 9 요약 실패
# ⛔ 못 하는 것: ELF (plot_num 8) 는 안 한다 (ELF SCF 가 끝난 뒤 따로) · 값을 판독하지 않는다 (카드 §5 비교는 회수 뒤) ·
#   bader 실행파일이 Q3 (gabia /data/apps/bader/bader) 와 같은 판인지는 판 줄과 md5 를 기록만 한다.
#   bash run_bader_pp_kgy.sh --selftest
set -u; set +H

main(){
  local W=${W:?W (worktree) is required} R=${R:-/home/kgy/work/runs/nd_q3p_1027}
  local BIN=${BIN:-/home/kgy/apps/qe-7.4.1-gpu/bin} PY=${PY:-python3} MODELS=${MODELS:-"MLi_04 MP_07"}
  local MINF=${PP_MIN_FREE_MIB:-6000} D=$W/db/inputs/nd_q3p_2026_10_27 OUT=$R/bader_pp
  local SUMM=$W/tools/electronic/bader_summary_zval.py m S pre od SAVE free rc
  mkdir -p "$OUT" || exit 2
  local LOG=$OUT/run.log
  say(){ echo "[$(date '+%F %T')] $*" | tee -a "$LOG"; }
  exec 8>"$OUT/.lock"; flock -n 8 || { say "⛔ 이미 실행 중 ($OUT/.lock)"; exit 2; }
  say "════ Nd Q3′ Bader 후처리 · HEAD $(git -C "$W" rev-parse --short HEAD 2>/dev/null || echo '?') · R $R · 모델 $MODELS ════"
  [ -f "$D/roles_manifest.json" ] && [ -f "$SUMM" ] || { say "⛔ worktree 에 manifest · 요약 도구가 없다 ($W)"; exit 2; }

  # ① 점검 — 입력 = 저장소 판 · SCF 수렴 · save
  for m in $MODELS; do
    S=$R/bader/$m
    cmp -s "$D/bader/$m/scf.in" "$S/scf.in" || { say "⛔ $m scf.in 이 저장소 판과 다르다 (또는 없다) — 다른 계일 수 있다"; exit 2; }
    grep -aq "JOB DONE" "$S/scf.out" 2>/dev/null && grep -aq "convergence has been achieved" "$S/scf.out" \
      || { say "⛔ $m SCF 가 끝나지 않았다 (JOB DONE · 수렴 줄) — $S/scf.out"; exit 3; }
    pre=$(sed -n "s/.*prefix *= *'\([^']*\)'.*/\1/p" "$S/scf.in" | head -1)
    od=$(sed -n "s/.*outdir *= *'\([^']*\)'.*/\1/p" "$S/scf.in" | head -1)
    case "$od" in /*) : ;; *) od="$S/${od#./}" ;; esac
    SAVE=${od%/}/$pre.save
    ls "$SAVE"/charge-density.* >/dev/null 2>&1 && [ -s "$SAVE/data-file-schema.xml" ] \
      || { say "⛔ $m save 가 없거나 불완전 ($SAVE)"; exit 3; }
    say "  ✓ $m — 입력 = 저장소 · SCF $(grep -a '^!' "$S/scf.out" | tail -1 | tr -s ' ') · save ✓"
  done

  # ② 실행파일 · MPI · 요약 도구
  [ -x "$BIN/pp.x" ] || { say "⛔ pp.x 없음 ($BIN)"; exit 5; }
  local BD=${BADER:-}
  if [ -z "$BD" ]; then
    for c in "$(command -v bader 2>/dev/null)" "$HOME/apps/bader/bader" "$HOME/bin/bader"; do
      [ -n "$c" ] && [ -x "$c" ] && { BD=$c; break; }
    done
  fi
  [ -n "$BD" ] && [ -x "$BD" ] || { say "⛔ bader 없음 — gabia /data/apps/bader/bader 를 ~/apps/bader/bader 로 옮기거나 BADER= 로 준다"; exit 5; }
  if [ -z "${MPIRUN:-}" ]; then
    # shellcheck disable=SC1090
    QE_FROM_LDD=1 PW="$BIN/pw.x" . "$W/tools/sei/qe_env.sh" _sourced >/dev/null 2>&1
    [ -z "${QE_ENV_ERROR:-}" ] && [ -n "${MPIRUN:-}" ] || { say "⛔ QE 환경 (ldd): ${QE_ENV_ERROR:-mpirun 없음}"; exit 5; }
  fi
  "$PY" "$SUMM" --selftest >/dev/null 2>&1 || { say "⛔ 요약 도구 selftest 실패"; exit 9; }
  say "  ✓ pp.x $BIN/pp.x · bader $BD (md5 $(md5sum "$BD" | cut -c1-8)) · mpirun $MPIRUN · 요약 selftest"
  [ "${DRY_RUN:-0}" = 1 ] && { say "DRY_RUN — 여기서 끝 (계산 0)"; exit 0; }

  # ③ 모델마다 pp.x → bader → 요약
  for m in $MODELS; do
    S=$R/bader/$m; mkdir -p "$OUT/$m"; cd "$OUT/$m" || exit 2
    pre=$(sed -n "s/.*prefix *= *'\([^']*\)'.*/\1/p" "$S/scf.in" | head -1)
    od=$(sed -n "s/.*outdir *= *'\([^']*\)'.*/\1/p" "$S/scf.in" | head -1)
    case "$od" in /*) : ;; *) od="$S/${od#./}" ;; esac
    if [ ! -s nd_rho_ae.cube ]; then
      free=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits 2>/dev/null | head -1 | tr -dc '0-9')
      [ -n "$free" ] && [ "$free" -ge "$MINF" ] || { say "⛔ $m VRAM 여유 ${free:-?} MiB < $MINF — pp.x 를 시작하지 않는다 (곁의 pw.x 보호)"; exit 5; }
      printf "&INPUTPP\n  prefix='%s', outdir='%s', plot_num=17, filplot='./nd_ae'\n/\n&PLOT\n  iflag=3, output_format=6, fileout='nd_rho_ae.cube'\n/\n" \
        "$pre" "${od%/}/" > pp_ae.in
      say "▶ $m pp.x plot_num=17 (AE 가전자 · save 읽기만 · VRAM 여유 $free MiB)"
      # shellcheck disable=SC2086
      $MPIRUN ${MPI_NP:--np 1} ${MPI_OVERSUB:-} "$BIN/pp.x" -in pp_ae.in > pp_ae.out 2>&1; rc=$?
      [ "$rc" = 0 ] && [ -s nd_rho_ae.cube ] || { say "⛔ $m pp.x rc=$rc 또는 cube 없음 — $OUT/$m/pp_ae.out"; exit 6; }
    fi
    say "  ✓ $m cube $(du -h nd_rho_ae.cube | cut -f1)"
    if [ ! -s ACF.dat ]; then
      say "▶ $m bader (ACF.dat · -p all_atom 안 씀)"
      "$BD" nd_rho_ae.cube > bader_run.out 2>&1; rc=$?
      [ "$rc" = 0 ] && [ -s ACF.dat ] || { say "⛔ $m bader rc=$rc 또는 ACF.dat 없음 — bader_run.out"; exit 7; }
    fi
    say "  ✓ $m bader $(grep -a 'NUMBER OF ELECTRONS' ACF.dat | tr -s ' ') · 판 $(grep -ai 'version' bader_run.out | head -1 | tr -s ' ')"
    cp -f "$S/scf.in" scf_input_copy.in
    "$PY" "$SUMM" --acf ACF.dat --struct "$S/scf.in" --zval_from_upf --sites nd_bader_sites.csv \
      --roles "$D/roles_manifest.json" --model "$m" --out nd_bader_summary.json > summary.txt 2>&1; rc=$?
    [ "$rc" = 0 ] && [ -s nd_bader_summary.json ] || { say "⛔ $m 요약 실패 — $OUT/$m/summary.txt"; exit 9; }
    git -C "$W" rev-parse HEAD > SOURCE_COMMIT 2>/dev/null || echo unknown > SOURCE_COMMIT
    md5sum "$BD" > bader_binary.md5
    find . -type f ! -name SHA256SUMS ! -name nd_ae -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS
    say "  ✓ $m 요약 → nd_bader_summary.json · SHA256SUMS $(wc -l < SHA256SUMS) 줄"
  done
  say "■ 끝 · 끝 코드 0 (회수: bader_pp/<모델>/ 의 ACF.dat · nd_bader_summary.json · nd_bader_sites.csv · pp_ae.* · bader_run.out · summary.txt · run.log — cube 는 kgy 에 둔다)"
  exit 0
}

selftest(){
  local T; T=$(mktemp -d); local n=0 f=0 REPO; REPO=$(cd "$(dirname "$0")/../../.." && pwd)
  ck(){ if [ "$2" = "$3" ]; then n=$((n+1)); else f=$((f+1)); echo "  ✗ $1 (기대 $3 · 실제 $2)"; fi; }
  mkdir -p "$T/W/db/inputs" "$T/W/tools/electronic" "$T/bin"
  cp -r "$REPO/db/inputs/nd_q3p_2026_10_27" "$T/W/db/inputs/"
  cp "$REPO/tools/electronic/bader_summary_zval.py" "$T/W/tools/electronic/"
  cat > "$T/bin/fakepy" <<'FAKE'
#!/usr/bin/env bash
[ "$1" = --selftest ] && exit 0
prev=""; for a in "$@"; do [ "$prev" = --out ] && echo "{}" > "$a"; prev=$a; done
echo "$*" >> __T__/summ.args; exit 0
FAKE
  cat > "$T/bin/pp.x" <<'FAKE'
#!/usr/bin/env bash
in=$2; echo "pp $PWD" >> __T__/pp.calls
grep -q "plot_num=17" "$in" || exit 1
grep -qF "outdir='./" "$in" && exit 1
f=$(sed -n "s/.*fileout='\([^']*\)'.*/\1/p" "$in"); echo cube > "$f"; exit 0
FAKE
  cat > "$T/bin/bader" <<'FAKE'
#!/usr/bin/env bash
echo "GRID BASED BADER ANALYSIS  (Version 1.05)"
printf "    #  X Y Z CHARGE MIN VOL\n  1 0 0 0 1.0 0.1 1.0\n NUMBER OF ELECTRONS: 1.0\n" > ACF.dat
FAKE
  cat > "$T/bin/mpirun" <<'FAKE'
#!/usr/bin/env bash
while [ $# -gt 0 ]; do case "$1" in -np) shift 2;; --*) shift;; *) break;; esac; done
exec "$@"
FAKE
  cat > "$T/bin/nvidia-smi" <<'FAKE'
#!/usr/bin/env bash
cat __T__/vram 2>/dev/null || echo 20000
FAKE
  sed -i "s#__T__#$T#g" "$T/bin/fakepy" "$T/bin/pp.x" "$T/bin/nvidia-smi"
  chmod +x "$T/bin/"*
  mk(){  # $1 = R
    for m in MLi_04 MP_07; do
      local S=$1/bader/$m pre; mkdir -p "$S"; cp "$REPO/db/inputs/nd_q3p_2026_10_27/bader/$m/scf.in" "$S/"
      pre=$(sed -n "s/.*prefix *= *'\([^']*\)'.*/\1/p" "$S/scf.in" | head -1)
      printf '!    total energy = -1.0 Ry\n     convergence has been achieved in  10 iterations\n   JOB DONE.\n' > "$S/scf.out"
      mkdir -p "$S/tmp/$pre.save"; echo d > "$S/tmp/$pre.save/charge-density.dat"; echo x > "$S/tmp/$pre.save/data-file-schema.xml"
    done; }
  run(){ ( PATH=$T/bin:$PATH W=$T/W R=$1 BIN=$T/bin BADER=$T/bin/bader PY=$T/bin/fakepy MPIRUN=$T/bin/mpirun main ) > "$1.log" 2>&1; echo $?; }
  mk "$T/R1"; ck "양성: 두 모델 끝 rc 0" "$(run "$T/R1")" 0
  ck "양성: ACF · 요약 · SHA256SUMS 둘 다" "$(ls "$T"/R1/bader_pp/*/ACF.dat "$T"/R1/bader_pp/*/nd_bader_summary.json "$T"/R1/bader_pp/*/SHA256SUMS 2>/dev/null | wc -l)" 6
  ck "양성: pp_ae.in = plot_num 17 · 절대 outdir" "$(grep -c "plot_num=17, filplot" "$T"/R1/bader_pp/MP_07/pp_ae.in):$(grep -c "outdir='$T/R1/bader/MP_07/tmp/'" "$T"/R1/bader_pp/MP_07/pp_ae.in)" "1:1"
  ck "양성: 요약에 --roles manifest · --model 모델" "$(grep -c -- "--roles .*roles_manifest.json --model MP_07" "$T/summ.args")" 1
  : > "$T/pp.calls"; ck "다시 돌리면 pp.x 를 안 부른다 (cube 있음)" "$(run "$T/R1"):$(wc -l < "$T/pp.calls")" "0:0"
  mk "$T/R2"; echo "! 바꿈" >> "$T/R2/bader/MP_07/scf.in"; ck "⛔음성: 입력이 저장소 판과 다르면 2" "$(run "$T/R2")" 2
  mk "$T/R3"; sed -i '/JOB DONE/d' "$T/R3/bader/MLi_04/scf.out"; ck "⛔음성: JOB DONE 없으면 3" "$(run "$T/R3")" 3
  mk "$T/R4"; rm -rf "$T"/R4/bader/MP_07/tmp; ck "⛔음성: save 없으면 3" "$(run "$T/R4")" 3
  mk "$T/R5"; ck "⛔음성: bader 없으면 5" "$( ( PATH=/usr/bin:/bin W=$T/W R=$T/R5 BIN=$T/bin BADER=$T/nope PY=$T/bin/fakepy MPIRUN=$T/bin/mpirun HOME=$T main ) > /dev/null 2>&1; echo $?)" 5
  mk "$T/R6"; echo 3000 > "$T/vram"; ck "⛔음성: VRAM 여유 모자라면 5 · cube 없음" "$(run "$T/R6"):$(ls "$T"/R6/bader_pp/*/nd_rho_ae.cube 2>/dev/null | wc -l)" "5:0"; rm -f "$T/vram"
  mk "$T/R7"; ck "DRY_RUN 은 계산 0" "$( ( PATH=$T/bin:$PATH W=$T/W R=$T/R7 BIN=$T/bin BADER=$T/bin/bader PY=$T/bin/fakepy MPIRUN=$T/bin/mpirun DRY_RUN=1 main ) > /dev/null 2>&1; echo $?):$(ls "$T"/R7/bader_pp/*/ACF.dat 2>/dev/null | wc -l)" "0:0"
  rm -rf "$T"; echo "selftest: ⭕ $n · ⛔ $f"; [ "$f" = 0 ]
}

case "${1:-}" in
  --selftest) selftest; exit $? ;;
  *) main ;;
esac
