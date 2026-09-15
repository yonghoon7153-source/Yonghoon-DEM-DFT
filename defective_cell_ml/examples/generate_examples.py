"""Recreate artificial example inputs. These are not measured battery data."""
from pathlib import Path
import sys
import numpy as np
import pandas as pd

PACKAGE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PACKAGE))
from config import Config,config_dict,write_json
from demo import make_demo
from extract_capacity import CYCLE_COLUMNS


def main():
    folder=Path(__file__).resolve().parent
    cfg=Config().validate()
    write_json(PACKAGE/'config.json',config_dict(cfg))
    write_json(folder/'config_eis_only.json',config_dict(Config(use_ocv=False)))
    write_json(folder/'config_group.json',config_dict(Config(outer_cv='leave_one_group_out')))
    data=make_demo(cfg)
    data.to_csv(folder/'demo_features.csv',index=False,encoding='utf-8-sig')
    new=data.drop(columns=['cap','cc_frac']).copy()
    # Different IDs demonstrate inference for unseen identifiers; values are artificial copies.
    new['cell_number']+=20
    new.to_csv(folder/'new_features.csv',index=False,encoding='utf-8-sig')
    cycle=folder/'raw'/'cycle'; eis=folder/'raw'/'eis'; new_eis=folder/'raw'/'new_eis'
    for path in [cycle,eis,new_eis]:
        path.mkdir(parents=True,exist_ok=True)
    manifest=[]
    for record in data.to_dict('records'):
        cell=int(record['cell_number']); cap=record['cap']; cc=cap*record['cc_frac']
        rows=[[0,0,1,10,0,3.7,0],[1,0,1,20,.01*cap,3.8,.01],
              [2,1,1,20,.5*cc,4.,.01],[3,2,1,20,cc,4.2,.005],
              [4,3,1,20,cap,4.2,.001],[5,0,1,30,cap,4.1,-.01]]
        text='SYNTHETIC SOFTWARE TEST INPUT; NOT MEASURED BATTERY DATA\n'
        text+='\t'.join(CYCLE_COLUMNS)+'\ns\ts\tindex\tindex\tAh\tV\tA\n'
        text+=''.join('\t'.join(str(v) for v in row)+'\n' for row in rows)
        cycle_name=f'cell{cell}_synthetic_cycle.txt'
        eis_name=f'cell{cell}_synthetic_eis.mpt'
        (cycle/cycle_name).write_text(text,encoding='utf-8')
        lines=['EC-Lab ASCII FILE','SYNTHETIC SOFTWARE TEST INPUT; NOT MEASURED BATTERY DATA',
               'freq/Hz\tRe(Z)/Ohm\t-Im(Z)/Ohm\t|Z|/Ohm\tPhase(Z)/deg\t<Ewe>/V']
        for f in cfg.frequency_grid_hz:
            real=record[f're@{f:g}Hz']; imag=record[f'im@{f:g}Hz']
            values=[f,real,-imag,np.hypot(real,imag),np.degrees(np.arctan2(imag,real)),record['ocv']]
            lines.append('\t'.join(f'{v:.17g}' for v in values))
        (eis/eis_name).write_text('\n'.join(lines)+'\n',encoding='utf-8')
        (new_eis/f'cell{cell+20}_synthetic_eis.mpt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
        manifest.append({'cell_number':cell,'cycle_file':cycle_name,'eis_file':eis_name,
                         'batch_id':record['batch_id'],'selection_reason':'one synthetic fixture per artificial cell'})
    pd.DataFrame(manifest).to_csv(folder/'selection_manifest.csv',index=False,encoding='utf-8-sig')
    print('Generated 12 training examples and 12 relabeled inference examples; all synthetic.')


if __name__=='__main__':
    main()
