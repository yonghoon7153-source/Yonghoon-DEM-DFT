#!/bin/bash
# watch_comp2_eps_ibb.sh — comp2 ε∞ (ph.x epsil) Slurm job 상세 감시 (ibb-master).
#   watch -n 30 'bash ~/comp2_eps/watch_comp2_eps_ibb.sh'
# SCF(iter로 skip 감지) · out_eps 존재(check_tempdir 예방) · ph.x(phonon 오염/E-field DFPT/ε∞).
set +H
cd "${WORK:-$HOME/comp2_eps}" 2>/dev/null || true
echo "══ comp2 ε∞ (ph.x epsil · ibb · PAW)  $(date '+%m-%d %H:%M:%S') ══"
echo "── Slurm ──"
squeue -u "$USER" -o "%.9i %.4t %.10M %.6D %R" 2>/dev/null | grep -iE "JOBID|comp2_ep" || echo "  (큐 없음 — 완료/실패; sacct 확인)"
O=$(ls -t comp2_eps_*.out 2>/dev/null | head -1); echo "── 러너로그: ${O:-없음} ──"
[ -z "$O" ] && exit 0

# ── MPI 건강 (starting charge 1~2 = 하나의 병렬 / 많으면 독립복사) ──
if [ -f scf_eps.out ]; then
  sc=$(grep -ac "starting charge" scf_eps.out 2>/dev/null)
  if [ "${sc:-0}" -ge 1 ] 2>/dev/null; then
    [ "$sc" -le 2 ] && echo "  MPI: starting charge ×${sc} ✅ (하나의 병렬 SCF)" \
                    || echo "  MPI: starting charge ×${sc} ⚠ (독립복사 — MPI 안 붙음)"
  fi
fi

# ── [1] fixed-occ SCF (iter 수로 '진짜 돌았나' 판정 — skip이면 out_eps 없어 ph.x 죽음) ──
if [ -f scf_eps.out ]; then
  ni=$(grep -ac "iteration #" scf_eps.out)
  if grep -aq "JOB DONE" scf_eps.out 2>/dev/null; then
    ho=$(grep -a "highest occupied" scf_eps.out 2>/dev/null | tail -1 | awk '{print $NF}')
    if [ "${ni:-0}" -le 1 ]; then
      echo "  [1] SCF ⚠ JOB DONE인데 iter=${ni} → skip 의심 (out_eps 재생성 안됐을 수)"
    else
      echo "  [1] SCF ✅ DONE (iter ${ni}, HOMO ${ho:-?} eV)"
    fi
  else
    ac=$(grep -a "scf accuracy" scf_eps.out 2>/dev/null | tail -1 | awk '{print $(NF-1),$NF}')
    echo "  [1] SCF 진행: iter ${ni}  acc=${ac:-—}"
  fi
else echo "  [1] SCF: 대기/입력생성"; fi

# ── out_eps 존재 (ph.x check_tempdir 예방; 이게 없으면 ph.x 즉사) ──
if [ -d out_eps ]; then
  echo "  out_eps ✅ ($([ -d out_eps/_ph0 ] && echo _ph0有 || echo _ph0待) / $([ -d out_eps/comp2.save ] && echo save有 || echo save無))"
else echo "  out_eps ✗ 없음 → ph.x check_tempdir 실패 위험 (SCF skip 확인!)"; fi

# ── [2] ph.x epsil (핵심) ──
if [ -f eps.out ]; then
  if grep -aqi "check_tempdir" eps.out 2>/dev/null; then
    echo "  [2] ph.x ✗ check_tempdir 실패 — out_eps 없음. 고치기: rm scf_eps.out out_eps → 재제출(SCF 재실행)"
  elif grep -aqi "Dielectric constant in cartesian" eps.out 2>/dev/null; then
    echo "  [2] ph.x ★★ ε∞ DONE — 텐서:"
    grep -aiA4 "Dielectric constant in cartesian" eps.out | tail -5 | sed 's/^/      /'
  elif grep -aq "TIMEOUT(hang)" "$O" 2>/dev/null; then
    echo "  [2] ph.x ⚠ TIMEOUT(hang) → Route B(epsilon.x)"
  else
    rp=$(grep -ac "Representation.*To be done" eps.out 2>/dev/null)
    if [ "${rp:-0}" -gt 0 ]; then
      echo "  [2] ph.x ⚠ phonon ${rp}개 잡음 (trans 오염 — outdir clean 필요)"
    else
      echo "  [2] ph.x: E-field 모드 ✅ (phonon 0)"
    fi
    ei=$(grep -ac "iter #" eps.out 2>/dev/null); echo "      E-field DFPT iter 누적 = ${ei} (늘면 살아있음)"
    grep -aE "Electric Fields Calc|iter #|total cpu time" eps.out 2>/dev/null | tail -2 | sed 's/^/      /'
  fi
else echo "  [2] ph.x epsil: 대기 (SCF 끝나야)"; fi

echo "── 러너로그 tail ──"; tail -2 "$O" 2>/dev/null | sed 's/^/    /'
