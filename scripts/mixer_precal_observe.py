#!/usr/bin/env python3
"""Unregistered precal observation adapter. Read-only; never authorizes a run.

Qualification of every selected run/reference frame precedes all metric calls.
Legacy sealed readers are reused for metrics without schema rewriting or globals.
"""
import argparse
import hashlib
import json
import math
import os
import re
from pathlib import Path
import stat
import sys

import numpy as np

# Capture the executing module code before any research-module import. Equality
# proves these recorded bytes compile to this code, not a unique historical text.
_EXECUTING_CODE = sys._getframe().f_code
import builtins
import io
import types

_DEPENDENCIES = ('mixer_precal_prepare', 'mixer_contact_reader',
                 'measure_mixing_index', 'measure_bed_aspect', 'make_mixer_deck',
                 'mixer_deck_readback', 'mixer_deck_diff', 'make_mixer_resume')
_BOUND_RAW, _BOUND_PATHS, _REGISTRY = {}, {}, {}
_BOOT_ERROR = None
_REAL_IMPORT = builtins.__import__
_REAL_OPEN = builtins.open


def _capture_source(path):
    first = path.lstat()
    if not stat.S_ISREG(first.st_mode):
        raise ValueError('source must be regular non-symlink: '+str(path))
    raw = path.read_bytes()
    last = path.lstat()
    fields = ('st_dev','st_ino','st_size','st_mtime_ns','st_ctime_ns','st_mode')
    if any(getattr(first,k) != getattr(last,k) for k in fields):
        raise ValueError('source changed during capture: '+str(path))
    return raw


def _private_import(name, globals=None, locals=None, fromlist=(), level=0):
    if level == 0 and name in _DEPENDENCIES:
        return _load_private(name)
    return _REAL_IMPORT(name, globals, locals, fromlist, level)


def _source_open(name):
    def source_open(file, mode='r', *args, **kwargs):
        try:
            own = os.path.abspath(os.fspath(file)) == _BOUND_PATHS[name]
        except TypeError:
            own = False
        if own:
            if mode not in ('r','rt','rb'):
                raise ValueError('bound module source is read-only')
            stream = io.BytesIO(_BOUND_RAW[name])
            if mode == 'rb':return stream
            # These sealed modules use encoding= explicitly for textual reads.
            return io.TextIOWrapper(stream, encoding=kwargs.get('encoding') or 'utf-8',
                                    errors=kwargs.get('errors'), newline=kwargs.get('newline'))
        return _REAL_OPEN(file, mode, *args, **kwargs)
    return source_open


def _load_private(name):
    if name in _REGISTRY:return _REGISTRY[name]
    module = types.ModuleType(name)
    module.__file__ = _BOUND_PATHS[name]
    module.__package__ = ''
    local_builtins = dict(vars(builtins))
    local_builtins.update(__import__=_private_import, open=_source_open(name))
    module.__dict__['__builtins__'] = local_builtins
    _REGISTRY[name] = module
    exec(compile(_BOUND_RAW[name], module.__file__, 'exec',
                 dont_inherit=True, optimize=sys.flags.optimize), module.__dict__)
    return module


try:
    _self_path = Path(__file__).absolute()
    _BOUND_PATHS['mixer_precal_observe'] = str(_self_path)
    _BOUND_RAW['mixer_precal_observe'] = _capture_source(_self_path)
    if compile(_BOUND_RAW['mixer_precal_observe'], _EXECUTING_CODE.co_filename,
               'exec', dont_inherit=True, optimize=sys.flags.optimize) != _EXECUTING_CODE:
        raise ValueError('recorded observer bytes do not compile to executing module code')
    for _name in _DEPENDENCIES:
        _path = _self_path.parent/(_name+'.py')
        _BOUND_PATHS[_name] = str(_path)
        _BOUND_RAW[_name] = _capture_source(_path)
    for _name in _DEPENDENCIES:_load_private(_name)
    preparation = _REGISTRY['mixer_precal_prepare']
    contact = _REGISTRY['mixer_contact_reader']
    mixing = _REGISTRY['measure_mixing_index']
    bed = _REGISTRY['measure_bed_aspect']
    frames = bed.frames
