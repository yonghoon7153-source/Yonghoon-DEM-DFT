"""Canonical input fingerprints for fixture data, never candidate evaluation."""
import json,base64,hashlib,sys
from decimal import Decimal
def normalize(v):
 if isinstance(v,Decimal):return {'__decimal__':str(v)}
 if isinstance(v,bytes):return {'__bytes_base64__':base64.b64encode(v).decode('ascii')}
 if isinstance(v,dict):return {'__mapping__':[[normalize(k),normalize(x)] for k,x in v.items()]}
 if isinstance(v,(list,tuple)):return [normalize(x) for x in v]
 if isinstance(v,set):return {'__set__':sorted([normalize(x) for x in v],key=lambda x:json.dumps(x,sort_keys=True))}
 return v
def fingerprint(name,args,kwargs):
 obj={'function':name,'args':normalize(args),'kwargs':normalize(kwargs)}
 # The canonical expanded bytes are hashed then discarded, never copied to disk.
 raw=json.dumps(obj,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
 return {'function':name,'canonical_bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
class VerificationProxy:
 def __init__(self,module,expected,profile=None):self.module=module;self.expected=expected;self.index=0;self.profile=profile
 def __getattr__(self,name):
  def invoke(*args,**kwargs):
   observed=fingerprint(name,args,kwargs)
   if self.index>=len(self.expected) or observed!=self.expected[self.index]:raise RuntimeError('FIXTURE_INPUT_SEAL_MISMATCH:'+name)
   self.index+=1
   sys.setprofile(self.profile)
   try:return getattr(self.module,name)(*args,**kwargs)
   finally:sys.setprofile(None)
  return invoke
