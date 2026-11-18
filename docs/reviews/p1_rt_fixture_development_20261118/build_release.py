"""Build the single fixed NP6 development fixture from the imported assembly."""
import argparse
import hashlib
import importlib.util
import json
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[2] / 'docs/data/ps45_unload_20261009'
LMP_SHA = 'ee2d77261bac9e7fa4e9311c8709e74bf7583a13225a5bc35a791bef9be60a3f'
ASSEMBLY = HERE.parent / 'p1_rt_fixture_runner_preparation_20261117'
INPUT_NAMES = {'read_rt_grammar.py', 'rt_fixture_contract.json', 'in.hist_rt1.liggghts',
               'in.hist_rt2.liggghts', 'in.hist_producer.liggghts', 'plate_hist.stl'}

def build(destination):
    destination = Path(destination)
    spec = importlib.util.spec_from_file_location('registered_assembly', ASSEMBLY / 'prepare_assembly.py')
    assembly = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(assembly)
    with tempfile.TemporaryDirectory() as temp:
        prepared = Path(temp) / 'assembly'
        assembly.build(SOURCE, prepared)
        history = prepared / 'history_test'
        registered = json.loads((prepared / 'RT_FIXTURE_CANDIDATE_IDENTITIES.json').read_bytes())
        if set(registered) != INPUT_NAMES:
            raise ValueError('unexpected fixture file set')
        files = {name:(history/name).read_bytes() for name in registered}
        if any(hashlib.sha256(raw).hexdigest() != registered[name] for name, raw in files.items()):
            raise ValueError('fixture identity mismatch')
        files['RT_CANDIDATE_SHA256SUMS'] = (history / 'RT_CANDIDATE_SHA256SUMS').read_bytes()
        runner = (history / 'run_history_rt_candidate.sh').read_text(encoding='utf8')
        start = runner.index('run_stage() {')
        stop = runner.index('\n}',start)+2
        stage = runner[start:stop]
        flow = (ASSEMBLY / 'rt_fixture_flow.sh').read_text(encoding='utf8')
        if flow.strip() not in runner:
            raise ValueError('fixture stage body differs from assembly')
        header = (HERE / 'fixture_header.sh').read_text().replace('@LMP_SHA@', LMP_SHA)
        destination.mkdir(parents=True, exist_ok=False)
        kit = destination / 'kit'
        kit.mkdir()
        for name, raw in files.items():
            (kit/name).write_bytes(raw)
        (destination/'fixture.sh').write_bytes(('\n'.join([header,stage,flow])+'\n').encode())
        (destination/'job.sh').write_bytes((HERE/'job.sh').read_bytes())

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('destination',type=Path)
    build(parser.parse_args().destination)
