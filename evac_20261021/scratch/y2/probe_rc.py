import sys
sys.path.insert(0, '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1a2386b8dc655b22/scripts')
import run_contract as RC  # noqa: E402

env = {'CJUNC': '1', 'CJUNC_RJ': '1e6', 'CJUNC_LEN_LAW': 'len_scaled_v0', 'CJUNC_UNREG_LAW': 'cut', 'CJUNC_S_MIN_UM': '0.5',
       'CJUNC_TOL_FF_UM': '0.5', 'CJUNC_PTFE_JLAW': 'P0', 'SDCP_MOD_C': '1', 'STEP3_RTOL': '1e-12'}
r = RC.runner_ca_ext(env, lean='2')
print(r)
v = RC.runner_ca_ext_view(dict(r['receipt'], ptfe_stamp='off'))
print(v)
print(RC.runner_ca_ext({'CJUNC': '1'}, lean='0'))
print(RC.runner_ca_ext({'STEP3_RTOL': '1e-10'}))
print(RC.runner_ca_ext_view({}))
print(RC.runner_ca_ext_view({'ptfe_stamp': 'face_alpha', 'step3_rtol': 1e-12}))
for bad in ('nan', 'inf', '1e999', '-1', '0', '1e6 ', '١٠', '1_000', '$HOME'):
    print(repr(bad), RC.runner_ca_ext(dict(env, CJUNC_RJ=bad), lean='2')['problems'])
