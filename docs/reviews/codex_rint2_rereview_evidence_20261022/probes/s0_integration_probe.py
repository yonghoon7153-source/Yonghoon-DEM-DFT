"""Tiny synthetic S0 producer→chain check, no transport or MPM solve.
Windows adaptations: Git Bash path spelling, fixture symlink replaced with legitimate run_* fallback,
Git autocrlf disabled in this subprocess only. Pinned numerical / census / validation code unchanged.
"""
from runtime import ROOT
import contextlib, copy, hashlib, io, json, os, subprocess, tempfile, traceback, sys
from unittest.mock import patch
import numpy as np
import ca_s0_census as s
import step3_sigma as sg
import rint_r_chain as r
import test_ca_s0_census as t

os.environ['GIT_CONFIG_COUNT']='1'; os.environ['GIT_CONFIG_KEY_0']='core.autocrlf'; os.environ['GIT_CONFIG_VALUE_0']='false'
out={}; logs=io.StringIO()
orig_resolver=s.resolve_payload_argv
orig_abs=os.path.abspath; orig_join=os.path.join; orig_run=subprocess.run
def resolve(*args,**kw):
    if '--fixture-argv' in sys.argv:
        kit,run_dir,out_dir=map(str,args)
        return ['--se','se_dump.npy','--scaffold',orig_join(kit,'am_scaffold.csv'),
                '--n-vox','48','--tri-step','4','--smooth','1.5','--void-max','1000',
                '--metrics-json','mpm_metrics.json','--case','fx','--phase','phase.npy','--fibre','fibre.npy',
                '--fibre-dia','fibre_dia.npy','--out',orig_join(out_dir,'_payload_never.json'),
                '--step3-vox',str(kw['vox']),'--step3-bridge-um',str(kw['bridge_um']),
                '--step3-origin-shift','0','0','0','--step3-sdcp-sphere-d',str(kw['sdcp_sphere_d']),
                '--ptfe-stamp','centerline','--step3-fibre-stamp','segment',
                '--no-ion','--no-field','--no-pore','--no-thermal','--no-trackb','--no-collector','--no-step4',
                '--step3-rasterize-only',orig_join(out_dir,'_payload_rasterize_only.json')]
    args=tuple(str(a).replace('\\','/') for a in args)
    if 'scripts_dir' in kw: kw['scripts_dir']=str(kw['scripts_dir']).replace('\\','/')
    def run(cmd,**k):
        if isinstance(cmd,list) and cmd and cmd[0]=='bash': cmd=['C:/Program Files/Git/bin/bash.exe']+cmd[1:]
        return orig_run(cmd,**k)
    with patch.object(os.path,'abspath',lambda x:orig_abs(x).replace('\\','/')), \
         patch.object(os.path,'join',lambda *x:orig_join(*x).replace('\\','/')), patch.object(subprocess,'run',run):
        return orig_resolver(*args,**kw)
def no_solve(*a,**k): raise AssertionError('Transport solve forbidden in this probe')

