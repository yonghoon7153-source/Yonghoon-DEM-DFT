"""comp3 v2 shared lib — load ref, build structure, Li_configs."""
import numpy as np
from pymatgen.core import Structure
from pymatgen.io.ase import AseAtomsAdaptor
from fairchem.core import pretrained_mlip
from fairchem.core.calculate.ase_calculator import FAIRChemCalculator

COMP_NAME = 'comp5'
N_CL = 3        # comp5: 3 Cl / 5 Br at 8 free sites
N_LI_SELECT = 27
N_LI_TRIALS = 20

_predictor = None
def get_predictor():
    global _predictor
    if _predictor is None:
        _predictor = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")
    return _predictor

def new_calc():
    return FAIRChemCalculator(get_predictor(), task_name="omat")

_adaptor = AseAtomsAdaptor()
def get_adaptor(): return _adaptor


def load_ref(cif='ref_comp3.cif'):
    ref = Structure.from_file(cif)
    li_sites, p_sites, s_framework, free_sites = [], [], [], []
    for site in ref:
        sp = str(site.specie); fc = site.frac_coords
        if sp == 'Li': li_sites.append(fc)
        elif sp == 'P': p_sites.append(fc)
        else:
            p_coords = np.array(p_sites) if p_sites else np.zeros((1,3))
            dists = ref.lattice.get_all_distances(fc.reshape(1,-1), p_coords)[0]
            if sp == 'S' and len(p_sites) > 0 and min(dists) < 2.5:
                s_framework.append(fc)
            else:
                free_sites.append(fc)
    return ref, li_sites, p_sites, s_framework, free_sites


def get_li_configs(n_li):
    rng = np.random.RandomState(42)
    return [sorted(rng.choice(n_li, N_LI_SELECT, replace=False).tolist())
            for _ in range(N_LI_TRIALS)]


def build(ref, li_sites, p_sites, s_framework, free_sites,
          s_idx, cl_idx, br_idx, li_idx):
    species, coords = [], []
    for i in li_idx: species.append('Li'); coords.append(li_sites[i])
    for c in p_sites: species.append('P'); coords.append(c)
    for c in s_framework: species.append('S'); coords.append(c)
    for i, c in enumerate(free_sites):
        if i in s_idx: species.append('S')
        elif i in cl_idx: species.append('Cl')
        elif i in br_idx: species.append('Br')
        else: species.append('Cl')
        coords.append(c)
    return Structure(ref.lattice, species, coords)


def jx(x):
    if isinstance(x, np.ndarray): return x.tolist()
    if isinstance(x, (np.integer,)): return int(x)
    if isinstance(x, (np.floating,)): return float(x)
    return x
