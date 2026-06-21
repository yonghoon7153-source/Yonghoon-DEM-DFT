#!/bin/bash
set -e
PW="mpirun -np ${NP:-8} pw.x"; PP="mpirun -np ${NP:-8} pp.x"; PH="mpirun -np ${NP:-8} ph.x"
echo '== SCF =='        ; $PW -in scf.in        > scf.out
echo '== ph.x eps =='   ; $PH -in ph.in         > ph.out
echo '== rho_scf =='    ; $PP -in pp_rho.in     > pp_rho.out
echo '== atomic SCF ==' ; $PW -in scf_atomic.in > scf_atomic.out
echo '== rho_atomic ==' ; $PP -in pp_atomic.in  > pp_atomic.out
echo 'DONE -> ph.out , comp1_rho_scf.cube , comp1_rho_atomic.cube'
