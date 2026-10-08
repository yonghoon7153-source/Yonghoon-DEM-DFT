"""B-only Windows transport. Import has no OS/process side effects.
Not exercised with real processes in A stage. Tests inject FakeTransport.
Private Job Object; root created suspended, assigned before ResumeThread.
No process-name termination. No elevation. No breakaway flags.
"""
import ctypes as C
from ctypes import wintypes as W
import os, time, subprocess

class NativeUnavailable(RuntimeError): pass
def cleanup_grade(assigned,remaining,outsiders,errors=()):
    return 'PASS' if assigned and remaining==[] and outsiders==[] and not errors else 'INCOMPLETE'
class WindowsJobTransport:
    def __init__(self, kernel=None, clock=None):
        self.clock=clock or time
        if kernel is not None:
            self.execution_kernel=kernel;self.census=kernel.census;return
        if os.name!='nt': raise NativeUnavailable('Windows only; no fallback')
        self.k=C.WinDLL('kernel32',use_last_error=True)
        self.a=C.WinDLL('advapi32',use_last_error=True)
        self._types()
        self.execution_kernel=NativeExecutionKernel(self)

    def _types(self):
        S=C.c_size_t; H=W.HANDLE; D=W.DWORD
        class IO(C.Structure): _fields_=[(n,C.c_ulonglong) for n in ('ReadOperationCount','WriteOperationCount','OtherOperationCount','ReadTransferCount','WriteTransferCount','OtherTransferCount')]
        class BASIC(C.Structure): _fields_=[('PerProcessUserTimeLimit',C.c_longlong),('PerJobUserTimeLimit',C.c_longlong),('LimitFlags',D),('MinimumWorkingSetSize',S),('MaximumWorkingSetSize',S),('ActiveProcessLimit',D),('Affinity',S),('PriorityClass',D),('SchedulingClass',D)]
        class EXT(C.Structure): _fields_=[('BasicLimitInformation',BASIC),('IoInfo',IO),('ProcessMemoryLimit',S),('JobMemoryLimit',S),('PeakProcessMemoryUsed',S),('PeakJobMemoryUsed',S)]
        class SI(C.Structure): _fields_=[('cb',D),('lpReserved',W.LPWSTR),('lpDesktop',W.LPWSTR),('lpTitle',W.LPWSTR),('dwX',D),('dwY',D),('dwXSize',D),('dwYSize',D),('dwXCountChars',D),('dwYCountChars',D),('dwFillAttribute',D),('dwFlags',D),('wShowWindow',W.WORD),('cbReserved2',W.WORD),('lpReserved2',C.POINTER(C.c_byte)),('hStdInput',H),('hStdOutput',H),('hStdError',H)]
        class PI(C.Structure): _fields_=[('hProcess',H),('hThread',H),('dwProcessId',D),('dwThreadId',D)]
        class PE(C.Structure): _fields_=[('dwSize',D),('cntUsage',D),('th32ProcessID',D),('th32DefaultHeapID',S),('th32ModuleID',D),('cntThreads',D),('th32ParentProcessID',D),('pcPriClassBase',W.LONG),('dwFlags',D),('szExeFile',W.WCHAR*260)]
        self.EXT,self.SI,self.PI,self.PE=EXT,SI,PI,PE
        signatures={
          'CreateJobObjectW':([C.c_void_p,W.LPCWSTR],H),
          'SetInformationJobObject':([H,C.c_int,C.c_void_p,D],W.BOOL),
          'QueryInformationJobObject':([H,C.c_int,C.c_void_p,D,C.POINTER(D)],W.BOOL),
          'CreateProcessW':([W.LPCWSTR,W.LPWSTR,C.c_void_p,C.c_void_p,W.BOOL,D,C.c_void_p,W.LPCWSTR,C.POINTER(SI),C.POINTER(PI)],W.BOOL),
          'AssignProcessToJobObject':([H,H],W.BOOL),'IsProcessInJob':([H,H,C.POINTER(W.BOOL)],W.BOOL),
          'ResumeThread':([H],D),'TerminateJobObject':([H,W.UINT],W.BOOL),
          'TerminateProcess':([H,W.UINT],W.BOOL),'CloseHandle':([H],W.BOOL),
          'WaitForSingleObject':([H,D],D),'GetExitCodeProcess':([H,C.POINTER(D)],W.BOOL),
          'GetProcessTimes':([H,C.POINTER(W.FILETIME),C.POINTER(W.FILETIME),C.POINTER(W.FILETIME),C.POINTER(W.FILETIME)],W.BOOL),
          'CreateToolhelp32Snapshot':([D,D],H),'Process32FirstW':([H,C.POINTER(PE)],W.BOOL),'Process32NextW':([H,C.POINTER(PE)],W.BOOL),
          'GetCurrentProcess':([],H),'GetCurrentProcessId':([],D)}
        for name,(args,result) in signatures.items(): f=getattr(self.k,name);f.argtypes=args;f.restype=result
        self.a.OpenProcessToken.argtypes=[H,D,C.POINTER(H)];self.a.OpenProcessToken.restype=W.BOOL
        self.a.GetTokenInformation.argtypes=[H,C.c_int,C.c_void_p,D,C.POINTER(D)];self.a.GetTokenInformation.restype=W.BOOL
    def must(self,value):
        if not value: raise C.WinError(C.get_last_error())
        return value
    def identity(self):
        token=W.HANDLE();self.must(self.a.OpenProcessToken(self.k.GetCurrentProcess(),8,C.byref(token)))
        try:
            elevated=W.DWORD();size=W.DWORD();self.must(self.a.GetTokenInformation(token,20,C.byref(elevated),4,C.byref(size)))
            if size.value!=4 or elevated.value not in (0,1):raise RuntimeError('TokenElevation length/value mismatch')
            # OS logon identity; do not treat environment USERNAME as token evidence.
            buf=C.create_unicode_buffer(256);length=W.DWORD(256)
            self.a.GetUserNameW.argtypes=[W.LPWSTR,C.POINTER(W.DWORD)];self.a.GetUserNameW.restype=W.BOOL
            self.must(self.a.GetUserNameW(buf,C.byref(length)))
            return {'user':buf.value,'elevated':bool(elevated.value),'launcher_pid':os.getpid(),'token_elevation_return_bytes':size.value}
        finally:self.k.CloseHandle(token)
    def census(self):
        snap=self.k.CreateToolhelp32Snapshot(2,0)
        if snap==C.c_void_p(-1).value:raise C.WinError(C.get_last_error())
        try:
            p=self.PE();p.dwSize=C.sizeof(p);out=[];ok=self.k.Process32FirstW(snap,C.byref(p))
            while ok:
                if p.szExeFile.lower().startswith('comsol'):
                    out.append({'pid':int(p.th32ProcessID),'parent_pid':int(p.th32ParentProcessID),'name':p.szExeFile})
                ok=self.k.Process32NextW(snap,C.byref(p))
            if C.get_last_error()!=18:raise C.WinError(C.get_last_error())
            return out
        finally:self.k.CloseHandle(snap)
    def resources(self,path):
        import shutil
        class MEMORY(C.Structure):
            _fields_=[('length',W.DWORD),('load',W.DWORD)]+[(k,C.c_ulonglong) for k in ('totalPhys','availPhys','totalPage','availPage','totalVirtual','availVirtual','availExtended')]
        m=MEMORY();m.length=C.sizeof(m)
        self.k.GlobalMemoryStatusEx.argtypes=[C.POINTER(MEMORY)];self.k.GlobalMemoryStatusEx.restype=W.BOOL
        self.must(self.k.GlobalMemoryStatusEx(C.byref(m)))
        return {'available_ram_bytes':int(m.availPhys),'free_disk_bytes':shutil.disk_usage(path).free}
    def _members(self,job):
        # If membership list exceeds this bound, fail closed, never infer empty.
        class IDS(C.Structure): _fields_=[('assigned',W.DWORD),('count',W.DWORD),('ids',C.c_size_t*4096)]
        data=IDS();size=W.DWORD();self.must(self.k.QueryInformationJobObject(job,3,C.byref(data),C.sizeof(data),C.byref(size)))
        if data.count>4096 or data.assigned!=data.count:raise RuntimeError('Ambiguous job membership')
        return list(data.ids[:data.count])
    def run(self,argv,cwd,log_path,seconds,cleanup_seconds,on_update,visible=False):
        # This same body is exercised with an inert kernel/clock. No toy duplicate controller.
        if seconds<=0:return {'rc':None,'timeout':True,'cleanup':'PASS','started':False,
            'not_started_verified':True,'ownership_verified':False,'remaining_owned':[],'unattributed_comsol':[],
            'recording_errors':[],'root_exit_observed':False,'exit_query_succeeded':False,'handles_closed':True}
        k=self.execution_kernel;clock=self.clock;begin=clock.monotonic();deadline=begin+seconds
        job=process=thread=None;pid=created=None;started=assigned=resumed=False
        remaining=None;outsiders=None;observed=set();errors=[];recording=[];original=None
        termination=None;timeout=False;wait_result=None;exit_ok=False;rc=None;exit_observed=False
        closed=[];before=set();cleanup_begin=None
        def error(operation,e):return {'operation':operation,'error':str(e),'winerror':getattr(e,'winerror',None)}
        def emit(v,critical=False):
            try:on_update(v)
            except BaseException as e:
                recording.append(error('critical_record' if critical else 'poll_record',e))
                if critical:raise
        def request_termination(reason):
            nonlocal termination
            if termination is not None or not started:return
            termination={'scope':'job' if assigned else 'suspended_root','requested_code':124 if reason=='timeout' else 125,'reason':reason,'success':False}
            try:
                if assigned:k.terminate_job(job,termination['requested_code'])
                else:k.terminate_root(process,termination['requested_code'])
                termination['success']=True
            except BaseException as e:errors.append(error('terminate_'+termination['scope'],e))
        try:
            before={r['pid'] for r in self.census()}
            job=k.create_job();k.set_kill_on_close(job)
            process,thread,pid=k.spawn(argv,cwd,log_path,visible);started=True
            created=k.creation(process)
            identity={'root_pid':pid,'root_creation_filetime':created}
            emit(dict(identity,event='root',suspended=True,assigned_before_resume=False),True)
            k.assign(job,process);assigned=True
            if not k.is_assigned(job,process):raise RuntimeError('Root not assigned to private job')
            emit(dict(identity,event='assignment',assigned_before_resume=True,job_members=k.members(job)),True)
            k.resume(thread);resumed=True
            emit(dict(identity,event='resume',assigned_before_resume=True),True)
            while True:
                remaining=k.members(job);observed.update(remaining)
                # Optional callback failures are latched, not unwound to kill-on-close.
                emit({'event':'poll','job_members':remaining,'observed_owned_pids':sorted(observed)})
                if not remaining:break
                if clock.monotonic()>=deadline:
                    timeout=True;request_termination('timeout');break
                clock.sleep(min(.5,max(0,deadline-clock.monotonic())))
        except BaseException as e:
            original=error('execution',e);request_termination('exception')
        finally:
            cleanup_begin=clock.monotonic();cleanup_deadline=cleanup_begin+cleanup_seconds
            if job is not None:
                try:
                    remaining=k.members(job)
                    while remaining and clock.monotonic()<cleanup_deadline:
                        clock.sleep(min(.2,max(0,cleanup_deadline-clock.monotonic())));remaining=k.members(job)
                    observed.update(remaining)
                except BaseException as e:remaining=None;errors.append(error('cleanup_members',e))
            else:remaining=[]
            if started:
                try:
                    wait_result=k.wait(process)
                    exit_observed=wait_result==0
                    if wait_result==0xFFFFFFFF:errors.append({'operation':'wait','winerror':k.last_error(),'error':'WAIT_FAILED'})
                except BaseException as e:errors.append(error('wait',e))
                try:
                    value=k.exit_code(process);exit_ok=True
                    if exit_observed:rc=value  # 259 is a valid actual exit after signaled wait.
                except BaseException as e:errors.append(error('exit_code',e))
            try:
                outsiders=[r for r in self.census() if r['pid'] not in before and r['pid'] not in (remaining or [])]
            except BaseException as e:errors.append(error('cleanup_census',e))
            # Last Job close can kill live members. It occurs only after normal loop/deadline/error cleanup.
            for label,handle in (('thread',thread),('process',process),('job',job)):
                if handle is None:continue
                try:k.close(handle);closed.append(label)
                except BaseException as e:errors.append(error('close_'+label,e))
            try:k.close_io()
            except BaseException as e:errors.append(error('close_io',e))
        handles_closed=all(h is None or n in closed for n,h in (('job',job),('process',process),('thread',thread))) and not any(e['operation']=='close_io' for e in errors)
        # A pre-assignment suspended process may be cleaned through its held handle without asserting Job ownership.
        clean=(remaining==[] and outsiders==[] and handles_closed and (not started or exit_observed and exit_ok)
            and not errors and clock.monotonic()<=cleanup_begin+cleanup_seconds)
        result={'started':started,'not_started_verified':not started,'rc':rc,'wait_result':wait_result,
            'root_exit_observed':exit_observed,'exit_query_succeeded':exit_ok,'timeout':timeout,'resumed':resumed,
            'root_pid':pid,'root_creation_filetime':created,'remaining_owned':remaining,'unattributed_comsol':outsiders,
            'ownership_verified':assigned,'observed_owned_pids':sorted(observed),'handles_closed':handles_closed,
            'cleanup':'PASS' if clean else 'INCOMPLETE','cleanup_errors':errors,'recording_errors':recording,
            'original_error':original,'termination_request':termination,'job_only_termination':bool(termination and assigned),
            'exception_owned_handle_termination':bool(termination and termination['reason']=='exception'),
            'elapsed_seconds':clock.monotonic()-begin,'cleanup_elapsed_seconds':clock.monotonic()-cleanup_begin,
            'closed_handles':closed,'kill_on_job_close_retained':True}
        emit({'event':'diagnostic','terminal_observation':dict(result)})
        result['recording_errors']=list(recording)
        return result

