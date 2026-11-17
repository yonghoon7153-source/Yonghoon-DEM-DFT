"""Add an offline numeric module to a NEW copy; leave runner entry closed."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def build(source,output):
    source,output=Path(source),Path(output)
    numeric=(HERE/'rt_numeric.py').read_bytes()
    spec=importlib.util.spec_from_file_location('rt_runner_layer',HERE.parent/'p1_rt_runner_preparation_20261117/prepare_rt_runner.py')
    previous=importlib.util.module_from_spec(spec);spec.loader.exec_module(previous)
    report=previous.build(source,output)
    with (output/'rt_numeric.py').open('xb') as f:f.write(numeric)
    summary={'schema':'rt_numeric_layer_v1','operational_kit_ready':False,'consumer_integrated':False,
             'engine_runs':0,'historical_source_files_preserved':report['historical_source_files_preserved'],
             'numeric_sha256':hashlib.sha256(numeric).hexdigest(),
             'runner_entry':'RT_RUNNER_LAYER_ONLY; immediate rc2 retained',
             'remaining':['technical/reset/post inventory integration','exclusive publish and read-only reread',
                          '20-check RT grammar fixture and prerequisite','pre-seal review and author field qualification']}
    with (output/'RT_NUMERIC_LAYER.json').open('x',encoding='utf8',newline='\n') as f:
        json.dump(summary,f,indent=2);f.write('\n')
    return summary


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(build(args.source,args.output),indent=2))


if __name__=='__main__':main()
