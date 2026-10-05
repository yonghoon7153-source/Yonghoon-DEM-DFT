"""Actual network producer -> real publication helper -> tau handover."""
import contextlib,copy,io,json
from pathlib import Path
from probe_contracts import pipeline_case
import network_conductivity as nc
import dem_analysis_core as dac

B={i:{'type':1,'x':3.0*i,'y':0.,'z':z,'radius':1.} for i,z in ((1,0.),(2,1.),(3,2.))}
B.update({10+k:{'type':1,'x':0.,'y':5.,'z':float(z),'radius':1.} for k,z in enumerate(range(10,21))})
C=[{'id1':10+k,'id2':11+k,'contact_area':0.1,'delta':0.05} for k in range(10)]
with contextlib.redirect_stdout(io.StringIO()):
 dual={cm:nc._run_all_networks(B,C,[1],[],{1:'SE'},1.,20.,10.,10.,None,contact_mode=cm) for cm in ('hertzian','physics')}
 cp=dac.calc_percolation(B,C,[1],20.,box_x=10.,box_y=10.)
def replace_with_producer(artifacts):
 artifacts['network_conductivity.json']=copy.deepcopy(dual['hertzian'])
 artifacts['network_conductivity_hertzian.json']=copy.deepcopy(dual['hertzian'])
 artifacts['network_conductivity_physics.json']=copy.deepcopy(dual['physics'])
 artifacts['network_conductivity_dual.json']=copy.deepcopy(dual)
out=pipeline_case('actual_nonpercolating_producer',replace_with_producer,seed={'percolation_pct':cp['percolation_pct']})
out['producer']=dual
(Path(__file__).parent/'actual_zero_results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'producer_sigma_status':{k:v['sigma_full_status'] for k,v in dual.items()},'calc_percolation_pct':cp['percolation_pct'],
 'pipeline_summary':out['summary'],'tau_status':{m:out['tau']['ion_net_status_'+m] for m in ('hertz','physics')},
 'f_hertz':out['tau']['f_ion_hertz'],'active_provenance':out['active_provenance']},ensure_ascii=False,indent=2))
assert out['summary'][0]=='failed'
assert out['tau']['ion_net_status_hertz']=='NOT_PERCOLATING'
