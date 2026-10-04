#!/usr/bin/env python3
"""10-21 워크숍 덱 (한양대 DEM 파트) 그래프 — Origin 워크시트 CSV · LabTalk (.ogs) · 미리보기 PNG · 본문 수치.

    python3 docs/report_20261021/make_figs.py

- 최종 그래프는 **Origin** (랩 통일 · BML 표준).  글꼴만 사용자 지정 **Aptos** (BML 기본 Arial · Calibri 대신).
- origin/Gx.csv : 그래프 하나 = 워크북 하나 (1 줄 Long Name · 2 줄 Units · 3 줄부터 값 · 열 길이가 달라도 된다).
- origin/Gx.ogs : 워크북이 **활성**일 때 Script Window 에 붙여 실행 → 그래프 생성 + BML 서식.  GUI 마무리는 origin/GUIDE.md.
- previews/Gx.png : 덱 자리 잡기용 미리보기 (이 기계에 Aptos 가 없어 Liberation Sans) — Origin 결과로 바꿔 끼운다.
- summary.json : 슬라이드 본문 수치 (생성기 build_deck_v2.py 가 읽는다).
원자료 (읽기만): ps45 union · 배포 v1 (130 + 64) · Phase A 104 팔 · 믹서 10 런 판독 — 경로는 아래 코드.
"""
import csv
import glob
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D = ROOT / 'docs/data'
O, P = HERE / 'origin', HERE / 'previews'
O.mkdir(exist_ok=True)
P.mkdir(exist_ok=True)
S = {}


def fnum(s):
    try:
        v = float(s)
        return v if math.isfinite(v) else float('nan')
    except (TypeError, ValueError):
        return float('nan')


def wcsv(name, head, units, cols):
    """cols = 열 목록 (길이가 달라도 된다 — 짧은 열은 빈칸)."""
    n = max(len(c) for c in cols)
    with open(O / f'{name}.csv', 'w', newline='', encoding='utf-8-sig') as f:   # utf-8-sig = Origin · Excel 한글
        w = csv.writer(f)
        w.writerow(head)
        w.writerow(units)
        for i in range(n):
            row = []
            for c in cols:
                v = c[i] if i < len(c) else ''
                row.append('' if (isinstance(v, float) and not math.isfinite(v)) else v)
            w.writerow(row)


# ═════════════════════════════ 데이터 ═════════════════════════════
r45 = {r['P_S']: r for r in csv.DictReader(open(D / 'ps45_r45_union_20260929/r45_union_summary.tsv', encoding='utf-8'), delimiter='\t')}
PS = ['0:10', '3:7', '5:5', '7:3', '10:0']
g1x = [int(p.split(':')[0]) / 10 for p in PS]
g1u = [round(fnum(r45[p]['porosity_union_exact_pct']), 2) for p in PS]
g1s = [round(fnum(r45[p]['porosity_sphere_web_pct']), 2) for p in PS]
g1t = [round(fnum(r45[p]['thickness_um']), 1) for p in PS]
wcsv('G1', ['AM_P fraction', 'P:S', 'Porosity (union)', 'Porosity (sphere sum)', 'Thickness'], ['', '', '%', '%', 'µm'],
     [g1x, PS, g1u, g1s, g1t])
S['G1'] = {p: dict(union=u, sphere=s, thickness=t) for p, u, s, t in zip(PS, g1u, g1s, g1t)}


def rel(tag):
    return list(csv.DictReader(open(D / f'lhs_release_20261001/{tag}_release_20261001.csv', encoding='utf-8')))


L, X = rel('lhs'), rel('lhsx')
col = lambda rows, k: np.array([fnum(r.get(k)) for r in rows])
U, se, ps, dse, dp = (col(L, k) for k in ('porosity_union_exact_pct', 'se_of_solid_vol', 'ps_frac', 'd_se_um', 'd_am_p_um'))
ok = np.isfinite(U) & np.isfinite(se) & np.isfinite(ps) & np.isfinite(dse)
Xm = np.column_stack([np.ones_like(se), se, se ** 2, dse])
b, *_ = np.linalg.lstsq(Xm[ok], np.log(U[ok]), rcond=None)
res = np.log(U) - Xm @ b
S['G2_control'] = dict(model='ln(union %) ~ 1 + SE/solid + (SE/solid)^2 + d_SE (OLS)', n=int(ok.sum()),
                      r2=round(float(1 - np.var(res[ok]) / np.var(np.log(U[ok]))), 3))
