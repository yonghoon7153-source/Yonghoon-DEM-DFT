"""Static source assertions and arithmetic only; no DEM/MPI/cluster execution."""
from pathlib import Path
import hashlib, json, math
from statistics import mean, stdev
HERE=Path(__file__).resolve().parent
SRC=HERE/"sources"
SNAP=HERE.parent.parent/"snapshot"/"repo"

manifest=json.loads((SRC/"source_manifest.json").read_text(encoding="utf-8"))
source_hashes=[]
for r in manifest:
    raw=(SRC/r["local"]).read_bytes()
    gitblob=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
    assert gitblob==r["blob_sha"], (r["path"],gitblob,r["blob_sha"])
    source_hashes.append(dict(path=r["path"],git_blob=gitblob,verified=True))
pack=(SRC/"fix_insert_pack.cpp").read_text(encoding="utf-8")
dist=(SRC/"fix_particledistribution_discrete.cpp").read_text(encoding="utf-8")
domain=(SRC/"src__domain_I.h").read_text(encoding="utf-8")
insert=(SRC/"fix_insert.cpp").read_text(encoding="utf-8")
assert "check_dist_from_subdomain_border_ = true;" in pack
assert "domain->dist_subbox_borders(pos) < rbound" in pack
assert "pti = fix_distribution->pti_list[ninserted_this_local];" in pack
assert "while(nins == 0 && ntry < maxtry)" in pack
assert "exact_number = 1;" in insert
assert "wire lists, make sure in correct order (large to small particles)" in dist
assert "pti_list[n_pti + j] = templates[chosendist]->pti_list[j];" in dist
segment=domain.split("inline double Domain::dist_subbox_borders(")[1].split("/*")[0]
assert "vectorMin3D(deltalo)" in segment and "vectorMin3D(deltahi)" in segment
assert "periodic" not in segment

