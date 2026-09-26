#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""σ closure 3×3 그림 — SDCP 원고 SI 그림 (신설): σ_NCM × σ_SDCP 9 격자점의 DBE/SBE σ_e 비 (원장 `CL-70`).

    python3 scripts/plot_sigma_closure_3x3.py              # → docs/figures/sigma_closure_3x3.{svg,png,csv} + _origin.csv
    python3 scripts/plot_sigma_closure_3x3.py --selftest

★ 값은 **원장 `docs/reviews/claims.json` 의 `CL-70` `measured.value` 에서 읽는다** — 여기에 숫자를 다시 적지 않는다.
  읽은 표는 스스로 검산한다: 행별 상대산포 % 로 만든 R̄ − 3·SD 가 원장에 함께 적힌 R̄ − 3·SD 와 맞아야 한다
  (산포 줄의 행·열 순서를 잘못 읽으면 여기서 멈춘다).
⚠ 등록된 한정어 (사전등록 `docs/reviews/sigma_closure_sweep_prereg_20260902.md` · 원장 CL-70 — 캡션에 그대로):
  격자점 9 (등록 25) · 막대 = **한 침대쌍의 origin 8 위상 산포 × 3** (표준오차가 아니다) ·
  격자점 사이를 **잇지 않는다** (보간 없음) · 절대값은 공유 침대쌍의 것.
⚠ 문헌 NCM811 값 (Wang 2018, 4.1 × 10⁻³ S cm⁻¹) 은 **축에 그리지 않는다** — 격자점 사이 값을 읽게 만든다 (보간 금지).
  비교는 표 S2 각주 ᵇ 의 문장으로만 한다.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, '..', 'docs', 'reviews', 'claims.json')
CLAIM = 'CL-70'
YLABEL = r'$\sigma_\mathrm{e}$(DBE) / $\sigma_\mathrm{e}$(SBE)'
TOL = 2e-4          # 원장의 R̄ · R̄−3SD 는 소수 4 자리, 산포 % 는 유효 3 자리 — 반올림 합이 이 안에 든다


def ledger_value(path=LEDGER):
    d = json.load(open(path, encoding='utf-8'))
    for c in d['claims']:
        if c.get('id') == CLAIM:
            return c['measured']['value']
    raise SystemExit(f'{path}: {CLAIM} 이 없다')


def parse(value):
    """원장 문자열 → 격자 dict.  9 칸 · 검산이 맞지 않으면 SystemExit."""
    lines = value.split('\n')
    head = next((ln for ln in lines if 'σ_SDCP' in ln), None)
    if head is None:
        raise SystemExit(f'{CLAIM}: σ_SDCP 머리줄이 없다')
    cols = [float(x) for x in re.findall(r'\(([\d.eE+-]+)\)', head)]
    col_lab = re.findall(r'(\S+)\s*\([\d.eE+-]+\)', head)
    rows, row_lab, cells = [], [], []
    for ln in lines:
        m = re.match(r'^(\S+)\s*\(([\d.eE+-]+)\)\s+(.*)$', ln)
        if not m or 'σ_SDCP' in ln:
            continue
        pairs = re.findall(r'([\d.]+)\s*→\s*([\d.]+)', m.group(3))
        if len(pairs) != len(cols):
            continue
        row_lab.append(m.group(1)); rows.append(float(m.group(2)))
        cells.append([(float(a), float(b)) for a, b in pairs])
    ms = re.search(r'상대산포 %:\s*([^\n]+)', value)
    if not ms:
        raise SystemExit(f'{CLAIM}: 상대산포 줄이 없다')
    rel = [[float(x) for x in grp.split('/')] for grp in ms.group(1).split('·')]
    if len(cols) != 3 or len(rows) != 3 or any(len(r) != 3 for r in rel) or len(rel) != 3:
        raise SystemExit(f'{CLAIM}: 3×3 이 아니다 (열 {len(cols)} · 행 {len(rows)} · 산포 {[len(r) for r in rel]})')
    out = []
    for i, s_ncm in enumerate(rows):
        for j, s_sdcp in enumerate(cols):
            r, r3 = cells[i][j]
            sd = r * rel[i][j] / 100.0
            if abs((r - 3 * sd) - r3) > TOL:
                raise SystemExit(f'{CLAIM}: 검산 실패 ({row_lab[i]}, {col_lab[j]}) — R̄ {r} · 산포 {rel[i][j]} % → '
                                 f'R̄−3SD {r - 3 * sd:.5f} ≠ 원장 {r3} (산포 줄 순서를 잘못 읽었나)')
            out.append(dict(sigma_ncm=s_ncm, sigma_sdcp=s_sdcp, R=r, R_m3sd=r3, rel_pct=rel[i][j], sd=sd,
                            used=(row_lab[i] == '생산' and col_lab[j] == '생산')))
    if sum(c['used'] for c in out) != 1:
        raise SystemExit(f'{CLAIM}: 생산점이 정확히 하나가 아니다')
    return out