g2x, g2l, g2n, g2r = [], [], [], []
for v in np.round(np.arange(0, 1.01, 0.1), 1):
    k = ok & (np.abs(ps - v) < 0.01)
    g2x.append(float(v)); g2l.append(f'{int(round(v * 10))}:{10 - int(round(v * 10))}'); g2n.append(int(k.sum()))
    g2r.append(round(float(np.expm1(np.median(res[k])) * 100), 1))   # 예측 대비 공극률 비 (%) — ln 잔차 × 100 이 아니다 (10-05 정정)
wcsv('G2', ['AM_P fraction', 'P:S', 'n', 'Porosity vs prediction', 'Denser than predicted', 'Looser than predicted'], ['', '', '', '%', '%', '%'],
     [g2x, g2l, g2n, g2r, [v if v < 0 else float('nan') for v in g2r], [v if v >= 0 else float('nan') for v in g2r]])
S['G2'] = list(zip(g2l, g2n, g2r))

#  ★ 10-05 정정: 130 설계점의 활물질 함량은 70–95 wt% **여섯 수준** (5 wt% 간격) 이라 SE 부피분율도 여섯 값 (11 · 21 · 30 · 37 · 44 · 51 %) 에 모인다.
#    옛 10 % 폭 구간 (20-30 등) 은 21 % · 30 % 두 수준을 한 칸에 합쳤다 → 활물질 함량 수준별 중앙값으로 바꾼다.
amL = col(L, 'am_pct')
LV = sorted({int(round(v)) for v in amL[ok]}, reverse=True)
bx, bl, bn, bm = [], [], [], []
for lv in LV:
    k = ok & (np.round(amL) == lv)
    bx.append(round(float(np.median(se[k]) * 100), 1)); bl.append(f'AM {lv}'); bn.append(int(k.sum())); bm.append(round(float(np.median(U[k])), 1))
wcsv('G3', ['SE fraction of solid', 'Porosity (union)', 'Level SE (median)', 'Level median', 'Level (AM wt %)', 'n'], ['vol %', '%', 'vol %', '%', '', ''],
     [[round(float(v) * 100, 2) for v in se[ok]], [round(float(v), 2) for v in U[ok]], bx, bm, bl, bn])
S['G3_levels'] = list(zip(bl, bn, bm, bx))
okp = ok & np.isfinite(dp)
PE = [(4.9, 7, '5-7'), (7, 9, '7-9'), (9, 11, '9-11'), (11, 13, '11-13'), (13, 15.1, '13-15')]
px, pl, pn, pm = [], [], [], []
for a, c, lab in PE:
    k = okp & (dp >= a) & (dp < c)
    px.append(round((a + c) / 2, 1)); pl.append(lab); pn.append(int(k.sum())); pm.append(round(float(np.median(U[k])), 1))
wcsv('G4', ['Large-AM diameter', 'Porosity (union)', 'Bin center', 'Bin median', 'Bin', 'n'], ['µm', '%', 'µm', '%', '', ''],
     [[round(float(v), 2) for v in dp[okp]], [round(float(v), 2) for v in U[okp]], px, pm, pl, pn])
S['G4_bins'] = list(zip(pl, pn, pm))
S['G4_excluded_mono_small'] = int((ok & ~np.isfinite(dp)).sum())

