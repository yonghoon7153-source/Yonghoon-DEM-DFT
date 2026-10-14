#!/usr/bin/env bash
# DEM 언로딩 키트 — 러너 (ibb · WSL).  정본 설명 = README.md §3 (명령 · 순서 · 보낼 것).  ⛔ 본 R · 10:0 연장 · U 는 Codex GO 뒤.
#   ibb 는 run_unload_ibb.sbatch 가 이 파일을 NP 6 · lmp_mpi 로 부른다 (#SBATCH -n 6 ↔ mpirun --oversubscribe --bind-to none -np 6).
#
#   bash run_unload.sh <침대> <잡>                    # 잡 하나 (아래) — 관문 (ul_reader.py gate) 이 거부하면 런 없이 멈춘다
#   bash run_unload.sh <침대> <잡> --preflight-only   # 사전 점검만 (런 · kit 사본 없음)
#   RESUME=1 bash run_unload.sh <침대> <팔>           # 기계 실패 이어 돌림 한 번 (마지막 restart_unload_* + 짝 상태 파일 · §4-4 · §13-1)
#     ⛔ 개정 3 §14-4: RESUME = 일반 팔 (UB · UT · UC · UVa · UVb · UT3) 만 · 첫 시도가 관문 ALLOW (gate=ALLOW 기록) 를 받았고 덱 요약 없이 끝났을 때 ·
#        UTc · G_* · RJ · RJ2 · EXT = 거부 — 다시 = 새 시도 (지금 폴더를 이름 바꿔 보존 → RESUME 없이 새 제출 · 관문 다시)
#
# 잡 (정본 이름 = README §0):
#   RJ    복원 시험 — (7:3) Ut0 → G0 (원 마지막 조각 덱) → R → UN (보조 소거 읽기) → UK (회전 KE) → 복원 판정 · KE 기준 파일
#         (10:0 의 RJ = 3,600,000 의 R → UN 만 · 그 뒤 EXT · RJ2)
#   EXT   10:0 이완 연장 (3,600,000 → 3,660,000) → S0′ 판정 → 미달이면 EXT2 (→ 3,710,000) → S0″ 판정 (s0_decision.json)
#   RJ2   10:0 S0′ 에서 R → UN → UK → 복원 판정 · KE 기준 파일
#   UB · UT · UC                      7:3 개발 팔 (서로 독립 · 먼저)
#   UVa · UVb                         UB · UT 끝점 판독 뒤 dt* 의 팔 하나만 (관문)
#   UT3                               본 런 (튜플 t3 · 7:3 은 UT + UTc)
#   UTc                               결정표 3 행 — U_UT3 덱을 UT 의 R_M (restart + 상태) 에서 이어 돌림
#   G_UB · G_UVa · G_UVb · G_UT3      중력 팔 (최종 팔의 R_M 에서)
#
# 환경 변수 (괄호 = 기본): WORK_ROOT ($HOME/ps45_unload_20261009 — 그 아래 <침대>/in/ 에 원 파일 · <침대>/<잡>/ 런 폴더)
#   NP (6) · MPIRUN (mpirun) · MPIRUN_FLAGS (--oversubscribe --bind-to none) · PY (python3)
#   LMP (/lustre$HOME/LIGGGHTS-PUBLIC/src/lmp_mpi — 표 binary.lmp_sha256 이 아니면 멈춘다 · ALLOW_OTHER_LMP=1 = 이탈 기록)
#   HIST_VERDICT (이력 시험 history_verdict.json — 복원 판정 ③ · 없으면 UNCONFIRMED) · ALLOW_CONCURRENT=1 (다른 LIGGGHTS 가 돌아도)
#
# 지키는 것: kit 사본으로 다시 실행 (SHA256SUMS) · 잡 폴더는 새로 (있으면 거부 · 이어 돌림만 예외) · 단계마다 화면 · 로그 · 덱 사본 · rc ·
#   Loop time 의 procs = NP · ERROR · UL_ABORT 검사 · 런 뒤 읽는 쪽 (판정 JSON) · 보고 묶음 (큰 덤프 · restart 제외) + sha256.
set -uo pipefail

