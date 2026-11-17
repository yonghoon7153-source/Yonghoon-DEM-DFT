"""Read-only rev5 RT consumer. A numeric verdict is not operational GO."""
import hashlib
import importlib.util
import math
from pathlib import Path
import re
import struct

def _load(name,relative):
    here=Path(__file__).resolve().parent
    path=here/(name+'.py')
    if not path.is_file():path=here.parent/relative/(name+'.py')
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

# The standalone fixture injects these exact closed source modules.
if 'N' not in globals():N=_load('rt_numeric','p1_rt_numeric_preparation_20261117')
if 'B' not in globals():B=_load('rt_binding','p1_rt_runner_preparation_20261117')
RESETS=(('history_zwall_bot','property/atom',('global','per-atom')),('top_mesh','mesh/surface/stress',('global',)),
 ('n_neighs_mesh_top_mesh','property/atom',('global','per-atom')),('tracker_top_mesh','contacthistory/mesh',('global','per-atom')),
 ('contacthistory','contacthistory',('global','per-atom')))
ATOM_COLS=['id','type','x','y','z','vx','vy','vz','omegax','omegay','omegaz','radius']+[f'f_history_zwall_bot[{i}]' for i in range(1,5)]
GRIDS={'ps_0_10_r45':(5,1,1),'ps_3_7_r45':(2,2,1),'ps_5_5_r45':(5,1,1),'ps_7_3_r45':(6,4,1),'ps_10_0_r45':(11,1,1)}

def text(path):
    try:return Path(path).read_text(encoding='utf8')
    except (OSError,UnicodeError):return None

def screen_info(raw,np_=6):
    raw=raw or ''
    loops=[int(n) for n in re.findall(r'Loop time of [0-9.eE+-]+ on (\d+) procs',raw)]
    errors=any(line.lstrip().startswith(('ERROR','UL_ABORT')) or 'Segmentation fault' in line or 'MPI_ABORT' in line for line in raw.splitlines())
    resets=set(re.findall(r'^Resetting (global|per-atom) state of Fix (\S+) Style (\S+) from restart file info\s*$',raw,re.M))
    return {'technical':bool('LIGGGHTS-PUBLIC 3.8.0' in raw and '3d5c00f' in raw and loops and all(n==np_ for n in loops) and not errors),
            'loops':loops,'resets_ok':all((k,f,s) in resets for f,s,ks in RESETS for k in ks),
            'markers':[s.strip() for s in raw.splitlines() if s.startswith('UL_')]}

def stage(job,name,kind,manifest,*,bed,step):
    raw=text(Path(job)/name/'screen.txt');info=screen_info(raw)
    records=[s.strip() for s in (text(Path(job)/name/'run_check.txt') or '').splitlines() if s.strip()]
    valid=bool(records) and all(s==f'{kind} screen.txt PASS rc=0 procs=6' for s in records)
    lines=[s for s in (manifest or '').splitlines() if re.match(r'^stage='+re.escape(kind)+r'(?:\s|$)',s)]
    valid=valid and lines==[f'stage={kind} screen=screen.txt rc=0 check=PASS']
    marker=True
    if kind.startswith('RT'):
        marker=[s for s in info['markers'] if s.startswith('UL_RT_DONE')]==[f'UL_RT_DONE bed={bed} step={step}']
    elif kind in ('R','UNread'):
        marker=any(s.startswith('UL_R_DONE' if kind=='R' else 'UL_UN_DONE') for s in info['markers'])
    return {'ok':valid and info['technical'] and marker,'resets_ok':info['resets_ok'],'loops':info['loops']}

def post_list(folder,step):
    folder=Path(folder)
    try:
        return all(sorted(p.name for p in folder.iterdir() if p.name.startswith(prefix))==[f'{prefix}{step}.dump']
                   and (folder/f'{prefix}{step}.dump').is_file() for prefix in ('rt_pair_','rt_atom_'))
    except OSError:return False

def read_atoms(path,count=None):
    try:
        raw=Path(path).read_bytes();lines=raw.decode('ascii').splitlines()
        if len(lines)<9 or lines[0]!='ITEM: TIMESTEP' or lines[2]!='ITEM: NUMBER OF ATOMS' or lines[8]!='ITEM: ATOMS '+' '.join(ATOM_COLS):
            raise ValueError('header')
        if not re.fullmatch('[0-9]+',lines[1]) or not re.fullmatch('[0-9]+',lines[3]):raise ValueError('step/count')
        flags=lines[4].split()
        if flags[:3]!=['ITEM:','BOX','BOUNDS'] or len(flags)!=6 or any(not re.fullmatch('[pfsm]{2}',s) for s in flags[3:]):raise ValueError('bounds header')
        bounds=[list(map(N._finite,line.split())) for line in lines[5:8]]
        if any(len(b)!=2 or b[1]<=b[0] for b in bounds):raise ValueError('bounds')
        rows={}
        for line in lines[9:]:
            if not line.strip():continue
            words=line.split()
            if len(words)!=16:raise ValueError('width')
            values=list(map(N._finite,words));values[0]=N._id(words[0]);values[1]=N._id(words[1])
            if values[0] in rows:raise ValueError('duplicate ID')
            rows[values[0]]=values
        if len(rows)!=int(lines[3]) or (count is not None and len(rows)!=count):raise ValueError('count')
        return {'ok':True,'step':int(lines[1]),'rows':rows,'sha256':hashlib.sha256(raw).hexdigest()}
    except (OSError,ValueError,UnicodeError,ArithmeticError):
        return {'ok':False,'step':None,'rows':{}}

