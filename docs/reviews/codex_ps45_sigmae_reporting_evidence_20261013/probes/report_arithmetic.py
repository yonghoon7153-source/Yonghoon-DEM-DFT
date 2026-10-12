"""Read-only reconstruction of published ps45 readouts; no network/DEM run."""
from pathlib import Path
import csv, hashlib, io, json, math, tarfile
R=Path(__file__).resolve().parents[1]
D=R/'source/docs/data/ps45_r45_network_g2_20261007'
order=['0:10','3:7','5:5','7:3','10:0']
rows={r['P_S']:r for r in csv.DictReader((D/'network_cases.tsv').open(encoding='utf8',newline=''),delimiter='\t')}
out={'scope':'stored solve-certificate reconstruction, not raw-bed re-solve','cases':[]}
with tarfile.open(D/'raw/ps45_network_g2.tgz') as t:
    archived={r['P_S']:r for r in csv.DictReader(io.StringIO(t.extractfile('network_cases.tsv').read().decode('utf8')),delimiter='\t')}
    assert rows==archived
    for ratio in order:
        row=rows[ratio]; cid=row['case_id']; item={'ratio':ratio,'case_id':cid,'modes':{}}
        for mode,stem in [('hertz','hertzian'),('physics','physics')]:
            name=f'solver_output/{cid}/network_conductivity_{stem}.json'
            raw=t.extractfile(name).read(); rec=json.loads(raw)
            c=rec['electronic_solve_certificate_full']
            assert c['status']=='computed' and c['sigma_bulk_S_cm']==.05
            q=c['I_bottom']/c['delta_V']*c['g_to_q']
            current_cons=abs(c['I_bottom']+c['I_top'])/max(abs(c['I_bottom']),abs(c['I_top']))
            assert current_cons < 1e-6 and c['residual_rel'] < 1e-6
            old=q*50; new=q*4.1
            assert round(old,6)==float(row[f'electronic_sigma_full_mScm_{mode}'])
            assert round(q,8)==rec['electronic_sigma_full']
            assert rec['electronic_area_binding_counts_physics']=={'native_unsupported_pair':rec['electronic_n_edges']}
            item['modes'][mode]={'q_reconstructed':q,'old50_mScm':old,'new4_1_mScm':new,
                'new4_1_display6':round(new,6),'old_TSV':float(row[f'electronic_sigma_full_mScm_{mode}']),
                'new_vs_scaled_rounded_delta_mScm':new-float(row[f'electronic_sigma_full_mScm_{mode}'])*.082,
                'electronic_edges':rec['electronic_n_edges'],'native_unsupported_pair':rec['electronic_area_binding_counts_physics']['native_unsupported_pair'],
                'conservation_rel_recomputed':current_cons,'residual_rel_recorded':c['residual_rel'],
                'temperature_provenance':rec.get('temperature_provenance'),
                'record_path':name,'record_sha256':hashlib.sha256(raw).hexdigest()}
        out['cases'].append(item)
f=1/(1+(4.5/2)**1.5)
out['pc_factor']={'exact':f,'inverse':1/f,'inverse_from_rounded_0_229':1/.229}
out['endpoints_conditional_monodisperse_ordinary_positive_edges']={}
for m in ['hertz','physics']:
    sc=out['cases'][0]['modes'][m]['new4_1_mScm'];pc=out['cases'][-1]['modes'][m]['new4_1_mScm']
    out['endpoints_conditional_monodisperse_ordinary_positive_edges'][m]={'SC':sc,'PC_factor_on':pc,'PC_factor_off':pc/f,'PC_over_SC_on':pc/sc,'PC_over_SC_off':pc/f/sc}
out['nominal_solid_fraction_from_user_densities']=(.816/4.85)/(.816/4.85+.184/1.64)
out['nominal_solid_fraction_from_DEM_densities']=(.816/4.8)/(.816/4.8+.184/2.0)
out['literature_composition_conversions']={'minnmann_53_to_solid':.53/.86,'minnmann_61_to_solid':.61/.86,'user_solid_60_to_total_at_porosity_14':.6*.86,'DEM_solid_to_total_at_porosity_14':out['nominal_solid_fraction_from_DEM_densities']*.86}
out['source_module_run_pin_equals_review_pin']=(R/'evidence/network_conductivity_run0801.py').read_bytes()==(R/'source/scripts/network_conductivity.py').read_bytes()
assert out['source_module_run_pin_equals_review_pin']
print(json.dumps(out,ensure_ascii=True,indent=2))
(R/'evidence/report_arithmetic.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
with (R/'evidence/rescaled_readout_pc_factor_on.csv').open('w',encoding='utf8',newline='') as fcsv:
    w=csv.writer(fcsv,lineterminator='\n');w.writerow(['PC_SC_ratio','case_id','Hertz_q','Physics_q','Hertz_at4_1_mScm','Physics_at4_1_mScm','PC_factor','basis'])
    for item in out['cases']:
        a=item['modes'];w.writerow([item['ratio'],item['case_id'],a['hertz']['q_reconstructed'],a['physics']['q_reconstructed'],a['hertz']['new4_1_mScm'],a['physics']['new4_1_mScm'],'original_enabled','readout_only_not_new_production'])
