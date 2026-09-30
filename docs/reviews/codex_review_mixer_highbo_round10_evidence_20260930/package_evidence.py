from pathlib import Path
import hashlib, json, shutil, zipfile

root=Path(__file__).resolve().parent
workspace=root.parent
report=workspace/'docs/reviews/codex_review_mixer_highbo_round10_20260930.md'
shutil.copyfile(report,root/'review.md')
status={
    'scope':'v2.6 round 10 Q1-Q4; no simulation or remote execution',
    'source_commit':'8e8474a68fa71216f3d4890b46a6cddb6380db66',
    'input_zip_sha256':'397ea3a16ab56e1947707502e99a8253bc5ad6e9e240ac81d92c32cdd3ad00aa',
    'Q1':'CONDITIONAL; report-only policy allowed; measurement-validity gate incomplete',
    'Q2':'ACCEPT AS DEVELOPMENT CANDIDATE ONLY; no measured safety margin',
    'Q3':'CONFIRMED within printed precision',
    'Q4':'ACCEPT within current single-insertion deck and source assumptions',
    'new_P1':0,
    'findings':[
        {'id':'HBR10-01','priority':'P2','status':'open','conclusion':'Missing/nonfinite report measurements accepted by producer/consumer boundary'},
        {'id':'HBR10-02','priority':'P2','status':'open','conclusion':'Global soft range does not implement documented unchanged AM-pair range'},
        {'id':'HBR10-03','priority':'P2','status':'open','conclusion':'Noise-only explanation and all-candidates-impossible claim not established'}],
    'confirmation_18':'HOLD; no production approval',
    'raw_DEV7_measurements_independently_reproduced':False,
    'production_files_modified':False,
    'simulation_or_remote_jobs_executed':False,
}
(root/'review_status.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
files=sorted(p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='MANIFEST.json')
manifest={str(p.relative_to(root)).replace('\\','/'):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
(root/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
out=workspace/'outputs/codex_mixer_highbo_round10_review_20260930.zip'
out.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
    for p in files+[root/'MANIFEST.json']:
        z.write(p,'codex_mixer_highbo_round10_review_20260930/'+p.relative_to(root).as_posix())
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
    for p,m in manifest.items():
        b=z.read('codex_mixer_highbo_round10_review_20260930/'+p)
        assert len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256']
print(json.dumps({'path':str(out),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'files_verified':len(manifest)},indent=2))
