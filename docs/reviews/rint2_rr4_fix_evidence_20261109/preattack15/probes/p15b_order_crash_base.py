# -*- coding: utf-8 -*-
"""P15b — P15 와 같은 입력을 바탕 (e48e5fa04) 사슬 모듈로 (시험 도우미 = 고친 시험 파일 · 사슬 = 바탕) → 옛 동작 (깔끔한 멈춤인가)."""
import contextlib, importlib.util, io, json, sys, tempfile
from pathlib import Path
PA15 = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PA15 / 'tree' / 'scripts'))
import test_rint_r_chain as T  # noqa: E402
spec = importlib.util.spec_from_file_location('rint_r_chain_base', str(PA15 / 'base' / 'scripts' / 'rint_r_chain.py'))
RB = importlib.util.module_from_spec(spec)
sys.modules['rint_r_chain_base'] = RB
spec.loader.exec_module(RB)
T.RR = RB
T.TD = tempfile.mkdtemp(prefix='pa15b_', dir=str(PA15 / 'out' / 'td'))
with contextlib.redirect_stdout(io.StringIO()):
    T.fixtures()
out = {}
for nm, fn in (('runs_int', lambda s: s.update(runs=5)), ('stop_str', lambda s: s.update(stop='x'))):
    atts = T.rr4_two(f'P15b_{nm}', 'source-ceiling')
    lines = T.rr4_lines(atts)
    f2 = Path(atts[1][0])
    s = json.loads((f2 / 'ladder_summary.json').read_text(encoding='utf-8'))
    fn(s)
    (f2 / 'ladder_summary.json').write_bytes(RB.canon_bytes(s))
    r2 = [x for x in lines if x.get('kind') == 'result' and x['n'] == 2][0]
    r2['folder_sha256'] = RB.folder_digest(f2)
    st = RB.ledger_parse(''.join(RB.ledger_line(x) for x in lines).encode('utf-8'))
    for place, call in (('order', lambda: RB.attempt_order_problem(st, T.rr4_next(st), T.RR4_PLAN)),
                        ('chain', lambda: RB.resume_chain_problem(st, T.rr4_next(st), 3, f2.parent))):
        try:
            o = call()
            out[f'{nm}_{place}'] = ['returned', o[0] if o else None, (o[1][:120] if o else None)]
        except Exception as e:  # noqa: BLE001
            out[f'{nm}_{place}'] = ['EXC', f'{type(e).__name__}: {e}'[:160]]
(PA15 / 'out' / 'p15b_order_crash_base.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
print(json.dumps(out, ensure_ascii=False))
