"""P1b — 실경로 (실제 git 원장 · `--stage recover --ledger` → 결과 줄 → `--add --resume 1` · RR3E 와 같은 길 `rc_recover_resume`): 앞 런 L01_floor 기록의
arms_read = 판독 실패 파일 신원 (이름 맞는 팔 · 내용 {} → 실제 read_run = ARM_UNREADABLE) 에 ARM_PUBLIC 나머지 11 칸을 생산자가 쓰지 않는 값으로 덧붙임 +
런 전 TIME_LIMIT (L02_ceiling) → resume rc 0 (허용) 인가.  대조 = 덧붙이지 않은 파일 신원 (rc 3 RESUME_NOT_ALLOWED)."""
import hashlib, json
from common import RR, T, setup_fixtures

def main():
    setup_fixtures()
    pay = b'{}\n'
    name = T.ct06_pub(0)['file']
    ids = [{'file': name, 'index': 0, 'sha256': hashlib.sha256(pay).hexdigest()}]
    pad = dict(ids[0], protocol_id='unknown:x', state='short', cg_info=None, cg_resid=None, imbalance=None, cert_pass=False, sid_fp='',
               cg_iters=True, resolve_iters=None, sv_cf_status=None, err_rel=-5.0)
    out = {}
    for tag, ar in (('ids', ids), ('padded', [pad])):
        r = T.rc_recover_resume(f'P1B_{tag}', T.CHAIN_OK0, T.LG_PLAIN, prep=T.rr3_cli_prep(ar, {name: pay}))
        out[tag] = {'recover_rc': r['recover_rc'], 'result': {k: (r['result'] or {}).get(k) for k in ('status', 'cause', 'resume_ok')},
                    'resume_rc': r['resume_rc'], 'not_allowed': r['not_allowed']}
    # 그 팔 파일을 실제 read_run 이 읽으면 (사슬 판독) 실패하는가 — 생산자 자리
    print(json.dumps(out, ensure_ascii=False, indent=1))

if __name__ == '__main__':
    main()
