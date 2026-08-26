import os, sys
import pickle
from pymatgen.io.vasp.outputs import Vasprun

import pandas as pd
import numpy as np
import scipy
import argparse
from tqdm import tqdm
from scipy.spatial import ConvexHull
from itertools import permutations
from pymatgen.core.structure import Structure
from pymatgen.core.periodic_table import *
from pymatgen.core.composition import *
from pymatgen.ext.matproj import MPRester
from pymatgen.io.vasp.outputs import *
from pymatgen.analysis.chemenv.coordination_environments.coordination_geometry_finder import LocalGeometryFinder
from pymatgen.analysis.chemenv.coordination_environments.structure_environments import LightStructureEnvironments
from pymatgen.analysis.chemenv.coordination_environments.chemenv_strategies import SimplestChemenvStrategy
from pymatgen.analysis.chemenv.coordination_environments.coordination_geometries import *

start = int(sys.argv[1])
final = int(sys.argv[2])

runs = range(start, final + 1)

vaspruns = []
for i in runs:
    if os.path.isfile("run%03d/vasprun.xml.gz" % i):
        vaspruns.append("run%03d/vasprun.xml.gz" % i)
    elif os.path.isfile("run%03d/vasprun.xml" % i):
        vaspruns.append("run%03d/vasprun.xml" % i)
    else:
        print("run%03d/vasprun.xml* not exist." % i)
        print("Quit.")
        quit()

print(vaspruns)

structures = []
for vasprun in vaspruns:
    run = Vasprun(vasprun)
    strs = run.structures
    for i in strs:
        structures.append(i)


def non_elements(struct, sp='Li'):
    '''
    struct : structure object from Pymatgen
    sp : the mobile specie
    returns the structure with all of the mobile specie (Li) removed
    '''
    num_li = struct.species.count(Element(sp))
    species = list(set(struct.species))
    species.remove(Element("S"))
    stripped = struct.copy()
    stripped.remove_species(species)
    stripped = stripped.get_sorted_structure(reverse=True)
    return stripped

def site_env(coord, struct, sp='Li'):
    stripped = non_elements(struct)
    with_li = stripped.copy()
    with_li.append(sp, coord, coords_are_cartesian=False, validate_proximity=False)
    with_li = with_li.get_sorted_structure()
    for dist in np.linspace(1, 4, 701):
        lists = []
        neigh = with_li.get_neighbors(with_li.sites[0], dist)
        if len(neigh) < 4:
            continue
        elif len(neigh) == 5:
            neigh = neigh[:4]
        elif len(neigh) > 5:
            break
        neigh_coords = [i.coords for i in neigh]        
        lgf = LocalGeometryFinder()
        lgf.setup_structure(structure=with_li)
        lgf.setup_local_geometry(isite=0, coords=neigh_coords)
        try:
            csm_value = (lgf.get_coordination_symmetry_measures()['T:4']['csm'])
            site_volume = ConvexHull(neigh_coords).volume

        except Exception as e:
            print(e)
            print('This site cannot be recognized as tetrahedral site')
        lists.append(csm_value)
        lists.append(site_volume)
        if len(neigh) == 4:
            break
        
    return lists

def extract_sites(structs, sp='Li'):
    csm_dicts, volume_dicts = {}, {}
    li_count  = sum(1 for site in structs[0] if site.specie.symbol == 'Li')

    for l in range(li_count):
        csm_dicts[l] = []
        volume_dicts[l] = []

    for j, structure in tqdm(enumerate(structs)):
#        envlist = []
        if j % 50 == 0:
            count = 0 
            for i in range(len(structure.sites)):
                if structure.sites[i].specie == Element(sp):
                    site = structure.sites[i] # Li sites
                    tmp_lists =  site_env(site.frac_coords, structure, sp)
                    site_info1, site_info2 = tmp_lists[0], tmp_lists[1]
                    csm_dicts[count].append(site_info1) 
                    volume_dicts[count].append(site_info2) 
                    count += 1

    return csm_dicts, volume_dicts

def export_values(csm_dicts, volume_dicts):
    ave1, ave2 = {}, {}
    print(csm_dicts)
    for key, values in csm_dicts.items():
        avg = sum(values) / len(values)
        ave1[key] = []
        ave1[key].append(avg)
    
    for key, values in volume_dicts.items():
        avg = sum(values) / len(values)
        ave2[key] = []
        ave2[key].append(avg)
    
    return ave1, ave2

site_info1, site_info2 = extract_sites(structures)
csm_ave, vol_ave = export_values(site_info1, site_info2)

df1 = pd.DataFrame.from_dict(csm_ave, orient='index')
df2 = pd.DataFrame.from_dict(vol_ave, orient='index')
df1.to_csv('csm_ave.csv')
df2.to_csv('vol_ave.csv')
print(df1)
print(df2)