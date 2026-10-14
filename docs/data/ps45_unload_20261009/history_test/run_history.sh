#!/usr/bin/env bash
# DEM 언로딩 키트 — 작은 침대 이력 시험 (H0–H5) 러너 (ibb · WSL).  정본 설명 = ../README.md §1 (명령 · 기대 · 보낼 것).
#   ibb 는 run_history_ibb.sbatch 가 이 파일을 NP 6 · lmp_mpi 로 부른다 (#SBATCH -n 6 ↔ mpirun --oversubscribe --bind-to none -np 6 ·
#   H2 단계만 NP_ALT 4 — 같은 할당 안에서 더 적은 rank).
#
#   bash run_history.sh                     # 전 단계 (P · C6 · C4 · Ebot→Cbot · Etop→Ctop · Enone→Cnone · PZ→CZ · BAD · SYN) → 읽는 쪽 → 보고 묶음
#   bash run_history.sh --grammar-only      # 문법 fixture 만 (P → GA → GB · 런 폴더 gram_<시각> · 판정 read_history.py --grammar · 등록 개정 3 §14-9)
#   bash run_history.sh --preflight-only    # 사전 점검만 (런 · kit 사본 없음)
#
# 환경 변수 (괄호 = 기본):
#   WORK_ROOT ($HOME/ps45_unload_hist_20261013)  런 폴더는 그 아래 hist_<시각>/ 로 새로 만든다 (있으면 거부)
#   NP (6) · NP_ALT (4 · H2) · MPIRUN (mpirun) · MPIRUN_FLAGS (--oversubscribe --bind-to none)
#   LMP (/lustre$HOME/LIGGGHTS-PUBLIC/src/lmp_mpi — 등록 §11-1 ⓖ 의 빌드 · sha256 이 다르면 멈춘다 · ALLOW_OTHER_LMP=1 = 이탈 기록)
#   PY (python3) · ALLOW_CONCURRENT=1 (다른 LIGGGHTS 가 돌아도 진행 · ibb 래퍼가 준다)
#
# 지키는 것: kit 사본으로 다시 실행 (리포 체크아웃이 바뀌어도) · SHA256SUMS · 단계마다 새 폴더 · 덱 사본 · rc · np 기록 ·
#   잘못된 ID 단계 (BAD) 는 실패가 기대값이다 (rc ≠ 0 이어도 멈추지 않는다) · 생산자 실패면 뒤 단계는 돌리지 않는다.
set -uo pipefail

EXPECT_LMP_SHA=ee2d77261bac9e7fa4e9311c8709e74bf7583a13225a5bc35a791bef9be60a3f
WORK_ROOT=${WORK_ROOT:-$HOME/ps45_unload_hist_20261013}
NP=${NP:-6}
NP_ALT=${NP_ALT:-4}
MPIRUN=${MPIRUN:-mpirun}
MPIRUN_FLAGS=${MPIRUN_FLAGS:---oversubscribe --bind-to none}
PY=${PY:-python3}
STAMP=${HIST_STAMP:-$(date +%Y%m%d_%H%M%S)}
SELF_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

die() { echo "⛔ $*" >&2; exit 1; }
say() { echo "[$(date +%H:%M:%S)] $*"; }

PREFLIGHT_ONLY=0; NO_KIT=0; GRAMMAR_ONLY=0
for a in "$@"; do case "$a" in --preflight-only) PREFLIGHT_ONLY=1; NO_KIT=1;; --grammar-only) GRAMMAR_ONLY=1;; -h|--help) NO_KIT=1;; esac; done

