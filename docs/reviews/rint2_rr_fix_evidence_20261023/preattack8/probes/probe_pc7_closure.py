"""PC7-01..05 closure checks (own probes, not the round-7 probe files).

  A  PC7-01  chain parent SIGKILL (group alive) -> (a) same --out after deleting the attempt folder, (b) different --out, (c) a stale
             ledger clone made before the start record + different --out  -> rc / runner calls / ledger
  B  PC7-03  summary-less path: recover end record with chain_end cause exception (unconfirmed) vs by-chain exception -> same cause
  C  PC7-05  summary-less path: chain end record cause None · rc 1 · unconfirmed -> recover -> runner_rc ; summary path GROUP_UNCONFIRMED rc None
  D  PC7-04  recover_group with an unconfirmed foreign end record -> held (no end written)

  python3 -I probe_pc7_closure.py <tree>
"""
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from probe_common import setup  # noqa: E402

RR, T = setup(sys.argv[1])
out = {}

# ── A ─────────────────────────────────────────────────────────────────────────────────────────────
d, _rc, _so = T.led_new('P806A')
_r, n1, _s = T.led_add(d, 'ladder:P0')
clone = Path(T.TD) / 'ledgers' / 'P806A_stale_clone'
T.git_(clone.parent, 'clone', '-q', str(d), str(clone))                    # stale clone (before the start record)
b1 = Path(T.TD) / 'runs' / 'P806A_b1'
w = T.world('P806A', dict(T.PW, faults=[{'do': 'msg_sleep_after_mark', 'msg': '[p2] solving (P806A)', 's': 30.0, 'match': {'rj': 'inf'}}]))
seen, f1, tok = T.pe_kill_after('P806A', d, n1, b1, w, 'solving (P806A)')
raw = T.led_raw(d)
shutil.rmtree(f1)                                                          # (a) delete the folder, same --out
wa = T.world('P806A_same_out_after_rm')
a = T.lad_att('P806A_a', wa, d, n1, base=b1)
wb = T.world('P806A_other_out')
b = T.lad_att('P806A_b', wb, d, n1, base=Path(T.TD) / 'runs' / 'P806A_b2')
wc = T.world('P806A_clone')
c = T.lad_att('P806A_c', wc, clone, n1, base=Path(T.TD) / 'runs' / 'P806A_b3')
out['A_PC7_01'] = {'seen_mark': seen, 'group_alive': bool(T.gr_alive(tok)) if tok else None,
                   'a_same_out_after_rm': (a['rc'], T.n_calls(wa), T.led_raw(d) == raw),
                   'b_other_out': (b['rc'], T.n_calls(wb), T.led_raw(d) == raw),
                   'c_stale_clone_other_out': (c['rc'], T.n_calls(wc), (c['sum'] or {}).get('status'),
                                               [x.get('kind') for x in T.led_lines(clone)])}
for pid in T.gr_alive(tok) if tok else []:
    try:
        os.kill(pid, 9)
    except OSError:
        pass

# ── B (PC7-03) ───────────────────────────────────────────────────────────────────────────────────
rows = {}
for nm, end in (('recover_chain_end_exception', {'by': 'recover', 'cause': 'parent_dead', 'rc': None, 'confirmed': True,
                                                 'chain_end': {'rc': -9, 'cause': 'exception', 'confirmed': False, 'ended_utc': 'x'}}),
                ('by_chain_exception_unconfirmed', {'by': 'chain', 'cause': 'exception', 'rc': -9, 'confirmed': False}),
                ('recover_chain_end_exception_oomlog', {'by': 'recover', 'cause': 'parent_dead', 'rc': None, 'confirmed': True,
                                                        'chain_end': {'rc': -9, 'cause': 'exception', 'confirmed': False, 'ended_utc': 'x'}})):
    f = T.pc_folder(f'P806B_{nm}', {T.PC_MARK: '{}\n'})
    T.pc_group(f, 'L01_floor', end, '[p2] run\n' + ('cupy.cuda.memory.OutOfMemoryError: out of memory\n' if 'oom' in nm else ''))
    r = RR.attempt_result_line(1, f, None, 'recover')
    rows[nm] = (r['cause'], r['resume_ok'])
out['B_PC7_03'] = rows

# ── C (PC7-05) ───────────────────────────────────────────────────────────────────────────────────
o5, tok5 = T.gr_fake_launch('P806C')
(o5 / 'groups' / 'L01_floor.end.json').write_text(json.dumps({'schema': 'rint-r-group-v1', 'name': 'L01_floor', 'token': tok5, 'rc': 1, 'cause': None,
                                                             'signal': None, 'confirmed': False, 'left': [999989], 'left_after_exit': 0,
                                                             'killed': 0, 'unsure': None, 'by': 'chain', 'ended_utc': 'x'}), encoding='utf-8')
end5, held5 = RR.recover_group(o5 / 'groups' / 'L01_floor.launch.json', RR.host_ident())
(o5 / 'groups' / 'L01_floor.end.json').write_text(json.dumps(end5), encoding='utf-8')
(o5 / 'logs').mkdir(exist_ok=True)
(o5 / 'logs' / 'L01_floor.log').write_text('[p2] run\n', encoding='utf-8')
c_no_summary = RR.orphan_cause(o5)
s = {'stop': {'code': 'GROUP_UNCONFIRMED', 'run': 'L01_floor', 'reason': None}, 'runs': [{'name': 'L01_floor', 'rc': None, 'group_cause': None}]}
c_summary = RR.stop_cause(s, o5)
out['C_PC7_05'] = {'held': held5, 'chain_end': (end5 or {}).get('chain_end'), 'no_summary_cause': c_no_summary, 'summary_cause': c_summary}

# ── D (PC7-04) ───────────────────────────────────────────────────────────────────────────────────
o4, tok4 = T.gr_fake_launch('P806D')
ep4 = o4 / 'groups' / 'L01_floor.end.json'
ep4.write_text(json.dumps({'schema': 'rint-r-group-v1', 'name': 'L01_floor', 'token': 'e' * 32, 'rc': 0, 'cause': None, 'confirmed': False,
                           'by': 'chain', 'ended_utc': 'x'}), encoding='utf-8')
b0 = ep4.read_bytes()
end4, held4 = RR.recover_group(o4 / 'groups' / 'L01_floor.launch.json', RR.host_ident())
out['D_PC7_04'] = {'end_written': end4 is not None, 'held_mentions_token': ('표지' in (held4 or '')), 'end_file_unchanged': ep4.read_bytes() == b0}
print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
