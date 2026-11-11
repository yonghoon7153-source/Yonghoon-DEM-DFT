# -*- coding: utf-8 -*-
# Independent re-computation of key cells of time_budget_v2 (does NOT import it).  Inputs = the probe bundle + registered script constants.
# usage: python3 chk_arith.py <repo root> <their json>
import json, math, sys, csv
from datetime import datetime, timedelta
repo, their = sys.argv[1], sys.argv[2]
J = json.load(open(their))
# ---- measured (read from the bundle files, not from their script) ----
scr = {}
for ln in open(repo + '/docs/data/rint2_probe6_a2_20261111/probe6_screen.txt'):
    if '=' in ln and ln.startswith('[probe6] '):
        k, v = ln[9:].split('=', 1); scr.setdefault(k.strip(), v.strip())
wall = int(scr['wall_s']); pre = int(scr['pre_step3_s']); raster = int(scr['raster_prep_s']); cgc = int(scr['cg_cert_s'])
cj = int(scr['cjunc_prep_s']); it_main = int(scr['cg_iters']); it_res = int(scr['cert_resolve_iters'])
save = wall - pre - raster - cgc
# ---- observed split: my own reading of samples.tsv (midpoints between the last / first sample of each gpu_util >= 97 run) ----
rows = [r for r in csv.reader(open(repo + '/docs/data/rint2_probe6_a2_20261111/samples.tsv'), delimiter='\t') if not r[0].startswith('#')]
el = [int(r[1]) for r in rows]; ut = [int(r[7]) for r in rows]
t_solve = pre + raster
runs, cur = [], None
for e, u in zip(el, ut):
    if e < t_solve - 15: continue
    hi = u >= 97
    if hi and cur is None: cur = [e, e]
    elif hi: cur[1] = e
    elif cur is not None: runs.append(cur); cur = None
if cur: runs.append(cur)
runs = [r for r in runs if r[1] - r[0] > 600]
assert len(runs) == 2, runs
def mid_after(t):   # midpoint between sample t and the next sample
    i = el.index(t); return (el[i] + el[i + 1]) / 2.0
def mid_before(t):
    i = el.index(t); return (el[i] + el[i - 1]) / 2.0
m_end = mid_after(runs[0][1]); r_start = mid_before(runs[1][0]); r_end = mid_after(runs[1][1])
main_s = m_end - t_solve; gap = r_start - m_end; res_s = r_end - r_start; post = (t_solve + cgc) - r_end
print('measured: wall %d pre %d raster %d (cjunc %d) cg+cert %d save %d | iters %d + %d' % (wall, pre, raster, cj, cgc, save, it_main, it_res))
print('my split of cg+cert: main %.0f s  gap %.0f s  resolve %.0f s  post %.0f s  (their OBS: %s)' % (main_s, gap, res_s, post, J['inputs']['observed_split']))
print('per iteration: main %.5f  resolve %.5f  whole %.5f' % (main_s / it_main, res_s / it_res, cgc / float(it_main + it_res)))
GPU = main_s + res_s; CERT = gap + post; OTHER = raster - cj; FIXED = pre + OTHER + save; GFIX = pre + OTHER
REG_R = 2578.0 / 879.0
def arm(s=1.0, r=REG_R, m=1.0, reuse=False, mode='arm'):
    rp, rs = (r, r) if mode == 'arm' else (1.0, r)
    cold = GPU * m / s + CERT; prep = FIXED + (0 if reuse else cj)
    return prep + cold, rp * prep + rs * cold, cold, rs * cold, prep, rp * prep, rp * (GFIX + (0 if reuse else cj)) + 240.0, rp
def f0(n, k, **kw):
    S, D, cold, coldd, prep, prepd, g, rp = arm(**kw)
    once_s = 3 * cj if kw.get('reuse') else 0; once_d = 3 * cj * rp if kw.get('reuse') else 0
    lad = 19 * S + once_s
    if n == 1: return (2 * lad - once_s + 12 * k * D + once_d) / 3600
    if n == 'nosplit': return (lad + 12 * k * D + once_d) / 3600
    return (lad + math.ceil(12 / n) * k * D + once_d) / 3600
chk = []
def cmp(name, mine, theirs):
    ok = abs(round(mine, 1) - theirs) < 0.051
    chk.append(ok); print('%-58s mine %9.1f  theirs %9.1f  %s' % (name, mine, theirs, 'same' if ok else 'DIFF'))
b = J['baseline_F0']
cmp('F0 s1 one machine lo', f0(1, 4), b['lo']['one_machine_h']); cmp('F0 s1 one machine hi', f0(1, 5), b['hi']['one_machine_h'])
cmp('F0 s1 no-split-2 lo', f0('nosplit', 4), b['lo']['no_split_2_h']); cmp('F0 s1 split-2 lo', f0(2, 4), b['lo']['split_2_h'])
cmp('F0 s1 split-2 hi', f0(2, 5), b['hi']['split_2_h']); cmp('F0 s1 split-3 hi', f0(3, 5), b['hi']['split_3_h'])
def grid(s, r, m, reuse, mode):
    for g in J['grid']:
        k = g['knobs']
        if k['s'] == s and abs(k['r'] - round(r, 4)) < 1e-9 and k['m'] == m and k['reuse'] == reuse and k['r_mode'] == mode: return g
