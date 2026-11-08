"""TIME_LIMIT 런 기록 없음 ('none') — 멈춘 런 이름 꼴 · 그 이름 흔적만 본다.  생산자는 앞 런이 정확한 rc 0 으로 끝나 팔을 읽은 뒤에만 다음 런의
시간 상한 관문에 닿는다 (실패 런 = 그 자리에서 RUNNER_RC · 단계 끝).  정직 = RUNNER_RC · 러너 rc 1 · Traceback (runner_rc · 재실행 자격 False) →
요약의 stop 객체 두 칸만 (code TIME_LIMIT · run = 다음 이름 L02_ceiling) 바꿈 (runs · 그룹 기록 · 로그 그대로)."""
from harness import *
setup(full=True)
rec = T.ct06_rec
L01_fail = rec(group_cause=None, rc=1, arms=1, arm_list=None, arms_read=[])
def summ(code, run, runs):
    def prep(f):
        RR.write_summary(Path(f) / 'ladder_summary.json', {'tool': RR.TOOL, 'schema': RR.SCHEMA, 'stage': 'ladder', 'status': 'STOPPED',
                                                           'stop': {'code': code, 'run': run, 'reason': None}, 'runs': runs})
    return prep
for nm, code, run in (('honest RUNNER_RC L01 rc 1', 'RUNNER_RC', 'L01_floor'), ('forged TIME_LIMIT run L02_ceiling', 'TIME_LIMIT', 'L02_ceiling'),
                      ('forged TIME_LIMIT run zzz (생산자 이름 꼴도 아님)', 'TIME_LIMIT', 'zzz')):
    r = T.rc_recover_resume('p4_' + str(abs(hash(nm)) % 10**6), T.CHAIN_OK1, T.RC02_LOG, prep=summ(code, run, [L01_fail]))
    print(f'{nm:50s} recover_rc={r["recover_rc"]} result={r["result"]} resume_rc={r["resume_rc"]} RESUME_NOT_ALLOWED={r["not_allowed"]}')
# 재실행이 무엇을 다시 도는가 — 원천 폴더의 L01 끝 기록 rc 1 = _src_done False → L01 을 새로 (복사 아님)
f = sorted(Path(T.TD).glob('runs/p4_*/attempt_1'))[-1]
rn = RR.ResumeRunner.__new__(RR.ResumeRunner); rn.src = f
print('ResumeRunner._src_done(L01_floor) on source =', rn._src_done('L01_floor', 'L01_floor_arm1'), '→ 재실행은 L01 (rc 1 Traceback 런) 을 다시 돈다')
