# MPFEM step 1 (MOOSE) runner - DEVELOPMENT DATA.   usage: bash run_step1.sh
# meshes m13 m26 -> SMOKE (m13, 12 steps, stops here on any error) -> full m13 -> full m26
# -> check_step1.py (C P1 P2 P4 fixed before the run, P6 report only).  No network use.
# Each call writes a NEW folder run_<date>_<fix>_XXXX next to this script; nothing is rerun.
# Manual fix switches (pre-registered order of step1 doc K-3, one at a time, never automatic):
#   FIX=dt_half  (1) half plate step: dt 0.5, 814 steps, same plate speed
#   FIX=no_vlc   (3) volumetric locking correction off (plain QUAD4)
#   (2) contact formulation change = a new input from the session, not a switch here
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
FIX=${FIX:-none}
END=407
case "$FIX" in
  none)    DT=1;   OVR="" ;;
  dt_half) DT=0.5; OVR="Executioner/dt=0.5 Executioner/dtmin=0.5" ;;
  no_vlc)  DT=1;   OVR="GlobalParams/volumetric_locking_correction=false" ;;
  *) echo "STOP: unknown FIX=$FIX (none | dt_half | no_vlc)"; exit 2 ;;
esac
CONDA_SH="$HOME/miniforge/etc/profile.d/conda.sh"
[ -f "$CONDA_SH" ] || { echo "STOP: $CONDA_SH not found (MOOSE install of 11-25)"; exit 1; }
. "$CONDA_SH"
conda activate moose || { echo "STOP: conda activate moose failed"; exit 1; }
EXE=""
for c in moose-opt moose combined-opt; do
  if command -v "$c" >/dev/null 2>&1; then EXE=$(command -v "$c"); break; fi
done
[ -n "$EXE" ] || { echo "STOP: no MOOSE executable (moose-opt moose combined-opt)"; exit 1; }
PY=$(command -v python3) || { echo "STOP: python3 not found"; exit 1; }
export OMP_NUM_THREADS=1
R=$(mktemp -d "$HERE/run_$(date +%Y%m%d_%H%M%S)_${FIX}_XXXX") || { echo "STOP: run folder"; exit 1; }
mkdir "$R/inputs" "$R/mesh"
for f in step1_disk.i make_disk_msh.py check_step1.py run_step1.sh; do cp "$HERE/$f" "$R/inputs/"; done
(cd "$R/inputs" && sha256sum step1_disk.i make_disk_msh.py check_step1.py run_step1.sh > SHA256SUMS)
{ echo "fix=$FIX dt=$DT end_time=$END"; echo "exe=$EXE"; "$EXE" --version 2>&1 | head -n 5
  "$PY" --version 2>&1; uname -sr; } > "$R/run_info.txt"
echo "== run folder: $R"
echo "== 1 meshes"
"$PY" "$HERE/make_disk_msh.py" --ns 8 --nr 2 --out "$R/mesh/disk_m13" || { echo "STOP: mesher m13"; exit 1; }
"$PY" "$HERE/make_disk_msh.py" --ns 16 --nr 4 --out "$R/mesh/disk_m26" || { echo "STOP: mesher m26"; exit 1; }

run_case() {  # name mesh timeout_s [extra overrides]
  local name=$1 mesh=$2 to=$3 d t0
  shift 3
  d="$R/$name"
  mkdir "$d"
  cp "$HERE/step1_disk.i" "$d/"
  cp "$R/mesh/$mesh.msh" "$d/disk.msh"
  cp "$R/mesh/$mesh.mesh.json" "$d/disk.mesh.json"
  t0=$(date +%s)
  (cd "$d" && timeout "$to" "$EXE" -i step1_disk.i $OVR "$@" > run.log 2>&1; echo $? > rc.txt)
  echo "   $name rc=$(cat "$d/rc.txt") wall_s=$(( $(date +%s) - t0 ))"
}
tail_log() {
  echo "--- error lines: $1/run.log"
  grep -n -i -E '\*\*\*|error|did not converge|cannot continue' "$1/run.log" | head -n 30
  echo "--- last 40 lines"
  tail -n 40 "$1/run.log"
}

echo "== 2 smoke m13 (12 steps; first contact at step 7)"
run_case smoke_m13 disk_m13 900 Executioner/end_time=12
if ! "$PY" "$HERE/check_step1.py" smoke --case "$R/smoke_m13" --end-time 12 --dt "$DT"; then
  echo "SMOKE FAIL - full runs not started.  Send this whole output to the session."
  tail_log "$R/smoke_m13"
  exit 1
fi
echo "== 3 full m13 (end time $END)"
run_case m13 disk_m13 14400
echo "== 4 full m26 (end time $END)"
run_case m26 disk_m26 14400
echo "== 5 check"
"$PY" "$HERE/check_step1.py" full --case m13="$R/m13" --case m26="$R/m26" --dt "$DT" \
  --end-time "$END" --out "$R/check_step1.json"
rc=$?
for n in m13 m26; do [ "$(cat "$R/$n/rc.txt")" = 0 ] || tail_log "$R/$n"; done
tar czf "$R/result_small.tgz" -C "$R" --exclude='*.e' --exclude='*.msh' \
  check_step1.json run_info.txt inputs mesh smoke_m13 m13 m26 2>/dev/null
echo "== outputs: $R"
echo "   check_step1.json run_info.txt inputs/SHA256SUMS mesh/  smoke_m13/ m13/ m26/: out.csv out.e run.log rc.txt"
echo "   to send back: $R/result_small.tgz (csv, logs, json; no .e, no .msh)"
exit $rc
