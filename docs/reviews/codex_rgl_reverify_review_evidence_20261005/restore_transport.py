"""Restore a text transport newline/BOM ONLY if it matches pinned Git blob."""
from pathlib import Path
import hashlib
R=Path(__file__).resolve().parent
p=R/'source/docs/data/lhs_union_20260927/lhsx64_union.tsv'
expect='b58ccd8061c7131bdc21e2507f66c483c0c3e2a7'
b=p.read_bytes(); hits=[]
for bom in (b'',b'\xef\xbb\xbf'):
 for ending in ('LF','CRLF'):
  clean=b.replace(b'\r\n',b'\n')
  for trail in ('same','remove','add'):
   c=clean[:-1] if trail=='remove' else clean+b'\n' if trail=='add' else clean
   if ending=='CRLF':c=c.replace(b'\n',b'\r\n')
   c=bom+c
   if hashlib.sha1(b'blob '+str(len(c)).encode()+b'\0'+c).hexdigest()==expect:
    hits.append((c,ending,trail,bool(bom)))
assert hits,'Transport bytes could not be reconstructed; do not accept unverified source'
p.write_bytes(hits[0][0])
print(dict(bytes=len(hits[0][0]),ending=hits[0][1:],git_blob=expect))
