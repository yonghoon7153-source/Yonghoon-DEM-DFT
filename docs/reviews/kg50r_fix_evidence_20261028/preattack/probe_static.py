#!/usr/bin/env python3
"""Static (-C) probes on the real D2 deck pair -- new tool vs old tool. Writes variants to a temp dir only."""
import os, subprocess, sys, tempfile, shutil

P = os.path.dirname(os.path.abspath(__file__))
NEW = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/kg50fix-1028/scripts/resume_ckpt.sh'
OLD = os.path.join(P, 'resume_ckpt_old.sh')
D2 = os.path.join(P, 'd2')
MAIN = os.path.join(D2, 'input_kg50_d2_b50.liggghts')
RES = os.path.join(D2, 'input_kg50_d2_b50_r4.liggghts')
CK = 'restart_kg50_d2_b50/restart_settling_20001.bin'


def rd(p):
    with open(p, encoding='utf-8') as f:
        return f.read()


def sub1(t, old, new):
    assert t.count(old) == 1, (old, t.count(old))
    return t.replace(old, new)


def run(tool, main_text, res_text, ck=CK, s0='20001', wd_files=()):
    d = tempfile.mkdtemp(prefix='pst_', dir=P)
    try:
        m, r = os.path.join(d, 'main.liggghts'), os.path.join(d, 'res.liggghts')
        with open(m, 'w', encoding='utf-8') as f:
            f.write(main_text)
        with open(r, 'w', encoding='utf-8') as f:
            f.write(res_text)
        wd = os.path.join(d, 'wd')
        os.mkdir(wd)
        for n in wd_files:
            open(os.path.join(wd, n), 'w').close()
        p = subprocess.run(['bash', tool, '-C', m, r, ck, s0, wd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return p.returncode, p.stdout.decode('utf-8', 'replace').replace(d, '<tmp>')
    finally:
        shutil.rmtree(d, ignore_errors=True)


M0, R0 = rd(MAIN), rd(RES)
TMPL_END = 'fix pdd_mix all particledistribution/discrete 16800023 2 pts1 0.85 pts3 0.15\n'

cases = {}
# A: variable redefinition around an immediate ${} substitution in the setup region (after read_restart) -> real dt = 2e-6
cases['A_dt_redef'] = (M0, sub1(R0, TMPL_END, TMPL_END + 'variable dt      equal 2.0e-6\ntimestep        ${dt}\nvariable dt      equal 1.0e-6\n'), ())
# A2: same but gravity redefinition via variable (main has literal gravity -> must stay literal) -- control: should FAIL
cases['A2_ctrl_literal_dt'] = (M0, sub1(R0, TMPL_END, TMPL_END + 'timestep 2.0e-6\n'), ())
# B: main checkpoint run carries options that the resume's first long run drops
cases['B_main_every'] = (sub1(M0, 'run 200000\n\n# --- Settling', 'run 200000 every 1000 "velocity all set 0.0 0.0 0.0"\n\n# --- Settling'), R0, ())
cases['B2_main_startstop'] = (sub1(M0, 'run 200000\n\n# --- Settling', 'run 200000 start 0 stop 400000\n\n# --- Settling'), R0, ())
cases['B3_main_every_include'] = (sub1(M0, 'run 200000\n\n# --- Settling', 'run 200000 every 1000 "include extra.in"\n\n# --- Settling'), R0, ())
# C: mesh file name allowance -- resume tail loads a different (stale) STL that exists in the work folder
mesh = 'fix top_mesh all mesh/surface/stress file plate_kg50_d2_b50.stl type 1'
cases['C_stale_mesh_exists'] = (M0, sub1(R0, mesh, mesh.replace('plate_kg50_d2_b50.stl', 'plate_stale.stl')), ('plate_stale.stl',))
cases['C2_stale_mesh_missing'] = (M0, sub1(R0, mesh, mesh.replace('plate_kg50_d2_b50.stl', 'plate_stale.stl')), ())
# D: fix order swap in the setup region (gravity <-> viscous) -- order not compared
cases['D_fix_order'] = (M0, sub1(R0, 'fix gravi all gravity 98.1 vector 0.0 0.0 -1.0\nfix damp all viscous 1.0e-5\n',
                                 'fix damp all viscous 1.0e-5\nfix gravi all gravity 98.1 vector 0.0 0.0 -1.0\n'), ())
# E: duplicate definition of a material fix with a different value, final one equal -> state equal (no run between)
cases['E_fix_redef'] = (M0, sub1(R0, TMPL_END, TMPL_END + 'fix damp all viscous 0.5\n'), ())
# F: unfix + re-fix of a contact-history-carrying wall fix (history lost?) -- state text equal
wall = 'fix zwall_bot all wall/gran model hooke/hysteresis tangential history rolling_friction cdt primitive type 1 zplane 0.0\n'
cases['F_wall_refix'] = (M0, sub1(R0, TMPL_END, TMPL_END) + '', ())
GRAV = "fix gravi all gravity 98.1 vector 0.0 0.0 -1.0\n"
# G: NBSP / unicode whitespace inside a state line (LIGGGHTS tokenizer would not split there)
cases['G_nbsp_in_fix'] = (M0, sub1(R0, GRAV + 'fix damp all viscous 1.0e-5\n', GRAV + 'fix damp all viscous\u00a01.0e-5\n'), ())
cases['G2_tab_cr'] = (M0, sub1(R0, GRAV + 'fix damp all viscous 1.0e-5\n', GRAV + 'fix\tdamp all viscous 1.0e-5 \r\n'), ())
# H: & continuation without space (LIGGGHTS joins without space; deck() inserts one)
cases['H_amp_nospace'] = (M0, sub1(R0, GRAV + 'fix damp all viscous 1.0e-5\n', GRAV + 'fix damp all viscous&\n1.0e-5\n'), ())
# I: unicode digits in first long run
cases['I_fullwidth_run'] = (M0, sub1(R0, 'run 180000   #', 'run １８００００   #'), ())

for name, (m, r, wf) in cases.items():
    for tag, tool in (('new', NEW), ('old', OLD)):
        rc, out = run(tool, m, r, wd_files=wf)
        last = [l for l in out.splitlines() if l.strip()]
        probs = [l for l in last if l.lstrip().startswith('✗')]
        print('%-22s %-3s rc=%d  %s' % (name, tag, rc, (last[-1].strip() if last else '')))
        for p in probs[:3]:
            print('      ', p.strip()[:220])
