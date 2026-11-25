# Source before running the GPU QE build (qe-7.4.1-gpu) on gabia (kserver116-27).
# Run `conda deactivate` FIRST so conda's GNU libgomp does not shadow NVHPC's.
#
# Why each line (the 4 bugs we hit, in order):
#   1. pseudo names must be dotted (P.pbe-n-rrkjus_psl.1.0.0.UPF ...)  -> fixed in scf.in
#   2. GPU build is linked to NVHPC HPC-X OpenMPI -> must launch with ITS mpirun
#   3. OpenMPI can't find its runtime data ("help file" at /proj/nv/...) -> set OPAL_PREFIX
#   4. "libgomp: TODO" = GNU libgomp loaded instead of NVHPC's -> put compilers/lib FIRST
NV=/data/apps/nvhpc/Linux_x86_64/24.11
export OPAL_PREFIX="$NV/comm_libs/12.6/hpcx/hpcx-2.20/ompi"
export LD_LIBRARY_PATH="$NV/compilers/lib:$NV/cuda/lib64:$NV/math_libs/lib64:$OPAL_PREFIX/lib"
export OMP_NUM_THREADS=1
export QEGPU=/data/apps/qe-7.4.1-gpu/bin
export MPIRUN="$OPAL_PREFIX/bin/mpirun"
echo "GPU QE env ready (did you 'conda deactivate'?). Example:"
echo "  \$MPIRUN -np 1 \$QEGPU/pw.x -in scf.in > scf.out 2>&1"
