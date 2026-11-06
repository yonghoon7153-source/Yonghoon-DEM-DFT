"""Independent pure-Python probes on exact AST nodes from the fixed received sources.

No inventory filesystem function or real ibb/WSL path is invoked.
TextIOWrapper(BytesIO(...)) is an in-memory simulation of the documented decoder.
Timing payloads are synthetic malformed text and are isolated in child processes.
"""
import ast
import contextlib
import hashlib
import io
import json
import math
from pathlib import Path
import random
import re
import subprocess
import sys
import time

BASE = Path(__file__).resolve().parents[1]
SOURCE = BASE / 'received/docs/reviews/lhs_pressure_inventory_20261104/pressure_inventory.sh'
B7 = BASE / 'received/scripts/lhs_pressure_record.py'
CODE = SOURCE.read_text(encoding='utf-8').split("-c '\n", 1)[1].split("\n' \"$@\"", 1)[0]


def extract(source, names, initial):
    nodes = []
    for node in ast.parse(source).body:
        label = node.name if isinstance(node, (ast.FunctionDef, ast.ClassDef)) else None
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            label = node.targets[0].id
        if label in names:
            nodes.append(node)
    module = ast.Module(body=nodes, type_ignores=[])
    exec(compile(module, '<exact extracted AST>', 'exec'), initial)
    return initial


INV = extract(CODE, {'PRESS_LINE', 'PRESS_PREFIX', 'RESTART_ECHO', 'RESTART_MESSAGE',
    'MAX_LINE', 'MAX_LOG_BYTES', 'Refusal', 'count_text', 'main', 'identity_allowed'},
    {'re': re, 'json': json})
B7_NS = extract(B7.read_text(encoding='utf-8'), {'PRESS_LINE', '_num', 'parse_log'},
    {'re': re, 'math': math})


def decoded(payload):
    return io.TextIOWrapper(io.BytesIO(payload), encoding='utf-8', errors='replace', newline=None)


def compare(payload):
    with decoded(payload) as stream:
        actual = INV['count_text'](stream)
    with decoded(payload) as stream:
        expected = B7_NS['parse_log'](stream.read())['n']
    assert actual['b7_matches'] == expected, (payload, actual, expected)
    assert set(actual) == {'b7_matches', 'pressure_prefix_malformed',
        'read_restart_echo_lines', 'reading_restart_message_lines'}
    assert all(isinstance(value, int) for value in actual.values())
    return actual


def timing(n):
    text = 'Current Pressure: ' + 'xMPa(Target:' * n + 'X'
    started = time.perf_counter()
    result = INV['count_text'](io.StringIO(text))
    print(json.dumps({'repeats': n, 'characters': len(text),
        'seconds': time.perf_counter() - started, 'result': result}))


def run():
    report = {'scope': 'Exact extracted parser/main functions; in-memory decoder simulation; no POSIX filesystem or host execution',
        'python': sys.version, 'command_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'b7_sha256': hashlib.sha256(B7.read_bytes()).hexdigest()}
    assert INV['PRESS_LINE'].pattern == B7_NS['PRESS_LINE'].pattern
    assert INV['PRESS_LINE'].flags == B7_NS['PRESS_LINE'].flags
    report['regex_pattern_and_flags_equal'] = True
    separators = ['\n', '\r', '\r\n', '\v', '\f', '\x1c', '\x1d', '\x1e', '\x85', '\u2028', '\u2029']
    pressure = 'Current Pressure: VALUE_947261 MPa (Target: TARGET_268314)'
    tokens = ['', pressure, 'Current Pressure: NaN MPa (Target: inf)',
        'Current Pressure: nonnumericMPa(Target:arbitrary)', 'Current Pressure: broken',
        'Current Pressure: 1 MPa (Target: 2) trailing', 'Current Pressure: 1 MPa (Target: 2)\0',
        'print "Current Pressure: ${current_press} MPa (Target: ${target_press})"',
        'read_restart SECRET_PATH', 'Reading restart file SECRET_PATH',
        '# read_restart SECRET_PATH', 'print "Reading restart file SECRET_PATH"',
        'Reading restart files SECRET_PATH', 'read_restartx SECRET_PATH',
        '\t' + pressure, '\u00a0' + pressure, '\ufeff' + pressure]
    count = 0
    for left in tokens:
        for right in tokens:
            for sep in separators:
                compare((left + sep + right).encode('utf-8'))
                count += 1
    rng = random.Random(20261104)
    for _ in range(4000):
        pieces = [rng.choice(tokens) for _ in range(rng.randrange(1, 15))]
        data = ''.join(piece + rng.choice(separators) for piece in pieces).encode('utf-8')
        if rng.randrange(2):
            index = rng.randrange(len(data) + 1)
            data = data[:index] + rng.choice([b'\xff', b'\xc0\x80', b'\xed\xa0\x80', b'\xe2\x80']) + data[index:]
        compare(data)
        count += 1
    report['byte_differential_cases_passed'] = count
    result = compare((pressure + '\nCurrent Pressure: NaN MPa (Target: inf)\n' +
        'read_restart SECRET_PATH\nReading restart file SECRET_PATH\n' +
        '# read_restart SECRET_PATH\nprint "Reading restart file SECRET_PATH"\n').encode())
    assert result == {'b7_matches': 2, 'pressure_prefix_malformed': 0,
        'read_restart_echo_lines': 1, 'reading_restart_message_lines': 1}
    serialized = json.dumps(result)
    assert all(secret not in serialized for secret in ['VALUE_947261', 'TARGET_268314', 'SECRET_PATH'])
    report['separate_restart_counts_and_value_nonoutput'] = result
    main_probes = []
    def broken_identity():
        raise RuntimeError('SECRET_EXCEPTION_954321')
    for label, argv, identity in [
        ('invalid CLI arguments', ['ibb', 'SECRET_PATH'], broken_identity),
        ('wrong identity', ['ibb'], lambda: ('Linux', 'SECRET_HOST', 'generic', 'SECRET_USER', 1, 1)),
        ('identity exception', ['ibb'], broken_identity)]:
        INV['runtime_identity'] = identity
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            rc = INV['main'](argv)
        actual = json.loads(stdout.getvalue())
        assert rc == 2 and actual['rc'] == 2 and stderr.getvalue() == ''
        assert 'SECRET' not in stdout.getvalue()
        main_probes.append({'case': label, 'rc': rc, 'result': actual, 'stderr': stderr.getvalue()})
    report['main_fakes_explicitly_labelled'] = main_probes
    report['timing_synthetic_malformed'] = []
    for n in [100, 300, 1000, 3000, 10000]:
        try:
            p = subprocess.run([sys.executable, '-I', '-X', 'utf8', '-B', str(Path(__file__).resolve()), '--timing', str(n)],
                capture_output=True, text=True, timeout=5)
            assert p.returncode == 0, p.stderr
            report['timing_synthetic_malformed'].append(json.loads(p.stdout))
        except subprocess.TimeoutExpired:
            report['timing_synthetic_malformed'].append({'repeats': n,
                'characters': len('Current Pressure: ') + 12*n + 1, 'timeout_seconds': 5})
    print(json.dumps(report, ensure_ascii=True, indent=2))


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--timing':
        timing(int(sys.argv[2]))
    else:
        run()
