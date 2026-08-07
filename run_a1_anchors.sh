#!/usr/bin/env bash
set -uo pipefail
# A-1 MPM 사이클 열화 앵커 (★2단: 제작압 300 MPa 압밀 → 제하 → 구동압 90 MPa 유지)
#   ① 제작압 압밀(hold) + --save-state 로 소성이력(F) 저장
#   ② --load-state 로 그 이력을 이어받아 구동압에서 재평형 + --cycle-deform 사이클 호흡
#      두 팔 = servo(정응력, 부드러운 스프링/압력제어) · hold(정적변위, 강체 지그/고정 갭)
#      ★ 두 팔 모두 먼저 실제로 제하한다(플래튼 상승 → 구동압).  servo 는 그 응력을 계속
#        유지하고(두께가 자유변수), hold 는 그 높이에서 플래튼을 고정해 응력이 아래로
#        이완한다(갭이 고정변수).  지그 강성을 모르므로 실제 셀은 두 팔 사이 = 브래킷.
#      ⚠ 2026-07-28 이전 버전에서는 hold 팔이 침묵 no-op 이었다(플래튼이 제작 높이에 그대로
#        멈춰 제작 형상을 구동압 라벨로 출력).  아래 검증 스텝이 그 재발을 막는다.
#   ⚠ 충전-상태(가역 SOC breathing) 스냅샷 = 영구 fade 아님; 비가역화 판정은 ledger(A-3).
#   ⚠ rate-independent J2 = 크리프/유지시간 없음 → "90 MPa 로 수백 시간" 은 표현 안 됨.
KIT="$(cd "$(dirname "$0")" && pwd)"
SCR=""; for c in "$KIT/scripts" "$KIT/../scripts"; do [ -d "$c" ] && SCR="$(cd "$c" && pwd)" && break; done
VENV_ON="${VIRTUAL_ENV:-}"; NO_VENV="${MPM_NO_VENV:-}"
# ── venv 자동탐지 (2026-07-29) ─────────────────────────────────────────────────────────
#   V100 실사고: run_mpm.sh 로는 되는데 같은 명령을 새 SSH 셸에서 직접 치면
#   ModuleNotFoundError: No module named 'numpy'.  레포 안 venv 를 새 세션이 자동으로
#   타지 않기 때문이다.  스크립트가 스스로 찾아 활성화한다.  이미 활성화돼 있거나
#   ($VIRTUAL_ENV) MPM_NO_VENV=1 이면 건드리지 않는다.
if [ -z "$VENV_ON" ] && [ -z "$NO_VENV" ]; then
  for _v in "$SCR/../venv" "$SCR/../.venv" "$KIT/../venv" "$HOME/Yonghoon-DEM-DFT/venv"; do
    if [ -f "$_v/bin/activate" ]; then . "$_v/bin/activate"; echo "[venv] activated: $_v"; break; fi
  done
fi
python3 -c "import numpy" >/dev/null 2>&1 || { echo "[venv] ABORT — 이 python3 에 numpy 가 없습니다: $(command -v python3)"; echo "        venv 를 못 찾았습니다 — source <repo>/venv/bin/activate 후 재실행하거나 MPM_NO_VENV=1 로 이 검사를 끄세요."; exit 1; }
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
        --lateral-box 0.05 --n-grid 256 --arch cuda --gpu-mem 28 --frames 150
        --e-se 1.53 --nu-se 0.49)
STATE="$OUT/fab_state.npz"
# ── ① 제작 (fabrication) — 제작압 0.3 GPa, LIGGGHTS 변위-정지 규약(hold) ──
echo "=== A-1 ① 제작압 압밀 300 MPa → 소성이력 저장 ==="
if [ -f "$STATE" ] && [ "${A1_REUSE_STATE:-1}" = "1" ]; then
  echo "  (기존 $STATE 재사용 — 새로 만들려면 A1_REUSE_STATE=0)"
else
  python3 "$SCR/mpm3d_compaction.py" "${COMMON[@]}" --protocol hold --target-gpa 0.3 --save-state "$STATE" --save-metrics "$OUT/m_fab.json" || { echo "FAIL fab"; exit 1; }
fi
# ── ② 구동 (operation) — 소성이력을 이어받아 구동압 0.09 GPa 에서 재평형 ──
run_op() { local arm="$1"; local lab="$2"; shift 2; echo "=== A-1 ② [$arm] $lab @ 90 MPa ==="; python3 "$SCR/mpm3d_compaction.py" "${COMMON[@]}" --load-state "$STATE" --protocol "$arm" --target-gpa 0.09 "$@" --save-metrics "$OUT/m_${lab}_${arm}.json" || { echo "FAIL $lab/$arm — 위 트레이스"; exit 1; }; }
for ARM in servo hold; do
  run_op "$ARM" N0
  run_op "$ARM" charged --cycle-deform --cycle-n 1 --cycle-dv-sc -0.051 --cycle-dv-poly 0.059 --dv-pct-poly 0.30
  run_op "$ARM" charged_deep --cycle-deform --cycle-n 2 --cycle-dv-sc -0.059 --cycle-dv-poly 0.059 --dv-pct-poly 0.30
  echo "=== 기하 debond/void [$ARM] (그 팔의 N0 대비) ==="
  python3 "$SCR/cycle_geom_debond.py" "$OUT/m_N0_${ARM}.json" "$OUT/m_charged_${ARM}.json" "$OUT/m_charged_deep_${ARM}.json" --csv "$OUT/a1_debond_${ARM}.csv"
done
# ── ③ 제하 검증 — "구동압 앵커" 라벨이 실제 달성값인지 확인 (라벨만 붙는 것 차단) ──
echo "=== 제하 검증 (unload_status · 달성압 · 플래튼 이동) ==="
python3 - "$OUT" <<'PYEOF'
import glob, json, os, sys
bad = []
for f in sorted(glob.glob(os.path.join(sys.argv[1], "m_*.json"))):
    sv = (json.load(open(f)) or {}).get("state_provenance") or {}
    if not sv.get("plastic_history_restored"):
        continue                      # 제작(①) 런 — 제하 대상 아님
    role = sv.get("P_this_stage_role", "?")
    print("  %-28s unload=%-14s P_req=%s MPa  P_achieved=%s MPa  platen %s (%s um)  role=%s"
          % (os.path.basename(f), sv.get("unload_status"), sv.get("P_this_stage_MPa"),
             sv.get("P_achieved_MPa"), sv.get("platen_direction"), sv.get("platen_delta_um"), role))
    if str(role).endswith("_NOT_REACHED") or sv.get("unload_status") not in ("completed", "not_needed_p_within_band"):
        bad.append(os.path.basename(f))
if bad:
    print("  ⚠ 구동압에 도달하지 못한 런: " + ", ".join(bad)
          + "  → 이 형상은 제작압 형상이므로 구동압 앵커로 쓰지 마세요 "
            "(--frames 를 늘리거나 --target-gpa 를 확인).")
PYEOF
echo "완료 → $OUT/  (m_fab.json = 제작압 앵커, m_*_servo/hold.json = 구동압 90 MPa 앵커,"
echo "        a1_debond_servo.csv / a1_debond_hold.csv = 두 지그 극한 브래킷)"
echo "⚠ servo=정응력(두께가 변함) · hold=정적변위(압력이 변함).  실제 지그는 둘 사이."
