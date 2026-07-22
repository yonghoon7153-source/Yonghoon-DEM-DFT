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

# ═══════════════ elastic DFT (lpsocl 방법; pw.x라 MD 후 순차) ═══════════════
EOUT=${EOUT:-/data/work/runs/comp2_elastic_dft}
ELOG=${ELOG:-$HOME/comp2_elastic_dft.log}
echo ""
echo "══ comp2 elastic DFT (12 relaxed-ion strain ±0.005 → full 6×6 → VRH) ══"
if pgrep -f 'run_comp2_elastic_dft' >/dev/null 2>&1; then echo "  실행중 ✔"
else echo "  (러너 안 보임 — 완료/미시작)"; fi
if [ -f "$EOUT/elastic_fit.txt" ]; then
  echo "  ✅ fit 완료:"
  grep -aiE "C1[124]|C44|B_VRH|G_VRH|VRH|^ *nu|zener|Pugh|Cauchy|Vickers|Universal|density|sound|Debye|E *=" "$EOUT/elastic_fit.txt" | tail -16 | sed 's/^/    /'
  echo "    → 비교: comp1(LPSCl) E_VRH = 29.1 GPa"
elif [ -d "$EOUT" ]; then
  nd=$(grep -l "JOB DONE" "$EOUT"/strain_*.out 2>/dev/null | wc -l)
  echo "  strain 완료 ${nd}/12"
  tail -2 "$ELOG" 2>/dev/null | grep -q "UMA.*대기" && echo "  ⏳ UMA(MD) 끝나길 대기중 (pw.x 공존 금지 규율)"
  grep -aE "pw.x strain|strain_.* OK|FAIL|GPU free" "$ELOG" 2>/dev/null | tail -3 | sed 's/^/    /'
else
  echo "  (out_dir 없음 — 아직 시작 전; c2eldft tmux 확인)"
fi

# ═══════════════ ICOHP LOBSTER (elastic 후 COEXIST) ═══════════════
LOUT=${LOUT:-/data/work/runs/comp2_lobster}
LLOG=${LLOG:-$HOME/comp2_lobster.log}
echo ""
echo "══ comp2 ICOHP (LOBSTER; all-PAW scf+nscf nbnd500 → Li-S/Cl/Br pCOHP) ══"
if pgrep -f 'run_comp2_lobster' >/dev/null 2>&1; then echo "  실행중 ✔"
else echo "  (러너 안 보임 — 완료/미시작)"; fi
if [ -s "$LOUT/ICOHPLIST.lobster" ]; then
  echo "  ✅ COHP 완료·등록 ($(grep -aioE 'spilling: *[0-9.]+%' "$LOUT/lobster_run.out" 2>/dev/null | head -1))"
  [ -s "$LOUT/ICOBILIST.lobster" ] && echo "     +ICOBI(bond order) ✅  | ICOHP: Li-Br(-1.93) < Li-Cl(-2.11) 확정"
elif [ -d "$LOUT" ]; then
  s="-"; n="-"
  grep -aq "JOB DONE" "$LOUT/lobster_scf.out"  2>/dev/null && s="✔"
  grep -aq "JOB DONE" "$LOUT/lobster_nscf.out" 2>/dev/null && n="✔"
  echo "  scf: $s | nscf: $n | LOBSTER(CPU): 대기"
  tail -2 "$LLOG" 2>/dev/null | grep -q "대기" && echo "  ⏳ MD/elastic 끝나길 대기중 (또는 GPU 대기)"
  grep -aE "pw.x lobster|lobster_.* OK|FAIL|LOBSTER start|GPU free ..* — go" "$LLOG" 2>/dev/null | tail -3 | sed 's/^/    /'
else
  echo "  (out_dir 없음 — elastic 끝난 뒤 c2lob COEXIST=1 실행)"
fi

# ═══════════════ b2o3 elastic (comp2 elastic 후 큐) ═══════════════
B2OUT=${B2OUT:-$HOME/work/b2o3_elastic}
B2LOG=${B2LOG:-$HOME/b2o3_elastic.log}
echo ""
echo "══ b2o3 elastic DFT (128atom · 12 strain ±0.01 → VRH) ══"
if pgrep -f 'run_b2o3_elastic_dft' >/dev/null 2>&1; then echo "  러너 실행중 ✔"
else echo "  (러너 안 보임 — 완료/미시작)"; fi
if [ -f "$B2OUT/elastic_fit.txt" ]; then
  echo "  ✅ fit 완료:"
  grep -aiE "B_VRH|G_VRH|VRH|Pugh|Cauchy|Vickers|Debye|density|sound|E *=" "$B2OUT/elastic_fit.txt" | tail -14 | sed 's/^/    /'
elif [ -d "$B2OUT" ]; then
  if [ -f "$B2OUT/strain_11_p.in" ]; then
    nd=$(grep -l "JOB DONE" "$B2OUT"/strain_*.out 2>/dev/null | wc -l)
    echo "  strain 완료 ${nd}/12"
  else echo "  (strain 생성 전)"; fi
  tail -3 "$B2LOG" 2>/dev/null | grep -q "comp2 elastic 아직" && echo "  ⏳ comp2 elastic 끝나길 대기중"
  grep -aE "pw.x strain|strain_.* OK|FAIL|VRAM free|종료 감지" "$B2LOG" 2>/dev/null | tail -3 | sed 's/^/    /'
else echo "  (out_dir 없음 — b2oel tmux 확인)"
fi
