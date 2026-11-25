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

# ── 생존 판정 (2026-07-29 추가) ─────────────────────────────────────────
# ⚠ neb.out 은 **iteration 경계에서만** 갱신되므로 "정체 = 죽음"이 아니다.
#   반대로 재부팅하면 tmux 도 프로세스도 통째로 사라져 아래가 전부 빈다.
#   그 둘을 가르는 근거는 (a) 프로세스 나이 (b) 로그 mtime vs 부팅시각 (c) GPU 사용률.
BOOT=$(uptime -s 2>/dev/null); BOOTS=$(date -d "$BOOT" +%s 2>/dev/null || echo 0)
# ⚠ 브래킷 회피: 패턴이 호출한 셸의 명령줄에 그대로 있으면 pgrep 이 자기 부모를 문다
#   (실제로 neb.x 가 없는데 ALIVE 로 찍혔다). [n]eb 는 "neb" 를 매치하되 자기 자신엔 안 걸린다.
NPID=$(pgrep -f '[n]eb\.x' | head -1)
echo "  부팅 ${BOOT:-?} ($(uptime -p 2>/dev/null))"
if [ -n "$NPID" ]; then
  echo "  ✔ neb.x ALIVE  pid $NPID  $(ps -o etime= -p "$NPID" | tr -d ' ') 경과"
else
  LAST=$(find "$N" -name 'neb.out' -printf '%T@ %p\n' 2>/dev/null | sort -n | tail -1)
  LT=${LAST%% *}; LP=${LAST#* }
  if [ -n "$LT" ]; then
    AGE=$(( $(date +%s) - ${LT%.*} ))
    if [ "${LT%.*}" -lt "$BOOTS" ] 2>/dev/null; then
      echo "  ⛔ **재부팅으로 죽음** — 마지막 neb.out 이 부팅보다 이르다 ($LP)"
    else
      echo "  ⛔ neb.x 없음 — 마지막 neb.out $((AGE/60))분 전 ($LP). 끝났거나 죽었다."
    fi
    echo "     재기동: tmux new -d -s vgcfneb 'bash tools/vgcf_hbn/run_neb_kgy.sh'"
  else
    echo "  · neb.x 없음 · neb.out 도 없음 — 아직 시작 전"
  fi
fi

echo "── 케이스 요약 (Pass1 endpoint / Pass2 CI-NEB) ──"
for c in Li_on_hbn Li_on_graphene Li_in_gallery Li_in_gallery_2L2L Li_in_gallery_gr2L Li_in_gallery_2L Li_on_graphene_2L; do
  bo=$N/${c}_nebB.out; no=$N/$c/neb.out
  if [ ! -f "$bo" ]; then printf "  %-19s · endpoint-B 대기\n" "$c"; continue; fi
  if ! grep -aq "JOB DONE" "$bo" 2>/dev/null; then
    ni=$(grep -ac "Total force" "$bo"); tf=$(grep -a "Total force" "$bo" | tail -1 | awk '{print $4}')
    printf "  %-19s ↻ endpoint relax (ion %s, |F|=%s)\n" "$c" "${ni:-0}" "${tf:-?}"; continue
  fi
  if [ ! -f "$no" ]; then printf "  %-19s ✅endpoint → NEB 대기\n" "$c"; continue; fi
  it=$(grep -ac "activation energy (->)" "$no")
  ef=$(grep -a "activation energy (->)" "$no" | tail -1 | awk '{print $(NF-1)}')
  eb=$(grep -a "activation energy (<-)" "$no" | tail -1 | awk '{print $(NF-1)}')
  if grep -aiq "convergence achieved" "$no"; then
    printf "  %-19s ✅수렴  Ea→ %s / ← %s eV (iter %s)\n" "$c" "${ef:-?}" "${eb:-?}" "$it"
  elif grep -aqE "Error in routine|MPI_ABORT|%%%%%%" "$no"; then
    printf "  %-19s 💥 crash (tail 확인)\n" "$c"
  else
    printf "  %-19s ↻ NEB iter %s  Ea→~%s / ←~%s\n" "$c" "${it:-0}" "${ef:-?}" "${eb:-?}"
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
echo "  2x2 gallery 행렬 ✅완성(2026-07-30): 1L|1L 0.3567 · 2L|1L 0.1495 · 1L|2L 0.3802 · 2L|2L 0.1473 eV"
echo "    → 209 meV 는 거의 전부 VGCF 쪽: VGCF만 2층 -207.2 meV(98.9%) · h-BN만 2층 +23.5 meV(악화)"
echo "  ✅ 기전 판정 완료(2026-07-30) = **CONFINEMENT**"
echo "    표면 대조군 Li_on_graphene 1L 0.2730 → 2L 0.2848 = +11.9 meV (허용오차 ~20 meV 안 → 0)"
echo "    갤러리 같은 변화 1L|1L 0.3567 → 2L|1L 0.1495 = -207.2 meV · 17배 차이, 부호 반대"
echo "    ⚠ +11.9 meV 를 '약간 악화'로 인용 금지 — 0 과 구별 안 됨. 3L 포화 미확인이라"
echo "      0.147 eV 는 '수렴값'이 아니라 **2L 값**으로만."
echo "    정리: kb/results/vgcf_hbn_gallery_mechanism_2026_07_30.md"
