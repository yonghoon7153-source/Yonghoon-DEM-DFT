"""Pinned actual network CLI -> actual app gate; independent coherent mutations.
Only temporary review fixtures are written; production source stays byte-identical.
"""
from pathlib import Path
import sys, json, tempfile, contextlib, io, hashlib, subprocess, csv
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
            if crash=='attempt_and_restore':
                # A genuinely different second solve, not a forged JSON number.
                with open(c,newline='') as f:
                    rr=csv.DictReader(f); fields=rr.fieldnames; rows=list(rr)
                for row in rows:
                    row['contact_area']=str(float(row['contact_area'])/2)
                    row['delta']=str(float(row['delta'])/2)
                with open(c,'w',newline='') as f:
                    w=csv.DictWriter(f,fields);w.writeheader();w.writerows(rows)
        mut=(lambda path:TP._edit_net_records(path,edit)) if edit else None
        cli=TP._CLIRunner(mutate=mut,break_solver=break_solver,delegate=TP._fake_stage_e)
        if crash:
            original=ps.atomic_write_json
            original_replace=ps._replace_retry
            def injected(path,*args,**kwargs):
                if crash is True and Path(path).name=='full_metrics.json': raise OSError('review injection: full_metrics write failure')
                if crash=='attempt_and_restore' and Path(path).name==ps.ATTEMPT_FILE and args[0].get('latest_attempt_status')=='success':
                    raise OSError('review injection: success attempt write failure')
                return original(path,*args,**kwargs)
            def replace_injected(src,dst,*args,**kwargs):
                if crash=='attempt_and_restore' and Path(src).name.startswith(ps.PUBLISH_BACKUP_PREFIX):
                    raise PermissionError('review injection: full_metrics rollback destination unavailable')
                return original_replace(src,dst,*args,**kwargs)
            ps.atomic_write_json=injected
            ps._replace_retry=replace_injected
        try: stages,rid=run(cli)
        except Exception as ex:error=type(ex).__name__+': '+str(ex)
        finally:
            if crash:
                ps.atomic_write_json=original
                ps._replace_retry=original_replace
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
        attempt=ps.read_network_attempt(str(d)),status_view=ps.network_status_view(str(d)),
        full_metrics_sigma=fm.get('sigma_full_mScm'),
        ui_state_rows=app._network_state_rows(dict(fm,_network_generation=app._network_generation(str(d)))),
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
        ('write_failure_after_stamp',dict(repeat=True,crash=True)),
        ('write_failure_first_run',dict(crash=True)),
        ('general_ratio_times4',dict(stop=False,edit=lambda rec,n,m:rec.update(sigma_full=rec['sigma_full']*4))),
        ('general_band_ratio_missing',dict(stop=False,bed='band_l1',edit=upd(sigma_full=None))),
        ('rollback_destination_failure',dict(repeat=True,crash='attempt_and_restore'))]
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
    for name in ('solver_failed_general','ratio_times4','band_ratio_missing','band_ratio_nan','band_ratio_negative','band_fraction_above1'):
        assert by[name]['status']=='failed', name
    assert by['write_failure_after_stamp']['status']=='failed' and by['write_failure_after_stamp']['previous_generation_identical'] is True
    assert by['write_failure_first_run']['status']=='failed' and not by['write_failure_first_run']['candidate_preserved']
    assert by['general_ratio_times4']['status']=='failed' and by['general_band_ratio_missing']['status']=='failed'
    rb=by['rollback_destination_failure']
    assert rb['status']=='failed' and rb['previous_generation_identical'] is False
    assert rb['provenance']['network_run_id']!=rb['full_metrics_run_id']
    assert rb['hertz']['sigma_full_mScm']!=rb['full_metrics_sigma']
    assert rb['attempt']['previous_generation_kept'] is False and rb['status_view']['active_status']=='invalid'
    assert rb['attempt']['failure_kind']=='rollback_failed'
    assert rb['tau']['ion_net_status_hertz']=='NOT_COMPUTED' and rb['tau']['ion_net_status_reason_hertz'].startswith('generation_invalid')
    (E/'network_adversarial.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf8')
