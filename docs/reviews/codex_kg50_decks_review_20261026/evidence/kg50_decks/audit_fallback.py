from pathlib import Path
import json,math,re
HERE=Path(__file__).resolve().parent
p=HERE/'fallback50'; m=json.loads((p/'manifest.json').read_text(encoding='utf8')); out=[]
for r in m['cases']:
 c=r['case']; t=(p/c/f'input_{c}.liggghts').read_text(encoding='utf8')
 xyz=list(map(float,re.search(r'^region reg_mix block (.*) units box$',t,re.M).group(1).split()))
 V=(xyz[1]-xyz[0])*(xyz[3]-xyz[2])*(xyz[5]-xyz[4])*1e9*.321
 f=(.85/4.85)/(.85/4.85+.15/1.64); ra=3; rs=float(re.search(r'^variable r_SE\s+equal\s+(\S+)',t,re.M).group(1))*1000
 na=round(V*f/(4/3*math.pi*ra**3)); ns=round(V*(1-f)/(4/3*math.pi*rs**3)); n=na+ns
 at=int(re.search(r'^\s+maxattempt (\d+)',t,re.M).group(1)); safe=n*at*1.3<2**31-1
 out.append(dict(case=c,parsed_counts=[na,ns],manifest_match={'AM_P':na,'SE':ns}==r['counts_pred'],total=n,maxattempt=at,int32_product=n*at,margin_product=n*at*1.3,safe=safe,max_allowed=math.ceil((2**31-1)/(n*1.3))-1))
print(json.dumps(out,indent=2)); (HERE/'fallback-independent.json').write_text(json.dumps(out,indent=2)+'\n')

