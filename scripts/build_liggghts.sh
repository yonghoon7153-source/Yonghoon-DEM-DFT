#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Build LIGGGHTS-PUBLIC (the DEM engine) — required for dem_scripts/*.liggghts.
# NOT vanilla LAMMPS: the inputs use `soft_particles yes` + LIGGGHTS granular
# models (fix property/global youngsModulus, pair gran), which are LIGGGHTS-only.
#
#     conda activate uma
#     bash scripts/build_liggghts.sh          # clones + builds into ./LIGGGHTS-PUBLIC
#
# Toolchain (install first if missing — via conda-forge is the most portable):
#     conda install -c conda-forge gxx_linux-64 gcc_linux-64 openmpi make
#   (or system: sudo apt install build-essential openmpi-bin libopenmpi-dev)
# ─────────────────────────────────────────────────────────────────────────────
set -uo pipefail
DIR="${1:-$PWD/LIGGGHTS-PUBLIC}"
JOBS="$(nproc 2>/dev/null || echo 4)"

command -v mpicxx >/dev/null 2>&1 || echo "⚠ mpicxx not found — install openmpi (conda install -c conda-forge openmpi gxx) then re-run"
command -v make   >/dev/null 2>&1 || { echo "✗ make not found — install build tools first"; exit 1; }

if [ ! -d "$DIR" ]; then
  echo "[liggghts] cloning → $DIR"
  git clone --depth 1 https://github.com/CFDEMproject/LIGGGHTS-PUBLIC.git "$DIR" || {
    echo "✗ clone failed (network?). Manual: git clone https://github.com/CFDEMproject/LIGGGHTS-PUBLIC.git"; exit 1; }
fi

cd "$DIR/src"
echo "[liggghts] building (make auto, -j$JOBS) …"
# 'make auto' autodetects MPI/serial and produces lmp_auto.  If it fails, try:
#   make -j$JOBS mpi     (→ lmp_mpi)   or   make -j$JOBS serial   (→ lmp_serial)
if make -j"$JOBS" auto; then BIN="$DIR/src/lmp_auto"
elif make -j"$JOBS" mpi;  then BIN="$DIR/src/lmp_mpi"
else echo "✗ build failed — see docs/server_setup.md §2 (common: newer g++ needs a small patch; try 'make serial')"; exit 1; fi

echo "[liggghts] ✓ built: $BIN"
echo "[liggghts] test a case (from the repo root):"
echo "    mpirun -np $JOBS \"$BIN\" -in dem_scripts/case09_E15x.liggghts   # writes atoms.csv/contacts.csv"
echo "[liggghts] add to PATH:  export LIGGGHTS_BIN=\"$BIN\"   (or ln -s \"$BIN\" ~/bin/liggghts)"
