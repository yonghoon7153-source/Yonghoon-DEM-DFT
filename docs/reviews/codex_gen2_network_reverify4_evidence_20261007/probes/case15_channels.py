"""Direct frozen raw-dump build/solve calls, not a DEM or 194 campaign."""
from pathlib import Path
import gzip,sys,json,io,contextlib,hashlib,collections
R=Path(__file__).resolve().parents[1];S=R/'source';E=R/'evidence';sys.path.insert(0,str(S/'scripts'))
import network_conductivity as nc
def load(p,tag):
 with gzip.open(p,'rt') as f:
  for line in f:
   if line.startswith(tag):head=line[len(tag):].split();break
  return [dict(zip(head,x.split())) for x in f if x.strip() and not x.startswith('ITEM')]
root=S/'docs/data/case15_corner_20261001'
ap=root/'atom_v4_1710000.liggghts.gz';cp=root/'contact_v4_1710000.liggghts.gz'
A={int(r['id']):dict(type=int(r['type']),**{k:float(r[k]) for k in ('x','y','z','radius')}) for r in load(ap,'ITEM: ATOMS')}
C=[dict(id1=int(float(r['c_cpl[7]'])),id2=int(float(r['c_cpl[8]'])),contact_area=float(r['c_cpl[22]']),delta=float(r['c_cpl[23]'])) for r in load(cp,'ITEM: ENTRIES')]
# Geometry from raw STL vertices and atom BOX BOUNDS, not review text.
zs=[float(s.split()[3]) for s in (root/'mesh_v4_1710000.stl').read_text().splitlines() if s.strip().startswith('vertex')]
plate=sum(zs)/len(zs)
with gzip.open(ap,'rt') as f:
 for line in f:
  if line.startswith('ITEM: BOX BOUNDS'):break
 bounds=[[float(x) for x in next(f).split()[:2]] for _ in range(3)]
box=[x[1]-x[0] for x in bounds[:2]]
out=dict(atoms=len(A),contacts=len(C),plate_um=plate*1000,box_um=[b*1000 for b in box],negative_area=[dict(c,area_um2=c['contact_area']*1e6) for c in C if c['contact_area']<0],
         raw_sha256={p.name:hashlib.sha256(gzip.decompress(p.read_bytes())).hexdigest() for p in (ap,cp)},channels={})
for mode,target in [('ionic',[2]),('electronic',[1]),('thermal',[1,2])]:
 for cm in ('hertzian','physics'):
  key=mode+'_'+cm;log=io.StringIO()
  with contextlib.redirect_stdout(log):
   try:
    n=nc.build_network(A,C,target,1000.,plate,box_x=box[0],box_y=box[1],type_map={1:'AM_P',2:'SE'},mode=mode,contact_mode=cm)
    val=nc.solve_network(n,mode='full')
    d=dict(value=val,solve_info=n['solve_info']['full'],bottom=len(n['bottom']),top=len(n['top']),intersection=sorted(n['bottom']&n['top']),n_edges=len(n['edges']))
   except Exception as ex:d=dict(error=f'{type(ex).__name__}: {ex}')
  out['channels'][key]=d;(E/(key+'.log')).write_text(log.getvalue(),encoding='utf8')
  print(key,json.dumps(d,ensure_ascii=False),flush=True)
(E/'case15_channels.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print('geometry',out['plate_um'],out['box_um'],'negative contacts',len(out['negative_area']))
