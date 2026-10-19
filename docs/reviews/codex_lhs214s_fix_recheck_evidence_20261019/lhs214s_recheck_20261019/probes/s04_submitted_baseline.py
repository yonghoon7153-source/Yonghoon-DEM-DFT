"""Run current submitted null test unchanged against baseline app/template imports."""
from pathlib import Path

REVIEW = Path(__file__).resolve().parents[1]
script = REVIEW / 'source/webapp/test_single_null_metrics.py'
baseline_path = REVIEW.parent / 'lhs214rr_recheck_20261019/source/webapp/test_single_null_metrics.py'
exec(compile(script.read_bytes(), str(script), 'exec'), dict(__name__='__main__', __file__=str(baseline_path)))
