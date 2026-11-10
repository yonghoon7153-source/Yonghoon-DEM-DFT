#!/usr/bin/env python3
"""probe6_read.py - value-blind reader for the Rint 2 development probe 6 (SBE numeric probe, sigma sealed).

Reads ONE runner output folder (one arm, arm 0, kit_SBE_vgcf100) and, optionally, the watcher's log folder, and
prints / writes ONLY the keys of the closed tables below: iteration counts, residuals, plate-current imbalance,
convergence flags, backend, number of unknowns, time, memory, identity hashes.  Every other number of the arm JSON
(conductivity, currents, resistances, dissipation shares, certificate brackets ...) is never printed, never written
and never used to derive anything.  Runner log lines are never copied: known lines are re-rendered from the parsed
numbers, failure lines are kept with every number replaced by one '#'.

  python3 -I -B probe6_read.py --outdir O --logdir L [--kit-run RUN] [--s0-plan cjunc_plan.json]
  python3 -I -B probe6_read.py --outdir O --report R.json            (output folder only)

exit code  0 PROBE_OK             one accepted arm, every required key present, converged, runner rc 0
           3 PROBE_NOT_CONVERGED  keys present but not a clean positive converged solve (iterations are still reported)
           4 PROBE_INCOMPLETE     something required is missing or has an unexpected shape (shown as NONE + reason),
                                  an identity / registered-value check has no evidence, or the report could not be written
           5 PROBE_REJECTED       rejection marker, non-SBE arm, or the seal is broken in the runner log
           2 usage
Rules: docs/reviews/rint2_dev_probe_ledger_20261026.md section 2.  Standard library only.  Python 3.8.  ASCII source.
"""
import argparse
import hashlib
import json
import math
import os
import re
import sys

SCHEMA = 'rint2-probe6-report-v2'
RC_OK, RC_USAGE, RC_NOT_CONVERGED, RC_INCOMPLETE, RC_REJECTED = 0, 2, 3, 4, 5
VERDICT = {RC_OK: 'PROBE_OK', RC_NOT_CONVERGED: 'PROBE_NOT_CONVERGED', RC_INCOMPLETE: 'PROBE_INCOMPLETE',
           RC_REJECTED: 'PROBE_REJECTED'}
KIT_ARM_PREFIX = 'p2_SBE_vgcf100_'
ARM_RE = r'p2_[A-Za-z0-9_]+_a([0-7])\.json'

# ---------------------------------------------------------------------------------------------------------------
# THE closed allowlist.  (output key, path below mpm_metrics.step3, kind, required for PROBE_OK)
#   kind: 'posint' int > 0 | 'int' int >= 0 | 'sint' any int | 'num' finite number | 'bool' | 'boolnull' |
#         ('enum', names) | ('re', pattern)
# Nothing outside this table (plus the fixed log / sample / meta / env tables below) is ever emitted with a value.
# ---------------------------------------------------------------------------------------------------------------
CERT_STATUSES = ('POSITIVE_SOLVED', 'VALID_ZERO_TOPOLOGY', 'ELECTRODE_SHORT', 'NOT_CERTIFIABLE')
COMP_STATUSES = ('complete', 'unconverged', 'not_solvable', 'failed', 'disabled', 'skipped', 'missing')
ARM_FIELDS = (
    ('n_dof', ('n_dof',), 'posint', True),
    ('cg_iters', ('cg_iters',), 'int', True),
    ('cg_info', ('cg_info',), 'sint', True),
    ('cg_resid', ('cg_resid',), 'num', True),
    ('unconverged', ('unconverged',), 'bool', True),
    ('cert_version', ('conv_cert', 'version'), ('re', r'conv-cert-v[0-9]{1,3}'), False),
    ('cert_status', ('conv_cert', 'status'), ('enum', CERT_STATUSES), True),
    ('cert_ok', ('conv_cert', 'ok'), 'bool', True),
    ('cert_pass_a', ('conv_cert', 'pass_a'), 'bool', True),
    ('cert_pass_b', ('conv_cert', 'pass_b'), 'bool', True),
    ('cert_pass_c', ('conv_cert', 'pass_c'), 'bool', True),
    ('cert_pass_d', ('conv_cert', 'pass_d'), 'boolnull', True),
    ('cert_info', ('conv_cert', 'info'), 'sint', False),
    ('cert_resid', ('conv_cert', 'resid'), 'num', False),
    ('cert_imbalance', ('conv_cert', 'imbalance'), 'num', True),
    ('cert_iters', ('conv_cert', 'iters'), 'int', True),
    ('cert_resolve_iters', ('conv_cert', 'resolve_iters'), 'int', True),
    ('cert_resolve_info', ('conv_cert', 'resolve_info'), 'sint', True),
    ('cert_rtol_used', ('conv_cert', 'rtol_used'), 'num', False),
    ('cert_rtol_max', ('conv_cert', 'rtol_max'), 'num', False),
    ('cert_eps_I', ('conv_cert', 'eps_I'), 'num', False),
    ('cert_resolve_rtol', ('conv_cert', 'resolve_rtol'), 'num', False),
    ('cert_target_tol', ('conv_cert', 'target_tol'), 'num', False),
    ('backend_requested', ('manifest', 'backend_last_solve', 'requested'), ('enum', ('gpu', 'cpu')), False),
    ('backend_used', ('manifest', 'backend_last_solve', 'used'), ('enum', ('gpu', 'cpu')), False),
    ('backend_precond', ('manifest', 'backend_last_solve', 'precond'), ('enum', ('jacobi', 'amg')), False),
    ('backend_rtol', ('manifest', 'backend_last_solve', 'rtol'), 'num', False),
    ('electronic_status', ('manifest', 'components', 'electronic', 'status'), ('enum', COMP_STATUSES), True),
    ('electronic_backend_used', ('manifest', 'components', 'electronic', 'backend', 'used'), ('enum', ('gpu', 'cpu')), False),
    ('manifest_status', ('manifest', 'status'), ('enum', ('complete', 'partial', 'failed')), False),
    ('protocol_id', ('manifest', 'physics_protocol_id'), ('re', r'p[0-9a-z]{1,8}-[0-9a-f]{8,64}'), False),
    ('code_sha', ('manifest', 'code_sha'), ('re', r'[0-9a-f]{7,40}(\+dirty)?'), False),
    ('input_digest', ('manifest', 'input_digest'), ('re', r'[0-9a-f]{16}'), False),
)
REQUIRED = tuple(row[0] for row in ARM_FIELDS if row[3])
#: needed on top of REQUIRED for PROBE_OK (the payload records a component backend only for a complete component)
REQUIRED_OK = ('electronic_backend_used',)
#: relative certificate numbers that are NOT sigma but are outside the ledger's list - names only, never values
HELD_BACK = ('conv_cert.dsigma_rel', 'conv_cert.target_err_bound_rel', 'conv_cert.target_width_rel',
             'conv_cert.target_in_bracket')
#: keys whose numbers are sealed - only used by the leak tripwire (no value of these may equal an emitted number)
SEALED_HINTS = ('sigma', 'I_bot', 'I_top', 'target_lo', 'target_hi', 'target_U', 'target_W', 'target_flow', 'scale',
                'R_bulk', 'share', 'P_total', 'P_sum', 'current', 'dsigma', 'err_bound', 'width_rel')