except Exception as _error:
    _BOOT_ERROR = str(_error)
_BOUND_DIGESTS = {name: hashlib.sha256(raw).hexdigest() for name, raw in _BOUND_RAW.items()}

SCHEMA = 'mixer_precal_observe/1'
GRIDS = ((16, 4), (12, 3), (8, 2))
PHASES = ('AM_P', 'AM_S', 'SE')


class Tech(ValueError):
    pass


class Undefined(ValueError):
    pass


def validate_case(case_id, deck, meta):
    # Lazy import permits the small unit fixtures to isolate the observation
    # layer; production always calls the actual independent preparation contract.
    return preparation.validate_case(case_id, deck, meta)


def _need(ok, reason):
    if not ok:
        raise Tech(reason)


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _strict_json(raw):
    def pairs(items):
        out = {}
        for k, v in items:
            _need(k not in out, 'duplicate metadata key: '+k)
            out[k] = v
        return out
    def constant(value):
        raise Tech('nonfinite JSON token')
    value = json.loads(raw.decode('utf-8'), object_pairs_hook=pairs, parse_constant=constant)
    _need(isinstance(value, dict), 'metadata must be object')
    return value


def _stamp(st):
    return st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns, st.st_mode


def _read(path, sources):
    path = Path(path)
    first = path.lstat()
    _need(stat.S_ISREG(first.st_mode), 'input must be regular non-symlink file: '+str(path))
    raw = path.read_bytes()
    _need(_stamp(first) == _stamp(path.lstat()), 'input changed during read: '+str(path))
    digest = _sha(raw)
    if str(path) in sources:
        _need(sources[str(path)] == digest, 'input changed: '+str(path))
    sources[str(path)] = digest
    return raw


def _present(path):
    # lstat includes dangling symlinks; only ENOENT is absence.
    try:
        Path(path).lstat()
        return True
    except FileNotFoundError:
        return False


def _verify_bound():
    _need(_BOOT_ERROR is None, 'source bootstrap failed: '+str(_BOOT_ERROR))
    for name, raw in _BOUND_RAW.items():
        _need(_capture_source(Path(_BOUND_PATHS[name])) == raw,
              'bound source changed: '+name)


def _verify_sources(sources, listings, optional):
    _verify_bound()
    for path, present in optional.items():
        _need(_present(path) == present, 'optional input presence changed: '+path)
    for path, digest in list(sources.items()):
        _need(_sha(_read(path, {})) == digest, 'input changed after qualification: '+path)
    for directory, names in listings.items():
        _need(_listing(Path(directory)) == names, 'frame set changed: '+directory)


def _listing(post):
    _need(post.is_dir() and not post.is_symlink(), 'post must be non-symlink directory')
    return [(s, str(p)) for s, p in frames(str(post))]


def _check_binding(B, case_id):
    _need(B['case_id'] == case_id, 'case identity mismatch')
    _need(B['role'] in ('U', 'C', 'N0', 'E0'), 'unsupported role')
    _need(set(B['phases']) == set(PHASES), 'three phases required')
    _need([B['phases'][p]['type'] for p in PHASES] == [1, 2, 3], 'M requires three-phase type map 1/2/3')
    _need(B['axis'] == 'x' and B['np_proposed'] == 20, 'unsupported axis/NP proposal')
    _need(type(B['n_planned']) is int and B['n_planned'] > 0, 'invalid planned atom count')
    _need(set(B['expected_counts']) == {'1', '2', '3'}, 'missing planned phase counts')
    _need(all(type(v) is int and v >= 0 for v in B['expected_counts'].values()), 'invalid planned phase counts')
    _need(sum(B['expected_counts'].values()) == B['n_planned'], 'planned counts disagree')
    _need(B['revolutions'] == (0 if B['role'] == 'E0' else 2), 'only E0 t0 or rotating bin1 supported')
    _need(math.isfinite(B['r_container']) and B['r_container'] > 0, 'invalid declared drum radius')
    _need(B['geometry']['r_container'] == B['r_container'] and B['geometry']['axis'] == B['axis'], 'geometry binding disagrees')
    for p in PHASES:
        r = B['phases'][p]['radius_m']
        _need(math.isfinite(r) and r > 0, 'invalid actual template radius')
    pm = B['frame_pm']
    for key in ('phases', 'n_planned', 'revolutions', 'seed'):
        _need(pm[key] == B[key], 'frame_pm disagrees: '+key)
    _need(pm['n_expected_file'] is None, 'unexpected frame_pm n_expected override')


