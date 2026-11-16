import argparse, importlib.util, io, json, tempfile, unittest
from pathlib import Path
parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,required=True)
R=parser.parse_args().root.resolve()
P=R/'docs/reviews/p1ab_rev5_receipt_20261116'
s=importlib.util.spec_from_file_location('checks',R/'docs/reviews/p1ab_rev5_20261116/check_design.py'); m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
mutations=[
 ('historical_pass',m.A,'역사 6×4·11×1 정직 B/C = UNCONFIRMED','역사 6×4·11×1 정직 B/C = PASS'),
 ('N99_pass',m.A,'| N99_EQUAL | 칸마다 N=99, 모든 힘 동일, W=W_c=0 | UNCONFIRMED |','| N99_EQUAL | 칸마다 N=99, 모든 힘 동일, W=W_c=0 | PASS |'),
 ('N99_reset_violation',m.A,'| N99_RESET_ONE | 칸마다 N=99, 한 칸 W_c=1, W=1/24 | UNCONFIRMED |','| N99_RESET_ONE | 칸마다 N=99, 한 칸 W_c=1, W=1/24 | VALUE_MISMATCH |'),
 ('C12_revision5',m.A,'C12 중력 팔 (별도 후속 개정)','C12 중력 팔 (개정 5)'),
 ('revision4',m.A,'"⛔ 개정 5 §15"','"⛔ 개정 4 §15"'),
 ('whole_gate_claim',m.Q,'전체 gate 미실행','이 요청서 커밋에서 실패 0'),
]
observations=[]
with tempfile.TemporaryDirectory(prefix='p1ab_doc_mut_') as td:
    root=Path(td);m.ROOT=root
    for name,p,old,new in mutations:
        for rel in (m.A,m.B,m.Q):
            dest=root/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((R/rel).read_bytes())
        path=root/p; text=path.read_text(encoding='utf-8');assert text.count(old)==1,(name,text.count(old));path.write_text(text.replace(old,new),encoding='utf-8')
        suite=unittest.TestSuite(m.DesignRegression(n) for n in ('test_13_historical_and_synthetic_cell_expectations','test_14_active_revision_scope_and_checks'))
        result=unittest.TextTestRunner(stream=io.StringIO()).run(suite)
        observations.append({'name':name,'methods':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'detected':len(result.failures)>0 and not result.errors})
assert all(x['detected'] for x in observations)
print(json.dumps(observations,ensure_ascii=False,indent=2))
