"""Codex 아님: independent document-only mutation exercise, no production imports."""
from pathlib import Path
import hashlib
import importlib.util
import io
import json
import unittest

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--root", type=Path, required=True)
parser.add_argument("--report", type=Path, required=True)
args = parser.parse_args()
ROOT = args.root.resolve()
if args.report.exists():
    raise FileExistsError("new report file required")
spec = importlib.util.spec_from_file_location('review_design', ROOT / 'docs/reviews/p1ab_rev5_20261116/check_design.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.ROOT = ROOT
original = {name: (ROOT / getattr(mod, name)).read_text(encoding='utf-8') for name in ('A', 'B', 'Q')}

cases = [
    ('M01_concurrent_publication', 'A', '동시 두 발행은 최대 한 개만 성공해야 한다.', '동시 두 발행은 두 개 모두 성공해도 된다.'),
    ('M02_id_acceptance', 'A', '`9007199254740993` · `2.0000000000000001`은 두 열 각각 거부', '`9007199254740993` · `2.0000000000000001`은 두 열 각각 허용'),
    ('M03_binding_priority', 'A', 'SYNTAX_FAIL이 우선.', 'UNCONFIRMED가 우선.'),
    ('M04_offscope_n_allowed', 'B', 'N 39900 등 그 밖은 attempt 줄 앞 rc 3 (reason=n_scope).', 'N 39900 등 그 밖은 attempt 줄 앞 허용 (rc 3 아님; reason=n_scope 기록만).'),
    ('M05_ledger_override_allowed', 'B', '우회 값은 reason=ledger_override,', '우회 값은 허용 (reason=ledger_override 기록만),'),
    ('M06_requeue_merge', 'B', '정직한 복구라도 어긋남 → 그 NP 결론 없음;', '정직한 복구면 기존 시도로 합침;'),
    ('M07_global_threshold', 'A', '전역 W ≤ **0.05** ∧', '전역 W ≤ **0.50** ∧'),
    ('M08_cell_threshold', 'A', '쓴 격자 칸별 안쪽 W 최대 ≤ 0.5**', '쓴 격자 칸별 안쪽 W 최대 ≤ 0.9**'),
    ('M09_pair_floor', 'A', '칸마다 안쪽 하중 쌍 ≥ **100**', '칸마다 안쪽 하중 쌍 ≥ **10**'),
    ('C01_pair_fixture_rollback', 'A', '쌍 덤프만 키움;', '쌍과 원자 덤프를 함께 키움;'),
    ('C02_atom_schema_rollback', 'A', 'omegaz radius f_history_zwall_bot[1] f_history_zwall_bot[2] f_history_zwall_bot[3] f_history_zwall_bot[4]', 'omegaz radius'),
    ('C03_consumer_rollback', 'A', '10–56 행 글자', '10–54 행 글자'),
    ('C04_float_order_rollback', 'A', 'float 변환 전 원 토큰을 검사', 'float 변환 후 원 토큰을 검사'),
]

cases.extend([
    ('A01_requeue_evidence_weakened', 'B', '미확정이면 B 현장 GO 보류; 실행 뒤 증거 누락이면 그 NP 결론 없음.', '미확정이어도 B 현장 GO 허용; 실행 뒤 증거 누락이어도 그 NP 결론 허용.'),
    ('A02_c12_revision_rollback', 'Q', 'C12 중력 팔 (별도 후속 개정)', 'C12 중력 팔 (개정 5)'),
])

results = []
for name, target, before, after in [('baseline', None, '', '')] + cases:
    documents = dict(original)
    if target:
        count = documents[target].count(before)
        assert count == 1, (name, count)
        documents[target] = documents[target].replace(before, after)
    def load_documents(cls):
        cls.a, cls.b, cls.q = (documents[k] for k in ('A', 'B', 'Q'))
    mod.DesignRegression.setUpClass = classmethod(load_documents)
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(mod.DesignRegression))
    item = {'name': name, 'group': 'baseline' if name == 'baseline' else 'additional' if name.startswith('A0') else 'original_13', 'document': target, 'before': before, 'after': after, 'methods': result.testsRun, 'passed': result.wasSuccessful(), 'failures': [str(t) for t, _ in result.failures], 'errors': [str(t) for t, _ in result.errors]}
    results.append(item)
    print(name, 'SURVIVED' if target and result.wasSuccessful() else 'PASS' if result.wasSuccessful() else 'DETECTED', result.testsRun)
report = {'label': 'Codex 아님', 'scope': 'independent document-only mutation; unchanged complete test class; three docs supplied in memory; history hash test still reads original history markdown', 'documents': {getattr(mod,k): hashlib.sha256((ROOT / getattr(mod,k)).read_bytes()).hexdigest() for k in original}, 'results': results, 'research_runs': 0, 'unique_test_methods': 12, 'original_mutation_cases': 13, 'additional_mutation_cases': 2}
with args.report.open("x", encoding="utf-8", newline="\n") as stream:
    json.dump(report, stream, ensure_ascii=False, indent=2)
    stream.write("\n")
assert results[0]["passed"] and all(not x["passed"] and not x["errors"] for x in results[1:])
