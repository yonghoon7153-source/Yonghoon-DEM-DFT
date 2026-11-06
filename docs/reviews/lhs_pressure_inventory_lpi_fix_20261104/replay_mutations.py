import ast,concurrent.futures,difflib,hashlib,json,os,pathlib,subprocess,sys,time
repo=pathlib.Path(__file__).resolve().parents[3]
d=repo/'docs/reviews/lhs_pressure_inventory_20261104'
e=pathlib.Path(__file__).resolve().parent
if len(sys.argv)!=2:
    raise SystemExit("usage: python3 -I -B replay_mutations.py NEW_SCRATCH_DIRECTORY (synthetic only)")
work=pathlib.Path(sys.argv[1]).resolve()
work.mkdir(parents=True, exist_ok=False)
out=work/'evidence';out.mkdir()
source=(d/'pressure_inventory.sh').read_text();sha=lambda b:hashlib.sha256(b).hexdigest()
mutations={
 'output_retry':source.replace('''    except BaseException:
        return 2
    return rc''','''    except BaseException:
        print(json.dumps({"status": "NOT_ESTABLISHED", "rc": 2}))
        return 2
    return rc'''),
 'missing_flush':source.replace('        sys.stdout.flush()','        pass  # deliberately removed explicit flush'),
 'shutdown_reflush':source.replace('    os._exit(main(sys.argv[1:]))','    sys.exit(main(sys.argv[1:]))'),
 'short_write_accepted':source.replace('''        if sys.stdout.write(payload) != len(payload):
            return 2''','''        sys.stdout.write(payload)'''),
 'shell_fallback':source.replace('exec python3 -I -B -c','python3 -I -B -c')+'''rc=$?
case "$rc" in
  0|2) exit "$rc" ;;
  *) printf '%s\\n' '{"schema":"lhs_pressure_inventory/v1","status":"NOT_ESTABLISHED","rc":2,"reason":"RUNTIME_ERROR"}' ; exit 2 ;;
esac
'''}
assert all(s!=source for s in mutations.values())
def run(item):
 name,s=item;p=work/(name+'.sh');p.write_text(s);patch=out/(name+'.patch');patch.write_text(''.join(difflib.unified_diff(source.splitlines(True),s.splitlines(True),fromfile='pressure_inventory.sh',tofile=name+'.sh')))
 env=dict(os.environ,LPI_COMMAND=str(p));cmd=[sys.executable,'-I','-B',str(d/'test_output_contract.py')];start=time.monotonic();r=subprocess.run(cmd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60)
 log=out/(name+'.log');log.write_bytes(r.stdout)
 failed=[line.split(' ',1)[0] for line in r.stdout.decode().splitlines() if line.startswith('test_') and line.endswith(' ... FAIL')]
 result={'name':name,'mutant_sha256':sha(p.read_bytes()),'patch_sha256':sha(patch.read_bytes()),'rc':r.returncode,'failures':failed,'log':log.name,'log_sha256':sha(log.read_bytes()),'elapsed_seconds':round(time.monotonic()-start,6)}
 assert r.returncode==1 and failed,result
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(run,mutations.items()))
# Inventory/parser/path/identity AST nodes must be identical to the reviewed version.
old=(e/'before/pressure_inventory.sh').read_text()
def defs(text):
 code=text.split("-c '\n",1)[1].split("\n' \"$@\"",1)[0]
 return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(code).body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name!='main'}
assert defs(old)==defs(source)
assert sha((repo/'scripts/lhs_pressure_record.py').read_bytes())=='34eb74142884489505590501840ccc6423a014a508989c82f135020146283ad3'
record={'source_sha256':sha(source.encode()),'test_sha256':sha((d/'test_output_contract.py').read_bytes()),'mutations':results,'detected':len(results),'attempted':len(mutations),'non_main_function_class_ast_unchanged':len(defs(source)),'b7_file_unchanged':True,'scope':'Synthetic faults and guarded-code reversions only; mutated commands never run against actual inventory paths.'}
(out/'mutations.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