def atom_report(job,step,count):
    a,b=[read_atoms(Path(job)/s/'post'/f'rt_atom_{step}.dump',count) for s in ('RT1','RT2')]
    valid=a['ok'] and b['ok'] and a['step']==b['step']==step and a['rows'].keys()==b['rows'].keys()
    result={'read_ok':valid,'base12_bits_equal':None,'bottom4_bits_equal':None,'report_only':True}
    if valid:
        for key,lo,hi in [('base12_bits_equal',0,12),('bottom4_bits_equal',12,16)]:
            result[key]=all(struct.pack('!'+str(hi-lo)+'d',*a['rows'][i][lo:hi])==struct.pack('!'+str(hi-lo)+'d',*b['rows'][i][lo:hi]) for i in a['rows'])
    return result

def select_source(root,bed,job,step,ext,orig_log):
    root=Path(root)
    if bed not in GRIDS or job not in ('RJ','RJ2'):raise ValueError('unsupported bed/job')
    if job=='RJ':
        if Path(orig_log).name!=orig_log or orig_log in ('','.', '..'):raise ValueError('orig log basename')
        parent=root/bed/'in'
        return {'contact':parent/f'contact_{step}.liggghts','log':parent/orig_log,'grid':GRIDS[bed],'written_np':math.prod(GRIDS[bed])}
    if bed!='ps_10_0_r45':raise ValueError('RJ2 bed')
    matches=[name for name,key in [('EXT','s0p'),('EXT2','s0pp')] if type(ext.get(key)) is int and ext[key]==step]
    if len(matches)!=1:raise ValueError('one selected S0 writer required')
    parent=root/bed/matches[0]
    return {'contact':parent/'post'/f'contact_{step}.liggghts','log':parent/'screen.txt','grid':(3,2,1),'written_np':6}

def evaluate(job,*,bed,step,atoms,reference_contact,grid_text,grid,written_np,legacy_checks,job_kind='RJ'):
    job=Path(job);checks=dict(legacy_checks);manifest=text(job/'run_manifest.txt')
    stages={n:stage(job,n,k,manifest,bed=bed,step=step) for n,k in [('R','R'),('UN','UNread'),('RT1','RT1'),('RT2','RT2')]}
    if bed=='ps_7_3_r45' and job_kind=='RJ':stages['Ut0']=stage(job,'Ut0','Ut0',manifest,bed=bed,step=step)
    technical=all(s['ok'] for s in stages.values()) and checks.get('syntax',{}).get('ok') is True
    binding=B.check_binding(job,technical_ok=technical)
    checks['rt_technical']=stages;checks['rt_binding']=binding
    resets=all(stages[s]['resets_ok'] for s in ('R','RT1','RT2'))
    checks['rt_resets']={'ok':resets}
    inventory=all(post_list(job/s/'post',step) for s in ('RT1','RT2'))
    checks['rt_post_list']={'ok':inventory}
    checks['G2c_cont']=checks.pop('G2c',{'status':'NOT_COMPUTED'})
    report={'schema':'rt_restore_candidate_v1','restore_rule':'rev5_g2cp','bed':bed,'job':job_kind,'s0':step,
            'checks':checks,'operational_qualification':False,'certificate_published':False}
    if not technical or binding['status']=='SYNTAX_FAIL':
        for name in ('G2cp','cont_R','cont_RT1'):
            checks[name]={'status':'NOT_COMPUTED','reason':'technical/binding failure; RT values not read'}
        checks['rt_atoms']={'read_ok':False,'report_only':True,'reason':'technical/binding failure; not read'}
        report['status']='SYNTAX_FAIL';return report
    checks['rt_atoms']=atom_report(job,step,atoms) if inventory else {'read_ok':False,'report_only':True}
    checks['G2cp']=(N.g2cp_compare(job/'RT2/post'/f'rt_pair_{step}.dump',job/'RT1/post'/f'rt_pair_{step}.dump',expected_step=step)
                    if inventory and binding['status']=='PASS' else {'status':'NOT_COMPUTED','reason':'roundtrip binding/inventory incomplete'})
    for label,path,layout in [('cont_R',job/'R/g2'/f'contact_{step}.liggghts','legacy26'),
                              ('cont_RT1',job/'RT1/post'/f'rt_pair_{step}.dump','rt30')]:
        checks[label]=(N.cont_guard(path,reference_contact,expected_step=step,grid_text=grid_text or '',expected_grid=grid,expected_np=written_np,test_layout=layout)
                       if label=='cont_R' or post_list(job/'RT1/post',step) else {'status':'NOT_COMPUTED','reason':'RT1 inventory incomplete'})
    values=[checks.get(k,{}).get('status') for k in ('G1','G2','mesh_md5','G3','G2cp','cont_R','cont_RT1')]
    equal=checks.get('pre_post',{}).get('equal')
    if not technical or binding['status']=='SYNTAX_FAIL':status='SYNTAX_FAIL'
    elif not resets or checks.get('g0',{}).get('ok') is not True or equal is False or 'FAIL' in values:status='VALUE_MISMATCH'
    elif (binding['status']!='PASS' or not inventory or not all(x=='PASS' for x in values) or equal is not True
          or checks.get('history_test',{}).get('pass') is not True or checks.get('un_erasure',{}).get('seen') is not True):status='UNCONFIRMED'
    else:status='RESTORED'
    report['status']=status
    return report