RECEIPT_FIELDS = (
    ('receipt_digest', ('receipt_digest',), ('re', r'[0-9a-f]{8,64}')),
    ('receipt_code_sha', ('code_sha',), ('re', r'[0-9a-f]{7,40}(\+dirty)?')),
    ('receipt_arms', ('arms',), 'posint'),
    ('receipt_expect_backend', ('expect_backend',), ('enum', ('gpu', 'cpu'))),
    ('receipt_step3_rtol', ('step3_rtol',), 'num'),
    ('receipt_vox_um', ('vox_um',), 'num'),
    ('receipt_ptfe_stamp', ('ptfe_stamp',), ('enum', ('off', 'centerline', 'face_alpha'))),
)
#: watcher meta file (key=value) - closed keys, each with a value pattern
META_FIELDS = (
    ('probe6_meta_version', r'[0-9]{1,3}', 'int'), ('pin', r'[0-9a-f]{40}', 'str'), ('maxiter', r'[0-9]{1,9}', 'int'),
    ('kit', r'kit_SBE_vgcf100', 'str'), ('kit_run', r'[A-Za-z0-9._+-]{1,120}', 'str'), ('kit_run_matches_s0', r'[01]', 'int'),
    ('outdir', r'~?[A-Za-z0-9._/+-]{1,300}', 'str'), ('logdir', r'~?[A-Za-z0-9._/+-]{1,300}', 'str'),
    ('start_epoch', r'[0-9]{9,11}', 'int'), ('start_kst', r'[0-9T:+-]{19,25}', 'str'),
    ('end_epoch', r'[0-9]{9,11}', 'int'), ('end_kst', r'[0-9T:+-]{19,25}', 'str'), ('wall_s', r'[0-9]{1,8}', 'int'),
    ('runner_rc', r'[0-9]{1,3}', 'int'), ('cap_gb', r'[0-9]{1,4}', 'int'), ('cap_term', r'[01]', 'int'),
    ('aborted', r'[01]', 'int'), ('sample_s', r'[0-9]{1,4}', 'int'), ('time_v', r'[01]', 'int'),
    ('umask', r'[0-7]{3,4}', 'str'), ('mode_bad', r'[0-9]{1,6}', 'int'), ('git_lines_before', r'[0-9]{1,6}', 'int'),
    ('git_lines_after', r'[0-9]{1,6}', 'int'), ('scrubbed', r'[A-Z0-9_ ]{0,600}', 'str'), ('pythonpath_set', r'[01]', 'int'),
    ('tool_sha256_wrapper', r'[0-9a-f]{64}', 'str'), ('tool_sha256_reader', r'[0-9a-f]{64}', 'str'),
    ('runner_sha256', r'[0-9a-f]{64}', 'str'), ('runner_log_sha256', r'[0-9a-f]{64}', 'str'),
    ('s0_plan_sha256', r'[0-9a-f]{64}', 'str'), ('kit_run_before', r'[0-9]{1,4}', 'int'), ('kit_run_new', r'[0-9]{1,4}', 'int'),
    ('attempt', r'[12]', 'int'), ('expect_rtol', r'[0-9][0-9.eE+-]{0,11}', 'str'), ('expect_backend', r'gpu|cpu', 'str'),
    ('solve_started', r'[01]', 'int'), ('orphans', r'[0-9]{1,6}', 'int'), ('orphans_left', r'[0-9]{1,6}', 'int'),
    ('pregate', r'[01]', 'int'), ('gpu_used_start_mib', r'[0-9]{1,7}|NA', 'str'), ('disk_free_gb_kit', r'[0-9]{1,9}|NA', 'str'),
    ('disk_free_gb_log', r'[0-9]{1,9}|NA', 'str'),
) + tuple(('env_' + n, r'unset|empty|set|value:[A-Za-z0-9][A-Za-z0-9,._-]{0,31}', 'str') for n in (
    'CUDA_VISIBLE_DEVICES', 'OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'OPENBLAS_CORETYPE', 'PYTHONUNBUFFERED', 'BASH_ENV'))
#: watcher environment fingerprint (key=value) - versions only
ENV_KEYS = ('python', 'python_impl', 'numpy', 'scipy', 'cupy', 'cupy_cuda_runtime', 'numpy_blas', 'blas_core', 'gpu_name',
            'gpu_driver', 'gpu_mem_total_mib', 'cuda_version', 'kernel', 'os', 'cpu_model', 'nproc', 'mem_total_kb',
            'git', 'bash')
ENV_VALUE_RE = r'[A-Za-z0-9 ._:+()/@,#-]{0,120}'
SAMPLE_COLS = ('epoch', 'elapsed_s', 'log_lines', 'rss_sum_kb', 'rss_proc_kb', 'gpu_used_mib', 'gpu_ours_mib', 'gpu_util')

# --- runner / payload log lines (non-ASCII text as escapes; sources: scripts/mpm_webapp_payload.py,
#     scripts/step3_sigma.py, scripts/sdcp_gain_vox015_8arm.sh) ---
SEAL_PREFIX = '[\ubd09\uc778'                                  # the payload's seal token starts with this
RESULT_WORD = '\u03c3_e_eff'                                    # the payload's result word (sigma_e_eff)
_NUM = r'[0-9.eE+-]+|nan|inf'
LOG_SOLVE = re.compile(r'^\s*STEP3 solve: ([0-9,]+) dof, plate contacts ([0-9,]+)/([0-9,]+) \u2014 CG running \((GPU|CPU),')
LOG_DONE = re.compile(r'^\s*STEP3 \u03c3_e_eff = (.*?) S/cm\s+\(vox ([0-9.]+)[\u00b5\u03bc]m, ([0-9,]+) dof, '
                      r'resid (' + _NUM + r'), ([0-9]+)s\)')
LOG_COLLECTOR = re.compile(r'^\s*STEP3 collector (scenarios|PRISTINE)')
LOG_MAXITER = re.compile(r'^\s*STEP3: CG maxiter ([0-9,]+) \(')
LOG_RTOL = re.compile(r'^\s*STEP3: CG rtol (' + _NUM + r') \+')
LOG_FA = re.compile(r'^\s*STEP3: \u2605 S1 face_alpha \u2014 .*\(([0-9]+)s\) \u2014')
LOG_CJ = re.compile(r'^\s*STEP3: \u2605 S2 .*\(([0-9]+)s\) \u2014 R_j =')
LOG_VOXELIZE = re.compile(r'^\s*STEP3: voxelizing ')
LOG_NOTCONV = re.compile(r'STEP3 CG not converged \(info=(-?[0-9]+), resid=(' + _NUM + r')\)')
LOG_CERTFAIL = re.compile(r'STEP3 \uc218\ub834 \uc99d\uc11c \uc2e4\ud328 \[([A-Z_]+)\] \(\u24d0 (True|False) \u00b7 \u24d1 (True|False) '
                          r'\ubd88\uade0\ud615 (' + _NUM + r') \u00b7 \u24d2 (True|False) .*? \u00b7 \u24d3 (True|False|None)')
LOG_PEAK = re.compile(r'^\[p2\] \u25b8 (\S+) \ud53c\ud06c \ud638\uc2a4\ud2b8 RSS = ([0-9.]+) GB')
LOG_ARM = re.compile(r'^\[p2\] \u2500\u2500 (p2_[A-Za-z0-9_]+_a[0-7])\s+shift=\(([0-9. ]+)\)')
LOG_SKIP = re.compile(r'^\[p2\] SKIP ')
LOG_SAVED = re.compile(r'^saved p2_[A-Za-z0-9_]+\.json ')
LOG_GATES = (('gate_receipt', re.compile(r'^\[p2\] \ub7f0 \uc601\uc218\uc99d \u2192')),
             ('gate_discipline', re.compile(r'^\[p2\] \uaddc\uc728 \uac80\uc0ac \ud1b5\uacfc')),
             ('gate_undefined', re.compile(r'^\[p2\] \ubbf8\uc815\uc758 \uc774\ub984 \uc5c6\uc74c')))
FAIL_MARK = re.compile(r'ABORT|FAILED|Traceback|Error|error|Killed|REFUSED|not converged|UNRELIABLE|CUDA|OutOfMemory|'
                       r'[A-Z][A-Z0-9_]{2,}\||^ {5}\S|\u26a0|\u2717|\u26d4|\uc2e4\ud328')
#: one '#' per NUMBER (not per digit): the digit count of a fixed-notation value would give away its magnitude.
#: Also hex floats, any Unicode decimal digit (\\d: full-width ...) and super / subscript digits.
_SUPSUB = '\u2070\u00b9\u00b2\u00b3\u2074-\u2079\u2080-\u2089'
_MASK_RE = re.compile(r'[-+]?0[xX][0-9a-fA-F]*\.?[0-9a-fA-F]*(?:[pP][-+]?[0-9]+)?|\d+(?:[.,]\d+)*(?:[eE][-+\u2212]?\d+)?|[' + _SUPSUB + r']+')
MASK_KEEP = 30                                                  # masked failure lines kept: the first 30 and the last 30


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 20), b''):
            h.update(blk)
    return h.hexdigest()


