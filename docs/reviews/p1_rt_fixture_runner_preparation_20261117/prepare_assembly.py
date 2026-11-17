"""Assemble new inactive candidates; retain every preceding file byte for byte."""
import argparse,hashlib,importlib.util,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
HISTORY_SHA='c74d7da71b3426b812776e0060f7f72c9dcbc1d24e31af15062fe7f4c610bf02'
GUARD='echo "RT_ASSEMBLY_INACTIVE: no operational seal or author field GO" >&2\nexit 2\n'
def sha(b):return hashlib.sha256(b).hexdigest()
def edit(text,old,new):
    if text.count(old)!=1:raise ValueError('nonunique assembly anchor: '+old[:50])
    return text.replace(old,new,1)
def render_history(raw):
    if sha(raw)!=HISTORY_SHA:raise ValueError('historical history runner changed')
    t=raw.decode('utf8')
    t=edit(t,'set -uo pipefail\n','set -uo pipefail\n'+GUARD)
    t=edit(t,'PREFLIGHT_ONLY=0; NO_KIT=0; GRAMMAR_ONLY=0','PREFLIGHT_ONLY=0; NO_KIT=0; GRAMMAR_ONLY=0; RT_GRAMMAR_ONLY=0')
    t=edit(t,'--grammar-only) GRAMMAR_ONLY=1;;','--grammar-only) GRAMMAR_ONLY=1;; --rt-grammar-only) RT_GRAMMAR_ONLY=1;;')
    t=edit(t,'--preflight-only|--grammar-only) ;;','--preflight-only|--grammar-only|--rt-grammar-only) ;;')
    first=t.index('  for f in in.hist_producer.liggghts ')
    last=t.index('\n  ( cd "$SELF_DIR"',first)
    t=t[:first]+'''  while read -r _ f; do
    cp -p "$SELF_DIR/$f" "$KIT/" || die "candidate fixture copy failed: $f"
  done < "$SELF_DIR/RT_HISTORY_SNAPSHOT_SHA256SUMS"
  cp -p "$SELF_DIR/RT_HISTORY_SNAPSHOT_SHA256SUMS" "$KIT/" || die "candidate history list copy"
'''.rstrip()+t[last:]
    t=edit(t,'exec bash "$KIT/run_history.sh"','exec bash "$KIT/run_history_rt_candidate.sh"')
    anchor='  echo "  ✓ 묶음 SHA256SUMS"'
    t=edit(t,anchor,anchor+'''
  (cd "$KIT" && sha256sum -c --quiet RT_HISTORY_SNAPSHOT_SHA256SUMS) || die "history snapshot changed"
  if [ "$RT_GRAMMAR_ONLY" = 1 ]; then
    [ "$NP" = 6 ] || die "RT fixture requires NP6"
    (cd "$KIT" && sha256sum -c --quiet RT_CANDIDATE_SHA256SUMS) || die "RT candidate identity changed"
  fi''')
    t=edit(t,'MODE=hist; [ "$GRAMMAR_ONLY" = 1 ] && MODE=gram','MODE=hist; [ "$GRAMMAR_ONLY" = 1 ] && MODE=gram\n[ "$RT_GRAMMAR_ONLY" = 1 ] && MODE=rt_grammar')
    anchor='  echo "sums_sha256=$(sha256sum "$KIT/SHA256SUMS" | cut -d\' \' -f1)"'
    t=edit(t,anchor,'''  HSUMS=SHA256SUMS; [ "$RT_GRAMMAR_ONLY" != 1 ] || HSUMS=RT_CANDIDATE_SHA256SUMS
  echo "sums_sha256=$(sha256sum "$KIT/$HSUMS" | cut -d' ' -f1)"
  echo "job_dir=$RUN"''')
    t=edit(t,'mkdir -p "$dir/producer" "$dir/restart" "$dir/probe"','mkdir -p "$dir/producer" "$dir/restart" "$dir/probe" "$dir/post" "$dir/obs"')
    t=edit(t,'if [ "$GRAMMAR_ONLY" = 1 ]; then\n',(HERE/'rt_fixture_flow.sh').read_text(encoding='utf8')+'\nif [ "$GRAMMAR_ONLY" = 1 ]; then\n')
    return t.encode('utf8')
