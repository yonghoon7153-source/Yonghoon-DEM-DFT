"""시험한 판 = 커밋할 바이트 — 바탕 40d9658c0 (git 객체) · 작업 트리 (고친 판) 의 sha256 → logs/code_sha256.txt.  python3 make_code_sha.py <작업 트리>"""
import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
out = ['# 바탕 = 40d9658c0 (git 객체 · rint_r_chain.py = 리뷰 핀 17d45fb9c 의 그 파일과 같음)']
for rel in ('scripts/rint_r_chain.py', 'scripts/test_rint_r_chain.py'):
    raw = subprocess.run(['git', 'show', f'40d9658c0:{rel}'], cwd=str(ROOT), capture_output=True, check=True).stdout
    out.append(f'{hashlib.sha256(raw).hexdigest()}  {rel}  (바탕)')
out.append('# 고친 판 = 이 커밋 (작업 트리 · 깨끗한 40d9658c0 + apply_chain.py · apply_tests.py 로 다시 만든 바이트와 같음 · 시험 · 변이 · 탐침 다시 = 이 바이트)')
for rel in ('scripts/rint_r_chain.py', 'scripts/test_rint_r_chain.py'):
    out.append(f'{hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()}  {rel}  (고친 판)')
(ROOT / 'docs/reviews/rint2_rr2_fix_evidence_20261105/rr3_fix/logs/code_sha256.txt').write_text('\n'.join(out) + '\n', encoding='utf-8')
print('\n'.join(out))
