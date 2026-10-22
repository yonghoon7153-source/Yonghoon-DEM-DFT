import os, sys, json
base = sys.argv[1]
sys.path.insert(0, os.path.join(base, 'scripts'))
import rint_r_chain as R
r1 = R.code_record(os.path.join(base, 'scripts', 'sdcp_gain_vox015_8arm.sh'))
print('chain git', r1['chain'], 'runner git', r1['runner'])
print('dirty problem', R.code_dirty_problem(r1))
p = os.path.join(base, 'scripts', 'ca_ext_cjunc.py')
src = open(p, encoding='utf-8').read()
open(p, 'w', encoding='utf-8').write(src + '\n# changed between stages (e.g. L_par default)\n')
r2 = R.code_record(os.path.join(base, 'scripts', 'sdcp_gain_vox015_8arm.sh'))
print('code_key equal after ca_ext_cjunc.py change:', R.code_key(r1) == R.code_key(r2))
print('code_verdict_problem:', R.code_verdict_problem(r1, 'stage'))
print('listed?', 'ca_ext_cjunc.py' in R.CODE_FILES, ' n listed', len(R.CODE_FILES))
