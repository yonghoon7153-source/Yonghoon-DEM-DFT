"""Independent R17 counterexamples. Only creates/mutates disposable review fixtures."""
import contextlib, copy, csv, hashlib, importlib.util, io, json, os, pathlib, shutil, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1] / 'work' / 'r17-head' / 'bms-balancing'
sys.path.insert(0, str(ROOT))
os.environ['PYTHONUTF8'] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

def module(name, path):
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp)
    sys.modules[name] = m
    sp.loader.exec_module(m)
    return m

def run(script, *args):
    p = subprocess.run([sys.executable, str(ROOT/script), *map(str,args)], cwd=ROOT,
                       capture_output=True, text=True, encoding='utf-8', timeout=120)
    return dict(rc=p.returncode, stdout=p.stdout, stderr=p.stderr)

def writecsv(path, rows):
    with path.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    from bms_balancing import verify as V, schema as S
    C = module('r17_check',ROOT/'scripts/check_u14.py')
    G = module('r17_gate',ROOT/'reviews/evidence_gate.py')
    tmp=pathlib.Path(tempfile.mkdtemp(prefix='fixtures-',dir=HERE)).resolve()
    result={'fixtures':str(tmp)}

    # A directory baseline cannot establish the recorded old commit. Production CLI,
    # no decision editing: CURRENT bodies without sidecars get a historical approval.
    old=tmp/'current-as-old';shutil.copytree(ROOT/'out',old,ignore=shutil.ignore_patterns('*.meta.json'))
    for p in old.iterdir():
        if p.suffix=='.csv':
            rows=list(csv.DictReader(io.StringIO(p.read_text(encoding='utf-8-sig'))))
            if rows and 'run_id' in rows[0]:
                for row in rows: row.pop('run_id',None)
                writecsv(p,rows)
        elif p.suffix=='.json':
            body=json.loads(p.read_text(encoding='utf-8-sig'))
            if isinstance(body,dict):
                body.pop('run_id',None)
                p.write_text(json.dumps(body,ensure_ascii=False),encoding='utf-8')
    r=run(pathlib.Path('scripts/check_u14.py'),'--new','out','--old',old)
    result['legacy_directory']=r
    result['legacy_directory']['verdict']=json.loads(next(x[10:] for x in r['stdout'].splitlines() if x.startswith('PROMOTION ')))
    result['legacy_directory']['recorded_old_rev']=C.load_decisions()['legacy_transitions'][-1]['old']['rev']
    result['legacy_wrong_rev_control']=C.legacy_transition(set(C.load_decisions()['legacy_transitions'][-1]['new']['roster']),
        set(C.load_decisions()['legacy_transitions'][-1]['code_commits']), 'f'*40,
        {'env_contract_legacy':13},C.load_decisions())

    # Shared attempt IDs are normal: one run can produce multiple matrix states.
    # state100/A is old, but state200/A is its most recent and must survive keep=1.
    out=tmp/'gc-safe-fixture';out.mkdir()
    entries=[]
    for name,rid,body in [('matrix_100.csv','A','100-old'),('matrix_200.csv','A','200-only'),('matrix_100.csv','B','100-new')]:
        canonical=out/name
        d=V.publish_target(canonical,'partial',run_id=rid)
        d.write_text(body,encoding='utf-8')
        # Build the documented index directly: production writer uses POSIX fcntl,
        # unavailable in this Windows environment. The GC code itself is unmodified.
        entries.append(dict(kind='matrix',attempt=rid,artifact=name,status='partial',
                            path=str(d.relative_to(out/'partial')),
                            sha256=hashlib.sha256(d.read_bytes()).hexdigest(),recorded_utc='2026-09-22T00:00:00Z'))
    (out/'partial/index.json').write_text(json.dumps({'index_version':1,'attempts':entries}),encoding='utf-8')
    victim=(out/'partial/matrix/A/matrix_200.csv').resolve()
    assert victim.is_relative_to(tmp) and out.resolve().is_relative_to(tmp)
    before=json.loads((out/'partial/index.json').read_text(encoding='utf-8'))
    r=run(pathlib.Path('scripts/gc_partial.py'),'--root',out,'--keep','1','--apply')
    result['gc_shared_attempt']={**r,'victim_survives':victim.exists(),'before':before,
        'after':json.loads((out/'partial/index.json').read_text(encoding='utf-8')),
        'deletion_scope':'only newly-created fixture under this review directory'}

    # Reporter fixtures have all production column names. Invalidity varies one axis.
    base={k:'1' for k in S.CYCLES_ROW}
    base.update(cell='syn',cycle='0',width_status='measured',width_tol='0.01',width_is_lower_bound='True')
    consumed={'full_cell':{'path':'cell.xlsx','sha256':'a'*64},
              'half_cell':{'path':'half.xlsx','sha256':'c'*64},
              'literature':{'gr':{'path':'gr.xlsx','sha256':'d'*64},
                            'si':{'path':'si.xlsx','sha256':'e'*64}}}
    base.update(consumed_inputs=json.dumps(consumed),inputs_sha=S.inputs_digest(consumed))
    for m in ('LAM_PE','LAM_NE','LLI'):
        base.update({m:'0',m+'_lo':'-0.01',m+'_hi':'0.01'})
    def pair(name, change=None, meta_change=None):
        d=tmp/name;d.mkdir()
        paths=[]
        for i in (0,1):
            rows=[dict(base,cycle=str(k)) for k in (0,1)]
            meta={'lb':[0.1,-0.2,0.1,-0.2,0], 'ub':[2,0.5,2,0.5,1],
                  'initial':[1,0,1,0,0.25], 'gamma_prefit':False,'gamma_lb':0,
                  'n_multistart':20,'seed':0,'scale_seed':0,'w_pocv':1,'w_dvdq':1,
                  'w_dqdv':i,'optimizer':'SLSQP','widths':True,'width_tol':0.01,
                  'width_starts':4,'width_method':'constrained-extrema','width_grid':0,
                  'cell':'syn','si_source':'external','starts':20,'cycles':[0,1],
                  'consumed_inputs':copy.deepcopy(consumed),
                  'env':{'python':'3.12','numpy':'2.5.3','scipy':'1.18.1','pandas':'3.0.6','openpyxl':'3.1.5','platform':'Windows'},
                  'code':{'commit':'same-code'}}
            if i and change:change(rows)
            if i and meta_change:meta_change(meta)
            for row in rows:
                row.update(consumed_inputs=json.dumps(meta['consumed_inputs']),
                           inputs_sha=S.inputs_digest(meta['consumed_inputs']))
            p=d/f'{i}.csv';writecsv(p,rows)
            meta['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
            p.with_name(p.name+'.meta.json').write_text(json.dumps(meta),encoding='utf-8')
            paths.append(p)
        return run(pathlib.Path('scripts/width_report.py'),*paths,'--axis','w_dqdv')
    result['width_positive_control']=pair('width-positive-control')
    result['width_negative_control']=pair('different-seed',meta_change=lambda m:m.update(seed=1))
    result['width_different_inputs']=pair('different-inputs',meta_change=lambda m:m['consumed_inputs']['full_cell'].update(sha256='b'*64))
    result['width_missing_cycle']=pair('missing-cycle',change=lambda rows:rows.pop())
    result['width_duplicate_cycle']=pair('duplicate-cycle',change=lambda rows:rows.append(dict(rows[0],LAM_NE_hi='0.9')))
    result['width_nan']=pair('nan',change=lambda rows:rows[0].update(LAM_NE_hi='nan'))
    result['width_blank_tol']=pair('blank-tol',change=lambda rows:rows[0].update(width_tol=''))
    # Schema accepts nonempty but false/invalid lower-bound tag, inverted interval.
    result['union_checks']={}
    for label,change in {'False-tag':{'width_is_lower_bound':'False'},'garbage-tag':{'width_is_lower_bound':'banana'},
                         'negative-tol':{'width_tol':'-0.5'},'inverted':{'LAM_NE_lo':'0.2','LAM_NE_hi':'-0.2'}}.items():
        row=dict(base,**change)
        result['union_checks'][label]={'union':S.check_width_union(row),'whole_schema':S.check_rows('cycles',[row],list(S.CYCLES_ROW),'cycles_syn.csv')}
    result['union_positive_control']=S.check_rows('cycles',[base],list(S.CYCLES_ROW),'cycles_syn.csv')
    # Resolve path from the unmodified public publisher without writing it.
    outside=tmp/'outside-partial';outside.mkdir()
    escaped=V.publish_target(tmp/'isolated-out/matrix_100.csv','partial',run_id=str(outside))
    result['partial_absolute_attempt']={'resolved':str(escaped),'under_partial':escaped.is_relative_to(tmp/'isolated-out/partial')}
    canonical=tmp/'canonical-fixture/matrix_100.csv'
    canonical.parent.mkdir()
    resolved=V.publish_target(canonical,'partial',run_id=str(canonical.parent))
    result['partial_canonical_target']={'canonical':str(canonical),'actual_partial_destination':str(resolved),
                                       'is_canonical':resolved.resolve()==canonical.resolve(),
                                       'payload_write_performed':False}

    # An incomplete receipt with no runtime/package/version passes the real verifier.
    git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
    receipt={'code':{'commit':git('rev-parse','HEAD'),'tree':git('rev-parse','HEAD^{tree}')},
             'instrument':{'reviews/evidence_gate.py':git('rev-parse','HEAD:./reviews/evidence_gate.py')}}
    receipt['signature']=G.receipt_signature(receipt)
    rp=tmp/'incomplete-receipt.json';rp.write_text(json.dumps(receipt),encoding='utf-8')
    result['incomplete_run_receipt']=run(pathlib.Path('scripts/verify_run_receipt.py'),'--receipt',rp,'--target',ROOT)
    # Assertions are the review's expected BAD observations, not pass claims for the target.
    assert result['legacy_directory']['verdict']['legacy_transition_approved'] is True
    assert result['legacy_directory']['verdict']['promotion_eligible'] is False
    assert result['gc_shared_attempt']['rc']==0 and not result['gc_shared_attempt']['victim_survives']
    assert result['width_positive_control']['rc']==0 and result['width_negative_control']['rc']==2
    assert all(result[k]['rc']==0 for k in ('width_different_inputs','width_missing_cycle','width_duplicate_cycle','width_nan','width_blank_tol'))
    assert all(not x['whole_schema'] for x in result['union_checks'].values())
    assert not result['union_positive_control']
    assert result['partial_canonical_target']['is_canonical']
    assert result['incomplete_run_receipt']['rc']==0

    p=HERE/'REPRO_RESULTS.json';p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Saved',p)
    for k,v in result.items():
        if isinstance(v,dict):print(k, 'rc='+str(v.get('rc')),v.get('victim_survives',''),v.get('verdict',{}).get('legacy_transition_approved',''))

if __name__=='__main__':main()
