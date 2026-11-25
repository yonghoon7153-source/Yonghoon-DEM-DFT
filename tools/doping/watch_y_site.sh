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
#   OUT=… LOG=… NEXP=12 bash tools/doping/watch_y_site.sh     # 다른 이완 런
#   DFT=~/work/runs/y_dft bash tools/doping/watch_y_site.sh   # DFT 칸 켜기
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
# key 이름을 틀리면 조용히 None 이 찍힌다 — 없으면 **없다고 말한다**.
if "E_above_hull_eV_per_atom" not in d:
    print(f"  {sys.argv[2]:<12} \u26d4 E_above_hull_eV_per_atom 키가 없다 "
          f"(있는 키: {sorted(d)[:6]})")
else:
    e = d["E_above_hull_eV_per_atom"]
    tag = "ON HULL" if d.get("on_hull") else "metastable"
    print(f"  {sys.argv[2]:<12} {e*1000:8.1f} meV/atom  {tag:<11} {d.get('reduced','')}")
    dec = ", ".join(f"{k} {v}" for k, v in list((d.get("decomposition") or {}).items())[:3])
    if dec:
        print(f"  {'':<12} -> {dec}")
PY
done
[ "$FOUND" = 0 ] && echo "  · 아직 없음 (이완이 끝난 뒤 hull 블록을 돌린다 · MP_API_KEY 필요)"

# ── 5-1. Y DFT 대조 (dft_decomp_check) ────────────────────────────────────
#   DFT= 로 작업 디렉터리를 주면 이 칸이 켜진다. 안 주면 통째로 빠진다.
if [ -n "${DFT:-}" ] && [ -d "$DFT" ]; then
  echo "── Y DFT 대조 ($DFT) ──"
  DPID=$(pgrep -f "[r]un_y_dft.sh" | head -1)
  if [ -n "$DPID" ]; then
    echo "  ✅ 실행중 PID=$DPID  경과 $(ps -o etime= -p "$DPID" 2>/dev/null | tr -d ' ')"
  else
    echo "  ·  runner 없음"
  fi
  NDONE=0; NTOT=0
  for n in LiCl Li2S LiYS2 Li3PO4 Li3PS4 sc_Li_24g_perm00 sc_P_4b_perm03; do
    [ -f "$DFT/in/$n.in" ] || continue
    NTOT=$((NTOT+1))
    O="$DFT/$n.out"
    if grep -aq "JOB DONE" "$O" 2>/dev/null; then
      NDONE=$((NDONE+1))
      E=$(grep -a "^!" "$O" | tail -1 | awk '{print $5}')
      printf "    ✓ %-20s E = %s Ry\n" "$n" "${E:-?}"
    elif [ -f "$O" ]; then
      # 진행중 — SCF 반복 횟수로 어디쯤인지
      IT=$(grep -ac "iteration #" "$O" 2>/dev/null)
      LE=$(grep -a "total energy" "$O" | tail -1 | awk '{print $4}')
      printf "    ▶ %-20s scf 반복 %s · 최근 E %s\n" "$n" "${IT:-0}" "${LE:-…}"
    else
      printf "    ·  %-20s 대기\n" "$n"
    fi
  done
  echo "    합계 $NDONE/$NTOT"
  [ "$NDONE" = "$NTOT" ] && [ "$NTOT" -gt 0 ] && \
    echo "    ★ 전부 끝 — python3 tools/doping/dft_decomp_check.py --collect --out $DFT"
  if [ -f "$DFT/decomp_result.json" ]; then
    python3 - "$DFT/decomp_result.json" <<'PY' 2>/dev/null
import json, sys
d = json.load(open(sys.argv[1]))
tg = d.get("targets") or {}
if tg:
    print("  ── ΔE_decomp (클수록 안정) ──")
    for k, v in sorted(tg.items(), key=lambda x: -x[1]["delta_E_decomp_eV_per_atom"]):
        print(f"    {k:<24}{v['delta_E_decomp_eV_per_atom']*1000:+9.1f} meV/atom")
    print("  ⛔ E_above_hull 이 아니다 — 5상 공통기저 안의 비교다")
PY
  fi
fi

# ── 6. GPU 와 **기존 런** — Y 때문에 T600 이 죽지 않았나 ──────────────────
echo "── GPU ──"
nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total \
  --format=csv,noheader 2>/dev/null | awk -F, \
  '{u=$1;m=$2;t=$3;gsub(/[^0-9]/,"",m);gsub(/[^0-9]/,"",t);
    printf "  util %s · %s/%s MiB · 여유 %d MiB\n", u, m, t, t-m}'

# ⛔ 어느 런인지 이름표로 짐작하지 않는다 — **실행중 프로세스의 인자**를 읽는다.
#   (초판은 pgrep -f "run_arrhenius_6pt" 로 T900 을 판별했는데, T900 을 **기다리는**
#    대기 bash 의 명령줄에도 그 문자열이 들어 있어 대기중을 '시작됨' 으로 오탐했다.)
MDPID=$(pgrep -f "[d]isorder_ensemble_diffusion" | head -1)
if [ -n "$MDPID" ]; then
  CMD=$(tr '\0' ' ' < "/proc/$MDPID/cmdline" 2>/dev/null)
  MDT=$(echo "$CMD" | grep -oE '\-\-temperatures[= ]+[0-9]+' | grep -oE '[0-9]+$')
  MDR=$(echo "$CMD" | grep -oE '\-\-out_root[= ]+[^ ]+' | sed 's|.*runs/||; s|/.*||')
  echo "  ✅ MD 실행중  T=${MDT:-?} K · run=${MDR:-?} · PID $MDPID · $(ps -o etime= -p "$MDPID" 2>/dev/null | tr -d ' ')"
else
  echo "  ·  disorder_ensemble_diffusion 프로세스 없음"
fi
for T in 600 900; do
  N=$(ls /data/work/runs/*/modelc/s*/*/T$T/msd.json 2>/dev/null | wc -l)
  [ "$N" -gt 0 ] && echo "  ★ modelc T$T 완료 msd.json ${N}개"
done
if [ -z "$MDPID" ] && ! ls /data/work/runs/*/modelc/s*/*/T600/msd.json >/dev/null 2>&1; then
  echo "  ⛔ MD 프로세스도 없고 T600 msd.json 도 없다 — **죽었을 수 있다**"
  tail -3 /data/work/mc600.log 2>/dev/null | sed 's/^/      /'
fi
# 대기 체인이 걸려 있나 — '시작됨' 과 구별한다
if pgrep -f "[w]hile pgrep -f" >/dev/null; then
  echo "  ⏸ T900 체인 **대기중** (T600 이 끝나면 시작)"
fi
