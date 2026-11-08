"""P2-A rejected_in_folder — 생산자 꼴 폴더 (attempt.json + rejected.json) 에서 기록 바이트를 바꿔 본다 (다시 셈 = result_recount)."""
from harness import *
setup()
C = 'a' * 40
ATT = {'schema': 'rint-r-attempt-v1', 'n': 1, 'target': 'ladder:P0', 'machine': 'kgy', 'resume_of': None, 'ledger_commit': C}
def rec(**o):
    r = {'schema': 'rint-r-rejected-v1', 'n': 1, 'code': 'MACHINE_NOT_ALLOWED', 'cause': 'x', 'ledger_commit': C, 'utc': '2026-11-06T00:00:00Z'}
    r.update(o); return r
def go(tag, body, att=ATT, extra=None):
    f = mkfolder(tag)
    (f / 'attempt.json').write_bytes(RR.canon_bytes(att))
    (f / 'rejected.json').write_bytes(body if isinstance(body, bytes) else RR.canon_bytes(body))
    if extra: extra(f)
    try:
        g = RR.result_recount(f); return [g['status'], g['side'], g['stop']['code'] if g['stop'] else None]
    except RR.Stop as e:
        return f'Stop {e.code}'
    except Exception as e:
        return f'EXC {type(e).__name__}'
rows = [
 ('producer', rec()),
 ('code XYZ (STOPS 밖)', rec(code='XYZ')),
 ('code CALIBRATED (상태 이름)', rec(code='CALIBRATED')),
 ('code GENERATION (결과 뒤 멈춤)', rec(code='GENERATION')),
 ('code OUTDIR_NOT_EMPTY (옆 기록 전용)', rec(code='OUTDIR_NOT_EMPTY')),
 ('utc ""', rec(utc='')),
 ('cause ""', rec(cause='')),
 ('n 1.0', rec(n=1.0)), ('n true', rec(n=True)), ('n "1"', rec(n='1')),
 ('code trailing NL', rec(code='MACHINE_NOT_ALLOWED\n')), ('code fullwidth', rec(code='ＭACHINE')),
 ('commit upper', rec(ledger_commit=C.upper())),
 ('dup key n (raw)', b'{"schema":"rint-r-rejected-v1","n":2,"n":1,"code":"X","cause":"x","ledger_commit":"' + C.encode() + b'","utc":"u"}'),
 ('NaN cause (raw)', b'{"schema":"rint-r-rejected-v1","n":1,"code":"X","cause":NaN,"ledger_commit":"' + C.encode() + b'","utc":"u"}'),
 ('n 1e400 (raw → inf)', b'{"schema":"rint-r-rejected-v1","n":1e400,"code":"X","cause":"x","ledger_commit":"' + C.encode() + b'","utc":"u"}'),
 ('BOM (raw)', b'\xef\xbb\xbf' + RR.canon_bytes(rec())),
]
for nm, b in rows:
    print(f'{nm:34s} → {go(nm[:20].replace(" ", "_").replace("/", "_"), b)}')
print('hidden dir .x       →', go('hid', rec(), extra=lambda f: (f / '.x').mkdir()))
print('rejected.json = dir (no file) →', end=' ')
f = mkfolder('dirrej'); (f / 'attempt.json').write_bytes(RR.canon_bytes(ATT)); (f / 'rejected.json').mkdir()
g = RR.result_recount(f); print([g['status'], g['side'], g['cause'], g['resume_ok']])
