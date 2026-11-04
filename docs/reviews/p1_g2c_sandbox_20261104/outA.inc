restart ${N} ${RST}/restart_*.bin
dump dc1 all local ${NM1} ${POST}/cpre_*.txt c_cpl[1] c_cpl[2] c_cpl[3] c_cpl[4] c_cpl[5] c_cpl[6] c_cpl[7] c_cpl[8] c_cpl[9] c_cpl[10] c_cpl[11] c_cpl[12] c_cpl[13] c_cpl[14] c_cpl[15] c_cpl[16] c_cpl[17] c_cpl[18] c_cpl[19] c_cpl[20] c_cpl[21] c_cpl[22] c_cpl[23] c_cpl[24] c_cpl[25] c_cpl[26] c_cpl[27] c_cpl[28] c_cpl[29] c_cpl[30] 
dump_modify dc1 format "%.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g"
dump dc2 all local ${N} ${POST}/c_*.txt c_cpl[1] c_cpl[2] c_cpl[3] c_cpl[4] c_cpl[5] c_cpl[6] c_cpl[7] c_cpl[8] c_cpl[9] c_cpl[10] c_cpl[11] c_cpl[12] c_cpl[13] c_cpl[14] c_cpl[15] c_cpl[16] c_cpl[17] c_cpl[18] c_cpl[19] c_cpl[20] c_cpl[21] c_cpl[22] c_cpl[23] c_cpl[24] c_cpl[25] c_cpl[26] c_cpl[27] c_cpl[28] c_cpl[29] c_cpl[30] 
dump_modify dc2 format "%.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g"
dump da all custom ${N} ${POST}/atom_*.txt id type x y z vx vy vz omegax omegay omegaz radius
dump_modify da format "%d %d %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g"