sl, tl, al, rl = (col(L, k) for k in ('se_of_solid_vol', 'tortuosity_SE_wall', 'ionic_active_pct', 'am_vulnerable_pct'))
sx, tx, ax_ = (col(X, k) for k in ('se_of_solid_vol', 'tortuosity_SE_wall', 'ionic_active_pct'))
span = np.isfinite(tl)
wcsv('G5a', ['SE fraction (130, spans)', 'Tortuosity wall (130)', 'SE fraction (64)', 'Tortuosity wall (64)',
             'SE fraction (130, no span)', 'Marker'], ['vol %', '', 'vol %', '', 'vol %', ''],
     [[round(v * 100, 2) for v in sl[span]], [round(v, 3) for v in tl[span]], [round(v * 100, 2) for v in sx],
      [round(v, 3) for v in tx], [round(v * 100, 2) for v in sl[~span]], [0.9] * int((~span).sum())])
wcsv('G5b', ['SE fraction (130)', 'AM isolated (130)', 'SE fraction (64)', 'AM isolated (64)'], ['vol %', '%', 'vol %', '%'],
     [[round(v * 100, 2) for v in sl], [round(100 - v, 2) for v in al], [round(v * 100, 2) for v in sx], [round(100 - v, 2) for v in ax_]])
S['G5'] = dict(n130=int(len(sl)), span130=int(span.sum()), nonspan130=int((~span).sum()),
               nonspan_se_max=round(float(sl[~span].max() * 100), 1), span_se_min=round(float(sl[span].min() * 100), 1),
               tau130=[round(float(tl[span].min()), 2), round(float(tl[span].max()), 2)],
               n64=int(len(sx)), span64=int(np.isfinite(tx).sum()), tau64=[round(float(np.nanmin(tx)), 2), round(float(np.nanmax(tx)), 2)],
               se64=[round(float(sx.min() * 100), 1), round(float(sx.max() * 100), 1)],
               iso64_max=round(float(np.nanmax(100 - ax_)), 2))
S['G5']['levels'] = []                                   # 활물질 함량 수준별 (G3 와 같은 여섯 수준)
for lv in LV:
    k = np.round(amL) == lv
    S['G5']['levels'].append(dict(level=f'AM {lv}', se_med=round(float(np.median(sl[k]) * 100), 1), n=int(k.sum()), span=int((k & span).sum()),
                                  tau_med=round(float(np.median(tl[k & span])), 2) if (k & span).any() else None,
                                  iso_med=round(float(np.median(100 - al[k])), 1), iso_max=round(float(np.max(100 - al[k])), 1),
                                  risk_med=round(float(np.median(rl[k])), 1)))
#  모든 설계점의 고립이 13 % 아래가 되는 가장 낮은 SE 수준 (그 위 수준도 전부) — 2-13 지침 ①
_lv_up = sorted(S['G5']['levels'], key=lambda d: d['se_med'])
_ok_from = [d for i, d in enumerate(_lv_up) if all(e['iso_max'] < 13 for e in _lv_up[i:])]
S['G5']['iso13_from'] = dict(se_med=_ok_from[0]['se_med'], level=_ok_from[0]['level']) if _ok_from else None

arms = [json.load(open(p)) for p in glob.glob(str(D / 'phase_a_104arms_20260921/verdict_dir_20260921/*.json'))]
prim = [a for a in arms if a.get('role') == 'primary']
VOX, WT = sorted({a['vox'] for a in prim}), sorted({a['vgcf_wt'] for a in prim})
mean6 = {(v, w): float(np.mean([a['sigma_e'] * 1000 for a in prim if a['vox'] == v and a['vgcf_wt'] == w])) for v in VOX for w in WT}
spread6 = max((max(a['sigma_e'] for a in prim if a['vox'] == v and a['vgcf_wt'] == w) /
               min(a['sigma_e'] for a in prim if a['vox'] == v and a['vgcf_wt'] == w) - 1) * 100 for v in VOX for w in WT)
wcsv('G6', ['VGCF content'] + [f'sigma_e (voxel {v:.2f} um)' for v in VOX], ['wt %'] + ['mS/cm'] * len(VOX),
     [WT] + [[round(mean6[(v, w)], 3) for w in WT] for v in VOX])
S['G6'] = dict(n_primary=len(prim), n_all=len(arms), vox=VOX, wt=WT, mean={f'{v}|{w}': round(mean6[(v, w)], 2) for v in VOX for w in WT},
               max_origin_spread_pct=round(spread6, 2))