for (s, rm, m, reuse, mode, n, k, key) in [(1.5, 1, 1, False, 'arm', 2, 4, 'lo'), (2, 1, 1, False, 'arm', 2, 5, 'hi'), (2, 0.5, 1, False, 'arm', 2, 4, 'lo'),
                                           (1, 2, 1, False, 'arm', 2, 5, 'hi'), (2, 1, 1, True, 'arm', 2, 4, 'lo'), (1, 1, 1, True, 'arm', 2, 5, 'hi'),
                                           (2, 1, 1, True, 'arm', 3, 5, 'hi'), (1, 1, 2, False, 'arm', 2, 4, 'lo'), (2, 1, 0.5, False, 'arm', 2, 5, 'hi'),
                                           (2, 1, 1, False, 'solve', 2, 4, 'lo')]:
    g = grid(float(s), rm * REG_R, float(m), reuse, mode)
    cmp('F0 s%s r x%s m%s reuse %s %s split-%d %s' % (s, rm, m, reuse, mode, n, key), f0(n, k, s=float(s), r=rm * REG_R, m=float(m), reuse=reuse, mode=mode),
        g['F0'][key]['split_%d_h' % n])
# F1 (chain-counted) baseline: unit, sim, post, graph-only run
S, D, cold, coldd, prep, prepd, g, rp = arm()
unit_lo = (prepd + 2 * coldd) + g + 2 * D; unit_hi = unit_lo + coldd
f1 = J['baseline_F1']
cmp('F1 unit lo', unit_lo / 3600, f1['lo']['unit_h']); cmp('F1 unit hi', unit_hi / 3600, f1['hi']['unit_h'])
cmp('F1 split-2 sim lo', (19 * S + 6 * unit_lo) / 3600, f1['lo']['split_2']['sim_h']); cmp('F1 split-2 post (36 graph-only)', 36 * g / 3600, f1['lo']['split_2']['post_h'])
cmp('F1 graph-only run', g / 3600, f1['graph_only_run_h'])
S2, D2, c2, cd2, p2, pd2, g2, _ = arm(s=2.0)
u2lo = (pd2 + 2 * cd2) + g2 + 2 * D2
print('F1 s2 split-2: sim %.1f-%.1f h  + merge+verdict (24 graph-only) %.1f h  + reverify (12) %.1f h  => with merge+verdict %.1f-%.1f h ; hours left 456'
      % ((19 * S2 + 6 * u2lo) / 3600, (19 * S2 + 6 * (u2lo + cd2)) / 3600, 24 * g2 / 3600, 12 * g2 / 3600,
         (19 * S2 + 6 * u2lo + 24 * g2) / 3600, (19 * S2 + 6 * (u2lo + cd2) + 24 * g2) / 3600))
# C materials
spi = main_s / it_main
for v, th in zip((560000, 1500000, 3000000), J['c_materials']['maxiter_candidates']):
    cmp('maxiter %d one solve to cap (h)' % v, v * spi / 3600, th['one_solve_to_cap_h_at_measured_rate'])
# sensitivity stage
sec = 2 * (38 * S + 36 * D) + 1.728 * (38 * S + 36 * D) + 36 * D + 6 * 1.728 * D
cmp('sensitivity one machine s1 (h)', sec / 3600, J['sensitivity_stage_outside_table']['s1']['one_machine_h'])
# deadline arithmetic
dl = datetime(2026, 12, 1); ref = datetime(2026, 11, 12)
print('hours left', (dl - ref).total_seconds() / 3600, '| latest start for 406.4 h:', (dl - timedelta(hours=406.4)).strftime('%m-%d %H:%M'), '| for 339.6 h:', (dl - timedelta(hours=339.6)).strftime('%m-%d %H:%M'))
# decade slopes (two attempts)
a1_res, a2_res = 4.81885e-07, 1.0519e-12
print('iters/decade: first 30000 = %.0f ; 30000 -> end = %.0f ; resolve = %.0f ; to 1e-8 at that slope = %.0f iters' % (
    30000 / -math.log10(a1_res), (it_main - 30000) / math.log10(a1_res / a2_res), it_res / math.log10(a2_res / 1e-14),
    30000 + math.log10(a1_res / 1e-8) * (it_main - 30000) / math.log10(a1_res / a2_res)))
print('registered arm range s: %.0f - %.0f ; measured/registered %.2f - %.2f' % (879 * (1 - 704 / 879 + 704 / 879 * 6.05), 879 * (1 - 704 / 879 + 704 / 879 * 7.37),
      wall / (879 * (1 - 704 / 879 + 704 / 879 * 7.37)), wall / (879 * (1 - 704 / 879 + 704 / 879 * 6.05))))
print('ALL SAME' if all(chk) else 'SOME DIFF', len(chk), 'cells')
