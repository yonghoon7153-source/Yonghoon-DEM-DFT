"""Copy the Codex S02 probe outside the bundle and change only path constants.

usage: python3 -I make_probe_copy.py <bundle_root> <dest_root> <our_repo> <baseline_src>
Writes <dest_root>/probes/s02/adversary.py and <dest_root>/probe_path_changes.diff.
Every replacement must match exactly once; nothing else is touched.
"""
import difflib
import sys
from pathlib import Path


def main():
    bundle, dest, repo, base = map(Path, sys.argv[1:5])
    src_rel = 'probes/s02/adversary.py'
    text = (bundle / src_rel).read_text(encoding='utf-8')
    reps = [
        ('WORK = ROOT.parent\n',
         'WORK = ROOT.parent\n'
         f'SRC = Path({str(repo)!r})  # our tree (was ROOT / "source")\n'
         f'BASE_SRC = Path({str(base)!r})  # git show 685c2bbdb extraction (was WORK / "lhs214s_recheck_20261019/source")\n'),
        ('sys.path[:0] = [\n'
         '    str(ROOT / "source/scripts"), str(ROOT / "source/webapp"),\n'
         '    str(WORK / "lhs_coverage_review_20260930/deps"),\n'
         '    str(WORK / "gen2_network_reverify3_20261007/deps"),\n'
         ']\n',
         'sys.path[:0] = [\n'
         '    str(SRC / "scripts"), str(SRC / "webapp"),\n'
         ']\n'),
        ('        now = (ROOT / "source" / rel).read_bytes()\n',
         '        now = (SRC / rel).read_bytes()\n'),
        ('        old = (WORK / "lhs214s_recheck_20261019/source" / rel).read_bytes()\n',
         '        old = (BASE_SRC / rel).read_bytes()\n'),
    ]
    new = text
    for before, after in reps:
        n = new.count(before)
        assert n == 1, (before, n)
        new = new.replace(before, after)
    out = dest / src_rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(new, encoding='utf-8')
    diff = ''.join(difflib.unified_diff(text.splitlines(True), new.splitlines(True),
                                        fromfile='bundle/' + src_rel, tofile='copy/' + src_rel))
    (dest / 'probe_path_changes.diff').write_text(diff, encoding='utf-8')
    print(diff)


if __name__ == '__main__':
    main()