vj = json.load(open(D / 'mixer_final10_20260930/verdict_20260930.json'))
lab7, m7, e7 = [], [], []
for cond, short in (('L0', 'L0'), ('LA', 'LA'), ('LB1', 'LB1'), ('LB2', 'LB2'), ('LB3', 'LB3'), ('LC', 'LC')):
    keys = sorted(k for k in vj['runs'] if k.startswith(cond + '_') and k.endswith('|16x4'))
    for i, k in enumerate(keys, 1):
        lab7.append(short if len(keys) == 1 else f'{short} s{i}')
        m7.append(round(vj['runs'][k]['M'], 4)); e7.append(round(vj['runs'][k]['sd'], 4))
wcsv('G7', ['Run', 'Mixing index M', 'Within-run SD'], ['', '', ''], [lab7, m7, e7])
S['G7'] = dict(runs=list(zip(lab7, m7, e7)), main=vj['main'])
json.dump(S, open(HERE / 'summary.json', 'w'), ensure_ascii=False, indent=1)

# ═════════════════════════════ 미리보기 (BML 모양) ═════════════════════════════
GRAY, RED, SKY, GREEN, ORANGE = '#404040', '#F14040', '#4FBDFF', '#52B788', '#F4A261'
plt.rcParams.update({'font.family': 'Liberation Sans', 'font.size': 11, 'axes.edgecolor': GRAY, 'axes.labelcolor': GRAY,
                     'xtick.color': GRAY, 'ytick.color': GRAY, 'axes.linewidth': 1.0, 'xtick.direction': 'out',
                     'ytick.direction': 'out', 'xtick.major.size': 5, 'ytick.major.size': 5, 'xtick.minor.size': 2.5,
                     'ytick.minor.size': 2.5, 'xtick.minor.visible': True, 'ytick.minor.visible': True,
                     'axes.labelsize': 12.5, 'legend.fontsize': 9.5, 'legend.frameon': False})
W, H = 4.3, 3.35


def fig_():
    fig, ax = plt.subplots(figsize=(W, H))
    ax.tick_params(top=False, right=False, which='both')
    return fig, ax


def save(fig, name):
    fig.tight_layout(pad=0.4)
    fig.savefig(P / f'{name}.png', dpi=300)
    plt.close(fig)


fig, ax = fig_()
ax.plot(g1x, g1u, '-o', color=RED, lw=2, ms=7)
for xi, ui in zip(g1x, g1u):
    ax.annotate(f'{ui:.1f}', (xi, ui), textcoords='offset points', xytext=(-12, 6), ha='center', fontsize=9.5, color=RED)
ax.set_xlabel('Large : small AM (mass)'); ax.set_ylabel('Porosity, union (%)', color=RED)
ax.set_xticks(g1x, PS); ax.set_ylim(15, 22); ax.set_xlim(-0.08, 1.08); ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
a2 = ax.twinx(); a2.plot(g1x, g1t, '--s', color=SKY, lw=1.6, ms=6); a2.set_ylabel('Thickness (µm)', color=SKY)
a2.set_ylim(108, 120); a2.tick_params(colors=SKY, direction='out', which='both'); a2.spines['right'].set_color(SKY)
save(fig, 'G1')

fig, ax = fig_()
ax.bar(g2x, g2r, width=0.07, color=[SKY if v < 0 else ORANGE for v in g2r], edgecolor=GRAY, lw=0.5)
ax.axhline(0, color=GRAY, lw=0.8)
for xi, yi in zip(g2x, g2r):
    ax.annotate(f'{yi:+.0f}', (xi, yi), textcoords='offset points', xytext=(0, 3 if yi >= 0 else -11), ha='center', fontsize=8.5, color=GRAY)
ax.set_xlabel('Large-AM fraction in AM'); ax.set_ylabel('Porosity vs prediction (%)'); ax.set_xlim(-0.08, 1.08); ax.set_ylim(-22, 17)
save(fig, 'G2')

