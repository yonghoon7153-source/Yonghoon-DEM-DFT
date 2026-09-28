#!/usr/bin/env bash
# =============================================================================
# run_v100.sh — WAD-CC 흑연 층간 C|C (사전등록 db/properties/wad_cc_graphite_prereg_2026_09_28.json) · V100 한 번에
#   ① 1단계 제약 이완 9 → ② 2단계 입력 생성 (ASE python · 결정적) → ③ 2단계 SCF 44 → ④ 집계 (ATM 열은 repo 에서 --atm)
#   → ⑤ 회수 묶음 ~/wad_cc_graphite_2026_09_28_return.tgz
#
# 사용 (V100 · tmux 안 · ~/wad4l = kgy `v100-serve` ref 의 git archive 사본 · CODE_ID 를 먼저 갱신):
#   bash db/inputs/wad_cc_graphite_2026_09_28/run_v100.sh
#   DRY_RUN=1 bash db/inputs/wad_cc_graphite_2026_09_28/run_v100.sh     ← 1단계 입력 점검만 (해시 · PP · D3 · GPU)
# env (기본값 = V2 2단계 실행과 같은 값): PWX · PSEUDO_DIR · NP 1 · START_MAX_MIB 2048 · KILL_MIB 31000 · RUN
#   PY = ASE·numpy 가 있는 python (기본 자동: python3 → 켜진 conda env 의 python · 둘 다 없으면 1단계만 → 회수)
#
# ⛔ 못 하는 것: 판정 문구를 만들지 않는다 (집계 JSON 만 · 판정은 카드 규칙대로 repo 에서) · 한 단계가 실패하면
#   뒤 단계를 돌리지 않는다 · pw.x 는 LD_LIBRARY_PATH 를 비운 셸로 띄운다 (conda 라이브러리가 새지 않게 —
#   플랫폼 문서 함정 ⑥) · GPU 를 UMA 와 같이 쓰지 않는다 (START_MAX_MIB 2048 = GPU 가 비어 있을 때만 시작).
# =============================================================================
set -uo pipefail
W=${W:-$HOME/wad4l}
cd "$W" || { echo "⛔ $W 없음"; exit 1; }
PKG=db/inputs/wad_cc_graphite_2026_09_28
CARD=db/properties/wad_cc_graphite_prereg_2026_09_28.json
RUN=${RUN:-$HOME/runs/wad_cc_graphite_2026_09_28}
export PWX=${PWX:-$HOME/apps/qe-7.4.1-gpu/bin/pw.x}
export PSEUDO_DIR=${PSEUDO_DIR:-$HOME/wad4l/pseudo_kgy}
export NP=${NP:-1} START_MAX_MIB=${START_MAX_MIB:-2048} KILL_MIB=${KILL_MIB:-31000}
mkdir -p "$RUN"; LOG=$RUN/run_v100.log
say() { echo "[$(date '+%F %T')] $*" | tee -a "$LOG"; }

# ASE·numpy 가 있는 python — 없으면 1단계만 돌리고 묶는다 (V100 은 밖으로 못 나가 pip 이 안 된다 ·
#   그때 2단계 입력은 repo 에서 같은 코드로 만들어 다시 보낸다 — 결과는 같다, 왕복이 하나 늘 뿐)
if [ -z "${PY:-}" ]; then
  if python3 -c "import ase, numpy" 2>/dev/null; then PY="python3"
  elif [ -n "${CONDA_PREFIX:-}" ] && env LD_LIBRARY_PATH="$CONDA_PREFIX/lib" "$CONDA_PREFIX/bin/python" -c "import ase, numpy" 2>/dev/null; then
    PY="env LD_LIBRARY_PATH=$CONDA_PREFIX/lib $CONDA_PREFIX/bin/python"
  else PY=""; fi
fi
[ -n "$PY" ] && ! $PY -c "import ase, numpy" 2>/dev/null && { say "⛔ PY=$PY 에 ase/numpy 없음"; exit 1; }
[ -f "$CARD" ] || { say "⛔ 사전등록 카드가 이 사본에 없다 ($CARD) — CODE_ID 커밋이 카드를 담은 커밋인지 본다"; exit 1; }
say "START @ $(cat CODE_ID 2>/dev/null || echo 'CODE_ID 없음') · PY=${PY:-없음 → 1단계만} · RUN=$RUN · PWX=$PWX"
if [ -n "$PY" ]; then
  # 판정 코드가 카드 문턱과 결속돼 있다는 증거를 이 기계에서 (selftest ⑨ 카드 결속 포함 · 3 초)
  st=$($PY tools/wad/cc_graphite.py --selftest 2>&1 | tail -1); say "selftest: $st"
  case "$st" in *✅*) ;; *) say "⛔ cc_graphite selftest 실패 — 시작하지 않는다"; exit 1;; esac
fi

say "① 1단계 제약 이완 9 (맨 아래층 고정 · 나머지 z 만)"
env -u LD_LIBRARY_PATH bash tools/wad/run_sese_gpu.sh "$PKG/stage1/qe" "$RUN/stage1"; rc=$?
[ $rc = 0 ] || { say "⛔ 1단계 러너 rc=$rc — 멈춘다 (runner.log · 해당 잡 pw.out 확인)"; exit 2; }
[ "${DRY_RUN:-0}" = 1 ] && { say "DRY_RUN — 1단계 점검만 하고 끝낸다"; exit 0; }
if [ -z "$PY" ]; then
  tar czf "$HOME/wad_cc_graphite_2026_09_28_stage1_return.tgz" -C "$(dirname "$RUN")" --exclude='tmp' "$(basename "$RUN")" \
    && say "✅ 1단계 끝 (ASE python 없음) — $HOME/wad_cc_graphite_2026_09_28_stage1_return.tgz 를 repo 로 → 2단계 입력은 repo 에서 만든다"
  exit 0
fi

say "② 2단계 입력 생성 (이완 좌표 → 끝점 10 Å · far8 · E(d) · G3 · G4)"
$PY tools/wad/cc_graphite.py --stage2 --stage1_dir "$PKG/stage1" --relax_raw "$RUN/stage1" --out "$RUN/stage2_pkg" 2>&1 | tee -a "$LOG"; rc=${PIPESTATUS[0]}
[ $rc = 0 ] || { say "⛔ 2단계 생성 rc=$rc — 이완 출력(P0 · 제약)부터 본다"; exit 3; }

say "③ 2단계 SCF"
env -u LD_LIBRARY_PATH bash tools/wad/run_sese_gpu.sh "$RUN/stage2_pkg/qe" "$RUN/stage2"; rc=$?
[ $rc = 0 ] || { say "⛔ 2단계 러너 rc=$rc — 멈춘다"; exit 4; }

say "④ 집계 (ATM 제외 — repo 에서 --atm)"
$PY tools/wad/cc_graphite.py --collect --stage2_dir "$RUN/stage2_pkg" --raw "$RUN/stage2" --out "$RUN/cc_collect_v100.json" 2>&1 | tee -a "$LOG"

say "⑤ 회수 묶음 (tmp 제외)"
tar czf "$HOME/wad_cc_graphite_2026_09_28_return.tgz" -C "$(dirname "$RUN")" --exclude='tmp' "$(basename "$RUN")" \
  && say "✅ 끝 — $HOME/wad_cc_graphite_2026_09_28_return.tgz ($(du -h "$HOME/wad_cc_graphite_2026_09_28_return.tgz" | cut -f1)) → repo db/raw/wad_cc_graphite_2026_09_28/"
