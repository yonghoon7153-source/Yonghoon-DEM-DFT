#!/bin/bash
# build_liggghts.sh — 테스트용 LIGGGHTS-PUBLIC (VTK 없이) 빌드 → $LIG_DIR/LIGGGHTS-PUBLIC/src/lmp_novtk  (~10분)
#   bash build_liggghts.sh   그 다음  LMP=<출력된 경로> bash run_tests.sh all
#   검증한 커밋: 3d5c00f20519e6bb6eb6756f51f1ad36564e649d (2024-06) · IBB 의 lmp_mpi 와 같은 LIGGGHTS-PUBLIC 3.8 계열
set -e
KIT=$(cd "$(dirname "$0")" && pwd); LIG_DIR=${LIG_DIR:-$HOME/lig}; mkdir -p "$LIG_DIR"; cd "$LIG_DIR"
command -v mpic++ > /dev/null || { echo "⛔ Open MPI 없음: apt-get install -y libopenmpi-dev openmpi-bin g++ make git"; exit 1; }
[ -d LIGGGHTS-PUBLIC ] || git clone --depth 1 https://github.com/CFDEMproject/LIGGGHTS-PUBLIC.git
cd LIGGGHTS-PUBLIC/src; echo "커밋 $(git rev-parse HEAD 2>/dev/null)"
cp "$KIT/Makefile.novtk" MAKE/Makefile.novtk
make -j"$(nproc)" novtk > make.log 2>&1 || { tail -30 make.log; exit 1; }
ls -la lmp_novtk; echo "LMP=$PWD/lmp_novtk"
