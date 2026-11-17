"""Publish complete certificate once using an exclusive same-directory link."""
import json
import os
from pathlib import Path
import tempfile

def _write_complete(fd,data):
    offset=0
    while offset<len(data):
        written=os.write(fd,data[offset:])
        if written<=0:raise OSError('short certificate write')
        offset+=written
    os.fsync(fd)

def publish_new(job,report):
    job=Path(job);target=job/'restore_verdict.json'
    if report.get('schema')!='rt_restore_candidate_v1' or report.get('restore_rule')!='rev5_g2cp' or report.get('status') not in ('RESTORED','UNCONFIRMED','VALUE_MISMATCH','SYNTAX_FAIL'):
        raise ValueError('rev5 report required')
    data=(json.dumps(report,ensure_ascii=False,allow_nan=False,sort_keys=True,indent=2)+'\n').encode('utf8')
    if os.path.lexists(target):raise FileExistsError('certificate destination already exists')
    fd,name=tempfile.mkstemp(prefix='.rt_certificate_',suffix='.tmp',dir=job)
    temporary=Path(name)
    try:
        _write_complete(fd,data)
        os.close(fd);fd=None
        # link() never replaces an existing name, including a broken symlink.
        os.link(temporary,target)
    finally:
        if fd is not None:
            try:os.close(fd)
            except OSError:pass
        temporary.unlink()
    return target
