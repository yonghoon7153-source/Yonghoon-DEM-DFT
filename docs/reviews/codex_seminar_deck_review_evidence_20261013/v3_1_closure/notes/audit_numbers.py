"""Read-only closure arithmetic. Only this audit's JSON output is written.

Run with bundled Python: python notes/audit_numbers.py
Uses the retained previous independent raw readouts, not delivered generators.
"""
import csv
import hashlib
import json
import math
import re
import statistics
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / 'evidence/numeric_inputs'
FIG = ROOT / 'input/repo/docs/seminar_20261013/figs_v3'
OLD_FIG = OLD / 'input/repo/docs/seminar_20261013/figs_v3'
S = '{http://www.w3.org/2000/svg}'
result = {'csv': {}, 'raw_mixing': {}, 'svg': {}, 'provenance': {}}

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def rows(p):
    return list(csv.reader(p.read_text(encoding='utf-8-sig').splitlines()))

def obj(p):
    return json.loads(p.read_text(encoding='utf-8'))

def numeric(x):
    try:
        return float(x)
    except ValueError:
        return None

for p in sorted(FIG.glob('*.csv')):
    before, after = rows(OLD_FIG / p.name), rows(p)
    assert len(before) == len(after)
    numeric_changes, other_changes = [], []
    for r, (old, new) in enumerate(zip(before, after), 1):
        assert len(old) == len(new)
        for c, (a, b) in enumerate(zip(old, new), 1):
            if a == b:
                continue
            av, bv = numeric(a), numeric(b)
            item = {'row': r, 'col': c, 'old': a, 'new': b}
            if av is not None and bv is not None:
                if math.isnan(av) and math.isnan(bv):
                    continue
                item['three_decimal_changes'] = round(av, 3) != round(bv, 3)
                numeric_changes.append(item)
            else:
                other_changes.append(item)
    result['csv'][p.stem] = {
        'rows_without_header': len(after)-1,
        'old_sha256': sha(OLD_FIG / p.name), 'new_sha256': sha(p),
        'numeric_changes': numeric_changes, 'label_changes': other_changes,
    }
for name in ('F_poro','F_trans','F_limits','F_load','F_vgcf','F_dataset'):
    assert result['csv'][name]['old_sha256'] == result['csv'][name]['new_sha256']

# Recalculate development delta M from saved per-frame variances.
RAW = OLD / 'sources_mixing/docs/data'
bo = RAW / 'mixer_highbo_devbo_prelim_20261003'
u = RAW / 'mixer_highbo_devu_prelim_20261006'
grids = {'16×16×4': '16x4', '12×12×3': '12x3', '8×8×2': '8x2'}
names = {'NCM-pair Bo 38.4':'LH_ref_r2_s32452843',
         'NCM-pair Bo 384':'LHx10_ref_r2_s32452843',
         'NCM-pair Bo 1152':'LHx30_ref_r2_s32452843',
         'All-pair CED ×10':'LU212_ref_r2_s32452843',
         'All-pair CED ×14.42':'LU637_ref_r2_s32452843'}
repro = []
for setting, grid, submitted, note in rows(FIG/'F_mix2.csv')[1:]:
    folder, prefix = (u, 'devu') if setting.startswith('All-') else (bo, 'devbo')
    p = folder / f'{prefix}_c{grids[grid]}.json'
    records = {r['provenance']['run']['name']: r for r in obj(p)}
    def m(rec):
        frames = [r for r in rec['rows'] if math.floor(r['rev']) == rec['planned']['final_bin']]
        assert len(frames) == rec['planned']['expected']
        values = [(rec['S0']-r['s2'])/(rec['S0']-rec['SR']) for r in frames]
        return sum(values)/len(values)
    recomputed = m(records['LC_ref_r2_s32452843']) - m(records[names[setting]])
    assert abs(float(submitted)-recomputed) < 1e-12
    repro.append({'setting':setting, 'grid':grid, 'source':str(p.relative_to(OLD)),
                  'frame_based_delta':recomputed, 'csv':float(submitted),
                  'three_decimals':f'{recomputed:.3f}'})
result['raw_mixing']['F_mix2'] = repro

raw = [r for r in obj(u / 'devu_contact.json')['runs'] if r.get('bin',{}).get('mean')]
cluster = []
for row, rec in zip(rows(FIG/'F_mix3.csv')[1:], raw):
    if not rec.get('bin',{}).get('mean'):
        continue
    frames = rec['bin']['frames']
    assert len(frames) == 100
    mean = sum(x['s1_se_clusters']['se_frac_in_clusters'] for x in frames)/len(frames)
    lo = sum(x['resolution']['lo']['se_frac_in_clusters'] for x in frames)/len(frames)
    hi = sum(x['resolution']['hi']['se_frac_in_clusters'] for x in frames)/len(frames)
    assert max(abs(a-float(b)) for a,b in zip((mean,lo,hi),row[1:])) < 1e-12
    cluster.append({'setting':row[0], 'frames':len(frames), 'recomputed':[mean,lo,hi],
                    'three_decimals':[f'{v:.3f}' for v in (mean,lo,hi)]})
assert len(cluster)==3
result['raw_mixing']['F_mix3'] = cluster

