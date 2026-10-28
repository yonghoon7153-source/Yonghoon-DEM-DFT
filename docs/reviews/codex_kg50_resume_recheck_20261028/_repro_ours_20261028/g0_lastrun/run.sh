#!/bin/bash
set -u
P="$1"; source "$P/funcs_from_ours.sh"
cat > "$P/bad_final.log" <<'L'
Step Atoms KinEng CPU
20001 312506 0.1000 0
21000 312506 0.0955 1
22000 312506 0.0902 2
22001
Loop time of 2 on 56 procs for 1999 steps with 312506 atoms
L
printf 'lastrun (bad_final: 1-token 22001 row) -> '; lastrun "$P/bad_final.log"
printf 'tl 22001 strict -> ['; tl 22001 "$P/bad_final.log"; printf ']\n'
cat > "$P/bad_late.log" <<'L'
Step Atoms KinEng CPU
20001 312506 0.1000 0
21000 312506 0.0955 1
22000 10 1000000 2
22001 312506 0.0902 2.001
Loop time of 2.001 on 56 procs for 2000 steps with 312506 atoms
L
printf 'reg (bad_late) -> '; reg "$P/bad_late.log" | tr '\n' ' '; echo
a='Step=21000 Atoms=312506 KinEng=0.0950'; b=$(tr2 21000 "$P/bad_late.log")
sane "$a" "$b"; echo "G3 first-row sane rc=$? (row 22000 has Atoms=10 KE=1e6 but only F2=21000 compared)"
