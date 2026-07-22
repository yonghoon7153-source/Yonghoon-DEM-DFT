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
for c in Li_on_hbn Li_on_graphene Li_in_gallery Li_in_gallery_2L2L; do
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
    dat=$(ls -t "$N/$ACT"/*.dat 2>/dev/null | head -1)
    if [ -n "$dat" ]; then
      echo "    barrier 프로파일 (reaction-coord  E[eV], 피크=안장):"
      awk 'NF>=2 && ($1+0==$1){printf "      %5.2f   %+9.4f\n",$1,$2}' "$dat" 2>/dev/null | head -9
    fi
    grep -a "activation energy" "$no" 2>/dev/null | tail -2 | sed 's/^/    /'
    grep -aiE "tot_error|climbing image|neb: reached" "$no" 2>/dev/null | tail -2 | sed 's/^/    /'
  fi
fi
echo "  기준: hBN 표면 Shi2017=0.10 / graphene 문헌~0.3 / gallery=신규(핵심값). 수렴 전 Ea는 추정치."