def missing(why):
    return {'missing': why}


def is_missing(v):
    return isinstance(v, dict) and 'missing' in v


def _nonfinite(_tok):
    return float('nan')


def load_json(path):
    """-> (object, None) or (None, reason).  NaN / Infinity tokens load as non-finite floats (rejected by typed())."""
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f, parse_constant=_nonfinite), None
    except (OSError, ValueError, UnicodeError, RecursionError) as e:
        return None, 'unreadable (%s)' % type(e).__name__


def pick(obj, path):
    cur = obj
    for k in path:
        if not isinstance(cur, dict) or k not in cur:
            return False, None
        cur = cur[k]
    return True, cur


def typed(kind, v):
    """-> (ok, value, reason).  No coercion: a string is never read as a number, a bool is never read as an int."""
    if kind == 'int':
        if isinstance(v, bool) or not isinstance(v, int):
            return False, None, 'shape (integer expected)'
        return (True, v, None) if v >= 0 else (False, None, 'shape (negative)')
    if kind == 'posint':
        if isinstance(v, bool) or not isinstance(v, int) or v <= 0:
            return False, None, 'shape (positive integer expected)'
        return True, v, None
    if kind == 'sint':
        if isinstance(v, bool) or not isinstance(v, int):
            return False, None, 'shape (integer expected)'
        return True, v, None
    if kind == 'num':
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            return False, None, 'shape (number expected)'
        x = float(v)
        if not math.isfinite(x):
            return False, None, 'non-finite'
        return True, x, None
    if kind == 'bool':
        return (True, v, None) if isinstance(v, bool) else (False, None, 'shape (true / false expected)')
    if kind == 'boolnull':
        return (True, v, None) if (v is None or isinstance(v, bool)) else (False, None, 'shape (true / false / null expected)')
    if isinstance(kind, tuple) and kind[0] == 'enum':
        return (True, v, None) if (isinstance(v, str) and v in kind[1]) else (False, None, 'shape (not a known name)')
    if isinstance(kind, tuple) and kind[0] == 're':
        pat = kind[1]
        if not isinstance(v, str):
            return False, None, 'shape (text expected)'
        if not re.fullmatch(pat, v):
            return False, None, 'shape (unexpected text)'
        return True, v, None
    return False, None, 'shape (unknown kind)'


def read_table(obj, table, with_required=True):
    out = {}
    for row in table:
        key, path, kind = row[0], row[1], row[2]
        found, v = pick(obj, path)
        if not found:
            out[key] = missing('absent')
            continue
        if v is None and kind != 'boolnull':
            out[key] = missing('null')
            continue
        ok, val, why = typed(kind, v)
        out[key] = val if ok else missing(why)
    return out


def sealed_numbers(obj, key=''):
    """Floats stored under sealed-looking keys (tripwire only - these values are never emitted)."""
    got = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            got |= sealed_numbers(v, key + '.' + str(k))
    elif isinstance(obj, list):
        for v in obj:
            got |= sealed_numbers(v, key)
    elif isinstance(obj, float) and math.isfinite(obj) and obj not in (0.0, 1.0):
        if any(h in key for h in SEALED_HINTS):
            got.add(obj)
    return got


def folder_summary(path):
    """Folder summary: every regular file (relative path, size, sha256) and two digests of the listing.
    listing_sha256   = sha256 of lines '<sha256>  <size>  <path>\\n' sorted by path bytes
    sha256sum_style  = sha256 of lines '<sha256>  <path>\\n' (same recipe as scripts/rint_r_chain.py folder_digest;
                       equals: cd DIR && find . -type f -printf '%P\\n' | LC_ALL=C sort | xargs sha256sum | sha256sum)
    A symlink or special file gives no digest (reason reported)."""
    out = {'n_files': None, 'files': [], 'listing_sha256': None, 'sha256sum_style': None, 'problem': None}
    if os.path.islink(path) or not os.path.isdir(path):
        out['problem'] = 'not a folder'
        return out
    rows = []
    try:
        for root, dirs, files in os.walk(path):
            for nm in dirs:
                if os.path.islink(os.path.join(root, nm)):
                    out['problem'] = 'symlink in folder'
                    return out
            for nm in files:
                fp = os.path.join(root, nm)
                if os.path.islink(fp) or not os.path.isfile(fp):
                    out['problem'] = 'symlink or special file in folder'
                    return out
                rel = os.path.relpath(fp, path).replace(os.sep, '/')
                rows.append({'path': rel, 'size': os.path.getsize(fp), 'sha256': sha256_file(fp)})
    except OSError as e:
        out['problem'] = 'unreadable (%s)' % type(e).__name__
        return out
    rows.sort(key=lambda x: x['path'].encode('utf-8'))
    out['files'] = rows
    out['n_files'] = len(rows)
    out['listing_sha256'] = hashlib.sha256(
        ''.join('%s  %d  %s\n' % (x['sha256'], x['size'], x['path']) for x in rows).encode('utf-8')).hexdigest()
    out['sha256sum_style'] = hashlib.sha256(
        ''.join('%s  %s\n' % (x['sha256'], x['path']) for x in rows).encode('utf-8')).hexdigest()
    return out


def mask_line(line):
    """A failure line with every number replaced by one '#' (no digit survives); the home prefix becomes ~."""
    h = os.path.expanduser('~')
    if h and h != '/':
        line = line.replace(h, '~')
    return _MASK_RE.sub('#', line)


def sealed_token(text):
    return text.startswith(SEAL_PREFIX)


def _num(text):
    try:
        x = float(text.replace(',', ''))
    except ValueError:
        return None
    return x if math.isfinite(x) else None


def _int(text):
    t = text.replace(',', '')
    return int(t) if re.fullmatch(r'-?[0-9]{1,15}', t) else None