def write_csv(path, cells):
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write('sigma_NCM_S_cm,sigma_SDCP_S_cm,R_mean,R_minus_3SD,rel_spread_pct,SD,value_used\n')
        for c in cells:
            fh.write(f"{c['sigma_ncm']:g},{c['sigma_sdcp']:g},{c['R']:.4f},{c['R_m3sd']:.4f},"
                     f"{c['rel_pct']:g},{c['sd']:.6f},{int(c['used'])}\n")
    ncm = sorted({c['sigma_ncm'] for c in cells}); sd_ = sorted({c['sigma_sdcp'] for c in cells})
    with open(path.replace('.csv', '_origin.csv'), 'w', encoding='utf-8') as fh:
        #  Origin wide — 행 = σ_NCM, 열 = σ_SDCP 의 R̄ (⚠ 주석줄 없음)
        fh.write('sigma_NCM (S cm-1),' + ','.join(f'R at sigma_SDCP {s:g} S cm-1' for s in sd_) + '\n')
        for n in ncm:
            fh.write(f'{n:g},' + ','.join(f"{c['R']:.4f}" for s in sd_ for c in cells
                                          if c['sigma_ncm'] == n and c['sigma_sdcp'] == s) + '\n')


def _sci(v):
    if v >= 1000:
        e = len(str(int(v))) - 1
        return rf'{v / 10 ** e:g}$\times$10$^{{{e}}}$'
    if v < 0.05:
        s = f'{v:.1e}'; m, e = s.split('e')
        return rf'{m}$\times$10$^{{{int(e)}}}$'
    return f'{v:.2f}' if v < 1 else f'{v:g}'


