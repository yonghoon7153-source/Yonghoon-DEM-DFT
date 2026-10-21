"""Copy a directory tree excluding .git (shutil) — usage: python3 copytree.py SRC DST"""
import shutil
import sys

src, dst = sys.argv[1], sys.argv[2]
shutil.rmtree(dst, ignore_errors=True)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns('.git', '__pycache__'), symlinks=True)
print('copied', src, '->', dst)
