"""PC12 시험 블록을 scripts/test_rint_r_chain.py 의 '실행' 절 앞에 한 번 (원자적) 끼운다."""
import os
import pathlib
import sys

W = pathlib.Path(__file__).resolve().parent
p = pathlib.Path(sys.argv[1])
src = p.read_text(encoding='utf-8')
block = (W / 'pc12_tests_block.py').read_text(encoding='utf-8')
marker = '# ═════════════════════════ 실행 ═════════════════════════\n'
assert src.count(marker) == 1, src.count(marker)
assert 'PC12A' not in src, 'already applied'
new = src.replace(marker, block + marker)
compile(new, str(p), 'exec')
tmp = p.with_name(p.name + '.tmp')
tmp.write_text(new, encoding='utf-8')
os.replace(tmp, p)
print('appended', len(block.splitlines()), 'lines; total', len(new.splitlines()))
