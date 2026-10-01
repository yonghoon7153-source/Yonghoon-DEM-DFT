"""Windows diagnostic only: temp-fixture symlinks use byte-identical copies, not production certification."""
import pathlib,runpy,sys,shutil,tempfile
R=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(R/'snapshot/scripts'))
def copy_fixture(self,target,target_is_directory=False):
    tmp=pathlib.Path(tempfile.gettempdir()).resolve()
    if not self.resolve().is_relative_to(tmp) or not pathlib.Path(target).resolve().is_relative_to(tmp):
        raise RuntimeError('Diagnostic replacement is restricted to temporary synthetic fixtures')
    shutil.copyfile(target,self)
pathlib.Path.symlink_to=copy_fixture
sys.argv=['lhs_webapp_batch.py','--selftest']
runpy.run_path(str(R/'snapshot/scripts/lhs_webapp_batch.py'),run_name='__main__')
