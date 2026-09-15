"""Deterministic artificial measurements for software checks, not battery evidence."""
import numpy as np
import pandas as pd
from extract_capacity import build_features

def make_demo(cfg,n=12):
    rng=np.random.default_rng(cfg.seed)
    rows=[]
    for i in range(n):
        severity=(i%4)/3
        resistance=20+45*severity+rng.normal(0,2)
        frequency=np.asarray(cfg.frequency_grid_hz,dtype=float)
        z=8+resistance/(1+1j*frequency/300)+(4+2*severity)/(1+1j*frequency/.8)
        spec=pd.DataFrame({'f':frequency,'re':z.real,'im':z.imag,'ocv':3.7-.05*severity+rng.normal(0,.001)})
        features,_=build_features(spec,cfg)
        rows.append({'cell_number':41+i,'batch_id':f'demo_batch_{i//4+1}',
                     'cap':.022-.009*severity+rng.normal(0,.00035),
                     'cc_frac':.9-.25*severity+rng.normal(0,.01),**features})
    return pd.DataFrame(rows)
