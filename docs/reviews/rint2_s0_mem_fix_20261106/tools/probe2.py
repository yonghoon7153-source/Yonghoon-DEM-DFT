import atexit, faulthandler, json, os, runpy, signal, sys
#  11-06 메모리 재기 감싸개 (`docs/reviews/rint2_s0_mem_probe_20261106/` 의 probe.py) 그대로 + 끝에 carbon_junction 의 후보 검색 기록
#  (`_PAIR_SEARCH_LAST` · 선분 수 · 최대 선분 길이 · 옛 · 새 반지름 · 조각 수 · 후보 수 · 질의 덩어리 — 기하만 · σ 없음) 을
#  <stacks 파일과 같은 폴더>/pair_search.json 으로 남긴다 (정상 종료 · SystemExit 때 · 신호로 끝나면 남지 않는다).
f = open(sys.argv[1], 'w')
faulthandler.register(signal.SIGUSR1, file=f, all_threads=True)
_stats = os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), 'pair_search.json')


def _dump():
    m = sys.modules.get('carbon_junction')
    rec = getattr(m, '_PAIR_SEARCH_LAST', None) if m is not None else None
    with open(_stats, 'w') as g:
        json.dump(rec, g, indent=1, default=str)


atexit.register(_dump)
script = os.path.abspath(sys.argv[2])
sys.argv = sys.argv[2:]
sys.path.insert(0, os.path.dirname(script))
runpy.run_path(script, run_name='__main__')
