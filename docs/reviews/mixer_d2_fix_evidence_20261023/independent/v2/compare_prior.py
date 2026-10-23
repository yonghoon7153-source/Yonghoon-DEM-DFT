#!/usr/bin/env python3
"""Compare independently emitted v1 and v2 production output without simulation."""
import argparse
import importlib.util
import itertools
import json
from pathlib import Path

ap=argparse.ArgumentParser()
ap.add_argument('--prior',type=Path,required=True)
ap.add_argument('--current',type=Path,required=True)
ap.add_argument('--out',type=Path,required=True)
args=ap.parse_args()
spec=importlib.util.spec_from_file_location('review_driver',Path(__file__).with_name('reproduce.py'))
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
old=r.module(args.prior,'prior_generator');new=r.module(args.current,'current_generator')
count=0
for gen,cgf,stiff,rho,coating,bo in itertools.product(
        ('gen1','lab20261014'),(75.7,151.4,302.8),(1.,20.),(.03,.3,1.,10.),(False,True),(.73,12.5)):
    a,am=r.emit(old,rho,coating,bo,gen,cgf,stiff)
    b,bm=r.emit(new,rho,coating,bo,gen,cgf,stiff)
    assert a==b, (gen,cgf,stiff,rho,coating,bo)
    # The generator source hash must change because the source was corrected.
    assert am.pop('generator_sha256') != bm.pop('generator_sha256')
    assert am==bm, (gen,cgf,stiff,rho,coating,bo)
    count+=1
result={'decks':count,'all_deck_bytes_equal':True,'metadata_equal_except_generator_source_hash':True}
args.out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
