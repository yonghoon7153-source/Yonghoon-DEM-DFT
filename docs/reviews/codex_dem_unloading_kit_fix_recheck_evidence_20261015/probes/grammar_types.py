"""Type regression probe using the actual checker; no real binary invocation."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parents[1]
HIST = BASE / 'source/docs/data/ps45_unload_20261009/history_test'
sys.path.insert(0, str(HIST))
spec = importlib.util.spec_from_file_location('grammar_target_generator', HIST / 'make_history_decks.py')
mg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mg)
good = (HIST / 'in.hist_grammar.liggghts').read_text(encoding='utf-8')
three = 'fix gr_av all ave/time 10 10 ${gr_W} v_Ps c_gr_ke c_gr_erot'
one = 'fix gr_av all ave/time 10 10 ${gr_W} v_Ps'
assert good.count(three) == 1
assert good.count('variable gr_P equal f_gr_av[1]') == 1
cases = {
    'current_three_value_vector': (good, False),
    'original_single_value_vector_error': (good.replace(three, one), True),
    'single_value_scalar_valid': (good.replace(three, one).replace('variable gr_P equal f_gr_av[1]', 'variable gr_P equal f_gr_av'), False),
    'three_value_scalar_error': (good.replace('variable gr_P equal f_gr_av[1]', 'variable gr_P equal f_gr_av'), True),
    'three_value_index_four_error': (good.replace('variable gr_P equal f_gr_av[1]', 'variable gr_P equal f_gr_av[4]'), True),
    'three_value_index_999_error': (good.replace('variable gr_P equal f_gr_av[1]', 'variable gr_P equal f_gr_av[999]'), True),
}
out = {'synthetic_only': True, 'ran_real_binary': False, 'cases': {}}
for name, (deck, expected_problem) in cases.items():
    probs = mg.fix_output_problems(deck)
    out['cases'][name] = {'problems': probs, 'expected_problem': expected_problem,
                          'expectation_satisfied': bool(probs) == expected_problem}
out['grammar_input_hashes_match'] = {}
import hashlib
sys.path.insert(0, str(HIST.parent))
import ul_reader
for filename, sha in ul_reader.GRAMMAR_INPUTS.items():
    out['grammar_input_hashes_match'][filename] = hashlib.sha256((HIST / filename).read_bytes()).hexdigest() == sha
try:
    sh = subprocess.run(['C:/Program Files/Git/bin/bash.exe', '--noprofile', '--norc', '-c', 'exit 0'], capture_output=True, text=True, timeout=15)
    out['git_bash_smoke'] = {'rc': sh.returncode, 'stdout': sh.stdout, 'stderr': sh.stderr}
except Exception as exc:
    out['git_bash_smoke'] = {'exception': repr(exc)}
out['all_expectations_satisfied'] = (all(c['expectation_satisfied'] for c in out['cases'].values())
                                      and all(out['grammar_input_hashes_match'].values()))
(BASE / 'evidence/grammar_types.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(out, ensure_ascii=False, indent=2))
sys.exit(0 if out['all_expectations_satisfied'] else 1)
