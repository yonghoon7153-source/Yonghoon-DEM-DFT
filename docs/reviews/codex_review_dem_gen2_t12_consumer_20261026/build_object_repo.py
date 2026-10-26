from pathlib import Path
import json,hashlib,datetime,zlib,subprocess,itertools,shutil,os
R=Path(__file__).resolve().parent;E=R/'evidence';G=R/'object_repo';G.mkdir(exist_ok=True);subprocess.run(['git','init','--quiet',str(G)],check=True)
os.environ.update(GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='safe.directory',GIT_CONFIG_VALUE_0=G.as_posix(),GIT_NO_LAZY_FETCH='1')
objects=G/'.git/objects';written=[]
def write(kind,b,sha):
 raw=kind.encode()+b' '+str(len(b)).encode()+b'\0'+b;actual=hashlib.sha1(raw).hexdigest();assert actual==sha,(kind,actual,sha)
 p=objects/sha[:2]/sha[2:];p.parent.mkdir(exist_ok=True);p.write_bytes(zlib.compress(raw));written.append({'type':kind,'sha':sha,'bytes':len(b)})
c=json.loads((E/'consumer_commit.json').read_text(encoding='utf-8-sig'))
for tzA,tzC,newline in itertools.product(['+0000','+0900','-0700'],['+0000','+0900','-0700'],['\n','']):
 def who(k,tz):
  d=c[k];stamp=int(datetime.datetime.fromisoformat(d['date'].replace('Z','+00:00')).timestamp());return f"{k} {d['name']} <{d['email']}> {stamp} {tz}\n"
 s='tree '+c['tree']['sha']+'\n'+''.join('parent '+p['sha']+'\n' for p in c['parents'])+who('author',tzA)+who('committer',tzC)+'\n'+c['message']+newline;b=s.encode()
 if hashlib.sha1(b'commit '+str(len(b)).encode()+b'\0'+b).hexdigest()==c['sha']:write('commit',b,c['sha']);break
else:raise Exception('Cannot reconstruct exact original commit bytes')
for idx in range(4):
 t=json.loads((E/f'consumer_tree{idx}.json').read_text(encoding='utf8'));assert not t['truncated'];b=b''.join(x['mode'].lstrip('0').encode()+b' '+x['path'].encode()+b'\0'+bytes.fromhex(x['sha']) for x in t['tree']);write('tree',b,t['sha'])
kit=R/'consumer';tree=json.loads((E/'consumer_tree3.json').read_text());names=['ul_reader.py','ul_gates.py','ul_lib.py','ul_observers.py','ul_s3.py','unload_params.json'];pin=c['sha'];manifest=json.loads((R/'snapshot/docs/reviews/dem_gen2_t12_consumer_contract_evidence_20261024/source-manifest.json').read_text())
for name in names:
 b=(kit/name).read_bytes();oid=next(x['sha'] for x in tree['tree'] if x['path']==name);write('blob',b,oid);assert hashlib.sha256(b).hexdigest()==manifest['files_sha256'][name]
 out=subprocess.run(['git','-C',str(G),'show',pin+':docs/data/ps45_unload_20261009/'+name],capture_output=True,check=True);assert out.stdout==b
(R/'evidence/object_database.json').write_text(json.dumps({'status':'PASS','method':'Exact original commit and four tree objects reconstructed from read-only GitHub API metadata, all SHA1 verified; six blobs from previously verified snapshot. New partial object database only, no shared repo modification or fetch.','objects':written,'consumer_pin':pin},indent=2),encoding='utf8');print('Exact Git object database ready',len(written),'objects')
