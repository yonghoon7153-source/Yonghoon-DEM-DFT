"""Read-only NPZ postprocessing; geometric cell overlap is not physical contact.

Point estimate: one center quadrature sample per material cell, weighted by its
current area / number of cells strictly containing that center. At least two
different carried particle IDs must contain the center. The estimate can miss
sub-cell overlaps. Cell metric: area of the union of all distinct-ID pairwise
intersections, so a triple intersection is counted once. No solver is imported.
"""
import argparse,csv,hashlib,json
from pathlib import Path
import numpy as np
import shapely
from shapely import Polygon,STRtree,points,unary_union

def need(ok,why):
    if not ok:raise ValueError(why)

def cells(data):
    x=np.asarray(data['x']);ids=np.asarray(data['particle_id']);pid=np.asarray(data['point_id'])
    f=np.asarray(data['F_total']);a=np.asarray(data['reference_area']);n=len(x)
    need(n>0 and x.shape==(n,2) and ids.shape==pid.shape==a.shape==(n,) and f.shape==(n,2,2),'frame shape')
    need(ids.dtype.kind in 'iu' and pid.dtype.kind in 'iu' and len(np.unique(pid))==n,'carried IDs')
    need(all(np.isfinite(t).all() for t in (x,f,a)) and np.all(a>0),'finite positive geometry')
    need(np.all(np.linalg.det(f)>0),'inverted or collapsed cell')
    offsets=np.sqrt(a)[:,None,None]*np.array([[-.5,-.5],[.5,-.5],[.5,.5],[-.5,.5]])
    quads=x[:,None,:]+np.einsum('nij,nkj->nki',f,offsets)
    polygons=np.array([Polygon(q) for q in quads],dtype=object)
    need(all(p.is_valid and p.area>0 for p in polygons),'invalid cell geometry')
    return x,ids,polygons

def group_overlap(polygons,ids):
    labels=np.unique(ids);groups=[unary_union(polygons[ids==i]) for i in labels]
    pair={};pieces=[]
    for i in range(len(groups)):
        for j in range(i+1,len(groups)):
            g=groups[i].intersection(groups[j]);pair[str(int(labels[i]))+':'+str(int(labels[j]))]=g.area
            if not g.is_empty:pieces.append(g)
    return groups,unary_union(pieces),pair

def measure_frame(data,stroke_width=0.0):
    need(np.isfinite(stroke_width) and stroke_width>=0,'stroke width')
    x,ids,polygons=cells(data);areas=np.array([p.area for p in polygons])
    groups,overlap,pair=group_overlap(polygons,ids);whole=unary_union(groups)
    query=points(x);hits=STRtree(polygons).query(query,predicate='within')
    counts=np.bincount(hits[0],minlength=len(x));need(np.all(counts>0),'center is not inside its carried cell')
    group_hits=STRtree(groups).query(query,predicate='within')
    distinct=np.bincount(group_hits[0],minlength=len(x));flags=distinct>=2
    estimate=float(np.sum(areas[flags]/counts[flags]))
    within_raw=float(areas.sum()-sum(g.area for g in groups));between_raw=float(sum(g.area for g in groups)-whole.area)
    need(within_raw>=-1e-10 and between_raw>=-1e-10,'invalid area accounting')
    drawn=overlap
    if stroke_width:
        expanded=np.array([p.buffer(stroke_width/2,join_style='mitre',mitre_limit=4) for p in polygons],dtype=object)
        _,drawn,_=group_overlap(expanded,ids)
    nearest=None
    for i,a in enumerate(np.unique(ids)):
        for b in np.unique(ids)[i+1:]:
            distances=np.sum((x[ids==a,None,:]-x[None,ids==b,:])**2,axis=2)
            v=float(np.sqrt(distances.min()));nearest=v if nearest is None else min(nearest,v)
    return dict(cell_overlap_area=float(overlap.area),point_overlap_area_estimate=estimate,
                point_inside_other_particle_count=int(flags.sum()),point_count=len(x),
                within_particle_excess_area=max(0.,within_raw),within_particle_excess_raw=within_raw,
                between_particle_excess_area=max(0.,between_raw),drawn_overlap_area=float(drawn.area),stroke_width=stroke_width,
                union_area=float(whole.area),cell_sum_area=float(areas.sum()),reference_area=float(np.asarray(data['reference_area']).sum()),
                point_estimated_union_area=float(np.sum(areas/counts)),pair_intersection_areas=pair,
                minimum_interparticle_point_distance=nearest,area_unit='normalized_code_length_squared')

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def analyze(root,out):
    need(not out.exists(),'output must be a new directory');out.mkdir(parents=True)
    records=[];sources=[]
    for arm in ('S','F'):
        folder=root/arm/(arm+'_shape');mp=folder/'MANIFEST.json';manifest=json.loads(mp.read_bytes())
        need(manifest['arm']==arm and manifest['status']=='SHAPE_OUTPUT_COMPLETE','complete arm manifest')
        identity=None;previous=-1
        for entry in manifest['frames']:
            name=entry['npz']['path'];need(Path(name).name==name,'frame basename')
            p=folder/name;digest=sha(p);need(digest==entry['npz']['sha256'] and p.stat().st_size==entry['npz']['bytes'],'frame hash')
            with np.load(p,allow_pickle=False) as z:data={k:z[k] for k in z.files}
            step=int(data['step']);time=float(data['time_code'])
            need(step==entry['step'] and time==entry['time_code'] and step>previous,'actual frame timing');previous=step
            key=tuple(np.asarray(data[k]).tobytes() for k in ('point_id','particle_id','X','reference_area'))
            if identity is None:identity=key
            else:need(key==identity,'frame identity changed')
            r=measure_frame(data,stroke_width=.00025);r.update(arm=arm,step=step,time_code=time,npz_sha256=digest)
            records.append(r);sources.append(dict(path=p.relative_to(root).as_posix(),sha256=digest))
        sources.append(dict(path=mp.relative_to(root).as_posix(),sha256=sha(mp)))
    need([r['step'] for r in records if r['arm']=='S']==[r['step'] for r in records if r['arm']=='F'],'paired times')
    report=dict(label='DEVELOPMENT_DATA_ONLY',analysis_source_sha256=sha(Path(__file__)),numpy=np.__version__,shapely=shapely.__version__,
                solver_execution=0,field_execution=0,input_mutation=0,records=records,sources=sources,
                interpretation='center quadrature estimate versus affine-cell union geometry; neither establishes physical interpenetration or contact qualification')
    (out/'overlap.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf8')
    fields=['arm','step','time_code','point_overlap_area_estimate','cell_overlap_area','drawn_overlap_area','point_inside_other_particle_count','point_count','union_area','within_particle_excess_area','between_particle_excess_area','minimum_interparticle_point_distance']
    with (out/'overlap.csv').open('w',encoding='utf8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(records)
    need(all(sha(root/s['path'])==s['sha256'] for s in sources),'input changed during analysis')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    r=analyze(a.input,a.out);print(json.dumps(dict(frames=len(r['records']),solver_execution=0)))
