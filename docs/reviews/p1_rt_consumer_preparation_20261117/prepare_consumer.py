"""Prepare a new inactive copy and a self-contained RT fixture reader."""
import argparse,ast,hashlib,importlib.util,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(data):return hashlib.sha256(data).hexdigest()
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def closed_history(raw):
    source=raw.decode('utf8');tree=ast.parse(source);names=('_num','read_dump','_close','local_map')
    found={n.name:ast.get_source_segment(source,n) for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names}
    if set(found)!=set(names):raise ValueError('history source closure')
    return ('import os,math\n\n'+'\n\n'.join(found[n] for n in names)+'\n').encode('utf8')

def standalone(source):
    source=Path(source)
    raw={'numeric':(HERE.parent/'p1_rt_numeric_preparation_20261117/rt_numeric.py').read_bytes(),
         'binding':(HERE.parent/'p1_rt_runner_preparation_20261117/rt_binding.py').read_bytes(),
         'contract':(HERE/'rt_contract.py').read_bytes(),
         'history':closed_history((source/'history_test/read_history.py').read_bytes())}
    h=json.loads((source/'history_test/history_params.json').read_bytes())
    contract={'schema':'rt_fixture_contract_candidate_v1','ul_bed':'hist_rt',
              'ul_s0':sum(h['steps'][k] for k in ('load','shear','hold')),'ul_atoms0':len(h['particles']),
              'tolerances':h['tolerances'],'expected_reset_fixes':h['expected_reset_fixes'],
              'pair_cols':h['observers']['pair_local']}
    C=load('local_rt_contract',HERE/'rt_contract.py')
    if json.loads(json.dumps(C.RESETS))!=contract['expected_reset_fixes']:raise ValueError('reset table drift')
    lines=['# Generated closed source candidate; no operational seal.',
           'import types,json','from pathlib import Path',
           'def _embed(name,raw,extra=None):',
           '    m=types.ModuleType(name);m.__dict__.update(extra or {})',
           '    exec(compile(bytes.fromhex(raw),"<embedded:"+name+">","exec"),m.__dict__);return m',
           'SOURCE_SHA256='+repr({k:sha(v) for k,v in raw.items()}),
           'CONTRACT='+repr(contract),
           'N=_embed("rt_numeric",'+repr(raw['numeric'].hex())+')',
           'B=_embed("rt_binding",'+repr(raw['binding'].hex())+')',
           'C=_embed("rt_contract",'+repr(raw['contract'].hex())+',{"N":N,"B":B})',
           'H=_embed("history_closure",'+repr(raw['history'].hex())+')']
    code=('\n'.join(lines)+'\n').encode()+(HERE/'rt_grammar_core.py').read_bytes()
    compile(code,'read_rt_grammar.py','exec')
    return code,(json.dumps(contract,indent=2)+'\n').encode('utf8')

def build(source,output):
    source=Path(source);output=Path(output)
    reader,contract=standalone(source)
    previous=load('rt_numeric_prepare',HERE.parent/'p1_rt_numeric_preparation_20261117/prepare_numeric.py')
    previous.build(source,output)
    additions={name:(HERE/name).read_bytes() for name in ('rt_contract.py','rt_publish.py','rt_restore.py','rt_fixture_prereq.py')}
    additions.update({'history_test/read_rt_grammar.py':reader,'history_test/rt_fixture_contract.json':contract})
    for name,data in additions.items():
        with (output/name).open('xb') as f:f.write(data)
    names=('in.hist_producer.liggghts','in.hist_rt1.liggghts','in.hist_rt2.liggghts','plate_hist.stl','read_rt_grammar.py','rt_fixture_contract.json')
    identities={name:sha((output/'history_test'/name).read_bytes()) for name in names}
    with (output/'history_test/RT_CANDIDATE_SHA256SUMS').open('x',encoding='ascii',newline='\n') as f:
        f.write(''.join(identities[n]+'  '+n+'\n' for n in sorted(names)))
    with (output/'RT_FIXTURE_CANDIDATE_IDENTITIES.json').open('x',encoding='utf8',newline='\n') as f:json.dump(identities,f,indent=2);f.write('\n')
    result={'schema':'rt_consumer_layer_v1','operational_kit_ready':False,'engine_runs':0,
            'added_sha256':{k:sha(v) for k,v in additions.items()},
            'runner_entry_closed':True,'historical_files_preserved':94}
    with (output/'RT_CONSUMER_LAYER.json').open('x',encoding='utf8',newline='\n') as f:json.dump(result,f,indent=2);f.write('\n')
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();print(json.dumps(build(a.source,a.output),indent=2))
if __name__=='__main__':main()
