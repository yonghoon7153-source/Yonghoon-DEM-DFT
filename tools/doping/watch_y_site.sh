#!/usr/bin/env bash
# watch_y_site.sh — Y 자리선호 검증(UMA 이완 → E_above_hull) 진행 감시.
#
# 왜 GPU 칸이 같이 있나: 이 런은 200 ps modelc T600 과 **같은 GPU 를 나눠 쓴다**.
#   Y 쪽에 --vram_fraction 0.10 을 걸어 Y 가 먼저 죽게 해뒀으므로, 확인해야 할 것은
#   "Y 가 끝났나" 만이 아니라 **"T600 이 아직 살아있나"** 다. 둘을 한 화면에 둔다.
#
# ⛔ 이 스크립트가 못 하는 것
#   · 결과의 옳고 그름을 판정하지 않는다 (E/atom 순서는 조성이 달라 순위가 아니다).
#   · 죽은 원인을 진단하지 않는다 — 로그 꼬리만 보여준다.
#   · hull 은 MP_API_KEY 가 있어야 돈다. 없으면 "미실행" 으로 보인다.
#
# 사용:
#   watch -n 30 'bash tools/doping/watch_y_site.sh'
#   bash tools/doping/watch_y_site.sh          # 1회
set +e
set +H

OUT="${OUT:-/data/work/runs/y_site_test}"
LOG="${LOG:-/data/work/runs/y_relax.log}"
NEXP="${NEXP:-4}"                       # 기대 구조 수 (sc_P_4b · sc_Li_24g · P_4b · Li_24g)

echo "════════ $(date '+%Y-%m-%d %H:%M:%S')  Y site-preference ════════"

# ── 1. 이완 프로세스 ──────────────────────────────────────────────────────
PID=$(pgrep -f "[b]2o3_uma_relax.py --generic" | head -1)
if [ -n "$PID" ]; then
  ET=$(ps -o etime= -p "$PID" 2>/dev/null | tr -d ' ')
  echo "이완 ✅ 실행중   PID=$PID   경과 $ET"
else
  echo "이완 ·  프로세스 없음 (끝났거나 죽었다 — 아래 로그 꼬리를 볼 것)"
fi

# ── 2. 진행 ──────────────────────────────────────────────────────────────
NCIF=$(ls "$OUT"/relaxed/*.cif 2>/dev/null | wc -l)
echo "진행: 이완 완료 ${NCIF}/${NEXP} 구조"
if [ -f "$LOG" ]; then
  # FIRE 스텝이 도는 중인지 (마지막 갱신 시각으로 멈춤 판별)
  AGE=$(( $(date +%s) - $(stat -c %Y "$LOG" 2>/dev/null || date +%s) ))
  echo "로그: $(du -h "$LOG" 2>/dev/null | cut -f1) · ${AGE}s 전 갱신"
  [ "$AGE" -gt 600 ] && [ -n "$PID" ] && echo "  ⚠ 10분 넘게 로그가 안 움직인다 — 멈춤 의심"
fi

# ── 3. 실패 신호 (조용히 넘기지 않는다) ───────────────────────────────────
if [ -f "$LOG" ]; then
  BAD=$(grep -a -cE "FAIL|Traceback|CUDA out of memory|RuntimeError" "$LOG" 2>/dev/null)
  if [ "${BAD:-0}" -gt 0 ]; then
    echo "⛔ 오류 신호 ${BAD}건:"
    grep -a -E "FAIL|Traceback|CUDA out of memory|RuntimeError" "$LOG" 2>/dev/null | tail -3 | sed 's/^/    /'
  fi
fi

# ── 4. 결과 표 (--generic 이 끝에 찍는다) ─────────────────────────────────
if grep -aq "^structure" "$LOG" 2>/dev/null; then
  echo "── 이완 결과 ──"
  grep -a -A "$((NEXP + 2))" "^structure" "$LOG" 2>/dev/null | tail -n "$((NEXP + 2))" | sed 's/^/  /'
  echo "  ⛔ 위 E/atom 순서를 자리선호로 읽지 말 것 — 원자수가 다르다(108/100/56/48)."
  echo "     판정은 E_above_hull 로: convex_hull_ehull.py --mode uma"
fi

# ── 5. hull ──────────────────────────────────────────────────────────────
echo "── E_above_hull ──"
FOUND=0
for S in sc_P_4b sc_Li_24g P_4b Li_24g; do
  F="$OUT/ehull_$S.json"
  [ -f "$F" ] || continue
  FOUND=1
  python3 - "$F" "$S" <<'PY' 2>/dev/null || echo "  $S: 읽기 실패"
import json, sys
d = json.load(open(sys.argv[1]))
e = d.get("e_above_hull_eV_per_atom", d.get("e_above_hull"))
print(f"  {sys.argv[2]:<12} E_hull = {e}  ({d.get('reduced') or d.get('composition','')})")
PY
done
[ "$FOUND" = 0 ] && echo "  · 아직 없음 (이완이 끝난 뒤 hull 블록을 돌린다 · MP_API_KEY 필요)"

# ── 6. GPU 와 **기존 런** — Y 때문에 T600 이 죽지 않았나 ──────────────────
echo "── GPU ──"
nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total \
  --format=csv,noheader 2>/dev/null | awk -F, \
  '{u=$1;m=$2;t=$3;gsub(/[^0-9]/,"",m);gsub(/[^0-9]/,"",t);
    printf "  util %s · %s/%s MiB · 여유 %d MiB\n", u, m, t, t-m}'

if pgrep -f "[d]isorder_ensemble_diffusion" >/dev/null; then
  MP=$(pgrep -f "[d]isorder_ensemble_diffusion" | head -1)
  echo "  ✅ modelc T600 살아있음 (PID $MP · $(ps -o etime= -p "$MP" 2>/dev/null | tr -d ' '))"
else
  if ls /data/work/runs/highT_reseed_traj/modelc/s4/*/T600/msd.json >/dev/null 2>&1; then
    echo "  ★ modelc T600 **완료** — msd.json 있음 (다음: T900 체인)"
  else
    echo "  ⛔ modelc T600 프로세스도 없고 msd.json 도 없다 — **죽었을 수 있다**"
    tail -3 /data/work/mc600.log 2>/dev/null | sed 's/^/      /'
  fi
fi
pgrep -f "[r]un_arrhenius_6pt" >/dev/null && echo "  ✅ T900 시작됨"
