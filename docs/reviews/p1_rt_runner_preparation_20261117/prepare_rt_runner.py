"""Prepare a NEW inactive RT runner layer while preserving the historical kit.

The generated candidate is intentionally not an operational runner: its entry
point exits before preflight. The existing restore publisher cannot be used for
rev5 until the new numeric/grammar/certificate consumers are integrated.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ORIGINAL_SHA='da9a6e7509a2f85cd0e845c1cbe72f1f214f7f92a380a14c26548f04d738c26e'

def render_runner(raw, bridge):
    if hashlib.sha256(raw).hexdigest()!=ORIGINAL_SHA:
        raise ValueError('historical runner bytes differ; do not guess patch anchors')
    text=raw.decode('utf8')
    edits=[('set -uo pipefail\n','set -uo pipefail\n'+
            'echo "RT_RUNNER_LAYER_ONLY: rev5 consumer, publisher and RT grammar prerequisite not integrated" >&2\nexit 2\n'),
           ('  echo "start=$(date -Iseconds)"\n','  echo "job_dir=$JD"\n  echo "start=$(date -Iseconds)"\n'),
           ('RRC=0\nreader() {',bridge.decode('utf8')+'\nRRC=0\nreader() {'),
           ('    NEED_UK=0; if [ "$BED" != ps_10_0_r45 ]',
            '    rt_pair_after_un\n    NEED_UK=0; if [ "$BED" != ps_10_0_r45 ]'),
           ('reader restore "$WORK_ROOT" "$BED" --job "$JOB"',
            'reader restore "$WORK_ROOT" "$BED" --job "$JOB" --publish-new')]
    for old,new in edits:
        if text.count(old)!=1:raise ValueError('nonunique RT runner insertion anchor')
        text=text.replace(old,new,1)
    return text.encode('utf8')

def build(source,output):
    source=Path(source);output=Path(output)
    # The established layer builder rejects overlapping/link/existing targets.
    spec=importlib.util.spec_from_file_location('rt_deck_layer',HERE.parent/'p1_rt_deck_preparation_20261116/prepare_rt_decks.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    runner=render_runner((source/'run_unload.sh').read_bytes(),(HERE/'rt_bridge.sh').read_bytes())
    old=m.build(source,output)
    additions={'run_unload_rt_dev.sh':runner,'rt_binding.py':(HERE/'rt_binding.py').read_bytes()}
    for name,data in additions.items():
        with (output/name).open('xb') as f:f.write(data)
    report={'schema':'rt_runner_layer_v1','operational_kit_ready':False,'engine_runs':0,
            'historical_source_files_preserved':old['source_files'],'rt_deck_additions':old['added_files'],
            'new_files':{k:hashlib.sha256(v).hexdigest() for k,v in additions.items()},
            'original_runner_sha256':ORIGINAL_SHA,'historical_seals_modified':False,
            'remaining':['30-column numeric comparison and continuity guards','20-check RT fixture reader and prerequisite',
                         'atomic publish-new and read-only restore integration','new operational seal and author field fixture']}
    with (output/'RT_RUNNER_LAYER.json').open('x',encoding='utf8',newline='\n') as f:json.dump(report,f,indent=2);f.write('\n')
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();print(json.dumps(build(a.source,a.output),indent=2))

if __name__=='__main__':main()
