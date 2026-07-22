#!/usr/bin/env bash
# =============================================================================
# watch_comp2_md.sh — comp2 (LPSClBr) MD 전도도 감시 (gabia). 3seed×3T UMA.
#   watch -n 60 'bash ~/Yonghoon-DEM-DFT/tools/ionic/watch_comp2_md.sh'
# seed 완료(ensemble_results.json)·T-run 완료(msd.json)·per-seed D/Ea·최종 3-seed Ea.
# =============================================================================
set +H
OUTROOT=${OUTROOT:-$HOME/work/runs/comp2_md}
LOG=${LOG:-$HOME/comp2_md.log}
echo "══ comp2 MD (Li6PS5Cl0.5Br0.5 · 3seed×3T · UMA-s-1p1 · MSD 2-50ps)  $(date '+%m-%d %H:%M:%S') ══"

if pgrep -f 'run_comp2_md|disorder_ensemble_diffusion' >/dev/null 2>&1; then echo "  실행중 ✔"
else echo "  (러너/드라이버 안 보임 — 완료됐거나 중단)"; fi
echo "  GPU: $(nvidia-smi --query-gpu=memory.used,memory.free,utilization.gpu --format=csv,noheader 2>/dev/null)"

# 진행 게이지
done_seeds=""
for S in 2 3 4; do [ -f "$OUTROOT/s$S/ensemble_results.json" ] && done_seeds="$done_seeds s$S"; done
nd=$(echo $done_seeds | wc -w)
msd=$(find "$OUTROOT" -name msd.json 2>/dev/null | wc -l)
echo "── 진행: seed ${nd}/3 완료${done_seeds:+ ($done_seeds)} | T-run(msd.json) ${msd}/9 ──"

# 현재 T-run ps (ASE md.log 마지막 줄 = Time[ps]; equilib 0-5 + prod 5-205)
ml=$(find "$OUTROOT" -name md.log -printf '%T@\t%p\n' 2>/dev/null | sort -n | tail -1 | cut -f2)
if [ -n "$ml" ]; then
  last=$(grep -aE '^[[:space:]]*[0-9]' "$ml" | tail -1)
  rel=${ml#$OUTROOT/}; rel=${rel%/md.log}
  echo "── 현재 run: ${rel} ──"
  [ -n "$last" ] && echo "$last" | awk '{ps=$1+0; Tk=$NF+0;
    if(ps<=5.0) printf "  ⏳ equilib %.2f / 5 ps   (T=%.0f K)\n", ps, Tk;
    else printf "  ⏳ prod %.1f / 200 ps   (총 %.1f/205 ps, T=%.0f K)\n", ps-5.0, ps, Tk }'
fi

echo "── 최근 진행 (log) ──"
grep -aE "seed [0-9]|T=[0-9]+|Ea =|prod|equilib" "$LOG" 2>/dev/null | tail -6 | sed 's/^/  /'

# 완료 seed별 D/Ea (D_per_T 3개면 Ea 계산 = collect와 동일)
if [ "$nd" -ge 1 ]; then
  echo "── 완료 seed D/Ea ──"
  for S in 2 3 4; do
    p="$OUTROOT/s$S/ensemble_results.json"
    [ -f "$p" ] || continue
    python3 - "$p" "$S" <<'PY' 2>/dev/null
import json, sys, numpy as np
p, S = sys.argv[1], sys.argv[2]
try:
    lv = json.load(open(p))["levels"][0]["configs"][0]
    D = lv.get("D_per_T", [])
    if len(D) == 3:
        x = 1.0/np.array([600.,800.,1000.]); m,_ = np.polyfit(x, np.log(D), 1)
        print(f"  s{S}: Ea={-m*8.617333e-5:.4f} eV | D(600/800/1000)=" + ", ".join(f"{d:.2e}" for d in D))
    else:
        print(f"  s{S}: T진행중 D={['%.2e'%d for d in D]}")
except Exception as e:
    print(f"  s{S}: 파싱대기 ({e})")
PY
  done
fi

# 최종 3-seed Ea (러너 collect가 all-done 후 로그에 찍음)
if [ "$nd" = 3 ]; then
  echo "── ★ 최종 (3-seed collect) ──"
  grep -aE "comp2 Ea|anchors" "$LOG" 2>/dev/null | tail -2 | sed 's/^/  /'
fi
echo "── log tail ──"; tail -3 "$LOG" 2>/dev/null | sed 's/^/    /'
