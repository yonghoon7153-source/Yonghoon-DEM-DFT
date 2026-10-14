"""Run unchanged diagnostic tests on Windows; resource is RSS telemetry only.
No physics, array, geometry, solver, expectation or tolerance is patched.
"""
from pathlib import Path
import sys, types, runpy
R=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(R/'source/scripts'),str(R.parent/'lhs_coverage_review_20260930/deps'),str(R.parent/'gen2_network_reverify3_20261007/deps')]
resource=types.ModuleType('resource')
resource.RUSAGE_SELF=0
resource.getrusage=lambda who:types.SimpleNamespace(ru_maxrss=float('nan'))
sys.modules['resource']=resource
script=sys.argv[1]
sys.argv=sys.argv[1:]
runpy.run_path(str(R/'source/scripts'/script),run_name='__main__')
