#!/bin/bash
# G2c 샌드박스 팔 A · A2 · B · B2 · C (노트 docs/reviews/p1_g2c_source_check_20261104.md §6) — 사용: LMP=<직렬 lmp> bash run_arms.sh N OUT
N=$1; O=$2; B=${LMP:?LMP = LIGGGHTS 3d5c00f 직렬 실행 파일 경로}
cd "$(dirname "$0")" || exit 9
for a in A A2 B B2 C; do mkdir -p "$O/$a/post" "$O/$a/rst"; done
{ ( cd "$(dirname "$B")" && md5sum "$(basename "$B")" ); md5sum *.inc *.liggghts run_arms.sh compare.py; } > "$O/inputs.md5"
go() { local arm=$1; shift; local t0=$(date +%s); nice -n 19 "$B" -log "$O/$arm/log.txt" "$@" > "$O/$arm/out.txt" 2>&1; echo "$arm rc $? sec $(( $(date +%s) - t0 ))" >> "$O/rc.txt"; }
go A  -in A.liggghts  -var N $N -var NM1 $((N-1)) -var RA $((N+999)) -var RST "$O/A/rst"  -var POST "$O/A/post"
go A2 -in A2.liggghts -var N $N -var NM1 $((N-1)) -var R2 $((N-1))  -var RST "$O/A2/rst" -var POST "$O/A2/post"
go B  -in R.liggghts  -var RFILE "$O/A/rst/restart_$N.bin"  -var POST "$O/B/post"
go B2 -in R.liggghts  -var RFILE "$O/A2/rst/restart_$N.bin" -var POST "$O/B2/post"
go C  -in R.liggghts  -var RFILE "$O/A2/rst/restart_cmd.bin" -var POST "$O/C/post"
cat "$O/rc.txt"
