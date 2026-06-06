#!/usr/bin/env python3
"""Generate pure-SE LIGGGHTS inputs for a Heckel pressure series.

Integrity test (E_SE model): run the SAME pure-SE assembly (E_SE=1.35 GPa,
fixed insert seed) to several target pressures.  Compute relative density D
at each P and fit the Heckel equation  ln(1/(1-D)) = K·P + A.
  • Linear with mean-yield-pressure P_y = 1/K ≈ H_LPSCl ≈ 0.85 GPa
    (σ_y ≈ P_y/3 ≈ 0.30 GPa)  → elastic-softened DEM faithfully mimics plasticity.
  • Curved / P_y far off → elastic limit exposed.

Pure SE (no AM) so the soft SE is load-bearing and actually yields — in a
composite the rigid AM (140 GPa) carries the load and masks SE yielding.

Run:  python3 scripts/make_heckel_inputs.py
Out:  heckel/input_SE_heckel_{100,200,300,400}.liggghts
Then run each on WSL (LIGGGHTS), upload final atom_*+mesh_*+contact_* per P,
and analyse with scripts/heckel_analysis.py.
"""
import os

PRESSURES_MPA = [100, 200, 300, 400]
SEED = 78049                      # SAME across all P → paired snapshots
E_SE_SCALED = '0.135e7'          # 1.35 GPa (×1000 scale)

