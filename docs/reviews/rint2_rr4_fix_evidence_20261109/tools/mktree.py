"""시험 뿌리 만들기 (고치기 전 대조 · 탐침 · 변이용) — <dest>/scripts = 작업 트리 scripts 의 링크 + 바꾼 rint_r_chain.py · test_rint_r_chain.py 사본 · docs 링크 ·
.gitignore 사본 (사전 공격 13 · 14 고침 docs/reviews/rint2_rr2_fix_evidence_20261105/pa13_fix/tools/mktree.py 와 같은 꼴).
쓰임: python3 mktree.py <작업트리> <dest> <rint_r_chain.py 원천> <test_rint_r_chain.py 원천>"""
import os
import shutil
import sys
from pathlib import Path


def make_tree(wt, dest, chain_src, test_src):
    wt, dest = Path(wt), Path(dest)
    if dest.exists():
        shutil.rmtree(dest)
    sd = dest / 'scripts'
    sd.mkdir(parents=True)
    for p in (wt / 'scripts').iterdir():
        if p.name in ('rint_r_chain.py', 'test_rint_r_chain.py', '__pycache__'):
            continue
        os.symlink(p, sd / p.name)
    shutil.copy2(chain_src, sd / 'rint_r_chain.py')
    shutil.copy2(test_src, sd / 'test_rint_r_chain.py')
    os.symlink(wt / 'docs', dest / 'docs')
    shutil.copy2(wt / '.gitignore', dest / '.gitignore')
    return dest


if __name__ == '__main__':
    print(make_tree(*sys.argv[1:5]))