WORK_ROOT=${WORK_ROOT:-$HOME/ps45_unload_20261009}
NP=${NP:-6}
MPIRUN=${MPIRUN:-mpirun}
MPIRUN_FLAGS=${MPIRUN_FLAGS:---oversubscribe --bind-to none}
PY=${PY:-python3}
STAMP=${UL_STAMP:-$(date +%Y%m%d_%H%M%S)}
SELF_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

die() { echo "⛔ $*" >&2; exit 1; }
say() { echo "[$(date +%H:%M:%S)] $*"; }

BED=${1:-}; JOB=${2:-}
PREFLIGHT_ONLY=0
for a in "${@:3}"; do case "$a" in --preflight-only) PREFLIGHT_ONLY=1;; *) die "모르는 인자: $a";; esac; done
case "$BED" in -h|--help|'') sed -n '2,/^set -uo pipefail/{/^#/p}' "$SELF_DIR/run_unload.sh"; exit 0;; esac
case "$BED" in ps_0_10_r45|ps_3_7_r45|ps_5_5_r45|ps_7_3_r45|ps_10_0_r45) ;; *) die "모르는 침대: $BED";; esac
case "$JOB" in RJ|RJ2|EXT|UB|UT|UC|UVa|UVb|UT3|UTc|G_UB|G_UVa|G_UVb|G_UT3) ;; *) die "모르는 잡: $JOB (README §0)";; esac
case "$WORK_ROOT" in *' '*) die "WORK_ROOT 에 공백 — LIGGGHTS 변수로 넘길 수 없다";; esac
if [ "${RESUME:-0}" = 1 ]; then   # 개정 3 §14-4 (ULKR-06) — kit 사본 · 사전 점검 전에 거부
  case "$JOB" in UB|UT|UC|UVa|UVb|UT3) ;;
    *) die "RESUME 거부 — $JOB 는 이어 돌림을 지원하지 않는다 (등록 개정 3 §14-4: 이어 돌림 = 일반 팔 UB · UT · UC · UVa · UVb · UT3 만).  다시 = 새 시도: 지금 폴더 $WORK_ROOT/$BED/$JOB 를 이름을 바꿔 보존 (예 ${JOB}.try1 · 지우지 · 덮지 않는다) → RESUME 없이 새로 제출 (관문 다시)";;
  esac
fi

# ── 0. kit 사본으로 다시 실행 (SHA256SUMS 목록 그대로) ─────────────────────────
if [ "${UL_KIT:-0}" != 1 ] && [ "$PREFLIGHT_ONLY" = 0 ]; then
  [ -d "$WORK_ROOT" ] || die "WORK_ROOT 가 없다: $WORK_ROOT"
  [ -f "$SELF_DIR/SHA256SUMS" ] || die "SHA256SUMS 없음 — 봉인되지 않은 키트"
  KIT=$(mktemp -d "$WORK_ROOT/kit_${STAMP}_${BED}_${JOB}_XXXX") || die "kit 폴더를 만들 수 없다: $WORK_ROOT"
  while read -r _ rel; do
    mkdir -p "$KIT/$(dirname "$rel")" && cp -p "$SELF_DIR/$rel" "$KIT/$rel" || die "kit 복사 실패: $rel"
  done < "$SELF_DIR/SHA256SUMS"
  cp -p "$SELF_DIR/SHA256SUMS" "$KIT/" || die "kit 복사 실패: SHA256SUMS"
  ( cd "$SELF_DIR" && echo "head=$(git rev-parse HEAD 2>/dev/null || echo unknown)" \
      && echo "dirty_here=$(git status --porcelain -- . 2>/dev/null | wc -l)" ) > "$KIT/repo_commit.txt" 2>/dev/null || true
  say "kit = $KIT"
  UL_KIT=1 UL_STAMP="$STAMP" exec bash "$KIT/run_unload.sh" "$@"
fi
KIT=$SELF_DIR