TEMPLATE = r"""# ============================================================
# SE_heckel_{TAG}: SE ONLY, Heckel point at {PMPA} MPa, E_SE=1.35 GPa
# 1-type: SE(0.5um) only.  RVE=50x50um, Scale: r*1000, E*0.001, P*0.001
# Same insert seed across the series -> paired compaction snapshots.
# ============================================================
atom_style      granular
atom_modify     map array sort 0 0
boundary        p p f
newton          off
soft_particles  yes
communicate     single vel yes
units           si

variable target_press equal {PSCALED}
variable r_SE    equal 0.5e-3
variable dt      equal 1.0e-6
variable plate_margin equal 0.003
timestep        ${{dt}}

region reg_box block 0.0 0.05 0.0 0.05 -0.01 1.0 units box
create_box      1 reg_box
neighbor        0.002 bin
neigh_modify    delay 0 check yes

fix m1 all property/global youngsModulus peratomtype {ESE}
fix m2 all property/global poissonsRatio peratomtype 0.30
fix m3 all property/global coefficientRestitution peratomtypepair 1 0.3
fix m4 all property/global coefficientFriction peratomtypepair 1 0.5
fix m5 all property/global coefficientRollingFriction peratomtypepair 1 0.1
fix m6 all property/global coefficientMaxElasticStiffness peratomtypepair 1 5.0
fix m7 all property/global coefficientAdhesionStiffness peratomtypepair 1 1.0e6
fix m8 all property/global coefficientPlasticityDepth peratomtypepair 1 0.005
fix m9 all property/global characteristicVelocity scalar 2.0

pair_style      gran model hooke/hysteresis tangential history rolling_friction cdt
pair_coeff      * *

compute strs all stress/atom
compute ke   all ke/atom
compute cpl all pair/gran/local pos id force force_normal force_tangential torque contactArea delta contactPoint

fix zwall_bot all wall/gran model hooke/hysteresis tangential history rolling_friction cdt primitive type 1 zplane 0.0

fix pts1 all particletemplate/sphere 32452843 atom_type 1 density constant 2000 radius constant ${{r_SE}}
fix pdd_mix all particledistribution/discrete 49979687 1 pts1 1.0

region reg_mix block 0.0 0.05 0.0 0.05 0.005 0.035 units box
print "====== INSERTING PARTICLES (SE_heckel_{TAG}, seed={SEED}) ======"
fix ins_mix all insert/pack seed {SEED} distributiontemplate pdd_mix &
    maxattempt 15000 insert_every once overlapcheck yes all_in no &
    vel constant 0.0 0.0 -0.5 &
    region reg_mix &
    volumefraction_region 0.281
run 1
unfix ins_mix

shell mkdir post_SE_heckel_{TAG}
thermo_style    custom step atoms ke cpu
thermo          1000

print "====== PHASE 1: SETTLING ======"
fix integr all nve/sphere
fix gravi all gravity 98.1 vector 0.0 0.0 -1.0
fix damp all viscous 1.0e-5
compute zmax all reduce max z
shell mkdir restart_SE_heckel_{TAG}
restart 50000 restart_SE_heckel_{TAG}/restart_settling_*.bin
run 200000

write_restart restart_SE_heckel_{TAG}/restart_after_settling.bin
thermo_style    custom step atoms c_zmax
thermo          1
run 1
variable z_max equal c_zmax
variable plate_z equal ${{z_max}}+${{r_SE}}+${{plate_margin}}
print "====== PLATE HEIGHT: ${{plate_z}} ======"

print "solid plate" file plate_SE_heckel_{TAG}.stl screen no
print "facet normal 0 0 -1" append plate_SE_heckel_{TAG}.stl screen no
print "outer loop" append plate_SE_heckel_{TAG}.stl screen no
print "vertex 0.0 0.0 ${{plate_z}}" append plate_SE_heckel_{TAG}.stl screen no
print "vertex 0.05 0.05 ${{plate_z}}" append plate_SE_heckel_{TAG}.stl screen no
print "vertex 0.05 0.0 ${{plate_z}}" append plate_SE_heckel_{TAG}.stl screen no
print "endloop" append plate_SE_heckel_{TAG}.stl screen no
print "endfacet" append plate_SE_heckel_{TAG}.stl screen no
print "facet normal 0 0 -1" append plate_SE_heckel_{TAG}.stl screen no
print "outer loop" append plate_SE_heckel_{TAG}.stl screen no
print "vertex 0.0 0.0 ${{plate_z}}" append plate_SE_heckel_{TAG}.stl screen no
print "vertex 0.0 0.05 ${{plate_z}}" append plate_SE_heckel_{TAG}.stl screen no
print "vertex 0.05 0.05 ${{plate_z}}" append plate_SE_heckel_{TAG}.stl screen no
print "endloop" append plate_SE_heckel_{TAG}.stl screen no
print "endfacet" append plate_SE_heckel_{TAG}.stl screen no
print "endsolid plate" append plate_SE_heckel_{TAG}.stl screen no

fix top_mesh all mesh/surface/stress file plate_SE_heckel_{TAG}.stl type 1 scale 1.0 reference_point 0 0 0
fix zwall_top all wall/gran model hooke/hysteresis tangential history rolling_friction cdt mesh n_meshes 1 meshes top_mesh
dump dmp_mesh all mesh/stl 5000 post_SE_heckel_{TAG}/mesh_*.stl top_mesh

print "====== PHASE 2: STABILIZE ======"
fix gravi all gravity 9.81 vector 0.0 0.0 -1.0
unfix damp
fix damp all viscous 0.5
variable pressMPa equal abs(f_top_mesh[3])/0.0025/1000000
thermo_style    custom step atoms ke cpu v_pressMPa
thermo 1000
run 200000

print "====== PHASE 3: COMPRESSION to {PMPA} MPa ======"
dump dmp_atom all custom 5000 post_SE_heckel_{TAG}/atom_*.liggghts id type x y z radius vx vy vz c_strs[1] c_strs[2] c_strs[3] c_ke
fix_modify      zwall_top energy yes
variable press_speed equal 0.01
fix move_press all move/mesh mesh top_mesh linear 0.0 0.0 -${{press_speed}}
restart 50000 restart_SE_heckel_{TAG}/restart_compress_*.bin

label loop_press
    run 5000
    variable current_press equal "abs(f_top_mesh[3]) / 0.0025 / 1000000"
    print "Current Pressure: ${{current_press}} MPa (Target: ${{target_press}})"
    if "${{current_press}} < ${{target_press}}" then "jump SELF loop_press"

unfix move_press

print "====== PHASE 4: RELAXATION ======"
unfix damp
fix damp all viscous 1.0e-5
dump dmp_contact all local 10000 post_SE_heckel_{TAG}/contact_*.liggghts &
    c_cpl[1] c_cpl[2] c_cpl[3] c_cpl[4] c_cpl[5] c_cpl[6] c_cpl[7] c_cpl[8] &
    c_cpl[9] c_cpl[10] c_cpl[11] c_cpl[12] c_cpl[13] c_cpl[14] c_cpl[15] c_cpl[16] &
    c_cpl[17] c_cpl[18] c_cpl[19] c_cpl[20] c_cpl[21] c_cpl[22] c_cpl[23] c_cpl[24] &
    c_cpl[25] c_cpl[26]
run 100000
print "====== SE_heckel_{TAG} ({PMPA} MPa) Finished! ======"
"""


def main():
    os.makedirs('heckel', exist_ok=True)
    for p in PRESSURES_MPA:
        tag = str(p)
        body = (TEMPLATE
                .replace('{TAG}', tag)
                .replace('{PMPA}', str(p))
                .replace('{PSCALED}', f'{p/1000.0:.3f}')
                .replace('{ESE}', E_SE_SCALED)
                .replace('{SEED}', str(SEED)))
        path = f'heckel/input_SE_heckel_{tag}.liggghts'
        with open(path, 'w') as f:
            f.write(body)
        print(f"wrote {path}  (target {p} MPa, seed {SEED}, E_SE 1.35 GPa)")
    print("\nRun each on WSL, then upload final atom_*+mesh_*+contact_* per P.")


if __name__ == '__main__':
    main()
