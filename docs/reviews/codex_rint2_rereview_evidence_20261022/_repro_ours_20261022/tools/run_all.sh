#!/bin/bash
# Codex 10-22 probes on our platform; REVIEW = copy of the mini bundle + rebuilt source/ (pin 0b3012460).
cd ${SP}/rr_repro
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
unset RINT_REVIEW_SOURCE
L=${SP}/rr_repro/logs
run() { name=$1; shift; s=$(date +%s.%N); nice -n 19 python3 -I -X utf8 -B "$@" > $L/$name.stdout 2> $L/$name.stderr; rc=$?; e=$(date +%s.%N); echo "$name rc=$rc t=$(python3 -c "print(round($e-$s,1))")" >> $L/summary.txt; }
: > $L/summary.txt
run registration ${SP}/rr_repro/rint2_rereview_20261022/registration/probe_registration_current.py
run certificate ${SP}/rr_repro/rint2_rereview_20261022/certificate/probe_certificate.py
run certificate_selected_tests ${SP}/rr_repro/rint2_rereview_20261022/certificate/run_selected_tests.py
run geometry ${SP}/rr_repro/rint2_rereview_20261022/geometry/run_review.py
run provenance ${SP}/rr_tools/run_with_dir.py ${SP}/rr_repro/rint2_rereview_20261022/probes/provenance_probe.py
run s0_integration ${SP}/rr_tools/run_with_dir.py ${SP}/rr_repro/rint2_rereview_20261022/probes/s0_integration_probe.py --fixture-argv
echo DONE >> $L/summary.txt
