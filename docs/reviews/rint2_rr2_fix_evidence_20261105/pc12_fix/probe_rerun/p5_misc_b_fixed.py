"""P2-B 나머지 — (a) 앞 런 기록이 실패인데 뒤에 위조 기록 (TIME_LIMIT · GU) · (b) 요약 중복 칸 (사람 = 앞 값 · 코드 = 뒤 값) ·
(c) 선언된 한정 확인 (arms 칸 없음 · arms_read 칸 없음 · GU 시작 기록 없음)."""
from harness import *
setup()
OOM = '[p2] run\n' + T.LG_OOM
def mk(tag, logs=('L01_floor',), trace=False, groups=()):
    f = mkfolder(tag)
    (f / T.LG_MARK).parent.mkdir(parents=True); (f / T.LG_MARK).write_text('{}\n')
    (f / 'logs').mkdir()
    for nm in logs:
        (f / 'logs' / f'{nm}.log').write_text(T.RC02_LOG if nm == 'L01_floor' else '')
    if trace:
        u = f / 'L01_floor_arm1' / '.unchecked'; u.mkdir(parents=True); (u / 'p2_SBE_vgcf100_a0.json').write_text('{}\n')
    for nm, end in groups:
        T.pc_group(f, nm, end)
    return f
R = T.ct06_rec
fail1 = R(group_cause=None, rc=1, arms=1, arm_list=None, arms_read=[])
print('(a1) runs [L01 rc1 실패, L02 {timeout,null}] · TIME_LIMIT L02 · 빈 로그 L02:',
      rf(mk('a1', logs=('L01_floor', 'L02_ceiling'), groups=(('L01_floor', T.CHAIN_OK1),)),
         {'status': 'STOPPED', 'stop': {'code': 'TIME_LIMIT', 'run': 'L02_ceiling'},
          'runs': [fail1, R('L02_ceiling', group_cause='timeout', rc=None, arms=1, arm_list=None, arms_read=[])]}))
print('(a2) runs [L01 rc1 실패, L02 {None,0}] · GU L02 · L02 그룹 기록 없음 · 빈 로그 L02:',
      rf(mk('a2', logs=('L01_floor', 'L02_ceiling'), groups=(('L01_floor', T.CHAIN_OK1),)),
         {'status': 'STOPPED', 'stop': {'code': 'GROUP_UNCONFIRMED', 'run': 'L02_ceiling'},
          'runs': [fail1, R('L02_ceiling', group_cause=None, rc=0, arms=1, arm_list=None, arms_read=[])]}))
# (b) 중복 칸 — stage_summary_read = json.loads (뒤 값) · 사람이 보는 앞 값 arms 1 · outdir _arm1
f = mk('b', trace=True, groups=(('L01_floor', T.CHAIN_OK1),))
(f / 'logs' / 'L01_floor.log').write_text(OOM)
raw = ('{"tool": "%s", "schema": "%s", "stage": "ladder", "status": "STOPPED", "stop": {"code": "RUNNER_RC", "run": "L01_floor", "reason": null}, '
       '"runs": [{"name": "L01_floor", "arms": 1, "arm_list": null, "outdir": "L01_floor_arm1", "group_cause": null, "rc": 1, "arms_read": [], '
       '"arms": 9, "outdir": "L01_floor_arm9"}]}') % (RR.TOOL, RR.SCHEMA)
(f / 'ladder_summary.json').write_text(raw)
s, st = RR.stage_summary_read(f)
print('(b) 중복 칸 요약 읽기 상태', st, '· 코드가 읽은 arms/outdir =', (s['runs'][0]['arms'], s['runs'][0]['outdir']) if s else None, '· 다시 셈 =',
      (lambda g: [g['status'], g['side'], g['cause'], g['resume_ok']])(RR.result_recount(f)))
# (c) 선언된 한정 (확인만)
f = mk('c1', trace=True); (f / 'logs' / 'L01_floor.log').write_text(OOM)
print('(c1 선언) arms 칸 없음 + outdir _arm9:', rf(f, {'status': 'STOPPED', 'stop': {'code': 'RUNNER_RC', 'run': 'L01_floor'},
                                                    'runs': [R(outdir='L01_floor_arm9', group_cause=None, rc=1, arms_read=[])]}))
f = mk('c2')
print('(c2 선언) GU · {None,0} · L01 그룹 기록 없음:', rf(f, {'status': 'STOPPED', 'stop': {'code': 'GROUP_UNCONFIRMED', 'run': 'L01_floor'},
                                                       'runs': [R(group_cause=None, rc=0, arms=1, arm_list=None, arms_read=[])]}))
f = mk('c3', groups=(('L01_floor', T.CHAIN_OK1),))
print('(c3 대조) 같은 + L01 끝 기록 by chain 확인 True:', rf(f, {'status': 'STOPPED', 'stop': {'code': 'GROUP_UNCONFIRMED', 'run': 'L01_floor'},
                                                          'runs': [R(group_cause=None, rc=0, arms=1, arm_list=None, arms_read=[])]}))
f = mk('c4', groups=(('L01_floor', T.CHAIN_OK1),))
print('(c4 선언) RUNNER_RC 정직 rc1 끝 기록 → 런 기록 {signal,null} 두 칸:', rf(f, {'status': 'STOPPED', 'stop': {'code': 'RUNNER_RC', 'run': 'L01_floor'},
                                                          'runs': [R(group_cause='signal', rc=None, arms=1, arm_list=None, arms_read=[])]}))
