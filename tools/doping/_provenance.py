"""Provenance helper — collect environment info for reproducibility.

Every output JSON from the doping pipeline should include the dict returned
by ``get_provenance()`` under a ``provenance`` top-level key, so that
reviewers / future-us can identify which model versions and exact code
revision produced a given result.
"""
import datetime
import platform
import subprocess
import sys
from pathlib import Path


def get_provenance() -> dict:
    """Collect runtime environment info."""
    info: dict = {
        'timestamp_iso': datetime.datetime.now().astimezone().isoformat(),
        'python_version': sys.version.split()[0],
        'platform': platform.platform(),
        'machine': platform.machine(),
        'hostname': platform.node(),
    }
    for pkg in ['ase', 'numpy', 'scipy', 'fairchem', 'torch']:
        try:
            mod = __import__(pkg)
            info[f'{pkg}_version'] = getattr(mod, '__version__', 'unknown')
        except ImportError:
            info[f'{pkg}_version'] = 'not_installed'
    # UMA-specific
    info['uma_model_name'] = 'uma-s-1p1'  # whatever load_uma_calc uses
    info['uma_task_name'] = 'omat'         # default in load_uma_calc

    # Git provenance (best-effort; works only if invoked inside repo)
    try:
        repo_root = Path(__file__).resolve().parent.parent.parent
        commit = subprocess.check_output(
            ['git', '-C', str(repo_root), 'rev-parse', 'HEAD'],
            stderr=subprocess.DEVNULL).decode().strip()
        info['git_commit'] = commit
        branch = subprocess.check_output(
            ['git', '-C', str(repo_root), 'rev-parse', '--abbrev-ref', 'HEAD'],
            stderr=subprocess.DEVNULL).decode().strip()
        info['git_branch'] = branch
        # Check if working tree has uncommitted changes (i.e., the run
        # used unsaved code modifications — provenance warning)
        dirty = subprocess.check_output(
            ['git', '-C', str(repo_root), 'status', '--porcelain'],
            stderr=subprocess.DEVNULL).decode().strip()
        info['git_dirty'] = bool(dirty)
    except Exception:
        info['git_commit'] = 'unknown'
        info['git_branch'] = 'unknown'
        info['git_dirty'] = None
    return info
