# 재료 · 접촉 (실제 ps45 7:3 계열 덱과 같은 값 · 같은 모델)
neighbor        0.0005 bin
neigh_modify    delay 0 check yes
fix m1 all property/global youngsModulus peratomtype 1.4e8 1.4e8 0.135e7
fix m2 all property/global poissonsRatio peratomtype 0.25 0.25 0.30
fix m3 all property/global coefficientRestitution peratomtypepair 3 0.3 0.3 0.3 0.3 0.3 0.3 0.3 0.3 0.3
fix m4 all property/global coefficientFriction peratomtypepair 3 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5
fix m5 all property/global coefficientRollingFriction peratomtypepair 3 0.2 0.2 0.1 0.2 0.2 0.1 0.1 0.1 0.1
fix m6 all property/global coefficientMaxElasticStiffness peratomtypepair 3 1.5 1.5 3.0 1.5 1.5 3.0 3.0 3.0 5.0
fix m7 all property/global coefficientAdhesionStiffness peratomtypepair 3 1.0e5 1.0e5 2.0e5 1.0e5 1.0e5 2.0e5 2.0e5 2.0e5 1.0e6
fix m8 all property/global coefficientPlasticityDepth peratomtypepair 3 0.05 0.05 0.01 0.05 0.05 0.01 0.01 0.01 0.005
fix m9 all property/global characteristicVelocity scalar 2.0
pair_style      gran model hooke/hysteresis tangential history rolling_friction cdt
pair_coeff      * *
fix zwall_bot all wall/gran model hooke/hysteresis tangential history rolling_friction cdt primitive type 1 zplane 0.0
