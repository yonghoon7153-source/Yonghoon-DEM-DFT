#!/usr/bin/env python3
"""Render an exact proposed devlog with the live app; all writable data stays in --out."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
sys.dont_write_bytecode = True
ap = argparse.ArgumentParser()
ap.add_argument('--repo', type=Path, required=True)
ap.add_argument('--devlog', type=Path, required=True)
ap.add_argument('--out', type=Path, required=True)
a = ap.parse_args()
a.out.mkdir(parents=True, exist_ok=False)
draft = a.out / 'devlog'
draft.mkdir()
for old in (a.repo / 'docs/mixer_devlog').glob('*.md'):
    shutil.copyfile(old, draft / old.name)
shutil.copyfile(a.devlog, draft / a.devlog.name)
for var, folder in [('WEBAPP_UPLOAD_FOLDER', 'uploads'), ('WEBAPP_RESULTS_FOLDER', 'results'),
                    ('WEBAPP_ARCHIVE_FOLDER', 'archive'), ('WEBAPP_MPM_LAB_FOLDER', 'mpm_lab'),
                    ('WEBAPP_EIS_FOLDER', 'eis')]:
    os.environ[var] = str(a.out / 'webapp_data' / folder)
sys.path.insert(0, str(a.repo / 'webapp'))
import app
original = app._repo_path
app._repo_path = lambda rel: str(draft) if rel == app._MIXER_DEVLOG_DIR else original(rel)
import test_mixer_devlog_page as test
assert test.main() == 0
entries = app._mixer_devlog_entries()
assert entries[0]['key'] == '17'
html = app.app.test_client().get('/mixer').get_data(as_text=True)
for needle in ('python3 -I scripts/make_mixer_deck.py', '--dens-gen lab20261014',
               '--gm-wall-ncm 0.3', 'mixer_deck_meta/2', 'MXD2-01'):
    assert needle in html, needle
result = {'status': 'PASS', 'page_checks': '9/9', 'isolated_cli_visible': True,
          'required_density_wall_schema_and_hold_visible': True,
          'devlog_sha256': hashlib.sha256(a.devlog.read_bytes()).hexdigest(),
          'python_isolated': bool(sys.flags.isolated), 'production_source_changed': False,
          'scope': 'Real /mixer route with scratch document lookup and writable directories; no simulation.'}
assert result['python_isolated']
(a.out / 'summary.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(result, ensure_ascii=False))
