"""P3-5 summary_shape_problem 완결성 — result_fields (요약 있는 길) 이 Stop 아닌 예외로 끝나는 꼴이 남았나 (무작위 · 값 꼴 전수)."""
import random, itertools
from harness import *
setup()
random.seed(12)
VALS = [None, True, False, 0, 1, -1, 2**70, 1.5, float('nan'), '', 'L01_floor', 'TIME_LIMIT', 'GROUP_UNCONFIRMED', 'RUNNER_RC', 'x/y', '../x',
        'L01_floor_arm1', [], [1], ['L01_floor'], {}, {'a': 1}, [[]], {'code': 'TIME_LIMIT'}, 'timeout', 'signal', 'L01_floor\x00x', '/abs']
f = mkfolder('fuzz')
(f / T.LG_MARK).parent.mkdir(parents=True); (f / T.LG_MARK).write_text('{}\n')
(f / 'logs').mkdir(); (f / 'logs' / 'L01_floor.log').write_text('[p2] run\n')
T.pc_group(f, 'L01_floor', {'by': 'recover', 'confirmed': True, 'chain_end': {'rc': 0, 'cause': None, 'confirmed': False}})
crashes = {}
n = 0
for _ in range(30000):
    rec = {}
    for k in ('name', 'outdir', 'group_cause', 'rc', 'arms', 'arm_list', 'arms_read'):
        if random.random() < 0.85:
            rec[k] = random.choice(VALS)
    if random.random() < 0.6:
        rec['name'] = 'L01_floor'
    stop = random.choice([None, {}, {'code': random.choice(VALS), 'run': random.choice(VALS)}, {'code': random.choice(['TIME_LIMIT', 'GROUP_UNCONFIRMED', 'RUNNER_RC']), 'run': random.choice(VALS + ['L01_floor'] * 5)}])
    runs = random.choice([None, [], [rec], [rec, dict(rec)], [dict(rec, name='L00'), rec]])
    s = {'status': random.choice(['STOPPED', 'TIME_LIMIT', 'GROUP_UNCONFIRMED', 'CALIBRATED']), 'stop': stop, 'runs': runs}
    if random.random() < 0.1:
        s.pop('runs')
    n += 1
    try:
        RR.result_fields(f, s)
    except RR.Stop:
        pass
    except Exception as e:
        key = f'{type(e).__name__}: {str(e)[:80]}'
        crashes.setdefault(key, s)
print('cases', n, 'non-Stop exception kinds', len(crashes))
for k, s in list(crashes.items())[:10]:
    print(' ', k, '←', repr(s)[:300])
