#!/usr/bin/env python3
"""Fixed first-eight pre-calibration preparation, never a launcher.

Only in-memory synthetic deck generation and static checks occur here. Exact bytes
and metadata are bound to this source's fixed generator recipe. That comparison is
a *source-output oracle*, not an independent proof of the generator's physics.
Positive cases additionally use the existing independent D2 readback. Zero-CED
controls have a separate unregistered contract, reusing structural/count checks;
they are never relabelled as positive D2 cases. No simulator/STL/observed particles,
MPI rank, binary, job, current resources, calibration or execution is certified.

Python 3.8+. API calls do not write files. The CLI prints a static JSON report only.
"""
import argparse
import copy
import hashlib
import json
import math
import threading

import make_mixer_deck as gen
import mixer_deck_diff as diff
import mixer_deck_readback as rb


CASE_IDS = tuple('PRECAL_R1_B%d_%s' % (b, role)
                 for b in (1, 2, 3) for role in ('U', 'C')) + ('PRECAL_N0', 'PRECAL_E0')
PHASES = ('AM_P', 'AM_S', 'SE')
_BO = (0.21244, 21.244, 212.44)
_LOCK = threading.RLock()
_TEMP_ARM = 'PRECAL_PREP_GM'
BASELINE_SCHEMA = 'mixer_precal_baseline_meta/1'
BASELINE_CONTRACT = 'precal-first8-zero/unregistered'


def _need(ok, message):
    if not ok:
        raise ValueError(message)


def _case(case_id):
    _need(type(case_id) is str and case_id in CASE_IDS, 'case_id outside the fixed first eight')
    if case_id in CASE_IDS[-2:]:
        role = case_id.rsplit('_', 1)[-1]
        return role, 0., 0 if role == 'E0' else 2
    index = CASE_IDS.index(case_id)
    return case_id[-1], _BO[index // 2], 2


def _json_exact(value):
    """JSON-native, finite, type-sensitive equality (True is not 1)."""
    def check(v):
        if type(v) is dict:
            _need(all(type(k) is str for k in v), 'metadata keys must be strings')
            for x in v.values():
                check(x)
        elif type(v) is list:
            for x in v:
                check(x)
        elif type(v) is float:
            _need(math.isfinite(v), 'metadata contains a nonfinite number')
        else:
            _need(type(v) in (str, int, bool, type(None)), 'metadata must contain JSON-native values')
    try:
        check(value)
        return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)
    except (TypeError, OverflowError, RecursionError) as exc:
        raise ValueError('invalid metadata representation') from exc


def _generate(case_id):
    role, bo, revs = _case(case_id)
    # Serialize this adapter's temporary state. Unrelated users of the legacy
    # generator's globals must not mutate them concurrently with generation.
    with _LOCK:
        old_types = gen.TYPES
        registered = False
        try:
            gen.set_phases(PHASES)
            if role in ('U', 'C'):
                gamma = {p: (1. if p == 'SE' or role == 'C' else .1) for p in PHASES}
                arm = gen.gm_arm(gamma, gamma_wall=gen.gm_wall_from_ncm(.1), bo_se=bo,
                                 rho_uncoated_ncm=.1)
                gen.register_arm(_TEMP_ARM, arm)
                registered = True
                arm_name = _TEMP_ARM
            else:
                arm_name = 'L0' if role == 'N0' else 'E0'
            plan = gen.plan(100000, cgf=151.4, stiffen_se=20., dens_gen='lab20261014')
            rpm = gen.resolve_rpm(plan['R'], fr=.0827)
            options = dict(hold_bo_pairwise=True, dt_factor=1., dump_full_precision=True)
            text = gen.deck(plan, rpm, revs, seed=32452843, arm=arm_name, n_baffles=0, **options)
            meta = gen.deck_meta(plan, rpm, revs, 32452843, arm_name, text, **options)
            if role in ('N0', 'E0'):
                # Do not emit the old registered/schema1 claim for these new
                # lab-generation controls. The legacy generator stays unchanged.
                meta.update(schema=BASELINE_SCHEMA, registered=None,
                            development_contract=BASELINE_CONTRACT, control_role=role)
            return dict(case_id=case_id, role=role, deck=text.encode('utf-8'), meta=meta)
        except (SystemExit, AssertionError, TypeError, KeyError, OverflowError, ZeroDivisionError) as exc:
            raise ValueError('fixed recipe generation refused: ' + str(exc)) from exc
        finally:
            if registered:
                gen.ARMS.pop(_TEMP_ARM, None)
            gen.TYPES = old_types


def _parsed(deck):
    _need(type(deck) is bytes, 'deck must be physical bytes')
    _need(b'\r' not in deck, 'deck must be LF-only bytes')
    try:
        text = deck.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError('deck must be UTF-8') from exc
    parsed = rb.read_deck(text)
    _need(not parsed['problems'], 'deck structural parsing failed')
    # The legacy read_deck type inference is gen1-only. Assign the fixed map only
    # after canonical bytes/metadata binding; actual radii come from templates.
    parsed['names'] = {1: 'AM_P', 2: 'AM_S', 3: 'SE', 4: 'WALL'}
    return text, parsed


