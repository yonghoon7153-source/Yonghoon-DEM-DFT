"""Read-only review bootstrap; scratch stays under this review."""
import os, sys, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT.parent
REPO = ROOT / 'repo'
TMP = ROOT / 'tmp' / 'runtime'
TMP.mkdir(parents=True, exist_ok=True)
tempfile.tempdir = str(TMP)
os.environ['TEMP'] = os.environ['TMP'] = str(TMP)
for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'): os.environ[key] = '1'
sys.dont_write_bytecode = True
sys.path[:0] = [str(REPO / 'scripts'), str(WORK / 'lhs_coverage_review_20260930' / 'deps'), str(WORK / 'gen2_network_reverify3_20261007' / 'deps')]
