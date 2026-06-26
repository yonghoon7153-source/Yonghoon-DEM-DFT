#!/bin/bash
# Sweep several pseudization settings for the P 1s half-core-hole PP to get
# past "compute_phi: phi has nodes before r_c". AE part (config/zval) is fixed
# and already converges; only &inputp + the valence card vary.
# Run DETACHED on gabia (survives SSH drops):
#   conda deactivate; conda deactivate; unset LD_LIBRARY_PATH OPAL_PREFIX
#   setsid bash tools/xps/sweep_corehole_pp.sh > /data/work/runs/xps_qe/sweep.log 2>&1 < /dev/null &
set +H
WORK=/data/work/runs/xps_qe
LD1=/data/apps/qe-7.4.1-cpu/bin/ld1.x
cd "$WORK" || { echo "no $WORK"; exit 1; }
pkill -9 -f ld1.x 2>/dev/null; sleep 1

HEAD=" &input
    title='P 1s half-core-hole', zed=15.0, rel=1, config='1s1.5 2s2 2p6 3s2.0 3p3.0 3d-2.0',
    iswitch=3, dft='PBE',
 /"

run () {  # $1 = variant name, $2 = inputp namelist + card (file_pseudopw must be P_ch.UPF)
  local n="$1" body="$2"
  rm -f P_ch.UPF
  printf '%s\n%s\n' "$HEAD" "$body" > P_ch_${n}.in
  echo "================= variant ${n} ================="
  timeout 200 "$LD1" < P_ch_${n}.in > P_ch_${n}.out 2>&1
  if [ -f P_ch.UPF ]; then
    mv P_ch.UPF P_ch_${n}.UPF
    echo "  >>> UPF OK  ($(wc -c < P_ch_${n}.UPF) bytes)  -> P_ch_${n}.UPF"
  else
    echo "  xxx FAIL:"; grep -iE "error in routine" -A2 P_ch_${n}.out | head -4
  fi
}

# v1: NC, smaller rc (most common fix for 'nodes before r_c')
run v1_smallrc " &inputp
   lloc=2, pseudotype=2, zval=5.5, file_pseudopw='P_ch.UPF', author='xps',
 /
3
3S  1  0  2.00  0.00  1.30  1.30
3P  2  1  3.00  0.00  1.40  1.40
3D  3  2 -2.00  0.25  1.30  1.30"

# v2: NC, larger rc (in case rc sits before the outer node)
run v2_largerc " &inputp
   lloc=2, pseudotype=2, zval=5.5, file_pseudopw='P_ch.UPF', author='xps',
 /
3
3S  1  0  2.00  0.00  1.95  1.95
3P  2  1  3.00  0.00  2.05  2.05
3D  3  2 -2.00  0.25  1.95  1.95"

# v3: NC, 3s/3p only (drop 3d virtual), p-channel local
run v3_no3d " &inputp
   lloc=1, pseudotype=2, zval=5.5, file_pseudopw='P_ch.UPF', author='xps',
 /
2
3S  1  0  2.00  0.00  1.60  1.60
3P  2  1  3.00  0.00  1.70  1.70"

# v4: NC, s-channel local
run v4_lloc0 " &inputp
   lloc=0, pseudotype=2, zval=5.5, file_pseudopw='P_ch.UPF', author='xps',
 /
3
3S  1  0  2.00  0.00  1.60  1.60
3P  2  1  3.00  0.00  1.70  1.70
3D  3  2 -2.00  0.25  1.60  1.60"

# v5: ULTRASOFT (most forgiving of nodes); rcutus > rcut
run v5_us " &inputp
   lloc=2, pseudotype=3, zval=5.5, rinner=0.8, file_pseudopw='P_ch.UPF', author='xps',
 /
3
3S  1  0  2.00  0.00  1.40  1.80
3P  2  1  3.00  0.00  1.50  1.90
3D  3  2 -2.00  0.25  1.40  1.80"

echo "================= SUMMARY ================="
ls -la P_ch_*.UPF 2>/dev/null || echo "no variant produced a UPF"
echo "=== SWEEP DONE ==="
