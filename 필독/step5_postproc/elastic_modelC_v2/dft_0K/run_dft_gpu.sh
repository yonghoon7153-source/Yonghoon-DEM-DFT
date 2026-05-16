#!/bin/bash
source ~/.bashrc
qegpu                           # nvhpc + QE-GPU PATH
cd /data/work/modelc_v2_elastic/1_dft_0K
PWX=$(which pw.x)
echo "Using $PWX (GPU)"
START=$(date +%s)
for d in e?_?; do
    if grep -qa "JOB DONE" $d/pw.out 2>/dev/null; then
        echo "[$d] already DONE"; continue
    fi
    echo "[$d] start $(date '+%H:%M:%S')"
    cd $d
    [ -d tmp ] && rm -rf tmp
    mpirun -np 1 $PWX -in scf.in > pw.out 2>&1
    grep -qa "JOB DONE" pw.out && echo "[$d] DONE" || echo "[$d] FAILED"
    cd ..
done
echo "Total: $(($(date +%s) - START)) sec"
