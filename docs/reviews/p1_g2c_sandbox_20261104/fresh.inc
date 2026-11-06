include head.inc
region reg_box block 0.0 0.012 0.0 0.012 -0.001 0.04 units box
create_box      3 reg_box
timestep        1.0e-6
include mat.inc
compute cpl all pair/gran/local pos id force force_normal force_tangential torque history contactArea delta contactPoint
fix pts1 all particletemplate/sphere 20000003 atom_type 1 density constant 4800 radius constant 2.0e-3
fix pts2 all particletemplate/sphere 21300029 atom_type 2 density constant 4800 radius constant 1.0e-3
fix pts3 all particletemplate/sphere 22600001 atom_type 3 density constant 2000 radius constant 0.5e-3
fix pdd_mix all particledistribution/discrete 23900027 3 pts1 0.4 pts2 0.3 pts3 0.3
region reg_mix block 0.0 0.012 0.0 0.012 0.002 0.035 units box
fix ins_mix all insert/pack seed 25200011 distributiontemplate pdd_mix maxattempt 10000 insert_every once overlapcheck yes all_in no region reg_mix volumefraction_region 0.25
run 1
unfix ins_mix
variable n_ins equal count(all)
print "INSERTED ${n_ins}"
thermo_style    custom step atoms ke cpu
thermo          5000
fix integr all nve/sphere
fix gravi all gravity 98.1 vector 0.0 0.0 -1.0
