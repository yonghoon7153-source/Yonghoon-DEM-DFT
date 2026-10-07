#!/usr/bin/env bash
# ps73 감쇠 가지 실험 (DEMP-01) — WSL 러너.  정본 설명 = 같은 폴더 README.md (§6 명령 · §7 가드 · §10 확인 안 된 점).
#
#   bash run_branch.sh                       # 기본 = 0 단계 문법 시험 (t0) + arm B (서보 · 주 측정)
#   bash run_branch.sh --t0-only             # t0 만 (수 분)
#   bash run_branch.sh --arm A               # t0 + A (원 프로토콜 재현 · 선택)
#   bash run_branch.sh --arm C1 --arm C2     # t0 + C1 → C2 (선택 · WORK_ROOT 에 A 와 B 가 끝까지 돈 기록이 있어야 한다)
#   bash run_branch.sh --skip-t0 --arm B     # 같은 덱 묶음 (SHA256SUMS) 으로 통과한 t0 가 WORK_ROOT 에 있을 때만
#
# 환경 변수 (괄호 = 기본):
#   WORK_ROOT (~/ps73_branch_20261007)  in/ 에 체크포인트 · 런 폴더는 그 아래 <arm>_<시각>/ 로 새로 만든다 (있으면 거부 · 덮어쓰지 않는다)
#   CKPT ($WORK_ROOT/in/restart_compress_3100000.bin)  · NP (15) · MPIRUN (mpirun) · MPIRUN_FLAGS (--oversubscribe --bind-to none)
#   LMP  LIGGGHTS 실행 파일 — 없으면 ~/lhs_local/lhs00_110/run_lhs00_110.sh 의 mpirun 줄에서 읽는다
#   SERVO_KP · SERVO_VMAX · HOLD_MAX   B 등록값 (30 · 0.01 · 300) 을 바꿀 때만 — 바꾸면 이탈이다 (run_manifest.txt 에 남는다)
#   ALLOW_CONCURRENT=1 (다른 LIGGGHTS 가 돌아도 진행) · FORCE_DISK=1 (빈 칸 20 GB 미만이어도) · FORCE_C=1 (A · B 완주 기록 없이 C)
#
# 지키는 것: 체크포인트 크기 · sha256 · 덱 묶음 SHA256SUMS 를 먼저 본다 · 리포 체크아웃이 런 도중 바뀌어도 되게 kit 사본으로 다시 실행한다 ·
#   mpirun --oversubscribe --bind-to none -np N 짝 · 런마다 새 폴더 · 덱은 그 폴더 사본을 읽는다 (jump SELF 가 덱을 다시 읽기 때문).
set -uo pipefail

EXPECT_SHA=82234bea543ae369043f54d4379c6451cdab5a404213c0ecf0a698638bf4b3ee
EXPECT_SIZE=80807696
WORK_ROOT=${WORK_ROOT:-$HOME/ps73_branch_20261007}
CKPT=${CKPT:-$WORK_ROOT/in/restart_compress_3100000.bin}
NP=${NP:-15}
MPIRUN=${MPIRUN:-mpirun}
MPIRUN_FLAGS=${MPIRUN_FLAGS:---oversubscribe --bind-to none}
STAMP=${BRANCH_STAMP:-$(date +%Y%m%d_%H%M%S)}
SELF_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

die() { echo "⛔ $*" >&2; exit 1; }
say() { echo "[$(date +%H:%M:%S)] $*"; }

