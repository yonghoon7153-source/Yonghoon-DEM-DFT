"""Synthetic integer state machine only; no engine, research input or I/O."""
from copy import deepcopy

POINT_FIELDS = ('x', 'v', 'C', 'F', 'dg_acc', 'eps_acc')
PROFILE_DELTA = (3, 5, 7, 11)
HOST_DELTA = (13, 17, 19, 23)
PLAIN_SITES = ('trial_created', 'p2g', 'g2p_first', 'g2p_done',
               'host_first', 'host_done', 'before_commit')
ROD_SITES = ('rod_first', 'rod_positions', 'rod_velocity_first', 'rod_done')


class InjectedFailure(RuntimeError):
    pass


def validate_state(state):
    required = {'step', 'time_ticks', 'wall_z', 'wall_vel', 'points', 'profiles', 'host'}
    if type(state) is not dict or set(state) != required:
        raise ValueError('Synthetic state keys required')
    if any(type(state[k]) is not int for k in ('step', 'time_ticks', 'wall_z', 'wall_vel')):
        raise ValueError('Exact integer sentinels required')
    if state['step'] < 0 or state['time_ticks'] < 0:
        raise ValueError('Nonnegative step and tick required')
    if type(state['points']) is not list or not state['points']:
        raise ValueError('Nonempty synthetic point list required')
    seen = set()
    keys = {'point_id', 'particle_id', *POINT_FIELDS}
    for point in state['points']:
        if type(point) is not dict or set(point) != keys or any(type(v) is not int for v in point.values()):
            raise ValueError('Complete integer synthetic point required')
        if point['point_id'] < 0 or point['particle_id'] < 0 or point['point_id'] in seen:
            raise ValueError('Unique point identity and nonnegative owner required')
        seen.add(point['point_id'])
    for key in ('profiles', 'host'):
        if type(state[key]) is not list or len(state[key]) != 4 or any(type(v) is not int for v in state[key]):
            raise ValueError('Four integer accumulator sentinels required')


class TrialModel:
    """Single-owner toy store. Values are integer markers, not physical tensors."""
    def __init__(self, state):
        validate_state(state)
        self._state = deepcopy(state)

    def snapshot(self):
        return deepcopy(self._state)

    def attempt(self, *, rods=False, fail_at=None):
        if type(rods) is not bool or (fail_at is not None and type(fail_at) is not str):
            raise ValueError('Exact control types required')
        allowed = PLAIN_SITES + (ROD_SITES if rods else ())
        if fail_at is not None and fail_at not in allowed:
            raise ValueError('Unknown or disabled injection site')

        def checkpoint(site):
            if fail_at == site:
                raise InjectedFailure(site)

        trial = deepcopy(self._state)
        checkpoint('trial_created')
        for i, delta in enumerate(PROFILE_DELTA):
            trial['profiles'][i] += delta
        checkpoint('p2g')
        for i, point in enumerate(trial['points']):
            for field, delta in zip(POINT_FIELDS, (1, 2, 3, 4, 5, 6)):
                point[field] += delta
            if i == 0:
                checkpoint('g2p_first')
        checkpoint('g2p_done')
        if rods:
            for i, point in enumerate(trial['points']):
                point['x'] += 7
                if i == 0:
                    checkpoint('rod_first')
            checkpoint('rod_positions')
            for i, point in enumerate(trial['points']):
                point['v'] += 11
                if i == 0:
                    checkpoint('rod_velocity_first')
            checkpoint('rod_done')
        for i, delta in enumerate(HOST_DELTA):
            trial['host'][i] += delta
            if i == 0:
                checkpoint('host_first')
        checkpoint('host_done')
        trial['step'] += 1
        trial['time_ticks'] += 10
        checkpoint('before_commit')
        validate_state(trial)
        result = deepcopy(trial)
        self._state = trial
        return result
