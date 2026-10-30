#!/usr/bin/env python3
"""PAI probe — D0.7 resume deck emulating ibb dem_restart.py (no copy of dem_restart.py exists in the repo).

Method: learn the transformation from the D2 precedent (main deck -> r4 deck as received from ibb), undo the two
edits resume_ckpt.sh itself makes after dem_restart.py (template re-declaration after read_restart · first long run
179999 -> 180000), check that the transformation T reproduces the D2 "raw" r4 deck byte for byte, then apply the same
T to the D0.7 main deck (same 257-line layout) with case kg50_d07_b50 and suffix r56.

Writes into OUT (argv[1]):
  d2_raw_r4.liggghts        D2 r4 with the tool's own edits undone (= what dem_restart.py wrote, reconstructed)
  d07_raw_r56.liggghts      D0.7 resume deck as dem_restart.py would write it (reconstructed)
  d07_tool_r56.liggghts     d07_raw_r56 + the tool's template insertion (its awk) + fix-run 179999 -> 180000
  d07_helper_runner_r56.sh  D0.7 helper runner in the D2 r4 form (cd = absolute work path placeholder {W})
Exit code 0 = T reproduced D2 exactly.
"""
import hashlib, os, sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..'))
D2 = os.path.join(REPO, 'docs/data/kg50_resume_tests_20261027/d2_main_1028_0942')
D07 = os.path.join(REPO, 'docs/data/kg50_decks_20261027_v3_b50/kg50_d07_b50')


def T(main_lines, case, sfx, ckpt, step, remain):
    """main deck lines (with \n) -> dem_restart.py style resume deck lines (reconstructed from the D2 precedent)."""
    L = list(main_lines)
    assert L[48].startswith('region reg_box block') and L[49].startswith('create_box'), (L[48], L[49])
    assert L[107].startswith('fix pts1 ') and L[116].startswith('region reg_mix'), (L[107], L[116])
    assert L[118].startswith('print "====== INSERTING') and L[125].startswith('unfix ins_mix'), (L[118], L[125])
    assert L[166] == 'run 200000\n', L[166]
    out = ['# %s RESTART (%s) — settling 체크포인트에서 이어받음\n' % (case, sfx),
           '#   read_restart : %s\n' % ckpt, '#   step         : %d\n' % step, '\n']
    for i, l in enumerate(L):
        if i == 48:
            out += ['\n', 'read_restart    %s\n' % ckpt]
            continue
        if i == 49 or 107 <= i <= 116 or 118 <= i <= 125:
            continue
        if l.startswith('shell mkdir '):
            l = 'shell mkdir -p ' + l[len('shell mkdir '):]
        if i == 166:
            l = 'run %d   # 원래 200000 − 이미 %d\n' % (remain, step)
        if l.startswith('write_restart restart_') and 'after_settling' in l:
            l = 'write_restart   ' + l[len('write_restart '):]
        out.append(l)
    return out


def tool_edits(lines, main_lines):
    """resume_ckpt.sh lines 1903-1905 (template awk after read_restart) + fix-run (179999 -> 180000) on the r-deck."""
    tmpl = [l for l in main_lines if l.split()[:1] == ['fix'] and len(l.split()) > 1 and
            (l.split()[1] == 'pdd_mix' or (l.split()[1].startswith('pts') and l.split()[1][3:].isdigit()))]
    out = []
    for l in lines:
        out.append(l)
        if l.split()[:1] == ['read_restart']:
            out += tmpl
    return [l.replace('run 179999   #', 'run 180000   #', 1) if l.startswith('run 179999 ') else l for l in out]


def undo_tool(lines):
    """D2 r4 as received -> remove the 4 template lines after read_restart, 180000 -> 179999."""
    out, skip = [], 0
    for l in lines:
        if skip:
            skip -= 1
            continue
        out.append(l)
        if l.startswith('read_restart'):
            skip = 4
    return [l.replace('run 180000   #', 'run 179999   #', 1) if l.startswith('run 180000 ') else l for l in out]


def rd(p):
    with open(p, encoding='utf-8', newline='') as f:
        return f.read().splitlines(keepends=True)


def wr(p, lines):
    with open(p, 'w', encoding='utf-8', newline='') as f:
        f.write(''.join(lines))
    with open(p, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    d2m = rd(os.path.join(D2, 'input_kg50_d2_b50.liggghts'))
    d2r = rd(os.path.join(D2, 'input_kg50_d2_b50_r4.liggghts'))
    raw = undo_tool(d2r)
    mine = T(d2m, 'kg50_d2_b50', 'r4', 'restart_kg50_d2_b50/restart_settling_20001.bin', 20001, 179999)
    ok = mine == raw
    print('T(D2 main) == D2 r4 with tool edits undone:', ok)
    if not ok:
        import difflib
        sys.stdout.writelines(difflib.unified_diff(raw, mine, 'raw', 'mine'))
    back = tool_edits(raw, d2m)
    print('tool_edits(raw) == D2 r4 as received:', back == d2r)
    print('d2_raw_r4', wr(os.path.join(out, 'd2_raw_r4.liggghts'), raw))
    d07m = rd(os.path.join(D07, 'input_kg50_d07_b50.liggghts'))
    d07raw = T(d07m, 'kg50_d07_b50', 'r56', 'restart_kg50_d07_b50/restart_settling_20001.bin', 20001, 179999)
    print('d07_raw_r56', wr(os.path.join(out, 'd07_raw_r56.liggghts'), d07raw))
    print('d07_tool_r56', wr(os.path.join(out, 'd07_tool_r56.liggghts'), tool_edits(d07raw, d07m)))
    rn = rd(os.path.join(D2, 'run_kg50_d2_b50_r4.sh'))
    rn = [l.replace('kg50_d2_b50_r4', 'kg50_d07_b50_r56').replace('-n 4\n', '-n 56\n').replace('-np 4 ', '-np 56 ')
          .replace('/lustre/home/yonghoon/dem_test/kg50_d2_b50', '{W}') for l in rn]
    print('d07_helper_runner_r56', wr(os.path.join(out, 'd07_helper_runner_r56.sh'), rn))
    return 0 if ok and back == d2r else 1


if __name__ == '__main__':
    sys.exit(main())
