#!/bin/bash
cd /data/work/modelc_v2_elastic/1_dft_0K
# QE CPU 빌드 (Xeon 4210R 20-thread)
PWX=$(which pw.x)
echo "Using $PWX"
START=$(date +%s)
for d in e?_?; do
    if grep -qa "JOB DONE" $d/pw.out 2>/dev/null; then
        echo "[$d] already DONE — skip"
        continue
    fi
    echo "[$d] start $(date '+%H:%M:%S')"
    cd $d
    [ -d tmp ] && rm -rf tmp
    mpirun -np 10 $PWX -in scf.in > pw.out 2>&1
    grep -qa "JOB DONE" pw.out && echo "[$d] DONE" || echo "[$d] FAILED"
    cd ..
done
END=$(date +%s)
echo "Total time: $((END-START)) sec"