# ── 1. 사전 점검 ─────────────────────────────────────────────────────────────
tbl() { "$PY" -I -c 'import json,sys; d=json.load(open(sys.argv[1])); print(eval(sys.argv[2], {}, {"d": d}))' "$KIT/unload_params.json" "$1"; }
GATE_LINE=""; GATE_WHY=""
resume_check() {   # 개정 3 §14-4 (ULKR-06) — 같은 승인 팔의 기술 재개인지 (관문을 건너뛰는 대신 첫 시도 기록을 대조)
  local jd="$WORK_ROOT/$BED/$JOB" man
  man="$jd/run_manifest.txt"
  [ -d "$jd" ] || die "이어 돌릴 잡 폴더가 없다: $jd"
  [ -f "$man" ] || die "첫 시도 기록 run_manifest.txt 가 없다 — 같은 승인 팔의 기술 재개인지 확인할 수 없다 (새 시도)"
  grep -qx "bed=$BED" "$man" && grep -qx "job=$JOB" "$man" || die "첫 시도 기록의 침대 · 잡이 $BED $JOB 가 아니다 (새 시도)"
  grep -qx 'resume=0' "$man" || die "첫 시도 (resume=0) 기록이 없다 (새 시도)"
  grep -qx 'gate=ALLOW' "$man" || die "첫 시도가 관문 ALLOW 를 받은 기록 (gate=ALLOW) 이 없다 — 이어 돌림이 아니라 새 제출 (관문 다시)"
  [ ! -e "$jd/screen_a2.txt" ] || die "이미 이어 돌렸다 (등록 범위 한 번 — §4-4 · §13-1 · 개정 3 §14-4 · 그 밖 = 새 승인 · 등록)"
  [ ! -e "$jd/ul_summary.txt" ] || die "첫 시도가 덱 요약 (ul_summary.txt) 까지 끝났다 — 기계 실패가 아니다 (이어 돌림 없음)"
  echo "  ✓ 이어 돌림 = 같은 승인 팔 ($BED $JOB · 첫 시도 gate=ALLOW · 요약 없음 · 한 번)"
}
preflight() {
  say "사전 점검 — $BED $JOB"
  [ -d "$WORK_ROOT" ] || die "WORK_ROOT 가 없다: $WORK_ROOT"
  ( cd "$KIT" && sha256sum -c --quiet SHA256SUMS ) || die "kit 파일이 SHA256SUMS 와 다르다 — 덱을 손으로 고쳤나? (make_unload_decks.py 로 다시 만든다)"
  echo "  ✓ 묶음 SHA256SUMS"
  command -v "$PY" >/dev/null 2>&1 || die "python 이 없다: $PY"
  LMP=${LMP:-/lustre$HOME/LIGGGHTS-PUBLIC/src/lmp_mpi}
  [ -x "$LMP" ] || die "LMP 를 실행할 수 없다: $LMP (LMP=… 로 준다)"
  LMP=$(readlink -f "$LMP")
  local want sh; want=$(tbl 'd["binary"]["lmp_sha256"]'); sh=$(sha256sum "$LMP" | cut -d' ' -f1)
  if [ "$sh" = "$want" ]; then echo "  ✓ LMP $LMP · sha256 = 표 (등록 §11-1 ⓖ 빌드)"
  elif [ "${ALLOW_OTHER_LMP:-0}" = 1 ]; then echo "  ⚠ LMP sha256 $sh ≠ 표 — ALLOW_OTHER_LMP=1 (이탈 · run_manifest 에 남는다)"
  else die "LMP sha256 $sh ≠ 표 $want (다른 바이너리 — ALLOW_OTHER_LMP=1 이면 이탈로 진행)"; fi
  LMP_SHA=$sh
  command -v "$MPIRUN" >/dev/null 2>&1 || die "mpirun 이 없다: $MPIRUN"
  case "$NP" in *[!0-9]*|'') die "NP 가 정수가 아니다: $NP";; esac
  echo "  ✓ $MPIRUN $MPIRUN_FLAGS -np $NP · $PY"
  "$PY" -I "$KIT/ul_reader.py" inputs "$WORK_ROOT" "$BED" > /dev/null || die "in/ 원 파일 sha256 ≠ 표 (또는 원 로그 · 원 마지막 조각 덱 없음) — $WORK_ROOT/$BED/in/"
  echo "  ✓ in/ 원 파일 = 표"
  if [ "${RESUME:-0}" = 1 ]; then
    resume_check
    GATE_LINE="gate=RESUME"
  else
    local gout grc
    gout=$("$PY" -I "$KIT/ul_reader.py" gate "$WORK_ROOT" "$BED" "$JOB"); grc=$?
    echo "$gout"
    [ "$grc" = 0 ] || die "관문 거부 — 위 이유 (제출하지 않는다)"
    GATE_LINE="gate=ALLOW"; GATE_WHY=$gout
  fi
  local others; others=$(pgrep -a -x "$(basename "$LMP")" 2>/dev/null || true)
  if [ -n "$others" ] && [ "${ALLOW_CONCURRENT:-0}" != 1 ]; then echo "$others"; die "다른 LIGGGHTS 가 돌고 있다 (ALLOW_CONCURRENT=1 로 넘김)"; fi
}
preflight
if [ "$PREFLIGHT_ONLY" = 1 ]; then say "✓ 사전 점검만 — 통과 (런 없음 · kit 사본 없음 · $BED $JOB · NP $NP)"; exit 0; fi

