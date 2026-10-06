"""Compare Codex preserved evidence (reverify bundle, pin 165d0cf61) with our re-run on the HEAD copy.

usage: python3 -I compare.py <codex_evidence_dir> <our_evidence_dir> [real]
Prints compact tables (markdown-ish) for acceptance · reread_extra · adversarial · numerics (· real_beds with 'real').
"""
import json
import sys
from pathlib import Path

C, O = Path(sys.argv[1]), Path(sys.argv[2])
want_real = len(sys.argv) > 3 and sys.argv[3] == 'real'


def rd(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))


def short(s, n=110):
    s = '' if s is None else str(s)
    return s if len(s) <= n else s[:n] + '…'


print('## acceptance — publication (G2RR-02)')
ca, oa = rd(C / 'acceptance.json'), rd(O / 'acceptance.json')
cp = {x['label']: x for x in ca['publication']}
op = {x['label']: x for x in oa['publication']}
print('| label | Codex status · full_q · I_bottom | ours status · full_q · I_bottom | ours τ hertz | ours stop verdict (first reason) |')
for lab in cp:
    c, o = cp[lab], op.get(lab, {})
    ci = (c.get('full_certificate') or {}).get('I_bottom')
    oi = (o.get('full_certificate') or {}).get('I_bottom')
    stop = o.get('stop') or [None, '']
    print(f"| {lab} | {c['status']} · {c.get('full_q')} · {ci} | {o.get('status')} · {o.get('full_q')} · {oi} | "
          f"{(o.get('row') or {}).get('ion_net_status_hertz')} {(o.get('row') or {}).get('tau2_ion_hertz')} | {stop[0]} · {short(stop[1], 160)} |")
print()
print('## acceptance — stamp (G2RR-01)')
cs = {x['label']: x for x in ca['stamp']}
os_ = {x['label']: x for x in oa['stamp']}
print('| label | Codex accepted · generation | ours accepted · generation · problem |')
for lab in cs:
    c, o = cs[lab], os_.get(lab, {})
    print(f"| {lab} | {c['accepted']} · {c['generation']} | {o.get('accepted')} · {o.get('generation')} · {short(o.get('problem'), 200)} |")
print()
print('## reread_extra (G2RR-03)')
cr = {x['label']: x for x in rd(C / 'reread_extra.json')}
orr = {x['label']: x for x in rd(O / 'reread_extra.json')}
print('| label | Codex rc · verdict · queue_n | ours rc · verdict · queue_n · queue_n_unique · first C8 fail |')
for lab in cr:
    c, o = cr[lab], orr.get(lab, {})
    c8 = o.get('c8') or {}
    f8 = [f for f in (o.get('fails') or []) if 'C8' in str(f)]
    print(f"| {lab} | {c['rc']} · {c['verdict']} · {(c.get('c8') or {}).get('queue_n')} | {o.get('rc')} · {o.get('verdict')} · "
          f"{c8.get('queue_n')} · {c8.get('queue_n_unique')} · {short(f8[0] if f8 else '', 160)} |")
print()
print('## adversarial (G2R-02 · G2R-03 · GEN2-01 regression)')
cv, ov = rd(C / 'adversarial.json'), rd(O / 'adversarial.json')
print('| dead-end high | Codex G · method · first attempt | ours G · method · first attempt |')
for c, o in zip(cv['cg_dead_end'], ov['cg_dead_end']):
    print(f"| {c['high']:g} | {c['G']} · {c['info'].get('method')} · {(c['info'].get('attempts') or [{}])[0].get('outcome')} | "
          f"{o['G']} · {o['info'].get('method')} · {(o['info'].get('attempts') or [{}])[0].get('outcome')} |")
print('| direct high | Codex G · status/reason | ours G · status/reason |')
for c, o in zip(cv['direct'], ov['direct']):
    print(f"| {c['high']:g} | {c['G']} · {c['info'].get('status')}/{c['info'].get('reason')} | {o['G']} · {o['info'].get('status')}/{o['info'].get('reason')} |")
print(f"| zero_Rc (GEN2-01) | {cv['zero_Rc']['G']} · {cv['zero_Rc']['info'].get('reason')} | {ov['zero_Rc']['G']} · {ov['zero_Rc']['info'].get('reason')} |")
print(f"| baseline statuses · tau2 | {cv['baseline']['statuses']} · {cv['baseline']['tau2']} | {ov['baseline']['statuses']} · {ov['baseline']['tau2']} |")
print('| generation mutant | Codex statuses · stop9 n | ours statuses · stop9 n |')
for c, o in zip(cv['generation_mutants'], ov['generation_mutants']):
    print(f"| {c['label']} | {sorted(set(c['statuses'].values()))} · {len(c['stop9'])} | {sorted(set(o['statuses'].values()))} · {len(o['stop9'])} |")
print()
print('## numerics (G2R-03 regression · exact G 1.45)')
cn, on = rd(C / 'numerics.json'), rd(O / 'numerics.json')
print('| high | Codex G · method · rel_err · cert_problem | ours G · method · rel_err · cert_problem | same G bits |')
worst_c = max(abs(x['rel_error']) for x in cn if x['rel_error'] is not None)
worst_o = max(abs(x['rel_error']) for x in on if x['rel_error'] is not None)
for c, o in zip(cn, on):
    print(f"| {c['high']:g} | {c['G']} · {c['certificate'].get('method')} · {c['rel_error']} · {c['certificate_problem']} | "
          f"{o['G']} · {o['certificate'].get('method')} · {o['rel_error']} · {o['certificate_problem']} | "
          f"{(c['G'] is not None and o['G'] is not None and float(c['G']).hex() == float(o['G']).hex())} |")
print(f'worst |rel_err| Codex {worst_c!r} · ours {worst_o!r}')
if want_real:
    print()
    print('## real_beds (graph solves · Codex direct build/solve)')
    cb, ob = rd(C / 'real_beds.json'), rd(O / 'real_beds.json')
    print('| bed | arm | mode | Codex [G, q] | ours [G, q] | rel diff q | bits same |')
    for bed in cb:
        for arm in cb[bed]['arms']:
            for mode, cvals in cb[bed]['arms'][arm]['solves'].items():
                ovals = ob[bed]['arms'][arm]['solves'][mode]
                if cvals[1] is None or ovals[1] is None:
                    rel = None if cvals[1] is None and ovals[1] is None else 'NONE_MISMATCH'
                else:
                    rel = abs(ovals[1] / cvals[1] - 1)
                same = [None if v is None else float(v).hex() for v in cvals] == [None if v is None else float(v).hex() for v in ovals]
                print(f'| {bed} | {arm} | {mode} | {cvals} | {ovals} | {rel} | {same} |')
    print('| bed | arm | Codex clamp · floor · n_zero_R (constr) | ours |')
    for bed in cb:
        for arm in cb[bed]['arms']:
            ca_, oa_ = cb[bed]['arms'][arm], ob[bed]['arms'][arm]
            nz = lambda a: ((a.get('solve_info') or {}).get('constriction_only') or {}).get('n_zero_resistance')  # noqa: E731
            print(f"| {bed} | {arm} | {ca_['clamp']} · {ca_['floor']} · {nz(ca_)} | {oa_['clamp']} · {oa_['floor']} · {nz(oa_)} |")
