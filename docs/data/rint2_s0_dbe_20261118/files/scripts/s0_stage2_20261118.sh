cd ~/dem-ca1 && umask 022
. ~/dem-venv/bin/activate && python3 -c 'import sys,numpy,scipy;print(sys.version.split()[0],numpy.__version__,scipy.__version__)'
H1=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['code']['git_head'])" docs/data/rint2_s0_sbe_20261116/files/ca1_s0_sbe_20261116T004809Z_q14final/s0_stage1_kit_SBE_vgcf100.json)
git diff --quiet "$H1" HEAD -- scripts/ca_s0_census.py scripts/carbon_junction.py scripts/ptfe_face_alpha.py scripts/step3_sigma.py \
    scripts/mpm_webapp_payload.py scripts/fibre_segment_raster.py scripts/sr01_stamp_compare.py && echo SAME_VERSION_OK && \
  python3 ~/dem-ca1/scripts/ca_s0_census.py --stage 2 --threshold-commit 29643188524f4fe31f81db5eb252edaa8cbbef7c \
    --plan-path docs/data/rint2_s0_sbe_20261116/files/ca1_s0_sbe_20261116T004809Z_q14final/cjunc_plan.json \
    --r-plan-path docs/data/rint2_r_plan_20261118/ca1_plan.json --r-doc docs/reviews/rint2_seal_20261118/registration_R_sealed.md \
    --kit ~/sdcp/kit_DBE_sdcp1um_vgcf100 --kit ~/sdcp/kit_DBE --out ~/sdcp/ca1_s0_dbe 2>&1 | tee ~/sdcp/ca1_logs/s0_stage2.log; echo "rc=${PIPESTATUS[0]}"