def parse_log(path):
    """-> (log dict, filtered lines, marker line numbers, problems, seal_broken)."""
    log, flt, marks, probs, seal_broken = {}, [], {}, [], False
    try:
        with open(path, 'rb') as f:
            text = f.read().decode('utf-8', 'replace')
    except OSError:
        return None, [], {}, ['runner.log unreadable'], False
    lines = text.split('\n')
    log['n_lines'] = len(lines) - 1 if text.endswith('\n') else len(lines)
    masked, tail, n_masked = [], [], 0
    for no, line in enumerate(lines, 1):
        m = LOG_ARM.match(line)
        if m:
            log['arm_tag'] = m.group(1)
            log['arm_shift_zero'] = all(_num(t) == 0.0 for t in m.group(2).split())
            marks.setdefault('arm_start', no)
            flt.append('arm_start tag=%s shift_zero=%d' % (m.group(1), 1 if log['arm_shift_zero'] else 0))
            continue
        m = LOG_SKIP.match(line)
        if m:
            log['skip_cached'] = True
            flt.append('skip_cached=1')
            continue
        for key, rx in LOG_GATES:
            if rx.match(line):
                log[key] = True
                flt.append('%s=1' % key)
        if LOG_VOXELIZE.match(line):
            marks.setdefault('voxelize', no)
            flt.append('step3_voxelize_start')
            continue
        m = LOG_MAXITER.match(line)
        if m:
            log['cg_maxiter'] = _int(m.group(1))
            flt.append('cg_maxiter=%s' % log['cg_maxiter'])
            continue
        m = LOG_RTOL.match(line)
        if m:
            log['cg_rtol'] = _num(m.group(1))
            flt.append('cg_rtol=%r' % log['cg_rtol'])
            continue
        m = LOG_FA.match(line)
        if m:
            log['face_alpha_prep_s'] = _int(m.group(1))
            marks.setdefault('face_alpha', no)
            flt.append('face_alpha_prep_s=%s' % log['face_alpha_prep_s'])
            continue
        m = LOG_CJ.match(line)
        if m:
            log['cjunc_prep_s'] = _int(m.group(1))
            marks.setdefault('cjunc', no)
            flt.append('cjunc_prep_s=%s' % log['cjunc_prep_s'])
            continue
        m = LOG_SOLVE.match(line)
        if m:
            log['solve_n_dof'] = _int(m.group(1))
            log['solve_plate_bot'] = _int(m.group(2))
            log['solve_plate_top'] = _int(m.group(3))
            log['solve_backend'] = m.group(4)
            marks.setdefault('solve', no)
            flt.append('step3_solve n_dof=%s plate_bot=%s plate_top=%s backend=%s'
                       % (log['solve_n_dof'], log['solve_plate_bot'], log['solve_plate_top'], log['solve_backend']))
            continue
        m = LOG_NOTCONV.search(line)
        if m:
            log['not_converged_info'] = _int(m.group(1))
            log['not_converged_resid'] = _num(m.group(2))
            flt.append('cg_not_converged info=%s resid=%r' % (log['not_converged_info'], log['not_converged_resid']))
            continue
        m = LOG_CERTFAIL.search(line)
        if m:
            tf = {'True': True, 'False': False, 'None': None}
            log['cert_fail_status'] = m.group(1) if m.group(1) in CERT_STATUSES else None
            log['cert_fail_pass'] = [tf[m.group(2)], tf[m.group(3)], tf[m.group(5)], tf[m.group(6)]]
            log['cert_fail_imbalance'] = _num(m.group(4))
            flt.append('cert_fail status=%s pass_abcd=%s imbalance=%r'
                       % (log['cert_fail_status'], ','.join(str(x) for x in log['cert_fail_pass']), log['cert_fail_imbalance']))
            continue
        m = LOG_DONE.match(line)
        if m:
            if not sealed_token(m.group(1)):
                seal_broken = True
                flt.append('step3_done SEAL_BROKEN (value not copied)')
            log['sealed'] = bool(sealed_token(m.group(1))) and log.get('sealed', True)
            log['done_vox_um'] = _num(m.group(2))
            log['done_n_dof'] = _int(m.group(3))
            log['done_resid'] = _num(m.group(4))
            log['done_step3_s'] = _int(m.group(5))
            marks.setdefault('done', no)
            flt.append('step3_done n_dof=%s resid=%r step3_s=%s sealed=%d'
                       % (log['done_n_dof'], log['done_resid'], log['done_step3_s'], 1 if log['sealed'] else 0))
            continue
        if LOG_COLLECTOR.match(line):
            if SEAL_PREFIX not in line:
                seal_broken = True
                log['sealed'] = False
                flt.append('collector_line SEAL_BROKEN (value not copied)')
            continue
        if (RESULT_WORD in line or 'STEP3 collector' in line) and 'S/cm' in line and SEAL_PREFIX not in line:
            seal_broken = True                                      # a result line in a shape the two patterns above do not know
            log['sealed'] = False
            flt.append('result_line SEAL_BROKEN (value not copied)')
            continue
        m = LOG_PEAK.match(line)
        if m:
            log['runner_peak_tag'] = m.group(1) if re.fullmatch(r'p2_[A-Za-z0-9_]+', m.group(1)) else None
            log['runner_peak_rss_gb'] = _num(m.group(2))
            flt.append('runner_peak_rss_gb=%r' % log['runner_peak_rss_gb'])
            continue
        if LOG_SAVED.match(line):
            log['saved'] = True
            marks.setdefault('saved', no)
            flt.append('payload_saved=1')
            continue
        if FAIL_MARK.search(line):
            n_masked += 1
            ml = mask_line(line.strip())[:240]
            if len(masked) < MASK_KEEP:
                masked.append(ml)
            else:
                tail = (tail + [ml])[-MASK_KEEP:]
    log['masked_lines'] = masked + tail
    log['masked_lines_dropped'] = n_masked - len(masked) - len(tail)
    for ln in log['masked_lines']:
        flt.append('masked: ' + ln)
    if log['masked_lines_dropped']:
        flt.append('masked_dropped=%d' % log['masked_lines_dropped'])
    if seal_broken:
        probs.append('SEAL_BROKEN_IN_LOG: the runner log has a result line without the seal token')
    return log, flt, marks, probs, seal_broken


def parse_keyvalue(path):
    """key=value lines -> dict (first '=' splits).  Unreadable -> None."""
    try:
        with open(path, 'rb') as f:
            text = f.read().decode('utf-8', 'replace')
    except OSError:
        return None
    out = {}
    for ln in text.split('\n'):
        if '=' in ln and not ln.startswith('#'):
            k, v = ln.split('=', 1)
            out.setdefault(k.strip(), v.strip())
    return out


def parse_meta(path):
    raw = parse_keyvalue(path)
    if raw is None:
        return None, ['meta.txt unreadable']
    out, probs, known = {}, [], set()
    for key, pat, conv in META_FIELDS:
        known.add(key)
        if key not in raw:
            continue
        if not re.fullmatch(pat, raw[key]):
            probs.append('meta key %s has an unexpected value shape (dropped)' % key)
            continue
        out[key] = int(raw[key]) if conv == 'int' else raw[key]
    extra = len([k for k in raw if k not in known])
    if extra:
        probs.append('meta has %d unknown key(s) (not copied)' % extra)
    return out, probs


