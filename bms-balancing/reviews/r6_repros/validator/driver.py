
"""mock driver — same shape as tests/test_review_findings.py::test_r3_07: data_root/build/dd_eval_anchors patched,
then verify.main(["eval", "--compare", <csv>, *extra]) → sys.exit(rc)."""
import sys, json
sys.path.insert(0, '<scratch>/verify_validator/wt_verify_validator/bms-balancing')
from unittest.mock import patch
from bms_balancing import verify
an = json.loads(sys.argv[1]); py = json.loads(sys.argv[2]); P = [[1.077218, -0.022949, 1.001342, 0.000309, 0.295099], [1.076074, -0.022129, 1.001279, 0.000299, 0.295298], [1.181472, -0.141171, 1.080759, -0.000775, 0.239466], [1.08, -0.04, 1.05, -0.03, 0.25], [1.1, -0.05, 1.1, -0.01, 0.1], [1.1, -0.05, 1.1, -0.01, 0.2], [1.1, -0.05, 1.1, -0.01, 0.3], [1.1, -0.05, 1.1, -0.01, 0.4]]
class Obj:
    def _at(self, p, col): return py[col][P.index([float(x) for x in p])]
    def rmse_pocv(self, p): return self._at(p, "rmse_pocv")
    def rmse_dvdq(self, p): return self._at(p, "rmse_dvdq")
    def rmse_dqdv(self, p, weighted=False): return self._at(p, "rmse_dqdv_w" if weighted else "rmse_dqdv")
with patch.object(verify.D, "data_root", return_value=None), \
     patch.object(verify, "build", return_value=Obj()), \
     patch.object(verify, "dd_eval_anchors", return_value=list(an.items())):
    sys.exit(verify.main(["eval", "--compare", sys.argv[3]] + sys.argv[4:]))
