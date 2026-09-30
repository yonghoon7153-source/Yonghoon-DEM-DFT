#!/usr/bin/env python3
"""Emit markdown tables (exact numbers) for the reasonableness report."""
import json

import os as _os, tempfile as _tf
HERE = _os.path.dirname(_os.path.abspath(__file__))
REPO = _os.path.abspath(_os.path.join(HERE, '..', '..', '..'))
SP = _os.environ.get('COV5_WORK') or _os.path.join(_tf.gettempdir(), 'cov5_work')   # 중간 산출 (리포 밖)
_os.makedirs(SP, exist_ok=True)
T = json.load(open(SP + '/cr_trends.json'))
C = json.load(open(SP + '/cr_checks.json'))
tr = T['trend']
FN = {'hz': 'Hertz-geom (수확기 = 웹앱)', 'we': '벽 제외 (수확기)', 'lp': 'legacy Physics v1', 'lr': 'legacy Physics rough', 'v2': 'physics v2 (후보)'}
PH = {'P': 'AM_P', 'S': 'AM_S', 'T': '전체'}
out = []


def f(x, d=3):
    return '—' if x is None or x != x else f'{x:+.{d}f}'


out.append('| 코호트 | 계열 | 칸 | n | 최소 · 중앙 · 최대 (%) | ρ(SE/고체) | ρ(SE wt%) | ρ(r_SE/r_AM) | 부분ρ_SE | 부분ρ_크기 | R² | raw z>4 | 잔차 z>4 |')
out.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for coh in ('LHS', 'lhsx'):
    for fam in ('hz', 'we', 'lp', 'lr', 'v2'):
        for ph in ('P', 'S', 'T'):
            t = tr.get(f'{coh}|{fam}|{ph}')
            if not t:
                continue
            q = t['q']
            r2 = t['R2']
            nfit = t.get('n_fit')
            raw = t['n_flag_raw'] if t['mad_raw'] and t['mad_raw'] > 0.01 else f"({t['n_flag_raw']}) MAD {t['mad_raw']:.4f}"
            out.append(f"| {coh} | {FN[fam]} | {PH[ph]} | {t['n']} | {q[0]:.3f} · {q[2]:.3f} · {q[4]:.3f} | {f(t['rho_se'])} | "
                       f"{f(t['rho_sewt'])} | {f(t['rho_ratio'])} | {f(t['prho_se'])} | {f(t['prho_ratio'])} | "
                       f"{('적합 불가 (비포화 ' + str(nfit) + ')') if r2 is None else (f'{r2:.3f}' + ('' if nfit is None else f' (n={nfit})'))} | {raw} | {t['n_flag_res'] if r2 is not None else '—'} |")
open(SP + '/cr_tab_trend.md', 'w').write('\n'.join(out) + '\n')

out = ['| 코호트 | 계열 | 칸 | 침대 n | = 100.000 | ≥ 99 | ≥ 95 | 고유값 수 (3 자리) | 25 · 75 백분위 (%) |', '|---|---|---|---|---|---|---|---|---|']
for coh in ('LHS', 'lhsx'):
    for fam in ('hz', 'we', 'lp', 'lr', 'v2'):
        for ph in ('P', 'S', 'T'):
            t = tr.get(f'{coh}|{fam}|{ph}')
            if not t:
                continue
            q = t['q']
            out.append(f"| {coh} | {FN[fam]} | {PH[ph]} | {t['n']} | {t['n100']} | {t['n99']} | {t['n95']} | {t['n_unique']} | {q[1]:.3f} · {q[3]:.3f} |")
open(SP + '/cr_tab_sat.md', 'w').write('\n'.join(out) + '\n')

# model coefficients for Hertz-type
out = ['| 코호트 | 계열 | 칸 | a | b (ln SE/고체) | c (ln r_SE/r_AM) | R² |', '|---|---|---|---|---|---|---|']
for coh in ('LHS', 'lhsx'):
    for fam in ('hz', 'we'):
        for ph in ('P', 'S', 'T'):
            t = tr[f'{coh}|{fam}|{ph}']
            b = t['beta']
            out.append(f"| {coh} | {FN[fam]} | {PH[ph]} | {b[0]:.3f} | {b[1]:.3f} | {b[2]:.3f} | {t['R2']:.3f} |")
open(SP + '/cr_tab_model.md', 'w').write('\n'.join(out) + '\n')

# ordering table
LBL = {'lp|wh': 'legacy Physics ≥ Hertz', 'lp|lr': 'legacy Physics ≥ rough', 'lp|v2': 'v2 ≥ legacy Physics',
       'hz|we': '벽 제외 ≥ Hertz', 'wh|v2': 'v2 ≥ Hertz', 'we|lp': 'legacy Physics ≥ 벽 제외', 'wh|lr': 'rough ≥ Hertz'}
out = ['| 순서 | 코호트 | 칸 | 비교 침대 n | 위반 | 최소 여유 (%p) | 중앙 여유 (%p) | 같음 (≤ 5e-4) |', '|---|---|---|---|---|---|---|---|']
for k, lab in LBL.items():
    for coh in ('LHS', 'lhsx'):
        for ph in ('P', 'S', 'T'):
            v = C['check2_order'][coh][f'{k}|{ph}']
            out.append(f"| {lab} | {coh} | {PH[ph]} | {v['n']} | {v['n_viol']} | {v['d_min']:.4f} | {v['d_median']:.3f} | {v['n_equal']} |")
open(SP + '/cr_tab_order.md', 'w').write('\n'.join(out) + '\n')
print('ok')