def parse_env(path):
    raw = parse_keyvalue(path)
    if raw is None:
        return None
    out = {}
    for key in ENV_KEYS:
        if key in raw and re.fullmatch(ENV_VALUE_RE, raw[key]):
            out[key] = raw[key]
    return out


def parse_samples(path):
    """-> (rows as dict of int-or-None lists, problem)."""
    try:
        with open(path, 'rb') as f:
            text = f.read().decode('ascii', 'replace')
    except OSError:
        return None, 'samples.tsv unreadable'
    rows = []
    for ln in text.split('\n'):
        if not ln or ln.startswith('#'):
            continue
        cells = ln.split('\t')
        if len(cells) != len(SAMPLE_COLS):
            return None, 'samples.tsv row shape'
        row = []
        for c in cells:
            if re.fullmatch(r'[0-9]{1,15}', c):
                row.append(int(c))
            elif c == 'NA':
                row.append(None)
            else:
                return None, 'samples.tsv cell shape'
        rows.append(row)
    if not rows:
        return None, 'samples.tsv has no rows'
    return rows, None


def parse_time_v(path):
    """GNU time -v file -> {'max_rss_kb', 'elapsed_s', 'exit_status'} (absent keys left out)."""
    try:
        with open(path, 'rb') as f:
            text = f.read().decode('utf-8', 'replace')
    except OSError:
        return None
    out = {}
    m = re.search(r'Maximum resident set size \(kbytes\): ([0-9]{1,15})', text)
    if m:
        out['max_rss_kb'] = int(m.group(1))
    m = re.search(r'Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): ([0-9:.]{3,20})', text)
    if m:
        parts = m.group(1).split(':')
        try:
            sec = 0.0
            for p in parts:
                sec = sec * 60.0 + float(p)
            out['elapsed_s'] = int(sec)
        except ValueError:
            pass
    m = re.search(r'Exit status: ([0-9]{1,3})', text)
    if m:
        out['exit_status'] = int(m.group(1))
    return out


def col_max(rows, name):
    i = SAMPLE_COLS.index(name)
    vals = [r[i] for r in rows if r[i] is not None]
    return max(vals) if vals else None


def first_time(rows, line_no):
    """Epoch of the first sample whose log line count has reached line_no (resolution = sampling interval)."""
    ie, il = SAMPLE_COLS.index('epoch'), SAMPLE_COLS.index('log_lines')
    for r in rows:
        if r[il] is not None and r[ie] is not None and r[il] >= line_no:
            return r[ie]
    return None


DERIVED_FIELDS = ('backend_fallback', 'origin_shift_zero')


def no_arm_fields(why):
    """The closed field table with every key present (missing + reason) - the same keys whether or not an arm was read."""
    f = {row[0]: missing(why) for row in ARM_FIELDS}
    for k in DERIVED_FIELDS:
        f[k] = missing(why)
    return f


def read_arm(path):
    """-> (fields, sealed number set, problems).  Only ARM_FIELDS plus four derived identity checks."""
    doc, why = load_json(path)
    if doc is None:
        return no_arm_fields('arm JSON ' + why), set(), ['arm JSON ' + why]
    found, s3 = pick(doc, ('mpm_metrics', 'step3'))
    if not found or not isinstance(s3, dict):
        return no_arm_fields('no step3 block'), set(), ['arm JSON has no mpm_metrics.step3 block']
    f = read_table(s3, ARM_FIELDS)
    fnd, fb = pick(s3, ('manifest', 'backend_last_solve', 'fallback_reason'))
    f['backend_fallback'] = (fb is not None) if fnd else missing('absent')
    fnd, osh = pick(s3, ('manifest', 'origin_shift_um'))
    if fnd and isinstance(osh, list) and len(osh) == 3 and all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in osh):
        f['origin_shift_zero'] = all(float(x) == 0.0 for x in osh)
    else:
        f['origin_shift_zero'] = missing('absent')
    fnd, inp = pick(s3, ('manifest', 'input_files'))
    f['_input_files'] = inp if (fnd and isinstance(inp, dict)) else None
    return f, sealed_numbers(s3), []


def bed_match(input_files, plan):
    """Arm manifest input digests (first 16 hex of each role file sha256) vs the S0 stage-1 plan's full sha256."""
    want = ((plan or {}).get('source') or {}).get('inputs_sha256')
    if not isinstance(want, dict) or not isinstance(input_files, dict):
        return missing('absent')
    roles = ('fibre', 'fibre_dia', 'metrics_json', 'phase', 'scaffold', 'se')
    for r in roles:
        a, b = input_files.get(r), want.get(r)
        if not (isinstance(a, str) and isinstance(b, str) and re.fullmatch(r'[0-9a-f]{16}', a) and re.fullmatch(r'[0-9a-f]{64}', b)):
            return missing('shape')
        if b[:16] != a:
            return False
    return True


def fmt(v):
    if is_missing(v):
        return 'NONE (%s)' % v['missing']
    if isinstance(v, bool) or v is None:
        return str(v)
    if isinstance(v, float):
        return '%.6g' % v
    return str(v)


def home_rel(p):
    h = os.path.expanduser('~')
    ap = os.path.abspath(p)
    return ('~' + ap[len(h):]) if (h and h != '/' and (ap == h or ap.startswith(h + os.sep))) else ap


