"""Local review bootstrap. Does not edit pinned modules."""
import os, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT.parent
SOURCE=Path(os.environ.get('RINT_REVIEW_SOURCE', str(ROOT/'source'))).resolve()
(ROOT/'tmp').mkdir(exist_ok=True)
tempfile.tempdir=str(ROOT/'tmp')
os.environ['TEMP']=os.environ['TMP']=str(ROOT/'tmp')
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'): os.environ[k]='1'
os.environ['PYTHONIOENCODING']='utf-8'
sys.dont_write_bytecode=True
sys.path[:0]=[str(SOURCE/'scripts'),str(WORK/'lhs_coverage_review_20260930/deps'),str(WORK/'gen2_network_reverify3_20261007/deps')]
if hasattr(sys.stdout,'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr,'reconfigure'): sys.stderr.reconfigure(encoding='utf-8')