# Decode plotted bar heights using SVG tick coordinates, not plotting constants.
def svg_bars(path):
    root = ET.parse(path).getroot()
    axes = root.find(f'.//{S}g[@id="axes_1"]')
    ticks = []
    for g in axes.findall(f'{S}g/{S}g'):
        if not g.get('id','').startswith('ytick_'):
            continue
        text = ''.join(g.find(f'.//{S}text').itertext()).replace('−','-')
        tick = next(q for q in g.findall(f'.//{S}use') if 'y' in q.attrib)
        ticks.append((float(text),float(tick.get('y'))))
    (v0,y0),(v1,y1) = ticks[:2]
    slope = (v1-v0)/(y1-y0)
    for v,y in ticks:
        assert abs(v-(v0+(y-y0)*slope)) < 1e-7
    found=[]
    for g in axes.findall(f'{S}g'):
        if not g.get('id','').startswith('patch_'):
            continue
        p=g.find(f'{S}path')
        if p is None or 'clip-path' not in p.attrib:
            continue
        pairs=re.findall(r'[ML]\s+([\d.eE+-]+)\s+([\d.eE+-]+)',p.get('d'))
        if len(pairs)!=4:
            continue
        pts=[(float(x),float(y)) for x,y in pairs]
        top=pts[2][1]
        found.append({'x':(pts[0][0]+pts[1][0])/2,'top':top,
                      'value':v0+(top-y0)*slope})
    return found

for name,col,tol in [('F_mix1',2,1e-7),('F_mix2',2,1e-7),('F_mix3',1,1e-7)]:
    bars=svg_bars(FIG/f'{name}.svg')
    targets=[float(r[col]) for r in rows(FIG/f'{name}.csv')[1:]]
    assert len(bars)==len(targets)
    diffs=[abs(a['value']-b) for a,b in zip(bars,targets)]
    assert max(diffs)<tol
    result['svg'][name]={'bars':len(bars),'max_abs_coordinate_decode_error':max(diffs),
                         'values_decoded':[r['value'] for r in bars], 'csv':targets}

# Actual delivered PPTX text and notes, not author claims/checker results.
slides=obj(ROOT/'evidence/pptx.json')['slides']
def full(n):
    s=slides[n-1]
    return '\n'.join(s['texts']), '\n'.join(s['notes'])
p7,n7=full(7)
p9,n9=full(9)
p12,n12=full(12)
p13,n13=full(13)
assert 'VGCF E = 10 GPa' in p7
assert '100 GPa replication' in n7 and 'not the 100 GPa means' in n7
assert 'experimental porosity summaries' in p9
assert all(v in n12 for v in ('+0.927','+0.865'))
assert '0.400 [0.143, 0.542]' in n13
result['provenance']['p7']={'original_10GPa_visible':True,'100GPa_replication_separate_in_notes':True}
result['provenance']['p9']={'experimental_porosity_qualifier_visible':True,'n5_exploratory_visible':'n = 5' in p9}
result['provenance']['rounds_actual_ppt_notes']={'p12_0927':True,'p12_0865':True,'p13_0400':True}

# Original 96-primary-arm generation, independently recomputed means.
original=obj(OLD/'notes/sources/phase_a_original_primary96.json')['files']
groups={}
for entry in original:
    a=entry['raw']
    groups.setdefault((a['vox'],a['vgcf_wt']),[]).append(a['sigma_e']*1000)
vg=[]
for voxel,wt,chart in rows(FIG/'F_vgcf.csv')[1:]:
    key=(float(voxel),float(wt))
    vals=groups[key]
    assert len(vals)==8
    mean=statistics.mean(vals)
    assert round(mean,2)==float(chart)
    vg.append({'voxel_um':key[0],'wt_pct':key[1],'n':8,'mean_mScm':mean,'chart_mScm':float(chart)})
result['provenance']['vgcf_original_means']=vg

# Compare source metadata and overlapping actual pixels. The old package only
# delivered a crop, not the full So source PNG, so do not claim full-file identity.
new_so=ROOT/'input/lit/so2021_dem_fabrication_degradation_ductile_particles/fig_4.png'
assert obj(OLD/'evidence/so_figures_source.json')==obj(new_so.parent/'figures.json')
from PIL import Image
im=Image.open(new_so)
oldcrop=Image.open(OLD/'input/lit/so2021_fig4a_crop.png')
newcrop=Image.open(ROOT/'input/lit/so2021_fig4a_crop.png')
assert oldcrop.size==(int(im.width*.475),im.height)
assert newcrop.size==(int(im.width*.515),im.height)
assert im.crop((0,0,oldcrop.width,im.height)).tobytes()==oldcrop.tobytes()
assert im.crop((0,0,newcrop.width,im.height)).tobytes()==newcrop.tobytes()
p6,n6=full(6)
p16,n16=full(16)
assert 'J. Electrochem. Soc. 168, 030538 (2021)' in p6
assert '[9] M. So et al., J. Electrochem. Soc. 168, 030538 (2021)' in p16
result['provenance']['so_full_figure']={'sha256':sha(new_so),'old_crop_pixels_unchanged':True,
                                      'new_crop_exact_full_source_subregion':True,
                                      'old_crop_size':oldcrop.size,'new_crop_size':newcrop.size,
                                      'p6_ref9_agree':True}

out=ROOT/'evidence/numeric_closure.json'
result['reference_input_sha256']={str(p.relative_to(OLD)):sha(p) for p in sorted(OLD.rglob('*')) if p.is_file()}
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'out':str(out),'unchanged_six_csv':True,
                  'mix2_frame_based':len(repro),'mix3_frame_based':len(cluster),
                  'svg_bar_counts':{k:v['bars'] for k,v in result['svg'].items()}},ensure_ascii=False))
