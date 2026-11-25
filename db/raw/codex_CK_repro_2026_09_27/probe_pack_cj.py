"""CJ packaging audit: unmodified deployed runner, synthetic text, PACK_ONLY only.
Usage: python probe_pack_cj.py --source CHECKOUT --bash /bin/bash
No scientific calculations, no source changes. Faults are Bash functions in BASH_ENV.
"""
import argparse, hashlib, json, os, shutil, subprocess, tempfile, tarfile
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,default=Path(__file__).parent/'source');ap.add_argument('--bash',default=shutil.which('bash') or 'bash');ap.add_argument('--assert-fixed',action='store_true');a=ap.parse_args()
HERE=Path(__file__).resolve().parent;PKG=a.source.resolve()/'db/inputs/wad_aprime_v5_vasp_2026_09_27'
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8',newline='\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
results={}
def emit(k,v):
    results[k]=v;(HERE/'pack_cj_results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8');print(k,json.dumps(v,ensure_ascii=False),flush=True)
env={**os.environ,'PACK_ONLY':'1','PYTHONUTF8':'1'};env.pop('BASH_ENV',None)
if os.name=='nt':env['PATH']=str(Path(a.bash).resolve().parent.parent/'usr/bin')+os.pathsep+env.get('PATH','')
with tempfile.TemporaryDirectory(prefix='cj_pack_',dir=HERE) as tmp:
    T=Path(tmp);w=T/'pkg';shutil.copytree(PKG,w)
    for n in ('V5_s_outer_A_bound','V5_s_outer_A_far'):
        for f in ('OUTCAR','OSZICAR','INCAR','KPOINTS','POSCAR','IBZKPT','POTCAR.titel','POTCAR.sha256','POTCAR.species.sha256','attempt.json','stdout.log'):
            write(w/'run'/n/f,'REVIEW SYNTHETIC TEXT ONLY\n')
    write(w/'run/env.txt','synthetic environment\n');write(w/'run/status.tsv','synthetic status\n')
    def run(label,body=None,wd=None):
        wd=wd or w;e=env.copy()
        if body:
            f=T/(label+'.sh');write(f,body);e['BASH_ENV']=f.as_posix()
        cp=subprocess.run([a.bash,(wd/'run_all.sh').as_posix()],env=e,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=45)
        names=[]
        if (wd/'V5_vasp_return.tgz').exists():
            with tarfile.open(wd/'V5_vasp_return.tgz') as tf:names=tf.getnames()
        sh=T/'check.sh';write(sh,'#!/usr/bin/env bash\nsha256sum -c V5_vasp_return.tgz.sha256\n')
        hc=subprocess.run([a.bash,sh.as_posix()],cwd=wd,env=env,capture_output=True,text=True,timeout=30)
        diag={}
        for name in ('members','list.sorted','members.sorted'):
            p=wd/'V5_vasp_return.tmp'/name
            if p.exists():
                b=p.read_bytes();diag[name]={'crlf':b.count(b'\r\n'),'lf':b.count(b'\n'),'head_repr':repr(b[:220])}
        return {'rc':cp.returncode,'success_message':'✅' in cp.stdout,'members':names,'sha_check_rc':hc.returncode,
          'parts_present':[p.name for p in wd.glob('*.part')],'comparison_diagnostics':diag,'log':cp.stdout+cp.stderr}
    emit('positive',run('positive'))
    pair={f:(w/f).read_bytes() for f in ('V5_vasp_return.tgz','V5_vasp_return.tgz.sha256')}
    cases={
      'find_error':'find(){ echo INJ_FIND >&2; return 73; }\n',
      'allow_grep_error':'grep(){ case "$*" in *found*) return 2;; esac; command grep "$@"; }\n',
      'allow_sort_error':'sort(){ case "$*" in *allowed*) return 73;; esac; command sort "$@"; }\n',
      'tar_create_error':'tar(){ if [ "$1" = czf ]; then return 73; fi; command tar "$@"; }\n',
      'tar_list_output_then_error':'tar(){ command tar "$@"; r=$?; if [ "$1" = tzf ]; then return 73; fi; return "$r"; }\n',
      'forbid_grep_error':'grep(){ case "$*" in *members*) return 2;; esac; command grep "$@"; }\n',
      'members_sort_error':'sort(){ case "$*" in *members*) return 73;; esac; command sort "$@"; }\n',
      'list_sort_error':'sort(){ case "$*" in *return.list*) return 73;; esac; command sort "$@"; }\n',
      'cmp_error':'cmp(){ return 2; }\n',
      'list_cat_error':'cat(){ case "$*" in *mgmt*) return 73;; esac; command cat "$@"; }\n',
      'sha_empty':'sha256sum(){ case "$*" in *tgz.part*) return 73;; esac; command sha256sum "$@"; }\n',
      'sha_valid_output_then_error':'sha256sum(){ command sha256sum "$@"; r=$?; case "$*" in *tgz.part*) echo INJ_HASH_READ_CLOSE_ERROR >&2; return 73;; esac; return "$r"; }\n',
      'sha_nonhex64':'sha256sum(){ case "$*" in *tgz.part*) printf "%064d  %s\\n" 0 "$1" | tr 0 z; return 0;; esac; command sha256sum "$@"; }\n',
      'mgmt_echo_error':'echo(){ case "$*" in run/env.txt|run/status.tsv) printf "INJ_MANAGEMENT_LIST_WRITE_ERROR\\n" >&2; return 73;; esac; builtin echo "$@"; }\n',
      'manifest_echo_error':'echo(){ if [ "$*" = MANIFEST.sha256 ]; then printf "INJ_MANIFEST_LIST_WRITE_ERROR\\n" >&2; return 73; fi; builtin echo "$@"; }\n',
      'first_mv_error':'mv(){ case "$*" in *tgz.part*) return 73;; esac; command mv "$@"; }\n',
      'second_mv_error':'mv(){ case "$*" in *sha256.part*) return 73;; esac; command mv "$@"; }\n',
    }
    for label,body in cases.items():
        for f,b in pair.items():(w/f).write_bytes(b)
        r=run(label,body);r['old_pair_preserved']=all((w/f).read_bytes()==b for f,b in pair.items())
        r['required_existing_files_omitted']=[f for f in ('MANIFEST.sha256','run/env.txt','run/status.tsv') if f not in r['members']]
        emit(label,r)
    emit('recovery',run('recovery'))
    empty=T/'empty';shutil.copytree(PKG,empty);write(empty/'run/env.txt','synthetic empty run\n')
    emit('empty_run',run('empty_run',wd=empty))
    if os.name=='nt' and Path('C:/Windows/System32/tar.exe').is_file():
        emit('windows_bsdtar',run('windows_bsdtar','tar(){ /c/Windows/System32/tar.exe "$@"; }\n'))
    # Enumerate cleanup semantics without weakening a scientific gate.
    for f,b in pair.items():(w/f).write_bytes(b)
    emit('post_promotion_cleanup_error',run('cleanup_error','rm(){ if [ "$#" = 2 ] && [ "$2" = V5_vasp_return.tmp ]; then echo INJ_FINAL_CLEANUP >&2; return 73; fi; command rm "$@"; }\n'))
    emit('unchanged_source',{'manifest':sha(PKG/'MANIFEST.sha256'),'runner':sha(PKG/'run_all.sh')})
    if a.assert_fixed:
        for label in ('mgmt_echo_error','manifest_echo_error'):
            r=results[label]
            assert r['rc']==4 and not r['success_message'] and r['old_pair_preserved'], (label,r)
