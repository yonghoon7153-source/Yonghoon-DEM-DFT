"""Execute the baseline-pin (685c2bbdb) test source as if it sat in our tree.

usage: python3 -B run_baseline_exec.py <baseline_test_file> <our_tree_test_path>
The baseline source (from `git show 685c2bbdb:...`) is compiled from the scratch
file and executed with __name__ == '__main__' and __file__ = our tree's path, so
its HERE / ROOT resolve to our tree (modules + docs/data). Nothing is written to
the tree. Our tree's modules equal the 685c2bbdb blobs except the two LHS214
files and Rint-only files (git diff --name-only 685c2bbdb HEAD -- scripts webapp).
"""
import sys
from pathlib import Path


def main():
    src_file = Path(sys.argv[1])
    fake_file = sys.argv[2]
    code = compile(src_file.read_text(encoding='utf-8'), str(src_file), 'exec')
    sys.argv = [fake_file]
    g = {'__name__': '__main__', '__file__': fake_file, '__builtins__': __builtins__}
    try:
        exec(code, g)
    finally:
        mods = sorted(m for m in sys.modules if m in ('step3_sigma', 'rint_iface_join'))
        print(f'[runner] rint modules loaded: {mods}', file=sys.stderr)


if __name__ == '__main__':
    main()
