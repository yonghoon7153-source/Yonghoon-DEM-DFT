"""Supplement audit: aggregate JSON arithmetic, Hertz elastic reconstruction, history.
No simulation; source/receipt summaries are NOT raw particle measurements.
"""
import hashlib,json,math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'mixer_highbo_round5_evidence_20260928'
sys.path.insert(0,str(BASE/'scripts'))
import make_mixer_deck as gen

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    manifest=json.loads((ROOT/'sources.json').read_text(encoding='utf-8'))
    sources=[]
    for e in manifest['files']:
        raw=(ROOT/e['path']).read_bytes()
        git=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        sources.append(dict(path=e['path'],bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),git_blob_matches=git==e['blob_sha']))
    p=gen.plan(100000,cgf=151.4)
    rp,rs=p['d']['AM_P']/2,p['d']['SE']/2
    nuP,nuS=gen.PHASE_MECH['AM_P'][0],gen.PHASE_MECH['SE'][0]
    e_star=1/((1-nuP**2)/gen.E_PHASE['AM_P']+(1-nuS**2)/gen.E_PHASE['SE'])
    r_star=rp*rs/(rp+rs)
    weight=4*math.pi/3*rp**3*(gen.DENS['AM']*1000)*9.81
    rows=[]
    for seed in gen.CAMPAIGN_SEEDS:
        f=ROOT/'docs/data/mixer_e0_contract_20260928'/f'e0_contract_s{seed}.json'
        e=json.loads(f.read_text(encoding='utf-8'))[0]; pf=e['per_frame'][0]
        delta=e['pp_max']*rs
        force=4/3*e_star*math.sqrt(r_star)*delta**1.5
        rows.append(dict(seed=seed,sha256=sha(f),n_frames=e['n_frames'],step=pf['step'],
            particle_count=sum(e['counts_t0'].values()),n_contact=pf['n_contact'],
            pp_max_pct=e['pp_max']*100,wall_max_pct=e['wall_max']*100,cap_max_pct=pf['cap_max']*100,
            pp_p99_pct=pf['pp_p99']*100,pp_p999_pct=pf['pp_p999']*100,
            pp_median_pct=pf['pp_median']*100,pp_n_over=pf['pp_n_over'],
            pp_fraction_over_pct=pf['pp_n_over']/pf['n_contact']*100,
            wall_n_over=pf['wall_n_over'],wall_touch_particles=pf['wall_n_touch'],
            wall_count_semantics='One nearest-plane maximum per particle; not particle-facet contact count (check_contact_validity.py:448-452,1001-1003).',
            wall_fraction_over_pct=pf['wall_n_over']/pf['wall_n_touch']*100,
            numeric_reject=e['pp_max']>.01 or e['wall_max']>.01,
            counterfactual_p99_only_pass=pf['pp_p99']<=.01,
            same_max_over_r_large_pct=e['pp_max']*rs/rp*100,
            se_se_max_pct=e['pp_max_by_pair']['3-3']*100,
            hertz_elastic_only=dict(delta_um=delta*1e6,force_N=force,AM_P_weight_N=weight,force_over_weight=force/weight)))
    frac=.0048; tail=.05;typical=.00034
    force_share=frac*tail**1.5/(frac*tail**1.5+(1-frac)*typical**1.5)
    energy_share=frac*tail**2.5/(frac*tail**2.5+(1-frac)*typical**2.5)
    refs=('71a00bdd99e8d0a0ee8f3abef6d5df48ae823c17','4cdcbf7bf0feff67bc2a2ae938ea6ca71d67c382','6963632a0f63e344b3994ecbcc00a604b2a0465f')
    history={}
    for ref in refs:
        s=(ROOT/'history'/ref/'mixer_layered_prereg_20260921.md').read_text(encoding='utf-8')
        history[ref]=dict(has_contract_max_1pct='최대 겹침 실측 ≤ 1 %' in s,
            has_section5='## 5.' in s,has_diagnostic_not_decision='보조 진단 (판정에 안 씀' in s)
    a=json.loads((ROOT/'docs/data/mixer_phase_receipt_20260928/receipt_v2.json').read_text(encoding='utf-8'))
    b=json.loads((BASE/'docs/data/mixer_phase_receipt_20260928/receipt_v2_ibb.json').read_text(encoding='utf-8'))
    fields=('step','error_deg','resid_m')
    vals=lambda x:[{k:r[k] for k in fields} for r in x['rows']]
    out=dict(pin=manifest['pin'],sources=sources,rows=rows,
        parameters=dict(rp_m=rp,rs_m=rs,E_star_Pa=e_star,R_star_m=r_star),
        weighted_fraction_counterexample=dict(note='Constructed same-pair elastic contacts, NOT E0 data or a bound on M error.',
            contact_tail_fraction=frac,tail_overlap_over_r=tail,other_overlap_over_r=typical,
            tail_force_share=force_share,tail_elastic_energy_share=energy_share),
        prereg_history=history,
        v2_wsl_ibb=dict(rows_wsl=len(a['rows']),rows_ibb=len(b['rows']),selected_rows_equal=vals(a)==vals(b),
            motion_clock_equal=a['motion_clock']==b['motion_clock'],pos_bound_equal=a['pos_bound_m']==b['pos_bound_m'],
            wsl_sha256=sha(ROOT/'docs/data/mixer_phase_receipt_20260928/receipt_v2.json')))
    assertions=dict(source_blobs=all(x['git_blob_matches'] for x in sources),
        three_numeric_rejects=all(x['numeric_reject'] for x in rows),
        correct_counts=all(x['particle_count']==100000 and x['n_frames']==1 and x['step']==385000 for x in rows),
        percentile_rule_would_flip=all(x['counterfactual_p99_only_pass'] for x in rows),
        original_has_contract_no_section5=history[refs[0]]['has_contract_max_1pct'] and not history[refs[0]]['has_section5'],
        later_section5=history[refs[2]]['has_diagnostic_not_decision'],
        receipt_equal=out['v2_wsl_ibb']['selected_rows_equal'])
    out['assertions']=assertions
    (ROOT/'supplement_output.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(out,ensure_ascii=False,indent=2))
    assert all(assertions.values()),assertions
if __name__=='__main__': main()
