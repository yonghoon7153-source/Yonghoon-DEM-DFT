"""Read-only composition audit; no solver or DEM execution."""
import collections
import csv
import gzip
import hashlib
import io
import json
import math
from pathlib import Path
import re
import tarfile

R=Path(__file__).resolve().parents[1]
S=R/'source'
CASE=S/'docs/data/ps45_r45_network_g2_20261007'
DECK=S/'dem_scripts/ps_sweep_6mah_20260914'
KIT=S/'docs/data/ps45_dh_transfer_20260926/kits'

def hashfile(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def mass_to_volume(wam,wse,rhoam,rhose):
    return (wam/rhoam)/(wam/rhoam+wse/rhose)

def main():
    tsv=list(csv.DictReader((CASE/'network_cases.tsv').open(encoding='utf-8'),delimiter='\t'))
    with tarfile.open(CASE/'raw/ps45_network_g2.tgz') as t:
        raw=json.load(t.extractfile('network_cases.json'))
        rows=[]
        for row in raw['rows']:
            bed=row['bed']; cid=row['case_id']; n={int(k):int(v) for k,v in
                (pair.split(':') for pair in row['dump_type_counts'].split(','))}
            deckpath=DECK/f'in.{bed}.liggghts'; text=deckpath.read_text(encoding='utf-8')
            rr={name:float(value) for name,value in re.findall(r'^variable\s+(r_\w+)\s+equal\s+(\S+)',text,re.M)}
            densities={int(ty):float(dens) for ty,dens in re.findall(r'atom_type\s+(\d+)\s+density constant\s+(\S+)',text)}
            distribution=next(line for line in text.splitlines() if line.startswith('fix pdd_mix '))
            weights={int(k):float(v) for k,v in re.findall(r'pts(\d+)\s+([0-9.]+)',distribution)}
            radii={1:rr['r_AM_P']*1000,2:rr['r_AM_S']*1000,3:rr['r_SE']*1000}
            sp=KIT/f'kit_{bed}__am_scaffold.csv.gz'
            scaffold=gzip.open(sp,'rt',encoding='utf-8').read()
            header=scaffold.splitlines()[0]
            entries=list(csv.reader(line for line in scaffold.splitlines() if line and not line.startswith('#')))
            sn=collections.Counter(int(entry[0]) for entry in entries)
            sr={str(ty):sorted({float(e[4])*1000 for e in entries if int(e[0])==ty}) for ty in (1,2)}
            vam=math.fsum(4/3*math.pi*(float(e[4])*1000)**3 for e in entries)
            vp=math.fsum(4/3*math.pi*(float(e[4])*1000)**3 for e in entries if int(e[0])==1)
            vse=n.get(3,0)*4/3*math.pi*radii[3]**3
            vcount={str(ty):n.get(ty,0)*4/3*math.pi*radii[ty]**3 for ty in (1,2,3)}
            sol=json.load(t.extractfile(f'solver_output/{cid}/network_conductivity_hertzian.json'))
            geom=sol['solve_certificate_full']['geometry']
            vbox=geom['plate_z']*geom['box_x']*geom['box_y']*geom['scale']**3
            vmc=float(row['thickness_mass_conserving_um'])*(geom['box_x']*geom['scale'])*(geom['box_y']*geom['scale'])
            trow=next(x for x in tsv if x['case_id']==cid)
            phi=vam/(vam+vse)
            rows.append(dict(bed=bed,P_S=row['P_S'],case_id=cid,deck=str(deckpath.relative_to(S)),deck_sha256=hashfile(deckpath),
                scaffold=str(sp.relative_to(S)),scaffold_sha256=hashfile(sp),scaffold_header=header,
                scaffold_case_id_matches=cid in header,raw_type_counts=n,tsv_raw_counts_agree=trow['dump_type_counts']==row['dump_type_counts'],
                scaffold_counts=dict(sn),scaffold_radii_um=sr,deck_radii_um=radii,deck_densities_kg_m3=densities,
                scaffold_am_counts_match_raw=all(sn.get(ty,0)==n.get(ty,0) for ty in (1,2)),
                scaffold_am_volume_matches_count_radius=math.isclose(vam,vcount['1']+vcount['2'],rel_tol=1e-14),
                raw_solver_nodes_match_counts=sol['n_nodes']==n[3] and sol['electronic_n_nodes']==n.get(1,0)+n.get(2,0),
                deck_mass_weights=weights,deck_am_solid_volume_fraction=mass_to_volume(weights.get(1,0)+weights.get(2,0),weights[3],densities[1],densities[3]),
                AM_volume_um3=vam,SE_volume_um3=vse,AM_solid_volume_fraction=phi,PC_fraction_of_AM_volume=vp/vam,
                AM_weight_fraction_at_deck_densities=vam*densities[1]/(vam*densities[1]+vse*densities[3]),
                AM_weight_fraction_at_4850_1640=vam*4850/(vam*4850+vse*1640),
                AM_volume_fraction_gap=vam/vbox,SE_volume_fraction_gap=vse/vbox,
                AM_volume_fraction_mass_conserving_height=vam/vmc,SE_volume_fraction_mass_conserving_height=vse/vmc,
                gap_porosity_from_sphere_sum=1-(vam+vse)/vbox,tsv_porosity_fraction=float(row['porosity'])/100,
                tsv_phi_se=float(row['phi_se']),tsv_phi_se_mass_conserving=float(row['phi_se_mass_conserving']),
                raw_solver_phi_se_rounded=sol['phi_se'],network_code_sha=row['network_code_sha'],atom_step=row['atom_step']))
    run=R/'evidence/network_conductivity_run0801.py'; now=S/'scripts/network_conductivity.py'
    return dict(scope='Read-only deck/scaffold/stored raw-record audit; no production run',
        formulas=dict(solid_AM_fraction='sum_AM(4*pi*r^3/3)/(sum_AM(4*pi*r^3/3)+N_SE*4*pi*r_SE^3/3)',
                      mass_to_volume='(w_AM/rho_AM)/(w_AM/rho_AM+w_SE/rho_SE)'),
        nominal_comparisons=dict(normalized_0816_0184_deck4800_2000=mass_to_volume(.816,.184,4800,2000),
                                 normalized_0816_0184_user4850_1640=mass_to_volume(.816,.184,4850,1640),
                                 exact_80_18_deck4800_2000=mass_to_volume(80,18,4800,2000),
                                 exact_80_18_user4850_1640=mass_to_volume(80,18,4850,1640)),
        raw_tgz_sha256=hashfile(CASE/'raw/ps45_network_g2.tgz'),tsv_sha256=hashfile(CASE/'network_cases.tsv'),
        solver_file_comparison=dict(run0801_sha256=hashfile(run),latest46cd_sha256=hashfile(now),identical=run.read_bytes()==now.read_bytes()),
        linkage_limitations=['No full atom dump or SE scaffold in this source subset; SE radius uses matched deck constant.',
                             'AM scaffold header case IDs, all AM counts/radii, archive TSV counts, and solver node counts agree; this is strong linkage but not byte-identical original atom input verification.',
                             'build_ps45_kits.py links kits from webapp case IDs and count tolerances; it explicitly cannot verify final dump is the completed DEM trajectory.',
                             'Sphere volumes are nominal particle volumes, not the exact union of overlapping deformed particles or measured electrode phase volumes.'],
        rows=rows)

print(json.dumps(main(),ensure_ascii=True,indent=2))
