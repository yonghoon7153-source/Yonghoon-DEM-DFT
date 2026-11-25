#!/usr/bin/env bash
# watch_pbrefine.sh — SDCP DFT+U binding refine status (image-clean preferred poses).
#   watch -n 60 'bash ~/Yonghoon-DEM-DFT/tools/sdcp/watch_pbrefine.sh'
set +H
OUT=${OUT:-/data/work/runs/sdcp_linio2_binding/phaseB_v7c_refine}
cs=$(awk 'NR==5{printf "%.0f", $3}' "$OUT/slab_cshrink.vasp" 2>/dev/null)
echo "══ SDCP DFT+U refine (doped=sulfonate_down / neutral=chelation, c=${cs:-?} ladder)  $(date '+%m-%d %H:%M:%S') ══"
gpu=$(nvidia-smi --query-gpu=memory.used,memory.free,utilization.gpu --format=csv,noheader,nounits 2>/dev/null | head -1)
cur=""                                   # pw.x runs with a relative 'scf.in' -> detect by latest non-done .out
if pgrep -f "pw\.x" >/dev/null 2>&1; then
  cur=$(for j in complex_doped complex_neutral mol_doped mol_neutral slab; do
          o=$OUT/$j/scf.out
          [ -f "$o" ] && ! grep -aq "JOB DONE" "$o" && echo "$(stat -c %Y "$o" 2>/dev/null) $j"
        done | sort -rn | head -1 | awk '{print $2}')
fi
echo "  실행중: ${cur:-(없음/pw.x대기)}  | GPU ${gpu} (used,free,util%)"

echo "── SCF 상태 (복합체=plateau, maxstep 300) ──"
for j in complex_doped complex_neutral mol_doped mol_neutral slab; do
  o=$OUT/$j/scf.out
  [ -f "$o" ] || { printf "  %-16s · 대기\n" "$j"; continue; }
  if grep -aq "JOB DONE" "$o"; then st="✅done"
  elif grep -aqE "Error in routine|MPI_ABORT" "$o"; then st="💥crash"
  else st="↻run "; fi
  e=$(grep -a '^!' "$o" | tail -1 | awk '{print $(NF-1)}')
  it=$(grep -a "iteration #" "$o" | tail -1 | grep -aoE "# *[0-9]+" | grep -aoE "[0-9]+")
  acc=$(grep -a "estimated scf accuracy" "$o" | tail -1 | awk '{print $(NF-1)}')
  [ "$st" = "💥crash" ] && acc="$(grep -a 'Error in routine' "$o" | head -1 | tr -s ' ')"
  printf "  %-16s %s scf#%-3s E=%s acc=%s\n" "$j" "$st" "${it:-?}" "${e:-?}" "${acc:-?}"
done

LOG=$(dirname "$OUT")/pbrefine.log
if [ -n "$cur" ]; then
  o=$OUT/$cur/scf.out; i=$OUT/$cur/scf.in
  age=$(( $(date +%s) - $(stat -c %Y "$o" 2>/dev/null || date +%s) ))
  nd=$(grep -ao "mixing_ndim *= *[0-9]*" "$i" | grep -o "[0-9]*$")
  kp=$(grep -aA1 "K_POINTS" "$i" | tail -1 | tr -s ' ')
  echo "── $cur 상세 (로그 ${age}s 전 갱신 | mixing_ndim=${nd:-?} | k=${kp:-?}) ──"
  grep -aE "iteration #|total cpu time|estimated scf accuracy" "$o" 2>/dev/null | tail -9 | sed 's/^ */    /'
fi
echo "── ladder 이력 ──"
grep -a "\[ladder\]" "$LOG" 2>/dev/null | tail -4 | sed 's/^/  /'
echo "── VERDICT (slab 상쇄, 복합체2+가스2면 나옴) ──"
python3 - <<PY
import re
Ry=13.605693
def E(p):
    try:
        t=open(f"$OUT/{p}/scf.out").read()
        m=re.findall(r"^!\s+total energy\s+=\s+(-\d+\.\d+)",t,re.M) or re.findall(r"total energy\s+=\s+(-\d+\.\d+)",t)
        return float(m[-1]) if m else None
    except FileNotFoundError: return None
e={k:E(k) for k in ["complex_doped","complex_neutral","mol_doped","mol_neutral","slab"]}
need=["complex_doped","complex_neutral","mol_doped","mol_neutral"]
done=all(e[k] is not None for k in need)
if done:
    d=(e["complex_doped"]-e["mol_doped"]-e["complex_neutral"]+e["mol_neutral"])*Ry
    print(f"  Delta = E_bind(doped,sulf) - E_bind(neutral,chel) = {d:+.3f} eV")
    print(f"  => {'✅ 도핑이 결합 강화 (vertical 약화는 자세강제 편향, DFT 확정)' if d<0 else '도핑이 결합 약화'}")
    if e["slab"] is not None:
        ebd=(e["complex_doped"]-e["slab"]-e["mol_doped"])*Ry; ebn=(e["complex_neutral"]-e["slab"]-e["mol_neutral"])*Ry
        print(f"  절대: doped(sulfonate) {ebd:+.3f} / neutral(chelation) {ebn:+.3f} eV")
else:
    got=[k for k in need if e[k] is not None]
    print(f"  대기 ({len(got)}/4: {','.join(got) or '없음'})")
PY