def _baseline(text, parsed, meta, role):
    _need(meta['schema'] == BASELINE_SCHEMA and meta['registered'] is None
          and meta['development_contract'] == BASELINE_CONTRACT and meta['control_role'] == role,
          'baseline must use the separate unregistered contract')
    _need(meta['cohesion_nonzero'] is False and all(x == 0. for x in parsed['ced'].values()),
          'baseline must have zero CED in every particle and wall pair')
    _need('adhesion_rule' not in meta, 'baseline is not a positive geomean case')
    commands = [t for _, t in parsed['cmds']]
    rb._d2_numeric_tokens(text)
    rb._d2_time_grammar(commands)
    rb._d2_contact_grammar(commands, 4)
    rb._d2_lifecycle(commands)
    density = rb.D2_DENSITY['lab20261014']
    counts = rb._d2_counts(parsed, meta, PHASES, density)
    rb._d2_text_form(text, meta)
    rb._d2_generator_form(commands, parsed, meta, parsed['names'], PHASES, density,
                          counts, 1, 151.4, 20.)
    inserts = [t for t in commands if t[0] == 'fix' and t[3] == 'insert/pack']
    _need(len(inserts) == (2 if role == 'N0' else 1), 'baseline insertion partition differs')
    _need((parsed['runs'][3] == 0) == (role == 'E0'), 'baseline rotation role differs')
    return counts


def validate_case(case_id, deck, meta):
    """Return a fresh observation binding, or raise ValueError; never a run GO.

    Geometry is from the printed STL scale under the generator's canonical
    0.5 m radius/0.2 m length convention, not a check of any actual STL bytes.
    np_proposed is only a proposal, not an observed or verified MPI rank.
    """
    role, _, revs = _case(case_id)
    _need(type(deck) is bytes and type(meta) is dict, 'physical bytes and metadata dict required')
    _need(meta.get('deck_sha256') == hashlib.sha256(deck).hexdigest()
          and type(meta.get('deck_bytes')) is int and meta['deck_bytes'] == len(deck),
          'metadata does not bind actual deck bytes')
    expected = _generate(case_id)
    _need(deck == expected['deck'], 'deck bytes differ from the fixed source-output recipe')
    _need(_json_exact(meta) == _json_exact(expected['meta']), 'metadata differs from the fixed case recipe')
    try:
        text, parsed = _parsed(deck)
        if role in ('U', 'C'):
            result = rb.read_d2(deck, meta)
            _need(result['verdict'] == 'PASS', 'D2 readback refused: ' + '; '.join(result['failures']))
            counts = result['expected_counts']
        else:
            counts = _baseline(text, parsed, meta, role)
        phases = {p: dict(type=i, radius_m=parsed['templates'][i]['radius'])
                  for i, p in enumerate(PHASES, 1)}
        drum = [t for _, t in parsed['cmds'] if t[:2] == ['fix', 'Drum']]
        _need(len(drum) == 1, 'one Drum declaration required')
        scale = float(drum[0][drum[0].index('scale') + 1])
        radius, length = .5 * scale, .2 * scale
        n_planned = sum(counts.values())
        frame_pm = dict(phases=copy.deepcopy(phases), n_planned=n_planned, revolutions=revs,
                        meta_steps={k: meta['steps'][k] for k in ('t0_planned', 'dump_every')},
                        arm=meta['arm'], seed=32452843, n_expected_file=None)
        return dict(case_id=case_id, role=role, phases=phases, n_planned=n_planned,
                    expected_counts=dict(counts), revolutions=revs, seed=32452843,
                    r_container=radius, axis='x', np_proposed=20, frame_pm=frame_pm,
                    density_generation='lab20261014',
                    geometry=dict(axis='x', r_container=radius, length=length, cgf=151.4),
                    registered=None, execution_authorized=False)
    except (KeyError, TypeError, IndexError, OverflowError, ZeroDivisionError, AssertionError) as exc:
        raise ValueError('preparation binding failed: ' + str(exc)) from exc


def prepare_case(case_id):
    """Generate and validate one of the eight fixed cases, in memory only."""
    item = _generate(case_id)
    validate_case(case_id, item['deck'], item['meta'])
    return item


def prepare_first8():
    """Static report, preserving every failed case; no decks are written."""
    report = dict(schema='mixer_precal_preparation/1', registered=None,
                  execution_authorized=False, research_results=0,
                  scope='fixed first8 synthetic preparation; no launch or observed particles',
                  oracle_limitation='exact current-source generator output; not independent physics validation',
                  np_proposed=20, cases=[], pairs=[])
    good = {}
    for cid in CASE_IDS:
        try:
            item = prepare_case(cid)
            good[cid] = item
            binding = validate_case(cid, item['deck'], item['meta'])
            report['cases'].append(dict(case_id=cid, status='STATIC_VALID', binding=binding,
                                        deck_sha256=item['meta']['deck_sha256'], deck_bytes=len(item['deck'])))
        except ValueError as exc:
            report['cases'].append(dict(case_id=cid, status='STATIC_REFUSED', reason=str(exc)))
    for b in (1, 2, 3):
        u, c = ('PRECAL_R1_B%d_%s' % (b, r) for r in ('U', 'C'))
        if u not in good or c not in good:
            report['pairs'].append(dict(pair='R1_B%d' % b, verdict='NOT_ESTABLISHED'))
        else:
            a, z = good[u], good[c]
            result = diff.diff_d2_decks(a['deck'], z['deck'], a['meta'], z['meta'])
            report['pairs'].append(dict(pair='R1_B%d' % b, verdict=result['verdict'], failures=result['failures']))
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description='Print first8 static preparation JSON; no file writes or execution')
    parser.parse_args(argv)
    report = prepare_first8()
    print(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False))
    return 0 if all(x['status'] == 'STATIC_VALID' for x in report['cases']) and all(
        x['verdict'] == 'PASS' for x in report['pairs']) else 2


if __name__ == '__main__':
    raise SystemExit(main())
