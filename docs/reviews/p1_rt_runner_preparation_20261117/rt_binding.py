"""Read-only binding evidence for preregistration 15-5 / 15-5d.

PASS means only that the RT binding records agree. No restore verdict, source
seal, certificate, stage execution, or field qualification is produced here.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

KEYS=('job_dir','rt1_bin','rt2_ckpt')
SHA=r'[0-9a-f]{64}'

def _read(path):
    before=path.stat();raw=path.read_bytes();after=path.stat()
    if (before.st_size,before.st_mtime_ns,before.st_ino)!=(after.st_size,after.st_mtime_ns,after.st_ino):
        raise OSError('input changed while reading')
    return raw.decode('utf8')

def parse_manifest(text):
    records={};errors=[]
    for number,line in enumerate(text.splitlines(),1):
        found=re.match(r'^\s*(job_dir|rt1_bin|rt2_ckpt)(?:=|\s|$)',line)
        if not found:continue
        key=found[1]
        if key in records:errors.append('duplicate '+key)
        pattern=key+r'=(\S+)' if key=='job_dir' else key+r'=(\S+) sha256=('+SHA+r')'
        match=re.fullmatch(pattern,line,flags=re.ASCII)
        if match is None or any(c.isspace() for c in (match[1] if match else '')):
            errors.append('malformed '+key+' line '+str(number));records[key]=None
        else:
            value={'path':match[1]}
            if key!='job_dir':value['sha256']=match[2]
            records[key]=value
    return records,errors

def parse_restart_command(text):
    commands=[];errors=[]
    for number,line in enumerate(text.splitlines(),1):
        tokens=line.split('#',1)[0].split()
        if not tokens or tokens[0]!='read_restart':continue
        if len(tokens)!=2:
            errors.append('malformed read_restart line '+str(number));continue
        if '${' not in tokens[1]:commands.append(tokens[1])
    if len(commands)>1:errors.append('multiple expanded read_restart commands')
    return commands,errors

def check_binding(job_dir, *, log_name='log_screen.liggghts', require_ckpt=False, technical_ok=True):
    if log_name not in ('log_screen.liggghts','log.liggghts'):
        raise ValueError('unsupported RT log layout')
    job=Path(job_dir);errors=[];missing=[];records={};commands=[];ckpt=None;actual_sha=None
    if technical_ok is not True:errors.append('RT stage technical failure or unconfirmed technical contract')
    try:records,bad=parse_manifest(_read(job/'run_manifest.txt'));errors.extend(bad)
    except (OSError,UnicodeError):missing.append('manifest unreadable or missing')
    try:commands,bad=parse_restart_command(_read(job/'RT2'/log_name));errors.extend(bad)
    except (OSError,UnicodeError):missing.append('RT2 log unreadable or missing')
    if require_ckpt:
        try:
            raw=_read(job/'RT2/ckpt.txt');parts=raw.splitlines()
            if len(parts)!=1 or not parts[0] or any(c.isspace() for c in parts[0]):errors.append('malformed RT2 ckpt record')
            else:ckpt=parts[0]
        except (OSError,UnicodeError):missing.append('RT2 ckpt record unreadable or missing')
    for key in KEYS:
        if key not in records:missing.append('missing '+key)
    if not commands:missing.append('missing expanded read_restart')
    valid={k:v for k,v in records.items() if v is not None}
    names=[v['path'] for k,v in valid.items() if k!='job_dir']
    if len(commands)==1:names.append(commands[0])
    if ckpt is not None:names.append(ckpt)
    if names and len(set(names))!=1:errors.append('RT producer record/log path spellings differ')
    hashes=[v['sha256'] for k,v in valid.items() if k!='job_dir']
    if len(set(hashes))>1:errors.append('RT1/RT2 recorded hashes differ')
    try:
        real_job=job.resolve(strict=True)
        if not real_job.is_dir():missing.append('job is not a directory')
        if 'job_dir' in valid:
            literal=valid['job_dir']['path'];record_job=Path(literal)
            if not record_job.is_absolute():errors.append('job_dir must be absolute')
            if record_job.resolve()!=real_job:errors.append('recorded job directory is a different attempt')
            expected=literal+'/RT1/rt.bin'
            if any(name!=expected for name in names):errors.append('RT path is not the recorded job RT1 binary spelling')
        target=job/'RT1/rt.bin'
        for name in names:
            if not Path(name).is_absolute() or Path(name).resolve()!=target.resolve():
                errors.append('RT binary resolves outside this attempt')
    except (OSError,RuntimeError):missing.append('job or binary path cannot be resolved')
    # Contradictions already established above survive absent/unreadable files.
    try:
        target=job/'RT1/rt.bin';before=target.stat();h=hashlib.sha256()
        with target.open('rb') as f:
            for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
        after=target.stat()
        if (before.st_size,before.st_mtime_ns,before.st_ino)!=(after.st_size,after.st_mtime_ns,after.st_ino):
            missing.append('rt.bin changed while reading')
        elif not before.st_size:missing.append('empty rt.bin')
        else:
            actual_sha=h.hexdigest()
            if any(value!=actual_sha for value in hashes):errors.append('actual rt.bin hash differs from recorded hash')
    except OSError:missing.append('rt.bin missing or unreadable')
    status='SYNTAX_FAIL' if errors else ('UNCONFIRMED' if missing else 'PASS')
    return {'schema':'rt_binding_readonly_v1','status':status,'errors':errors,'missing':missing,
            'actual_sha256':actual_sha,'record_keys':sorted(records),'expanded_commands':len(commands),
            'physical_qualification':False,'certificate_published':False,
            'scope':'binding only; stage/reset/numeric/grammar/continuity gates remain separate'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('job_dir',type=Path)
    p.add_argument('--fixture',action='store_true');a=p.parse_args()
    r=check_binding(a.job_dir,log_name='log.liggghts' if a.fixture else 'log_screen.liggghts',require_ckpt=a.fixture)
    print(json.dumps(r,sort_keys=True));return 0 if r['status']=='PASS' else 2

if __name__=='__main__':raise SystemExit(main())
