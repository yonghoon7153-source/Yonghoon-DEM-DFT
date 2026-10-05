"""Record actual versions used for the local review, not production certification."""
from pathlib import Path
import importlib.metadata,json,os,platform,sys
R=Path(__file__).resolve().parent
out=dict(python=sys.version,executable=sys.executable,platform=platform.platform(),
 packages={n:importlib.metadata.version(n) for n in ('numpy','scipy','pandas','flask')},
 PYTHONPATH=os.environ.get('PYTHONPATH'),scope='Windows isolated synthetic tests; no WSL or real14/campaign execution')
(R/'environment.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(out,ensure_ascii=False,indent=2))
