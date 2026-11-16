"""Prepare one collection-only retry, preserving original output bytes.

This helper does not submit, cancel, wait for, or execute a simulation. The
frozen original controller is subsequently invoked with --collect only.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

CONTROLLER_SHA='56f2d5ea366e55c987417bc7fea0f777598fb807f21de1887ae4aeea8af2a943'
TERMINAL={'COMPLETED','FAILED','CANCELLED','TIMEOUT','OUT_OF_MEMORY','NODE_FAIL','PREEMPTED','BOOT_FAIL','DEADLINE','REVOKED','SPECIAL_EXIT'}

def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def snapshot(root):
    rows={}
    if root.is_symlink():raise ValueError('linked evidence/return directory')
    for p in sorted(root.rglob('*')):
        if p.is_symlink():raise ValueError('linked evidence/return member')
        if p.is_file():rows[p.relative_to(root).as_posix()]=dict(bytes=p.stat().st_size,sha256=digest(p))
        elif not p.is_dir():raise ValueError('nonregular member')
    return rows

def put(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2);f.write('\n')

def prepare(packet,job,queue,accounting,live_controllers,controller_sha):
    packet=Path(packet).resolve(strict=True)
    if job!='366423' or controller_sha!=CONTROLLER_SHA:raise ValueError('fixed job/controller mismatch')
    history=packet/'collection_history/collect_366423_20261116'
    if history.exists() or history.is_symlink():raise FileExistsError('recovery already prepared; inspect, never rotate again')
    if queue.strip():raise ValueError('job still in queue or ambiguous queue output; no collection')
    rows=[s.split('|') for s in accounting.splitlines() if s.split('|')[0]==job]
    if len(rows)!=1 or len(rows[0])<3:raise ValueError('unique terminal accounting row required')
    state=rows[0][1].split()[0].rstrip('+') if rows[0][1].split() else ''
    if state not in TERMINAL or not re.fullmatch(r'[0-9]+:[0-9]+',rows[0][2]):raise ValueError('terminal state/exit code missing')
    if live_controllers:raise ValueError('old controller still alive; do not move its output')
    if not (packet/'returns').is_dir() or not (packet/'evidence').is_dir():raise ValueError('first output directories missing')
    original={name:snapshot(packet/name) for name in ('returns','evidence')}
    names=set()
    for line in (packet/'returns/SHA256SUMS').read_text(encoding='ascii').splitlines():
        hit=re.fullmatch(r'([0-9a-f]{64})  (e0_report\.tar\.gz|e0_full_result\.tar\.gz)',line)
        if not hit or hit[2] in names:raise ValueError('first return manifest syntax')
        names.add(hit[2])
        if hit[2] not in original['returns'] or original['returns'][hit[2]]['sha256']!=hit[1]:raise ValueError('first return hash mismatch')
    if 'e0_report.tar.gz' not in names:raise ValueError('first report missing')
    if (packet/'collection_history').is_symlink():raise ValueError('linked history parent')
    history.mkdir(parents=True,exist_ok=False)
    record=dict(schema='mixer_e0_collect_recovery_v1',job_id=job,
                history=history.relative_to(packet).as_posix(),original=original,
                terminal=dict(state=state,exit_code=rows[0][2]),scientific_acceptance=False,
                new_submission=False,automatic_retry=False,
                note='directory names change; original file bytes preserved; one recovery only')
    put(history/'BEFORE.json',record)
    # No rollback or implicit second attempt after a partial failure. Preserve
    # the history and stop; BEFORE.json states what was intended to move.
    for name in ('returns','evidence'):
        os.rename(packet/name,history/name)
        if snapshot(history/name)!=original[name]:raise ValueError('history bytes changed while preserving')
    (packet/'evidence').mkdir(exist_ok=False)
    put(packet/'evidence/collection_recovery.json',record)
    put(history/'PRESERVED.json',dict(byte_preservation=True,files=sum(map(len,original.values()))))
    return record

def query(argv):
    r=subprocess.run(argv,capture_output=True,text=True,timeout=30)
    if r.returncode:raise ValueError('scheduler query failed; no collection')
    return r.stdout

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--packet',type=Path,required=True);a=ap.parse_args()
    root=a.packet.resolve(strict=True);controller=root/'controller/mixer_e0_pilot_ibb.py'
    receipt=json.loads((root/'B/docs/reviews/mixer_first8_launch_preparation_20261106/cases/PRECAL_E0/submission.receipt.json').read_bytes())
    if receipt.get('state')!='SUBMITTED' or str(receipt.get('job_id'))!='366423':raise ValueError('job receipt mismatch')
    if not Path('/proc').is_dir():raise ValueError('Linux process inspection required')
    live=[]
    for p in Path('/proc').iterdir():
        if not p.name.isdigit():continue
        try:argv=(p/'cmdline').read_bytes().split(b'\0')
        except FileNotFoundError:continue
        except PermissionError:continue  # Other users are not the approved operator.
        for token in argv:
            if token and Path(os.fsdecode(token)).name=='mixer_e0_pilot_ibb.py':
                candidate=Path(os.fsdecode(token))
                try:
                    if not candidate.is_absolute():candidate=(p/'cwd').resolve(strict=True)/candidate
                    if candidate.resolve(strict=True)==controller:live.append(int(p.name))
                except FileNotFoundError:continue
    queue=query(['squeue','-h','-j','366423','-o','%i|%T'])
    accounting=query(['sacct','-n','-P','-j','366423','--format=JobIDRaw,State,ExitCode,Elapsed,AllocCPUS,NNodes,MaxRSS'])
    r=prepare(root,'366423',queue,accounting,live,digest(controller))
    print('PRESERVED_FIRST_COLLECTION job='+r['job_id']+' state='+r['terminal']['state'])

if __name__=='__main__':main()