IN="$WORK_ROOT/$BED/in"
JD="$WORK_ROOT/$BED/$JOB"
CKPT0="$IN/$(tbl "d['beds']['$BED']['in_files']['ckpt']['file']")"
PLATE="$IN/$(tbl "d['beds']['$BED']['in_files']['mesh']['file']")"
BASE="$WORK_ROOT/$BED/ul_base.in"
EXTRA_VARS=()
if [ "$BED" = ps_10_0_r45 ] && [ "$JOB" != RJ ] && [ "$JOB" != EXT ]; then
  S0P=$(tbl "__import__('json').load(open('$WORK_ROOT/ps_10_0_r45/s0_decision.json'))['s0']" 2>/dev/null) || die "10:0 S0′ 결정 없음"
  EXTRA_VARS=(-var ul_s0 "$S0P")
  CKPT0=$(ls "$WORK_ROOT"/ps_10_0_r45/EXT*/restart/restart_ext_"$S0P".bin 2>/dev/null | head -1)
  [ -s "$CKPT0" ] || die "10:0 S0′ 체크포인트 restart_ext_$S0P.bin 없음"
fi

if [ "${RESUME:-0}" = 1 ]; then
  [ -d "$JD" ] || die "이어 돌릴 잡 폴더가 없다: $JD"
  [ ! -e "$JD/screen_a2.txt" ] || die "이미 이어 돌렸다 (등록 범위 한 번 — §4-4 · §13-1 · 그 밖 = 새 승인 · 등록)"
else
  mkdir -p "$WORK_ROOT/$BED"
  mkdir "$JD" || die "잡 폴더가 이미 있다 (덮어쓰지 않는다): $JD"
fi
{
  echo "kit=$KIT"; sed 's/^/repo_/' "$KIT/repo_commit.txt" 2>/dev/null
  echo "sums_sha256=$(sha256sum "$KIT/SHA256SUMS" | cut -d' ' -f1)"
  echo "lmp=$LMP"; echo "lmp_sha256=$LMP_SHA"; echo "np=$NP"; echo "mpirun=$MPIRUN $MPIRUN_FLAGS"; echo "bed=$BED"; echo "job=$JOB"
  echo "resume=${RESUME:-0}"; echo "slurm_job=${SLURM_JOB_ID:-none} slurm_ntasks=${SLURM_NTASKS:-none} slurm_nodes=${SLURM_JOB_NODELIST:-none}"
  echo "allow_other_lmp=${ALLOW_OTHER_LMP:-0}"; echo "$GATE_LINE"; [ -n "$GATE_WHY" ] && echo "gate_why=$GATE_WHY"; echo "start=$(date -Iseconds)"
} >> "$JD/run_manifest.txt"
MAN="$JD/run_manifest.txt"
note() { echo "$*" >> "$MAN"; }   # 단계 기록 (개정 3 §14-10 · ULKR-11) — 줄을 덧붙이기만 한다

