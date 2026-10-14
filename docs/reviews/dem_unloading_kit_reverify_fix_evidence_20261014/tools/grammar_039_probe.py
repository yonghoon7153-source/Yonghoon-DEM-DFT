#!/usr/bin/env python3
"""Q5 evidence probe — the grammar-fixture code at 039abb141 (run_history.sh --grammar-only + read_history.py --grammar,
extracted from git) on a mock binary → its grammar_verdict.json → the NEW preflight CLI (ul_reader.py grammar).

    python3 grammar_039_probe.py <repo worktree> <kit dir with the new ul_reader.py> <out json>

No LIGGGHTS: the fake lmp dispatches each history deck to the 039abb141 read_history.py --mock-stage (synthetic outputs).
This shows only that a verdict produced by the 039abb141 fixture code passes the new preflight when its decks/plate STL
equal the pins and the binary hash matches; it is not a native grammar PASS (that is ibb run 2).
"""
import glob
import hashlib
import json
import os
import subprocess
import sys
import tempfile

PIN = '039abb141'
REL = 'docs/data/ps45_unload_20261009/history_test'


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def main():
    repo, kit, out = (os.path.abspath(x) for x in sys.argv[1:4])
    res = {'pin': PIN, 'steps': []}
    with tempfile.TemporaryDirectory(prefix='gram039_') as td:
        src = os.path.join(td, 'src')
        os.makedirs(src)
        a = subprocess.run(['git', '-C', repo, 'archive', PIN, REL], capture_output=True)
        subprocess.run(['tar', '-x', '-C', src], input=a.stdout, check=True)
        h = os.path.join(src, REL)
        res['pin_files_sha256'] = {n: sha(os.path.join(h, n)) for n in sorted(os.listdir(h))}
        b = os.path.join(td, 'bin')
        os.makedirs(b)
        open(os.path.join(b, 'mpirun'), 'w').write(
            '#!/bin/bash\nnp=""\nwhile [ $# -gt 0 ]; do case "$1" in --oversubscribe) shift;; --bind-to) shift 2;; -np) np=$2; shift 2;;\n'
            '  *) break;; esac; done\nMOCK_NP=$np exec "$@"\n')
        # mock binary = the worktree's synthetic stage writer (a test double for LIGGGHTS; it needs the repo's source tgz) —
        # the runner (run_history.sh) and the judge (read_history.py --grammar) below are the 039abb141 files.
        mock = os.path.join(repo, REL, 'read_history.py')
        open(os.path.join(b, 'lmp'), 'w').write(
            '#!/bin/bash\nout=""; while [ $# -gt 0 ]; do case "$1" in -var) [ "$2" = out ] && out=$3; shift 3;; *) shift;; esac; done\n'
            'echo "LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, git commit 3d5c00f)"\n'
            f'exec {sys.executable} {mock} --mock-stage "$(basename "$out")" "$out"\n')
        for x in ('mpirun', 'lmp'):
            os.chmod(os.path.join(b, x), 0o755)
        lsha = sha(os.path.join(b, 'lmp'))
        work = os.path.join(td, 'work')
        os.makedirs(work)
        env = dict(os.environ, WORK_ROOT=work, MPIRUN=os.path.join(b, 'mpirun'), LMP=os.path.join(b, 'lmp'), NP='6', NP_ALT='4',
                   HIST_STAMP='20261014_000000', PY=sys.executable, ALLOW_CONCURRENT='1', ALLOW_OTHER_LMP='1')
        for k in ('MOCK_FAIL_STAGE', 'MOCK_FAIL_AFTER_STAGE', 'HIST_KIT', 'KIT', 'GRAMMAR_VERDICT'):
            env.pop(k, None)
        p = subprocess.run(['bash', os.path.join(h, 'run_history.sh'), '--grammar-only'], env=env, capture_output=True, text=True, timeout=900)
        res['steps'].append({'cmd': f'bash <{PIN}>/{REL}/run_history.sh --grammar-only (mock binary)', 'rc': p.returncode,
                             'stdout_tail': p.stdout[-3000:], 'stderr_tail': p.stderr[-1500:]})
        for st in ('P', 'GA', 'GB'):
            sp = glob.glob(os.path.join(work, 'gram_*', st, 'screen.out'))
            res[f'screen_{st}_tail'] = open(sp[0]).read()[-1500:] if sp else None
        gv = (glob.glob(os.path.join(work, 'gram_*', 'grammar_verdict.json')) or [None])[0]
        res['verdict_status'] = json.load(open(gv)).get('status') if gv else None
        res['verdict_exit_code'] = json.load(open(gv)).get('exit_code') if gv else None
        kitsums = glob.glob(os.path.join(work, 'kit_*', 'SHA256SUMS'))
        res['grammar_run_kit_SHA256SUMS_sha256'] = sha(kitsums[0]) if kitsums else None
        res['grammar_run_kit_lines'] = [ln for ln in open(kitsums[0]).read().splitlines()
                                        if ln.endswith(('in.hist_grammar.liggghts', 'in.hist_producer.liggghts', 'plate_hist.stl'))] if kitsums else []
        for tag, s in (('same_binary', lsha), ('other_binary', 'f' * 64)):
            q = subprocess.run([sys.executable, '-I', os.path.join(kit, 'ul_reader.py'), 'grammar', gv or '-', '--lmp-sha', s],
                               capture_output=True, text=True, timeout=300)
            res['steps'].append({'cmd': f'python3 -I ul_reader.py grammar <gram>/grammar_verdict.json --lmp-sha <{tag}>', 'rc': q.returncode,
                                 'stdout': q.stdout, 'stderr': q.stderr})
        res['lmp_sha256_mock'] = lsha
    res['ok'] = (res['steps'][0]['rc'] == 0 and res['verdict_status'] == 'PASS' and res['steps'][1]['rc'] == 0 and 'status=PASS' in res['steps'][1]['stdout']
                 and res['steps'][2]['rc'] == 2 and 'status=REFUSE' in res['steps'][2]['stdout'])
    json.dump(res, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(json.dumps({k: res[k] for k in ('ok', 'verdict_status', 'verdict_exit_code', 'grammar_run_kit_lines')}, ensure_ascii=False, indent=1))
    for s in res['steps'][1:]:
        print(s['rc'], s['stdout'].strip()[:400])
    return 0 if res['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())
