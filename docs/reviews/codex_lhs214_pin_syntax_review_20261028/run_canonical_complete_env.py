from pathlib import Path
import os, runpy, sys, tempfile
r=Path(__file__).resolve().parent
tmp=r/'tmp'; tmp.mkdir(exist_ok=True)
os.environ['TEMP']=os.environ['TMP']=str(tmp)
tempfile.tempdir=str(tmp)
sys.argv=[str(r/'repo/docs/reviews/lhs214_pin_syntax_fix_evidence_20261024/tools/check_pin_boundaries.py'),'--repo',str(r/'repo'),'--out',str(r/'canonical_boundary_complete_env')]
runpy.run_path(sys.argv[0],run_name='__main__')
