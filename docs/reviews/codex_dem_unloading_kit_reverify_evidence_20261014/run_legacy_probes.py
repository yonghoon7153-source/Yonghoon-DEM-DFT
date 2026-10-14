"""Run archived probes verbatim; old 'bug exists' assertions are not pass criteria."""
from pathlib import Path
import sys, subprocess, json, os
R=Path(__file__).resolve().parent
out=[]
for name in ('reader_adversarial','reader_continuation','observer_adversarial','history_restore','deck_control'):
    cmd=[sys.executable,'-X','utf8','-B',str(R/'legacy_probes'/f'{name}.py')]
    p=subprocess.run(cmd,capture_output=True,text=True,encoding='utf8',errors='replace',timeout=120,
                     env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1'))
    log=p.stdout+'\nSTDERR\n'+p.stderr
    (R/'evidence'/f'legacy_{name}.log').write_text(log,encoding='utf8')
    out.append({'name':name,'argv':cmd,'rc':p.returncode,'tail':log.splitlines()[-8:]})
(R/'evidence/legacy_probe_runs.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(out,ensure_ascii=False,indent=2))
