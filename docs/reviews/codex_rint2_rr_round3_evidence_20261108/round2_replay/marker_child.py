import sys,types
from pathlib import Path
sys.path.insert(0,sys.argv[1])
import rint_first_result as r
m=types.SimpleNamespace(_solve_cg=lambda: 7, solve_sigma_z=lambda: {"sigma":7})
r.install(sys.argv[2],m)
m._solve_cg()
Path(sys.argv[3]).write_text("returned")
