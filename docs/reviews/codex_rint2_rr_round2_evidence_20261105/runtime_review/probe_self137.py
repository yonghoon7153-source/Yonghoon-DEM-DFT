"""Execute actual e13_cmdlines with mocked /proc bytes only; no kill or solver."""
import builtins, io, json, sys
from pathlib import Path
from unittest.mock import patch
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'received/repo/scripts'))
import test_rint_r_chain_e2e as e
rows=[]
for length in [74,180,1000]:
    raw=(('/'+('long-interpreter-path/'*60))[:length]+'\0-I\0'+('/'+'nested/'*30)+'rint_first_result.py\0marker\0mpm_webapp_payload.py').encode()
    with patch.object(builtins,'open',return_value=io.BytesIO(raw)):
        got=e.e13_cmdlines([424242])
    rows.append({'interpreter_length':length,'old_160_would_see_wrapper':'rint_first_result.py' in raw[:160].decode(),
                 'actual_full_cmdline_has_wrapper':len(got)==1 and 'rint_first_result.py' in got[0],
                 'actual_preserves_full_length':len(got[0])==len(raw)})
(HERE/'self137_results.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf8')
print(json.dumps(rows))
assert all(x['actual_full_cmdline_has_wrapper'] and x['actual_preserves_full_length'] for x in rows)
