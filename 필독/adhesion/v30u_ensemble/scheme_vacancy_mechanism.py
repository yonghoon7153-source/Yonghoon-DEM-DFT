"""scheme_vacancy_mechanism.py — graphical-abstract style figure showing
the vacancy-driven family signal in SE/NCM adhesion.

Side-by-side 2-panel scheme:
  Left:  Li6 family (comp1, Li₆PS₅Cl) — S-rich surface → fewer Li-O, more S-O
  Right: Li5.4 family (comp4, Li₅.₄PS₄.₄Cl₀.₈Br₀.₈) — vacancy-mediated Li-rich
         surface → more Li-O, fewer S-O

Annotations:
  • NCM block (gray) with O atoms (red) facing up
  • SE block (composite color) with key atoms exposed
  • Cyan arrows: Li-O attractive contacts (paper-direction)
  • Red dashed: S-O repulsive contacts
  • Vacancy (dashed circle) in Li5.4 panel + Li-migration arrow
  • Paper W_ad values overlaid

Output: scheme_vacancy_mechanism.{png,pdf}
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch, FancyBboxPatch
from matplotlib.lines import Line2D
import numpy as np

COLORS = {
    'Li': '#9971D9', 'P': '#A8A8A8', 'S': '#FCC830',
    'Cl': '#1FE61F', 'Br': '#A52A2A',
    'Ni': '#5078D2', 'O': '#FF1C00',
}

# Layout constants
INTERFACE_Z = 4.0          # interface y-position (z-axis in our view)
SE_TOP_Z = 11.0
NCM_BOTTOM_Z = 0.0
ATOM_R = 0.32              # sphere radius (visual)
PANEL_W = 8.0              # width of each panel in atomic units


def draw_atom(ax, x, y, element, radius=ATOM_R, label=None, alpha=1.0):
    """Draw a single atom as a filled circle with edge."""
    c = COLORS.get(element, '#888')
    circle = Circle((x, y), radius, facecolor=c, edgecolor='black',
                    linewidth=1.0, alpha=alpha, zorder=3)
    ax.add_patch(circle)
    if label:
        ax.text(x, y + radius + 0.15, label, ha='center', fontsize=7, zorder=4)


def draw_ncm_block(ax, x_lo, x_hi, z_lo, z_hi):
    """Draw NCM slab background + O atoms at top + Ni atoms inside."""
    # Background
    bg = Rectangle((x_lo, z_lo), x_hi - x_lo, z_hi - z_lo,
                   facecolor='#E0E8F5', edgecolor='#5078D2',
                   linewidth=1.2, alpha=0.55, zorder=1)
    ax.add_patch(bg)
    ax.text(x_lo + 0.3, z_lo + 0.3, "NCM (LiNiO$_2$)", fontsize=10,
            color='#3A57A8', fontweight='bold', zorder=4)

    # O atoms at top (NCM-facing)
    n_O = 6
    o_xs = np.linspace(x_lo + 0.8, x_hi - 0.8, n_O)
    for x in o_xs:
        draw_atom(ax, x, z_hi - 0.3, 'O', radius=0.30)

    # Ni atoms inside
    ni_xs = np.linspace(x_lo + 1.4, x_hi - 1.4, 3)
    ni_y = (z_lo + z_hi) / 2 - 0.4
    for x in ni_xs:
        draw_atom(ax, x, ni_y, 'Ni', radius=0.35)


def draw_se_block_li6(ax, x_lo, x_hi, z_lo, z_hi):
    """SE block for Li6 family (comp1): S-rich termination at bottom."""
    bg = Rectangle((x_lo, z_lo), x_hi - x_lo, z_hi - z_lo,
                   facecolor='#FFF5DE', edgecolor='#FCC830',
                   linewidth=1.2, alpha=0.55, zorder=1)
    ax.add_patch(bg)
    ax.text(x_lo + 0.3, z_hi - 0.5, "Li$_6$PS$_5$Cl (comp1)",
            fontsize=10, color='#A8861A', fontweight='bold', zorder=4)

    # Interface termination (bottom of SE) — S-rich + Cl + few Li
    z_term = z_lo + 0.3
    se_positions = [
        ('S',  x_lo + 1.0, z_term),
        ('S',  x_lo + 2.2, z_term),
        ('Li', x_lo + 3.4, z_term),
        ('S',  x_lo + 4.6, z_term),
        ('Cl', x_lo + 5.8, z_term),
        ('S',  x_lo + 7.0, z_term),
    ]
    for el, x, y in se_positions:
        draw_atom(ax, x, y, el)

    # SE bulk (above) — fewer atoms, just indicative
    bulk_z = z_lo + 1.5
    bulk = [
        ('Li', x_lo + 1.5, bulk_z), ('S',  x_lo + 3.0, bulk_z),
        ('Li', x_lo + 4.5, bulk_z), ('P',  x_lo + 6.0, bulk_z),
        ('Li', x_lo + 1.5, bulk_z + 1.5), ('Li', x_lo + 3.0, bulk_z + 1.5),
        ('S',  x_lo + 4.5, bulk_z + 1.5), ('Li', x_lo + 6.0, bulk_z + 1.5),
    ]
    for el, x, y in bulk:
        draw_atom(ax, x, y, el, alpha=0.7)


def draw_se_block_li54(ax, x_lo, x_hi, z_lo, z_hi):
    """SE block for Li5.4 family (comp4): Li-rich termination + vacancy."""
    bg = Rectangle((x_lo, z_lo), x_hi - x_lo, z_hi - z_lo,
                   facecolor='#F0E0F5', edgecolor='#9971D9',
                   linewidth=1.2, alpha=0.55, zorder=1)
    ax.add_patch(bg)
    ax.text(x_lo + 0.3, z_hi - 0.5, "Li$_{5.4}$PS$_{4.4}$Cl$_{0.8}$Br$_{0.8}$ (comp4)",
            fontsize=10, color='#5B3C8B', fontweight='bold', zorder=4)

    # Interface termination — Li-rich
    z_term = z_lo + 0.3
    se_positions = [
        ('Li', x_lo + 1.0, z_term),
        ('Li', x_lo + 2.2, z_term),
        ('Br', x_lo + 3.4, z_term),
        ('Li', x_lo + 4.6, z_term),
        ('Li', x_lo + 5.8, z_term),
        ('Li', x_lo + 7.0, z_term),
    ]
    for el, x, y in se_positions:
        draw_atom(ax, x, y, el)

    # SE bulk — vacancy + migration arrow
    bulk_z = z_lo + 1.5
    bulk = [
        ('Li', x_lo + 1.5, bulk_z), ('S',  x_lo + 3.0, bulk_z),
        ('Li', x_lo + 4.5, bulk_z), ('P',  x_lo + 6.0, bulk_z),
        ('S',  x_lo + 3.0, bulk_z + 1.5), ('Li', x_lo + 6.0, bulk_z + 1.5),
    ]
    for el, x, y in bulk:
        draw_atom(ax, x, y, el, alpha=0.7)

    # Vacancy (dashed empty circle)
    vac_x, vac_y = x_lo + 1.5, bulk_z + 1.5
    vac = Circle((vac_x, vac_y), ATOM_R, facecolor='none',
                 edgecolor='black', linestyle='--', linewidth=1.5, zorder=3)
    ax.add_patch(vac)
    ax.text(vac_x, vac_y + 0.55, "V$_{Li}$", ha='center', fontsize=8,
            fontweight='bold', color='black', zorder=4)

    # Li migration arrow (from vacancy region to interface)
    arr = FancyArrowPatch((vac_x, vac_y - 0.4), (vac_x + 0.2, z_term + 0.4),
                          arrowstyle='->', mutation_scale=18,
                          color='#9971D9', linewidth=2.0,
                          connectionstyle="arc3,rad=-0.3", zorder=4)
    ax.add_patch(arr)
    ax.text(vac_x - 0.3, (vac_y + z_term) / 2 + 0.3, "Li migration",
            fontsize=8, color='#5B3C8B', rotation=70, fontweight='bold',
            zorder=4)


def draw_interface_contacts_li6(ax, x_lo, x_hi):
    """S-O repulsive (many), Li-O attractive (few) — Li6 case."""
    # S-O repulsive (red dashed × marks between S and O)
    z_o = INTERFACE_Z - 0.3
    z_s = INTERFACE_Z + 0.3
    se_pos = [(x_lo + 1.0, 'S'), (x_lo + 2.2, 'S'),
              (x_lo + 4.6, 'S'), (x_lo + 7.0, 'S'),
              (x_lo + 3.4, 'Li')]
    o_xs = np.linspace(x_lo + 0.8, x_hi - 0.8, 6)

    n_repulsive, n_attract = 0, 0
    for x_se, el in se_pos:
        # Find nearest O
        x_o = o_xs[np.argmin(np.abs(o_xs - x_se))]
        if el == 'S':
            # Red dashed line + X mark
            ax.plot([x_se, x_o], [z_s, z_o], color='#FF1C00',
                    linestyle=':', linewidth=2.0, alpha=0.8, zorder=2)
            n_repulsive += 1
        elif el == 'Li':
            ax.plot([x_se, x_o], [z_s, z_o], color='#00BFFF',
                    linestyle='-', linewidth=2.5, alpha=0.9, zorder=2)
            n_attract += 1
    return n_attract, n_repulsive


def draw_interface_contacts_li54(ax, x_lo, x_hi):
    """Li-O attractive (many), S-O few — Li5.4 case."""
    z_o = INTERFACE_Z - 0.3
    z_s = INTERFACE_Z + 0.3
    se_pos = [(x_lo + 1.0, 'Li'), (x_lo + 2.2, 'Li'),
              (x_lo + 4.6, 'Li'), (x_lo + 5.8, 'Li'),
              (x_lo + 7.0, 'Li'), (x_lo + 3.4, 'Br')]
    o_xs = np.linspace(x_lo + 0.8, x_hi - 0.8, 6)

    n_attract = 0
    for x_se, el in se_pos:
        x_o = o_xs[np.argmin(np.abs(o_xs - x_se))]
        if el == 'Li':
            ax.plot([x_se, x_o], [z_s, z_o], color='#00BFFF',
                    linestyle='-', linewidth=2.5, alpha=0.9, zorder=2)
            n_attract += 1
        elif el == 'Br':
            ax.plot([x_se, x_o], [z_s, z_o], color='#9932CC',
                    linestyle='--', linewidth=1.5, alpha=0.7, zorder=2)
    return n_attract


def draw_panel(ax, family, x_offset=0):
    """Draw one full panel."""
    x_lo = x_offset
    x_hi = x_offset + PANEL_W

    # NCM block
    draw_ncm_block(ax, x_lo, x_hi, NCM_BOTTOM_Z, INTERFACE_Z - 0.6)
    # Interface dashed line
    ax.plot([x_lo, x_hi], [INTERFACE_Z - 0.6, INTERFACE_Z - 0.6],
            color='black', linestyle='--', linewidth=0.8, alpha=0.5, zorder=2)

    if family == 'Li6':
        draw_se_block_li6(ax, x_lo, x_hi, INTERFACE_Z, SE_TOP_Z)
        n_att, n_rep = draw_interface_contacts_li6(ax, x_lo, x_hi)
        ax.text((x_lo + x_hi) / 2, SE_TOP_Z + 0.8,
                f"S-rich termination → {n_rep} S–O repulsive, {n_att} Li–O attractive",
                ha='center', fontsize=9.5, color='#A8861A', fontweight='bold')
        ax.text((x_lo + x_hi) / 2, NCM_BOTTOM_Z - 1.0,
                "$W_{ad}$ = 194 aJ  (paper)", ha='center', fontsize=12,
                color='#3A57A8', fontweight='bold')
    else:
        draw_se_block_li54(ax, x_lo, x_hi, INTERFACE_Z, SE_TOP_Z)
        n_att = draw_interface_contacts_li54(ax, x_lo, x_hi)
        ax.text((x_lo + x_hi) / 2, SE_TOP_Z + 0.8,
                f"Li-rich termination → {n_att} Li–O attractive (+ vacancy)",
                ha='center', fontsize=9.5, color='#5B3C8B', fontweight='bold')
        ax.text((x_lo + x_hi) / 2, NCM_BOTTOM_Z - 1.0,
                "$W_{ad}$ = 298 aJ  (paper, +53%)",
                ha='center', fontsize=12, color='#5B3C8B', fontweight='bold')

    ax.set_xlim(x_lo - 0.5, x_hi + 0.5)
    ax.set_ylim(NCM_BOTTOM_Z - 2.0, SE_TOP_Z + 2.0)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)


def main():
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))

    draw_panel(axes[0], 'Li6')
    draw_panel(axes[1], 'Li5.4')

    # Title
    fig.suptitle("Vacancy-driven family signal in SE/NCM adhesion",
                 fontsize=15, fontweight='bold', y=0.98)

    # Subtitle
    fig.text(0.5, 0.925,
             "Li$_{5.4}$ family — vacancy enables Li migration to interface, "
             "exposing more Li–O attractive contacts and fewer S–O repulsive contacts",
             ha='center', fontsize=11, style='italic', color='#444')

    # Bottom mechanism arrow
    fig.text(0.5, 0.05,
             "stoichiometric  →  S-O dominant  →  weak $W_{ad}$    "
             "       vs       "
             "    vacancy → Li migration → Li-O dominant → strong $W_{ad}$",
             ha='center', fontsize=11, color='#222', fontweight='bold')

    # Legend (atoms + bond types)
    handles = []
    for el, c in COLORS.items():
        handles.append(Line2D([0], [0], marker='o', color='w',
                              markerfacecolor=c, markeredgecolor='k',
                              markersize=10, label=el))
    handles.append(Line2D([0], [0], color='#00BFFF', linewidth=2.5,
                          label='Li–O attractive'))
    handles.append(Line2D([0], [0], color='#FF1C00', linewidth=2,
                          linestyle=':', label='S–O repulsive'))
    handles.append(Line2D([0], [0], color='#9932CC', linewidth=1.5,
                          linestyle='--', label='Br–O contact'))
    handles.append(Line2D([0], [0], marker='o', color='w',
                          markerfacecolor='none', markeredgecolor='k',
                          markersize=10, label='V$_{Li}$ (vacancy)'))
    fig.legend(handles=handles, loc='center right', bbox_to_anchor=(0.99, 0.5),
               fontsize=9, framealpha=0.95, title='Legend', title_fontsize=10)

    plt.tight_layout(rect=[0, 0.06, 0.94, 0.92])
    out = "scheme_vacancy_mechanism"
    fig.savefig(f"{out}.png", dpi=250, bbox_inches='tight')
    fig.savefig(f"{out}.pdf", bbox_inches='tight')
    print(f"Saved: {out}.png")
    print(f"Saved: {out}.pdf")


if __name__ == "__main__":
    main()
