#!/usr/bin/env python3
import os,sys
from pathlib import Path
B=Path(__file__).resolve().parent
repo=Path('/workspace/Yonghoon-DEM-DFT')
draft=B/'deliverables/docs/mixer_devlog'
for old in (repo/'docs/mixer_devlog').glob('*.md'):
 q=draft/old.name
 if not q.exists(): q.symlink_to(old)
for var,folder in [('WEBAPP_UPLOAD_FOLDER','uploads'),('WEBAPP_RESULTS_FOLDER','results'),('WEBAPP_ARCHIVE_FOLDER','archive'),('WEBAPP_MPM_LAB_FOLDER','mpm_lab'),('WEBAPP_EIS_FOLDER','eis')]:
 os.environ[var]=str(B/'webapp_data'/folder)
sys.path.insert(0,str(repo/'webapp'))
import app
orig=app._repo_path
app._repo_path=lambda rel: str(draft) if rel==app._MIXER_DEVLOG_DIR else orig(rel)
import test_mixer_devlog_page as test
assert test.main()==0
entries=app._mixer_devlog_entries();assert entries[0]['key']=='17'
text=app.app.test_client().get('/mixer').get_data(as_text=True)
assert '--dens-gen lab20261014' in text and '--gm-wall-ncm 0.3' in text
assert 'mixer_deck_meta/2' in text and 'MXD2-01' in text
print('draft v17 rendered through real /mixer route: PASS (scratch document lookup only)')
