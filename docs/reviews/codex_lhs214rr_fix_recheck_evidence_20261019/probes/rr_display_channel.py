"""Follow-up: inspect final page after channel-only metadata mutation.

Consumes numeric agent's four fresh synthetic producer fixtures read-only;
copies into this subtask's cases, uses actual network projection and loader.
Only adapter is code_sha during provenance stamping, avoiding Git operations.
"""
import contextlib
import csv
import hashlib
from html.parser import HTMLParser
import io
import json
import os
from pathlib import Path
import shutil
import sys

review=Path(__file__).resolve().parents[1]
work=review/'evidence/rr_display_channel_work'
for key,name in [('WEBAPP_RESULTS_FOLDER','results'),('WEBAPP_UPLOAD_FOLDER','uploads'),
                 ('WEBAPP_ARCHIVE_FOLDER','archive'),('WEBAPP_MPM_LAB_FOLDER','mpm'),('MPLCONFIGDIR','mpl')]:
    os.environ[key]=str(work/name)
sys.path[:0]=[str(review/'source/webapp'),str(review/'source/scripts')]
quiet=io.StringIO()
with contextlib.redirect_stdout(quiet): import app
import pipeline_service as ps
app.app.config.update(TESTING=True,PROPAGATE_EXCEPTIONS=False)

class Rows(HTMLParser):
    def __init__(self): super().__init__(); self.rows=[];self.row=self.cell=None
    def handle_starttag(self,t,a):
        if t=='tr':self.row=[]
        if t=='td' and self.row is not None:self.cell=[]
    def handle_data(self,d):
        if self.cell is not None:self.cell.append(d)
    def handle_endtag(self,t):
        if t=='td' and self.cell is not None:self.row.append(''.join(self.cell).strip());self.cell=None
        if t=='tr' and self.row is not None:
            if self.row:self.rows.append(self.row)
            self.row=None

inputs=json.loads((review/'evidence/rr_numeric_scope.json').read_text(encoding='utf-8'))
cases={'baseline':inputs['baseline'],**inputs['channel_mutants']}
out={}
for name,detail in cases.items():
    src=Path(detail['folder']);rd=work/'results'/name;ud=work/'uploads'/name
    rd.mkdir(parents=True,exist_ok=True);ud.mkdir(parents=True,exist_ok=True)
    sha0={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in src.iterdir() if p.is_file()}
    for filename in ('full_metrics.json','network_conductivity_dual.json','network_conductivity_hertzian.json',
                     'network_conductivity.json','network_conductivity_physics.json'):
        shutil.copy2(src/filename,rd/filename)
    (ud/'meta.json').write_text(json.dumps({'name':name,'status':'done','scale':1}),encoding='utf-8')
    with (rd/'network_summary.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f);w.writerow(['metric','value']);w.writerow(['SE Volume Fraction',.4886921905584123])
    rid='rr-display-channel-'+name
    projection=app._network_projection(str(rd),rid)
    if projection.get('error'):raise RuntimeError(projection)
    (rd/'full_metrics.json').write_text(json.dumps(projection['fm'],ensure_ascii=False),encoding='utf-8')
    old_sha=ps.code_sha
    ps.code_sha=lambda root=None:'77d8fd44545c33cd10ab18fc250c7ad3023833ea'
    try:ps.stamp_network_provenance(str(rd),rid)
    finally:ps.code_sha=old_sha
    with contextlib.redirect_stdout(quiet):
        tables,metrics,_=app._load_case_tables(str(rd),{})
        response=app.app.test_client().get('/single/'+name)
    html=response.get_data(as_text=True);parser=Rows();parser.feed(html)
    (work/(name+'.html')).write_text(html,encoding='utf-8')
    selected={r[0]:r[1:] for r in parser.rows if r and (r[0].startswith('σ_ionic — full') or r[0].startswith('σ_ionic network state') or r[0].startswith('tau2 handover status') or r[0].startswith('Network generation contract'))}
    sha1={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in src.iterdir() if p.is_file()}
    out[name]=dict(http=response.status_code,selected=selected,loader=tables['network_summary']['data'],
        channel_projection=projection['chv'],fm_status=metrics.get('sigma_full_status'),fm_sigma=metrics.get('sigma_full_mScm'),
        generation_problem=metrics.get('network_generation_problem'),original_fixture_unchanged=sha0==sha1)
baseline=out['baseline']
summary={k:dict(http=v['http'],selected=v['selected'],channel_projection=v['channel_projection'],
               same_selected_as_baseline=v['selected']==baseline['selected'],same_full_loader_as_baseline=v['loader']==baseline['loader'],
               original_fixture_unchanged=v['original_fixture_unchanged']) for k,v in out.items()}
(review/'evidence/rr_display_channel.json').write_text(json.dumps({'results':out,'summary':summary},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False))
