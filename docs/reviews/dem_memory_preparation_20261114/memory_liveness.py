"""Exact byte arithmetic for synthetic lifetime plans, without resource probes."""
import re


def _keys(value, expected):
    if type(value) is not dict or set(value) != set(expected):
        raise ValueError('unexpected or missing planning fields')


def _integer(value, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError('exact nonnegative integer required')


def _name(value):
    if type(value) is not str or re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*', value) is None:
        raise ValueError('ASCII planning identifier required')


def _interval(value):
    _integer(value['start']); _integer(value['end'])
    if value['end'] <= value['start']:
        raise ValueError('nonempty half-open lifetime required')


def account(plan):
    """Compute per-pool peaks of declared allocations; no completeness claim."""
    _keys(plan, ['schema', 'units', 'pools', 'allocations', 'views'])
    if plan['schema'] != 'synthetic_memory_liveness/1' or plan['units'] != 'B':
        raise ValueError('synthetic schema and exact B units required')
    pools, allocations, views = plan['pools'], plan['allocations'], plan['views']
    if type(pools) is not dict or not pools:
        raise ValueError('declared pools required')
    if type(allocations) is not list or not allocations or type(views) is not list:
        raise ValueError('nonempty allocation list and explicit view list required')
    for pool, budget in pools.items():
        _name(pool); _keys(budget, ['budget_bytes']); _integer(budget['budget_bytes'])
    owners = {}
    for a in allocations:
        _keys(a, ['id', 'pool', 'reserved_bytes', 'used_bytes', 'start', 'end'])
        _name(a['id']); _name(a['pool']); _interval(a)
        _integer(a['reserved_bytes'], 1); _integer(a['used_bytes'])
        if a['used_bytes'] > a['reserved_bytes']:
            raise ValueError('used exceeds reserved')
        if a['id'] in owners or a['pool'] not in pools:
            raise ValueError('duplicate allocation or unknown pool')
        owners[a['id']] = a
    ids = set(owners)
    for v in views:
        _keys(v, ['id', 'owner', 'start', 'end', 'offset_bytes', 'nbytes'])
        _name(v['id']); _name(v['owner']); _interval(v)
        _integer(v['offset_bytes']); _integer(v['nbytes'], 1)
        if v['id'] in ids or v['owner'] not in owners:
            raise ValueError('duplicate view or missing allocation owner')
        ids.add(v['id'])
        a = owners[v['owner']]
        if v['start'] < a['start'] or v['end'] > a['end']:
            raise ValueError('view outlives owner')
        if v['offset_bytes'] + v['nbytes'] > a['reserved_bytes']:
            raise ValueError('view exceeds owner reservation')

    output = {}
    for pool in sorted(pools):
        events = {}
        for a in allocations:
            if a['pool'] != pool:
                continue
            size = a['reserved_bytes']
            events[a['start']] = events.get(a['start'], 0) + size
            events[a['end']] = events.get(a['end'], 0) - size
        live = peak = 0
        timeline = []
        for tick in sorted(events):
            live += events[tick]
            peak = max(peak, live)
            timeline.append([tick, live])
        if live != 0:
            raise ValueError('unbalanced lifetime events')
        budget = pools[pool]['budget_bytes']
        output[pool] = dict(peak_bytes=peak, budget_bytes=budget,
                            headroom_bytes=budget-peak, over_budget=peak > budget,
                            timeline=timeline)
    return dict(status='SYNTHETIC_ARITHMETIC_ONLY', pools=output,
                actual_resource_qualification=False, execution_go=False)
