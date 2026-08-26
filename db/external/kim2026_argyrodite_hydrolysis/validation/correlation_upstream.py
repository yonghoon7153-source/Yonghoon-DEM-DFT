import torch
import ase.io

from sevenn.sevennet_calculator import SevenNetCalculator

# Let's test our model by predicting DFT MD trajectory
# Instead of using other functions in SevenNet, we will use ASE calculator as an interface of our model
#DFT_md_xyz = 'test_md.extxyz'
DFT_md_xyz = 'combined.xyz'

# initialize calculator from checkpoint.
fine_tuned_calc = SevenNetCalculator('checkpoint_best.pth')
sevennet_0_calc = SevenNetCalculator('7net-0')  # As a baseline
#no_pretrained_calc = SevenNetCalculator('checkpoint_best_nopretrain.pth')

# load DFT md trajectory
traj = ase.io.read(DFT_md_xyz, index=':')
import numpy as np
from tqdm import tqdm

dft_energy, dft_forces, dft_stress = [], [], []
ft_energy, ft_forces, ft_stress = [], [], []
base_energy, base_forces, base_stress = [], [], []
#nopr_energy, nopr_forces, nopr_stress = [], [], []
to_kBar = 1602.1766208

for atoms in tqdm(traj):
  dft_energy.append(atoms.info['DFT_energy'] / len(atoms))
  dft_forces.append(atoms.arrays['DFT_forces'])
  dft_stress.extend(-1 * atoms.info['DFT_stress'] * to_kBar)
  
  atoms.calc = fine_tuned_calc
  ft_energy.append(atoms.get_potential_energy() / len(atoms))  # as per atom energy
  ft_forces.append(atoms.get_forces())
  ft_stress.extend(-1 * atoms.get_stress() * to_kBar)  # eV/Angstrom^3 to kBar unit

  atoms.calc = sevennet_0_calc
  base_energy.append(atoms.get_potential_energy() / len(atoms))  # as per atom energy
  base_forces.append(atoms.get_forces())
  base_stress.extend(-1 * atoms.get_stress() * to_kBar)

#  atoms.calc = no_pretrained_calc
#  nopr_energy.append(atoms.get_potential_energy() / len(atoms))  # as per atom energy
#  nopr_forces.append(atoms.get_forces())
#  nopr_stress.extend(-1 * atoms.get_stress() * to_kBar)

# flatten forces and stress for parity plot
ft_forces = np.concatenate([f.reshape(-1,) for f in ft_forces])
ft_stress = np.concatenate([s.reshape(-1,) for s in ft_stress])

base_forces = np.concatenate([f.reshape(-1,) for f in base_forces])
base_stress = np.concatenate([s.reshape(-1,) for s in base_stress])

dft_forces = np.concatenate([f.reshape(-1,) for f in dft_forces])
dft_stress = np.concatenate([s.reshape(-1,) for s in dft_stress])

#nopr_forces = np.concatenate([f.reshape(-1,) for f in nopr_forces])
#nopr_stress = np.concatenate([s.reshape(-1,) for s in nopr_stress])

import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
# draw a parity plot of energy / force / stress
unit = {"energy": "eV/atom", "force": r"eV/$\rm{\AA}$", "stress": "kbar"}
def density_colored_scatter_plot(dft_energy, nnp_energy, dft_force, nnp_force, dft_stress, nnp_stress, title=None):
    modes = ['energy', 'force', 'stress']
    plt.figure(figsize=(18/2.54, 6/2.54))
    for num, (x, y) in enumerate(zip([dft_energy, dft_force, dft_stress], [nnp_energy, nnp_force, nnp_stress])):
        mode = modes[num]
        idx = np.random.choice(len(x), 1000) if len(x) > 1000 else list(range(len(x)))
        xsam = [x[i] for i in idx]
        ysam = [y[i] for i in idx]
        xy = np.vstack([x, y])
        xysam = np.vstack([xsam, ysam])
        zsam = gaussian_kde(xysam)

        z = zsam.pdf(xy)
        idx = z.argsort()

        x = [x[i] for i in idx]
        y = [y[i] for i in idx]
        z = [z[i] for i in idx]

        ax = plt.subplot(int(f'13{num+1}'))
        plt.scatter(x, y, c=z, s=4, cmap='plasma')

        mini = min(min(x), min(y))
        maxi = max(max(x), max(y))
        ran = (maxi-mini) / 20
        plt.plot([mini-ran, maxi+ran], [mini-ran, maxi+ran], color='grey', linestyle='dashed')
        plt.xlim(mini-ran, maxi+ran)
        plt.ylim(mini-ran, maxi+ran)

        plt.xlabel(f'DFT {mode} ({unit[mode]})')
        plt.ylabel(f'MLP {mode} ({unit[mode]})')
        ax.set_aspect('equal')
        if title:
          ax.set_title(f'{title} {mode}')
    plt.tight_layout()
    plt.savefig('%s.png' % title)
    plt.show()
def print_mae(label, dft_e, pred_e, dft_f, pred_f, dft_s, pred_s):
    e_mae = np.mean(np.abs(np.array(dft_e) - np.array(pred_e)))
    f_mae = np.mean(np.abs(np.array(dft_f) - np.array(pred_f)))
    s_mae = np.mean(np.abs(np.array(dft_s) - np.array(pred_s)))
    print(f"[{label}]")
    print(f"  Energy MAE : {e_mae:.4f} eV/atom")
    print(f"  Force MAE  : {f_mae:.4f} eV/Å")
    print(f"  Stress MAE : {s_mae:.2f} kbar\n")

density_colored_scatter_plot(dft_energy, base_energy, dft_forces, base_forces, dft_stress, base_stress, '7net-0')
print_mae("7net-0", dft_energy, base_energy, dft_forces, base_forces, dft_stress, base_stress)
density_colored_scatter_plot(dft_energy, ft_energy, dft_forces, ft_forces, dft_stress, ft_stress, 'fine-tuned')
print_mae("fine-tuned", dft_energy, ft_energy, dft_forces, ft_forces, dft_stress, ft_stress)
#density_colored_scatter_plot(dft_energy, ft_energy, dft_forces, nopr_forces, nopr_stress, nopr_stress, 'no-pretrained')
#print_mae("no-pretrained", dft_energy, ft_energy, dft_forces, nopr_forces, dft_stress, nopr_stress)
