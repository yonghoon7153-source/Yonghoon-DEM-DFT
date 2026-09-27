"""Independent reviewer; received builder is never imported or executed."""
from pathlib import Path,PurePosixPath
from decimal import Decimal as D,getcontext
import json,csv,hashlib,zipfile,stat
from pypdf import PdfReader
getcontext().prec=50
H=Path(__file__).resolve().parent
DL=Path('C:/Users/Administrator/Downloads')
Z=DL/'COMSOL63_B020_VOLTAGE_DECOMPOSITION_20260928.zip'
P=DL/'B020_voltage_decomposition.pdf'
OLD=DL/'COMSOL63_B020_EVIDENCE_RECONCILIATION_REVIEW_20260927.zip'
VIS=DL/'b020_results_visual_summary_20260928.zip'
def ident(p):
    with p.open('rb') as f:s=hashlib.file_digest(f,'sha256').hexdigest()
    return {'bytes':p.stat().st_size,'sha256':s}
def bid(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def j(p):return json.loads(p.read_bytes())
def rows(p):
    with p.open(encoding='utf-8-sig',newline='') as f:
        c=csv.DictReader(f);assert len(c.fieldnames)==len(set(c.fieldnames))
        out=list(c);assert all(None not in r and None not in r.values() for r in out);return out
def num(p):
    out=[{k:D(v) for k,v in r.items()} for r in rows(p)]
    assert all(v.is_finite() for r in out for v in r.values());return out
ids={p.name:ident(p) for p in [Z,P,OLD,VIS]}
assert ids[OLD.name]['sha256']=='ecab51759d01ff6f82ffd9f5a9e39c3b1caf0202a40be18040c9d477d19b4c5d'
assert ids[VIS.name]['sha256']=='16ebd1858a7d3235e44207715600861eaa63017a3c665f4fca2d663273a8ca77'
R=H/'received';R.mkdir(exist_ok=False)
with zipfile.ZipFile(Z) as z:
    names=z.namelist();assert len(names)==len(set(x.casefold() for x in names))
    for i in z.infolist():
        p=PurePosixPath(i.filename)
        assert not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename and ':' not in i.filename
        assert not stat.S_ISLNK(i.external_attr>>16)
    assert z.testzip() is None
    mf=json.loads(z.read('MANIFEST.json'))['files'];assert set(names)==set(mf)|{'MANIFEST.json'}
    for name,record in mf.items():assert bid(z.read(name))==record,name
    z.extractall(R)
assert ident(P)==ident(R/P.name)
mapping=j(R/'SOURCE_PATH_MAP.json');pres=j(R/'SOURCE_PRESERVATION.json');assert pres['before']==pres['after']
for ref in mapping:
    expected={k:ref[k] for k in ['bytes','sha256']};assert ident(R/ref['member'])==expected
    before=next(r for r in pres['before'] if r['path']==ref['original_path']);assert expected=={k:before[k] for k in expected}
source_cross=[]
with zipfile.ZipFile(OLD) as oz,zipfile.ZipFile(VIS) as vz:
    for ref in mapping:
        member=ref['member'];path=member.replace('source/','workspace/',1)
        if path in oz.namelist():assert bid(oz.read(path))==ident(R/member);source_cross.append(member)
        elif member.endswith('/time_series_0_5s.csv'):
            assert bid(vz.read('b020_results_visual_summary_20260928/time_series_0_5s.csv'))==ident(R/member);source_cross.append(member)
F=R/'source/outputs/b020_profile_unit_stages_20260927/runtime/b020/output'
n=num(F/'preflight_boundary1.csv');p=num(F/'preflight_boundary4.csv')
rr=num(R/'voltage_decomposition_987_times.csv')
previous=num(R/'source/outputs/b020_results_visual_summary_20260928/time_series_0_5s.csv')
times=[r['time_s'] for r in n];assert len(times)==987 and times==sorted(set(times)) and times[0]==0 and times[-1]==5
assert all([r['time_s'] for r in rows_]==times for rows_ in [p,rr,previous])
terms={'Eeq':'Eeq_V','etaMid':'etamid_V','phiL':'phil_V'}
v0=p[0]['phis_V']-n[0]['phis_V'];expected=[]
for i,t in enumerate(times):
    x={'time_s':t,'terminal_voltage_V':p[i]['phis_V']-n[i]['phis_V']}
    x['voltage_change_mV']=(x['terminal_voltage_V']-v0)*1000
    for term,col in terms.items():
        spatial=p[i][col]-n[i][col]
        x[term+'_P_minus_N_V']=spatial
        x[term+'_N_signed_change_mV']=-(n[i][col]-n[0][col])*1000
        x[term+'_P_signed_change_mV']=(p[i][col]-p[0][col])*1000
        x[term+'_change_mV']=(spatial-(p[0][col]-n[0][col]))*1000
        assert x[term+'_change_mV']==x[term+'_N_signed_change_mV']+x[term+'_P_signed_change_mV']
        assert previous[i]['delta_'+term+'_V']==spatial
    x['sum_component_changes_mV']=sum(x[term+'_change_mV'] for term in terms)
    x['identity_residual_V']=x['terminal_voltage_V']-sum(x[term+'_P_minus_N_V'] for term in terms)
    x['change_residual_V']=(x['voltage_change_mV']-x['sum_component_changes_mV'])/1000
    for side,data in [('N',n),('P',p)]:
        for col in ['x_surface','Eeq_V','etamid_V','phil_V']:x[side+'_'+col]=data[i][col]
    assert set(x)==set(rr[i]) and x==rr[i],i
    assert previous[i]['terminal_voltage_V']==x['terminal_voltage_V']
    expected.append(x)
last=expected[-1];elec=rows(R/'electrode_contributions_at_5s.csv');assert len(elec)==6
assert len({(r['term'],r['electrode']) for r in elec})==6
for row in elec:
    term=row['term'];e=row['electrode'];data=n if e=='N' else p;sign=-1 if e=='N' else 1;col=terms[term]
    exp={'boundary_id':1 if e=='N' else 4,'initial_V':data[0][col],'final_V':data[-1][col],'temporal_change_mV':(data[-1][col]-data[0][col])*1000,'voltage_sign':sign,'signed_voltage_contribution_mV':last[term+'_'+e+'_signed_change_mV']}
    assert all(D(row[k])==D(v) for k,v in exp.items())
s=j(R/'SUMMARY.json');assert s['stored_times']==987 and s['computation_decimal_precision']==50
assert D(s['terminal_voltage_initial_V'])==v0 and D(s['terminal_voltage_final_V'])==last['terminal_voltage_V'] and D(s['voltage_change_mV'])==last['voltage_change_mV']
for term in terms:
    claim=s['components'][term]
    assert D(claim['initial_P_minus_N_V'])==expected[0][term+'_P_minus_N_V']
    assert D(claim['final_P_minus_N_V'])==last[term+'_P_minus_N_V']
    assert D(claim['change_mV'])==last[term+'_change_mV']
    assert D(claim['signed_share_of_net_change_percent'])==last[term+'_change_mV']/last['voltage_change_mV']*100
for row in s['electrode_components']:
    other=next(r for r in elec if r['term']==row['term'] and r['electrode']==row['electrode'])
    assert all(row[k]==other[k] if k in ['term','electrode'] else D(str(row[k]))==D(other[k]) for k in row)
maxres=max(abs(r['identity_residual_V']) for r in expected)
maxchange=max(abs(r['change_residual_V']) for r in expected)
direct=max(abs(r['Eeq_V']-r['direct_Eeq_surface_V']) for data in [n,p] for r in data)
assert maxres==D(s['max_voltage_identity_residual_V'])==D('6.82e-16')
assert maxchange==D(s['max_change_identity_residual_V'])==D('9.11e-16')
assert direct==D(s['max_Eeq_direct_surface_difference_V'])==0
assert maxres<D('1e-8') and maxchange<D('1e-8')
rank=sorted(((r['term']+'_'+r['electrode'],D(r['signed_voltage_contribution_mV'])) for r in elec),key=lambda x:x[1],reverse=True)
assert rank[0][0]=='Eeq_N'
pdf=PdfReader(P);assert len(pdf.pages)==1
text=pdf.pages[0].extract_text();(H/'PDF_TEXT.txt').write_text(text,encoding='utf-8')
for token in ['+123.563','-2.772','+0.774','+121.565','6.820E-16','INCOMPLETE','UNVERIFIED']:assert token in text,token
md=(R/'REPORT_KO.md').read_text(encoding='utf-8');tablechecks=0
for line in md.splitlines():
    if not line.startswith('|'):continue
    cells=[x.strip() for x in line.split('|')[1:-1]]
    try:t=D(cells[0])
    except Exception:continue
    row=expected[times.index(t)]
    for v,col in zip(cells[1:],['voltage_change_mV','Eeq_change_mV','etaMid_change_mV','phiL_change_mV']):assert D(v)==row[col].quantize(D('0.000001'));tablechecks+=1
assert ids=={p.name:ident(p) for p in [Z,P,OLD,VIS]}
a={'decision':'ACCEPT_BOUNDED_ALGEBRAIC_DECOMPOSITION','inputs':ids,'package_payloads':len(mf),'manifest_sha256':ident(R/'MANIFEST.json')['sha256'],'CRC_exact_set_safe_names':True,'standalone_pdf_identical':True,'source_records_in_package_verified':5,'previously_received_sources_byte_matched':source_cross,'sender_before_after_records_equal':True,'remote_preservation_independently_observed':False,'time_rows':987,'numeric_columns':len(rr[0]),'all_exported_numeric_cells_exactly_recomputed':True,'N_P_contributions_exact_sum':True,'summary_verified':True,'rounded_time_table_cells':tablechecks,'endpoint_components':s['components'],'electrode_components':s['electrode_components'],'ranked_signed_contributions_mV':[(k,str(v)) for k,v in rank],'voltage_change_mV':str(last['voltage_change_mV']),'max_identity_residual_V':str(maxres),'max_change_residual_V':str(maxchange),'max_direct_surface_difference_V':str(direct),'PDF_pages':1,'source_inputs_unchanged':True,'COMSOL_JVM_received_code_calls':0,'original_overall':'INCOMPLETE','new_execution_approved':False}
(H/'AUDIT.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:a[k] for k in ['decision','package_payloads','time_rows','numeric_columns','ranked_signed_contributions_mV','max_identity_residual_V','max_change_residual_V']},ensure_ascii=False))
