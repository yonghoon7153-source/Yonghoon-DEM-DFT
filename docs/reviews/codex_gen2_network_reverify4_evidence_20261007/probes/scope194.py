"""Recount archived per-case evidence (not a new 194 raw-dump run)."""
from pathlib import Path
import sys,json,collections
R=Path(__file__).resolve().parents[1];S=R/'source';E=R/'evidence';sys.path.insert(0,str(S/'scripts'))
import run_network_194_parallel as np194
load=lambda p:json.loads(p.read_text(encoding='utf8'))
out={};allrows=[]
for ds,folder in [('lhs','lhs_descriptors_cov_1e09f661d'),('lhsx','lhsx_descriptors_cov_1e09f661d')]:
    j=load(S/f'docs/data/lhs_perc_audit_20261001/{ds}_20261001_d1ec42fba/perc_audit.json')
    rows=[r for r in j['rows'] if r.get('status')=='OK'];allrows+=rows
    h={p.stem:load(p) for p in (S/'docs/data'/folder).glob('*.json') if not p.name.startswith('_')}
    assert set(h)=={r['case'] for r in rows}
    mismatch=[];counts=collections.Counter();margin=[]
    for r in rows:
        a=h[r['case']]
        if r['mesh_sha256']!=a['raw']['mesh']['sha256']:mismatch.append((r['case'],'mesh_sha'))
        if r['atoms_declared']!=sum(a['phase_counts'].values()):mismatch.append((r['case'],'atoms'))
        if abs(r['plate_z_sim']-a['plate_z_sim'])>1e-14:mismatch.append((r['case'],'plate'))
        g=next(v for v in a.values() if isinstance(v,dict) and isinstance(v.get('all'),dict) and 'n_area_dump_negative' in v['all'])
        for k in ('n_rows','n_area_dump_negative','n_area_dump_zero','n_tested'):counts[k]+=g['all'][k]
        for k in ('n_orphan_rows_skipped','n_nonfinite_skipped'):counts[k]+=g[k]
        if g['all']['n_rows']!=r['n_rows']:mismatch.append((r['case'],'contacts'))
        margin.append((r['thickness_um']-4*max(r['r_se_max_um'],r['r_am_max_um']),r['case']))
    out[ds]=dict(n=len(rows),se_levels=dict(collections.Counter(r['se_level'] for r in rows)),am_levels=dict(collections.Counter(r['am_level'] for r in rows)),
                se_overlap=sum(r['se_overlap'] for r in rows),am_overlap=sum(r['am_overlap'] for r in rows),area_counts=dict(counts),
                linkage_mismatch=mismatch,minimum_L_minus_4r_um=min(margin),audit_has_atom_contact_hashes=any('atom_sha256' in r or 'contact_sha256' in r for r in rows))
print(json.dumps(out,ensure_ascii=False,indent=2));(E/'scope194.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
