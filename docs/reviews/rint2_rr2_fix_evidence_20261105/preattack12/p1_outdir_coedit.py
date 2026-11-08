"""P2-B 정확 출력 폴더 이름 대조 (record_outdir) — 요청 칸을 함께 고치면 비켜 간다.
정직 꼴 = RUNNER_RC · 러너 rc 1 · OOM 로그 · 멈춘 런 폴더 L01_floor_arm1/.unchecked/ 에 검사 실패본 (검사 실패 흔적) → 재실행 자격 False.
위조 = 같은 기록의 outdir 를 흔적 없는 옆 이름으로 + 요청 칸 (arms · arm_list) 을 그 이름에 맞게."""
from harness import *
setup()
LOG = '[p2] run\n' + T.LG_OOM
def case(tag, code, rec, trace=True, extra_dirs=()):
    f = mkfolder(tag)
    (f / T.LG_MARK).parent.mkdir(parents=True); (f / T.LG_MARK).write_text('{}\n')
    (f / 'logs').mkdir(); (f / 'logs' / 'L01_floor.log').write_text(LOG)
    if trace:
        u = f / 'L01_floor_arm1' / '.unchecked'; u.mkdir(parents=True)
        (u / 'p2_SBE_vgcf100_a0.json').write_text('{}\n')
    for d in extra_dirs:
        (f / d).mkdir(parents=True, exist_ok=True)
    s = {'status': 'STOPPED', 'stop': {'code': code, 'run': 'L01_floor', 'reason': None}, 'runs': [rec]}
    return rf(f, s), RR.stop_record_problem(s, f)
base = dict(name='L01_floor', role='floor', kit='kit_SBE_vgcf100', law='P0', c='0', rj='inf', variant=None, sv_cf=False,
            group_cause=None, rc=1, seconds=1.0, arms_read=[], machine='kgy')
rows = [
 ('honest arms1 outdir _arm1',            dict(base, arms=1, arm_list=None, outdir='L01_floor_arm1')),
 ('CT06-style sibling _arm9, arms 1',      dict(base, arms=1, arm_list=None, outdir='L01_floor_arm9')),
 ('co-edit arms 9 + _arm9',                dict(base, arms=9, arm_list=None, outdir='L01_floor_arm9')),
 ('co-edit arms 2 + _arm2 (in domain)',    dict(base, arms=2, arm_list=None, outdir='L01_floor_arm2')),
 ('co-edit arms 0 + _arm0',                dict(base, arms=0, arm_list=None, outdir='L01_floor_arm0')),
 ('co-edit arms -1 + _arm-1',              dict(base, arms=-1, arm_list=None, outdir='L01_floor_arm-1')),
 ('co-edit arms 1, arm_list [] + _arm1_arml', dict(base, arms=1, arm_list=[], outdir='L01_floor_arm1_arml')),
 ('co-edit arms 1, arm_list [0] (prefix list)', dict(base, arms=1, arm_list=[0], outdir='L01_floor_arm1_arml0')),
 ('co-edit arms 5, arm_list [9]',          dict(base, arms=5, arm_list=[9], outdir='L01_floor_arm5_arml9')),
 ('co-edit arms 2, arm_list [3,3] dup',    dict(base, arms=2, arm_list=[3, 3], outdir='L01_floor_arm2_arml3-3')),
 ('co-edit arms 2, arm_list [3,1] unsorted', dict(base, arms=2, arm_list=[3, 1], outdir='L01_floor_arm2_arml3-1')),
 ('co-edit arms 10**30',                   dict(base, arms=10**30, arm_list=None, outdir='L01_floor_arm' + str(10**30))),
 ('arm_list key dropped (arms 1) + _arm1',  {k: v for k, v in dict(base, arms=1, outdir='L01_floor_arm9').items()}),
]
for nm, rec in rows:
    for code in ('RUNNER_RC',):
        got, prob = case(nm.replace(' ', '_').replace(',', '').replace('[', '').replace(']', '')[:60], code, rec)
        print(f'{nm:45s} {code:10s} result_fields={got}  stop_record_problem={"None" if prob is None else "사유"}')
# same with GU (honest GU rc0 + chain_end confirmed False) and TIME_LIMIT shapes
print('--- TIME_LIMIT killed:timeout (trace in _arm1) ---')
tl = dict(base, group_cause='timeout', rc=None)
for nm, rec in (('honest', dict(tl, arms=1, arm_list=None, outdir='L01_floor_arm1')), ('co-edit arms 9', dict(tl, arms=9, arm_list=None, outdir='L01_floor_arm9')),
                ('co-edit arms 2', dict(tl, arms=2, arm_list=None, outdir='L01_floor_arm2'))):
    got, prob = case('TL_' + nm.replace(' ', '_'), 'TIME_LIMIT', rec)
    print(f'{nm:45s} TIME_LIMIT result_fields={got}  stop_record_problem={"None" if prob is None else "사유"}')
