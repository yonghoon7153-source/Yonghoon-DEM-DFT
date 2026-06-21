#!/bin/bash
set -e
# ph.x exists in the CPU build; the GPU build (qe-7.4.1-gpu) crashes 'libgomp: TODO'.
# Use the CPU build. Override QE_BIN / NP / RUN as needed.
QE_BIN="${QE_BIN:-/data/apps/qe-7.4.1-cpu/bin}"
NP="${NP:-8}"
RUN="${RUN:-mpirun -np $NP}"        # if mpirun PMIx-segfaults, run: RUN='' NP=1 OMP_NUM_THREADS=8 bash run_all.sh
export OMP_NUM_THREADS="${OMP_NUM_THREADS:-1}"
PW="$RUN $QE_BIN/pw.x"; PP="$RUN $QE_BIN/pp.x"; PH="$RUN $QE_BIN/ph.x"
echo "QE_BIN=$QE_BIN  RUN='$RUN'  OMP=$OMP_NUM_THREADS"
echo '== SCF =='        ; $PW -in scf.in        > scf.out
grep -q 'convergence has been achieved' scf.out || { echo 'SCF FAILED — see scf.out'; tail -20 scf.out; exit 1; }
echo '== ph.x eps =='   ; $PH -in ph.in         > ph.out
echo '== rho_scf =='    ; $PP -in pp_rho.in     > pp_rho.out
echo '== atomic SCF ==' ; $PW -in scf_atomic.in > scf_atomic.out
echo '== rho_atomic ==' ; $PP -in pp_atomic.in  > pp_atomic.out
echo 'DONE -> ph.out , comp1_rho_scf.cube , comp1_rho_atomic.cube'
