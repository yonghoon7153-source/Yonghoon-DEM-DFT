"""Recompute the received transcript's arithmetic and receipt bytes; no run launch."""
from pathlib import Path
import hashlib,json,re
root=Path(__file__).resolve().parent
p=root/'received_zip/repo/docs/50kg/d07_guard/t_test_20261103/t_output_grep.txt'
t=p.read_text(encoding='utf-8')
lines=[x for x in t.splitlines() if re.fullmatch(r'[0-9a-f]{64}  /lustre/home/yonghoon/dem_test/kg50_d07_b50/[^\s]+',x)]
assert len(lines)==5
receipt=('\n'.join(lines)+'\n').encode()
sha=hashlib.sha256(receipt).hexdigest()
assert sha=='cff47c44385a95529ed2c6e97438985a56e6e2ede194e05f7541c14788570176'
for i,ending in enumerate(('input_kg50_d07_b50_r56.liggghts','run_kg50_d07_b50_r56.sh','input_kg50_d07_b50_r56t.liggghts','run_kg50_d07_b50_r56t.sh','restart_compress_1000000.bin')):
    assert lines[i].endswith('/'+ending)
gate=next(x for x in t.splitlines() if x.startswith('- G0 잡 안 덱 신원'))
assert lines[2][:64] in gate and lines[4][:64] in gate
assert re.search(r'337078\s+COMPLETED\s+0:0\s+00:03:53',t)
for i in range(4):assert f'- G{i} ' in t
oldp,newp=0.00011997834,0.00011998104
oldke,newke=3.3622402e-8,3.364381e-8
result=dict(pin='4d2b8fc42dc4d65845570c1bf4de5a67924ad311',
    status='PASS: transcribed receipt bytes and displayed arithmetic only; original decks/checkpoint/dumps not rehashed',
    reconstructed_receipt_sha256=sha,rows=lines,
    pressure_relative_change=(newp-oldp)/oldp,pressure_percent_change=100*(newp-oldp)/oldp,
    ke_relative_change=(newke-oldke)/oldke,ke_percent_change=100*(newke-oldke)/oldke,
    target_fraction=oldp/0.30,target_percent=100*oldp/0.30,
    first_judgment=1000000+2,trial_end=1000000+2+1998,
    identity_main_deck_vs_trial_deck_are_different=lines[0][:64]!=lines[2][:64],
    remaining_steps_if_D2_end_reused=4485002-1000000,
    conditional_hours_if_20000_steps_per_hour=(4485002-1000000)/20000)
(root/'trial_receipt_check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(root/'reconstructed_main_inputs.sha256').write_bytes(receipt)
print(json.dumps(result,ensure_ascii=False,indent=2))