# ── 0. kit 사본으로 다시 실행 ─────────────────────────────────────────────────
if [ "${HIST_KIT:-0}" != 1 ] && [ "$NO_KIT" = 0 ]; then
  [ -d "$WORK_ROOT" ] || die "WORK_ROOT 가 없다: $WORK_ROOT"
  case "$WORK_ROOT" in *' '*) die "WORK_ROOT 에 공백 — LIGGGHTS 변수로 넘길 수 없다";; esac
  KIT="$WORK_ROOT/kit_$STAMP"
  mkdir "$KIT" || die "kit 폴더를 만들 수 없다 (이미 있다?): $KIT"
  for f in in.hist_producer.liggghts in.hist_producer_zero.liggghts in.hist_consumer.liggghts in.hist_erase_bot.liggghts \
           in.hist_erase_top.liggghts in.hist_erase_none.liggghts in.hist_badid.liggghts in.hist_syntax_probe.liggghts in.hist_grammar.liggghts \
           plate_hist.stl history_params.json make_history_decks.py read_history.py run_history.sh run_history_ibb.sbatch SHA256SUMS; do
    cp -p "$SELF_DIR/$f" "$KIT/" || die "kit 복사 실패: $f"
  done
  ( cd "$SELF_DIR" && echo "head=$(git rev-parse HEAD 2>/dev/null || echo unknown)" \
      && echo "dirty_here=$(git status --porcelain -- . 2>/dev/null | wc -l)" ) > "$KIT/repo_commit.txt" 2>/dev/null || true
  say "kit = $KIT"
  HIST_KIT=1 HIST_STAMP="$STAMP" KIT="$KIT" exec bash "$KIT/run_history.sh" "$@"
fi
if [ "$NO_KIT" = 1 ]; then KIT=$SELF_DIR; else KIT=${KIT:-$SELF_DIR}; fi

for a in "$@"; do
  case "$a" in
    --preflight-only|--grammar-only) ;;
    -h|--help) sed -n '2,/^set -uo pipefail/{/^#/p}' "$KIT/run_history.sh"; exit 0;;
    *) die "모르는 인자: $a (--help)";;
  esac
done

# ── 1. 사전 점검 ─────────────────────────────────────────────────────────────
preflight() {
  say "사전 점검"
  [ -d "$WORK_ROOT" ] || die "WORK_ROOT 가 없다: $WORK_ROOT"
  ( cd "$KIT" && sha256sum -c --quiet SHA256SUMS ) || die "kit 파일이 SHA256SUMS 와 다르다 — 덱을 손으로 고쳤나? (make_history_decks.py 로 다시 만든다)"
  echo "  ✓ 묶음 SHA256SUMS"
  LMP=${LMP:-/lustre$HOME/LIGGGHTS-PUBLIC/src/lmp_mpi}
  [ -x "$LMP" ] || die "LMP 를 실행할 수 없다: $LMP (LMP=… 로 준다)"
  LMP=$(readlink -f "$LMP")
  local sh; sh=$(sha256sum "$LMP" | cut -d' ' -f1)
  if [ "$sh" = "$EXPECT_LMP_SHA" ]; then echo "  ✓ LMP $LMP · sha256 = 등록 §11-1 ⓖ 빌드"
  elif [ "${ALLOW_OTHER_LMP:-0}" = 1 ]; then echo "  ⚠ LMP sha256 $sh ≠ 등록 빌드 — ALLOW_OTHER_LMP=1 (이탈 · run_manifest 에 남는다)"
  else die "LMP sha256 $sh ≠ 등록 빌드 $EXPECT_LMP_SHA (다른 바이너리 — ALLOW_OTHER_LMP=1 이면 이탈로 진행)"; fi
  LMP_SHA=$sh
  command -v "$MPIRUN" >/dev/null 2>&1 || die "mpirun 이 없다: $MPIRUN"
  case "$NP$NP_ALT" in *[!0-9]*|'') die "NP · NP_ALT 가 정수가 아니다: $NP · $NP_ALT";; esac
  [ "$NP_ALT" != "$NP" ] || die "NP_ALT = NP — H2 (NP 바꿈) 가 시험되지 않는다"
  command -v "$PY" >/dev/null 2>&1 || die "python 이 없다: $PY"
  echo "  ✓ $MPIRUN $MPIRUN_FLAGS -np $NP (H2 = -np $NP_ALT) · $PY"
  local others; others=$(pgrep -a -x "$(basename "$LMP")" 2>/dev/null || true)
  if [ -n "$others" ] && [ "${ALLOW_CONCURRENT:-0}" != 1 ]; then echo "$others"; die "다른 LIGGGHTS 가 돌고 있다 (ALLOW_CONCURRENT=1 로 넘김)"; fi
}

preflight
if [ "$PREFLIGHT_ONLY" = 1 ]; then
  say "✓ 사전 점검만 — 통과 (런 없음 · kit 사본 없음 · NP $NP · NP_ALT $NP_ALT · WORK_ROOT $WORK_ROOT)"
  exit 0