# ── 2. 한 덱 ─────────────────────────────────────────────────────────────────
FAILS=0
run_deck() {   # $1 = 단계 폴더  $2 = 덱 종류  $3 = 읽을 restart  $4 = 상태 파일 (- = 빈 파일)  $5 = 이어 돌림 0/1  $6 = 화면 이름
  local dir=$1 kind=$2 ck=$3 st=$4 resume=$5 scr=${6:-screen.txt}
  local deck="$KIT/decks/$BED/in.$kind.liggghts"
  [ -f "$deck" ] || die "덱 없음: $deck"
  mkdir -p "$dir/dump" "$dir/restart" "$dir/obs" "$dir/g2" "$dir/post" || die "단계 폴더 실패: $dir"
  [ -s "$ck" ] || { echo "missing_ckpt $ck" >> "$dir/run_check.txt"; note "stage=$kind screen=$scr rc=missing_ckpt check=FAIL"; say "✗ $kind — 읽을 restart 가 없다: $ck"; FAILS=$((FAILS + 1)); return 1; }
  [ -f "$dir/deck.liggghts" ] || { cp -p "$deck" "$dir/deck.liggghts" && echo "in.$kind.liggghts" > "$dir/deck.txt"; }
  cmp -s "$deck" "$dir/deck.liggghts" || die "단계 폴더의 덱 사본 ≠ kit 덱 (이어 돌림은 같은 덱으로만): $dir"
  if [ "$st" = - ]; then st="$dir/state_fresh.in"; echo "# 처음 (빈 상태 파일 — 덱은 상태 파일을 늘 맨 바깥에서 include 한다)" > "$st"; fi
  say "▶ $kind → $dir ($scr · -np $NP · ckpt $(basename "$ck"))"
  local base_var=(); [ -f "$BASE" ] && base_var=(-var ul_base "$BASE") || base_var=(-var ul_base "$dir/state_fresh_base_missing.in")
  # shellcheck disable=SC2086
  ( cd "$dir" && export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 && \
    "$MPIRUN" $MPIRUN_FLAGS -np "$NP" "$LMP" -in "$dir/deck.liggghts" -log "$dir/log_${scr%.txt}.liggghts" \
      -var out "$dir" -var plate_stl "$PLATE" -var ckpt "$ck" -var ul_state "$st" -var ul_resume "$resume" ${base_var[@]+"${base_var[@]}"} \
      ${EXTRA_VARS[@]+"${EXTRA_VARS[@]}"} ) > "$dir/$scr" 2>&1
  local rc=$? why=""
  grep -q 'LIGGGHTS-PUBLIC 3.8.0' "$dir/$scr" || why="$why banner"
  grep -q '^ERROR' "$dir/$scr" && why="$why ERROR"
  grep -q 'UL_ABORT' "$dir/$scr" && why="$why UL_ABORT"
  local procs; procs=$(grep -o 'Loop time of [0-9.eE+-]* on [0-9]* procs' "$dir/$scr" | awk '{print $6}' | sort -u | tr '\n' ' ')
  [ "$procs" = "$NP " ] || why="$why procs[$procs]≠$NP"
  [ "$rc" = 0 ] || why="$why rc=$rc"
  note "stage=$kind screen=$scr rc=$rc check=${why:-PASS}"
  if [ -z "$why" ]; then echo "$kind $scr PASS rc=0 procs=$NP" >> "$dir/run_check.txt"; say "■ $kind PASS"
  else echo "$kind $scr FAIL$why" >> "$dir/run_check.txt"; say "✗ $kind FAIL$why"; FAILS=$((FAILS + 1)); return 1; fi
}

bundle() {   # 경량 보고 묶음 — 큰 덤프 · restart 제외 = 모든 관측을 다시 검증하는 원천이 아니다 (원자료 = 이 기계) · 판정에 쓴 결정 파일은 함께
  #   (EXT = EXT2 · s0_decision.json · RJ · RJ2 = ul_base.in · 7:3 = selection.json — 개정 3 §14-8 · ULKR-12)
  local rep="$WORK_ROOT/$BED/$JOB.report.tgz" extra=() x
  case "$JOB" in
    EXT) for x in EXT2 s0_decision.json; do [ -e "$WORK_ROOT/$BED/$x" ] && extra+=("$x"); done ;;
    RJ|RJ2) [ -e "$WORK_ROOT/$BED/ul_base.in" ] && extra+=(ul_base.in) ;;
  esac
  if [ "$BED" = ps_7_3_r45 ] && [ -e "$WORK_ROOT/$BED/selection.json" ]; then extra+=(selection.json); fi
  ( cd "$WORK_ROOT/$BED" && tar --exclude='*.bin' --exclude='*/dump/atom_*' --exclude='*/dump/contact_*' --exclude='*/obs/*.dump' \
      --exclude='*/g2/atom_*' --exclude='*/g2/contact_*' --exclude='*/post/*' -czf "$rep" "$JOB" ${extra[@]+"${extra[@]}"} ) \
    && say "보낼 것: $rep  sha256 $(sha256sum "$rep" | cut -d' ' -f1) (경량 묶음 — 큰 덤프 · restart 제외 · 모든 관측을 다시 검증하는 원천 아님 · 원자료 = 이 기계)"
}

