"""고치기 전 탐침 다시 (probe_out/*_before.out) ↔ 사전 공격 13 원 출력 (preattack13/*.out) 바이트 대조 — 쓰임: python3 before_vs_preattack.py <probe_out> <preattack13>"""
import hashlib
import sys
from pathlib import Path

po, pa = Path(sys.argv[1]), Path(sys.argv[2])
PAIRS = [('p1_value_domain', 'p1_value_domain'), ('p1b_value_domain_cli', 'p1b_value_domain_cli'), ('p2_resume_mismatch', 'p2_resume_mismatch'),
         ('p2b_resume_mismatch_chain', 'p2b_resume_mismatch_chain'), ('p3_honest_shapes_main_pred', 'p3_honest_main_pred'),
         ('p3_honest_shapes_units_over', 'p3_honest_units_over'), ('p4_all_arm_forms', 'p4_all_arm_forms'),
         ('p5_value_domain_honest_units', 'p5_value_domain_honest'), ('p6_struct_edges', 'p6_struct_edges')]
same = 0
for ours, theirs in PAIRS:
    a, b = (po / f'{ours}_before.out').read_bytes(), (pa / f'{theirs}.out').read_bytes()
    ok = a == b
    same += ok
    print(f'{ours}_before.out ↔ preattack13/{theirs}.out  같음 {ok}  sha256 {hashlib.sha256(a).hexdigest()[:16]}')
print(f'바이트 같음 {same}/{len(PAIRS)}')
