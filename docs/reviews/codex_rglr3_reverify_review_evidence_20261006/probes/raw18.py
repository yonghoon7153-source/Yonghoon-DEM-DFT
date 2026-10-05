"""Invoke unchanged prior independent raw comparison with new pinned production."""
from pathlib import Path
import json,hashlib
import original_network_probe as p
R=Path(__file__).resolve().parents[1]
b=(Path(__file__).parent/'reference_network_eedada5d3.py').read_bytes()
blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
assert blob=='2e0c4a47721cd8593b039fe1e189419bbb2eea64'
x=dict(reference_blob=blob,old_new=p.old_new(),independent_power=p.independent_power())
(R/'evidence/raw18.json').write_text(json.dumps(x,indent=2),encoding='utf8')
print(json.dumps(x,indent=2))