# ── 0. kit 사본으로 다시 실행 (리포 체크아웃이 런 도중 바뀌어도 이 사본으로 돈다) ─────────────────────
if [ "${BRANCH_KIT:-0}" != 1 ]; then
  [ -d "$WORK_ROOT" ] || die "WORK_ROOT 가 없다: $WORK_ROOT"
  case "$WORK_ROOT" in *' '*) die "WORK_ROOT 에 공백이 있다 — LIGGGHTS 변수로 넘길 수 없다";; esac
  KIT="$WORK_ROOT/kit_$STAMP"
  mkdir "$KIT" || die "kit 폴더를 만들 수 없다 (이미 있다?): $KIT"
  for f in in.branch_t0_syntax.liggghts in.branch_A.liggghts in.branch_B.liggghts in.branch_C1.liggghts \
           in.branch_C2.liggghts plate_branch3100000.stl run_branch.sh make_branch_decks.py analyze_branch.py SHA256SUMS; do
    cp -p "$SELF_DIR/$f" "$KIT/" || die "kit 복사 실패: $f"
  done
  REF_TGZ="$SELF_DIR/../ps73_compaction_curve_20261006/raw/ps73_curve_1.tgz"
  if [ -f "$REF_TGZ" ]; then
    tar -xzf "$REF_TGZ" -O post_ps_7_3_r45/mesh_3100000.stl > "$KIT/ref_mesh_3100000.stl" 2>/dev/null \
      || rm -f "$KIT/ref_mesh_3100000.stl"
  fi
  ( cd "$SELF_DIR" && echo "head=$(git rev-parse HEAD 2>/dev/null || echo unknown)" \
      && echo "dirty_here=$(git status --porcelain -- . 2>/dev/null | wc -l)" ) > "$KIT/repo_commit.txt" 2>/dev/null || true
  say "kit = $KIT"
  BRANCH_KIT=1 BRANCH_STAMP="$STAMP" KIT="$KIT" exec bash "$KIT/run_branch.sh" "$@"
fi
KIT=${KIT:-$SELF_DIR}

# ── 인자 ─────────────────────────────────────────────────────────────────────
ARMS=(); DO_T0=1; T0_ONLY=0
while [ $# -gt 0 ]; do
  case "$1" in
    --arm) shift; [ $# -gt 0 ] || die "--arm 뒤에 A | B | C1 | C2"
           case "$1" in A|B|C1|C2) ARMS+=("$1");; *) die "모르는 arm: $1";; esac;;
    --t0-only) T0_ONLY=1;;
    --skip-t0) DO_T0=0;;
    -h|--help) sed -n '2,22p' "$KIT/run_branch.sh"; exit 0;;
    *) die "모르는 인자: $1 (--help)";;
  esac
  shift
