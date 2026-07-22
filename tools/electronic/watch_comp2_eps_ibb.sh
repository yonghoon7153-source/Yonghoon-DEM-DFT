#!/bin/bash
# watch_comp2_eps_ibb.sh — comp2 ε∞ (ph.x epsil) Slurm job 감시 (ibb-master).
#   watch -n 30 'bash ~/comp2_eps/watch_comp2_eps_ibb.sh'
set +H
cd "${WORK:-$HOME/comp2_eps}" 2>/dev/null || true
echo "══ comp2 ε∞ (ph.x epsil · ibb Slurm · PAW)  $(date '+%m-%d %H:%M:%S') ══"
echo "── Slurm ──"
squeue -u "$USER" -o "%.9i %.9P %.4t %.10M %.6D %R" 2>/dev/null | grep -iE "JOBID|comp2_ep" || echo "  (큐에 없음 — 완료/실패)"
O=$(ls -t comp2_eps_*.out 2>/dev/null | head -1); echo "── out: ${O:-없음} ──"
[ -z "$O" ] && exit 0

# [1] SCF
if grep -aq "SCF OK" "$O" 2>/dev/null; then
  echo "  [1] fixed-occ SCF: ✅ DONE"; grep -a "highest occupied" scf_eps.out 2>/dev/null | tail -1 | sed 's/^/      /'
elif [ -f scf_eps.out ]; then
  echo "  [1] SCF 진행: iter $(grep -ac 'iteration #' scf_eps.out)  acc=$(grep -a 'estimated scf accuracy' scf_eps.out | tail -1 | awk '{print $(NF-1),$NF}')"
else echo "  [1] SCF: 대기/입력생성"; fi

# [2] ph.x epsil (핵심 — hang vs run)
if grep -aqi "Dielectric constant in cartesian" eps.out "$O" 2>/dev/null; then
  echo "  [2] ph.x epsil: ★★ DONE — ε∞ 텐서:"
  grep -aiA4 "Dielectric constant in cartesian" eps.out 2>/dev/null | tail -5 | sed 's/^/      /'
elif grep -aqi "TIMEOUT" "$O" 2>/dev/null; then
  echo "  [2] ph.x epsil: ⚠ TIMEOUT(hang) → Route B(epsilon.x)"
elif [ -f eps.out ]; then
  echo "  [2] ph.x epsil 진행 (살아있으면 iter# 증가, 안 움직이면 hang 의심):"
  grep -a "Representation #" eps.out 2>/dev/null | tail -1 | sed 's/^/      /'
  grep -aE "iter #|Self-consistent|Pert" eps.out 2>/dev/null | tail -2 | sed 's/^/      /'
else echo "  [2] ph.x epsil: 대기 (SCF 끝나야)"; fi

echo "── out tail ──"; tail -3 "$O" 2>/dev/null | sed 's/^/    /'