for name, xv, xl, bxv, bmv, c, xlim, mlab in (('G3', se[ok] * 100, 'SE fraction of solid (vol %)', bx, bm, RED, (5, 56), 'AM-level median'),
                                               ('G4', dp[okp], 'Large-AM diameter, D$_P$ (µm)', px, pm, SKY, (4, 16), 'Bin median')):
    yv = U[ok] if name == 'G3' else U[okp]
    fig, ax = fig_()
    ax.plot(xv, yv, 'o', ms=4.5, mfc='none', mec='#9AA0A8', mew=0.8, label='130 design points')
    ax.plot(bxv, bmv, '-o', color=c, lw=2, ms=7, label=mlab)
    ax.set_xlabel(xl); ax.set_ylabel('Porosity, union (%)'); ax.legend(loc='upper right'); ax.set_xlim(*xlim); ax.set_ylim(0, 32)
    save(fig, name)

fig, ax = fig_()
ax.axvspan(5, S['G5']['nonspan_se_max'], color='#EEF2F8', zorder=0)
ax.plot(sl[span] * 100, tl[span], 'o', ms=5, color=SKY, mec=GRAY, mew=0.4, label='130 set')
ax.plot(sx * 100, tx, '^', ms=5, color=ORANGE, mec=GRAY, mew=0.4, label='64 SE-rich set')
ax.plot(sl[~span] * 100, [0.9] * int((~span).sum()), 'x', color=RED, ms=6, mew=1.4, label=f'No SE path ({int((~span).sum())})')
ax.set_xlabel('SE fraction of solid (vol %)'); ax.set_ylabel('Tortuosity, wall (geometric)'); ax.set_xlim(5, 90); ax.set_ylim(0.7, 4.5)
ax.legend(loc='upper right')
save(fig, 'G5a')
fig, ax = fig_()
ax.axvspan(5, S['G5']['nonspan_se_max'], color='#EEF2F8', zorder=0)
ax.plot(sl * 100, 100 - al, 'o', ms=5, color=SKY, mec=GRAY, mew=0.4, label='130 set')
ax.plot(sx * 100, 100 - ax_, '^', ms=5, color=ORANGE, mec=GRAY, mew=0.4, label='64 SE-rich set')
ax.set_xlabel('SE fraction of solid (vol %)'); ax.set_ylabel('Ionically isolated AM (%)'); ax.set_xlim(5, 90); ax.set_ylim(-5, 105)
ax.legend(loc='upper right')
save(fig, 'G5b')

fig, ax = fig_()
for v, c, m in zip(VOX, (RED, SKY, GREEN), ('o', 's', '^')):
    ax.plot(WT, [mean6[(v, w)] for w in WT], '-' + m, color=c, lw=1.8, ms=6.5, label=f'voxel {v:.2f} µm')
ax.set_yscale('log'); ax.set_xlabel('VGCF content (wt %)'); ax.set_ylabel('σ$_e$ (mS cm$^{-1}$)'); ax.set_xticks(WT)
ax.set_xlim(0.7, 4.3); ax.legend(loc='lower right'); ax.tick_params(axis='x', which='minor', bottom=False)
save(fig, 'G6')

fig, ax = fig_()
cols7 = [GRAY if l.startswith('L0') else SKY if l.startswith('LA') else RED if l.startswith('LC') else '#B8C4D6' for l in lab7]
ax.bar(range(len(m7)), m7, yerr=e7, color=cols7, edgecolor=GRAY, lw=0.5, capsize=2.5, error_kw=dict(ecolor=GRAY, lw=0.8))
ax.set_xticks(range(len(m7)), [l.replace(' ', '\n') for l in lab7], fontsize=8.5); ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
ax.set_ylim(0.85, 1.05); ax.set_ylabel('Mixing index, M'); ax.axhline(1.0, color=GRAY, lw=0.6, ls=':')
mn = vj['main']['16x4']
ax.text(0.03, 0.96, f"Δ (LC − LA) = {mn['Delta']:+.3f} ± {mn['SE']:.3f}", transform=ax.transAxes, fontsize=9.5, color=GRAY, va='top')
save(fig, 'G7')

