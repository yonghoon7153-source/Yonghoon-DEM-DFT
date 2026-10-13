"""Independent identity, actual embedded media and closure checks. No author code execution."""
from pathlib import Path
import hashlib, json, re
import pdfplumber
from PIL import Image, ImageChops

R=Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
inv=json.loads((R/'evidence/input_manifest.json').read_text(encoding='utf8'))
deck=json.loads((R/'evidence/pptx.json').read_text(encoding='utf8'))
slides=deck['slides']
body=lambda i: '\n'.join(slides[i-1]['texts'])
notes=lambda i: '\n'.join(slides[i-1]['notes'])
manifest=(R/'input/MANIFEST.md').read_text(encoding='utf8')
declared=[]
for hash_value,name in re.findall(r'^([a-f0-9]{64})  \./(.+)$',manifest,re.M):
    p=R/'input'/name
    assert p.is_file(),name
    assert sha(p)==hash_value,name
    declared.append(name)
assert sha(R/'input/deck/seminar_20261013_v3_1.pptx')=='73fa2dc3b5629eabb9ec744b47495512db477dd962753a003820ad02b525401b'
assert sha(R/'input/deck/seminar_20261013_v3_1.pdf')=='5335e3fe61715eff556258dbb50946174a3d7b043db02a341294bf6107eaf474'

figroot=R/'input/repo/docs/seminar_20261013/figs_v3'
expected={3:'F_poro',4:'F_trans',7:'F_vgcf',8:'F_limits',9:'F_load',10:'F_dataset',11:'F_mix1',12:'F_mix2',13:'F_mix3'}
media=[]
for page,name in list(expected.items())+[(13,'F_mix3_scheme')]:
    h=sha(figroot/f'{name}.png')
    assert h in [x['sha256'] for x in slides[page-1]['media']],(page,name)
    media.append(dict(page=page,figure=name,sha256=h,embedded_exact_match=True))
so=R/'input/lit/so2021_dem_fabrication_degradation_ductile_particles/fig_4.png'
old_crop=Image.open(R/'evidence/so_v3_crop.png').convert('RGB')
new_crop=Image.open(R/'input/lit/so2021_fig4a_crop.png').convert('RGB')
original_so=Image.open(so).convert('RGB')
same_so=(ImageChops.difference(old_crop,new_crop.crop((0,0,*old_crop.size))).getbbox() is None
         and ImageChops.difference(new_crop,original_so.crop((0,0,*new_crop.size))).getbbox() is None)
assert same_so
crop_sha=sha(R/'input/lit/so2021_fig4a_crop.png')
assert crop_sha in [x['sha256'] for x in slides[5]['media']]

checks={
 '01_correct_JES_source_p6_p16':all('J. Electrochem. Soc. 168, 030538 (2021)' in body(i) for i in (6,16)),
 '02_nonzero_comparator_in_actual_notes':'small but nonzero' in notes(11) and '108,795' in notes(11),
 '02_no_zero_mislabel_body':not any(x in '\n'.join(body(i) for i in (11,12,13)).lower() for x in ('no ncm–ncm cohesion','non-cohesive','cohesion removed')),
 '03_diagnostic_qualifier_visible':'the original 1% overlap condition was not met' in body(11),
 '03_summary_unresolved':'unresolved diagnostic mixing-index contrast' in body(15),
 '04_Bo_CED_separated':'model Bond number 38.4, 384, 1152' in body(12) and 'cohesion-energy densities' in body(12),
 '04_posthoc_no_verdict':'post hoc' in body(12) and 'no verdict' in body(12),
 '05_assumptions_visible':'assumed geometric-mean adhesion rule' in body(13) and 'equal contact areas' in body(13),
 '05_per_area_units_in_notes':'J m⁻²' in notes(13),
 '05_cluster_survival_not_force_criterion':'not a necessary or sufficient condition' in notes(13),
 '07_10GPa_100GPa_separated':'VGCF E = 10 GPa' in body(7) and '100 GPa replication' in notes(7),
 '08_experimental_rank':'experimental porosity summaries' in body(9),
 '10_implementation_qualified':'Our fixed-shape implementation' in body(5),
 '10_random_reference':'M = 1: random-reference variance' in body(11),
 '10_no_unsupported_sigma_y_band':'inside the literature range' not in notes(6),
}
assert all(checks.values()),checks
with pdfplumber.open(R/'input/deck/seminar_20261013_v3_1.pdf') as pdf:
    assert len(pdf.pages)==len(slides)==17
    source_bounds=[]
    for i in (11,12,13):
        page=pdf.pages[i-1]
        words=[w for w in page.extract_words() if 66<w['top']<90]
        edge=max(w['x1'] for w in words)
        assert edge<page.width
        source_bounds.append(dict(page=i,width_pt=page.width,right_edge_pt=edge,right_margin_pt=page.width-edge,text=' '.join(w['text'] for w in words)))

out=dict(archive=inv['archive'],verified_declared_manifest_files=len(declared),slides=17,pages=17,
         pptx_sha256=sha(R/'input/deck/seminar_20261013_v3_1.pptx'),pdf_sha256=sha(R/'input/deck/seminar_20261013_v3_1.pdf'),
         closure_checks=checks,actual_PPTX_chart_media=media,So_crop_prefix_pixels_match_previous_and_original=same_so,
         So_crop_dimensions=dict(old=old_crop.size,new=new_crop.size,original=original_so.size),
         actual_PPTX_So_crop_sha256=crop_sha,source_line_bounds=source_bounds,
         note='Checks support targeted closure only. Producer selftests not run. Visual review and numeric audit remain separate.')
(R/'evidence/closure_checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(out,ensure_ascii=False,indent=2))
