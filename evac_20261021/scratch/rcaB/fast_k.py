"""Run the fast checks (K1-K6, K9) of scripts/test_step3_conv_cert.py without the heavy seal table."""
import importlib.util
import os
import sys

root = sys.argv[1]
sys.path.insert(0, os.path.join(root, 'scripts'))
spec = importlib.util.spec_from_file_location('tcc', os.path.join(root, 'scripts', 'test_step3_conv_cert.py'))
T = importlib.util.module_from_spec(spec)
spec.loader.exec_module(T)
import step3_sigma as S3  # noqa: E402
import step3_conv_cert as CC  # noqa: E402
T.S3, T.CC = S3, CC
for fn in (T.t_k1_default_bitid, T.t_k2_defaults, T.t_k3_knob, T.t_k4_x0, T.t_k5_certify_unit, T.t_k6_solve_cert, T.t_k9_cli):
    print('--', fn.__name__)
    fn()
print(f'fast part: {T._ok}/{T._ok + len(T._fail)} PASS', T._fail)
