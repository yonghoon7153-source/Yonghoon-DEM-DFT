"""New preparation timing tool; no candidate import or execution."""
from pathlib import Path
import sys,json,time,datetime
out=Path(__file__).resolve().parents[1]
origin=json.loads((out/'ORIGIN.json').read_text(encoding='utf-8-sig'))
start=origin['monotonic_ticks']/origin['frequency']
now=time.perf_counter(); elapsed=now-start
path=out/'PHASE_EVENTS.json'
events=json.loads(path.read_text(encoding='utf-8')) if path.exists() else [{'phase':'correction','start_elapsed_s':0,'limit_s':1200}]
last=events[-1]
if elapsed>2700 or elapsed-last['start_elapsed_s']>last['limit_s']:
    raise SystemExit('PREPARATION_BUDGET_EXCEEDED_NO_CONTINUATION')
if len(sys.argv)>1:
    next_phase=sys.argv[1]
    expected={'correction':'static','static':'plan_seal','plan_seal':'delivery'}
    assert expected.get(last['phase'])==next_phase
    last['end_elapsed_s']=elapsed;last['duration_s']=elapsed-last['start_elapsed_s'];last['within_limit']=last['duration_s']<=last['limit_s']
    events.append({'phase':next_phase,'start_elapsed_s':elapsed,'limit_s':origin['phase_limits'][next_phase]})
path.write_text(json.dumps(events,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'kind':'OFFLINE_PREPARATION_PHASE_BOUNDARY','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_s':elapsed,'total_limit_s':2700,'phase':events[-1]['phase'],'phase_limit_s':events[-1]['limit_s'],'candidate_executed':False}))
