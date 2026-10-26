from pathlib import Path
import sys,re,json,math,hashlib,difflib
O=Path(__file__).resolve().parent; R=O.parents[1]/'snapshot/repo'; D=R/'docs/data/kg50_decks_20261026'; B=(R/'docs/data/phase_a_6mah/in.real_4.liggghts').read_text(encoding='utf8')
sys.dont_write_bytecode=True; sys.path.insert(0,str(R/'scripts')); import make_se_size_decks as G
M=json.loads((D/'manifest.json').read_text(encoding='utf8')); checks=[]; rows=[]; seeds=[]
def ck(n,c,detail=None):
 checks.append(dict(name=n,passed=bool(c),detail=detail))
 if not c: print('FAIL',n,detail)
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
files=[p for p in (O/'regenerated').rglob('*') if p.is_file()]
comparisons=[dict(path=str(p.relative_to(O/'regenerated')),equal=digest(p)==digest(D/p.relative_to(O/'regenerated')),sha256=digest(p)) for p in files]
ck('All regenerated files byte-identical',all(x['equal'] for x in comparisons),len(files))
def skeleton(t):
 out=[]
 for ln in t.splitlines():
  if not ln.strip() or ln.lstrip().startswith('#'): continue
  s=ln.split('#',1)[0].rstrip()
  if s=='processors * * 1' or re.match(r'(variable n_ins |variable n_am_ins |group g_am_ins |print "====== (INSERTED |AM )|if "\$\{n_(ins|am_ins)\})',s):continue
  if s.strip().startswith('"print \'FATAL:') or s.strip()=='"quit 1"':continue
  if re.fullmatch(r'(restart \d+ restart_\S+/restart_compress_\*\.bin|write_restart restart_\S+/restart_settling_1\.bin)',s):continue
  s=re.sub(r'kg50_d(?:07|1|2|3)_b(?:40|50)(?:_s[23])?','real_4',s); s=re.sub(r'KG50_D(?:07|1|2|3)_B(?:40|50)(?:_S[23])?','REAL_4',s)
  if re.match(r'variable r_(AM_P|SE)\s+equal',s):s=re.sub(r'(equal\s+)\S+',r'\1<R>',s)
  elif s.startswith('region reg_'):
   a=s.split(); a[4]=a[6]='<BOX>'
   if a[1]=='reg_mix': a[8]='<ZTOP>'
   s=' '.join(a)
  elif re.match(r'fix pts[123] all particletemplate/sphere ',s):s=re.sub(r'(sphere |density constant )\d+',r'\1<N>',s)
  elif s.startswith('fix pdd_mix all particledistribution/discrete '):s='fix pdd_mix <DISTRIBUTION>'
  elif s.startswith('fix ins_mix all insert/pack seed '):s=re.sub(r'(seed )\d+',r'\1<SEED>',s)
  elif s.strip().startswith('maxattempt '):s=re.sub(r'(maxattempt )\d+',r'\1<ATT>',s)
  elif s.startswith('print "====== INSERTING PARTICLES '):s='print <INSERT>'
  elif s.startswith('print "====== Simulation Finished!'):s='print <END>'
  elif s.startswith('print "vertex '):s=re.sub(r'(?<!\S)0\.(?:05|04)(?=\s)','<BOX>',s)
  elif s.startswith('variable pressMPa ') or s.strip().startswith('variable current_press '):s=re.sub(r'0\.00(?:25|16)','<AREA>',s)
  elif s.startswith('dump dmp_atom all custom '):s=re.sub(r'(custom )\d+',r'\1<PERIOD>',s)
  out.append(s)
 return out
