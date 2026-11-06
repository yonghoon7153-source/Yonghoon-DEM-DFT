import hashlib, json, os, pathlib, subprocess, tempfile, time, unittest, runpy
CANON=runpy.run_path(str(pathlib.Path(__file__).resolve().parent/"submit_one.py.txt"))["canonical_runner"]
HERE=pathlib.Path(__file__).resolve().parent
class Submission(unittest.TestCase):
 def exercise(self,mode,mutate=None,hook=None):
  import importlib.util,contextlib,io
  spec=importlib.util.spec_from_file_location('mla_local_fixture',str(HERE/'test_mla_boundaries.py'))
  module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
  with tempfile.TemporaryDirectory() as td:
   fixture=module.Fixture(td);fixture.mode={'fail':'failed'}.get(mode,mode)
   c,approval,files,put=fixture.make();live=json.loads(pathlib.Path(c['live_preflight']['path']).read_text())
   def seal(name,data):
    if name in ('job_start','python'):
     target=pathlib.Path(c['runner_bindings'][name]);target.write_text(data)
     return {'path':str(target),'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
    return put(name,data)
   if mutate:mutate(c,live,seal)
   approval.write_text(json.dumps(c))
   if hook:return hook(c,approval,files,seal)
   def attempt():
    try:
     with contextlib.redirect_stdout(io.StringIO()):fixture.submit(approval)
     return 0
    except Exception:return 2
   return attempt(),attempt(),'x'*len(fixture.calls)
 def test_exact_once(self):self.assertEqual(self.exercise('ok'),(0,2,'x'))
 def test_failure_no_retry(self):self.assertEqual(self.exercise('fail'),(2,2,'x'))
 def test_ambiguous_no_retry(self):self.assertEqual(self.exercise('ambiguous'),(2,2,'x'))
 def test_missing_go(self):self.assertEqual(self.exercise('ok',lambda c,l,s:c.update(execution_authorized=False)),(2,2,''))
 def test_cpu_cap(self):
  def bad(c,l,s):l['reserved_cpus']=41;c['live_preflight']=s('live',json.dumps(l))
  self.assertEqual(self.exercise('ok',bad),(2,2,''))
 def test_identity(self):self.assertEqual(self.exercise('ok',lambda c,l,s:c['binary'].update(sha256='0'*64)),(2,2,''))
 def test_source_pin(self):self.assertEqual(self.exercise('ok',lambda c,l,s:c.update(source_pin='bad')),(2,2,''))
 def test_runner_bytes(self):self.assertEqual(self.exercise('ok',lambda c,l,s:c.update(runner=s('runner','arbitrary command'))),(2,2,''))
 def test_changed_job_start(self):
  def change(c,l,seal):
   new=seal('job_start','arbitrary Python code')
   m=json.loads(pathlib.Path(c['source_manifest']['path']).read_text())
   for a in m['files']:
    if a['path']==new['path']:a.update(new)
   c['source_manifest']=seal('manifest',json.dumps(m))
  self.assertEqual(self.exercise('ok',change),(2,2,''))
 def test_choices(self):self.assertEqual(self.exercise('ok',lambda c,l,s:c.update(author_choices_confirmed=False)),(2,2,''))
if __name__=='__main__':unittest.main()
