"""Static deck closure, source and algebra probes. No simulation or deck edits."""
from pathlib import Path
import hashlib, json, math

R = Path(__file__).resolve().parents[1]
ppt = json.loads((R/'evidence/pptx.json').read_text(encoding='utf8'))
slides = ppt['slides']
body = lambda n: '\n'.join(slides[n-1]['texts'])
notes = lambda n: '\n'.join(slides[n-1]['notes'])
checks = {
 'slide_count_17':len(slides)==17,
 'servo_current_status_preserved_in_notes': all(s in notes(6) for s in ['DEM-seeded SE, stress-controlled servo','f = 0 completed; f(a) execution failed']),
 'not_one_validation_series_on_screen':'they are not one validation series' in body(6),
 'dataset_a_130_plus_64':'geometric tortuosity, 130 + 64' in body(10),
 'dataset_b_130':'(b) porosity, 130-bed set' in body(10),
 'dataset_nonspan_24':'24 non-percolating beds' in body(10),
 'young_bulk_moduli_separated':all(s in notes(5) for s in ['22.06','26.23','separate quantity']),
 'no_yield_strength_literature_band_on_screen':'range' not in body(6).lower(),
 'pending_validation_on_screen':'pending' in body(6),
 'zero_comparator_mislabel_present':'No NCM–NCM cohesion' in body(11),
 'physical_mixing_headline_present':'stronger cohesion lowers mixing' in body(12),
 'adhesion_unqualified_preference_present':'keeps like–like contacts best' in body(13),
}
assert all(checks.values()),checks
manifest=json.loads((R/'evidence/input_manifest.json').read_text(encoding='utf8'))
identity=[]
for entry in manifest['inventory']:
 if entry['path'] in ('seminar_20261013_v3.pdf','seminar_20261013_v3.pptx'):
  actual=hashlib.sha256((R/'input'/entry['path']).read_bytes()).hexdigest()
  assert actual==entry['sha256']
  identity.append(dict(path=entry['path'],sha256=actual))
figmeta=json.loads((R/'evidence/so_figures_source.json').read_text(encoding='utf8'))
src=(R/'input/repo/docs/seminar_20261013/build_seminar_v3.py').read_text(encoding='utf8')
assert 'so2021_dem_fabrication_degradation_ductile_particles/fig_4.png' in src
assert 'J. Power Sources 508, 230344' in body(6)
assert '030538.pdf' in figmeta['sources'][0]

# Restricted spherical JKR scaling, same small-particle weight and work W.
size_counterexamples=[]
for ra in (4.5,2.0):
 rs=.5
 rstar_as=ra*rs/(ra+rs)
 rstar_ss=rs/2
 factor=rstar_as/rstar_ss
 size_counterexamples.append(dict(r_NCM_um=ra,r_SE_um=rs,
   equal_W_F_AS_over_F_SS=factor,
   geometric_mean_gamma_ratio_for_equal_force=1/factor**2))
# W has units J/m^2. Equal contact area is required to turn the
# per-area identity into a total energy-release identity.
ga,gs=4.0,1.0
waa,wss,was=2*ga,2*gs,2*math.sqrt(ga*gs)
delta_work=waa+wss-2*was
assert delta_work==2*(math.sqrt(ga)-math.sqrt(gs))**2==2.0
counter=dict(gamma_A=ga,gamma_S=gs,W_AA=waa,W_SS=wss,W_AS=was,
  per_area_delta_W=delta_work,
  assumed_contact_areas=dict(AA=.1,SS=.1,AS1=1.,AS2=1.),
  adhesive_energy_release=waa*.1+wss*.1-was*2,
  status='synthetic algebra counterexample, not a measured bed')
assert counter['adhesive_energy_release']==-7.
report={'input_identity':identity,'static_checks':checks,
 'so_source':{'figure_src':figmeta['sources'][0],'deck_citation':'J. Power Sources 508, 230344 (2021)',
 'correct_source':'J. Electrochem. Soc. 168, 030538 (2021), DOI 10.1149/1945-7111/abed23'},
 'adhesion_size_counterexamples':size_counterexamples,
 'equal_area_counterexample':counter,
 'SE_SS_over_large_NCM_AA_Bo_at_equal_W':4.8/2.0*9**2}
(R/'evidence/root_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(report,ensure_ascii=False,indent=2))