for r in M['cases']:
 c=r['case']; p=D/c/f'input_{c}.liggghts'; t=p.read_text(encoding='utf8')
 ck(c+' allowed executable changes',skeleton(B)==skeleton(t),list(difflib.unified_diff(skeleton(B),skeleton(t))))
 (O/(c+'.diff')).write_text(''.join(difflib.unified_diff(B.splitlines(True),t.splitlines(True))),encoding='utf8')
 x0,x1,y0,y1,z0,z1=map(float,re.search(r'^region reg_mix block (.*) units box$',t,re.M).group(1).split()); vf=float(re.search(r'volumefraction_region ([\d.]+)',t).group(1))
 ra=float(re.search(r'^variable r_AM_P\s+equal\s+(\S+)',t,re.M).group(1))*1000; rs=float(re.search(r'^variable r_SE\s+equal\s+(\S+)',t,re.M).group(1))*1000
 da=float(re.search(r'atom_type 1 density constant (\d+)',t).group(1))/1000; ds=float(re.search(r'atom_type 3 density constant (\d+)',t).group(1))/1000
 box=(x1-x0)*1000; area_cm2=(box*1e-4)**2; ma=6.5/200*area_cm2; ms=ma*.15/.85; va=4/3*math.pi*ra**3; vs=4/3*math.pi*rs**3
 na_load=ma/da/(va*1e-12); ns_load=ms/ds/(vs*1e-12); solid_um=6.5/200*(1/da+.15/.85/ds)*1e4
 v=(x1-x0)*(y1-y0)*(z1-z0)*1e9*vf; f=(.85/da)/(.85/da+.15/ds); na=round(v*f/va); ns=round(v*(1-f)/vs); n=na+ns
 ck(c+' parsed counts',{'AM_P':na,'SE':ns}==r['counts_pred']); ck(c+' geometry densities',da==4.85 and ds==1.64 and ra==3 and abs(solid_um/vf-(z1-z0)*1000)<.00051); ck(c+' loading route',abs(na-na_load)<.51 and abs(ns-ns_load)<1.)
 ar=re.findall(r'abs\(f_top_mesh\[3\]\)\s*/\s*([\d.]+)\s*/\s*1000000',t); ck(c+' pressure areas',len(ar)==2 and all(abs(float(a)-area_cm2*100)<1e-15 for a in ar))
 at=int(re.search(r'^\s+maxattempt (\d+)',t,re.M).group(1)); ck(c+' int32',n*at*1.3<2**31-1)
 floor=int(re.search(r'if "\$\{n_ins\} < (\d+)"',t).group(1)); lo,hi=map(int,re.search(r'if "\$\{n_am_ins\} < (\d+) \|\| \$\{n_am_ins\} > (\d+)"',t).groups())
 raw=p.read_bytes(); ins=(D/c/f'input_{c}_insert.liggghts').read_bytes(); cut=re.search(rb'^write_restart restart_\S+/restart_settling_1\.bin[^\n]*\n',raw,re.M).end()
 ck(c+' insert prefix bytes',ins[:cut]==raw[:cut]); ck(c+' insert tail',[a for a in ins[cut:].decode('utf8').splitlines() if a.strip() and not a.startswith('#')]==['run 2000'])
 ss=[int(next(a for a in m if a)) for m in re.findall(r'particletemplate/sphere (\d+)|particledistribution/discrete (\d+)|insert/pack seed (\d+)',t)]; seeds.extend(ss)
 ck(c+' primes',len(ss)==5 and all(10**7<=a<20_000_000 and all(a%d for d in range(2,math.isqrt(a)+1)) for a in ss))
 rows.append(dict(case=c,na_load=na_load,ns_load=ns_load,na=na,ns=ns,n=n,solid_um=solid_um,height_um=(z1-z0)*1000,areas=ar,int32=n*at,margin_int32=n*at*1.3,total_floor=floor,total_floor_pct=100*floor/n,am_gate=[lo,hi],am_gate_outer_pct=100*max(na-lo,hi-na)/na,strict_am_gate=[math.ceil(na*.995),math.floor(na*1.005)],loading=na*va*1e-12*da/area_cm2*200))
ck('Main case seeds unique',len(seeds)==len(set(seeds)))
cfg=dict(G.PRESET_KG50Y4); kw={k:cfg[k] for k in G.DECK_KW}; fallback=[]
for c,rs,b,slot in cfg['fallback50']:
 d,r=G.make_deck(B,c,rs,b,slot,**kw); fallback.append(r); n=r['n_total_pred']; lim=(2**31-1)/(n*1.3); low=math.ceil(lim)-1; high=math.ceil(lim)
 try:G.make_deck(B,c,rs,b,slot,**dict(kw,maxattempt=low)); passed=True
 except SystemExit:passed=False
 try:G.make_deck(B,c,rs,b,slot,**dict(kw,maxattempt=high)); rejected=False
 except SystemExit:rejected=True
 ck(c+' int32 boundary',passed and rejected,dict(largest_pass=low,first_reject=high))
bound=[]
for r in rows:
 lo,hi=r['am_gate']; a=r['na']; n=r['n']; f=r['total_floor']
 for nt,na in [(f-1,a),(f,a),(n,lo-1),(n,lo),(n,hi),(n,hi+1)]:bound.append(dict(case=r['case'],total=nt,am=na,accepted=not(nt<f or na<lo or na>hi),am_relative=na/a,total_relative=nt/n))
(O/'independent_audit.json').write_text(json.dumps(dict(checks=checks,rows=rows,fallback=fallback,boundaries=bound,regenerated_hashes=comparisons),ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(sum(c['passed'] for c in checks),'/',len(checks),'audit checks passed')
for r in rows[:5]:print(r)