def qualify_arrays(arrays, B):
    """D13: planned minus initial observed 0..10; initial IDs 1..N;
    later ID/type/radius unchanged. No planned count is rewritten.
    Returns the planned/observed count record; no metrics are computed.
    """
    _need(bool(arrays), 'no qualified arrays')
    ref = None
    initial_counts = None
    for D in arrays:
        _need(all(k in D for k in ('id', 'type', 'radius', 'x', 'y', 'z')), 'missing dump columns')
        A = {k: np.asarray(D[k], dtype=float) for k in ('id', 'type', 'radius', 'x', 'y', 'z')}
        _need(all(a.ndim == 1 for a in A.values()), 'non-vector dump column')
        n = len(A['id'])
        _need(n > 0 and all(len(a) == n and np.isfinite(a).all() for a in A.values()), 'empty, nonfinite or mismatched dump arrays')
        for key in ('id', 'type'):
            a = A[key]
            _need(np.equal(a, np.floor(a)).all() and (a >= 1).all() and (a <= 2**53-1).all(), 'invalid integer '+key)
        ids, types = A['id'].astype(np.int64), A['type'].astype(np.int64)
        order = np.argsort(ids, kind='stable')
        _need(np.array_equal(ids[order], np.arange(1, n+1)), 'D13 IDs must be unique contiguous 1..observed N')
        _need(set(types.tolist()) <= {1, 2, 3}, 'unknown phase type')
        radii = A['radius']
        _need((radii > 0).all(), 'nonpositive radius')
        hr = contact.half_width(radii, contact.sigfigs_effective(radii))
        for p in PHASES:
            t, r = B['phases'][p]['type'], B['phases'][p]['radius_m']
            _need((np.abs(radii[types == t]-r) <= hr[types == t]+1e-12*r).all(), 'dump radius differs from actual template: '+p)
        if ref is None:
            _need(0 <= B['n_planned']-n <= 10, 'D13 initial missing count outside 0..10')
            initial_counts = {str(t): int((types == t).sum()) for t in (1, 2, 3)}
            ref = (ids[order], types[order], radii[order])
        else:
            _need(all(np.array_equal(a, b) for a, b in zip(ref, (ids[order], types[order], radii[order]))), 'later ID/type/radius changed')
    return dict(planned_total=B['n_planned'], observed_total=len(ref[0]),
                initial_missing=B['n_planned']-len(ref[0]), planned_by_type=dict(B['expected_counts']),
                observed_by_type=initial_counts, rule='D13 initial missing <=10; IDs 1..N; subsequent ID/type/radius unchanged')


def qualify_reference(B, R):
    _need(R['case_id'] == 'PRECAL_E0' and R['role'] == 'E0' and R['revolutions'] == 0, 'reference must be qualified PRECAL_E0, not rotating N0')
    for key in ('seed', 'density_generation', 'geometry', 'phases', 'n_planned', 'expected_counts', 'axis', 'np_proposed'):
        _need(B[key] == R[key], 'E0 reference differs: '+key)


