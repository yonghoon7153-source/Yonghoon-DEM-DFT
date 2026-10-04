"""Standard-library illustration only. No submitted code or scientific package import."""
import importlib
import importlib.machinery
import json
import sys
from pathlib import Path
from types import ModuleType

root = Path(__file__).resolve().parent
name = 'g90_inert_origin'
site = root / 'fixtures' / 'site'
stray = root / 'fixtures' / 'stray' / (name + '.py')
assert name not in sys.modules
cached = ModuleType(name)
cached.__file__ = str(stray)
cached.__spec__ = importlib.machinery.ModuleSpec(name, loader=None, origin=str(stray))
sys.modules[name] = cached
try:
    resolved = importlib.machinery.PathFinder.find_spec(name, [str(site)])
    actually_returned = importlib.import_module(name)
    assert actually_returned is cached
    assert resolved.origin != actually_returned.__file__
    print(json.dumps({
        'case':'cached module and current path resolution differ',
        'pathfinder_origin':resolved.origin,
        'import_returned_cached_module':actually_returned is cached,
        'cached_module_origin':actually_returned.__file__,
        'origins_differ':True,
        'submitted_programs_executed':0,
        'scientific_packages_imported':0,
        'fixture_module_bodies_executed':0,
        'scope':'Illustrates Python import semantics, not a dynamic test of tools.env_profile or the submitter environment.'
    },ensure_ascii=False,indent=2))
finally:
    del sys.modules[name]
