#!/usr/bin/env python3
"""PAI mutation spot-check — weaken one new guard at a time (F01 2nd edition R1–R8 · F02) in a scratch copy of
scripts/resume_ckpt.sh (2dc7f693) and run the repo test suite group against it (--script <mutant> --only <grp>).
A mutant 'survives' when the group still prints 'N PASS · 0 FAIL'.  Each replacement must match exactly once.
usage: python3 mutate_spot.py <scratch dir> [name ...]
"""
import os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '../../../../..'))
TOOL = os.path.join(REPO, 'scripts/resume_ckpt.sh')
TEST = os.path.join(REPO, 'scripts/test_resume_ckpt.py')

M = [  # (name, group, guard, old, new)
    ('R1_keypos_off', 'VP', 'run_state KEYPOS $ in key positions',
     "        kp = [w[x] for x in KEYPOS.get(c, ()) if x < n and '$' in w[x]]\n",
     "        kp = []\n"),
    ('R2_runevery_off', 'VP', 'mprefix_check run … every commands',
     "        if w[0] == 'run' and 'every' in w[2:]:\n            cs = [x for x in w[w.index('every', 2) + 2:] if x != 'NULL']\n",
     "        if w[0] == 'run' and 'every' in w[2:]:\n            cs = []\n"),
    ('R2_partition_off', 'VP', 'mprefix_check partition command',
     "            if (words(part_cmd(l)) or [''])[0] not in IFOK:\n",
     "            if False:\n"),
    ('R2_unsup_partition_off', 'VP', 'unsupported() partition inner command',
     "            todo.append(cw[3:])                    # 10-30 (사전 공격 R2)",
     "            pass  # todo.append(cw[3:])                    # 10-30 (사전 공격 R2)"),
    ('R3_ctrl_off', 'VP', 'deck_lines control-character rejection',
     "            if (c < 32 and c != 9 and not (c == 13 and j == len(p) - 1)) or c == 127:\n",
     "            if False:\n"),
    ('R3_nonascii_off', 'VP', 'deck_lines non-ASCII outside comments',
     "        bad = [x for x in c if x > 127]\n",
     "        bad = []\n        c = bytes(x if x < 128 else 32 for x in c)\n"),
    ('R3_amp_space', 'VP', 'deck_lines & join without space (old: one space)',
     "                line = full[:m - 1]\n",
     "                line = full[:m - 1] + b' '\n"),
    ('R4_printfile_off', 'VP', 'print_file_reads call',
     "        print_file_reads(R, q, '재개 덱', probs)  # 10-30 사전 공격 R4\n",
     "        pass\n"),
    ('R5_flowwrite_off', 'VP', 'flow_before_write call',
     "        flow_before_write(M[:pM], probs)          # 10-30 사전 공격 R5\n",
     "        pass\n"),
    ('R6_seq_dollar_off', 'VP', 'seq_cmp $ in mesh file name',
     "                if '$' in nf or '$' in (mesh_file(b, a) or ''):\n",
     "                if False:\n"),
    ('R6_state_marker_off', 'VP', 'state_cmp mesh file expanded with value markers',
     "            elif any(c in nfx for c in (VAL0, VAL1, RT0, RT1)):\n",
     "            elif False:\n"),
    ('R7_expand_cap_off', 'VP', 'expand() size cap (both checks)',
     ["        if size > XCAP:\n            return None, xcap_why(x)              # 10-30 사전 공격 R7",
      "    if size > XCAP:\n        return None, xcap_why(x)\n    t = VAL0"],
     ["        if False:\n            return None, xcap_why(x)              # 10-30 사전 공격 R7",
      "    if False:\n        return None, xcap_why(x)\n    t = VAL0"]),
    ('R7_all_caps_off', 'VP', 'expand() + var_env() size caps',
     ["        if size > XCAP:\n            return None, xcap_why(x)              # 10-30 사전 공격 R7",
      "    if size > XCAP:\n        return None, xcap_why(x)\n    t = VAL0",
      "            if not bad and len(b) > XCAP:\n"],
     ["        if False:\n            return None, xcap_why(x)              # 10-30 사전 공격 R7",
      "    if False:\n        return None, xcap_why(x)\n    t = VAL0",
      "            if False:\n"]),
    ('R7_varenv_cap_off', 'VP', 'var_env() size cap',
     "            if not bad and len(b) > XCAP:\n",
     "            if False:\n"),
    ('F02_envlike_off', 'RB', 'runnerck ENVLIKE rejection',
     "        if ENVLIKE.match(s):\n",
     "        if False:\n"),
    ('F02_cd_realpath_off', 'RB', 'runnerck cd realpath = work folder',
     "            elif os.path.realpath(s[3:]) != WR:\n",
     "            elif False:\n"),
    ('F02_injob_check_off', 'RB', 'rendered runner in-job sha256 check',
     "            '[ \"$ds\" = \"%s\" ] && [ \"$ks\" = \"%s\" ] || { echo",
     "            'true || [ \"$ds\" = \"%s\" ] && [ \"$ks\" = \"%s\" ] || { echo"),
    ('F02_g0_identity_off', 'RB', 'G0 identity gate (GI forced 1)',
     "  GI=0\n  if [ \"$NLID\" != 1 ]",
     "  GI=1\n  if false && [ \"$NLID\" != 1 ]"),
    ('F02_receipt_mis_off', 'RB', 'receipt file sha256 vs memory (MIS)',
     "      [ -z \"$BLK\" ] && [ \"$(sha256sum < $AD/main_inputs.sha256 2>/dev/null | cut -c1-64)\" != \"$MIS\" ] \\\n",
     "      [ -z \"$BLK\" ] && false \\\n"),
    ('F02_receipt_c_off', 'RB', 'sha256sum -c of the 5 inputs before main',
     "      [ -z \"$BLK\" ] && ! CKO=$(sha256sum -c --quiet $AD/main_inputs.sha256 2>&1) \\\n",
     "      [ -z \"$BLK\" ] && false \\\n"),
    ('F02_symlink_S_off', 'RB', 'stopped folder symlink rejection',
     "  [ -L \"$S\" ] && { rej",
     "  false && { rej"),
    ('F02_error_identity_excl_off', 'RB', 'ERROR count excludes identity line (revert to plain grep)',
     "E=$(grep -av '^LMP_IDENTITY ' $T | grep -ac ERROR)",
     "E=$(grep -ac ERROR $T)"),
]


