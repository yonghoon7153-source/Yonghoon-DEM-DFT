"""Static generated deck/consumer evidence only; no simulator or real run inputs."""
from pathlib import Path
import hashlib,json,sys
scripts=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();out.mkdir(parents=True,exist_ok=False)
sys.path.insert(0,str(scripts))
import test_mixer_d2_consumers as t
rows=[]
for label,seed,layered in [('max_layered',2147483647,True),('max_uniform',2147483647,False),('nearmax_layered',2147483629,True)]:
 a,am,_=t.fixture(seed=seed,layered=layered);b,bm,_=t.fixture(seed=seed,layered=layered,coated=True)
 root=out/label;root.mkdir();t._write_case(root,a,b,am,bm)
 apis={'readback':t.rb.read_d2(a,am),'pair':t.dd.diff_d2_decks(a,b,am,bm),'plan':t.smoke.d2_plan_check(a,am)}
 cli={}
 for k,(rc,stdout,stderr) in t._run_three_cli(root).items():
  (root/(k+'.stdout')).write_text(stdout,encoding='utf-8');(root/(k+'.stderr')).write_text(stderr,encoding='utf-8')
  cli[k]={'rc':rc,'stdout':label+'/'+k+'.stdout','stderr':label+'/'+k+'.stderr'}
 rows.append({'case':label,'seed':seed,'layered':layered,
              'printed_seeds':[tokens[tokens.index('seed')+1] for _,tokens in t.rb.read_deck(a)['cmds'] if len(tokens)>3 and tokens[3]=='insert/pack'],
              'apis':apis,'cli':cli,'bytes':{p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in root.glob('*.in')}})
(out/'summary.json').write_text(json.dumps({'rows':rows,'research_results':0,'scope':'synthetic planned decks only'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps([{'case':x['case'],'apis':{k:r['verdict'] for k,r in x['apis'].items()},'cli_rc':{k:r['rc'] for k,r in x['cli'].items()}} for x in rows]))
