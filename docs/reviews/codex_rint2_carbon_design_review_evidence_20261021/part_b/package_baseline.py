"""One-time exact-byte packaging of the few historical inputs used by probes."""
from pathlib import Path
import hashlib,json,shutil
HERE=Path(__file__).resolve().parent
WORK=HERE.parent.parent
DST=HERE/'baseline'
items=[]
def cp(src,rel,pin):
    src=Path(src); dst=DST/rel
    dst.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(src,dst)
    a=hashlib.sha256(src.read_bytes()).hexdigest()
    b=hashlib.sha256(dst.read_bytes()).hexdigest()
    assert a==b
    items.append({'path':rel,'sha256':a,'source_pin':pin,'bytes':dst.stat().st_size})
old=WORK/'rint_join_q7_recheck_20261020'
early=WORK/'rint_g2_impl_reverify_20261015'
cp(old/'source/scripts/rint_iface_join.py','old_join/scripts/rint_iface_join.py','2b9efa253edbf455c2e1abfef1d60e51818e01f8')
cp(early/'source/scripts/rint_iface_join.py','early/source/scripts/rint_iface_join.py','dcb97f1ed942f622d9189eee1a1e9432dc05a655')
for name in ('structure_probe.py','structure_minimal_replay.py','numeric_review.py','numeric_overflow_replay.py'):
    cp(old/'probes'/name,'probes/'+name,'previous Codex review evidence 2026-10-20')
tags=('baseline','malformed_numeric_contact_row_inside_block','malformed_numeric_atom_row_inside_block',
      'malformed_extra_contact_row','malformed_extra_atom_row','duplicate_radius_column','step_extra_token',
      'count_extra_token','wellshaped_duplicate_contact_control','wellshaped_duplicate_atom_control')
for tag in tags:
    for suf in ('sc.csv','atom.dump','contact.dump'):
        name=tag+'_'+suf
        cp(early/'tmp/join_independent'/name,'early/tmp/join_independent/'+name,'previous Codex synthetic counterexamples 2026-10-15')
(DST/'MANIFEST.json').write_text(json.dumps({'note':'Exact byte copies, no historical source edits. Only the old join module is substituted; imported dependencies and consumer remain the current environment, as in the controlled original probe. This is not a whole historical stack replay.','files':items,'total_bytes':sum(x['bytes'] for x in items)},indent=2),encoding='utf8')
print(len(items),'files',sum(x['bytes'] for x in items),'bytes')
