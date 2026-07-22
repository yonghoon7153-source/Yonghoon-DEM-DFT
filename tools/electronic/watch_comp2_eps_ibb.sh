#!/bin/bash
# watch_comp2_eps_ibb.sh — comp2 ε∞ (ph.x epsil) Slurm job 상세 감시 (ibb-master).
#   watch -n 30 'bash ~/comp2_eps/watch_comp2_eps_ibb.sh'
set +H
cd "${WORK:-$HOME/comp2_eps}" 2>/dev/null || true
echo "══ comp2 ε∞ (ph.x epsil · ibb · 60c · PAW)  $(date '+%m-%d %H:%M:%S') ══"
echo "── Slurm ──"
squeue -u "$USER" -o "%.9i %.4t %.10M %.6D %R" 2>/dev/null | grep -iE "JOBID|comp2_ep" || echo "  (큐 없음 — 완료/실패; sacct 확인)"
O=$(ls -t comp2_eps_*.out 2>/dev/null | head -1); echo "── out: ${O:-없음} ──"
[ -z "$O" ] && exit 0

# ── MPI 건강 (starting charge: 1~2 = 하나의 병렬 / 많으면 독립복사=MPI 안붙음) ──
if [ -f scf_eps.out ]; then
  sc=$(grep -ac "starting charge" scf_eps.out 2>/dev/null)
  if [ "${sc:-0}" -ge 1 ] 2>/dev/null; then
    [ "$sc" -le 2 ] && echo "  MPI: starting charge ×${sc}  ✅ (하나의 병렬 SCF)" \
                    || echo "  MPI: starting charge ×${sc}  ⚠ (독립복사 — mpirun/MPI 안 붙음)"
  fi
fi

# ── [1] fixed-occ SCF ──
if grep -aq "SCF OK" "$O" 2>/dev/null || grep -aq "JOB DONE" scf_eps.out 2>/dev/null; then
  echo "  [1] SCF: ✅ DONE"; grep -a "highest occupied" scf_eps.out 2>/dev/null | tail -1 | sed 's/^/      /'
elif [ -f scf_eps.out ]; then
  ni=$(grep -ac "iteration #" scf_eps.out); ac=$(grep -a "scf accuracy" scf_eps.out | tail -1 | awk '{print $(NF-1),$NF}')
  echo "  [1] SCF 진행: iter ${ni}  acc=${ac:-—}"
else echo "  [1] SCF: 대기/입력생성"; fi

# ── [2] ph.x epsil (★핵심: hang vs run) ──
if grep -aqi "Dielectric constant in cartesian" eps.out 2>/dev/null; then
  echo "  [2] ph.x epsil: ★★ DONE — ε∞ 텐서:"
  grep -aiA4 "Dielectric constant in cartesian" eps.out | tail -5 | sed 's/^/      /'
elif grep -aqi "TIMEOUT" "$O" 2>/dev/null; then
  echo "  [2] ph.x epsil: ⚠ TIMEOUT(hang) → Route B(epsilon.x)"
elif [ -f eps.out ]; then
  echo "  [2] ph.x epsil 진행 (DFPT iter 증가 = 살아있음, 정체 = hang 의심):"
  grep -aE "Electric Field|Representation #|Self-consistent Calc" eps.out 2>/dev/null | tail -1 | sed 's/^/      단계: /'
  ei=$(grep -ac "iter #" eps.out 2>/dev/null); echo "      DFPT iter 누적 = ${ei}"
  grep -a "iter #" eps.out 2>/dev/null | tail -1 | sed 's/^/      최근: /'
  grep -a "total cpu time" eps.out 2>/dev/null | tail -1 | sed 's/^/      /'
else echo "  [2] ph.x epsil: 대기 (SCF 끝나야)"; fi

echo "── out tail ──"; tail -2 "$O" 2>/dev/null | sed 's/^/    /'