def main():
    sp = sys.argv[1]
    pick = set(sys.argv[2:])
    os.makedirs(os.path.join(sp, 'mut'), exist_ok=True)
    src = open(TOOL, encoding='utf-8').read()
    rows = []
    for name, grp, guard, old, new in M:
        if pick and name not in pick:
            continue
        olds, news = (old, new) if isinstance(old, list) else ([old], [new])
        ks = [src.count(o) for o in olds]
        if any(k != 1 for k in ks):
            rows.append((name, grp, guard, 'BAD-MUTANT (match %s)' % ks, ''))
            print(name, 'BAD-MUTANT', ks, flush=True)
            continue
        mut = src
        for o, n_ in zip(olds, news):
            mut = mut.replace(o, n_)
        mp = os.path.join(sp, 'mut', name + '.sh')
        with open(mp, 'w', encoding='utf-8') as f:
            f.write(mut)
        t0 = time.time()
        env = dict(os.environ, TMPDIR=os.path.join(sp, 'tmp'))
        p = subprocess.run(['nice', '-n', '10', sys.executable, TEST, '--script', mp, '--only', grp], cwd=REPO, env=env,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1800)
        out = p.stdout.decode('utf-8', 'replace')
        tot = re.findall(r'^(\d+) PASS · (\d+) FAIL$', out, re.M)
        fails = re.findall(r'^FAIL (\S+)', out, re.M)
        res = ('%s PASS · %s FAIL' % tot[-1]) if tot else 'no summary (rc %d)' % p.returncode
        verdict = 'survived' if tot and tot[-1][1] == '0' else 'caught'
        rows.append((name, grp, guard, '%s · %s · %.0fs' % (verdict, res, time.time() - t0), ' '.join(fails[:12])))
        print('%-28s %-3s %-9s %s | %s' % (name, grp, verdict, res, ' '.join(fails[:12])), flush=True)
        os.remove(mp)
    print('\n| 변이 | 묶음 | 약하게 한 관문 | 결과 | 실패한 시험 (앞 12) |\n|---|---|---|---|---|')
    for r in rows:
        print('| %s | %s | %s | %s | %s |' % r)


if __name__ == '__main__':
    main()
