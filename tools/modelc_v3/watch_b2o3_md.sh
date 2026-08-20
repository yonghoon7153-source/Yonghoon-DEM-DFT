#!/usr/bin/env bash
# UMA-MD 라이브 점검. 1회 출력 (반복: watch -n 60 bash <이 파일> <루트>).
#
# 2026-08-20 확장 — 옛 판은 `$R/d0.00_cfg0/T{600,800,1000}/msd.json` **한 겹**만 봤다.
#   highT_reseed 계열은 `$R/<sys>/s<N>/d0.00_cfg0/T<K>/` 로 두 겹 더 깊어서 아무것도
#   안 보였다. 이제 msd.json/md.log 를 **재귀 탐색**하므로 두 배치 모두 본다.
#
# ⭐ traj.xyz 칸이 이 판의 핵심이다. 2026-07 highT_reseed 는 --save_traj 가 빠져
#   msd.json 12개 · traj.xyz **0개**로 끝났는데 화면상으로는 정상 완료였다(F9).
#   같은 사고가 조용히 반복되지 않도록 궤적 개수를 **완료 개수와 나란히** 찍는다.
#
# ⛔ 이 도구가 못 하는 것: (1) D/Ea 의 물리적 타당성 판정 — 숫자를 옮길 뿐이다.
#   (2) 게이트 판정 (골격 β 는 msd_diffusive_check.py --framework 소관).
#   (3) 죽은 런과 대기 중인 런 구별 — 프로세스가 없고 msd.json 도 없으면 둘 다 '대기'다.
set +H

R="${1:-/data/work/runs/b2o3_md}"
TOTAL_PS="${2:-}"                    # equilib+prod [ps]. 비우면 md.log 진행률을 ps 로만 표시

echo "════ $(date '+%m-%d %H:%M:%S')  UMA-MD  ($R) ════"

if P=$(pgrep -f disorder_ensemble_diffusion.py); then
  for p in $P; do
    lbl=$(tr '\0' ' ' < /proc/$p/cmdline 2>/dev/null | grep -o -- '--out_root [^ ]*' | awk '{print $2}')
    echo "✅ MD PID=$p  경과 $(ps -o etime= -p $p 2>/dev/null | tr -d ' ')  ${lbl##*/runs/}"
  done
else
  echo "⛔ 실행 중 MD 없음 (끝났거나 죽음)"
fi

# ── 런별 상태 (재귀) ─────────────────────────────────────────────────────────
DONE=0; RUNNING=0; TRAJ=0
echo "── 런별 상태 ──"
while IFS= read -r d; do
  [ -z "$d" ] && continue
  rel=${d#"$R"/}; rel=${rel%/}
  t="✗"; if [ -f "$d/traj.xyz" ]; then t="✓"; TRAJ=$((TRAJ+1)); fi
  if [ -f "$d/msd.json" ]; then
    DONE=$((DONE+1))
    printf "  %-34s ✓ 완료  traj %s  %s\n" "$rel" "$t" \
      "$(python3 -c "
import json,sys
try:
    v=json.load(open('$d/msd.json')).get('D_Li_cm2_s')
    print('D_Li = %.3e cm2/s'%v if v else 'D n/a')
except Exception as e: print('읽기 실패: %s'%e)" 2>/dev/null)"
  elif [ -f "$d/md.log" ]; then
    RUNNING=$((RUNNING+1))
    l=$(tail -1 "$d/md.log" 2>/dev/null)
    ps=$(echo "$l" | awk '{print $1}'); K=$(echo "$l" | awk '{print $NF}')
    printf "  %-34s ▶ 진행  traj %s  ~%s%s ps  (%s K)\n" "$rel" "$t" "$ps" \
      "${TOTAL_PS:+/$TOTAL_PS}" "$K"
  else
    printf "  %-34s · 대기  traj %s\n" "$rel" "$t"
  fi
done < <(find "$R" -type d -name 'T[0-9]*' 2>/dev/null | sort)
#        ↑ T<K> 디렉터리는 **파일이 없어도** 낸다 — 드라이버가 폴더를 먼저 만들고 MD 를
#          시작하므로 그 구간이 '대기'다. 파일 유무로 거르면 대기 분기가 죽은 코드가 된다.

echo "── 합계 ──"
echo "  완료 $DONE · 진행 $RUNNING · 궤적 $TRAJ"
if [ "$DONE" -gt 0 ] && [ "$TRAJ" -lt "$DONE" ]; then
  echo "  ⛔⛔ 완료 $DONE 인데 궤적은 $TRAJ 개다 — --save_traj 가 빠졌거나 resume 이 건너뛰었다."
  echo "       이대로 끝나면 골격 게이트를 **소급으로 못 돌린다** (2026-07 F9 재발)."
fi

for f in "$R"/ensemble_results.json "$R"/*/ensemble_results.json; do
  [ -f "$f" ] || continue
  echo "── $(dirname "${f#"$R"/}") 헤드라인 ──"
  grep -a -A8 '"headline"' "$f" 2>/dev/null | head -10 | sed 's/^/  /'
done

echo "── GPU ──"
nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv,noheader 2>/dev/null | sed 's/^/  /'