def plot(cells, out_base):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams['svg.hashsalt'] = 'sigma_closure_3x3'      # SVG 안 id 를 고정 — 다시 돌려도 같은 파일
    ncm = sorted({c['sigma_ncm'] for c in cells}); sdc = sorted({c['sigma_sdcp'] for c in cells})
    at = {(c['sigma_ncm'], c['sigma_sdcp']): c for c in cells}
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.8, 2.55), dpi=300, gridspec_kw={'width_ratios': [1, 1.3]})

    #  (a) 격자 그대로 — 9 칸의 R̄ (칸 사이 값은 없다)
    grid = [[at[(n, s)]['R'] for s in sdc] for n in ncm]
    im = ax1.imshow(grid, cmap='Blues', vmin=1.0, vmax=1.4, aspect='auto')
    for i, n in enumerate(ncm):
        for j, s in enumerate(sdc):
            c = at[(n, s)]
            ax1.text(j, i, f"{c['R']:.3f}", ha='center', va='center', fontsize=8,
                     color='white' if c['R'] > 1.25 else '#11161c', fontweight='bold' if c['used'] else 'normal')
            if c['used']:
                ax1.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, lw=1.4, ec='#11161c'))
    ax1.set_xticks(range(3)); ax1.set_xticklabels([_sci(s) for s in sdc], fontsize=8)
    ax1.set_yticks(range(3)); ax1.set_yticklabels([_sci(n) for n in ncm], fontsize=8)
    ax1.set_xlabel(r'$\sigma_\mathrm{SDCP}$ (S cm$^{-1}$)', fontsize=9)
    ax1.set_ylabel(r'$\sigma_\mathrm{NCM}$ (S cm$^{-1}$)', fontsize=9)
    cb = fig.colorbar(im, ax=ax1, fraction=0.05, pad=0.03)
    cb.ax.tick_params(labelsize=7.5); cb.set_label(YLABEL, fontsize=8)

    #  (b) σ_NCM 축 — 점만 (잇지 않는다), 막대 = ±3·SD (한 침대쌍의 origin 8 위상 산포, 표준오차 아님)
    style = {sdc[0]: ('o', '#9aa3ad'), sdc[1]: ('s', '#3b6fb6'), sdc[2]: ('^', '#c0504d')}
    offs = {sdc[0]: 0.84, sdc[1]: 1.0, sdc[2]: 1.19}
    for s in sdc:
        mk, col = style[s]
        xs = [n * offs[s] for n in ncm]; ys = [at[(n, s)]['R'] for n in ncm]
        es = [3 * at[(n, s)]['sd'] for n in ncm]
        lab = _sci(s) + (' (used)' if any(at[(n, s)]['used'] for n in ncm) else '')
        ax2.errorbar(xs, ys, yerr=es, fmt=mk, ms=4.2, color=col, mec=col, capsize=2, lw=0.8, label=lab)
    u = next(c for c in cells if c['used'])
    ax2.plot([u['sigma_ncm']], [u['R']], marker='s', ms=7.5, mfc='none', mec='#11161c', mew=1.1, ls='none')
    ax2.axhline(1.0, color='#5a6470', lw=0.8)
    ax2.axhline(1.01, color='#5a6470', lw=0.8, ls='--')
    ax2.text(ncm[0] * 0.62, 1.012, r'$\bar R - 3\,$SD threshold 1.01', fontsize=6.5, color='#5a6470', va='bottom')
    ax2.set_xscale('log')
    ax2.set_xticks(ncm); ax2.set_xticklabels([_sci(n) for n in ncm], fontsize=8)
    ax2.minorticks_off()
    ax2.set_xlim(ncm[0] * 0.45, ncm[-1] * 2.2)
    ax2.set_ylim(0.98, 1.42)
    ax2.set_xlabel(r'$\sigma_\mathrm{NCM}$ (S cm$^{-1}$)', fontsize=9)
    ax2.set_ylabel(YLABEL, fontsize=9)
    ax2.tick_params(labelsize=8)
    for sp in ('top', 'right'):
        ax2.spines[sp].set_visible(False)
    ax2.legend(title=r'$\sigma_\mathrm{SDCP}$ (S cm$^{-1}$)', fontsize=7, title_fontsize=7, frameon=False,
               loc='upper right', handletextpad=0.3)
    for ax, t in ((ax1, '(a)'), (ax2, '(b)')):
        ax.text(-0.02, 1.04, t, transform=ax.transAxes, fontsize=9, fontweight='bold', ha='right', va='bottom')
    fig.tight_layout()
    fig.savefig(f'{out_base}.svg', bbox_inches='tight', metadata={'Date': None})   # 날짜 없이 — 다시 돌려도 같은 파일
    fig.savefig(f'{out_base}.png', bbox_inches='tight')
    plt.close(fig)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--ledger', default=LEDGER)
    ap.add_argument('--out', default=os.path.join('docs', 'figures', 'sigma_closure_3x3'))
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    cells = parse(ledger_value(a.ledger))
    os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
    write_csv(a.out + '.csv', cells)
    plot(cells, a.out)
    for c in cells:
        print(f"  σ_NCM {c['sigma_ncm']:<8g} σ_SDCP {c['sigma_sdcp']:<7g} R̄ {c['R']:.4f}  R̄−3SD {c['R_m3sd']:.4f}"
              + ('   ← 생산점' if c['used'] else ''))
    print(f"\n최소 R̄−3SD {min(c['R_m3sd'] for c in cells):.4f} (문턱 1.01) · 검산 9/9 통과")
    print(f'산출: {a.out}.svg · .png · .csv · _origin.csv')
    return 0