def _parse_dump(raw, step):
    """Parse exactly the hashed bytes, never reopen the source pathname."""
    lines = raw.decode('utf-8').splitlines()
    _need(len(lines) >= 9, 'short dump header')
    _need(lines[0] == 'ITEM: TIMESTEP' and lines[1] == str(step), 'dump timestep mismatch')
    _need(lines[2] == 'ITEM: NUMBER OF ATOMS' and re.fullmatch(r'[0-9]+', lines[3]), 'invalid atom count header')
    n = int(lines[3])
    _need(lines[4].startswith('ITEM: BOX BOUNDS '), 'missing box header')
    for line in lines[5:8]:
        bounds = [float(x) for x in line.split()]
        _need(len(bounds) == 2 and all(math.isfinite(x) for x in bounds) and bounds[0] < bounds[1], 'invalid orthogonal bounds')
    _need(lines[8].startswith('ITEM: ATOMS '), 'missing atom header')
    cols = lines[8].split()[2:]
    _need(len(set(cols)) == len(cols) and set(('id','type','x','y','z','radius')) <= set(cols), 'duplicate/missing columns')
    rows = [line.split() for line in lines[9:] if line.strip()]
    _need(n > 0 and len(rows) == n and all(len(row) == len(cols) for row in rows), 'dump row/count mismatch')
    A = np.asarray(rows, dtype=float)
    _need(np.isfinite(A).all(), 'nonfinite dump value')
    return {key: A[:, i] for i, key in enumerate(cols)}


def _frozen_plan(deck, B, listing):
    D = preparation.rb.read_deck(deck.decode('utf-8'))
    runs, dt, period, de = D['runs'], D['dt'], D['period'], D['dump_every']
    _need(len(runs) == 4 and runs[0] == 1 and runs[1] == runs[2] and runs[1] > 0 and runs[3] >= 0, 'fresh four-run structure required')
    _need(dt is not None and period is not None and math.isfinite(dt) and math.isfinite(period) and dt > 0 and period > 0 and type(de) is int and de > 0, 'invalid frame plan')
    spr = period / dt
    revs = int(round(runs[-1] / spr))
    _need(revs == B['revolutions'] and ((runs[-1] == 0) == (B['role'] == 'E0')), 'rotation plan mismatch')
    plan = dict(steps_fill=runs[1], dump_every=de, dt=dt, steps_per_rev=spr,
                steps_run=runs[-1], steps_total=sum(runs), n_run_lines=4)
    t0 = mixing.planned_t0(plan)
    _need(t0 > runs[0] and B['frame_pm']['meta_steps'] == dict(t0_planned=t0,dump_every=de), 'metadata frame plan mismatch')
    cur = {}
    for step, path in listing:cur.setdefault(step, []).append(path)
    _need(len(cur.get(t0, [])) == 1, 'missing/duplicate t0')
    lat = []
    if B['role'] != 'E0':
        lat = [step for step in range(t0, sum(runs)+1, de) if mixing.bin_of(step,t0,spr) == 1]
        actual = {step for step in cur if step >= t0 and mixing.bin_of(step,t0,spr) == 1}
        _need(bool(lat) and actual == set(lat) and all(len(cur[step]) == 1 for step in lat), 'missing/duplicate/off-lattice bin1 frame')
    return dict(mode='t0_only' if B['role']=='E0' else 'rot2', plan=plan, n_revs=revs,
                t0_step=t0,t0_path=cur[t0][0],bin_steps=lat,bin_paths=[cur[x][0] for x in lat],runs=runs)


