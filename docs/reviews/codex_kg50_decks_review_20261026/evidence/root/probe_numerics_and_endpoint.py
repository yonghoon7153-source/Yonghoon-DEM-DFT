"""Read-only arithmetic/source probe. No DEM, MPI, WSL or launcher execution."""
from pathlib import Path
import json, math, re, hashlib
ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT / "snapshot" / "repo"
HERE = Path(__file__).resolve().parent
deck_path = REPO / "docs/data/kg50_decks_20261026/kg50_d07_b40/input_kg50_d07_b40.liggghts"
deck = deck_path.read_text(encoding="utf-8-sig")
vis = (HERE / "sources/fix_viscous.cpp").read_text(encoding="utf-8-sig")
nve = (HERE / "sources/fix_nve_sphere.cpp").read_text(encoding="utf-8-sig")
base = (HERE / "sources/fix_nve.cpp").read_text(encoding="utf-8-sig")
assert "f[i][0] -= drag*v[i][0]" in vis
assert "mask |= POST_FORCE" in vis
assert nve.count("v[i][0] += dtfm * f[i][0]") == 2
assert "dtf = 0.5 * update->dt * force->ftm2v" in base
assert re.search(r"^fix damp all viscous 0.5$", deck, re.M)
assert re.search(r"^variable dt\s+equal 1.0e-6$", deck, re.M)
assert "density constant 1640 radius constant \u0024{r_SE}" in deck
rows=[]
for d in (0.7,1.0,2.0,3.0):
    r=d/2*1e-3 # deck SI metres = real micrometres * 1e-3
    mass=1640*4/3*math.pi*r**3
    gamma=0.5
    alpha=gamma*1e-6/mass
    rows.append(dict(SE_D_real_um=d,SE_r_deck_m=r,mass_deck_kg=mass,
                     drag_time_s=mass/gamma,alpha_dt_gamma_over_m=alpha,
                     drag_only_halfstep_multiplier=1-alpha,
                     multiplier_dt_half=1-alpha/2,
                     drag_only_absolute_stability_limit_dt_s=2*mass/gamma,
                     pure_drag_continuum_factor_at_dt=math.exp(-alpha)))
assert 1 < rows[0]["alpha_dt_gamma_over_m"] < 2
assert all(row["alpha_dt_gamma_over_m"]<1 for row in rows[1:])
assert re.search(r"dump dmp_atom all custom 50000", deck)
assert re.search(r"dump dmp_contact all local 10000", deck)
assert re.search(r"run 100000\s+print \"====== Simulation Finished", deck)
for forbidden in ("write_dump", "dump_modify", "write_restart restart_kg50_d07_b40/restart_final"):
    assert forbidden not in deck
schedule=[]
for k in range(1010,1021):
    c=400002+5000*k
    final=c+100000
    atom=final//50000*50000
    contact=final//10000*10000
    old_atom=final//5000*5000
    schedule.append(dict(compression_loops=k,compression_end=c,final_step=final,
        atom_step=atom,contact_step=contact,last_common_step=atom,
        atom_age_steps=final-atom,relaxation_steps_at_last_common=atom-c,
        legacy_atom_age_steps=final-old_atom,
        legacy_last_common_age_steps=final-contact))
assert next(s for s in schedule if s["compression_loops"]==1019)["atom_age_steps"]==45002
files=[deck_path,*sorted((HERE/"sources").glob("*.cpp"))]
result=dict(kind="algebraic source-backed counterexamples; no physical simulation",
    assertions_passed=True,drag=rows,sampling=schedule,
    critical_diameter_real_um_for_alpha_2=2*(0.5*1e-6/(2*1640*4/3*math.pi))**(1/3)*1000,
    source_pin="3d5c00f20519e6bb6eb6756f51f1ad36564e649d",
    sources=[dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in files])
(HERE/"root_probe_results.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
print(json.dumps(dict(assertions_passed=True,drag=rows,sampling_example=schedule[9],critical_diameter_real_um_for_alpha_2=result["critical_diameter_real_um_for_alpha_2"]),indent=2))