def run(args):
    probs, notes = [], []
    rep = {'schema': SCHEMA, 'tool': {'name': 'probe6_read.py', 'sha256': sha256_file(os.path.abspath(__file__))},
           'scope': 'outdir_and_logdir' if args.logdir else 'outdir_only', 'held_back': list(HELD_BACK)}
    rejected, incomplete = False, False
    out = args.outdir
    # ---- output folder ----
    rep['folder'] = folder_summary(out)
    rep['folder']['path'] = home_rel(out)
    if rep['folder']['problem']:
        probs.append('output folder: ' + rep['folder']['problem'])
        incomplete = True
    names = sorted(os.listdir(out)) if os.path.isdir(out) and not os.path.islink(out) else []
    arms, unknown = [], []
    for nm in names:
        if nm.startswith('.rejected_'):
            rejected = True
            probs.append('REJECTION_MARKER in the output folder')
        elif nm == 'run_receipt.json':
            pass
        elif nm.startswith('p2_') and nm.endswith('.json'):
            arms.append(nm)
        else:
            unknown.append(nm)
    for nm in arms:
        if 'DBE' in nm:
            rejected = True
            probs.append('DBE arm in the output folder (allowed input = SBE only) - not read')
    if unknown:
        incomplete = True
        probs.append('output folder has %d unexpected entr(y/ies) (not read)' % len(unknown))
    # ---- receipt ----
    receipt, rdoc = {k: missing('no receipt') for k, _p, _k in RECEIPT_FIELDS}, None
    rp = os.path.join(out, 'run_receipt.json')
    if os.path.isfile(rp) and not os.path.islink(rp):
        rdoc, why = load_json(rp)
        if isinstance(rdoc, dict):
            receipt = read_table(rdoc, RECEIPT_FIELDS)
            receipt['receipt_sha256'] = sha256_file(rp)
            receipt['receipt_has_arm_list'] = 'arm_list' in rdoc
        else:
            rdoc = None
            probs.append('run_receipt.json ' + (why or 'is not an object'))
            incomplete = True
    else:
        probs.append('run_receipt.json missing')
        incomplete = True
    if receipt.get('receipt_arms') not in (1,) and not is_missing(receipt.get('receipt_arms')):
        incomplete = True
        probs.append('receipt arms is not 1 (the probe is one arm)')
    if receipt.get('receipt_has_arm_list'):
        incomplete = True
        probs.append('receipt has an arm list (the probe is arm 0 only)')
    rep['receipt'] = receipt
    # ---- meta / env / samples / log (watcher's log folder) ----
    meta, env, rows, log, flt, marks = None, None, None, None, [], {}
    if args.logdir:
        meta, mp = parse_meta(os.path.join(args.logdir, 'meta.txt'))
        probs += mp
        if meta is None:
            incomplete = True
        env = parse_env(os.path.join(args.logdir, 'env.txt'))
        if env is None:
            probs.append('env.txt unreadable')
            incomplete = True
        rows, sp = parse_samples(os.path.join(args.logdir, 'samples.tsv'))
        if sp:
            probs.append(sp)
            incomplete = True
        log, flt, marks, lp, seal_broken = parse_log(os.path.join(args.logdir, 'runner.log'))
        probs += lp
        if log is None:
            incomplete = True
        if seal_broken:
            rejected = True
    rep['meta'] = meta if meta is not None else ({} if not args.logdir else missing('meta.txt unreadable'))
    rep['attempt'] = (meta or {}).get('attempt', missing('absent')) if args.logdir else missing('not requested')
    rep['env'] = env if env is not None else ({} if not args.logdir else missing('env.txt unreadable'))
    start = (meta or {}).get('start_epoch')
    # ---- which arm file ----
    source, arm_path = 'none', None
    if not rejected:
        if len(arms) > 1:
            incomplete = True
            probs.append('more than one arm file in the output folder (%d) - none read' % len(arms))
        elif len(arms) == 1:
            nm = arms[0]
            m = re.fullmatch(ARM_RE, nm)
            if not nm.startswith(KIT_ARM_PREFIX) or not m:
                incomplete = True
                probs.append('arm file name is not an SBE probe arm name - not read')
            elif m.group(1) != '0':
                incomplete = True
                probs.append('arm index is not 0 - not read')
            else:
                source, arm_path = 'outdir', os.path.join(out, nm)
    # ---- kit run folder: new files of this attempt (never opened except one failure leftover) ----
    knew = []
    if args.kit_run and os.path.isdir(args.kit_run):
        cands = []
        for nm in sorted(os.listdir(args.kit_run)):
            fp = os.path.join(args.kit_run, nm)
            if not (nm.startswith(KIT_ARM_PREFIX) or nm.startswith('.peak_rss_' + KIT_ARM_PREFIX)):
                continue
            if os.path.islink(fp) or not os.path.isfile(fp):
                continue
            if start is None or os.path.getmtime(fp) < start - 2:
                continue
            knew.append({'name': nm, 'size': os.path.getsize(fp), 'sha256': sha256_file(fp)})
            if re.fullmatch(KIT_ARM_PREFIX + r'[A-Za-z0-9_]+_a0\.json(\.failed)?', nm):
                cands.append(nm)
        if source == 'none' and not rejected and not arms:
            if len(cands) == 1:
                source = 'kit_run_failed' if cands[0].endswith('.failed') else 'kit_run_unmoved'
                arm_path = os.path.join(args.kit_run, cands[0])
            elif len(cands) > 1:
                incomplete = True
                probs.append('more than one leftover arm file in the kit run folder (%d) - none read' % len(cands))
    # byte copies kept by the watcher (the runner would overwrite same-named files on a later attempt)
    before = []
    if args.logdir:
        for x in knew:
            cp_ = os.path.join(args.logdir, 'kit_run_new', x['name'])
            x['copy_ok'] = bool(os.path.isfile(cp_) and not os.path.islink(cp_) and sha256_file(cp_) == x['sha256'])
        bd = os.path.join(args.logdir, 'kit_run_before')
        if os.path.isdir(bd) and not os.path.islink(bd):
            for nm in sorted(os.listdir(bd)):
                fp = os.path.join(bd, nm)
                if os.path.isfile(fp) and not os.path.islink(fp) and (nm.startswith(KIT_ARM_PREFIX) or nm.startswith('.peak_rss_' + KIT_ARM_PREFIX)):
                    before.append({'name': nm, 'size': os.path.getsize(fp), 'sha256': sha256_file(fp)})
    rep['kit_run_new_files'] = knew
    rep['kit_run_before_files'] = before
    rep['source'] = source
    # ---- arm fields (closed table) ----
    fields, sealed = no_arm_fields('no arm file'), set()
    if arm_path is not None:
        fields, sealed, ap = read_arm(arm_path)
        probs += ap
        rep['arm'] = {'file': os.path.basename(arm_path), 'size': os.path.getsize(arm_path), 'sha256': sha256_file(arm_path),
                      'index': 0}
    inp = fields.pop('_input_files', None)
    # S0 plan cross-checks (same bed, same tol_ff) - identity only
    if args.s0_plan:
        plan, why = load_json(args.s0_plan)
        if isinstance(plan, dict):
            rep['s0_plan_sha256'] = sha256_file(args.s0_plan)
            fields['bed_inputs_match_s0'] = bed_match(inp, plan) if arm_path is not None else missing('no arm file')
            tol_p = ((plan.get('values_um') or {}).get('tol_ff'))
            fnd, tol_r = pick(rdoc or {}, ('ca_ext_request', 'cjunc', 'tol_ff_um'))
            ok_t = isinstance(tol_p, float) and fnd and isinstance(tol_r, float)
            fields['tol_ff_matches_s0'] = (tol_p == tol_r) if ok_t else missing('absent')
        else:
            probs.append('S0 plan ' + (why or 'is not an object'))
            incomplete = True
            fields['bed_inputs_match_s0'] = missing('S0 plan unreadable')
            fields['tol_ff_matches_s0'] = missing('S0 plan unreadable')
    else:
        fields['bed_inputs_match_s0'] = missing('not requested')
        fields['tol_ff_matches_s0'] = missing('not requested')
    pin = (meta or {}).get('pin')
    cs = fields.get('code_sha')
    if pin and isinstance(cs, str):
        fields['code_matches_pin'] = ('+' not in cs) and pin.startswith(cs)
    else:
        fields['code_matches_pin'] = missing('not requested' if not args.logdir else 'absent')
    rep['fields'] = fields
    # ---- log / timing / resources ----
    timing, res = {}, {}
    if args.logdir:
        rep['log'] = log if log is not None else missing('runner.log unreadable')
        log = log or {}
        timing['wall_s'] = (meta or {}).get('wall_s', missing('absent'))
        timing['runner_rc'] = (meta or {}).get('runner_rc', missing('absent'))
        timing['step3_stage_s'] = log.get('done_step3_s', missing('absent'))
        timing['face_alpha_prep_s'] = log.get('face_alpha_prep_s', missing('absent'))
        timing['cjunc_prep_s'] = log.get('cjunc_prep_s', missing('absent'))
        tmark = {}
        for name in ('arm_start', 'voxelize', 'solve', 'done', 'saved'):
            tmark[name] = first_time(rows, marks[name]) if (rows and name in marks) else None

        def span(a, b):
            return (tmark[b] - tmark[a]) if (tmark.get(a) is not None and tmark.get(b) is not None) else missing('absent')
        timing['pre_step3_s'] = (tmark['voxelize'] - start) if (tmark.get('voxelize') is not None and start) else missing('absent')
        timing['raster_prep_s'] = span('voxelize', 'solve')
        timing['cg_cert_s'] = span('solve', 'done')
        end = (meta or {}).get('end_epoch')
        if tmark.get('done') is not None:
            timing['solve_to_end_s'] = missing('result line present')
        elif tmark.get('solve') is not None and isinstance(end, int):
            timing['solve_to_end_s'] = end - tmark['solve']        # the run ended (or was stopped) before the result line
        else:
            timing['solve_to_end_s'] = missing('absent')
        timing['resolution_s'] = (meta or {}).get('sample_s', missing('absent'))
        ci, ri = fields.get('cg_iters'), fields.get('cert_resolve_iters')
        if isinstance(timing['cg_cert_s'], int) and isinstance(ci, int) and isinstance(ri, int) and (ci + ri) > 0:
            timing['cg_cert_s_per_iter'] = float(timing['cg_cert_s']) / float(ci + ri)
        else:
            timing['cg_cert_s_per_iter'] = missing('absent')
        if rows:
            res['n_samples'] = len(rows)
            for name, okey in (('rss_sum_kb', 'rss_sum_max_kb'), ('rss_proc_kb', 'rss_proc_max_kb'),
                               ('gpu_used_mib', 'gpu_used_max_mib'), ('gpu_ours_mib', 'gpu_ours_max_mib'),
                               ('gpu_util', 'gpu_util_max_pct')):
                v = col_max(rows, name)
                res[okey] = v if v is not None else missing('no sample')
            g0 = rows[0][SAMPLE_COLS.index('gpu_used_mib')]
            res['gpu_used_first_mib'] = g0 if g0 is not None else missing('no sample')
        res['runner_peak_rss_gb'] = log.get('runner_peak_rss_gb', missing('absent'))
        tv = parse_time_v(os.path.join(args.logdir, 'time_v.txt'))
        res['time_v_max_rss_kb'] = (tv or {}).get('max_rss_kb', missing('absent'))
        res['time_v_elapsed_s'] = (tv or {}).get('elapsed_s', missing('absent'))
        atv = None
        for x in knew:
            if x['name'].startswith('.peak_rss_'):
                atv = parse_time_v(os.path.join(args.kit_run, x['name']))
        res['arm_time_v_max_rss_kb'] = (atv or {}).get('max_rss_kb', missing('absent'))
        res['arm_time_v_elapsed_s'] = (atv or {}).get('elapsed_s', missing('absent'))
        res['cap_gb'] = (meta or {}).get('cap_gb', missing('absent'))
        res['cap_term'] = (meta or {}).get('cap_term', missing('absent'))
    rep['timing'] = timing
    rep['resources'] = res
    # ---- leak tripwire: no emitted float may equal a sealed number of the arm ----
    emitted = [(k, v) for k, v in fields.items() if isinstance(v, float)] + \
              [(k, v) for k, v in timing.items() if isinstance(v, float)]
    for k, v in emitted:
        if v in sealed:
            rejected = True
            fields[k] = missing('withheld (tripwire)')
            probs.append('LEAK_TRIPWIRE: emitted key %s equals a sealed number (withheld)' % k)
    # ---- verdict ----
    f = fields
    rc = RC_OK
    if rejected:
        rc = RC_REJECTED
    else:
        miss = [k for k in REQUIRED if is_missing(f.get(k))]
        st = f.get('cert_status')
        said_unconverged = (f.get('unconverged') is True or f.get('cert_ok') is False
                            or f.get('electronic_status') == 'unconverged'
                            or (isinstance(f.get('cg_info'), int) and f.get('cg_info') != 0))
        if isinstance(st, str) and st != 'POSITIVE_SOLVED':
            rc = RC_NOT_CONVERGED
            probs.append('certificate status is not POSITIVE_SOLVED (no clean positive solve)')
        elif miss and said_unconverged:
            rc = RC_NOT_CONVERGED
            probs.append('not converged (the arm says so); required key(s) missing as well: ' + ' '.join(miss))
        elif miss:
            rc = RC_INCOMPLETE
            probs.append('required key(s) missing: ' + ' '.join(miss))
        else:
            conv = True
            if f.get('unconverged') is not False:
                conv = False
            if f.get('cg_info') != 0 or f.get('cert_ok') is not True or f.get('cert_resolve_info') != 0:
                conv = False
            if not (f.get('cert_pass_a') is True and f.get('cert_pass_b') is True and f.get('cert_pass_c') is True
                    and f.get('cert_pass_d') is True):
                conv = False
            if f.get('electronic_status') != 'complete':
                conv = False
            if not conv:
                rc = RC_NOT_CONVERGED
                probs.append('not converged (unconverged / cg_info / certificate flags / component status)')
        if rc == RC_OK:
            miss_ok = [k for k in REQUIRED_OK if is_missing(f.get(k))]
            if miss_ok:
                incomplete = True
                probs.append('required key(s) missing: ' + ' '.join(miss_ok))
            if f.get('cg_iters') != f.get('cert_iters'):
                incomplete = True
                probs.append('cg_iters and the certificate iteration count differ')
            if f.get('origin_shift_zero') is not True:
                incomplete = True
                probs.append('arm origin shift is not zero (not arm 0)')
            # identity: with a log folder and an S0 plan the three checks must be True (no evidence = not OK)
            idreq = bool(args.logdir and args.s0_plan and arm_path is not None)
            if f.get('bed_inputs_match_s0') is False or (idreq and f.get('bed_inputs_match_s0') is not True):
                incomplete = True
                probs.append('arm input digests are not shown to match the S0 stage-1 plan (not the same bed, or no evidence)')
            if f.get('tol_ff_matches_s0') is False or (idreq and f.get('tol_ff_matches_s0') is not True):
                incomplete = True
                probs.append('receipt tol_ff is not shown to match the S0 stage-1 plan')
            if f.get('code_matches_pin') is False or (idreq and f.get('code_matches_pin') is not True):
                incomplete = True
                probs.append('arm code sha is not shown to be the pin (other commit, dirty tree, or no evidence)')
            if source != 'outdir':
                incomplete = True
                probs.append('the arm was not accepted by the runner (leftover in the kit run folder)')
            eb, rb = f.get('electronic_backend_used'), receipt.get('receipt_expect_backend')
            if isinstance(rb, str) and eb != rb:
                incomplete = True
                probs.append('solve backend differs from the receipt expectation')
            if args.logdir:
                rc_run = (meta or {}).get('runner_rc')
                if rc_run is None:
                    incomplete = True
                    probs.append('runner rc unknown')
                elif rc_run != 0:
                    incomplete = True
                    probs.append('runner rc is not 0')
                if log.get('skip_cached'):
                    incomplete = True
                    probs.append('the runner reused a cached arm (no fresh solve in this attempt)')
                for key in ('done_step3_s',):
                    if key not in log:
                        incomplete = True
                        probs.append('runner log has no STEP3 result line (time unknown)')
                # registered values (the watcher writes what it set into meta) and a clean watcher record
                m_ = meta or {}
                if not isinstance(m_.get('maxiter'), int) or log.get('cg_maxiter') != m_.get('maxiter'):
                    incomplete = True
                    probs.append('runner log CG maxiter differs from the meta maxiter (or one is missing)')
                xr = _num(m_['expect_rtol']) if isinstance(m_.get('expect_rtol'), str) else None
                if xr is None or receipt.get('receipt_step3_rtol') != xr or f.get('cert_rtol_used') != xr:
                    incomplete = True
                    probs.append('receipt / certificate rtol differs from the meta expect_rtol (or one is missing)')
                xb = m_.get('expect_backend')
                if not isinstance(xb, str) or rb != xb or eb != xb or f.get('backend_used') != xb:
                    incomplete = True
                    probs.append('solve backend differs from the meta expect_backend (or one is missing)')
                for key, want in (('aborted', 0), ('cap_term', 0), ('git_lines_after', 0), ('orphans', 0),
                                  ('kit_run_matches_s0', 1), ('solve_started', 1)):
                    if m_.get(key) != want:
                        incomplete = True
                        probs.append('meta %s is not %d (or missing)' % (key, want))
            if incomplete:
                rc = RC_INCOMPLETE
    rep['verdict'], rep['rc'], rep['problems'], rep['notes'] = VERDICT[rc], rc, probs, notes
    return rep, flt


