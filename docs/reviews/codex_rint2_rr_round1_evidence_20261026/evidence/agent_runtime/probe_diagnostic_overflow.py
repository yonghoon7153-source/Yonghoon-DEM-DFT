import runtime_bootstrap as boot
import importlib.util, json, warnings
import numpy as np
from scipy import sparse
import step3_conv_cert as cc

ix=np.arange(3); gb=np.full(3,8e307); gt=np.ones(3); phi=np.full(3,.2)
L=sparse.diags(gb+gt,format='csr'); b=gb.copy()
args=(L,b,phi,ix,gb,ix,gt)
out={}
for mode in ('default','warnings_error'):
    try:
        with warnings.catch_warnings(record=True) as seen:
            warnings.simplefilter('error' if mode == 'warnings_error' else 'always')
            r=cc.target_bracket(*args)
        out[mode]={'warnings':[str(w.message) for w in seen], 'ledger_ok':r['target_ledger_ok'],
                   'target_U':r['target_U'], 'target_kcl_raw':str(r['target_kcl_raw']), 'target_lo':r['target_lo'], 'target_hi':r['target_hi']}
    except Exception as e:
        import traceback
        out[mode]={'exception':str(e),'type':type(e).__name__,'traceback':traceback.format_exc()}
with warnings.catch_warnings(record=True) as ws:
    warnings.simplefilter('always')
    c=cc.certify(L,b,phi,0,0.,1e-12,ix,gb,ix,gt,1.,lambda A,b,x0,rt:(x0,0))
out['certify']={k:c[k] for k in ('status','ok','pass_a','pass_b','pass_c','pass_d')}
path=boot.ROOT/'evidence'/'agent_runtime'/'diagnostic_overflow.json'
path.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2))


