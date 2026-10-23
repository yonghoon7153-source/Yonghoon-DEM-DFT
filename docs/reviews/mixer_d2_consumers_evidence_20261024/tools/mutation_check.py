#!/usr/bin/env python3
"""Remove one consumer guard per isolated copy, then run the real regression suite."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--scripts',type=Path,default=Path(__file__).parent/'scripts')
    ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    specs=[
        ('deck_hash',"message == 'metadata SHA256 != actual deck'"),
        ('deck_bytes',"message == 'metadata bytes != actual deck'"),
        ('actual_density',"message.startswith('actual density ')"),
        ('absolute_bo',"message.startswith('absolute printed SE Bo:')"),
        ('gravity',"message == 'actual gravity != declared mixer gravity'"),
        ('mass_fraction',"message == 'actual distribution fraction != ratified active-phase mass recipe'"),
        ('plan_total',"message == 'actual planned counts != metadata total'"),
        ('first_seed',"message == 'actual insertion seed != metadata'"),
        ('unknown_meta',"message == 'unknown metadata keys'"),
        ('ascii_numeric',"message.endswith(': ASCII decimal token required before float conversion')"),
        ('duplicate_json',"message.startswith('duplicate metadata key:')"),
        ('pair_non_ced',"message == 'non-CED command tokens differ (geometry/seed/gravity/material/time/etc.)'"),
        ('pair_orientation',"message == 'pair direction must be uncoated rho -> coated 1'"),
        ('command_scope',"message == 'unsupported command/control flow in development deck'"),
        ('insertion_lifetime',"message == 'first insertion lifecycle differs'"),
        ('sphere_integrator',"message == 'one persistent sphere integrator required before insertion run'"),
        ('rotation_order',"message == 'mesh rotation must follow both settling runs'"),
        ('insertion_region',"message == 'insertion region/reference order'"),
        ('overlap_ceiling',"message == 'static pair overlap exceeds 1%'"),
    ]
    files=[p.name for p in a.scripts.glob('*.py')]
    rows=[]
    for name,skip in [('clean',None)]+specs:
        dst=a.out/name/'scripts';dst.mkdir(parents=True,exist_ok=True)
        for file in files: shutil.copy2(a.scripts/file,dst/file)
        path=dst/'mixer_deck_readback.py';text=path.read_text()
        if skip:
            old='    if not condition:\n        raise ValueError(message)'
            assert text.count(old)==1
            text=text.replace(old,'    if not condition and not ('+skip+'):\n        raise ValueError(message)')
            path.write_text(text)
        cmd=[sys.executable,'-I',str(dst/'test_mixer_d2_consumers.py')]
        run=subprocess.run(cmd,capture_output=True,text=True)
        (a.out/name/'stdout.log').write_text(run.stdout)
        (a.out/name/'stderr.log').write_text(run.stderr)
        row=dict(case=name,skip_guard_condition=skip,source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                 command=cmd,returncode=run.returncode,expected_returncode='zero' if skip is None else 'nonzero',
                 caught=run.returncode!=0 if skip else run.returncode==0)
        rows.append(row);print(json.dumps(row),flush=True)
    result=dict(clean_pass=rows[0]['caught'],mutations=len(specs),caught=sum(r['caught'] for r in rows[1:]),
                all_expected=all(r['caught'] for r in rows),results=rows)
    (a.out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    return 0 if result['all_expected'] else 1

if __name__=='__main__': raise SystemExit(main())
