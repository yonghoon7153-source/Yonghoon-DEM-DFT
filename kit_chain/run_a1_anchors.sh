#!/usr/bin/env bash
set -uo pipefail
# A-1 MPM 사이클 열화 앵커 — pristine(N0) + 충전앵커(SC-5.1%/poly팽창) + ΔV심화(-5.9%)
#   → cycle_geom_debond 로 기하 debond/void.  ⚠ 충전-상태(가역 SOC breathing) 스냅샷 =
#   영구 fade 아님; 비가역화 판정은 ledger 캘리브(A-3 --mpm-anchor).  사용: bash run_a1_anchors.sh
KIT="$(cd "$(dirname "$0")" && pwd)"
SCR=""; for c in "$KIT/scripts" "$KIT/../scripts"; do [ -d "$c" ] && SCR="$(cd "$c" && pwd)" && break; done
[ -z "$SCR" ] && { echo "scripts/ 못 찾음 — 레포 루트에 킷을 푸세요"; exit 1; }
if [ -z "${MPM_NO_PULL:-}" ] && [ -d "$SCR/../.git" ]; then ( cd "$SCR/.." && git pull --ff-only ) || echo "  ⚠ git pull 스킵"; fi
OUT="$KIT/a1_anchors"; mkdir -p "$OUT"
if [ -z "${A1_DETACHED:-}" ]; then
  export A1_DETACHED=1
  log="$OUT/a1_run_$(date +%Y%m%d_%H%M%S).log"
  echo "→ detached — log: $log"
  setsid nohup bash "$0" "$@" >"$log" 2>&1 </dev/null &
  echo "   PID $!     follow: tail -f $log"
  exit 0
fi
COMMON=(--am-scaffold "$KIT/am_scaffold.csv" --se-dump "$KIT/se_scaffold.csv" --periodic
        --lateral-box 0.05 --n-grid 256 --arch cuda --gpu-mem 28 --protocol hold --frames 150
        --e-se 1.53 --nu-se 0.49 --target-gpa 0.3)
run_one() { local lab="$1"; shift; echo "=== A-1 앵커: $lab ==="; python3 "$SCR/mpm3d_compaction.py" "${COMMON[@]}" "$@" --save-metrics "$OUT/m_${lab}.json" || { echo "FAIL $lab — 위 트레이스"; exit 1; }; }
run_one N0
run_one charged --cycle-deform --cycle-n 1 --cycle-dv-sc -0.051 --cycle-dv-poly 0.059 --dv-pct-poly 0.30
run_one charged_deep --cycle-deform --cycle-n 2 --cycle-dv-sc -0.059 --cycle-dv-poly 0.059 --dv-pct-poly 0.30
echo "=== 기하 debond/void (pristine 대비) ==="
python3 "$SCR/cycle_geom_debond.py" "$OUT/m_N0.json" "$OUT/m_charged.json" "$OUT/m_charged_deep.json" --csv "$OUT/a1_debond.csv"
echo "완료 → $OUT/ (m_*.json 앵커, a1_debond.csv 기하 debond/void).  ⚠ 충전상태(가역); ledger가 비가역 판정."