def screen(rep):
    L = []
    L.append('[probe6] verdict %s (rc %d)   source %s   scope %s   attempt %s'
             % (rep['verdict'], rep['rc'], rep['source'], rep['scope'], fmt(rep.get('attempt', missing('absent')))))
    arm = rep.get('arm') or {}
    if arm:
        L.append('[probe6] arm %s  size %d  sha256 %s' % (arm.get('file'), arm.get('size'), arm.get('sha256')))
    L.append('[probe6] --- solver (arm JSON, closed allowlist) ---')
    for row in ARM_FIELDS:
        L.append('[probe6] %-26s = %s' % (row[0], fmt(rep['fields'].get(row[0]))))
    for k in ('backend_fallback', 'origin_shift_zero', 'bed_inputs_match_s0', 'tol_ff_matches_s0', 'code_matches_pin'):
        L.append('[probe6] %-26s = %s' % (k, fmt(rep['fields'].get(k))))
    if rep['scope'] == 'outdir_and_logdir':
        lg = rep.get('log') if isinstance(rep.get('log'), dict) and not is_missing(rep.get('log')) else {}
        L.append('[probe6] --- runner log (re-rendered) ---')
        for k in ('solve_n_dof', 'solve_plate_bot', 'solve_plate_top', 'solve_backend', 'cg_maxiter', 'cg_rtol', 'done_n_dof',
                  'done_resid', 'done_step3_s', 'sealed', 'face_alpha_prep_s', 'cjunc_prep_s', 'not_converged_info',
                  'not_converged_resid', 'cert_fail_status', 'cert_fail_imbalance', 'skip_cached', 'saved', 'n_lines'):
            if k in lg:
                L.append('[probe6] %-26s = %s' % (k, fmt(lg[k])))
        L.append('[probe6] %-26s = %d (%d dropped from the middle; digits masked; see the report)'
                 % ('masked_failure_lines', len(lg.get('masked_lines') or []), lg.get('masked_lines_dropped') or 0))
        L.append('[probe6] --- time (s) ---')
        for k in ('wall_s', 'runner_rc', 'pre_step3_s', 'raster_prep_s', 'cg_cert_s', 'resolution_s', 'cg_cert_s_per_iter',
                  'solve_to_end_s', 'step3_stage_s', 'face_alpha_prep_s', 'cjunc_prep_s'):
            L.append('[probe6] %-26s = %s' % (k, fmt(rep['timing'].get(k, missing('absent')))))
        L.append('[probe6] --- memory ---')
        for k in sorted(rep['resources']):
            L.append('[probe6] %-26s = %s' % (k, fmt(rep['resources'][k])))
        L.append('[probe6] --- environment / identity ---')
        for src in ('env', 'meta'):
            d = rep.get(src) if isinstance(rep.get(src), dict) and not is_missing(rep.get(src)) else {}
            for k in sorted(d):
                L.append('[probe6] %-26s = %s' % (k, d[k]))
    L.append('[probe6] --- receipt / folder ---')
    for k in sorted(rep['receipt']):
        L.append('[probe6] %-26s = %s' % (k, fmt(rep['receipt'][k])))
    fo = rep['folder']
    L.append('[probe6] folder %s  files %s' % (fo.get('path'), fo.get('n_files')))
    L.append('[probe6] folder sha256 (name size sha256 listing) = %s' % fo.get('listing_sha256'))
    L.append('[probe6] folder sha256 (sha256sum style)          = %s' % fo.get('sha256sum_style'))
    for x in rep.get('kit_run_new_files') or []:
        L.append('[probe6] kit run new file %s  size %d  sha256 %s  copy_ok %s' % (x['name'], x['size'], x['sha256'], x.get('copy_ok')))
    for x in rep.get('kit_run_before_files') or []:
        L.append('[probe6] kit run earlier file (copied before the start) %s  size %d  sha256 %s' % (x['name'], x['size'], x['sha256']))
    L.append('[probe6] held back (names only): ' + ' '.join(rep['held_back']))
    for p in rep['problems']:
        L.append('[probe6] problem: ' + p)
    return L


