"""Independently rerun deferred X6/X3/X5 and F6 on actual producer records."""
import contextlib,io,copy,json
with contextlib.redirect_stdout(io.StringIO()):
    import probe_actual as P
T,C,V,RC,RR=P.T,P.C,P.V,P.RC,P.RR
OUT=P.OUT
cases=[('QD2_3',[T.QD2_A3,T.QD2_B3,T.QD2_C3],T.QD2_S3,T.QD2_N3,1.2),('QDX',T.QDX_POLYS,T.QDX_SDCP,T.QDX_N,2.0),('RAIL5',T.QD5_RAIL5,T.QD4_SDCP,T.QD5_RAIL5_N,1.2),('QD2_1',[T.QD2_A1,T.QD2_B1],T.QD2_S1,T.QD2_N1,1.2),('QD4',T.QD4_POLYS,T.QD4_SDCP,T.QD4_N,1.2)]
x6=[];runs={}
for name,polys,sd,n,th in cases:
    rr=T._qd3_run(polys,sd,n); runs[name]=rr
    m=P.manifest(*rr[:3]); old=copy.deepcopy(m['ca_ext']['cjunc']['evidence']); e=m['ca_ext']['cjunc']['evidence']; rec=P.record(e)
    rec['n_unsplit_bridging_components']=0;rec['upper']=None
    for suffix in ('status','sv_counterfactual_ratio','ratio_limit'):rec[suffix+'_hi']=rec[suffix]
    rec['ratio_cert_interval']=[V._enc(x) for x in V.cert_interval(rec)]
    reject_without_census=RC.ca_ext_record_ok(m)
    e['census']['n_unsplit_bridging_components']=0
    got=RC.ca_ext_record_ok(m)
    x6.append({'name':name,'honest_flags':P.flags(old,th),'edited_flags':P.flags(e,th),'threshold':th,'without_census_edit':reject_without_census,'with_census_edit':got})
    assert reject_without_census[0] is False and got==(True,None) and P.flags(old,th)==['SV_UNCHECKED'] and P.flags(e,th)==[]

rr=runs['QDX'];m=P.manifest(*rr[:3]);e=m['ca_ext']['cjunc']['evidence'];old=copy.deepcopy(e);s=P.record(e)
for k in ('conv_cert','G_cut_code','sv_counterfactual_ratio','ratio_limit'):s[k]=copy.deepcopy(s['upper'][k])
s['ratio_cert_interval']=[V._enc(x) for x in V.cert_interval(s)]
x3={'before':P.flags(old,2.0),'after':P.flags(e,2.0),'contract':RC.ca_ext_record_ok(m),'interval':s['ratio_cert_interval']}
assert x3['contract']==(True,None) and x3['after']==['SV_DEPENDENT']
rr=T._qd3_run([T.QD2_A1,T.QD2_B1C],T.QD2_S1,T.QD2_N1)
x5=[]
for value in [True,False,-1,1.0,'1',None,2**63,10**6]:
    m=P.manifest(*rr[:3]);P.record(m['ca_ext']['cjunc']['evidence'])['n_reach_pairs_cut']=value
    got=RC.ca_ext_record_ok(m);x5.append({'value':value,'contract':got})
    assert got==(True,None)

f6=[]
for name,polys,sd,n,nu in [('one_actual_census0',[T.QD2_A1,T.QD2_B1],T.QD2_S1,T.QD2_N1,0),('two_actual_census1',T.QD4_POLYS,T.QD4_SDCP,T.QD4_N,1)]:
    def hook(reg):reg['census']['n_unsplit_bridging_components']=nu
    sid,reg,r,cf=T._qd2_run(polys,sd,n,reg_hook=hook,cert=True)
    pl=T.plan(reg,1000.0,sv_counterfactual={'threshold':None})
    m=P.manifest(reg,pl,r);e=m['ca_ext']['cjunc']['evidence'];rec=P.record(e)
    f,d=RR.sv_assess({('1','P0','R_j0'):{'sv_cf':V.chain_view(rec)}},2.0,'R_j0')
    why=RR.sv_reasons(f,d)
    result={'case':name,'contract':RC.ca_ext_record_ok(m),'upper_status':rec['status_hi'],'census':nu,'actual_components':rec['upper']['n_components_removed'],'flags':f,'reason':why}
    f6.append(result)
    assert result['contract']==(True,None) and f==['SV_UNCHECKED'] and 'unsplit_census_mismatch' in str(why)

out={'X6':x6,'X3':x3,'X5':x5,'RCA2_06_F6':f6}
(OUT/'deferred_and_f6_results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2,allow_nan=False))
