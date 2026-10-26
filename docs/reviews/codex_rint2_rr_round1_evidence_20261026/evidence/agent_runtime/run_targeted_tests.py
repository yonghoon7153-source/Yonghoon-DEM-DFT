import runtime_bootstrap as boot
import importlib.util, sys
import step3_sigma as s3
import step3_conv_cert as cc
import test_step3_conv_cert as conv
import test_step3_target_cert as target

def load_file(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

conv._load_base = lambda: load_file(boot.ROOT / 'historical' / 'd1768cf0c' / 'scripts' / 'step3_sigma.py', 'historical_step3_sigma')
conv.S3, conv.CC = s3, cc
sys.argv = ['test_step3_conv_cert.py']
rc = conv.main()
target.S3, target.CC = s3, cc
original_loader = target._load_base
def historical_loader(rel, name, commit=None):
    if commit != target.RCA208_BASE:
        raise RuntimeError('Only the requested T24 historical source is mapped')
    return load_file(boot.ROOT / 'historical' / commit / rel, name)
target._load_base = historical_loader
target.t24()
print('TARGET_T24', target._ok, 'PASS;', len(target._fail), 'FAIL')
sys.exit(rc or bool(target._fail))

