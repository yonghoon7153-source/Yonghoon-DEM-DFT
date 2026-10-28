#!/usr/bin/env python3
"""Make one-gate-off mutants of the fixed resume_ckpt.sh (scratch copies only) and run the worktree test suite on each.
usage: python3 -I mutants.py make | run <jobs>"""
import os, subprocess, sys, concurrent.futures as cf

P = os.path.dirname(os.path.abspath(__file__))
WT = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/kg50fix-1028'
SRC = os.path.join(WT, 'scripts/resume_ckpt.sh')
MD = os.path.join(P, 'mut')

M = [
    # ---- python (deckcheck) ----
    ('py_unsupported', "    # 다룰 수 없는 구문 (10-28 KG50R-03 (ⅵ)) — if 안 명령까지 · '' = 없음\n    w = words(l)\n",
     "    # 다룰 수 없는 구문 (10-28 KG50R-03 (ⅵ)) — if 안 명령까지 · '' = 없음\n    return ''\n    w = words(l)\n"),
    ('py_reinsert', "probs.append('재개 덱에 삽입 fix (재삽입): [%s]' % l)", "pass"),
    ('py_cf_def', "probs.append('재개 덱이 %s_%s 를 쓰는데 정의가 없음: [%s]' % (kind, name, l))", "pass"),
    ('py_rr_count', "    if len(rs) != 1:\n        probs.append('재개 덱에 read_restart 가 %d 개 (1 개여야 · 10-28 KG50R-03)' % len(rs))",
     "    if len(rs) == 0:\n        probs.append('재개 덱에 read_restart 가 %d 개 (1 개여야 · 10-28 KG50R-03)' % len(rs))"),
    ('py_rr_file', "probs.append('재개 덱 read_restart 가 체크포인트 %s 가 아님 (10-28 KG50R-03): [%s]' % (ckpt, R[rs[0]]))", "pass"),
    ('py_ir_before', "    if ir < rs[0]:\n", "    if False:\n"),
    ('py_first_form', "    # 재개 덱 첫 긴 run = 꼬리 없는 [run N] 원 줄 한 줄 (10-28 KG50R-02 · 05) — '' = 됨 · 아니면 이유\n",
     "    # 재개 덱 첫 긴 run = 꼬리 없는 [run N] 원 줄 한 줄 (10-28 KG50R-02 · 05) — '' = 됨 · 아니면 이유\n    return ''\n"),
    ('py_q3', "        if base.startswith('restart_compress_') or (not known and labs):\n", "        if False:\n"),
    ('py_pre', "            if pre:\n", "            if False:\n"),
    ('py_range', "            if not step0 < s0 < step:\n", "            if False:\n"),
    ('py_end', "                if end != step:\n", "                if False:\n"),
    ('py_write_plain', "        if bad:\n            probs.append('첫 긴 run 길이를 정할 수 없음", "        if False:\n            probs.append('첫 긴 run 길이를 정할 수 없음"),
    ('py_sched', "    if rl != ml:\n", "    if False:\n"),
    ('py_seg', "            seq_cmp(seg, R[q:ir], W, notes, probs, '체크포인트 뒤 ~ 첫 긴 run 앞 명령')", "            pass"),
    ('py_tail', "    seq_cmp(M[im + 1:], R[ir + 1:], W, notes, probs, '첫 긴 run 뒤 명령')", "    pass"),
    ('py_mprefix', "        mprefix_check(M[:pM], probs)", "        pass"),
    ('py_setup', "        setup_check([l for i, l in enumerate(R[:q]) if i != rs[0]], M[:pM], probs)", "        pass"),
    ('py_state', "        state_cmp(run_state(M[:pM], '본 덱 체크포인트 앞', probs), run_state(R[:q], '재개 덱 준비 구간', probs), W, notes, probs)", "        pass"),
    ('py_varrefs', "    var_refs(R, probs)\n    label_check", "    pass\n    label_check"),
    ('py_labels', "    label_check(M, R, pM, probs)\n    return probs, notes", "    pass\n    return probs, notes"),
    ('py_label_dup', "        if dup:\n            probs.append('%s label 이 겹침", "        if False:\n            probs.append('%s label 이 겹침"),
    ('py_jump_absent', "            if cw[2] not in rl:\n", "            if False:\n"),
    ('py_jump_place', "            elif ml.get(cw[2], -1) < pM:\n", "            elif False:\n"),
    ('py_var_style', "                probs.append('%s 에 다룰 수 없는 변수 꼴", "                pass  # probs.append('%s 에 다룰 수 없는 변수 꼴"),
    ('py_need', "    # 본 덱 상태에 있으면 재개 덱에도 꼭 있어야 하는 것 (템플릿 fix 는 선언하면 같아야만)\n",
     "    # 본 덱 상태에 있으면 재개 덱에도 꼭 있어야 하는 것 (템플릿 fix 는 선언하면 같아야만)\n    return False\n"),
    ('py_qnone', "        if q is None:\n            probs.append('재개 덱에 본 덱 체크포인트 뒤 첫 명령", "        if False:\n            probs.append('재개 덱에 본 덱 체크포인트 뒤 첫 명령"),
    ('py_cut_reread', "        if deck(t) != R[:ir] + ['run %d' % tn]:\n", "        if False:\n"),
    ('py_cut_rawlen', "    if len(rawb) != len(raw):\n        print('재개 덱 원 줄 수를 못 맞춤", "    if False:\n        print('재개 덱 원 줄 수를 못 맞춤"),
    ('py_ts_stepc', "        if w[0] in STEPC and i != rs[0]:\n", "        if False:\n"),
    ('py_ts_flow', "        if w[0] in FLOWC:\n            print('흐름 명령", "        if False:\n            print('흐름 명령"),
    ('py_ts_if', "        if w[0] == 'if' and not if_ok(w):\n            print('print · quit 말고", "        if False:\n            print('print · quit 말고"),
    ('py_ts_last', "    if not runs or (words(L[-1]) or [''])[0] != 'run':\n", "    if not runs:\n"),
    ('py_runn_tail', "        if k in rest:\n            return None, 'run 꼬리 %s' % k", "        if False:\n            return None, 'run 꼬리 %s' % k"),
    ('py_fixrun_recheck', "        if len(R2) != len(R) or [i for i in range(len(R)) if R[i] != R2[i]] != [ir] or R2[ir] != 'run %d' % n1 or p2:\n",
     "        if False:\n"),
    ('py_fixrun_one', "    if len(probs) != 1 or len(rem) != 1:\n", "    if len(rem) != 1:\n"),
    ('py_mesh_exists', "                if os.path.isfile(os.path.join(W, nf)):\n                    notes.append('판 메시 파일만 다름 (%s): %s' % (what, nf))",
     "                if True:\n                    notes.append('판 메시 파일만 다름 (%s): %s' % (what, nf))"),
    # ---- shell ----
    ('sh_seen', 'case "$SEEN" in *" $C "*) rej "케이스 목록"', 'case "$SEEN" in *" __never__ "*) rej "케이스 목록"'),
    ('sh_qfail', 'QL=$(squeue -u $USER -h -o %j 2>/dev/null) || { rej', 'QL=$(squeue -u $USER -h -o %j 2>/dev/null) || true || { rej'),
    ('sh_qbusy', '  if printf \'%s\\n\' "$QL" | grep -qxE "$(qre $C)"; then rej', '  if false; then rej'),
    ('sh_compress', '[ "$M" = compress ] && { rej "압축 체크포인트 (Q3)"', 'false && { rej "압축 체크포인트 (Q3)"'),
    ('sh_approve_start', 'if [ $TONLY = 0 ] && ! {', 'if false && ! {'),
    ('sh_approve_main', '[ -z "$BLK" ] && { [ "$T2" != "$APT" ] || [ "$H2" != "$APH" ]; } && BLK=', 'false && BLK='),
    ('sh_q2fail', 'QL2=$(squeue -u $USER -h -o \'%i %j\' 2>/dev/null) || BLK=', 'QL2=$(squeue -u $USER -h -o \'%i %j\' 2>/dev/null) || true || BLK='),
    ('sh_q2busy', '[ -n "$BZ" ] && BLK=', 'false && BLK='),
    ('sh_mainjob', '[ -z "$BLK" ] && [ -e $AD/main_job.txt ] && BLK=', 'false && BLK='),
    ('sh_jnum', 'if [ $JR = 0 ] && [[ "$J" =~ ^([0-9]+)(;[^[:space:]]*)?$ ]]; then J=${BASH_REMATCH[1]}', 'if [ -n "$J" ]; then :'),
    ('sh_lpn', ' && [ "$LPN" = "$LN" ]', ''),
    ('sh_lpl', ' && [ "$LPL" -gt "$LTL" ]', ''),
    ('sh_fin', 'function fin(x){return x ~ /^[-+]?([0-9]+[.]?[0-9]*|[.][0-9]+)([eE][-+]?[0-9]+)?$/}', 'function fin(x){return 1}'),
    ('sh_nf', 'q&&NF==n&&$1~/^[0-9]+$/{ok=1', 'q&&$1~/^[0-9]+$/{ok=1'),
    ('sh_budget', 'if [ "$CPS" = - ] || [ "$NT" != $((CPS + CTN)) ] || [[ "$TDS" != *"[run $CTN]" ]]; then', 'if false; then'),
    ('sh_ts', '[[ "$TS" =~ ^[1-9][0-9]*$ ]] || {', 'true || {'),
    ('sh_lts', ' && [ "$LTS" = "$EXP" ]', ''),
    ('sh_miss', 'elif [ -n "$MISS" ]; then G3=0', 'elif false; then G3=0'),
    ('sh_g1', 'same "$a" "$b" 1e-6 && G1=1', 'G1=1'),
    ('sh_rmtd', 'TD=$W/input_${C}_${SFX}t.liggghts; rm -f $TD', 'TD=$W/input_${C}_${SFX}t.liggghts; :'),
    ('sh_cutc', 'if [ $CUTC = 0 ] && [[ "$CUT" =~ $CRE ]]; then', 'if [[ "$CUT" =~ $CRE ]]; then'),
    ('sh_tsc', 'if [ $TSC = 0 ] && [[ "$TSR" != *$\'\\n\'* ]] && [[ "$TSR" =~ $TRE ]]; then', 'if [[ "$TSR" =~ $TRE ]]; then'),
]

