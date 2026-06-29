#!/usr/bin/env python3
"""UMA smoke-test — loads UMA the EXACT way disorder_ensemble_diffusion.py does
and runs ONE energy/force eval on the b2o3 champion. If this prints OK, MD will
run here; if it raises, the env is the problem (not the MD code).

  python3 tools/modelc_v3/uma_smoke.py [xyz] [device]
"""
import sys
xyz = sys.argv[1] if len(sys.argv) > 1 else "db/structures/b2o3_relaxV0.xyz"
device = sys.argv[2] if len(sys.argv) > 2 else "cuda"

from ase.io import read
from fairchem.core import pretrained_mlip
from fairchem.core.calculate.ase_calculator import FAIRChemCalculator

import fairchem.core as fc
print("fairchem", getattr(fc, "__version__", "?"), "device", device)
predictor = pretrained_mlip.get_predict_unit("uma-s-1p1", device=device)
calc = FAIRChemCalculator(predictor, task_name="omat")

a = read(xyz)
a.calc = calc
e = a.get_potential_energy()
f = a.get_forces()
import numpy as np
print(f"OK  natoms={len(a)}  E={e:.4f} eV  |F|max={np.abs(f).max():.4f} eV/A")
print("=> UMA MD will run on this machine.")
