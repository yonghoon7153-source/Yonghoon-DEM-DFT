"""Counterexamples to same-code / same-bed binding. No simulation or source mutation.
Run: python review/probes/provenance_probe.py
"""
from runtime import ROOT
import copy, hashlib, json, subprocess
from unittest.mock import patch
import rint_r_chain as r

def baseline_reports():
    files=r.code_files(r.HERE)
    common={'schema':r.S0_REPORT_SCHEMA,'code':{'git_head':'a'*40,'git_dirty':False,'file_digests':files},
            'inputs':{'files':{'fibre':{'sha256':'a'*64}},'counts':{'vgcf_points':120}},
            'raster':{'convention':{'vox_um':.15},'grid_shape':[10,10,10]}}
    a=copy.deepcopy(common); a.update(stage=1,kit={'name':r.SBE_KIT},plan={'sha256':'1'*64,'source':'stage1_computed'})
    b=copy.deepcopy(common); b.update(stage=2,kit={'name':r.DBE_KIT},plan={'sha256':'1'*64,'source':'commit:'+'a'*40,
        'r_plan':{'sha256':'2'*64,'path':'docs/data/plan.json'}})
    return a,b,files

out={}
# F1: actual archive outside Git; unknown identity accepted. Hashes remain exact.
rec=r.code_record(str(r.HERE/'sdcp_gain_vox015_8arm.sh'))
out['F1_actual_nongit']={'chain':rec['chain'],'runner':rec['runner'],
    'dirty_problem':r.code_dirty_problem(rec),'verdict_problem':r.code_verdict_problem(rec,'review fixture'),
    'omitted_imports':[x for x in ('ca_ext_cjunc.py','additives.py','se_material.py','lens_geometry.py','step4_dyn.py','rint_cycle_traj.py') if x not in r.CODE_FILES]}
# git status failure with a successful rev-parse is falsely read as clean.
def failed_status(cmd,**kw):
    return subprocess.CompletedProcess(cmd,128,'','fatal: cannot read index') if 'status' in cmd else subprocess.CompletedProcess(cmd,0,'a'*40+'\n','')
with patch.object(r.subprocess,'run',failed_status): ident=r.git_identity(r.HERE)
out['F1_status_failure']={'identity':ident,'dirty_problem':r.code_dirty_problem({'chain':ident,'runner':ident})}

a,b,files=baseline_reports()
reports={'stage1':r.s0_report_record(a,'a'*64,'S0_A.json'),'stage2':r.s0_report_record(b,'b'*64,'S0_B.json')}
# F2: chain and runner are individually clean but different pinned revisions, three files differ.
mixed=copy.deepcopy(rec)
mixed['chain']={'head':'a'*40,'dirty':False}; mixed['runner']={'head':'b'*40,'dirty':False}
mixed['runner_files']=copy.deepcopy(files)
changed=('step3_conv_cert.py','ca_ext_svcf.py','run_contract.py')
for row in mixed['runner_files']:
    if row['file'] in changed: row['sha256']='f'*64
with patch.object(r,'git_identity',lambda path: {'head':'a'*40,'dirty':False}):
    out['F2_clean_mixed_code']={'changed':changed,'dirty_problem':r.code_dirty_problem(mixed),
        's0_problem':r.s0_reports_problem(reports,'2'*64,'1'*64,files,mixed['runner_files']),
        'verdict_problem':r.code_verdict_problem(mixed,'mixed clean fixture'),
        'same_code_self':r.same_code(mixed,mixed)}
# F8: input geometry changes after census, while report gate has no corresponding comparison.
bb=copy.deepcopy(b); bb['inputs']['files']['fibre']['sha256']='f'*64
bb['inputs']['counts']['vgcf_points']=999; bb['raster']['grid_shape']=[11,10,10]
p=r.s0_report_record(b,'b'*64,'S0_B.json'); q=r.s0_report_record(bb,'c'*64,'S0_B2.json')
out['F8_input_loss']={'different_raw_input':b['inputs']!=bb['inputs'],
    'projection_keys':sorted(p),'old_report_accepted':r.s0_reports_problem(reports,'2'*64,'1'*64,files,files),
    'new_report_accepted':r.s0_reports_problem(dict(reports,stage2=q),'2'*64,'1'*64,files,files),
    'differences_projected':[k for k in p if p[k]!=q[k]],
    's0_stage2_has_input_argument':False}
# F5: source label grammar not checked. No shell is invoked.
p_bad=copy.deepcopy(p); p_bad['plan_source']='commit:'
out['F5_empty_commit']={'problem':r.s0_stage2_problem(p_bad,'2'*64,'1'*64)}
dst=ROOT/'evidence/provenance_probe.json'; dst.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(out,ensure_ascii=False,indent=2))