number_am=(.85/(4850*3**3))/(.85/(4850*3**3)+.15/(1640*.35**3))
max_total_if_no_am=math.ceil(1/number_am)-1
geometries=[]
for np in (28,56):
    pairs=[(px,np//px) for px in range(1,np+1) if np%px==0]
    all_impossible=all(min(40/px,40/py)<6 for px,py in pairs)
    assert all_impossible
    px,py=min(pairs,key=lambda p:sum(p))
    wx,wy=40/px,40/py
    local_target=312506/np
    record=dict(np=np,all_integer_factor_pairs=pairs,
        every_factorization_has_width_lt_am_diameter=all_impossible,
        automatic_grid=[px,py,1],local_xy_um=[wx,wy],
        largest_possible_distance_to_nearest_xy_face_um=min(wx,wy)/2,
        required_clearance_um=3,expected_target_each_rank=local_target,
        am_floor_near_uniform_target=math.floor(math.floor(local_target)*number_am),
        geometric_am_insertion_capacity=0,
        usual_uniform_case_total_inserted_prediction=0,
        rigorous_upper_total_if_arbitrary_allocation=np*max_total_if_no_am,
        total_gate=309380)
    assert record["rigorous_upper_total_if_arbitrary_allocation"]<record["total_gate"]
    geometries.append(record)
    for skin in (20,5):
        tag=f"kg50_spd_d07_b40_sk{skin:02}_np{np}"
        folder=SNAP/"docs/data/kg50_decks_20261026/speed"/tag
        deck=(folder/f"input_{tag}.liggghts").read_text(encoding="utf-8")
        runner=(folder/f"run_{tag}.sh").read_text(encoding="utf-8")
        assert "processors * * 1" in deck
        assert "check_dist_from_subdomain_border" not in deck
        assert "variable r_AM_P  equal 3e-3" in deck
        assert "2 pts1 0.85 pts3 0.15" in deck
        assert "maxattempt 3000 insert_every once overlapcheck yes all_in no" in deck
        assert f"-np {np}" in runner
        assert deck.rstrip().endswith("run 20000")
        assert "fix top_mesh" not in deck and "fix move_press" not in deck
        assert "g_am_ins" not in deck

# Arithmetic estimates; not dynamic simulation or a timing measurement.
v_am=.85/4.85
v_se=.15/1.64
solid_se=v_se/(v_am+v_se)
phi_se_insertion=.321*solid_se
neighbors=[]
halos=[]
for skin in (2,.5):
    for r in (.35,.5,1,1.5):
        neighbors.append(dict(se_radius_um=r,skin_um=skin,
            candidate_count_at_se_volfrac_030=.3*((2*r+skin)/r)**3,
            candidate_count_at_initial_se_volfrac=phi_se_insertion*((2*r+skin)/r)**3))
    for np,px,py in [(28,4,7),(56,7,8)]:
        wx,wy=40/px,40/py
        h=6+skin
        halos.append(dict(np=np,skin_um=skin,halo_um=h,
            uniform_xy_ghost_owned_ratio=(wx+2*h)*(wy+2*h)/(wx*wy)-1,
            mesh_only_steps_half_skin=(skin/2)/(10*1e-6)))
se=.31*math.sqrt(2/3)
ci90=2.13184678632665*se
ci95=2.7764451051978*se
x=[19.69,20,20.31]
y=[20.09,20.4,20.71]
assert abs(mean(x)-mean(y))<=.5
result=dict(
    scope="static assertions + deterministic arithmetic; no physical simulation",
    source_hash_verification=source_hashes,
    source_assertions="passed",
    am_number_fraction=number_am,
    max_local_insert_target_that_can_floor_am_to_zero=max_total_if_no_am,
    speed_fixture_impossibility=geometries,
    insertion_arithmetic=dict(solid_phase_se_volume_fraction=solid_se,
        initial_se_volume_fraction=phi_se_insertion,
        initial_am_volume_fraction=.321*(1-solid_se),
        maxtry_np1_40=312506*3000,int32_max=2**31-1,
        meaning="finite trial cap and low average fraction are not a guarantee of completing random sequential insertion"),
    neighbor_candidates_heuristic=neighbors,
    ghost_halo_uniform_density_heuristic=halos,
    benchmark_phase_gap=dict(benchmark_steps=20000,benchmark_seconds=.02,
        settling_fraction=.1,total_5M_fraction=.004,total_7M_fraction=20000/7000000,
        benchmark_gravity=98.1,compression_gravity=9.81,
        benchmark_gamma=1e-5,compression_gamma=.5,gamma_ratio=.5/1e-5,
        benchmark_mesh=False,benchmark_atom_dump=False,
        total_steps_if_plate_travel_50_60um=[int(50/10/1e-6+500000),int(60/10/1e-6+500000)],
        elapsed_from_neighbor_count_alone="not identifiable"),
    area_pilot_uncertainty=dict(assumption="independent normal outcomes; observed SD .31 percentage points in both groups; illustrative, not measured KG50 scatter",
        n_each=3,df=4,se_difference_pp=se,halfwidth_90_pp=ci90,halfwidth_95_pp=ci95,
        illustrative_40=x,illustrative_50=y,illustrative_sd40=stdev(x),illustrative_sd50=stdev(y),
        illustrative_mean_difference_pp=mean(x)-mean(y),readme_mean_gate_pass=True,
        illustrative_90_ci=[mean(x)-mean(y)-ci90,mean(x)-mean(y)+ci90],
        conclusion="mean-only gate may pass while uncertainty crosses tolerance; D3-only evidence cannot establish finite-size equivalence of other diameters",
        length_per_AM_diameter=[40/6,50/6],
        am_to_se_diameter_ratios={str(d):6/d for d in (.7,1,2,3)}))
out=HERE/"probe_design_results.json"
out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"source_files_verified":len(source_hashes),"source_assertions":"passed",
 "am_number_fraction":number_am,"geometry":geometries,
 "ci90_halfwidth_pp":ci90,"ci95_halfwidth_pp":ci95,"output":str(out)},indent=2))
