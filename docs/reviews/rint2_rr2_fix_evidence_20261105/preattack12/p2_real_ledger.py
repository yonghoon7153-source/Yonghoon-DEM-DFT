"""실제 git 원장 경로 — recover --ledger → 결과 줄 → --add --resume 1 (attempt_order_problem).
(1) P2-B 정확 이름: 정직 RUNNER_RC rc 1 + 검사 실패 흔적 (L01_floor_arm1/.unchecked) · 끝 기록 by chain 확인 True —
    기록의 outdir 를 L01_floor_arm9 · arms 를 9 로 함께 고침 (CT06 의 TR_forged_outdir_sibling_req_trace 는 arms 1 이라 거부됨)
(2) GU 한 칸: 정직 GROUP_UNCONFIRMED · 러너가 스스로 rc 1 (Traceback) · 끝 기록 by chain 확인 False → recover 가 by recover 로 갈아 씀 (chain_end rc 1) —
    요약 런 기록 rc 1 → 0 한 칸만 고침."""
from harness import *
setup(full=True)
OOM = '[p2] run\n' + T.LG_OOM
def run(tag, end, log, runs, code='RUNNER_RC', trace=False):
    prep = T.ct06_summ(code, runs)
    if trace:
        prep = T.ct06_trace(prep)
    r = T.rc_recover_resume(tag, end, log, prep=prep)
    return {'recover_rc': r['recover_rc'], 'result': r['result'], 'resume_rc': r['resume_rc'], 'RESUME_NOT_ALLOWED': r['not_allowed']}
rec = T.ct06_rec
print('(1a) CT06 대조 — 옆 이름 _arm9 · arms 1 (거부 기대):',
      run('p1a', T.CHAIN_OK1, OOM, [rec(outdir='L01_floor_arm9', group_cause=None, rc=1, arms=1, arm_list=None, arms_read=[])], trace=True))
print('(1b) 같은 + arms 9 로 함께 고침:',
      run('p1b', T.CHAIN_OK1, OOM, [rec(outdir='L01_floor_arm9', group_cause=None, rc=1, arms=9, arm_list=None, arms_read=[])], trace=True))
print('(1c) 정직 (outdir _arm1 · arms 1):',
      run('p1c', T.CHAIN_OK1, OOM, [rec(outdir='L01_floor_arm1', group_cause=None, rc=1, arms=1, arm_list=None, arms_read=[])], trace=True))
GU_END = {'by': 'chain', 'left': [999989], 'confirmed': False, 'cause': None, 'rc': 1}
print('(2a) 정직 GU · 런 기록 rc 1 · 끝 기록 rc 1 확인 False:',
      run('p2a', GU_END, T.RC02_LOG, [rec(group_cause=None, rc=1, arms=1, arm_list=None, arms_read=[])], code='GROUP_UNCONFIRMED'))
print('(2b) 한 칸 — 런 기록 rc 1 → 0:',
      run('p2b', GU_END, T.RC02_LOG, [rec(group_cause=None, rc=0, arms=1, arm_list=None, arms_read=[])], code='GROUP_UNCONFIRMED'))
print('(2c) 두 칸 — 런 기록 {timeout · rc null}:',
      run('p2c', GU_END, T.RC02_LOG, [rec(group_cause='timeout', rc=None, arms=1, arm_list=None, arms_read=[])], code='GROUP_UNCONFIRMED'))