# old-behavior regression mutant: second loop over CASES with W job files (and do not move old markers)
OLD_LOOP = ('sh_stale_loop',
            'for ENT in $SUBMITTED; do\n',
            'for ENT in $(for c in $CASES; do [ -f $L/$c/job_${SFX}t.txt ] && echo "$c|$(cat $L/$c/job_${SFX}t.txt)"; done); do\n'
            '  [ -f $L/${ENT%|*}/$ATT/mode.txt ] || { mkdir -p $L/${ENT%|*}/$ATT; cp $L/${ENT%|*}/mode_$SFX.txt $L/${ENT%|*}/$ATT/mode.txt 2>/dev/null; '
            'awk \'{print 2000}\' $L/${ENT%|*}/mode_$SFX.txt > $L/${ENT%|*}/$ATT/lastrun_n.txt 2>/dev/null; }\n')
OM_OFF = ('  if [ -n "$OM" ]; then mkdir $AD/old_markers', '  if false; then mkdir $AD/old_markers')


def make():
    os.makedirs(MD, exist_ok=True)
    src = open(SRC, encoding='utf-8').read()
    out = []
    for name, a, b in M:
        n = src.count(a)
        if n != 1:
            print('ANCHOR', name, 'count', n)
            continue
        with open(os.path.join(MD, name + '.sh'), 'w', encoding='utf-8') as f:
            f.write(src.replace(a, b))
        out.append(name)
    s2 = src
    for a, b in (OLD_LOOP[1:], OM_OFF):
        assert s2.count(a) == 1, a
        s2 = s2.replace(a, b)
    with open(os.path.join(MD, OLD_LOOP[0] + '.sh'), 'w', encoding='utf-8') as f:
        f.write(s2)
    out.append(OLD_LOOP[0])
    print(len(out), 'mutants')


def run1(name):
    p = os.path.join(MD, name + '.sh')
    r = subprocess.run(['nice', '-n', '19', sys.executable, '-I', os.path.join(WT, 'scripts/test_resume_ckpt.py'), '--script', p],
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=WT)
    out = r.stdout.decode('utf-8', 'replace')
    with open(os.path.join(MD, name + '.out'), 'w', encoding='utf-8') as f:
        f.write(out)
    fails = [l.split(' · ')[0] for l in out.splitlines() if l.startswith('FAIL')]
    tail = [l for l in out.splitlines() if 'PASS ·' in l]
    return name, (tail[-1] if tail else 'NO SUMMARY rc=%d' % r.returncode), fails


def run(jobs):
    names = sorted(f[:-3] for f in os.listdir(MD) if f.endswith('.sh'))
    with cf.ThreadPoolExecutor(jobs) as ex:
        for name, summ, fails in ex.map(run1, names):
            print('%-20s %-22s %s' % (name, summ, ' | '.join(x[5:40] for x in fails[:4])), flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'make':
        make()
    else:
        run(int(sys.argv[2]))