def main(argv=None):
    ap = argparse.ArgumentParser(description='value-blind reader for the Rint 2 probe 6 output (closed allowlist)')
    ap.add_argument('--outdir', required=True, help='runner output folder (one arm)')
    ap.add_argument('--logdir', default='', help="watcher log folder (meta.txt, runner.log, samples.tsv, env.txt)")
    ap.add_argument('--kit-run', default='', help='kit run folder (new leftover files of this attempt)')
    ap.add_argument('--s0-plan', default='', help='S0 stage-1 plan (cjunc_plan.json) for the same-bed check')
    ap.add_argument('--report', default='', help='report path (default: <logdir>/probe6_report.json)')
    ap.add_argument('--filtered-log', default='', help='filtered log path (default: <logdir>/runner_filtered.log)')
    args = ap.parse_args(argv)
    if not args.logdir and not args.report:
        ap.error('give --logdir or --report')
    report = args.report or os.path.join(args.logdir, 'probe6_report.json')
    filtered = args.filtered_log or (os.path.join(args.logdir, 'runner_filtered.log') if args.logdir else '')
    try:
        rep, flt = run(args)
    except Exception as e:                                  # noqa: BLE001 - never print exception text (it may carry data)
        tb = sys.exc_info()[2]
        while tb is not None and tb.tb_next is not None:
            tb = tb.tb_next
        print('[probe6] READER_CRASH %s at line %s (no value printed)' % (type(e).__name__, tb.tb_lineno if tb else '?'))
        return RC_INCOMPLETE
    rc, why = rep['rc'], None
    try:
        text = json.dumps(rep, indent=1, sort_keys=True, ensure_ascii=True, allow_nan=False)
        with open(report, 'w', encoding='ascii') as f:
            f.write(text + '\n')
        if filtered:
            with open(filtered, 'w', encoding='utf-8') as f:
                f.write(''.join(ln + '\n' for ln in flt))
    except (OSError, ValueError) as e:                         # full disk, read-only folder ... : never a traceback
        why, rc = type(e).__name__, RC_INCOMPLETE
    for ln in screen(rep):
        print(ln.encode('ascii', 'replace').decode('ascii'))
    if why:
        print('[probe6] READER_CRASH %s while writing the report or the filtered log (no value printed) - rc 4' % why)
    return rc


if __name__ == '__main__':
    sys.exit(main())