# Completion-log forms of the sealed build (LIGGGHTS-PUBLIC 3.8.0, git 3d5c00f), registration
# draft 7-4 / Q5.  Each form below is read from same-build logs committed in this repository:
#  * the fixed deck line `thermo_style custom step atoms ke c_rke vol` is headed
#    `Step Atoms KinEng rke Volume` (the build drops the c_ prefix) and every Loop line ends with
#    a ctime finish stamp (docs/data/mixer_highbo_devu_prelim_20261006/exact_runs/
#    exact_LU212_settled/log.exact L65-67, same thermo_style line);
#  * fix insert/pack writes its two-line insertion report (fix_insert.cpp print_stats_during)
#    inside the thermo table of the run in which it inserts, right after that table's setup row
#    (docs/data/kg50_d07_end_20261105/kg50_d07_b50_log_ins1.liggghts L116-121);
#  * log.liggghts echoes every input line, comments included, so a deck comment quoting an
#    `ERROR:` message appears verbatim (planned decks L34/L50; kg50 logs).
# Only these forms are admitted.  Any other line inside a thermo table, any other ERROR word or
# line-start ERROR, a malformed Loop line, a nonfinite value or a drop of the thermo atom count
# stays TECH.
_THERMO_HEADER = re.compile(r'[ \t]*Step[ \t]+Atoms[ \t]+KinEng[ \t]+rke[ \t]+Volume[ \t]*')
_THERMO_ROW = re.compile(r'[ \t]*([0-9]+)[ \t]+([0-9]+)[ \t]+([^ \t]+)[ \t]+([^ \t]+)[ \t]+([^ \t]+)[ \t]*')
_THERMO_VALUE = re.compile(r'[-+]?(?:(?:[0-9]+\.?[0-9]*|\.[0-9]+)(?:[eE][-+]?[0-9]+)?|[nN][aA][nN]|[iI][nN][fF])')
_LOOP_LINE = re.compile(r'Loop time of [-+.0-9eE]+ on ([0-9]+) procs for ([0-9]+) steps with ([0-9]+) atoms, '
                        r'finish time [A-Z][a-z]{2} [A-Z][a-z]{2} [ 0-9][0-9] [0-9]{2}:[0-9]{2}:[0-9]{2} [0-9]{4}[ \t]*')
_INSERT_REPORT = re.compile(r'INFO: Particle insertion ([^ \t:]+): inserted ([0-9]+) particle templates '
                            r'\(mass ([^ \t)]+)\) at step ([0-9]+)[ \t]*')
_INSERT_TOTAL = re.compile(r' - a total of ([0-9]+) particle templates \(mass ([^ \t)]+)\) inserted so far\.[ \t]*')
_ERROR_LINE = re.compile(r'\bERROR\b|^[ \t]*ERROR')


def _positive_value(text):
    return bool(_THERMO_VALUE.fullmatch(text)) and math.isfinite(float(text)) and float(text) > 0


def _deck_log_facts(deck):
    """Facts of the run's own deck that its completion log must match: full-line comments
    (with multiplicity; the build echoes each input line once) and, for each insert/pack fix,
    the index of the run in which it inserts (the run following its declaration)."""
    text = deck.decode('utf-8')
    comments = {}
    for line in text.split('\n'):
        if line.lstrip().startswith('#'):
            comments[line.rstrip()] = comments.get(line.rstrip(), 0)+1
    insert_run, runs_seen = {}, 0
    for _, tokens in preparation.rb.read_deck(text)['cmds']:
        if tokens[0] == 'run':
            runs_seen += 1
        elif tokens[0] == 'fix' and len(tokens) >= 4 and tokens[3] == 'insert/pack':
            _need(tokens[1] not in insert_run, 'insert/pack fix id repeated in deck')
            insert_run[tokens[1]] = runs_seen
    return dict(comment_lines=comments, insert_fix_run=insert_run)


