# Slide figures (paper-grade source for technical report)

This dir is the vm-side landing zone for paper figures we need to embed into slides.
Each subdir mirrors the source paths on v100 container:

- `slide05_dos_pdos/comp1_V0_dos_pdos.png`   <- container:/home/ubuntu/work/runs/comp1_v3/v3_post/k444_props/V0_dos_pdos.png
- `slide05_dos_pdos/modelc_V0_dos_pdos.png`  <- container:/home/ubuntu/work/runs/modelC_v3/V0_dos_pdos.png
- `slide06_bvse_5x5x5/comp1/V0_BVSE_iso_min030.png`  <- container:/home/ubuntu/work/runs/bvse_cubic_5x5x5/comp1_5x5x5/V0_BVSE_iso_min030.png
- `slide06_bvse_5x5x5/comp1/V0_BVSE_slice_z_mid_noatoms.png`  <- same dir
- `slide06_bvse_5x5x5/modelc/V0_BVSE_iso_min030.png`  <- container:/home/ubuntu/work/runs/bvse_cubic_5x5x5/modelc_5x5x5_exact/V0_BVSE_iso_min030.png
- `slide06_bvse_5x5x5/modelc/V0_BVSE_slice_z_mid_noatoms.png`  <- same dir

Provenance and parameters are recorded in:
- DOS/PDOS: `db/compositions/modelc_v3.json -> v3_postprocess_pipeline_v2_8.8f_dos_pdos`
- BVSE 5x5x5: `db/compositions/modelc_v3.json -> v3_postprocess_pipeline_v2_8.bvse_5x5x5_paired_2026_06_03`
