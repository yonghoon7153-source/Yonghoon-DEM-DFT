#!/usr/bin/env bash
# =============================================================================
# run_kgy.sh — WAD-AgC Ag(111)|흑연 3층 (사전등록 db/properties/wad_agc_graphite_prereg_2026_10_02.json) · kgy
#   ① 1단계 (기계 대조 2 → 제약 이완 5) → ② 2단계 입력 생성 (uma env python · 결정적) → ③ 2단계 SCF 31 → ④ 집계 (ATM 은 repo 에서 --atm)
#   회수(이 worktree 에서 커밋 · push)는 따로 블록으로 한다.
#
# 사용 (kgy · tmux 안 · 이 카드를 담은 커밋의 git worktree 에서):
#   PWX=<kgy pw.x> bash db/inputs/wad_agc_graphite_2026_10_02/run_kgy.sh                    # 전부 (STAGE=all)
#   DRY_RUN=1 EXCEPTION_ID="<문구>" PWX=… bash …/run_kgy.sh                                  # 1단계 입력 점검만 (계산 안 함)
#   STAGE=2 PWX=… bash …/run_kgy.sh                                                          # 1단계가 끝난 뒤 2단계만
#   FALLBACK="<원 잡 이름 …>" PWX=… bash …/run_kgy.sh                                        # SCF 미수렴 잡만 β 0.1 판 한 번 → 나머지 재개 → 집계
# env: PWX (필수 · 추측하지 않는다) · PSEUDO_DIR (~/work/pseudo) · PY (/home/kgy/apps/miniforge3/envs/uma/bin/python · 절대경로)
#      RUN (~/work/runs/wad_agc_graphite_2026_10_02) · START_MAX_MIB 12000 · KILL_MIB 23000 · HOST_START_MIB 8192 · HOST_KILL_MIB 2048
#      EXCEPTION_ID (기본 = 이 카드의 결정 D-2026-10-02-wad-agc-graphite — 러너가 원장에서 active 를 확인하고서야 시작한다)
#
# ⛔ 못 하는 것: 판정 문구를 만들지 않는다 (집계 JSON 만 · 판정은 카드 규칙대로 repo 에서) · 한 단계가 실패하면 뒤 단계를 돌리지 않는다 ·
#   β 0.1 대체 잡을 저절로 고르지 않는다 (멈춘 잡을 사람이 FALLBACK 으로 준다 — 카드 §4 '원 잡이 SCF 미수렴일 때만 한 번') ·
#   총 견적이 7 일을 넘는지 판단하지 않는다 (벽시계를 찍기만 한다 — 판단은 사용자 · 카드 §8) ·
#   li2s UMA 런을 건드리지 않는다 (가드는 우리 잡만 멈춘다 · run_sese_gpu.sh ③).
# =============================================================================
set -uo pipefail
W=$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)
cd "$W" || { echo "⛔ $W 없음"; exit 1; }
PKG=db/inputs/wad_agc_graphite_2026_10_02
CARD=db/properties/wad_agc_graphite_prereg_2026_10_02.json
RUN=${RUN:-$HOME/work/runs/wad_agc_graphite_2026_10_02}
[ -n "${PWX:-}" ] || { echo "⛔ PWX 를 준다 (점검 블록에서 ldd 로 확인한 kgy pw.x 경로)"; exit 1; }
export PWX PSEUDO_DIR=${PSEUDO_DIR:-$HOME/work/pseudo}
PY=${PY:-/home/kgy/apps/miniforge3/envs/uma/bin/python}
export NP=1 START_MAX_MIB=${START_MAX_MIB:-12000} KILL_MIB=${KILL_MIB:-23000} HOST_START_MIB=${HOST_START_MIB:-8192} HOST_KILL_MIB=${HOST_KILL_MIB:-2048}
export ALLOW_UMA_COEXIST=1 EXCEPTION_ID=${EXCEPTION_ID:-D-2026-10-02-wad-agc-graphite}
STAGE=${STAGE:-all}
mkdir -p "$RUN"; LOG=$RUN/run_kgy.log
say() { echo "[$(date '+%F %T')] $*" | tee -a "$LOG"; }
runner() { env -u LD_LIBRARY_PATH bash tools/wad/run_sese_gpu.sh "$@"; }   # conda 라이브러리가 pw.x 로 새지 않게 (V100 함정 ⑥)