def _log_contract(raw, runs, facts=None):
    """Fresh four-run completion log of the fixed deck.  Without deck facts no ERROR echo
    and no insertion report is admitted (strictest form)."""
    text = raw.decode('utf-8')
    facts = facts or dict(comment_lines={}, insert_fix_run={})
    lines = text.splitlines()
    echoes = {}
    for line in lines:
        if _ERROR_LINE.search(line):
            key = line.rstrip()
            echoes[key] = echoes.get(key, 0)+1
            _need(echoes[key] <= facts['comment_lines'].get(key, 0), 'error/resume log is not fresh completion evidence')
    _need(not re.search(r'RESUME_STEP|^\s*read_restart\b', text, re.M), 'error/resume log is not fresh completion evidence')
    # Fixed deck: make_mixer_deck.py thermo_style custom step atoms ke c_rke vol.
    # Accept only its named five-column thermo table, not arbitrary numeric text.
    loops, endpoints, procs, reports = [], [], [], []
    active, last, atoms, rows, report, expect = False, None, None, 0, None, None
    for line in lines:
        if line.isascii() and _THERMO_HEADER.fullmatch(line):
            _need(not active, 'thermo header inside an unfinished table')
            active, last, rows = True, None, 0
            continue
        if line.startswith('Loop time of'):
            loop = _LOOP_LINE.fullmatch(line)
            _need(loop is not None, 'malformed Loop line')
            _need(active and last is not None, 'Loop lacks a qualified thermo table')
            _need(report is None and expect is None, 'insertion report without its thermo row')
            loops.append(int(loop.group(2)))
            endpoints.append(last)
            procs.append(int(loop.group(1)))
            _need(len(loops) <= len(runs) and loops[-1] == runs[len(loops)-1]
                  and last == sum(runs[:len(loops)]), 'Loop/thermo cumulative run endpoint mismatch')
            _need(int(loop.group(3)) == atoms, 'Loop atom count differs from the last thermo row')
            active, last = False, None
            continue
        if not active or not line.strip(' \t'):
            continue
        _need(line.isascii(), 'non-ASCII line inside thermo table')
        if report is not None:
            total = _INSERT_TOTAL.fullmatch(line)
            _need(total is not None and int(total.group(1)) == report['inserted']
                  and total.group(2) == report['mass'], 'incomplete or inconsistent insertion report')
            report = None
            continue
        info = _INSERT_REPORT.fullmatch(line)
        if info:
            fix, n, step = info.group(1), int(info.group(2)), int(info.group(4))
            _need(facts['insert_fix_run'].get(fix) == len(loops) and all(r['fix'] != fix for r in reports),
                  'insertion report of an undeclared, repeated or misplaced insert/pack fix')
            _need(rows == 1 and expect is None and step == last+1, 'insertion report is not at the first step of its run')
            _need(n > 0 and _positive_value(info.group(3)), 'invalid insertion report values')
            report = dict(fix=fix, inserted=n, step=step, mass=info.group(3))
            reports.append(report)
            expect = (step, atoms+n)
            continue
        row = _THERMO_ROW.fullmatch(line)
        _need(row is not None and all(_THERMO_VALUE.fullmatch(x) for x in row.groups()[2:]),
              'invalid five-column thermo row')
        _need(all(math.isfinite(float(x)) for x in row.groups()), 'nonfinite thermo row')
        step, count = int(row.group(1)), int(row.group(2))
        if expect is not None:
            _need(step >= expect[0] and count == expect[1], 'thermo atom count after insertion report differs from the report')
            expect = None
        _need(atoms is None or count >= atoms, 'thermo atom count decreased (lost particles)')
        last, atoms, rows = step, count, rows+1
    _need(loops == runs and not active, 'log fresh four-run completion mismatch')
    _need(sorted(r['fix'] for r in reports) == sorted(facts['insert_fix_run']),
          'declared insert/pack fix without its insertion report')
    return dict(status='MATCH', loop_steps=loops,last_thermo_step=endpoints[-1],
                thermo_endpoints=endpoints, loop_procs=procs,
                insertion_reports=[dict(fix=r['fix'], step=r['step'], inserted=r['inserted']) for r in reports],
                deck_comment_echo_error_lines=sum(echoes.values()),
                total_wall_time_banner='Total wall time' in text,
                limitation='completion log conditions only; not exitcode, MPI rank, host or same-execution certification; '
                           'line forms are those of same-build logs, not yet of an actual first8 log')


