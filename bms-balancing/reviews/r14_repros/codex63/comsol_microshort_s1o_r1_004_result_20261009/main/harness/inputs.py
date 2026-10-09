"""Data-only four positive baselines and explicit historical negative deltas."""
import copy
from decimal import Decimal as D
import shared_fixture as f
def inputs():
 raw=b'time_s,value\n0,1\n1,2\n'; units={'time_s':'s','value':'1'}
 return {
 'READ_CTRL_CSV':('read_csv_bytes',(raw,['time_s','value'],f.identity('simple.csv',raw),units,units.copy())),
 'READ_CTRL_TIME':('timed_rows',([{'time_s':D(0)},{'time_s':D(1)}],'1')),
 'READ_CTRL_COVERAGE':('coverage',([D(0),D(1)],[D(0),D(1)],['0','1'],['0','1'],['0','1'],'1')),
 'READ_CTRL_PROFILE':('profile_rows',(f.data([D(0)])['profile_N'][D(0)],[D(0)],f.COORDS['N'],1))}
def negatives():
 out={}; base=inputs()
 for i in range(2,13):
  cid=f'READ{i:02d}'
  ctrl='READ_CTRL_CSV' if i<=7 else 'READ_CTRL_TIME' if i==8 else 'READ_CTRL_COVERAGE' if i<=10 else 'READ_CTRL_PROFILE'
  fn,args=copy.deepcopy(base[ctrl]);a=list(args)
  if i==2:a[2]['sha256']='0'*64;delta=['identity.sha256 ->64 zeros']
  elif i==3:a[3]={'time_s':'ms','value':'1'};delta=['unit_record.time_s s->ms']
  elif i==4:a[1]=['other','value'];delta=['expected_header[0] time_s->other']
  elif i in (5,6,7):
   a[0]={5:b'time_s,value\n0\n',6:b'time_s,value\n0,NaN\n',7:b'time_s,value\n'}[i];a[2]=f.identity('simple.csv',a[0]);delta=['raw bytes replacement','identity bytes/SHA recomputed; path unchanged']
  elif i==8:a[0][1]['time_s']=D(0);delta=['rows[1].time_s1->0']
  elif i==9:a[0]=[D(0)];delta=['times_a removes1']
  elif i==10:
   a[:5]=[[D(0)],[D(0)],['0'],['0'],['0']];delta=['remove1 from times_a,times_b,requests_a,requests_b,common_requests']
  elif i==11:a[0][0]['domain_id']=D(3);delta=['profile[0].domain_id1->3']
  else:a[0].pop();delta=['remove final profile row']
  out[cid]={'control':ctrl,'function':fn,'args':tuple(a),'delta':delta}
 return out