# ── 3. 잡 ────────────────────────────────────────────────────────────────────
RRC=0
reader() {   # 판독기 한 번 — rc 를 잡 기록에 (reader_<명령>_rc) · 0 이 아니면 RRC (정상 미식별은 JSON · rc 0 / 프로그램 오류 = rc ≠ 0 · ULKR-11)
  local cmd=$1 r; shift
  "$PY" -I "$KIT/ul_reader.py" "$cmd" "$@"; r=$?
  note "reader_${cmd}_rc=$r"
  [ "$r" = 0 ] || RRC=$r
  return "$r"
}
case "$JOB" in
  RJ|RJ2)
    LAST_DECK="$IN/$(tbl "d['beds']['$BED']['last_deck']")"
    PRE_OK=1
    "$PY" -I "$KIT/ul_gates.py" g0 "$LAST_DECK" "$KIT/decks/$BED/in.R.liggghts" > "$JD/g0.json"; G0RC=$?
    note "stage=G0 rc=$G0RC"; echo "  G0 rc=$G0RC (0 = PASS · $JD/g0.json)"
    if [ "$G0RC" != 0 ]; then say "✗ G0 실패 (rc=$G0RC) — Ut0 · R · UN · UK 를 돌리지 않는다 (개정 3 §14-10 · ULKR-11)"; FAILS=$((FAILS + 1)); PRE_OK=0; fi
    if [ "$PRE_OK" = 1 ] && [ "$BED" = ps_7_3_r45 ]; then
      run_deck "$JD/Ut0" Ut0 "$CKPT0" - 0 || { say "✗ Ut0 (문법 런) 기술 실패 — R · UN · UK 를 돌리지 않는다 (ULKR-11)"; PRE_OK=0; }
    fi
    if [ "$PRE_OK" = 1 ]; then
      { run_deck "$JD/R" R "$CKPT0" - 0 && run_deck "$JD/UN" UNread "$JD/R/un_diag.bin" - 0; } || PRE_OK=0
    fi
    NEED_UK=0; if [ "$BED" != ps_10_0_r45 ] || [ "$JOB" = RJ2 ]; then NEED_UK=1; fi
    if [ "$PRE_OK" = 1 ] && [ "$NEED_UK" = 1 ]; then run_deck "$JD/UK" UK "$CKPT0" - 0 || PRE_OK=0; fi
    HV=(); [ -n "${HIST_VERDICT:-}" ] && HV=(--hist "$HIST_VERDICT")
    reader restore "$WORK_ROOT" "$BED" --job "$JOB" ${HV[@]+"${HV[@]}"}
    if [ "$NEED_UK" = 1 ]; then
      if [ "$PRE_OK" = 1 ]; then reader kebase "$WORK_ROOT" "$BED" || RRC=2; else note "reader_kebase_rc=skipped (선행 단계 실패)"; RRC=2; fi
    fi
    ;;
  EXT)
    run_deck "$JD" EXT "$CKPT0" - 0
    reader s0p "$WORK_ROOT"
    if [ "$RRC" != 0 ] && [ -s "$JD/restart/restart_ext_$(tbl "d['ext_10_0']['end1']").bin" ]; then
      mkdir -p "$WORK_ROOT/$BED/EXT2"
      RRC=0
      run_deck "$WORK_ROOT/$BED/EXT2" EXT2 "$JD/restart/restart_ext_$(tbl "d['ext_10_0']['end1']").bin" - 0
      reader s0p "$WORK_ROOT"
    fi
    ;;
  UB|UT|UC|UVa|UVb|UT3)
    KIND=$JOB; case "$JOB" in UB|UVa|UVb|UT3) KIND="U_$JOB";; esac
    if [ "${RESUME:-0}" = 1 ]; then
      LASTR=$(ls "$JD"/restart/restart_unload_*.bin 2>/dev/null | sed 's/.*restart_unload_\([0-9]*\)\.bin/\1 &/' | sort -n | tail -1 | cut -d' ' -f2)
      [ -n "$LASTR" ] || die "이어 돌릴 restart_unload_* 가 없다: $JD/restart"
      LSTEP=$(basename "$LASTR" .bin); LSTEP=${LSTEP#restart_unload_}
      [ -s "$JD/restart/state_unload_$LSTEP.in" ] || die "짝 상태 파일 state_unload_$LSTEP.in 없음"
      echo "resume_from=$LSTEP" >> "$JD/run_manifest.txt"
      run_deck "$JD" "$KIND" "$LASTR" "$JD/restart/state_unload_$LSTEP.in" 1 screen_a2.txt
    else
      run_deck "$JD" "$KIND" "$CKPT0" - 0
    fi
    reader arm "$WORK_ROOT" "$BED" "$JOB"
    ;;
  UTc)
    SRC="$WORK_ROOT/$BED/UT"
    RM=$(ls "$SRC"/restart/restart_RM_*.bin 2>/dev/null); [ "$(echo "$RM" | grep -c .)" = 1 ] || die "UT 의 R_M restart 가 하나가 아니다: $RM"
    RS=${RM##*/restart_RM_}; RS=${RS%.bin}
    [ -s "$SRC/restart/state_RM_$RS.in" ] || die "UT 의 R_M 상태 파일 없음"
    # 개정 3 §14-3 (ULKR-03) — UT 의 기록 · 덤프 · thermo 를 복사하지 않는다: 부모 경로 + sha256 목록 (판독기가 거기서 읽고 대조) ·
    #   UTc 기록 CSV 는 머리만 (덱의 이어 돌림 경로는 머리를 쓰지 않고 줄만 덧붙인다)
    "$PY" -I "$KIT/ul_reader.py" parentsums "$SRC" > "$JD/parent_UT.sha256" || die "UT 부모 관측 sha256 목록을 쓸 수 없다"
    for f in windows steps events; do tbl "','.join(d['records']['${f}_cols'])" > "$JD/ul_$f.csv" || die "UTc 기록 머리 실패: ul_$f.csv"; done
    { echo "continues=UT"; echo "parent_dir=$SRC"; echo "rm_step=$RS"; echo "parent_sums=parent_UT.sha256"
      echo "parent_sums_sha256=$(sha256sum "$JD/parent_UT.sha256" | cut -d' ' -f1)"; } >> "$JD/run_manifest.txt"
    run_deck "$JD" U_UT3 "$RM" "$SRC/restart/state_RM_$RS.in" 1
    reader arm "$WORK_ROOT" "$BED" "$JOB"
    ;;
  G_*)
    ARM=${JOB#G_}; SRC="$WORK_ROOT/$BED/$ARM"
    if [ "$BED" = ps_7_3_r45 ] && [ "$ARM" = UT3 ]; then SRC="$WORK_ROOT/$BED/UT"; fi
    RM=$(ls "$SRC"/restart/restart_RM_*.bin 2>/dev/null); [ "$(echo "$RM" | grep -c .)" = 1 ] || die "$SRC 의 R_M restart 가 하나가 아니다"
    RS=${RM##*/restart_RM_}; RS=${RS%.bin}
    echo "source=$SRC rm_step=$RS" >> "$JD/run_manifest.txt"
    run_deck "$JD" "$JOB" "$RM" "$SRC/restart/state_RM_$RS.in" 0
    reader arm "$WORK_ROOT" "$BED" "$JOB"
    ;;
esac
if [ "$BED" = ps_7_3_r45 ] && [ -d "$WORK_ROOT/ps_7_3_r45/UB" ]; then reader select "$WORK_ROOT"; fi
echo "end=$(date -Iseconds) fails=$FAILS reader_rc=$RRC" >> "$JD/run_manifest.txt"
bundle
if [ "$FAILS" != 0 ]; then say "끝 — 기술 실패 $FAILS (run_check.txt) — TECH · 1저자"; exit 2; fi
say "끝 — 런 PASS · 읽는 쪽 rc=$RRC"
exit "$RRC"