def _load(case_id, directory, sources, listings, optional):
    directory = Path(directory).absolute()
    _need(directory.is_dir() and not directory.is_symlink(), 'run directory must be non-symlink')
    ne = directory/'n_expected'
    optional[str(ne)] = _present(ne)
    deck = _read(directory/'in.mixer', sources)
    meta = _strict_json(_read(directory/'deck_meta.json', sources))
    B = validate_case(case_id, deck, meta)
    _check_binding(B, case_id)
    if optional[str(ne)]:
        raw = _read(ne, sources).decode('ascii').strip()
        _need(raw.isdigit() and int(raw) == B['n_planned'], 'n_expected differs from planned count')
    post = directory/'post'
    listings[str(post)] = _listing(post)
    fp = _frozen_plan(deck, B, listings[str(post)])
    log = _log_contract(_read(directory/'log.liggghts', sources), fp['runs'], _deck_log_facts(deck))
    todo = [(fp['t0_step'], fp['t0_path'])]+list(zip(fp['bin_steps'], fp['bin_paths']))
    arrays, used = [], []
    for step, path in todo:
        raw = _read(path, sources)
        digest = _sha(raw)
        D = _parse_dump(raw, step)
        arrays.append(D)
        used.append(dict(step=step, path=str(path), sha256=digest))
    counts = qualify_arrays(arrays, B)
    return dict(binding=B, frame_plan=fp, arrays=arrays, counts=counts, frames=used, completion_log=log)


def mixing_summary(c0, cR, stats_rows, steps):
    """Existing M=(S0-S)/(S0-SR), no clipping or theoretical denominator."""
    s0, sr = float(c0['s2']), float(cR['s2'])
    if not (math.isfinite(s0) and math.isfinite(sr) and s0 > sr):
        raise Undefined('M denominator S0-SR must be finite and positive')
    _need(len(stats_rows) == len(steps) and bool(stats_rows), 'empty or mismatched mixing window')
    rows = []
    for step, cs in zip(steps, stats_rows):
        value = (s0-float(cs['s2']))/(s0-sr)
        if not math.isfinite(value):
            raise Undefined('nonfinite M')
        rows.append(dict(step=int(step), M=value, **cs))
    values = np.array([r['M'] for r in rows])
    return dict(status='OK', S0=s0, SR=sr, t0_stats=c0, reference_t0_stats=cR,
                frames=rows, M_mean=float(values.mean()),
                M_sd=float(values.std(ddof=1)) if len(values)>1 else 0.,
                qc=mixing.qc_representativeness(rows),
                sd_note='frame SD only; not seed uncertainty; one-frame SD 0 follows existing convention')


def _metrics(run, ref):
    B, fp, arrays = run['binding'], run['frame_plan'], run['arrays']
    rows = [dict(step=int(step), **contact.frame_quantities(D, B['frame_pm']))
            for step, D in zip([fp['t0_step']]+fp['bin_steps'], arrays)]
    cq = dict(t0=rows[0], bin=(contact.bin_summary(rows[1:], fp['bin_steps']) if B['role']!='E0'
                             else dict(status='NOT_APPLICABLE', reason='E0 has t0 only')),
              observable_label='믹서 판독 전용 AM–SE 접촉 부착',
              attachment_definition='Instantaneous contact attachment; fractions use all SE atoms as denominator; not surface-area coverage.',
              attachment_note='AM_P and AM_S attachment fractions share the SE denominator and can overlap; their sum is not the union fraction.')
    grids = []
    for cells, axial in GRIDS:
        kw = dict(cells=cells, x_cells=axial, n_min=20, axis='x')
        cs = [mixing.cell_stats(D, B['r_container'], **kw) for D in arrays]
        if B['role'] == 'E0':
            item = dict(status='NOT_APPLICABLE', t0_stats=cs[0], reason='reference raw variance only; no self-normalized M')
        else:
            cr = mixing.cell_stats(ref['arrays'][0], B['r_container'], **kw)
            item = mixing_summary(cs[0], cr, cs[1:], fp['bin_steps'])
        grids.append(dict(grid=[cells,cells,axial], n_min=20, axis='x', r_container=B['r_container'], **item))
    return cq, dict(grids=grids, denominator='own t0 and qualified uniform zero-cohesion E0 t0; not theoretical Lacey')


