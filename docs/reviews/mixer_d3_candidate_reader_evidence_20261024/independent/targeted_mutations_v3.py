#!/usr/bin/env python3
from pathlib import Path
import sys,subprocess,json,hashlib
root=Path(__file__).resolve().parent; source=root/'reviewed-v3/mixer_d3_candidates.py'; code=source.read_text(); out=root/'targeted-mutations-v3'; out.mkdir(exist_ok=False)
cases=[('decimal_exception_removed',', ValueError, InvalidOperation) as exc:',', ValueError) as exc:','28' if False else '1 != 2','cli'),('declared_reason_guard_removed','    if "reason" in point:\n        result["declared_reason"] = _string(point["reason"], where + ".reason")\n','','eligible_reason_type_checked','probe'),('Bo_po_divisor_changed','bo / Decimal("6.75")','bo / Decimal("6.76")','Bo_po_50_digit_ratio','probe')]
results=[]
for name,old,new,expected,mode in cases:
 assert code.count(old)==1,(name,code.count(old)); d=out/name; d.mkdir(); mutant=d/'mixer_d3_candidates.py'; mutant.write_text(code.replace(old,new))
 if mode=='cli':
  tests=d/'test_mixer_d3_candidates.py'; tests.write_bytes((root/'reviewed-v3/test_mixer_d3_candidates.py').read_bytes()); cmd=[sys.executable,'-I','-B',str(tests),'CliTests.test_extreme_decimal_exponent_cli_contract_error']
 else: cmd=[sys.executable,'-I','-B',str(root/'probe_independent_v2.py'),'--module',str(mutant),'--out',str(d/'result')]
 cp=subprocess.run(cmd,capture_output=True,text=True); (d/'stdout.log').write_text(cp.stdout); (d/'stderr.log').write_text(cp.stderr)
 found=cp.returncode!=0 and 'AssertionError' in cp.stderr and expected in cp.stderr
 results.append({'name':name,'rc':cp.returncode,'expected_assertion_detected':found,'expected':expected,'source_sha256':hashlib.sha256(mutant.read_bytes()).hexdigest()}); assert found,(name,cp.stderr)
(out/'summary.json').write_text(json.dumps(results,indent=2)+'\n'); print(json.dumps({'mutations':len(results),'expected_assertions':sum(x['expected_assertion_detected'] for x in results)}))
