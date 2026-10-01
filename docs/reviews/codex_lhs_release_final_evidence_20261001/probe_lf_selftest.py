"""Diagnostic: normalize synthetic text fixtures to Linux LF; production source unchanged."""
import builtins,pathlib,runpy,sys
R=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(R/'snapshot/scripts'))
original_open=builtins.open
def lf_open(file,mode='r',*args,**kwargs):
    if 'w' in mode and 'b' not in mode and 'newline' not in kwargs:kwargs['newline']='\n'
    return original_open(file,mode,*args,**kwargs)
builtins.open=lf_open
sys.argv=['lhs_descriptor_harvest.py','--selftest']
runpy.run_path(str(R/'snapshot/scripts/lhs_descriptor_harvest.py'),run_name='__main__')