class NativeExecutionKernel:
    """B-only adapter. No initialization at import; all process functions gated by launcher."""
    def __init__(self,t):self.t=t;self.k=t.k;self.io=[]
    def last_error(self):return C.get_last_error()
    def create_job(self):return self.t.must(self.k.CreateJobObjectW(None,None))
    def set_kill_on_close(self,job):
        limits=self.t.EXT();limits.BasicLimitInformation.LimitFlags=0x2000
        self.t.must(self.k.SetInformationJobObject(job,9,C.byref(limits),C.sizeof(limits)))
    def spawn(self,argv,cwd,log_path,visible):
        import msvcrt
        log=open(log_path,'xb',buffering=0);self.io.append(log)
        null=open(os.devnull,'rb',buffering=0);self.io.append(null)
        os.set_inheritable(log.fileno(),True);os.set_inheritable(null.fileno(),True)
        si=self.t.SI();si.cb=C.sizeof(si);si.dwFlags=0x100|1;si.wShowWindow=5 if visible else 0
        si.hStdOutput=msvcrt.get_osfhandle(log.fileno());si.hStdError=si.hStdOutput;si.hStdInput=msvcrt.get_osfhandle(null.fileno())
        pi=self.t.PI();cmd=C.create_unicode_buffer(subprocess.list2cmdline(argv))
        self.t.must(self.k.CreateProcessW(argv[0],cmd,None,None,True,0x4|(0 if visible else 0x08000000),None,str(cwd),C.byref(si),C.byref(pi)))
        return pi.hProcess,pi.hThread,int(pi.dwProcessId)
    def creation(self,process):
        ft=[W.FILETIME() for _ in range(4)];self.t.must(self.k.GetProcessTimes(process,*[C.byref(v) for v in ft]));return (ft[0].dwHighDateTime<<32)|ft[0].dwLowDateTime
    def assign(self,j,p):self.t.must(self.k.AssignProcessToJobObject(j,p))
    def is_assigned(self,j,p):
        v=W.BOOL();self.t.must(self.k.IsProcessInJob(p,j,C.byref(v)));return bool(v.value)
    def resume(self,t):
        if self.k.ResumeThread(t)==0xFFFFFFFF:raise C.WinError(C.get_last_error())
    def members(self,j):return self.t._members(j)
    def wait(self,p):return int(self.k.WaitForSingleObject(p,0))
    def exit_code(self,p):
        v=W.DWORD();self.t.must(self.k.GetExitCodeProcess(p,C.byref(v)));return int(v.value)
    def terminate_job(self,j,c):self.t.must(self.k.TerminateJobObject(j,c))
    def terminate_root(self,p,c):self.t.must(self.k.TerminateProcess(p,c))
    def close(self,h):self.t.must(self.k.CloseHandle(h))
    def close_io(self):
        errors=[]
        for f in self.io:
            try:f.close()
            except Exception as e:errors.append(e)
        if errors:raise errors[0]
