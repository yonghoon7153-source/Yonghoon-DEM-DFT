"""Emulate Linux default LF when synthetic selftests write text on Windows.
No production source is edited. No solver or scheduler execution.
"""
import builtins, io, runpy, sys
orig_open, orig_io = builtins.open, io.open
def wrap(fn):
    def opened(file, mode='r', *a, **kw):
        if isinstance(mode,str) and 'b' not in mode and any(x in mode for x in ('w','a','x')) and 'newline' not in kw:
            if len(a)>=4:
                if a[3] is None:
                    a=(*a[:3],'\n',*a[4:])
            else:
                kw['newline']='\n'
        return fn(file,mode,*a,**kw)
    return opened
builtins.open=wrap(orig_open)
io.open=wrap(orig_io)
target=sys.argv[1]
sys.argv=[target,'--selftest']
sys.path.insert(0,str(__import__('pathlib').Path(target).resolve().parent))
runpy.run_path(target,run_name='__main__')
