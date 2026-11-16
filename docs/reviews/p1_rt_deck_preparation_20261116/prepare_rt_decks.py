"""A1 static RT deck layer. Never runs an engine or publishes a restore certificate.

Copies the historical kit byte for byte into a NEW directory, adding RT decks.
The old runner/readers/seals are preserved as historical input, not an updated
operational kit. A2 integration is required before any fixture/production run.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

BEDS = ('ps_0_10_r45','ps_3_7_r45','ps_5_5_r45','ps_7_3_r45','ps_10_0_r45')

def block(raw, name):
    found = re.findall(rb'^# >>> block '+name.encode()+rb'[^\n]*\n.*?^# <<< block '+name.encode()+rb'\r?\n',raw,re.M|re.S)
    if len(found)!=1:raise ValueError('unique source block required: '+name)
    return found[0]

def rt_block(kind):
    if kind not in ('RT1','RT2'):raise ValueError('RT kind')
    lines=['# >>> block rt',
           'thermo_style custom step atoms ke cpu',
           'variable ul_step equal step','variable ul_step equal ${ul_step}',
           'variable ul_na equal atoms','variable ul_na equal ${ul_na}',
           'if "${ul_step} != ${ul_s0}" then "print \'UL_ABORT reason=start_step step=${ul_step} expect=${ul_s0}\'" "quit"',
           'if "${ul_na} != ${ul_atoms0}" then "print \'UL_ABORT reason=start_atoms atoms=${ul_na} expect=${ul_atoms0}\'" "quit"',
           'uncompute cpl',
           'compute ul_ph all pair/gran/local pos id force force_normal force_tangential torque history contactArea delta contactPoint',
           'dump ul_rp all local ${ul_big} ${out}/post/rt_pair_*.dump '+' '.join('c_ul_ph[%d]'%i for i in range(1,31)),
           'dump_modify ul_rp first yes format "'+' '.join(['%.17g']*30)+'"',
           'dump ul_ra all custom ${ul_big} ${out}/post/rt_atom_*.dump id type x y z vx vy vz omegax omegay omegaz radius '+' '.join('f_history_zwall_bot[%d]'%i for i in range(1,5)),
           'dump_modify ul_ra first yes format "'+' '.join(['%d','%d']+['%.17g']*14)+'"',
           'compute ul_wh all wall/gran/local id history force_normal',
           'dump ul_rw all local ${ul_big} ${out}/obs/rt_wall_*.dump '+' '.join('c_ul_wh[%d]'%i for i in range(1,11)),
           'dump_modify ul_rw first yes format "'+' '.join(['%.17g']*10)+'"',
           'run 0','undump ul_rp','undump ul_ra','undump ul_rw']
    if kind=='RT1':lines.append('write_restart ${out}/rt.bin')
    lines += ['print "UL_RT_DONE bed=${ul_bed} step=${ul_step}"','# <<< block rt']
    return ('\n'.join(lines)+'\n').encode('utf-8')

def generated_additions(source):
    source=Path(source);out={}
    for bed in BEDS:
        raw=(source/'decks'/bed/'in.R.liggghts').read_bytes()
        for kind in ('RT1','RT2'):
            out['decks/'+bed+'/in.'+kind+'.liggghts']=(
                ('# DEVELOPMENT RT DECK LAYER: '+bed+' '+kind+'; not operationally sealed\n').encode()
                +block(raw,'head')+b'\n'+block(raw,'r_params')+b'\n'+rt_block(kind))
    h=json.loads((source/'history_test/history_params.json').read_bytes())
    params=dict(schema='ps45_rt_grammar_params_draft_v1',ul_bed='hist_rt',
                ul_s0=sum(h['steps'][k] for k in ('load','shear','hold')),
                ul_atoms0=len(h['particles']),ul_big=h['grammar_probe']['big'])
    if any(type(params[k]) is not int or params[k]<=0 for k in ('ul_s0','ul_atoms0','ul_big')):
        raise ValueError('history table integer parameters')
    raw=(source/'history_test/in.hist_consumer.liggghts').read_bytes()
    lines=raw.splitlines(keepends=True)
    start=[i for i,s in enumerate(lines) if s.strip()==b'atom_style granular']
    end=[i for i,s in enumerate(lines) if s.startswith(b'variable pressMPa equal ')]
    if len(start)!=1 or len(end)!=1 or start[0]>=end[0]:raise ValueError('consumer head boundaries')
    head=b'# >>> block head\n'+b''.join(lines[start[0]:end[0]+1])+b'# <<< block head\n'
    rparams=('\n'.join(['# >>> block r_params','variable ul_bed string hist_rt',
              'variable ul_s0 index '+str(params['ul_s0']),
              'variable ul_atoms0 equal '+str(params['ul_atoms0']),
              'variable ul_big equal '+str(params['ul_big']),'# <<< block r_params'])+'\n').encode()
    for kind in ('RT1','RT2'):
        out['history_test/in.hist_'+kind.lower()+'.liggghts']=(
            ('# DEVELOPMENT RT FIXTURE '+kind+'; no execution qualification\n').encode()+head+b'\n'+rparams+b'\n'+rt_block(kind))
    out['history_test/rt_grammar_params.json']=(json.dumps(params,indent=2)+'\n').encode()
    return out

def validate_generated(source, files):
    expected=generated_additions(source)
    if files!=expected:raise ValueError('RT deck/table differs from deterministic source')
    return True

def build(source, output):
    source=Path(source).resolve();output=Path(output)
    dest=output.resolve()
    if output.is_symlink() or dest==source or source in dest.parents or dest in source.parents:
        raise ValueError('source and destination must be separate')
    if output.exists():raise FileExistsError('new destination required')
    raw={}
    for p in sorted(source.rglob('*')):
        if p.is_symlink():raise ValueError('source link is not a frozen regular-file input')
        if p.is_file():raw[p.relative_to(source).as_posix()]=p.read_bytes()
    additions=generated_additions(source)
    if set(raw)&set(additions):raise ValueError('RT additions already exist in source')
    validate_generated(source,additions)
    output.mkdir(parents=True,exist_ok=False)
    for name,data in {**raw,**additions}.items():
        p=output/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
    manifest=dict(schema='rt_deck_layer_v1',status='STATIC_DECK_LAYER_ONLY',
        operational_kit_ready=False,engine_runs=0,source_files=len(raw),added_files=len(additions),
        preserved={k:hashlib.sha256(v).hexdigest() for k,v in raw.items()},
        added={k:hashlib.sha256(v).hexdigest() for k,v in additions.items()},
        remaining=['runner RT sequencing and bind receipts','30-column reader and continuity guards',
                   'publish-new certificate path','RT fixture 20 checks','pre-seal review and author field run'])
    (output/'RT_DECK_LAYER.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    return manifest

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();r=build(args.source,args.output)
    print(json.dumps({k:r[k] for k in ('status','source_files','added_files','engine_runs')}))

if __name__=='__main__':main()
