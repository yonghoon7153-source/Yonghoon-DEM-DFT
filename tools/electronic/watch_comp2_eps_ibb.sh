#!/bin/bash
# watch_comp2_eps_ibb.sh — comp2 ε∞ (ph.x epsil) 초상세 (ibb).
#   Slurm → MPI → [1]SCF(iter/save) → [2]ph.x(setup 나열 vs E-field DFPT) → iter당 시간·수렴 예상 → ε∞.
#   watch -n 30 'bash ~/comp2_eps/watch_comp2_eps_ibb.sh'
set +H
cd "${WORK:-$HOME/comp2_eps}" 2>/dev/null || true
echo "══ comp2 ε∞ (ph.x epsil · ibb · PAW · timeout 120h/5일)  $(date '+%m-%d %H:%M:%S') ══"
sq=$(squeue -u "$USER" -h -o "%.9i %.2t %.10M %R" 2>/dev/null | grep -iE "node0|R |PD ")
echo "── Slurm: ${sq:-없음(sacct 확인)} ──"
O=$(ls -t comp2_eps_*.out 2>/dev/null | head -1); echo "── 러너로그: ${O:-없음} ──"
[ -z "$O" ] && exit 0

# ── MPI 건강 ──
if [ -f scf_eps.out ]; then
  sc=$(grep -ac "starting charge" scf_eps.out 2>/dev/null)
  [ "${sc:-0}" -ge 1 ] && { [ "$sc" -le 2 ] && echo "  MPI ✅ starting charge ×${sc}" || echo "  MPI ⚠ ×${sc} (독립복사 — MPI 안 붙음)"; }
fi

# ── [1] SCF (iter로 skip 판정) ──
if [ -f scf_eps.out ]; then
  ni=$(grep -ac "iteration #" scf_eps.out)
  if grep -aq "JOB DONE" scf_eps.out 2>/dev/null; then
    ho=$(grep -a "highest occupied" scf_eps.out 2>/dev/null | tail -1 | awk '{print $NF}')
    [ "${ni:-0}" -le 1 ] && echo "  [1] SCF ⚠ JOB DONE인데 iter=${ni} (skip 의심 → out_eps 확인)" \
                         || echo "  [1] SCF ✅ DONE (iter ${ni}, HOMO ${ho} eV = insulator)"
  else
    ac=$(grep -a "estimated scf accuracy" scf_eps.out 2>/dev/null | tail -1 | awk '{print $(NF-1),$NF}')
    echo "  [1] SCF 진행: iter ${ni}  acc ${ac:-—}"
  fi
else echo "  [1] SCF: 대기/입력생성"; fi
[ -d out_eps ] && echo "  out_eps ✅ ($([ -d out_eps/comp2.save ]&&echo save有||echo save無) / $([ -d out_eps/_ph0 ]&&echo _ph0有||echo _ph0待))" \
               || echo "  out_eps ✗ 없음 → ph.x check_tempdir 위험"

# ── [2] ph.x epsil — 단계별 + iter 속도/수렴 예상 ──
if [ -f eps.out ]; then
  if grep -aqi "Dielectric constant in cartesian" eps.out; then
    echo "  [2] ph.x ★★★ ε∞ 완료 — 텐서:"
    grep -aiA5 "Dielectric constant in cartesian" eps.out | tail -6 | sed 's/^/      /'
  elif grep -aqi "check_tempdir" eps.out; then
    echo "  [2] ph.x ✗ check_tempdir 실패 (out_eps 없음. rm scf_eps.out out_eps → 재제출)"
  else
    rp=$(grep -ac "Representation.*To be done" eps.out 2>/dev/null)
    ef=$(grep -ac "Electric Fields Calculation" eps.out 2>/dev/null)
    ni=$(grep -ac "iter #" eps.out 2>/dev/null)
    if [ "${ef:-0}" -eq 0 ]; then
      echo "  [2] ph.x: representation 나열 중 (setup) — phonon ${rp}개는 trans=.false.여도 정상 나열(오염 아님)"
      echo "      → Electric Fields 진입 대기 (52원자 PAW·ecutrho 560이라 setup 무거움)"
    else
      echo "  [2] ph.x: ★ E-field DFPT 진행 중 (Electric Fields 진입, representation ${rp}개 지남)"
      echo "      DFPT iter 누적 = ${ni}"
      grep -a "iter #" eps.out 2>/dev/null | tail -2 | sed 's/^/      /'
      # iter당 시간 + 수렴 예상 (연속 iter의 total cpu 차)
      grep -a "iter #" eps.out 2>/dev/null | awk -F'total cpu time :' 'NF>1{split($2,a," ");c=a[1]+0; if(p!="")d=c-p; p=c; n++}
        END{ if(n>=2) printf "      → 최근 iter당 ~%.0f분 (누적 %.1fh, %d iter 완료). 수렴 ~15 iter 가정시 남은 ~%.1fh\n", d/60, c/3600, n, (n<15?(15-n)*d/3600:0);
             else if(n==1) printf "      → iter#1 누적 %.1fh (대부분 setup; ★iter#2 속도가 수렴시간의 관건)\n", c/3600 }'
    fi
  fi
else echo "  [2] ph.x epsil: SCF 끝나야 시작"; fi

st=$(grep -aoE "\[[0-9:]+\] ph.x epsil" "$O" 2>/dev/null | tail -1)
echo "── ph.x 시작 ${st:-?} · timeout 120h → walltime 5일 안에 수렴 목표 ──"
echo "── 러너로그 tail ──"; tail -2 "$O" 2>/dev/null | sed 's/^/    /'
