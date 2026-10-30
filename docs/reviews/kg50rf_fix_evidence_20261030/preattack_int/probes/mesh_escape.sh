#!/bin/bash
# PAI-01 probe — D0.7-kind settling resume deck whose post-checkpoint plate mesh fix reads a file OUTSIDE the work folder.
#   The "plate mesh file name only differs" allowance (registered G6 ② · "그 파일이 작업 폴더에 있을 때") checks
#   os.path.isfile(os.path.join(W, nf)) — an absolute nf ignores W, a ../ nf walks out of it.
#   usage: bash mesh_escape.sh <scratch with d07/ from make_d07_resume.py>
WT=$(cd "$(dirname "$0")/../../../../.." && pwd)
SP=${1:?scratch}
T=$WT/scripts/resume_ckpt.sh
MAIN=$WT/docs/data/kg50_decks_20261027_v3_b50/kg50_d07_b50/input_kg50_d07_b50.liggghts
RES=$SP/d07/d07_tool_r56.liggghts
CK=restart_kg50_d07_b50/restart_settling_20001.bin
B=$SP/mesh_escape; rm -rf "$B"; mkdir -p "$B/W" "$B/elsewhere"
printf 'solid plate\nfacet normal 0 0 -1\nouter loop\nvertex 0 0 0.9\nvertex 0.05 0.05 0.9\nvertex 0.05 0 0.9\nendloop\nendfacet\nendsolid plate\n' > "$B/elsewhere/plate_kg50_d2_b50.stl"
cp "$RES" "$B/W/input_kg50_d07_b50_r56.liggghts"
OLD='fix top_mesh all mesh/surface/stress file plate_kg50_d07_b50.stl type 1'
grep -c "^$OLD" "$RES" | sed 's/^/post-checkpoint plate mesh lines in the resume deck: /'
run() {  # $1 tag · $2 replacement file name
  sed "s#^$OLD#fix top_mesh all mesh/surface/stress file $2 type 1#" "$RES" > "$B/res_$1.liggghts"
  echo "=== $1 : file $2"
  diff <(grep -n top_mesh "$RES") <(grep -n top_mesh "$B/res_$1.liggghts") | sed 's/^/    diff /'
  bash "$T" -C "$MAIN" "$B/res_$1.liggghts" "$CK" 20001 "$B/W" | grep -E "판 메시|재개 덱 정적 대조:|✗"
  echo "    rc=${PIPESTATUS[0]}"
}
run abs "$B/elsewhere/plate_kg50_d2_b50.stl"
run dotdot "../elsewhere/plate_kg50_d2_b50.stl"
run inW_nonstl "input_kg50_d07_b50_r56.liggghts"
run missing "plate_nonexistent.stl"
