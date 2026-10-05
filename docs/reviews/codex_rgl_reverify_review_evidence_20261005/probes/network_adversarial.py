"""Pinned actual network CLI -> actual app gate; independent coherent mutations.
Only temporary review fixtures are written; production source stays byte-identical.
"""
from pathlib import Path
import sys, json, tempfile, contextlib, io, hashlib, subprocess
R=Path(__file__).resolve().parents[1]; S=R/'source'; E=R/'evidence'
sys.path[:0]=[str(S/'webapp'),str(S/'scripts')]
import app, pipeline_service as ps, test_pipeline_provenance as TP, tau_flux as tf

def hashes(d):
    return {n:hashlib.sha256((d/n).read_bytes()).hexdigest() for n in (*TP._NET_FOUR,ps.PROVENANCE_FILE,'full_metrics.json') if (d/n).is_file()}

def probe(name,edit=None,bed='through',stop=True,break_solver=False,repeat=False,crash=False):
    d=Path(tempfile.mkdtemp(prefix=name+'_',dir=E)); a,c=TP._write_bed(str(d),bed)
    (d/'full_metrics.json').write_text(json.dumps(TP._bed_ledger(bed)),encoding='utf8')
    stdout=io.StringIO(); stages=[]; error=None
    before={}
    def run(runner):
        return app._network_and_stage_e(str(d),str(S/'scripts'),a,c,'1:SE',1,[],runner=runner,stop_before_stage_e=stop)
    with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stdout):
        if repeat:
            run(TP._CLIRunner()); before=hashes(d)
        mut=(lambda path:TP._edit_net_records(path,edit)) if edit else None
        cli=TP._CLIRunner(mutate=mut,break_solver=break_solver,delegate=TP._fake_stage_e)
        if crash:
            original=ps.atomic_write_json
            def injected(path,*args,**kwargs):
                if Path(path).name=='full_metrics.json': raise OSError('review injection: full_metrics write failure')
                return original(path,*args,**kwargs)
            ps.atomic_write_json=injected
        try: stages,rid=run(cli)
        except Exception as ex:error=type(ex).__name__+': '+str(ex)
        finally:
            if crash:ps.atomic_write_json=original
    (d/'probe.log').write_text(stdout.getvalue(),encoding='utf8')
    fm=json.loads((d/'full_metrics.json').read_text(encoding='utf8'))
    dual=json.loads((d/'network_conductivity_dual.json').read_text(encoding='utf8')) if (d/'network_conductivity_dual.json').is_file() else {}
    tau=tf.case_row(str(d)); gt2,gs0=tf.tau2_from_metrics(fm)
    prov=ps.read_network_provenance(str(d)) or {}
    after=hashes(d)
    ans=dict(name=name,bed=bed,stop=stop,stage_e_stub=not stop,status=('EXCEPTION' if error else ps.summarize(stages)[0]),error=error,
        stages=stages, path=str(d.relative_to(R)),candidate_preserved=bool(dual),
        previous_hashes=before,current_hashes=after,previous_generation_identical=before==after if repeat else None,
        provenance=prov,full_metrics_run_id=fm.get('network_run_id'),fm_status=fm.get('network_solver_status'),
        tau=tau,grade_tau2=gt2,grade_sigma0=gs0,
        hertz={k:dual.get('hertzian',{}).get(k) for k in ('sigma_full','sigma_full_mScm','sigma_full_status','phi_se','boundary_rule','percolating_fraction')})
    return ans

def upd(**kw):
    return lambda rec,n,m:rec.update(kw)

if __name__=='__main__':
    cases=[('positive',{}),('no_through',dict(bed='nonthrough')),('legitimate_band',dict(bed='band_l1')),
        ('solver_failed_stop',dict(break_solver=True)),('solver_failed_general',dict(break_solver=True,stop=False)),
        ('ratio_times4',dict(edit=lambda rec,n,m:rec.update(sigma_full=rec['sigma_full']*4))),
        ('band_ratio_missing',dict(bed='band_l1',edit=upd(sigma_full=None))),
        ('band_ratio_nan',dict(bed='band_l1',edit=upd(sigma_full=float('nan')))),
        ('band_ratio_negative',dict(bed='band_l1',edit=upd(sigma_full=-1))),
        ('band_fraction_above1',dict(bed='band_l1',edit=upd(percolating_fraction=2))),
        ('rejected_retry_preserves_generation',dict(repeat=True,edit=upd(sigma_full_status='not_computed'))),
        ('write_failure_after_stamp',dict(repeat=True,crash=True))]
    results=[]
    for name,kw in cases:
        try:
            x=probe(name,**kw);results.append(x)
            print(json.dumps({k:x[k] for k in ('name','status','error','previous_generation_identical','hertz','grade_tau2')},ensure_ascii=False),flush=True)
        except Exception as e:
            import traceback
            traceback.print_exc(); results.append(dict(name=name,harness_error=repr(e)))
    by={x['name']:x for x in results}
    assert not any('harness_error' in x for x in results)
    assert by['positive']['status']=='done' and by['no_through']['status']=='done'
    assert by['solver_failed_stop']['status']=='failed'
    assert by['rejected_retry_preserves_generation']['previous_generation_identical'] is True
    assert by['ratio_times4']['tau']['tau2_ion_hertz']==by['positive']['tau']['tau2_ion_hertz']/4
    assert by['band_ratio_nan']['status']=='done' and by['band_ratio_negative']['status']=='done'
    assert by['write_failure_after_stamp']['status']=='EXCEPTION'
    (E/'network_adversarial.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf8')
