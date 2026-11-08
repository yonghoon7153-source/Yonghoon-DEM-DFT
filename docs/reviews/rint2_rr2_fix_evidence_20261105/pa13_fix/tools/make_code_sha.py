"""code_sha256.txt (바탕 → 고친 판 · 두 코드 파일) — 쓰임: python3 make_code_sha.py <바탕 폴더> <고친 판 폴더> <출력 파일>"""
import hashlib
import sys
from pathlib import Path

base, fixed, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
names = ('rint_r_chain.py', 'test_rint_r_chain.py')
lines = ['# 바탕 = f44478535 (rint_r_chain.py · test_rint_r_chain.py = 사전 공격 13 대상 742a3b83f 와 같은 blob 9d1ed51d9 · e2f608a14)']
lines += [f'{hashlib.sha256((base / n).read_bytes()).hexdigest()}  scripts/{n}  (바탕)' for n in names]
lines.append('# 고친 판 = 바탕 + code.diff (apply 확인 = 아래 바이트) = 이 커밋 · 시험 · 변이 · 탐침 다시 = 이 바이트')
lines += [f'{hashlib.sha256((fixed / n).read_bytes()).hexdigest()}  scripts/{n}  (고친 판)' for n in names]
out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(out.read_text(encoding='utf-8'), end='')