try:
  with tempfile.TemporaryDirectory(prefix='s0rev_') as td, contextlib.redirect_stdout(logs), contextlib.redirect_stderr(logs), \
       patch.object(s,'resolve_payload_argv',resolve), patch.object(sg,'solve_sigma_z',no_solve), \
       patch.object(sg,'_solve_cg',no_solve), patch.object(sg,'solve_thermal',no_solve):
    with patch.object(os,'symlink',lambda *a,**k:None):
        ka=t.write_kit(td,r.SBE_KIT,vgcf=[t.F1],ptfe=[t.P1],vol={'VGCF':.04,'PTFE':.1})
        kb=t.write_kit(td,r.DBE_KIT,vgcf=[t.F1,t.F2],ptfe=[t.P1],sdcp=t.S1,vol={'VGCF':.04,'PTFE':.1,'SDCP':t.V_SDCP1})
    a=s.run_stage(1,[ka],orig_join(td,'s1'),vox=t.VOX)
    rawA=open(a['reports'][0],'rb').read(); repA=json.loads(rawA)
    pb=open(a['plan'],'rb').read(); ph=hashlib.sha256(pb).hexdigest()
    # Call stage-2 census body with explicit fixture plan. Git commit-verification is NOT covered here
    # (sandbox cannot write an index). The census, actual payload raster capture and validators are unmodified.
    rp=t.r_plan_bytes(json.loads(pb)['values_um']['tol_ff']); rh=hashlib.sha256(rp).hexdigest(); robj=json.loads(rp)
    rinfo={'sha256':rh,'path':t.R_PLAN_REL,'s_min_um':robj['s_min_um'],'tol_ff_um':robj['tol_ff_um'],
           'len_law':robj['len_law'],'unreg_law':robj['unreg_law'],'step3_rtol':robj['step3_rtol']}
    def stage2_body(outdir):
        os.makedirs(outdir)
        rep,*_=s.census_kit(kb,outdir,stage=2,plan=json.loads(pb),plan_sha=ph,plan_source='commit:'+'a'*40,
                           vox=t.VOX,plan_extra={'r_plan':rinfo})
        return rep,json.dumps(rep,ensure_ascii=False).encode('utf8')
    repB,rawB=stage2_body(orig_join(td,'s2'))
    records={'stage1':r.s0_report_record(repA,hashlib.sha256(rawA).hexdigest(),a['reports'][0]),
             'stage2':r.s0_report_record(repB,hashlib.sha256(rawB).hexdigest(),'S0_stage2_fixture.json')}
    files=r.code_files(r.HERE)
    out['actual_stage1_stage2']={'stage1_points':repA['inputs']['counts'],'stage2_points':repB['inputs']['counts'],
       'plan_source':repB['plan']['source'],'gate':r.s0_reports_problem(records,rh,ph,files,files),'transport_solve_calls':0}
    # The same named DBE kit is regenerated after S0: a real non-collinear path changes.
    rd=s.find_run_dir(kb); pp=orig_join(rd,'se_dump.npy'); x=np.load(pp); phase=np.load(orig_join(rd,'phase.npy'))
    fid=np.load(orig_join(rd,'fibre.npy'))
    x[(phase==2)&(fid==1),2]+=.04; np.save(pp,x)
    repB2,rawB2=stage2_body(orig_join(td,'s2_newbed'))
    recB2=r.s0_report_record(repB2,hashlib.sha256(rawB2).hexdigest(),'S0_stage2_changed_fixture.json')
    out['actual_bed_change']={'changed_inputs':[k for k in repB['inputs']['files'] if repB['inputs']['files'][k]!=repB2['inputs']['files'][k]],
        'cells_before':repB['raster']['cells_by_sid']['off'],'cells_after':repB2['raster']['cells_by_sid']['off'],
        'junctions_before':repB['junction_census']['n_instances'],'junctions_after':repB2['junction_census']['n_instances'],
        'old_reports_gate_after_change':r.s0_reports_problem(records,rh,ph,files,files),
        'new_reports_gate':r.s0_reports_problem(dict(records,stage2=recB2),rh,ph,files,files),
        'input_binding_preserved': 'inputs' in records['stage2']}
    for name,obj in [('s0_actual_stage1.json',repA),('s0_actual_stage2.json',repB),('s0_actual_stage2_changed_bed.json',repB2)]:
        (ROOT/'evidence'/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf8')
except Exception as e:
    out['exception']={'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc()}
out['shell_argv_mode']='fixed_fixture_not_shell' if '--fixture-argv' in sys.argv else 'actual_shell'
out['stage2_scope']='actual census body with explicit fixture plan; Git pre-gate not tested'
tag='_fixed_argv' if '--fixture-argv' in sys.argv else ''
(ROOT/f'evidence/s0_integration_probe{tag}.log').write_text(logs.getvalue(),encoding='utf8')
(ROOT/f'evidence/s0_integration_probe{tag}.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(out,ensure_ascii=False,indent=2))
