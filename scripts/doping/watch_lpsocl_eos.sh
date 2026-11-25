#!/bin/bash
# watch_lpsocl_eos.sh — detailed live status for the LPSOCl DFT EOS chain (KISTI).
#   watch -n 60 bash ~/watch_lpsocl.sh
# Mirrors sbatch_dft_eos_lpsocl_chain.sh: 7 fixed-cell relaxes v094..v106 over
# 2 GPU streams (GPU0: v094 v098 v102 v106 / GPU1: v096 v100 v104), done-marker
# "JOB DONE", ALL_DONE flag when 7/7.
# v2 (846250-253 재가동판):
#   - 세그먼트 벽킬(큐에 RUNNING 없음)과 진짜 정체를 구분해 표시
#   - 이번 세그먼트의 carry 이벤트("carried last geometry") 표시 — ion 진행분 승계 확인
#   - 완료점 E-곡선(최소 대비 ΔE meV) 한 줄 — BM 형상/최소점 위치 즉시 확인
#   - ALL_DONE 시 llm_fitting_bm.py 실행 힌트 출력
WB=/scratch/x3430a02/kgy/lpsocl_eos
RY=13.605693
declare -A GPU=( [v094]=0 [v098]=0 [v102]=0 [v106]=0 [v096]=1 [v100]=1 [v104]=1 )
VOLS="v094 v096 v098 v100 v102 v104 v106"
now=$(date +%s)

echo "══════ KISTI LPSOCl EOS  $(date '+%m-%d %H:%M:%S') ══════"

# ---- chain (squeue) ----
echo "── 체인 (squeue, QOS 상한 4) ──"
q=$(squeue -u x3430a02 -h -n llm1 -o "  %.9i %.9T %.8M %.9L %R" 2>/dev/null | sort -k1)
if [ -n "$q" ]; then echo "$q"; else echo "  (큐에 lpsocl_eos 없음)"; fi
nq=$(squeue -u x3430a02 -h -n llm1 2>/dev/null | wc -l)
nr=$(squeue -u x3430a02 -h -n llm1 -t RUNNING 2>/dev/null | wc -l)
echo "  세그먼트: 큐 $nq개 (실행 $nr / 대기 $((nq-nr)))"
if [ -f "$WB/ALL_DONE" ]; then
  echo "  ★★ ALL_DONE — 7/7 완료, 체인 no-op ★★"
  echo "  → 다음: python3 scripts/doping/llm_fitting_bm.py --base $WB"
fi

# ---- carry events in the newest segment log ----
last=$(ls -t $WB/logs/lpsocl_eos_*.out 2>/dev/null | head -1)
if [ -n "$last" ]; then
  c=$(grep -E "carried last geometry|no carry info" "$last" 2>/dev/null | sed 's/^/  /')
  [ -n "$c" ] && { echo "── carry 이벤트 ($(basename "$last")) ──"; echo "$c"; }
fi

# ---- per-volume table ----
echo "── 볼륨별 진행 (7점 격자) ──"
active=$(ls -t $WB/v0*/relax.out 2>/dev/null | while read f; do \
          grep -q "JOB DONE" "$f" || { echo "$f"; break; }; done)
done=0
for v in $VOLS; do
  f=$WB/$v/relax.out
  g=${GPU[$v]}
  cm=""
  [ -n "$last" ] && grep -q "\[$v\] incomplete — carried" "$last" 2>/dev/null && cm="↻"
  if [ ! -f "$f" ]; then
    printf "  %-5s [G%s] ⬚ 대기\n" "$v" "$g"; continue
  fi
  if grep -q "JOB DONE" "$f" 2>/dev/null; then
    e=$(grep '^!' "$f" 2>/dev/null | tail -1 | awk '{print $5}')
    ev=$(awk -v e="${e:-0}" -v r=$RY 'BEGIN{printf "%.2f", e*r}')
    conv="?"; grep -q "bfgs converged" "$f" && conv="수렴"
    grep -q "maximum number of steps" "$f" && conv="MAXSTEP"
    printf "  %-5s [G%s] ✅ DONE(%-7s) E=%s Ry (%s eV)\n" "$v" "$g" "$conv" "${e:-–}" "$ev"
    done=$((done+1))
  else
    st=$(grep -c "Self-consistent Calculation" "$f" 2>/dev/null)   # ionic steps (이번 세그먼트 기준)
    en=$(grep '^!' "$f" 2>/dev/null | tail -1 | awk '{print $5}')
    fo=$(grep "Total force" "$f" 2>/dev/null | tail -1 | awk '{print $4}')
    age=$(( now - $(stat -c %Y "$f" 2>/dev/null || echo $now) ))
    mark="  "; [ "$f" = "$active" ] && mark="▶ "
    if [ "$nr" -eq 0 ]; then
      tag="⏸ 벽킬-carry대기"          # 세그먼트가 없는데 미완 = 4h 벽 킬, 다음 세그먼트가 승계
    elif [ $age -gt 300 ]; then
      tag="⚠정체${age}s"              # 세그먼트 실행 중인데 출력이 멈춤 = 진짜 이상
    else
      tag="진행"
    fi
    printf "  %s%-5s%s [G%s] %s  ion≈%s  E=%s Ry  |F|=%s  (%ds前)\n" \
           "$mark" "$v" "$cm" "$g" "$tag" "${st:-0}" "${en:-–}" "${fo:-–}" "$age"
  fi
done
echo "  ─────  완료 $done / 7  ─────"

# ---- E-curve sanity line (완료점 최소 대비; BM이면 최소점 양쪽 단조 상승) ----
emin=""
for v in $VOLS; do
  f=$WB/$v/relax.out
  grep -q "JOB DONE" "$f" 2>/dev/null || continue
  e=$(grep '^!' "$f" | tail -1 | awk '{print $5}')
  [ -z "$e" ] && continue
  if [ -z "$emin" ] || awk -v a="$e" -v b="$emin" 'BEGIN{exit !(a<b)}'; then emin=$e; fi
done
if [ -n "$emin" ]; then
  out="  "
  for v in $VOLS; do
    f=$WB/$v/relax.out
    e=$(grep '^!' "$f" 2>/dev/null | tail -1 | awk '{print $5}')
    [ -z "$e" ] && continue
    s=""; grep -q "JOB DONE" "$f" || s="*"
    de=$(awk -v e="$e" -v m="$emin" 'BEGIN{printf "%+d", (e-m)*13605.7}')
    out="$out$v ${de}${s}  "
  done
  echo "── E-곡선 (완료 최소 대비 ΔE meV, *=진행중 잠정) ──"
  echo "$out"
fi

# ---- latest segment log tail ----
echo "── 최신 세그먼트 로그 ──"
if [ -n "$last" ]; then
  echo "  ($(basename "$last"))"
  tail -6 "$last" 2>/dev/null | sed 's/^/  /'
else
  echo "  (로그 없음 — 세그먼트 아직 시작 안 함)"
fi
