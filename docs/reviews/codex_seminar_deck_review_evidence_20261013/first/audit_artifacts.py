from pathlib import Path,PurePosixPath
import csv,hashlib,io,json,tarfile,zipfile
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
slides=json.loads((R/'evidence/pptx_slides.json').read_text(encoding='utf8'))
assets={sha(p.read_bytes()):str(p.relative_to(R)).replace('\\','/') for root in [R/'sources/code',R/'input/docs/seminar_20261013/figs'] for p in root.rglob('*') if p.is_file() and p.suffix.lower() in ['.png','.jpg','.svg']}
matches=[{'slide':s['slide'],'media':m['path'],'sha256':m['sha256'],'match':assets.get(m['sha256'])} for s in slides for m in s['media']]
(R/'evidence/image_matches.json').write_text(json.dumps(matches,ensure_ascii=False,indent=2),encoding='utf8')
def table(p):return list(csv.DictReader(p.open(encoding='utf-8-sig',newline=''),delimiter='\t'))
N=R/'sources/code/docs/data/ps45_r45_network_g2_20261007'
rows=table(N/'network_cases.tsv');out=[]
for p in ['0:10','3:7','5:5','7:3','10:0']:
    x=next(x for x in rows if x['P_S']==p)
    full=float(x['sigma_full_mScm_hertz']);cf=float(x['sigma_bulk_net_mScm_hertz']);tau=float(x['tau2_ion_hertz'])
    out.append({'ps':p,'sigma_ion_at_1p5':full/2,'tau2_full':tau,'tau2_cf_from_same_basis':tau*full/cf,'cf_over_full':cf/full,'constriction_power_share_percent_recorded':100*float(x['constriction_power_share_ion_hertz']),'phi_source':x['phi_basis'],'length_source':x['L_basis']})
F=R/'sources/code/docs/data/ps45_sigmae_factor_off_20261013'
new=table(F/'factor_off_electronic.tsv');checks=[]
with tarfile.open(F/'raw/ps45_sigmae_factor_off_20261013.tgz','r:gz') as t:
    entries=t.getmembers();assert sum(e.size for e in entries)<20_000_000
    for e in entries:
        name=PurePosixPath(e.name);assert '..' not in name.parts and not name.is_absolute() and not e.issym() and not e.islnk()
    tsvs=[e for e in entries if e.name.endswith('factor_off_electronic.tsv')];assert len(tsvs)==1
    assert t.extractfile(tsvs[0]).read()==(F/'factor_off_electronic.tsv').read_bytes()
    raw_inventory=[{'path':e.name,'bytes':e.size} for e in entries if e.isfile()]
for x in new:
    q=float(x['main_q']);sig=float(x['main_sigma_ref_mScm']);reference=float(x['sigma_ref_S_cm'])*1000
    assert abs(q*reference-sig)<1e-14
    checks.append({'ps':x['P_S'],'sigma':sig,'q':q,'round3':round(sig,3),'reference_mScm':reference,'off_over_on':float(x['off_over_on_hertz']),'control_rel_diff':float(x['control_hertz_rel_diff'])})
# The delivered PDF is the rendering evidence. matplotlib is unavailable in this
# runtime, so do not claim that the plotting function was independently executed.
ticks={'method':'visual inspection of delivered PDF page 12 and source call order',
       'visible':['0:10','7:3'],'missing':['3:7','5:5','10:0'],
       'source_issue':'_fmt replaces the categorical x-axis locator after set_xticks/set_xticklabels',
       'plot_function_rerun':False}
values={'network_readouts':out,'ps45_factor_off':checks,'ps45_archive_inventory':raw_inventory,'dcp_ratios':[54/4.47,70.6/12.4],'K_GPa':1.53/(3*(1-2*.49)),'mu_GPa':1.53/(2*(1+.49)),'F4_ticks_observation':ticks,'images_matched':sum(bool(x['match']) for x in matches),'image_uses':len(matches),'caveat':'recorded power shares checked as readouts, not recomputed from unavailable per-edge currents; no transport/DEM/MPM solver executed'}
(R/'evidence/independent_arithmetic.json').write_text(json.dumps(values,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in values.items() if k!='ps45_archive_inventory'},ensure_ascii=False,indent=2))