done
if [ "$T0_ONLY" = 1 ]; then ARMS=(); DO_T0=1; fi
if [ "$T0_ONLY" = 0 ] && [ ${#ARMS[@]} -eq 0 ]; then ARMS=(B); fi

# ── 1. 사전 점검 ─────────────────────────────────────────────────────────────
TMPL_RUN="$HOME/lhs_local/lhs00_110/run_lhs00_110.sh"
env_hint() {   # 로컬 러너가 mpirun 앞에서 켜는 환경 (conda · module · source · PATH) 을 보여 준다
  [ -f "$TMPL_RUN" ] || return 0
  echo "  · 참고 — $TMPL_RUN 의 환경 줄 (필요하면 같은 것을 먼저 켜고 다시):"
  grep -nE 'conda activate|source |module load|export (PATH|LD_LIBRARY_PATH)' "$TMPL_RUN" | sed 's/^/      /'
}

resolve_lmp() {
  if [ -z "${LMP:-}" ] && [ -f "$TMPL_RUN" ]; then
    LMP=$(grep -E '^[^#]*mpirun' "$TMPL_RUN" | head -1 | sed -nE 's/.*-np[[:space:]]+[0-9]+[[:space:]]+([^[:space:]]+).*/\1/p')
    [ -n "$LMP" ] && say "LMP 를 $TMPL_RUN 의 mpirun 줄에서 읽었다: $LMP"
  fi
  [ -n "${LMP:-}" ] || { env_hint; die "LMP (LIGGGHTS 실행 파일) 를 정해 달라 — 예: LMP=~/src/LIGGGHTS-PUBLIC/src/lmp_auto bash run_branch.sh"; }
  LMP="${LMP/#\~/$HOME}"
  if [ ! -x "$LMP" ]; then
    if command -v "$LMP" >/dev/null 2>&1; then LMP=$(command -v "$LMP"); else env_hint; die "LMP 를 실행할 수 없다: $LMP"; fi
  fi
  LMP=$(readlink -f "$LMP")
}

preflight() {
  say "사전 점검"
  ( cd "$KIT" && sha256sum -c --quiet SHA256SUMS ) || die "kit 파일이 SHA256SUMS 와 다르다 — 덱을 손으로 고쳤나? (make_branch_decks.py 로 다시 만든다)"
  echo "  ✓ 덱 묶음 SHA256SUMS"
  [ -f "$CKPT" ] || die "체크포인트가 없다: $CKPT"
  local sz sh
  sz=$(stat -c %s "$CKPT"); [ "$sz" = "$EXPECT_SIZE" ] || die "체크포인트 크기 $sz ≠ $EXPECT_SIZE"
  sh=$(sha256sum "$CKPT" | cut -d' ' -f1); [ "$sh" = "$EXPECT_SHA" ] || die "체크포인트 sha256 $sh ≠ $EXPECT_SHA"
  echo "  ✓ 체크포인트 $sz B · sha256 $sh"
  resolve_lmp; echo "  ✓ LMP = $LMP"
  command -v "$MPIRUN" >/dev/null 2>&1 || { env_hint; die "mpirun 이 없다: $MPIRUN"; }
  case "$NP" in ''|*[!0-9]*) die "NP 가 정수가 아니다: $NP";; esac
  [ "$NP" -ge 1 ] || die "NP ≥ 1"
  echo "  ✓ $MPIRUN $MPIRUN_FLAGS -np $NP"
  local free_kb; free_kb=$(df -Pk "$WORK_ROOT" | awk 'NR==2{print $4}')
  if [ "${free_kb:-0}" -lt 20000000 ] && [ "${FORCE_DISK:-0}" != 1 ]; then
    die "WORK_ROOT 빈 칸 $((free_kb / 1048576)) GB < 20 GB (B ≈ 2 GB · A ≈ 4.5 GB · C 각 ≈ 2 GB — FORCE_DISK=1 로 넘김)"
  fi
  echo "  ✓ 빈 칸 $((free_kb / 1048576)) GB"
  local others; others=$(pgrep -a -x "$(basename "$LMP")" 2>/dev/null || true)
  if [ -n "$others" ]; then
    echo "$others"
    [ "${ALLOW_CONCURRENT:-0}" = 1 ] || die "다른 LIGGGHTS 가 돌고 있다 — 코어를 나눠 쓰면 느려진다 (ALLOW_CONCURRENT=1 로 넘김)"
  fi
}

# ── 2. 한 단계 돌리기 ────────────────────────────────────────────────────────
CUR_RUN=""
trap '[ -n "$CUR_RUN" ] && echo "interrupted=$(date -Iseconds)" >> "$CUR_RUN/run_manifest.txt"; exit 130' INT TERM

run_stage() {   # $1 = 이름 (t0 · A · B · C1 · C2)   $2 = 덱 파일   그 뒤 = 덧붙일 -var
  local label=$1 deck=$2; shift 2
  local run="$WORK_ROOT/${label}_$STAMP"
  mkdir "$run" || die "런 폴더가 이미 있다 (덮어쓰지 않는다): $run"
  mkdir "$run/post" "$run/stop" "$run/end" "$run/end_relax" "$run/post_hold" "$run/restart" || die "하위 폴더 실패"
  cp -p "$KIT/$deck" "$KIT/plate_branch3100000.stl" "$run/" || die "덱 복사 실패"
  CUR_RUN=$run
  {
    echo "arm=$label"
    echo "deck=$deck"
    echo "deck_sha256=$(sha256sum "$run/$deck" | cut -d' ' -f1)"
    echo "ckpt=$CKPT"
    echo "ckpt_sha256=$EXPECT_SHA"
    echo "lmp=$LMP"
    echo "lmp_sha256=$(sha256sum "$LMP" | cut -d' ' -f1)"
    echo "np=$NP"
    echo "mpirun=$MPIRUN $MPIRUN_FLAGS"
    echo "kit=$KIT"
    sed 's/^/repo_/' "$KIT/repo_commit.txt" 2>/dev/null
    echo "extra_vars=${*:-none}"
    echo "start=$(date -Iseconds)"
  } > "$run/run_manifest.txt"
  say "▶ $label 시작 → $run   (진행: tail -f $run/screen.out | grep -E 'Current Pressure|Hold|BRANCH|ERROR')"
  # shellcheck disable=SC2086
  ( cd "$run" && export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 && \
    "$MPIRUN" $MPIRUN_FLAGS -np "$NP" "$LMP" -in "$run/$deck" -log "$run/log.liggghts" \
      -var ckpt "$CKPT" -var out "$run" -var plate_stl "$run/plate_branch3100000.stl" "$@" ) > "$run/screen.out" 2>&1
  local rc=$?
  { echo "end=$(date -Iseconds)"; echo "rc=$rc"; } >> "$run/run_manifest.txt"
  LAST_RUN=$run; LAST_RC=$rc
  say "■ $label 끝 rc=$rc"
}

last_result() { grep '^result=' "$1/branch_summary.txt" 2>/dev/null | tail -1 | cut -d= -f2; }
kv() { grep "^$2=" "$1/branch_summary.txt" 2>/dev/null | tail -1 | cut -d= -f2-; }

report_tgz() {   # 작은 파일만 (덤프 · restart 는 WSL 에 남긴다)
  local r=$1 base; base=$(basename "$r")
  local list=()
  for f in branch_summary.txt branch_summary_forced_trip.txt branch_trace.csv run_manifest.txt screen.out log.liggghts \
           analysis_branch.json t0_verdict.txt plate_servo_stop.stl; do
    [ -f "$r/$f" ] && list+=("$base/$f")
  done
  for d in stop end end_relax post post_hold; do
    for f in "$r/$d"/mesh_*.stl; do [ -f "$f" ] && list+=("$base/$d/$(basename "$f")"); done
  done
  tar -czf "$r.report.tgz" -C "$WORK_ROOT" "${list[@]}" && say "보낼 것: $r.report.tgz  sha256 $(sha256sum "$r.report.tgz" | cut -d' ' -f1)"
}

stop_plate_check() {   # $1 = 런 폴더 — 덱 공식 판 높이 (BRANCH_STOP) = 멈춘 step 의 판 메시 덤프 꼭짓점 (6 자리)
  local r=$1 line s zf zm
  line=$(grep -o 'BRANCH_STOP arm=[^ ]* step=[0-9]* plate_z_deck=[^ ]*' "$r/screen.out" | tail -1)
  if [ -z "$line" ]; then echo "  ✗ BRANCH_STOP 줄이 없다"; return 1; fi
  s=$(echo "$line" | sed 's/.*step=\([0-9]*\).*/\1/')
  zf=${line##*plate_z_deck=}
  zm=$(grep -o 'vertex .*' "$r/stop/mesh_$s.stl" 2>/dev/null | awk '{print $4}' | sort -u)
  if [ -n "$zm" ] && [ "$(echo "$zm" | wc -l)" = 1 ] && \
     [ "$(awk -v a="$zf" 'BEGIN{printf "%.6g", a}')" = "$(awk -v a="$zm" 'BEGIN{printf "%.6g", a}')" ]; then
    echo "  ✓ 멈춘 step $s 판 높이: 덱 공식 $zf = 메시 덤프 $zm (6 자리)"
    return 0
  fi
  echo "  ✗ 멈춘 step $s 판 높이: 덱 공식 $zf ↔ 메시 덤프 '$zm'"
  return 1
}

# ── 3. t0 판정 ───────────────────────────────────────────────────────────────
check_t0() {
  local r=$1 bad=0 m
  echo "  t0 점검 ($r)"
  if [ "$LAST_RC" != 0 ]; then echo "  ✗ mpirun rc=$LAST_RC"; bad=1; fi
  if grep -q "LIGGGHTS-PUBLIC 3.8.0" "$r/screen.out"; then echo "  ✓ 배너 LIGGGHTS-PUBLIC 3.8.0"; else echo "  ✗ 배너에 LIGGGHTS-PUBLIC 3.8.0 없음"; bad=1; fi
  if grep -q "3d5c00f" "$r/screen.out"; then echo "  ✓ git commit 3d5c00f (서보 · 파서 소스를 확인한 커밋)"
  else echo "  ⚠ 배너에 3d5c00f 없음 — 문법을 확인한 소스와 다른 빌드일 수 있다 (README §10 · 진행은 한다)"; fi
  for m in "T0_G1 PASS" "T0_G3 PASS" "T0_PZ PASS" "T0_SERVO PASS" "T0_DONE" "BRANCH_HOLD_DONE arm=t0 status=BUDGET_EXHAUSTED" \
           "BRANCH_DONE arm=t0" "BRANCH_GUARD_TRIP arm=t0 reason=t0_forced" "BRANCH_SCRIPT_END arm=t0"; do
    if grep -q "$m" "$r/screen.out"; then echo "  ✓ $m"; else echo "  ✗ '$m' 없음"; bad=1; fi
  done
  if grep -n -E "ERROR|Segmentation|Abort" "$r/screen.out" | head -5; then bad=1; fi
  # G3 — setup 뒤 첫 정규 줄 3101000: 원자 수 같음 · 압력 5 % (원 로그 r8 0.29635467) · resume 절차 §3
  local g3; g3=$(awk '$1=="3101000" && NF==5 && $4+0>0 {print $2, $5; exit}' "$r/screen.out")
  if [ -n "$g3" ] && awk -v a="${g3% *}" -v p="${g3#* }" 'BEGIN{d=p/0.29635467-1; if(d<0)d=-d; exit !(a==160420 && d<=0.05)}'; then
    echo "  ✓ G3 3101000: 원자 · 압력 $g3 (기준 160420 · 0.29635467 · 5 %)"
  else echo "  ✗ G3 3101000 줄 '$g3'"; bad=1; fi
  local nmiss=0 f
  for f in post/atom_3100000.liggghts post/mesh_3100000.stl stop/atom_3105000.liggghts stop/contact_3105000.liggghts \
           stop/mesh_3105000.stl end_relax/atom_3105200.liggghts end_relax/contact_3105200.liggghts end_relax/mesh_3105200.stl \
           end/atom_3106200.liggghts end/contact_3106200.liggghts end/mesh_3106200.stl plate_servo_stop.stl \
           restart/restart_stop_3105000.bin restart/restart_end_relax_3105200.bin restart/restart_end_3106200.bin \
           restart/restart_guard_3106200.bin; do
    if [ ! -s "$r/$f" ]; then echo "  ✗ 파일 없음: $f"; nmiss=$((nmiss + 1)); bad=1; fi
  done
  [ "$nmiss" = 0 ] && echo "  ✓ 스냅숏 · restart 파일 16 개 (멈춤 · 이완 끝 · 서보 끝 · 가드)"
  stop_plate_check "$r" || bad=1
  # G2 — 체크포인트 step 의 판 메시 = 원 런 mesh_3100000.stl (리포 tgz)
  if [ -f "$KIT/ref_mesh_3100000.stl" ]; then
    if cmp -s "$KIT/ref_mesh_3100000.stl" "$r/post/mesh_3100000.stl"; then echo "  ✓ G2 판 메시 mesh_3100000.stl = 원 런"
    else echo "  ✗ G2 판 메시가 원 런과 다르다"; bad=1; fi
  else echo "  ⚠ G2 판 메시 참조 없음 (리포 tgz 를 못 읽었다)"; fi
  # G2 — 원자 (선택: 원 런 atom_3100000.liggghts 를 $WORK_ROOT/in/ 에 두었을 때) · id 정렬 · id type x y z radius vx vy vz
  if [ -f "$WORK_ROOT/in/atom_3100000.liggghts" ]; then
    local h1 h2
    h1=$(awk 'f{print $1,$2,$3,$4,$5,$6,$7,$8,$9} /^ITEM: ATOMS/{f=1}' "$WORK_ROOT/in/atom_3100000.liggghts" | sort -n -k1,1 | md5sum | cut -d' ' -f1)
    h2=$(awk 'f{print $1,$2,$3,$4,$5,$6,$7,$8,$9} /^ITEM: ATOMS/{f=1}' "$r/post/atom_3100000.liggghts" | sort -n -k1,1 | md5sum | cut -d' ' -f1)
    if [ "$h1" = "$h2" ]; then echo "  ✓ G2 원자 (id 정렬 · 위치 · 속도) md5 $h1"; else echo "  ✗ G2 원자 md5 $h1 ≠ $h2"; bad=1; fi
  else echo "  · G2 원자 생략 (선택 — README §6 의 atom_3100000.liggghts 복사)"; fi
  # 서보 판 높이 = 끝 메시 꼭짓점
  local zs zp
  zs=$(grep -o 'vertex .*' "$r/end/mesh_3106200.stl" 2>/dev/null | awk '{print $4}' | sort -u | tr '\n' ' ')
  zp=$(grep -o 'BRANCH_END_STATE arm=t0 dir=end step=[0-9]* plate_z_deck=[^ ]*' "$r/screen.out" | tail -1 | sed 's/.*plate_z_deck=//')
  echo "  · 서보 판: 끝 메시 꼭짓점 z = $zs · f_plate_servo[12] = $zp"
  # 속도 → 예상 시간
  local lt; lt=$(grep -E 'Loop time of [0-9.]+ on [0-9]+ procs for 5000 steps' "$r/screen.out" | head -1)
  if [ -n "$lt" ]; then
    local rate; rate=$(echo "$lt" | awk '{print 5000/$4}')
    echo "  · 속도: $lt → $rate step/s"
    awk -v r="$rate" 'BEGIN{printf "  · 어림 (README §5): B 0.75 M step ≈ %.1f h (예산 끝 1.53 M ≈ %.1f h) · A 0.13 M ≈ %.1f h · C1 ≈ %.1f h · C2 ≈ %.1f h\n", 750000/r/3600, 1525000/r/3600, 125000/r/3600, 560000/r/3600, 690000/r/3600}'
  fi
  if [ "$bad" = 0 ]; then echo "T0=PASS sums=$(sha256sum "$KIT/SHA256SUMS" | cut -d' ' -f1)" > "$r/t0_verdict.txt"; say "✓ t0 PASS"
  else echo "T0=FAIL" > "$r/t0_verdict.txt"; say "✗ t0 FAIL — arm 을 돌리지 않는다 ($r/screen.out 을 보낼 것)"; fi
  return $bad
}

t0_passed_before() {
  local want; want=$(sha256sum "$KIT/SHA256SUMS" | cut -d' ' -f1)
  grep -l "^T0=PASS sums=$want" "$WORK_ROOT"/t0_*/t0_verdict.txt >/dev/null 2>&1
}

done_before() {   # $1 = A | B — 끝까지 돈 기록 (마지막 result=DONE)
  local s
  for s in "$WORK_ROOT"/"$1"_*/branch_summary.txt; do
    [ -f "$s" ] || continue
    [ "$(grep '^result=' "$s" | tail -1 | cut -d= -f2)" = DONE ] && return 0
  done
  return 1
}

check_arm() {
  local r=$1 label=$2 res; res=$(last_result "$r")
  echo "  $label 결과: result=${res:-없음} · rc=$LAST_RC"
  echo "    멈춤 step $(kv "$r" stop_step) · 두께 $(kv "$r" stop_thickness_um) µm · 판 압력 $(kv "$r" stop_press_deckMPa) 덱 MPa"
  [ -n "$(kv "$r" hold_status)" ] && echo "    서보 유지 $(kv "$r" hold_status) · 덩어리 $(kv "$r" hold_chunks)"
  echo "    끝 step $(kv "$r" end_step) · 두께 $(kv "$r" end_thickness_um) µm · 판 압력 $(kv "$r" end_press_deckMPa) 덱 MPa · 원자 $(kv "$r" atoms_end)"
  if [ "$res" = GUARD_TRIP ]; then echo "    ⛔ 가드: $(kv "$r" guard) @ step $(kv "$r" guard_step) — README §7"; fi
  [ -n "$(kv "$r" stop_step)" ] && { stop_plate_check "$r" || echo "    ⚠ 판 높이 기록이 메시와 다르다 — 두께는 analysis_branch.json (메시 기준) 을 쓴다"; }
  if command -v python3 >/dev/null 2>&1; then
    python3 -I "$KIT/analyze_branch.py" "$r" || echo "    ⚠ analyze_branch.py 실패 (런 결과는 그대로)"
  fi
  report_tgz "$r"
  [ "$res" = DONE ] && [ "$LAST_RC" = 0 ]
}

# ── 4. 차례대로 ──────────────────────────────────────────────────────────────
preflight
say "작업 = t0:$([ "$DO_T0" = 1 ] && echo 예 || echo 아니오) · arm: ${ARMS[*]:-없음} · NP $NP · WORK_ROOT $WORK_ROOT"

if [ "$DO_T0" = 1 ]; then
  run_stage t0 in.branch_t0_syntax.liggghts
  check_t0 "$LAST_RUN" || { report_tgz "$LAST_RUN"; exit 2; }
  report_tgz "$LAST_RUN"
else
  t0_passed_before || die "--skip-t0 은 같은 덱 묶음으로 통과한 t0 가 WORK_ROOT 에 있을 때만"
  say "t0 생략 — 같은 덱 묶음의 t0 PASS 기록이 있다"
fi

for arm in ${ARMS[@]+"${ARMS[@]}"}; do
  extra=()
  case "$arm" in
    B)
      [ -n "${SERVO_KP:-}" ] && extra+=(-var servo_kp "$SERVO_KP")
      [ -n "${SERVO_VMAX:-}" ] && extra+=(-var servo_vmax "$SERVO_VMAX")
      [ -n "${HOLD_MAX:-}" ] && extra+=(-var hold_max "$HOLD_MAX")
      [ ${#extra[@]} -gt 0 ] && say "⚠ B 등록값 바꿈 (이탈 — run_manifest.txt 에 남는다): ${extra[*]}"
      ;;
    C1|C2)
      if [ "${FORCE_C:-0}" != 1 ]; then
        done_before A || die "$arm 은 A 와 B 가 끝까지 돈 뒤에만 (1저자 10-07) — WORK_ROOT 에 A 의 result=DONE 이 없다 (FORCE_C=1 로 넘김)"
        done_before B || die "$arm 은 A 와 B 가 끝까지 돈 뒤에만 (1저자 10-07) — WORK_ROOT 에 B 의 result=DONE 이 없다 (FORCE_C=1 로 넘김)"
      fi
      ;;
  esac
  run_stage "$arm" "in.branch_${arm}.liggghts" ${extra[@]+"${extra[@]}"}
  check_arm "$LAST_RUN" "$arm" || { say "✗ $arm 이 끝까지 가지 않았다 — 뒤 arm 은 돌리지 않는다"; exit 3; }
done
say "끝 — 보낼 것: 위의 *.report.tgz (README §6)"
