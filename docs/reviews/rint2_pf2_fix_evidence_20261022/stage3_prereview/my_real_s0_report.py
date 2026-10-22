import hashlib, json, os, sys, tempfile, contextlib, io
SC = sys.argv[1]; WD = sys.argv[2]
sys.path.insert(0, SC)
import test_ca_s0_census as T
import rint_r_chain as R
tmp = tempfile.mkdtemp(dir=WD)
for name, kw in (('kit_SBE_vgcf100', dict(vgcf=[T.F1], ptfe=[T.P1], vol={'VGCF': 0.04, 'PTFE': 0.1})),):
    kit = T.write_kit(tmp, name, **kw)
    out = os.path.join(tmp, 'out_' + name)
    with contextlib.redirect_stdout(io.StringIO()):
        res = T._stage(1, [kit], out)
    rp = os.path.join(out, f's0_stage1_{name}.json')
    raw = open(rp, 'rb').read()
    print('report bytes', len(raw), 'has NaN/Infinity tokens:', any(t in raw for t in (b'NaN', b'Infinity')))
    try:
        rec = R.read_s0_report(rp, 1)
    except R.Stop as e:
        print('read_s0_report STOP', e.code, e.cause[:200]); continue
    psha = hashlib.sha256(open(os.path.join(out, 'cjunc_plan.json'), 'rb').read()).hexdigest()
    print('record:', {k: (v if k != 'file_digests' else [x['file'] for x in v]) for k, v in rec.items() if k not in ('path',)})
    print('s0_stage1_problem:', R.s0_stage1_problem(rec, psha))
    print('s0_code_problem (chain folder = same scripts):', R.s0_code_problem(rec, 'S0 단계 1', R.code_files(R.HERE), None))
