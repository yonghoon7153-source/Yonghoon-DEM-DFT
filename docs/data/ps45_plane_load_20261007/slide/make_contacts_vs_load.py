"""접촉 수 몫 ↔ σ_zz 기여 (조성마다 100 % 막대 한 쌍) — 값 = ps45_v2/plane_load.json 그대로 (contact_count_share_group_pct = 침대 전체 입자–입자 접촉 수 몫 ·
contribution_sigma_zz_pct = 21 수평 단면 평균 σ_zz 몫).  색 = 그림 1 과 같음 (AM–AM 검정 · AM–SE 회색 · SE–SE 주황).
다시 만들기: python3 make_contacts_vs_load.py <ps45_v2/plane_load.json> <출력 폴더>"""
import json, sys, csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

src, out = sys.argv[1], sys.argv[2]
d = json.load(open(src, encoding='utf-8'))
CS = ['0:10', '3:7', '5:5', '7:3', '10:0']; G = ['AM–AM', 'AM–SE', 'SE–SE']
COL = {'AM–AM': '#000000', 'AM–SE': '#7f7f7f', 'SE–SE': '#ed7d31'}
cnt = {cs: d['cases'][cs]['contact_count_share_group_pct'] for cs in CS}
ld = {cs: d['cases'][cs]['contribution_sigma_zz_pct'] for cs in CS}
with open(f'{out}/contacts_vs_sigma_zz_share.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['PC:SC'] + [f'Contacts {g}' for g in G] + [f'σzz {g}' for g in G])
    w.writerow(['wt%'] + ['%'] * 6)
    w.writerow(['조성'] + ['접촉 수 몫 (침대 전체 입자–입자 접촉)'] * 3 + ['Contribution to σ_zz (21 수평 단면 평균)'] * 3)
    for cs in CS:
        w.writerow([cs] + [f'{cnt[cs][g]:.4f}' for g in G] + [f'{ld[cs][g]:.4f}' for g in G])
plt.rcParams.update({'font.family': 'Liberation Sans', 'font.size': 9, 'axes.linewidth': 1.0,
                     'xtick.direction': 'in', 'ytick.direction': 'in', 'ytick.right': True, 'mathtext.default': 'regular'})
fig, ax = plt.subplots(figsize=(5.6, 3.2), dpi=220)
bw, off = 0.36, 0.2
for i, cs in enumerate(CS):
    for j, (lab, vals) in enumerate((('Contacts', cnt[cs]), (r'$\sigma_{zz}$', ld[cs]))):
        x = i + (-off if j == 0 else off); b = 0.0
        for g in G:
            v = vals[g]
            ax.bar(x, v, bw, bottom=b, color=COL[g], edgecolor='white', linewidth=0.6, label=g if (i == 0 and j == 0) else None)
            if v >= 6:
                ax.text(x, b + v / 2, f'{v:.0f}', ha='center', va='center', fontsize=6.5, color='white')
            b += v
        if vals['AM–AM'] < 6:
            ax.text(x, vals['AM–AM'] + 2.5, f'{vals["AM–AM"]:.1f}', ha='center', va='bottom', fontsize=6, color='black')
        ax.text(x, 101.5, lab, ha='center', va='bottom', fontsize=6.5, color='#404040')
ax.set_xticks(range(len(CS)), CS); ax.set_xlim(-0.6, len(CS) - 0.4)
ax.set_ylim(0, 108); ax.set_yticks([0, 20, 40, 60, 80, 100], ['0', '20', '40', '60', '80', '100'])
ax.set_xlabel('PC:SC (wt%)'); ax.set_ylabel('Share (%)')
ax.legend(frameon=False, fontsize=7.5, ncol=3, loc='upper center', bbox_to_anchor=(0.5, -0.17))
fig.tight_layout()
for ext in ('png', 'svg'):
    fig.savefig(f'{out}/contacts_vs_sigma_zz_share.{ext}', dpi=220)
print('ok')
