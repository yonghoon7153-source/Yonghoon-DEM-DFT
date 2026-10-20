"""Copy the Codex probes OUT of the bundle into a new folder and change ONLY path constants.

Current code = this worktree (2b9efa253 code; d8808c164 differs only in docs).
Prior code   = git archive of dcb97f1ed (scratch).
Prior fixtures (10-15 originals) = the bundle's rint_g2_impl_reverify_20261015/tmp/join_independent (read-only).

Every replacement must match exactly once; otherwise abort.  Writes a unified diff per probe.
Usage: python3 -I patch_probes.py
"""
import difflib
import os
import sys

SCR = '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad'
BUNDLE = SCR + '/import_rq7/x'
SRC_PROBES = BUNDLE + '/rint_join_q7_recheck_20261020/probes'
REPRO = SCR + '/import_rq7_repro/rint_join_q7_recheck_20261020'
WT = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a43562c127acff2de'
OLDT = SCR + '/import_rq7_repro/old_dcb97f1ed'
PRIOR_TMP = BUNDLE + '/rint_g2_impl_reverify_20261015/tmp/join_independent'

BLOCK = (
    '# [import 10-20] path constants only — current = worktree (review-pin code), prior = git archive dcb97f1ed,\n'
    '# prior 10-15 fixtures = bundle originals (read-only).\n'
    f'WT = Path({WT!r})\n'
    f'OLDT = Path({OLDT!r})\n'
    f'PRIOR_TMP = Path({PRIOR_TMP!r})\n'
)

ANCHOR = 'ROOT = Path(__file__).resolve().parents[1]\n'
EDITS = {
    'structure_minimal_replay.py': [
        (ANCHOR, ANCHOR + BLOCK),
        ('str(ROOT / "source/scripts"),', 'str(WT / "scripts"),'),
        ('D = ROOT.parent / "rint_g2_impl_reverify_20261015/tmp/join_independent"', 'D = PRIOR_TMP'),
    ],
    'structure_probe.py': [
        (ANCHOR, ANCHOR + BLOCK),
        ('str(ROOT / "source/scripts"),', 'str(WT / "scripts"),'),
        ('PRIOR / "source/scripts/rint_iface_join.py"', 'OLDT / "scripts/rint_iface_join.py"'),
        ('PRIOR / "tmp/join_independent"', 'PRIOR_TMP'),
        ('data = ROOT / "source/docs/data"', 'data = WT / "docs/data"'),
    ],
    'numeric_review.py': [
        (ANCHOR, ANCHOR + BLOCK),
        ('SRC = (WORK / "rint_g2_impl_reverify_20261015/source") if BASELINE else ROOT / "source"',
         'SRC = OLDT if BASELINE else WT'),
    ],
    'numeric_overflow_replay.py': [
        (ANCHOR, ANCHOR + BLOCK),
        ('SRC = ROOT.parent / "rint_g2_impl_reverify_20261015/source" if BASELINE else ROOT / "source"',
         'SRC = OLDT if BASELINE else WT'),
    ],
    'q7_independent.py': [
        (ANCHOR, ANCHOR + BLOCK),
        ('BASE = ROOT.parent / "rint_g2_impl_reverify_20261015/source/scripts"', 'BASE = OLDT / "scripts"'),
        ('NEW = ROOT / "source/scripts"', 'NEW = WT / "scripts"'),
    ],
    'run_submitted.py': [
        ('R=Path(__file__).resolve().parents[1]\n', 'R=Path(__file__).resolve().parents[1]\n' + BLOCK),
        ("BASE=R.parent/'rint_g2_impl_reverify_20261015/source'", 'BASE=OLDT'),
        ("text=(R/'source/scripts'/test)", "text=(WT/'scripts'/test)"),
        # Linux has the real resource module; the bundle's Windows-only shim (support/resource.py) would shadow it.
        ("paths=[R/'support',R/'source/scripts',", "paths=[WT/'scripts',"),
        ("cmd += [str(R/'source/scripts'/args[0]),*args[1:]]", "cmd += [str(WT/'scripts'/args[0]),*args[1:]]"),
        ("cwd=BASE if mode=='old' else R/'source'", "cwd=BASE if mode=='old' else WT"),
    ],
}

os.makedirs(REPRO + '/probes', exist_ok=False)
os.makedirs(REPRO + '/evidence')
os.makedirs(REPRO + '/tmp')
all_diff = []
for name, edits in EDITS.items():
    text = open(os.path.join(SRC_PROBES, name), encoding='utf-8').read()
    new = text
    for old, rep in edits:
        n = new.count(old)
        if n != 1:
            sys.exit(f'{name}: expected exactly 1 occurrence of {old!r}, found {n}')
        new = new.replace(old, rep, 1)
    # No remaining reference to the bundle's (absent) source/ folders in executable lines.
    for i, line in enumerate(new.splitlines(), 1):
        if ('source/scripts' in line or "/source'" in line or '/source")' in line) and not line.lstrip().startswith('#'):
            sys.exit(f'{name}:{i}: residual source path: {line}')
    with open(os.path.join(REPRO, 'probes', name), 'x', encoding='utf-8') as fh:
        fh.write(new)
    all_diff += difflib.unified_diff(text.splitlines(True), new.splitlines(True),
                                     fromfile='bundle/probes/' + name, tofile='repro/probes/' + name)
with open(os.path.join(SCR, 'import_rq7_repro', 'probe_path_changes.diff'), 'w', encoding='utf-8') as fh:
    fh.writelines(all_diff)
print('patched', len(EDITS), 'probes into', REPRO)
