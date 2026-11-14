"""Observe a pinned synthetic model's copy boundary; plan declared byte lifetimes."""
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def checked_module(path, expected_sha256, name):
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected_sha256:
        raise ValueError('Synthetic dependency identity mismatch')
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MODEL = checked_module(HERE.parent / 'dem_trial_isolation_20261114/trial_model.py',
                       '8a636801bad425481111c820d3af761bbcedcb1cad7ca087dd9bc7fbf44caa4e', 'pinned_trial')
FIXTURE = checked_module(HERE.parent / 'dem_trial_isolation_20261114/test_trial_model.py',
                         '5aa6b3d5eb77406ca080634e902325c82fb13cade8ece40ea35470c05d53498f', 'pinned_fixture')
MEMORY = checked_module(HERE.parent / 'dem_memory_preparation_20261114/memory_liveness.py',
                        '1a7128aaf566920640faa158857eb678599f38bc581adfd1566a2f7a8031fe10', 'pinned_memory')


def observe_attempt(*, rods=False, fail_at=None):
    """Observe top-level deepcopy calls only, with the fixed toy's ordinary behavior."""
    store = MODEL.TrialModel(FIXTURE.seed())
    before = json.dumps(store._state, sort_keys=True)
    parent_id = id(store._state)
    original = MODEL.deepcopy
    events = []
    destinations = []

    def observed(source):
        clone = original(source)
        destinations.append(id(clone))
        roots = {id(store._state), id(source), id(clone)}
        events.append(dict(copy_number=len(events) + 1, live_state_roots=len(roots),
                           source_is_committed=source is store._state,
                           parent_still_current=id(store._state) == parent_id))
        return clone

    MODEL.deepcopy = observed
    status, returned = 'COMPLETED_SYNTHETIC', None
    try:
        returned = store.attempt(rods=rods, fail_at=fail_at)
    except MODEL.InjectedFailure:
        status = 'INJECTED_FAILURE'
    finally:
        MODEL.deepcopy = original
    completed = status == 'COMPLETED_SYNTHETIC'
    return dict(status=status, rods=rods, injected_site=fail_at, copy_events=events,
                parent_unchanged=json.dumps(store._state, sort_keys=True) == before,
                committed_trial_and_detached_return=bool(
                    completed and len(destinations) == 2
                    and id(store._state) == destinations[0] and id(returned) == destinations[1]
                    and destinations[0] != destinations[1]),
                actual_memory_measured=False, physical_solver_imported=False, execution_go=False)


def declared_plan(state_bytes, budget_bytes, *, retained_copies=0):
    """Hypothetical reservations; the caller supplies bytes, never inferred from dict size."""
    if type(state_bytes) is not int or state_bytes <= 0:
        raise ValueError('Exact positive declared bytes required')
    if type(budget_bytes) is not int or budget_bytes < 0:
        raise ValueError('Exact nonnegative declared budget required')
    if type(retained_copies) is not int or retained_copies < 0:
        raise ValueError('Exact nonnegative retained copy count required')

    def allocation(name, start, end):
        return dict(id=name, pool='planned_arrays', reserved_bytes=state_bytes,
                    used_bytes=state_bytes, start=start, end=end)

    allocations = [allocation('old', 0, 4), allocation('trial', 1, 6), allocation('returned', 2, 7)]
    allocations += [allocation('retained_' + str(i), 0, 7) for i in range(retained_copies)]
    return dict(schema='synthetic_memory_liveness/1', units='B',
                pools={'planned_arrays': {'budget_bytes': budget_bytes}},
                allocations=allocations, views=[])