# ═════════════════════════════ Origin LabTalk (.ogs) ═════════════════════════════
AX = '''
// ── BML 축 서식 (글꼴 = Aptos · 사용자 지정) ──
layer.unit = 3; layer.width = {w}; layer.height = {h};
layer.x.color = color(64,64,64); layer.x.thickness = 1; layer.x.ticks = 10;
layer.x.ticklength = 6; layer.x.tickthickness = 1; layer.x.mticklength = 3; layer.x.mtickthickness = 1;
layer.x.label.font = font(Aptos); layer.x.label.pt = 28; layer.x.label.color = color(64,64,64);
layer.y.color = color(64,64,64); layer.y.thickness = 1; layer.y.ticks = 10;
layer.y.ticklength = 6; layer.y.tickthickness = 1; layer.y.mticklength = 3; layer.y.mtickthickness = 1;
layer.y.label.font = font(Aptos); layer.y.label.pt = 28; layer.y.label.color = color(64,64,64);
layer.x2.showAxes = 3; layer.x2.color = color(64,64,64); layer.x2.thickness = 1; layer.x2.ticks = 0; layer.x2.showLabels = 0;
{y2}page.margincontrol = 1;
label -xb {xt};
label -yl {yt};
'''
Y2_LINE = 'layer.y2.showAxes = 3; layer.y2.color = color(64,64,64); layer.y2.thickness = 1; layer.y2.ticks = 0; layer.y2.showLabels = 0;\n'
OGS = {
 'G1': ('사양 5 조성 — 공극률 (union) · 두께 vs 대 : 소 (DoubleY)',
        'plotxy iy:=[%(bk$)]1!(1,3) plot:=202 ogl:=<new template:=DoubleY>;\n'
        'set %C -c color(241,64,64); set %C -w 1000; set %C -k 2; set %C -z 10; set %C -d 0;\n'
        'plotxy iy:=[%(bk$)]1!(1,5) plot:=202 ogl:=2!;\n'
        'set %C -c color(79,189,255); set %C -w 800; set %C -k 1; set %C -z 9; set %C -d 1;\n'
        'page.active = 1;\n',
        dict(w=10, h=8, y2='', xt='Large : small AM (mass)', yt='Porosity, union (%)'),
        'page.active = 2;\nlayer2.y.color = color(79,189,255); layer2.y.thickness = 1; layer2.y.ticks = 10;\n'
        'layer2.y.label.font = font(Aptos); layer2.y.label.pt = 28; layer2.y.label.color = color(79,189,255);\nlabel -yr Thickness (\\g(m)m);\n'),
 'G2': ('130 설계점 — 함량 · 입경 보정 뒤 공극률 편차 vs 대입자 몫 (열 두 개 = 치밀 · 성김)',
        'plotxy iy:=[%(bk$)]1!(1,5) plot:=100 ogl:=<new>;\nset %C -c color(79,189,255);\n'
        'plotxy iy:=[%(bk$)]1!(1,6) plot:=100 ogl:=1!;\nset %C -c color(244,162,97);\n',
        dict(w=10, h=8, y2=Y2_LINE, xt='Large-AM fraction in AM', yt='Porosity vs prediction (%)'), ''),
 'G3': ('130 설계점 — 공극률 vs 고체 중 SE 부피분율 (점 + 활물질 함량 수준별 중앙값)',
        'plotxy iy:=[%(bk$)]1!(1,2) plot:=201 ogl:=<new>;\nset %C -c color(154,160,168); set %C -k 2; set %C -z 7;\n'
        'plotxy iy:=[%(bk$)]1!(3,4) plot:=202 ogl:=1!;\nset %C -c color(241,64,64); set %C -w 1000; set %C -k 2; set %C -z 10;\n',
        dict(w=10, h=8, y2=Y2_LINE, xt='SE fraction of solid (vol %)', yt='Porosity, union (%)'), ''),
 'G4': ('130 설계점 — 공극률 vs 대입자 지름 (점 + 구간 중앙값)',
        'plotxy iy:=[%(bk$)]1!(1,2) plot:=201 ogl:=<new>;\nset %C -c color(154,160,168); set %C -k 2; set %C -z 7;\n'
        'plotxy iy:=[%(bk$)]1!(3,4) plot:=202 ogl:=1!;\nset %C -c color(79,189,255); set %C -w 1000; set %C -k 2; set %C -z 10;\n',
        dict(w=10, h=8, y2=Y2_LINE, xt='Large-AM diameter, D\\-(P) (\\g(m)m)', yt='Porosity, union (%)'), ''),
 'G5a': ('이온 경로 — 벽 기준 굴곡도 vs SE 부피분율 (130 관통 · 64 · 비관통 표시)',
         'plotxy iy:=[%(bk$)]1!(1,2) plot:=201 ogl:=<new>;\nset %C -c color(79,189,255); set %C -k 2; set %C -z 9;\n'
         'plotxy iy:=[%(bk$)]1!(3,4) plot:=201 ogl:=1!;\nset %C -c color(244,162,97); set %C -k 3; set %C -z 9;\n'
         'plotxy iy:=[%(bk$)]1!(5,6) plot:=201 ogl:=1!;\nset %C -c color(241,64,64); set %C -k 9; set %C -z 10;\n',
         dict(w=10, h=8, y2=Y2_LINE, xt='SE fraction of solid (vol %)', yt='Tortuosity, wall (geometric)'), ''),
 'G5b': ('이온 경로 — 경로 기준 고립 AM vs SE 부피분율 (130 · 64)',
         'plotxy iy:=[%(bk$)]1!(1,2) plot:=201 ogl:=<new>;\nset %C -c color(79,189,255); set %C -k 2; set %C -z 9;\n'
         'plotxy iy:=[%(bk$)]1!(3,4) plot:=201 ogl:=1!;\nset %C -c color(244,162,97); set %C -k 3; set %C -z 9;\n',
         dict(w=10, h=8, y2=Y2_LINE, xt='SE fraction of solid (vol %)', yt='Ionically isolated AM (%)'), ''),
 'G6': ('Phase A — σ_e vs VGCF 함량 (격자 셋 · 원점 8 평균 · 로그 Y)',
        'plotxy iy:=[%(bk$)]1!(1,2:4) plot:=202 ogl:=<new>;\n'
        'range r1 = 1!1; set r1 -c color(241,64,64); set r1 -k 2;\nrange r2 = 1!2; set r2 -c color(79,189,255); set r2 -k 1;\n'
        'range r3 = 1!3; set r3 -c color(82,183,136); set r3 -k 3;\nlayer.y.type = 2;\n',
        dict(w=10, h=8, y2=Y2_LINE, xt='VGCF content (wt %)', yt='\\g(s)\\-(e) (mS cm\\+(-1))'), ''),
 'G7': ('건식 믹싱 — 8 회전 뒤 혼합지수 M (16×16×4 칸 · 런내부 SD 오차 막대)',
        'wks.col1.type = 4; wks.col3.type = 3;   // A = X (런 이름) · C = Y 오차 (런내부 SD)\n'
        'plotxy iy:=[%(bk$)]1!(1,2,3) plot:=100 ogl:=<new>;\nset %C -c color(79,189,255);\n',
        dict(w=12, h=8, y2=Y2_LINE, xt=' ', yt='Mixing index, M'), ''),
}
for g, (title, plot, ax_kw, extra) in OGS.items():
    txt = (f'// {g}.ogs — {title}\n// 사용: {g}.csv 를 가져온 워크북을 활성으로 두고 Script Window 에 붙여 넣기 → Enter.\n'
           f'// 결과: 새 그래프 + BML 서식 (바깥 틱 · 위/오른쪽 축선 · #404040 · 틱 라벨 Aptos 28 pt).  축 제목 글꼴 · 범례는 GUIDE.md 의 GUI 단계.\n'
           'string bk$ = %H;\n' + plot + AX.format(**ax_kw) + extra)
    (O / f'{g}.ogs').write_text(txt, encoding='utf-8')
print(json.dumps({k: S[k] for k in ('G1', 'G2_control', 'G3_levels', 'G4_bins', 'G5')}, ensure_ascii=False)[:2500])
print('G6', S['G6']['max_origin_spread_pct'], '| G7', S['G7']['runs'])
