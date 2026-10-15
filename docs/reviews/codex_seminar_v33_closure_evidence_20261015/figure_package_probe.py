"""Independent checks of delivered package and plotted coordinates, no producer import."""
from pathlib import Path
import csv, hashlib, json, re, zipfile, posixpath, difflib
from lxml import etree as E
from PIL import Image

R=Path(__file__).resolve().parent
P=R/'input'; EV=R/'evidence'; BASE=R/'baseline'
F=P/'repo/docs/seminar_20261013/figs_v3'
for name in ['F_p4.csv','F_p4.svg','F_p4.png']:
    assert (BASE/name).is_file(), f'Missing packaged baseline: {name}'
sha=lambda b:hashlib.sha256(b).hexdigest()
NS={'s':'http://www.w3.org/2000/svg','x':'http://www.w3.org/1999/xlink'}
def byid(root,name): return root.xpath('//*[@id=$v]',v=name)[0]
def points(path):
    a=[float(x) for x in re.findall(r'-?\d+(?:\.\d+)?(?:e[-+]?\d+)?',path.get('d'),re.I)]
    return list(zip(a[::2],a[1::2]))
def coordinate_data(file):
    root=E.parse(str(file)); result={}
    for no,patches in [(1,['patch_3','patch_4','patch_5']),(2,['patch_9','patch_10'])]:
        axis=byid(root,'axes_'+str(no)); ticks=[]
        for tick in axis.xpath('.//s:g[starts-with(@id,"ytick_")]',namespaces=NS):
            use=tick.xpath('.//s:use',namespaces=NS)[0]
            label=''.join(tick.xpath('.//s:text//text()',namespaces=NS))
            ticks.append((float(use.get('y')),float(label)))
        y0,v0=ticks[0]; y1,v1=ticks[-1]
        def value(y): return v0+(y-y0)*(v1-v0)/(y1-y0)
        bars=[]
        for name in patches:
            path=byid(root,name).find('s:path',NS)
            pts=points(path)
            bars.append({'path_id':name,'value_from_geometry':value(min(y for x,y in pts)),
                         'baseline':value(max(y for x,y in pts)),'style':path.get('style')})
        frame=axis.find('s:g/s:path',NS)
        result['panel_'+str(no)]={'ticks':ticks,'bars':bars,'ylim_from_frame':[value(max(y for x,y in points(frame))),value(min(y for x,y in points(frame)))]}
        if no==2:
            group=byid(root,'FillBetweenPolyCollection_1')
            path=group.find('s:defs/s:path',NS); use=group.find('s:g/s:use',NS)
            ys=sorted(set(y+float(use.get('y')) for x,y in points(path)))
            result['band']=sorted(value(y) for y in ys)
            line=byid(root,'LineCollection_1').find('s:path',NS)
            result['band_point']=value(points(line)[0][1])
    pats=root.xpath('//s:pattern',namespaces=NS)
    whole=E.tostring(root).decode()
    result['hatches']=[]
    for pat in pats:
        ident=pat.get('id'); count=whole.count('url(#'+ident+')'); pat.set('id','PATTERN')
        result['hatches'].append({'body':E.tostring(pat,method='c14n').decode(),'uses':count})
    a=E.tostring(byid(root,'axes_1'),method='c14n').decode()
    a=re.sub(r'#[a-z][0-9a-f]{10}', '#ID',a)
    result['panel_a_normalized']=re.sub(r'id="[a-z][0-9a-f]{10}"', 'id="ID"',a)
    result['labels']=[''.join(t.itertext()) for t in root.xpath('//s:text',namespaces=NS)]
    return result
old=coordinate_data(BASE/'F_p4.svg'); new=coordinate_data(F/'F_p4_v33.svg')
def rows(path):
    with path.open(encoding='utf-8',newline='') as f: return list(csv.DictReader(f))
oc,nc=rows(BASE/'F_p4.csv'),rows(F/'F_p4_v33.csv')
cmp=[]
for a,b in zip(oc,nc):
    cmp.append({'old_state':a['state'],'new_state':b['state'],
                'data_unchanged':{k:v for k,v in a.items() if k!='state'}=={k:v for k,v in b.items() if k!='state'}})
chart={'old':old,'new':new,'csv_count_equal':len(oc)==len(nc),'csv':cmp,
       'panel_a_identical_normalized':old['panel_a_normalized']==new['panel_a_normalized'],
       'hatches_same':old['hatches']==new['hatches'],
       'png_dimensions_old':Image.open(BASE/'F_p4.png').size,
       'png_dimensions_new':Image.open(F/'F_p4_v33.png').size}
(EV/'figure_normalized.diff').write_text(''.join(difflib.unified_diff(old['panel_a_normalized'].splitlines(True),new['panel_a_normalized'].splitlines(True),fromfile='old',tofile='new')),encoding='utf-8')
for data in (old,new): data.pop('panel_a_normalized')
expected=[[300.906,165.34,299.274],[14.953,10.769]]
for data in (old,new):
    for panel,values in enumerate(expected,1):
        for row,val in zip(data['panel_'+str(panel)]['bars'],values): assert abs(row['value_from_geometry']-val)<1e-4
    assert max(abs(x-y) for x,y in zip(data['band'],[8.3,11.7]))<1e-5
    assert abs(data['band_point']-10)<1e-5
assert chart['csv_count_equal'] and all(x['data_unchanged'] for x in cmp)
(EV/'figure_debug.json').write_text(json.dumps(chart,ensure_ascii=False,indent=2),encoding='utf-8')
assert chart['hatches_same'] and chart['panel_a_identical_normalized']
req=(P/'codex_seminar_deck_v3_3_closure_request_20261015.md').read_text(encoding='utf-8')
entries=[]
for digest,sz,rel in re.findall(r'^([0-9a-f]{64})\s+(\d+)\s+(.+)$',req,re.M):
    fp=P/rel.strip(); entries.append({'path':rel.strip(),'bytes_match':fp.stat().st_size==int(sz),'sha_match':sha(fp.read_bytes())==digest})
intake=json.loads((EV/'intake.json').read_text(encoding='utf-8'))
covered={x['path'] for x in entries}|{'codex_seminar_deck_v3_3_closure_request_20261015.md','MANIFEST.sha256'}
package={'request_entries':entries,'request_exact_member_set':covered=={x['path'] for x in intake['members']}}
assert package['request_exact_member_set'] and all(x['bytes_match'] and x['sha_match'] for x in entries)
out={'chart':chart,'package':package,'scope':'Delivered SVG coordinates/CSV/ZIP; no solver or producer execution.'}
(EV/'figure_package_probe.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'chart_panels_equal_in_data_units':True,'band_old':old['band'],'band_new':new['band'],
                  'ylim_old':old['panel_2']['ylim_from_frame'],'ylim_new':new['panel_2']['ylim_from_frame'],
                  'hatches_same':chart['hatches_same'],'request_exact_member_set':package['request_exact_member_set'],
                  'request_entries_checked':len(entries)},ensure_ascii=False,indent=2))