def selftest():
    import tempfile
    ok = True

    def chk(label, cond):
        nonlocal ok
        print(('  PASS  ' if cond else '  FAIL  ') + label)
        ok = ok and bool(cond)

    v = ledger_value()
    cells = parse(v)
    chk('원장 CL-70 에서 9 칸을 읽는다', len(cells) == 9)
    u = [c for c in cells if c['used']]
    chk('생산점 = (σ_NCM 0.01, σ_SDCP 250) 하나', len(u) == 1 and u[0]['sigma_ncm'] == 0.01 and u[0]['sigma_sdcp'] == 250)
    chk('모든 칸이 등록 문턱 1.01 위 (원장 판정 DIRECTION-ROBUST 와 같다)', all(c['R_m3sd'] > 1.01 for c in cells))

    #  ★★ 음성 대조 1 — 산포 줄을 열 우선으로 읽으면 (행·열 뒤바뀜) 검산이 거부한다
    m = re.search(r'상대산포 %:\s*([^\n]+)', v)
    g = [grp.split('/') for grp in m.group(1).split('·')]
    swapped = ' · '.join(' / '.join(g[r][c].strip() for r in range(3)) for c in range(3))
    try:
        parse(v.replace(m.group(1), swapped)); chk('★★ 산포 행·열 뒤바뀜은 거부', False)
    except SystemExit as ex:
        chk('★★ 산포 행·열 뒤바뀜은 거부', '검산 실패' in str(ex))
    #  음성 대조 2 — 한 행이 빠지면 거부
    drop = '\n'.join(ln for ln in v.split('\n') if not ln.startswith('×30'))
    try:
        parse(drop); chk('행이 빠지면 거부', False)
    except SystemExit as ex:
        chk('행이 빠지면 거부', '3×3 이 아니다' in str(ex))
    #  음성 대조 3 — 원장 값 하나가 바뀌면 (R̄ 만 고침) 검산이 거부
    try:
        parse(v.replace('1.3078 → 1.3047', '1.3178 → 1.3047')); chk('R̄ 만 바뀐 원장은 거부', False)
    except SystemExit as ex:
        chk('R̄ 만 바뀐 원장은 거부', '검산 실패' in str(ex))

    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, 'f.csv'); write_csv(p, cells)
        rows = open(p, encoding='utf-8').read().strip().split('\n')
        chk('CSV = 머리 + 9 칸', len(rows) == 10 and rows[0].startswith('sigma_NCM_S_cm,'))
        ow = open(p.replace('.csv', '_origin.csv'), encoding='utf-8').read().strip().split('\n')
        chk('Origin CSV 는 주석줄 없이 wide (3 행 × 3 열)', len(ow) == 4 and not ow[0].startswith('#')
            and all(len(r.split(',')) == 4 for r in ow))
        try:
            plot(cells, os.path.join(td, 'f'))
            chk('SVG·PNG 를 낸다', all(os.path.exists(os.path.join(td, 'f.' + e)) for e in ('svg', 'png')))
        except Exception as ex:                                    # noqa: BLE001
            chk(f'SVG·PNG 를 낸다 ({ex})', False)

    print('\n✓ plot_sigma_closure_3x3 selftest PASS' if ok else '\n✗ plot_sigma_closure_3x3 selftest FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
