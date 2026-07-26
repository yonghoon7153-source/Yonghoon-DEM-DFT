#!/usr/bin/env bash
# watch_neb.sh — VGCF/h-BN Li 확산 CI-NEB 상세 진행 (kgy).
#   watch -n 60 'bash ~/Yonghoon-DEM-DFT/tools/vgcf_hbn/watch_neb.sh'
# Pass1 endpoint-B relax(ion/force/E) + Pass2 CI-NEB(Ea→/←, iter, barrier 프로파일).
set +H
W=${WORK:-$HOME/work/vgcf_hbn}; N=$W/neb
echo "══ Li diffusion CI-NEB 상세 (hollow→hollow 2.46A · 7img)  $(date '+%m-%d %H:%M:%S') ══"
gpu=$(nvidia-smi --query-gpu=memory.used,memory.free,utilization.gpu --format=csv,noheader,nounits 2>/dev/null | head -1)
run=$(pgrep -af 'neb\.x|pw\.x' 2>/dev/null | grep -aoE '[A-Za-z0-9_]+\.in' | head -1)
echo "  실행중: ${run:-없음}  | GPU ${gpu} (used,free,util%)"
sess=$(tmux ls 2>/dev/null | grep -oE 'vgcf(qe|2L|neb)' | tr '\n' ' ')
echo "  세션: ${sess:-없음}"

echo "── 케이스 요약 (Pass1 endpoint / Pass2 CI-NEB) ──"
for c in Li_on_hbn Li_on_graphene Li_in_gallery Li_in_gallery_2L2L Li_in_gallery_gr2L Li_in_gallery_2L; do
  bo=$N/${c}_nebB.out; no=$N/$c/neb.out
  if [ ! -f "$bo" ]; then printf "  %-18s · endpoint-B 대기\n" "$c"; continue; fi
  if ! grep -aq "JOB DONE" "$bo" 2>/dev/null; then
    ni=$(grep -ac "Total force" "$bo"); tf=$(grep -a "Total force" "$bo" | tail -1 | awk '{print $4}')
    printf "  %-18s ↻ endpoint relax (ion %s, |F|=%s)\n" "$c" "${ni:-0}" "${tf:-?}"; continue
  fi
  if [ ! -f "$no" ]; then printf "  %-18s ✅endpoint → NEB 대기\n" "$c"; continue; fi
  it=$(grep -ac "activation energy (->)" "$no")
  ef=$(grep -a "activation energy (->)" "$no" | tail -1 | awk '{print $(NF-1)}')
  eb=$(grep -a "activation energy (<-)" "$no" | tail -1 | awk '{print $(NF-1)}')
  if grep -aiq "convergence achieved" "$no"; then
    printf "  %-18s ✅수렴  Ea→ %s / ← %s eV (iter %s)\n" "$c" "${ef:-?}" "${eb:-?}" "$it"
  elif grep -aqE "Error in routine|MPI_ABORT|%%%%%%" "$no"; then
    printf "  %-18s 💥 crash (tail 확인)\n" "$c"
  else
    printf "  %-18s ↻ NEB iter %s  Ea→~%s / ←~%s\n" "$c" "${it:-0}" "${ef:-?}" "${eb:-?}"
  fi
done

# ── 현재 활성 케이스 상세 ──
ACT=""; MODE=""
for c in Li_in_gallery_2L2L Li_in_gallery Li_on_graphene Li_on_hbn; do
  bo=$N/${c}_nebB.out; no=$N/$c/neb.out
  if [ -f "$bo" ] && ! grep -aq "JOB DONE" "$bo" 2>/dev/null; then ACT=$c; MODE=endpoint; break; fi
  if [ -f "$no" ] && ! grep -aiq "convergence achieved" "$no" 2>/dev/null; then ACT=$c; MODE=neb; break; fi