def render_unload(raw):
    t=raw.decode('utf8')
    old='echo "RT_RUNNER_LAYER_ONLY: rev5 consumer, publisher and RT grammar prerequisite not integrated" >&2\nexit 2\n'
    t=edit(t,old,GUARD)
    t=edit(t,'done < "$SELF_DIR/SHA256SUMS"','done < "$SELF_DIR/RT_ASSEMBLY_SHA256SUMS"')
    t=edit(t,'cp -p "$SELF_DIR/SHA256SUMS" "$KIT/"','cp -p "$SELF_DIR/RT_ASSEMBLY_SHA256SUMS" "$KIT/"')
    t=edit(t,'exec bash "$KIT/run_unload.sh"','exec bash "$KIT/run_unload_rt_candidate.sh"')
    t=edit(t,'  echo "  ✓ 묶음 SHA256SUMS"','  echo "  ✓ 묶음 SHA256SUMS"\n  (cd "$KIT" && sha256sum -c --quiet RT_ASSEMBLY_SHA256SUMS) || die "candidate assembly changed"')
    t=edit(t,'  grammar_check\n','  grammar_check\n  rt_prerequisites\n')
    t=edit(t,'preflight() {\n',(HERE/'rt_prerequisites.sh').read_text(encoding='utf8')+'\npreflight() {\n')
    t=edit(t,'"$KIT/ul_reader.py" gate','"$KIT/rt_dispatch.py" gate')
    t=edit(t,'"$KIT/ul_reader.py" "$cmd"','"$KIT/rt_dispatch.py" "$cmd"')
    t=edit(t,'echo "sums_sha256=$(sha256sum "$KIT/SHA256SUMS"','echo "sums_sha256=$(sha256sum "$KIT/RT_ASSEMBLY_SHA256SUMS"')
    return t.encode('utf8')
def build(source,output):
    source=Path(source);output=Path(output)
    history=render_history((source/'history_test/run_history.sh').read_bytes())
    p=HERE.parent/'p1_rt_consumer_preparation_20261117/prepare_consumer.py'
    s=importlib.util.spec_from_file_location('consumer_builder',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
    m.build(source,output)
    additions={'history_test/run_history_rt_candidate.sh':history,
               'run_unload_rt_candidate.sh':render_unload((output/'run_unload_rt_dev.sh').read_bytes()),
               'rt_dispatch.py':(HERE/'rt_dispatch.py').read_bytes()}
    for name,b in additions.items():
        with (output/name).open('xb') as f:f.write(b)
    hdir=output/'history_test';hfiles=sorted(p for p in hdir.iterdir() if p.is_file())
    with (hdir/'RT_HISTORY_SNAPSHOT_SHA256SUMS').open('xb') as f:
        f.write(''.join(sha(p.read_bytes())+'  '+p.name+'\n' for p in hfiles).encode('ascii'))
    report={'schema':'rt_assembly_candidate_v1','operational_kit_ready':False,'runner_entry_closed':True,
            'engine_runs':0,'previous_files_preserved':122,'history_original_sha256':HISTORY_SHA,
            'new_sources':{n:sha(b) for n,b in additions.items()},
            'history_snapshot_files':len(hfiles),'dispatch':'rev5 only for restore and certificate gate',
            'remaining':['complete kit preseal review','operational identities/qualification','author field GO']}
    with (output/'RT_ASSEMBLY_LAYER.json').open('xb') as f:f.write((json.dumps(report,indent=2)+'\n').encode())
    files=sorted(p for p in output.rglob('*') if p.is_file())
    with (output/'RT_ASSEMBLY_SHA256SUMS').open('xb') as f:
        f.write(''.join(sha(p.read_bytes())+'  '+p.relative_to(output).as_posix()+'\n' for p in files).encode('ascii'))
    return report
def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();print(json.dumps(build(a.source,a.output),indent=2))
if __name__=='__main__':main()
