"""Small exact circuit/geometric counterexamples to the proposed design, no DEM/FV runs."""
import json
import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'source' / 'scripts'))
from fibre_segment_raster import segment_cells


def network(n, edges, source, sink):
    L = np.zeros((n, n))
    for a, b, g, tag in edges:
        L[a,a] += g; L[b,b] += g
        L[a,b] -= g; L[b,a] -= g
    u = np.zeros(n); u[source] = 1.
    free = [i for i in range(n) if i not in (source,sink)]
    u[free] = np.linalg.solve(L[np.ix_(free,free)], -L[free,source])
    I = float((L @ u)[source])
    P = {}
    for a,b,g,tag in edges:
        P[tag] = P.get(tag, 0.) + float(g*(u[a]-u[b])**2)
    return {'G_S': I, 'R_ohm': 1/I, 'potentials': u.tolist(), 'P_W': P}


out = {}
# SV branch: high axial resistance is outside the guarded SV/SDCP dissipation category.
sv = network(4, [(0,1,1/1000,'carbon_axial'),(1,3,1/50,'SV_SDCP'),
                 (0,2,1/5000,'VV'),(2,3,1/5000,'VV')],0,3)
sv['SV_terminal_current_fraction'] = float((sv['potentials'][1]/50)/sv['G_S'])
sv['SV_DOMINANT_guard'] = sv['P_W']['SV_SDCP'] >= sv['P_W']['VV']
sv['G_ratio_to_SV_path_cut'] = sv['G_S']/(1/10000)
out['sv_dissipation_guard'] = sv

# Same polyline, different redundant collinear sampling: S0 derived tolerance differs.
d = 0.18; rf = 0.075
out['s0_resampling'] = [
    {'point_spacing_um': h, 'tol_ff_um': min(h/2,rf),
     'centreline_distance_um':d, 'register_contact':d <= 2*rf+min(h/2,rf)}
    for h in (.10,.02)]

# Midpoint face quadrature may declare zero when real open area is positive.
r=.65
blocked=np.pi*r*r-4*(r*r*np.arccos(.5/r)-.5*np.sqrt(r*r-.25))
out['face_false_zero']={'h':1.,'radius':r,'exact_alpha':float(1-blocked),
    'midpoint_alpha':{str(k):float(1-np.mean(sum(x*x for x in np.meshgrid(
        (np.arange(k)+.5)/k-.5,(np.arange(k)+.5)/k-.5)) <= r*r))
        for k in (4,8,16,32)}}

# Existing actual raster function sees a same-fid path visit a cell twice after a long detour.
# Two straight strands are separated by sqrt(2)*0.13 > diameter .15, inside one h=.15 cell.
pts = np.array([[.01,.01,.01],[.44,.01,.01],[.44,.44,.01],
                [.44,.44,.14],[.44,.14,.14],[.01,.14,.14]])
cell_runs = [segment_cells(a,b,.15).tolist() for a,b in zip(pts[:-1],pts[1:])]
target = [0,0,0]
visits = [i for i,run in enumerate(cell_runs) if target in run]
out['same_fid_same_cell'] = {
    'points_um':pts.tolist(),'r_f_um':rf,'h_um':.15,'target_cell':target,
    'segments_visiting_target':visits,'segments':cell_runs,
    'strand_separation_um':float(np.sqrt(2)*.13),
    'finite_path_R_ohm':5.,'collapsed_cell_fid_R_ohm':2.,'G_multiplier':2.5,
    'explanation':'5-edge series graph has two nonconsecutive target-cell visits at nodes1,4; identifying cell,fid merges1,4 and shorts middle3 edges.'}

# Closest-point tied ports: reversing identical physical path reverses cell-list index.
out['port_tie'] = {
 'port_near_terminal':network(3,[(0,1,1.,'axial'),(0,2,1.,'junction')],0,2),
 'port_after_reversal':network(3,[(0,1,1.,'axial'),(1,2,1.,'junction')],0,2),
 'geometry':'instance at midpoint between adjacent cell centres; equal distances; path reversal only changes index-order tie winner.'}

# Distributed long contact and same-total-G one-point substitute, two end boundary conditions.
def rails(distributed, source, sink, port=2, axial=(1.,1.)):
    n=5; edges=[]
    for rail,rr in enumerate(axial):
        edges += [(rail*n+i,rail*n+i+1,1/rr,'axial') for i in range(n-1)]
    if distributed:
        edges += [(i,n+i,1.,'junction') for i in range(n)]
    else:
        edges += [(port,n+port,5.,'junction')]
    return network(10,edges,source,sink)
out['long_contact_lumping'] = []
for source,sink,port in [(0,5,0),(0,5,2),(0,9,2),(0,4,2)]:
    a=rails(True,source,sink); b=rails(False,source,sink,port=port)
    out['long_contact_lumping'].append({'source':source,'sink':sink,
       'lumped_port':port,
       'G_distributed':a['G_S'],'G_lumped':b['G_S'],
       'relative_error':b['G_S']/a['G_S']-1,'same_total_junction_G_S':5.})

rp = 1e-4/(1e4*np.pi*(.075e-4)**2)  # ohm per micrometre, Endo fixed bulk.
out['transfer_length']={'axial_ohm_per_um':float(rp), 'lambda_um':
    {str(rj):float(np.sqrt(rj*.30/(2*rp))) for rj in (1e4,1e6,1e8)},
    'formula':'lambda=sqrt(R_j0*L_par/(rprime_i+rprime_j)) for uniform distributed contact; criterion L_c/lambda small needs preregistered numerical bound.'}
rendered=json.dumps(out, ensure_ascii=False, indent=2)
(ROOT/'_repro_ours_20261021'/'geometry_probe_results.json').write_text(rendered+'\n',encoding='utf8')
print(rendered)
