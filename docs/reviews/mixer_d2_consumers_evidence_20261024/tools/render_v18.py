#!/usr/bin/env python3
"""Exercise the real /mixer route using a scratch document overlay and data dirs."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--document',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    docs=a.out/'docs';docs.mkdir(exist_ok=True)
    for p in (a.repo/'docs/mixer_devlog').glob('*.md'):shutil.copy2(p,docs/p.name)
    shutil.copy2(a.document,docs/a.document.name)
    for key in ('UPLOAD','RESULTS','ARCHIVE','MPM_LAB'):
        os.environ['WEBAPP_'+key+'_FOLDER']=str((a.out/key.lower()).resolve())
    sys.path.insert(0,str((a.repo/'webapp').resolve()))
    import app
    import test_mixer_devlog_page as test
    original=app._repo_path
    app._repo_path=lambda value: str(docs.resolve()) if value=='docs/mixer_devlog' else original(value)
    status=test.main()
    entries=app._mixer_devlog_entries()
    entry=next(e for e in entries if e['key']=='18')
    page=app.app.test_client().get('/mixer').get_data(as_text=True)
    markers=['--d2','--allow D2','--d2-plan','--d2-meta','python3 -I','execution_authorized','143','99,158','전체 비준']
    checks={marker:marker in page for marker in markers}
    report=dict(status='PASS' if status==0 and all(checks.values()) else 'FAIL',page_checks='9/9' if status==0 else 'FAIL',
                latest_key=entries[0]['key'],two_sections=bool(entry['easy_html'].strip() and entry['detail_html'].strip()),
                markers=checks,document_sha256=hashlib.sha256(a.document.read_bytes()).hexdigest(),
                python_isolated=bool(sys.flags.isolated),production_source_changed=False,
                scope='Real /mixer route, scratch document lookup and writable data folders; no simulator or launch')
    (a.out/'render-summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if report['status']=='PASS' else 1

if __name__=='__main__':raise SystemExit(main())
