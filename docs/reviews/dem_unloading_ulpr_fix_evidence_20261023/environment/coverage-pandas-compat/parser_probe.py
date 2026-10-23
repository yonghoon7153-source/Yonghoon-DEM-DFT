import argparse,json,pathlib,sys
p=argparse.ArgumentParser();p.add_argument('--repo',required=True);p.add_argument('--fixture',required=True);p.add_argument('--overlay');p.add_argument('--out',required=True);a=p.parse_args()
if a.overlay: sys.path.insert(0,a.overlay)
import pandas as pd,numpy as np
f=pathlib.Path(a.fixture)
result={'pandas':pd.__version__,'numpy':np.__version__,'files':{}}
for name in ['atoms.csv','contacts.csv']:
 df=pd.read_csv(f/name)
 result['files'][name]={'columns':list(df.columns),'dtypes':{str(k):str(v) for k,v in df.dtypes.items()},'rows':[[{'repr':repr(float(v)),'hex':float(v).hex()} for v in row] for row in df.itertuples(index=False,name=None)]}
pathlib.Path(a.out).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
