import sys, os, json, tempfile, shutil
W = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-afe53be7bdb176c82'
sys.path.insert(0, os.path.join(W, 'scripts'))
import test_ca_ext_b6 as B6
import run_contract as RC
B6.RC = RC
td = tempfile.mkdtemp(prefix='floorprobe_')
d = os.path.join(td, 'nf')
os.makedirs(d)
B6.make_fixture_nofloor(d)
FLOOR = B6.OFF + B6.LEAN2 + B6.cj_with(rj='inf') + ['--step3-cjunc-rj-limit', 'inf', '--step3-rtol', '1e-12']
rc, log, p = B6.run_payload(d, FLOOR, out='floor.json')
print('rc', rc)
fp = os.path.join(d, 'floor.json.failed')
if os.path.exists(fp):
    p = json.load(open(fp))
s3 = ((p or {}).get('mpm_metrics') or {}).get('step3') or {}
m = s3.get('manifest') or {}
print('components', json.dumps(m.get('components'), ensure_ascii=False)[:800])
print('missing', m.get('missing'), 'failed', m.get('failed'), 'status', m.get('status'))
cj = ((m.get('ca_ext') or {}).get('cjunc') or {}).get('evidence') or {}
print('receipts', json.dumps(cj.get('receipts'), ensure_ascii=False)[:600])
print('backend', m.get('backend'))
print('interface_receipts', json.dumps(m.get('interface_receipts'), ensure_ascii=False)[:400])
print(log[-600:])
shutil.rmtree(td, ignore_errors=True)
