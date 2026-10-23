"""Path and provenance helpers for local, read-only ULPR evidence runs."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys

REL_KIT = Path('docs/data/ps45_unload_20261009')
SOURCES = ('ul_gates.py', 'ul_reader.py', 'ul_lib.py', 'ul_s3.py',
           'ul_observers.py', 'make_unload_decks.py', 'unload_params.json',
           'history_test/read_history.py', 'history_test/history_params.json',
           'history_test/SHA256SUMS')


def paths(description):
    p = argparse.ArgumentParser(description=description)
    p.add_argument('--repo', type=Path, help='Repository with fixture archives and scripts')
    p.add_argument('--kit', type=Path, help='Override kit; default: REPO/docs/data/ps45_unload_20261009')
    p.add_argument('--out', type=Path, required=True, help='A new output directory; existing evidence is never overwritten')
    a = p.parse_args()
    if a.repo is None:
        if a.kit is None:
            p.error('give --repo or --kit')
        k = a.kit.resolve()
        if k.parent.name != 'data' or k.parent.parent.name != 'docs':
            p.error('a kit outside REPO/docs/data requires --repo for fixture dependencies')
        a.repo = k.parents[2]
    a.repo = a.repo.resolve()
    a.kit = (a.kit or a.repo / REL_KIT).resolve()
    if not a.repo.is_dir() or not a.kit.is_dir():
        p.error('repo and kit must exist')
    a.out = a.out.resolve()
    if a.out.exists():
        p.error('--out must be a new directory')
    a.out.mkdir(parents=True)
    return a


def hashes(kit):
    return {name: hashlib.sha256((kit / name).read_bytes()).hexdigest() for name in SOURCES}


def provenance(a):
    head = subprocess.run(['git', '-C', str(a.repo), 'rev-parse', 'HEAD'], text=True, capture_output=True)
    return {'repo': str(a.repo), 'kit': str(a.kit), 'git_head_context_only': head.stdout.strip() if head.returncode == 0 else None,
            'source_sha256': hashes(a.kit), 'python': sys.version, 'command': [sys.executable] + sys.argv}


def mirror(a):
    """Copy only the kit; link read-only fixture dependencies outside that copy."""
    work = a.out / '_work'
    data = work / 'docs/data'
    data.mkdir(parents=True)
    local_kit = data / REL_KIT.name
    shutil.copytree(a.kit, local_kit, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    for src in (a.repo / 'docs/data').iterdir():
        if src.name != REL_KIT.name:
            (data / src.name).symlink_to(src.resolve(), target_is_directory=src.is_dir())
    for src in (a.repo / 'docs').iterdir():
        if src.name != 'data':
            (work / 'docs' / src.name).symlink_to(src.resolve(), target_is_directory=src.is_dir())
    (work / 'scripts').symlink_to((a.repo / 'scripts').resolve(), target_is_directory=True)
    return work, local_kit


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