$PY -c "import ase, numpy" 2>/dev/null || { say "⛔ PY=$PY 에 ase/numpy 없음"; exit 1; }
[ -f "$CARD" ] || { say "⛔ 카드가 이 worktree 에 없다 ($CARD) — 카드를 담은 커밋인지 본다"; exit 1; }
say "START @ $(git rev-parse --short=9 HEAD 2>/dev/null) · 변경 $(git status --porcelain 2>/dev/null | wc -l) · STAGE=$STAGE · RUN=$RUN · PWX=$PWX · PSEUDO=$PSEUDO_DIR · 공존 근거 $EXCEPTION_ID"
st=$($PY tools/wad/agc_graphite.py --selftest 2>&1 | tail -1); say "selftest: $st"
case "$st" in *✅*) ;; *) say "⛔ agc_graphite selftest 실패 — 시작하지 않는다"; exit 1;; esac

tsv_show() { [ -f "$1" ] && awk -F'\t' 'NR>1{printf "   %-34s %6s s · 완료 %s · 피크 %s MiB\n",$1,$4,$3,$5}' "$1" | tee -a "$LOG"; }

collect() {
  say "④ 집계 (ATM 제외)"
  $PY tools/wad/agc_graphite.py --collect --stage1_dir "$PKG/stage1" --stage2_dir "$RUN/stage2_pkg" --raw1 "$RUN/stage1" --raw2 "$RUN/stage2" \
      ${FB_RAW:+--fallback_raw "$FB_RAW"} --out "$RUN/collect_kgy.json" 2>&1 | tee -a "$LOG"
  say "✅ 끝 — 회수 블록으로 $RUN 을 worktree 에 커밋한다 (tmp 제외)"
}

if [ -n "${FALLBACK:-}" ]; then
  [ -f "$RUN/stage2_pkg/qe/jobs.json" ] || { say "⛔ 2단계 묶음이 없다 — FALLBACK 은 2단계가 멈춘 뒤에만"; exit 1; }
  FBJ=$(for j in $FALLBACK; do printf '%s_b01 ' "$j"; done)
  say "③′ β 0.1 대체 (카드 §4 · 원 잡이 SCF 미수렴일 때만 한 번): $FBJ"
  JOBS="$FBJ" runner "$RUN/stage2_pkg/fallback/qe" "$RUN/stage2_fb" || say "⚠ 대체 잡 실패 — 그 잡은 INCOMPLETE 로 남는다 (카드 §4)"
  REST=$($PY -c "import json,sys; s=set(sys.argv[1].split()); print(' '.join(j['dir'] for j in json.load(open(sys.argv[2]))['jobs'] if j['dir'] not in s))" "$FALLBACK" "$RUN/stage2_pkg/qe/jobs.json")
  say "③ 2단계 나머지 재개 (대체한 원 잡 제외)"
  JOBS="$REST" runner "$RUN/stage2_pkg/qe" "$RUN/stage2"; rc=$?
  tsv_show "$RUN/stage2/jobs_run.tsv"
  [ $rc = 0 ] || { say "⛔ 2단계 러너 rc=$rc — 멈춘다"; exit 4; }
  FB_RAW="$RUN/stage2_fb" collect; exit 0
fi

if [ "$STAGE" = 1 ] || [ "$STAGE" = all ]; then
  say "① 1단계 — 기계 대조 2 (V2 입력 그대로) → 제약 이완 5"
  runner "$PKG/stage1/qe" "$RUN/stage1"; rc=$?
  [ "${DRY_RUN:-0}" = 1 ] && { say "DRY_RUN — 1단계 점검만 하고 끝낸다 (rc=$rc)"; exit $rc; }
  tsv_show "$RUN/stage1/jobs_run.tsv"
  [ $rc = 0 ] || { say "⛔ 1단계 러너 rc=$rc — 멈춘다 (runner.log · 그 잡 pw.out)"; exit 2; }
fi
if [ "$STAGE" = 2 ] || [ "$STAGE" = all ]; then
  say "② 2단계 입력 생성 (이완 좌표 → 끝점 10 Å · far8 · E(d) · G3 · G4 · β 0.1 대체)"
  $PY tools/wad/agc_graphite.py --stage2 --stage1_dir "$PKG/stage1" --relax_raw "$RUN/stage1" --out "$RUN/stage2_pkg" 2>&1 | tee -a "$LOG"; rc=${PIPESTATUS[0]}
  [ $rc = 0 ] || { say "⛔ 2단계 생성 rc=$rc — 이완 출력(P0 · 제약)부터 본다"; exit 3; }
  say "③ 2단계 SCF"
  runner "$RUN/stage2_pkg/qe" "$RUN/stage2"; rc=$?
  tsv_show "$RUN/stage2/jobs_run.tsv"
  [ $rc = 0 ] || { say "⛔ 2단계 러너 rc=$rc — 멈춘다. SCF 미수렴이면 FALLBACK=\"<그 잡>\" 으로 β 0.1 판을 한 번 (카드 §4)"; exit 4; }
  collect
fi
