"""Read-only artifact comparison and saved-data checks; never runs a solver."""
from pathlib import Path
import ast, csv, difflib, hashlib, json, subprocess, sys

R = Path(__file__).resolve().parent
OLD = R.parent / 'seminar_review_20261013'
S = OLD / 'sources/code'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
out = {'artifact_identity': {}, 'limitations': [
    'Original template and native PowerPoint rendering unavailable.',
    'No DEM, MPM, FV, network or campaign solver executed.',
    'Pixel content is inspected visually, not exhaustively certified by OCR.',
    'Selftest not executed: bundled runtime has no matplotlib; constants and CSVs independently checked.'
]}
for suffix in ['pptx', 'pdf']:
    name = f'seminar_20261013_draft.{suffix}'
    paths = {'previous': Path('C:/Users/Administrator/Downloads') / name,
             'v2': R / 'v2' / name, 'v3': R / 'v3' / name}
    hashes = {k: sha(p) for k, p in paths.items()}
    out['artifact_identity'][suffix] = {'sha256': hashes, 'identical': len(set(hashes.values())) == 1}
    assert len(set(hashes.values())) == 1

outline = Path('docs/seminar_20261013/outline_v1.md')
diff = ''.join(difflib.unified_diff((R/'v2'/outline).read_text(encoding='utf8').splitlines(True),
                                   (R/'v3'/outline).read_text(encoding='utf8').splitlines(True),
                                   fromfile='v2/outline_v1.md', tofile='v3/outline_v1.md'))
(R/'evidence/v2_to_v3_outline.diff').write_text(diff, encoding='utf8')
claims = json.loads((S/'docs/reviews/claims.json').read_text(encoding='utf8'))
patterns = [x.get('pattern') if isinstance(x,dict) else x for x in claims.get('quotation_ban',[])]
patterns = [x for x in patterns if x]
slides = json.loads((R/'evidence/v3_pptx.json').read_text(encoding='utf8'))['slides']
fields = {}
for s in slides:
    fields[f"pptx/slide{s['slide']}/body"] = '\n'.join(s['texts'])
    fields[f"pptx/slide{s['slide']}/notes"] = '\n'.join(s['notes'])
for p in (R/'v3/docs/seminar_20261013/figs').glob('*'):
    if p.suffix in ['.csv', '.svg']:
        fields[str(p.relative_to(R))] = p.read_text(encoding='utf8')
hits = [{'where': where, 'pattern': pat} for where,text in fields.items() for pat in patterns if pat in text]
out['literal_ban_scan'] = {'patterns': len(patterns), 'text_units': len(fields), 'hits': hits,
    'scope': 'PPTX text and notes, supplied figure CSV/SVG text. Raster figures require visual inspection.'}

# Read constants without importing plotting code or executing its self-reporting selftest.
figdir = R/'v3/docs/seminar_20261013/figs'
tree = ast.parse((figdir/'make_seminar_figs.py').read_text(encoding='utf8'))
constants = {}
for node in tree.body:
    if isinstance(node, ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0], ast.Name):
        name = node.targets[0].id
        if name in ['GRID','SIGMA_E_EXP','PS45']:
            constants[name] = {x.arg: ast.literal_eval(x.value) for x in node.value.keywords}
with (figdir/'F4_ps45_sigma_e.csv').open(encoding='utf-8-sig',newline='') as f:
    delivered = list(csv.reader(f))[1:]
with (S/'docs/data/ps45_sigmae_factor_off_20261013/factor_off_electronic.tsv').open(encoding='utf-8-sig',newline='') as f:
    source = list(csv.DictReader(f,delimiter='\t'))
source = {x['P_S']: x for x in source}
f4=[]
for label,val in delivered:
    raw = float(source[label]['main_sigma_ref_mScm'])
    q = float(source[label]['main_q']); ref=1000*float(source[label]['sigma_ref_S_cm'])
    f4.append({'label':label,'csv':float(val),'source':raw,'round3_matches':float(val)==round(raw,3),
               'q_times_reference_error':q*ref-raw})
    assert float(val)==round(raw,3)
out['F4_saved_data_recheck']=f4
out['F4_range_mScm']=[min(x['source'] for x in f4),max(x['source'] for x in f4)]
out['plot_constants']=constants
completed = subprocess.run([sys.executable,'-X','utf8','-B',str(OLD/'verify_results.py')],capture_output=True,text=True,encoding='utf8',check=True)
(R/'evidence/saved_data_recheck_stdout.txt').write_text(completed.stdout,encoding='utf8')
out['saved_data_recheck']={'exit_code':completed.returncode,'method':'Prior transparent read-only arithmetic script rerun on pinned saved data.'}
out['original_inputs_sha256']={str(p):sha(p) for p in [
    Path('C:/Users/Administrator/Downloads/seminar_20261013_codex_review_v2.zip'),
    Path('C:/Users/Administrator/Downloads/seminar_20261013_codex_review_v3.zip'),
    Path('C:/Users/Administrator/Downloads/codex_seminar_deck_review_request_20261013.md')]}
(R/'evidence/followup_checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(out,ensure_ascii=False,indent=2))