done
if [ -n "$ACT" ]; then
  echo "── 상세: $ACT ($MODE) ──"
  if [ "$MODE" = endpoint ]; then
    grep -aE "^!|Total force|bfgs converged|number of bfgs" "$N/${ACT}_nebB.out" 2>/dev/null | tail -3 | sed 's/^/    /'
    echo "    (endpoint-B relax 수렴하면 이 케이스 NEB 입력 자동 생성)"
  else
    no=$N/$ACT/neb.out
    # 살아있음 지표: 이미지 SCF(tmp/*/PW.out)가 진짜 진행 — neb.out은 iteration 경계에서만 갱신되므로 정체가 정상
    gu=$(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits 2>/dev/null | head -1)
    imgf=$(find "$N/$ACT/tmp" -name "PW.out" -printf '%T@ %p\n' 2>/dev/null | sort -n | tail -1 | cut -d' ' -f2)
    if [ -n "$imgf" ]; then
      img=$(basename "$(dirname "$imgf")"); isc=$(grep -ac "iteration #" "$imgf" 2>/dev/null)
      iage=$(( $(date +%s) - $(stat -c%Y "$imgf" 2>/dev/null || echo 0) ))
      if [ "$iage" -lt 120 ] || [ "${gu:-0}" -ge 50 ] 2>/dev/null; then
        echo "    ✔ 살아있음: 이미지 ${img} SCF iter ${isc} 진행중 (${iage}s前 갱신, GPU ${gu}%) · 첫 NEB iter은 무거움"
      else echo "    ⚠ 이미지 out ${iage}s 정체 + GPU ${gu}% — hang 의심"; fi
    else
      s1=$(stat -c%s "$no" 2>/dev/null); sleep 2; s2=$(stat -c%s "$no" 2>/dev/null)
      [ "${s2:-0}" -gt "${s1:-0}" ] && echo "    ✔ neb.out 증가중" || echo "    ⚠ neb.out 정체·GPU ${gu}%"
    fi
    echo "    neb.out 갱신 $(stat -c '%y' "$no" 2>/dev/null | cut -d. -f1) (iteration 경계에서만 갱신)"
    it=$(grep -ac "activation energy (->)" "$no" 2>/dev/null)
    dat=$(ls -t "$N/$ACT"/*.dat 2>/dev/null | head -1)
    if [ -n "$dat" ] && [ -s "$dat" ]; then
      echo "    barrier 프로파일 (iter $it, 피크=안장):"
      awk 'NF>=2 && ($1+0==$1){printf "      %5.2f   %+9.4f\n",$1,$2}' "$dat" 2>/dev/null | head -9
    else
      echo "    (iter $it 완료 — 첫 iteration은 7 image 초기 SCF라 오래; 프로파일은 iter 1부터)"
    fi
    grep -aiE "image [0-9]|scf iteration|estimated scf|activation energy|tot_error|climbing image|reached" "$no" 2>/dev/null | tail -4 | sed 's/^/    /'
    # ── 수렴 ETA: max force error → path_thr, iter당 감소율로 남은 iter 추정 ──
    thr=$(grep -aiE 'path_thr' "$N/$ACT"/neb.in 2>/dev/null | head -1 | sed -E 's/.*=[[:space:]]*//; s/[^0-9.].*//'); thr=${thr:-0.05}
    errs=$(grep -aE '^ +[0-9]+ +-?[0-9]+\.[0-9]+ +[0-9]+\.[0-9]+ +[TF]' "$no" 2>/dev/null | awk '{print $3}' | \
           awk '{a[NR]=$1} END{for(i=1;i<=NR;i+=7){m=0;for(j=i;j<i+7;j++)if(a[j]>m)m=a[j];print m}}')
    en=$(echo "$errs" | tail -1); ep=$(echo "$errs" | tail -2 | head -1)
    if [ -n "$en" ]; then
      left=$(awk -v n="$en" -v p="$ep" -v t="$thr" 'BEGIN{
        if(n+0<=t+0){print "0 (수렴권)"; exit}
        if(p!="" && p+0>n+0 && n+0>0){r=n/p; L=log(t/n)/log(r); printf "%.0f", (L<0?0:L)} else print "?(추이부족)"}')
      echo "    ⏱ 수렴 ETA: max|F|=${en} → 목표 ${thr} (직전 ${ep:-–}) · 대략 ${left} iter 남음"
    fi
  fi
fi
echo "  기준: hBN 표면 Shi2017=0.10 / graphene 문헌~0.3 / gallery 2L2L=0.1473(대표값). 수렴 전 Ea는 추정치."
echo "  2x2 gallery 행렬: 1L1L 0.3567 · 2L2L 0.1473 완료 / gr2L(2L|1L) · 2L(1L|2L) 진행 — 209 meV 층수효과 분해용."
