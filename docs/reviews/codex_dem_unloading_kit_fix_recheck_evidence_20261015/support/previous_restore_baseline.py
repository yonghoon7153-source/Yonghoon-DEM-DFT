"""Previous independent restoration baseline; definitions only.

Origin: dem_unloading_kit_reverify_20261014/probes/runner_recheck.py
Original file SHA256: 61662b0f662473d67cf2024e32bc79aec8a4b647772ac39747e2563b4b5db3bb
The baseline function below is copied without semantic changes. Its globals
are supplied by probes/receipt_ids_recheck.py, which loads this definition by AST.
"""

def baseline(root):
    j = root / BED / 'RJ'
    g1, g3 = B['g1'].split(), B['g3'].split()
    resets = ''.join(f'Resetting {k} state of Fix {f} Style {s} from restart file info\n'
                     for f, s, ks in R.EXPECTED_RESETS for k in ks)
    head = 'Step Atoms KinEng ul_erot ul_Ps pressMPa CPU\n'
    scr = ('LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, git commit 3d5c00f)\n' + resets + head +
           f'{g1[0]} {g1[1]} {g1[2]} 1e-08 {g1[4]} {g1[4]} 0\n' +
           'Loop time of 0 on 6 procs for 0 steps\n' + head +
           f'{g1[0]} {g1[1]} {g1[2]} 1e-08 {g1[4]} {g1[4]} 0\n' +
           f'{g3[0]} {g3[1]} {g3[2]} 1e-08 {g3[4]} {g3[4]} 1\n' +
           'Loop time of 1 on 6 procs for 2000 steps\nUL_R_DONE\n')
    put(j / 'R/screen.txt', scr)
    put(root / BED / 'in' / B['orig_log'], scr)
    for stage, kind, marker in (('Ut0', 'Ut0', 'UL_SUMMARY arm=Ut0 result=DONE'),
                                ('UN', 'UNread', 'UL_UN_DONE')):
        put(j / stage / 'screen.txt',
            'LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, git commit 3d5c00f)\n'
            'Loop time of 1 on 6 procs for 100 steps\n' + marker + '\n')
        put(j / stage / 'run_check.txt', f'{kind} screen.txt PASS rc=0 procs=6\n')
    put(j / 'R/run_check.txt', 'R screen.txt PASS rc=0 procs=6\n')
    js(j / 'g0.json', {'status': 'PASS', 'violations': []})
    put(j / 'run_manifest.txt', f'bed={BED}\njob=RJ\nresume=0\ngate=ALLOW\nstart=x\n'
        'stage=G0 rc=0\nstage=Ut0 screen=screen.txt rc=0 check=PASS\n'
        'stage=R screen=screen.txt rc=0 check=PASS\nstage=UNread screen=screen.txt rc=0 check=PASS\n'
        'reader_restore_rc=0\nreader_kebase_rc=0\nend=x fails=0 reader_rc=0\n')
    acols = ['id', 'type', 'x', 'y', 'z', 'radius', 'vx', 'vy', 'vz']
    atoms = [dict(zip(acols, [i, 3, i*.001, .002, .003, .0005, 1e-6, 0, 0])) for i in range(1, 4)]
    ccols = [f'c_cpl[{i}]' for i in range(1, 27)]
    contact = dict(zip(ccols, [.001,.01,.01,.0015,.01,.01,1,2,0,-.5,0,0,-.5,0,0,0,.01,0,0,0,0,1e-8,1e-5,.00125,.01,.01]))
    for base in (root / BED / 'in', j / 'R/g2'):
        base.mkdir(parents=True, exist_ok=True)
        L.write_custom(str(base / f'atom_{S0}.liggghts'), S0, acols, atoms)
        L.write_local(str(base / f'contact_{S0}.liggghts'), S0, ccols, [contact])
        put(base / f'mesh_{S0}.stl', 'solid fixture\nendsolid fixture\n')
    hist = []
    for atom in atoms:
        a = dict(atom, mass=1e-6, omegax=0, omegay=0, omegaz=0, fx=0, fy=0, fz=0)
        a.update({f'f_history_zwall_bot[{i}]': (2e-5 if atom['id'] == 1 and i == 1 else 0) for i in range(1, 5)})
        hist.append(a)
    zero = [{**a, **{f'f_history_zwall_bot[{i}]': 0 for i in range(1, 5)}} for a in hist]
    for rel, step, cols, rows in [('R/obs/pre_bot.dump', S0, R.HIST_PRE_COLS, hist),
                                (f'R/obs/post_atom_{S0}.dump', S0, R.HIST_POST_COLS, hist),
                                ('R/obs/end_pre_bot.dump', END, R.HIST_PRE_COLS, hist),
                                ('UN/obs/un_pre_bot.dump', END, R.HIST_PRE_COLS, zero)]:
        path = j / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        L.write_custom(str(path), step, list(cols), rows)
    # Complete UK evidence provides a genuine production-generated S2 baseline.
    uk = j/'UK'
    put(uk/'screen.txt', 'LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, git commit 3d5c00f)\n'
        'Loop time of 1 on 6 procs for 15000 steps\nUL_SUMMARY arm=UK result=DONE\n')
    put(uk/'run_check.txt', 'UK screen.txt PASS rc=0 procs=6\n')
    put(uk/'ul_summary.txt', f'result=DONE\narm=UK\nbed={BED}\n')
    put(uk/'ul_events.csv', ','.join(P['records']['events_cols']) + f'\nSTART,0,{S0},{B["h0"]},0,s0\n')
    rows = [f'UK,{BED},0,{w},4,{S0+P["windows"]["W0"]*w},{B["h0"]},0,0.16,2e-07,{rot},0,-1,-1,-1,400,160417,11,2e-07'
            for w, rot in ((1, 3e-8), (2, 1e-8), (3, 2e-8))]
    put(uk/'ul_windows.csv', ','.join(P['records']['windows_cols']) + '\n' + '\n'.join(rows) + '\n')
    k = R.kebase(str(root), BED, P)
    assert k['s2_limit'] is not None and not k['problems'], k
    return j

