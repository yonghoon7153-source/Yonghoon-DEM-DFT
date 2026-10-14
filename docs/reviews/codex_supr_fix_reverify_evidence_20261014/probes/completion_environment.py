"""Diagnose selftest environment; bootstrap existing dependencies in real isolated probe."""
import contextlib
import io
import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / 'source' / 'scripts'))
import supp20_input_receipt as S

NP = S.NP
OUT = BASE / 'evidence' / 'completion_environment'
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'tmp').mkdir(exist_ok=True)
tempfile.tempdir = str(OUT / 'tmp')
real_generation = NP.derive_generation(NP.ROOT)
(OUT / 'real_generation_probe.json').write_text(json.dumps(real_generation, ensure_ascii=False, indent=2), encoding='utf-8')
original_main = NP.main
original_subprocess_run = NP.subprocess.run
deps = [str(BASE.parent / 'lhs_coverage_review_20260930' / 'deps'),
        str(BASE.parent / 'gen2_network_reverify3_20261007' / 'deps')]
bootstrap = 'import sys; sys.path[:0] = ' + repr(deps) + '\n'
bootstrapped_calls = []
mode = 'original'


def observing_main(argv=None):
    rc = original_main(argv)
    if argv and '--preflight-receipt' in argv:
        rp = Path(argv[argv.index('--preflight-receipt') + 1])
        if rp.name == 'pos_preflight.json' and rp.is_file():
            folder = OUT / mode
            folder.mkdir(exist_ok=True)
            rec = json.loads(rp.read_text(encoding='utf-8'))
            (folder / rp.name).write_bytes(rp.read_bytes())
            log = Path(rec['log']['path'])
            (folder / log.name).write_bytes(log.read_bytes())
    return rc


def bootstrap_generation_process(argv, *a, **kw):
    if isinstance(argv, list) and len(argv) > 4 and argv[1:4] == ['-I', '-B', '-c'] and argv[4] == NP.GEN_PROBE:
        argv = list(argv)
        argv[4] = bootstrap + argv[4]
        bootstrapped_calls.append(dict(python=argv[0], code_root=argv[5], bootstrap=bootstrap))
    return original_subprocess_run(argv, *a, **kw)


summary = dict(real_generation=real_generation, runs=[], bootstrap=bootstrap)
for mode in ('original', 'dependency_bootstrap_only'):
    buf = io.StringIO()
    bootstrap_patch = patch.object(NP.subprocess, 'run', bootstrap_generation_process) if mode != 'original' else contextlib.nullcontext()
    with bootstrap_patch, patch.object(NP, 'main', observing_main), contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        if mode != 'original':
            summary['bootstrapped_real_generation'] = NP.derive_generation(NP.ROOT)
        rc = S.main(['--selftest'])
    text = buf.getvalue()
    (OUT / f'{mode}.log').write_text(text, encoding='utf-8')
    summary['runs'].append(dict(mode=mode, rc=rc, final_line=text.strip().splitlines()[-1],
                                failures=[line for line in text.splitlines() if line.lstrip().startswith('FAIL')]))
    print(mode, rc, text.strip().splitlines()[-1])
summary['bootstrapped_calls'] = bootstrapped_calls
(OUT / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
print('actual isolated generation error:', real_generation['error'])
