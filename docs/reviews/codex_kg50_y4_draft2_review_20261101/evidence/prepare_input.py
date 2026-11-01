from pathlib import Path
import hashlib,sys,zipfile
root=Path(__file__).resolve().parent
z=Path(sys.argv[1]); expected='0851437db6d1893ba80699718fb115b99f9bb2aff870bec3e73f1b602b6b1c30'
assert hashlib.sha256(z.read_bytes()).hexdigest()==expected, 'wrong input ZIP'
name='external/kg50_d1_end_20261031.tgz'
with zipfile.ZipFile(z) as f: data=f.read(name)
assert hashlib.sha256(data).hexdigest()=='a3c91af34ee57fe8ffb7326f5622cd84bcfbabef59b8df4958c9cb34587ee2d7'
out=root/'source'/name;out.parent.mkdir(parents=True,exist_ok=True)
if out.exists(): assert out.read_bytes()==data, 'existing file differs; not overwritten'
else: out.write_bytes(data)
print('verified input D1 archive ready:',out)