def _clean(value):
    if isinstance(value, dict): return {str(k):_clean(v) for k,v in value.items()}
    if isinstance(value, (list, tuple)): return [_clean(v) for v in value]
    if isinstance(value, np.ndarray): return _clean(value.tolist())
    if isinstance(value, np.generic): return _clean(value.item())
    if isinstance(value, float) and not math.isfinite(value): return None
    return value


def analyse_run(case_id, run_dir, reference_dir=None):
    """Actual read-only entry. A local observation OK is never execution GO."""
    result = dict(schema=SCHEMA, case_id=case_id, status='TECH', reasons=[], registered=None,
                  execution_authorized=False, contact=None, mixing=None, counts=None, reference_counts=None,
                  provenance={}, limitations=['development observations only; no physical qualification',
                    'declared deck geometry, not measured STL geometry',
                    'NP20 is a proposal, not observed MPI rank verification',
                    'fresh-run first-eight observation only; no resume or bit-identical claim',
                    'observed phase allocation can differ from planned and affect observables',
                    'nonfinite auxiliary raw statistics serialize as null, never zero'])
    result['provenance']['module_sha256'] = {
        name: dict(path=_BOUND_PATHS[name], sha256=digest)
        for name, digest in _BOUND_DIGESTS.items()}
    result['provenance']['source_binding'] = (
        'private dependencies compiled from recorded bytes; observer recorded bytes '
        'compile to executing module code; not unique historical source-text proof')
    # Bootstrap failures must not evaluate contact exception classes before load.
    if _BOOT_ERROR is not None:
        result['reasons'] = ['source bootstrap failed: '+_BOOT_ERROR]
        return result
    sources, listings, optional = {}, {}, {}
    try:
        _verify_bound()
        run = _load(case_id, run_dir, sources, listings, optional)
        ref = None
        if run['binding']['role'] != 'E0':
            _need(reference_dir is not None, 'rotating case requires E0 reference')
            ref = _load('PRECAL_E0', reference_dir, sources, listings, optional)
            qualify_reference(run['binding'], ref['binding'])
        else:
            _need(reference_dir is None, 'E0 is a reference, not a rotating comparison')
        _verify_sources(sources, listings, optional)
        cq, mq = _metrics(run, ref)
        _verify_sources(sources, listings, optional)
        result.update(status='OK', contact=cq, mixing=mq, counts=run['counts'],
                      reference_counts=ref['counts'] if ref else None)
        result['provenance'].update(binding=run['binding'], frames=run['frames'],
                                    reference_frames=ref['frames'] if ref else [],
                                    reference_binding=ref['binding'] if ref else None,
                                    completion_log=run['completion_log'],
                                    reference_completion_log=ref['completion_log'] if ref else None)
    except (Undefined, contact.Undefined) as exc:
        result.update(status='UNDEFINED', reasons=[str(exc)])
    except (ValueError, OSError, TypeError, KeyError, IndexError, OverflowError, SystemExit, contact.Tech) as exc:
        result.update(status='TECH', reasons=[str(exc)])
    try:
        _verify_sources(sources, listings, optional)
    except (ValueError, OSError) as exc:
        result.update(status='TECH', reasons=[str(exc)])
    if result['status'] != 'OK':
        result.update(contact=None, mixing=None, counts=None, reference_counts=None)
    result['provenance']['input_sha256'] = dict(sources)
    result['provenance']['frame_listing_snapshot'] = dict(listings)
    result['provenance']['optional_presence_snapshot'] = dict(optional)
    return _clean(result)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', required=True)
    parser.add_argument('--run', required=True)
    parser.add_argument('--reference')
    args = parser.parse_args(argv)
    result = analyse_run(args.case, args.run, args.reference)
    print(json.dumps(result, ensure_ascii=False, allow_nan=False, sort_keys=True))
    return 0 if result['status']=='OK' else 2


if __name__=='__main__':sys.exit(main())
