"""Runs Python unit/selftests only. Does not execute any DEM or shell launcher."""
import json,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1",PYTHONUTF8="1",PYTHONIOENCODING="utf-8")
results={}
for name in ("check_contact_validity","measure_mixing_index","mixer_deck_diff","mixer_restart_phase_test","make_mixer_deck"):
    p=subprocess.run([sys.executable,str(ROOT/"scripts"/(name+".py")),"--selftest"],
                     cwd=ROOT,env=env,capture_output=True,text=True,encoding="utf-8")
    results[name]=dict(returncode=p.returncode,stdout=p.stdout,stderr=p.stderr)
    print(name,p.returncode,p.stdout.strip().splitlines()[-1] if p.stdout.strip() else "")
(ROOT/"selftests_output.json").write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding="utf-8")
if any(x["returncode"] for x in results.values()):raise SystemExit(1)

