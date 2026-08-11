#!/usr/bin/env bash
# run_site_screen_gabia.sh — 자리 선호·자세 스크리닝을 gabia 에서 단계별로 돌린다.
#   프로토콜: kb/methodology/site_preference_protocol_2026_08_11.md
#
#   bash tools/sdcp/run_site_screen_gabia.sh fetch    # 0단계: 입력 회수 (SDCP 기체상 2종 + 0.85 기하)
#   bash tools/sdcp/run_site_screen_gabia.sh atlas    # 1단계: 자세 아틀라스 (GPU 불필요)
#   bash tools/sdcp/run_site_screen_gabia.sh rigid    # 2단계: UMA rigid SP
#   bash tools/sdcp/run_site_screen_gabia.sh relax    # 3단계: UMA relax (freeze 1.0 · 0.85)
#   bash tools/sdcp/run_site_screen_gabia.sh verdict  # 4단계: 판정표
#   bash tools/sdcp/run_site_screen_gabia.sh watch    # 진행 상황
set -euo pipefail

REPO="${REPO:-$HOME/Yonghoon-DEM-DFT}"
RUN="${RUN:-/data/work/runs/sdcp_v4_sitescreen}"
MOLDIR="${MOLDIR:-/data/work/runs/sdcp_linio2_binding/mols}"
TOP1FREE="${TOP1FREE:-/data/work/runs/sdcp_v2/phaseA_top1free}"
LOG="$RUN/logs"; mkdir -p "$LOG"
SS="python3 $REPO/tools/sdcp/site_screen.py"
STAGE="${1:-}"

guard() {                      # CLAUDE.md — pw.x 와 UMA 동시 실행 금지
  if pgrep -fa 'pw\.x' >/dev/null 2>&1; then
    echo "⛔ pw.x 가 돌고 있다. nvidia-smi 로 확인하고 끝난 뒤에 다시."; nvidia-smi || true; exit 1
  fi
  if [ "$(pgrep -fc 'site_screen.py score' || echo 0)" -gt 1 ]; then
    echo "⛔ score 가 이미 돌고 있다 (중복 실행 방지)"; exit 1
  fi
  nvidia-smi --query-gpu=name,memory.used,memory.total --format=csv,noheader || true
}

case "$STAGE" in
fetch)
  echo "── 0단계: 입력 회수 ─────────────────────────────────────"
  # (a) SDCP 기체상 ORCA 기하 2종 — repo 에 없다
  for m in neutral doped; do
    src="$MOLDIR/sdcp_v7c_$m.xyz"
    if [ -f "$src" ]; then
      cp -v "$src" "$REPO/db/structures/sdcp_v7c_$m.xyz"
    else
      echo "⚠ 없다: $src  — find 로 찾아본다"
      find /data/work -name "sdcp_v7c_${m}.xyz" -not -path '*/\.*' 2>/dev/null | head -5
    fi
  done
  # (b) freeze 0.85 (phaseA_top1free) 챔피언 기하 — VASP 단일점이 실제로 쓴 자세
  for p in doped_sulfonate_down_r0_g20 neutral_sulfonate_down_r180_g22; do
    f="$TOP1FREE/complex_$p.xyz"
    [ -f "$f" ] && cp -v "$f" "$REPO/db/structures/sdcp_pose_f085_$p.xyz" \
                || echo "⚠ 없다: $f"
  done
  ls -la "$TOP1FREE" 2>/dev/null | head -20 || echo "⚠ $TOP1FREE 없음"
  echo; echo "── 검증 ──"; cd "$REPO" && $SS inputs
  echo; echo "★ sha256 (프로토콜에 고정할 값):"
  sha256sum "$REPO"/db/structures/sdcp_v7c_{neutral,doped}.xyz 2>/dev/null || true
  ;;

atlas)
  cd "$REPO"
  $SS inputs   | tee "$LOG/inputs.txt"
  $SS sites    | tee "$LOG/sites.txt"
  $SS selftest | tee "$LOG/selftest.txt"
  $SS atlas --out "$RUN" 2>&1 | tee "$LOG/atlas.txt"
  ;;

rigid)
  guard; cd "$REPO"
  nohup $SS score --out "$RUN" --stage rigid --task "${TASK:-omat}" \
        > "$LOG/rigid_${TASK:-omat}.log" 2>&1 &
  echo "PID $! · tail -f $LOG/rigid_${TASK:-omat}.log"
  ;;

relax)
  guard; cd "$REPO"
  nohup $SS score --out "$RUN" --stage relax --task "${TASK:-omat}" \
        --freeze 1.0 0.85 --top-per-site 2 --pairs 5 \
        > "$LOG/relax_${TASK:-omat}.log" 2>&1 &
  echo "PID $! · tail -f $LOG/relax_${TASK:-omat}.log"
  ;;

verdict)
  cd "$REPO"
  for f in sdcp_neutral sdcp_doped ptfe_dimer ptfe_c10; do
    for ff in 1.00 0.85; do
      d="$RUN/$f/relax_f$ff"
      [ -d "$d" ] || continue
      echo "═══ $f · freeze $ff ═══"
      $SS verdict "$d"
    done
  done | tee "$LOG/verdict.txt"
  ;;

watch)
  echo "RUN=$RUN"
  for f in sdcp_neutral sdcp_doped ptfe_dimer ptfe_c10; do
    r=$(ls "$RUN/$f/rigid"/*.json 2>/dev/null | grep -vc '_references' || echo 0)
    a=$(ls "$RUN/$f"/*.xyz 2>/dev/null | wc -l)
    printf '  %-14s atlas %4s · rigid %4s' "$f" "$a" "$r"
    for ff in 1.00 0.85; do
      n=$(ls "$RUN/$f/relax_f$ff"/*.json 2>/dev/null | grep -vc '_references' || echo 0)
      printf ' · relax@%s %3s' "$ff" "$n"
    done; echo
  done
  pgrep -fa 'site_screen.py score' || echo "  (score 미실행)"
  nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader || true
  ;;

*)
  sed -n '2,10p' "$0"; exit 1;;
esac