fi

MODE=hist; [ "$GRAMMAR_ONLY" = 1 ] && MODE=gram
RUN="$WORK_ROOT/${MODE}_$STAMP"
mkdir "$RUN" || die "런 폴더가 이미 있다 (덮어쓰지 않는다): $RUN"
{
  echo "kit=$KIT"; sed 's/^/repo_/' "$KIT/repo_commit.txt" 2>/dev/null
  echo "sums_sha256=$(sha256sum "$KIT/SHA256SUMS" | cut -d' ' -f1)"
  echo "lmp=$LMP"; echo "lmp_sha256=$LMP_SHA"; echo "np=$NP"; echo "np_alt=$NP_ALT"; echo "mpirun=$MPIRUN $MPIRUN_FLAGS"
  echo "slurm_job=${SLURM_JOB_ID:-none} slurm_ntasks=${SLURM_NTASKS:-none} slurm_nodes=${SLURM_JOB_NODELIST:-none}"
  echo "mode=$MODE"; echo "allow_other_lmp=${ALLOW_OTHER_LMP:-0}"; echo "start=$(date -Iseconds)"
} > "$RUN/run_manifest.txt"
say "런 폴더 = $RUN"

# ── 2. 한 단계 ───────────────────────────────────────────────────────────────
run_stage() {   # $1 = 단계 이름  $2 = 덱  $3 = NP  $4 = 읽을 restart (없으면 -)  [$5 $6 …] = 덱 변수 짝 (-var · vars.txt 에 기록)
  local name=$1 deck=$2 np=$3 ck=$4 dir="$RUN/$1"
  shift 4
  mkdir -p "$dir/producer" "$dir/restart" "$dir/probe" || die "단계 폴더 실패: $dir"
  cp -p "$KIT/$deck" "$KIT/plate_hist.stl" "$dir/" || die "덱 복사 실패: $deck"
  echo "$np" > "$dir/np.txt"
  echo "$deck" > "$dir/deck.txt"
  local extra=() vars=()
  while [ $# -ge 2 ]; do vars+=(-var "$1" "$2"); echo "$1=$2" >> "$dir/vars.txt"; shift 2; done
  if [ "$ck" != - ]; then
    [ -s "$ck" ] || { echo "missing_ckpt $ck" > "$dir/rc"; say "✗ $name — 읽을 restart 가 없다: $ck"; return 1; }
    extra=(-var ckpt "$ck"); echo "$ck" > "$dir/ckpt.txt"
  fi
  say "▶ $name ($deck · -np $np)"
  # shellcheck disable=SC2086
  ( cd "$dir" && export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 && \
    "$MPIRUN" $MPIRUN_FLAGS -np "$np" "$LMP" -in "$dir/$deck" -log "$dir/log.liggghts" \
      -var out "$dir" -var plate_stl "$dir/plate_hist.stl" ${extra[@]+"${extra[@]}"} ${vars[@]+"${vars[@]}"} ) > "$dir/screen.out" 2>&1
  local rc=$?
  echo "$rc" > "$dir/rc"
  say "■ $name rc=$rc"
  return $rc
}

# ── 2b. 문법 fixture 만 (Q8 · 등록 개정 3 §14-9) — P → GA (처음 · 빈 상태 파일) → GB (GA 마지막 단 끝 restart + 짝 상태 파일 · 새 프로세스) ──
if [ "$GRAMMAR_ONLY" = 1 ]; then
  # Q4 (나 · Codex 판정문 10-14 §6-2): 다음 단계 = 앞 단계 rc 0 **과** 그 산출물 둘 다 (파일을 다 쓴 뒤 실패한 단계에서 이어 가지 않는다)
  PRC=0; run_stage P in.hist_producer.liggghts "$NP" - || PRC=$?
  FIX="$RUN/P/fixture.bin"
  if [ "$PRC" = 0 ] && [ -s "$FIX" ]; then
    mkdir -p "$RUN/GA" && echo "# 처음 (빈 상태 파일 — 덱은 상태 파일을 늘 맨 바깥에서 include 한다)" > "$RUN/GA/state_fresh.in"
    GARC=0; run_stage GA in.hist_grammar.liggghts "$NP" "$FIX" gr_state "$RUN/GA/state_fresh.in" gr_resume 0 || GARC=$?
    LASTS=$(ls "$RUN"/GA/restart/state_g_*.in 2>/dev/null | sed 's/.*state_g_\([0-9]*\)\.in$/\1/' | sort -n | tail -1)
    if [ "$GARC" = 0 ] && [ -n "$LASTS" ] && [ -s "$RUN/GA/restart/restart_g_$LASTS.bin" ]; then
      run_stage GB in.hist_grammar.liggghts "$NP" "$RUN/GA/restart/restart_g_$LASTS.bin" gr_state "$RUN/GA/restart/state_g_$LASTS.in" gr_resume 1
    else
      say "✗ GA rc=$GARC · 마지막 단 끝 restart + 상태 파일 — 둘 다 있어야 GB (이어 돌림) 를 돌린다 · GB 없음"
    fi
  else
    say "✗ 생산자 rc=$PRC · fixture.bin — 둘 다 있어야 문법 단계를 돌린다 · GA · GB 없음"
  fi
  echo "end=$(date -Iseconds)" >> "$RUN/run_manifest.txt"
  "$PY" -I "$KIT/read_history.py" --grammar "$RUN" --params "$KIT/history_params.json" --out "$RUN/grammar_verdict.json" | tee "$RUN/grammar_verdict.txt"
  VRC=${PIPESTATUS[0]}
  ( cd "$WORK_ROOT" && tar -czf "$RUN.report.tgz" "$(basename "$RUN")" "$(basename "$KIT")/SHA256SUMS" ) \
    && say "보낼 것: $RUN.report.tgz  sha256 $(sha256sum "$RUN.report.tgz" | cut -d' ' -f1)"
  say "끝 — 문법 fixture 읽는 쪽 rc=$VRC (0 = 기대대로 · 짧은 문법 런 = 물리 검증 아님)"
  exit "$VRC"
fi

PRC=0; run_stage P in.hist_producer.liggghts "$NP" - || { PRC=$?; say "✗ 생산자 실패 (rc $PRC) — 뒤 단계를 돌리지 않는다"; }
FIX="$RUN/P/fixture.bin"
if [ "$PRC" = 0 ] && [ -s "$FIX" ]; then   # 앞 단계 rc 0 과 fixture 둘 다 (Q4 나 — 파일을 쓴 뒤 실패한 생산자에서 이어 가지 않는다)
  run_stage C6 in.hist_consumer.liggghts "$NP" "$FIX"
  run_stage C4 in.hist_consumer.liggghts "$NP_ALT" "$FIX"
  for m in bot top none; do
    run_stage "E$m" "in.hist_erase_$m.liggghts" "$NP" "$FIX" && run_stage "C$m" in.hist_consumer.liggghts "$NP" "$RUN/E$m/erased.bin"
  done
  run_stage BAD in.hist_badid.liggghts "$NP" "$FIX"; say "  (BAD 은 rc ≠ 0 이 기대값 — 잘못된 내부 ID)"
  run_stage SYN in.hist_syntax_probe.liggghts "$NP" "$FIX"
fi
run_stage PZ in.hist_producer_zero.liggghts "$NP" - && run_stage CZ in.hist_consumer.liggghts "$NP" "$RUN/PZ/fixture.bin"
echo "end=$(date -Iseconds)" >> "$RUN/run_manifest.txt"

# ── 3. 읽는 쪽 · 보고 묶음 ───────────────────────────────────────────────────
"$PY" -I "$KIT/read_history.py" "$RUN" --params "$KIT/history_params.json" --out "$RUN/history_verdict.json" | tee "$RUN/history_verdict.txt"
VRC=${PIPESTATUS[0]}
( cd "$WORK_ROOT" && tar -czf "$RUN.report.tgz" "$(basename "$RUN")" "$(basename "$KIT")/SHA256SUMS" ) \
  && say "보낼 것: $RUN.report.tgz  sha256 $(sha256sum "$RUN.report.tgz" | cut -d' ' -f1)"
say "끝 — 읽는 쪽 rc=$VRC (0 = H0–H5 전부 기대대로)"
exit "$VRC"
