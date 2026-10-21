import sys, os, json, tempfile
W = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-afe53be7bdb176c82'
sys.path.insert(0, os.path.join(W, 'scripts'))
import test_ca_ext_b6 as B6
import run_contract as RC
import ca_ext_cjunc as CW
import sr01_stamp_compare as SC
B6.RC = RC
B6.CW = CW
m = B6.cj_manifest()
print('fibre_stamp', m.get('fibre_stamp'), 'components', json.dumps(m.get('components'))[:300])
print('backend', m.get('backend'))
s3 = {'sigma_e_eff_S_cm': 0.05, 'n_dof': 100, 'cg_info': 0, 'unconverged': False, 'cg_resid': 1e-13, 'vox_um': m.get('vox_um'),
      'manifest': m, 'conv_cert': B6.good_cert(0.05)}
d = tempfile.mkdtemp()
p = os.path.join(d, 'a.json')
json.dump({'mpm_metrics': {'step3': s3}}, open(p, 'w'))
print('check_arm positive:', SC.check_arm(p, 'segment', expect_backend=None, receipt=None))
print('check_arm positive gpu:', SC.check_arm(p, 'segment', expect_backend='gpu', receipt=None))
